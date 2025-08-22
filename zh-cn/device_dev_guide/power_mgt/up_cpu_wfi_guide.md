# up_cpu_wfi 实现指南

\[ [English](../../../en/device_dev_guide/power_mgt/up_cpu_wfi_guide.md) | 简体中文 \]

函数 `up_cpu_wfi()` 是平台进入低功耗状态的核心，它由[使用 pm_idle 标准化 Idle 线程的功耗管理](./pm_idle_guide.md)示例代码中的 `up_pm_idle_handler` 调用。该函数的实现与 CPU 架构紧密相关。本章节提供主流架构 (Cortex-M 和 RISC-V) 的参考实现和关键技术点的解析。

## 一、Cortex-M 架构

在 Cortex-M 架构中，尤其是在启用了零延迟中断 (`CONFIG_ARCH_ZOOLATENCY`) 的系统中，`up_cpu_wfi()` 的实现需要特别注意，以确保在进入 `WFI` (Wait For Interrupt) 状态前，所有中断（包括高优先级的零延迟中断）都已被正确屏蔽。

标准的 `up_irq_save()` 函数通常通过设置 `PRIMASK` 寄存器来屏蔽所有可屏蔽中断，但它无法屏蔽零延迟中断。因此，必须直接操作 `BASEPRI` 寄存器来临时提升中断屏蔽等级。

**参考实现**：[源码链接](https://github.com/FishsemiCode/nuttx/blob/song-u1/arch/arm/src/song/song_idle.c#L192-L225)

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

### 实现解析

1. **`cpsid i`**：全局禁止中断。这是为了防止在修改 `BASEPRI` 期间，有中断（即使是低优先级的）被响应，从而造成竞态条件。
2. **`mrs %0, basepri`**：将当前的 `BASEPRI` 寄存器值保存到变量 `basepri` 中。
3. **`msr basepri, %1`**：设置 `BASEPRI` 为 `NVIC_SYSH_PRIORITY_MIN`。该值通常是系统支持的最高优先级数值（即最低优先级），确保所有低于该优先级的中断都被屏蔽。这有效地屏蔽了包括零延迟中断在内的所有可屏蔽中断。
4. **`dsb`**：数据同步屏障 (Data Synchronization Barrier)。确保所有在 `WFI` 指令之前的内存访问操作都已完成。
5. **`wfi`**：执行 `Wait For Interrupt` 指令，使 CPU 进入低功耗状态，直到一个中断事件唤醒它。
6. **`msr basepri, %0`**：CPU 从 `WFI` 唤醒后，立即恢复之前保存的 `BASEPRI` 值，使中断屏蔽恢复到正常状态。
7. **`cpsie i`**：全局使能中断，与第一步的 `cpsid i` 对应。

## 二、RISC-V 架构

相比之下，RISC-V 架构的 `up_cpu_wfi` 实现通常更为简洁。标准的 `WFI` 指令足以使核心 (hart) 进入低功耗状态，等待中断唤醒。

**参考实现：**[源码链接](https://github.com/open-vela/nuttx/blob/31734b0c9ca1d021b03528d17b6d869e2392ff74/arch/risc-v/src/common/riscv_idle.c#L50-L75)

```C
void up_cpu_wfi(void)
{
  __asm__ volatile("wfi");
}
```

### 实现解析

在 RISC-V 中，当 `up_idle` 函数被调用时，操作系统已经通过 `up_irq_save()` 禁用了全局中断（通常通过操作 `mstatus` 寄存器的 `MIE` 位）。因此，在 `up_cpu_wfi()` 中，您只需执行 `wfi` 指令。处理器将暂停执行，直到一个外部中断、本地中断或调试请求变为挂起状态。
