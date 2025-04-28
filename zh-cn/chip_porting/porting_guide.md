# 新平台适配指南

## 一、本文目标

1. 了解 openvela 启动（bringup）流程。
2. 了解在 openvela 中如何适配新的芯片和板级设计。

## 二、概述

openvela 是一个支持多种硬件平台的嵌入式操作系统，具有模块化和高扩展性。通过分层架构设计，openvela 简化了从处理器架构、芯片层到板级平台的适配工作。本文档介绍 openvela 的系统架构、移植步骤及相关开发资源。

### 1、系统架构

openvela 的设计分为三层架构，分别是架构层（Architecture）、芯片层（Chip/SoC）和板级层（Board）。

![img](./figures/001.svg)

#### 架构层（Architecture）

架构层是系统的核心基础，定义了 CPU 架构，例如 ARMv7-M、ARMv7-A/R 和 RISC-V 等主流处理器架构。openvela 已支持多种 CPU 架构，通常无需进行修改或适配。

#### 芯片层（Chip/SoC）

芯片层（System on Chip，简称 SoC）基于具体的处理器架构进行扩展，包含芯片的特定逻辑设计，例如中断控制、时钟管理、通用 I/O 逻辑和专用外设模块。例如，采用 ARMv7-M 处理器架构的 STM32 是典型的 SoC。

#### 板级层（Board）

板级层在芯片的基础之上，连接外设以形成特定功能的开发板。例如，STM32F4 Discovery 开发板包含 STM32F407 SoC，同时集成了外部传感器和其他辅助电路板。板级层的适配通常包含 PIN 脚定义、板级驱动和硬件初始化逻辑。

在开发过程中，多个相似 SoC 或开发板可以共享公共部分代码，以提升开发效率和维护便捷性。

### 2、支持平台与移植说明

openvela 已支持多种主流开发板，可参考 [Supported Platforms](https://nuttx.apache.org/docs/latest/platforms/index.html#) 获取详细信息。

如果需要将 openvela 移植到一个新的开发板上，需完成以下适配工作：

1. 确保目标架构（Architecture）已被 openvela 支持。
2. 针对新开发板，完成以下层次的适配：

    - 芯片层（Chip/SoC）：增加目标芯片的支持，代码通常遵循 `nuttx/arch` 下的某种架构目录（如 armv8-m、risc-v、arm64 等）。
    - 板级层（Board）：完成与目标开发板相关的配置、链接脚本及驱动适配。  

完成适配流程后，可生成以下二进制产物，用于部署到目标硬件：

- **libarch.a**：架构层静态库。
- **libboards.a**：代码驱动静态库。
- **vela_nuttx.bin**：编译生成的最终运行二进制文件。

### 3、新平台移植流程

移植 openvela 时，需要完成以下操作：

1. 熟悉代码结构。 开发者需熟悉 [Vendor 代码仓](Vendor.md)的基本结构，`vendor` 目录支持通过 Git 仓库管理厂商定制化代码。目录命名通常以厂商名称命名，例如 [open-vela/vendor_template](../../../../open-vela/vendor_template) 为适配模板。
2. 配置 Kconfig 文件。

    - Kconfig：用于定义编译选项和模块依赖项。开发者需根据硬件模块和外设配置文件，确保所需功能已在 Kconfig 中启用。Kconfig 使用可参考[Kconfig 使用指南](../device_dev_guide/build/Kconfig.md)。

3. 编写 Makefile。

    - Makefile 使用工具链完成代码编译，需确保规则定义正确，并支持目标硬件平台。

4. 完成芯片层（Chip/SoC）与板级层（Board）代码适配。 根据 [open-vela/vendor_template](../../../../open-vela/vendor_template) 中的模板，适配芯片层和板级层代码。需要更新驱动文件、板级配置文件，以及完成硬件初始化逻辑。
5. 编译与测试。 编译并生成目标静态库和最终运行文件，测试所有功能是否工作正常。

### 4、编译方式与产物管理

开发者需关注以下内容：

- 所有定制代码存放在 `vendor` 目录中，不得修改核心代码，以便与 openvela 的主仓库保持兼容。
- 编译步骤生成的产物包括：
    - **libarch.a**：架构层代码库。
    - **libboards.a**：板级代码库。
    - **vela_nuttx.bin**：最终的二进制镜像，用于固件烧录。

### 5、示例流程图

以下为 openvela 新平台移植的流程图，直观展示了开发步骤及逻辑顺序：

![img](./figures/002.png)

下面以 `vendor` 目录下适配为例，所有 **vendor** 仓库的初始源代码为 [open-vela/vendor_template](../../../../open-vela/vendor_template)，该模板包含了 操作系统的基本代码结构，因此适配过程只需打开相应文件进行修改。

## 二、芯片层适配

芯片层适配是 openvela 框架中支持硬件平台的重要环节，主要完成基于操作系统的入口函数，涉及以下方面的实现与配置：

1. 启动入口函数：定义操作系统的初始加载逻辑。
2. 架构（Arch） API 实现：实现系统调用所需的基础架构接口。
3. 中断适配：配置中断处理函数及相关寄存器。
4. 串口驱动：实现串口输入输出，并进行串口驱动注册。
5. 定时器驱动：支持操作系统调度和时间相关功能。
6. 内存（堆区）初始化：配置动态内存分配所需的堆区。
7. Kconfig 和 Makefile 编写：管理配置选项和代码构建流程。

芯片层代码位于 `vendor/<vendor_name>/chips` 目录下，典型的目录结构如下所示：

```Shell
vendor/vendor_name/
├── chips
│   └── <chip_name>
│       ├── chip.h
│       ├── include
│       │   ├── chip.h
│       │   └── irq.h
│       ├── Kconfig
│       ├── Make.defs
│       ├── <vendor_name>_irq.c
│       ├── <vendor_name>_irq.h
│       ├── <vendor_name>_lowputc.c
│       ├── <vendor_name>_lowputc.h
│       ├── <vendor_name>_start.c
│       ├── <vendor_name>_start.h
│       └── <vendor_name>_timeisr.c
```

### 1、启动入口

#### 概述

在 `nuttx/arch` 目录下，系统为统一异常处理流程，为每个架构（arch）都定义了异常向量表（如 `_vectors`）。

以 [ARMv8-M](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/arch/arm/src/armv8-m/arm_vectors.c#L94) 为例，当发生复位异常时，系统会调用不同芯片实现的 `__start` 函数。

`__start` 函数的具体实现位于 **`<vendor_name>`**`_start.c` 文件中。开发者可以参考典型实现，如 [stm32_start.c](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/arch/arm/src/stm32f7/stm32_start.c)，以完成芯片平台的适配。

#### `__start` 函数的职责

`__start` 函数是系统复位异常的入口函数，其主要职责包括以下方面：

- 清除 BSS 段：
    - BSS（Block Started by Symbol）段用于存储未初始化的全局变量和静态变量。在系统复位后，需将其清零。
- 拷贝 `.data` 和 RAM 函数到指定位置：
    - 将只读存储器（如 Flash）中的 `.data` 段和 RAM 函数拷贝到运行时 RAM 的指定区域。
- 初始化必要模块：
    - 配置系统时钟（clock）。
    - 初始化串口（serial）。
    - 设置堆栈限制（stack limit）等环境变量。
- 调用操作系统启动入口：
    - 通过 `nx_start()` 函数加载和启动 openvela 核心操作系统。

#### 示例代码：`__start` 函数

以下是一个标准的 `__start` 函数实现模板，用于完成系统复位入口的初始化流程：

```C
/****************************************************************************
 * Name: __start
 *
 * Description:
 *   This is the reset entry point.
 *
 ****************************************************************************/

void __start(void)
{
  /* do something initialize */
  
  ...
  
#ifdef CONFIG_ARCH_PERF_EVENTS
  up_perf_init((void *)STM32_SYSCLK_FREQUENCY);
#endif

  /* Perform early serial initialization */

#ifdef USE_EARLYSERIALINIT
  arm_earlyserialinit();
#endif

  /* Bring up NuttX */
    
  nx_start();

  /* Shouldn't get here */

  for (; ; );
}
```

### 2、串口

#### 概述

芯片通常包含多路串口，通常选用一路串口作为系统控制台（console），用于输出日志和 `nsh` 交互。在系统初始化（bringup）过程中，这一路串口的正常工作非常关键，详情请参见[串口驱动适配](../device_dev_guide/driver/bus_driver/UART/UART.md)。

#### 代码位置

- 参考实现：
    - [stm32_serial.c](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/arch/arm/src/stm32f7/stm32_serial.c)
    - [stm32_lowputc.c](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/arch/arm/src/stm32f7/stm32_lowputc.c)

- 串口相关实现一般位于：

    - `<vendor_name>_lowputc.c`
    - `<vendor_name>_serial.c`

#### 初始化流程

- 串口的初始化通常发生在 `nx_start` 之前。

- 每个架构（arch）都会提供 `<arch>_earlyserialinit` 接口，用于初始化控制台对应的串口寄存器，后续可通过 `<arch>_lowputc` 函数完成日志打印。下面是 ARM 平台的示例函数：

    ```C

    ./arm/src/common/arm_internal.h

    /****************************************************************************
    - Name: arm_earlyserialinit
    -
    - Description:
    - Performs the low level USART initialization early in debug so that the
    - serial console will be available during bootup.  This must be called
    - before arm_serialinit.
    -
     ****************************************************************************/

    #ifdef USE_EARLYSERIALINIT
    void arm_earlyserialinit(void)
    {
    }

    /****************************************************************************
    - Name: arm_lowputc
    -
    - Description:
    - Output one byte on the serial console
    -
     ****************************************************************************/

    void arm_lowputc(char ch)
    {
    }

    ```

#### 串口访问

操作系统代码会使用通用架构接口 `up_putc` 和 `up_puts` 来直接访问串口，其中 `up_putc` 需要厂商实现。

```C
/****************************************************************************
 * Name: up_putc
 *
 * Description:
 *   Provide priority, low-level access to support OS debug writes
 *
 ****************************************************************************/

void up_putc(int ch)
{
}
```

#### 串口驱动注册

为了使应用可以通过标准输入/输出（`stdin/out/err`）访问物理串口，必须注册串口驱动。

- 每个架构提供 `<arm>_serialinit` 接口，又厂商实现。

- 内部调用 `uart_register` 注册控制台和其他串口设备节点。以下为 ARM 平台示例：

    ```C

    /****************************************************************************
    - Name: arm_serialinit
    -
    - Description:
    - Register serial console and serial ports.  This assumes
    - that arm_earlyserialinit was called previously.
    -
     ****************************************************************************/

    void arm_serialinit(void)
    {
    #ifdef CONSOLE_DEV
      uart_register("/dev/console", &CONSOLE_DEV);
    #endif
      ...
    }
    ```

### 3、定时器

#### 概述

定时器（Timer）与系统的计时和定时相关。在 openvela 中，提供了两种主要的驱动模型：

- `arch_alarm`：基于单次定时器（oneshot driver）。
- `arch_timer`：基于常规计时器（timer driver）。

两种驱动的主要区别在于硬件计数器超时后的处理方式，这直接影响定时精度和误差。

#### 驱动模型区别与适用

- arch_alarm 适用于硬件计数器超时后无需清空计数器的情况。该模型避免了重新启动计数器带来的累计误差。
- arch_timer 通常适配于如系统滴答定时器（`systick`）等周期性定时器，硬件计数器在超时后需要清空并重新启动，更多详情请参见 [Arch Timer 驱动框架使用指南](../device_dev_guide/driver/timer_driver/timer/Arch_Timer.md)。

#### arch_alarm 驱动适配流程

厂商实现时，主要关注如下步骤：

1. 实现单次定时器（oneshot）驱动。
2. 在 `up_timer_initialize` 函数中，调用驱动初始化接口创建 `oneshot_lowerhalf_s` 实例。
3. 调用 `up_alarm_set_lowerhalf` 将驱动与系统 `arch_alarm` 模型绑定。

以下是 `up_timer_initialize` 函数的参考实现，位于 [arm_arch_timer.c](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/arch/arm/src/armv8-r/arm_arch_timer.c#L377)：

```C
/****************************************************************************
 * Function:  up_timer_initialize
 *
 * Description:
 *   This function is called during start-up to initialize the timer
 *   interrupt.
 *
 ****************************************************************************/

void up_timer_initialize(void)
{
   struct oneshot_lowerhalf_s *lower = xxx_oneshot_initialize();
   
   up_alarm_set_lowerhalf(lower);
}
```

### 4、异常/中断

每个架构（arch）都提供好了对应的中断异常向量表，使得厂商能够调用 `irq_attach` 绑定相应的中断处理函数。

为实现中断的初始化、启用、禁用和优先级设置，厂商需要实现一系列与架构相关的以 `up_` 开头的函数。

- 详细内容请参见[中断系统适配指南](./Interrupt_System_Adaptation_Guide.md)。
- 相关代码请参考 [stm32_irq.c](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/arch/arm/src/stm32f7/stm32_irq.c)，中断的实现在`<vendor_name>_irq.c`中。

### 5、Stack/Heap

#### 概述

在嵌入式系统中，栈（stack）和堆（heap）的划分至关重要。通常在平面构建（flat build）下的内存布局如下：

```C
.data region              Size determined at link time.
.bss region               Size determined at link time.
IDLE thread stack         Size determined by CONFIG_IDLETHREAD_STACKSIZE.
Heap                      Extends to the end of SRAM.
```

说明如下：

- `.data` 区域：该区域大小在链接时确定。
- `.bss` 区域：该区域大小在链接时确定。
- IDLE 线程栈：大小由 `CONFIG_IDLETHREAD_STACKSIZE` 定义。
- 堆（Heap）：从静态随机存取存储器（SRAM）的末尾向下延伸。

> 注意
>
> IDLE 栈通常位于 `.bss` 段之后，其大小由 `CONFIG_IDLETHREAD_STACKSIZE` 指定，堆紧随其后。

#### 中断栈配置

- 厂商可通过配置项 `CONFIG_ARCH_INTERRUPTSTACK` 设置中断栈大小。
- 中断栈空间由全局变量 `g_intstackalloc` 定义。
- 各架构通过对应的初始化函数（例如 `arm_initialize_stack`）调用 `up_get_intstackbase` 获取中断栈底部地址，并根据 `CONFIG_ARCH_INTERRUPTSTACK` 计算栈顶。

#### 堆管理

- openvela 支持多个独立的堆管理。同一堆可包含多个不连续的物理内存区域。
- 系统、驱动和应用通过 `kmm_malloc` 或标准 `malloc` API 申请堆内存。
- 参考代码位置：[stm32_allocateheap.c](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/arch/arm/src/stm32f7/stm32_allocateheap.c)。

#### 堆大小计算

通常情况下，系统的剩余 RAM（去除了 `.data`、`.bss` 和 IDLE 栈等部分）将注册为堆。因此，堆的总大小会随系统的变化而变化。可以使用以下方法计算堆的起始地址和大小：

- 起始地址：`ebss + CONFIG_IDLETHREAD_STACKSIZE`
- 堆大小：`RAM 末地址 - 起始地址`

### 6、Kconfig 和 Make.defs

#### 概述

Kconfig 和 Make.defs 是构建和配置 openvela 系统的两个重要文件。它们分别用于定义芯片的配置项和管理编译源文件。

#### Kconfig 作用

chip 目录下的 Kconfig 文件用于定义芯片相关的配置项，内容包括：

- 芯片型号（Chip Model）
- 芯片功能（Chip Features）
- 内部模块配置项（Internal Module Settings）

例如，[nuttx/arch/arm/src/stm32f7/Kconfig](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/arch/arm/src/stm32f7/Kconfig) 文件定义了 STM32F7 系列芯片的相关配置，支持不同型号的 flash 配置和片内驱动配置。

以下是针对 STM32F7 系列芯片的 Kconfig 配置片段示例，其中 `ARCH_CHIP_STM32F722RC` 和 `ARCH_CHIP_STM32F722RE` 都属于定义该芯片系列的选项，但两者具有不同的 flash 配置。

```Shell
if ARCH_CHIP_STM32F7

comment "STM32 F7 Configuration Options"

choice
        prompt "STM32 F7 Chip Selection"
        default ARCH_CHIP_STM32F746NG
        depends on ARCH_CHIP_STM32F7

config ARCH_CHIP_STM32F722RC
        bool "STM32F722RC"
        select STM32F7_STM32F722XX
        select STM32F7_FLASH_CONFIG_C
        select STM32F7_IO_CONFIG_R
        ---help---
                STM32 F7 Cortex M7, 256 FLASH, 256K (176+16+64) Kb SRAM

config ARCH_CHIP_STM32F722RE
        bool "STM32F722RE"
        select STM32F7_STM32F722XX
        select STM32F7_FLASH_CONFIG_E
        select STM32F7_IO_CONFIG_R
        ---help---
                STM32 F7 Cortex M7, 512 FLASH, 256K (176+16+64) Kb SRAM
...
endif
```

- `choice` 节点定义了芯片选择菜单，用户可通过该配置选择具体芯片型号。
- 各 `config` 项对应具体芯片型号，指定对应的特性和资源分配（如 flash 大小和 IO 配置）。
- `select` 关键字用于自动选择相应的配置子项。

芯片的片内驱动及各种硬件相关配置也可以在此 Kconfig 文件中进行定义和管理。

#### Make.defs 作用

Make.defs 文件用于管理参与编译的源文件列表，确保构建系统正确编译所需代码。在对应的 Make.defs 文件中，需要添加所有要参与编译的源文件，确保构建系统能够正确处理各模块代码。可参考 [nuttx/arch/arm/src/stm32f7/Make.defs](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/arch/arm/src/stm32f7/Make.defs) 示例文件。

### 7、chip.h 和 irq.h 文件说明

- `chip.h` 文件
    - `vendor/vendor_name/chip/chip_name` 目录下有两个 `chip.h` 文件：
        - 局部 `chip.h`：位于当前目录，定义与该芯片相关的宏和函数声明。
        - 公共 `chip.h`：位于 `include/chip.h`，通过 `#include <arch/chip/chip.h>` 引用，定义与架构相关的宏和函数，被架构层公共代码使用。
- `irq.h` 文件
    - 结构类似：存在局部和公共两个层次。
    - 公共 `include/irq.h` 负责架构通用中断相关定义。
    - 局部 `irq.h` 针对具体芯片的中断定义。
- 引用建议
    - 局部文件用于芯片特定代码，使用相对路径引用。
    - 公共文件用于架构共享代码，通过标准 include 路径引用。
- 目的
    - 明确区分局部与公共文件，避免混淆和冲突。
    - 保证代码模块化，架构统一。

## 三、板级层适配

板级层适配主要完成以下内容：

- 链接脚本（Linker Script）
- 主 `Make.defs`
- `etcramfs` 构建
- Board 配置（Board Configs）
- Board 初始化代码

整体代码结构如下：

```Shell
vendor/vendor_name/
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
```

### 1、初始化代码

#### 阶段划分

- `board_early_initialize`：在 idle 任务前执行，早期硬件初始化。
- `board_late_initialize`：在 Appbringup 线程上下文执行，常规驱动初始化。
- `board_app_initialize`：在 nsh 任务上下文执行，文件系统与核心服务初始化。
- `board_app_finalinitialize`：在 nsh 任务上下文执行，应用相关初始化。

详细流程请参见[启动流程](../device_dev_guide/kernal/boot_process.md)，厂商需要按照外设所初始化的时刻写到对应的函数中。

#### 示例代码

相关的文件包括：

- `<vendor_name>_bringup.c`
- `<vendor_name>_appinit.c`
- `<vendor_name>_boot.c`

示例代码可参考 [nuttx/boards/arm/stm32f7/stm32f746g-disco/src/stm32_boot.c](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/boards/arm/stm32f7/stm32f746g-disco/src/stm32_boot.c#L99)

```C
#ifdef CONFIG_BOARD_EARLY_INITIALIZE
void board_early_initialize(void)
{

}
#endif

#ifdef CONFIG_BOARD_LATE_INITIALIZE
void board_late_initialize(void)
{

}

int board_app_initialize(uintptr_t arg)
{

}

#ifdef CONFIG_BOARDCTL_FINALINIT
int board_app_finalinitialize(uintptr_t arg)
{

}
#endif
```

### 2、ETCROMFS 构建

- 功能说明： 根文件系统以只读文件系统（ROMFS）形式存放于 Flash。
- 用途： 存储应用配置文件、密钥等敏感文件。
- 添加文件步骤：
    - 在 `Make.defs` 中通过 `RCRAWS` 增加目标文件路径。
    - 删除 `etctmp` 目录后，触发增量编译。
    - 启动后，文件可通过 `/etc/` 路径访问。

##### 示例 `Make.defs` 配置

```Makefile
ifeq ($(CONFIG_ETC_ROMFS),y)                                  
RCSRCS += etc/init.d/rc.sysinit etc/init.d/rcS                
RCRAWS += etc/group etc/passwd                                
RCRAWS += etc/build.prop                                      
RCRAWS += etc/txtable.txt                                     
                                                              
ifneq ($(CONFIG_UTILS_AVB_VERIFY)$(CONFIG_UTILS_ZIP_VERIFY),) 
  RCRAWS += etc/key.avb                                       
endif                                                         
                                                              
ifeq ($(CONFIG_ATS3085X_BOOTLOADER),y)                        
RCRAWS += etc/factory.sh                                      
endif                                                         
                                                                         
```

### 3、链接脚本

每个 board 可配置自定义链接脚本，该链接脚本在 `board/Make.defs` 中通过 `LDSCRIPT` 关键字指定。一般链接脚本存放于如下路径： `vendor/vendor_name/boards/chip_name/board_name/scripts`

例如：[nuttx//boards/arm/stm32f7/stm32f746g-disco/scripts/flash.ld](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/boards/arm/stm32f7/stm32f746g-disco/scripts/flash.ld)

链接脚本的要求包括：

- 设置 ENTRY 为 `_vectors`，以支持全局向量表。
- 若支持 backtrace，需添加 `.arm.exidx` 段。更多详情请参见 [Backtrace](../device_dev_guide/debugging/memory/offline/backtrace.md)。

链接脚本示例：

```Makefile
MEMORY
{                                                                                       
  flash (rx) : ORIGIN = 0x10000000, LENGTH = 2560K                                      
  sram (rwx) : ORIGIN = 0x01000400, LENGTH = 111K                                       
  psram (rwx) : ORIGIN = 0x18000000, LENGTH = 4M                                        
  dsp_inner_ram (rwx) : ORIGIN = 0x01054000, LENGTH = 16K                           
  share_ram (rwx) : ORIGIN = 0x0106A600, LENGTH = 22K                                   
}        
                                                                               
OUTPUT_ARCH(arm)                                                                        
EXTERN(_vectors)                                                                        
ENTRY(_stext)                                                                           
SECTIONS                                                                                {                                                                                       
    .text : {                                                                           
        . = 0x200;                                                                      
        _stext = ABSOLUTE(.);                                                           
        *(.vectors)                                                                     
        *(.text .text.*)                                                                
        *(.fixup)                                                                       
        *(.gnu.warning)                                                                 
        *(.rodata .rodata.*)                                                            
        *(.gnu.linkonce.t.*)                                                            
        *(.glue_7)                                                                      
        *(.glue_7t)                                                                     
        *(.got)                                                                         
        *(.gcc_except_table)                                                            
        *(.gnu.linkonce.r.*)                                                            
        _etext = ABSOLUTE(.);                                                         
    } > flash    
}
```

### 4、配置文件（Configs）

每个 board 可包含多个配置文件（config files），通常以 `nsh` 配置启动系统，仅具基本功能，配置位置在： `vendor/vendor_name/boards/chip_name/board_name/configs/nsh`。

例如：[nuttx/boards/arm/stm32f7/stm32f746g-disco/configs](https://github.com/open-vela/nuttx/tree/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/boards/arm/stm32f7/stm32f746g-disco/configs)

> 注意
>
> openvela 建议不要增加太多配置文件，以减少维护负担。

### 5、Kconfig、Makefile 和 Make.defs

- Kconfig：定义板外设的配置项，包括外设驱动和板级配置。更多详情请参见 [Kconfig](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/boards/arm/stm32f7/stm32f746g-disco/Kconfig) 示例。

- Makefile：将需要编译的源文件添加到构建中，最终生成 `libboard.a`。更多详情请参见 [Makefile](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/boards/arm/stm32f7/stm32f746g-disco/src/Make.defs) 示例。

- scripts/Make.defs：顶层构建配置，包含系统配置 `.config`、`Toolchain.defs`、链接脚本及外部库引用等。详情请参见 [Make.defs](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/boards/arm/stm32f7/stm32f746g-disco/scripts/Make.defs) 示例。

    示例 Make.defs 片段：

    ```Makefile

    include $(TOPDIR)/.config
    include $(TOPDIR)/tools/Config.mk
    include $(TOPDIR)/arch/arm/src/armv7-m/Toolchain.defs

    LDSCRIPT = ld.script

    ARCHSCRIPT += $(BOARD_DIR)$(DELIM)scripts$(DELIM)$(LDSCRIPT)

    CFLAGS := $(ARCHCFLAGS) $(ARCHOPTIMIZATION) $(ARCHCPUFLAGS) $(ARCHINCLUDES) $(ARCHDEFINES) $(EXTRAFLAGS) -pipe
    CPICFLAGS = $(ARCHPICFLAGS) $(CFLAGS)
    CXXFLAGS := $(ARCHCXXFLAGS) $(ARCHOPTIMIZATION) $(ARCHCPUFLAGS) $(ARCHXXINCLUDES) $(ARCHDEFINES) $(EXTRAFLAGS) -pipe
    CXXPICFLAGS = $(ARCHPICFLAGS) $(CXXFLAGS)
    CPPFLAGS := $(ARCHINCLUDES) $(ARCHDEFINES) $(EXTRAFLAGS)
    AFLAGS := $(CFLAGS) -D__ASSEMBLY__

    EXTRA_LIBS += $(wildcard $(shell readlink -f $(TOPDIR)/$(CONFIG_ARCH_BOARD_CUSTOM_DIR)/libs/$(CONFIG_ARCH_BOARD_CUSTOM_NAME))/*.a)
    EXTRA_LIBS += $(wildcard $(shell readlink -f $(TOPDIR)/$(CONFIG_ARCH_BOARD_CUSTOM_DIR)/libmedia/*.a))

    ```

### 6、board.h 与 nsh_romfsimg.h

- `board.h`：主要用于定义外设驱动和板级配置相关的宏或函数声明，通过 `<arch/board/board.h>` 引入。 可参考 [nuttx/boards/arm/stm32f7/stm32f746g-disco/include/board.h](https://github.com/open-vela/nuttx/blob/41545a4ca98165813908e5fe25d3ecdbfc5ab19a/boards/arm/stm32f7/stm32f746g-disco/include/board.h) 示例。
- `nsh_romfsimg.h`：自动生成的根文件系统内容，不建议手动修改。

### 7、工具链

厂商可导入自定义工具链，通常存放于 `vendor/vendor_name/prebuilt`。可通过 `board/scripts/Make.defs` 配置编译器、链接器工具路径等。

## 四、构建运行

openvela 支持两种编译方式：CMake 和 Make。

推荐使用以下 CMake 命令进行构建：

```Makefile
./build.sh vendor/vendor_name/board/chip_name/configs/nsh --cmake -j8
```

执行上述命令后，将生成 `vela_ap.bin` 文件，厂商可采用相应的烧录方式进行运行验证。

## 五、测试验证

厂商完成适配后，需要通过准入测试进行检验，主要包括以下几个方面：

- 功能测试
- 稳定性测试
- 性能测试
