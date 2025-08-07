# Power Management Procfs Debugging Guide

\[ English | [简体中文](../../../zh-cn/device_dev_guide/power_mgt/pm_procfs_debug.md) \]

This document guides developers on how to use the Power Management (PM) interface provided by Procfs (the `/proc` file system) in the openvela system. Through this interface, you can monitor the power state distribution of each Power Domain in real-time and diagnose `Wakelock` usage, making it a powerful tool for power consumption optimization and issue diagnosis.

**Prerequisite**: The system must have Procfs enabled in Kconfig (`CONFIG_FS_PROCFS=y`).

## I. Accessing PM Debugging Information

You can access PM debugging information in two ways: by using the convenient `pmconfig` command or by directly reading the files in Procfs.

### Method 1: Using the `pmconfig` Command (Recommended)

`pmconfig` is a command-line wrapper tool that aggregates and displays the status and `Wakelock` information for all power domains in the system. It is the preferred method for viewing a PM overview.

Execute the following in the target device's shell:

```Bash
pmconfig
```

### Method 2: Accessing Procfs Files Directly

You can also read the underlying Procfs files directly using the `cat` command. This method is particularly useful for scripting or remote access (e.g., via `adb shell`). The PM information files are located in the `/proc/pm/` directory and are distinguished by their Power Domain index.

- **State File**: `/proc/pm/state<domain_id>`
- **Wakelock File**: `/proc/pm/wakelock<domain_id>`

**Example: Viewing PM Information for Each Core in a Multi-Core System**

```Bash
Assuming the system includes an Application Processor (AP) and a Communication Processor (CP), you can view their information as follows:

# In environments without mount points, like simulators or QEMU, the path might be /proc/pm/...
# The following example is based on a system where the remote core's file system is mounted at /mnt

# View Domain 0 and Domain 1 information for the local core (AP)
cat /mnt/ap/pm/state0
cat /mnt/ap/pm/wakelock0
cat /mnt/ap/pm/state1
cat /mnt/ap/pm/wakelock1

# View Domain 0 information for the remote core (CP)
cat /mnt/cp/pm/state0
cat /mnt/cp/pm/wakelock0
```

## II. Interpreting Procfs Output

This section explains the meaning of the content in the `state` and `wakelock` files in detail.

### 1. Power State Statistics (`/proc/pm/state<N>`)

This file displays the time spent in each power state since the system started.

**Example Output (`/proc/pm/state0`):**

```Bash
//             Active Time      Sleep Time      Total time in this state (Active + Sleep)
DOMAIN0           WAKE         SLEEP         TOTAL
normal         14s 01%       20s 02%       34s 04%
idle            0s 00%        0s 00%        0s 00%
standby         0s 00%        0s 00%        0s 00%
sleep           0s 00%      712s 95%      712s 95%
```

**Field Descriptions**:

| **Field**             | **Description**                                                                                                                                                                               |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DOMAIN<N>`           | Header indicating the statistics for this power domain.                                                                                                                                       |
| `normal`, `idle`, ... | The various power states supported by the system.                                                                                                                                             |
| `WAKE`                | **Active Time**: The total time the CPU spent **executing code** in this state.                                                                                                               |
| `SLEEP`               | **Sleep Time**: The total time the CPU spent in a **low-power wait state (e.g., WFI)**. <br>For the `sleep` state, this value is a key indicator of the system's energy-saving effectiveness. |
| `TOTAL`               | **Total Time**: The sum of `WAKE` and `SLEEP` time, representing the total duration spent in this state.                                                                                      |
| **(Percentage)**      | The percentage of the total system uptime that was spent in this state.                                                                                                                       |

**Analysis Example**: The output above shows that since startup, `DOMAIN0` has successfully entered the `PM_SLEEP` state for 95% of the time. This indicates that the system's power management strategy is functioning well and achieving effective energy savings.

### 2. Wakelock Statistics (`/proc/pm/wakelock<N>`)

This file lists all registered `Wakelocks` in the specified power domain, along with their current status and historical data.

**Example Output (`/proc/pm/wakelock0`):**

```Bash
//wakelock   state   current stay count  total stay time
DOMAIN0      STATE     COUNT             TIME
system       normal        0             10s
system       idle          0             10s
system       standby       0             10s
system       sleep         0             10s
rptun-tee    idle          0             0s
i2c          normal        0             1s
rptun-cp     idle          0             0s
rptun-sensor idle          0             1s
rptun-audio  idle          0             0s
gpu          normal        0             8s
```

**Field Descriptions**:

| **Field**   | **Description**                                                                                                                                                                                                                              |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DOMAIN<N>` | Header indicating the `Wakelock` list for this power domain.                                                                                                                                                                                 |
| `wakelock`  | The name of the `Wakelock`, specified when calling `pm_wakelock_init`.                                                                                                                                                                       |
| `STATE`     | The **minimum power state** the system is kept in when this `Wakelock` is active. For example, `normal` prevents the system from entering any low-power state.                                                                               |
| `COUNT`     | **Current Reference Count**.<br>If this value is **greater than 0**, it means the lock is **currently held**, preventing the system from entering a deeper sleep state. <br>This is a key indicator for diagnosing power consumption issues. |
| `TIME`      | **Cumulative Hold Time**.<br>The total duration this `Wakelock` has been held since the system started. <br>This value helps identify which modules have historically been the **main contributors to power consumption**.                   |

**Analysis Example**: The output above indicates that in `DOMAIN0`:

- **No** `Wakelocks` are currently active (all `COUNT` values are 0).
- Historically, the `system`, `i2c`, and `gpu` drivers or modules have been the primary `Wakelock` users, with cumulative hold times of 10s, 1s, and 8s, respectively. If the system fails to sleep, the `COUNT` values for these modules should be checked first.
