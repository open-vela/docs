# Sim 环境音频功能开发指南

[ [English](./../../../en/quickstart/emulator/sim_audio_guide.md) | 简体中文 ]

## 一、 简介

本文档旨在指导开发者在 openvela Sim（模拟器）环境中进行音频功能的开发与测试。通过 Sim 环境，开发者可以利用 host 主机的音频能力模拟嵌入式设备的音频输入输出，验证驱动逻辑与中间件功能。

主要测试范围包括：

1. 使用 `nxplayer`、`nxrecorder`、`nxlooper` 验证 **Audio** **Driver** 的基础功能。
2. 使用 `mediatool` 验证 **Media Framework** 的业务逻辑。

## 二、 模块架构

Sim 环境下的音频子系统由以下核心模块构成：

1. **Audio Driver**

    - 在 Sim 环境下，底层驱动通过映射 Host 主机（Linux）的 ALSA 接口来模拟音频硬件的输入与输出。

2. **命令行工具集 (CLI Tools)**

    - **nxplayer**：音频播放测试工具。
    - **nxrecorder**：音频录制测试工具。
    - **nxlooper**：音频回环（Loopback）测试工具。
    - 以上工具均基于 Audio Driver 实现。

3. **Media Framework**

    - 包含 Media Framework、RPC 通信、Audio Policy（音频策略）等组件。
    - 对外提供播放、录音、音频通路切换及音量控制等标准接口。

4. **mediatool**

    - 基于 Media Framework 实现的命令行交互程序，用于测试框架层功能。

## 三、 编译配置

请在 openvela 的构建系统（Kconfig）中进行如下配置。

### 1、Audio Driver 配置

启用基础音频驱动支持及缓冲区配置：

```Makefile
CONFIG_AUDIO=y                          # 启用 AUDIO 子系统
CONFIG_AUDIO_NUM_BUFFERS=2              # 驱动缓冲区数量
CONFIG_AUDIO_BUFFER_NUMBYTES=8192       # 单个缓冲区大小 (Bytes)
```

### 2、命令行工具配置

启用 `nxplayer`、`nxrecorder` 和 `nxlooper` 工具：

```Makefile
CONFIG_SYSTEM_NXPLAYER=y
CONFIG_SYSTEM_NXRECORDER=y
CONFIG_SYSTEM_NXLOOPER=y              

# 其他相关配置保持默认即可
```

### 3、Media Framework 配置

Media Framework 支持跨核操作。在 Sim 环境中，通常涉及 AP（应用处理器）与 Audio DSP（数字信号处理器）的模拟。

#### AP 侧配置

将 Media Framework 主体编译在 AP 核时的配置：

```Makefile
 CONFIG_MEDIA=y  
 CONFIG_MEDIA_SERVER=y
 CONFIG_MEDIA_SERVER_CONFIG_PATH="/etc/media/"
 CONFIG_MEDIA_SERVER_PROGNAME="mediad"
 CONFIG_MEDIA_SERVER_STACKSIZE=2097152
 CONFIG_MEDIA_SERVER_PRIORITY=245
 CONFIG_MEDIA_TOOL=y
 CONFIG_MEDIA_TOOL_STACKSIZE=16384    
 CONFIG_MEDIA_TOOL_PRIORITY=100
 CONFIG_MEDIA_CLIENT_LISTEN_STACKSIZE=4096
 
 CONFIG_PFW=y
 CONFIG_LIB_XML2=y
 CONFIG_HAVE_CXX=y
 CONFIG_HAVE_CXXINITIALIZE=y
 CONFIG_LIBCXX=y
 CONFIG_LIBSUPCXX=y
```

#### AUDIO 侧配置

将 Media Framework 主体编译在 Audio 核时的配置（包含 FFmpeg 支持）：

```Makefile
CONFIG_MEDIA=y
CONFIG_MEDIA_SERVER=y

# CONFIG_MEDIA_FOCUS is not set
CONFIG_MEDIA_SERVER_CONFIG_PATH="/etc/media/"
CONFIG_MEDIA_SERVER_PROGNAME="mediad"
CONFIG_MEDIA_SERVER_STACKSIZE=81920
CONFIG_MEDIA_SERVER_PRIORITY=245
CONFIG_MEDIA_TOOL=y
CONFIG_MEDIA_TOOL_STACKSIZE=16384
CONFIG_MEDIA_TOOL_PRIORITY=100
CONFIG_MEDIA_CLIENT_LISTEN_STACKSIZE=4096

# Audio Policy
CONFIG_PFW=y                       
CONFIG_LIB_XML2=y                 
CONFIG_HAVE_CXX=y
CONFIG_HAVE_CXXINITIALIZE=y
CONFIG_LIBCXX=y
CONFIG_LIBSUPCXX=y
CONFIG_KVDB

# FFmpeg 核心配置
CONFIG_LIB_FFMPEG=y 
CONFIG_LIB_FFMPEG_CONFIGURATION="--disable-sse --enable-avcodec --enable-avdevice --enable-avfilter --enable-avformat --enable-decoder='aac,aac_latm,flac,mp3,pcm_s16le,libopus,libfluoride_sbc,libfluoride_sbc_packed,silk' --enable-demuxer='aac,mp3,pcm_s16le,flac,mov,ogg,wav,silk' --enable-encoder='aac,pcm_s16le,libopus,libfluoride_sbc,silk' --enable-hardcoded-tables --enable-indev=nuttx --enable-ffmpeg --enable-ffprobe --enable-filter='adevsrc,adevsink,afade,amix,amovie_async,amoviesink_async,astats,astreamselect,aresample,volume' --enable-libopus --enable-muxer='opus,opusraw,pcm_s16le,silk,wav' --enable-outdev=bluelet,nuttx --enable-parser='aac,flac' --enable-protocol='cache,concat,file,http,https,rpmsg,tcp,unix' --enable-swresample --tmpdir='/stream'"
```

## 四、FFmpeg 扩展配置

Media Framework 基于 FFmpeg 实现。开发者需根据项目需求配置 FFmpeg 组件（demuxer, muxer, decoder, encoder, filter 等）。

### 1、基础配置字符串

核心配置字符串参考如下（需写入 `.config` 或相关构建文件）：

```Makefile
CONFIG_LIB_FFMPEG_CONFIGURATION="--disable-sse --enable-avcodec --enable-avdevice --enable-avfilter --enable-avformat --enable-decoder='aac,aac_latm,flac,mp3,pcm_s16le,libopus,libfluoride_sbc,libfluoride_sbc_packed,silk' --enable-demuxer='aac,mp3,pcm_s16le,flac,mov,ogg,wav,silk' --enable-encoder='aac,pcm_s16le,libopus,libfluoride_sbc,silk' --enable-hardcoded-tables --enable-indev=nuttx --enable-ffmpeg --enable-ffprobe --enable-filter='adevsrc,adevsink,afade,amix,amovie_async,amoviesink_async,astats,astreamselect,aresample,volume' --enable-libopus --enable-muxer='opus,opusraw,pcm_s16le,silk,wav' --enable-outdev=bluelet,nuttx --enable-parser='aac,flac' --enable-protocol='cache,concat,file,http,https,rpmsg,tcp,unix' --enable-swresample --tmpdir='/stream'"
```

**配置说明：**

- `--enable-decoder`: 启用指定的解码器。
- `--enable-filter`: 启用指定的过滤器。

**故障排查：**

如果遇到类似 `Failed to avformat_open_input ret -1330794744, Protocol not found.` 的错误，通常意味着缺少相应的协议或格式支持，请检查并修改上述配置字符串以扩展 FFmpeg 能力。

### 2、依赖库配置

部分 FFmpeg 解码器依赖第三方解码库，必须在 Kconfig 中显式启用这些依赖项：

```Makefile
# libhelix_aac 依赖
CONFIG_LIB_HELIX_AAC=y
CONFIG_LIB_HELIX_AAC_SBR=y

# libfluoride_sbc,libfluoride_sbc_packed 依赖
CONFIG_LIB_FLUORIDE_SBC=y
CONFIG_LIB_FLUORIDE_SBC_DECODER=y
CONFIG_LIB_FLUORIDE_SBC_ENCODER=y

# libopus 依赖
CONFIG_LIB_OPUS=y

#silk 依赖
CONFIG_LIB_SILK=y
```

## 五、调试工具使用指南

本节介绍如何在 Sim 环境中运行并测试音频工具。

### 1、环境启动

1. **运行模拟器**

    进入 `nuttx` 目录并启动 GDB 进行调试运行：

    ```Bash
    cd nuttx
    sudo gdb --args ./nuttx
    ```

2. **挂载 Host 文件系统**

    在 NuttX Shell 中（nsh），将 Host 主机的音频流目录挂载到 Sim 环境的 `/stream` 目录：

    ```Bash
    # 替换 <username> 为实际用户名
    mount -t hostfs -o fs=/home/<username>/Streams/ /stream
    ```

### 2、nxplayer 使用说明

`nxplayer` 用于测试音频播放功能。

#### 场景 A：播放 PCM 原始数据

**测试用例**：播放 `/stream/8000.pcm`（单声道，16bits，44100Hz）。

```Bash
nxplayer

# 指定播放设备
device pcm0p

# 格式: playraw <path> <channels> <width> <rate>
playraw /stream/8000.pcm 1 16 44100
```

#### 场景 B：播放 MP3 文件 (模拟 Offload)

**Host 依赖**： 模拟 MP3 解码需要 Host 主机安装 `libmad` 库

```Bash
sudo apt install libmad0-dev:i386
```

**测试用例**：

```Bash
nxplayer 
# 指定 Offload 播放设备
device pcm1p
# 播放文件
play /stream/1.mp3help

# 停止播放
stop 
```

**功能限制**：

- 支持带 ID3V2 header 的文件。
- 支持不带任何 ID3 header 的文件。
- **暂不支持** ID3V1 格式。

### 3、nxrecorder 使用说明

`nxrecorder` 用于测试音频录制功能。

#### 场景 A：录制 PCM 原始数据

**测试用例**：录制双声道、16bits、48000Hz 的音频到 `1.pcm`。

```Bash
nxrecorder
# 指定录音设备
device pcm0c
# 格式: recordraw <path> <channels> <width> <rate>
recordraw /stream/1.pcm 2 16 48000

# 停止录音
stop 
```

验证方法：检查 Host 主机对应目录下是否生成 `1.pcm` 且能正常播放。

#### 场景 B：录制 MP3 文件 (模拟 Offload)

**Host 依赖**： 模拟 MP3 编码需要 Host 主机安装 `libmp3lame` 库：

```Bash
sudo apt-get install libmp3lame-dev:i386
```

**测试用例**：

```Bash
nxrecorder

# 指定 Offload 录音设备
device pcm1c

# 录制 MP3
record /stream/100.mp3 2 16 44100
```

### 4、nxlooper 使用说明

`nxlooper` 用于测试音频回环（Loopback），即录音数据直接送入播放通道。

#### 场景 A：PCM 数据回环

```Bash
nxlooper
# 指定播放设备
device pcm0p
# 指定录音设备
device pcm0c
# 启动回环: 2通道 16bit 48kHz
loopback 2 16 48000

# 停止回环
stop
```

#### 场景 B：MP3 数据回环

```Bash
nxlooper
device pcm1p
device pcm1c
# 最后一个参数 '8' 代表格式代码 (AUDIO_FMT_MP3)
loopback 2 16 44100 8

# 停止回环
stop 
```

**参数说明**： `loopback` 命令格式为：`loopback <channels> <width> <rate> [format]`

其中 `[format]` 参数对应 `audio.h` 中的定义（默认为 PCM）：

```C
/* 位于 ./nuttx/include/nuttx/audio/audio.h */
#define AUDIO_FMT_UNDEF             0x00
#define AUDIO_FMT_OTHER             0x01
#define AUDIO_FMT_MPEG              0x02
#define AUDIO_FMT_AC3               0x03
#define AUDIO_FMT_WMA               0x04
#define AUDIO_FMT_DTS               0x05
#define AUDIO_FMT_PCM               0x06
#define AUDIO_FMT_WAV               0x07
#define AUDIO_FMT_MP3               0x08
#define AUDIO_FMT_MIDI              0x09
#define AUDIO_FMT_OGG_VORBIS        0x0a
#define AUDIO_FMT_FLAC              0x0b
```

## 六,  mediatool 使用说明

关于 `mediatool` 的详细命令与使用方法，请参考 [Mediatool 介绍](../../device_dev_guide/media/mediatool_zh-cn.md)。
