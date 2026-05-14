\[ [English](../../../../en/api/framework/bluetooth/bt_cs.md) | 简体中文 \]

# 蓝牙 Channel Sounding API

openvela 蓝牙 Channel Sounding（CS）接口，用于蓝牙设备间的距离测量和定位功能。CS 基于蓝牙 5.4 规范引入的信道探测技术，支持厘米级精度的测距。

头文件：`#include <bt_cs.h>`

## openvela 实现说明

- **测距方法**：支持自动选择（AUTO）、RSSI 和 CS 三种测距方法
- **角色模型**：支持发起方（Initiator）和反射方（Reflector）两种角色
- **RAS 特性**：支持实时测距数据、丢失数据段恢复、中止操作和数据过滤
- **回调通知**：通过回调函数异步返回测距启动、停止和结果事件
- **配置依赖**：测试接口需启用 `CONFIG_BT_CS_RAS_TEST`

## 回调管理

### bt_cs_register_callbacks

```c
void* bt_cs_register_callbacks(bt_instance_t* ins, const cs_callbacks_t* callbacks);
```

注册 CS 事件回调函数。注册成功后，当距离测量启动、停止或产生结果时，系统会通过回调函数通知应用。

**参数**：

- `ins` 蓝牙客户端实例。
- `callbacks` CS 事件回调函数集合，参见 `cs_callbacks_t`。

**返回值**：

成功时返回回调 cookie（非 NULL），用于后续注销；失败时返回 NULL。

### bt_cs_unregister_callbacks

```c
bool bt_cs_unregister_callbacks(bt_instance_t* ins, void* cookie);
```

注销已注册的 CS 事件回调函数。

**参数**：

- `ins` 蓝牙客户端实例。
- `cookie` 注册回调时返回的 cookie。

**返回值**：

成功时返回 `true`，失败时返回 `false`。

## 距离测量

### bt_cs_start_distance_measurement

```c
bt_status_t bt_cs_start_distance_measurement(bt_instance_t* ins, const bt_distance_measurement_params_t* params);
```

启动距离测量。调用前需先通过 `bt_cs_register_callbacks` 注册回调函数，测量结果将通过 `cs_distance_measure_result_cb` 回调返回。

**参数**：

- `ins` 蓝牙客户端实例。
- `params` 距离测量参数，参见 `bt_distance_measurement_params_t`。

**返回值**：

成功时返回 `BT_STATUS_SUCCESS`，失败时返回错误码。

### bt_cs_stop_distance_measurement

```c
bt_status_t bt_cs_stop_distance_measurement(bt_instance_t* ins, bt_address_t* addr, uint8_t method, bool timeout);
```

停止距离测量。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远端设备地址。
- `method` 测距方法（AUTO/RSSI/CS）。
- `timeout` 是否因超时而停止。

**返回值**：

成功时返回 `BT_STATUS_SUCCESS`，失败时返回错误码。

## 能力查询

### bt_get_cs_max_supported_security_level

```c
bt_status_t bt_get_cs_max_supported_security_level(bt_instance_t* ins, bt_address_t* addr);
```

获取远端设备支持的最大 CS 安全等级。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远端设备地址。

**返回值**：

成功时返回 `BT_STATUS_SUCCESS`，失败时返回错误码。

## 配置管理

### bt_cs_set_config

```c
bt_status_t bt_cs_set_config(bt_instance_t* ins, bt_address_t* addr, const bt_cs_set_params_t* params);
```

设置 CS 配置参数，包括 RAS 特性、角色、天线选择和最大发射功率。

**参数**：

- `ins` 蓝牙客户端实例。
- `addr` 远端设备地址。
- `params` CS 配置参数，参见 `bt_cs_set_params_t`。

**返回值**：

成功时返回 `BT_STATUS_SUCCESS`，失败时返回错误码。

## 数据结构

### bt_distance_measurement_params_t

距离测量参数结构体。

| 字段                 | 类型           | 说明                             |
| -------------------- | -------------- | -------------------------------- |
| `addr`               | `bt_address_t` | 远端设备地址                     |
| `method`             | `uint8_t`      | 测距方法（0=AUTO, 1=RSSI, 2=CS） |
| `role`               | `uint8_t`      | 角色（发起方/反射方）            |
| `interval_ms`        | `uint16_t`     | 测量间隔（毫秒）                 |
| `duration_ms`        | `uint16_t`     | 测量持续时间（毫秒）             |
| `submode`            | `uint8_t`      | CS 子模式                        |
| `max_steps`          | `uint8_t`      | 最大步数                         |
| `mode0_steps`        | `uint8_t`      | Mode 0 步数                      |
| `rtt_type`           | `uint8_t`      | RTT 类型                         |
| `sync_phy`           | `uint8_t`      | 同步 PHY                         |
| `channel_map`        | `uint8_t`      | 信道映射                         |
| `antenna_paths_mask` | `uint8_t`      | 天线路径掩码                     |
| `vendor_specific`    | `uint8_t`      | 厂商自定义参数                   |
| `debug_flags`        | `uint8_t`      | 调试标志                         |

### bt_distance_measurement_result_t

距离测量结果结构体。

| 字段                        | 类型      | 说明                   |
| --------------------------- | --------- | ---------------------- |
| `centimeter`                | `uint8_t` | 距离（厘米）           |
| `error_centimeter`          | `uint8_t` | 距离误差（厘米）       |
| `azimuth_angle`             | `uint8_t` | 方位角                 |
| `error_azimuthAngle`        | `uint8_t` | 方位角误差             |
| `altitude_angle`            | `uint8_t` | 仰角                   |
| `error_altitudeAngle`       | `uint8_t` | 仰角误差               |
| `elapsed_realtime_nanos`    | `long`    | 经过的实时时间（纳秒） |
| `confidence_level`          | `uint8_t` | 置信度                 |
| `delay_spread_meters`       | `double`  | 延迟扩展（米）         |
| `detected_attack_level`     | `uint8_t` | 检测到的攻击等级       |
| `velocity_meters_persecond` | `double`  | 速度（米/秒）          |
| `method`                    | `uint8_t` | 使用的测距方法         |

### bt_cs_set_params_t

CS 配置参数结构体。

| 字段                        | 类型       | 说明                                      |
| --------------------------- | ---------- | ----------------------------------------- |
| `ras_feature`               | `uint32_t` | RAS 特性位（见下方宏定义）                |
| `role`                      | `uint8_t`  | CS 角色位（Bit 0: 发起方, Bit 1: 反射方） |
| `cs_sync_antenna_selection` | `uint8_t`  | CS_SYNC 天线选择                          |
| `max_tx_power`              | `int8_t`   | 最大发射功率（dBm，范围 -127 到 20）      |

### cs_callbacks_t

CS 事件回调函数集合。

| 字段                             | 类型     | 说明             |
| -------------------------------- | -------- | ---------------- |
| `size`                           | `size_t` | 结构体大小       |
| `cs_distance_measure_started_cb` | 函数指针 | 距离测量启动回调 |
| `cs_distance_measure_stopped_cb` | 函数指针 | 距离测量停止回调 |
| `cs_distance_measure_result_cb`  | 函数指针 | 距离测量结果回调 |

## 宏定义

### RAS 特性位

| 宏                                      | 值   | 说明                 |
| --------------------------------------- | ---- | -------------------- |
| `BT_CS_RAS_REAL_TIME_RANGING_DATA`      | 0x01 | 实时测距数据         |
| `BT_CS_RAS_RETRIEVE_LOST_DATA_SEGMENTS` | 0x02 | 恢复丢失的测距数据段 |
| `BT_CS_RAS_ABORT_OPERATION`             | 0x04 | 中止操作             |
| `BT_CS_RAS_FILTER_RANGING_DATA`         | 0x08 | 过滤测距数据         |

### 天线选择

| 宏                                 | 值   | 说明                   |
| ---------------------------------- | ---- | ---------------------- |
| `BT_CS_ANTENNA_SEL_1`              | 0x01 | 使用天线 1             |
| `BT_CS_ANTENNA_SEL_2`              | 0x02 | 使用天线 2             |
| `BT_CS_ANTENNA_SEL_3`              | 0x03 | 使用天线 3             |
| `BT_CS_ANTENNA_SEL_4`              | 0x04 | 使用天线 4             |
| `BT_CS_ANTENNA_SEL_SINGLE_REPEATE` | 0xFD | 天线标识符单次重复顺序 |
| `BT_CS_ANTENNA_SEL_DOUBLE_REPEATE` | 0xFE | 天线标识符双次重复顺序 |
| `BT_CS_ANTENNA_SEL_NO_RECOMMEND`   | 0xFF | 主机无推荐             |

**openvela 扩展接口。**
