# openvela Peripheral Drivers Overview

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/driver/peripheral_driver/peripheral_drivers_overview.md) \]

openvela provides a rich and standardized peripheral driver framework designed to simplify low-level hardware access and management. This framework supports a wide range of common peripherals through a unified API, helping developers quickly build upper-layer applications.

The following table categorizes and describes the main peripheral drivers supported by openvela:

| **Category**                       | **Driver Name**              | **Full Name / Abbreviation**        | **Description**                                                                                                                           |
| :--------------------------------- | :--------------------------- | :---------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **System Core & Bus**              | Direct Memory Access         | DMA (Direct Memory Access)          | Enables high-speed data transfer between peripherals and memory without occupying the CPU.                                                |
|                                    | Pin Control                  | Pinctl (Pin Control)                | Manages and configures the functional multiplexing and electrical characteristics (e.g., pull-up/pull-down, drive strength) of chip pins. |
| **Security & Randomness**          | Random Number Generator      | RNG (Random Number Generator)       | Provides a hardware interface to generate true or pseudo-random numbers for scenarios like cryptography and security protocols.           |
|                                    | Cryptography Engine          | Crypto (Cryptography)               | Uses hardware to accelerate cryptographic operations such as symmetric/asymmetric encryption and hash calculations.                       |
| **Data Processing & Acceleration** | Hardware Accelerator         | Accel (Accelerator)                 | Offloads CPU-intensive computing tasks, such as graphics processing or AI operations.                                                     |
| **Analog & Conversion**            | Analog Signal Processing     | Analog                              | Includes drivers like ADC (Analog-to-Digital Converter) and DAC (Digital-to-Analog Converter) for processing analog signals.              |
| **General-Purpose Interface**      | General-Purpose Input/Output | GPIO (General-Purpose Input/Output) | Controls the electrical level (high/low) of pins to implement basic digital signal input and output.                                      |
| **Sensor & Positioning**           | Sensor                       | Sensor                              | Provides a unified access interface for various sensors, such as accelerometers, gyroscopes, and temperature/humidity sensors.            |
|                                    | Global Positioning System    | GPS (Global Positioning System)     | Parses positioning data from a GPS module to obtain geospatial information like latitude, longitude, and speed.                           |
| **Human-Machine Interaction**      | Vibrator                     | Vibrator                            | Controls a vibration motor to provide haptic feedback to the user.                                                                        |
|                                    | Infrared Communication       | IR (Infrared)                       | Implements the transmission and reception of infrared signals, commonly used in applications like remote controls.                        |
| **Wireless Communication**         | Near Field Communication     | NFC (Near Field Communication)      | Supports contactless data exchange and identification between devices over a short distance.                                              |

Subsequent chapters will detail the implementation, configuration methods, and API usage guidelines for each of these driver types.