# 日志系统

## 一、syslog

### 1、函数声明

```C
void syslog(int priority, const char *format, ...);
```

### 2、注意事项

内核中禁止直接调用 `syslog` 输出日志。在内核中，请使用 `include/debug.h` 中定义的日志宏，或者根据需求自定义类似的宏以确保日志的统一性和规范性。

### 3、功能概述

`syslog` 支持多等级、多通道的日志打印，能够以带有时间戳、CPU ID 和进程 ID（PID）的格式输出日志。其整体框架如下图所示：

![img](./figures/001.svg)

### 4、工作流程

1. `syslog` 通过 `log level filter` 对日志进行过滤。
2. 根据指定的格式对日志进行包装，并将其发送至 `lib_vsprintf`。
3. `lib_vsprintf` 将数据发送到对应的 `stream`（数据流）。
4. `syslog stream` 支持多种 `channel`，例如：
    - `default_channel`
    - `ramlog_channel`
    - `rpmsg_channel`
    - `dev_channel`

5. 各个 `channel` 使用对应的驱动程序，将日志输出到目标设备或介质（如 `uart`、`ram`、`file` 等）。

### 5、日志优先级

`syslog` 支持以下日志优先级（`log level`）：

```Plain%20Text
LOG_EMERG
  system is unusable
LOG_ALERT
  action must be taken immediately
LOG_CRIT
  critical conditions
LOG_ERR
  error conditions
LOG_WARNING
  warning conditions
LOG_NOTICE
  normal, but significant, condition
LOG_INFO
  informational message
LOG_DEBUG
  debug-level message
```

### 6、内核中使用的日志宏

下面每个宏选择配置一个内核 `log` 等级。例如：

关闭 `CONFIG_DEBUG_INFO` 宏后，内核中所有通过 `_info` 函数打印的 `log` 将被过滤。

```C
// include/debug.h和include/syslog.h
CONFIG_DEBUG_ASSERT  ->  _alert
CONFIG_DEBUG_ERROR   ->  _err
CONFIG_DEBUG_WARN    ->  _warn
CONFIG_DEBUG_INFO    ->  _info
```

### 7、内核模块中的日志打印

在内核的各模块中，支持日志等级打印，与 `syslog` 的日志等级相对应。以下是关于日志打印的建议和配置说明。

#### 7.1 驱动开发者

请使用各模块提供的专用打印函数，以确保日志输出的规范性和一致性。

#### 7.2 应用开发者

可以直接使用 `syslog(LOG_LEVEL, ...)` 进行日志打印，例如：

```C
CONFIG_DEBUG_SCHED_ERROR  ->  serr
CONFIG_DEBUG_SCHED_WARN   ->  swarn
CONFIG_DEBUG_SCHED_INFO   ->  sinfo
CONFIG_DEBUG_MM_ERROR     ->  merr
CONFIG_DEBUG_MM_WARN      ->  mwarn
CONFIG_DEBUG_MM_INFO      ->  minfo
```

#### 7.3 日志多通道配置

内核日志支持多种输出通道，包括终端、串口、内存等。开发者可以根据需求选择合适的配置，灵活调整日志的输出方式、内容和格式。

##### 单核打印到终端或串口

如果需要将日志打印到终端或串口，请启用以下配置：

```Makefile
CONFIG_SYSLOG_DEFAULT=y      # 默认配置，输出到串口
```

##### 打印到内存

如果需要将日志打印到内存，请配置以下选项：

```Makefile
CONFIG_RAMLOG=y                # 启用 RAMLOG  
CONFIG_RAMLOG_SYSLOG=y         # 启用 RAMLOG 的 syslog 支持  
CONFIG_RAMLOG_BUFSIZE=1024     # RAMLOG 缓冲区大小  
CONFIG_RAMLOG_OVERWRITE=y      # 缓冲区满后覆盖旧日志  
RAMLOG_BUFFER_SECTION=".bss"   # 将缓冲区放置到固定 section
```

##### 打印到文件

如果需要将日志打印到文件，请配置以下选项：

```Makefile
CONFIG_SYSLOG_FILE=y           # 启用日志文件输出
```

##### 打印到设备文件

如果需要将日志打印到指定设备文件，例如 `/dev/ttyS1`，请配置以下选项：

```Makefile
CONFIG_SYSLOG_CONSOLE=y             # 打印日志到 /dev/console  
CONFIG_SYSLOG_CHAR=y                # 打印日志到指定设备文件，例如 /dev/ttyS1  
CONFIG_SYSLOG_DEVPATH="/dev/ttyS1"  # 指定设备文件路径
```

##### 打印到主核 CPU

如果需要将日志打印到主核 CPU 或远程 CPU，请配置以下选项：

```Makefile
# 主核CPU配置
CONFIG_SYSLOG_RPMSG_SERVER=y

# 远程CPU配置
CONFIG_SYSLOG_RPMSG=y
CONFIG_SYSLOG_RPMSG_SERVER_NAME="ap"
```

##### 打印到 USB CDCACM

```Makefile
CONFIG_SYSLOG_CDCACM=y     配置CDCACM做为SYSLOG的一个通道
```

##### 时间戳配置

日志支持多种时间戳格式，可以通过以下配置项启用和调整。

```Makefile
CONFIG_SYSLOG_TIMESTAMP=y                # 启用时间戳，默认打印 UTC 时间，以微秒 (us) 为单位  
CONFIG_SYSLOG_TIMESTAMP_REALTIME=y       # 打印本地时间 (localtime)  

CONFIG_SYSLOG_TIMESTAMP_FORMAT="%H:%M:%S"  # 自定义时间格式：时分秒  
# CONFIG_SYSLOG_TIMESTAMP_FORMAT="%y/%m/%e %H:%M:%S"  # 自定义时间格式：年月日 时分秒  

CONFIG_SYSLOG_TIMESTAMP_LOCALTIME=y      # 启用本地时间显示  
CONFIG_SYSLOG_TIMESTAMP_FORMATTED=y      # 格式化时间戳输出
```

##### 颜色打印

> 注意
>
> 请不要在自定义日志（LOG）中直接添加颜色字符。

```Makefile
CONFIG_SYSLOG_COLOR_OUTPUT=y
```

##### 附加日志信息

```Makefile
CONFIG_SYSLOG_PREFIX=y        # 打印 CPU 信息  
CONFIG_SYSLOG_PROCESSID=y     # 打印进程 ID (PID)  
CONFIG_SYSLOG_PRIORITY=y      # 打印日志等级  
CONFIG_SYSLOG_BUFFER=y        # 启用日志缓冲区（MM_IOB）  
CONFIG_SYSLOG_INTBUFFER=y     # 启用中断日志缓冲区
```

##### setlogmask

通过 `setlogmask` 命令，用户可以动态设置系统日志的最低输出等级，过滤掉低优先级的日志。

```Makefile
# 启用 setlogmask 功能
CONFIG_SYSTEM_SETLOGMASK=y     
```

```Bash
# setlogmask 用法
nsh> setlogmask

Usage: setlogmask <d|i|n|w|e|c|a|r>
       setlogmask -h
       setlogmask list
       setlogmask <enable/disable> <channel>
       
Where:
  d=DEBUG
  i=INFO
  n=NOTICE
  w=WARNING
  e=ERROR
  c=CRITICAL
  a=ALERT
  r=EMERG
  
# 用法示例：
# 只保留 error 及以上级别 log
nsh> setlogmask e
```

## 二、printf

### 1、函数声明

```C
int printf( const char * format, ... );
```

### 2、注意事项

#### 2.1 跨平台兼容性

打印数字时，建议使用 `<inttypes.h>` 中定义的类型进行格式化，以确保代码的跨平台兼容性。具体可参考 [cinttypes](https://cplusplus.com/reference/cinttypes/)。

#### 2.2 异构多核环境中的限制

虽然 `printf` 可以在单核环境下正常使用，但**不推荐在异构多核环境中使用。**

- 原因：

    在多核环境中，非主核调用 `printf` 时，会通过 `uart_rpmsg` IPC 将打印内容发送到主核的 `cu` 程序进行读取。如果 `cu` 程序未切换到对应核（例如使用 `cu -l /dev/ttyRBT`），将无法读取 `uart_rpmsg` IPC 缓冲区中的内容。导致如下后果：

    - IPC 缓冲区无法及时归还，导致缓冲区耗尽。
    - 频繁的日志打印可能阻塞其他 IPC 功能，从而影响系统中其他组件的正常运行。

- 解决方案：

    在非主核上打印日志时，请使用 `syslog`，以避免上述问题。

#### 2.3 适用场景

- `printf` 适用于与用户交互的命令行工具。
- 如下场景禁止使用：
    - 内核模块。
    - 后台长期运行的程序或服务。

### 3、使用限制

- 调用 `printf` 的线程可能会阻塞，影响程序运行。
- 中断函数中禁止调用 `printf`。
- `printf` 的输出无法跨核传递。
- `printf` 的输出不会存储为文件。
- 在 Linux 内核中，`printk` 的功能等价于 `syslog`，而不是 `printf`。

## 三、常见问题

### 1、syslog 和 printf 交叉打印问题

#### 问题描述

在 SMP（Symmetric Multiprocessing）环境或中断与应用程序同时打印日志时，可能会出现多条日志交叉打印的问题。

原因是日志尚未完全打印完成时，线程（或 CPU）切换导致新的日志开始打印，造成交叉输出。

#### 解决方案

为保证日志能够一次性完整打印，可采用以下方法：

1. 将日志保存到缓冲区再一次性打印。

    开启 `syslog` 缓冲区，使日志按整行打印。

    ```Makefile
    CONFIG_SYSLOG_BUFFER=y     
    CONFIG_SYSLOG_INTBUFFER=y
    ```

2. 避免 `syslog` 和 `printf` 交叉打印。

    在 `syslog` 和 `printf` 同时使用的情况下，需启用以下配置项：

    ```Makefile
    CONFIG_STDIO_LINEBUFFER=y
    CONFIG_STDIO_BUFFER_SIZE=512
    CONFIG_STREAM_OUT_BUFFER_SIZE=256
    CONFIG_UART0_RXBUFSIZE=1024
    CONFIG_UART0_TXBUFSIZE=1024
    ```

3. 保证打印过程不被中断。

    - 芯片驱动需实现 `up_nputs` 函数。
    - 串口驱动需支持 DMA 发送。

### 2、ramlog 冷启动乱码问题

#### 问题描述

在支持 `ramlog` 的系统中（尤其是支持 **warm reset** 的场景），需要保证 RAM 能保留重启前的日志内容。但在冷启动（cold start）时，`ramlog` 的缓冲区（ringbuffer）可能包含随机值，导致日志乱码。

#### 解决方案

1. 冷启动时初始化缓冲区。

    - 在 `ramlog` 的缓冲区（ringbuffer）中预留最后 4 字节，用于存储标定值。
    - 启动时，检查预留字节是否包含标定值：
        - 如果不是标定值：说明是冷启动，此时缓冲区为随机值，需使用 `memset` 初始化为 `0`，并写入标定值。
        - 如果是标定值：说明是 warm reset，无需初始化缓冲区。

2. warm reset 快速获取指针。

    - 在 `ramlog` 的缓冲区中保存 `head` 和 `tail` 指针。
    - 重启后：
        - 若为 warm reset：直接使用当前的 `head` 和 `tail` 值。
        - 若为冷启动：将 `head` 和 `tail` 指针初始化为 `0`。

### 3、Android 兼容性

#### 描述

所有 Android C/C++ 日志定义的 API 和宏可以直接使用，无需修改。

#### 参考文档

- [Logging | Android NDK | Android Developers](https://developer.android.com/ndk/reference/group/logging)
- [Using Asserts in Embedded Systems | Interrupt (memfault.com)](https://interrupt.memfault.com/blog/asserts-in-embedded-systems)
- [Exploring printf on Cortex-M | Interrupt (memfault.com)](https://interrupt.memfault.com/blog/printf-on-embedded)