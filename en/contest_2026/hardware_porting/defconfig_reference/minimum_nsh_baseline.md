# Minimum Bootable NSH System defconfig Reference

\[ English | [简体中文](../../../../zh-cn/contest_2026/hardware_porting/defconfig_reference/minimum_nsh_baseline.md) \]

This document targets contestants of the Hardware Porting Track. The goal is to help contestants **boot to the NSH command-line prompt on their development board first**. The recommended workflow is: start from the minimum set provided in this document, verify that the serial console and NSH work correctly, and then incrementally enable subsystems such as filesystem, networking, and sensors.

## 1. Overview

### 1.1 Document goal

When a contestant receives a development board not yet supported by openvela, the most critical first step is to bring the system up to the NSH command-line prompt. This document provides a **bare-minimum** reference defconfig that contains only the configuration items required to boot NSH, helping contestants quickly identify:

- Which CONFIGs **must be modified** (strongly tied to target hardware);
- Which CONFIGs **can be reused as-is** (hardware-independent runtime support);
- After L0 brings up, in which order to **incrementally enable** subsystems.

### 1.2 Recommended workflow

```
Step 0: Hardware ready
        - Target chip is supported under nuttx/arch/<arch>/src/<chip>/
        - Board directory exists at boards/<arch>/<chip>/<board>/
        - Serial TX/RX pins are connected to the host
        ↓
Step 1: Apply this minimum set → build → flash → see NSH prompt on console
        ↓
Step 2: Incrementally enable subsystems based on hardware capability
        - Filesystem (FAT / LittleFS)
        - Networking stack (Ethernet / Wi-Fi)
        - Graphics (LCD / framebuffer / LVGL)
        - Sensors (uORB / I2C / SPI sensors)
        ↓
Step 3: Trim for release once porting stabilizes
        - Disable DEBUG_*, ALLSYMS, and similar debug items
        - Adjust stack sizes based on measured needs
```

## 2. Minimum NSH required configuration

The configuration items in this section are derived from `nuttx/boards/arm/stm32/nucleo-f303re/configs/nsh/defconfig` (35 lines), and also draw on Mateusz Szafoni's [NuttX small systems blog series](https://www.railab.me/tags/small-systems/) for practical minimization techniques.

### 2.1 Architecture and board identity (Must be replaced for the target hardware)

```
CONFIG_ARCH="arm"
CONFIG_ARCH_CHIP="stm32"
CONFIG_ARCH_CHIP_STM32=y
CONFIG_ARCH_CHIP_STM32F303RE=y
CONFIG_ARCH_BOARD="nucleo-f303re"
CONFIG_ARCH_BOARD_NUCLEO_F303RE=y
```

#### Replacement guidelines

| Item | Replacement guideline |
| ---- | ---- |
| `CONFIG_ARCH=` | Target CPU architecture, e.g. `"arm"`, `"arm64"`, `"risc-v"`, `"xtensa"` |
| `CONFIG_ARCH_CHIP=` and `CONFIG_ARCH_CHIP_<FAMILY>=y` | Target SoC family, must match `nuttx/arch/<arch>/src/<chip>/` (e.g. `stm32`, `stm32h7`, `nrf52`, `esp32s3`) |
| `CONFIG_ARCH_CHIP_<DEVICE>=y` | Specific device, e.g. `STM32F407VG`, `NRF52840`, `ESP32S3` |
| `CONFIG_ARCH_BOARD=` and `CONFIG_ARCH_BOARD_<NAME>=y` | Board directory name, must match `nuttx/boards/<arch>/<chip>/<board>/` |

### 2.2 Memory layout (Must be filled in per target hardware)

```
CONFIG_RAM_START=0x20000000
CONFIG_RAM_SIZE=65536
CONFIG_MM_REGIONS=2
CONFIG_BOARD_LOOPSPERMSEC=6522
```

#### Item descriptions

- `CONFIG_RAM_START`: starting physical address of the main SRAM, refer to the target chip's datasheet (most ARM Cortex-M chips use `0x20000000`).
- `CONFIG_RAM_SIZE`: main SRAM size in bytes.
- `CONFIG_MM_REGIONS`: number of memory regions managed by the heap allocator. Adjust accordingly when the chip has multiple discontiguous SRAM blocks (e.g. STM32F4's CCM, STM32H7's AXI/AHB SRAM).
- `CONFIG_BOARD_LOOPSPERMSEC`: busy-wait delay calibration value, related to CPU frequency. May be filled with an estimated value initially and calibrated later via `up_mdelay()`.

### 2.3 Serial console (Must be replaced per target hardware)

```
CONFIG_STM32_USART2=y
CONFIG_USART2_SERIAL_CONSOLE=y
CONFIG_STM32_JTAG_SW_ENABLE=y
```

#### Replacement guidelines

| Item | Replacement guideline |
| ---- | ---- |
| `CONFIG_<CHIP>_USART<N>=y` | Enable the target chip's UART peripheral. STM32 uses `STM32_USARTx`, nRF52 uses `NRF52_UART0`, ESP32 uses `ESP32_UART0` |
| `CONFIG_USART<N>_SERIAL_CONSOLE=y` | Designate that UART as the system console |
| `CONFIG_<CHIP>_JTAG_SW_ENABLE=y` | Optional per chip; preserves the SWD debug port |

Refer to `board.h` under `nuttx/boards/<arch>/<chip>/<board>/include/` for pin definitions and confirm that the serial port maps to TX/RX pins matching your hardware design.

### 2.4 NSH Shell entry point (Reuse as-is)

```
CONFIG_SYSTEM_NSH=y
CONFIG_INIT_ENTRYPOINT="nsh_main"
```

#### Item descriptions

- `CONFIG_SYSTEM_NSH=y`: builds NSH as a system application.
- `CONFIG_INIT_ENTRYPOINT="nsh_main"`: makes NSH the first user-mode task after system boot. Once the serial console is connected, the command-line prompt appears.

### 2.5 Scheduling and runtime support (Reuse as-is)

```
CONFIG_RR_INTERVAL=200
CONFIG_SCHED_WAITPID=y
CONFIG_PREALLOC_TIMERS=4
CONFIG_IDLETHREAD_STACKSIZE=2048
CONFIG_TASK_NAME_SIZE=0
CONFIG_START_DAY=27
CONFIG_START_YEAR=2013
```

#### Item descriptions

- `CONFIG_RR_INTERVAL=200`: round-robin scheduling time slice of 200 ms.
- `CONFIG_SCHED_WAITPID=y`: enables the `waitpid()` syscall, which NSH relies on when running built-in commands.
- `CONFIG_PREALLOC_TIMERS=4`: pre-allocates 4 POSIX timers, sufficient for basic needs.
- `CONFIG_IDLETHREAD_STACKSIZE=2048`: idle-thread stack size. 2 KB is suitable for most Cortex-M boards. Reduce to 1024 if RAM is tight.
- `CONFIG_TASK_NAME_SIZE=0`: disables task-name strings to save RAM. Set to 16~32 if the `ps` command is needed to display task names.
- `CONFIG_START_DAY` and `CONFIG_START_YEAR`: initial date when the system boots; can be set to any reasonable values.

### 2.6 Debug and diagnostics (Strongly recommended to retain)

```
CONFIG_DEBUG_SYMBOLS=y
CONFIG_ARCH_STACKDUMP=y
CONFIG_INTELHEX_BINARY=y
CONFIG_RAW_BINARY=y
```

#### Item descriptions

- `CONFIG_DEBUG_SYMBOLS=y`: retains debug symbols for GDB single-stepping and backtrace analysis.
- `CONFIG_ARCH_STACKDUMP=y`: prints stack contents on hardfault — an essential aid during the porting phase.
- `CONFIG_INTELHEX_BINARY=y` and `CONFIG_RAW_BINARY=y`: produce both `.hex` and `.bin` artifacts after the build.

### 2.7 CPU feature trimming (Adjust as needed)

```
# CONFIG_ARCH_FPU is not set
```

#### Description

`CONFIG_ARCH_FPU` controls whether the hardware floating-point unit is enabled. Cortex-M4F, M7 and similar cores with FPU should set `CONFIG_ARCH_FPU=y` if floating-point operations are required. Cortex-M0/M3 cores have no FPU and should leave it disabled.

### 2.8 Board-level helpers (Optional)

```
CONFIG_ARCH_BUTTONS=y
```

#### Description

`CONFIG_ARCH_BUTTONS=y`: enables the button driver framework when the board has a USER button. Omit if the target board has no buttons.

## 3. Reusable defconfig fragment

The following 13 items are hardware-independent and may be used as-is on any ARM Cortex-M board:

```
CONFIG_RR_INTERVAL=200
CONFIG_SCHED_WAITPID=y
CONFIG_PREALLOC_TIMERS=4
CONFIG_IDLETHREAD_STACKSIZE=2048
CONFIG_TASK_NAME_SIZE=0
CONFIG_START_DAY=27
CONFIG_START_YEAR=2013
CONFIG_SYSTEM_NSH=y
CONFIG_INIT_ENTRYPOINT="nsh_main"
CONFIG_DEBUG_SYMBOLS=y
CONFIG_ARCH_STACKDUMP=y
CONFIG_INTELHEX_BINARY=y
CONFIG_RAW_BINARY=y
```

Contestants only need to fill in the hardware-specific items marked "Must be replaced per target hardware" in Section 2 (architecture identity, memory layout, serial console) to form a complete L0 defconfig.

## 4. Reference implementations

### 4.1 Nucleo-F303RE (recommended reference board)

Full defconfig path:

```
nuttx/boards/arm/stm32/nucleo-f303re/configs/nsh/defconfig
```

This board is built around the STM32F303RE (Cortex-M4F @ 72 MHz, 512 KB Flash, 64 KB SRAM) and integrates the ST-Link/V2-1 debugger with a USB virtual serial port. With a single USB cable, contestants can perform both flashing and serial communication, making it the most convenient hardware reference for verifying the minimum-NSH workflow.

### 4.2 Other minimal NSH defconfigs for reference

| Reference board | Path | Lines | Use case |
| ---- | ---- | ---- | ---- |
| Nucleo-F303RE | `nuttx/boards/arm/stm32/nucleo-f303re/configs/nsh/defconfig` | 35 | Mainstream ARM Cortex-M4F reference |
| nRF52840-DK | `nuttx/boards/arm/nrf52/nrf52840-dk/configs/nsh/defconfig` | 41 | Reference for the Nordic nRF52 family |
| STM32F411-Minimum | `nuttx/boards/arm/stm32/stm32f411-minimum/configs/nsh/defconfig` | 46 | STM32F4 with constrained resources |
| STM32F4Discovery | `nuttx/boards/arm/stm32/stm32f4discovery/configs/nsh/defconfig` | 50 | Classic STM32F4 evaluation board (includes some extras) |

## 5. Incrementally enabling subsystems

Once L0 boots successfully (the NSH prompt is visible on the serial console), subsystems can be enabled progressively per the target board's capability. Common CONFIG entry points for each subsystem are:

| Subsystem | Primary CONFIG entry points |
| ---- | ---- |
| Filesystem (FAT, LittleFS, PROCFS) | `CONFIG_FS_FAT`, `CONFIG_FS_LITTLEFS`, `CONFIG_FS_PROCFS` |
| Networking stack (TCP/IP, Wi-Fi) | `CONFIG_NET`, `CONFIG_NET_TCP`, `CONFIG_NET_UDP` |
| Graphics and display (fb, LCD, LVGL) | `CONFIG_VIDEO_FB`, `CONFIG_GRAPHICS_LVGL` |
| Sensors and uORB | `CONFIG_SENSORS`, `CONFIG_UORB` |
| Bluetooth (BLE) | `CONFIG_BLUETOOTH`, `CONFIG_NIMBLE` |
| Audio | `CONFIG_AUDIO` |
| Power management | `CONFIG_PM` |

Contestants may also refer to `vendor/openvela/boards/vela/configs/goldfish-x86_64-ap/defconfig` (253 lines) as a reference example of openvela's full CONFIG set with all subsystems enabled, useful as a comparison baseline when adding subsystems incrementally.

## 6. Functional validation

Once subsystems are enabled, it is recommended to validate functional completeness on the target hardware using standardized test cases. The openvela community maintains an xTS test case collection for community developers, covering peripheral drivers, filesystem, networking, media, and other subsystems, which can serve as a functional acceptance reference once a subsystem has been enabled.

### 6.1 Recommended usage

- **L0 boot validation**: after the minimum set in this document brings up NSH, manually run commands such as `help`, `uname`, and `ps` on the serial console to verify basic shell and syscall behavior.
- **Subsystem functional validation**: after enabling each subsystem, run the corresponding test cases from the xTS collection (e.g. run the SPI_I2C tests after enabling the SPI/I2C drivers).
- **Regression validation**: once porting stabilizes, the full xTS suite can serve as a regression set for verifying functionality after subsequent configuration changes.

### 6.2 xTS coverage areas

| Test topic | Applicable scenario |
| ---- | ---- |
| SPI / I2C drivers | Validate bus communication after peripheral drivers are enabled (includes a BMI160 sensor example) |
| Ymodem file transfer | Validate serial-port file transfer capability |
| mediatool media tests | Validate audio/video codec and playback pipelines |
| Wi-Fi compatibility | Verified-router list and connection-stability validation |
| Self-test framework (cmocka) | How to use the framework when authoring custom unit tests |

For detailed test steps, test resources, and dependency configurations, refer to the [openvela Community Developer xTS Test Case Collection (zh-cn)](../../../../zh-cn/test_dev_guide/openvela_xts_test_cases.md) and the [openvela Test Framework Usage Guide](../../../test_dev_guide/openvela_testcase_dev_guide.md). The xTS test case collection is currently available in Chinese only.

## 7. New-hardware adaptation Checklist

After completing BSP porting, contestants are advised to validate the defconfig and target-hardware compatibility against the following checklist:

- [ ] `CONFIG_ARCH`, `CONFIG_ARCH_CHIP`, and `CONFIG_ARCH_BOARD` have been replaced with target-hardware identifiers
- [ ] `CONFIG_RAM_START` and `CONFIG_RAM_SIZE` have been filled in per the target chip's datasheet
- [ ] For chips with multiple SRAM regions (e.g. STM32F4 with CCM), `CONFIG_MM_REGIONS` has been set correctly
- [ ] The serial peripheral macro (e.g. `CONFIG_STM32_USART2=y`) has been switched to the target chip's UART
- [ ] `CONFIG_USART<N>_SERIAL_CONSOLE=y` is consistent with the pin definitions in `board.h`
- [ ] The serial baud rate defaults to 115200 and matches the host terminal
- [ ] `CONFIG_SYSTEM_NSH=y` and `CONFIG_INIT_ENTRYPOINT="nsh_main"` are enabled
- [ ] `CONFIG_DEBUG_SYMBOLS=y` and `CONFIG_ARCH_STACKDUMP=y` are enabled to aid boot-issue diagnostics
- [ ] Cores with FPU (M4F/M7) have `CONFIG_ARCH_FPU=y`; cores without FPU (M0/M3) keep it disabled
- [ ] `CONFIG_BOARD_LOOPSPERMSEC` has an initial estimate based on the CPU frequency

After passing the checklist, run `./build.sh <vendor>:<config> -j` to build. After flashing, when the serial console is connected and the `nsh> ` prompt appears, L0 has booted successfully.

## 8. References

### 8.1 openvela internal references

| Resource | Description |
| ---- | ---- |
| `nuttx/boards/arm/stm32/nucleo-f303re/configs/nsh/defconfig` | Recommended L0 reference defconfig (35 lines) |
| `nuttx/boards/arm/stm32/nucleo-f303re/include/board.h` | Board-level clock and pin reference |
| `nuttx/boards/arm/nrf52/nrf52840-dk/configs/nsh/defconfig` | Minimum NSH reference for the nRF52 platform |
| `nuttx/boards/sim/sim/sim/configs/nsh/defconfig` | Toolchain self-check reference |
| `vendor/openvela/boards/vela/configs/goldfish-x86_64-ap/defconfig` | Full-subsystem example (253 lines), useful as a reference when enabling subsystems incrementally |
| [openvela Chip Porting Guide](../../../chip_porting/porting_guide.md) | Complete BSP porting workflow from scratch |
| [Hardware Porting Track Guide (zh-cn)](../../../../zh-cn/contest_2026/hardware_porting/hardware_porting_track_guide.md) | Track description, scoring criteria and reference resources (Chinese only at this stage) |
| [Kconfig Usage Guide](../../../device_dev_guide/build/Kconfig.md) | Detailed explanation of the relationship between menuconfig, defconfig, and .config |
| [openvela Community Developer xTS Test Case Collection (zh-cn)](../../../../zh-cn/test_dev_guide/openvela_xts_test_cases.md) | Functional validation test cases for subsystems after enablement (covers peripherals, filesystem, networking, media, etc., Chinese only at this stage) |
| [openvela Test Framework Usage Guide](../../../test_dev_guide/openvela_testcase_dev_guide.md) | Setup and usage of the test framework (cmocka, etc.) |

### 8.2 External references

The "NuttX and small systems" blog series by Mateusz Szafoni ([@raiden00pl](https://github.com/raiden00pl)) provides an in-depth exploration of minimal NuttX configuration practices on resource-constrained MCUs. It is a valuable reference for resource trimming and incremental subsystem enablement after L0:

| Article | Topic |
| ---- | ---- |
| [Apache NuttX and small systems - Hello, World !](https://www.railab.me/posts/2024/11/nuttx-and-small-systems-hello-world/) | Booting a minimal NuttX system on a small MCU |
| [Apache NuttX and small systems - NuttX Core Size](https://www.railab.me/posts/2024/12/nuttx-and-small-systems-core-os/) | NuttX kernel size analysis and Flash/RAM footprint |
| [Apache NuttX and small systems - OS components](https://www.railab.me/posts/2025/1/nuttx-and-small-systems-os-components/) | OS component switches and their resource costs |
| [Apache NuttX and small systems - CAN node example](https://www.railab.me/posts/2025/2/nuttx-and-small-systems-can-node-example/) | A minimal CAN node implementation on STM32 |
| [Apache NuttX and small systems - Modbus slave example](https://www.railab.me/posts/2025/3/nuttx-and-small-systems-modbus-slave-example/) | Fitting a Modbus RTU slave application within 64 KB of Flash |
