# System Boot Process

\[ English | [简体中文](../../../zh-cn/device_dev_guide/kernel/boot_process.md) \]

This document outlines the openvela boot process, detailing the Board Support Package (BSP) initialization sequence, the startup script mechanism, and the core function call relationships.

## I. Board Initialization Sequence

The openvela system boot-up follows a well-defined Board Support Package (BSP) initialization sequence. The process begins at the kernel entry point, `nx_start`, and proceeds through several initialization stages within different task contexts before finally entering the `idle` loop.

### Core Initialization Sequence

```C
// --- In Idle Task context ---
nx_start()
  |
  +--> board_early_initialize()
  |
  +--> // Creates the AppBringup_task thread
// --- In AppBringup_task context ---
board_late_initialize()
  |
  +--> // Creates the nsh_task thread
// --- In nsh_task context ---
board_app_initialize()
  |
  +--> rc.sysinit // Script execution
  |
  +--> board_app_finalinitialize()
  |
  +--> rcS        // Script execution
// --- System enters the idle loop ---
```

The following table details the purpose, execution context, and required configuration for each key function and script in the sequence.

| Sequence | Function/Script               | Execution Context | Description                                                                                                                                                                                                                                                                                           | Required Kconfig                |
| :------- | :---------------------------- | :---------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| 1        | **nx_start**                  | Idle Task         | The openvela operating system entry point.                                                                                                                                                                                                                                                            |                                 |
| 2        | **board_early_initialize**    | Idle Task         | Performs early board-level hardware initialization. <br> **Note**: This stage runs before core OS components are ready, so it **must not** call any function that could block or wait for an event (e.g., `sem_wait`).                                                                                | `CONFIG_BOARD_EARLY_INITIALIZE` |
| 3        | **board_late_initialize**     | AppBringup Task   | Initializes the main board-level drivers. <br> **Note**: At this stage, core OS components are ready, allowing calls to functions that may involve event waiting.                                                                                                                                     | `CONFIG_BOARD_LATE_INITIALIZE`  |
| 4        | **board_app_initialize**      | `nsh` Task        | Called by the `nsh` task via `boardctl` (`BOARDIOC_INIT`) to initialize the application layer. <br> **Note**: The file system is not yet mounted, so file access is not possible.                                                                                                                     |                                 |
| 5        | **rc.sysinit**                | `nsh` Task        | Mounts the file system and initializes core startup services.                                                                                                                                                                                                                                         | `CONFIG_NSH_SYSINITSCRIPT`      |
| 6        | **board_app_finalinitialize** | `nsh` Task        | Performs final board-level initialization, called via `boardctl` (`BOARDIOC_FINALINIT`). <br> **Note**: Used for drivers that depend on file system access (e.g., TP, Charger, Audio PA). These drivers can now directly access files without needing to defer operations via the delayed work queue. |                                 |
| 7        | **rcS**                       | `nsh` Task        | Starts user-space core applications and services, such as `miwear` and `algo_service`.                                                                                                                                                                                                                | `CONFIG_NSH_INITSCRIPT`         |

## II. Startup Script Mechanism

### Location and Loading

openvela uses the `rcS` and `rc.sysinit` startup scripts to configure the system during boot. These scripts are loaded and parsed by the `nsh task` via the `nshlib` library. Their locations are specified by the following Kconfig options:

1. `CONFIG_ETC_ROMFSMOUNTPT/CONFIG_NSH_SYSINITSCRIPT`
2. `CONFIG_ETC_ROMFSMOUNTPT/CONFIG_NSH_INITSCRIPT`

Typically, the startup scripts reside in the `/etc` directory. The contents of `/etc` are compiled and linked with the `openvela binary` as a `ROMFS (Read-Only File System)`, which is automatically mounted at boot. The related configuration is as follows:

```Makefile
CONFIG_FS_ROMFS=y
CONFIG_ETC_ROMFS=y
CONFIG_ETC_ROMFSMOUNTPT="/etc"
CONFIG_NSH_SYSINITSCRIPT="init.d/rc.sysinit"
CONFIG_NSH_INITSCRIPT="init.d/rcS"
```

### Generation

The contents of the /etc directory are typically generated from a source directory within the board-specific configuration. The `genromfs` and `xxd` tools can be used to generate an `etc_romfs.c` file, which is then compiled into the kernel. For example:

- **Generated File:** `boards/arm/at32/at32f437-mini/src/etc_romfs.c`
- **Generation Script:** `boards/arm/at32/at32f437-mini/tool/mkromfs.sh`

A more common method is to build the `/etc` contents directly from a `board/arch/board/src/etc` directory, such as:

- **Example Directory:** `boards/sim/sim/sim/src/etc`

All files within `/etc` are controlled by the Makefile in the parent directory:

- `RCSRCS` is used to specify the startup scripts.
- `RCRAWS` is used to specify other files and directories to be included in `/etc`.

```Makefile
ifeq ($(CONFIG_ETC_ROMFS),y)
  RCSRCS = etc/init.d/rc.sysinit etc/init.d/rcS
  RCRAWS = etc/group etc/passwd
endif
```

## III. Call Relationships

The following diagram illustrates the core function call relationships in the openvela boot process, providing a visual overview of the entire sequence.

> **Note**: This diagram is for illustrative purposes and shows the main flow. For precise implementation details, always refer to the latest source code.

![img](./figures/boot_process.svg)

## IV. References

- For a detailed visual analysis of the NuttX boot process, see Lee Lup Yuen's article: [Call Graph for Apache NuttX RTOS](https://lupyuen.github.io/articles/unicorn2).