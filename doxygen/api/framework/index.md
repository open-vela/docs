# 应用框架 (Application Framework)

openvela 应用框架为上层应用提供了统一的系统能力接口，涵盖进程间通信、蓝牙与连接管理、多媒体、电话服务、图形界面、安全可信执行等核心子系统。开发者可通过这些 API 快速构建 IoT 及智能设备应用，而无需关注底层硬件差异。

框架按功能领域划分为以下模块：

- **Binder** — 进程间通信（IPC）框架，提供跨进程的服务调用能力
- **蓝牙 (Bluetooth)** — 蓝牙协议栈接口，支持 BLE、经典蓝牙及多种 Profile（A2DP、HFP、HID 等）
- **电话服务 (Telephony)** — 蜂窝网络通信接口，涵盖通话、短信、数据连接、SIM 卡管理等
- **多媒体 (Media)** — 音视频播放与录制框架
- **连接服务 (Connectivity)** — 设备互联能力，包括投屏（MiPlay）、数字车钥匙、跨进程通信（XPC）等
- **系统服务 (Services)** — 应用管理（AMS）与权限管理（PMS）等核心系统服务
- **Feature** — 系统能力（SystemCapability）查询接口
- **快应用 (QuickApp)** — 轻量级应用运行时框架
- **工具库 (Utils)** — 日志（Log）与性能追踪（Trace）等通用工具
- **KVDB** — 轻量级键值对持久化存储
- **安全 (Security)** — 基于 OP-TEE 的可信执行环境（TEE）接口
- **uORB** — 发布/订阅消息总线，用于模块间的异步数据通信

```eval_rst

.. toctree::
    :maxdepth: 2

    binder/binder
    bluetooth/index
    telephony/index
    media/index
    connectivity/index
    services/index
    feature/index
    quickapp/index
    utils/index
    kvdb
    security
    uorb

```
