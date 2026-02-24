/**
 * @defgroup crashlog Crash Log + Backtrace + Allsyms
 * @ingroup crash_recovery
 * @brief 轻量级 Crash 现场保留与离线还原机制
 *
 * @details
 * 在资源受限或对恢复时延要求较高的嵌入式系统中，完整的 CoreDump
 * 由于存储空间占用大、写入耗时长，并不总是适合启用。
 *
 * OpenVela 提供了一种更轻量级的 Crash 现场保留方案：
 *
 *   Crash Log + Backtrace + Allsyms
 *
 * 该方案放弃全量内存快照，仅保留用于定位根因所必需的最小信息集，
 * 在 Flash 空间、异常恢复时间与调试有效性之间取得平衡。
 *
 * 该机制通常作为 CoreDump 的补充或替代方案使用。
 */

/**
 * @section crashlog_overview 机制概述
 *
 * Crash Log + Backtrace + Allsyms 方案通过组合三类信息，
 * 在系统崩溃时保留关键上下文：
 *
 * - Crash Log
 *   记录崩溃前后的系统日志与异常原因，提供时间维度上的上下文，
 *   用于回答“崩溃前系统在做什么”。
 *
 * - Backtrace（调用栈）
 *   在异常发生瞬间展开函数调用链，提供空间维度上的上下文，
 *   用于回答“在哪个函数路径中发生了错误”。
 *
 * - Allsyms（符号信息）
 *   将 PC/LR 等地址映射为函数名与偏移，减少人工 addr2line
 *   解析成本，提高日志可读性。
 *
 * 相比 CoreDump，该机制不保存完整内存映像，但成功保留了
 * 定位问题最关键的最小可行信息集（Minimal Viable Set）。
 */

/**
 * @section crashlog_config 配置说明
 *
 * 启用 Crash Log + Backtrace + Allsyms 需要以下配置项：
 *
 * @code
 * CONFIG_DEBUG_ALERT=y
 *
 * // 启用调用栈回溯
 * CONFIG_SCHED_BACKTRACE=y
 * CONFIG_SYSTEM_DUMPSTACK=y
 *
 * // 启用符号表支持（可选）
 * // 若 Flash 空间受限，可关闭并通过 addr2line 离线解析
 * CONFIG_ALLSYMS=y
 *
 * // 架构支持
 * CONFIG_ARCH_HAVE_BACKTRACE=y
 * @endcode
 *
 * 说明：
 * - Backtrace 是该机制的核心能力；
 * - Allsyms 用于提升日志可读性，但不是强制依赖；
 * - 在 Flash 紧张的平台，可关闭 Allsyms，改用离线地址解析。
 */

/**
 * @section crashlog_analysis 分析方式
 *
 * Crash Log + Backtrace 的分析方式主要分为两类：
 *
 * @subsection crashlog_gdbserver 基于 gdbserver.py 的离线调试（推荐）
 *
 * gdbserver.py 可以将 Crash Log 中的寄存器、栈内容与 PC/LR
 * 信息重建为一个“虚拟调试现场”，并通过 GDB 进行交互式分析：
 *
 * - 离线调用链回溯
 * - 栈帧展开与切换
 * - 寄存器查看
 * - 内存与局部变量访问
 * - 地址与符号自动映射
 *
 * 优点：
 * - 日志长度不影响分析效率
 * - 接近在线 GDB 的调试体验
 * - 无需复现问题或连接真实设备
 *
 * 具体流程详见 gdbserver 工具章节。
 *
 * @subsection crashlog_manual 基于日志的手动分析
 *
 * 在不使用 gdbserver 的情况下，也可直接基于日志进行人工分析。
 * 典型的 Crash Log 包含以下信息：
 *
 * - 异常触发原因（HardFault / Assert / Panic）
 * - 异常寄存器现场（R0–R12、SP、LR、PC、xPSR）
 * - 用户栈 / IRQ 栈内存 dump
 * - Backtrace（符号或地址）
 * - 多核系统下的各 CPU 现场
 *
 * 常见分析步骤包括：
 * - 定位异常类型与触发点
 * - 结合 PC/LR 确定崩溃指令位置
 * - 根据 Backtrace 还原调用链
 * - 结合栈内容分析参数或局部变量异常
 * - 在 SMP / AMP 场景下进行多核关联分析
 */

/**
 * @section crashlog_usage 使用场景
 *
 * Crash Log + Backtrace + Allsyms 适用于以下典型场景：
 *
 * - Flash / 存储空间极度受限，无法启用 CoreDump
 * - 系统需要在 Crash 后快速重启恢复运行
 * - 崩溃类型较为局部（空指针、栈溢出、断言失败）
 * - 作为 CoreDump 的补充手段，用于快速初步定位
 *
 * 对于一次性、不可复现、涉及复杂内存破坏的问题，
 * 仍推荐优先使用 CoreDump 机制进行完整现场还原。
 */
