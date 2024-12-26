# Run Build Artifacts on openvela Emulator

\[ English | [简体中文](./Run_Vela_on_Vela_Emulator_zh-cn.md) \]

## Overview of openvela Emulator

openvela Emulator simulates an openvela device on a computer, allowing developers to test applications and drivers on a variety of devices. A physical device is not needed.

openvela Emulator is based on Android Emulator, with improvements and enhancements.

openvela Emulator offers the following advantages:

- An exclusive operating mode for loading and running the mirror of openvela. It’s a way to skip Android-specific operations
- Loading openvela's own kernel in openvela mode
- Loading openvela's own system partition in openvela mode
- `NMEA` calibration support for a GNSS emulator

The following Hosts are supported:

- Linux x86\_64
- Linux arm64
- macOS x86\_64
- macOS aarch64
- Windows x64

The following Targets are supported:

- arm
- arm64
- x86
- x86\_64

The following goldfish-specific drivers have been implemented in openvela:

- Qemu Pipe
- ADB
- Battery
- Camera
- GNSS
- Graphic
- Sensors

## Run openvela Emulator

1. Switch to the root directory of openvela repository, and start an instance of openvela Emulator by passing the option “vela” to emulator.sh

    ```Bash
    ./emulator.sh vela
    ```

2. Once openvela is started and gets into “nsh”, run the following command inside “openvela-ap":

    ```Bash
    lvgldemo &
    ```
    
   This appears after execution:
    ![img](images/001.png)

3. Exit the openvela Emulator instance, as shown below:

    ![img](images/002.png)

## Control openvela Emulator

You can control a running instance of openvela Emulator with ADB or the console.

- [ADB commands](./Android_Debug_Bridge_commands.md)
- [Send emulator console commands](./Send_emulator_console_commands.md)

## Debug with openvela Emulator

- [Debugging with openvela Emulator](./Debugging_Vela_with_Vela_Emulator.md)
