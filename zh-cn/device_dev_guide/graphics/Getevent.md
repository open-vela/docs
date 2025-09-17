# getevent 工具使用指南

\[ [English](../../../en/device_dev_guide/graphics/Getevent.md) | 简体中文 \]

`getevent` 是一个命令行工具，用于实时监控并显示来自触摸屏、键盘、鼠标等输入设备的事件。它通过提供详细的事件数据，帮助您调试输入设备驱动和应用程序。

## 一、功能特性

`getevent` 提供以下核心功能：

- **鼠标事件监控**：跟踪点击、移动和滚轮活动。
- **多点触控捕获**：捕获每个触摸点的坐标和时间戳等数据。
- **键盘按键检测**：报告按键码和事件类型（如按下、释放）。
- **设备自动发现**：默认扫描 `/dev` 目录并监控所有检测到的输入设备。
- **指定设备监控**：允许您通过命令行选项监控一个或多个特定设备。
- **非阻塞 I/O**：采用 500 毫秒超时的非阻塞模式，避免在等待事件时挂起系统。
- **资源安全管理**：确保在退出时（例如通过 `Ctrl+C`）能正确释放资源，防止内存或文件描述符泄漏。

## 二、构建配置

要启用 `getevent` 工具，您必须在 openvela 的板级配置文件中设置以下选项：

```Makefile
# 启用 getevent 工具
CONFIG_GRAPHICS_INPUT_GETEVENT=y

# (可选)启用 getevent 的详细调试信息
CONFIG_GRAPHICS_INPUT_GETEVENT_DETAIL_INFO=y
```

## 三、使用说明

您可以从 openvela 的命令行终端（如 NSH）运行 `getevent`。

### 命令示例

- **监控所有自动检测到的设备：**

    ```Bash
    getevent
    ```

- **监控指定的鼠标设备：**

    ```Bash
    getevent -m /dev/mouse0
    ```

- **监控指定的触摸屏设备：**

    ```Bash
    getevent -t /dev/input0
    ```

- **监控指定的键盘设备：**

    ```Bash
    getevent -k /dev/kbd0
    ```

- **同时监控多个设备：**

    ```Bash
    getevent -m /dev/mouse0 -t /dev/input0
    ```

要停止监控，请按 `Ctrl+C`，程序将安全终止。

### 参数说明

| 参数 | 说明                                         |
| :--- | :------------------------------------------- |
| -m   | 指定要监控的鼠标设备。例如 : `/dev/mouse0`   |
| -t   | 指定要监控的触摸屏设备。例如 : `/dev/input0` |
| -k   | 指定要监控的键盘设备。例如 : `/dev/kbd0`     |

### 输出示例

当您运行 `getevent` 时，它会首先列出正在打开的设备，然后实时打印事件数据。

```Bash
goldfish-armv7a-ap> getevent

[getevent]: opening /dev/input0
[getevent]: ioctl TSIOC_GETMAXPOINTS: 1
[getevent]: opening /dev/kbd0
[getevent]: opening /dev/mouse0

# 触摸屏事件数据
[getevent]: touch event: /dev/input0
[getevent]:    npoints : 1
[getevent]: Point      : 0
[getevent]:      flags : 11             # 触摸事件标志 (例如：按下、移动)
[getevent]:          x : 493
[getevent]:          y : 312
[getevent]:  timestamp : 31272800

# 键盘事件数据
[getevent]: keyboard event: /dev/kbd0
[getevent]:          type : 0           # 0代表KEY_DOWN(按下), 1代表KEY_UP(释放)
[getevent]:          code : 57          # 按键码，例如 SPACE 键

[getevent]: keyboard event: /dev/kbd0
[getevent]:          type : 1
[getevent]:          code : 57

# 鼠标事件数据
[getevent]: mouse event: /dev/mouse0
[getevent]:    buttons : 00              # 按钮状态的位掩码
[getevent]:          x : 14              # 水平方向的相对位移
[getevent]:          y : -16             # 垂直方向的相对位移
```

## 四、先决条件

要成功构建和运行 `getevent`，您的系统必须满足以下先决条件：

- **输入子系统**：您必须在配置中启用 openvela 输入子系统。该子系统为 `getevent` 提供了处理事件所需的底层驱动和事件处理机制。详情请参见 [Input 驱动开发指南](./Input_Driver_Guide.md)。
- **系统日志 (推荐)**：为了便于调试，我们建议您在内核配置中启用系统日志输出。当 `CONFIG_GRAPHICS_INPUT_GETEVENT_DETAIL_INFO` 被启用时，`getevent` 可以打印更详细的诊断消息。