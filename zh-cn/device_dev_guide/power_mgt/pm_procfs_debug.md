# 电源管理 Procfs 调试指南

\[ [English](../../../en/device_dev_guide/power_mgt/pm_procfs_debug.md) | 简体中文 \]

本文档指导开发者如何使用 openvela 系统中 Procfs (`/proc` 文件系统) 提供的电源管理 (PM) 接口。通过此接口，您可以实时监控每个电源域 (Power Domain) 的功耗状态分布，并诊断 `Wakelock` 的使用情况，是功耗优化与问题定位的强大工具。

**前置条件**：系统必须在 Kconfig 中启用 Procfs (`CONFIG_FS_PROCFS=y`)。

## 一、访问 PM 调试信息

您可以通过两种方式访问 PM 的调试信息：使用便捷的 `pmconfig` 命令，或直接读取 Procfs 中的文件。

### 方式 1：使用 `pmconfig` 命令 (推荐)

`pmconfig` 是一个封装好的命令行工具，它能聚合显示系统中所有电源域的状态和 `Wakelock` 信息，是查看 PM 概览的首选方法。

在目标设备的 Shell 中执行：

```Bash
pmconfig
```

### 方式 2：直接访问 Procfs 文件

您也可以通过 `cat` 命令直接读取底层的 Procfs 文件。这种方法在需要脚本化处理或远程访问（如通过 `adb shell`）时非常有用。PM 信息文件位于 `/proc/pm/` 目录下，并按电源域 (Domain) 索引进行区分。

- **状态文件**: `/proc/pm/state<domain_id>`
- **Wakelock 文件**: `/proc/pm/wakelock<domain_id>`

**示例：在多核系统中查看各核心的 PM 信息**

假设系统包含一个应用处理器 (AP) 和一个通信处理器 (CP)，您可以通过以下方式查看：

```Bash
# 在模拟器或 QEMU 等无挂载点的环境中，路径可能为 /proc/pm/...
# 以下示例基于一个将远程核心文件系统挂载到 /mnt 的系统

# 查看本地核心 (AP) 的 Domain 0 和 Domain 1 信息
cat /mnt/ap/pm/state0
cat /mnt/ap/pm/wakelock0
cat /mnt/ap/pm/state1
cat /mnt/ap/pm/wakelock1

# 查看远程核心 (CP) 的 Domain 0 信息
cat /mnt/cp/pm/state0
cat /mnt/cp/pm/wakelock0
```

## 二、解读 Procfs 输出

本节详细解释 `state` 和 `wakelock` 文件内容的含义。

### 1、电源状态统计 (`/proc/pm/state<N>`)

此文件展示了自系统启动以来，各个电源状态下所花费的时间。

**示例输出 (`/proc/pm/state0`)**：

```Bash
//             执行时间         睡眠时间    该state下执行+睡眠时间
DOMAIN0           WAKE         SLEEP         TOTAL
normal         14s 01%       20s 02%       34s 04%
idle            0s 00%        0s 00%        0s 00%
standby         0s 00%        0s 00%        0s 00%
sleep           0s 00%      712s 95%      712s 95%
```

**字段说明**：

| **字段**              | **描述**                                                                                                                     |
| :-------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| `DOMAIN<N>`           | 表头，指明这是哪个电源域的统计数据。                                                                                         |
| `normal`, `idle`, ... | 系统支持的各个电源状态。                                                                                                     |
| `WAKE`                | **活动时间**：CPU 在此状态下**执行代码**的总时间。                                                                           |
| `SLEEP`               | **休眠时间**：CPU 在此状态下**处于低功耗（如 WFI）等待**的总时间。 <br>对于 `sleep` 状态，此值是衡量系统节能效果的关键指标。 |
| `TOTAL`               | **总时间**：`WAKE` 时间与 `SLEEP` 时间之和，即在该状态下停留的总时长。                                                       |
| **(百分比)**          | 该状态的总时间占系统运行总时间的百分比。                                                                                     |

**分析示例**： 以上输出显示，`DOMAIN0` 自启动以来，有 95% 的时间都成功地进入了 `PM_SLEEP` 状态，这表明系统的电源管理策略运行良好，实现了有效的节能。

### 2、Wakelock 统计 (`/proc/pm/wakelock<N>`)

此文件列出了指定电源域中所有已注册的 `Wakelock` 及其当前状态和历史数据。

示例输出 (`/proc/pm/wakelock0`)：

```Bash
//wakelock   state   当前stay次数  总stay时间
DOMAIN0      STATE     COUNT      TIME
system       normal        0       10s
system       idle          0       10s
system       standby       0       10s
system       sleep         0       10s
rptun-tee    idle          0        0s
i2c          normal        0        1s
rptun-cp     idle          0        0s
rptun-sensor idle          0        1s
rptun-audio  idle          0        0s
gpu          normal        0        8s
```

**字段说明**：

| **字段**    | **描述**                                                                                                                         |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------- |
| `DOMAIN<N>` | 表头，指明这是哪个电源域的 `Wakelock` 列表。                                                                                     |
| `wakelock`  | `Wakelock` 的名称，在调用 `pm_wakelock_init` 时指定。                                                                            |
| `STATE`     | 此 `Wakelock` 生效时，将系统维持的**最低功耗状态**。例如，`normal` 表示它会阻止系统进入任何低功耗状态。                          |
| `COUNT`     | **当前引用计数**。<br>如果此值**大于 0**，表示该锁**当前正被持有**，正在阻止系统进入更深的休眠状态。<br>这是排查耗电问题的关键。 |
| `TIME`      | **累计持有时间**。<br>自系统启动以来，此 `Wakelock` 被持有的总时长。<br>此值有助于识别哪些模块是历史上最主要的**耗电大户**。     |

**分析示例**： 以上输出表明，在 `DOMAIN0` 中：

- 当前**没有**任何 `Wakelock` 处于活动状态（所有 `COUNT` 均为 0）。
- 从历史上看，`system`、`i2c` 和 `gpu` 驱动或模块是主要的 `Wakelock` 使用者，累计持有时间分别为 10s、1s 和 8s。如果系统无法休眠，应首先检查这些模块的 `COUNT` 值。
