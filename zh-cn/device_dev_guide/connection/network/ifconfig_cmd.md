# 使用 ifconfig 命令配置网卡

## 概述

本命令主要用于对网卡进行如下配置：

- 设置 ip 地址
- 设置网络掩码
- 设置网关地址
- 设置 mac 地址
- 查看网络接口的状态

## 前提条件

使用 ifconfig 命令需要在编译时开启网络支持和 proc 文件系统功能，可按如下步骤打开配置：

1. 切换到 openvela 仓库的根目录，编译时使用 `menuconfig` 打开图形化配置界面，执行如下命令：

    ```Bash
    ./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap menuconfig
    ```

2. 打开界面后输入 `/`，分别搜索以下五个配置项并修改为如下配置：

    ```Makefile
    CONFIG_NET=y
    CONFIG_NETDEV_STATISTICS=y
    CONFIG_FS_PROCFS=y
    CONFIG_FS_PROCFS_EXCLUDE_NET=n
    CONFIG_NSH_DISABLE_IFCONFIG=n
    ```

## 参数说明

```Shell
ifconfig interface [[inet|inet6] [<ip-address>|dhcp]] [dr|gw|gateway <dr-address>] [netmask <net-mask>|prefixlen <len>] [dns <dns-address>] [hw <hw-mac>]]
```

> **说明**：openvela 的 ifconfig 和 Linux 的 ifconfig 有部分差异，暂时不支持 [-v] [-a] [-s] 等参数。

| 参数                                | 描述                                                       |
|-------------------------------------|------------------------------------------------------------|
| interface                           | 接口的名称。<br> 这通常是一个驱动程序名，后面跟着一个单元号。例如用于第一个以太网接口的 eth0，Wi-Fi 类型的网卡一般为 wlan0。 |
| inet/inet6                          | 选定地址族，与地址分配联合使用。                             |
| \<ip-address>\|dhcp                  | 直接指定网卡静态 IP 地址或通过 DHCP 获取动态地址。           |
| dr\|gw\|gateway \<dr-address>        | 设置网关地址。                                               |
| netmask \<net-mask>\|prefixlen \<len> | 设置此接口的 IP 网络掩码。<br> 此值默认为通常的 A、B 或 C 类网络掩码（从接口 IP 地址派生），但可以设置为任何值。 |
| dns <dns-address>                   | 设置 DNS。                                                    |
| hw <hw-mac>                         | 如果设备驱动程序支持此操作，则设置此接口的硬件地址。         |

## 常用命令

- ifup & ifdown 命令通常与 ifconfig 搭配使用，用以使能或关闭网卡。

  - ```Bash
    ifup eth0    #使能eth0网卡
    ifdown eth0  #关闭eth0网卡
    ```

- 不带选项的 ifconfig 命令将显示所有接口的配置。

  - ```Bash
    ifconfig
    ```

- 显示指定（如 eth0 ）接口的配置。

  - ```Bash
    ifconfig eth0
    ```

- 配置 eth0 静态 ip 为 10.0.1.3。

  - ```Bash
    ifconfig eth0 10.0.1.3
    ```

- 配置 eth0 静态 ip 为10.0.1.3，网关为 10.0.1.1 ，掩码地址为 255.255.255.0，dns 为 8.8.8.8。

  - ```Bash
    ifconfig eth0 10.0.1.3 gateway 10.0.1.1 netmask 255.255.255.0 dns 8.8.8.8
    ```

- 配置 eth0 静态 ipv6 地址为 2001:db8::，掩码 32 位。

  - ```Bash
    ifconfig eth0 inet6 add 2001:db8::/32
    ```