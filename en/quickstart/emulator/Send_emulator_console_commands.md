# Sending Emulator Console Commands

\[ English | [简体中文](./../../../zh-cn/quickstart/emulator/Send_emulator_console_commands_zh-cn.md) \]

Each running virtual device provides a console that you can use to query and control the emulated device environment.

## I. Starting and Stopping a Console Session

To access the console and enter commands, use `telnet` from a terminal window to connect to the console port and provide an authentication token. Whenever the console displays `OK`, it indicates that it is ready to accept commands. A common command prompt is usually not displayed.

To connect to the console of a running virtual device, do the following:

1. Open a terminal window and enter the following command:

    ```bash
    telnet localhost console-port
    ```

    The emulator listens for connections on ports 5554 to 5585 and accepts connections from localhost only.

    Also, the `adb devices` command produces a list of running virtual devices and their console port numbers.

2. After the console displays `OK`, enter the `auth <auth_token>` command.

    The emulator console requires authentication before you can enter commands. The `<auth_token>` must match the contents of the `.emulator_console_auth_token` file in your `HOME` directory.

    If this file does not exist, the `telnet localhost <console-port>` command creates it with a randomly generated authentication token. To disable authentication, delete the token from the `.emulator_console_auth_token` file or create an empty file if it doesn't exist.

3. After connecting to the console, you can enter console commands.

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

## II. Emulator Command Reference

### 1. General Commands

- `avd {stop|start|status|name}`

    Queries, controls, and manages the virtual device as described below:

    - stop: Stop the execution of the device.
    - start: Start the execution of the device.
    - status: Query the virtual device status, which can be running or stopped.
    - name: Query the virtual device name.

- `kill`

    Terminate the virtual device.

- `ping`

    Check whether the virtual device is running.

- `rotate`

    Rotate the AVD counterclockwise in 45 degree increments.

### 2. Port Redirection

- `redir list`

    List the current port redirection.

- `redir add protocol:host-port:guest-port`

    Adds a new port redirection, as described below:

    - `protocol`: Must be `tcp` or `udp`.
    - `host-port`: The port number to open on the host.
    - `guest-port`: The port number to which data is transferred on the emulator.

- `redir del protocol:host-port`

    Delete a port redirection.

    - `protocol`: Must be `tcp` or `udp`.
    - `host-port`: The port number to close on the host.

### 3. Geolocation

Sets the geographic location reported to apps running inside the emulator by sending it a GPS fix.

- `geo fix longitude latitude [altitude] [satellites] [velocity]`

    Sends a simple GPS fix to the emulator. Specify `longitude` and `latitude` in decimal degrees. Specify the number of `satellites` used to determine the location with a number from 1 to 12. Specify `altitude` in meters and `velocity` in knots.

- `geo nmea sentence`

    Sends an `NMEA 0183` sentence to the emulated device, as if it were sent from a simulated GPS modem. The sentence must start with "$GP". Currently, only "$GPGGA" and "$GPRMC" sentences are supported. The following example is a GPGGA (Global Positioning System Fix Data) sentence, which describes the time, position, and fix data received by the GPS receiver:
  
    ```bash
    geo nmea $GPGGA ,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx
    ```

### 4. Simulated Hardware Events

- `event types`

    Lists all simulated event types. For events that include codes, the code aliases are listed in parentheses on the right.

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

    Sends one or more simulated event types.

- `event codes type`

    Lists the event codes for a specified simulated event type.

- `event send type[:code]:[value] [...]`

    Sends one or more simulated events with optional codes and code values.

    To determine which event to send, you can use `adb` commands while manually pressing buttons on the emulator.

- `event text message`

    Sends a string of characters to simulate key presses. The message must be a UTF-8 string. Unicode messages are reverse-mapped based on the current device keyboard, and unsupported characters are silently discarded.

### 5. Power State Control

- `power display`

    Displays the battery and charger status.

- `power ac {on|off}`

    Sets the AC charging state to `on` or `off`.

- `power status {unknown|charging|discharging|not-charging|full}`

    Changes the battery status as specified.

- `power present {true|false}`

    Sets the battery presence state.

- `power health {unknown|good|overheat|dead|overvoltage|failure}`

    Sets the battery health status.

- `power capacity percent`

    Sets the remaining battery capacity as a percentage from 0 to 100.

### 6. Managing Sensors on the Emulator

These commands relate to the sensors available in the AVD. In addition to using the `sensor` command, you can view and adjust settings in the `Accelerometer` and `Additional sensors` tabs on the emulator's `Virtual sensors` screen.

- `sensor status`

    Lists all sensors and their statuses. Below is an example output of the `sensor status` command:

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

    Gets the settings for a `sensor-name`. The following example gets the value for the accelerometer:

    ```bash
    sensor get acceleration
    acceleration = 2.23517e-07:9.77631:0.812348
    ```

    The colon-separated (`:`) values for `acceleration` refer to the x, y, and z coordinates of the virtual sensor.

- `sensor set sensor-name value-x:value-y:value-z`

    Sets the value for a `sensor-name`. The following example sets the accelerometer to the specified colon-separated x, y, and z values.

    ```bash
    sensor set acceleration 2.23517e-07:9.77631:0.812348
    ```
