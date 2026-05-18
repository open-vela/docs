\[ [English](../../../../en/api/framework/bluetooth/bt_gap.md) | 简体中文 \]

# 蓝牙 GAP API

openvela 蓝牙 GAP（通用访问规范）接口提供蓝牙适配器的管理功能，包括启用/禁用、设备发现、属性配置、配对管理等。

头文件：`#include "bt_adapter.h"`

## openvela 实现说明

- **双模支持**：支持经典蓝牙（BR/EDR）和低功耗蓝牙（BLE）独立控制
- **异步模式**：大部分 API 提供同步和异步两个版本，异步版本以 `_async` 后缀命名，通过回调返回结果
- **实例管理**：所有 API 的第一个参数为 `bt_instance_t* ins`（蓝牙客户端实例），通过 `bt_open()` 获取
- **状态机**：适配器状态遵循 OFF → BLE_TURNING_ON → BLE_ON → TURNING_ON → ON 的转换流程


## 适配器控制


#### bt_adapter_get_state

```c
bt_adapter_state_t bt_adapter_get_state(bt_instance_t* ins);
```

获取适配器状态。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.

**返回值**：

返回当前适配器状态枚举值，参见 `bt_adapter_state_t`。


#### bt_adapter_is_support_le

```c
bool bt_adapter_is_support_le(bt_instance_t* ins);
```

查询是否支持 BLE。

**参数**：

- `ins` 蓝牙客户端实例。


**返回值**：

支持时返回 `true`，不支持时返回 `false`。


#### bt_adapter_is_support_leaudio

```c
bool bt_adapter_is_support_leaudio(bt_instance_t* ins);
```

查询是否支持 LE Audio。

**参数**：

- `ins` 蓝牙客户端实例。


**返回值**：

支持时返回 `true`，不支持时返回 `false`。


## 设备发现


#### bt_adapter_set_discovery_filter

```c
bt_status_t bt_adapter_set_discovery_filter(bt_instance_t* ins);
```

设置设备发现过滤条件。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.


#### bt_adapter_start_discovery

```c
bt_status_t bt_adapter_start_discovery(bt_instance_t* ins, uint32_t timeout);
```

开始设备发现。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `timeout` 超时时间。

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


#### bt_adapter_cancel_discovery

```c
bt_status_t bt_adapter_cancel_discovery(bt_instance_t* ins);
```

取消设备发现。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


#### bt_adapter_is_discovering

```c
bool bt_adapter_is_discovering(bt_instance_t* ins);
```

查询是否正在发现设备。

**参数**：

- `ins` 蓝牙客户端实例。


**返回值**：

正在发现时返回 `true`，否则返回 `false`。


## 属性管理


#### bt_adapter_get_type

```c
bt_device_type_t bt_adapter_get_type(bt_instance_t* ins);
```

获取设备类型。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.


#### bt_adapter_set_name

```c
bt_status_t bt_adapter_set_name(bt_instance_t* ins, const char* name);
```

设置设备名称。

**参数**：

- `ins` 蓝牙客户端实例。
- `name` 名称。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


#### bt_adapter_get_name

```c
void bt_adapter_get_name(bt_instance_t* ins, char* name, int length);
```

获取设备名称。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `name` 输出参数，存储适配器名称。
- `length` 缓冲区长度。


#### bt_adapter_set_scan_mode

```c
bt_status_t bt_adapter_set_scan_mode(bt_instance_t* ins, bt_scan_mode_t mode, bool bondable);
```

设置扫描模式。

**参数**：

- `ins` 蓝牙客户端实例。
- `mode` 扫描模式。
- `bondable` 是否可配对。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


#### bt_adapter_get_scan_mode

```c
bt_scan_mode_t bt_adapter_get_scan_mode(bt_instance_t* ins);
```

获取扫描模式。

**参数**：

- `ins` 蓝牙客户端实例。


**返回值**：

返回扫描模式枚举值，参见 `bt_scan_mode_t`。

```c
bt_status_t bt_adapter_set_device_class(bt_instance_t* ins, uint32_t cod);
```

设置设备类型（CoD）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cod` 设备类型（CoD）。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回负的错误码。。


#### bt_adapter_get_device_class

```c
uint32_t bt_adapter_get_device_class(bt_instance_t* ins);
```

获取设备类型（CoD）。

**参数**：

- `ins` 蓝牙客户端实例。


**返回值**：

返回 24 位 Class of Device 值。

```c
bt_status_t bt_adapter_set_debug_mode(bt_instance_t* ins, bt_debug_mode_t mode, uint8_t operation);
```

设置蓝牙适配器的调试模式，用于工厂测试和射频认证。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `mode` 调试模式。
- `operation` 调试操作。


#### bt_adapter_set_le_address

```c
bt_status_t bt_adapter_set_le_address(bt_instance_t* ins, bt_address_t* addr);
```

设置本地 BLE 地址。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` BLE 身份地址。


#### bt_adapter_set_le_appearance

```c
bt_status_t bt_adapter_set_le_appearance(bt_instance_t* ins, uint16_t appearance);
```

设置 BLE 外观值。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `appearance` BLE 外观值。


#### bt_adapter_le_add_whitelist_with_type

```c
bt_status_t bt_adapter_le_add_whitelist_with_type(bt_instance_t* ins, bt_address_t* addr, ble_addr_type_t type);
```

BLE 连接添加BLE 白名单（指定类型）特征值（签名写入）type。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 设备地址。
- `type` 地址类型。


## 配对与安全


#### bt_adapter_set_io_capability

```c
bt_status_t bt_adapter_set_io_capability(bt_instance_t* ins, bt_io_capability_t cap);
```

设置 IO 能力。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `cap` IO 能力值。


#### bt_adapter_get_bonded_devices

```c
bt_status_t bt_adapter_get_bonded_devices(bt_instance_t* ins, bt_transport_t transport, bt_address_t** addr, int* num, bt_allocator_t allocator);
```

获取已配对设备列表。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `transport` Transport type, 参见 bt_transport_t.
- `allocator` 内存分配函数。
- `addr` 输出参数，存储已配对设备地址数组。
- `num` 输出参数，存储设备数量。


#### bt_adapter_disconnect_all_devices

```c
void bt_adapter_disconnect_all_devices(bt_instance_t* ins);
```

断开所有已连接设备。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.


#### bt_adapter_get_le_io_capability

```c
uint32_t bt_adapter_get_le_io_capability(bt_instance_t* ins);
```

获取 BLE IO 能力。

**参数**：

- `ins` 蓝牙客户端实例。

**返回值**：

返回 BLE IO 能力值。


## BLE 管理


#### bt_adapter_enable

```c
bt_status_t bt_adapter_enable(bt_instance_t* ins);
```

启用蓝牙适配器。

**参数**：

- `ins` 蓝牙客户端实例。


**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


#### bt_adapter_disable

```c
bt_status_t bt_adapter_disable(bt_instance_t* ins);
```

禁用蓝牙适配器。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.

**返回值**：

成功时返回 BT_STATUS_SUCCESS，失败时返回错误码。


#### bt_adapter_disable_safe

```c
bt_status_t bt_adapter_disable_safe(bt_instance_t* ins);
```

安全禁用蓝牙适配器，等待所有连接断开后再关闭。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.


#### bt_adapter_disable_le

```c
bt_status_t bt_adapter_disable_le(bt_instance_t* ins);
```

禁用低功耗蓝牙（BLE）。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.


#### bt_adapter_is_le_enabled

```c
bool bt_adapter_is_le_enabled(bt_instance_t* ins);
```

查询 BLE 是否已启用。

**参数**：

- `ins` 蓝牙客户端实例。


**返回值**：

已启用时返回 `true`，未启用时返回 `false`。


#### bt_adapter_le_enable_key_derivation

```c
bt_status_t bt_adapter_le_enable_key_derivation(bt_instance_t* ins, bool brkey_to_lekey, bool lekey_to_brkey);
```

启用 BLE 密钥派生。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `brkey_to_lekey` 是否启用 BR→LE 密钥派生。
- `lekey_to_brkey` 是否启用 LE→BR 密钥派生。


#### bt_adapter_le_remove_whitelist

```c
bt_status_t bt_adapter_le_remove_whitelist(bt_instance_t* ins, bt_address_t* addr);
```

从 BLE 白名单移除设备。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `addr` 要移除的设备地址。


#### bt_adapter_set_page_scan_parameters

```c
bt_status_t bt_adapter_set_page_scan_parameters(bt_instance_t* ins, bt_scan_type_t type, uint16_t interval, uint16_t window);
```

设置页面扫描参数。

**参数**：

- `ins` 蓝牙客户端实例, 参见 bt_instance_t.
- `type` 扫描类型。
- `interval` 扫描间隔。
- `window` 扫描窗口。


## 异步接口


#### bt_adapter_register_callback_async

```c
bt_status_t bt_adapter_register_callback_async(bt_instance_t* ins, const adapter_callbacks_t* adapter_cbs, bt_register_callback_cb_t cb, void* userdata);
```

异步版本。

**参数**：

- `ins` 蓝牙客户端实例。
- `adapter_cbs` 适配器回调函数集合。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_unregister_callback_async

```c
bt_status_t bt_adapter_unregister_callback_async(bt_instance_t* ins, void* cookie, bt_bool_cb_t cb, void* userdata);
```

取消注册回调函数（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cookie` 用户上下文。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_enable_async

```c
bt_status_t bt_adapter_enable_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

适配器状态变更回调（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_disable_async

```c
bt_status_t bt_adapter_disable_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

禁用蓝牙适配器.（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_enable_le_async

```c
bt_status_t bt_adapter_enable_le_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

启用低功耗蓝牙（BLE）.（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_disable_le_async

```c
bt_status_t bt_adapter_disable_le_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

禁用低功耗蓝牙（BLE）.（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_state_async

```c
bt_status_t bt_adapter_get_state_async(bt_instance_t* ins, bt_adapter_get_state_cb_t get_state_cb, void* userdata);
```

获取当前适配器状态（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `get_state_cb` 获取状态的回调函数。
- `userdata` 用户数据。



#### bt_adapter_is_le_enabled_async

```c
bt_status_t bt_adapter_is_le_enabled_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

Check if BLE is enabled（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_type_async

```c
bt_status_t bt_adapter_get_type_async(bt_instance_t* ins, bt_device_type_cb_t get_dtype_cb, void* userdata);
```

获取适配器设备类型（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `get_dtype_cb` 获取设备类型的回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_discovery_filter_async

```c
bt_status_t bt_adapter_set_discovery_filter_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

设置发现过滤器（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_start_discovery_async

```c
bt_status_t bt_adapter_start_discovery_async(bt_instance_t* ins, uint32_t timeout, bt_status_cb_t cb, void* userdata);
```

开始设备发现.（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `timeout` 超时时间。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_cancel_discovery_async

```c
bt_status_t bt_adapter_cancel_discovery_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

取消设备发现.（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_is_discovering_async

```c
bt_status_t bt_adapter_is_discovering_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

查询适配器是否正在发现设备（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_address_async

```c
bt_status_t bt_adapter_get_address_async(bt_instance_t* ins, bt_address_cb_t cb, void* userdata);
```

读取蓝牙控制器地址（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_name_async

```c
bt_status_t bt_adapter_set_name_async(bt_instance_t* ins, const char* name, bt_status_cb_t cb, void* userdata);
```

设置适配器本地名称（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `name` 名称。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_name_async

```c
bt_status_t bt_adapter_get_name_async(bt_instance_t* ins, bt_string_cb_t get_name_cb, void* userdata);
```

获取适配器本地名称（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `get_name_cb` 获取名称的回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_uuids_async

```c
bt_status_t bt_adapter_get_uuids_async(bt_instance_t* ins, bt_uuids_cb_t get_uuids_cb, void* userdata);
```

获取适配器支持的 UUID 列表（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `get_uuids_cb` 获取 UUID 列表的回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_scan_mode_async

```c
bt_status_t bt_adapter_set_scan_mode_async(bt_instance_t* ins, bt_scan_mode_t mode, bool bondable, bt_status_cb_t cb, void* userdata);
```

设置适配器扫描模式（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `mode` 模式。
- `bondable` 是否可配对。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_scan_mode_async

```c
bt_status_t bt_adapter_get_scan_mode_async(bt_instance_t* ins, bt_adapter_get_scan_mode_cb_t get_scan_mode_cb, void* userdata);
```

获取适配器扫描模式（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `get_scan_mode_cb` 获取扫描模式的回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_device_class_async

```c
bt_status_t bt_adapter_set_device_class_async(bt_instance_t* ins, uint32_t cod, bt_status_cb_t cb, void* userdata);
```

设置适配器设备类型（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cod` 设备类型（CoD）。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_device_class_async

```c
bt_status_t bt_adapter_get_device_class_async(bt_instance_t* ins, bt_u32_cb_t get_cod_cb, void* userdata);
```

获取适配器设备类型（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `get_cod_cb` 获取设备类型的回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_io_capability_async

```c
bt_status_t bt_adapter_set_io_capability_async(bt_instance_t* ins, bt_io_capability_t cap, bt_status_cb_t cb, void* userdata);
```

设置 BR/EDR 适配器 IO 能力（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cap` IO 能力值。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_io_capability_async

```c
bt_status_t bt_adapter_get_io_capability_async(bt_instance_t* ins, bt_adapter_get_io_capability_cb_t get_ioc_cb, void* userdata);
```

获取 BR/EDR 适配器 IO 能力（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `get_ioc_cb` 获取 IO 能力的回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_inquiry_scan_parameters_async

```c
bt_status_t bt_adapter_set_inquiry_scan_parameters_async(bt_instance_t* ins, bt_scan_type_t type, uint16_t interval, uint16_t window, bt_status_cb_t cb, void* userdata);
```

设置查询扫描参数（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `type` 类型。
- `interval` 间隔。
- `window` 扫描窗口（时间槽数）。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_page_scan_parameters_async

```c
bt_status_t bt_adapter_set_page_scan_parameters_async(bt_instance_t* ins, bt_scan_type_t type, uint16_t interval, uint16_t window, bt_status_cb_t cb, void* userdata);
```

设置页面扫描参数（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `type` 类型。
- `interval` 间隔。
- `window` 扫描窗口（时间槽数）。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_le_io_capability_async

```c
bt_status_t bt_adapter_set_le_io_capability_async(bt_instance_t* ins, uint32_t le_io_cap, bt_status_cb_t cb, void* userdata);
```

设置 BLE 适配器 IO 能力（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `le_io_cap` BLE IO 能力值。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_le_io_capability_async

```c
bt_status_t bt_adapter_get_le_io_capability_async(bt_instance_t* ins, bt_u32_cb_t get_le_ioc_cb, void* userdata);
```

获取 BLE 适配器 IO 能力（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `get_le_ioc_cb` 获取 BLE IO 能力的回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_le_address_async

```c
bt_status_t bt_adapter_get_le_address_async(bt_instance_t* ins, bt_adapter_get_le_address_cb_t cb, void* userdata);
```

获取 BLE 适配器地址（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_le_address_async

```c
bt_status_t bt_adapter_set_le_address_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

设置 BLE 私有地址（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_le_identity_address_async

```c
bt_status_t bt_adapter_set_le_identity_address_async(bt_instance_t* ins, bt_address_t* addr, bool is_public, bt_status_cb_t cb, void* userdata);
```

设置 BLE 身份地址（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `is_public` 是否使用公共地址。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_le_appearance_async

```c
bt_status_t bt_adapter_set_le_appearance_async(bt_instance_t* ins, uint16_t appearance, bt_status_cb_t cb, void* userdata);
```

设置 BLE 适配器外观值（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `appearance` 外观值。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_le_appearance_async

```c
bt_status_t bt_adapter_get_le_appearance_async(bt_instance_t* ins, bt_u16_cb_t cb, void* userdata);
```

获取 BLE 适配器外观值（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_le_enable_key_derivation_async

```c
bt_status_t bt_adapter_le_enable_key_derivation_async(bt_instance_t* ins, bool brkey_to_lekey, bool lekey_to_brkey, bt_status_cb_t cb, void* userdata);
```

启用或禁用跨传输密钥派生（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `brkey_to_lekey` 是否启用 BR 密钥派生 LE 密钥。
- `lekey_to_brkey` 是否启用 LE 密钥派生 BR 密钥。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_le_add_whitelist_async

```c
bt_status_t bt_adapter_le_add_whitelist_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

添加设备到 BLE 白名单（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_le_remove_whitelist_async

```c
bt_status_t bt_adapter_le_remove_whitelist_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

从 BLE 白名单移除设备（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远程设备蓝牙地址。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_bonded_devices_async

```c
bt_status_t bt_adapter_get_bonded_devices_async(bt_instance_t* ins, bt_transport_t transport, bt_adapter_get_devices_cb_t get_bonded_cb, void* userdata);
```

获取已配对设备列表（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `get_bonded_cb` 获取已配对设备列表的回调函数。
- `userdata` 用户数据。



#### bt_adapter_get_connected_devices_async

```c
bt_status_t bt_adapter_get_connected_devices_async(bt_instance_t* ins, bt_transport_t transport, bt_adapter_get_devices_cb_t get_connected_cb, void* userdata);
```

获取已连接设备列表（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `transport` 传输类型（BR/EDR 或 BLE）。
- `get_connected_cb` 获取已连接设备列表的回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_afh_channel_classification_async

```c
bt_status_t bt_adapter_set_afh_channel_classification_async(bt_instance_t* ins, uint16_t central_frequency, uint16_t band_width, uint16_t number, bt_status_cb_t cb, void* userdata);
```

设置 AFH 自适应跳频信道分类（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `central_frequency` 中心频率（MHz）。
- `band_width` 带宽（MHz）。
- `number` 号码。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_set_auto_sniff_async

```c
bt_status_t bt_adapter_set_auto_sniff_async(bt_instance_t* ins, bt_auto_sniff_params_t* params, bt_status_cb_t cb, void* userdata);
```

设置自动 Sniff 模式参数（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `params` 参数结构体。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_disconnect_all_devices_async

```c
bt_status_t bt_adapter_disconnect_all_devices_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

断开所有已连接设备（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_is_support_bredr_async

```c
bt_status_t bt_adapter_is_support_bredr_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

Check if BR/EDR is supported（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_is_support_le_async

```c
bt_status_t bt_adapter_is_support_le_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

Check if BLE is supported（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。



#### bt_adapter_is_support_leaudio_async

```c
bt_status_t bt_adapter_is_support_leaudio_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

查询是否支持 LE Audio（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。

