\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/bt_le_advertiser.md) \]

# Bluetooth BLE Advertising API

The openvela Bluetooth BLE advertising interface is used to send BLE advertising data and manage advertising instances.

Header file: `#include "bt_le_advertiser.h"`


## openvela Implementation Notes

- **Advertising types**: Supports connectable advertising, non-connectable advertising, scan response, etc.
- **Advertising data**: Supports custom advertising data and scan response data
- **Multiple instances**: Supports running multiple advertising instances simultaneously


## Synchronous Interfaces


### bt_le_stop_advertising

```c
void bt_le_stop_advertising(bt_instance_t* ins, bt_advertiser_t* adver);
```

Stop BLE advertising.

**Parameters**:

- `ins` Bluetooth client instance.
- `adver` Advertiser instance.

**Returns**:

None.


### bt_le_stop_advertising_id

```c
void bt_le_stop_advertising_id(bt_instance_t* ins, uint8_t adv_id);
```

Stop the BLE advertising instance with the specified ID.

**Parameters**:

- `ins` Bluetooth client instance.
- `adv_id` Advertising instance ID.


### bt_le_advertising_is_supported

```c
bool bt_le_advertising_is_supported(bt_instance_t* ins);
```

Query whether BLE advertising is supported.

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

Returns true if BLE advertising is supported, false otherwise.


## Asynchronous Interfaces


### bt_le_start_advertising_async

```c
bt_status_t bt_le_start_advertising_async(bt_instance_t* ins, ble_adv_params_t* params, uint8_t* adv_data, uint16_t adv_len, uint8_t* scan_rsp_data, uint16_t scan_rsp_len, advertiser_callback_t* adv_cbs, bt_le_start_adv_callback_cb_t cb, void* userdata);
```

Start BLE advertising (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `params` Advertising parameters structure.
- `adv_data` Advertising data.
- `adv_len` Advertising data length.
- `scan_rsp_data` Scan response data.
- `scan_rsp_len` Scan response data length.
- `adv_cbs` Advertiser callback function set.
- `cb` Completion callback function.
- `userdata` User data.


### bt_le_stop_advertising_async

```c
bt_status_t bt_le_stop_advertising_async(bt_instance_t* ins, bt_advertiser_t* adver, bt_status_cb_t cb, void* userdata);
```

Stop BLE advertising (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `adver` Advertiser instance.
- `cb` Completion callback function.
- `userdata` User data.



### bt_le_stop_advertising_id_async

```c
bt_status_t bt_le_stop_advertising_id_async(bt_instance_t* ins, uint8_t adv_id, bt_status_cb_t cb, void* userdata);
```

Stop BLE advertising by specified ID (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `adv_id` Advertising instance ID.
- `cb` Completion callback function.
- `userdata` User data.


### bt_le_advertising_is_supported_async

```c
bt_status_t bt_le_advertising_is_supported_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

Query whether BLE advertising is supported (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Completion callback function.
- `userdata` User data.
