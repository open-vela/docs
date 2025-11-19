# Sensor 配置选项

\[ [English](../../../../../en/device_dev_guide/driver/peripheral_driver/sensor/sensor_config.md) | 简体中文 \]

本文详细介绍 openvela Sensor 的核心 Kconfig 配置项，涵盖主框架、多核通信以及各类虚拟与仿真驱动。

## 一、核心框架

此选项是启用所有传感器功能的基础。

- **`CONFIG_SENSORS`：启用传感器子系统。**

    作为传感器框架的总开关，此选项用于编译和初始化传感器驱动的核心抽象层。您必须启用此配置，系统才能支持任何传感器设备。

## 二、多核通信支持

此选项用于在多核处理器（MPU）环境中实现传感器数据的高效流转。

- **`CONFIG_SENSORS_RPMSG`：启用基于 RPMsg 的传感器多核通信。**

    此选项为传感器子系统增加基于 RPMsg（Remote Processor Messaging）协议的通信能力。启用后，系统允许 uORB 主题（Topics）在不同处理器核心之间进行传输、发布和订阅，是异构多核架构下实现跨核数据共享的关键。

## 三、虚拟与仿真驱动

虚拟与仿真驱动主要用于开发和测试阶段，允许在没有物理硬件的环境中模拟传感器数据。

- **`CONFIG_SENSORS_FAKESENSOR`：启用伪传感器（Fake Sensor）驱动。**

    该驱动通过读取文件系统中的预设数据来模拟真实的传感器输入，并将其发布为 uORB 主题。此功能使您可以在脱离硬件的环境中，独立进行上层应用逻辑的开发与调试。

- **`CONFIG_SENSORS_GOLDFISH_SENSOR`：启用 Goldfish 模拟器传感器驱动。**

    当您在 Android Goldfish 模拟器环境中运行 NuttX 时，请启用此选项。它能够从模拟器获取虚拟传感器（如加速度计、陀螺仪）的数据。

    - **`CONFIG_SENSORS_GOLDFISH_GNSS`：启用 Goldfish 模拟器 GNSS 驱动。**

        此为 `CONFIG_SENSORS_GOLDFISH_SENSOR` 的一个子选项，专门用于从模拟器获取虚拟的 GNSS（全球导航卫星系统）位置数据。

- **`CONFIG_SENSORS_WTGAHRS2`：启用 WTGAHRS2 传感器驱动。**

    此选项用于编译 WTGAHRS2 AHRS（姿态和航向参考系统）传感器的驱动程序。该驱动既可以连接真实的传感器硬件，也可在仿真环境中使用，为系统提供姿态数据。

## 四、配置文件路径

相关的 Kconfig 文件位于以下路径：

- **传感器驱动 Kconfig**：`drivers/sensors/Kconfig`
- **uORB Kconfig**：`apps/system/uorb/Kconfig`

## 五、相关文档

更多关于 uORB 的配置信息，请参阅以下文档：

- **uORB 配置**：[uORB配置](../../../middleware/uorb_config.md)
