# CMake Quick Start Guide

\[ English | [简体中文](../../../zh-cn/device_dev_guide/build/CMake_quick_start.md) \]

This document aims to comprehensively explain the background, advantages, and practical implementation of the openvela project's migration from the GNU Make to the CMake build system. It provides developers with a complete guide for migration, usage, and development.

If you are not yet familiar with CMake, it is recommended to review the following official resources first to better understand the content of this document:

- **CMake Official Tutorial:** https://cmake.org/cmake/help/latest/guide/tutorial/index.html
- **CMake Official Documentation:** https://cmake.org/documentation/

## I. Background: Why Migrate to CMake

To address growing project complexity and the demand for higher developer efficiency, openvela has decided to migrate its build system from the traditional GNU Make to the modern CMake. This upgrade is intended to solve a series of challenges related to compilation efficiency, reliability, and extensibility in the old system.

### 1. The Challenges of GNU Make

According to statistics, the current GNU Make-based build system suffers from the following core pain points:

- **Frequent Issues**: In 2023, out of **1,043** reported issues, **92** were directly related to the build system, accounting for **8.8%** of the total.
- **Low Efficiency**: A full CI build now takes over an hour, severely impacting development and continuous integration efficiency.
- **Poor Developer Experience**: Developers widely report slow compilation speeds, unreliable incremental builds, incomplete cleanup of build artifacts, and a lack of modular compilation capabilities.

### 2. Why Choose CMake

After researching and comparing mainstream build systems, we chose CMake for the following key reasons:

| Build System | Speed              | Auto-Dependency | Cross-Platform Support | Widespread Adoption | Ninja Generator | Community Size | Migration Cost       |
| :----------- | :----------------- | :-------------- | :--------------------- | :------------------ | :-------------- | :------------- | :------------------- |
| CMake        | Depends on Backend | Supported       | Supported              | Highest             | Supported       | Large          | Community Foundation |
| GN           | Fast               | Supported       | Supported              | Medium              | Supported       | Small          | From Scratch         |
| SCons        | Slow               | Supported       | Supported              | Medium              | Not Supported   | Small          | From Scratch         |

> **Note**: Data reference: [Stack Overflow 2023 Survey](https://survey.stackoverflow.co/2023/#most-popular-technologies-tools-tech)

With its mature ecosystem, powerful cross-platform capabilities, precise dependency management, and support for high-performance backends like Ninja, CMake is the best choice for this upgrade.

## II. Core Advantages: The Value of CMake

Migrating to CMake brings the following significant benefits to openvela developers:

- **Significantly Improved Compilation Speed**: Measurements show that even when using the same Makefile backend, CMake provides more than a 2x speed improvement. Performance can be further optimized by using the Ninja backend.
- **Out-of-Tree Builds**: Build artifacts are kept completely separate from the source code, ensuring a clean source tree. This feature also allows for parallel builds of multiple different configurations from the same source, greatly improving multi-target validation efficiency.
- **Precise Dependency Management**: CMake automatically analyzes dependencies between targets, ensuring the correctness and reliability of incremental builds and completely resolving the shortcomings of the old `mkdep` and `.depend` mechanisms.
- **Modular Compilation**: Developers can build and verify any specific module independently, facilitating rapid debugging, library distribution, and SDK integration.
- **Excellent Cross-Platform Support**: CMake natively supports development on various host environments, including Windows, Linux, and macOS. It seamlessly integrates with multiple build tools and IDEs like GNU Make, Ninja, and Xcode through its generators.
- **Improved Development and Debugging Experience**: CMake's syntax is clearer and easier to maintain and extend. Its deep integration with mainstream IDEs like VSCode and CLion provides developers with graphical tools for build configuration and debugging.

## III. Quick Start

### 1. Build Steps

You can configure and compile openvela in two simple steps.

```Bash
# Ensure the current working directory is nuttx/

# 1. Configure Phase: Generate the build system files
#    -B build: Specifies 'build' as the build directory (for an out-of-tree build)
#    -DBOARD_CONFIG=sim/nsh: Specifies the target board configuration.
#                          Can also be an absolute or relative path to a defconfig file.
#    -GNinja: (Optional) Specifies Ninja as the backend generator. Defaults to Makefile if not set.
cmake -B build -DBOARD_CONFIG=sim/nsh -GNinja

# 2. Build Phase: Execute the compilation
#    --build build: Specifies that the build should be run in the 'build' directory.
cmake --build build
```

### 2. Common Build Options

| **Option**          | **Alias** | **Description**                                 | **Example**                         |
| :------------------ | :-------- | :---------------------------------------------- | :---------------------------------- |
| `--build <dir>`     |           | Specifies the build directory and runs a build. | `cmake --build build`               |
| `--target <target>` | `-t`      | Builds only the specified target.               | `cmake --build build -t menuconfig` |
| `--parallel <jobs>` | `-j`      | Specifies the number of parallel build jobs.    | `cmake --build build --parallel 8`  |
| `--verbose`         | `-v`      | Prints detailed build logs.                     | `cmake --build build -v`            |
| `--clean-first`     |           | Runs a clean operation before building.         | `cmake --build build --clean-first` |

## IV. [IMPORTANT] Dual Build System Maintenance During the Transition Period

> **Note: This is a core rule that all developers must follow during the transition phase.**

To ensure a smooth project transition, openvela will support both Makefile and CMake build systems concurrently for a period of time. When you make any file modifications related to compilation (such as adding/deleting source files or changing compile options), you **must** update both the `Makefile` and the `CMakeLists.txt` file in the same directory to ensure the two systems behave identically.

## V. Daily Development Practices

This section guides developers on how to perform daily development tasks in the CMake environment.

### 1. Adding a New Application

To integrate a new application into the CMake build system, simply create a `CMakeLists.txt` file in the same directory as its `Makefile`.

```Bash
apps/
└── example/
    └── hello_main/
        ├── hello_main.c
        ├── Kconfig
        ├── Make.defs
        ├── Makefile
        └── CMakeLists.txt  <-- Add this file
```

Example `CMakeLists.txt` content:

```CMake
# Kconfig options (like CONFIG_EXAMPLES_HELLO) are automatically loaded as CMake variables
if(CONFIG_EXAMPLES_HELLO)
  # Call the nuttx_add_application function to register a built-in application
  nuttx_add_application(
    NAME      ${CONFIG_EXAMPLES_HELLO_PROGNAME}   # App name, from Kconfig
    SRCS      hello_main.c                        # Source file list
    STACKSIZE ${CONFIG_EXAMPLES_HELLO_STACKSIZE}  # Stack size, from Kconfig
    PRIORITY  ${CONFIG_EXAMPLES_HELLO_PRIORITY}   # Priority, from Kconfig
  )
endif()
```

Function Prototype Reference: `nuttx_add_application()`

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

### 2. Porting a Third-Party Library

#### Basic Porting Method (Recommended)

We recommend writing a new `CMakeLists.txt` file to adapt the third-party library for openvela. This allows for precise control over its build behavior.

```Bash
openvela                                 openvela
 └── external                             └── external
   └── ThirdPartyLib (Wrapper)              └── ThirdPartyLib (Wrapper)
       ├── Makefile           Add                ├── Makefile
       ├── Kconfig         =========>            ├── Kconfig
       ├── Make.defs                             ├── Make.defs
       └── ThirdPartyLib (Actual)                ├── CMakeLists.txt
                └── your changes                 └── ThirdPartyLib (Actual)
                                                          └── your changes
```

`CMakeLists.txt` structural template (using `libtommath` as an example):

```CMake
# Example source: nuttx/apps/math/libtommath/CMakeLists.txt

# 1. Enable Switch: Check if the library is enabled in Kconfig
if(CONFIG_MATH_LIBTOMMATH)

  # #####################################################
  # Config and Fetch Tommath lib
  # This stage is analogous to the 'context' preparation step in the original Makefile.
  # #####################################################
  
  # 2. Source Code Preparation: (Optional) If needed, use FetchContent to
  #    automatically download and extract the source code.
  set(LIBTOMMATH_DIR ${CMAKE_CURRENT_LIST_DIR}/libtommath)
  
  if(NOT EXISTS ${LIBTOMMATH_DIR})
    set(CONFIG_LIBTOMMATH_URL https://github.com/libtom/libtommath/archive)
    # Use CMake's FetchContent module to get external resources
    FetchContent_Declare(
      libtommath_fetch
      URL ${CONFIG_LIBTOMMATH_URL}/v${CONFIG_LIBTOMMATH_VERSION}.zip SOURCE_DIR
          ${CMAKE_CURRENT_LIST_DIR}/libtommath BINARY_DIR
          ${CMAKE_BINARY_DIR}/apps/math/libtommath/libtommath
      DOWNLOAD_NO_PROGRESS true
      TIMEOUT 30)

    FetchContent_GetProperties(libtommath_fetch)
    if(NOT libtommath_fetch_POPULATED)
      FetchContent_Populate(libtommath_fetch)
    endif()
  endif()

  # ########################################################
  # Sources: Add the third-party library's source files
  # ########################################################
  # 3. Source File Definition: Use file(GLOB ...) or list all required source files directly.
  file(GLOB CSRCS ${LIBTOMMATH_DIR}/*.c)  # Using file() here

  if(CONFIG_LIBTOMMATH_DEMOS)
    list(APPEND CSRCS ${LIBTOMMATH_DIR}/demo/shared.c) # You can also append individual files
  endif()

  # #########################################################
  # Include Directory: Path for the third-party library's headers
  # #########################################################
  # 4. Include Directory Definition: Specify the library's public include directory.
  set(INCDIR ${LIBTOMMATH_DIR})
  
  # ########################################################
  # Flags: Configure compile options for the third-party library
  # #######################################################
  # 5. Compile Flags Definition: (Optional) Set specific compile flags for this library.
  set(CFLAGS -Wno-format)

  # #########################################################
  # Library Configuration: Add the third-party library
  # #########################################################
 
  # 6. Register the Library Target: Define it as a static library using nuttx_add_library.
  nuttx_add_library(libtommath STATIC) 
  
  # 7. Configure the Library Target: Apply the source files, include paths,
  #    and compile options to the target.
  target_compile_options(libtommath PRIVATE ${CFLAGS})
  target_sources(libtommath PRIVATE ${CSRCS})
  target_include_directories(libtommath PRIVATE ${INCDIR})

  # ###########################################################
  # Applications Configuration: If there are applications, add them as before.
  # ###########################################################
  # 8. (Optional) Add Example Applications: If the library includes examples
  #    or test programs, they can be added here.
  if(CONFIG_LIBTOMMATH_TEST)
    nuttx_add_application(
      NAME
      ${CONFIG_LIBTOMMATH_TEST_PROGNAME}
      STACKSIZE
      ${CONFIG_LIBTOMMATH_TEST_STACKSIZE}
      PRIORITY
      ${CONFIG_LIBTOMMATH_TEST_PRIORITY}
      SRCS
      ${LIBTOMMATH_DIR}/demo/test.c
      INCLUDE_DIRECTORIES
      ${INCDIR}
      DEPENDS
      libtommath)
  endif()
endif()
```

For other porting methods, please see [Advanced Development Practices: Porting Third-Party Libraries](./CMake_advanced_guide.md#2-porting-a-third-party-library).

### 3. Adapting Custom Boards and Chips

To add CMake support for your custom hardware, you need to create `CMakeLists.txt` files in the corresponding `board` and `chip` directories.

Example directory structure:

```Bash
# Location: vendor/vendor_name
├── boards
│   ├── <chip_name>
│   │   └── <board_name>
│   │       ├── Kconfig       
│   │       ├── CMakeLists.txt     <-- Add this
│   │       └── src
│   │           ├── Make.defs
│   │           └── CMakeLists.txt   <-- Add this
├── chips
│   └── chip_name
│       ├── Kconfig
│       ├── Make.defs
│       └── CMakeLists.txt       <-- Add this
```

Example `CMakeLists.txt` content:

1. `chips/<`**`chip_name`**`>/CMakeLists.txt`:

    ```Makefile
    # Add the source files for the custom chip
    set(SRCS chip_startup.S)

    # Note: Add sources to the 'arch' target, which will be archived into libarch.a
    target_sources(arch PRIVATE ${SRCS})
    ```

2. `boards/<`**`chip_name`**`>/<`**`board_name`**`>/src/CMakeLists.txt`:

    ```Makefile
    # Add the source files for the custom board
    set(SRCS board_source.c)

    # Note: Add sources to the 'board' target, which will be archived into libboard.a
    target_sources(board PRIVATE ${SRCS})
    ```

3. `boards/<`**`chip_name`**`>/<`**`board_name`**`>/CMakeLists.txt`:

    ```CMake
    # Add the custom/board/src directory to the build structure
    add_subdirectory(src) 

    # Set the path to the linker script
    set_property(
    GLOBAL
    PROPERTY
        LD_SCRIPT
        "${NUTTX_BOARD_ABS_DIR}/scripts/app.ld"
    )

    # Define a post_build target for automatic processing of artifacts after the build
    add_custom_target(
        nuttx_post_build ALL
        POST_BUILD
        COMMAND ${NUTTX_DIR}/../vendor/xxx/post_build.sh ${CMAKE_BINARY_DIR}
    )
    ```

## VI. FAQ

### 1. What is the most important principle when writing CMakeLists.txt?

Maintain the purity of out-of-tree builds. You must ensure that all build operations are performed within the build directory (Binary Tree) and strictly avoid modifying the source directory (Source Tree). Operations like creating symbolic links or modifying files, which were common in the old Makefile system, should be migrated to execute within the build directory.

### 2. Is there a required format for CMake code?

**Yes**. openvela uses `cmake-format` from the `cmakelang` toolset to format CMake code. You must run the formatting command before committing code; otherwise, the CI check will fail.

```Makefile
# Reference: https://cmake-format.readthedocs.io/en/latest/cmake-format.html
# Install the tool
pip3 install cmake-format
# Format a file (in-place modification)
cmake-format -i CMakeLists.txt

# usage:
# cmake-format [-h]
#              [--dump-config {yaml,json,python} | -i]
#              [-c CONFIG_FILE]
#              infilepath [infilepath ...]
```

### 3. How should I handle dependencies between modules?

Use the `nuttx_add_dependencies()` function. It automatically adds the public include directories of a dependency to any module that depends on it.

```CMake
# Scenario: libtomcrypt depends on libtommath

# In libtommath's CMakeLists.txt:
nuttx_add_library(libtommath STATIC)
nuttx_export_header(TARGET libtommath INCLUDE_DIRECTORIES ${LIBTOMMATH_DIR})

# In libtomcrypt's CMakeLists.txt:
nuttx_add_library(libtomcrypt STATIC)
# libtomcrypt will automatically get the include path for libtommath
nuttx_add_dependencies(TARGET libtomcrypt DEPENDS libtommath)
```

### 4. How can I set unique compile options for a specific file?

Use the `set_source_files_properties()` function.

```CMake
# Use CMake's set_source_files_properties()
set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/source.c 
    PROPERTIES 
    COMPILE_FLAGS -O2)
```

### 5. How do I link a pre-compiled static library (.a file)?

Use the `nuttx_add_extra_library()` function.

```CMake
# Call the function
nuttx_add_extra_library(${NUTTX_CHIP_ABS_DIR}/libadc.a)
```

### 6. How can I customize post-build actions (like packaging firmware)?

- The original Makefile build provided a `POSTBUILD` macro for customizing post-build artifact handling.
- CMake offers a similar method:

```CMake
# Inside the custom board's CMakeLists.txt
# Define a custom 'nuttx_post_build' target
add_custom_target(
    nuttx_post_build ALL
    POST_BUILD
    # Define any custom post-build actions here
    COMMAND ${NUTTX_DIR}/../vendor/xxx/post_build.sh ${CMAKE_BINARY_DIR}
)
```

## References

- Further Reading: [CMake In-Depth Analysis and Maintenance Manual](./CMake_advanced_guide.md)
- Makefile: [Makefile Build System Guide](./Makefile_guide.md)
