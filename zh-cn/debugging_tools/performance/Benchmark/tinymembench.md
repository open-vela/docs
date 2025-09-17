# 使用 Tinymembench 分析内存性能

\[ [English](./../../../../en/debugging_tools/performance/Benchmark/tinymembench.md) | 简体中文 \]

## 一、概述

`tinymembench` 是一款轻量级的跨平台基准测试工具，您可以使用它来精确测量系统的内存带宽和随机存取延迟。此工具为分析和优化嵌入式系统的内存子系统性能提供了关键数据。

`tinymembench` 的主要特性包括：

- **官方源码**：https://github.com/ssvb/tinymembench

- **支持的处理器架构**：

    - AArch64
    - ARM
    - amd64
    - MIPS32

- **支持的向量指令集**：

    - SSE2 (Streaming SIMD Extensions 2)
    - NEON

## 二、使用说明

您可以通过简单的配置和命令，在 openvela 环境中启用并运行 `tinymembench`。

### 1、启用 tinymembench

在您的项目配置中，启用 `tinymembench` 应用程序。

1. 进入 openvela 的配置菜单（例如，执行 `make menuconfig`）。

2. 导航至 `Application Configuration` -> `BenchMarks`。

3. 选中 `tinymembench` 选项。

    ```Makefile
    CONFIG_BENCHMARKS_TINYMEMBENCH=y
    ```

4. 保存配置并重新编译您的项目。

`tinymembench` 的源代码位于 `apps/benchmarks/tinymembench` 目录下。

### 2、运行基准测试

在命令行（NuttShell）中，直接执行 `tinymembench` 命令即可启动测试。该命令无需任何参数。

```Bash
nsh> tinymembench
```

## 三、分析测试结果

`tinymembench` 的输出分为两个主要部分：内存带宽测试和内存延迟测试。

### 1、解读核心指标

性能评估的基本原则非常简单：

- **内存带宽越高越好**：表示单位时间内可以传输更多数据。
- **内存延迟越低越好**：表示单次内存访问所需时间更短。

### 2、示例输出

测试完成后，`tinymembench` 会打印详细的性能报告，如下所示：

```Bash
nsh> tinymembench
tinymembench v0.4.9 (simple benchmark for memory throughput and latency)

==========================================================================
== Memory bandwidth tests                                               ==
... (此处省略了带宽测试的详细输出) ...
 C copy                                               :   7153.3 MB/s (3.7%)
 standard memcpy                                      :  13278.0 MB/s (7.2%)
 standard memset                                      :   5833.2 MB/s (1.0%)
 SSE2 copy                                            :  12823.8 MB/s (6.8%)

==========================================================================
== Memory latency test                                                  ==
... (此处省略了延迟测试的详细输出) ...
==========================================================================

block size : single random read / dual random read
      1024 :    0.1 ns          /     0.1 ns
...
  16777216 :   66.7 ns          /    84.9 ns
  33554432 :   73.6 ns          /    99.8 ns
  67108864 :   69.4 ns          /    94.7 ns
```

### 3、影响内存性能的关键因素

内存性能受到多种硬件和软件配置的共同影响。在分析结果时，请重点考虑以下因素：

- **数据缓存 (Data Cache)**：启用数据缓存可以显著降低平均访存延迟，从而提升整体性能。
- **内存管理单元 (MMU)**：启用 MMU 会引入虚拟地址到物理地址的转换开销，增加平均访存时间和最坏情况访存时间。在多级页表（如 4 级页表）的配置下，最坏情况下的访存延迟会显著增加。相比之下，使用内存保护单元 (MPU) 进行块式地址转换对性能的影响较小。
- **转译后备缓冲器 (TLB)**：TLB (Translation Lookaside Buffer) 是 MMU 的地址转换缓存。启用 TLB 可以有效加速地址转换过程，降低开启 MMU 时的平均访存延迟。
- **页表项的缓存属性 (Cacheable Attribute)**：如果将内存区域配置为非缓存 (Non-Cacheable)，CPU 将绕过缓存直接访问主存。这会增加平均访存时间，但可能略微降低最坏情况下的访存延迟抖动。
- **虚拟化环境**：在虚拟化环境中运行通常会引入额外的地址转换层（例如，中间物理地址到主机物理地址），这会轻微增加平均访存时间，并可能显著增加最坏情况下的访存时间。
- **DDR 内存时序**：DDR (Double Data Rate) SDRAM 的物理特性直接影响性能。

    - **刷新周期**：内存刷新期间（由 `t_REF`, `t_REFI` 等参数定义），内存控制器会暂停响应访存请求，直接影响最坏情况下的访存时间。
    - **访问时序**：其他关键时序参数，如 `t_CL` (CAS Latency) 和 `t_RCD` (RAS to CAS Delay)，同样会影响平均和最坏情况下的访存时间。

## 四、openvela 移植说明

在将 `tinymembench` 移植到 `openvela` 的过程中，进行了一项关键修改：

- 为 `fmin` 函数增加了 `attribute((weak))` 修饰，以解决其与标准库中同名函数可能发生的符号冲突问题。
