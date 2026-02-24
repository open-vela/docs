/**
 * @page sdt_critical_section_count 临界区统计工具（critmon）
 * @brief 监控并量化系统运行期间的“关中断临界区 / 关调度临界区”行为，定位异常长临界区导致的实时性风险。
 *
 * @section sdt_cs_overview 概述
 * 在实时操作系统中，临界区（Critical Section）通常通过两类方式实现：关闭中断（enter/leave critical section）与锁调度器（sched_lock/sched_unlock）。:contentReference[oaicite:0]{index=0}
 *
 * 临界区用于保护共享资源，但如果临界区过长或使用不当，会带来明显的系统风险：中断长时间被屏蔽导致外设响应延迟、任务调度被阻塞导致实时性下降、系统抖动增大甚至触发看门狗。:contentReference[oaicite:1]{index=1}
 *
 * 为此 OpenVela 提供 critmon 临界区统计工具，对系统运行期间的临界区行为进行监控和量化分析，核心目标是：
 * @b “系统被阻塞了多久”，而不是“阻塞发生了多少次”。:contentReference[oaicite:2]{index=2}
 *
 * @section sdt_cs_config 基本配置
 * 开启 critmon 需要启用内核监控、用户态命令与 procfs 支持，并分别打开“关中断/关调度”耗时统计：:contentReference[oaicite:3]{index=3}
 * @code{.cfg}
 * # 启用临界区和调度锁监控
 * CONFIG_SCHED_CRITMONITOR=y
 *
 * # 启用 critmon 用户空间命令行工具
 * CONFIG_SYSTEM_CRITMONITOR=y
 *
 * # 启用 procfs 文件系统支持
 * CONFIG_FS_PROCFS=y
 *
 * # 设置为 0 以开启临界区耗时统计，-1 为禁用统计
 * CONFIG_SCHED_CRITMONITOR_MAXTIME_CSECTION=0
 *
 * # 设置为 0 以开启调度锁耗时统计，-1 为禁用统计
 * CONFIG_SCHED_CRITMONITOR_MAXTIME_PREEMPTION=0
 * @endcode
 *
 * @section sdt_cs_principle 实现原理
 *
 * @subsection sdt_cs_principle_irq 关中断临界区统计原理
 * 系统中典型的关中断接口为：:contentReference[oaicite:4]{index=4}
 * @code{.c}
 * flags = enter_critical_section();
 * leave_critical_section(flags);
 * @endcode
 *
 * critmon 在这两个接口中插入监控逻辑：进入时记录时间戳并标记当前 CPU/thread 进入关中断状态；退出时再次读取时间戳并计算时间差，得到本次关中断持续时间；随后维护统计信息（更新该线程最大关中断时间 MAX，可选记录累计统计）。:contentReference[oaicite:5]{index=5} :contentReference[oaicite:6]{index=6}
 *
 * 该机制可以准确反映“系统最长一次关中断持续了多久”以及是否存在异常长时间关中断路径。:contentReference[oaicite:7]{index=7}
 *
 * @subsection sdt_cs_principle_sched 关调度临界区统计原理
 * 调度锁通常通过如下接口实现：:contentReference[oaicite:8]{index=8}
 * @code{.c}
 * sched_lock();
 * sched_unlock();
 * @endcode
 *
 * 统计逻辑与关中断类似：在 sched_lock() 记录起始时间，在 sched_unlock() 记录结束时间，计算时间差并更新最大关调度时间。:contentReference[oaicite:9]{index=9}
 *
 * @section sdt_cs_usage 使用方法
 * critmon 提供两类信息获取方式：命令行汇总输出，以及按 PID 读取 /proc 节点。:contentReference[oaicite:10]{index=10} :contentReference[oaicite:11]{index=11}
 *
 * @subsection sdt_cs_usage_app 方式一：Critmon App 命令行
 * critmon 提供一组命令来控制和显示统计信息：:contentReference[oaicite:12]{index=12}
 * - @b critmon：显示统计信息。与 irqinfo 类似，首次执行显示累计数据，后续执行显示增量数据；数据读取后自动清零。:contentReference[oaicite:13]{index=13}
 * - @b critmon_start：后台启动任务，按 CONFIG_SYSTEM_CRITMONITOR_INTERVAL（默认 2 秒）周期自动打印统计信息。:contentReference[oaicite:14]{index=14}
 * - @b critmon_stop：停止后台自动打印任务。:contentReference[oaicite:15]{index=15}
 *
 * @subsection sdt_cs_usage_output 输出字段说明
 * critmon 输出表头包含 PRE-EMPTION、CSECTION、RUN、TIME、PID、DESCRIPTION 等列，并给出对应 caller 地址：:contentReference[oaicite:16]{index=16}
 *
 * - @b PRE-EMPTION & CALLER：最长关调度时间（秒）及调用者地址，记录线程通过 sched_lock() 等函数禁用调度器的最长持续时间。:contentReference[oaicite:17]{index=17}
 * - @b CSECTION & CALLER：最长关中断时间（秒）及调用者地址，记录线程通过 enter_critical_section() 进入临界区的最长持续时间。:contentReference[oaicite:18]{index=18}
 * - @b RUN：单次最长运行时间（秒），线程在两次被抢占（preemption）之间连续运行的最长时间。:contentReference[oaicite:19]{index=19}
 * - @b TIME：总计运行时间（秒），线程在统计周期内获得 CPU 的总时间。:contentReference[oaicite:20]{index=20}
 * - @b PID：线程 ID。:contentReference[oaicite:21]{index=21}
 * - @b DESCRIPTION：线程名称。:contentReference[oaicite:22]{index=22}
 *
 * @subsection sdt_cs_usage_proc 方式二：按线程读取 /proc/<pid>/critmon
 * 可通过读取 /proc 文件系统中对应节点获取单个线程的监控数据，便于自动化测试脚本或精细化分析：:contentReference[oaicite:23]{index=23}
 * - 命令：@code{.bash} cat /proc/<pid>/critmon @endcode :contentReference[oaicite:24]{index=24}
 * - 功能：获取指定 PID 线程的单次最长运行时间和总运行时间。:contentReference[oaicite:25]{index=25}
 */
