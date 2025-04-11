<div align="center">
  <img src="./images/openvela.svg" width="180" />
</div>

<h1 align="center">openvela</h1>

\[ [English](README.md) | [简体中文](README_zh-cn.md) | 繁體中文 \]

## openvela 簡介

openvela 作業系統專為 AIoT 領域量身打造，專注在輕量化、符合標準、安全性及高度可擴充性。openvela 已成為數百萬物聯網裝置和人工智慧裝置的首選技術，包括智慧手錶、健身手環、智慧音箱、耳機、智慧家電和機器人等多個領域。

Vela 這個名字源自於拉丁語【帆】，也是南方天空中形似船帆的星座名稱。我們渴望與開發者合作，在 AIoT 領域揚帆起航。

## openvela 特色

- **高度可擴展性**：openvela 的設計著重於模組化與可擴充性，讓其能夠靈活適應多樣的物聯網應用場景。最低只需要 8KB RAM 的微型 BLE 模组，最大更可以來到 512MB RAM 帶有螢幕的智慧音箱，openvela 讓設備擁有高度的擴展性。

- **一站式解决方案**：多年來，openvela 已發展成為一個強大的平台，具有完整的軟體平台，使其成為各種物聯網應用的一站式解決方案。我們不斷融入新功能以滿足新興需求。透過利用 openvela，製造商可以大幅降低研發成本並加快產品開發週期。

- **成熟的異構計算支援**：openvela 為不同的架構及核心系統提供強大的支援，具有 MCU、MPU、DSP、GPU 和 NPU 等各種處理單元之間的無縫 IPC 機制。此外，openvela 在 openvela、Linux 和 Android 系統之間提供了先進的 RPC 框架，從而實現利用三種系統優勢的混合作業系統。

- **符合標準且可移植性高**：openvela 核心建立在 Apache NuttX 之上，通常被稱為「微型 Linux」。在此基礎上，openvela 實現了與 POSIX 標準的高度一致。我們的團隊一直在不斷增強其 POSIX 相容性，目前已達到令人印象深刻的 88%。由於符合此標準，在其他標準作業系統（例如 Linux）下開發的軟體可以輕鬆移植到 openvela。

- **完整的連接套件**：openvela 提供廣泛的協定支持，包括藍牙 BR/EDR/LE、LE Mesh、WiFi、Matter、IEEE802.15.4、LTE Cat1、乙太網路、CAN/LIN 等。

- **豐富的開發者工具**：openvela 提供了一系列完整的開發者工具，包括系統監控、效能分析、偵錯工具、trace、閃退分析和 log 分析工具，為開發者提供強大的資源。

## 硬體支援

openvela 支援許多不同的架構（ARM32、ARM64、RISC-V、Xtensa、MIPS、CEVA 等）和硬體平台。請在[硬體支援](https://nuttx.apache.org/docs/latest/platforms/index.html)頁面中查詢完整的列表。

## 快速入門

如果您想要體驗 openvela，我們提供一個功能完整的模擬器，不需要硬體即可使用。詳細資訊請參考下方指南。

1. [準備開發環境](./zh-cn/quickstart/Set_up_the_development_environment_zh-cn.md)
2. [下载 openvela 原始碼](./zh-cn/quickstart/Download_Vela_sources_zh-cn.md)
3. [編譯 openvela 原始碼](./zh-cn/quickstart/Build_Vela_from_sources_zh-cn.md)
4. [在模擬器上執行並編譯程式](./zh-cn/quickstart/Run_Vela_on_Vela_Emulator_zh-cn.md)

## 子倉庫清單

| 子倉庫連結                                     | 描述                                                                                                                                                                                                                                                                            |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [frameworks](../../../../open-vela/frameworks) | openvela 服務框架：主要包含藍芽、電話、圖形、多媒體、應用框架、安全、系統服務框架（KVDB、OTA、healthd、binder、charger 等）。                                                                                                                                                   |
| [vendor](../../../../open-vela/vendor)         | 晶片原廠的驅動和框架。                                                                                                                                                                                                                                                          |
| [nuttx](../../../../open-vela/nuttx)           | 基於開源的 RTOS NuttX 打造的內核，提供基礎的核心功能，包括任務調度、跨進程通訊、檔案系統、TCP/IP 協定堆疊、裝置驅動和電源管理等，同時對上提供標準的 POSIX 接口。如果您想要對 NuttX 操作系統有更深的了解，可以在 [Apache NuttX](https://nuttx.apache.org/) 官網查看更多資訊。 |
| [apps](../../../../open-vela/apps)             | `apps` 是開源即時作業系統（NuttX）的應用程式庫，包含了一系列為 NuttX RTOS 設計的應用程式和實用工具。這些應用程式和工具包括 shell 命令列工具、檔案系統工具、網路工具等，它們可以幫助開發者更方便地開發和偵錯基於 NuttX RTOS 的嵌入式系統。                                       |
| [external](../../../../open-vela/external)     | openvela 引入的第三方程式庫。                                                                                                                                                                                                                                                         |
| [tests](../../../../open-vela/tests)           | 該倉庫包含接口測試，具體包括多媒體、文件系統、記憶體管理和 socket 通訊等核心 API 的測試。                                                                                                                                                                                         |
| [docs](../../../../open-vela/docs)             | openvela 對應的開發者文件。                                                                                                                                                                                                                                                     |

## 範例

- [音樂播放器](./zh-cn/demo/Music_Player_Example_zh-cn.md)
- [智慧手環](./zh-cn/demo/Smart_Band_Example_zh-cn.md)
- [自行車碼錶](./zh-cn/demo/X_Track_zh-cn.md)

## 貢獻

- [原始碼貢獻指南](CONTRIBUTING_zh-tw.md)
- [文件貢獻指南](./zh-cn/contribute/process/doc_dev_process.md)

## 授權

這個代碼庫中的代碼使用 Apache 2.0 授權。你可以在[這裡](https://www.apache.org/licenses/LICENSE-2.0.txt)找到更多關於 Apache 2.0 授權的資訊。

openvela 引用第三方開源軟體及授權說明，參考[第三方開源軟體說明](Third_Party_and_Open_Source_Components_zh-tw.md)。

## 聯絡方式

為了更好的管理和處裡回饋及技術支援，建議通過以下方式聯絡我們：

- **Issues**: 如果你有任何問題、建議或是發現任何的 Bug，請在 Issues 頁面中發起一個新的 Issue。盡可能提供詳細的資訊，讓我們能更快的釐清問題並解決。
- **Pull Requests**: 如果你發現問題並修復了，歡迎發起 Pull Request。請確認依照我們的[貢獻指南](./CONTRIBUTING_zh-tw.md)。
- **Discussions**: 如果你有更多的想法，可以在 Discussions 頁面發起一個新的討論。
