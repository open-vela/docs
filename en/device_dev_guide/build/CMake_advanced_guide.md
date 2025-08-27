# CMake In-Depth Analysis and Maintenance Manual

\[ English | [简体中文](../../../zh-cn/device_dev_guide/build/CMake_advanced_guide.md) \]

This document is intended to serve as an in-depth technical reference for build system maintainers and advanced developers of openvela. It covers the internal architecture of the CMake build system, advanced development practices, and techniques for solving complex problems.

Before reading this document, it is recommended that you are familiar with the basic operations described in the [CMake Quick Start Guide](./CMake_quick_start.md).

## I. CMake Build System Architecture

This section provides a deep dive into the internal workflow and core design of the openvela CMake build system.

### 1. Overall Build Flow

The openvela CMake build process follows the standard NuttX framework, with `nuttx/CMakeLists.txt` as its entry point. The entire flow generates build rules during the `cmake` configuration phase and executes the compilation during the `--build` phase. It can be summarized into the following key stages:

1. **Configuration and Environment Check**: Performs basic CMake configuration, resolves core working directories like `NuttXDir` and `AppDir`, and executes fundamental sanity checks.
2. **Kconfig and Configuration Import**: Parses the `defconfig` file, identifies and links the `board`, `chip`, and `apps` directories, and generates a complete Kconfig tree. Subsequently, it generates the `.config` file and imports all macro definitions from it into the CMake environment as cache variables.
3. **Toolchain Loading**: Loads the corresponding CMake toolchain file based on configurations like `CONFIG_ARCH`, setting up the cross-compilation environment.
4. **Build Context Generation**: Executes modules like `mkconfig.cmake` and `gen_header.cmake` to generate necessary headers and configurations, such as `config.h` and `version.h`, ensuring the build environment is ready.
5. **Target Library Generation**: CMake iteratively traverses module directories such as `arch`, `drivers`, `mm`, `sched`, and `apps`, compiling the source files of each module and packaging them into corresponding static libraries (`.a` files).
6. **Final Artifact Linking**: Links all generated static libraries (`${nuttx_libs}`) to produce the `nuttx` ELF executable file.
7. **Artifact Post-Processing**: Executes user-defined `POST_BUILD` actions, such as generating `.bin` files via `objcopy` or packaging firmware.

The build steps are illustrated in the figure below:

<img src="./figures/013.png" alt="" width="60%">

### 2. Build Dependency Relationships

All modules are ultimately organized into different categories of library collections and linked to form the final product. The dependency relationship is shown in the figure below:

<img src="./figures/014.svg" alt="" width="100%">

## II. Advanced Development Practices Guide

### 1. Adapting Custom Boards and Chips

To add CMake support for your custom hardware, you need to create `CMakeLists.txt` files in the corresponding `board` and `chip` directories.

Example directory structure:

```Bash
# Location: vendor/vendor_name
├── boards
│   ├── <chip_name>
│   │   └── <board_name>
│   │       ├── Kconfig       
│   │       ├── CMakeList.txt        <-- Top-level board CMake file              
│   │       └── src
│   │           ├── Make.defs
│   │           └──  CMakeList.txt   <-- Board source CMake file
├── chips
│   └── chip_name
│       ├── Kconfig
│       ├── Make.defs
│       └──  CMakeList.txt      <-- Chip-level CMake file
```

Example `CMakeLists.txt` content:

1. `chips/<`**`chip_name`**`>/CMakeLists.txt`:

    ```Makefile
    # Add chip-related source files (e.g., startup files)
    set(SRCS chip_startup.S)

    # Add the source files to the 'arch' target, which will be archived into libarch.a
    target_sources(arch PRIVATE ${SRCS})
    ```

2. `boards/<`**`chip_name`**`>/<`**`board_name`**`>/src/CMakeLists.txt`:

    ```Makefile
    # Add board-level drivers and initialization source files
    set(SRCS board_source.c)

    # Add the source files to the 'board' target, which will be archived into libboard.a
    target_sources(board PRIVATE ${SRCS})
    ```

3. `boards/<`**`chip_name`**`>/<`**`board_name`**`>/CMakeLists.txt`:

    ```CMake
    # Include the src directory in the build
    add_subdirectory(src)

    # Set the path for the Linker Script
    set_property(GLOBAL PROPERTY LD_SCRIPT
    "${NUTTX_BOARD_ABS_DIR}/scripts/app.ld"
    )

    # Define a post_build target for automatic artifact processing after the build
    add_custom_target(
    nuttx_post_build ALL
    POST_BUILD
    COMMAND ${NUTTX_DIR}/../vendor/xxx/post_build.sh ${CMAKE_BINARY_DIR}
    )
    ```

### 2. Porting a Third-Party Library

#### Methodology: When to Reuse, When to Rewrite?

If a third-party library already provides a `CMakeLists.txt`, you can evaluate whether to reuse it.

**Decision Principle**: Follow this principle when choosing a porting method. You **should not reuse** a third-party library's `CMakeLists.txt` and should instead write a new adaptation script if any of the following conditions apply:

1. The third-party library does not support cross-compilation or has strong dependencies on the host platform.
2. The third-party library needs to be registered as a built-in application in openvela.
3. The third-party library's `CMakeLists.txt` contains compile options that cannot be controlled externally.
4. The third-party library's build script defines too many redundant targets or targets that conflict with the system.

If the third-party library is a pure static library without the issues above, you may consider reusing its build script.

#### Method 1 (Recommended): Write a New `CMakeLists.txt`

This method offers the greatest flexibility and control by completely rewriting the build logic. For details, refer to the [Basic Porting Method](./CMake_quick_start.md#basic-porting-method-recommended) section in the CMake Quick Start guide.

#### Method 2: Reuse via `add_subdirectory`

- **Description**: This method uses `add_subdirectory()` to include the third-party library as a subproject and integrates its library target into openvela using `nuttx_add_external_library`.
- **Characteristics**: Allows reuse of external scripts, reducing the amount of porting code. However, it may introduce redundant or conflicting targets, requiring a careful evaluation of its `CMakeLists.txt`.
- **Example** (`libpng`):

    ```Makefile
    # Control its build behavior by setting its CACHE variables externally
    set(PNG_SHARED OFF CACHE BOOL "Disable libpng shared library" FORCE)
    set(PNG_EXECUTABLES OFF CACHE BOOL "Disable libpng executable" FORCE)
    set(PNG_TESTS OFF CACHE BOOL "Disable libpng tests program" FORCE)

    # Add the third-party library as a subdirectory
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/libpng
                    ${CMAKE_CURRENT_BINARY_DIR}/libpng EXCLUDE_FROM_ALL)

    # Integrate the target defined by the third-party library into the openvela build environment
    nuttx_add_external_library(png_static)
    ```

#### Method 3: Independent Build via `ExternalProject_Add`

- **Description**: This method initiates a completely separate sub-build process to compile the third-party library and then brings its build artifacts into the main project as an `IMPORTED` library.
- **Characteristics**: Provides good isolation but is complex, requiring manual handling of toolchain passing and artifact importing.
- **Example** (`libpng`):

    ```Makefile
    # Manually pass openvela's cross-compilation toolchain info to the sub-build process
    set(FLAGS_ARGS "$<JOIN:$<TARGET_PROPERTY:nuttx,COMPILE_OPTIONS>, >")
    set(EXTERN_C_FLAGS "${CMAKE_C_FLAGS} ${FLAGS_ARGS}")
    ExternalProject_Add(
        libpng_external
        SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/libpng/
        BINARY_DIR ${CMAKE_BINARY_DIR}/external/libpng_external
        CMAKE_ARGS
            -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
            -DCMAKE_C_FLAGS=${EXTERN_C_FLAGS}
            -DPNG_SHARED=OFF
            -DPNG_EXECUTABLES=OFF
            -DPNG_TEST=OFF
        TEST_COMMAND ""
        INSTALL_COMMAND ""
    )

    # Bring the sub-build's artifacts into the main build process as an IMPORTED library
    add_library(libpng STATIC IMPORTED GLOBAL)
    set_target_properties(libpng PROPERTIES
        IMPORTED_LOCATION ${CMAKE_BINARY_DIR}/external/libpng_external/libpng.a
    )
    add_dependencies(libpng libpng_external)
    set_property(GLOBAL APPEND PROPERTY NUTTX_SYSTEM_LIBRARIES libpng)
    ```

## III. FAQ

### 1. How can I make a module's header files visible to all other modules?

Use the `nuttx_export_header()` function.

- **Background**: The `PUBLIC` keyword of `target_include_directories()` is only effective for targets with an explicit dependency relationship (via `target_link_libraries`). In NuttX's flat module structure, there are typically no direct link dependencies between modules, so `PUBLIC` cannot propagate include paths.
- **Solution**: `nuttx_export_header()` adds the exported include directory path to a global property, making it visible to all subsequent targets.

    ```CMake
    # nuttx/cmake/nuttx_export_header.cmake

    # Usage:
    #   nuttx_export_header(TARGET <string> INCLUDE_DIRECTORIES <list>)

    # Example (in the CMakeLists.txt for libtommath):
    nuttx_export_header(TARGET libtommath INCLUDE_DIRECTORIES ${LIBTOMMATH_DIR})
    ```

- **Usage Recommendation**: This method is suitable for common base libraries. For dependencies between specific libraries, it is still recommended to manage them explicitly using `nuttx_add_dependencies()`.

### 2. How can I remove or override global compile options?

**Problem**: The toolchain's default compile options (e.g., `-march`, `-mabi`) conflict with the requirements of a specific chip (e.g., `-mcpu`). How can this be resolved?

**Solution**: Use the `nuttx_remove_compile_options()` function.

- **Background**: In Makefiles, the toolchain's default settings can be overridden by redefining `ARCHCPUFLAGS` in `Make.defs`. CMake's `add_compile_options()` has no direct inverse operation, so openvela provides this enhanced function.

- **Example**:

    ```CMake
    # For example, with a custom toolchain for a RISC-V architecture where
    # -march and -mabi conflict with -mcpu

    # CMake does not provide an inverse operation for add_compile_options(),
    # so we can use the enhanced function nuttx_remove_compile_options(ARGS) here.
    # For this custom RISC-V architecture, remove the conflicting options.
    nuttx_remove_compile_options(-march -mabi)

    # CFLAGS before removal: -O2 -g -march=rv32if -mabi=ilp32f -mcpu=e907fp
    # CFLAGS after removal:  -O2 -g -mcpu=e907fp
    ```

## Appendix

### Core CMake Modules

NuttX's CMake modules are defined in the `nuttx/cmake/` directory. They are the core extensions of the build system, providing encapsulated, specialized functions, analogous to the `tools` and `.mk` scripts in the Makefile system.

| **Module File**                      | **Function Description**                                                                                     |
| :----------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| `menuconfig.cmake`                   | Defines configuration targets like `menuconfig` based on Kconfig-frontend.                                   |
| `nuttx_add_application.cmake`        | A wrapper function for adding NuttX built-in applications.                                                   |
| `nuttx_add_dependencies.cmake`       | An enhanced `add_dependencies` that can automatically pass the include directories of dependent targets.     |
| `nuttx_add_library.cmake`            | An enhanced wrapper function for CMake's `add_library`.                                                      |
| `nuttx_add_module.cmake`             | A wrapper function for generating independent kernel modules (`.ko`).                                        |
| `nuttx_add_romfs.cmake`              | A wrapper function for adding and generating a ROMFS image.                                                  |
| `nuttx_add_subdirectory.cmake`       | An enhanced wrapper function for CMake's `add_subdirectory`.                                                 |
| `nuttx_add_symtab.cmake`             | Generates a symbol table for undefined symbols.                                                              |
| `nuttx_create_symlink.cmake`         | A method for creating symbolic links (symlinks).                                                             |
| `nuttx_export_header.cmake`          | Exports the include directories of a specified target to a global scope, making them visible to all modules. |
| `nuttx_generate_headers.cmake`       | Defines the `nuttx_context` target, used for generating necessary header files.                              |
| `nuttx_generate_outputs.cmake`       | Defines commands like `objcopy` for generating final artifacts such as `.bin` files.                         |
| `nuttx_kconfig.cmake`                | The core logic for Kconfig parsing and `.config` generation.                                                 |
| `nuttx_mkconfig.cmake`               | Generates `include/nuttx/config.h` based on the `.config` file.                                              |
| `nuttx_mkversion.cmake`              | Generates `include/nuttx/version.h` based on Git information.                                                |
| `nuttx_parse_function_args.cmake`    | An enhancement for CMake's built-in `cmake_parse_arguments` module.                                          |
| `nuttx_redefine_symbols.cmake`       | Used for the `sim` simulation platform to rename potentially conflicting symbols.                            |
| `nuttx_remove_compile_options.cmake` | An inverse operation to `add_compile_options`, used for removing global compile options.                     |
| `symtab.c.in`                        | A code generation template used in conjunction with `nuttx_add_symtab.cmake`.                                |

## References

- [CMake Quick Start Guide](./CMake_quick_start.md)
- [Makefile Build System Guide](./Makefile_guide.md)
