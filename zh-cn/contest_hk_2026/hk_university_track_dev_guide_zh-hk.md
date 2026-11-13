# 香港高校組 openvela 開發指南
\[ [English](../../en/contest_hk_2026/hk_university_track_dev_guide.md) | [简体中文](./hk_university_track_dev_guide.md) | 繁體中文 \]

> 本文面向《三十港章 慧智北都》AIoT 比賽高校組、使用 openvela 的參賽隊伍，只介紹技術內容：該選哪種開發環境、怎麼準備電腦和代碼、兩種應用怎麼開發、怎麼接入 AI。
>
> 開發板的具體用法見 [R528 MIBOX-X1 開發板使用指南](./mibox_x1_board_guide_zh-hk.md)。

## 一、三種開發環境

作品可以在開發板上做，也可以只在模擬器上做。三種環境的區別如下：

| 環境                  | 能做什麼                                                                                                         | 做不了什麼                                                     | 適合                             |
| --------------------- | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------- |
| R528 MIBOX-X1 開發板  | 命令行、LVGL 界面、全部板載外設（按鍵、LED、觸摸屏、音頻、紅外、藍牙、Wi-Fi、九軸傳感器、SD 卡）、排針接外部器件 | `nsh` 配置已啟用 JS 應用運行時（QuickJS），但沒有包含 ai_agent | 需要硬件的作品                   |
| openvela 模擬器       | 命令行、LVGL 界面、JS 應用、ai_agent（模擬器自帶網絡），JS 應用調用 AI                                           | 沒有 GPIO、傳感器、紅外、藍牙等硬件                            | 沒有開發板，或只做界面和 AI      |
| AIoT-IDE 自帶的模擬器 | 編寫、預覽、調試 JS 應用，不需要每次重新編譯系統                                                                 | 不是 openvela 系統，行為與真實系統有差異                       | 只做 JS 應用，需要快速修改和預覽 |

用 JS 應用做的作品，提交前建議再到 openvela 模擬器上運行驗證一遍，詳見[快應用開發指南](../app_dev/quickapp/quickapp_manual.md)第四章。

## 二、準備電腦

- 系統：Ubuntu 22.04。
- 配置：官方要求至少 16GB 內存、40GB 可用硬盤。用虛擬機的話，內存不足時編譯會很慢，可以把並行數調小，例如 `-j4`。
- [快應用開發指南（AI 工作流）](../app_dev/quickapp/quickapp_ai_workflow.md)説明不支持 WSL 和 Docker。
- 依賴包、`repo` 和 `git-lfs` 的安裝步驟見[快速入門（Ubuntu）](../quickstart/openvela_ubuntu_quick_start.md)。
- 燒錄開發板用的工具（PhoenixSuit 和驅動）在 Windows 上運行。只有 Ubuntu 的話，需要另一台 Windows 電腦做燒錄，細節見開發板使用指南第四節。

## 三、獲取代碼

統一使用 `dev-ai-contest-2026` 分支，不要用 `dev` 或 `trunk`：

```bash
mkdir openvela && cd openvela
repo init -u https://github.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs
repo sync -c -j4
```

第一次同步要下載很多內容，網絡不好時耗時較長。中斷後重新執行 `repo sync -c -j4` 會接着下載。

## 四、用開發板開發

編譯、打包、燒錄、外設測試和第一個應用，按[開發板使用指南](./mibox_x1_board_guide_zh-hk.md)操作。板子對應的板級目錄是 `vendor/allwinnertech/boards/r528/r528s3-mibox-x1`，默認使用 `nsh` 配置。

## 五、用模擬器開發

編譯並啟動 openvela 模擬器：

```bash
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake -j$(nproc)
./emulator.sh cmake_out/vela_goldfish-arm64-v8a-ap/
```

看到 `goldfish-armv8a-ap>` 提示符就説明啟動成功。模擬器默認帶網絡，不需要配置 Wi-Fi。

要在模擬器裏使用 ai_agent，需要換成 ai_agent 的模擬器配置並重新編譯，步驟見 [ai_agent 應用開發上手指南](../edge_ai_dev/ai_agent/ai_agent_quickstart.md)第六章「QEMU 模擬器」一節。

## 六、兩種應用形態

JS 應用在官方文檔中叫「快應用」。

|          | 原生應用（C + LVGL）                                                                                                | JS 應用                                                  |
| -------- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 開發方式 | 用 C 語言開發，編進系統固件                                                                                         | 用 JS 開發，在 AIoT-IDE 裏編寫和預覽                     |
| 運行在   | 開發板、模擬器                                                                                                      | 開發板（運行時已啟用）、模擬器                           |
| 控制硬件 | 可以，直接使用板載外設和排針                                                                                        | 以界面和系統能力為主                                     |
| 接入 AI  | 調用 ai_agent，入口是 `velaclaw_client_open()`                                                                      | 調用 `@system.velaclaw`                                  |
| 參考     | [mini_memo 應用介紹](../edge_ai_dev/ai_agent/mini_memo_guide.md)、[開發板使用指南第六節](./mibox_x1_board_guide_zh-hk.md) | [快應用開發指南](../app_dev/quickapp/quickapp_manual.md) |

## 七、接入 AI

ai_agent（openvelaClaw）需要一個大模型 API Key，申請見 [ai_agent 應用開發上手指南](../edge_ai_dev/ai_agent/ai_agent_quickstart.md)第一章，配置見第二章。

- **原生應用**：用 `velaclaw_client_open("應用名")` 連接 openvelaClaw，再調用大模型。完整例子見 [mini_memo 應用介紹](../edge_ai_dev/ai_agent/mini_memo_guide.md)第二章。
- **JS 應用**：用 `@system.velaclaw`，例如：

  ```javascript
  import velaclaw from '@system.velaclaw'

  velaclaw.ask({
    query: '北京今天天氣怎麼樣',
    success: function (res) { console.log('AI reply:', res.reply) },
    fail: function (data, code) { console.log('fail, code:', code) }
  })
  ```

  詳細教程見[快應用調用端側 AI Agent 教程](../app_dev/quickapp/quickapp_velaclaw.md)。

目前官方配置中，只有 goldfish 模擬器的 ai_agent 配置同時包含 JS 應用和 ai_agent，所以 JS 應用調用 AI 請先在模擬器上開發。開發板的 `nsh` 配置沒有包含 ai_agent，在板子上做 AI 對話需要自己調整配置，參考 [ai_agent 應用開發上手指南](../edge_ai_dev/ai_agent/ai_agent_quickstart.md)第六章「添加新開發板」一節。

## 八、文檔索引

- [R528 MIBOX-X1 開發板使用指南](./mibox_x1_board_guide_zh-hk.md)
- [快速入門（Ubuntu）](../quickstart/openvela_ubuntu_quick_start.md)
- [ai_agent 應用開發上手指南](../edge_ai_dev/ai_agent/ai_agent_quickstart.md)
- [mini_memo 應用介紹](../edge_ai_dev/ai_agent/mini_memo_guide.md)
- [快應用開發指南](../app_dev/quickapp/quickapp_manual.md)
- [快應用調用端側 AI Agent 教程](../app_dev/quickapp/quickapp_velaclaw.md)
- [芯片移植指南](../chip_porting/porting_guide.md)
