# 蓝牙 GAP API 开发指南

**通用访问规范 (Generic Access Profile, GAP)** 是蓝牙协议栈的基础层，定义了蓝牙设备如何发现彼此、建立连接以及管理安全认证。它主要负责处理设备未连接时的行为（如广播、扫描）以及连接建立后的安全配置。

在 openvela 系统中，GAP 接口主要围绕 **本地蓝牙适配器 (Local Bluetooth Adapter)** 的管理展开。

## 1. 接口概览

`bt_adapter` 模块提供了蓝牙基础功能的控制入口。整体接口设计根据使用场景分为两类：

### 1.1 应用开发接口 (Application APIs)

这是面向最终应用开发者的核心接口，封装了标准的蓝牙业务逻辑。

- **功能范围**：
  
    - 蓝牙协议栈的初始化与去初始化 (Enable/Disable)。
    - 设备属性配置（如设备名称、本地地址查询）。
    - 扫描 (Scanning) 与广播 (Advertising) 参数设置。
    - 配对与绑定管理 (Pairing & Bonding)。

- **适用场景**：常规的蓝牙业务开发，如连接耳机、数据传输、HID 设备交互等。

### 1.2 诊断与调试接口 (Debug & Test APIs)

这是一组面向底层验证和系统调试的扩展接口。

- **功能范围**：

    - 强制模式切换。
    - 射频 (RF) 测试模式控制。
    - 底层状态转储 (State Dump)。

- **适用场景**：工厂生产测试 (PTS)、硬件认证、故障排查。

### API 详情

```eval_rst

.. doxygenfile:: bt_adapter.h
    :project: doxygen
```
