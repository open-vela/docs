# 新硬件适配赛道详细指引

## 赛题目标

旨在加速 openvela 的硬件生态多样化，鼓励参赛者将 openvela 适配到更多芯片与开发板上，让 AIoT 操作系统能力覆盖更广泛的硬件场景。

## 赛题说明

选择一款尚未适配 openvela 的硬件平台，完成从底层 BSP 移植、驱动开发到系统构建的全链路适配工作，使 openvela 能够在目标硬件上正常启动并运行核心功能。

> 可选的待适配平台见 [支持的硬件平台 — 待适配开发板](./supported_hardware.md#二待适配开发板)（已适配的开发板不计入本赛道）。

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

## 提交方式

本赛道涉及修改 openvela 的 vendor / nuttx 等仓库（跨仓适配），须走**跨仓需求单独审批**流程：

1. **申请**：向赛事组报备需求（要适配哪块板、需改动哪些仓库）。
2. **评估**：赛事组确认需求合理性。
3. **开仓**：由 SCM 为该需求单独建仓并配置权限。
4. **开发**：在分配的仓库内完成适配（defconfig 配置、板级初始化代码 `boards/`、必要的驱动适配，以及便于复现的适配说明）。
5. **日志归集**：AI Coding 日志仍由插件统一写入本队 demo 仓的 `logs/` 目录。

> 大赛仅在 GitHub 进行（不在 Gitee）。**获奖后**，适配代码按要求 PR 至 openvela 上游对应 vendor 仓库（如 `vendor_st`、`vendor_espressif`、`vendor_rockchip`、`vendor_artinchip` 等）的 `dev-ai-contest-2026` 分支，走标准 PR + CI 流程。各开发板对应的具体仓库，见 [《支持的硬件平台》](./supported_hardware.md) 中每块板的"开发指南"链接。

## 评分加分项

本赛道作品在评分体系「技术难度」维度（30 分）中具备显著优势：

- 适配的硬件平台覆盖范围越广、驱动越完整（GPIO、SPI、I2C、WiFi、BLE、LCD、音频等），技术得分越高
- 在适配基础上开发了应用 Demo（如传感器采集、屏幕显示、蓝牙通信）
- 适配了全新架构（如 RISC-V、MIPS）或国产芯片平台
- 针对特定硬件能力（如 AI 加速器、低功耗传感器、多媒体引擎）进行深度优化适配
- 代码质量高、文档完整，可直接合入 openvela 主线
- 编写了详细的适配指南，方便后续开发者复现

## 参考资源

| 资源                                                                                             | 说明                                                                                                 |
| ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| [NuttX 已支持平台列表](https://nuttx.apache.org/docs/latest/platforms/index.html)                | 选择目标硬件的参考                                                                                   |
| [支持的硬件平台](./supported_hardware.md)                                                        | 大赛提供的开发板清单（已支持 + 待适配）                                                              |
| [openvela 已适配硬件清单](../../dev_board/Development_Board.md)                                  | 避免重复适配（已适配的不计入本赛道）                                                                 |
| [openvela 驱动开发指南](../../device_dev_guide/driver/driver_development.md)                     | 板级适配与驱动开发参考                                                                               |
| [openvela 芯片移植指南](../../chip_porting/porting_guide.md)                                     | 完整的芯片移植流程                                                                                   |
| [openvela AI 驱动开发技能集](../../../../../../.claude/blob/dev-ai-contest-2026/README_zh-cn.md) | AI 辅助驱动开发：`nuttx-driver-development` / `driver-code-reviewer` skill + `driver-workflow` agent |

## AI 辅助开发（推荐）

大赛鼓励使用 AI Coding 完成开发并沉淀有效 Skill。openvela 官方提供了一套面向驱动开发的 AI 技能集（位于 [`.claude`](../../../../../../.claude/blob/dev-ai-contest-2026/README_zh-cn.md) 仓库），与本赛道高度契合，推荐配合使用：

- **`nuttx-driver-development`（skill）**：创建/更新/审查 NuttX 设备驱动，覆盖 sensor、char、network、fb/LCD、USB、audio、电源电池、MCAL、I2C/SPI 等子系统。
- **`driver-code-reviewer`（skill）**：驱动代码质量审查（59 Pattern + 双轮交叉验证 + 量化评分），提交前自检。
- **`driver-workflow`（agent）**：驱动开发端到端工作流，覆盖新驱动开发、改进现有驱动、代码审查、测试生成四种模式（6 步流程 / 3 次交互，从需求到提交）。

将 `.claude` 仓库克隆到 openvela 项目根目录下，AI 助手即可自动发现并在驱动开发任务中调用这些能力。详细用法见 [`.claude/README_zh-cn.md`](../../../../../../.claude/blob/dev-ai-contest-2026/README_zh-cn.md)。

> 注意：这些驱动相关的 skill 与 agent 仅提供**基线驱动适配**，生成结果需要参赛者进一步优化与贡献，才能达到可用、可合入主线的质量。

## 适合人群

- 有嵌入式开发经验，熟悉 MCU/MPU 板级开发
- 对操作系统移植、驱动开发感兴趣的硬件极客
- 手头有开发板，想尝试在新平台上跑 openvela 的开发者
