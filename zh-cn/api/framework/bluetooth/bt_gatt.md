\[ [English](../../../../en/api/framework/bluetooth/bt_gatt.md) | 简体中文 \]

# 蓝牙 GATT API

openvela 蓝牙 GATT（通用属性规范）接口，支持 BLE 数据属性的读写与通知。

头文件：#include "bt_gattc.h"、#include "bt_gatts.h"


## openvela 实现说明

- **双角色支持**：Client（GATTC，发起读写请求）和 Server（GATTS，提供服务和特征值）
- **BLE 核心**：GATT 是 BLE 数据交换的基础协议


## 同步接口


### bt_gattc_create_connect

```c
bt_status_t bt_gattc_create_connect(bt_instance_t* ins, gattc_handle_t* phandle, gattc_callbacks_t* callbacks);
```

创建 GATT 客户端连接实例。

**参数**：

- `ins` 蓝牙客户端实例。
- `phandle` 输出参数，存储 GATT 客户端句柄。
- `callbacks` 回调函数集合。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_delete_connect

```c
bt_status_t bt_gattc_delete_connect(gattc_handle_t conn_handle);
```

删除 GATT 客户端连接实例，释放相关资源。

**参数**：

- `conn_handle` 连接句柄。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_connect

```c
bt_status_t bt_gattc_connect(gattc_handle_t conn_handle, bt_address_t* addr, ble_addr_type_t addr_type);
```

发起与远程设备的连接。

**参数**：

- `conn_handle` 连接句柄。
- `addr` 远程设备蓝牙地址。
- `addr_type` BLE 地址类型。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_disconnect

```c
bt_status_t bt_gattc_disconnect(gattc_handle_t conn_handle);
```

断开与远程设备的连接。

**参数**：

- `conn_handle` 连接句柄。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_discover_service

```c
bt_status_t bt_gattc_discover_service(gattc_handle_t conn_handle, bt_uuid_t* filter_uuid);
```

发现远程设备上的 GATT 服务，结果通过回调异步返回。

**参数**：

- `conn_handle` 连接句柄。
- `filter_uuid` 服务 UUID 过滤条件（NULL 表示不过滤）。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_get_attribute_by_handle

```c
bt_status_t bt_gattc_get_attribute_by_handle(gattc_handle_t conn_handle, uint16_t attr_handle, gatt_attr_desc_t* attr_desc);
```

通过属性句柄获取 GATT 属性信息。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `attr_desc` 输出参数，存储属性描述信息。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_get_attribute_by_uuid

```c
bt_status_t bt_gattc_get_attribute_by_uuid(gattc_handle_t conn_handle, uint16_t start_handle, uint16_t end_handle, bt_uuid_t* attr_uuid, gatt_attr_desc_t* attr_desc);
```

通过 UUID 获取 GATT 属性信息。

**参数**：

- `conn_handle` 连接句柄。
- `start_handle` 起始句柄。
- `end_handle` 结束句柄。
- `attr_uuid` 属性 UUID。
- `attr_desc` 输出参数，存储属性描述信息。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_read

```c
bt_status_t bt_gattc_read(gattc_handle_t conn_handle, uint16_t attr_handle);
```

读取远程设备的 GATT 特征值或描述符，结果通过回调异步返回。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_write

```c
bt_status_t bt_gattc_write(gattc_handle_t conn_handle, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

向远程设备写入 GATT 特征值或描述符，等待确认后通过回调返回结果。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `value` 值。
- `length` 长度。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_write_without_response

```c
bt_status_t bt_gattc_write_without_response(gattc_handle_t conn_handle, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

向远程设备写入 GATT 特征值（Write Without Response），不等待确认。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `value` 值。
- `length` 长度。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_write_with_signed

```c
bt_status_t bt_gattc_write_with_signed(gattc_handle_t conn_handle, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

向远程设备写入 GATT 特征值（Signed Write），使用签名认证。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `value` 值。
- `length` 长度。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_subscribe

```c
bt_status_t bt_gattc_subscribe(gattc_handle_t conn_handle, uint16_t attr_handle, uint16_t ccc_value);
```

订阅远程设备的 GATT 特征值通知或指示（Notification/Indication）。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `ccc_value` CCCD 值（0 禁用，1 通知，2 指示）。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_unsubscribe

```c
bt_status_t bt_gattc_unsubscribe(gattc_handle_t conn_handle, uint16_t attr_handle);
```

取消订阅远程设备的 GATT 特征值通知或指示。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_exchange_mtu

```c
bt_status_t bt_gattc_exchange_mtu(gattc_handle_t conn_handle, uint32_t mtu);
```

与远程设备协商 ATT MTU 大小，影响单次数据传输的最大长度。

**参数**：

- `conn_handle` 连接句柄。
- `mtu` MTU 值。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_update_connection_parameter

```c
bt_status_t bt_gattc_update_connection_parameter(gattc_handle_t conn_handle, uint32_t min_interval, uint32_t max_interval, uint32_t latency, uint32_t timeout, uint32_t min_connection_event_length, uint32_t max_connection_event_length);
```

更新 BLE 连接参数。

**参数**：

- `conn_handle` 连接句柄。
- `min_interval` 最小间隔。
- `max_interval` 最大间隔。
- `latency` 从设备延迟。
- `timeout` 超时时间。
- `min_connection_event_length` 最小连接事件长度。
- `max_connection_event_length` 最大连接事件长度。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_read_phy

```c
bt_status_t bt_gattc_read_phy(gattc_handle_t conn_handle);
```

读取当前连接的 PHY 配置，结果通过回调异步返回。

**参数**：

- `conn_handle` 连接句柄。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_update_phy

```c
bt_status_t bt_gattc_update_phy(gattc_handle_t conn_handle, ble_phy_type_t tx_phy, ble_phy_type_t rx_phy);
```

PHY 配置操作。

**参数**：

- `conn_handle` 连接句柄。
- `tx_phy` 发送 PHY。
- `rx_phy` 接收 PHY。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gattc_read_rssi

```c
bt_status_t bt_gattc_read_rssi(gattc_handle_t conn_handle);
```

读取远程设备的 RSSI 值，结果通过回调异步返回。

**参数**：

- `conn_handle` 连接句柄。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_register_service

```c
bt_status_t bt_gatts_register_service(bt_instance_t* ins, gatts_handle_t* phandle, gatts_callbacks_t* callbacks);
```

注册 GATT 服务。

**参数**：

- `ins` 蓝牙客户端实例。
- `phandle` 输出参数，存储 GATT 服务句柄。
- `callbacks` 回调函数集合。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。



### bt_gatts_unregister_service

```c
bt_status_t bt_gatts_unregister_service(gatts_handle_t srv_handle);
```

取消注册 GATT 服务。

**参数**：

- `srv_handle` GATT 服务句柄。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_connect

```c
bt_status_t bt_gatts_connect(gatts_handle_t srv_handle, bt_address_t* addr, ble_addr_type_t addr_type);
```

发起与远程设备的连接。

**参数**：

- `srv_handle` GATT 服务句柄。
- `addr` 远程设备蓝牙地址。
- `addr_type` BLE 地址类型。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_connect_bear

```c
bt_status_t bt_gatts_connect_bear(gatts_handle_t srv_handle, bt_address_t* addr, ble_addr_type_t addr_type, uint8_t bear_type);
```

发起与远程设备的连接。

**参数**：

- `srv_handle` GATT 服务句柄。
- `addr` 远程设备蓝牙地址。
- `addr_type` BLE 地址类型。
- `bear_type` 承载类型。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_disconnect

```c
bt_status_t bt_gatts_disconnect(gatts_handle_t srv_handle, bt_address_t* addr);
```

断开与远程设备的连接。

**参数**：

- `srv_handle` GATT 服务句柄。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_add_attr_table

```c
bt_status_t bt_gatts_add_attr_table(gatts_handle_t srv_handle, gatt_srv_db_t* srv_db);
```

向本地 GATT 服务器添加属性表（服务、特征值、描述符）。

**参数**：

- `srv_handle` GATT 服务句柄。
- `srv_db` GATT 服务属性表。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_remove_attr_table

```c
bt_status_t bt_gatts_remove_attr_table(gatts_handle_t srv_handle, uint16_t attr_handle);
```

从本地 GATT 服务器移除属性表。

**参数**：

- `srv_handle` GATT 服务句柄。
- `attr_handle` 属性句柄。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_set_attr_value

```c
bt_status_t bt_gatts_set_attr_value(gatts_handle_t srv_handle, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

设置本地 GATT 属性的值。

**参数**：

- `srv_handle` GATT 服务句柄。
- `attr_handle` 属性句柄。
- `value` 值。
- `length` 长度。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_get_attr_value

```c
bt_status_t bt_gatts_get_attr_value(gatts_handle_t srv_handle, uint16_t attr_handle, uint8_t* value, uint16_t* length);
```

获取本地 GATT 属性的值。

**参数**：

- `srv_handle` GATT 服务句柄。
- `attr_handle` 属性句柄。
- `value` 值。
- `length` 长度。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_response

```c
bt_status_t bt_gatts_response(gatts_handle_t srv_handle, bt_address_t* addr, uint32_t req_handle, uint8_t* value, uint16_t length);
```

回复远程设备的 GATT 读写请求。

**参数**：

- `srv_handle` GATT 服务句柄。
- `addr` 远程设备蓝牙地址。
- `req_handle` 请求句柄。
- `value` 值。
- `length` 长度。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_notify

```c
bt_status_t bt_gatts_notify(gatts_handle_t srv_handle, bt_address_t* addr, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

向已订阅的远程设备发送 GATT 通知（Notification），不需要确认。

**参数**：

- `srv_handle` GATT 服务句柄。
- `addr` 远程设备蓝牙地址。
- `attr_handle` 属性句柄。
- `value` 值。
- `length` 长度。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_indicate

```c
bt_status_t bt_gatts_indicate(gatts_handle_t srv_handle, bt_address_t* addr, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

向已订阅的远程设备发送 GATT 指示（Indication），需要确认。

**参数**：

- `srv_handle` GATT 服务句柄。
- `addr` 远程设备蓝牙地址。
- `attr_handle` 属性句柄。
- `value` 值。
- `length` 长度。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_read_phy

```c
bt_status_t bt_gatts_read_phy(gatts_handle_t srv_handle, bt_address_t* addr);
```

读取 PHY 配置。

**参数**：

- `srv_handle` GATT 服务句柄。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_gatts_update_phy

```c
bt_status_t bt_gatts_update_phy(gatts_handle_t srv_handle, bt_address_t* addr, ble_phy_type_t tx_phy, ble_phy_type_t rx_phy);
```

PHY 配置操作。

**参数**：

- `srv_handle` GATT 服务句柄。
- `addr` 远程设备蓝牙地址。
- `tx_phy` 发送 PHY。
- `rx_phy` 接收 PHY。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


## 异步接口


### bt_gattc_create_connect_async

```c
bt_status_t bt_gattc_create_connect_async(bt_instance_t* ins, gattc_handle_t* phandle, gattc_callbacks_t* callbacks, bt_gattc_create_connect_cb_t cb, void* userdata);
```

建立连接（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `phandle` 输出参数，存储 GATT 客户端句柄。
- `callbacks` 回调函数集合。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_gattc_delete_connect_async

```c
bt_status_t bt_gattc_delete_connect_async(gattc_handle_t conn_handle, bt_status_cb_t bt_gattc_delete_connect_cb_t, void* userdata);
```

删除 GATT 客户端（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `bt_gattc_delete_connect_cb_t` 删除连接的回调函数。
- `userdata` 用户数据。



### bt_gattc_connect_async

```c
bt_status_t bt_gattc_connect_async(gattc_handle_t conn_handle, bt_address_t* addr, ble_addr_type_t addr_type, bt_status_cb_t cb, void* userdata);
```

建立连接（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `addr` 远程设备蓝牙地址。
- `addr_type` BLE 地址类型。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_gattc_disconnect_async

```c
bt_status_t bt_gattc_disconnect_async(gattc_handle_t conn_handle, bt_status_cb_t cb, void* userdata);
```

断开 ATT 承载连接（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_gattc_discover_service_async

```c
bt_status_t bt_gattc_discover_service_async(gattc_handle_t conn_handle, bt_uuid_t* filter_uuid, bt_status_cb_t cb, void* userdata);
```

发现GATT 服务（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `filter_uuid` 服务 UUID 过滤条件（NULL 表示不过滤）。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_gattc_get_attribute_by_handle_async

```c
bt_status_t bt_gattc_get_attribute_by_handle_async(gattc_handle_t conn_handle, uint16_t attr_handle, bt_gattc_get_attribute_cb_t cb, void* userdata);
```

通过属性句柄获取属性（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_gattc_get_attribute_by_uuid_async

```c
bt_status_t bt_gattc_get_attribute_by_uuid_async(gattc_handle_t conn_handle, uint16_t start_handle, uint16_t end_handle, bt_uuid_t* attr_uuid, bt_gattc_get_attribute_cb_t cb, void* userdata);
```

获取属性（按 UUID）（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `start_handle` 起始句柄。
- `end_handle` 结束句柄。
- `attr_uuid` 属性 UUID。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_gattc_read_async

```c
bt_status_t bt_gattc_read_async(gattc_handle_t conn_handle, uint16_t attr_handle, bt_status_cb_t cb, void* userdata);
```

通过句柄读取属性值（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_gattc_write_async

```c
bt_status_t bt_gattc_write_async(gattc_handle_t conn_handle, uint16_t attr_handle, uint8_t* value, uint16_t length, bt_status_cb_t cb, void* userdata);
```

写入操作（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `value` 值。
- `length` 长度。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_gattc_write_without_response_async

```c
bt_status_t bt_gattc_write_without_response_async(gattc_handle_t conn_handle, uint16_t attr_handle, uint8_t* value, uint16_t length, bt_gattc_write_cb_t cb, void* userdata);
```

向指定属性写入数据（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `value` 值。
- `length` 长度。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_gattc_subscribe_async

```c
bt_status_t bt_gattc_subscribe_async(gattc_handle_t conn_handle, uint16_t attr_handle, uint16_t ccc_value, bt_status_cb_t cb, void* userdata);
```

订阅操作（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `ccc_value` CCCD 值（0 禁用，1 通知，2 指示）。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_gattc_unsubscribe_async

```c
bt_status_t bt_gattc_unsubscribe_async(gattc_handle_t conn_handle, uint16_t attr_handle, bt_status_cb_t cb, void* userdata);
```

禁用指定的 CCCD（客户端特征配置描述符）（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `attr_handle` 属性句柄。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_gattc_exchange_mtu_async

```c
bt_status_t bt_gattc_exchange_mtu_async(gattc_handle_t conn_handle, uint32_t mtu, bt_status_cb_t cb, void* userdata);
```

交换 MTU 大小（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `mtu` MTU 值。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_gattc_update_connection_parameter_async

```c
bt_status_t bt_gattc_update_connection_parameter_async(gattc_handle_t conn_handle, uint32_t min_interval, uint32_t max_interval, uint32_t latency, uint32_t timeout, uint32_t min_connection_event_length, uint32_t max_connection_event_length, bt_status_cb_t cb, void* userdata);
```

修改 BLE 连接参数（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `min_interval` 最小间隔。
- `max_interval` 最大间隔。
- `latency` 从设备延迟。
- `timeout` 超时时间。
- `min_connection_event_length` 最小连接事件长度。
- `max_connection_event_length` 最大连接事件长度。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_gattc_read_phy_async

```c
bt_status_t bt_gattc_read_phy_async(gattc_handle_t conn_handle, bt_status_cb_t cb, void* userdata);
```

读取PHY 配置（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_gattc_update_phy_async

```c
bt_status_t bt_gattc_update_phy_async(gattc_handle_t conn_handle, ble_phy_type_t tx_phy, ble_phy_type_t rx_phy, bt_status_cb_t cb, void* userdata);
```

更新 PHY 配置（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `tx_phy` 发送 PHY。
- `rx_phy` 接收 PHY。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_gattc_read_rssi_async

```c
bt_status_t bt_gattc_read_rssi_async(gattc_handle_t conn_handle, bt_status_cb_t cb, void* userdata);
```

读取 RSSI 值（异步版本）。

**参数**：

- `conn_handle` 连接句柄。
- `cb` 回调函数。
- `userdata` 用户数据。

