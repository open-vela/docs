# Telephony SIM Toolkit (STK) API

SIM Application Toolkit（STK / CAT）是运营商在 SIM 卡上预置的交互菜单与事件处理能力，常见用途包括运营商增值菜单、服务密码管理、URL 浏览器启动等。

头文件：`#include <tapi_stk.h>`

## openvela 实现说明

- **Agent 模式**：应用侧作为"STK Agent"注册到 TAPI，SIM 卡主动发起的显示/输入/确认请求通过 Agent 回调触达应用
- **注册层级**：支持 per-slot Agent（通过 `tapi_stk_agent_register`）与 default Agent（系统默认 UI）
- **主菜单**：`tapi_stk_get_main_menu*` 查询 SIM 卡提供的主菜单结构
- **Proactive Command 响应**：`tapi_stk_handle_agent_*` 系列接口用于将 Agent 对 SIM 卡主动命令的响应回传给 SIM
- **多卡支持**：所有接口带 `slot_id`

## Agent 注册

### tapi_stk_agent_register

```c
int tapi_stk_agent_register(tapi_context context, int slot_id,
                            char* agent_id, tapi_async_function p_handle);
```

为指定 SIM 卡槽注册 STK Agent。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `agent_id` Agent 标识字符串。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_agent_unregister

```c
int tapi_stk_agent_unregister(tapi_context context, int slot_id,
                              char* agent_id, tapi_async_function p_handle);
```

取消 STK Agent 注册。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `agent_id` Agent 标识字符串。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_default_agent_register

```c
int tapi_stk_default_agent_register(tapi_context context, int slot_id,
                                    char* agent_id, tapi_async_function p_handle);
```

注册为默认 STK Agent（全局 fallback）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `agent_id` Agent 标识字符串。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_default_agent_unregister

```c
int tapi_stk_default_agent_unregister(tapi_context context, int slot_id,
                                      tapi_async_function p_handle);
```

取消默认 STK Agent 注册。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_agent_interface_register

```c
int tapi_stk_agent_interface_register(tapi_context context, int slot_id, char* agent_id,
                                      tapi_stk_agent_interface* iface);
```

在 Agent 层注册具体的接口实现（回调函数集合）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `agent_id` Agent 标识字符串。
- `iface` Agent 接口回调结构体指针。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_agent_interface_unregister

```c
int tapi_stk_agent_interface_unregister(tapi_context context, char* agent_id);
```

注销 Agent 接口实现。

**参数**：

- `context` Telephony 上下文句柄。
- `agent_id` Agent 标识字符串。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_default_agent_interface_register

```c
int tapi_stk_default_agent_interface_register(tapi_context context, int slot_id,
                                              tapi_stk_agent_interface* iface);
```

为默认 Agent 注册接口实现。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `iface` Agent 接口回调结构体指针。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_default_agent_interface_unregister

```c
int tapi_stk_default_agent_interface_unregister(tapi_context context, int slot_id);
```

注销默认 Agent 的接口实现。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## 主菜单与空闲模式

### tapi_stk_select_item

```c
int tapi_stk_select_item(tapi_context context, int slot_id,
                         int item_idx, tapi_async_function p_handle);
```

选择主菜单中的某个条目，触发 SIM 卡的业务响应。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `item_idx` 条目索引。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_get_idle_mode_text

```c
int tapi_stk_get_idle_mode_text(tapi_context context, int slot_id, char** text);
```

查询 SIM 卡设定的空闲模式显示文本。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `text` 输出参数，返回文本字符串。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_get_idle_mode_icon

```c
int tapi_stk_get_idle_mode_icon(tapi_context context, int slot_id, char** icon);
```

查询 SIM 卡设定的空闲模式图标标识。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `icon` 输出参数，返回图标标识字符串。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_get_main_menu

```c
int tapi_stk_get_main_menu(tapi_context context, int slot_id, int* length,
                           tapi_stk_menu_item out[]);
```

获取 SIM 卡提供的主菜单条目列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `length` 输入输出参数：入参表示缓冲区容量，出参返回实际条目数。
- `out` 输出缓冲区，接收菜单条目数组。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_get_main_menu_title

```c
int tapi_stk_get_main_menu_title(tapi_context context, int slot_id, char** title);
```

查询主菜单标题。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `title` 输出参数，返回标题字符串。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_get_main_menu_icon

```c
int tapi_stk_get_main_menu_icon(tapi_context context, int slot_id, int* icon);
```

查询主菜单图标编号。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `icon` 输出参数，返回图标编号。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## Agent 响应处理

以下接口由 Agent 实现使用，用于向 SIM 卡回传 proactive command 的响应。所有接口成功时返回 `0`，失败时返回负的错误码。

### tapi_stk_handle_agent_request_selection

```c
int tapi_stk_handle_agent_request_selection(tapi_context context, int slot_id,
                                            char* agent_id, int selection,
                                            tapi_async_function p_handle);
```

处理 SIM 卡的菜单项选择请求，回传用户选中的条目索引。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `agent_id` Agent 标识字符串。
- `selection` 用户选中的条目索引。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_display_text

```c
int tapi_stk_handle_agent_display_text(tapi_context context, int slot_id,
                                       char* agent_id, int result,
                                       tapi_async_function p_handle);
```

响应 SIM 卡的文本显示请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `result` 显示操作结果（用户是否确认等）。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_request_input

```c
int tapi_stk_handle_agent_request_input(tapi_context context, int slot_id,
                                        char* agent_id, char* input,
                                        tapi_async_function p_handle);
```

响应 SIM 卡的字符串输入请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `input` 用户输入的字符串。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_request_digits

```c
int tapi_stk_handle_agent_request_digits(tapi_context context, int slot_id,
                                         char* agent_id, char* digits,
                                         tapi_async_function p_handle);
```

响应 SIM 卡的数字序列输入请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `digits` 用户输入的数字序列。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_request_key

```c
int tapi_stk_handle_agent_request_key(tapi_context context, int slot_id,
                                      char* agent_id, char key,
                                      tapi_async_function p_handle);
```

响应 SIM 卡的单键输入请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `key` 用户输入的按键字符。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_request_digit

```c
int tapi_stk_handle_agent_request_digit(tapi_context context, int slot_id,
                                        char* agent_id, char digit,
                                        tapi_async_function p_handle);
```

响应 SIM 卡的单数字输入请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `digit` 用户输入的单个数字字符。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_request_quick_digit

```c
int tapi_stk_handle_agent_request_quick_digit(tapi_context context, int slot_id,
                                              char* agent_id, char digit,
                                              tapi_async_function p_handle);
```

响应 SIM 卡的快速数字输入请求（无需回显）。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `digit` 用户输入的单个数字字符。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_request_confirmation

```c
int tapi_stk_handle_agent_request_confirmation(tapi_context context, int slot_id,
                                               char* agent_id, bool confirmed,
                                               tapi_async_function p_handle);
```

响应 SIM 卡的确认/取消类请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `confirmed` 用户是否确认。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_confirm_call_setup

```c
int tapi_stk_handle_agent_confirm_call_setup(tapi_context context, int slot_id,
                                             char* agent_id, bool confirmed,
                                             tapi_async_function p_handle);
```

响应 SIM 卡发起的 call-setup 确认请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `confirmed` 用户是否确认拨出。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_play_tone

```c
int tapi_stk_handle_agent_play_tone(tapi_context context, int slot_id,
                                    char* agent_id, int result,
                                    tapi_async_function p_handle);
```

响应 SIM 卡的播放提示音请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `result` 播放结果。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_loop_tone

```c
int tapi_stk_handle_agent_loop_tone(tapi_context context, int slot_id,
                                    char* agent_id, int result,
                                    tapi_async_function p_handle);
```

响应 SIM 卡的循环提示音请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `result` 播放结果。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_display_action_information

```c
int tapi_stk_handle_agent_display_action_information(tapi_context context, int slot_id,
                                                     char* agent_id, int result,
                                                     tapi_async_function p_handle);
```

响应 SIM 卡的动作进度信息显示请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `result` 显示操作结果。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_confirm_launch_browser

```c
int tapi_stk_handle_agent_confirm_launch_browser(tapi_context context, int slot_id,
                                                 char* agent_id, bool confirmed,
                                                 tapi_async_function p_handle);
```

响应 SIM 卡的浏览器启动确认请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `confirmed` 用户是否确认启动浏览器。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_display_action

```c
int tapi_stk_handle_agent_display_action(tapi_context context, int slot_id,
                                         char* agent_id, int result,
                                         tapi_async_function p_handle);
```

响应 SIM 卡的动作状态更新请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `result` 操作结果。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


### tapi_stk_handle_agent_confirm_open_channel

```c
int tapi_stk_handle_agent_confirm_open_channel(tapi_context context, int slot_id,
                                               char* agent_id, bool confirmed,
                                               tapi_async_function p_handle);
```

响应 SIM 卡发起的打开数据通道确认请求。

**参数**：

- `context` / `slot_id` / `agent_id` 同上。
- `confirmed` 用户是否确认打开通道。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。


