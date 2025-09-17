# blktest Block Device I/O Test Guide

\[ English | [简体中文](./../../../zh-cn/debugging_tools/stress_testing/blktest.md) \]

This guide provides developers and test engineers with instructions for using the `blktest` test suite on the openvela system. The `blktest` suite validates the stability, data integrity, and performance of block and Flash storage device drivers by executing a series of I/O operations.

## I. Overview

`blktest` is a driver test suite built on the CMocka framework that performs low-level I/O functional verification on storage devices. The suite interacts directly with device nodes to simulate file system read and write behavior, which allows you to effectively evaluate the robustness of a target driver.

The test supports the following device types:

- **Block Devices**: Such as RAM disks (`/dev/ram*`) and SD cards (`/dev/sd*`).
- **MTD (Flash) Devices**: Such as NAND or SPI-NOR Flash, which are accessed through a Flash Translation Layer (FTL) and a Block-to-Character (BCH) conversion layer.

`blktest` executes three core test cases that cover multiple scenarios, from full-disk stress tests to specific I/O patterns.

> **Note**: Block devices perform read and write operations in fixed-size units called blocks or pages. Common block sizes range from 512 bytes to 32,768 bytes.

## II. System Configuration

Before you run the test, you must enable the following Kconfig options in your `defconfig` file. This ensures that the system correctly compiles and integrates the `blktest` suite and its dependencies.

```ini
# Enables the BCH driver, required for accessing MTD devices
CONFIG_BCH=y

# Enables the driver test collection, which includes blktest
CONFIG_TESTING_DRIVER_TEST=y

# Enables the CMocka test framework, which provides the runtime for blktest
CONFIG_TESTING_CMOCKA=y
```

**Configuration Details:**

- `CONFIG_BCH=y`: Enables the Block-to-Character (BCH) translation driver. This layer is required when testing MTD devices.
- `CONFIG_TESTING_DRIVER_TEST=y`: Enables the base driver test suite.
- `CONFIG_TESTING_CMOCKA=y`: Enables the CMocka unit testing framework, on which the `blktest` test cases are built.

## III. Running the Test

### 1. Command Syntax

Run the `blktest` suite using the `cmocka_driver_block` command.

```bash
cmocka_driver_block -m <device_path>
```

- **`device_path`**
    - The path to the target device node. For example, use `/dev/ram10` for a block device or `/dev/mtdblock0` for an MTD device.

### 2. Example

The following command runs the test on a RAM disk device located at `/dev/ram10`:

```bash
cmocka_driver_block -m /dev/ram10
```

> **Note**: The test traverses large sections of the device for read and write operations. The duration of the test depends on the device type and size, so please allow sufficient time for it to complete.

## IV. Test Case Details

The `cmocka_driver_block` command executes the following three test cases in sequence:

| Test Case Name            | Purpose and Behavior                                                                                                                                                                                                                                                                                 |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `blktest_stress`          | **Full-Disk Stress and Data Integrity Test**. <br>This test traverses every block on the device, writes random data to each block, and then immediately reads it back. It performs a CRC32 checksum to verify data integrity. For Flash devices, this operation goes through the FTL and BCH layers. |
| `blktest_single_write`    | **Single-Block Write Test**. <br>This test simulates a file system operation by writing a single block (or page) to the device. It verifies the driver's ability to process a basic write request.                                                                                                   |
| `blktest_cachesize_write` | **Cache-Sized Write Test**. <br>This test simulates a file system operation by writing a number of blocks equal to the device's cache size in a single operation. It validates the driver's ability to handle buffered I/O and bulk write operations.                                                |

## V. Expected Output

A successful test run produces output similar to the following example. Each line containing `[ OK ]` indicates that a test case passed.

```bash
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

## VI. References

`blktest` is part of the open-source Apache NuttX project. For more information, see the following resources:

- **[Apache NuttX Official Website](https://nuttx.apache.org/)**: Find the latest updates, features, and community resources for the NuttX RTOS.
- **[CMocka Official Website](https://cmocka.org/)**: The official website for the unit testing framework used by `blktest`.