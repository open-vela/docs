/**
 * @page gdb_plugin GDB Plugin
 *
 * @brief OpenVela 在线调试扩展框架（GDB Plugin）
 *
 * GDB Plugin 是 OpenVela 在 NuttX 工程体系中构建的一套在线调试扩展框架。
 * 该框架通过 Python 脚本形式集成到 GDB 中，围绕线程调度、内存管理、
 * 文件系统、IPC、网络、蓝牙等核心子系统，提供高层、系统语义化的调试能力。
 *
 * 与原生 GDB 仅能操作寄存器、裸内存不同，GDB Plugin 直接以系统对象
 * （Task、Heap、Circbuf、uORB、RPMsg、Socket、FS Context 等）为调试单位，
 * 使开发者能够从“系统视角”而非“指令视角”定位问题。
 *
 * @section gdb_plugin_goals 设计目标
 *
 * GDB Plugin 主要解决以下三个核心问题：
 *
 * 1. 原生 GDB 无法理解 NuttX 运行结构  
 *    原生 GDB 只能看到线程 ID，无法解析 NuttX 中的 Task / Pthread / TCB
 *    结构，也无法感知线程真实状态、阻塞原因和调度语义。
 *
 *    GDB Plugin 通过解析内核数据结构，补齐调度层语义，使调试者能够
 *    “看到系统真正的运行状态”。
 *
 *    典型能力包括：
 *    - info nxthreads：查看完整线程列表、优先级、状态、PC、SP
 *    - nxthread <id>：恢复指定线程的寄存器上下文并切换调试视角
 *
 * 2. 原生 GDB 难以解析 NuttX 内存管理结构  
 *    NuttX 的 Heap、Pool、Uncache 等内存节点结构复杂，单纯查看裸内存
 *    难以判断内存使用状况或问题根因。
 *
 *    GDB Plugin 将内存问题从“不可见”转化为“可量化、可分析、可定位”：
 *    - heap / pool 节点解析
 *    - 内存碎片率统计
 *    - backtrace 分类统计
 *    - KASan 辅助定位越界访问
 *
 *    典型命令包括：
 *    memdump、memleak、memfind、memclassify、memfrag、kasan 等。
 *
 * 3. 复杂子系统缺乏统一调试入口  
 *    蓝牙、uORB、文件系统、RPMsg、网络等子系统原本各自分散，
 *    缺乏统一的调试工具入口。
 *
 *    GDB Plugin 将这些能力统一整合到 GDB 环境中，形成“一站式调试入口”：
 *    - uORB topic 状态查看（uorb）
 *    - RPMsg 端点与回调解析（rpmsgdump）
 *    - 文件系统树与缓存状态（fatfs / romfs / yaffs / lrofs）
 *    - 网络 socket / IOB 状态（netstats）
 *    - 蓝牙 IPC / adapter 状态（btsocket / btdev）
 *
 * @section gdb_plugin_scenarios 使用场景
 *
 * GDB Plugin 适用于所有可运行 GDB 的调试场景，包括：
 *
 * - 在线调试（J-Link / Trace32）  
 *   实时查看线程、堆、IPC 状态，适用于功能 Bring-up 和联调阶段。
 *
 * - GDB Stub 调试  
 *   通过串口或网络与目标交互，适用于设备无硬件调试口的场景。
 *
 * - Crash Log + Memory Dump 现场还原  
 *   分析崩溃前的栈、内存与线程状态。
 *
 * - CoreDump 离线调试  
 *   用于复现困难、现场不可再现的问题分析。
 *
 * @section gdb_plugin_commands 命令分类概览
 *
 * GDB Plugin 提供的命令按功能大致可分为以下几类：
 *
 * @subsection gdb_plugin_cmd_system 系统类（System）
 *
 * - list_check       ：检查 list_node / sq_queue_t / dq_queue_t 结构完整性
 * - foreach list     ：遍历 NuttX 内核中的各类链表
 * - tlsdump          ：dump 并校验 TLS（task-local storage）数据
 * - nxgcore          ：拉取设备 coredump（封装 gdb gcore）
 * - free             ：系统内存使用信息（与设备 free 行为一致）
 * - uname            ：查看固件版本信息
 * - irqinfo          ：查看 IRQ 统计信息
 * - dmesg            ：查看 ramlog（系统日志）
 * - resetcause       ：查看上次设备重启原因
 * - wdog             ：查看 watchdog 状态
 * - worker           ：查看 worker queue 状态
 * - note / notedump  ：查看 NoteRAM 中的系统打点数据
 * - note snapshot    ：抓取 crash 前的调度快照
 * - diagnose         ：一键执行诊断命令并生成 JSON 报告
 * - circbuf          ：查看 circle buffer 状态
 *
 * @subsection gdb_plugin_cmd_thread 线程与调度类（Thread / Scheduler）
 *
 * - info nxthreads   ：查看线程列表与调度状态（NuttX 专用）
 * - setregs          ：设置当前寄存器值，用于切换线程上下文
 * - deadlock         ：检测线程死锁
 * - critmon          ：查看临界区统计信息
 * - ps               ：查看 process / task 状态
 * - crash busyloop   ：检测 busy-loop 忙循环线程
 *
 * @subsection gdb_plugin_cmd_memory 内存类（Memory）
 *
 * - memdump          ：Dump 各类内存节点（heap / pool / uncache 等）
 * - memleak          ：内存泄漏分析
 * - memfind          ：内存模式搜索
 * - memclassify      ：内存分配分类统计
 * - memfrag          ：内存碎片分析
 * - kasan            ：KASan 辅助分析
 *
 * @section gdb_plugin_summary 小结
 *
 * GDB Plugin 将 GDB 从“底层调试工具”提升为“系统级诊断平台”，
 * 是 OpenVela 调试工具链中承上启下的关键组件：
 *
 * - 向下承接：CoreDump、Crash Log、Memory Dump 等现场保留机制
 * - 向上增强：以系统语义方式理解线程、内存与子系统状态
 *
 * 在复杂嵌入式系统中，GDB Plugin 极大降低了调试门槛，
 * 提升了问题定位效率，是在线调试与离线分析阶段的核心工具之一。
 */
