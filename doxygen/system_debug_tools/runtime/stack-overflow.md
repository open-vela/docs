/**
 * @defgroup runtime_stackcheck Runtime Stack Overflow Detection
 * @ingroup runtime_diagnosis
 * @brief 栈溢出与栈破坏检测机制
 *
 * 在嵌入式系统中，栈空间往往是最容易被忽视、却又最容易引发系统级异常的内存区域。
 * 一次看似轻微的越界写操作，可能不会立刻触发崩溃，而是以随机崩溃、不可复现异常、
 * 函数返回异常或调度混乱等形式，在系统后续运行过程中逐步显现。
 *
 * 栈溢出检测机制的核心目标并非在系统已经崩溃后还原现场，而是在栈结构被破坏或即将
 * 越界时，尽早发现异常并阻止问题进一步扩散。
 *
 * OpenVela 针对不同层级的栈使用场景，提供了多种互补的栈溢出检测方案，覆盖函数栈与
 * 线程栈两类对象，在性能开销、检测时效性与覆盖范围之间形成平衡。
 */

/**
 * @section stack_concepts Stack Concepts
 * @brief 函数栈与线程栈的区分
 *
 * 在理解栈溢出检测机制之前，需要区分两个在工程实践中经常被混用但语义并不相同的概念：
 * 函数栈（Function Stack）与线程栈（Thread Stack）。
 */

/**
 * @subsection function_stack Function Stack
 * @brief 函数栈（函数调用栈帧）
 *
 * 函数栈是指单次函数调用过程中使用的栈帧（Stack Frame）。每次函数调用时，
 * 编译器都会在当前线程栈上分配一个新的栈帧，用于保存：
 * - 返回地址
 * - 上一层栈帧指针
 * - 局部变量
 * - 寄存器保存区
 *
 * 当函数返回后，该栈帧随即被释放，栈指针恢复至调用前位置。
 *
 * 函数栈相关问题通常由以下因素引起：
 * - 过深的函数调用嵌套
 * - 递归失控
 * - 局部变量尺寸过大
 * - 非法指针写操作
 *
 * 此类问题的破坏范围通常局限于相邻栈帧，但一旦破坏返回地址等控制信息，
 * 往往会导致不可预测的执行结果。
 */

/**
 * @subsection thread_stack Thread Stack
 * @brief 线程栈（任务栈）
 *
 * 线程栈是在任务或线程创建时分配的一段连续、独立的内存区域。
 * 该线程内所有函数调用、异常处理以及上下文切换相关的数据，
 * 均在这块栈空间中完成。
 *
 * 线程栈在任务创建时一次性分配，其大小通常由系统配置决定，
 * 常见范围从 1KB 到数十 KB 不等。
 *
 * 当线程栈发生溢出时，栈指针（SP）将越过合法边界，破坏相邻内存区域，
 * 其影响范围更大，更容易引发系统级异常。
 */

/**
 * @section stack_methods Stack Check Mechanisms
 * @brief OpenVela 栈溢出检测机制概览
 *
 * 基于函数栈与线程栈在生命周期和破坏范围上的差异，
 * OpenVela 未采用单一栈保护方案，而是提供了多种互补的检测机制：
 *
 * - 基于编译器插桩的栈保护（Stack Canaries）
 * - 基于函数插桩的栈检查（Function Instrumentation）
 * - 基于栈顶标记的栈检查（Watermark）
 * - 基于硬件机制的栈边界保护（ARMv8-M MSP/PSPLIM）
 *
 * 这些机制适用于不同架构、不同调用深度以及不同调试阶段，
 * 可在系统发生严重异常之前提前暴露潜在风险。
 */

/**
 * @subsection stack_canary Stack Canaries
 * @brief 基于编译器插桩的栈保护
 *
 * @par 基本配置
 * @code
 * CONFIG_STACK_CANARIES=y
 * @endcode
 *
 * @par 工作原理
 * 编译器在函数栈帧中插入一个哨兵值（canary），通常位于局部变量与控制信息之间。
 * 在函数返回前，自动校验该值是否被篡改：
 * - 若值保持不变，函数正常返回
 * - 若值被覆盖，立即触发异常处理流程
 *
 * 任何越界写操作在覆盖返回地址之前，极有可能先破坏 canary，
 * 从而被及时检测。
 *
 * @par 性能开销
 * - 函数入口写入 canary
 * - 函数返回路径执行一次校验
 *
 * 该机制引入的额外指令和栈空间占用极小，对系统性能影响较低。
 *
 * @par 适用场景
 * - 高时效性、高精度
 * - 仅适用于函数栈
 * - 适合检测局部缓冲区越界、错误的 memcpy/memset 操作
 */

/**
 * @subsection stack_instrument Function Instrumentation Stack Check
 * @brief 基于函数插桩的栈检查
 *
 * @par 基本配置
 * @code
 * CONFIG_ARMV7M_STACKCHECK=y
 * CONFIG_ARMV8M_STACKCHECK=y
 * @endcode
 *
 * @par 工作原理
 * 编译器通过 -finstrument-functions 在函数入口插入检测逻辑，
 * 在函数执行期间检查当前栈指针（SP）是否仍处于合法范围内，
 * 从而更早发现异常增长或越界风险。
 *
 * @par 性能开销
 * 相较 Stack Canaries，该机制开销更高，主要来自：
 * - 函数入口处的额外检测指令
 * - 栈指针读取与边界比较
 * - 高频函数调用下的重复执行
 *
 * @par 适用场景
 * - 高时效性、高精度
 * - 仅适用于函数栈
 * - 适合捕获递归失控、调用深度异常增长等问题
 * - 仅支持 ARMv7-M / ARMv8-M 架构
 */

/**
 * @subsection stack_watermark Stack Watermark
 * @brief 基于栈顶标记的线程栈检查
 *
 * @par 基本配置
 * @code
 * CONFIG_STACKCHECK_MARGIN=16
 * @endcode
 *
 * @par 工作原理
 * 在线程创建或初始化时，对整段线程栈进行固定模式填充。
 * 在运行过程中，通过扫描栈区域中仍保持初始标记的部分，
 * 推算线程历史上的最大栈使用深度。
 *
 * 若标记被覆盖至接近栈边界，说明该线程存在明显的栈溢出风险。
 *
 * @par 性能开销
 * - 线程创建时的一次性初始化
 * - 检查阶段对栈区域的顺序扫描
 *
 * @par 适用场景
 * - 时效性较低
 * - 仅适用于线程栈
 * - 适合长期监控和评估线程栈大小配置是否合理
 */

/**
 * @subsection stack_hardware ARMv8-M Hardware Stack Check
 * @brief 基于硬件的栈边界保护（MSP/PSPLIM）
 *
 * @par 基本配置
 * @code
 * CONFIG_ARMV8M_STACKCHECK_HARDWARE=y
 * @endcode
 *
 * @par 工作原理
 * ARMv8-M 架构提供 MSPLIM 与 PSPLIM 寄存器用于定义主栈与进程栈的下界。
 * 当栈指针向低地址移动并越过配置的下界时，
 * 硬件会立即触发异常（UsageFault 或 HardFault）。
 *
 * 该检测完全由硬件完成，不依赖函数返回或软件插桩。
 *
 * @par 性能开销
 * - 几乎为零
 *
 * @par 适用场景
 * - 高时效性
 * - 适用于线程栈
 * - 仅支持具备 MSP/PSPLIM 的 ARMv8-M 平台
 */
