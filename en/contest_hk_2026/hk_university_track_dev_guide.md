# openvela Development Guide for the Hong Kong University Track
\[ English | [简体中文](../../zh-cn/contest_hk_2026/hk_university_track_dev_guide.md) | [繁體中文](../../zh-cn/contest_hk_2026/hk_university_track_dev_guide_zh-hk.md) \]

> This guide is for university-track teams that use openvela in the 《三十港章 慧智北都》 AIoT competition. It covers technical content only: which development environment to choose, how to prepare your computer and code, how to build the two kinds of apps, and how to connect AI.
>
> For board details, see the [R528 MIBOX-X1 Development Board Guide](./mibox_x1_board_guide.md).

## I. Three Development Environments

You can build your project on the development board, or only in an emulator. The three environments differ as follows:

| Environment | What you can do | What you cannot do | Best for |
| ----------- | --------------- | ------------------ | -------- |
| R528 MIBOX-X1 development board | Command line, LVGL UI, all onboard peripherals (buttons, LED, touch screen, audio, infrared, Bluetooth, Wi-Fi, 9-axis sensor, SD card), external parts on the header pins | The `nsh` configuration enables the JS app runtime (QuickJS) but does not include ai_agent | Projects that need hardware |
| openvela emulator | Command line, LVGL UI, JS apps, ai_agent (the emulator has its own network), JS apps that call AI | No GPIO, sensors, infrared, Bluetooth, or other hardware | No board, or UI and AI only |
| Emulator built into AIoT-IDE | Write, preview, and debug JS apps without rebuilding the system each time | It is not the openvela system, so behavior can differ from the real system | JS apps only, with fast edit-and-preview cycles |

If you build with JS apps, run your app on the openvela emulator once before you submit. See Chapter IV of the [Quick App Development Guide](../app_dev/quickapp/quickapp_manual.md).

## II. Prepare Your Computer

- OS: Ubuntu 22.04.
- Hardware: the official requirement is at least 16 GB of memory and 40 GB of free disk space. In a virtual machine, builds are slow when memory is tight. You can lower the parallel job count, for example with `-j4`.
- The [Quick App Development Guide (AI Workflow)](../app_dev/quickapp/quickapp_ai_workflow.md) states that WSL and Docker are not supported.
- For installing the dependency packages, `repo`, and `git-lfs`, see [Quick Start (Ubuntu)](../quickstart/openvela_ubuntu_quick_start.md).
- The flashing tools for the development board (PhoenixSuit and its drivers) run on Windows. If you only have Ubuntu, you need a separate Windows computer for flashing. For details, see Section IV of the board guide.

## III. Get the Code

Always use the `dev-ai-contest-2026` branch. Do not use `dev` or `trunk`:

```bash
mkdir openvela && cd openvela
repo init -u https://github.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs
repo sync -c -j4
```

The first sync downloads a lot of data and can take a long time on a slow network. If it is interrupted, run `repo sync -c -j4` again and it continues where it stopped.

## IV. Develop on the Development Board

For building, packing, flashing, peripheral tests, and your first application, follow the [Development Board Guide](./mibox_x1_board_guide.md). The board's directory is `vendor/allwinnertech/boards/r528/r528s3-mibox-x1`, and the default configuration is `nsh`.

## V. Develop in the Emulator

Build and start the openvela emulator:

```bash
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake -j$(nproc)
./emulator.sh cmake_out/vela_goldfish-arm64-v8a-ap/
```

When you see the `goldfish-armv8a-ap>` prompt, the emulator has started. It has network access by default, so you do not need to set up Wi-Fi.

To use ai_agent in the emulator, switch to the ai_agent emulator configuration and rebuild. See the "QEMU Emulator" section in Chapter VI of the [ai_agent Application Development Quick Start](../edge_ai_dev/ai_agent/ai_agent_quickstart.md).

## VI. Two Kinds of Apps

A JS app is called a Quick App in the official documentation.

| | Native app (C + LVGL) | JS app |
| -- | --------------------- | ------ |
| How you build it | Write C and build it into the system firmware | Write JS, edit and preview in AIoT-IDE |
| Runs on | Development board, emulator | Development board (runtime enabled), emulator |
| Hardware control | Yes, directly through onboard peripherals and header pins | Mainly UI and system capabilities |
| Connecting AI | Call ai_agent, starting from `velaclaw_client_open()` | Call `@system.velaclaw` |
| References | [mini_memo Example Application](../edge_ai_dev/ai_agent/mini_memo_guide.md), [Section VI of the board guide](./mibox_x1_board_guide.md) | [Quick App Development Guide](../app_dev/quickapp/quickapp_manual.md) |

## VII. Connect AI

ai_agent (openvelaClaw) needs a large-model API key. For getting one, see Chapter I of the [ai_agent Application Development Quick Start](../edge_ai_dev/ai_agent/ai_agent_quickstart.md). For configuring it, see Chapter II.

- **Native apps**: connect to openvelaClaw with `velaclaw_client_open("app name")`, then call the large model. For a complete example, see Chapter II of the [mini_memo Example Application](../edge_ai_dev/ai_agent/mini_memo_guide.md).
- **JS apps**: use `@system.velaclaw`, for example:

  ```javascript
  import velaclaw from '@system.velaclaw'

  velaclaw.ask({
    query: '北京今天天气怎么样',   // "What is the weather in Beijing today?"
    success: function (res) { console.log('AI reply:', res.reply) },
    fail: function (data, code) { console.log('fail, code:', code) }
  })
  ```

  For the full tutorial, see [Calling the On-Device AI Agent from a Quick App (@system.velaclaw)](../app_dev/quickapp/quickapp_velaclaw.md).

In the current official configurations, only the ai_agent configuration for the goldfish emulator includes both JS apps and ai_agent. Develop JS apps that call AI in the emulator first. The board's `nsh` configuration does not include ai_agent. To build AI conversation on the board, you need to adjust the configuration yourself. See the "Adding a New Development Board" section in Chapter VI of the [ai_agent Application Development Quick Start](../edge_ai_dev/ai_agent/ai_agent_quickstart.md).

## VIII. Document Index

- [R528 MIBOX-X1 Development Board Guide](./mibox_x1_board_guide.md)
- [Quick Start (Ubuntu)](../quickstart/openvela_ubuntu_quick_start.md)
- [ai_agent Application Development Quick Start](../edge_ai_dev/ai_agent/ai_agent_quickstart.md)
- [mini_memo Example Application](../edge_ai_dev/ai_agent/mini_memo_guide.md)
- [Quick App Development Guide](../app_dev/quickapp/quickapp_manual.md)
- [Calling the On-Device AI Agent from a Quick App (@system.velaclaw)](../app_dev/quickapp/quickapp_velaclaw.md)
- [New Platform Adaptation Guide](../chip_porting/porting_guide.md)
