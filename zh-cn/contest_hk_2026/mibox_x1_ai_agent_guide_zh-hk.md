# 在 R528 MIBOX-X1 上運行 AI Agent（實驗）
\[ [English](../../en/contest_hk_2026/mibox_x1_ai_agent_guide.md) | [简体中文](./mibox_x1_ai_agent_guide.md) | 繁體中文 \]

> 本文介紹怎樣編譯一份帶 ai_agent 的 R528 MIBOX-X1 固件，燒錄後讓開發板聯網，設置大模型，並在串口裏和 Agent 對話。這是一篇實驗性質的指南：默認的 `nsh` 配置不帶 ai_agent，需要自己新建配置並編譯固件。我們在開發板上驗證過文字對話，語音等功能沒有驗證，見[第七節](#七沒有驗證的內容)。

## 一、開始之前

默認的 `nsh` 配置不包含 ai_agent。本文在 `nsh` 的基礎上多開 ai_agent 和它依賴的幾項配置，做成一個新配置 `nsh_agent`。

開始之前需要：

- 已經能按[開發板使用指南](./mibox_x1_board_guide_zh-hk.md)編譯、燒錄 `nsh` 固件。
- 已經能按[連接開發板指南](./mibox_x1_connect_guide_zh-hk.md)用串口連上開發板，並連接 Wi-Fi。
- 一個大模型的 API key（自己申請）。本文以小米 MiMo 的 Token Plan 為例，其他平台的做法相同。

## 二、新建 nsh_agent 配置

在 SDK 根目錄執行：

```bash
cd vendor/allwinnertech/boards/r528/r528s3-mibox-x1/configs
cp -r nsh nsh_agent
```

然後編輯 `nsh_agent/defconfig`：

1. 刪除這一行：

   ```text
   # CONFIG_MBEDTLS_NET_C is not set
   ```

   Agent 用 mbedTLS 的網絡接口連接大模型服務器，這一項必須打開。刪除這一行後，編譯時它會被打開，我們編譯後確認過最終配置裏是 `CONFIG_MBEDTLS_NET_C=y`。
2. 在文件末尾追加這五行：

   ```text
   CONFIG_EVENT_FD=y
   CONFIG_EXAMPLES_AI_AGENT_VELA=y
   CONFIG_NETUTILS_WEBCLIENT=y
   CONFIG_OPENSSL_MBEDTLS_WRAPPER=y
   CONFIG_SYSTEM_POPEN=y
   ```

   其中 `CONFIG_EXAMPLES_AI_AGENT_VELA` 是 ai_agent 本體，命令名是 `ai_agent`；其餘四項是它依賴的組件。

這樣得到的配置，和我們編譯驗證用的配置完全一致。

## 三、編譯和打包

`m nsh` 命令只會編譯 `nsh` 配置，所以編譯 `nsh_agent` 要直接調用 `build.sh`：

```bash
cd vendor/allwinnertech/lichee
source envsetup.sh
lunch_nuttx r528s3-mibox-x1
cd ../../..
./build.sh vendor/allwinnertech/boards/r528/r528s3-mibox-x1/configs/nsh_agent/ -e -Wno-error -j$(nproc)
cd vendor/allwinnertech/lichee
pack
```

- 在 24 核的開發機上，編譯加打包約 4 分鐘。
- `pack` 結束時命令的返回值可能不是 0。請以輸出裏的 `pack finish` 和生成的 `.img` 文件為準。
- 固件文件名和 `nsh` 固件相同：`vendor/allwinnertech/lichee/out/r528s3/mibox-x1_nand/rtos_nuttx_r528s3-mibox-x1_uart0_256Mnand.img`。再編譯一次會覆蓋它，建議編完馬上覆制一份並改個名字，例如加上 `_agent` 後綴。

## 四、燒錄並聯網

1. 按[開發板使用指南](./mibox_x1_board_guide_zh-hk.md)第四節燒錄固件。
2. 按[連接開發板指南](./mibox_x1_connect_guide_zh-hk.md)用串口連上開發板，確認出現 `nsh>`。
3. 連接 Wi-Fi，並確認能 ping 通域名，例如：

   ```text
   nsh> ping api.xiaomimimo.com
   ```

   板子每次上電後都要重新連接 Wi-Fi。要用 2.4 GHz 的網絡。

## 五、設置大模型並提問

在 `nsh>` 提示符下輸入 `ai_agent`，進入 Agent 的命令行，提示符變成 `vela>`：

```text
nsh> ai_agent
vela>
```

### 1、設置大模型

`set_llm` 有兩種寫法：

```text
vela> set_llm <預設名> <key>
vela> set_llm <地址> <模型名> <key>
```

預設名有 `kimi`、`qwen`、`deepseek`、`glm`、`openai`、`openrouter`、`mimo`，各自帶一個默認地址和默認模型。如果你的 key 要用別的地址，就用第二種寫法，把地址寫到 `/v1` 為止，程序會自動補上 `/chat/completions`。

以小米 MiMo 的 Token Plan 為例。Token Plan 的 key 只能用它專屬的地址，不能用 `mimo` 預設（預設用的是 `api.xiaomimimo.com`，用 Token Plan 的 key 會返回 401）：

```text
vela> set_llm https://token-plan-cn.xiaomimimo.com/v1 mimo-v2.6-flash <你的key>
```

- 地址和可用的模型名，請以 MiMo 開放平台控制枱裏 Token Plan 頁面顯示的為準。控制枱裏列出的對話模型有 `mimo-v2.6-pro` 和 `mimo-v2.6-flash`，我們測試用的是 `mimo-v2.6-flash`。名字裏帶 `asr` 的是語音識別模型，帶 `tts` 的是語音合成模型，不是對話模型。
- 設置成功後，日誌裏會顯示 `LLM backend: ...` 和 `API key saved.`。用 `config_show` 可以查看當前配置。

API key 是私人信息。命令會回顯在終端裏，日誌裏也可能出現，截圖或貼日誌給別人之前，請先把 key 遮住。key 不小心泄露後，到平台重置它。

### 2、提問

```text
vela> ask hello
```

聯網和 key 都正確時，幾秒鐘後會看到回覆。下面是一次真實運行的日誌節選（`<…>` 處省略了部分內容）：

```text
[llm] OpenAI API with tools (model: mimo-v2.6-flash, <…> bytes)
[vela_tls] Handshake OK: TLSv1.2 / <…>
[llm] Response: 55 bytes text, 0 tool calls, finish=end_turn
[trace:<…>] iter=0 tool=(none) latency=3015ms llm=ok backend=0
[agent] [Agent]: Hello! I'm your AI assistant. How can I help you today?
```

這次請求耗時約 3 秒。看到 `[Agent]:` 後面是模型的回覆，就説明整條鏈路（聯網、域名解析、TLS、大模型、Agent）都通了。

## 六、看日誌排錯

Agent 給你的提示不一定能説明真實原因，出錯時請看它前面的日誌行：

| 日誌裏的內容 | 原因和處理 |
| ------------ | ---------- |
| `API error 401`，`Invalid API Key` | key 無效，或者 key 和地址不配套。檢查 key 有沒有輸錯，Token Plan 的 key 要用專屬地址 |
| `API error 404`，提示模型不存在 | 模型名寫錯了，核對控制枱裏的模型名 |
| `API error 429` | 額度或請求頻率超限 |
| `net_connect <域名>:443 ret=0x52` | 解析不出域名，板子沒有聯網或沒有 DNS。回到[第四節](#四燒錄並聯網)檢查 Wi-Fi，用 `ifconfig` 看 `wlan0` 有沒有地址 |
| Agent 回覆「請求超時，LLM 響應時間過長」 | 不一定是真的超時，見下面的「系統時間」 |
| Agent 回覆 `Sorry, I encountered an error.` | 沒有説明原因，看它前面的 `API error` 等日誌行 |
| 每隔 5 秒出現 `[weixin] No token, waiting...` | 微信通道已開啟但沒有配置，可以忽略，只是會刷屏 |

### 系統時間

Agent 在 TLS 握手之前會檢查系統時間。如果時間早於 2024 年（板子聯網校時之前顯示的是 1970 年），它會把系統時鐘直接改成 2026 年 2 月 28 日。所以你會看到日誌裏的時間突然跳到 `26/02/28`，這不是真實日期。

時間跳變還會影響超時判斷：從日誌看，Agent 用跳變前後的時間差計算請求耗時，一跳就是幾十年，於是報出「請求超時」，但實際上請求是因為別的原因立即失敗的。遇到這種提示，先看前面有沒有 `net_connect` 或 `API error` 的日誌行。

開機時會啟動 NTP 服務，但它早於 Wi-Fi 連接。聯網之後系統時間能否被自動校準，我們還沒有驗證。

## 七、沒有驗證的內容

以下內容我們沒有在 MIBOX-X1 開發板上驗證過，請不要當作可用的功能：

- 語音：錄音、播放、語音識別和合成。Gemini-S1 開發板為 ai_agent 專門調整過音頻配置，MIBOX-X1 沒有做這一步。
- 飛書、微信、MQTT 通道，以及 Node、MCP。它們默認是開啟的，但我們沒有配置和測試。
- 工具調用。我們只測試了普通對話（`tool_use=0`），沒有測試 Agent 調用內置工具（讀文件、聯網搜索、定時任務等）。
- 重新上電之後，大模型配置是否保留。
- 內存佔用。
- 5 GHz 的 Wi-Fi 網絡。
