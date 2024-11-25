# openvela 项目

\[ [English](README.md) | 简体中文 \]

openvela 的命名源自拉丁语中船帆的含义，也是南方星空中船帆星座的名字。我们选择这个名字的意义是希望与开发者一道携手，共同踏上星辰大海的征途。

## 项目介绍

openvela 操作系统专为 AIoT 领域量身定制，以轻量化、标准兼容、安全性和高度可扩展性为核心特点。openvela 以其卓越的技术优势，已成为众多物联网设备和 AI 硬件的技术首选，涵盖了智能手表、运动手环、智能音箱、耳机、智能家居设备以及机器人等多个领域。



## 技术优势

- **高度可扩展**：openvela 的设计注重模块化与可扩展性，使其能够灵活适应多样的物联网应用场景。小到仅配备 32K RAM 的微型 BLE 模组，大到拥有 256M RAM 的智能有屏音箱，openvela 都能提供高度可扩展的支持。

- **一站式解决方案**：随着时间的推移，openvela 不断沉淀了各类 AIoT 应用的共性需求，成为一个功能完备的软件平台，为各类物联网解决方案提供了全面的支持。厂商采用 openvela，可以显著降低研发成本并加速产品的上市时间。

- **成熟的异构计算支持**：openvela 为异构多核系统提供了强大的支持，实现了 MCU、MPU、DSP、GPU 以及 NPU 等不同处理单元间无缝的 IPC 通信机制。此外，openvela 还提供了一个高级的 RPC 框架，简化了 openvela 与 Android 和 Linux 系统的通信，使快速打造一个异构融合操作系统成为可能。

- **标准兼容和高可移植性**：openvela 内核基于 Apache NuttX ，这个被称为 “Tiny Linux” 的系统为 openvela 提供了高标准的 POSIX 兼容性。通过持续提升其 POSIX 兼容性，openvela 当前已达到 88% 的兼容水平。这种高标准的兼容性意味着在其他标准操作系统（例如 Linux）上开发的软件可以轻松迁移到 openvela，几乎不需要额外的工作。

- **全面的连接套件**：openvela 提供了广泛的协议支持，包括蓝牙 BR/EDR/LE、LE Mesh、WiFi、Matter、LTE Cat1、以太网、CAN/LIN 等。同时，它还能与小米的 HyperConnect 协议无缝集成，提供了强大的连接能力。

- **丰富的开发者工具**：openvela 提供了一系列完备的开发者工具，包括系统监控、性能分析、调试器、追踪、崩溃分析和日志分析工具，为开发者提供了强大的支持。



## 硬件支持

openvela 支持各种不同的架构（ARM32、ARM64、Risc-V、Xtensa、MIPS、CEVA 等）和硬件平台。请在[硬件支持](https://nuttx.apache.org/docs/latest/platforms/index.html)页面上查看完整列表。



## 快速入门

如果您想要体验 openvela，我们提供一个功能完备的模拟器，无需硬件平台即可使用。有关详细信息，请参阅如下指南。

1. [准备开发环境](./Getting_Started/Set_up_the_development_environment_zh-cn.md)
2. [下载 openvela 源码](./Getting_Started/Download_Vela_sources_zh-cn.md)
3. [编译 openvela 源码](./Getting_Started/Build_Vela_from_sources_zh-cn.md)
4. [使用 openvela Emulator 运行 openvela](./Getting_Started/Run_Vela_on_Vela_Emulator_zh-cn.md)


## 示例

* [音乐播放器示例](./Examples/Music_Player_Example_zh-cn.md)
* [智能手环示例](./Examples/Smart_Band_Example_zh-cn.md)
* [自行车码表示例](./Examples/X_Track_zh-cn.md)

## 代码贡献

参与贡献：[代码贡献指南](CONTRIBUTING_zh-cn.md)。



## 许可协议

这个代码库中的代码使用 Apache 2.0 许可证。你可以在[这里](https://www.apache.org/licenses/LICENSE-2.0.txt)找到更多关于 Apache 2.0 许可证的信息。

openvela引用三方开源软件及许可证说明，参考[第三方开源软件说明](Third_Party_and_Open_Source_Components_zh-cn.md)。



## 联系方式

为了更好地管理和响应反馈和支持请求，建议通过以下方式联系我们：

- **GitHub Issues**: 如果你有任何问题、建议或发现任何 Bug，请在 Issues 页面提交一个新的 Issue。请尽量提供详细的信息，以便我们更快地理解和解决问题。
- **Pull Requests**: 如果你发现了问题并已经修复，欢迎提交 Pull Request。请确保遵循我们的 [贡献指南](./CONTRIBUTING_zh-cn.md)。
- **Discussions**: 如果你有更广泛的话题或讨论，可以在 Discussions 页面发起一个新的讨论。

我们非常感谢每一位用户的反馈和支持，通过 GitHub 平台进行交流可以帮助我们更好地维护和改进项目。

