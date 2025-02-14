<!-- title: 如何分析蓝牙问题 -->

<!-- omit from toc -->
# 目录

- [GAP-BR/EDR](#gap-bredr)
  - [1 扫描](#1-扫描)
  - [2 连接](#2-连接)
- [SSP](#ssp)
- [A2DP](#a2dp)
  - [A2DP-SRC](#a2dp-src)
  - [A2DP-SNK](#a2dp-snk)
- [AVRCP](#avrcp)
  - [AVRCP-CT](#avrcp-ct)
    - [Issue: 不能控制播放、暂停](#issue-不能控制播放暂停)
    - [Issue: 不能受音乐源设备（手机）控制调节音量](#issue-不能受音乐源设备手机控制调节音量)
  - [AVRCP-TG](#avrcp-tg)
    - [Issue: 不能受控改变播放、暂停状态](#issue-不能受控改变播放暂停状态)
- [HFP](#hfp)
  - [HFP-HF](#hfp-hf)
  - [HFP-AG](#hfp-ag)
- [PBAP](#pbap)
- [SPP](#spp)
- [HID](#hid)
- [GAP-LE](#gap-le)
  - [广告](#广告)
  - [扫描](#扫描)
  - [连接](#连接)
- [SMP](#smp)
- [GATT](#gatt)
  - [GATT Client](#gatt-client)
  - [GATT Server](#gatt-server)
- [LE Audio](#le-audio)
- [Mesh](#mesh)

---

# GAP-BR/EDR

## 1 扫描

## 2 连接

# SSP

# A2DP

## A2DP-SRC

## A2DP-SNK

# AVRCP

本章介绍Audio/Vedio Remote Control Profile（AVRCP）相关问题常用的分析、定位方法。  
AVRCP是蓝牙音视频遥控协议，包含Controller（CT）和Target（TG）两个角色。通常，CT是控制方，TG是受控方。Vela蓝牙服务框架中，蓝牙音乐输出设备（例如音箱/耳机/车机）可以为AVRCP-CT，蓝牙音乐源设备（例如手机/手表/手环）可以为AVRCP-TG。

## AVRCP-CT

### Issue: 不能控制播放、暂停

本地设备不能控制对端设备上的播放器进行播放、暂停，可能有多种原因导致，建议由以下步骤定位问题：

<a id="AVRCP-CT-观察是否建立了AVRCP连接"></a>

#### 1 观察是否建立了AVRCP连接

通常，可以通过syslog，snoop log，或者air log观察是否建立了AVRCP连接。

##### 1.1 通过syslog观察是否建立了AVRCP连接

典型log如下：

```
[avrcp_controller]: avrc ct connnection --> device:[AA:AA:AA:AA:AA:AA], state: 2
```

##### 1.2 通过snoop log观察是否建立了AVRCP连接，以及观察可能的失败原因

典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_avctp_establishment.png" alt="snoop:AVRCP连接" width="50%">

##### 1.3 通过air log观察是否建立了AVRCP连接，以及观察可能的失败原因

典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/sniffer_avctp_establishment.png" alt="sniffer:AVRCP连接" width="50%">

##### 1.4 分析方法

* 若双方设备中，至少一方发起了连接，但连接失败，建议对比上述典型log，分析连接失败的原因。

* 若双方设备均未能发起上述连接，建议[观察双方设备是否支持AVRCP](#AVRCP-CT-观察是否支持AVRCP)。

* 若AVRCP连接成功，建议[观察是否发送了播放、暂停请求](#观察是否发送了播放、暂停请求)。

<a id="AVRCP-CT-观察是否支持AVRCP"></a>

#### 2 观察设备是否支持AVRCP

当两个设备均未能发起AVRCP连接时，建议观察双方设备是否支持AVRCP。通常，可以通过syslog，snoop log，或者air log观察设备是否支持AVRCP。

##### 2.1 通过syslog观察本地设备是否打开了AVRCP-CT服务

典型log如下：

* AVRCP CT 服务注册成功
```
[service_manager]: AVRCP-CT service register success
```
* AVRCP CT 服务开启成功
```
[service_manager]: service_on_startup {AVRCP-CT} start ret:1
```

<a id="snoop:SDP声明支持AVRCP"></a>

##### 2.2 通过snoop log观察双方设备是否支持AVRCP

典型log如下：

* SDP中，声明支持AVRCP-CT角色

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_sdp_avrc_controller.png" alt="snoop:AVRCP-CT服务" width="50%">

* SDP中，声明支持AVRCP-TG角色

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_sdp_avrc_target.png" alt="snoop:AVRCP-TG服务" width="50%">

<a id="sniffer:SDP声明支持AVRCP"></a>

##### 2.3 通过air log观察双方设备是否支持AVRCP

Air log解析同[snoop log](#snoop:SDP声明支持AVRCP)

##### 2.4 分析方法

* 若音乐源设备（A2DP-SRC）不支持AVRCP-TG，或音乐播放设备（A2DP-SNK）不支持AVRCP-CT，则建议观察编译选项，是否打开了相应设置。
  
* 若音乐源设备（A2DP-SRC）未能正确的注册或开启AVRCP-TG服务，或者音乐播放设备（A2DP-SNK）未能正确的注册或开启AVRCP-CT服务，则建议根据syslog观察失败原因。
  
* 若音乐源设备（A2DP-SRC）支持AVRCP-TG，且音乐播放设备（A2DP-SNK）支持AVRCP-CT，则双方应当至少有一方主动发起连接。若双方均未发起连接，则建议首先观察音乐播放设备（A2DP-SNK）为什么没有发起AVRCP连接。

<a id="观察是否发送了播放、暂停请求"></a>

#### 3 观察是否发送了播放、暂停请求

通过syslog，snoop log，或者air log可以观察是否发送了播放、暂停请求。

##### 3.1 通过syslog观察是否发送了播放、暂停请求

典型log如下：

```
[avrcp_controller]: avrcp_ct_on_play
[avrcp_controller]: avrcp_ct_on_pause
```

##### 3.2 通过snoop log或air log观察是否发送了播放、暂停请求

典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_passthrough_pause_play.png" alt="snoop:AVRCP播放暂停请求" width="50%">

##### 3.3 分析方法

* 若本地设备未能发送播放、暂停请求，建议在App侧观察是否调用了Media Session相关接口。

* 若本地设备发送了播放、暂停请求，建议观察手机侧行为异常的原因。

### Issue: 不能受音乐源设备（手机）控制调节音量

AVRCP音量调节问题，分为绝对音量和相对音量两种。首先需要判断当前产品使用了哪一种调节方式。

#### 1 观察是否使用了绝对音量

AVRCP-CT和AVRCP-TG使用绝对音量的前提是双方均支持绝对音量功能。

##### 1.1 通过syslog观察是否支持绝对音量

对端设备请求注册volume changed notification（EventID = 0x0D），表明双方均支持绝对音量
```
[avrcp_controller]: register notification event: 13
```

##### 1.2 通过snoop log观察是否支持绝对音量

绝对音量功能中，音乐源设备（手机）需要在SDP声明支持AVRCP-CT角色，音乐播放设备（耳机）需要在SDP声明支持AVRCP-TG角色。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_sdp_absolute_volume_supported.png" alt="snoop:AVRCP绝对音量" width="50%">

此外，音乐源设备（手机）向音乐播放设备（耳机）注册音量变化事件，表明双方均支持绝对音量。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_register_notification_volume_changed.png" alt="snoop:AVRCP注册音量变化" width="50%">

##### 1.3 分析方法

* 若双方设备均支持绝对音量，则建议[观察音乐源设备是否设置了绝对音量](#观察手机是否设置了绝对音量)。

* 双方设备未使用绝对音量，则音乐播放设备（耳机）不参与音量调节，由音乐源设备（手机）自行修改音频幅值。建议[观察音乐源设备是否改变了音频幅值](#观察手机是否改变了音频幅值)。

<a id="观察手机是否设置了绝对音量"></a>

#### 2 观察音乐源设备（手机）是否设置了绝对音量

当双方均支持绝对音量时，音乐源设备（手机）需要发送set absolute volume改变音乐播放设备（耳机）的音量。可以通过snoop log，或air log观察手机是否设置了绝对音量。

##### 2.1 通过snoop log或air log观察手机是否设置了绝对音量

典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/snoop_set_absolute_volume.png" alt="snoop:AVRCP设置绝对音量" width="50%">

##### 2.2 分析方法

* 若音乐源设备（手机）未能设置绝对音量，建议观察手机侧行为异常的原因。

* 若音乐源设备（手机）设置了绝对音量，但本地未能生效，建议[观察本地设备是否设置了绝对音量](#观察本地设备是否设置了绝对音量)

<a id="观察本地设备是否设置了绝对音量"></a>

#### 3 观察本地设备是否设置了绝对音量

若音乐源设备（手机）正确设置了绝对音量，本地却未能生效，需要观察本地音量未能生效的原因。通过syslog可以观察本地设备是否成功设置了绝对音量。

##### 3.1 通过syslog观察本地设备是否设置了绝对音量

典型log如下：

```
[avrcp_controller]: set absolute volume rsp: status: 0, volume: 50
```

##### 3.2 分析方法

* 若本地设备设置了绝对音量，但观察不到本地音量变化，建议在Vela Media侧观察音量未能生效的原因。

* 若本地设备为能正确设置绝对音量，建议根据syslog判断未能设置音量的原因。

<a id="观察手机是否改变了音频幅值"></a>

#### 4 观察音乐源设备（手机）是否改变了音频幅值

##### 4.1 通过音频源文件观察音乐源设备（手机）是否改变了音频幅值

通常可以通过air log导出音频，解析音乐文件，观察幅值变化。典型的蓝牙音频文件如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/pcm_volume_changed.png" alt="pcm:通过幅值判断音量" width="50%">

##### 4.2 通过air log观察音乐源设备（手机）是否改变了音频幅值

对于SBC和AAC编码的音频，可以使用以下方式粗略的分辨音量大小，但不准确。更多的时候，可以用来判断是否静音。

对于SBC编码的音频，可以通过Media Payload中的Scale Factor判断音量。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/sniffer_sbc_scale_factor.png" alt="sniffer:通过Scale Factor判断SBC音量" width="50%">

对于AAC编码的音频，可以通过编码帧长度判断音量。典型log如下：

<img src="img/how_to_analyze_bluetooth_issues/avrcp/sniffer_aac_payload_length.png" alt="sniffer:通过Payload Length判断AAC音量" width="50%">

##### 4.3 分析方法

* 若使用相对音量时，手机未能正确改变音频幅值，建议观察手机侧行为异常的原因。

* 若使用相对音量时，手机正确改变了音频幅值，建议Vela Media侧观察音量变化未能体现的原因。

## AVRCP-TG

### Issue: 不能受控改变播放、暂停状态

本地播放器不能受对端对端设备控制进行播放、暂停，可能有多种原因导致，建议由以下步骤定位问题：

#### 1  观察AVRCP是否建立了连接

通常，可以通过syslog，snoop log，或者air log观察是否建立了AVRCP连接。

##### 1.1 通过syslog观察是否建立了AVRCP连接

典型log如下：

```
[avrcp_target]: avrc tg connnection --> device:[AA:AA:AA:AA:AA:AA], state: 2
```

##### 1.2 通过snoop log观察是否建立了AVRCP连接，以及观察可能的失败原因

方法同[观察是否建立了AVRCP连接](#AVRCP-CT-观察是否建立了AVRCP连接)

##### 1.3 通过air log观察是否建立了AVRCP连接，以及观察可能的失败原因

方法同[观察是否建立了AVRCP连接](#AVRCP-CT-观察是否建立了AVRCP连接)

##### 1.4 分析方法

* 若双方设备中，至少一方发起了连接，但连接失败，建议对比上述典型log，分析连接失败的原因。

* 若双方设备均未能发起上述连接，建议[观察双方设备是否支持AVRCP](#AVRCP-TG-观察是否支持AVRCP)。

* 若双方设备正确建立了AVRCP连接，建议[观察对端设备是否发送了播放、暂停请求](#观察对端设备是否发送了播放、暂停请求)。

<a id="AVRCP-TG-观察是否支持AVRCP"></a>

#### 2 观察设备是否支持AVRCP

##### 2.1 通过syslog观察本地设备是否打开了AVRCP-TG服务

典型log如下：

* AVRCP TG 服务注册成功
```
[service_manager]: AVRCP-TG service register success
```
* AVRCP TG 服务开启成功
```
[service_manager]: service_on_startup {AVRCP-TG} start ret:1
```

##### 2.2 通过snoop log观察双方设备是否支持AVRCP

方法同[AVRCP-CT：通过snoop log观察双方设备是否支持AVRCP](#snoop:SDP声明支持AVRCP)

##### 2.3 通过air log观察双方设备是否支持AVRCP

方法同[AVRCP-CT：通过air log观察双方设备是否支持AVRCP](#sniffer:SDP声明支持AVRCP)

##### 2.4 分析方法

* 若音乐源设备（A2DP-SRC）不支持AVRCP-TG，或音乐播放设备（A2DP-SNK）不支持AVRCP-CT，则建议观察编译选项，是否打开了相应设置。
  
* 若音乐源设备（A2DP-SRC）未能正确的注册或开启AVRCP-TG服务，或者音乐播放设备（A2DP-SNK）未能正确的注册或开启AVRCP-CT服务，则建议根据syslog观察失败原因。
  
* 若音乐源设备（A2DP-SRC）支持AVRCP-TG，且音乐播放设备（A2DP-SNK）支持AVRCP-CT，则双方应当至少有一方主动发起连接。若双方均未发起连接，则建议首先观察音乐播放设备（A2DP-SNK）为什么没有发起AVRCP连接。

<a id="观察对端设备是否发送了播放、暂停请求"></a>

#### 3 观察对端设备是否发送了播放、暂停请求

通过syslog，snoop log，或者air log可以观察对端设备是否发送了播放、暂停请求。

##### 3.1 通过syslog观察对端设备是否发送了播放、暂停请求

以下4个典型log依次分别对应了播放键按下、播放键抬起、暂停键按下、暂停键抬起。

```
[avrcp_target]: passthrough cmd: 40, state: 0
[avrcp_target]: passthrough cmd: 40, state: 1
[avrcp_target]: passthrough cmd: 42, state: 0
[avrcp_target]: passthrough cmd: 42, state: 1
```

##### 3.2 通过snoop log或air log观察对端设备是否发送了播放、暂停请求

观察方法同[AVRCP-CT：观察是否发送了播放、暂停请求](#观察是否发送了播放、暂停请求)

##### 3.3 分析方法

* 若对端设备未能发送播放、暂停请求，建议观察对端设备行为异常的原因。

* 若对端设备发送了播放、暂停请求，建议观察App侧是否正确收到并响应了相关消息。

# HFP

## HFP-HF

## HFP-AG

# PBAP

# SPP

# HID

# GAP-LE

## 广告

## 扫描

## 连接

# SMP

# GATT

## GATT Client

## GATT Server

# LE Audio

# Mesh
