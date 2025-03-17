<!-- title: 如何分析蓝牙问题 -->

<!-- omit from toc -->
# 目录

- [发现、连接、配对问题](#发现连接配对问题)
  - [分析方法](#分析方法)
    - [方法：观察是否对方设备未打开可连接模式](#方法观察是否对方设备未打开可连接模式)
    - [方法：观察是否ACL连接超时断开（Connection Timeout）](#方法观察是否acl连接超时断开connection-timeout)
    - [方法：观察是否已经绑定成功，但是未有Profile连接，ACL主动断开](#方法观察是否已经绑定成功但是未有profile连接acl主动断开)
    - [方法：观察是否本地配对信息无效（Linkey Missing）](#方法观察是否本地配对信息无效linkey-missing)
    - [方法：观察是否对方配对信息无效（Linkey Missing）](#方法观察是否对方配对信息无效linkey-missing)
  - [典型问题](#典型问题)
    - [问题：经典蓝牙设备主动绑定对方设备失败](#问题经典蓝牙设备主动绑定对方设备失败)
- [音频传输问题](#音频传输问题)
  - [分析方法](#分析方法-1)
    - [方法：观察是否打开了蓝牙和Media之间的transport](#方法观察是否打开了蓝牙和media之间的transport)
    - [方法：观察是否建立了AVDTP signaling连接](#方法观察是否建立了avdtp-signaling连接)
    - [方法：观察是否建立了AVDTP media连接](#方法观察是否建立了avdtp-media连接)
    - [方法：观察Media是否成功设置了codec](#方法观察media是否成功设置了codec)
    - [方法：观察A2DP SRC是否开始播放音乐](#方法观察a2dp-src是否开始播放音乐)
    - [方法：观察A2DP SRC是否停止音频流传输](#方法观察a2dp-src是否停止音频流传输)
    - [方法：观察AVDTP signaling连接是否断开](#方法观察avdtp-signaling连接是否断开)
- [音乐播放控制问题](#音乐播放控制问题)
  - [分析方法](#分析方法-2)
    - [方法：观察是否建立了AVRCP连接](#方法观察是否建立了avrcp连接)
    - [方法：观察设备是否支持AVRCP](#方法观察设备是否支持avrcp)
    - [方法：观察是否发送了播放、暂停请求](#方法观察是否发送了播放暂停请求)
    - [方法：观察是否使用了绝对音量](#方法观察是否使用了绝对音量)
    - [方法：观察音乐源设备（手机）是否设置了绝对音量](#方法观察音乐源设备手机是否设置了绝对音量)
    - [方法：观察本地设备是否设置了绝对音量](#方法观察本地设备是否设置了绝对音量)
    - [方法：观察音乐源设备（手机）是否改变了音频幅值](#方法观察音乐源设备手机是否改变了音频幅值)
    - [方法：观察是否打开了AVRCP配置](#方法观察是否打开了avrcp配置)
    - [方法：观察音量变化是否由蓝牙引起](#方法观察音量变化是否由蓝牙引起)
    - [方法：观察音量变化由AVRCP或是HFP控制](#方法观察音量变化由avrcp或是hfp控制)
  - [典型问题](#典型问题-1)
    - [问题: 不能控制播放、暂停](#问题-不能控制播放暂停)
    - [问题: 不能受音乐源设备（手机）控制调节音量](#问题-不能受音乐源设备手机控制调节音量)
    - [问题: 音量异常变化](#问题-音量异常变化)
- [通话问题](#通话问题)
  - [分析方法](#分析方法-3)
    - [方法：观察是否建立了HFP连接](#方法观察是否建立了hfp连接)
    - [方法：观察设备是否支持HFP](#方法观察设备是否支持hfp)
    - [方法：观察是否建立了SCO连接](#方法观察是否建立了sco连接)
    - [方法：观察是否向Media设置了SCO音频参数](#方法观察是否向media设置了sco音频参数)
    - [方法：观察AG端是否收到了HF端的Answer请求](#方法观察ag端是否收到了hf端的answer请求)
  - [典型问题](#典型问题-2)
    - [问题：AG端接通电话，HF端通话无声](#问题ag端接通电话hf端通话无声)
    - [问题：HF端接通电话，HF端无声](#问题hf端接通电话hf端无声)
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

本章介绍Advanced Audio Distribution Profile（A2DP）和Audio/Video Distribution Transport Protocol（AVDTP）相关问题常用的分析、定位方法。AVDTP负责控制音频/视频的传输过程，而A2DP定义了音频数据的编码和传输规范，通过这两个协议配合工作，可以实现在蓝牙设备之间高质量的音频传输。
A2DP是蓝牙音频分发配置协议，包含Sink（SNK）和Source（SRC）两个角色。通常，SRC是音频源，SNK是音频接收方。Vela蓝牙服务框架中，蓝牙音乐输出设备（例如音箱/耳机/车机）可以为A2DP-SNK，蓝牙音乐源设备（例如手机/手表）可以为A2DP-SRC。
AVDTP是蓝牙音频传输控制协议，协议中定义了Stream End Point Discovery过程、Get All Capabilities/Get Capabilities过程、Stream Configuration过程、Get All Capabilities/Get Capabilities过程、Stream Configuration过程、Stream Establishment、 Stream Start等AVDTP信令过程。AVDTP信令过程的发起方称为Initiator（INT），信令过程的接收方称为Acceptor (ACP)。
蓝牙设备传输音频时需要建立两条AVDTP连接。首先建立AVDTP signaling连接，用于编解码参数的协商和media连接的控制，协商完成（AVDTP open）后，再建立AVDTP media连接，用于传输音频数据。
蓝牙和Media之间有两条transport channel，分别为control channel和data channel，其中，control channel用于传输控制信息，data channel用于传输音频数据。

## 分析方法

<a id="方法：观察是否打开了蓝牙和Media之间的transport"></a>

### 方法：观察是否打开了蓝牙和Media之间的transport

通常，可以通过syslog观察蓝牙和Media之间的control channel和data channel是否打开。

典型的log如下：

* A2DP SRC的transport成功打开
```
[a2dp_control]: a2dp_ctrl_cb, path:[a2dp_source_ctrl], event:TRANSPORT_OPEN_EVT
[a2dp_control]: a2dp_data_cb, path:[a2dp_source_data], event:TRANSPORT_OPEN_EVT
```
* A2DP SNK的transport成功打开
```
[a2dp_control]: a2dp_ctrl_cb, path:[a2dp_sink_ctrl], event:TRANSPORT_OPEN_EVT
[a2dp_control]: a2dp_data_cb, path:[a2dp_sink_data], event:TRANSPORT_OPEN_EVT
```

<a id="方法：观察是否建立了AVDTP signaling连接"></a>

### 方法：观察是否建立了AVDTP signaling连接

通常，可以通过snoop log或者air log观察是否建立了AVDTP signaling连接。

#### 1 通过snoop log观察是否建立了AVDTP signaling连接，以及观察可能的失败原因

AVDTP signaling连接成功的典型log如下，其中两个设备间建立的第一条AVDTP连接为AVDTP signaling连接。

<img src="img/how_to_analyze_bluetooth_issues/a2dp/snoop_avdtp_signaling_establishment.png" alt="snoop:AVDTP signaling连接" width="50%">

<a id="方法：观察是否建立了AVDTP media连接"></a>

### 方法：观察是否建立了AVDTP media连接

建立AVDTP media连接之前，可能会进行Discovery、Get（ALL）Capabilities、set/get Configuration、Stream Establishment等过程，其中，Set Configuration和Stream Establishment过程是必须的。通常，可以通过syslog、snoop log或者air log观察是否建立了AVDTP media连接

#### 1 通过snoop log观察是否建立了AVDTP media连接，以及观察可能的失败原因

下面log中，Command是AVDTP Int，回复Accept的是AVDTP Acp。

##### 1.1 AVDTP Discovery

可选的，在建立AVDTP media连接之前，可以发起AVDTP Discovery过程，用于发现对方设备可用的Stream End Point(SEP)。通常，发起AVDTP signaling连接的设备会发起这一过程。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/a2dp/snoop_avdtp_discovery.png" alt="snoop:AVDTP discovery" width="50%">

log有显示Acp的序号从1到6,说明对方设备的SEP一共有6个。

##### 1.2 AVDTP Get Capabilities

可选的，在建立AVDTP media连接之前，可以通过Get Capabilities或者Get All Capabilities获取对方SEP的具体信息。通常，发起AVDTP signaling连接的设备会发起这一流程。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/a2dp/snoop_avdtp_get_capabilities.png" alt="snoop:AVDTP get capabilities" width="50%">

log显示本地设备获取对方设备的1号SEP的Capabilities。

##### 1.3 AVDTP Set Configuration

在建立AVDTP media连接之前，需要通过Set Configuration过程选定双方的SEP，以及编解码参数。通常，发起AVDTP signaling连接的设备应当发起这一流程。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/a2dp/snoop_avdtp_set_configuration.png" alt="snoop:AVDTP set configuration" width="50%">

log中显示使用本地的1号SEP和对方设备的1号SEP进行音频传输。

##### 1.4 AVDTP Stream Establishment

在建立AVDTP media连接之前，需要通过Open打开双方的SEP。通常，发起AVDTP signaling连接的设备应当发起这一流程。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/a2dp/snoop_avdtp_stream_establishment.png" alt="snoop:AVDTP stream establishment" width="50%">

##### 1.5 AVDTP media连接成功

完成Set Configuration和Stream Establish流程后，需要建立第二条AVDTP连接，也就是AVDTP media连接。通常，发起AVDTP signaling连接的设备应当发起这一流程。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/a2dp/snoop_avdtp_media_establishment.png" alt="snoop:AVDTP media连接" width="50%">

通常，AVDTP Open过程后面的L2CAP（PSM=AVDTP）是AVDTP media连接。

#### 2 通过syslog观察是否建立了AVDTP media连接，以及观察可能的失败原因

典型log如下：

* 本地设备被连接
```
[a2dp_stm]: ProcessEvent, State=Idle, Peer=[11:22:33:44:55:66], Event=CONNECTED_EVT
[a2dp_stm]: Enter State=Opened, Peer=[11:22:33:44:55:66]
```
* 本地设备主动连接对端设备
```
[a2dp_stm]: ProcessEvent, State=Opening, Peer=[11:22:33:44:55:66], Event=CONNECTED_EVT
[a2dp_stm]: Enter State=Opened, Peer=[11:22:33:44:55:66]
```

<a id="方法：观察Media是否成功设置了codec"></a>

### 方法：观察Media是否成功设置了codec

传输或播放音乐前，需要在Media子系统设置编解码参数。可以通过syslog观察Media是否成功设置了编解码参数。

典型log如下：

```
[a2dp_control]: a2dp_recv_ctrl_data: a2dp-ctrl-cmd : A2DP_CTRL_CMD_CONFIG_DONE
```

<a id="方法：观察A2DP SRC是否开始播放音乐"></a>

### 方法：观察A2DP SRC是否开始播放音乐

通常，可以通过syslog、snoop log或者air log观察A2DP SRC是否开始播放音乐。

#### 1 通过syslog观察A2DP SRC是否开始播放音乐

在A2DP SRC端，Vela蓝牙服务开始播放音乐的流程由来自Media的命令触发，典型log如下：

```
[a2dp_control]: a2dp_recv_ctrl_data: a2dp-ctrl-cmd : A2DP_CTRL_CMD_START
```

当蓝牙服务收到开始播放音乐的命令时，会开始AVDTP Stream Start流程，并在流程成功结束后进入Started状态，典型log如下：

```
[a2dp_stm]: ProcessEvent, State=Opened, Peer=[11:22:33:44:55:66], Event=STREAM_START_REQ
[a2dp_stm]: ProcessEvent, State=Opened, Peer=[11:22:33:44:55:66], Event=STREAM_STARTED_EVT
[a2dp_stm]: Exit  State=Opened, Peer=[11:22:33:44:55:66]
[a2dp_stm]: Enter State=Started, Peer=[11:22:33:44:55:66]
```

#### 2 通过air log观察A2DP SRC是否开始播放音乐

在音频流开始传输之前，A2DP SRC会发起Stream Start流程。在音频流传输过程中，A2DP SRC会向SNK发送media packets，典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/a2dp/sniffer_avdtp_stream_start.png" alt="sniffer:AVDTP media start" width="50%">

<a id="方法：观察A2DP SRC是否停止传输音频包"></a>

### 方法：观察A2DP SRC是否停止音频流传输

通常，可以通过syslog、snoop log或者air log观察A2DP SRC是否停止音频流传输。

#### 1 通过syslog观察A2DP SRC是否停止音频流传输

当Vela设备为A2DP SRC时，蓝牙服务有两个途径终止传输音频数据。
* 当收到Media发送的STOP命令时。
* 当连续2秒不能从Media获取音频数据时。

蓝牙服务收到Media发送的STOP命令时，典型log如下：

```
[a2dp_control]: a2dp_recv_ctrl_data: a2dp-ctrl-cmd : A2DP_CTRL_CMD_STOP
```

蓝牙2秒从media读不到数据，syslog中会打印如下log，且持续时间约2秒：

```
[src_sbc]: a2dp_sbc_send_frames, underflow :6
```

蓝牙服务发起Stream Suspend流程的典型log如下：

```
[a2dp_stm]: ProcessEvent, State=Started, Peer=[11:22:33:44:55:66], Event=STREAM_SUSPEND_REQ
[a2dp_stm]: ProcessEvent, State=Started, Peer=[11:22:33:44:55:66], Event=STREAM_SUSPENDED_EVT
[a2dp_stm]: Exit  State=Started, Peer=[11:22:33:44:55:66]
[a2dp_stm]: Enter State=Opened, Peer=[11:22:33:44:55:66]
```

#### 1 通过snoop log观察A2DP SRC是否停止传输音频包

典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/a2dp/sniffer_avdtp_stream_suspend.png" alt="sniffer:AVDTP media suspend" width="50%">

### 方法：观察AVDTP signaling连接是否断开

AVDTP signaling断开的原因有：应用告诉蓝牙断开A2DP连接，蓝牙协议栈主动断开连接，对端设备请求断开连接。通常，可以通过syslog，snoop log，或者air log观察是否断开了AVDTP signaling连接。

#### 1 通过syslog观察是否断开了AVDTP signaling连接

只有应用告诉蓝牙断开AVDTP signaling连接时，a2dp状态机会收到DISCONNECT_REQ，典型log如下：

```
[a2dp_stm]: ProcessEvent, State=Opened, Peer=[11:22:33:44:55:66], Event=DISCONNECT_REQ
```

断开连接完成时的典型log如下：

```
[a2dp_stm]: ProcessEvent, State=Closing, Peer=[11:22:33:44:55:66], Event=DISCONNECTED_EVT
[a2dp_stm]: Exit  State=Closing, Peer=[11:22:33:44:55:66]
[a2dp_stm]: Enter State=Idle, Peer=[11:22:33:44:55:66]
```

#### 2 通过snoop log观察是否断开了AVDTP signaling连接，以及观察可能的失败原因

snoop log中AVDTP signaling连接断开的原因有两种：本地设备主动断开连接，对端设备请求断开连接。本地设备的snoop log中，本地设备主动断开连接的典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/a2dp/snoop_avdtp_stream_release.png" alt="snoop:AVDTP media release" width="50%">

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

<a id="方法：观察音量变化是否由蓝牙引起"></a>

### 方法：观察音量变化是否由蓝牙引起

通常，当蓝牙设备音量异常变化时，可以在相同场景中尝试断开蓝牙连接，观察是否仍然引起了音量变化。若仍可见音量变化，通常该音量变化与蓝牙连接无关。

<a id="方法：观察音量变化由AVRCP或是HFP控制"></a>

### 方法：观察音量变化由AVRCP或是HFP控制

在蓝牙规范中，AVRCP和HFP均可以控制音量。通常可以通过snoop log确定音量控制的途径。

#### 1 通过snoop log观察音量变化由AVRCP或是HFP控制

在蓝牙通话中，音量变化通常由HFP协议控制。在其他场景，音量变化通常由AVRCP协议控制。

当双方设备支持AVRCP绝对音量控制时，AVRCP TG（手机）设备可以主动设置绝对音量，典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_set_absolute_volume.png" alt="snoop:AVRCP TG改变绝对音量" width="50%">

当双方设备支持AVRCP绝对音量控制时，AVRCP CT（耳机）设备可以主动反馈绝对音量变化，典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_absolute_volume_changed.png" alt="snoop:AVRCP CT改变绝对音量" width="50%">

HFP AG（手机）设备可以主动设置通话音量，典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/hfp/snoop_hfp_ag_set_volume.png" alt="snoop:HFP AG改变音量" width="50%">

HFP HF（耳机）设备可以主动设置通话音量，典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/hfp/snoop_hfp_hf_set_volume.png" alt="snoop:HFP HF改变音量" width="50%">

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

  * 若本地设备未能正确设置绝对音量，建议根据syslog判断未能设置音量的原因。

* [观察手机是否改变了音频幅值](#方法：观察手机是否改变了音频幅值)

  * 若使用相对音量时，手机未能正确改变音频幅值，建议观察手机侧行为异常的原因。

  * 若使用相对音量时，手机正确改变了音频幅值，建议Vela Media侧观察音量变化未能体现的原因。

### 问题: 音量异常变化

当遇到蓝牙设备音量异常变化时，通常有以下方法可以逐步缩小范围并定位问题。

* [观察音量变化是否由蓝牙引起](#方法：观察音量变化是否由蓝牙引起)

  * 若音量变化并非由蓝牙连接引起，建议在产生音量变化的设备处观察原因。若该设备为Vela设备，建议在Vela Media侧观察音量变化的原因。

  * 若音量变化可能由蓝牙连接引起，建议[观察音量变化由AVRCP或是HFP控制](#方法：观察音量变化由AVRCP或是HFP控制)

* [观察音量变化由AVRCP或是HFP控制](#方法：观察音量变化由AVRCP或是HFP控制)

  * 若音量改变由AVRCP控制，建议观察控制发起方（CT或TG）发起该改变的原因。若该设备为Vela设备，建议在Vela App或Media侧观察音量改变的原因。

  * 若音量改变由HFP控制，建议观察控制发起方（AG或HF）发起该改变的原因。若该设备为Vela设备，建议在Vela App侧观察音量改变的原因。

# 通话问题
本章介绍Hands-Free Profile（HFP）相关问题常用的分析、定位方法。
HFP是蓝牙通话协议，包含Audio Gateway（AG）和Hands-Free unit （HF）两个角色。通常，AG是音频网关，负责音频设备输入输出，典型设备为手机，HF作为音频网关的远程音频输入/输出设备，典型设备为耳机。

## 分析方法

<a id="方法：观察是否建立了HFP连接"></a>

### 方法：观察是否建立了HFP连接

通常，可以通过syslog，snoop log，或者air log观察是否建立了HFP连接。

#### 1 通过syslog观察是否建立了HFP连接

典型log如下：

* HFP HF 连接对端设备（HFP AG）成功
```
[hf_stm]: Enter State=Connected, Peer=[AA:AA:AA:AA:AA:AA]
```
* HFP AG 连接对端设备（HFP HF）成功
```
[ag_stm]: Enter State=Connected, Peer=[AA:AA:AA:AA:AA:AA]
```
#### 2 通过snoop log观察是否建立了HFP连接，以及观察可能的失败原因

典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/hfp/snoop_hfp_slc.png" alt="snoop:HFP连接" width="50%">

CMER命令的交互标志着SLC建立完成，可参考下图spec中SLC建立流程，其中实线为必须操作，其余为可选操作。

<img src="img/how_to_analyze_bluetooth_issues/hfp/snoop_hfp_slc_core.png" alt="snoop:HFP连接规范" width="50%">

<a id="方法：观察设备是否支持HFP"></a>

### 方法：观察设备是否支持HFP

当两个设备均未能发起HFP连接时，建议观察双方设备是否支持HFP。通常，可以通过syslog，snoop log，或者air log观察设备是否支持HFP。

#### 1 通过syslog观察设备是否支持HFP

典型log如下：

* HFP HF 服务注册成功
```
[service_manager]: HFP-HF service register success
```
* HFP HF 服务开启成功
```
[service_manager]: service_on_startup {HFP-HF} start ret:1
```
* HFP AG 服务注册成功
```
[service_manager]: HFP-AG service register success
```
* HFP AG 服务开启成功
```
[service_manager]: service_on_startup {HFP-AG} start ret:1
```

#### 2 通过snoop log或air log观察双方设备是否支持HFP

典型log如下：

* SDP中，声明支持HFP-HF角色

<img src="img/how_to_analyze_bluetooth_issues/hfp/snoop_hfp_ag_sdp.png" alt="snoop:HFP-AG服务" width="50%">

* SDP中，声明支持HFP-AG角色

<img src="img/how_to_analyze_bluetooth_issues/hfp/snoop_hfp_hf_sdp.png" alt="snoop:HFP-HF服务" width="50%">

<a id="方法：观察是否建立了SCO连接"></a>

### 方法：观察是否建立了SCO连接

两台设备之间传输通话语音需要建立SCO连接。通常，可以通过syslog，snoop log，或者air log观察SCO是否建立成功。

#### 1 通过syslog观察是否建立了SCO连接
* HFP HF SCO建立完成并通知Media
```
[hf_stm]: Enter State=AudioOn, Peer=[AA:AA:AA:AA:AA:AA]
```
* HFP AG SCO建立完成并通知Media
```
[ag_stm]: Enter State=AudioOn, Peer=[AA:AA:AA:AA:AA:AA]
```
<a id="方法：观察是否向Media设置了SCO音频参数"></a>

### 方法：观察是否向Media设置了SCO音频参数

AG和HF都需要在SCO建立完成之后向Media设置了SCO音频参数，典型log如下：
```
[Media_proxy_once:430] policy:audio:0x20556fd4 HFPSampleRate set_int 16000 _ ret:0 resp:0
[Media_proxy_once:430] policy:audio:0x20556fec AvailableDevices include sco apply ret:0 resp:0
```

<a id="方法：观察AG端是否收到了HF端的Answer请求"></a>

### 方法：观察AG端是否收到了HF端的Answer请求

HF端发起Answer请求，需要向AG端发送ATA命令，通常，可以通过syslog，snoop log，或者air log观察AG是否收到了HF的Answer请求。

#### 1 通过syslog观察AG是否收到了HF的Anser请求

```
[hfp_ag]: ag_service_notify_call_answered
```
## 典型问题

<a id="问题：AG端接通电话，HF端通话无声"></a>

### 问题：AG端接通电话，HF端通话无声

AG端接通电话，HF端通话无声的问题可能有多种原因导致，可考虑的定位方法包括：

* [观察是否建立了HFP连接](#方法：观察是否建立了HFP连接)

  * 若双方设备中，至少一方发起了连接，但连接失败，建议对比典型log，分析连接失败的原因。

  * 若双方设备均未能发起上述连接，建议[观察双方设备是否支持HFP](#方法：观察设备是否支持HFP)。

* [观察双方设备是否建立了SCO连接](#方法：观察是否建立了SCO连接)

  * 若HFP连接成功，建议观察双方设备是否建立了SCO连接，通常，应当由AG设备发起SCO连接，在AG侧，通常由App发起SCO连接。（部分场景协议栈自己发起，需结合源码分析）。
  * 若双方均未能发起SCO连接，建议检查AG侧App为什么没有发起SCO连接。
  * 若发起SCO连接，但是连接失败，建议对比典型log，分析失败原因。
  * 若SCO建立成功，建议[观察是否向Media设置了SCO音频参数](#方法：观察是否向Media设置了SCO音频参数)。
* [观察是否向Media设置了SCO音频参数](#方法：观察是否向Media设置了SCO音频参数)
  * 若蓝牙成功设置了SCO音频参数，则蓝牙侧完成了音频传输的必要流程，建议Vela Media侧观察无声的原因。
  * 若未设置SCO音频参数，则检查是蓝牙未发送给Meida，还是发了但是卡在了和Media的跨进程通信。


<a id="问题：HF端接通电话，HF端无声"></a>

### 问题：HF端接通电话，HF端无声

* [观察AG端是否收到了HF端的Answer请求](#方法：观察AG端是否收到了HF端的Answer请求)
  * 若AG端未到了HF端的Answer请求，则检查syslog，snoop或空口log分析原因。
  * 若AG端收到了HF端的Answer请求，则参考[问题: AG端接通电话，HF端通话无声](#问题：AG端接通电话，HF端通话无声)，分析HF端无声原因。

# 数据传输问题