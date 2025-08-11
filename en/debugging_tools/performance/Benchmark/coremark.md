# Executing the CoreMark Benchmark

\[ English | [简体中文](./../../../../zh-cn/debugging_tools/performance/Benchmark/coremark.md) \]

## I. Overview

CoreMark is an industry-standard benchmark designed specifically to measure the performance of a central processing unit (CPU) in embedded systems. It was developed in 2009 by Shay Gal-on of the EEMBC (Embedded Microprocessor Benchmark Consortium) to provide a more realistic and comprehensive performance evaluation standard than Dhrystone.

The benchmark is written entirely in C, and its workload primarily simulates common operations that a CPU performs in real-world applications. It includes the following core algorithms:

- **List Processing:** Involves finding, sorting, inserting, and deleting items in a linked list.
- **Matrix Manipulation:** Performs common operations such as matrix multiplication.
- **State Machine:** Processes an input data stream through state transitions.
- **Cyclic Redundancy Check (CRC):** Calculates a checksum on the data to verify the correctness of the results from the preceding algorithms.

## II. Enabling the Feature

You can enable the CoreMark feature by setting the following Kconfig option:

```Makefile
CONFIG_BENCHMARK_COREMARK=y
```

## III. Executing the Test

CoreMark can be used to evaluate the core performance of both single-core and multi-core processors. After enabling the feature and compiling the firmware, you can run the test directly in the openvela shell.

```Bash
ap> coremark
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 207740
Total time (secs): 20.774000
Iterations/Sec   : 529.508039
Iterations       : 11000
Compiler version : GCC11.3.1 20220712
Compiler flags   : -Wstrict-prototypes -nostdlib -pipe -O3 -fno-strict-aliasing -fomit-frame-pointer -mthumb -Wa,-mthumb -Wa,-mimplicit-it=always -fno-common -Wall -Wshadow -x
Memory location  : Please put data memory location here
                        (e.g. code in flash, data on heap, etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 529.508039 / GCC11.3.1 20220712 -Wstrict-prototypes -nostdlib -pipe -O3 -fno-strict-aliasing -fomit-frame-pointer -mthumb -Wa,-mthumb -Wa,-mimplicit-it=always p
```

## IV. Interpreting the Results

After the command is executed, it outputs detailed performance data and validation information. The table below explains the key output parameters:After the command is executed, it outputs detailed performance data and validation information. The table below explains the key output parameters:

| **Parameter**        | **Description**                                                                                                                | **Example Value**                 |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------- | :-------------------------------- |
| `Run Type`           | The run type and parameters for the test.                                                                                      | `2K performance run...`           |
| `CoreMark Size`      | The size of the data buffer used for the test.                                                                                 | `666`                             |
| `Total ticks`        | The total number of system clock ticks consumed to complete all iterations.                                                    | `207740`                          |
| `Total time (secs)`  | The total time taken to complete the test, in seconds.                                                                         | `20.774000`                       |
| **`Iterations/Sec`** | **The core performance score. This value is the key metric for CPU performance; a higher value indicates better performance.** | **`529.508039`**                  |
| `Iterations`         | The total number of iterations performed during the test.                                                                      | `11000`                           |
| `Compiler version`   | The version of the compiler used to build the test code.                                                                       | `GCC11.3.1 20220712`              |
| `Compiler flags`     | The flags used during compilation and linking, which can significantly impact the final performance score.                     | `-O3 -fno-strict-aliasing...`     |
| `seedcrc`            | The initial seed value used for the three sets of CRC calculations.                                                            | `0xe9f5`                          |
| `[0]crclist`         | The CRC checksum for the list processing algorithm, used to validate the correctness of the results.                           | `0xe714`                          |
| `[0]crcmatrix`       | The CRC checksum for the matrix manipulation algorithm.                                                                        | `0x1fd7`                          |
| `[0]crcstate`        | The CRC checksum for the state machine algorithm.                                                                              | `0x8e3a`                          |
| `[0]crcfinal`        | The final combined CRC checksum after three iterations, used to ensure the validity of the test.                               | `0x33ff`                          |
| `Final Score`        | A compact summary of the final score, appended with environmental information such as the compiler version and flags.          | `CoreMark 1.0 : 529.508039 / ...` |

## V. References

- [Official CoreMark Website (EEMBC)](https://www.eembc.org/coremark/)
- [CoreMark GitHub Repository](https://github.com/eembc/coremark)