# Bluetooth Adapter enable Sub-command

\[ English | [简体中文](../../../../../../zh-cn/device_dev_guide/connection/bluetooth/functionality_test/AdapterBTCommands/enable.md) \]

## I. Introduction

This document explains how to enable the Bluetooth adapter. Enabling the adapter is a prerequisite for executing other Bluetooth-related commands.

## II. Example

The following example demonstrates how to enable the Bluetooth adapter.

### Prerequisites

Launch `bttool` in NSH. For detailed information on the `bttool` commands, please refer to the [bttool Command Description](../bttool_cmd.md).

```Bash
ap> bttool
```

### Command Input

```Bash
bttool> enable
```

### Output Information

Successful execution returns:  

```Bash
Adapter state changed: 4
```

This output indicates that both the BR/EDR (Basic Rate/Enhanced Data Rate) and LE (Low Energy) functionalities of the Bluetooth adapter have been successfully enabled.

#### Adapter States

| State | Description                    |
| :---- | :----------------------------- |
| 1     | Enabling BLE functionality.    |
| 2     | BLE functionality enabled.     |
| 3     | Enabling BR/EDR functionality. |
| 4     | BR/EDR functionality enabled.  |

#### Sample Output

The following is an example of the Bluetooth adapter state changes:

```Plain
[bttool] Context:0xf1893610, Adapter state changed: 1
[bttool] Context2:0xf1893590, Adapter state changed: 1
[bttool] Context:0xf1893610, Adapter state changed: 2
[bttool] Context2:0xf1893590, Adapter state changed: 2
[bttool] Context:0xf1893610, Adapter state changed: 3
[bttool] Context2:0xf1893590, Adapter state changed: 3
[bttool] Context:0xf1893610, Adapter state changed: 4
[bttool] Adapter Name: XIAOMI VELA-052, Cap: 3, Class: 0x00280704, Mode:2
[bttool] Context2:0xf1893590, Adapter state changed: 4
```
