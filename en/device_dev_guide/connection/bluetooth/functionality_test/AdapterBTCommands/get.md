# Bluetooth Adapter get Sub-command

\[ English | [简体中文](../../../../../../zh-cn/device_dev_guide/connection/bluetooth/functionality_test/AdapterBTCommands/get.md) \]

## I. Introduction

The `get` command retrieves properties of the local Bluetooth adapter. It allows querying multiple configurations and statuses of the adapter.  

## II. Syntax

```Bash
get  
{  
    scanmode |  
    iocap |  
    addr |  
    leaddr |  
    name |  
    appearance |  
    class |  
    bonded <transport> |  
    connected <transport> |  
}  
```

## III. Commands

### 1. scanmode

#### Description

The `scanmode` command is used to get the current scanning status attribute of the local Bluetooth adapter. The scanning status indicates whether the device is discoverable or connectable.

#### Parameter Table

| **Parameter** | **Description**                                                                                                                                                        |    **Type**     |
| :-----------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: |
|   scan mode   | Discoverability and connectivity state:<br>0: Not discoverable, not connectable.<br>1: Not discoverable but connectable.<br>2: (Default) Discoverable and connectable. | Decimal integer |

#### Example

The following example demonstrates how to get the scanning status attribute of the local Bluetooth adapter.

##### Prerequisites

Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Enter the following command to retrieve the scanning status attribute:

```Plain
bttool> get scanmode
```

##### Output

```Plain
[bttool] Scan Mode:2
```

### 2. iocap

#### Description

The `iocap` command is used to get the input/output (IO) capability of the local Bluetooth adapter. The IO capability determines the type of user interaction supported during Bluetooth pairing.

#### Parameter Table

| **Parameter** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |    **Type**     |
| :-----------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: |
| io capability | The IO capability of the local Bluetooth adapter:<br>0: displayonly – no input capability, only displays or transmits a 6-digit decimal number.<br>1: yes/no – has a yes/no input mechanism and can display or transmit a 6-digit decimal number.<br>2: keyboardonly – can input numbers “0” to “9”, confirmation, and “yes”/“no”, but cannot output.<br>3: (Default) no-in/no-out – no input and output capability.<br>4: keyboard&display – can input numbers “0” to “9”, confirmation, and “yes”/“no”, and can display or transmit a 6-digit decimal number. | Decimal Integer |

#### Example

The following example demonstrates how to retrieve the IO capability of the local Bluetooth adapter.

##### Prerequisites

Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Enter the following command to retrieve the IO capability:

```Plain
bttool> get iocap
```

##### Output

```Plain
[bttool] IO Capability:4
```

### 3. addr

#### Description

The `addr` command is used to retrieve the address of the local Bluetooth adapter. This address is the unique identifier used in BR/EDR mode to identify the device.

#### Example

The following example demonstrates how to retrieve the address of the local Bluetooth adapter.

##### Prerequisites

Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Enter the following command to retrieve the adapter address:

```Plain
bttool> get addr
```

##### Output

```Plain
[bttool] Local Address:[xx:xx:xx:xx:xx:xx]
```

### 4. leaddr

#### Description

The `leaddr` command is used to retrieve the address used by the local Bluetooth adapter in Low Energy (LE) mode. This address can be either a public address or a private address.

#### Example

The following example demonstrates how to retrieve the address used by the local Bluetooth adapter in LE mode.

##### Prerequisites

Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Enter the following command to retrieve the LE mode address:

```Plain
bttool> get leaddr
```

##### Output

```Plain
[bttool] LE Address:xx:xx:xx:xx:xx:xx, type:0
```

In the output, the `type` indicates the address type:

- 0: Public Address.
- 1: Private Address.

### 5. name

#### Description

The `name` command is used to retrieve the name of the local Bluetooth adapter. This name is used to identify the device, and is typically displayed during the Bluetooth device discovery process.

#### Example

The following example demonstrates how to retrieve the name of the local Bluetooth adapter.

##### Prerequisites

Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Enter the following command to retrieve the adapter name:

```Plain
bttool> get name
```

##### Output

```Plain
[bttool] Local Name:Xiaomiii
```

### 6. appearance

#### Description

The `appearance` command is used to retrieve the appearance attribute of the local Bluetooth adapter. The appearance attribute describes the type or category of the device and is typically displayed during the Bluetooth device discovery process.

#### Example

The following example demonstrates how to retrieve the appearance attribute of the local Bluetooth adapter.

##### Prerequisites

Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Enter the following command to retrieve the adapter's appearance attribute:

```Plain
bttool> get appearance
```

##### Output

```Plain
[bttool] Le appearance:0x00c2
```

> **Note**: For the meaning of the numbers, refer to Section 2.6.3 of [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/).

### 7. class

#### Description

The `class` command is used to retrieve the device class of the local Bluetooth adapter. The device class describes the functionality and intended use of the Bluetooth device.

#### Example

The following example demonstrates how to retrieve the device class of the local Bluetooth adapter.

##### Prerequisites

Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Enter the following command to retrieve the device class:

```Plain
bttool> get class
```

##### Output

```Plain
[bttool] Local class of device: 0x00740704, is HEADSET: false
```

> **Note**: For the meaning of the numbers, refer to Section 2.8 of [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/).

### 8. bonded

#### Description

The `bonded` command is used to retrieve the information of devices that are currently bonded to the local Bluetooth adapter. This command can be used to view the devices that have been paired and bonded with the local Bluetooth adapter.

#### Parameter Table

| **Parameter** | **Description**                      |    **Type**     |
| :-----------: | :----------------------------------- | :-------------: |
|   transport   | Transport mode:<br>0: LE<br>1: BREDR | Decimal Integer |

#### Example

The following example demonstrates how to retrieve information on the devices bonded with the local Bluetooth adapter, using the bonded devices in BR/EDR mode as an example.

##### Prerequisites

1. Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

    ```Plain
    ap> bttool
    bttool> enable
    ```

2. In addition, ensure that there is at least one device that has established a Bluetooth connection and completed bonding with the local Bluetooth adapter; otherwise, this command will have no effect.

##### Command Input

Enter the following command to retrieve the bonded devices information in BR/EDR mode:

```Plain
bttool> get bonded 1
```

##### Output

> **Note**: The number in the output indicates the number of devices bonded in the corresponding mode.

```Plain
[bttool] device [xx:xx:xx:xx:xx:xx]
[bttool]        Name: Samsung S21
[bttool]        Alias: Samsung S21
[bttool]        Class: 0x005a020c
[bttool]        DeviceType: 1
[bttool]        IsConnected: 1
[bttool]        ACLHandle: 6
[bttool]        IsEnc: 1
[bttool]        IsBonded: 1
[bttool]        BondState: BONDED
[bttool]        IsBondInitiateLocal: 0
[bttool] bonded device cnt:1
```

### 9. connected

#### Description

The `connected` command is used to retrieve the detailed information of devices that are currently connected. With this command, you can view the detailed connection information of devices connected to the local Bluetooth adapter.

#### Parameter Table

| **Parameter** | **Description**                      |    **Type**     |
| :-----------: | :----------------------------------- | :-------------: |
|   transport   | Transport mode:<br>0: LE<br>1: BREDR | Decimal Integer |

#### Example

The following example demonstrates how to retrieve the information of devices that are currently connected, using the connected devices in LE mode as an example.

##### Prerequisites

1. Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

    ```Plain
    ap> bttool
    bttool> enable
    ```

2. In addition, ensure that there is at least one device that has established a Bluetooth connection with the local Bluetooth adapter; otherwise, this command will have no effect.

##### Command Input

```Plain
bttool> get connected 0
```

##### Output

> **Note**: The number in the output indicates the number of devices connected in the corresponding mode.

```Plain
[bttool] device [xx:xx:xx:xx:xx:xx]
[bttool]        IsConnected: 1
[bttool]        IsEnc: 0
[bttool]        IsBonded: 0
[bttool]        BondState: BOND_NONE
[bttool]        IsBondInitiateLocal: 0
[bttool] connected device cnt:1
```
