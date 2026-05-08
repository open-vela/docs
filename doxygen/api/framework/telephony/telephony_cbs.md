# Telephony 小区广播 API

Cell Broadcast Service（CBS）是蜂窝网络的小区广播能力，常用于接收政府紧急警报（地震、海啸）和运营商公告。

头文件：`#include <tapi_cbs.h>`

## openvela 实现说明

- **开关控制**：通过 `set_cell_broadcast_power_on` 启用/禁用小区广播接收
- **主题订阅**：通过 `set_cell_broadcast_topics` 配置要接收的广播主题范围（按频道 ID）
- **事件回调**：通过 `tapi_cbs_register` 注册事件回调，接收到的广播消息
- **多卡支持**：所有接口带 `slot_id`，支持多 SIM 卡设备
- **相关协议**：底层对应 3GPP TS 23.041 定义的 Cell Broadcast 流程

## 开关控制

### tapi_sms_set_cell_broadcast_power_on

```c
int tapi_sms_set_cell_broadcast_power_on(tapi_context context, int slot_id, bool enabled);
```

启用或禁用小区广播接收。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `enabled` `true` 表示启用，`false` 表示禁用。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_sms_get_cell_broadcast_power_on

```c
int tapi_sms_get_cell_broadcast_power_on(tapi_context context, int slot_id, bool* enabled);
```

查询小区广播接收开关状态。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `enabled` 输出参数，返回当前开关状态。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## 主题订阅

### tapi_sms_set_cell_broadcast_topics

```c
int tapi_sms_set_cell_broadcast_topics(tapi_context context, int slot_id, char* topics);
```

配置小区广播的主题范围（频道 ID 列表）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `topics` 主题字符串，典型格式为逗号分隔的频道 ID 或范围（如 `"4352-4356,919"`）。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_sms_get_cell_broadcast_topics

```c
int tapi_sms_get_cell_broadcast_topics(tapi_context context, int slot_id, char** topics);
```

查询当前配置的小区广播主题。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `topics` 输出参数，返回主题字符串（调用方负责释放）。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## 事件订阅

### tapi_cbs_register

```c
int tapi_cbs_register(tapi_context context, int slot_id, tapi_indication_msg msg,
                      void* user_obj, tapi_async_function p_handle);
```

注册小区广播事件回调。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `msg` 要监听的事件类型。
- `user_obj` 用户数据，将回传给回调函数。
- `p_handle` 事件回调函数。

**返回值**：

成功时返回事件订阅 watch ID，失败时返回负的错误码。
