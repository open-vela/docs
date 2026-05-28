\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/bt_gatt.md) \]

# Bluetooth GATT API

openvela Bluetooth GATT (Generic Attribute Profile) interface, supporting BLE data attribute read/write and notifications.

Header files: #include "bt_gattc.h", #include "bt_gatts.h"


## openvela Implementation Notes

- **Dual-role support**: Client (GATTC, initiates read/write requests) and Server (GATTS, provides services and characteristic values)
- **BLE core**: GATT is the fundamental protocol for BLE data exchange


## Synchronous Interfaces


### bt_gattc_create_connect

```c
bt_status_t bt_gattc_create_connect(bt_instance_t* ins, gattc_handle_t* phandle, gattc_callbacks_t* callbacks);
```

Create a GATT client connection instance.

**Parameters**:

- `ins` Bluetooth client instance.
- `phandle` Output parameter, stores the GATT client handle.
- `callbacks` Callback function set.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_delete_connect

```c
bt_status_t bt_gattc_delete_connect(gattc_handle_t conn_handle);
```

Delete a GATT client connection instance.

**Parameters**:

- `conn_handle` Connection handle.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_connect

```c
bt_status_t bt_gattc_connect(gattc_handle_t conn_handle, bt_address_t* addr, ble_addr_type_t addr_type);
```

Initiate a connection to a remote device.

**Parameters**:

- `conn_handle` Connection handle.
- `addr` Bluetooth address of the remote device.
- `addr_type` BLE address type.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_disconnect

```c
bt_status_t bt_gattc_disconnect(gattc_handle_t conn_handle);
```

Disconnect from a remote device.

**Parameters**:

- `conn_handle` Connection handle.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_discover_service

```c
bt_status_t bt_gattc_discover_service(gattc_handle_t conn_handle, bt_uuid_t* filter_uuid);
```

Discover GATT services on a remote device. Results are returned asynchronously via callback.

**Parameters**:

- `conn_handle` Connection handle.
- `filter_uuid` Service UUID filter (NULL means no filter).

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_get_attribute_by_handle

```c
bt_status_t bt_gattc_get_attribute_by_handle(gattc_handle_t conn_handle, uint16_t attr_handle, gatt_attr_desc_t* attr_desc);
```

Get GATT attribute information by attribute handle.

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `attr_desc` Output parameter, stores the attribute description.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_get_attribute_by_uuid

```c
bt_status_t bt_gattc_get_attribute_by_uuid(gattc_handle_t conn_handle, uint16_t start_handle, uint16_t end_handle, bt_uuid_t* attr_uuid, gatt_attr_desc_t* attr_desc);
```

Get GATT attribute information by UUID.

**Parameters**:

- `conn_handle` Connection handle.
- `start_handle` Start handle.
- `end_handle` End handle.
- `attr_uuid` Attribute UUID.
- `attr_desc` Output parameter, stores the attribute description.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_read

```c
bt_status_t bt_gattc_read(gattc_handle_t conn_handle, uint16_t attr_handle);
```

Read a GATT characteristic value or descriptor from a remote device. Results are returned asynchronously via callback.

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_write

```c
bt_status_t bt_gattc_write(gattc_handle_t conn_handle, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

Write a GATT characteristic value or descriptor to a remote device, waiting for confirmation before returning the result via callback.

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `value` Data to write.
- `length` Data length.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_write_without_response

```c
bt_status_t bt_gattc_write_without_response(gattc_handle_t conn_handle, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

Write a GATT characteristic value to a remote device (Write Without Response), without waiting for confirmation.

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `value` Data to write.
- `length` Data length.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_write_with_signed

```c
bt_status_t bt_gattc_write_with_signed(gattc_handle_t conn_handle, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

Write a GATT characteristic value to a remote device (Signed Write), using signed authentication.

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `value` Data to write.
- `length` Data length.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_subscribe

```c
bt_status_t bt_gattc_subscribe(gattc_handle_t conn_handle, uint16_t attr_handle, uint16_t ccc_value);
```

Subscribe to GATT characteristic value notifications or indications from a remote device.

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `ccc_value` CCCD value (0 disable, 1 notification, 2 indication).

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_unsubscribe

```c
bt_status_t bt_gattc_unsubscribe(gattc_handle_t conn_handle, uint16_t attr_handle);
```

Unsubscribe from GATT characteristic value notifications or indications from a remote device.

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_exchange_mtu

```c
bt_status_t bt_gattc_exchange_mtu(gattc_handle_t conn_handle, uint32_t mtu);
```

Negotiate the ATT MTU size with a remote device, affecting the maximum data length per transfer.

**Parameters**:

- `conn_handle` Connection handle.
- `mtu` MTU value.

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_update_connection_parameter

```c
bt_status_t bt_gattc_update_connection_parameter(gattc_handle_t conn_handle, uint32_t min_interval, uint32_t max_interval, uint32_t latency, uint32_t timeout, uint32_t min_connection_event_length, uint32_t max_connection_event_length);
```

Update BLE connection parameters.

**Parameters**:

- `conn_handle` Connection handle.
- `min_interval` Minimum connection interval.
- `max_interval` Maximum connection interval.
- `latency` Peripheral latency.
- `timeout` Supervision timeout.
- `min_connection_event_length` Minimum connection event length.
- `max_connection_event_length` Maximum connection event length.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_read_phy

```c
bt_status_t bt_gattc_read_phy(gattc_handle_t conn_handle);
```

Read the current PHY configuration. Results are returned asynchronously via callback.

**Parameters**:

- `conn_handle` Connection handle.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_update_phy

```c
bt_status_t bt_gattc_update_phy(gattc_handle_t conn_handle, ble_phy_type_t tx_phy, ble_phy_type_t rx_phy);
```

Update the PHY configuration.

**Parameters**:

- `conn_handle` Connection handle.
- `tx_phy` Transmit PHY.
- `rx_phy` Receive PHY.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gattc_read_rssi

```c
bt_status_t bt_gattc_read_rssi(gattc_handle_t conn_handle);
```

Read the RSSI value of the connection. Results are returned asynchronously via callback.

**Parameters**:

- `conn_handle` Connection handle.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_register_service

```c
bt_status_t bt_gatts_register_service(bt_instance_t* ins, gatts_handle_t* phandle, gatts_callbacks_t* callbacks);
```

Register a GATT service.

**Parameters**:

- `ins` Bluetooth client instance.
- `phandle` Output parameter, stores the GATT server handle.
- `callbacks` Callback function set.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_unregister_service

```c
bt_status_t bt_gatts_unregister_service(gatts_handle_t srv_handle);
```

Unregister a GATT service.

**Parameters**:

- `srv_handle` GATT service handle.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_connect

```c
bt_status_t bt_gatts_connect(gatts_handle_t srv_handle, bt_address_t* addr, ble_addr_type_t addr_type);
```

Initiate a connection to a remote device.

**Parameters**:

- `srv_handle` GATT service handle.
- `addr` Bluetooth address of the remote device.
- `addr_type` BLE address type.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_connect_bear

```c
bt_status_t bt_gatts_connect_bear(gatts_handle_t srv_handle, bt_address_t* addr, ble_addr_type_t addr_type, uint8_t bear_type);
```

Initiate a connection to a remote device with a specified bearer type.

**Parameters**:

- `srv_handle` GATT service handle.
- `addr` Bluetooth address of the remote device.
- `addr_type` BLE address type.
- `bear_type` Bearer type.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_disconnect

```c
bt_status_t bt_gatts_disconnect(gatts_handle_t srv_handle, bt_address_t* addr);
```

Disconnect from a remote device.

**Parameters**:

- `srv_handle` GATT service handle.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_add_attr_table

```c
bt_status_t bt_gatts_add_attr_table(gatts_handle_t srv_handle, gatt_srv_db_t* srv_db);
```

Add an attribute table (services, characteristics, descriptors) to the local GATT server.

**Parameters**:

- `srv_handle` GATT service handle.
- `srv_db` GATT service attribute table.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_remove_attr_table

```c
bt_status_t bt_gatts_remove_attr_table(gatts_handle_t srv_handle, uint16_t attr_handle);
```

Remove an attribute table from the local GATT server.

**Parameters**:

- `srv_handle` GATT service handle.
- `attr_handle` Attribute handle.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_set_attr_value

```c
bt_status_t bt_gatts_set_attr_value(gatts_handle_t srv_handle, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

Set the value of a local GATT attribute.

**Parameters**:

- `srv_handle` GATT service handle.
- `attr_handle` Attribute handle.
- `value` Data to set.
- `length` Data length.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_get_attr_value

```c
bt_status_t bt_gatts_get_attr_value(gatts_handle_t srv_handle, uint16_t attr_handle, uint8_t* value, uint16_t* length);
```

Get the value of a local GATT attribute.

**Parameters**:

- `srv_handle` GATT service handle.
- `attr_handle` Attribute handle.
- `value` Output buffer for the attribute value.
- `length` Output parameter, stores the data length.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_response

```c
bt_status_t bt_gatts_response(gatts_handle_t srv_handle, bt_address_t* addr, uint32_t req_handle, uint8_t* value, uint16_t length);
```

Respond to a GATT read/write request from a remote device.

**Parameters**:

- `srv_handle` GATT service handle.
- `addr` Bluetooth address of the remote device.
- `req_handle` Request handle.
- `value` Response data.
- `length` Data length.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_notify

```c
bt_status_t bt_gatts_notify(gatts_handle_t srv_handle, bt_address_t* addr, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

Send a GATT notification to a subscribed remote device, without requiring confirmation.

**Parameters**:

- `srv_handle` GATT service handle.
- `addr` Bluetooth address of the remote device.
- `attr_handle` Attribute handle.
- `value` Notification data.
- `length` Data length.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_indicate

```c
bt_status_t bt_gatts_indicate(gatts_handle_t srv_handle, bt_address_t* addr, uint16_t attr_handle, uint8_t* value, uint16_t length);
```

Send a GATT indication to a subscribed remote device, requiring confirmation.

**Parameters**:

- `srv_handle` GATT service handle.
- `addr` Bluetooth address of the remote device.
- `attr_handle` Attribute handle.
- `value` Indication data.
- `length` Data length.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_read_phy

```c
bt_status_t bt_gatts_read_phy(gatts_handle_t srv_handle, bt_address_t* addr);
```

Read the current PHY configuration.

**Parameters**:

- `srv_handle` GATT service handle.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_gatts_update_phy

```c
bt_status_t bt_gatts_update_phy(gatts_handle_t srv_handle, bt_address_t* addr, ble_phy_type_t tx_phy, ble_phy_type_t rx_phy);
```

Update the PHY configuration.

**Parameters**:

- `srv_handle` GATT service handle.
- `addr` Bluetooth address of the remote device.
- `tx_phy` Transmit PHY.
- `rx_phy` Receive PHY.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


## Asynchronous Interfaces


### bt_gattc_create_connect_async

```c
bt_status_t bt_gattc_create_connect_async(bt_instance_t* ins, gattc_handle_t* phandle, gattc_callbacks_t* callbacks, bt_gattc_create_connect_cb_t cb, void* userdata);
```

Create a GATT client connection instance (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `phandle` Output parameter, stores the GATT client handle.
- `callbacks` Callback function set.
- `cb` Completion callback function.
- `userdata` User data.


### bt_gattc_delete_connect_async

```c
bt_status_t bt_gattc_delete_connect_async(gattc_handle_t conn_handle, bt_status_cb_t bt_gattc_delete_connect_cb_t, void* userdata);
```

Delete a GATT client connection instance (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `bt_gattc_delete_connect_cb_t` Completion callback for connection deletion.
- `userdata` User data.



### bt_gattc_connect_async

```c
bt_status_t bt_gattc_connect_async(gattc_handle_t conn_handle, bt_address_t* addr, ble_addr_type_t addr_type, bt_status_cb_t cb, void* userdata);
```

Initiate a connection to a remote device (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `addr` Bluetooth address of the remote device.
- `addr_type` BLE address type.
- `cb` Completion callback function.
- `userdata` User data.


### bt_gattc_disconnect_async

```c
bt_status_t bt_gattc_disconnect_async(gattc_handle_t conn_handle, bt_status_cb_t cb, void* userdata);
```

Disconnect the ATT bearer connection (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `cb` Completion callback function.
- `userdata` User data.



### bt_gattc_discover_service_async

```c
bt_status_t bt_gattc_discover_service_async(gattc_handle_t conn_handle, bt_uuid_t* filter_uuid, bt_status_cb_t cb, void* userdata);
```

Discover GATT services (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `filter_uuid` Service UUID filter (NULL means no filter).
- `cb` Completion callback function.
- `userdata` User data.


### bt_gattc_get_attribute_by_handle_async

```c
bt_status_t bt_gattc_get_attribute_by_handle_async(gattc_handle_t conn_handle, uint16_t attr_handle, bt_gattc_get_attribute_cb_t cb, void* userdata);
```

Get attribute by handle (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `cb` Completion callback function.
- `userdata` User data.



### bt_gattc_get_attribute_by_uuid_async

```c
bt_status_t bt_gattc_get_attribute_by_uuid_async(gattc_handle_t conn_handle, uint16_t start_handle, uint16_t end_handle, bt_uuid_t* attr_uuid, bt_gattc_get_attribute_cb_t cb, void* userdata);
```

Get attribute by UUID (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `start_handle` Start handle.
- `end_handle` End handle.
- `attr_uuid` Attribute UUID.
- `cb` Completion callback function.
- `userdata` User data.


### bt_gattc_read_async

```c
bt_status_t bt_gattc_read_async(gattc_handle_t conn_handle, uint16_t attr_handle, bt_status_cb_t cb, void* userdata);
```

Read attribute value by handle (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `cb` Completion callback function.
- `userdata` User data.



### bt_gattc_write_async

```c
bt_status_t bt_gattc_write_async(gattc_handle_t conn_handle, uint16_t attr_handle, uint8_t* value, uint16_t length, bt_status_cb_t cb, void* userdata);
```

Write attribute value (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `value` Data to write.
- `length` Data length.
- `cb` Completion callback function.
- `userdata` User data.


### bt_gattc_write_without_response_async

```c
bt_status_t bt_gattc_write_without_response_async(gattc_handle_t conn_handle, uint16_t attr_handle, uint8_t* value, uint16_t length, bt_gattc_write_cb_t cb, void* userdata);
```

Write data to a specified attribute without response (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `value` Data to write.
- `length` Data length.
- `cb` Completion callback function.
- `userdata` User data.



### bt_gattc_subscribe_async

```c
bt_status_t bt_gattc_subscribe_async(gattc_handle_t conn_handle, uint16_t attr_handle, uint16_t ccc_value, bt_status_cb_t cb, void* userdata);
```

Subscribe to notifications or indications (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `ccc_value` CCCD value (0 disable, 1 notification, 2 indication).
- `cb` Completion callback function.
- `userdata` User data.


### bt_gattc_unsubscribe_async

```c
bt_status_t bt_gattc_unsubscribe_async(gattc_handle_t conn_handle, uint16_t attr_handle, bt_status_cb_t cb, void* userdata);
```

Disable the specified CCCD (Client Characteristic Configuration Descriptor) (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `attr_handle` Attribute handle.
- `cb` Completion callback function.
- `userdata` User data.



### bt_gattc_exchange_mtu_async

```c
bt_status_t bt_gattc_exchange_mtu_async(gattc_handle_t conn_handle, uint32_t mtu, bt_status_cb_t cb, void* userdata);
```

Exchange MTU size (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `mtu` MTU value.
- `cb` Completion callback function.
- `userdata` User data.


### bt_gattc_update_connection_parameter_async

```c
bt_status_t bt_gattc_update_connection_parameter_async(gattc_handle_t conn_handle, uint32_t min_interval, uint32_t max_interval, uint32_t latency, uint32_t timeout, uint32_t min_connection_event_length, uint32_t max_connection_event_length, bt_status_cb_t cb, void* userdata);
```

Update BLE connection parameters (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `min_interval` Minimum connection interval.
- `max_interval` Maximum connection interval.
- `latency` Peripheral latency.
- `timeout` Supervision timeout.
- `min_connection_event_length` Minimum connection event length.
- `max_connection_event_length` Maximum connection event length.
- `cb` Completion callback function.
- `userdata` User data.



### bt_gattc_read_phy_async

```c
bt_status_t bt_gattc_read_phy_async(gattc_handle_t conn_handle, bt_status_cb_t cb, void* userdata);
```

Read PHY configuration (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `cb` Completion callback function.
- `userdata` User data.


### bt_gattc_update_phy_async

```c
bt_status_t bt_gattc_update_phy_async(gattc_handle_t conn_handle, ble_phy_type_t tx_phy, ble_phy_type_t rx_phy, bt_status_cb_t cb, void* userdata);
```

Update PHY configuration (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `tx_phy` Transmit PHY.
- `rx_phy` Receive PHY.
- `cb` Completion callback function.
- `userdata` User data.



### bt_gattc_read_rssi_async

```c
bt_status_t bt_gattc_read_rssi_async(gattc_handle_t conn_handle, bt_status_cb_t cb, void* userdata);
```

Read RSSI value (asynchronous version).

**Parameters**:

- `conn_handle` Connection handle.
- `cb` Completion callback function.
- `userdata` User data.
