# up_cpu_wfi Implementation Guide

\[ English | [简体中文](../../../zh-cn/device_dev_guide/power_mgt/up_cpu_wfi_guide.md) \]

The `up_cpu_wfi()` function is central to placing the platform into a low-power state. It is called by `up_pm_idle_handler` in the example code from [Standardizing Idle Thread Power Management with pm_idle](./pm_idle_guide.md). The implementation of this function is tightly coupled with the CPU architecture. This section provides reference implementations and an analysis of key technical points for mainstream architectures (Cortex-M and RISC-V).

## I. Cortex-M Architecture

On the Cortex-M architecture, especially in systems with zero-latency interrupts enabled (`CONFIG_ARCH_ZOOLATENCY`), the implementation of `up_cpu_wfi()` requires special attention to ensure that all interrupts, including high-priority zero-latency interrupts, are correctly masked before entering the WFI (Wait For Interrupt) state.

The standard `up_irq_save()` function typically masks all maskable interrupts by setting the `PRIMASK` register, but it cannot mask zero-latency interrupts. Therefore, it is necessary to directly manipulate the `BASEPRI` register to temporarily raise the interrupt mask level.

**Reference Implementation**: [Source Link](https://github.com/FishsemiCode/nuttx/blob/song-u1/arch/arm/src/song/song_idle.c#L192-L225)

```C
void up_cpu_wfi(void)
{
/* The WFI implementation is architecture-specific */
#ifdef CONFIG_ARCH_CORTEXM4

  /* 
   * This implementation is required for systems that use BASEPRI for interrupt
   * management, especially when zero-latency interrupts are enabled.
   */
  int basepri = 0;

  /* Change BASEPRI to the minimal priority
   * value for waking up from PRIMASK == 1
   */

  __asm__ __volatile__
    (
#ifdef CONFIG_ARMV7M_USEBASEPRI
      "\tcpsid i\n"               /* Disable interrupts globally */
#endif
      "\tmrs %0, basepri\n"       /* Save current BASEPRI value */
      "\tmsr basepri, %1\n"       /* Set BASEPRI to block all maskable IRQs */
      "\tdsb\n"                   /* Ensure all memory accesses complete */
      "\twfi\n"                   /* Enter wait-for-interrupt state */
      "\tmsr basepri, %0\n"       /* Restore original BASEPRI value */
#ifdef CONFIG_ARMV7M_USEBASEPRI
      "\tcpsie i\n"               /* Re-enable interrupts globally */
#endif
      : "+r" (basepri)            /* Output/Input: original basepri value */
      : "r" (0xff)
      : "memory"
    );
#else
  __asm__ __volatile__
    (
      "\tdsb\n"
      "\twfi\n"
    );
#endif
}
```

### Implementation Analysis

1. **`cpsid i`**: Globally disables interrupts. This is to prevent a race condition where an interrupt (even a low-priority one) is serviced while `BASEPRI` is being modified.
2. **`mrs %0, basepri`**: Saves the current value of the `BASEPRI` register into the `basepri` variable.
3. **`msr basepri, %1`**: Sets `BASEPRI` to `NVIC_SYSH_PRIORITY_MIN`. This value is typically the highest numerical priority (i.e., the lowest actual priority) supported by the system, ensuring that all interrupts with a lower or equal priority are masked. This effectively masks all maskable interrupts, including zero-latency ones.
4. **`dsb`**: Data Synchronization Barrier. Ensures that all memory access operations preceding the `WFI` instruction have completed.
5. **`wfi`**: Executes the `Wait For Interrupt` instruction, causing the CPU to enter a low-power state until an interrupt event wakes it.
6. **`msr basepri, %0`**: Immediately after the CPU wakes from `WFI`, restores the previously saved `BASEPRI` value, returning the interrupt mask to its normal state.
7. **`cpsie i`**: Globally re-enables interrupts, corresponding to the `cpsid i` in the first step.

## II. RISC-V Architecture

In contrast, the implementation of `up_cpu_wfi` for the RISC-V architecture is typically much simpler. The standard `WFI` instruction is sufficient to place the core (hart) into a low-power state to wait for an interrupt.

**Reference Implementation:** [Source Link](https://github.com/open-vela/nuttx/blob/31734b0c9ca1d021b03528d17b6d869e2392ff74/arch/risc-v/src/common/riscv_idle.c#L50-L75)

```C
void up_cpu_wfi(void)
{
  __asm__ volatile("wfi");
}
```

### Implementation Analysis

In RISC-V, by the time the `up_idle` function is called, the operating system has already disabled global interrupts via `up_irq_save()` (typically by manipulating the `MIE` bit in the `mstatus` register). Therefore, within `up_cpu_wfi()`, you only need to execute the `wfi` instruction. The processor will pause execution until an external interrupt, local interrupt, or debug request becomes pending.
