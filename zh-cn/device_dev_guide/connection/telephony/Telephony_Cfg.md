# Telephony 配置

Telephony 业务涉及模块众多，以下是相关配置的详细说明。

## 一、DBUS 配置

以下是 DBUS 的相关配置项：

```Makefile
CONFIG_DBUS_DAEMON=y
CONFIG_DBUS_MONITOR=y
CONFIG_DBUS_SEND=y
CONFIG_LIB_DBUS=y
CONFIG_LIBC_EXECFUNCS=y
CONFIG_LIBC_MAX_EXITFUNS=4
CONFIG_NET_LOCAL_SCM=y
```

## 二、GLIB 配置

以下是 GLIB 的相关配置项：

```Makefile
CONFIG_LIB_GLIB=y
```

## 三、oFono 配置

以下是 oFono 的相关配置项：

```Makefile
CONFIG_OFONO=y
// modem类型选择，openvela支持ril通信，启用ofono的rilmodem
CONFIG_OFONO_RILMODEM=y 
CONFIG_OFONO_STACKSIZE=32768
CONFIG_SIGNAL_FD=y
// dlopen系列接口库，oFono编译需要
CONFIG_LIBC_DLFCN=y  
```

## 四、GDBUS 配置

以下是 GDBUS 的相关配置项：

```Makefile
CONFIG_LIB_DBUS=y
CONFIG_ALLOW_BSD_COMPONENTS=y
```

## 五、Telephony API 配置

以下是 Telephony API 的相关配置项：

```Makefile
// 启用 Telephony 功能，建议子项保持默认配置：  
// 单卡产品 "active modem count" 配置为 1
// "modem path" 配置为 /ril_0  
CONFIG_TELEPHONY=y
CONFIG_TELEPHONY_TOOL=y
```

## 六、注意事项

为了让 openvela 支持蜂窝通信能力，除了上述 Telephony 的配置外，还需要根据具体产品平台，启用对应的 modem 配置。
