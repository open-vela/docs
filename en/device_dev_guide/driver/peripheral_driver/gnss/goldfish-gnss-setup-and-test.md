# Enabling and Testing Goldfish GNSS in the Emulator

[ English | [简体中文](../../../../../zh-cn/device_dev_guide/driver/peripheral_driver/gnss/goldfish-gnss-setup-and-test.md) ]

This document guides you on how to configure, enable, and test the virtual Goldfish Global Navigation Satellite System (GNSS) device in the openvela Emulator environment.

## I. Prerequisites

You have successfully set up the Emulator simulation environment.

## II. Configuration and Enabling

You need to complete the following configurations to ensure that the Goldfish GNSS driver can be loaded and run correctly.

### 1. Enable Virtual GPS Hardware

In your Android Virtual Device (AVD) configuration file, you must enable the virtual GPS hardware.

1. Open the AVD configuration file:

    ```Bash
    $HOME/.android/avd/Vela_Virtual_Device.avd/config.ini
    ```

2. Add or modify the following configuration line, ensuring its value is set to `yes`:

    ```Bash
    hw.gps = yes
    ```

### 2. Verify Kernel Compilation Configuration (Kconfig)

The Goldfish GNSS driver depends on a series of kernel configurations. For standard `goldfish` target devices, these configurations are enabled by default.

You can verify that the following configuration items exist in your build configuration:

```Makefile
CONFIG_GNSSUTILS_MINMEA_LIB=y
CONFIG_SENSORS=y
CONFIG_SENSORS_GOLDFISH_GNSS=y
CONFIG_SENSORS_GNSS=y
```

**Note**: These configuration items are primarily for the `goldfish-arm64-v8a-ap` and `goldfish-armeabi-v7a-ap` target devices and are enabled by default.

### 3. Understand the Driver Initialization Entry Point

The Goldfish GNSS driver is initialized at system startup by the Board Support Package (BSP). You can find the driver's entry point code in the following file:

**File path**: `vendor/qemu/boards/vela/src/qemu_vela.c`

```C
#ifdef CONFIG_SENSORS_GOLDFISH_GNSS
  goldfish_gnss_init(0, 1);
#endif
```

## III. Runtime Interaction and Testing

After successfully enabling the GNSS device, you can interact with and verify the virtual device's functionality in the following three ways.

### Method 1: Listen for GNSS Data via NuttShell (NSH)

You can use the `uorb_listener` tool to subscribe to the `sensor_gnss` uORB topic to view the location data published by the GNSS driver in real-time.

1. In the Emulator's NSH command line, execute the following command:

    ```Bash
    uorb_listener -r 1 sensor_gnss
    ```

2. Observe the output. Normal output should include information such as timestamp, UTC time, latitude, longitude, and speed, as shown below:

    ```Bash
    [   18.240000] [13] [  INFO] [ap] Mointor objects num:2
    [   18.240000] [13] [  INFO] [ap] object_name:sensor_gnss, object_instance:0
    [   18.240000] [13] [  INFO] [ap] object_name:sensor_gnss, object_instance:1
    [   18.240000] [13] [ ALERT] [ap] period_us = 1000000
    [   19.010000] [13] [  INFO] [ap] sensor_gnss:   timestamp: 19010000 (0 us ago) time_utc: 1689601925 latitude: 37.4210 longitude: -121.9150
    [   19.010000] [13] [  INFO] [ap] sensor_gnss:   altitude: 0.0000 altitude_ellipsoid: 0.0000 ground_speed: 145.3254 course: 166.2700
    [   19.010000] [13] [  INFO] [ap] sensor_gnss:   eph: nan epv: nan hdop: nan vdop: nan
    [   20.020000] [13] [  INFO] [ap] sensor_gnss:   timestamp: 20020000 (0 us ago) time_utc: 1689601926 latitude: 37.4210 longitude: -121.9150
    ...
    ```

> **Note**: The virtual GNSS device in the Emulator does not support custom data reporting intervals. The default reporting interval is 1 second (corresponding to the 1X rate in the control panel). You can adjust the data playback rate (supports 1X to 5X) through the Emulator control panel's Playback feature to change the data update frequency.

### Method 2: Interact via the Emulator GUI

The Emulator provides a graphical control panel that allows you to intuitively simulate location and navigation scenarios.

#### Simulating a Static Location

1. In the Emulator's **Extended Controls** -> **Location** panel, you can directly select a point on the map.
2. You can also import a file containing waypoint data using the **Import GPX/KML** button.
3. Click the **Set Location** button to send this location information to the virtual device.

#### Simulating a Navigation Route

1. Select a start and end point on the map to plan a route.
2. Set the travel speed in the **Playback** section.
3. Click the **Play Route** button, and the Emulator will simulate continuous GNSS data along the route.

### Method 3: Send GEO Commands via the Emulator Console

For automated testing or scripted interactions, you can use `telnet` to connect to the Emulator console and send `geo` commands.

#### Step 1: Obtain the Authentication Token

> Security Tip: This token is used for authentication. Please store it securely and do not expose it in public documents or code.

Execute the following command to view your authentication token:

```Bash
cat $HOME/.emulator_console_auth_token
```

#### Step 2: Start the Emulator

```Bash
./emulator.sh
```

#### Step 3: Connect to the Console and Authenticate

1. Use `telnet` to connect to the Emulator's default console port, `5554`.
2. Use the `auth` command with the token you obtained to authenticate.

    ```Bash
    telnet localhost 5554
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
    auth ***89ABC***
    Android Console: type 'help' for a list of commands
    OK
    ```

#### Step 4: Send GEO Commands

After successful authentication, you can use the `geo` series of commands to send GNSS data to the virtual device.

| **Command**                 | **Description**                                                           |
| :-------------------------- | :------------------------------------------------------------------------ |
| `geo nmea <sentence>`       | Sends a raw NMEA format sentence, e.g., `$GPGGA,...`                      |
| `geo fix <lon> <lat> [alt]` | Sends a single point fix with longitude, latitude, and optional altitude. |
| `geo gnss <payload>`        | Sends a more complex GNSS data payload.                                   |

## IV. References

- **GNSS Driver Framework**: See [GNSS Driver Framework Development Guide](./gnss_driver_guide.md).
