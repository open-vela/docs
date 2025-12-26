# Sim Command

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/telephony/telephonytool/sim.md) \]

## I. Overview

In the NSH command line of openvela, all operations related to the SIM card can be executed by entering the Console of the telephonytool command tool.

## II. Preconditions

Make sure the `telephonytool` is opened.

```Bash
ap> telephonytool
```

## III. Commands

### 1. listen-sim

#### Description

The `listen-sim` command is used to register for listening to events related to the SIM card.

#### Syntax

```Bash
listen-sim [slot_id][event_id]
```

- slot_id: Set the slot to listen to; currently, only `0` is supported.
- event_id: The event ID to listen for, supports the following events:
    - `MSG_SIM_STATE_CHANGE_IND`: SIM state change event.
    - `MSG_SIM_UICC_APP_ENABLED_CHANGE_IND`: SIM UICC application enabled status change event.
    - `MSG_SIM_ICCID_CHANGE_IND`: SIM ICCID (Integrated Circuit Card Identifier) change event.

#### Example

##### Input

```Bash
telephonytool> listen-sim 0 28
```

##### Output

```Bash
listen-sim 0 28
[12296.667000] [46] [ DEBUG] [ap] start to watch sim event : 28 , return watch_id : 189
```

### 2. unlisten-sim

#### Description

The `unlisten-sim`command is used to cancel listening to events related to the SIM card.

#### Syntax

```Bash
unlisten-sim [watch_id]
```

- watch_id: The corresponding return value from the `listen-sim`.

#### Example

##### Input

```Bash
telephonytool> unlisten-sim 189
```

##### Output

```Bash
telephonytool> unlisten-sim 189
[12323.192900] [46] [ DEBUG] [ap] stop to watch sim event with watch_id : 189 with return value : 0
```

### 3. has-icc

#### Description

The `has-icc` command is used to query whether there is an ICC (Integrated Circuit Card) present in the specified slot.

#### Syntax

```Bash
has-icc [slot_id]
```

- slot_id: Set the slot to query; currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> has-icc 0
```

##### Output

```Bash
telephonytool> has-icc 0
[12341.192300] [46] [ DEBUG] [ap] telephonytool_cmd_has_icc_card, slotId : 0 value : 1
```

### 4. get-sim-state

#### Description

The `get-sim-state` command is used to get the state of the SIM card in the specified slot.

#### Syntax

```Bash
get-sim-state [slot_id]
```

- slot_id: Set the slot to query; currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-sim-state 0
```

##### Output

```Bash
get-sim-state 0
[12357.230900] [46] [ DEBUG] [ap] telephonytool_cmd_get_sim_state, slotId : 0 state : SIM_READY
```

### 5. get-iccid

#### Description

The `get-iccid` command is used to obtain the ICCID (Integrated Circuit Card Identifier) information of the SIM card in the specified slot.

#### Syntax

```Bash
get-iccid [slot_id]
```

- slot_id: Set the slot to query; currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool>  get-iccid 0
```

##### Output

```Bash
telephonytool> get-iccid 0
[12378.832200] [46] [ DEBUG] [ap] telephonytool_cmd_get_sim_iccid, slotId : 0 iccid : 12345678901234567890  # sample data
```

### 6. get-sim-operator

#### Description

The `get-sim-operator` command is used to obtain the PLMN (Public Land Mobile Network) information of the SIM card in the specified slot. PLMN is an identifier composed of the operator's country code (MCC) and network code (MNC), which indicates the operator to which the SIM card belongs.

#### Syntax

```Bash
get-sim-operator [slot_id]
```

- slot_id: Set the slot to query; currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-sim-operator 0
```

##### Output

```Bash
telephonytool> get-sim-operator 0
[12795.415400] [46] [ DEBUG] [ap] telephonytool_cmd_get_sim_operator, slotId : 0 operator : 310260
```

### 7. get-sim-operator-name

#### Description

The `get-sim-operator-name` command is used to obtain the name of the SIM card's operator (SPN, Service Provider Name) in the specified slot.

#### Syntax

```Bash
get-sim-operator-name [slot_id]
```

- slot_id: Set the slot to query; currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-sim-operator-name 0
```

##### Output

```Bash
telephonytool> get-sim-operator-name 0
[12809.795600] [46] [ DEBUG] [ap] telephonytool_cmd_get_sim_operator_name, slotId : 0 spn : T-Mobile
```

### 8. get-sim-subscriber-id

#### Description

The `get-sim-subscriber-id` command is used to obtain the subscriber identifier of the SIM card in the specified slot.

#### Syntax

```Bash
get-sim-subscriber-id [slot_id]
```

- slot_id: Set the slot to query; currently, only `0` is supported.

#### Example

##### Input

```Bash
telephonytool> get-sim-subscriber-id 0
```

##### Output

```Bash
telephonytool> get-sim-subscriber-id 0
[12824.331100] [46] [ DEBUG] [ap] telephonytool_cmd_get_sim_subscriber_id, slotId : 0 subscriber_id : 310260000000000
```

### 9. change-pin

#### Description

The `change-pin` command is used to modify the PIN (Personal Identification Number) of the SIM card in the specified slot.

#### Syntax

```Bash
change-pin [slot_id][pin_type, pin or pin2][old_pin][new_pin]
```

- slot_id: Set the slot to query; currently, only `0` is supported.
- pin_type: Type of the PIN code, optional values are `pin` or `pin2`.
- old_pin: The current PIN code value.
- new_pin: The new PIN code value to be set.

#### Example

##### Input

```Bash
telephonytool> change-pin 0 pin 1234 2345
```

##### Output

```Bash
telephonytool> change-pin 0 pin 1234 2345
[12840.148400] [46] [ DEBUG] [ap] telephonytool_cmd_change_sim_pin, slot_id: 0 pin_type: pin old_pin: 1234 new_pin: 2345
telephonytool> [12840.160200] [21] [  INFO] [ap] [0,0081]> RIL_REQUEST_CHANGE_SIM_PIN (old=***,new=***,aid=(null))
```

### 10. Enter-pin

#### Description

The `enter-pin` command is used to validate the PIN (Personal Identification Number) of the SIM card in the specified slot.
#### Syntax

```Bash
enter-pin [slot_id][pin_type][pin]
```

- slot_id: Set the slot to query; currently, only `0` is supported.
- pin_type: Type of the PIN code, either `pin` or `pin2`.
- pin: The PIN code value to be validated.

#### Example

##### Input

```Bash
telephonytool> enter-pin 0 pin 1234
```

##### Output

```Bash
telephonytool> enter-pin 0 pin 1234
[12860.520000] [46] [ DEBUG] [ap] telephonytool_cmd_enter_sim_pin, slot_id: 0 pin_type: pin pin: ****
```

### 11. reset-pin

#### Description

The `reset-pin` command is used to reset the PIN (Personal Identification Number) of a SIM card in a specified slot using the PUK (Personal Unblocking Key).

#### Syntax

```Bash
reset-pin [slot_id][puk_type][puk][new_pin]
```

- slot_id: Specifies the slot to be monitored. Currently, only slot `0` is supported.
- puk_type: Type of PUK code. Options are `puk` or `puk2`.
- puk: Value of the PUK code.
- new_pin: Value of the new PIN code.

#### Example

##### Input

```Bash
telephonytool> reset-pin 0 puk 12345678 2345
```

##### Output

```Bash
telephonytool> reset-pin 0 puk 12345678 2345
[12877.463600] [46] [ DEBUG] [ap] telephonytool_cmd_reset_sim_pin, slot_id: 0 puk_type: puk puk: ****** new_pin: ******
```

### 12. lock-pin

#### Description

The `lock-pin` command is used to activate the PIN lock feature on the SIM card to ensure its security.

#### Syntax

```Bash
lock-pin [slot_id][pin_type, pin or pin2][pin]
```

- slot_id: Specifies the slot to be monitored. Currently, only slot `0` is supported.
- pin_type: Type of PIN code. Options are `pin` or `pin2`.
- pin: Value of the current PIN code.

#### Example

##### Input

```Bash
telephonytool> lock-pin 0 pin 1234 
```

##### Output

```Bash
telephonytool> lock-pin 0 pin 1234
[12894.617100] [46] [ DEBUG] [ap] telephonytool_cmd_lock_sim_pin, slot_id: 0 pin_type: pin pin: 1234
telephonytool> [12894.648800] [21] [  INFO] [ap] [0,0092]> RIL_REQUEST_SET_FACILITY_LOCK (SC,1,***,0,aid=(null))
```

### 13. unlock-pin

#### Description

The `unlock-pin` command is used to deactivate the PIN lock feature on the SIM card, removing the requirement for PIN verification.

#### Syntax

```Bash
unlock-pin [slot_id][pin_type, pin or pin2][pin]
```

- slot_id: Specifies the slot to be monitored. Currently, only slot `0` is supported.
- pin_type: Type of PIN code. Options are `pin` or `pin2`.
- pin: Value of the current PIN code.

#### Example

##### Input

```Bash
telephonytool>unlock-pin 0 pin 1234
```

##### Output

```Bash
telephonytool> unlock-pin 0 pin 1234
[12907.847700] [46] [ DEBUG] [ap] telephonytool_cmd_unlock_sim_pin, slot_id: 0 pin_type: pin pin: 1234
telephonytool> [12907.882000] [21] [  INFO] [ap] [0,0093]> RIL_REQUEST_SET_FACILITY_LOCK (SC,0,***,0,aid=(null))
```

### 14. open-logical-channel

#### Description

The `open-logical-channel` command is used to open a logical channel for reading and writing operations on the SIM card.
#### Syntax

```Bash
open-logical-channel [slot_id] [aid_str]
```

- slot_id: Specifies the slot to be monitored. Currently, only slot `0` is supported.
- aid_str: Application Identifier (AID) string used to specify the target application.

#### Example

##### Input

```Bash
telephonytool>open-logical-channel 0 A0000000871002FF86FFFF89FFFFFFFF 16
```

##### Output

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

- session id: The returned `session id` represents the logical channel session identifier for subsequent read/write operations.

### 15. close-logical-channel

#### Description

The `close-logical-channel` command closes a specified logical channel and releases the session resources with the SIM card.

#### Syntax

```Bash
close-logical-channel [slot_id][session_id]
```

- slot_id: Specifies the slot to query (currently only `0` is supported).
- session_id: Session ID of the logical channel to be closed.

#### Example

##### Input

```Bash
telephonytool>close-logical-channel 0 1
```

##### Output

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

- session_id: The `session od` in the output information represents the logical channel session identifier that has been successfully closed.

### 16. transmit-apdu-basic-channel

#### Description

The `transmit-apdu-logical-channel` command is used to send an APDU (Application Protocol Data Unit) command through a logical channel to the SIM card.

#### Syntax

```Bash
transmit-apdu-logical-channel [slot_id][session_id][pdu][len]
```

- slot_id: Specifies the slot to query, currently only supports `0`.
- session_id: The session identifier of the logical channel.
- pdu: The APDU data content to send.
- len: The byte length of the APDU data.

#### Example

##### Input

```Bash
telephonytool>transmit-apdu-logical-channel 0 1 FFF2000000 5
```

##### Output

```Bash
telephonytool> transmit-apdu-logical-channel 0 1 FFF2000000 5
[12971.991700] [46] [ DEBUG] [ap] telephonytool_cmd_transmit_apdu_logical_channel, slot_id: 0 sessionid: 1 pdu: FFF****000 len: 5
telephonytool> [12972.002100] [21] [  INFO] [ap] [0,0097]> RIL_REQUEST_SIM_TRANSMIT_APDU_CHANNEL (1, 255, 242, 0, 0, 0, (null))
```

### 17. transmit-apdu-basic-channel

#### Description

The `transmit-apdu-basic-channel` command is used to send an APDU (Application Protocol Data Unit) command through the basic channel to the SIM card.

#### Syntax

```Bash
transmit-apdu-basic-channel [slot_id][pdu][len]
```

- slot_id: Specifies the slot to query, currently only supports `0`.
- pdu: The APDU data content to send.
- len: The byte length of the APDU data.

#### Example

##### Input

```Bash
telephonytool>transmit-apdu-basic-channel 0 A0B000010473656E669000 11
```

##### Output

```Bash
telephonytool> transmit-apdu-basic-channel 0 A0B000010473656E669000 11
[12987.899500] [46] [ DEBUG] [ap] telephonytool_cmd_transmit_apdu_basic_channel, slot_id: 0 pdu: A0B0******9000 len: 11
telephonytool> [12987.929800] [21] [  INFO] [ap] [0,0098]> RIL_REQUEST_SIM_TRANSMIT_APDU_BASIC (0, 160, 176, 0, 1, 4, 73656e669000)
[12987.932900] [15] [  INFO] [ap] [AT_RIL] onRequest: 114<->SIM_TRANSMIT_APDU_BASIC, reqtype: 4
[12987.934800] [15] [  INFO] [ap] [AT_SIM] On request sim end
[12987.935700] [21] [  INFO] [ap] [0,0098]< RIL_REQUEST_SIM_TRANSMIT_APDU_BASIC (sw1=0x90,sw2=0x00)
```

### 18. get-uicc-enablement

#### Description

The `get-uicc-enablement` command is used to get the enablement status of the UICC (Universal Integrated Circuit Card) application.

#### Syntax

```Bash
get-uicc-enablement [slot_id]
```

- slot_id: Specifies the slot to query, currently only supports `0`.

#### Example

##### Input

```Bash
telephonytool>get-uicc-enablement 0
```

##### Output

```Bash
telephonytool> get-uicc-enablement 0
[13002.369500] [46] [ DEBUG] [ap] telephonytool_cmd_get_uicc_enablement, slotId : 0 state : 0
```

- state:
    - `0` indicates the UICC application is not enabled.
    - `1` indicates the UICC application is enabled.

### 19. set-uicc-enablement

#### Description

The `set-uicc-enablement` command is used to set the enablement or disablement status of the UICC (Universal Integrated Circuit Card) application.

#### Syntax

```Bash
set-uicc-enablement [slot_id][[state]
```

- slot_id: Specifies the slot to query, currently only supports `0`.
- state: Specifies the target state of the UICC application:
    - `0`: Disable the UICC application.
    - `1`: Enable the UICC application.

#### Example

##### Input

```Bash
telephonytool>set-uicc-enablement 0 1
```

##### Output

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
