# VirtIO Framework

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/kernel/inter_processor_communication/VirtIO/VirtIO_Framework.md) \]

## I. Introduction

openvela has implemented a complete VirtIO framework based on OpenAMP. This framework supports the implementation of various VirtIO drivers compatible with the VirtIO standard at the upper layer, such as VirtIO-Net and VirtIO-Block; and supports different VirtIO transport layer implementations at the lower layer, including VirtIO-MMIO, VirtIO-PCI, etc.

## II. Architecture Diagram

### 1. Framework Diagram

The following figure shows the overall structure of the openvela VirtIO framework, which can be divided into the following three parts:

1. Driver Layer:

    The driver layer is responsible for docking VirtIO with the openvela driver framework. The driver layer completes device initialization and data interaction by calling the unified interfaces provided by VirtIO.

2. VirtIO Layer:

    The VirtIO layer provides unified interfaces for drivers, supporting registration, uninstallation, and matching mechanisms for Drivers and Devices.

3. Transport Layer:

    The transport layer supports various transport methods, including MMIO, RemoteProc, and PCI.

![img](./figures/011.svg)

### 2. Flow Diagram

![img](./figures/012.svg)

The above figure shows the matching process and call relationship between VirtIO Device and VirtIO Driver:

1. Driver Registration:

    During openvela initialization, call `virtio_register_drivers()` to register all supported VirtIO Drivers into the VirtIO bus.

2. Device Registration:

    The registration process is initiated by the transport layer:

    - The MMIO transport layer calls `virtio_register_mmio_device()`.
    - The REMOTEPROC transport layer calls `rptun_register_device()`.
    - The PCI transport layer calls `virtio_pci_probe()`. After the transport layer completes initialization, call `virtio_register_device()` to register the VirtIO Device into the VirtIO bus.

3. Driver and Device Matching:

    When the device is registered to the bus, the system attempts to match the Driver and Device. If the matching is successful, execute the `probe` function implemented by the Driver. In the `probe` function, the driver initializes, configures, and negotiates features (feature negotiation) for the VirtIO Device. Depending on the complexity and type of the device, it may also be necessary to initialize private structures or perform additional operations.

4. Register openvela Driver:

    The driver is registered into the virtual file system (VFS) for user access via the API provided by the OpenVela driver framework.

5. Operation:

    During operation, the Driver will call the general `virtqueue` interfaces provided by OpenAMP to exchange data and send notifications in the VirtIO standard format, thereby implementing driver functions.

## III. Code Directory

```plaintext
|--- nuttx
|    |--- drivers
|    |    |--- virtio
|    |         |--- virtio.c       # Core implementation of the VirtIO framework
|    |--- include
|    |    |--- nuttx
|    |         |--- virtio
|    |              |--- virtio.h  # VirtIO header file
|    |--- openamp
|    |    |--- open-amp            # OpenAMP repository
```

## IV. API Description

This section describes the interfaces that need to be called during the adaptation of VirtIO drivers.

### 1. openvela Log Interfaces

- `vrtinfo(...)`

    Description: INFO-level log interface for the VirtIO system.

- `vrtwarn(...)`

    Description: WARNING-level log interface for the VirtIO system.

- `vrterr(...)`

    Description: ERROR-level log interface for the VirtIO system.

### 2. openvela VirtIO Framework Interfaces

`int virtio_register_driver(FAR struct virtio_driver *driver)`

Description: Register a VirtIO Driver to the VirtIO bus. When a corresponding device already exists in the bus, it will immediately match and call the `probe` function implemented by the driver. If there is no corresponding device in the bus, the driver's `probe` function will be called back to complete driver initialization after a corresponding VirtIO device is registered to the VirtIO bus.

### 3. OpenAMP Interfaces

#### Preliminary Knowledge

- Driver TX virtqueue:

    The driver's transmission queue. Obtain buffers from the `used ring` of `txvq`, fill in the data to be sent, and then add them to the `avail ring` of `txvq` to complete the data transmission process.

- Driver RR virtqueue:

    The driver's reception queue. Obtain buffers from the `used ring` of `rxvq`, read the data therein, and then return them to the `avail ring` of `rxvq` to complete the data reception process.

#### Interface Description

- `void *virtqueue_get_buffer(struct virtqueue *vq, uint32_t *len, uint16_t *idx)`

    Description: Obtain a buffer from the `used ring` of the virtqueue.

    Parameters:

    - `vq`: Pointer to the virtqueue.
    - `len`: Length of the obtained buffer.
    - `idx`: Index of the obtained buffer in the `used ring`.

- `int virtqueue_add_buffer(struct virtqueue *vq, struct virtqueue_buf *buf_list, int readable, int writable, void *cookie)`

    Description: Add a buffer to the `avail ring` of the `virtqueue`.

    Parameters:
    - `vq`: Pointer to the virtqueue.
    - `buf_list`: Array of buffers to be added.
    - `readable`: Number of readable buffers in `buf_list`, indicating the part expected to be read by the device (Device).
    - `writable`: Number of writable buffers in `buf_list`, indicating the part expected to be filled by the device (Device).
    - `cookie`: Cache pointer, which will be returned when calling `virtqueue_get_buffer` to obtain the buffer.

- `void virtqueue_kick(struct virtqueue *vq)`

    Description: Notify the device (Device). Typically, after sending data to the device or returning a buffer to the device, this function is called to notify the device to proceed with the next operation.

    Parameters:
    - `vq`: Pointer to the virtqueue.

- `virtqueue_enable_cb(struct virtqueue *vq)` and `virtqueue_disable_cb(struct virtqueue *vq)`

    Description: Enable or disable interrupts for the virtqueue.

    Parameters:
    - `vq`: Pointer to the virtqueue.

## V. Related Documents

- [virtio: Towards a De-Facto Standard For Virtual I/O Devices](https://ozlabs.org/~rusty/virtio-spec/virtio-paper.pdf)
- [Virtual I/O Device (VIRTIO) Version 1.2](https://docs.oasis-open.org/virtio/virtio/v1.2/csd01/virtio-v1.2-csd01.pdf)