# 网络工具库（netlib）API

openvela 网络工具库（`netlib_*`）提供了一系列简化 BSD 套接字操作的辅助函数，涵盖 IPv4/IPv6 地址管理、路由、ARP、MAC 地址、MTU、防火墙（iptables/ip6tables）、网络连通性检查等。

头文件：`#include <netutils/netlib.h>`

## openvela 实现说明

- **定位**：在 BSD socket API 基础上的便利封装，隐藏 `ioctl` + `SIOCGIF*` 等底层细节
- **覆盖范围**：
    - IPv4/IPv6 地址、网关、子网掩码、DNS、路由
    - MAC 地址读写、接口上/下、MTU 设置
    - VLAN 管理、ARP 表操作
    - iptables/ip6tables 操作
    - 网络连通性检查（`ping` / HTTP / 接口可达性）
    - URL 解析工具
- **配置依赖**：需启用 `CONFIG_NETUTILS_NETLIB`，部分子接口另需对应模块配置（如 `CONFIG_NET_ARP`、`CONFIG_NET_IPv6` 等）
- **错误处理**：多数接口成功时返回 `0` 或 `OK`，失败时返回 `ERROR`（`-1`）并设置 `errno`

## 网络工具库

头文件：`#include <netutils/netlib.h>`

netlib 提供网络配置工具函数，包括接口地址设置、路由管理、ARP 操作等。

**IPv4 地址管理**

### netlib_get_ipv4addr

```c
int netlib_get_ipv4addr(const char *ifname, struct in_addr *addr);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 用于存储 IP 地址

### netlib_set_ipv4addr

```c
int netlib_set_ipv4addr(const char *ifname, const struct in_addr *addr);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 要设置的地址

### netlib_set_dripv4addr

```c
int netlib_set_dripv4addr(const char *ifname, const struct in_addr *addr);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 要设置的地址

### netlib_get_dripv4addr

```c
int netlib_get_dripv4addr(const char *ifname, struct in_addr *addr);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 用于存储默认路由地址

### netlib_set_ipv4netmask

```c
int netlib_set_ipv4netmask(const char *ifname, const struct in_addr *addr);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 要设置的地址

### netlib_get_ipv4netmask

```c
int netlib_get_ipv4netmask(const char *ifname, struct in_addr *addr);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 用于存储子网掩码

### netlib_ipv4adaptor

```c
int netlib_ipv4adaptor(in_addr_t destipaddr, in_addr_t *srcipaddr);
```

**参数**：

- `destipaddr` 目标 IPv4 地址
- `srcipaddr` 用于存储适配器地址

### netlib_read_ipv4route

```c
ssize_t netlib_read_ipv4route(FILE *stream, struct netlib_ipv4_route_s *route);
```

**参数**：

- `fd` procfs IPv4 路由表的文件描述符
- `route` 用于存储下一条路由表项

### netlib_ipv4router

```c
int netlib_ipv4router(const struct in_addr *destipaddr, struct in_addr *router);
```

**参数**：

- `destipaddr` 目标 IP 地址。
- `router` - 用于存储网关的 IP 地址，即

### netlib_obtain_ipv4addr

```c
int netlib_obtain_ipv4addr(const char *ifname);
```

**参数**：

- `ifname` 网络接口名称

### netlib_set_ipv4dnsaddr

```c
int netlib_set_ipv4dnsaddr(const struct in_addr *inaddr);
```

**参数**：

- `inaddr` 要设置的地址

**IPv6 地址管理**

### netlib_add_ipv6addr

```c
int netlib_add_ipv6addr(const char *ifname, const struct in6_addr *addr, uint8_t preflen);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 地址 to add
- `preflen` 前缀长度（位）。

### netlib_del_ipv6addr

```c
int netlib_del_ipv6addr(const char *ifname, const struct in6_addr *addr, uint8_t preflen);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 地址 to delete
- `preflen` 前缀长度（位）。

### netlib_get_ipv6addr

```c
int netlib_get_ipv6addr(const char *ifname, struct in6_addr *addr);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 用于存储 IP 地址

### netlib_set_ipv6addr

```c
int netlib_set_ipv6addr(const char *ifname, const struct in6_addr *addr);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 要设置的地址

### netlib_set_dripv6addr

```c
int netlib_set_dripv6addr(const char *ifname, const struct in6_addr *addr);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 要设置的地址

### netlib_set_ipv6netmask

```c
int netlib_set_ipv6netmask(const char *ifname, const struct in6_addr *addr);
```

**参数**：

- `ifname` 网络接口名称
- `ipaddr` 要设置的地址

### netlib_ipv6adaptor

```c
int netlib_ipv6adaptor(const struct in6_addr *destipaddr, struct in6_addr *srcipaddr);
```

**参数**：

- `destipaddr` 目标 IP 地址。
- `srcipaddr` - 用于存储适配器地址

### netlib_ipv6netmask2prefix

```c
uint8_t netlib_ipv6netmask2prefix(const uint16_t *mask);
```

**参数**：

- `mask` 子网掩码。

### netlib_prefix2ipv6netmask

```c
void netlib_prefix2ipv6netmask(uint8_t preflen, struct in6_addr *netmask);
```

**参数**：

- `preflen` 前缀长度（位）。
- `netmask` 用于存储子网掩码.

### netlib_read_ipv6route

```c
ssize_t netlib_read_ipv6route(FILE *stream, struct netlib_ipv6_route_s *route);
```

**参数**：

- `fd` 路由表项。
- `route` 用于存储下一条路由表项

### netlib_ipv6router

```c
int netlib_ipv6router(const struct in6_addr *destipaddr, struct in6_addr *router);
```

**参数**：

- `destipaddr` 目标 IP 地址。
- `router` - 用于存储网关的 IP 地址，即

### netlib_obtain_ipv6addr

```c
int netlib_obtain_ipv6addr(const char *ifname);
```

**参数**：

- `ifname` 网络接口名称。

### netlib_set_ipv6dnsaddr

```c
int netlib_set_ipv6dnsaddr(const struct in6_addr *inaddr);
```

**参数**：

- `inaddr` 要设置的地址

**接口管理**

### netlib_setmacaddr

```c
int netlib_setmacaddr(const char *ifname, const uint8_t *macaddr);
```

**参数**：

- `ifname` 网络接口名称
- `macaddr` MAC 地址。

### netlib_getmacaddr

```c
int netlib_getmacaddr(const char *ifname, uint8_t *macaddr);
```

**参数**：

- `ifname` 网络接口名称
- `macaddr` 用于存储 MAC 地址

### netlib_getessid

```c
int netlib_getessid(const char *ifname, char *essid, size_t idlen);
```

**参数**：

- `ifname` 网络接口名称
- `essid` 用于存储结果。
- `idlen` ESSID 缓冲区大小。

### netlib_setessid

```c
int netlib_setessid(const char *ifname, const char *essid);
```

**参数**：

- `ifname` 网络接口名称
- `essid` ESSID（网络名称）。

### netlib_getifstatus

```c
int netlib_getifstatus(const char *ifname, uint8_t *flags);
```

**参数**：

- `ifname` 网络接口名称
- `flags` 接口标志。

### netlib_ifup

```c
int netlib_ifup(const char *ifname);
```

**参数**：

- `ifname` 网络接口名称

### netlib_ifdown

```c
int netlib_ifdown(const char *ifname);
```

**参数**：

- `ifname` 网络接口名称

### netlib_set_mtu

```c
int netlib_set_mtu(const char *ifname, int mtu);
```

**参数**：

- `ifname` 网络接口名称
- `mtu` 最大传输单元（MTU）。

**返回值**：

:

### netlib_getifstatistics

```c
int netlib_getifstatistics(const char *ifname, struct netdev_statistics_s *stat);
```

**参数**：

- `ifname` 网络接口名称。
- `stat` 用于存储设备统计信息。

### netlib_check_ifconflict

```c
int netlib_check_ifconflict(const char *ifname);
```

**参数**：

- `ifname` 网络接口名称

**路由管理**

### netlib_get_route

```c
ssize_t netlib_get_route(struct rtentry *rtelist, unsigned int nentries, sa_family_t family);
```

**参数**：

- `rtelist` 用于存储设备列表。
- `nentries` 数组容量（条目数）。
- `family` - 地址族。  See AF_* definitions in

**ARP 管理**

### netlib_del_arpmapping

```c
int netlib_del_arpmapping(const struct sockaddr_in *inaddr, const char *ifname);
```

**参数**：

- `inaddr` IPv4 地址。
- `ifname` 网络接口名称。

### netlib_get_arpmapping

```c
int netlib_get_arpmapping(const struct sockaddr_in *inaddr, uint8_t *macaddr, const char *ifname);
```

**参数**：

- `inaddr` IPv4 地址。
- `macaddr` 用于存储对应的以太网 MAC 地址
- `ifname` 网络接口名称。

### netlib_set_arpmapping

```c
int netlib_set_arpmapping(const struct sockaddr_in *inaddr, const uint8_t *macaddr, const char *ifname);
```

**参数**：

- `inaddr` IPv4 地址。
- `macaddr` MAC 地址。
- `ifname` 网络接口名称。

### netlib_get_arptable

```c
ssize_t netlib_get_arptable(struct arpreq *arptab, unsigned int nentries);
```

**参数**：

- `arptab` 用于存储 ARP 表副本
- `nentries` 数组容量（条目数）。

### netlib_ifarp

```c
int netlib_ifarp(const char *ifname);
```

**参数**：

- `ifname` 网络接口名称

### netlib_ifnoarp

```c
int netlib_ifnoarp(const char *ifname);
```

**参数**：

- `ifname` 网络接口名称

**DNS 管理**

### netlib_clear_dnsaddr

```c
void netlib_clear_dnsaddr(void);
```

**VLAN 管理**

### netlib_add_vlan

```c
int netlib_add_vlan(const char *ifname, int vlanid, int prio);
```

**参数**：

- `ifname` 网络接口名称。
- `vlanid` VLAN 标识符。
- `prio` 默认 VLAN 优先级（PCP）。

### netlib_del_vlan

```c
int netlib_del_vlan(const char *vlanif);
```

**iptables**

### netlib_ipt_commit

```c
int netlib_ipt_commit(const struct ipt_replace *repl);
```

**参数**：

- `repl` 要提交的配置。

### netlib_ipt_flush

```c
int netlib_ipt_flush(const char *table, enum nf_inet_hooks hook);
```

**参数**：

- `table` 表名。
- `hook` 钩子点。

### netlib_ipt_policy

```c
int netlib_ipt_policy(const char *table, enum nf_inet_hooks hook, int verdict);
```

**参数**：

- `table` 策略。
- `hook` 钩子点。
- `verdict` 判定值。

### netlib_ipt_append

```c
int netlib_ipt_append(struct ipt_replace **repl, const struct ipt_entry *entry, enum nf_inet_hooks hook);
```

**参数**：

- `repl` 要提交的配置。
- `entry` 要追加的规则条目。
- `hook` 钩子点。

### netlib_ipt_insert

```c
int netlib_ipt_insert(struct ipt_replace **repl, const struct ipt_entry *entry, enum nf_inet_hooks hook, int rulenum);
```

**参数**：

- `repl` 要提交的配置。
- `entry` 要插入的规则条目。
- `hook` 钩子点。
- `rulenum` 规则编号。

### netlib_ipt_delete

```c
int netlib_ipt_delete(struct ipt_replace *repl, const struct ipt_entry *entry, enum nf_inet_hooks hook, int rulenum);
```

**参数**：

- `repl` 要提交的配置。
- `entry` 要删除的规则条目。
- `hook` 钩子点。
- `rulenum` 规则编号。

### netlib_ipt_fillifname

```c
int netlib_ipt_fillifname(struct ipt_entry *entry, const char *inifname, const char *outifname);
```

**参数**：

- `entry` 要填充的规则条目。
- `inifname` 输入设备名称，`NULL` 表示不变。
- `outifname` 输出设备名称，`NULL` 表示不变。

### netlib_ip6t_commit

```c
int netlib_ip6t_commit(const struct ip6t_replace *repl);
```

**参数**：

- `repl` 要提交的配置。

### netlib_ip6t_flush

```c
int netlib_ip6t_flush(const char *table, enum nf_inet_hooks hook);
```

**参数**：

- `table` 表名。
- `hook` 钩子点。

### netlib_ip6t_policy

```c
int netlib_ip6t_policy(const char *table, enum nf_inet_hooks hook, int verdict);
```

**参数**：

- `table` 策略。
- `hook` 钩子点。
- `verdict` 判定值。

### netlib_ip6t_append

```c
int netlib_ip6t_append(struct ip6t_replace **repl, const struct ip6t_entry *entry, enum nf_inet_hooks hook);
```

**参数**：

- `repl` 要提交的配置。
- `entry` 要追加的规则条目。
- `hook` 钩子点。

### netlib_ip6t_insert

```c
int netlib_ip6t_insert(struct ip6t_replace **repl, const struct ip6t_entry *entry, enum nf_inet_hooks hook, int rulenum);
```

**参数**：

- `repl` 要提交的配置。
- `entry` 要插入的规则条目。
- `hook` 钩子点。
- `rulenum` 规则编号。

### netlib_ip6t_delete

```c
int netlib_ip6t_delete(struct ip6t_replace *repl, const struct ip6t_entry *entry, enum nf_inet_hooks hook, int rulenum);
```

**参数**：

- `repl` 要提交的配置。
- `entry` 要删除的规则条目。
- `hook` 钩子点。
- `rulenum` 规则编号。

### netlib_ip6t_fillifname

```c
int netlib_ip6t_fillifname(struct ip6t_entry *entry, const char *inifname, const char *outifname);
```

**参数**：

- `entry` 要填充的规则条目。
- `inifname` 输入设备名称，`NULL` 表示不变。
- `outifname` 输出设备名称，`NULL` 表示不变。

**连接检测**

### netlib_check_ipconnectivity

```c
int netlib_check_ipconnectivity(const char *ip, int timeout, int retry);
```

**参数**：

- `ip` 要检查的 IPv4 地址。
- `timeout` 超时时间。
- `retry` 重试次数。

### netlib_check_ifconnectivity

```c
int netlib_check_ifconnectivity(const char *ifname, int timeout, int retry);
```

**参数**：

- `ifname` 网络接口名称
- `timeout` 超时时间。
- `retry` 重试次数。

**URL 解析**

### netlib_parsehttpurl

```c
int netlib_parsehttpurl(const char *url, uint16_t *port, char *hostname, int hostlen, char *filename, int namelen);
```

**参数**：

- `url` HTTP 相关参数。
- `port` 指向 `uint16_t`，用于存储解析出的端口号。
- `hostname` 用于存储结果的缓冲区。
- `hostlen` 缓冲区大小。
- `filename` 用于存储结果的缓冲区。
- `namelen` 缓冲区大小。

### netlib_parseurl

```c
int netlib_parseurl(const char *str, struct url_s *url);
```

### netlib_check_httpconnectivity

```c
int netlib_check_httpconnectivity(const char *host, const char *getmsg, int port, int expect_code);
```

**参数**：

- `host` 远程主机地址。
- `getmsg` HTTP 相关参数。
- `port` 端口号。
- `expect_code` HTTP 相关参数。

**其他**

### netlib_get_devices

```c
ssize_t netlib_get_devices(struct netlib_device_s *devlist, unsigned int nentries, sa_family_t family);
```

**参数**：

- `devlist` 用于存储设备列表。
- `nentries` 数组容量（条目数）。
- `family` 地址族。  See AF_* definitions in

### netlib_seteaddr

```c
int netlib_seteaddr(const char *ifname, const uint8_t *eaddr);
```

**参数**：

- `ifname` 网络接口名称
- `eaddr` 新地址。

### netlib_getpanid

```c
int netlib_getpanid(const char *ifname, uint8_t *panid);
```

**参数**：

- `ifname` 网络接口名称
- `panid` 用于存储当前 PAN ID

### netlib_getproperties

```c
int netlib_getproperties(const char *ifname, struct pktradio_properties_s *properties);
```

**参数**：

- `ifname` 网络接口名称
- `nodeadd` 用于存储节点地址。

### netlib_setnodeaddr

```c
int netlib_setnodeaddr(const char *ifname, const struct pktradio_addr_s *nodeaddr);
```

**参数**：

- `ifname` 网络接口名称
- `nodeadd` 新地址。

### netlib_getnodnodeaddr

```c
int netlib_getnodnodeaddr(const char *ifname, struct pktradio_addr_s *nodeaddr);
```

**参数**：

- `ifname` 网络接口名称
- `nodeadd` 用于存储节点地址。

### netlib_get_nbtable

```c
ssize_t netlib_get_nbtable(struct neighbor_entry_s *nbtab, unsigned int nentries);
```

**参数**：

- `nbtab` 用于存储邻居表副本
- `nentries` 数组容量（条目数）。

### netlib_icmpv6_autoconfiguration

```c
int netlib_icmpv6_autoconfiguration(const char *ifname);
```

**参数**：

- `ifname` 网络接口名称

### netlib_parse_conntrack

```c
int netlib_parse_conntrack(const struct nlmsghdr *nlh, size_t len, struct netlib_conntrack_s *ct);
```

**参数**：

- `nlh` 要解析的 netlink 消息。
- `ct` 连接跟踪条目。

### netlib_get_conntrack

```c
int netlib_get_conntrack(sa_family_t family, netlib_conntrack_cb_t cb);
```

**参数**：

- `family` 地址族，用于过滤 conntrack 表项。
- `cb` 连接跟踪条目。

### netlib_listenon

```c
int netlib_listenon(uint16_t portno);
```

**参数**：

- `portno` 端口号。

### netlib_server

```c
void netlib_server(uint16_t portno, pthread_startroutine_t handler, int stacksize);
```

**参数**：

- `portno` 端口号。
- `handler` 任务入口函数。
- `stacksize` 栈大小。

### netlib_get_iobinfo

```c
int netlib_get_iobinfo(struct iob_stats_s *iob);
```

**参数**：

- `iob` IOB 信息结构体。


### netlib_ipv4addrconv

```c
bool netlib_ipv4addrconv(const char *addrstr, uint8_t *addr);
```

将 IPv4 地址字符串（如 `"192.168.1.1"`）转换为 4 字节二进制数组。

**参数**：

- `addrstr` IPv4 地址字符串。
- `addr` 输出缓冲区（4 字节）。

**返回值**：

转换成功返回 `true`，格式非法时返回 `false`。

### netlib_ethaddrconv

```c
bool netlib_ethaddrconv(const char *hwstr, uint8_t *hw);
```

将以太网 MAC 地址字符串（如 `"aa:bb:cc:dd:ee:ff"`）转换为 6 字节二进制数组。

**参数**：

- `hwstr` MAC 地址字符串。
- `hw` 输出缓冲区（6 字节）。

**返回值**：

转换成功返回 `true`，格式非法时返回 `false`。

### netlib_saddrconv

```c
bool netlib_saddrconv(const char *hwstr, uint8_t *hw);
```

将 IEEE 802.15.4 短地址（2 字节）字符串转换为二进制形式。

**参数**：

- `hwstr` 地址字符串。
- `hw` 输出缓冲区（2 字节）。

**返回值**：

转换成功返回 `true`，格式非法时返回 `false`。

### netlib_eaddrconv

```c
bool netlib_eaddrconv(const char *hwstr, uint8_t *hw);
```

将 IEEE 802.15.4 扩展地址（8 字节）字符串转换为二进制形式。

**参数**：

- `hwstr` 地址字符串。
- `hw` 输出缓冲区（8 字节）。

**返回值**：

转换成功返回 `true`，格式非法时返回 `false`。

### netlib_nodeaddrconv

```c
bool netlib_nodeaddrconv(const char *addrstr,
                         struct pktradio_addr_s *nodeaddr);
```

将 pktradio 节点地址字符串转换为 `pktradio_addr_s` 结构体。

**参数**：

- `addrstr` 节点地址字符串。
- `nodeaddr` 输出结构体指针。

**返回值**：

转换成功返回 `true`，格式非法时返回 `false`。
