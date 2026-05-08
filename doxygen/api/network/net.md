# 网络 API

openvela 提供与 BSD 兼容的套接字接口，支持 IPv4（`AF_INET`）、IPv6（`AF_INET6`）等协议族，以及流套接字（`SOCK_STREAM`）、数据报套接字（`SOCK_DGRAM`）和原始套接字（`SOCK_RAW`）。

头文件：`#include <sys/socket.h>`、`#include <netinet/in.h>`、`#include <arpa/inet.h>`

## openvela 实现说明

- **协议族支持**：`AF_INET`（IPv4）、`AF_INET6`（IPv6）、`AF_LOCAL`/`AF_UNIX`（本地套接字）、`AF_PACKET`（原始链路层）等，具体取决于网络栈配置
- **配置依赖**：网络子系统是可选的，需要启用 `CONFIG_NET` 及相关协议配置（如 `CONFIG_NET_TCP`、`CONFIG_NET_UDP`）
- **非阻塞 I/O**：通过 `fcntl(fd, F_SETFL, O_NONBLOCK)` 或 `SOCK_NONBLOCK` 标志设置
- **DNS 解析**：需要启用 `CONFIG_NETDB_DNSCLIENT`，通过 `nuttx/net/dns.h` 接口管理 DNS 服务器

## 套接字创建与管理

### socket

```c
int socket(int domain, int type, int protocol);
```

创建一个通信端点（套接字），返回文件描述符。

**参数**：

- `domain` 协议族：
  - `AF_INET` IPv4
  - `AF_INET6` IPv6
  - `AF_LOCAL` / `AF_UNIX` 本地套接字
  - `AF_PACKET` 原始链路层
- `type` 套接字类型：
  - `SOCK_STREAM` 面向连接的流套接字（TCP）
  - `SOCK_DGRAM` 无连接的数据报套接字（UDP）
  - `SOCK_RAW` 原始套接字
  - 可与 `SOCK_NONBLOCK`、`SOCK_CLOEXEC` 按位或组合
- `protocol` 协议编号，通常为 0（自动选择）。也可指定 `IPPROTO_TCP`、`IPPROTO_UDP` 等。

**返回值**：

成功时返回非负文件描述符，失败时返回 -1 并设置 `errno`：

- `EAFNOSUPPORT` 不支持的协议族。
- `EPROTONOSUPPORT` 不支持的协议类型。
- `EMFILE` 进程文件描述符数量已达上限。
- `ENOMEM` 内存不足。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### socketpair

```c
int socketpair(int domain, int type, int protocol, int sv[2]);
```

创建一对已连接的套接字，常用于父子进程间通信。

**参数**：

- `domain` 协议族，通常为 `AF_LOCAL`。
- `type` 套接字类型（`SOCK_STREAM` 或 `SOCK_DGRAM`）。
- `protocol` 通常为 0。
- `sv` 输出参数，存储两个已连接的文件描述符。

**返回值**：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EAFNOSUPPORT` 不支持的协议族。
- `EMFILE` 文件描述符数量已达上限。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### shutdown

```c
int shutdown(int sockfd, int how);
```

关闭套接字的部分或全部通信方向。与 `close()` 不同，`shutdown()` 可以只关闭读或写方向。

**参数**：

- `sockfd` 套接字文件描述符。
- `how` 关闭方式：
  - `SHUT_RD` 关闭读方向。
  - `SHUT_WR` 关闭写方向（发送 FIN）。
  - `SHUT_RDWR` 关闭读写双向。

**返回值**：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EBADF` 无效的文件描述符。
- `ENOTCONN` 套接字未连接。
- `EINVAL` `how` 参数无效。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

## 连接管理

### bind

```c
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```

将套接字绑定到指定的本地地址和端口。服务器端在 `listen()` 前必须调用 `bind()`。

**参数**：

- `sockfd` 套接字文件描述符。
- `addr` 本地地址结构体（`struct sockaddr_in` 或 `struct sockaddr_in6`）。
- `addrlen` 地址结构体的大小。

**返回值**：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EBADF` 无效的文件描述符。
- `EINVAL` 套接字已绑定，或地址无效。
- `EADDRINUSE` 地址已被使用。
- `EADDRNOTAVAIL` 请求的地址不可用。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### connect

```c
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```

发起到远程地址的连接。对于 TCP 套接字，执行三次握手；对于 UDP 套接字，设置默认目标地址。

**参数**：

- `sockfd` 套接字文件描述符。
- `addr` 远程地址结构体。
- `addrlen` 地址结构体的大小。

**返回值**：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EBADF` 无效的文件描述符。
- `ECONNREFUSED` 远程主机拒绝连接。
- `ETIMEDOUT` 连接超时。
- `ENETUNREACH` 网络不可达。
- `EINPROGRESS` 非阻塞模式下连接正在进行。
- `EISCONN` 套接字已连接。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### listen

```c
int listen(int sockfd, int backlog);
```

将套接字标记为被动监听状态，准备接受连接请求。

**参数**：

- `sockfd` 已绑定的套接字文件描述符。
- `backlog` 等待连接队列的最大长度。

**返回值**：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EBADF` 无效的文件描述符。
- `EOPNOTSUPP` 套接字类型不支持 `listen()`。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### accept

```c
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
```

从监听套接字的等待队列中取出第一个连接请求，创建并返回一个新的已连接套接字。如果队列为空，阻塞等待。

**参数**：

- `sockfd` 监听套接字文件描述符。
- `addr` 如果非 `NULL`，存储客户端地址。
- `addrlen` 输入时为 `addr` 缓冲区大小，输出时为实际地址大小。

**返回值**：

成功时返回新的已连接套接字描述符，失败时返回 -1 并设置 `errno`：

- `EBADF` 无效的文件描述符。
- `EMFILE` 文件描述符数量已达上限。
- `ECONNABORTED` 连接被中止。
- `EINTR` 被信号中断。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### accept4

```c
int accept4(int sockfd, struct sockaddr *addr, socklen_t *addrlen, int flags);
```

与 `accept()` 相同，但可通过 `flags` 设置新套接字的属性。

**参数**：

- `sockfd` 监听套接字文件描述符。
- `addr` 客户端地址（可为 `NULL`）。
- `addrlen` 地址长度。
- `flags` 标志位：
  - `SOCK_NONBLOCK` 新套接字设为非阻塞。
  - `SOCK_CLOEXEC` 新套接字设为 exec 时关闭。

**返回值**：

同 `accept()`。

**POSIX 兼容性**：兼容 Linux 扩展接口（非 POSIX 标准）。

## 数据发送

### send

```c
ssize_t send(int sockfd, const void *buf, size_t len, int flags);
```

在已连接的套接字上发送数据。等价于 `sendto()` 不指定目标地址。

**参数**：

- `sockfd` 已连接的套接字文件描述符。
- `buf` 要发送的数据缓冲区。
- `len` 数据长度（字节）。
- `flags` 发送标志：
  - `MSG_DONTWAIT` 非阻塞发送。
  - `MSG_NOSIGNAL` 对端关闭时不产生 `SIGPIPE`。
  - `0` 默认行为。

**返回值**：

成功时返回发送的字节数，失败时返回 -1 并设置 `errno`：

- `EBADF` 无效的文件描述符。
- `ENOTCONN` 套接字未连接。
- `EAGAIN` / `EWOULDBLOCK` 非阻塞模式下发送缓冲区满。
- `EPIPE` 对端已关闭连接。
- `EINTR` 被信号中断。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### sendto

```c
ssize_t sendto(int sockfd, const void *buf, size_t len, int flags,
               const struct sockaddr *to, socklen_t tolen);
```

发送数据到指定地址。主要用于 UDP 套接字，也可用于已连接的 TCP 套接字（此时忽略目标地址）。

**参数**：

- `sockfd` 套接字文件描述符。
- `buf` 数据缓冲区。
- `len` 数据长度。
- `flags` 发送标志（同 `send()`）。
- `to` 目标地址。对于已连接套接字可为 `NULL`。
- `tolen` 目标地址长度。

**返回值**：

成功时返回发送的字节数，失败时返回 -1 并设置 `errno`（同 `send()`，另加）：

- `EDESTADDRREQ` 未连接的套接字且未指定目标地址。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### sendmsg

```c
ssize_t sendmsg(int sockfd, const struct msghdr *msg, int flags);
```

通过 `msghdr` 结构发送数据，支持分散/聚集 I/O 和辅助数据（如文件描述符传递）。

**参数**：

- `sockfd` 套接字文件描述符。
- `msg` 消息头结构体，包含目标地址、I/O 向量、辅助数据等。
- `flags` 发送标志。

**返回值**：

成功时返回发送的字节数，失败时返回 -1 并设置 `errno`。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

## 数据接收

### recv

```c
ssize_t recv(int sockfd, void *buf, size_t len, int flags);
```

从已连接的套接字接收数据。

**参数**：

- `sockfd` 已连接的套接字文件描述符。
- `buf` 接收缓冲区。
- `len` 缓冲区大小（字节）。
- `flags` 接收标志：
  - `MSG_DONTWAIT` 非阻塞接收。
  - `MSG_PEEK` 查看数据但不移除。
  - `MSG_WAITALL` 等待接收完整的 `len` 字节。
  - `0` 默认行为。

**返回值**：

成功时返回接收的字节数（0 表示对端关闭连接），失败时返回 -1 并设置 `errno`：

- `EBADF` 无效的文件描述符。
- `ENOTCONN` 套接字未连接。
- `EAGAIN` / `EWOULDBLOCK` 非阻塞模式下无数据可读。
- `EINTR` 被信号中断。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### recvfrom

```c
ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags,
                 struct sockaddr *from, socklen_t *fromlen);
```

接收数据并获取发送方地址。主要用于 UDP 套接字。

**参数**：

- `sockfd` 套接字文件描述符。
- `buf` 接收缓冲区。
- `len` 缓冲区大小。
- `flags` 接收标志（同 `recv()`）。
- `from` 如果非 `NULL`，存储发送方地址。
- `fromlen` 输入时为 `from` 缓冲区大小，输出时为实际地址大小。

**返回值**：

成功时返回接收的字节数，失败时返回 -1 并设置 `errno`（同 `recv()`）。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### recvmsg

```c
ssize_t recvmsg(int sockfd, struct msghdr *msg, int flags);
```

通过 `msghdr` 结构接收数据，支持分散/聚集 I/O 和辅助数据。

**参数**：

- `sockfd` 套接字文件描述符。
- `msg` 消息头结构体。
- `flags` 接收标志。

**返回值**：

成功时返回接收的字节数，失败时返回 -1 并设置 `errno`。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

## 套接字选项

### setsockopt

```c
int setsockopt(int sockfd, int level, int option, const void *value, socklen_t value_len);
```

设置套接字选项。

**参数**：

- `sockfd` 套接字文件描述符。
- `level` 选项所在的协议层：
  - `SOL_SOCKET` 套接字层选项。
  - `IPPROTO_TCP` TCP 层选项。
  - `IPPROTO_IP` IP 层选项。
  - `IPPROTO_IPV6` IPv6 层选项。
- `option` 选项名称（如 `SO_REUSEADDR`、`SO_KEEPALIVE`、`TCP_NODELAY` 等）。
- `value` 选项值。
- `value_len` 选项值的大小。

**返回值**：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EBADF` 无效的文件描述符。
- `ENOPROTOOPT` 不支持的选项。
- `EINVAL` 选项值无效。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### getsockopt

```c
int getsockopt(int sockfd, int level, int option, void *value, socklen_t *value_len);
```

获取套接字选项。

**参数**：

- `sockfd` 套接字文件描述符。
- `level` 协议层（同 `setsockopt()`）。
- `option` 选项名称。
- `value` 存储选项值的缓冲区。
- `value_len` 输入时为缓冲区大小，输出时为实际值大小。

**返回值**：

成功时返回 0，失败时返回 -1 并设置 `errno`（同 `setsockopt()`）。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

## 地址查询

### getsockname

```c
int getsockname(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
```

获取套接字绑定的本地地址。

**参数**：

- `sockfd` 套接字文件描述符。
- `addr` 存储本地地址的缓冲区。
- `addrlen` 输入时为缓冲区大小，输出时为实际地址大小。

**返回值**：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EBADF` 无效的文件描述符。
- `EINVAL` `addrlen` 无效。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

### getpeername

```c
int getpeername(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
```

获取已连接套接字的远程地址。

**参数**：

- `sockfd` 已连接的套接字文件描述符。
- `addr` 存储远程地址的缓冲区。
- `addrlen` 输入时为缓冲区大小，输出时为实际地址大小。

**返回值**：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EBADF` 无效的文件描述符。
- `ENOTCONN` 套接字未连接。

**POSIX 兼容性**：兼容 POSIX/BSD 同名接口。

## DNS 接口

头文件：`#include <nuttx/net/dns.h>`

### dns_add_nameserver

```c
int dns_add_nameserver(const struct sockaddr *addr, socklen_t addrlen);
```

添加一个 DNS 名称服务器。

**参数**：

- `addr` DNS 服务器地址（`struct sockaddr_in` 或 `struct sockaddr_in6`）。
- `addrlen` 地址结构体大小。

**返回值**：

成功时返回 0，失败时返回负的错误码。

**POSIX 兼容性**：openvela/NuttX 扩展接口。

### dns_default_nameserver

```c
int dns_default_nameserver(void);
```

重置 DNS 解析器，仅使用默认 DNS 服务器。

**返回值**：

成功时返回 0，失败时返回负的错误码。

**POSIX 兼容性**：openvela/NuttX 扩展接口。

### dns_foreach_nameserver

```c
int dns_foreach_nameserver(dns_callback_t callback, void *arg);
```

遍历所有已配置的 DNS 服务器，对每个服务器调用回调函数。

**参数**：

- `callback` 回调函数，对每个 DNS 服务器调用。
- `arg` 传递给回调函数的用户参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

**POSIX 兼容性**：openvela/NuttX 扩展接口。

### dns_register_notify

```c
int dns_register_notify(dns_callback_t callback, void *arg);
```

注册 DNS 服务器变更通知。当 DNS 服务器列表发生变化时，调用回调函数。

**参数**：

- `callback` 变更通知回调函数。
- `arg` 传递给回调函数的用户参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

**POSIX 兼容性**：openvela/NuttX 扩展接口。

### dns_unregister_notify

```c
int dns_unregister_notify(dns_callback_t callback, void *arg);
```

取消 DNS 服务器变更通知注册。

**参数**：

- `callback` 之前注册的回调函数。
- `arg` 注册时提供的用户参数。

**返回值**：

成功时返回 0，失败时返回负的错误码。

**POSIX 兼容性**：openvela/NuttX 扩展接口。

### dns_set_queryfamily

```c
int dns_set_queryfamily(sa_family_t family);
```

设置 DNS 查询使用的地址族。

**参数**：

- `family` 地址族（`AF_INET`、`AF_INET6` 或 `AF_UNSPEC`）。

**返回值**：

成功时返回 0，失败时返回负的错误码。

**POSIX 兼容性**：openvela/NuttX 扩展接口。
