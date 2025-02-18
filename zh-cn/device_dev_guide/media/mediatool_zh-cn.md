# **Mediatool 工具说明**

[[English](./mediatool.md) | 简体中文]

采用 Mediatool 测试程序，用于测试 Media Framework API，可模拟实际使用场景。

## **配置 Mediatool 工具**

  配置使用 mediatool 工具的 CPU ,比如 AP :
```shell
CONFIG_MEDIA=y                        // 需要使用 Media 功能的 cpu, enable 该选项
CONFIG_MEDIA_TOOL=y                   // 开启mediatool 工具
CONFIG_MEDIA_SERVER_CPUNAME='audio'   // 提供Media 能力的 cpu name
 ```
 提供 media 能力（运行着 mediad ）的 CPU,  比如 AUDIO:
```shell
CONFIG_MEDIA_SERVER=y                 // 提供 Media 能力的 cpu, enable 该选项
CONFIG_MEDIA_SERVER_CONFIG_PATH="/etc/media/" // 设置media相关配置文件放置目录, 默认
CONFIG_MEDIA_SERVER_PROGNAME="mediad"         // media deamon 程序名字，默认
CONFIG_LIB_FFMPEG=y
CONFIG_LIB_FFMPEG_CONFIGURATION="--disable-sse --enable-avcodec
 --enable-avdevice --enable-avfilter --enable-avformat --enable-decoder='aac,aac_latm,flac,mp3float,pcm_s16le,libopus,libfluoride_sbc,libfluoride_sbc_packed' --enable-demuxer='aac,mp3,pcm_s16le,flac,mov,ogg,wav' --enable-encoder='aac,pcm_s16le,libopus,libfluoride_sbc' --enable-hardcoded-tables --enable-indev=nuttx --enable-ffmpeg --enable-ffprobe --enable-filter='adevsrc,adevsink,afade,amix,amovie_async,amoviesink_async,astats,astreamselect,aresample,volume' --enable-libopus --enable-muxer='opus,opusraw,pcm_s16le,wav' --enable-outdev=bluelet,nuttx --enable-parser='aac,flac' --enable-protocol='cache,file,http,https,rpmsg,tcp,unix' --enable-swresample --tmpdir='/log'"
CONFIG_LIB_PFW=y
```

## **Sim 环境运行 Mediatool**

1. 运行 ap ，audio 虚拟机：
   ```shell
   sudo ./nuttx
   ```
2. 挂载目录，/music 存放媒体文件，首先把host路径挂载当前核上（ap）：
   ```shell
   ap>mount -t hostfs -o fs=/home/jhd/music /music
   ```
3. 运行 mediatool 工具：
   ```shell
   ap>mediatool
   ```

## **测试方法**

- 播放音频文件( URL 模式 )：
   ```shell
   open Music
   prepare 0 url music/1.mp3          //采用 URL 模式播放
   start 0                            //启动播放
   stop 0                             //停止播放
   close 0                            //关闭播放
   ```

- 播放音频文件(Buffer模式)：
   ```shell
   open Music
   prepare 0 buffer /music/1.mp3      //采用 Buffer 模式播放
   start 0
   stop 0
   close 0
   ```
- 录制音频文件(URL模式)：
   ```shell
   copen cap
   prepare 0 url music/2.opus
   start 0                            //启动录制
   stop 0                             //停止录制
   close 0                            //关闭录制
   ```
- 录制音频文件(Buffer模式)：
   ```shell
   copen cap
   prepare 0 buffer /music/b3.opus format=opus:sample_rate=16000:ch_layout=mono
   start 0
   stop 0
   close 0
   ```
- 播放控制：
   ```shell
   pause 0                            //暂停播放
   resume 0                           //恢复播放
   seek 0 1000                        //跳转到1000ms处播放
   ```
- 调整音量：
   ```shell
   volume 0 50                       //设置音量为50%
   ```

- mediatool 提供 debug 指令，方便日志调试：
   ```shell
   mediatool>dump
   ```