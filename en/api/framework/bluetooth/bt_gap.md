\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/bt_gap.md) \]

# Bluetooth GAP API

The openvela Bluetooth GAP (Generic Access Profile) interface provides adapter management, including enabling/disabling, device discovery, property configuration, and pairing management.

Header file: `#include "bt_adapter.h"`

## openvela Implementation Notes

- **Dual-mode support**: Supports independent control of Classic Bluetooth (BR/EDR) and Bluetooth Low Energy (BLE)
- **Asynchronous mode**: Most APIs provide both synchronous and asynchronous versions. Asynchronous versions are named with the `_async` suffix and return results via callback
- **Instance management**: The first parameter of every API is `bt_instance_t* ins` (Bluetooth client instance), obtained from `bt_open()`
- **State machine**: The adapter state follows the transition flow OFF → BLE_TURNING_ON → BLE_ON → TURNING_ON → ON


## Adapter Control


#### bt_adapter_get_state

```c
bt_adapter_state_t bt_adapter_get_state(bt_instance_t* ins);
```

Gets the adapter state.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.

**Returns**:

The current adapter state.


#### bt_adapter_is_support_le

```c
bool bt_adapter_is_support_le(bt_instance_t* ins);
```

Queries whether BLE is supported.

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

Returns true if BLE is supported, false otherwise.


#### bt_adapter_is_support_leaudio

```c
bool bt_adapter_is_support_leaudio(bt_instance_t* ins);
```

Queries whether LE Audio is supported.

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

Returns true if LE Audio is supported, false otherwise.


## Device Discovery


#### bt_adapter_set_discovery_filter

```c
bt_status_t bt_adapter_set_discovery_filter(bt_instance_t* ins);
```

Sets the device discovery filter.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.


#### bt_adapter_start_discovery

```c
bt_status_t bt_adapter_start_discovery(bt_instance_t* ins, uint32_t timeout);
```

Starts device discovery.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `timeout` Timeout duration.

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


#### bt_adapter_cancel_discovery

```c
bt_status_t bt_adapter_cancel_discovery(bt_instance_t* ins);
```

Cancels device discovery.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


#### bt_adapter_is_discovering

```c
bool bt_adapter_is_discovering(bt_instance_t* ins);
```

Queries whether a device discovery is in progress.

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

Returns true if discovery is in progress, false otherwise.


## Property Management


#### bt_adapter_get_type

```c
bt_device_type_t bt_adapter_get_type(bt_instance_t* ins);
```

Gets the device type.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.


#### bt_adapter_set_name

```c
bt_status_t bt_adapter_set_name(bt_instance_t* ins, const char* name);
```

Sets the device name.

**Parameters**:

- `ins` Bluetooth client instance.
- `name` Name.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negative error code on failure.


#### bt_adapter_get_name

```c
void bt_adapter_get_name(bt_instance_t* ins, char* name, int length);
```

Gets the device name.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `name` Output parameter, stores the adapter name.
- `length` Buffer length.


#### bt_adapter_set_scan_mode

```c
bt_status_t bt_adapter_set_scan_mode(bt_instance_t* ins, bt_scan_mode_t mode, bool bondable);
```

Sets the scan mode.

**Parameters**:

- `ins` Bluetooth client instance.
- `mode` Scan mode.
- `bondable` Whether pairing is allowed.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


#### bt_adapter_get_scan_mode

```c
bt_scan_mode_t bt_adapter_get_scan_mode(bt_instance_t* ins);
```

Gets the scan mode.

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

The current scan mode.


#### bt_adapter_set_device_class

```c
bt_status_t bt_adapter_set_device_class(bt_instance_t* ins, uint32_t cod);
```

Sets the device class (CoD).

**Parameters**:

- `ins` Bluetooth client instance.
- `cod` Device class (CoD).


**Returns**:

Returns BT_STATUS_SUCCESS on success, or a negative error code on failure.


#### bt_adapter_get_device_class

```c
uint32_t bt_adapter_get_device_class(bt_instance_t* ins);
```

Gets the device class (CoD).

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

The current device class (CoD).


#### bt_adapter_set_debug_mode

```c
bt_status_t bt_adapter_set_debug_mode(bt_instance_t* ins, bt_debug_mode_t mode, uint8_t operation);
```

Sets the Bluetooth adapter debug mode for factory testing and RF certification.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `mode` Debug mode.
- `operation` Debug operation.


#### bt_adapter_set_le_address

```c
bt_status_t bt_adapter_set_le_address(bt_instance_t* ins, bt_address_t* addr);
```

Sets the local BLE address.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Pointer to the BLE identity address.


#### bt_adapter_set_le_appearance

```c
bt_status_t bt_adapter_set_le_appearance(bt_instance_t* ins, uint16_t appearance);
```

Sets the BLE appearance value.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `appearance` BLE appearance value.


#### bt_adapter_le_add_whitelist_with_type

```c
bt_status_t bt_adapter_le_add_whitelist_with_type(bt_instance_t* ins, bt_address_t* addr, ble_addr_type_t type);
```

Adds a device of the specified address type to the BLE whitelist.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Device address.
- `type` Address type.


## Pairing and Security


#### bt_adapter_set_io_capability

```c
bt_status_t bt_adapter_set_io_capability(bt_instance_t* ins, bt_io_capability_t cap);
```

Sets the IO capability.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `cap` IO capability value.


#### bt_adapter_get_bonded_devices

```c
bt_status_t bt_adapter_get_bonded_devices(bt_instance_t* ins, bt_transport_t transport, bt_address_t** addr, int* num, bt_allocator_t allocator);
```

Gets the list of bonded devices.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `transport` Transport type, see bt_transport_t.
- `allocator` Memory allocation function.
- `addr` Output parameter, stores the array of bonded device addresses.
- `num` Output parameter, stores the number of devices.


#### bt_adapter_disconnect_all_devices

```c
void bt_adapter_disconnect_all_devices(bt_instance_t* ins);
```

Disconnects all connected devices.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.


#### bt_adapter_get_le_io_capability

```c
uint32_t bt_adapter_get_le_io_capability(bt_instance_t* ins);
```

Gets the BLE IO capability.

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

Returns the BLE IO capability value.


## BLE Management


#### bt_adapter_enable

```c
bt_status_t bt_adapter_enable(bt_instance_t* ins);
```

Enables the Bluetooth adapter.

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


#### bt_adapter_disable

```c
bt_status_t bt_adapter_disable(bt_instance_t* ins);
```

Disables the Bluetooth adapter.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.

**Returns**:

Returns BT_STATUS_SUCCESS on success, or an error code on failure.


#### bt_adapter_disable_safe

```c
bt_status_t bt_adapter_disable_safe(bt_instance_t* ins);
```

Safely disables the Bluetooth adapter, waiting for all connections to be disconnected before shutting down.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.


#### bt_adapter_disable_le

```c
bt_status_t bt_adapter_disable_le(bt_instance_t* ins);
```

Disables Bluetooth Low Energy (BLE).

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.


#### bt_adapter_is_le_enabled

```c
bool bt_adapter_is_le_enabled(bt_instance_t* ins);
```

Queries whether BLE is enabled.

**Parameters**:

- `ins` Bluetooth client instance.


**Returns**:

Returns true if BLE is enabled, false otherwise.


#### bt_adapter_le_enable_key_derivation

```c
bt_status_t bt_adapter_le_enable_key_derivation(bt_instance_t* ins, bool brkey_to_lekey, bool lekey_to_brkey);
```

Enables BLE key derivation.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `brkey_to_lekey` Whether to enable BR→LE key derivation.
- `lekey_to_brkey` Whether to enable LE→BR key derivation.


#### bt_adapter_le_remove_whitelist

```c
bt_status_t bt_adapter_le_remove_whitelist(bt_instance_t* ins, bt_address_t* addr);
```

Removes a device from the BLE whitelist.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `addr` Address of the device to remove.


#### bt_adapter_set_page_scan_parameters

```c
bt_status_t bt_adapter_set_page_scan_parameters(bt_instance_t* ins, bt_scan_type_t type, uint16_t interval, uint16_t window);
```

Sets the page scan parameters.

**Parameters**:

- `ins` Bluetooth client instance, see bt_instance_t.
- `type` Scan type.
- `interval` Scan interval.
- `window` Scan window.


## Asynchronous Interfaces


#### bt_adapter_register_callback_async

```c
bt_status_t bt_adapter_register_callback_async(bt_instance_t* ins, const adapter_callbacks_t* adapter_cbs, bt_register_callback_cb_t cb, void* userdata);
```

Asynchronous version.

**Parameters**:

- `ins` Bluetooth client instance.
- `adapter_cbs` Adapter callback function set.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_unregister_callback_async

```c
bt_status_t bt_adapter_unregister_callback_async(bt_instance_t* ins, void* cookie, bt_bool_cb_t cb, void* userdata);
```

Unregisters a callback function (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cookie` User context.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_enable_async

```c
bt_status_t bt_adapter_enable_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

Adapter state change callback (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_disable_async

```c
bt_status_t bt_adapter_disable_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

Disables the Bluetooth adapter (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_enable_le_async

```c
bt_status_t bt_adapter_enable_le_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

Enables Bluetooth Low Energy (BLE) (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_disable_le_async

```c
bt_status_t bt_adapter_disable_le_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

Disables Bluetooth Low Energy (BLE) (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_get_state_async

```c
bt_status_t bt_adapter_get_state_async(bt_instance_t* ins, bt_adapter_get_state_cb_t get_state_cb, void* userdata);
```

Gets the current adapter state (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `get_state_cb` Callback function for getting the state.
- `userdata` User data.



#### bt_adapter_is_le_enabled_async

```c
bt_status_t bt_adapter_is_le_enabled_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

Checks if BLE is enabled (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_get_type_async

```c
bt_status_t bt_adapter_get_type_async(bt_instance_t* ins, bt_device_type_cb_t get_dtype_cb, void* userdata);
```

Gets the adapter device type (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `get_dtype_cb` Callback function for getting the device type.
- `userdata` User data.



#### bt_adapter_set_discovery_filter_async

```c
bt_status_t bt_adapter_set_discovery_filter_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

Sets the discovery filter (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_start_discovery_async

```c
bt_status_t bt_adapter_start_discovery_async(bt_instance_t* ins, uint32_t timeout, bt_status_cb_t cb, void* userdata);
```

Starts device discovery (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `timeout` Timeout duration.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_cancel_discovery_async

```c
bt_status_t bt_adapter_cancel_discovery_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

Cancels device discovery (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_is_discovering_async

```c
bt_status_t bt_adapter_is_discovering_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

Queries whether the adapter is performing device discovery (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_get_address_async

```c
bt_status_t bt_adapter_get_address_async(bt_instance_t* ins, bt_address_cb_t cb, void* userdata);
```

Reads the Bluetooth controller address (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_set_name_async

```c
bt_status_t bt_adapter_set_name_async(bt_instance_t* ins, const char* name, bt_status_cb_t cb, void* userdata);
```

Sets the adapter local name (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `name` Name.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_get_name_async

```c
bt_status_t bt_adapter_get_name_async(bt_instance_t* ins, bt_string_cb_t get_name_cb, void* userdata);
```

Gets the adapter local name (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `get_name_cb` Callback function for getting the name.
- `userdata` User data.



#### bt_adapter_get_uuids_async

```c
bt_status_t bt_adapter_get_uuids_async(bt_instance_t* ins, bt_uuids_cb_t get_uuids_cb, void* userdata);
```

Gets the list of UUIDs supported by the adapter (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `get_uuids_cb` Callback function for getting the UUID list.
- `userdata` User data.



#### bt_adapter_set_scan_mode_async

```c
bt_status_t bt_adapter_set_scan_mode_async(bt_instance_t* ins, bt_scan_mode_t mode, bool bondable, bt_status_cb_t cb, void* userdata);
```

Sets the adapter scan mode (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `mode` Mode.
- `bondable` Whether pairing is allowed.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_get_scan_mode_async

```c
bt_status_t bt_adapter_get_scan_mode_async(bt_instance_t* ins, bt_adapter_get_scan_mode_cb_t get_scan_mode_cb, void* userdata);
```

Gets the adapter scan mode (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `get_scan_mode_cb` Callback function for getting the scan mode.
- `userdata` User data.



#### bt_adapter_set_device_class_async

```c
bt_status_t bt_adapter_set_device_class_async(bt_instance_t* ins, uint32_t cod, bt_status_cb_t cb, void* userdata);
```

Sets the adapter device class (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cod` Device class (CoD).
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_get_device_class_async

```c
bt_status_t bt_adapter_get_device_class_async(bt_instance_t* ins, bt_u32_cb_t get_cod_cb, void* userdata);
```

Gets the adapter device class (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `get_cod_cb` Callback function for getting the device class.
- `userdata` User data.



#### bt_adapter_set_io_capability_async

```c
bt_status_t bt_adapter_set_io_capability_async(bt_instance_t* ins, bt_io_capability_t cap, bt_status_cb_t cb, void* userdata);
```

Sets the BR/EDR adapter IO capability (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cap` IO capability value.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_get_io_capability_async

```c
bt_status_t bt_adapter_get_io_capability_async(bt_instance_t* ins, bt_adapter_get_io_capability_cb_t get_ioc_cb, void* userdata);
```

Gets the BR/EDR adapter IO capability (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `get_ioc_cb` Callback function for getting the IO capability.
- `userdata` User data.



#### bt_adapter_set_inquiry_scan_parameters_async

```c
bt_status_t bt_adapter_set_inquiry_scan_parameters_async(bt_instance_t* ins, bt_scan_type_t type, uint16_t interval, uint16_t window, bt_status_cb_t cb, void* userdata);
```

Sets the inquiry scan parameters (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `type` Type.
- `interval` Interval.
- `window` Scan window (in time slots).
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_set_page_scan_parameters_async

```c
bt_status_t bt_adapter_set_page_scan_parameters_async(bt_instance_t* ins, bt_scan_type_t type, uint16_t interval, uint16_t window, bt_status_cb_t cb, void* userdata);
```

Sets the page scan parameters (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `type` Type.
- `interval` Interval.
- `window` Scan window (in time slots).
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_set_le_io_capability_async

```c
bt_status_t bt_adapter_set_le_io_capability_async(bt_instance_t* ins, uint32_t le_io_cap, bt_status_cb_t cb, void* userdata);
```

Sets the BLE adapter IO capability (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `le_io_cap` BLE IO capability value.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_get_le_io_capability_async

```c
bt_status_t bt_adapter_get_le_io_capability_async(bt_instance_t* ins, bt_u32_cb_t get_le_ioc_cb, void* userdata);
```

Gets the BLE adapter IO capability (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `get_le_ioc_cb` Callback function for getting the BLE IO capability.
- `userdata` User data.



#### bt_adapter_get_le_address_async

```c
bt_status_t bt_adapter_get_le_address_async(bt_instance_t* ins, bt_adapter_get_le_address_cb_t cb, void* userdata);
```

Gets the BLE adapter address (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_set_le_address_async

```c
bt_status_t bt_adapter_set_le_address_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

Sets the BLE private address (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Remote device Bluetooth address.
- `cb` Callback function.
- `userdata` User data.




#### bt_adapter_set_le_identity_address_async

```c
bt_status_t bt_adapter_set_le_identity_address_async(bt_instance_t* ins, bt_address_t* addr, bool is_public, bt_status_cb_t cb, void* userdata);
```

Sets the BLE identity address (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Remote device Bluetooth address.
- `is_public` Whether to use a public address.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_set_le_appearance_async

```c
bt_status_t bt_adapter_set_le_appearance_async(bt_instance_t* ins, uint16_t appearance, bt_status_cb_t cb, void* userdata);
```

Sets the BLE adapter appearance (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `appearance` Appearance value.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_get_le_appearance_async

```c
bt_status_t bt_adapter_get_le_appearance_async(bt_instance_t* ins, bt_u16_cb_t cb, void* userdata);
```

Gets the BLE adapter appearance (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_le_enable_key_derivation_async

```c
bt_status_t bt_adapter_le_enable_key_derivation_async(bt_instance_t* ins, bool brkey_to_lekey, bool lekey_to_brkey, bt_status_cb_t cb, void* userdata);
```

Enables or disables cross-transport key derivation (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `brkey_to_lekey` Whether to enable BR key derivation to LE key.
- `lekey_to_brkey` Whether to enable LE key derivation to BR key.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_le_add_whitelist_async

```c
bt_status_t bt_adapter_le_add_whitelist_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

Adds a device to the BLE whitelist (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Remote device Bluetooth address.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_le_remove_whitelist_async

```c
bt_status_t bt_adapter_le_remove_whitelist_async(bt_instance_t* ins, bt_address_t* addr, bt_status_cb_t cb, void* userdata);
```

Removes a device from the BLE whitelist (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Remote device Bluetooth address.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_get_bonded_devices_async

```c
bt_status_t bt_adapter_get_bonded_devices_async(bt_instance_t* ins, bt_transport_t transport, bt_adapter_get_devices_cb_t get_bonded_cb, void* userdata);
```

Gets the list of bonded devices (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `transport` Transport type (BR/EDR or BLE).
- `get_bonded_cb` Callback function for getting the bonded device list.
- `userdata` User data.



#### bt_adapter_get_connected_devices_async

```c
bt_status_t bt_adapter_get_connected_devices_async(bt_instance_t* ins, bt_transport_t transport, bt_adapter_get_devices_cb_t get_connected_cb, void* userdata);
```

Gets the list of connected devices (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `transport` Transport type (BR/EDR or BLE).
- `get_connected_cb` Callback function for getting the connected device list.
- `userdata` User data.



#### bt_adapter_set_afh_channel_classification_async

```c
bt_status_t bt_adapter_set_afh_channel_classification_async(bt_instance_t* ins, uint16_t central_frequency, uint16_t band_width, uint16_t number, bt_status_cb_t cb, void* userdata);
```

Sets AFH (Adaptive Frequency Hopping) channel classification (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `central_frequency` Central frequency (MHz).
- `band_width` Bandwidth (MHz).
- `number` Number.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_set_auto_sniff_async

```c
bt_status_t bt_adapter_set_auto_sniff_async(bt_instance_t* ins, bt_auto_sniff_params_t* params, bt_status_cb_t cb, void* userdata);
```

Sets the automatic sniff mode parameters (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `params` Parameter structure.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_disconnect_all_devices_async

```c
bt_status_t bt_adapter_disconnect_all_devices_async(bt_instance_t* ins, bt_status_cb_t cb, void* userdata);
```

Disconnects all connected devices (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_is_support_bredr_async

```c
bt_status_t bt_adapter_is_support_bredr_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

Checks if BR/EDR is supported (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_is_support_le_async

```c
bt_status_t bt_adapter_is_support_le_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

Checks if BLE is supported (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.



#### bt_adapter_is_support_leaudio_async

```c
bt_status_t bt_adapter_is_support_leaudio_async(bt_instance_t* ins, bt_bool_cb_t cb, void* userdata);
```

Queries whether LE Audio is supported (asynchronous version).

**Parameters**:

- `ins` Bluetooth client instance.
- `cb` Callback function.
- `userdata` User data.
