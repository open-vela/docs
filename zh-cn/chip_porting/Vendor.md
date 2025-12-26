# Vendor 代码仓说明

\[ [English](../../en/chip_porting/Vendor.md) | 简体中文 \]

## 一、概述

为了保障厂商代码的隔离和隐私安全，在 `openvela` 代码中，可以通过 `vendor` 目录为厂商代码创建独立的存放目录。具体的目录名称采用厂商的缩写作为标识。

## 二、目录结构

### 1、顶层目录

代码下载完成后，整体目录结构如下：

```Shell
$ tree -L 1
.
├── apps
├── build.sh -> nuttx/tools/build.sh
├── external
├── frameworks
├── nuttx
├── prebuilts
├── tests
└── <vendor>

7 directories, 1 file
```

- `nuttx` 包括内核、网络、文件系统等内容。
- `apps` 包括示例代码、系统服务、nsh（NuttShell CLI）等内容。
- `external` 存放 `openvela` 系统支持的第三方库，这些库以源码形式提供。
- `prebuilts` 包含代码编译所需要的工具链（toolchain）。
- `tests` 存放由 `openvela` 发布的测试集，覆盖网络、文件系统以及系统调用等 API 测试内容。
- `frameworks` 提供 `openvela` 框架的导出头文件，以 `.a` 库文件形式提供。
- `build.sh` 用于代码编译的脚本文件，可通过附加编译参数生成 `nuttx.bin` 文件。

### `2、vendor` 目录结构

`vendor` 目录用于存放厂商的相关代码和配置。其目录内容布局如下：

```Shell
$ tree -L 1
.
├── <vendor_name>
├── Make.defs
├── Makefile
├── sim
└── xiaomi

3 directories, 2 files
```

- `vendor_name` 厂商代码存放的根目录，厂商的所有代码均应存放于此处。
- `sim` 包含启动 `openvela Simulator` 仿真环境所需的配置和源码。
- `xiaomi` 存放小米（Xiaomi）提供的库文件，例如蓝牙 `bluelet` 等相关代码库。

## 三、Vendor 目录和文件

厂商初次获取代码时，`vendor_name` 目录的布局如下：

```C
//目录位置
$ pwd
/home/{name_path}/workspace/velaos/vendor/<vendor_name>

//目录layout
$ tree -l
├── boards
│   └── <chip_name>
│       └── <board_name>
│           ├── configs
│           │   └── nsh
│           │       └── defconfig
│           ├── include
│           │   ├── board.h
│           │   └── nsh_romfsimg.h
│           ├── Kconfig
│           ├── scripts
│           │   ├── ld.script
│           │   └── Make.defs
│           └── src
│               ├── board_name.h
│               ├── etc
│               │   ├── group
│               │   ├── init.d
│               │   │   ├── rcS
│               │   │   └── rc.sysinit
│               │   └── passwd
│               ├── Makefile
│               ├── <vendor_name>_appinit.c
│               ├── <vendor_name>_boot.c
│               └── <vendor_name>_bringup.c
├── chips
│   └── <chip_name>
│       ├── chip.h
│       ├── include
│       │   ├── chip.h
│       │   └── irq.h
│       ├── Kconfig
│       ├── Make.defs
│       ├── <vendor_name>_irq.c
│       ├── <vendor_name>_irq.h
│       ├── <vendor_name>_lowputc.c
│       ├── <vendor_name>_lowputc.h
│       ├── <vendor_name>_start.c
│       ├── <vendor_name>_start.h
│       └── <vendor_name>_timeisr.c
```

### 1、`boards` 目录

`boards` 目录主要存放和板级硬件相关的所有代码。 每块板的代码组织在 `boards/<chip_name>/<board_name>` 路径下，其中：

- `chip_name`：芯片名称。
- `board_name`：板的名称。

#### `boards/<chip_name>/<board_name>` 目录

- `configs` 存放该板的所有配置文件。默认包含 `nsh`（NuttShell CLI）的配置，提供基础操作系统功能。厂商可基于 `nsh` 配置点亮 `openvela`，并逐步添加更多功能。
- `include` 包含与板相关的头文件：
    - `board.h`：声明适用于该板的宏和函数，厂商可根据需求修改。
    - `nsh_romfsimg.h`：提供系统文件的 ROM 文件系统镜像（romfs bin），无需厂商修改。
- `Kconfig` 定义与板相关的配置项，包括功能开关和外设选择，厂商需要根据实际需求调整。
- `scripts` 包含与构建流程相关的脚本和配置文件：
    - `ld.script`：板的链接脚本。
    - `Make.defs`：定义编译流程和文件规则，需厂商根据要求修改。
- `src` 包括板级启动和初始化相关的源代码和配置文件。
    - `etc`：
        - 保存操作系统和应用的启动脚本：
            - `rc.sysinit`：核心应用启动和文件系统挂载。
            - `rcS`：应用程序启动脚本。
        - 系统账户文件：
            - `group` 和 `passwd`：默认提供示例文件，实际使用时厂商需重新定义。
    - `<vendor_name>_*.c` 文件： 包括必要的板级启动代码，如外设初始化文件（`vendor_name_appinit.c`、`vendor_name_boot.c` 等），用于初始化外设和板级配置，厂商可根据需求扩展这些文件。
    - `Makefile`：用于构建编译的源文件以及加入 `etc` 目录的目标文件。

### 2. `chips` 目录

`chips` 目录存放与芯片启动及内部组件（如 UART 驱动、DMA 驱动）相关的代码。 每颗芯片代码组织在 `chips/<chip_name>` 路径下。

#### `chips/<chip_name>` 子目录说明

- `include` 芯片相关的头文件：
    - `chip.h`：存放芯片通用的宏定义和函数声明。
    - `irq.h`：中断相关内容。
- `Kconfig` 定义与芯片相关的配置项，包括芯片型号、功能选择和模块配置。
- `Make.defs` 定义芯片代码的构建流程，列出参与编译的 C 文件。
- `<vendor_name>_*.c` 文件： 包含芯片启动所需的默认实现代码，例如：
    - UART 驱动（`vendor_name_lowputc.c`）。
    - 中断处理（`vendor_name_irq.c` 和 `vendor_name_irq.h`）。
    - 系统启动代码（`vendor_name_start.c` 和 `vendor_name_timeisr.c`）。 厂商可根据芯片和硬件需求补充其他模块代码。
