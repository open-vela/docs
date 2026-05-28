\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/bt_hid.md) \]

# Bluetooth HID API

The openvela Bluetooth HID (Human Interface Device) interface supports input devices such as keyboards, mice, and game controllers.

Header file: #include "bt_hid_device.h"


## openvela Implementation Notes

- **Device role**: HID Device (input device side)


## Synchronous Interfaces


### bt_hid_device_unregister_callbacks

```c
bool bt_hid_device_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

Unregister callback functions and stop receiving state change notifications.

**Parameters**:

- `cookie` User context.
- `ins` Bluetooth client instance.

**Returns**:

Returns `true` on success, `false` on failure.


### bt_hid_device_register_app

```c
bt_status_t bt_hid_device_register_app(bt_instance_t* ins, hid_device_sdp_settings_t* sdp_setting, bool le_hid);
```

Register an HID device application.

**Parameters**:

- `ins` Bluetooth client instance.
- `sdp_setting` SDP settings.
- `le_hid` Whether this is a LE HID instance.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_hid_device_unregister_app

```c
bt_status_t bt_hid_device_unregister_app(bt_instance_t* ins);
```

Unregister the HID device application.

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_hid_device_connect

```c
bt_status_t bt_hid_device_connect(bt_instance_t* ins, bt_address_t* addr);
```

Initiate a connection to the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_hid_device_disconnect

```c
bt_status_t bt_hid_device_disconnect(bt_instance_t* ins, bt_address_t* addr);
```

Disconnect from the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_hid_device_send_report

```c
bt_status_t bt_hid_device_send_report(bt_instance_t* ins, bt_address_t* addr, uint8_t rpt_id, uint8_t* rpt_data, int rpt_size);
```

Send an HID input report to the connected host.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `rpt_id` HID report ID.
- `rpt_data` HID report data.
- `rpt_size` Report data size in bytes.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_hid_device_response_report

```c
bt_status_t bt_hid_device_response_report(bt_instance_t* ins, bt_address_t* addr, uint8_t rpt_type, uint8_t* rpt_data, int rpt_size);
```

Respond to a host HID report request.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `rpt_type` HID report type (input/output/feature).
- `rpt_data` HID report data.
- `rpt_size` Report data size in bytes.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_hid_device_report_error

```c
bt_status_t bt_hid_device_report_error(bt_instance_t* ins, bt_address_t* addr, hid_status_error_t error);
```

Report an HID error to the host.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `error` Error code.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_hid_device_virtual_unplug

```c
bt_status_t bt_hid_device_virtual_unplug(bt_instance_t* ins, bt_address_t* addr);
```

Send a virtual unplug request to disconnect the HID connection.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.
