@page system_debug_tools_performance_perf perf（函数级 CPU 热点分析工具）
@ingroup system_debug_tools_performance
@brief 基于 PMU（Performance Monitoring Unit）与内核性能事件的采样分析工具，用于回答“CPU 时间究竟消耗在了哪些函数上”。

@tableofcontents

@section perf_overview 1. 工具定位与适用场景
在性能问题分析中：
- Trace / SystemView 更关注调度行为、任务切换关系以及系统运行时间轴；
- perf 则聚焦于另一类问题：CPU 时间究竟消耗在了哪些函数上？ :contentReference[oaicite:0]{index=0}

perf 属于**基于 PMU 和内核性能事件**的采样分析工具，常用于：热点函数分析、指令与缓存行为统计、调用栈（Callchain）与火焰图分析。:contentReference[oaicite:1]{index=1}  
它不关心“任务何时被切换”，而是回答：哪些函数真正“吃 CPU”、哪段代码是瓶颈、某次优化是否带来实际提升。:contentReference[oaicite:2]{index=2}

@section perf_config 2. 基本配置
启用 perf 工具需要以下配置：:contentReference[oaicite:3]{index=3}
@code
CONFIG_SCHED_PERF_EVENTS=y
CONFIG_PERF_TOOLS=y
CONFIG_SCHED_HAVE_PARENT=y
CONFIG_LIBC_EXECFUNCS=y
@endcode

@section perf_principle 3. 工作原理
@subsection perf_principle_sampling 3.1 核心思想：采样（Sampling）
perf 的核心思想是采样：通过 PMU 或内核计数器，以固定周期（如 CPU cycles 或时间间隔）中断当前执行流，记录当时正在执行的指令/函数/调用栈。大量采样后，统计结果即可近似反映程序在各函数中消耗 CPU 时间的比例。:contentReference[oaicite:4]{index=4}

@subsection perf_principle_modes 3.2 两种主要工作模式
- @b 事件统计（perf stat）：不做采样，直接统计 PMU 事件总量，用于整体性能特征评估（例如 cycles、instructions、cache-misses、branch-misses）。:contentReference[oaicite:5]{index=5}
- @b 性能采样（perf record）：周期性采样 CPU 执行状态，保存为 perf.data，用于热点函数/调用栈分析。:contentReference[oaicite:6]{index=6} :contentReference[oaicite:7]{index=7}

@section perf_usage 4. 使用方法（设备侧）
@section perf_usage_stat 4.1 perf stat：性能事件统计
查看当前系统支持的 PMU 事件：:contentReference[oaicite:8]{index=8}
@code
nsh> perf list -h
@endcode

常见事件包括 cycles / instructions / cache-references / cache-misses / branches / branch-misses。:contentReference[oaicite:9]{index=9}

示例：统计指定 CPU Core 的事件（以 Core 0、持续 20 秒为例）：:contentReference[oaicite:10]{index=10}
@code
nsh> perf stat -C 0 sleep 20
@endcode

@section perf_usage_record 4.2 perf record：采集热点函数
perf record 用于对 CPU 执行进行采样，并生成热点分析数据。设备端采集示例（在 /tmp 目录下运行 CoreMark）：:contentReference[oaicite:11]{index=11}
@code
goldfish-armv8a-ap> cd /tmp
goldfish-armv8a-ap> perf record /bin/coremark
@endcode

采样结束后生成：`/tmp/perf.data`。:contentReference[oaicite:12]{index=12}  
当前设备端不支持直接运行 `perf report`，需要将数据导出到 Host 端分析。:contentReference[oaicite:13]{index=13}

@section perf_host_analysis 5. Host 端解析 perf.data（热点函数）
@subsection perf_host_pull 5.1 拉取 perf.data
@code
adb pull /tmp/perf.data
@endcode
:contentReference[oaicite:14]{index=14}

@subsection perf_host_mmap 5.2 补充 mmap 映射信息
需要补充可执行文件与符号映射信息，否则 perf report 无法正确解析符号：:contentReference[oaicite:15]{index=15}
@code
./tools/perfaddmmap.py -e nuttx
@endcode
:contentReference[oaicite:16]{index=16}

@subsection perf_host_report 5.3 查看热点函数
@code
@mi:~/OpenVela/nuttx$ perf report
@endcode
示例输出中可直接看到各函数的 CPU 占用比例与热点函数列表。:contentReference[oaicite:17]{index=17}

@section perf_flamegraph 6. 调用栈与火焰图分析（perf record -g）
火焰图用于展示“调用栈与函数 CPU 占比关系”：纵轴为调用栈深度，横轴为采样次数（≈ CPU 时间占比），函数块越宽表示消耗 CPU 时间越多。:contentReference[oaicite:18]{index=18}

@subsection perf_flamegraph_record 6.1 采集调用栈数据（设备侧）
使用 `-g` 采集调用栈：:contentReference[oaicite:19]{index=19}
@code
goldfish-armv8a-ap> perf record -g /bin/coremark
@endcode

@subsection perf_flamegraph_gen 6.2 Host 端生成火焰图
下载 FlameGraph 工具，并按如下流程生成火焰图（核心步骤为 perf script + stackcollapse + flamegraph）：:contentReference[oaicite:20]{index=20}
@code
git clone https://github.com/brendangregg/FlameGraph.git

# 从设备侧拉取 perf.data，并补充 mmap 信息
@mi:~/OpenVela/nuttx$ adb pull /tmp/perf.data
@mi:~/OpenVela/nuttx$ ./tools/perfaddmmap.py -e nuttx

# 生成火焰图输入与输出
@mi:~/OpenVela/nuttx$ perf script > data.txt
@mi:~/OpenVela/nuttx$ ~/work/code/FlameGraph/stackcollapse-perf.pl data.txt > data.flode
@mi:~/OpenVela/nuttx$ ~/work/code/FlameGraph/flamegraph.pl data.flode > data.svg
@endcode

@section perf_notes 7. 注意事项
- 当前设备端不支持直接运行 `perf report`，请按“导出到 Host + perfaddmmap.py + perf report”的流程分析符号与热点。:contentReference[oaicite:21]{index=21} :contentReference[oaicite:22]{index=22}
