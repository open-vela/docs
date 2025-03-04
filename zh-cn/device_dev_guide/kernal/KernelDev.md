# 内核开发

## 一、概述

openvela 内核基于当前实时嵌入式操作系统中对 POSIX 标准支持率最高的 NuttX 内核，提供了以下关键特性：

- 实时响应性：支持多线程、信号量、消息队列、定时器等实时操作系统特性，并保持优先级继承机制。
- 文件系统与网络支持：兼容多种文件系统和网络连接协议。
- 驱动接口兼容性：兼容 Linux/xBSD 驱动访问接口，为上层通用 Linux 用户程序、模块组件复用和互联通信奠定基础。

这些特性使得 Openvela 能够在嵌入式设备中提供高效、可靠的实时操作能力。

## 二、支持的处理器架构

openvela 支持多种处理器架构，涵盖了主流嵌入式设备的硬件平台，包括但不限于以下架构：

- ARM（A/R/M，包括 64 位架构）
- AVR
- MIPS
- RISC-V
- x86/64
- Xtensa
- CEVA
- CSKY
- Z80

### 1、硬件平台支持

Openvela 可运行在多种嵌入式设备上，例如：

- Espressif
- Allwinner
- Microchip/Atmel
- NXP/Freescale
- Nordic
- ST
- TI

### 2、多处理器支持

openvela 同时支持以下多处理器模式：

1. SMP（Symmetric Multiprocessing）：多个处理器共享同一内存和总线，提升并发响应效率。
2. AMP（Asymmetric Multiprocessing）：每个处理器拥有独立的内存和总线，并通过通信机制实现协作。

这些特性使得 Openvela 能够在多个芯片和子系统上同时部署，确保系统的可靠性和实时性能。

## 三、相关仓

开发者可以通过以下代码仓库获取 openvela 的内核代码和相关资源：

- [openvela NuttX 仓库](https://github.com/open-vela/nuttx)

## 四、后续操作

在接下来的章节中，将详细介绍 openvela 内核的各个模块功能特性，帮助开发者根据不同硬件资源定制产品。

openvela 可支持存储空间小至 **128KB** 的模组，适用于多种嵌入式场景。
