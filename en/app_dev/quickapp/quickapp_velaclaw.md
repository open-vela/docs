# Calling the On-Device AI Agent from a Quick App (@system.velaclaw)

\[ English | [简体中文](../../../zh-cn/app_dev/quickapp/quickapp_velaclaw.md) \]

> This tutorial shows how to call on-device AI Agent capabilities (such as natural-language Q&A) from a quick app through `@system.velaclaw`, covering the whole flow from environment configuration, building and deployment to the actual call.

## I. Introduction

`velaclaw` is a quick app feature provided by openvela. It lets a quick app (a JS app) call the capabilities of the on-device **ai_agent** directly. With `@system.velaclaw`, a few lines of code are enough for your quick app to ask the AI a question and get a reply (for example, "What's the weather like in Beijing today?"), without implementing a conversation channel yourself.

**Use cases**: voice assistants, smart Q&A, information lookup and other quick apps that need AI conversation.

**End result**: the quick app calls `velaclaw.ask()` to send a question, the AI Agent processes it and returns a reply, and the app displays it.

## II. Prerequisites

Before you start, prepare the following:

- A quick app development and runtime environment. See [Quick App Development Guide (AI Workflow)](./quickapp_ai_workflow.md).
- A working LLM API (this tutorial uses **Xiaomi MiMo** as the example; other compatible LLMs also work).

> This tutorial uses the `vela_goldfish-arm64-v8a-ap` emulator as the example.

## III. Enabling the Required Configuration

In the openvela emulator build environment, make sure the following options are enabled through `menuconfig`. They fall into two groups, "quick app environment" and "`velaclaw` feature":

### 1. Quick App Environment Configuration

```
CONFIG_FEATURE_FRAMEWORK=y       # Enable the Feature Framework
CONFIG_INTERPRETERS_QUICKJS=y    # Enable the QuickJS interpreter
CONFIG_LIBASH=y                  # Enable the libash library
CONFIG_LIBUV_EXTENSION=y         # Enable the libuv extension
CONFIG_LIB_YOGA=y                # Enable the Yoga layout library
CONFIG_LV_USE_QRCODE=y           # Enable LVGL QR code support
CONFIG_LV_USE_VECTOR_GRAPHIC=y   # Enable LVGL vector graphics
CONFIG_PROTOBUF_C=y              # Enable protobuf-c
CONFIG_QUICKAPP=y                # Enable the quick app framework
CONFIG_QUICKAPP_LOG_LEVEL=0      # Quick app log level (0=DEBUG 1=INFO 2=WARNING 3=ERROR 4=ALERT 5=OFF)
CONFIG_QUICKAPP_VAPP=y           # Enable quick app VAPP
CONFIG_SYSLOG_CONSOLE=y          # Enable syslog console output
CONFIG_UTILS_CURL=y              # Enable the curl utility
```

### 2. `velaclaw` Feature Configuration

```
CONFIG_EXAMPLES_AI_AGENT_VELA=y      # Enable the ai_agent example
CONFIG_FEATURE_SYSTEM_VELACLAW=y     # Enable the velaclaw feature
CONFIG_MQ_MAXMSGSIZE=4096            # Set the maximum message queue message size to 4096
```

## IV. Building

Build from the root of the openvela project (using the goldfish emulator as the example):

```bash
# Open menuconfig to adjust the configuration (as needed)
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap --cmake -j8 menuconfig

# Build
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap --cmake -j8
```

**Clean before rebuilding after a configuration change**: after you change the configuration through `menuconfig` (or edit the defconfig), clear the build cache before building. Otherwise the openvela CMake cache keeps the old configuration and the newly enabled options don't take effect:

```bash
rm -rf cmake_out/vela_goldfish-arm64-v8a-ap
```

Other common commands:

```bash
# Save the current configuration to the defconfig
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap --cmake -j8 savedefconfig

# Clean
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap --cmake -j8 distclean
```

## V. Running and Deployment

### 1. Start the Emulator

```bash
./emulator.sh cmake_out/vela_goldfish-arm64-v8a-ap/
```

`emulator.sh` occupies the current terminal, so **open another terminal** for the `adb` commands that follow.

### 2. Push the Fonts and the App Package

This section uses the sample app package `com.application.lyra.demo.debug.1.0.0.rpk` as the example (replace it with your own app's rpk file name; the package name must match the `package` field in `manifest.json`). An `rpk` is a quick app installation package. It is essentially a zip file, so you can extract it and push it to the device to run.

> Attachment downloads: [Sample RPK app package](../../../zh-cn/app_dev/quickapp/attachment/com.application.lyra.demo.debug.1.0.0.rpk) | [Font package font.zip](../../../zh-cn/app_dev/quickapp/attachment/font.zip)

Run the following commands in **another terminal on the host** (not at the emulator's `goldfish-armv8a-ap>` prompt, and not at `vela>`), because `emulator.sh` from Step 1 already occupies the first terminal. Make sure **the current terminal is at the root of the openvela project**; step 0 below switches to the attachment directory:

```bash
# 0. Switch to the directory with font.zip and the .rpk (shipped with the repository; run from the openvela project root)
cd docs/zh-cn/app_dev/quickapp/attachment

# 1. Extract the font package (don't add -d font: font.zip already contains a font/ directory; an extra level nests it twice, so the font path ends up wrong and Chinese text renders as boxes □)
unzip font.zip

# 2. Push the fonts
adb push ./font /data/

# 3. Extract the rpk (an rpk is essentially a zip file)
unzip com.application.lyra.demo.debug.1.0.0.rpk -d com.application.lyra.demo

# 4. Push the app (the target path must include the full package name)
adb push com.application.lyra.demo /data/app/com.application.lyra.demo
```

### 3. Connect to the Network

The goldfish emulator gets a network connection automatically through a virtual Ethernet interface (eth0). **No manual configuration is needed, so you can skip this step.** `ai_agent` runs `ifup eth0` automatically when it starts.

The WiFi commands below are entered in the emulator's NSH terminal (the `goldfish-armv8a-ap>` prompt) and only apply to real development boards with a WiFi module. In the goldfish emulator they report Failed, so just skip this step:

```bash
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <password> 3
wapi essid wlan0 <ssid> 1
renew wlan0
```

### 4. Configure the LLM

Enter the following commands in the emulator's NSH terminal (the `goldfish-armv8a-ap>` prompt that appears after you start the emulator in Step 1). First start ai_agent in the foreground, then configure the LLM at the `vela>` prompt:

```bash
ai_agent
```

Once the `vela>` prompt appears, enter the following command to configure the LLM:

**Option 1: Token Plan subscribers (keys starting with tp-)**

```bash
set_llm https://token-plan-cn.xiaomimimo.com/v1 <model> tp-YOUR_TOKEN_PLAN_KEY
```

**Option 2: pay-as-you-go users (keys starting with sk-)**

```bash
set_llm https://api.xiaomimimo.com/v1 <model> sk-YOUR_API_KEY
```

> For `<model>`, fill in a model name your account supports. See the [MiMo official documentation (Chinese)](https://platform.xiaomimimo.com/docs/zh-CN/integration/claudecode) or the [subscription management](https://platform.xiaomimimo.com/console/token-plan) page for the exact values. Tip: enter `set_llm` with no arguments at `vela>` to see the full usage.

All settings (`set_llm`, `set_tavily_key` and so on) are **persisted automatically in the device's `/data/ai_agent/config/` directory** and loaded again after the ai_agent process or the virtual machine restarts, so you don't have to configure them again. They are lost only when you **run a clean build again** (which regenerates `vela_data.bin` and discards `userdata-qemu.img`), reflash the firmware or wipe the `/data` partition; in that case, set them once more at `vela>`. Use `config_show` at `vela>` to see the current settings (keys are shown masked).

**Configure a search key (optional; everything works without it)**: the LLM (the one configured with `set_llm`) can only answer questions within its training knowledge and **can't get real-time information** (such as weather, news or stock prices). If your app needs to answer such questions, also configure a Tavily search API key. **Tavily is a web search service built for AI.** Once it is configured, ai_agent can search the web before answering and let the LLM answer based on the search results. Apps that only do ordinary conversation and don't need real-time information can skip this step.

```bash
set_tavily_key <your_tavily_key>
```

> Register at https://tavily.com to get a Tavily key.

When the configuration is done, press `Ctrl+C` to exit ai_agent and return to the `goldfish-armv8a-ap>` prompt.

### 5. Start ai_agent in the Background and Run the Quick App

Restart ai_agent in the background, then start the quick app:

```bash
ai_agent &
vapp hap://app/com.application.lyra.demo
```

## VI. Calling `velaclaw` from a Quick App

> The [Xiaomi Vela official documentation: system.velaclaw (Chinese)](https://iot.mi.com/vela/quickapp/zh/features/other/velaclaw.html) is the authoritative interface specification. This section shows the common ways to call it.

What you ran above is the sample app. To use `velaclaw` in your own quick app, the core call looks like this (this code is part of the app source, so add it to your quick app project before building and packaging):

```javascript
import velaclaw from '@system.velaclaw'

velaclaw.ask({
  query: '北京今天天气怎么样',
  success: function(res) {
    console.log('AI reply:', res.reply)
  },
  fail: function(data, code) {
    console.log('fail, code:', code)
  },
  complete: function() {
    console.log('complete')
  }
})
```

- `query`: the question to ask the AI.
- `success`: success callback; `res.reply` holds the AI's reply.
- `fail`: failure callback; `code` is the error code.
- `complete`: called when the call ends (fires on both success and failure).

Promise-style calls are also supported:

```javascript
const res = await velaclaw.ask({ query: '今天天气怎么样' })
console.log('AI reply:', res.reply)
```

**Error codes:**

| code | Description                                           |
| ---- | ----------------------------------------------------- |
| 200  | General system error                                  |
| 202  | Invalid parameter (query missing or of wrong type)    |
| 203  | Not supported (the device has no AI capability)       |
| 204  | Request timeout (the AI Agent timed out)              |
| 1000 | AI service unavailable                                |
| 1001 | Conversation content rejected (content safety policy) |

## VII. FAQ

- **No AI reply after the quick app starts**: make sure `ai_agent` is running in the background (`ai_agent &`) and the LLM is configured correctly with `set_llm`.
- **Questions that need the network fail**: make sure the network is available and `set_tavily_key` is configured (if web search is needed).
- **The app doesn't load**: make sure the app package was pushed to `/data/app/<package name>/` and the package name matches the `package` field in `manifest.json`.

## VIII. Related Repositories

- [packages_ai_agent](../../../../../../packages_ai_agent/tree/dev-ai-contest-2026)
- [frameworks_runtimes_feature](../../../../../../frameworks_runtimes_feature/tree/dev-ai-contest-2026)
- [Integration guide for ai_agent and the quick app velaclaw feature on the goldfish ARM64 emulator](../../../../../../packages_ai_agent/tree/dev-ai-contest-2026/defconfigs/goldfish-arm64-v8a-ap)
