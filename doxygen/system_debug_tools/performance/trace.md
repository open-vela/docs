/**
 * @section trace_config 配置说明
 *
 * Trace 分析工具基于 NuttX 的 sched_note 机制实现，其功能启用与行为
 * 主要由 Kconfig 选项控制。根据实际调试需求，可在信息完整度、
 * 运行开销与存储成本之间进行权衡。
 *
 * @subsection trace_config_core 核心配置（必选）
 *
 * 以下配置为启用 Trace 机制的基础条件：
 *
 * @code{.config}
 * CONFIG_SCHED_NOTE=y
 * @endcode
 *
 * 启用 sched_note 基础框架，是所有 Trace 功能的前提。
 *
 * @subsection trace_config_events 事件类型配置
 *
 * Trace 支持对不同类型的系统事件进行独立控制，常见配置如下：
 *
 * - 任务调度事件
 * @code{.config}
 * CONFIG_SCHED_NOTE_TASK_SWITCH=y
 * CONFIG_SCHED_NOTE_TASK_START=y
 * CONFIG_SCHED_NOTE_TASK_STOP=y
 * @endcode
 *
 * 用于记录任务创建、切换、退出等调度行为，是调度分析的核心数据来源。
 *
 * - 中断事件
 * @code{.config}
 * CONFIG_SCHED_NOTE_IRQ=y
 * @endcode
 *
 * 用于记录 IRQ 进入 / 退出事件，支持中断嵌套与中断时序分析。
 *
 * - 系统调用事件
 * @code{.config}
 * CONFIG_SCHED_NOTE_SYSCALL=y
 * @endcode
 *
 * 用于分析系统调用频率与内核路径开销。
 *
 * - 临界区与锁相关事件（可选）
 * @code{.config}
 * CONFIG_SCHED_NOTE_CRITSECT=y
 * @endcode
 *
 * 用于分析临界区持续时间与潜在锁竞争问题。
 *
 * @subsection trace_config_buffer 缓冲区与存储配置
 *
 * Trace 数据通常通过 RAM 环形缓冲区进行缓存，以降低运行时开销：
 *
 * @code{.config}
 * CONFIG_DRIVERS_NOTE=y
 * CONFIG_DRIVERS_NOTERAM=y
 * @endcode
 *
 * 启用 NoteRAM 作为 Trace 数据的主要存储后端。
 *
 * - NoteRAM 缓冲区大小配置
 * @code{.config}
 * CONFIG_DRIVERS_NOTERAM_BUFSIZE=16384
 * @endcode
 *
 * 缓冲区大小直接影响可保留的 Trace 时间窗口：
 * - 较小缓冲区：开销低，适合长期运行
 * - 较大缓冲区：信息完整，适合问题复现阶段
 *
 * @subsection trace_config_smp 多核相关配置（SMP / AMP）
 *
 * 在多核系统中，Trace 可记录 CPU ID 信息，用于跨核分析：
 *
 * @code{.config}
 * CONFIG_DRIVERS_NOTE_CPUID=y
 * @endcode
 *
 * 启用后，Trace 事件中将携带 CPU ID 字段，便于区分事件来源核。
 *
 * @subsection trace_config_backend 后端与输出方式
 *
 * Trace 数据可被不同后端工具解析，常见使用方式包括：
 *
 * - SystemView / Trace32  
 *   通过 RTT / J-Link / Trace32 通道实时导出 Trace 数据。
 *
 * - Perfetto / 离线分析  
 *   将 NoteRAM 中的数据导出并转换为可视化格式。
 *
 * 后端选择不影响内核侧 Trace 机制，仅影响数据导出方式。
 *
 * @subsection trace_config_recommend 推荐配置组合
 *
 * - 调度与时序分析（常用）
 * @code{.config}
 * CONFIG_SCHED_NOTE=y
 * CONFIG_SCHED_NOTE_TASK_SWITCH=y
 * CONFIG_SCHED_NOTE_IRQ=y
 * CONFIG_DRIVERS_NOTERAM=y
 * CONFIG_DRIVERS_NOTERAM_BUFSIZE=16384
 * @endcode
 *
 * - 性能与临界区分析
 * @code{.config}
 * CONFIG_SCHED_NOTE=y
 * CONFIG_SCHED_NOTE_TASK_SWITCH=y
 * CONFIG_SCHED_NOTE_CRITSECT=y
 * CONFIG_SCHED_NOTE_SYSCALL=y
 * @endcode
 *
 * - 多核调度分析
 * @code{.config}
 * CONFIG_SCHED_NOTE=y
 * CONFIG_DRIVERS_NOTE_CPUID=y
 * @endcode
 */
