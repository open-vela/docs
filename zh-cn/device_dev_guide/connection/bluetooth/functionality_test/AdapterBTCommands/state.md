# state 子命令

\[ [English](../../../../../../en/device_dev_guide/connection/bluetooth/functionality_test/AdapterBTCommands/state.md) | 简体中文 \]

## 一、简介

`state` 命令用于获取蓝牙适配器（Adapter）的当前状态。通过该命令，用户可以查看适配器的运行状态，例如是否已启用 BLE（低功耗蓝牙）或 BR/EDR（基本速率/增强数据速率）功能。

## 二、示例

### 示例 1：查看蓝牙适配器状态

#### 前提条件

确保已打开 `bttool` 工具， 有关 `bttool` 的详细命令说明，请参见 [bttool 命令说明](../bttool_cmd.md)。

```Bash
ap> bttool
```

#### 命令输入

```Bash
bttool> state
```

#### 输出信息

执行成功后，预期输出如下：

```Bash
Adapter State: <状态值>  
```

#### 适配器状态

以下是适配器状态值及其对应的含义：

| 状态值 | 释义                   |
| :----- | :--------------------- |
| 0      | 蓝牙关闭。             |
| 1      | 正在启用 BLE 功能。    |
| 2      | BLE 功能已启用。       |
| 3      | 正在启用 BR/EDR 功能。 |
| 4      | BR/EDR 功能已启用。    |
| 5      | 关闭 BR/EDR 功能。     |
| 6      | 关闭 BLE 功能。        |

#### 示例输出

```Bash
[bttool] Adapter State: 0
```

### 示例 2：查看蓝牙适配器成功启动后的状态

#### 前提条件

在执行此操作之前，需通过 `enable` 命令启动蓝牙适配器。

```Plain
ap> bttool
bttool> enable
```

#### 命令输入

```Bash
bttool> state
```

#### 输出信息

执行成功后，预期输出如下：

```Bash
[bttool] Adapter State: 4
```
