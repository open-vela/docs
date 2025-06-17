# 安全配置

\[ [English](../../../en/device_dev_guide/security/security_configuration.md) | 简体中文 \]

## 一、简介

本文介绍如何通过 Kconfig 配置，在设备或模拟器上搭建 TEE（Trusted Execution Environment）和安全服务框架。配置内容涵盖 TEE 核 和 AP 核，包括以下核心模块：

- TEE 框架：提供可信执行环境的基础。
- 跨核通信配置：实现 AP 核与 TEE 核的高效通信。
- 应用 CA（Client Application）和 TA（Trusted Application）：支持客户端应用和可信应用的运行。

## 二、架构图

以下架构图展示了 TEE 和安全服务框架的核心组成部分及其运行环境。

![img](figures/001.svg)

## 三、代码目录

| 序号 | 代码目录                                   | 描述                |
| :--- | :----------------------------------------- | :------------------ |
| 1    | `frameworks/security`                      | CA 和 TA 框架代码   |
| 2    | `external/optee/optee_os/optee_os`         | OPTEE OS 源代码     |
| 3    | `external/optee/optee_client/optee_client` | OPTEE 客户端代码    |
| 4    | `frameworks/security/optee_vela`           | OPTEE Vela 相关代码 |
| 5    | `external/optee/optee_test/optee_test`     | OP-TEE 测试代码     |

## 四、TEE 核配置

以下内容介绍了 TEE 核的配置项，包括跨核通信、WAMR 运行时环境及 TA 的相关功能配置。  

| 序号 | 配置项                                             | 是否必选 | 默认值 | 功能描述                                   | 备注                     |
| :--- | :------------------------------------------------- | :------- | :----- | :----------------------------------------- | :----------------------- |
| 1    | `CONFIG_OPTEE_OS`                                  | 是       | `y`    | TEE OS 框架的基础配置                      |                          |
| 2    | `CONFIG_NET_RPMSG`                                 | 是       | `y`    | AP 与 TEE 跨核通过 RPMSG 通信              |                          |
| 3    | `CONFIG_RPTUN`                                     | 是       | `y`    |                                            |                          |
| 4    | `CONFIG_OPTEE_SERVER_RPMSG`                        | 是       | `y`    |                                            |                          |
| 5    | `CONFIG_RPMSG_LOCAL_CPUNAME`                       | 是       | `tee`  |                                            |                          |
| 6    | `CONFIG_BOARDCTL_UNIQUEID`                         | 是       | `y`    | 需要硬件厂商提供 Hardware Unique Key 适配  |                          |
| 7    | `CONFIG_BOARDCTL_UNIQUEKEY`                        | 是       | `y`    |                                            |                          |
| 8    | `CONFIG_INTERPRETERS_WAMR`                         | 是       | `y`    | 配置 WAMR（WebAssembly Micro Runtime）环境 |                          |
| 9    | `CONFIG_INTERPRETERS_WAMR_AOT`                     | 是       | `y`    |                                            |                          |
| 10   | `CONFIG_INTERPRETERS_WAMR_BUILD_MODULES_FOR_NUTTX` | 是       | `y`    |                                            |                          |
| 11   | `CONFIG_INTERPRETERS_WAMR_LIBC_BUILTIN`            | 是       | `y`    |                                            |                          |
| 12   | `CONFIG_TA_COMSST`                                 | 否       | `y`<br>`n` | 安全存储功能 TA                            | 根据设备特性决定是否开启 |
| 13   | `CONFIG_TA_HELLO_WORLD`                            | 否       | `y`<br>`n` | Hello World 示例 TA                        |                          |
| 14   | `CONFIG_TA_PIN`                                    | 否       | `y`<br>`n` | PIN 码功能 TA                              |                          |
| 15   | `CONFIG_TA_TRIAD`                                  | 否       | `y`<br>`n` | 三元组功能 TA                              |                          |

## 五、AP 核配置

| 序号 | 配置项                   | 是否必选 | 默认值 | 功能描述                               |
| :--- | :----------------------- | :------- | :----- | :------------------------------------- |
| 1    | `CONFIG_LIB_TEEC`        | 是       | `y`    | AP 侧 CA 通过 Client API 与 TEE 侧交互 |
| 2    | `CONFIG_DEV_OPTEE_RPMSG` | 是       | `y`    | 设备驱动实现跨核通信 RPMSG             |
| 3    | `CA_COMSST_API`          | 否       | `y`<br>`n` | 安全存储功能 CA 的 API                 |
| 4    | `CA_HELLO_WORLD`         | 否       | `y`<br>`n` | Hello World 示例 CA 的 API             |
| 5    | `CA_PIN_API`             | 否       | `y`<br>`n` | PIN 码功能 CA 的 API                   |
| 6    | `CA_TRIAD_API`           | 否       | `y`<br>`n` | 三元组功能 CA 的 API                   |

## 六、QEMU/SIM 模拟平台配置

在 QEMU (Quick Emulator) / SIM 模拟平台上，无需使用独立的 TEE 核来提供安全环境。可以通过模拟运行，将 TEE 核的功能整合为一个独立的 AP 服务进程。为实现此目标，需要完成以下调整：

1. 通信方式调整：将跨核通信方式从 RPMsg 修改为 LOCAL SOCKET 通信，以简化通信逻辑并适配模拟平台。
2. 配置迁移：将所有 TEE 核的相关配置迁移至 AP 核，集中实现系统的功能逻辑。

| 序号 | 配置项                                             | 是否必选 | 默认值 | 功能描述                                   |
| :--- | :------------------------------------------------- | :------- | :----- | :----------------------------------------- |
| 1    | `CONFIG_OPTEE_OS`                                  | 是       | `y`    | TEE OS 框架的基础配置                      |
| 2    | `CONFIG_OPTEE_SERVER_LOCAL`                        | 是       | `y`    | 支持模拟器中 TEE 核与 AP 核的通信          |
| 3    | `CONFIG_DEV_OPTEE_LOCAL`                           | 是       | `y`    |                                            |
| 4    | `CONFIG_BOARDCTL_UNIQUEID`                         | 是       | `y`    | 需要硬件厂商提供 Hardware Unique Key 适配  |
| 5    | `CONFIG_BOARDCTL_UNIQUEKEY`                        | 是       | `y`    |                                            |
| 6    | `CONFIG_INTERPRETERS_WAMR`                         | 是       | `y`    | 配置 WAMR（WebAssembly Micro Runtime）环境 |
| 7    | `CONFIG_INTERPRETERS_WAMR_AOT`                     | 是       | `y`    |                                            |
| 8    | `CONFIG_INTERPRETERS_WAMR_BUILD_MODULES_FOR_NUTTX` | 是       | `y`    |                                            |
| 9    | `CONFIG_INTERPRETERS_WAMR_LIBC_BUILTIN`            | 是       | `y`    |                                            |