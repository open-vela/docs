# enable 子命令

\[ [English](../../../../../../en/device_dev_guide/connection/bluetooth/functionality_test/AdapterBTCommands/enable.md) | 简体中文 \]

## 一、简介

本文介绍如何启动蓝牙适配器（Adapter），这是执行其他蓝牙相关命令的前置条件。

## 二、示例

以下示例介绍如何启动蓝牙适配器。

### 前提条件

在 NSH 中打开 `bttool`。有关 `bttool` 的详细命令说明，请参见 [bttool 命令说明](../bttool_cmd.md)。

```Bash
ap> bttool
```

### 命令输入

```Bash
bttool> enable
```

### 输出信息

执行成功后，预期输出如下：

```Bash
Adapter state changed: 4
```

此输出表示蓝牙适配器的 BR/EDR（基本速率/增强数据速率）和 LE（低功耗）功能已成功启用。

#### 适配器状态

| 状态 | 释义                   |
| :--- | :--------------------- |
| 1    | 正在启用 BLE 功能。    |
| 2    | BLE 功能已启用。       |
| 3    | 正在启用 BR/EDR 功能。 |
| 4    | BR/EDR 功能已启用。    |

#### 示例输出

以下是蓝牙适配器状态变化的示例输出：

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
