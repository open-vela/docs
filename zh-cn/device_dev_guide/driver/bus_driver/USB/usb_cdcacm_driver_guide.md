# USB CDC-ACM 类驱动程序指南

\[ [English](../../../../../en/device_dev_guide/driver/bus_driver/USB/usb_cdcacm_driver_guide.md) | 简体中文 \]

## 一、概述

本文档旨在为开发者提供在 **openvela** 系统中配置和使用 USB 通信设备类 (Communication Device Class, CDC) 的抽象控制模型 (Abstract Control Model, ACM) 驱动程序的详细指南。

CDC-ACM 是一种标准的 USB 协议，它能够在主机和设备之间模拟一个虚拟串口，广泛应用于调试、日志输出和数据传输等场景。该协议主要定义了两种通信端点 (Endpoint)：

- **控制端点 (Control Endpoint)**：用于传输和配置虚拟串口的控制类信息，例如波特率、数据位等。
- **数据端点 (Data Endpoint)**：用于双向传输实际的串行数据。

## 二、在 USB Device 模式下使用 CDC-ACM

当您需要将 openvela 设备模拟成一个 USB 虚拟串口设备（如开发板连接 PC 后出现一个 COM 口）时，请参考本章节进行配置。驱动及相关接口的通用适配方法，请参考 [USB Device 驱动开发指南](./usb_driver_dev_guide.md)。

### 1、单一设备模式

在此模式下，USB 设备仅作为 CDC-ACM 设备存在。

#### Kconfig 配置

请在项目的 `defconfig` 文件中启用以下核心配置：

```Makefile
# 启用 USB Device 核心驱动
CONFIG_USBDEV=y                     
# 启用 CDC-ACM 设备类驱动
CONFIG_CDCACM=y                     
# 启用接口关联描述符 (IAD)，用于在复合设备中正确标识功能组
CONFIG_COMPOSITE_IAD=y              

# --- 可选配置 ---
# 启用 USB 高速模式
CONFIG_USBDEV_DUALSPEED=y           
# 启用 USB DMA 传输
CONFIG_USBDEV_DMA=y                 

# 自定义设备 VID (Vendor ID)
CONFIG_CDCACM_VENDORID
# 自定义设备 PID (Product ID)
CONFIG_CDCACM_PRODUCTID
```

#### 初始化

您需要在系统启动流程中调用 `cdcacm_initialize()` 函数来初始化 CDC-ACM 设备。openvela 系统已实现此函数。

推荐的调用位置是在板级初始化函数 `up_initialize()` 中，或在检测到 USB 连接的特定线程中。

### 2、复合设备模式

在此模式下，CDC-ACM 与其他 USB 功能（如 ADB、RNDIS）组合成一个复合设备。

#### Kconfig 配置

```Makefile
# --- USB 核心配置 ---
CONFIG_USBDEV=y                     
# 启用 USB 复合设备框架
CONFIG_USBDEV_COMPOSITE=y           
# 启用接口关联描述符 (IAD)
CONFIG_COMPOSITE_IAD=y

# --- CDC-ACM 相关配置 ---
CONFIG_CDCACM=y
# 使能 CDC-ACM 在复合设备模式下的支持
CONFIG_CDCACM_COMPOSITE=y


# --- 可选配置 ---
CONFIG_USBDEV_DUALSPEED=y           
CONFIG_USBDEV_DMA=y                 
CONFIG_CDCACM_VENDORID
CONFIG_CDCACM_PRODUCTID
```

#### 初始化

在复合设备模式下，您需要为您的硬件平台实现两个板级支持 (BSP) 函数，用于描述和连接复合设备。

- `board_composite_initialize()`: 执行复合设备所需的架构特定初始化。
- `board_composite_connect()`: 根据配置 ID 连接并注册包含 CDC-ACM 在内的各个 USB 功能。

这两个函数通常也在 `up_initialize()` 过程中或 USB 连接线程中被调用。

以下是一个 `board_composite_connect()` 的实现示例，展示了如何将 CDC-ACM 添加到复合设备中：

```C++
#ifdef CONFIG_USBDEV_COMPOSITE

/****************************************************************************
 * Name: board_composite_initialize
 *
 * Description:
 *   Perform architecture specific initialization of a composite USB device.
 *
 ****************************************************************************/
int board_composite_initialize(int port)
{
  return OK;
}

/****************************************************************************
 * Name:  board_composite_connect
 *
 * Description:
 *   Connect the USB composite device on the specified USB device port using
 *   the specified configuration.  The interpretation of the configid is
 *   board specific.
 *
 * Input Parameters:
 *   port     - The USB device port.
 *   configid - The USB composite configuration
 *
 * Returned Value:
 *   A non-NULL handle value is returned on success.  NULL is returned on
 *   any failure.
 *
 ****************************************************************************/
void *board_composite_connect(int port, int configid)
{
  struct composite_devdesc_s dev[2];
  int ifnobase = 0;
  int strbase = COMPOSITE_NSTRIDS - 1;
  int dev_idx = 0;

#ifdef CONFIG_USBADB
  /* Configure the ADB USB device */
  
    ......

#endif

#ifdef CONFIG_CDCACM
  /* Configure the CDC/ACM device */
  cdcacm_get_composite_devdesc(&dev[dev_idx]);

  /* The callback functions for the CDC/ACM class */
  dev[dev_idx].classobject = cdcacm_classobject;
  dev[dev_idx].uninitialize = cdcacm_uninitialize;

  /* Interfaces */
  dev[dev_idx].devinfo.ifnobase = ifnobase;
  dev[dev_idx].minor = 0;

  /* Strings */
  dev[dev_idx].devinfo.strbase = strbase;

  /* Endpoints */
  dev[dev_idx].devinfo.epno[CDCACM_EP_INTIN_IDX] = 3;
  dev[dev_idx].devinfo.epno[CDCACM_EP_BULKIN_IDX] = 4;
  dev[dev_idx].devinfo.epno[CDCACM_EP_BULKOUT_IDX] = 5;

  /* Count up the base numbers */
  ifnobase += dev[dev_idx].devinfo.ninterfaces;
  strbase += dev[dev_idx].devinfo.nstrings;

  dev_idx += 1;
#endif

  return composite_initialize(composite_getdevdescs(), dev, dev_idx);
}

#endif /* CONFIG_USBDEV_COMPOSITE */
```

### 3、测试指南

参考 [USB 设备模拟 (SIM) 驱动程序指南](./sim/usb_device_sim_guide.md#三使用指南usb-功能测试)

## 三、在 USB Host 模式下使用 CDC-ACM

当您需要让 openvela 设备作为主机，去连接并控制一个外部的 CDC-ACM 设备（如 USB 转串口模块）时，请参考本章节进行配置。驱动及相关接口的通用适配方法，请参考 [USB Host 驱动程序开发指南](./usb_driver_host_guide.md)。

### 1、Kconfig 配置

```Makefile
# --- USB Host 核心配置 ---
CONFIG_USBHOST=y                    
# 启用对 USB 复合设备的支持
CONFIG_USBHOST_COMPOSITE=y      

# --- CDC-ACM Host 相关配置 ---
CONFIG_USBHOST_CDCACM=y              
# 启用对复合设备中 CDC-ACM 功能的支持
CONFIG_CDCACM_COMPOSITE=y            
# 减少内存占用的简化模式
CONFIG_USBHOST_CDCACM_REDUCED=y      
```

### 2、初始化

您需要在系统启动流程中调用 `usbhost_cdcacm_initialize()` 函数，以向 USB Host 核心注册 CDC-ACM 类驱动。当一个兼容的 CDC-ACM 设备连接到 Host 时，该驱动将被自动加载和枚举。

以下是在 `sim` 平台上的初始化示例：

```C++
int sim_usbhost_initialize(void)
{
  struct sim_usbhost_s *priv = &g_sim_usbhost;
  struct usbhost_hubport_s *hport;
  int ret;

#ifdef CONFIG_USBHOST_CDCACM
  ret = usbhost_cdcacm_initialize();
#endif

   ......

}
```

### 3、测试指南

初始化完成后，当您将一个外部 USB 串口设备连接到 openvela 主机时，系统 `/dev` 目录下应自动创建设备节点（如 `/dev/ttyACM0`）。您可以像操作普通串口一样，通过读写此设备节点与外部设备通信。详细测试方法请参考 [USB Host 驱动程序开发指南](./usb_driver_host_guide.md)。

## 四、参考资料

- [USB 设备模拟 (SIM) 驱动程序指南](./sim/usb_device_sim_guide.md)
- [USB 主机模拟 (SIM) 驱动程序指南](./sim/usb_host_sim_guide.md)
- [USB Host 驱动程序开发指南](./usb_driver_host_guide.md)