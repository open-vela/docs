# ims 命令

\[ [English](../../../../../en/device_dev_guide/connection/telephony/telephonytool/ims.md) | 简体中文 \]

## 一、概述

 在 openvela 的 NSH 命令行中，可以通过 `telephonytool` 命令工具进入 Console，执行所有与 IMS（IP Multimedia Subsystem）相关的操作。

## 二、前提条件

 打开 `telephonytool`，执行如下命令：

```Bash
ap> telephonytool
```

## 三、命令

### 1、enable-ims

#### 命令说明

 `enable-ims` 命令用于开启或关闭 IMS（IP Multimedia Subsystem）能力。

#### 命令格式

```Bash
enable-ims [slot_id][action]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。
- action：
    - `0`：关闭 IMS 能力。
    - `1`：开启 IMS 能力。

#### 示例

##### 命令输入

```Bash
telephonytool>enable-ims 0 1
```

##### 输出信息

```Bash
telephonytool> enable-ims 0 1
[149517.760100] [35] [ DEBUG] [ap] telephonytool_cmd_ims_enable: slot_id: 0, action: 1
telephonytool> [149517.786400] [21] [  INFO] [ap] [0,0124]> RIL_REQUEST_IMS_REG_STATE_CHANGE (1)
[149518.064500] [25] [  INFO] [ap] [AT_NETWORK] Receive signal strength URC
```

### 2、get-ims-enabled

#### 命令说明

 `get-ims-enabled` 命令用于获取 IMS（IP Multimedia Subsystem）开关的当前状态。

#### 命令格式

```Bash
get-ims-enabled [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

####  示例

#####  命令输入

```Bash
telephonytool>get-ims-enabled 0
```

#####  输出信息

```Bash
telephonytool> get-ims-enabled 0
[149542.284600] [35] [ DEBUG] [ap] telephonytool_cmd_get_ims_enabled: slot_id: 0, ims enable: 1
```

###  3、set-ims-cap

####  命令说明

 `set-ims-cap` 命令用于设置支持 IMS（IP Multimedia Subsystem）的业务功能。

####  命令格式

```Bash
set-ims-cap [slot_id][cap-value]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。
- cap-value：IMS 支持的功能类型：
    - `1`：语音（voice）。
    - `4`：短信（SMS）。
    - `5`：语音和短信（voice & SMS）。

#### 示例

##### 命令输入

```Bash
telephonytool> set-ims-cap 0 1
```

##### 输出信息

```Bash
set-ims-cap 0 1
[149558.379600] [35] [ DEBUG] [ap] telephonytool_cmd_set_ims_service: slot_id: 0, action: 1
telephonytool> [149558.409700] [21] [  INFO] [ap] [0,0127]> RIL_REQUEST_IMS_SET_SERVICE_STATUS
[149558.412900] [15] [  INFO] [ap] [AT_RIL] onRequest: 503<->IMS_SET_SERVICE_STATUS, reqtype: 6
[149558.414800] [21] [  INFO] [ap] [0,0127]< RIL_REQUEST_IMS_SET_SERVICE_STATUS
[149558.417100] [21] [  INFO] [ap] [0,0128]> RIL_REQUEST_IMS_REGISTRATION_STATE
[149558.421400] [15] [  INFO] [ap] [AT_RIL] onRequest: 502<->IMS_REGISTRATION_STATE, reqtype: 6
[149558.424600] [21] [  INFO] [ap] [0,0128]< RIL_REQUEST_IMS_REGISTRATION_STATE
[149558.425000] [21] [  INFO] [ap] ril_registration_status_cb reg_info:1, ext_info:1
[149558.425400] [21] [  INFO] [ap] /ril_0 reg_info:1 ext_info:1
```

### 4、listen-ims

#### 命令说明

`listen-ims` 命令用于监听指定卡槽的 IMS（IP Multimedia Subsystem）注册状态，包含信号强度和网络状态变化等信息。

#### 命令格式

```Bash
listen-ims [slot_id]
```

- slot_id：监听的卡槽 ID，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>listen-ims 0
```

##### 输出信息

```Bash
telephonytool> listen-ims 0
[149573.889900] [35] [ DEBUG] [ap] telephonytool_cmd_ims_register: slot_id: 0, watch_id: 100
telephonytool>
telephonytool>
telephonytool> get-ims-enabled 0[149578.065500] [25] [  INFO] [ap] [AT_NETWORK] Receive signal strength URC
[149578.068000] [21] [  INFO] [ap] [0,UNSOL]< UNSOL_SIGNAL_STRENGTH {gw: 99, cdma: -1, evdo: -1, lte: 99 59 2147483647 2147483647 2147483647}
```

### 5、get-ims-registration

#### 命令说明

`get-ims-registration` 命令用于查询 IMS（IP Multimedia Subsystem）相关信息，包括 IMS 注册状态和 VoLTE（Voice over LTE）状态。

#### 命令格式

```Bash
get-ims-registration [slot_id][action]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。
- action：
    - `0`：表示查询 IMS 信息（IMS info）。
    - `1`：表示查询 IMS 注册状态（IMS state）。
    - `2`：表示查询 VoLTE 状态（VoLTE state）。

#### 示例

##### 命令输入

```Bash
telephonytool>get-ims-registration 0 0
```

##### 输出信息

```Bash
telephonytool> get-ims-registration 0 0
[149616.226900] [35] [ DEBUG] [ap] telephonytool_cmd_ims_get_registration: slot_id: 0, acton: 0
[149616.229700] [35] [ DEBUG] [ap] telephonytool_cmd_ims_get_registration: ret_info: 0, ext_info: 0
```
