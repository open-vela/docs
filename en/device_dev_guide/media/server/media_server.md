# Media Server Development Guide

[English | [简体中文](../../../../zh-cn/device_dev_guide/media/server/media_server.md)]

## I. Overview

Media Server provides a comprehensive set of features based on an event-loop model to handle various media events and client interactions, offering users functions such as audio and video playback, audio/video recording, focus management, policy enforcement, and session control.

## II. Project Directory

```tree
.
├── focus_stack.c
├── focus_stack.h
├── media_daemon.c
├── media_focus.c
├── media_graph.c
├── media_policy.c
├── media_server.c
├── media_server.h
├── media_session.c
├── media_stub.c
└── README.md
```

## III. Module Introduction

### 1. Media Daemon

Media Daemon is the core of Media Server, responsible for creating and managing various Media modules such as `Media Focus`, `Media Graph`, `Media Session`, and `Media Policy`. Its core principle is to use the `poll` function to listen on the `RPC socket fd` and the `message queue fd` registered by audio/video device drivers, in order to process RPC commands and trigger FFmpeg operations.

<img src="../images/server/Media_Daemon.jpg" alt="Media Daemon Architecture Diagram" width="75%">

The main work of Media Daemon is carried out in a loop, the general steps are as follows:

- Initialize instances of various modules, such as Media Focus.
- Get event file descriptors (fds) from each module via the `media_get_pollfds` interface.
- Use `poll` to block and wait for events. `poll` returns when an event is detected.
- Process the event. When `poll` returns, call `media_poll_available` to handle the event.
- Execute a `run once` cycle (mainly for FFmpeg) to ensure effective resource management and scheduling.

### 2. Media Focus

The Media Focus module is an important part of the Media Server, designed to provide playback policies for scenarios where multiple audio streams are mixed together. It helps to ensure that only one audio stream is played as the primary audio content at a time, while other audio streams are either downgraded to secondary streams or paused. The media focus mechanism is a cooperative preemption type, allowing applications to still play music without using media focus, but they cannot access the audio focus management system, which may impact user experience.

- The default configuration file for audio event type interactions is located at `/etc/media`.
- The input for audio event types is based on the various `MEDIA_SCENARIO_XXX` macros in the `media wrapper`. It currently includes 11 types of audio events.
- It supports functions such as applications **requesting focus**, **abandoning focus**, and receiving **focus change notifications**.

### 3. Media Graph

The principle of Media Graph is to link the `inputs` and `outputs` of audio/video-related `filters` together to form playback and recording pipelines. The main strategies are as follows:

- Load the `graph` configuration file to create and configure the Media Graph and its corresponding `filters`.
- Provide a series of functions to handle `filter` commands and events, including operations like **open**, **close**, **play**, **pause**, **stop**, **set event callback**, and **process command queue**.
- Encapsulate the operation interfaces for Media Player and Media Recorder, calling the FFmpeg library to implement playback and recording functionalities.

### 4. Media Policy

The server-side Media Policy module provides a series of functions to handle media policy settings, retrieval, and notifications. It offers a unified interface to APPs across different projects, **translating user's routing and volume control information into control commands for device drivers**. In different projects, Policy uses different configuration files to handle the mapping of control commands from the Policy interface. The Media Policy strategy is implemented through configuration files:

- Modify the FFmpeg `filter graph` configuration file; Policy controls the `graph`'s `filters` to manage volume and pipeline control.
- Write `pfw` configuration files to implement plugin extensions and other features.

### 5. Media Server

The Media Server module listens on different types of sockets to receive connection requests from clients and uses callback functions to process the received data. It supports the following functions:

- Create and destroy server instances.
- The `media_server_get_pollfds` interface gets a list of file descriptors for polling.
- The `media_server_poll_available` handles file descriptor events.
- `media_server_notify` sends notifications to specific connections and manages connection data.

### 6. Media Session

The server-side Media Session module plays a key role in the media framework. Through a controller-controlee architectural design, it achieves efficient management of media playback and accurate status notifications.

- **Controller**: Responsible for managing other streams, including receiving status change notifications or querying information, but is not responsible for stream creation and destruction.
- **Controlee**: Controls the playback status of certain streams, is responsible for the creation, destruction, and playback functions of these streams, and must update its own status information in a timely manner.

Here is a scenario of playing music from a phone on a speaker:

- **Controller**: The UI is the controller, responsible for interacting with the user and issuing playback commands.
- **Controlee**: The Bluetooth module is the controlee, responsible for establishing the audio channel with the phone, managing music playback, and maintaining its own state.
