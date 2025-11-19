# Configuring Network Interfaces Using the ifconfig Command

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/network/network_tools/ifconfig_cmd.md) \]

## I. Overview

This command is primarily used for the following network interface configurations:

- Setting IP addresses

- Configuring netmasks

- Specifying gateway addresses

- Assigning MAC addresses

- Viewing network interface status

## II. Prerequisites

To use the ifconfig command, enable network support and proc filesystem support during compilation:

1. Navigate to the openvela repository root and use `menuconfig` to configure:

    ```Bash
    ./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap menuconfig
    ```

2. Enable the following configurations:

    ```Makefile
    CONFIG_NET=y
    CONFIG_NETDEV_STATISTICS=y
    CONFIG_FS_PROCFS=y
    CONFIG_FS_PROCFS_EXCLUDE_NET=n
    CONFIG_NSH_DISABLE_IFCONFIG=n
    ```

## III. Parameter Reference

> **Note**: openvela's ifconfig differs from Linux's implementation. Parameters like [-v], [-a], and [-s] are not supported.

```Shell
ifconfig interface [[inet|inet6] [<ip-address>|dhcp]] [dr|gw|gateway <dr-address>] [netmask <net-mask>|prefixlen <len>] [dns <dns-address>] [hw <hw-mac>]]
```

| Parameter                               | Description                                                |
| --------------------------------------- | ---------------------------------------------------------- |
| interface                               | Interface name (e.g., eth0 for Ethernet, wlan0 for Wi-Fi). |
| inet/inet6                              | Address family (IPv4/IPv6).                                |
| \<ip-address\>\|dhcp                    | Static IP assignment or DHCP-based dynamic address.        |
| dr\|gw\|gateway \<dr-address\>          | Configure gateway address.                                 |
| netmask \<net-mask\>\|prefixlen \<len\> | Set IP netmask (default derived from IP class).            |
| dns \<dns-address\>                     | Configure DNS server.                                      |
| hw \<hw-mac\>                           | Set hardware MAC address (if supported by driver).         |

## IV. Common Commands

- Enable/disable interfaces:

    ```Bash
    # Enable eth0
    ifup eth0
    
    # Disable eth0
    ifdown eth0
    ```

- Display all interface configurations:

     ```Bash
    ifconfig
    ```

- Show specific interface (e.g., eth0) configuration:
  
    ```Bash
    ifconfig eth0
    ```

- Configure static IPv4 address for eth0:

    ```Bash
    ifconfig eth0 10.0.1.3
    ```

- Full configuration (IP, gateway, netmask, DNS):

    ```Bash
    ifconfig eth0 10.0.1.3 gateway 10.0.1.1 netmask 255.255.255.0 dns 8.8.8.8
    ```

- Configure IPv6 address with prefix length:
  
    ```Bash
    ifconfig eth0 inet6 add 2001:db8::/32
    ```
