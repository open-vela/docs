<div align="center">
  <img src="./images/openvela.svg" width="180" />
</div>

<h1 align="center">openvela</h1>

# openvela 開源項目

\[ [English](README.md) | [简体中文](README_zh-cn.md) | 繁體中文 \]

## openvela 簡介

openvela 操作系統專為 AIoT 領域量身定制，以輕量化、標準兼容、安全性和高度可擴展性為核心特點。openvela 以其卓越的技術優勢，已成為眾多物聯網設備和 AI 硬體的技術首選，涵蓋了智能手錶、運動手環、智能音箱、耳機、智能家居設備以及機器人等多個領域。

Vela 的命名源自拉丁語中船帆的含義，也是南方星空中船帆星座的名字。我們選擇這個名字的意義是希望與開發者一道攜手，共同踏上星辰大海的征途。

## 技術架構

![img](images/001.png)

- **內核層**

    提供基礎的操作系統（OS）功能，包括任務調度、跨行程間通信（IPC）、檔案系統管理。此外，還提供設備驅動、輕量級 TCP/IP 協議棧和電源管理等精簡高效的組件。同時，內核層支援同構多核和異構多核架構，以提升系統在不同架構下的性能支援能力。

- **服務框架層**

    通用的服務框架，專為擴展系統服務設計，包含連接子系統、圖形子系統、多媒體子系統、安全子系統和 XPC 跨核通信能力等。該層提供靈活的服務擴展支援，是系統功能擴展的重要基礎。

- **維測工具**

    常用工具和維測框架，除了常見的 Logger 和 Debugger 工具外，還包含 Emulator 這一強大的高仿真設備模擬器工具。Emulator 支援全面功能仿真，同時支援 CPU 指令集仿真。

    目前模擬器已支援多種產品形態，包括智慧面板、手錶、手環和智能有屏音箱等。通過 Emulator 開發者可以使用 PC 端豐富的調試工具和信息，無需真實設備即可進行應用開發調試，降低開發和調試難度。

## 技術優勢

- **高度可擴展**：openvela 的設計注重模組化與可擴展性，使其能夠靈活適應多樣的物聯網應用場景。小到僅配備 32KB RAM 的微型 BLE 模組，大到擁有 512MB RAM 的智能有屏音箱，openvela 都能提供高度可擴展的支援。

- **一站式解決方案**：隨著時間的推移，openvela 不斷沉澱了各類 AIoT 應用的共性需求，成為一個功能完備的軟體平台，為各類物聯網解決方案提供了全面的支援。廠商採用 openvela，可以顯著降低研發成本並加速產品的上市時間。

- **成熟的異構計算支援**：openvela 為異構多核系統提供了強大的支援，實現了 MCU、MPU、DSP、GPU 以及 NPU 等不同處理單元間無縫的 IPC 通信機制。此外，openvela 還提供了一個高級的 RPC 框架，簡化了 openvela 與 Android 和 Linux 系統的通信，使快速打造一個異構融合操作系統成為可能。

- **標準兼容和高可移植性**：openvela 內核基於 Apache NuttX ，這個被稱為 "Tiny Linux" 的系統為 openvela 提供了高標準的 POSIX 兼容性。通過持續提升其 POSIX 兼容性，openvela 當前已達到 88% 的兼容水平。這種高標準的兼容性意味著在其他標準操作系統（例如 Linux）上開發的軟體可以輕鬆遷移到 openvela，幾乎不需要額外的工作。

- **全面的連接套件**：openvela 提供了廣泛的協議支援，包括藍牙 BR/EDR/LE、LE Mesh、WiFi、Matter、LTE Cat1、乙太網、CAN/LIN 等。同時，它還能與小米的 HyperConnect 協議無縫集成，提供了強大的連接能力。

- **豐富的開發者工具**：openvela 提供了一系列完備的開發者工具，包括系統監控、性能分析、調試器、追蹤、崩潰分析和日誌分析工具，為開發者提供了強大的支援。

## 硬體支援

- openvela 支援各種不同的架構（ARM32、ARM64、RISC-V、Xtensa、MIPS、CEVA 等）和硬體平台。請在[硬體支援](https://nuttx.apache.org/docs/latest/platforms/index.html)頁面上查看完整列表。
- 關於**開發板**的適配案例，請參見[案例文件](./zh-cn/dev_board/Development_Board.md)。

## 快速入門

### 設備開發

如果您想要體驗 openvela，我們提供一個功能完備的模擬器，無需硬體平台即可使用。有關詳細信息，請參閱如下指南。

[快速入門（Ubuntu）](./zh-cn/quickstart/openvela_ubuntu_quick_start.md)

### 快應用開發

[快應用快速入門](https://iot.mi.com/vela/quickapp/zh/guide/start/use-ide.html)

## 子倉庫列表

| 子倉庫連結                                     | 描述                                                                                                                                                                                                                                                                            |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [frameworks](../../../../open-vela/frameworks) | openvela 服務框架：主要包含藍牙、電話、圖形、多媒體、應用框架、安全、系統服務框架（KVDB、OTA、healthd、binder、charger 等）。                                                                                                                                                   |
| [vendor](../../../../open-vela/vendor)         | 晶片原廠的驅動和框架。                                                                                                                                                                                                                                                          |
| [nuttx](../../../../open-vela/nuttx)           | 基於開源即時操作系統 NuttX 打造的內核，提供基礎的內核功能，包括任務調度、跨行程通信、檔案系統、TCP/IP 協議棧、設備驅動和電源管理等，同時對上提供標準的 POSIX 接口。如果您想要對 NuttX 操作系統有更深入了解，可以在 [Apache NuttX](https://nuttx.apache.org/) 官網查看更多信息。 |
| [apps](../../../../open-vela/apps)             | `apps` 是開源即時操作系統（NuttX）的應用程式庫，包含了一系列為 NuttX RTOS 設計的應用程式和實用工具。這些應用程式和工具包括 shell 命令行工具、檔案系統工具、網路工具等，它們可以幫助開發者更方便地開發和調試基於 NuttX RTOS 的嵌入式系統。                                       |
| [external](../../../../open-vela/external)     | openvela 引入的三方庫。                                                                                                                                                                                                                                                         |
| [tests](../../../../open-vela/tests)           | 該倉庫包含接口測試，具體包括多媒體、檔案系統、記憶體管理和 socket 通信等核心 API 的測試。                                                                                                                                                                                       |
| [docs](../../../../open-vela/docs)             | openvela 對應的開發者文件。                                                                                                                                                                                                                                                     |

## 開發者文件

- [文件中心](https://doc.openvela.com/document)

## 應用示例中心

匯總可供開發者參考學習的原生應用與快應用示例。

### 原生應用 (Native Apps)

以下是一些典型的原生應用示例，展示了不同模組和功能的使用方法。

- [音樂播放器](./zh-cn/demo/Music_Player_Example_zh-cn.md)：演示音訊播放、列表管理和後台服務。
- [智能手環](./zh-cn/demo/Smart_Band_Example_zh-cn.md)：演示睡眠監測、心率監測、音樂播放、秒表計時。
- [自行車碼表](./zh-cn/demo/X_Track_zh-cn.md)：演示 GPS 定位、即時數據顯示和運動軌跡記錄。
- [計算器](../../../../open-vela/packages_demos/blob/trunk-5.2/calculator/Readme.md)：一個基礎的 UI 與邏輯交互示例。
- [親戚計算器](../../../../open-vela/packages_demos/blob/trunk-5.2/relation_calculator/Readme_zh-cn.md)：演示複雜的條件邏輯與算法實現。
- [打地鼠](../../../../open-vela/packages_demos/blob/trunk-5.2/Whackmole/README_zh-cn.md)：演示遊戲循環、亂數生成和動畫效果。

查看完整的原生應用列表，請訪問[原生應用示例倉庫](../../../packages_demos/blob/dev/README_zh-cn.md)。

### 快應用（Quick Apps）

- [小米手環天氣預報應用](../../.././packages_fe_examples/blob/trunk-5.2/weather/README.md)：提供簡潔直觀的未來七日天氣信息展示。
- [音樂播放器](../../.././packages_fe_examples/blob/trunk-5.2/player/README.md)：演示一個基礎的音樂播放器，包含音樂的播放，音量調節，歌單查看。
- [日曆](../../.././packages_fe_examples/blob/trunk-5.2/calendar/README.md)：演示一個基礎的日曆。

快應用相關示例正在持續豐富中。查看所有示例，請訪問[快應用示例倉庫](../../../packages_fe_examples)。

## 參與貢獻

- [程式碼貢獻指南](./CONTRIBUTING_zh-cn.md)
- [文件貢獻指南](./zh-cn/contribute/process/doc_dev_process.md)

## 許可協議

這個程式碼庫中的程式碼使用 Apache 2.0 許可證。你可以在[這裡](https://www.apache.org/licenses/LICENSE-2.0.txt)找到更多關於 Apache 2.0 許可證的信息。

openvela 引用三方開源軟體及許可證說明，參考[第三方開源軟體說明](Third_Party_and_Open_Source_Components_zh-cn.md)。

## 社區與支援

我們歡迎您通過多種渠道與 openvela 社區互動和貢獻。

### 微信公眾號

掃描下方二維碼，關注 **openvela** 官方微信公眾號，獲取項目的第一手資訊、深度技術文章以及最新的社區活動信息。

![img](./images/openvela_WeChat_Official_Account.png)

### 技術討論與貢獻

- **Issues**: 如果您有任何問題、建議或發現任何 Bug，請在 Issues 頁面提交一個新的 Issue。請盡量提供詳細的資訊，以便我們更快地理解和解決問題。
- **Pull Requests**: 如果您發現了問題並已經修復，歡迎提交 Pull Request。請確保遵循我們的[貢獻指南](./CONTRIBUTING_zh-cn.md)。
- **Discussions**: 如果您有更廣泛的話題或討論，可以在 Discussions 頁面發起一個新的討論。
