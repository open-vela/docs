# 使用 Dhrystone 评估 CPU 整数性能

\[ [English](./../../../../en/debugging_tools/performance/Benchmark/Dhrystone.md) | 简体中文 \]

## 一、概述

Dhrystone 是一个行业标准的基准测试程序，专门用于评估处理器的整数和逻辑运算性能。它通过执行一系列预定义的、不含浮点运算的计算密集型操作来模拟典型的程序行为。

测试结果通常以两个关键指标来衡量：

- **每秒 Dhrystone 数 (Dhrystones per Second)**：表示处理器在一秒内可以完整执行 Dhrystone 主循环的次数。这个值越高，表明性能越强。
- **DMIPS** **(Dhrystone Million Instructions Per Second)**：一个标准化的性能指标，通过将**每秒 Dhrystone 数**与一个基准值（VAX 11/780 计算机的性能）进行比较得出。它提供了一个跨平台、跨架构的相对性能参考。

## 二、启用 Dhrystone

要使用 Dhrystone 基准测试工具，您必须在 openvela 的板级配置文件中设置以下 Kconfig 选项。

```Makefile
# 启用 Dhrystone 基准测试
CONFIG_BENCHMARK_DHRYSTONE=y
```

## 三、执行测试

配置并编译固件后，您可以在 openvela 的 NSH (NuttShell) 终端中运行测试。

### 命令

在终端中，直接执行以下命令启动测试：

```Bash
dhrystone
```

### 示例输出

程序会首先尝试一个较小的运行次数，如果执行时间过短，它会自动增加运行次数以获得更精确的测量结果。测试完成后，会打印最终的性能数据。

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
... (中间详细的变量验证输出已省略) ...
Str_2_Loc:           DHRYSTONE PROGRAM, 2'ND STRING
        should be:   DHRYSTONE PROGRAM, 2'ND STRING

Microseconds for one run through Dhrystone:        8.5 
Dhrystones per Second:                          117647 
```

## 四、解读测试结果

测试完成后，程序会输出详细的验证数据和两个关键的性能指标。

### 关键性能指标

| **指标 (Metric)**                            | **说明**                                                   |
| :------------------------------------------- | :--------------------------------------------------------- |
| `Microseconds for one run through Dhrystone` | 执行一次 Dhrystone 主循环所需的平均时间，单位为微秒 (µs)。 |
| `Dhrystones per Second`                      | 处理器每秒可以执行的 Dhrystone 主循环次数。                |

### 计算 DMIPS

DMIPS 是一个更具参考价值的标准化指标。它将测试结果与 VAX 11/780 计算机的性能（定义为 1 MIPS）进行比较，该计算机的 Dhrystone 得分为 **1757** Dhrystones/sec。

您可以使用以下公式将测试结果转换为 DMIPS：

**DMIPS = Dhrystones per Second / 1757**

根据上文的示例输出：

- **Dhrystones per Second** = 117647
- **DMIPS** = 117647 / 1757 ≈ **66.96**

#### 归一化性能 (DMIPS/MHz)

为了在不同主频的处理器之间进行公平比较，通常会使用 **DMIPS/MHz** 作为归一化指标。

**DMIPS/MHz = DMIPS / 处理器主频 (MHz)**

例如，如果处理器运行在 100 MHz，其归一化性能为：

- **DMIPS/MHz** = 66.96 / 100 ≈ **0.67**
