/**
 * @defgroup online_jlink J-Link Debugger Support
 * @ingroup online_debug_tools
 * @brief 基于 J-Link 的在线调试与数据通道支持
 *
 * J-Link 是 SEGGER 公司推出的 JTAG / SWD 仿真器，
 * 广泛用于 ARM 内核芯片的软件调试与下载。
 *
 * 在 OpenVela 调试体系中，J-Link 不仅用于传统的
 * 断点调试与寄存器查看，还被扩展用于：
 * - 无物理串口条件下的交互式控制台（NSH）
 * - 高速日志输出（Syslog）
 *
 * 这些能力主要基于 J-Link 的 RTT（Real-Time Transfer）机制实现，
 * 以共享内存作为通信介质，绕过传统串口的波特率瓶颈，
 * 在调试阶段提供更高吞吐与更低侵入性的交互能力。
 */

/**
 * @section jlink_nsh J-Link NSH Console
 * @brief 基于 RTT 的 NSH 交互终端
 *
 * J-Link NSH Console 功能基于 J-Link RTT 实现，
 * 使用一段共享内存作为串口设备的通信介质。
 *
 * 该方式不依赖物理 UART，因此不受波特率限制，
 * 实际传输速率主要受芯片运行频率和调试接口速度影响。
 */

/**
 * @subsection jlink_nsh_config Configuration
 * @brief 基本配置
 *
 * 启用 J-Link NSH Console 需要在系统配置中完成以下设置：
 *
 * @par 禁用其他串口作为系统控制台
 * @code
 * CONFIG_OTHER_SERIAL_CONSOLE=n
 * @endcode
 *
 * @par 启用 RTT 串口
 * @code
 * CONFIG_SERIAL_RTT0=y
 * @endcode
 *
 * @par 启用 RTT 串口终端
 * @code
 * CONFIG_SERIAL_RTT_CONSOLE=y
 * @endcode
 */

/**
 * @subsection jlink_nsh_usage Usage
 * @brief 使用方法
 *
 * RTT 数据通过 J-Link GDB Server 转发至本地主机端口，
 * 再映射为虚拟 TTY 设备供终端程序使用。
 *
 * @par 启动 J-Link GDB Server
 * @code
 * JLinkGDBServer -if SWD -device stm32h743zi -speed 20000
 * @endcode
 *
 * @par RTT 数据端口转发（需要 root 权限）
 * @code
 * sudo socat -d -d \
 *   PTY,link=/dev/Vela-console,raw,ignoreeof \
 *   TCP:127.0.0.1:19021,reuseaddr
 * @endcode
 *
 * @par 使用终端访问 NSH
 * @code
 * sudo minicom -D /dev/Vela-console
 * @endcode
 *
 * 通过该方式，开发者可在无物理串口条件下，
 * 直接与系统 NSH 终端进行交互。
 */

/**
 * @section jlink_syslog J-Link Syslog
 * @brief 基于 J-Link 的日志输出机制
 *
 * J-Link Syslog 提供了一种无需额外串口资源的日志输出方式，
 * 可用于调试阶段的系统日志采集。
 *
 * OpenVela 支持两种基于 J-Link 的 Syslog 输出模式。
 */

/**
 * @subsection jlink_syslog_console Syslog via Console
 * @brief Syslog 复用 Console 通道
 *
 * 在该模式下，Syslog 与 NSH Console 共用同一 RTT 通道，
 * 系统通过 /dev/console 输出日志。
 *
 * 该方式配置简单，适用于：
 * - 调试早期阶段
 * - 日志量较小的场景
 *
 * 但需要注意：
 * - Syslog 与交互式终端输出混合
 * - 不适合高频日志或自动化分析
 */

/**
 * @subsection jlink_syslog_rtt Syslog via Dedicated RTT Channel
 * @brief 使用独立 RTT 通道输出 Syslog
 *
 * 在该模式下，Syslog 使用独立的 RTT 通道输出，
 * 与 NSH Console 分离。
 *
 * 相较于复用 Console 通道：
 * - 日志结构更清晰
 * - 适合高频日志输出
 * - 更利于自动化采集与后处理
 *
 * 该模式通常用于：
 * - 性能分析阶段
 * - 大规模日志采集
 * - 与 Trace / Profiling 工具配合使用
 */
