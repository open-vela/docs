# 在 R528 MIBOX-X1 上运行 AI Agent（实验）
\[ [English](../../en/contest_hk_2026/mibox_x1_ai_agent_guide.md) | 简体中文 | [繁體中文](./mibox_x1_ai_agent_guide_zh-hk.md) \]

> 本文介绍怎样编译一份带 ai_agent 的 R528 MIBOX-X1 固件，烧录后让开发板联网，设置大模型，并在串口里和 Agent 对话。这是一篇实验性质的指南：默认的 `nsh` 配置不带 ai_agent，需要自己新建配置并编译固件。我们在开发板上验证过文字对话，语音等功能没有验证，见[第七节](#七没有验证的内容)。

## 一、开始之前

默认的 `nsh` 配置不包含 ai_agent。本文在 `nsh` 的基础上多开 ai_agent 和它依赖的几项配置，做成一个新配置 `nsh_agent`。

开始之前需要：

- 已经能按[开发板使用指南](./mibox_x1_board_guide.md)编译、烧录 `nsh` 固件。
- 已经能按[连接开发板指南](./mibox_x1_connect_guide.md)用串口连上开发板，并连接 Wi-Fi。
- 一个大模型的 API key（自己申请）。本文以小米 MiMo 的 Token Plan 为例，其他平台的做法相同。

## 二、新建 nsh_agent 配置

在 SDK 根目录执行：

```bash
cd vendor/allwinnertech/boards/r528/r528s3-mibox-x1/configs
cp -r nsh nsh_agent
```

然后编辑 `nsh_agent/defconfig`：

1. 删除这一行：

   ```text
   # CONFIG_MBEDTLS_NET_C is not set
   ```

   Agent 用 mbedTLS 的网络接口连接大模型服务器，这一项必须打开。删除这一行后，编译时它会被打开，我们编译后确认过最终配置里是 `CONFIG_MBEDTLS_NET_C=y`。
2. 在文件末尾追加这五行：

   ```text
   CONFIG_EVENT_FD=y
   CONFIG_EXAMPLES_AI_AGENT_VELA=y
   CONFIG_NETUTILS_WEBCLIENT=y
   CONFIG_OPENSSL_MBEDTLS_WRAPPER=y
   CONFIG_SYSTEM_POPEN=y
   ```

   其中 `CONFIG_EXAMPLES_AI_AGENT_VELA` 是 ai_agent 本体，命令名是 `ai_agent`；其余四项是它依赖的组件。

这样得到的配置，和我们编译验证用的配置完全一致。

## 三、编译和打包

`m nsh` 命令只会编译 `nsh` 配置，所以编译 `nsh_agent` 要直接调用 `build.sh`：

```bash
cd vendor/allwinnertech/lichee
source envsetup.sh
lunch_nuttx r528s3-mibox-x1
cd ../../..
./build.sh vendor/allwinnertech/boards/r528/r528s3-mibox-x1/configs/nsh_agent/ -e -Wno-error -j$(nproc)
cd vendor/allwinnertech/lichee
pack
```

- 在 24 核的开发机上，编译加打包约 4 分钟。
- `pack` 结束时命令的返回值可能不是 0。请以输出里的 `pack finish` 和生成的 `.img` 文件为准。
- 固件文件名和 `nsh` 固件相同：`vendor/allwinnertech/lichee/out/r528s3/mibox-x1_nand/rtos_nuttx_r528s3-mibox-x1_uart0_256Mnand.img`。再编译一次会覆盖它，建议编完马上复制一份并改个名字，例如加上 `_agent` 后缀。

## 四、烧录并联网

1. 按[开发板使用指南](./mibox_x1_board_guide.md)第四节烧录固件。
2. 按[连接开发板指南](./mibox_x1_connect_guide.md)用串口连上开发板，确认出现 `nsh>`。
3. 连接 Wi-Fi，并确认能 ping 通域名，例如：

   ```text
   nsh> ping api.xiaomimimo.com
   ```

   板子每次上电后都要重新连接 Wi-Fi。要用 2.4 GHz 的网络。

## 五、设置大模型并提问

在 `nsh>` 提示符下输入 `ai_agent`，进入 Agent 的命令行，提示符变成 `vela>`：

```text
nsh> ai_agent
vela>
```

### 1、设置大模型

`set_llm` 有两种写法：

```text
vela> set_llm <预设名> <key>
vela> set_llm <地址> <模型名> <key>
```

预设名有 `kimi`、`qwen`、`deepseek`、`glm`、`openai`、`openrouter`、`mimo`，各自带一个默认地址和默认模型。如果你的 key 要用别的地址，就用第二种写法，把地址写到 `/v1` 为止，程序会自动补上 `/chat/completions`。

以小米 MiMo 的 Token Plan 为例。Token Plan 的 key 只能用它专属的地址，不能用 `mimo` 预设（预设用的是 `api.xiaomimimo.com`，用 Token Plan 的 key 会返回 401）：

```text
vela> set_llm https://token-plan-cn.xiaomimimo.com/v1 mimo-v2.6-flash <你的key>
```

- 地址和可用的模型名，请以 MiMo 开放平台控制台里 Token Plan 页面显示的为准。控制台里列出的对话模型有 `mimo-v2.6-pro` 和 `mimo-v2.6-flash`，我们测试用的是 `mimo-v2.6-flash`。名字里带 `asr` 的是语音识别模型，带 `tts` 的是语音合成模型，不是对话模型。
- 设置成功后，日志里会显示 `LLM backend: ...` 和 `API key saved.`。用 `config_show` 可以查看当前配置。

API key 是私人信息。命令会回显在终端里，日志里也可能出现，截图或贴日志给别人之前，请先把 key 遮住。key 不小心泄露后，到平台重置它。

### 2、提问

```text
vela> ask hello
```

联网和 key 都正确时，几秒钟后会看到回复。下面是一次真实运行的日志节选（`<…>` 处省略了部分内容）：

```text
[llm] OpenAI API with tools (model: mimo-v2.6-flash, <…> bytes)
[vela_tls] Handshake OK: TLSv1.2 / <…>
[llm] Response: 55 bytes text, 0 tool calls, finish=end_turn
[trace:<…>] iter=0 tool=(none) latency=3015ms llm=ok backend=0
[agent] [Agent]: Hello! I'm your AI assistant. How can I help you today?
```

这次请求耗时约 3 秒。看到 `[Agent]:` 后面是模型的回复，就说明整条链路（联网、域名解析、TLS、大模型、Agent）都通了。

## 六、看日志排错

Agent 给你的提示不一定能说明真实原因，出错时请看它前面的日志行：

| 日志里的内容 | 原因和处理 |
| ------------ | ---------- |
| `API error 401`，`Invalid API Key` | key 无效，或者 key 和地址不配套。检查 key 有没有输错，Token Plan 的 key 要用专属地址 |
| `API error 404`，提示模型不存在 | 模型名写错了，核对控制台里的模型名 |
| `API error 429` | 额度或请求频率超限 |
| `net_connect <域名>:443 ret=0x52` | 解析不出域名，板子没有联网或没有 DNS。回到[第四节](#四烧录并联网)检查 Wi-Fi，用 `ifconfig` 看 `wlan0` 有没有地址 |
| Agent 回复「请求超时，LLM 响应时间过长」 | 不一定是真的超时，见下面的「系统时间」 |
| Agent 回复 `Sorry, I encountered an error.` | 没有说明原因，看它前面的 `API error` 等日志行 |
| 每隔 5 秒出现 `[weixin] No token, waiting...` | 微信通道已开启但没有配置，可以忽略，只是会刷屏 |

### 系统时间

Agent 在 TLS 握手之前会检查系统时间。如果时间早于 2024 年（板子联网校时之前显示的是 1970 年），它会把系统时钟直接改成 2026 年 2 月 28 日。所以你会看到日志里的时间突然跳到 `26/02/28`，这不是真实日期。

时间跳变还会影响超时判断：从日志看，Agent 用跳变前后的时间差计算请求耗时，一跳就是几十年，于是报出「请求超时」，但实际上请求是因为别的原因立即失败的。遇到这种提示，先看前面有没有 `net_connect` 或 `API error` 的日志行。

开机时会启动 NTP 服务，但它早于 Wi-Fi 连接。联网之后系统时间能否被自动校准，我们还没有验证。

## 七、没有验证的内容

以下内容我们没有在 MIBOX-X1 开发板上验证过，请不要当作可用的功能：

- 语音：录音、播放、语音识别和合成。Gemini-S1 开发板为 ai_agent 专门调整过音频配置，MIBOX-X1 没有做这一步。
- 飞书、微信、MQTT 通道，以及 Node、MCP。它们默认是开启的，但我们没有配置和测试。
- 工具调用。我们只测试了普通对话（`tool_use=0`），没有测试 Agent 调用内置工具（读文件、联网搜索、定时任务等）。
- 重新上电之后，大模型配置是否保留。
- 内存占用。
- 5 GHz 的 Wi-Fi 网络。
