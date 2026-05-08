# Telephony 公共工具 API

TAPI 提供的通用工具函数，涵盖状态字符串转换、modem 路径解析、运营商状态解析等辅助能力。

头文件：`#include <tapi.h>`

## openvela 实现说明

- **字符串↔枚举转换**：`*_from_string` / `*_to_string` 系列把 oFono D-Bus 字符串与 TAPI 枚举互转，便于状态解析
- **Modem 路径**：`tapi_utils_get_modem_path` 将 `slot_id` 转成 oFono 的 modem 对象路径
- **工具性质**：本组接口不依赖 tapi_context，可在任意位置直接调用
- **适用场景**：实现自定义事件处理、打印调试日志、或扩展 TAPI 能力时使用

## SIM 状态

### tapi_sim_state_to_string

```c
const char* tapi_sim_state_to_string(tapi_sim_state state);
```

将 SIM 状态枚举转为可读字符串。

**参数**：

- `state` SIM 状态枚举值。

**返回值**：

返回状态的字符串表示，失败时返回 `NULL` 或占位字符串。

## APN 工具

### tapi_utils_apn_auth_from_string

```c
int tapi_utils_apn_auth_from_string(const char* str);
```

将认证类型字符串转为 APN 认证枚举值。

**参数**：

- `str` 认证类型字符串（如 `"pap"`、`"chap"`）。

**返回值**：

返回认证枚举值；无效字符串时返回错误值。

### tapi_utils_apn_auth_to_string

```c
const char* tapi_utils_apn_auth_to_string(int auth);
```

将 APN 认证枚举值转为字符串。

**参数**：

- `auth` 认证枚举值。

**返回值**：

返回对应字符串。

### tapi_utils_apn_proto_from_string

```c
int tapi_utils_apn_proto_from_string(const char* str);
```

将协议字符串转为 APN 协议枚举值。

**参数**：

- `str` 协议字符串（如 `"ip"`、`"ipv6"`、`"dual"`）。

**返回值**：

返回协议枚举值。

### tapi_utils_apn_proto_to_string

```c
const char* tapi_utils_apn_proto_to_string(int proto);
```

将 APN 协议枚举值转为字符串。

**参数**：

- `proto` 协议枚举值。

**返回值**：

返回对应字符串。

### tapi_utils_apn_type_from_string

```c
int tapi_utils_apn_type_from_string(const char* str);
```

将 APN 类型字符串转为类型枚举值。

**参数**：

- `str` APN 类型字符串（如 `"default"`、`"mms"`、`"ims"`）。

**返回值**：

返回类型枚举值。

### tapi_utils_apn_type_to_string

```c
const char* tapi_utils_apn_type_to_string(int type);
```

将 APN 类型枚举值转为字符串。

**参数**：

- `type` APN 类型枚举值。

**返回值**：

返回对应字符串。

## 通话工具

### tapi_utils_call_disconnected_reason

```c
int tapi_utils_call_disconnected_reason(const char* reason);
```

将通话断开原因字符串转为 TAPI 断开原因枚举值。

**参数**：

- `reason` 断开原因字符串。

**返回值**：

返回断开原因枚举值。

### tapi_utils_call_status_from_string

```c
int tapi_utils_call_status_from_string(const char* status);
```

将通话状态字符串转为状态枚举值。

**参数**：

- `status` 状态字符串（如 `"active"`、`"held"`、`"dialing"`）。

**返回值**：

返回状态枚举值。

## 小区与网络工具

### tapi_utils_cell_type_from_string

```c
int tapi_utils_cell_type_from_string(const char* str);
```

将小区类型字符串转为枚举值。

**参数**：

- `str` 小区类型字符串。

**返回值**：

返回小区类型枚举值。

### tapi_utils_cell_type_to_string

```c
const char* tapi_utils_cell_type_to_string(int type);
```

将小区类型枚举值转为字符串。

**参数**：

- `type` 小区类型枚举值。

**返回值**：

返回对应字符串。

### tapi_utils_network_mode_from_string

```c
int tapi_utils_network_mode_from_string(const char* str);
```

将网络模式字符串转为枚举值。

**参数**：

- `str` 网络模式字符串（如 `"gsm"`、`"lte"`）。

**返回值**：

返回网络模式枚举值。

### tapi_utils_network_mode_to_string

```c
const char* tapi_utils_network_mode_to_string(int mode);
```

将网络模式枚举值转为字符串。

**参数**：

- `mode` 网络模式枚举值。

**返回值**：

返回对应字符串。

### tapi_utils_network_type_from_ril_tech

```c
int tapi_utils_network_type_from_ril_tech(int tech);
```

将 RIL 层传来的网络技术值转为 TAPI 网络类型枚举。

**参数**：

- `tech` RIL 网络技术值。

**返回值**：

返回 TAPI 网络类型枚举值。

### tapi_utils_network_operator_status_from_string

```c
int tapi_utils_network_operator_status_from_string(const char* str);
```

将运营商状态字符串转为枚举值。

**参数**：

- `str` 运营商状态字符串。

**返回值**：

返回运营商状态枚举值。

### tapi_utils_operator_status_from_string

```c
int tapi_utils_operator_status_from_string(const char* str);
```

`tapi_utils_network_operator_status_from_string` 的简写版本，等价功能。

**参数**：

- `str` 运营商状态字符串。

**返回值**：

返回运营商状态枚举值。

## 注册状态工具

### tapi_utils_registration_mode_from_string

```c
int tapi_utils_registration_mode_from_string(const char* str);
```

将注册模式字符串转为枚举值。

**参数**：

- `str` 注册模式字符串（如 `"auto"`、`"manual"`）。

**返回值**：

返回注册模式枚举值。

### tapi_utils_registration_status_from_string

```c
int tapi_utils_registration_status_from_string(const char* str);
```

将注册状态字符串转为枚举值。

**参数**：

- `str` 注册状态字符串。

**返回值**：

返回注册状态枚举值。

### tapi_utils_get_registration_status_string

```c
const char* tapi_utils_get_registration_status_string(int status);
```

将注册状态枚举值转为可读字符串。

**参数**：

- `status` 注册状态枚举值。

**返回值**：

返回对应字符串。

## Modem 路径与 Slot

### tapi_utils_get_modem_path

```c
const char* tapi_utils_get_modem_path(int slot_id);
```

根据 SIM 卡槽 ID 获取 oFono 的 modem 对象路径。

**参数**：

- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

返回 modem 对象路径字符串（如 `/ril_0`、`/ril_1`）。

### tapi_utils_get_slot_id

```c
int tapi_utils_get_slot_id(const char* path);
```

从 oFono modem 对象路径解析 SIM 卡槽 ID。

**参数**：

- `path` modem 对象路径。

**返回值**：

返回对应的卡槽 ID（0 或 1），无效路径时返回负值。
