\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/bt_spp.md) \]

# Bluetooth SPP API

The openvela Bluetooth SPP (Serial Port Profile) interface provides virtual serial port communication as a replacement for physical serial ports.

Header file: #include "bt_spp.h"


## openvela Implementation Notes

- **Features**: Virtual serial port communication, suitable for Bluetooth-enabling traditional serial devices


## Synchronous Interfaces


### bt_spp_unregister_app

```c
bt_status_t bt_spp_unregister_app(bt_instance_t* ins, void* handle);
```

Unregister an SPP application.

**Parameters**:

- `handle` Application handle.
- `ins` Bluetooth client instance.

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_spp_server_start

```c
bt_status_t bt_spp_server_start(bt_instance_t* ins, void* handle, uint16_t scn, bt_uuid_t* uuid, uint8_t max_connection);
```

Start an SPP server to listen for connection requests from remote devices.

**Parameters**:

- `ins` Bluetooth client instance.
- `handle` Application handle.
- `scn` Server channel number.
- `uuid` Service UUID.
- `max_connection` Maximum number of connections.

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_spp_server_stop

```c
bt_status_t bt_spp_server_stop(bt_instance_t* ins, void* handle, uint16_t scn);
```

Stop the SPP server and stop accepting new connections.

**Parameters**:

- `ins` Bluetooth client instance.
- `handle` Application handle.
- `scn` Server channel number.

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_spp_connect

```c
bt_status_t bt_spp_connect(bt_instance_t* ins, void* handle, bt_address_t* addr, int16_t scn, bt_uuid_t* uuid, uint16_t* port);
```

Initiate a connection to the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `handle` Application handle.
- `addr` Bluetooth address of the remote device.
- `scn` Server channel number.
- `uuid` Service UUID.
- `port` Port number.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_spp_insecure_connect

```c
bt_status_t bt_spp_insecure_connect(bt_instance_t* ins, void* handle, bt_address_t* addr, int16_t scn, bt_uuid_t* uuid, uint16_t* port);
```

Initiate an insecure connection to the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `handle` Application handle.
- `addr` Bluetooth address of the remote device.
- `scn` Server channel number.
- `uuid` Service UUID.
- `port` Port number.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_spp_disconnect

```c
bt_status_t bt_spp_disconnect(bt_instance_t* ins, void* handle, bt_address_t* addr, uint16_t port);
```

Disconnect the SPP connection.

**Parameters**:

- `ins` Bluetooth client instance.
- `handle` Application handle.
- `addr` Bluetooth address of the peer device.
- `port` Port number.

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.
