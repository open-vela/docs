# 為 openvela 做出貢獻

\[ [English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING_zh-cn.md) | 繁體中文 \]

openvela 由一群活躍的軟體工程師和研究人員團隊開發。歡迎你加入 openvela 開源社區，為改進此專案做出任何貢獻！

openvela 主要遵循 Apache License 2.0 授權，具體請查看 LICENSE 文件。

## 簽署貢獻者許可協議 (CLA)

為了參與社區貢獻，您需要簽署相應的「貢獻者授權協議」（Contributor License Agreement, CLA）。以下是針對不同平台的步驟說明：

- **Gitee 平台**:
  - 請前往 [Gitee CLA 簽署頁面](https://gitee.com/organizations/open-vela/cla/zs6b7c48u6juka2tsnrnkzx6k88np85e) 完成簽署。
  - 您可以通過 [我的 CLA 狀態](https://gitee.com/profile/clas) 查看簽署狀態。

- **GitHub 平台**:
  - 在提交新的 Pull Request (PR) 后，系统会提示您完成 CLA 的签署。请根据提示操作以完成签署流程。

## 錯誤報告

如果您認為在 openvela 中發現了錯誤，請先確保您已使用了最新版本的 openvela 進行了測試（您的問題可能已在最新版本被修復）。

如果未解決，請搜尋問題列表，查看是否已有類似的問題。

## 功能請求

請提交一個 Issue，描述您希望新增的功能、您需要它的原因以及預期的工作方式。

## 貢獻程式碼和文件

如果您想為 openvela 增加新功能或修復一些錯誤，先確認是否有類似的問題。如果沒有，請您新建一個問題，和大家討論您的想法。

### 分支策略

- **trunk**：**trunk** 分支不接受 pull request。
- **dev**：從 **dev** 分支 fork 代碼，並推送到 pull request。

### 提交程式碼前提示

在發送 pull request 之前遵循以下提示將加快審核的時間。

- 新增適當的單元測試
- 如果適用，請新增整合測試
- 不應該編輯不是您變更的地方（例如，不要格式化未更改的地方，不要重新排序現有的導入）
- 在任何新文件中增加適當的授權標頭

### 提交您的更改  

1. 測試您的更改
  
   請執行測試套件以確保沒有出現任何問題。 

2. 簽署貢獻者許可協議

    請確保您已簽署我們的貢獻者授權協議（CLA）。我們不要求您轉讓版權，而是確保我們可以無限制地分發您的程式碼。所有貢獻者只需簽署一次 CLA，以向使用者保證程式碼的來源和持續存在。  

3. **基於最新程式碼進行 Rebase**

    使用主 openvela 儲存庫中的最新程式碼更新您的本機儲存庫。然後，將您的特性分支基於最新的主分支進行變基，以合併上游變更。如果在變基過程中遇到衝突，請依照指示解決衝突並完成變基。我們希望您的初始變更被壓縮為單一提交。如果我們要求您進行額外更改，請將它們新增為單獨的提交，以方便審查。作為合併前的最後一步，請您自己壓縮所有​​提交，或者我們會為您完成。  

4. 發送 pull request

    將本機變更推送到您 fork 的儲存庫副本，並發送 pull request。在 pull request 中，選擇一個簡潔的標題來總結您的更改，並在正文中提供詳細說明。請提及相關問題的編號，例如「關閉 #123」。

### 衝突的處理方式

當平台提示您的 pull request 無法合併時，請使用下列命令將您的 pull request 重新定位到最新的主分支之上：

1. 重新定位到最新的主分支

     ```Bash
     git remote add upstream https://github.com/open-vela/[repository].git
     git fetch upstream
     git rebase upstream/dev
     ```

2. git 可能會在無法合併時顯示一些衝突，例如 `conflict.cpp`，需要手動修改檔案以解決衝突，解決後將其標記為已解決

    ```Bash
    git add conflict.cpp
    ```

3. 你可以透過以下方式繼續進行 **`rebase`**

    ```Bash
    git rebase --continue
    ```

4. 推送到你的 fork，然後 pull request 將會更新

    ```Bash
    git push --force
    ```
