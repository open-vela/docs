# 為 openvela 做出貢獻

\[ [English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING_zh-cn.md) | 繁體中文 \]

openvela 由一支活躍的軟體工程師和研究人員團隊開發。歡迎您加入 openvela 開源社區，為改進此專案做出任何貢獻！
openvela 主要遵循 Apache License 2.0 許可證，具體請參看 LICENSE 檔案。

## 簽署貢獻者許可協議 (CLA)

為了參與社區貢獻，首次提交程式碼時，需要簽署相應的**貢獻者許可協議（Contributor License Agreement, CLA）**。以下是針對不同平台的具體步驟：

- **Gitee 平台**：

    - 請訪問 [Gitee CLA 簽署頁面](https://gitee.com/organizations/open-vela/cla/zs6b7c48u6juka2tsnrnkzx6k88np85e) 完成簽署。
    - 您可以透過 [我簽署的 CLA](https://gitee.com/profile/clas) 查看簽署狀態。

- **GitHub 平台**：

    - 在提交新的 Pull Request (PR) 後，系統會提示您完成 CLA 的簽署。請根據提示操作以完成簽署流程。

## 錯誤報告

如果您認為在 openvela 中發現了錯誤，請首先確保您已使用了最新版本的 openvela 進行了測試（您的問題可能已得到修復）。
如果未解決，請搜索問題列表，查看是否已有類似的問題。

## 功能請求

請提交一個 Issue，描述您希望添加的功能、您需要它的原因以及預期的工作方式。

## 提交程式碼

如果您想給 openvela 增加新功能或者修復一些錯誤，先確認是否已有類似的問題。如果沒有，請您新建一個問題，與大家討論您的想法。

### 分支策略

- **trunk**：**trunk** 分支不接受 pull request。
- **dev**：從 **dev** 分支 fork 程式碼，並推送 pull request。

### 提交程式碼前準備

在新建 pull request 之前遵循這些提示將加快審核週期。

- 添加適當的單元測試。
- 如果適用，添加整合測試。
- 不屬於您更改範圍的行不應被編輯（例如，不要格式化未更改的行，不要重新排序現有的匯入）。
- 在任何新檔案中添加適當的許可證標頭。

### 提交您的更改  

#### 1 測試您的更改
  
請執行測試套件以確保沒有出現任何問題。  

#### 2 簽署貢獻者許可協議

**首次提交需完成**：簽署貢獻者許可協議，請參考[簽署貢獻者許可協議 (CLA)](#簽署貢獻者許可協議-cla)章節。

#### 3 提交程式碼

1. 檢查當前狀態。

    ```Bash
    # 查看工作區狀態
    git status
    ```

2. 暫存更改。

    ```Bash
    # 添加特定檔案到暫存區
    git add path/to/changed/file.cpp
    # 或添加所有更改
    git add .
    ```

3. 提交更改。

    ```Bash
    # 創建提交
    git commit -m "簡明扼要的提交資訊"
    # 或使用詳細提交資訊
    git commit
    ```

4. 配置上游倉庫。

    ```Bash
    # 顯示現有遠端倉庫地址
    git remote -v
    # 添加上游遠端倉庫引用（僅首次需要執行）
    git remote add upstream https://github.com/open-vela/[repository].git
    # 顯示現有遠端倉庫地址（應包含 origin 和 upstream）
    git remote -v
    ```

5. 獲取最新程式碼並變基。

    ```Bash
    # 獲取上游倉庫的最新程式碼
    git fetch upstream
    # 將當前分支變基到最新主分支
    git rebase upstream/dev
    ```

6. 解決衝突（如有）。

    ```Bash
    # 檢測衝突狀態（推薦）  
    git status                   
    # 編輯衝突檔案（如 conflict.cpp），可使用任何編輯器，如 nano、vim、VSCode 等
    nano conflict.cpp            
    # 標記為已解決  
    git add conflict.cpp  
    # 解決所有衝突後繼續變基操作
    git rebase --continue
    # 確認變基完成狀態
    git status
    ```

7. 強制推送更新：

    ```Bash
    # 強制推送更新後的分支到您的遠端倉庫
    git push --force origin dev
    ```

#### 4 創建合入請求

1. 訪問 GitHub 上您的 fork 倉庫。
2. 點擊 **New pull request** 按鈕。
3. 點擊 **Create pull request** 創建合入請求。
4. 填寫合入請求資訊。

#### 5 合入請求後續工作

- **持續監控合入請求的審查意見**
- 及時回應審查者的反饋
- 如需修改，在同一分支上進行更改並推送
