# 香港高校組作品代碼提交指南
\[ [English](../../en/contest_hk_2026/hk_code_submission_guide.md) | [简体中文](./hk_code_submission_guide.md) | 繁體中文 \]

> 本文面向《三十港章 慧智北都》AIoT 比賽高校組、使用 openvela 的參賽隊伍，説明怎樣把自己的應用代碼提交到 openvela 的 GitHub 倉庫：先 fork 目標倉庫，再向它發起 Pull Request（PR）。

## 一、提交到哪個倉庫

所有 PR 的目標分支都是 `dev-ai-contest-2026`。

| 你要提交的內容                     | 目標倉庫                                                                              | 説明                                       |
| ---------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| 快應用（JS 應用）                  | [`open-vela/packages_apps`](https://github.com/open-vela/packages_apps)               | 在 openvela 模擬器上運行的快應用           |
| 原生應用（C 語言）                 | [`open-vela/packages_demos`](https://github.com/open-vela/packages_demos)             | openvela 原生應用示例倉庫                  |
| 板級配置、外設驅動等開發板相關改動 | [`open-vela/vendor_allwinnertech`](https://github.com/open-vela/vendor_allwinnertech) | R528 MIBOX-X1 的板級代碼在這個倉庫裏       |
| `nuttx` 等公共倉庫的改動           | 對應的公共倉庫                                                                        | 同樣 fork 後向 `dev-ai-contest-2026` 發 PR |

注意：[`packages_fe_examples`](https://github.com/open-vela/packages_fe_examples) 裏的快應用只在 AIoT-IDE 內置模擬器裏運行，僅供學習參考，作品代碼不要提交到那裏。

## 二、開始之前

- 有一個 GitHub 賬號。
- 完成開發環境搭建，能拉取代碼並編譯、運行，見[開發指南](./hk_university_track_dev_guide_zh-hk.md)和[快速入門（Ubuntu）](../quickstart/openvela_ubuntu_quick_start.md)。
- 快應用要先在 openvela 模擬器上運行通過，見[快應用開發指南](../app_dev/quickapp/quickapp_manual.md)第四章。
- 原生應用要先在開發板或模擬器上編譯運行通過，開發板上的做法見[開發板使用指南](./mibox_x1_board_guide_zh-hk.md)。
- 簽署貢獻者許可協議（CLA）：首次提交 PR 時會自動檢查，沒簽署的話 PR 不能合入。在 [openvela 官網](https://openvela.com/#/community/cla)用你的 GitHub 賬號簽署；簽署後不用重建 PR，在原來的 PR 下評論 `/check-cla` 觸發複檢即可。

## 三、提交步驟

以快應用為例。原生應用的做法相同，倉庫換成 `packages_demos`，目錄換成 `packages/demos`。

1. **Fork**：在 GitHub 上打開目標倉庫頁面（如 `open-vela/packages_apps`），點右上角的 **Fork**，得到你自己賬號下的副本。
2. **在工作區裏開發**：按[開發指南](./hk_university_track_dev_guide_zh-hk.md)用 `repo` 拉取代碼後，`packages_apps` 在工作區的 `packages/apps` 目錄，`packages_demos` 在 `packages/demos`，`vendor_allwinnertech` 在 `vendor/allwinnertech`。進入對應目錄，新建一個分支：

   ```bash
   cd packages/apps
   git checkout -b my-app
   ```

3. **放入你的應用**：先看倉庫 README 裏的目錄結構，選和你的應用最接近的目錄放入；拿不準放哪裏時，在 PR 裏説明，由評審的人決定。原生應用除了 C 源碼，還要有 `Kconfig`、`Make.defs`、`CMakeLists.txt`、`Makefile` 四個文件，參考倉庫裏已有的示例，也可以看[開發板使用指南](./mibox_x1_board_guide_zh-hk.md)裏 hello_r528 的寫法。
4. **提交到本地分支**：

   ```bash
   git add <你的应用目录>
   git commit -s -m "<一句话说明这次提交>"
   ```

   `-s` 會在提交信息里加上 `Signed-off-by`。
5. **推送到你的 fork**：

   ```bash
   git remote add myfork git@github.com:<你的 GitHub 用户名>/packages_apps.git
   git push myfork my-app
   ```

6. **發起 PR**：打開你的 fork 頁面，點 **Compare & pull request**，確認目標倉庫是 `open-vela/packages_apps`、目標分支是 `dev-ai-contest-2026`，填寫説明後創建。
7. **跟進評審**：關注評審意見並及時回覆。需要修改時，在同一個分支上繼續提交併推送，PR 會自動更新。

## 四、PR 裏寫什麼

建議在 PR 説明裏寫清楚：

- 作品名稱，和一兩句話的功能介紹。
- 怎麼運行：快應用寫明在哪個模擬器配置上運行；原生應用寫明用哪個配置、怎麼編譯、在 `nsh>` 裏輸入什麼命令啟動。
- 用到哪些開發板外設（沒有用開發板就不寫）。

## 五、提交前自檢

- 新增的每個文件都有許可證頭部。
- 代碼風格符合 [openvela 代碼風格檢查指南](../contribute/code_style_check_guide.md)。
- 這個 PR 只包含你的作品，沒有混進無關的格式調整。
- 沒有把個人信息、密鑰、API Key 提交進代碼。
- 首次提交已簽署 CLA。

更完整的貢獻流程見[為 openvela 做出貢獻](../../CONTRIBUTING_zh-cn.md)。
