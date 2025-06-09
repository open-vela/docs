# 功耗问题

<a id="方法：观察是否进入Sniff模式"></a>

## 一、观察是否进入Sniff模式

正常情况下，可以通过蓝牙service log、协议栈的syslog、snoop log及空口log观察设备是否进入Sniff模式

### 1、通过蓝牙service log观察设备进入Sniff模式

```text
[20240906_11:33:55_242]#[01/01 01:19:13] [126] [ DEBUG] [ap] [392][pm_mgr]: pm_request_sniff, peer_addr:XX:XX:XX:D7:B4:85, max:800, min:400, attempt:4, timeout:1

[20240906_11:33:55_302]#[01/01 01:19:13] [126] [ DEBUG] [ap] [784][pm_mgr]: bt_pm_remote_link_mode_changed, addr:XX:XX:XX:D7:B4:85, mode:1, sniff_interval:800
```

### 2、通过协议栈syslog观察设备进入Sniff模式

```text
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap] ---->[HCI][Cbk][Reg:1][0x60ba2b51]
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [OP][Sniff_Mode]
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap] 
[20240906_11:33:55_242]#------>FSM Func Start<------
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap] ---->[HCI][CMDN][P:0,$:1][+Sniff_Mode]
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap] ---->[HCI][*Send][AID:0,PLen:10][Sniff_Mode]
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [connection_handle:2050 | 02,08]
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [sniff_max_interval:0x320 * 0.625 = 500.00ms | 20,03]
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [sniff_min_interval:0x190 * 0.625 = 250.00ms | 90,01]
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [sniff_attempt:0x4 * 1.250 = 5.00ms | 04,00]
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [sniff_timeout:0x1 * 1.250 = 1.25ms | 01,00]
[20240906_11:33:55_242]#[01/01 01:19:13] [200] [ DEBUG] [ap] [HCI][*Send][Command]: 4+10=14
[20240906_11:33:55_252]#[01/01 01:19:13] [200] [ DEBUG] [ap] 0000: 01 03 08 0A 02 08 20 03 90 01 04 00 01 00         ...... .......  
[20240906_11:33:55_262]#[01/01 01:19:13] [200] [ DEBUG] [ap] clk enable ret 1
[20240906_11:33:55_262]#[01/01 01:19:13] [200] [ DEBUG] [ap] clk_enable
[20240906_11:33:55_262]#[01/01 01:19:13] [126] [ DEBUG] [ap] [HCI][*Recv][Event]: 3+4=7
[20240906_11:33:55_262]#[01/01 01:19:13] [126] [ DEBUG] [ap] 0000: 04 0F 04 00 01 03 08                              .......         
[20240906_11:33:55_262]#[01/01 01:19:13] [200] [ DEBUG] [ap] 
[20240906_11:33:55_262]#------>FSM Func Start<------
[20240906_11:33:55_262]#[01/01 01:19:13] [200] [ DEBUG] [ap] ---->[HCI][*Recv][AID:0,PLen:4][Command_Status]
[20240906_11:33:55_262]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [status:OK | 00]
[20240906_11:33:55_262]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [num_hci_command_packets:01 | 01]
[20240906_11:33:55_272]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [command_opcode:Sniff_Mode]
[20240906_11:33:55_282]#[01/01 01:19:13] [126] [ DEBUG] [ap] [HCI][*Recv][Event]: 3+6=9
[20240906_11:33:55_282]#[01/01 01:19:13] [126] [ DEBUG] [ap] 0000: 04 14 06 00 02 08 02 20 03                        ....... .       
[20240906_11:33:55_282]#[01/01 01:19:13] [200] [ DEBUG] [ap] 
[20240906_11:33:55_282]#------>FSM Func Start<------
[20240906_11:33:55_282]#[01/01 01:19:13] [200] [ DEBUG] [ap] ---->[HCI][*Recv][AID:0,PLen:6][Mode_Change]
[20240906_11:33:55_282]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [status:OK | 00]
[20240906_11:33:55_292]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [connection_handle:2050 | 02,08]
[20240906_11:33:55_292]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [current_mode:Sniff | 02]
[20240906_11:33:55_292]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [interval:0x320 * 0.625 = 500.00ms | 20,03]
[20240906_11:33:55_292]#[01/01 01:19:13] [200] [ DEBUG] [ap] ---->[HCI][CMDN][P:1,$:1][-Sniff_Mode][status:OK | 00]
[20240906_11:33:55_292]#[01/01 01:19:13] [200] [ DEBUG] [ap]      [Mode_Change][T:0x61c81320]
```

### 3、通过snoop log观察设备进入Sniff模式

### 4、通过空口log观察设备进入Sniff

<a id="方法：观察是否退出Sniff模式"></a>

## 二、观察是否退出Sniff模式

正常情况下，可以通过蓝牙service log、协议栈的syslog、snoop log及空口log观察设备是否退出Sniff模式

### 1、通过蓝牙service log观察设备退出Sniff模式

```text
[20240909_15:56:55_246]#[09/09 07:56:52] [26] [ DEBUG] [ap] [420][pm_mgr]: pm_request_active, peer_addr:XX:XX:XX:XX:B4:85

[20240909_15:56:55_338]#[09/09 07:56:02] [26] [ DEBUG] [ap] [784][pm_mgr]: bt_pm_remote_link_mode_changed, addr:XX:XX:XX:XX:B4:85, mode:0, sniff_interval:0
```

### 2、通过协议栈syslog观察设备退出Sniff模式

```text
[20240913_11:54:44_358]#[09/13 03:54:43] [14] [cp] 
[20240913_11:54:44_358]#------>FSM Func Start<------
[20240913_11:54:44_358]#[09/13 03:54:43] [14] [cp] ---->[HCI][Cbk][Reg:1][0x14102341]
[20240913_11:54:44_358]#[09/13 03:54:43] [14] [cp]      [OP][Exit_Sniff_Mode]
[20240913_11:54:44_358]#[09/13 03:54:43] [14] [cp] 
[20240913_11:54:44_358]#------>FSM Func Start<------
[20240913_11:54:44_362]#[09/13 03:54:43] [14] [cp] ---->[HCI][CMDN][P:0,$:1][+Exit_Sniff_Mode]
[20240913_11:54:44_366]#[09/13 03:54:43] [14] [cp] ---->[HCI][*Send][AID:0,PLen:2][Exit_Sniff_Mode]
[20240913_11:54:44_366]#[09/13 03:54:43] [14] [cp]      [connection_handle:0129 | 81,00]
[20240913_11:54:44_366]#[09/13 03:54:43] [14] [cp] [HCI][*Send][Command]: 4+2=6
[20240913_11:54:44_366]#[09/13 03:54:43] [14] [cp] 0000: 01 04 08 02 81 00                                 ......          
[20240913_11:54:44_366]#[09/13 03:54:44] [14] [cp] 
[20240913_11:54:44_366]#------>FSM Func Start<------
[20240913_11:54:44_366]#[09/13 03:54:44] [14] [cp] ---->[HCI][CMDN][P:1,$:0][+Exit_Sniff_Mode]
[20240913_11:54:44_370]#[09/13 03:54:44] [14] [cp] ---->[HCI][TXQOS][0x430081|L|62][Tail][NewIn][Num:0]
[20240913_11:54:44_370]#[09/13 03:54:44] [10] [cp] [HCI][*Recv][Event]: 3+4=7
[20240913_11:54:44_370]#[09/13 03:54:44] [10] [cp] 0000: 04 0F 04 00 05 04 08                              .......         
[20240913_11:54:44_374]#[09/13 03:54:44] [14] [cp] 
[20240913_11:54:44_374]#------>FSM Func Start<------
[20240913_11:54:44_374]#[09/13 03:54:44] [14] [cp] ---->[HCI][*Recv][AID:0,PLen:4][Command_Status]
[20240913_11:54:44_374]#[09/13 03:54:44] [14] [cp]      [status:OK | 00]
[20240913_11:54:44_378]#[09/13 03:54:44] [14] [cp]      [num_hci_command_packets:05 | 05]
[20240913_11:54:44_386]#[09/13 03:54:44] [14] [cp]      [command_opcode:Exit_Sniff_Mode]

[20240913_11:54:44_739]#[09/13 03:54:44] [10] [cp] [HCI][*Recv][Event]: 3+6=9
[20240913_11:54:44_739]#[09/13 03:54:44] [10] [cp] 0000: 04 14 06 00 81 00 00 00 00                        .........       
[20240913_11:54:44_743]#[09/13 03:54:44] [14] [cp] 
[20240913_11:54:44_747]#------>FSM Func Start<------
[20240913_11:54:44_747]#[09/13 03:54:44] [14] [cp] ---->[HCI][*Recv][AID:0,PLen:6][Mode_Change]
[20240913_11:54:44_747]#[09/13 03:54:44] [14] [cp]      [status:OK | 00]
[20240913_11:54:44_747]#[09/13 03:54:44] [14] [cp]      [connection_handle:0129 | 81,00]
[20240913_11:54:44_747]#[09/13 03:54:44] [14] [cp]      [current_mode:Active | 00]
[20240913_11:54:44_747]#[09/13 03:54:44] [14] [cp]      [interval:0x0 * 0.625 = 0.00ms | 00,00]
[20240913_11:54:44_747]#[09/13 03:54:44] [14] [cp] ---->[HCI][CMDN][P:2,$:1][Pend:Exit_Sniff_Mode][-Exit_Sniff_Mode][status:OK | 00]
[20240913_11:54:44_747]#[09/13 03:54:44] [14] [cp]      [Mode_Change][T:0x2059f160]   
```

### 3、通过snoop log观察设备退出Sniff模式

### 4、通过空口log观察设备退出Sniff

<a id="方法：查找当前Profile工作状态的Sniff允许参数"></a>

## 三、查找当前Profile工作状态的Sniff允许参数

Vela支持如下各Profile的Sniff场景管理，其中每个Profile对应8种状态，每个状态对应的Sniff参数允许模式如下定义。

```c
static const bt_pm_spec_table_t g_pm_spec[] = {
    /* HF AG: 0(BT_PM_SPEC_INDEX_0) */
    { (BT_PM_SNIFF), /* allow sniff */
        (0), /* the SSR entry */
        {
            { BT_PM_SNIFF, 7000 }, /* conn open */
            { BT_PM_NO_PREF, 0 }, /* conn close  */
            { BT_PM_NO_ACTION, 0 }, /* app open */
            { BT_PM_NO_ACTION, 0 }, /* app close */
            { BT_PM_SNIFF3, 7000 }, /* sco open */
            { BT_PM_SNIFF, 7000 }, /* sco close */
            { BT_PM_SNIFF, 7000 }, /* idle */
            { BT_PM_ACTIVE, 0 } /* busy */
        } },

    /* AV: 1(BT_PM_SPEC_INDEX_1) */
    { (BT_PM_SNIFF), /* allow sniff */
        (0), /* the SSR entry */
        {
            { BT_PM_SNIFF, 7000 }, /* conn open */
            { BT_PM_NO_PREF, 0 }, /* conn close */
            { BT_PM_NO_ACTION, 0 }, /* app open */
            { BT_PM_NO_ACTION, 0 }, /* app close */
            { BT_PM_NO_ACTION, 0 }, /* sco open */
            { BT_PM_NO_ACTION, 0 }, /* sco close */
            { BT_PM_SNIFF, 7000 }, /* idle */
            { BT_PM_ACTIVE, 0 } /* busy */
        } },

    /* SPP: 2(BT_PM_SPEC_INDEX_2) */
    { (BT_PM_SNIFF), /* allow sniff */
        (0), /* the SSR entry */
        {
            { BT_PM_ACTIVE, 0 }, /* conn open */
            { BT_PM_NO_PREF, 0 }, /* conn close */
            { BT_PM_ACTIVE, 0 }, /* app open */
            { BT_PM_NO_ACTION, 0 }, /* app close */
            { BT_PM_NO_ACTION, 0 }, /* sco open */
            { BT_PM_NO_ACTION, 0 }, /* sco close */
            { BT_PM_SNIFF, 1000 }, /* idle */
            { BT_PM_ACTIVE, 0 } /* busy */
        } },

    /* PAN: 3(BT_PM_SPEC_INDEX_3) */
    { (BT_PM_SNIFF), /* allow sniff */
        (0), /* the SSR entry */
        {
            { BT_PM_ACTIVE, 0 }, /* conn open */
            { BT_PM_NO_PREF, 0 }, /* conn close */
            { BT_PM_ACTIVE, 0 }, /* app open */
            { BT_PM_NO_ACTION, 0 }, /* app close */
            { BT_PM_NO_ACTION, 0 }, /* sco open */
            { BT_PM_NO_ACTION, 0 }, /* sco close */
            { BT_PM_SNIFF, 5000 }, /* idle */
            { BT_PM_ACTIVE, 0 } /* busy */
        } },

    /* HID: 4(BT_PM_SPEC_INDEX_4) */
    { (BT_PM_SNIFF), /* allow sniff */
        (0), /* the SSR entry */
        {
            { BT_PM_SNIFF, 5000 }, /* conn open */
            { BT_PM_NO_PREF, 0 }, /* conn close */
            { BT_PM_NO_ACTION, 0 }, /* app open */
            { BT_PM_NO_ACTION, 0 }, /* app close */
            { BT_PM_NO_ACTION, 0 }, /* sco open */
            { BT_PM_NO_ACTION, 0 }, /* sco close */
            { BT_PM_SNIFF2, 5000 }, /* idle */
            { BT_PM_SNIFF4, 200 } /* busy */
        } },
};
```

Vela一共定义7种Sniff模式，各种Sniff mode对应的Interval、Attempt和Timeout参数如下表，其中mode越高表示Sniff间隔越短。

```c
#ifndef BT_PM_SNIFF_MAX
#define BT_PM_SNIFF_MAX 800
#define BT_PM_SNIFF_MIN 400
#define BT_PM_SNIFF_ATTEMPT 4
#define BT_PM_SNIFF_TIMEOUT 1
#endif

#ifndef BT_PM_SNIFF1_MAX
#define BT_PM_SNIFF1_MAX 400
#define BT_PM_SNIFF1_MIN 200
#define BT_PM_SNIFF1_ATTEMPT 4
#define BT_PM_SNIFF1_TIMEOUT 1
#endif

#ifndef BT_PM_SNIFF2_MAX
#define BT_PM_SNIFF2_MAX 54
#define BT_PM_SNIFF2_MIN 30
#define BT_PM_SNIFF2_ATTEMPT 4
#define BT_PM_SNIFF2_TIMEOUT 1
#endif

#ifndef BT_PM_SNIFF3_MAX
#define BT_PM_SNIFF3_MAX 150
#define BT_PM_SNIFF3_MIN 50
#define BT_PM_SNIFF3_ATTEMPT 4
#define BT_PM_SNIFF3_TIMEOUT 1
#endif

#ifndef BT_PM_SNIFF4_MAX
#define BT_PM_SNIFF4_MAX 18
#define BT_PM_SNIFF4_MIN 10
#define BT_PM_SNIFF4_ATTEMPT 4
#define BT_PM_SNIFF4_TIMEOUT 1
#endif

#ifndef BT_PM_SNIFF5_MAX
#define BT_PM_SNIFF5_MAX 36
#define BT_PM_SNIFF5_MIN 30
#define BT_PM_SNIFF5_ATTEMPT 2
#define BT_PM_SNIFF5_TIMEOUT 0
#endif

#ifndef BT_PM_SNIFF6_MAX
#define BT_PM_SNIFF6_MAX 18
#define BT_PM_SNIFF6_MIN 14
#define BT_PM_SNIFF6_ATTEMPT 1
#define BT_PM_SNIFF6_TIMEOUT 0
#endif
```

<a id="方法：对方优先请求进入Sniff优先级高于本地"></a>

## 四、对方优先请求进入Sniff优先级高于本地

本地和对方均可以主动发起请求进入Sniff模式，可以通过上述“分析方法：观察是否进入Sniff模式”章节，若是对方优先调度请求进入Sniff，当Controller协商通过时，设备Sniff参数以对方发起协商为准。

```c
void bt_pm_remote_link_mode_changed(bt_address_t* addr, uint8_t mode, uint16_t sniff_interval)
{
    bt_pm_device_t* device;
    bt_pm_manager_t* manager = &g_pm_manager;

    BT_LOGD("%s, addr:%s, mode:%d, sniff_interval:%" PRId16, __func__, bt_addr_str(addr), mode, sniff_interval);
    
    ......
   
    switch (mode) {
    case BT_LINK_MODE_ACTIVE: {
        pm_stop_timer(addr);
        pm_mode_request(addr, BT_PM_RESTART, manager->last_profile_id);
    } break;
    case BT_LINK_MODE_SNIFF: { //对方进入sniff，则暂停本地Sniff调度
        pm_stop_timer(addr); 
    } break;
    default:
        break;
    }
}
```

<a id="方法：对方优先请求退出Sniff优先级低于本地"></a>

## 五、对方优先请求退出Sniff优先级低于本地

本地和对方均可以主动发起请求进入Sniff模式，可以通过上述“分析方法：观察是否退出Sniff模式”章节，若是对方优先调度请求退出Sniff，当Controller协商通过，设备进入Active模式后，重新请求调度本地Sniff状态。

```c
void bt_pm_remote_link_mode_changed(bt_address_t* addr, uint8_t mode, uint16_t sniff_interval)
{
    bt_pm_device_t* device;
    bt_pm_manager_t* manager = &g_pm_manager;

    BT_LOGD("%s, addr:%s, mode:%d, sniff_interval:%" PRId16, __func__, bt_addr_str(addr), mode, sniff_interval);
    
    ......
   
    switch (mode) {
    case BT_LINK_MODE_ACTIVE: { //若是对方请求退出Sniff，则本地请求重新调度
        pm_stop_timer(addr);
        pm_mode_request(addr, BT_PM_RESTART, manager->last_profile_id);
    } break;
    case BT_LINK_MODE_SNIFF: {
        pm_stop_timer(addr); 
    } break;
    default:
        break;
    }
}
```

<a id="功耗典型问题"></a>

## 典型问题

<a id="问题-设备经典蓝牙连接设备功耗异常"></a>

## 问题一：设备经典蓝牙连接设备功耗异常
一般情况下，设备在连接状态下，若是设备未发送数据，会进入Sniff模式。若是设备正在发送数据，则会进入Active模式。设备功耗异常，我们需要确认是否在Sniff模式，以及Sniff参数是否符合预期。

Sniff间隔越大，功耗越低，但会导致设备响应变慢。反之，Sniff间隔越小，功耗越高，但会导致设备响应变快。因此，我们需要根据实际场景，选择合适的Sniff间隔。

第一步检查设备Sniff状态，确认是否进入Sniff模式。若是未进入Sniff模式，请按照如下步骤进一步分析。否则，进入第二步骤检查设备Sniff参数是否合理。
* [方法：观察是否进入Sniff模式](#方法：观察是否进入Sniff模式)
  * 若是设备未进入Sniff模式，请进一步确认当前是否正在发送数据，比如：听歌、SPP传数据等操作。
  * 否则，建议按照如下步骤进一步分析。

第二步检查设备Sniff参数是否合理。依据当前Profile工作状态，查找当前Profile工作状态的Sniff允许参数。
* [方法：查找当前Profile工作状态的Sniff允许参数](#方法：查找当前Profile工作状态的Sniff允许参数)
  * 若是Sniff参数异常，建议进一步确认，当前是否有其他Profile连接影响，比如在待机场景下，若是HID的处于连接状态，则Sniff优先级高于SPP的Sniff参数，导致待机功耗增加。
  * 否则,建议按照如下步骤进一步分析。

* [方法：对方优先请求进入Sniff优先级高于本地](#方法：对方优先请求进入Sniff优先级高于本地)
  * 若是对方请求进入Sniff，并且Sniff参数更严格，则会导致当前连接状态下，功耗异常。
  * 否则,建议按照如下步骤进一步分析。