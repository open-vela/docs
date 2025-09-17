# opus_ramtest Stress Test Guide

[ English | [简体中文](./../../../zh-cn/debugging_tools/stress_testing/opus_ramtest.md) ]

This document provides a detailed guide for configuring and running the `opus_ramtest` stress test on the openvela system. This test evaluates the stability of the system's memory and scheduler under heavy load by concurrently decoding Opus audio data.

## I. Overview

`opus_ramtest` is a stress test tool designed to assess system stability. It creates multiple concurrent child processes (threads), each independently performing high-intensity Opus audio decoding tasks. This applies pressure to two core aspects of the system:

- **Memory System**: Concurrent decoding operations trigger a large volume of memory allocations and deallocations, effectively testing the robustness of the system's memory management. This helps identify issues such as memory leaks, fragmentation, or illegal memory access.
- **Task Scheduler**: A large number of active processes frequently compete for CPU resources, posing a stringent challenge to the operating system's task scheduler. This can be used to evaluate the efficiency, real-time performance, and fairness of the scheduling algorithm.

This test is crucial for verifying the reliability of embedded systems under sustained high loads.

## II. Preparation: System Configuration

Before running the test, you must enable and optimize the relevant components in your system build configuration.

### 1. Enable Core Features

In your `defconfig` file, ensure the following Kconfig options are enabled to integrate the Opus library and the test program:

```bash
CONFIG_LIB_OPUS=y
CONFIG_LIB_OPUS_DEMO=y
CONFIG_TESTING_OPUS_RAMTEST=y
```

- `CONFIG_LIB_OPUS=y`: Enables the Opus audio codec library.
- `CONFIG_LIB_OPUS_DEMO=y`: Enables the Opus demo code, which `opus_ramtest` depends on.
- `CONFIG_TESTING_OPUS_RAMTEST=y`: Compiles and enables the `opus_ramtest` test command.

### 2. Optimize the Test Environment

To ensure the test can effectively apply pressure, make the following configurations:

- **Configure the Task Scheduler:**

    - Set `CONFIG_RR_INTERVAL`, the time slice for Round-Robin scheduling. **Reducing this value increases the frequency of task switching, thereby increasing the scheduling pressure on the system**. For example, setting it to `5` (milliseconds) provides good test results.
    - `CONFIG_RR_INTERVAL=5`

- **Adjust the Main Process Stack Size:**

    - If a stack overflow occurs when the test process starts, you need to increase the main process's stack space.
    - Modify the value of `CONFIG_TESTING_OPUS_RAMTEST_STACKSIZE`. The default value is `40960` bytes.

## III. Executing the Test

### 1. Disable the Watchdog

Prolonged stress testing may slow down system responsiveness, potentially triggering a watchdog reset. Before testing, use the following command to disable the watchdog:

```bash
echo V > /dev/watchdog0
```

### 2. Run the Test Command

Start the test using the `opus_ramtest` command. The following is a recommended command:

```bash
# The -s parameter sets a 40960-byte stack for each child process
opus_ramtest -s 40960
```

## IV. Command-Line Parameter Details

The `opus_ramtest` command supports several parameters to customize its behavior.

| Parameter | Description                                                                                                                                                                                                                           | Default Value  |
| :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------- |
| `-s`      | **(Required)** Sets the stack size (in bytes) for each created child process (thread). On embedded devices, `pthread` may use a small default stack, so you must use this parameter to allocate sufficient space to prevent overflow. | N/A            |
| `-n`      | Specifies the number of concurrent child processes for decoding tasks. **Note**: This value should not be set too high to avoid exhausting system resources.                                                                          | `5`            |
| `-r`      | Sets the scheduling priority for the child processes.                                                                                                                                                                                 | N/A            |
| `-f`      | Specifies the path to an external Opus audio file for decoding. If this parameter is not provided, the test will use its built-in audio data array.                                                                                   | Built-in array |

## V. Important Notes

- **Built-in Data Source Size:**

    - The test tool includes a built-in static array of approximately **250 KB**, which serves as the default audio data source. Ensure your target hardware has enough RAM to accommodate this array and the additional overhead from the test itself.

## VI. References

- **[Opus Official Website](https://opus-codec.org/)**: Get the latest information, specifications, and resources for the Opus codec.
- **[Opus IETF RFC 6716](https://www.rfc-editor.org/rfc/rfc6716)**: The authoritative technical standard for the Opus codec, published by the Internet Engineering Task Force (IETF).
