# Debugging the SIM Environment with VSCode

\[ English | [简体中文](./../../../zh-cn/debugging_tools/GDB/VSCODE_debugging.md) \]

## I. Overview

This guide provides a detailed explanation of how to configure and use GDB in Visual Studio Code (VSCode) for graphical debugging of the **openvela** `sim` simulation environment. VSCode offers a modern debugging experience, including setting breakpoints, viewing the call stack, and monitoring variables and memory, which significantly enhances development and troubleshooting efficiency.

**The core workflow includes:**

1. **Environment Preparation**: Install the necessary VSCode extensions.
2. **Project Configuration**: Create and configure the `launch.json` file to instruct VSCode on how to start a debug session.
3. **Debugging in Practice**: Demonstrate how to start debugging, set breakpoints, and analyze the program state with a practical example.
4. **Advanced Topics**: Address potential issues in specific scenarios, such as SMP and networking features.

## II. Prerequisites

Before you begin debugging, ensure your development environment meets the following requirements.

### 1. Environment Requirements

- **Visual Studio Code**: Must be installed.
- **C/C++ Extension**: The core plugin from Microsoft that provides C/C++ language support and debugging capabilities in VSCode.
- **Compiled `sim` Target**: The `sim` version of openvela must be successfully compiled, generating an executable (`nuttx`) that includes debugging information. The compilation must include the `-g` or `-g3` flag.

### 2. VSCode Environment Setup

#### Step 1: Install the C/C++ Extension

In the VSCode Marketplace, search for `C/C++` (published by Microsoft) and click Install.

#### Step 2: Open the Project Workspace

Launch VSCode and use the menu `File > Add Folder to Workspace...` to add your openvela project root directory. This ensures that VSCode correctly resolves the `${workspaceFolder}` variable in `launch.json`.

## III. Debug Configuration (`launch.json`)

The `launch.json` file is the core configuration file for VSCode's debugging functionality. It defines how to launch and attach to your program.

### 1. Create launch.json

1. Switch to the "Run and Debug" view in VSCode (shortcut: `Ctrl+Shift+D`).
2. Click the "create a launch.json file" link.
3. From the dropdown menu that appears, select **C++ (GDB/LLDB)**.
4. VSCode will automatically generate a `launch.json` template file and save it in the `.vscode` folder within your project's root directory.

### 2. Configure launch.json

Replace the contents of `launch.json` with the following configuration. This configuration is specifically tailored for debugging the openvela `sim` environment.

```JSON
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug openvela (sim)",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/nuttx/nuttx",
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}/nuttx",
            "environment": [],
            "console": "externalTerminal",
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```

#### Configuration Parameter Breakdown

| **Attribute**   | **Value**                        | **Description**                                                                                                                                                                                           |
| --------------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`          | `Debug openvela (sim)`           | The name of the debug configuration, which appears in the VSCode debug dropdown menu.                                                                                                                     |
| `type`          | `cppdbg`                         | Specifies using the C/C++ extension for debugging.                                                                                                                                                        |
| `request`       | `launch`                         | Indicates a launch type session, where VSCode is responsible for starting the program.                                                                                                                    |
| `program`       | `${workspaceFolder}/nuttx/nuttx` | **Key Parameter**.<br> Specifies the path to the executable file to be debugged. `${workspaceFolder}` represents the root directory of the project you have open in VSCode.                               |
| `stopAtEntry`   | `false`                          | If set to `true`, the program will automatically pause at the entry point (e.g., `_start`).<br>It is usually set to `false` to let the program run directly to your set breakpoints.                      |
| `cwd`           | `${workspaceFolder}/nuttx`       | Sets the working directory for the program being debugged.<br>For the `sim` environment, this is typically the directory containing the `nuttx` executable.                                               |
| `console`       | `externalTerminal`               | Specifies running the program in an **external terminal**.<br>This is crucial for the `sim` environment, which requires interaction with the NuttShell (NSH), as you can input commands in this terminal. |
| `MIMode`        | `gdb`                            | Specifies GDB as the debugger backend.                                                                                                                                                                    |
| `setupCommands` | `[...]`                          | Commands to be executed after GDB starts but before the program runs.<br>By default, this enables 'pretty-printing' to display complex data structures like STL in a more readable format.                |

## IV. Debugging in Practice

Next, we will walk through the entire process using the `ping` command as an example.

### Step 1: Open Source Code and Set a Breakpoint

In VSCode, open the file `apps/system/ping/ping.c`. At the entry of the `ping_main` function (or any line you are interested in), click in the margin to the left of the line number to set a red dot breakpoint.

### Step 2: Start the Debug Session

Press `F5` or click the green start button in the "Run and Debug" view. VSCode will:

- Launch GDB.
- Open a new external terminal window.
- Run the `nuttx` program in that terminal, where you will see the NSH startup prompt `nsh>`.

### Step 3: Trigger the Breakpoint

In the **external terminal** where the `nsh>` prompt is displayed, enter the command to trigger the breakpoint:

```Bash
nsh> ping 127.0.0.1
```

### Step 4: Analyze the Program State

When the program execution reaches `ping_main`, you will see:

- The VSCode window automatically gains focus.
- The line with the breakpoint is highlighted in the code editor.
- The debug panel on the left is populated with real-time information:
    - **VARIABLES**: Displays the values of local and global variables in the current scope.
    - **WATCH**: Allows you to add expressions to continuously monitor their values.
    - **CALL STACK**: Clearly shows the function call stack, helping you understand the program's execution path.
    - **BREAKPOINTS**: Manages all the breakpoints you have set.

## V. Advanced Topics and FAQ

### 1. Handling the SIGUSR1 Signal in SMP Debugging

#### Symptom

If your openvela configuration has Symmetric Multiprocessing (SMP) enabled, the program might unexpectedly pause due to a `SIGUSR1` signal shortly after starting a debug session.

#### Cause Analysis

In SMP mode, openvela uses the `SIGUSR1` signal for inter-core task scheduling and communication. By default, GDB intercepts all signals and pauses the program, which interferes with the system's normal operation.

#### Solution

You can instruct GDB to ignore this signal by creating a global GDB initialization script.

1. Create a file: `~/.gdbinit` (located in your user home directory).
2. Add the following command to the file:

    ```gdb
    # Instruct GDB to not stop or print a message for SIGUSR1
    handle SIGUSR1 nostop noprint
    ```

3. Save the file. GDB will automatically load and execute the commands in this file every time it starts, thus resolving the issue.

### 2. Acquiring Root Privileges for `sim`

#### Scenario

Certain advanced features of the `sim` environment, especially those related to networking (like using a TAP device to communicate with the host system), require root privileges to function correctly. Directly using `sudo F5` is not feasible.

#### Solution

The recommended approach is to configure `sudo` to allow your user account to run gdb as root without a password.

1. Configure passwordless `sudo`.

    For security and best practice, we will create a dedicated configuration file in the `/etc/sudoers.d/` directory. This method is safer than directly modifying the main `sudoers` file.

    Execute the following command in your Linux terminal, replacing `your_username` with your actual username:

    ```bash
    # Replace your_username with your actual username
    echo "your_username ALL=(ALL) NOPASSWD: /usr/bin/gdb" | sudo tee /etc/sudoers.d/gdb-nopasswd
    ```

2. Create a GDB wrapper script.

    In your project's root directory (for example, `openvela/`), create a file named `sudo-gdb.sh` and add the following content:

    ```bash
    #!/bin/bash
    # This script acts as a wrapper to launch gdb with sudo.
    sudo /usr/bin/gdb "$@"
    ```

    Then, grant the script execute permissions:

    ```bash
    chmod +x sudo-gdb.sh
    ```

3. Modify `launch.json`.

    Modify the `.vscode/launch.json` file by adding the `"miDebuggerPath"` property to your debug configuration, pointing it to the script we just created.

    ```json
    {
        "name": "Debug openvela (sim) with Root",
        "type": "cppdbg",
        "request": "launch",
        "program": "${workspaceFolder}/nuttx/nuttx",
        "miDebuggerPath": "${workspaceFolder}/sudo-gdb.sh", // <-- Add this line
        "stopAtEntry": false,
        "cwd": "${workspaceFolder}/nuttx",
        "environment": [],
        "console": "externalTerminal",
        "MIMode": "gdb",
        "setupCommands": [
            {
                "description": "Enable pretty-printing for gdb",
                "text": "-enable-pretty-printing",
                "ignoreFailures": true
            }
        ]
    }
    ```

After completing these steps, select the new debug configuration and press `F5` to start. Your `sim` program will now run with root privileges.

## VI. References

- [Visual Studio Code Docs: Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [MCU on Eclipse: VS Code for C/C++ with ARM Cortex-M](https://mcuoneclipse.com/2021/05/01/visual-studio-code-for-c-c-with-arm-cortex-m-part-1/)
- [MCU on Eclipse: VS Code Data Breakpoints and Watchpoints](https://mcuoneclipse.com/2023/11/14/vs-code-data-breakpoints-and-watchpoints/)
- [Gunnar Peipman's Blog: Browse WSL files with Windows Explorer](https://gunnarpeipman.com/browse-wsl-with-explorer/)