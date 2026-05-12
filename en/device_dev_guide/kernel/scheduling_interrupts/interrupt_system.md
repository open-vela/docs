# Interrupt System

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/kernel/scheduling_interrupts/interrupt_system.md) \]

## I. Implementing Chip Interrupt Debugging

When debugging the chip interrupt subsystem (`bringup`), the manufacturer needs to implement a series of architecture-related functions (`arch` functions) to complete the following tasks:

- Initialize interrupts
- Enable and disable interrupts
- Set interrupt priorities

The following content provides specific requirements and implementation examples.

### 1. Interrupt-Related Functions to be Implemented

The following are the interrupt-related functions that the vendor needs to implement and their functional descriptions.

#### 1. Initialize the interrupt system, including disabling all interrupts, configuring the vector table location, setting the default priority, and enabling interrupts.

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

#### 2. Enable a specified interrupt

```C
void up_enable_irq(int irq)
{
   //enable interrupt with irq
}
```

This function is used to enable the specified interrupt number.

#### 3. Disable the specified interrupt number

```C
void up_disable_irq(int irq)
{
   //disable interrupt with irq
}
```

#### 4. Set interrupt priority

If the `CONFIG_ARCH_IRQPRIO` configuration is enabled, the following function needs to be implemented:

```C
#ifdef CONFIG_ARCH_IRQPRIO
int up_prioritize_irq(int irq, int priority)
{
  // set irq priority
}
#endif
```

#### 5. Manage interrupt status

- Determine whether the `flags` are currently in the interrupt-disabled state.

    ```C
    #define up_irq_is_disabled(flags)
    ```

- Save the current interrupt status and disable interrupts.

    ```C
    // Disable interrupts
    irqstate_t up_irq_save(void)
    {
    }
    ```

- Restore the specified interrupt status.

    ```C
    // Restore the interrupt status represented by flags
    void up_irq_restore(irqstate_t flags)
    {
    }
    ```

- Enable all interrupts.

    ```C
    // Enable all interrupts
    irqstate_t up_irq_enable(void)
    {
    }
    ```

- Obtain the current interrupt status.

    ```C
    // Obtain the current interrupt status
    irqstate_t irqstate(void)
    {
    }
    ```

#### 6. Handle inter-processor interrupts

```C
// Trigger an inter-processor interrupt
void up_trigger_irq(int irq, cpu_set_t cpuset)
```

#### 7. Set the security attributes of interrupts

- Set the security attributes of a specified interrupt.

    ```C
    // Set the security attributes of an interrupt
    void up_secure_irq(int irq, bool secure)
    ```

- Change the security attributes of all interrupts.

    ```C
    // Change the security attributes of all interrupts
    void up_secure_irq_all(bool secure)
    ```

### 2. Interrupt-Related Macros to be Defined

In addition to the above function implementations, the manufacturer also needs to define a series of interrupt-related macros to describe the configuration of the NVIC (Nested Vectored Interrupt Controller). These macros need to be defined in the `chips/chip_name/include/irq.h` file. For reference, see the [RTL8720C example](../../../../../../../nuttx/blob/dev-ai-contest-2026/arch/arm/src/rtl8720c/include/irq.h).

The following are the macros that must be implemented and their functional descriptions:

#### 1. The first interrupt vector number

```C
#define NVIC_IRQ_FIRST  (16)   /* Vector number of the first interrupt */
```

#### 2. Number of interrupts

```C
#define NR_IRQS (64)
```

#### 3. NVIC priority levels

- Minimum priority

    ```C
    #define NVIC_SYSH_PRIORITY_MIN  0xff /* All bits set in minimum priority */
    ```

- Default priority

    ```C
    #define NVIC_SYSH_PRIORITY_DEFAULT  0x40 /* Midpoint is the default */
    ```

- Maximum priority

    ```C
    #define NVIC_SYSH_PRIORITY_MAX   0x00 /* Zero is maximum priority */
    ```

- Priority step

    ```C
    #define NVIC_SYSH_PRIORITY_STEP 0x40 /* Three bits priority used, bits[7-6] as group */
    ```

- Subpriority step

    ```C
    #define NVIC_SYSH_PRIORITY_SUBSTEP  0x20 /* Three bits priority used, bit[5] as sub */
    ```

## II. Interrupt Binding Handling Functions

During the interrupt handling process, handling functions can be bound in the following three ways. Each method is suitable for different scenarios and has its own advantages and disadvantages.

### 1. Using `irq_attach`

```C
int irq_attach(int irq, xcpt_t isr, FAR void *arg)
```

#### 1. Working mechanism

- When an interrupt is triggered, `isr` is called in the interrupt context.
- The advantage of this method is high efficiency because interrupt handling is completed directly in the interrupt context.
- All interrupt responses are masked during the execution of `isr`, which is not suitable for systems with high real-time requirements.
- APIs that cause blocking (such as `sleep`, `wait`, etc.) cannot be called in `isr`.

#### 2. Unbinding

```C
irq_detach(irq)
```

#### 3. Advantages and disadvantages

- Advantage: High processing efficiency.
- Disadvantage: All interrupts are masked during interrupt handling, affecting system real-time performance.

### 2. Using `irq_attach_thread`

```C
int irq_attach_thread(int irq, xcpt_t isr, xcpt_t isrthread, FAR void *arg, int priority, int stack_size)
```

#### 1. Working mechanism

- Users need to provide 1 or 2 handling functions:

    - `isr` is called in the interrupt context, typically used to mask the current interrupt and quickly wake up `isrthread`.
    - `isrthread` is called in the thread context, used to handle remaining interrupt tasks.

- If `isr` is `NULL`, `isrthread` will be called directly.

#### 2. Advantages

- The execution time of `isr` is shortened as much as possible, thereby improving system real-time performance.
- `isrthread` runs as a thread, supports priority scheduling, and can be preempted by other high-priority tasks.

#### 3. Disadvantages

- Consumes more memory (independent thread stack and interrupt thread structure).
- Increases a context switch, reducing efficiency.
- There will be a certain delay in the completion time of interrupt handling (about 5 microseconds).

#### 4. Unbinding

- Use the following method to unbind:

    ```C
    irq_detach_thread(irq)
    ```

### 3. Using `irq_attach_wqueue`

```C
int irq_attach_wqueue(int irq, xcpt_t isr, xcpt_t isrwork, FAR void *arg, int priority)
```

#### 1. Working mechanism

- Users need to provide 1 or 2 handling functions:

    - `isr` is called in the interrupt context.
    - `isrwork` is called in the work queue context.

- The difference from `irq_attach_thread` is that `isrwork` is executed in the work queue instead of an independent thread.

#### 2. Advantages

- Multiple interrupts with the same priority can reuse the same work queue, thereby saving memory.
- High-priority work queues can preempt low-priority queues.
- If there are many interrupts, it saves more memory than `irq_attach_thread`.

#### 3. Disadvantages

- If there is only one interrupt, creating a work queue will bring additional overhead.
- In a multi-core system, the flexibility to control thread attributes and quantity is poor.

#### 4. Unbinding

```C
irq_detach_wqueue(irq)
```

### Summary and comparison

| Binding method    | Advantages                                                    | Disadvantages                                                                                                   | Usage scenarios                                                        |
| :---------------- | :------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| irq_attach        | High efficiency, direct handling in the interrupt context.    | All interrupts are masked during interrupt handling, not suitable for systems with high real-time requirements. | Scenarios with simple processing logic and low real-time requirements. |
| irq_attach_thread | Improves real-time performance, supports priority scheduling. | Consumes more memory, increases context switching, and there is a certain delay in processing completion.       | Scenarios with high real-time requirements.                            |
| irq_attach_wqueue | Saves memory, supports work queue reuse.                      | Low efficiency in single interrupt scenarios, insufficient flexibility in multi-core scenarios.                 | Scenarios with many interrupts and limited memory resources.           |

## III. Implementation Examples of Interrupt Thread/Work Queue

The following is sample code for binding interrupts and implementing interrupt threads or work queues.

### 1. Binding interrupts

Use the `irq_attach_work` function to bind the interrupt handling program:

```C
irq_attach_work(IRQ, isrhandle, isrwork, arg, 253)
```

- `isrhandle`: Interrupt handling function, executed in the interrupt context.
- `isrwork`: Interrupt thread or work queue handling function, executed in the thread context.
- `arg`: Parameters passed to the handling function.
- `253`: Priority setting.

### 2. Interrupt handling function example

In `isrhandle`, return `IRQ_WAKE_THREAD` to wake up the interrupt thread or work queue. If `OK` is returned, the interrupt thread will not be woken up. The sample code is as follows:

```C
static int isrhandle(int irq, void *regs, void *arg)  
{  
    up_disabled_irq(irq); // Mask the interrupt to ensure it will not be triggered again after exit  
    return IRQ_WAKE_THREAD; // Wake up the interrupt thread or work queue  
}
```

### 3. Interrupt thread/work queue handling function example

`isrwork` is used to handle interrupt tasks and clear the interrupt status after completion. The sample code is as follows:

```C
static int isrwork(int irq, void *regs, void *arg)
{
  // Execute interrupt handling logic
  // Clear the pending bit of the interrupt
  up_enabled_irq(irq); // Re-enable the interrupt.
  return OK;
}
```

### 4. Special case: One-shot interrupts

For some one-shot interrupts, `isrhandle` can be set to `NULL`, and `isrwork` is directly used to handle interrupt tasks.

## IV. Optimization of Interrupt Structures

When using interrupts, the system usually defines a global interrupt structure array:

```C
struct irq_info_s g_irqvector[NR_IRQS];
```

Where `NR_IRQS` represents the maximum interrupt number supported by the system, usually more than 200. However, the actual number of interrupts used is usually only a dozen, and these interrupt numbers are discretely distributed. This design will lead to the following problems:

- Memory waste: Even if only a few interrupts are used, memory needs to be allocated for all possible interrupt numbers to store `NR_IRQS` structures.
- Inefficient resource utilization: Structures corresponding to most interrupt numbers are unused, causing resource waste.

### 1. Optimization strategy and implementation principle

To solve the above problems, the storage of interrupt structures can be optimized through the following dynamic mapping methods.

#### Mapping relation array

Define a mapping relation array to dynamically establish the mapping between interrupt numbers and interrupt structures:

```C
irq_mapped_t g_irqmap[NR_IRQS]
```

- This array only occupies an additional `NR_IRQS` bytes of memory.
- The mapping relation is dynamically established when interrupts are used.

#### Streamline the interrupt structure array

Define `g_irqvector` as:

```C
struct irq_info_s g_irqvector[CONFIG_ARCH_NUSER_INTERRUPTS];
```

- `CONFIG_ARCH_NUSER_INTERRUPTS` represents the maximum number of interrupts that may be used in the system plus 1.
- By limiting the array size, memory is only allocated for interrupts that may actually be used.

#### Interrupt usage statistics

Use `g_irqmap_count` to count the number of interrupts currently in use, which is convenient for monitoring and debugging.

### 2. Configuration examples

Enable optimization through the following macro configurations:

```Makefile
CONFIG_ARCH_MINIMAL_VECTORTABLE_DYNAMINC=y
CONFIG_ARCH_MINIMAL_VECTORTABLE=y
CONFIG_ARCH_NUSER_INTERRUPTS=24
```

- `CONFIG_ARCH_MINIMAL_VECTORTABLE_DYNAMIC`: Enable dynamic mapping function.
- `CONFIG_ARCH_MINIMAL_VECTORTABLE`: Enable the streamlined interrupt vector table.
- `CONFIG_ARCH_NUSER_INTERRUPTS`: Set the maximum number of interrupts that may be used.

### 3. Optimization effects

- Memory saving: Only allocate storage space for actually used interrupts, avoiding memory waste for unused interrupt numbers.
- Improved flexibility: Support discretely distributed interrupt numbers through dynamic mapping relations.
- Scalability: Flexibly adjust the interrupt number limit through configuration macros.

## V. Related repositories

- [nuttx](../../../../../../../nuttx)