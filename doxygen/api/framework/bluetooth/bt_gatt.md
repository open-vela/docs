# 蓝牙 GATT API 开发指南

**通用属性规范 (Generic Attribute Profile, GATT)** 是蓝牙低功耗 (BLE) 数据通信的核心层。它基于 ATT (Attribute Protocol) 构建，定义了两个连接设备之间如何进行数据传输。

GATT 使用层级结构来组织数据：

- **Service (服务)**：功能的逻辑集合（如“心率服务”）。
- **Characteristic (特征)**：实际的数据点（如“心率测量值”）。

## 1. 接口概览

`bt_gatt` 模块的接口设计遵循 GATT 的 C/S (Client/Server) 架构。开发者需根据设备在业务逻辑中扮演的角色，选择对应的接口集。

> **注意**：一个设备可以同时作为 GATT Client 和 GATT Server。

### 1.1 GATT Client 接口 (GATTC)

`bt_gattc` (GATT Client) 模块面向**数据的使用者**。通常是手机 App 或网关设备，它们主动发起请求以获取或控制远程设备的数据。

- **核心职责**：

    - **发现 (Discovery)**：遍历远程设备的 Service 和 Characteristic (UUID)。
    - **读写操作 (Read/Write)**：读取传感器数据或写入控制指令。
    - **订阅 (Subscription)**：配置 CCCD 以接收远程设备的 Notification/Indication 推送。
    - **MTU 协商**：调整最大传输单元以优化吞吐量。

**API 参考：**

```eval_rst

.. doxygenfile:: bt_gattc.h
  :project: doxygen
```

### 1.2 GATT Server 接口 (GATTS)

`bt_gatts` (GATT Server) 模块面向**数据的持有者**。通常是传感器、手环或智能家居终端，它们存储数据并响应 Client 的请求。

- **核心职责**：

    - **属性表构建**：注册本地 Service、Characteristic 及 Descriptor。
    - **请求响应**：处理来自 Client 的 Read/Write 请求（支持回调鉴权）。
    - **主动推送**：当本地数据变化时，通过 Notification 或 Indication 主动通知已订阅的 Client。

**API 参考：**

```eval_rst

.. doxygenfile:: bt_gatts.h
  :project: doxygen
```
