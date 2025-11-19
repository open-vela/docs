# Sensor Framework Guide

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/driver/peripheral_driver/sensor/sensor_framework_guide.md) \]

## I. Overview

Sensors are the perceptual core of Internet of Things (IoT) systems, responsible for converting changes in the physical world (such as motion, light, and temperature) into digital signals. To address the growing variety of sensors and the resulting complexity in application development, a unified and efficient software framework is essential.

## II. Architecture Evolution

The openvela Sensor framework has evolved from a simple model to a more complex architecture to adapt to changing product requirements.

### 1. Early Model: Native Character Devices

The initial sensor driver model in openvela was primarily based on simple character devices. Applications operated sensors by directly accessing `/dev/xxx` device nodes through standard system calls such as `open`, `read`, and `ioctl`.

The drawback of this model was that it exposed the full complexity of sensor management to the application layer.

### 2. Sensor Framework 2.0: Layering and Message-Driven Architecture

With increasing demands for low power consumption, multi-core communication, and standardization, openvela significantly refactored the Sensor framework, leading to the current stable and efficient 2.0 architecture.

The latest Sensor framework (labeled **Vela Sensor Fw** on the right side of the diagram) is based on two core design principles: **layered decoupling** and a **message-driven** approach. It primarily consists of two components: the **Sensor Driver Stack** and the **uORB Middleware**.

<img src="./figures/001.png" alt="Sensor Framework 2.0" width="100%">

## III. Core Architecture Details

The latest Vela Sensor software architecture is composed of two main parts: the **Sensor Driver Stack** and the **uORB Middleware**. These components work together to achieve layered decoupling between hardware and applications.

### 1. Sensor Driver Stack

The Sensor Driver Stack is responsible for interacting with the physical hardware and providing a unified interface to the upper layers. To facilitate code reuse and separation of concerns, the driver stack is designed with two layers: an **Upper Half** and a **Lower Half**.

#### Upper Half Driver (Common Layer)

This layer does not interact directly with hardware. Instead, it provides a common framework and set of services for all sensor drivers. Its main responsibilities include:

- **Device Node Management**: Automatically creates standardized device nodes, such as `/dev/sensor/accel0`.
- **System Call Interface**: Provides a standard `file_operations` structure to respond to requests from the kernel.
- **Resource Management**: Implements multi-user access control through reference counting.
- **Data Buffering**: Features a built-in, efficient circular buffer to cache sensor events.
- **Advanced Features**: Manages batch mode and provides a unified `ioctl` control interface.

#### Lower Half Driver (Hardware Adaptation Layer)

This layer is the actual hardware driver, implemented by **driver developers** for specific sensor chips. Its core responsibilities are:

- **Hardware Interaction**: Configures and controls the sensor hardware via buses like I2C/SPI.
- **Standard Interface Implementation**: Implements standard callback functions such as `activate` (to enable/disable), `set_interval` (to set the sampling rate), and `batch` (to configure batch processing).
- **Data Acquisition and Reporting**: Fetches data from the hardware via interrupts or polling, encapsulates it into a `sensor_event`, and sends it to the Upper Half's circular buffer.
- **Multi-core Communication Support (Rpmsg Lower Half)**: As a special type of Lower Half, it enables cross-core sensor data communication. A CPU on one core can transparently subscribe to a topic published by another core, and vice versa, providing distributed sensing capabilities for multi-core heterogeneous systems.

### 2. uORB Middleware

uORB acts as the crucial bridge between drivers and applications. It employs a publish-subscribe model and implements automatic power management for sensors.

- **Publish-Subscribe Model**:

    - **Application Layer**: Applications no longer access device nodes directly. Instead, they **subscribe** to sensor topics of interest through the uORB API to receive data.
    - **Driver Layer**: During initialization, a sensor driver **advertises** its corresponding topics to uORB.

- **Automatic Power Management**:

    - uORB monitors the subscription status of all topics.
    - When a topic is subscribed to for the **first time**, uORB automatically calls the lower-half driver's `activate` function through the driver framework to **enable** the sensor.
    - When the **last subscriber** to a topic unsubscribes, uORB automatically calls the function to **disable** the sensor, thus achieving intelligent and efficient power management.

To help developers in different roles use the framework efficiently, the following documentation explains the framework from the perspectives of both application developers and driver developers.