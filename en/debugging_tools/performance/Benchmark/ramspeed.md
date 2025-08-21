# ramspeed Memory Performance Benchmarking Guide

\[ English | [简体中文](./../../../../zh-cn/debugging_tools/performance/Benchmark/ramspeed.md) \]

This document provides a comprehensive guide for developers and performance engineers on using the `ramspeed` benchmark tool in the `openvela` system. The tool accurately evaluates the performance of `memcpy` and `memset` functions by executing a series of standard memory operations under various loads.

## I. Overview

`ramspeed` is a command-line tool designed to assess memory performance. It measures memory read/write throughput for various block sizes by repeatedly executing `memcpy` (memory copy) and `memset` (memory fill) operations on a specified memory region.

The benchmark results help developers:

- Assess the real-world performance of memory operation functions in the system's C library (`libc`).
- Analyze the impact of various compiler optimization options on performance.
- Identify potential system-level performance bottlenecks.

To ensure accurate and reproducible results, please carefully read the configuration requirements and best practices in this document before testing.

## II. System Configuration

To obtain reliable benchmark data, you must properly configure the system to eliminate performance overhead caused by non-essential system activities and debugging features.

### 1. Kconfig Configuration

In your `defconfig` file, verify and apply the following settings. These options maximize code execution efficiency and disable debugging or monitoring features that could interfere with performance measurements.

```makefile
# Enable custom optimization flags
CONFIG_DEBUG_CUSTOMOPT=y
# Set compiler optimization level to -O3 for maximum performance
CONFIG_DEBUG_OPTLEVEL=-O3

# --- Disable the following performance-impacting options ---
# Disable scheduler instrumentation
CONFIG_SCHED_INSTRUMENTATION=n
# Disable interrupt monitor
CONFIG_SCHED_IRQMONITOR=n
# Disable critical section monitor
CONFIG_SCHED_CRITMONITOR=n
# Disable stack canaries. This has a significant performance impact,
# especially for short function calls, potentially causing up to a 3x difference!
CONFIG_STACK_CANARIES=n
# Disable the watchdog to prevent assertions during long tests
CONFIG_WATCHDOG=n

# --- Enable the ramspeed test suite ---
# Enable the ramspeed tool
CONFIG_BENCHMARK_RAMSPEED=y
# Enable floating-point support, required by ramspeed for rate calculation
CONFIG_LIBC_FLOATINGPOINT=y
```

## III. Usage

You can run the `ramspeed` tool from the command-line interface, using various arguments to control its behavior.

### 1. Command Syntax

```bash
nsh> ramspeed -h
RAM Speed: Missing required arguments

Usage: ramspeed -a -r <hex-address> -w <hex-address> -s <decimal-size> -v <hex-value>[0x00] -n <decimal-repeat number>[100] -i

Where:
  -a allocate RW buffers on heap. Overwrites -r and -w option.
  -r <hex-address> read address.
  -w <hex-address> write address.
  -s <decimal-size> number of memory locations (in bytes).
  -v <hex-value> value to fill in memory [default value: 0x00].
  -n <decimal-repeat num> number of repetitions [default value: 100].
  -i turn off interrupts while testing [default value: false].
```

### 2. Parameter Description

| **Argument**          | **Description**                                                                                                         | **Required**             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `-a`                  | **Allocate Memory Automatically**.<br>Allocates read/write buffers on the heap. This option overrides `-r` and `-w`.    | Choose `-a` or `-r`/`-w` |
| `-r <hex-address>`    | **Specify Read Address**.<br>Sets the source memory address for `memcpy`.                                               | No                       |
| `-w <hex-address>`    | **Specify Write Address**.<br>Sets the destination address for `memcpy` or the target address for `memset`.             | No                       |
| `-s <decimal-size>`   | **Set Maximum Test Size** (in bytes).<br>The test starts from 32 bytes and increases by powers of two up to this limit. | Yes                      |
| `-v <hex-value>`      | The hexadecimal value to fill memory with during the `memset` test. Defaults to `0x00`.                                 | No                       |
| `-n <decimal-repeat>` | The **number of repetitions** for each block size test.<br>Defaults to 100.                                             | No                       |
| `-i`                  | **Disable Interrupts**.<br>Enters a critical section during the test to prevent interrupt interference.                 | No                       |

**Operating Modes:**

- **`memcpy` Test**: Requires both read and write addresses. You can use `-a` for automatic allocation or specify them manually with `-r` and `-w`.
- **`memset` Test**: Requires only a write address. You can use `-a` for automatic allocation (the read buffer is ignored) or specify it manually with `-w`.

### 3. Example Command

The following command automatically allocates 512 KB (524288 bytes) of memory and repeats each block size test 10,000 times.

```bash
ramspeed -a -s 524288 -n 10000
```

## IV. Interpreting and Analyzing the Output

The test results present performance data for `memcpy` and `memset` separately.

![img](./figures/001.png)

### 1. Sample Output

```shell
vela> ramspeed -a -s 524288 -n 10000
RAM Speed: Allocate RW buffers on heap
RAM Speed: Write address: 0xed95d800
RAM Speed: Read address: 0xed57f800
RAM Speed: Size: 524288 bytes
RAM Speed: Value: 0x00
RAM Speed: Repeat number: 10000
RAM Speed: Interrupts disabled: false
______memcpy performance______
______Perform 32 Bytes access ______
RAM Speed: system memcpy():      Rate = 781250.000 KB/s [cost: 0.400 ms]
RAM Speed: internal memcpy():    Rate = 781250.000 KB/s [cost: 0.400 ms]
______Perform 64 Bytes access ______
RAM Speed: system memcpy():      Rate = 892857.143 KB/s [cost: 0.700 ms]
RAM Speed: internal memcpy():    Rate = 781250.000 KB/s [cost: 0.800 ms]
______Perform 128 Bytes access ______
RAM Speed: system memcpy():      Rate = 1041666.667 KB/s        [cost: 1.200 ms]
RAM Speed: internal memcpy():    Rate = 833333.333 KB/s [cost: 1.500 ms]
______Perform 256 Bytes access ______
...
```

### 2. Analysis of Results

The output log contains two key sets of performance metrics:

- **`system memxxx()`**

    - **Meaning**: Calls the `memcpy`/`memset` functions provided by the standard C library (`libc`). Its performance is directly affected by the compiler version, optimization flags, and `libc` implementation.
    - **Purpose**: Reflects the memory operation performance of the system in a real-world application context.

- **`internal memxxx()`**

    - **Meaning**: Calls a basic C-language implementation of `memcpy`/`memset` built into the `ramspeed` tool. This implementation serves as a performance baseline, designed to reduce loop overhead by processing more data per cycle (e.g., using 32-bit or 64-bit word-sized operations).
    - **Purpose**: Provides a stable and controlled performance reference.

**Performance Diagnostics:** Typically, the performance of `system memxxx()` should be close to or better than `internal memxxx()`. If you observe that the `system` performance is significantly lower than the `internal` one, investigate the following causes:

1. **Compiler Optimizations are Inactive**: Return to Section II and double-check that the optimization-related settings in `defconfig` are correctly enabled.
2. **Compiler-Specific Optimizations**: Newer GCC toolchains may apply vectorization optimizations (e.g., using the Arm MVE instruction set) to the C implementation of `memcpy`. This can lead to the `internal` implementation outperforming the `system` one in some tests, which is normal. You can confirm this by analyzing the disassembly.

## V. Best Practices

Follow these recommendations to obtain accurate and reproducible performance data:

- **Isolate the Test Environment**: Before running the benchmark, shut down all non-essential applications and background tasks. Ensure that only core system processes are running to minimize contention for the CPU and memory bus.
- **Mitigate Cache Effects**: Use a large memory test size (`-s` argument, 512 KB or larger is recommended). This reduces the impact of cache hits on small-block tests, providing a more realistic measurement of DDR/SRAM performance.
- **Increase the Sample Size**: Use a high number of repetitions (`-n` argument, 1000 or more is recommended). This helps to average out performance jitter from single runs and makes the statistical results more reliable.
- **Eliminate Interrupt Interference**: For latency-critical analysis, use the `-i` flag to disable interrupts during the test. This measures the pure CPU-to-Memory performance without external interference.

## VI. References

- **[How Memory Usage Patterns Can Derail Real-time Performance](https://interrupt.memfault.com/blog/memory-debugging)**: An in-depth article exploring how memory usage patterns can affect real-time performance.
