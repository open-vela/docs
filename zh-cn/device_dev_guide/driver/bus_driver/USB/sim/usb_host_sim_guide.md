# USB Host 模拟 (SIM) 驱动程序指南

\[ [English](../../../../../../en/device_dev_guide/driver/bus_driver/USB/sim/usb_host_sim_guide.md) | 简体中文 \]

本文档详细介绍在 openvela 仿真 (SIM) 环境中 USB 主机 (Host) 驱动程序的架构与使用方法。

## 一、架构解析

该驱动程序采用分层设计，由两部分协同工作：

- **openvela 仿真侧驱动(SIM USB Host Driver)**：在 openvela 仿真环境中运行，负责实现上层接口。
- **主机侧驱动(Host USB Host Driver)**：在开发主机（如 Linux）上运行，利用 `libusb` 模拟硬件行为。

此架构解耦了 openvela USB 主机协议栈与底层硬件模拟，提高了驱动的可移植性。

![alt text](./../figures/009.png)

### 1、仿真侧驱动(SIM USB Host Driver)

该驱动程序运行于 openvela 仿真环境内部，主要负责以下功能：

- **实现 USB 主机核心接口**：实现 `usbhost` 和 `usbhost connect` 操作接口，供  openvela 的 USB 主机类驱动调用。
- **抽象底层驱动接口**：定义一套标准接口，用于和运行在外部开发主机上的**主机侧驱动**通信。这种设计使其能轻松适配不同的开发主机操作系统（如 Linux、Windows）。

默认配置下，该驱动支持 CDC-ACM (Communications Device Class - Abstract Control Model) 复合设备，可直接与 openvela 的 SIM USB Device 设备进行连接和调试。

### 2、主机侧驱动 (Host USB Host Driver)

该驱动程序运行于开发主机上，通过 `libusb` 库与连接到主机的物理或虚拟 USB 设备进行通信，从而模拟真实的 USB 主机控制器硬件。其核心功能包括：

- **管理连接状态**：通过 `libusb` 接口获取指定 USB 设备的连接与断开状态。
- **管理描述符信息**：通过 `libusb` 接口获取指定 USB 设备的配置、接口、端点等描述信息。
- **模拟 USB 设备枚举**：模拟 USB 设备的枚举过程。目前版本只支持 `SetConfiguation` 请求。
- **模拟端点传输**：模拟不同类型的端点数据传输。当前版本支持中断 (Interrupt) 和批量 (Bulk) 传输。

#### libusb 库简介

`libusb` 是一个开源库，它提供了一系列用户空间 (User Space) API，允许应用程序直接与 USB 设备交互，而无需编写内核驱动程序。

- **`libusb_init`**：初始化 `libusb` 上下文。在调用任何其他 `libusb` 函数之前，必须先调用此函数。

    ```C
    int libusb_init(libusb_context ** ctx)
    ```

- **`libusb_open`**：打开一个指定的 USB 设备，并返回一个设备句柄用于后续操作。

    ```C
    int libusb_open(libusb_device * dev, libusb_device_handle ** dev_handle)
    ```

- **`libusb_get_config_descriptor`**：获取指定 USB 设备的配置描述符。

    ```C
    int libusb_get_config_descriptor(libusb_device * dev,
                                     uint8_t config_index,
                                     struct libusb_config_descriptor ** config)
    ```

- **`libusb_control_transfer`**：向指定 USB 设备发送控制包。

    ```C
    int libusb_control_transfer(libusb_device_handle * dev_handle,
                                uint8_t bmRequestType,
                                uint8_t bRequest,
                                uint16_t wValue,
                                uint16_t wIndex,
                                unsigned char * data,
                                uint16_t wLength,
                                unsigned int timeout)
    ```

- **`libusb_bulk_transfer`**：向指定 USB 设备发送批量 Bulk 包。

    ```C
    int libusb_bulk_transfer(libusb_device_handle * dev_handle,
                             unsigned char endpoint,
                             unsigned char * data,
                             int length,
                             int * transferred,
                             unsigned int timeout)
    ```

更多关于 libusb 1.0 的 API 信息，请参考 [libusb 官方 API 文档](https://libusb.sourceforge.io/api-1.0/index.html)。

## 二、使用指南

### 1、前提条件：安装 libusb

在您的开发主机（以 Ubuntu 为例）上，使用以下命令安装 `libusb-1.0` 开发库：

```Bash
sudo apt-get -y install libusb-1.0-0-dev
```

安装完成后，头文件通常位于 `/usr/include/libusb-1.0/libusb.h`。

### 2、操作步骤

#### 步骤 1：编译并运行 USB Host 仿真环境

执行以下命令编译并启动 USB Host 仿真程序。请注意，该程序需要管理员权限运行以访问 USB 设备。

```Bash
# 编译
./build.sh sim:usbhost -j8
# 以管理员权限运行
sudo ./nuttx/nuttx
```

#### 步骤 2：编译并运行 USB Device 仿真环境

在另一个终端窗口中，编译并运行 USB Device 仿真程序。

```Bash
# 编译
./build.sh sim:usbdev -j8
# 运行
sudo ./nuttx/nuttx
```

关于 USB Device 的详细信息，请参考 [USB 设备模拟 (SIM) 驱动程序指南](./usb_device_sim_guide.md)。

#### 步骤 3：建立连接与设备使能

在 **USB Device** 仿真环境的 NSH 终端中，执行 `conn 1` 命令以使能 CDC-ACM 设备：

```Bash
# 在 USB Device 终端中执行
NuttShell (NSH) NuttX-10.3.0
nsh> conn 1
```

此时，您应该能在 **USB Host** 仿真环境的终端中看到设备成功注册的消息，系统创建了一个名为 `/dev/ttyACM0` 的设备节点。

```Bash
# USB Host 终端的预期输出
usbhost_connect: Register device: /dev/ttyACM0
usbhost_classbind: Returning: 0
```

#### 步骤 4：验证数据通信

现在，您可以通过 `/dev/ttyACM0` 设备节点在 Host 和 Device 之间进行双向通信。

- **从 Device 发送数据到 Host。**

    在 **Device** 终端中，使用 `echo` 命令向设备节点写入数据：

    ```Bash
    # Device 终端
    nsh> echo hello > /dev/ttyACM0
    ```

- **在 Host 接收数据。**

    在 **Host** 终端中，使用 `cat` 命令读取设备节点。您将看到从 Device 发送的 "hello" 字符串。

    ```Bash
    # Host 终端
    nsh> cat /dev/ttyACM0 &
    sh [7:100]
    nsh> usbhost_setup: Entry
    hello
    ```

​    至此，您已成功完成了仿真环境下 USB Host 与 Device 的通信验证。
