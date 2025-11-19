# ADB Commands

\[ English | [简体中文](./../../../zh-cn/quickstart/emulator/Android_Debug_Bridge_commands_zh-cn.md) \]

Android Debug Bridge (ADB) is a versatile command-line tool that lets you communicate with a device. `adb` provides access to a device's Unix shell, allowing you to run a variety of commands. It operates as a client-server program that consists of three components:

- Client: Sends commands. The client runs on your development machine and can be invoked from a command-line terminal by issuing an `adb` command.
- Daemon (adbd): Runs commands on a device. The daemon runs as a background process on each device.
- Server: Manages communication between the client and the daemon. The server runs as a background process on your development machine.

## I. How ADB Works

All adb clients use port 5037 to communicate with the adb server. When an adb client starts, it first checks whether an adb server process is already running. If not, it starts the server process. When the server starts, it binds to local TCP port 5037 and listens for commands from adb clients.

The server then sets up connections to all running devices. It finds emulators by scanning odd-numbered ports in the range 5555 to 5585 (the range used by the first 16 emulators). Once the server finds an adb daemon (adbd), it sets up a connection to that port.

Each emulator uses a pair of sequential ports: an even-numbered port for console connections and an odd-numbered port for adb connections. For example:

Emulator 1, console: 5554; Emulator 1, adb: 5555.

Emulator 2, console: 5556; Emulator 2, adb: 5557.

And so on. The emulator connected to adb on port 5555 is the same as the emulator whose console is listening on port 5554.

After the server has established connections to all devices, you can use adb commands to access them. Because the server manages connections to devices and handles commands from multiple adb clients, you can control any device from any client or script.

## II. Query for Devices

Before you can issue adb commands, you need to know which device instances are connected to the adb server. You can get a list of connected devices using the following command:

```bash
adb devices
```

adb prints the following status information for each device:

- Serial number: adb creates a string to uniquely identify the device by its port number. For example: `emulator-5554`
- State: The connection state of the device can be one of the following:

    - `offline`: The device is not connected to adb or is not responding.
    - `device`: The device is connected to the adb server. Note that this state does not imply that the guest system is fully booted and operational, as the device connects to adb while the system is still booting. After booting is complete, a device is typically in this state.
    - `no device`: There is no device connected.

### 1. Emulator not listed

The `adb devices` command has an edge-case sequence that causes a running emulator to not appear in the output, even though it is visible on your desktop. This happens when all of the following conditions are met:

- The adb server is not running.
- You use the `emulator` command with the `-port` or `-ports` option, specifying an odd-numbered port value between 5554 and 5584.
- The odd-numbered port you chose is not busy, so the connection can be made at the specified port number; or if it is busy, the emulator switches to another port that meets the requirement in the second condition.
- You start the adb server after starting the emulator.

## III. Send Commands to a Specific Device

To specify a target device for an adb command, follow these steps:

1. Use the `devices` command to get the serial number of the target device.
2. Once you have the serial number, use the `-s` option with your `adb` commands to specify it.

### 1. Set up port forwarding

You can use the `forward` command to set up arbitrary port forwarding, which forwards requests from a specific host port to a different port on a device. The following example sets up forwarding from host port 6100 to device port 7100:

```bash
adb forward tcp:6100 tcp:7100
```

The following example sets up forwarding from host port 6100 to `local:logd`:

```bash
adb forward tcp:6100 local:logd
```

This can be useful if you want to determine what is being sent to a specific port on the device. All received data is written to the system logging daemon and displayed in the device logs.

### 2. Push and pull files

You can use the `pull` and `push` commands to copy files to and from a device.

To copy a file or directory (and its subdirectories) from a device, use the following command:

```bash
adb pull remote local
```

To copy a file or directory (and its subdirectories) to a device, use the following command:

```bash
adb push local remote
```

Replace `local` and `remote` with the paths to the target files/directories on your development machine (local) and on the device (remote). For example:

```bash
adb push myfile.txt /sdcard/myfile.txt
```

### 3. Stop the adb server

In some cases, you might need to terminate the adb server process and then restart it to resolve an issue, such as when adb does not respond to a command.

To stop the adb server, use the `adb kill-server` command. You can then restart the server by issuing any adb command.

### 4. Issue adb commands

You can issue adb commands from a command line on your development machine or from a script. The format is:

```bash
adb [-d | -e | -s serial_number] command
```

If only one emulator is running or only one device is connected, the adb command is sent to that device by default. If multiple emulators are running and/or multiple devices are connected, you need to use the `-d`, `-e`, or `-s` option to specify the target device to which the command should be directed.

You can see a detailed list of all supported adb commands by using the following command:

```bash
adb --help
```

## IV. Issue Shell Commands

You can use the `shell` command to issue device commands through adb, or to start an interactive shell. To issue a single command, use the `shell` command as follows:

```bash
adb [-d |-e | -s serial_number] shell shell_command
```

To start an interactive shell on a device, use the `shell` command as follows:

```bash
adb [-d | -e | -s serial_number] shell
```

To exit an interactive shell, press `Control+D` or type `exit`.
