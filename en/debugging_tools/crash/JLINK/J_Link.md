# Using J-Link GDB Plug-in to Enhance openvela Thread Debugging  

\[ English | [简体中文](../../../../zh-cn/debugging_tools/crash/JLINK/J_Link.md) \] 

## I. Overview  

In standard embedded development workflows, when debugging with **SEGGER J-Link** and **GDB** (the GNU Project Debugger), **GDB** cannot recognize the thread model of **openvela** (based on NuttX RTOS) by default. This limitation prevents developers from listing all system threads or switching between them freely, significantly hindering debugging efficiency for multithreaded applications.  

This guide details how to extend **GDB** debugging capabilities using the **J-Link** **RTOS** plug-in, enabling thread-level debugging for openvela systems. You will learn to compile, configure, and use the plug-in to view thread information, switch thread contexts, and analyze call stacks for specific threads.  

## II. Prerequisites  

Ensure your development environment meets these requirements:  

- **SEGGER J-Link** drivers and tools are installed correctly.  
- A multi-architecture GDB toolchain (e.g., `gdb-multiarch`) is available.  
- The complete openvela project source code is accessible.  

## III. Operation Steps  

Follow these steps to compile and enable the thread debugging plug-in.  

### Step 1: Compile the RTOS Plug-in  

1. Locate the plug-in source code in NuttX's `tools` directory and compile the dynamic library (`.so`).  

    ```bash
    cd nuttx/tools
    ```  

2. Execute the `make` command to build the plug-in:  

    ```makefile
    make -f Makefile.host jlink-nuttx.so
    ```  

    A successful compilation generates `jlink-nuttx.so` in the current directory.  

### Step 2: Start J-Link GDB Server with Plug-in Loading  

Launch the J-Link GDB server with the `-rtos` parameter specifying the plug-in's absolute path:  

```bash
JLinkGDBServer -if SWD -device Cortex-M55 -rtos <your-nuttx-project-path>/nuttx/tools/jlink-nuttx.so
```  

- `-if SWD`: Sets the debug interface to SWD.  
- `-device Cortex-M55`: Specifies the target CPU core (modify for your hardware).  
- `-rtos`: Designates the RTOS plug-in path.  

### Step 3: Connect GDB Client and Verify Plug-in Loading  

1. Start the GDB client and connect to the J-Link GDB server (default port `2331`)  

    ```bash
    gdb-multiarch nuttx -ex "target remote localhost:2331"
    ```  

2. Check GDB startup messages for successful plug-in loading:  

    ```plaintext
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

## IV. Core Debug Commands and Result Analysis  

After loading the plug-in, use GDB's standard thread commands for openvela debugging.  

### 1. List All Threads (`info threads`)  

This command displays all running threads and their statuses:  

```bash
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

**Output interpretation:**

- `*`: Indicates the current GDB context thread (active thread).  
- `Id`: Unique GDB thread identifier for subsequent operations.  
- `Target Id`: Thread ID reported by J-Link plug-in (typically `Target Id = PID + 1` in openvela).  
- Parentheses contain:  
    - `PID`: Thread process ID.  
    - `Name`: Thread name (e.g., `Idle Task`).  
    - `PRI`: Thread priority.  
- `Frame`: Current function and code location.  

### 2. Switch Active Thread (`thread <Id>`)  

Switch debugging context to a target thread by GDB `Id`:  

```bash
(gdb) thread 4
[Switching to thread 4 (Thread 19)]
#0  arm_switchcontext (saveregs=0x3c015fbc, restoreregs=0x3c00efdc) at /home/zyl/code/m1ap/nuttx/include/arch/armv8-m/syscall.h:121
121          return reg0;
```  

This switches GDB focus to thread `Id 4` (the `rpmsg-uorb-sens` task with `PID 18`), directing subsequent commands to this thread.  

### 3. View Thread Call Stack (`bt`)  

```bash
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

With the call stack, you can clearly trace the path of a function, e.g. from the task entry `nxtask_start` to the current choke point `arm_switchcontext`.

### 4. View Stack Frame Details (`info frame`)  

This command provides detailed information about the current stack frames, including program counters (PC), register save locations, and so on.

```bash
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

Key insights:  

- Current PC address: `0x2c016f52`  
- Context save address: `saveregs=0x3c015fbc`  
- Context restore address: `restoreregs=0x3c00efdc`  

### 5. Display Register Values (`info registers`)  

View all CPU registers for the active thread:  

```bash
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

You can view the values of general registers (`r0-r12`, `sp`, `lr`, `pc`) as well as special registers (`xpsr`, `primask`, etc.) for in-depth debugging.

## V. Related Resources  

- [ELC-E Linux Awareness in Debugger (PDF)](https://events.static.linuxfound.org/sites/events/files/slides/ELC-E%20Linux%20Awareness.pdf)
