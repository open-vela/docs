# fstest Filesystem Stress Testing Tool Guide

\[ English | [简体中文](./../../../zh-cn/debugging_tools/stress_testing/fstest.md) \]

## I. Overview

`fstest` is a command-line tool designed for stress testing filesystem performance and stability.

By simulating high-load file operations (such as concurrent creation, writing, reading, and deletion of files) on a specified mount point, it comprehensively tests the entire I/O stack, from the upper-level filesystem down to the drivers for underlying storage media (like eMMC, SD cards, and on-board flash). This tool is crucial for evaluating filesystem performance on a specific hardware platform, identifying I/O bottlenecks, and verifying the stability of storage drivers.

## II. Command Details

Run `fstest -h` in the openvela system shell to get the complete command-line options.

### 1. Command Syntax

```bash
fstest [OPTIONS]
```

### 2. Parameter Descriptions

| **Option** | **Argument** | **Description**                                                                                                                        | **Default** |
| :--------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------- | :---------- |
| `-h`       | N/A          | Displays this help message and exits.                                                                                                  | N/A         |
| `-n`       | `[count]`    | Specifies the number of test loops. Each loop executes a complete cycle of file creation, writing, reading, and deletion.              | 100         |
| `-m`       | `[path]`     | **(Required)** Specifies the target mount point (path) for the test. The tool will create and operate on test files in this directory. | N/A         |
| `-o`       | `[num]`      | Specifies the total number of files to create and operate on within a single test loop.                                                | 512         |
| `-s`       | `[size]`     | Specifies the size of each test file in bytes.                                                                                         | 8192        |

### 3. Raw Help Message

The following is the raw output of the `fstest -h` command in the terminal for your reference.

```bash
ap>fstest -h 

Usage:fstest [OPTION [ARG]] ...
-h show this help statement 
-n num of test loop e.g. [100] 
-m mount point to be tested e.g. [] 
-o num of open file e.g 
-s size of every file e.g 

Note: The product of the values for -o and -s must be less than the total size of the partition.
```

## III. Prerequisites

Before running the test, you must ensure that the target partition has enough free space to accommodate all test files. The total space required is determined by the **number of files** (`-o`) and the **size of each file** (`-s`), and must satisfy the following condition:

```text
(Number of files × Size per file) < Available space on the target partition
```

If there is insufficient space, the test will fail because it cannot create the files.

## IV. Execution and Examples

### 1. Test Command Examples

The following examples demonstrate how to run `fstest` on different mount points.

```Bash
# Run 100 test loops in the /tmp directory
fstest -n 100 -m /tmp

# Run 100 test loops in the /data directory
fstest -n 100 -m /data
```

### 2. Example Output

After the test runs, you will see output logs similar to the following. The log displays the test configuration and prints the time taken for each phase of file operations.

- Test output after running `fstest -n 100 -m /tmp`:

    ![img](./figures/001.png)

- Test output after running `fstest -n 100 -m /data`:

    ![img](./figures/002.png)

### 3. Interpreting the Results

The output log from `fstest` consists of two main parts: **performance data** and a **memory usage report**.

#### Memory Usage Report

The `Final memory usage` table at the end of the log is key for diagnosing memory leaks. It shows the changes in the openvela kernel memory heap before and after the test run.

- **`BEFORE` / `AFTER`**: Represent the snapshot values of a memory metric before the test task starts and after it ends, respectively.
- **`DELTA`**: The difference between `AFTER` and `BEFORE`. **For a healthy system, the `DELTA` value should be `0`**, indicating that all memory dynamically allocated during the test was correctly freed upon completion.
- **Key Metric Descriptions**:

    - `arena`: Total heap size.
    - `ordblks`: Number of free memory blocks (Free Chunks).
    - `uordblks`: Total size of allocated memory blocks (Allocated Chunks).
    - `fordblks`: Total size of free memory blocks.

If a non-zero value appears in the `DELTA` column, it usually indicates a memory leak. For example, in the first sample output, `ordblks` (free blocks) increased by 3, while `uordblks` (used space) increased by 1080 bytes. This suggests that the test run on the `/tmp` path may have triggered memory allocations that were not properly released.

#### Performance Data

Lines in the log that start with `[TMR]` show the performance data for each file operation phase.

- **Success Indicator**: When all test loops complete without errors, the log will print `fstest success!` at the end.
- **Performance Metrics**: Entries like `create file`, `write file`, `read file`, and `remove file` correspond to the file creation, writing, reading, and deletion phases, respectively. The subsequent time value indicates the total time consumed to complete all operations in that phase (the unit is typically milliseconds or system clock ticks, depending on the platform implementation). By analyzing this timing data, you can evaluate the filesystem's performance under various I/O patterns.
