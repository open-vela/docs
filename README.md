# openvela Project

\[ English | [简体中文](README_zh-cn.md) \]

Openvela is named after the Latin word for sail, which is also the name of the constellation of Vela in the southern sky. We chose this name because we hope to work hand in hand with developers and embark on a journey to the stars and the sea together.

## openvela Introduction

The openvela operating system is tailored for the AIoT field, with lightweight, standard compatibility, security and high scalability as its core features. With its outstanding technical advantages, openvela has become the technical choice for many IoT devices and AI hardware, covering smart watches, sports bracelets, smart speakers, headphones, smart home devices, robots and other fields.

## Technical Advantages

- **Highly Scalable**: The design of openvela focuses on modularity and scalability, making it flexible to adapt to a variety of IoT application scenarios. From a micro BLE module with only 32K RAM to a smart speaker with a screen with 256M RAM, openvela can provide highly scalable support.

- **One-Stop Solution**: Over time, openvela has continuously accumulated the common needs of various AIoT applications and has become a fully functional software platform that provides comprehensive support for various IoT solutions. Manufacturers can significantly reduce R&D costs and accelerate product time to market by adopting openvela.

- **Mature Heterogeneous Computing Support**: openvela provides strong support for heterogeneous multi-core systems, realizing seamless IPC communication mechanisms between different processing units such as MCU, MPU, DSP, GPU, and NPU. In addition, openvela also provides an advanced RPC framework that simplifies the communication between openvela and Android and Linux systems, making it possible to quickly build a heterogeneous fusion operating system.

- **Standard Compliant and High Portability**: The openvela kernel is based on Apache NuttX, a system called "Tiny Linux" that provides openvela with high standards of POSIX compatibility. By continuously improving its POSIX compatibility, openvela has currently reached a compatibility level of 88%. This high standard of compatibility means that software developed on other standard operating systems (such as Linux) can be easily migrated to openvela with little additional work.

- **Comprehensive Connectivity Suite**: openvela provides a wide range of protocol support, including Bluetooth BR/EDR/LE, LE Mesh, WiFi, Matter, LTE Cat1, Ethernet, CAN/LIN, etc. At the same time, it can also seamlessly integrate with Xiaomi's HyperConnect protocol, providing powerful connectivity capabilities.

- **Rich Developer Tools**: openvela provides a complete range of developer tools, including system monitoring, performance analysis, debugger, tracing, crash analysis and log analysis tools, providing strong support for developers.

## Hardware Support
openvela supports a variety of different architectures (ARM32, ARM64, Risc-V, Xtensa, MIPS, CEVA, etc.) and hardware platforms. Please see the full list on the [Hardware Support](https://nuttx.apache.org/docs/latest/platforms/index.html) page.


## Quick Start

If you want to experience openvela, we provide a fully functional simulator that can be used without a hardware platform. For more information, please refer to the following guide.

1. [Prepare the development environment](./Getting_Started/Set_up_the_development_environment.md)
2. [Download openvela source code](./Getting_Started/Download_Vela_sources.md)
3. [Compile openvela source code](./Getting_Started/Build_Vela_from_sources.md)
4. [Run openvela with openvela Emulator](./Getting_Started/Run_Vela_on_Vela_Emulator.md)

## Examples

* [Music Player Example](./Examples/Music_Player_Example.md)
* [Smart Band Example](./Examples/Smart_Band_Example.md)
* [Bicycle Track Example](./Examples/X_Track.md)

##  Code Contributions

Contribute: [Contribution Guideline](./CONTRIBUTING.md).

## License Agreement

The code in this repository is licensed under the Apache 2.0 license. You can find more information about Apache 2.0 license [here](https://www.apache.org/licenses/LICENSE-2.0.txt).

Third-party license: [Third-Party Open-Source Software and License Notice](Third_Party_and_Open_Source_Components.md)


## Contact

In order to better manage and respond to feedback and support requests, we recommend contacting us through the following methods:

- **GitHub Issues**: If you have any questions, suggestions, or find any bugs, please submit a new issue on the Issues page. Please try to provide detailed information so that we can understand and solve the problem faster.
- **Pull Requests**: If you find an issue and have fixed it, you are welcome to submit a Pull Request. Please make sure to follow our [Contribution Guide](./CONTRIBUTING.md).
- **Discussions**: If you have a broader topic or discussion, you can start a new discussion on the Discussions page.

We are very grateful for the feedback and support of every user. Communicating through the GitHub platform can help us better maintain and improve the project.