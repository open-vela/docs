# Telephony Phone Service API

简化版电话服务接口，面向轻量客户端使用。相较于 `tapi_call`，该模块封装更紧凑的通话控制能力，并整合音频类型控制、无线电开关和 WTP（Wireless Telephony Profile）配套接口。

头文件：`#include <tapi_phone.h>`

## openvela 实现说明

- **客户端会话**：通过 `tapi_start_phone_service_client` 启动，`tapi_stop_phone_service_client` 停止
- **回调注册**：通过 `tapi_client_register_callbacks` 注册统一回调，监听通话事件
- **无需 tapi_context**：本接口在底层自管理与服务端的连接，调用方不需要持有 `tapi_context`
- **WTP 支持**：封装蓝牙配对手表/设备的 WTP（Wireless Telephony Profile）适配能力
- **适用场景**：嵌入式可穿戴设备、简单通话客户端

## 服务生命周期

### tapi_start_phone_service_client

```c
int tapi_start_phone_service_client(const char* client_name);
```

启动电话服务客户端。

**参数**：

- `client_name` 客户端名称。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_stop_phone_service_client

```c
int tapi_stop_phone_service_client(void);
```

停止电话服务客户端。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_client_register_callbacks

```c
int tapi_client_register_callbacks(void* callbacks);
```

注册客户端回调集合。

**参数**：

- `callbacks` 回调函数集合指针。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_client_unregister_callbacks

```c
int tapi_client_unregister_callbacks(void);
```

取消客户端回调注册。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## 通话控制

### tapi_dial_call

```c
int tapi_dial_call(const char* number);
```

拨打电话。

**参数**：

- `number` 要拨打的号码字符串。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_answer_call

```c
int tapi_answer_call(void);
```

接听来电。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_reject_call

```c
int tapi_reject_call(void);
```

拒绝来电。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_hangup_call

```c
int tapi_hangup_call(void);
```

挂断当前通话。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_hold_call

```c
int tapi_hold_call(void);
```

保持当前通话。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_hold_and_answer_call

```c
int tapi_hold_and_answer_call(void);
```

保持当前通话并接听新来电。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_release_and_answer_call

```c
int tapi_release_and_answer_call(void);
```

释放当前通话并接听新来电。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_merge_call

```c
int tapi_merge_call(void);
```

合并多个通话形成会议通话。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_send_tones

```c
int tapi_send_tones(const char* tones);
```

发送 DTMF 音序列。

**参数**：

- `tones` DTMF 字符串（`0-9 * # A-D`）。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## 音频与射频控制

### tapi_client_set_audio_type

```c
int tapi_client_set_audio_type(int type);
```

设置通话期间使用的音频类型。

**参数**：

- `type` 音频类型枚举值。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_client_set_radio_power

```c
int tapi_client_set_radio_power(bool enabled);
```

简化版射频功率开关。

**参数**：

- `enabled` `true` 开启射频，`false` 关闭。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## WTP（无线电话配置文件）

### tapi_client_wtp_register_cb

```c
int tapi_client_wtp_register_cb(void* callbacks);
```

注册 WTP 事件回调。

**参数**：

- `callbacks` WTP 回调集合指针。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_client_wtp_unregister_cb

```c
int tapi_client_wtp_unregister_cb(void);
```

取消 WTP 事件回调注册。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_wtp_set_local_info

```c
int tapi_wtp_set_local_info(const char* info);
```

设置 WTP 本地信息（设备标识、能力等）。

**参数**：

- `info` 本地信息字符串。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_wtp_modify_discovery

```c
int tapi_wtp_modify_discovery(int mode);
```

修改 WTP 发现模式。

**参数**：

- `mode` 发现模式枚举值。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_wtp_modify_visibility

```c
int tapi_wtp_modify_visibility(int visibility);
```

修改 WTP 可见性配置。

**参数**：

- `visibility` 可见性枚举值。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。
