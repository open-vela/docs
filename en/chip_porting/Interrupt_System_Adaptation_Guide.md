# Interrupt System Adaptation Guide  

\[ English | [简体中文](../../zh-cn/chip_porting/Interrupt_System_Adaptation_Guide.md) \]

## I. Implementing Chip Interrupt Debugging  

When debugging the chip interrupt subsystem (`bringup`), vendors need to implement a series of architecture-related functions (`arch` functions) to accomplish the following tasks:  

- Initialize interrupts  
- Enable and disable interrupts  
- Set interrupt priority  

The following information provides specific requirements and implementation examples.  

### 1. Required Interrupt-Related Functions  

The following are the interrupt-related functions that vendors need to implement, along with their descriptions.  

1. **Initialize the interrupt system**, including disabling all interrupts, configuring the vector table position, setting default priorities, and enabling interrupts.  

    ```C  
    void up_irqinitialize(void)  
    {  
      // Disable all interrupts  
      // Set the NVIC vector location  
      // Set all interrupts (and exceptions) to the default priority  
      // Attach the SVCall and Hard Fault exception handlers  
      // Enable interrupts  
    }  
    ```  

2. **Enable a specific interrupt**:  

    ```C  
    void up_enable_irq(int irq)  
    {  
      // Enable interrupt with irq  
    }  
    ```

3. **Disable a specific interrupt**:  

    ```C  
    void up_disable_irq(int irq)  
    {  
      // Disable interrupt with irq  
    }  
    ```  

4. **Set interrupt priority**: If the `CONFIG_ARCH_IRQPRIO` configuration is enabled, the following function must be implemented:  

    ```C  
    #ifdef CONFIG_ARCH_IRQPRIO  
    int up_prioritize_irq(int irq, int priority)  
    {  
      // Set IRQ priority  
    }  
    #endif  
    ```

5. **Manage interrupt states**:  

    - Check if `flags` indicate that interrupts are currently disabled:  

        ```C  
        #define up_irq_is_disabled(flags)  
        ```  

    - Save the current interrupt state and disable interrupts:  

        ```C  
        irqstate_t up_irq_save(void)  
        {  
          // Save current interrupt state and disable interrupts  
        }  
        ```  

    - Restore the specified interrupt state:  

        ```C  
        void up_irq_restore(irqstate_t flags)  
        {  
          // Restore the interrupt state indicated by flags  
        }  
        ```  

    - Enable all interrupts:  

        ```C  
        irqstate_t up_irq_enable(void)  
        {  
          // Enable all interrupts  
        }  
        ```  

    - Get the current interrupt state:  

        ```C  
        irqstate_t irqstate(void)  
        {  
          // Get the current interrupt state  
        }  
        ```  

6. **Handle inter-core interrupts**:  

    ```C  
    // Trigger an inter-core interrupt  
    void up_trigger_irq(int irq, cpu_set_t cpuset)  
    ```  

7. **Set the secure attributes of interrupts**:  

    - Set the secure attributes for a specific interrupt:  

        ```C  
        void up_secure_irq(int irq, bool secure)  
        ```  

    - Modify the secure attributes for all interrupts:  

        ```C  
        void up_secure_irq_all(bool secure)  
        ```  

### 2. Required Interrupt-Related Macros  

Alongside the above function implementations, vendors need to define a series of interrupt-related macros, which describe the configuration of the NVIC (Nested Vectored Interrupt Controller). These macros should be defined in the `chips/chip_name/include/irq.h` file. Refer to the [RTL8720C example](../../../../../nuttx/blob/dev-ai-contest-2026/arch/arm/src/rtl8720c/include/irq.h) for guidance.  

The required macros and their descriptions are as follows:  

1. **First interrupt vector number**:  

    ```C  
    #define NVIC_IRQ_FIRST  (16)   /* Vector number of the first interrupt */  
    ```  

2. **Number of interrupts**:  

    ```C  
    #define NR_IRQS (64)  
    ```

3. **NVIC priority levels**:  

    - **Minimum priority**:  

        ```C  
        #define NVIC_SYSH_PRIORITY_MIN  0xff /* All bits set in minimum priority */  
        ```  

    - **Default priority**:  

        ```C  
        #define NVIC_SYSH_PRIORITY_DEFAULT  0x40 /* Midpoint is the default */  
        ```  

    - **Maximum priority**:  

        ```C  
        #define NVIC_SYSH_PRIORITY_MAX   0x00 /* Zero is maximum priority */  
        ```  

    - **Priority step size**:  

        ```C  
        #define NVIC_SYSH_PRIORITY_STEP 0x40 /* Three bits priority used, bits[7-6] as group */  
        ```  

    - **Sub-priority step size**:  

        ```C  
        #define NVIC_SYSH_PRIORITY_SUBSTEP  0x20 /* Three bits priority used, bit[5] as sub */  
        ```  

---

## II. Binding Interrupt Handlers  

During interrupt processing, handlers can be bound using the following three methods. Each method is suitable for different scenarios and has its own advantages and disadvantages.  

### 1. Using `irq_attach`  

```C
int irq_attach(int irq, xcpt_t isr, FAR void *arg)
```

1. **Mechanism**:  

    - When the interrupt is triggered, `isr` is called in the interrupt context.  
    - The advantage of this method is high efficiency since the interrupt handling is completed directly in the interrupt context.  
    - During the execution of `isr`, all interrupts are masked, making it less suitable for systems with high real-time requirements.  
    - Blocking APIs (e.g., `sleep`, `wait`) cannot be called within `isr`.  

2. **Unbinding**:  

    ```C  
    irq_detach(irq)  
    ```  

3. **Advantages and Disadvantages**:  

    - **Advantages**: High processing efficiency.  
    - **Disadvantages**: Interrupts are masked during processing, which affects the real-time performance of the system.  

### 2. Using `irq_attach_thread`  

```C
int irq_attach_thread(int irq, xcpt_t isr, xcpt_t isrthread, FAR void *arg, int priority, int stack_size)
```

1. **Mechanism**:  

    - Users need to provide one or two handler functions:  
        - `isr` is called in the interrupt context, typically to mask the current interrupt and quickly wake up `isrthread`.  
        - `isrthread` is called in the thread context to handle the remaining interrupt tasks.  
    - If `isr` is `NULL`, `isrthread` is invoked directly.  

2. **Advantages**:  

    - The execution time of `isr` is minimized, improving the system's real-time performance.  
    - `isrthread` runs as a thread, supports priority scheduling, and can be preempted by other higher-priority tasks.  

3. **Disadvantages**:  

    - Consumes more memory (independent thread stacks and interrupt thread structures).  
    - Introduces an additional context switch, reducing execution efficiency.  
    - There may be a delay (approximately 5 microseconds) in completing interrupt handling.  

4. **Unbinding**:  

    ```C  
    irq_detach_thread(irq)  
    ```  

### 3. Using `irq_attach_wqueue`  

```C
int irq_attach_wqueue(int irq, xcpt_t isr, xcpt_t isrwork, FAR void *arg, int priority)
```

1. **Mechanism**:  

    - Users need to provide one or two handler functions:  
        - `isr` is called in the interrupt context.  
        - `isrwork` is called in the work queue context.  
    - The key difference from `irq_attach_thread` is that `isrwork` is executed in the work queue instead of an independent thread.  

2. **Advantages**:  

    - Interrupts with the same priority can share the same work queue, saving memory.  
    - High-priority work queues can preempt lower-priority queues.  
    - This method is more memory-efficient than `irq_attach_thread` when dealing with many interrupts.  

3. **Disadvantages**:  

    - If there is only one interrupt, creating a work queue introduces additional overhead.  
    - In multi-core systems, there is limited flexibility in controlling thread attributes and the number of threads.  

4. **Unbinding**:  

    ```C  
    irq_detach_wqueue(irq)  
    ```  

### Summary Comparison  

| Binding Method    | Advantages                                                    | Disadvantages                                                                                   | Use Cases                                                        |
| :---------------- | :------------------------------------------------------------ | :---------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- |
| irq_attach        | High efficiency, direct handling in the interrupt context.    | Interrupts are masked during handling, unsuitable for systems with high real-time requirements. | Scenarios with simple processing and low real-time requirements. |
| irq_attach_thread | Improves real-time performance, supports priority scheduling. | Consumes more memory, introduces context switches, and has some delay in processing completion. | Scenarios with high real-time requirements.                      |
| irq_attach_wqueue | Saves memory, supports work queue reuse.                      | Low efficiency for single-interrupt scenarios, limited flexibility in multi-core systems.       | Scenarios with many interrupts and limited memory resources.     |

## III. Implementation Example of Interrupt Thread/Work Queue  

Below is an example of binding interrupts and implementing interrupt threads or work queues.

### 1. Binding Interrupts  

Use the `irq_attach_work` function to bind an interrupt handler:  

```C
irq_attach_work(IRQ, isrhandle, isrwork, arg, 253)
```

- `isrhandle`: The interrupt handler function, executed in the interrupt context.  
- `isrwork`: The interrupt thread or work queue handler function, executed in the thread context.  
- `arg`: The parameter passed to the handler functions.  
- `253`: The priority setting.  

### 2. Example of Interrupt Handler  

In `isrhandle`, return `IRQ_WAKE_THREAD` to wake up the interrupt thread or work queue. If `OK` is returned, the interrupt thread will not be woken up. Example code is as follows:  

```C  
static int isrhandle(int irq, void *regs, void *arg)  
{  
    up_disabled_irq(irq); // Mask the interrupt to ensure it does not trigger again after exit  
    return IRQ_WAKE_THREAD; // Wake up the interrupt thread or work queue  
}
```

### 3. Example of Interrupt Thread/Work Queue Handler  

`isrwork` is used to handle interrupt tasks and clear the interrupt state after completion. Example code is as follows:  

```C  
static int isrwork(int irq, void *regs, void *arg)  
{  
  // Execute the interrupt handling logic  
  // Clear the pending bit of the interrupt  
  up_enabled_irq(irq); // Re-enable the interrupt  
  return OK;  
}
```

### 4. Special Case: One-shot Interrupt  

For certain one-shot interrupts, `isrhandle` can be set to `NULL`, and `isrwork` can be used directly to handle interrupt tasks.  

## IV. Interrupt Structure Optimization  

When using interrupts, the system typically defines a global interrupt structure array: 

```C
struct irq_info_s g_irqvector[NR_IRQS];
```

Here, `NR_IRQS` represents the maximum number of interrupts supported by the system, which is typically greater than 200. However, in practice, only a few interrupts are used, and these interrupt numbers are sparsely distributed. This design results in the following issues:  

- **Memory Waste**: Even if only a small number of interrupts are used, memory must still be allocated for all possible interrupt numbers, requiring storage for `NR_IRQS` structures.  
- **Inefficient Resource Utilization**: The majority of interrupt numbers’ corresponding structures remain unused, leading to resource waste.  

### 1. Optimization Strategy and Implementation Principle  

To address the issues above, the storage of interrupt structures can be optimized using the following dynamic mapping method.  

#### Mapping Relationship Array  

Define a mapping relationship array to dynamically establish the mapping between interrupt numbers and interrupt structures:  

```C
irq_mapped_t g_irqmap[NR_IRQS]
```

- This array only requires `NR_IRQS` bytes of additional memory.  
- The mapping relationship is dynamically established during interrupt usage.  

#### Simplified Interrupt Structure Array  

Define `g_irqvector` as:  

```C
struct irq_info_s g_irqvector[CONFIG_ARCH_NUSER_INTERRUPTS];
```

- `CONFIG_ARCH_NUSER_INTERRUPTS` represents the maximum number of interrupts that may be used in the system plus 1.  
- By limiting the size of the array, memory is allocated only for interrupts that are actually likely to be used.  

#### Interrupt Usage Statistics  

Use `g_irqmap_count` to keep track of the number of interrupts currently in use, facilitating monitoring and debugging.  

### 2. Configuration Example  

Enable the optimization with the following macros:

```Makefile
CONFIG_ARCH_MINIMAL_VECTORTABLE_DYNAMINC=y
CONFIG_ARCH_MINIMAL_VECTORTABLE=y
CONFIG_ARCH_NUSER_INTERRUPTS=24
```

- `CONFIG_ARCH_MINIMAL_VECTORTABLE_DYNAMIC`: Enables the dynamic mapping functionality.  
- `CONFIG_ARCH_MINIMAL_VECTORTABLE`: Enables the minimal interrupt vector table.  
- `CONFIG_ARCH_NUSER_INTERRUPTS`: Sets the maximum number of interrupts that may be used.  

### 3. Optimization Effects  

- **Memory Saving**: Allocates memory only for interrupts in use, avoiding waste for unused interrupt numbers.  
- **Flexibility Improvement**: Supports sparsely distributed interrupt numbers through dynamic mapping.  
- **Scalability**: Flexibly adjusts the interrupt limit via configuration macros.  

## V. Related Repository

- [nuttx](../../../../../nuttx)
