# 在 IDLE 线程中实现电源管理

\[ [English](../../../en/device_dev_guide/power_mgt/pm_idle_impl.md) | 简体中文 \]

## 一、概述

本文档旨在介绍在 openvela 系统的 IDLE 线程中执行电源管理 (Power Management, PM) 操作的推荐方法。

IDLE 线程是系统没有其他活动任务时执行的线程。因此，它是进入低功耗状态（如 Standby 或 Sleep）以节省能源的理想位置。为了确保电源状态切换的原子性和稳定性，该过程必须在禁止中断和调度器锁定的临界区内执行。

## 二、核心原则：确保原子性操作

在更改系统电源状态时，必须防止任何并发活动（如中断服务程序或任务切换）干扰该过程。否则，可能导致系统状态不一致或崩溃。

为实现这一目标，我们采用以下两种关键机制：

- **关闭中断**：使用 `up_irq_save` 函数，可以防止外部中断打断正在进行的电源状态切换逻辑。
- **锁定调度器**：使用 `sched_lock` 函数，可以禁止操作系统进行任何线程上下文切换，确保 IDLE 线程的执行不会被其他线程抢占。

## 三、推荐实现：`up_idle` 函数详解

`up_idle` 函数是特定于架构（`up_` 前缀）的函数，由 openvela 的通用 IDLE 循环调用。您应在此函数中实现具体的低功耗逻辑。

### 1、示例代码

```C
void up_idle(void)
{
  enum pm_state_e newstate;
  irqstate_t flags;
  int ret;
  
  /* If sched lock before irq save, and irq handler do post, scheduler will
   * be delayed after WFI until next sched unlock. which is not acceptable.
   */

  flags = up_irq_save();
  sched_lock();
  
  /*
  * Check and change the power state.
  * The system will enter a low-power state within pm_changestate.
  */
  newstate = pm_checkstate(PM_IDLE_DOMAIN);
  ret = pm_changestate(PM_IDLE_DOMAIN, newstate);
  if (ret < 0)
    { 
      /* If state change fails, revert to NORMAL state. */
      newstate = PM_NORMAL;
    }
  
  /*
  * Logic to handle different power states after waking up.
  * The actual low-power instruction (e.g., WFI) is executed
  * inside pm_changestate.
  */
  switch (newstate)
    { 
      case PM_NORMAL:
          // normal pm
          break;
      
      case PM_IDLE:
          // normal pm
          break;
      
      case PM_STANDBY:
          /* deep but no power down */
          break;
      
      case PM_SLEEP:
          /* deep with power down */
          break;
      
      default:
          break;
    }
  
  /*
  * Restore system state before enabling scheduler and interrupts.
  * This is an opportunity to restore clocks or other settings.
  */
  pm_changestate(PM_IDLE_DOMAIN, PM_RESTORE);
    
  /* If there is pending irq, enable irq make handlers finish all execution
   * will be better decrease scheduler context switch times.
   */

  up_irq_restore(flags);
  
  sched_unlock();
}
```

### 2、代码逻辑解析

#### 步骤 1：进入临界区

```C
flags = up_irq_save();
sched_lock();
```

此处的执行顺序至关重要：**必须先关闭中断，再锁定调度器**。

- **原因**：如果您先锁定调度器，系统仍然可以响应中断。如果一个中断服务程序（ISR）唤醒了一个高优先级任务（例如通过 `sem_post`），该任务会被置于就绪状态。然而，由于调度器已锁定，上下文切换会被推迟。这可能导致非预期的行为，例如在执行 `WFI`（Wait For Interrupt）指令后，系统唤醒的延迟增加。

#### 步骤 2：执行电源状态切换

```C
newstate = pm_checkstate(PM_IDLE_DOMAIN);
ret = pm_changestate(PM_IDLE_DOMAIN, newstate);
```

- `pm_checkstate`: 此函数根据当前系统活动决定下一个合适的目标电源状态。
- `pm_changestate`: 此函数执行实际的状态切换操作，例如关闭时钟、断电，并最终执行 `WFI` 或 `WFE` 指令使 CPU 进入低功耗模式。系统将在此函数中暂停，直到一个中断将其唤醒。

#### 步骤 3：唤醒后的处理

```C
switch (newstate) { ... }
pm_changestate(PM_IDLE_DOMAIN, PM_RESTORE);
```

当系统被中断唤醒后，代码从 `pm_changestate` 返回并继续执行。

- `switch` 语句：您可以根据系统是从哪种状态（`PM_STANDBY`, `PM_SLEEP`）唤醒的，来执行特定的恢复操作。
- `pm_changestate(..., PM_RESTORE)`：在退出临界区之前，调用此函数来执行统一的恢复逻辑，例如重新启用在睡眠期间被禁用的系统时钟。

#### 步骤 4：退出临界区

```C
up_irq_restore(flags);
sched_unlock();
```

- `up_irq_restore(flags)`：恢复之前保存的中断状态。如果唤醒是由中断触发的，这将允许中断服务程序（ISR）完全执行。
- `sched_unlock()`：解锁调度器。如果在临界区执行期间有更高优先级的任务变为就绪态，系统将在此刻进行上下文切换。

## 四、常见问题 (FAQ)

### 1、如果在 `pm_changestate` 内部（或在临界区内的其他任何地方）通过中断唤醒了一个等待信号量的任务（例如调用 `sem_post`），会发生什么？

IDLE 线程会继续执行，直到 `sched_unlock()` 被调用后，才会发生上下文切换。

**详细解释：**

1. **任务被唤醒**：一个中断发生，其中断服务程序调用 `sem_post`。这会将一个正在等待该信号量的高优先级任务从等待状态移动到就绪（Ready-to-run）状态。
2. **调度被推迟**：尽管有一个更高优先级的任务就绪，但由于调度器已被 `sched_lock()` 锁定，上下文切换被**推迟（Deferred）**。
3. **IDLE 线程继续执行**：`up_idle` 函数中的代码将继续执行，完成 `switch` 语句、调用 `pm_changestate` 进行恢复，并恢复中断状态。
4. **执行上下文切换**：当执行到 `sched_unlock()` 时，调度器解除锁定。此时，它会检查是否有更高优先级的任务处于就绪状态。如果存在，NuttX 会立即执行上下文切换，让高优先级任务运行。

这个机制确保了电源管理操作的完整性，同时保证了系统在退出低功耗状态后能够及时响应挂起的任务。
