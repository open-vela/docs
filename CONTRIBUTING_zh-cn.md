# 为 openvela 做出贡献

\[ [English](CONTRIBUTING.md) | 简体中文 \]

openvela 由一支活跃的软件工程师和研究人员团队开发。欢迎你加入 openvela 开源社区，为改进此项目做出任何贡献！

openvela 主要遵循 Apache License 2.0 许可证，具体请参看 LICENSE 文件。

## 签署贡献者许可协议 (CLA)

为了参与社区贡献，您需要签署相应的“贡献者许可协议”（Contributor License Agreement, CLA）。以下是针对不同平台的具体步骤：

- **Gitee 平台**:
  - 请访问 [Gitee CLA 签署页面](https://gitee.com/organizations/open-vela/cla/zs6b7c48u6juka2tsnrnkzx6k88np85e) 完成签署。
  - 您可以通过 [我的 CLA 状态](https://gitee.com/profile/clas) 查看签署状态。

- **GitHub 平台**:
  - 在提交新的 Pull Request (PR) 后，系统会提示您完成 CLA 的签署。请根据提示操作以完成签署流程。

## 错误报告

如果您认为在 openvela 中发现了错误，请首先确保您已使用了最新版本的 openvela 进行了测试（您的问题可能已得到修复）。

如果未解决，请搜索问题列表，查看是否已有类似的问题。

## 功能请求

请提交一个 Issue，描述您希望添加的功能、您需要它的原因以及预期的工作方式。

## 贡献代码和文档更改

如果您想给 openvela 增加新功能或者修复一些错误，先确认是否已有类似的问题。如果没有，您就新建一个问题，和大家讨论您的想法。

### 分支策略

- **trunk**：**trunk** 分支不接受 pull request
- **dev**：从 **dev** 分支fork代码，并推送pull request

### 提交代码更改提示

在提出拉取请求（pull request）之前遵循这些提示将加快审核周期。

- 添加适当的单元测试
- 如果适用，添加集成测试
- 不属于您更改范围的行不应被编辑（例如，不要格式化未更改的行，不要重新排序现有的导入）
- 在任何新文件中添加适当的许可证标头

### 提交您的更改  

1. 测试您的更改
  
   请运行测试套件以确保没有出现任何问题。  

2. 签署贡献者许可协议

    请确保您已签署我们的贡献者许可协议（CLA）。我们不要求您转让版权，而是确保我们可以无限制地分发您的代码。所有贡献者只需签署一次 CLA，以向用户保证代码的来源和持续存在。  

3. **基于最新代码进行变基（Rebase）**

    使用主 openvela 存储库中的最新代码更新您的本地存储库。然后，将您的特性分支基于最新的主分支进行变基，以合并上游更改。如果在变基过程中遇到冲突，请按照提示解决冲突并完成变基。我们希望您的初始更改被压缩为单个提交。如果我们要求您进行额外更改，请将它们添加为单独的提交，以方便审查。作为合并前的最后一步，请您自己压缩所有提交，或者我们会为您完成。  

4. 提交拉取请求

    将本地更改推送到您 fork 的存储库副本，并提交拉取请求。在拉取请求中，选择一个简明的标题来总结您的更改，并在正文中提供详细说明。请提及相关问题的编号，例如“关闭 #123”。

### 冲突的处理方式

通常情况下，除非与主分支存在合并冲突，否则您无需重新定位您的拉取请求。当 GitHub/Gitee 提示您的拉取请求“无法自动合并”，请使用以下命令将您的拉取请求重新定位到最新的主分支之上：

1. 重新定位到最新的主分支

     ```Bash
     git remote add upstream https://github.com/open-vela/[repository].git
     git fetch upstream
     git rebase upstream/dev
     ```

2. git 可能会在无法合并时显示一些冲突，比如 `conflict.cpp`，需要手动修改文件以解决冲突，解决后将其标记为已解决

    ```Bash
    git add conflict.cpp
    ```

3. 你可以通过以下方式继续进行 **`rebase`**

    ```Bash
    git rebase --continue
    ```

4. 推送到你的 fork，然后 pull request 将会更新

    ```Bash
    git push --force
    ```
