\[ [English](../../../../en/api/framework/bluetooth/bt_avrcp.md) | 简体中文 \]

# 蓝牙 AVRCP API

openvela 蓝牙 AVRCP（音视频远程控制）接口，支持播放控制、曲目信息查询等。

头文件：#include "bt_avrcp.h"、#include "bt_avrcp_control.h"、#include "bt_avrcp_target.h"


## openvela 实现说明

- **双角色支持**：Controller（控制端）和 Target（目标端）
- **功能**：播放/暂停/切歌、音量控制、曲目信息获取


## 同步接口


### bt_avrcp_control_unregister_callbacks

```c
bool bt_avrcp_control_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

取消注册回调函数，停止接收状态变更通知。

**参数**：

- `ins` 蓝牙客户端实例。
- `cookie` 用户上下文。

**返回值**：

取消注册回调函数。


### bt_avrcp_control_get_element_attributes

```c
bt_status_t bt_avrcp_control_get_element_attributes(bt_instance_t* ins, bt_address_t* addr);
```

获取媒体元素属性。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_avrcp_control_send_passthrough_cmd

```c
bt_status_t bt_avrcp_control_send_passthrough_cmd(bt_instance_t* ins, bt_address_t* addr, uint8_t cmd, uint8_t state);
```

发送透传命令。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cmd` 命令。
- `state` 状态。


### bt_avrcp_control_get_unit_info

```c
bt_status_t bt_avrcp_control_get_unit_info(bt_instance_t* ins, bt_address_t* addr);
```

获取远程 AVRCP 设备的单元信息。


**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 蓝牙地址。


### bt_avrcp_control_get_subunit_info

```c
bt_status_t bt_avrcp_control_get_subunit_info(bt_instance_t* ins, bt_address_t* addr);
```

获取子单元信息。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


### bt_avrcp_control_get_playback_state

```c
bt_status_t bt_avrcp_control_get_playback_state(bt_instance_t* ins, bt_address_t* addr);
```

获取远程设备的当前播放状态。


**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 蓝牙地址。


### bt_avrcp_control_register_notification

```c
bt_status_t bt_avrcp_control_register_notification(bt_instance_t* ins, bt_address_t* addr, uint8_t event, uint32_t interval);
```

注册事件通知。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `event` 事件类型。
- `interval` 间隔。


### bt_avrcp_target_unregister_callbacks

```c
bool bt_avrcp_target_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

取消注册回调函数，停止接收状态变更通知。

**参数**：

- `ins` 蓝牙客户端实例。
- `cookie` 用户上下文。



- `cookie` 用户上下文。
- `ins` 蓝牙客户端实例。

**返回值**：

成功时返回回调 cookie，失败或已注册时返回 NULL。


### bt_avrcp_target_get_play_status_response

```c
bt_status_t bt_avrcp_target_get_play_status_response(bt_instance_t* ins, bt_address_t* addr, avrcp_play_status_t status, uint32_t song_len, uint32_t song_pos);
```

回复播放状态查询。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 蓝牙地址 of the peer device.
- `status` 状态码。
- `song_len` 歌曲长度（毫秒）。
- `song_pos` 当前播放位置（毫秒）。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_avrcp_target_play_status_notify

```c
bt_status_t bt_avrcp_target_play_status_notify(bt_instance_t* ins, bt_address_t* addr, avrcp_play_status_t status);
```

通知播放状态变更。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `status` 状态码。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。
