# openvela Semaphores

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/kernel/resource_sync/semaphore_mechanism.md) \]

## I. Overview

In the openvela real-time operating system (RTOS), the Semaphore is a core mechanism for implementing inter-task synchronization and mutual exclusion. It complies with the POSIX standard, providing developers with a powerful tool for managing shared resources and coordinating task execution order.

Compared to disabling the scheduler with `sched_lock()`, semaphores are the preferred solution for protecting shared resources. `sched_lock()` indiscriminately blocks all other tasks, including high-priority tasks that do not access the protected resource, which can degrade system responsiveness. In contrast, semaphores offer more granular control, blocking only the specific tasks that attempt to access the same resource.

This document provides a detailed introduction to the core concepts of openvela semaphores, their usage patterns, API reference, and strategies for resolving priority inversion.

## II. Core Concepts

### 1. Semaphore

A semaphore is essentially a protected counter used to control access to a finite number of resources.

- **Mutual Exclusion (Mutex)**: When a semaphore is initialized with a value of 1, it can be used as a mutex to ensure that only one task can access its protected critical section at any given time.
- **Synchronization**: A task can wait on a semaphore until another task or an Interrupt Service Routine (ISR) posts to it, thus enabling coordination of execution order between tasks.

### 2. Priority Inversion

Priority inversion is a common problem in preemptive multitasking systems. It occurs when a high-priority task is blocked waiting for a resource held by a low-priority task. If a medium-priority task then becomes ready, it will preempt the low-priority task, preventing it from releasing the resource and thereby indirectly blocking the high-priority task.

#### Typical Scenario

1. **low-priority task C** acquires a semaphore and enters its critical section.
2. **high-priority task A** starts and attempts to acquire the same semaphore but is blocked because the resource is held by task C.
3. **medium-priority task B** starts. Since its priority is higher than task C's, it preempts the CPU.
4. **Result**: Task B (and other medium-priority tasks) continues to run, preventing task C from executing and releasing the semaphore. This causes the high-priority task A to be indefinitely blocked by the medium-priority task B, as if task A had a lower priority than task B.

To solve this problem, openvela implements priority protection and priority inheritance mechanisms.

## III. Semaphore Usage Patterns

In openvela, semaphores are primarily used in two modes: **Locking Semaphore** and **Signaling Semaphore**. Correctly distinguishing and using these modes is critical for system stability.

### 1. Locking Semaphore Mode

This mode is used to protect shared resources and ensure mutually exclusive access to critical sections.

- **Purpose**: To ensure that only one task at a time can access a shared data structure or hardware resource.
- **Characteristics**:

    - The operations to acquire (`wait`) and release (`post`) the semaphore are performed by the **same task**.
    - **It is strongly recommended to enable** priority inheritance or priority protection to avoid priority inversion.

### 2. Signaling Semaphore Mode

This mode is used for inter-task synchronization or communication.

- **Purpose**: For one task (or an ISR) to notify another task that an event has occurred. For example, task A waits on a semaphore until task B completes data preparation and posts to the semaphore to wake up task A.
- **Characteristics**:

    - The operations to acquire (`wait`) and release (`post`) the semaphore are performed by **different tasks** (or a task and an ISR).
    - **Priority inheritance must be disabled**. Otherwise, the task posting the semaphore (task B) might erroneously inherit the priority of the waiting task (task A), leading to unexpected scheduling behavior.

**Best Practice**: When initializing a semaphore, set the appropriate priority protocol using `sem_setprotocol()` based on its intended use.

## IV. Solving Priority Inversion

openvela provides two strategies to solve the problem of priority inversion: Priority Protection and Priority Inheritance.

### 1. Priority Protection

Priority Protection is based on the principles of the Priority Ceiling Protocol.

#### Overview

When a task acquires a semaphore, the system immediately raises its priority to a pre-configured "ceiling" priority for that semaphore. This ceiling is typically set to the highest priority among all tasks that may access the semaphore. After the task releases the semaphore, its priority is restored to its original value.

This mechanism is simple to implement and effectively prevents a lock-holding task from being preempted by other tasks.

#### Configuration

This feature can be enabled via the Kconfig option `CONFIG_PRIORITY_PROTECT`.

#### Implementation

Priority protection is implemented through two core functions: `nxsem_protect_wait` and `nxsem_protect_post`.

### 2. Priority Inheritance

Priority Inheritance is a dynamic priority adjustment strategy.

#### Overview

When a high-priority task is blocked while waiting for a semaphore, the system automatically boosts the priority of the low-priority task currently holding the semaphore to be the same as the blocked high-priority task. This allows the lock-holding task to complete its critical section and release the lock as quickly as possible, thus minimizing the blocking time of the high-priority task. Once the lock is released, the holder's priority is restored.

Since the semaphore is the most fundamental synchronization primitive in openvela, implementing priority inheritance for it means that higher-level mechanisms like mutexes automatically gain this capability.

#### Data Structures

The implementation of priority inheritance relies on the following core data structures:

- `struct sem_s`: Describes the semaphore itself, including its count, list of waiting tasks, and holder information.
- `struct semholder_s`: Describes the ownership of a semaphore, linking a Task Control Block (TCB) to the semaphores it holds.

**`struct sem_s` Key Members**

```c
/* This is the generic semaphore structure. */
struct sem_s
{
  volatile int32_t semcount;      // >0: Number of available resources; <0: Number of waiting tasks
  uint8_t flags;                  // Protocol flags (SEM_PRIO_INHERIT, etc.)
  dq_queue_t waitlist;            // Priority queue of waiting tasks

#ifdef CONFIG_PRIORITY_INHERITANCE
#  if CONFIG_SEM_PREALLOCHOLDERS > 0
  FAR struct semholder_s *hhead;  // Head of the holder list
#  else
  struct semholder_s holder;      // Slot for a single holder
#  endif
#endif
#ifdef CONFIG_PRIORITY_PROTECT
  uint8_t ceiling;                // Priority ceiling
  uint8_t saved;                  // Task's original priority
#endif
};
```

**`struct semholder_s` Key Members**

```c
/* This structure contains information about the holder of a semaphore */
struct semholder_s
{
  FAR struct semholder_s *flink;  // Points to the next holder of the same semaphore
  FAR struct semholder_s *tlink;  // Points to the next semaphore held by the same task
  FAR struct sem_s *sem;          // Points to the corresponding semaphore
  FAR struct tcb_s *htcb;         // Points to the TCB of the holder task
  int32_t counts;                 // Hold count
};
```

#### Implementation Process

1. **Acquisition and Inheritance**: When a task attempts to acquire a semaphore that is already held, the system boosts the priority of the low-priority task holding the semaphore to the priority of the current task.
2. **Restoration**: When a task releases a semaphore, the system recalculates its priority. It checks if the task holds other semaphores and sets its new priority based on the highest-priority task waiting for any of those semaphores. If it no longer holds any semaphores that caused a priority boost, its priority is restored to its base value.

#### Configuration

- `CONFIG_PRIORITY_INHERITANCE`: Enables the priority inheritance feature.
- `CONFIG_SEM_PREALLOCHOLDERS`: Defines the number of pre-allocated `semholder_s` structures, determining how many different tasks can hold a semaphore simultaneously (applicable for semaphores with a count greater than 1).

## V. API Reference

### `int sem_init(sem_t *sem, int pshared, unsigned int value)`

- **Description**: Initializes an unnamed semaphore.
- **Parameters**:
    - `sem`: A pointer to the semaphore object to be initialized.
    - `pshared`: Not used in openvela; should be set to 0.
    - `value`: The initial count of the semaphore.
- **Remarks**: After initialization, the semaphore can be used by functions like `sem_wait()` and `sem_post()`.

### `int sem_destroy(sem_t *sem)`

- **Description**: Destroys an unnamed semaphore previously initialized by `sem_init()`.
- **Caution**:
    - Destroying a semaphore that other tasks are currently waiting on results in undefined behavior.
    - This function cannot be used to destroy a named semaphore.

### `sem_t *sem_open(const char *name, int oflag, ...)`

- **Description**: Opens or creates a connection to a named semaphore.
- **Remarks**: Allows unrelated tasks to access the same semaphore by its name.

### `int sem_close(sem_t *sem)`

- **Description**: Closes the connection to a named semaphore.
- **Remarks**: Releases the current task's reference to the semaphore. The semaphore resource is only reclaimed by the system after all references have been closed and `sem_unlink()` has been called.

### `int sem_unlink(const char *name)`

- **Description**: Removes a named semaphore from the system.
- **Remarks**: If tasks are still using the semaphore, its removal is deferred until the last task closes its connection via `sem_close()`.

### `int sem_wait(sem_t *sem)`

- **Description**: Acquires (waits for) a semaphore.
- **Remarks**: Decrements the semaphore's count. If the count becomes negative, the calling task is blocked until another task releases the semaphore.

### `int sem_timedwait(sem_t *sem, const struct timespec *abstime)`

- **Description**: A version of `sem_wait()` with a timeout.
- **Remarks**: If the semaphore cannot be acquired before the absolute time specified by `abstime`, the function times out and returns with the error `ETIMEDOUT`.

### `int sem_trywait(sem_t *sem)`

- **Description**: Attempts to acquire a semaphore without blocking.
- **Remarks**: If the semaphore is immediately available, it is acquired, and the function returns success. Otherwise, it returns an error immediately, and the calling task is not blocked.

### `int sem_post(sem_t *sem)`

- **Description**: Releases (posts to) a semaphore.
- **Remarks**: Increments the semaphore's count. If any tasks are waiting on the semaphore, one of them (typically the highest-priority one) is unblocked. This function is safe to call from an Interrupt Service Routine (ISR).

### `int sem_getvalue(sem_t *sem, int *sval)`

- **Description**: Gets the current value of a semaphore.
- **Remarks**:
    - If the value is positive, it represents the number of available resources.
    - If the value is zero, there are no available resources and no waiting tasks.
    - If the value is negative, its absolute value represents the number of tasks waiting for the semaphore.

### `int sem_setprotocol(pthread_mutexattr_t *attr, int protocol)`

- **Description**: Sets the priority protocol for a semaphore.
- **Parameter `protocol`**:
    - `SEM_PRIO_NONE`: No special protocol (for signaling semaphores).
    - `SEM_PRIO_INHERIT`: Use priority inheritance.
    - `SEM_PRIO_PROTECT`: Use priority protection.

### `int sem_getprotocol(const pthread_mutexattr_t *attr, int *protocol)`

- **Description**: Gets the current priority protocol of a semaphore.

## VI. Implementation Details

This section delves into the internal implementation of openvela semaphores, intended for readers who want to understand the underlying mechanisms or engage in system development.

### 1. Core Framework

The openvela semaphore implementation is built around the `struct sem_s` core structure, a global pool of holders, and a queue for waiting tasks.

- **`struct sem_s`**: The core data structure for a semaphore, maintaining its count, wait queue (`waitlist`), and list of holders (`hhead`).
- **`g_freeholders`**: A global pool of `semholder_s` structures, used for on-demand allocation and deallocation of holder objects when priority inheritance is enabled, avoiding the overhead of dynamic memory allocation.
- **`waitlist`**: A doubly-linked list, sorted by task priority, that holds all tasks blocked on the semaphore.

### 2. Key Function Analysis

#### `nxsem_wait_slow()` (Core of sem_wait)

**Execution Flow**:

1. **Enter Critical Section**: Disable interrupts to ensure atomicity.
2. **Attempt to Acquire**: Atomically decrement the semaphore count.
3. **Acquisition Succeeded**: If the count is still non-negative after decrementing, the acquisition is successful.
    - If priority protection is enabled, call `nxsem_protect_wait()` to boost the task's priority.
    - If priority inheritance is enabled, call `nxsem_add_holder()` to register the current task as a holder.
4. **Block and Wait**: If the count becomes negative, the resource is unavailable.
    - Set the current task's state to `TSTATE_WAIT_SEM`.
    - If priority inheritance is enabled, call `nxsem_boost_priority()` to boost the priority of other holders.
    - Remove the current task from the ready-to-run list and add it to the semaphore's `waitlist`.
    - Call `up_switch_context()` to perform a context switch and yield the CPU.
5. **Wake-up**: When the task is awakened by `sem_post()`, it returns from `up_switch_context()` and checks for errors (e.g., interruption by a signal).
6. **Leave Critical Section**: Re-enable interrupts and return.

#### `nxsem_post_slow()` (Core of sem_post)

**Execution Flow**:

1. **Enter Critical Section**: Disable interrupts.
2. **Atomic Increment**: Atomically increment the semaphore count and check for overflow.
3. **Release Holder**: If priority inheritance is enabled, call `nxsem_release_holder()` to decrement the current task's hold count.
4. **Check for Waiters**: If the count was negative before the increment, it means tasks are waiting.
    - Remove the highest-priority task from the `waitlist`.
    - If the task has a watchdog timer set, cancel it.
    - Register this task as the new holder of the semaphore.
    - Call `nxsched_add_readytorun()` to move it to the ready-to-run list.
    - If the awakened task has a higher priority than the current task, perform a context switch.
5. **Restore Priority**: If priority inheritance or protection is enabled, call the appropriate function to restore the priorities of relevant tasks.
6. **Leave Critical Section**: Re-enable interrupts and return.

#### `nxsem_clockwait()` and Timeout Handling

The core logic for timed waits (`sem_timedwait`) is implemented in `nxsem_clockwait`.

- **Timer Setup**: After failing to acquire the semaphore, it starts a watchdog timer (`wd_start_...`) and sets the timeout callback to `nxsem_timeout`.
- **Timeout Wake-up**: If the timer expires, `nxsem_timeout` is called. Its main job is to call `nxsem_wait_irq`.
- **Interrupt/Timeout Handling**: `nxsem_wait_irq` is responsible for the wake-up logic. It will:
    1. Call `nxsem_canceled()` to restore any boosted priorities.
    2. Increment the semaphore count (to counteract the decrement from the `wait` operation).
    3. Remove the task from the `waitlist`.
    4. Add the task back to the ready-to-run list.

## VII. Summary

The openvela semaphore mechanism is a cornerstone for building robust multitasking applications. Developers should fully understand its core features and choose the appropriate usage pattern for their application scenario:

- **For Mutual Exclusion**: Use a **Locking Semaphore** and enable **priority inheritance** or **priority protection** to prevent priority inversion.
- **For Task Synchronization**: Use a **Signaling Semaphore** and **disable** priority-related protocols (`SEM_PRIO_NONE`) to ensure predictable scheduling behavior.

By skillfully applying these mechanisms, you can effectively guarantee your system's real-time performance, stability, and scheduling efficiency.
