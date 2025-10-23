# uORB 配置选项

[[English](../../../en/device_dev_guide/middleware/uorb_config.md) | 简体中文]

本文介绍 uORB 框架及其相关工具链在 Kconfig 中的核心配置项。

### 一、核心框架

以下是启用 uORB 核心功能所需的基本配置项。

- **`CONFIG_UORB`：启用 uORB 消息中间件**。

    这是 uORB 的核心开关，用于编译和启用其发布-订阅（Publish-Subscribe）消息内核，为系统提供高效、异步的通信机制。

- **`CONFIG_USENSOR`：启用 NuttX 传感器框架**。

    此选项用于编译传感器驱动的上层抽象（Upper Half），为系统提供标准的字符设备接口（如 `/dev/sensor*`）。它通常是 uORB 在传感器子系统中应用的基础。

### 二、开发与测试工具

这些选项用于构建 uORB 的命令行工具和测试套件，方便开发者进行调试和验证。

- **`CONFIG_UORB_LISTENER`：构建 `uorb listener` 命令行工具。**

    开发者可在 Shell 中使用此命令，实时监控主题（Topic）的发布状态、订阅者数量和数据更新情况。

- **`CONFIG_UORB_TESTS`：构建 uORB 单元测试套件。**

    用于编译 uORB 框架的自测试程序，可用于验证 uORB 内核功能的正确性、性能和稳定性。

### 三、调试选项

此选项用于增强调试能力，获取更详细的运行时信息。

- **`CONFIG_DEBUG_UORB`：启用 uORB 详细调试信息。**

    启用后，`uorb listener` 等工具可以打印出每个主题消息的完整数据结构，而不仅仅是摘要。这对于深度调试特定数据流和内容至关重要。
