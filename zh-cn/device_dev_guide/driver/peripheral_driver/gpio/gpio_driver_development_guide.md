# GPIO 驱动开发指南

[ [English](../../../../../en/device_dev_guide/driver/peripheral_driver/gpio/gpio_driver_development_guide.md) | 简体中文 ]

本指南面向**驱动开发者和 BSP (板级支持包) 工程师**，详细介绍 openvela 的 GPIO 驱动框架，以及如何将底层硬件 GPIO 功能接入 openvela 内核。

在阅读本文之前，我们假定您已经熟悉 GPIO 的基本概念和北向接口。如果您对此尚不了解，请先阅读 [GPIO 应用开发指南](./gpio_app_development_guide.md)。

本文档将深入探讨驱动层的实现细节，内容组织如下：

- **南向接口(驱动层)**：详细介绍 `ioexpander` 和 `lower_half` 两种驱动实现方式及其差异。
- **芯片级 API**：阐述最底层的硬件抽象层职责。
- **开发与实践**：提供文件组织规范和与其他操作系统的对比。

## 一、GPIO 南向接口 (驱动层)

南向接口负责将底层的芯片（Chip）或板级（Board）GPIO 功能接入 openvela 的虚拟文件系统（VFS）或其他驱动子系统。开发者需要实现一套标准的操作函数集，以供北向接口调用。

openvela 提供两种实现南向接口的方式：

- **`ioexpander`** **框架**：一种通用的 I/O 抽象框架，推荐用于管理大量或复用的 I/O 资源。
- **`lower_half`** **方式**：一种直接、轻量级的实现，通常与特定板级代码紧密绑定。

> **推荐**：在进行 SOC (System on a Chip) 适配时，我们推荐使用 `ioexpander` 方式。它能统一管理所有 I/O 资源，并能有效减少适配代码量。

### 1、`ioexpander` 框架

`ioexpander` 是一个通用的 I/O 扩展驱动框架，适用于需要统一管理大量 GPIO 的场景。采用此方式，您需要为 `ioexpander` 框架实现一套标准的回调函数。

`ioexpander` 驱动实例不仅可以在内核中被其他驱动直接高效调用，可以直接访问不同的引脚，甚至于同时访问多个引脚，还可以通过 `gpio_lower_half()` 接口将每个引脚注册为用户空间可见的 `/dev/gpiox` 设备。

内核通过 [drivers/ioexpander/gpio_lower_half.c](https://github.com/apache/nuttx/blob/master/drivers/ioexpander/gpio_lower_half.c) 文件中的代码实现 `ioexpander` 与 VFS 之间的桥接，该桥接层会调用您在驱动中实现的 `IOEXP_xxx` 宏接口，而宏接口也就需要按 `ioexpender` 所需要实现的接口分别实现。

<img src="./figures/003.png" alt="" width="75%">

#### 配置选项

要使用 `ioexpander` 方式，请在配置中启用以下选项：

```Makefile
# 启用 ioexpander 框架
CONFIG_IOEXPANDER=y
# 启用将 ioexpander 桥接到 GPIO 字符设备的功能
CONFIG_GPIO_LOWER_HALF=y
# 用于支持多引脚批量操作
CONFIG_IOEXPANDER_MULTIPIN=y
# 用于支持中断功能
CONFIG_IOEXPANDER_INT_ENABLE=y
```

#### 依赖头文件

在 `ioexpander` 方式下，需要实现的接口定义在如下头文件中，在编写 GPIO 驱动时需要包含该头文件：

```C
//配置依赖：CONFIG_GPIO_LOWER_HALF=y
#include <nuttx/ioexpander/ioexpander.h>
```

#### 核心接口实现

您需要实现 `ioexpander_ops_s` 结构体中定义的回调函数。下表总结了这些核心接口。

| **函数原型**                                                                                       | **描述**                                                                       | **状态**                              |
| :------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------- | :------------------------------------ |
| `int ioe_direction(dev, pin, dir)`                                                                 | 设置单个引脚的方向（输入/输出/上拉/下拉等）。                                  | **必需**                              |
| `int ioe_option(dev, pin, opt, val)`                                                               | 配置引脚选项，如中断触发方式（边沿/电平）或有效电平。                          | **必需**                              |
| `int ioe_writepin(dev, pin, val)`/`int ioe_readpin(dev, pin, *val)`                                | 对某个引脚进行读写操作。                                                       | **必需**                              |
| `int ioe_readbuf(dev, pin, *val)`                                                                  | 从内部缓冲区读取引脚电平。此操作效率高，但可能与引脚实际状态不一致。           | **必需**                              |
| `int ioe_multiwritepin(dev, *pins, *vals, count)`/`int ioe_multireadpin(dev, *pins, *vals, count)` | 批量读写多个引脚的电平值。                                                     | 可选 (`CONFIG_IOEXPANDER_MULTIPIN`)   |
| `int ioe_multireadbuf(dev, *pins, *vals, count)`                                                   | 从内部缓冲区批量读取多个引脚的电平。此操作效率高，但可能与引脚实际状态不一致。 | 可选 (`CONFIG_IOEXPANDER_MULTIPIN`)   |
| `void *ioe_attach(dev, pinset, cb, arg)`                                                           | 附加一个中断回调函数到指定的引脚集。                                           | 可选 (`CONFIG_IOEXPANDER_INT_ENABLE`) |
| `int ioe_detach(dev, handle)`                                                                      | 移除一个已附加的中断回调。                                                     | 可选 (`CONFIG_IOEXPANDER_INT_ENABLE`) |

#### 注意事项

1. 您需要在驱动初始化时，手动调用 `gpio_lower_half()` 函数，才能将 `ioexpander` 的引脚注册为用户空间可见的 `/dev/gpiox` 设备。
2. 设备注册名遵循固定规则 `/dev/gpiox`，其中 `x` 是引脚编号。

#### 示例代码

- **`ioexpander`** **驱动实现**：可参考 PCA9555 I/O 扩展芯片的驱动实现 [pca9555.c](https://github.com/apache/nuttx/blob/master/drivers/ioexpander/pca9555.c)。
- **`ioexpander`** **驱动实例化**：可参考仿真平台（SIM）的 `ioexpander` 实例化代码 [sim_ioexpander.c](https://github.com/apache/nuttx/blob/master/boards/sim/sim/sim/src/sim_ioexpander.c)。

### 2、`lower_half` 方式

`lower_half` 方式是一种更直接的 GPIO 驱动实现，其代码通常与特定的板级（Board）配置绑定。在这种模式下，您需要直接实现 `gpio_dev_s` 结构体定义的回调函数。

这些回调函数通常会调用芯片厂商提供的底层 GPIO API（即 `chip gpio api`）。openvela 对 `chip gpio api` 没有强制规范，开发者只需遵循 openvela 的编码风格，并确保实现芯片所支持的全部 GPIO 功能即可。

<img src="./figures/004.png" alt="" width="75%">

#### 依赖头文件

在 `lower_half` 方式下，需要实现的接口定义在如下头文件中，在编写 Board GPIO 驱动时需要包含该头文件：

```C
//配置依赖：CONFIG_DEV_GPIO=y
#include <nuttx/ioexpander/gpio.h>
```

#### 核心接口实现

您需要为 `gpio_lowerhalf_s` 结构体填充以下回调函数指针。

| **函数原型**                      | **描述**                                       |
| :-------------------------------- | :--------------------------------------------- |
| `int go_read(dev, *value)`        | 读取引脚电平。对所有引脚类型都是必需的。       |
| `int go_write(dev, value)`        | 写入引脚电平。仅对输出类型的引脚有效。         |
| `int go_setpintype(dev, pintype)` | 设置引脚类型，如输入、输出、中断等。           |
| `int go_attach(dev, callback)`    | 附加一个中断回调函数。仅对中断类型的引脚有效。 |
| `int go_enable(dev, enable)`      | 使能或禁用引脚中断。                           |

#### 注意事项

1. `go_write()` 函数仅需为输出类型的引脚实现。
2. 在实现 `go_enable()` 时，必须检查是否已通过 `go_attach()` 注册了回调函数，否则不应允许使能中断。
3. `go_attach()` 和 `go_enable()` 仅需为支持中断的引脚类型实现。
4. **重要**：在实现 `go_setpintype()` 时，除了配置硬件，您还**必须**手动更新 `dev->gpio.gp_pintype` 成员变量。

#### 示例代码

`lower_half` 驱动与板级代码紧密相关。您可以在 `boards` 目录下找到适用于不同架构和板卡的实现。例如，树莓派 Pico（RP2040 芯片）的 `lower_half` GPIO 驱动：[rp2040_gpio.c](https://github.com/apache/nuttx/blob/master/boards/arm/rp2040/raspberrypi-pico/src/rp2040_gpio.c)。

#### 设备注册

要使 GPIO 设备对用户空间可见，必须进行设备注册。注册过程会将您的南向接口实现与一个设备文件名（如 `/dev/gpio0`）关联起来。

您可以使用以下函数进行注册：

- **`int gpio_pin_register(FAR struct gpio_dev_s \*dev, int minor)`**

    - 通过次设备号（minor number）注册设备，设备名为 `/dev/gpio` + `minor`。

- **`int gpio_pin_register_byname(FAR struct gpio_dev_s \*dev, FAR const char \*pinname)`**

    - 通过指定名称注册设备，设备名为 `/dev/` + `pinname`。

> **提示**：如果您使用 `ioexpander` 方式，可以直接调用 [gpio_lower_half()](https://github.com/apache/nuttx/blob/master/drivers/ioexpander/gpio_lower_half.c) 函数，它内部封装了注册逻辑。

#### `ioexpander` 与 `lower_half` 对比

下表总结了两种南向接口实现方式的主要差异。

| **特性**               | **`lower_half`** **方式**            | **`ioexpander`** **方式**                                                                                                                                        |
| :--------------------- | :----------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **核心配置**           | `CONFIG_DEV_GPIO=y`                  | `CONFIG_DEV_GPIO=y` <br>`CONFIG_IOEXPANDER=y` <br>`CONFIG_GPIO_LOWER_HALF=y`<br>可选配置：<br>`CONFIG_IOEXPANDER_MULTIPIN=y`<br>`CONFIG_IOEXPANDER_INT_ENABLE=y` |
| **批量操作**           | 不支持                               | 支持 (`IOEXP_MULTIWRITEPIN`, `IOEXP_MULTIREADPIN`)                                                                                                               |
| **其他驱动子系统调用** | 需通过 VFS 访问，一般通过`file_open` | 提供 `IOEXP_xxx()` 宏接口，可被其他驱动直接高效调用。                                                                                                            |
| **设备注册**           | 需手动调用 `gpio_pin_register()`     | 调用 `gpio_lower_half()` 统一注册，名称固定为 `/dev/gpiox`                                                                                                       |
| **中断设置**           | 仅通过 `ioctl` 的 `GPIOC_SETPINTYPE` | 除 `ioctl` 外，还可使用 `IOEXP_SETOPTION()` 在内核层配置                                                                                                         |

## 二、芯片级 GPIO API (`chip gpio api`)

芯片级 API 是最底层的硬件抽象层，负责直接操作 GPIO 寄存器。它需要实现芯片所支持的全部 GPIO 功能，包括引脚模式配置、电平读写、复用功能切换等。

openvela 对此层级没有定义标准接口。芯片厂商或开发者需要根据具体芯片的数据手册，自行实现这部分功能，并遵循 openvela 的编码规范。

- **参考实现**：您可以参考 [STM32 系列芯片的 GPIO 底层实现 stm32_gpio.c](https://github.com/apache/nuttx/blob/master/arch/arm/src/stm32/stm32_gpio.c)。

## 三、文件组织规范

以下是在 openvela 开发分支中推荐的 GPIO 相关文件组织结构。如果您使用上游 NuttX master 分支，请参考其社区规范。

<details>
<summary>点击展开</summary>

```Bash
vendor
└── vendor_name    # 产品型号
    ├── boards    #板子目录
    │   └── board_name    #板子型号
    │      ├── configs    #配置目录
    │      │   ├── gpio
    │      │   │   └── defconfig
    ...    ...    ...
    │      ├── include    # 板子的头文件内容
    │      │   ├── board.h
    │      │   ├── board_memorymap.h
    │      │   ├── nsh_romfsimg.h   
    │      ├── Kconfig    #板子配置文件
    │      ├── scripts   #板子的脚本文件
    │      │   └── Make.defs
    │      └── src  #板子用的源码
    │          ├── xxx_appinit.c
    │          ├── xxx_boot.c
    │          ├── xxx_bringup.c
    │          ├── xxx_gpio.c    # 板级gpio驱动，即南向接口实现
    │          ├── xxx_ioctl.c
    │          ├── xxx_reset.c
    │          ├── xxx_uid.c
    │          ├── etc  
    │          │   ├── init.d   # 系统启动脚本文件
    │          │   │   ├── rcS
    │          │   │   ├── rc.sysinit
    │          │   ├── group
    │          │   └── passwd
    │          ├── Make.defs
    │          └── Makefile
    ├── chips    #芯片内文件
    │   └── chip_name    #芯片名称
    │       ├── xxx_gpio.c      #芯片内部gpio所有能力实现
    │       ├── xxx_gpio.h      #芯片board提供的gpio
    │       ├── ...
    │       ├── ...
    │       ├── xxx_wlan.c
    │       ├── xxx_wlan.h
    │       ├── include
    │       │   └── xxx.h     
    │       ├── hardware
    │       │   └── apb_ctrl_reg.h
    │       │   └── bb_reg.h
    │       │   └── xxx_aes.h
    │       │   └── xxx_memory.h
    │       │   └── xxx_dma.h
    │       │   └── xxx_efuse.h
    │       │   └── xxx_gpio.h
    │       │   └── xxx_gpio_sigmap.h
    │       │   └── xxx_i2c.h
    │       ├── include
    │       │   ├── chips_name_gpio.h
    │       │   └── debug.h
    │       ├── Kconfig
    │       └── Make.defs
    │       └── rom
    │       ├── xxx_libc_stubs.h
    │            └── xxx_spiflash.h
    └── tools    #目录，构建前的工具或toolchain放置位置
```

</details>

---

- **`boards/<board_name>/src/xxx_gpio.c`**：这是**南向接口**的实现文件，负责将芯片的 GPIO 功能桥接到 openvela 的 VFS。
- **`chips/<chip_name>/xxx_gpio.c`**：这是**芯片级 API** 的实现文件，负责直接操作硬件寄存器，是 GPIO 功能的最底层实现。

## 四、与其他操作系统的对比

下表简要对比了 openvela、Linux 和 Zephyr 在 GPIO 子系统上的主要差异。

| **特性**               | **openvela**                                                            | **Zephyr**                   | **Linux**                         |
| :--------------------- | :---------------------------------------------------------------------- | :--------------------------- | :-------------------------------- |
| **北向接口**           | 字符设备 (`/dev/gpiox`)                                                 | 自定义系统调用, 需设备树配合 | `libgpiod` (现代), `sysfs` (传统) |
| **南向接口**           | `struct gpio_dev_s` (lower_half) `struct ioexpander_dev_s` (ioexpander) | `struct gpio_driver_api`     | `struct gpio_chip`                |
| **其他驱动子系统使用** | `ioexpander` 宏接口                                                     | `device_get_binding()`       | `gpio_to_chip()`                  |
| **Pin Control**        | 无独立子系统，功能分散在 GPIO 驱动中                                    | 支持                         | 独立的 Pinctrl 子系统             |
| **配置系统**           | Kconfig                                                                 | Kconfig, Device Tree         | Kconfig, Device Tree              |