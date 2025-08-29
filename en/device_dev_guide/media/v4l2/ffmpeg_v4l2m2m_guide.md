# FFmpeg V4L2 M2M Usage Guide

[English | [简体中文](../../../../zh-cn/device_dev_guide/media/v4l2/ffmpeg_v4l2m2m_guide.md)]

## I. Overview

This document provides developers with a detailed guide on enabling V4L2 M2M (Video4Linux2 Memory-to-Memory) hardware acceleration for FFmpeg on the `openvela` platform.

V4L2 M2M is a standard Linux kernel framework designed specifically for memory-to-memory video processing devices that do not have display hardware, such as video codecs.

By integrating FFmpeg with hardware drivers that support V4L2 M2M, the system can offload video encoding and decoding tasks (like H.264) from the CPU to dedicated hardware units, thereby significantly improving processing efficiency and overall system performance.

## II. Environment and Configuration

This guide uses the `simulator` platform as an example.

### 1. System Configuration (Kconfig)

In `menuconfig`, you must enable the following core configuration options related to video processing to ensure that the video framework and simulator drivers are compiled into the system.

```Makefile
# Enable the video framework
CONFIG_VIDEO=y
CONFIG_DRIVERS_VIDEO=y
CONFIG_VIDEO_STREAM=y

# Enable the simulator video codec drivers
CONFIG_SIM_VIDEO_DECODER=y
CONFIG_SIM_VIDEO_ENCODER=y

CONFIG_VIDEOUTILS_OPENH264=y
CONFIG_VIDEOUTILS_LIBX264=y
```

### 2. FFmpeg Configuration (`defconfig`)

You need to modify the `CONFIG_LIB_FFMPEG_CONFIGURATION` macro in your `defconfig` file to enable the V4L2 M2M-related codecs in the FFmpeg library's build parameters.

#### Enabling the V4L2 M2M Decoder

1. Locate the `CONFIG_LIB_FFMPEG_CONFIGURATION` option.
2. In its `--enable-decoder` parameter list, add `h264_v4l2m2m`.
3. To ensure the hardware decoder is used during testing, you can remove the pure software `h264` decoder from the `--enable-decoder` list.

#### Enabling the V4L2 M2M Encoder

1. Locate the `CONFIG_LIB_FFMPEG_CONFIGURATION` option.
2. In its `--enable-encoder` parameter list, add `h264_v4l2m2m`.
3. In its `--enable-demuxer` parameter list, ensure `rawvideo` is added to support reading data from raw formats like YUV for encoding.

## III. Functional Verification

After completing the above configurations and flashing the compiled firmware, you can verify the functionality using the `ffmpeg` command-line tool or the `mediatool` framework.

### 1. Preparation

Before running the tests, mount the test video files into the system's file system.

```bash
# Mount hostfs, mapping the host directory /path/to/your/video_files to the device's /stream directory
mount -t hostfs -o fs=/path/to/your/video_files /stream
```

### 2. Decoder Verification

#### Using the `ffmpeg` Command

The following command explicitly specifies the `h264_v4l2m2m` decoder to decode an MP4 file into RGB32 format and output it directly to the Framebuffer device (`/dev/fb0`) for display.

```Bash
ffmpeg -vcodec h264_v4l2m2m -i /data/m2m-video-0.1s.mp4 -pix_fmt rgb32 -f fbdev /dev/fb0
```

#### Using the `mediatool` Command

When `h264_v4l2m2m` is the only enabled H.264 decoder in FFmpeg, `mediatool` will automatically select it to play videos.

```Bash
# Enter the mediatool interactive environment
mediatool

# Execute the following commands in mediatool
open Video
prepare 0 url /stream/h264_aac_240p.mp4
start 0
```

### 3. Encoder Verification

#### Using the `ffmpeg` Command

The following command takes a raw video file in YUV420P format and compresses it into H.264 format using the `h264_v4l2m2m` hardware encoder, then muxes it into an MP4 file.

```Bash
ffmpeg -y -video_size 256x144 -pix_fmt yuv420p \
      -i /data/256x144-yuv420p.yuv -vcodec h264_v4l2m2m /data/out.mp4
```

#### Using the `mediatool` Command

`mediatool` can perform recording by constructing different media graphs.

**Example 1: Recording with `moviesink_async`**

`moviesink_async` can process both audio and video streams simultaneously.

```Bash
# Enter the mediatool interactive environment
mediatool

# Execute the following commands in mediatool
copen VideoSink
prepare 0 url /stream/output.mp4
send devsink@preview start
start 0
```

- **Key Configurations and Notes**:

    - **Buffer Configuration**: To successfully use the V4L2 M2M hardware encoder, buffer count constraints must be met.

        - The number of output buffers for the hardware encoder driver (`v4l2_m2m_enc`), `num_capture_buffers`, must be greater than the data queue depth (`dat_max`) of `moviesink_async`.
        - The data queue depth (`dat_max`) of `moviesink_async` must be less than the system-defined maximum for video request buffers (`VIDEO_REQBUFS_COUNT_MAX`, which usually defaults to 3).
        - Alternatively, you can directly set the `datqmax` parameter of the `moviesink_async` node to a smaller value (e.g., 2) in the Graph configuration file to meet the condition.

    - **Encoder Selection**: As long as `h264_v4l2m2m` is the only or preferred H.264 encoder in the system, setting the `video_codec` parameter in the `prepare` command to either `h264` or `h264_v4l2m2m` will ultimately route to the hardware encoder.
    - **Starting the Data Stream**: The `send devsink@preview start` command is used to start the upstream Camera data stream and can be executed at any stage in `mediatool`.

**Example 2: Video-only Recording with `vmoviesink_async`**

Encoder - mediatool recording - vmoviesink_async

`vmoviesink_async` processes only the video stream.

> **Note**: The following example uses `vmoviesink_async@vrtp` to reuse an existing Graph node configured for an RTP stream. When running this test, you can ignore the `vrtp` part of its name; it serves only as a node identifier here.

```Bash
# Enter the mediatool interactive environment
mediatool

# Execute the following commands in mediatool
open vmoviesink_async@vrtp
prepare 0 url /stream/m2m-out.mp4 video_codec=h264_v4l2m2m
send devsink@preview start
start 0
```

## IV. Appendix: Common FFmpeg Command Reference

- Decode an MP4 to a YUV file:

    ```Bash
    ffmpeg -i input.mp4 -c:v rawvideo -pix_fmt yuv420p 256x144-yuv420p.yuv
    ```

- Play a raw YUV file:

    ```Bash
    ffplay -video_size 256x144 -pixel_format yuv420p 256x144-yuv420p.yuv
    ```

- Extract an H.264 stream from an MP4 file:

    ```Bash
    ffmpeg -i input.mp4 -c:v copy -frames:v 1 -f h264 frame.h264
    ```

- Encode a YUV file into an MP4:

    ```Bash
    ffmpeg -y -video_size 1080x720 -pix_fmt yuv420p -i yuv420p.yuv out.mp4
    ```
