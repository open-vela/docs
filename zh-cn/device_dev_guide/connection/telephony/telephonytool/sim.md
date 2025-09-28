# sim 命令

\[ [English](../../../../../en/device_dev_guide/connection/telephony/telephonytool/sim.md) | 简体中文 \]

## 一、概述

在 openvela 的 NSH 命令行中，可以通过进入 telephonytool 命令工具的 Console 来执行所有与 SIM 卡相关的操作。

## 二、前提条件

确保已打开 `telephonytool` 工具。

```Bash
ap> telephonytool
```

## 三、命令

### 1、listen-sim

#### 命令说明

`listen-sim` 命令用于注册监听与 SIM 卡相关的事件。

#### 命令格式

```Bash
listen-sim [slot_id][event_id]
```

- slot_id: 设置要监听的插槽，目前仅支持 `0`。
- event_id: 要监听的事件 ID，支持以下事件：
    - `MSG_SIM_STATE_CHANGE_IND`: SIM 状态变更事件。
    - `MSG_SIM_UICC_APP_ENABLED_CHANGE_IND`: SIM UICC 应用启用状态变更事件。
    - `MSG_SIM_ICCID_CHANGE_IND`: SIM ICCID（集成电路卡标识符）变更事件。

#### 示例

##### 命令输入

```Bash
telephonytool> listen-sim 0 28
```

##### 输出信息

```Bash
listen-sim 0 28
[12296.667000] [46] [ DEBUG] [ap] start to watch sim event : 28 , return watch_id : 189
```

### 2、unlisten-sim

#### 命令说明

`unlisten-sim` 命令用于取消监听与 SIM 卡相关的事件。

#### 命令格式

```Bash
unlisten-sim [watch_id]
```

- watch_id: 对应 `listen-sim` 命令返回的监听 ID，用于标识需要取消的监听事件。

#### 示例

##### 命令输入

```Bash
telephonytool> unlisten-sim 189
```

##### 输出信息

```Bash
telephonytool> unlisten-sim 189
[12323.192900] [46] [ DEBUG] [ap] stop to watch sim event with watch_id : 189 with return value : 0
```

### 3、has-icc

#### 命令说明

`has-icc` 命令用于查询指定插槽中是否存在 ICC（Integrated Circuit Card，集成电路卡）。

#### 命令格式

```Bash
has-icc [slot_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> has-icc 0
```

##### 输出信息

```Bash
telephonytool> has-icc 0
[12341.192300] [46] [ DEBUG] [ap] telephonytool_cmd_has_icc_card, slotId : 0 value : 1
```

### 4、get-sim-state

#### 命令说明

`get-sim-state` 命令用于获取指定插槽中 SIM 卡的状态。

#### 命令格式

```Bash
get-sim-state [slot_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-sim-state 0
```

##### 输出信息

```Bash
get-sim-state 0
[12357.230900] [46] [ DEBUG] [ap] telephonytool_cmd_get_sim_state, slotId : 0 state : SIM_READY
```

### 5、get-iccid

#### 命令说明

`get-iccid` 命令用于获取指定插槽中 SIM 卡的 ICCID（Integrated Circuit Card Identifier，集成电路卡标识符）信息。

#### 命令格式

```Bash
get-iccid [slot_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>  get-iccid 0
```

##### 输出信息

```Bash
telephonytool> get-iccid 0
[12378.832200] [46] [ DEBUG] [ap] telephonytool_cmd_get_sim_iccid, slotId : 0 iccid : 12345678901234567890  # 示例数据 
```

### 6、get-sim-operator

#### 命令说明

`get-sim-operator` 命令用于获取指定插槽中 SIM 卡的 PLMN（Public Land Mobile Network，公共陆地移动网络）信息。PLMN 是由运营商的国家代码（MCC）和网络代码（MNC）组成的标识符，用于标识 SIM 卡所属的运营商。

#### 命令格式

```Bash
get-sim-operator [slot_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-sim-operator 0
```

##### 输出信息

```Bash
telephonytool> get-sim-operator 0
[12795.415400] [46] [ DEBUG] [ap] telephonytool_cmd_get_sim_operator, slotId : 0 operator : 310260
```

### 7、get-sim-operator-name

#### 命令说明

`get-sim-operator-name` 命令用于获取指定插槽中 SIM 卡所属运营商的名称（SPN，Service Provider Name）。

#### 命令格式

```Bash
get-sim-operator-name [slot_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-sim-operator-name 0
```

##### 输出信息

```Bash
telephonytool> get-sim-operator-name 0
[12809.795600] [46] [ DEBUG] [ap] telephonytool_cmd_get_sim_operator_name, slotId : 0 spn : T-Mobile
```

### 8、get-sim-subscriber-id

#### 命令说明

`get-sim-subscriber-id` 命令用于获取指定插槽中 SIM 卡的订阅者标识（Subscriber ID）。

#### 命令格式

```Bash
get-sim-subscriber-id [slot_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-sim-subscriber-id 0
```

##### 输出信息

```Bash
telephonytool> get-sim-subscriber-id 0
[12824.331100] [46] [ DEBUG] [ap] telephonytool_cmd_get_sim_subscriber_id, slotId : 0 subscriber_id : 310260000000000
```

### 9、change-pin

#### 命令说明

`change-pin` 命令用于修改指定插槽中 SIM 卡的 PIN（Personal Identification Number，个人识别码）。

#### 命令格式

```Bash
change-pin [slot_id][pin_type, pin or pin2][old_pin][new_pin]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。
- pin_type: PIN 码类型，可选值为 `pin` 或 `pin2`。
- old_pin: 当前的 PIN 码值。
- new_pin: 要设置的新 PIN 码值。

#### 示例

##### 命令输入

```Bash
telephonytool> change-pin 0 pin 1234 2345
```

##### 输出信息

```Bash
telephonytool> change-pin 0 pin 1234 2345
[12840.148400] [46] [ DEBUG] [ap] telephonytool_cmd_change_sim_pin, slot_id: 0 pin_type: pin old_pin: 1234 new_pin: 2345
telephonytool> [12840.160200] [21] [  INFO] [ap] [0,0081]> RIL_REQUEST_CHANGE_SIM_PIN (old=***,new=***,aid=(null))
```

### 10、Enter-pin

#### 命令说明

`enter-pin` 命令用于验证指定插槽中 SIM 卡的 PIN（Personal Identification Number，个人识别码）。

#### 命令格式

```Bash
enter-pin [slot_id][pin_type][pin]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。
- pin_type: PIN 码类型，可选值为 `pin` 或 `pin2`。
- pin: 要验证的 PIN 码值。

#### 示例

##### 命令输入

```Bash
telephonytool> enter-pin 0 pin 1234
```

##### 输出信息

```Bash
telephonytool> enter-pin 0 pin 1234
[12860.520000] [46] [ DEBUG] [ap] telephonytool_cmd_enter_sim_pin, slot_id: 0 pin_type: pin pin: ****
```

### 11、reset-pin

#### 命令说明

`reset-pin` 命令用于通过 PUK（Personal Unblocking Key，个人解锁密钥）重置指定插槽中 SIM 卡的 PIN（Personal Identification Number，个人识别码）。

#### 命令格式

```Bash
reset-pin [slot_id][puk_type][puk][new_pin]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。
- puk_type: PUK 码类型，可选值为 `puk` 或 `puk2`。
- puk: 当前的 PUK 码值，用于解锁 PIN。
- new_pin: 要设置的新 PIN 码值。

#### 示例

##### 命令输入

```Bash
telephonytool> reset-pin 0 puk 12345678 2345
```

##### 输出信息

```Bash
telephonytool> reset-pin 0 puk 12345678 2345
[12877.463600] [46] [ DEBUG] [ap] telephonytool_cmd_reset_sim_pin, slot_id: 0 puk_type: puk puk: ****** new_pin: ******
```

### 12、lock-pin

#### 命令说明

`lock-pin` 命令用于激活 SIM 卡的 PIN 锁功能，确保 SIM 卡的安全性。

#### 命令格式

```Bash
lock-pin [slot_id][pin_type, pin or pin2][pin]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。
- pin_type: PIN 码类型，可选值为 `pin` 或 `pin2`。
- pin: 当前的 PIN 码值，用于激活 PIN 锁。

#### 示例

##### 命令输入

```Bash
telephonytool> lock-pin 0 pin 1234 
```

##### 输出信息

```Bash
telephonytool> lock-pin 0 pin 1234
[12894.617100] [46] [ DEBUG] [ap] telephonytool_cmd_lock_sim_pin, slot_id: 0 pin_type: pin pin: 1234
telephonytool> [12894.648800] [21] [  INFO] [ap] [0,0092]> RIL_REQUEST_SET_FACILITY_LOCK (SC,1,***,0,aid=(null))
```

### 13、unlock-pin

#### 命令说明

`unlock-pin` 命令用于去激活 SIM 卡的 PIN 锁功能，解除对 SIM 卡的 PIN 验证要求。

#### 命令格式

```Bash
unlock-pin [slot_id][pin_type, pin or pin2][pin]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。
- pin_type: PIN 码类型，可选值为 `pin` 或 `pin2`。
- pin: 当前的 PIN 码值，用于解除 PIN 锁。

#### 示例

##### 命令输入

```Bash
telephonytool>unlock-pin 0 pin 1234
```

##### 输出信息

```Bash
telephonytool> unlock-pin 0 pin 1234
[12907.847700] [46] [ DEBUG] [ap] telephonytool_cmd_unlock_sim_pin, slot_id: 0 pin_type: pin pin: 1234
telephonytool> [12907.882000] [21] [  INFO] [ap] [0,0093]> RIL_REQUEST_SET_FACILITY_LOCK (SC,0,***,0,aid=(null))
```

### 14、open-logical-channel

#### 命令说明

`open-logical-channel` 命令用于打开逻辑通道，以便对 SIM 卡进行读写操作。

#### 命令格式

```Bash
open-logical-channel [slot_id] [aid_str]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。
- aid_str: 应用标识符（AID，Application Identifier）字符串，用于指定目标应用。

#### 示例

##### 命令输入

```Bash
telephonytool>open-logical-channel 0 A0000000871002FF86FFFF89FFFFFFFF 16
```

##### 输出信息

```Bash
telephonytool> open-logical-channel 0 A0000000871002FF86FFFF89FFFFFFFF 16
[12924.300200] [46] [ DEBUG] [ap] telephonytool_cmd_open_logical_channel, slot_id: 0 aid: A0000000871002FF86FFFF89FFFFFFFF len: 16
telephonytool> [12924.334200] [21] [  INFO] [ap] [0,0094]> RIL_REQUEST_SIM_OPEN_CHANNEL (A0000000871002FF86FFFF89FFFFFFFF, -1)
[12924.337900] [15] [  INFO] [ap] [AT_RIL] onRequest: 115<->SIM_OPEN_CHANNEL, reqtype: 4
[12924.340100] [15] [  INFO] [ap] [AT_SIM] On request sim end
[12924.341400] [21] [  INFO] [ap] [0,0094]< RIL_REQUEST_SIM_OPEN_CHANNEL {1, 0}
[12924.348700] [40] [ DEBUG] [ap] tele_sim_async_fun :
[12924.349100] [40] [ DEBUG] [ap] result->msg_id : 38
[12924.349600] [40] [ DEBUG] [ap] result->status : 0
[12924.350000] [40] [ DEBUG] [ap] result->arg1 : 0
[12924.350300] [40] [ DEBUG] [ap] result->arg2 : 1
12924.350600] [40] [ DEBUG] [ap] open logical channel respond session id : 1
```

- session id: 返回的 `session id` 表示逻辑通道的会话标识符，用于后续的读写操作。

### 15、close-logical-channel

#### 命令说明

`close-logical-channel` 命令用于关闭指定的逻辑通道，释放与 SIM 卡的会话资源。

#### 命令格式

```Bash
close-logical-channel [slot_id][session_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。
- session_id: 要关闭的逻辑通道的会话标识符（session ID）。

#### 示例

##### 命令输入

```Bash
telephonytool>close-logical-channel 0 1
```

##### 输出信息

```Bash
telephonytool> close-logical-channel 0 1
[12950.633800] [46] [ DEBUG] [ap] telephonytool_cmd_close_logical_channel, slot_id: 0 session id: 1
telephonytool> [12950.641100] [21] [  INFO] [ap] [0,0095]> RIL_REQUEST_SIM_CLOSE_CHANNEL (1,1)
[12950.642200] [15] [  INFO] [ap] [AT_RIL] onRequest: 116<->SIM_CLOSE_CHANNEL, reqtype: 4
[12950.643000] [15] [  INFO] [ap] [AT_SIM] On request sim end
[12950.643500] [21] [  INFO] [ap] [0,0095]< RIL_REQUEST_SIM_CLOSE_CHANNEL
[12950.647600] [40] [ DEBUG] [ap] tele_sim_async_fun :
[12950.647800] [40] [ DEBUG] [ap] result->msg_id : 39
[12950.648000] [40] [ DEBUG] [ap] result->status : 0
[12950.648200] [40] [ DEBUG] [ap] result->arg1 : 0
[12950.648400] [40] [ DEBUG] [ap] result->arg2 : 1
```

- session_id: 输出信息中的 `session id` 表示已成功关闭的逻辑通道会话标识符。

### 16、transmit-apdu-basic-channel

#### 命令说明

`transmit-apdu-logical-channel` 命令用于通过逻辑通道向 SIM 卡发送 APDU（Application Protocol Data Unit，应用协议数据单元）命令。

#### 命令格式

```Bash
transmit-apdu-logical-channel [slot_id][session_id][pdu][len]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。
- session_id: 逻辑通道的会话标识符（session ID）。
- pdu: 要发送的 APDU 数据内容。
- len: APDU 数据的字节长度。

#### 示例

##### 命令输入

```Bash
telephonytool>transmit-apdu-logical-channel 0 1 FFF2000000 5
```

##### 输出信息

```Bash
telephonytool> transmit-apdu-logical-channel 0 1 FFF2000000 5
[12971.991700] [46] [ DEBUG] [ap] telephonytool_cmd_transmit_apdu_logical_channel, slot_id: 0 sessionid: 1 pdu: FFF****000 len: 5
telephonytool> [12972.002100] [21] [  INFO] [ap] [0,0097]> RIL_REQUEST_SIM_TRANSMIT_APDU_CHANNEL (1, 255, 242, 0, 0, 0, (null))
```

### 17、transmit-apdu-basic-channel

#### 命令说明

`transmit-apdu-basic-channel` 命令用于通过基本通道向 SIM 卡发送 APDU（Application Protocol Data Unit，应用协议数据单元）命令。

#### 命令格式

```Bash
transmit-apdu-basic-channel [slot_id][pdu][len]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。
- pdu: 要发送的 APDU 数据内容。
- len: APDU 数据的字节长度。

#### 示例

##### 命令输入

```Bash
telephonytool>transmit-apdu-basic-channel 0 A0B000010473656E669000 11
```

##### 输出信息

```Bash
telephonytool> transmit-apdu-basic-channel 0 A0B000010473656E669000 11
[12987.899500] [46] [ DEBUG] [ap] telephonytool_cmd_transmit_apdu_basic_channel, slot_id: 0 pdu: A0B0******9000 len: 11
telephonytool> [12987.929800] [21] [  INFO] [ap] [0,0098]> RIL_REQUEST_SIM_TRANSMIT_APDU_BASIC (0, 160, 176, 0, 1, 4, 73656e669000)
[12987.932900] [15] [  INFO] [ap] [AT_RIL] onRequest: 114<->SIM_TRANSMIT_APDU_BASIC, reqtype: 4
[12987.934800] [15] [  INFO] [ap] [AT_SIM] On request sim end
[12987.935700] [21] [  INFO] [ap] [0,0098]< RIL_REQUEST_SIM_TRANSMIT_APDU_BASIC (sw1=0x90,sw2=0x00)
```

### 18、get-uicc-enablement

#### 命令说明

`get-uicc-enablement` 命令用于获取 UICC（Universal Integrated Circuit Card，通用集成电路卡）应用的启用状态。

#### 命令格式

```Bash
get-uicc-enablement [slot_id]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool>get-uicc-enablement 0
```

##### 输出信息

```Bash
telephonytool> get-uicc-enablement 0
[13002.369500] [46] [ DEBUG] [ap] telephonytool_cmd_get_uicc_enablement, slotId : 0 state : 0
```

- state:
    - `0` 表示 UICC 应用未启用。
    - `1` 表示 UICC 应用已启用。

### 19、set-uicc-enablement

#### 命令说明

`set-uicc-enablement` 命令用于设置 UICC（Universal Integrated Circuit Card，通用集成电路卡）应用的启用或禁用状态。

#### 命令格式

```Bash
set-uicc-enablement [slot_id][[state]
```

- slot_id: 设置要查询的插槽，目前仅支持 `0`。
- state: 指定 UICC 应用的目标状态：
    - `0`: 禁用 UICC 应用。
    - `1`: 启用 UICC 应用。

#### 示例

##### 命令输入

```Bash
telephonytool>set-uicc-enablement 0 1
```

##### 输出信息

```Bash
telephonytool> set-uicc-enablement 0 1
[13015.089700] [46] [ DEBUG] [ap] telephonytool_cmd_set_uicc_enablement, slotId : 0 target_state: 1
telephonytool> [13015.122400] [21] [  INFO] [ap] [0,0099]> RIL_REQUEST_ENABLE_UICC_APPLICATIONS
[13015.125000] [15] [  INFO] [ap] [AT_RIL] onRequest: 208<-><unknown request>, reqtype: 4
[13015.125800] [15] [  INFO] [ap] [AT_SIM] On request sim end
[13015.126700] [21] [  INFO] [ap] [0,0099]< RIL_REQUEST_ENABLE_UICC_APPLICATIONS
[13015.128800] [21] [  INFO] [ap] [0,0100]> RIL_REQUEST_GET_UICC_APPLICATIONS_ENABLEMENT
[13015.133000] [15] [  INFO] [ap] [AT_RIL] onRequest: 209<-><unknown request>, reqtype: 4
[13015.133600] [15] [  INFO] [ap] [AT_SIM] On request sim end
[13015.134900] [21] [  INFO] [ap] [0,0100]< RIL_REQUEST_GET_UICC_APPLICATIONS_ENABLEMENT {1}
[13015.139000] [40] [ DEBUG] [ap] tele_sim_async_fun :
[13015.139300] [40] [ DEBUG] [ap] result->msg_id : 42
[13015.139500] [40] [ DEBUG] [ap] result->status : 0
[13015.139700] [40] [ DEBUG] [ap] result->arg1 : 0
[13015.139900] [40] [ DEBUG] [ap] result->arg2 : 26740

telephonytool> get-uicc-enablement 0
[13017.372400] [46] [ DEBUG] [ap] telephonytool_cmd_get_uicc_enablement, slotId : 0 state : 1
```
