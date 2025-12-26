# Bluetooth Adapter set Sub-command

\[ English | [简体中文](../../../../../../zh-cn/device_dev_guide/connection/bluetooth/functionality_test/AdapterBTCommands/set.md) \]

## I. Introduction

The `set` command is used to configure the properties of the local Bluetooth adapter. With this command, you can set attributes such as the adapter's scan mode, name, device class, and more.

## II. Syntax

The syntax structure for the `set` command is as follows:

```Bash
set  
{  
    scanmode <scan mode> |  
    iocap <io capability> |  
    name <local name> |  
    class <local class of device> |  
    appearance <appearance> |  
    leaddr <leaddr> |  
    id <identity addr> <addr type> |  
    scanparams <mode> <type> <interval> <window>  
}
```

## III. Commands

### 1. scanmode

#### Description

`scanmode` sets the scan mode of the local Bluetooth adapter, controlling whether the BR/EDR controller periodically performs page scans and responds to inquiries. It determines the adapter's discoverability and connectability.

#### Parameters

| **Parameter** | **Description**                                                                                                                                                                  | **Type**        |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------- |
| scan mode     | Configures discoverability and connectability:<br>0: Not discoverable and not connectable.<br>1: Not discoverable but connectable.<br>2: (Default) Discoverable and connectable. | Decimal integer |


#### Example

Set the adapter to connectable but not discoverable:

##### Prerequisites

Ensure the Bluetooth adapter is enabled via `bttool`:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Type the following command to set the scan mode to `1` (not discoverable but connectable):

```Plain
bttool> set scanmode 1
```

##### Output

The expected results are as follows:

```Plain
[bttool] Scan Mode:1 set success
```

### 2. iocap

#### Description

`iocap` sets the IO capability of the adapter, which defines the authentication method used during Bluetooth pairing.

#### Parameters

| **Parameter** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | **Type**        |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------------- |
| io capability | IO capability options:<br>0: `DisplayOnly` – No input capability; can only display/transmit 6-digit codes.<br>1: `Yes/No` – Can accept "Yes" or "No" input; can display/transmit 6-digit codes.<br>2: `KeyboardOnly` – Can input digits 0-9, "Confirm," "Yes," or "No"; no output capability.<br>3: (Default) `NoInputNoOutput` – No input or output capability.<br>4: `KeyboardDisplay` – Can input digits 0-9, "Confirm," "Yes," or "No"; can display/transmit 6-digit codes. | Decimal integer |

#### Example

Set IO capability to `displayonly`:

##### Prerequisites

Ensure the Bluetooth adapter is enabled via `bttool`:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Enter the following command to set the IO capability to `0` (displayonly):

```Plain
bttool> set iocap 0
```

##### Output

The expected results are as follows:

```Plain
[bttool] IO Capability:0 set success
```

The number `0` corresponds to the `displayonly` IO capability.

### 3. name

#### Description

`name` sets the user-friendly name of the adapter visible to other Bluetooth devices.

#### Parameters

| **Parameter** | **Description** | **Type** | **Range**           | **Default** |
| ------------- | --------------- | -------- | ------------------- | ----------- |
| local name    | Adapter name    | String   | Up to 64 characters | N/A         |

#### Example

The following example demonstrates how to set the local Bluetooth adapter's name to `Xiaomiii`.

##### Prerequisites

Ensure the Bluetooth adapter is enabled via `bttool`:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Enter the following command to set the local Bluetooth adapter's name to `Xiaomiii`:

```Plain
bttool> set name Xiaomiii
```

##### Output

The expected results are as follows:

```Plain
[bttool] Local Name:Xiaomiii set success  
[bttool] Adapter update device name: Xiaomiii
```

### 4. class

#### Description 

`class` sets the Class of Device (CoD) for the local Bluetooth Adapter. The CoD identifies the device’s primary functionality and services.  

#### Parameters  

| **Parameter** | **Description**                                                                                                                                 | **Type**            | **Default** |
| :------------ | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ | :---------- |
| class         | Device class:<br>Bits 23–13: Major Service Class.<br>Bits 12–8: Major Device Class.<br>Bits 7–2: Minor Device Class.<br>Bits 1–0: Fixed to `0`. | Hexadecimal integer | 0x00280704  |

#### Notes

- The last hexadecimal digit must be `0`, `4`, `8`, or `C`.  
- Refer to Bluetooth SIG [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/) §2.8 for valid values.  

#### Example

The following example demonstrates how to set the local Bluetooth adapter's class to "Wearable Watch".

##### Prerequisites

Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. Use the following command to enable it:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

According to the [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/) document:

- The major device class "Wearable" is represented as `0b00111`.
- The minor device class "Wristwatch" is represented as `0b000001`.
- The supported services include Telephony, Audio, Object Transfer, and Rendering, represented as `0b01110100000`.
- The final device class is `0b011101000000011100000100`, which converts to hexadecimal as `0x740704`.

Enter the following command to set the device class:

```Plain
bttool> set class 740704
```

##### Output

The expected results are as follows:

```Plain
[bttool] Local class of device:0x00740704 set success
```

### 5. appearance

#### Description

`appearance` sets the appearance of the adapter, used in LE mode to describe device type and subtype.

#### Parameters

| **Parameter** | **Description**                                                                                                                                            | **Type**    | **Default** |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ----------- |
| appearance    | 16-bit value (bit 16–6: category, bit 5–0: subcategory). See [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/) Section 2.6.3. | Hex Integer | 0           |

#### Example

The following example demonstrates how to set the local Bluetooth adapter's appearance to Smart Watch.

##### Prerequisites

Before executing the following command, make sure that the Bluetooth adapter has been enabled via the `bttool` console. Use the following command to enable it:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

According to the [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/) document, the appearance value for a Smart Watch is `0x00C2`. Enter the following command to set the appearance:

```Plain
bttool> set appearance c2
```

##### Output

The expected results are as follows:

```Plain
[bttool] Set Le appearance:0x00c2
```

### 6. leaddr

#### Functionality Description

The term `leaddr` is used to set the private address (a type of LE random address) used by the local Bluetooth adapter in Low Energy (LE) mode.

In LE mode, Bluetooth devices can use either a public address or a random address to identify the device. The random address is further divided into static addresses and private addresses.

- The type of random address is indicated by bits 47~46 of the address, while the remaining bits are the random part.

- Description of address types:

| **Bits 47–46** | **Type**               |
| -------------- | ---------------------- |
| 0b00           | Non-resolvable private |
| 0b01           | Resolvable private     |
| 0b10           | Reserved               |
| 0b11           | Static address         |

#### Address Type Description

1. Public Address:

    - A unique address that needs to be allocated by IEEE.
    - In the case of dual-mode BR/EDR and LE, it is typically the same address used by BR/EDR.

2. Static Address:

    - Randomly generated, not unique, and only generated during the initialization process.
    - The random part cannot be all `0`s or all `1`s.

3. Private Address:

    - Randomly generated, not unique, and updated each time a connection is made or after a specific period.
    - Non-Resolvable Private Address: The random part cannot be all `0`s or all `1`s, and it cannot be the same as the public address.
    - Resolvable Private Address: The lower 24 bits must follow a specific generation algorithm.

#### Parameters

| **Parameter** | **Description**                                   | **Type** | **Default** |
| ------------- | ------------------------------------------------- | -------- | ----------- |
| leaddr        | LE private address in format `XX:XX:XX:XX:XX:XX`. | String   | N/A         |

#### Example

The following example demonstrates how to set the LE address of the local Bluetooth adapter to `01:02:03:04:05:06`.

##### Prerequisites

Before executing the following commands, ensure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

Enter the following command to set the LE address:

```Plain
bttool> set leaddr 01:02:03:04:05:06
```

##### Output

The expected results are as follows:

```Plain
bttool> [   80.646100] [49] [ DEBUG] [ap] [1362][adapter-svc]: adapter_on_le_addr_update
```

### 7. id

#### Description

`id` sets the adapter's static or public identity address for LE mode.

> **Note**: This feature is currently **not supported**.

#### Parameters

| **Parameter** | **Description**                                | **Type** | **Default** |
| ------------- | ---------------------------------------------- | -------- | ----------- |
| identity addr | Identity address in `XX:XX:XX:XX:XX:XX` format | String   | N/A         |
| addr type     | Address type: 0 = Static, 1 = Public           | Integer  | 1           |

### 8. scanparam

#### Description

`scanparam` sets scanning parameters for specific scan modes.

#### Parameters

| **Parameter** | **Description**                                                                   | **Type**        | **Default**                 |
| :------------ | :-------------------------------------------------------------------------------- | :-------------- | :-------------------------- |
| mode          | Scan mode:<br>0: Inquiry Scan (discoverable).<br>1: Page Scan (connectable).      | Decimal integer | N/A                         |
| type          | Scan type:<br>0: Standard Scan.<br>1: Interlaced Scan.                            | Decimal integer | N/A                         |
| interval      | Scan interval (period between scans).<br>Range: 18–4096 slots (1 slot = 0.625ms). | Decimal integer | Inquiry: 4096<br>Page: 2048 |
| window        | Scan window (duration of each scan).<br>Range: 17–`<interval>` slots.             | Decimal integer | 18                          |

#### Notes

- Slot unit: 1 slot equals 0.625ms.
- Interlaced Scan limitation: If `<interval>` is not at least twice the size of `<window>`, Interlaced Scan cannot be used.

#### Example

The following example demonstrates how to set a set of scanning parameters. It sets the scan interval to 1.28 seconds and the scan window to 31.25 milliseconds for a standard Inquiry Scan.

##### Prerequisites

Before executing the following commands, ensure that the Bluetooth adapter has been enabled via the `bttool` console. The enable command is as follows:

```Plain
ap> bttool
bttool> enable
```

##### Command Input

- Inquiry Scan corresponds to `<mode>` being `0`.
- Standard Scan corresponds to `<type>` being `0`.
- A scan interval of 1.28 seconds corresponds to `1280 / 0.625 = 2048` slots.
- A scan window of 31.25 milliseconds corresponds to `31.25 / 0.625 = 50` slots.

```Plain
bttool> set scanparams 0 0 2048 50
```

##### Output Information

This command has no output information.
