# network 命令

\[ [English](../../../../../en/device_dev_guide/connection/telephony/telephonytool/network.md) | 简体中文 \]

## 一、概述

在 openvela 的 NSH 命令行中，可以通过进入 telephonytool 命令工具的 Console， 来执行所有与网络（network）相关的操作。

## 二、前提条件

确保已打开 `telephonytool` 工具，执行如下命令：

```Bash
ap> telephonytool
```

## 三、命令

### 1、listen-network

#### 命令说明

`listen-network` 命令用于注册监听与网络（network）相关的事件。

#### 命令格式

```Bash
listen-network [slot_id][event_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。
- event_id：事件 ID，支持以下事件类型：
    - `MSG_NETWORK_STATE_CHANGE_IND`：网络状态变化指示。
    - `MSG_VOICE_REGISTRATION_STATE_CHANGE_IND`：语音注册状态变化指示。
    - `MSG_CELLINFO_CHANGE_IND`：小区信息变化指示。
    - `MSG_SIGNAL_STRENGTH_CHANGE_IND`：信号强度变化指示。
    - `MSG_NITZ_STATE_CHANGE_IND`：NITZ（Network Identity and Time Zone）状态变化指示。

#### 示例

##### 命令输入

```Bash
telephonytool>listen-network 0 18
```

##### 输出信息

```Bash
telephonytool> listen-network 0 18
[21503.829200] [46] [ DEBUG] [ap] start to watch network event : 18 , return watch_id : 198
```

### 2、unlisten-network

#### 命令说明

`unlisten-network` 命令用于取消监听与网络（network）相关的事件。

#### 命令格式

```Bash
unlisten-network [watch_id]
```

- watch_id：对应 `listen-network` 命令的返回值，用于标识需要取消监听的事件。

#### 示例

##### 命令输入

```Bash
telephonytool> 
```

##### 输出信息

```Bash
telephonytool> unlisten-network 198
[21522.399100] [46] [ DEBUG] [ap] stop to watch network event with watch_id : 198 with return value : 0
```

### 3、register-auto

#### 命令说明

`register-auto` 命令用于设置为自动网络选择模式。

#### 命令格式

```Bash
register-auto [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>register-auto 0
```

##### 输出信息

```Bash
telephonytool> register-auto 0
[21549.525700] [46] [ DEBUG] [ap] telephonytool_cmd_network_select_auto, slotId : 0 value :0
telephonytool> [21549.532800] [21] [  INFO] [ap] [0,0110]> RIL_REQUEST_SET_NETWORK_SELECTION_AUTOMATIC
[21549.534000] [15] [  INFO] [ap] [AT_RIL] onRequest: 46<->SET_NETWORK_SELECTION_AUTOMATIC, reqtype: 6
```

### 4、register-manual

#### 命令说明

`register-manual` 命令用于设置手动选网模式。

#### 命令格式

```Bash
 register-manual [slot_id][mcc][mnc][technology]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。
- mcc：国家码（Mobile Country Code）。
- mnc：网络码（Mobile Network Code）。
- technology：无线接入技术类型（RAT，Radio Access Technology），例如 `lte`。

#### 示例

##### 命令输入

```Bash
telephonytool>register-manual 0 460 00 lte
```

##### 输出信息

```Bash
telephonytool> register-manual 0 460 00 lte
telephonytool> [   23.514600] [21] [  INFO] [ap] [0,0079]> RIL_REQUEST_SET_NETWORK_SELECTION_MANUAL (46000)
[   24.438000] [15] [  INFO] [ap] [AT_RIL] onRequest: 47<->SET_NETWORK_SELECTION_MANUAL, reqtype: 6
```

### 5、get-signalstrength

#### 命令说明

`get-signalstrength` 命令用于获取设备的信号强度信息。

#### 命令格式

```Bash
get-signalstrength [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-signalstrength 0
```

##### 输出信息

```Bash
telephonytool> get-signalstrength 0
[   53.030000] [35] [ DEBUG] [ap] telephonytool_cmd_query_signalstrength, slotId : 0 rssi :2147483647 rsrp :-68 rsrq :2147483647 rssnr :2147483647 cqi : 2147483647 level :4
```

### 6、get-display-name

#### 命令说明

`get-display-name` 命令用于获取当前驻留网络的运营商名称。

#### 命令格式

```Bash
get-display-name [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>get-display-name 0
```

##### 输出信息

```Bash
get-display-name 0
[   76.929700] [35] [ DEBUG] [ap] telephonytool_cmd_get_operator_name, slotId : 0 value :
```

### 7、get-registration-info

#### 命令说明

`get-registration-info` 命令用于获取设备的网络注册信息。

#### 命令格式

```Bash
get-registration-info [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-registration-info 0
```

##### 输出信息

```Bash
get-registration-info 0
telephonytool> [   96.809800] [31] [ DEBUG] [ap] network_event_callback :
[   96.810200] [31] [ DEBUG] [ap] reg_state = 4 operator_name =  mcc =  mnc =
```

### 8、get-voice-nwtype

#### 命令说明

`get-voice-nwtype` 命令用于获取 CS（Circuit Switched）域的网络类型。

#### 命令格式

```Bash
get-voice-nwtype [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>get-voice-nwtype 0
```

##### 输出信息

```Bash
get-voice-nwtype 0
[  117.115200] [35] [ DEBUG] [ap] telephonytool_cmd_get_voice_networktype, slotId : 0 value :0
```

### 9、get-voice-registered

#### 命令说明

`get-voice-registered` 命令用于获取 CS（Circuit Switched）域的注册状态。

#### 命令格式

```Bash
get-voice-registered [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-voice-registered 0
```

##### 输出信息

```Bash
telephonytool> get-voice-registered 0
[  131.299100] [35] [ DEBUG] [ap] telephonytool_cmd_is_voice_registered, slotId : 0 value :0
```

### 10、get-voice-roaming

#### 命令说明

`get-voice-roaming` 命令用于获取 CS（Circuit Switched）域的漫游状态。

#### 命令格式

```Bash
get-voice-roaming [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>get-voice-roaming 0
```

##### 输出信息

```Bash
telephonytool> get-voice-roaming 0
[  149.630700] [35] [ DEBUG] [ap] telephonytool_cmd_is_voice_roaming, slotId : 0 value :0
```

### 11、scan-network

#### 命令说明

`scan-network` 命令用于发起搜网操作，查询当前可用的网络。

#### 命令格式

```Bash
scan-network [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>scan-network 0
```

##### 输出信息

```Bash
telephonytool> scan-network 0
telephonytool> [  161.901900] [21] [  INFO] [ap] [0,0087]> RIL_REQUEST_QUERY_AVAILABLE_NETWORKS
[  161.906400] [15] [  INFO] [ap] [AT_RIL] onRequest: 48<->QUERY_AVAILABLE_NETWORKS , reqtype: 6
```

### 12、get-serving-cellinfo

#### 命令说明

`get-serving-cellinfo` 命令用于获取当前服务小区的相关信息。

#### 命令格式

```Bash
get-serving-cellinfo [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>get-serving-cellinfo 0
```

##### 输出信息

```Bash
telephonytool> get-serving-cellinfo 0
telephonytool> [  175.409900] [21] [  INFO] [ap] [0,0088]> RIL_REQUEST_GET_CELL_INFO_LIST
[  175.414500] [15] [  INFO] [ap] [AT_RIL] onRequest: 109<->GET_CELL_INFO_LIST, reqtype: 6
[  175.417500] [21] [  INFO] [ap] [0,0088]< RIL_REQUEST_GET_CELL_INFO_LIST cell_info_cnt = 1 {type = 1, registered = 1, mcc = 311, mnc = 740, lac = 8514, ci = 47108, strength = 0, ber = 1}
```

### 13、get-neighbouring-cellInfos

#### 命令说明

`get-neighbouring-cellInfos` 命令用于获取邻区的相关信息。

#### 命令格式

```Bash
get-neighbouring-cellInfos [slot_id]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>get-neighbouring-cellInfos 0
```

##### 输出信息

```Bash
telephonytool> get-neighbouring-cellInfos 0
telephonytool> [  192.285200] [21] [  INFO] [ap] [0,0089]> RIL_REQUEST_GET_NEIGHBORING_CELL_IDS
[  192.286100] [15] [  INFO] [ap] [AT_RIL] onRequest: 75<->GET_NEIGHBORING_CELL_IDS, reqtype: 6
[  192.286700] [21] [ ERROR] [ap] parcel_r_int32: parcel is too small
[  192.286900] [21] [  INFO] [ap] [0,0089]< RIL_REQUEST_GET_NEIGHBORING_CELL_IDS cell_info_cnt = 2 {type = 90, registered = 4, mcc = 091, mnc = 04, {type = 3145778, registered = 3473458, mcc = 000, mnc = 00,
[  192.300600] [31] [ DEBUG] [ap] ci : 0, mcc : 091, mnc : 04, registered : 1, type : 101,
[  192.300900] [31] [ DEBUG] [ap] ci : 0, mcc : 000, mnc : 00, registered : 1, type : 0,
```

### 14、set-cell-info-list-rate

#### 命令说明

`set-cell-info-list-rate` 命令用于设置小区信息的更新周期。

#### 命令格式

```Bash
set-cell-info-list-rate [slot_id][period]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。
- period：更新周期，单位为秒。

#### 示例

##### 命令输入

```Bash
telephonytool>set-cell-info-list-rate 0 10
```

##### 输出信息

```Bash
telephonytool> set-cell-info-list-rate 0 10
[  209.176900] [35] [ DEBUG] [ap] telephonytool_cmd_set_cell_info_list_rate, slot_id: 0 period: 10
telephonytool> [  209.201300] [21] [  INFO] [ap] [0,0090]> RIL_REQUEST_SET_UNSOL_CELL_INFO_LIST_RATE
[  209.205100] [15] [  INFO] [ap] [AT_RIL] onRequest: 110<->SET_UNSOL_CELL_INFO_LIST_RATE, reqtype: 6
```
