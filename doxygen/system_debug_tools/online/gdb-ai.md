/**
 * @defgroup gdb_ai_agent GDB AI Agent
 * @ingroup online_debug_tools
 * @brief 基于 GDB 的 AI 辅助调试代理
 *
 * GDB AI Agent 是 OpenVela 提供的一种面向 Crash 问题的快速调试解决方案。
 * 该机制通过 MCP（Model Context Protocol）将 GDB 与大模型连接起来，
 * 使 AI 能够直接调用 GDB 完成调试分析工作。
 *
 * GDB AI Agent 的核心通信基础是 gdbrpc，它为 GDB 提供了可远程调用的
 * RPC 接口，并在不侵占现有 GDB 调试会话的前提下，实现 AI 与人工调试
 * 的协同工作。
 */

/**
 * @section gdb_ai_overview Overview
 * @brief 设计目标与核心价值
 *
 * GDB AI Agent 在保留原生 GDB 命令执行能力的基础上，
 * 对复杂的 GDB Plugin 调用流程进行了适配与封装，
 * 使用户无需深入理解大量 GDB Plugin 细节，
 * 也能够完成针对 OpenVela 系统的调试与分析工作。
 *
 * 相较于传统人工调试，该机制的优势主要体现在：
 * - 能够直接围绕地址、内存布局和指令行为进行分析
 * - 在调试信息不足或内存已部分损坏的场景下，
 *   避免工程师长时间对汇编代码或裸地址进行人工推断
 * - 将复杂、重复的调试操作交由 AI 自动执行，
 *   工程师可专注于结果验证与结论判断
 */

/**
 * @section gdb_ai_arch Architecture
 * @brief 架构与工作机制
 *
 * GDB AI Agent 通过 MCP Client 与 GDB MCP Server 建立连接，
 * GDB MCP Server 依托 gdbrpc 与正在运行的 GDB 实例通信，
 * 从而实现以下能力：
 *
 * - AI 远程调用 GDB 命令
 * - AI 调用并组合复杂的 GDB Plugin 功能
 * - 在不打断当前人工调试会话的情况下并行执行分析
 *
 * 该架构允许工程师在使用 AI 自动分析的同时，
 * 手动对关键结论进行验证，避免“黑盒式调试”。
 */

/**
 * @section gdb_ai_usage Usage
 * @brief 使用方法
 *
 * 使用 GDB AI Agent 需要完成 MCP Client 与 GDB MCP Server 的配置。
 *
 * @subsection gdb_ai_mcp MCP Client 配置
 *
 * 以 Visual Studio Code 为例，需要在 `.vscode/mcp.json` 中
 * 添加如下配置：
 *
 * @code
 * {
 *   "inputs": [],
 *   "servers": {
 *     "gdbmcp": {
 *       "command": "python",
 *       "type": "stdio",
 *       "args": [
 *         "-m",
 *         "nxgdbmcp",
 *         "--stdio"
 *       ],
 *       "env": {
 *         "PYTHONPATH": "nuttx/tools/pynuttx/"
 *       }
 *     }
 *   }
 * }
 * @endcode
 *
 * 若已通过 `pip install pynuttx` 安装 pynuttx，则无需额外设置
 * PYTHONPATH。
 *
 * 当 `args` 中未指定 `--stdio` 时，系统将使用 streamable-http
 * 方式进行通信，该方式更适合统一部署，但目前尚不支持身份认证。
 */

/**
 * @subsection gdb_ai_gdbrpc gdbrpc 启动
 * @brief 在现有 GDB 会话中启用 gdbrpc
 *
 * 在一个已经建立的 GDB 调试会话中，需要启动 gdbrpc
 * 以允许 MCP Server 远程调用 GDB。
 *
 * gdbrpc 可通过以下方式获得：
 * - 随 GDB Plugin 自动加载
 * - 通过 pip 单独安装 gdbrpc
 *
 * 若使用 GDB Plugin，可直接在 GDB 中执行：
 *
 * @code
 * (gdb) source nuttx/tools/pynuttx/gdbinit.py
 * @endcode
 *
 * 启动完成后，当前 GDB 会话将暴露 RPC 接口，
 * 供 GDB AI Agent 调用。
 */

/**
 * @section gdb_ai_scenarios Scenarios
 * @brief 典型使用场景
 *
 * GDB AI Agent 适用于以下调试场景：
 *
 * - Crash Log / CoreDump 场景下的快速问题定位
 * - 内存部分损坏、调试信息不完整的复杂异常
 * - 不希望人工逐条分析汇编或地址特征的场景
 * - 希望在人工调试基础上引入 AI 辅助分析的场景
 *
 * 在上述场景中，AI 可作为“自动化分析助手”，
 * 而工程师仍保有对调试结论的最终判断权。
 */
