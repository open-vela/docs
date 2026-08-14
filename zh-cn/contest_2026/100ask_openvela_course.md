# openvela 快速入门与工程实践课程（百问网）

> 百问网（100ASK）韦东山团队与 openvela 官方联合推出的 openvela 完整实战课程。课程从开发环境搭建讲起，最终落地一台能听、会说、带动态表情的 AI 语音机器人。

## 课程资料

| 资源     | 地址                                                                                                             |
| -------- | ---------------------------------------------------------------------------------------------------------------- |
| 视频课程 | [B 站：openvela 快速入门与工程实践](https://www.bilibili.com/video/BV1th3e6gENh/)                                |
| 配套文档 | [《openvela 快速入门与工程实践》Rev 1.2](./attachment/openvela快速入门与工程实践_v1.2.pdf)（2026/04/08，342 页） |

配套开发板为 [百问网 DShanPixVela-Devkit](https://www.100ask.net/hardware/detail/16)（全志 R528，openvela 板级代号 `r528s3-dshanpi`），是本届大赛支持硬件之一，板级说明见 [r528s3-dshanpi README](../../../../../vendor_allwinnertech/blob/dev-ai-contest-2026/boards/r528/r528s3-dshanpi/README_zh-cn.md)。

## 课程内容

课程共 9 章、124 讲：

1. **openvela 开发环境搭建与体验** —— 环境搭建、体验 openvela、VSCode 配置
2. **openvela 系统介绍** —— 裸机开发的缺陷、RTOS 的优势与挑战、为何选择 openvela
3. **openvela 多任务系统开发** —— 任务/线程/调度、FIFO 与 RR 调度实验、消息队列、信号量、互斥量、信号、openvelaRPC，含调度与 IPC 的源码分析
4. **openvela 驱动程序开发** —— 驱动模型与驱动分层、I2C 与 SPI 控制器驱动、触摸屏驱动、Framebuffer 与 SPI LCD 驱动实例
5. **openvela 文件系统** —— VFS 使用与内部实现、binfs / procfs / tmpfs / romfs
6. **openvela 的启动与构建** —— 启动流程、GCC 与 Makefile 基础、Kconfig、构建脚本解析
7. **跨核通信** —— RPMSG 分层与通道建立、基于 VirtIO 的跨核通信
8. **openvela 调试技术** —— `ps` / `top` / `memdump` / `dumpstack` 等命令的使用与内部机制、堆实现、栈回溯、Crash log 解读、GDB 与 Coredump
9. **项目实战：AI 语音聊天机器人** —— 麦克风采集与 Opus 编解码、HTTPS 设备激活、WebSocket 上云交互、LVGL 显示文本与动态表情、系统集成

## 对参赛者的价值

- **配套开发板即大赛支持硬件**：选用 DShanPixVela-Devkit 的团队可直接按课程流程搭建环境、编译烧写。
- **通用能力不限开发板**：第 3、4、6、8 章（多任务与 IPC、驱动开发、构建系统、调试技术）适用于所有 openvela 开发板。
- **语音类作品的参考实现**：第 9 章的完整链路（麦克风采集 → Opus 编码 → WebSocket 上云 → 解码播放 → LVGL 表情渲染）与多数语音交互类作品的技术路径一致。

> 课程与配套资料由百问网维护并持续更新（当前配套文档为 Rev 1.2）。开发板购买与课程咨询请访问[百问网官网](https://www.100ask.net/)，资料下载见[百问网 r528s3-dshanpi 资料页](https://download.100ask.net/project/item7/index.html)。
