\[ [English](../../../../en/api/framework/bluetooth/bt_device.md) | 简体中文 \]

# 蓝牙设备管理 API

openvela 蓝牙远程设备管理接口，提供设备配对、连接、属性查询和管理功能。

头文件：`#include "bt_device.h"`


## openvela 实现说明

- **设备属性**：支持查询远程设备名称、地址、类型、配对状态、连接状态等
- **配对管理**：支持发起配对、取消配对、确认配对请求
- **连接管理**：支持建立和断开与远程设备的连接
- **异步模式**：大部分 API 提供同步和异步两个版本


## 同步接口


### bt_device_get_identity_address

```c
bt_status_t bt_device_get_identity_address(bt_instance_t* ins, bt_address_t* bd_addr, bt_address_t* id_addr);
```

获取远程设备的身份地址（Identity Address），用于标识使用随机地址的 BLE 设备。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `bd_addr` 远程设备 BLE 地址。- `id_addr` 输出参数，存储身份地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_device_get_address_type

```c
ble_addr_type_t bt_device_get_address_type(bt_instance_t* ins, bt_address_t* addr);
```

获取远程设备的 BLE 地址类型（Public/Static Random/RPA 等）。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.

**返回值**：

返回设备的 BLE 地址类型，未找到时返回 `BLE_ADDR_TYPE_UNKNOWN`。


### bt_device_get_device_type

```c
bt_device_type_t bt_device_get_device_type(bt_instance_t* ins, bt_address_t* addr);
```

获取远程设备的类型（经典蓝牙/BLE/双模）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

返回设备类型枚举值，参见 `bt_device_type_t`。



### bt_device_get_name

```c
bool bt_device_get_name(bt_instance_t* ins, bt_address_t* addr, char* name, uint32_t length);
```

获取远程设备的蓝牙名称。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `name` 输出缓冲区，用于存储设备名称。
- `length` 缓冲区长度。


**返回值**：

成功时返回 `true`，失败时返回 `false`。


### bt_device_get_device_class

```c
uint32_t bt_device_get_device_class(bt_instance_t* ins, bt_address_t* addr);
```

获取远程设备的设备类型（Class of Device），包含主设备类、子设备类和服务类信息。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.

**返回值**：

返回 24 位 Class of Device 值，包含主设备类、子设备类和服务类信息。



### bt_device_get_uuids

```c
bt_status_t bt_device_get_uuids(bt_instance_t* ins, bt_address_t* addr, bt_uuid_t** uuids, uint16_t* size, bt_allocator_t allocator);
```

获取远程设备支持的服务 UUID 列表。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.
- `allocator` 内存分配函数。- `uuids` UUID 数组（由 allocator 分配）。
- `size` 返回 UUID 数量。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_device_get_appearance

```c
uint16_t bt_device_get_appearance(bt_instance_t* ins, bt_address_t* addr);
```

获取远程设备的 BLE 外观特征值（Appearance），用于标识设备的物理外观。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.


### bt_device_get_rssi

```c
int8_t bt_device_get_rssi(bt_instance_t* ins, bt_address_t* addr);
```

获取远程设备的接收信号强度指示（RSSI）。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.


### bt_device_get_alias

```c
bool bt_device_get_alias(bt_instance_t* ins, bt_address_t* addr, char* alias, uint32_t length);
```

获取远程设备的用户自定义别名，未设置时返回设备名称。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.
- `length` 缓冲区长度。
- `alias` 输出参数，存储别名字符串。


**返回值**：

成功时返回 `true`，失败时返回 `false`。


### bt_device_set_alias

```c
bt_status_t bt_device_set_alias(bt_instance_t* ins, bt_address_t* addr, const char* alias);
```

设置远程设备的用户自定义别名，长度不超过 BT_LOC_NAME_MAX_LEN。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.
- `alias` 设备别名。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_is_connected

```c
bool bt_device_is_connected(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

查询与远程设备是否已建立连接。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.
- `transport` Transport type, 参见 bt_transport_t.

**返回值**：

已连接时返回 `true`，未连接时返回 `false`。


### bt_device_is_encrypted

```c
bool bt_device_is_encrypted(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

查询与远程设备的连接是否已加密。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.
- `transport` Transport type, 参见 bt_transport_t.

**返回值**：

已加密时返回 `true`，未加密时返回 `false`。


### bt_device_is_bond_initiate_local

```c
bool bt_device_is_bond_initiate_local(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

查询与远程设备的配对是否由本地发起。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.
- `transport` Transport type, 参见 bt_transport_t.

**返回值**：

由本地发起时返回 `true`，否则返回 `false`。


### bt_device_get_bond_state

```c
bond_state_t bt_device_get_bond_state(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

获取与远程设备的配对状态。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。


**返回值**：

返回当前配对状态，参见 bond_state_t。


### bt_device_is_bonded

```c
bool bt_device_is_bonded(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

查询远程设备是否已配对。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。


**返回值**：

已配对时返回 `true`，未配对时返回 `false`。


### bt_device_create_bond

```c
bt_status_t bt_device_create_bond(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

发起与远程设备的配对（Bonding），建立长期安全关系。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_set_security_level

```c
bt_status_t bt_device_set_security_level(bt_instance_t* ins, uint8_t level, bt_transport_t transport);
```

设置与远程设备的安全级别（0~4），级别越高安全性越强。

**参数**：

- `ins` 蓝牙客户端实例。
- `level` 安全级别。
- `transport` 传输类型（BR/EDR 或 BLE）。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_device_set_bondable_le

```c
bt_status_t bt_device_set_bondable_le(bt_instance_t* ins, bool bondable);
```

设置远程设备是否允许 BLE 配对。

**参数**：

- `ins` 蓝牙客户端实例。
- `bondable` 是否可配对。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_device_remove_bond

```c
bt_status_t bt_device_remove_bond(bt_instance_t* ins, bt_address_t* addr, uint8_t transport);
```

移除与远程设备的配对关系，删除存储的配对密钥。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_cancel_bond

```c
bt_status_t bt_device_cancel_bond(bt_instance_t* ins, bt_address_t* addr);
```

取消正在进行的配对过程。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_pair_request_reply

```c
bt_status_t bt_device_pair_request_reply(bt_instance_t* ins, bt_address_t* addr, bool accept);
```

回复远程设备的配对请求，接受或拒绝配对。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `accept` 是否接受。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_set_pairing_confirmation

```c
bt_status_t bt_device_set_pairing_confirmation(bt_instance_t* ins, bt_address_t* addr, uint8_t transport, bool accept);
```

确认或拒绝 SSP 配对的数字比较请求。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `accept` 是否接受。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_set_pin_code

```c
bt_status_t bt_device_set_pin_code(bt_instance_t* ins, bt_address_t* addr, bool accept, char* pincode, int len);
```

设置 PIN 码用于传统配对认证。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `accept` 是否接受。
- `pincode` PIN 码字符串。
- `len` 长度。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_set_pass_key

```c
bt_status_t bt_device_set_pass_key(bt_instance_t* ins, bt_address_t* addr, uint8_t transport, bool accept, uint32_t passkey);
```

设置数字密钥用于 SSP 配对认证。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `accept` 是否接受。
- `passkey` 配对密钥。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_set_le_legacy_tk

```c
bt_status_t bt_device_set_le_legacy_tk(bt_instance_t* ins, bt_address_t* addr, bt_128key_t tk_val);
```

设置 BLE Legacy 配对 TK 值。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `tk_val` OOB TK 值。


### bt_device_set_le_sc_remote_oob_data

```c
bt_status_t bt_device_set_le_sc_remote_oob_data(bt_instance_t* ins, bt_address_t* addr, bt_128key_t c_val, bt_128key_t r_val);
```

设置远程设备的 BLE Secure Connections OOB 数据，用于带外配对。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `c_val` SC 确认值（128 位）。
- `r_val` SC 随机值（128 位）。



- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.
- `c_val` LE 安全连接确认值（128 位密钥）。
- `r_val` LE 安全连接随机值（128 位密钥）。


### bt_device_get_le_sc_local_oob_data

```c
bt_status_t bt_device_get_le_sc_local_oob_data(bt_instance_t* ins, bt_address_t* addr);
```

获取 BLE SC 本地 OOB 数据。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_connect

```c
bt_status_t bt_device_connect(bt_instance_t* ins, bt_address_t* addr);
```

发起与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_background_connect

```c
bt_status_t bt_device_background_connect(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

发起与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_device_disconnect

```c
bt_status_t bt_device_disconnect(bt_instance_t* ins, bt_address_t* addr);
```

断开与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。


### bt_device_background_disconnect

```c
bt_status_t bt_device_background_disconnect(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

断开与远程设备的连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


### bt_device_connect_le

```c
bt_status_t bt_device_connect_le(bt_instance_t* ins, bt_address_t* addr, ble_addr_type_t type, ble_connect_params_t* param);
```

发起与远程设备的 BLE 连接。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 蓝牙地址。
- `type` LE address type, 参见 ble_addr_type_t.
- `param` 指向 connection parameters, 参见 ble_connect_params_t.


### bt_device_disconnect_le

```c
bt_status_t bt_device_disconnect_le(bt_instance_t* ins, bt_address_t* addr);
```

断开与远程设备的 BLE 连接。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 蓝牙地址。


### bt_device_connect_request_reply

```c
bt_status_t bt_device_connect_request_reply(bt_instance_t* ins, bt_address_t* addr, bool accept);
```

回复远程设备的连接请求，接受或拒绝连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `accept` 是否接受。


### bt_device_set_le_phy

```c
bt_status_t bt_device_set_le_phy(bt_instance_t* ins, bt_address_t* addr, ble_phy_type_t tx_phy, ble_phy_type_t rx_phy);
```

设置与远程设备的 BLE PHY 配置（1M/2M/Coded）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `tx_phy` 发送 PHY。
- `rx_phy` 接收 PHY。



- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 蓝牙地址。
- `tx_phy` Preferred TX PHY, 参见 ble_phy_type_t.
- `rx_phy` Preferred RX PHY, 参见 ble_phy_type_t.


### bt_device_connect_all_profile

```c
void bt_device_connect_all_profile(bt_instance_t* ins, bt_address_t* addr);
```

连接所有 Profile 连接。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。


### bt_device_disconnect_all_profile

```c
void bt_device_disconnect_all_profile(bt_instance_t* ins, bt_address_t* addr);
```

断开与远程设备的所有 Profile 连接。


**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。




### bt_device_enable_enhanced_mode

```c
bt_status_t bt_device_enable_enhanced_mode(bt_instance_t* ins, bt_address_t* addr, bt_enhanced_mode_t mode);
```

启用与远程设备的增强模式。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `mode` 模式。


### bt_device_disable_enhanced_mode

```c
bt_status_t bt_device_disable_enhanced_mode(bt_instance_t* ins, bt_address_t* addr, bt_enhanced_mode_t mode);
```

禁用与远程设备的增强模式。


**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 远程设备地址.
- `mode` Enhanced mode to disable, 参见 bt_enhanced_mode_t.


## 异步接口


### bt_device_get_identity_address_async

```c
bt_status_t bt_device_get_identity_address_async(bt_instance_t* ins, bt_address_t* bd_addr, bt_address_cb_t cb, void* userdata);
```

获取身份地址（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `bd_addr` BLE 地址。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_get_address_type_async

```c
bt_status_t bt_device_get_address_type_async(bt_instance_t* ins, bt_address_t* addr, bt_device_get_address_type_cb_t cb, void* userdata);
```

获取远程设备的 BLE 地址类型。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_get_device_type_async

```c
bt_status_t bt_device_get_device_type_async(bt_instance_t* ins, bt_address_t* addr, bt_device_type_cb_t cb, void* userdata);
```

获取设备类型（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_get_name_async

```c
bt_status_t bt_device_get_name_async(bt_instance_t* ins, bt_address_t* addr, bt_string_cb_t cb, void* userdata);
```

获取远程设备名称（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_get_device_class_async

```c
bt_status_t bt_device_get_device_class_async(bt_instance_t* ins, bt_address_t* addr, bt_u32_cb_t cb, void* userdata);
```

获取设备类型（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_get_uuids_async

```c
bt_status_t bt_device_get_uuids_async(bt_instance_t* ins, bt_address_t* addr, bt_uuids_cb_t cb, void* userdata);
```

获取远程设备支持的 UUID 列表。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_get_appearance_async

```c
bt_status_t bt_device_get_appearance_async(bt_instance_t* ins, bt_address_t* addr, bt_u16_cb_t cb, void* userdata);
```

获取外观特征值（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_get_rssi_async

```c
bt_status_t bt_device_get_rssi_async(bt_instance_t* ins, bt_address_t* addr, bt_s8_cb_t cb, void* userdata);
```

获取远程设备的 RSSI（接收信号强度）。（异步版本）

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_get_alias_async

```c
bt_status_t bt_device_get_alias_async(bt_instance_t* ins, bt_address_t* addr, bt_string_cb_t cb, void* userdata);
```

获取别名（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_set_alias_async

```c
bt_status_t bt_device_set_alias_async(bt_instance_t* ins, bt_address_t* addr, const char* alias, bt_status_cb_t cb, void* userdata);
```

设置远程设备的别名。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `alias` 别名。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_is_connected_async

```c
bt_status_t bt_device_is_connected_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_bool_cb_t cb, void* userdata);
```

检查是否已连接（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_is_encrypted_async

```c
bt_status_t bt_device_is_encrypted_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_bool_cb_t cb, void* userdata);
```

检查与远程设备的连接是否已加密。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_is_bond_initiate_local_async

```c
bt_status_t bt_device_is_bond_initiate_local_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_bool_cb_t cb, void* userdata);
```

查询配对是否由本地发起（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_get_bond_state_async

```c
bt_status_t bt_device_get_bond_state_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_device_get_bond_state_cb_t cb, void* userdata);
```

获取与远程设备的配对状态（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_is_bonded_async

```c
bt_status_t bt_device_is_bonded_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_bool_cb_t cb, void* userdata);
```

查询是否已配对（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_connect_async

```c
bt_status_t bt_device_connect_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

连接远程设备（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_disconnect_async

```c
bt_status_t bt_device_disconnect_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

断开连接（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_connect_le_async

```c
bt_status_t bt_device_connect_le_async(bt_instance_t* ins, bt_address_t* addr, ble_addr_type_t type, ble_connect_params_t* param, bt_status_cb_t cb, void* userdata);
```

连接远程 BLE 设备（异步版本，支持指定连接参数）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `type` 类型。
- `param` 连接参数结构体。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_disconnect_le_async

```c
bt_status_t bt_device_disconnect_le_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

断开BLE 连接（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_connect_request_reply_async

```c
bt_status_t bt_device_connect_request_reply_async(bt_instance_t* ins, bt_address_t* addr, bool accept, bt_status_cb_t cb, void* userdata);
```

回复连接请求（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `accept` 是否接受。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_connect_all_profile_async

```c
bt_status_t bt_device_connect_all_profile_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

连接所有 Profile 连接（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_disconnect_all_profile_async

```c
bt_status_t bt_device_disconnect_all_profile_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

断开所有 Profile 连接（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_set_le_phy_async

```c
bt_status_t bt_device_set_le_phy_async(bt_instance_t* ins, bt_address_t* addr, ble_phy_type_t tx_phy, ble_phy_type_t rx_phy, bt_status_cb_t cb, void* userdata);
```

设置BLE PHY 配置（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `tx_phy` 发送 PHY。
- `rx_phy` 接收 PHY。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_create_bond_async

```c
bt_status_t bt_device_create_bond_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_status_cb_t cb, void* userdata);
```

发起与远程设备的配对（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_remove_bond_async

```c
bt_status_t bt_device_remove_bond_async(bt_instance_t* ins, bt_address_t* addr, uint8_t transport, bt_status_cb_t cb, void* userdata);
```

取消配对（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_cancel_bond_async

```c
bt_status_t bt_device_cancel_bond_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

取消正在进行的配对（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_pair_request_reply_async

```c
bt_status_t bt_device_pair_request_reply_async(bt_instance_t* ins, bt_address_t* addr, bool accept, bt_status_cb_t cb, void* userdata);
```

配对配对请求回复（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `accept` 是否接受。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_set_pairing_confirmation_async

```c
bt_status_t bt_device_set_pairing_confirmation_async(bt_instance_t* ins, bt_address_t* addr, uint8_t transport, bool accept, bt_status_cb_t cb, void* userdata);
```

设置安全配对确认（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `accept` 是否接受。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_set_pin_code_async

```c
bt_status_t bt_device_set_pin_code_async(bt_instance_t* ins, bt_address_t* addr, bool accept, char* pincode, int len, bt_status_cb_t cb, void* userdata);
```

设置 PIN 码（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `accept` 是否接受。
- `pincode` PIN 码字符串。
- `len` 长度。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_set_pass_key_async

```c
bt_status_t bt_device_set_pass_key_async(bt_instance_t* ins, bt_address_t* addr, uint8_t transport, bool accept, uint32_t passkey, bt_status_cb_t cb, void* userdata);
```

设置配对密钥（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `accept` 是否接受。
- `passkey` 配对密钥。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_set_le_legacy_tk_async

```c
bt_status_t bt_device_set_le_legacy_tk_async(bt_instance_t* ins, bt_address_t* addr, bt_128key_t tk_val, bt_status_cb_t cb, void* userdata);
```

设置 BLE Legacy 配对 TK 值（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `tk_val` OOB TK 值。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_device_set_le_sc_remote_oob_data_async

```c
bt_status_t bt_device_set_le_sc_remote_oob_data_async(bt_instance_t* ins, bt_address_t* addr, bt_128key_t c_val, bt_128key_t r_val, bt_status_cb_t cb, void* userdata);
```

设置 LE SC 配对的远程 OOB 数据（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `c_val` SC 确认值。
- `r_val` SC 随机值。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_device_get_le_sc_local_oob_data_async

```c
bt_status_t bt_device_get_le_sc_local_oob_data_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

获取 LE SC 配对的本地 OOB 数据（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。

