# 音频焦点管理 API

音频焦点（Audio Focus）用于协调多个音频应用之间的播放优先级。当多个应用同时请求音频焦点时，系统根据场景（scenario）判断谁应当播放、谁应当停止或降低音量，并通过回调通知各应用。

头文件：`#include <media_focus.h>`

## openvela 实现说明

- **场景优先级**：通过 `scenario` 字符串标识请求类型（如 `MEDIA_SCENARIO_MUSIC`、`MEDIA_SCENARIO_NOTIFICATION` 等），框架根据场景优先级返回焦点建议
- **同步/异步双模型**：提供两组接口
    - 同步：`media_focus_*` 系列，适合简单场景
    - 异步（基于 libuv）：`media_uv_focus_*` 系列，需启用 `CONFIG_LIBUV`，适合基于 uv_loop 的应用
- **自动回复**：`request2` 接口新增 `auto_reply` 参数，为 `1` 时框架自动回复收到的建议，无需应用手动调用 `reply`
- **回调失联保护**：即使 `initial_suggestion` 返回 `MEDIA_FOCUS_STOP`（意味着立即被其他焦点抢占），框架仍会返回有效句柄，必须调用 `abandon` 释放，否则会有资源泄漏
- **新旧接口**：`media_focus_request` / `media_uv_focus_request` 已标记 deprecated，请使用带 `2` 后缀的新版本

## 焦点请求（同步）

### media_focus_request

```c
void* media_focus_request(int* initial_suggestion, const char* scenario,
                          media_focus_callback on_suggestion, void* cookie)
    __attribute__((deprecated));
```

请求音频焦点（**已废弃**，请使用 `media_focus_request2`）。

**参数**：

- `initial_suggestion` 输出参数，返回初始焦点建议，取值为 `MEDIA_FOCUS_*` 常量。
- `scenario` 场景标识字符串，取值为 `MEDIA_SCENARIO_*` 常量。
- `on_suggestion` 焦点建议变化时的回调函数。
- `cookie` 传递给回调的用户数据。

**返回值**：

成功时返回焦点句柄，失败时返回 `NULL`。

**注意**：

- 若 `initial_suggestion` 为 `MEDIA_FOCUS_STOP`，`on_suggestion` 不会被调用，但仍会返回有效句柄，调用方必须调用 `media_focus_abandon` 释放，否则会泄漏。

### media_focus_request2

```c
void* media_focus_request2(int* initial_suggestion, const char* scenario,
                           media_focus_callback2 on_suggestion,
                           int auto_reply, void* cookie);
```

请求音频焦点（推荐使用，替代 `media_focus_request`）。

**参数**：

- `initial_suggestion` 输出参数，返回初始焦点建议，取值为 `MEDIA_FOCUS_*` 常量。
- `scenario` 场景标识字符串，取值为 `MEDIA_SCENARIO_*` 常量。
- `on_suggestion` 焦点建议变化时的回调函数（新版签名包含 `req_id`）。
- `auto_reply` 是否启用自动回复：`1` 表示框架自动回复焦点建议，`0` 表示由应用手动调用 `media_focus_reply`。
- `cookie` 传递给回调的用户数据。

**返回值**：

成功时返回焦点句柄，失败时返回 `NULL`。

**注意**：

- 若 `initial_suggestion` 为 `MEDIA_FOCUS_STOP`，`on_suggestion` 不会被调用，但仍会返回有效句柄，调用方必须调用 `media_focus_abandon` 释放。

**示例**：

```c
int initial_suggestion;

context->handle = media_focus_request2(&initial_suggestion,
    MEDIA_SCENARIO_MUSIC, demo_focus_callback, 1, context);
if (!context->handle) {
    // 处理错误
}

if (initial_suggestion == MEDIA_FOCUS_STOP)
    media_focus_abandon(context->handle);
```

### media_focus_abandon

```c
int media_focus_abandon(void* handle);
```

释放音频焦点。

**参数**：

- `handle` 待释放的焦点句柄。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### media_focus_reply

```c
int media_focus_reply(void* handle, int req_id);
```

回复焦点请求。当 `request2` 的 `auto_reply` 为 `0` 时使用，手动确认焦点建议。

**参数**：

- `handle` 焦点句柄。
- `req_id` 请求 ID，由焦点建议回调传入。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。

## 焦点请求（异步，基于 libuv）

以下接口仅在启用 `CONFIG_LIBUV` 时可用。

### media_uv_focus_request

```c
void* media_uv_focus_request(void* loop, const char* scenario,
                             media_focus_callback on_suggestion, void* cookie)
    __attribute__((deprecated));
```

异步请求音频焦点（**已废弃**，请使用 `media_uv_focus_request2`）。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环。
- `scenario` 场景标识字符串，取值为 `MEDIA_SCENARIO_*` 常量。
- `on_suggestion` 焦点建议变化时的回调函数。
- `cookie` 传递给回调的用户数据。

**返回值**：

成功时返回异步焦点句柄，失败时返回 `NULL`。

**注意**：

- 当 `on_suggestion` 回调收到 `MEDIA_FOCUS_STOP` 时，应用应调用 `media_uv_focus_abandon` 释放句柄。

### media_uv_focus_request2

```c
void* media_uv_focus_request2(void* loop, const char* scenario,
                              media_focus_callback2 on_suggestion,
                              int auto_reply, void* cookie);
```

异步请求音频焦点（推荐使用，替代 `media_uv_focus_request`）。

**参数**：

- `loop` 当前线程的 `uv_loop_t*` 事件循环。
- `scenario` 场景标识字符串，取值为 `MEDIA_SCENARIO_*` 常量。
- `on_suggestion` 焦点建议变化时的回调函数（新版签名包含 `req_id`）。
- `auto_reply` 是否启用自动回复：`1` 表示框架自动回复焦点建议。
- `cookie` 传递给回调的用户数据。

**返回值**：

成功时返回异步焦点句柄，失败时返回 `NULL`。

**示例**：

```c
void user_on_suggestion(int suggestion, int req_id, void* cookie) {
    UserContext* ctx = cookie;
    switch (suggestion) {
    case MEDIA_FOCUS_STOP:
        media_uv_focus_abandon(ctx->handle, NULL);
        break;
    }
}

ctx->handle = media_uv_focus_request2(loop, MEDIA_SCENARIO_MUSIC,
    user_on_suggestion, 1, ctx);
```

### media_uv_focus_abandon

```c
int media_uv_focus_abandon(void* handle, media_uv_callback on_abandon);
```

异步释放音频焦点。

**参数**：

- `handle` 异步焦点句柄。
- `on_abandon` 释放完成后的回调，通常用于释放 cookie。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。

### media_uv_focus_reply

```c
int media_uv_focus_reply(void* handle, int req_id);
```

异步回复焦点请求。当 `request2` 的 `auto_reply` 为 `0` 时使用。

**参数**：

- `handle` 异步焦点句柄。
- `req_id` 请求 ID。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。

## 调试接口

### media_focus_dump

```c
void media_focus_dump(const char* options);
```

转储焦点栈信息用于调试。

**参数**：

- `options` 转储选项（目前未使用）。

**注意**：

- 该接口将来会并入统一的 `media_dump()`。
