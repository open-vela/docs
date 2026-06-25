# 快应用开发指南（AI 工作流）

> 本文档面向参赛者，介绍如何使用 openvela 快应用工作流，实现从需求到代码到调试的全流程自动化开发。

## 一、概述

### 1、什么是快应用

快应用是运行在 openvela 设备（手表、手环、音箱、AI 硬件等）上的轻量级应用，基于前端技术栈（HTML/CSS/JavaScript）开发。

### 2、技术特点

| 特性        | 说明                                                |
| ----------- | --------------------------------------------------- |
| 类 Web 开发 | 使用 `template` + `style` + `script` 三段式页面结构 |
| 内置组件    | 提供 `div`、`text`、`image`、`list` 等原生组件      |
| Flex 布局   | 默认采用 Flex 弹性布局                              |
| 系统能力    | 网络请求、传感器、录音、振动、蓝牙等系统 API        |
| 多设备适配  | 一套代码适配不同屏幕尺寸（手表圆屏、方屏、7寸屏等） |

### 3、与大赛的关系

> 参赛者可以在已支持的硬件平台上，用快应用快速搭建交互界面和 AI 应用原型，实现 AI 硬件的业务逻辑。

### 4、适用场景

- 智能手表/手环上的轻量应用
- 带屏音箱的交互界面
- AI 硬件的控制面板
- IoT 设备的配置和展示界面

### 5、工作流概述

本工作流将开发过程拆分为四个阶段，每个阶段由不同角色的 AI 负责：

| 阶段 | 名称       | AI 角色       | 产出物              |
| ---- | ---------- | ------------- | ------------------- |
| S1   | PRD 生成   | AI 产品经理   | 01-prd.md           |
| S2   | 技术方案   | AI 架构师     | 02-tech-design.md   |
| S3   | 功能研发   | AI 工程师     | 项目代码文件        |
| S4   | 模拟器调试 | AI 测试工程师 | 调试报告 + 修复代码 |

> 工作流支持两种模式：完整模式（S1→S2→S3→S4，适合需求不明确时）和快速模式（跳过 S1/S2 直接生成代码，适合需求明确时）。

## 二、环境搭建

> **环境要求**
> - 操作系统：推荐 **Ubuntu 22.04**
> - **不支持** Windows Subsystem for Linux (WSL) 和 Docker 容器环境

### 步骤一：安装 Node.js

推荐使用 Node.js v22 或更高的 LTS 版本。Ubuntu 22.04 推荐用 nvm 管理版本：

```bash
# 1. 安装 nvm（用当前最新版 v0.40.4）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash

# 2. 重新打开终端，安装 Node 22 (LTS)
nvm install 22

# 3. 验证
node -v
npm -v
```

### 步骤二：安装 adb 工具

部署快应用到 openvela 模拟器时需要 adb（Android Debug Bridge）进行文件推送。openvela 仓库不自带 adb，需手动安装：

```bash
sudo apt install -y adb
```

### 步骤三：安装 AIoT IDE

下载地址：https://iot.mi.com/vela/quickapp/zh/guide/start/use-ide.html

### 步骤四：配置大模型

工作流通过 Claude Code 调用大模型，官方推荐使用 MiMo 大模型，本节以 MiMo 大模型为例进行配置说明。

- **推荐使用多模态模型 mimo-v2.5，不要使用 mimo-v2.5-pro。**
- **按官方文档完成配置**：https://platform.xiaomimimo.com/docs/zh-CN/integration/claudecode
- **确认 ~/.claude/settings.json 中四个模型字段全部填 mimo-v2.5**（防止运行中自动切换到 pro）：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "<你的 MiMo Base URL>",
    "ANTHROPIC_AUTH_TOKEN": "<你的 API Key>",
    "ANTHROPIC_MODEL": "mimo-v2.5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "mimo-v2.5",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "mimo-v2.5",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "mimo-v2.5"
  }
}
```

### 步骤五：安装 IDE 插件

在插件市场安装以下 IDE 插件：

| 插件                    | 用途        |
| ----------------------- | ----------- |
| Claude Code for VS Code | AI 辅助开发 |

## 三、创建并启动项目

### 步骤一：下载工作流模板

打开一个空文件夹的终端，执行：

```bash
npx create-vela-workflow my-app --mode claude
```

### 步骤二：用 AIoT IDE 打开项目

用 AIoT IDE 打开刚下载的 `my-app`，可以看到里面有一个 `.claude` 文件夹。

### 步骤三：通过 AI 工作流创建项目生成代码

1. 在 AIoT IDE 中打开 Claude Code 插件，在 Claude Code 对话框中输入 `/vela-workflow`，按照提示操作即可生成完整的快应用。例如输入："创建一个小米手表音乐播放器快应用，支持播放/暂停、上一首/下一首、进度条显示"。

2. 工作流启动后的交互流程如下：

```
Step 1.1  需求确认    → 输入 y 确认 / e 修改
Step 1.2  设计稿确认  → 输入 1 提供设计稿 / 2 跳过
Step 1.3  模式选择    → 输入 1 完整流程 / 2 快速模式
```

您也可以参考[官方文档](https://iot.mi.com/vela/quickapp/zh/guide/start/use-ide.html)手动创建项目，创建项目后手写代码。

### 步骤四：配置模拟器

1. 具备代码后，请使用 AIoT IDE 打开生成的代码工程。
2. 在 AIoT-IDE 中点击 banner 栏的「模拟器」按钮。
3. 点击「新建」，选择 **vela-watch-5** 镜像。
4. 填写模拟器名称，点击「新建」。

### 步骤五：通过模拟器调试

请参考 https://www.npmjs.com/package/velajs-mcp 进行配置，配置成功后告诉 AI "**帮我用 VelaJS MCP 启动 xxx 模拟器运行项目**"，即可进入模拟器调试阶段。

> 提交前建议在 openvela 模拟器上实际运行验证，确保应用在真实系统环境下正常工作。本步骤使用的是 AIoT-IDE 内置模拟器，与 openvela 模拟器存在差异。openvela 模拟器的部署和验证方法请参考《快应用开发指南（手动开发）》部署到 openvela 模拟器章节。

## 四、打包

请参考[《快应用开发指南（手动开发）》「三、打包」章节](./quickapp_manual.md#三打包)，**可使用工作流辅助开发**。

## 五、部署到 openvela 模拟器

请参考《快应用开发指南（手动开发）》。

## 六、部署到开发板

请参考《快应用开发指南（手动开发）》。

## 七、提交参赛代码

请参考《快应用开发指南（手动开发）》。

## 八、常见问题

### 1、使用相关

**Q: 工作流中断了怎么恢复？**

重新输入 `/vela-workflow`，系统会检测到未完成的 Session 并提示恢复。

**Q: 快速模式和完整模式怎么选？**

- **完整模式**：需求不明确、需要文档沉淀、团队协作时使用
- **快速模式**：需求明确、快速出原型、个人开发时使用

**Q: VelaJS MCP 工具不可用怎么办？**

1. 确认已安装 aiot-core、aiot-emulator、aiot-devtools 插件
2. 重启 IDE 后重试
3. 检查 MCP 配置中路径是否正确

**Q: 生成的代码有问题怎么办？**

- 在 Checkpoint 处输入 `e`，描述具体问题，AI 会迭代修复
- 进入 S4 模拟器调试，AI 会自动发现并修复运行时问题

**Q: 支持哪些设备？**

快应用面向基于 VelaOS 的智能穿戴设备：
- Xiaomi Watch S1 Pro / S5（480x480px 圆屏）
- Xiaomi Watch S3 / S4 / H1（466x466px 圆屏）
- REDMI Watch 5（432x514px 方屏）
- 小米手环 9（192x490px 跑道屏）
- 其他基于 Vela 系统的设备

### 2、常见布局与样式问题

- 如果遇到布局错乱问题，在根组件的样式中增加 `flex-direction:column;`
- 如果 `list` 中的内容不显示，需要在 `list-item` 样式中加上显式宽高：
  ```css
  height:50px;
  width:100%;
  ```

## 附录

### 1、工作流使用示例

**示例 1：快速创建计时器应用**

```
创建一个小米手表计时器快应用，功能包括：
- 开始/暂停/重置
- 显示分:秒:毫秒
- 圆形进度环显示
```

选择快速模式 → AI 直接生成代码 → 审阅确认 → 启动模拟器调试

**示例 2：基于设计稿创建应用**

```
创建小米手表应用商店，设计稿：https://www.figma.com/board/xxx/store?node-id=2-1621
```

选择完整模式 → AI 生成 PRD → 技术方案 → 从 Figma 导出资源并生成代码 → 模拟器调试

**示例 3：给现有项目添加新页面**

```
给当前项目添加一个播放列表页面，支持歌曲列表展示和点击播放
```

AI 检测到已有项目 → 增量开发模式 → 新增页面和路由 → 更新 manifest

### 2、VelaJS MCP 工具参考

#### 设备与调试管理

| 功能                               | AI 提示词                  |
| ---------------------------------- | -------------------------- |
| 列出可用模拟器                     | 帮我查看已安装的模拟器设备 |
| 列出已连接设备（包括模拟器和真机） | 帮我列出已连接的设备       |
| 选择调试设备                       | 指定目标设备               |
| 启动调试                           | 编译并推送应用到设备       |
| 停止调试                           | 停止当前调试会话           |
| 获取调试状态                       | 查看当前调试是否运行中     |
| 构建项目                           | 编译生成 rpk 包            |

#### UI 检查工具

| 功能         | AI 提示词                |
| ------------ | ------------------------ |
| 截取屏幕截图 | 获取当前页面 UI 截图     |
| 获取页面快照 | 获取完整组件树结构       |
| 获取元素信息 | 查看指定元素的属性和样式 |

#### 日志与调试工具

| 功能           | 说明                         |
| -------------- | ---------------------------- |
| 获取控制台日志 | 查看 JS console 输出         |
| 获取网络请求   | 查看 fetch 请求记录          |
| 执行脚本       | 在应用上下文中执行 JS 表达式 |
| 获取存储数据   | 查看 localStorage 数据       |
| 获取构建日志   | 查看编译输出                 |
| 获取模拟器日志 | 查看模拟器系统日志           |

#### 工作流之外单独使用

即使不启动完整工作流，也可以在对话中直接请求 VelaJS MCP 能力：
- "帮我使用 Vela js-mcp 启动模拟器调试当前项目"
- "截取当前页面截图，检查布局是否正确"
- "查看控制台日志，看看有没有报错"
- "模拟点击页面上的播放按钮"

### 3、Figma MCP 设计稿集成（可选）

当你有 Figma 设计稿时，工作流会自动通过 Figma MCP 获取设计数据，确保代码与设计稿高度一致。

#### 配置方法

在 MCP 配置中添加 Figma 服务器：

```json
{
  "mcpServers": {
    "figma": {
      "command": "uvx",
      "args": ["mcp-figma"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "你的 Figma Token",
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "autoApprove": ["get_file", "get_file_nodes", "export_image"]
    }
  }
}
```

获取 Token：Figma → Settings → Personal Access Tokens → 创建新 Token。

#### 使用方式

在 Step 1.2 设计稿确认环节选择 `1`，粘贴 Figma 链接即可。支持的 URL 格式：

```
https://www.figma.com/board/{file_key}/{name}?node-id={node_id}
https://www.figma.com/file/{file_key}/{name}?node-id={node_id}
```

工作流会自动解析链接、获取节点结构和样式、导出图片资源到项目目录、基于真实设计数据生成代码。

#### 两个 MCP 的分工

| MCP 工具   | 用途                     | 使用阶段                   |
| ---------- | ------------------------ | -------------------------- |
| Figma MCP  | 获取设计稿信息、导出图片 | S1/S2/S3（设计稿驱动开发） |
| VelaJS MCP | 调试运行、截图、交互测试 | S4（模拟器调试）           |

> 两者不可混用。设计稿阶段用 Figma MCP，调试阶段用 VelaJS MCP。
