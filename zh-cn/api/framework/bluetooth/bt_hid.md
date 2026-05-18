\[ [English](../../../../en/api/framework/bluetooth/bt_hid.md) | 简体中文 \]

# 蓝牙 HID API

openvela 蓝牙 HID（人机接口设备）接口，支持键盘、鼠标、游戏手柄等输入设备。

头文件：#include "bt_hid_device.h"


## openvela 实现说明

- **设备角色**：HID Device（输入设备端）


## 同步接口


### bt_hid_device_unregister_callbacks

```c
bool bt_hid_device_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

取消注册回调函数，停止接收状态变更通知。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `cookie` 用户上下文。

**返回值**：

成功时返回 `true`，失败时返回 `false`。


### bt_hid_device_register_app

```c
bt_status_t bt_hid_device_register_app(bt_instance_t* ins, hid_device_sdp_settings_t* sdp_setting, bool le_hid);
```

注册操作。

**参数**：

- `ins` 蓝牙客户端实例。
- `sdp_setting` SDP 设置。
- `le_hid` LE HID 实例。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_hid_device_unregister_app

```c
bt_status_t bt_hid_device_unregister_app(bt_instance_t* ins);
```

取消注册 HID 设备应用。

**参数**：

- `ins` 蓝牙客户端实例。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hid_device_connect

```c
bt_status_t bt_hid_device_connect(bt_instance_t* ins, bt_address_t* addr);
```

发起与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_hid_device_disconnect

```c
bt_status_t bt_hid_device_disconnect(bt_instance_t* ins, bt_address_t* addr);
```

断开与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_hid_device_send_report

```c
bt_status_t bt_hid_device_send_report(bt_instance_t* ins, bt_address_t* addr, uint8_t rpt_id, uint8_t* rpt_data, int rpt_size);
```

向已连接的主机发送 HID 输入报告。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `rpt_id` HID 报告 ID。
- `rpt_data` HID 报告数据。
- `rpt_size` 报告数据大小（字节）。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_hid_device_response_report

```c
bt_status_t bt_hid_device_response_report(bt_instance_t* ins, bt_address_t* addr, uint8_t rpt_type, uint8_t* rpt_data, int rpt_size);
```

回复主机的 HID 报告请求。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `rpt_type` HID 报告类型（输入/输出/特性）。
- `rpt_data` HID 报告数据。
- `rpt_size` 报告数据大小（字节）。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hid_device_report_error

```c
bt_status_t bt_hid_device_report_error(bt_instance_t* ins, bt_address_t* addr, hid_status_error_t error);
```

向主机报告 HID 错误。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `error` 错误码，参见 `hid_status_error_t`。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_hid_device_virtual_unplug

```c
bt_status_t bt_hid_device_virtual_unplug(bt_instance_t* ins, bt_address_t* addr);
```

发送虚拟拔出请求，断开 HID 连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。
