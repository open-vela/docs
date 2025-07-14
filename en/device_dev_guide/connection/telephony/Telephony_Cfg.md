# Telephony Service Configuration Guide

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/connection/telephony/Telephony_Cfg.md) \]

## I. Overview

This document guides you through the proper configuration of the Telephony service in the `openvela` system to enable cellular communication capabilities. Enabling this service involves the coordination of several key components, including the D-Bus message bus, the oFono telephony protocol stack, the Radio Interface Layer (RIL), and related libraries and tools.

The configuration process is divided into three core steps:

1. **Kconfig Configuration:** Enable all necessary kernel components and dependent libraries for the Telephony service.
2. **Resource File Configuration:** Provide the necessary configuration files for system services like D-Bus.
3. **Startup Script Configuration:** Load and run Telephony-related daemons in the correct order during system startup.

## II. Kconfig Configuration

You need to enable the following build options using `menuconfig` or by directly modifying the `defconfig` file. These options are categorized by their dependent modules.

### 1. D-Bus Configuration

D-Bus is the core Inter-Process Communication (IPC) mechanism that oFono depends on.

| Option                       | Description                                                                                                                                              |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CONFIG_DBUS_DAEMON`         | Enable the D-Bus daemon.                                                                                                                                 |
| `CONFIG_DBUS_MONITOR`        | Enable the D-Bus monitor tool for debugging.                                                                                                             |
| `CONFIG_DBUS_SEND`           | Enable the D-Bus message sending tool for debugging.                                                                                                     |
| `CONFIG_LIB_DBUS`            | Enable the D-Bus client library.                                                                                                                         |
| `CONFIG_LIBC_EXECFUNCS`      | Enable support for functions like `atexit()`.                                                                                                            |
| `CONFIG_LIBC_MAX_EXITFUNS=4` | Set the maximum number of functions that can be registered with `atexit()`.                                                                              |
| `CONFIG_NET_LOCAL_SCM`       | Enable the feature to pass ancillary data over Unix Sockets.                                                                                             |
| `CONFIG_NET_RPMSG`           | (Optional) Enable for cross-core D-Bus communication via RPMSG. For example, a Bluetooth module on the CP core communicating with the AP core via D-Bus. |

### 2. GLib Configuration

oFono relies on the core library functions provided by GLib.

| Option            | Description              |
| :---------------- | :----------------------- |
| `CONFIG_LIB_GLIB` | Enable the GLib library. |

### 3. oFono Configuration

oFono is the core middleware that implements the cellular protocol stack.

| Option                         | Description                                                                                   |
| :----------------------------- | :-------------------------------------------------------------------------------------------- |
| `CONFIG_OFONO`                 | Enable the oFono daemon.                                                                      |
| `CONFIG_OFONO_RILMODEM`        | Enable the oFono RIL plugin to communicate with the `openvela` RIL daemon.                    |
| `CONFIG_OFONO_STACKSIZE=32768` | Set a 32 KB stack size for the oFono daemon.                                                  |
| `CONFIG_SIGNAL_FD`             | Enable the `signalfd` mechanism, which oFono uses for signal handling.                        |
| `CONFIG_LIBC_DLFCN`            | Enable dynamic linking library functions (e.g., `dlopen`), required by oFono to load plugins. |

### 4. GDBus Configuration

GDBus is a D-Bus binding library provided by GLib that simplifies D-Bus programming.

| Option                        | Description                                                         |
| :---------------------------- | :------------------------------------------------------------------ |
| `CONFIG_LIB_DBUS`             | Enable the D-Bus library (dependency, as mentioned in section 2.1). |
| `CONFIG_ALLOW_BSD_COMPONENTS` | Allow BSD-licensed components in openvela.                          |

### 5. Telephony API Configuration

This is the high-level application interface provided by `openvela`.

| Option                  | Description                                       |
| :---------------------- | :------------------------------------------------ |
| `CONFIG_TELEPHONY`      | Enable the `openvela` Telephony API framework.    |
| `CONFIG_TELEPHONY_TOOL` | Enable the Telephony command-line debugging tool. |

In the `CONFIG_TELEPHONY` sub-menu within `menuconfig`, it is recommended to keep the following default settings:

- **Active modem count:** Set to `1` for single-SIM products.
- **Modem path:** Set to `/ril_0` to match the path of the RIL daemon.

## III. Platform and Resource File Configuration

### 1. D-Bus Daemon Resource Configuration

The D-Bus daemon requires a configuration file at startup. Please create the following file structure in your product directory:

```text
.
└── src/
    └── etc/
        └── dbus-1/
            ├── system.conf   # D-Bus system bus configuration file
            └── system.d/     # Directory for D-Bus policies of other system services
```

The `system.conf` file is used to define the socket the D-Bus daemon listens on. Choose one of the following based on your application scenario:

- **Local AP Core Communication:**

    ```xml
    <!-- Use D-Bus only within the AP core -->
    <listen>unix:path=/var/run/dbus/system_bus_socket</listen>
    ```

- **Cross-Core (AP and CP) Communication:**

    ```xml
    <!-- Allow other cores (e.g., the CP core) to access D-Bus via RPMSG -->
    <listen>rpmsg:name=dbus_socket</listen>
    ```

### 2. openvela RIL and Modem Configuration

This part of the configuration is highly dependent on the specific product hardware platform. You need to enable and configure the corresponding RIL implementation in the Board Support Package (BSP) based on the selected Modem model.

**Key Points:**

- Ensure the correct driver for your Modem is enabled.
- The `openvela` RIL implementation must interface correctly with oFono's `rilmodem` plugin.

## IV. Startup Script Configuration

To run the Telephony service automatically on system startup, add the following commands to a startup script such as `rcS`.

```sh
# 1. Start the RIL daemon
#ifdef CONFIG_RILD
rild &
#endif

# 2. Start the D-Bus daemon to provide IPC service for oFono
#ifdef CONFIG_DBUS_DAEMON
dbus-daemon --system --nopidfile --nofork &
#ifdef CONFIG_DBUS_TEST
# Optionally, start another D-Bus instance for the user session
# dbus-daemon --session --nopidfile --nofork &
#endif
#endif

# 3. Configure and start oFono
#ifdef CONFIG_OFONO
#ifdef CONFIG_OFONO_RILMODEM

# Set environment variables required by the oFono RIL plugin
# Please adjust these values according to your product requirements
set OFONO_RIL_DEVICE ril                   # RIL device name
set OFONO_RIL_NUM_SIM_SLOTS 1              # Number of SIM slots
set OFONO_RIL_RAT_LTE 1                    # Enable LTE radio access technology
set OFONO_RIL_TRACE 1                      # Enable RIL debug tracing
set OFONO_CALL_BARRING_INTERFACE_SUPPORT 0 # Disable Call Barring interface
set OFONO_CELL_BROADCAST_INTERFACE_SUPPORT 0 # Disable Cell Broadcast interface
set OFONO_PHONEBOOK_INTERFACE_SUPPORT 0    # Disable Phonebook interface
set OFONO_STK_INTERFACE_SUPPORT 0          # Disable SIM Toolkit interface
set OFONO_SUPPLEMENTARY_SERVICES_INTERFACE_SUPPORT 0 # Disable Supplementary Services interface
set OFONO_FIVE_SIGNAL_LEVEL_SUPPORT 0      # Disable five-level signal strength support
set OFONO_CALL_VOLUME_INTERFACE_SUPPORT 0  # Disable Call Volume interface
set OFONO_GPRS_CONTEXT_TYPE_SUPPORT internet,ims # Supported GPRS context types
#endif

# Start the oFono daemon
#ifdef CONFIG_INTERPRETERS_WAMR
# If using WAMR (WebAssembly Micro Runtime), start in AOT mode
iwasm --disable-bounds-checks --max-threads=1 /etc/ofonod.aot &
#else
# Otherwise, start the native executable directly
ofonod &
#endif
#endif
```

**Notes:**

- **Startup Order:** You must ensure that `rild` and `dbus-daemon` start before `ofonod`.
- **Environment Variables:** The `OFONO_*` environment variables are used to configure the behavior of the oFono RIL plugin at startup. Please adjust them according to your product definition.

After completing all the above configurations, then compiling and flashing the firmware, the `openvela` system will have basic cellular communication capabilities. You can use tools like `telephony-tool` for functional verification.