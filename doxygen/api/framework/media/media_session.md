# media session API

Media Session的含义是"媒体会话"，每个媒体会话中都有控制者（Controller）和受控者（Player/Controllee）两个角色：
- 控制者：只想控制其他流或者接受状态变化通知，不会对流的创建和销毁负责。
- 受控者：掌握着某些流的播放状态，需要负责对这些流的创建，销毁，以及播放功能。

下面举几个例子：
- 我们作为音箱，播放来自手机的音乐：
    - 控制者：UI界面或者按钮传感器是控制者；
    - 受控者：与手机建立音频通道的蓝牙模块是受控者；
- 我们作为智能手表，播放音乐到耳机：
    - 控制者：在avrcp中承接停起指令的服务是控制者；
    - 受控者：音乐播放器是受控者。

## media_session.h

```eval_rst

.. doxygenfile:: media_session.h
  :project: doxygen

```
