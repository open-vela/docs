# Telephony

Telephony 提供蜂窝通信能力，framework/telephony 是 openvela 蜂窝通信对应用层提供的接口层，又称为 TAPI（Telephony API）。封装的接口涵盖了蜂窝通信业务：网络服务、通话、短信、数据、SIM 双卡和 modem 配置管理等。

TAPI 独立于 openvela telephony core stack，内部逻辑基于 DBUS LIB 对 Core Stack 进行业务逻辑封装，屏蔽掉 D-BUS 的复杂操作，对外以标准 C 的方式提供标准化统一的 Telephony API 接口定义，方便 openvela 应用层 APP 的使用，让 openvela APP 实现 openvela 系统版本间复用。

## 一、模块代码介绍

| 模块           | 文件                      | 说明                  |
| :------------- | :------------------------ | :-------------------- |
| 对外统一头文件 | tapi.h                    | 公共与 utils 接口定义 |
| Radio 接口     | tapi_manager.c/h          | Telephony 公共接口    |
| Call 接口      | tapi_call.c/h tapi_ss.c/h | 通话管理接口          |
| Network 接口   | tapi_network.c/h          | 网络注册接口          |
| Data 接口      | tapi_data.c/h             | 数据服务接口          |
| SIM 接口       | tapi_sim.c/h tapi_stk.c/h | 卡和 STK 接口         |
| SMS 接口       | tapi_sms.c/h              | 短信管理接口          |
| IMS 接口       | tapi_ims.c/h              | IMS 服务接口          |

## 二、TAPI 配置

完整的 Telephony 业务涉及模块众多，需要所有模块开启完整使用 Telephony 业务：

- DBUS 配置

    ```
    CONFIG_DBUS_DAEMON=y
    CONFIG_DBUS_MONITOR=y
    CONFIG_DBUS_SEND=y
    CONFIG_LIB_DBUS=y
    ```

- GLIB 配置

    ```
    CONFIG_LIB_GLIB=y
    ```

- OFONO 配置

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

- Telephony API 配置

    ```
    CONFIG_TELEPHONY=y
    CONFIG_TELEPHONY_TOOL=y  //debug工具，可选
    ```

## 三、TAPI 工作使用模型

![TAPIWork](figures/TapiWork.png)


## 四、TAPI 函数使用举例

1. 获取 TAPI 工作上下文

    先声明一个 callback 函数：

    ```c
    static void on_tapi_client_ready(const char* client_name, void* user_data)
    {
        if (client_name != NULL)
            syslog(LOG_DEBUG, "tapi is ready for %s\n", client_name);
        ...
    }
    ```

    再调用 tapi_open 函数获取上下文。获取成功需要 oFono、DBus 等服务启动成功，当 ready 后会调用 callback 函数。

    ```c
    tapi_context context;
    char* dbus_name = "vela.telephony.tool";
    context = tapi_open(dbus_name, on_tapi_client_ready, NULL);
    ```

2. 释放 TAPI 工作上下文

    ```c
    tapi_close(context);
    ```

3. 查询当前的 radio power 状态

    ```c
    int slot_id = 0;
    bool value = false;
    tapi_get_radio_power(context, slot_id, &value);
    ```

## 五、TAPI 列表

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
