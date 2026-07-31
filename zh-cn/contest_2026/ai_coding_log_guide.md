# AI Coding 日志归集与提交手册

本手册面向参赛者，说明在使用 AI 编程工具开发时，如何将与 AI 的对话日志归集并提交至比赛仓库。系统采用了“工作区检测”与“自动入仓”机制。采集器仅在 `openvela` 工作区内（通过识别 `.repo/` 目录）激活。工作区内的对话会在会话结束时自动写入比赛仓库的日志目录，参赛者只需随代码执行常规提交即可。

> 仓库获取与提交的总体流程，见 [《参赛代码提交指南》](./code_submission_guide.md)。

## 全流程速览

日志归集与提交分为三步：

```text
① 安装    一次性运行 install.sh                                  （见第一节）
② 开发    在 openvela 工作区内使用 AI 工具进行开发                  （见第二节）
③ 提交    检查并提交 logs/ 下的日志记录至远程仓库                  （见第三节）
```

**关键术语**

- **工作区闸门（Workspace Gate）**：通过向上遍历查找 `.repo/` 目录实现环境识别。系统仅在工作区内采集记录。
- **staging（本机缓冲区）**：位于 `~/.claude/contest-collector-staging/`。作为工具内部交换数据的中转站，不再是主要的隐私屏障。
- **自动入仓**：在工作区内结束会话后，记录会自动写入比赛仓库的 `logs/` 目录。
- **手动同步**：通过脚本重新导出或选择性同步日志的可选操作。
- **hook（钩子）**：随安装部署在本机的程序，在会话结束时自动触发日志流转。
- **repo init / repo sync**：多仓库管理命令，用于拉取 openvela 代码及参赛专属仓库。

## 一、安装与自检

### 1、运行 install.sh（仅需一次）

完成 [《参赛代码提交指南》](./code_submission_guide.md) 中的 `repo init` 与 `repo sync` 后，在参赛专属仓库目录内执行一次：

```bash
cd <你的 demo 仓>     # 例如 contest2026_042_openvela
bash ../.claude/skills/contest-log-collector/onboarding/install.sh \
  --team-id contest2026_042_openvela \
  --github-login <你的 GitHub username>
```

`install.sh` 将自动创建身份信息文件 `~/.claude/contest-collector.env`（内容为 TEAM_ID 与 GITHUB_LOGIN），无需手动创建。执行完成后可通过以下命令核对：

```text
TEAM_ID=contest2026_042_openvela
GITHUB_LOGIN=<你的 GitHub username>
```

> 注意：若 GITHUB_LOGIN 不是本人，请改为本人的 username，否则日志将归属至队友名下。

### 2、运行健康检查脚本

`verify-setup.sh` 位于 manifest 拉取的工具仓库中，从专属仓库目录内以相对路径执行：

```bash
bash ../.claude/skills/contest-log-collector/onboarding/verify-setup.sh
```

如出现任何 `[FAIL]` 项，请按提示修复；无法解决时请在组委会群求助。

### 3、查看 staging（可选）

```bash
ls ~/.claude/contest-collector-staging/<your-github-login>/
```

首次为空；首次结束 AI 会话后，将出现 `<date>/<tool>__<sid>.jsonl`。

## 二、启用 AI 工具

本届支持以下 4 种工具，可任选其一使用。完成第一节的 `install.sh` 后，采集钩子即已就位。系统仅在 `openvela` 工作区内进行采集。

### 1、Claude Code（官方主推，支持 CLI 与 AIoT-IDE 内嵌）

**通过 AIoT-IDE（推荐）**

1. 安装 AIoT-IDE，参见大赛官方 IDE 使用文档。
2. 在 `openvela` 工作区目录内打开 Claude Code 插件并开始对话。
3. 关闭对话后，记录自动写入比赛仓 `logs/`。

**通过 Claude Code CLI**

```bash
# 必须在 openvela 工作区内的目录执行，方可被采集
claude
```

退出时（`/exit` 或 Ctrl+D）记录自动写入比赛仓 `logs/`。

### 2、OpenCode（CLI / TUI / VS Code 扩展）

```bash
opencode
```

会话结束后，记录自动写入比赛仓 `logs/`。

### 3、Codex CLI

```bash
codex
```

会话结束后，记录自动写入比赛仓 `logs/`。

### 4、多人协作

每位成员需分别完成以下操作：

1. 各自克隆本地副本。
2. 将 `~/.claude/contest-collector.env` 中的 GITHUB_LOGIN 修改为本人的 username（重要）。
3. 各自在工作区内与 AI 工具协作。

各成员的日志会按 GitHub 账号自动存放到对应的 `logs/<github_login>/` 目录下。

## 三、自动化入仓与日志提交

在 `openvela` 工作区内进行的 AI 对话，记录会在会话结束时自动写入比赛仓的 `logs/` 目录。

### 1、默认流程：自动归集

你无需执行任何额外的导出指令。在工作区内完成开发并关闭 AI 工具后，日志文件已物理存放在你的 demo 仓下。你可以通过以下操作完成提交：

```bash
git add logs/
git commit -s -m "logs: sync AI sessions"
git push
```

注意：工具仅负责写入本地文件，不会执行 `git push` 操作。物理上传的控制权完全掌握在你手中。

### 2、手动工具：管理与重新导出（可选）

虽然流程已自动化，但你仍可以使用 `contest-snapshot` 脚本来列出或查看记录。该脚本对 `export-session.py` 进行了封装。

```bash
# 1. 列出当前已采集的会话清单
contest-snapshot --list

# 2. 预览特定会话的详细内容（不写入文件）
contest-snapshot --session <session-id>

# 3. 手动重新同步当天的所有会话（通常无需使用）
contest-snapshot --today --confirm
```

**若 `contest-snapshot: command not found`**：表示 `~/.local/bin` 不在 `PATH` 中。执行以下任一操作即可：

```bash
# 方法 1：将 ~/.local/bin 永久加入 PATH（推荐）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 方法 2：使用完整路径作为等价形式
python3 ../.claude/skills/contest-log-collector/tools/export-session.py --list
```

### 3、多人协作提交

在团队开发模式下，请确保每位成员在 commit 前都拉取了最新的日志文件。各成员的日志按 GitHub 账号区分，合并代码时不会发生冲突。推荐在 push 前执行一次 `git add logs/`。

效果同上，同样遵循“预览 → 确认”两步。

### 3、直接运行脚本

`install.sh` 在 `~/.local/bin/contest-snapshot` 安装了短命令脚本，对长路径进行了封装。请优先使用：

```bash
# 1. 列出 staging 中的所有会话，确认待导出项
contest-snapshot --list

# 2. 预览待导出会话（默认仅预览，不写入文件）
contest-snapshot --latest
contest-snapshot --session <session-id>
contest-snapshot --today

# 3. 核对无误后，追加 --confirm 正式导出
contest-snapshot --latest --confirm
contest-snapshot --session <session-id> --confirm
contest-snapshot --today --confirm
contest-snapshot --since 2026-06-15 --confirm
contest-snapshot --all --confirm
```

> 重要：未追加 `--confirm` 时仅为预览，不会写入任何文件。此设计用于避免误导出此前与 AI 进行的个人项目对话。建议流程：`--list` 查看清单 → `--session <id>` 预览 → `--session <id> --confirm` 正式写入。

**若 `contest-snapshot: command not found`**：表示 `~/.local/bin` 不在 `PATH` 中。执行以下任一操作即可：

```bash
# 方法 1：将 ~/.local/bin 永久加入 PATH（推荐）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 方法 2：使用完整路径作为 fallback（短命令的等价形式）
python3 ../.claude/skills/contest-log-collector/tools/export-session.py --latest --confirm
```

### 4、提交（commit + push）

```bash
git add logs/
git commit -s -m "logs: capture session"
git push
```

亦可与代码一并提交：

```bash
git add .   # 自动包含 logs/
git commit -s -m "feat: implement xxx"
git push
```

## 四、隐私保护：工具采集范围说明

### 1、隔离边界：工作区闸门

系统通过识别 `openvela` 工作区根目录下的 `.repo/` 标识来确定采集范围。只有在此目录树内进行的操作才会被记录并自动入仓。

### 2、非工作区不采集

在工作区之外进行的任何对话，例如个人项目、系统根目录、个人文档或 `$HOME` 目录等，完全不被采集。这意味着此类对话既不会写入暂存区，也不会进入比赛仓库，在根源上实现了隐私隔离。

### 3、记录字段

| 字段                             | 内容                               |
| -------------------------------- | ---------------------------------- |
| `text`                           | 与 AI 的对话正文                   |
| `thinking`                       | AI 的思考过程                      |
| `tool_name` / `input` / `output` | AI 调用的工具（read/edit/bash 等） |
| `model` / `tokens_in/out`        | 所用模型与使用统计                 |
| `seq`                            | 会话内递增序号（用于验证一致性）   |

### 4、查看与核对内容

```bash
# 终端预览（彩色）
python3 ../.claude/skills/contest-log-collector/tools/render-log.py logs/<your-github-login>/

# 生成 HTML 报告供浏览器查看
python3 ../.claude/skills/contest-log-collector/tools/render-log.py logs/<your-github-login>/ \
  --format html --out my-report.html
```

## 五、验证与排错

### 1、确认自动导出生效

与 AI 协作并结束会话后，请检查你的 demo 仓目录：

```bash
ls -lt logs/<your-github-login>/<today>/
```

应可见最新的 `.jsonl` 文件。如果该目录未出现，请检查你是否在 `openvela` 工作区内运行工具。

### 2、查看 stderr 提示

每次 AI 会话结束，采集器会在终端输出：

```text
[session-log] auto-exported session -> logs/.../claude-code__abc.jsonl
              (remember to 'git push' to complete submission)
```

### 3、合规性自检

```bash
python3 ../.claude/skills/contest-log-collector/tools/validate-log.py logs/
```

### 4、排查建议

1. 确认当前路径位于 `openvela` 工作区内。
2. 运行健康检查：`bash ../.claude/skills/contest-log-collector/onboarding/verify-setup.sh`
3. 查看错误记录：`cat ~/.claude/contest-collector-staging/<your-login>/errors/*.err`

## 六、常见问题

### Q1：未执行“打包”操作，对话会自动上传吗？

物理上传由你控制。工具仅负责将日志写入本机磁盘的 `logs/` 目录，它自身永远不会执行 `git push` 命令。你需要手动提交代码并推送至 GitHub，日志才会真正上传。

### Q2：与 AI 谈及的私人内容会泄露吗？

在工作区（识别到 `.repo/` 的目录）之外进行的对话完全不采集，无需担心。如果你在工作区内谈论了敏感内容，记录会在会话结束时自动写入 `logs/`。你可以在执行 `git commit` 前，手动删除对应的 `.jsonl` 文件。

### Q3：可以修改 logs 中的内容吗？

`validate-log.py` 脚本会检测序号断档或内容篡改行为。修改日志内容会被视为作弊。如果你需要撤回某次对话，在 `git commit` 前直接删除 `logs/` 下对应的文件即可，这样评委将无法看到该次对话。

### Q4：可以临时关闭日志收集吗？

最简单的办法是在工作区外（找不到 `.repo/` 目录的地方）与 AI 对话，此时工具不会进行任何采集。

### Q5：临近截止如何处理？

由于会话已自动导出至本地，你只需在截止前确保已完成 `git push` 即可。如果你想做一次最终清查，可以运行以下命令确认是否有遗漏：

```bash
# 确认本地所有已采集的日志均已入仓
contest-snapshot --list
git add logs/ && git commit -s -m "logs: final sync" && git push
```

### Q6：工具异常或未采集到日志怎么办？

排查步骤见“五、验证与排错”第 4 条。

### Q7：从仓库子目录（如 `cd nuttx && claude`）启动 AI 可以吗？

可以。只要你处于 `openvela` 工作区的任何子目录内（包括嵌入式源码目录等），采集器都会通过识别上层的 `.repo/` 目录来激活。反之，若在工作区外的随机目录启动工具，则不会进行采集。

### Q8：拥有多个 demo 仓库（主仓 + 子模块）时日志如何归集？

按大赛规则，所有日志统一汇集至主 demo 仓库。子模块仓库无需重复配置，在工作区内进行的任何 AI 协作都会自动同步至主仓的 `logs/` 目录下。

### Q9：可以使用 ChatGPT / Cursor / Cody 等其他工具吗？

暂不支持。本届官方支持且能自动采集日志的工具为：

- Claude Code（主推，含 AIoT-IDE 内嵌）
- AIoT-IDE
- OpenCode
- Codex

使用其他三方工具产生的对话无法被采集，将无法计入有效工时。

### Q10：直接调用 Anthropic API / OpenAI API 可以吗？

不可以。直接调用 API 的对话不在 session transcript 中，工具无法采集。请务必使用上述 4 种官方支持的工具。

### Q11：安装 hook 之前的 Claude Code 历史对话能补回来吗？

可以。Claude Code 的历史对话保存在本机 `~/.claude/projects/` 目录。在选手仓内执行以下命令即可一键补回：

```bash
contest-snapshot --backfill
git add logs/ && git commit -s -m "logs: backfill history" && git push
```

命令会自动扫描所有历史 transcript，跳过已采集的，将未采集的补导进 `logs/`。可多次执行，不会产生重复。

## 七、Windows 用户操作指南

Windows 用户无需 WSL，只需 **Python 3 + Git** 即可使用全部功能。所有操作在 **Git Bash** 中执行。

### 1、环境准备（一次性）

1. **安装 Python 3**：从 [python.org](https://www.python.org/downloads/) 下载，安装时勾选 **Add Python to PATH**。
2. **安装 Git for Windows**：从 [git-scm.com](https://git-scm.com/download/win) 下载，安装时自带 **Git Bash**。
3. **安装 Claude Code**（如使用）：`npm install -g @anthropic-ai/claude-code`

> 如果已安装 WSL，可直接在 WSL 中按 Linux 流程操作，跳过本节。

### 2、拉取 openvela 工程

打开 **Git Bash**，执行：

```bash
# 如未安装 repo 工具
mkdir -p ~/.bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/.bin/repo
chmod +x ~/.bin/repo
export PATH=~/.bin:$PATH

# 拉取工程
repo init -u https://github.com/open-vela/contest2026_XXX_yourteam \
  -b dev-ai-contest-2026 -m contest2026_XXX_yourteam.xml
repo sync -c -j8
```

### 3、安装日志工具

在 **Git Bash** 中进入选手仓执行：

```bash
cd contest2026_XXX_yourteam
bash ../.claude/skills/contest-log-collector/onboarding/install.sh \
  --team-id contest2026_XXX_yourteam \
  --github-login <你的GitHub用户名>
```

安装脚本会自动检测 Python 路径（`python3` / `python` / `py`），并在 `settings.json` 中用 Python 直接调用采集脚本 —— **hook 不依赖 bash 执行**，因此 Claude Code 的 hook 在 Windows 上也能正常触发。

### 4、开发与提交

在 Git Bash 中启动 AI 工具（`claude` / `opencode` / `mimo`）即可。首次对话结束时会询问是否上传日志，回答 `yes` 后后续自动上传。提交方式与 Mac/Linux 完全一致：

```bash
git add logs/ && git commit -s -m "logs: capture session" && git push
```

### 与 Mac/Linux 的区别

| 项目 | Mac/Linux | Windows |
| --- | --- | --- |
| 终端 | Terminal | **Git Bash** |
| Python | 系统自带 | 安装 Python 3（勾选 Add to PATH） |
| hook 执行 | bash 调用 | **Python 直接调用**（不依赖 bash） |
| 其他 | — | **无区别** |

## 八、反馈与支持

- 技术问题：大赛技术支持群（由组委会拉入）。
- 工具缺陷：<https://github.com/open-vela/.claude/issues>
- 隐私与数据相关问题：组委会邮箱。

## 附录：工具自带文件清单（参考，可跳过）

以下为工具仓库与全局钩子的目录结构，仅供了解内部实现参考。

`repo sync` 拉取的工程结构如下。`.claude/` 为工具仓库（与 demo 仓库平级）。`install.sh` 采用**零侵入**设计。demo 仓库中**在工作区内首次结束 AI 会话后**会自动出现 `logs/` 目录。

```text
<你的工作树>/                            # repo init 拉取的工作树根目录
├── .repo/                              # repo 工作区标识
├── .claude/                            # 大赛工具仓库（open-vela/.claude）
│   └── skills/contest-log-collector/
│       ├── adapters/                   # 核心采集逻辑
│       ├── tools/                      # 同步与校验工具
│       └── onboarding/
│           ├── install.sh              # 安装脚本
│           └── verify-setup.sh         # 健康检查
├── nuttx/  apps/  vendor/  ...         # openvela 全量源码
└── <你的 demo 仓>/                      # 例如 contest2026_042_openvela
    ├── (你的代码、README、配置)
    └── logs/                           # 首次结束 AI 会话后自动生成
        └── <your-github-login>/
            ├── manifest.json
            └── <date>/<tool>__<sid>.jsonl
```

此外，`install.sh` 会在 home 目录部署全局状态（**这些文件不进入 demo 仓库**）：

```text
~/.claude/
├── settings.json                       # 挂载会话结束钩子
├── contest-collector.env               # 身份信息
└── contest-collector-staging/          # 本机缓冲区
    └── <your-github-login>/
        └── <date>/<tool>__<sid>.jsonl

~/.config/opencode/plugin/
└── contest-collector.js                # OpenCode 插件

~/.local/bin/
└── contest-snapshot                    # 便捷脚本
```

采集器不会自动执行网络上传，仅在本机工作区内流转日志，最终提交由参赛者自行通过 git 完成。
**demo 仓库中除 `logs/` 目录外不会出现任何采集器相关文件。**
