\[ [English](../../../../en/api/framework/bluetooth/bt_le_scan.md) | 简体中文 \]

# 蓝牙 BLE 扫描 API

openvela 蓝牙 BLE 扫描接口，用于发现周围的 BLE 设备和广播数据。

头文件：`#include "bt_le_scan.h"`


## openvela 实现说明

- **扫描模式**：支持被动扫描和主动扫描
- **过滤器**：支持按名称、地址、UUID 等条件过滤扫描结果
- **回调通知**：通过回调函数异步返回扫描结果


## 同步接口


### bt_le_stop_scan

```c
void bt_le_stop_scan(bt_instance_t* ins, bt_scanner_t* scanner);
```

停止 BLE 扫描。

**参数**：

- `scanner` 扫描器实例。
- `ins` 蓝牙客户端实例, 参见 bt_instance_t.

**返回值**：



### bt_le_scan_is_supported

```c
bool bt_le_scan_is_supported(bt_instance_t* ins);
```

查询操作。

**参数**：

- `ins` 蓝牙客户端实例。


**返回值**：

bt_le_scan_is_supported 操作。


## 异步接口


### bt_le_start_scan_async

```c
bt_status_t bt_le_start_scan_async(bt_instance_t* ins, const scanner_callbacks_t* scan_cbs, bt_le_start_scan_cb_t cb, void* userdata);
```

开始BLE 扫描（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `scan_cbs` 扫描回调函数集合。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_le_start_scan_settings_async

```c
bt_status_t bt_le_start_scan_settings_async(bt_instance_t* ins, ble_scan_settings_t* settings, const scanner_callbacks_t* scan_cbs, bt_le_start_scan_cb_t cb, void* userdata);
```

异步版本。

**参数**：

- `ins` 蓝牙客户端实例。
- `settings` 设置。
- `scan_cbs` 扫描回调函数集合。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_le_start_scan_with_filters_async

```c
bt_status_t bt_le_start_scan_with_filters_async(bt_instance_t* ins, ble_scan_settings_t* settings, ble_scan_filter_t* filter, const scanner_callbacks_t* scan_cbs, bt_le_start_scan_cb_t cb, void* userdata);
```

开始操作（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `settings` 设置。
- `filter` 过滤条件。
- `scan_cbs` 扫描回调函数集合。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_le_stop_scan_async

```c
bt_status_t bt_le_stop_scan_async(bt_instance_t* ins, bt_scanner_t* scanner, bt_le_stop_scan_cb_t cb, void* userdata);
```

停止扫描（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `scanner` 扫描器实例。
- `cb` 回调函数。
- `userdata` 用户数据。




### bt_le_scan_is_supported_async

```c
bt_status_t bt_le_scan_is_supported_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

查询是否支持 BLE 扫描（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。

