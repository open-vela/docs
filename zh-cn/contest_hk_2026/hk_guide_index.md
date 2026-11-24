# 香港高校组 openvela 教程导航
\[ [English](../../en/contest_hk_2026/hk_guide_index.md) | 简体中文 | [繁體中文](./hk_guide_index_zh-hk.md) \]

> 本页面向《三十港章 慧智北都》AIoT 比赛高校组、使用 openvela 的参赛队伍，列出本目录下的文档和相关资料，说明先看哪一篇。

## 教程列表

按下面的顺序阅读：

| 顺序 | 文档 | 内容 |
| ---- | ---- | ---- |
| 1 | [香港高校组 openvela 开发指南](./hk_university_track_dev_guide.md) | 选哪种开发环境、准备电脑和代码、两种应用怎么开发、怎么接入 AI |
| 2 | [R528 MIBOX-X1 开发板使用指南](./mibox_x1_board_guide.md) | 硬件规格、接口和拨码开关、编译和烧录、外设测试、第一个应用 |
| 3 | [香港高校组作品代码提交指南](./hk_code_submission_guide.md) | fork 后发 Pull Request，把快应用和原生应用提交到对应仓库 |

## 开发板资料

- [R528 openvela 开发板](https://mi-p.feishu.cn/wiki/UCO2wOYXUiR2xzkI8rscLbUWnVW)：开发板厂商提供的页面，有规格介绍和资料下载（开发板介绍、硬件原理图、用户开发手册、配置工具）。烧录用的镜像，请使用按[开发板使用指南](./mibox_x1_board_guide.md)编译出的 MIBOX-X1 镜像（配置 `nsh`）。
- [板级代码和说明](https://github.com/open-vela/vendor_allwinnertech/tree/dev-ai-contest-2026/boards/r528/r528s3-mibox-x1)：`vendor_allwinnertech` 仓库里的 `r528s3-mibox-x1` 目录，目录里有 [README](https://github.com/open-vela/vendor_allwinnertech/blob/dev-ai-contest-2026/boards/r528/r528s3-mibox-x1/README_zh-cn.md)。

## 如何选择

- 第一次接触 openvela：先读开发指南，再读开发板使用指南。
- 已经有开发板，想马上烧录运行：直接看开发板使用指南的第三、四节。
- 作品做好了，要提交代码：看作品代码提交指南。
