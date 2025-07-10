# Bluetooth Adapter state Sub-command

\[ English | [简体中文](../../../../../../zh-cn/device_dev_guide/connection/bluetooth/functionality_test/AdapterBTCommands/state.md) \]

## I. Introduction

The `state` command is used to retrieve the current status of the Bluetooth adapter. With this command, users can check whether features such as BLE (Low Energy) or BR/EDR (Basic Rate/Enhanced Data Rate) are enabled.

## II. Examples

### Example 1: Check Bluetooth Adapter Status

#### Prerequisites

Ensure that the `bttool` utility is open. For detailed command descriptions, see [bttool Command Description](../bttool_cmd.md).

```Bash
ap> bttool
```

#### Command Input

```Bash
bttool> state
```

#### Output

Upon success, the output will display: 

```Bash
Adapter State: <state value>
```

#### Adapter States

| State Value | Description                     |
| :---------- | :------------------------------ |
| 0           | Bluetooth is off.               |
| 1           | Enabling BLE functionality.     |
| 2           | BLE functionality enabled.      |
| 3           | Enabling BR/EDR functionality.  |
| 4           | BR/EDR functionality enabled.   |
| 5           | Disabling BR/EDR functionality. |
| 6           | Disabling BLE functionality.    |

#### Sample Output

```Bash
[bttool] Adapter State: 0
```

---

### Example 2: Check Status After Successful Adapter Startup

#### Prerequisites

Before performing this, start the Bluetooth adapter using the `enable` command.

```Plain
ap> bttool
bttool> enable
```

#### Command Input

```Bash
bttool> state
```

#### Output Information

Upon success, the output will display:

```Bash
[bttool] Adapter State: 4
```
