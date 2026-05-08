# 网络服务 API

蜂窝网络注册、信号强度、运营商信息等。

头文件：`#include <tapi_network.h>`

## openvela 实现说明

- **选网模式**：支持自动选网（`select_auto`）和手动选网（`select_manual`）
- **扫描**：`tapi_network_scan` 扫描可用的网络运营商
- **小区信息**：`get_serving_cellinfos` 获取当前服务小区，`get_neighbouring_cellinfos` 获取相邻小区
- **多卡支持**：大部分接口带 `slot_id`，区分不同 SIM 卡槽的网络状态
- **事件订阅**：`tapi_network_register` / `tapi_network_unregister` 监听注册状态/信号强度变化

## 选网与扫描

### tapi_network_select_auto

```c
int tapi_network_select_auto(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

自动选择网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_select_manual

```c
int tapi_network_select_manual(tapi_context context, int slot_id, int event_id, tapi_operator_info* network, tapi_async_function p_handle);
```

手动选择网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `network` 网络信息。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_scan

```c
int tapi_network_scan(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 小区信息

### tapi_network_get_serving_cellinfos

```c
int tapi_network_get_serving_cellinfos(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_get_neighbouring_cellinfos

```c
int tapi_network_get_neighbouring_cellinfos(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 语音网络状态

### tapi_network_is_voice_registered

```c
int tapi_network_is_voice_registered(tapi_context context, int slot_id, bool* out);
```

查询是否已注册语音服务。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_is_voice_emergency_only

```c
int tapi_network_is_voice_emergency_only(tapi_context context, int slot_id, bool* out);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_get_voice_network_type

```c
int tapi_network_get_voice_network_type(tapi_context context, int slot_id, tapi_network_type* out);
```

获取语音网络类型。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_is_voice_roaming

```c
int tapi_network_is_voice_roaming(tapi_context context, int slot_id, bool* out);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 运营商信息

### tapi_network_get_display_name

```c
int tapi_network_get_display_name(tapi_context context, int slot_id, char** out);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 信号强度

### tapi_network_get_signalstrength

```c
int tapi_network_get_signalstrength(tapi_context context, int slot_id, tapi_signal_strength* out);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 注册信息

### tapi_network_get_registration_info

```c
int tapi_network_get_registration_info(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

获取网络注册信息。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 上报频率与事件

### tapi_network_set_cell_info_list_rate

```c
int tapi_network_set_cell_info_list_rate(tapi_context context, int slot_id, int event_id, u_int32_t period, tapi_async_function p_handle);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `period` 周期（毫秒）。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_register

```c
int tapi_network_register(tapi_context context, int slot_id, tapi_indication_msg msg, void* user_obj, tapi_async_function p_handle);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `msg` 消息内容。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_unregister

```c
int tapi_network_unregister(tapi_context context, int watch_id);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `watch_id` 监听 ID（用于取消监听）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## MCC / MNC

### tapi_network_get_mcc

```c
int tapi_network_get_mcc(tapi_context context, int slot_id, char** mcc);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `mcc` 移动国家码。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_get_mnc

```c
int tapi_network_get_mnc(tapi_context context, int slot_id, char** mnc);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `mnc` 移动网络码。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_get_operator_status

```c
int tapi_network_get_operator_status(tapi_context context, int slot_id, int* out);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_get_operator_name

```c
int tapi_network_get_operator_name(tapi_context context, int slot_id, char** out);
```

获取运营商名称。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_network_get_reg_state

```c
int tapi_network_get_reg_state(tapi_context context, int slot_id, tapi_registration_state* out);
```

手动选择指定网络。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

