# 香港高校组 openvela 开发指南
\[ [English](../../en/contest_hk_2026/hk_university_track_dev_guide.md) | 简体中文 | [繁體中文](./hk_university_track_dev_guide_zh-hk.md) \]

> 本文面向《三十港章 慧智北都》AIoT 比赛高校组、使用 openvela 的参赛队伍，只介绍技术内容：该选哪种开发环境、怎么准备电脑和代码、两种应用怎么开发、怎么接入 AI。
>
> 开发板的具体用法见 [R528 MIBOX-X1 开发板使用指南](./mibox_x1_board_guide.md)。

## 一、三种开发环境

作品可以在开发板上做，也可以只在模拟器上做。三种环境的区别如下：

| 环境                  | 能做什么                                                                                                         | 做不了什么                                                     | 适合                             |
| --------------------- | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------- |
| R528 MIBOX-X1 开发板  | 命令行、LVGL 界面、全部板载外设（按键、LED、触摸屏、音频、红外、蓝牙、Wi-Fi、九轴传感器、SD 卡）、排针接外部器件 | `nsh` 配置已启用 JS 应用运行时（QuickJS），但没有包含 ai_agent | 需要硬件的作品                   |
| openvela 模拟器       | 命令行、LVGL 界面、JS 应用、ai_agent（模拟器自带网络），JS 应用调用 AI                                           | 没有 GPIO、传感器、红外、蓝牙等硬件                            | 没有开发板，或只做界面和 AI      |
| AIoT-IDE 自带的模拟器 | 编写、预览、调试 JS 应用，不需要每次重新编译系统                                                                 | 不是 openvela 系统，行为与真实系统有差异                       | 只做 JS 应用，需要快速修改和预览 |

用 JS 应用做的作品，提交前建议再到 openvela 模拟器上运行验证一遍，详见[快应用开发指南](../app_dev/quickapp/quickapp_manual.md)第四章。

## 二、准备电脑

- 系统：Ubuntu 22.04。
- 配置：官方要求至少 16GB 内存、40GB 可用硬盘。用虚拟机的话，内存不足时编译会很慢，可以把并行数调小，例如 `-j4`。
- [快应用开发指南（AI 工作流）](../app_dev/quickapp/quickapp_ai_workflow.md)说明不支持 WSL 和 Docker。
- 依赖包、`repo` 和 `git-lfs` 的安装步骤见[快速入门（Ubuntu）](../quickstart/openvela_ubuntu_quick_start.md)。
- 烧录开发板用的工具（PhoenixSuit 和驱动）在 Windows 上运行。只有 Ubuntu 的话，需要另一台 Windows 电脑做烧录，细节见开发板使用指南第四节。

## 三、获取代码

统一使用 `dev-ai-contest-2026` 分支，不要用 `dev` 或 `trunk`：

```bash
mkdir openvela && cd openvela
repo init -u https://github.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs
repo sync -c -j4
```

第一次同步要下载很多内容，网络不好时耗时较长。中断后重新执行 `repo sync -c -j4` 会接着下载。

## 四、用开发板开发

编译、打包、烧录、外设测试和第一个应用，按[开发板使用指南](./mibox_x1_board_guide.md)操作。板子对应的板级目录是 `vendor/allwinnertech/boards/r528/r528s3-mibox-x1`，默认使用 `nsh` 配置。

## 五、用模拟器开发

编译并启动 openvela 模拟器：

```bash
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake -j$(nproc)
./emulator.sh cmake_out/vela_goldfish-arm64-v8a-ap/
```

看到 `goldfish-armv8a-ap>` 提示符就说明启动成功。模拟器默认带网络，不需要配置 Wi-Fi。

要在模拟器里使用 ai_agent，需要换成 ai_agent 的模拟器配置并重新编译，步骤见 [ai_agent 应用开发上手指南](../edge_ai_dev/ai_agent/ai_agent_quickstart.md)第六章「QEMU 模拟器」一节。

## 六、两种应用形态

JS 应用在官方文档中叫「快应用」。

|          | 原生应用（C + LVGL）                                                                                                | JS 应用                                                  |
| -------- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 开发方式 | 用 C 语言开发，编进系统固件                                                                                         | 用 JS 开发，在 AIoT-IDE 里编写和预览                     |
| 运行在   | 开发板、模拟器                                                                                                      | 开发板（运行时已启用）、模拟器                           |
| 控制硬件 | 可以，直接使用板载外设和排针                                                                                        | 以界面和系统能力为主                                     |
| 接入 AI  | 调用 ai_agent，入口是 `velaclaw_client_open()`                                                                      | 调用 `@system.velaclaw`                                  |
| 参考     | [mini_memo 应用介绍](../edge_ai_dev/ai_agent/mini_memo_guide.md)、[开发板使用指南第六节](./mibox_x1_board_guide.md) | [快应用开发指南](../app_dev/quickapp/quickapp_manual.md) |

## 七、接入 AI

ai_agent（openvelaClaw）需要一个大模型 API Key，申请见 [ai_agent 应用开发上手指南](../edge_ai_dev/ai_agent/ai_agent_quickstart.md)第一章，配置见第二章。

- **原生应用**：用 `velaclaw_client_open("应用名")` 连接 openvelaClaw，再调用大模型。完整例子见 [mini_memo 应用介绍](../edge_ai_dev/ai_agent/mini_memo_guide.md)第二章。
- **JS 应用**：用 `@system.velaclaw`，例如：

  ```javascript
  import velaclaw from '@system.velaclaw'

  velaclaw.ask({
    query: '北京今天天气怎么样',
    success: function (res) { console.log('AI reply:', res.reply) },
    fail: function (data, code) { console.log('fail, code:', code) }
  })
  ```

  详细教程见[快应用调用端侧 AI Agent 教程](../app_dev/quickapp/quickapp_velaclaw.md)。

目前官方配置中，只有 goldfish 模拟器的 ai_agent 配置同时包含 JS 应用和 ai_agent，所以 JS 应用调用 AI 请先在模拟器上开发。开发板的 `nsh` 配置没有包含 ai_agent，在板子上做 AI 对话需要自己调整配置，参考 [ai_agent 应用开发上手指南](../edge_ai_dev/ai_agent/ai_agent_quickstart.md)第六章「添加新开发板」一节。

## 八、文档索引

- [R528 MIBOX-X1 开发板使用指南](./mibox_x1_board_guide.md)
- [快速入门（Ubuntu）](../quickstart/openvela_ubuntu_quick_start.md)
- [ai_agent 应用开发上手指南](../edge_ai_dev/ai_agent/ai_agent_quickstart.md)
- [mini_memo 应用介绍](../edge_ai_dev/ai_agent/mini_memo_guide.md)
- [快应用开发指南](../app_dev/quickapp/quickapp_manual.md)
- [快应用调用端侧 AI Agent 教程](../app_dev/quickapp/quickapp_velaclaw.md)
- [芯片移植指南](../chip_porting/porting_guide.md)
