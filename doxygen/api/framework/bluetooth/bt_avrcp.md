# 蓝牙 AVRCP API 开发指南

**音视频远程控制规范 (AVRCP)** 定义了在音视频分发场景中，具备音视频控制功能的蓝牙设备之间确保互操作性所需的特性和流程。

AVRCP 定义了两种设备角色：

- **控制端 (Controller, CT)**：发起事务的设备，负责向目标端发送命令帧。
  
    - *典型设备*：个人电脑、PDA、手机、遥控器，或车载系统、耳机等 AV 设备。

- **目标端 (Target, TG)**：接收命令帧并生成相应响应帧的设备。

    - *典型设备*：音频/视频播放器、录音机、电视、调谐器、放大器或耳机。

### 连接与流媒体说明

在 openvela 蓝牙系统中，AVRCP 的连接状态包括：

- **DISCONNECTED** (已断开)
- **CONNECTING** (连接中)
- **CONNECTED** (已连接)
- **DISCONNECTING** (断开中)

> **注意**：AVRCP 仅负责控制信令，**不处理**音视频流数据的传输。支持此规范的设备通常需要同时实现**高级音频分发规范 (A2DP)** 和/或**视频分发规范 (VDP)** 以支持流媒体传输。

## 1. 通用接口 (Common)

本节包含 AVRCP 通用的数据结构与定义。

```eval_rst

.. doxygenfile:: bt_avrcp.h
  :project: doxygen
```

## 2. AVRCP 控制端 (Controller)

AVRCP Controller 应用程序主要用于向目标设备发送控制指令并获取信息。

**主要功能**：

- **属性获取**：应用程序可以从 AVRCP Target 设备检索当前播放歌曲的媒体元素属性信息（如歌名、艺术家等）。
- **回调注册**：应用程序需向蓝牙服务注册连接状态回调和元素属性回调。
- **事件通知**：当 AVRCP 连接状态发生变化，或收到 TG 返回的属性信息响应时，蓝牙服务将通过相应的回调函数通知应用程序。

### AVRCP Controller API 详情

```eval_rst

.. doxygenfile:: bt_avrcp_control.h
  :project: doxygen
```

## 3. AVRCP 目标端 (Target)

AVRCP Target 应用程序主要用于响应控制指令并上报播放器状态。

**主要功能**：

- **回调注册**：应用程序可向蓝牙服务注册多种回调函数，包括：

    - 连接状态变更回调
    - 播放器状态请求回调 (Player status request)
    - 注册通知请求回调 (Register notification request)
    - 面板操作回调 (Panel operation，如音量旋钮、按键操作)

- **被动响应**：当相关事件发生时，蓝牙服务通过回调通知应用程序。
- **主动通知**：如果 CT 注册了播放器状态通知，当 TG 设备的播放器状态发生变化时（例如暂停、切歌），TG 将主动向 CT 发送通知。

**支持的通知事件 (Notification Events)**：

- `NOTIFICATION_EVT_PLAY_STATUS_CHANGED` (0x01): 播放状态变更
- `NOTIFICATION_EVT_TRACK_CHANGED`: 曲目变更
- `NOTIFICATION_EVT_TRACK_END`: 曲目结束
- `NOTIFICATION_EVT_TRACK_START`: 曲目开始
- `NOTIFICATION_EVT_PLAY_POS_CHANGED`: 播放位置变更
- `NOTIFICATION_EVT_BATTERY_STATUS_CHANGED`: 电池状态变更
- `NOTIFICATION_EVT_SYSTEM_STATUS_CHANGED`: 系统状态变更
- `NOTIFICATION_EVT_APP_SETTING_CHANGED`: 应用设置变更
- `NOTIFICATION_EVT_NOW_PLAYING_CONTENT_CHANGED`: 当前播放内容变更
- `NOTIFICATION_EVT_AVAILABLE_PLAYERS_CHANGED`: 可用播放器变更
- `NOTIFICATION_EVT_ADDRESSED_PLAYER_CHANGED`: 被控播放器变更
- `NOTIFICATION_EVT_UIDS_CHANGED`: UID 变更
- `NOTIFICATION_EVT_VOLUME_CHANGED`: 音量变更
- `NOTIFICATION_EVT_FLAG_INTERIM`: 临时响应标志

### AVRCP Target API 详情

```eval_rst

.. doxygenfile:: bt_avrcp_target.h
  :project: doxygen
```
