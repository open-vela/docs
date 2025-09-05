# 系统日志 (Syslog) 深度解析

\[ [English](../../../../en/device_dev_guide/kernel/logging/syslog.md) | 简体中文 \]

## 一、概述

`syslog` 是 openvela 系统中用于记录内核与应用日志的标准框架。它提供了一套灵活、可扩展的日志解决方案，能够捕获系统运行时的关键信息。

**核心特性:**

- **分级日志 (Graded Logging)**：支持从 `LOG_DEBUG` (调试)到 `LOG_EMERG` (紧急)等多种日志优先级，便于分类和过滤。
- **多通道输出 (Multi-Channel Output)**：允许将日志同时路由到多个目的地，例如物理串口、内存缓冲区 (RAM log)、文件系统或远程处理器。
- **灵活的格式化 (Flexible Formatting)**：可以自动为每条日志添加时间戳、CPU ID、进程/线程 ID (PID) 等丰富的上下文信息。

## 二、API 参考与使用规范

### 1、应用层 API

应用开发者使用 `syslog()` 函数向系统提交日志。

**函数原型**:

```C
#include <syslog.h>
void syslog(int priority, const char *format, ...);
```

**参数**:

- `priority`：日志的优先级，例如 `LOG_INFO`, `LOG_ERR` 等。
- `format`：格式化字符串，与 `printf` 语法兼容。

### 2、内核层使用规范

内核代码（包括驱动）**必须**使用 `include/debug.h` 中提供的日志宏，例如 `_info()`, `_warn()`, `_err()` 等，**不应**直接调用 `syslog()` 函数。

- **优势**: 这些宏是可配置的，在编译时能根据 Kconfig 选项被彻底移除。
- **目的**: 这种机制能有效避免在生产固件中引入不必要的日志代码，从而减小固件体积并提升系统性能。

## 三、核心架构：内部工作流与数据流

`syslog` 框架的核心是一个分发机制，它接收日志，进行格式化，然后通过不同的通道将日志路由到最终目的地。其整体框架如下图所示：

![img](./figures/001.svg)

### 1、核心工作流程

1. 接收与过滤：`syslog()` 或内核日志宏被调用，系统首先根据当前配置的日志级别过滤消息。
2. 格式化：`nx_vsyslog()` 函数根据 Kconfig 配置为日志添加前缀、时间戳、PID 等元数据。
3. 输出到流：所有格式化操作最终汇集到 `lib_vsprintf()`，它将格式化后的字符串逐字符写入一个抽象的输出流 (stream)。
4. 分发到通道：`syslog` 的输出流是一个特殊的多路分发器。它会将接收到的每个字符分发给所有已注册的日志通道 (channel)。
5. 驱动输出：每个通道负责通过其底层驱动将日志数据输出到具体介质，例如 UART、RAM 缓冲区或文件。

### 2、调用栈概览

```Bash
// 应用/内核日志调用
syslog() / _info()
    |
    v-- 格式化与分发
nx_vsyslog()
    |
    v-- C库标准格式化
lib_vsprintf()
    |
    v-- 写入 syslog 输出流
stream_putc() --> syslogstream_putc()
    |
    v-- 遍历所有已注册通道并区分上下文
syslog_putc()
    |
    v-- 调用通道驱动的输出函数
g_syslog_channel[i]->sc_ops->sc_putc()    // 任务上下文
g_syslog_channel[i]->sc_ops->sc_force()   // 中断上下文
```

### 3、动态通道注册机制

系统中的任何模块（如驱动）都可以通过 `syslog_channel()` 函数注册一个自定义的日志输出通道。

#### 注册接口

```C
// 定义于: drivers/syslog/syslog_channel.c
int syslog_channel(FAR struct syslog_channel_s *channel);
```

注册时，通道驱动必须提供一个操作函数集（`ops`），它定义了通道如何处理日志数据。

#### 通道操作接口 (`struct syslog_channel_ops_s`)

```C
// 定义于: include/nuttx/syslog/syslog.h
struct syslog_channel_ops_s {
  // 用于任务上下文的字符输出 (可阻塞)
  syslog_putc_t  sc_putc;
  // 用于中断上下文的字符输出 (必须非阻塞、可重入)
  syslog_putc_t  sc_force;
  // 强制刷新缓冲区 (例如系统崩溃时调用)
  syslog_flush_t sc_flush;
  // 优化用：一次性写入多个字节
  syslog_write_t sc_write;
  // 通道关闭回调
  syslog_close_t sc_close;
};
```

#### 工作原理

1. 驱动调用：在驱动初始化时，会构建一个 `syslog_channel_s` 结构体，并填充其操作函数集 `ops`。
2. 注册到核心：驱动调用 `syslog_channel()` 函数，将该结构体的指针传递给 `syslog` 核心。
3. 加入列表：`syslog` 核心将接收到的通道指针存入一个全局数组 `g_syslog_channel[]` 中。`CONFIG_SYSLOG_MAX_CHANNELS` 定义了此数组的大小。

    > **注意**: `CONFIG_SYSLOG_MAX_CHANNELS` 定义了此数组的大小，即系统支持的最大通道数量。

#### 关键设计：上下文安全

`syslog` 框架能够自动检测当前的执行上下文（任务或中断）。

- 在**任务上下文**中，它调用 `sc_putc`。
- 在**中断上下文**中，它调用 `sc_force`，以避免在中断服务程序中发生阻塞或资源竞争。

因此，通道驱动开发者必须确保其 `sc_force` 函数的实现是**非阻塞且可重入**的，这是保证系统实时性和稳定性的关键。

### 4、底层数据流：缓冲与直写

数据从 `lib_vsprintf` 到物理通道的输出路径，有两种核心工作模式，由 `CONFIG_SYSLOG_BUFFER` 控制。如下图所示：

![img](./figures/002.png)

#### 模式 1：启用缓冲区 (`CONFIG_SYSLOG_BUFFER=y`)

此模式为默认和推荐选项，旨在通过减少 I/O 操作次数来提升性能。

1. 写入缓冲区: 格式化后的字符被逐一添加到内部的 I/O 缓冲区。
2. 批量刷写: 当缓冲区被填满或遇到换行符时，`syslogstream_flush()` 函数被触发。
3. 高效写入: 该函数会遍历所有已注册的通道，并调用每个通道的 `sc_write()` 方法，将整个缓冲区的数据一次性写入。这种方式显著降低了高频日志输出时的函数调用开销。

#### 模式 2：直接输出 (无 `CONFIG_SYSLOG_BUFFER`)

在此模式下，系统不使用中间缓冲区，每个字符都会被立即发送。

1. 直接分发：`stream_putc` 直接调用 `syslog_putc()`。
2. 上下文感知：`syslog_putc()` 函数会检查当前的执行上下文：

    - 如果处于**任务上下文**，它会调用通道驱动的 `sc_putc()` 函数。
    - 如果处于**中断上下文**，它会调用通道驱动的 `sc_force()` 函数，该函数必须是非阻塞的。

3. 逐一发送：每个字符都会触发一次对所有通道的遍历和函数调用。

> **说明**：即使在直接输出模式下，`syslog` 框架依然通过独立的**中断日志缓冲区(**`CONFIG_SYSLOG_INTBUFFER`) 来保证中断日志的原子性和非阻塞性，防止日志内容交叉错乱，可参见[中断中的日志记录](#七中断中的日志记录-logging-in-interrupts)。

## 四、日志控制与过滤

`syslog` 框架提供了编译时和运行时两种灵活的日志控制机制，允许开发者精确地管理日志的输出内容和目标。

### 1、日志优先级

系统定义了 8 个标准的日志优先级，从高到低依次为：

| 优先级 | C语言宏     | 描述                                                  |
| ------ | ----------- | ----------------------------------------------------- |
| 最高   | LOG_EMERG   | 系统无法使用 (System is unusable)                     |
|        | LOG_ALERT   | 必须立即采取行动 (Action must be taken immediately)   |
|        | LOG_CRIT    | 严重情况 (Critical conditions)                        |
|        | LOG_ERR     | 错误情况 (Error conditions)                           |
|        | LOG_WARNING | 警告情况 (Warning conditions)                         |
|        | LOG_NOTICE  | 正常但重要的事件 (Normal, but significant, condition) |
|        | LOG_INFO    | 信息性消息 (Informational message)                    |
| 最低   | LOG_DEBUG   | 调试级别消息 (Debug-level message)                    |

### 2、编译时过滤：通过 Kconfig 控制

编译时过滤是控制固件大小和性能的**最有效**手段。通过在 Kconfig 中关闭特定模块或级别的日志宏，相关的日志代码会从最终的二进制文件中被彻底移除。

- **通用日志宏**：这些宏在整个内核中通用。

    - `CONFIG_DEBUG_INFO`: 控制 `_info()`
    - `CONFIG_DEBUG_WARN`: 控制 `_warn()`
    - `CONFIG_DEBUG_ERROR`: 控制 `_err()`
    - `CONFIG_DEBUG_ASSERT`: 控制 `_alert()` 和 `ASSERT()`

- **子系统专用宏**：为了实现更精细的控制，许多内核子系统（如调度器、内存管理）提供了专用的日志宏。这允许开发者在调试特定模块时，只开启该模块的日志，而保持其他部分安静。

    - `CONFIG_DEBUG_SCHED_INFO`: 控制 `sinfo()` (调度器信息)
    - `CONFIG_DEBUG_MM_ERROR`: 控制 `merr()` (内存管理错误)

### 3、运行时控制：`setlogmask` 命令

`setlogmask` 是一个强大的 shell 命令，它允许用户在系统运行时动态调整日志行为，无需重新编译固件。

**必要配置**：

```Bash
# 启用 setlogmask 命令
CONFIG_SYSTEM_SETLOGMASK=y

# 启用通过 ioctl 控制日志通道的功能
CONFIG_SYSLOG_IOCTL=y
```

`setlogmask` 命令主要有两个功能：设置日志过滤级别和管理输出通道。

#### 功能 1：设置日志过滤级别

此功能用于设置系统输出的**最低**日志优先级。只有优先级**等于或高于**设定级别的日志才会被输出。

**用法示例**：

```Bash
# 查看帮助和可用级别
nsh> setlogmask -h
Usage: setlogmask <d|i|n|w|e|c|a|r>
Where: d=DEBUG, i=INFO, ..., r=EMERG

# 设置为 DEBUG 级别，输出所有日志
nsh> setlogmask d

# 设置为 ERROR 级别，仅输出 LOG_ERR 及更高优先级的日志
nsh> setlogmask e
```

#### 功能 2：动态管理输出通道

此功能允许用户动态地启用或禁用已注册的日志通道，从而控制日志的输出目的地。

**用法示例**：

```Bash
# 查看所有已注册通道及其当前状态
nsh> setlogmask list
Channels:
  default: enable
  ramlog: enable

# 临时关闭到物理串口的日志输出（通常是 'default' 通道）
nsh> setlogmask disable default

# 再次查看，确认通道状态已改变
nsh> setlogmask list
Channels:
  default: disable
  ramlog: enable

# 重新启用串口日志输出
nsh> setlogmask enable default
```

## 五、日志多通道配置

内核日志系统支持将日志输出到多个通道，如终端、内存、文件系统等。开发者可以根据不同的调试和产品需求，灵活地组合和配置这些通道。

### 1、通道概览与选择

为了帮助您快速选择合适的日志通道，下表总结了各个通道的特点和适用场景：

| 通道 (Channel) | 主要配置宏            | 特点与核心用途                                                                     | 限制与注意事项                                             |
| -------------- | --------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Default        | CONFIG_SYSLOG_DEFAULT | 通过底层 up_putc 接口输出，适用于系统早期启动阶段的调试。中断安全。                | 功能最简单，通常输出到第一个串口。可能会与printf输出混合。 |
| RAM Log        | CONFIG_RAMLOG_SYSLOG  | 写入内存环形缓冲区 (Ring Buffer)，速度极快，对系统性能影响小。                     | 日志在设备重启后会丢失。缓冲区大小有限。                   |
| File Log       | CONFIG_SYSLOG_FILE    | 将日志持久化存储到文件，支持日志轮转 (Rotation)，便于事后分析。                    | 依赖文件系统，不适用于系统启动初期的日志记录。             |
| Device Log     | CONFIG_SYSLOG_CHAR    | 将日志写入指定的字符设备文件（如 /dev/ttyS1），灵活性高。                          | 依赖设备驱动初始化。非中断安全，因其内部有锁机制。         |
| Console Log    | CONFIG_SYSLOG_CONSOLE | Device Log 的一种特例，固定输出到 /dev/console。                                   | 同 Device Log，依赖驱动且非中断安全。                      |
| RPMSG          | CONFIG_SYSLOG_RPMSG   | 用于多核系统，将从核 (Remote Core) 的日志通过 RPMSG 框架发送给主核 (Master Core)。 | 依赖 RPMSG 通信框架的正常运行。                            |
| USB CDC-ACM    | CONFIG_SYSLOG_CDCACM  | 通过 USB 虚拟串口 (Virtual COM Port) 输出日志，方便连接PC调试。                    | 依赖 USB 协议栈的初始化。                                  |

### 2、通道详细配置

#### Default 通道 (Low-Level Serial Output)

这是最基础的日志通道，它绕过上层驱动，直接调用底层的字符输出函数 (`up_putc`)，通常用于输出到串口。

- **适用场景**: 捕获系统启动早期（在设备驱动完全初始化之前）的日志。

- **核心配置**:

    ```Makefile
    # 启用 Default 通道
    CONFIG_SYSLOG_DEFAULT=y
    
    # 确保底层 low-level putc 接口已实现
    CONFIG_ARCH_LOWPUTC=y
    ```

- **工作原理**: 该通道直接调用 `up_putc` 函数，该函数通常通过轮询硬件寄存器的方式发送数据，并会屏蔽中断，因此是中断安全的。

#### RAM Log 通道 (In-Memory Buffer)

将日志高速写入预先分配的内存缓冲区。

- **适用场景**: 需要高性能日志记录，且对系统实时性影响要求苛刻的场景。常用于性能分析或问题复现后从内存中导出日志。

- **核心配置**:

    ```Makefile
    # 启用 RAMLOG 功能
    CONFIG_RAMLOG=y
    # 将 RAMLOG 作为 syslog 的一个通道
    CONFIG_RAMLOG_SYSLOG=y
    # 设置缓冲区大小 (单位: 字节)，写满后会覆盖旧日志
    CONFIG_RAMLOG_BUFSIZE=1024
    # (可选) 将缓冲区放置在指定的内存 section
    # RAMLOG_BUFFER_SECTION=".bss"
    ```

- **注意**: 存储在 RAM 中的日志是易失的，设备断电或重启后将全部丢失。

#### File Log 通道 (Persistent Storage)

将日志保存到文件系统中，实现持久化存储。

- **适用场景**: 需要在设备运行后，对历史日志进行长期保存和分析的场景。

- **核心配置**:

    ```Makefile
    # 启用 File Log 通道
    CONFIG_SYSLOG_FILE=y
    ```

- **使用方法**: 此通道默认不激活。应用层需要在文件系统挂载成功后，通过调用 `syslog_file_channel()` 函数来初始化并指定日志文件路径。

- **高级选项**:

    | 配置项                 | 描述                                                                             | 默认值   |
    | ---------------------- | -------------------------------------------------------------------------------- | -------- |
    | SYSLOG_FILE_SEPARATE   | 若为 y，每次重启后向日志文件写入一个空行，以区分不同启动会话的日志。             | n        |
    | SYSLOG_FILE_ROTATIONS  | 启用日志轮转。当文件达到大小限制时，创建新文件。此值定义了保留的旧日志文件数量。 | 0 (禁用) |
    | SYSLOG_FILE_SIZE_LIMIT | 启用轮转时，单个日志文件的最大体积 (单位: 字节)。                                | 524288   |

#### Device / Console 通道 (Character Device Output)

将日志作为标准数据流写入一个字符设备文件。

- 适用场景: 将日志重定向到特定的串口、虚拟终端或其他字符设备。

- 配置方式:

    - 输出到指定设备 (如 `/dev/ttyS1`):

        ```Makefile
        # 启用字符设备通道
        CONFIG_SYSLOG_CHAR=y
        
        # 指定目标设备路径
        CONFIG_SYSLOG_DEVPATH="/dev/ttyS1"
        ```

    - 输出到系统控制台 (`/dev/console`):

        ```Makefile
        # 启用 Console 通道
        CONFIG_SYSLOG_CONSOLE=y
        ```

- 工作原理: 此通道通过标准的文件 I/O (`write()`) 将日志写入设备节点。因为它会获取设备锁，所以**不能在中断上下文中使用**，否则可能导致系统死锁。

- 特殊配置 `CONSOLE_SYSLOG`:

    - 作用: 这个宏会将 `/dev/console` 的底层实现**替换**为 syslog 系统。这意味着所有通过 `printf` 等标准库函数输出到控制台的内容，都会被重定向到所有已启用的 syslog 通道（如 File, RAM Log 等）。
    - **注意**: `CONFIG_CONSOLE_SYSLOG` 与 `CONFIG_SYSLOG_CONSOLE` 是**互斥**的，不能同时启用。

#### RPMSG 通道 (Multi-Core Logging)

用于多核处理器架构，允许从核（Remote Core）将日志发送到主核（Primary Core）。

- 适用场景: 在非对称多处理（AMP）系统中，统一收集和管理所有核心的日志。

- 核心配置:

    - 主核 (接收端) 配置:

        ```Makefile
        CONFIG_SYSLOG_RPMSG_SERVER=y    
        ```

        并在板级初始化代码中调用 `syslog_rpmsg_server_init()`。

    - 从核 (发送端) 配置:

        ```Makefile
        CONFIG_SYSLOG_RPMSG=y
        CONFIG_SYSLOG_RPMSG_SERVER_NAME="ap" # RPMSG 服务端点名称
        ```

        并在板级初始化代码中调用 `syslog_rpmsg_init()` 和 `syslog_rpmsg_init_early`。

- 参考文档：[Rpmsg Syslog]()

#### USB CDC-ACM 通道 (USB Virtual COM Port)

将日志通过 USB 接口输出，PC 端会将其识别为一个虚拟串口。

- **适用场景**: 设备没有物理串口，或希望通过 USB 方便地连接电脑查看日志。
- **核心配置**: `CONFIG_SYSLOG_CDCACM=y`

## 六、日志输出格式化 (Log Output Formatting)

为了便于调试和分析，您可以在原始日志消息前自动添加各种上下文信息，如时间戳、线程ID等。

以下是可用的格式化选项，您可以根据需要组合使用：

| 分类       | 配置宏                                     | 描述                                                                                  |
| ---------- | ------------------------------------------ | ------------------------------------------------------------------------------------- |
| 时间戳     | CONFIG_SYSLOG_TIMESTAMP                    | (主开关) 在每条日志前添加一个时间戳。默认输出的是系统启动以来的原始时间单位 (ticks)。 |
|            | CONFIG_SYSLOG_TIMESTAMP_REALTIME           | 将时间戳解析为真实世界时间（Wall-clock time）。依赖于系统已正确设置 RTC。             |
|            | CONFIG_SYSLOG_TIMESTAMP_FORMATTED          | 启用自定义格式化时间字符串的功能。                                                    |
|            | CONFIG_SYSLOG_TIMESTAMP_LOCALTIME          | （依赖 _REALTIME）将时间以本地时区（而非UTC）显示。                                   |
|            | CONFIG_SYSLOG_TIMESTAMP_FORMAT             | （依赖 _FORMATTED）定义时间格式，例如 "%y/%m/%d %H:%M:%S"。                           |
|            | CONFIG_SYSLOG_TIMESTAMP_FORMAT_MICROSECOND | （依赖 _FORMATTED）在格式化时间后追加毫秒或微秒值，提升时间精度。                     |
|            | CONFIG_SYSLOG_TIMESTAMP_BUFFER             | （高级/内部）定义用于暂存格式化时间戳字符串的缓冲区大小。一般无需修改。               |
| 日志元数据 | CONFIG_SYSLOG_PRIORITY                     | 在日志中显示其优先级（如 [ERR], [WARN], [INFO]）。                                    |
|            | CONFIG_SYSLOG_PROCESSID                    | 在日志中显示当前任务（线程）的 PID。                                                  |
|            | CONFIG_SYSLOG_PROCESS_NAME                 | 在日志中显示当前任务（线程）的名称。                                                  |
| 自定义前缀 | CONFIG_SYSLOG_PREFIX                       | (主开关) 为所有日志添加一个固定的字符串前缀。                                         |
|            | CONFIG_SYSLOG_PREFIX_STRING                | 定义要添加的具体前缀内容，例如 "ap:" 或 "core0:"。                                    |
| 视觉效果   | CONFIG_SYSLOG_COLOR_OUTPUT                 | 根据日志的优先级以不同颜色显示。<br> **注意**：这会向输出流中添加颜色控制字符。       |

### 1、配置示例

假设您希望日志包含自定义前缀 "ap"，显示优先级和进程 ID，并以 "年/月/日 时:分:秒.毫秒" 的格式显示本地时间。

```Makefile
# --- 时间戳配置 ---
CONFIG_SYSLOG_TIMESTAMP=y
CONFIG_SYSLOG_TIMESTAMP_REALTIME=y
CONFIG_SYSLOG_TIMESTAMP_FORMATTED=y
CONFIG_SYSLOG_TIMESTAMP_FORMAT="%y/%m/%d %H:%M:%S"
CONFIG_SYSLOG_TIMESTAMP_FORMAT_MICROSECOND=y
CONFIG_SYSLOG_TIMESTAMP_LOCALTIME=y

# --- 元数据与前缀配置 ---
CONFIG_SYSLOG_PRIORITY=y
CONFIG_SYSLOG_PROCESSID=y
CONFIG_SYSLOG_PREFIX=y
CONFIG_SYSLOG_PREFIX_STRING="ap"
```

**最终输出效果可能如下所示:**

`ap [INFO][12] 23/10/26 15:30:05.123: This is a sample log message`.

## 七、中断中的日志记录 (Logging in Interrupts)

在中断服务程序（ISR）中打印日志需要特殊处理，以避免影响系统实时性并保证日志的完整性。

### 问题

1. **执行时间过长**：在 ISR 中直接进行 I/O 操作（如写串口）会占用宝贵的 CPU 时间，可能导致错过其他更重要的中断。
2. **日志交错**：如果 ISR 的日志和普通任务的日志同时输出到 `default_channel` 或 `ramlog_channel`，它们的内容可能会混杂在一起，导致日志信息损坏或无法阅读。
3. **功能限制**：`dev_channel`（包括 File 和 Console 通道）内部包含锁机制，**严禁**在 ISR 中使用，否则会造成系统死锁。

### 解决方案：中断日志缓冲区

为了解决上述问题，系统提供了一个专用的**中断日志缓冲区 (****`SYSLOG_INTBUFFER`****)**。

**核心配置:**

```Makefile
# 启用中断日志缓冲区
CONFIG_SYSLOG_INTBUFFER=y

# 设置缓冲区大小 (单位: 字节)
CONFIG_SYSLOG_INTBUFSIZE=512
```

### 工作原理：先暂存，后刷出

1. **在 ISR 中**: 当 `syslog()` 在中断上下文中被调用时，它**不会**立即将日志发送到最终通道。而是将日志内容快速地暂存到中断缓冲区中，然后 ISR 就可以立刻返回。这个过程非常快，对系统实时性影响极小。

2. **在任务中**: 当下一次 `syslog()` 在正常的任务（非中断）上下文中被调用时，系统会执行一个额外的步骤：它会先检查中断缓冲区中是否有待处理的日志。如果有，系统会**先将缓冲区中的所有日志完整地刷出（Flush）到**最终通道，然后再处理当前任务发出的新日志。

通过这种“先暂存，后刷出”的机制，既保证了 ISR 的快速执行，又确保了所有日志（包括中断和任务的）都按正确的时序输出，不会发生交错。

## 八、相关文档

- [printf 函数使用规范](./printf.md)
- [日志管理与故障排查](./troubleshooting.md)
