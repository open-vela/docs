\[ [English](../../../../en/api/framework/media/media_policy.md) | 简体中文 \]

# 音频策略 API

音频路由、设备管理和模式切换策略。

头文件：`#include <media_policy.h>`

## openvela 实现说明

- **Parameter Framework（PFW）后端**：策略数据通过 openvela PFW 规则引擎管理，运行时可动态切换
- **同步/异步双模型**：`media_policy_*`（同步）和 `media_uv_policy_*`（异步，基于 libuv）
- **策略类别**：涵盖 5 类运行时控制
    - 音频模式（Audio Mode）：通话、媒体播放、免提等场景切换
    - 设备路由（Device Routing）：启用/禁用、可用性、使用状态
    - 音量控制（Stream Volume）：按音频流类型调整音量
    - 静音（Mute）：全局静音与麦克风静音
    - 通用参数（int/string/include/exclude/contain）：扩展配置读写
- **订阅机制**：通过 `media_policy_subscribe` 监听策略变化事件（同步接口独有）
- **HFP 采样率**：通过 `set_hfp_samplerate` 调整蓝牙免提音频采样率

## 同步接口 - 音频模式

### media_policy_set_audio_mode

```c
int media_policy_set_audio_mode(const char* mode);
```

设置音频模式（如通话模式、正常模式）。

**参数**：

- `mode` 模式常量

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_get_audio_mode

```c
int media_policy_get_audio_mode(char* mode, int len);
```

获取当前音频模式。

**参数**：

- `mode` 输出缓冲区。
- `len` 缓冲区长度。


## 同步接口 - 设备使用


### media_policy_set_devices_use

```c
int media_policy_set_devices_use(const char* devices);
```

强制使用指定音频设备或协议。

**参数**：

- `devices` 设备常量，支持多设备，用 "|" 分隔。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_policy_set_devices_unuse

```c
int media_policy_set_devices_unuse(const char* devices);
```

取消强制使用音频设备。

**参数**：

- `devices` 设备常量，支持多设备，用 "|" 分隔。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_policy_get_devices_use

```c
int media_policy_get_devices_use(char* devices, int len);
```

获取当前强制使用的音频设备。

**参数**：

- `devices` 设备名称字符串，多个设备用 `|` 分隔（例如 `"sco"`、`"sco|mic"`、`"<none>"`）。
- `len` 缓冲区长度。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_policy_is_devices_use

```c
int media_policy_is_devices_use(const char* devices, int* use);
```

检查指定设备是否处于强制使用状态。

**参数**：

- `devices` 设备常量，支持多设备，用 "|" 分隔。
- `use` 设备使用状态：0 表示所有设备均未使用，1 表示至少有一个设备正在使用。


## 同步接口 - HFP 采样率与设备可用性


### media_policy_set_hfp_samplerate

```c
int media_policy_set_hfp_samplerate(int rate);
```

设置 HFP 蓝牙通话采样率。HFP（Hands-Free Profile）基于 BT-SCO 传输，采样率在协商完成前不确定。

**参数**：

- `rate` 采样率，CVSD 编码取 8000，mSBC 编码取 16000。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_set_devices_available

```c
int media_policy_set_devices_available(const char* devices);
```

报告音频设备（或协议）可用。

**参数**：

- `devices` 设备常量，支持多设备，用 "|" 分隔。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_set_devices_unavailable

```c
int media_policy_set_devices_unavailable(const char* devices);
```

报告音频设备（或协议）不可用。

**参数**：

- `devices` 设备常量，支持多设备，用 "|" 分隔。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_get_devices_available

```c
int media_policy_get_devices_available(char* devices, int len);
```

获取当前可用设备。

**参数**：

- `devices` 设备名称字符串，多个设备用 `|` 分隔（例如 `"sco"`、`"sco|mic"`、`"<none>"`）。
- `len` 缓冲区长度。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_policy_is_devices_available

```c
int media_policy_is_devices_available(const char* devices, int* available);
```

检查指定设备是否可用。

**参数**：

- `devices` 待检查的设备，取值为 `MEDIA_DEVICE_*` 常量，多个设备用 `|` 分隔。
- `available` 设备可用性状态：0 表示所有设备均不可用，1 表示至少有一个设备可用。


## 同步接口 - 静音控制


### media_policy_set_mute_mode

```c
int media_policy_set_mute_mode(int mute);
```

设置静音模式。

**参数**：

- `mute` 新的静音模式：0 表示关闭静音，1 表示开启静音。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_policy_get_mute_mode

```c
int media_policy_get_mute_mode(int* mute);
```

获取当前静音模式。

**参数**：

- `mute` 当前静音模式：0 表示关闭静音，1 表示开启静音。


## 同步接口 - 音量控制


### media_policy_set_stream_volume

```c
int media_policy_set_stream_volume(const char* stream, int volume);
```

设置指定流类型的音量档位。

**参数**：

- `stream` 流类型常量（`MEDIA_STREAM_*`）。
- `volume` 新的音量档位。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_policy_get_stream_volume

```c
int media_policy_get_stream_volume(const char* stream, int* volume);
```

获取指定流类型的音量档位。

**参数**：

- `stream` 流类型常量（`MEDIA_STREAM_*`）。
- `volume` 当前音量档位。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_policy_increase_stream_volume

```c
int media_policy_increase_stream_volume(const char* stream);
```

将指定流类型的音量档位加 1。

**参数**：

- `stream` 流类型常量（`MEDIA_STREAM_*`）。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_policy_decrease_stream_volume

```c
int media_policy_decrease_stream_volume(const char* stream);
```

将指定流类型的音量档位减 1。

**参数**：

- `stream` 流类型常量（`MEDIA_STREAM_*`）。


## 同步接口 - 麦克风静音


### media_policy_set_mic_mute

```c
int media_policy_set_mic_mute(int mute);
```

静音麦克风。

**参数**：

- `mute` 麦克风静音模式：1 表示关闭静音，0 表示开启静音。


## 同步接口 - 通用参数读写


### media_policy_set_int

```c
int media_policy_set_int(const char* name, int value, int apply);
```

设置策略条件的数值。

**参数**：

- `name` 准则名称。
- `value` 数值。
- `apply` 是否将变更应用到策略。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_get_int

```c
int media_policy_get_int(const char* name, int* value);
```

获取策略条件的数值。

**参数**：

- `name` 准则名称。
- `value` 数值。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_get_range

```c
int media_policy_get_range(const char* name, int* min_value, int* max_value);
```

获取策略条件的数值范围。

**参数**：

- `name` 准则名称。
- `min_value` 数值最小值。
- `min_value` 数值最大值。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_set_string

```c
int media_policy_set_string(const char* name, const char* value, int apply);
```

设置策略条件的字符串值。

**参数**：

- `name` 准则名称。
- `value` 字符串值。
- `apply` 是否将变更应用到策略。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_get_string

```c
int media_policy_get_string(const char* name, char* value, int len);
```

获取策略条件的字符串值。

**参数**：

- `name` 准则名称。
- `value` 输出缓冲区。
- `len` 缓冲区长度。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_include

```c
int media_policy_include(const char* name, const char* values, int apply);
```

向包含型条件添加字面值。

**参数**：

- `name` 准则名称。
- `values` 字符串值。
- `apply` 是否将变更应用到策略。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_exclude

```c
int media_policy_exclude(const char* name, const char* values, int apply);
```

从包含型条件移除字面值。

**参数**：

- `name` 准则名称。
- `values` 字符串值。
- `apply` 是否将变更应用到策略。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_contain

```c
int media_policy_contain(const char* name, const char* values, int* result);
```

检查字面值是否包含在包含型条件中。

**参数**：

- `name` 准则名称。
- `values` 字符串值数组。
- `result` 值是否被包含。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_increase

```c
int media_policy_increase(const char* name, int apply);
```

将数值型条件值加 1。

**参数**：

- `name` 准则名称。
- `apply` 是否将变更应用到策略。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_policy_decrease

```c
int media_policy_decrease(const char* name, int apply);
```

将数值型条件值减 1。

**参数**：

- `name` 准则名称。
- `apply` 是否将变更应用到策略。

**返回值**：

成功时返回 0，失败时返回负的错误码。


## 同步接口 - 订阅事件

### media_policy_subscribe

```c
void* media_policy_subscribe(const char* name, media_policy_change_callback on_change, void* cookie);
```

订阅策略条件变化事件。

**参数**：

- `name` 准则名称。
- `on_change` 准则值变化时触发的回调。

**返回值**：

成功时返回有效句柄，失败时返回 `NULL`。


### media_policy_unsubscribe

```c
int media_policy_unsubscribe(void* handle);
```

取消订阅策略条件变化事件。

**参数**：

- `name` 准则名称。
- `handle` 用于取消订阅的句柄。


## 异步接口（基于 libuv）

以下接口仅在启用 `CONFIG_LIBUV` 时可用。


### media_uv_policy_set_int

```c
int media_uv_policy_set_int(void* loop, const char* name, int value, int apply, media_uv_callback cb, void* cookie);
```

设置策略条件的数值。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `name` 准则名称。
- `value` 要设置的数值。
- `apply` 是否将新值应用到策略配置。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_policy_get_int

```c
int media_uv_policy_get_int(void* loop, const char* name, media_uv_int_callback cb, void* cookie);
```

获取策略条件的数值。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `name` 准则名称。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_policy_increase

```c
int media_uv_policy_increase(void* loop, const char* name, int apply, media_uv_callback cb, void* cookie);
```

将策略条件的数值加 1。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `name` 准则名称。
- `apply` 是否将新值应用到策略配置。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_policy_set_string

```c
int media_uv_policy_set_string(void* loop, const char* name, const char* value, int apply, media_uv_callback cb, void* cookie);
```

设置策略条件的字符串值。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `name` 准则名称。
- `value` 要设置的字符串值。
- `apply` 是否将新值应用到策略配置。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_policy_get_string

```c
int media_uv_policy_get_string(void* loop, const char* name, media_uv_string_callback cb, void* cookie);
```

获取策略条件的字符串值。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `name` 准则名称。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_policy_decrease

```c
int media_uv_policy_decrease(void* loop, const char* name, int apply, media_uv_callback cb, void* cookie);
```

将策略条件的数值减 1。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `name` 准则名称。
- `apply` 是否将新值应用到策略配置。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_policy_include

```c
int media_uv_policy_include(void* loop, const char* name, const char* value, int apply, media_uv_callback cb, void* cookie);
```

向包含型条件添加字面值。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `name` 准则名称。
- `value` 字符串值数组。
- `apply` 是否将新值应用到策略配置。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_policy_exclude

```c
int media_uv_policy_exclude(void* loop, const char* name, const char* value, int apply, media_uv_callback cb, void* cookie);
```

从包含型条件移除字面值。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `name` 准则名称。
- `value` 字符串值数组。
- `apply` 是否将新值应用到策略配置。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_policy_contain

```c
int media_uv_policy_contain(void* loop, const char* name, const char* value, media_uv_int_callback cb, void* cookie);
```

检查字面值是否包含在包含型条件中。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `name` 准则名称。
- `value` 字符串值数组。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_policy_set_stream_volume

```c
int media_uv_policy_set_stream_volume(void* loop, const char* stream, int volume, media_uv_callback cb, void* cookie);
```

设置指定流类型的音量。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `stream` 流类型，取值为流类型常量。
- `volume` 要设置的音量档位。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_get_stream_volume

```c
int media_uv_policy_get_stream_volume(void* loop, const char* stream, media_uv_int_callback cb, void* cookie);
```

获取指定流类型的音量。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `stream` 流类型，取值为流类型常量。
- `volume` 要设置的音量档位。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_increase_stream_volume

```c
int media_uv_policy_increase_stream_volume(void* loop, const char* stream, media_uv_callback cb, void* cookie);
```

将指定流类型的音量加 1。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `stream` 流类型，取值为流类型常量。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_decrease_stream_volume

```c
int media_uv_policy_decrease_stream_volume(void* loop, const char* stream, media_uv_callback cb, void* cookie);
```

将指定流类型的音量减 1。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `stream` 流类型，取值为流类型常量。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_set_audio_mode

```c
int media_uv_policy_set_audio_mode(void* loop, const char* mode, media_uv_callback cb, void* cookie);
```

设置音频模式（如通话模式、正常模式）。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `mode` 新的音频模式。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_get_audio_mode

```c
int media_uv_policy_get_audio_mode(void* loop, media_uv_string_callback cb, void* cookie);
```

获取当前音频模式。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_set_devices_use

```c
int media_uv_policy_set_devices_use(void* loop, const char* devices, bool use, media_uv_callback cb, void* cookie);
```

强制使用或取消使用指定设备（或协议）。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `devices` 目标设备。
- `use` 将设备设置为使用或未使用状态。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_get_devices_use

```c
int media_uv_policy_get_devices_use(void* loop, media_uv_string_callback cb, void* cookie);
```

获取当前强制使用的设备。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_is_devices_use

```c
int media_uv_policy_is_devices_use(void* loop, const char* devices, media_uv_int_callback cb, void* cookie);
```

检查指定设备是否正在被使用。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `devices` 待检查的设备。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_set_hfp_samplerate

```c
int media_uv_policy_set_hfp_samplerate(void* loop, int rate, media_uv_callback cb, void* cookie);
```

设置 HFP（Hands-Free Profile）采样率。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `rate` 采样率，CVSD 编码取 8000，mSBC 编码取 16000。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

**注意**：

- 此接口已废弃，`rate` 参数将来会改为 `int` 类型。


### media_uv_policy_set_devices_available

```c
int media_uv_policy_set_devices_available(void* loop, const char* devices, bool available, media_uv_callback cb, void* cookie);
```

设置设备可用或不可用状态。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `devices` 目标设备。
- `available` 将设备设置为可用或不可用状态。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_policy_get_devices_available

```c
int media_uv_policy_get_devices_available(void* loop, media_uv_string_callback cb, void* cookie);
```

获取当前可用设备。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_is_devices_available

```c
int media_uv_policy_is_devices_available(void* loop, const char* devices, media_uv_int_callback cb, void* cookie);
```

检查指定设备是否可用。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `devices` 待检查的设备。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_set_mute_mode

```c
int media_uv_policy_set_mute_mode(void* loop, int mute, media_uv_callback cb, void* cookie);
```

设置静音模式。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `mute` 新的静音模式。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_get_mute_mode

```c
int media_uv_policy_get_mute_mode(void* loop, media_uv_int_callback cb, void* cookie);
```

获取当前静音模式。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_policy_set_mic_mute

```c
int media_uv_policy_set_mic_mute(void* loop, int mute, media_uv_callback cb, void* cookie);
```

静音内置麦克风或蓝牙麦克风。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `mute` 静音模式。
- `cb` 结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


