\[ [English](../../../../en/api/framework/bluetooth/bt_hfp.md) | 简体中文 \]

# 蓝牙 HFP API

openvela 蓝牙 HFP（免提规范）接口，支持蓝牙通话功能。

头文件：#include "bt_hfp.h"、#include "bt_hfp_hf.h"、#include "bt_hfp_ag.h"


## openvela 实现说明

- **双角色支持**：HF（Hands-Free，免提端）和 AG（Audio Gateway，音频网关端）
- **功能**：接听/挂断电话、音量控制、语音识别、电话簿访问


## 同步接口


### bt_hfp_hf_unregister_callbacks

```c
bool bt_hfp_hf_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

取消注册回调函数，停止接收状态变更通知。

**参数**：

- `ins` 蓝牙客户端实例。
- `cookie` 用户上下文。

**返回值**：

成功时返回 `true`，失败时返回 `false`。


### bt_hfp_hf_is_connected

```c
bool bt_hfp_hf_is_connected(bt_instance_t* ins, bt_address_t* addr);
```

查询与远程设备的 HFP HF 是否已连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

已连接时返回 `true`，未连接时返回 `false`。


### bt_hfp_hf_is_audio_connected

```c
bool bt_hfp_hf_is_audio_connected(bt_instance_t* ins, bt_address_t* addr);
```

查询与远程设备的 HFP 音频通道是否已连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

音频已连接时返回 `true`，未连接时返回 `false`。


### bt_hfp_hf_get_connection_state

```c
profile_connection_state_t bt_hfp_hf_get_connection_state(bt_instance_t* ins, bt_address_t* addr);
```

获取与远程设备的 HFP HF 连接状态。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

返回当前连接状态枚举值，参见 `profile_connection_state_t`。


### bt_hfp_hf_connect

```c
bt_status_t bt_hfp_hf_connect(bt_instance_t* ins, bt_address_t* addr);
```

发起与远程设备的 HFP HF 连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 对端设备蓝牙地址。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_disconnect

```c
bt_status_t bt_hfp_hf_disconnect(bt_instance_t* ins, bt_address_t* addr);
```

断开与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_set_connection_policy

```c
bt_status_t bt_hfp_hf_set_connection_policy(bt_instance_t* ins, bt_address_t* addr, connection_policy_t policy);
```

发起与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `policy` 策略值。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_connect_audio

```c
bt_status_t bt_hfp_hf_connect_audio(bt_instance_t* ins, bt_address_t* addr);
```

发起与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_disconnect_audio

```c
bt_status_t bt_hfp_hf_disconnect_audio(bt_instance_t* ins, bt_address_t* addr);
```

断开与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_start_voice_recognition

```c
bt_status_t bt_hfp_hf_start_voice_recognition(bt_instance_t* ins, bt_address_t* addr);
```

启动远程设备的语音识别功能。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_stop_voice_recognition

```c
bt_status_t bt_hfp_hf_stop_voice_recognition(bt_instance_t* ins, bt_address_t* addr);
```

停止远程设备的语音识别功能。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_dial

```c
bt_status_t bt_hfp_hf_dial(bt_instance_t* ins, bt_address_t* addr, const char* number);
```

发起通话。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `number` 号码。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_dial_memory

```c
bt_status_t bt_hfp_hf_dial_memory(bt_instance_t* ins, bt_address_t* addr, uint32_t memory);
```

通过 HFP 拨打内存中存储的号码。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `memory` 内存位置编号。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_redial

```c
bt_status_t bt_hfp_hf_redial(bt_instance_t* ins, bt_address_t* addr);
```

发起通话。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_accept_call

```c
bt_status_t bt_hfp_hf_accept_call(bt_instance_t* ins, bt_address_t* addr, hfp_call_accept_t flag);
```

通过 HFP 接听来电。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `flag` 标志位。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_reject_call

```c
bt_status_t bt_hfp_hf_reject_call(bt_instance_t* ins, bt_address_t* addr);
```

通过 HFP 拒绝来电。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_hold_call

```c
bt_status_t bt_hfp_hf_hold_call(bt_instance_t* ins, bt_address_t* addr);
```

通过 HFP 保持当前通话。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_terminate_call

```c
bt_status_t bt_hfp_hf_terminate_call(bt_instance_t* ins, bt_address_t* addr);
```

通过 HFP 挂断当前通话。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_control_call

```c
bt_status_t bt_hfp_hf_control_call(bt_instance_t* ins, bt_address_t* addr, hfp_call_control_t chld, uint8_t index);
```

control通话状态。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `chld` CHLD 命令类型。
- `index` 索引。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_query_current_calls

```c
bt_status_t bt_hfp_hf_query_current_calls(bt_instance_t* ins, bt_address_t* addr, hfp_current_call_t** calls, int* num, bt_allocator_t allocator);
```

查询当前所有通话的状态信息（CLCC）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 对端设备蓝牙地址。
- `allocator` 内存分配函数。- `calls` 输出参数，存储通话信息数组。
- `num` 输出参数，存储通话数量。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_send_at_cmd

```c
bt_status_t bt_hfp_hf_send_at_cmd(bt_instance_t* ins, bt_address_t* addr, const char* cmd);
```

发送自定义 AT 命令到远程设备。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cmd` 命令。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_update_battery_level

```c
bt_status_t bt_hfp_hf_update_battery_level(bt_instance_t* ins, bt_address_t* addr, uint8_t level);
```

向远程设备更新本地电池电量信息。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `level` 安全级别。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_volume_control

```c
bt_status_t bt_hfp_hf_volume_control(bt_instance_t* ins, bt_address_t* addr, hfp_volume_type_t type, uint8_t volume);
```

通过 HFP 控制远程设备的音量。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `type` 类型。
- `volume` 音量值。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_send_dtmf

```c
bt_status_t bt_hfp_hf_send_dtmf(bt_instance_t* ins, bt_address_t* addr, char dtmf);
```

通过 HFP 发送 DTMF 按键音。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `dtmf` DTMF 按键字符。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_hf_get_subscriber_number

```c
bt_status_t bt_hfp_hf_get_subscriber_number(bt_instance_t* ins, bt_address_t* addr);
```

获取用户号码。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


### bt_hfp_hf_query_current_calls_with_callback

```c
bt_status_t bt_hfp_hf_query_current_calls_with_callback(bt_instance_t* ins, bt_address_t* addr);
```

查询当前所有通话的状态信息（CLCC），结果通过回调异步返回。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_unregister_callbacks

```c
bool bt_hfp_ag_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

取消注册回调函数，停止接收状态变更通知。

**参数**：

- `ins` 蓝牙客户端实例。
- `cookie` 用户上下文。

**返回值**：

成功时返回 `true`，失败时返回 `false`。


### bt_hfp_ag_is_connected

```c
bool bt_hfp_ag_is_connected(bt_instance_t* ins, bt_address_t* addr);
```

查询与远程设备的 HFP AG 是否已连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

已连接时返回 `true`，未连接时返回 `false`。


### bt_hfp_ag_is_audio_connected

```c
bool bt_hfp_ag_is_audio_connected(bt_instance_t* ins, bt_address_t* addr);
```

查询与远程设备的 HFP AG 音频通道是否已连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

音频已连接时返回 `true`，未连接时返回 `false`。


### bt_hfp_ag_get_connection_state

```c
profile_connection_state_t bt_hfp_ag_get_connection_state(bt_instance_t* ins, bt_address_t* addr);
```

获取与远程设备的 HFP AG 连接状态。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

返回当前连接状态枚举值，参见 `profile_connection_state_t`。


### bt_hfp_ag_connect

```c
bt_status_t bt_hfp_ag_connect(bt_instance_t* ins, bt_address_t* addr);
```

发起与远程设备的 HFP AG 连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 对端设备蓝牙地址。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_disconnect

```c
bt_status_t bt_hfp_ag_disconnect(bt_instance_t* ins, bt_address_t* addr);
```

断开与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_connect_audio

```c
bt_status_t bt_hfp_ag_connect_audio(bt_instance_t* ins, bt_address_t* addr);
```

发起与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_disconnect_audio

```c
bt_status_t bt_hfp_ag_disconnect_audio(bt_instance_t* ins, bt_address_t* addr);
```

断开与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_start_virtual_call

```c
bt_status_t bt_hfp_ag_start_virtual_call(bt_instance_t* ins, bt_address_t* addr);
```

开始操作。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_stop_virtual_call

```c
bt_status_t bt_hfp_ag_stop_virtual_call(bt_instance_t* ins, bt_address_t* addr);
```

停止操作。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_start_voice_recognition

```c
bt_status_t bt_hfp_ag_start_voice_recognition(bt_instance_t* ins, bt_address_t* addr);
```

启动远程设备的语音识别功能。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_stop_voice_recognition

```c
bt_status_t bt_hfp_ag_stop_voice_recognition(bt_instance_t* ins, bt_address_t* addr);
```

停止远程设备的语音识别功能。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_phone_state_change

```c
bt_status_t bt_hfp_ag_phone_state_change(bt_instance_t* ins, bt_address_t* addr, uint8_t num_active, uint8_t num_held, hfp_ag_call_state_t call_state, hfp_call_addrtype_t type, const char* number, const char* name);
```

通知远程设备电话状态变更（来电/通话/挂断等）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `num_active` 活跃通话数量。
- `num_held` 保持中通话数量。
- `call_state` 通话状态。
- `type` 类型。
- `number` 号码。
- `name` 名称。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_notify_device_status

```c
bt_status_t bt_hfp_ag_notify_device_status(bt_instance_t* ins, bt_address_t* addr, hfp_network_state_t network, hfp_roaming_state_t roam, uint8_t signal, uint8_t battery);
```

notify设备类型status。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `network` 网络信息。
- `roam` 漫游状态。
- `signal` 信号强度。
- `battery` 电池电量。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_volume_control

```c
bt_status_t bt_hfp_ag_volume_control(bt_instance_t* ins, bt_address_t* addr, hfp_volume_type_t type, uint8_t volume);
```

通过 HFP 控制远程设备的音量。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `type` 类型。
- `volume` 音量值。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_send_at_command

```c
bt_status_t bt_hfp_ag_send_at_command(bt_instance_t* ins, bt_address_t* addr, const char* at_command);
```

发送操作。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `at_command` AT 命令字符串。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_send_vendor_specific_at_command

```c
bt_status_t bt_hfp_ag_send_vendor_specific_at_command(bt_instance_t* ins, bt_address_t* addr, const char* command, const char* value);
```

发送操作。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `command` 命令。
- `value` 值。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_send_clcc_response

```c
bt_status_t bt_hfp_ag_send_clcc_response(bt_instance_t* ins, bt_address_t* addr, uint32_t index, hfp_call_direction_t dir, hfp_ag_call_state_t state, hfp_call_mode_t mode, hfp_call_mpty_type_t mpty, hfp_call_addrtype_t type, const char* number);
```

发送操作。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 蓝牙地址。
- `index` 索引。
- `dir` 方向（呼入/呼出）。
- `state` 状态。
- `mode` 模式。
- `mpty` 是否为多方通话。
- `type` 类型。
- `number` 通话号码。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hfp_ag_send_cind_response

```c
bt_status_t bt_hfp_ag_send_cind_response(bt_instance_t* ins, bt_address_t* addr, hfp_network_state_t network, hfp_call_t call, hfp_callheld_t call_held, hfp_callsetup_t call_setup, uint8_t signal, hfp_roaming_state_t roam, uint8_t battery);
```

发送操作。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `network` 网络信息。
- `call` 通话信息。
- `call_held` 保持中通话数量。
- `call_setup` 通话建立状态。
- `signal` 信号强度。
- `roam` 漫游状态。
- `battery` 电池电量。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。
