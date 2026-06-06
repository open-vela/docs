# openvela 快应用调用 velaclaw（端侧 AI Agent）教程

> 本教程面向 openvela AI 硬件大赛参赛者，介绍如何在快应用中通过 `@system.velaclaw` 调用端侧 AI Agent 能力（如自然语言问答），实现从环境配置、编译、部署到调用的完整流程。

## 一、简介

`velaclaw` 是 openvela 提供的一个快应用 feature，它让快应用（JS 应用）可以直接调用端侧 **ai_agent** 的能力。通过 `@system.velaclaw`，你的快应用只需几行代码就能向 AI 提问并获得回复（例如「北京今天天气怎么样」），无需自己实现对话通道。

**适用场景**：语音助手、智能问答、信息查询等需要 AI 对话能力的快应用。

**最终效果**：快应用调用 `velaclaw.ask()` 发送问题，AI Agent 处理后返回回复，并在应用中展示。

## 二、前置条件

开始前，请先完成以下环境准备：

- 快应用开发与运行环境，请参见[快应用开发指南（AI 工作流）](./quickapp_ai_workflow.md)。
- 一个可用的大模型 API（本教程以 **Xiaomi MiMo** 为例，其他兼容的大模型亦可）。

> 本教程以 `vela_goldfish-arm64-v8a-ap` 模拟器为例进行说明。

## 三、开启所需配置

在 openvela 模拟器编译环境中，通过 `menuconfig` 确保开启以下配置项。配置分为「快应用环境」与「velaclaw feature」两组：

### 1、快应用环境配置

```
CONFIG_FEATURE_FRAMEWORK=y       # 启用 Feature Framework
CONFIG_INTERPRETERS_QUICKJS=y    # 启用 QuickJS 解释器
CONFIG_LIBASH=y                  # 启用 libash 库
CONFIG_LIBUV_EXTENSION=y         # 启用 libuv 扩展
CONFIG_LIB_YOGA=y                # 启用 Yoga 布局库
CONFIG_LV_USE_QRCODE=y           # 启用 LVGL 二维码支持
CONFIG_LV_USE_VECTOR_GRAPHIC=y   # 启用 LVGL 矢量图形
CONFIG_PROTOBUF_C=y              # 启用 protobuf-c
CONFIG_QUICKAPP=y                # 启用快应用框架
CONFIG_QUICKAPP_LOG_LEVEL=0      # 快应用日志级别（0=DEBUG 1=INFO 2=WARNING 3=ERROR 4=ALERT 5=OFF）
CONFIG_QUICKAPP_VAPP=y           # 启用快应用 VAPP
CONFIG_SYSLOG_CONSOLE=y          # 启用 syslog 控制台输出
CONFIG_UTILS_CURL=y              # 启用 curl 工具
```

### 2、velaclaw feature 配置

```
CONFIG_EXAMPLES_AI_AGENT_VELA=y      # 启用 ai_agent 示例
CONFIG_FEATURE_SYSTEM_VELACLAW=y     # 启用 velaclaw feature
CONFIG_MQ_MAXMSGSIZE=4096            # 消息队列最大消息大小设为 4096
```

## 四、编译

在 openvela 工程根目录执行编译（以 goldfish 模拟器为例）：

```bash
# 进入 menuconfig 调整配置（按需）
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap --cmake -j8 menuconfig

# 编译
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap --cmake -j8
```

其他常用命令：

```bash
# 保存当前配置到 defconfig
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap --cmake -j8 savedefconfig

# 清理
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap --cmake -j8 distclean
```

## 五、运行与部署

### 1、启动模拟器

```bash
./emulator.sh cmake_out/vela_goldfish-arm64-v8a-ap/
```

`emulator.sh` 会占用当前终端，请**另开一个终端**执行后续 `adb` 命令。

### 2、推送字体与应用包

本节以示例应用包 `com.application.lyra.demo.debug.1.0.0.rpk` 为例（请替换为你自己应用的 rpk 文件名，包名需与 `manifest.json` 中的 `package` 字段一致）。`rpk` 是快应用的安装包，本质为 zip 包，可解压后推送到设备运行。

> 附件下载：[示例 RPK 应用包](attachment/com.application.lyra.demo.debug.1.0.0.rpk) | [字体包 font.zip](attachment/font.zip)

```bash
# 1. 解压字体包
unzip font.zip -d font

# 2. 推送字体
adb push ./font /data/

# 3. 解压 rpk（rpk 本质是 zip 包）
unzip com.application.lyra.demo.debug.1.0.0.rpk -d com.application.lyra.demo

# 4. 推送应用（目标路径必须包含完整包名）
adb push com.application.lyra.demo /data/app/com.application.lyra.demo
```

### 3、连接网络

goldfish 模拟器通过虚拟以太网（eth0）自动获得网络连接，**无需手动配置，此步骤可跳过**。`ai_agent` 启动时会自动执行 `ifup eth0`。

以下 WiFi 配置命令仅适用于带 WiFi 模块的真机开发板，模拟器中执行会提示 Failed：

```bash
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <password> 3
wapi essid wlan0 <ssid> 1
renew wlan0
```

### 4、配置大模型（LLM）

先以前台方式启动 ai_agent，在 `vela>` 提示符下完成大模型配置：

```bash
ai_agent
```

等待出现 `vela>` 提示符后，输入以下命令配置大模型：

**方式一：Token Plan 套餐用户（tp- 开头的 key，大赛发放）**

```bash
set_llm https://token-plan-cn.xiaomimimo.com/v1 <model> tp-你的套餐KEY
```

**方式二：按量付费用户（sk- 开头的 key）**

```bash
set_llm https://api.xiaomimimo.com/v1 <model> sk-你的API_KEY
```

> `<model>` 请填写你的账户支持的模型名称，具体值请参考 [MiMo 官方文档](https://platform.xiaomimimo.com/docs/zh-CN/integration/claudecode) 或 [订阅管理](https://platform.xiaomimimo.com/console/token-plan) 页面。提示：在 `vela>` 下输入 `set_llm`（不带参数）可查看完整用法说明。

**配置搜索 Key（可选，不配也能正常使用）**：如果你的应用需要 AI 回答实时信息（如天气、新闻等），需要配置 Tavily 搜索 API Key，让 ai_agent 具备联网搜索能力。不需要实时搜索功能的应用可跳过此步。

```bash
set_tavily_key <your_tavily_key>
```

> Tavily Key 需自行到 https://tavily.com 注册获取。

配置完成后，按 `Ctrl+C` 退出 ai_agent，回到 `goldfish-armv8a-ap>` 提示符。

### 5、后台启动 ai_agent 并运行快应用

将 ai_agent 以后台方式重新启动，然后启动快应用：

```bash
ai_agent &
vapp hap://app/com.application.lyra.demo
```

## 六、在快应用中调用 velaclaw

上面运行的是示例应用。如果你要在自己的快应用中使用 velaclaw，核心调用方式如下（该调用代码属于应用源码，需在编译打包前写入你的快应用工程）：

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

- `query`：要向 AI 提出的问题。
- `success`：成功回调，`res.reply` 为 AI 的回复内容。
- `fail`：失败回调，`code` 为错误码。
- `complete`：调用结束回调（无论成功失败都会触发）。

## 七、运行效果

示例演示录屏：

<video src="attachment/录屏 2026年05月27日 15时57分03秒.webm" controls></video>

## 八、常见问题

- **快应用启动后无 AI 回复**：确认 `ai_agent` 已在后台运行（`ai_agent &`），且已通过 `set_llm` 正确配置大模型。
- **联网类问答失败**：确认网络可用，并已配置 `set_tavily_key`（如需联网搜索）。
- **应用无法加载**：确认应用包已推送到 `/data/app/包名/`，且包名与 `manifest.json` 中的 `package` 字段一致。

## 九、提交参赛代码

请参见[快应用开发指南（AI 工作流）](./quickapp_ai_workflow.md)。

## 十、相关仓库

- [packages_ai_agent](https://github.com/open-vela/packages_ai_agent/tree/dev-ai-contest-2026)
- [frameworks_runtimes_feature](https://github.com/open-vela/frameworks_runtimes_feature/tree/dev-ai-contest-2026)
- [goldfish ARM64 模拟器 ai_agent 与快应用 velaclaw 集成指南](https://github.com/open-vela/packages_ai_agent/tree/dev-ai-contest-2026/defconfigs/goldfish-arm64-v8a-ap)
