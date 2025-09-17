# Implementing Power Management in the IDLE Thread

\[ English | [简体中文](../../../zh-cn/device_dev_guide/power_mgt/pm_idle_impl.md) \]

## I. Overview

This document describes the recommended method for performing Power Management (PM) operations within the IDLE thread of the openvela system.

The IDLE thread is the thread that executes when the system has no other active tasks. Therefore, it is the ideal place to enter low-power states (such as Standby or Sleep) to conserve energy. To ensure the atomicity and stability of power state transitions, this process must be executed within a critical section where interrupts are disabled and the scheduler is locked.

## II. Core Principle: Ensuring Atomic Operations

When changing the system's power state, it is essential to prevent any concurrent activities (like interrupt service routines or task switches) from interfering with the process. Failure to do so could lead to system state inconsistencies or crashes.

To achieve this, we employ two key mechanisms:

- **Disabling Interrupts**: Using the `up_irq_save` function prevents external interrupts from disrupting the ongoing power state transition logic.
- **Locking the Scheduler**: Using the `sched_lock` function prohibits the operating system from performing any thread context switches, ensuring that the IDLE thread's execution is not preempted by other threads.

## III. Recommended Implementation: `up_idle` Function Details

The `up_idle` function is an architecture-specific function (indicated by the `up_` prefix) called by openvela's generic IDLE loop. You should implement your specific low-power logic within this function.

### 1. Example Code

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

### 2. Code Logic Analysis

#### Step 1: Entering the Critical Section

```C
flags = up_irq_save();
sched_lock();
```

The order of execution here is critical: **interrupts must be disabled before the scheduler is locked**.

- **Reason**: If you lock the scheduler first, the system can still respond to interrupts. If an interrupt service routine (ISR) wakes up a high-priority task (e.g., via `sem_post`), that task is placed in the ready state. However, because the scheduler is locked, the context switch is postponed. This can lead to unintended behavior, such as increased wake-up latency after executing a `WFI` (Wait For Interrupt) instruction.

#### Step 2: Executing the Power State Transition

```C
newstate = pm_checkstate(PM_IDLE_DOMAIN);
ret = pm_changestate(PM_IDLE_DOMAIN, newstate);
```

- `pm_checkstate`: This function determines the next appropriate target power state based on current system activity.
- `pm_changestate`: This function performs the actual state transition, such as turning off clocks, powering down peripherals, and finally executing a `WFI` or `WFE` instruction to place the CPU in a low-power mode. The system will pause within this function until it is awakened by an interrupt.

#### Step 3: Post-Wakeup Processing

```C
switch (newstate) { ... }
pm_changestate(PM_IDLE_DOMAIN, PM_RESTORE);
```

When the system is awakened by an interrupt, code execution resumes from the return of `pm_changestate`.

- `switch` statement: You can perform specific recovery actions based on which state (`PM_STANDBY`, `PM_SLEEP`) the system woke up from.
- `pm_changestate(..., PM_RESTORE)`: Before exiting the critical section, this function is called to execute unified restoration logic, such as re-enabling system clocks that were disabled during sleep.

#### Step 4: Exiting the Critical Section

```C
up_irq_restore(flags);
sched_unlock();
```

- `up_irq_restore(flags)`: Restores the previously saved interrupt state. If the wakeup was triggered by an interrupt, this allows the interrupt service routine (ISR) to complete its execution.
- `sched_unlock()`: Unlocks the scheduler. If a higher-priority task became ready to run during the critical section, the system will perform a context switch at this moment.

## IV. FAQ

### 1. What happens if a task waiting on a semaphore is awakened by an interrupt (e.g., via `sem_post`) inside `pm_changestate` (or anywhere else in the critical section)?

The IDLE thread will continue to execute until `sched_unlock()` is called, at which point the context switch will occur.

**Detailed Explanation:**

1. **Task is Awakened**: An interrupt occurs, and its service routine calls `sem_post`. This moves a high-priority task that was waiting for the semaphore from the waiting state to the ready-to-run state.
2. **Scheduling is Deferred**: Although a higher-priority task is now ready, the context switch is **deferred** because the scheduler has been locked by `sched_lock()`.
3. **IDLE Thread Continues Execution**: The code in the `up_idle` function will continue to execute, completing the `switch` statement, calling `pm_changestate` for restoration, and restoring the interrupt state.
4. **Context Switch Occurs**: When `sched_unlock()` is executed, the scheduler is unlocked. It then checks if any higher-priority tasks are in the ready state. If so, NuttX immediately performs a context switch to run the high-priority task.

This mechanism ensures the integrity of the power management operation while guaranteeing that the system can promptly respond to pending tasks after exiting a low-power state.
