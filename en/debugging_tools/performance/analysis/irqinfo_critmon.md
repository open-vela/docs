# Using irqinfo and critmon for Interrupt and Critical Section Monitoring

\[ English | [简体中文](./../../../../zh-cn/debugging_tools/performance/analysis/irqinfo_critmon.md) \]

This document provides a detailed guide for embedded developers on using the two core tools, `irqinfo` and `critmon`, on the `openvela` system. You will learn how to monitor interrupt performance, analyze critical section execution time, and track the maximum hold time of the scheduler lock, enabling you to identify system performance bottlenecks and optimize real-time behavior.

## I. Overview

`irqinfo` and `critmon` are two powerful command-line tools provided by the `openvela` system for real-time performance analysis.

- `irqinfo`: Focuses on Interrupt (IRQ) monitoring. It collects statistics on the trigger frequency, number of occurrences, and maximum execution time of the Interrupt Service Routine (ISR) for each interrupt. This is crucial for identifying "interrupt storms" or excessively long interrupt handling.
- `critmon`: Focuses on monitoring the execution time of critical sections and scheduler locks. It tracks the longest time each thread spends with interrupts disabled (in a critical section) or with the scheduler disabled, helping you discover the key code paths that cause system response delays.

## II. System Configuration

To use these monitoring tools, you must enable the corresponding kernel configuration options in your `defconfig` file and ensure that the `procfs` file system is properly mounted.

### 1. General Configuration: Mounting `procfs`

Both `irqinfo` and `critmon` rely on the `procfs` file system to expose their statistical data. Please ensure that `CONFIG_FS_PROCFS=y` is enabled in your system and execute the following command to mount `procfs` after system startup:

```Bash
mount -t procfs /proc
```

### 2. `irqinfo` Specific Configuration

To enable interrupt frequency and execution time statistics, set the following Kconfig options:

```Makefile
# Enable interrupt monitoring feature
CONFIG_SCHED_IRQMONITOR=y

# Enable procfs file system support
CONFIG_FS_PROCFS=y
```

### 3. `critmon` Specific Configuration

To enable statistics for critical sections, scheduler locks, and thread execution time, set the following Kconfig options:

```Makefile
# Enable critical section and scheduler lock monitoring
CONFIG_SCHED_CRITMONITOR=y  

# Enable the critmon user-space command-line tool
CONFIG_SYSTEM_CRITMONITOR=y 

# Enable procfs file system support
CONFIG_FS_PROCFS=y
```

**Important Note**: After enabling `CONFIG_SCHED_CRITMONITOR`, the following two options have a default value of `-1` (disabled). You must change them to `0` to enable the statistics feature.

```Makefile
# Set to 0 to enable critical section execution time statistics
CONFIG_SCHED_CRITMONITOR_MAXTIME_CSECTION=0

# Set to 0 to enable scheduler lock execution time statistics
CONFIG_SCHED_CRITMONITOR_MAXTIME_PREEMPTION=0
```

## III. Using `irqinfo` for Interrupt Analysis

The `irqinfo` tool helps you gain deep insights into your system's interrupt behavior.

### 1. Usage

Simply execute the `irqinfo` command in the shell to view the statistics.

```Bash
irqinfo
```

- **First execution**: Displays cumulative interrupt statistics from system boot to the current time.
- **Subsequent executions**: Displays incremental interrupt statistics since the last `irqinfo` command was executed.

The statistical data is automatically cleared after each read, which facilitates segmented observation.

### 2. Interpreting the Output

```Bash
ap> irqinfo
IRQ  HANDLER   ARGUMENT     COUNT  RATE    TIME (us)
---  --------  --------     -----  ------  ---------
11   2c604591  00000000       233   0.000         12
39   0005753d  2c786451        18   2.395         83
43   0005753d  00057455       759   0.000        143
```

| **Column Name** | **Description**                                                                                                     |
| :-------------- | :------------------------------------------------------------------------------------------------------------------ |
| `IRQ`           | **Interrupt Number**. A unique numerical identifier to distinguish different interrupt sources.                     |
| `HANDLER`       | **Interrupt Handler Address**. A memory address pointing to the Interrupt Service Routine (ISR) for this interrupt. |
| `ARGUMENT`      | **Argument passed to the handler**. Usually `0` or a pointer to a specific device instance.                         |
| `COUNT`         | **Number of Occurrences**. The total number of times the interrupt was triggered during the statistical period.     |
| `RATE`          | **Interrupt Frequency (times/sec)**. The average number of triggers per second during the statistical period.       |
| `TIME`          | **Maximum Execution Time (μs)**. The longest time a single execution of the ISR took, in microseconds.              |

### 3. Analysis Techniques

#### Resolving the Interrupt Handler (HANDLER)

You can use the `addr2line` tool to convert the `HANDLER` address into a specific file name and line number, thereby locating the ISR source code.

```Bash
addr2line -fe <your_elf_file> <address>
addr2line -fe nuttx 0005753d
```

Example output:

```Bash
up_irq_handler
/path/to/nuttx_os.c:55
```

**Note**: In many ARM architecture implementations, peripheral interrupts share a top-level entry point (like `up_irq_handler`). In such cases, you need to use the `IRQ` number to further distinguish the specific interrupt source.

#### Resolving the Interrupt Number (IRQ)

The meaning of an `IRQ` number is highly dependent on the hardware platform and architecture.

- **ARM Platforms**

    - **0-15**: Typically system-level interrupts (e.g., SVC, PendSV). The corresponding interrupt can be found via the interrupt handler (HANDLER).
    - **> 15**: Hardware interrupts. To map them to the `IRQn` enum defined in the board-level header file, use the formula: `enum value = IRQ number - 16`.

- **Xtensa Platforms**

    - IRQ definitions are usually located in a platform-specific board-level header file. Please consult it directly.

**Example Analysis and Code Mapping:**

The following `irqinfo` output demonstrates how to map an IRQ number to its definition in a BSP header file.

```Bash
ap> irqinfo
IRQ HANDLER  ARGUMENT    COUNT    RATE    TIME
 11 2c604591 00000000          8    0.205    7  # System interrupt, SVC
 39 0005753d 2c786451         37    0.948   62  # Hardware interrupt, 39-16=23 -> UART0_IRQn
 43 0005753d 00057455       3862   99.015   73  # Hardware interrupt, 43-16=27 -> Timer11 Interrupt
 ```

 ```C
/* Example: framework/services/platform/cmsis/inc/best1600.h */
typedef enum IRQn {
    // ...
    UART0_IRQn                =  23,      /*!< UART0 Interrupt                    */
    // ...
    SYS_TIMER11_IRQn          =  27,      /*!< Timer11 Interrupt                  */
    // ...
} IRQn_Type;
```

## IV. Using `critmon` for Critical Section and Scheduler Lock Analysis

The `critmon` tool helps you monitor the longest time a thread spends with interrupts or scheduling disabled.

### 1. Usage

`critmon` provides a set of commands to control and display statistics.

- **`critmon`**:

    Displays statistics. Similar to `irqinfo`, the first execution shows cumulative data, while subsequent executions show incremental data. The data is automatically cleared after being read.

- **`critmon_start`**:

    Starts a background task that automatically prints `critmon` statistics at an interval defined by `CONFIG_SYSTEM_CRITMONITOR_INTERVAL` (default is 2 seconds).

- **`critmon_stop`**:

    Stops the background auto-printing task.

### 2. Interpreting the Output

```Bash
ap> critmon
PRE-EMPTION  CALLER      CSECTION     CALLER      RUN          TIME         PID  DESCRIPTION
-----------  ----------  -----------  ----------  -----------  -----------  ---  -----------
1.392849000              0.004460000              -----------  -----------  ---- CPU 0
0.000039000  0x81f88a7   0.000021000  0x81bf457   0.000631000  0.012379000    1  hpwork
0.001204000  0x81ccc6d   0.000029000  0x81bcfa1   0.001750000  0.108839000    3  nsh_main
```

| **Column Name**          | **Description**                                                                                                                                                            |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PRE-EMPTION` & `CALLER` | **Longest preemption-off time (seconds)** and **Caller address**.<br>Records the longest duration a thread disabled the scheduler via `sched_lock()` or similar functions. |
| `CSECTION` & `CALLER`    | **Longest critical section time (seconds)** and **Caller address**.<br>Records the longest duration a thread entered a critical section via `enter_critical_section()`.    |
| `RUN`                    | **Longest single run time (seconds)**.<br>The longest continuous time a thread ran between two preemptions.                                                                |
| `TIME`                   | **Total run time (seconds)**. The total time the thread held the CPU during the statistical period.                                                                        |
| `PID`                    | **Thread ID**.                                                                                                                                                             |
| `DESCRIPTION`            | **Thread Name**.                                                                                                                                                           |

### 3. Analyzing a Single Thread's Execution Time

You can also retrieve monitoring data for a single thread by reading the corresponding node in the `/proc` file system. This is very useful for writing automated test scripts or for fine-grained analysis.

- **Command**: `cat /proc/<pid>/critmon`
- **Function**: Gets the longest single run time and total run time for the specified PID.

![img](./figures/001.png)

## V. Implementation Principles

- **Interrupt Monitoring (`irqinfo`)**: The system records a timestamp each time it enters and exits an ISR. By calculating the difference, it obtains the single execution time and compares it with the recorded maximum value to update it if necessary. A counter is incremented each time the interrupt is triggered.
- **Critical Section/Scheduler Lock Monitoring (`critmon`)**:

    - **Disabling/Enabling Interrupts**: The `enter_critical_section()` and `leave_critical_section()` functions have built-in timing logic to calculate and update the maximum time the current thread has disabled interrupts. It records the MAX value for the critical section time. Timing starts at boot, is cleared upon reading, and then restarts.
    - **Disabling/Enabling Scheduler**: The `sched_lock()` and `sched_unlock()` functions also contain timing logic to calculate and update the maximum time the current thread has disabled the scheduler. The tool records the MAX time for this as well, using the same principle.

## Appendix: Key Concept Explanations

- **Interrupt (IRQ) and Interrupt Service Routine (ISR)**

    - **Interrupt (IRQ)**: A signal sent by hardware or software to the CPU, indicating an urgent event that needs immediate attention.
    - **Interrupt Service Routine (ISR)**: A piece of code specifically designed to handle a particular interrupt event. When an interrupt occurs, the CPU suspends its current task and executes the corresponding ISR.

- **Critical Section**

    - Refers to a segment of code that must be executed atomically, meaning it cannot be interrupted or preempted by other tasks during its execution. In `openvela`/NuttX, this is typically achieved by **disabling all interrupts**. The `CSECTION` column in `critmon` monitors the time a thread holds this highest-priority lock. Occupying a critical section for a long time can severely impact the system's real-time responsiveness.

- **Scheduler Lock**

    - A lighter-weight lock than a critical section. It **only disables the task scheduler**, preventing the OS from switching to other tasks, but it **does not disable hardware interrupts**. This means that while a scheduler lock is held, interrupts can still occur and be processed. The `PRE-EMPTION` column in `critmon` monitors the time a thread holds the scheduler lock.

- **`procfs` (Process File System)**

    - A virtual file system that does not reside on a physical disk but is dynamically generated by the kernel in memory. It provides a user interface that allows users to view and modify the kernel's internal data structures and state by reading and writing files. `irqinfo` and `critmon` use `procfs` to expose the statistical data from the kernel to user-space command-line tools.
