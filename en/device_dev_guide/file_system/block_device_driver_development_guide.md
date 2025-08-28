# Block Device Driver Development Guide

\[ English | [简体中文](../../../zh-cn/device_dev_guide/file_system/block_device_driver_development_guide.md) \]

## I. Overview

This document guides developers on how to adapt block devices for the `openvela` system, focusing on eMMC or SD cards connected via the SDIO bus interface as an example. You will learn how to implement the lower-half of the SDIO driver and bind it with the generic `mmcsd` upper-half block device driver.

**Note**: The mmc/sd driver path is `nuttx/drivers/mmcsd`

### 1. Prerequisites

Before you begin, please ensure you are familiar with the `openvela` storage driver framework. It is recommended to first read the [Storage Driver Framework Guide](./storage_driver_framework_guide.md).

### 2. Architecture Overview

`openvela` supports eMMC/SD cards through a layered architecture:

1. **Upper-Half Block Device Driver (`mmcsd`)**: Implements all the common logic related to the eMMC/SD card protocol, such as card identification, initialization, command sending/receiving, etc. This part is provided by `openvela`.
2. **Lower-Half SDIO Driver**: Responsible for interacting with the specific SDIO host controller hardware. **This is the part that needs to be implemented by the chip or board vendor.**

Your core task is to implement the `struct sdio_dev_s` interface, which serves as a bridge between the upper-level `mmcsd` and the underlying hardware.

![img](./figures/007.png)

### 3. Core Data Structures

- **`struct sdio_dev_s`**: Defines the low-level operations for the SDIO host controller.
- **`struct block_operations`**: Defines the standard block device operations interface, which is implemented by the `mmcsd` upper-half. You only need to call `register_blockdriver` to register it.

## II. Block Device Driver Development Process

Developing an SDIO-based block device driver typically follows these steps:

1. **Implement the SDIO Controller Interface**: Write the specific implementations for functions like `reset`, `sendcmd`, `recvsetup`, `dmasendsetup`, etc., based on the hardware manual.
2. **Instantiate `sdio_dev_s`**: Define a static `sdio_dev_s` struct variable and assign the function pointers implemented in the previous step to it.
3. **Provide an SDIO Initialization Function**: Write a global initialization function (e.g., `my_chip_sdio_initialize()`) that returns a pointer to the instantiated `sdio_dev_s` struct.
4. **Bind the `mmcsd` and SDIO Drivers**: In the board-level initialization code, call `mmcsd_slotinitialize()` to bind your SDIO driver instance with the `mmcsd` upper-half driver. This function will automatically complete the card initialization and call `register_blockdriver` to register the block device node (e.g., `/dev/mmcsd0`).

## III. Implementing the SDIO Lower-Half Interface

You need to provide an instance of `struct sdio_dev_s`. The following is a description of some of the key interfaces:

```C
// Defined in nuttx/include/nuttx/sdio.h
struct sdio_dev_s {
  /* Mutual exclusion */
  int (*lock)(FAR struct sdio_dev_s *dev, bool lock);

  /* Initialization and configuration */
  void (*reset)(FAR struct sdio_dev_s *dev);
  sdio_capset_t (*capabilities)(FAR struct sdio_dev_s *dev);
  void (*widebus)(FAR struct sdio_dev_s *dev, bool enable); // Set bus width
  void (*clock)(FAR struct sdio_dev_s *dev, enum sdio_clock_e rate); // Set clock
  int (*attach)(FAR struct sdio_dev_s *dev); // Attach interrupt

  /* Command and data transfer */
  int (*sendcmd)(FAR struct sdio_dev_s *dev, uint32_t cmd, uint32_t arg);
  int (*recv_r1)(FAR struct sdio_dev_s *dev, uint32_t cmd, uint32_t *r1);
  // ... Other response receive functions (R2-R7)
  
  /* Non-DMA data transfer setup */
  int (*recvsetup)(FAR struct sdio_dev_s *dev, FAR uint8_t *buffer, size_t nbytes);
  int (*sendsetup)(FAR struct sdio_dev_s *dev, FAR const uint8_t *buffer, size_t nbytes);
  
  /* DMA data transfer setup (if supported) */
#ifdef CONFIG_SDIO_DMA
  int (*dmarecvsetup)(FAR struct sdio_dev_s *dev, FAR uint8_t *buffer, size_t buflen);
  int (*dmasendsetup)(FAR struct sdio_dev_s *dev, FAR const uint8_t *buffer, size_t buflen);
#endif

  // ... Other event and callback interfaces
};
```

### Key Interface Implementation Points

- **`capabilities`**: Returns the features supported by your SDIO controller, such as support for 4-bit/8-bit mode, DMA support, etc.
- **`status`**: Returns the card's status, most importantly `SDIO_STATUS_PRESENT` (whether the card is inserted).
- **`sendcmd`/`recv_r*`**: Implements the low-level logic for sending commands to the card and receiving responses.
- **`setup`**: These functions are used to prepare for data transfer. For example, `dmarecvsetup` should configure the DMA controller to be ready to receive data from the SDIO interface into the specified `buffer`. The actual data transfer is triggered by the `mmcsd` upper-half through interfaces like `sdio_io_rw_extended`.

## IV. Binding and Registration

After completing the implementation and instantiation of `sdio_dev_s`, the final step is to bind it with `mmcsd` in the board-level initialization code.

```C
// A typical implementation, referenced from nuttx/boards/arm/sama5/sama5d3-xplained/src/sam_mmcsd.c
#include <nuttx/sdio.h>
#include <nuttx/mmcsd.h>

int my_board_mmcsd_init(void)
{
  FAR struct sdio_dev_s *sdio;
  int ret;
  
  // 1. Get the instance of your implemented SDIO lower-half driver
  //    (Assuming my_chip_sdio_initialize(0) initializes the 0th SDIO interface)
  sdio = my_chip_sdio_initialize(0);
  if (!sdio) {
    // Error handling
    return -ENODEV;
  }
  
  // 2. Bind the SDIO instance with the mmcsd upper-half
  //    (Assuming this card is registered with minor device number 0, i.e., /dev/mmcsd0)
  ret = mmcsd_slotinitialize(0, sdio);
  if (ret != OK) {
    // Error handling
    return ret;
  }
  
  // 3. (Optional) Configure card detection interrupt
  // ...
  
  return OK;
}
```

`mmcsd_slotinitialize()` will complete all subsequent tasks, including:

- Communicating with the SD card to complete the initialization sequence.
- Obtaining the card's geometry information (sector size, count, etc.).
- Calling `register_blockdriver()` to register it as a block device.

## V. Reference Implementation

`nuttx/boards/arm/at32/at32f437-mini/src/at32_mmcsd.c`

```C
struct at32_dev_s g_sdiodev =
{
  .dev =
  {
#ifdef CONFIG_SDIO_MUXBUS
    .lock             = at32_lock,
#endif
    .reset            = at32_reset,
    .capabilities     = at32_capabilities,
    .status           = at32_status,
    .widebus          = at32_widebus,
    .clock            = at32_clock,
    .attach           = at32_attach,
    .sendcmd          = at32_sendcmd,
#ifdef CONFIG_SDIO_BLOCKSETUP
    .blocksetup       = at32_blocksetup,
#endif
    .recvsetup        = at32_recvsetup,
    .sendsetup        = at32_sendsetup,
    .cancel           = at32_cancel,
    .waitresponse     = at32_waitresponse,
    .recv_r1          = at32_recvshortcrc,
    .recv_r2          = at32_recvlong,
    .recv_r3          = at32_recvshort,
    .recv_r4          = at32_recvshort,
    .recv_r5          = at32_recvshortcrc,
    .recv_r6          = at32_recvshortcrc,
    .recv_r7          = at32_recvshort,
    .waitenable       = at32_waitenable,
    .eventwait        = at32_eventwait,
    .callbackenable   = at32_callbackenable,
    .registercallback = at32_registercallback,
#ifdef CONFIG_SDIO_DMA
#ifdef CONFIG_AT32_SDIO_DMA
#ifdef CONFIG_ARCH_HAVE_SDIO_PREFLIGHT
    .dmapreflight     = at32_dmapreflight,
#endif
    .dmarecvsetup     = at32_dmarecvsetup,
    .dmasendsetup     = at32_dmasendsetup,
#else
#ifdef CONFIG_ARCH_HAVE_SDIO_PREFLIGHT
    .dmapreflight     = NULL,
#endif
    .dmarecvsetup     = at32_recvsetup,
    .dmasendsetup     = at32_sendsetup,
#endif
#endif
  },
  .waitsem = SEM_INITIALIZER(0),
};

/****************************************************************************
 * Name: sdio_initialize
 *
 * Description:
 *   Initialize SDIO for operation.
 *
 * Input Parameters:
 *   slotno - Not used.
 *
 * Returned Value:
 *   A reference to an SDIO interface structure.  NULL is returned on
 *   failures.
 *
 ****************************************************************************/

struct sdio_dev_s *sdio_initialize(int slotno)
{
  /* There is only one slot */

  struct at32_dev_s *priv = &g_sdiodev;

  /* Allocate a DMA channel */

#ifdef CONFIG_AT32_SDIO_DMA
  priv->dma = at32_dmachannel(SDIO_DMACHAN);
  DEBUGASSERT(priv->dma);
#endif

  /* Configure GPIOs for 4-bit, wide-bus operation (the chip is capable of
   * 8-bit wide bus operation but D4-D7 are not configured).
   *
   * If bus is multiplexed then there is a custom bus configuration utility
   * in the scope of the board support package.
   */

#ifndef CONFIG_SDIO_MUXBUS
  at32_configgpio(GPIO_SDIO_D0 | SDIO_PULLUP_ENABLE);
#ifndef CONFIG_AT32_SDIO_WIDTH_D1_ONLY
  at32_configgpio(GPIO_SDIO_D1 | SDIO_PULLUP_ENABLE);
  at32_configgpio(GPIO_SDIO_D2 | SDIO_PULLUP_ENABLE);
  at32_configgpio(GPIO_SDIO_D3 | SDIO_PULLUP_ENABLE);
#endif
  at32_configgpio(GPIO_SDIO_CK | SDIO_PULLUP_ENABLE);
  at32_configgpio(GPIO_SDIO_CMD | SDIO_PULLUP_ENABLE);
#endif

  /* Reset the card and assure that it is in the initial, unconfigured
   * state.
   */

  at32_reset(&priv->dev);
  return &g_sdiodev.dev;
}

/****************************************************************************
 * Name: at32_sdinitialize
 *
 * Description:
 *   Initialize the SPI-based SD card.  Requires CONFIG_DISABLE_MOUNTPOINT=n
 *   and CONFIG_AT32_SDIO=y
 *
 ****************************************************************************/

int at32_sdinitialize(int minor)
{
#ifdef HAVE_MMCSD
  struct sdio_dev_s *sdio;
  int ret;

  /* First, get an instance of the SDIO interface */

  sdio = sdio_initialize(AT32_MMCSDSLOTNO);
  if (!sdio)
    {
      ferr("ERROR: Failed to initialize SDIO slot %d\n", AT32_MMCSDSLOTNO);
      return -ENODEV;
    }

  finfo("Initialized SDIO slot %d\n", AT32_MMCSDSLOTNO);

  /* Now bind the SDIO interface to the MMC/SD driver */

  ret = mmcsd_slotinitialize(minor, sdio);
  if (ret != OK)
    {
      ferr("ERROR:");
      ferr(" Failed to bind SDIO slot %d to the MMC/SD driver, minor=%d\n",
              AT32_MMCSDSLOTNO, minor);
    }

  finfo("Bound SDIO slot %d to the MMC/SD driver, minor=%d\n",
         AT32_MMCSDSLOTNO, minor);

  /* Then let's guess and say that there is a card in the slot.
   * I need to check to see if the M3 Wildfire board supports a GPIO to
   * detect if there is a card in the slot.
   */

  sdio_mediachange(sdio, true);
#endif
  return OK;
}
```

## VI. Testing and Validation

`openvela` provides testing tools to verify your block device driver:

- **fstest**: A comprehensive file system stress testing tool. You can first create a file system on `/dev/mmcsd0` (e.g., using `mkfatfs`), then mount it and use `fstest` for testing. For details, please see the [fstest File System Stress Testing Tool Guide](./../../debugging_tools/stress_testing/fstest.md).
- **cmocka_block_test**: Can directly perform low-level block read/write tests on the `/dev/mmcsd0` device node to verify the correctness and performance of the `read` and `write` interfaces. For details, please see the [blktest Block Device I/O Test Guide](./../../debugging_tools/stress_testing/blktest.md).
