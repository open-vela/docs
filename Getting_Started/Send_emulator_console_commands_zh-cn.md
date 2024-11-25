# 发送模拟器控制台命令

\[ [English](./Send_emulator_console_commands.md) | 简体中文 \]

每个正在运行的虚拟设备都提供了一个控制台，可用来查询和控制模拟设备的环境。

## 启动和停止控制台会话

如需访问控制台并输入命令，请从终端窗口中使用 `telnet` 连接到控制台端口，并提供身份验证令牌。每当控制台显示 `OK` 时，表明已可以开始接受命令。通常不会显示常见的命令提示符。

要连接到正在运行的虚拟设备的控制台，请执行以下操作：

1. 打开终端窗口并输入以下命令：

    ```
    telnet localhost console-port
    ```

    模拟器会监听端口 5554 到 5585 上的连接，并且仅接受来自 localhost 的连接。

    `adb devices` 命令也会输出正在运行的虚拟设备及其控制台端口号的列表。

2. 控制台显示 `OK` 后，输入 `auth auth_token` 命令。

    在输入控制台命令之前，模拟器控制台会进行身份验证。`auth_token` 必须与 `HOME` 目录中 `.emulator_console_auth_token` 文件的内容相符。

    如果该文件不存在，则 `telnet localhost console-port` 命令会创建该文件，其中包含一个随机生成的身份验证令牌。如需停用身份验证，请从 `.emulator_console_auth_token` 文件中删除令牌，或者创建一个空文件（如果该文件不存在）。

3. 连接到控制台后，输入控制台命令。

    输入 `help`、`help command` 或 `help-verbose` 可查看控制台命令的列表并了解特定的命令。

4. 如要退出控制台会话，请输入 `quit` 或 `exit`。

    下面是一个会话示例：

    ```
    $ telnet localhost 5554
    Trying ::1...
    telnet: connect to address ::1: Connection refused
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    Android Console: Authentication required
    Android Console: type 'auth <auth_token>' to authenticate
    Android Console: you can find your <auth_token> in
    '/Users/me/.emulator_console_auth_token'
    OK
    auth 123456789ABCdefZ
    Android Console: type 'help' for a list of commands
    OK
    help-verbose
    Android console command help:
        help|h|?         Prints a list of commands
        help-verbose     Prints a list of commands with descriptions
        ping             Checks if the emulator is alive
        automation       Manages emulator automation
        event            Simulates hardware events
        geo              Geo-location commands
        gsm              GSM related commands
        cdma             CDMA related commands
        crash            Crashes the emulator instance
        crash-on-exit    Simulates crash on exit for the emulator instance
        kill             Terminates the emulator instance
        restart          Restarts the emulator instance
        network          Manages network settings
        power            Power related commands
        quit|exit        Quits control session
        redir            Manages port redirections
        sms              SMS related commands
        avd              Controls virtual device execution
        qemu             QEMU-specific commands
        sensor           Manages emulator sensors
        physics          Manages physical model
        finger           Manages emulator finger print
        debug            Controls the emulator debug output tags
        rotate           Rotates the screen clockwise by 90 degrees
        screenrecord     Records the emulator's display
        fold             Folds the device
        unfold           Unfolds the device
        multidisplay     Configures the multi-display
        nodraw           turn on/off NoDraw mode. (experimental)
        resize-display   resize the display resolution to the preset size
        virtualscene-image  customize virtualscene image for virtulscene camera
        proxy            manage network proxy server settings
        phonenumber      set phone number for the device


    try 'help <command>' for command-specific help
    OK
    exit
    Connection closed by foreign host.
    ```

## 模拟器命令参考

### 常规命令

* `avd {stop|start|status|name}`

  查询、控制和管理虚拟设备，具体说明如下：

  * stop：停止设备的执行。

  * start：开始设备的执行。

  * status：查询虚拟设备状态，可以是 running 或 stopped。

  * name：查询虚拟设备名称。

* `kill`

  终止虚拟设备。

* `ping`

  检查虚拟设备是否正在运行。

* rotate

  以 45 度的增量逆时针旋转 AVD。

### 端口重定向

* `redir list`

  列出当前端口重定向。

* `redir add protocol:host-port:guest-port`

  添加新的端口重定向，具体说明如下：

  * `protocol`：必须是 tcp 或 udp。

  * `host-port`：要在主机上打开的端口号。

  * `guest-port`：要在模拟器上将数据传输到的端口号。

* `redir del protocol:host-port`

  删除端口重定向。

  * `protocol`：必须是 tcp 或 udp。

  * `host-port`：要在主机上打开的端口号。

### 地理位置

通过向模拟器发送 GPS 定位，设置向模拟器内运行的应用报告的地理位置。

* `geo fix longitude latitude [altitude] [satellites] [velocity]`

  向模拟器发送简单的 GPS 定位。 以十进制度为单位指定 `longitude` 和 `latitude`。使用 1 到 12 之间的数字指定用于确定位置的 `satellites` 数量，并以米为单位指定 `altitude`，以节为单位指定 `velocity`。

* `geo nmea sentence`

  向模拟设备发送 NMEA 0183 语句，就像是从模拟的 GPS 调制解调器发送的一样。让 sentence 以“$GP”开头。 目前仅支持“$GPGGA”和“$GPRCM”语句。以下示例是一个 GPGGA（全球定位系统定位数据）语句，它描述了 GPS 接收器接收的时间、位置和定位数据：
  
  ```
  geo nmea $GPGGA ,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx
  ```

### 虚假硬件事件

* `event types`

  列出所有虚假事件类型。对于包含代码的事件，代码数列在右侧的圆括号中。

  ```
  event types
  event <type> can be an integer or one of the following aliases:
      EV_SYN
      EV_KEY    (405 code aliases)
      EV_REL    (2 code aliases)
      EV_ABS    (27 code aliases)
      EV_MSC
      EV_SW     (4 code aliases)
      EV_LED
      EV_SND
      EV_REP
      EV_FF
      EV_PWR
      EV_FF_STATUS
      EV_MAX
  OK
  ```

* `event send types [types ...]`

  发送一个或多个虚假事件类型。

* `event codes type`

  列出指定虚假事件类型的事件代码。

* `event send type[:code]:[value] [...]`

  发送一个或多个虚假事件以及可选的代码和代码值。

  如需了解到底要发送哪个事件，可以在手动按模拟器上按钮的同时使用 adb 命令。

* `event text message`

  发送用于模拟按键的字符串。该消息必须是 UTF-8 字符串。 Unicode 消息会根据当前设备键盘进行反向映射，不受支持的字符会被静默舍弃。

### 电源状态控制

* `power display`

  显示电池和充电器状态。

* `power ac {on|off}`

  将交流电充电状态设为 on 或 off。

* `power status {unknown|charging|discharging|not-charging|full}`

  按照说明更改电池状态。

* `power present {true|false}`

  设置电池存在状态。

* `power health {unknown|good|overheat|dead|overvoltage|failure}`

  设置电池运行状况。

* `power capacity percent`

  将电池剩余电量状态设为 0 到 100 之间的百分比。

### 在模拟器上管理传感器

这些命令与 AVD 中可用的传感器有关。除了使用 `sensor` 命令之外，还可以在模拟器的 `Virtual sensors` 屏幕上的 `Accelerometer` 和 `Additional sensors` 标签页中查看和调整相关设置。

* `sensor status`

  列出所有传感器及其状态。下面是 sensor status 命令的输出示例：

  ```
  sensor status
  acceleration: enabled.
  gyroscope: enabled.
  magnetic-field: enabled.
  orientation: enabled.
  temperature: enabled.
  proximity: enabled.
  light: enabled.
  pressure: enabled.
  humidity: enabled.
  magnetic-field-uncalibrated: enabled.
  gyroscope-uncalibrated: enabled.
  hinge-angle0: disabled.
  hinge-angle1: disabled.
  hinge-angle2: disabled.
  heart-rate: disabled.
  rgbc-light: disabled.
  wrist-tilt: disabled.
  acceleration-uncalibrated: enabled.
  ```

* `sensor get sensor-name`

  获取 `sensor-name` 的设置。以下示例会获取加速度传感器的值：

  ```
  sensor get acceleration
  acceleration = 2.23517e-07:9.77631:0.812348
  ```

  以英文冒号 (:) 分隔的 `acceleration` 值是指虚拟传感器的 x、y 和 z 坐标。

* `sensor set sensor-name value-x:value-y:value-z`

  设置 sensor-name 的值。以下示例将加速度传感器设为以英文冒号分隔的 x、y 和 z 值。
  
  ```
  sensor set acceleration 2.23517e-07:9.77631:0.812348
  ```
