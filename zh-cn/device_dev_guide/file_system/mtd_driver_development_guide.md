# MTD 驱动开发指南

\[ [English](../../../en/device_dev_guide/file_system/mtd_driver_development_guide.md) | 简体中文 \]

## 一、概述

本文档详细指导开发者如何为 `openvela` 系统适配基于 MTD (Memory Technology Device) 模型的存储设备，如 NOR Flash 和 NAND Flash。您将学习如何实现 MTD 驱动的下半部接口，并将其注册到系统中。

### 1、前提条件

在开始之前，请确保您已经熟悉 `openvela` 的存储驱动框架。建议您先阅读[存储驱动框架指南](./storage_driver_framework_guide.md)。

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
4. **注册 MTD 设备**：在板级初始化代码中，调用您的初始化函数获取 MTD 设备实例，然后使用 `register_mtddriver()` 将其注册到 VFS 中。
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

- `ioctl` 接口完整定义在 `nuttx/include/nuttx/mtd/mtd.h`

#### 1.3  参考实现

`nuttx/drivers/mtd/w25.c`

```C
/****************************************************************************
 * Name: w25_initialize
 *
 * Description:
 *   Create an initialize MTD device instance. MTD devices are not registered
 *   in the file system, but are created as instances that can be bound to
 *   other functions (such as a block or character driver front end).
 *
 ****************************************************************************/

FAR struct mtd_dev_s *w25_initialize(FAR struct spi_dev_s *spi)
{
  FAR struct w25_dev_s *priv;
  int ret;

  w25_finfo("spi: %p\n", spi);

  /* Allocate a state structure (we allocate the structure instead of using
   * a fixed, static allocation so that we can handle multiple FLASH devices.
   * The current implementation would handle only one FLASH part per SPI
   * device (only because of the SPIDEV_FLASH(0) definition) and so would
   * have to be extended to handle multiple FLASH parts on the same SPI bus.
   */

  /* 分配实例 */
  
  priv = kmm_zalloc(sizeof(struct w25_dev_s));
  if (priv)
    {
      /* Initialize the allocated structure (unsupported methods were
       * nullified by kmm_zalloc).
       */

      priv->mtd.erase  = w25_erase;
      priv->mtd.bread  = w25_bread;
      priv->mtd.bwrite = w25_bwrite;
      priv->mtd.read   = w25_read;
      priv->mtd.ioctl  = w25_ioctl;
#if defined(CONFIG_MTD_BYTE_WRITE) && !defined(CONFIG_W25_READONLY)
      priv->mtd.write  = w25_write;
#endif
      priv->mtd.name   = "w25";
      priv->spi        = spi;

      /* Deselect the FLASH */

      SPI_SELECT(spi, SPIDEV_FLASH(0), false);

      /* Identify the FLASH chip and get its capacity */

      ret = w25_readid(priv);
      if (ret != OK)
        {
          /* Unrecognized! Discard all of that work we just did and
           * return NULL
           */

          w25_ferr("ERROR: Unrecognized\n");
          kmm_free(priv);
          return NULL;
        }

    ...

  w25_finfo("Return %p\n", priv);
  return (FAR struct mtd_dev_s *)priv;
}
```

### 2、实现 NAND Flash 驱动

NAND Flash 的管理比 NOR Flash 更复杂，涉及坏块管理 (BBM) 和错误纠正码 (ECC)。`openvela` 提供了针对 NAND 的抽象层。

#### 2.1 核心数据结构：`nand_raw_s`

openvela 针对 NAND 闪存适配提供了底层驱动抽象，即 `struct nand_raw_s`。这一抽象结构体为驱动开发人员提供了一种标准化的方式来处理 NAND 闪存相关操作。驱动开发人员只需对 `struct nand_raw_s` 进行实例化，也就是创建该结构体的具体对象，填充相应的成员变量以适配实际的 NAND 闪存硬件特性。

您需要实现 `struct nand_raw_s` 结构体，它定义了更底层的 NAND 操作。

```C
// 定义于 nuttx/drivers/mtd/nand_raw.h
struct nand_raw_s {
  /* NAND data description */

  struct nand_model_s model; /* The NAND model storage */
  uintptr_t cmdaddr;         /* NAND command address base */
  uintptr_t addraddr;        /* NAND address address base */
  uintptr_t dataaddr;        /* NAND data address */
  uint8_t ecctype;           /* See NANDECC_* definitions */

  // 底层操作函数

  CODE int (*eraseblock)(FAR struct nand_raw_s *raw, off_t block);
  CODE int (*rawread)(FAR struct nand_raw_s *raw, off_t block,
                      unsigned int page, FAR void *data, FAR void *spare);
  CODE int (*rawwrite)(FAR struct nand_raw_s *raw, off_t block,
                       unsigned int page, FAR const void *data,
                       FAR const void *spare);

#ifdef CONFIG_MTD_NAND_HWECC
  CODE int (*readpage)(FAR struct nand_raw_s *raw, off_t block,
                       unsigned int page, FAR void *data, FAR void *spare);
  CODE int (*writepage)(FAR struct nand_raw_s *raw, off_t block,
                        unsigned int page, FAR const void *data,
                        FAR const void *spare);
#endif

...
}
```

在位错误纠正（ECC，Error - Correcting Code）处理方面，提供了 3 种方式：

1. 不需要 ECC 处理。
2. 软件 ECC：当开启配置项 `CONFIG_MTD_NAND_SWECC` 时，驱动支持通过软件方式进行 ECC 计算和错误纠正。软件 ECC 的实现意味着系统会在软件层面完成 ECC 码的生成、存储以及在读取数据时的错误检测和纠正操作。
3. 硬件 ECC：若采用硬件 ECC 方式，驱动的下半部逻辑不进行 ECC 计算，而是依赖硬件本身来提供 ECC 功能。硬件会自动完成 ECC 码的生成和错误检测纠正，减轻了软件的负担，提高了处理效率。

对应 `ecc_type` 字段：

1. NANDECC_NONE：不需要 ECC 处理。
2. NANDECC_SWECC：软件 ECC，使用通用的 Nuttx ECC处 理逻辑，配合 `CONFIG_MTD_NAND_SWECC` 使用。
3. NANDECC_HWECC：硬件 ECC ，配合 `CONFIG_MTD_NAND_HWECC` 使用。

```C
nuttx/include/nuttx/mtd/nand_raw.h
/* Type of ECC to be performed (may also need to be enabled in the
 * configuration)
 *
 *   NANDECC_NONE     No ECC, only raw NAND FLASH accesses
 *   NANDECC_SWECC    Software ECC.  Handled by the common MTD logic.
 *   NANDECC_HWECC    Values >= 2 are various hardware ECC implementations
 *                    all handled by the lower-half, raw NAND FLASH driver.
 *                    These hardware ECC types may be extended beginning
 *                    with the value NANDECC_HWECC.
 *
 * Software ECC is performed by common, upper-half MTD logic;  All
 * hardware assisted ECC operations are handled by the platform-specific,
 * lower-half driver.
 */

#define NANDECC_NONE                    0
#define NANDECC_SWECC                   1
#define NANDECC_HWECC                   2
```

#### 2.2. 开发流程

1. 实现并实例化 `struct nand_raw_s`。
2. 调用 `nand_initialize(FAR struct nand_raw_s *raw)`。此函数会处理 ONFI (Open NAND Flash Interface) 协议探测、ECC 初始化等通用逻辑，并返回一个配置好的 `struct mtd_dev_s *` 实例。
3. 完成实例化之后，能够通过 `register_mtddriver` 函数将其注册到虚拟文件系统层，以便系统进行统一管理和调度。

#### 2.3. ECC 和坏块管理

- **ECC**：`openvela` 支持硬件 ECC 和软件 ECC (`CONFIG_MTD_NAND_SWECC`)。

    - `rawread`/`rawwrite`：实现这两个接口时，您需要负责读/写数据区和备用区 (Spare Area)，但**不**进行 ECC 计算。
    - `readpage`/`writepage`：如果您的硬件支持 ECC，请实现这两个接口。`writepage` 应触发硬件生成 ECC 并写入，`readpage` 应触发硬件进行 ECC 校验和纠正。

- **坏块管理**：

    - 您的驱动需要决定坏块标记在备用区的存储位置。
    - `ioctl` 接口需要实现 `MTDIOC_ISBAD` 和 `MTDIOC_MARKBAD` 命令。

#### 2.4 参考实现

`nuttx/arch/arm/src/sam34/sam4s_nand.c`

```C
struct mtd_dev_s *sam_nand_initialize(int cs)
{
  struct sam_nandcs_s *priv;
  struct mtd_dev_s *mtd;
  uintptr_t cmdaddr;
  uintptr_t addraddr;
  uintptr_t dataaddr;
  uint8_t ecctype;
  int ret;

  finfo("CS%d\n", cs);

  if (SAM_SMCCS_BASE(cs) == SAM_SMC_CS0_BASE)
    {
      /* Refer to the pre-allocated NAND device structure */

      priv = &g_cs0nand;

      /* Set up the NAND addresses.  These must be provided in the board.h
       * header file.
       */
      cmdaddr  = BOARD_NCS0_NAND_CMDADDR;
      addraddr = BOARD_NCS0_NAND_ADDRADDR;
      dataaddr = BOARD_NCS0_NAND_DATAADDR;

      /* Pass on the configured ECC type */

      ecctype = SAM34_NCS0_ECCTYPE;
    }
  else
    {
      ferr("ERROR: CS%d unsupported or invalid\n", cs);
      return NULL;
    }

  /* Initialize the device structure */

  memset(priv, 0, sizeof(struct sam_nandcs_s));
  priv->raw.cmdaddr    = cmdaddr;
  priv->raw.addraddr   = addraddr;
  priv->raw.dataaddr   = dataaddr;
  priv->raw.ecctype    = ecctype;
  priv->raw.eraseblock = nand_eraseblock;
  priv->raw.rawread    = nand_rawread;
  priv->raw.rawwrite   = nand_rawwrite;

  priv->cs             = cs;
  priv->rb             = GPIO_SMC_RB;

  ret = board_nandflash_config(cs);
  if (ret < 0)
    {
      ferr("ERROR: board_nandflash_config failed for CS%d: %d\n",
           cs, ret);
      return NULL;
    }

  /* Reset the NAND FLASH part */

  nand_reset(priv);

  /* Probe the NAND part.  On success, an MTD interface that wraps
   * our raw NAND interface is returned.
   **/

  mtd = nand_initialize(&priv->raw);
  if (!mtd)
    {
      ferr("ERROR: CS%d nand_initialize failed\n", cs);
      return NULL;
    }

  /* Return the MTD wrapper interface as the MTD device */

  return mtd;
}
```

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

### 3、参考实现

一个典型的 MTD 设备分区创建 ptable 分区表例子如下：

```C
struct partition_s
{
  char   name[NAME_MAX + 1];    // 分区名
  size_t index;                 // 分区index
  size_t firstblock;            // 分区逻辑起始block地址
  size_t nblocks;               // 分区占用block数量，这个地方是page单位，不是eraseblock
  size_t blocksize;             // 分区每个block大小
};
```

```C
#define FLASH_FIRSTBLOCK   0x10000000   //addr
#define FLASH_BLOCK        0x1000       //block size
#define SST_FLASH_SIZE     (512 * 1024)
#define TEE_FLASH_SIZE     (512 * 1024)
#define AP_FLASH_SIZE      (2 * 1024 * 1024)
#define AUDIO_FLASH_SIZE   (2 * 1024 * 1024)

static const struct partition_s ptable[] =
{
  {
    .name       = "sst",
    .firstblock = FALSH_FIRSTBLOCK / FLASH_BLOCK,
    .nblocks    = SST_FLASH_SIZE / FLASH_BLOCK,
  },
  {
    .name       = "tee",
    .firstblock = (FALSH_FIRSTBLOCK + SST_FLASH_SIZE) / FLASH_BLOCK,
    .nblocks    = TEE_FLASH_SIZE / FLASH_BLOCK,
  },
  {
    .name       = "ap",
    .firstblock = (FALSH_FIRSTBLOCK + SST_FLASH_SIZE + TEE_FLASH_SIZE) / FLASH_BLOCK,
    .nblocks    = AP_FLASH_SIZE / FLASH_BLOCK,
  },
  {
    .name       = "audio",
    .firstblock = (FALSH_FIRSTBLOCK + SST_FLASH_SIZE + TEE_FLASH_SIZE + AP_FLASH_SIZE) / FLASH_BLOCK,
    .nblocks    = AUDIO_FLASH_SIZE / FLASH_BLOCK,
  },
}

//分区示例代码, path 为 parent mtd path
for (int idx = 0; idx < sizeof(ptable)/sizeof(ptable[0]); idx++)
  {
    char dev[32];
    
    snprintf(dev, sizeof(dev), "/dev/%s", &ptable[idx]->name);
    register_mtdpartition(dev, 0, path,
                        &ptable[idx]->firstblock,
                        &ptable[idx]->nblocks);
  }
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

- **fstest**：一个综合性的文件系统压力测试工具，可以挂载文件系统到您的 MTD 分区上进行读写、擦除、耗尽空间等测试。详情请参见 [fstest 文件系统压力测试工具指南](./../../debugging_tools/stress_testing/fstest.md)。
- **cmocka_block_test**：虽然名为 block test，但它也可以通过 MTD 的块设备代理（如 `/dev/mtdblock0`）来测试底层的 `bread` 和 `bwrite` 接口是否正确。详情请参见 [blktest 块设备 I/O 测试指南](./../../debugging_tools/stress_testing/blktest.md)。
