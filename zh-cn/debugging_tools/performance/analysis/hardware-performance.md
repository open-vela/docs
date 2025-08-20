# 评估硬件性能

\[ [English](./../../../../en/debugging_tools/performance/analysis/hardware-performance.md) | 简体中文 \]

在着手分析和优化软件性能之前，您必须首先评估硬件的性能基准。硬件规格定义了系统性能的上限（即“性能天花板”），确认硬件能力能否满足项目需求，是所有性能工作的起点。

## 一、核心硬件性能指标

评估硬件时，请重点考察以下核心指标。这些指标直接影响系统的计算、存储和图形处理能力。

### 计算核心 (Processing Core)

- **CPU 频率**：决定处理器的基本运算速度。
- **浮点运算单元 (FPU)**：评估其是否支持以及支持的浮点精度（单精度/双精度）。
- **DSP 指令集**：确认是否支持数字信号处理指令，这对音视频和通信等计算密集型任务至关重要。

### 内存与缓存 (Memory and Cache)

- **指令缓存 (I-Cache)、数据缓存 (D-Cache)、外部缓存**：缓存的大小和速度是影响 CPU 实际性能的关键因素。
- **RAM 频率**：影响内存子系统的整体数据吞吐率。
- **SRAM 带宽**：片上 SRAM 提供高速数据访问，其带宽对实时任务至关重要。
- **PSRAM 带宽**：PSRAM 作为外部 RAM 扩展，其带宽直接影响大数据量的处理效率。

### 存储 (Storage)

- **闪存 (Flash) 性能**：包括代码执行速度（Execute-in-Place）和数据读写吞吐率。
- **eMMC/SD 性能**：影响文件系统操作和数据存储速度。

### 多媒体与图形加速 (Multimedia & Graphics Acceleration)

- **2D 图形加速**：确认硬件是否支持 Bit Blit 或其他 2D 加速功能，对 UI 流畅度有显著影响。
- **图形处理单元 (GPU)**：评估 GPU 的 3D 渲染能力和并行计算性能。
- **硬件视频编解码**：确认是否集成硬件编解码器，以高效处理视频流。

## 二、使用基准测试工具量化性能

您可以使用行业标准的基准测试工具，来量化评估芯片的关键性能。

- **[Dhrystone]**：评估处理器在整数运算方面的性能，详情请参见[使用 Dhrystone 评估 CPU 整数性能](./../Benchmark/Dhrystone.md)。
- **[CoreMark]**：综合评估 CPU 核心的计算性能，是目前广泛使用的跨平台基准，详情请参见[执行 CoreMark 基准测试](./../Benchmark/coremark.md)。
- **[CacheSpeed]**：测试并量化缓存和内存子系统的读写速度，详情请参见 [CacheSpeed 测试工具指南](./../Benchmark/cachespeed.md)。
- **[RAMSpeed]**：专门用于评估 RAM 的数据吞吐量和访问延迟，详情请参见[ramspeed 内存性能测试指南](./../Benchmark/ramspeed.md)

## 三、关键分析与优化策略

基于硬件指标和测试数据，您可以采用以下策略进行深入分析和初步优化。

### 1、横向对比分析

将目标硬件的核心指标与同类产品或现有项目进行横向对比。这种方法可以帮助您快速识别当前硬件的性能长处与短板，为后续的性能优化指明方向。

### 2、优化浮点数运算

**注意**：部分微控制器（如基于 Arm Cortex-M4 内核的型号）的 FPU 仅原生支持单精度浮点运算。如果在这些平台上执行双精度运算，编译器会调用软件库进行模拟，导致性能急剧下降。

- **行动项**：务必查阅芯片手册，确认其 FPU 支持的浮点精度。在代码中，应优先使用硬件原生支持的浮点类型。
- **参考资料**：[Be Aware: Floating Point Operations on Arm Cortex-M4(F)](https://mcuoneclipse.com/2019/03/29/be-aware-floating-point-operations-on-arm-cortex-m4f/)

### 3、优化代码与数据布局

将执行频率高的“热点代码”和需要频繁访问的关键数据放置在访问速度更快的内存区域（如 SRAM），是嵌入式系统中一项非常有效的优化手段。

- **行动项**：分析程序的性能瓶颈后，您可以使用链接器脚本（Linker Script），将特定的函数或变量从慢速存储器（如 Flash）重定向到高速存储器（如 SRAM）中运行。
- **参考资料**：[Putting Code of Files into Special Section with the GNU Linker](https://mcuoneclipse.com/2014/10/06/putting-code-of-files-into-special-section-with-the-gnu-linker/)