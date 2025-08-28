# MTD Driver Development Guide

\[ English | [简体中文](../../../zh-cn/device_dev_guide/file_system/mtd_driver_development_guide.md) \]

## I. Overview

This document provides detailed guidance for developers on how to adapt MTD (Memory Technology Device) model-based storage devices, such as NOR Flash and NAND Flash, for the `openvela` system. You will learn how to implement the lower-half interface of an MTD driver and register it with the system.

### 1. Prerequisites

Before you begin, please ensure you are familiar with the `openvela` storage driver framework. It is recommended to first read the [Storage Driver Framework Guide](./storage_driver_framework_guide.md).

### 2. Core Data Structure: `mtd_dev_s`

In `openvela`, all MTD devices are abstracted through the `struct mtd_dev_s` structure. Your main task is to implement the callback functions defined in this structure and populate the device information.

```C
// Defined in nuttx/include/nuttx/mtd/mtd.h
struct mtd_dev_s
{
  // Erase a specified number of blocks
  int (*erase)(FAR struct mtd_dev_s *dev, off_t startblock, size_t nblocks);

  // Read by block
  ssize_t (*bread)(FAR struct mtd_dev_s *dev, off_t startblock,
                   size_t nblocks, FAR uint8_t *buffer);
  // Write by block
  ssize_t (*bwrite)(FAR struct mtd_dev_s *dev, off_t startblock,
                    size_t nblocks, FAR const uint8_t *buffer);

  // Read by byte (optional)
  ssize_t (*read)(FAR struct mtd_dev_s *dev, off_t offset, size_t nbytes,
                  FAR uint8_t *buffer);
#ifdef CONFIG_MTD_BYTE_WRITE
  // Write by byte (optional, requires CONFIG_MTD_BYTE_WRITE)
  ssize_t (*write)(FAR struct mtd_dev_s *dev, off_t offset, size_t nbytes,
                   FAR const uint8_t *buffer);
#endif

  // Control interface, for getting geometry info, bulk erase, etc.
  int (*ioctl)(FAR struct mtd_dev_s *dev, int cmd, unsigned long arg);

  // MTD device name
  FAR const char *name;
};
```

## II. MTD Driver Development Process

![img](./figures/006.png)

Developing the lower-half of an MTD driver typically follows these steps:

1. **Implement Device Operation Interfaces**: Based on the hardware manual, write the specific implementations for functions like `erase`, `bread`, `bwrite`, and `ioctl`.
2. **Instantiate `mtd_dev_s`**: Define a static `mtd_dev_s` struct variable and assign the function pointers implemented in the previous step to it.
3. **Provide an Initialization Function**: Write a global initialization function (e.g., `my_chip_mtd_initialize()`) that returns a pointer to the instantiated `mtd_dev_s` struct.
4. **Register the MTD Device**: In the board-level initialization code, call your initialization function to get the MTD device instance, then use `register_mtddriver()` to register it with the VFS.
5. **(Optional) Create Partitions**: If needed, call `register_mtdpartition()` to divide a single MTD device into multiple logical partitions.

## III. Implementing the MTD Lower-Half Interface

This section will use NOR Flash and NAND Flash as examples to introduce the key points of interface implementation.

### 1. Implementing a NOR Flash Driver

`openvela` provides an excellent NOR Flash driver template at `nuttx/drivers/mtd/skeleton.c`. You can use this as a starting point for your development.

#### 1.1 Instantiating `mtd_dev_s`

First, define a private device structure that contains an instance of `mtd_dev_s`. Then, create a static global variable and assign your implementations to its set of operation functions.

```C
// Example: Define a private device structure
struct my_nor_dev_s {
  struct mtd_dev_s mtd;
  // Add other hardware-related private data, such as locks, status, etc.
};

// Example: Function implementation
static int my_nor_erase(FAR struct mtd_dev_s *dev, off_t startblock, size_t nblocks);
static ssize_t my_nor_bread(FAR struct mtd_dev_s *dev, off_t startblock, size_t nblocks, FAR uint8_t *buf);
// ... Other function implementations

// Example: Instantiation
static struct my_nor_dev_s g_nor_dev = {
  .mtd = {
    .erase  = my_nor_erase,
    .bread  = my_nor_bread,  // read by page size
    .bwrite = my_nor_bwrite, // write by page size
    .read   = my_nor_read,   // read by byte
    .write  = my_nor_write,  // interface for byte-wise writing (depends on CONFIG_MTD_BYTE_WRITE)
    .ioctl  = my_nor_ioctl,
    .name   = "my_nor_flash"
  }
};
```

#### 1.2 Implementing the `ioctl` Interface

`ioctl` is a critical interface, and the `MTDIOC_GEOMETRY` command must be implemented. You need to return the basic dimensional information of the Flash here.

```C
static int my_nor_ioctl(FAR struct mtd_dev_s *dev, int cmd, unsigned long arg) {
  switch (cmd) {
    case MTDIOC_GEOMETRY:
    {
      FAR struct mtd_geometry_s *geo = (FAR struct mtd_geometry_s *)arg;
      if (geo) {
        // Fill in these values according to your hardware manual
        geo->blocksize    = 256;    // Read/write block size (Page Size)
        geo->erasesize    = 4096;   // Erase block size (Sector Size)
        geo->neraseblocks = 1024;   // Total number of erase blocks
        return OK;
      }
      return -EINVAL;
    }

    case MTDIOC_BULKERASE:
    {
      // Implement bulk erase logic
      return OK;
    }
    
    // ... Handle other commands
    
    default:
      return -ENOTTY;
  }
}
```

> The complete `ioctl` interface is defined in `nuttx/include/nuttx/mtd/mtd.h`

#### 1.3. Reference Implementation

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

  /* Allocate instance */
  
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

### 2. Implementing a NAND Flash Driver

NAND Flash management is more complex than NOR Flash, involving Bad Block Management (BBM) and Error Correction Codes (ECC). `openvela` provides an abstraction layer for NAND.

#### 2.1 Core Data Structure: `nand_raw_s`

`openvela` provides a low-level driver abstraction for adapting NAND flash, which is `struct nand_raw_s`. This abstract structure provides a standardized way for driver developers to handle NAND flash-related operations. Driver developers only need to instantiate `struct nand_raw_s`, that is, create a specific object of this structure, and fill the corresponding member variables to adapt to the actual NAND flash hardware characteristics.

You need to implement the `struct nand_raw_s` structure, which defines lower-level NAND operations.

```C
// Defined in nuttx/drivers/mtd/nand_raw.h
struct nand_raw_s {
  /* NAND data description */

  struct nand_model_s model; /* The NAND model storage */
  uintptr_t cmdaddr;         /* NAND command address base */
  uintptr_t addraddr;        /* NAND address address base */
  uintptr_t dataaddr;        /* NAND data address */
  uint8_t ecctype;           /* See NANDECC_* definitions */

  // Low-level operation functions

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

For bit error correction (ECC, Error-Correcting Code) handling, three methods are provided:

1. No ECC handling is required.
2. Software ECC: When the `CONFIG_MTD_NAND_SWECC` option is enabled, the driver supports ECC calculation and error correction via software. The implementation of software ECC means that the system will perform ECC code generation, storage, and error detection and correction operations at the software level when reading data.
3. Hardware ECC: If hardware ECC is used, the lower-half logic of the driver does not perform ECC calculations, but relies on the hardware itself to provide the ECC function. The hardware automatically completes ECC code generation and error detection/correction, reducing the software's burden and improving processing efficiency.

Corresponding to the `ecc_type` field:

1. NANDECC_NONE: No ECC handling is required.
2. NANDECC_SWECC: Software ECC, using the common Nuttx ECC handling logic, used with `CONFIG_MTD_NAND_SWECC`.
3. NANDECC_HWECC: Hardware ECC, used with `CONFIG_MTD_NAND_HWECC`.

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

#### 2.2 Development Process

1. Implement and instantiate `struct nand_raw_s`.
2. Call `nand_initialize(FAR struct nand_raw_s *raw)`. This function handles common logic like ONFI (Open NAND Flash Interface) protocol detection, ECC initialization, etc., and returns a configured `struct mtd_dev_s *` instance.
3. After instantiation is complete, it can be registered with the virtual file system layer via the `register_mtddriver` function, allowing the system to manage and schedule it uniformly.

#### 2.3 ECC and Bad Block Management

- **ECC**: `openvela` supports hardware ECC and software ECC (`CONFIG_MTD_NAND_SWECC`).

    - `rawread`/`rawwrite`: When implementing these interfaces, you are responsible for reading/writing the data area and the Spare Area, but **not** for performing ECC calculations.
    - `readpage`/`writepage`: If your hardware supports ECC, implement these two interfaces. `writepage` should trigger the hardware to generate and write the ECC, and `readpage` should trigger the hardware to perform ECC checking and correction.

- **Bad Block Management**:

    - Your driver needs to decide the storage location of the bad block marker in the spare area.
    - The `ioctl` interface needs to implement the `MTDIOC_ISBAD` and `MTDIOC_MARKBAD` commands.

#### 2.4 Reference Implementation

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

## IV. Registration and Partitioning

### 1. Registering an MTD Device

In the board-level initialization code, call `register_mtddriver()` to register your device under the `/dev` directory.

```C
// In the board-level initialization function
FAR struct mtd_dev_s *mtd_dev;

// 1. Get the MTD device instance
mtd_dev = my_nor_initialize(); // Your initialization function

if (mtd_dev) {
  // 2. Register the device
  int ret = register_mtddriver("/dev/mynor", mtd_dev, 0666, NULL);
  if (ret < 0) {
    // Handle error
  }
}
```

### 2. Creating MTD Partitions

`openvela` allows you to divide a single physical MTD device into multiple logical partitions for easier management.

- **Core function**: `mtd_partition()` creates an MTD sub-device representing a partition.
- **Registration function**: `register_mtdpartition()` encapsulates the logic for creating and registering partitions.

```C
// Example: Divide /dev/mynor into two partitions
// "config" partition: starts at block 0, spans 16 erase blocks
register_mtdpartition("/dev/config", 0666, "/dev/mynor", 0, 16);

// "userdata" partition: starts at block 16, spans 1008 erase blocks
register_mtdpartition("/dev/userdata", 0666, "/dev/mynor", 16, 1008);
```

### 3. Reference Implementation

A typical example of creating a ptable partition table for an MTD device is as follows:

```C
struct partition_s
{
  char   name[NAME_MAX + 1];    // Partition name
  size_t index;                 // Partition index
  size_t firstblock;            // Logical starting block address of the partition
  size_t nblocks;               // Number of blocks occupied by the partition, this is in units of pages, not eraseblocks
  size_t blocksize;             // Size of each block in the partition
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

//Partitioning example code, path is the parent mtd path
for (int idx = 0; idx < sizeof(ptable)/sizeof(ptable[0]); idx++)
  {
    char dev[32];
    
    snprintf(dev, sizeof(dev), "/dev/%s", &ptable[idx]->name);
    register_mtdpartition(dev, 0, path,
                        &ptable[idx]->firstblock,
                        &ptable[idx]->nblocks);
  }
```

## V. Related Kernel Configuration (Kconfig)

Ensure that the necessary MTD and related modules are enabled in your `defconfig` file:

```Makefile
# Enable MTD core support
CONFIG_MTD=y

# Enable MTD partition support
CONFIG_MTD_PARTITION=y
CONFIG_MTD_PROGMEM=y

# Enable BCH proxy to support accessing MTD via file interfaces
CONFIG_BCH=y
CONFIG_BCH_BUFFER_ALIGNMENT=32 //86panel & k03 alignment = 0

# Read/write cache configuration
CONFIG_DRVR_WRITEBUFFER=y
CONFIG_DRVR_WRDELAY=350
# Read buffer is not enabled in most projects
# CONFIG_DRVR_READAHEAD is not set
# CONFIG_DRVR_READBYTES is not set
```

## VI. Testing and Verification

`openvela` provides a rich set of testing tools to verify your MTD driver:

- **fstest**: A comprehensive file system stress testing tool. You can mount a file system onto your MTD partition to perform tests like reading, writing, erasing, and exhausting space. For details, please see the [fstest File System Stress Testing Tool Guide](./../../debugging_tools/stress_testing/fstest.md).
- **cmocka_block_test**: Although named block test, it can also test whether the underlying `bread` and `bwrite` interfaces are correct through the MTD's block device proxy (e.g., `/dev/mtdblock0`). For details, please see the [blktest Block Device I/O Test Guide](./../../debugging_tools/stress_testing/blktest.md).
