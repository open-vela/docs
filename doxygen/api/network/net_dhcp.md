# DHCP API

DHCP（Dynamic Host Configuration Protocol）客户端与服务器接口，覆盖 IPv4（`dhcpc_*` / `dhcpd_*`）和 IPv6（`dhcp6c_*`）两套地址分配协议。

头文件：`#include <netutils/dhcpc.h>`、`#include <netutils/dhcp6c.h>`、`#include <netutils/dhcpd.h>`

## openvela 实现说明

- **IPv4 客户端**：`dhcpc_*` 系列封装完整的 DHCP 客户端状态机（DISCOVER/OFFER/REQUEST/ACK）
- **IPv6 客户端**：`dhcp6c_*` 系列处理 IPv6 的 SLAAC / DHCPv6 流程
- **服务器**：`dhcpd_*` 系列提供简单的 DHCP 服务器能力，可在热点/AP 模式下分配 IP
- **异步调用**：`*_request_async` 接口提供回调式调用，避免阻塞当前线程
- **配置依赖**：需启用 `CONFIG_NETUTILS_DHCPC` / `CONFIG_NETUTILS_DHCP6C` / `CONFIG_NETUTILS_DHCPD`

## DHCP 客户端

头文件：`#include <netutils/dhcpc.h>`

### dhcpc_open

```c
void *dhcpc_open(const char *interface, const void *mac_addr, int mac_len);
```

创建 DHCP 客户端会话。

**参数**：

- `interface` 网络接口名称（如 `"eth0"`）。
- `mac_addr` MAC 地址。
- `mac_len` MAC 地址长度。

**返回值**：

成功时返回会话句柄，失败时返回 `NULL`。

### dhcpc_request

```c
int dhcpc_request(void *handle, struct dhcpc_state *presult);
```

执行 DHCP 协商获取 IP 地址（阻塞调用）。

**参数**：

- `handle` 由 `dhcpc_open()` 返回的会话句柄。
- `presult` 存储获取的网络配置（IP、子网掩码、网关、DNS、租约时间）。

**返回值**：

成功时返回 0，失败时返回 -1。

### dhcpc_request_async

```c
int dhcpc_request_async(void *handle, dhcpc_callback_t callback);
```

异步执行 DHCP 协商，在后台线程中运行，通过回调返回结果。

**参数**：

- `handle` 会话句柄。
- `callback` 结果回调函数。

**返回值**：

成功启动时返回 0，失败时返回 -1。

### dhcpc_cancel

```c
void dhcpc_cancel(void *handle);
```

取消正在进行的 DHCP 协商。

### dhcpc_close

```c
void dhcpc_close(void *handle);
```

关闭 DHCP 客户端会话，释放所有资源。内部会先调用 `dhcpc_cancel()`。


## DHCPv6 客户端

头文件：`#include <netutils/dhcp6c.h>`

### dhcp6c_open

```c
void *dhcp6c_open(const char *interface);
```

创建 DHCPv6 客户端会话。

**参数**：

- `interface` 网络接口名称。

**返回值**：

成功时返回会话句柄，失败时返回 `NULL`。

### dhcp6c_request

```c
int dhcp6c_request(void *handle, struct dhcp6c_state *presult);
```

执行 DHCPv6 协商获取地址（阻塞调用）。

### dhcp6c_request_async

```c
int dhcp6c_request_async(void *handle, dhcp6c_callback_t callback);
```

异步执行 DHCPv6 协商。

### dhcp6c_cancel

```c
void dhcp6c_cancel(void *handle);
```

取消正在进行的 DHCPv6 协商。

### dhcp6c_close

```c
void dhcp6c_close(void *handle);
```

关闭 DHCPv6 客户端会话。


## DHCP 服务器

头文件：`#include <netutils/dhcpd.h>`

### dhcpd_run

```c
int dhcpd_run(const char *interface);
```

在当前线程运行 DHCP 服务器（阻塞，直到出错才返回）。

### dhcpd_start

```c
int dhcpd_start(const char *interface);
```

以后台任务启动 DHCP 服务器守护进程。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### dhcpd_stop

```c
int dhcpd_stop(void);
```

停止运行中的 DHCP 服务器守护进程。

### dhcpd_set_startip

```c
int dhcpd_set_startip(in_addr_t startip);
```

配置 DHCP 服务器分配地址池的起始 IP 地址。

**参数**：

- `startip` 起始 IP 地址（网络字节序）。

**返回值**：

始终返回 `0`。

### dhcpd_set_routerip

```c
int dhcpd_set_routerip(in_addr_t routerip);
```

配置 DHCP 服务器下发给客户端的默认网关地址。

**参数**：

- `routerip` 默认网关 IP（网络字节序）。

**返回值**：

始终返回 `0`。

### dhcpd_set_netmask

```c
int dhcpd_set_netmask(in_addr_t netmask);
```

配置 DHCP 服务器下发给客户端的子网掩码。

**参数**：

- `netmask` 子网掩码（网络字节序）。

**返回值**：

始终返回 `0`。

### dhcpd_set_dnsip

```c
int dhcpd_set_dnsip(in_addr_t dnsip);
```

配置 DHCP 服务器下发给客户端的 DNS 服务器地址。

**参数**：

- `dnsip` DNS 服务器 IP（网络字节序）。

**返回值**：

始终返回 `0`。
