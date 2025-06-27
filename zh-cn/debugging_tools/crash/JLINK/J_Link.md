# 使用 J-Link GDB 插件增强 openvela 线程调试

## 一、概述

在标准的嵌入式开发流程中，使用 **SEGGER J-Link** 和 **GDB** (the GNU Project Debugger) 进行调试时，**GDB** 默认无法识别 **openvela**（基于 NuttX RTOS）的线程模型。这导致开发者无法列出当前系统的所有线程或在它们之间自由切换，极大地限制了多线程应用的调试效率。

本指南详细介绍如何通过 **J-Link** 的 **RTOS** 插件，扩展 **GDB** 的调试能力，从而实现对 **openvela** 系统的线程级调试。您将学习如何编译、配置并使用该插件来查看线程信息、切换线程上下文、以及分析特定线程的调用栈。

## 二、先决条件

在开始之前，请确保您的开发环境满足以下条件：

- 已正确安装 **SEGGER J-Link** 驱动和相关工具。
- 已准备好多架构 GDB 工具链（例如 `gdb-multiarch`）。
- 拥有 openvela 项目的完整源代码。

## 三、操作步骤

请遵循以下步骤来编译和启用线程调试插件。

### 步骤 1：编译 RTOS 插件

1. 插件的源代码位于 NuttX 的 `tools` 目录下。您需要手动编译生成动态库文件 (`.so`)。

    ```Bash
    cd nuttx/tools
    ```

2. 执行 `make` 命令编译插件。

    ```Makefile
    make -f Makefile.host jlink-nuttx.so
    ```

    编译成功后，将在当前目录下生成 `jlink-nuttx.so` 文件。

### 步骤 2：启动 J-Link GDB 服务器并加载插件

启动 J-Link GDB 服务器时，必须通过 `-rtos` 参数指定插件的绝对路径，以使其生效。

```Bash
JLinkGDBServer -if SWD -device Cortex-M55 -rtos <your-nuttx-project-path>/nuttx/tools/jlink-nuttx.so
```

- `-if SWD`: 指定调试接口为 SWD。
- `-device Cortex-M55`: 指定目标设备的核心类型。请根据您的硬件平台进行修改。
- `-rtos`: 指定 RTOS 插件的绝对路径。

### 步骤 3：连接 GDB 客户端并验证插件加载

1. 启动 GDB 客户端，并连接到 J-Link GDB 服务器。默认端口为 `2331`。

    ```Bash
    gdb-multiarch nuttx -ex "target remote localhost:2331"
    ```

2. 观察 GDB 的启动信息。如果看到以下输出，则表示插件已成功加载。

    ```Plaintext
    Loading RTOS plugin: /<your-nuttx-project-path>/nuttx/tools/jlink-nuttx.so...
    RTOS plugin (API v1.0) loaded successfully
    RTOS plugin: Loaded
    Received symbol: g_pidhash (0x3C036ADC)
    Received symbol: g_npidhash (0x3C036ACC)
    Received symbol: g_tcbinfo (0x2C531ACC)
    Received symbol: g_cpuload_total (0x3C036DE0)
    Received symbol: g_assignedtasks (0x00000000)
    All mandatory symbols successfully loaded.
    ```

## 四、核心调试命令与结果分析

插件加载成功后，您可以使用 GDB 的标准线程命令来调试 openvela 系统。

### 1、查看所有线程 (`info threads`)

此命令列出系统中所有正在运行的线程及其状态。

```Bash
  (gdb) info thread
  Id   Target Id                                           Frame
* 2    Thread 1 ([PID:000]Idle Task:0003[PRI:000])         nx_start () at init/nx_start.c:797
  3    Thread 2 ([PID:001]hpwork:0005[PRI:224])            arm_switchcontext (saveregs=0x3c00927c, restoreregs=0x3c00c5ac) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  4    Thread 19 ([PID:018]rpmsg-uorb-sens:0005[PRI:100])  arm_switchcontext (saveregs=0x3c015fbc, restoreregs=0x3c00efdc) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  5    Thread 4 ([PID:003]bes_main:0005[PRI:101])          arm_switchcontext (saveregs=0x3c00ae1c, restoreregs=0x3c00a2ec) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  6    Thread 5 ([PID:004]rptun:0005[PRI:224])             arm_switchcontext (saveregs=0x3c00c5ac, restoreregs=0x3c010fac) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  7    Thread 6 ([PID:005]rptun:0005[PRI:224])             arm_switchcontext (saveregs=0x3c00d43c, restoreregs=0x3c012acc) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  8    Thread 7 ([PID:006]rptun:0005[PRI:224])             arm_switchcontext (saveregs=0x3c00e29c, restoreregs=0x2000972c <g_idletcb+140>) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  9    Thread 8 ([PID:007]init:0005[PRI:100])              arm_switchcontext (saveregs=0x3c00efdc, restoreregs=0x2000972c <g_idletcb+140>) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  10   Thread 11 ([PID:010]thread-10:0005[PRI:101])        arm_switchcontext (saveregs=0x3c00a2ec, restoreregs=0x3c00efdc) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  11   Thread 13 ([PID:012]kvdbd:0005[PRI:100])            arm_switchcontext (saveregs=0x3c011cfc, restoreregs=0x3c013cdc) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  12   Thread 14 ([PID:013]rpmsg-gpio:0005[PRI:224])       arm_switchcontext (saveregs=0x3c012acc, restoreregs=0x3c00efdc) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  13   Thread 15 ([PID:014]rpmsg-uorb-audio:0005[PRI:100]) arm_switchcontext (saveregs=0x3c013cdc, restoreregs=0x3c014e2c) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
  14   Thread 16 ([PID:015]rpmsg-uorb-cp:0005[PRI:100])    arm_switchcontext (saveregs=0x3c014e2c, restoreregs=0x3c015fbc) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
```

如何解读输出信息：

- `*` (星号)：标记当前 GDB 上下文所在的线程（即当前活动线程）。
- `Id`：GDB 为每个线程分配的唯一标识符。后续的线程操作（如切换）将使用此 `Id`。
- `Target Id`：由 J-Link 插件报告的线程 ID。在 openvela 中，`Target Id` 与 `PID` 的关系通常是 `Target Id = PID + 1`。例如，`Thread 2` 对应的系统 `PID` 是 `1`。
- 括号内包含丰富的线程信息：
    - `PID`: 线程的进程 ID。
    - `Name`: 线程名称，如 `Idle Task`。
    - `PRI`: 线程的实时优先级。
- `Frame`：显示该线程当前停止的函数及代码位置。

### 2、切换活动线程 (`thread <Id>`)

使用 `thread` 命令并指定 GDB `Id`，可以将调试上下文切换到目标线程。

```Bash
(gdb) thread 4
[Switching to thread 4 (Thread 19)]
#0  arm_switchcontext (saveregs=0x3c015fbc, restoreregs=0x3c00efdc) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
121          return reg0;
```

执行此命令后，GDB 的焦点将切换到 `Id` 为 `4` 的线程（即 `PID` 为 `18` 的 `rpmsg-uorb-sens` 任务）。后续的调试命令（如查看调用栈、寄存器）都将针对此线程执行。

### 3、查看线程调用栈 (`bt`)

```Bash
(gdb) bt
#0  arm_switchcontext (saveregs=0x3c015fbc, restoreregs=0x3c00efdc) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
#1  0x2c016ab6 in up_block_task (tcb=tcb@entry=0x3c015f30, task_state=task_state@entry=TSTATE_WAIT_SEM) at armv8-m/arm_blocktask.c:139
#2  0x2c008338 in nxsem_wait (sem=sem@entry=0x3c016b44) at semaphore/sem_wait.c:153
#3  0x2c03d054 in poll_semtake (sem=0x3c016b44) at vfs/fs_poll.c:59
#4  nx_poll (fds=fds@entry=0x3c015ca8, nfds=32, timeout=1006721824) at vfs/fs_poll.c:439
#5  0x2c03d0c0 in poll (fds=fds@entry=0x3c015ca8, nfds=<optimized out>, timeout=<optimized out>) at vfs/fs_poll.c:500
#6  0x2c00927c in ppoll (fds=fds@entry=0x3c015ca8, nfds=738386121, nfds@entry=32, timeout_ts=timeout_ts@entry=0x0, sigmask=sigmask@entry=0x3c016c00) at signal/sig_ppoll.c:122
#7  0x2c02e0c8 in uorb_rpmsg_task (argc=<optimized out>, argv=<optimized out>) at uORB/uORBRpmsg.cpp:404
#8  0x2c00fa42 in nxtask_startup (entrypt=entrypt@entry=0x2c02dfd5 <uorb_rpmsg_task(int, char**)>, argc=<optimized out>, argv=<optimized out>) at sched/task_startup.c:151
#9  0x2c00971a in nxtask_start () at task/task_start.c:130
#10 0x00000000 in ?? ()
Backtrace stopped: previous frame identical to this frame (corrupt stack?)
```

通过调用栈，您可以清晰地追踪函数的调用路径，例如从任务入口 `nxtask_start` 到当前阻塞点 `arm_switchcontext`。

### 4、查看栈帧信息 (`info frame`)

此命令提供当前栈帧的详细信息，包括程序计数器（PC）、寄存器保存位置等。

```Bash
(gdb) info frame
Stack level 0, frame at 0x3c016b20:
 pc = 0x2c016f52 in arm_switchcontext (/home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121); saved pc = 0x2c016ab6
 called by frame at 0x3c016b20
 source language c.
 Arglist at 0x3c016b18, args: saveregs=0x3c015fbc, restoreregs=0x3c00efdc
 Locals at 0x3c016b18, Previous frame's sp is 0x3c016b20
 Saved registers:
  r7 at 0x3c016b18, lr at 0x3c016b1c
```

可以看到：

- 当前 PC 指针地址为 `0x2c016f52`。
- 上下文保存的地址为 `saveregs=0x3c015fbc`。
- 恢复的地址为 `restoreregs=0x3c00efdc`。

### 5、查看寄存器 (`info registers`)

此命令显示当前活动线程上下文中的所有 CPU 寄存器值。

```Bash
(gdb) info registers
r0             0x2                 2
r1             0x3c015fbc          1006723004
r2             0x3c00efdc          1006694364
r3             0x3c015fbc          1006723004
r4             0x3c015f30          1006722864
r5             0x80                128
r6             0x3c015f28          1006722856
r7             0x3c016b18          1006725912
r8             0x3c015ca8          1006722216
r9             0x3c016b44          1006725956
r10            0x20                32
r11            0x20                32
r12            0x42                66
sp             0x3c016b18          0x3c016b18
lr             0x2c008339          738231097
pc             0x2c016f52          0x2c016f52 <arm_switchcontext+14>
xpsr           0x1100000           17825792
msp            0x0                 0
psp            0x0                 0
primask        0x0                 0
basepri        0x0                 0
faultmask      0x0                 0
control        0x0                 0
fpscr          0x0                 0
```

您可以查看通用寄存器（`r0-r12`, `sp`, `lr`, `pc`）以及特殊寄存器（`xpsr`, `primask` 等）的值，以进行深度调试。

## 五、相关资料

- [ELC-E Linux Awareness in Debugger (PDF)](https://events.static.linuxfound.org/sites/events/files/slides/ELC-E Linux Awareness.pdf)