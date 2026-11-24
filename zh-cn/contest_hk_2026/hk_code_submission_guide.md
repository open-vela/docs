# 香港高校组作品代码提交指南
\[ [English](../../en/contest_hk_2026/hk_code_submission_guide.md) | 简体中文 | [繁體中文](./hk_code_submission_guide_zh-hk.md) \]

> 本文面向《三十港章 慧智北都》AIoT 比赛高校组、使用 openvela 的参赛队伍，说明怎样把自己的应用代码提交到 openvela 的 GitHub 仓库：先 fork 目标仓库，再向它发起 Pull Request（PR）。

## 一、提交到哪个仓库

所有 PR 的目标分支都是 `dev-ai-contest-2026`。

| 你要提交的内容                     | 目标仓库                                                                              | 说明                                       |
| ---------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| 快应用（JS 应用）                  | [`open-vela/packages_apps`](https://github.com/open-vela/packages_apps)               | 在 openvela 模拟器上运行的快应用           |
| 原生应用（C 语言）                 | [`open-vela/packages_demos`](https://github.com/open-vela/packages_demos)             | openvela 原生应用示例仓库                  |
| 板级配置、外设驱动等开发板相关改动 | [`open-vela/vendor_allwinnertech`](https://github.com/open-vela/vendor_allwinnertech) | R528 MIBOX-X1 的板级代码在这个仓库里       |
| `nuttx` 等公共仓库的改动           | 对应的公共仓库                                                                        | 同样 fork 后向 `dev-ai-contest-2026` 发 PR |

注意：[`packages_fe_examples`](https://github.com/open-vela/packages_fe_examples) 里的快应用只在 AIoT-IDE 内置模拟器里运行，仅供学习参考，作品代码不要提交到那里。

## 二、开始之前

- 有一个 GitHub 账号。
- 完成开发环境搭建，能拉取代码并编译、运行，见[开发指南](./hk_university_track_dev_guide.md)和[快速入门（Ubuntu）](../quickstart/openvela_ubuntu_quick_start.md)。
- 快应用要先在 openvela 模拟器上运行通过，见[快应用开发指南](../app_dev/quickapp/quickapp_manual.md)第四章。
- 原生应用要先在开发板或模拟器上编译运行通过，开发板上的做法见[开发板使用指南](./mibox_x1_board_guide.md)。
- 签署贡献者许可协议（CLA）：首次提交 PR 时会自动检查，没签署的话 PR 不能合入。在 [openvela 官网](https://openvela.com/#/community/cla)用你的 GitHub 账号签署；签署后不用重建 PR，在原来的 PR 下评论 `/check-cla` 触发复检即可。

## 三、提交步骤

以快应用为例。原生应用的做法相同，仓库换成 `packages_demos`，目录换成 `packages/demos`。

1. **Fork**：在 GitHub 上打开目标仓库页面（如 `open-vela/packages_apps`），点右上角的 **Fork**，得到你自己账号下的副本。
2. **在工作区里开发**：按[开发指南](./hk_university_track_dev_guide.md)用 `repo` 拉取代码后，`packages_apps` 在工作区的 `packages/apps` 目录，`packages_demos` 在 `packages/demos`，`vendor_allwinnertech` 在 `vendor/allwinnertech`。进入对应目录，新建一个分支：

   ```bash
   cd packages/apps
   git checkout -b my-app
   ```

3. **放入你的应用**：先看仓库 README 里的目录结构，选和你的应用最接近的目录放入；拿不准放哪里时，在 PR 里说明，由评审的人决定。原生应用除了 C 源码，还要有 `Kconfig`、`Make.defs`、`CMakeLists.txt`、`Makefile` 四个文件，参考仓库里已有的示例，也可以看[开发板使用指南](./mibox_x1_board_guide.md)里 hello_r528 的写法。
4. **提交到本地分支**：

   ```bash
   git add <你的应用目录>
   git commit -s -m "<一句话说明这次提交>"
   ```

   `-s` 会在提交信息里加上 `Signed-off-by`。
5. **推送到你的 fork**：

   ```bash
   git remote add myfork git@github.com:<你的 GitHub 用户名>/packages_apps.git
   git push myfork my-app
   ```

6. **发起 PR**：打开你的 fork 页面，点 **Compare & pull request**，确认目标仓库是 `open-vela/packages_apps`、目标分支是 `dev-ai-contest-2026`，填写说明后创建。
7. **跟进评审**：关注评审意见并及时回复。需要修改时，在同一个分支上继续提交并推送，PR 会自动更新。

## 四、PR 里写什么

建议在 PR 说明里写清楚：

- 作品名称，和一两句话的功能介绍。
- 怎么运行：快应用写明在哪个模拟器配置上运行；原生应用写明用哪个配置、怎么编译、在 `nsh>` 里输入什么命令启动。
- 用到哪些开发板外设（没有用开发板就不写）。

## 五、提交前自检

- 新增的每个文件都有许可证头部。
- 代码风格符合 [openvela 代码风格检查指南](../contribute/code_style_check_guide.md)。
- 这个 PR 只包含你的作品，没有混进无关的格式调整。
- 没有把个人信息、密钥、API Key 提交进代码。
- 首次提交已签署 CLA。

更完整的贡献流程见[为 openvela 做出贡献](../../CONTRIBUTING_zh-cn.md)。
