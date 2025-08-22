# Power Management Wakelock Usage Guide

\[ English | [简体中文](../../../zh-cn/device_dev_guide/power_mgt/pm_wakelock_guide.md) \]

This document provides a detailed guide for openvela developers on the `Wakelock` mechanism in Power Management (PM). Unlike the reactive approach of using `prepare` callbacks at the driver level, a `Wakelock` allows the application layer or middleware to **proactively** request that the system remain at a specified power level when it anticipates the need for system activity, thereby preventing unnecessary sleep states.

**Prerequisite Reading**: Before you begin, we highly recommend reading the [Power Management Framework Guide](./pm_framework_guide.md) to fully understand the core concepts of the PM framework.

## I. Core Concepts and Use Cases

In embedded development, certain tasks—such as file writes, network data transfers, or firmware updates—require preventing the system from entering a low-power state for a period to ensure task integrity and real-time performance.

The traditional method is to implement a `prepare` callback in a device driver to veto a sleep request. However, this approach has two main problems:

1. **Performance Overhead**: The `prepare` callback is invoked every time the system attempts to enter a low-power state, even during non-critical tasks. This increases the interrupt-disabled time in the Idle Loop and adds to the overall system overhead.
2. **High Sleep Failure Rate**: This is a **post-facto** check. The PM framework has already decided to sleep before it asks drivers for their consent. If a driver vetoes the transition, it results in a failed power state change attempt and a state rollback, which harms the efficiency of power management.

The `Wakelock` mechanism solves these issues through a **proactive request** model. When a task begins, it acquires a `Wakelock`; when the task ends, it releases the `Wakelock`. The PM framework will only attempt to transition the system into a deeper sleep state when no active `Wakelocks` exist.

**In short: Prioritize using a `Wakelock` whenever you can predict the need to prevent system sleep at the business logic level.**

## II. API Reference

Wakelock functionality is provided through a series of `pm_wakelock_*` interfaces in `pm.h`.

### `pm_wakelock_init`

Initializes a `Wakelock` instance.

```C
void pm_wakelock_init(FAR struct pm_wakelock_s *wakelock,
                      FAR const char *name, int domain,
                      enum pm_state_e state)
```

- **Use Case**: Call this function during the initialization phase of a module or driver to create a named `Wakelock`.
- **Parameters**:

    - `wakelock`: A pointer to an instance of a user-defined `pm_wakelock_s` structure.
    - `name`: The name string for the lock. This name is used for identification and debugging in Procfs.
    - `domain`: The target Power Domain for this `Wakelock`.
    - `state`: The **minimum power state** the system can enter while this `Wakelock` is held. For example, if set to `PM_IDLE`, holding this lock will prevent the system from entering `PM_STANDBY` or `PM_SLEEP`.

### `pm_wakelock_stay`

Acquires the specified `Wakelock`.

```C
void pm_wakelock_stay(FAR struct pm_wakelock_s *wakelock)
```

- **Use Case**: Call this function before a critical operation begins to notify the PM framework that the system needs to remain active.
- **Description**: This function internally maintains a reference count. You can call `pm_wakelock_stay` multiple times, but a corresponding number of `pm_wakelock_relax` calls are required to fully release the lock.

### `pm_wakelock_relax`

Releases the specified `Wakelock`.

```C
void pm_wakelock_relax(FAR struct pm_wakelock_s *wakelock)
```

- **Use Case**: Call this function after a critical operation is complete to inform the PM framework that the system may enter sleep states normally.
- **Description**: This function decrements the `Wakelock`'s reference count. The `Wakelock` is only fully released when its reference count reaches zero. It must be used in **matching pairs** with `pm_wakelock_stay`.

### `pm_wakelock_staytimeout`

Acquires a `Wakelock` with an automatic timeout release.

```C
void pm_wakelock_staytimeout(FAR struct pm_wakelock_s *wakelock, int ms);
```

- **Use Case**: Suitable for operations that need to keep the system active for a fixed duration.
- **Description**: After calling this function, the `Wakelock` will be held for `ms` milliseconds and then automatically released. If this function is called again before the timeout expires, the timer will be reset.

### `pm_wakelock_staycount`

Gets the current reference count of a `Wakelock`.

```C
int pm_wakelock_staycount(FAR struct pm_wakelock_s *wakelock);
```

- **Use Case**: Primarily for debugging. You can check the current hold count of a lock before calling `pm_wakelock_relax` to prevent asymmetrical release operations.

## III. Key Advantages

Adopting the `Wakelock` mechanism provides the following significant benefits for your system:

### 1. Reduced System Overhead

By using proactive locking, the system avoids iterating through and calling the `prepare` callbacks of all drivers during every idle cycle. This effectively reduces the interrupt-disabled time and improves system responsiveness.

### 2. Improved Power Management Efficiency

The status of `Wakelocks` is checked early in the PM framework's decision-making process. This significantly reduces power state rollbacks caused by driver vetoes during the `prepare` phase, leading to smoother and more efficient power state transitions.

### 3. Enhanced Debuggability

If Procfs (`CONFIG_FS_PROCFS`) is enabled, you can view the real-time status of all `Wakelocks` in the system by accessing the `/proc/pm/wakelock` filesystem node. This includes their names, hold counts, and cumulative active time, greatly simplifying the debugging of power consumption issues.

For more details, see [PM procfs usage](./pm_procfs_debug.md).
