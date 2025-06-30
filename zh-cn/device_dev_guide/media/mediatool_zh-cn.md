# Mediatool 使用指南

[[English](../../../en/device_dev_guide/media/mediatool.md) | 简体中文]

Mediatool 是一款测试程序，用于验证 Media Framework API 的功能，可基于模拟的实际使用场景测试媒体框架。

## 一、配置 Mediatool 工具

### 1、配置使用 Mediatool 的 CPU

以下配置适用于需要使用 Mediatool 的 CPU，例如 AP：  

```shell
CONFIG_MEDIA=y                        # 启用需要使用 Media 功能的 CPU  
CONFIG_MEDIA_TOOL=y                   # 启用 Mediatool 工具  
CONFIG_MEDIA_SERVER_CPUNAME='audio'   # 提供 Media 功能的 CPU 名称  
```

### 2、配置提供 Media 功能的 CPU

以下配置适用于运行 mediad（提供 Media 能力）的 CPU，例如 AUDIO：

```shell
CONFIG_MEDIA_SERVER=y                               # 启用提供 Media 功能的 CPU  
CONFIG_MEDIA_SERVER_CONFIG_PATH="/etc/media/"       # 配置文件默认放置目录  
CONFIG_MEDIA_SERVER_PROGNAME="mediad"               # Media deamon 程序名称
CONFIG_LIB_FFMPEG=y
CONFIG_LIB_FFMPEG_CONFIGURATION="--disable-sse --enable-avcodec
 --enable-avdevice --enable-avfilter --enable-avformat --enable-decoder='aac,aac_latm,flac,mp3float,pcm_s16le,libopus,libfluoride_sbc,libfluoride_sbc_packed' --enable-demuxer='aac,mp3,pcm_s16le,flac,mov,ogg,wav' --enable-encoder='aac,pcm_s16le,libopus,libfluoride_sbc' --enable-hardcoded-tables --enable-indev=nuttx --enable-ffmpeg --enable-ffprobe --enable-filter='adevsrc,adevsink,afade,amix,amovie_async,amoviesink_async,astats,astreamselect,aresample,volume' --enable-libopus --enable-muxer='opus,opusraw,pcm_s16le,wav' --enable-outdev=bluelet,nuttx --enable-parser='aac,flac' --enable-protocol='cache,file,http,https,rpmsg,tcp,unix' --enable-swresample --tmpdir='/log'"
CONFIG_LIB_PFW=y
```

## 二、Sim 模拟环境运行 Mediatool

通过配置以下步骤运行 Mediatool 测试工具，验证模拟运行环境中的媒体功能。

1. 启动 AP 和 AUDIO 虚拟机：

    ```shell
    sudo ./nuttx
    ```

2. 挂载目录：将 `host` 路径挂载到当前核（AP）上的 `/music`，用于存放媒体文件：

    ```shell
    ap>mount -t hostfs -o fs=/home/jhd/music /music
    ```

3. 启动 Mediatool 工具运行测试：

    ```shell
    ap>mediatool
    ```

## 三、测试方法

以下是使用 Mediatool 工具的常见操作方法，包括媒体文件的播放、录制以及调试指令。

### 1、播放音频文件

- URL 模式播放：

    ```shell
    open Music  
    prepare 0 url music/1.mp3          # 采用 URL 模式播放  
    start 0                            # 启动播放  
    stop 0                             # 停止播放  
    close 0                            # 关闭播放  
    ```

- Buffer 模式播放：

    ```shell
    open Music  
    prepare 0 buffer /music/1.mp3      # 采用 Buffer 模式播放  
    start 0  
    stop 0  
    close 0  
    ```

### 2、录制音频文件

- URL 模式录制：

    ```shell
    copen cap  
    prepare 0 url music/2.opus  
    start 0                            # 启动录制  
    stop 0                             # 停止录制  
    close 0                            # 关闭录制  
    ```

- Buffer 模式录制：

    ```shell
    copen cap  
    prepare 0 buffer /music/b3.opus format=opus:sample_rate=16000:ch_layout=mono  
    start 0  
    stop 0  
    close 0  
    ```

### 3、播放控制指令

- 暂停播放：

    ```shell
    pause 0                            # 暂停播放  
    ```

- 恢复播放：

    ```shell
    resume 0                           # 恢复播放  
    ```

- 快速跳转播放：

    ```shell
    seek 0 1000                        # 跳转到 1000ms 处播放  
    ```

### 4、调节音量指令

- 设置音量大小：

    ```shell
    volume 0 50                        # 设置音量为50%
    ```

### 5、调试指令

- 使用 mediatool 提供的调试命令，方便查看日志，排查问题：

    ```shell
    mediatool>dump
    ```
