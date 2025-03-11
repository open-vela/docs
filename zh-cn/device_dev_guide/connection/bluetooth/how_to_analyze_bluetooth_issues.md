<!-- title: 如何分析蓝牙问题 -->

<!-- omit from toc -->
# 目录

- [发现、连接、配对问题](#发现连接配对问题)
  - [分析方法](#发现连接配对分析方法)
      - [方法：观察是否对方设备未打开可连接模式(Page Timeout)](#方法观察是否对方设备未打开可连接模式)
      - [方法：观察是否ACL连接超时断开(Connection Timeout)](#方法观察是否ACL连接超时断开)
      - [方法：观察是否已经绑定成功，但是未有Profile连接，ACL主动断开](#方法观察是否已经绑定成功，但是未有Profile连接，ACL主动断开)
      - [方法：观察是否本地配对信息无效(Linkey Missing)](#方法观察是否本地配对信息无效)
      - [方法：观察是否对方配对信息无效(Linkey Missing)](#方法观察是否对方配对信息无效)

  - [典型问题](#发现连接配对典型问题)
  - [问题: 经典蓝牙设备主动绑定对方设备失败](#问题-经典蓝牙设备主动绑定对方设备失败)
- [音频传输问题](#音频传输问题)
- [音乐播放控制问题](#音乐播放控制问题)
  - [分析方法](#分析方法)
    - [方法：观察是否建立了AVRCP连接](#方法观察是否建立了avrcp连接)
    - [方法：观察设备是否支持AVRCP](#方法观察设备是否支持avrcp)
    - [方法：观察是否发送了播放、暂停请求](#方法观察是否发送了播放暂停请求)
    - [方法：观察是否使用了绝对音量](#方法观察是否使用了绝对音量)
    - [方法：观察音乐源设备（手机）是否设置了绝对音量](#方法观察音乐源设备手机是否设置了绝对音量)
    - [方法：观察本地设备是否设置了绝对音量](#方法观察本地设备是否设置了绝对音量)
    - [方法：观察音乐源设备（手机）是否改变了音频幅值](#方法观察音乐源设备手机是否改变了音频幅值)
    - [方法：观察是否打开了AVRCP配置](#方法观察是否打开了avrcp配置)
  - [典型问题](#典型问题)
    - [问题: 不能控制播放、暂停](#问题-不能控制播放暂停)
    - [问题: 不能受音乐源设备（手机）控制调节音量](#问题-不能受音乐源设备手机控制调节音量)
- [通话问题](#通话问题)
- [数据传输问题](#数据传输问题)

---

# 发现、连接、配对问题

<a id="发现连接配对分析方法"></a>

## 分析方法

<a id="方法：观察是否对方设备未打开可连接模式"></a>

### 方法：观察是否对方设备未打开可连接模式
通常，可以通过第三方设备、airlog协议流程、协议栈syslog流程、snoop log等方式，观察对方设备是否打开可连接模式。

#### 1 通过第三方设备观察是否连接成功
使用第三个设备，在蓝牙设置界面主动发起绑定过程，观察能否和对方设备绑定成功，排除对方设备未打开可连接模式

#### 2 通过airlog观察是否Page成功
观察空口log，检查是否对方不响应Page过程的ID包，其中，spec标准流程如下:

<img src="img/how_to_analyze_bluetooth_issues/gap/spec_page_response_sequence.png" alt="spec:通过airlog观察是否Page成功" width="50%">

依据spec流程链路层page ID包发出去后，对方设备是否回复ID。如下空口log看Page过程的ID包，对方未响应，因此对方未打开可连接模式。

<img src="img/how_to_analyze_bluetooth_issues/gap/sniffer_page_timeout.png" alt="sniffer:通过airlog观察是否Page成功" width="50%">

#### 3 通过协议栈syslog观察是否Page成功
观察协议栈syslog，检查若是出现PageTimeout，对应错误码04。

```text
[08/09 19:26:38.620200] [28] [ap] ---->[HCI][CMDN][P:1,$:1][-Create_Connection][status:PAGE TIMEOUT | 04]
[08/09 19:26:38.621300] [28] [ap]      [Connection_Complete][T:0x200ed280]
[08/09 19:26:38.622400] [28] [ap] GAP_IND_CONNECTION_EVENT: <addr: 28:02:2e:82:b9:22.0><type: 2><status: 0><error: 4>
```

#### 4 通过HCI log可观察是否Page成功
如下，观察HCI log看Create Connection对应的HCI Connection Complete事件为Page timeout，则表示对方未打开可连接模式。

<img src="img/how_to_analyze_bluetooth_issues/gap/snoop_page_timeout.png" alt="snoop:通过HCI log可观察是否Page成功" width="50%">


<a id="方法观察是否ACL连接超时断开"></a>

### 方法：观察是否ACL连接超时断开（Connection Timeout）

通常，可以通过蓝牙服务log、airlog协议流程、协议栈syslog流程、snoop log等方式，观察对方设备是否异常超时断开连接。

#### 1 通过蓝牙服务log可观察是否超时断开
如下，可通过btservice的log事件CONNECTION_STATE_DISCONNECTED，08错误表示连接超时断开错误码。

```text
[2024-12-31 20:04:31] [06/04 03:10:58.173500] [26] [ap] [660][adapter-svc]: ACL connection state changed, addr:28:02:2E:82:B9:22, link:0, state:CONNECTION_STATE_DISCONNECTED, status:0, reason:8
```

#### 2 观察空口log，是否超时断开ACL连接

如下，可以通过空口log看，连接数据包在retry多次，直到最终超时断开。

<img src="img/how_to_analyze_bluetooth_issues/gap/sniffer_connection_timeout.png" alt="sniffer:观察空口log，是否超时断开ACL连接" width="50%">


#### 3 观察snoop log，是否超时断开
如下，观察snoop log蓝牙断开连接事件HCI Disconnect Complete事件，对应reason为connection timeout。

<img src="img/how_to_analyze_bluetooth_issues/gap/snoop_connection_timeout.png" alt="snoop:观察snoop log，是否超时断开" width="50%">


<a id="方法观察是否已经绑定成功，但是未有Profile连接，ACL主动断开"></a>

### 方法：观察是否已经绑定成功，但是未有Profile连接，ACL主动断开

通常，可以通过蓝牙服务log、airlog协议流程、协议栈syslog流程、snoop log等方式，观察双方是否有Profile连接，导致连接断开。

#### 1 观察蓝牙服务log，是否有Profile连接
观察本地btservice log，设备绑定成功后，没有A2DP、SPP等Profile连接，ACL连接成功一段事件后，出现ACL连接断开事件
如下，从btservice log看acl建立连接成功，SDP完成后，未连接其他Profile连接，最终断开错误码reason:19，表示对方主动断开。

<img src="img/how_to_analyze_bluetooth_issues/gap/service_no_profile_acl_disconnect.png" alt="service:观察蓝牙服务log，是否有Profile连接" width="50%">

#### 2 观察HCI log，是否有Profile连接
如下，从HCI log看ACL连接成功，设备绑定完成后，SDP服务发现完成，未连接其他Profile，最终设备断开Remote User Terminated Connection（图上是对方主动断开，也很有可能本地协议栈主动断开）。

<img src="img/how_to_analyze_bluetooth_issues/gap/snoop_no_profile_acl_disconnect.png" alt="snoop:观察HCI log，是否有Profile连接" width="50%">

#### 3 观察空口log，是否有Profile连接
如下，从空口log看ACL连接成功，设备绑定完成后，SDP服务发现完成，未连接其他Profile，最终设备Detach断开（图上是对方主动断开，也很有可能本地协议栈主动断开）。

<img src="img/how_to_analyze_bluetooth_issues/gap/sniffer_no_profile_acl_disconnect.png" alt="sniffer:观察空口log，是否有Profile连接" width="50%">

<a id="方法观察是否本地配对信息无效"></a>

### 方法：观察是否本地配对信息无效（Linkey Missing）

#### 1 观察HCI log，手表本地配对信息无效，手机保存上次配对信息
如下，HCI log看本地linkkey未空，发起配对时Host端回复Negative Reply，然后重启发起配对，最终在Simple Pairing Complete阶段提示Authentication Fail，断开连接。

<img src="img/how_to_analyze_bluetooth_issues/gap/snoop_local_key_missing.png" alt="snoop:观察HCI log，手表本地配对信息无效，手机保存上次配对信息" width="50%">

#### 2 观察空口log，手表本地配对信息无效，手机保存上次配对信息
如下，从空口log看，手表本地配对信息无效，手机保存上次配对信息,提示DH Key Check失败。

<img src="img/how_to_analyze_bluetooth_issues/gap/sniffer_local_key_missing.png" alt="sniffer:观察空口log，手表本地配对信息无效，手机保存上次配对信息" width="50%">

#### 3 观察协议栈log，手表本地配对信息无效，手机保存上次配对信息
如下，观察协议栈log，手表本地配对信息无效，手机保存上次配对信息,从协议栈的HCI log Authentication_Complete时收到PIN OR KEY MISSING，最终配对失败。

```text
[ 1103.523193] [13] [cp]    ->[L2CAP,PSM:3][Out][Request:][RequestNum:0]
[ 1103.526428] [13] [cp] ---->[HCISEC][Go][Link_Bondable][Link_Bonded][Node_Encrypt]
[ 1103.526916] [13] [cp]    ->[Link:P256,LinkKey,Bonded,Bondable[key_type:Unauthenticated Combination Key generated from P256 | 07]
[ 1103.527282] [13] [cp]    ->[SSP_Enable][SC_Enable][SSP:OK][LinkKey_Good]
[ 1103.527526] [13] [cp]    ->[Local_Bondable:General]
[ 1103.528625] [13] [cp] ---->[HCI][CMDN][P:0,$:2][+Authentication_Requested]
[ 1103.532348] [13] [cp] ---->[HCI][*Send][AID:0,PLen:2][Authentication_Requested]
[ 1103.532653] [13] [cp]    ->[connection_handle:0129 | 81,00]
[ 1103.537719] [13] [cp] 
------>FSM Func Start<------
[ 1103.538024] [13] [cp] ---->[HCI][*Recv][AID:0,PLen:4][Command_Status]
[ 1103.538269] [13] [cp]    ->[status:OK | 00]
[ 1103.538574] [13] [cp]    ->[num_hci_command_packets:05 | 05]
[ 1103.538818] [13] [cp]    ->[command_opcode:Authentication_Requested]
[ 1103.542419] [13] [cp] 
------>FSM Func Start<------
[ 1103.542785] [13] [cp] ---->[HCI][*Recv][AID:0,PLen:6][Link_Key_Request]
[ 1103.543029] [13] [cp]    ->[bd:3c,13,5a,d5,a3,f6]
[ 1103.544311] [13] [cp] ---->[HCI][CMDN][P:1,$:2][+Link_Key_Request_Reply]
[ 1103.550903] [13] [cp] ---->[HCI][*Send][AID:0,PLen:22][Link_Key_Request_Reply]
[ 1103.551330] [13] [cp]    ->[bd:3c,13,5a,d5,a3,f6]
[ 1103.551635] [13] [cp]    ->[link_key:22,04,a4,2b,af,19,c3,ac,bc,02,f5,63,19,46,59,8d]
[ 1103.557250] [13] [cp] 
------>FSM Func Start<------
[ 1103.557617] [13] [cp] ---->[HCI][*Recv][AID:0,PLen:10][Command_Complete]
[ 1103.557861] [13] [cp]    ->[num_hci_command_packets:05 | 05]
[ 1103.558166] [13] [cp]    ->[command_opcode:Link_Key_Request_Reply]
[ 1103.558410] [13] [cp]    ->[status:OK | 00]
[ 1103.558654] [13] [cp]    ->[bd:3c,13,5a,d5,a3,f6]
[ 1103.560180] [13] [cp] ---->[HCI][CMDN][P:2,$:2][-Link_Key_Request_Reply][status:OK | 00]
[ 1103.560607] [13] [cp]    ->[COMMAND_COMPLETE][T:0x205658c0]
[ 1103.579223] [13] [cp] 
------>FSM Func Start<------
[ 1103.579528] [13] [cp] ---->[HCI][*Recv][AID:0,PLen:3][Authentication_Complete]
[ 1103.579833] [13] [cp]    ->[status:PIN OR KEY MISSING | 06]
[ 1103.580078] [13] [cp]    ->[connection_handle:0129 | 81,00]
[ 1103.581848] [13] [cp] ---->[HCI][CMDN][P:1,$:2][-Authentication_Requested][status:PIN OR KEY MISSING | 06]
[ 1103.582275] [13] [cp]    ->[Authentication_Complete][T:0x205680e0]
[ 1103.583557] [13] [cp] ---->[HCISEC][ResultEv][Failed:0x6][Ev:Authenticate]
------>FSM Func Start<------
[ 1104.618957] [13] [cp] ---->[HCI][Link][ACL][IdleExpire]
[ 1104.619201] [13] [cp]    ->[Local:[Identity:82,77,16,b2,4e,7b,Pub]]
[ 1104.619506] [13] [cp]    ->[Remote:[BREDR][Identity:3c,13,5a,d5,a3,f6,Pub][LELink:3c,13,5a,d5,a3,f6,Pub]]
[ 1104.619934] [13] [cp]    ->[HDL:0x81][Sending:0][Recv:N:0][Initiator][Connection_Completed][Master][Ref:0][READY_OK][LinkMode:Active]
[ 1104.621215] [13] [cp] ---->[HCI][CMDN][P:0,$:2][+Disconnect]
[ 1104.625915] [13] [cp] ---->[HCI][*Send][AID:0,PLen:3][Disconnect]
[ 1104.626281] [13] [cp]    ->[connection_handle:0129 | 81,00]
[ 1104.626586] [13] [cp]    ->[reason:REMOTE USER TERMINATED CONNECTION | 13]
```

<a id="方法观察是否对方配对信息无效"></a>

### 方法：观察是否对方配对信息无效（Linkey Missing）

#### 1 观察HCI log，手机配对信息无效，本地配对信息有效
如下，snoop  log看本地发起绑定过程，上报hci Authentication completed事件，对应的原因是PIN Or Key Missing。

<img src="img/how_to_analyze_bluetooth_issues/gap/snoop_remote_key_missing.png" alt="snoop:观察HCI log，手机配对信息无效，本地配对信息有效" width="50%">

#### 2 观察空口log，手机配对信息无效，本地配对信息有效
如下, air log看本地发起绑定，在LMP Authentication过程，提示LMP Not Accepted，原因是PIN Or Key Missing。

<img src="img/how_to_analyze_bluetooth_issues/gap/sniffer_remote_key_missing.png" alt="sniffer:观察空口log，手机配对信息无效，本地配对信息有效" width="50%">

<a id="发现连接配对典型问题"></a>

## 典型问题

<a id="问题-经典蓝牙设备主动绑定对方设备失败"></a>

### 问题：经典蓝牙设备主动绑定对方设备失败

设备主动绑定失败，可通过下面方法，进一步定位原因。

* [观察是否对方设备未打开可连接模式](#方法观察是否对方设备未打开可连接模式)
  * 若是对方设备未打开可连接模式，建议观察手机端未打开可连接模式原因。
  * 否则，建议按照如下步骤进一步分析。

* [观察是否对方设备未打开可连接模式(Page Timeout)](#方法观察是否对方设备未打开可连接模式)
  * 若是对方设备未打开可连接模式，建议观察手机端未打开可连接模式原因。
  * 否则，建议按照如下步骤进一步分析。

* [观察是否ACL连接超时断开(Connection Timeout)](#方法观察是否ACL连接超时断开)
  * 若是在通信距离有效方位内，，出现链路层连接超时，请补充空口log及HCI log，一般需要芯片厂商进一步确认蓝牙Controller行为。
  * 否则，建议按照如下步骤进一步分析。

* [观察是否已经绑定成功，但是未有Profile连接，ACL主动断开](#方法观察是否已经绑定成功，但是未有Profile连接，ACL主动断开)
  * 若ACL连接成功后，未连接A2DP、HID等Profile，设备会断开，符合预期。
  * 否则，建议按照如下步骤进一步分析。

* [观察是否本地配对信息无效(Linkey Missing)](#方法观察是否本地配对信息无效)
  * 若本地Linkey无效或者丢失（离线取消配对），对方绑定信息有效，手表主动发起配对可能失败，符合预期。
  * 否则，建议按照如下步骤进一步分析。

* [观察是否对方配对信息无效(Linkey Missing)](#方法观察是否对方配对信息无效)
  * 若对方Linkey无效或者丢失（离线取消配对），本地绑定信息有效，手表主动发起配对可能失败，符合预期。
  * 否则，建议上传蓝牙服务log、协议栈log、空口log和手机snoop log，再进一步分析。


# 音频传输问题

# 音乐播放控制问题

本章介绍Audio/Vedio Remote Control Profile（AVRCP）相关问题常用的分析、定位方法。  
AVRCP是蓝牙音视频遥控协议，包含Controller（CT）和Target（TG）两个角色。通常，CT是控制方，TG是受控方。Vela蓝牙服务框架中，蓝牙音乐输出设备（例如音箱/耳机/车机）可以为AVRCP-CT，蓝牙音乐源设备（例如手机/手表/手环）可以为AVRCP-TG。

## 分析方法

<a id="方法：观察是否建立了AVRCP连接"></a>

### 方法：观察是否建立了AVRCP连接

通常，可以通过syslog，snoop log，或者air log观察是否建立了AVRCP连接。

#### 1 通过syslog观察是否建立了AVRCP连接

典型log如下：

* AVRCP CT 连接对端设备（AVRCP TG）成功
```
[avrcp_controller]: avrc ct connnection --> device:[AA:AA:AA:AA:AA:AA], state: 2
```
* AVRCP TG 连接对端设备（AVRCP CT）成功
```
[avrcp_target]: avrc tg connnection --> device:[AA:AA:AA:AA:AA:AA], state: 2
```

#### 2 通过snoop log观察是否建立了AVRCP连接，以及观察可能的失败原因

典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_avctp_establishment.png" alt="snoop:AVRCP连接" width="50%">

#### 3 通过air log观察是否建立了AVRCP连接，以及观察可能的失败原因

典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/sniffer_avctp_establishment.png" alt="sniffer:AVRCP连接" width="50%">

<a id="方法：观察设备是否支持AVRCP"></a>

### 方法：观察设备是否支持AVRCP

当两个设备均未能发起AVRCP连接时，建议观察双方设备是否支持AVRCP。通常，可以通过syslog，snoop log，或者air log观察设备是否支持AVRCP。

#### 1 通过syslog观察本地设备是否打开了AVRCP服务

典型log如下：

* AVRCP CT 服务注册成功
```
[service_manager]: AVRCP-CT service register success
```
* AVRCP CT 服务开启成功
```
[service_manager]: service_on_startup {AVRCP-CT} start ret:1
```
* AVRCP TG 服务注册成功
```
[service_manager]: AVRCP-TG service register success
```
* AVRCP TG 服务开启成功
```
[service_manager]: service_on_startup {AVRCP-TG} start ret:1
```

#### 2 通过snoop log或air log观察双方设备是否支持AVRCP

典型log如下：

* SDP中，声明支持AVRCP-CT角色

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_sdp_avrc_controller.png" alt="snoop:AVRCP-CT服务" width="50%">

* SDP中，声明支持AVRCP-TG角色

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_sdp_avrc_target.png" alt="snoop:AVRCP-TG服务" width="50%">

<a id="方法：观察是否发送了播放、暂停请求"></a>

### 方法：观察是否发送了播放、暂停请求

通过syslog，snoop log，或者air log可以观察是否发送了播放、暂停请求。

#### 1 通过syslog观察是否发送了播放、暂停请求

典型log如下：
* 本地设备发送了播放、暂停请求
```
[avrcp_controller]: avrcp_ct_on_play
[avrcp_controller]: avrcp_ct_on_pause
```
* 对端设备按下播放键、抬起播放键、按下暂停键、抬起暂停键
```
[avrcp_target]: passthrough cmd: 40, state: 0
[avrcp_target]: passthrough cmd: 40, state: 1
[avrcp_target]: passthrough cmd: 42, state: 0
[avrcp_target]: passthrough cmd: 42, state: 1
```

#### 2 通过snoop log或air log观察是否发送了播放、暂停请求

典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_passthrough_pause_play.png" alt="snoop:AVRCP播放暂停请求" width="50%">

<a id="方法：观察是否使用了绝对音量"></a>

### 方法：观察是否使用了绝对音量

AVRCP-CT和AVRCP-TG使用绝对音量的前提是双方均支持绝对音量功能。

#### 1 通过syslog观察是否支持绝对音量

对端设备请求注册volume changed notification（EventID = 0x0D），表明双方均支持绝对音量
```
[avrcp_controller]: register notification event: 13
```

#### 2 通过snoop log观察是否支持绝对音量

绝对音量功能中，音乐源设备（手机）需要在SDP声明支持AVRCP-CT角色，音乐播放设备（耳机）需要在SDP声明支持AVRCP-TG角色。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_sdp_absolute_volume_supported.png" alt="snoop:AVRCP绝对音量" width="50%">

此外，音乐源设备（手机）向音乐播放设备（耳机）注册音量变化事件，表明双方均支持绝对音量。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_register_notification_volume_changed.png" alt="snoop:AVRCP注册音量变化" width="50%">

<a id="方法：观察手机是否设置了绝对音量"></a>

### 方法：观察音乐源设备（手机）是否设置了绝对音量

当双方均支持绝对音量时，音乐源设备（手机）需要发送set absolute volume改变音乐播放设备（耳机）的音量。可以通过snoop log，或air log观察手机是否设置了绝对音量。

#### 1 通过snoop log或air log观察手机是否设置了绝对音量

典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_set_absolute_volume.png" alt="snoop:AVRCP设置绝对音量" width="50%">

<a id="方法：观察本地设备是否设置了绝对音量"></a>

### 方法：观察本地设备是否设置了绝对音量

若音乐源设备（手机）正确设置了绝对音量，本地却未能生效，需要观察本地音量未能生效的原因。通过syslog可以观察本地设备是否成功设置了绝对音量。

#### 1 通过syslog观察本地设备是否设置了绝对音量

典型log如下：

```
[avrcp_controller]: set absolute volume rsp: status: 0, volume: 50
```

<a id="方法：观察手机是否改变了音频幅值"></a>

### 方法：观察音乐源设备（手机）是否改变了音频幅值

#### 1 通过音频源文件观察音乐源设备（手机）是否改变了音频幅值

通常可以通过air log导出音频，解析音乐文件，观察幅值变化。典型的蓝牙音频文件如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/pcm_volume_changed.png" alt="pcm:通过幅值判断音量" width="50%">

#### 2 通过air log观察音乐源设备（手机）是否改变了音频幅值

对于SBC和AAC编码的音频，可以使用以下方式粗略的分辨音量大小，但不准确。更多的时候，可以用来判断是否静音。

对于SBC编码的音频，可以通过Media Payload中的Scale Factor判断音量。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/sniffer_sbc_scale_factor.png" alt="sniffer:通过Scale Factor判断SBC音量" width="50%">

对于AAC编码的音频，可以通过编码帧长度判断音量。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/sniffer_aac_payload_length.png" alt="sniffer:通过Payload Length判断AAC音量" width="50%">

<a id="方法：观察是否打开了AVRCP配置"></a>

### 方法：观察是否打开了AVRCP配置

通常可以通过.config文件观察是否打开了AVRCP配置。在编译产物中，.config文件位于蓝牙服务所在核路径下，例如：
```
image/sim-vela/vela/.config
image/qemu-vela/goldfish-armeabi-v7a-ap/.config
```
AVRCP相关配置如下：

```
CONFIG_BLUETOOTH_AVRCP_TARGET=y
CONFIG_BLUETOOTH_AVRCP_CONTROL=y
```

## 典型问题

### 问题: 不能控制播放、暂停

本地设备不能控制对端设备上的播放器进行播放、暂停，可能有多种原因导致，可考虑的定位方法包括：

* [观察是否建立了AVRCP连接](#方法：观察是否建立了AVRCP连接)

  * 若双方设备中，至少一方发起了连接，但连接失败，建议对比典型log，分析连接失败的原因。

  * 若双方设备均未能发起上述连接，建议[观察双方设备是否支持AVRCP](#方法：观察设备是否支持AVRCP)。

  * 若AVRCP连接成功，建议[观察是否发送了播放、暂停请求](#方法：观察是否发送了播放、暂停请求)。

* [观察设备是否支持AVRCP](#方法：观察设备是否支持AVRCP)

  * 若音乐源设备（A2DP-SRC）不支持AVRCP-TG，或音乐播放设备（A2DP-SNK）不支持AVRCP-CT，则建议[观察是否打开了相应配置](#方法：观察是否打开了AVRCP配置)。
    
  * 若音乐源设备（A2DP-SRC）未能正确的注册或开启AVRCP-TG服务，或者音乐播放设备（A2DP-SNK）未能正确的注册或开启AVRCP-CT服务，则建议根据syslog观察失败原因。
    
  * 若音乐源设备（A2DP-SRC）支持AVRCP-TG，且音乐播放设备（A2DP-SNK）支持AVRCP-CT，则双方应当至少有一方主动发起连接。若双方均未发起连接，则建议首先观察音乐播放设备（A2DP-SNK）为什么没有发起AVRCP连接。

* [观察是否发送了播放、暂停请求](#方法：观察是否发送了播放、暂停请求)

  * 若本地设备未能发送播放、暂停请求，建议在App侧观察是否调用了Media Session相关接口。

  * 若本地设备发送了播放、暂停请求，建议观察手机侧行为异常的原因。

### 问题: 不能受音乐源设备（手机）控制调节音量

AVRCP音量调节问题，分为绝对音量和相对音量两种。首先需要判断当前产品使用了哪一种调节方式。可考虑的定位方法包括：

* [观察是否使用了绝对音量](#方法：观察是否使用了绝对音量)

  * 若双方设备均支持绝对音量，则建议[观察音乐源设备是否设置了绝对音量](#方法：观察手机是否设置了绝对音量)。

  * 双方设备未使用绝对音量，则音乐播放设备（耳机）不参与音量调节，由音乐源设备（手机）自行修改音频幅值。建议[观察音乐源设备是否改变了音频幅值](#方法：观察手机是否改变了音频幅值)。

* [观察手机是否设置了绝对音量](#方法：观察手机是否设置了绝对音量)

  * 若音乐源设备（手机）未能设置绝对音量，建议观察手机侧行为异常的原因。

  * 若音乐源设备（手机）设置了绝对音量，但本地未能生效，建议[观察本地设备是否设置了绝对音量](#方法：观察本地设备是否设置了绝对音量)

* [观察本地设备是否设置了绝对音量](#方法：观察本地设备是否设置了绝对音量)

  * 若本地设备设置了绝对音量，但观察不到本地音量变化，建议在Vela Media侧观察音量未能生效的原因。

  * 若本地设备为能正确设置绝对音量，建议根据syslog判断未能设置音量的原因。

* [观察手机是否改变了音频幅值](#方法：观察手机是否改变了音频幅值)

  * 若使用相对音量时，手机未能正确改变音频幅值，建议观察手机侧行为异常的原因。

  * 若使用相对音量时，手机正确改变了音频幅值，建议Vela Media侧观察音量变化未能体现的原因。

# 通话问题

# 数据传输问题