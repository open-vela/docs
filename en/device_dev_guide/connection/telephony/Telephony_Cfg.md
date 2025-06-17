# Telephony Configuration

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/connection/telephony/Telephony_Cfg.md) \]

The Telephony service involves many modules. Below are the detailed descriptions of the related configurations.

## 1. DBUS Configuration

The following are the related configuration items for DBUS:

```Makefile
CONFIG_DBUS_DAEMON=y
CONFIG_DBUS_MONITOR=y
CONFIG_DBUS_SEND=y
CONFIG_LIB_DBUS=y
CONFIG_LIBC_EXECFUNCS=y
CONFIG_LIBC_MAX_EXITFUNS=4
CONFIG_NET_LOCAL_SCM=y
```

## 2. GLIB Configuration

The following are the related configuration items for GLIB:

```Makefile
CONFIG_LIB_GLIB=y
```

## 3. oFono Configuration

The following are the related configuration items for oFono:

```Makefile
CONFIG_OFONO=y
// Select modem type, openvela supports RIL communication, enable oFono's rilmodem
CONFIG_OFONO_RILMODEM=y 
CONFIG_OFONO_STACKSIZE=32768
CONFIG_SIGNAL_FD=y
// dlopen series interface libraries required for oFono compilation
CONFIG_LIBC_DLFCN=y  
```

## 4. GDBUS Configuration

The following are the related configuration items for GDBUS:

```Makefile
CONFIG_LIB_DBUS=y
CONFIG_ALLOW_BSD_COMPONENTS=y
```

## 5. Telephony API Configuration

The following are the related configuration items for Telephony API:

```Makefile
// 1. Enable Telephony feature, it is recommended to keep the sub-items at default configuration:
// 2. For single-SIM products, configure "active modem count" to 1
// Set "modem path" to /ril_0  
CONFIG_TELEPHONY=y
CONFIG_TELEPHONY_TOOL=y
```

## 6. Notes

To enable openvela to support cellular communication capabilities, in addition to the above Telephony configurations, the corresponding modem configurations must also be enabled based on the specific product platform.
