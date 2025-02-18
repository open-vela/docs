# **Media Client**

[[English](./README.md)|简体中文]

## **概述**

Media Client 提供了一组与 Media Server 进行交互的接口和工具。它支持各种媒体操作，如播放音频和视频、录制音频、管理音频焦点、设置媒体策略以及处理媒体会话等。Client 端的各个模块分别封装了**同步接口**和**异步接口**，以供用户调用。用户可以选择使用异步操作并与服务器进行高效通信。

## **项目目录**
```tree
.
├── media_dtmf.c
├── media_focus.c
├── media_graph.c
├── media_policy.c
├── media_proxy.c
├── media_proxy.h
├── media_session.c
├── media_uv.c
├── media_uv_focus.c
├── media_uv_graph.c
├── media_uv.h
├── media_uv_policy.c
├── media_uv_session.c
├── py_mediatool.py
└── README.md
```
## **模块介绍**

 Client 端封装了 Media Focus、Media Graph、Media Policy、Media Session 各个模块的同步接口和异步接口。此外，Client 端也支持同步RPC和异步RPC的接口，用于和Server通信。

### **Media Focus**

 Media Focus 模块实现了客户端对 Focus 信令的管理与请求操作。
- 同步接口：
  - **media_focus.c** 为 Client 提供了与 Server 交互以管理 Media Focus 的同步接口。
  - 该模块支持接收用户关于Focus的指令，如请求 Focus 的 **media_focus_request** 接口、释放 Media Focus 以及打印 Focus 日志信息的 **media_focus_dump** 接口。
  - 通过 **media_proxy** 接口将命令转发给 Server 端处理。
- 异步接口：
  - **media_uv_focus.c** 提供 Client 异步请求和释放 Media Focus，通过 media_uv 与 Server 进行通信。
  - 在请求焦点时，会进行一系列的异步操作，包括连接服务器、发送 Ping 请求、开始监听、发送焦点请求等，最终调用用户定义的 Focus 回调函数返回。
  - 放弃焦点时，发送放弃请求并断开与服务器的连接，释放资源等。

### **Media Graph**

 Client 端的 Media Graph 模块实现了对音频处理的功能，涵盖媒体播放器（Media Player）和媒体录制器（Media Recorder）的操作接口。其主要用于与 Media Server 交互以管理 Media Player 和 Media Recorder 的相关操作，且分别封装了同步接口和异步接口。
- 同步接口：
  - 由 **media_graph.c** 提供一系列函数，可与 Server 进行同步交互。
  - 支持播放器和录制器的各种操作，如打开、关闭、准备、播放、暂停、停止、定位、设置属性、获取属性等。
- 异步接口：
  - **media_uv_graph.c** 提供一些系列函数用于在基于 libuv 的环境下与 Server 交互。
  - 支持 **Media Player**和 **Media Recorder** 的各种操作，包括打开、关闭、准备、播放、暂停、停止、定位、设置属性、获取属性等。
  - 通过 **media_uv_stream_send** 接口将相应的指令发送给 Server，并设置 Server 响应的回调函数。

### **Media Policy**

 Client 端的 Media Policy 提供了设置和获取各种 Media Policy 参数的接口，通过与服务器交互实现对 Media Policy 的灵活控制和查询，可用于调整音频设置、管理设备使用及控制媒体播放特性。
- 同步接口：
  - **media_policy.c** 提供管理 Policy 的同步接口，客户端可方便设置和获取各种媒体相关参数。
  - 支持管理静音模式、订阅 Policy 变化、控制音频设备使用接口以及设置音量等。
- 异步接口：
  - **media_uv_policy.c** 提供 Client 以异步方式设置和获取各种Policy相关参数的接口。
  - 支持获取音频模式、设备使用状态等。
### **Media Session**

Media Session 在 Media Client 中负责媒体会话管理，包括打开和关闭会话、注册与取消注册、设置事件回调及处理事件通知、进行播放控制操作（如开始、暂停、停止、切换歌曲、增减音量等）以及查询会话状态和元数据等功能。
- 同步接口：**media_session.c**
- 异步接口：**media_uv_session.c**

### **Media RPC通信**

Client 端封装了和 Server 通信的接口，支持同步和异步两种方式。
- 同步 RPC ：
  - **media_proxy.c** 提供了一套完整的同步通信接口，用于 Client 和 Server 同步通信。
  - 具备连接管理、消息发送与接收、回调设置以及请求处理等功能。
- 异步RPC：
  - **media_uv.c** 提供了媒体异步操作的底层接口，用于与媒体服务器进行通信和交互。
  - 支持连接到**media server**、以及与**Server**断开连接、重新连接、创建监听器和发送消息包等。
  - 文件中使用了UV库进行异步 I/O 操作，通过管道与媒体服务器进行通信。消息包的发送和接收通过队列进行管理，确保消息的顺序和可靠性。
