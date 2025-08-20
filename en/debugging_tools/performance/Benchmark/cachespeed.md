# A Guide to the CacheSpeed Tool

\[ English | [简体中文](./../../../../zh-cn/debugging_tools/performance/Benchmark/cachespeed.md) \]

## I. Overview

`cachespeed` is a command-line benchmark tool designed to precisely measure the performance of cache operations in the openvela system. It quantifies the execution time of `invalidate`, `flush`, and `clean` operations on the Instruction Cache (I-Cache) and Data Cache (D-Cache). To provide comprehensive performance data, the tool covers both memory-aligned and unaligned test scenarios.

### Technical Terminology Explained

- **`clean` (Write back)**: Writes modified ("dirty") data from the cache back to main memory, but the data remains in the cache.
- **`invalidate`**: Marks data in the cache as invalid without writing it back to main memory. The next time this data is accessed, the CPU is forced to reload it from main memory.
- **`flush`**: Typically a combination of `clean` and `invalidate`. It first writes dirty data back to main memory and then invalidates the corresponding cache line.

### Target Audience

This document is intended for developers who need to perform performance analysis and optimization on the openvela Real-Time Operating System (RTOS), including:

- **System Performance Engineers**: Responsible for evaluating and tuning overall system performance.
- **Embedded Kernel Developers**: Responsible for developing or maintaining low-level code related to memory management and processor architecture.
- **Board Support Package (BSP) Engineers**: Responsible for porting openvela to new hardware platforms and verifying its performance.

## II. Prerequisites

The tool relies on the `up_perf_gettime()` function for high-precision timing. Before running the test, you must ensure that the system's performance counter is correctly configured.

For platforms based on the ARMv8-M architecture, you need to enable the Cycle Counter by setting the following registers. Typically, you can execute these commands in a debugger or a system startup script.

```Plain
// Example: Please verify based on your target chip's specifications.
mw 0xe000edfc=0x01100000
mw 0xe0001000=0x48000001
```

## III. Build Configuration

To ensure the accuracy of the benchmark results, apply the following settings in your build configuration file. These configurations minimize system overhead that could interfere with the test.

```Makefile
# --- Performance & Optimization ---
DEBUG_CUSTOMOPT=y          # Enable custom optimization options
DEBUG_OPTLEVEL=-O3         # Set compiler optimization level to -O3 to ensure code runs with maximum efficiency

# --- Disable Monitoring & Security Checks ---
CONFIG_SCHED_INSTRUMENTATION=n # Disable scheduler instrumentation
CONFIG_SCHED_IRQMONITOR=n      # Disable interrupt monitoring
CONFIG_SCHED_CRITMONITOR=n     # Disable critical section monitoring
CONFIG_STACK_CANARIES=n        # Disable stack canaries. This option has a significant impact on performance, 
                               # especially in short function call scenarios, potentially causing a performance gap of up to 3x.
CONFIG_WATCHDOG=n              # Disable the watchdog to prevent system resets during long tests

# --- Enable Test Tool ---
CONFIG_BENCHMARK_CACHESPEED=y  # Compile the cachespeed tool
```

## IV. Running the Test

The source code for this tool is located in the `apps/benchmarks/cachespeed` directory. Execute the `cachespeed` command in the system shell to run the test.

### Example Output

```Bash
cachespeed
CACHE Speed: address src: 38506ec0
** dcache invalidate [rate, avg, cost] in nanoseconds(bytes/nesc) align **
64 Bytes: 0.045714, 1400, 14000
128 Bytes: 0.116364, 1100, 11000
192 Bytes: 0.128000, 1500, 15000
256 Bytes: 0.182857, 1400, 14000
320 Bytes: 0.213333, 1500, 15000
384 Bytes: 0.256000, 1500, 15000
448 Bytes: 0.320000, 1400, 14000
...
```

## V. Interpreting the Results

The test process typically starts with a single cache line size and progressively increases the data block size until it approaches or exceeds the cache capacity. **Focus on the `avg` value during analysis**; `rate` and `cost` provide supplementary perspectives but can be easily influenced by sample size and measurement methods.

The meaning of each column in the output is as follows:

| **Metric** | **Unit**         | **Description**                                                                |
| :--------- | :--------------- | :----------------------------------------------------------------------------- |
| `rate`     | bytes/nanosecond | The processing rate, calculated as `(test data size) / avg`.                   |
| `avg`      | nanoseconds      | **(Key Metric)** The average time taken to perform a single cache operation.   |
| `cost`     | nanoseconds      | The total time taken to complete all test iterations for a specific data size. |

## VI. How It Works

Understanding the underlying mechanisms of cache operations will help you correctly interpret the performance data.

### 1. Invalidate

- **Observation**: The `invalidate` operation's rate (`rate`) typically increases as the test data size grows.
- **Reasoning**: The core overhead of an `invalidate` operation (e.g., the CPU finding the cache tag and marking it as invalid) is relatively fixed and has little to do with the size of the data block being invalidated. When this relatively fixed time (`avg`) is used to process a larger data block (`size`), the calculated average rate (`rate = size / avg`) naturally increases.

### 2. Clean & Flush

- **Observation**: When the size of the test data exceeds the total capacity of the physical D-Cache, the average time (`avg`) for `clean` and `flush` operations tends to stabilize.
- **Reasoning**: `clean` and `flush` operations need to write dirty (modified) data from the cache back to main memory. Once the test data is too large to fit entirely in the cache, the performance bottleneck shifts from the cache's internal execution speed to the much slower **memory bus bandwidth**. Since the bus bandwidth is fixed, the rate at which the system writes data back to main memory becomes constant. Consequently, the average time per operation (`avg`) no longer changes significantly with increasing data size.

Conclusion: When analyzing the `cachespeed` output, focus on `avg` and perform root cause analysis by considering the target platform's cache size, cache line size, and memory bandwidth.

## VII. Further Reading

- [ARM Architecture Reference Manual (ARMv8-M)](https://developer.arm.com/documentation/ddi0553/latest/)
    - Consult this manual to find authoritative technical specifications for low-level hardware modules such as the Data Watchpoint and Trace unit (DWT) and cache controllers.
