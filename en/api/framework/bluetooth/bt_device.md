\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/bt_device.md) \]

# Bluetooth Device Management API

openvela Bluetooth remote device management interface, providing device pairing, connection, property query, and management functions.

Header file: `#include "bt_device.h"`


## openvela Implementation Notes

- **Device properties**: Supports querying remote device name, address, type, bond state, connection state, etc.
- **Pairing management**: Supports initiating pairing, canceling pairing, and confirming pair requests
- **Connection management**: Supports establishing and disconnecting connections with remote devices
- **Asynchronous mode**: Most APIs provide both synchronous and asynchronous versions


## Synchronous Interfaces


### bt_device_get_identity_address

```c
bt_status_t bt_device_get_identity_address(bt_instance_t* ins, bt_address_t* bd_addr, bt_address_t* id_addr);
```

Gets the identity address of a remote device, used to identify BLE devices using random addresses.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `bd_addr` Remote device BLE address.
- `id_addr` Output parameter, stores the identity address.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_device_get_address_type

```c
ble_addr_type_t bt_device_get_address_type(bt_instance_t* ins, bt_address_t* addr);
```

Gets the BLE address type of a remote device (Public/Static Random/RPA, etc.).

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.

**Returns**:

Returns the BLE address type of the device, or `BLE_ADDR_TYPE_UNKNOWN` if not found.


### bt_device_get_device_type

```c
bt_device_type_t bt_device_get_device_type(bt_instance_t* ins, bt_address_t* addr);
```

Gets the type of a remote device (Classic Bluetooth/BLE/Dual-mode).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Remote device Bluetooth address.


**Returns**:

Returns the device type, see `bt_device_type_t`.


### bt_device_get_name

```c
bool bt_device_get_name(bt_instance_t* ins, bt_address_t* addr, char* name, uint32_t length);
```

Gets the Bluetooth name of a remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Remote device Bluetooth address.
- `name` Name buffer.
- `length` Buffer length.


**Returns**:

Returns `true` on success, `false` on failure.


### bt_device_get_device_class

```c
uint32_t bt_device_get_device_class(bt_instance_t* ins, bt_address_t* addr);
```

Gets the Class of Device of a remote device, containing major device class, minor device class, and service class information.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.

**Returns**:

Returns the 24-bit Class of Device value.


### bt_device_get_uuids

```c
bt_status_t bt_device_get_uuids(bt_instance_t* ins, bt_address_t* addr, bt_uuid_t** uuids, uint16_t* size, bt_allocator_t allocator);
```

Gets the list of service UUIDs supported by a remote device.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.
- `allocator` Memory allocator function.
- `uuids` UUID array (allocated by allocator).
- `size` Returns the number of UUIDs.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_device_get_appearance

```c
uint16_t bt_device_get_appearance(bt_instance_t* ins, bt_address_t* addr);
```

Gets the BLE Appearance value of a remote device, used to identify the physical appearance of the device.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.


### bt_device_get_rssi

```c
int8_t bt_device_get_rssi(bt_instance_t* ins, bt_address_t* addr);
```

Gets the Received Signal Strength Indication (RSSI) of a remote device.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.


### bt_device_get_alias

```c
bool bt_device_get_alias(bt_instance_t* ins, bt_address_t* addr, char* alias, uint32_t length);
```

Gets the user-defined alias of a remote device; returns the device name if no alias is set.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.
- `length` Buffer length.
- `alias` Output parameter, stores the alias string.


**Returns**:

Returns `true` on success, `false` on failure.


### bt_device_set_alias

```c
bt_status_t bt_device_set_alias(bt_instance_t* ins, bt_address_t* addr, const char* alias);
```

Sets the user-defined alias of a remote device, with a maximum length of BT_LOC_NAME_MAX_LEN.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.
- `alias` Device alias.

**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.



### bt_device_is_connected

```c
bool bt_device_is_connected(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

Check whether the connection to the remote device is established.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.
- `transport` Transport type, see bt_transport_t.

**Returns**:

Returns `true` if connected, `false` otherwise.


### bt_device_is_encrypted

```c
bool bt_device_is_encrypted(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

Query whether the connection to the remote device is encrypted.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.
- `transport` Transport type, see bt_transport_t.

**Returns**:

Returns `true` if encrypted, `false` otherwise.


### bt_device_is_bond_initiate_local

```c
bool bt_device_is_bond_initiate_local(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

Query whether the pairing with the remote device was initiated locally.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.
- `transport` Transport type, see bt_transport_t.

**Returns**:

Returns `true` if bonding was initiated locally, `false` otherwise.


### bt_device_get_bond_state

```c
bond_state_t bt_device_get_bond_state(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

Get the bond state with the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).


**Returns**:

Returns the current bond state, see bond_state_t.


### bt_device_is_bonded

```c
bool bt_device_is_bonded(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

Query whether the remote device is bonded.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).


**Returns**:

Returns `true` if bonded, `false` otherwise.


### bt_device_create_bond

```c
bt_status_t bt_device_create_bond(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

Initiate bonding with the remote device to establish a long-term security relationship.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_device_set_security_level

```c
bt_status_t bt_device_set_security_level(bt_instance_t* ins, uint8_t level, bt_transport_t transport);
```

Set the security level (0-4) for the remote device; the higher the level, the stronger the security.

**Parameters**:

- `ins` Bluetooth client instance.
- `level` Security level.
- `transport` Transport type (BR/EDR or BLE).


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_device_set_bondable_le

```c
bt_status_t bt_device_set_bondable_le(bt_instance_t* ins, bool bondable);
```

Set whether the remote device is allowed to be paired via BLE.

**Parameters**:

- `ins` Bluetooth client instance.
- `bondable` Whether bonding is allowed.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_device_remove_bond

```c
bt_status_t bt_device_remove_bond(bt_instance_t* ins, bt_address_t* addr, uint8_t transport);
```

Remove the bond with the remote device and delete the stored pairing keys.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_device_cancel_bond

```c
bt_status_t bt_device_cancel_bond(bt_instance_t* ins, bt_address_t* addr);
```

Cancel an ongoing bonding process.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_device_pair_request_reply

```c
bt_status_t bt_device_pair_request_reply(bt_instance_t* ins, bt_address_t* addr, bool accept);
```

Reply to a pairing request from the remote device, accepting or rejecting the pairing.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `accept` Whether to accept.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_device_set_pairing_confirmation

```c
bt_status_t bt_device_set_pairing_confirmation(bt_instance_t* ins, bt_address_t* addr, uint8_t transport, bool accept);
```

Confirm or reject the numeric comparison request of an SSP pairing.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `accept` Whether to accept.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_device_set_pin_code

```c
bt_status_t bt_device_set_pin_code(bt_instance_t* ins, bt_address_t* addr, bool accept, char* pincode, int len);
```

Set the PIN code for legacy pairing authentication.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `accept` Whether to accept.
- `pincode` PIN code string.
- `len` Length.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_device_set_pass_key

```c
bt_status_t bt_device_set_pass_key(bt_instance_t* ins, bt_address_t* addr, uint8_t transport, bool accept, uint32_t passkey);
```

Set the numeric pass key for SSP pairing authentication.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `accept` Whether to accept.
- `passkey` Pairing pass key.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_device_set_le_legacy_tk

```c
bt_status_t bt_device_set_le_legacy_tk(bt_instance_t* ins, bt_address_t* addr, bt_128key_t tk_val);
```

Set the TK value for BLE Legacy pairing.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `tk_val` OOB TK value.


### bt_device_set_le_sc_remote_oob_data

```c
bt_status_t bt_device_set_le_sc_remote_oob_data(bt_instance_t* ins, bt_address_t* addr, bt_128key_t c_val, bt_128key_t r_val);
```

Set the BLE Secure Connections OOB data of the remote device for out-of-band pairing.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `c_val` SC confirmation value (128 bits).
- `r_val` SC random value (128 bits).



- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.
- `c_val` LE Secure Connections confirmation value (128-bit key).
- `r_val` LE Secure Connections random value (128-bit key).


### bt_device_get_le_sc_local_oob_data

```c
bt_status_t bt_device_get_le_sc_local_oob_data(bt_instance_t* ins, bt_address_t* addr);
```

Get the local BLE SC OOB data.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_device_connect

```c
bt_status_t bt_device_connect(bt_instance_t* ins, bt_address_t* addr);
```

Initiate a connection to the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_device_background_connect

```c
bt_status_t bt_device_background_connect(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

Initiate a background connection to the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_device_disconnect

```c
bt_status_t bt_device_disconnect(bt_instance_t* ins, bt_address_t* addr);
```

Disconnect from the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negated error code on failure.


### bt_device_background_disconnect

```c
bt_status_t bt_device_background_disconnect(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport);
```

Disconnect from the remote device in the background.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


### bt_device_connect_le

```c
bt_status_t bt_device_connect_le(bt_instance_t* ins, bt_address_t* addr, ble_addr_type_t type, ble_connect_params_t* param);
```

Initiate a BLE connection to the remote device.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Bluetooth address.
- `type` LE address type, see ble_addr_type_t.
- `param` Pointer to connection parameters, see ble_connect_params_t.


### bt_device_disconnect_le

```c
bt_status_t bt_device_disconnect_le(bt_instance_t* ins, bt_address_t* addr);
```

Disconnect the BLE connection to the remote device.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Bluetooth address.


### bt_device_connect_request_reply

```c
bt_status_t bt_device_connect_request_reply(bt_instance_t* ins, bt_address_t* addr, bool accept);
```

Reply to a connection request from the remote device, accepting or rejecting the connection.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `accept` Whether to accept.


### bt_device_set_le_phy

```c
bt_status_t bt_device_set_le_phy(bt_instance_t* ins, bt_address_t* addr, ble_phy_type_t tx_phy, ble_phy_type_t rx_phy);
```

Set the BLE PHY configuration (1M/2M/Coded) for the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `tx_phy` Transmit PHY.
- `rx_phy` Receive PHY.



- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Bluetooth address.
- `tx_phy` Preferred TX PHY, see ble_phy_type_t.
- `rx_phy` Preferred RX PHY, see ble_phy_type_t.


### bt_device_connect_all_profile

```c
void bt_device_connect_all_profile(bt_instance_t* ins, bt_address_t* addr);
```

Connect all profile connections.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.


### bt_device_disconnect_all_profile

```c
void bt_device_disconnect_all_profile(bt_instance_t* ins, bt_address_t* addr);
```

Disconnect all profile connections with the remote device.


**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.




### bt_device_enable_enhanced_mode

```c
bt_status_t bt_device_enable_enhanced_mode(bt_instance_t* ins, bt_address_t* addr, bt_enhanced_mode_t mode);
```

Enable the enhanced mode with the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `mode` Mode.


### bt_device_disable_enhanced_mode

```c
bt_status_t bt_device_disable_enhanced_mode(bt_instance_t* ins, bt_address_t* addr, bt_enhanced_mode_t mode);
```

Disable the enhanced mode with the remote device.


**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Remote device address.
- `mode` Enhanced mode to disable, see bt_enhanced_mode_t.


## Asynchronous Interfaces


### bt_device_get_identity_address_async

```c
bt_status_t bt_device_get_identity_address_async(bt_instance_t* ins, bt_address_t* bd_addr, bt_address_cb_t cb, void* userdata);
```

Get the identity address (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `bd_addr` BLE address.
- `cb` Callback function.
- `userdata` User data.


### bt_device_get_address_type_async

```c
bt_status_t bt_device_get_address_type_async(bt_instance_t* ins, bt_address_t* addr, bt_device_get_address_type_cb_t cb, void* userdata);
```

Get the BLE address type of the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.



### bt_device_get_device_type_async

```c
bt_status_t bt_device_get_device_type_async(bt_instance_t* ins, bt_address_t* addr, bt_device_type_cb_t cb, void* userdata);
```

Get the device type (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.


### bt_device_get_name_async

```c
bt_status_t bt_device_get_name_async(bt_instance_t* ins, bt_address_t* addr, bt_string_cb_t cb, void* userdata);
```

Get the name of the remote device (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.



### bt_device_get_device_class_async

```c
bt_status_t bt_device_get_device_class_async(bt_instance_t* ins, bt_address_t* addr, bt_u32_cb_t cb, void* userdata);
```

Get the device class (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.


### bt_device_get_uuids_async

```c
bt_status_t bt_device_get_uuids_async(bt_instance_t* ins, bt_address_t* addr, bt_uuids_cb_t cb, void* userdata);
```

Get the list of UUIDs supported by the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.



### bt_device_get_appearance_async

```c
bt_status_t bt_device_get_appearance_async(bt_instance_t* ins, bt_address_t* addr, bt_u16_cb_t cb, void* userdata);
```

Get the appearance characteristic value (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.


### bt_device_get_rssi_async

```c
bt_status_t bt_device_get_rssi_async(bt_instance_t* ins, bt_address_t* addr, bt_s8_cb_t cb, void* userdata);
```

Get the RSSI (received signal strength) of the remote device (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.



### bt_device_get_alias_async

```c
bt_status_t bt_device_get_alias_async(bt_instance_t* ins, bt_address_t* addr, bt_string_cb_t cb, void* userdata);
```

Get the alias (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.


### bt_device_set_alias_async

```c
bt_status_t bt_device_set_alias_async(bt_instance_t* ins, bt_address_t* addr, const char* alias, bt_status_cb_t cb, void* userdata);
```

Set the alias of the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `alias` Alias.
- `cb` Callback function.
- `userdata` User data.



### bt_device_is_connected_async

```c
bt_status_t bt_device_is_connected_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_bool_cb_t cb, void* userdata);
```

Check whether the device is connected (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `cb` Callback function.
- `userdata` User data.


### bt_device_is_encrypted_async

```c
bt_status_t bt_device_is_encrypted_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_bool_cb_t cb, void* userdata);
```

Check whether the connection to the remote device is encrypted.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `cb` Callback function.
- `userdata` User data.



### bt_device_is_bond_initiate_local_async

```c
bt_status_t bt_device_is_bond_initiate_local_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_bool_cb_t cb, void* userdata);
```

Query whether bonding was initiated locally (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `cb` Callback function.
- `userdata` User data.


### bt_device_get_bond_state_async

```c
bt_status_t bt_device_get_bond_state_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_device_get_bond_state_cb_t cb, void* userdata);
```

Get the bond state with the remote device (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `cb` Callback function.
- `userdata` User data.



### bt_device_is_bonded_async

```c
bt_status_t bt_device_is_bonded_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_bool_cb_t cb, void* userdata);
```

Query whether the device is bonded (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `cb` Callback function.
- `userdata` User data.


### bt_device_connect_async

```c
bt_status_t bt_device_connect_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

Connect to the remote device (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.



### bt_device_disconnect_async

```c
bt_status_t bt_device_disconnect_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

Disconnect from the remote device (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.


### bt_device_connect_le_async

```c
bt_status_t bt_device_connect_le_async(bt_instance_t* ins, bt_address_t* addr, ble_addr_type_t type, ble_connect_params_t* param, bt_status_cb_t cb, void* userdata);
```

Connect to a remote BLE device (asynchronous version, with specified connection parameters).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `type` Type.
- `param` Connection parameters structure.
- `cb` Callback function.
- `userdata` User data.



### bt_device_disconnect_le_async

```c
bt_status_t bt_device_disconnect_le_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

Disconnect a BLE connection (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.


### bt_device_connect_request_reply_async

```c
bt_status_t bt_device_connect_request_reply_async(bt_instance_t* ins, bt_address_t* addr, bool accept, bt_status_cb_t cb, void* userdata);
```

Reply to a connection request (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `accept` Whether to accept.
- `cb` Callback function.
- `userdata` User data.



### bt_device_connect_all_profile_async

```c
bt_status_t bt_device_connect_all_profile_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

Connect all profile connections (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.


### bt_device_disconnect_all_profile_async

```c
bt_status_t bt_device_disconnect_all_profile_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

Disconnect all profile connections (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.



### bt_device_set_le_phy_async

```c
bt_status_t bt_device_set_le_phy_async(bt_instance_t* ins, bt_address_t* addr, ble_phy_type_t tx_phy, ble_phy_type_t rx_phy, bt_status_cb_t cb, void* userdata);
```

Set the BLE PHY configuration (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `tx_phy` Transmit PHY.
- `rx_phy` Receive PHY.
- `cb` Callback function.
- `userdata` User data.


### bt_device_create_bond_async

```c
bt_status_t bt_device_create_bond_async(bt_instance_t* ins, bt_address_t* addr, bt_transport_t transport, bt_status_cb_t cb, void* userdata);
```

Initiate bonding with the remote device (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `cb` Callback function.
- `userdata` User data.



### bt_device_remove_bond_async

```c
bt_status_t bt_device_remove_bond_async(bt_instance_t* ins, bt_address_t* addr, uint8_t transport, bt_status_cb_t cb, void* userdata);
```

Remove the bond (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `cb` Callback function.
- `userdata` User data.


### bt_device_cancel_bond_async

```c
bt_status_t bt_device_cancel_bond_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

Cancel an ongoing bonding process (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.



### bt_device_pair_request_reply_async

```c
bt_status_t bt_device_pair_request_reply_async(bt_instance_t* ins, bt_address_t* addr, bool accept, bt_status_cb_t cb, void* userdata);
```

Reply to a pairing request (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `accept` Whether to accept.
- `cb` Callback function.
- `userdata` User data.


### bt_device_set_pairing_confirmation_async

```c
bt_status_t bt_device_set_pairing_confirmation_async(bt_instance_t* ins, bt_address_t* addr, uint8_t transport, bool accept, bt_status_cb_t cb, void* userdata);
```

Set the pairing confirmation (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `accept` Whether to accept.
- `cb` Callback function.
- `userdata` User data.



### bt_device_set_pin_code_async

```c
bt_status_t bt_device_set_pin_code_async(bt_instance_t* ins, bt_address_t* addr, bool accept, char* pincode, int len, bt_status_cb_t cb, void* userdata);
```

Set the PIN code (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `accept` Whether to accept.
- `pincode` PIN code string.
- `len` Length.
- `cb` Callback function.
- `userdata` User data.


### bt_device_set_pass_key_async

```c
bt_status_t bt_device_set_pass_key_async(bt_instance_t* ins, bt_address_t* addr, uint8_t transport, bool accept, uint32_t passkey, bt_status_cb_t cb, void* userdata);
```

Set the pass key (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `transport` Transport type (BR/EDR or BLE).
- `accept` Whether to accept.
- `passkey` Pairing pass key.
- `cb` Callback function.
- `userdata` User data.



### bt_device_set_le_legacy_tk_async

```c
bt_status_t bt_device_set_le_legacy_tk_async(bt_instance_t* ins, bt_address_t* addr, bt_128key_t tk_val, bt_status_cb_t cb, void* userdata);
```

Set the TK value for BLE Legacy pairing (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `tk_val` OOB TK value.
- `cb` Callback function.
- `userdata` User data.


### bt_device_set_le_sc_remote_oob_data_async

```c
bt_status_t bt_device_set_le_sc_remote_oob_data_async(bt_instance_t* ins, bt_address_t* addr, bt_128key_t c_val, bt_128key_t r_val, bt_status_cb_t cb, void* userdata);
```

Set the remote OOB data for LE SC pairing (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `c_val` SC confirmation value.
- `r_val` SC random value.
- `cb` Callback function.
- `userdata` User data.



### bt_device_get_le_sc_local_oob_data_async

```c
bt_status_t bt_device_get_le_sc_local_oob_data_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

Get the local OOB data for LE SC pairing (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Bluetooth address of the remote device.
- `cb` Callback function.
- `userdata` User data.

