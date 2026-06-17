\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/bt_avrcp.md) \]

# Bluetooth AVRCP API

The openvela Bluetooth AVRCP (Audio/Video Remote Control Profile) interface supports playback control, track information queries, and more.

Header files: #include "bt_avrcp.h", #include "bt_avrcp_control.h", #include "bt_avrcp_target.h"


## openvela Implementation Notes

- **Dual-role support**: Controller (control side) and Target (target side)
- **Features**: Play/pause/skip tracks, volume control, track information retrieval


## Synchronous Interfaces


### bt_avrcp_control_unregister_callbacks

```c
bool bt_avrcp_control_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

Unregister callback functions and stop receiving state change notifications.

**Parameters**:

- `ins` Bluetooth client instance.
- `cookie` User context.

**Returns**:

Returns the callback cookie on success, or NULL on failure.


### bt_avrcp_control_get_element_attributes

```c
bt_status_t bt_avrcp_control_get_element_attributes(bt_instance_t* ins, bt_address_t* addr);
```

Get media element attributes from the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_avrcp_control_send_passthrough_cmd

```c
bt_status_t bt_avrcp_control_send_passthrough_cmd(bt_instance_t* ins, bt_address_t* addr, uint8_t cmd, uint8_t state);
```

Send a passthrough command to the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cmd` Command code.
- `state` Key state.


### bt_avrcp_control_get_unit_info

```c
bt_status_t bt_avrcp_control_get_unit_info(bt_instance_t* ins, bt_address_t* addr);
```

Get unit information from the remote AVRCP device.


**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


### bt_avrcp_control_get_subunit_info

```c
bt_status_t bt_avrcp_control_get_subunit_info(bt_instance_t* ins, bt_address_t* addr);
```

Get subunit information from the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


### bt_avrcp_control_get_playback_state

```c
bt_status_t bt_avrcp_control_get_playback_state(bt_instance_t* ins, bt_address_t* addr);
```

Get the current playback state of the remote device.


**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


### bt_avrcp_control_register_notification

```c
bt_status_t bt_avrcp_control_register_notification(bt_instance_t* ins, bt_address_t* addr, uint8_t event, uint32_t interval);
```

Register for event notifications from the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `event` Event type.
- `interval` Notification interval.


### bt_avrcp_target_unregister_callbacks

```c
bool bt_avrcp_target_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

Unregister callback functions and stop receiving state change notifications.

**Parameters**:

- `ins` Bluetooth client instance.
- `cookie` User context.

**Returns**:

Returns the callback cookie on success, or NULL on failure.


### bt_avrcp_target_get_play_status_response

```c
bt_status_t bt_avrcp_target_get_play_status_response(bt_instance_t* ins, bt_address_t* addr, avrcp_play_status_t status, uint32_t song_len, uint32_t song_pos);
```

Respond to a play status query from the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the peer device.
- `status` Play status code.
- `song_len` Song length in milliseconds.
- `song_pos` Current playback position in milliseconds.

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_avrcp_target_play_status_notify

```c
bt_status_t bt_avrcp_target_play_status_notify(bt_instance_t* ins, bt_address_t* addr, avrcp_play_status_t status);
```

Notify the remote device of a playback status change.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `status` Play status code.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.
