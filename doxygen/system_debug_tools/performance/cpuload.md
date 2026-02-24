/**
 * @page cpuload cpuload 分析工具
 * @brief 线程级 CPU 使用率统计（top/ps 的底层数据来源）
 *
 * @section cpuload_overview 概述
 *
 * cpuload 是系统提供的一种线程级 CPU 使用率统计机制，用于刻画系统运行过程中各个线程（task）
 * 对 CPU 的占用情况。它是 top、ps 等系统监控命令的底层数据来源，可实时或准实时展示：
 * - 各线程的 CPU 使用率
 * - 系统整体负载分布
 * - 是否存在异常占用 CPU 的线程
 * :contentReference[oaicite:4]{index=4}
 *
 * 与其他性能工具的关注点不同：
 * - Trace / SystemView 更关注“什么时候发生了什么调度行为”
 * - perf / gprof 更关注“CPU 时间花在了哪些函数上”
 * - cpuload 更关注“当前 CPU 都被哪些线程占用了？”
 * 因此 cpuload 通常作为系统运行态的基础监控能力，用于问题初筛与运行态观察。 :contentReference[oaicite:5]{index=5}
 *
 * @section cpuload_config 基本配置
 *
 * cpuload 依赖内核采集线程运行信息的能力，启用时需配置（示意）：
 * @code{.text}
 * # 启用 CPULOAD 支持
 * CONFIG_SCHED_CPULOAD=y
 *
 * # 选择 CPULOAD 统计方式（示意）
 * CONFIG_SCHED_CPULOAD_SYSTICK=y
 * # 或
 * CONFIG_SCHED_CPULOAD_EXTCLK=y
 * # 或
 * CONFIG_SCHED_CPULOAD_CONTEXT_SWITCH=y
 * @endcode
 * :contentReference[oaicite:6]{index=6}
 *
 * @section cpuload_principle 工作原理
 *
 * cpuload 的核心目标是：统计每个线程在一定时间窗口内实际占用 CPU 的比例。其实现依赖内核对线程
 * 运行状态的感知，主要存在三种实现方式。 :contentReference[oaicite:7]{index=7}
 *
 * @subsection cpuload_principle_systick 1) 基于定时采样（Systick）
 *
 * 利用系统核心节拍定时器（System Tick Timer）中断，在每个 tick 对当前正在运行的任务采样估算负载：
 * - 工作原理：在系统时钟中断服务程序中，对当前活动任务的执行时间进行累加
 * - 优点：配置简单，不依赖额外硬件定时器
 * - 缺点：精度受限于系统时钟频率，可能无法精确捕捉短时运行任务
 * :contentReference[oaicite:8]{index=8}
 *
 * @subsection cpuload_principle_extclk 2) 基于定时采样（外部时钟）
 *
 * 使用独立硬件定时器（External Timer）以更高频率采样，以获得更精确的 CPU 负载数据：
 * - 工作原理：配置专用硬件定时器，以高于系统时钟的频率触发中断，并在 ISR 中对活动任务采样
 * - 优点：统计精度更高，更准确反映任务瞬时 CPU 占用
 * - 缺点：需要额外硬件定时器，且需要目标硬件平台（BSP）提供驱动适配
 * :contentReference[oaicite:9]{index=9} :contentReference[oaicite:10]{index=10}
 *
 * @subsection cpuload_principle_ctxsw 3) 基于线程切换（Context Switch）
 *
 * 通过 SCHED_CRITMONITOR 模块记录任务启动/停止的时间戳，累计每个任务的实际执行时长来计算 CPU 占用率：
 * - 工作原理：利用性能监控器记录任务切换的精确时间点，累计执行时长
 * - 优点：三种方式中精度最高，不受采样频率限制，能真实反映任务 CPU 消耗
 * - 缺点：引入轻微性能开销（任务切换时需要记录额外时间信息）
 * :contentReference[oaicite:11]{index=11}
 *
 * @section cpuload_notes 注意事项
 *
 * - 统计方式的选择本质是“精度 vs 成本”的权衡：Systick 最易用但精度受限；外部时钟精度更高但依赖 BSP；
 *   基于线程切换精度最高但会引入轻微切换路径开销。 :contentReference[oaicite:14]{index=14} :contentReference[oaicite:15]{index=15}
 */
