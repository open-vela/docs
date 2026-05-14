\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/bt_cs.md) \]

# Bluetooth Channel Sounding API

The openvela Bluetooth Channel Sounding (CS) interface provides distance measurement and positioning capabilities between Bluetooth devices. Based on the channel sounding technology introduced in the Bluetooth 5.4 specification, it supports centimeter-level ranging accuracy.

Header file: `#include <bt_cs.h>`

## openvela Implementation Notes

- **Ranging methods**: Supports automatic selection (AUTO), RSSI, and CS ranging methods
- **Role model**: Supports Initiator and Reflector roles
- **RAS features**: Supports real-time ranging data, lost data segment retrieval, abort operation, and data filtering
- **Callback notifications**: Ranging start, stop, and result events are delivered asynchronously via callbacks
- **Configuration dependency**: Test interface requires `CONFIG_BT_CS_RAS_TEST`

## Callback Management

### bt_cs_register_callbacks

```c
void* bt_cs_register_callbacks(bt_instance_t* ins, const cs_callbacks_t* callbacks);
```

Register CS event callback functions. After successful registration, the system notifies the application via callbacks when distance measurement starts, stops, or produces results.

**Parameters**:

- `ins` Bluetooth client instance.
- `callbacks` CS event callback function set, see `cs_callbacks_t`.

**Returns**:

On success, returns a callback cookie (non-NULL) for later unregistration; on failure, returns NULL.

### bt_cs_unregister_callbacks

```c
bool bt_cs_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

Unregister previously registered CS event callback functions.

**Parameters**:

- `ins` Bluetooth client instance.
- `cookie` Cookie returned during callback registration.

**Returns**:

Returns `true` on success, `false` on failure.

## Distance Measurement

### bt_cs_start_distance_measurement

```c
bt_status_t bt_cs_start_distance_measurement(bt_instance_t* ins, const bt_distance_measurement_params_t* params);
```

Start distance measurement. Callbacks must be registered via `bt_cs_register_callbacks` before calling this function. Measurement results are delivered through the `cs_distance_measure_result_cb` callback.

**Parameters**:

- `ins` Bluetooth client instance.
- `params` Distance measurement parameters, see `bt_distance_measurement_params_t`.

**Returns**:

Returns `BT_STATUS_SUCCESS` on success, or an error code on failure.

### bt_cs_stop_distance_measurement

```c
bt_status_t bt_cs_stop_distance_measurement(bt_instance_t* ins, bt_address_t* addr, uint8_t method, bool timeout);
```

Stop distance measurement.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Remote device address.
- `method` Ranging method (AUTO/RSSI/CS).
- `timeout` Whether stopping due to timeout.

**Returns**:

Returns `BT_STATUS_SUCCESS` on success, or an error code on failure.

## Capability Query

### bt_get_cs_max_supported_security_level

```c
bt_status_t bt_get_cs_max_supported_security_level(bt_instance_t* ins, bt_address_t* addr);
```

Get the maximum CS security level supported by the remote device.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Remote device address.

**Returns**:

Returns `BT_STATUS_SUCCESS` on success, or an error code on failure.

## Configuration Management

### bt_cs_set_config

```c
bt_status_t bt_cs_set_config(bt_instance_t* ins, bt_address_t* addr, const bt_cs_set_params_t* params);
```

Set CS configuration parameters, including RAS features, role, antenna selection, and maximum transmit power.

**Parameters**:

- `ins` Bluetooth client instance.
- `addr` Remote device address.
- `params` CS configuration parameters, see `bt_cs_set_params_t`.

**Returns**:

Returns `BT_STATUS_SUCCESS` on success, or an error code on failure.

## Data Structures

### bt_distance_measurement_params_t

Distance measurement parameters structure.

| Field                | Type           | Description                           |
| -------------------- | -------------- | ------------------------------------- |
| `addr`               | `bt_address_t` | Remote device address                 |
| `method`             | `uint8_t`      | Ranging method (0=AUTO, 1=RSSI, 2=CS) |
| `role`               | `uint8_t`      | Role (initiator/reflector)            |
| `interval_ms`        | `uint16_t`     | Measurement interval (milliseconds)   |
| `duration_ms`        | `uint16_t`     | Measurement duration (milliseconds)   |
| `submode`            | `uint8_t`      | CS submode                            |
| `max_steps`          | `uint8_t`      | Maximum steps                         |
| `mode0_steps`        | `uint8_t`      | Mode 0 steps                          |
| `rtt_type`           | `uint8_t`      | RTT type                              |
| `sync_phy`           | `uint8_t`      | Sync PHY                              |
| `channel_map`        | `uint8_t`      | Channel map                           |
| `antenna_paths_mask` | `uint8_t`      | Antenna paths mask                    |
| `vendor_specific`    | `uint8_t`      | Vendor-specific parameter             |
| `debug_flags`        | `uint8_t`      | Debug flags                           |

### bt_distance_measurement_result_t

Distance measurement result structure.

| Field                       | Type      | Description                    |
| --------------------------- | --------- | ------------------------------ |
| `centimeter`                | `uint8_t` | Distance (centimeters)         |
| `error_centimeter`          | `uint8_t` | Distance error (centimeters)   |
| `azimuth_angle`             | `uint8_t` | Azimuth angle                  |
| `error_azimuthAngle`        | `uint8_t` | Azimuth angle error            |
| `altitude_angle`            | `uint8_t` | Altitude angle                 |
| `error_altitudeAngle`       | `uint8_t` | Altitude angle error           |
| `elapsed_realtime_nanos`    | `long`    | Elapsed realtime (nanoseconds) |
| `confidence_level`          | `uint8_t` | Confidence level               |
| `delay_spread_meters`       | `double`  | Delay spread (meters)          |
| `detected_attack_level`     | `uint8_t` | Detected attack level          |
| `velocity_meters_persecond` | `double`  | Velocity (meters/second)       |
| `method`                    | `uint8_t` | Ranging method used            |

### bt_cs_set_params_t

CS configuration parameters structure.

| Field                       | Type       | Description                                       |
| --------------------------- | ---------- | ------------------------------------------------- |
| `ras_feature`               | `uint32_t` | RAS feature bits (see macro definitions below)    |
| `role`                      | `uint8_t`  | CS role bits (Bit 0: initiator, Bit 1: reflector) |
| `cs_sync_antenna_selection` | `uint8_t`  | CS_SYNC antenna selection                         |
| `max_tx_power`              | `int8_t`   | Maximum TX power (dBm, range -127 to 20)          |

### cs_callbacks_t

CS event callback function set.

| Field                            | Type             | Description                           |
| -------------------------------- | ---------------- | ------------------------------------- |
| `size`                           | `size_t`         | Structure size                        |
| `cs_distance_measure_started_cb` | Function pointer | Distance measurement started callback |
| `cs_distance_measure_stopped_cb` | Function pointer | Distance measurement stopped callback |
| `cs_distance_measure_result_cb`  | Function pointer | Distance measurement result callback  |

## Macro Definitions

### RAS Feature Bits

| Macro                                   | Value | Description                         |
| --------------------------------------- | ----- | ----------------------------------- |
| `BT_CS_RAS_REAL_TIME_RANGING_DATA`      | 0x01  | Real-time ranging data              |
| `BT_CS_RAS_RETRIEVE_LOST_DATA_SEGMENTS` | 0x02  | Retrieve lost ranging data segments |
| `BT_CS_RAS_ABORT_OPERATION`             | 0x04  | Abort operation                     |
| `BT_CS_RAS_FILTER_RANGING_DATA`         | 0x08  | Filter ranging data                 |

### Antenna Selection

| Macro                              | Value | Description                                    |
| ---------------------------------- | ----- | ---------------------------------------------- |
| `BT_CS_ANTENNA_SEL_1`              | 0x01  | Use antenna identifier 1                       |
| `BT_CS_ANTENNA_SEL_2`              | 0x02  | Use antenna identifier 2                       |
| `BT_CS_ANTENNA_SEL_3`              | 0x03  | Use antenna identifier 3                       |
| `BT_CS_ANTENNA_SEL_4`              | 0x04  | Use antenna identifier 4                       |
| `BT_CS_ANTENNA_SEL_SINGLE_REPEATE` | 0xFD  | Antenna identifiers in single repetitive order |
| `BT_CS_ANTENNA_SEL_DOUBLE_REPEATE` | 0xFE  | Antenna identifiers in double repetitive order |
| `BT_CS_ANTENNA_SEL_NO_RECOMMEND`   | 0xFF  | Host has no recommendation                     |

**openvela extension interface.**
