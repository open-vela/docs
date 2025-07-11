# 网络驱动适配指南

\[ [English](../../../../../en/device_dev_guide/connection/network/driver/net_driver_guide.md) | 简体中文 \]

## 一、网络驱动简介

openvela 内置了一套轻量级的 **TCP/IP** **网络协议栈**，并提供了一套网络驱动框架。通过该框架，内置的 TCP/IP 协议栈可以与芯片驱动交互，实现网络数据包的收发。

在网络驱动架构中，openvela 提供了通用的 **上半部分实现（UpperHalf）**，厂商只需实现驱动的 **下半部分（LowerHalf）**，即可完成驱动适配工作，从而赋予 openvela 访问互联网的能力。

## 二、配置说明

openvela 使用 Kconfig 工具进行功能配置。以下是与网络相关的主要配置选项：

### 1、网络协议栈配置

根据需求启用所需的网络协议：

```Makefile
/* 网络协议栈配置相关，按需启用所需协议 */
CONFIG_NET
CONFIG_NET_TCP
CONFIG_NET_UDP
CONFIG_NET_ICMP
CONFIG_NET_IGMP
CONFIG_NET_IPv4
CONFIG_NET_IPv6
CONFIG_NET_MLD
CONFIG_NET_ROUTE
CONFIG_NET_ETHERNET
```

### 2、驱动相关配置

以下选项用于配置网络驱动功能：

```Makefile
/* Driver配置相关 */
CONFIG_NETDEVICES
CONFIG_NETDEV_IOCTL
CONFIG_NETDEV_WIRELESS_HANDLER
```

## 三、数据收发流程

### 1、发送流程

![img](./figures/001.svg)

### 2、接收流程

![img](./figures/002.svg)

## 四、驱动适配接口说明

本节介绍 openvela 网络驱动适配接口的设计与实现，主要基于 `nuttx/net/netdev_lowerhalf.h` 文件。通过这些接口，开发者可以实现网络设备的驱动适配工作。

### 1、驱动接口

#### 驱动接口定义

以下是网络设备操作接口的定义，包含设备启动、关闭、数据收发、MAC 地址管理等功能。

```C
struct netdev_ops_s
{
  CODE int (*ifup)(FAR struct netdev_lowerhalf_s *dev);
  CODE int (*ifdown)(FAR struct netdev_lowerhalf_s *dev);

  CODE int (*transmit)(FAR struct netdev_lowerhalf_s *dev, FAR netpkt_t *pkt);
  CODE FAR netpkt_t (*receive)(FAR struct netdev_lowerhalf_s *dev);

  CODE int (*addmac)(FAR struct netdev_lowerhalf_s *dev, FAR const uint8_t *mac);
  CODE int (*rmmac)(FAR struct netdev_lowerhalf_s *dev, FAR const uint8_t *mac);
  CODE int (*ioctl)(FAR struct netdev_lowerhalf_s *dev, int cmd, unsigned long arg);

  CODE void (*reclaim)(FAR struct netdev_lowerhalf_s *dev);
}
```

#### 无线网络操作接口

无线网络设备的操作接口定义如下，支持无线网络的连接、断开以及相关参数的读写操作。

```C
struct wireless_ops_s
{
  CODE int (*connect)(FAR struct netdev_lowerhalf_s *dev);
  CODE int (*disconnect)(FAR struct netdev_lowerhalf_s *dev);

  iw_handler_rw essid;
  iw_handler_rw bssid;
  iw_handler_rw passwd;
  iw_handler_rw mode;
  iw_handler_rw auth;
  iw_handler_rw freq;
  iw_handler_rw bitrate;
  iw_handler_rw txpower;
  iw_handler_rw country;
  iw_handler_rw sensitivity;
  iw_handler_rw scan;
  iw_handler_ro range;
};
```

#### 网络设备结构体

网络设备的核心结构体 `netdev_lowerhalf_s` 定义如下：

```C
struct netdev_lowerhalf_s
{
  FAR const struct netdev_ops_s *ops;
  FAR const struct wireless_ops_s *iw_ops;
  atomic_int quota[NETPKT_TYPENUM]; /* Max # of buffer held by driver */

  ...
};
```

#### 驱动适配 API

以下是网络设备适配的主要 API：

```C
int netdev_lower_register(FAR struct netdev_lowerhalf_s *dev,
                          enum net_lltype_e lltype);
int netdev_lower_unregister(FAR struct netdev_lowerhalf_s *dev);
void netdev_lower_carrier_on(FAR struct netdev_lowerhalf_s *dev);
void netdev_lower_carrier_off(FAR struct netdev_lowerhalf_s *dev);

void netdev_lower_rxready(FAR struct netdev_lowerhalf_s *dev);
void netdev_lower_txdone(FAR struct netdev_lowerhalf_s *dev);
```

#### 网络设备操作说明

以下是网络设备操作的 API 说明：

- `ifup()`：启动网络设备。
- `ifdown()`：关闭网络设备。
- `transmit()`：通知驱动可以发送数据包，驱动返回发送结果。
- `receive()`：从驱动获取接收到的数据包，驱动返回接收结果（报文）。
- `addmac()`（可选）：向网络设备添加接收组播的 MAC 地址。如果设备不涉及 MAC 地址过滤，可不实现。
- `rmmac()`（可选）：从网络设备移除接收组播的 MAC 地址。如果设备不涉及 MAC 地址过滤，可不实现。
- `ioctl()`（可选）：实现其他控制命令，主要用于无线网络相关命令（与 `wireless_ops_s` 二选一实现即可）。
- `reclaim()`（可选）：用于资源回收。当发送缓冲区（TX Quota）耗尽时，上层会调用该接口。主要用于辅助设备的轮询模式资源回收。如果设备能及时释放缓冲区并调用 `TX Done`，则无需实现。

### 2、NetPKT 接口

NetPKT 是 `transmit` 和 `receive` 接口与上层交换网络报文使用的数据结构。本节将介绍 NetPKT 的相关接口及其使用方法。

#### NetPKT Buffer 结构

![img](./figures/003.svg)

- reserved：保留字段，可能被驱动使用。
- base：Buffer 的起始地址。
- data：数据的起始地址。
- free：Buffer 的空闲部分。
- datalen：当前数据的长度。
- data end：Buffer 的结束地址。
- next：指向下一个 Buffer 的指针（用于链式结构）。

#### Buffer 接口

以下是与 NetPKT Buffer 操作相关的接口定义：

```C
#define NETPKT_BUFLEN 1518 /* 不同产品上配置不同，128 ~ 1600 均有可能 */

enum netpkt_type_e
{
  NETPKT_TX,
  NETPKT_RX,
  NETPKT_TYPENUM
};

FAR netpkt_t *netpkt_alloc(FAR struct netdev_lowerhalf_s *dev,
                           enum netpkt_type_e type);
void netpkt_free(FAR struct netdev_lowerhalf_s *dev, FAR netpkt_t *pkt,
                 enum netpkt_type_e type);

/* 与pkt buffer互相copy数据，任何场景可用，无需关心内部buffer结构 */
int netpkt_copyin(FAR struct netdev_lowerhalf_s *dev, FAR netpkt_t *pkt,
                  FAR const uint8_t *src, unsigned int len, int offset);
int netpkt_copyout(FAR struct netdev_lowerhalf_s *dev, FAR uint8_t *dest,
                   FAR const netpkt_t *pkt, unsigned int len, int offset);

/* 直接获取buffer中的地址，直接操作单个连续buffer（用来减少一次copy）时使用 */
FAR uint8_t *netpkt_getdata(FAR struct netdev_lowerhalf_s *dev,
                            FAR netpkt_t *pkt);
FAR uint8_t *netpkt_getbase(FAR netpkt_t *pkt);

/* 当前data长度 */
void netpkt_setdatalen(FAR struct netdev_lowerhalf_s *dev,
                       FAR netpkt_t *pkt, unsigned int len);
unsigned int netpkt_getdatalen(FAR struct netdev_lowerhalf_s *dev,
                               FAR netpkt_t *pkt);

/* 重设data起始点 */
void netpkt_reset_reserved(FAR struct netdev_lowerhalf_s *dev,
                           FAR netpkt_t *pkt, unsigned int len);
/* 判断是否连续（数据在一个还是多个buffer里） */
bool netpkt_is_fragmented(FAR netpkt_t *pkt);
```

#### TX Buffer 布局

在 openvela 的网络驱动中，TX Buffer（Transmit Buffer，发送缓冲区）用于存储即将发送的数据。以下是 TX Buffer 的布局结构及相关说明。

![img](./figures/004.svg)

以下是 TX Buffer 的布局结构：

- reserved：保留字段，可能被驱动使用。
- tx data：发送数据的起始地址。
- base：Buffer 的起始地址。
- data：数据的起始地址。
- free：Buffer 的空闲部分。
- datalen：当前数据的长度。
- data end：Buffer 的结束地址。

说明：`TX_RESERVED = LL_GUARDSIZE - LL_HDRLEN`

#### RX Buffer 布局

在 openvela 的网络驱动中，RX Buffer（Receive Buffer，接收缓冲区）用于存储接收到的数据。以下是 RX Buffer 的布局结构及相关说明。

![img](./figures/005.svg)

以下是 RX Buffer 的布局结构：

- rx head：接收数据的头部信息。
- rx data：接收数据的起始地址。
- base：Buffer 的起始地址。
- data：数据的起始地址。
- free：Buffer 的空闲部分。
- datalen：当前数据的长度。
- data end：Buffer 的结束地址。
- reserved：保留字段。

### 3、其他接口

- `wdog`：

    - 内核实现的定时操作机制，可用于定时回调某函数。例如，定时任务的执行。
    - 参考文档：[System Time and Clock — NuttX latest documentation (apache.org)](https://nuttx.apache.org/docs/latest/reference/os/time_clock.html#watchdog-timer-interfaces)

- `work_queue`： 内核利用独立线程实现的异步执行机制，与 Linux 的工作队列类似，可用于任务的异步处理。例如：

    - 网络数据包的收发处理。
    - 中断的下半部处理。
    - 参考文档：[工作队列](../../../kernel/IPC/work_queue.md)

- `ninfo`，`nwarn`，`nerr`： 用于打印不同等级的日志（Log），便于调试网络模块。 打开网络模块的日志功能需要启用以下配置选项：

    ```Makefile
    CONFIG_DEBUG_NET
    CONFIG_DEBUG_NET_ERROR
    CONFIG_DEBUG_WARN
    CONFIG_DEBUG_NET_WARN
    CONFIG_DEBUG_INFO
    CONFIG_DEBUG_NET_INFO
    ```

## 五、驱动实现

本节介绍 Openvela 驱动实现的关键部分，包括驱动数据结构、网络数据包发送和接收的实现方法。示例代码基于 `arch/sim/src/sim/sim_netdriver.c`。

### 1、驱动数据结构

以下是驱动数据结构的定义和初始化方法：

```C
struct <chip>_priv_s
{
  /* This holds the information visible to the Vela network */
  struct netdev_lowerhalf_s dev;

  ...
};

static const struct netdev_ops_s g_ops =
{
  .ifup     = <chip>_ifup,
  .ifdown   = <chip>_ifdown,
  .transmit = <chip>_transmit,
  .receive  = <chip>_receive,
  .addmac   = <chip>_addmac,
  .rmmac    = <chip>_rmmac,
  .ioctl    = <chip>_ioctl,
  .reclaim  = <chip>_reclaim
};

/* Wi-Fi 驱动注册函数可以按照如下方式实现，<chip>指芯片名称
 * netdev_lower_register() 为vela提供的网络设备接口，用于注册网络设备驱动
 */

int <chip>_netdev_init(FAR struct <chip>_priv_s *priv)
{
    FAR struct netdev_lowerhalf_s *dev = &priv->dev;

    dev->ops = &g_ops;

    /* 当前驱动最多可以同时持有的buffer数
     * 发送：每当上层transmit交给驱动一个pkt时，相当于驱动持有了一个pkt，会减少tx配额。
     *   tx配额用完时，上层不会再调用transmit，驱动通过netpkt_free释放pkt后配额恢复，transmit继续
     * 接收：每当驱动通过netpkt_alloc获取pkt时，相当于驱动持有了一个pkt，会减少rx配额。
     *   rx配额用完后，netpkt_alloc会失败，通过receive接口向上层提交pkt即可恢复配额
     *   （可以通过调用netdev_lower_rxready触发receive）
     * 如果驱动对每个包都单独处理（使用后立即释放），可以设置为1
     */
    dev->quota[NETPKT_TX] = 1;
    dev->quota[NETPKT_RX] = 1;

    return netdev_lower_register(dev, NET_LL_ETHERNET);
}
```

### 2、网络数据包发送

#### 数据发送流程

1. 上半部分（Upper Half）：调用 `transmit` 接口发送数据包。
2. 下半部分（Lower Half）：驱动处理数据包并完成发送。
3. 发送完成通知：通过 `txdone` 通知上层发送完成。

![img](./figures/006.svg)

![img](./figures/007.svg)

#### 数据发送代码示例

```C
struct <chip>_txhead_s; /* 假定硬件在数据前需要一些头部 */

static int <chip>_transmit(FAR struct netdev_lowerhalf_s *dev, FAR netpkt_t *pkt)
{
  FAR struct <chip>_priv_s *priv = (FAR struct <chip>_priv_s *)dev;
  unsigned int len = netpkt_getdatalen(dev, pkt);
  
  if (netpkt_is_fragmented(pkt))
    {
      /* 内存不连续，需要用Copy出来的方式，直接向devbuf中copy L2数据 */
      uint8_t devbuf[1600];
      netpkt_copyout(dev, devbuf + sizeof(struct <chip>_txhead_s), pkt, len, 0);

      /* Transmit */
    }
  else
    {
      /* 内存连续情况下也可以直接使用buffer（可选，可以一直用上面的分支copy） */
      FAR uint8_t *databuf = netpkt_getdata(dev, pkt);
      FAR uint8_t *devbuf  = databuf - sizeof(struct <chip>_txhead_s);

      /* 检查是否越界 或 不符合硬件对齐要求（取决于网卡硬件要求，可省略） */
      if (devbuf < netpkt_getbase(pkt) || check_align(devbuf) != OK)
        {
          /* Fail or fallback to copyout */
        }

      /* Transmit */
    }

  return OK;
}

static void <chip>_txdone_interrupt(FAR struct <chip>_priv_s *priv)
{
  FAR struct netdev_lowerhalf_s *dev = &priv->dev;
  
  /* 驱动进行一些处理（如果需要） */
  
  /* 释放buffer并通知上层 */
  netpkt_free(dev, pkt, NETPKT_TX);
  netdev_lower_txdone(dev);
}
```

### 3、网络数据包接收

本节介绍网络数据包接收的实现流程，包括中断处理和数据包接收的具体实现。

![img](./figures/008.svg)

![img](./figures/009.svg)

```C
struct <chip>_rxhead_s;

/* 中断处理 */
static void <chip>_rxready_interrupt(FAR struct <chip>_priv_s *priv)
{
  FAR struct netdev_lowerhalf_s *dev = &priv->dev;
  netdev_lower_rxready(dev);
}

/* 数据包接收 */
static FAR netpkt_t *<chip>_receive(FAR struct netdev_lowerhalf_s *dev)
{
  /* 也可以提前申请pkt，提前收完数据再调用rxready并通过receive返回 */
  FAR netpkt_t *pkt = netpkt_alloc(dev, NETPKT_RX);

  if (pkt)
    {
#if NETPKT_BUFLEN < 15xx
      uint8_t devbuf[1600];

      /* 从src进行copy的方式，len对应L2的完整数据长度 */
      len = receive_data_into(devbuf);
      netpkt_copyin(dev, pkt, devbuf + sizeof(struct <chip>_rxhead_s), len, 0);
#else
      /* 直接写入pkt对应buffer的方式，len对应L2的完整数据长度 */
      len = receive_data_into(netpkt_getbase(pkt));
      netpkt_resetreserved(&priv->dev, pkt, sizeof(struct <chip>_rxhead_s));
      netpkt_setdatalen(&priv->dev, pkt, len);
#endif
    }

  return pkt;
}
```

### 4、WAPI 命令对接

WAPI（Wireless Application Protocol Interface） 命令依赖驱动的 `ioctl()` 接口实现。上层通过 WAPI 命令设置或获取 Wi-Fi 参数，控制 Wi-Fi 的行为。常用功能已被抽象为接口，在初始化时将其设置到 `dev->iw_ops` 即可。

#### WAPI 接口定义

```C
typedef int (*iw_handler_rw)(FAR struct netdev_lowerhalf_s *dev,
                             FAR struct iwreq *iwr, bool set);
typedef int (*iw_handler_ro)(FAR struct netdev_lowerhalf_s *dev,
                             FAR struct iwreq *iwr);

struct wireless_ops_s
{
  /* Connect / disconnect operation, should exist if essid or bssid exists */

  int (*connect)(FAR struct netdev_lowerhalf_s *dev);
  int (*disconnect)(FAR struct netdev_lowerhalf_s *dev);

  /* The following attributes need both set and get. */

  iw_handler_rw essid;
  iw_handler_rw bssid;
  iw_handler_rw passwd;
  iw_handler_rw mode;
  iw_handler_rw auth;
  iw_handler_rw freq;
  iw_handler_rw bitrate;
  iw_handler_rw txpower;
  iw_handler_rw country;
  iw_handler_rw sensitivity;

  /* Scan operation: start scan (set=1) / get scan result (set=0). */
  iw_handler_rw scan;

  /* Get-only attributes. */
  iw_handler_ro range;
};
```

#### WAPI 命令列表

驱动需要完成列表中所有 WAPI 命令的适配，完成上述接口后，WAPI 命令即可用于验证。

| **序号** | **Item**                 | **Usage**                                             | **Results**                                                                                                                |
| :------- | :----------------------- | :---------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| 1        | Show info                | `wapi show <ifname>`                                  | 打印当前 `ifname` 对应网卡的相关信息。                                                                                     |
| 2        | Scan                     | `wapi scan <ifname>`                                  | 打印扫描到的 AP 信息。                                                                                                     |
| 3        | Scan SSID                | `wapi scan <ifname> <essid>`                          | 打印指定 ESSID 的扫描信息。                                                                                                |
| 4        | Set channel or frequency | `wapi freq <ifname> <frequency/channel> <index/flag>` | 在多个相同 SSID 但频道（Channel）不同的场景下，指定频道。                                                                  |
| 5        | Set ESSID                | `wapi essid <ifname> <essid> <index/flag>`            | 设置 ESSID 并完成配网操作。<br>Flag 说明：<br>0：断开连接 <br>1：连接 <br>2：设置 ESSID，但暂不连接，待设置 BSSID 后连接。 |
| 6        | Set PSK                  | `wapi psk <ifname> <passphrase> <index/flag>`         | 设置 AP 密码及加密类型（开放网络无需此命令）。<br>Flag 说明：<br>1：WEP <br>2：TKIP <br>3：CCMP                            |
| 7        | Disconnect               | `wapi disconnect <ifname>`                            | 断开当前无线连接（STA/AP 模式），断开后网络通信将中断。                                                                    |
| 8        | Set mode (STA/AP)        | `wapi mode <ifname> <index/mode>`                     | 设置无线网络的工作模式。<br>Mode 说明：<br>2：STA 模式 <br>3：AP 模式                                                      |
| 9        | Set BSSID                | `wapi ap <ifname> <``MAC`` address>`                  | 指定 BSSID（基本服务集标识符）连接，防止路由 AP 修改 ESSID。                                                               |
| 10       | Save config to wapi.conf | `wapi save_config <ifname>`                           | 保存当前联网信息到 `/data/wapi.conf` 文件。                                                                                |
| 11       | Reconnect from wapi.conf | `wapi reconnect <ifname>`                             | 从 `/data/wapi.conf` 加载配置并重新联网。                                                                                  |
| 12       | Set Country Code         | `wapi country <ifname> <country code>`                | 设置国家码。                                                                                                               |
| 13       | Sensitivity(RSSI)        | `wapi sense <ifname>`                                 | 获取当前连接的信号强度（RSSI，接收信号强度指示）。                                                                         |

#### WAPI 命令使用示例

以下是 WAPI 命令的常见使用场景：

**AP 模式**

```Bash
wapi disconnect wlan0
ifup wlan0
wapi mode wlan0 3
wapi psk wlan0 <psk> 3
wapi essid wlan0 <ssid> 1
dhcpd wlan0 &
```

**STA 模式**

1. 通过 ESSID 连接：

    ```Bash
    ifup wlan0
    wapi mode wlan0 2
    wapi psk wlan0 <psk> 3
    wapi freq wlan0 1 1
    wapi essid wlan0 <ssid> 1
    renew wlan0
    ```

2. 通过 BSSID 连接：

    ```Bash
    ifup wlan0
    wapi mode wlan0 2
    wapi psk wlan0 <psk> 3
    wapi freq wlan0 1 1
    wapi ap wlan0 <bssid>
    renew wlan0
    ```

**配置保存与加载**

```Bash
wapi save_config wlan0   # 保存当前配置到 wapi.conf  
wapi reconnect wlan0     # 从 wapi.conf 加载配置并重新联网  
```

### 5、如何实现双网卡（AP/STA）

在 openvela 的 Wi-Fi 框架中，支持 AP（Access Point，接入点） 和 STA（Station，站点） 模式的共存。通过在驱动初始化阶段枚举两个网卡实例（如 `wlan0` 和 `wlan1`），可以分别固定为 STA 模式和 AP 模式。

#### 双网卡模式的功能说明

1. 双重功能支持： 模组既可以连接到环境中的无线热点（STA 模式），又可以允许外部无线终端接入（AP 模式）。
2. DHCP 功能支持：
    - 在 `wlan0` 接口上支持 DHCP Client 功能，从外部无线热点动态获取 IP 地址。
    - 在 `wlan1` 接口上支持 DHCP Server 功能，为外部无线终端动态分配 IP 地址。
3. 接口独立性： STA 和 AP 两个网络接口独立工作，互不干扰：
    - 一个接口的 UP/DOWN 状态发生变化时，另一个接口不受影响。
    - 一个接口上有 Wi-Fi 连接建立或释放时，另一个接口上的 Wi-Fi 连接不受影响。

#### 驱动实现注意事项

1. 弃用方法：
    - WAPI_ESSID_DELAY_ON 方式已经弃用。
2. 新的连接逻辑：
    - 设置 AP 的 MAC 地址时，如果没有设置过 ESSID（扩展服务集标识符），则不会触发任何动作。
    - 当设置 ESSID 时，会触发连接操作。
    - 如果之前已经设置过 ESSID，再设置 AP 的 MAC 地址时，也会触发新的连接。

#### 参考实现代码

以下是 Linux 中相关实现的参考代码链接：

- [wext-sme.c](https://elixir.bootlin.com/linux/latest/source/net/wireless/wext-sme.c#L43)（具体实现）
- [wext-compat.c](https://elixir.bootlin.com/linux/latest/source/net/wireless/wext-compat.c#L1463)（兼容性实现）

## 六、测试工具

openvela 提供了多个网络测试工具，用于驱动移植和网络吞吐量（Throughput）调试。以下是相关工具的说明和用法。

### 1、ping (Packet Internet Groper)

#### 功能说明

- ping 的作用：用于测试网络连通性和响应时间。
- 配置启用：通过配置 `CONFIG_NETUTILS_PING` 选项可以启用 ping 功能。

#### 使用方法

```Bash
Usage: ping [-c <count>] [-i <interval>] [-W <timeout>] [-s <size>] <hostname>
       ping -h

Where:
  <hostname> is either an IPv4 address or the name of the remote host
   that is requested the ICMPv4 ECHO reply.
  -c <count> determines the number of pings.  Default 10.
  -i <interval> is the default delay between pings (milliseconds).
    Default 1000.
  -W <timeout> is the timeout for wait response (milliseconds).
    Default 1000.
  -s <size> specifies the number of data bytes to be sent.  Default 56.
  -h shows this text and exits.

> r //此命令表示每个包携带1400字节数据以100毫秒的间隔给 www.xiaomi.com 发送50次，等待response的超时时间为200毫秒
```

### 2、iperf2/3

有关 iperf2 和 iperf3 的详细使用说明，请参考以下文档：

- [iperf2](../network_tools/iperf2.md)
- [iperf3](../network_tools/iperf3.md)

### 3、tcpdump

有关 tcpdump 的详细使用说明，请参考以下文档：

- [tcpdump](../network_tools/tcpdump.md)
