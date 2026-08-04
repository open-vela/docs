# 支持的硬件平台

> 本页汇总本届大赛提供的硬件开发平台。提交项目方向时可备注意向硬件型号，主办方将优先参考分配，并结合项目实际需求匹配更适配的平台。
>
> 平台分为两类：**已支持开发板**（openvela 已适配，可直接上手）与**待适配开发板**（提供技术资料，适合「新硬件平台适配」赛道挑战）。

## 一、已支持开发板

### 1、润芯微 Gemini-S1（R528）— 全志

<img src="../images/gemini_s1.png" alt="润芯微 Gemini-S1 开发板" width="360" />

- **芯片特点**：Cortex-A7 + HiFi4 DSP + WiFi/BLE + LCD + 音频（首款 openvela 官方产品兼容性认证）
- **适用场景**：openvela 系统生态适配、快应用演示、智能屏/音响原型、端侧 AI 交互
- **开发指南**：[Gemini-S1 README](../../../../../../vendor_allwinnertech/blob/dev-ai-contest-2026/boards/r528/r528s3-gemini-s1/README_zh-cn.md)

### 2、ESP32-S3-EYE — 乐鑫

<img src="../images/esp32s3_eye.png" alt="ESP32-S3-EYE 开发板" width="360" />

- **芯片特点**：双核 240MHz + WiFi/BLE + 摄像头 + LCD + 麦克风 + 加速度计（AIoT 视觉/语音一体化板）
- **适用场景**：人脸检测、物体识别、语音交互、智能门禁、扫码识别
- **设备介绍**：搭载 ESP32-S3，配 200 万像素摄像头、LCD 与麦克风，板载 8MB PSRAM + 8MB flash，支持 Wi-Fi 图传与 USB 调试，适用于图像识别、音频处理等 AIoT 应用。[官方入门指南](https://documentation.espressif.com/esp-who/master/docs/zh_CN/get-started/ESP32-S3-EYE_Getting_Started_Guide.md)
- **openvela 已适配外设**：

  | 外设                               | 设备节点             |
  | ---------------------------------- | -------------------- |
  | OV2640 摄像头（DVP，QVGA RGB565）  | `/dev/video0`        |
  | ST7789 LCD（1.3" 240×240 SPI）     | `/dev/lcd0`          |
  | MSM261S4030H0 PDM 麦克风           | `/dev/audio/pcm_in0` |
  | QMA7981 三轴加速度计（I2C0 @0x12） | `/dev/accel0`        |
  | microSD（1-bit SDIO）              | `/dev/mmcsd1`        |
  | Wi-Fi 4 (b/g/n) STA                | `wlan0`              |
  | BLE 5 LE                           | `bnep0`              |
  | BOOT 按键                          | `/dev/buttons`       |
  | Power LED                          | `/dev/userleds`      |

- **选型注意**：
  - 板上**无触摸硬件**，`/dev/input0` 返回 `ENOENT` 属预期行为；交互输入可用 BOOT 按键、加速度计（敲击/翻转）或摄像头。
  - 板上**无扬声器/功放**，openvela defconfig 只启用 I2S0 RX（麦克风），无音频输出通路；需要语音播报的方案请另选带 Codec 的开发板或外接功放。
  - ESP-WHO / ESP-DL 是 ESP-IDF 私有 AI 栈，**不能在 openvela 上使用**；端侧推理请使用 `apps/mlearning/tflite-micro` 自行部署量化模型，openvela 侧的 camera 例程只做采集与显示，不含推理。
- **开发指南**：[ESP32-S3-EYE README](../../../../../../vendor_espressif/blob/dev-ai-contest-2026/boards/esp32s3/esp32s3-eye/README_zh-cn.md)

### 3、黄山派 SF32LB52 — 思澈科技

<img src="../images/huangshan_pi.png" alt="黄山派 SF32LB52 开发板" width="360" />

- **芯片特点**：低功耗双模蓝牙 + 自研 GPU + 多媒体 + 集成屏幕和传感器
- **适用场景**：轻量穿戴（手表/手环原型）、码表、低功耗显示
- **设备介绍**：[黄山派 wiki](https://wiki.sifli.com/board/sf32lb52x/SF32LB52-黄山派.html)
- **开发指南**：[黄山派 README](../../../../../../vendor_sifli/blob/dev-ai-contest-2026/boards/sf32lb52/lckfb_huangshan_pi/README_zh-cn.md)

### 4、SF32LB52 LCD（DevKit）— 思澈科技

<img src="../images/sf32lb52_lcd.png" alt="SF32LB52 LCD DevKit" width="360" />

- **芯片特点**：低功耗双模蓝牙 + 自研 GPU + 多媒体 + 可自由拓展外设
- **适用场景**：智能手表/手环原型、蓝牙音频终端、LVGL 应用开发
- **设备介绍**：[SF32LB52-DevKit-LCD wiki](https://wiki.sifli.com/board/sf32lb52x/SF32LB52-DevKit-LCD.html)
- **开发指南**：[SF32LB52 DevKit LCD README](../../../../../../vendor_sifli/blob/dev-ai-contest-2026/boards/sf32lb52/sf32lb52_devkit_lcd/README_zh-cn.md)

### 5、百问网 DShanPixVela-Devkit（R528）— 全志

<img src="../images/dshanpix_vela.png" alt="百问网 DShanPixVela-Devkit" width="360" />

- **芯片特点**：Cortex-A7 + HiFi4 DSP + WiFi/BLE + 3.5 寸 SPI 屏（电容触摸）+ 音频 + RS485×2 + CAN×2
- **适用场景**：工业控制、智能显示、AIoT 音视频、教学开发
- **设备介绍**：[百问网 DShanPixVela-Devkit](https://www.100ask.net/hardware/detail/16)
- **开发指南**：[r528s3-dshanpi README](../../../../../../vendor_allwinnertech/blob/dev-ai-contest-2026/boards/r528/r528s3-dshanpi/README_zh-cn.md)

### 6、BES 2800BP — 恒玄科技

<img src="../images/bes2800bp.jpeg" alt="BES 2800BP 开发板" width="360" />

- **芯片特点**：M55 + HiFi4 + 2×M33 / BT6.0 / Wi-Fi 6 / 8.3MB SRAM / 64MB PSRAM / 40MB Nor Flash / Audio CODEC / 2.5D GPU
- **适用场景**：TWS 耳机、智能手表/手环、低功耗蓝牙音频终端
- **技术资料**：[BES2800BP.zip](../attachment/BES2800BP.zip)
- **开发指南**：[BEST1700 AOS EVB README](../../../../../../vendor_bes/blob/dev-ai-contest-2026/boards/best1700_ep/aos_evb/README_zh-cn.md)（BES2800BP 芯片，板/SDK 代号 best1700_ep）

### 7、STM32H750B-DK — 意法半导体

<img src="../images/stm32h750vbt6.jpeg" alt="STM32H750B-DK 开发板" width="360" />

- **芯片特点**：主控 STM32H750XBH6（Cortex-M7 480MHz），板载 4.3" RGB 触摸屏 + SDRAM + QSPI Flash
- **适用场景**：AI 硬件、高性能 MCU 通用开发、图形 HMI
- **开发指南**：[STM32H750B-DK README](../../../../../../nuttx/blob/dev-ai-contest-2026/boards/arm/stm32h7/stm32h750b-dk/README_zh-cn.md)

### 8、STM32H7A3 — 意法半导体

<img src="../images/stm32h7a3.jpg" alt="STM32H7A3 开发板" width="360" />

- **芯片特点**：Cortex-M7 280MHz + 大容量 Flash/RAM
- **适用场景**：AIoT 边缘节点、低功耗 HMI、可穿戴主控、工业控制器
- **开发指南**：[NUCLEO-H7A3ZI-Q README](../../../../../../vendor_st/blob/dev-ai-contest-2026/boards/stm32h7a3/nucleo-h7a3zi-q/README_zh-cn.md)

### 9、GD32F470V-START — 兆易创新

<img src="../images/gd32f470v_start.jpg" alt="GD32F470V-START 开发板" width="360" />

- **芯片特点**：Cortex-M4 240MHz，内置高级 DSP 硬件加速器与单精度 FPU；3072KB Flash（含 1024KB Code-Flash）+ 768KB SRAM；EXMC 支持 SDRAM/SRAM/NOR/NAND；8×U(S)ART、3×I2C、6×SPI、2×I2S；USB FS+HS OTG、Ethernet、CAN2.0B；TFT-LCD/Camera/IPA；3×12bit ADC、2×12bit DAC
- **适用场景**：物联网与智能家居、机器人与关节驱动、工业自动化与电机控制、高精度数据采集与仪器仪表、HMI 人机界面、四轴飞行器
- **说明**：GD32F4 系列已成功适配 Xiaomi Vela OS，支持 I2C、SPI、USART 等基础外设。
- **开发指南**：[GD32F470V-START README](../../../../../../vendor_gigadevice/blob/dev-ai-contest-2026/boards/gd32f4/gd32f470v_start/README_zh-cn.md)
- **设备介绍**：[GD32F4xx Demo Suites 下载](https://www.gd32mcu.com/cn/download?kw=GD32F4xx+Demo+Suites&lan=cn)

### 10、D12x 系列 EVM 评估板 — 匠芯创

<img src="../images/aic_d12x.png" alt="匠芯创 D12x 系列 EVM 评估板" width="360" />

- **芯片特点**：RISC-V 架构、国产自主、显控一体 MCU
- **适用场景**：工业 HMI、网关、串口屏等泛工业领域及智慧家居
- **设备介绍**：[匠芯创D12x开发板资料.zip](../attachment/匠芯创D12x开发板资料.zip)
- **开发指南**：[D12X-Demo68-nor README](../../../../../../vendor_artinchip/blob/dev-ai-contest-2026/README.md)

### 11、D13x 系列 EVM 评估板 — 匠芯创

<img src="../images/aic_d13x.jpg" alt="匠芯创 D13x 系列 EVM 评估板" width="360" />

- **芯片特点**：RISC-V 架构、国产自主、显控一体 MCU
- **适用场景**：工业 HMI、网关、串口屏等泛工业领域及智慧家居
- **设备介绍**：[匠芯创开发板资料.zip](../attachment/匠芯创开发板资料.zip)
- **开发指南**：待补充（等待开发人员提供 D13x 专属 README 链接）

## 二、待适配开发板

> 以下平台 openvela 尚未完成适配，主办方提供芯片手册、硬件设计文档、参考代码等技术资料，适合「新硬件平台适配」赛道挑战（重点加分方向）。
>
> **提交方式**：比赛期间，适配代码在你的专属仓 `contest2026_<编号>_<队伍名>` 内开发（板级代码放专属仓子目录、由 manifest 通过 `<linkfile>` 映射到 openvela 工程对应位置，参照已适配板的 `boards/<芯片>/<开发板>/` 结构），通过 **fork + PR + 自行合入** 提交。下方各板标注的 vendor 仓库为**获奖后 PR 的上游目标仓**；部分仓库的大赛分支仍在创建中，以仓库实际为准。完整流程见 [《参赛代码提交指南》](../code_submission_guide.md) 与 [赛道指引「提交方式」](./hardware_porting_track_guide.md#提交方式)。

### 1、ESP32-P4X-Function-EV-Board — 乐鑫

<img src="../images/esp32p4x.jpg" alt="ESP32-P4X-Function-EV-Board" width="360" />

- **芯片特点**：双核 400MHz RISC-V + AI 加速 + MIPI CSI/DSI
- **适用场景**：AI 视觉终端、多媒体网关、高性能 IoT 边缘设备
- **设备介绍**：基于 ESP32-P4 的多媒体开发板，双核 RISC-V，最大 32MB PSRAM，支持 USB 2.0、MIPI-CSI/DSI、H264 编码；板载 ESP32-C6-MINI-1（Wi-Fi 6 + BLE 5）、7 寸 1024×600 触摸屏、200 万像素 MIPI CSI 摄像头，适用于可视门铃、网络摄像头、智能家居中控屏等。[官方文档](https://docs.espressif.com/projects/esp-dev-kits/zh_CN/latest/esp32p4/esp32-p4x-function-ev-board/index.html)
- **上游目标仓（获奖后 PR）**：`vendor_espressif`（`dev-ai-contest-2026` 分支，`boards/` 目录）

### 2、BK7258 DevKit — 博通集成

<img src="../images/bk7258.jpg" alt="BK7258 DevKit" width="360" />

- **芯片特点**：双核 480MHz Armv8-M Wi-Fi SoC + 低功耗 + 硬件音视频编解码 + 丰富显示接口
- **适用场景**：智能门锁、AI 玩具、AI 眼镜、智能家电
- **设备介绍**：面向端侧 AI 的全功能评估/量产参考平台，BK7258 Wi-Fi 6 AI-SoC（480MHz ARMv8-M），板载双 QSPI 屏、DVP 摄像头、麦克风阵列、陀螺仪、NFC、震动马达、Nand Flash 等；支持端侧语音唤醒（KWS）、AEC、NS、G711/G722 编码及 H.264/MJPEG 硬件编解码，可对接 OpenAI、豆包、DeepSeek 等大模型。[官方文档](https://docs.bekencorp.com/arminodoc/bk_ai_smp/bk7258/zh_CN/v3.1.1/intro/index.html)
- **上游目标仓（获奖后 PR）**：`vendor_beken`（`dev-ai-contest-2026` 分支，`boards/` 目录）

### 3、STM32N647 开发板 — 意法半导体

<img src="../images/stm32n647.jpg" alt="STM32N647 开发板" width="360" />

- **芯片特点**：CM55 800MHz CPU / 600GOPS 算力 NPU；MIPI CSI-2 接口和 ISP / 图形加速器 / 超大容量存储
- **适用场景**：边缘 AI 应用开发 / 音视频处理 / 嵌入式学习
- **设备介绍**：[STM32N6 系列](https://www.st.com.cn/zh/microcontrollers-microprocessors/stm32n6-series.html) ｜ [正点原子 DNN647 资料](https://wiki.alientek.com/docs/Boards/STM32/DNN647/TOC/)
- **上游目标仓（获奖后 PR）**：`vendor_st`（`dev-ai-contest-2026` 分支，`boards/` 目录）

### 4、逻极派 LogicPi A1 边缘 AI 开发板 — Amlogic

<img src="../images/logicpi_a1.png" alt="逻极派 LogicPi A1 边缘 AI 开发板" width="360" />

- **芯片特点**：基于 Amlogic A311Y2 6nm AI SoC，四核 Cortex-A510，集成 RISC-V 控制核、Mali-G310 GPU 与 4TOPS NPU；配备 8GB LPDDR5 + 16GB eMMC；内置 HOX SDK 与 Device Agent，支持自然语言生成硬件控制代码。
- **适用场景**：物理智能体、AI 编程教育、机器人控制、多模态感知、智能硬件原型验证、多智能体协同
- **技术资料**：[LogicPi A1 开发板资料.zip](../attachment/LogicPi%20A1%20开发板资料.zip)
- **上游目标仓（获奖后 PR）**：`vendor_amlogic`（仓库 / 大赛分支待创建，`boards/` 目录）

### 5、KICKPI-K7（RK3576）— 瑞芯微

- **芯片特点**：Rockchip RK3576 高性能多核 SoC（含 NPU，详见官方硬件资料）
- **适用场景**：边缘 AI、多媒体网关、工业控制、嵌入式学习
- **设备介绍**：[KICKPI-K7 上手指南](https://doc.kickpi.cn/Products/Beginner-Guide/KICKPI-K7/) ｜ [硬件资料](https://doc.kickpi.cn/Products/Introduction/KICKPI-K7/) ｜ [百度网盘（提取码 kpcd）](https://pan.baidu.com/s/1cMKQt06pWdxZcsOp1XIvQA?pwd=kpcd)
- **适配指引**：[KICKPI-K7 README](../../../../../../vendor_rockchip/blob/dev-ai-contest-2026/boards/rk3576/kickpi-k7/README_zh-cn.md)
- **上游目标仓（获奖后 PR）**：`vendor_rockchip`（`dev-ai-contest-2026` 分支，`boards/` 目录）

### 6、对话式 AI 开发套件 — 声网 & 博通集成

<img src="../images/agora_beken_convai.png" alt="声网 & 博通集成 对话式 AI 开发套件" width="360" />

- **芯片特点**：贴近真人的极致 AI 对话体验、支持视觉理解、主流 AI 与芯片支持、灵活的单/双屏设计、极速产品原型送样、一站式出海支持
- **适用场景**：AI 玩具、AI 教育硬件、AI 陪伴设备、家居语音助手、穿戴设备（个人助手）
- **设备介绍**：声网（Agora）与博通集成联合推出的对话式 AI 开发套件，将声网的实时对话式 AI 能力与博通集成的端侧 AI 芯片结合，面向 AI 玩具、教育硬件、陪伴设备等场景，支持单/双屏灵活设计与快速原型送样。
- **技术资料**：[声网开发套件使用说明.pdf](../attachment/声网开发套件使用说明.pdf)
- **上游目标仓（获奖后 PR）**：`vendor_beken`（`dev-ai-contest-2026` 分支，`boards/` 目录；以仓库实际为准）

### 7、K1 MUSE Pi Pro — 进迭时空

<img src="../images/spacemit_k1_musepi_pro.png" alt="进迭时空 K1 MUSE Pi Pro 开发板" width="360" />

- **芯片特点**：SpacemiT K1（M1 模组）八核 RISC-V X60 + 2.0 TOPS AI 算力 + 8GB DDR；板载 WiFi6 & Bluetooth 5.2、40Pin 标准 GPIO 扩展接口，支持 MIPI/HDMI 显示；软硬件资料全开源
- **适用场景**：边缘智能硬件、多模态感知、大语言模型应用、机器人、工业自动化、AI 教育科研、物联网
- **设备介绍**：基于进迭时空 SpacemiT K1 的紧凑型单板计算机，八核 RISC-V X60 处理器搭配 2.0 TOPS AI 融合算力，板载 WiFi6/BT5.2 与 40Pin GPIO 扩展，支持 MIPI/HDMI 显示，软硬件资料全开源，适合边缘 AI、大模型应用与机器人等方向的适配挑战。
- **适配指引**：[K1 MUSE Pi Pro README](../../../../../../vendor_SpacemiT/blob/dev-ai-contest-2026/boards/k1/muse_pi_pro/README_zh-cn.md)
- **上游目标仓（获奖后 PR）**：`vendor_SpacemiT`（`dev-ai-contest-2026` 分支，`boards/` 目录）

## 三、相关资源

- [新硬件适配赛道详细指引](./hardware_porting_track_guide.md)
- [openvela 芯片移植指南](../../chip_porting/porting_guide.md)
