# PCI Endpoint (EPC) 框架深度解析

\[ [English](../../../../../en/device_dev_guide/driver/bus_driver/PCI/pci_epc_framework.md) | 简体中文 \]

本文档旨在深度解析 openvela 操作系统中的 PCI Endpoint Controller (EPC) 框架。内容涵盖其架构设计、核心职责、工作流程、关键数据结构和 API，为开发者提供一个全面的开发与使用指南。

## 一、术语表

| **术语/缩写** | **英文全称**        | **中文释义**                                                                                       |
| :------------ | :------------------ | :------------------------------------------------------------------------------------------------- |
| **EPC**       | Endpoint Controller | **Endpoint 控制器**。<br> 负责直接控制 PCI Endpoint 硬件的底层控制器。                             |
| **EPF**       | Endpoint Function   | **Endpoint 功能**。 <br> 在 Endpoint 设备上实现的具体 PCI 功能，例如一个网卡功能或存储功能。       |
| **BME**       | Bus Master Enable   | **总线主控使能**。<br> PCI 配置空间中的一个控制位，用于使能设备发起总线事务（如 DMA 读写）的能力。 |

## 二、架构设计与核心职责

openvela 的 PCI Endpoint 框架采用分层设计，主要包含 **Endpoint 控制器驱动(EPC Driver)**、**Endpoint 核心层 (Endpoint Core)** 和 **Endpoint 功能驱动 (EPF Driver)** 三个部分。

![alt text](./figures/008.png)

### PCI Endpoint 核心层

Endpoint 核心层是整个框架的中枢，其核心职责是实现解耦和资源管理。

1. 解耦 Endpoint Device 和 Endpoint Controller。

    核心层通过两组标准化的回调函数接口，隔离了上层功能与底层硬件的直接依赖：

    - Endpoint Controller 向 PCI Endpoint Core 注册回调函数 **`pci_epc_ops_s`**，Endpoint Device 通过该回调函数接口执行 Endpoint Controller 相关操作。
    - Endpoint Device 向 PCI Endpoint Core 注册回调函数注册 **`pci_epc_event_ops_s`**，Endpoint Controller通过该回调函数接口执行 EPF 相关操作。

2. 管理 PCI 地址空间。

    核心层负责管理和分配由底层硬件驱动初始化的 PCI 地址空间。

    - PCI 地址域空间通常由与具体 SoC 相关的 IP 驱动进行初始化。

    - 地址窗口 (`pci_epc_mem_window_s`) 的页面大小 (`page_size`) 通常设计为 4KB 的整数倍，以匹配系统内存管理单元 (MMU) 的页面大小。

        ```C++
        struct pci_epc_mem_window_s
        {
          uintptr_t phys_base; //pci physical
          size_t    size;      // pci windows size
          size_t    page_size; //windows page size
        };
        ```

## 三、初始化与绑定流程

当系统配置为 PCI Endpoint 模式时，其初始化、驱动加载和功能绑定的流程遵循以下步骤：

![alt text](./figures/009.png)

1. **注册 Endpoint 控制器 (EPC)：**

    EPC 驱动调用 `pci_epc_create()` 函数，向核心层注册一个 EPC 实例，并提供其底层操作函数集。

2. **注册 Endpoint 功能驱动 (EPF Driver)：**

    实现具体设备功能的 EPF 驱动调用 `pci_epf_register_driver()` 向核心层注册自身。

3. **注册 Endpoint 功能设备 (EPF Device)：**

    代表逻辑功能的 EPF 设备通过 `pci_epf_device_register()` 进行注册。

4. **匹配 EPF 设备与驱动：**

    核心层根据 `id_table` 将已注册的 EPF 设备与兼容的 EPF 驱动进行匹配。

5. **执行 EPF 驱动 `probe`：**

    匹配成功后，核心层调用 EPF 驱动的 `probe` 回调函数，进行初步的功能初始化。

6. **匹配 EPF 与 EPC：**

    `probe` 函数中，EPF 会根据名称 (`name`) 寻找到对应的 EPC 实例。

7. **执行绑定 (Binding)：**

    EPF 与 EPC 匹配成功后，核心层开始执行绑定操作，并调用 EPF 驱动的 `bind` 回调函数，通知驱动其已与底层硬件控制器关联。

8. **启动 EPC：**

    绑定完成后，上层逻辑调用 `pci_epc_start()`。该调用会触发 EPC 驱动的 `start` 回调，完成硬件寄存器的最终配置并使能 PCI Link，使设备在 PCI 总线上对主机可见。

> **说明：** EPC 操作集中的 `dma_xfer` 回调提供了一个可选的系统级 DMA 传输能力。该功能也可以在具体的 EPF 驱动中独立实现。

## 四、核心数据结构

### 1、`struct pci_epc_ctrl_s`: Endpoint 控制器

该结构代表一个物理上的 Endpoint 控制器硬件。

```C
/* 定义 PCI Endpoint 控制器 (EPC) 的数据结构 */
struct pci_epc_ctrl_s
{
  FAR const char *name;                      /* EPC 实例的唯一名称，用于与 EPF 绑定 */
  struct list_node pci_epf;                  /* 挂载到此 EPC 上的 EPF 链表 */
  mutex_t list_lock;                         /* 用于保护 pci_epf 链表的互斥锁 */
  FAR const struct pci_epc_ops_s *ops;       /* EPC 底层操作函数集 */
  FAR struct pci_epc_mem_s **windows;        /* EPC 的地址空间窗口数组 */
  FAR struct pci_epc_mem_s *mem;             /* 指向第一个地址空间窗口的便捷指针 */
  unsigned int num_windows;                  /* 支持的地址窗口数量 */
  uint8_t max_functions;                     /* 支持的最大 PCI Function 数量 */
  struct list_node node;                     /* 用于挂载到全局 EPC 链表的节点 */
  mutex_t lock;                              /* 用于保护 EPC 操作的互斥锁 */
  unsigned long function_num_map;            /* 用于管理物理 Function 编号的位图 */
};
```

### 2、`struct pci_epc_ops_s`: EPC 操作回调

该结构定义了由 EPC 驱动实现、供上层调用的底层硬件操作函数集。

```C
/* 定义 EPC 的底层操作回调函数集 */
struct pci_epc_ops_s
{
  /* 配置空间与 BAR 操作 */
  CODE int (*write_header)(...);
  CODE int (*set_bar)(...);
  CODE void (*clear_bar)(...);

  /* 地址映射操作 */
  CODE int (*map_addr)(...);
  CODE void (*unmap_addr)(...);

  /* 中断操作 */
  CODE int (*raise_irq)(...);
  CODE int (*set_msi)(...);
  CODE int (*get_msi)(...);
  CODE int (*set_msix)(...);
  CODE int (*get_msix)(...);
  CODE int (*map_msi_irq)(...);
  
  /* Link 与特性管理 */
  CODE int (*start)(...);
  CODE void (*stop)(...);
  CODE FAR const struct pci_epc_features_s *(*get_features)(...);

  /* DMA 操作 (可选) */
  CODE int (*dma_xfer)(...);
};
```

**关键回调函数说明：**

| **回调函数**           | **功能描述**                                          |
| :--------------------- | :---------------------------------------------------- |
| `write_header`         | 填充指定 Function 的 PCI 配置空间头部。               |
| `set_bar`              | 配置指定 Function 的 BAR (Base Address Register)。    |
| `clear_bar`            | ops to reset the BAR                                  |
| `map_addr`             | 将本地 CPU 地址映射到 PCI 总线地址。                  |
| `unmap_addr`           | 解除 CPU 地址与 PCI 总线地址的映射。                  |
| `set_msi` / `set_msix` | 在能力寄存器中设置请求的 MSI / MSI-X 中断数量。       |
| `get_msi` / `get_msix` | 从能力寄存器中获取 RC 分配的 MSI / MSI-X 中断数量。   |
| `raise_irq`            | 发起一个 Legacy、MSI 或 MSI-X 中断。                  |
| `map_msi_irq`          | 将物理地址映射到 MSI 地址，并返回 MSI 数据。          |
| `start`                | 启动 PCI Link，使设备在总线上可见。                   |
| `stop`                 | 停止 PCI Link。                                       |
| `get_features`         | 获取 EPC 硬件支持的特性（如中断模式、BAR 大小等）。   |
| `dma_xfer`             | 使用系统级 DMA 在主机内存与设备本地内存之间传输数据。 |

### 3、`struct pci_epf_driver_s`: Endpoint 功能驱动

该结构定义了一个 EPF 驱动，包含了匹配信息和核心回调函数。

```C
/* 定义 PCI Endpoint 功能 (EPF) 驱动的数据结构 */
struct pci_epf_driver_s
{
  CODE int (*probe)(FAR struct pci_epf_device_s *epf);
  CODE void (*remove)(FAR struct pci_epf_device_s *epf);

  struct list_node node;
  FAR struct pci_epf_ops_s *ops;                   /* EPF 操作回调 (如 bind/unbind) */
  FAR const struct pci_epf_device_id_s *id_table;  /* EPF 设备 ID 表，用于设备-驱动匹配 */
};

/* 定义 EPF 驱动的匹配 ID */
struct pci_epf_device_id_s
{
  char name[PCI_EPF_NAME_SIZE];
  unsigned long driver_data;
};
```

- **`id_table`**: 用于标识该驱动支持的 EPF 设备，核心层依据此表进行设备与驱动的匹配。
- **`ops`**: EPF 驱动实现的回调函数集（如 `bind` 和 `unbind`），用于响应来自核心层的绑定/解绑事件。

### 4、`struct pci_epf_device_s`: Endpoint 功能设备

该结构代表一个逻辑上的 Endpoint 功能，定义了其资源需求和状态。

```C
/* 定义 PCI Endpoint 功能 (EPF) 设备的数据结构 */
struct pci_epf_device_s
{
  FAR const char *name;                      /* EPF 设备的唯一名称 */
  FAR struct pci_epf_header_s *header;       /* 指向标准配置空间头部的指针 */
  struct pci_epf_bar_s bar[6];               /* EPF 所需的 BAR 配置 */
  uint8_t msi_interrupts;                    /* 请求的 MSI 中断数量 */
  uint16_t msix_interrupts;                  /* 请求的 MSI-X 中断数量 */
  uint8_t func_no;                           /* 在 EPC 内唯一的物理 Function 编号 */

  FAR struct pci_epc_ctrl_s *epc;            /* 指向已绑定的 EPC */
  FAR struct pci_epf_driver_s *driver;       /* 指向已绑定的 EPF 驱动 */
  FAR const struct pci_epf_device_id_s *id;  /* 指向设备 ID */
  struct list_node node;                     /* 用于挂载到 EPC 的 pci_epf 链表的节点 */
  
  mutex_t lock;                              /* 用于保护 EPF 操作的互斥锁 */
  unsigned int is_bound;                     /* 标记是否已调用 bind 回调 */
  FAR const struct pci_epc_event_ops_s *event_ops; /* 用于接收 EPC 事件的回调函数集 */
};
```

## 五、核心 API 说明

### 1、EPC 核心层接口 (`pci-epc-core.c`, `pci-epc-mem.c`)

这些 API 主要由 EPC 驱动和 Endpoint 核心层内部调用。

| **函数原型**               | **功能描述**                                                                                                  |
| :------------------------- | :------------------------------------------------------------------------------------------------------------ |
| `pci_epc_create()`         | 创建并初始化一个 EPC 设备实例，并将其注册到 EPC 核心层。                                                      |
| `pci_epc_destroy()`        | 注销并销毁一个已创建的 EPC 设备实例。                                                                         |
| `pci_epc_start()`          | 触发 EPC 硬件的启动流程，使能 PCI Link。                                                                      |
| `pci_epc_raise_irq()`      | 当 EP 侧执行完 `write/read` 操作后，触发 Legacy、MSI 或 MSI-X 中断给 RC (Root Complex)， 通知其完成相关操作。 |
| `pci_epc_add_epf()`        | 将一个 EPF 设备与指定的 EPC 进行关联（绑定）。                                                                |
| `pci_epc_linkup()`         | 通知 EPF 设备 EPC 已经和 RC 建立 PCI Link。                                                                   |
| `pci_epc_init_notify`      | 通知 EPC 已经初始化完成。                                                                                     |
| `pci_epc_bme_notify()`     | EPC 设备接收到 BME（BUS Master Enable）事件后，以通知 EPF 设备。                                              |
| `pci_epc_mem_init()`       | 初始化 PCI Endpoint Controller 设备的内存地址空间。                                                           |
| `pci_epc_mem_alloc_addr()` | 从 EPC 的地址空间中分配一段内存， 用于 Memory 域地址到 PCI 域地址的映射。                                     |
| `pci_epc_set_bar`          | 配置 Endpoint 设备中某个 BAR 的数据。                                                                         |
| `pci_epc_map_addr`         | 映射 CPU 地址空间到 PCI 域地址空间，用于分配 BAR 的地址空间。                                                 |
| `pci_epc_add_epf`          | 用于绑定 PCI EPF 到指定的 PCI EPC 上。                                                                        |
| `pci_epc_map_msi_irq`      | 映射物理地址到 MSI 地址。                                                                                     |

### 2、EPF 核心层接口 (`pci-epf-core.c`)

这些 API 主要由 EPF 驱动调用。

| **函数原型**                | **功能描述**                                                             |
| :-------------------------- | :----------------------------------------------------------------------- |
| `pci_epf_register_driver()` | 注册一个 EPF 驱动程序。                                                  |
| `pci_epf_device_register()` | 注册一个 EPF 设备实例。                                                  |
| `pci_epf_alloc_space()`     | 为 EPF 分配一块用于 BAR 映射的内存空间。                                 |
| `pci_epf_bind()`            | 将 EPF 与一个匹配的 EPC 进行绑定，通常在 EPF 驱动的 `probe` 函数中调用。 |

## 六、总结与关键特性

1. **物理设备支持：**

    当前框架专注于物理硬件，不支持虚拟化的 EPF (Virtual EPF) 与 EPC (Virtual EPC)。

2. **多功能设备 (Multi-Function)：**

    框架支持将多个不同的 EPF 绑定到同一个物理 EPC，从而实现多功能设备。

3. **灵活的测试与验证：**

    开发者可以通过 `pci_epf_device_register` API 注册多个 EPF 设备实例，以便捷地进行多功能设备的开发、测试与验证。
