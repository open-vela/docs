# 媒体会话 API

媒体播放控制和状态同步，支持控制器-被控端模式。

头文件：`#include <media_session.h>`

## openvela 实现说明

- **控制器-被控端模式**：支持两种角色
    - 控制器（Controller）：通过 `media_session_open` 打开，向当前活跃媒体发送播放控制命令
    - 被控端（Controllee）：通过 `media_session_register` 注册，接收控制命令并上报状态
- **同步/异步双模型**：`media_session_*`（同步）和 `media_uv_session_*`（异步，基于 libuv）
- **控制命令**：start / stop / pause / seek / prev_song / next_song / volume 等
- **状态查询**：控制器可查询当前播放状态、位置、时长、音量等
- **状态通知**：被控端通过 `notify` / `update` 向控制器推送播放状态变化

## 控制器接口 - 生命周期

### media_session_open

```c
void* media_session_open(const char* params);
```

打开媒体会话控制器。

**参数**：

- `params` NULL, 暂未使用.

**返回值**：

void*    控制器句柄, 失败时返回 NULL。


### media_session_close

```c
int media_session_close(void* handle);
```

关闭媒体会话控制器。

**参数**：

- `handle` 控制器句柄

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_set_event_callback

```c
int media_session_set_event_callback(void* handle, void* cookie, media_event_callback on_event);
```

设置事件回调，接收被控端消息。

**参数**：

- `handle` 控制器句柄
- `cookie` 回调参数 for `on_event`.
- `on_event` 事件回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


## 控制器接口 - 播放控制

### media_session_start

```c
int media_session_start(void* handle);
```

请求开始播放。

**参数**：

- `handle` 控制器句柄.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_stop

```c
int media_session_stop(void* handle);
```

请求停止播放。

**参数**：

- `handle` 控制器句柄.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_pause

```c
int media_session_pause(void* handle);
```

请求暂停播放。

**参数**：

- `handle` 控制器句柄.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_seek

```c
int media_session_seek(void* handle, unsigned position);
```

请求跳转到指定位置。

**参数**：

- `handle` 控制器句柄.
- `position` 起始位置，单位为毫秒。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_prev_song

```c
int media_session_prev_song(void* handle);
```

请求播放上一首。

**参数**：

- `handle` 控制器句柄.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_next_song

```c
int media_session_next_song(void* handle);
```

请求播放下一首。

**参数**：

- `handle` 控制器句柄.


## 控制器接口 - 音量控制

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_increase_volume

```c
int media_session_increase_volume(void* handle);
```

请求 increase 音量。

**参数**：

- `handle` 控制器句柄.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_decrease_volume

```c
int media_session_decrease_volume(void* handle);
```

请求 decrease 音量。

**参数**：

- `handle` 控制器句柄.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_set_volume

```c
int media_session_set_volume(void* handle, int volume);
```

Rquest set 音量。

**参数**：

- `handle` 控制器句柄.
- `volume` 音量档位。

**返回值**：

成功时返回 0，失败时返回负的错误码。


## 控制器接口 - 状态查询

### media_session_query

```c
int media_session_query(void* handle, const media_metadata_t** data);
```

Query 元数据 from most 活跃状态 controllee。

**参数**：

- `handle` 控制器句柄.
- `data` 用于接收元数据指针的输出指针。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_session_get_state

```c
int media_session_get_state(void* handle, int* state);
```

获取 all status。

**参数**：

- `handle` 控制器句柄.
- `state` 当前状态。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_session_get_position

```c
int media_session_get_position(void* handle, unsigned* position);
```

获取 msec 位置。

**参数**：

- `handle` 控制器句柄.
- `position` 当前位置，单位为毫秒。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_session_get_duration

```c
int media_session_get_duration(void* handle, unsigned* duration);
```

获取 msec 时长。

**参数**：

- `handle` 控制器句柄.
- `duration` 当前总时长，单位为毫秒。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_session_get_volume

```c
int media_session_get_volume(void* handle, int* volume);
```

获取 current 音量 index。

**参数**：

- `handle` 控制器句柄.
- `volume` 音量档位。

**返回值**：

成功时返回 0，失败时返回负的错误码。


## 被控端接口

### media_session_register

```c
void* media_session_register(void* cookie, media_event_callback on_event);
```

注册 as a session controllee。

**参数**：

- `cookie` Callback arguemnt of `on_event`.
- `on_event` 事件回调函数。.

**返回值**：

成功时返回被控端句柄，失败时返回 NULL。


### media_session_unregister

```c
int media_session_unregister(void* handle);
```

取消注册 会话 controllee。

**参数**：

- `handle` 被控端句柄。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_notify

```c
int media_session_notify(void* handle, int event, int result, const char* extra);
```

通知 the result of control message. * After receive MEDIA_EVENT_* from `on_事件`, as controllee you should do something to handle the control message, after you acknowledge the control message, you should call this api to send response to 控制器。

**参数**：

- `handle` 被控端句柄。
- `event` MEDIA_EVENT_*
- `result` 操作结果，成功时为 `0`，失败时为负的 errno。
- `extra` 附加消息。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_session_update

```c
int media_session_update(void* handle, const media_metadata_t* data);
```

Update 元数据 to session。

**参数**：

- `handle` 被控端句柄。
- `data` 要更新的元数据。


## 异步接口（基于 libuv）

以下接口仅在启用 `CONFIG_LIBUV` 时可用，控制器与被控端均有对应异步版本。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_open

```c
void* media_uv_session_open(void* loop, char* params, media_uv_callback on_open, void* cookie);
```

打开 an async session controller。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `params` 暂未使用.
- `on_open` 打开完成后触发的回调函数。
- `cookie` 回调上下文，供 `on_open`、`on_event`、`on_close` 共用。

**返回值**：

成功时返回异步控制器句柄。


### media_uv_session_close

```c
int media_uv_session_close(void* handle, media_uv_callback on_close);
```

关闭 the async controller handle。

**参数**：

- `handle` 待销毁的异步控制器句柄。
- `on_close` 关闭完成后触发的回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_session_listen

```c
int media_uv_session_listen(void* handle, media_event_callback on_event);
```

Listen to the 事件s from controllee。

**参数**：

- `handle` Async 控制器句柄.
- `on_event` 事件回调函数。.

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_session_start

```c
int media_uv_session_start(void* handle, media_uv_callback on_start, void* cookie);
```

请求开始播放。

**参数**：

- `handle` Async 控制器句柄.
- `on_start` 结果回调函数。
- `cookie` 回调参数 of `on_start`

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_stop

```c
int media_uv_session_stop(void* handle, media_uv_callback on_stop, void* cookie);
```

请求停止播放。

**参数**：

- `handle` Async 控制器句柄.
- `on_stop` 结果回调函数。
- `cookie` 回调参数 of `on_stop`

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_pause

```c
int media_uv_session_pause(void* handle, media_uv_callback on_pause, void* cookie);
```

请求暂停播放。

**参数**：

- `handle` Async 控制器句柄.
- `on_pause` 结果回调函数。
- `cookie` 回调参数 of `on_pause`

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_seek

```c
int media_uv_session_seek(void* handle, unsigned position, media_uv_callback on_seek, void* cookie);
```

请求跳转到指定位置。

**参数**：

- `handle` 播放器句柄。
- `position` 起始位置，单位为毫秒。
- `on_seek` 结果回调函数。
- `cookie` 回调参数 of `on_seek`

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_prev_song

```c
int media_uv_session_prev_song(void* handle, media_uv_callback on_pre_song, void* cookie);
```

请求播放上一首。

**参数**：

- `handle` Async 控制器句柄.
- `on_prev` 结果回调函数。
- `cookie` 回调参数 of `on_prev`

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_next_song

```c
int media_uv_session_next_song(void* handle, media_uv_callback on_next, void* cookie);
```

请求播放下一首。

**参数**：

- `handle` Async 控制器句柄.
- `on_next` 结果回调函数。
- `cookie` 回调参数 of `on_next`

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_increase_volume

```c
int media_uv_session_increase_volume(void* handle, media_uv_callback on_increase, void* cookie);
```

请求 increase 音量。

**参数**：

- `handle` 异步控制器句柄。
- `on_increase` 结果回调函数。
- `cookie` 回调参数 of `on_increase`

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_decrease_volume

```c
int media_uv_session_decrease_volume(void* handle, media_uv_callback on_decrease, void* cookie);
```

请求 decrease 音量。

**参数**：

- `handle` 异步控制器句柄。
- `on_decrease` 结果回调函数。
- `cookie` 回调参数 of `on_decrease`

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_set_volume

```c
int media_uv_session_set_volume(void* handle, int volume, media_uv_callback on_set_volume, void* cookie);
```

请求设置音量。

**参数**：

- `handle` 异步控制器句柄。
- `Volume` 音量档位。
- `on_volume` 结果回调函数。
- `cookie` 回调参数 of `on_volume`

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_session_query

```c
int media_uv_session_query(void* handle, media_uv_object_callback on_query, void* cookie);
```

查询完整状态信息。

**参数**：

- `handle` 异步控制器句柄。
- `on_query` 接收元数据指针的回调函数。
- `cookie` 回调参数.

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_session_get_state

```c
int media_uv_session_get_state(void* handle, media_uv_int_callback on_state, void* cookie);
```

获取 current state。

**参数**：

- `handle` Async 控制器句柄.
- `on_state` 结果回调函数。
- `cookie` 回调参数 of `on_state`

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_session_get_position

```c
int media_uv_session_get_position(void* handle, media_uv_unsigned_callback on_position, void* cookie);
```

获取当前播放位置。

**参数**：

- `handle` 异步控制器句柄。
- `on_position` 结果回调函数。
- `cookie` 回调参数 of `on_position`

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_session_get_duration

```c
int media_uv_session_get_duration(void* handle, media_uv_unsigned_callback on_duration, void* cookie);
```

获取 current 时长。

**参数**：

- `handle` 异步控制器句柄。
- `on_duration` 结果回调函数。
- `cookie` 回调参数 of `on_duration`

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_session_get_volume

```c
int media_uv_session_get_volume(void* handle, media_uv_int_callback on_get_volume, void* cookie);
```

获取 current 音量。

**参数**：

- `handle` 异步控制器句柄。
- `on_volume` 结果回调函数。
- `cookie` 回调参数 of `on_volume`

**返回值**：

成功时返回 0，失败时返回负的错误码。


### media_uv_session_register

```c
void* media_uv_session_register(void* loop, const char* params, media_event_callback on_event, void* cookie);
```

注册 as a session controllee to receive control message。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环句柄。
- `params` 未使用，请传 `NULL`。
- `on_event` 接收控制消息的回调函数。
- `cookie` 回调参数.

**返回值**：

void*    Async controlee handle, 失败时返回 NULL。


### media_uv_session_unregister

```c
int media_uv_session_unregister(void* handle, media_uv_callback on_release);
```

取消注册 self。

**参数**：

- `handle` 异步被控端句柄。
- `on_release` 调用方资源释放回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_notify

```c
int media_uv_session_notify(void* handle, int event, int result, const char* extra, media_uv_callback on_notify, void* cookie);
```

通知 the result of control message. * After receive MEDIA_EVENT_* from `on_事件`, as controllee you should do something to handle the control message, after you acknowledge the control message, you should call this api to send response to 控制器。

**参数**：

- `handle` 异步被控端句柄。
- `event` 要通知的事件。
- `result` 事件结果，成功时通常为 `0`，失败时为负的 errno。
- `extra` 事件的附加字符串消息，不需要时传 `NULL`。
- `on_notify` 通知确认回调函数。
- `cookie` 回调参数.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


### media_uv_session_update

```c
int media_uv_session_update(void* handle, const media_metadata_t* data, media_uv_callback on_update, void* cookie);
```

Update 元数据 to session。

**参数**：

- `handle` 异步被控端句柄。
- `data` 要更新的元数据。
- `on_update` 更新确认回调函数。
- `cookie` 回调参数.

**返回值**：

成功时返回 `0`，失败时返回负的 errno。


