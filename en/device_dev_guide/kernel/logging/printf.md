# printf Function Usage Guidelines

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/kernel/logging/printf.md) \]

## I. Overview

The `printf` function is primarily intended for the development and debugging phases, used to print formatted information to standard output (stdout) in command-line tools that require direct user interaction.

**Core Principle**: The use of `printf` is strictly prohibited in kernel modules and background services. In such scenarios, `syslog` should be used as the standard logging solution. Improper use of `printf` can trigger severe issues in multi-core systems, such as service blocking, resource exhaustion, and log corruption, posing a threat to system stability and real-time performance.

## II. Use Case: Command-Line Interaction

The only recommended use case for `printf` is in the development of command-line interface (CLI) applications that require direct interaction with the user.

- **Function**: To output program status, user prompts, or debugging information to the console (terminal) in real-time.
- **Example**: A tool that requires user-input parameters and immediately displays the results.

## III. Prohibited Scenarios and Core Risk Analysis

The use of `printf` must be forbidden in the following scenarios:

- **Kernel Modules**
- **Background Services & Daemons**

The main risk analysis is as follows:

### 1. Multi-Core Blocking and IPC Resource Exhaustion

In a multi-core system, the implementation of `printf` relies on inter-processor communication (IPC) between cores.

- **Mechanism**: When a non-primary core calls `printf`, the system sends the content to be printed to the primary core via the `uart_rpmsg` IPC mechanism. A terminal tool such as `cu` on the primary core is then responsible for displaying it.
- **Risk**: If the terminal tool on the primary core is not listening to the corresponding non-primary core device (for example, `cu -l /dev/ttyRBT` has not been executed), IPC messages will accumulate in the buffer, leading to the following severe consequences:

    - **IPC Buffer Exhaustion**: Because messages cannot be consumed, the IPC buffer will be rapidly depleted, causing new IPC requests to fail.
    - **System Service Blocking**: Other critical system services that rely on IPC (such as heartbeats or data synchronization) will be blocked because they cannot acquire a buffer, potentially leading to a system hang or crash.
    - **Log Corruption and Truncation**: When used concurrently with `syslog`, the synchronous, blocking nature of `printf` interferes with `syslog`'s asynchronous log stream. This can cause log entries to be truncated, interleaved, or lost entirely, rendering them unreadable.

### 2. Thread Blocking

The underlying implementation of `printf` involves file I/O operations, which are blocking calls. The thread that calls `printf` will be suspended until the data is fully written to the output buffer. For tasks with real-time requirements, this non-deterministic blocking time is unacceptable.

### 3. Disabled in Interrupt Context (ISR)

`printf` is not a re-entrant function and can cause blocking. Calling it from an Interrupt Service Routine (ISR) will destroy system real-time performance and may even lead to a system crash.

### 4. Data Volatility

The output of `printf` flows directly to a standard output device (like a serial terminal) and is not persistently stored in a log file. All printed information is lost after a system reboot or session closure.

## IV. Best Practices and Alternatives

### 1. Use `syslog` for Logging

For kernels and services, the `syslog` API must be used for logging. `syslog` offers the following advantages:

- **Asynchronous and Non-blocking**: Calling `syslog` does not block the current thread.
- **Unified Management**: Supports log levels (e.g., DEBUG, INFO, ERROR) for easy filtering and management.
- **Persistence**: Can be configured to save logs to a file or send them to a remote server.

> **Note**: In the Linux kernel environment, the `printk` function has a role and position similar to `syslog`, used for outputting logs to the kernel ring buffer, rather than being a direct equivalent to the user-space `printf`.

### 2. Ensure Cross-Platform Compatibility

When using `printf` in its appropriate context (CLI tools), it is recommended to use the macros defined in the [<inttypes.h>](https://cplusplus.com/reference/cinttypes/) header to format integers. This ensures code portability across different architectures (e.g., 32-bit/64-bit).

**Example:**

```C
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
int main() {
    uint64_t my_large_number = 12345678901234567890ULL;

    // Use the PRIu64 macro to correctly print a uint64_t type
    printf("My large number is: %" PRIu64 "\n", my_large_number);
    return 0;
}
```

## V. Function Prototype

```C
#include <stdio.h>

int printf(const char *format, ...);
```

## VI. Related Documents

- [A Deep Dive into the System Log (Syslog)](./syslog.md)
- [Log Management and Troubleshooting](./troubleshooting.md)

