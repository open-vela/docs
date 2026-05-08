# 声学模型 API

声学模型（Sound Model）接口用于处理媒体触发器所需的低层声学模型数据，提供模型加载、卸载、属性/选项查询和热词检测能力。

头文件：`#include <media_trigger_model.h>`

## openvela 实现说明

- **与 Media Trigger 的关系**：`media_trigger_*` 是高层语音唤醒接口（含 DSP 通路），`media_trigger_model_*` 是底层模型操作接口（不涉及音频采集）
- **典型用途**：自定义识别流程、在特定 PCM 缓冲上跑一次性的关键词检测
- **模型属性/选项**：通过 `get_properties` 查询厂商属性，`get_options` 读取推荐的音频采样参数
- **一次性检测**：`detect_hotword` 在给定 PCM 缓冲上做一次同步检测

## 模型生命周期

### media_trigger_model_load

```c
void* media_trigger_model_load(const void* model, size_t size);
```

加载声学模型数据，返回模型上下文。

**参数**：

- `model` 模型数据起始指针。
- `size` 模型数据字节数。

**返回值**：

成功时返回模型上下文指针，失败时返回 `NULL`。

### media_trigger_model_unload

```c
void media_trigger_model_unload(void* context);
```

卸载已加载的模型上下文。

**参数**：

- `context` 待卸载的模型上下文。

## 模型属性查询

### media_trigger_model_get_properties

```c
void media_trigger_model_get_properties(void* properties, size_t* size);
```

查询厂商提供的模型属性信息。

**参数**：

- `properties` 输出缓冲区，用于存放属性数据。
- `size` 输入输出参数：调用时表示缓冲区大小，返回时被更新为实际写入的字节数。

### media_trigger_model_get_options

```c
void media_trigger_model_get_options(void* context, char* options, size_t size);
```

查询模型推荐的音频采集选项字符串，例如 `"format=s16le:sample_rate=16000:ch_layout=mono"`。

**参数**：

- `context` 模型上下文（由 `media_trigger_model_load` 返回）。
- `options` 输出缓冲区，用于接收选项字符串。
- `size` 输出缓冲区字节数。

### media_trigger_model_get_buffer_size

```c
void media_trigger_model_get_buffer_size(void* context, size_t* size);
```

查询模型推荐的录音缓冲区大小。

**参数**：

- `context` 模型上下文。
- `size` 输出参数，返回推荐的缓冲区字节数。

## 热词检测

### media_trigger_model_detect_hotword

```c
bool media_trigger_model_detect_hotword(void* context, const char* buffer, size_t size);
```

在给定 PCM 缓冲上运行一次模型检测，判断是否匹配到热词。

**参数**：

- `context` 模型上下文。
- `buffer` 待检测的 PCM 音频缓冲区。
- `size` 缓冲区字节数。

**返回值**：

检测到热词时返回 `true`，未检测到返回 `false`。
