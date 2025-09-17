# Mediatool User Guide

[English | [简体中文](../../../zh-cn/device_dev_guide/media/mediatool_zh-cn.md)]

Mediatool is a test program used to verify the functionality of the Media Framework API. It allows for testing the media framework by simulating real-world usage scenarios.

## I. Configure the Mediatool

### 1. Configure the CPU that uses Mediatool

The following configuration applies to the CPU that will use Mediatool, for example, the AP:

```shell
CONFIG_MEDIA=y                        # Enable the CPU that requires Media functionality
CONFIG_MEDIA_TOOL=y                   # Enable the Mediatool
CONFIG_MEDIA_SERVER_CPUNAME='audio'   # Name of the CPU that provides Media functionality
 ```

### 2. Configure the CPU that provides Media functionality

The following configuration applies to the CPU running `mediad` (which provides Media capabilities), for example, the AUDIO CPU:

```shell
CONFIG_MEDIA_SERVER=y                               # Enable the CPU that provides Media functionality
CONFIG_MEDIA_SERVER_CONFIG_PATH="/etc/media/"       # Default directory for configuration files
CONFIG_MEDIA_SERVER_PROGNAME="mediad"               # Name of the Media daemon program
CONFIG_LIB_FFMPEG=y
CONFIG_LIB_FFMPEG_CONFIGURATION="--disable-sse --enable-avcodec --enable-avdevice --enable-avfilter --enable-avformat --enable-decoder='aac,aac_latm,flac,mp3float,pcm_s16le,libopus,libfluoride_sbc,libfluoride_sbc_packed' --enable-demuxer='aac,mp3,pcm_s16le,flac,mov,ogg,wav' --enable-encoder='aac,pcm_s16le,libopus,libfluoride_sbc' --enable-hardcoded-tables --enable-indev=nuttx --enable-ffmpeg --enable-ffprobe --enable-filter='adevsrc,adevsink,afade,amix,amovie_async,amoviesink_async,astats,astreamselect,aresample,volume' --enable-libopus --enable-muxer='opus,opusraw,pcm_s16le,wav' --enable-outdev=bluelet,nuttx --enable-parser='aac,flac' --enable-protocol='cache,file,http,https,rpmsg,tcp,unix' --enable-swresample --tmpdir='/log'"
CONFIG_LIB_PFW=y
```

## II. Run Mediatool in a Simulation Environment

Follow the steps below to run the Mediatool test tool and verify media functionality in the simulation environment.

1. Start the AP and AUDIO virtual machines:

    ```shell
    sudo ./nuttx
    ```

2. Mount the directory: Mount the `host` path to `/music` on the current core (AP). This directory is used to store media files:

    ```shell
    ap>mount -t hostfs -o fs=/home/jhd/music /music
    ```

3. Start the Mediatool to run tests:

    ```shell
    ap>mediatool
    ```

## III. Test Methods

The following sections describe common operating methods for the Mediatool, including media file playback, recording, and debugging commands.

### 1. Play Audio Files

- URL Mode Playback:

    ```shell
    open Music
    prepare 0 url music/1.mp3          # Play in URL mode
    start 0                            # Start playback
    stop 0                             # Stop playback
    close 0                            # Close playback
    ```

- Buffer Mode Playback:

    ```shell
    open Music
    prepare 0 buffer /music/1.mp3      # Play in Buffer mode
    start 0
    stop 0
    close 0
    ```

### 2. Record Audio Files

- URL Mode Recording:

    ```shell
    copen cap
    prepare 0 url music/2.opus
    start 0                            # Start recording
    stop 0                             # Stop recording
    close 0                            # Close recording
    ```

- Buffer Mode Recording:

    ```shell
    copen cap
    prepare 0 buffer /music/b3.opus format=opus:sample_rate=16000:ch_layout=mono
    start 0
    stop 0
    close 0
    ```

### 3. Playback Control Commands

- Pause Playback:

    ```shell
    pause 0                            # Pause playback
    ```

- Resume Playback:

    ```shell
    resume 0                           # Resume playback
    ```

- Seek Playback:

    ```shell
    seek 0 1000                        # Seek to 1000ms for playback
    ```

### 4. Volume Control Commands

- Set Volume Level:

    ```shell
    volume 0 50                        # Set volume to 50%
    ```

### 5. Debug Commands

- Use the debug command provided by mediatool to view logs and troubleshoot issues:

    ```shell
    mediatool>dump
    ```
