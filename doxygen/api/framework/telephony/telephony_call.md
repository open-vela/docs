# 通话管理 API

语音通话控制，包括拨号、接听、挂断、保持等。

头文件：`#include <tapi_call.h>`

## openvela 实现说明

- **多卡支持**：部分接口不带 `slot_id`，使用默认卡；需要指定卡时通过 `tapi_call_set_default_slot` 切换
- **同步/异步**：拨号、应答等耗时操作同时提供同步版本和 `_async` 版本（回调风格）
- **按 ID 操作**：长生命周期通话通过返回的 call ID（字符串）唯一标识，`*_by_id` 接口据此执行操作
- **DTMF**：拨号盘按键通过 `tapi_call_send_tones`（批量）或 `tapi_call_start_dtmf` / `tapi_call_stop_dtmf`（持续按键）触发
- **会议通话**：通过 `tapi_call_dial_conferece` 和 `tapi_call_merge_call` 组织，`tapi_call_separate_call` 拆分

## 拨打与应答

### tapi_call_dial

```c
int tapi_call_dial(tapi_context context, int slot_id, char* number, int hide_callerid, int event_id, tapi_async_function p_handle);
```

发起语音通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `number` 电话号码。
- `hide_callerid` 是否隐藏主叫号码。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_dial_async

```c
int tapi_call_dial_async(tapi_context context, int slot_id, char* number, int hide_callerid, int event_id, void* user_data, tapi_async_function p_handle);
```

发起语音通话（异步版本）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `number` 电话号码。
- `hide_callerid` 是否隐藏主叫号码。
- `event_id` 事件 ID，用于回调匹配。
- `user_data` 用户数据，传递给回调函数。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 挂断控制

### tapi_call_hangup_all_calls

```c
int tapi_call_hangup_all_calls(tapi_context context, int slot_id);
```

挂断所有通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 保持与切换

### tapi_call_release_and_answer

```c
int tapi_call_release_and_answer(tapi_context context, int slot_id);
```

挂断当前通话并接听等待中的来电。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_hold_and_answer

```c
int tapi_call_hold_and_answer(tapi_context context, int slot_id);
```

保持当前通话并接听等待中的来电。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_release_and_swap

```c
int tapi_call_release_and_swap(tapi_context context, int slot_id);
```

挂断当前通话并切换到保持中的通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_hold_call

```c
int tapi_call_hold_call(tapi_context context, int slot_id);
```

保持当前通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_unhold_call

```c
int tapi_call_unhold_call(tapi_context context, int slot_id);
```

恢复保持中的通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 转移与会议

### tapi_call_transfer

```c
int tapi_call_transfer(tapi_context context, int slot_id);
```

转接通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_merge_call

```c
int tapi_call_merge_call(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

合并通话（多方通话）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_merge_call_async

```c
int tapi_call_merge_call_async(tapi_context context, int slot_id, int event_id, void* user_data, tapi_async_function p_handle);
```

合并通话（多方通话）（异步版本）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `user_data` 用户数据，传递给回调函数。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_separate_call

```c
int tapi_call_separate_call(tapi_context context, int slot_id, int event_id, char* call_id, tapi_async_function p_handle);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `call_id` 通话 ID。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_hangup_multiparty

```c
int tapi_call_hangup_multiparty(tapi_context context, int slot_id);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## DTMF 与拨号音

### tapi_call_send_tones

```c
int tapi_call_send_tones(void* context, int slot_id, char* tones);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `tones` DTMF 按键序列。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 通话查询

### tapi_call_get_all_calls

```c
int tapi_call_get_all_calls(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_get_call_by_state

```c
int tapi_call_get_call_by_state(tapi_context context, int slot_id, int state, tapi_call_info* call_list, int size, tapi_call_info* out_list);
```

获取指定通话的信息。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `state` 状态。
- `call_list` 通话列表。
- `size` 大小。
- `out_list` 输出列表。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 紧急号码

### tapi_call_get_ecc_list

```c
int tapi_call_get_ecc_list(tapi_context context, int slot_id, ecc_info* out);
```

获取紧急呼叫号码列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_is_emergency_number

```c
int tapi_call_is_emergency_number(tapi_context context, char* number);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `number` 电话号码。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 事件订阅

### tapi_call_register_emergency_list_change

```c
int tapi_call_register_emergency_list_change(tapi_context context, int slot_id, void* user_obj, tapi_async_function p_handle);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_register_ringback_tone_change

```c
int tapi_call_register_ringback_tone_change(tapi_context context, int slot_id, void* user_obj, tapi_async_function p_handle);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_register_default_voicecall_slot_change

```c
int tapi_call_register_default_voicecall_slot_change(tapi_context context, void* user_obj, tapi_async_function p_handle);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 会议通话

### tapi_call_dial_conferece

```c
int tapi_call_dial_conferece(tapi_context context, int slot_id, char* participants[], int size);
```

发起语音通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `participants` 参与者列表。
- `size` 大小。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_invite_participants

```c
int tapi_call_invite_participants(tapi_context context, int slot_id, char* participants[], int size);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `participants` 参与者列表。
- `size` 大小。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_register_call_state_change

```c
int tapi_call_register_call_state_change(tapi_context context, int slot_id, void* user_obj, tapi_async_function p_handle);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 按 ID 操作

### tapi_call_answer_by_id

```c
int tapi_call_answer_by_id(tapi_context context, int slot_id, char* call_id);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `call_id` 通话 ID。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_answer_by_id_async

```c
int tapi_call_answer_by_id_async(tapi_context context, int slot_id, char* call_id, void* user_obj, tapi_async_function p_handle);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `call_id` 通话 ID。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_hangup_by_id

```c
int tapi_call_hangup_by_id(tapi_context context, int slot_id, char* call_id);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `call_id` 通话 ID。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_deflect_by_id

```c
int tapi_call_deflect_by_id(tapi_context context, int slot_id, char* call_id, char* number);
```

转移来电到指定号码。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `call_id` 通话 ID。
- `number` 电话号码。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 连续 DTMF

### tapi_call_start_dtmf

```c
int tapi_call_start_dtmf(tapi_context context, int slot_id, unsigned char digit, int event_id, tapi_async_function p_handle);
```

开始发送 DTMF 按键音。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `digit` DTMF 按键字符。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_stop_dtmf

```c
int tapi_call_stop_dtmf(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

停止发送 DTMF 按键音。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 默认卡槽

### tapi_call_set_default_slot

```c
int tapi_call_set_default_slot(tapi_context context, int slot_id);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_call_get_default_slot

```c
int tapi_call_get_default_slot(tapi_context context, int* out);
```

从多方通话中分离指定通话。

**参数**：

- `context` Telephony 上下文句柄。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

