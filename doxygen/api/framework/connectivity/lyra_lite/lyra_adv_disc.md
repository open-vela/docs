# Lyra Lite 广播与发现 API 开发指南

**Lyra Lite** 模块提供了轻量级的低功耗蓝牙 (BLE) **广播 (Advertising)** 与 **发现 (Discovery)** 功能封装。

该模块允许设备对外发送广播包以声明自身存在或传输无连接数据，同时支持扫描周围环境以发现其他设备。它是构建设备间连接、信标（Beacon）应用及近场交互的基础。

## 1. 接口概览

本模块的接口设计涵盖了广播与发现功能的完整生命周期管理，主要包括：

- **广播管理**：配置广播参数、启动/停止广播、动态更新广播数据以及查询当前广播状态。
- **发现管理**：配置扫描参数、启动/停止扫描、注册/注销设备发现的回调监听器，以及查询扫描状态。

### 1.1 广播接口 (Advertising API)

该部分主要负责控制设备作为**广播者 (Broadcaster)** 或**外设 (Peripheral)** 时的行为。

#### 1.1.1 广播类型定义

`advertising_types.h` 定义了配置广播所需的数据结构与枚举，包括广播模式、广播间隔、广播数据包格式等参数配置。

```eval_rst

.. doxygenfile:: advertising_types.h
  :project: doxygen
```

#### 1.1.2 广播功能接口

`advertising.h` 提供了控制广播状态的核心函数，支持开启广播、停止广播以及在广播过程中更新 Payload 数据。

```eval_rst

.. doxygenfile:: advertising.h
  :project: doxygen
```

### 1.2 发现接口 (Discovery API)

该部分主要负责控制设备作为**观察者 (Observer)** 或**中心设备 (Central)** 时的行为，用于扫描周围的广播设备。

#### 1.2.1 发现类型定义

`discovery_types.h` 定义了与扫描相关的数据结构，包括扫描窗口、扫描间隔、过滤策略以及扫描结果（如 RSSI、设备地址、原始数据）的结构体定义。

```eval_rst

.. doxygenfile:: discovery_types.h
  :project: doxygen
```

#### 1.2.2 发现功能接口

`discover.h` 提供了扫描控制与结果处理的接口，支持注册监听回调以接收发现的设备信息，以及控制扫描的启停。

```eval_rst

.. doxygenfile:: discover.h
  :project: doxygen
```
