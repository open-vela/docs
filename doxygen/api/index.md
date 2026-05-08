# API 参考文档

本文档提供 openvela 操作系统的 API 参考，涵盖从内核系统调用到应用框架的完整接口说明。

openvela 基于 Apache NuttX RTOS 构建，遵循 POSIX 标准，支持 ARM、ARM64、RISC-V、x86_64 等多种架构。开发者可通过以下章节查阅各层级的 API 接口：

- **[内核接口](kernel/index.md)** — 进程/线程管理、任务调度、内存管理、信号机制、消息队列等 POSIX 兼容的系统接口
- **[网络接口](network/index.md)** — BSD 套接字、DNS 解析等标准网络编程接口
- **[应用框架](framework/index.md)** — Binder IPC、蓝牙、多媒体、安全（TEE + Keystore）、uORB 消息总线等上层能力接口
