# 新硬件适配赛道详细指引

## 赛题目标

旨在加速 openvela 的硬件生态多样化，鼓励参赛者将 openvela 适配到更多芯片与开发板上，让 AIoT 操作系统能力覆盖更广泛的硬件场景。

## 赛题说明

选择一款尚未适配 openvela 的硬件平台，完成从底层 BSP 移植、驱动开发到系统构建的全链路适配工作，使 openvela 能够在目标硬件上正常启动并运行核心功能。

### 适配参考范围（不限于此）

- 芯片级 BSP（Board Support Package）开发与移植
- 外设驱动适配（UART / SPI / I2C / GPIO / Display / Audio / Wi-Fi / Bluetooth 等）
- 系统启动流程与内存配置调优
- 构建系统集成（defconfig 配置、编译工具链适配）
- 硬件能力验证与基础功能 Demo

## 重点鼓励

- 将已适配 NuttX 但尚未支持 openvela 的芯片/开发板移植到 openvela
- 从 0 到 1 为全新芯片平台完成 openvela 首次适配

## 参赛要求

1. **完成系统移植**：实现 openvela 在目标硬件上的启动引导、基础外设驱动（至少包含 UART 控制台输出）、系统正常运行
2. **提交适配代码**：将适配代码提交至 openvela 开源社区，包含 defconfig 配置、板级初始化代码、必要的驱动适配

## 评分加分项

本赛道作品在评分体系「技术难度」维度（30 分）中具备显著优势：

- 适配的硬件平台覆盖范围越广、驱动越完整（GPIO、SPI、I2C、WiFi、BLE、LCD、音频等），技术得分越高
- 在适配基础上开发了应用 Demo（如传感器采集、屏幕显示、蓝牙通信）
- 适配了全新架构（如 RISC-V、MIPS）或国产芯片平台
- 针对特定硬件能力（如 AI 加速器、低功耗传感器、多媒体引擎）进行深度优化适配
- 代码质量高、文档完整，可直接合入 openvela 主线
- 编写了详细的适配指南，方便后续开发者复现

## 参考资源

| 资源                                                                              | 说明                                    |
| --------------------------------------------------------------------------------- | --------------------------------------- |
| [NuttX 已支持平台列表](https://nuttx.apache.org/docs/latest/platforms/index.html) | 选择目标硬件的参考                      |
| [支持的硬件平台](./supported_hardware.md)                                         | 大赛提供的开发板清单（已支持 + 待适配） |
| [openvela 已适配硬件清单](../../dev_board/Development_Board.md)                   | 避免重复适配（已适配的不计入本赛道）    |
| [openvela 驱动开发指南](../../device_dev_guide/driver/driver_development.md)      | 板级适配与驱动开发参考                  |
| [openvela 芯片移植指南](../../chip_porting/porting_guide.md)                      | 完整的芯片移植流程                      |

## 适合人群

- 有嵌入式开发经验，熟悉 MCU/MPU 板级开发
- 对操作系统移植、驱动开发感兴趣的硬件极客
- 手头有开发板，想尝试在新平台上跑 openvela 的开发者
