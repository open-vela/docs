
# **Media Framework**

[English | [简体中文](../../../zh-cn/device_dev_guide/media/media_framework.md)]

## I. Overview

The Media Framework is a library for processing audio and video, providing a rich set of APIs for application development. It adopts a **Client-Server (C/S) architecture**, where the client interface packs commands and sends them to the server via RPC. The server's loop then performs the actual work. The Media Framework supports playback and recording of various audio and video formats and features a distributed architecture, allowing it to run on multiple CPUs.

<img src="./images/MediaFramework.jpg" alt="Media Daemon Architecture Diagram" width="75%">

## II. Features

The main functional modules of the Media Framework include **Media Player**, **Media Recorder**, **Media Focus**, **Media Policy**, and **Media Session**. The **Media Player** and **Media Recorder** are encapsulated by the **Media Graph** module.

### 1. Media Player

- **Playback Service**: Provides the ability to create a player instance and control playback.
- **Format Support**: Supports a wide range of audio and video formats to ensure broad compatibility.
- **Playback Control**: Offers comprehensive playback controls, such as play, pause, stop, and seek, to meet various user demands for audio and video playback.

### 2. Media Recorder

- **Recording Service**: Provides the ability to create a recorder instance and control recording.
- **Format Support**: Supports a wide range of audio and video formats to ensure broad compatibility.
- **Recording Control**: Offers comprehensive recording controls, such as start, pause, and stop recording, to meet various user demands for audio and video recording.

### 3. Media Focus

Through its focus management mechanism, it effectively handles competition for media focus among multiple applications. It ensures that only one application holds the media focus and plays media at any given time. Users can subscribe to focus events, participate in the **focus preemption** logic, and receive behavioral suggestions from the focus manager, ensuring a smooth user experience.

### 4. Media Policy

Media Policy uses **PFW** to construct various states, such as routing and audio policies. It can be extended with plugins to support features like processing FFmpeg commands and setting device parameters. Furthermore, by writing a policy configuration file and setting parameters, the system can alter global states of the Graph according to predefined policies, such as switching I/O device paths and controlling volume, providing users with a highly customizable media processing environment.

### 5. Media Session

It uses a controller-and-controllable architecture to achieve fine-grained control over media playback and state notifications. It provides functionalities such as registering controllers and controllables, sending control commands, handling event notifications, and updating media metadata, facilitating unified management and control over multiple media clients.

### 6. Media RPC

A dual-socket communication model is used, with two independent sockets for communication, regardless of whether it spans across cores.

- **Trans socket** is responsible for transmitting control commands from the Client to the Server and returning RPC execution results.
- **Notify socket** is responsible for transmitting notifications from the Server to the Client, which are delivered to the user via callbacks.

<img src="./images/MediaRPC.jpg" alt="Media RPC Architecture Diagram" width="75%">

- **Universality**: The RPC mechanism is universal for Player, Recorder, Session, Policy, and Focus users, allowing applications to communicate between different CPUs.
- **Mode Support**: The Media Framework supports both synchronous and asynchronous RPC modes.

    - **Synchronous Mode**: The client sends a request and waits for the server's response. This is suitable for scenarios requiring immediate feedback.
    - **Asynchronous Mode**: The client sends a request and returns immediately. The server notifies the client via a callback after processing the request. This provides an efficient communication mechanism, ensuring data reliability and real-time delivery.

## III. Media Framework Architecture

<img src="./images/Distributed_Server_Architecture.jpg" alt="Media Distributed Server Architecture Diagram" width="75%">

- [Client Model](./client/media_client.md)
- [Server Model](./server/media_server.md)

## IV. **Test Media Framework**

 The Mediatool test program is used to test the Media Framework API, which can simulate real-world usage scenarios.

[Mediatool User Guide](./mediatool.md)
