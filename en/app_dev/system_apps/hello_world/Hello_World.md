# Add Hello World Example

\[ English | [简体中文](../../../../zh-cn/app_dev/system_apps/hello_world/Hello_World.md) \]

## I. Overview

openvela is built based on the open-source operating system NuttX, which further provides a variety of complex system-level services. To make openvela more comprehensive and feature-rich, it is necessary to introduce a complete development framework or functional module. A complete development framework typically includes the following two components:

- System Applications: Internally developed system applications, usually stored in folders such as `apps/` and others.
- Third-Party System Libraries: Integration of third-party libraries and their adaptation, usually stored in folders such as `external/` and others.

The directory structure for new features and frameworks is shown in the figure below:

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

## II. Add Hello World Example

This section describes how to add a `Hello World` example application in openvela, including the main framework, file contents, and related build configurations.

### 1. Main Framework

The Hello World example application needs to include the following core files:

- `hello_main.c`: Defines the main logic of the application.
- `Kconfig`: Defines conditional compilation macros for feature trimming.
- `CMakeLists.txt`: Organizes the build system for openvela using `CMake`.
- `Make.defs`: Indicates whether the current directory needs to be compiled and must be included by the parent directory.
- `Makefile`: Defines the internal file compilation rules and compilation flags (FLAGS) for the library.

An example of the directory structure is shown below:

```Bash
apps
 └── examples
     └── hello_main
         ├── hello_main.c
         ├── CMakeLists.txt
         ├── Kconfig
         ├── Make.defs
         └── Makefile
```

### 2. File contents

#### hello_main.c

The file `hello_main.c` should contain the basic C application logic:

```C
#include <stdio.h>

int main(int argc, char *argv[])
{
    printf("Hello, World!!\n");
    return 0;
}
```

To add a C++ application, the entry function (`main`) needs to use the `extern "C"` declaration to ensure compatibility with the higher-level interface:

```C++
#include <iostream>

extern "C" int main(int argc, char *argv[])
{
    std::cout << "Hello, World!!" << endl;
    return 0;
}
```

#### Kconfig

Here's an example of what a `kconfig` file looks like:

```plaintext
config EXAMPLES_HELLO
        tristate "\"Hello, World!\" example"
        default n
        ---help---
                Enable the \"Hello, World!\" example

if EXAMPLES_HELLO
# The following directives default "hello" need to be run :
config EXAMPLES_HELLO_PROGNAME
        string "Program name"
        default "hello"
        ---help---
                This is the name of the program that will be used when the NSH ELF
                program is installed.

config EXAMPLES_HELLO_PRIORITY
        int "Hello task priority"
        default 100

config EXAMPLES_HELLO_STACKSIZE
        int "Hello stack size"
        default DEFAULT_TASK_STACKSIZE
        
endif
```

#### CMakeLists.txt

Here's an example of the contents of a `CMakeLists.txt` file, where all the configuration variables can be used directly:

```CMake
# All the configurations in .config are loaded into the CMake environment, so the variables can be used directly

# Enable Config, which replaces the configuration of the original Make.defs configured_apps
if(CONFIG_EXAMPLES_HELLO) # If defconfig enables this feature, add it to compilation
# call Add app module 'nuttx_add_application' Add hello as a builtin app.

nuttx_add_application(
NAME                                                 #Parameter flags: the unique name of the application
${CONFIG_EXAMPLES_HELLO_PROGNAME}                    #Parameter value: Set the value in hello kconfig as the name of the hello application
SRCS                                                 #Parameter flags: Source file
hello_main.c                                         #Parameter value: The source file of the application, which can be multiple, and the main must be the first
STACKSIZE                                            #Parameter flags: STACK SIZE
${CONFIG_EXAMPLES_HELLO_STACKSIZE}                   #Parameter value: takes the value set in Kconfig, and if you don't pass it, it is CONFIG_DEFAULT_TASK_STACKSIZE
PRIORITY                                             #Parameter flags: THE PRIORITY OF THE TASK
${CONFIG_EXAMPLES_HELLO_PRIORITY})                   #Parameter value: takes the value set in Kconfig, and if you don't pass it, it is SCHED_PRIORITY_DEFAULT
endif()
```

`nuttx_add_application()`

The CMake function is located in the `nuttx/cmake/nuttx_add_application.cmake` file and is used to add and configure the application.

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

#### Makefile

To add a new application in openvela, the core steps are to add the application’s entry source file to `MAINSRC` and to correctly define the following three essential parameters:

- `PROGNAME`: The name of the application, used when launching under `nsh`.

- `PRIORITY`: The execution priority of the application.

- `STACKSIZE`: The stack size allocated to the application.

These three settings are mandatory for building and running the application. 

Below is an example of a `Makefile` demonstrating how to configure them:

```Makefile
include $(APPDIR)/Make.defs

# Program name: can be taken from the Kconfig setting, or defined directly
PROGNAME = $(CONFIG_EXAMPLES_HELLO_PROGNAME)
# Or: PROGNAME = hello

# Application priority
PRIORITY = $(CONFIG_EXAMPLES_HELLO_PRIORITY)
# Or: PRIORITY = 100   (adjust as needed)

# Stack size for the application
STACKSIZE = $(CONFIG_EXAMPLES_HELLO_STACKSIZE)
# Or: STACKSIZE = 4096 (adjust as needed)

# Enable this module
MODULE = $(CONFIG_EXAMPLES_HELLO)

# Entry-point source file
MAINSRC = hello_main.c

# If you need to include additional headers, add them here, for example:
CFLAGS += ${INCDIR_PREFIX}$(APPDIR)/external/libs/include
# Which is equivalent to:
# CFLAGS += -I$(APPDIR)/external/libs/include

# For C++ projects, add include paths to CXXFLAGS:
# CXXFLAGS

# To include other internally developed source files, append them here:
# CSRCS += device_example.c

# For C++ source files, similarly:
# CXXSRCS += hello_main.cxx

# Finally, pull in openvela’s standard application build rules
include $(APPDIR)/Application.mk
```

When your project has multiple entry points, you can use #ifdef blocks or Kconfig-driven conditionals in the `Makefile` to select which MAINSRC (and related settings) to use. For example:

```Bash
ifeq ($(CONFIG_MAIN1),yes)
  PROGNAME += main1
  MAINSRC  += main1.c
endif

ifeq ($(CONFIG_MAIN2),yes)
  PROGNAME += main2
  MAINSRC  += main2.c
endif
```

If the C++ source file in your project does not have a suffix of `.cxx`, you need to specify the suffix in `Makefile` with the `CXXEXT` parameter. For example:

```Makefile
CXXEXT := .cpp
```

#### Make.defs

In the `Make.defs` file, you need to add the path of the application to the `CONFIGURED_APPS` so that the openvela build system can find the required path correctly:

```Makefile
ifneq ($(CONFIG_EXAMPLES_HELLO),)
CONFIGURED_APPS += $(APPDIR)/examples/hello_main
endif
```

## III. Verification and Testing

The newly added application must be cleaned and rebuilt before it can take effect. Follow these steps to verify:

### 1. Clean the Build

Run the following command to perform a clean:

```Bash
# clean the project  
./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap  distclean -j8
```

### 2. Configure via Menuconfig

Enable the new application in the `menuconfig`:

```Bash
# 启动 menuconfig  
./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap  menuconfig -j8
```

Inside `menuconfig`, navigate to and enable `hello_main`:

![img](./figures/001.png)

## 3. Build and Run

```Bash
# Build: 
./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap  -j8

# Run:
./emulator.sh vela
```

After booting, at the serial console prompt type the program name (as defined in your `Kconfig`). For example:

![img](./figures/002.png)

## IV. Implementing Application Auto-Start

openvela uses the NuttShell (NSH) startup script mechanism to run applications automatically at boot. The process is as follows:

1. During system startup, a pre-configured Read-Only File System (ROMFS) is mounted to the `/etc` directory.
2. After the mount is complete, NSH automatically executes the `/etc/init.d/rcS` script file.
3. To enable auto-start for an application, add its launch command to the `rcS` script.

### 1. Enabling the Auto-Start Feature

To use this feature, enable the following options in your build configuration using the Kconfig system.

| Configuration Option       | Recommended Value     | Description                                                                                     |
| :------------------------- | :-------------------- | :---------------------------------------------------------------------------------------------- |
| `CONFIG_FS_ROMFS`          | `y`                   | Enables ROMFS support, which is required to store the startup script.                           |
| `CONFIG_NSH_ROMFSETC`      | `y`                   | Enables the automatic mounting of the ROMFS to the `/etc` directory at system startup.          |
| `CONFIG_NSH_ROMFSMOUNTPT`  | `"/etc"`              | Specifies the mount point path for the ROMFS.                                                   |
| `CONFIG_NSH_SYSINITSCRIPT` | `"init.d/rc.sysinit"` | Specifies the path to the system-level initialization script.                                   |
| `CONFIG_NSH_INITSCRIPT`    | `"init.d/rcS"`        | Specifies the path to the user-level initialization script, which is the file you need to edit. |

### 2. Editing the User Startup Script

#### Script Location

The file you need to modify is the user startup script, `rcS`.

- **User Script (Recommended to modify):** `vendor/openvela/boards/vela/src/etc/init.d/rcS`
- **System Script (Do not modify):** `vendor/openvela/boards/vela/src/etc/init.d/rc.sysinit`
  This script handles core system initialization. Modifying it may prevent the system from booting.

#### Script Writing Example

The following is an example of an `rcS` script. NSH scripts support standard shell commands and are compatible with C preprocessor directives (e.g., `#ifdef`).

```bash
# NuttShell Script (rcS)

#include <nuttx/config.h>

# Use a C preprocessor directive to check if Host File System (Host FS) is configured.
#ifdef CONFIG_FS_HOSTFS
  # If configured, mount the host directory to /data.
  mount -t hostfs -o fs=. /data
#endif

# Start an application named "hello" in the foreground.
# The script blocks here until the hello program finishes execution.
hello

# Start an application named "hello" in the background.
# The "&" symbol runs the program in the background, allowing the script
# to continue to the next command immediately.
hello &
```

#### Important Considerations

1. Task Creation Methods.

    We recommend the following methods for applications that need to run at system startup:

    - **Start via NSH Script (Recommended)**: For most applications, the simplest and most robust method is to add the command to the `rcS` script and run it in the background using the `&` symbol.
    - **Start via Programmatic Interface**: For scenarios requiring complex initialization or dynamic task creation, you can use the standard POSIX function `pthread_create()` within your application to create new threads.

2. Thread Management.

    If your main application creates child threads using `pthread_create()`, ensure the main thread waits for all child threads to exit safely before it terminates. Prematurely exiting the main thread can cause child threads to be terminated unexpectedly, leading to system instability or resource leaks.