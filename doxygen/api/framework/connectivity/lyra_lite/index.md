# Lyra Lite SDK API 参考手册

**Lyra Lite SDK** 是一套面向物联网设备的轻量级通信开发框架，旨在简化底层协议栈的复杂性，为上层应用提供高效、模块化的连接能力。

本开发指南涵盖了设备生命周期的各个阶段，从系统的初始化、设备的广播与发现，到连接建立后的数据传输、消息中心交互以及复杂的自组网管理。开发者可以根据业务需求，灵活调用以下模块接口构建稳定的物联网应用。

## 目录索引

以下是 Lyra Lite SDK 的核心模块文档索引：

- **广播与发现 (Adv & Disc)**：管理设备的可见性与扫描流程。
- **设备连接管理 (Device)**：处理设备间的连接建立与维护。
- **传输通道 (Transmit)**：提供大数据分包与流控的高效传输管道。
- **消息中心 (Message Center)**：负责控制信令与短消息的交互。
- **组网管理 (Networking)**：构建和维护多设备网络拓扑。
- **SDK 初始化 (SDK Init)**：系统的启动、配置与资源释放。

```eval_rst

.. toctree::
  :maxdepth: 2

  lyra_adv_disc.md
  lyra_device.md
  lyra_transmit.md
  lyra_message_center.md
  lyra_networking.md
  lyra_sdk_init.md

```