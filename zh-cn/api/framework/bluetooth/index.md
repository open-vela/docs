\[ [English](../../../../en/api/framework/bluetooth/index.md) | 简体中文 \]

# 蓝牙 API

openvela 蓝牙框架提供完整的蓝牙协议栈接口，支持经典蓝牙（BR/EDR）和低功耗蓝牙（BLE），涵盖从底层连接管理到上层应用规范。

## 核心协议

- **[GAP](bt_gap.md)**（通用访问规范）— 设备发现、连接管理、配对与安全
- **[GATT](bt_gatt.md)**（通用属性规范）— BLE 数据属性读写与通知
- **[设备管理](bt_device.md)** — 远程设备配对、连接、属性查询

## 经典蓝牙规范

- **[A2DP](bt_a2dp.md)**（高级音频分发）— 高质量立体声音乐传输
- **[HFP](bt_hfp.md)**（免提规范）— 蓝牙通话功能
- **[HID](bt_hid.md)**（人机接口设备）— 键盘、鼠标、游戏手柄
- **[SPP](bt_spp.md)**（串口仿真）— 数据透传
- **[PAN](bt_pan.md)**（个人局域网）— 网络共享与蓝牙组网

## 低功耗蓝牙规范

- **[CS](bt_cs.md)**（Channel Sounding）— 蓝牙信道探测测距与定位
