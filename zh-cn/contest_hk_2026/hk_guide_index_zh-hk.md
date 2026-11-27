# 香港高校組 openvela 教程導航
\[ [English](../../en/contest_hk_2026/hk_guide_index.md) | [简体中文](./hk_guide_index.md) | 繁體中文 \]

> 本頁面向《三十港章 慧智北都》AIoT 比賽高校組、使用 openvela 的參賽隊伍，列出本目錄下的文檔和相關資料，説明先看哪一篇。

## 教程列表

按下面的順序閲讀：

| 順序 | 文檔 | 內容 |
| ---- | ---- | ---- |
| 1 | [香港高校組 openvela 開發指南](./hk_university_track_dev_guide_zh-hk.md) | 選哪種開發環境、準備電腦和代碼、兩種應用怎麼開發、怎麼接入 AI |
| 2 | [R528 MIBOX-X1 開發板使用指南](./mibox_x1_board_guide_zh-hk.md) | 硬件規格、接口和撥碼開關、編譯和燒錄、外設測試、第一個應用 |
| 3 | [連接 R528 MIBOX-X1 開發板（串口與聯網）](./mibox_x1_connect_guide_zh-hk.md) | 用 MobaXterm 連串口、確認系統啟動、連接 Wi-Fi、常見問題 |
| 4 | [在 R528 MIBOX-X1 上運行 AI Agent（實驗）](./mibox_x1_ai_agent_guide_zh-hk.md) | 新建帶 ai_agent 的配置並編譯、聯網、設置大模型、和 Agent 對話、讀日誌排錯 |
| 5 | [香港高校組作品代碼提交指南](./hk_code_submission_guide_zh-hk.md) | fork 後發 Pull Request，把快應用和原生應用提交到對應倉庫 |

## 開發板資料

- [R528 openvela 開發板](https://my.feishu.cn/wiki/BLn6w3By0i8yuNk62GOcxnbfnmh)：開發板廠商提供的頁面，有規格介紹和資料下載（開發板介紹、硬件原理圖、用户開發手冊、配置工具）。燒錄用的鏡像，請使用按[開發板使用指南](./mibox_x1_board_guide_zh-hk.md)編譯出的 MIBOX-X1 鏡像（配置 `nsh`）。
- [板級代碼和説明](https://github.com/open-vela/vendor_allwinnertech/tree/dev-ai-contest-2026/boards/r528/r528s3-mibox-x1)：`vendor_allwinnertech` 倉庫裏的 `r528s3-mibox-x1` 目錄，目錄裏有 [README](https://github.com/open-vela/vendor_allwinnertech/blob/dev-ai-contest-2026/boards/r528/r528s3-mibox-x1/README_zh-cn.md)。

## 如何選擇

- 第一次接觸 openvela：先讀開發指南，再讀開發板使用指南。
- 已經有開發板，想馬上燒錄運行：直接看開發板使用指南的第三、四節。
- 板子燒錄好了，想用電腦連上看日誌、聯網：看連接開發板指南。
- 想在開發板上試一試 AI Agent：看在開發板上運行 AI Agent 的指南（實驗性質，需要自己編譯固件）。
- 作品做好了，要提交代碼：看作品代碼提交指南。
