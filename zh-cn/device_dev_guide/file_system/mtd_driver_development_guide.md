# MTD 驱动开发指南

## 一、概述

本文档详细指导开发者如何为 `openvela` 系统适配基于 MTD (Memory Technology Device) 模型的存储设备，如 NOR Flash 和 NAND Flash。您将学习如何实现 MTD 驱动的下半部接口，并将其注册到系统中。

### 1、前提条件

在开始之前，请确保您已经熟悉 `openvela` 的存储驱动框架。建议您先阅读 [openvela 存储驱动框架指南](./storage_driver_framework_guide.md)。

### 2、核心数据结构：`mtd_dev_s`

在 `openvela` 中，所有 MTD 设备都通过 `struct mtd_dev_s` 结构体进行抽象。您的主要任务就是实现这个结构体中定义的回调函数，并填充设备信息。

```C
// 定义于 nuttx/include/nuttx/mtd/mtd.h
struct mtd_dev_s
{
  // 擦除指定数量的块
  int (*erase)(FAR struct mtd_dev_s *dev, off_t startblock, size_t nblocks);

  // 按块读取
  ssize_t (*bread)(FAR struct mtd_dev_s *dev, off_t startblock,
                   size_t nblocks, FAR uint8_t *buffer);
  // 按块写入
  ssize_t (*bwrite)(FAR struct mtd_dev_s *dev, off_t startblock,
                    size_t nblocks, FAR const uint8_t *buffer);

  // 按字节读取 (可选)
  ssize_t (*read)(FAR struct mtd_dev_s *dev, off_t offset, size_t nbytes,
                  FAR uint8_t *buffer);
#ifdef CONFIG_MTD_BYTE_WRITE
  // 按字节写入 (可选, 需开启 CONFIG_MTD_BYTE_WRITE)
  ssize_t (*write)(FAR struct mtd_dev_s *dev, off_t offset, size_t nbytes,
                   FAR const uint8_t *buffer);
#endif

  // 控制接口，用于获取几何信息、整片擦除等
  int (*ioctl)(FAR struct mtd_dev_s *dev, int cmd, unsigned long arg);

  // MTD 设备名称
  FAR const char *name;
};
```

## 二、MTD 驱动开发流程

![img](./figures/006.png)

开发 MTD 驱动下半部通常遵循以下步骤：

1. **实现设备操作接口**：根据硬件手册，编写 `erase`, `bread`, `bwrite`, `ioctl` 等函数的具体实现。
2. **实例化** **`mtd_dev_s`**：定义一个静态的 `mtd_dev_s` 结构体变量，并将上一步实现的函数指针赋值给它。
3. **提供初始化函数**：编写一个全局的初始化函数（如 `my_chip_mtd_initialize()`），该函数返回已实例化的 `mtd_dev_s` 结构体指针。
4. **注册** **MTD** **设备**：在板级初始化代码中，调用您的初始化函数获取 MTD 设备实例，然后使用 `register_mtddriver()` 将其注册到 VFS 中。
5. **（可选）创建分区**：如果需要，调用 `register_mtdpartition()` 将单个 MTD 设备划分为多个逻辑分区。

## 三、实现 MTD 下半部接口

本节将以 NOR Flash 和 NAND Flash 为例，介绍接口实现的要点。

### 1、实现 NOR Flash 驱动

`openvela` 在 `nuttx/drivers/mtd/skeleton.c` 提供了一个优秀的 NOR Flash 驱动模板。您可以以此为起点进行开发。

#### 1.1 实例化 `mtd_dev_s`

首先，定义一个私有设备结构体，并在其中包含一个 `mtd_dev_s` 实例。然后，创建一个静态全局变量，并为其操作函数集赋予您的实现。

```C
// 示例：定义私有设备结构体
struct my_nor_dev_s {
  struct mtd_dev_s mtd;
  // 添加其他硬件相关的私有数据，如锁、状态等
};

// 示例：函数实现
static int my_nor_erase(FAR struct mtd_dev_s *dev, off_t startblock, size_t nblocks);
static ssize_t my_nor_bread(FAR struct mtd_dev_s *dev, off_t startblock, size_t nblocks, FAR uint8_t *buf);
// ... 其他函数实现

// 示例：实例化
static struct my_nor_dev_s g_nor_dev = {
  .mtd = {
    .erase  = my_nor_erase,
    .bread  = my_nor_bread,  // 按照page size读取
    .bwrite = my_nor_bwrite, // 按照page size写入
    .read   = my_nor_read,   // 按照字节读取
    .write  = my_nor_write,  // 按照字节写入的接口（依赖CONFIG_MTD_BYTE_WRITE）
    .ioctl  = my_nor_ioctl,
    .name   = "my_nor_flash"
  }
};
```

#### 1.2. 实现 `ioctl` 接口

`ioctl` 是一个关键接口，其中 `MTDIOC_GEOMETRY` 命令必须实现。您需要在此返回 Flash 的几何信息。

```C
static int my_nor_ioctl(FAR struct mtd_dev_s *dev, int cmd, unsigned long arg) {
  switch (cmd) {
    case MTDIOC_GEOMETRY:
    {
      FAR struct mtd_geometry_s *geo = (FAR struct mtd_geometry_s *)arg;
      if (geo) {
        // 根据您的硬件手册填充这些值
        geo->blocksize    = 256;    // 读/写块大小 (Page Size)
        geo->erasesize    = 4096;   // 擦除块大小 (Sector Size)
        geo->neraseblocks = 1024;   // 总擦除块数量
        return OK;
      }
      return -EINVAL;
    }

    case MTDIOC_BULKERASE:
    {
      // 实现整片擦除逻辑
      return OK;
    }
    
    // ... 处理其他命令
    
    default:
      return -ENOTTY;
  }
}
```

> **参考实现**: `nuttx/drivers/mtd/w25.c`

### 2、实现 NAND Flash 驱动

NAND Flash 的管理比 NOR Flash 更复杂，涉及坏块管理 (BBM) 和错误纠正码 (ECC)。`openvela` 提供了针对 NAND 的抽象层。

#### 2.1. 核心数据结构：`nand_raw_s`

您需要实现 `struct nand_raw_s` 结构体，它定义了更底层的 NAND 操作。

```C
// 定义于 nuttx/drivers/mtd/nand_raw.h
struct nand_raw_s {
  // ... 设备几何信息、地址等
  
  // 底层操作函数
  CODE int (*eraseblock)(FAR struct nand_raw_s *raw, off_t block);
  CODE int (*rawread)(FAR struct nand_raw_s *raw, off_t block, unsigned int page, FAR void *data, FAR void *spare);
  CODE int (*rawwrite)(FAR struct nand_raw_s *raw, off_t block, unsigned int page, FAR const void *data, FAR const void *spare);

  // ... 其他硬件 ECC 相关接口
};
```

#### 2.2. 初始化流程

1. 实现并实例化 `struct nand_raw_s`。
2. 调用 `nand_initialize(FAR struct nand_raw_s *raw)`。此函数会处理 ONFI (Open NAND Flash Interface) 协议探测、ECC 初始化等通用逻辑，并返回一个配置好的 `struct mtd_dev_s *` 实例。

#### 2.3. ECC 和坏块管理

- **ECC**：`openvela` 支持硬件 ECC 和软件 ECC (`CONFIG_MTD_NAND_SWECC`)。

    - **`rawread`****/****`rawwrite`**：实现这两个接口时，您需要负责读/写数据区和备用区 (Spare Area)，但**不**进行 ECC 计算。
    - **`readpage`****/****`writepage`**：如果您的硬件支持 ECC，请实现这两个接口。`writepage` 应触发硬件生成 ECC 并写入，`readpage` 应触发硬件进行 ECC 校验和纠正。

- **坏块管理**：

    - 您的驱动需要决定坏块标记在备用区的存储位置。
    - `ioctl` 接口需要实现 `MTDIOC_ISBAD` 和 `MTDIOC_MARKBAD` 命令。

> **参考实现**: `nuttx/arch/arm/src/sam34/sam4s_nand.c`

## 四、注册与分区

### 1、注册 MTD 设备

在板级初始化代码中，调用 `register_mtddriver()` 将您的设备注册到 `/dev` 目录下。

```C
// 在板级初始化函数中
FAR struct mtd_dev_s *mtd_dev;

// 1. 获取 MTD 设备实例
mtd_dev = my_nor_initialize(); // 您编写的初始化函数

if (mtd_dev) {
  // 2. 注册设备
  int ret = register_mtddriver("/dev/mynor", mtd_dev, 0666, NULL);
  if (ret < 0) {
    // 处理错误
  }
}
```

### 2、创建 MTD 分区

`openvela` 允许您将一个物理 MTD 设备划分为多个逻辑分区，便于管理。

- **核心函数**：`mtd_partition()` 创建一个代表分区的 MTD 子设备。
- **注册函数**：`register_mtdpartition()` 封装了创建和注册分区的逻辑。

```C
// 示例：将 /dev/mynor 划分为两个分区
// "config" 分区: 从第 0 块开始，共 16 个擦除块
register_mtdpartition("/dev/config", 0666, "/dev/mynor", 0, 16);

// "userdata" 分区: 从第 16 块开始，共 1008 个擦除块
register_mtdpartition("/dev/userdata", 0666, "/dev/mynor", 16, 1008);
```

## 五、相关内核配置 (Kconfig)

确保在 `defconfig` 文件中启用了必要的 MTD 和相关模块：

```Makefile
# 启用 MTD 核心支持
CONFIG_MTD=y

# 启用 MTD 分区支持
CONFIG_MTD_PARTITION=y
CONFIG_MTD_PROGMEM=y

# 启用 BCH 代理，以支持通过文件接口访问 MTD
CONFIG_BCH=y
CONFIG_BCH_BUFFER_ALIGNMENT=32 //86panel & k03 alignment = 0

# 读写 cache 的配置
CONFIG_DRVR_WRITEBUFFER=y
CONFIG_DRVR_WRDELAY=350
# 多数项目下不开读buffer
# CONFIG_DRVR_READAHEAD is not set
# CONFIG_DRVR_READBYTES is not set
```

## 六、测试与验证

`openvela` 提供了丰富的测试工具来验证您的 MTD 驱动：

- **fstest**：一个综合性的文件系统压力测试工具，可以挂载文件系统到您的 MTD 分区上进行读写、擦除、耗尽空间等测试。
- **cmocka_block_test**：虽然名为 block test，但它也可以通过 MTD 的块设备代理（如 `/dev/mtdblock0`）来测试底层的 `bread` 和 `bwrite` 接口是否正确。

请参考相关测试工具的文档，对您的驱动进行充分验证。

- [fstest]()
- [blktest]()