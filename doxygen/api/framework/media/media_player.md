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

- `stream` 流类型常量。 不同流类型有不同的路由逻辑.

**返回值**：

void*    播放器句柄, NULL on failure。


### media_player_close

```c
int media_player_close(void* handle, int pending_stop);
```

关闭播放器。

**参数**：

- `handle` 播放器句柄.
- `pending_stop` 关闭前是否等待停止完成：0 表示立即停止并关闭，1 表示等待当前曲目播放完成再关闭。此参数仅对音频播放器有效；视频播放器设置为 1 时不产生等待效果。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_set_event_callback

```c
int media_player_set_event_callback(void* handle, void* event_cookie, media_event_callback on_event);
```

设置事件回调，监听流状态变更。

**参数**：

- `handle` 播放器句柄.
- `event_cookie` 回调参数.
- `on_event` 事件回调函数，用于接收流状态变化通知。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_player_prepare

```c
int media_player_prepare(void* handle, const char* url, const char* options);
```

准备播放资源。

**参数**：

- `handle` 播放器句柄.
- `url` 资源路径，支持两种模式：1. URL 模式：`url` 为本地文件路径或网络地址，框架会读取并播放；2. BUFFER 模式：`url` 为 `NULL`，调用方需通过 `media_player_write_data()` 或 `media_player_get_socket()` + `write()` 持续推送数据。
- `options` 资源的额外配置参数，通常为描述资源格式的键值对（例如 `"format=s16le,sample_rate=44100,channels=2"`）。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_player_reset

```c
int media_player_reset(void* handle);
```

重置指定类型的播放器。

**参数**：

- `handle` 播放器句柄，由 `media_player_open` 返回。
- `handle` 播放器句柄.

**返回值**：

成功时返回 0，失败时返回负的错误码。


## 同步接口 - 数据流

### media_player_write_data

```c
ssize_t media_player_write_data(void* handle, const void* data, size_t len);
```

写入数据到播放器进行播放。

**参数**：

- `handle` 播放器句柄.
- `data` 缓冲区地址.
- `len` 缓冲区长度 to write.

**返回值**：

成功时返回发送的字节数，失败时返回负的错误码。


### media_player_get_sockaddr

```c
int media_player_get_sockaddr(void* handle, struct sockaddr_storage* addr);
```

获取缓冲模式的 Socket 地址信息。

**参数**：

- `handle` 播放器句柄
- `addr` Socket 地址信息。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_get_socket

```c
int media_player_get_socket(void* handle);
```

获取用于写入的 Socket 文件描述符。

**参数**：

- `handle` 播放器句柄.

**返回值**：

成功时返回 Socket 文件描述符，失败时返回负的错误码。


### media_player_close_socket

```c
void media_player_close_socket(void* handle);
```

关闭 Socket 文件描述符。

**参数**：

- `handle` 播放器句柄.


## 同步接口 - 播放控制

### media_player_start

```c
int media_player_start(void* handle);
```

开始/resume playing the re音频源。

**参数**：

- `handle` 播放器句柄.

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_player_stop

```c
int media_player_stop(void* handle);
```

停止 and clear the re音频源。

**参数**：

- `handle` 播放器句柄.

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_player_pause

```c
int media_player_pause(void* handle);
```

暂停。

**参数**：

- `handle` 播放器句柄.

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_player_seek

```c
int media_player_seek(void* handle, unsigned int position);
```

跳转 to msec 位置 from begining。

**参数**：

- `handle` 播放器句柄.
- `position` 位置，单位为毫秒。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_player_set_looping

```c
int media_player_set_looping(void* handle, int loop);
```

设置 loop times。

**参数**：

- `handle` 播放器句柄.
- `loop` 循环次数，`-1` 表示无限循环。


## 同步接口 - 状态查询

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_is_playing

```c
int media_player_is_playing(void* handle);
```

检查 playing status。

**参数**：

- `handle` 播放器句柄.

**返回值**：

int  Positive on playing, zero on in活跃状态, negative on error。


### media_player_get_position

```c
int media_player_get_position(void* handle, unsigned int* position);
```

Gert current msec 位置 of re音频源。

**参数**：

- `handle` 播放器句柄.
- `position` 位置，单位为毫秒。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_get_duration

```c
int media_player_get_duration(void* handle, unsigned int* duration);
```

Gert msec 时长 of current re音频源。

**参数**：

- `handle` 播放器句柄.
- `duration` 位置，单位为毫秒。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_get_latency

```c
int media_player_get_latency(void* handle, unsigned int* latency);
```

Gert latency of current re音频源。

**参数**：

- `handle` 播放器句柄.
- `latency` 延迟帧数。


## 同步接口 - 音量与属性

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_set_volume

```c
int media_player_set_volume(void* handle, float volume);
```

设置音量。

**参数**：

- `handle` 播放器句柄.
- `volume` 音量值，取值范围 `[0.0, 1.0]`。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_player_get_volume

```c
int media_player_get_volume(void* handle, float* volume);
```

获取音量。

**参数**：

- `handle` 播放器句柄.
- `volume` 音量值，取值范围 `[0.0, 1.0]`。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_set_property

```c
int media_player_set_property(void* handle, const char* target, const char* key, const char* value);
```

设置 properties。

**参数**：

- `handle` 播放器句柄。
- `target` 目标 filter 名称。
- `key` Key
- `value` Value

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_player_get_property

```c
int media_player_get_property(void* handle, const char* target, const char* key, char* value, int value_len);
```

获取 properties。

**参数**：

- `handle` 播放器句柄。
- `target` 目标 filter 名称。
- `key` Key
- `value` 输出缓冲区。
- `value_len` 缓冲区长度 of value


## 异步接口（基于 libuv）

以下接口仅在启用 `CONFIG_LIBUV` 时可用，回调在 `uv_loop` 上执行，避免阻塞调用线程。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_open

```c
void* media_uv_player_open(void* loop, const char* stream, media_uv_callback on_open, void* cookie);
```

打开 an async player with given 流 type。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `stream` 流类型常量。 . 不同流类型有不同的路由逻辑.
- `on_open` 打开完成后触发的回调函数。
- `cookie` 回调上下文，供 `on_open`、`on_event`、`on_connection`、`on_close` 共用。

**返回值**：

void*    Handle of player, 失败时返回 NULL。


### media_uv_player_listen

```c
int media_uv_player_listen(void* handle, media_event_callback on_event);
```

Listen to status change 事件 by setting 回调。

**参数**：

- `handle` 异步播放器句柄。
- `on_event` 事件回调函数，在收到通知后调用。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_close

```c
int media_uv_player_close(void* handle, int pending, media_uv_callback on_close);
```

关闭 the async player。

**参数**：

- `handle` 异步播放器句柄。
- `pending` 是否以 pending 方式关闭。
- `on_close` 资源释放完成后触发的回调函数。

**返回值**：

成功时返回 0，无效句柄时返回负的错误码。


### media_uv_player_prepare

```c
int media_uv_player_prepare(void* handle, const char* url, const char* options, media_uv_object_callback on_connection, media_uv_callback on_prepare, void* cookie);
```

准备 re音频源 for playing。

**参数**：

- `handle` 异步播放器句柄。
- `url` 资源路径，支持两种模式：1. URL 模式：`url` 为本地文件路径或网络地址，框架会读取并播放；2. BUFFER 模式：`url` 为 `NULL`，调用方需通过 `media_player_write_data()` 或 `media_player_get_socket()` + `write()` 持续推送数据。
- `options` 资源的额外配置参数，通常为描述资源格式的键值对（例如 `"format=s16le,sample_rate=44100,channels=2"`）。
- `on_connection` BUFFER 模式下接收 `uv_pipe_t` 的回调函数。
- `on_prepare` 结果回调函数。
- `cookie` 回调参数 for `on_prepare`.

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_player_reset

```c
int media_uv_player_reset(void* handle, media_uv_callback on_reset, void* cookie);
```

重置 player。

**参数**：

- `handle` 异步播放器句柄。
- `on_reset` 结果回调函数。
- `cookie` 回调参数 for `on_reset`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_start_auto

```c
int media_uv_player_start_auto(void* handle, const char* scenario, media_uv_callback on_start, void* cookie);
```

Play or resume the prepared 音频源 with auto 焦点 request。

**参数**：

- `handle` 异步播放器句柄。
- `scenario` 场景常量，不同场景对应不同的焦点优先级。
- `on_play` 结果确认回调（用于 request/start 操作）。
- `cookie` 回调参数 for `on_play`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_start

```c
int media_uv_player_start(void* handle, media_uv_callback on_start, void* cookie);
```

播放或恢复已准备的资源。

**参数**：

- `handle` 异步播放器句柄。
- `on_start` 结果回调函数。
- `cookie` 回调参数 for `on_start`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_pause

```c
int media_uv_player_pause(void* handle, media_uv_callback on_pause, void* cookie);
```

暂停 the playing。

**参数**：

- `handle` 异步播放器句柄。
- `on_pause` 结果回调函数。
- `cookie` 回调参数 for `on_pause`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_stop

```c
int media_uv_player_stop(void* handle, media_uv_callback on_stop, void* cookie);
```

停止 the playing, clear the prepared re音频源 file。

**参数**：

- `handle` 异步播放器句柄。
- `on_stop` 结果回调函数。
- `cookie` 回调参数 for `on_stop`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_set_volume

```c
int media_uv_player_set_volume(void* handle, float volume, media_uv_callback on_volume, void* cookie);
```

设置 player 音量。

**参数**：

- `handle` 异步播放器句柄。
- `volume` Volume in [0.0, 1.0].
- `on_volume` 结果回调函数。
- `cookie` 回调参数 for `on_volume`.

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_player_get_volume

```c
int media_uv_player_get_volume(void* handle, media_uv_float_callback on_volume, void* cookie);
```

获取 播放器 handle 音量。

**参数**：

- `handle` 异步播放器句柄。
- `volume` 音量值，取值范围 `0.0 - 1.0`。
- `on_volume` 结果回调函数。
- `cookie` 回调参数 for `on_volume`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_get_playing

```c
int media_uv_player_get_playing(void* handle, media_uv_int_callback on_playing, void* cookie);
```

获取 current playing status。

**参数**：

- `handle` 异步播放器句柄。
- `on_playing` 结果回调函数。
- `cookie` 回调参数 for `on_playing`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_get_position

```c
int media_uv_player_get_position(void* handle, media_uv_unsigned_callback on_position, void* cookie);
```

获取 current playing 位置。

**参数**：

- `handle` 异步播放器句柄。
- `on_position` 结果回调函数。
- `cookie` 回调参数 for `on_position`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_get_duration

```c
int media_uv_player_get_duration(void* handle, media_uv_unsigned_callback on_duration, void* cookie);
```

获取 时长 of current playing re音频源。

**参数**：

- `handle` 异步播放器句柄。
- `on_duration` 结果回调函数。
- `cookie` 回调参数 for `on_duration`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_get_latency

```c
int media_uv_player_get_latency(void* handle, media_uv_unsigned_callback cb, void* cookie);
```

获取 latency of current playing re音频源。

**参数**：

- `handle` 异步播放器句柄。
- `cb` 结果回调函数。
- `cookie` 回调参数 for `on_latency`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_set_looping

```c
int media_uv_player_set_looping(void* handle, int loop, media_uv_callback on_looping, void* cookie);
```

设置 the loop times。

**参数**：

- `handle` 异步播放器句柄。
- `loop` 循环次数，`-1` 表示无限循环。
- `on_looping` 结果回调函数。
- `cookie` 回调参数 for `on_looping`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_seek

```c
int media_uv_player_seek(void* handle, unsigned int position, media_uv_callback on_seek, void* cookie);
```

跳转 to msec 位置 from begining。

**参数**：

- `handle` 异步播放器句柄。
- `position` 起始位置，单位为毫秒。
- `on_seek` 结果回调函数。
- `cookie` 回调参数 for `on_seek`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_set_property

```c
int media_uv_player_set_property(void* handle, const char* target, const char* key, const char* value, media_uv_callback on_setprop, void* cookie);
```

设置 properties of 播放器 handle。

**参数**：

- `handle` 异步播放器句柄。
- `target` 目标 filter 名称。
- `key` Key
- `value` Value
- `on_setprop` 结果回调函数。
- `cookie` 回调参数 for `on_setprop`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_get_property

```c
int media_uv_player_get_property(void* handle, const char* target, const char* key, media_uv_string_callback on_getprop, void* cookie);
```

获取 properties of 播放器 handle。

**参数**：

- `handle` 异步播放器句柄。
- `target` 目标 filter 名称。
- `key` Key
- `on_getprop` 结果回调函数。
- `cookie` 回调参数 for `on_getprop`.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_player_query

```c
int media_uv_player_query(void* handle, media_uv_object_callback on_query, void* cookie);
```

Query 元数据 of 播放器 handle。

**参数**：

- `handle` 异步播放器句柄。
- `on_query` 接收元数据指针的回调函数。
- `cookie` 回调参数 for `on_query`.

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_player_close_socket

```c
int media_uv_player_close_socket(void* handle);
```

关闭 Socket 文件描述符。

**参数**：

- `handle` 播放器句柄.

**返回值**：

成功时返回 0，失败时返回负的错误码。
