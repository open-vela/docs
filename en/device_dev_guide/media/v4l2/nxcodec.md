# nxcodec User Guide

[English | [简体中文](../../../../zh-cn/device_dev_guide/media/v4l2/nxcodec.md)]

## I. Overview

`nxcodec` is a command-line test tool used to verify the functionality of V4L2 (Video4Linux2) M2M (Memory-to-Memory) Codec drivers. It supports both encoding and decoding operations for video streams.

## II. Prerequisites

Before running `nxcodec` tests, you need to configure the system and prepare the necessary test files.

### 1. Build Configuration

You must enable `nxcodec` and its dependencies in `menuconfig`.

1. Enable the `nxcodec` tool:

    In `menuconfig`, enable the following option:

    ```Makefile
    CONFIG_SYSTEM_NXCODEC=y
    ```

2. Ensure dependencies are enabled:

    `nxcodec` depends on the V4L2 framework and related drivers. Ensure the following core configurations are enabled:

    ```Makefile
    # V4L2 core support
    CONFIG_VIDEO=y
    CONFIG_DRIVERS_VIDEO=y
    CONFIG_VIDEO_STREAM=y

    # Example Codec driver (replace with your hardware driver as needed)
    CONFIG_SIM_VIDEO_DECODER=y
    CONFIG_SIM_VIDEO_ENCODER=y

    # Codec algorithm library
    CONFIG_VIDEOUTILS_OPENH264=y
    CONFIG_VIDEOUTILS_LIBX264=y
    ```

3. Enable the host filesystem (Optional):

    When testing in a simulator (`sim`) environment, enable `hostfs` to easily access test files on the host machine:

    ```Makefile
    CONFIG_FS_HOSTFS=y
    ```

### 2. Prepare the Filesystem (Optional)

If running in a simulator environment, use the following command to mount the host directory containing test files into the openvela filesystem.

```Makefile
# Mount the host directory /path/from/your/host/machine to /stream in openvela
nsh> mount -t hostfs -o fs=/path/from/your/host/machine /stream
```

## III. Command Reference

### 1. Command Format

The basic command format for `nxcodec` is as follows:

```Bash
nsh> nxcodec -d <device> -s <wxh> -f <in_format> -i <infile> -f <out_format> -o <outfile>
```

```bash
# Request help information
ap> nxcodec -h
NxCodec Version: 1.00
Usage: nxcodec -d <devname> [options] -i <infile> [options] -o <outfile>

Options:
  -d | --device    Video device name
  -s | --size      Size of stream
  -f | --format    Format of stream
  -i | --infile    Input filename for M2M devices
  -o | --outfile   Outputs stream to filename
  -h | --help      Print this help message
```

### 2. Parameter Descriptions

| **Short Option** | **Long Option** | **Description**                                                                                                                                                                                       |
| :--------------- | :-------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-d`             | `--device`      | Specifies the V4L2 Codec device node path, e.g., `/dev/video1`.                                                                                                                                       |
| `-s`             | `--size`        | Specifies the video stream resolution in `widthxheight` format, e.g., `256x144`.                                                                                                                      |
| `-f`             | `--format`      | **[Important]** Specifies the format for the input or output stream. The position of this parameter determines its scope: it defines the format for the file immediately following it (`-i` or `-o`). |
| `-i`             | `--infile`      | Specifies the path to the input file.                                                                                                                                                                 |
| `-o`             | `--outfile`     | Specifies the path to the output file.                                                                                                                                                                |
| `-h`             | `--help`        | Displays the help message and exits.                                                                                                                                                                  |

## IV. Test Examples

The following examples demonstrate how to use `nxcodec` to perform decoding and encoding operations.

### 1. Decoding Test (H.264 -> YUV)

This operation uses the decoder device (`/dev/video1`) to decode an H.264 encoded video file into a raw YUV format file.

Decode command:

```Bash
nsh> nxcodec -d /dev/video1 -s 256x144 -f H264 -i /stream/256x144.h264 -f YU12 -o /stream/256x144-yuv420p-out.yuv
```

Command Breakdown:

- `-d /dev/video1`: Specifies the decoder device path as `/dev/video1`.
- `-s 256x144`: Specifies the video stream resolution as `256x144`.
- `-f H264`: Specifies the input video stream format as H.264.
- `-i /stream/256x144.h264`: Specifies the input video file path as `/stream/256x144.h264`.
- `-f YU12`: Specifies the output video stream pixel format as YU12.
- `-o /stream/256x144-yuv420p-out.yuv`: Specifies the output YUV file path as `/stream/256x144-yuv420p-out.yuv`.

Simplified command: If the driver supports automatic detection of the input stream format and resolution, you can omit the `-f` (input format) and `-s` parameters.

```Bash
nsh> nxcodec -d /dev/video1 -i /stream/256x144.h264 -o /stream/256x144-yuv420p-out.yuv
```

### 2. Encoding Test (YUV -> H.264)

This operation uses the encoder device (`/dev/video2`) to encode a raw YUV format video file into an H.264 stream file.

Mount host filesystem (optional, required in the simulator environment):

```Bash
nsh> mount -t hostfs -o fs=/path/from/ /stream
```

Encode command:

```Bash
nsh> nxcodec -d /dev/video2 -s 256x144 -f YU12 -i /stream/256x144-yuv420p.yuv -f H264 -o /stream/256x144-out.h264
```

This command uses the `nxcodec` tool to encode the input YUV video file and writes the encoded stream to a specified output file.

The parameters are described as follows:

- `-d /dev/video2`: Specifies the encoder device path as `/dev/video2`.
- `-s 256x144`: Specifies the input video stream resolution as `256x144`.
- `-f YU12`: Specifies the input video stream pixel format as YU12.
- `-i /stream/256x144-yuv420p.yuv`: Specifies the input video file path.
- `-f H264`: Specifies the output video stream encoding format as H.264.
- `-o /stream/256x144-out.h264`: Specifies the output video stream file path.
