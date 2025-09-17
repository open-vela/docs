# getevent Tool Usage Guide

\[ English | [简体中文](../../../zh-cn/device_dev_guide/graphics/Getevent.md) \]

`getevent` is a command-line tool that monitors and displays real-time events from input devices such as touchscreens, keyboards, and mice. It provides detailed event data to help you debug input device drivers and applications.

## I. Features

`getevent` provides the following core functions:

- **Mouse Event Monitoring**: Tracks clicks, movements, and scroll wheel activity.
- **Multi-touch Capture**: Captures data such as coordinates and timestamps for each touch point.
- **Keyboard Key Detection**: Reports key codes and event types (e.g., press, release).
- **Automatic Device Discovery**: Scans the `/dev` directory by default and monitors all detected input devices.
- **Specific Device Monitoring**: Allows you to monitor one or more specific devices using command-line options.
- **Non-blocking I/O**: Uses a non-blocking mode with a 500-millisecond timeout to avoid suspending the system while waiting for events.
- **Safe Resource Management**: Ensures that resources are correctly released on exit (e.g., via `Ctrl+C`) to prevent memory or file descriptor leaks.

## II. Build Configuration

To enable the `getevent` tool, you must set the following options in the `openvela` board-level configuration file:

```Makefile
# Enable the getevent tool
CONFIG_GRAPHICS_INPUT_GETEVENT=y

# (Optional) Enable detailed debug information for getevent
CONFIG_GRAPHICS_INPUT_GETEVENT_DETAIL_INFO=y
```

## III. Usage Instructions

You can run `getevent` from the `openvela` command-line terminal (such as NSH).

### Command Examples

- **Monitor all automatically detected devices:**

    ```Bash
    getevent
    ```

- **Monitor a specific mouse device:**

    ```Bash
    getevent -m /dev/mouse0
    ```

- **Monitor a specific touchscreen device:**

    ```Bash
    getevent -t /dev/input0
    ```

- **Monitor a specific keyboard device:**

    ```Bash
    getevent -k /dev/kbd0
    ```

- **Monitor multiple devices simultaneously:**

    ```Bash
    getevent -m /dev/mouse0 -t /dev/input0
    ```

To stop monitoring, press `Ctrl+C`, and the program will terminate safely.

### Parameter Descriptions

| Parameter | Description                                                         |
| :-------- | :------------------------------------------------------------------ |
| -m        | Specifies the mouse device to monitor. Example: `/dev/mouse0`       |
| -t        | Specifies the touchscreen device to monitor. Example: `/dev/input0` |
| -k        | Specifies the keyboard device to monitor. Example: `/dev/kbd0`      |

### Output Example

When you run `getevent`, it first lists the devices being opened and then prints event data in real-time.

```Bash
goldfish-armv7a-ap> getevent

[getevent]: opening /dev/input0
[getevent]: ioctl TSIOC_GETMAXPOINTS: 1
[getevent]: opening /dev/kbd0
[getevent]: opening /dev/mouse0

# Touchscreen event data
[getevent]: touch event: /dev/input0
[getevent]:    npoints : 1
[getevent]: Point      : 0
[getevent]:      flags : 11             # Touch event flags (e.g., press, move)
[getevent]:          x : 493
[getevent]:          y : 312
[getevent]:  timestamp : 31272800

# Keyboard event data
[getevent]: keyboard event: /dev/kbd0
[getevent]:          type : 0           # 0 represents KEY_DOWN (press), 1 represents KEY_UP (release)
[getevent]:          code : 57          # Key code, e.g., SPACE key

[getevent]: keyboard event: /dev/kbd0
[getevent]:          type : 1
[getevent]:          code : 57

# Mouse event data
[getevent]: mouse event: /dev/mouse0
[getevent]:    buttons : 00              # Bitmask of button states
[getevent]:          x : 14              # Relative displacement in the horizontal direction
[getevent]:          y : -16             # Relative displacement in the vertical direction
```

## IV. Prerequisites

To successfully build and run `getevent`, your system must meet the following prerequisites:

- **Input Subsystem**: You must enable the `openvela` input subsystem in your configuration. This subsystem provides the underlying drivers and event handling mechanisms required for `getevent` to process events. For details, see the [Input Driver Development Guide](./Input_Driver_Guide.md).
- **System Log (Recommended)**: For easier debugging, we recommend enabling system log output in your kernel configuration. When `CONFIG_GRAPHICS_INPUT_GETEVENT_DETAIL_INFO` is enabled, `getevent` can print more detailed diagnostic messages.
