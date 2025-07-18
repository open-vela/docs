# ARM Cortex-M 系列中断嵌套

\[ [English](../../../../en/device_dev_guide/kernel/scheduling_interrupts/ARM_Cortex-M_Series_Interrupt_Nesting.md) | 简体中文 \]

## 一、简介

本文介绍 openvela 系统中 ARM Cortex-M 系列中断嵌套的支持情况，以及在新平台移植过程中支持中断嵌套需要注意的事项。同时，系统开发者在实现中断处理时需要特别关注的关键点也会在本文中详细说明。

## 二、ARM Cortex-M 系列中断嵌套方式

### 1、零延迟高优先级中断嵌套

在以下两种情况下，系统支持零延迟中断嵌套：

- 无中断栈，只有进程栈。

    - 默认支持中断嵌套。
    - 正常情况下和触发中断异常时都使用由 MSP（Main Stack Pointer）指向的当前进程栈。
    - 需要注意：此模式可能需要配置更大的进程栈。

- 有中断栈。

    - 需要配置 `CONFIG_ARCH_INTERRUPTSTACK`（详情请参见 [CONFIG 配置](#1config-配置)）。
    - Handler 模式（触发中断/异常时进入）：硬件会自动切换到 MSP，系统初始化完成后，MSP 始终指向中断栈，中断/异常处理过程运行在中断栈上。
    - Thread 模式（正常进程执行时进入）：使用 PSP（Process Stack Pointer），系统初始化完成后，PSP 始终指向当前进程栈，进程执行过程运行在进程栈上。
    - 系统复位（Reset）后：
        - 系统处于 Thread 模式，特权等级，硬件默认使用 MSP，MSP 默认指向 `_vectors` 表中的 `IDLE_STACK`（详情请参见 [系统初始化](#2系统初始化)）。
        - 系统初始化过程中会调整 MSP 和 PSP，将 MSP 指向中断栈顶，PSP 指向 IDLE 进程栈的当前位置。

#### 零延迟中断优先级排布

零延迟中断优先级的排布如下图所示：

![img](./figures/001.png)

注意事项：

- 系统 API 调用限制：在零延迟中断中，无法在 ISR（Interrupt Service Routine）中调用系统 API，但高优先级中断可以实现零延迟（Zero latency）。

- 特殊处理方式：虽然无法调用系统 API，但可以通过触发注册的 PendSV（Pendable Service Call） 回调来完成一些特殊处理。

    ```C
    # 初始化时注册 pendsv
    irq_attach(NVIC_IRQ_PENDSV, pendsv_callback, NULL);
    up_enable_irq(NVIC_IRQ_PENDSV);
    
    # 在需要的时候触发/清除 pendsv
    up_trigger_irq(NVIC_IRQ_PENDSV, 0);
    ```

   > 说明
   >
   > 由于上下文切换时也会触发 PendSV，需要在 PendSV 的 ISR 中判断是系统触发还是 ISR 自行触发。

### 2、可屏蔽的中断嵌套

ARM Cortex-M 系列支持 BASEPRI（Base Priority Register） 功能，用于禁用某个优先级以下的中断。这一功能可以实现**可屏蔽的嵌套中断**。

#### 特性说明

- 可屏蔽的嵌套中断遵循系统的中断屏蔽机制。
- 设置 `BASEPRI` 寄存器为特定阈值后，所有优先级低于或等于该值的中断将被屏蔽。
- 高优先级中断（如不可屏蔽中断或零延迟中断）不受屏蔽影响。

#### 可屏蔽中断优先级排布

可屏蔽中断优先级的排布如下图所示：

![img](./figures/002.png)

注意事项：

- 在可屏蔽中断中，可以在 ISR 中调用系统 API，但会受到关中断的影响。

## 三、新平台移植注意事项

### 1、CONFIG 配置

- 未配置中断栈：如果未配置中断栈，进程栈默认支持中断嵌套，无需额外配置。
- 配置中断栈：如果配置了中断栈（`CONFIG_ARCH_INTERRUPTSTACK=xxxx`），默认情况下不支持中断嵌套。

### 2、系统初始化

系统默认配置了 `_vectors` 表。如果没有特殊需求，请使用系统默认初始化的 `_vectors` 表。默认配置包括以下内容：

1. Idle 进程栈：`IDLE_STACK`。
2. Reset 入口：`__start`。
3. 通用中断处理子系统入口：`exception_common`。
4. 上下文更少且支持嵌套的中断入口：`exception_direct`。

以下是 `_vectors` 表的示例代码：

```C
const void * const _vectors[] locate_data(".vectors") =
{
  /* Initial stack */

  IDLE_STACK,

  /* Reset exception handler */

  __start,

  /* Vectors 2 - n point directly at the generic handler */
  
  [2 ... NVIC_IRQ_PENDSV] = &exception_common,
  [(NVIC_IRQ_PENDSV + 1) ... (15 + XXXX_PERIPHERAL_INTERRUPTS)]
                          = &exception_direct
};
```

### 3、新平台移植要求

#### 未开启中断栈的情况

在未开启中断栈的情况下，新平台移植需要满足以下要求：

1. 硬件复位后的状态：
    - `CONTROL.SELSP = 0`，默认使用 MSP，并指向 `IDLE_STACK`。
    - 系统此时处于 Thread 模式，特权等级。
2. Reset 入口实现：
    - 在 vendor 代码中实现 Reset 入口 `__start` 时，应保持以上状态。
    - 在整个系统运行过程中始终使用 MSP，不能使用 PSP（Process Stack Pointer，进程栈指针）。

#### 开启中断栈的情况

在开启中断栈的情况下，新平台移植需要满足以下要求：

1. 硬件复位后的状态：
     - `CONTROL.SELSP = 0`，默认使用 MSP，并指向 `IDLE_STACK`。
     - 系统此时处于 Thread 模式，特权等级。
2. Reset 入口实现：
     - 在 vendor 代码中实现 Reset 入口 `__start` 时，应保持以上状态。
     - 在系统初始化过程中，会调用 `arm_initialize_stack` 切换栈：
         - 将 MSP 指向中断栈顶。
         - 将 PSP 指向 `IDLE` 进程栈的当前位置。
         - 设置 `CONTROL.SELSP = 1`，启用 PSP。
         - ARMv8-M 还需要设置 PSPLIM 和 MSPLIM。
3. 支持 OTA 的情况： 如果支持 OTA，可能存在多个固件（如 `boot`、`ota`、`ap` 等）。在 `boot` 跳转到 `ap` 运行时，需要注意以下事项：
    - 跳转前的状态：
         - `CONTROL.SELSP = 1`，使用 PSP 指向 `boot` 的进程栈。
         - MSP 指向 `boot` 的中断栈。
    - 跳转到 `ap` 的要求：
         - 需要正确设置栈指针寄存器，确保当前使用的栈指针指向 `ap` 的 `IDLE` 进程栈。
         - 以下是两种常见情况：
             - `CONTROL.SELSP = 1`：使用 PSP 指向 `ap` 的 `IDLE` 栈。（ARMv8-M 还需要设置 PSPLIM）。
             - `CONTROL.SELSP = 0`：使用 MSP 指向 `ap` 的 `IDLE` 栈。（ARMv8-M 还需要设置 MSPLIM）。
    - Reset 入口实现的注意事项：
         - 需要注意，进入 `__start` 时可能并非硬件复位状态，因此需要额外处理。

### 4、中断优先级设置

#### BASEPRI 支持情况

- ARMv6-M：不支持 BASEPRI（Base Priority Register），仅支持 NMI（Non-Maskable Interrupt）。
- ARMv7-M 和 ARMv8-M：支持 BASEPRI，可以根据具体需求设置不同优先级的中断。

#### 中断优先级配置示例

下是通过 `Makefile` 配置高优先级中断的示例代码：

```Makefile
# 配置支持高优先级中断
CONFIG_ARCH_HIPRI_INTERRUPT=y

# ARMV7-M
# 在配置 CONFIG_ARCH_HIPRI_INTERRUPT 的情况下被默认配置
# 依赖配置：CONFIG_ARCH_CORTEXM3、CONFIG_ARCH_CORTEXM4、CONFIG_ARCH_CORTEXM7
CONFIG_ARMV7M_USEBASEPRI=y

# ARMV8-M
# 在配置 CONFIG_ARCH_HIPRI_INTERRUPT 的情况下被默认配置
CONFIG_ARMV8M_USEBASEPRI=y
```

