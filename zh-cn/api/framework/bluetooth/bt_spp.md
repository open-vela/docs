\[ [English](../../../../en/api/framework/bluetooth/bt_spp.md) | 简体中文 \]

# 蓝牙 SPP API

openvela 蓝牙 SPP（串口仿真）接口，用于替代物理串口进行数据透传。

头文件：#include "bt_spp.h"


## openvela 实现说明

- **功能**：虚拟串口通信，适用于传统串口设备的蓝牙化


## 同步接口


### bt_spp_unregister_app

```c
bt_status_t bt_spp_unregister_app(bt_instance_t* ins, void* handle);
```

取消注册 SPP 应用。

**参数**：

- `ins` 蓝牙客户端实例。
- `handle` 句柄。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_spp_server_start

```c
bt_status_t bt_spp_server_start(bt_instance_t* ins, void* handle, uint16_t scn, bt_uuid_t* uuid, uint8_t max_connection);
```

启动 SPP 服务器，监听远程设备的连接请求。

**参数**：

- `ins` 蓝牙客户端实例。
- `handle` 句柄。
- `scn` 服务器通道号。
- `uuid` 服务 UUID。
- `max_connection` 最大连接数。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_spp_server_stop

```c
bt_status_t bt_spp_server_stop(bt_instance_t* ins, void* handle, uint16_t scn);
```

停止 SPP 服务器，不再接受新连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `handle` 句柄。
- `scn` 服务器通道号。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_spp_connect

```c
bt_status_t bt_spp_connect(bt_instance_t* ins, void* handle, bt_address_t* addr, int16_t scn, bt_uuid_t* uuid, uint16_t* port);
```

发起与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `handle` 句柄。
- `addr` 远程设备蓝牙地址。
- `scn` 服务器通道号。
- `uuid` 服务 UUID。
- `port` 端口号。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_spp_insecure_connect

```c
bt_status_t bt_spp_insecure_connect(bt_instance_t* ins, void* handle, bt_address_t* addr, int16_t scn, bt_uuid_t* uuid, uint16_t* port);
```

发起与远程设备的非安全连接（不要求加密）。

**参数**：

- `ins` 蓝牙客户端实例。
- `handle` 句柄。
- `addr` 远程设备蓝牙地址。
- `scn` 服务器通道号。
- `uuid` 服务 UUID。
- `port` 端口号。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_spp_disconnect

```c
bt_status_t bt_spp_disconnect(bt_instance_t* ins, void* handle, bt_address_t* addr, uint16_t port);
```

断开连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `handle` 句柄。
- `addr` 对端设备蓝牙地址。
- `port` 端口号。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。
