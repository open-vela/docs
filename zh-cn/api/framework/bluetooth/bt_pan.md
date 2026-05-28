\[ [English](../../../../en/api/framework/bluetooth/bt_pan.md) | 简体中文 \]

# 蓝牙 PAN API

openvela 蓝牙 PAN（个人局域网）接口，支持通过蓝牙实现网络共享。

头文件：#include "bt_pan.h"


## openvela 实现说明

- **功能**：网络共享（Tethering）、蓝牙组网


## 同步接口


### bt_pan_unregister_callbacks

```c
bool bt_pan_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

取消注册回调函数，停止接收状态变更通知。

**参数**：

- `ins` 蓝牙客户端实例。
- `cookie` 用户上下文。

**返回值**：

成功时返回 `true`，失败时返回 `false`。


### bt_pan_connect

```c
bt_status_t bt_pan_connect(bt_instance_t* ins, bt_address_t* addr, uint8_t dst_role, uint8_t src_role);
```

发起与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `dst_role` 目标设备角色。
- `src_role` 本地设备角色。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_pan_disconnect

```c
bt_status_t bt_pan_disconnect(bt_instance_t* ins, bt_address_t* addr);
```

断开与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。
