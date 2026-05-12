# Backtrace 使用指南

\[ [English](../../../en/debugging_tools/offline_debugging/backtrace.md) | 简体中文 \]

## 一、概述

在日常开发中，我们常常需要查看指定线程的栈信息，常见的场景包括：

- 死锁（deadlock）
- 高 CPU 使用率（high CPU usage）
- 忙循环（busy loop）
- 系统崩溃（crash）
- 内存调试（memory debug）

通常情况下，借助调试工具（如 JLink），可以通过 `gdb` 和断点（breakpoint，简称 bp）的方式实现这些功能。但在设备封包发布和外围调试功能关闭之后，这些功能在真实设备上往往无法使用。

为了解决这一问题，openvela 支持在运行环境中查看特定线程的栈信息。

## 二、配置说明

### 1、通用配置说明

openvela 支持 ARM、RISC-V 和 Xtensa 三种架构的通用配置，具体如下：

```Makefile
# 开启 backtrace 功能，默认不显示函数名称
CONFIG_SCHED_BACKTRACE=y
CONFIG_SYSTEM_DUMPSTACK=y

# 如果需要符号名支持，启用以下选项；  
# 若 Flash 空间不足，可以通过 addr2line 手动解析地址到符号  
CONFIG_ALLSYMS=y

# 启用架构支持  
CONFIG_ARCH_HAVE_BACKTRACE=y
```

对于 ARM 平台，由于代码资源限制及 Thumb-2 特性的要求，提供以下三种 backtrace 实现方式供选择：

```Makefile
# 基于帧指针（frame pointer）的回溯实现
CONFIG_UNWINDER_FRAME_POINTER

# 基于栈指针（stack pointer）的回溯实现 
CONFIG_UNWINDER_STACK_POINTER

# 基于 ARM 架构的 .exidx 段的回溯实现
CONFIG_UNWINDER_ARM
```

目前，openvela 支持 ARM、RISC-V 和 Xtensa 三种体系结构的 backtrace 功能，各架构的配置和实现如下。

### 2、ARM

#### ARM Cortex-A/R

在 ARM Cortex-A 和 Cortex-R 系列中，backtrace 实现支持以下两种方式，选择其中一种即可：

```Makefile
# 方式 1：基于 fp 寄存器的回溯实现  
CONFIG_UNWINDER_FRAME_POINTER

# 方式 2：基于 .exidx 段的回溯实现 
CONFIG_UNWINDER_ARM
```

#### ARM Cortex-M

在 ARM Cortex-M 系列中，backtrace 有以下三种实现方式，根据项目需求选择其一：

```Makefile
# 方式 1：基于 fp 的回溯实现（需注意编译器限制）  
CONFIG_UNWINDER_FRAME_POINTER=y  

# 方式 2：基于 sp 的回溯实现，适用于小资源设备  
CONFIG_UNWINDER_STACK_POINTER=y  

# 方式 3：基于 .exidx 段的回溯实现  
CONFIG_UNWINDER_ARM=y
```

- CONFIG_UNWINDER_FRAME_POINTER：GCC 编译器上存在相关限制（详情参考 [GCC 问题](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=92172)）。
- CONFIG_UNWINDER_STACK_POINTER：通过 `bl`/`blx` 指令获取 pc 地址，适用于资源有限的设备，但存在一定的误判概率。如果项目代码被分散到多个区域，需要通过以下 API 配置多个代码区域：

    ```C
    void up_backtrace_init_code_regions(FAR void **regions)
    ```

- CONFIG_UNWINDER_ARM：在编译阶段生成 .exidx 段，代码体积增加 5%-8%。

### 3、RISC-V

在 RISC-V 架构中，backtrace 基于帧指针（frame pointer）实现，只需启用以下配置：

```Makefile
CONFIG_FRAME_POINTER=y
CONFIG_SCHED_BACKTRACE=y
```

更多信息参考：[RISC-V Backtrace 实现](../../../../../../nuttx/blob/dev-ai-contest-2026/arch/risc-v/src/common/riscv_backtrace.c)

### 4、Xtensa

在 Xtensa 架构中，backtrace 默认支持栈回溯，不需要额外启用 `-fno-omit-frame-pointer` 选项。

## 三、操作使用

在代码中使用 backtrace 系列函数需要包含头文件 `#include <execinfo.h>`。本章介绍如何使用 backtrace 获取函数调用堆栈信息、打印日志及定位错误行。

### 1、在代码中使用 backtrace

使用 backtrace 系列函数可以捕获当前程序状态，打印堆栈信息。以下是常见函数说明，

更多细节请参考 Linux Man Page: [backtrace](https://man7.org/linux/man-pages/man3/backtrace.3.html)。

```C
#include<execinfo.h>

/* 存储当前程序状态至__array数组，array最大数量为__size
    返回值为实际存储的元素个数 
*/
extern int backtrace (void **__array, int __size) __nonnull ((1));

/*  
  功能：返回一个字符串数组，存放从 backtrace 获取的信息。  
  参数：  
    - __array: backtrace 返回的指针数组  
    - __size:  backtrace 的返回值  
  注意：该方法会调用 `backtrace_malloc(FAR void *const *buffer, int size)` 申请空间，定义在   
  nuttx/libs/libc/misc/lib_execinfo.c 文件中。  
*/  
extern char **backtrace_symbols (void *const *__array, int __size)
     __THROW __nonnull ((1));

/*  
  功能：和 backtrace_symbols 类似，但无需申请额外空间，直接写入文件描述符 __fd。  
*/  
extern void backtrace_symbols_fd (void *const *__array, int __size, int __fd)
     __THROW __nonnull ((1));
```

### 2、`dump_stack()`

1. 在 openvela 系统中，可以直接调用 `dump_stack()` 函数打印堆栈信息。例如：

    ```C
    // 在 examples/hello/hello_main.c 文件中添加测试代码
    37 int main(int argc, FAR char *argv[])
    38 {
    39   printf("Hello, World!!\n");
    +40   dump_stack();  // 打印堆栈信息  
    41   return 0;
    42 }
    ```

    打印输出示例：

    ```Bash
    ap> hello
    Hello, World!!
    [07:06:21] [28] [  INFO] [BackTrace|28|0]:   0xc070a96  0xc063d7c  0xc0809bc  0xc063d38  0xc0587de
    ```

2. 使用 `addr2line` 工具解析打印出的回溯地址到具体的代码行：

    ```Bash
    addr2line -fe nuttx 0xc070a96  0xc063d7c  0xc0809bc  0xc063d38  0xc0587de  
    ```

    解析结果示例：

    ```Bash
    nuttx/arch/arm/src/armv8-m/arm_backtrace.c:446
    nuttx/libs/libc/sched/sched_dumpstack.c:60
    apps/examples/hello/hello_main.c:40
    nuttx/libs/libc/sched/task_startup.c:151
    nuttx/sched/task/task_start.c:130
    ```

3. 利用 `dump_stack()` 的地址定位错误位置，或者通过[打开符号表](./allsyms_guide.md)功能直接打印函数名称，方便分析。

### 3、`dumpstack` 命令

在命令行中，可以使用 `dumpstack` 命令获取指定任务的 backtrace。以下是使用方法：

#### 使用 `dumpstack [pid]` 获取任务堆栈

1. 获取进程的堆栈。

    ```Bash
    # 查看进程状态
    ap> ps
    ...
    26       100 RR       Task    --- Waiting  Semaphore 00000010 004056 000648  15.9%    0.0% Telnet daemon 0x3c4293e0

    # 查看 PID 为 26 的 backtrace
    ap> dumpstack 26
    [15:18:53] [29] [  INFO] [BackTrace|26|0]:   0xc06b1c2   0x2154aa   0x20f312  0xc2ca118  0xc2c9bc4  0xc2c9c34  0xc08d894  0xc063d38
    [15:18:53] [29] [  INFO] [BackTrace|26|1]:   0xc0587de
    ```

2. 使用 `addr2line` 解析回溯地址。

    ```Bash
    addr2line -e nuttx 0xc06b1c2   0x2154aa   0x20f312  0xc2ca118  0xc2c9bc4  0xc2c9c34  0xc08d894  0xc063d38
    ```

3. 查看解析结果。

    解析结果示例如下：

    ```Bash
    nuttx/arch/arm/src/armv8-m/arm_switchcontext.S:79
    nuttx/net/utils/net_lock.c:128
    nuttx/net/tcp/tcp_accept.c:281
    nuttx/net/inet/inet_sockif.c:889
    nuttx/net/socket/accept.c:141 (discriminator 4)
    nuttx/net/socket/accept.c:270
    apps/netutils/telnetd/telnetd_daemon.c:240 (discriminator 3)
    nuttx/libs/libc/sched/task_startup.c:151
    ```

#### 使用 `dumpstack [pid_start] [pid_end]` 查看多个进程堆栈

查看 PID 从 0 到 26 的 backtrace 信息：

```Bash
ap> dumpstack 0 26  
[15:21:07] [30] [  INFO] [BackTrace|0|0]:  0xc054ba0  0xc3129f0  0xc000056  
[15:21:07] [30] [  INFO] [BackTrace|1|0]:  0xc06b1c2  0xc0572e2  0xc0595e6  0xc0587d4  
[15:21:07] [30] [  INFO] [BackTrace|26|0]:  0xc06b1c2  0xc2154aa  0xc0587d4  
...  
```

### 4、crash 日志中的调用栈解析

```Bash
[15:21:21] [25] [  INFO] [BackTrace|25|0]:   0xc070aa6  0xc063d7c  0xc070f58  0xc060948  0xc06b2a2  0xc054d1e  0xc070dc8  0xc06b21e
[15:21:21] [25] [  INFO] [BackTrace|25|1]:   0xc087556  0xc0847fa  0xc087864  0xc0889b4  0xc0837a8  0xc063d38  0xc0587de

crash thread 25:

$ addr2line -e nuttx 0xc070aa6  0xc063d7c  0xc070efc  0xc0569c8  0xc070fba  0xc060948  0xc06b2a2  0xc054d1e 0xc070dc8  0xc06b21e  0xc087556  0xc0847fa  0xc087864  0xc0889b4  0xc0837a8  0xc063d38
nuttx/arch/arm/src/armv8-m/arm_backtrace.c:446
nuttx/libs/libc/sched/sched_dumpstack.c:60
nuttx/arch/arm/src/armv8-m/arm_assert.c:167
```
