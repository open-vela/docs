# 适配和启动问题

## 一、观察蓝牙驱动是否注册成功

Vela 支持丰富的设备驱动类型，包括 BTH4，BTH5，BT Bridge 等驱动协议，此外还支持片内蓝牙驱动，以及片外蓝牙驱动，可参考 Vela 蓝牙驱动文档。

### 1、观察设备节点是否存在

通过`ls /dev/`命令，观察是否存在`ttyHCI0`设备节点，正常输出信息如下：

```text
openvela-ap> ls /dev
/dev:
 audio/
 binder
 ......
 ttyHCI0
 ......
 uorb/
 ......
```

### 2、观察Vendor驱动注册成功

可在 Vendor 主动注册函数添加 debug log，观察 Vendor 驱动是否注册成功。

<a id="方法：检查蓝牙服务是否启动"></a>

## 二、检查蓝牙服务是否启动

当前Vela蓝牙服务支持两种运行模式：在应用程序进程中，也支持运行在后台。可依据使用场景来配置。若运行在后台模式运行，可通过如下步骤观察蓝牙服务是否存在。

如下蓝牙bluetootd初始log，包括蓝牙log初始过程，Profile初始化过程，蓝牙驱动初始化过程，以及libuv loop初始化等过程。

```text
[    0.054300] [11] [  INFO] [ap] bluetoothd main 34
[    0.074000] [11] [  INFO] [ap] /data/misc/bt folder create: 0
[    0.084300] [11] [ ALERT] [ap] Framework log level: 7, Stack:0, mask:00000000, Snoop: 0
[    0.084800] [11] [ DEBUG] [ap] [195][storage]: bt_storage_init successed
[    0.085100] [11] [ DEBUG] [ap] [129][service_manager]: A2DP-Sink service register success
[    0.085300] [11] [ DEBUG] [ap] [129][service_manager]: AVRCP-CT service register success
[    0.085800] [11] [ DEBUG] [ap] [201][adapter-stm]: Enter, PrevState=(null) ---> NewState=Off
[    0.087400] [11] [  INFO] [ap] [32][stack_manager]: Stack Info: Zblue Ver:5.4 Sal:2
[    0.088100] [11] [  INFO] [ap] <inf> [h4_init] <406>: Bluetooth H4 driver
[    0.088600] [11] [ DEBUG] [ap] [45][stack_manager]: stack_manager_init done
[    0.088700] [11] [ DEBUG] [ap] [257][bt_service]: bt_service_init done
[    0.089100] [11] [ DEBUG] [ap] [260][service_loop]: service loop running now !!!
[    0.089300] [11] [ DEBUG] [ap] [134][service_loop]: service_schedule_loop:0x40288958, async:0x4024d1b4
[    0.090100] [11] [ DEBUG] [ap] [81][service_loop]: set_ready
```

### 1、确认是否启动bluetoothd

若是通过启动脚本启动bluetoothd服务，请确rcS启动脚本是否配置：

```text
bluetoothd &
```

### 2、检查各阶段初始化是否成功

按照如上初始化log，可观察到如下初始化过程：

* 检查bt_storage_init是否成功
  
    ```text
    [    0.084800] [11] [ DEBUG] [ap] [195][storage]: bt_storage_init successed
    ```

    若是失败，则检查uv db配置是否打开，请查阅系统相关文档或者联系系统团队解决。

* 检查蓝牙目录是否创建成功

    ```text
    [    0.074000] [11] [  INFO] [ap] /data/misc/bt folder create: 0
    ```

    若是失败，则检查目录是否存在，请查阅系统相关文档或者联系系统团队解决。

* 检查协议栈是否初始化成功

    ```text
        [    0.088600] [11] [ DEBUG] [ap] [45][stack_manager]: stack_manager_init done
    ```

    若是失败，则可能协议栈初始化失败，可联系Vela团队解决。

* 检查libuv loop是否启动成功

    ```text
    [    0.089300] [11] [ DEBUG] [ap] [134][service_loop]: service_schedule_loop:0x40288958, async:0x4024d1b4
    ```

    若是失败，则检查libuv loop是否启动成功，btservice模块开源，可在btservice添加debug信息，可进一步确认。

### 3、检查bluetoothd进程是否运行

利用`ps`命令，观察蓝牙服务线程是否存在，正常输出信息可以观察到名为`bluetoothd`的线程。

```text
  PID GROUP PRI POLICY   TYPE    NPX STATE    EVENT     SIGMASK             STACK    USED FILLED COMMAND
    0     0   0 FIFO     Kthread   - Ready              0000000000000000  0001968 0000824  41.8%  Idle_Task
    1     0 192 RR       Kthread   - Waiting  Semaphore 0000000000000000  0003968 0000480  12.0%  hpwork 0x4020f954 0x4020f978
    2     0 100 RR       Kthread   - Waiting  Semaphore 0000000000000000  0003968 0000752  18.9%  lpwork 0x4020f91c 0x4020f940
    4     0 100 RR       Kthread   - Ready              0000000000000000  0003968 0000496  12.5%  goldfish_gpu_fb_thread 0x4024c930
    5     0 100 RR       Kthread   - Waiting  Semaphore 0000000000000000  0003968 0000864  21.7%  goldfish_gnss_thread 0x406d4b30
    6     0 100 RR       Kthread   - Waiting  Semaphore 0000000000000000  0003968 0000904  22.7%  goldfish_sensor_thread 0x402e20a0
    7     7 100 RR       Task      - Running            0000000000000000  0003992 0002048  51.3%  nsh_main
    9     9 100 RR       Task      - Waiting  Semaphore 0000000000000000  0004000 0003096  77.4%  kvdbd
   10    10 100 RR       Task      - Waiting  Semaphore 0000000000000000  0004000 0002192  54.8%  adbd
   11    11 103 RR       Task      - Waiting  Semaphore 0000000000000000  0008088 0003340  41.2%  bluetoothd
   12    12 100 RR       Task      - Waiting  Semaphore 0000000000020000  0004000 0001232  30.8%  telnetd
   13    11 110 FIFO     pthread   - Waiting  Semaphore 0000000000000000  0004016 0000600  14.9%  sysworkq 0x71ffa5 0x40700350
```

<a id="方法：检查蓝牙Enable是否成功"></a>

## 三、检查蓝牙 Enable 是否成功

蓝牙Enable包括蓝牙设备驱动打开，蓝牙各Profile初始化，蓝牙绑定信息恢复等过程。可通过如下步骤观察蓝牙Enable是否成功：

### 1、观察蓝牙驱动节点是否打开成功

```c
int bt_sal_hci_transport_init(const bt_vhal_interface* vhal)
{
    g_hci_rxlen = 0;
    g_vhal = vhal;
    g_tlfd = open(CONFIG_BLUETOOTH_SERVICE_HCI_UART_NAME, O_RDWR | O_BINARY | O_CLOEXEC);
    BT_LOGI("%s: g_tlfd = %d", __func__, g_tlfd);

    if (g_vhal) {
        g_vhal->open(g_tlfd);
    }

    return g_tlfd;
}
```

驱动设备节点打开成功log，如下：

```text
[72][h4]: bt_sal_hci_transport_init: g_tlfd = 16
```
若 fd = -1，蓝牙驱动打开失败， 确认[蓝牙驱动是否注册成功](#一观察蓝牙驱动是否注册成功)，则进一步排查CONFIG_BLUETOOTH_SERVICE_HCI_UART_NAME配置是否正确。

### 2、观察Enbale流程是否成功

蓝牙启动状态机，可观察到蓝牙Enable过程，如下：

```text
[ap] on_adapter_state_changed_cb: state = 1. ...
[ap] on_adapter_state_changed_cb: state = 2...
```

| 状态值 | 释义                 |
| ------ | -------------------- |
| `0`    | 蓝牙关闭             |
| `1`    | 正在启用 BLE 功能    |
| `2`    | BLE 功能已启用       |
| `3`    | 正在启用 BR/EDR 功能 |
| `4`    | BR/EDR 功能已启用    |
| `5`    | 正在关闭 BR/EDR 功能 |
| `6`    | 正在关闭 BLE 功能    |


<a id="适配启动典型问题"></a>

## 典型问题

### 问题一 创建蓝牙 instance 失败

当应用程序调用bluetooth_create_instance接口时，蓝牙instance创建失败，如下：

```text
[03-10 20:23:11.549][03/09 17:29:15] [15] [cp] [270][BT]: [VelaBT], bt_log_server_init 270
[03-10 20:23:15.852][03/09 17:29:19] [19] [cp] [BT] bts_adapter_init: create bt instance failed
[03-10 20:23:17.027][03/09 17:29:20] [15] [cp] [278][BT]: [VelaBT], bt_log_server_init 278
```

蓝牙启动过程包括：设备驱动注册、蓝牙驱动初始化、蓝牙Profile初始化、蓝牙驱动打开、蓝牙Enable等过程。

第一步，按照[观察蓝牙驱动是否注册成功](#一观察蓝牙驱动是否注册成功)，检查蓝牙驱动是否注册成功。

第二步，按照[检查蓝牙服务是否启动](#二检查蓝牙服务是否启动)，检查蓝牙服务是否启动成功。

第三步，检查蓝牙instance是否创建成功。当bluetoothd进程启动阶段，蓝牙instance创建失败，则需要应用程序重试。保证蓝牙服务启动成功后，再创建蓝牙instance。

```c
int bt_socket_client_init(bt_instance_t* ins, int family,
    const char* name, const char* cpu, int port)
{
    uv_poll_t* poll;
    int retry = CLIENT_MAX_RETRY; // 10

    ......
        do {
        ins->peer_fd = bt_socket_client_connect(family, name, cpu, port);
        if (ins->peer_fd <= 0 && !retry) {
            /* connect fail, go out */
            bt_socket_client_deinit(ins);
            return BT_STATUS_PARM_INVALID;
        } else if (ins->peer_fd <= 0) {
            /* connect fail, retry after sleep 100ms */
            usleep(CLIENT_DELAY_MS(retry) * 1000);
            continue;
        } else {
            /* success, goto next step */
            break;
        }
    } while (retry--);
    ......
}
```

第四步，按照[方法：检查蓝牙Enable是否成功](#三检查蓝牙-enable-是否成功)，检查蓝牙使能是否成功。
