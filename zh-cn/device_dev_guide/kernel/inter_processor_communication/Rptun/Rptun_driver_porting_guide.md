# Rptun 驱动适配指南

本指南详细介绍了如何在 `openvela` 操作系统中为 Rptun (Remoteproc Tunnel) 框架适配特定硬件平台的驱动程序。您将学习 Rptun 的核心概念，以及如何通过实现 `rptun_ops` 操作接口来集成您的驱动。

## 一、Rptun 框架概述

阅读本文前，建议您首先阅读 [Rptun 框架技术指南](./Rptun.md)。

Rptun（Remoteproc Tunnel）是在 openvela 中基于 OpenAMP 的 Remoteproc 和 Remoteproc VirtIO 实现的一个远端 CPU 生命周期管理和 VirtIO 的传输层。

**核心功能组件：**

- **Remoteproc**: 负责管理远端处理器的生命周期，包括启动、停止和固件加载。平台适配层（Vendor）需要实现部分底层操作。
- **VirtIO**: 提供一个标准化的传输层，用于实现高效的跨核数据交换。平台适配层需要提供共享内存和跨核中断机制的支持。

通过这两个组件的结合，Rptun 实现了强大的跨核通信能力。其中，基于 Rpmsg (Remote Processor Messaging) 的 VirtIO 驱动是 `openvela` 中应用最广泛的通信方式。

同时 Rptun 也对用户态提供了字符设备，让用户可以方便的对远端 CPU 进行操作和调试。

![img](./figures/001.png)

## 二、驱动适配核心：`rptun_ops` 接口

适配 Rptun 驱动的核心任务是实现 `rptun_ops` 结构体中定义的一系列回调函数。此结构体定义了 Rptun 框架与底层硬件交互的标准化接口。

驱动程序在填充此结构体后，需调用 `rptun_initialize()` 函数来向 Rptun 框架注册并完成初始化。

**接口定义**：`nuttx/include/nuttx/rptun/rptun.h`

```C
struct rptun_ops_s
{
    /* 获取通讯对端CPU的名字，必须实现 */
    CODE FAR const char *(*get_cpuname)(FAR struct rptun_dev_s *dev); 
    /* 获取对端CPU的固件，对于需要通过elf laoder启动对端CPU的情况，需要实现，否则可以返回NULL */
    CODE FAR const char *(*get_firmware)(FAR struct rptun_dev_s *dev);
    /* 获取resoucre table，两端需要获取到同一个resoucre table，必须实现 */
    CODE FAR struct rptun_rsc_s *(*get_resource)(FAR struct rptun_dev_s *dev); 
    /* 地址环境，用于进行虚拟和物理地址的转换，无需要可以不实现，默认PA和VA 1:1 */
    CODE FAR const struct rptun_addrenv_s *(*get_addrenv)(FAR struct rptun_dev_s *dev);
    
    /* 本端是master还是slave，一般来说主核心是master */
    CODE bool (*is_master)(FAR struct rptun_dev_s *dev); 
    /* 是否自动启动，如果是，在rptun_intialize()后rptun自动启动，否则通过命令行启动 */
    CODE bool (*is_autostart)(FAR struct rptun_dev_s *dev); 
    /* 启动回调，可以用于启动对端的CPU，非必须 */
    CODE int (*start)(FAR struct rptun_dev_s *dev); 
    /* 停止回调，可以用于停止对端的CPU，非必须 */
    CODE int (*stop)(FAR struct rptun_dev_s *dev); 
    
    /* 通过中断通知对端CPU，必须实现 */
    CODE int (*notify)(FAR struct rptun_dev_s *dev, uint32_t vqid);
    /* Rptun调用该API将自己的中断回调函数传递下来，发生中断时回调callback函数，必须实现 */
    CODE int (*register_callback)(FAR struct rptun_dev_s *dev, rptun_callback_t callback, FAR void *arg);
    
    /* 配置接口，初始化时OpenAMP会回调，非必须 */
    CODE int (*config)(FAR struct rptun_dev_s *dev, FAR void *data); 
};
```

### 1、资源与配置回调

这类回调函数向 Rptun 框架提供通信所需的基础资源信息。

#### `get_cpuname`

- **要求**：强制实现
- **功能**：返回通信**对端处理器的名称字符串**。
- **说明**：Rptun 为每对通信的 CPU 建立一个通道。例如，在 AP (Application Processor) 与 CP (Communication Processor) 的通信场景中，AP 端的驱动应返回 `"cp"`，CP 端的驱动应返回 `"ap"`。

#### `get_firmware`

- **要求**：可选实现
- **功能**：返回远端处理器固件的路径或地址。
- **说明**：当主核需要加载并启动从核的固件（通常为 ELF 格式）时，必须实现此函数。Rptun 框架会解析该固件，并自动从中提取 `.resource_table` 段作为 Resource Table。
- **注意**：此回调与 `get_resource` 互斥。如果实现了 `get_firmware`，则无需实现 `get_resource`。对于两个核心都采用 XIP (Execute In Place) 方式运行的系统，通常不实现此函数。

#### `get_resource`

- **要求**：条件性强制实现
- **功能**：返回指向共享内存中 Resource Table 的指针。
- **说明**：Resource Table 是定义共享资源的**契约**。如果未通过 `get_firmware` 提供固件，则必须实现此函数来直接指定Resource Table。有关 Resource Table 的详细信息，请参阅 [Resource Table](#1resource-table)。

#### `get_addrenv`

- **要求**：可选实现
- **功能**：提供地址转换表。
- **说明**：当主核与从核访问同一块共享内存时，如果它们看到的地址不同（例如 VA/PA 不一致），则必须实现此函数。Rptun 框架会使用该转换表在通信时进行地址转换。若地址空间一致，则无需实现。

### 2、生命周期管理回调

这类回调函数用于控制远端处理器的状态和 Rptun 服务自身的行为。

#### `is_master`

- **要求**：强制实现
- **功能**：声明当前处理器在通信对中是否为 Master 角色。
- **说明**：在每一对 Rptun 通道中，必须有一个 Master 和一个 Slave。Master 通常负责初始化共享内存、管理 Resource Table，并具备启动或停止 Slave 核的能力。

#### `is_autostart`

- **要求**：可选实现 (默认为 `false`)
- **功能**：指定是否在初始化后自动启动 Rptun 服务。
- **说明**：

    - **返回** `true`: 在 `rptun_initialize()` 调用后，Rptun 框架将自动启动服务，包括初始化 VirtIO 设备。
    - **返回** `false`: Rptun 将等待外部命令启动。您可以通过用户态字符设备或 `openvela` 提供的命令行工具 (`rptun start /dev/rptun/<cpuname>`) 手动启动。

#### `start`

- **要求**：可选实现
- **功能**：提供启动远端处理器的底层硬件操作。
- **说明**：通常由 Master 端实现。如果 Slave 核需要由 Master 核显式启动（例如，通过写寄存器或时钟控制），您应在此函数中实现该逻辑。该 API 会在本核心的 Rptun 初始化完成后进行调用。

#### `stop`

- **要求**：可选实现
- **功能**：提供停止远端处理器的底层硬件操作。
- **说明**：通常由 Master 端实现，用于需要停止或重启 Slave 核的场景。

### 3、通信与中断回调

这类回调函数是实现跨核数据交换的关键。

#### `notify`

- **要求**：强制实现
- **功能**：向远端处理器发送通知。
- **说明**：当 VirtIO 驱动将数据写入共享内存后，会调用此函数。您需要在此实现触发对端硬件中断的逻辑。`vqid` 参数指定了哪个 Virtqueue 需要处理，Vendor 需要把 `vqid` 传递过去，一般是通过跨核中断原生携带短消息的能力；如果无法传递 `vqid`，直接传递 `NOTIFY_ALL` 亦可。远端 CPU 在收到中断后，调用 Rptun 框架注册的 `rptun_callback` 函数。

#### `register_callback`

- **要求**：强制实现
- **功能**：注册一个 Rptun 框架的回调函数，用于处理来自远端的通知。
- **说明**：Rptun 框架在初始化时会调用此函数，将一个内部处理函数（`callback`）传递给您的驱动。您的驱动必须保存此函数指针。当硬件检测到来自远端的中断时，您的中断服务程序 (ISR) 必须调用这个已保存的回调函数。
- **注意**：请确保在调用此回调函数之后再使能相关的跨核中断，以避免在 Rptun 准备就绪前收到无法处理的中断。

### 4、可选配置回调

#### `config`

- **要求**：可选实现
- **功能**：该接口用于在启动跨核通讯前，对驱动进行配置。
- **说明**：如果您的驱动需要在 Rptun 服务启动前执行一些预配置（例如，复杂的时钟或中断配置），可以在此实现。`data` 参数可用于传递自定义配置数据。如果 Vendor 在起始阶段已经将跨核中断和 Resource Table 等配置完毕，则无需适配当前 API。

## 三、核心适配要点

在实现 `rptun_ops` 的过程中，需要重点关注以下几个概念。

### 1、Resource Table

Resource Table是 Rptun 正常工作的基石。它是一个存放在共享内存中的 C 结构体，用于描述双方共用的资源，例如 VirtIO 设备类型、特性、vring 缓冲区和配置信息。

- **位置**：必须位于 Master 和 Slave 核都能访问的共享内存中。

- **初始化**：必须在任何一端尝试访问它之前完成初始化。

    - **对于有明确启动顺序的系统**： 由先启动的 Master 核负责初始化。
    - **对于同步启动的系统**： 可由 TEE (Trusted Execution Environment) 固件提前初始化。

- **内容**：格式遵循 OpenAMP 标准。下面是一个为 Rpmsg VirtIO 设备定义的 Resource Table 示例。

    ```C
    /* Resource Table 示例：定义一个 Rpmsg VirtIO 设备 */
    /* 注意：此为简化示例，实际结构体定义请参考源码 */
    struct aligned_data(8) rptun_rsc_s
    {
      struct resource_table    rsc_tbl_hdr; // 标准头部
      uint32_t                 offset[3];   // 各资源条目的偏移
      struct fw_rsc_trace      log_trace;
      struct fw_rsc_vdev       rpmsg_vdev;  // VirtIO 设备描述
      struct fw_rsc_vdev_vring rpmsg_vring0;
      struct fw_rsc_vdev_vring rpmsg_vring1;
      struct fw_rsc_config     config;      // VirtIO 设备配置
      struct fw_rsc_carveout   carveout;    // 共享内存区域描述
    };
    
    /* 初始化示例 */
    struct rptun_rsc_s *rsc = &priv->shmem->rsc;
    
    // 填充头部信息
    rsc->rsc_tbl_hdr.ver            = 1; /* 版本 */
    rsc->rsc_tbl_hdr.num            = 2; /* 设备数量1个 */
    /* 第一个设备到share memory base的offset */
    rsc->offset[0]                  = offsetof(struct sim_rptun_rsc_s,
                                               rpmsg0);
    rsc->rpmsg0.type                = RSC_VDEV;
    rsc->rpmsg0.id                  = VIRTIO_ID_RPMSG;
    rsc->rpmsg0.notifyid            = RSC_NOTIFY_ID_ANY;
    rsc->rpmsg0.dfeatures           = (1 << VIRTIO_RPMSG_F_NS) |
                                      (1 << VIRTIO_RPMSG_F_ACK) |
                                      (1 << VIRTIO_RPMSG_F_BUFSZ) |
                                      (1 << VIRTIO_RPMSG_F_CPUNAME);
    rsc->rpmsg0.config_len          = sizeof(struct fw_rsc_config);
    rsc->rpmsg0.num_of_vrings       = 2;
    rsc->rpmsg0.reserved[0]         = VIRTIO_DEV_DRIVER;
    rsc->rpmsg0.reserved[1]         = 0;
    
    // 填充 vring 信息
    rsc->rpmsg0_vring0.align        = 8;
    rsc->rpmsg0_vring0.num          = 8;
    rsc->rpmsg0_vring0.notifyid     = RSC_NOTIFY_ID_ANY;
    rsc->rpmsg0_vring0.da           = 0;
    rsc->rpmsg0_vring1.align        = 8;
    rsc->rpmsg0_vring1.num          = 8;
    rsc->rpmsg0_vring1.notifyid     = RSC_NOTIFY_ID_ANY;
    rsc->rpmsg0_vring1.da           = 0;
    rsc->rpmsg0_config.h2r_buf_size = 0x600;
    rsc->rpmsg0_config.r2h_buf_size = 0x600;
    strlcpy((FAR char *)rsc->rpmsg0_config.host_cpuname,
    CONFIG_RPMSG_LOCAL_CPUNAME, VIRTIO_RPMSG_CPUNAME_SIZE);
    strlcpy((FAR char *)rsc->rpmsg0_config.remote_cpuname,
    priv->cpuname, VIRTIO_RPMSG_CPUNAME_SIZE);
    
    /* Virtio Rpmsg0 share memory buffer */
    
    rsc->offset[1]                  = offsetof(struct sim_rptun_rsc_s,
                                             rpmsg0_carveout);
                                             
    // 填充 carveout 信息（指定共享内存区域）
    rsc->rpmsg0_carveout.type       = RSC_CARVEOUT;
    rsc->rpmsg0_carveout.da         = offsetof(struct sim_rptun_shmem_s,
                                             rsc.rpmsg0_shm);
    rsc->rpmsg0_carveout.pa         = FW_RSC_U32_ADDR_ANY;
    rsc->rpmsg0_carveout.len        = sizeof(priv->shmem->rsc.rpmsg0_shm);
    memcpy(rsc->rpmsg0_carveout.name, "rpmsg0_shm", 10);
    ```

### 2、消息收发流程

#### 消息发送

1. 上层应用（如 Rpmsg）调用 VirtIO 接口，将数据写入共享内存中的 vring 缓冲区。
2. VirtIO 驱动调用您实现的 `rptun_ops->notify()` 回调函数。
3. 您的 `notify()` 函数触发一个硬件中断，通知对端处理器有新数据。

#### 消息接收

1. 本地处理器收到对端发来的硬件中断，中断服务程序 (ISR) 被触发。
2. 在 ISR 中，调用通过 `register_callback` 保存的 Rptun 回调函数，并传入 `vqid`。

    - 如果硬件中断无法传递 `vqid`，可传入 `RPTUN_NOTIFY_ALL`，Rptun 框架将轮询检查所有 vring。

3. Rptun 框架的内部回调函数被执行，它会检查 vring，处理收到的数据，并通知上层应用。

### 3、共享内存与缓存一致性

共享内存的缓存属性是适配过程中极易出错的一点。

- **建议：** 除非您对平台的缓存一致性机制有十足的把握，否则**强烈建议将共享内存配置为非缓存 (Uncacheable/Device) 属性**。这可以从根本上避免因缓存未同步导致的数据损坏问题。
- **使用可缓存 (Cacheable) 内存：**

    - **必须使能** **`CONFIG_OPENAMP_CACHE`** **配置**： 此配置会启用 OpenAMP 框架内置的缓存管理操作（刷新和失效），确保数据在 CPU 缓存和物理内存之间正确同步。
    - **注意缓存行对齐：** 如果您的平台 Cache Line 大小有特定对齐要求，请务必在 Resource Table 的 `vring` 定义中设置 `align` 字段以匹配该值，防止因非对齐访问引发硬件异常。

## 四、Rptun 驱动实例

您可以参考以下 `openvela` 源码中已有的 Rptun 驱动实现：

- **Simulation 平台:**
    - `nuttx/arch/sim/src/sim/sim_rptun.c`
- **QEMU 平台 (基于 ivshmem):**
    - `nuttx/drivers/rptun/rptun_ivshmem.c`

## 五、参考文档

- VirtIO 相关概念：[VirtIO 简介](./../VirtIO/introduction_to_virtio.md)
- Rptun 框架介绍：[Rptun 框架技术指南](./Rptun.md)
- [OpenAMP 介绍]()