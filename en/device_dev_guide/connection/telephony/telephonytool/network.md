# Network Commands

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/telephony/telephonytool/network.md) \]

## I. Overview

In the NSH command line of openvela, you can perform all network-related operations by accessing the Console of the telephonytool command tool.

## II. Prerequisites

Ensure that the `telephonytool` tool is opened by executing the following command:

```Bash
ap> telephonytool
```

## III. Commands

### 1. listen-network

#### Description

The `listen-network` command is used to register for listening to network-related events.

#### Syntax

```Bash
listen-network [slot_id][event_id]
```

- slot_id: Sets the slot to listen to, currently only supports `0`.
- event_id: Event ID; supports the following event types:
    - `MSG_NETWORK_STATE_CHANGE_IND`：Indicates a change in network state.
    - `MSG_VOICE_REGISTRATION_STATE_CHANGE_IND`：Indicates a change in voice registration state.
    - `MSG_CELLINFO_CHANGE_IND`：Indicates a change in cell information.
    - `MSG_SIGNAL_STRENGTH_CHANGE_IND`：Indicates a change in signal strength.
    - `MSG_NITZ_STATE_CHANGE_IND`：Indicates a change in NITZ (Network Identity and Time Zone) status.

#### Example

##### Input

```Bash
telephonytool>listen-network 0 18
```

##### Output

```Bash
telephonytool> listen-network 0 18
[21503.829200] [46] [ DEBUG] [ap] start to watch network event : 18 , return watch_id : 198
```

### 2. unlisten-network

#### Description

The `unlisten-network` command is used to cancel listening to network-related events.

#### Syntax

```Bash
unlisten-network [watch_id]
```

- watch_id：Corresponds to the return value of the `listen-network` command, used to identify the event to stop listening to.

#### Example

##### Input

```Bash
telephonytool> 
```

##### Output

```Bash
telephonytool> unlisten-network 198
[21522.399100] [46] [ DEBUG] [ap] stop to watch network event with watch_id : 198 with return value : 0
```

### 3. register-auto

#### Description

The `register-auto` command sets the device to automatic network selection mode.

#### Syntax

```Bash
register-auto [slot_id]
```

- slot_id：Sets the slot to listen to, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool>register-auto 0
```

##### Output

```Bash
telephonytool> register-auto 0
[21549.525700] [46] [ DEBUG] [ap] telephonytool_cmd_network_select_auto, slotId : 0 value :0
telephonytool> [21549.532800] [21] [  INFO] [ap] [0,0110]> RIL_REQUEST_SET_NETWORK_SELECTION_AUTOMATIC
[21549.534000] [15] [  INFO] [ap] [AT_RIL] onRequest: 46<->SET_NETWORK_SELECTION_AUTOMATIC, reqtype: 6
```

### 4. register-manual

#### Description

The `register-manual` command sets the device to manual network selection mode.

#### Syntax

```Bash
 register-manual [slot_id][mcc][mnc][technology]
```

- slot_id: Sets the slot to listen to, currently only supports `0`.
- mcc: Mobile Country Code.
- mnc: Mobile Network Code.
- technology: Radio Access Technology (RAT), such as `lte`.

#### Example

##### Input

```Bash
telephonytool>register-manual 0 460 00 lte
```

##### Output

```Bash
telephonytool> register-manual 0 460 00 lte
telephonytool> [   23.514600] [21] [  INFO] [ap] [0,0079]> RIL_REQUEST_SET_NETWORK_SELECTION_MANUAL (46000)
[   24.438000] [15] [  INFO] [ap] [AT_RIL] onRequest: 47<->SET_NETWORK_SELECTION_MANUAL, reqtype: 6
```

### 5. get-signalstrength

#### Description

The `get-signalstrength` command is used to retrieve the signal strength information of the device.

#### Syntax

```Bash
get-signalstrength [slot_id]
```

- slot_id：Sets the slot to listen to, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool> get-signalstrength 0
```

##### Output

```Bash
telephonytool> get-signalstrength 0
[   53.030000] [35] [ DEBUG] [ap] telephonytool_cmd_query_signalstrength, slotId : 0 rssi :2147483647 rsrp :-68 rsrq :2147483647 rssnr :2147483647 cqi : 2147483647 level :4
```

### 6. get-display-name

#### Description

The `get-display-name` command retrieves the name of the current roaming network operator.

#### Syntax

```Bash
get-display-name [slot_id]
```

- slot_id：Sets the slot to listen to, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool>get-display-name 0
```

##### Output

```Bash
get-display-name 0
[   76.929700] [35] [ DEBUG] [ap] telephonytool_cmd_get_operator_name, slotId : 0 value :
```

### 7. get-registration-info

#### Description

The `get-registration-info` command is used to retrieve the network registration information of the device.

#### Syntax

```Bash
get-registration-info [slot_id]
```

- slot_id：Sets the slot to listen to, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool> get-registration-info 0
```

##### Output

```Bash
get-registration-info 0
telephonytool> [   96.809800] [31] [ DEBUG] [ap] network_event_callback :
[   96.810200] [31] [ DEBUG] [ap] reg_state = 4 operator_name =  mcc =  mnc =
```

### 8. get-voice-nwtype

#### Description

The `get-voice-nwtype` command retrieves the network type of the CS (Circuit Switched) domain.

#### Syntax

```Bash
get-voice-nwtype [slot_id]
```

- slot_id：Sets the slot to listen to, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool>get-voice-nwtype 0
```

##### Output

```Bash
get-voice-nwtype 0
[  117.115200] [35] [ DEBUG] [ap] telephonytool_cmd_get_voice_networktype, slotId : 0 value :0
```

### 9. get-voice-registered

#### Description

The `get-voice-registered` command retrieves the registration status of the CS (Circuit Switched) domain.

#### Syntax

```Bash
get-voice-registered [slot_id]
```

- slot_id：Sets the slot to listen to, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool> get-voice-registered 0
```

##### Output

```Bash
telephonytool> get-voice-registered 0
[  131.299100] [35] [ DEBUG] [ap] telephonytool_cmd_is_voice_registered, slotId : 0 value :0
```

### 10. get-voice-roaming

#### Description

The `get-voice-roaming` command is used to retrieve the roaming status in the CS (Circuit Switched) domain.

#### Syntax

```Bash
get-voice-roaming [slot_id]
```

- slot_id：Specifies the slot to be monitored, currently supports only `0`.

#### Example

##### Input

```Bash
telephonytool>get-voice-roaming 0
```

##### Output

```Bash
telephonytool> get-voice-roaming 0
[  149.630700] [35] [ DEBUG] [ap] telephonytool_cmd_is_voice_roaming, slotId : 0 value :0
```

### 11. scan-network

#### Description

The `scan-network` command initiates a network scan to query the currently available networks.

#### Syntax

```Bash
scan-network [slot_id]
```

- slot_id：Specifies the slot to be monitored, currently supports only `0`.

#### Example

##### Input

```Bash
telephonytool>scan-network 0
```

##### Output

```Bash
telephonytool> scan-network 0
telephonytool> [  161.901900] [21] [  INFO] [ap] [0,0087]> RIL_REQUEST_QUERY_AVAILABLE_NETWORKS
[  161.906400] [15] [  INFO] [ap] [AT_RIL] onRequest: 48<->QUERY_AVAILABLE_NETWORKS , reqtype: 6
```

### 12. get-serving-cellinfo

#### Description

The `get-serving-cellinfo` command is used to obtain information related to the current serving cell.

#### Syntax

```Bash
get-serving-cellinfo [slot_id]
```

- slot_id：Specifies the slot to be monitored, currently supports only `0`.

#### Example

##### Input

```Bash
telephonytool>get-serving-cellinfo 0
```

##### Output

```Bash
telephonytool> get-serving-cellinfo 0
telephonytool> [  175.409900] [21] [  INFO] [ap] [0,0088]> RIL_REQUEST_GET_CELL_INFO_LIST
[  175.414500] [15] [  INFO] [ap] [AT_RIL] onRequest: 109<->GET_CELL_INFO_LIST, reqtype: 6
[  175.417500] [21] [  INFO] [ap] [0,0088]< RIL_REQUEST_GET_CELL_INFO_LIST cell_info_cnt = 1 {type = 1, registered = 1, mcc = 311, mnc = 740, lac = 8514, ci = 47108, strength = 0, ber = 1}
```

### 13. get-neighbouring-cellInfos

#### Description

The `get-neighbouring-cellInfos` command is used to retrieve information about neighboring cells.

#### Syntax

```Bash
get-neighbouring-cellInfos [slot_id]
```

- slot_id：Specifies the slot to be monitored, currently supports only `0`.

#### Example

##### Input

```Bash
telephonytool>get-neighbouring-cellInfos 0
```

##### Output

```Bash
telephonytool> get-neighbouring-cellInfos 0
telephonytool> [  192.285200] [21] [  INFO] [ap] [0,0089]> RIL_REQUEST_GET_NEIGHBORING_CELL_IDS
[  192.286100] [15] [  INFO] [ap] [AT_RIL] onRequest: 75<->GET_NEIGHBORING_CELL_IDS, reqtype: 6
[  192.286700] [21] [ ERROR] [ap] parcel_r_int32: parcel is too small
[  192.286900] [21] [  INFO] [ap] [0,0089]< RIL_REQUEST_GET_NEIGHBORING_CELL_IDS cell_info_cnt = 2 {type = 90, registered = 4, mcc = 091, mnc = 04, {type = 3145778, registered = 3473458, mcc = 000, mnc = 00,
[  192.300600] [31] [ DEBUG] [ap] ci : 0, mcc : 091, mnc : 04, registered : 1, type : 101,
[  192.300900] [31] [ DEBUG] [ap] ci : 0, mcc : 000, mnc : 00, registered : 1, type : 0,
```

### 14. set-cell-info-list-rate

#### Description

The `set-cell-info-list-rate` command is used to set the update rate for cell information.

#### Syntax

```Bash
set-cell-info-list-rate [slot_id][period]
```

- slot_id：Specifies the slot to be monitored, currently supports only `0`.
- period：Update rate in seconds.

#### Example

##### Input

```Bash
telephonytool>set-cell-info-list-rate 0 10
```

##### Output

```Bash
telephonytool> set-cell-info-list-rate 0 10
[  209.176900] [35] [ DEBUG] [ap] telephonytool_cmd_set_cell_info_list_rate, slot_id: 0 period: 10
telephonytool> [  209.201300] [21] [  INFO] [ap] [0,0090]> RIL_REQUEST_SET_UNSOL_CELL_INFO_LIST_RATE
[  209.205100] [15] [  INFO] [ap] [AT_RIL] onRequest: 110<->SET_UNSOL_CELL_INFO_LIST_RATE, reqtype: 6
```
