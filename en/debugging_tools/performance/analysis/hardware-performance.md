# Evaluating Hardware Performance

\[ English | [简体中文](./../../../../zh-cn/debugging_tools/performance/analysis/hardware-performance.md) \]

Before analyzing and optimizing software performance, you must first establish a hardware performance baseline. Hardware specifications define the upper limit of system performance (i.e., the "performance ceiling"). Confirming that the hardware capabilities meet project requirements is the starting point for all performance-related work.

## I. Core Hardware Performance Metrics

When evaluating hardware, focus on the following core metrics. These directly impact the system's computing, storage, and graphics processing capabilities.

### Processing Core

- **CPU Frequency**: Determines the processor's fundamental operational speed.
- **Floating-Point Unit (FPU)**: Assess whether it is supported and the precision it handles (single-precision/double-precision).
- **DSP Instruction Set**: Verify support for Digital Signal Processing instructions, which is crucial for compute-intensive tasks like audio/video processing and communications.

### Memory and Cache

- **Instruction Cache (I-Cache)**, **Data Cache (D-Cache)**, **External Cache**: The size and speed of caches are key factors affecting actual CPU performance.
- **RAM Frequency**: Affects the overall data throughput of the memory subsystem.
- **SRAM Bandwidth**: On-chip SRAM provides high-speed data access, and its bandwidth is critical for real-time tasks.
- **PSRAM Bandwidth**: As an external RAM extension, PSRAM bandwidth directly impacts the efficiency of processing large amounts of data.

### Storage

- **Flash Memory Performance**: Includes code execution speed (Execute-in-Place) and data read/write throughput.
- **eMMC/SD Performance**: Affects file system operations and data storage speed.

### Multimedia & Graphics Acceleration

- **2D Graphics Acceleration**: Confirm if the hardware supports Bit Blit or other 2D acceleration features, which significantly impacts UI fluency.
- **Graphics Processing Unit (GPU)**: Evaluate the GPU's 3D rendering capabilities and parallel computing performance.
- **Hardware Video Codec**: Verify if a hardware codec is integrated for efficient video stream processing.

## II. Quantify Performance with Benchmarking Tools

You can use industry-standard benchmarking tools to quantify the key performance of the chip.

- **[Dhrystone]**: Evaluates processor performance for integer operations. For details, see [Using Dhrystone to Evaluate CPU Integer Performance](./../Benchmark/Dhrystone.md).
- **[CoreMark]**: Comprehensively evaluates the computational performance of the CPU core. It is a widely used cross-platform benchmark. For details, see [Executing the CoreMark Benchmark](./../Benchmark/coremark.md).
- **[CacheSpeed]**: Tests and quantifies the read/write speed of the cache and memory subsystem. For details, see [A Guide to the CacheSpeed Tool](./../Benchmark/cachespeed.md).
- **[RAMSpeed]**: Specifically used to evaluate RAM data throughput and access latency. For details, see [ramspeed Memory Performance Benchmarking Guide](./../Benchmark/ramspeed.md).

## III. Key Analysis and Optimization Strategies

Based on hardware metrics and test data, you can adopt the following strategies for in-depth analysis and initial optimization.

### 1. Comparative Analysis

Compare the core metrics of the target hardware against similar products or existing projects. This approach helps you quickly identify the performance strengths and weaknesses of the current hardware, providing direction for subsequent performance optimization.

### 2. Optimize Floating-Point Operations

**Note**: Some microcontrollers (e.g., those based on the Arm Cortex-M4 core) only have native support for single-precision floating-point operations. Performing double-precision calculations on these platforms will cause the compiler to fall back to a software library for emulation, leading to a sharp decline in performance.

- **Action Item**: Be sure to consult the chip's datasheet to confirm its FPU-supported precision. In your code, prioritize using the natively supported floating-point type.
- **Reference**: [Be Aware: Floating Point Operations on Arm Cortex-M4(F)](https://mcuoneclipse.com/2019/03/29/be-aware-floating-point-operations-on-arm-cortex-m4f/)

### 3. Optimize Code and Data Placement

Placing frequently executed "hot code" and frequently accessed critical data into faster memory regions (like SRAM) is a highly effective optimization technique in embedded systems.

- **Action Item**: After analyzing the program's performance bottlenecks, you can use a linker script to redirect specific functions or variables from slower memory (like Flash) to run in high-speed memory (like SRAM).
- **Reference**: [Putting Code of Files into Special Section with the GNU Linker](https://mcuoneclipse.com/2014/10/06/putting-code-of-files-into-special-section-with-the-gnu-linker/)
