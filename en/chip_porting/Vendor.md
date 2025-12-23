# Vendor Code Repository

\[ English | [简体中文](../../zh-cn/chip_porting/Vendor.md) \]

## I. Overview

To ensure the isolation and privacy security of vendor code, a dedicated directory named vendor is provided within the openvela codebase. This directory is intended to store the code for each vendor, with the directory name representing the vendor’s abbreviation as an identifier.

## II. Directory Structure

### 1. Top-Level Directory

Upon completing the code download, the overall directory structure is as follows:

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

seven directories, one file
```

- `nuttx` contains the core components, including the kernel, networking stack, and file system.
- `apps` includes sample applications, system services, and `nsh` (NuttShell Command-Line Interface).
- `external` stores third-party libraries supported by the openvela system, which are provided in source code form.
- `prebuilts` contains the toolchains required for compiling the code.
- `tests` holds the test suites released by openvela, covering tests for networking, file systems, and system calls, as well as API tests.
- `frameworks` provides the exported header files for the openvela framework, available in the form of .a library files.
- `build.sh` is a script file used for code compilation, allowing the generation of the nuttx.bin file through additional compilation parameters.

### 2. vendor Directory Structure

The vendor directory is used to store the relevant code and configurations for each vendor. The layout of its contents is as follows:

```Shell
$ tree -L 1
.
├── <vendor_name>
├── Make.defs
├── Makefile
├── sim
└── xiaomi

three directories, two files
```

- `vendor_name` is the root directory for storing the vendor's code, and all of the vendor's code should be placed here.
- `sim` contains the configuration and source code required to launch the openvela Simulator simulation environment.
- `xiaomi` stores the library files provided by Xiaomi, such as the Bluetooth bluelet and other related code libraries.

## III. Vendor Directory and Files

When a vendor initially acquires the code, the layout of the vendor_name directory is as follows:

```C
// Directory location
$ pwd
/home/{namepath}/workspace/velaos/vendor/<vendor_name>

// Directory layout
$ tree -l
├── boards
│   └── <chip_name>
│       └── <board_name>
│           ├── configs
│           │   └── nsh
│           │       └── defconfig
│           ├── include
│           │   ├── board.h
│           │   └── nsh_romfsimg.h
│           ├── Kconfig
│           ├── scripts
│           │   ├── ld.script
│           │   └── Make.defs
│           └── src
│               ├── board_name.h
│               ├── etc
│               │   ├── group
│               │   ├── init.d
│               │   │   ├── rcS
│               │   │   └── rc.sysinit
│               │   └── passwd
│               ├── Makefile
│               ├── <vendor_name>_appinit.c
│               ├── <vendor_name>_boot.c
│               └── <vendor_name>_bringup.c
├── chips
│   └── chip_name
│       ├── chip.h
│       ├── include
│       │   ├── chip.h
│       │   └── irq.h
│       ├── Kconfig
│       ├── Make.defs
│       ├── vendor_name_irq.c
│       ├── vendor_name_irq.h
│       ├── vendor_name_lowputc.c
│       ├── vendor_name_lowputc.h
│       ├── vendor_name_start.c
│       ├── vendor_name_start.h
│       └── vendor_name_timeisr.c
```

### 1. `boards` Directory

`boards` :The directory primarily stores all code related to board-level hardware. The code for each board is organized under the path `boards/<chip_name>/<board_name>`.

- `chip_name`：chip_name。
- `board_name`：board_name。

#### `boards/<chip_name>/<board_name>` Directory

- `configs`  stores all configuration files for the board. By default, it includes the configuration for `nsh` (NuttShell CLI), which provides basic operating system functionality. Vendors can use the `nsh` configuration to initialize `openvela` and gradually add more features.

- `include` contains header files related to the board:
    - `board.h`：Declares macros and functions applicable to the board. Vendors can modify this as needed.
    - `nsh_romfsimg.h`：Provides the ROM file system image (romfs bin) for system files, which does not require modification by the vendor.

- `Kconfig`  defines board-related configuration options, including feature switches and peripheral selections, which vendors need to adjust according to actual requirements.

- `scripts` contains scripts and configuration files related to the build process:
    - `ld.script`：The board’s linker script.
    - `Make.defs`：Defines the compilation process and file rules, which vendors must modify according to requirements.

- `src` includes source code and configuration files related to board-level startup and initialization.
    - `etc`：
        - Contains startup scripts for the operating system and applications:
            - `rc.sysinit`：Core application startup and file system mounting.
            - `rcS`： Application startup script.
        - System account files:
            - `group` and `passwd`：Default example files are provided. Vendors need to redefine these for actual use.
    - `<vendor_name>_*.c` files： Include necessary board-level startup code, such as peripheral initialization files (`vendor_name_appinit.c`, `vendor_name_boot.c`, etc.), used to initialize peripherals and board-level configurations. Vendors can extend these files as needed.
    - `Makefile`：Used to build the source files for compilation and add target files from the `etc`directory.

### 2. `chips` Directory

The `chips` directory stores code related to chip startup and internal components (such as UART drivers, DMA drivers). The code for each chip is organized under the path `chips/<chip_name>`.

#### `chips/<chip_name>` Subdirectory

- `include`  Chip-related header files:
    - `chip.h`：Contains common macro definitions and function declarations for the chip.
    - `irq.h`：Contains interrupt-related content.

- `Kconfig` Defines chip-related configuration options, including chip models, feature selections, and module configurations.

- `Make.defs` Defines the build process for the chip code and lists the C files involved in the compilation.

- `<vendor_name>_*.c` files： Contain the default implementation code required for chip startup, such as:
    - UART driver（`vendor_name_lowputc.c`）。
    - Interrupt handling（`vendor_name_irq.c` 和 `vendor_name_irq.h`）。
    - System startup code（`vendor_name_start.c` and `vendor_name_timeisr.c`）. Vendors can supplement additional module code based on chip and hardware requirements.