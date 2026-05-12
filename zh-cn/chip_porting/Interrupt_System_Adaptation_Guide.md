# 中断系统适配指南

\[ [English](../../en/chip_porting/Interrupt_System_Adaptation_Guide.md) | 简体中文 \]

## 一、实现芯片中断调试

在调试芯片中断子系统（`bringup`）时，厂商需要实现一系列与架构相关的函数（`arch` 函数），以完成以下任务：

- 初始化中断
- 启用和禁用中断
- 设置中断优先级

以下内容提供了具体的要求和实现示例。

### 1、需要实现的中断相关函数

以下是厂商（ Vendor）需要实现的中断相关函数及其功能说明。

1. 初始化中断系统，包括禁用所有中断、配置向量表位置、设置默认优先级以及启用中断。

    ```C
    void up_irqinitialize(void)
    {
        // Disable all interrupts
        // Set the NVIC vector location
        // Set all interrupts (and exceptions) to the default priority
        // Attach the SVCall and Hard Fault exception handlers
        // enable interrupts
    }
    ```

2. 启用指定中断。

    ```C
    void up_enable_irq(int irq)
    {
        //enable interrupt with irq
    }
      ```

3. 禁用指定的中断号。

    ```C
    void up_disable_irq(int irq)
    {
        //disable interrupt with irq
    }
    ```

4. 设置中断优先级。 如果启用了 `CONFIG_ARCH_IRQPRIO` 配置，则需要实现以下函数：

    ```C
    #ifdef CONFIG_ARCH_IRQPRIO
    int up_prioritize_irq(int irq, int priority)
    {
        // set irq priority
    }
    #endif
    ```

5. 管理中断状态。

    - 判断 `flags` 当前是否是关中断状态。

        ```C
        #define up_irq_is_disabled(flags)
        ```

    - 保存当前中断状态并关闭中断。

        ```C
        // 关中断
        irqstate_t up_irq_save(void)
        {
        }
        ```

    - 恢复指定中断状态。

        ```C
        // 恢复flags表示的中断状态
        void up_irq_restore(irqstate_t flags)
        {
        }
        ```

    - 开启所有中断。

        ```C
        // 开启所有中断
        irqstate_t up_irq_enable(void)
        {
        }
        ```

    - 获取当前中断状态。

        ```C
        // 获取当前中断状态
        irqstate_t irqstate(void)
        {
        }
        ```

6. 处理核间中断：

    ```C
    // 发起核间中断
    void up_trigger_irq(int irq, cpu_set_t cpuset)
    ```

7. 设置中断的安全属性。

    - 设置指定中断的安全属性。

        ```C
        // 设置中断安全属性
        void up_secure_irq(int irq, bool secure)
        ```

    - 改变所有中断的安全属性。

        ```C
        // 改变所有中断安全属性
        void up_secure_irq_all(bool secure)
        ```

### 2、需要定义的中断相关宏

除上面的函数实现，厂商还需定义一系列中断相关的宏，用于描述 NVIC（Nested vectored interrupt controller） 的配置，这些宏需定义在`chips/chip_name/include/irq.h` 文件中。可参考 [RTL8720C 示例](../../../../../nuttx/blob/dev-ai-contest-2026/arch/arm/src/rtl8720c/include/irq.h)。

以下是必须实现的宏及其功能说明：

1. 第一个中断向量号。

    ```C
    #define NVIC_IRQ_FIRST  (16)   /* Vector number of the first interrupt */
    ```

2. 中断数量。

    ```C
    #define NR_IRQS (64)
    ```

3. NVIC 优先级级别。

    - 最低优先级

        ```C
        #define NVIC_SYSH_PRIORITY_MIN  0xff /* All bits set in minimum priority */
        ```

    - 默认优先级

        ```C
        #define NVIC_SYSH_PRIORITY_DEFAULT  0x40 /* Midpoint is the default */
        ```

    - 最高优先级

        ```C
        #define NVIC_SYSH_PRIORITY_MAX   0x00 /* Zero is maximum priority */
        ```

    - 优先级步长

        ```C
        #define NVIC_SYSH_PRIORITY_STEP 0x40 /* Three bits priority used, bits[7-6] as group */
        ```

    - 子优先级步长

        ```C
        #define NVIC_SYSH_PRIORITY_SUBSTEP  0x20 /* Three bits priority used, bit[5] as sub */
        ```

## 二、中断绑定处理函数

在中断处理过程中，可以通过以下三种方式绑定处理函数。每种方式适用于不同场景，具有各自的优缺点。

### 1、使用`irq_attach`

```C
int irq_attach(int irq, xcpt_t isr, FAR void *arg)
```

1. 工作机制。

    - 当中断触发时，`isr` 在中断上下文中被调用。
    - 这种方式的优点是效率高，因为中断处理直接在中断上下文中完成。
    - `isr` 执行期间会屏蔽所有中断应，对实时性要求较高的系统不太合适。
    - `isr`中不能调用会导致阻塞的 API（例如 `sleep`、`wait` 等）。

2. 解除绑定。

    ```C
    irq_detach(irq)
    ```

3. 优缺点。

    - 优点：处理效率高。
    - 缺点：中断处理期间屏蔽所有中断，影响系统实时性。

### 2、使用`irq_attach_thread`

```C
int irq_attach_thread(int irq, xcpt_t isr, xcpt_t isrthread, FAR void *arg, int priority, int stack_size)
```

1. 工作机制。

    - 用户需提供 1 个或者 2 个处理函数：
        - `isr` 在中断上下文中被调用，通常用于屏蔽当前中断并快速唤醒 `isrthread`。
        - `isrthread` 在线程上下文中被调用，用于处理剩余中断任务。
    - 如果 `isr` 为 `NULL`，会直接调用 `isrthread`。

2. 优势。

    - `isr` 的执行时间被尽可能缩短，从而提升系统实时性。
    - `isrthread` 作为线程运行，支持优先级调度，可以被其他高优先级任务抢占。

3. 劣势。

    - 消耗更多内存（独立线程栈和中断线程结构体）。
    - 增加一次上下文切换，降低效率。
    - 中断处理完成时间会有一定延迟（约 5 微秒）。

4. 解除绑定。

    ```C
    irq_detach_thread(irq)
    ```

### 3、使用`irq_attach_wqueue`

```C
int irq_attach_wqueue(int irq, xcpt_t isr, xcpt_t isrwork, FAR void *arg, int priority)
```

1. 工作机制。

    - 用户需提供 1 个或 2 个处理函数：
        - `isr` 在中断上下文中被调用。
        - `isrwork` 在工作队列上下文中被调用。
    - 与 `irq_attach_thread` 的区别在于，`isrwork` 在工作队列中被执行，而不是独立线程中。

2. 优势。

    - 多个优先级相同的中断可以复用同一个工作队列，从而节省内存。
    - 高优先级的工作队列可以抢占低优先级队列。
    - 如果中断数量较多，比 `irq_attach_thread` 更节省内存。

3. 劣势。
    - 如果只有一个中断，工作队列的创建会带来额外开销。
    - 在多核系统中，控制线程属性和数量的灵活性较差。

4. 解除绑定。

    ```C
    irq_detach_wqueue(irq)
    ```

### 总结对比

| 绑定方式          | 优点                             | 缺点                                               | 使用场景                             |
| :---------------- | :------------------------------- | :------------------------------------------------- | :----------------------------------- |
| irq_attach        | 效率高，直接在中断上下文中处理。 | 中断期间屏蔽所有中断，不适合实时性要求高的系统。   | 处理逻辑简单、实时性要求不高的场景。 |
| irq_attach_thread | 提升实时性，支持优先级调度。     | 消耗更多内存，增加上下文切换，处理完成有一定延迟。 | 实时性要求高的场景。                 |
| irq_attach_wqueue | 节省内存，支持工作队列复用。     | 单一中断场景效率低，多核场景灵活性不足。           | 中断数量多、内存资源有限的场景。     |

## 三、中断线程/工作队列的实现示例

以下是绑定中断并实现中断线程或工作队列的示例代码。

### 1、绑定中断

使用 `irq_attach_work` 函数绑定中断处理程序：

```C
irq_attach_work(IRQ, isrhandle, isrwork, arg, 253)
```

- `isrhandle`：中断处理函数，在中断上下文中执行。
- `isrwork`：中断线程或工作队列处理函数，在线程上下文中执行。
- `arg`：传递给处理函数的参数。
- `253`：优先级设置。

### 2、中断处理函数示例

在 `isrhandle` 中返回 `IRQ_WAKE_THREAD`，以唤醒中断线程或工作队列。如果返回 `OK`，则不会唤醒中断线程。示例代码如下：

```C
static int isrhandle(int irq, void *regs, void *arg)  
{  
    up_disabled_irq(irq); // 屏蔽中断，确保退出后中断不会再次触发  
    return IRQ_WAKE_THREAD; // 唤醒中断线程或工作队列  
}
```

### 3、中断线程/工作队列处理函数示例

`isrwork` 用于处理中断任务，并在完成后清除中断状态。示例代码如下：

```C
static int isrwork(int irq, void *regs, void *arg)
{
  // 执行中断处理逻辑
  // 清除中断的pending位
  up_enabled_irq(irq); // 重新使能中断。
  return OK;
}
```

### 4、特殊情况：One-shot 中断

对于一些 one-shot 中断，可以将 `isrhandle` 设置为 `NULL`，直接使用 `isrwork` 处理中断任务。

## 四、中断结构体优化

在中断使用时，系统通常会定义一个全局中断结构体数组：

```C
struct irq_info_s g_irqvector[NR_IRQS];
```

其中，`NR_IRQS` 表示系统支持的最大中断号，通常大于 200。然而，实际使用的中断数量通常只有十几个，并且这些中断号是离散分布的。这种设计会导致以下问题：

- 内存浪费：即使只使用少量中断，也需要为所有可能的中断号分配内存，存储 `NR_IRQS` 个结构体。
- 低效资源利用：大部分中断号对应的结构体未被使用，造成资源浪费。

### 1、优化策略与实现原理

为了解决上述问题，可以通过如下动态映射的方式优化中断结构体的存储。

#### 映射关系数组

定义一个映射关系数组，用于动态建立中断号与中断结构体的映射：

```C
irq_mapped_t g_irqmap[NR_IRQS]
```

- 该数组仅占用 `NR_IRQS` 字节的额外内存。
- 在中断使用时，动态建立映射关系。

#### 精简中断结构体数组

将 `g_irqvector` 定义为：

```C
struct irq_info_s g_irqvector[CONFIG_ARCH_NUSER_INTERRUPTS];
```

- `CONFIG_ARCH_NUSER_INTERRUPTS` 表示系统中可能使用的最大中断数量加 1 。
- 通过限制数组大小，仅为实际可能使用的中断分配内存。

#### 中断使用统计

使用 `g_irqmap_count` 统计当前已使用的中断数量，便于监控和调试。

### 2、配置示例

通过以下宏配置启用优化：

```Makefile
CONFIG_ARCH_MINIMAL_VECTORTABLE_DYNAMINC=y
CONFIG_ARCH_MINIMAL_VECTORTABLE=y
CONFIG_ARCH_NUSER_INTERRUPTS=24
```

- `CONFIG_ARCH_MINIMAL_VECTORTABLE_DYNAMIC`：启用动态映射功能。
- `CONFIG_ARCH_MINIMAL_VECTORTABLE`：启用精简中断向量表。
- `CONFIG_ARCH_NUSER_INTERRUPTS`：设置最大可能使用的中断数量。

### 3、优化效果

- 内存节省：仅为实际使用的中断分配存储空间，避免为未使用的中断号浪费内存。
- 灵活性提升：通过动态映射关系，支持离散分布的中断号。
- 可扩展性：通过配置宏灵活调整中断数量限制。

## 五、相关仓

- [nuttx](../../../../../nuttx)
