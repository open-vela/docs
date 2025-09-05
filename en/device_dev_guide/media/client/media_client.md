# Media Client Development Guide

[English | [简体中文](../../../../zh-cn/device_dev_guide/media/client/media_client.md)]

## I. Overview

Media Client provides a set of interfaces and tools for interacting with Media Server. It supports various media operations, such as audio and video playback, audio recording, audio focus management, media policy setting, and media session handling. Each module on the client side encapsulates both **synchronous** and **asynchronous** interfaces for user invocation. Users can opt for asynchronous operations for efficient communication with the server.

## II. Project Directory

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

## III. Module Introduction

The client side encapsulates synchronous and asynchronous interfaces for the **Media Focus**, **Media Graph**, **Media Policy**, and **Media Session** modules. Additionally, the client side supports both synchronous and asynchronous RPC interfaces for communication with the server.

### 1. Media Focus

The Media Focus module implements client-side management and request operations for focus signaling.

- Synchronous Interface:

    - `media_focus.c` provides synchronous interfaces for the client to interact with the server for Media Focus management.
    - This module supports user commands related to focus, such as the **`media_focus_request`** interface for requesting focus, abandoning Media Focus, and the **`media_focus_dump`** interface for printing focus log information.
    - Commands are forwarded to the server for processing through the **`media_proxy`** interface.

- Asynchronous Interface:

    - `media_uv_focus.c` provides interfaces for the client to asynchronously request and abandon Media Focus, communicating with the server via `media_uv`.
    - When requesting focus, a series of asynchronous operations are performed, including connecting to the server, sending a Ping request, starting to listen, and sending the focus request, ultimately invoking a user-defined focus callback function upon completion.
    - When abandoning focus, it sends an abandon request, disconnects from the server, and releases resources.

### 2. Media Graph

The client-side Media Graph module implements audio processing functionalities, encompassing operational interfaces for the Media Player and Media Recorder. It is primarily used to interact with Media Server to manage operations related to Media Player and Media Recorder, and it encapsulates both synchronous and asynchronous interfaces.

- Synchronous Interface:

    - `media_graph.c` provides a series of functions for synchronous interaction with the server.
    - It supports various player and recorder operations, such as open, close, prepare, play, pause, stop, seek, set attribute, and get attribute.

- Asynchronous Interface:

    - `media_uv_graph.c` provides a series of functions for interacting with the server in a `libuv`-based environment.
    - It supports various operations for **Media Player** and **Media Recorder**, including open, close, prepare, play, pause, stop, seek, set attribute, and get attribute.
    - It sends corresponding commands to the server via the **`media_uv_stream_send`** interface and sets up callback functions for server responses.

### 3. Media Policy

The client-side Media Policy provides interfaces for setting and getting various Media Policy parameters, enabling flexible control and querying of Media Policy through server interaction. It can be used to adjust audio settings, manage device usage, and control media playback features.

- Synchronous Interface:

    - `media_policy.c` provides synchronous interfaces for managing Policy, allowing the client to conveniently set and get various media-related parameters.
    - It supports managing mute mode, subscribing to policy changes, controlling audio device usage interfaces, and setting volume.

- Asynchronous Interface:

    - `media_uv_policy.c` provides interfaces for the client to asynchronously set and get various Policy-related parameters.
    - It supports getting audio mode, device usage status, and other parameters.

### 4. Media Session

The Media Session module in the Media Client is responsible for media session management. This includes functions such as opening and closing sessions, registering and unregistering, setting event callbacks and handling event notifications, performing playback control operations (like play, pause, stop, skip, and volume control), and querying session status and metadata.

- **Synchronous Interface:** `media_session.c`
- **Asynchronous Interface:** `media_uv_session.c`

## 5. Media RPC Communication

The client side encapsulates interfaces for communication with the server, supporting both synchronous and asynchronous methods.

- Synchronous RPC:

    - `media_proxy.c` provides a complete set of synchronous communication interfaces for client-server communication.
    - It features functionalities such as connection management, message sending and receiving, callback setup, and request handling.

- Asynchronous RPC:

    - `media_uv.c` provides the underlying interfaces for asynchronous media operations, used for communication and interaction with the media server.
    - It supports connecting to, disconnecting from, and reconnecting to the **media server**, as well as creating listeners and sending message packets.
    - The file uses the `libuv` library for asynchronous I/O operations, communicating with the media server via pipes. Message packet sending and receiving are managed through queues to ensure message order and reliability.
