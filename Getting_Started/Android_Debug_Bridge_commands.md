# Android Debug Bridge commands

\[ English | [简体中文](./Android_Debug_Bridge_commands_zh-cn.md) \]

Android Debug Bridge (`adb`) is a versatile command-line tool that lets you communicate with a device. `adb` provides access to a Unix shell that you can use to run a variety of commands on a device. It is a client-server program that includes three components:

* **A client**, which sends commands. The client runs on your development machine. You can invoke a client from a command-line terminal by issuing an `adb` command.

* **A daemon (adbd)**, which runs commands on a device. The daemon runs as a background process on each device.

* **A server**, which manages communication between the client and the daemon. The server runs as a background process on your development machine.

## How adb works

All adb clients use port 5037 to communicate with the adb server. When an adb client is started, it first checks to see if there is an adb server process already running. If not, it starts the server process. Once started, the server binds to local TCP port 5037 and listens for commands from the adb client.

The server then establishes connections to all running devices. It searches for emulators by scanning the odd-numbered ports between 5555 and 5585 (the range used for the first 16 emulators). Once the server finds the adb daemon (adbd), it connects to the appropriate port.

Each emulator uses a pair of sequential ports: an even-numbered port for console connections and an odd-numbered port for adb connections. For example:

Emulator 1, console: 5554; emulator 1, adb: 5555.

Emulator 2, console: 5556; emulator 2, adb: 5557.

And so on, the emulator that connects to adb at port 5555 is the same emulator that has the console listening on port 5554.

Once the server has established connections to all devices, you can access them using adb commands. Because the server manages connections to the devices and handles commands from multiple adb clients, you can control any device from any client or from a script.

## Query for devices

Before sending an adb command, you need to know which device instances are connected to the adb server. You can use the following command to query the list of connected devices:

```
adb devices
```

adb will output the following status information for each device:

* Serial number: adb will create a string that uniquely identifies the device by port number. For example: `emulator-5554`

* Status: The device's connection status can be one of the following:

* offline: The device is not connected to adb or is not responding.

* device: The device is connected to the adb server, but this status does not mean that the Guest system has been fully started and can run normally. It is possible that the system is still starting when the device is connected to adb. The device is usually in this operating state after the system has finished starting.

* no device: No device is connected.

### Emulator not listed

The adb devices command has a corner-case command sequence that causes running emulators to not show up in the adb devices output even though the emulators are visible on your desktop. This happens when all of the following conditions are true:

The adb server is not running.

* You use the emulator command with the -port or -ports option with an odd-numbered port value between 5554 and 5584.

* The odd-numbered port you chose is not busy, so the port connection can be made at the specified port number — or, if it is busy, the emulator switches to another port that meets the requirements in 2.

* You start the adb server after you start the emulator.

## Send commands to a specific device

If multiple devices are running, you must specify the target device when you issue the adb command. To specify the target, follow these steps:

* Use the `devices` command to get the serial number of the target.

* Once you have the serial number, use the -s option with the adb commands to specify the serial number.

## Set up port forwarding

Use the `forward` command to set up arbitrary port forwarding, which forwards requests on a specific host port to a different port on a device. The following example sets up forwarding of host port 6100 to device port 7100:

```
adb forward tcp:6100 tcp:7100
```

The following example sets up forwarding of host port 6100 to local:logd:

```
adb forward tcp:6100 local:logd
```

This could be useful if you are trying to detemine what is being sent to a given port on the device. All received data will be written to the system-logging daemon and displayed in the device logs.

## Copy files to and from a device

You can use the `pull` and `push` commands to copy files to and from a device.

To copy a file or directory (and its subdirectories) from a device, use the following command:

```
adb pull remote local
```

To copy a file or directory (and its subdirectories) to a device, use the following command:

```
adb push local remote
```

Replace local and remote with the path to the target file/directory on your development workstation (local) and device (remote), and use the following command:

```
adb push myfile.txt /sdcard/myfile.txt
```

## Stop the adb server

In some cases, you might need to terminate the adb server process and then restart it to resolve the problem. For example, this could be the case if adb does not respond to a command.

To stop the adb server, use the `adb kill-server` command. You can then restart the server by issuing any other adb command.

## Issue adb commands

Issue adb commands from a command line on your development machine or from a script using the following:

```
adb [-d | -e | -s serial_number] command
```

If there's only one emulator running or only one device connected, the adb command is sent to that device by default. If multiple emulators are running and/or multiple devices are attached, you need to use the `-d`, `-e`, or `-s` option to specify the target device to which the command should be directed.

You can see a detailed list of all supported adb commands using the following command:

```
adb --help
```

## Issue shell commands

You can use the `shell` command to issue device commands through adb or to start an interactive shell. To issue a single command, use the shell command like this:

```
adb [-d |-e | -s serial_number] shell shell_command
```

To start an interactive shell on a device, use the shell command like this:

```
adb [-d | -e | -s serial_number] shell
```

To exit an interactive shell, type exit.
