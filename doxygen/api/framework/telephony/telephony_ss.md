# Telephony 补充业务（SS）API

Supplementary Services（补充业务）是 3GPP 蜂窝标准定义的增值通话能力，包括呼叫限制（Call Barring）、呼叫转移（Call Forwarding）、主叫识别（CLIR/CLIP）、呼叫等待、USSD 等。

头文件：`#include <tapi_ss.h>`

## openvela 实现说明

- **呼叫限制 Call Barring**：`tapi_ss_*_call_barring*` 系列控制拨出/拨入的号码范围
- **呼叫转移 Call Forwarding**：`tapi_ss_*_call_forwarding*` 系列配置无条件/忙/无应答/不可达四种转移
- **CLIR/CLIP**：主叫号码显示与限制，通过 `calling_line_restriction` 和 `calling_line_presentation_info` 接口
- **USSD**：`tapi_ss_send_ussd` 发送 `*#xxxx#` 命令，`tapi_ss_cancel_ussd` 取消会话
- **FDN**：固定拨号开关通过 `tapi_ss_enable_fdn` / `tapi_ss_query_fdn`
- **多卡支持**：所有接口带 `slot_id`
- **异步回调**：所有操作使用 `tapi_async_function`

## 呼叫限制

### tapi_ss_request_call_barring

```c
int tapi_ss_request_call_barring(tapi_context context, int slot_id, int event_id,
                                 char* fac, char* pin2,
                                 tapi_async_function p_handle);
```

请求某类呼叫限制（按 FAC 编码）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `fac` 呼叫限制 FAC 码（如 `"OI"`、`"IR"` 等）。
- `pin2` SIM 卡 PIN2 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_set_call_barring_option

```c
int tapi_ss_set_call_barring_option(tapi_context context, int slot_id, int event_id,
                                    char* facility, char* pin2,
                                    tapi_async_function p_handle);
```

设置呼叫限制选项。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `facility` 限制类型字符串。
- `pin2` SIM 卡 PIN2 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_get_call_barring_option

```c
int tapi_ss_get_call_barring_option(tapi_context context, int slot_id,
                                    const char* service_type, char** out);
```

查询当前呼叫限制配置。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `service_type` 服务类型字符串。
- `out` 输出参数，返回配置字符串。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_change_call_barring_password

```c
int tapi_ss_change_call_barring_password(tapi_context context, int slot_id, int event_id,
                                         char* old_pin, char* new_pin,
                                         tapi_async_function p_handle);
```

修改呼叫限制服务的密码。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `old_pin` 旧密码。
- `new_pin` 新密码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_disable_all_call_barrings

```c
int tapi_ss_disable_all_call_barrings(tapi_context context, int slot_id, int event_id,
                                      char* passwd, tapi_async_function p_handle);
```

关闭所有呼叫限制。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `passwd` 服务密码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_disable_all_incoming

```c
int tapi_ss_disable_all_incoming(tapi_context context, int slot_id,
                                 int event_id, char* passwd,
                                 tapi_async_function p_handle);
```

关闭所有入呼限制。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `passwd` 服务密码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_disable_all_outgoing

```c
int tapi_ss_disable_all_outgoing(tapi_context context, int slot_id,
                                 int event_id, char* passwd,
                                 tapi_async_function p_handle);
```

关闭所有出呼限制。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `passwd` 服务密码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## 呼叫转移

### tapi_ss_query_call_forwarding_option

```c
int tapi_ss_query_call_forwarding_option(tapi_context context, int slot_id, int event_id,
                                         int cf_reason, tapi_async_function p_handle);
```

查询呼叫转移配置。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `cf_reason` 转移类型（无条件/忙/无应答/不可达，详见 `tapi_call_forward_option`）。
- `p_handle` 异步回调函数，回调时返回 `tapi_call_forwarding_info`。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_set_call_forwarding_option

```c
int tapi_ss_set_call_forwarding_option(tapi_context context, int slot_id, int event_id,
                                       tapi_call_forwarding_info* info,
                                       tapi_async_function p_handle);
```

设置呼叫转移配置。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `info` 呼叫转移配置结构体。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## USSD 会话

### tapi_ss_initiate_service

```c
int tapi_ss_initiate_service(tapi_context context, int slot_id, int event_id,
                             char* command, tapi_async_function p_handle);
```

发起 SS 服务命令（USSD/SS 字符串形式，如 `*#06#`）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `command` 命令字符串。
- `p_handle` 异步回调函数，回调返回 `tapi_ss_initiate_info`。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_get_ussd_state

```c
int tapi_get_ussd_state(tapi_context context, int slot_id, char** out);
```

查询当前 USSD 会话状态。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `out` 输出参数，返回状态字符串（如 `"idle"`、`"user-response"`）。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_send_ussd

```c
int tapi_ss_send_ussd(tapi_context context, int slot_id, int event_id, char* reply,
                     tapi_async_function p_handle);
```

发送 USSD 回复消息。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `reply` 回复字符串。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_cancel_ussd

```c
int tapi_ss_cancel_ussd(tapi_context context, int slot_id, int event_id,
                       tapi_async_function p_handle);
```

取消当前 USSD 会话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## 呼叫等待

### tapi_ss_set_call_waiting

```c
int tapi_ss_set_call_waiting(tapi_context context, int slot_id, int event_id, bool enable,
                             tapi_async_function p_handle);
```

启用或禁用呼叫等待功能。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `enable` `true` 启用，`false` 禁用。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_get_call_waiting

```c
int tapi_ss_get_call_waiting(tapi_context context, int slot_id, int event_id,
                             tapi_async_function p_handle);
```

查询呼叫等待开关状态。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `p_handle` 异步回调函数，回调返回当前状态。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## CLIR / CLIP（主叫号码显示与限制）

### tapi_ss_get_calling_line_presentation_info

```c
int tapi_ss_get_calling_line_presentation_info(tapi_context context, int slot_id,
                                               int event_id, tapi_async_function p_handle);
```

查询主叫号码显示（CLIP）状态。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_set_calling_line_restriction

```c
int tapi_ss_set_calling_line_restriction(tapi_context context, int slot_id, int event_id,
                                         tapi_clir_status status,
                                         tapi_async_function p_handle);
```

设置主叫号码限制（CLIR）状态。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `status` CLIR 状态枚举值（`CLIR_DEFAULT` / `CLIR_INVOCATION` / `CLIR_SUPPRESSION`）。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_get_calling_line_restriction_info

```c
int tapi_ss_get_calling_line_restriction_info(tapi_context context, int slot_id,
                                              int event_id, tapi_async_function p_handle);
```

查询主叫号码限制（CLIR）状态。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## FDN（固定拨号）开关

### tapi_ss_enable_fdn

```c
int tapi_ss_enable_fdn(tapi_context context, int slot_id, int event_id,
                      bool enable, char* pin2, tapi_async_function p_handle);
```

启用或禁用 FDN 模式（需要 PIN2）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `enable` `true` 启用 FDN，`false` 禁用。
- `pin2` SIM 卡 PIN2 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_ss_query_fdn

```c
int tapi_ss_query_fdn(tapi_context context, int slot_id, int event_id,
                     tapi_async_function p_handle);
```

查询 FDN 开关状态。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## 事件订阅

### tapi_ss_register

```c
int tapi_ss_register(tapi_context context, int slot_id, tapi_indication_msg msg,
                    void* user_obj, tapi_async_function p_handle);
```

注册 SS 相关事件回调。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `msg` 要监听的事件类型。
- `user_obj` 用户数据。
- `p_handle` 事件回调函数。

**返回值**：

成功时返回 watch ID，失败时返回负的错误码。

### tapi_ss_unregister

```c
int tapi_ss_unregister(tapi_context context, int watch_id);
```

取消 SS 事件订阅。

**参数**：

- `context` Telephony 上下文句柄。
- `watch_id` 订阅时返回的 watch ID。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。
