\[ [English](../../../../en/api/framework/media/media_player.md) | 简体中文 \]

# 多媒体播放器 API

音视频播放功能，支持本地文件和网络流媒体。

头文件：`#include <media_player.h>`

## openvela 实现说明

- **同步/异步双模型**：提供两套对等接口
    - 同步：`media_player_*` 系列，调用在当前线程返回
    - 异步：`media_uv_player_*` 系列，基于 libuv 事件循环，需启用 `CONFIG_LIBUV`
- **生命周期**：`open` 创建播放器 → `prepare` 设置源 → `start` 开始播放 → `stop`/`close` 释放
- **数据源**：支持两种输入方式
    - 本地/网络 URL：通过 `prepare(url)` 直接指定
    - 字节流缓冲：通过 `write_data` 推送，或 `get_socket` 获取底层套接字
- **事件回调**：通过 `set_event_callback` 注册事件监听器，接收播放状态变化、错误等通知
- **参数配置**：通用参数通过 `set_property` / `get_property` 读写（如采样率、通道数等）

## 同步接口 - 生命周期

### media_player_open

```c
void* media_player_open(const char* stream);
```

打开指定流类型的播放器。

**参数**：

- `stream` 流类型常量，不同流类型有不同的路由逻辑。

**返回值**：

成功时返回播放器句柄，失败时返回 `NULL`。


### media_player_close

```c
int media_player_close(void* handle, int pending_stop);
```

关闭播放器。

**参数**：

- `handle` 播放器句柄。
- `pending_stop` 关闭前是否等待停止完成：0 表示立即停止并关闭，1 表示等待当前曲目播放完成再关闭。此参数仅对音频播放器有效；视频播放器设置为 1 时不产生等待效果。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_set_event_callback

```c
int media_player_set_event_callback(void* handle, void* event_cookie, media_event_callback on_event);
```

设置事件回调，监听流状态变更。

**参数**：

- `handle` 播放器句柄。
- `event_cookie` 回调上下文参数。
- `on_event` 事件回调函数，用于接收流状态变化通知。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_player_prepare

```c
int media_player_prepare(void* handle, const char* url, const char* options);
```

准备播放资源。

**参数**：

- `handle` 播放器句柄。
- `url` 资源路径，支持两种模式：1. URL 模式：`url` 为本地文件路径或网络地址，框架会读取并播放；2. BUFFER 模式：`url` 为 `NULL`，调用方需通过 `media_player_write_data()` 或 `media_player_get_socket()` + `write()` 持续推送数据。
- `options` 资源的额外配置参数，通常为描述资源格式的键值对（例如 `"format=s16le,sample_rate=44100,channels=2"`）。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_player_reset

```c
int media_player_reset(void* handle);
```

重置播放器到初始状态。

**参数**：

- `handle` 播放器句柄，由 `media_player_open` 返回。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


## 同步接口 - 数据流

### media_player_write_data

```c
ssize_t media_player_write_data(void* handle, const void* data, size_t len);
```

写入数据到播放器进行播放。

**参数**：

- `handle` 播放器句柄。
- `data` 数据缓冲区地址。
- `len` 要写入的数据长度（字节）。

**返回值**：

成功时返回实际写入的字节数，失败时返回负的错误码。


### media_player_get_sockaddr

```c
int media_player_get_sockaddr(void* handle, struct sockaddr_storage* addr);
```

获取缓冲模式的 Socket 地址信息。

**参数**：

- `handle` 播放器句柄。
- `addr` 用于存储 Socket 地址信息的输出参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_get_socket

```c
int media_player_get_socket(void* handle);
```

获取用于写入的 Socket 文件描述符。

**参数**：

- `handle` 播放器句柄。

**返回值**：

成功时返回 Socket 文件描述符，失败时返回负的错误码。


### media_player_close_socket

```c
void media_player_close_socket(void* handle);
```

关闭 Socket 文件描述符。

**参数**：

- `handle` 播放器句柄。


## 同步接口 - 播放控制

### media_player_start

```c
int media_player_start(void* handle);
```

开始或恢复播放音频源。

**参数**：

- `handle` 播放器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_player_stop

```c
int media_player_stop(void* handle);
```

停止播放并清除已准备的音频源。

**参数**：

- `handle` 播放器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_player_pause

```c
int media_player_pause(void* handle);
```

暂停播放。

**参数**：

- `handle` 播放器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_player_seek

```c
int media_player_seek(void* handle, unsigned int position);
```

跳转到指定的播放位置。

**参数**：

- `handle` 播放器句柄。
- `position` 目标位置，单位为毫秒，从起始位置计算。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_player_set_looping

```c
int media_player_set_looping(void* handle, int loop);
```

设置循环播放次数。

**参数**：

- `handle` 播放器句柄。
- `loop` 循环次数，`-1` 表示无限循环。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


## 同步接口 - 状态查询

### media_player_is_playing

```c
int media_player_is_playing(void* handle);
```

查询当前是否正在播放。

**参数**：

- `handle` 播放器句柄。

**返回值**：

正在播放时返回正值，未播放时返回 `0`，出错时返回负的错误码。


### media_player_get_position

```c
int media_player_get_position(void* handle, unsigned int* position);
```

获取当前播放位置。

**参数**：

- `handle` 播放器句柄。
- `position` 输出参数，当前播放位置，单位为毫秒。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_get_duration

```c
int media_player_get_duration(void* handle, unsigned int* duration);
```

获取当前音频源的总时长。

**参数**：

- `handle` 播放器句柄。
- `duration` 输出参数，音频源总时长，单位为毫秒。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_get_latency

```c
int media_player_get_latency(void* handle, unsigned int* latency);
```

获取当前音频源的播放延迟。

**参数**：

- `handle` 播放器句柄。
- `latency` 输出参数，延迟帧数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


## 同步接口 - 音量与属性

### media_player_set_volume

```c
int media_player_set_volume(void* handle, float volume);
```

设置播放音量。

**参数**：

- `handle` 播放器句柄。
- `volume` 音量值，取值范围 `[0.0, 1.0]`。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_player_get_volume

```c
int media_player_get_volume(void* handle, float* volume);
```

获取当前播放音量。

**参数**：

- `handle` 播放器句柄。
- `volume` 输出参数，当前音量值，取值范围 `[0.0, 1.0]`。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_set_property

```c
int media_player_set_property(void* handle, const char* target, const char* key, const char* value);
```

设置播放器属性。

**参数**：

- `handle` 播放器句柄。
- `target` 目标 filter 名称。
- `key` 属性键名。
- `value` 属性值。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_get_property

```c
int media_player_get_property(void* handle, const char* target, const char* key, char* value, int value_len);
```

获取播放器属性。

**参数**：

- `handle` 播放器句柄。
- `target` 目标 filter 名称。
- `key` 属性键名。
- `value` 输出缓冲区，用于存储属性值。
- `value_len` 输出缓冲区长度。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


## 异步接口（基于 libuv）

以下接口仅在启用 `CONFIG_LIBUV` 时可用，回调在 `uv_loop` 上执行，避免阻塞调用线程。

### media_uv_player_open

```c
void* media_uv_player_open(void* loop, const char* stream, media_uv_callback on_open, void* cookie);
```

打开异步播放器。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `stream` 流类型常量，不同流类型有不同的路由逻辑。
- `on_open` 打开完成后触发的回调函数。
- `cookie` 回调上下文，供 `on_open`、`on_event`、`on_connection`、`on_close` 共用。

**返回值**：

成功时返回播放器句柄，失败时返回 `NULL`。


### media_uv_player_listen

```c
int media_uv_player_listen(void* handle, media_event_callback on_event);
```

注册事件监听回调，接收播放状态变化通知。

**参数**：

- `handle` 异步播放器句柄。
- `on_event` 事件回调函数，在收到通知后调用。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_close

```c
int media_uv_player_close(void* handle, int pending, media_uv_callback on_close);
```

关闭异步播放器。

**参数**：

- `handle` 异步播放器句柄。
- `pending` 是否以 pending 方式关闭（等待当前播放完成）。
- `on_close` 资源释放完成后触发的回调函数。

**返回值**：

成功时返回 `0`，无效句柄时返回负的错误码。


### media_uv_player_prepare

```c
int media_uv_player_prepare(void* handle, const char* url, const char* options, media_uv_object_callback on_connection, media_uv_callback on_prepare, void* cookie);
```

准备音频源以供播放。

**参数**：

- `handle` 异步播放器句柄。
- `url` 资源路径，支持两种模式：1. URL 模式：`url` 为本地文件路径或网络地址，框架会读取并播放；2. BUFFER 模式：`url` 为 `NULL`，调用方需通过 `media_player_write_data()` 或 `media_player_get_socket()` + `write()` 持续推送数据。
- `options` 资源的额外配置参数，通常为描述资源格式的键值对（例如 `"format=s16le,sample_rate=44100,channels=2"`）。
- `on_connection` BUFFER 模式下接收 `uv_pipe_t` 的回调函数。
- `on_prepare` 准备完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_uv_player_reset

```c
int media_uv_player_reset(void* handle, media_uv_callback on_reset, void* cookie);
```

重置播放器到初始状态。

**参数**：

- `handle` 异步播放器句柄。
- `on_reset` 重置完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_start_auto

```c
int media_uv_player_start_auto(void* handle, const char* scenario, media_uv_callback on_start, void* cookie);
```

播放或恢复已准备的音频源，并自动请求音频焦点。

**参数**：

- `handle` 异步播放器句柄。
- `scenario` 场景常量，不同场景对应不同的焦点优先级。
- `on_start` 播放开始后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_start

```c
int media_uv_player_start(void* handle, media_uv_callback on_start, void* cookie);
```

播放或恢复已准备的资源。

**参数**：

- `handle` 异步播放器句柄。
- `on_start` 播放开始后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_pause

```c
int media_uv_player_pause(void* handle, media_uv_callback on_pause, void* cookie);
```

暂停播放。

**参数**：

- `handle` 异步播放器句柄。
- `on_pause` 暂停完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_stop

```c
int media_uv_player_stop(void* handle, media_uv_callback on_stop, void* cookie);
```

停止播放并清除已准备的音频源。

**参数**：

- `handle` 异步播放器句柄。
- `on_stop` 停止完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_set_volume

```c
int media_uv_player_set_volume(void* handle, float volume, media_uv_callback on_volume, void* cookie);
```

设置播放音量。

**参数**：

- `handle` 异步播放器句柄。
- `volume` 音量值，取值范围 `[0.0, 1.0]`。
- `on_volume` 设置完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_uv_player_get_volume

```c
int media_uv_player_get_volume(void* handle, media_uv_float_callback on_volume, void* cookie);
```

获取当前播放音量。

**参数**：

- `handle` 异步播放器句柄。
- `on_volume` 结果回调函数，回调参数为当前音量值（范围 `0.0 - 1.0`）。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_get_playing

```c
int media_uv_player_get_playing(void* handle, media_uv_int_callback on_playing, void* cookie);
```

获取当前播放状态。

**参数**：

- `handle` 异步播放器句柄。
- `on_playing` 结果回调函数，回调参数为播放状态。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_get_position

```c
int media_uv_player_get_position(void* handle, media_uv_unsigned_callback on_position, void* cookie);
```

获取当前播放位置。

**参数**：

- `handle` 异步播放器句柄。
- `on_position` 结果回调函数，回调参数为当前位置（毫秒）。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_get_duration

```c
int media_uv_player_get_duration(void* handle, media_uv_unsigned_callback on_duration, void* cookie);
```

获取当前音频源的总时长。

**参数**：

- `handle` 异步播放器句柄。
- `on_duration` 结果回调函数，回调参数为总时长（毫秒）。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_get_latency

```c
int media_uv_player_get_latency(void* handle, media_uv_unsigned_callback cb, void* cookie);
```

获取当前音频源的播放延迟。

**参数**：

- `handle` 异步播放器句柄。
- `cb` 结果回调函数，回调参数为延迟帧数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_set_looping

```c
int media_uv_player_set_looping(void* handle, int loop, media_uv_callback on_looping, void* cookie);
```

设置循环播放次数。

**参数**：

- `handle` 异步播放器句柄。
- `loop` 循环次数，`-1` 表示无限循环。
- `on_looping` 设置完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_seek

```c
int media_uv_player_seek(void* handle, unsigned int position, media_uv_callback on_seek, void* cookie);
```

跳转到指定的播放位置。

**参数**：

- `handle` 异步播放器句柄。
- `position` 目标位置，单位为毫秒，从起始位置计算。
- `on_seek` 跳转完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_set_property

```c
int media_uv_player_set_property(void* handle, const char* target, const char* key, const char* value, media_uv_callback on_setprop, void* cookie);
```

设置播放器属性。

**参数**：

- `handle` 异步播放器句柄。
- `target` 目标 filter 名称。
- `key` 属性键名。
- `value` 属性值。
- `on_setprop` 设置完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_get_property

```c
int media_uv_player_get_property(void* handle, const char* target, const char* key, media_uv_string_callback on_getprop, void* cookie);
```

获取播放器属性。

**参数**：

- `handle` 异步播放器句柄。
- `target` 目标 filter 名称。
- `key` 属性键名。
- `on_getprop` 结果回调函数，回调参数为属性值字符串。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_query

```c
int media_uv_player_query(void* handle, media_uv_object_callback on_query, void* cookie);
```

查询播放器元数据。

**参数**：

- `handle` 异步播放器句柄。
- `on_query` 结果回调函数，回调参数为元数据指针。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_uv_player_close_socket

```c
int media_uv_player_close_socket(void* handle);
```

关闭 Socket 文件描述符。

**参数**：

- `handle` 播放器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。
