# 模型转换与代码集成

[ [English](../../en/edge_ai_dev/model_integration.md) | 简体中文 ]

在 openvela 开发中，由于微控制器 (MCU) 的 RAM 资源受限且文件系统支持可能被裁剪，直接读取 .tflite 文件通常不可行。标准做法是将训练好的 TensorFlow Lite 模型转换为 C 语言数组，作为只读数据 (RODATA) 编译到应用程序固件中，直接从 Flash 执行读取。

本节将指导开发者如何将模型转换为 C 数组，并将其集成到 openvela 的 C++ 应用（如 helloxx）中。

## 一、模型转换 (TFLite 转 C 数组)

为了将模型嵌入固件，我们需要使用工具将 `.tflite` 二进制文件转换为 C 源代码文件。

### 1、准备模型文件

本教程使用 TensorFlow Lite Micro 官方的 Hello World 模型（正弦波预测）。为了配合下文的代码逻辑，我们需要下载 Float32（浮点）版本的模型。

- 下载地址：[hello_world_float.tflite](https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/examples/hello_world/models/hello_world_float.tflite) (Google 官方示例)

请将下载的文件重命名为 `converted_model.tflite` 并放置在当前目录下。

### 2、使用 xxd 工具转换

在 Linux/Unix 环境下，使用 `xxd` 命令即可生成包含模型数据的源文件：

```Bash
# 将 converted_model.tflite 转换为 model_data.cc
xxd -i converted_model.tflite > model_data.cc
```

### 3、优化模型数组声明

`xxd` 生成的默认输出类似如下：

```c++
unsigned char converted_model_tflite[] = {  0x18, 0x00, ...};
unsigned int converted_model_tflite_len = 18200;
```

**关键优化步骤**：

为了节省宝贵的 RAM 资源并确保程序稳定运行，**必须**对生成的数组进行修改：

1. **添加 `const`**：将模型数据放置在 Flash (RODATA段) 中，避免占用 RAM。
2. **添加内存对齐**：TFLite Micro 要求模型数据首地址必须 16 字节对齐。

请打开 `model_data.cc`，复制其中的数组内容，将其直接粘贴到主程序文件 `helloxx_main.cxx` 中（推荐）：

```C++
// 添加 alignas(16) 以满足 TFLite 的内存对齐要求
// 添加 const 将数据放入 Flash，节省 RAM
alignas(16) const unsigned char converted_model_tflite[] = { 
    0x18, 0x00, ... 
};
const unsigned int converted_model_tflite_len = 18200;
```

## 二、集成到应用程序

本节以修改 openvela 中的标准 C++ 示例程序 `apps/examples/helloxx` 为例，展示如何集成 TFLite Micro。

### 1、修改构建系统

在应用编译时，需要包含 TFLite Micro 的头文件路径和构建规则。编辑 `apps/examples/helloxx/CMakeLists.txt`，可以参考以下内容：

```Bash
if(CONFIG_EXAMPLES_HELLOXX)
  nuttx_add_application(
    NAME
    helloxx
    STACKSIZE
    10240
    MODULE
    ${CONFIG_EXAMPLES_HELLOXX}
    SRCS
    helloxx_main.cxx
    DEPENDS
    tflite_micro
    DEFINITIONS
    TFLITE_WITH_STABLE_ABI=0
    TFLITE_USE_OPAQUE_DELEGATE=0
    TFLITE_SINGLE_ROUNDING=0
    TF_LITE_STRIP_ERROR_STRINGS
    TF_LITE_STATIC_MEMORY
    COMPILE_FLAGS
    -Wno-error)
endif()
```

### 2、修改配置

- 参考[配置 TFLite Micro 开发环境](./configure_tflite_micro_dev_env.md)，配置编译环境与依赖库。
- 启用示例应用：在配置菜单 (`menuconfig`) 中，定位到 `Application Configuration` -> `Examples`，勾选 `"Hello, World!" C++ example` (即 `helloxx`)。

### 3、实现推理逻辑

在代码中集成 TFLite Micro 主要包含五个标准步骤：

1. **加载模型**：从 C 数组加载模型结构。
2. **注册算子**：实例化 `OpResolver` 并注册模型所需的算子（Operators）。
3. **准备环境**：实例化 `Interpreter` 并分配 Tensor Arena（张量内存池）。
4. **写入输入**：将传感器数据或测试数据填入输入张量。
5. **执行与读取**：调用 `Invoke()` 并读取输出张量。

打开 `apps/examples/helloxx/helloxx_main.cxx`，需包含以下核心逻辑：

```C++
#include <cstdio>
#include <syslog.h>
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"

// ==========================================================
// 模型数据定义 (建议直接粘贴 xxd 生成的内容并修改修饰符)
// ==========================================================
alignas(16) const unsigned char converted_model_tflite[] = {
    // ... 这里粘贴 xxd -i 生成的具体十六进制数据 ...
    0x1c, 0x00, 0x00, 0x00, 0x54, 0x46, 0x4c, 0x33, // 示例头
    // ... 省略中间数据 ...
};
const unsigned int converted_model_tflite_len = 18200; // 请填写实际长度

static void test_inference(const void* file_data, size_t arenaSize) {
  // 1. 加载模型
  const tflite::Model* model = tflite::GetModel(file_data); 

  // 2. 注册算子
  // 注意：此处仅注册了 FullyConnected 算子，请根据实际模型需求添加
  tflite::MicroMutableOpResolver<1> resolver;
  resolver.AddFullyConnected(tflite::Register_FULLY_CONNECTED());

  // 3. 分配内存与实例化解释器
  std::unique_ptr<uint8_t[]> pArena(new uint8_t[arenaSize]);
  // 创建一个解释器实例。解释器需要模型、算子解析器、内存缓冲区作为输入
  tflite::MicroInterpreter interpreter(model,
    resolver, pArena.get(), arenaSize);

  // 分配张量内存
  interpreter.AllocateTensors();
  
  // 4. 写入输入数据
  TfLiteTensor* input_tensor = interpreter.input(0);
  float* input_tensor_data = tflite::GetTensorData<float>(input_tensor);
  
  // 测试用例：输入 x = π/2 (1.5708)，期望模型输出 y ≈ 1.0
  float x_value = 1.5708f;  
  input_tensor_data[0] = x_value;

   // 5. 执行推理
  interpreter.Invoke();

  // 读取输出结果
  TfLiteTensor* output_tensor = interpreter.output(0);
  float* output_tensor_data = tflite::GetTensorData<float>(output_tensor);
  printf("Output value after inference: %f\n", output_tensor_data[0]);
}
```

### 4、验证结果

编译并烧录固件后，运行 `helloxx` 命令，终端应输出如下推理结果：

```Plain
Output value after inference:0.99999
```

若输出值接近 1.0，表明模型已成功在 openvela 平台上加载并完成了一次正弦波推理计算。
