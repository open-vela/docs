\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/bt_le_scan.md) \]

# Bluetooth BLE Scanning API

The openvela Bluetooth BLE scanning interface is used to discover nearby BLE devices and receive broadcast data.

Header file: `#include "bt_le_scan.h"`


## openvela Implementation Notes

- **Scan modes**: Supports passive scanning and active scanning
- **Filters**: Supports filtering scan results by name, address, UUID, and other criteria
- **Callback notifications**: Scan results are returned asynchronously via callback functions


## Synchronous Interfaces


### bt_le_stop_scan

```c
void bt_le_stop_scan(bt_instance_t* ins, bt_scanner_t* scanner);
```

Stop BLE scanning.

**Parameters**:

- `scanner` Scanner instance.
- `ins` Bluetooth client instance.

**Returns**:

None.


### bt_le_scan_is_supported

```c
bool bt_le_scan_is_supported(bt_instance_t* ins);
```

Query whether BLE scanning is supported.

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

Returns true if BLE scanning is supported, false otherwise.


## Asynchronous Interfaces


### bt_le_start_scan_async

```c
bt_status_t bt_le_start_scan_async(bt_instance_t* ins, const scanner_callbacks_t* scan_cbs, bt_le_start_scan_cb_t cb, void* userdata);
```

Start BLE scanning (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `scan_cbs` Scanner callback function set.
- `cb` Completion callback function.
- `userdata` User data.


### bt_le_start_scan_settings_async

```c
bt_status_t bt_le_start_scan_settings_async(bt_instance_t* ins, ble_scan_settings_t* settings, const scanner_callbacks_t* scan_cbs, bt_le_start_scan_cb_t cb, void* userdata);
```

Start BLE scanning with custom settings (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `settings` Scan settings.
- `scan_cbs` Scanner callback function set.
- `cb` Completion callback function.
- `userdata` User data.



### bt_le_start_scan_with_filters_async

```c
bt_status_t bt_le_start_scan_with_filters_async(bt_instance_t* ins, ble_scan_settings_t* settings, ble_scan_filter_t* filter, const scanner_callbacks_t* scan_cbs, bt_le_start_scan_cb_t cb, void* userdata);
```

Start BLE scanning with filters (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `settings` Scan settings.
- `filter` Filter criteria.
- `scan_cbs` Scanner callback function set.
- `cb` Completion callback function.
- `userdata` User data.


### bt_le_stop_scan_async

```c
bt_status_t bt_le_stop_scan_async(bt_instance_t* ins, bt_scanner_t* scanner, bt_le_stop_scan_cb_t cb, void* userdata);
```

Stop BLE scanning (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `scanner` Scanner instance.
- `cb` Completion callback function.
- `userdata` User data.




### bt_le_scan_is_supported_async

```c
bt_status_t bt_le_scan_is_supported_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

Query whether BLE scanning is supported (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Completion callback function.
- `userdata` User data.
