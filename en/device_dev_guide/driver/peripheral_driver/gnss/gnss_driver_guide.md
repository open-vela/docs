# GNSS Driver Framework Development Guide

[ English | [简体中文](../../../../../zh-cn/device_dev_guide/driver/peripheral_driver/gnss/gnss_driver_guide.md) ]

This document provides comprehensive technical guidance for developing and using Global Navigation Satellite System (GNSS) drivers in the openvela operating system.

## I. Overview

openvela implements a unified GNSS driver framework. This framework is designed based on the Upper/Lower-Half layered architecture of the Sensor driver model, aiming to simplify the porting of hardware drivers and seamlessly integrate with the uORB message bus.

### 1. Framework Architecture

The GNSS framework clearly divides the driver logic into two layers, defining the responsibilities of the framework and the driver developer:

- **Upper-Half Driver**: Provided by the openvela framework. It handles generic logic independent of specific hardware, including:

    - Parsing standard NMEA (National Marine Electronics Association) messages.
    - Publishing the parsed structured data as uORB topics to the Sensor driver framework.
    - Registering a character device node (`/dev/ttyGNSS[n]`) for application-level access to the raw data stream.

- **Lower-Half Driver**: Implemented by the driver developer. It encapsulates all hardware-specific operations for a particular GNSS module, such as serial communication, power management, and data reading.

This layered design allows driver developers to focus on the hardware itself without needing to worry about complex upper-level system integration.

![alt text](./figures/001.png)

## II. Driver Development Guide (Southbound Interface)

This section is intended for **driver developers**, guiding you on how to integrate a new GNSS module into the openvela system. You will need to implement the lower-half driver.

The development process follows these four core steps:

### Step 1: Implement the Hardware Operations Interface (`gnss_ops_s`)

First, you need to implement a set of function pointers defined in the `struct gnss_ops_s` structure. These functions encapsulate the low-level control logic for the GNSS hardware, including how to open, control, set the sampling rate, and inject data into the GNSS module.

```C
struct gnss_ops_s
{
  /* Activate or deactivate the GNSS device */
  CODE int (*activate)(FAR struct gnss_lowerhalf_s *lower,
                       FAR struct file *filep, bool enable);

  /* Set the sampling rate, i.e., the data reporting period of the GNSS module (unit: microseconds) */
  CODE int (*set_interval)(FAR struct gnss_lowerhalf_s *lower,
                           FAR struct file *filep,
                           FAR uint32_t *period_us);

  /* Control the GNSS: provides a generic I/O control interface for handling specific commands */
  CODE int (*control)(FAR struct gnss_lowerhalf_s *lower,
                      FAR struct file *filep,
                      int cmd, unsigned long arg);

  /* Inject data into the GNSS module, such as assisted-GNSS (A-GNSS) data, ephemeris, or firmware updates */
  CODE ssize_t (*inject_data)(FAR struct gnss_lowerhalf_s *lower,
                              FAR struct file *filep,
                              FAR const void *buffer, size_t buflen);
};
```

### Step 2: Implement Data Reporting

When the GNSS module reports data via a serial port or other means, your driver (typically in an interrupt service routine or a worker thread) needs to call the callback functions provided by the upper-half driver to push the data to the framework for processing.

The framework provides two reporting functions for the driver developer to choose from based on the data type:

| **Function Prototype**                         | **Use Case**                                                                                                                                                                                             |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gnss_push_data_t(priv, data, bytes, is_nmea)` | Used to push the **raw data stream**. <br>If the data is in NMEA format, set `is_nmea` to `true`; otherwise, set it to `false`. <br>The upper-half driver will be responsible for parsing the NMEA data. |
| `gnss_push_event_t(priv, data, bytes, type)`   | Used to push **structured data** that has already been parsed by the driver itself. <br>For example, `sensor_gnss` or `sensor_gnss_satellite`. The `type` parameter is used to specify the data type.    |

```C++
/* Callback function prototype, provided by the upper-half, populated in lower->push_data during registration */
typedef CODE void (*gnss_push_data_t)(FAR void *priv, FAR const void *data,
                                      size_t bytes, bool is_nmea);

/* Callback function prototype, provided by the upper-half, populated in lower->push_event during registration */
typedef CODE void (*gnss_push_event_t)(FAR void *priv, FAR const void *data,
                                       size_t bytes, int type);
```

**Key Note**: When calling, the `priv` parameter must be `lower->priv`, which is the private context handle of the upper-half driver.

### Step 3: Instantiate and Register the Lower-Half Driver

Next, you need to instantiate a `struct gnss_lowerhalf_s` and register it with the GNSS framework.

1. **Instantiate `gnss_lowerhalf_s`**:

    This structure serves as the bridge between the upper-half and lower-half drivers.

    ```C
    struct gnss_lowerhalf_s
    {
        /* Points to the set of hardware operation functions you implemented in Step 1 */
        FAR const struct gnss_ops_s *ops;
        
        /* Populated by the upper-half driver, used to push raw data */
        gnss_push_data_t push_data;
        
        /* Populated by the upper-half driver, used to push structured events */
        gnss_push_event_t push_event;
        
        /* Populated by the upper-half driver, used as the context for callbacks */
        FAR void *priv;
    };
    ```

2. **Register by Calling `gnss_register()`**:

    Use the `gnss_register()` function to register your lower-half driver instance with the system.

    ```C
    int gnss_register(FAR struct gnss_lowerhalf_s *dev, int devno,
                      uint32_t nbuffer);
    ```

    **Parameter Description**

    - `dev`: A pointer to the `gnss_lowerhalf_s` structure you instantiated.
    - `devno`: The sequence number assigned to this GNSS device (e.g., 0, 1, ...).
    - `nbuffer`: Specifies the size of the internal ring buffer in the upper-half driver. A recommended value is `1`, which means the buffer caches at most one GNSS data entry, and new data will overwrite the old.

    Upon successful registration, the framework will automatically create the following device nodes:

    - `/dev/ttyGNSS[devno]`
    - `/dev/uorb/sensor_gnss[devno]`
    - `/dev/uorb/sensor_gnss_satellite[devno]`
    - And other related uORB nodes.

### Step 4: Development Example (`fakesensor_uorb.c`)

The `simulator` in openvela provides a complete `fakesensor` GNSS driver, which serves as a best-practice reference for lower-half driver development. We highly recommend that developers carefully study the implementation of this file before starting to write a new driver to understand the full context and interaction flow.

- Reference Value: This file fully demonstrates the implementation of `gnss_ops_s`, the instantiation of the lower-half structure, and the entire process of registering with the framework.
- Code Path: `drivers/sensors/fakesensor_uorb.c`

```C
/* 1. Define hardware operation functions */
static int fakegnss_activate(FAR struct gnss_lowerhalf_s *lower,
                             FAR struct file *filep, bool enable)
{
  /* ... Implement hardware enable/disable logic ... */
  return 0;
}

static int fakegnss_set_interval(FAR struct gnss_lowerhalf_s *lower,
                                 FAR struct file *filep,
                                 FAR uint32_t *period_us)
{
  /* ... Implement hardware sampling rate setting logic ... */
  return 0;
}

/* 2. Instantiate the operations function set */
static struct gnss_ops_s g_fakegnss_ops =
{
  .activate     = fakegnss_activate,
  .set_interval = fakegnss_set_interval,
};

/* 3. In the driver initialization function, allocate and register the lower-half device */
int my_gnss_driver_initialize(int devno)
{
    // Allocate memory for the lower-half device
    FAR struct gnss_lowerhalf_s *gnss = kmm_zalloc(sizeof(*gnss));
    if (gnss == NULL)
      {
        return -ENOMEM;
      }

    // Associate the hardware operations function set
    gnss->ops = &g_fakegnss_ops;

    // Register the device with the GNSS framework
    int ret = gnss_register(gnss, devno, 1);
    if (ret < 0)
      {
        kmm_free(gnss);
        return ret;
      }

    return 0;
}
```

## III. Application Development Guide (Northbound Interface)

This section is intended for **application developers**, explaining how to access and use GNSS data from the application layer.

### 1. Access Methods

openvela provides two main methods for applications to access GNSS data:

1. **Subscribing to Structured Data via uORB (Recommended):**

    This is the most common and recommended method. The upper-half driver automatically parses standard NMEA data (or receives structured data pushed directly from the lower-half driver) and publishes it as multiple uORB topics. Applications can subscribe to these topics using the standard uORB API to obtain parsed, ready-to-use position, velocity, and satellite information.
​

    **Main uORB Nodes:**

    - `/dev/uorb/sensor_gnss[n]`: Main positioning information (latitude, longitude, altitude, velocity, etc.).
    - `/dev/uorb/sensor_gnss_satellite[n]`: Visible satellite information (satellite ID, elevation, azimuth, signal-to-noise ratio, etc.).
    - `/dev/uorb/sensor_gnss_clock[n]`
    - `/dev/uorb/sensor_gnss_measurement[n]`
    - `/dev/uorb/sensor_gnss_geofence_event[n]`

2. **Reading Raw NMEA/Raw Data:**

    For some advanced use cases, such as parsing proprietary NMEA messages from GNSS module vendors, or for data playback and analysis, you can directly read from and write to the character device node.

    - **Device Node**: `/dev/ttyGNSS[n]`
    - **Usage**: Open and read this node like a standard serial port device (`open()` and `read()`) to get the unprocessed raw data stream.
    - **NMEA Parsing Library**: To help application developers process raw NMEA data, the openvela system has a built-in lightweight parsing library, `minmea`.

        - **Header File**: `#include <minmea/minmea.h>`
        - **Usage**: Application code can directly call the `minmea_parse_xxx()` series of functions to parse various NMEA sentences.
        - **Reference**: You can also refer to the `gnss_parse()` function in the `drivers/sensors/gnss_uorb.c` file to see how the upper-half driver uses the `minmea` library for parsing.

## IV. Practice and Testing

The `fakesensor` simulated GNSS device is enabled by default in the openvela `simulator`. After compiling and running the simulator, you can use the following commands to test and verify the GNSS functionality.

### 1. Subscribing to uORB Topics

Use the `uorb_listener` command to listen to uORB topics in real-time and print the data.

- **Listen to the `sensor_gnss` topic:**

    ```Bash
    ap> uorb_listener -r 1 sensor_gnss
    [    6.544200] [43] [  INFO] [ap] 
    Mointor objects num:2
    [    6.545000] [43] [  INFO] [ap] object_name:sensor_gnss, object_instance:0
    ...
    ```

- **Listen to both `sensor_gnss` and `sensor_gnss_satellite` topics simultaneously:**

    ```Bash
    ap> uorb_listener -r 1 sensor_gnss,sensor_gnss_satellite
    [   71.427800] [59] [  INFO] [ap] 
    Mointor objects num:4
    [   71.428200] [59] [  INFO] [ap] object_name:sensor_gnss, object_instance:0
    ...
    ```

### 2. Reading Raw Data

Use the `hexdump` command to directly view the raw data stream output from the `/dev/ttyGNSS0` node.

```bash
ap> hexdump ttyGNSS0
ttyGNSS0 at 00000000:
...
```
