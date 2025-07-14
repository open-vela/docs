# Telephonytool Command

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/telephony/telephonytool/telephonytool_cmd_desc.md) \]

## I. Overview

`telephonytool` is a tool executed in the NSH command line of openvela, used to enter the Console of the Telephony command tool. Within the console, specific subcommands integrated in the `telephonytool` can be executed.

## II. Syntax

The following rules describe the command line syntax:

| **Notation**                                   | **Description**                                                          | **Example**                                                                                       |
| :--------------------------------------------- | :----------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------ |
| Text without square brackets or curly brackets | Type exactly as displayed.                                               | The `hold_and_answer` portion of the `hold_and_answer` command must be typed as is.               |
| [Text in square brackets]                      | Indicates a placeholder that needs to be replaced with the actual value. | The `[slot_id]` in the `hangup-all [slot_id]` command needs to be replaced with the actual value. |

## III. Example

The following example demonstrates how to launch the `telephonytool` in the NSH command line.

### 1. Command Input

```Bash
ap> telephonytool
```

### 2. Output Information

After executing the command, the terminal will display the `telephonytool` prompt, indicating successful entry into the `telephonytool` console. Below is an example output:

```Bash
goldfish-armv7a-ap> telephonytool
[  177.780000] [31] [  WARN] [ap] Successfully connected to unix socket /var/run/dbus/system_bus_socket
[  177.847300] [31] [ DEBUG] [ap] [async_queue:85]uv_async_queue_init
telephonytool> [  178.167200] [31] [  INFO] [ap] enable_modem_abnormal_event_done:0
[  178.246700] [31] [  INFO] [ap] on_modem_property_change - from 0 to 1
[  178.258900] [31] [ DEBUG] [ap] tapi is ready for vela.telephony.tool
```
