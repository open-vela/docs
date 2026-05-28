\[ English | [简体中文](../../../../zh-cn/api/framework/telephony/telephony_manager.md) \]

# Telephony Manager API

Cellular communication management interfaces, including initialization, status query, and event registration.

Header: `#include <tapi_manager.h>`

## openvela Implementation Notes

- **D-Bus Based**: TAPI Manager communicates with the Telephony Core Stack (oFono) via D-Bus, exposing standard C interfaces externally
- **SIM identification**: The manager layer does not directly handle SIM slot selection; slot-specific operations use the `slot_id` parameter in submodules such as `tapi_sim`
- **Client Handle**: Obtain a `tapi_context` via `tapi_open`; all subsequent calls take this context as the first parameter
- **Event Subscription**: Register event callbacks via `tapi_register`, unsubscribe via `tapi_unregister`
- **Synchronous vs Asynchronous**: Most interfaces are asynchronous (with callbacks); some provide `*_sync` variants for simple scenarios

## Client Connection Management

### tapi_open

```c
tapi_context tapi_open(const char* client_name, tapi_client_ready_function callback, void* user_data);
```

Open a Telephony connection and obtain a context handle.

**Parameters**:

- `client_name` Client name.
- `callback` Callback function.
- `user_data` User data passed to the callback function.

**Returns**:

Returns a valid `tapi_context` handle on success, or `NULL` on failure.



### tapi_open_service

```c
tapi_context tapi_open_service(const char* client_name, tapi_client_ready_function callback, void* user_data, unsigned int tapi_service);
```

Open a Telephony connection with a specified service type.

**Parameters**:

- `client_name` Client name.
- `callback` Callback function.
- `user_data` User data passed to the callback function.
- `tapi_service` Telephony service type.

**Returns**:

Returns a valid `tapi_context` handle on success, or `NULL` on failure.



### tapi_close

```c
int tapi_close(tapi_context context);
```

Close a Telephony connection.

**Parameters**:

- `context` Telephony context handle.

**Returns**:

Returns 0 on success, or a negative error code on failure.



## Capability Query

### tapi_is_feature_supported

```c
bool tapi_is_feature_supported(tapi_feature_type feature);
```

Query whether a specified feature is supported.

**Parameters**:

- `feature` Feature type enum value.

**Returns**:

Returns `true` if supported, `false` otherwise.



## Radio Control

### tapi_set_radio_power

```c
int tapi_set_radio_power(tapi_context context, int slot_id, int event_id, bool state, tapi_async_function p_handle);
```

Set radio power.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `state` State.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_set_radio_power_async

```c
int tapi_set_radio_power_async(tapi_context context, int slot_id, int event_id, bool state, void* user_data, tapi_async_function p_handle);
```

Set radio power (asynchronous version).

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `state` State.
- `user_data` User data passed to the callback function.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_radio_power

```c
int tapi_get_radio_power(tapi_context context, int slot_id, bool* out);
```

Get radio power state.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



## Network Mode

### tapi_set_pref_net_mode

```c
int tapi_set_pref_net_mode(tapi_context context, int slot_id, int event_id, tapi_pref_net_mode mode, tapi_async_function p_handle);
```

Set preferred network mode.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `mode` Mode.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_pref_net_mode

```c
int tapi_get_pref_net_mode(tapi_context context, int slot_id, tapi_pref_net_mode* out);
```

Get preferred network mode.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_radio_state

```c
int tapi_get_radio_state(tapi_context context, int slot_id, tapi_radio_state* out);
```

Get radio state.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



## Modem Information

### tapi_get_imei

```c
int tapi_get_imei(tapi_context context, int slot_id, char** out);
```

Get device IMEI.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_imeisv

```c
int tapi_get_imeisv(tapi_context context, int slot_id, char** out);
```

Get device IMEISV.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_modem_revision

```c
int tapi_get_modem_revision(tapi_context context, int slot_id, char** out);
```

Get Modem revision information.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_phone_state

```c
int tapi_get_phone_state(tapi_context context, int slot_id, tapi_phone_state* state);
```

Get phone state.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `state` State.

**Returns**:

Returns 0 on success, or a negative error code on failure.



## Phone Number

### tapi_get_msisdn_number

```c
int tapi_get_msisdn_number(tapi_context context, int slot_id, char** out);
```

Get SIM card phone number (MSISDN).

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



## Modem Status and Control

### tapi_get_modem_activity_info

```c
int tapi_get_modem_activity_info(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

Get Modem activity information.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_invoke_oem_ril_request_raw

```c
int tapi_invoke_oem_ril_request_raw(tapi_context context, int slot_id, int event_id, unsigned char oem_req[], int length, tapi_async_function p_handle);
```

Send an OEM RIL request.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `oem_req` OEM request data.
- `length` Data length.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_invoke_oem_ril_request_strings

```c
int tapi_invoke_oem_ril_request_strings(tapi_context context, int slot_id, int event_id, char* oem_req[], int length, tapi_async_function p_handle);
```

Send an OEM RIL request.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `oem_req` OEM request data.
- `length` Data length.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_enable_modem

```c
int tapi_enable_modem(tapi_context context, int slot_id, int event_id, bool enable, tapi_async_function p_handle);
```

Enable or disable Modem.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `enable` Whether to enable.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_enable_modem_abnormal_event

```c
int tapi_enable_modem_abnormal_event(tapi_context context, int slot_id, bool enable, int event_id, int module_mask, int from_event_id, int to_event_id, tapi_async_function p_handle);
```

Enable Modem abnormal event reporting.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `enable` Whether to enable.
- `event_id` Event ID for callback matching.
- `module_mask` Module mask.
- `from_event_id` Source event ID.
- `to_event_id` Target event ID.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_set_signal_report_threshold

```c
int tapi_set_signal_report_threshold(tapi_context context, int slot_id, int event_id, int type, tapi_async_function p_handle);
```

Set signal report threshold.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `type` Type.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_suppress_message_report

```c
int tapi_suppress_message_report(tapi_context context, int slot_id, int event_id, bool enable, tapi_async_function p_handle);
```

Suppress message reporting.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `enable` Whether to enable.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_enable_modem_stationary

```c
int tapi_enable_modem_stationary(tapi_context context, int slot_id, int event_id, bool enable, tapi_async_function p_handle);
```

Enable Modem stationary mode.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `enable` Whether to enable.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_set_modem_stationary_threshold

```c
int tapi_set_modem_stationary_threshold(tapi_context context, int slot_id, int event_id, int value, tapi_async_function p_handle);
```

Set Modem stationary threshold.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `value` Value.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_modem_status

```c
int tapi_get_modem_status(tapi_context context, int slot_id, int event_id, tapi_async_function p_handle);
```

Get Modem status.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_modem_status_sync

```c
int tapi_get_modem_status_sync(tapi_context context, int slot_id, tapi_modem_state* out);
```

Get Modem status (synchronous version).

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_set_fast_dormancy

```c
int tapi_set_fast_dormancy(tapi_context context, int slot_id, int event_id, bool state, tapi_async_function p_handle);
```

Set fast dormancy.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `event_id` Event ID for callback matching.
- `state` State.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_phone_number

```c
int tapi_get_phone_number(tapi_context context, int slot_id, char** out);
```

Get local phone number.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



## Event Subscription

### tapi_register

```c
int tapi_register(tapi_context context, int slot_id, tapi_indication_msg msg, void* user_obj, tapi_async_function p_handle);
```

Register an event callback.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `msg` Message content.
- `user_obj` User object pointer.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_unregister

```c
int tapi_unregister(tapi_context context, int watch_id);
```

Unregister an event callback.

**Parameters**:

- `context` Telephony context handle.
- `watch_id` Watch ID (used to cancel the subscription).

**Returns**:

Returns 0 on success, or a negative error code on failure.



## Carrier Configuration

### tapi_get_carrier_config_bool

```c
int tapi_get_carrier_config_bool(tapi_context context, int slot_id, char* key, bool* out);
```

Get a boolean carrier configuration value.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `key` Key name.
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_carrier_config_int

```c
int tapi_get_carrier_config_int(tapi_context context, int slot_id, char* key, int* out);
```

Get an integer carrier configuration value.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `key` Key name.
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_get_carrier_config_string

```c
int tapi_get_carrier_config_string(tapi_context context, int slot_id, char* key, char** out);
```

Get a string carrier configuration value.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM slot ID (0 or 1).
- `key` Key name.
- `out` Output parameter.

**Returns**:

Returns 0 on success, or a negative error code on failure.
