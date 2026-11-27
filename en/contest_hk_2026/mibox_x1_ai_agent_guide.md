# Running the AI Agent on the R528 MIBOX-X1 (Experimental)
\[ English | [简体中文](../../zh-cn/contest_hk_2026/mibox_x1_ai_agent_guide.md) | [繁體中文](../../zh-cn/contest_hk_2026/mibox_x1_ai_agent_guide_zh-hk.md) \]

> This guide explains how to build R528 MIBOX-X1 firmware that includes ai_agent, flash it, connect the board to the network, set a large language model, and chat with the Agent over the serial port. It is experimental: the default `nsh` configuration does not include ai_agent, so you create a new configuration and build the firmware yourself. We verified text chat on a real board. We did not verify voice and other features; see [Section VII](#vii-what-has-not-been-verified).

## I. Before You Start

The default `nsh` configuration does not include ai_agent. This guide turns on ai_agent and a few options it depends on, on top of `nsh`, to make a new configuration called `nsh_agent`.

You need:

- Experience building and flashing the `nsh` firmware by following the [Development Board Guide](./mibox_x1_board_guide.md).
- A working serial connection and a Wi-Fi connection, as described in the [Connecting Guide](./mibox_x1_connect_guide.md).
- An API key for a large language model (you apply for it yourself). This guide uses the Xiaomi MiMo Token Plan as the example. Other providers work the same way.

## II. Create the nsh_agent Configuration

Run these commands in the SDK root directory:

```bash
cd vendor/allwinnertech/boards/r528/r528s3-mibox-x1/configs
cp -r nsh nsh_agent
```

Then edit `nsh_agent/defconfig`:

1. Delete this line:

   ```text
   # CONFIG_MBEDTLS_NET_C is not set
   ```

   The Agent uses the mbedTLS network interface to reach the model server, so this option must be on. After you delete the line, the build turns it on. We checked that the final configuration after the build contains `CONFIG_MBEDTLS_NET_C=y`.
2. Append these five lines at the end of the file:

   ```text
   CONFIG_EVENT_FD=y
   CONFIG_EXAMPLES_AI_AGENT_VELA=y
   CONFIG_NETUTILS_WEBCLIENT=y
   CONFIG_OPENSSL_MBEDTLS_WRAPPER=y
   CONFIG_SYSTEM_POPEN=y
   ```

   `CONFIG_EXAMPLES_AI_AGENT_VELA` is ai_agent itself, and its command name is `ai_agent`. The other four are components it depends on.

The result is identical to the configuration we built and verified.

## III. Build and Pack

The `m nsh` command only builds the `nsh` configuration, so call `build.sh` directly to build `nsh_agent`:

```bash
cd vendor/allwinnertech/lichee
source envsetup.sh
lunch_nuttx r528s3-mibox-x1
cd ../../..
./build.sh vendor/allwinnertech/boards/r528/r528s3-mibox-x1/configs/nsh_agent/ -e -Wno-error -j$(nproc)
cd vendor/allwinnertech/lichee
pack
```

- On a 24-core development machine, building and packing take about 4 minutes.
- The return value of `pack` may be non-zero when it ends. Go by the `pack finish` line in the output and by the generated `.img` file.
- The firmware has the same file name as the `nsh` firmware: `vendor/allwinnertech/lichee/out/r528s3/mibox-x1_nand/rtos_nuttx_r528s3-mibox-x1_uart0_256Mnand.img`. Building again overwrites it, so copy it right away and rename the copy, for example with an `_agent` suffix.

## IV. Flash and Connect to the Network

1. Flash the firmware by following Section IV of the [Development Board Guide](./mibox_x1_board_guide.md).
2. Connect over the serial port by following the [Connecting Guide](./mibox_x1_connect_guide.md), and check that `nsh>` appears.
3. Connect to Wi-Fi and check that you can ping a domain name, for example:

   ```text
   nsh> ping api.xiaomimimo.com
   ```

   The board must reconnect to Wi-Fi after every power-up. Use a 2.4 GHz network.

## V. Set the Model and Ask a Question

At the `nsh>` prompt, type `ai_agent` to enter the Agent command line. The prompt changes to `vela>`:

```text
nsh> ai_agent
vela>
```

### 1. Set the model

`set_llm` has two forms:

```text
vela> set_llm <preset> <key>
vela> set_llm <url> <model> <key>
```

The presets are `kimi`, `qwen`, `deepseek`, `glm`, `openai`, `openrouter` and `mimo`. Each comes with a default address and a default model. If your key must be used with a different address, use the second form. End the address at `/v1`, and the program appends `/chat/completions`.

Take the Xiaomi MiMo Token Plan as an example. A Token Plan key works only with its own dedicated address. Do not use the `mimo` preset, which points to `api.xiaomimimo.com` and returns 401 for a Token Plan key:

```text
vela> set_llm https://token-plan-cn.xiaomimimo.com/v1 mimo-v2.6-flash <your key>
```

- Take the address and the model names from the Token Plan page of the MiMo console. The chat models listed in the console are `mimo-v2.6-pro` and `mimo-v2.6-flash`, and we tested with `mimo-v2.6-flash`. Names containing `asr` are speech recognition models, and names containing `tts` are speech synthesis models. They are not chat models.
- After a successful setting, the log shows `LLM backend: ...` and `API key saved.`. Use `config_show` to see the current configuration.

An API key is private. The command is echoed in the terminal and may appear in logs, so cover the key before you send a screenshot or a log to anyone. If a key is exposed by accident, reset it on the provider's platform.

### 2. Ask a question

```text
vela> ask hello
```

With the network and the key correct, the reply appears after a few seconds. The following is an excerpt from a real run (parts are replaced by `<…>`):

```text
[llm] OpenAI API with tools (model: mimo-v2.6-flash, <…> bytes)
[vela_tls] Handshake OK: TLSv1.2 / <…>
[llm] Response: 55 bytes text, 0 tool calls, finish=end_turn
[trace:<…>] iter=0 tool=(none) latency=3015ms llm=ok backend=0
[agent] [Agent]: Hello! I'm your AI assistant. How can I help you today?
```

This request took about 3 seconds. When `[Agent]:` is followed by a reply from the model, the whole chain (network, name resolution, TLS, model and Agent) works.

## VI. Troubleshooting with the Log

The message the Agent gives you does not always show the real cause. When something fails, read the log lines before it:

| What the log shows | Cause and what to do |
| ------------------ | -------------------- |
| `API error 401`, `Invalid API Key` | The key is invalid, or the key does not match the address. Check the key for typos. A Token Plan key needs its dedicated address. |
| `API error 404`, saying the model does not exist | The model name is wrong. Compare it with the model names in the console. |
| `API error 429` | The quota or the request rate is exceeded. |
| `net_connect <domain>:443 ret=0x52` | The domain name cannot be resolved: the board is not on the network or has no DNS. Go back to [Section IV](#iv-flash-and-connect-to-the-network), and use `ifconfig` to check whether `wlan0` has an address. |
| The Agent replies "请求超时，LLM 响应时间过长" (request timed out) | It may not be a real timeout. See "System time" below. |
| The Agent replies `Sorry, I encountered an error.` | It gives no reason. Read the `API error` or other log lines before it. |
| `[weixin] No token, waiting...` every 5 seconds | The WeChat channel is on but not configured. You can ignore it. It only floods the screen. |

### System time

Before the TLS handshake, the Agent checks the system time. If the time is earlier than 2024 (the board shows 1970 until it gets the time from the network), it sets the system clock to 28 February 2026. So the timestamps in the log suddenly jump to `26/02/28`, which is not the real date.

The jump also affects the timeout check. From the log, the Agent computes the request time from the clock before and after the jump, which differs by decades, and so it reports "request timed out" although the request failed immediately for another reason. When you see this message, first look for a `net_connect` or `API error` line before it.

The NTP service starts at boot, before the Wi-Fi connection. We have not verified whether the system time is corrected automatically after the board gets online.

## VII. What Has Not Been Verified

We have not verified the following on the MIBOX-X1 board. Do not treat them as working features:

- Voice: recording, playback, speech recognition and synthesis. The Gemini-S1 board has an audio configuration adjusted for ai_agent. We did not do this for the MIBOX-X1.
- The Feishu, WeChat and MQTT channels, and Node and MCP. They are on by default, but we did not configure or test them.
- Tool calls. We only tested plain chat (`tool_use=0`). We did not test the Agent calling its built-in tools (file access, web search, scheduled tasks and so on).
- Whether the model setting is kept after a power cycle.
- Memory usage.
- 5 GHz Wi-Fi networks.
