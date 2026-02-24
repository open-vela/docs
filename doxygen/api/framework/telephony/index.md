# Telephony

telephony提供蜂窝通信能力，framewrok/telephony是Vela蜂窝通信对应用层提供的接口层，又称为TAPI（Telephony API）。封装的接口涵盖了蜂窝通信业务：网络服务、通话、短信、数据、SIM双卡和modem配置管理等。

TAPI独立于vela telephony core stack，内部逻辑基于DBUS LIB对Core Stack进行业务逻辑封装，屏蔽掉D-BUS的复杂操作，对外以标准C的方式提供标准化统一的Telephony API接口定义，方便Vela应用层APP的使用，让Vela APP实现Vela系统版本间复用。

## 模块代码介绍

| 模块     | 文件  | 说明      |
| :------ | :------- | :--------- |
| <div style="width: 100pt">对外统一头文件 | tapi.h  | 公共与utils接口定义 |
| Radio接口 | tapi_manager.c/h  | <div style="width: 150pt">Telephony公共接口 |
| Call接口 | tapi_call.c/h<br>tapi_ss.c/h | 通话管理接口|
| Network接口 | tapi_network.c/h | 网络注册接口 |
| Data接口 | tapi_data.c/h | 数据服务接口  |
| SIM接口| tapi_sim.c/h <br> tapi_stk.c/h  |卡和STK接口|
| SMS接口 | tapi_sms.c/h | 短信管理接口 |
| IMS接口| tapi_ims.c/h | ims服务接口  |

## TAPI配置

完整的Telephony业务涉及模块众多，需要所有模块开启完整使用telephony业务：

- DBUS配置

```
CONFIG_DBUS_DAEMON=y
CONFIG_DBUS_MONITOR=y
CONFIG_DBUS_SEND=y
CONFIG_LIB_DBUS=y
```

- GLIB配置

```
CONFIG_LIB_GLIB=y
```

- OFONO配置

```
CONFIG_LIB_ELL=y
CONFIG_OFONO=y
CONFIG_OFONO_RILMODEM=y //modem类型选择，支持rild的选择rilmodem
CONFIG_OFONO_ATMODEM=y //支持串口、USB的选择atmodem
```

- GDBUS 配置

```
CONFIG_LIB_DBUS=y
```

- Telephony API配置

```
CONFIG_TELEPHONY=y
CONFIG_TELEPHONY_TOOL=y  //debug工具，可选
```

## TAPI工作使用模型

![TAPIWork](../../../../images/TapiWork.png)


## TAPI函数使用举例

1. 获取TAPI工作上下文
<br>先声明一个callback函数
```c
static void on_tapi_client_ready(const char* client_name, void* user_data)
{
    if (client_name != NULL)
        syslog(LOG_DEBUG, "tapi is ready for %s\n", client_name);
    ...
}
```
再调用tapi_open函数获取上下文。获取成功需要oFono、DBus等服务启动成功，当ready后会调用callback函数。
```c
    tapi_context context;
    char* dbus_name = "vela.telephony.tool";
    context = tapi_open(dbus_name, on_tapi_client_ready, NULL);
```

2. 释放TAPI工作上下文
```c
tapi_close(context);
```

3. 查询当前的radio power状态
```c
    int slot_id = 0;
    bool value = false;
    tapi_get_radio_power(context, slot_id, &value);
```

## TAPI列表

```eval_rst

.. toctree::
  :maxdepth: 2

  telephony_manager
  telephony_call
  telephony_data
  telephony_ims
  telephony_network
  telephony_sim
  telephony_sms

```
