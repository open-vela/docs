# GDB Debugging Guide

\[ English | [简体中文](./../../../zh-cn/debugging_tools/GDB/GDB_debugging.md) \]

## I. Overview

This guide aims to provide developers with a comprehensive and practical manual for the GNU Debugger (GDB). Whether you are a beginner or a developer looking to deepen your embedded debugging skills, you will benefit from it.

### 1. What is GDB

GDB (GNU Debugger) is the standard debugger provided by the GNU Project. It is a powerful tool that works closely with the GCC compiler to help developers deeply understand and fix problems in their programs.

### 2. GDB's Core Capabilities

GDB provides the following four core capabilities, giving you complete control over program execution:

1. **Control Execution**: Start and run your program according to your specifications, including passing command-line arguments and setting environment variables.
2. **Set Breakpoints**: Set breakpoints at any point in the code (such as a specific line number or function entry) or create conditional breakpoints that trigger only when certain conditions are met.
3. **Examine State**: When the program is paused, you can inspect the current values of variables, view memory contents, trace the function call stack, and check register states.
4. **Dynamic Modification**: Dynamically change the values of variables or modify memory contents at runtime to test different code paths and hypothetical fixes.

## II. Preparation

Before starting a debug session, you must ensure that your program contains the debugging information required by GDB.

### 1. Compiling with Debug Information

When compiling your code with GCC, you must add the `-g` flag. For the most detailed debugging information (including macro definitions), it is recommended to use `-g3`:

```Bash
# Example compile command
gcc -g3 -o my_program my_program.c
```

In the **openvela** build system, you can enable debugging options via Kconfig, and the system will automatically add the appropriate flags for the compiler.

### 2. Installing GDB

For cross-platform embedded development (for example, debugging an ARM target from an x86 host), you need a multi-architecture version of GDB.

```Bash
# Install gdb-multiarch on Ubuntu/Debian systems
sudo apt install gdb-multiarch
```

For a specific ARM target, you can also use the GDB included in the corresponding toolchain, such as `arm-none-eabi-gdb`.

## III. GDB Core Command Reference

This section groups commands by function to help you quickly master GDB's core operations.

### 1. Launching and Exiting

| **Command**                 | **Description**                                                                                                                                                |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gdb ./nuttx`               | Loads the `nuttx` executable and enters the GDB interactive interface.                                                                                         |
| `attach <PID>`              | Attaches to a process already running in the background. <br>You first need to find the Process ID (PID) using `ps -ef \| grep nuttx`.                         |
| `target remote <IP>:<Port>` | Executed within GDB to connect to a GDB server running on a remote target. <br> For example, `target remote :1234` connects to port 1234 on the local machine. |
| `gdb -q ./nuttx`            | Starts GDB without displaying the verbose version and copyright information.                                                                                   |
| `quit`                      | `q`, **Exits** the GDB session.                                                                                                                                |
| `kill`                      | **Terminates** the program being debugged.                                                                                                                     |

### 2. Controlling Program Execution

| **Command** | **Description**                                                                                                                                                     |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `run`       | `r`, **Starts or restarts** the program.<br> The program runs until it hits a breakpoint, watchpoint, exception, or is manually interrupted.                        |
| `continue`  | `c`, **Continues execution** from the current pause point until the next breakpoint or the program terminates.                                                      |
| `next`      | `n`, **Step Over**.<br> Executes the current line of code. If the current line is a function call, it executes the entire function and then stops at the next line. |
| `step`      | `s`, **Step In**.<br> If the current line is a function call, it enters the function and stops at its first line.                                                   |
| `stepi`     | `si`, **Single Instruction Execution**.<br> Used for assembly-level single-stepping.                                                                                |
| `finish`    | `fin`, **Finish Current Function**.<br> Executes the remainder of the current function, then stops at the statement immediately after the function returns.         |
| `(Enter)`   | Repeats the last command (very useful for commands like `n`, `s`).                                                                                                  |

### 3. Managing Breakpoints and Watchpoints

Breakpoints pause the program at specific locations, while watchpoints pause it when a variable or memory address is accessed.

| **Command**                | **Description**                                                                                                                                                                      |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `break <location>`         | `b`, Sets a breakpoint at the specified location. <br> `<location>` can be a **line number** (`b main.c:25`), **function name** (`b my_function`), or **address** (`b *0xdeadbeef`). |
| `break ... if <condition>` | Sets a **conditional breakpoint**.<br> The breakpoint triggers only when `<condition>` evaluates to true.<br> For example: `b 15 if i == 10`.                                        |
| `info breakpoints`         | `info b`, Displays all breakpoints and their status, such as number, enabled/disabled state, and hit count.                                                                          |
| `delete <num>`             | `del`, Deletes the breakpoint with the specified number. If no number is given, deletes all breakpoints.                                                                             |
| `disable <num>`            | `dis`, Disables the specified breakpoint without deleting it.                                                                                                                        |
| `enable <num>`             | `en`, Re-enables a disabled breakpoint.                                                                                                                                              |
| `watch <expr>`             | Sets a **Write Watchpoint**.<br> The program pauses when the value of `<expr>` (typically a variable name or memory address) is **written to**.                                      |
| `rwatch <expr>`            | Sets a **Read Watchpoint**.<br> The program pauses when `<expr>` is **read from**.                                                                                                   |
| `awatch <expr>`            | Sets an **Access Watchpoint**.<br> The program pauses when `<expr>` is **read from or written to**.                                                                                  |

### 4. Inspecting Program State

When the program is paused, these commands help you investigate the source of the problem.

| **Command**              | **Description**                                                                                                                                                                                                                                                                                 |
| :----------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `print <expr>`           | `p`, Prints the value of a variable or expression. <br>For example, `p my_var` or `p *my_ptr`.                                                                                                                                                                                                  |
| `x/<nfu> <addr>`         | **Examine Memory**. <br> `n` is the count. <br> `f` is the format (`x`=hex, `d`=decimal, `c`=char, `s`=string).<br>`u` is the unit size (`b`=byte, `h`=halfword, `w`=word, `g`=giant word).<br>For example: `x/16xw 0x1000` displays 16 words of content in hex starting from address `0x1000`. |
| `backtrace`              | `bt`, Displays the current **function call stack**, helping you trace how execution reached the current location.                                                                                                                                                                               |
| `frame <num>`            | `f`, Switches to the stack frame with the specified number. Used with `bt`, it allows you to inspect local variables and arguments at any level of the call stack.                                                                                                                              |
| `info locals`            | Displays all **local variables** in the current stack frame.                                                                                                                                                                                                                                    |
| `info args`              | Displays all **function arguments** in the current stack frame.                                                                                                                                                                                                                                 |
| `info registers`         | Displays the current values of all CPU **registers**.                                                                                                                                                                                                                                           |
| `info threads`           | In a multi-threaded program (like openvela), displays all threads and their IDs.                                                                                                                                                                                                                |
| `thread <id>`            | Switches to the context of the specified thread ID.                                                                                                                                                                                                                                             |
| `ptype <expr>`           | Displays the **data structure definition** of a variable or type. For example:<br> `ptype struct my_struct`.<br>The `ptype /o <type>` command displays the complete memory layout for a specified type, detailing the offset and size of each member.                                           |
| `set var <name>=<value>` | **Modifies the value of a variable** at runtime. <br>For example, `set var i = 10`. When there is no ambiguity, you can use `set i = 10`                                                                                                                                                        |

### 5. Interacting with Source Code and Assembly

| **Command**          | **Description**                                                                                                                                                                          |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `list`               | `l`, Displays the source code around the current execution point.                                                                                                                        |
| `layout src`         | Enters Text User Interface (TUI) mode with a **split view for source code**.                                                                                                             |
| `layout asm`         | Enters TUI mode with a **split view for assembly code**.                                                                                                                                 |
| `layout split`       | Enters TUI mode with a **split view showing both source and assembly code**.<br> In this mode, use the `focus` command or the shortcut `Ctrl + X` + `O` to switch focus between windows. |
| `Ctrl + X, A`        | Exits TUI mode and returns to the standard GDB command-line interface.                                                                                                                   |
| `disassemble <func>` | `disas`, Disassembles the specified function.<br> The `/m` argument mixes the source code with the disassembled instructions.                                                            |

### 6. GDB Environment and Shell Interaction

| **Command**                 | **Description**                                                                                  |
| :-------------------------- | :----------------------------------------------------------------------------------------------- |
| `help <command>`            | Displays help information for the specified GDB command.                                         |
| `pipe <cmd> \| <shell_cmd>` | Pipes the output of the GDB command `cmd` to a shell command.<br>For example: `pipe bt \| less`. |
| `shell <shell_cmd>`         | Executes a shell command from within GDB.<br>For example: `shell ls -l`.                         |

## IV. Typical openvela Debugging Scenarios

This section applies theory to practice, showing how to use GDB to solve specific problems encountered during openvela development (especially for `sim` and hardware targets).

### Scenario 1: Analyzing a Program Crash (Hard Fault)

#### Problem Description

The program crashes unexpectedly on the `sim` environment or a development board, resulting in an ASan error, segmentation fault, or a hardware exception (such as a Data Abort or Prefetch Abort).

#### Debugging Strategy

1. Reproduce the Issue: Start a debugging session with `gdb ./nuttx`, then type `r` to run the program until it crashes.
2. Locate the Crash Point: GDB will automatically pause when the program crashes. Use the `bt` command to view the call stack. The top-most frame is usually the direct cause of the crash.
3. Analyze the Context: Use `frame <num>` to switch to a suspicious stack frame. Then, use `p <var>` and `info locals` to inspect variable values at that time to determine the cause of the crash.
4. Analyze Hardware Exceptions: For hardware exceptions, it is crucial to check the values of registers such as PC (Program Counter) and LR (Link Register) using `info registers`. Use `disassemble /m <PC_value>` to view the assembly instruction being executed at the time of the crash and its corresponding source code line.

### Scenario 2: Program Hangs or Deadlocks

#### Problem Description

The terminal becomes unresponsive after the program starts, and CPU usage is high, suggesting an infinite loop or deadlock.

#### Debugging Strategy

1. Interrupt the Program:

    - If the program is running in the foreground, press `Ctrl + C` in GDB.
    - If the program is running in the background, find its PID with `ps`, then execute `sudo gdb attach <PID>`. The program will pause automatically upon attachment.
    - For the `sim` environment, you can also execute `pkill -SIGSTOP nuttx` in a new terminal to pause the process.

2. Check All Threads: Enter `info threads` to view the status of all threads. Check if any threads are in an abnormal state or are all waiting for the same resource.
3. Analyze Each Thread: Use `thread <id>` to switch to each thread one by one, then use `bt` to view its call stack to determine what task it is performing. This can often quickly pinpoint the location of the infinite loop or deadlock.

### Scenario 3: Tracking Unintended Variable Modifications

#### Problem Description

A global variable's value is being incorrectly modified at some point, but there are multiple places in the code that could be responsible.

#### Debugging Strategy

1. Set a Watchpoint: After starting GDB, set a write watchpoint on the variable using `watch my_global_variable` or `watch *<address_of_variable>`.
2. Run and Wait: Type `run` or `continue` to start or resume program execution. The program will pause immediately when the variable's value is modified.
3. Locate the Modifier: GDB will report the old and new values of the variable and stop at the line of code that modified it. Use `bt` to view the call stack to find the code responsible for the change.

### Scenario 4: Analyzing Compiler-Optimized Variables

#### Problem Description

When trying to inspect a local variable with `print` after compiling with optimizations (such as `-O2` or `-O3`), GDB reports `<optimized out>`.

#### Cause Analysis

For efficiency, the compiler may have eliminated the variable or stored its value in a CPU register instead of on the stack.

#### Debugging Strategy

1. **Check Variable Address Information**: Use `info address your_var`.
2. **Interpret the Output**: GDB will tell you where the variable is currently located.
    - If it says "in register r5", it means the variable's value is in the `r5` register, which you can view with `p $r5`.
    - If it indicates a stack address, you can still try to view the memory with `x/w <address>`.
3. **As a Last Resort**: If precise debugging is necessary, temporarily recompile with `-O0` to disable optimizations.

### Scenario 5: Remote-Debugging a Coredump File

#### Problem Description

A program compiled on a server crashes on a target device and generates a `coredump`. You need to analyze it locally, but the source code paths do not match.

#### Debugging Strategy

1. **Load the Coredump**: `gdb ./nuttx /path/to/coredump`

2. **View Original Paths**: Use `info source` to see the source paths recorded at compile time.

3. **Map Paths**: Use the `set substitute-path <original_path> <local_path>` command to substitute the path.

    ```Bash
    # Example: Map the server path to a local path
    set substitute-path /home/build-server/project/ /home/user/my_project/
    ```

4. **Begin Analysis**: After mapping the paths, you can use commands like `bt` and `list` to view the source code as usual.

## V. How GDB Works

### 1. Local Debugging

In local debugging, GDB and the program being debugged run on the same machine. GDB uses system calls provided by the operating system, such as `ptrace` (on Linux), to control and inspect the target process.

### 2. Remote Debugging

Remote debugging is the most common mode in embedded development. It uses a Client/Server architecture:

- **GDB Client**: Runs on your development host (for example, your PC).
- **GDB Server**: A lightweight program that runs on the target device (for example, an ARM development board).
- **Communication Protocol**: The two communicate via the GDB Remote Serial Protocol (RSP) over a medium like a serial port or a network (TCP/IP).

When you type `continue` in the GDB client, it sends the corresponding RSP command to the server. The server receives the command and directs the target program to continue execution. When the program hits a breakpoint, the server pauses it and sends status information back to the client for display via RSP.

## VI. Advanced Topics and Related Practices

### 1. Using GDB Scripts (Command Files)

When you need to execute a series of GDB commands repeatedly, you can write them into a text file (for example, `my_setup.gdb`) and then load it using the `source` command:

```Bash
source [-s] [-v] filename
```

- `-s` searches for the specified file in the system's PATH environment variable.
- `-v` enables verbose mode, showing each command as it is executed.

For more information, see [Debugging with GDB - Command Files (gnu.org)](https://ftp.gnu.org/old-gnu/Manuals/gdb/html_node/gdb_190.html)

### 2. Related Debugging Practices

- **IDE Integration**: For instructions on how to configure GDB in VSCode to debug the `sim` environment, please refer to [Debugging the sim environment in VSCode](./VSCODE_debugging.md)
- **Thread-Aware Debugging**: To better view openvela thread information in GDB, you can use J-Link's GDB plugin. For details, see [Enhancing openvela Thread Debugging with the J-Link GDB Plugin](../crash/JLINK/J_Link.md).

## VII. Troubleshooting

### GDB reports `ModuleNotFoundError: No module named 'encodings'` on startup

#### Cause

This is typically caused by an incompatibility between the Python version GDB depends on and the default or configured Python version in your system's environment. GDB uses internal Python scripts for extended features (such as pretty-printing), and it will fail to start if it cannot find the correct Python environment.

#### Solution

1. Confirm the Python Version GDB Needs: The error message often indicates the required version (for example, `python3.8`).

2. Install the Corresponding Version: Ensure this version of Python is installed on your system. You can refer to guides such as [How to Install and Switch Python Versions](https://www.rosehosting.com/blog/how-to-install-and-switch-python-versions-on-ubuntu-20-04/).

3. Configure `PYTHONHOME`: If the problem persists after installation, try setting the `PYTHONHOME` environment variable to force GDB to use the correct Python interpreter.

## VIII. References

- [GDB Official Documentation](https://www.gnu.org/software/gdb/documentation/)
- [GDB Command Cheat Sheet](https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf)
- [Interrupt Blog: Debugging Firmware with GDB](https://interrupt.memfault.com/blog/gdb-for-firmware-1) (An excellent blog series on GDB for embedded developers)
