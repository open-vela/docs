# Using Dhrystone to Evaluate CPU Integer Performance

\[ English | [简体中文](./../../../../zh-cn/debugging_tools/performance/Benchmark/Dhrystone.md) \]

## I. Overview

Dhrystone is an industry-standard benchmark program specifically designed to evaluate a processor's integer and logical operation performance. It simulates typical program behavior by executing a predefined series of computationally intensive operations that do not involve floating-point calculations.

The test results are typically measured using two key metrics:

- **Dhrystones per Second**: Represents the number of times the processor can complete the main Dhrystone loop in one second. A higher value indicates better performance.
- **DMIPS (Dhrystone Million Instructions Per Second)**: A standardized performance metric derived by comparing the **Dhrystones per Second** value against a baseline (the performance of a VAX 11/780 computer). It provides a relative performance reference across different platforms and architectures.

## II. Enabling Dhrystone

To use the Dhrystone benchmark tool, you must set the following Kconfig option in your openvela board-level configuration file.

```Makefile
# Enable the Dhrystone benchmark
CONFIG_BENCHMARK_DHRYSTONE=y
```

## III. Executing the Test

After configuring and compiling the firmware, you can run the test in the openvela NSH (NuttShell) terminal.

### Command

In the terminal, execute the following command to start the test:

```Bash
dhrystone
```

### Sample Output

The program first attempts a small number of runs. If the execution time is too short, it automatically increases the number of runs to obtain a more accurate measurement. After the test completes, it prints the final performance data.

```Bash
nsh> dhrystone

Dhrystone Benchmark, Version C, Version 2.2
Program compiled without 'register' attribute
Using MSC clock(), HZ=100

Trying 50000 runs through Dhrystone:
Measured time too small to obtain meaningful results

Trying 500000 runs through Dhrystone:
Final values of the variables used in the benchmark:

Int_Glob:            5
        should be:   5
Bool_Glob:           1
        should be:   1
... (Detailed intermediate variable verification output omitted) ...
Str_2_Loc:           DHRYSTONE PROGRAM, 2'ND STRING
        should be:   DHRYSTONE PROGRAM, 2'ND STRING

Microseconds for one run through Dhrystone:        8.5 
Dhrystones per Second:                          117647 
```

## IV. Interpreting the Results

After the test is complete, the program outputs detailed verification data and two key performance metrics.

### Key Performance Metrics

| **Metric**                                   | **Description**                                                                              |
| :------------------------------------------- | :------------------------------------------------------------------------------------------- |
| `Microseconds for one run through Dhrystone` | The average time required to execute one main Dhrystone loop, measured in microseconds (µs). |
| `Dhrystones per Second`                      | The number of main Dhrystone loops the processor can execute per second.                     |

### Calculating DMIPS

DMIPS is a more valuable standardized metric. It compares the test results with the performance of a VAX 11/780 computer (defined as 1 MIPS), which has a Dhrystone score of **1757** Dhrystones/sec.

You can use the following formula to convert the test result to DMIPS:

**DMIPS = Dhrystones per Second / 1757**

Based on the sample output above:

- **Dhrystones per Second** = 117647
- **DMIPS** = 117647 / 1757 ≈ **66.96**

#### Normalized Performance (DMIPS/MHz)

To make a fair comparison between processors with different clock frequencies, **DMIPS/MHz** is often used as a normalized metric.

**DMIPS/MHz = DMIPS / Processor Clock Frequency (MHz)**

For example, if the processor runs at 100 MHz, its normalized performance is:

- **DMIPS/MHz** = 66.96 / 100 ≈ **0.67**
