# USB Host 驱动程序开发指南

\[ [English](../../../../../en/device_dev_guide/driver/bus_driver/USB/usb_driver_host_guide.md) | 简体中文 \]

本文档为开发者提供在 **openvela** 系统中开发和适配 USB Host 驱动程序的详细指南。

## 一、架构概述

openvela 的 USB Host 驱动框架遵循分层设计，将驱动程序清晰地划分为两个核心部分：

- **USB Host 控制器驱动 (`usbhost_controller`)**：这是与硬件紧密相关的底层驱动。开发者需要根据具体的 USB Host 控制器芯片（如 EHCI, OHCI, xHCI 等）来实现这一层。其主要职责包括：

    - **端点 0 (EP0) 配置**：管理用于设备枚举和控制传输的默认端点。
    - **资源管理**：负责端点 (Endpoint) 和 I/O 缓冲区的分配与释放。
    - **数据传输**：处理控制端点和其它端点的传输，包括接收、发送和停止传输等功能。
    - **连接管理**：管理 USB 设备连接和释放过程。

- **USB Host 类驱动 (`usbhost_class`)**：这是独立于硬件的上层驱动，用于实现对特定 USB 设备类（如 Mass Storage, CDC-ACM, HID）的支持。openvela 系统已提供多种标准的类驱动。其主要职责是：

    - **连接管理**：USB 设备连接到当前类驱动或断开连接。

下图展示了这两层之间的关系：

![alt text](./figures/010.png)

## 二、核心 API 参考

openvela 的 USB Host 驱动接口均在头文件 `include/nuttx/usb/usbhost.h` 中定义。要为新硬件适配 USB Host 功能，您主要需要实现与 **USB Host 控制器驱动**相关的接口。

### 1、USB Host 控制器驱动层接口

您需要为您的硬件实现一个 USB Host 控制器驱动(`usbhost_controller`)，主要涉及填充 `struct usbhost_driver_s` 和 `struct usbhost_connection_s` 两个核心结构体中的函数指针。

#### 端口实例 (`struct usbhost_hubport_s`)

该结构体是 USB Host 栈中每个端口的抽象表示。每个 USB 设备控制器驱动必须实现此实例。需要实现的接口信息如下：

```C++
struct usbhost_hubport_s
{
  /* 指向底层控制器驱动接口的指针 */
  FAR struct usbhost_driver_s *drvr;
#ifdef CONFIG_USBHOST_HUB
  /* 指向父 Hub 的指针，若为 Root Hub 则为 NULL */
  FAR struct usbhost_hubport_s *parent;
#endif
  /* 指向已绑定的上层类驱动实例 */
  FAR struct usbhost_class_s *devclass;
  /* 控制端点 EP0 的句柄 */
  usbhost_ep_t ep0;
  /* 连接状态标志 */
  bool connected;
  /* 端口号 */
  uint8_t port;
  /* 设备功能地址 */
  uint8_t funcaddr;
  /* 设备速度 (USB_SPEED_*) */
  uint8_t speed;
};
```

#### 控制器驱动接口 (`struct usbhost_driver_s`)

此结构体定义了一系列回调函数，供 USB Host 核心逻辑调用，以操作底层硬件。

| **函数指针**         | **描述**                                                                                                                               |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| `ep0configure`       | 配置默认控制端点 (EP0)，包括 `speed` 和 EP0 支持的最大包，在设备枚举前调用。                                                           |
| `epalloc`            | 分配并配置一个端点 (Endpoint)，在类驱动绑定设备时调用。                                                                                |
| `epfree`             | 释放一个已分配的端点。                                                                                                                 |
| `alloc` / `free`     | 分配/释放数据缓冲区。<br>如果计算机硬件（Hardware）有提供特殊的缓存，调用此接口实现；否则可直接调用 `kmm_malloc`/`kmm_free`。          |
| `ioalloc` / `iofree` | 分配/释放用于 I/O 操作的缓冲区。<br>如果计算机硬件（Hardware）有提供特殊的缓存，调用此接口实现，否则直接使用 `kmm_malloc`/`kmm_free`。 |
| `ctrlin`             | 执行一个阻塞式的控制读 (IN) 传输。                                                                                                     |
| `ctrlout`            | 执行一个阻塞式的控制写 (OUT) 传输。                                                                                                    |
| `transfer`           | 执行一个阻塞式的传输。                                                                                                                 |
| `asynch`             | 发起一个异步传输。<br>函数立即返回，传输完成后通过回调函数通知。需启用 `CONFIG_USBHOST_ASYNCH`。                                       |
| `cancel`             | 取消指定端点上正在进行的同步或异步传输。                                                                                               |
| `connect`            | （仅当 `CONFIG_USBHOST_HUB` 启用时）通知有新 USB 设备接入到 Hub。                                                                      |
| `disconnect`         | 当 USB 设备断开或类驱动有错误发生时，调用此函数通知控制器驱动USB设备已断开连接。                                                       |

#### 连接管理接口 (`struct usbhost_connection_s`)

此结构体是连接管理和设备枚举逻辑的接口，由控制器驱动实现，供上层监控线程调用。需要实现的接口如下：

| **函数指针** | **描述**                                                                         |
| :----------- | :------------------------------------------------------------------------------- |
| `wait`       | 阻塞等待，直到有 USB 设备连接或断开。<br>返回受影响的 `usbhost_hubport_s` 实例。 |
| `enumerate`  | 对指定端口上新连接的设备执行枚举。                                               |

### 2、USB Host 类驱动层接口

#### 类驱动注册表 (`struct usbhost_registry_s`)

每个类驱动通过此结构体向系统注册自己，并提供一个 `create` 函数。当一个设备的 VID/PID 与注册表中的 ID 匹配时，系统将调用此 `create` 函数来实例化类驱动。

```C++
struct usbhost_registry_s
{
  /* 用于将多个类驱动注册信息链接成一个单向链表 */
  FAR struct usbhost_registry_s *flink;

  /*
   * 类驱动的工厂函数。当设备匹配时，系统调用此函数创建
   * 一个类驱动实例，并将其与设备会话绑定。
   */
  CODE FAR struct usbhost_class_s *(*create)
                                  (FAR struct usbhost_hubport_s *hub,
                                  FAR const struct usbhost_id_s *id);
  /* 描述该类驱动支持的设备ID (VID/PID) 列表 */
  uint8_t nids;
  FAR const struct usbhost_id_s *id;
};
```

- `create`：用于创建 USB 主机类状态的新实例，以及将 USB 主机驱动程序**会话**绑定到类实例。

    ```C
    CCODE FAR struct usbhost_class_s *(*create)
                                      (FAR struct usbhost_hubport_s *hub,
                                      FAR const struct usbhost_id_s *id);
    ```

#### 类驱动实例 (`struct usbhost_class_s`)

每个 USB Host 类驱动必须实现此实例，需要实现的接口如下：

| **函数指针**   | **描述**                                                                                  |
| :------------- | :---------------------------------------------------------------------------------------- |
| `connect`      | 当 USB 设备连接后，为类驱动提供配置描述符信息，用于申请和配置端点并执行类驱动的特定操作。 |
| `disconnected` | 通知类驱动对应 USB 设备已断开连接。                                                       |

## 三、 核心工作流程

USB Host 驱动的运行涉及三个主要流程：**初始化**、**枚举**和**数据传输**。下面分别对其进行说明。

### 1、初始化过程

系统初始化上电后，需要对 USB Host 驱动进行初始化。其中包括：

- 主机控制器硬件的初始化。
- 设备类型驱动初始化。
- 主机等待设备连接的任务创建。

![alt text](./figures/011.png)

### 2、枚举流程

当监控线程通过 `wait` 函数检测到设备连接后，便启动枚举流程。此过程涉及配置端点 0、获取设备描述符，并最终通过 `create` 和 `connect` 回调函数将设备与匹配的类驱动进行绑定。

![alt text](./figures/012.png)

### 3、数据传输流程

USB 设备成功枚举并与类驱动绑定后，上层应用程序即可通过类驱动提供的接口（如文件系统节点 `/dev/sda`）进行数据读写。这些操作最终会调用控制器驱动实现的 `transfer` 函数来完成物理数据传输。下图为同步传输过程的示意图：

![alt text](./figures/013.png)

## 四、驱动适配实践指南 (以 SIM 为例)

本章节以 openvela 模拟器 (SIM) 的 USB Host 驱动为例，展示如何适配一个新的 Host 控制器。SIM USB Host 的详细配置和使用方法，请参考 [USB 主机模拟 (SIM) 驱动程序指南](./sim/usb_host_sim_guide.md)。

### 1、实现初始化函数

您需要实现 `sim_usbhost_initialize()` 初始化函数。此函数是驱动适配的入口点，负责完成以下任务：

- **初始化上层类驱动**：调用 `usbhost_*_initialize()` 注册所有需要支持的类驱动。
- **填充驱动操作集**：将您实现的硬件操作函数赋值给 `struct usbhost_driver_s` 实例的各个函数指针。
- **初始化端口和地址管理**：配置 `struct usbhost_hubport_s` 实例，并初始化设备地址生成器。
- **初始化硬件控制器**：调用底层函数，完成控制器硬件的复位和基本配置。
- **创建监控线程**：启动一个新线程来等待和处理设备连接/断开事件。

```C
int sim_usbhost_initialize(void)
{
  struct sim_usbhost_s *priv = &g_sim_usbhost;
  struct usbhost_hubport_s *hport;
  int ret;

/* 1. 初始化需要的类驱动 */
#ifdef CONFIG_USBHOST_CDCACM
  ret = usbhost_cdcacm_initialize();
#endif

  /* 2. 填充控制器驱动的操作函数集 */
  priv->drvr.ep0configure   = sim_usbhost_ep0configure;
  priv->drvr.epalloc        = sim_usbhost_epalloc;
  priv->drvr.epfree         = sim_usbhost_epfree;
  priv->drvr.alloc          = sim_usbhost_alloc;
  priv->drvr.free           = sim_usbhost_free;
  priv->drvr.ioalloc        = sim_usbhost_ioalloc;
  priv->drvr.iofree         = sim_usbhost_iofree;
  priv->drvr.ctrlin         = sim_usbhost_ctrlin;
  priv->drvr.ctrlout        = sim_usbhost_ctrlout;
  priv->drvr.transfer       = sim_usbhost_transfer;
  priv->drvr.cancel         = sim_usbhost_cancel;
  priv->drvr.disconnect     = sim_usbhost_disconnect;
#ifdef CONFIG_USBHOST_ASYNCH
  priv->drvr.asynch         = sim_usbhost_asynch;
#endif

  /* 3. 初始化端口实例 */
  hport                       = &priv->hport.hport;
  hport->drvr                 = &priv->drvr;
  hport->ep0                  = &priv->ep0;
  hport->port                 = 0;
  hport->speed                = USB_SPEED_HIGH;

  usbhost_devaddr_initialize(&priv->devgen);
  priv->hport.pdevgen = &priv->devgen;

  /* 4. 初始化硬件并创建监控线程 */
  host_usbhost_init();
  priv->state = USB_HOST_DETACHED;
  ret = kthread_create("usbhost monitor", CONFIG_SIM_USB_PRIO,
                       CONFIG_SIM_USB_STACKSIZE,
                       sim_usbhost_waittask, NULL);
  if (ret < 0)
    {
      uerr("ERROR: Failed to create sim_usbhost_waittask: %d\n", ret);
      return -ENODEV;
    }

  return OK;
}
```

### 2、实现驱动操作函数集

您需要实现 `struct usbhost_driver_s` 和 `struct usbhost_connection_s` 中定义的所有回调函数。

`struct usbhost_driver_s` 的函数指针已在上面的 `sim_usbhost_initialize()` 中赋值。

此外，您还需定义一个 `struct usbhost_connection_s` 静态实例，以提供连接检测和枚举的入口点。

```C
/*
 * 实现 wait 和 enumerate 函数，将它们与 g_sim_usbconn 绑定。
 * 上层监控线程将通过此实例与您的驱动进行交互。
 */
static struct usbhost_connection_s g_sim_usbconn =
{
  .wait      = sim_usbhost_wait,
  .enumerate = sim_usbhost_enumerate,
};
```