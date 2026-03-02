# Media Session API

Media Session（媒体会话）实现控制者与受控者之间的媒体控制通信。每个媒体会话包含两种角色：

- 控制者（Controller）：发送控制指令或接收状态变化通知，不负责音频流的创建和销毁。
- 受控者（Controllee）：管理音频流的播放状态，负责音频流的创建、销毁和播放控制。

以下是两个典型场景：

- 音箱播放来自手机的音乐：
    - 控制者：UI 界面或按钮传感器
    - 受控者：与手机建立音频通道的蓝牙模块
- 智能手表播放音乐到耳机：
    - 控制者：在 AVRCP 中承接停起指令的服务
    - 受控者：音乐播放器

## media_session.h

```eval_rst

.. doxygenfile:: media_session.h
  :project: doxygen

```
