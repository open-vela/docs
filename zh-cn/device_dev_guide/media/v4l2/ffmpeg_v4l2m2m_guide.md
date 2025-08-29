# FFmpeg V4L2 M2M 使用指南

[[English](../../../../en/device_dev_guide/media/v4l2/ffmpeg_v4l2m2m_guide.md) | 简体中文]

## 一、概述

本文档为开发者提供在 openvela 平台上为 FFmpeg 启用 V4L2 M2M (Video4Linux2 Memory-to-Memory) 硬件加速功能的详细指南。

V4L2 M2M 是一个标准的 Linux 内核框架，专用于无显示硬件的内存到内存视频处理设备，例如视频编解码器。

通过将 FFmpeg 与支持 V4L2 M2M 的硬件驱动相结合，系统可以将 H.264 等视频编解码任务从 CPU 卸载到专用的硬件单元，从而显著提升处理效率和系统性能。

## 二、环境与配置

本指南以 `simulator` 平台为例进行说明。

### 1、系统配置 (Kconfig)

在 `menuconfig` 中，您必须启用以下与视频处理相关的核心配置项，以确保视频框架和模拟器驱动已编译进系统。

```Makefile
# 使能视频框架
CONFIG_VIDEO=y
CONFIG_DRIVERS_VIDEO=y
CONFIG_VIDEO_STREAM=y

# 使能模拟器视频编解码驱动
CONFIG_SIM_VIDEO_DECODER=y
CONFIG_SIM_VIDEO_ENCODER=y

CONFIG_VIDEOUTILS_OPENH264=y
CONFIG_VIDEOUTILS_LIBX264=y
```

### 2、FFmpeg 配置 (`defconfig`)

您需要修改 `defconfig` 文件中的 `CONFIG_LIB_FFMPEG_CONFIGURATION` 宏，以在 FFmpeg 库的构建参数中启用 V4L2 M2M 相关的编解码器。

#### 启用 V4L2 M2M 解码器

1. 找到 `CONFIG_LIB_FFMPEG_CONFIGURATION` 配置项。
2. 在其 `--enable-decoder` 参数列表中，添加 `h264_v4l2m2m`。
3. 为了确保测试时调用的是硬件解码器，可以从 `--enable-decoder` 列表中移除纯软件的 `h264` 解码器。

#### 启用 V4L2 M2M 编码器

1. 找到 `CONFIG_LIB_FFMPEG_CONFIGURATION` 配置项。
2. 在其 `--enable-encoder` 参数列表中，添加 `h264_v4l2m2m`。
3. 在其 `--enable-demuxer` 参数列表中，确保已添加 `rawvideo`，以便支持从原始 YUV 等格式文件读取数据进行编码。

## 三、功能验证

完成上述配置并编译烧录固件后，您可以通过 `ffmpeg` 命令行工具或 `mediatool` 框架进行功能验证。

### 1、准备工作

在执行测试前，请将测试视频文件挂载到系统的文件系统中。

```bash
# 挂载hostfs，将主机目录 /path/to/your/video_files 映射到设备的 /stream 目录
mount -t hostfs -o fs=/path/to/your/video_files /stream
```

### 2、解码器验证

#### 使用 `ffmpeg` 命令

以下命令显式指定使用 `h264_v4l2m2m` 解码器，将 MP4 文件解码为 RGB32 格式，并直接输出到 Framebuffer 设备 (`/dev/fb0`) 进行显示。

```Bash
ffmpeg -vcodec h264_v4l2m2m -i /data/m2m-video-0.1s.mp4 -pix_fmt rgb32 -f fbdev /dev/fb0
```

#### 使用 `mediatool` 命令

当 FFmpeg 中只启用 `h264_v4l2m2m` 作为 H.264 解码器时，`mediatool` 会自动选择该解码器来播放视频。

```Bash
# 进入 mediatool 交互环境
mediatool

# 在 mediatool 中执行以下命令
open Video
prepare 0 url /stream/h264_aac_240p.mp4
start 0
```

### 3、编码器验证

#### 使用 `ffmpeg` 命令

以下命令将一个 YUV420P 格式的原始视频文件，通过 `h264_v4l2m2m` 硬件编码器压缩为 H.264 格式并封装成 MP4 文件。

```Bash
ffmpeg -y -video_size 256x144 -pix_fmt yuv420p \
      -i /data/256x144-yuv420p.yuv -vcodec h264_v4l2m2m /data/out.mp4
```

#### 使用 `mediatool` 命令

`mediatool` 可以通过构建不同的媒体图 (Graph) 来实现录像功能。

**示例 1: 使用 `moviesink_async` 进行录制**

`moviesink_async` 可以同时处理音视频流。

```Bash
# 进入 mediatool 交互环境
mediatool

# 在 mediatool 中执行以下命令
copen VideoSink
prepare 0 url /stream/output.mp4
send devsink@preview start
start 0
```

- **关键配置与说明**:

    - **缓冲区配置**: 要成功使用 V4L2 M2M 硬件编码器，必须满足缓冲区数量的约束条件。

        - 硬件编码器驱动 (`v4l2_m2m_enc`) 的输出缓冲区数量 (`num_capture_buffers`) 必须大于 `moviesink_async` 的数据队列深度 (`dat_max`)。
        - `moviesink_async` 的数据队列深度 (`dat_max`) 必须小于系统定义的视频请求缓冲区最大值 (`VIDEO_REQBUFS_COUNT_MAX`，通常默认为 3)。
        - 您也可以直接在 Graph 配置文件中，将 `moviesink_async` 节点的 `datqmax` 参数设置为一个较小的值（例如 2），以满足条件。

    - **编码器选择**: 只要 `h264_v4l2m2m` 是系统中唯一或优先的 H.264 编码器，`prepare` 命令中的 `video_codec` 参数无论是设置为 `h264` 还是 `h264_v4l2m2m`，最终都会路由到硬件编码器。
    - **启动数据流**: `send devsink@preview start` 命令用于启动上游的 Camera 数据流，可以在 `mediatool` 的任意阶段执行。

**示例 2: 使用** **`vmoviesink_async`** **进行纯视频录制**

**Encoder** **- mediatool录像  - vmoviesink_async**

`vmoviesink_async` 仅处理视频流。

**说明**：以下示例使用 `vmoviesink_async@vrtp` 是为了复用一个已存在的、为 RTP 流配置的 Graph 节点。在执行此测试时，您可以忽略其名称中的 `vrtp` 部分，它在此处仅作为节点标识符。

```Bash
# 进入 mediatool 交互环境
mediatool

# 在 mediatool 中执行以下命令
open vmoviesink_async@vrtp
prepare 0 url /stream/m2m-out.mp4 video_codec=h264_v4l2m2m
send devsink@preview start
start 0
```

## 四、附录：常用 FFmpeg 命令参考

- 解码 MP4 为 YUV 文件

    ```Bash
    ffmpeg -i input.mp4 -c:v rawvideo -pix_fmt yuv420p 256x144-yuv420p.yuv
    ```

- 播放原始 YUV 文件

    ```Bash
    ffplay -video_size 256x144 -pixel_format yuv420p 256x144-yuv420p.yuv
    ```

- 从 MP4 中提取 H.264 流文件

    ```Bash
    ffmpeg -i input.mp4 -c:v copy -frames:v 1 -f h264 frame.h264
    ```

- 编码 YUV 文件为 MP4

    ```Bash
    ffmpeg -y -video_size 1080x720 -pix_fmt yuv420p -i yuv420p.yuv out.mp4
    ```
