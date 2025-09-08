# USB CDC-ACM Class Driver Guide

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/driver/bus_driver/USB/usb_cdcacm_driver_guide.md) \]

## I. Overview

This document provides a detailed guide for developers on configuring and using the USB Communication Device Class (CDC) Abstract Control Model (ACM) driver in the **openvela** system.

CDC-ACM is a standard USB protocol that emulates a virtual serial port between a host and a device. It is widely used for scenarios such as debugging, log output, and data transfer. The protocol primarily defines two types of communication endpoints:

- **Control Endpoint**: Used to transfer and configure control-related information for the virtual serial port, such as baud rate and data bits.
- **Data Endpoints**: Used for the bidirectional transfer of actual serial data.

## II. Using CDC-ACM in USB Device Mode

Refer to this section when you need to configure an openvela device to act as a USB virtual serial port device (e.g., making a COM port appear when a development board is connected to a PC). For general adaptation methods for the driver and related interfaces, please refer to the [USB Device Driver Development Guide](./usb_driver_dev_guide.md).

### 1. Single-Device Mode

In this mode, the USB device functions solely as a CDC-ACM device.

#### Kconfig Configuration

Enable the following core options in your project's `defconfig` file:

```Makefile
# Enable the core USB Device driver
CONFIG_USBDEV=y
# Enable the CDC-ACM device class driver
CONFIG_CDCACM=y
# Enable Interface Association Descriptor (IAD), used to correctly
# identify function groups in composite devices
CONFIG_COMPOSITE_IAD=y

# --- Optional Configuration ---
# Enable USB high-speed mode
CONFIG_USBDEV_DUALSPEED=y
# Enable USB DMA transfers
CONFIG_USBDEV_DMA=y

# Custom device VID (Vendor ID)
CONFIG_CDCACM_VENDORID
# Custom device PID (Product ID)
CONFIG_CDCACM_PRODUCTID
```

#### Initialization

You need to call the `cdcacm_initialize()` function during the system startup process to initialize the CDC-ACM device. This function is already implemented in the openvela system.

The recommended place to call it is within the board-level initialization function `up_initialize()` or in a dedicated thread that detects USB connections.

### 2. Composite Device Mode

In this mode, CDC-ACM is combined with other USB functions (such as ADB, RNDIS) to form a composite device.

#### Kconfig Configuration

```Makefile
# --- Core USB Configuration ---
CONFIG_USBDEV=y
# Enable the USB composite device framework
CONFIG_USBDEV_COMPOSITE=y
# Enable Interface Association Descriptor (IAD)
CONFIG_COMPOSITE_IAD=y

# --- CDC-ACM Related Configuration ---
CONFIG_CDCACM=y
# Enable CDC-ACM support in composite device mode
CONFIG_CDCACM_COMPOSITE=y

# --- Optional Configuration ---
CONFIG_USBDEV_DUALSPEED=y
CONFIG_USBDEV_DMA=y
CONFIG_CDCACM_VENDORID
CONFIG_CDCACM_PRODUCTID
```

#### Initialization

In composite device mode, you need to implement two board-support package (BSP) functions for your hardware platform to describe and connect the composite device.

- `board_composite_initialize()`: Performs architecture-specific initialization required for the composite device.
- `board_composite_connect()`: Connects and registers the various USB functions, including CDC-ACM, based on a configuration ID.

These functions are typically also called during the `up_initialize()` process or from a USB connection thread.

The following is an example implementation of `board_composite_connect()`, showing how to add CDC-ACM to a composite device:

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

### 3. Testing Guide

For testing instructions, refer to the [USB Device Simulation (SIM) Driver Guide](./sim/usb_device_sim_guide.md#iii-usage-guide-testing-usb-functions).

## III. Using CDC-ACM in USB Host Mode

Refer to this section when you need your openvela device to act as a host to connect and control an external CDC-ACM device (such as a USB-to-serial module). For general adaptation methods for the driver and related interfaces, please refer to the [USB Host Driver Development Guide](./usb_driver_host_guide.md).

### 1. Kconfig Configuration

```Makefile
# --- Core USB Host Configuration ---
CONFIG_USBHOST=y
# Enable support for USB composite devices
CONFIG_USBHOST_COMPOSITE=y

# --- CDC-ACM Host Related Configuration ---
CONFIG_USBHOST_CDCACM=y
# Enable support for the CDC-ACM function in composite devices
CONFIG_CDCACM_COMPOSITE=y
# Enable reduced-memory (simplified) mode
CONFIG_USBHOST_CDCACM_REDUCED=y
```

### 2. Initialization

You need to call the `usbhost_cdcacm_initialize()` function during the system startup process to register the CDC-ACM class driver with the USB Host core. When a compatible CDC-ACM device is connected to the host, this driver will be automatically loaded and enumerated.

The following is an initialization example on the `sim` platform:

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

### 3. Testing Guide

After initialization, when you connect an external USB serial device to the openvela host, a device node (e.g., `/dev/ttyACM0`) should be automatically created in the system's `/dev` directory. You can communicate with the external device by reading from and writing to this node, just like a standard serial port. For detailed testing methods, please refer to the [USB Host Driver Development Guide](./usb_driver_host_guide.md).

## IV. References

- [USB Device Simulation (SIM) Driver Guide](./sim/usb_device_sim_guide.md)
- [USB Host Simulation (SIM) Driver Guide](./sim/usb_host_sim_guide.md)
- [USB Host Driver Development Guide](./usb_driver_host_guide.md)