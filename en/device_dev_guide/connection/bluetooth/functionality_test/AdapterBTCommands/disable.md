# Bluetooth Adapter disable Sub-command

\[ English | [简体中文](../../../../../../zh-cn/device_dev_guide/connection/bluetooth/functionality_test/AdapterBTCommands/disable.md) \]

## I. Introduction

The `disable` command is used to turn off the Bluetooth adapter. If active Bluetooth connections exist, executing this command will disconnect all devices. After disabling the adapter, only the following `bttool` commands remain available:  

- `enable`  
- `quit`  
- `state`  
- `log`  

## II. Examples

The following example demonstrates how to disable the Bluetooth adapter.

### Command Input

```Plain
bttool> disable
```

### Notes

If the Bluetooth adapter is already inactive, the command returns state machine information only, e.g.:  

```Bash
Process, State=Off, Event=SYS_TURN_OFF  
```

### Output Information

Successful execution returns:  

```Bash
Adapter state changed: 0
```

### Adapter States

| State | Description               |
| :---- | :------------------------ |
| 0     | Bluetooth off.            |
| 5     | BR/EDR functionality off. |
| 6     | BLE functionality off.    |

### Sample Output

```Plain
bttool> disable
[bttool] Context:0xe5b50d70, Adapter state changed: 5
[bttool] Context2:0xe5b50cf0, Adapter state changed: 5
[bttool] Context:0xe5b50d70, Adapter state changed: 6
[bttool] Context2:0xe5b50cf0, Adapter state changed: 6
[bttool] Context:0xe5b50d70, Adapter state changed: 0
[bttool] Context2:0xe5b50cf0, Adapter state changed: 0
```
