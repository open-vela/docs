# SMS/CBS Commands

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/telephony/telephonytool/sms_cbs.md) \]

## I. Overview

In the NSH command line of openvela, you can enter the Console of the telephonytool command tool to perform all operations related to SMS (Short Message Service) and CBS (Cell Broadcast Service).

## II. Prerequisites

Ensure that the telephonytool tool is opened by executing the following command:

```Bash
ap> telephonytool
```

## III. Commands

### 1. send-sms

#### Description

The send-sms command is used to send short messages (SMS, Short Message Service).

#### Syntax

```Bash
send-sms [slot_id][number][text]
```

- slot_id: Specifies the slot to monitor，currently only `0` is supported.
- number: The target phone number.
- text: The content of the short message.

#### Example

##### Input

```Bash
telephonytool> send-sms 0 10086 hello
```

##### Output

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

### 2. send-data-sms

#### Description

The `send-data-sms` command is used to send a Data SMS (Short Message). A Data SMS is a special type of SMS typically used to transmit binary data or for communication between applications.

#### Syntax

```Bash
send-sms [slot_id][number][text][port]
```

- slot_id: Specifies the slot to be monitored, currently only supports `0`.
- number: The target phone number.
- text: The content of the short message.
- port: The port for sending the Data SMS.

#### Example

##### Input

```Bash
telephonytool> send-data-sms 0 10086 hello 0
```

##### Output

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

### 3. get-service-center-number

#### Description

The `get-service-center-number` command is used to retrieve the phone number of the Short Message Service Center (SMSC).

#### Syntax

```Bash
get-service-center-number [slot_id]
```

- slot_id: Specifies the slot to query, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool>get-service-center-number 0
```

##### Output

```Bash
telephonytool> get-service-center-number 0
[18090.348600] [46] [ DEBUG] [ap] telephonytool_tapi_sms_get_service_center_number, slotId : 0  smsc_addr: 10086
```

### 4. set-service-center-number

#### Description

The `set-service-center-number` command is used to set the phone number of the Short Message Service Center (SMSC).

#### Syntax

```Bash
set-service-center-number [slot_id][number]
```

- slot_id: Specifies the slot to be monitored, currently only supports `0`.
- number: The service center number.

#### Example

##### Input

```Bash
telephonytool>set-service-center-number 0 10086
```

##### Output

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

### 5. get-cell-broadcast-power

#### Description

The `get-cell-broadcast-power `command is used to get the status of the Cell Broadcast (CB) feature (enabled or disabled).

#### Syntax

```Bash
get-cell-broadcast-power [slot_id]
```

- slot_id: Specifies the slot to query, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool>get-cell-broadcast-power 0
```

##### Output

```Bash
telephonytool> get-cell-broadcast-power 0
[18233.940800] [46] [ DEBUG] [ap] telephonytool_tapi_sms_get_cell_broadcast_power, slotId : 0 state: 1
```

- state:
    - `1`: Cell Broadcast feature is enabled.
    - `0`: Cell Broadcast feature is disabled.

### 6. set-cell-broadcast-power

#### Description

The `set-cell-broadcast-power` command is used to enable or disable the Cell Broadcast (CB) feature.

#### Syntax

```Bash
set-cell-broadcast-power [slot_id][state]
```

- slot_id: Specifies the slot to be monitored, currently only supports `0`.
- state:
    - `0`: Disable Cell Broadcast reception.
    - `1`: Enable Cell Broadcast reception.

#### Example

##### Input

```Bash
telephonytool> set-cell-broadcast-power 0 1
```

##### Output

```Bash
telephonytool> set-cell-broadcast-power 0 1
[18220.629900] [46] [ DEBUG] [ap] telephonytool_tapi_sms_set_cell_broadcast_power, slotId : 0 state: 1
telephonytool> [18220.661800] [21] [  INFO] [ap] [0,0105]> RIL_REQUEST_GSM_SET_BROADCAST_SMS_CONFIG
[18220.664700] [15] [  INFO] [ap] [AT_RIL] onRequest: 90<->GSM_SET_BROADCAST_SMS_CONFIG, reqtype: 3
```

- state:
    - `1`: Cell Broadcast feature has been successfully enabled.
    - `0`: Cell Broadcast feature has been successfully disabled.

### 7. get-cell-broadcast-topics

#### Description

The `get-cell-broadcast-topics` command is used to retrieve the supported types of Cell Broadcast messages.

#### Syntax

```Bash
get-cell-broadcast-topics [slot_id]
```

- slot_id: Specifies the slot to query, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool>get-cell-broadcast-topics 0
```

##### Output

```Bash
telephonytool> get-cell-broadcast-topics 0
[18328.263700] [46] [ DEBUG] [ap] telephonytool_tapi_sms_get_cell_broadcast_topics, slotId : 0  cbs_topics: 1
```

- cbs_topics: Indicates the supported types of Cell Broadcast messages.

### 8. set-cell-broadcast-topics

#### Description

The `set-cell-broadcast-topics` command is used to set the supported types of Cell Broadcast messages.

#### Syntax

```Bash
set-cell-broadcast-topics [slot_id][topic_type]
```

- slot_id: Specifies the slot to be monitored, currently only supports `0`.
- topic_type: Specifies the type of broadcast message, such as `etws` (Earthquake and Tsunami Warning System), cmas (Commercial Mobile Alert System), etc.

#### Example

##### Input

```Bash
telephonytool> set-cell-broadcast-topics 0 1
```

##### Output

```Bash
telephonytool> set-cell-broadcast-topics 0 1
[18314.860400] [46] [ DEBUG] [ap] telephonytool_tapi_sms_set_cell_broadcast_topics, slotId : 0 cbs_topics: 1
telephonytool> [18314.898000] [21] [  INFO] [ap] [0,0106]> RIL_REQUEST_GSM_SET_BROADCAST_SMS_CONFIG
[18314.901100] [15] [  INFO] [ap] [AT_RIL] onRequest: 90<->GSM_SET_BROADCAST_SMS_CONFIG, reqtype: 3
```

- cbs_topics: Indicates the types of broadcast messages set.

### 9. copy-sms-to-sim

#### Description

The `copy-sms-to-sim` command is used to copy a short message to the SIM card.

#### Syntax

```Bash
copy-sms-to-sim [slot_id][number][text]
```

- slot_id: Specifies the slot to be monitored, currently only supports `0`.
- number: The target phone number.
- text: The content of the short message.

#### Example

##### Input

```Bash
telephonytool> copy-sms-to-sim 0 10086 hello11
```

##### Output

```Bash
telephonytool> copy-sms-to-sim 0 10086 hello11
[18362.255300] [46] [ DEBUG] [ap] telephonytool_tapi_sms_copy_message_to_sim, slotId : 0  number : 10086 text: hello11 port 0
telephonytool> [18362.292600] [21] [  INFO] [ap] pdu_len: 14
[18362.293500] [21] [  INFO] [ap] [0,0107]> RIL_REQUEST_WRITE_SMS_TO_SIM
[18362.295700] [15] [  INFO] [ap] [AT_RIL] onRequest: 63<->WRITE_SMS_TO_SIM, reqtype: 3
[18362.298600] [21] [  INFO] [ap] [0,0107]< RIL_REQUEST_WRITE_SMS_TO_SIM
```

### 10. delete-sms-from-sim

#### Description

The `delete-sms-from-sim` command is used to delete a short message from the SIM card.

#### Syntax

```Bash
delete-sms-from-sim [slot_id][index]
```

- slot_id: Specifies the slot to be monitored, currently only supports `0`.
- index: The index of the short message.

#### Example

##### Input

```Bash
telephonytool> delete-sms-from-sim 0 1
```

##### Output

```Bash
telephonytool> delete-sms-from-sim 0 1
[18398.380000] [46] [ DEBUG] [ap] telephonytool_tapi_sms_delete_message_from_sim, slotId : 0 index: 1
telephonytool> [18398.408700] [21] [  INFO] [ap] [0,0109]> RIL_REQUEST_DELETE_SMS_ON_SIM
[18398.411500] [15] [  INFO] [ap] [AT_RIL] onRequest: 64<-><unknown request>, reqtype: 3
[18398.413700] [21] [ ERROR] [ap] parcel_r_int32: parcel is too small
[18398.414300] [21] [  INFO] [ap] [0,0109]< RIL_REQUEST_DELETE_SMS_ON_SIM {0}
```
