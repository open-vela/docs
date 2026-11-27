# Hong Kong University Track openvela Guide Index
\[ English | [简体中文](../../zh-cn/contest_hk_2026/hk_guide_index.md) | [繁體中文](../../zh-cn/contest_hk_2026/hk_guide_index_zh-hk.md) \]

> This page is for university-track teams that use openvela in the 《三十港章 慧智北都》 AIoT competition. It lists the documents in this directory and related resources, and says which one to read first.

## Guides

Read them in this order:

| Order | Document | Content |
| ----- | -------- | ------- |
| 1 | [openvela Development Guide for the Hong Kong University Track](./hk_university_track_dev_guide.md) | Which development environment to choose, how to prepare your computer and code, how to build the two kinds of apps, and how to connect AI |
| 2 | [R528 MIBOX-X1 Development Board Guide](./mibox_x1_board_guide.md) | Hardware specifications, interfaces and DIP switches, building and flashing, peripheral tests, and a first application |
| 3 | [Connecting to the R528 MIBOX-X1 Board](./mibox_x1_connect_guide.md) | Connect the serial port with MobaXterm, confirm the system has started, join Wi-Fi, troubleshooting |
| 4 | [Running the AI Agent on the R528 MIBOX-X1 (Experimental)](./mibox_x1_ai_agent_guide.md) | Create the ai_agent configuration and build it, get online, set the model, chat with the Agent, troubleshoot with the log |
| 5 | [Code Submission Guide for the Hong Kong University Track](./hk_code_submission_guide.md) | Fork, then open a Pull Request to submit Quick Apps and native apps to the matching repository |

## Development Board Resources

- [R528 openvela Development Board](https://my.feishu.cn/wiki/BLn6w3By0i8yuNk62GOcxnbfnmh): a page from the board vendor with the specifications and downloads (board introduction, hardware schematic, user development manual, configuration tools). For flashing, use the MIBOX-X1 image you build by following the [Development Board Guide](./mibox_x1_board_guide.md) (configuration `nsh`).
- [Board support code and README](https://github.com/open-vela/vendor_allwinnertech/tree/dev-ai-contest-2026/boards/r528/r528s3-mibox-x1): the `r528s3-mibox-x1` directory in the `vendor_allwinnertech` repository, which has its own [README](https://github.com/open-vela/vendor_allwinnertech/blob/dev-ai-contest-2026/boards/r528/r528s3-mibox-x1/README.md).

## How to Choose

- First time with openvela: read the Development Guide, then the Development Board Guide.
- You already have the board and want to flash and run right away: go straight to Sections III and IV of the Development Board Guide.
- The board is flashed and you want to connect to it from a computer to read the log and get online: read the Connecting guide.
- You want to try the AI Agent on the board: read the AI Agent guide (experimental; you build the firmware yourself).
- Your project is ready and you need to submit the code: read the Code Submission Guide.
