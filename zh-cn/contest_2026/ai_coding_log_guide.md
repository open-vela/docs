# AI Coding 日志归集与提交手册

本手册面向参赛者，说明在使用 AI 编程工具开发时，如何将与 AI 的对话日志归集并提交至比赛仓库。日志采用两阶段机制：对话先暂存于本机，仅在参赛者主动导出后才会进入比赛仓库，个人对话不会被误传。

> 仓库获取与提交的总体流程，见 [《参赛代码提交指南》](./code_submission_guide.md)。

## 全流程速览

日志归集与提交分为三步：

```text
① 安装    一次性运行 install.sh                                  （见第一节）
② 开发    使用 Claude Code / AIoT-IDE / OpenCode / Codex 进行开发   （见第二节）
③ 提交    主动导出选定对话至 logs/，随代码一并提交                （见第三节）
```

**关键术语**

- **staging（本机暂存区）**：位于 `~/.claude/contest-collector-staging/`，AI 对话首先写入此处，不会自动上传。
- **导出（打包）**：由参赛者主动将选定对话从 staging 复制至比赛仓库的 `logs/` 目录。
- **hook（钩子）**：随安装部署在本机的程序，在 AI 对话结束时自动将记录写入 staging。
- **repo init / repo sync**：多仓库管理命令，用于一次性拉取 openvela 全量代码及参赛专属仓库。

## 一、安装与自检

### 1、运行 install.sh（仅需一次）

完成 [《参赛代码提交指南》](./code_submission_guide.md) 中的 `repo init` 与 `repo sync` 后，在参赛专属仓库目录内执行一次：

```bash
cd <你的 demo 仓>     # 例如 contest2026-042-openvela
bash ../.claude/skills/contest-log-collector/onboarding/install.sh \
  --team-id contest2026-042-openvela \
  --github-login <你的 GitHub username>
```

`install.sh` 将自动创建身份信息文件 `~/.claude/contest-collector.env`（内容为 TEAM_ID 与 GITHUB_LOGIN），无需手动创建。执行完成后可通过以下命令核对：

```text
TEAM_ID=contest2026-042-openvela
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

本届支持以下 4 种工具，可任选其一使用。完成第一节的 `install.sh` 后，全局 hook 即已就位。

### 1、Claude Code（官方主推，支持 CLI 与 AIoT-IDE 内嵌）

**通过 AIoT-IDE（推荐）**

1. 安装 AIoT-IDE，参见大赛官方 IDE 使用文档。
2. 在 AIoT-IDE 中于任意位置（包括桌面、子目录或仓库之外）打开 Claude Code 插件并开始对话。
3. 关闭对话后，记录自动写入 staging。

**通过 Claude Code CLI**

```bash
claude   # 可在任意目录运行，不限于仓库内
```

退出时（`/exit` 或 Ctrl+D）记录自动写入 staging。

### 2、OpenCode（CLI / TUI / VS Code 扩展）

```bash
opencode
```

OpenCode V1 插件已预装，会话结束后自动写入 staging。

### 3、Codex CLI

```bash
codex
```

Stop hook 自动写入 staging。

### 4、多人协作

每位成员需分别完成以下操作：

1. 各自克隆本地副本。
2. 将 `~/.claude/contest-collector.env` 中的 GITHUB_LOGIN 修改为本人的 username（重要）。
3. 各自与 AI 工具协作。

各成员的 staging 相互独立，分别导出各自的会话即可。

## 三、导出并提交对话日志

工具不会自动将对话写入比赛仓库，需由参赛者主动导出。以下 3 种方式可任选其一。

### 1、自然语言指令（推荐）

向 AI 发送如下任一指令：

- "archive this session into the contest repo"
- "把刚才的会话存到比赛仓库"
- "package this conversation"
- "归档对话"

AI 将先运行 `tools/export-session.py --latest` 进行预览，展示待导出的会话；确认无误后再追加 `--confirm` 正式写入。

### 2、Slash 命令（Claude Code）

```text
/contest-snapshot
```

效果同上，同样遵循“预览 → 确认”两步。

### 3、直接运行脚本

```bash
# 1. 列出 staging 中的所有会话，确认待导出项
python3 tools/export-session.py --list

# 2. 预览待导出会话（默认仅预览，不写入文件）
python3 tools/export-session.py --latest
python3 tools/export-session.py --session <session-id>
python3 tools/export-session.py --today

# 3. 核对无误后，追加 --confirm 正式导出
python3 tools/export-session.py --latest --confirm
python3 tools/export-session.py --session <session-id> --confirm
python3 tools/export-session.py --today --confirm
python3 tools/export-session.py --since 2026-06-15 --confirm
python3 tools/export-session.py --all --confirm
```

> 重要：未追加 `--confirm` 时仅为预览，不会写入任何文件。此设计用于避免误导出此前与 AI 进行的个人项目对话。建议流程：`--list` 查看清单 → `--session <id>` 预览 → `--session <id> --confirm` 正式写入。

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

### 1、写入 staging 的内容

只要与 AI 工具（Claude Code / OpenCode / Codex / AIoT-IDE）对话，所有对话均会写入 staging，涵盖以下全部场景：

- 在比赛仓库内
- 在个人项目内
- 在 `$HOME` 目录内
- 其他任意位置

但 staging 不会上传，仅保存于本机 `~/.claude/contest-collector-staging/`。

### 2、进入比赛仓库的内容（即评委可见）

仅限参赛者主动导出的会话。若与 AI 进行了 50 轮对话而仅导出 10 轮，则评委仅可见该 10 轮，其余 40 轮始终保留在本机。

### 3、记录的字段

| 字段                             | 内容                               |
| -------------------------------- | ---------------------------------- |
| `text`                           | 与 AI 的对话正文                   |
| `thinking`                       | AI 的思考过程（如工具暴露）        |
| `tool_name` / `input` / `output` | AI 调用的工具（read/edit/bash 等） |
| `model` / `tokens_in/out`        | 所用模型与 token 用量              |
| `seq`                            | 会话内单调递增序号（用于防作弊）   |

### 4、查看已导出内容

```bash
# 终端预览（彩色）
python3 tools/render-log.py logs/<your-github-login>/

# 生成 HTML 报告（浏览器打开）
python3 tools/render-log.py logs/<your-github-login>/ \
  --format html --out my-report.html
```

## 五、验证与排错

### 1、确认 staging 持续累积

```bash
# 与 AI 协作数轮后，另开终端执行：
ls -lt ~/.claude/contest-collector-staging/<your-github-login>/<today>/
```

应可见 `.jsonl` 文件，且大小随对话推进而增长。

### 2、查看 stderr 提示

每次 AI 会话结束，collector 会在 stderr 输出：

```text
[session-log] captured 3 event(s) -> .../claude-code__abc.jsonl
              (remember to 'git add logs/' when committing)
```

### 3、导出后合规性自检

```bash
python3 tools/validate-log.py logs/
```

应输出 `ALL OK`。若报错，多为工具缺陷，请在组委会群反馈。

### 4、未采集到或报错时的排查

请按以下顺序排查：

1. 运行健康检查：`bash ../.claude/skills/contest-log-collector/onboarding/verify-setup.sh`
2. 查看错误日志：`cat ~/.claude/contest-collector-staging/<your-login>/errors/*.err`
3. 仍无法解决，请在大赛技术支持群反馈。

## 六、常见问题

### Q1：未执行“打包”，对话会自动上传吗？

不会。工具不会自动 push 至任何 git 仓库。staging 位于 `~/.claude/contest-collector-staging/`，与 git 无关。

### Q2：与 AI 谈及的私人内容（薪资、情感、其他项目）会泄露吗？

只要不主动执行“打包”，此类对话不会进入比赛仓库，仅保存于本机 staging。如有顾虑，可在导出前删除 staging 中对应文件：

```bash
ls ~/.claude/contest-collector-staging/<your-login>/<date>/
rm <session-id>.jsonl
```

### Q3：可以修改 staging 或 logs 中的内容吗？

`tools/validate-log.py` 会检测 seq 缺号、跨字段不一致、manifest 与文件不匹配等篡改行为，修改日志将被视为作弊。但在导出前于 staging 中删除整个会话是允许的，其效果等同于“不打包”，评委不可见。

### Q4：可以临时关闭日志收集吗？

不建议。大赛规则要求全程归集（staging 全量采集）。参赛者可控制的是导出哪些会话至比赛仓库，这是为参赛者保留的隐私边界。

### Q5：临近截止如何处理？

截止时间到达后，组委会将：

1. 将仓库权限由 write 降为 read（不可再 push）；
2. 触发最终归档。

建议在截止前数小时：

```bash
# 查看尚未导出的会话
python3 tools/export-session.py --list

# 预览全部待导出会话（核对是否包含不应上传的个人对话）
python3 tools/export-session.py --all

# 核对无误后，追加 --confirm 一次性导出
python3 tools/export-session.py --all --confirm
git add logs/ && git commit -s -m "logs: final batch" && git push
```

### Q6：工具异常或未采集到日志怎么办？

排查步骤见“五、验证与排错”第 4 条。

### Q7：从仓库子目录（如 `cd src && claude`）启动 AI 可以吗？

可以。hook 为全局生效，无论当前工作目录位于何处，只要与 Claude Code / OpenCode / Codex 对话，记录均会写入 staging。

### Q8：拥有多个 demo 仓库（主仓 + 子模块）时日志如何归集？

按大赛规则，所有日志统一汇集至主 demo 仓库。子模块仓库无需安装日志工具，在主仓库内运行 `export-session.py` 即可。

### Q9：可以使用 ChatGPT / Cursor / Cody 等其他工具吗？

暂不支持。本届官方支持的工具为：

- Claude Code（主推，含 AIoT-IDE 内嵌）
- AIoT-IDE
- OpenCode
- Codex

使用其他工具产生的对话不会写入 staging，视为无效工时。

### Q10：直接调用 Anthropic API / OpenAI API 可以吗？

不可以。直接调用 API 的对话不在 session transcript 中，工具无法采集，须使用上述 4 种工具之一。

## 七、反馈与支持

- 技术问题：大赛技术支持群（由组委会拉入）。
- 工具缺陷：<https://github.com/open-vela/.claude/issues>
- 隐私与数据相关问题：组委会邮箱。

## 附录：工具自带文件清单（参考，可跳过）

以下为工具仓库与全局 hook 的目录结构，仅供需要了解内部实现者参考，正常使用无需关注。

`repo sync` 拉取的工程结构如下，其中 `.claude/` 为工具仓库（与 demo 仓库平级），并非安装在 demo 仓库内部：

```text
<你的工作树>/                            # repo init 拉取的工作树根目录
├── .repo/                              # repo 工具元数据
├── .claude/                            # 大赛工具仓库（open-vela/.claude，由 manifest 拉取）
│   └── skills/contest-log-collector/
│       ├── adapters/                   # snapshot core / opencode plugin 源
│       ├── commands/                   # slash command 源
│       ├── tools/                      # export / render / validate 工具源
│       ├── schema/                     # JSONL 契约源
│       └── onboarding/
│           ├── install.sh              # 安装脚本
│           ├── verify-setup.sh         # 健康检查
│           ├── USAGE.md                # 本文件（源）
│           └── JUDGE_GUIDE.md          # 评委指南（源）
├── nuttx/  apps/  vendor/  ...         # openvela 全量源码
└── <你的 demo 仓>/                      # 例如 contest2026-042-openvela
    ├── .gitignore
    ├── .claude/  .opencode/  tools/  schema/   # 安装后生成
    ├── USAGE.md  JUDGE_GUIDE.md
    └── logs/                           # 主动导出会话后生成
```

此外，第一节的 `install.sh` 会在 home 目录部署一份全局 hook：

```text
~/.claude/
├── settings.json                       # 注入 Stop/SessionEnd hook
├── contest-collector.env               # 身份信息（TEAM_ID + GITHUB_LOGIN）
├── contest-shared/                     # 全局 hook
└── contest-collector-staging/          # staging 区（本机全部 AI 对话）
```

全局 hook 不会自动 push，仅在本机写入文件，提交由参赛者自行控制。
