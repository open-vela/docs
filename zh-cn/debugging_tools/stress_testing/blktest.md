# blktest 块设备 I/O 测试指南

\[ [English](./../../../en/debugging_tools/stress_testing/blktest.md) | 简体中文 \]

本文档为 openvela 系统的开发者和测试工程师提供 `blktest` 测试套件的详细使用指南。该测试套件通过执行一系列 I/O 操作，旨在验证块设备和 Flash 存储设备驱动的稳定性、数据完整性和基本性能。

## 一、概述

`blktest` 是一个基于 CMocka 框架的驱动程序测试套件，用于对存储设备执行底层 I/O 功能验证。它通过直接与设备节点交互，模拟文件系统的读写行为，从而有效地评估目标驱动程序的健壮性。

该测试支持以下两种类型的设备：

- **块设备 (Block Devices)**：如 RAM 盘 (`/dev/ram*`)、SD 卡 (`/dev/sd*`) 等。
- **MTD** **设备 (Flash Devices)**：如 NAND/SPI-NOR Flash，通过 FTL (Flash Translation Layer) 和 BCH (Block-to-Character) 转换层进行访问。

`blktest` 主要执行三个核心测试用例，覆盖了从全盘压力扫描到特定 I/O 模式的多种场景。

**说明**：块设备以固定大小的 block/page 为单位进行地址化读写，常见 block 大小范围为 512 字节-32 768 字节。

## 二、系统配置

在执行测试前，您必须在 `defconfig` 文件中启用以下 Kconfig 选项，以确保 `blktest` 套件及其依赖项被正确编译和集成到系统中。

```CMake
# 启用 BCH 驱动，用于访问 MTD 设备
CONFIG_BCH=y

# 启用驱动测试集合，其中包含 blktest
CONFIG_TESTING_DRIVER_TEST=y

# 启用 CMocka 测试框架，为 blktest 提供运行环境
CONFIG_TESTING_CMOCKA=y
```

**配置说明:**

- `CONFIG_BCH=y`: 启用块到字符 (Block-to-Character) 转换驱动。当测试 MTD 设备时，该层是必需的。
- `CONFIG_TESTING_DRIVER_TEST=y`: 启用基础驱动测试集。
- `CONFIG_TESTING_CMOCKA=y`: 启用 CMocka 单元测试框架，`blktest` 测试用例基于此框架构建。

## 三、执行测试

### 1、命令语法

`blktest` 测试套件通过 `cmocka_driver_block` 命令启动。

```Bash
cmocka_driver_block -m <device_path>
```

- device_path：
    - 说明：指定要测试的目标设备节点路径。如 `/dev/ram10`（块设备）或 `/dev/mtdblock0`（MTD 设备）。

### 2、执行示例

以下命令演示了如何对位于 `/dev/ram10` 的 RAM 盘设备执行测试：

```Bash
cmocka_driver_block -m /dev/ram10
```

**注意**：测试过程会遍历设备的大部分区域进行读写，根据设备类型和大小，测试可能会持续较长时间，请耐心等待其执行完成。

## 四、测试用例详解

`cmocka_driver_block` 命令会依次执行以下三个独立的测试用例：

| **测试用例名称**          | **测试目的与行为**                                                                                                                                                                       |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `blktest_stress`          | **全盘压力与数据完整性测试**。 遍历设备的每一个块 (block)，向其中写入随机数据，然后立即回读并进行 CRC32 校验，以确保数据写入和读取的准确性。对于 Flash 设备，此操作会经过 FTL/BCH 堆栈。 |
| `blktest_single_write`    | **单块写入功能测试**。 模拟文件系统操作，向设备写入单个块/页 (block/page)，验证驱动程序处理基本写入请求的能力。                                                                          |
| `blktest_cachesize_write` | **缓存写入功能测试**。 模拟文件系统操作，一次性写入与设备缓存大小相等的块/页数量，用于检验驱动对缓冲 I/O 或批量写入操作的处理能力。                                                      |

## 五、预期输出

测试成功后，您将在控制台看到类似以下的输出。每一行 `[ OK ]` 表示一个测试用例成功通过。

```Bash
ap> cmocka_driver_block -m /dev/ram10
[  INFO] [ap] [==========] tests: Running 1 test(s).
[  INFO] [ap] [ RUN      ] blktest_stress
[  INFO] [ap] [       OK ] blktest_stress
[  INFO] [ap] [ RUN      ] blktest_single_write
[  INFO] [ap] [       OK ] blktest_single_write
[  INFO] [ap] [ RUN      ] blktest_cachesize_write
[  INFO] [ap] [       OK ] blktest_cachesize_write
[  INFO] [ap] [==========] tests: 1 test(s) run.
[  INFO] [ap] [  PASSED  ] 1 test(s).
ap> 
```

## 六、参考资料

`blktest` 是开源项目 Apache NuttX 的一部分，您可以通过以下链接获取更多信息：

- **[Apache NuttX 官方网站](https://nuttx.apache.org/)**：了解 NuttX RTOS 的最新动态、功能和社区资源。
- **[CMocka 官方网站](https://cmocka.org/)**：了解 `blktest` 所使用的单元测试框架。