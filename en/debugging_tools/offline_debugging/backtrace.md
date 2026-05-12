# Backtrace User Guide

\[ English | [简体中文](../../../zh-cn/debugging_tools/offline_debugging/backtrace.md) \]

## I. Overview

In daily development, we often need to check the stack information of a specified thread, common scenarios include:

- Deadlock
- High CPU usage
- Busy Loop
- System crash
- Memory debugging

Typically, with the help of debugging tools such as JLink, this can be done in the form of 'gdb' and breakpoints (bps). However, after device packet publishing and peripheral debugging are turned off, these features are often unusable on real devices.

To solve this problem, openvela allows you to view the stack information of a specific thread in the runtime environment.

## II. Configuration Description

### 1. General configuration description

openvela supports common configurations for ARM, RISC-V, and Xtensa architectures, as follows:

```Makefile
# If the backtrace function is enabled, the function name will not be displayed by default
CONFIG_SCHED_BACKTRACE=y
CONFIG_SYSTEM_DUMPSTACK=y

# If you need symbol name support, enable the following options;
# If the Flash space is insufficient, you can manually parse the address to the symbol by addr2line
CONFIG_ALLSYMS=y

# Enable schema support
CONFIG_ARCH_HAVE_BACKTRACE=y
```

For the ARM platform, due to code resource limitations and Thumb-2 feature requirements, the following three backtrace implementations are available:

```Makefile
# Backtracking implementation based on frame pointer
CONFIG_UNWINDER_FRAME_POINTER

# Backtracking implementation based on stack pointer
CONFIG_UNWINDER_STACK_POINTER

# Backtracking implementation of .exidx segments based on ARM architecture
CONFIG_UNWINDER_ARM
```

Currently, openvela supports the backtrace function of ARM, RISC-V, and Xtensa architectures, and the configuration and implementation of each architecture are as follows.

### 2. ARM

#### ARM Cortex-A/R

In the ARM Cortex-A and Cortex-R families, the backtrace implementation supports one of two ways:

```Makefile
# Method 1: Backtrace implementation based on fp register 
CONFIG_UNWINDER_FRAME_POINTER 

# Method 2: Backtrace implementation based on .exidx section 
CONFIG_UNWINDER_ARM 

``` #### ARM Cortex-M 

In the ARM Cortex-M series, there are three implementations of backtrace, choose one according to project needs:

 ```Makefile 
 # Method 1: Backtrace implementation based on fp (注意编译器限制) 
 CONFIG_UNWINDER_FRAME_POINTER=y 
 
 # Method 2: Backtrace implementation based on sp, suitable for low-resource devices 
 CONFIG_UNWINDER_STACK_POINTER=y 

 # Method 3: Backtrace implementation based on .exidx section 
 CONFIG_UNWINDER_ARM=y 
 ```

- CONFIG_UNWINDER_FRAME_POINTER: There are related limitations on GCC compiler (for details refer to [GCC issues](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=92172)). 
- CONFIG_UNWINDER_STACK_POINTER: Obtains pc address through `bl`/`blx` instructions, suitable for resource-constrained devices, but has a certain probability of misjudgment. If the project code is scattered across multiple regions, multiple code regions need to be configured through the following API:

    ```C
    void up_backtrace_init_code_regions(FAR void **regions) 
    ```

- CONFIG_UNWINDER_ARM: Generates .exidx section during compilation, increasing the code size by 5%-8%.

### 3. RISC-V

In the RISC-V architecture, backtrace is implemented based on the frame pointer. Just enable the following configuration:

```Makefile
CONFIG_FRAME_POINTER=y 
CONFIG_SCHED_BACKTRACE=y 
```

 For more information, refer to: [RISC-V Backtrace Implementation](../../../../../../nuttx/blob/dev-ai-contest-2026/arch/risc-v/src/common/riscv_backtrace.c).

### 4. Xtensa
  
In the Xtensa architecture,  backtrace supports stack unwinding by default, and there is no need to enable the `-fno-omit-frame-pointer` option additionally. 

## III. Usage To use the backtrace series of functions 

In the code, the header file `#include <execinfo.h>` must be included. This chapter describes how to use backtrace to obtain function call stack information, print logs, and locate error lines. 

### 1. Using backtrace in code

Using the backtrace series of functions can capture the current program state and print stack information. Below is a description of common functions.

For more details, please refer to the Linux Man Page: [backtrace](https://man7.org/linux/man-pages/man3/backtrace.3.html).

```C
#include <execinfo.h> 

/* Store the current program state in the __array array. The maximum number of elements in array is __size. The return value is the actual number of elements stored */ 
extern int backtrace (void **__array, int __size) __nonnull ((1)); 

/* Function: Returns an array of strings that contains the information obtained from backtrace. Parameters: - __array: Pointer array returned by backtrace - __size: Return value of backtrace Note: This method will call `backtrace_malloc(FAR void *const *buffer, int size)` to allocate space, defined in nuttx/libs/libc/misc/lib_execinfo.c. */
 extern char **backtrace_symbols (void *const *__array, int __size) 
    __THROW __nonnull ((1)); 

/* Function: Similar to backtrace_symbols, but does not require additional space; it writes directly to the file descriptor __fd. 
*/ 
extern void backtrace_symbols_fd (void *const *__array, int __size, int __fd) __THROW __nonnull ((1));
```

### 2. `dump_stack()`

1. In the openvela system, you can directly call the `dump_stack()` function to print stack information. For example:

    ```C
    // Add test code in the examples/hello/hello_main.c file.
    37 int main(int argc, FAR char *argv[])
    38 {
    39   printf("Hello, World!!\n");
    +40   dump_stack();  // Print stack information  
    41   return 0;
    42 }
    ```

    Print output example:

    ```Bash
    ap> hello
    Hello, World!!
    [07:06:21] [28] [  INFO] [BackTrace|28|0]:   0xc070a96  0xc063d7c  0xc0809bc  0xc063d38  0xc0587de
    ```

2. Use the `addr2line` tool to resolve the printed backtrace addresses to specific code lines:

    ```Bash
    addr2line -fe nuttx 0xc070a96  0xc063d7c  0xc0809bc  0xc063d38  0xc0587de  
    ```

    Example of analysis results:

    ```Bash
    nuttx/arch/arm/src/armv8-m/arm_backtrace.c:446
    nuttx/libs/libc/sched/sched_dumpstack.c:60
    apps/examples/hello/hello_main.c:40
    nuttx/libs/libc/sched/task_startup.c:151
    nuttx/sched/task/task_start.c:130
    ```

3. Use the addresses from dump_stack() to locate the point of error, or print function names directly for easier analysis by [allsyms symbol table feature usage guide](./allsyms_guide.md).

### 3. `dumpstack` Command

In the command line, you can use the `dumpstack` command to obtain the backtrace of a specified task. Here is how to use it:

#### Use `dumpstack [pid]` to get the task stack

1. Obtain the stack of the process.

    ```Bash
    # Check Process Status
    ap> ps
    ...
    26       100 RR       Task    --- Waiting  Semaphore 00000010 004056 000648  15.9%    0.0% Telnet daemon 0x3c4293e0

    # View the backtrace of PID 26
    ap> dumpstack 26
    [15:18:53] [29] [  INFO] [BackTrace|26|0]:   0xc06b1c2   0x2154aa   0x20f312  0xc2ca118  0xc2c9bc4  0xc2c9c34  0xc08d894  0xc063d38
    [15:18:53] [29] [  INFO] [BackTrace|26|1]:   0xc0587de
    ```

2. Use `addr2line` to resolve the backtrace address.

    ```Bash
    addr2line -e nuttx 0xc06b1c2   0x2154aa   0x20f312  0xc2ca118  0xc2c9bc4  0xc2c9c34  0xc08d894  0xc063d38
    ```

3. Check the analysis results.

    An example of the analysis results is as follows:

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

#### Use `dumpstack [pid_start] [pid_end]` to view the stack of multiple processes

View the backtrace information for PIDs from 0 to 26:

```Bash
ap> dumpstack 0 26  
[15:21:07] [30] [  INFO] [BackTrace|0|0]:  0xc054ba0  0xc3129f0  0xc000056  
[15:21:07] [30] [  INFO] [BackTrace|1|0]:  0xc06b1c2  0xc0572e2  0xc0595e6  0xc0587d4  
[15:21:07] [30] [  INFO] [BackTrace|26|0]:  0xc06b1c2  0xc2154aa  0xc0587d4  
...  
```

### 4. Call stack analysis in crash logs

```Bash
[15:21:21] [25] [  INFO] [BackTrace|25|0]:   0xc070aa6  0xc063d7c  0xc070f58  0xc060948  0xc06b2a2  0xc054d1e  0xc070dc8  0xc06b21e
[15:21:21] [25] [  INFO] [BackTrace|25|1]:   0xc087556  0xc0847fa  0xc087864  0xc0889b4  0xc0837a8  0xc063d38  0xc0587de

crash thread 25:

$ addr2line -e nuttx 0xc070aa6  0xc063d7c  0xc070efc  0xc0569c8  0xc070fba  0xc060948  0xc06b2a2  0xc054d1e 0xc070dc8  0xc06b21e  0xc087556  0xc0847fa  0xc087864  0xc0889b4  0xc0837a8  0xc063d38
nuttx/arch/arm/src/armv8-m/arm_backtrace.c:446
nuttx/libs/libc/sched/sched_dumpstack.c:60
nuttx/arch/arm/src/armv8-m/arm_assert.c:167
```
