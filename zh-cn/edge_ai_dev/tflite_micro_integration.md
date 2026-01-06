# TFLite Micro 架构解析与集成

[ [English](../../en/edge_ai_dev/tflite_micro_integration.md) | 简体中文 ]

在 openvela 平台上集成 TensorFlow Lite for Microcontrollers (TFLite Micro)，要求开发者深入理解其分层软件架构、组件依赖关系及硬件加速机制。本文档将详细介绍 TFLite Micro 在 openvela 平台上的完整架构设计，指导开发者完成高效集成。

## 一、前置概念与术语

为了更好地理解 TFLite Micro 在嵌入式环境下的工作原理，开发者需先理解以下核心概念，这些术语贯穿于整个集成流程中。

| **术语 (Term)**                    | **解释 (Definition)**                                                                                           | **openvela 平台上下文**                                                        |
| :--------------------------------- | :-------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| **TFLite Micro (TFLM)**            | TensorFlow 的微控制器版本，专为资源受限（KB级内存）设备设计的轻量级推理框架。                                   | 运行在 openvela 上的核心推理引擎。                                             |
| **Tensor** **Arena**               | 一块预先分配的大型连续内存区域。TFLM 不使用 `malloc/free`，而是将模型输入、输出及中间计算数据全部放置在此区域。 | 决定了系统能运行多大的模型，需根据 SRAM 大小谨慎配置。                         |
| **FlatBuffers**                    | 一种高效的序列化格式。模型文件以该格式存储，允许直接从 Flash 读取数据。                                         | 模型数据通常直接编译进固件或存储在文件系统中。                                 |
| **Operator (****Op****) / Kernel** | 神经网络中的具体算子实现（如 Conv2D, Softmax）。Kernel 是 Op 的具体 C++ 代码。                                  | 可通过 **CMSIS-NN** 替换标准 Kernel 以利用 openvela 硬件加速特性。             |
| **Op** **Resolver**                | 算子解析器。用于在运行时查找并注册模型所需的算子实现。                                                          | 推荐使用 `MicroMutableOpResolver` 按需注册，避免引入无用代码导致固件体积膨胀。 |
| **Quantization (量化)**            | 将 32 位浮点数转换为 8 位整数的技术，旨在减少模型体积并加速计算。                                               | openvela 推荐运行 `int8` 量化模型以获得最佳性能。                              |

## 二、软件栈层次

openvela 平台的 TFLite Micro 软件栈采用模块化分层设计，实现了从底层硬件抽象到上层应用接口的解耦。

### 1、整体架构概览

```Plain
┌─────────────────────────────────────────────────────────────┐
│                    应用层 (Application Layer)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    语音识别应用  │  │     图像检测应用  │  │    传感器分析     │      
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  推理 API 层 (Inference API)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Model Loading │ Tensor Management │ Inference API   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              框架层 (TFLite Micro Framework)                 │
│  ┌─────────────────┐  ┌────────────────────────────────┐    │
│  │ Micro Interpreter│  │  Operator Kernels (含 CMSIS-NN │   │
│  ├─────────────────┤  │  / 自定义加速内核)             │   │  │
│  │ Memory Planner  │  ├────────────────────────────────┤    │
│  ├─────────────────┤  │ CONV │ FC │ POOL │ RELU │ ... │     │
│  │ FlatBuffer Parser│  └────────────────────────────────┘   │
│  └─────────────────┘                                        │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│        RTOS / 平台服务层 (NuttX 驱动、内存、文件系统等)          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Task Scheduler │ Memory Mgmt │ Drivers │ File Sys  │    │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  硬件平台 (Hardware)                         │
│    ARM Cortex-M │ RISC-V │ ESP32 │ Custom SoC               │
└─────────────────────────────────────────────────────────────┘
```

### 2、应用层：推理 API

应用层通过 C/C++ API 封装模型加载、推理执行和结果获取等核心功能。开发者应关注如何初始化解释器并高效处理张量数据。

#### 推理程序实现示例

以下代码展示了在 openvela 环境下执行一次完整推理的标准流程：

```C++
static void test_inference(void* file_data, size_t arenaSize) {
  // 1. 加载模型
  const tflite::Model* model = tflite::GetModel(file_data); 
  printf("arenaSize: %d\n", (int)arenaSize);

  // 2. 手动添加算子
  tflite::MicroMutableOpResolver<1> resolver;
  resolver.AddFullyConnected(tflite::Register_FULLY_CONNECTED());

  // 3. 准备 Tensor Arena (内存池)
  std::unique_ptr<uint8_t[]> pArena(new uint8_t[arenaSize]);
  
  // 4. 创建解释器实例
  // 解释器需要模型、算子解析器、内存缓冲区作为输入
  tflite::MicroInterpreter interpreter(model,
    resolver, pArena.get(), arenaSize);

  // 5. 分配张量内存
  interpreter.AllocateTensors();
  
  // 6. 填充输入数据
  TfLiteTensor* input_tensor = interpreter.input(0);
  float* input_tensor_data = tflite::GetTensorData<float>(input_tensor);
  
   // 示例：测试输入 x = π/2, expect y ≈ 1.0
  float x_value = 1.5708f;
  input_tensor_data[0] = x_value;

  // 7. 执行推理
  interpreter.Invoke();

  // 8. 获取输出结果
  TfLiteTensor* output_tensor = interpreter.output(0);
  float* output_tensor_data = tflite::GetTensorData<float>(output_tensor);
  syslog(LOG_INFO, "Output value after inference: %f\n", output_tensor_data[0]);
}
```

### 3、框架层：TFLite Micro 核心组件

框架层是 TFLite Micro 的核心，负责模型解析、内存管理、算子调度等关键功能。该层通过静态内存分配和精简的运行时环境，确保在 openvela 平台上实现极低的系统开销。

#### Micro Interpreter（微型解释器）

解释器是框架的中枢，负责协调模型加载、内存分配、算子执行等流程。它包含三个核心子组件：

1. Model Parser（模型解析器）

    - 解析 FlatBuffers 格式的模型文件。
    - 提取模型元数据：算子类型、张量维度、量化参数。
    - 构建计算图数据结构。

2. Subgraph Manager（子图管理器）

    - 管理模型的计算子图（针对大多数嵌入式模型，通常仅含有一个子图）。
    - 维护节点（算子）和边（张量）的拓扑关系。

3. Invocation Engine（调用引擎）

    - 按拓扑顺序执行算子。
    - 管理算子的输入/输出张量绑定。
    - 处理算子执行错误和异常。

**解释器执行流程如下**：

```Plain
初始化阶段(Setup):
1. AllocateTensors() → 规划并分配所有张量所需的内存空间 (Tensor Arena)


推理阶段 (Inference):
1. interpreter.input() → 填充输入张量并填充数据
2. Invoke() → 触发推理循环
   ├─ for each node in execution_plan（遍历执行计划中的每个节点 (Node)）：
   │    ├─ 获取算子注册信息(Registration)
   │    ├─ 绑定输入/输出张量
   │    └─ 调用算子的 Invoke 函数
   └─ 返回执行状态
3. interpreter.output() → 读取输出张量结果
```

#### Operator Kernels Library（算子内核库）

算子内核是执行数学运算（如卷积、全连接）的具体实现。TFLite Micro 采用注册机制来解耦框架与具体算法实现，这使得在 openvela 上替换特定算子（例如使用硬件加速的卷积）变得非常容易。

**算子接口规范**

开发者若需自定义算子或封装硬件加速驱动，需遵循 `TfLiteRegistration` 接口定义：

```C++
typedef struct {

    // [可选] 初始化：分配算子所需的持久化内存（如滤波器系数表）
    void* (*init)(TfLiteContext* context, const char* buffer, size_t length);
    
    // [可选] 释放：清理 init 分配的资源
    void (*free)(TfLiteContext* context, void* buffer);
    
    // [必须] 准备：校验张量维度、类型，计算临时缓冲区（Scratch Buffer）大小
    TfLiteStatus (*prepare)(TfLiteContext* context, TfLiteNode* node);
    
    // [必须] 执行：核心计算逻辑，从 Input Tensor 读取数据，写入 Output Tensor
    TfLiteStatus (*invoke)(TfLiteContext* context, TfLiteNode* node);
} TfLiteRegistration;
```

**算子实现参考：ReLU**

以下代码展示了一个标准 ReLU 激活函数的实现逻辑，体现了 TFLite Micro 对类型安全和内存操作的封装：

```C++
// 1. 准备阶段：校验数据类型与维度
TfLiteStatus ReluPrepare(TfLiteContext* context, TfLiteNode* node)
{
    // 校验：输入/输出张量数量
    TF_LITE_ENSURE_EQ(context, node->inputs->size, 1);
    TF_LITE_ENSURE_EQ(context, node->outputs->size, 1);

    const TfLiteTensor* input = GetInput(context, node, 0);
    TfLiteTensor* output = GetOutput(context, node, 0);

    // 校验：张量类型
    TF_LITE_ENSURE_TYPES_EQ(context, input->type, kTfLiteFloat32);

    // 配置：调整输出张量形状与输入一致
    return context->ResizeTensor(context, output, TfLiteIntArrayCopy(input->dims));
}

// 2. 执行阶段：数值计算
TfLiteStatus ReluInvoke(TfLiteContext* context, TfLiteNode* node)
{
    const TfLiteTensor* input = GetInput(context, node, 0);
    TfLiteTensor* output = GetOutput(context, node, 0);

    const float* input_data = GetTensorData<float>(input);
    float* output_data = GetTensorData<float>(output);

    // 获取数据总长度
    const int flat_size = MatchingFlatSize(input->dims, output->dims);

    // 执行 ReLU: output = max(0, input)
    for (int i = 0; i < flat_size; ++i) {
        output_data[i] = (input_data[i] > 0.0f) ? input_data[i] : 0.0f;
    }

    return kTfLiteOk;
}

// 3. 注册阶段：返回函数指针结构体
TfLiteRegistration* Register_RELU()
{
    static TfLiteRegistration r = {
        nullptr,      // init
        nullptr,      // free
        ReluPrepare,  // prepare
        ReluInvoke    // invoke
    };
    return &r;
}
```

**算子库源码目录结构**

在 `tensorflow/lite/micro/kernels/` 目录下，代码按算子功能组织：

```Plain
tensorflow/lite/micro/kernels/
├── conv.cc                    # 卷积算子
├── depthwise_conv.cc          # 深度可分离卷积
├── fully_connected.cc         # 全连接层
├── pooling.cc                 # 池化算子
├── activations.cc             # 激活函数（ReLU, Sigmoid 等）
├── softmax.cc                 # Softmax
├── add.cc, mul.cc, sub.cc     # 逐元素运算
├── reshape.cc, transpose.cc   # 张量变换
└── ...
```

#### Memory Planner（内存规划器）

内存规划器是 TFLite Micro 实现低内存占用的关键技术。与桌面端 TensorFlow 动态分配内存不同，Micro 通过分析张量生命周期实现内存复用。

## 三、平台依赖与集成

在 openvela 平台上运行 TFLite Micro 并非孤立存在，它深度依赖底层的 OS 服务与硬件库。理解这些依赖关系，对于性能调优和故障排查至关重要。

### 1、NuttX 内核服务

TFLite Micro 通过平台抽象层与 NuttX RTOS 交互。尽管 TFLite Micro 设计为无 OS 依赖，但在 openvela 上，合理的 OS 配置能显著提升系统稳定性。

#### 任务调度与同步

NuttX 提供了完整的 POSIX 标准支持，TFLite Micro 的推理任务通常封装在标准的 `pthread` 或 NuttX 任务（Task）中。

#### 内存分配器

TFLite Micro 推荐使用 **Tensor Arena** 机制进行内存管理，但在初始化阶段或处理非张量数据时，仍可能与 NuttX 的内存管理器（Mm）交互。

**Tensor Arena 分配策略**

虽然可以使用 `malloc` 动态申请 Arena，但强烈建议采用静态分配。

```C++
// 推荐：编译时确定大小，放置于 BSS 段或特定内存段（如 CCM）
// 预估大小方法：先分配大空间，运行 Interpreter::ArenaUsedBytes() 获取实际用量后调整
#define ARENA_SIZE (100 * 1024)
static uint8_t tensor_arena[ARENA_SIZE] __attribute__((aligned(16)));
```

### 2、硬件加速：CMSIS-NN 集成

为提升在 ARM Cortex-M 核心（openvela 的主要计算单元）上的推理性能，必须集成 CMSIS-NN 库。该库利用 SIMD（单指令多数据）指令集，可将卷积和矩阵乘法的性能提升 4-5 倍。

#### 构建系统配置 (Makefile)

在集成 CMSIS-NN 时，核心逻辑是**替换**：引入优化版本的源文件，同时从编译列表中剔除 TFLite 自带的通用参考实现（Reference Kernels），以避免符号定义冲突。

以下是针对 NuttX 构建系统的配置范本：

```Makefile
# 检测是否在 Kconfig 中开启了 CMSIS-NN 选项
ifneq ($(CONFIG_MLEARNING_CMSIS_NN),)

# 1. 定义宏：告知 TFLite Micro 启用 CMSIS-NN 路径
COMMON_FLAGS += -DCMSIS_NN

# 添加头文件搜索路径
COMMON_FLAGS += ${INCDIR_PREFIX}$(APPDIR)/mlearning/cmsis-nn/cmsis-nn

# 2. 寻找优化源文件：获取 cmsis_nn 目录下的所有 .cc 文件
CMSIS_NN_SRCS := $(wildcard $(TFLM_DIR)/tensorflow/lite/micro/kernels/cmsis_nn/*.cc)

# 3. 排除冲突文件：
# 计算需要排除的通用实现文件名（例如 conv.cc, fully_connected.cc）
# 逻辑：取 CMSIS_NN_SRCS 的文件名，对应到 kernels/ 根目录
UNNEEDED_SRCS := $(addprefix $(TFLM_DIR)/tensorflow/lite/micro/kernels/, $(notdir $(CMSIS_NN_SRCS)))

# 4. 从原始编译列表 CXXSRCS 中过滤掉这些通用实现
CXXSRCS := $(filter-out $(UNNEEDED_SRCS), $(CXXSRCS))

# 5. 将优化后的源文件加入编译列表
CXXSRCS += $(CMSIS_NN_SRCS)

endif
```
