# Radio/Modem Commands

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/telephony/telephonytool/radio_modem.md) \]

## I. Introduction

In the NSH command line of openvela, you can enter the Console of the telephonytool command tool to perform all operations related to modem and radio management.

## II. Prerequisites

Ensure the telephonytool is opened.

```Bash
ap> telephonytool
```

After executing the above command, enter the telephonytool console and prepare to perform related operations.

## III. Commands

### 1. list-modem

#### Description

List all available modems.

#### Syntax

```Bash
list-modem
```

#### Example

##### Input

```Bash
telephonytool> list-modem
```

##### Output

```Bash
telephonytool> [ 1050.782500] [31] [ DEBUG] [ap] modem_list_query_complete :
[ 1050.782800] [31] [ DEBUG] [ap] result->status : 0
[ 1050.783000] [31] [ DEBUG] [ap] modem found with path -> /ril_0
```

### 2. listen-modem

#### Description

Set to listen for specific modem events.

#### Syntax

```Bash
listen-modem [slot_id] [event_id]
```

- slot_id: Set the slot to listen to, currently only `0` is supported.
- event_id: The event ID to listen to.

#### Supported Event ID List

`event_id` is used to specify the event to listen to. The following are the supported event categories and their corresponding event IDs.

1. Generic Events (Generic Indication Message)

    - `MSG_RADIO_STATE_CHANGE_IND` = 0
    - `MSG_PHONE_STATE_CHANGE_IND`
    - `MSG_OEM_HOOK_RAW_IND`
    - `MSG_MODEM_RESTART_IND`
    - `MSG_DEVICE_INFO_CHANGE_IND`
    - `MSG_AIRPLANE_MODE_CHANGE_IND`

2. Call Events (Call Indication Message)

    - `MSG_CALL_STATE_CHANGE_IND`：Call state change notification
    - `MSG_CALL_RING_BACK_TONE_IND`：Ringback tone notification
    - `MSG_ECC_LIST_CHANGE_IND`：Emergency call list change notification
    - `MSG_DEFAULT_VOICECALL_SLOT_CHANGE_IND`：Default voice call slot change notification

3. Network Events (Network Indication Message)

    - `MSG_NETWORK_STATE_CHANGE_IND`
    - `MSG_VOICE_REGISTRATION_STATE_CHANGE_IND`
    - `MSG_CELLINFO_CHANGE_IND`
    - `MSG_SIGNAL_STRENGTH_CHANGE_IND`
    - `MSG_NITZ_STATE_CHANGE_IND`

4. Data Events (Data Indication Message)

    - `MSG_DATA_ENABLED_CHANGE_IND`
    - `MSG_DATA_REGISTRATION_STATE_CHANGE_IND`
    - `MSG_DATA_NETWORK_TYPE_CHANGE_IND`
    - `MSG_DATA_CONNECTION_STATE_CHANGE_IND`
    - `MSG_DEFAULT_DATA_SLOT_CHANGE_IND`

5. SIM Card Events (SIM Indication Message)

    - `MSG_SIM_STATE_CHANGE_IND`
    - `MSG_SIM_UICC_APP_ENABLED_CHANGE_IND`
    - `MSG_SIM_ICCID_CHANGE_IND`

6. STK Events (STK Indication Message)

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

7. SMS Events (SMS Indication Message)

    - `MSG_INCOMING_MESSAGE_IND`
    - `MSG_IMMEDIATE_MESSAGE_IND`
    - `MSG_STATUS_REPORT_MESSAGE_IND`
    - `MSG_DEFAULT_SMS_SLOT_CHANGED_IND`

8. CBS Events (CBS Indication Message)

    - `MSG_INCOMING_CBS_IND`
    - `MSG_EMERGENCY_CBS_IND`

9. SS Events (SS Indication Message)

    - `MSG_CALL_BARRING_PROPERTY_CHANGE_IND`
    - `MSG_USSD_NOTIFICATION_RECEIVED_IND`
    - `MSG_USSD_REQUEST_RECEIVED_IND`
    - `MSG_USSD_PROPERTY_CHANGE_IND`

10. IMS Events (IMS Indication Message)

    - `MSG_IMS_REGISTRATION_MESSAGE_IND`

11. Modem State Change Events (Modem State Change Message)

    - `MSG_MODEM_STATE_CHANGE_IND`

12. Other Events

    - `MSG_DATA_LOGING_IND`
    - `MSG_MODEM_ECC_LIST_CHANGE_IND` = 61

#### Example

##### Input

```Bash
telephonytool> listen-modem 0 0
```

##### Output

```Bash
telephonytool> listen-modem 0 0
[ 1632.199400] [35] [ DEBUG] [ap] start to watch radio event : 0 , return watch_id : 75
```

### 3. unlisten-modem

#### Description

Stop listening to specified modem events.

#### Syntax

```Bash
unlisten-modem [watch_id]
```

- watch_id：Listen ID, derived from the return value of the `listen-modem` command.

#### Example

##### Input

```Bash
telephonytool> unlisten-modem 75
```

##### Output

Complete example of executing the `unlisten-modem` command:

```Bash
telephonytool> listen-modem 0 0
[ 1632.199400] [35] [ DEBUG] [ap] start to watch radio event : 0 , return watch_id : 75
telephonytool> unlisten-modem 75
[ 2050.331400] [35] [ DEBUG] [ap] stop to watch radio event with watch_id : 75 with return value : 0
telephonytool>
```

### 4. get-radio-cap

#### Description

Query modem feature support status.

#### Syntax

```Bash
get-radio-cap [feature_type]
```

- feature_type: Specifies the feature type to query.
    - `0`：Voice
    - `1`：Data
    - `2`：SMS
    - `3`：IMS (IP Multimedia Subsystem)

#### Example

##### Input

```Bash
telephonytool> get-radio-cap 0
```

##### Output

Complete example of executing the `get-radio-cap` command:

```Bash
telephonytool> get-radio-cap 0
[ 2145.490400] [35] [ DEBUG] [ap] radio feature type : 0 is supported ? 1
telephonytool> get-radio-cap 1
[ 2164.658700] [35] [ DEBUG] [ap] radio feature type : 1 is supported ? 1
```

### 5. set-radio-power

#### Description

Set the radio power state for the specified slot, corresponding to turning airplane mode off/on.

#### Syntax

```Bash
set-radio-power [slot_id][state]
```

- slot_id: Specifies the slot to set, currently only 0 is supported.
- state: Radio power state:
    - `0`： Turn radio off
    - `1`： Turn radio on

#### Example

##### Input

```Bash
telephonytool>  set-radio-power 0 0
```

##### Output

Complete example of executing the `set-radio-power` command:

```Bash
telephonytool> set-radio-power 0 0
[ 2322.660700] [35] [ DEBUG] [ap] telephonytool_cmd_set_radio_power, slotId : 0 target_state: 0
telephonytool> set-radio-power 0 1
[ 2324.918200] [35] [ DEBUG] [ap] telephonytool_cmd_set_radio_power, slotId : 0 target_state: 1
```

### 6. get-radio-power

#### Description

Get the radio power status of the specified slot.

#### Syntax

```Bash
get-radio-power [slot_id]
```

#### Example

##### Input

```Bash
telephonytool> get-radio-power 0
```

##### Output

Complete example of executing the `get-radio-power` command:

```Bash
telephonytool> get-radio-power 0
[ 2480.612100] [35] [ DEBUG] [ap] telephonytool_cmd_get_radio_power, slotId : 0 value : 1
```

### 7. set-rat-mode

#### Description

Set the Radio Access Technology (RAT) mode for the specified slot.

#### Syntax

```Bash
set-rat-mode [slot_id] [mode]
```

- slot_id: Specifies the slot to set (currently only `0` is supported)
- mode: Target network mode, supports the following values:
    - `0`：UMTS
    - `1`：GSM only
    - `2`：WCDMA only
    - `9`：LTE/GSM/WCDMA
    - `11`：LTE only
    - `12`：LTE/WCDMA

#### Example

##### Input

```Bash
telephonytool> set-rat-mode 0 9
```

##### Output

```Bash
telephonytool> set-rat-mode 0 11
[   48.155000] [35] [ DEBUG] [ap] telephonytool_cmd_set_rat_mode, slotId : 0 target_state: 11
[   53.549600] [21] [  INFO] [ap] [0,0059]> RIL_REQUEST_SET_PREFERRED_NETWORK_TYPE (11)
[   54.717700] [21] [  INFO] [ap] [0,0059]< RIL_REQUEST_SET_PREFERRED_NETWORK_TYPE
```

### 8. get-rat-mode

#### Description

Get the Radio Access Technology (RAT) mode of the specified slot.

#### Syntax

```Bash
get-rat-mode [slot_id]
```

- slot_id：Specifies the slot to query， currently only `0` is supported

#### Example

##### Input

```Bash
telephonytool> get-rat-mode 0
```

##### Output

```Bash
telephonytool> get-rat-mode 0
[  184.550000] [35] [ DEBUG] [ap] telephonytool_cmd_get_rat_mode, slotId : 0 value :11
```

### 9. get-imei

#### Description

Retrieve the device's IMEI (International Mobile Equipment Identity) information.

#### Syntax

```Bash
set-rat-mode [slot_id]
```

- slot_id：Specifies the SIM card slot to query. Currently, only slot 0 is supported.

#### Example

##### Input

```Bash
telephonytool> get-imei 0
```

##### Output

The following is a complete example of executing the `get-imei` command:

```Bash
telephonytool> get-imei 0
[  236.301900] [35] [ DEBUG] [ap] telephonytool_cmd_get_imei, slotId : 0 imei : 8674000******7199
```

### 10. get-imeisv

#### Description

Retrieve the device's IMEISV (International Mobile Equipment Identity Software Version) information.

#### Syntax

```Bash
get-imeisv [slot_id]
```

- slot_id：Specify the slot to query, currently only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-imeisv 0
```

##### Output

```Bash
telephonytool> get-imeisv 0  
[  401.567800] [35] [ DEBUG] [ap] telephonytool_cmd_get_imeisv, slotId : 0 imeisv : 8674000******7901
```

### 11. get-phone-state

#### Description

Retrieve the device's phone state information.

#### Syntax

```Bash
get-phone-state [slot_id]
```

- slot_id：Specify the slot to query, currently only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-phone-state 0
```

##### Output

```Bash
telephonytool> get-phone-state 0
[ 9427.739300] [35] [ DEBUG] [ap] telephonytool_cmd_get_phone_state, slotId : 0 state : 0
```

### 12. send-modem-power

#### Description

Control the power state of the Modem module.

#### Syntax

```Bash
send-modem-power[slot_id] [on]
```

- slot_id：Specify the slot to operate on, currently only `0` is supported.
- on：Set the target power state of the Modem:
    - `0`： Turn off the Modem
    - `1`：Turn on the Modem

#### Example

##### Input

```Bash
telephonytool> send-modem-power 0 0
```

##### Output

The following is a complete example of executing the `send-modem-power` command:

```Bash
telephonytool> send-modem-power 0 0
[ 9461.379300] [35] [ DEBUG] [ap] telephonytool_cmd_send_modem_power, slotId : 0 target_state: 0
telephonytool> [ 9461.415300] [21] [  INFO] [ap] modem_change_state, old state: 2, new state: 0
[ 9461.415900] [21] [  INFO] [ap] flush_atoms
[ 9461.421100] [21] [  INFO] [ap] free_contexts
```

### 13. get-radio-state

#### Description

Retrieve the device's radio (Radio) state information.

#### Syntax

```Bash
get-radio-state [slot_id]
```

- slot_id：Specify the slot to query, currently only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-radio-state 0
```

##### Output

The following is a complete example of executing the `get-radio-state` command:

```Bash
telephonytool> get-radio-state 0
[ 9486.517900] [35] [ DEBUG] [ap] telephonytool_cmd_get_radio_state, slotId : 0 state : 1
```

### 14. get-modem-revision

#### Description

Retrieve the Modem's baseband version information.

#### Syntax

```Bash
get-modem-revision [slot_id]
```

- slot_id：Specify the slot to query, currently only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-modem-revision 0
```

##### Output

The following is a complete example of executing the `get-modem-revision` command:

```Bash
telephonytool> get-modem-revision 0
[ 9505.417900] [35] [ DEBUG] [ap] telephonytool_cmd_get_modem_revision, slotId : 0 value : 1.0.*.*  
```

### 15. get-msisdn

#### Description

Get local phone number information

#### Syntax

```Bash
get-msisdn [slot_id]
```

- slot_id：Specify the slot to query, currently only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-msisdn 0
```

##### Output

The following is a complete example of executing the `get-msisdn` command:

```Bash
telephonytool> get-msisdn 0
[ 9529.024200] [35] [  INFO] [ap] get phone number from UICC.
[ 9529.025200] [35] [ DEBUG] [ap] telephonytool_cmd_get_phone_number, slotId : 0  number : +1555******67
```

### 16. get-modem-activity-info

#### Description

Retrieve the Modem's activity information.

#### Syntax

```Bash
get-modem-activity-info [slot_id]
```

- slot_id: Specify the slot to query, currently only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-modem-activity-info 0
```

##### Output

The following is a complete example of executing the `get-modem-activity-info` command:

```Bash
telephonytool> get-modem-activity-info 0
[ 9743.317300] [35] [ DEBUG] [ap] telephonytool_cmd_get_modem_activity_info, slotId : 0
```

### 17. enable-modem

#### Description

Enable or disable the Modem.

#### Syntax

```Bash
enable-modem[slot_id] [state]
```

- slot_id：Specify the slot to operate on, currently only `0` is supported.
- state：Set the target power state of the Modem:
    - `0`：Turn off the Modem
    - `1`：Turn on the Modem

#### Example

##### Input

```Bash
telephonytool> enable-modem 0 1
```

##### Output

The following is a complete example of executing the `enable-modem` command:

```Bash
telephonytool> enable-modem 0 1
[   15.700700] [28] [ DEBUG] [ap] telephonytool_cmd_enable_modem, slotId : 0 target_state: 1
```

### 18. get-modem-status

#### Description

Retrieve the Modem's status information.

#### Syntax

```Bash
get-modem-status [slot_id]
```

- slot_id：Specify the slot to query, currently only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-modem-status 0
```

##### Output

The following is a complete example of executing the `get-modem-status` command:

```Bash
telephonytool> get-modem-status 0
[  782.186200] [28] [ DEBUG] [ap] telephonytool_cmd_get_modem_status, slotId : 0
```

### 19. oem-req-raw

#### Description

Send formatted hexadecimal characters directly to the Modem for operations such as eSIM file download, eSIM file content reading, etc.

#### Syntax

```Bash
oem-req-raw [slot_id][request_data][data_length]
```

- slot_id：Specify the slot to operate on, currently only `0` is supported.
- request_data：16 Hexadecimal string representing the raw data to be sent.
- data_length：The number of bytes in `request_data`.

#### Example

##### Input

```Bash
telephonytool> oem-req-raw 0 01A0B023 4
```

##### Output

```Bash
telephonytool> oem-req-raw 0 01A0B023 4
[  854.969700] [28] [ DEBUG] [ap] telephonytool_cmd_oem_ril_req_raw, slot_id: 0 oem_req: 01A0B023 length: 4
```

### 20. oem-req-strings

#### Description

Send a string directly to the Modem, such as an AT command.

#### Syntax

```Bash
 oem-req-strings [slot_id][request_data][data_length]
```

- slot_id: Specify the slot to operate on, currently only `0` is supported.
- request_data: The string to send, such as an AT command.
- data_length: The number of bytes in request_data.

#### Example

##### Input

```Bash
telephonytool> oem-req-strings 0 AT+CPIN? 1
```

##### Output

```Bash
telephonytool> oem-req-strings 0 AT+CPIN? 1
[  870.751200] [28] [ DEBUG] [ap] telephonytool_cmd_oem_ril_req_strings, slot_id: 0 length: 1
```

### 21. send-command

#### Description

Send an internal RIL (Radio Interface Layer) message directly.

#### Syntax

```Bash
send-command [slot_id][atom id][ril request id]
```

- slot_id: Specify the slot to operate on, currently only `0` is supported.
- atom_id: Atom ID information used to identify the target module.
- ril_request_id: Internal Request ID used to specify the request type.

#### Example

##### Input

```Bash
telephonytool> send-command 0 16 57
```

##### Output

```Bash
telehonytool>
telephonytool> send-command 0 16 57
[  882.733000] [28] [ DEBUG] [ap] telephonytool_cmd_send_command, slot_id: 0 atom: 16  command: 57
```

### 22. send-screen-state

#### Description

Set the screen power state information to the modem.

#### Syntax

```Bash
send-screen-state [slot_id][][screen_state]
```

- slot_id: Specify the slot to operate on, currently only `0` is supported.
- screen_state: The screen state:
    - `0`： Screen off
    - `1`： Screen on

#### Example

##### Input

```Bash
telephonytool> send-screen-state 0 1
```

##### Output

```Bash
telephonytool>
telephonytool> send-screen-state 0 1
telephonytool> [  927.719000] [21] [  INFO] [ap] Set fast_dormancy: 1
```
