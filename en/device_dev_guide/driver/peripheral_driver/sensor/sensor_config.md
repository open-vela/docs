# Sensor Configuration Options

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/driver/peripheral_driver/sensor/sensor_config.md) \]

This document details the core Kconfig options for the openvela Sensor subsystem, covering the main framework, multi-core communication, and various virtual and simulation drivers.

## I. Core Framework

This option is fundamental to enabling all sensor functionalities.

- **`CONFIG_SENSORS`: Enable the sensor subsystem.**

    As the master switch for the sensor framework, this option compiles and initializes the core abstraction layer for sensor drivers. You must enable this option for the system to support any sensor devices.

## II. Multi-Core Communication Support

This option enables efficient sensor data flow in a multi-core processor (MPU) environment.

- **`CONFIG_SENSORS_RPMSG`: Enable RPMsg-based multi-core communication for sensors.**

    This option adds communication capabilities based on the RPMsg (Remote Processor Messaging) protocol to the sensor subsystem. When enabled, it allows uORB topics to be transferred, published, and subscribed between different processor cores, which is crucial for achieving cross-core data sharing in heterogeneous multi-core architectures.

## III. Virtual and Simulation Drivers

Virtual and simulation drivers are primarily used during development and testing, allowing sensor data to be simulated in an environment without physical hardware.

- **`CONFIG_SENSORS_FAKESENSOR`: Enable the Fake Sensor driver.**

    This driver simulates real sensor input by reading preset data from the file system and publishing it as a uORB topic. This feature allows you to develop and debug high-level application logic independently in a hardware-detached environment.

- **`CONFIG_SENSORS_GOLDFISH_SENSOR`: Enable the Goldfish emulator sensor driver.**

    Enable this option when running NuttX in the Android Goldfish emulator environment. It retrieves virtual sensor data (e.g., accelerometer, gyroscope) from the emulator.

    - **`CONFIG_SENSORS_GOLDFISH_GNSS`: Enable the Goldfish emulator GNSS driver.**

        This is a sub-option of `CONFIG_SENSORS_GOLDFISH_SENSOR` specifically for retrieving virtual GNSS (Global Navigation Satellite System) position data from the emulator.

- **`CONFIG_SENSORS_WTGAHRS2`: Enable the WTGAHRS2 sensor driver.**

    This option compiles the driver for the WTGAHRS2 AHRS (Attitude and Heading Reference System) sensor. The driver can connect to real sensor hardware or be used in a simulation environment to provide attitude data to the system.

## IV. Configuration File Paths

The related Kconfig files are located at the following paths:

- **Sensor Driver Kconfig**: `drivers/sensors/Kconfig`
- **uORB Kconfig**: `apps/system/uorb/Kconfig`

## V. Related Documents

For more information on uORB configuration, refer to the following document:

- **uORB Configuration**: [uORB Configuration](../../../middleware/uorb_config.md)
