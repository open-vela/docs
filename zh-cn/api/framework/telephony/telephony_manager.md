\[ [English](../../../../en/api/framework/telephony/telephony_manager.md) | 简体中文 \]

# Telephony 管理 API

蜂窝通信管理接口，包括初始化、状态查询和事件注册。

头文件：`#include <tapi_manager.h>`

## openvela 实现说明

- **基于 D-Bus**：TAPI Manager 通过 D-Bus 与 Telephony Core Stack（oFono）通信，对外以标准 C 接口封装
- **SIM 卡标识**：管理器层面不直接涉及 SIM 卡槽选择，涉及特定卡槽的操作在 `tapi_sim` 等子模块中使用 `slot_id` 参数
- **客户端句柄**：通过 `tapi_open` 获取 `tapi_context`，所有后续调用均以该 context 作为第一个参数
- **事件订阅**：通过 `tapi_register` 注册事件回调，`tapi_unregister` 取消订阅
- **同步 vs 异步**：多数接口是异步的（带回调），部分提供 `*_sync` 变体用于简单场景

## 客户端连接管理

### tapi_open

```c
tapi_context tapi_open(const char* client_name, tapi_client_ready_function callback, void* user_data);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `client_name` 客户端名称。
- `callback` 回调函数。
- `user_data` 用户数据，传递给回调函数。

**返回值**：

成功时返回有效的 `tapi_context` 句柄，失败时返回 `NULL`。



### tapi_open_service

```c
tapi_context tapi_open_service(const char* client_name, tapi_client_ready_function callback, void* user_data, unsigned int tapi_service);
```

打开 Telephony 连接，指定服务类型。

**参数**：

- `client_name` 客户端名称。
- `callback` 回调函数。
- `user_data` 用户数据，传递给回调函数。
- `tapi_service` Telephony 服务类型。

**返回值**：

成功时返回有效的 `tapi_context` 句柄，失败时返回 `NULL`。



### tapi_close

```c
int tapi_close(tapi_context context);
```

关闭 Telephony 连接。

**参数**：

- `context` Telephony 上下文句柄。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 能力查询

### tapi_is_feature_supported

```c
bool tapi_is_feature_supported(tapi_feature_type feature);
```

查询是否支持指定功能。

**参数**：

- `feature` 功能类型枚举值。

**返回值**：

支持时返回 `true`，不支持时返回 `false`。



## 无线电控制

### tapi_set_radio_power

```c
int tapi_set_radio_power(tapi_context context, int slot_id, int event_id, bool state, tapi_async_function p_handle);
```

设置射频功率。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `state` 状态。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_set_radio_power_async

```c
int tapi_set_radio_power_async(tapi_context context, int slot_id, int event_id, bool state, void* user_data, tapi_async_function p_handle);
```

设置射频功率（异步版本）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `state` 状态。
- `user_data` 用户数据，传递给回调函数。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_radio_power

```c
int tapi_get_radio_power(tapi_context context, int slot_id, bool* out);
```

获取射频功率状态。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 网络模式

### tapi_set_pref_net_mode

```c
int tapi_set_pref_net_mode(tapi_context context, int slot_id, int event_id, tapi_pref_net_mode mode, tapi_async_function p_handle);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `mode` 模式。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_pref_net_mode

```c
int tapi_get_pref_net_mode(tapi_context context, int slot_id, tapi_pref_net_mode* out);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_radio_state

```c
int tapi_get_radio_state(tapi_context context, int slot_id, tapi_radio_state* out);
```

获取射频状态。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## Modem 信息

### tapi_get_imei

```c
int tapi_get_imei(tapi_context context, int slot_id, char** out);
```

获取设备 IMEI。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_imeisv

```c
int tapi_get_imeisv(tapi_context context, int slot_id, char** out);
```

获取设备 IMEI。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_modem_revision

```c
int tapi_get_modem_revision(tapi_context context, int slot_id, char** out);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_phone_state

```c
int tapi_get_phone_state(tapi_context context, int slot_id, tapi_phone_state* state);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `state` 状态。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 手机号码

### tapi_get_msisdn_number

```c
int tapi_get_msisdn_number(tapi_context context, int slot_id, char** out);
```

获取 SIM 卡电话号码（MSISDN）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## Modem 状态与控制

### tapi_get_modem_activity_info

```c
int tapi_get_modem_activity_info(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

获取 Modem 活动信息。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_invoke_oem_ril_request_raw

```c
int tapi_invoke_oem_ril_request_raw(tapi_context context, int slot_id, int event_id, unsigned char oem_req[], int length, tapi_async_function p_handle);
```

发送 OEM RIL 请求。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `oem_req` OEM 请求数据。
- `length` 数据长度。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_invoke_oem_ril_request_strings

```c
int tapi_invoke_oem_ril_request_strings(tapi_context context, int slot_id, int event_id, char* oem_req[], int length, tapi_async_function p_handle);
```

发送 OEM RIL 请求。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `oem_req` OEM 请求数据。
- `length` 数据长度。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_enable_modem

```c
int tapi_enable_modem(tapi_context context, int slot_id, int event_id, bool enable, tapi_async_function p_handle);
```

启用 Modem。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `enable` 是否启用。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_enable_modem_abnormal_event

```c
int tapi_enable_modem_abnormal_event(tapi_context context, int slot_id, bool enable, int event_id, int module_mask, int from_event_id, int to_event_id, tapi_async_function p_handle);
```

启用 Modem。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `enable` 是否启用。
- `event_id` 事件 ID，用于回调匹配。
- `module_mask` 模块掩码。
- `from_event_id` 源事件 ID。
- `to_event_id` 目标事件 ID。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_set_signal_report_threshold

```c
int tapi_set_signal_report_threshold(tapi_context context, int slot_id, int event_id, int type, tapi_async_function p_handle);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `type` 类型。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_suppress_message_report

```c
int tapi_suppress_message_report(tapi_context context, int slot_id, int event_id, bool enable, tapi_async_function p_handle);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `enable` 是否启用。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_enable_modem_stationary

```c
int tapi_enable_modem_stationary(tapi_context context, int slot_id, int event_id, bool enable, tapi_async_function p_handle);
```

启用 Modem。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `enable` 是否启用。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_set_modem_stationary_threshold

```c
int tapi_set_modem_stationary_threshold(tapi_context context, int slot_id, int event_id, int value, tapi_async_function p_handle);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `value` 值。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_modem_status

```c
int tapi_get_modem_status(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_modem_status_sync

```c
int tapi_get_modem_status_sync(tapi_context context, int slot_id, tapi_modem_state* out);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_set_fast_dormancy

```c
int tapi_set_fast_dormancy(tapi_context context, int slot_id, int event_id, bool state, tapi_async_function p_handle);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `state` 状态。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_phone_number

```c
int tapi_get_phone_number(tapi_context context, int slot_id, char** out);
```

获取本机号码。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 事件订阅

### tapi_register

```c
int tapi_register(tapi_context context, int slot_id, tapi_indication_msg msg, void* user_obj, tapi_async_function p_handle);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `msg` 消息内容。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_unregister

```c
int tapi_unregister(tapi_context context, int watch_id);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `watch_id` 监听 ID（用于取消监听）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 运营商配置

### tapi_get_carrier_config_bool

```c
int tapi_get_carrier_config_bool(tapi_context context, int slot_id, char* key, bool* out);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `key` 键名。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_carrier_config_int

```c
int tapi_get_carrier_config_int(tapi_context context, int slot_id, char* key, int* out);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `key` 键名。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_get_carrier_config_string

```c
int tapi_get_carrier_config_string(tapi_context context, int slot_id, char* key, char** out);
```

打开 Telephony 连接，获取上下文句柄。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `key` 键名。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

