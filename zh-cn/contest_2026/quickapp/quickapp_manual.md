# 快应用开发指南（手动开发）（大赛参赛说明）

> 本页为 2026 首届 openvela AI 硬件全球开发者大赛的参赛说明。快应用手动开发的完整技术文档见 [快应用开发指南（手动开发）](../../app_dev/quickapp/quickapp_manual.md)，本页仅保留与大赛相关的要求。

## 大赛环境要求

> 大赛参赛者请统一基于大赛分支 `dev-ai-contest-2026` 拉取 openvela 代码（`repo init` 时通过 `-b dev-ai-contest-2026` 指定），不要使用 dev 或 trunk 分支，以确保与大赛环境一致。
>
> 注意：debug.rpk 仅用于开发调试阶段，参赛提交时请使用 release.rpk（生产模式打包）。

## 提交参赛代码

> 完整的提交流程、仓库获取方式、时间与权限说明，以 [《参赛代码提交指南》](../code_submission_guide.md) 为准。

组委会会为每支队伍 / 每位参赛者创建专属的 GitHub 代码仓库（命名 `contest2026_<编号>_<队伍名>`，默认 public）。比赛期间，你 **fork 自己的专属仓** 进行开发，再以 **PR** 形式提交回专属仓，可**自行 review 并合入**（无需等待组委会审核）。

AI Coding 对话会自动记录到本机 staging（不会自动上传），需由你**主动导出/打包**选定会话到仓内 `logs/` 目录后一并提交（详见 [《AI Coding 日志归集与提交手册》](../ai_coding_log_guide.md)）。

**提交内容**：快应用**源码工程**（`src/`、`package.json`、`manifest.json` 等）+ 生产模式打包产物 **release.rpk**，二者都放入你的专属仓。

> 大赛仅在 GitHub 进行（不在 Gitee）；专属仓通过 **fork → PR → 自行 review 合入** 提交。**获奖后**需按要求将作品 PR 至 openvela 上游 `packages_apps` 仓库的 `dev-ai-contest-2026` 分支，走标准 PR + CI 流程。
>
> 运行环境区分：`packages_apps` 在 openvela 模拟器上运行；`packages_fe_examples` 在 AIoT IDE 内置模拟器中运行，仅供学习参考。

## 技术文档

- [快应用开发指南（手动开发）](../../app_dev/quickapp/quickapp_manual.md)
