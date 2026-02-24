/**
 * @file gdbserver.md
 * @brief Crash 现场还原 —— gdbserver 离线调试机制
 *
 * @section gdbserver_overview 概述
 *
 * gdbserver 是 OpenVela Crash 现场还原工具链中的分析执行层，
 * 基于 GDB Remote Serial Protocol（RSP），
 * 用于将设备侧采集的 Crash 现场数据（Coredump / Crash Log / Memory Dump）
 * 转换为可被 GDB 解析和交互的调试环境。
 *
 * 与在线调试不同，gdbserver 面向的是“已经停止运行的系统现场”，
 * 其核心目标是：
 *
 * - 将原始二进制现场数据转化为可视化、可交互的调试视图
 * - 在离线环境中重建接近实时调试的分析体验
 *
 * @section gdbserver_position 机制定位
 *
 * 在调试路径中，gdbserver 位于：
 *
 * - 运行时诊断（Runtime Diagnosis）之后
 * - 现场保留（Coredump / Crash Log）之后
 * - 深度还原（Root Cause Analysis）之前
 *
 * gdbserver 本身不负责采集现场，
 * 而是负责“解释和还原”已经采集的现场数据。
 *
 * @section gdbserver_corevalue 核心价值
 *
 * gdbserver 的核心价值体现在以下几个方面：
 *
 * - 地址 → 符号 → 源码行号的自动映射
 * - 调用栈（Backtrace）的自动重建
 * - 寄存器、内存、变量的交互式查询
 * - 多线程 / 多核现场的统一分析
 *
 * 它将不可读的二进制数据，转化为工程师可直接理解的系统语义视图。
 *
 * @section gdbserver_supported_input 支持的输入类型
 *
 * gdbserver 支持多种 Crash 现场输入形式，可单独或组合使用：
 *
 * - Coredump 文件（.core）
 * - Crash Log（日志形式保存的寄存器 / 栈 / PC / LR）
 * - 原始内存转储（Memory Dump）
 *
 * 不同输入类型对应不同的分析深度：
 *
 * - Crash Log：最轻量，适合快速定位调用链
 * - Memory Dump：用于补充特定内存区域
 * - Coredump：完整系统快照，分析能力最强
 *
 * @section gdbserver_basic_usage 基本用法
 *
 * gdbserver 提供统一的命令行入口：
 *
 * @code
 * usage: gdbserver.py [-h]
 *   -a {arm,arm-a,arm64,riscv,x86-64,esp32s3,xtensa}
 *   -e ELFFILE
 *   [-p PORT] [--proxy PROXY]
 *   [-r [RAWFILE ...]] [-c CORE]
 *   [--remap [REMAP ...]]
 *   [-l LOG] [-d]
 *   [-g GDB] [-i INIT_CMD]
 * @endcode
 *
 * gdbserver 本质上是一个基于 Crash 数据构建的 NuttX GDB Server（nxstub）。
 *
 * @section gdbserver_parameters 参数说明
 *
 * - @b -a, --arch  
 *   目标架构类型，必须指定，例如：arm、arm-a、arm64、riscv、xtensa。
 *
 * - @b -e, --elffile  
 *   对应设备运行版本的 ELF 文件（必须匹配）。
 *
 * - @b -p, --port  
 *   gdbserver 监听端口，默认 1234。
 *
 * - @b --proxy  
 *   GDB 代理转发（高级场景使用）。
 *
 * - @b -r, --rawfile  
 *   原始内存转储文件，格式为：
 *   @code
 *   mem.bin:0x20000000
 *   @endcode
 *
 * - @b -c, --core  
 *   Coredump 文件路径。
 *
 * - @b --remap  
 *   地址重映射配置，用于 AMP / 多核地址空间不一致场景。
 *
 * - @b -l, --log  
 *   Crash Log 文件路径。
 *
 * - @b -d, --debug  
 *   启用 gdbserver 自身调试日志。
 *
 * - @b -g, --gdb  
 *   指定 GDB 可执行文件路径，并自动拉起 GDB 会话。
 *
 * - @b -i, --init-cmd  
 *   GDB 启动后自动执行的初始化命令。
 *
 * @section gdbserver_usage_pattern 常见使用模式
 *
 * @subsection gdbserver_use_crashlog 基于 Crash Log
 *
 * @code
 * gdbserver.py -a arm -e Vela.elf -l crash.log
 * gdb-multiarch Vela.elf -ex "target remote localhost:1234"
 * @endcode
 *
 * 适合快速分析调用链、寄存器和基础栈信息。
 *
 * @subsection gdbserver_use_coredump 基于 Coredump
 *
 * @code
 * gdbserver.py -a arm -e Vela.elf -c coredump.core
 * gdb-multiarch Vela.elf -ex "target remote localhost:1234"
 * @endcode
 *
 * 提供最完整的系统现场分析能力。
 *
 * @subsection gdbserver_use_memdump 基于内存转储
 *
 * @code
 * gdbserver.py -a arm-a -e Vela.elf -r memdump.bin:0x40200000
 * @endcode
 *
 * 用于补充特定地址空间的数据。
 *
 * @section gdbserver_multicore 多核场景支持
 *
 * 在 AMP / SMP 系统中：
 *
 * - 单一 Coredump 可包含多个 CPU 的内存与寄存器信息
 * - gdbserver 可针对不同核加载不同 ELF
 * - 通过 remap 参数解决地址空间差异
 *
 * 示例：
 *
 * @code
 * gdbserver.py -a xtensa -e Vela_audio.elf -c coredump.core
 * @endcode
 *
 * @section gdbserver_analysis_capability 分析能力
 *
 * 通过 GDB 客户端，gdbserver 支持：
 *
 * - 查看调用栈（bt / bt full）
 * - 查看寄存器（info reg）
 * - 切换线程（info threads / thread <id>）
 * - 查看内存（x/<n>x <addr>）
 * - 查看变量与结构体（p <var>）
 *
 * 其分析体验接近于“对一个已冻结进程的在线调试”。
 *
 * @section gdbserver_relation 与其它工具的关系
 *
 * - gdbserver 是 Coredump / Crash Log 的解析执行层
 * - GDB Plugin 构建在 gdbserver 之上，提供系统语义级调试能力
 * - 二者共同构成 OpenVela 的离线调试闭环
 *
 * @section gdbserver_scenario 适用场景
 *
 * gdbserver 适用于以下典型问题：
 *
 * - 无法复现的 Crash
 * - 一次性 HardFault / Panic
 * - 内存破坏、竞态条件导致的异常
 * - 无法接入 J-Link / Trace32 的设备
 *
 * 在 Crash 现场还原阶段，gdbserver 是将“数据”转化为“结论”的关键工具。
 */
