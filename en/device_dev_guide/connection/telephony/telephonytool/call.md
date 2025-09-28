# Call Command

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/telephony/telephonytool/call.md) \]

## I. Overview

In the openvela NSH command line, you can enter the `telephonytool` console to perform all operations related to call control.

## II. Prerequisites

Ensure `telephonytool` has been started by running the following command:

```Bash
ap> telephonytool
```

## III. Commands

### 1. listen-call

#### Description

The `listen-call` command is used to monitor information such as call state changes, emergency number changes, and ringback tone changes.

#### Format

```Bash
listen-call [slot_id] [event_id]
```

- `slot_id`: The slot to monitor. Currently, only `0` is supported.
- `event_id`:

    - `0`: Call state change.
    - `1`: Emergency number list change (ecc list change).
    - `2`: Ringback tone change.

#### Example

##### Input

```Bash
telephonytool> listen-call 0 1
```

##### Output

```Bash
telephonytool>  listen-call 0 1
[12797.466700] [28] [ DEBUG] [ap] telephonytool_cmd_listen_call_manager_change, slot_id : 0, event_id : 1, watch_id : 95
```

### 2. unlisten-call

#### Description

The `unlisten-call` command is used to stop monitoring call state changes, emergency number changes, and ringback tone changes.

#### Format

```Bash
unlisten-call [watch_id]
```

- `watch_id`: The ID returned by the `listen-call` command, which identifies the event to stop monitoring.

#### Example

##### Input

```Bash
telephonytool> unlisten-call 95
```

##### Output

```Bash
telephonytool> unlisten-call 95
[12820.712800] [28] [ DEBUG] [ap] stop to watch call event with watch_id : 95 with return value : 0
```

### 3. listen-call-slot-change

#### Description

The `listen-call-slot-change` command is used to monitor changes in the call slot.

#### Format

```Bash
listen-call-slot-change
```

#### Example

##### Input

```Bash
telephonytool> listen-call-slot-change
```

##### Output

```Bash
telephonytool> listen-call-slot-change
[12935.086700] [28] [ DEBUG] [ap] telephonytool_cmd_listen_call_slot_change, , watch_id : 96
```

### 4. dial

#### Description

The `dial` command is used to initiate a phone call.

#### Format

```Bash
dial [slot_id] [number] [hide_call_id]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.
- `number`: The phone number to dial.
- `hide_call_id`: Specifies whether to hide the caller ID:

    - `0`: Show caller ID.
    - `1`: Hide caller ID.

#### Example

##### Input

```Bash
telephonytool> dial 0 10086 0
```

##### Output

```Bash
telephonytool> dial 0 10086 0
[13153.728500] [28] [ DEBUG] [ap] telephonytool_cmd_dial, slot_id: 0 number: 10086  hide_callerid: 0
[13153.730700] [28] [ DEBUG] [ap] OFONO_DFX_CALL_INFO:1,1,1,0,NA
[13170.772100] [21] [  INFO] [ap] [0,0087]> RIL_REQUEST_DIAL (***,0,0,0)
```

### 5. answer_0

#### Description

Answer an incoming call.

#### Format

```Bash
answer_0 [slot_id] [call_id]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.
- `call_id`: The call ID of the incoming call.

#### Example

##### Input

```Bash
telephonytool> answer_0 0 /ril_0/voicecall01
```

##### Output

```Bash
telephonytool> answer_0  0  /ril_0/voicecall01
[  187.166200] [28] [ DEBUG] [ap] telephonytool_cmd_answer_by_id, slotId : 0
```

### 6. hangup_0

#### Description

The `hangup_0` command is used to hang up a call.

#### Format

```Bash
hangup_0 [slot_id] [call_id] 
```

- `slot_id`: The slot to use. Currently, only `0` is supported.
- `call_id`: The ID of the call to hang up.

#### Example

##### Input

```Bash
telephonytool> hangup_0 0 /ril_0/voicecall01
```

##### Output

```Bash
telephonytool> hangup_0 0 /ril_0/voicecall01
[  309.834700] [28] [ DEBUG] [ap] telephonytool_cmd_hangup_by_id, slotId : 0
```

### 7. release_and_answer

#### Description

The `release_and_answer` command releases the current active call and answers the newest incoming call.

#### Format

```Bash
release_and_answer [slot_id]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> release_and_answer 0
```

##### Output

```Bash
telephonytool> release_and_answer 0
[55124.855300] [28] [ DEBUG] [ap] telephonytool_cmd_release_and_answer_call, slotId : 0
```

### 8. hold_and_answer

#### Description

The `hold_and_answer` command puts the current active call on hold and answers the newest incoming call.

#### Format

```Bash
hold_and_answer [slot_id]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> hold_and_answer 0
```

##### Output

```Bash
telephonytool> hold_and_answer 0
[57690.627700] [28] [ DEBUG] [ap] telephonytool_cmd_hold_and_answer_call, slotId : 0
[57690.628200] [28] [ DEBUG] [ap] OFONO_DFX_CALL_INFO:1,2,1,0,NA:HoldAndAnswer
```

### 9. release_and_swap

#### Description

The `release_and_swap` command hangs up the current active call and switches the held call to active.

#### Format

```Bash
release_and_swap [slot_id]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> release_and_swap 0
```

##### Output

```Bash
release_and_swap 0
[57714.464400] [28] [ DEBUG] [ap] telephonytool_cmd_release_and_swap_call, slotId : 0
telephonytool> [57714.489500] [21] [  INFO] [ap] [0,0087]> RIL_REQUEST_HANGUP_FOREGROUND_RESUME_BACKGROUND
[57714.493900] [15] [  INFO] [ap] [AT_RIL] onRequest: 14<->HANGUP_FOREGROUND_RESUME_BACKGROUND, reqtype: 2
[57714.502300] [21] [  INFO] [ap] [0,0087]< RIL_REQUEST_HANGUP_FOREGROUND_RESUME_BACKGROUND
```

### 10. swap

#### Description

The `swap` command switches the call state:

- From an active call to a held call.
- Or from a held call to an active call.

#### Format

```Bash
swap [slot_id] [action]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.
- `action`: Specifies the swap action:

    - `1`: Switch to hold call.
    - `0`: Switch to active call (unhold).

#### Example

##### Input

```Bash
telephonytool> swap 0 1 
```

##### Output

```Bash
telephonytool>  swap 0 1
[57750.186200] [28] [ DEBUG] [ap] telephonytool_cmd_swap_call, slotId : 0
telephonytool> [57750.211600] [21] [  INFO] [ap] [0,0089]> RIL_REQUEST_SWITCH_HOLDING_AND_ACTIVE
[57750.215900] [15] [  INFO] [ap] [AT_RIL] onRequest: 15<->SWITCH_WAITING_OR_HOLDING_AND_ACTIVE, reqtype: 2
[57750.218900] [21] [  INFO] [ap] [0,0089]< RIL_REQUEST_SWITCH_HOLDING_AND_ACTIVE
```

### 11. hangup-all

#### Description

The `hangup-all` command hangs up all existing calls, including background calls.

#### Format

```Bash
 hangup-all [slot_id]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> hangup-all 0 
```

##### Output

```Bash
telephonytool> hangup-all 0
[57768.041500] [28] [ DEBUG] [ap] telephonytool_cmd_hangup_all, slotId : 0
[57768.043500] [28] [ DEBUG] [ap] OFONO_DFX_CALL_INFO:4,3,3,0,NA
```

### 12. get-call

#### Description

The `get-call` command gets information about all current calls.

#### Format

```Bash
get-call [slot_id]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-call 0
```

##### Output

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

### 13. transfer

#### Description

The `transfer` command transfers the current active call to another device. This feature is network-dependent.

#### Format

```Bash
transfer [slot_id]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> transfer 0
```

##### Output

```Bash
telephonytool> transfer 0
[57861.765100] [28] [ DEBUG] [ap] telephonytool_cmd_transfer_call, slotId : 0
```

### 14. get-ecclist

#### Description

The `get-ecclist` command gets information about all emergency numbers.

#### Format

```Bash
get-ecclist [slot_id]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-ecclist 0
```

##### Output

```Bash
telephonytool> get-ecclist 0
[57889.833100] [28] [ DEBUG] [ap] telephonytool_cmd_get_ecc_list, slotId : 0
[57889.835500] [28] [ DEBUG] [ap] tapi_call_get_ecc_list info:911,0,1
[57889.836900] [28] [ DEBUG] [ap] tapi_call_get_ecc_list info:112,0,1
[57889.838200] [28] [ DEBUG] [ap] ecc number : 911,0,1
[57889.839500] [28] [ DEBUG] [ap] ecc number : 112,0,1
```

### 15. is-ecc

#### Description

The `is-ecc` command checks if a phone number is an emergency number.

#### Format

```Bash
is-ecc [number]
```

- `number`: The phone number to check.

#### Example

##### Input

```Bash
telephonytool> is-ecc 110
```

##### Output

```Bash
telephonytool> is-ecc 110
[57906.267200] [28] [ DEBUG] [ap] tapi_call_get_ecc_list info:911,0,1
[57906.269300] [28] [ DEBUG] [ap] tapi_call_get_ecc_list info:112,0,1
[57906.270700] [28] [ DEBUG] [ap] telephonytool_cmd_is_emergency_number, ret : -1
```

### 16. send-tones

#### Description

The `send-tones` command sends a predefined DTMF (Dual-Tone Multi-Frequency) command.

#### Format

```Bash
send-tones [slot_id] [dtmf]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.
- `dtmf`: The digit(s) to send as a DTMF signal.

#### Example

##### Input

```Bash
telephonytool> send-tones 0 11
```

##### Output

```Bash
telephonytool> send-tones 0 11
[58031.748600] [28] [ DEBUG] [ap] telephonytool_cmd_send_tones, slotId : 0 dtmf : 11
```

### 17. start-dtmf

#### Description

The `start-dtmf` command starts sending a single DTMF (Dual-Tone Multi-Frequency) signal during a call.

#### Format

```Bash
start-dtmf [slot_id] [dtmf]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.
- `dtmf`: The digit to send as a DTMF signal.

#### Example

##### Input

```Bash
telephonytool> start-dtmf 0 1
```

##### Output

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

### 18. stop-dtmf

#### Description

The `stop-dtmf` command stops sending the DTMF (Dual-Tone Multi-Frequency) signal during a call.

#### Format

```Bash
stop-dtmf [slot_id]
```

- `slot_id`: The slot to use. Currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> stop-dtmf 0
```

##### Output

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
