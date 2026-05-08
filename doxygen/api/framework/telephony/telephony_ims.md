# IMS 服务 API

IP 多媒体子系统（VoLTE/VoWiFi）管理。

头文件：`#include <tapi_ims.h>`

## openvela 实现说明

- **IMS 开关**：通过 `turn_on` / `turn_off` 控制 IMS 服务的启用状态
- **注册状态**：查询 IMS 是否已注册到网络，订阅注册状态变化事件
- **业务开关**：`set_service_status` 控制具体业务（如语音、视频）的启用
- **VoLTE 支持**：通过 `is_volte_available` 查询当前网络是否支持 VoLTE
- **多卡支持**：所有接口带 `slot_id`

## IMS 开关

### tapi_ims_turn_on

```c
int tapi_ims_turn_on(tapi_context context, int slot_id);
```

开启 IMS 服务（VoLTE/VoWiFi）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_ims_turn_off

```c
int tapi_ims_turn_off(tapi_context context, int slot_id);
```

关闭 IMS 服务。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 服务状态配置

### tapi_ims_set_service_status

```c
int tapi_ims_set_service_status(tapi_context context, int slot_id, int capability);
```

开启 IMS 服务（VoLTE/VoWiFi）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `capability` 能力值。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## 注册状态与事件

### tapi_ims_get_registration

```c
int tapi_ims_get_registration(tapi_context context, int slot_id, tapi_ims_registration_info* ims_reg);
```

开启 IMS 服务（VoLTE/VoWiFi）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `ims_reg` IMS 注册状态。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_ims_register_registration_change

```c
int tapi_ims_register_registration_change(tapi_context context, int slot_id, void* user_obj, tapi_async_function p_handle);
```

开启 IMS 服务（VoLTE/VoWiFi）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `user_obj` 用户对象指针。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_ims_is_registered

```c
int tapi_ims_is_registered(tapi_context context, int slot_id, bool* out);
```

开启 IMS 服务（VoLTE/VoWiFi）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



## VoLTE 与业务查询

### tapi_ims_is_volte_available

```c
int tapi_ims_is_volte_available(tapi_context context, int slot_id, bool* out);
```

开启 IMS 服务（VoLTE/VoWiFi）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_ims_get_subscriber_uri_number

```c
int tapi_ims_get_subscriber_uri_number(tapi_context context, int slot_id, char** out);
```

开启 IMS 服务（VoLTE/VoWiFi）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。



### tapi_ims_get_enabled

```c
int tapi_ims_get_enabled(tapi_context context, int slot_id, bool* out);
```

查询 IMS 是否启用。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID（0 或 1）。
- `out` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

