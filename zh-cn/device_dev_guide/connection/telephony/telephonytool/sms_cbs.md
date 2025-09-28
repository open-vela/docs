# sms/cbs 命令

\[ [English](../../../../../en/device_dev_guide/connection/telephony/telephonytool/sms_cbs.md) | 简体中文 \]

## 一、概述

在 openvela 的 NSH 命令行中，可以通过进入 telephonytool 命令工具的 Console，执行所有与 SMS（Short Message Service，短消息服务）和 CBS（Cell Broadcast Service，小区广播服务）相关的操作。

## 二、前提条件

确保已打开 `telephonytool` 工具，执行如下命令：

```Bash
ap> telephonytool
```

## 三、命令

### 1、send-sms

#### 命令说明

`send-sms` 命令用于发送短消息（SMS，Short Message Service）。

#### 命令格式

```Bash
send-sms [slot_id][number][text]
```

- slot_id: 设置要监听的插槽，目前仅支持 `0`。
- number: 目标电话号码。
- text: 短消息的内容。

#### 示例

##### 命令输入

```Bash
telephonytool> send-sms 0 10086 hello
```

##### 输出信息

```Bash
telephonytool> send-sms 0 10086 hello
[17860.285400] [46] [ DEBUG] [ap] telephonytool_tapi_sms_send_message, slotId : 0  number : 10086 text: hello
[17860.337600] [21] [  INFO] [ap] tx_next: 0x40a400f0
[17860.338000] [21] [  INFO] [ap] pdu_len: 17, tpdu_len: 16 mms: 0
[17860.338400] [21] [  INFO] [ap] [0,0101]> RIL_REQUEST_SEND_SMS (110005810180F60000A705E8329BFD06)
[17860.345300] [15] [  INFO] [ap] [AT_RIL] onRequest: 25<->SEND_SMS, reqtype: 3
[17860.415800] [21] [  INFO] [ap] [0,0101]< RIL_REQUEST_SEND_SMS {2,(null),0}
[17860.416100] [21] [  INFO] [ap] tx_finished 0x40a400f0
[17860.510200] [40] [ DEBUG] [ap] tele_sms_event_response :
[17860.510400] [40] [ DEBUG] [ap] result->msg_id : 129
[17860.510500] [40] [ DEBUG] [ap] result->status : 0
[17860.510700] [40] [ DEBUG] [ap] result->arg1 : 0
[17860.510800] [40] [ DEBUG] [ap] result->arg2 : 0
[17860.511000] [40] [ DEBUG] [ap] send message successed, uuid : /ril_0/message_80E48FEE******2BE819803B
```

### 2、send-data-sms

#### 命令说明

`send-data-sms` 命令用于发送数据短消息（Data SMS）。数据短消息是一种特殊的 SMS 类型，通常用于传输二进制数据或应用程序间的通信。

#### 命令格式

```Bash
send-sms [slot_id][number][text][port]
```

- slot_id: 设置要监听的插槽，目前仅支持 `0`。
- number: 目标电话号码。
- text: 短消息的内容。
- port: 数据短消息的目标端口号。

#### 示例

##### 命令输入

```Bash
telephonytool> send-data-sms 0 10086 hello 0
```

##### 输出信息

```Bash
telephonytool> send-data-sms 0 10086 hello 0
[17884.617100] [46] [ DEBUG] [ap] telephonytool_tapi_sms_send_data_message, slotId: 0  number: 10086 text: hello port: 0
[17884.620200] [46] [ DEBUG] [ap] OFONO_DFX_SMS:5,4,1,0
[17884.664800] [21] [  INFO] [ap] tx_next: 0x409750f0
[17884.665100] [21] [  INFO] [ap] pdu_len: 24, tpdu_len: 23 mms: 0
[17884.665600] [21] [  INFO] [ap] [0,0102]> RIL_REQUEST_SEND_SMS (510005810180F60004A70C0605040000000068656C6C6F)
[17884.673100] [15] [  INFO] [ap] [AT_RIL] onRequest: 25<->SEND_SMS, reqtype: 3
[17884.744100] [21] [  INFO] [ap] [0,0102]< RIL_REQUEST_SEND_SMS {3,(null),0}
[17884.744400] [21] [  INFO] [ap] tx_finished 0x409750f0
[17884.827800] [10] [  INFO] [ap] sysevent_dev_poll: setup: 1
[17884.889400] [40] [ DEBUG] [ap] tele_sms_event_response :
[17884.889600] [40] [ DEBUG] [ap] result->msg_id : 130
[17884.889800] [40] [ DEBUG] [ap] result->status : 0
[17884.890000] [40] [ DEBUG] [ap] result->arg1 : 0
[17884.890100] [40] [ DEBUG] [ap] result->arg2 : 0
[17884.890300] [40] [ DEBUG] [ap] send message successed, uuid : /ril_0/message_064DE2FF8******F8C77
```

### 3、get-service-center-number

#### 命令说明

`get-service-center-number` 命令用于获取短消息服务中心（SMSC，Short Message Service Center）的电话号码。

#### 命令格式

```Bash
get-service-center-number [slot_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>get-service-center-number 0
```

##### 输出信息

```Bash
telephonytool> get-service-center-number 0
[18090.348600] [46] [ DEBUG] [ap] telephonytool_tapi_sms_get_service_center_number, slotId : 0  smsc_addr: 10086
```

### 4、set-service-center-number

#### 命令说明

`set-service-center-number` 命令用于设置短消息服务中心（SMSC，Short Message Service Center）的电话号码。

#### 命令格式

```Bash
set-service-center-number [slot_id][number]
```

- slot_id: 设置要监听的插槽，目前仅支持 `0`。
- number: 服务中心号码。

#### 示例

##### 命令输入

```Bash
telephonytool>set-service-center-number 0 10086
```

##### 输出信息

```Bash
telephonytool> set-service-center-number 0 10086
[18074.174100] [46] [ DEBUG] [ap] telephonytool_tapi_sms_set_service_center_number, slotId : 0 smsc_addr: 10086
telephonytool> [18074.206600] [21] [  INFO] [ap] [0,0103]> RIL_REQUEST_SET_SMSC_ADDRESS (***)
[18074.209500] [15] [  INFO] [ap] [AT_RIL] onRequest: 101<->SET_SMSC_ADDRESS, reqtype: 3
[18074.212200] [21] [  INFO] [ap] Sending csca_query
[18074.212700] [21] [  INFO] [ap] [0,0104]> RIL_REQUEST_GET_SMSC_ADDRESS
[18074.214400] [15] [  INFO] [ap] [AT_RIL] onRequest: 100<->GET_SMSC_ADDRESS, reqtype: 3
[18074.216100] [21] [  INFO] [ap] [0,0104]< RIL_REQUEST_GET_SMSC_ADDRESS {type=129,number=***}
```

### 5、get-cell-broadcast-power

#### 命令说明

`get-cell-broadcast-power` 命令用于获取接收小区广播（Cell Broadcast，CB）功能的开关状态。

#### 命令格式

```Bash
get-cell-broadcast-power [slot_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>get-cell-broadcast-power 0
```

##### 输出信息

```Bash
telephonytool> get-cell-broadcast-power 0
[18233.940800] [46] [ DEBUG] [ap] telephonytool_tapi_sms_get_cell_broadcast_power, slotId : 0 state: 1
```

- state:
    - `1`: 表示小区广播功能已启用。
    - `0`: 表示小区广播功能已禁用。

### 6、set-cell-broadcast-power

#### 命令说明

`set-cell-broadcast-power` 命令用于设置开启或关闭接收小区广播（Cell Broadcast，CB）功能。

#### 命令格式

```Bash
set-cell-broadcast-power [slot_id][state]
```

- slot_id: 设置要监听的插槽，目前仅支持 `0`。
- state:
    - `0`: 关闭接收小区广播。
    - `1`: 开启接收小区广播。

#### 示例

##### 命令输入

```Bash
telephonytool> set-cell-broadcast-power 0 1
```

##### 输出信息

```Bash
telephonytool> set-cell-broadcast-power 0 1
[18220.629900] [46] [ DEBUG] [ap] telephonytool_tapi_sms_set_cell_broadcast_power, slotId : 0 state: 1
telephonytool> [18220.661800] [21] [  INFO] [ap] [0,0105]> RIL_REQUEST_GSM_SET_BROADCAST_SMS_CONFIG
[18220.664700] [15] [  INFO] [ap] [AT_RIL] onRequest: 90<->GSM_SET_BROADCAST_SMS_CONFIG, reqtype: 3
```

- state:
    - `1`: 表示小区广播功能已成功启用。
    - `0`: 表示小区广播功能已成功关闭。

### 7、get-cell-broadcast-topics

#### 命令说明

`get-cell-broadcast-topics` 命令用于获取设备支持的广播消息类型（Cell Broadcast Topics）。

#### 命令格式

```Bash
get-cell-broadcast-topics [slot_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>get-cell-broadcast-topics 0
```

##### 输出信息

```Bash
telephonytool> get-cell-broadcast-topics 0
[18328.263700] [46] [ DEBUG] [ap] telephonytool_tapi_sms_get_cell_broadcast_topics, slotId : 0  cbs_topics: 1
```

- cbs_topics: 表示支持的广播消息类型。

### 8、set-cell-broadcast-topics

#### 命令说明

`set-cell-broadcast-topics` 命令用于设置设备支持的广播消息类型（Cell Broadcast Topics）。

#### 命令格式

```Bash
set-cell-broadcast-topics [slot_id][topic_type]
```

- slot_id: 设置要监听的插槽，目前仅支持 `0`。
- topic_type: 指定广播消息的类型，例如 `etws`（Earthquake and Tsunami Warning System，地震和海啸预警系统）、`cmas`（Commercial Mobile Alert System，商业移动警报系统）等。

#### 示例

##### 命令输入

```Bash
telephonytool> set-cell-broadcast-topics 0 1
```

##### 输出信息

```Bash
telephonytool> set-cell-broadcast-topics 0 1
[18314.860400] [46] [ DEBUG] [ap] telephonytool_tapi_sms_set_cell_broadcast_topics, slotId : 0 cbs_topics: 1
telephonytool> [18314.898000] [21] [  INFO] [ap] [0,0106]> RIL_REQUEST_GSM_SET_BROADCAST_SMS_CONFIG
[18314.901100] [15] [  INFO] [ap] [AT_RIL] onRequest: 90<->GSM_SET_BROADCAST_SMS_CONFIG, reqtype: 3
```

- cbs_topics: 表示设置的广播消息类型。

### 9、copy-sms-to-sim

#### 命令说明

`copy-sms-to-sim` 命令用于将短消息拷贝到 SIM 卡中。

#### 命令格式

```Bash
copy-sms-to-sim [slot_id][number][text]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。
- number：目标电话号码。
- text：短消息的内容。

#### 示例

##### 命令输入

```Bash
telephonytool> copy-sms-to-sim 0 10086 hello11
```

##### 输出信息

```Bash
telephonytool> copy-sms-to-sim 0 10086 hello11
[18362.255300] [46] [ DEBUG] [ap] telephonytool_tapi_sms_copy_message_to_sim, slotId : 0  number : 10086 text: hello11 port 0
telephonytool> [18362.292600] [21] [  INFO] [ap] pdu_len: 14
[18362.293500] [21] [  INFO] [ap] [0,0107]> RIL_REQUEST_WRITE_SMS_TO_SIM
[18362.295700] [15] [  INFO] [ap] [AT_RIL] onRequest: 63<->WRITE_SMS_TO_SIM, reqtype: 3
[18362.298600] [21] [  INFO] [ap] [0,0107]< RIL_REQUEST_WRITE_SMS_TO_SIM
```

### 10、delete-sms-from-sim

#### 命令说明

`delete-sms-from-sim` 命令用于删除 SIM 卡中的短消息。

#### 命令格式

```Bash
delete-sms-from-sim [slot_id][index]
```

- slot_id：设置要监听的卡槽，目前仅支持 `0`。
- index：短消息对应的序号。

#### 示例

##### 命令输入

```Bash
telephonytool> delete-sms-from-sim 0 1
```

##### 输出信息

```Bash
telephonytool> delete-sms-from-sim 0 1
[18398.380000] [46] [ DEBUG] [ap] telephonytool_tapi_sms_delete_message_from_sim, slotId : 0 index: 1
telephonytool> [18398.408700] [21] [  INFO] [ap] [0,0109]> RIL_REQUEST_DELETE_SMS_ON_SIM
[18398.411500] [15] [  INFO] [ap] [AT_RIL] onRequest: 64<-><unknown request>, reqtype: 3
[18398.413700] [21] [ ERROR] [ap] parcel_r_int32: parcel is too small
[18398.414300] [21] [  INFO] [ap] [0,0109]< RIL_REQUEST_DELETE_SMS_ON_SIM {0}
```
