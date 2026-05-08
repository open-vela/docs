# 网络接口

openvela 包括一个全面的网络子系统，提供标准的 BSD 套接字接口和 DNS 解析功能。网络子系统是可选的，可以根据应用需求进行配置。openvela 提供的网络接口遵循 POSIX 标准，可以很容易地将现有的网络应用程序移植到 openvela。

## 核心接口

- **[网络接口](net.md)** — BSD 套接字接口（socket/bind/connect/send/recv）与 DNS 解析

## 地址管理与配置

- **[DHCP](net_dhcp.md)** — DHCP 客户端（IPv4）、DHCPv6 客户端与 DHCP 服务器
- **[网络工具库 netlib](netlib.md)** — IPv4/IPv6 地址、路由、MAC、MTU、iptables、连通性检查等辅助接口

## 无线网络

- **[WAPI 无线接口](wapi.md)** — Wi-Fi 接口配置、扫描、关联、功率管理（基于 Linux Wireless Extensions）

## 文件服务

- **[FTP 服务器](net_ftp.md)** — 轻量 FTP 服务器接口
