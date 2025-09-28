# Introduction to the Network Protocol Stack

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/network/protocol_stack/NetProtocolStackIntro.md) \]

## I. Overview

### 1. Functions of the OS Network Protocol Stack

The OS network protocol stack mainly handles Layer 2, Layer 3, and Layer 4 protocols during network communication. Below is a comparison between the OSI seven-layer network model and the TCP/IP four-layer model, along with the corresponding network protocols used in network communications:

<table>
  <thead>
    <tr>
      <th>TCP/IP 4-Layer Model</th>
      <th>OSI 7-Layer Model</th>
      <th>Protocol Examples</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="3"><b>Application Layer</b></td>
      <td>Application Layer</td>
      <td>HTTP, FTP, SMTP, DNS, Telnet</td>
    </tr>
    <tr>
      <td>Presentation Layer</td>
      <td>JPEG, ASCII, TLS, SSL</td>
    </tr>
    <tr>
      <td>Session Layer</td>
      <td>RPC, NetBIOS</td>
    </tr>
    <tr>
      <td><b>Transport Layer</b></td>
      <td>Transport Layer</td>
      <td>TCP, UDP</td>
    </tr>
    <tr>
      <td><b>Network Layer</b></td>
      <td>Network Layer</td>
      <td>IP, ICMP, ARP, RARP</td>
    </tr>
    <tr>
      <td rowspan="2"><b>Network Interface Layer</b></td>
      <td>Data Link Layer</td>
      <td>Ethernet, PPP, SLIP</td>
    </tr>
    <tr>
      <td>Physical Layer</td>
      <td>Cables, Hubs, Repeaters</td>
    </tr>
  </tbody>
</table>

### 2. Capabilities of the openvela Network Protocol Stack

The openvela network protocol stack provides full-stack network communication capabilities from the driver level to user space, supporting a variety of protocols and tools. The following diagram illustrates its core functionalities:

### 3. User Space Interface

The Socket interface is the core of network communication. The openvela network protocol stack supports the standard POSIX Socket interface for efficient user space network communication. Below are some common Socket interface functions and their descriptions:

```C
int socket(int domain, int type, int protocol);
int socketpair(int domain, int type, int protocol, int sv[2]);
int bind(int sockfd, FAR const struct sockaddr *addr, socklen_t addrlen);
int connect(int sockfd, FAR const struct sockaddr *addr, socklen_t addrlen);

int listen(int sockfd, int backlog);
int accept(int sockfd, FAR struct sockaddr *addr, FAR socklen_t *addrlen);
int accept4(int sockfd, FAR struct sockaddr *addr, FAR socklen_t *addrlen,
            int flags);

ssize_t send(int sockfd, FAR const void *buf, size_t len, int flags);
ssize_t sendto(int sockfd, FAR const void *buf, size_t len, int flags,
               FAR const struct sockaddr *to, socklen_t tolen);

ssize_t recv(int sockfd, FAR void *buf, size_t len, int flags);
ssize_t recvfrom(int sockfd, FAR void *buf, size_t len, int flags,
                 FAR struct sockaddr *from, FAR socklen_t *fromlen);

int shutdown(int sockfd, int how);

int ioctl(int fd, int req, ...);

int setsockopt(int sockfd, int level, int option,
               FAR const void *value, socklen_t value_len);
int getsockopt(int sockfd, int level, int option,
               FAR void *value, FAR socklen_t *value_len);

int getsockname(int sockfd, FAR struct sockaddr *addr,
                FAR socklen_t *addrlen);
int getpeername(int sockfd, FAR struct sockaddr *addr,
                FAR socklen_t *addrlen);

ssize_t recvmsg(int sockfd, FAR struct msghdr *msg, int flags);
ssize_t sendmsg(int sockfd, FAR struct msghdr *msg, int flags);

int poll(FAR struct pollfd *fds, nfds_t nfds, int timeout);
int select(int nfds, FAR fd_set *readfds, FAR fd_set *writefds,
           FAR fd_set *exceptfds, FAR struct timeval *timeout);
```

## II. Basic Capabilities of the Protocol Stack

The openvela network protocol stack supports multiple network and transport layer protocols, including IPv4, IPv6, TCP, UDP, and ICMP, providing developers with comprehensive network communication capabilities. Below is a brief introduction to the functionalities of each protocol.

### 1. IPv4 / IPv6 Capabilities

The openvela network protocol stack supports both IPv4 and IPv6 protocols and offers the following extended features:

- ARP and NDP Protocols.
- DHCP / DHCPv6: Supports both DHCP client and server functionalities.
- Fragmentation Support: Supports fragmentation in both IPv4 and IPv6.
- 6LoWPAN: Supports the Low-Power Wireless Personal Area Network protocol.
- Multiple Address Support: A single network interface can be configured with multiple IPv6 addresses.
- IPv6 Auto-Configuration: Supports the reception and transmission of IPv6 Router Advertisements, allowing automatic configuration of its own IPv6 address as well as providing prefixes for other devices.

### 2. TCP Capabilities

The openvela network protocol stack supports the TCP protocol on both IPv4 and IPv6, and provides the following functionalities:

- Standard Socket Interface Support:

    - Provides standard POSIX Socket interfaces such as `bind`, `listen`, `connect`, `accept`, `send`, `recv`, `shutdown`, `poll`, etc.

- TCP Feature Support:

    - Backlog: Supports connection queue management.
    - Keepalive: Supports the TCP keepalive mechanism.
    - SACK / Delayed ACK: Supports Selective Acknowledgment (SACK) and Delayed ACK.
    - Send / Recv Buffer Management: Manages transmit and receive buffers.
    - Fast Retransmit: Implements fast retransmission mechanisms.
    - Zero Window Probe: Supports zero window probe functionality.
    - Congestion Control Algorithms: Supports the New Reno congestion control algorithm.
    - RTT Estimation: Provides round-trip time (RTT) estimation functionality.

### 3. UDP / ICMP / ICMPv6 Capabilities

In addition to the basic network communication capabilities, the openvela network stack also provides a series of advanced features for multi-core architectures, complex routing scenarios, and high-performance network requirements. The following is a detailed introduction to the advanced capabilities.

#### UDP Capabilities

- Standard Socket Interface Support:

    - Provides standard POSIX Socket interfaces such as bind, listen, connect, send, recv, poll, etc.

- UDP Feature Support:

    - Receive Buffer: Manages the receive buffer.
    - Multicast & Broadcast: Supports multicast and broadcast communications.
    - Bind to Device: Supports binding to a specific device.

#### ICMP / ICMPv6 Capabilities

- ICMP Message Support:

    - Sends ICMP and ICMPv6 messages when appropriate, for example:
        - Responds to ECHO requests (e.g., ping).
        - Sends responses when the packet’s Time-To-Live (TTL) expires.
        - Sends error messages for unreachable addresses or ports.

## III. Advanced Capabilities of the Protocol Stack

In addition to the basic network communication capabilities, the openvela network protocol stack provides a series of advanced features suitable for multi-core architectures, complex routing scenarios, and high-performance network requirements. The details are described below.

### 1. Usrsock Proxy Capability

Rpmsg Usrsock is a proxy mechanism implemented by openvela that transfers user space socket operations via methods such as RPMsg to be executed on the server side. It is divided into two parts—the client side and the server side—which are responsible for request forwarding and actual processing, respectively. The following diagram illustrates the concept:

#### Working Principle

- Usrsock Client Side:

    - All socket operations (e.g., `send`, `recv`, etc.) performed by user space applications are forwarded via proxy mechanisms (such as RPMsg) to the server side.

- Usrsock Server Side:

    - Responsible for executing the actual socket operations.
    - Applies the socket parameters received from the client side to the network protocol stack on the server side to complete the operations.

#### Application Scenarios

- Multi-Core openvela Products:

    - In multi-core devices, RPMsg-based Usrsock enables only one openvela instance to run the network protocol stack, while other cores access network functionality through the proxy.

- Internet Connectivity in Emulators:

    - In an emulator environment, direct system calls implement Usrsock, effectively allowing openvela internal applications to use the host Linux socket interface.

### 2. Routing and Forwarding Capability

When a device is equipped with multiple network interfaces, the openvela network protocol stack provides robust routing and forwarding features to support complex network topologies and efficient packet processing.

- Basic Forwarding Capability:

    - When the device receives an IP packet with a destination address that does not belong to it, the packet is forwarded between interfaces.
    - During forwarding, the packet’s TTL (Time-To-Live) is decremented by 1, and the packet is sent out from another interface.

- Routing Table and Longest Prefix Matching:

    - Supports route selection based on routing tables using the longest prefix matching algorithm.

- Error Handling and ICMP Messages:

    - Sends ICMP and ICMPv6 messages when errors occur, such as:

        - TTL Expiry: Sends an error message when the packet’s TTL reaches 0.
        - Destination Unreachable: Sends an error message when the target address is unreachable.

- IPv4/IPv6 NAT Support:

    - Provides NAT (Network Address Translation) functionality similar to Linux iptables, supporting both IPv4 and IPv6.

### 3. Other Advanced Capabilities

The openvela network protocol stack also supports the following advanced features to meet high-performance and complex network demands:

- Zero-Copy:

    - Supports zero-copy for fixed-length buffers (IOB Offloading).
    - Will soon support zero-copy for variable-length buffers to further enhance performance.

- GRO/GSO:

    - GRO (Generic Receive Offload): Reduces protocol stack processing overhead at the receiver.
    - GSO (Generic Segmentation Offload): Reduces the segmentation processing overhead at the transmitter.

- Firewall:

    - Provides basic firewall functionalities for filtering and managing network traffic.

- VLAN Support:

    - Supports Virtual Local Area Network (VLAN) features suitable for complex network topologies.

## IV. Driver Interface

Netdev is the driver interface layer of the openvela network protocol stack and is responsible for connecting the network protocol stack with the underlying hardware drivers. Through standardized interfaces, Netdev offers flexible network device management capabilities, including device registration, data transmission and reception, and wireless network operations.

```C
typedef struct iob_s netpkt_t;

struct netdev_ops_s
{
  int (*ifup)(FAR struct netdev_lowerhalf_s *dev);
  int (*ifdown)(FAR struct netdev_lowerhalf_s *dev);

  int (*transmit)(FAR struct netdev_lowerhalf_s *dev, FAR netpkt_t *pkt);
  FAR netpkt_t *(*receive)(FAR struct netdev_lowerhalf_s *dev);

  int (*addmac)(FAR struct netdev_lowerhalf_s *dev, FAR const uint8_t *mac);
  int (*rmmac)(FAR struct netdev_lowerhalf_s *dev, FAR const uint8_t *mac);
  int (*ioctl)(FAR struct netdev_lowerhalf_s *dev, int cmd, unsigned long arg);
}

typedef int (*iw_handler_rw)(FAR struct netdev_lowerhalf_s *dev,
                             FAR struct iwreq *iwr, bool set);
typedef int (*iw_handler_ro)(FAR struct netdev_lowerhalf_s *dev,
                             FAR struct iwreq *iwr);

struct wireless_ops_s
{
  int (*connect)(FAR struct netdev_lowerhalf_s *dev);
  int (*disconnect)(FAR struct netdev_lowerhalf_s *dev);

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

struct netdev_lowerhalf_s
{
  FAR const struct netdev_ops_s *ops;
  FAR const struct wireless_ops_s *iw_ops;
  int quota[NETPKT_TYPENUM]; /* Max # of buffer held by driver */

  ...
};

int netdev_lower_register(FAR struct netdev_lowerhalf_s *dev,
                          enum net_lltype_e lltype);
int netdev_lower_unregister(FAR struct netdev_lowerhalf_s *dev);
int netdev_lower_carrier_on(FAR struct netdev_lowerhalf_s *dev);
int netdev_lower_carrier_off(FAR struct netdev_lowerhalf_s *dev);

void netdev_lower_rxready(FAR struct netdev_lowerhalf_s *dev);
void netdev_lower_txdone(FAR struct netdev_lowerhalf_s *dev);
```

## V. Special Network Card Support

The openvela network protocol stack supports various special network cards suitable for virtualization and embedded scenarios. The following special network card types are supported:

- RNDIS (Remote Network Driver Interface Specification).
- CDCNCM (USB Communication Device Class – Network Control Model).
- CDCMBIM (USB Communication Device Class – Multi-Broadcast Interface Model).
- SLIP (Serial Line IP).
- TUN (Virtual Network Device).
- VirtIO-Net (Virtualization Network Device).

