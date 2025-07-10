# Logging System


\[ English | [简体中文](../../../../zh-cn/device_dev_guide/kernel/logging/logging_system.md) \] 

## I. syslog

### 1. Function Declaration

```C
void syslog(int priority, const char *format, ...);
```

### 2. Notes

- It is not recommended to directly call `syslog` in the kernel to output logs; instead, use macros like _info, _alert, etc.

  In the kernel, please use the log macros defined in `include/debug.h`, or customize similar macros according to requirements to ensure the uniformity and standardization of logs.

### 3. Function Overview

`syslog` supports multi-level and multi-channel log printing, and can output logs in a format with timestamps, CPU IDs, and process IDs (PIDs). Its overall framework is as follows:

![img](./figures/001.svg)

**Note**: The total number of channels defined by CONFIG_SYSLOG_MAX_CHANNELS needs to match the total number of configurations of each channel as above.

According to the overall framework diagram, all syslogs will eventually be output by the lib_vsprintf function:

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

The data output process is as follows:
![img](./figures/002.png)

The vsprintf_internal function sequentially calls the stream_putc for each character in the string to output. For the syslog stream, when `CONFIG_SYSLOG_BUFFER` is configured, a log buffer will be set up. stream_putc will add characters to the buf in sequence, and when the buf is full, it will call the data sending function of the driver channel to actually send the data. When `CONFIG_SYSLOG_BUFFER` is not configured, it will directly call the character sending function of the driver channel to send the data. Code implementation:
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
    syslog_putc //Here, log printing in interrupts will be handled to resolve resource conflicts (a separate buffer is set for interrupt printing; otherwise, data may be disrupted)
          g_syslog_channel[i]->sc_ops->sc_force(g_syslog_channel[i],ch); //Log printing interface in interrupts
          g_syslog_channel[i]->sc_ops->sc_putc(g_syslog_channel[i], ch); //Call the data sending function of each channel
#endif
```

syslog_putc will traverse g_syslog_channel and call their respective driver functions to send log data. Channel registration:

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

The ops that need to be provided when each channel is registered:

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

Note that the syslog_putc function will determine the current context, and different data output functions will be called when in interrupts and task threads. Therefore, each channel needs to ensure that the data output function in the interrupt is available (non-blocking, reentrant). The configuration item descriptions of each syslog channel are in drivers/syslog/Kconfig, and the function descriptions of each syslog channel are in drivers/syslog/README.txt.

### 4. Workflow

1. `syslog` filters logs through the `log level filter`.
2. Wrap the log according to the specified format and send it to `lib_vsprintf`.
3. `lib_vsprintf` sends the data to the corresponding `stream`.
4. `syslog stream` supports multiple `channels`, such as:
    - `default_channel`
    - `ramlog_channel`
    - `rpmsg_channel`
    - `dev_channel`

5. Each `channel` uses the corresponding driver to output logs to the target device or medium (such as `uart`, `ram`, `file`, etc.).
6. Multiple channels can exist at the same time, for example: logs can be output to both uart and ram simultaneously.

### 5. Log Priority & Log Filtering setlogmask

`syslog` supports the following log priorities (`log level`):

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
Through the `setlogmask` command, users can dynamically set the minimum output level of system logs to filter out low-priority logs.

```Makefile
# Enable the setlogmask function
CONFIG_SYSTEM_SETLOGMASK=y     

# After enabling the configuration, the channel can be configured at runtime
CONFIG_SYSLOG_IOCTL=y
```
Example usage of `setlogmask`:

Filter log information, dependent on CONFIG_SYSTEM_SETLOGMASK

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
  
# Set to the strictest level, turn off all syslogs
nsh> setlogmask r

# Set to debug level, print debug information
nsh> setlogmask d
```

View/set syslog channel, dependent on CONFIG_SYSLOG_IOCTL

```Bash

# View/set syslog channel, dependent on CONFIG_SYSLOG_IOCTL
nsh> setlogmask list
Channels:
  default: enable
  ram: enable
 
# Turn off syslog serial port output
nsh> setlogmask disable default
  
# View the syslog channel after turning off
nsh> setlogmask list
Channels:
  default: disable
  ram: enable
```

### 6. Log Macros Used in the Kernel

Each of the following macros selects and configures a kernel `log` level. For example:

After turning off the `CONFIG_DEBUG_INFO` macro, all `logs` printed by the `_info` function in the kernel will be filtered out.

```C
// include/debug.h and include/syslog.h
CONFIG_DEBUG_ASSERT  ->  _alert
CONFIG_DEBUG_ERROR   ->  _err
CONFIG_DEBUG_WARN    ->  _warn
CONFIG_DEBUG_INFO    ->  _info
```

### 7. Log Printing in Kernel Modules

In each module of the kernel, log level printing is supported, corresponding to the log levels of `syslog`. The following are suggestions and configuration instructions for log printing.

#### 7.1 Driver Developers

Please use the dedicated printing functions provided by each module to ensure the standardization and consistency of log output.

#### 7.2 Application Developers

You can directly use `syslog(LOG_LEVEL, ...)` for log printing, for example:

```C
CONFIG_DEBUG_SCHED_ERROR  ->  serr
CONFIG_DEBUG_SCHED_WARN   ->  swarn
CONFIG_DEBUG_SCHED_INFO   ->  sinfo
CONFIG_DEBUG_MM_ERROR     ->  merr
CONFIG_DEBUG_MM_WARN      ->  mwarn
CONFIG_DEBUG_MM_INFO      ->  minfo
```
### 8. Multi-Channel Configuration of Logs

Kernel logs support multiple output channels, including terminals, serial ports, memory, etc. Developers can select appropriate configurations according to requirements and flexibly adjust the output method, content, and format of logs.

#### 8.1 Single-Core Printing to Terminal or Serial Port

If you need to print logs to a terminal or serial port, enable the following configuration:

```Makefile
CONFIG_SYSLOG_DEFAULT=y      # Default configuration, output to serial port
```
The default_channel outputs logs to the serial port by default. No special initialization is required. It can be used as long as the low-level hardware-related uart driver interface is provided (i.e., configure `CONFIG_ARCH_LOWPUTC`), and it can record logs in the early startup phase.

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

Reference configuration:
```Makefile
CONFIG_SYSLOG_DEFAULT=y
CONFIG_ARCH_LOWPUTC=y
```

Code implementation:

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

For example, the up_putc function provided in /arch/arm/src/stm32f010g0/stm32_serial_v1.c

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

The low-level uart driver sends data by disabling interrupts and polling the uart register. Logs printed in interrupts can be output to the uart through this channel. However, logs output in interrupts and tasks may be mixed together.

#### 8.2 Printing to Memory (ramlog)

If you need to print logs to memory, configure the following options:

```Makefile
CONFIG_RAMLOG=y                # Enable RAMLOG  
CONFIG_RAMLOG_SYSLOG=y         # Enable syslog support for RAMLOG  
CONFIG_RAMLOG_BUFSIZE=1024     # RAMLOG buffer size  
CONFIG_RAMLOG_OVERWRITE=y      # Overwrite old logs when the buffer is full  
RAMLOG_BUFFER_SECTION=".bss"   # Place the buffer in a fixed section
```

#### 8.3 Printing to File

If you need to print logs to a file, configure the following option:

```Makefile
CONFIG_SYSLOG_FILE=y           # Enable log file output
```

The file_channel outputs data to a file. The file node can also be regarded as a device node, so its channel_ops is the same as that of the dev_channel. By default, this channel is not used in the vela kernel. If you need to use it, the application needs to actively call the syslog_file_channel interface and pass in the path of the log file, such as:
 
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
Configuration description:

| SYSLOG_FILE | Enable file channel feature |
|:------|:------|
|SYSLOG_FILE_SEPARATE|Each time the log file is opened, a blank line will be added to distinguish logs from two starts. The default is n| 
|SYSLOG_FILE_ROTATIONS|When the size of the log file reaches a certain size, a new file will be created to store logs. This macro is the maximum number of new files created. The default is 0| 
| SYSLOG_FILE_SIZE_LIMIT| When SYSLOG_FILE_ROTATIONS is enabled, the maximum size of a single log file. The default is 524288|


#### 8.4 Printing to Device File

If you need to print logs to a specified device file, such as `/dev/ttyS1`, configure the following options:

```Makefile
CONFIG_SYSLOG_CONSOLE=y             # Print logs to /dev/console  
CONFIG_SYSLOG_CHAR=y                # Print logs to a specified device file, such as /dev/ttyS1  
CONFIG_SYSLOG_DEVPATH="/dev/ttyS1"  # Specify the device file path
```
Output syslog to the specified character device:

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
In syslog_dev_putc, data is finally sent by calling the driver function of the character device through file_write(fd,). Therefore, when using this kind of channel, the character device driver needs to be initialized. In addition, syslog_dev_putc will wait to acquire the dev lock, so it cannot be used to output log printing in interrupts.

The console_channel is also a special type of dev_channel, which outputs logs to /dev/console.

Configuration item:

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
Reference configuration:

```Makefile
CONFIG_SYSLOG_CONSOLE=y
```
The console is put forward separately because the system also supports using the syslog dev as /dev/console (replacing the operation function of the original /dev/console device node):

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

That is to say, logs printed by printf can also be output to each channel of syslog.

Configuration item:
```Plaintext
config CONSOLE_SYSLOG
        bool "Use SYSLOG for /dev/console"
        default n
        depends on DEV_CONSOLE && !SYSLOG_CONSOLE
```

CONSOLE_SYSLOG and SYSLOG_CONSOLE macros are mutually exclusive.

#### 8.5 Printing to Main Core CPU

The rpmsg_channel is used in multi-core systems where the secondary core sends logs to the main core, depending on the communication framework/mechanism between the secondary core and the main core.
If you need to print logs cross-core to the main core CPU or remote CPU, configure the following options:


```Makefile
# Main core CPU configuration
CONFIG_SYSLOG_RPMSG_SERVER=y

# Main core board init
syslog_rpmsg_server_init()

# Secondary core CPU configuration
CONFIG_SYSLOG_RPMSG=y
CONFIG_SYSLOG_RPMSG_SERVER_NAME="ap"

# Secondary core board init
syslog_rpmsg_init_early()
syslog_rpmsg_init()
```

#### 8.6 Printing to USB CDCACM

```Makefile
CONFIG_SYSLOG_CDCACM=y     Configure CDCACM as a channel of SYSLOG
```

### 9. Format Printing

Format printing refers to adding system information, such as timestamp, pid, etc., to the log string printed by the user. The supported macro configurations are as follows:

| Field name and description                                                                 | Detailed description                                                                                   |
| :----------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| SYSLOG_TIMESTAMP<br>Display timestamp                                                   |  SYSLOG_TIMESTAMP_REALTIME：wall-clock (the time since 1970)<br> SYSLOG_TIMESTAMP_FORMATTED：formatted time output<br> SYSLOG_TIMESTAMP_LOCALTIME：display in local time<br> SYSLOG_TIMESTAMP_FORMAT："%d/%m/%y %H:%M:%S"<br> SYSLOG_TIMESTAMP_FORMAT_MICROSECOND：add ms<br> SYSLOG_TIMESTAMP_BUFFER：buffer for timestamp |
| SYSLOG_PRIORITY                                                                 | Display log priority (info, err, etc.)                                                                |
| SYSLOG_PROCESS_NAME                                                             | Display thread name                                                                                |
| SYSLOG_PROCESSID                                                                | Display thread PID                                                                                 |
| SYSLOG_PREFIX <br> Add log prefix                                                  | SYSLOG_PREFIX_STRING<br>Added prefix string                                     |
| SYSLOG_COLOR_OUTPUT                                                             | Display logs printed with different log priorities in different colors (it is forbidden to add color printing characters in the log printing of itself)                  |

For example:
```Makefile
CONFIG_SYSLOG_TIMESTAMP=y                //Only print UTC in us
CONFIG_SYSLOG_TIMESTAMP_REALTIME=y       //Print localtime
CONFIG_SYSLOG_TIMESTAMP_FORMAT="%y/%m/%e %H:%M:%S"// Year/month/day hour:minute:second
CONFIG_SYSLOG_TIMESTAMP_LOCALTIME=y
CONFIG_SYSLOG_TIMESTAMP_FORMATTED=y

CONFIG_SYSLOG_PROCESSID=y
CONFIG_SYSLOG_PREFIX=y
CONFIG_SYSLOG_PREFIX_STRING=ap
```

### 10. Printing syslog in Interrupts

When printing syslog in interrupts, use the syslog api normally. To avoid the interrupt execution time being too long, it is recommended to enable `SYSLOG_INTBUFFER`

```Bash
CONFIG_SYSLOG_INTBUFFER=y
CONFIG_SYSLOG_INTBUFSIZE=512
```
As mentioned earlier, logs printed in interrupts cannot be output in dev_channel (including file_channel and console_channel). Although they can be output in default_channel and ramlog_channel, logs printed in interrupts and tasks may be out of order. Therefore, the system maintains an optional configuration item for logs printed in interrupts:

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
When it is found that the current context is an interrupt, the log is first output to an interrupt log buffer and then returned. When the log is printed again next time, if it is not in the interrupt context at this time, the data previously saved in the interrupt log buffer will be output first, and then the current log will be output:

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

## II. printf

### 1. Function Declaration

```C
int printf( const char * format, ... );
```

### 2. Notes

#### 2.1 Cross-Platform Compatibility

When printing numbers, it is recommended to use the types defined in `<inttypes.h>` for formatting to ensure cross-platform compatibility of the code. For details, refer to [cinttypes](https://cplusplus.com/reference/cinttypes/).

#### 2.2 printf is Not Allowed in Kernel or Services

The following scenarios are prohibited:

  - Kernel modules.
  - Programs or services running in the background for a long time.
  
>Reason 1 Multi-core blocking:
>In a multi-core environment, when a non-main core calls printf, the printed content will be sent to the cu program of the main core through uart_rpmsg IPC for reading. If the cu program is not switched to the corresponding core (for example, using cu -l /dev/ttyRBT), it will not be able to read the content in the uart_rpmsg IPC buffer. Resulting in the following consequences:
>  - The IPC buffer cannot be returned in time, leading to buffer exhaustion.
>  - Frequent log printing may block other IPC functions, thereby affecting the normal operation of other components in the system.
>
>Reason 2 Printing confusion:
>
>  - If printf and syslog are used alternately, it is easy to make the logs truncated, confused, and unreadable.

#### 2.3 Applicable Scenarios for printf

- `printf` is suitable for command-line tools that interact with users.

### 3. Usage Restrictions
- Threads calling `printf` may be blocked, affecting program operation.
- Calling `printf` in interrupt functions is prohibited.
- The output of `printf` cannot be transmitted cross-core.
- The output of `printf` will not be stored as a file.
- In the Linux kernel, the function of `printk` is equivalent to `syslog`, not `printf`.

## III. Common Problems

### 1. Problem of Cross Printing Between syslog and printf

#### Problem Description

In an SMP (Symmetric Multiprocessing) environment or when interrupts and applications print logs at the same time, there may be a problem of cross printing of multiple logs.

The reason is that when the log has not been completely printed, thread (or CPU) switching causes a new log to start printing, resulting in cross output.

#### Solution

To ensure that logs can be printed completely at one time, the following methods can be adopted:

1. Save the log to a buffer and then print it at one time.

    Enable the `syslog` buffer to print logs line by line.

    ```Makefile
    CONFIG_SYSLOG_BUFFER=y     
    CONFIG_SYSLOG_INTBUFFER=y
    ```

2. Avoid cross printing between `syslog` and `printf`.

    When `syslog` and `printf` are used at the same time, the following configuration items need to be enabled:

    ```Makefile
    CONFIG_STDIO_LINEBUFFER=y
    CONFIG_STDIO_BUFFER_SIZE=512
    CONFIG_STREAM_OUT_BUFFER_SIZE=256
    CONFIG_UART0_RXBUFSIZE=1024
    CONFIG_UART0_TXBUFSIZE=1024
    ```

3. Ensure that the printing process is not interrupted.

    - The chip driver needs to implement the `up_nputs` function.
    - The serial port driver needs to support DMA transmission.

### 2. Problem of Garbled Characters in ramlog Cold Start

#### Problem Description

In systems supporting `ramlog` (especially scenarios supporting **warm reset**), it is necessary to ensure that the RAM can retain the log content before restart. However, during cold start, the buffer (ringbuffer) of `ramlog` may contain random values, resulting in garbled logs.

#### Solution

1. Initialize the buffer during cold start.

    - Reserve the last 4 bytes in the buffer (ringbuffer) of `ramlog` for storing the calibration value.
    - During startup, check whether the reserved bytes contain the calibration value:
        - If it is not the calibration value: it indicates a cold start. At this time, the buffer is a random value, and it needs to be initialized to `0` using `memset` and write the calibration value.
        - If it is the calibration value: it indicates a warm reset, and there is no need to initialize the buffer.

2. Quickly obtain pointers for warm reset.

    - Save the `head` and `tail` pointers in the buffer of `ramlog`.
    - After restart:
        - For warm reset: directly use the current `head` and `tail` values.
        - For cold start: initialize the `head` and `tail` pointers to `0`.

### 3. Android Compatibility

#### Description

All APIs and macros defined by Android C/C++ logs can be used directly without modification.

#### Reference Documents

- [Logging | Android NDK | Android Developers](https://developer.android.com/ndk/reference/group/logging)
- [Using Asserts in Embedded Systems | Interrupt (memfault.com)](https://interrupt.memfault.com/blog/asserts-in-embedded-systems)
- [Exploring printf on Cortex-M | Interrupt (memfault.com)](https://interrupt.memfault.com/blog/printf-on-embedded)
- [https://kb.segger.com/DCC](https://kb.segger.com/DCC)
- [https://github.com/eyalroz/printf](https://github.com/eyalroz/printf)
- [https://interrupt.memfault.com/blog/device-logging](https://interrupt.memfault.com/blog/device-logging)