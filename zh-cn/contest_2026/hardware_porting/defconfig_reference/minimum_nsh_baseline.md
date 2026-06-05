# 最小可运行 NSH 系统 defconfig 参考

\[ [English](../../../../en/contest_2026/hardware_porting/defconfig_reference/minimum_nsh_baseline.md) | 简体中文 \]

本文档面向「新硬件适配赛道」的开发者，目标是帮助开发者在自己的开发板上**先启动到 NSH 命令行提示符**。建议的工作流是：先以本文给出的最小集启动，验证串口与 NSH 工作正常后，再按需逐步打开文件系统、网络、传感器等子系统。

## 一、概述

### 1、文档目标

参赛者拿到一块尚未适配 openvela 的开发板后，最关键的第一步是让系统能启动到 NSH 命令行提示符。本文档提供一份**最小**的 defconfig 参考，仅包含启动 NSH 所必需的配置项，便于参赛者：

- 快速判断哪些 CONFIG **必须修改**（与目标硬件强相关）；
- 哪些 CONFIG **可直接复用**（与硬件无关的运行时支持）；
- 完成 L0 启动后，按子系统顺序**增量启用**功能。

### 2、推荐工作流

```
Step 0: 硬件就绪
        - 目标芯片在 nuttx/arch/<arch>/src/<chip>/ 下已有支持
        - 板级目录已建立 (boards/<arch>/<chip>/<board>/)
        - 串口 TX/RX 引脚与上位机连通
        ↓
Step 1: 套用本文最小集 → 编译 → 烧录 → 串口看到 NSH 提示符
        ↓
Step 2: 按硬件能力增量启用子系统
        - 文件系统 (FAT / LittleFS)
        - 网络协议栈 (Ethernet / Wi-Fi)
        - 图形 (LCD / framebuffer / LVGL)
        - 传感 (uORB / I2C / SPI sensors)
        ↓
Step 3: 移植稳定后做 release 瘦身
        - 关闭 DEBUG_*、ALLSYMS 等调试项
        - 调整 stack size 至实测需求
```

## 二、最小 NSH 必需配置

本节配置项参考 `nuttx/boards/arm/stm32/nucleo-f303re/configs/nsh/defconfig`（35 行）整理而来，并参考了 Mateusz Szafoni 的 [NuttX small systems 系列文章](https://www.railab.me/tags/small-systems/) 对最小化裁剪的实践经验。

### 1、架构与板级标识（必须按目标硬件替换）

```
CONFIG_ARCH="arm"
CONFIG_ARCH_CHIP="stm32"
CONFIG_ARCH_CHIP_STM32=y
CONFIG_ARCH_CHIP_STM32F303RE=y
CONFIG_ARCH_BOARD="nucleo-f303re"
CONFIG_ARCH_BOARD_NUCLEO_F303RE=y
```

#### 替换原则

| 配置项 | 替换原则 |
| ---- | ---- |
| `CONFIG_ARCH=` | 目标 CPU 架构，例如 `"arm"`、`"arm64"`、`"risc-v"`、`"xtensa"` |
| `CONFIG_ARCH_CHIP=` 与 `CONFIG_ARCH_CHIP_<FAMILY>=y` | 目标 SoC 家族，需与 `nuttx/arch/<arch>/src/<chip>/` 目录一致（如 `stm32`、`stm32h7`、`nrf52`、`esp32s3`） |
| `CONFIG_ARCH_CHIP_<DEVICE>=y` | 具体型号，例如 `STM32F407VG`、`NRF52840`、`ESP32S3` |
| `CONFIG_ARCH_BOARD=` 与 `CONFIG_ARCH_BOARD_<NAME>=y` | 板级目录名，需与 `nuttx/boards/<arch>/<chip>/<board>/` 一致 |

### 2、内存布局（必须按目标硬件填写）

```
CONFIG_RAM_START=0x20000000
CONFIG_RAM_SIZE=65536
CONFIG_MM_REGIONS=2
CONFIG_BOARD_LOOPSPERMSEC=6522
```

#### 配置项说明

- `CONFIG_RAM_START`：主 SRAM 起始物理地址，参考目标芯片 datasheet（多数 ARM Cortex-M 为 `0x20000000`）。
- `CONFIG_RAM_SIZE`：主 SRAM 容量，单位字节。
- `CONFIG_MM_REGIONS`：堆管理器管理的内存区域数量。当芯片存在多块不连续 SRAM（如 STM32F4 的 CCM、STM32H7 的 AXI/AHB SRAM）时需调整为对应数量。
- `CONFIG_BOARD_LOOPSPERMSEC`：忙等延时校准值，与 CPU 频率相关，可先填一个估算值，启动后通过 `up_mdelay()` 校准。

### 3、串口控制台（必须按目标硬件替换）

```
CONFIG_STM32_USART2=y
CONFIG_USART2_SERIAL_CONSOLE=y
CONFIG_STM32_JTAG_SW_ENABLE=y
```

#### 替换原则

| 配置项 | 替换原则 |
| ---- | ---- |
| `CONFIG_<CHIP>_USART<N>=y` | 启用目标芯片对应 UART 外设。STM32 用 `STM32_USARTx`，nRF52 用 `NRF52_UART0`，ESP32 用 `ESP32_UART0` |
| `CONFIG_USART<N>_SERIAL_CONSOLE=y` | 指定该 UART 作为系统控制台 |
| `CONFIG_<CHIP>_JTAG_SW_ENABLE=y` | 视目标芯片可选，用于保留 SWD 调试口 |

参赛者可参考 `nuttx/boards/<arch>/<chip>/<board>/include/board.h` 中的引脚定义，确认串口对应的物理 TX/RX 引脚与电路板设计一致。

### 4、NSH Shell 启动入口（直接复用）

```
CONFIG_SYSTEM_NSH=y
CONFIG_INIT_ENTRYPOINT="nsh_main"
```

#### 配置项说明

- `CONFIG_SYSTEM_NSH=y`：将 NSH 编译为系统应用。
- `CONFIG_INIT_ENTRYPOINT="nsh_main"`：将 NSH 设为系统启动后的首个用户态任务，串口接通后即进入命令行提示符。

### 5、调度与运行时支持（直接复用）

```
CONFIG_RR_INTERVAL=200
CONFIG_SCHED_WAITPID=y
CONFIG_PREALLOC_TIMERS=4
CONFIG_IDLETHREAD_STACKSIZE=2048
CONFIG_TASK_NAME_SIZE=0
CONFIG_START_DAY=27
CONFIG_START_YEAR=2013
```

#### 配置项说明

- `CONFIG_RR_INTERVAL=200`：轮转调度时间片为 200 ms。
- `CONFIG_SCHED_WAITPID=y`：启用 `waitpid()` 系统调用，NSH 在执行内置命令时依赖此特性。
- `CONFIG_PREALLOC_TIMERS=4`：预分配 4 个 POSIX 定时器，满足基础需求。
- `CONFIG_IDLETHREAD_STACKSIZE=2048`：idle 线程栈大小，2 KB 适用于多数 Cortex-M 板。RAM 紧张时可下调至 1024。
- `CONFIG_TASK_NAME_SIZE=0`：禁用任务名称字符串以节省 RAM。如需 `ps` 命令显示任务名，可设为 16~32。
- `CONFIG_START_DAY` 与 `CONFIG_START_YEAR`：系统启动时的初始日期，可任意填写。

### 6、调试与诊断（强烈建议保留）

```
CONFIG_DEBUG_SYMBOLS=y
CONFIG_ARCH_STACKDUMP=y
CONFIG_INTELHEX_BINARY=y
CONFIG_RAW_BINARY=y
```

#### 配置项说明

- `CONFIG_DEBUG_SYMBOLS=y`：保留调试符号，便于使用 GDB 单步调试与 backtrace 分析。
- `CONFIG_ARCH_STACKDUMP=y`：系统出现 hardfault 时输出栈内容，移植阶段是定位问题的重要手段。
- `CONFIG_INTELHEX_BINARY=y` 与 `CONFIG_RAW_BINARY=y`：编译后同时产出 `.hex` 与 `.bin` 两种烧录格式。

### 7、CPU 特性裁剪（按需调整）

```
# CONFIG_ARCH_FPU is not set
```

#### 说明

`CONFIG_ARCH_FPU` 控制硬件浮点单元的启用。Cortex-M4F、M7 等带 FPU 的内核如需使用浮点运算，应改为 `CONFIG_ARCH_FPU=y`。Cortex-M0/M3 无 FPU，保持注释状态即可。

### 8、板级辅助（可选）

```
CONFIG_ARCH_BUTTONS=y
```

#### 说明

`CONFIG_ARCH_BUTTONS=y`：当板上存在 USER 按钮时启用按钮驱动框架。如目标板无按键，可省略。

## 三、可直接复用的 defconfig 片段

下列 16 项配置与硬件无关，可在任何 ARM Cortex-M 板上原样使用：

```
CONFIG_RR_INTERVAL=200
CONFIG_SCHED_WAITPID=y
CONFIG_PREALLOC_TIMERS=4
CONFIG_IDLETHREAD_STACKSIZE=2048
CONFIG_TASK_NAME_SIZE=0
CONFIG_START_DAY=27
CONFIG_START_YEAR=2013
CONFIG_SYSTEM_NSH=y
CONFIG_INIT_ENTRYPOINT="nsh_main"
CONFIG_DEBUG_SYMBOLS=y
CONFIG_ARCH_STACKDUMP=y
CONFIG_INTELHEX_BINARY=y
CONFIG_RAW_BINARY=y
```

参赛者只需根据自己的硬件填写第二节中标注「必须按目标硬件替换」的部分（架构标识、内存布局、串口配置），即可形成完整的 L0 defconfig。

## 四、参考实现

### 1、Nucleo-F303RE（参考板）

完整 defconfig 路径：

```
nuttx/boards/arm/stm32/nucleo-f303re/configs/nsh/defconfig
```

该板搭载 STM32F303RE（Cortex-M4F @ 72 MHz, 512 KB Flash, 64 KB SRAM），板载 ST-Link/V2-1 调试器与 USB 虚拟串口，参赛者只需一根 USB 线即可完成烧录与串口连接，是验证最小 NSH 流程最便捷的硬件参考。

### 2、其他可参考的最小 NSH defconfig

| 参考板 | 路径 | 行数 | 适用场景 |
| ---- | ---- | ---- | ---- |
| Nucleo-F303RE | `nuttx/boards/arm/stm32/nucleo-f303re/configs/nsh/defconfig` | 35 | ARM Cortex-M4F 主流参考 |
| nRF52840-DK | `nuttx/boards/arm/nrf52/nrf52840-dk/configs/nsh/defconfig` | 41 | Nordic nRF52 系列参考 |
| STM32F411-Minimum | `nuttx/boards/arm/stm32/stm32f411-minimum/configs/nsh/defconfig` | 46 | STM32F4 资源紧张场景 |
| STM32F4Discovery | `nuttx/boards/arm/stm32/stm32f4discovery/configs/nsh/defconfig` | 50 | STM32F4 经典评估板（含部分扩展项） |

## 五、增量启用子系统

L0 启动成功（串口看到 NSH 提示符）后，可按目标板的硬件能力逐步启用子系统。各类子系统的常用 CONFIG 起点如下：

| 子系统 | 主要 CONFIG 起点 |
| ---- | ---- |
| 文件系统（FAT、LittleFS、PROCFS） | `CONFIG_FS_FAT`、`CONFIG_FS_LITTLEFS`、`CONFIG_FS_PROCFS` |
| 网络协议栈（TCP/IP、Wi-Fi） | `CONFIG_NET`、`CONFIG_NET_TCP`、`CONFIG_NET_UDP` |
| 图形与显示（fb、LCD、LVGL） | `CONFIG_VIDEO_FB`、`CONFIG_GRAPHICS_LVGL` |
| 传感与 uORB | `CONFIG_SENSORS`、`CONFIG_UORB` |
| 蓝牙（BLE） | `CONFIG_BLUETOOTH`、`CONFIG_NIMBLE` |
| 音频 | `CONFIG_AUDIO` |
| 电源管理 | `CONFIG_PM` |

参赛者也可参考 `vendor/openvela/boards/vela/configs/goldfish-x86_64-ap/defconfig`（253 行）了解 openvela 在子系统全开场景下的完整 CONFIG 集合，作为增量启用时的对照样本。

## 六、功能验证

子系统启用后，建议通过标准化测试用例验证目标硬件上各子系统的功能完整性。openvela 社区维护了一份面向社区开发者的 xTS 测试用例精简集，覆盖了外设驱动、文件系统、网络、媒体等多个子系统，可作为子系统启用后的功能验收手段。

### 1、推荐使用方式

- **L0 启动验证**：参赛者按本文最小集完成 NSH 启动后，通过串口手动输入命令（如 `help`、`uname`、`ps`）验证基础 shell 与系统调用工作正常。
- **子系统功能验证**：每启用一个子系统后，从 xTS 测试集中选取该子系统对应的用例运行（如启用 SPI/I2C 驱动后跑 SPI_I2C 测试）。
- **回归验证**：移植稳定后，将整套 xTS 用例作为回归测试集，便于后续配置变更后的功能确认。

### 2、xTS 测试集覆盖范围

| 测试主题 | 适用场景 |
| ---- | ---- |
| SPI / I2C 驱动 | 外设驱动启用后验证总线通信（含 BMI160 传感器示例） |
| Ymodem 文件传输 | 串口文件传输能力验证 |
| mediatool 媒体测试 | 音视频编解码与播放链路验证 |
| WiFi 兼容性 | 已适配路由器列表与连接稳定性验证 |
| 自测试框架（cmocka） | 编写自定义单元测试时的框架使用方法 |

详细的测试步骤、测试资源与依赖配置请参考 [openvela 社区开发者 xTS 测试用例精简集](../../../test_dev_guide/openvela_xts_test_cases.md) 与 [openvela 自测试框架使用指南](../../../test_dev_guide/openvela_testcase_dev_guide.md)。

## 七、新硬件适配 Checklist

参赛者完成 BSP 移植后，建议按以下清单检查 defconfig 完整性与目标硬件兼容性：

- [ ] `CONFIG_ARCH`、`CONFIG_ARCH_CHIP`、`CONFIG_ARCH_BOARD` 三项已替换为目标硬件标识
- [ ] `CONFIG_RAM_START` 与 `CONFIG_RAM_SIZE` 已按目标芯片 datasheet 填写
- [ ] 多 SRAM 区芯片（如 STM32F4 含 CCM）已正确设置 `CONFIG_MM_REGIONS`
- [ ] 串口外设宏（如 `CONFIG_STM32_USART2=y`）已切换至目标芯片对应 UART
- [ ] `CONFIG_USART<N>_SERIAL_CONSOLE=y` 与 `board.h` 中的引脚定义一致
- [ ] 串口波特率默认为 115200，与上位机终端一致
- [ ] `CONFIG_SYSTEM_NSH=y` 与 `CONFIG_INIT_ENTRYPOINT="nsh_main"` 已启用
- [ ] `CONFIG_DEBUG_SYMBOLS=y` 与 `CONFIG_ARCH_STACKDUMP=y` 已启用，便于排查启动问题
- [ ] 带 FPU 的内核（M4F/M7）已启用 `CONFIG_ARCH_FPU=y`，无 FPU 的内核（M0/M3）保持关闭
- [ ] `CONFIG_BOARD_LOOPSPERMSEC` 已根据 CPU 频率设置初始估算值

通过 Checklist 后即可执行 `./build.sh <vendor>:<config> -j` 编译。烧录后，串口接通并出现 `nsh> ` 提示符即代表 L0 启动成功。

## 八、参考资料

### 1、openvela 内部参考

| 资源 | 说明 |
| ---- | ---- |
| `nuttx/boards/arm/stm32/nucleo-f303re/configs/nsh/defconfig` | 推荐 L0 参考 defconfig（35 行） |
| `nuttx/boards/arm/stm32/nucleo-f303re/include/board.h` | 板级时钟与引脚定义参考 |
| `nuttx/boards/arm/nrf52/nrf52840-dk/configs/nsh/defconfig` | nRF52 平台最小 NSH 参考 |
| `nuttx/boards/sim/sim/sim/configs/nsh/defconfig` | 工具链自检参考 |
| `vendor/openvela/boards/vela/configs/goldfish-x86_64-ap/defconfig` | 子系统全开示例（253 行），增量启用时的对照样本 |
| [openvela 芯片移植指南](../../../chip_porting/porting_guide.md) | 从零完成 BSP 移植的完整流程 |
| [新硬件适配赛道详细指引](../hardware_porting_track_guide.md) | 赛道说明、评分维度与参考资源 |
| [Kconfig 使用指南](../../../device_dev_guide/build/Kconfig.md) | menuconfig、defconfig、.config 三者关系详解 |
| [openvela 社区开发者 xTS 测试用例精简集](../../../test_dev_guide/openvela_xts_test_cases.md) | 子系统启用后的功能验证用例集（覆盖外设、文件系统、网络、媒体等） |
| [openvela 自测试框架使用指南](../../../test_dev_guide/openvela_testcase_dev_guide.md) | 测试框架（cmocka 等）的搭建与使用方法 |

### 2、外部参考资料

Mateusz Szafoni（[@raiden00pl](https://github.com/raiden00pl)）撰写的 NuttX small systems 系列博客，深入探讨了 NuttX 在资源受限 MCU 上的最小化配置实践，对 L0 后续的资源裁剪与子系统增量启用具有重要参考价值：

| 文章 | 主题 |
| ---- | ---- |
| [Apache NuttX and small systems - Hello, World !](https://www.railab.me/posts/2024/11/nuttx-and-small-systems-hello-world/) | 在小型 MCU 上启动最小 NuttX 系统 |
| [Apache NuttX and small systems - NuttX Core Size](https://www.railab.me/posts/2024/12/nuttx-and-small-systems-core-os/) | NuttX 内核体积分析与 Flash/RAM 占用 |
| [Apache NuttX and small systems - OS components](https://www.railab.me/posts/2025/1/nuttx-and-small-systems-os-components/) | 各 OS 组件的开关与资源代价 |
| [Apache NuttX and small systems - CAN node example](https://www.railab.me/posts/2025/2/nuttx-and-small-systems-can-node-example/) | 基于 STM32 的 CAN 节点最小实现 |
| [Apache NuttX and small systems - Modbus slave example](https://www.railab.me/posts/2025/3/nuttx-and-small-systems-modbus-slave-example/) | 64 KB Flash 内塞下 Modbus RTU Slave 应用 |
