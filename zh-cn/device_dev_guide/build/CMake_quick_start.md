# CMake 快速入门

\[ [English](../../../en/device_dev_guide/build/CMake_quick_start.md) | 简体中文 \]

## 前言

本文档旨在完整阐述 openvela 项目从 GNU Make 迁移至 CMake 构建系统的背景、优势与具体实践，为开发者提供一套完整的迁移、使用与开发指引。

如果您对 CMake 尚不熟悉，建议先行阅览以下官方资源，以便更好地理解本文内容：

- **CMake 官方教程 (CMake Tutorial):** https://cmake.org/cmake/help/latest/guide/tutorial/index.html
- **CMake 官方文档 (CMake Documentation):** https://cmake.org/documentation/

## 一、背景：为何迁移至 CMake

为应对日益增长的项目复杂度和开发者对效率的需求，openvela 决定将其构建系统从传统的 GNU Make 迁移至现代化的 CMake。此次升级旨在解决旧有系统在编译效率、可靠性及可扩展性方面面临的一系列挑战。

### 1、GNU Make 的挑战

根据统计，当前基于 GNU Make 的构建系统存在以下核心痛点：

- **问题频发**：2023 年，在报告的 **1043** 个问题中，与编译系统直接相关的问题高达 **92** 个，占比 **8.8%**。
- **效率低下**：CI 全量编译耗时已超过一小时，严重影响开发与持续集成效率。
- **体验不佳**：开发者普遍反馈编译速度慢、增量编译不可靠、构建产物清理不彻底、缺乏模块化编译能力等问题。

### 2、为何是 CMake

我们对主流构建系统进行了调研和比较，最终选择 CMake 的核心原因如下：

| 构建系统 | 速度       | 自动依赖 | 跨平台支持 | 应用广泛程度 | Ninja生成器 | 社区规模 | 迁移成本   |
| :------- | :--------- | :------- | :--------- | :----------- | :---------- | :------- | :--------- |
| CMake    | 取决于后端 | 支持     | 支持       | 最高         | 支持        | 庞大     | 有社区基础 |
| GN       | 快         | 支持     | 支持       | 中           | 支持        | 较小     | 从零开始   |
| SCons    | 较慢       | 支持     | 支持       | 中           | 不支持      | 较小     | 从零开始   |

> **说明**：数据参考: [Stackoverflow 2023 survey](https://survey.stackoverflow.co/2023/#most-popular-technologies-tools-tech)

CMake 凭借其成熟的生态、强大的跨平台能力、精确的依赖管理以及对 Ninja 等高性能后端的支持，成为本次升级的最佳选择。

## 二、核心优势：CMake 带来的价值

迁移至 CMake 为 openvela 开发者带来以下显著价值：

- **显著提升编译速度**：实测表明，即使同为 Makefile 后端，CMake 的编译速度也有一倍以上的提升。若配合 Ninja 后端，性能将进一步优化。
- **支持源码外构建 (Out-of-Tree)**：将构建产物与源码完全分离，确保源码树的整洁。同时，此特性允许在同一份源码上并行构建多个不同的配置，极大提升多目标验证效率。
- **精确的依赖关系管理**：CMake 自动分析目标间的依赖关系，确保增量编译的正确性和可靠性，彻底解决了旧系统中 `mkdep` 和 `.depend` 机制的缺陷。
- **支持模块独立编译**：开发者可以独立构建和验证任一特定模块，便于快速调试、库文件发布及 SDK 的集成。
- **卓越的跨平台支持**：CMake 原生支持在 Windows、Linux 和 macOS 等多种主机环境下进行开发，并通过生成器无缝对接 GNU Make、Ninja、Xcode 等多种构建工具和 IDE。
- **改善开发与调试体验**：CMake 语法结构清晰，更易于维护和扩展。它与 VSCode、CLion 等主流 IDE 深度集成，为开发者提供了图形化的构建配置与调试功能。

## 三、快速上手

### 1、构建步骤

您可以通过以下两个简单步骤完成 openvela 的配置与编译。

```Bash
# 确保当前工作目录位于 nuttx/

# 1. 配置阶段：生成构建系统文件
#    -B build: 指定构建目录为 build (源码外构建)
#    -DBOARD_CONFIG=sim/nsh: 指定目标板级配置，也可是 defconfig 文件的绝对或相对路径
#    -GNinja: (可选) 指定使用 Ninja 作为后端生成器，不指定则默认为 Makefile
cmake -B build -DBOARD_CONFIG=sim/nsh -GNinja

# 2. 构建阶段：执行编译
#    --build build: 指定在 'build' 目录中执行构建
cmake --build build
```

### 2、常用构建选项

| **选项**            | **别名** | **描述**                 | **示例**                            |
| :------------------ | :------- | :----------------------- | :---------------------------------- |
| `--build <dir>`     |          | 指定构建目录并执行编译。 | `cmake --build build`               |
| `--target <target>` | `-t`     | 仅构建指定的目标。       | `cmake --build build -t menuconfig` |
| `--parallel <jobs>` | `-j`     | 指定并行编译的任务数。   | `cmake --build build --parallel 8`  |
| `--verbose`         | `-v`     | 输出详细的构建日志。     | `cmake --build build -v`            |
| `--clean-first`     |          | 在构建前先执行清理操作。 | `cmake --build build --clean-first` |

## 四、【重要】过渡期双构建系统维护须知

> **注意：此为过渡阶段所有开发者必须遵守的核心规则。**

为确保项目平稳过渡，openvela 将在一段时间内同时支持 Makefile 和 CMake 两个构建系统。当您进行任何与编译相关的文件修改（如增删源文件、修改编译选项）时，必须同时更新 `Makefile` 和同级目录下的 `CMakeLists.txt` 文件，以确保两个系统行为一致。

## 五. 日常开发实践

本章节指导开发者如何在 CMake 环境下进行日常开发。

### 1、添加新应用

要将一个新应用集成到 CMake 构建系统中，只需在其 `Makefile` 同级目录下创建一个 `CMakeLists.txt` 文件。

```Bash
apps/
└── example/
    └── hello_main/
        ├── hello_main.c
        ├── Kconfig
        ├── Make.defs
        ├── Makefile
        └── CMakeLists.txt  <-- 新增此文件
```

`CMakeLists.txt` 内容示例：

```CMake
# Kconfig 中的配置项 (如 CONFIG_EXAMPLES_HELLO) 已自动加载为 CMake 变量
if(CONFIG_EXAMPLES_HELLO)
  # 调用 nuttx_add_application 函数注册一个内置应用
  nuttx_add_application(
    NAME      ${CONFIG_EXAMPLES_HELLO_PROGNAME}   # 应用名，从 Kconfig 获取
    SRCS      hello_main.c                        # 源文件列表
    STACKSIZE ${CONFIG_EXAMPLES_HELLO_STACKSIZE}  # 栈大小，从 Kconfig 获取
    PRIORITY  ${CONFIG_EXAMPLES_HELLO_PRIORITY}   # 优先级，从 Kconfig 获取
  )
endif()
```

函数原型参考：`nuttx_add_application()`

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

### 2、移植第三方库

#### 基础移植方法 (推荐)

我们推荐为第三方库编写一个适配 openvela 的新 `CMakeLists.txt` 文件，这样可以精确控制其构建行为。

```Bash
openvela                                 openvela                                       
 └── external                             └── external
   └── Tripartite Library（外层）              └── Tripartite Library（外层）
       ├── Makefile           新增               ├── Makefile
       ├── Kconfig         =========>            ├── Kconfig 
       ├── Make.defs                             ├── Make.defs                 
       └── Tripartite Library（实际目录）          ├── CMakeLists.txt                  
                └── your changes                 └── Tripartite Library（实际目录） 
                                                          └── your changes 
```

`CMakeLists.txt` 结构模板 (以 `libtommath` 为例):

```CMake
# 示例来源 nuttx/apps/math/libtommath/CMakeLists.txt

# 1. 使能开关：检查 Kconfig 是否启用了此库
if(CONFIG_MATH_LIBTOMMATH)

  # #####################################################
  # Config and Fetch Tommath lib
  # 获取和配置三方库 类比原Makefile context的准备阶段
  # #####################################################
  
  # 2. 源码准备：(可选) 如果需要，可使用 FetchContent 自动下载和解压源码
  set(LIBTOMMATH_DIR ${CMAKE_CURRENT_LIST_DIR}/libtommath)
  
  if(NOT EXISTS ${LIBTOMMATH_DIR})
    set(CONFIG_LIBTOMMATH_URL https://github.com/libtom/libtommath/archive)
    # 使用cmake FetchContent模块获取外部资源
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
  # Sources 三方库的源文件添加
  # ########################################################
  # 3. 源文件定义：使用 file(GLOB ...) 或直接列出所有需要编译的源文件
  file(GLOB CSRCS ${LIBTOMMATH_DIR}/*.c)  # 此处使用file()

  if(CONFIG_LIBTOMMATH_DEMOS)
    list(APPEND CSRCS ${LIBTOMMATH_DIR}/demo/shared.c) # 也可以单独添加某个、某几个源文件
  endif()

  # #########################################################
  # Include Directory 三方库头文件路径
  # #########################################################
  # 4. 头文件路径定义：指定库的公共头文件目录
  set(INCDIR ${LIBTOMMATH_DIR})
  
  # ########################################################
  # Flags 三方库的编译选项配置
  # #######################################################
  # 5. 编译选项定义：(可选) 为该库设置特定的编译标志
  set(CFLAGS -Wno-format)

  # #########################################################
  # Library Configuration 三方库添加
  # #########################################################
 
  # 6. 注册库目标：使用 nuttx_add_library 将其定义为一个静态库
  nuttx_add_library(libtommath STATIC) 
  
  # 7. 配置库目标：将源文件、头文件路径和编译选项应用到目标
  # 将上面配置好的flags、sources、和incdir 配置给这个静态库目标
  target_compile_options(libtommath PRIVATE ${CFLAGS}) # 
  target_sources(libtommath PRIVATE ${CSRCS})
  target_include_directories(libtommath PRIVATE ${INCDIR})

  # ###########################################################
  # Applications Configuration 如果有应用也可以添加应用同上
  # ###########################################################
  # 8. (可选) 添加示例应用：如果库包含示例或测试程序，可在此处添加
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

其他移植方法请参见[高级开发实践：移植第三方库](./CMake_advanced_guide.md#2移植第三方库)。

### 3、适配自定义板级与芯片

为您的自定义硬件添加 CMake 支持，需要在相应的 `board` 和 `chip` 目录下创建 `CMakeLists.txt` 文件。

目录结构示例：

```Bash
# 目录位置 vendor/vendor_name
├── boards
│   ├── <chip_name>
│   │   └── <board_name>
│   │       ├── Kconfig       
│   │       ├── CMakeList.txt        <-- 新增                     
│   │       └── src
│   │           ├── Make.defs
│   │           └──  CMakeList.txt     <-- 新增
├── chips
│   └── chip_name
│       ├── Kconfig
│       ├── Make.defs
│       └──  CMakeList.txt      <-- 新增
```

`CMakeLists.txt` 内容示例：

1. `chips/<`**`chip_name`**`>/CMakeLists.txt`:

    ```Makefile
    # 添加custom chip的源文件
    set(SRCS chip_startup.S)
    # 注意添加的target为`arch`，最终将ar进libarch.a
    target_sources(arch PRIVATE ${SRCS})
    ```

2. `boards/<`**`chip_name`**`>/<`**`board_name`**`>/src/CMakeLists.txt`:

    ```Makefile
    # 添加custom board的源文件
    set(SRCS board_source.c)
    # 注意添加的target为`board`，最终将ar进libboard.a
    target_sources(board PRIVATE ${SRCS})
    ```

3. `boards/<`**`chip_name`**`>/<`**`board_name`**`>/CMakeLists.txt`:

    ```CMake
    # 添加custom/board/src目录至编译结构内
    add_subdirectory(src) 
    # 设置链接脚本位置
    set_property(
    GLOBAL
    PROPERTY
        LD_SCRIPT
        "${NUTTX_BOARD_ABS_DIR}/scripts/app.ld"
    )
    # 定义post_build目标，用于构建结束时自动处理产物
    add_custom_target(
        TARGET nuttx_post_build
        POST_BUILD
        COMMAND ${NUTTX_DIR}/../vendor/xxx/post_build.sh ${CMAKE_BINARY_DIR}
    )
    ```

## 六、FAQ

### 1、编写 CMakeLists.txt 时最重要的原则是什么

保持源码外构建 (Out-of-Tree) 的纯净性。必须确保所有构建操作都在构建目录（Binary Tree）内完成，严禁修改源码目录（Source Tree）。原 Makefile 中的软链接创建、文件修改等操作，都应迁移至在构建目录内执行。

### 2、CMake 代码有格式要求吗

**有**。openvela 使用 `cmakelang` 工具集中的 `cmake-format` 对 CMake 代码进行格式化。提交代码前，请务必运行格式化命令，否则会触发 CI 检查失败。

```Makefile
# 参考: https://cmake-format.readthedocs.io/en/latest/cmake-format.html
# 安装工具
pip3 install cmake-format
# 格式化文件 (原地修改)
cmake-format -o CMakeLists.txt CMakeLists.txt

usage: 
cmake-format [-h]
             [--dump-config {yaml,json,python} | -i | -o OUTFILE_PATH]
             [-c CONFIG_FILE]
             infilepath [infilepath ...]
```

### 3、如何处理模块间的依赖关系

使用 `nuttx_add_dependencies()` 函数。它会自动将被依赖模块的公共头文件路径添加到依赖它的模块中。

```CMake
# 场景：libtomcrypt 依赖 libtommath
# 在 libtommath 的 CMakeLists.txt 中：
nuttx_add_library(libtommath STATIC)
nuttx_export_header(TARGET libtommath INCLUDE_DIRECTORIES $${LIBTOMMATH_DIR})
# 在 libtomcrypt 的 CMakeLists.txt 中：
nuttx_add_library(libtomcrypt STATIC)
# libtomcrypt 将自动获得 libtommath 的头文件路径
nuttx_add_dependencies(TARGET libtomcrypt DEPENDS libtommath)
```

### 4、如何为特定文件设置独立的编译选项

使用 `set_source_files_properties()` 函数。

```CMake
# 使用CMake set_source_files_properties()
set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/source.c 
    PROPERTIES 
    COMPILE_FLAGS -O2)
```

### 5、如何链接一个已经编译好的静态库 (.a 文件)

使用 `nuttx_add_extra_library()` 函数。

```CMake
# 调用
nuttx_add_extra_library(${NUTTX_CHIP_ABS_DIR}/libadc.a)
```

### 6、如何自定义构建完成后的处理动作（如打包固件）

- 原 Makefile 构建提供了`POSTBUILD`宏定义，实现该宏可定制处理构建后的产物处理动作。
- CMake 也提供类似方法：

```CMake
# 在custom board内的CMakeList.txt内
# 实现一下定制目标`nuttx_post_build`
add_custom_target(
    TARGET nuttx_post_build
    POST_BUILD
    # 定制构建后任意动作
    COMMAND ${NUTTX_DIR}/${POSH_BIN}/post_build.sh ${CMAKE_BINARY_DIR}
)
```

## 参考文档

- 进一步阅读：[CMake 深度解析与维护手册](./CMake_advanced_guide.md)
- Makefile：[Makefile 编译系统](./Makefile_guide.md)