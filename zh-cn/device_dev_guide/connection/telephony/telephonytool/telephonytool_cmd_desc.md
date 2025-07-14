# telephonytool 命令

\[ [English](../../../../../en/device_dev_guide/connection/telephony/telephonytool/telephonytool_cmd_desc.md) | 简体中文 \]

## 一、概述

`telephonytool` 是一个在 openvela 的 NSH 命令行中执行的工具，用于进入 Telephony 命令工具的控制台（Console）。在控制台中，可以执行 `telephonytool` 工具内集成的特定子命令。

## 二、语法

以下是命令行语法的规则说明：

| **表示法**               | **说明**                       | **示例**                                                         |
| :----------------------- | :----------------------------- | :--------------------------------------------------------------- |
| 不含方括号或大括号的文本 | 需要按所显示内容原样键入。     | `hold_and_answer` 命令中的 `hold_and_answer` 部分必须原样键入。  |
| [方括号内的文本]         | 表示占位符，需要用实际值替换。 | `hangup-all [slot_id]` 命令中的 `[slot_id]` 需要替换为实际的值。 |

## 三、示例

以下示例展示如何在 NSH 命令行中打开 `telephonytool` 工具。

### 1、命令输入

```Bash
ap> telephonytool
```

### 2、输出信息

执行命令后，终端会显示 `telephonytool>` 提示符，表示已成功进入 `telephonytool` 控制台。以下是示例输出：

```Bash
goldfish-armv7a-ap> telephonytool
[  177.780000] [31] [  WARN] [ap] Successfully connected to unix socket /var/run/dbus/system_bus_socket
[  177.847300] [31] [ DEBUG] [ap] [async_queue:85]uv_async_queue_init
telephonytool> [  178.167200] [31] [  INFO] [ap] enable_modem_abnormal_event_done:0
[  178.246700] [31] [  INFO] [ap] on_modem_property_change - from 0 to 1
[  178.258900] [31] [ DEBUG] [ap] tapi is ready for vela.telephony.tool
```
