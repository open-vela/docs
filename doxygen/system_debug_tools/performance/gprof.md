@page system_debug_tools_performance_gprof gprof（函数级性能分析工具）
@ingroup system_debug_tools_performance
@brief 通过编译期插桩统计“热点函数 + 调用关系”，辅助确定优化优先级。

@tableofcontents

@section gprof_overview 1. 工具定位与适用场景
gprof 是一种**函数级**性能分析工具：在程序运行过程中收集函数执行相关统计信息，并在结束后生成报告，用于定位性能热点与分析函数调用关系。:contentReference[oaicite:0]{index=0}

与其它性能分析工具的关注点不同：  
- Trace / SystemView 更偏“时间轴与行为”（什么时候发生了什么调度/事件）:contentReference[oaicite:1]{index=1}  
- perf 更偏“CPU 时间消耗在哪些函数”（基于 PMU 采样）:contentReference[oaicite:2]{index=2}  
- gprof 更偏“程序主要停留在哪些函数上，以及函数之间如何调用”:contentReference[oaicite:3]{index=3}  

因此，gprof 更适合：  
- 定位**函数级热点**  
- 判断**哪些函数值得优先优化**:contentReference[oaicite:4]{index=4}


@section gprof_config 2. 基本配置
以下为文档中给出的关键配置项：:contentReference[oaicite:5]{index=5}

@subsection gprof_config_kconfig 2.1 Kconfig 选项
@code
# 开启 gprof 命令（必选）
CONFIG_SYSTEM_GPROF=y

# 设备侧使用：开启采样所需的 -pg 插桩（必选）
CONFIG_PROFILE_MINI=y

# 全局默认开启 -pg，采样数据包含函数调用次数和函数调用关系（可选）
CONFIG_PROFILE_ALL=y

# SIM 环境下使用 gprof（按需）
CONFIG_SIM_GPROF=y
@endcode

@note
- 如果只需要“热点函数大致分布”，可先启用最小必选项；若需要更完整的调用关系分析，再开启 CONFIG_PROFILE_ALL。:contentReference[oaicite:6]{index=6}


@section gprof_principle 3. 工作原理
gprof 的核心机制基于**编译期插桩（Instrumentation）**，而不是硬件 PMU 或内核事件，因此具有较好的平台通用性。:contentReference[oaicite:7]{index=7}

在编译阶段启用 `-pg` 后，编译器会在**每个函数入口处**自动插入调用逻辑：:contentReference[oaicite:8]{index=8}  
- 记录当前函数的调用次数  
- 记录函数之间的调用关系（caller/callee）  
从而在运行过程中构建完整的 Call Graph，并统计调用频率。:contentReference[oaicite:9]{index=9}

@warning
插桩会引入额外开销（指令与数据记录），建议用于性能定位/验证阶段；不要在对性能极敏感的“最终发布配置”中默认长期开启（属于工程建议）。


@section gprof_usage 4. 使用方式（设备侧）
文档给出了一套典型流程（以 Arm32 QEMU 平台示例）：:contentReference[oaicite:10]{index=10}

@subsection gprof_usage_cmd 4.1 采集命令
@code
# 开始采集
nsh> gprof start

# 停止采集
nsh> gprof stop

# 导出采集数据（生成 gmon.out）
nsh> gprof dump /tmp/gmon.out
@endcode
导出后会生成 `gmon.out` 文件用于 Host 端分析。:contentReference[oaicite:11]{index=11}


@section gprof_analysis 5. 结果分析（Host 侧）
将设备侧生成的 `gmon.out` 拉取到 Host 端后，使用交叉工具链中的 `gprof` 工具分析：:contentReference[oaicite:12]{index=12}

@subsection gprof_analysis_cmd 5.1 分析命令
@code
arm-none-eabi-gprof nuttx.elf gmon.out -b
@endcode
:contentReference[oaicite:13]{index=13}

@subsection gprof_analysis_output 5.2 输出解读要点
gprof 常见输出包括两部分：  

- **Flat profile**：展示各函数的采样占比、累计耗时、调用次数等（用于快速锁定热点函数）。:contentReference[oaicite:14]{index=14}  
- **Call graph**：展示函数间调用关系与链路上的自耗时/子耗时（用于分析“热点从哪里来”“被谁调用导致的放大效应”）。:contentReference[oaicite:15]{index=15}  

@note
进行 Host 侧分析时，请确保：
- 使用与目标固件匹配的 `nuttx.elf`（符号要一致，否则符号解析会偏差）。（工程建议）
- 如果需要可读性更强的报告，可结合 gprof 的更多参数进一步过滤/排序。（工程建议）
