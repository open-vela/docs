# RIL 适配指南

\[ [English](../../../../en/device_dev_guide/connection/telephony/ril_adaptation_guide.md) | 简体中文 \]

本指南详细阐述了 openvela 射频接口层（Radio Interface Layer, RIL）的架构，并为 Modem 厂商提供了在 openvela 系统中适配和集成其 `vendor-ril` 的完整流程与技术要求。

## 一、概述

openvela 射频接口层 (Radio Interface Layer, RIL) 是一套完整的 Telephony 功能解决方案，其设计深受 Android RIL 架构启发。它最初为 openvela QEMU 模拟器开发，现已推广至实体硬件产品。

本节介绍 openvela RIL 的核心架构、组件职责以及厂商适配的协作模式。

### 1、RIL 架构与组件

openvela RIL 架构由三个核心组件构成，它们协同工作，连接上层 Telephony 框架与底层 Modem 硬件。

- **`libril`**: 作为接口库，负责接收上层 Telephony 框架 (oFono) 的 Socket 请求，并将其转发给 `rild` 守护进程。其实现参考了 Android 7.0 版本。
- **`rild`**: 作为核心守护进程，充当 `libril` 和 `vendor-ril` 之间的桥梁。它管理两者间的通信链路，并将请求分发给 `vendor-ril` 处理。
- **`vendor-ril`**: 作为厂商特定的实现，直接与底层 Modem 硬件或 QEMU 模拟器 (`modem_simulator`) 交互，执行具体的通信操作。openvela 提供的参考实现 (`reference-ril`) 主要参照了 Android 13 的代码。

<img src="./figures/004.png" width="75%" height="100%">

### 2、协作模式与适配策略

为简化不同硬件平台的适配工作，openvela RIL 采用标准化与定制化分离的策略，明确了 openvela 与 Modem 芯片厂商的职责分工。

- **通用组件 (openvela 维护)**: openvela 负责维护和提供通用的 `libril` 库和 `rild` 守护进程。这些组件在所有搭载 openvela 的产品中保持一致，厂商无需修改。
- **定制模块 (****`vendor-ril`****) (Modem 厂商开发)**: Modem 芯片厂商仅需专注于开发和实现与其硬件相适配的 `vendor-ril`。这部分代码需要处理特定芯片的硬件接口、AT 命令集、通信协议和控制逻辑。

该协作模式通过标准化通用组件、分离定制化模块，旨在大幅降低 Modem 厂商的适配成本，加速其产品融入 openvela 生态系统。

## 二、代码库结构

### 1、代码目录简介

openvela RIL 的源代码位于 `external/ril` 仓库，其核心代码存放在 `external/ril/ril` 子目录中。

#### 代码库路径

```Bash
vela_source_code/external/ril
```

顶层的 `external/ril` 目录主要存放 RIL 项目的顶层编译配置文件，而实际的核心源代码则位于 `external/ril/ril` 子目录中。

#### 核心目录结构

```Bash
.
├── include         # RIL 公共头文件，定义核心数据结构和接口
├── libril          # 通用 libril 库实现，负责与上层框架通信
├── librilutils     # RIL 通用工具函数库
├── reference-ril   # QEMU 模拟器专用的参考实现 (厂商不应修改)
└── rild            # RIL 守护进程 (rild) 的主程序入口
```

### 2、`reference-ril` 的作用与模块化设计

`reference-ril` 目录提供了一个基于 AT 命令的 RIL 参考实现，其**核心目的仅在于作为示例**，用以展示 `vendor-ril` 的基础结构、接口规范以及与 `rild` 的交互逻辑。在当前代码库中，该实现专为 QEMU 模拟器 (`modem_simulator`) 环境定制。

> **注意：**
>
> `reference-ril` **绝非**设计用来存放厂商最终产品代码的位置。

为了提升代码的可读性和可维护性，`reference-ril` 将功能按模块拆分，主要包括：

- `at_call.c`: 通话 (Call) 相关 AT 命令处理
- `at_data.c`: 数据业务 (Data) 相关 AT 命令处理
- `at_modem.c`: Modem 控制相关 AT 命令处理
- `at_network.c`: 网络 (Network) 相关 AT 命令处理
- `at_sim.c`: SIM 卡相关 AT 命令处理
- `at_sms.c`: 短信 (SMS) 相关 AT 命令处理
- `at_ril.c`: RIL 请求分发与主逻辑
- `atchannel.c`: AT 命令收发通道管理

这种模块化设计通过 `on_request_*` 和 `try_handle_unsol_*` 等分发函数，将 RIL 请求和主动上报路由到相应的模块文件中处理。

> **开发建议：**
>
> Modem 厂商在开发自己的 `vendor-ril` 时，应遵循此模块化结构。这能确保代码逻辑清晰、职责分明，极大地便利后续的开发、调试与长期维护工作。

## 三、Vendor RIL 适配工作流

适配工作的核心是将厂商特定的 `vendor-ril` 正确集成到 openvela 构建系统中。请严格遵循以下步骤。

### 步骤 1：创建目录

> **注意**
>
> **严禁**以任何形式直接修改、删除或替换 `external/ril/ril/reference-ril` 目录内的任何内容。

建议您在芯片专属的 `vendor` 目录下创建一个新的 `vendor-ril` 目录，用于存放您的定制 RIL 代码。

#### 目录路径示例

```Bash
vendor/<厂商名称>/<芯片平台名称>/<vendor-ril>/
```

### 步骤 2：部署代码与编译脚本

将您开发的所有 `vendor-ril` 源代码文件复制到上一步创建的目录中。同时，在此目录内添加相应的构建系统配置文件（例如 Kconfig 或 `CMakeLists.txt`），以确保构建系统能够正确编译和链接您的代码。

#### 目录文件示例

```CMake
$ tree sample_vendor_ril/
sample_vendor_ril/
├── CMakeLists.txt
├── Kconfig
└── sample_vendor_ril
    ├── at_call.c
    ├── at_call.h
    ├── atchannel.c
    ├── atchannel.h
    ├── at_data.c
    ├── at_data.h
    ├── at_modem.c
    ├── at_modem.h
    ├── at_network.c
    ├── at_network.h
    ├── at_ril.c
    ├── at_ril.h
    ├── at_sim.c
    ├── at_sim.h
    ├── at_sms.c
    ├── at_sms.h
    ├── at_tok.c
    ├── at_tok.h
    ├── misc.c
    ├── misc.h
    ├── MODULE_LICENSE_APACHE2
    └── NOTICE

1 directory, 24 files
```

### 步骤 3：集成到 openvela 构建系统

您需要通过 `Kconfig` 和 `CMakeLists.txt` 将您的 `vendor-ril` 集成到系统构建流程中。构建系统将自动把通用的 `libril`、`rild` 与您的 `vendor-ril` 编译链接，最终生成一个适配目标硬件的 `rild` 守护进程。

#### 3.1 停用模拟器 RIL

首先，通过 Kconfig 配置系统，**禁用**默认的 QEMU 模拟器 RIL (`CONFIG_GOLDFISH_RIL`)。

#### 3.2 添加 Kconfig 选项

在您 `vendor` 目录的顶层，创建一个 `Kconfig` 文件，为您的 RIL 添加一个启用选项。

**Kconfig 示例 (`vendor/<厂商>/<平台>/Kconfig`)：**

```Makefile
#
# For a description of the syntax of this configuration file,
# see the file kconfig-language.txt in the NuttX tools repository.
#

config SAMPLE_VENDOR_RIL
        tristate "Enable SAMPLE_VENDOR_RIL"
        default n
        depends on RILD
        ---help---
                Enable sample vendor ril
```

#### 3.3 创建 `vendor-ril` 的 CMakeLists.txt

在您的 `vendor-ril` 目录中 (`vendor/<厂商>/<平台>/vendor-ril/`)，创建一个 `CMakeLists.txt` 文件来描述如何编译您的源代码。此 `CMakeLists.txt` 仅需关注 `vendor-ril` 自身的源文件。

**CMakeLists.txt 示例 (`vendor/<xxx>/<platform>/<sample_vendor_ril>/CMakeLists.txt`)：**

```CMake
#
# Copyright (C) 2021 Xiaomi Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

if(CONFIG_SAMPLE_VENDOR_RIL)
  set(SAMPLE_VENDOR_RIL_DIR ${CMAKE_CURRENT_LIST_DIR}/sample_vendor_ril)
  file(GLOB CSRCS ${SAMPLE_VENDOR_RIL_DIR}/*.c)
  set(INCDIR ${SAMPLE_VENDOR_RIL_DIR})
  set(CFLAGS -Wno-format)

  nuttx_add_library(sample_vendor_ril STATIC)

  target_compile_options(sample_vendor_ril PRIVATE ${CFLAGS})
  target_sources(sample_vendor_ril PRIVATE ${CSRCS})
  target_include_directories(sample_vendor_ril PRIVATE ${INCDIR})

endif()
```

## 四、开发注意事项与建议

### 1、关键注意事项

- **模拟器与真机的差异**: `reference-ril` 是为受限的 QEMU 模拟器环境设计的。在移植到实体硬件时，您必须考虑更复杂的真实场景，例如更全面的错误处理、信号强度动态变化、网络切换逻辑等。
- **移除模拟器专用代码**: `reference-ril` 中包含一些模拟器特有的代码（例如 `ENABLE_MODEM` 宏）。在适配您的硬件时，您必须识别并移除这些代码。
- **健壮的状态管理**: `reference-ril` 为简化实现，使用了一些全局变量来保存状态。在实体产品中，这种做法可能导致竞态条件和系统不稳定。我们强烈建议您在 `vendor-ril` 中采用更健壮的状态管理机制（例如基于上下文的结构体）。

### 2、开发建议

- **限制修改范围**: 请将您的代码修改严格限制在自己的 `vendor-ril` 目录内。`libril` 和 `rild` 是跨平台共享的通用组件。如果必须修改通用代码，请创建 Patch 并提交给开发人员进行评估和合入。
- **完善硬件特定功能**: `reference-ril` 中的某些功能是为模拟器模拟的（如 `enable modem`）。您需要根据实际硬件的行为，在 `vendor-ril` 中实现这些功能的完整逻辑。
- **适配设备节点**: `reference-ril` 打开的设备节点是 `/dev/ttyV0`，这是 Goldfish 模拟器提供的虚拟串口。您必须将其修改为您的 Modem 硬件在系统中的实际设备节点（例如 `/dev/ttyS1` 或 `/dev/ttyUSB0`）。

## 五、接口要求

您的 `vendor-ril` 实现必须遵循 openvela Telephony 的接口规范。

- **请求分类**: RIL 请求分为 **必选** 和 **可选** 两类。您的实现**必须**支持所有必选请求，**建议**支持可选请求。
- **文档优先原则**: 如果 `reference-ril` 的实现与接口文档存在差异，**请始终以接口文档为准**。

    - 例如，`reference-ril` 的 `at_network.c` 中 `requestSetPreferredNetworkType` 函数可能沿用了 Android 原生实现，而未遵循文档要求的 `RIL_PreferredNetworkType` 枚举。在这种情况下，您应参考文档进行正确开发。

## 六、RIL 适配准入测试

完成 `vendor-ril` 适配后，您可以使用 `RILTEST` 工具进行准入测试，以验证实现的正确性。

### 1、测试步骤

1. **关闭 oFono**: `RILTEST` 工具与 `oFono` 服务存在冲突，不能同时运行。请在 Kconfig 中**禁用** `CONFIG_OFONO` 选项。

2. **开启 RILTEST**: 在 Kconfig 中**启用** `CONFIG_RIL_TEST` 选项。

3. **重新编译系统**：执行完整的编译流程，生成包含 `RILTEST` 的固件并烧录至设备。

4. **推送测试脚本**: 将 [run_testcase.sh](./run_testcase.sh) 脚本通过 `adb` 推送到设备的数据分区。

    ```bash
    adb push run_testcase.sh /data/
    ```

5. **执行测试**: 通过 `adb shell` 登录设备并运行测试脚本。

    ```bash
    adb shell "sh /data/run_testcase.sh"
    ```

​    测试工具将自动执行一系列 RIL 命令并验证 Modem 的响应，帮助您快速定位和修复实现中的问题。
