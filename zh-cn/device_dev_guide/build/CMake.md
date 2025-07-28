# CMake构建系统迁移与开发指南

## 前言

本文档旨在完整阐述 openvela 项目从 GNU Make 迁移至 CMake 构建系统的背景、优势与具体实践，为开发者提供一套完整的迁移、使用与开发指引。

如果您对 CMake 尚不熟悉，建议先行阅览以下官方资源，以便更好地理解本文内容：

- **CMake 官方教程 (CMake Tutorial):** https://cmake.org/cmake/help/latest/guide/tutorial/index.html
- **CMake 官方文档 (CMake Documentation):** https://cmake.org/documentation/
- **精讲系列：Modern CMake (An Introduction to Modern CMake):** https://cliutils.gitlab.io/modern-cmake/

## 一、背景：为何迁移至 CMake

为应对日益增长的项目复杂度和开发者对效率的需求，openvela 决定将其构建系统从传统的 GNU Make 迁移至现代化的 CMake。此次升级旨在解决旧有系统在编译效率、可靠性及可扩展性方面面临的一系列挑战。

### 1、当前构建系统的挑战

根据统计，当前基于 GNU Make 的构建系统存在以下核心痛点：

- **问题频发**：2023 年，在报告的 **1043** 个问题中，与编译系统直接相关的问题高达 **92** 个，占比 **8.8%**。
- **效率低下**：CI 全量编译耗时已超过一小时，严重影响开发与持续集成效率。
- **体验不佳**：开发者普遍反馈的问题包括：
  - **编译速度慢**，且无法支持多配置并行编译。
  - **增量编译不可靠**，导致需要频繁 `distclean`。
  - **构建产物清理不彻底**，易引发非预期构建错误。
  - **缺乏模块化编译能力**，无法针对单个模块进行快速验证。

这些问题在大型嵌入式项目中普遍存在。业界主流 RTOS，如 NuttX、Zephyr、FreeRTOS 等，均已成功迁移至 CMake 以解决类似问题。

### 2、技术选型：为何选择 CMake

我们对主流构建系统进行了调研和比较，最终选择 CMake 的核心原因如下：

| 构建系统 | 速度       | 自动依赖 | 跨平台支持 | 应用广泛程度 | Ninja生成器 | 社区规模 | 迁移成本   |
| :------- | :--------- | :------- | :--------- | :----------- | :---------- | :------- | :--------- |
| CMake    | 取决于后端 | 支持     | 支持       | 最高         | 支持        | 庞大     | 有社区基础 |
| GN       | 快         | 支持     | 支持       | 中           | 支持        | 较小     | 从零开始   |
| SCons    | 较慢       | 支持     | 支持       | 中           | 不支持      | 较小     | 从零开始   |

> 数据参考: [Stackoverflow 2023 survey](https://survey.stackoverflow.co/2023/#most-popular-technologies-tools-tech)

CMake 凭借其成熟的生态、强大的跨平台能力、精确的依赖管理以及对 Ninja 等高性能后端的支持，成为本次升级的最佳选择。

## 二、核心价值：迁移至 CMake 的优势

迁移至 CMake 为 openvela 开发者带来以下显著价值：

- **显著提升编译速度**：实测表明，即使同为 Makefile 后端，CMake 的编译速度也有一倍以上的提升。若配合 Ninja 后端，性能将进一步优化。

  - ```Bash
    ## 以下对比可以看出，CMake相比当前构建系统
    ## 同为Makefile生成器时，构建提速在一倍以上。
    ## 切换Ninja生成器时仍然有继续提升的空间。
    
    # lm3s6965-ek/qemu-flat 构建速度对比
             Original       CMake     CMake(Ninja)
     real    0m9.982s      0m4.739s      0m4.475s
    
    # sabre-6quad/smp 构建速度对比
             Original       CMake     CMake(Ninja)
     real    0m10.921s     0m3.936s      0m3.616s
    ```

- **支持源码外构建 (Out-of-Tree)**：将构建产物与源码完全分离，确保源码树的整洁。同时，此特性允许在同一份源码上并行构建多个不同的配置，极大提升多目标验证效率。

- **精确的依赖关系管理**：CMake 自动分析目标间的依赖关系，确保增量编译的正确性和可靠性，彻底解决了旧系统中 `mkdep` 和 `.depend` 机制的缺陷。

- **支持模块独立编译**：开发者可以独立构建和验证任一特定模块，便于快速调试、库文件发布及 SDK 的集成。

- **卓越的跨平台支持**：CMake 原生支持在 Windows、Linux 和 macOS 等多种主机环境下进行开发，并通过生成器无缝对接 GNU Make、Ninja、Xcode 等多种构建工具和 IDE。

- **改善开发与调试体验**：CMake 语法结构清晰，更易于维护和扩展。它与 VSCode、CLion 等主流 IDE 深度集成，为开发者提供了图形化的构建配置与调试功能。

## 三、快速上手：使用 CMake 构建

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

**常用构建选项：**

| **选项**            | **别名** | **描述**                 | **示例**                            |
| :------------------ | :------- | :----------------------- | :---------------------------------- |
| `--build <dir>`     |          | 指定构建目录并执行编译。 | `cmake --build build`               |
| `--target <target>` | `-t`     | 仅构建指定的目标。       | `cmake --build build -t menuconfig` |
| `--parallel <jobs>` | `-j`     | 指定并行编译的任务数。   | `cmake --build build --parallel 8`  |
| `--verbose`         | `-v`     | 输出详细的构建日志。     | `cmake --build build -v`            |
| `--clean-first`     |          | 在构建前先执行清理操作。 | `cmake --build build --clean-first` |

## 四、CMake 构建系统架构解析

本章节深入剖析 openvela CMake 构建系统的内部工作流程。

### 1、主要构建流程

openvela 的 CMake 构建过程遵循 NuttX 的标准框架，其入口文件为 `nuttx/CMakeLists.txt`。整个流程可概括为以下几个关键阶段：

1. 基础配置：CMake基础配置、工作目录解析NuttXDir & AppDir、解析board config & directory 、基本sanity检查、环境检查；
2. 解析defconfig ===> 识别应用目录apps/ ===> symbolic link board/ chip/目录 ===> 应用目录Kconfig生成；
3. 使用olddefconfig和生成好的Kconfig树展开defconfig生成.config并将所有配置宏导入CMake环境；
4. 导入所有cmake module并且根据CONFIG_ARCH加载CMake TOOLCHAIN FILE完成工具链的配置；
5. mkconfig.cmake、gen_header.cmake执行生成构建context目标，确保在编译开始前环境被正确的配置；
6. 依次添加各模块目录（arch、driver、mm、sched、apps...）生成各个.a静态库，最终链接全部的${nuttx_libs};
7. 产物处理、执行POST_BUILD宏处理。

![alt text](image.png)

该过程简单直观的按时序列出了大致的构建步骤，其实在真正执行CMake build时，中间编译的规则在configure阶段已经由CMake生成组织完成，在--build才进行真正编译。以使用Makefile规则为例。其生成，编译规则在` nuttx/build/CMakeFiles`中，可以单独查看调试。

### 2、构建依赖关系

所有模块最终被组织成不同类别的库集合，并链接成最终产物。其依赖关系如下图所示：

![alt text](image-1.png)

## 五. 开发实践指南

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

#### 2.1 基础移植方法 (推荐)

我们推荐为第三方库编写一个适配 openvela 的新 `CMakeLists.txt` 文件，这样可以精确控制其构建行为。

```Bash
vela                                      vela                                       
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
  # 8. 添加示例应用：(可选) 如果库包含示例或测试程序，可在此处添加
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

#### 2.2 移植已支持 CMake 的库：方法选择

如果一个第三方库本身已提供 `CMakeLists.txt`，您可以评估是否复用它。

**决策原则**：在选择移植方式时，请遵循以下原则。当存在下列情况时，不应复用三方库的 `CMakeLists.txt`，而应为其编写新的适配脚本：

1. 三方库不支持交叉编译或对主机平台有强依赖。
2. 三方库需要作为 openvela 的内置应用进行注册。
3. 三方库的 `CMakeLists.txt` 存在无法在外部控制的编译选项。
4. 三方库的构建脚本定义了过多冗余或与系统冲突的目标。

如果三方库是一个纯粹的静态库且无上述问题，可考虑复用其构建脚本。

- **方式一（推荐）：编写新** `CMakeLists.txt`

  - **描述**：如 5.2.1 节所示，此方法提供了最大的灵活性和控制力，完全重写构建逻辑。
  - **特点**：简易、灵活、移植难度低，但可能代码量较大。

- **方式二：通过** `add_subdirectory` **复用**

  - **描述**：此方法通过 `add_subdirectory()` 将第三方库作为子项目引入，并使用 `nuttx_add_external_library` 将其库目标集成到 openvela 中。

  - **示例** (`libpng`)：

    - ```Makefile
      # 在外部设置其 CACHE 变量来控制其构建行为
      set(PNG_SHARED OFF CACHE BOOL "Disable libpng shared library" FORCE)
      set(PNG_EXECUTABLES OFF CACHE BOOL "Disable libpng executable" FORCE)
      set(PNG_TESTS OFF CACHE BOOL "Disable libpng tests program" FORCE)
      # 将三方库作为子目录添加
      add_subdirectory($${CMAKE_CURRENT_SOURCE_DIR}/libpng
                       $${CMAKE_CURRENT_BINARY_DIR}/libpng EXCLUDE_FROM_ALL)
      # 将三方库定义的目标集成到 openvela 构建环境中
      nuttx_add_external_library(png_static)
      ```

  - 特点：可复用外部脚本，减少移植代码量。但可能引入冗余或冲突的目标，需要仔细评估其 `CMakeLists.txt`。

- **方式三：通过** **`ExternalProject_Add`** **独立构建**

  - **描述**：此方法会启动一个完全独立的子构建过程来编译第三方库，并将其构建产物作为 `IMPORTED` 库引入。

  - **示例** (`libpng`)：

    - ```Makefile
      # 手动将 openvela 的交叉编译工具链信息传递给子构建过程
      set(FLAGS_ARGS "$$<JOIN:$$<TARGET_PROPERTY:nuttx,COMPILE_OPTIONS>, >")
      set(EXTERN_C_FLAGS "$${CMAKE_C_FLAGS} $${FLAGS_ARGS}")
      ExternalProject_Add(
          libpng_external
          SOURCE_DIR $${CMAKE_CURRENT_LIST_DIR}/libpng/
          BINARY_DIR $${CMAKE_BINARY_DIR}/external/libpng_external
          CMAKE_ARGS
              -DCMAKE_C_COMPILER=$${CMAKE_C_COMPILER}
              -DCMAKE_C_FLAGS=$${EXTERN_C_FLAGS}
              -DPNG_SHARED=OFF
              -DPNG_EXECUTABLES=OFF
              -DPNG_TEST=OFF
          TEST_COMMAND ""
          INSTALL_COMMAND ""
      )
      # 将子构建的产物作为 IMPORTED 库引入主构建过程
      add_library(libpng STATIC IMPORTED GLOBAL)
      set_target_properties(libpng PROPERTIES
          IMPORTED_LOCATION $${CMAKE_BINARY_DIR}/external/libpng_external/libpng.a
      )
      add_dependencies(libpng libpng_external)
      set_property(GLOBAL APPEND PROPERTY NUTTX_SYSTEM_LIBRARIES libpng)
      ```

  - 特点：隔离性好，但过程复杂，需要手动处理工具链传递和产物导入。

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

   1. ```Makefile
      # 添加custom chip的源文件
      set(SRCS chip_startup.S)
      # 注意添加的target为`arch`，最终将ar进libarch.a
      target_sources(arch PRIVATE ${SRCS})
      ```

2. `boards/<`**`chip_name`**`>/<`**`board_name`**`>/src/CMakeLists.txt`:

   1. ```Makefile
      # 添加custom board的源文件
      set(SRCS board_source.c)
      # 注意添加的target为`board`，最终将ar进libboard.a
      target_sources(board PRIVATE ${SRCS})
      ```

3. `boards/your_chip/your_board/CMakeLists.txt`:

   1. ```CMake
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

## 四、注意事项与常见问题 (FAQ)

### 1、在过渡期，如何维护两个构建系统？

openvela 同时支持 Makefile 和 CMake。当您修改了任何与编译相关的文件（如增删源文件、修改编译选项）时，必须同时更新 `Makefile` 和同级目录下的 `CMakeLists.txt`，以确保两个系统行为一致。

### 2、编写 CMakeLists.txt 时最重要的原则是什么？

保持源码外构建 (Out-of-Tree) 的纯净性。必须确保所有构建操作都在构建目录（Binary Tree）内完成，严禁修改源码目录（Source Tree）。原 Makefile 中的软链接创建、文件修改等操作，都应迁移至在构建目录内执行。

### 3、CMake 代码有格式要求吗？

有。openvela 使用 `cmakelang` 工具集中的 `cmake-format` 对 CMake 代码进行格式化。提交代码前，请务必运行格式化命令，否则会触发 CI 检查失败。

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

### 4、如何让一个模块的头文件对其他所有模块可见？

- CMake的静态目标`target_include_directories()`只提供私有头文件路径。公有的头文件需要通过nuttx的增强函数nuttx_export_header()实现。（注意 CMake中的PUBLIC关键子在此场景并不能自动传递头文件路径，因为apps/下的目标是同级关系，并未手动维护依赖关系。）

  - ```CMake
    # nuttx/cmake/nuttx_export_header.cmake
    
    # Usage:
    #   nuttx_export_header(TARGET <string> INCLUDE_DIRECTORIES <list>)
    
    # 以上文三方库 libtommath为例 ，In CMakeLists.txt of libtommath
    nuttx_export_header(TARGET libtommath INCLUDE_DIRECTORIES ${LIBTOMMATH_DIR})
    ```

  - 以上 NUTTX_INCLUDE_DIRECTORIES 和 nuttx_export_header 如何选择

    取决于这个应用模块是否为一个common的应用 如果是特定库之间的依赖更推荐手动指定依赖关系。参考下一小节

- 原Makefile构建中，应用的公有头文件路径可以配置在`Make.defs`中，私有头文件路径加入`Makefile`。

全局的头文件路径在CMake中使用一个global的属性来保存，在定义目标时自动添加到目标属性内。

```CMake
  # 为nuttx添加全局头文件属性
  set_property(
    TARGET nuttx
    APPEND
    PROPERTY NUTTX_INCLUDE_DIRECTORIES ${INCDIR})
```

### 5、如何处理模块间的依赖关系？

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

### 6、如何为特定文件设置独立的编译选项？

使用 `set_source_files_properties()` 函数。

```CMake
# 使用CMake set_source_files_properties()
set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/source.c 
    PROPERTIES 
    COMPILE_FLAGS -O2)
```

### 7、如何链接一个已经编译好的静态库 (.a 文件)？

使用 `nuttx_add_extra_library()` 函数。

```CMake
# 调用
nuttx_add_extra_library(${NUTTX_CHIP_ABS_DIR}/libadc.a)
```

### 8、如何移除或覆盖全局编译选项？

- 原Makefile提供多种优化编译配置如: `ARCHCPUFLAGS` 、`ARCHCFLAGS`、`ARCHOPTIMIZATION`可以灵活在板子的Make.defs中覆盖、补充Toolchain.defs的编译配置。
- 切换CMake后编译选项统一在对应Arch的Toolchain.cmake添加，灵活性降低了。如果有编译配置的冲突Vela实现了一个CMake add_complie_options()的逆操作可供调整：

```CMake
# 以某custom riscv arch的定制工具链为例：

# -march 和 -mabi 与-mcpu冲突

# 在Makefile中可以在board/script/Make.defs重写ARCHCPUFLAGS = -mcpu=xxx 
# 将Toolchain.defs中通用设置的-march与-mabi覆盖

# 而CMake不提供add_complie_options()的反向操作，此处可以使用增强函数nuttx_remove_compile_options(ARGNS)

# Example:
nuttx_remove_compile_options(-march -mabi)
#
#   befor: CFLAGS = -O2 -g -march=rv32if -mabi=ilp32f -mcpu=e907fp
#   after: CFLAGS = -O2 -g -mcpu=e907fp
```

### 9、如何自定义构建完成后的处理动作（如打包固件）？

- 原Makefile构建提供了`POSTBUILD`宏定义，实现该宏可定制处理构建后的产物处理动作。
- CMake也提供类似方法：

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

## 附录

### 1、核心 CMake 模块

NuttX的CMake module定义在 `nuttx/cmake/`下，他是CMake构建系统的扩展模块，提供了额外的功能和变量，用于辅助管理和构建整个项目。和原Makefile类比的话，可以简单理解为将NuttX的host tools和Makefile中的Config.mk的部分工具和工具宏在CMake中做了模块化。

```Bash
# nuttx下cmake module目录
cmake
├── menuconfig.cmake                     # 定义config target base on kconfig_frontend
├── nuttx_add_application.cmake          # 添加app应用的包装函数
├── nuttx_add_dependencies.cmake         # 增强add_dependencies，可以同时添加依赖头文件目录
├── nuttx_add_library.cmake              # 对cmake add_library的增强包装函数
├── nuttx_add_module.cmake               # 生成独立模块目标包装函数
├── nuttx_add_romfs.cmake                # 添加生成romfs包装函数
├── nuttx_add_subdirectory.cmake         # 对cmake add_subdirectroy的增强
├── nuttx_add_symtab.cmake               # 生成未定义符号的符号表
├── nuttx_create_symlink.cmake           # 软链生成方法
├── nuttx_export_header.cmake            # 全局include目录导出
├── nuttx_generate_headers.cmake         # nuttx_context target定义
├── nuttx_generate_outputs.cmake         # objcopy命令目标定义
├── nuttx_kconfig.cmake                  # kconfig解析与生成
├── nuttx_mkconfig.cmake                 # 转换config.h
├── nuttx_mkversion.cmake                # 转换version.h
├── nuttx_parse_function_args.cmake      # 对cmake_parse_argument module的增强
├── nuttx_redefine_symbols.cmake         # sim重命名冲突符号
├── nuttx_remove_compile_options.cmake   # 对add_complie_options的逆实现增强
└── symtab.c.in                          # 配合add_symtab generate code模版
```

## 参考文档

- Makefile：[编译系统](https://xiaomi.f.mioffice.cn/wiki/wikk46XY5oMyszR6q1BfJwRjuDh)