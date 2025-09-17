# 系统启动流程

\[ [English](../../../en/device_dev_guide/kernel/boot_process.md) | 简体中文 \]

本文详细解析 openvela 系统的板级支持包（BSP）初始化流程、启动脚本机制以及核心函数调用关系，旨在为开发者提供一份清晰、结构化的启动过程指南。

## 一、板级初始化流程

openvela 系统的启动过程遵循明确的板级支持包（BSP）初始化序列。该序列从内核入口 `nx_start` 开始，在不同任务上下文中分阶段执行初始化函数，直至进入 `idle` 循环。

### 核心初始化顺序

```C
// --- 在 Idle Task (空闲任务) 上下文中 ---
nx_start()
  |
  +--> board_early_initialize()
  |
  +--> // 创建 AppBringup_task 线程
// --- 在 AppBringup_task (应用启动任务) 上下文中 ---
board_late_initialize()
  |
  +--> // 创建 nsh_task 线程
// --- 在 nsh_task (Nsh 任务) 上下文中 ---
board_app_initialize()
  |
  +--> rc.sysinit // 执行脚本
  |
  +--> board_app_finalinitialize()
  |
  +--> rcS        // 执行脚本
// --- 系统进入 idle 循环 ---
```

下表详细说明了每个关键函数的作用、执行上下文和相关配置项。

| 顺序 | 函数                          | 执行上下文      | 功能描述                                                                                                                                                                                               | 依赖配置项                      |
| :--- | :---------------------------- | :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| 1    | **nx_start**                  | ldle task       | openvela 操作系统入口点。                                                                                                                                                                              |                                 |
| 2    | **board_early_initialize**    | Idle task       | 执行板级早期硬件初始化。 <br> 此阶段在核心组件就绪前执行，因此禁止调用任何可能导致阻塞或依赖事件等待的函数（如 `sem_wait`）。                                                                          | `CONFIG_BOARD_EARLY_INITIALIZE` |
| 3    | **board_late_initialize**     | AppBringup task | 执行板级主要驱动的初始化。 <br> 此时操作系统核心组件已就绪，允许调用包含事件等待的函数。                                                                                                               | `CONFIG_BOARD_LATE_INITIALIZE`  |
| 4    | **board_app_initialize**      | Nsh task        | 由 `nsh` 任务通过 `boardctl` (`BOARDIOC_INIT`) 调用，用于初始化应用层。 <br> **注意**：此阶段文件系统尚未挂载，无法访问文件。                                                                          |                                 |
| 5    | **rc.sysinit**                | Nsh task        | 挂载文件系统并初始化核心启动服务。                                                                                                                                                                     | `CONFIG_NSH_SYSINITSCRIPT`      |
| 6    | **board_app_finalinitialize** | Nsh task        | 执行最终的板级初始化，由 `boardctl` (`BOARDIOC_FINALINIT`) 调用。 <br> 用于初始化依赖文件系统访问的驱动（例如 TP、Charger、Audio PA 等），可直接操作文件，无需通过延迟工作（delay work）机制推后执行。 |                                 |
| 7    | **rcS**                       | Nsh task        | 启动用户空间的核心应用和服务，例如 `miwear`、`algo_service` 等。                                                                                                                                       | `CONFIG_NSH_INITSCRIPT`         |

## 二、启动脚本机制

### 启动脚本位置与加载方式

openvela 使用启动脚本 `rcS` 和 `rc.sysinit` 来完成系统启动配置。启动脚本由 `nsh task` 通过 `nshlib` 加载并解析，其位置由以下配置项指定：

1. `CONFIG_ETC_ROMFSMOUNTPT/CONFIG_NSH_SYSINITSCRIPT`
2. `CONFIG_ETC_ROMFSMOUNTPT/CONFIG_NSH_INITSCRIPT`

通常，启动脚本存放于 `/etc` 目录下。`/etc` 的内容以 `romfs` 文件系统形式与 `openvela binary` 一同编译链接，系统启动后自动挂载。相关配置如下

```Makefile
CONFIG_FS_ROMFS=y
CONFIG_ETC_ROMFS=y
CONFIG_ETC_ROMFSMOUNTPT="/etc"
CONFIG_NSH_SYSINITSCRIPT="init.d/rc.sysinit"
CONFIG_NSH_INITSCRIPT="init.d/rcS"
```

### 启动脚本生成方式

openvela 的 `/etc` 内容由不同的板级目录生成，可通过 `genromfs` 和 `xxd` 工具生成 `etc_romfs.c` 文件，并编译到内核。例如：

- 生成文件路径: `boards/arm/at32/at32f437-mini/src/etc_romfs.c`
- 生成脚本路径: `boards/arm/at32/at32f437-mini/tool/mkromfs.sh`

常见方式是直接从 `board/arch/board/src/etc` 目录构建 `/etc` 内容。例如：

- 示例目录: `boards/sim/sim/sim/src/etc`

`/etc` 下的所有文件由上一级目录的 Makefile 控制：

- `RCSRCS` 用于指定启动脚本。
- `RCRAWS` 用于指定加入 `etc` 目录下的其他文件和目录。

```Makefile
ifeq ($(CONFIG_ETC_ROMFS),y)
  RCSRCS = etc/init.d/rc.sysinit etc/init.d/rcS
  RCRAWS = etc/group etc/passwd
endif
```

## 三、调用关系

下图展示了 openvela 启动流程中的核心函数调用关系，以帮助开发者更直观地理解整个过程。

> 注意：此图为示意图，旨在说明主要流程，具体实现请以最新代码为准。

![img](./figures/boot_process.svg)

## 四、参考资料

- 更多关于openvela和NuttX调用关系的详细信息，请参考 [Call Graph for Apache NuttX Real-Time Operating System (lupyuen.github.io)](https://lupyuen.github.io/articles/unicorn2)
