# 日志系统

\[ [English](../../../../en/device_dev_guide/kernel/logging/logging_system.md) | 简体中文 \]

## 一、syslog

### 1、函数声明

```C
void syslog(int priority, const char *format, ...);
```

### 2、注意事项

- 内核中不建议直接调用`syslog`输出日志，而是使用 _info, _alert 等

  在内核中，请使用 `include/debug.h` 中定义的日志宏，或者根据需求自定义类似的宏以确保日志的统一性和规范性。

### 3、功能概述

`syslog` 支持多等级、多通道的日志打印，能够以带有时间戳、CPU ID 和进程 ID（PID）的格式输出日志。其整体框架如下图所示：

![img](./figures/001.svg)

**注意**：CONFIG_SYSLOG_MAX_CHANNELS定义的通道总数需要和如上各通道的配置总数相匹配。

根据整体框架图，所有的syslog最终都将由lib_vsprintf函数完成输出：

```Bash
syslog //libs/libc/syslog/lib_syslog.c
    vsyslog
        nx_vsyslog //drivers/syslog/vsyslog.c
            lib_sprintf //libs/libc/stdio/lib_libsprintf.c
                lib_vsprintf //libs/libc/stdio/lib_libvsprintf.c
                    vsprintf_internal //libs/libc/stdio/lib_libvsprintf.c
                        stream_putc

printf //libs/libc/stdio/lib_printf.c
    vfprintf //libs/libc/stdio/lib_vfprintf.c
        lib_vsprintf
```

数据输出流程如下所示：
![img](./figures/002.png)

vsprintf_internal函数依次对字符串中的每个字符，调用stream_putc进行输出。对于syslog stream，当配置了`CONFIG_SYSLOG_BUFFER`时，将设立一个log缓冲区。stream_putc将字符依次添加到buf中，当buf被填满时，再调用驱动channel的数据发送函数将数据实际发送出去。当没有配置CONFIG_SYSLOG_BUFFER时，将直接调用驱动channel的字符发送函数发送数据。代码实现：
```C
//libs/libc/stdio/lib_libvsprintf.c
#define stream_putc(c,stream)  (total_len++, lib_stream_putc(stream, c))
#define lib_stream_putc(stream, ch) \
        ((FAR struct lib_outstream_s *)(stream))->putc( \
        (FAR struct lib_outstream_s *)(stream), ch)

//libs/libc/stream/lib_syslogstream.c      
syslogstream_putc
#ifdef CONFIG_SYSLOG_BUFFER
    syslogstream_addchar(stream, ch);
          if (iob->io_len >= CONFIG_IOB_BUFSIZE)
            {
              syslogstream_flush(stream);
                  syslog_write
                        g_syslog_channel[i]->sc_ops->sc_write(g_syslog_channel[i],buffer, buflen);
            }
#else
    syslog_putc //这里会处理中断中的log打印，解决资源冲突（为中断打印单独设置一个buf，如果没有的话将有可能打乱数据）
          g_syslog_channel[i]->sc_ops->sc_force(g_syslog_channel[i],ch); //中断中的log打印接口
          g_syslog_channel[i]->sc_ops->sc_putc(g_syslog_channel[i], ch); //调用各个channel自己的数据发送函数
#endif
```

syslog_putc将遍历g_syslog_channel，并分别调用各自的驱动函数将log数据发送出去，通道注册：

```C
//drivers/syslog/syslog_channel.c
int syslog_channel(FAR struct syslog_channel_s *channel)
{
#if (CONFIG_SYSLOG_MAX_CHANNELS != 1)
  int i;
#endif

  DEBUGASSERT(channel != NULL);

  if (channel != NULL)
    {
      DEBUGASSERT(channel->sc_ops->sc_putc != NULL &&
                  channel->sc_ops->sc_force != NULL);

#if (CONFIG_SYSLOG_MAX_CHANNELS == 1)
      g_syslog_channel[0] = channel;
      return OK;
#else
      for (i = 0; i < CONFIG_SYSLOG_MAX_CHANNELS; i++)
        {
          if (g_syslog_channel[i] == NULL)
            {
              g_syslog_channel[i] = channel;
              return OK;
            }
          else if (g_syslog_channel[i] == channel)
            {
              return OK;
            }
        }
#endif
    }

  return -EINVAL;
}
```

各channel注册时需要提供的ops:

```C
//include/nuttx/syslog/syslog.h
/* SYSLOG device operations */

struct syslog_channel_ops_s
{
  syslog_putc_t  sc_putc;   /* Normal buffered output */
  syslog_putc_t  sc_force;  /* Low-level output for interrupt handlers */
  syslog_flush_t sc_flush;  /* Flush buffered output (on crash) */
  syslog_write_t sc_write;  /* Write multiple bytes */
  syslog_close_t sc_close;  /* Channel close callback */
};
```

注意，在syslog_putc函数中会判断当前所处上下文，当处于中断和任务线程中会分别调用不同的数据输出函数。因此各个channel需要自己保证中断中的数据输出函数可用（非阻塞、可重入）。在drivers/syslog/Kconfig中有各syslog channels的配置项描述，在drivers/syslog/README.txt中有各syslog channel的功能描述。

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
6. 多种channel 可以同时存在，例如：可以往 uart 和 ram 里同时输出

### 5、日志优先级 & 日志过滤 setlogmask

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
通过 `setlogmask` 命令，用户可以动态设置系统日志的最低输出等级，过滤掉低优先级的日志。

```Makefile
# 启用 setlogmask 功能
CONFIG_SYSTEM_SETLOGMASK=y     

# 开启配置后可运行时配置 channel
CONFIG_SYSLOG_IOCTL=y
```
`setlogmask` 用法示例：

过滤日志信息，依赖 CONFIG_SYSTEM_SETLOGMASK

```Bash
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
  
# 设置为最严格等级，关闭所有 syslog
nsh> setlogmask r

# 设置为 debug 等级，打印 debug 信息
nsh> setlogmask d
```

查看/设置 syslog channel，依赖 CONFIG_SYSLOG_IOCTL

```Bash

# 查看/设置 syslog channel，依赖 CONFIG_SYSLOG_IOCTL
nsh> setlogmask list
Channels:
  default: enable
  ram: enable
 
# 关闭 syslog 串口输出
nsh> setlogmask disable default
  
# 查看关闭后的 syslog channel
nsh> setlogmask list
Channels:
  default: disable
  ram: enable
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

### 8、日志多通道配置

内核日志支持多种输出通道，包括终端、串口、内存等。开发者可以根据需求选择合适的配置，灵活调整日志的输出方式、内容和格式。

#### 8.1 单核打印到终端或串口

如果需要将日志打印到终端或串口，请启用以下配置：

```Makefile
CONFIG_SYSLOG_DEFAULT=y      # 默认配置，输出到串口
```
default_channel是将log默认输出到串口，无需特别的初始化，只要提供了底层硬件相关的low-level的uart driver接口（即配置`CONFIG_ARCH_LOWPUTC`）就可以使用，可以记录在较早启动阶段的log。

```Plaintext
//drivers/syslog/Kconfig
comment "SYSLOG channels"

config SYSLOG_DEFAULT
        bool "Default SYSLOG device"
        default ARCH_LOWPUTC && !SYSLOG_CHAR && !RAMLOG_SYSLOG && !SYSLOG_RPMSG && !SYSLOG_RTT && !SYSLOG_CONSOLE
        ---help---
                syslog() interfaces will be present, but all output will go to the
                up_putc(ARCH_LOWPUTC == y) or bit-bucket(ARCH_LOWPUTC == n).
```

参考配置：
```Makefile
CONFIG_SYSLOG_DEFAULT=y
CONFIG_ARCH_LOWPUTC=y
```

代码实现：

```C
///drivers/syslog/syslog_channel.c
static const struct syslog_channel_ops_s g_default_channel_ops =
{
  syslog_default_putc,
  syslog_default_putc,
  NULL,
  syslog_default_write
};

#if defined(CONFIG_SYSLOG_DEFAULT)
static int syslog_default_putc(FAR struct syslog_channel_s *channel, int ch)
{
  UNUSED(channel);

#if defined(CONFIG_ARCH_LOWPUTC)
  return up_putc(ch);
#else
  return ch;
#endif
}
```

比如/arch/arm/src/stm32f010g0/stm32_serial_v1.c中提供的up_putc函数

```C
/****************************************************************************
 * Name: up_putc
 * Description:
 *   Provide priority, low-level access to support OS debug writes
 ****************************************************************************/
int up_putc(int ch)
{
#if CONSOLE_USART > 0
  /* Check for LF */
  if (ch == '\n')
    {
      /* Add CR */
      arm_lowputc('\r');
    }
  arm_lowputc(ch);
#endif
  return ch;
}
```

low-level的uart driver发送数据是通过关闭中断，通过轮询uart寄存器的方式实现的。在中断中打印的log可以通过该channel输出到uart。但是中断和任务中输出的log可能会混杂在一起。

#### 8.2 打印到内存 ramlog

如果需要将日志打印到内存，请配置以下选项：

```Makefile
CONFIG_RAMLOG=y                # 启用 RAMLOG  
CONFIG_RAMLOG_SYSLOG=y         # 启用 RAMLOG 的 syslog 支持  
CONFIG_RAMLOG_BUFSIZE=1024     # RAMLOG 缓冲区大小  
RAMLOG_BUFFER_SECTION=".bss"   # 将缓冲区放置到固定 section
```

#### 8.3 打印到文件 file

如果需要将日志打印到文件，请配置以下选项：

```Makefile
CONFIG_SYSLOG_FILE=y           # 启用日志文件输出
```

file_channel是将数据输出到文件，文件节点同样可以被视作为一个设备节点，所以其channel_ops和dev_channel相同。默认情况下，vela内核中没有使用该channel，如需使用，则需应用主动调用syslog_file_channel接口，并传入log file的路径，如：
 
```C
//boards/arm/stm32/clicker2-stm32/src/stm32_appinit.c
board_app_initialize()
{
    #ifdef CONFIG_CLICKER2_STM32_SYSLOG_FILE
    
      /* Delay some time for the automounter to finish mounting before
       * bringing up file syslog.
       */
    
      nxsig_usleep(CONFIG_CLICKER2_STM32_SYSLOG_FILE_DELAY * 1000);
    
      struct syslog_channel_s *channel;
      channel = syslog_file_channel(CONFIG_CLICKER2_STM32_SYSLOG_FILE_PATH);
      if (channel == NULL)
        {
          syslog(LOG_ERR, "ERROR: syslog_file_channel() failed\n");
          return -EINVAL;
        }
    #endif
}
```
配置说明：

| SYSLOG_FILE | 使能file channel feature |
|:------|:------|
|SYSLOG_FILE_SEPARATE|每次打开日志文件，将增加一个空白行，用于区分两次启动的log。默认为n| 
|SYSLOG_FILE_ROTATIONS|当log file的size到达一定size时，创建新的文件存储log，该宏为新创建文件的最大值。默认为0| 
| SYSLOG_FILE_SIZE_LIMIT| 在使能了SYSLOG_FILE_ROTATIONS的情况下，单个log文件的最大值。默认为524288|


#### 8.4 打印到设备文件 device

如果需要将日志打印到指定设备文件，例如 `/dev/ttyS1`，请配置以下选项：

```Makefile
CONFIG_SYSLOG_CONSOLE=y             # 打印日志到 /dev/console  
CONFIG_SYSLOG_CHAR=y                # 打印日志到指定设备文件，例如 /dev/ttyS1  
CONFIG_SYSLOG_DEVPATH="/dev/ttyS1"  # 指定设备文件路径
```
将syslog输出到指定的字符设备：

```C
//drivers/syslog/syslog_device.c
static const struct syslog_channel_ops_s g_syslog_dev_ops =
{
  syslog_dev_putc,
  syslog_dev_force,
  syslog_dev_flush,
  syslog_dev_write,
  syslog_dev_uninitialize
};
```
在syslog_dev_putc中，最终通过file_write(fd,)调用字符设备的驱动函数发送数据，所以在使用该种channel时，需要字符设备驱动已经初始化。此外，在syslog_dev_putc中，会等待获取dev的锁，所以不能被用在输出中断中的log打印。

console_channel也是dev_channel中特殊的一种，将log输出到/dev/console。

配置项：

```Plaintext
config SYSLOG_CONSOLE
        bool "Log to /dev/console"
        default !ARCH_LOWPUTC && !SYSLOG_CHAR && !RAMLOG_SYSLOG && !SYSLOG_RPMSG && !SYSLOG_RTT
        depends on DEV_CONSOLE
```
```Plaintext
//sched/Kconfig
config DEV_CONSOLE
        bool "Enable /dev/console"
        default y
```
参考配置：

```Makefile
CONFIG_SYSLOG_CONSOLE=y
```
单独将console提出来是因为，系统还支持将syslog dev作为/dev/console使用（取代了原来/dev/console设备节点的操作函数）：

```C
//drivers/drivers_initialize.c
#elif defined(CONFIG_CONSOLE_SYSLOG)
  syslog_console_init();
#endif

//drivers/syslog/syslog_console.c
void syslog_console_init(void)
{
  register_driver("/dev/console", &g_consoleops, 0666, NULL);
}

static const struct file_operations g_consoleops =
{
  NULL,                 /* open */
  NULL,                 /* close */
  syslog_console_read,  /* read */
  syslog_console_write, /* write */
};
```

也就是说通过printf打印的log也可以输出到syslog的各个channel中。

配置项：
```Plaintext
config CONSOLE_SYSLOG
        bool "Use SYSLOG for /dev/console"
        default n
        depends on DEV_CONSOLE && !SYSLOG_CONSOLE
```

CONSOLE_SYSLOG和SYSLOG_CONSOLE宏互斥。

#### 8.5 打印到主核 CPU

rpmsg_channel用于多核系统，从核向主核发送log的情况，依赖于从核和主核之间的通讯框架/机制。
如果需要将日志跨核打印到主核 CPU 或远程 CPU，请配置以下选项：


```Makefile
# 主核CPU配置
CONFIG_SYSLOG_RPMSG_SERVER=y

# 主核 board init
syslog_rpmsg_server_init()

# 从核CPU配置
CONFIG_SYSLOG_RPMSG=y
CONFIG_SYSLOG_RPMSG_SERVER_NAME="ap"

# 从核 board init
syslog_rpmsg_init_early()
syslog_rpmsg_init()
```

#### 8.6 打印到 USB CDCACM

```Makefile
CONFIG_SYSLOG_CDCACM=y     配置CDCACM做为SYSLOG的一个通道
```

### 9、格式打印

格式打印是指在用户打印的log string基础之上，加上系统信息，如timestamp、pid等系统信息，支持的宏配置如下：

| 字段名称及描述                                                                 | 详细说明                                                                                   |
| :----------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| SYSLOG_TIMESTAMP<br>显示时间戳                                                   | - SYSLOG_TIMESTAMP_REALTIME：wall-clock（自1970的那个时间）<br>- SYSLOG_TIMESTAMP_FORMATTED：格式化时间输出<br>- SYSLOG_TIMESTAMP_LOCALTIME：以本地时间显示<br>- SYSLOG_TIMESTAMP_FORMAT："%d/%m/%y %H:%M:%S"<br>- SYSLOG_TIMESTAMP_FORMAT_MICROSECOND：加ms<br>- SYSLOG_TIMESTAMP_BUFFER：时间戳的buffer |
| SYSLOG_PRIORITY                                                                 | 显示log优先级（info、err等）                                                                |
| SYSLOG_PROCESS_NAME                                                             | 显示线程名称                                                                                |
| SYSLOG_PROCESSID                                                                | 显示线程PID                                                                                 |
| SYSLOG_PREFIX                                                                   | 添加log前缀<br>SYSLOG_PREFIX_STRING<br>增加的前缀字符串                                      |
| SYSLOG_COLOR_OUTPUT                                                             | 以不同颜色显示不同log优先级打印的log（禁止在自身log打印中添加颜色打印字符）                  |

如：
```Makefile
CONFIG_SYSLOG_TIMESTAMP=y                //只打印UTC，以us为单位
CONFIG_SYSLOG_TIMESTAMP_REALTIME=y       //打印localtime
CONFIG_SYSLOG_TIMESTAMP_FORMAT="%y/%m/%e %H:%M:%S"// 年月日 时分秒
CONFIG_SYSLOG_TIMESTAMP_LOCALTIME=y
CONFIG_SYSLOG_TIMESTAMP_FORMATTED=y

CONFIG_SYSLOG_PROCESSID=y
CONFIG_SYSLOG_PREFIX=y
CONFIG_SYSLOG_PREFIX_STRING=ap
```

### 10、中断打印syslog

在中断打印 syslog 时，正常使用 syslog api，为了避免中断执行时间过长，建议开`SYSLOG_INTBUFFER`

```Bash
CONFIG_SYSLOG_INTBUFFER=y
CONFIG_SYSLOG_INTBUFSIZE=512
```
根据前面所述，在中断中打印的log无法在dev_channel（包括file_channel 和console_channel）中输出，在default_channel和ramlog_channel虽然可以输出，但是中断中打印的log和任务中打印的log会存在错序的情况。所以，系统针对中断中打印的log，维护了一个可选的配置项：

```Plaintext
//drivers/syslog/Kconfig
config SYSLOG_INTBUFFER
        bool "Use interrupt buffer"
        default n
        ---help---
                Enables an interrupt buffer that will be used to serialize debug
                output from interrupt handlers.

config SYSLOG_INTBUFSIZE
        int "Interrupt buffer size"
        default 512
        depends on SYSLOG_INTBUFFER
        ---help---
                The size of the interrupt buffer in bytes.
```
当发现当前处于中断上下文时，首先将log输出到一个中断log buffer中便返回，当下次再次打印log时，如果此时所处的不是中断上下文，则先将之前保存到中断log buffer中的数据输出，再输出本次的log：

```C
//drivers/syslog/syslog_putc.c/syslog_putc
#if defined(CONFIG_SYSLOG_INTBUFFER)
      if (up_interrupt_context())
        {
          /* Buffer the character in the interrupt buffer.
           * The interrupt buffer will be flushed before the next
           * normal,non-interrupt SYSLOG output.
           */

          return syslog_add_intbuffer(ch);
        }
      else
#endif
    {
#ifdef CONFIG_SYSLOG_INTBUFFER
      /* Flush any characters that may have been added to the interrupt
       * buffer.
       */

      syslog_flush_intbuffer(false);
#endif

    .............
}
```

## 二、printf

### 1、函数声明

```C
int printf( const char * format, ... );
```

### 2、注意事项

#### 2.1 跨平台兼容性

打印数字时，建议使用 `<inttypes.h>` 中定义的类型进行格式化，以确保代码的跨平台兼容性。具体可参考 [cinttypes](https://cplusplus.com/reference/cinttypes/)。

#### 2.2 内核或者services 不允许使用 printf

以下场景禁止使用：

  - 内核模块。
  - 后台长期运行的程序或服务。
  
>原因1 多核阻塞：
>在多核环境中，非主核调用 printf 时，会通过 uart_rpmsg IPC 将打印内容发送到主核的 cu 程序进行读取。如果 cu 程序未切换到对应核（例如使用 cu -l /dev/ttyRBT），将无法读取 uart_rpmsg IPC 缓冲区中的内容。导致如下后果：
>  - IPC 缓冲区无法及时归还，导致缓冲区耗尽。
>  - 频繁的日志打印可能阻塞其他 IPC 功能，从而影响系统中其他组件的正常运行。
>
>原因2 打印混乱：
>
>  - Printf 和 syslog 交叉使用，则容易让日至截断，混乱，不可读

#### 2.3 printf 适用场景

- `printf` 适用于与用户交互的命令行工具。

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
- [https://kb.segger.com/DCC](https://kb.segger.com/DCC)
- [https://github.com/eyalroz/printf](https://github.com/eyalroz/printf)
- [https://interrupt.memfault.com/blog/device-logging](https://interrupt.memfault.com/blog/device-logging)
