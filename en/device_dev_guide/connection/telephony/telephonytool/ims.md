## IMS Command

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/telephony/telephonytool/ims.md) \]

## I. Overview

In the openvela NSH command line, you can use the `telephonytool` command tool to enter the Console and perform all operations related to IMS (IP Multimedia Subsystem).

## II. Prerequisites

 To open the `telephonytool`, execute the following command:

```Bash
ap> telephonytool
```

## III. Commands

### 1. enable-ims

#### Description

 The `enable-ims` command is used to enable or disable IMS (IP Multimedia Subsystem) capabilities.

#### Syntax

```Bash
enable-ims [slot_id][action]
```

- slot_id: The slot to listen to, currently only supports 0.
- action:

    - `0`： Disable IMS capability.
    - `1`： Enable IMS capability.

#### Example

##### Input

```Bash
telephonytool>enable-ims 0 1
```

##### Output

```Bash
telephonytool> enable-ims 0 1
[149517.760100] [35] [ DEBUG] [ap] telephonytool_cmd_ims_enable: slot_id: 0, action: 1
telephonytool> [149517.786400] [21] [  INFO] [ap] [0,0124]> RIL_REQUEST_IMS_REG_STATE_CHANGE (1)
[149518.064500] [25] [  INFO] [ap] [AT_NETWORK] Receive signal strength URC
```

### 2. get-ims-enabled

#### Description

 The `get-ims-enabled` command is used to retrieve the current status of the IMS (IP Multimedia Subsystem) switch.

#### Syntax

```Bash
get-ims-enabled [slot_id]
```

- slot_id: The slot to listen to, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool>get-ims-enabled 0
```

##### Information

```Bash
telephonytool> get-ims-enabled 0
[149542.284600] [35] [ DEBUG] [ap] telephonytool_cmd_get_ims_enabled: slot_id: 0, ims enable: 1
```

### 3. set-ims-cap

#### Description

 The `set-ims-cap` command is used to set the IMS (IP Multimedia Subsystem) supported service capabilities.

#### Syntax

```Bash
set-ims-cap [slot_id][cap-value]
```

- slot_id: The slot to listen to, currently only supports 0.
- cap-value: The IMS supported functionality type:
    - `1`： Voice.
    - `4`： SMS.
    - `5`： Voice & SMS.

#### Example

##### Input

```Bash
telephonytool> set-ims-cap 0 1
```

##### Output

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

### 4. listen-ims

#### Description

The `listen-ims` command is used to listen for IMS (IP Multimedia Subsystem) registration status on the specified slot, including information like signal strength and network status changes.

#### Syntax

```Bash
listen-ims [slot_id]
```

- slot_id: The slot ID to listen to, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool>listen-ims 0
```

##### Output

```Bash
telephonytool> listen-ims 0
[149573.889900] [35] [ DEBUG] [ap] telephonytool_cmd_ims_register: slot_id: 0, watch_id: 100
telephonytool>
telephonytool>
telephonytool> get-ims-enabled 0[149578.065500] [25] [  INFO] [ap] [AT_NETWORK] Receive signal .strength URC
[149578.068000] [21] [  INFO] [ap] [0,UNSOL]< UNSOL_SIGNAL_STRENGTH {gw: 99, cdma: -1, evdo: -1, lte: 99 59 2147483647 2147483647 2147483647}
```

### 5. get-ims-registration

#### Description

The `get-ims-registration` command is used to query IMS (IP Multimedia Subsystem) related information, including IMS registration status and VoLTE (Voice over LTE) status.

#### Syntax

```Bash
get-ims-registration [slot_id][action]
```

- slot_id: The slot to listen to, currently only supports `0`.
- action:
    - `0`： Query IMS information (IMS info).
    - `1`： Query IMS registration status (IMS state).
    - `2`： Query VoLTE status (VoLTE state).

#### Example

##### Input

```Bash
telephonytool>get-ims-registration 0 0
```

##### Output

```Bash
telephonytool> get-ims-registration 0 0
[149616.226900] [35] [ DEBUG] [ap] telephonytool_cmd_ims_get_registration: slot_id: 0, acton: 0
[149616.229700] [35] [ DEBUG] [ap] telephonytool_cmd_ims_get_registration: ret_info: 0, ext_info: 0
```
