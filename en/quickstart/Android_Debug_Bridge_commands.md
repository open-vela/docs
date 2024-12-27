# ADB commands

\[ English | [简体中文](./../../zh-cn/quickstart/Android_Debug_Bridge_commands_zh-cn.md) \]

ADB is a versatile command-line tool that lets you communicate with a device.With access to the device’s Unix shell, ADB allows you to run a variety of commands on the device.It is a client-server program that includes three components:

- A client that sends commands. The client runs on a development workstation. You can invoke a client from a command-line terminal by issuing an ”adb” command.

- A daemon (adbd) that runs commands on a device: The “adbd” program runs as a background process on each device.

- A server: It manages communication between the client and the daemon. The server runs as a background process on your development workstation.

## How ADB works

All adb clients use port 5037 to communicate with the adb server.When you start an adb client, the client first checks whether there is an adb server process already running.If there isn't, it starts the server process.When the server starts, it binds to local TCP port 5037 and listens for commands sent from adb clients.

The server then sets up connections to all running devices.It locates emulators by scanning odd-numbered ports within the range from 5555 to 5585 (the range used by the first 16 emulators).Once the server finds an adb daemon (adbd), it sets up a connection to that port.

Each emulator uses a pair of sequential ports: an even-numbered port for console connections and an odd-numbered port for adb connections.For example:

Emulator 1, console: 5554; Emulator 1, adb: 5555.

Emulator 2, console: 5556; Emulator 2, adb: 5557.

And so on. The emulator connected to adb on port 5555 is the same as the emulator whose console listens on port 5554.

Once the server has set up connections to all devices, you can use adb commands to access these devices.As the server manages connections to devices and handles commands from multiple adb clients, you can control any device from any client or from a script.

## Query for devices

Before issuing adb commands, it is necessary to know what device instances are connected to the adb server. Use the following command to generate a list of connected devices:

```bash
adb devices
```

adb produces the following status information for each device:

- Serial number: adb creates a string to uniquely identify the device by its port number.For example: “emulator-5554”

- State: The connection state of the device can be one of the following:

  - offline: The device is not connected to adb or is not responding.

  - device: The device is connected to the adb server. However, this does not imply that the Guest system is fully booted and operational. The device can be connected to adb while the system is still booting.After boot-up, this is the normal operational state of a device.

  - no device: There is no device connected.

### Emulators not listed

The adb devices command has a corner-case command sequence that causes running emulators to not show up in the output of adb devices (even though the emulators are visible on your desktop).This happens when all of the following conditions are true:

- The adb server is not running.

- You use the emulator command when the”-port” or “-ports”option is given an odd-numbered port value between 5554 and 5584.

- The odd-numbered port chosen is idle and can establish a port connection at the specified port number, or if that port is busy, the emulator switches to another port that meets the second requirement.

- You start the adb server after starting the emulator.

## Send commands to a specific device

To specify the target when issuing an adb command, follow these steps:

1. Use the devices command to get the serial number of the target.

2. Once you have the serial number, use the “-s” option and the adb command to specify the serial number.

## Set up port forwarding

Use the forward command to set up arbitrary port forwarding, which forwards requests on a specific host port to a different port on the device.Forwarding of host port 6100 to device port 7100 is set up as shown below:

```bash
adb forward tcp:6100 tcp:7100
```

Forwarding of host port 6100 to local:logd is set up as shown below:

```bash
adb forward tcp:6100 local:logd
```

This could be useful if you are trying to determine what is being sent to a given port on the device.All received data will be written to the system-logging daemon and displayed in the device logs.

## Push files to or pull files from a device

Use the “pull” and “push” commands to copy files to and from a device.

To copy a file or directory (and its sub-directories) from the device, use the following command:

```bash
adb pull remote local
```

To copy a file or directory (and its sub-directories) to the device, use the following command:

```bash
adb push local remote
```

Replace local and remote with the paths to the target files/directory on your development workstation (local) and on the device (remote). Use the following command:

```bash
adb push myfile.txt /sdcard/myfile.txt
```

## Stop the adb server

In some cases, you might need to terminate the adb server process and then restart it to resolve the problem. An example is that adb does not respond to a command.

To stop the adb server, use the “adb kill-server” command. Then, restart the server by issuing any other adb command.

## Issue adb commands

Issue adb commands from a command line on your development workstation or from a script. For example:

```bash
adb [-d | -e | -s serial_number] command
```

If there is only one emulator running or only one device connected, the adb command is sent to that device by default.If multiple emulators are running and/or multiple devices are attached, you need to use the “-d”, “-e” or “-s”option to specify the target device to which the command should be directed.

You can see a detailed list of all supported adb commands with the following command:

```bash
adb --help
```

## Issue shell commands

You can use the shell command to issue device commands through adb or to start an interactive shell.To issue a single command, use the shell command shown below:

```bash
adb [-d |-e | -s serial_number] shell shell_command
```

To start an interactive shell on a device, use the shell command shown below:

```bash
adb [-d | -e | -s serial_number] shell
```

To exit an interactive shell, press “Control+D” or enter “exit”.
