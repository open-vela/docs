# 新硬件适配赛道教程导航

> 本页面是 openvela AI 硬件开发者大赛「新硬件适配赛道」相关文档的总入口，帮助参赛者快速找到所需资料。

## 文档列表

| 文档 | 说明 |
| ---- | ---- |
| [新硬件适配赛道详细指引](./hardware_porting_track_guide.md) | 赛道概述、赛题要求、评分加分项、参考资源。 |
| [最小可运行 NSH 系统 defconfig 参考](./defconfig_reference/minimum_nsh_baseline.md) | L0 起步 defconfig：在新开发板上先启动到 NSH 命令行提示符，再按需逐步启用文件系统、网络、传感器等子系统。 |
| openvela 芯片移植指南 | 从零完成 BSP 移植的完整流程（位于 docs 仓库 `zh-cn/chip_porting/porting_guide.md`）。 |
| openvela 驱动开发指南 | UART/SPI/I2C 等各类驱动的适配与使用。[在线文档](https://doc.openvela.com/document?id=198&version=trunk&language=cn) |

## 如何开始

1. **阅读赛道指引** → 明确赛题要求和评分加分项
2. **选择目标硬件** → 参考 NuttX 已支持平台列表，挑选一块尚未适配 openvela 的板子
3. **跟着芯片移植指南动手** → 完成 BSP 移植、驱动适配、系统启动
4. **提交代码** → fork + PR 到 `dev-ai-contest-2026` 分支

> 代码统一基于 openvela 大赛分支 `dev-ai-contest-2026` 开发与提交。
