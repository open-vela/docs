/**
 * @file memory-trampling.md
 * @page runtime_mem_trampling 内存越界检测（KASan / ASan）
 * @ingroup system_debug_tools_runtime
 *
 * @brief 运行时内存访问越界检测机制，用于在程序执行过程中“即时发现”越界读写、UAF 等内存错误，尽可能在内存被进一步破坏之前暴露根因。
 *
 * @tableofcontents
 *
 * @section mem_trampling_overview 1. 概述
 * 内存访问越界是嵌入式系统中最隐蔽、最难复现、也最容易导致系统崩溃的问题之一。它往往不会在越界发生的瞬间触发崩溃，
 * 而是以“静默破坏”的形式污染其他任务或关键结构体，最终表现为随机 HardFault、结构体字段异常、链表断裂等难定位现象。
 *
 * 因此，在调试阶段启用运行时内存越界检测工具（KASan/ASan 系列）具有极高价值：强调“即时发现”，力求在错误首次发生时直接暴露问题根因。
 *
 * OpenVela 提供：
 * - 三类内核态 KASan 实现：Generic / SoftTag / MTE（Hardware Tagged）
 * - 一类仅用于模拟器环境的 ASan（Host-Side）
 *
 * @section mem_trampling_matrix 2. 能力范围对比（错误类型 / 精度 / 适用范围）
 * 为帮助理解各机制的覆盖能力，下表总结了四种方案能够检测的错误类型与适用范围：
 *
 * @code{.text}
 * 错误类型 / 特性                 | Generic KASAN | SoftTag KASAN | MTE KASAN | ASAN（SIM Host）
 * -------------------------------|--------------|---------------|----------|-----------------
 * 堆越界写（Heap OOB Write）      |      ✓       |       ✓       |    ✓     |        ✓
 * 堆越界读（Heap OOB Read）       |      ✓       |       ✓       |    ✓     |        ✓
 * Use-After-Free（UAF）           |      ✓       |       ✓       |    ✓     |        ✓
 * Double Free / Invalid Free      |      ✓       |       ✓       |    ✓     |        ✓
 * 全局变量越界                    |      ✓       |       ✓       |    ✗     |        ✓
 * 栈变量越界                      |      ✗       |       ✗       |    ✗     |        ✓
 * 野指针/未初始化指针访问          | ✗（部分可检） |       ✓       |    ✓     |        ✓
 *
 * 检测粒度/精度                   | 4B(32位) / 8B(64位) | 4B(32位) / 8B(64位) | 16B | 16B 对齐
 * 适用范围                        | 通用          | 仅 ARM64（TBI） | 仅 ARM64 + MTE | 仅 SIM 模拟器
 * @endcode
 *
 * @section mem_trampling_generic 3.2.1 Generic KASan（最通用实现）
 * @subsection mem_trampling_generic_cfg 基本配置
 * @code{.cfg}
 * CONFIG_MM_KASAN_GENERIC=y
 * # 开启全局插桩
 * CONFIG_MM_KASAN_INSTRUMENT_ALL=y
 * @endcode
 *
 * @subsection mem_trampling_generic_principle 实现原理
 * Generic KASan 是最通用、覆盖范围最广的内存访问越界检测方案。它通过编译器插桩，在每一次内存访问发生之前对访问地址进行合法性校验，
 * 从而在内存被破坏的第一时间捕获非法访问行为。该方案不依赖指针标签或硬件支持，而是通过独立维护的 Shadow Memory（影子内存）记录真实内存的访问权限状态。
 *
 * @par i) 编译器插桩（-fsanitize=kernel-address）
 * 开启 `-fsanitize=kernel-address` 后，编译器会在每一次内存访问操作前插入检查调用。
 * 例如，读写指针不会直接执行，而会被重写为类似：
 * @code{.c}
 * _asan_load1_noabort(addr);
 * @endcode
 * 检查函数通常会：
 * - 查询目标地址对应的 Shadow 条目（Shadow Value）
 * - 判定该地址是否位于合法访问区域
 * - 若 Shadow 标记为 “poisoned”，则报告为越界访问
 *
 * @par ii) Shadow Memory（影子内存映射）
 * Shadow Memory 可理解为“主内存访问权限地图”：
 * - 通常 1 字节 Shadow 对应 8 字节真实内存（粒度因此常为 8B/64位 或 4B/32位）
 * - 插桩检查通过查询 Shadow 状态判断访问是否允许
 *
 * @par iii) Redzone Poisoning（红区标记）
 * 在 malloc/free 等分配释放路径中，KASan 会在堆块前后插入不可访问区（Redzone），并在 Shadow 中标记为 poisoned：
 * - 用户缓冲区外的任意访问都会命中红区
 * - 越界读写将立即触发 KASan 报错
 * - 可捕获大多数堆溢出问题
 *
 * @par 报错示例（信息含义）
 * 典型日志形态可能类似：
 * @code{.text}
 * kasan_report: kasan detected a read access error, address at 0xXXXXXXXX, size is 4, return address: 0xYYYYYYYY
 * @endcode
 * 表示在执行返回地址 0xYYYYYYYY 对应代码时，读取了一个非法/未分配的地址 0xXXXXXXXX。
 *
 * @section mem_trampling_softtag 3.2.2 SoftTag KASan（ARM64 软件指针标记模式）
 * @subsection mem_trampling_softtag_cfg 基本配置
 * @code{.cfg}
 * CONFIG_MM_KASAN_SW_TAGS=y
 * # 开启全局插桩
 * CONFIG_MM_KASAN_INSTRUMENT_ALL=y
 * @endcode
 *
 * @subsection mem_trampling_softtag_principle 实现原理
 * SoftTag KASan 是 KASan 在 ARM64 平台上的一种优化实现。
 * 与 Generic KASan 使用 Shadow Memory 记录“访问权限”不同，SoftTag 通过 “指针 Tag” 与 “内存 Tag” 的匹配关系来判断访问是否合法，
 * 依赖 ARM64 的 Top-Byte-Ignore（TBI）能力，将 Tag 放入指针的高 8 位。
 *
 * @subsection mem_trampling_softtag_vs_generic SoftTag 与 Generic 的关键差异
 * @par ① 技术基础不同
 * - Generic：依赖 Shadow Memory（权限地图）
 * - SoftTag：依赖 ARM64 TBI（指针高字节 Tag）
 *
 * @par ② 检测机制不同
 * - Generic：访问前查询 Shadow bit/byte 是否 poisoned
 * - SoftTag：为每个分配块生成 Tag，同时写入：
 *   - Pointer Tag（指针高 8 位）
 *   - Memory Tag（对应的影子 Tag 区域）
 *   访问时插桩逻辑比较 Pointer Tag 与 Memory Tag，一致则合法，不一致则非法
 *
 * @par ③ Redzone 处理方式不同
 * - Generic：依赖 Redzone + Shadow Poisoning
 * - SoftTag：不依赖 Redzone，主要通过 Tag 不匹配捕获越界
 *
 * @par ④ 限制
 * - 仅适用于 ARM64 架构（TBI）
 *
 * @section mem_trampling_mte 3.2.3 Hardware Tagged KASan（ARMv8.5 MTE 硬件模式）
 * @subsection mem_trampling_mte_cfg 基本配置
 * @code{.cfg}
 * CONFIG_MM_KASAN_HW_TAGS=y
 * @endcode
 *
 * @subsection mem_trampling_mte_principle 实现原理
 * MTE KASan 同样基于 “Tag 匹配” 思想，但与 SoftTag 的“软件维护 + 插桩比对”不同，它依赖 ARMv8.5 MTE 硬件能力：
 * - Pointer Tag：仍存于指针高 8 位
 * - Memory Tag：由硬件 Tag 存储单元维护
 *
 * 在实际访存路径上，每一条 load/store 指令都会由硬件自动完成 Pointer Tag 与 Memory Tag 的匹配；
 * 一旦校验失败，直接触发异常。该机制不依赖软件维护影子结构，也不依赖编译器是否插桩。
 *
 * @subsection mem_trampling_mte_vs_softtag SoftTag 与 MTE 的差异要点
 * - Tag 存储位置：
 *   - SoftTag：Memory Tag 由软件维护在影子 Tag 区域
 *   - MTE：Memory Tag 由硬件维护
 * - 检测触发位置：
 *   - SoftTag：依赖插桩代码显式读取并比较 Tag（覆盖范围受插桩影响）
 *   - MTE：硬件访存路径自动校验（覆盖所有真实读写：C/汇编/未插桩库）
 * - 性能影响：
 *   - SoftTag：额外插桩指令 + 影子 Tag 访问与软件比较，开销较高，偏调试/验证
 *   - MTE：访存指令本身几乎不增加额外指令，最接近“常态运行”，但前提是硬件平台具备 MTE 支持
 *
 * @section mem_trampling_asan 3.2.4 ASan（仅 SIM：Host-Side）
 * @subsection mem_trampling_asan_cfg 基本配置
 * @code{.cfg}
 * CONFIG_SIM_ASAN=y
 * @endcode
 *
 * @subsection mem_trampling_asan_notes 说明
 * 在 OpenVela 中，CONFIG_SIM_ASAN 用于在 SIM 模拟环境下启用主机侧 ASan 检测，
 * 作用是辅助开发者在仿真环境中提前发现内存越界问题。
 * 由于 ASan 检测逻辑运行在 Host（主机）侧，并不参与 OpenVela 内核的运行时机制，
 * 因此它不属于“真实硬件上的内核内存访问越界检查能力”。
 * 若目标是在真实硬件上运行的越界检测，请使用 KASan 系列（Generic / SoftTag / MTE）。
 *
 * @section mem_trampling_reco 4. 实践建议（怎么选）
 * - 通用平台、优先覆盖面：@b Generic KASan
 * - ARM64 且希望降低 Shadow 维护成本：@b SoftTag KASan（但仍依赖插桩）
 * - ARM64 且硬件支持 MTE、希望接近常态运行：@b MTE KASan
 * - 仅在 SIM 仿真阶段提前暴露问题：@b Host-Side ASan
 *
 */
