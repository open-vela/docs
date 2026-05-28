\[ English | [简体中文](../../../../zh-cn/api/framework/telephony/telephony_sms.md) \]

# SMS Management API

SMS sending and receiving.

Header: `#include <tapi_sms.h>`

## openvela Implementation Notes

- **Text and Data SMS**: `send_message` sends text SMS, `send_data_message` sends binary PDU
- **Service Center Address**: Configure the carrier SMS gateway via `set_service_center_address` / `get_service_center_address`
- **Delivery Report**: Toggle delivery reports with `enable_delivery_report`
- **SIM Card Storage**: Provides `get_all_messages_from_sim` / `copy_message_to_sim` / `delete_message_from_sim` to operate on SMS stored on the SIM card
- **Event Subscription**: `tapi_sms_register` listens for incoming/outgoing message events

## Sending SMS

### tapi_sms_send_message

```c
int tapi_sms_send_message(tapi_context context, int slot_id, int sms_id, char* number, char* text, int event_id, tapi_async_function p_handle);
```

Sends a text SMS message.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).
- `sms_id` SMS message ID.
- `number` Phone number.
- `text` Text content.
- `event_id` Event ID for callback matching.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_sms_send_data_message

```c
int tapi_sms_send_data_message(tapi_context context, int slot_id, int sms_id, char* dest_addr, unsigned int port, char* text, int event_id, tapi_async_function p_handle);
```

Sends a data SMS message.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).
- `sms_id` SMS message ID.
- `dest_addr` Destination number.
- `port` Port number.
- `text` Text content.
- `event_id` Event ID for callback matching.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



## Service Center and Delivery Report

### tapi_sms_set_service_center_address

```c
bool tapi_sms_set_service_center_address(tapi_context context, int slot_id, char* number);
```

Sets the SMSC (Short Message Service Center) address.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).
- `number` SMSC phone number.

**Returns**:

Returns `true` on success, `false` on failure.



### tapi_sms_get_service_center_address

```c
int tapi_sms_get_service_center_address(tapi_context context, int slot_id, char** number);
```

Gets the SMSC (Short Message Service Center) address.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).
- `number` Pointer to receive the SMSC phone number.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_sms_enable_delivery_report

```c
int tapi_sms_enable_delivery_report(tapi_context context, int slot_id, bool enable);
```

Enables or disables SMS delivery reports.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).
- `enable` Whether to enable delivery reports.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_sms_get_delivery_report_status

```c
int tapi_sms_get_delivery_report_status(tapi_context context, int slot_id, bool* out);
```

Gets the current delivery report status.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).
- `out` Output parameter to receive the status.

**Returns**:

Returns 0 on success, or a negative error code on failure.



## SIM Card SMS Storage

### tapi_sms_get_all_messages_from_sim

```c
int tapi_sms_get_all_messages_from_sim(tapi_context context, int slot_id, tapi_message_list* list, tapi_async_function p_handle);
```

Retrieves all SMS messages stored on the SIM card.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).
- `list` Message list to populate.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_sms_copy_message_to_sim

```c
int tapi_sms_copy_message_to_sim(tapi_context context, int slot_id, char* number, char* text, char* send_time, int type);
```

Copies an SMS message to the SIM card.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).
- `number` Phone number.
- `text` Text content.
- `send_time` Send time.
- `type` Message type.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_sms_delete_message_from_sim

```c
int tapi_sms_delete_message_from_sim(tapi_context context, int slot_id, int index);
```

Deletes an SMS message from the SIM card.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).
- `index` Message index on the SIM card.

**Returns**:

Returns 0 on success, or a negative error code on failure.



## Event Subscription and Default Slot

### tapi_sms_register

```c
int tapi_sms_register(tapi_context context, int slot_id, tapi_indication_msg msg, void* user_obj, tapi_async_function p_handle);
```

Registers for SMS event notifications.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).
- `msg` Indication message type.
- `user_obj` User object pointer.
- `p_handle` Asynchronous callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_sms_unregister

```c
int tapi_sms_unregister(tapi_context context, int watch_id);
```

Unregisters from SMS event notifications.

**Parameters**:

- `context` Telephony context handle.
- `watch_id` Watch ID (used to cancel the subscription).

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_sms_set_default_slot

```c
int tapi_sms_set_default_slot(tapi_context context, int slot_id);
```

Sets the default SIM slot for SMS.

**Parameters**:

- `context` Telephony context handle.
- `slot_id` SIM card slot ID (0 or 1).

**Returns**:

Returns 0 on success, or a negative error code on failure.



### tapi_sms_get_default_slot

```c
int tapi_sms_get_default_slot(tapi_context context, int* out);
```

Gets the default SIM slot for SMS.

**Parameters**:

- `context` Telephony context handle.
- `out` Output parameter to receive the default slot ID.

**Returns**:

Returns 0 on success, or a negative error code on failure.
