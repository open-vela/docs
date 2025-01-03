# bttool命令说明

## 简介

在 openvela的 `NSH` 命令行中执行，用于进入蓝牙命令工具的 Console。在 Console 中，可以执行 `bttool` 工具内集成的特有的子命令。

## 语法

| **命令行表示法**         | **说明**                       | **举例**                                                     |
| :----------------------- | :----------------------------- | :----------------------------------------------------------- |
| 不含方括号或大括号的文本 | 必须按所显示键入的项。         | `cd` <br> 命令中的 `cd` 部分就是必须原样键入的。                  |
| <尖括号内的文本>         | 必须为其提供值的占位符。       | `mkdir <directory_name>` <br>命令中的 `<directory_name>` 需要被替换成实际的目录名。 |
| [方括号内的文本]         | 可选项。                       | `ls [-l]` <br> 命令中的 `[-l]` 是一个可选项，表示是否以长列表格式显示文件。 |
| {花括号内的文本}         | 一组必需的项， 必须选择一个。  | `git reset { --soft \| --mixed \| --hard }` <br> 必须选择这三个选项中的一个，例如 `git reset --soft`。 |
| 竖线 \|                  | 互斥项的分隔符，必须选择一个。 | `git reset { --soft \| --mixed \| --hard }` <br> `--soft`, `--mixed`, `--hard`只能选其中一个。 |
| 省略号 …                 | 可重复使用多次的项。           | `cp <file1> <file2> … <destination>` <br> 省略号表示可以复制多个文件到目的地。 |

## 示例

本示例介绍在 `NSH` 命令行打开 `bttool`。

### 前提条件

已进入 `NSH` 操作界面。

### 命令输入

```Bash
ap> bttool
```

### 输出信息

终端显示 `bttool>` 提示符，进入 bttool Console。

```Bash
[    8.232900] [51] [ DEBUG] [ap] thread_schedule_loop:0xf0b10580, async:0xf1b0c740
[    8.233900] [51] [ DEBUG] [ap] set_ready
[    8.234400] [50] [ DEBUG] [ap] bt_client_50 loop running now !!!
bttool>
```
