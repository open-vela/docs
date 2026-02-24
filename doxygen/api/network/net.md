# Network Interfaces

## Network Functions (sys/socket.h)
openvela支持与BSD兼容的套接字接口层，为应用程序开发人员提供熟悉的网络api。这些套接字接口可以通过架构配置文件中的设置来启用。套接字层支持多种协议族，包括IPv4 （AF INET）和IPv6 (AF INET6)，以及各种套接字类型，如流套接字（SOCK stream）、数据报套接字（SOCK DGRAM）和原始套接字。

```eval_rst

.. doxygenfile:: socket.h
  :project: doxygen
```

## DNS Functions (net/dns.h)
openvela提供了用于配置和管理DNS服务器的DNS解析器功能。这些功能定义在nuttx/net/dns.h中，允许应用程序添加、移除和查询DNS名称服务器。

```eval_rst

.. doxygenfile:: dns.h
  :project: doxygen
```

## apps (apps/include)
apps目录下网络的相关接口介绍

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
