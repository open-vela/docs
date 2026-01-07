# 配置 TFLite Micro 开发环境

[ [English](../../en/edge_ai_dev/configure_tflite_micro_dev_env.md) | 简体中文 ]

在 openvela 平台上开发 TensorFlow Lite for Microcontrollers (TFLite Micro) 应用前，必须正确配置编译环境与依赖库。本节指导开发者完成源码确认、库依赖配置及内存策略制定。

## 一、先决条件

在开始之前，请确保已完成以下准备工作：

- **基础环境**：参考[官方文档](../quickstart/openvela_ubuntu_quick_start.md)，完成 openvela 基础开发环境的部署。
- **源码确认**：TFLite Micro 源码已集成至 openvela 代码仓库中，路径为：

    - `apps/mlearning/tflite-micro/`

## 二、组件与依赖库支持

TFLite Micro 依赖特定的数学库和工具库来实现模型解析与算子加速。openvela 仓库已预置以下关键组件：

| **组件名称**    | **功能描述**                                            | **源码路径**               |
| :-------------- | :------------------------------------------------------ | :------------------------- |
| **FlatBuffers** | TFLite 模型序列化格式支持库，提供必要的头文件。         | `apps/system/flatbuffers/` |
| **Gemmlowp**    | Google 提供的低精度通用矩阵乘法库，用于量化运算。       | `apps/math/gemmlowp/`      |
| **Ruy**         | TensorFlow 的高性能矩阵乘法后端，主要优化全连接层运算。 | `apps/math/ruy/`           |
| **KissFFT**     | 轻量级快速傅里叶变换库，支持定点与浮点运算。            | `apps/math/kissfft/`       |
| **CMSIS-NN**    | ARM Cortex-M 专用神经网络内核优化库（可选）。           | `apps/mlearning/cmsis-nn/` |

## 三、编译配置 (Kconfig)

通过 menuconfig 图形化界面启用必要的库支持，以确保编译通过并优化代码体积。

启动配置菜单

```Bash
cmake --build cmake_out/goldfish-arm64-v8a-ap -t menuconfig
```

请依次完成以下四个核心模块的配置：

### 1、启用 C++ 运行时支持

TFLite Micro 基于 C++11/14 标准编写，必须启用 LLVM libc++ 支持。

- **配置路径**：`Library Routines` -> `C++ Library`
- **操作**：选择 `LLVM libc++ C++ Standard Library`

```Plain
(Top) → Library Routines → C++ Library

( ) Toolchain C++ support
( ) Basic C++ support
(X) LLVM libc++ C++ Standard Library
```

### 2、启用数学加速库

根据模型需求启用矩阵运算与信号处理库。

- **配置路径**：`Application Configuration` -> `Math Library Support`
- **操作**：选中 `Gemmlowp`, `kissfft`, `Ruy`

```Plain
(Top) → Application Configuration → Math Library Support

[*] Gemmlowp
[*] kissfft
[ ] LibTomMath MPI Math Library
[*] Ruy
```

### 3、启用 FlatBuffers 支持

启用系统级 FlatBuffers 库以支持模型解析。

- **配置路径**：`Application Configuration` -> `System Libraries and NSH Add-Ons`
- **操作**：选中 `flatbuffers`

```Plain
(Top) → Application Configuration → System Libraries and NSH Add-Ons

[*] flatbuffers
```

### 4、启用 TFLite Micro 核心

- **配置路径**：`Application Configuration` -> `Machine Learning Support`
- **操作**：选中 `TFLiteMicro`。如需使用 ARM 硬件加速，建议同时选中 `CMSIS_NN Library`。

```Plain
(Top) → Application Configuration → Machine Learning Support

[ ] CMSIS_NN Library
[*] TFLiteMicro
[ ] Print tflite-micro's debug message
```

## 四、内存分配策略

嵌入式系统的内存资源有限，TFLite Micro 需要一块连续的内存区域（Tensor Arena）来存放输入/输出张量及中间计算结果。

### 1、静态分配（推荐）

对于生产环境，推荐使用静态数组分配。这种方式无内存碎片风险，且内存占用在编译期可知。

**实现示例**：

```C++
// 在应用代码全局区域定义
// 注意：内存必须按照 16 字节对齐，以满足 SIMD 指令要求
#define TENSOR_ARENA_SIZE (100 * 1024)
static uint8_t tensor_arena[TENSOR_ARENA_SIZE] __attribute__((aligned(16)));
```

### 2、确定 Arena 大小

为了精准设定 `TENSOR_ARENA_SIZE`，避免浪费或溢出，可以使用 `RecordingMicroInterpreter` 在运行时抓取实际内存用量。

**调试步骤**：

1. 引入记录器头文件。
2. 使用 `RecordingMicroInterpreter` 替换标准的 `MicroInterpreter`。
3. 运行一次模型推理（Invoke）。
4. 读取实际使用量并添加安全冗余（建议 +1KB）。

```C++
#include "tensorflow/lite/micro/recording_micro_interpreter.h"

// 1. 创建记录分配器
auto* allocator = tflite::RecordingMicroAllocator::Create(tensor_arena, arena_size);

// 2. 实例化记录解释器
tflite::RecordingMicroInterpreter interpreter(model, resolver, allocator);

// 3. 分配张量并执行推理
interpreter.AllocateTensors();
interpreter.Invoke();

// 4. 获取内存统计信息
size_t used = interpreter.arena_used_bytes();  // 实际占用
interpreter.GetMicroAllocator().PrintAllocations();  // 分项明细
size_t recommended = used + 1024;  // 至少额外预留 ~1KB 空间
```