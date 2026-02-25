# 蓝牙 PAN API 开发指南

**个人局域网规范 (Personal Area Network Profile, PAN)** 允许蓝牙设备通过 BNEP (Bluetooth Network Encapsulation Protocol) 封装网络协议包（如 IPv4/IPv6），从而构建无线局域网。

该协议主要用于以下场景：

- **蓝牙网络共享 (Tethering)**：手机作为网关，让其他设备通过蓝牙共享其移动网络连接。
- **本地组网**：多个设备在没有外部网络的情况下组成临时的 Ad-hoc 网络进行通信。

在 PAN 架构中，主要涉及以下角色：

- **PANU (PAN User)**：PAN 用户端。通常指连接到网关以获取网络服务的设备（如：连接手机热点的平板电脑）。
- **NAP (Network Access Point)**：网络接入点。提供网络连接服务的网关设备（如：开启蓝牙热点的手机）。

## 1. API 接口概览

`bt_pan` 模块提供了管理蓝牙网络连接及数据传输的接口。

### 1.1 PAN 协议接口

`bt_pan.h` 定义了 PAN Profile 的通用操作，支持设备作为 PANU 或 NAP 进行连接和数据交互。

- **核心功能**：

    - **服务注册**：注册 PANU 或 NAP 服务记录 (SDP)，声明设备支持的网络角色。
    - **连接管理**：建立或断开基于 BNEP 的网络连接。
    - **数据传输**：在蓝牙链路与上层 TCP/IP 协议栈之间转发以太网帧。
    - **多路复用**：支持同时处理多个设备的网络连接（通常针对 NAP 角色）。

**API 详情：**

```eval_rst

.. doxygenfile:: bt_pan.h
  :project: doxygen
```
