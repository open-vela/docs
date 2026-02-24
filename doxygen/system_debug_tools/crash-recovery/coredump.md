/**
 * @file coredump.md
 * @brief Crash 现场还原 —— Coredump 机制
 *
 * @section coredump_overview 概述
 *
 * Coredump 是 Crash 现场还原类工具体系中最核心的机制，用于在系统发生致命异常
 * 并即将停止运行之前，完整保存系统当下的运行现场。
 *
 * 当系统发生不可恢复错误（如非法内存访问、硬件 Fault、断言失败等）时，
 * Coredump 机制会将系统的关键状态冻结并持久化，从而为后续的离线分析提供
 * 可还原的“时间快照”。
 *
 * 在嵌入式系统中，Coredump 是解决“一次性 Crash”与“不可复现问题”的
 * 最可靠手段。
 *
 * @section coredump_mechanism 基本机制
 *
 * 在系统进入 Crash 流程后，Coredump 机制会在系统彻底停止运行之前，
 * 将以下关键信息保存为一个持久化的 Core 文件：
 *
 * - CPU 寄存器状态（PC / SP / LR / 通用寄存器等）
 * - 所有线程的上下文与调用栈信息
 * - 系统内存映像（堆、栈、全局变量、动态分配内存等）
 * - 多核系统中其它 CPU 的同步现场（如适用）
 *
 * 该 Core 文件可在 PC 端结合对应的 ELF 固件，通过 GDB 等工具进行
 * 离线调试和深度分析。
 *
 * @section coredump_value 核心价值
 *
 * Coredump 的本质是一台“时间机器”：
 *
 * - 将瞬时的、不可再现的系统状态冻结为静态文件
 * - 允许工程师在任意时间、任意地点反复分析同一次崩溃
 * - 不依赖在线调试器或问题复现环境
 *
 * 对于资源受限、并发复杂的嵌入式系统，Coredump 是事后分析（Post-mortem Analysis）
 * 的基础能力。
 *
 * @section coredump_config 基本配置
 *
 * 启用 Coredump 机制需要以下配置项：
 *
 * @code
 * CONFIG_COREDUMP=y
 *
 * /* 默认启用，压缩 coredump 数据，减少原始镜像体积 */
 * CONFIG_BOARD_COREDUMP_COMPRESSION=y
 *
 * /* 默认启用，保存所有线程的上下文信息；
 *  * 若关闭，仅保存触发异常的线程 */
 * CONFIG_BOARD_COREDUMP_FULL=y
 * @endcode
 *
 * @section coredump_trigger Coredump 触发方式
 *
 * Coredump 的生成统一发生在系统进入异常状态（Crash）时，
 * 根据触发来源可分为以下三类：
 *
 * @subsection coredump_trigger_auto 系统异常自动触发
 *
 * 系统检测到不可恢复错误时自动触发 Coredump，典型场景包括：
 *
 * - 断言失败（ASSERT / PANIC）
 * - HardFault / BusFault / UsageFault
 * - 栈溢出
 * - 非法内存访问
 * - 调度器致命错误
 *
 * @subsection coredump_trigger_manual 手工触发
 *
 * 在调试或问题复现阶段，可通过主动触发 Crash 获取系统现场，例如：
 *
 * - 串口输入特定组合键
 * - 调试工具触发 panic
 * - 调试代码中调用 PANIC() / up_assert()
 *
 * 手工触发后的处理流程与真实异常完全一致。
 *
 * @subsection coredump_trigger_multicore 多核系统触发
 *
 * 在 SMP / AMP 系统中，当任一核心发生异常后：
 *
 * - 其它核心会被通知并同步进入 Crash 流程
 * - 各核心寄存器、栈与上下文被统一保存
 *
 * 该机制保证多核系统现场的一致性与完整性。
 *
 * @section coredump_store Coredump 保存方式
 *
 * Coredump 数据可通过多种方式保存，具体取决于平台资源与配置：
 *
 * @subsection coredump_store_syslog Syslog 输出（默认）
 *
 * @code
 * CONFIG_BOARD_COREDUMP_SYSLOG=y
 * @endcode
 *
 * 通过系统日志输出 Coredump 数据，通常为 HEX 或 Base64 编码文本。
 *
 * @subsection coredump_store_blkdev Block Device
 *
 * @code
 * CONFIG_BOARD_COREDUMP_BLKDEV=y
 * CONFIG_BOARD_COREDUMP_DEVPATH="/dev/coredump"
 * @endcode
 *
 * @subsection coredump_store_mtd MTD Flash
 *
 * @code
 * CONFIG_BOARD_COREDUMP_MTDDEV=y
 * CONFIG_BOARD_COREDUMP_DEVPATH="/dev/trapinfo"
 * @endcode
 *
 * @subsection coredump_store_memflash Mem Flash
 *
 * @code
 * CONFIG_BOARD_COREDUMP_MTDDEV=y
 * CONFIG_BOARD_COREDUMP_DEVPATH="/dev/mem"
 * @endcode
 *
 * @section coredump_memory_range 多核与额外内存区段保存
 *
 * 在多核或复杂 SoC 场景中，可配置额外内存区段一并保存：
 *
 * @code
 * CONFIG_BOARD_MEMORY_RANGE="{0x3c000000,0x3e000000,0x6}"
 * @endcode
 *
 * 用于补充非默认内存映射区域的数据。
 *
 * @section coredump_usage 使用流程概述
 *
 * Coredump 的典型使用流程包括：
 *
 * 1. 设备端生成并保存 Coredump 数据
 * 2. 将 Coredump 数据导出至 PC
 * 3. 使用工具将原始数据转换为标准 .core 文件
 * 4. 结合对应 ELF 文件，通过 GDB 进行离线调试
 *
 * 详细调试流程与命令参见后续 gdbserver 与 GDB 调试章节。
 *
 * @section coredump_scenario 适用场景
 *
 * Coredump 特别适用于以下问题场景：
 *
 * - 仅发生一次、无法复现的 Crash
 * - 内存破坏、竞态条件导致的随机崩溃
 * - 多线程 / 多核系统中的复杂异常
 * - 无法使用在线调试器的设备环境
 *
 * 在调试工具体系中，Coredump 是 Crash 现场还原阶段的基础能力。
 */
