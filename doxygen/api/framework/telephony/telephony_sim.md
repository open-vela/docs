# SIM 卡管理 API

SIM 卡状态查询和管理。

头文件：`#include <tapi_sim.h>`

## openvela 实现说明

- **多卡支持**：所有接口均带 `slot_id`，支持多 SIM 卡设备
- **PIN 管理**：提供 `enter_pin` / `change_pin` / `reset_pin` / `lock_pin` / `unlock_pin` 完整 PIN/PUK 流程
- **APDU 通道**：通过 `open_logical_channel` / `close_logical_channel` / `transmit_apdu_*` 直接向 SIM 卡发送 APDU 命令
- **UICC 开关**：通过 `get_uicc_enablement` / `set_uicc_enablement` 控制 SIM 卡的启用状态
- **事件订阅**：`tapi_sim_register` / `tapi_sim_unregister` 监听 SIM 卡状态变化

## SIM 状态查询

### tapi_sim_has_icc_card

```c
int tapi_sim_has_icc_card(tapi_context context, int slot_id, bool* out);
```

查询是否插入 SIM 卡。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_get_sim_state

```c
int tapi_sim_get_sim_state(tapi_context context, int slot_id, int* out);
```

获取 SIM 卡状态。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_get_sim_operator

```c
int tapi_sim_get_sim_operator(tapi_context context, int slot_id, int length, char* out);
```

获取 SIM 卡运营商信息。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `length` 数据长度。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_get_sim_operator_name

```c
int tapi_sim_get_sim_operator_name(tapi_context context, int slot_id, char** out);
```

获取 SIM 卡运营商信息。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_get_sim_iccid

```c
int tapi_sim_get_sim_iccid(tapi_context context, int slot_id, char** out);
```

获取 SIM 卡 ICCID。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_get_subscriber_id

```c
int tapi_sim_get_subscriber_id(tapi_context context, int slot_id, char** out);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 事件订阅

### tapi_sim_register

```c
int tapi_sim_register(tapi_context context, int slot_id, tapi_indication_msg msg, void* user_obj, tapi_async_function p_handle);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `msg` 消息内容。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_unregister

```c
int tapi_sim_unregister(tapi_context context, int watch_id);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `watch_id` 监听 ID（用于取消监听）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## PIN 管理

### tapi_sim_change_pin

```c
int tapi_sim_change_pin(tapi_context context, int slot_id, int event_id, char* pin_type, char* old_pin, char* new_pin, tapi_async_function p_handle);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `pin_type` PIN 码类型。
- `old_pin` 旧 PIN 码。
- `new_pin` 新 PIN 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_enter_pin

```c
int tapi_sim_enter_pin(tapi_context context, int slot_id, int event_id, char* pin_type, char* pin, tapi_async_function p_handle);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `pin_type` PIN 码类型。
- `pin` PIN 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_reset_pin

```c
int tapi_sim_reset_pin(tapi_context context, int slot_id, int event_id, char* puk_type, char* puk, char* new_pin, tapi_async_function p_handle);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `puk_type` PUK 码类型。
- `puk` PUK 码。
- `new_pin` 新 PIN 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_lock_pin

```c
int tapi_sim_lock_pin(tapi_context context, int slot_id, int event_id, char* pin_type, char* pin, tapi_async_function p_handle);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `pin_type` PIN 码类型。
- `pin` PIN 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_unlock_pin

```c
int tapi_sim_unlock_pin(tapi_context context, int slot_id, int event_id, char* pin_type, char* pin, tapi_async_function p_handle);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `pin_type` PIN 码类型。
- `pin` PIN 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## APDU 逻辑通道

### tapi_sim_open_logical_channel

```c
int tapi_sim_open_logical_channel(tapi_context context, int slot_id, int event_id, unsigned char aid[], int len, tapi_async_function p_handle);
```

打开 SIM 卡逻辑通道。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `aid` 应用 ID。
- `len` 长度。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_close_logical_channel

```c
int tapi_sim_close_logical_channel(tapi_context context, int slot_id, int event_id, int session_id, tapi_async_function p_handle);
```

关闭 SIM 卡逻辑通道。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `session_id` 会话 ID。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_transmit_apdu_logical_channel

```c
int tapi_sim_transmit_apdu_logical_channel(tapi_context context, int slot_id, int event_id, int session_id, unsigned char pdu[], int len, tapi_async_function p_handle);
```

通过逻辑通道发送 APDU 命令。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `session_id` 会话 ID。
- `pdu` PDU 数据。
- `len` 长度。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_transmit_apdu_basic_channel

```c
int tapi_sim_transmit_apdu_basic_channel(tapi_context context, int slot_id, int event_id, unsigned char pdu[], int len, tapi_async_function p_handle);
```

通过逻辑通道发送 APDU 命令。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `pdu` PDU 数据。
- `len` 长度。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## UICC 开关

### tapi_sim_get_uicc_enablement

```c
int tapi_sim_get_uicc_enablement(tapi_context context, int slot_id, tapi_sim_uicc_app_state* out);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_set_uicc_enablement

```c
int tapi_sim_set_uicc_enablement(tapi_context context, int slot_id, int event_id, int state, tapi_async_function p_handle);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `state` 状态。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sim_get_sim_invalid

```c
int tapi_sim_get_sim_invalid(tapi_context context, int slot_id, int* out);
```

获取用户标识（IMSI）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

