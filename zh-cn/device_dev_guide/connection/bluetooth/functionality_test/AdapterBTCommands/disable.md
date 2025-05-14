# disable 子命令

\[ [English](../../../../../../en/device_dev_guide/connection/bluetooth/functionality_test/AdapterBTCommands/disable.md) | 简体中文 \]

## 一、简介

`disable` 命令用于关闭蓝牙适配器（Adapter）。如果当前有活跃的蓝牙连接，执行该命令会断开所有设备的蓝牙连接。蓝牙适配器关闭后，除以下命令外，其余 `bttool` 命令将无法使用：

- `enable`
- `quit`
- `state`
- `log`

## 二、示例

以下示例介绍如何关闭蓝牙适配器。

### 命令输入

```Plain
bttool> disable
```

### 注意事项

- 如果蓝牙适配器未启动时执行该命令，系统将仅返回适配器状态机信息，例如：

    ```Bash
    Process, State=Off, Event=SYS_TURN_OFF  
    ```

### 输出信息

执行成功后，预期输出如下：

```Bash
Adapter state changed: 0
```

### 适配器状态

| 状态 | 释义               |
| :--- | :----------------- |
| 0    | 蓝牙关闭。         |
| 5    | 关闭 BR/EDR 功能。 |
| 6    | 关闭 BLE 功能。    |

### 示例输出

```Plain
bttool> disable
[bttool] Context:0xe5b50d70, Adapter state changed: 5
[bttool] Context2:0xe5b50cf0, Adapter state changed: 5
[bttool] Context:0xe5b50d70, Adapter state changed: 6
[bttool] Context2:0xe5b50cf0, Adapter state changed: 6
[bttool] Context:0xe5b50d70, Adapter state changed: 0
[bttool] Context2:0xe5b50cf0, Adapter state changed: 0
```
