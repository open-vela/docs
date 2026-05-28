\[ English | [简体中文](../../../../zh-cn/api/framework/media/media_policy.md) \]

# Audio Policy API

Audio routing, device management, and mode switching policies.

Header file: `#include <media_policy.h>`

## openvela Implementation Notes

- **Parameter Framework (PFW) Backend**: Policy data is managed through the openvela PFW rule engine and can be dynamically switched at runtime.
- **Synchronous/Asynchronous Dual Model**: `media_policy_*` (synchronous) and `media_uv_policy_*` (asynchronous, based on libuv).
- **Policy Categories**: Covers 5 types of runtime control:
    - Audio Mode: Switching between scenarios such as call, media playback, and hands-free.
    - Device Routing: Enable/disable, availability, and usage state.
    - Stream Volume: Adjust volume by audio stream type.
    - Mute: Global mute and microphone mute.
    - Generic Parameters (int/string/include/exclude/contain): Extended configuration read/write.
- **Subscription Mechanism**: Monitor policy change events via `media_policy_subscribe` (synchronous interface only).
- **HFP Sample Rate**: Adjust Bluetooth hands-free audio sample rate via `set_hfp_samplerate`.

## Synchronous Interface - Audio Mode

### media_policy_set_audio_mode

```c
int media_policy_set_audio_mode(const char* mode);
```

Set the audio mode (e.g., call mode, normal mode).

**Parameters**:

- `mode` Mode constant.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_get_audio_mode

```c
int media_policy_get_audio_mode(char* mode, int len);
```

Get the current audio mode.

**Parameters**:

- `mode` Buffer address.
- `len` Buffer length.

**Returns**:

Returns 0 on success, or a negative error code on failure.


## Synchronous Interface - Device Usage

### media_policy_set_devices_use

```c
int media_policy_set_devices_use(const char* devices);
```

Force use of specified audio devices or protocols.

**Parameters**:

- `devices` Device constant; multiple devices separated by `|`.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_policy_set_devices_unuse

```c
int media_policy_set_devices_unuse(const char* devices);
```

Cancel forced use of audio devices.

**Parameters**:

- `devices` Device constant; multiple devices separated by `|`.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_policy_get_devices_use

```c
int media_policy_get_devices_use(char* devices, int len);
```

Get the currently forced-use audio devices.

**Parameters**:

- `devices` Device name string; multiple devices separated by `|` (e.g., `"sco"`, `"sco|mic"`, `"<none>"`).
- `len` Buffer length.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_policy_is_devices_use

```c
int media_policy_is_devices_use(const char* devices, int* use);
```

Check whether the specified devices are in forced-use state.

**Parameters**:

- `devices` Device constant; multiple devices separated by `|`.
- `use` Device usage status: 0 means none of the devices are in use, 1 means at least one device is in use.

**Returns**:

Returns `0` on success, or a negative errno on failure.


## Synchronous Interface - HFP Sample Rate and Device Availability

### media_policy_set_hfp_samplerate

```c
int media_policy_set_hfp_samplerate(int rate);
```

Set the HFP Bluetooth call sample rate. HFP (Hands-Free Profile) is based on BT-SCO; the sample rate is uncertain before negotiation is complete.

**Parameters**:

- `rate` Sample rate: 8000 for CVSD encoding, 16000 for mSBC encoding.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_set_devices_available

```c
int media_policy_set_devices_available(const char* devices);
```

Report that audio devices (or protocols) are available.

**Parameters**:

- `devices` Device constant; multiple devices separated by `|`.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_set_devices_unavailable

```c
int media_policy_set_devices_unavailable(const char* devices);
```

Report that audio devices (or protocols) are unavailable.

**Parameters**:

- `devices` Device constant; multiple devices separated by `|`.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_get_devices_available

```c
int media_policy_get_devices_available(char* devices, int len);
```

Get the currently available devices.

**Parameters**:

- `devices` Device name string; multiple devices separated by `|` (e.g., `"sco"`, `"sco|mic"`, `"<none>"`).
- `len` Buffer length.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_policy_is_devices_available

```c
int media_policy_is_devices_available(const char* devices, int* available);
```

Check whether the specified devices are available.

**Parameters**:

- `devices` Devices to check, using `MEDIA_DEVICE_*` constants; multiple devices separated by `|`.
- `available` Device availability status: 0 means none of the devices are available, 1 means at least one device is available.

**Returns**:

Returns `0` on success, or a negative errno on failure.


## Synchronous Interface - Mute Control

### media_policy_set_mute_mode

```c
int media_policy_set_mute_mode(int mute);
```

Set the mute mode.

**Parameters**:

- `mute` New mute mode: 0 to disable mute, 1 to enable mute.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_policy_get_mute_mode

```c
int media_policy_get_mute_mode(int* mute);
```

Get the current mute mode.

**Parameters**:

- `mute` Current mute mode: 0 means mute is disabled, 1 means mute is enabled.

**Returns**:

Returns `0` on success, or a negative errno on failure.


## Synchronous Interface - Volume Control

### media_policy_set_stream_volume

```c
int media_policy_set_stream_volume(const char* stream, int volume);
```

Set the volume index for a stream type.

**Parameters**:

- `stream` Stream type constant (MEDIA_STREAM_XXX).
- `volume` New volume level.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_policy_get_stream_volume

```c
int media_policy_get_stream_volume(const char* stream, int* volume);
```

Get the volume index for a stream type.

**Parameters**:

- `stream` Stream type constant (MEDIA_STREAM_XXX).
- `volume` Current volume level.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_policy_increase_stream_volume

```c
int media_policy_increase_stream_volume(const char* stream);
```

Increase the volume index for a stream type by 1.

**Parameters**:

- `stream` Stream type constant (MEDIA_STREAM_XXX).

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_policy_decrease_stream_volume

```c
int media_policy_decrease_stream_volume(const char* stream);
```

Decrease the volume index for a stream type by 1.

**Parameters**:

- `stream` Stream type constant (MEDIA_STREAM_XXX).

**Returns**:

Returns `0` on success, or a negative errno on failure.


## Synchronous Interface - Microphone Mute

### media_policy_set_mic_mute

```c
int media_policy_set_mic_mute(int mute);
```

Mute the microphone.

**Parameters**:

- `mute` Microphone mute mode: 1 to unmute, 0 to mute.

**Returns**:

Returns `0` on success, or a negative errno on failure.


## Synchronous Interface - Generic Parameter Read/Write

### media_policy_set_int

```c
int media_policy_set_int(const char* name, int value, int apply);
```

Set a numerical value for a policy criterion.

**Parameters**:

- `name` Criterion name.
- `value` Numerical value.
- `apply` Whether to apply the change to the policy.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_get_int

```c
int media_policy_get_int(const char* name, int* value);
```

Get the numerical value of a policy criterion.

**Parameters**:

- `name` Criterion name.
- `value` Numerical value.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_get_range

```c
int media_policy_get_range(const char* name, int* min_value, int* max_value);
```

Get the numerical value range of a policy criterion.

**Parameters**:

- `name` Criterion name.
- `min_value` Minimum value.
- `max_value` Maximum value.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_set_string

```c
int media_policy_set_string(const char* name, const char* value, int apply);
```

Set a literal value for a policy criterion.

**Parameters**:

- `name` Criterion name.
- `value` String value.
- `apply` Whether to apply the change to the policy.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_get_string

```c
int media_policy_get_string(const char* name, char* value, int len);
```

Get the literal value of a policy criterion.

**Parameters**:

- `name` Criterion name.
- `value` Buffer address.
- `len` Buffer length.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_include

```c
int media_policy_include(const char* name, const char* values, int apply);
```

Add literal values to an inclusive criterion.

**Parameters**:

- `name` Criterion name.
- `values` String values.
- `apply` Whether to apply the change to the policy.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_exclude

```c
int media_policy_exclude(const char* name, const char* values, int apply);
```

Remove literal values from an inclusive criterion.

**Parameters**:

- `name` Criterion name.
- `values` String values.
- `apply` Whether to apply the change to the policy.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_contain

```c
int media_policy_contain(const char* name, const char* values, int* result);
```

Check whether literal values are included in an InclusiveCriterion.

**Parameters**:

- `name` Criterion name.
- `values` String values array.
- `result` Whether the values are contained.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_increase

```c
int media_policy_increase(const char* name, int apply);
```

Increment the numerical criterion value by 1.

**Parameters**:

- `name` Criterion name.
- `apply` Whether to apply the change to the policy.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_policy_decrease

```c
int media_policy_decrease(const char* name, int apply);
```

Decrement the numerical criterion value by 1.

**Parameters**:

- `name` Criterion name.
- `apply` Whether to apply the change to the policy.

**Returns**:

Returns 0 on success, or a negative error code on failure.


## Synchronous Interface - Event Subscription

### media_policy_subscribe

```c
void* media_policy_subscribe(const char* name, media_policy_change_callback on_change, void* cookie);
```

Subscribe to policy criterion changes.

**Parameters**:

- `name` Criterion name.
- `on_change` Callback triggered when the criterion value changes.
- `cookie` User data passed to the callback.

**Returns**:

Returns a valid handle on success, or `NULL` on failure.


### media_policy_unsubscribe

```c
int media_policy_unsubscribe(void* handle);
```

Unsubscribe from policy criterion changes.

**Parameters**:

- `handle` Handle used to cancel the subscription.

**Returns**:

Returns `0` on success, or a negative errno on failure.


## Asynchronous Interface (libuv-based)

The following interfaces are only available when `CONFIG_LIBUV` is enabled.

### media_uv_policy_set_int

```c
int media_uv_policy_set_int(void* loop, const char* name, int value, int apply, media_uv_callback cb, void* cookie);
```

Set a numerical value for a policy criterion.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `name` Criterion name.
- `value` Numerical value to set.
- `apply` Whether to apply the new value to the policy configuration.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_policy_get_int

```c
int media_uv_policy_get_int(void* loop, const char* name, media_uv_int_callback cb, void* cookie);
```

Get the numerical value of a policy criterion.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `name` Criterion name.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_policy_increase

```c
int media_uv_policy_increase(void* loop, const char* name, int apply, media_uv_callback cb, void* cookie);
```

Increment the numerical value of a policy criterion by one.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `name` Criterion name.
- `apply` Whether to apply the new value to the policy configuration.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_policy_set_string

```c
int media_uv_policy_set_string(void* loop, const char* name, const char* value, int apply, media_uv_callback cb, void* cookie);
```

Set a literal value for a policy criterion.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `name` Criterion name.
- `value` String value to set.
- `apply` Whether to apply the new value to the policy configuration.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_policy_get_string

```c
int media_uv_policy_get_string(void* loop, const char* name, media_uv_string_callback cb, void* cookie);
```

Get the literal value of a policy criterion.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `name` Criterion name.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_policy_decrease

```c
int media_uv_policy_decrease(void* loop, const char* name, int apply, media_uv_callback cb, void* cookie);
```

Decrement the numerical value of a policy criterion by one.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `name` Criterion name.
- `apply` Whether to apply the new value to the policy configuration.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_policy_include

```c
int media_uv_policy_include(void* loop, const char* name, const char* value, int apply, media_uv_callback cb, void* cookie);
```

Add literal values to an inclusive criterion.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `name` Criterion name.
- `value` String values array.
- `apply` Whether to apply the new value to the policy configuration.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_policy_exclude

```c
int media_uv_policy_exclude(void* loop, const char* name, const char* value, int apply, media_uv_callback cb, void* cookie);
```

Remove literal values from an inclusive criterion.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `name` Criterion name.
- `value` String values array.
- `apply` Whether to apply the new value to the policy configuration.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_policy_contain

```c
int media_uv_policy_contain(void* loop, const char* name, const char* value, media_uv_int_callback cb, void* cookie);
```

Check whether literal values are included in an InclusiveCriterion.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `name` Criterion name.
- `value` String values array.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_policy_set_stream_volume

```c
int media_uv_policy_set_stream_volume(void* loop, const char* stream, int volume, media_uv_callback cb, void* cookie);
```

Set the volume of a stream type.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `stream` Stream type constant.
- `volume` Volume level to set.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_get_stream_volume

```c
int media_uv_policy_get_stream_volume(void* loop, const char* stream, media_uv_int_callback cb, void* cookie);
```

Get the volume of a stream type.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `stream` Stream type constant.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_increase_stream_volume

```c
int media_uv_policy_increase_stream_volume(void* loop, const char* stream, media_uv_callback cb, void* cookie);
```

Increase the volume of a stream type by one level.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `stream` Stream type constant.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_decrease_stream_volume

```c
int media_uv_policy_decrease_stream_volume(void* loop, const char* stream, media_uv_callback cb, void* cookie);
```

Decrease the volume of a stream type by one level.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `stream` Stream type constant.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_set_audio_mode

```c
int media_uv_policy_set_audio_mode(void* loop, const char* mode, media_uv_callback cb, void* cookie);
```

Set the audio mode (e.g., call mode, normal mode).

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `mode` New audio mode.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_get_audio_mode

```c
int media_uv_policy_get_audio_mode(void* loop, media_uv_string_callback cb, void* cookie);
```

Get the current audio mode.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_set_devices_use

```c
int media_uv_policy_set_devices_use(void* loop, const char* devices, bool use, media_uv_callback cb, void* cookie);
```

Force use or unuse devices (or protocols).

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `devices` Target devices.
- `use` Set devices to used or unused state.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_get_devices_use

```c
int media_uv_policy_get_devices_use(void* loop, media_uv_string_callback cb, void* cookie);
```

Get the currently forced-use devices.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_is_devices_use

```c
int media_uv_policy_is_devices_use(void* loop, const char* devices, media_uv_int_callback cb, void* cookie);
```

Check whether devices are being force-used.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `devices` Devices to check.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_set_hfp_samplerate

```c
int media_uv_policy_set_hfp_samplerate(void* loop, int rate, media_uv_callback cb, void* cookie);
```

Set the HFP (Hands-Free Profile) sampling rate.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `rate` Sample rate: 8000 for CVSD encoding, 16000 for mSBC encoding.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.

**Note**:

- This API is deprecated. The `rate` parameter will be changed to `int` type in the future.


### media_uv_policy_set_devices_available

```c
int media_uv_policy_set_devices_available(void* loop, const char* devices, bool available, media_uv_callback cb, void* cookie);
```

Set devices as available or unavailable.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `devices` Target devices.
- `available` Set devices to available or unavailable state.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_policy_get_devices_available

```c
int media_uv_policy_get_devices_available(void* loop, media_uv_string_callback cb, void* cookie);
```

Get the currently available devices.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_is_devices_available

```c
int media_uv_policy_is_devices_available(void* loop, const char* devices, media_uv_int_callback cb, void* cookie);
```

Check whether devices are available.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `devices` Devices to check.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_set_mute_mode

```c
int media_uv_policy_set_mute_mode(void* loop, int mute, media_uv_callback cb, void* cookie);
```

Set the mute mode.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `mute` New mute mode.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_get_mute_mode

```c
int media_uv_policy_get_mute_mode(void* loop, media_uv_int_callback cb, void* cookie);
```

Get the current mute mode.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_policy_set_mic_mute

```c
int media_uv_policy_set_mic_mute(void* loop, int mute, media_uv_callback cb, void* cookie);
```

Mute the built-in microphone or Bluetooth microphone.

**Parameters**:

- `loop` `uv_loop_t*` event loop handle for the current thread.
- `mute` Mute mode.
- `cb` Result callback function.
- `cookie` Callback user data.

**Returns**:

Returns `0` on success, or a negative errno on failure.
