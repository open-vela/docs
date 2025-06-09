# 控制拍照问题

<a id="方法：观察HID通道连接是否成功"></a>

## 一、观察HID通道连接是否成功

### 1、通过syslog观察HID通道连接是否成功

如下是典型syslog，通过state字段可以看到HID通道连接成功，其中state字段为1表示连接中，2表示连接成功

```text
[bttool> hidd connect a4:cc:b3:xx:xx:xx
[[bttool] HID device connect host, address:a4:cc:b3:xx:xx:xx
bttool> [bttool] hidd_connection_state_cb, addr:a4:cc:b3:xx:xx:xx, transport: br, state:1
[bttool] hidd_connection_state_cb, addr:a4:cc:b3:xx:xx:xx, transport: br, state:2
```

### 2、通过Airlog或者Snoop log观察HID Control L2CAP Channel是否连接成功

如下是典型snoop log，通过蓝色柱体可以看到HID 控制L2CAP Channel连接成功，L2CAP Connection Request和L2CAP Connection Response 对应Channels的连接事件：

<img src="img/hid/snoop_hidd_control_connection.png" alt="snoop:HID L2CAP 控制Channel连接成功" width="75%">

### 3、通过Airlog或者Snoop log观察HID Interrupt L2CAP Channel是否连接成功

如下是典型snoop log，通过蓝色柱体可以看到HID 中断L2CAP Channel连接成功，L2CAP Connection Request和L2CAP Connection Response 对应Channels的连接事件：

<a id="方法：观察HID通道手表还是手机断开HID通道"></a>

## 二、观察HID通道手表还是手机断开HID通道

### 1、通过通过Airlog或者Snoop log观察是否对方断开HID Control或者Interrupt L2CAP Channel

如下是典型snoop log，通过蓝色柱体可以看到HID L2CAP Channel连接断开，L2CAP Disconnection Request和L2CAP Disconnection Response 对应Channels的断开事件：

<img src="img/hid/snoop_hidd_disconnection.png" alt="snoop:HID L2CAP Channel连接断开" width="75%">

可以看到，HID L2CAP Channel连接断开，手机端主动发起断开L2CAP通道。

<a id="方法：手机蓝牙设备绑定数量是否超过7个"></a>

## 三、手机蓝牙设备绑定数量是否超过7个

进入设置->蓝牙->手机蓝牙设备，查看手机蓝牙设备绑定数量是否超过7个。若是，则需要解绑手机蓝牙设备。

## 典型问题

<a id="问题：手表无法控制手机拍照"></a>

### 问题一：手表无法控制手机拍照

通常，可以通过蓝牙服务log、airlog协议流程、协议栈syslog流程、snoop log等方式，观察双方是否有ACL连接、 HID L2CAP连接等，导致无法控制手机拍照。

* [观察HID通道连接是否成功](#方法：观察HID通道连接是否成功)

  * 若是HID L2CAP通道没有连接成功，则打开协议栈syslog，进一步确认手表是否发起HID控制通道建立过程。
  * 若是HID L2CAP通道连接成功，则进一步确认是否是手机端主动断开连接。

* [观察HID通道手表还是手机断开HID通道](#方法：观察HID通道手表还是手机断开HID通道)

  * 若是手表端断开连接，则打开协议栈syslog进一步排查。
  * 若是手机端断开连接，则进一步手机蓝牙设备绑定数量是否超过7个。

* [手机蓝牙设备绑定数量是否超过7个](#方法：手机蓝牙设备绑定数量是否超过7个)

  * 若是手机蓝牙设备绑定数量超过7个，则需要解绑手机蓝牙设备。
  * 否则，则检查手机端是否支持HID，让手机同学进一步分析。
