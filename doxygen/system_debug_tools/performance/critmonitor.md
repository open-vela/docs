/**
 * @page tool_exec_time_monitor 执行时间统计工具
 * @brief 基于调度与临界区监控的执行时间统计与超时告警机制
 *
 * @section exec_time_overview 概述
 *
 * 在复杂嵌入式系统中，线程长时间占用 CPU、工作队列回调执行过久、
 * 关调度或关中断时间异常增长，往往会引发系统响应变慢、实时性下降，
 * 甚至触发 Watchdog 复位等严重问题。
 *
 * OpenVela 提供的 **执行时间统计工具**，用于在系统运行过程中对多类
 * 关键执行路径进行时间监控，并在运行时间超过预设阈值时自动通过
 * log 输出告警信息，从而帮助开发者快速定位异常执行路径。
 *
 * 该工具属于 **运行时行为分析类工具**，重点关注：
 * - 谁占用了 CPU
 * - 占用了多久
 * - 是否已经超出系统设计预期
 *
 * @section exec_time_capability 监控能力
 *
 * 执行时间统计工具可覆盖以下典型场景：
 *
 * - 线程连续运行时间（未被抢占）
 * - work_queue 回调函数执行时间
 * - 调度器锁（sched_lock / sched_unlock）持有时长
 * - 临界区（enter / leave critical section）持续时间
 * - 锁持有后的 Busy-Wait 等待时间
 * - IRQ 回调函数执行时间
 * - Watchdog 回调函数执行时间
 *
 * 当上述任一执行路径的运行时间超过配置阈值时，
 * 系统会自动输出告警日志，用于后续分析。
 *
 * @section exec_time_config 配置说明
 *
 * 执行时间统计工具通过一组 Kconfig 选项进行精细化配置，
 * 不同选项对应不同类型的执行路径监控：
 *
 * | 配置项 | 说明 |
 * |------|------|
 * | CONFIG_SCHED_CRITMONITOR_MAXTIME_THREAD | 线程连续运行超时阈值 |
 * | CONFIG_SCHED_CRITMONITOR_MAXTIME_WQUEUE | work_queue 回调函数执行超时 |
 * | CONFIG_SCHED_CRITMONITOR_MAXTIME_PREEMPTION | 从 sched_lock 到 sched_unlock 的间隔超时 |
 * | CONFIG_SCHED_CRITMONITOR_MAXTIME_CSECTION | 从 enter_critical_section 到 leave_critical_section 的间隔超时 |
 * | CONFIG_SCHED_CRITMONITOR_MAXTIME_BUSYWAIT | 持锁后的最长 Busy-Wait 等待时间 |
 * | CONFIG_SCHED_CRITMONITOR_MAXTIME_IRQ | IRQ 回调函数执行超时 |
 * | CONFIG_SCHED_CRITMONITOR_MAXTIME_WDOG | wd_start 回调函数执行超时 |
 *
 * 各阈值通常以 **时间长度（如微秒或毫秒）** 形式配置，
 * 超过阈值即视为异常执行。
 *
 * @section exec_time_trigger 触发与输出行为
 *
 * 当系统检测到某一执行路径运行时间超过配置的最大阈值时：
 *
 * - 不会立即中断系统运行
 * - 会通过 log 输出超时告警信息
 * - 日志中通常包含：
 *   - 超时类型（线程 / IRQ / work queue 等）
 *   - 执行实体（PID、线程名或回调函数）
 *   - 实际运行时间
 *   - 触发位置或调用者信息（如可获取）
 *
 * 该设计保证了：
 * - **低侵入性**：不影响系统正常运行
 * - **可持续监控**：适合长期运行场景
 *
 * @section exec_time_usage 使用场景
 *
 * 执行时间统计工具特别适用于以下问题定位场景：
 *
 * - 系统偶发卡顿、响应变慢但未崩溃
 * - Watchdog 复位前缺乏直接异常信息
 * - work_queue 回调设计不当导致系统阻塞
 * - 临界区或关调度范围过大，破坏实时性
 * - IRQ 或底层驱动执行时间异常增长
 *
 * 在性能调优、系统健康监控以及疑难问题排查阶段，
 * 该工具通常与：
 * - CPU Load 统计
 * - 临界区统计工具
 * - Crash Log / Backtrace
 *
 * 联合使用，可形成完整的行为分析闭环。
 */
