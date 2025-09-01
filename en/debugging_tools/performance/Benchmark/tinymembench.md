# Analyzing Memory Performance with Tinymembench

\[ English | [简体中文](./../../../../zh-cn/debugging_tools/performance/Benchmark/tinymembench.md) \]

## I. Overview

`tinymembench` is a lightweight, cross-platform benchmarking tool that you can use to precisely measure your system's memory bandwidth and random-access latency. This tool provides critical data for analyzing and optimizing the performance of an embedded system's memory subsystem.

The main features of `tinymembench` include:

- **Official Source Code**: https://github.com/ssvb/tinymembench

- **Supported Processor Architectures**:

    - AArch64
    - ARM
    - amd64
    - MIPS32

- **Supported Vector Instruction Sets**:

    - SSE2 (Streaming SIMD Extensions 2)
    - NEON

## II. Usage Instructions

You can enable and run `tinymembench` in the openvela environment with simple configuration and commands.

### 1. Enabling `tinymembench`

Enable the `tinymembench` application in your project's configuration.

1. Enter the openvela configuration menu (e.g., by running `make menuconfig`).

2. Navigate to `Application Configuration` -> `BenchMarks`.

3. Select the `tinymembench` option.

    ```Makefile
    CONFIG_BENCHMARKS_TINYMEMBENCH=y
    ```

4. Save the configuration and recompile your project.

The source code for `tinymembench` is located in the `apps/benchmarks/tinymembench` directory.

### 2. Running the Benchmark

In the command line (NuttShell), simply execute the `tinymembench` command to start the test. The command requires no arguments.

```Bash
nsh> tinymembench
```

## III. Analyzing Test Results

The output of `tinymembench` is divided into two main parts: memory bandwidth tests and memory latency tests.

### 1. Interpreting Core Metrics

The basic principles for performance evaluation are straightforward:

- **Higher memory bandwidth is better**: It indicates that more data can be transferred per unit of time.
- **Lower memory latency is better**: It indicates that a single memory access takes less time.

### 2. Example Output

After the test is complete, `tinymembench` will print a detailed performance report, as shown below:

```Bash
nsh> tinymembench
tinymembench v0.4.9 (simple benchmark for memory throughput and latency)

==========================================================================
== Memory bandwidth tests                                               ==
... (Detailed output for bandwidth tests omitted) ...
 C copy                                               :   7153.3 MB/s (3.7%)
 standard memcpy                                      :  13278.0 MB/s (7.2%)
 standard memset                                      :   5833.2 MB/s (1.0%)
 SSE2 copy                                            :  12823.8 MB/s (6.8%)

==========================================================================
== Memory latency test                                                  ==
... (Detailed output for latency tests omitted) ...
==========================================================================

block size : single random read / dual random read
      1024 :    0.1 ns          /     0.1 ns
...
  16777216 :   66.7 ns          /    84.9 ns
  33554432 :   73.6 ns          /    99.8 ns
  67108864 :   69.4 ns          /    94.7 ns
```

### 3. Key Factors Affecting Memory Performance

Memory performance is influenced by a combination of hardware and software configurations. When analyzing the results, consider the following key factors:

- **Data Cache**: Enabling the data cache can significantly reduce average memory access latency, thereby improving overall performance.
- **Memory Management Unit (MMU)**: Enabling the MMU introduces overhead for virtual-to-physical address translation, increasing both average and worst-case memory access times. With multi-level page tables (e.g., 4-level tables), the worst-case memory access latency can increase significantly. In contrast, using a Memory Protection Unit (MPU) for block-based address translation has a smaller impact on performance.
- **Translation Lookaside Buffer (TLB)**: The TLB is the MMU's address translation cache. Enabling the TLB can effectively accelerate the address translation process, reducing the average memory access latency when the MMU is active.
- **Cacheable Attribute of Page Table Entries**: If a memory region is configured as Non-Cacheable, the CPU bypasses the cache and accesses main memory directly. This increases the average access time but may slightly reduce worst-case latency jitter.
- **Virtualization Environment**: Running in a virtualized environment typically introduces an additional layer of address translation (e.g., Intermediate Physical Address to Host Physical Address), which slightly increases average access time and can significantly increase worst-case access time.
- **DDR Memory Timings**: The physical characteristics of DDR (Double Data Rate) SDRAM directly impact performance.

    - **Refresh Cycle**: During a memory refresh period (defined by parameters like `t_REF` and `t_REFI`), the memory controller pauses responses to access requests, which directly affects the worst-case access time.
    - **Access Timings**: Other key timing parameters, such as `t_CL` (CAS Latency) and `t_RCD` (RAS to CAS Delay), also affect average and worst-case access times.

## IV. openvela Porting Notes

During the process of porting `tinymembench` to `openvela`, a key modification was made:

- The `__attribute__((weak))` modifier was added to the `fmin` function to resolve potential symbol conflicts with a function of the same name in the standard library.
