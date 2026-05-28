\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/bt_pan.md) \]

# Bluetooth PAN API

The openvela Bluetooth PAN (Personal Area Network) interface supports network sharing over Bluetooth.

Header file: #include "bt_pan.h"


## openvela Implementation Notes

- **Features**: Network tethering, Bluetooth networking


## Synchronous Interfaces


### bt_pan_unregister_callbacks

```c
bool bt_pan_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

Unregister callback functions and stop receiving state change notifications.

**Parameters**:

- `cookie` User context.
- `ins` Bluetooth client instance.

**Returns**:

Returns `true` on success, `false` on failure.


### bt_pan_connect

```c
bt_status_t bt_pan_connect(bt_instance_t* ins, bt_address_t* addr, uint8_t dst_role, uint8_t src_role);
```

Initiate a PAN connection to the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `dst_role` Destination device role.
- `src_role` Local device role.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_pan_disconnect

```c
bt_status_t bt_pan_disconnect(bt_instance_t* ins, bt_address_t* addr);
```

Disconnect the PAN connection from the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.
