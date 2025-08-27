# Add Hello World Example

\[ English | [简体中文](../../../../zh-cn/app_dev/system_apps/hello_world/Hello_World.md) \]

## Overview

This document is for developers, providing a detailed guide on how to add, configure, and run a new user application in the openvela operating system. openvela is built on the NuttX RTOS, and its modular design allows developers to easily integrate custom features or third-party libraries.

A typical functional module includes the following parts:

- **System Application**: A built-in function of the system, typically located in the `apps/` directory.
- **Third-Party Library**: An external dependency, usually placed in the `external/` directory.

This guide uses a `Hello, World!` example application to demonstrate the entire process, from code creation to building, running, and configuring auto-start.

An example directory structure is as follows:

```Bash
└── vela
    ├── apps
    │   └── examples
    │       ├── hello_main_1
    │       └── hello_main_2
    └── external
        ├── libs_1
        └── libs_2
```

## Step 1: Create the Hello World Example Framework

This section describes how to add a `Hello, World!` example application in openvela, including the core framework, file contents, and related build configurations.

### 1. Core Framework

The Hello World example application requires the following core files:

- `hello_main.c`: The application's source code, which contains the `main` function entry point.
- `Kconfig`: The build system's configuration file, used to provide selectable compilation options in `menuconfig`.
- `CMakeLists.txt`: The CMake build script, used to define source files, dependencies, and compilation rules.

An example directory structure is as follows:

```Bash
apps
 └── examples
     └── hello_main
         ├── hello_main.c
         ├── CMakeLists.txt
         ├── Kconfig
```

### 2. Write the Source Code (hello_main.c)

Create the `hello_main.c` file and add the following C code. This is the application's logical entry point.

```C
#include <stdio.h>

int main(int argc, char *argv[])
{
    printf("Hello, World!!\n");
    return 0;
}
```

If you need to use C++, ensure the `main` function is declared with `extern "C"` to maintain C-language linkage compatibility, allowing the system to call it correctly.

```C++
#include <iostream>

extern "C" int main(int argc, char *argv[])
{
    std::cout << "Hello, World!!" << endl;
    return 0;
}
```

### 3. Create the Kconfig Configuration File

Create the `Kconfig` file to define the application's compilation options. These options will appear in the `menuconfig` graphical interface, allowing users to enable or configure your application as needed.

```Makefile
config EXAMPLES_HELLO
        tristate "\"Hello, World!\" example"
        default n
        ---help---
                Enable the "Hello, World!" example

# The following options are only visible when EXAMPLES_HELLO is enabled
if EXAMPLES_HELLO

# Defines the command name for the application in openvela
config EXAMPLES_HELLO_PROGNAME
        string "Program name"
        default "hello"
        ---help---
                This is the name of the program that will be used when the NSH ELF
                program is installed.

# Defines the task priority of the application
config EXAMPLES_HELLO_PRIORITY
        int "Hello task priority"
        default 100

# Defines the stack size of the application
config EXAMPLES_HELLO_STACKSIZE
        int "Hello stack size"
        default DEFAULT_TASK_STACKSIZE

endif
```

### 4. Create the CMake Build Script

Create the `CMakeLists.txt` file. The openvela build system automatically loads all macro definitions from the `.config` file as CMake variables, so you can directly use the configurations defined in `Kconfig`.

```CMake
# Check if 'EXAMPLES_HELLO' is enabled in .config
if(CONFIG_EXAMPLES_HELLO) # Add to build if the feature is enabled in defconfig

  # Call nuttx_add_application to register the app as a built-in program
  nuttx_add_application(
    # NAME: Specifies the unique name of the application,
    #       typically matching PROGNAME in Kconfig
    NAME
    ${CONFIG_EXAMPLES_HELLO_PROGNAME}

    # SRCS: Specifies the list of source files;
    #       the file containing main should be first
    SRCS
    hello_main.c

    # STACKSIZE: Specifies the task stack size
    STACKSIZE
    ${CONFIG_EXAMPLES_HELLO_STACKSIZE}

    # PRIORITY: Specifies the task priority; defaults to
    #           SCHED_PRIORITY_DEFAULT if not provided
    PRIORITY
    ${CONFIG_EXAMPLES_HELLO_PRIORITY})
endif()
```

#### Definition of `nuttx_add_application()`

This CMake function is located in `nuttx/cmake/nuttx_add_application.cmake` and is used to add and configure applications.

```CMake
nuttx/cmake/nuttx_add_application.cmake

 Usage:
   nuttx_add_application( NAME <string> [ PRIORITY <string> ]
     [ STACKSIZE <string> ] [ COMPILE_FLAGS <list> ]
     [ INCLUDE_DIRECTORIES <list> ] [ DEPENDS <string> ]
     [ DEFINITIONS <string> ] [ MODULE <string> ] [ SRCS <list> ] )

 Parameters:
   NAME                : unique name of application
   PRIORITY            : priority
   STACKSIZE           : stack size
   COMPILE_FLAGS       : compile flags
   INCLUDE_DIRECTORIES : include directories
   DEPENDS             : targets which this module depends on
   DEFINITIONS         : optional compile definitions
   MODULE              : if "m", build module (designed to received
                         CONFIG_<app> value)
   SRCS                : source files
   NO_MAIN_ALIAS       : do not add a main=<app>_main alias(*)
```

## Step 2: Verify the Application

After creating the files, you need to configure, compile, and run your application using the following steps.

### 1. Clean the Build Environment (Optional)

If you have modified the Kconfig file or want to perform a completely clean build, it is recommended to clean the environment first.

```Bash
# Use distclean to clean all build artifacts and configurations
./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap  distclean -j8
```

### 2. Configure via menuconfig

Start `menuconfig` to enable your new application in the graphical interface.

```Bash
# Start menuconfig
./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap  menuconfig -j8
```

In the `menuconfig` interface, find and enable your application at the following path:
`Application Configuration` ---> `Examples` ---> `[*] "Hello, World!" example`

![img](./figures/001.png)

### 3. Compile and Run

After saving the `menuconfig` configuration, execute the build.

```Bash
# Build: 
./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap  -j8

# Run:
./emulator.sh vela
```

After the system starts, enter the program name you set in `Kconfig` (default is `hello`) in the NSH command line and press Enter. You will see the program's output.

![img](./figures/002.png)

## Step 3: Configure Application Auto-Start

openvela supports automatically running specified scripts at system startup. You can achieve application auto-start by editing the startup script.

### 1. Auto-Start Mechanism and Configuration

The openvela startup scripts are stored in the `/etc` directory, which is linked with the openvela binary as a `romfs` filesystem. It is automatically mounted by `nshlib` after the system starts. The relevant configurations are as follows.

Ensure your board-level configuration has the following `Kconfig` options enabled:

```Makefile
CONFIG_FS_ROMFS=y
CONFIG_NSH_ROMFSETC=y
CONFIG_NSH_ROMFSMOUNTPT="/etc"
CONFIG_NSH_SYSINITSCRIPT="init.d/rc.sysinit"
CONFIG_NSH_INITSCRIPT="init.d/rcS"
```

### 2. Startup Script Location

The default user startup scripts are located in the board-level configuration directory:

```Bash
vendor/openvela/boards/vela/src/etc/init.d/rc.sysinit    # System initialization script
vendor/openvela/boards/vela/src/etc/init.d/rcS           # User script 
```

### 3. Edit the Startup Script

Open the `rcS` file and add the command to execute your application.

```bash
#include <nuttx/config.h>

#ifdef CONFIG_FS_HOSTFS
mount -t hostfs -o fs=. /data # Mount the host filesystem to /data
#endif

hello    # Run hello in the foreground
hello &  # Run hello in the background
```

**Note:**

- **Use POSIX Threads**: Inside your application, it is recommended to use `pthread_create()` to create and manage child threads instead of calling the low-level `task_create()`. This ensures better portability and compatibility.
- **Guard the Main Thread**: If your main thread creates child threads, ensure the main thread only exits after all child threads have safely terminated. Otherwise, the exit of the main thread could cause the entire process to be reclaimed, forcibly terminating the child threads.
- **Create a Background Service**: For services that need to run long-term, you can run them in the background using `&` in the `rcS` script. The application itself would typically enter a loop (e.g., `while(1)`) to handle events or perform periodic tasks.

## References

To help you better understand and add `CMakeLists.txt`, here are reference materials and tool information:

- For the openvela CMake build system, please refer to [CMake Quick Start](../../../../en/device_dev_guide/build/CMake_quick_start.md).
