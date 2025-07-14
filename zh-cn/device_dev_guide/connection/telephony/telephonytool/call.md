# call 命令

\[ [English](../../../../../en/device_dev_guide/connection/telephony/telephonytool/call.md) | 简体中文 \]

## 一、概述

在 openvela 的 NSH 命令行中，可以通过进入 telephonytool 命令工具的 Console，来执行所有与呼叫控制相关的操作。

## 二、前提条件

确保已打开 `telephonytool`，执行如下命令：

```Bash
ap> telephonytool
```

## 三、命令

### 1、listen-call

#### 命令说明

`listen-call` 用于监听呼叫状态变化、紧急号码变化以及回铃音变化等信息。

#### 命令格式

```Bash
listen-call [slot_id][event_id]
```

- slot_id: 设置要监听的插槽，目前仅支持 `0`。
- event_id:
    - `0`: 呼叫状态变化（call state change）。
    - `1`: 紧急号码列表变化（ecc list change）。
    - `2`: 回铃音变化（ringback tone change）。

#### 示例

##### 命令输入

```Bash
telephonytool> listen-call 0 1
```

##### 输出信息

```Bash
telephonytool>  listen-call 0 1
[12797.466700] [28] [ DEBUG] [ap] telephonytool_cmd_listen_call_manager_change, slot_id : 0, event_id : 1, watch_id : 95
```

### 2、unlisten-call

#### 命令说明

`unlisten-call` 用于取消监听呼叫状态变化、紧急号码变化以及回铃音变化等信息。

#### 命令格式

```Bash
unlisten-call [watch_id]
```

- watch_id: 对应 `listen-call` 命令的返回值，用于标识需要取消监听的事件。

#### 示例

##### 命令输入

```Bash
telephonytool> unlisten-call 95
```

##### 输出信息

```Bash
telephonytool> unlisten-call 95
[12820.712800] [28] [ DEBUG] [ap] stop to watch call event with watch_id : 95 with return value : 0
```

### 3、listen-call-slot-change

#### 命令说明

`listen-call-slot-change` 用于监听呼叫插槽（call slot）的变化。

#### 命令格式

```Bash
listen-call-slot-change
```

#### 示例

##### 命令输入

```Bash
telephonytool> listen-call-slot-change
```

##### 输出信息

```Bash
telephonytool> listen-call-slot-change
[12935.086700] [28] [ DEBUG] [ap] telephonytool_cmd_listen_call_slot_change, , watch_id : 96
```

### 4、dial

#### 命令说明

`dial` 命令用于发起电话请求。

#### 命令格式

```Bash
dial [slot_id][number][hide_call_id]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。
- number: 要拨打的电话号码。
- hide_call_id: 是否隐藏本机号码：
    - `0`: 显示本机号码（show）。
    - `1`: 隐藏本机号码（hide）。

#### 示例

##### 命令输入

```Bash
telephonytool> dial 0 10086 0
```

##### 输出信息

```Bash
telephonytool> dial 0 10086 0
[13153.728500] [28] [ DEBUG] [ap] telephonytool_cmd_dial, slot_id: 0 number: 10086  hide_callerid: 0
[13153.730700] [28] [ DEBUG] [ap] OFONO_DFX_CALL_INFO:1,1,1,0,NA
[13170.772100] [21] [  INFO] [ap] [0,0087]> RIL_REQUEST_DIAL (***,0,0,0)
```

### 5、answer_0

#### 命令说明

接听来电

#### 命令格式

```Bash
answer_0 [slot_id] [call_id]
slot_id:设置要监听的slot,当前只支持0
call_id:来电的call id信息
```

#### 示例

##### 命令输入

```Bash
telephonytool> answer_0 0 /ril_0/voicecall01
```

##### 输出信息

```Bash
telephonytool> answer_0  0  /ril_0/voicecall01
[  187.166200] [28] [ DEBUG] [ap] telephonytool_cmd_answer_by_id, slotId : 0
```

### 6、hangup_0

#### 命令说明

`hangup_0` 命令用于挂断电话。

#### 命令格式

```Bash
hangup_0 [slot_id][call_id] 
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。
- call_id: 呼叫的 ID 信息，用于指定要挂断的电话。

#### 示例

##### 命令输入

```Bash
telephonytool> hangup_0 0 /ril_0/voicecall01
```

##### 输出信息

```Bash
telephonytool> hangup_0 0 /ril_0/voicecall01
[  309.834700] [28] [ DEBUG] [ap] telephonytool_cmd_hangup_by_id, slotId : 0
```

### 7、release_and_answer

#### 命令说明

`release_and_answer` 命令用于释放当前正在进行的电话，并接通最新的来电。

#### 命令格式

```Bash
release_and_answer [slot_id]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> release_and_answer 0
```

##### 输出信息

```Bash
telephonytool> release_and_answer 0
[55124.855300] [28] [ DEBUG] [ap] telephonytool_cmd_release_and_answer_call, slotId : 0
```

### 8、hold_and_answer

#### 命令说明

`hold_and_answer` 命令用于将当前正在进行的电话置于保持状态，并接通最新的来电。

#### 命令格式

```Bash
hold_and_answer [slot_id]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> hold_and_answer 0
```

##### 输出信息

```Bash
telephonytool> hold_and_answer 0
[57690.627700] [28] [ DEBUG] [ap] telephonytool_cmd_hold_and_answer_call, slotId : 0
[57690.628200] [28] [ DEBUG] [ap] OFONO_DFX_CALL_INFO:1,2,1,0,NA:HoldAndAnswer
```

### 9、release_and_swap

#### 命令说明

`release_and_swap` 命令用于挂断当前正在进行的通话，并将处于保持状态的通话切换为活动通话。

#### 命令格式

```Bash
release_and_swap [slot_id]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> release_and_swap 0
```

##### 输出信息

```Bash
release_and_swap 0
[57714.464400] [28] [ DEBUG] [ap] telephonytool_cmd_release_and_swap_call, slotId : 0
telephonytool> [57714.489500] [21] [  INFO] [ap] [0,0087]> RIL_REQUEST_HANGUP_FOREGROUND_RESUME_BACKGROUND
[57714.493900] [15] [  INFO] [ap] [AT_RIL] onRequest: 14<->HANGUP_FOREGROUND_RESUME_BACKGROUND, reqtype: 2
[57714.502300] [21] [  INFO] [ap] [0,0087]< RIL_REQUEST_HANGUP_FOREGROUND_RESUME_BACKGROUND
```

### 10、swap

#### 命令说明

切换call的状态，从active call切换hold call或者从hold call切换到active call

`swap` 命令用于切换通话状态：

- 从活动通话（active call）切换到保持通话（hold call）。
- 或从保持通话（hold call）切换到活动通话（active call）。

#### 命令格式

```Bash
swap [slot_id][action]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。
- action: 指定切换操作：
    - `1`: 切换到保持通话（hold call）。
    - `0`: 切换到活动通话（unhold call）。

#### 示例

##### 命令输入

```Bash
telephonytool> swap 0 1 
```

##### 输出信息

```Bash
telephonytool>  swap 0 1
[57750.186200] [28] [ DEBUG] [ap] telephonytool_cmd_swap_call, slotId : 0
telephonytool> [57750.211600] [21] [  INFO] [ap] [0,0089]> RIL_REQUEST_SWITCH_HOLDING_AND_ACTIVE
[57750.215900] [15] [  INFO] [ap] [AT_RIL] onRequest: 15<->SWITCH_WAITING_OR_HOLDING_AND_ACTIVE, reqtype: 2
[57750.218900] [21] [  INFO] [ap] [0,0089]< RIL_REQUEST_SWITCH_HOLDING_AND_ACTIVE
```

### 11、hangup-all

#### 命令说明

`hangup-all` 命令用于挂断所有存在的通话，包括后台通话（background call）。

#### 命令格式

```Bash
 hangup-all [slot_id]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> hangup-all 0 
```

##### 输出信息

```Bash
telephonytool> hangup-all 0
[57768.041500] [28] [ DEBUG] [ap] telephonytool_cmd_hangup_all, slotId : 0
[57768.043500] [28] [ DEBUG] [ap] OFONO_DFX_CALL_INFO:4,3,3,0,NA
```

### 12、get-call

#### 命令说明

`get-call` 命令用于获取当前所有通话的信息。

#### 命令格式

```Bash
get-call [slot_id]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-call 0
```

##### 输出信息

```Bash
telephonytool> get-call 0
telephonytool_cmd_get_call
telephonytool> [57791.194300] [27] [ DEBUG] [ap] call_list_query_complete :
[57791.194600] [27] [ DEBUG] [ap] call count: 1

[57791.194900] [27] [ DEBUG] [ap] call id: /ril_0/voicecall03
[57791.195300] [27] [ DEBUG] [ap] call state: 2
[57791.195500] [27] [ DEBUG] [ap] call LineIdentification: 10086
[57791.195900] [27] [ DEBUG] [ap] call IncomingLine:
[57791.196200] [27] [ DEBUG] [ap] call Name:
[57791.196500] [27] [ DEBUG] [ap] call StartTime:
[57791.196800] [27] [ DEBUG] [ap] call Multiparty: 0
[57791.197100] [27] [ DEBUG] [ap] call RemoteHeld: 0
[57791.197400] [27] [ DEBUG] [ap] call RemoteMultiparty: 0
[57791.197700] [27] [ DEBUG] [ap] call Information:
[57791.198000] [27] [ DEBUG] [ap] call Icon: 0
[57791.198200] [27] [ DEBUG] [ap] call Emergency: 0
```

### 13、transfer

#### 命令说明

`transfer` 命令用于将当前正在进行的通话转移到另一个设备。此功能依赖网络支持。

#### 命令格式

```Bash
transfer [slot_id]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> transfer 0
```

##### 输出信息

```Bash
telephonytool> transfer 0
[57861.765100] [28] [ DEBUG] [ap] telephonytool_cmd_transfer_call, slotId : 0
```

### 14、get-ecclist

#### 命令说明

`get-ecclist` 命令用于获取所有紧急号码的信息。

#### 命令格式

```Bash
get-ecclist [slot_id]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> get-ecclist 0
```

##### 输出信息

```Bash
telephonytool> get-ecclist 0
[57889.833100] [28] [ DEBUG] [ap] telephonytool_cmd_get_ecc_list, slotId : 0
[57889.835500] [28] [ DEBUG] [ap] tapi_call_get_ecc_list info:911,0,1
[57889.836900] [28] [ DEBUG] [ap] tapi_call_get_ecc_list info:112,0,1
[57889.838200] [28] [ DEBUG] [ap] ecc number : 911,0,1
[57889.839500] [28] [ DEBUG] [ap] ecc number : 112,0,1
```

### 15、is-ecc

#### 命令说明

`is-ecc` 命令用于检查某个电话号码是否为紧急号码。

#### 命令格式

```Bash
is-ecc [number]
```

- number: 要检查的电话号码。

#### 示例

##### 命令输入

```Bash
telephonytool> is-ecc 110
```

##### 输出信息

```Bash
telephonytool> is-ecc 110
[57906.267200] [28] [ DEBUG] [ap] tapi_call_get_ecc_list info:911,0,1
[57906.269300] [28] [ DEBUG] [ap] tapi_call_get_ecc_list info:112,0,1
[57906.270700] [28] [ DEBUG] [ap] telephonytool_cmd_is_emergency_number, ret : -1
```

### 16、send-tones

#### 命令说明

`send-tones` 命令用于发送预置的 DTMF（Dual-Tone Multi-Frequency）命令。

#### 命令格式

```Bash
send-tones [slot_id][dtmf]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。
- dtmf: 要发送的数字（DTMF 信号）。

#### 示例

##### 命令输入

```Bash
telephonytool> send-tones 0 11
```

##### 输出信息

```Bash
telephonytool> send-tones 0 11
[58031.748600] [28] [ DEBUG] [ap] telephonytool_cmd_send_tones, slotId : 0 dtmf : 11
```

### 17、start-dtmf

#### 命令说明

`start-dtmf` 命令用于在通话过程中发送单个 DTMF（Dual-Tone Multi-Frequency）信号。

#### 命令格式

```Bash
start-dtmf [slot_id][dtmf]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。
- dtmf: 要发送的数字（DTMF 信号）。

#### 示例

##### 命令输入

```Bash
telephonytool> start-dtmf 0 1
```

##### 输出信息

```Bash
telephonytool> start-dtmf 0 1
[58070.442600] [28] [ DEBUG] [ap] telephonytool_cmd_start_dtmf, slotId : 0 dtmf : 1
telephonytool> [58070.453600] [21] [  INFO] [ap] [0,0104]> RIL_REQUEST_DTMF_START (1)
[58070.454400] [15] [  INFO] [ap] [AT_RIL] onRequest: 49<->DTMF_START, reqtype: 2
[58070.455100] [21] [  INFO] [ap] [0,0104]< RIL_REQUEST_DTMF_START
[58070.458000] [27] [ DEBUG] [ap] tele_call_async_fun :
[58070.458200] [27] [ DEBUG] [ap] result->msg_id : 114
[58070.458300] [27] [ DEBUG] [ap] result->status : 0
[58070.458500] [27] [ DEBUG] [ap] result->arg1 : 0
[58070.458600] [27] [ DEBUG] [ap] result->arg2 : 6750472
[58070.458800] [27] [ DEBUG] [ap] start dtmf , state : 0
```

### 18、stop-dtmf

#### 命令说明

`stop-dtmf` 命令用于在通话过程中停止发送 DTMF（Dual-Tone Multi-Frequency）信号。

#### 命令格式

```Bash
stop-dtmf [slot_id]
```

- slot_id: 设置要使用的插槽，目前仅支持 `0`。

#### 示例

##### 命令输入

```Bash
telephonytool> stop-dtmf 0
```

##### 输出信息

```Bash
stop-dtmf 0
[58082.923500] [28] [ DEBUG] [ap] telephonytool_cmd_stop_dtmf, slotId : 0
telephonytool> [58082.933700] [21] [  INFO] [ap] [0,0105]> RIL_REQUEST_DTMF_STOP
[58082.934400] [15] [  INFO] [ap] [AT_RIL] onRequest: 50<->DTMF_STOP, reqtype: 2
[58082.935100] [21] [  INFO] [ap] [0,0105]< RIL_REQUEST_DTMF_STOP
[58082.938100] [27] [ DEBUG] [ap] tele_call_async_fun :
[58082.938200] [27] [ DEBUG] [ap] result->msg_id : 115
[58082.938400] [27] [ DEBUG] [ap] result->status : 0
[58082.938500] [27] [ DEBUG] [ap] result->arg1 : 0
[58082.938700] [27] [ DEBUG] [ap] result->arg2 : 0
[58082.938800] [27] [ DEBUG] [ap] stop dtmf , state : 0
```
