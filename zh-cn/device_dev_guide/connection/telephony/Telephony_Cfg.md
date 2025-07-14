# Telephony 服务配置指南

\[ [English](../../../../en/device_dev_guide/connection/telephony/Telephony_Cfg.md) | 简体中文 \]

## 一、概述

本文档旨在指导您在 `openvela` 系统中正确配置 Telephony 服务，以启用蜂窝网络通信能力。启用此服务涉及多个关键组件的协同工作，包括 D-Bus 消息总线、oFono 电话协议栈、无线接口层（Radio Interface Layer, RIL）以及相关的库和工具。

配置过程主要分为三个核心步骤：

1. 内核配置（Kconfig）： 启用 Telephony 服务所需的所有内核组件和依赖库。
2. 资源文件配置： 为 D-Bus 等系统服务提供必要的配置文件。
3. 启动脚本配置： 在系统启动时按正确顺序加载和运行 Telephony 相关的守护进程。

## 二、Kconfig 配置

您需要通过 `menuconfig` 或直接修改 `defconfig` 文件来启用以下编译选项。这些选项按依赖模块进行分类。

### 1、D-Bus 配置

D-Bus 是 oFono 依赖的核心进程间通信（IPC）机制。

| 配置项                     | 说明                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------ |
| CONFIG_DBUS_DAEMON         | 启用 D-Bus 守护进程。                                                                                  |
| CONFIG_DBUS_MONITOR        | 启用 D-Bus 监视工具，用于调试。                                                                        |
| CONFIG_DBUS_SEND           | 启用 D-Bus 消息发送工具，用于调试。                                                                    |
| CONFIG_LIB_DBUS            | 启用 D-Bus 客户端库。                                                                                  |
| CONFIG_LIBC_EXECFUNCS      | 启用 atexit() 等函数支持。                                                                             |
| CONFIG_LIBC_MAX_EXITFUNS=4 | 设置 atexit() 可注册的最大函数数量。                                                                   |
| CONFIG_NET_LOCAL_SCM       | 启用通过 Unix Sockets 传递辅助数据的功能。                                                             |
| CONFIG_NET_RPMSG           | （可选） 当需要通过 RPMSG 进行跨核 D-Bus 通信时启用。 例如，CP 核上的蓝牙模块通过 D-Bus 与 AP 核通信。 |

### 2、GLIB 配置

oFono 依赖 GLib 提供的核心库功能。

| 配置项          | 说明           |
| --------------- | -------------- |
| CONFIG_LIB_GLIB | 启用 GLib 库。 |

### 3、oFono 配置

oFono 是实现蜂窝网络协议栈的核心中间件。

| 配置项                       | 说明                                                          |
| ---------------------------- | ------------------------------------------------------------- |
| CONFIG_OFONO                 | 启用 oFono 守护进程。                                         |
| CONFIG_OFONO_RILMODEM        | 启用 oFono 的 RIL 插件，用于和 openvela 的 RIL 守护进程通信。 |
| CONFIG_OFONO_STACKSIZE=32768 | 为 oFono 守护进程设置 32 KB 的栈空间。                        |
| CONFIG_SIGNAL_FD             | 启用 signalfd 机制，oFono 使用它进行信号处理。                |
| CONFIG_LIBC_DLFCN            | 启用动态链接库函数（如 dlopen），为 oFono 加载插件所必需。    |

### 4、GDBus 配置

GDBus 是 GLib 提供的 D-Bus 绑定库，用于简化 D-Bus 编程。

| 配置项                      | 说明                                               |
| --------------------------- | -------------------------------------------------- |
| CONFIG_LIB_DBUS             | 启用 D-Bus 库（已在 2.1 节中提及，此处为依赖项）。 |
| CONFIG_ALLOW_BSD_COMPONENTS | 允许 openvela 中包含 BSD 许可的组件。              |

### 5、Telephony API 配置

这是 openvela 提供的上层应用接口。

| 配置项                | 说明                               |
| --------------------- | ---------------------------------- |
| CONFIG_TELEPHONY      | 启用 openvela Telephony API 框架。 |
| CONFIG_TELEPHONY_TOOL | 启用 Telephony 命令行调试工具。    |

在 `menuconfig` 中进入 `CONFIG_TELEPHONY` 的子菜单，建议保持以下默认配置：

- **Active modem count:** 对于单卡产品，设置为 `1`。
- **Modem path:** 设置为 `/ril_0`，与 RIL 守护进程的路径匹配。

## 三、平台与资源文件配置

### 1、D-Bus 守护进程资源配置

D-Bus 守护进程启动时需要加载配置文件。请在您的产品目录下创建以下文件结构：

```Plain
.
└── src/
    └── etc/
        └── dbus-1/
            ├── system.conf   # D-Bus 系统总线配置文件
            └── system.d/     # 其他系统服务的 D-Bus 策略目录
```

`system.conf` 文件用于定义 D-Bus 守护进程监听的套接字。根据应用场景选择以下一种：

- **本地 AP 核通信：**

    ```XML
    <!-- 仅在 AP 核内部使用 D-Bus -->
    <listen>unix:path=/var/run/dbus/system_bus_socket</listen>
    ```

- **跨核（AP 与 CP）通信：**

    ```XML
    <!-- 允许其他核心（如 CP 核）通过 RPMSG 访问 D-Bus -->
    <listen>rpmsg:name=dbus_socket</listen>
    ```

### 2、openvela RIL 与 Modem 配置

此部分配置与具体的产品硬件平台强相关。您需要根据所选的 Modem 型号，在板级支持包（BSP）中启用并配置对应的 RIL 实现。

**关键点：**

- 确保已为您的 Modem 启用正确的驱动程序。
- `openvela` 的 RIL 实现需要与 oFono 的 `rilmodem` 插件正确对接。

## 四、启动脚本配置

为了在系统启动时自动运行 Telephony 服务，请将以下命令添加到 `rcS` 等启动脚本中。

```Shell
# 1. 启动 RIL 守护进程
#ifdef CONFIG_RILD
rild &
#endif

# 2. 启动 D-Bus 守护进程，为 oFono 提供 IPC 服务
#ifdef CONFIG_DBUS_DAEMON
dbus-daemon --system --nopidfile --nofork &
#ifdef CONFIG_DBUS_TEST
# 如果需要，可为用户会话启动另一个 D-Bus 实例
# dbus-daemon --session --nopidfile --nofork &
#endif
#endif

# 3. 配置并启动 oFono
#ifdef CONFIG_OFONO
#ifdef CONFIG_OFONO_RILMODEM

# 设置 oFono RIL 插件所需的环境变量
# 请根据实际产品需求调整这些值
set OFONO_RIL_DEVICE ril                   # RIL 设备名称
set OFONO_RIL_NUM_SIM_SLOTS 1              # SIM 卡槽数量
set OFONO_RIL_RAT_LTE 1                    # 启用 LTE 无线接入技术
set OFONO_RIL_TRACE 1                      # 启用 RIL 调试跟踪
set OFONO_CALL_BARRING_INTERFACE_SUPPORT 0 # 禁用呼叫限制接口
set OFONO_CELL_BROADCAST_INTERFACE_SUPPORT 0 # 禁用小区广播接口
set OFONO_PHONEBOOK_INTERFACE_SUPPORT 0    # 禁用电话本接口
set OFONO_STK_INTERFACE_SUPPORT 0          # 禁用 SIM 卡工具包接口
set OFONO_SUPPLEMENTARY_SERVICES_INTERFACE_SUPPORT 0 # 禁用补充服务接口
set OFONO_FIVE_SIGNAL_LEVEL_SUPPORT 0      # 禁用五级信号强度支持
set OFONO_CALL_VOLUME_INTERFACE_SUPPORT 0  # 禁用通话音量接口
set OFONO_GPRS_CONTEXT_TYPE_SUPPORT internet,ims # 支持的GPRS上下文类型
#endif

# 启动 oFono 守护进程
#ifdef CONFIG_INTERPRETERS_WAMR
# 如果使用 WAMR (WebAssembly Micro Runtime)，则以 AOT 模式启动
iwasm --disable-bounds-checks --max-threads=1 /etc/ofonod.aot &
#else
# 否则，直接启动原生可执行文件
ofonod &
#endif
#endif
```

**说明：**

- **启动顺序：** 必须确保 `rild` 和 `dbus-daemon` 在 `ofonod` 之前启动。
- **环境变量：** `OFONO_*` 环境变量用于在启动时配置 oFono RIL 插件的行为。请根据您的产品定义进行调整。

完成以上所有配置并编译烧录固件后，`openvela` 系统将具备基础的蜂窝通信能力。您可以使用 `telephony-tool` 等工具进行功能验证。
