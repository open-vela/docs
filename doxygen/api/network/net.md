# 网络接口详情

## 套接字接口（sys/socket.h）

openvela 支持与 BSD 兼容的套接字接口层，为应用程序开发人员提供熟悉的网络 API。这些套接字接口可以通过架构配置文件中的设置来启用。套接字层支持多种协议族，包括 IPv4（AF_INET）和 IPv6（AF_INET6），以及各种套接字类型，如流套接字（SOCK_STREAM）、数据报套接字（SOCK_DGRAM）和原始套接字。

```eval_rst

.. doxygenfile:: socket.h
    :project: doxygen

```

## DNS 接口（net/dns.h）

openvela 提供了用于配置和管理 DNS 服务器的 DNS 解析器功能。这些功能定义在 nuttx/net/dns.h 中，允许应用程序添加、移除和查询 DNS 名称服务器。

```eval_rst

.. doxygenfile:: dns.h
    :project: doxygen

```

## 应用层接口（apps/include）

apps 目录下网络相关的接口介绍。

### netutils/dhcpc.h

```eval_rst

.. doxygenfile:: dhcpc.h
    :project: doxygen

```

### netutils/dhcp6c.h

```eval_rst

.. doxygenfile:: dhcp6c.h
    :project: doxygen

```

### netutils/dhcpd.h

```eval_rst

.. doxygenfile:: dhcpd.h
    :project: doxygen

```

### netutils/ftpd.h

```eval_rst

.. doxygenfile:: ftpd.h
    :project: doxygen

```

### netutils/netlib.h

```eval_rst

.. doxygenfile:: netlib.h
    :project: doxygen

```

### wireless/wapi.h

```eval_rst

.. doxygenfile:: wapi.h
    :project: doxygen

```
