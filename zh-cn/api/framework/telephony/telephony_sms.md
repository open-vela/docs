\[ [English](../../../../en/api/framework/telephony/telephony_sms.md) | 简体中文 \]

# 短信管理 API

短信发送和接收。

头文件：`#include <tapi_sms.h>`

## openvela 实现说明

- **文本与数据短信**：`send_message` 发送文本短信，`send_data_message` 发送二进制 PDU
- **服务中心地址**：通过 `set_service_center_address` / `get_service_center_address` 配置运营商短信网关
- **送达报告**：可通过 `enable_delivery_report` 开关送达报告
- **SIM 卡存储**：提供 `get_all_messages_from_sim` / `copy_message_to_sim` / `delete_message_from_sim` 操作 SIM 卡上的短信
- **事件订阅**：`tapi_sms_register` 监听收件/发件事件

## 发送短信

### tapi_sms_send_message

```c
int tapi_sms_send_message(tapi_context context, int slot_id, int sms_id, char* number, char* text, int event_id, tapi_async_function p_handle);
```

发送短信。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `sms_id` 短信 ID。
- `number` 电话号码。
- `text` 文本内容。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sms_send_data_message

```c
int tapi_sms_send_data_message(tapi_context context, int slot_id, int sms_id, char* dest_addr, unsigned int port, char* text, int event_id, tapi_async_function p_handle);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `sms_id` 短信 ID。
- `dest_addr` 目标号码。
- `port` 端口号。
- `text` 文本内容。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 服务中心与送达报告

### tapi_sms_set_service_center_address

```c
bool tapi_sms_set_service_center_address(tapi_context context, int slot_id, char* number);
```

设置短信服务中心地址。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `number` 服务中心号码。

**返回值**：

成功时返回 `true`，失败时返回 `false`。



### tapi_sms_get_service_center_address

```c
int tapi_sms_get_service_center_address(tapi_context context, int slot_id, char** number);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `number` 电话号码。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sms_enable_delivery_report

```c
int tapi_sms_enable_delivery_report(tapi_context context, int slot_id, bool enable);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `enable` 是否启用。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sms_get_delivery_report_status

```c
int tapi_sms_get_delivery_report_status(tapi_context context, int slot_id, bool* out);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## SIM 卡短信存储

### tapi_sms_get_all_messages_from_sim

```c
int tapi_sms_get_all_messages_from_sim(tapi_context context, int slot_id, tapi_message_list* list, tapi_async_function p_handle);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `list` 列表。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sms_copy_message_to_sim

```c
int tapi_sms_copy_message_to_sim(tapi_context context, int slot_id, char* number, char* text, char* send_time, int type);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `number` 电话号码。
- `text` 文本内容。
- `send_time` 发送时间。
- `type` 类型。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sms_delete_message_from_sim

```c
int tapi_sms_delete_message_from_sim(tapi_context context, int slot_id, int index);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `index` 索引。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 事件订阅与默认卡

### tapi_sms_register

```c
int tapi_sms_register(tapi_context context, int slot_id, tapi_indication_msg msg, void* user_obj, tapi_async_function p_handle);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `msg` 消息内容。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sms_unregister

```c
int tapi_sms_unregister(tapi_context context, int watch_id);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `watch_id` 监听 ID（用于取消监听）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sms_set_default_slot

```c
int tapi_sms_set_default_slot(tapi_context context, int slot_id);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_sms_get_default_slot

```c
int tapi_sms_get_default_slot(tapi_context context, int* out);
```

发送数据短信。

**参数**：

- `context` Telephony 上下文句柄。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

