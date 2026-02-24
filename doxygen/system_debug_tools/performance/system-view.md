/**
 * @file systemview.md
 * @brief SystemView 实时 Trace 可视化分析工具
 *
 * @section systemview_overview 概述
 *
 * SystemView 是 OpenVela Trace 体系中的一种高实时性、强可视化的 Trace 输出工具，
 * 主要用于将内核运行过程中的调度行为、中断活动以及系统调用等事件，
 * 以极低延迟实时传输到上位机，并以时间轴形式进行可视化分析。
 *
 * 与 NoteRAM、Syslog、RTT 等 Trace 后端侧重“日志保存”不同，
 * SystemView 的核心目标是 **实时观测系统运行行为**，
 * 帮助开发者回答如下问题：
 *
 * - 当前系统在“什么时候”发生了任务切换？
 * - 哪些中断在高频触发？
 * - 某一时间段内 CPU 的调度行为是否符合预期？
 *
 * SystemView 并未引入新的插桩机制，
 * 而是复用 Trace / sched_note 产生的统一事件源，
 * 仅在 Note Driver 层将事件映射为 SEGGER SystemView 协议，
 * 并通过 RTT 通道实时发送到主机端进行解析与展示。
 *
 *
 * @section systemview_principle 工作原理
 *
 * SystemView 的整体工作流程如下：
 *
 * 1. **内核插桩阶段**
 *    - 内核关键路径（任务切换、中断进入/退出、系统调用等）
 *      通过 sched_note 机制产生统一的 Trace 事件。
 *
 * 2. **Note Driver 映射阶段**
 *    - SystemView 作为一种 Note Driver，
 *      订阅 sched_note 事件流；
 *    - 将内核 Trace 事件转换为 SEGGER SystemView 协议格式。
 *
 * 3. **RTT 实时传输阶段**
 *    - 通过 SEGGER RTT 通道，将事件以低延迟方式发送至主机；
 *    - 不依赖串口打印，适合高频 Trace 场景。
 *
 * 4. **主机端可视化分析**
 *    - 使用 SEGGER SystemView 工具加载 RTT 数据；
 *    - 以时间轴方式展示任务调度、IRQ、系统行为。
 *
 * 该机制的关键优势在于：
 *
 * - 插桩点与 Trace / Perfetto 完全一致；
 * - 差异仅体现在 Note Driver 层；
 * - 不影响现有 Trace 数据模型；
 * - 适用于实时调试与性能分析阶段。
 *
 *
 * @section systemview_config 配置说明
 *
 * SystemView 依赖 Trace / sched_note 基础能力，
 * 启用前需首先打开内核调度插桩功能。
 *
 * @subsection systemview_trace_config Trace / sched_note 配置
 *
 * @code{.config}
 * CONFIG_SCHED_INSTRUMENTATION=y
 * CONFIG_SCHED_INSTRUMENTATION_DUMP=y
 * @endcode
 *
 * 根据分析需求，可进一步开启以下事件类型：
 *
 * @code{.config}
 * CONFIG_SCHED_INSTRUMENTATION_SWITCH=y      /* 任务切换事件 */
 * CONFIG_SCHED_INSTRUMENTATION_IRQHANDLER=y  /* 中断 enter / leave */
 * CONFIG_SCHED_INSTRUMENTATION_SYSCALL=y     /* 系统调用 */
 * @endcode
 *
 *
 * @subsection systemview_driver_config SystemView 驱动配置
 *
 * 启用 SystemView Note Driver：
 *
 * @code{.config}
 * CONFIG_SEGGER_SYSVIEW=y
 * @endcode
 *
 * 常用可调参数包括：
 *
 * @code{.config}
 * CONFIG_SEGGER_SYSVIEW_FILTER_DEFAULT_MODE=0
 * CONFIG_SEGGER_SYSVIEW_CPUSET=
 * CONFIG_SEGGER_SYSVIEW_RTT_BUFFER_SIZE=20480
 * CONFIG_SEGGER_SYSVIEW_RAM_BASE=
 * @endcode
 *
 *
 * @subsection systemview_rtt_config RTT 支持配置
 *
 * SystemView 基于 SEGGER RTT 进行数据传输，
 * 需确保 RTT 功能已启用：
 *
 * @code{.config}
 * CONFIG_RTT=y
 * @endcode
 *
 * RTT 的缓冲区大小、通道数量需满足 SystemView 的实时传输需求，
 * 避免 Trace 数据丢失。
 *
 *
 * @section systemview_example 使用示例
 *
 * 使用 SystemView 进行实时 Trace 分析的典型流程如下：
 *
 * 1. 系统正常启动，并完成上述配置；
 * 2. 上位机启动 SEGGER SystemView 工具；
 * 3. 通过 RTT 连接目标设备；
 * 4. 实时观察以下信息：
 *    - 任务切换时间轴
 *    - 各线程运行时序
 *    - IRQ 触发频率与嵌套关系
 *    - 系统调用行为
 *
 * 该方式适合：
 * - Bring-up 阶段调度行为验证
 * - 实时性能瓶颈定位
 * - 中断风暴、调度抖动分析
 *
 *
 * @section systemview_scene 适用场景与限制
 *
 * **适用场景**
 * - 实时调试系统调度行为
 * - IRQ 频率与时序分析
 * - 低延迟 Trace 可视化
 * - 性能调优与行为验证阶段
 *
 * **注意事项**
 * - SystemView 更关注“实时性”，不适合长期日志保存；
 * - RTT 缓冲区过小可能导致 Trace 数据丢失；
 * - 不适用于无 RTT 支持的平台；
 * - 对 Flash / RAM 有一定额外占用。
 *
 * 在工程实践中，SystemView 常与：
 * - Perfetto（离线 Trace 分析）
 * - cpuload / perf / gprof（统计类工具）
 * 形成互补使用关系。
 */
