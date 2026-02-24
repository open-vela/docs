/**
 * @page sdt_showinfo showinfo 工具（CPU/内存/文件系统信息监控）
 *
 * @brief showinfo 用于监控系统资源信息，主要包括 CPU、内存使用情况，并可按需查看指定文件系统的容量信息。:contentReference[oaicite:0]{index=0}
 *
 * @section sdt_showinfo_overview 概述
 * showinfo 是用来监控内存信息的工具，同时支持输出 CPU/内存统计，并可选查看文件系统空间信息与落盘保存。:contentReference[oaicite:1]{index=1}
 *
 * @section sdt_showinfo_config 基本配置
 * 启用 showinfo 相关能力的配置如下：:contentReference[oaicite:2]{index=2}
 * @code{.cfg}
 * # 启用
 * LOW_RESOURCE_TEST=y
 * @endcode
 *
 * @section sdt_showinfo_usage 使用方法
 * showinfo 命令行形式如下：:contentReference[oaicite:3]{index=3}
 * @code{.bash}
 * showinfo [-i <interval>] [-p <pid>] [-a] [-d <dir>] [-l <logpath>] [-k <logpath>]
 * @endcode
 *
 * @subsection sdt_showinfo_args 参数说明
 * - @b -i <interval> ：设置刷新间隔（秒），即多长时间打印一次结果，默认为 1s。:contentReference[oaicite:4]{index=4}
 * - @b -p <pid> ：设置需要查看的进程 PID；未设置时，只显示系统级信息。:contentReference[oaicite:5]{index=5}
 * - @b -a ：仅在设置了 @b -p 后有效；
 *   - 未设置 @b -a ：显示的进程 CPU/MEM 仅为该 PID 本身（不包含子线程/子任务）
 *   - 设置 @b -a ：显示该进程及其全部子线程（同一个 task group）的 CPU/MEM 总和。:contentReference[oaicite:6]{index=6}
 * - @b -d <dir> ：查看文件系统信息：
 *   - total size：文件系统总大小
 *   - free size：文件系统剩余大小（包括超级块、inode 块等）
 *   - avail size：用户可用大小（仅数据块）
 *   - block size：块大小。:contentReference[oaicite:7]{index=7}
 * - @b -l <logpath> ：将 CPU、内存结果输出到 logpath 指定文件。:contentReference[oaicite:8]{index=8}
 * - @b -k <logpath> ：将文件系统结果输出到 logpath 指定文件。:contentReference[oaicite:9]{index=9}
 *
 * @section sdt_showinfo_examples 使用示例
 * - 查看系统 CPU、内存（后台周期输出）：:contentReference[oaicite:10]{index=10}
 *   @code{.bash}
 *   showinfo -i 1 &
 *   @endcode
 *
 * - 查看 PID 为 1000 的进程资源：:contentReference[oaicite:11]{index=11}
 *   @code{.bash}
 *   showinfo -p 1000 &
 *   @endcode
 *
 * - 查看 /data 文件系统大小：:contentReference[oaicite:12]{index=12}
 *   @code{.bash}
 *   showinfo -d /data &
 *   @endcode
 *
 * @section sdt_showinfo_notes 注意事项
 * - 若希望统计“进程整体资源”（包含线程组），请在使用 @b -p 的同时开启 @b -a；否则仅统计单个 PID 本身。:contentReference[oaicite:13]{index=13}
 * - 使用 @b -l/@b -k 落盘时，建议将输出目录指向可写且空间充足的位置，以避免因日志增长导致存储压力。:contentReference[oaicite:14]{index=14}
 */
