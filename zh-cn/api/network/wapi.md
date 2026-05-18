\[ [English](../../../en/api/network/wapi.md) | 简体中文 \]

# 无线网络接口（WAPI）API

`wapi_*` 系列接口基于 Linux Wireless Extensions（WEXT）封装，提供无线网络配置、扫描、关联、功率管理、区域代码和 PMKSA 缓存等能力。

头文件：`#include <wireless/wapi.h>`

## openvela 实现说明

- **底层机制**：基于 Linux Wireless Extensions（WEXT）的 ioctl 协议与 Wi-Fi 驱动通信
- **支持场景**：Station（客户端）模式、AP 模式、混杂模式（由驱动支持程度决定）
- **配置依赖**：需启用 `CONFIG_WIRELESS_WAPI` 及对应的 Wi-Fi 芯片驱动
- **典型用法**：
    - `wapi_set_ifup`/`wapi_set_ifdown` 控制接口启停
    - `wapi_set_essid` + `wapi_set_mode` 配置连接目标
    - `wapi_scan_*` / `wapi_escan_*` 扫描周围 AP
    - `wapi_load_config` / `wapi_save_config` 持久化配置
- **扩展能力**：通过 `wapi_extend_params` / `wapi_set_pmksa` 等接口与驱动私有特性交互

## 无线网络接口

头文件：`#include <wireless/wapi.h>`

wapi 提供无线网络配置接口，包括 SSID 扫描、连接、频率设置等。

**连接管理**

### wapi_get_ifup

```c
int wapi_get_ifup(int sock, const char *ifname, int *is_up);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称.
- `is_up` 接口状态，0 表示启用，1 表示禁用。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_ifup

```c
int wapi_set_ifup(int sock, const char *ifname);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称.

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_ifdown

```c
int wapi_set_ifdown(int sock, const char *ifname);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称，将被关闭。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_get_ip

```c
int wapi_get_ip(int sock, const char *ifname, struct in_addr *addr);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称.
- `addr` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_ip

```c
int wapi_set_ip(int sock, const char *ifname, const struct in_addr *addr);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称，其 IP 地址
- `addr` 指向包含新 IP 地址的结构体。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_get_netmask

```c
int wapi_get_netmask(int sock, const char *ifname, struct in_addr *addr);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称.
- `addr` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_netmask

```c
int wapi_set_netmask(int sock, const char *ifname, const struct in_addr *addr);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称.
- `addr` 指向包含新子网掩码的结构体。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_add_route_gw

```c
int wapi_add_route_gw(int sock, enum wapi_route_target_e targettype, const struct in_addr *target, const struct in_addr *netmask, const struct in_addr *gw);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `targettype` 目标类型。
- `target` 指向目标 IP 地址。
- `netmask` 指向目标地址对应的子网掩码。
- `gw` 指向对应的网关（路由器）IP 地址，用于

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_del_route_gw

```c
int wapi_del_route_gw(int sock, enum wapi_route_target_e targettype, const struct in_addr *target, const struct in_addr *netmask, const struct in_addr *gw);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `targettype` 目标类型。
- `target` 指向路由的目标 IP 地址
- `netmask` 指向目标地址对应的子网掩码。
- `gw` 指向对应的网关（路由器）IP 地址，用于

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_get_freq

```c
int wapi_get_freq(int sock, const char *ifname, double *freq, enum wapi_freq_flag_e *flag);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `freq` 输出参数。
- `flag` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_freq

```c
int wapi_set_freq(int sock, const char *ifname, double freq, enum wapi_freq_flag_e flag);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `freq` 频率值。
- `flag` 频率值。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_freq2chan

```c
int wapi_freq2chan(int sock, const char *ifname, double freq, int *chan);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `freq` 频率（Hz），将被转换为信道编号。
- `chan` 输出参数。

### wapi_chan2freq

```c
int wapi_chan2freq(int sock, const char *ifname, int chan, double *freq);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 信道。
- `chan` 信道编号，将被转换为频率。
- `freq` 输出参数。

### wapi_get_essid

```c
int wapi_get_essid(int sock, const char *ifname, char *essid, enum wapi_essid_flag_e *flag);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `essid` 用于存储结果。
- `flag` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_essid

```c
int wapi_set_essid(int sock, const char *ifname, const char *essid, enum wapi_essid_flag_e flag);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `essid` 指向一个以 `\0` 结尾的 ESSID 字符串
- `flag` 控制标志。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_get_mode

```c
int wapi_get_mode(int sock, const char *ifname, enum wapi_mode_e *mode);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `mode` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_mode

```c
int wapi_set_mode(int sock, const char *ifname, enum wapi_mode_e mode);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `mode` 输出参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_make_broad_ether

```c
int wapi_make_broad_ether(struct ether_addr *sa);
```

**参数**：

- `sa` 输出参数。

**返回值**：

返回底层 `wapi_make_ether()` 调用的结果。

### wapi_make_null_ether

```c
int wapi_make_null_ether(struct ether_addr *sa);
```

**参数**：

- `sa` 输出参数。

**返回值**：

返回底层 `wapi_make_ether()` 调用的结果。

### wapi_get_ap

```c
int wapi_get_ap(int sock, const char *ifname, struct ether_addr *ap);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `ap` 要设置的地址。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_ap

```c
int wapi_set_ap(int sock, const char *ifname, const struct ether_addr *ap);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `ap` 接入点的 MAC 地址。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_get_bitrate

```c
int wapi_get_bitrate(int sock, const char *ifname, int *bitrate, enum wapi_bitrate_flag_e *flag);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `bitrate` 输出参数，用于存储查询到的比特率。
- `flag` 输出参数，用于存储比特率标志位。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_bitrate

```c
int wapi_set_bitrate(int sock, const char *ifname, int bitrate, enum wapi_bitrate_flag_e flag);
```

**参数**：

- `sock` 套接字描述符（用于 ioctl 操作）。
- `ifname` 网络接口名称。
- `bitrate` 比特率 .
- `flag` 比特率 flag.

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_dbm2mwatt

```c
int wapi_dbm2mwatt(int dbm);
```

**参数**：

- `dbm` 要转换的 dBm 值。

**返回值**：

转换后的毫瓦值。

### wapi_mwatt2dbm

```c
int wapi_mwatt2dbm(int mwatt);
```

**参数**：

- `mwatt` 毫瓦值。

**返回值**：

转换后的 dBm 值。

### wapi_get_txpower

```c
int wapi_get_txpower(int sock, const char *ifname, int *power, enum wapi_txpower_flag_e *flag);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。
- `power` 输出参数，用于存储发射功率值。
- `flag` 输出参数，用于存储发射功率的单位。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_txpower

```c
int wapi_set_txpower(int sock, const char *ifname, int power, enum wapi_txpower_flag_e flag);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。
- `power` 发射功率。
- `flag` 发射功率。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_make_socket

```c
int wapi_make_socket(void);
```

### wapi_scan_init

```c
int wapi_scan_init(int sock, const char *ifname, const char *essid);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。
- `essid` 要扫描的 ESSID。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_scan_channel_init

```c
int wapi_scan_channel_init(int sock, const char *ifname, const char *essid, uint8_t *channels, int num_channels);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。
- `essid` 要扫描的 ESSID。
- `channels` 要扫描的信道编号数组。
- `num_channels` 信道。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_escan_init

```c
int wapi_escan_init(int sock, const char *ifname, uint8_t scan_type, const char *essid);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。
- `scan_type` 扫描类型。
- `essid` 要扫描的 ESSID。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_escan_channel_init

```c
int wapi_escan_channel_init(int sock, const char *ifname, uint8_t scan_type, const char *essid, uint8_t *channels, int num_channels);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。
- `scan_type` 扫描类型。
- `essid` 要扫描的 ESSID。
- `channels` 要扫描的信道编号数组。
- `num_channels` 信道。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_scan_stat

```c
int wapi_scan_stat(int sock, const char *ifname);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。

### wapi_scan_coll

```c
int wapi_scan_coll(int sock, const char *ifname, struct wapi_list_s *aps);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。
- `aps` 收集的扫描结果列表。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_scan_coll_free

```c
void wapi_scan_coll_free(struct wapi_list_s *aps);
```

**参数**：

- `aps` 要释放的扫描结果列表。

### wapi_set_country

```c
int wapi_set_country(int sock, const char *ifname, const char *country);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。
- `country` 指向双字符字符串，表示要设置的

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_get_country

```c
int wapi_get_country(int sock, const char *ifname, char *country);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。
- `country` 指向调用方提供的缓冲区，用于接收

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_get_sensitivity

```c
int wapi_get_sensitivity(int sock, const char *ifname, int *sense);
```

**参数**：

- `sock` 套接字描述符.
- `ifname` 网络接口名称。
- `sense` 指向调用方提供的整型变量，用于接收

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_load_config

```c
void *wapi_load_config(const char *ifname, const char *confname, struct wpa_wconfig_s *conf);
```

**参数**：

- `ifname` 网络接口名称。
- `confname` 路径。
- `conf` 指向调用方提供的结构体，用于填入

### wapi_unload_config

```c
void wapi_unload_config(void *load);
```

**参数**：

- `load` 配置资源句柄。

### wapi_save_config

```c
int wapi_save_config(const char *ifname, const char *confname, const struct wpa_wconfig_s *conf);
```

**参数**：

- `ifname` 网络接口名称。
- `confname` 路径。
- `conf` 指向包含配置信息的结构体

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_pta_prio

```c
int wapi_set_pta_prio(int sock, const char *ifname, enum wapi_pta_prio_e pta_prio);
```

**参数**：

- `sock` 文件描述符。
- `ifname` 网络接口名称。
- `pta_prio` PTA 优先级。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_get_pta_prio

```c
int wapi_get_pta_prio(int sock, const char *ifname, enum wapi_pta_prio_e *pta_prio);
```

**参数**：

- `sock` 文件描述符。
- `ifname` 网络接口名称。
- `pta_prio` 指向用于接收当前 PTA 优先级的变量

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_pmksa

```c
int wapi_set_pmksa(int sock, const char *ifname, const uint8_t *pmk, int len);
```

**参数**：

- `sock` 文件描述符。
- `ifname` 网络接口名称。
- `pmk` 指向包含 PMKSA 数据的缓冲区
- `len` 长度。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_get_pmksa

```c
int wapi_get_pmksa(int sock, const char *ifname, uint8_t *pmk, int len);
```

**参数**：

- `sock` 文件描述符。
- `ifname` 网络接口名称。
- `pmk` 指向用于接收查询到的 PMKSA 数据的缓冲区
- `len` 缓冲区大小。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_extend_params

```c
int wapi_extend_params(int sock, int cmd, struct iwreq *wrq);
```

**参数**：

- `sock` 文件描述符。
- `cmd` 私有 ioctl 命令码。
- `wrq` 指向 `iwreq` 结构体，调用方需预先

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_set_power_save

```c
int wapi_set_power_save(int sock, const char *ifname, bool on);
```

**参数**：

- `sock` 文件描述符。
- `ifname` 网络接口名称。
- `on` 控制标志。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### wapi_get_power_save

```c
int wapi_get_power_save(int sock, const char *ifname, bool *on);
```

**参数**：

- `sock` 文件描述符。
- `ifname` 网络接口名称。
- `on` 指向用于接收当前状态的布尔变量

**返回值**：

成功时返回 0，失败时返回负的错误码。

