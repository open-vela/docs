/**
 * @file irq-count.md
 * @brief 中断频率统计工具（irqinfo）
 * @details
 * OpenVela 提供 `irqinfo` 中断频率统计工具，用于在系统运行过程中：
 * - 统计各个中断的触发次数（COUNT）
 * - 计算中断触发频率（RATE, Hz）
 * - 记录单次中断最大执行时间（TIME, µs）
 *
 * 该工具适合用来快速识别：
 * - 是否存在“中断风暴”（某个 IRQ 频率异常高）
 * - 是否存在“超长中断”（单次执行时间异常长，影响实时性/调度）
 *
 * @section irqinfo_config 基本配置
 * 启用 IRQ 监控与统计功能：
 * @code
 * # 启用 IRQ 监控与统计功能
 * CONFIG_SCHED_IRQMONITOR=y
 *
 * # 用于通过 /proc 暴露统计数据接口
 * CONFIG_FS_PROCFS=y
 * @endcode
 *
 * `irqinfo` 依赖 procfs，系统启动后需挂载：
 * @code
 * mount -t procfs /proc
 * @endcode
 *
 * @section irqinfo_principle 工作原理
 * - 统计窗口：默认从系统启动开始计时；读取一次统计信息后会清空并重新开始计时，后续输出为“增量窗口”统计。
 * - 次数统计：每次中断触发时，对该 IRQ 的计数器累加。
 * - 频率计算：对统计窗口内的触发次数除以窗口时长，得到 RATE（Hz）。
 * - 耗时统计：在中断入口/出口记录时间戳，计算本次中断执行时间，并维护该 IRQ 的“单次最大执行时间（MAX）”。
 *
 * @section irqinfo_usage 使用方法
 * 系统启动后，在 shell 中执行：
 * @code
 * ap> irqinfo
 * @endcode
 *
 * - 第一次执行：统计区间为「系统启动 → 当前时刻」。
 * - 第二次及后续执行：统计区间为「上一次执行 irqinfo → 当前时刻」（读完清空，重新计时）。
 *
 * @section irqinfo_output 输出格式与字段说明
 * 示例输出：
 * @code
 * IRQ HANDLER   ARGUMENT   COUNT   RATE    TIME
 * 11  2c604591  00000000   233     0.000   12
 * 39  0005753d  2c786451   18      2.395   83
 * 43  0005753d  00057455   759     0.000   143
 * @endcode
 *
 * 字段含义：
 * - IRQ：中断号
 * - HANDLER：中断处理函数地址
 * - ARGUMENT：中断参数
 * - COUNT：统计窗口内触发次数
 * - RATE：统计窗口内触发频率（Hz）
 * - TIME：单次中断最大执行时间（µs）
 */
