# 多媒体 API

openvela 多媒体框架提供统一的音视频播放、录制、音频焦点管理、策略控制和媒体会话能力，同时包含语音唤醒与工具类接口。

## openvela 实现说明

- **编解码后端**：底层由 **FFmpeg** 提供音视频编解码、封装/解封装和滤镜能力，源码位于 `external/ffmpeg/`（LGPL v2.1+）
- **调用建议**：
    - 首选使用 openvela `framework/media` 封装（`media_player_*` / `media_recorder_*` 等），已集成音频焦点、策略控制、会话同步
    - 需要自定义 filter graph、直接编解码或探测非常规流媒体时，可直接使用 FFmpeg 原生 API，请参考 [FFmpeg 官方文档](https://ffmpeg.org/documentation.html)
- **FFmpeg 集成配置**（`external/ffmpeg/Kconfig`）：

    ```kconfig
    CONFIG_LIB_FFMPEG=y                # 主开关：启用 FFmpeg 库
    CONFIG_LIB_FFMPEG_CONFIGURATION="" # 传递给 FFmpeg ./configure 的参数，用于裁剪组件
    CONFIG_LIB_FFMPEG_TEST=n           # 是否编译 FFmpeg 测试目标
    CONFIG_UTILS_FFMPEG_PRIORITY=100   # ffmpeg 命令行工具的任务优先级
    CONFIG_UTILS_FFMPEG_STACKSIZE=51200 # ffmpeg 命令行工具的任务栈大小
    ```

    组件裁剪通过 `CONFIG_LIB_FFMPEG_CONFIGURATION` 字符串传给 FFmpeg 自带的 `./configure` 脚本。例如：

    ```kconfig
    CONFIG_LIB_FFMPEG_CONFIGURATION="--disable-everything --enable-decoder=mp3,aac --enable-demuxer=mov,mp4"
    ```

    具体可用的 `--enable-*` / `--disable-*` 参数请参考 FFmpeg 官方 `./configure --help`。

## 核心能力

- **[播放器](media_player.md)** — 音视频播放（本地/网络流/字节流）
- **[录制器](media_recorder.md)** — 音视频录制与图片捕获
- **[媒体会话](media_session.md)** — 控制器-被控端模式的播放控制与状态同步

## 音频策略

- **[音频焦点](media_focus.md)** — 多应用音频播放优先级协调
- **[音频策略](media_policy.md)** — 音频路由、设备管理、音量和模式切换

## 语音唤醒

- **[媒体触发器](media_trigger.md)** — 语音唤醒高层接口（声学模型加载 + 识别控制）
- **[声学模型](media_trigger_model.md)** — 底层声学模型操作（加载/属性/热词检测）

## 工具与调试

- **[媒体工具](media_utils.md)** — DTMF 信号生成、事件名查询、dump、自定义命令
