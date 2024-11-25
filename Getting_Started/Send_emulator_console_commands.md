# Send emulator console commands

\[ English | [简体中文](./Send_emulator_console_commands_zh-cn.md) \]

Each running virtual device provides a console that lets you query and control the emulated device environment.

## Start and stop a console session

To access the console and enter commands from a terminal window, use `telnet` to connect to the console port and provide your authentication token. Each time the console displays `OK`, it's ready to accept commands. There isn't a typical prompt.

To connect to the console of a running virtual device:

1. Open a terminal window and enter the following command:

    ```
    telnet localhost console-port
    ```

    The emulator listens for connections on ports 5554 to 5585 and accepts connections from localhost only.

    The `adb devices` command prints a list of running virtual devices and their console port numbers.

2. After the console displays `OK`, enter the `auth auth_token` command.

    Before you can enter console commands, the emulator console requires authentication. `auth_token` must match the contents of the `.emulator_console_auth_token` file in your home directory.

    If that file doesn't exist, the `telnet localhost console-port` command creates the file, which contains a randomly generated authentication token. To disable authentication, delete the token from the `.emulator_console_auth_token` file or create an empty file if it doesn't exist.

3. After you're connected to the console, enter console commands.

    Enter `help`, `help command`, or `help-verbose` to see a list of console commands and learn about specific commands.

4. To exit the console session, enter `quit` or `exit`.

    Here's an example session:

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

## Emulator command reference

### General commands

* `avd {stop|start|status|name}`

  Queries, controls, and manages the virtual device, as follows:

  * stop: Stops the execution of the device.

  * start: Starts the execution of the device.

  * status: Queries the virtual device status, which can be running or stopped.

  * name: Queries the virtual device name.

* `kill`

  Terminates the virtual device.

* `ping`

  Checks whether the virtual device is running.

* rotate

  Rotates the AVD counterclockwise in 45 degree increments.

### Port redirection

* `redir list`

  Lists the current port redirection.

* `redir add protocol:host-port:guest-port`

  Adds a new port redirection, as follows:

  * `protocol`: Must be either tcp or udp.

  * `host-port`: The port number to open on the host.

  * `guest-port`: The port number to route data to on the emulator.

* `redir del protocol:host-port`

  Deletes a port redirection.

  * `protocol`: Must be either tcp or udp.

  * `host-port`: The port number to open on the host.

### Geographic location

Sets the geographic location reported to the apps running inside an emulator by sending a GPS fix to the emulator.

* `geo fix longitude latitude [altitude] [satellites] [velocity]`

  Sends a simple GPS fix to the emulator. Specify `longitude` and `latitude` in decimal degrees. Use a number from 1 to 12 to specify the number of `satellites` to use to determine the position, and specify `altitude` in meters and `velocity` in knots.

* `geo nmea sentence`

  Sends an NMEA 0183 sentence to the emulated device as if it were sent from an emulated GPS modem. Start sentence with '$GP'. Only '$GPGGA' and '$GPRCM' sentences are currently supported. The following example is a GPGGA (Global Positioning System Fix Data) sentence that gets the time, position, and fix data for a GPS receiver:
  
  ```
  geo nmea $GPGGA ,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx
  ```

### Fake hardware events

* `event types`

  Lists all fake event types. For events that have codes, the number of codes is listed in parentheses on the right.

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

  Sends one or more fake event types.

* `event codes type`

  Lists the event codes for the specified fake event type.

* `event send type[:code]:[value] [...]`

  Sends one or more fake events with optional codes and code values.

  To discover exactly which event to send, you can use the adb command while manually pressing the buttons on the emulator.

* `event text message`

  Sends a string of characters that simulate keypresses. The message must be a UTF-8 string. Unicode posts are reverse-mapped according to the current device keyboard, and unsupported characters are discarded silently.

### Power state controls

* `power display`

  Displays battery and charger state.

* `power ac {on|off}`

  Sets AC charging state to on or off.

* `power status {unknown|charging|discharging|not-charging|full}`

  Changes battery status as specified.

* `power present {true|false}`

  Sets battery presence state.

* `power health {unknown|good|overheat|dead|overvoltage|failure}`

  Sets battery health state.

* `power capacity percent`

  Sets remaining battery capacity state as a percent from 0 to 100.

### Manage sensors on the emulator

These commands relate to which sensors are available in the AVD. Besides using the `sensor` command, you can see and adjust the settings in the emulator in the `Virtual sensors` screen in the `Accelerometer` and `Additional sensors` tabs.

* `sensor status`

  Lists all sensors and their status. The following is example output for the sensor status command:

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

  Gets the settings for `sensor-name`. The following example gets the value for the acceleration sensor:

  ```
  sensor get acceleration
  acceleration = 2.23517e-07:9.77631:0.812348
  ```

  The `acceleration` values separated by colons(:) refer to the x, y, and z coordinates for the virtual sensors.

* `sensor set sensor-name value-x:value-y:value-z`

  Sets the values for sensor-name. The following example sets the acceleration sensor to the x, y, and z values separated by colons.
  
  ```
  sensor set acceleration 2.23517e-07:9.77631:0.812348
  ```
