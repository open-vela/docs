# Developer FAQ

[ English | [简体中文](./../../zh-cn/faq/devoloper_tech_faq.md) ]

## I. Community and General

### 1. What should I do if I encounter technical issues or bugs?

If it is a technical issue, please submit it on the [Issue page](../../../../docs/issues).

- For blocking issues, after submitting the Issue, you can send the link directly to the WeChat group for a quick response.
- For non-blocking issues, the community maintenance team will reply and handle them regularly within the Issue tracker.

### 2. Are there rewards for community contributions?

Yes, the community has a contribution incentive mechanism. For detailed reward rules and instructions, please refer to the [Contribution Reward Instructions](../../../../docs/issues).

### 3. When will the IDE be released?

It has been released. openvela now ships an official VS Code plugin that supports the full development lifecycle on Ubuntu — project creation, build, system debugging, and application development. See the [openvela VS Code Plugin User Guide](../quickstart/vscode_plugin_usage.md) for details.

### 4. Is there a difference between the Gitee and GitHub versions of the source code repository?

There is no difference between the two. The GitHub and Gitee internal repositories utilize bidirectional real-time synchronization. You can choose either one for access based on your network conditions.

## II. Compilation and Build

### 5. Does openvela application development (e.g., Hello World) run in kernel mode or user mode?

The system primarily supports three compilation modes.

Currently, the official recommendation is to use **Flat Build**, where applications and the kernel reside in the same address space (similar to kernel mode). This provides optimal performance and is suitable for embedded small systems such as modules and smart bands.

Additionally, Kernel Build (user mode isolation) and Product Mode are supported, but they are less commonly used in resource-constrained scenarios.

### 6. Using the recommended Flat Build mode, will an application crash cause the entire system to crash?

Theoretically, in Flat Build mode, since applications and the kernel share the same space, an application crash can indeed affect the system. However, openvela is developing a polymorphic isolation protection mechanism to prevent memory corruption. Although the system supports running ELF binary files, the official recommendation remains strongly in favor of using Flat Build mode for embedded scenarios.

### 7. Does openvela support incremental compilation? Do I need to rebuild everything every time I modify the code?

The system supports incremental compilation.

- If you only modified `.c` or `.h` source files, you can compile incrementally, which is relatively fast.
- However, if you modified the `Kconfig` (menuconfig) configuration file (i.e., enabled or disabled certain features), it is recommended to perform a full recompilation to ensure the configuration takes effect properly.

## III. System Architecture and Kernel

### 8. Is the openvela protocol stack located in the module or on the AP side?

The protocol stacks (such as TCP/IP, Bluetooth Host Stack, etc.) run on the AP (Application Processor) side. External WiFi or Bluetooth modules are typically used only as transceivers, communicating with the main controller via interfaces like HCI or SDIO, with the modules primarily running firmware internally.

### 9. I see many functions starting with NX_ in the code (e.g., nx_read). Should I use them in my application?

**It is not recommended.**

Functions starting with `NX_` are typically system calls or low-level encapsulations used internally by the kernel.

To ensure code standardization and portability (openvela has passed PNS 52 certification), please strictly use standard POSIX interfaces (such as `open`, `read`, `pthread_create`) for development.

### 10. In isolation mode, does user memory use a physical flat model or virtual address mapping?

The system uses a **Physical Flat Memory Model**.

In this model, user memory is not mapped via virtual addresses through an MMU like in Linux. Instead, independent segments are partitioned within the physical flat memory.

### 11. Do user memory segments of different processes (Tasks) have the same virtual base address?

**No, they do not.**

Since there is no virtual address overlapping, different processes do not share the same virtual base address (e.g., all processes starting from 0x0000). Each process possesses an independent base address in physical memory, and different tasks are distinguished by their physical address ranges.

### 12. Does the system's isolation mechanism rely on MMU or MPU?

System memory isolation primarily relies on the **MPU (Memory Protection Unit)**.

This is designed to achieve secure isolation even on chips that do not possess an MMU (such as the Cortex-M series).

### 13. How is secure isolation achieved without an MMU?

This is achieved by defining access permission regions on physical memory via the MPU.

The system allocates specific physical memory regions for each task and utilizes the MPU to restrict that task to accessing only its allocated region, thereby realizing secure isolation between tasks at the physical addressing level.

### 14. In a multi-tasking environment, how are the user-mode Heap and Stack allocated?

To align with the MPU's region protection mechanism, each task is technically required to have an independent user-mode Heap and Stack. This ensures that runtime data storage does not interfere with others and prevents out-of-bounds memory access between tasks.

## IV. Development Environment and Tools

### 15. Are the JLink and Trace32 debugging tools mentioned in the documentation mandatory?

This depends on your run target.

If debugging on real hardware, hardware debuggers like JLink or Trace32 are usually required. If you are using a Simulator (running locally on Linux) or an Emulator (QEMU/Goldfish) for development, the system comes with built-in debugging mechanisms, and you can use GDB directly without extra hardware.

### 16. What if `repo sync` has no response or fails to download in the Ubuntu VM?

Please troubleshoot in the following order:

- Confirm you are downloading code based on the `trunk` branch.
- Confirm the operating system version is Ubuntu 22.04.
- Check network connections and proxy settings (there may be network firewall issues).

If the problem persists after troubleshooting, please screenshot the error message and submit an Issue in the community.

### 17. Does openvela have a companion VS Code plugin or IDE?

Yes, there is an official IDE customized based on VS Code that supports openvela development.

The current version has not yet been fully released as open source. It will be synchronized with developers as soon as it is officially released.

### 18. Why can the AI assistant (like the Doubao plugin) in the Quick App IDE only read code but not edit/automatically modify it?

This situation is usually caused by compatibility issues resulting from the synchronization delay between the rapidly updating VS Code core version and the VS Code source version built into the IDE.

It is recommended to report the specific plugin version and IDE version, and the development team will investigate and fix it.

### 19. Why can't I see network interfaces when enabling network configuration under the QEMU goldfish arm64 configuration?

This is because basic configurations like `goldfish arm64` are primarily used to verify CPU architecture and basic kernel functions, and do not enable complete network bridging or peripheral support by default.

If you need to verify network or multimedia functions, it is recommended to use product-form configuration files, such as the complete configuration for `smart speaker` or `ARMv7a Goldfish`.

### 20. Files created by programs running in the simulator are lost after restart. How can I achieve data persistence?

It is recommended to use the **9PFS (9P File System)** feature.

By directly mounting and mapping a folder from the host machine (Host PC) into the simulator, data can be written directly to the PC hard drive, achieving both persistence and convenient viewing on the PC side.

### 21. Why do low-power devices like smart bands/watches also use QEMU Goldfish (ARM A-series) for simulation?

This is mainly to unify the teaching platform and facilitate management; currently, the QEMU platform based on Google Goldfish is used uniformly.
The openvela operating system abstracts underlying architectural differences, so whether the bottom layer is A-series or M-series has little impact on the learning of upper-layer applications and frameworks. Support for ARM M/R series simulators will be released in the future.

### 22. Is it possible to start driver development learning and course design before physical development boards arrive?

**Absolutely.**

It is recommended to prioritize using the simulator (QEMU). The driver framework is consistent across the simulator and physical boards. You can first complete theoretical learning, framework development, and core concepts like memory management based on the simulator, and then perform hardware adaptation verification once the development board arrives.

### 23. Does Telephony (phone/communication) related business need to be verified on real devices?

It is recommended to use the **Simulator**.

Debugging communication business on real machines has a high threshold (requires Modem, SIM card, network access). The openvela simulator features a built-in Modem Simulator capable of fully simulating processes like making calls and sending/receiving SMS, which is sufficient to meet teaching needs.

### 24. Can the RPK file generated by Quick App packaging run directly on openvela devices?

Currently, it cannot. The Quick App framework engine (Runtime) is planned to be open-sourced in library form and integrated into the system around **June 2026**. At this stage, it is recommended to use the simulator for learning and development.

## V. Hardware Adaptation and Porting

### 25. Can openvela be ported to hardware platforms not currently officially supported (e.g., STM32)?

**Yes.**

openvela is fully compatible with the NuttX kernel. Theoretically, openvela can be smoothly adapted and ported to all hardware platforms supported by NuttX.

### 26. What is the current support status for ESP32 series development boards?

Although the bottom layer is compatible with NuttX, adaptation and testing for ESP32 are not yet fully covered, and some Demos may not run directly. If a stable development experience is required, it is currently recommended to prioritize using officially verified ARM platform development boards.

### 27. When developing drivers or low-level code, which directory should the code be submitted to?

Please decide based on the universality of the code:

- General driver frameworks, scheduling code, or bug fixes are recommended to be submitted to the `nuttx` main directory (e.g., under `drivers`).
- Specific chip vendor or private board-level driver code is recommended to be stored in the `vendor` directory.

openvela follows the Apache license, so you can freely choose whether to open source it.

### 28. After porting to a new development board, how can I verify the adaptation? Are there ready-to-use test cases?

**Yes.**

The openvela community provides a ready-to-use [xTS Test Case Collection](/document?id=XXX&version=trunk&language=en) that covers standard test cases for system kernel, driver BSP, filesystem, WiFi, Bluetooth, audio/video and other fundamental capabilities. Commands can be copied directly into nsh for execution without writing tests from scratch.

Test cases are divided into two categories:

- **General self-tests** (mandatory): cover fundamental capabilities such as memory, scheduling, GPIO, I2C/SPI, UART, RTC, Watchdog.
- **Category-specific self-tests** (optional): selected based on product characteristics, including WiFi, Bluetooth, LCD, Audio, filesystem, OTA, etc.

Once the basic tests pass, the results can serve as the acceptance criteria for the new platform port. If a test case does not apply to your platform or you have questions, please [file an issue on open-vela/docs](https://github.com/open-vela/docs/issues).

## VI. Application Framework and Multimedia

### 29. Is the underlying engine for openvela Quick Apps Node.js or V8?

Neither. The openvela device-side Quick App engine is based on **QuickJS**.

### 30. What is the difference in running mechanisms between Quick Apps and Native Apps?

- Quick Apps run in an independent container within the system, isolated from the system. A crash does not easily cause a system freeze, and they invoke underlying capabilities via JS interfaces.
- Native Apps call system APIs directly, offering higher performance but also a higher degree of coupling with the system.

### 31. Does openvela currently support running MPlayer?

Running MPlayer directly is currently not supported; the official team has not yet ported it.

### 32. What multimedia development tools or frameworks are available under the current system?

Currently available solutions include: ported FFmpeg, the system's built-in native multimedia toolkit (please refer to the [Sim Environment Audio Function Development Guide](../quickstart/emulator/sim_audio_guide.md)), and ported open-source codec libraries such as `libx264`, `openh264`, and `libopus`.

### 33. Which common Linux multimedia tools are suitable for porting to openvela?

Tools with a Pure Software implementation are usually easier to port. Tools that rely heavily on specific hardware drivers or hardware acceleration cannot be ported directly and must be adapted based on openvela's existing multimedia framework.

### 34. Is there any reference case or path if third-party code needs to be ported?

Developers are advised to directly reference the `apps/external` folder in the source directory. This directory contains a large number of ported third-party libraries and serves as the best practice for understanding the build system and porting methods.

### 35. For developing graphical interfaces on openvela, are Qt or GTK/JDK supported?

**Not supported and not recommended.**

- Qt and GTK frameworks are too heavy for embedded RTOS.
- The official recommendation is to use **LVGL**, which the team has deeply optimized and integrated well with the NuttX system.

### 36. Does openvela support IoT protocols like MQTT, CoAP, Matter?

**Yes.**

The system has integrated MQTT, CoAP, and Matter (partial versions).

Relevant libraries are usually located in the `apps/netutils` or `external` directories and can be referenced directly in the source code.

### 37. Is it necessary to deeply master kernel principles just to learn multimedia development?

**No.**

You only need to master basic system calls (such as threads, locks, message queues, Sockets). The learning focus should be on Pipeline design (decoding, post-processing), without needing to delve into kernel underlying implementations like scheduling algorithms.