# Conducting Memory Stress Tests with memstress

[ English | [简体中文](./../../../zh-cn/debugging_tools/stress_testing/memstress.md) ]

## I. Overview

`memstress` is a test tool designed to verify the stability and correctness of a system's memory manager, making it particularly suitable for use during development and debugging phases.

When run in debug mode, the tool outputs detailed logs for each memory allocation and deallocation, which helps in tracking down memory-related issues.

## II. How It Works

The `memstress` tool stress-tests the system by randomly performing the following three types of memory operations:

1. **Standard `malloc`**: Allocates memory using `malloc()`.
2. **Aligned allocation**: Allocates aligned memory using `aligned_alloc()`.
3. **Reallocation**: Resizes existing memory blocks using `realloc()`.

The tool fills the allocated memory with random data (or a fixed pattern in debug mode) and subsequently verifies the data's integrity to detect memory corruption or other read/write errors.

If a memory error is detected, the tool prints detailed error information and triggers an assertion to help pinpoint the issue.

## III. How to Use memstress

### Step 1: Enable the Tool at Compile Time

Enable the following Kconfig options in your `defconfig` file.

```makefile
# Enable the memstress tool
CONFIG_TESTING_MEMORY_STRESS=y

# Set the program name
CONFIG_TESTING_MEMORY_STRESS_PROGNAME

# Set the task priority
CONFIG_TESTING_MEMORY_STRESS_PRIORITY

# Set the stack size
CONFIG_TESTING_MEMORY_STRESS_STACKSIZE
```

### Step 2: Run the Test Command

Execute the `memstress` command from the system shell.

#### Command Syntax

```bash
memstress -m <max-allocsize> -n <node-length> -t <sleep-us> [-x <nthreads>] [-d]
```

#### Parameters

| Parameter            | Description                                                                           |
| :------------------- | :------------------------------------------------------------------------------------ |
| `-m <max-allocsize>` | Sets the maximum size for a single memory allocation, in bytes. Default: `8192`.      |
| `-n <node-length>`   | Sets the number of memory blocks (nodes) to manage in the test list. Default: `1024`. |
| `-t <sleep-us>`      | Sets the sleep interval between operations, in microseconds. Default: `100`.          |
| `-x <nthreads>`      | Enables multi-threaded testing and sets the number of threads. Default: `1`.          |
| `-d`                 | Enables debug mode, which outputs verbose logs to help locate issues.                 |

#### Examples

```bash
# Basic usage with default parameters
memstress

# Set max allocation to 4 KB, 1000 blocks, and 4 threads
memstress -m 4096 -n 1000 -x 4

# Run a test with debug mode enabled
memstress -d -m 2048 -n 500
```

## IV. Important: Estimating Memory Consumption

The maximum potential memory consumption of the `memstress` tool is determined by the following factors:

1. **Node array per thread**: Each thread creates an array to manage `<node-length>` memory allocations.
2. **Maximum allocation per node**: Each node in the array can hold one memory block, with a random size up to `<max-allocsize>`.
3. **Multi-threaded execution**: The tool supports `<nthreads>` running concurrently, each with its own set of nodes.

`memstress` runs continuously until an error is detected. Before execution, you **must** estimate the maximum potential memory consumption using the formula below to ensure the system has sufficient available memory.

**Maximum Memory Consumption ≈ `<max-allocsize>` × `<node-length>` × `<nthreads>`**

Please note that this is a theoretical peak value. The actual memory usage will fluctuate due to the random allocation and deallocation of memory blocks. It is recommended to start with smaller parameters and gradually increase the test load.
