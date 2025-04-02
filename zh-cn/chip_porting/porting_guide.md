# openvela 硬件移植指南

## 一、概述

openvela 内核通过对硬件进行抽象分层设计，不仅提升了代码复用性，还使开发板的配置更加灵活。以下是 openvela 的硬件层次结构。

### 1、硬件层次结构

![img](./figures/001.svg)

- **Architecture（架构层）**：CPU 架构层，支持多种主流 CPU 架构，包括 ARMv7-M、ARMv7-A/R 和 RISC-V。
- **Chip/****SoC****（芯片层）**：System on Chip (SoC) 是片上系统体系结构，每个处理器架构均嵌入在 SoC 系统中。完整的 SoC 结构包括处理器架构及芯片特定的中断逻辑、时钟逻辑、通用 I/O 逻辑以及专用内部外设。例如，基于 ARMv7-M 处理器的 STM32 是典型的 SoC。
- **Board（板级层）**：SoC 与其他外设连接形成特定功能的电路板。例如，STM32F4 Discovery 电路板中包含 STM32F407 SoC。

### 2、硬件支持与移植指南

openvela 已支持多种评估板，具体信息可参阅 [openvela Supported Platforms](https://nuttx.apache.org/docs/latest/platforms/index.html#)。

如果需要将 openvela 移植到新的评估板上，需要依次完成以下三层的移植工作：

1. 架构层 (Architecture)
2. SoC 层 (Chip/SoC)
3. 板级层 (Board)

以下将以基于 RISC-V 架构的 `qemu-rv` 为例，详细说明移植流程。

## 二、Architecture 适配

> **说明**  本文不涉及新增Architecture的适配。

openvela 已支持大部分常用的 CPU 架构，用户可根据需求选择对应的 CPU 架构。

例如，在 qemu-rv 中需要选择 `CONFIG_ARCH_RISCV=y`。

以下是 openvela 当前支持的 Architecture 列表：

- **arch/arm**：包含通用的 ARM32 体系结构。
- **arch/arm64**：包含通用的 ARM64 体系结构。
- **arch/avr**：包含通用的 AVR 和 AVR32 体系结构。
- **arch/ceva**：包含 CEVA 体系结构。
- **arch/hc**：包含 HC M9S12 芯片体系结构。
- **arch/mips**：包含通用的 MIPS 体系结构。
- **arch/misoc**：包含 Misoc LM3 体系结构。
- **arch/or1k**：包含 OpenRISC mor1kx 体系结构。
- **arch/renesas**：包含各种 Renesas 体系结构，目前支持 M16C 和 SuperH-1 体系结构。
- **arch/risc-v**：包含 RISC-V 32/64 体系结构。
- **arch/sim**：用于在 x86 Linux 或 Cygwin 平台上进行 OpenVela OS 特性开发。
- **arch/sparc**：包含 SPARC 体系结构。
- **arch/x86**：包含 x86 32bit 体系结构。
- **arch/x86_64**：包含 x86 64bit 体系结构。
- **arch/xtensa**：包含 Xtensa LX6/7 体系结构。
- **arch/z16f**：包含 Zilog z16f 微处理器体系结构。
- **arch/z80**：包含 8bit ZiLOG 体系结构。

## 三、Chip适配

对于移植 openvela 已支持的体系结构，Chip 级别的适配主要工作是实现该 Chip 的启动文件和片内外设驱动。实现最小系统移植时，需要完成 **timer 驱动** 和 **serial 驱动** 的实现。

### 1、目录结构

Chip 级别的代码位于 `arch/<arch_name>` 目录下，主要由以下内容构成：

- `include/<chip_name>`：包含 Chip 特定的头文件，在编译时会链接为 `include/arch/chip` 目录。
- `src/<chip_name>`：包含 Chip 特定的启动文件和驱动程序，在编译时会链接为 `src/chip` 目录。
- `src/<chip_name>/Make.defs`：Makefile 的片段文件，指示 Chip 相关编译参数及参与编译的文件。
- `src/<chip_name>/Kconfig`：包含 Chip 相关的配置选项。

以下以 `qemu-rv` 为例说明其目录结构：

```Bash
nuttx/arch/risc-v/include/qemu-rv
            ├── chip.h
            └── irq.h

nuttx/arch/risc-v/src/qemu-rv
            ├── chip.h                   // 对外提供的接口定义
            ├── hardware
            │   ├── qemu_rv_clint.h      // CLINT寄存器地址定义
            │   ├── qemu_rv_memorymap.h  // 芯片内部的寄存器映射定义
            │   └── qemu_rv_plic.h       // PLIC寄存器地址定义
            ├── Kconfig                  // 芯片特性配置选项
            ├── Make.defs                // 用于提供芯片的编译参数及参与编译的文件
            ├── qemu_rv_allocateheap.c   // 提供heap分配相关的接口
            ├── qemu_rv_head.S           // 启动文件
            ├── qemu_rv_irq.c            // 初始化/开/关中断等接口的实现
            ├── qemu_rv_irq_dispatch.c   // 中断分发相关接口实现
            ├── qemu_rv_memorymap.h      // 提供idle线程栈的定义
            ├── qemu_rv_mm_init.c        // 提供MMU相关的配置接口
            ├── qemu_rv_mm_init.h
            ├── qemu_rv_pgalloc.c        // 提供页内存分配器
            ├── qemu_rv_start.c          // 提供芯片初始化接口
            └── qemu_rv_timerisr.c       // 提供系统定时器相关的接口
```

### 2、实现API

内核需要 Architecture 代码提供一组 API 来实现基本功能。Architecture 层已经实现了通用的 API，用户也可以根据需求自行实现这些接口以完成更高级的功能。例如，通过自定义实现 `up_idle()` 提供低功耗能力。对于未实现的 API，用户需要在 Chip 层中自行实现。因此，Chip 层需要实现的 API 主要包括以下内容：

- Architecture 层中未实现的 API。
- 启动接口。
- 片内外设初始化接口。

API 列表及详细信息可参考 [此链接](https://nuttx.apache.org/docs/latest/reference/os/arch.html)。

#### Chip 层 API 示例

以 `qemu-rv` 为例，Chip 级别提供的 API 包括以下内容：

- `__start`

    通常实现在 `xxx_head.S` 文件中，例如 `qemu_rv_head.S`。芯片上电后，程序通常从这里开始执行，完成进入 C 环境前的准备工作，例如设置栈指针、关闭不必要的中断等操作。
- `qemu_rv_start`
  
  C 级别的启动代码，由 `__start` 调用，负责完成 `.bss` 段、`.data` 段的初始化操作，并启动内核。

- `up_allocate_heap`

    为内核提供可用的堆（heap）区间，包括起始地址和大小信息。
- `riscv_dispatch_irq`
  
  中断派发逻辑，用于清理中断标志并完成与外设相关的中断派发操作。
- `up_irqinitialize`
  
  初始化中断系统，通常包括挂载中断服务函数和清理无效的中断标志。
- `up_disable_irq` / `up_enable_irq`
  
  根据指定的中断号，启用或禁用特定中断。
- `up_irq_enable`
  
  开启总中断。
- `riscv_serialinit`
  
  串口初始化，通常用于日志输出。
- `up_putc`
  
  打印单个字符。
- `up_timer_initialize`
  
  初始化系统定时器，用于提供周期性中断。

### 3、添加 Kconfig  配置

以 `qemu-rv` 为例，Chip 相关的配置选项如下所示：

```Makefile
if ARCH_CHIP_QEMU_RV
comment "QEMU RISC-V Options"

choice
    prompt "QEMU Chip Selection"
    default ARCH_CHIP_QEMU_RV32

config ARCH_CHIP_QEMU_RV32
    bool "QEMU RV32"
    select ARCH_RV32

config ARCH_CHIP_QEMU_RV64
    bool "QEMU RV64"
    select ARCH_RV64

endchoice

config ARCH_CHIP_QEMU_RV_ISA_M
    bool "Standard Extension for Integer Multiplication and Division"
    default n
    select ARCH_RV_ISA_M

config ARCH_CHIP_QEMU_RV_ISA_A
    bool "Standard Extension for Atomic Instructions"
    default n
    select ARCH_RV_ISA_A

config ARCH_CHIP_QEMU_RV_ISA_C
    bool "Standard Extension for Compressed Instructions"
    default n
    select ARCH_RV_ISA_C

endif
```

QEMU 支持完整的 RV32GC 和 RV64GC 指令集。为了方便利用 QEMU 评估 RISC-V 指令集的性能和密度表现，这些选项被设置为可配置项。在真实芯片上，可以不增加类似的配置项。

### 4、添加 Makefile 配置

以 `qemu-rv` 为例，`Make.defs` 文件通过 `include common/Make.defs` 引入 RISC-V 的公用源文件，然后在 `CHIP_CSRCS` 中加入本芯片相关的源文件：

```Makefile
include common/Make.defs

# Specify our HEAD assembly file.  This will be linked as
# the first object file, so it will appear at address 0
HEAD_ASRC = qemu_rv_head.S

# Specify our C code within this directory to be included
CHIP_CSRCS  = qemu_rv_start.c qemu_rv_irq_dispatch.c qemu_rv_irq.c
CHIP_CSRCS += qemu_rv_timerisr.c qemu_rv_allocateheap.c

ifeq ($(CONFIG_BUILD_KERNEL),y)
CHIP_CSRCS += qemu_rv_mm_init.c
endif

ifeq ($(CONFIG_MM_PGALLOC),y)
CHIP_CSRCS += qemu_rv_pgalloc.c
endif
```

## 四、Board 适配

### 1、目录结构

`/boards` 子目录包含每个开发板的自定义逻辑和板级配置数据，主要由以下内容构成：

- include：包含板级的头文件，在编译时会链接为 `include/arch/board` 目录。
- src：包含板级驱动程序，在编译时会链接为 `arch/<arch-name>/src/board` 目录。
- src/Makefile：板级驱动的 Makefile 文件，必须包含以下三个目标：`libext$(LIBEXT)`、`clean` 和 `distclean`。
- scripts：包含开发板的链接脚本。
- scripts/Make.defs：Makefile 的片段文件，包含编译工具的相关配置。
- configs/xxx/defconfig：类似于 Linux 的配置文件，指示开发板的配置。

以下以 `nuttx/boards/risc-v/qemu-rv` 为例，展示基于 `qemu-rv` 芯片的开发板目录结构及包含文件：

```Bash
nuttx/boards/risc-v/qemu-rv
                        └── rv-virt
                            ├── configs               # 该目录用于存放不同应用的配置文件
                            │   ├── knsh64
                            │   │   └── defconfig
                            │   ├── nsh
                            │   │   └── defconfig
                            │   ├── nsh64
                            │   │   └── defconfig
                            │   ├── smp
                            │   │   └── defconfig
                            │   └── smp64
                            │       └── defconfig
                            ├── include               # 该目录用于存放开发板对外导出的接口和定义
                            │   ├── board.h
                            │   ├── board_memorymap.h
                            │   └── nsh_romfsimg.h
                            ├── Kconfig               # 描述该开发板可用的配置项
                            ├── README.txt
                            ├── scripts               # 该目录用于存放该开发板的连接脚本和Makefile
                            │   ├── ld-kernel.script
                            │   ├── ld.script
                            │   └── Make.defs
                            └── src                   # 源码目录
                                ├── etc               # 该开发板需要用到的资源文件
                                │   └── init.d
                                │       └── rcS
                                ├── Makefile
                                └── qemu_rv_appinit.c
```

### 2、实现API

Board 的接口定义在头文件 `include/nuttx/board.h` 中，用户可根据具体需求使能并实现相应的 API。例如，`qemu-rv` 仅实现了 `board_app_initialize` 接口。

API 具体说明可参考 [APIs Exported by Board-Specific Logic to NuttX](https://nuttx.apache.org/docs/latest/reference/os/board.html) 和 [boardctl](https://nuttx.apache.org/docs/latest/reference/user/13_boardctl.html?highlight=boardctl#c.boardctl)。

### 3、添加 Makefile 和链接脚本

#### Makefile 配置

以 `qemu-rv` 为例，`Makefile` 文件指定了需要编译的板级源文件以及资源文件：

```Makefile
include $(TOPDIR)/Make.defs

RCSRCS = etc/init.d/rc.sysinit etc/init.d/rcS

CSRCS = qemu_rv_appinit.c

include $(TOPDIR)/boards/Board.mk
```

#### Make.defs 配置

`Make.defs` 文件指定了链接脚本以及编译相关配置：

```Makefile
include $(TOPDIR)/.config
include $(TOPDIR)/tools/Config.mk
include $(TOPDIR)/arch/risc-v/src/common/Toolchain.defs

ifeq ($(CONFIG_ARCH_CHIP_QEMU_RV),y)
ifeq ($(CONFIG_BUILD_KERNEL),y)
  LDSCRIPT = ld-kernel.script
else
  LDSCRIPT = ld.script
endif
endif

ARCHSCRIPT += $(BOARD_DIR)$(DELIM)scripts$(DELIM)$(LDSCRIPT)

ARCHCPUFLAGS += -mcmodel=medany
ARCHPICFLAGS = -fpic -msingle-pic-base

CFLAGS := $(ARCHCFLAGS) $(ARCHOPTIMIZATION) $(ARCHCPUFLAGS) $(ARCHINCLUDES) $(ARCHDEFINES) $(EXTRAFLAGS) -pipe
CPICFLAGS = $(ARCHPICFLAGS) $(CFLAGS)
CXXFLAGS := $(ARCHCXXFLAGS) $(ARCHOPTIMIZATION) $(ARCHCPUFLAGS) $(ARCHXXINCLUDES) $(ARCHDEFINES) $(EXTRAFLAGS) -pipe
CXXPICFLAGS = $(ARCHPICFLAGS) $(CXXFLAGS)
CPPFLAGS := $(ARCHINCLUDES) $(ARCHDEFINES) $(EXTRAFLAGS)
AFLAGS += $(CFLAGS) -D__ASSEMBLY__

# ELF module definitions

CELFFLAGS = $(CFLAGS)
CXXELFFLAGS = $(CXXFLAGS)

ifeq ($(CONFIG_ARCH_RV32),y)
  LDELFFLAGS = --oformat elf32-littleriscv
else
  LDELFFLAGS = --oformat elf64-littleriscv
endif

LDELFFLAGS += -r -e main
LDELFFLAGS += -T $(call CONVERT_PATH,$(TOPDIR)/binfmt/libelf/gnu-elf.ld)
```

### 4、添加 defconfig

在 `configs` 目录下新建 `config` 文件夹，并创建初始的 `defconfig` 文件。根据需求使能相应的配置。