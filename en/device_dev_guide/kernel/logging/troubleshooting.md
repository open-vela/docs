# Log Management and Troubleshooting

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/kernel/logging/troubleshooting.md) \]

This document aims to explain common issues encountered in advanced logging scenarios within the openvela system and provide corresponding solutions and best practices. The content covers log concurrency, `ramlog` initialization, and Android API compatibility.

## I. Solving the Log Interleaving Issue

### Problem Description

In a multi-core (SMP) or concurrent environment, log outputs from different execution units (such as multi-core threads or Interrupt Service Routines) can become interleaved. This can lead to individual log messages being truncated or mixed, reducing log readability.

**Root Cause**: Log output operations are not atomic. When a task is outputting a log through a device like a serial port, the operating system may schedule another high-priority task (or respond to an interrupt). This new task may also attempt to output a log, thereby interrupting the previous, unfinished output.

To ensure the integrity and atomicity of each log message, we recommend the following three solutions, which can be combined based on system requirements.

### Solutions

#### Solution 1: Enable Log Line Buffering

This mechanism avoids interruptions during output by constructing a complete log line in memory and then submitting it to the underlying driver in a single operation.

You need to enable the relevant `syslog` buffer configurations:

- `CONFIG_SYSLOG_BUFFER=y`: Enables the `syslog` buffer for applications and kernel threads.
- `CONFIG_SYSLOG_INTBUFFER=y`: Provides a separate `syslog` buffer specifically for Interrupt Service Routines (ISRs) to avoid contention with threads.

#### Solution 2: Optimize Mixed Use of `printf` and `syslog`

When `printf` and `syslog` must be used together in the system, enabling line buffering for `printf` (and its underlying `stdio`) and configuring a sufficiently large buffer size can significantly reduce the probability of interleaved printing.

It is recommended to enable the following configurations:

```Makefile
# Enable line buffering for standard output (stdout)
CONFIG_STDIO_LINEBUFFER=y

# Allocate buffers for standard I/O streams, 512 bytes or more is recommended
CONFIG_STDIO_BUFFER_SIZE=512
CONFIG_STREAM_OUT_BUFFER_SIZE=256

# Configure ample TX/RX buffers for the underlying serial driver to handle data bursts
CONFIG_UART0_TXBUFSIZE=1024
CONFIG_UART0_RXBUFSIZE=1024
```

#### Solution 3: Achieve Atomic Output Using Hardware Features

For scenarios with extremely high performance requirements, underlying hardware features can be leveraged to guarantee output atomicity.

1. **Implement the `up_nputs` Interface**: The chip's Board Support Package (BSP) should implement the `up_nputs` function. This function typically ensures that it cannot be preempted while outputting a complete string—by disabling interrupts or using a spinlock—thereby achieving hardware-level atomicity.
2. **Enable DMA Transfer**: If the serial (UART) hardware supports Direct Memory Access (DMA), it should be enabled as a priority. Once started, the DMA controller transfers the entire log buffer data to the serial port in the background. This process does not occupy the CPU and cannot be interrupted by other threads, making it the most efficient and atomic way to output logs.

## II. Solving the `ramlog` Garbled Log Issue on Cold Start

### Problem Description

`ramlog` is a mechanism for recording logs in RAM, which allows a device to retain log information from before a crash even after a software reset (Warm Reset). However, when the system restarts after a complete power loss (Cold Start), the data in RAM is random, and reading it directly will result in garbled logs.

### Solution

By introducing a magic number and persistent read/write pointers into the `ramlog` buffer, the system can determine the boot type and perform a fast initialization.

#### Design Rationale

1. **Magic Number**: Reserve 4 bytes at a fixed location in the `ramlog` ring buffer (e.g., at the end) to store a predefined, non-zero special value (the magic number).
2. **Persistent Pointers**: Store the current values of the `head` and `tail` pointers within the buffer itself.

#### Initialization Flow

On system startup, the `ramlog` driver should perform the following logic:

1. Check the magic number:

    - **Mismatch**: This indicates a cold start. The RAM content is invalid.
        - Use `memset` to clear the entire `ramlog` buffer.
        - Initialize the `head` and `tail` pointers to `0`.
        - Write the correct magic number to the fixed location.
    - **Match**: This indicates a warm reset. The RAM contains valid logs.
        - Directly read the `head` and `tail` pointer values already saved in RAM to quickly restore the log read/write state.
        - The buffer is not cleared, preserving the final logs from before the reset.

With this mechanism, `ramlog` can not only effectively distinguish between cold and warm starts but also recover quickly after a warm reset, providing critical information for diagnostics.

## III. Compatibility with Android Log API

The openvela system is natively compatible with the standard Android NDK logging interface, allowing engineers familiar with Android application development to seamlessly migrate their logging code.

- **Direct Usage**: Developers can directly include the `<android/log.h>` header file and use all the logging APIs and macros defined within it, such as `__android_log_print()`.
- **No Modification Needed**: Logging code in existing Android C/C++ projects can be compiled and run on the openvela system without any changes.

## IV. Related Documents

- [A Deep Dive into the System Log (Syslog)](./syslog.md)
- [printf Function Usage Guidelines](./printf.md)

## V. References

- [Logging  |  Android NDK  |  Android Developers](https://developer.android.com/ndk/reference/group/logging)
- [Using Asserts in Embedded Systems | Interrupt (memfault.com)](https://interrupt.memfault.com/blog/asserts-in-embedded-systems)
- [Exploring printf on Cortex-M | Interrupt (memfault.com)](https://interrupt.memfault.com/blog/printf-on-embedded)
- https://kb.segger.com/DCC
- https://github.com/eyalroz/printf
- https://interrupt.memfault.com/blog/device-logging