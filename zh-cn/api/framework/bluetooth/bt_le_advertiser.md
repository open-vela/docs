\[ [English](../../../../en/api/framework/bluetooth/bt_le_advertiser.md) | 简体中文 \]

# 蓝牙 BLE 广播 API

openvela 蓝牙 BLE 广播接口，用于发送 BLE 广播数据和管理广播实例。

头文件：`#include "bt_le_advertiser.h"`


## openvela 实现说明

- **广播类型**：支持可连接广播、不可连接广播、扫描响应等
- **广播数据**：支持自定义广播数据和扫描响应数据
- **多实例**：支持同时运行多个广播实例


## 同步接口


### bt_le_stop_advertising

```c
void bt_le_stop_advertising(bt_instance_t* ins, bt_advertiser_t* adver);
```

停止 BLE 广播。

**参数**：

- `ins` 蓝牙客户端实例。
- `adver` 广播器实例。

**返回值**：



### bt_le_stop_advertising_id

```c
void bt_le_stop_advertising_id(bt_instance_t* ins, uint8_t adv_id);
```

停止指定 ID 的 BLE 广播实例。

**参数**：

- `ins` 蓝牙客户端实例。
- `adv_id` 广播实例 ID。


### bt_le_advertising_is_supported

```c
bool bt_le_advertising_is_supported(bt_instance_t* ins);
```

广播数据查询supported。

**参数**：

- `ins` 蓝牙客户端实例。


**返回值**：

bt_le_advertising_is_supported 操作。


## 异步接口


### bt_le_start_advertising_async

```c
bt_status_t bt_le_start_advertising_async(bt_instance_t* ins, ble_adv_params_t* params, uint8_t* adv_data, uint16_t adv_len, uint8_t* scan_rsp_data, uint16_t scan_rsp_len, advertiser_callback_t* adv_cbs, bt_le_start_adv_callback_cb_t cb, void* userdata);
```

开始 BLE 广播（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `params` 参数结构体。
- `adv_data` 广播数据。
- `adv_len` 广播数据长度。
- `scan_rsp_data` 扫描响应数据。
- `scan_rsp_len` 扫描响应数据长度。
- `adv_cbs` 广播回调函数集合。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_le_stop_advertising_async

```c
bt_status_t bt_le_stop_advertising_async(bt_instance_t* ins, bt_advertiser_t* adver, bt_status_cb_t cb, void* userdata);
```





**参数**：

- `ins` 蓝牙客户端实例。
- `adver` 广播器实例。
- `cb` 回调函数。
- `userdata` 用户数据。



### bt_le_stop_advertising_id_async

```c
bt_status_t bt_le_stop_advertising_id_async(bt_instance_t* ins, uint8_t adv_id, bt_status_cb_t cb, void* userdata);
```

停止BLE 广播（指定 ID）（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `adv_id` 广播实例 ID。
- `cb` 回调函数。
- `userdata` 用户数据。


### bt_le_advertising_is_supported_async

```c
bt_status_t bt_le_advertising_is_supported_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

查询是否支持 BLE 广播（异步版本）。

**参数**：

- `ins` 蓝牙客户端实例。
- `cb` 回调函数。
- `userdata` 用户数据。

