\[ English | [简体中文](../../../../zh-cn/api/framework/bluetooth/index.md) \]

# Bluetooth API

The openvela Bluetooth framework provides a complete Bluetooth stack interface, supporting Classic Bluetooth (BR/EDR) and Bluetooth Low Energy (BLE), covering everything from low-level connection management to upper-layer application profiles.

## Core Protocols

- **[GAP](bt_gap.md)** (Generic Access Profile) — Device discovery, connection management, pairing and security
- **[GATT](bt_gatt.md)** (Generic Attribute Profile) — BLE data attribute read/write and notifications
- **[Device Management](bt_device.md)** — Remote device pairing, connection, and property queries

## Audio and Media

- **[A2DP](bt_a2dp.md)** (Advanced Audio Distribution Profile) — High-quality stereo music streaming
- **[HFP](bt_hfp.md)** (Hands-Free Profile) — Bluetooth call functionality

## Positioning and Ranging

- **[CS](bt_cs.md)** (Channel Sounding) — Bluetooth channel sounding for distance measurement and positioning

## Data and Peripherals

- **[HID](bt_hid.md)** (Human Interface Device) — Keyboards, mice, game controllers
- **[SPP](bt_spp.md)** (Serial Port Profile) — Data pass-through
- **[PAN](bt_pan.md)** (Personal Area Network) — Network sharing and Bluetooth networking
