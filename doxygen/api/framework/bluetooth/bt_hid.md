# 蓝牙 HID API 开发指南

**人机接口设备规范 (Human Interface Device Profile, HID)** 定义了蓝牙设备如何与主机进行低延迟的人机交互。它允许鼠标、键盘、游戏手柄等设备（HID Device）通过蓝牙无线控制计算机、平板或手机（HID Host）。

## 1. API 接口概览

本模块接口主要针对 **HID Device (设备端)** 角色设计。

`bt_hid_device.h` 模块面向**外设开发**。开发者利用此接口将设备模拟为标准的输入/输出设备。

- **适用场景**：蓝牙键盘、鼠标、游戏控制器、遥控器等。

- **核心功能**：

    - **连接管理**：注册 HID 服务记录 (SDP)，管理与主机的连接与断开。
    - **发送报告 (Send Input Report)**：向主机发送按键点击、鼠标移动或传感器数据。
    - **接收报告 (Receive Output Report)**：处理来自主机的反馈数据（如键盘的大小写锁定 LED 灯指令、手柄震动指令）。
    - **协议模式切换**：支持 Boot Protocol（引导模式，用于BIOS等简单环境）与 Report Protocol（报告模式，用于操作系统）的切换。
    - **虚拟拔插 (Virtual Cable Unplug)**：发送控制指令以断开并移除配对关系。

**API 详情：**

```eval_rst

.. doxygenfile:: bt_hid_device.h
    :project: doxygen
```