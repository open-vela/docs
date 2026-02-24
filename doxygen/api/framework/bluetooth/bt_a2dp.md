# 蓝牙 A2DP API 开发指南

## 1. 概述

**高级音频分发规范 (A2DP)** 定义了在单声道、立体声或多声道模式下传输高质量音频内容的协议和过程。该规范为实现此功能的设备定义了 **源端 (Source/SRC)** 和 **接收端 (Sink/SNK)** 角色。

- **源端 (SRC)**：当设备作为数字音频流的源头，将其传送给微微网 (Piconet) 中的接收端 (SNK) 时，该设备即为 SRC。
- **接收端 (SNK)**：当设备作为数字音频流的接收方，接收同一微微网中源端 (SRC) 传送的数据时，该设备即为 SNK。

常见的 A2DP 接收端设备包括蓝牙耳机、蓝牙音箱和车载蓝牙免提系统。音频流在传输前需要进行压缩和编码。目前，openvela 系统支持两种音频编解码器，包括 **SBC** 和 **AAC**。

### 1.1 音频传输模式

音频流的传输主要有两种截然不同的方式：**硬件卸载 (Offloading)** 和 **非卸载 (Non-offloading)**。这两种模式的主要区别在于蓝牙核心协议栈是否参与音频传输。

- **非卸载模式**：音频流通过蓝牙核心协议栈传输至远端设备。
- **硬件卸载模式**：音频流不经过蓝牙核心协议栈传输。

### 1.2 远程控制说明

需要注意的是，A2DP 仅负责传输音频流数据，不包含远程控制功能。然而，在某些情况下，设备可能会结合 A2DP 和控制规范来支持远程控制功能，例如音视频远程控制规范 (AVRCP) 中所使用的功能。

## 2. A2DP 状态机与连接管理

蓝牙服务通过状态机维护 A2DP 的生命周期。开发过程中需严格区分 **Profile 连接**（控制链路）和 **Audio 连接**（数据链路）。

### 2.1 状态定义

蓝牙服务负责维护 A2DP 的状态机，其中包含空闲 (Idle)、打开中 (Opening)、已打开 (Opened)、已启动 (Started) 和关闭中 (Closing) 等状态。这些状态可分为稳态和瞬态：

- **稳态 (Stable States)**:

    - **Idle (空闲)**：初始状态。
    - **Opened (已打开)**：A2DP 连接已建立。
    - **Started (已启动)**：正在传输音频流。

- **瞬态 (Transient States)**:

    - **Opening (打开中)**：正在建立 A2DP 连接。
    - **Closing (关闭中)**：正在断开 A2DP 连接。

状态变化如下图所示：

![img](./a2dp.png)  

### 2.2 连接与流状态

- **A2DP 连接状态**：包含四种不同状态，分别为 DISCONNECTED (已断开)、CONNECTING (连接中)、CONNECTED (已连接) 和 DISCONNECTING (断开中)。
- **音频流状态**：涉及音频流的状态，包括 Started (已启动) 和 Stopped (已停止)。

此外，A2DP 流仅在 Profile 连接建立后专用于传输音频数据。应用程序 (APP) 能够接收有关 A2DP 连接状态变化以及 A2DP 音频状态变化的通知。

框架提供了一个名为 `bttool` 的测试工具。该工具通过调用 A2DP 接口，协助与远程设备建立 A2DP 连接。关于如何使用 `bttool` 命令的详细指南，请参阅 `bttool` 命令手册。

## 3. 开发工具

框架提供了命令行测试工具 `bttool`，用于验证 A2DP 功能。开发者可通过该工具调用底层接口，快速与远程设备建立连接并进行音频测试。

- **参考文档**：请查阅 `bttool` 命令手册获取详细指令说明。

## 4. API 参考

### 4.1 通用接口 (Common)

#### A2DP API

```eval_rst

.. doxygenfile:: bt_a2dp.h
  :project: doxygen
```

### 4.2 A2DP 接收端 (Sink)

A2DP Sink 设备负责接收音频流。A2DP Sink 定义了一些特定行为：

- **初始化**：初始化后，A2DP Sink 处于 Idle 状态并注册相关回调函数。
- **状态通知**：当状态发生变化时，A2DP Sink 会将状态变更结果发送给 APP。
- **连接管理**：A2DP Sink 可以主动连接 A2DP Source 设备，也可以主动断开连接。
- **状态查询**：此外，APP 还可以检查 A2DP Sink 是否已连接、判断 A2DP Sink 是否正在播放，以及获取 A2DP Sink 当前的连接状态。

#### A2DP Sink API 详情

```eval_rst

.. doxygenfile:: bt_a2dp_sink.h
  :project: doxygen
```

### 4.3 A2DP 源端 (Source)

A2DP Source 设备负责发送音频流。A2DP Source 定义了一些特定行为：

- **初始化**：初始化后，A2DP Source 处于 Idle 状态并注册相关回调函数。
- **状态通知**：当状态发生变化时，A2DP Source 会将状态变更结果发送给 APP。
- **连接管理**：A2DP Source 设备可以主动连接 A2DP Sink 设备，也可以主动断开连接。
- **状态查询**：此外，APP 还可以调用 A2DP Source 提供的接口来检查是否已连接、判断是否正在播放，以及获取当前的连接状态。
- **多设备支持**：当 A2DP Source 设备连接到多个 A2DP Sink 设备时，A2DP Source 可以设置静音 (Silence) 的 Sink 设备和活动 (Active) 的 Sink 设备。

#### A2DP Source API 详情

```eval_rst

.. doxygenfile:: bt_a2dp_source.h
  :project: doxygen
```
