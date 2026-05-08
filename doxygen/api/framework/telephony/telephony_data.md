# 数据连接 API

蜂窝数据连接管理。

头文件：`#include <tapi_data.h>`

## openvela 实现说明

- **APN 上下文**：通过 `tapi_data_*_apn_context` 系列接口管理 APN 配置（增删改查）
- **按需连接**：`tapi_data_request_network` / `tapi_data_release_network` 控制数据网络的建立与释放
- **漫游控制**：通过 `tapi_data_enable_roaming` 显式开关数据漫游
- **多卡支持**：涉及特定卡的操作使用 `slot_id` 参数；数据默认卡通过 `tapi_data_set_default_slot` 设置
- **状态订阅**：`tapi_data_register` / `tapi_data_unregister` 用于注册/取消状态变化事件

## APN 配置管理

### tapi_data_load_apn_contexts

```c
int tapi_data_load_apn_contexts(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

加载 APN 配置。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_add_apn_context

```c
int tapi_data_add_apn_context(tapi_context context, int slot_id, int event_id, tapi_data_context* apn, tapi_async_function p_handle);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `apn` 接入点名称（APN）。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_remove_apn_context

```c
int tapi_data_remove_apn_context(tapi_context context, int slot_id, int event_id, tapi_data_context* apn, tapi_async_function p_handle);
```

删除 APN 配置。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `apn` 接入点名称（APN）。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_edit_apn_context

```c
int tapi_data_edit_apn_context(tapi_context context, int slot_id, int event_id, tapi_data_context* apn, tapi_async_function p_handle);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `apn` 接入点名称（APN）。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_reset_apn_contexts

```c
int tapi_data_reset_apn_contexts(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

重置 APN 配置为默认值。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 数据网络状态

### tapi_data_is_registered

```c
int tapi_data_is_registered(tapi_context context, int slot_id, bool* out);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_is_data_emergency_only

```c
int tapi_data_is_data_emergency_only(tapi_context context, int slot_id, bool* out);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_get_network_type

```c
int tapi_data_get_network_type(tapi_context context, int slot_id, tapi_network_type* out);
```

获取当前网络类型。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_is_data_roaming

```c
int tapi_data_is_data_roaming(tapi_context context, int slot_id, bool* out);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 数据连接控制

### tapi_data_request_network

```c
int tapi_data_request_network(tapi_context context, int slot_id, const char* type);
```

请求建立数据连接。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `type` 类型。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_release_network

```c
int tapi_data_release_network(tapi_context context, int slot_id, const char* type);
```

释放数据连接。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `type` 类型。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_get_data_connection_list

```c
int tapi_data_get_data_connection_list(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 首选 APN

### tapi_data_set_preferred_apn

```c
int tapi_data_set_preferred_apn(tapi_context context, int slot_id, tapi_data_context* apn);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `apn` 接入点名称（APN）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_get_preferred_apn

```c
int tapi_data_get_preferred_apn(tapi_context context, int slot_id, char** out);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 数据开关

### tapi_data_enable_data

```c
int tapi_data_enable_data(tapi_context context, bool enabled);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `enabled` 是否启用。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_get_enabled

```c
int tapi_data_get_enabled(tapi_context context, bool* out);
```

查询 IMS 是否启用。

**参数**：

- `context` Telephony 上下文句柄。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 漫游控制

### tapi_data_enable_roaming

```c
int tapi_data_enable_roaming(tapi_context context, bool enabled);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `enabled` 是否启用。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_get_roaming_enabled

```c
int tapi_data_get_roaming_enabled(tapi_context context, bool* out);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 默认卡槽与授权

### tapi_data_set_default_slot

```c
int tapi_data_set_default_slot(tapi_context context, int slot_id);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_get_default_slot

```c
int tapi_data_get_default_slot(tapi_context context, int* out);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_set_data_allow

```c
int tapi_data_set_data_allow(tapi_context context, int slot_id, int event_id, bool allowed, tapi_async_function p_handle);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `event_id` 事件 ID，用于回调匹配。
- `allowed` 是否允许。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 事件订阅

### tapi_data_register

```c
int tapi_data_register(tapi_context context, int slot_id, tapi_indication_msg msg, void* user_obj, tapi_async_function p_handle);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `msg` 消息内容。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_data_unregister

```c
int tapi_data_unregister(tapi_context context, int watch_id);
```

加载 APN 配置列表。

**参数**：

- `context` Telephony 上下文句柄。
- `watch_id` 监听 ID（用于取消监听）。

**返回值**：

成功时返回 0，失败时返回负的错误码。

