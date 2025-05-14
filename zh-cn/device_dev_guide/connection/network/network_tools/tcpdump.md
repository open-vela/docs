# tcpdump

\[ [English](../../../../../en/device_dev_guide/connection/network/network_tools/tcpdump.md) | 简体中文 \]

## 一、概述

本文介绍了使用 `tcpdump` 工具抓取网络数据包的基本方法，包括抓包、退出、结果解读以及网卡驱动适配的相关说明。

## 二、配置说明

使用 `tcpdump` 工具前，需要在系统中启用以下配置项：

```Makefile
CONFIG_NET_PKT=y
CONFIG_SYSTEM_TCPDUMP=y

# 不同文件系统对Stack的需求有差异，建议配置为8192
CONFIG_SYSTEM_TCPDUMP_STACKSIZE=8192 
```

## 三、操作使用

### 1、tcpdump参数说明

```Bash
指定抓包的网卡名称
-i interface
--interface=interface

保存抓包文件的路径
-w file

设置单个包的最大保存长度。例如：对于长度为 1KB 的数据包，可以仅保存头部的 100 字节。
-s snaplen
--snapshot-length=snaplen
```

### 2、tcpdump的使用

1. 准备工作。

    在使用 `tcpdump` 抓包之前，需要完成以下准备工作：

    - 准备存储目录：确保设备上有可用的目录用于存储抓包文件，具体路径取决于设备的存储方式。
    - 挂载宿主机目录（适用于 openvela SIM 环境）：可以将宿主机的目录挂载到设备中，便于存储抓包文件。

        ```Bash
        # 以SIM为例，挂载host上的目录到/data1
        mount -t hostfs -o fs=. /data1
        ```

2. 抓包。

    使用 `tcpdump` 命令抓取网络数据包，以下是常见的操作方法：

    - 基本抓包。

        直接执行 `tcpdump` 命令，指定网卡和保存路径：

        ```Bash
        # 将eth0的网络包保存至test.pcap
        tcpdump -i eth0 -w /data1/test.pcap
        ```

    - 后台抓包。

        如果需要在抓包的同时执行其他命令，可以将 `tcpdump` 设置为后台运行（在命令末尾加 `&`）：

        ```Bash
        # 后台将eth0的网络包保存至test.pcap
        tcpdump -i eth0 -w /data1/test.pcap &
        ```

3. 退出。

    - 前台运行退出。
  
        按下 `Ctrl+C` 退出 `tcpdump`，会正常保存抓包文件并退出。

    - 后台运行退出。

        如果 `tcpdump` 在后台运行，可以通过以下命令结束进程：

        ```Bash
        kill -2 <tcpdump 的 PID>
        ```

        说明：该命令的效果等同于按下 `Ctrl+C`。

## 四、结果解读

抓包完成后，可以使用 **Wireshark** 工具对生成的 `.pcap` 文件进行分析。以下是基本操作步骤：

1. 打开 **Wireshark** 工具。
2. 通过菜单 **File > Open**，选择抓包生成的 `.pcap` 文件。
3. 查看并分析网络数据包的详细信息。

> 说明：**Wireshark** 的具体使用方法不在本文范围内，用户可参考网上的公开教程以获取更多操作细节。
