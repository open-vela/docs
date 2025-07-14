# radio/modem 命令

\[ [English](../../../../../en/device_dev_guide/connection/telephony/telephonytool/radio_modem.md) | 简体中文 \]

## 一、概述

在 openvela 的 NSH 命令行中，可以通过进入 telephonytool 命令工具的 Console，来执行所有与调制解调器（modem）和无线电（radio）管理相关的操作。

## 二、前提条件

确保已打开 `telephonytool` 工具。

```Bash
ap> telephonytool
```

执行上述命令后，进入 `telephonytool` 控制台，准备执行相关操作。

## 三、命令

### 1、list-modem

#### 命令说明

列出所有可用的 modem。

#### 命令格式

```Bash
list-modem
```

#### 示例

##### 命令输入

```Bash
telephonytool> list-modem
```

##### 输出信息

```Bash
telephonytool> [ 1050.782500] [31] [ DEBUG] [ap] modem_list_query_complete :
[ 1050.782800] [31] [ DEBUG] [ap] result->status : 0
[ 1050.783000] [31] [ DEBUG] [ap] modem found with path -> /ril_0
```

### 2、listen-modem

#### 命令说明

设置监听特定的 modem 事件。

#### 命令格式

```Bash
listen-modem [slot_id] [event_id]
```

- slot_id：设置要监听的 slot，目前仅支持 `0`。
- event_id：要监听的事件 ID。

#### 支持的事件 ID 列表

`event_id` 用于指定要监听的事件。以下是支持的事件分类及其对应的事件 ID。

1. 通用事件 (Generic Indication Message)

    - `MSG_RADIO_STATE_CHANGE_IND` = 0
    - `MSG_PHONE_STATE_CHANGE_IND`
    - `MSG_OEM_HOOK_RAW_IND`
    - `MSG_MODEM_RESTART_IND`
    - `MSG_DEVICE_INFO_CHANGE_IND`
    - `MSG_AIRPLANE_MODE_CHANGE_IND`

2. 呼叫事件 (Call Indication Message)

    - `MSG_CALL_STATE_CHANGE_IND`：呼叫状态变化通知
    - `MSG_CALL_RING_BACK_TONE_IND`：回铃音通知
    - `MSG_ECC_LIST_CHANGE_IND`：紧急呼叫列表变化通知
    - `MSG_DEFAULT_VOICECALL_SLOT_CHANGE_IND`：默认语音呼叫 slot 变化通知

3. 网络事件 (Network Indication Message)

    - `MSG_NETWORK_STATE_CHANGE_IND`
    - `MSG_VOICE_REGISTRATION_STATE_CHANGE_IND`
    - `MSG_CELLINFO_CHANGE_IND`
    - `MSG_SIGNAL_STRENGTH_CHANGE_IND`
    - `MSG_NITZ_STATE_CHANGE_IND`

4. 数据事件 (Data Indication Message)

    - `MSG_DATA_ENABLED_CHANGE_IND`
    - `MSG_DATA_REGISTRATION_STATE_CHANGE_IND`
    - `MSG_DATA_NETWORK_TYPE_CHANGE_IND`
    - `MSG_DATA_CONNECTION_STATE_CHANGE_IND`
    - `MSG_DEFAULT_DATA_SLOT_CHANGE_IND`

5. SIM 卡事件 (SIM Indication Message)

    - `MSG_SIM_STATE_CHANGE_IND`
    - `MSG_SIM_UICC_APP_ENABLED_CHANGE_IND`
    - `MSG_SIM_ICCID_CHANGE_IND`

6. STK 事件 (STK Indication Message)

    - `MSG_STK_AGENT_DISPLAY_TEXT_IND`
    - `MSG_STK_AGENT_REQUEST_DIGIT_IND`
    - `MSG_STK_AGENT_REQUEST_KEY_IND`
    - `MSG_STK_AGENT_REQUEST_CONFIRMATION_IND`
    - `MSG_STK_AGENT_REQUEST_INPUT_IND`
    - `MSG_STK_AGENT_REQUEST_DIGITS_IND`
    - `MSG_STK_AGENT_PLAY_TONE_IND`
    - `MSG_STK_AGENT_LOOP_TONE_IND`
    - `MSG_STK_AGENT_REQUEST_SELECTION_IND`
    - `MSG_STK_AGENT_REQUEST_QUICK_DIGIT_IND`
    - `MSG_STK_AGENT_CONFIRM_CALL_SETUP_IND`
    - `MSG_STK_AGENT_DISPLAY_ACTION_INFORMATION_IND`
    - `MSG_STK_AGENT_CONFIRM_LAUNCH_BROWSER_IND`
    - `MSG_STK_AGENT_DISPLAY_ACTION_IND`
    - `MSG_STK_AGENT_CONFIRM_OPEN_CHANNEL_IND`
    - `MSG_STK_AGENT_RELEASE_IND`
    - `MSG_STK_AGENT_CANCEL_IND`

7. 短信事件 (SMS Indication Message)

    - `MSG_INCOMING_MESSAGE_IND`
    - `MSG_IMMEDIATE_MESSAGE_IND`
    - `MSG_STATUS_REPORT_MESSAGE_IND`
    - `MSG_DEFAULT_SMS_SLOT_CHANGED_IND`

8. CBS 事件 (CBS Indication Message)

    - `MSG_INCOMING_CBS_IND`
    - `MSG_EMERGENCY_CBS_IND`

9. SS 事件 (SS Indication Message)

    - `MSG_CALL_BARRING_PROPERTY_CHANGE_IND`
    - `MSG_USSD_NOTIFICATION_RECEIVED_IND`
    - `MSG_USSD_REQUEST_RECEIVED_IND`
    - `MSG_USSD_PROPERTY_CHANGE_IND`

10. IMS 事件 (IMS Indication Message)

    - `MSG_IMS_REGISTRATION_MESSAGE_IND`

11. Modem 状态变化事件 (Modem State Change Message)

    - `MSG_MODEM_STATE_CHANGE_IND`

12. 其他事件

    - `MSG_DATA_LOGING_IND`
    - `MSG_MODEM_ECC_LIST_CHANGE_IND` = 61

#### 示例

##### 命令输入

```Bash
telephonytool> listen-modem 0 0
```

##### 输出信息

```Bash
telephonytool> listen-modem 0 0
[ 1632.199400] [35] [ DEBUG] [ap] start to watch radio event : 0 , return watch_id : 75
```

### 3、unlisten-modem

#### 命令说明

取消监听指定的 modem 事件。

#### 命令格式

```Bash
unlisten-modem [watch_id]
```

- watch_id：监听 ID，来源于 `listen-modem` 命令的返回值。

#### 示例

##### 命令输入

```Bash
telephonytool> unlisten-modem 75
```

##### 输出信息

以下是执行 `unlisten-modem` 命令的完整示例：

```Bash
telephonytool> listen-modem 0 0
[ 1632.199400] [35] [ DEBUG] [ap] start to watch radio event : 0 , return watch_id : 75
telephonytool> unlisten-modem 75
[ 2050.331400] [35] [ DEBUG] [ap] stop to watch radio event with watch_id : 75 with return value : 0
telephonytool>
```

### 4、get-radio-cap

#### 命令说明

查询 modem 的功能支持情况。

#### 命令格式

```Bash
get-radio-cap [feature_type]
```

- feature_type：指定要查询的功能类型。
    - `0`：语音（voice）
    - `1`：数据（data）
    - `2`：短信（sms）
    - `3`：IMS（IP Multimedia Subsystem）

#### 示例

##### 命令输入

```Bash
telephonytool> get-radio-cap 0
```

##### 输出信息

以下是执行 `get-radio-cap` 命令的完整示例：

```Bash
telephonytool> get-radio-cap 0
[ 2145.490400] [35] [ DEBUG] [ap] radio feature type : 0 is supported ? 1
telephonytool> get-radio-cap 1
[ 2164.658700] [35] [ DEBUG] [ap] radio feature type : 1 is supported ? 1
```

### 5、set-radio-power

#### 命令说明

设置指定 slot 的无线电（radio）电源状态，对应飞行模式的关闭和开启。

#### 命令格式

```Bash
set-radio-power [slot_id][state]
```

- slot_id：指定要设置的 slot，目前仅支持 `0`。
- state：无线电电源状态：
    - `0`：关闭无线电（radio off）
    - `1`：开启无线电（radio on）

#### 示例

##### 命令输入

```Bash
telephonytool>  set-radio-power 0 0
```

##### 输出信息

以下是执行 `set-radio-power` 命令的完整示例：

```Bash
telephonytool> set-radio-power 0 0
[ 2322.660700] [35] [ DEBUG] [ap] telephonytool_cmd_set_radio_power, slotId : 0 target_state: 0
telephonytool> set-radio-power 0 1
[ 2324.918200] [35] [ DEBUG] [ap] telephonytool_cmd_set_radio_power, slotId : 0 target_state: 1
```

### 6、get-radio-power

#### 命令说明

获取指定 slot 的无线电（radio）电源状态。

#### 命令格式

```Bash
get-radio-power [slot_id]
```

#### 示例

##### 命令输入

```Bash
telephonytool> get-radio-power 0
```

##### 输出信息

以下是执行 `get-radio-power` 命令的完整示例：

```Bash
telephonytool> get-radio-power 0
[ 2480.612100] [35] [ DEBUG] [ap] telephonytool_cmd_get_radio_power, slotId : 0 value : 1
```

### 7、set-rat-mode

#### 命令说明

设置指定 slot 的无线接入技术（RAT，Radio Access Technology）模式。

#### 命令格式

```Bash
set-rat-mode [slot_id] [mode]
```

- slot_id：指定要设置的 slot，目前仅支持 `0`。
- mode：目标网络模式，支持以下值：
    - `0`：UMTS
    - `1`：GSM only
    - `2`：WCDMA only
    - `9`：LTE/GSM/WCDMA
    - `11`：LTE only
    - `12`：LTE/WCDMA

#### 示例

##### 命令输入

```Bash
telephonytool> set-rat-mode 0 9
```

##### 输出信息

```Bash
telephonytool> set-rat-mode 0 11
[   48.155000] [35] [ DEBUG] [ap] telephonytool_cmd_set_rat_mode, slotId : 0 target_state: 11
[   53.549600] [21] [  INFO] [ap] [0,0059]> RIL_REQUEST_SET_PREFERRED_NETWORK_TYPE (11)
[   54.717700] [21] [  INFO] [ap] [0,0059]< RIL_REQUEST_SET_PREFERRED_NETWORK_TYPE
```

### 8、get-rat-mode

#### 命令说明

获取指定 slot 的无线接入技术（RAT，Radio Access Technology）模式。

#### 命令格式

```Bash
get-rat-mode [slot_id]
```

- slot_id：指定要查询的 slot，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-rat-mode 0
```

##### 输出信息

```Bash
telephonytool> get-rat-mode 0
[  184.550000] [35] [ DEBUG] [ap] telephonytool_cmd_get_rat_mode, slotId : 0 value :11
```

### 9、get-imei

#### 命令说明

获取设备的 IMEI（国际移动设备识别码）信息。

#### 命令格式

```Bash
set-rat-mode [slot_id]
slot_id:设置要监听的slot,当前只支持0
```

- slot_id：指定要查询的 slot，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-imei 0
```

##### 输出信息

以下是执行 `get-imei` 命令的完整示例：

```Bash
telephonytool> get-imei 0
[  236.301900] [35] [ DEBUG] [ap] telephonytool_cmd_get_imei, slotId : 0 imei : 8674000******7199
```

### 10、get-imeisv

#### 命令说明

获取设备的 IMEISV（国际移动设备识别码软件版本）信息。

#### 命令格式

```Bash
get-imeisv [slot_id]
```

- slot_id：指定要查询的 slot，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-imeisv 0
```

##### 输出信息

```Bash
telephonytool> get-imeisv 0  
[  401.567800] [35] [ DEBUG] [ap] telephonytool_cmd_get_imeisv, slotId : 0 imeisv : 8674000******7901
```

### 11、get-phone-state

#### 命令说明

获取设备的电话状态信息。

#### 命令格式

```Bash
get-phone-state [slot_id]
```

- slot_id：指定要查询的 slot，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-phone-state 0
```

##### 输出信息

```Bash
telephonytool> get-phone-state 0
[ 9427.739300] [35] [ DEBUG] [ap] telephonytool_cmd_get_phone_state, slotId : 0 state : 0
```

### 12、send-modem-power

#### 命令说明

控制 Modem 模块的开关状态。

#### 命令格式

```Bash
send-modem-power[slot_id] [on]
```

- slot_id：指定要操作的 slot，目前仅支持 `0`。
- on：设置 Modem 的目标状态：
    - `0`：关闭 Modem
    - `1`：开启 Modem

#### 示例

##### 命令输入

```Bash
telephonytool> send-modem-power 0 0
```

##### 输出信息

以下是执行 `send-modem-power` 命令的完整示例：

```Bash
telephonytool> send-modem-power 0 0
[ 9461.379300] [35] [ DEBUG] [ap] telephonytool_cmd_send_modem_power, slotId : 0 target_state: 0
telephonytool> [ 9461.415300] [21] [  INFO] [ap] modem_change_state, old state: 2, new state: 0
[ 9461.415900] [21] [  INFO] [ap] flush_atoms
[ 9461.421100] [21] [  INFO] [ap] free_contexts
```

### 13、get-radio-state

#### 命令说明

获取设备的无线电（Radio）状态信息。

#### 命令格式

```Bash
get-radio-state [slot_id]
```

- slot_id：指定要查询的 slot，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-radio-state 0
```

##### 输出信息

以下是执行 `get-radio-state` 命令的完整示例：

```Bash
telephonytool> get-radio-state 0
[ 9486.517900] [35] [ DEBUG] [ap] telephonytool_cmd_get_radio_state, slotId : 0 state : 1
```

### 14、get-modem-revision

#### 命令说明

获取 Modem 的基带版本信息。

#### 命令格式

```Bash
get-modem-revision [slot_id]
```

- slot_id：指定要查询的 slot，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-modem-revision 0
```

##### 输出信息

以下是执行 `get-modem-revision` 命令的完整示例：

```Bash
telephonytool> get-modem-revision 0
[ 9505.417900] [35] [ DEBUG] [ap] telephonytool_cmd_get_modem_revision, slotId : 0 value : 1.0.*.*  
```

### 15、get-msisdn

#### 命令说明

获取本地电话号码信息

#### 命令格式

```Bash
get-msisdn [slot_id]
```

- slot_id：指定要查询的 slot，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-msisdn 0
```

##### 输出信息

以下是执行 `get-msisdn` 命令的完整示例：

```Bash
telephonytool> get-msisdn 0
[ 9529.024200] [35] [  INFO] [ap] get phone number from UICC.
[ 9529.025200] [35] [ DEBUG] [ap] telephonytool_cmd_get_phone_number, slotId : 0  number : +1555******67
```

### 16、get-modem-activity-info

#### 命令说明

获取 Modem 的活动信息。

#### 命令格式

```Bash
get-modem-activity-info [slot_id]
```

- slot_id：指定要查询的 slot，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-modem-activity-info 0
```

##### 输出信息

以下是执行 `get-modem-activity-info` 命令的完整示例：

```Bash
telephonytool> get-modem-activity-info 0
[ 9743.317300] [35] [ DEBUG] [ap] telephonytool_cmd_get_modem_activity_info, slotId : 0
```

### 17、enable-modem

#### 命令说明

启用或关闭 Modem。

#### 命令格式

```Bash
enable-modem[slot_id] [state]
```

- slot_id：指定要操作的 slot，目前仅支持 `0`。
- state：设置 Modem 的目标状态：
    - `0`：关闭 Modem
    - `1`：开启 Modem

#### 示例

##### 命令输入

```Bash
telephonytool> enable-modem 0 1
```

##### 输出信息

以下是执行 `enable-modem` 命令的完整示例：

```Bash
telephonytool> enable-modem 0 1
[   15.700700] [28] [ DEBUG] [ap] telephonytool_cmd_enable_modem, slotId : 0 target_state: 1
```

### 18、get-modem-status

#### 命令说明

获取 Modem 的状态信息。

#### 命令格式

```Bash
get-modem-status [slot_id]
```

- slot_id：指定要查询的 slot，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-modem-status 0
```

##### 输出信息

以下是执行 `get-modem-status` 命令的完整示例：

```Bash
telephonytool> get-modem-status 0
[  782.186200] [28] [ DEBUG] [ap] telephonytool_cmd_get_modem_status, slotId : 0
```

### 19、oem-req-raw

#### 命令说明

直接发送格式化的 16 进制字符给 Modem，用于 eSIM 文件下载、eSIM 文件内容读取等操作。

#### 命令格式

```Bash
oem-req-raw [slot_id][request_data][data_length]
```

- slot_id：指定要操作的 slot，目前仅支持 `0`。
- request_data：16 进制字符串，表示要发送的原始数据。
- data_length：`request_data` 的字节数。

#### 示例

##### 命令输入

```Bash
telephonytool> oem-req-raw 0 01A0B023 4
```

##### 输出信息

```Bash
telephonytool> oem-req-raw 0 01A0B023 4
[  854.969700] [28] [ DEBUG] [ap] telephonytool_cmd_oem_ril_req_raw, slot_id: 0 oem_req: 01A0B023 length: 4
```

### 20、oem-req-strings

#### 命令说明

直接发送字符串到 Modem，例如 AT 命令。

#### 命令格式

```Bash
 oem-req-strings [slot_id][request_data][data_length]
```

- slot_id：指定要操作的 slot，目前仅支持 `0`。
- request_data：要发送的字符串，例如 AT 命令。
- data_length：`request_data` 的字节数。

#### 示例

##### 命令输入

```Bash
telephonytool> oem-req-strings 0 AT+CPIN? 1
```

##### 输出信息

```Bash
telephonytool> oem-req-strings 0 AT+CPIN? 1
[  870.751200] [28] [ DEBUG] [ap] telephonytool_cmd_oem_ril_req_strings, slot_id: 0 length: 1
```

### 21、send-command

#### 命令说明

直接发送内部的 RIL（Radio Interface Layer）消息。

#### 命令格式

```Bash
send-command [slot_id][atom id][ril request id]
```

- slot_id：指定要操作的 slot，目前仅支持 `0`。
- atom_id：Atom ID 信息，用于标识目标模块。
- ril_request_id：内部的 Request ID 信息，用于指定请求类型。

#### 示例

##### 命令输入

```Bash
telephonytool> send-command 0 16 57
```

##### 输出信息

```Bash
telehonytool>
telephonytool> send-command 0 16 57
[  882.733000] [28] [ DEBUG] [ap] telephonytool_cmd_send_command, slot_id: 0 atom: 16  command: 57
```

### 22、send-screen-state

#### 命令说明

设置屏幕开关状态信息给modem

#### 命令格式

```Bash
send-screen-state [slot_id][][screen_state]
```

- slot_id：指定要操作的 slot，目前仅支持 `0`。
- screen_state：屏幕状态：
    - `0`：屏幕关闭状态
    - `1`：屏幕开启状态

#### 示例

##### 命令输入

```Bash
telephonytool> send-screen-state 0 1
```

##### 输出信息

```Bash
telephonytool>
telephonytool> send-screen-state 0 1
telephonytool> [  927.719000] [21] [  INFO] [ap] Set fast_dormancy: 1
```
