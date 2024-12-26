# Sending Emulator Console Commands

\[ English | [简体中文](./Send_emulator_console_commands_zh-cn.md) \]

Each running virtual device provides a console that lets you query and control the emulated device environment.

## Start and stop a console session

To access the console and enter commands, use `telnet` at a terminal window to connect to the console port and provide the authentication token.Whenever the console displays “OK”, it's ready to accept commands.A typical prompt is usually not displayed.

To connect to the console of a running virtual device, do the following:

1. Open a terminal window and enter the following command:

    ```bash
    telnet localhost console-port
    ```

    The emulator listens for connections on ports 5554 to 5585 and accepts connections from localhost only.

   Also, the `adb devices` command produces a list of running virtual devices and their console port numbers.

2. After the console displays “OK”, enter the “auth auth_token” command.

   Before you can enter console commands, the emulator console requires authentication."auth_token” must match the contents of the “.emulator_console_auth_token” file in your Home directory.

   If that file doesn't exist, the `telnet localhost console-port` command creates the file, which contains a randomly generated authentication token.To disable authentication, delete the token from the `.emulator_console_auth_token` file or create an empty file (if that file doesn't exist).

3. After you're connected to the console, enter console commands.

    Enter `help`, `help command`, or `help-verbose` to see a list of console commands and learn about specific commands.

4. To exit the console session, enter `quit` or `exit`.

   The following session is an example:

    ```bash
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

- `avd {stop|start|status|name}`

  Query, control and manage the virtual device, as follows:

  - stop: Stop the execution of the device.

  - start: Start the execution of the device.

  - status: Query the virtual device status, which can be running or stopped.

  - name: Query the virtual device name.

- `kill`

  Terminate the virtual device.

- `ping`

  Check whether the virtual device is running.

- rotate

  Rotate the AVD counterclockwise in 45 degree increments.

### Port redirection

- `redir list`

  List the current port redirection.

- `redir add protocol:host-port:guest-port`

  Add a new port redirection, as follows:

  - “protocol”: Must be either tcp or udp.

  - "host-port": The port number to open on the host.

  - "guest-port": The port number to route data to on the emulator.

- `redir del protocol:host-port`

  Delete a port redirection.

  - “protocol”: Must be either tcp or udp.

  - "host-port": The port number to open on the host.

### Geographic location

Set the geographic location reported to the apps running inside an emulator by sending a GPS locator to the emulator.

- `geo fix longitude latitude [altitude] [satellites] [velocity]`

  Send a simple GPS locator to the emulator. Specify “longitude” and “latitude” in decimal degrees.Use a number from 1 to 12 to specify the number of “satellites” used to determine the position, and specify “altitude” in meters and “velocity” in knots.

- `geo nmea sentence`

  Send an NMEA 0183 sentence to the emulated device as if it is sent from an emulated GPS modem.Start the sentence with "$GP". Only "$GPGGA" and "$GPRCM" sentences are currently supported.The following example is a GPGGA (Global Positioning System Fix Data) sentence that gets the time, position, and fix data for a GPS receiver:
  
  ```bash
  geo nmea $GPGGA ,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx
  ```

### Fake hardware events

- `event types`

  Lists all fake event types. For events that have codes, the number of codes is listed in parentheses on the right.

  ```bash
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

- `event send types [types ...]`

  Send one or more fake event types.

- `event codes type`

  List the event codes for the specified fake event type.

- `event send type[:code]:[value] [...]`

  Send one or more fake events with optional codes and code values.

  To discover exactly which event to send, you can use the adb command while manually pressing the buttons on the emulator.

- `event text message`

  Send a string of characters that simulate keystrokes.The message must be a UTF-8 string. Unicode messages are reverse-mapped according to the current device keyboard, and unsupported characters are discarded silently.

### Power state control

- `power display`

  Display battery and charger state.

- `power ac {on|off}`

  Set AC charging state to on or off.

- `power status {unknown|charging|discharging|not-charging|full}`

  Change battery status as specified.

- `power present {true|false}`

  Set battery presence state.

- `power health {unknown|good|overheat|dead|overvoltage|failure}`

  Set battery health state.

- `power capacity percent`

  Sets remaining battery capacity state as a percent from 0 to 100.

### Manage sensors on the emulator

These commands relate to the sensors available in AVD. In addition to using the “sensor” command, you can see and adjust the settings in the “Accelerometer” and “Additional sensors” tabs on the emulator’s “Virtual sensors” screen.

- `sensor status`

  List all sensors and their status.The following is an example of the “sensor status” command’s output:

  ```bash
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

- `sensor get sensor-name`

  Get the settings for "sensor-name". The following example gets the value for the acceleration sensor:

  ```bash
  sensor get acceleration
  acceleration = 2.23517e-07:9.77631:0.812348
  ```

  The “acceleration” values separated by colons(:) refer to the x, y, and z coordinates for the virtual sensors.

- `sensor set sensor-name value-x:value-y:value-z`

  Set the values for “sensor-name”.The following example set the acceleration sensor to the x, y, and z values separated by colons.

  ```bash
  sensor set acceleration 2.23517e-07:9.77631:0.812348
  ```
