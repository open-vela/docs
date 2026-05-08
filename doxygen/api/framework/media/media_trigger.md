# 媒体触发器 API

媒体触发器（Media Trigger）用于语音唤醒（Voice Trigger）场景，通过加载声学模型实现关键词检测、启动识别等功能。

头文件：`#include <media_trigger.h>`

## openvela 实现说明

- **典型场景**：智能音箱、智能手表的"嘿小爱"等语音唤醒
- **工作流程**：
    1. `open` 打开触发器句柄
    2. `set_event_callback` 注册事件回调
    3. `load_sound_model` 加载声学模型
    4. `start_recognition` 开始识别
    5. 监听回调，检测到关键词后处理
    6. `stop_recognition` → `unload_sound_model` → `close` 清理
- **参数配置**：通过 `open` 传入的 `params` 选择麦克风配置（如 `"default"` / `"Dual Mic"`）
- **底层实现**：对接 DSP 侧的声学模型处理器

## 触发器生命周期

### media_trigger_open

```c
void* media_trigger_open(const char* params);
```

打开媒体触发器句柄。

**参数**：

- `params` 触发器参数字符串，例如 `"default"` 或 `"Dual Mic"`，用于选择麦克风配置。

**返回值**：

成功时返回触发器句柄，失败时返回 `NULL`。

**示例**：

```c
// 1. 创建实例
void* handle = media_trigger_open("default");

// 2. 设置事件回调
ret = media_trigger_set_event_callback(handle, cookie, callback);

// 3. 加载声学模型
ret = media_trigger_load_sound_model(handle, model, model_size);

// 4. 开始识别
ret = media_trigger_start_recognition(handle);

// 5. 停止识别
ret = media_trigger_stop_recognition(handle);

// 6. 卸载模型
ret = media_trigger_unload_sound_model(handle);

// 7. 关闭句柄
ret = media_trigger_close(handle);
```

### media_trigger_close

```c
int media_trigger_close(void* handle);
```

关闭触发器句柄，释放相关资源。

**参数**：

- `handle` 待关闭的触发器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。

## 事件与回调

### media_trigger_set_event_callback

```c
int media_trigger_set_event_callback(void* handle, void* event_cookie,
                                     media_event_callback on_event);
```

为触发器设置事件回调，用于接收识别状态变化等事件。

**参数**：

- `handle` 触发器句柄。
- `event_cookie` 传递给回调的用户数据。
- `on_event` 事件回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。

## 声学模型管理

### media_trigger_load_sound_model

```c
int media_trigger_load_sound_model(void* handle, void* model, size_t model_size);
```

为触发器加载声学模型数据。

**参数**：

- `handle` 触发器句柄。
- `model` 声学模型数据指针。
- `model_size` 模型数据字节数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。

### media_trigger_unload_sound_model

```c
int media_trigger_unload_sound_model(void* handle);
```

卸载已加载的声学模型。

**参数**：

- `handle` 触发器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。

## 识别控制

### media_trigger_start_recognition

```c
int media_trigger_start_recognition(void* handle);
```

开始语音识别。触发器会持续检测输入音频，匹配已加载模型中的关键词。

**参数**：

- `handle` 触发器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。

### media_trigger_stop_recognition

```c
int media_trigger_stop_recognition(void* handle);
```

停止语音识别。

**参数**：

- `handle` 触发器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。

## DSP 属性查询

### media_trigger_get_property

```c
int media_trigger_get_property(char* properties, int len);
```

查询触发器底层 DSP 的属性信息。

**参数**：

- `properties` 输出缓冲区，用于接收属性字符串。
- `len` 缓冲区长度。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。
