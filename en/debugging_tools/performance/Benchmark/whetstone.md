# A Guide to the Whetstone CPU Performance Benchmark

\[ English | [简体中文](./../../../../zh-cn/debugging_tools/performance/Benchmark/whetstone.md) \]

This document provides a detailed guide for developers and performance engineers on the openvela system to use the `whetstone` benchmark tool. `whetstone` is a classic comprehensive benchmark program designed to accurately evaluate a system's floating-point and integer arithmetic performance by executing a series of standardized computational tasks.

## I. Overview

`whetstone` is a command-line tool used to evaluate a processor's arithmetic performance. It derives a standardized performance score by executing a mixed set of computational tasks, including floating-point operations, integer operations, function calls, and array access.

The test results can help developers:

- Quantitatively evaluate the performance of the processor's Floating-Point Unit (FPU).
- Analyze the impact of different compiler optimization levels (`-O2`, `-O3`, etc.) on code execution efficiency.
- Compare arithmetic performance across different hardware platforms or system configurations.

## II. System Configuration

Before running the test, you must enable the following Kconfig options in your `defconfig` file to ensure the `whetstone` test suite and its dependencies are compiled correctly.

```Makefile
# Compile the Whetstone benchmark tool
CONFIG_BENCHMARK_WHETSTONE=y

# The core of the Whetstone test is floating-point arithmetic, so C library floating-point support must be enabled
CONFIG_LIBC_FLOATINGPOINT=y
```

## III. Usage

The `whetstone` tool is launched via a simple command-line interface and supports parameters to control the test load.

### 1. Command Syntax

```Bash
whetstone [-c <iterations>] [<loops>]
```

### 2. Parameter Description

| **Parameter**     | **Description**                                                                                                                                                                                                                      | **Required** | **Default Value** |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- | :---------------- |
| `[<loops>]`       | **Module Loop Count**. A positional argument that sets the number of execution loops for each internal test module. Increasing this value significantly increases the computational load and execution time of a single test module. | No           | 1000              |
| `-c <iterations>` | **Total Test Rounds**. An optional parameter that sets the number of times the entire `whetstone` test suite is repeated.                                                                                                            | No           | 1                 |

### 3. Execution Examples

1. Run a standard test: Uses default parameters, with each module looping 1,000 times and the entire test running for 1 round.

    ```Bash
    whetstone
    ```

2. Increase the computational load of each module: Each module loops 100,000 times, and the entire test runs for 1 round. This is suitable for scenarios requiring longer run times to obtain a stable average.

    ```Bash
    whetstone 100000
    ```

3. Repeat the test multiple times: Each module loops 100,000 times, and the entire test suite is repeated for 10 rounds.

    ```Bash
    whetstone 100000 -c 10
    ```

## IV. Interpreting the Results

After the test is complete, `whetstone` outputs the test configuration, total time elapsed, and the final performance score.

### 1. Example Output

```Bash
ap> whetstone 100000
Loops: 100000, Iterations: 1, Duration: 5 sec.
C Converted Double Precision Whetstones: 2.00 MWIPS
```

- `Loops: 100000`: Each module executed 100,000 loops.
- `Iterations: 1`: The entire test suite was executed for 1 round.
- `Duration: 5 sec`: Total execution time was 5 seconds.
- `C Converted Double Precision Whetstones: 2.00 MWIPS`: The final performance score is 2.00 MWIPS.

### 2. Key Metrics Explained

- **MWIPS / KWIPS**

    - **Meaning**: The performance units for `whetstone`, which stand for **MWIPS** (Mega Whetstone Instructions Per Second) and **KWIPS** (Kilo Whetstone Instructions Per Second).
    - **Calculation**: This value is calculated based on a fixed benchmark workload, the number of test loops (`loops` and `-c` parameters), and the total execution time. It is a standardized score; the higher the score, the stronger the processor's arithmetic performance.
    - **Unit Conversion**: When the score is below 1 MWIPS (i.e., 1000 KWIPS), the result is displayed in KWIPS.

## V. Test Module Details

The `whetstone` benchmark consists of 11 carefully designed computational modules that comprehensively cover different types of operations:

- Modules 1-4: Basic floating-point operations, array operations, and conditional judgments
- Module 5: Omitted integer arithmetic module
- Module 6: Complex integer arithmetic
- Module 7: Trigonometric function calculations (including inverse trigonometric functions)
- Module 8: Procedure call test
- Module 9: Array indexing test
- Module 10: Simple integer arithmetic
- Module 11: Chained mathematical function calls

## VI. openvela Porting Notes

This version of `whetstone` has been critically optimized for embedded real-time systems.

- **Optimized Timer Precision**: The original `whetstone` could only produce results when the test duration reached the second level. The version ported to openvela provides precise output even at the millisecond level. This allows for quick, stable, and accurate performance data even with fewer loop iterations on high-performance embedded CPUs.
