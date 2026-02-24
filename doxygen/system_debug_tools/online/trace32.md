/**
@page system_debug_tools_trace32 TRACE32 调测能力（TERM / FDX Syslog / FDX Trace）
@brief 基于 TRACE32 的调测能力集合：NSH 终端重定向、FDX Syslog 抓取、FDX Trace 抓取与解析。

@section trace32_overview 概述
TRACE32 在 OpenVela/NuttX 场景下主要承担三类能力：
- TRACE32 TERM：将 NuttX Shell 控制台重定向到 TRACE32 终端窗口，不依赖 UART/独立串口控制台即可交互。:contentReference[oaicite:3]{index=3}
- TRACE32 FDX Syslog：通过 FDX 通道将 syslog 直接输出到 TRACE32，由 TRACE32 保存为二进制日志文件。:contentReference[oaicite:4]{index=4}
- TRACE32 FDX Trace：通过 FDX 通道抓取 note trace 数据生成 trace.bin，并在主机侧解析为 Perfetto 可视化格式。:contentReference[oaicite:5]{index=5} :contentReference[oaicite:6]{index=6}

@note 三类能力都要求 TRACE32 侧已加载 ELF/符号表，并能 attach 到目标系统（JTAG/SWD）。

@section trace32_term TRACE32 TERM（NSH 终端）
@subsection trace32_term_cfg 配置说明（NuttX）
启用 TRACE32 TERM 的典型配置如下：:contentReference[oaicite:7]{index=7}
- 禁用其他串口作为系统控制台：
  - CONFIG_OTHER_SERIAL_CONSOLE=n
- 启用 TRACE32 Term 终端：
  - CONFIG_SERIAL_T32TERM=y
- 设置 TERM 内部缓存区大小（通信缓冲）：
  - CONFIG_TRACE32_TERM_MEMORY_BLOCKED_SIZE=4096
- 将 TRACE32 Term 作为系统 Shell 控制台：
  - CONFIG_SERIAL_T32TERM_CONSOLE=y

@subsection trace32_term_script 脚本机制与示例（TRACE32）
TRACE32 侧通过执行 `nuttx/drivers/trace32/t32term.cmm` 建立终端通信通道。脚本的核心动作包括：:contentReference[oaicite:8]{index=8}
1) 初始化共享内存（Tar2Host / Host2Tar）并清零缓冲区。:contentReference[oaicite:9]{index=9}  
2) 使用 `TERM.METHOD Buffer` 读写缓冲区内容，并通过 `TERM.GATE` 激活虚拟终端。:contentReference[oaicite:10]{index=10}  

下面给出一个“CONFIG_TRACE32_TERM_MEMORY_BLOCKED_SIZE=4096”时的示例脚本骨架（按文档示例补全为可直接落地版本）：:contentReference[oaicite:11]{index=11}

@code{.cmm}
; t32term.cmm (example)
SYStem.JtagClock 50.0MHz

; Clear shared buffers (Tar2Host / Host2Tar)
Var.Assign T32_Term_Memory_Tar2HostBuffer[0..3] = 0
Var.Assign T32_Term_Memory_Host2TarBuffer[0..3] = 0

WinCLEAR
TERM.RESet

; Use Buffer method to bind shared memory as terminal RX/TX
; Note: 4096-0x1 comes from CONFIG_TRACE32_TERM_MEMORY_BLOCKED_SIZE=4096
TERM.METHOD Buffer                                              \
    E:Var.VALUE(&T32_Term_Memory_Tar2HostBuffer[0])++(4096-0x1)  \
    E:Var.VALUE(&T32_Term_Memory_Host2TarBuffer[0])++(4096-0x1)

TERM.GATE

; Keep terminal alive
DO
    Go.direct
ENDDO
@endcode

@par 使用示例
在 TRACE32 的 NSH 控制台输入 `hello`，即可通过 TRACE32 终端触发设备侧命令执行并观察输出。:contentReference[oaicite:12]{index=12}

@section trace32_fdx_syslog TRACE32 FDX Syslog（高效日志抓取）
@subsection trace32_syslog_cfg 配置说明（NuttX）
启用 FDX Syslog 通道的关键配置：:contentReference[oaicite:13]{index=13}
- CONFIG_SYSLOG_DEFAULT=n
- CONFIG_SYSLOG_FDX=y

@subsection trace32_syslog_script TRACE32 侧脚本与流程
OpenVela 提供 FDX Syslog 示例脚本：`nuttx/drivers/trace32/t32fdx_syslog.cmm`。脚本流程包含：:contentReference[oaicite:14]{index=14}
- 检查 ELF 是否加载（否则无法解析 g_fdx_syslog_channel 等符号）
- `System.Attach` 连接目标，必要时 `Go` 拉起运行
- 配置 FDX 通道（Outchannel / Address / FIFO / Clear）
- `Fdx.Write` 将二进制日志保存到本地文件（如 syslog.bin）:contentReference[oaicite:15]{index=15}

下面按文档示例补全成可直接使用的脚本内容：:contentReference[oaicite:16]{index=16}

@code{.cmm}
; t32fdx_syslog.cmm (example)
If !Symbol.Exist("g_fdx_syslog_channel")
(
    Printf "ERROR: No ELF file loaded! Please load ELF file."
    Enddo
)

System.Attach
If !State.Run()
(
    Go
)

System.JtagClock 100MHZ

Fdx.Outchannel g_fdx_syslog_channel
Fdx.Address    g_fdx_syslog_channel

; Reset channel and clear history data
Fdx.DisableChannel g_fdx_syslog_channel
Fdx.Clear
Fdx.Mode FIFO

; Discard stale data
Wait 10ms

Printf "FDX record start."
Fdx.Write g_fdx_syslog_channel syslog.bin
@endcode

@note 文档中说明 syslog.bin 为二进制日志流，可通过 bin2txt 脚本转换为可读文本。:contentReference[oaicite:17]{index=17}

@section trace32_fdx_trace TRACE32 FDX Trace（note trace 抓取与解析）
@subsection trace32_trace_cfg 配置说明（NuttX）
以 TRACE32 FDX 抓取 trace 为例，关键配置包括：:contentReference[oaicite:18]{index=18}
- CONFIG_TRACE32_FDX_NOTE=y
- CONFIG_TRACE32_FDX_NOTE_FILTER_DEFAULT_MODE=0
- TRACE32_FDX_NOTE_BUFSIZE=16384
- CONFIG_DRIVERS_NOTE_CPUID=0（AMP 多核场景下用于区分 CPU ID）

@subsection trace32_trace_script TRACE32 侧脚本（生成 trace.bin）
脚本的关键点是配置 `g_fdx_note_channel` 并将 FDX 数据保存为 `trace.bin`：:contentReference[oaicite:19]{index=19}

@code{.cmm}
; t32fdx_note_trace.cmm (example)
If !Symbol.Exist("g_fdx_note_channel")
(
    Printf "ERROR: No ELF file loaded! Please load ELF file."
    Enddo
)

System.Attach

; Check if the system is running, if not, execute Go
If !State.Run()
(
    Go
)

; Set the JTAG clock to 100MHz, transfer rate is related to clock frequency
System.JtagClock 100MHZ

Fdx.Outchannel    g_fdx_note_channel
Fdx.Address       g_fdx_note_channel
Fdx.DisableChannel g_fdx_note_channel
Fdx.Clear
Fdx.Mode FIFO
Fdx.EnableChannel

; Wait for a while and discard the old data in the fdx buffer
Wait 10ms

Printf "FDX record start..."
; Write the trace data to trace.bin
Fdx.Write g_fdx_note_channel trace.bin
@endcode

@par 生成物
执行完成后会在 TRACE32 当前工作目录（cwd）下生成 `trace.bin`。:contentReference[oaicite:20]{index=20}

@subsection trace32_trace_parse 主机侧解析为 Perfetto
将 `trace.bin` 复制到代码根目录后，使用 traceparse 解析为 Perfetto 文件：:contentReference[oaicite:21]{index=21}

@code{.bash}
sh nuttx/tools/pynuttx/traceparse.py -e ./nuttx.elf -b trace.bin -o trace.perfetto
@endcode

生成的 `trace.perfetto` 可在 Perfetto 页面直接打开查看。:contentReference[oaicite:22]{index=22}

@section trace32_notes 注意事项
- TERM/FDX 脚本都依赖 TRACE32 已加载 ELF/符号；缺失符号会导致脚本无法解析通道地址（如 g_fdx_syslog_channel / g_fdx_note_channel）。:contentReference[oaicite:23]{index=23} :contentReference[oaicite:24]{index=24}
- `System.JtagClock` 影响传输效率；FDX Trace/Syslog 示例脚本中使用 100MHz。:contentReference[oaicite:25]{index=25} :contentReference[oaicite:26]{index=26}
*/
