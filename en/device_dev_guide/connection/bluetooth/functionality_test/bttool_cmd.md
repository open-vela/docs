# bttool Command

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/bluetooth/functionality_test/bttool_cmd.md) \]

## I. Introduction

Executed in the openvela NSH command line to enter the Bluetooth command tool console. Within this console, you can execute `bttool`’s built‑in sub-commands.

## II. Syntax

| **Syntax Element**           | **Description**                                     | **Example**                                                                                   |
| :--------------------------- | :-------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| Text without brackets/braces | Items that must be typed exactly as shown.          | `cd` <br> The `cd` portion of the command must be typed verbatim.                             |
| \<Text in angle brackets\>   | Placeholders requiring value substitution.          | `mkdir <directory_name>` <br> Replace `<directory_name>` with an actual.                      |
| [Text in square brackets]    | Optional items.                                     | `ls [-l]` <br> `[-l]` is optional to display files in long list format.                       |
| {Text in curly braces}       | Required group - exactly one item must be selected. | `git reset { --soft \| --mixed \| --hard }` <br> Select one option, e.g., `git reset --soft`. |
| Vertical bar \|              | Separator for mutually exclusive items.             | `git reset { --soft \| --mixed \| --hard }` <br> Choose only one of the options.              |
| Ellipsis …                   | Items that can be repeated multiple times.          | `cp <file1> <file2> … <destination>` <br> Copy multiple files to destination.                 |

## III. Example

This example demonstrates launching `bttool` from the `NSH` command-line.

### Prerequisites

Have accessed the `NSH` interface.

### Command Input

```Bash
ap> bttool
```

### Output Information

The prompt changes to `bttool>`, indicating you have entered the bttool console.

```Bash
[    8.232900] [51] [ DEBUG] [ap] thread_schedule_loop:0xf0b10580, async:0xf1b0c740
[    8.233900] [51] [ DEBUG] [ap] set_ready
[    8.234400] [50] [ DEBUG] [ap] bt_client_50 loop running now !!!
bttool>
```
