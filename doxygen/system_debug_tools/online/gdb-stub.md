/**
 * @defgroup gdb_stub GDB Stub
 * @ingroup online_debug
 * @brief OpenVela/NuttX 轻量级远程调试服务器（GDB Remote Stub）
 *
 * @details
 * GDB Stub 是 OpenVela 在 NuttX 系统中集成的一个轻量级远程调试服务器，
 * 遵循 GNU GDB 的 Remote Serial Protocol（RSP）规范。
 *
 * 设备在运行过程中可以通过 UART / USB / 网络端口接收来自主机端 GDB
 * 的调试指令，从而在无硬件调试器的情况下完成底层调试。
 *
 * 与 GDB Plugin 提供的“系统语义级调试”不同，GDB Stub 提供的是
 * CPU 与内存级别的底层调试能力，是 OpenVela 在线调试体系中的
 * 核心基础组件之一。
 */

/**
 * @section gdbstub_capabilities 功能能力
 *
 * GDB Stub 支持以下典型调试能力：
 *
 * - 读取 / 修改 CPU 寄存器
 * - 读取 / 写入任意内存地址
 * - 设置 / 删除断点与监视点
 * - 单步执行与继续执行
 * - Crash 后进入调试环境进行现场分析
 * - 导出 Coredump（通过 nxgcore / gcore）
 *
 * 所有能力均通过 GDB Remote Serial Protocol 与主机端 GDB 交互完成。
 */

/**
 * @section gdbstub_usage 使用场景
 *
 * GDB Stub 主要用于以下两类场景：
 *
 * - 设备上无硬件调试器（J-Link / Trace32），
 *   需要通过串口、USB 或网络进行底层调试；
 *
 * - 系统发生 Crash 后，自动进入可调试状态，
 *   用于辅助现场还原与问题定位。
 */

/**
 * @section gdbstub_config 配置说明
 *
 * GDB Stub 根据运行位置不同，可分为应用层 Stub 与内核层 Stub，
 * 二者的配置方式与能力存在差异。
 */

/**
 * @subsection gdbstub_app 应用层 GDB Stub
 *
 * 若仅需要在系统正常运行时提供在线调试能力，
 * 可启用应用层 GDB Stub：
 *
 * @code
 * CONFIG_LIB_GDBSTUB=y
 * CONFIG_SYSTEM_GDBSTUB=y
 * @endcode
 *
 * 特点：
 * - Stub 运行在普通任务上下文中
 * - 适合通过 WiFi / USB / UART 进行在线调试
 * - 不接管 HardFault
 * - Crash 时不会自动进入调试模式
 */

/**
 * @subsection gdbstub_kernel 内核层 GDB Stub（Crash 调试）
 *
 * 若希望在系统 Crash 时自动接管调试串口并进入 GDB，
 * 需要启用串口级 GDB Stub：
 *
 * @code
 * CONFIG_LIB_GDBSTUB=y
 * CONFIG_SERIAL_GDBSTUB=y
 * CONFIG_SERIAL_GDBSTUB_PATH="/dev/ttyS1"
 * @endcode
 *
 * 说明：
 * - CONFIG_SERIAL_GDBSTUB
 *   使 GDB Stub 能在中断上下文中工作；
 *
 * - CONFIG_SERIAL_GDBSTUB_PATH
 *   指定用于调试的串口设备。
 *
 * 可选配置：
 *
 * @code
 * CONFIG_SERIAL_GDBSTUB_AUTO_ATTACH=y
 * @endcode
 *
 * 含义：
 * - Y：系统 Crash 后自动接管调试串口并立即进入 Stub；
 * - N：Crash 后需用户按指定按键才进入调试模式。
 *
 * 注意：
 * - 若设备存在多个串口（如 /dev/ttyS0、/dev/ttyS1），
 *   需确保调试串口未被 NSH 等组件占用。
 */

/**
 * @section gdbstub_memrange 内存访问范围限制
 *
 * 为避免 GDB 在调试过程中读写非法地址，
 * 导致系统发生二次异常，可通过如下配置
 * 限制 GDB Stub 允许访问的物理内存范围：
 *
 * @code
 * CONFIG_BOARD_MEMORY_RANGE="start,end,flags"
 * @endcode
 *
 * 该配置用于约束 GDB 可访问的内存区间，
 * 提升在线调试过程中的系统安全性与稳定性。
 */
