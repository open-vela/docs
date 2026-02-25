# 蓝牙 API 开发指南

本手册旨在指导开发者在 **openvela** 系统上进行蓝牙协议栈的配置与应用开发。文档体系涵盖了从底层的连接管理（GAP/GATT）到经典蓝牙的上层应用规范（Profiles），支持构建音频流传输、语音通话、人机交互及数据透传等多种应用场景。

## 1. 协议栈模块索引

开发者可根据具体的应用需求，参考以下分类文档：

### 1.1 基础核心 (Core)

构建蓝牙应用的基石，涉及设备发现、连接建立及通用数据交换。

- **GAP (Generic Access Profile)**：通用访问规范。负责广播、扫描、配对及链路安全管理。
- **GATT (Generic Attribute Profile)**：通用属性规范。负责低功耗蓝牙 (BLE) 及部分经典蓝牙的数据属性读写与通知。

### 1.2 音频与媒体 (Audio & Media)

面向蓝牙耳机、音箱及车载系统的多媒体功能。

- **A2DP (Advanced Audio Distribution Profile)**：高级音频分发。用于传输高质量的立体声音乐。
- **AVRCP (Audio/Video Remote Control Profile)**：音视频远程控制。用于控制播放暂停、切歌及音量调节。
- **HFP (Hands-Free Profile)**：免提规范。用于实现蓝牙通话功能。

### 1.3 数据与外设 (Data & Peripherals)

面向数据传输、网络共享及人机交互设备。

- **HID (Human Interface Device Profile)**：人机接口设备。用于开发键盘、鼠标、游戏手柄等输入设备。
- **SPP (Serial Port Profile)**：串口仿真。用于替代物理串口进行数据透传。
- **PAN (Personal Area Network Profile)**：个人局域网。用于通过蓝牙实现网络共享 (Tethering) 或组网。

## 2. 文档列表

详细 API 说明请参阅下表：

```eval_rst

.. toctree::
  :maxdepth: 2

  bt_a2dp.md
  bt_avrcp.md
  bt_gap.md
  bt_gatt.md
  bt_hfp.md
  bt_hid.md
  bt_spp.md
  bt_pan.md

```
