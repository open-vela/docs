\[ [English](../../../../en/api/framework/media/media_recorder.md) | 简体中文 \]

# 多媒体录制器 API

音视频录制功能，支持文件录制和缓冲模式。

头文件：`#include <media_recorder.h>`

## openvela 实现说明

- **同步/异步双模型**：`media_recorder_*`（同步）和 `media_uv_recorder_*`（异步，基于 libuv）
- **输出方式**：支持两种目标
    - 本地文件：通过 `prepare(url)` 指定路径
    - 字节流缓冲：通过 `read_data` 读取，或 `get_socket` 获取底层套接字
- **拍照**：除音视频录制外，提供 `take_picture` / `start_picture` / `finish_picture` 图片捕获接口
- **事件回调**：通过 `set_event_callback` 注册事件监听器

## 同步接口 - 生命周期

### media_recorder_open

```c
void* media_recorder_open(const char* params);
```

打开指定源类型的录制器。

**参数**：

- `params` 源类型常量，通常为 `MEDIA_SOURCE_MIC`。

**返回值**：

成功时返回录制器句柄，失败时返回 `NULL`。


### media_recorder_close

```c
int media_recorder_close(void* handle);
```

关闭录制器。

**参数**：

- `handle` 录制器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_recorder_set_event_callback

```c
int media_recorder_set_event_callback(void* handle, void* cookie, media_event_callback event_cb);
```

设置录制器事件回调，当状态变化或发生用户关注的事件时触发回调。

**参数**：

- `handle` 录制器句柄。
- `cookie` 用户数据，在 `event_cb` 触发时回传给用户。
- `event_cb` 事件回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_recorder_prepare

```c
int media_recorder_prepare(void* handle, const char* url, const char* options);
```

准备录制器。

**参数**：

- `handle` 录制器句柄。
- `url` 资源路径，支持两种模式：1. URL 模式：`url` 为本地文件路径，框架会打开并录制到该路径；2. BUFFER 模式：`url` 为 `NULL`，调用方需通过 `media_recorder_read_data()` 或 `media_recorder_get_socket()` + `read()` 持续接收数据。
- `options` 额外配置参数，字段包括：format（封装格式，如 opus/wav）、sample_rate（采样率）、ch_layout（声道布局）、b（比特率，如 `"23900"`）、vbr（0=固定码率，1=可变码率）、level（编码复杂度，0-10，默认 10）。示例：`"format=opusraw:sample_rate=16000:ch_layout=mono:b=32000:vbr=0:level=1"`。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_recorder_reset

```c
int media_recorder_reset(void* handle);
```

重置录制器到初始状态。

**参数**：

- `handle` 录制器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


## 同步接口 - 数据流

### media_recorder_read_data

```c
ssize_t media_recorder_read_data(void* handle, void* data, size_t len);
```

从录制器读取录制数据。

**参数**：

- `handle` 录制器句柄。
- `data` 数据缓冲区地址。
- `len` 要读取的数据长度（字节）。

**返回值**：

成功时返回读取的字节数，失败时返回负的错误码。


### media_recorder_get_sockaddr

```c
int media_recorder_get_sockaddr(void* handle, struct sockaddr_storage* addr);
```

获取缓冲模式的 Socket 地址信息。

**参数**：

- `handle` 录制器句柄。
- `addr` 用于存储 Socket 地址信息的输出参数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_recorder_get_socket

```c
int media_recorder_get_socket(void* handle);
```

获取用于读取的 Socket 文件描述符。

**参数**：

- `handle` 录制器句柄。

**返回值**：

成功时返回 Socket 文件描述符，失败时返回负的错误码。


### media_recorder_close_socket

```c
void media_recorder_close_socket(void* handle);
```

关闭录制器数据接收完成后的 Socket 文件描述符。

**参数**：

- `handle` 录制器句柄。


## 同步接口 - 录制控制

### media_recorder_start

```c
int media_recorder_start(void* handle);
```

开始或恢复录制。

**参数**：

- `handle` 录制器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_recorder_pause

```c
int media_recorder_pause(void* handle);
```

暂停录制。

**参数**：

- `handle` 录制器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### media_recorder_stop

```c
int media_recorder_stop(void* handle);
```

停止录制。

**参数**：

- `handle` 录制器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


## 同步接口 - 属性

### media_recorder_set_property

```c
int media_recorder_set_property(void* handle, const char* target, const char* key, const char* value);
```

设置录制器属性。

**参数**：

- `handle` 录制器句柄。
- `target` 目标 filter 名称。
- `key` 属性键名。
- `value` 属性值。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_recorder_get_property

```c
int media_recorder_get_property(void* handle, const char* target, const char* key, char* value, int value_len);
```

获取录制器属性。

**参数**：

- `handle` 录制器句柄。
- `target` 目标 filter 名称。
- `key` 属性键名。
- `value` 输出缓冲区，用于存储属性值。
- `value_len` 输出缓冲区长度。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


## 同步接口 - 图片捕获

### media_recorder_take_picture

```c
int media_recorder_take_picture(char* params, char* filename, size_t number);
```

从摄像头拍照。

**参数**：

- `params` 相机打开路径参数。
- `filename` 新图片的存储路径。
- `number` 拍摄图片的数量。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_recorder_start_picture

```c
void* media_recorder_start_picture(char* params, char* filename, size_t number, media_event_callback event_cb, void* cookie);
```

开始拍照，内部依次执行打开、设置事件回调、准备和启动操作。

**参数**：

- `params` 打开参数。
- `filename` 新图片的存储路径。
- `number` 拍摄图片的数量。
- `event_cb` 处理状态反馈的回调函数。
- `cookie` 用户私有数据。

**返回值**：

成功时返回有效句柄，失败时返回 `NULL`。


### media_recorder_finish_picture

```c
int media_recorder_finish_picture(void* handle);
```

拍照完成后关闭录制器。

**参数**：

- `handle` 由 `media_recorder_start_picture()` 返回的录制器句柄。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


## 异步接口（基于 libuv）

以下接口仅在启用 `CONFIG_LIBUV` 时可用。

### media_uv_recorder_open

```c
void* media_uv_recorder_open(void* loop, const char* source, media_uv_callback on_open, void* cookie);
```

打开异步录制器。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `source` 源类型。
- `on_open` 打开完成后触发的回调函数。
- `cookie` 回调上下文，供 `on_open`、`on_event`、`on_close` 共用。

**返回值**：

成功时返回录制器句柄，失败时返回 `NULL`。


### media_uv_recorder_listen

```c
int media_uv_recorder_listen(void* handle, media_event_callback on_event);
```

注册事件监听回调，接收录制状态变化通知。

**参数**：

- `handle` 异步录制器句柄。
- `on_event` 事件回调函数，在收到通知后调用。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_recorder_close

```c
int media_uv_recorder_close(void* handle, media_uv_callback on_close);
```

关闭异步录制器。

**参数**：

- `handle` 异步录制器句柄。
- `on_close` 资源释放完成后触发的回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_recorder_prepare

```c
int media_uv_recorder_prepare(void* handle, const char* url, const char* options, media_uv_object_callback on_connection, media_uv_callback on_prepare, void* cookie);
```

准备录制目标文件。

**参数**：

- `handle` 异步录制器句柄。
- `url` 目标路径。
- `options` 目标配置参数，详见 `media_recorder_prepare`。
- `on_connection` BUFFER 模式下接收可写入数据的 `uv_pipe_t` 的回调函数。
- `on_prepare` 准备完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_recorder_start_auto

```c
int media_uv_recorder_start_auto(void* handle, const char* stream, media_uv_callback on_start, void* cookie);
```

开始或恢复录制，并自动请求音频焦点。

**参数**：

- `handle` 异步录制器句柄。
- `scenario` 场景常量（定义在 `media_defs.h` 中）。
- `on_start` 录制开始后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_recorder_start

```c
int media_uv_recorder_start(void* handle, media_uv_callback on_start, void* cookie);
```

开始或恢复录制。

**参数**：

- `handle` 异步录制器句柄。
- `on_start` 录制开始后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_recorder_pause

```c
int media_uv_recorder_pause(void* handle, media_uv_callback on_pause, void* cookie);
```

暂停录制。

**参数**：

- `handle` 异步录制器句柄。
- `on_pause` 暂停完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_recorder_stop

```c
int media_uv_recorder_stop(void* handle, media_uv_callback on_stop, void* cookie);
```

停止录制并完成目标文件写入。

**参数**：

- `handle` 异步录制器句柄。
- `on_stop` 停止完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_recorder_set_property

```c
int media_uv_recorder_set_property(void* handle, const char* target, const char* key, const char* value, media_uv_callback cb, void* cookie);
```

设置录制器属性。

**参数**：

- `handle` 异步录制器句柄。
- `target` 目标 filter 名称。
- `key` 属性键名。
- `value` 属性值。
- `cb` 设置完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_recorder_get_property

```c
int media_uv_recorder_get_property(void* handle, const char* target, const char* key, media_uv_string_callback cb, void* cookie);
```

获取录制器属性。

**参数**：

- `handle` 异步录制器句柄。
- `target` 目标 filter 名称。
- `key` 属性键名。
- `cb` 结果回调函数，回调参数为属性值字符串。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_recorder_reset

```c
int media_uv_recorder_reset(void* handle, media_uv_callback on_reset, void* cookie);
```

重置录制器，清除当前录制内容以准备新的录制。

**参数**：

- `handle` 异步录制器句柄。
- `on_reset` 重置完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_recorder_take_picture

```c
int media_uv_recorder_take_picture(void* loop, char* params, char* filename, size_t number, media_uv_callback on_complete, void* cookie);
```

从摄像头异步拍照。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `params` 相机打开路径参数。
- `filename` 新图片的存储路径。
- `number` 拍摄图片的数量。
- `on_complete` 拍照完成后的结果回调函数。
- `cookie` 回调上下文参数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。
