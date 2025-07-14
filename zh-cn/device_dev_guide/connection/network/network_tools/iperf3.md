# iperf3

\[ [English](../../../../../en/device_dev_guide/connection/network/network_tools/iperf3.md) | 简体中文 \]

## 一、概述

openvela 提供了网络性能测试工具 iperf3，其功能与 iperf2 类似，支持以下特性：

- 测量 TCP 和 UDP 的带宽质量。
- 测量 TCP 和 UDP 的最大带宽。
- 统计带宽、延迟抖动和数据包丢失等信息。

与 iperf2 相比，iperf3 的主要优化点是：

- 单个服务器可以同时支持 TCP 和 UDP 客户端连接。

## 二、配置说明

在使用 iperf3 工具时，需要在配置文件中启用以下选项：

```Makefile
CONFIG_UTILS_IPERF3=y
CONFIG_UTILS_IPERF3_PRIORITY=89
```

### 1、配置注意事项

- perf2 和 iperf3 的互斥性： iperf2 和 iperf3 只能选择其中一个进行编译，同时启用会导致符号冲突。
- 优先级设置： `CONFIG_UTILS_IPERF3_PRIORITY` 的值需要低于网卡驱动线程的优先级，否则可能导致 UDP 客户端行为异常。通常情况下，设置为 89 可以满足绝大多数场景的需求。

## 三、操作使用

### 1、参数说明

#### 1.1 通用参数

以下是 iperf3 的常用参数及其功能说明：

- `-f [k|m|K|M]`：指定报告显示的单位。

    - `k` 和 `m` 表示以 Kbits 和 Mbits 为单位显示。

    - `K` 和 `M` 表示以 KBytes 和 MBytes 为单位显示。

    - 默认单位为 Mbits。

    - 示例：

        ```Bash
        iperf3 -c 192.0.2.1 -f K
        ```

- `-i sec`：指定报告间隔时间（以秒为单位）。

    - 示例：

        ```Bash
        iperf3 -c 192.0.2.1 -i 2
        ```

    - 注意：在客户端发送数据时，服务器端显示的是接收速率。建议使用 `-i` 参数跟踪速率变化。

- `-p`：指定服务器端使用的端口或客户端连接的端口。

    - 示例：

        ```Bash
        iperf3 -s -4 -p 5201  
        iperf3 -c 192.0.2.1 -p 5201
        ```

- `-B`：绑定到指定的主机地址或接口（适用于多地址或多接口主机）。

#### 1.2 服务端专用参数

- `-D`：以服务方式运行 iperf3。

    - 示例：

        ```Bash
        iperf3 -s -D  
        ```

- `-1`：被客户端连接一次后自动退出。

- `-4/-6`：监听 IPv4 或 IPv6 地址（默认监听 IPv6）。

#### 1.3 客户端专用参数

- `-u`：使用 UDP 协议。

- `-t sec`：指定测试时间（默认 10 秒）。

    - 示例：

        ```Bash
        iperf3 -c 192.0.2.1 -t 5
        ```

- `-n bytes`：指定传输的字节数。

    - 示例：

        ```Bash
        iperf3 -c 192.0.2.1 -n 100000
        ```

- `-b bandwidth`：指定发送带宽（默认 UDP 带宽为 1 Mbit/s）。

- `--bidir`：同时进行双向传输测试。

- `-l size`：指定缓冲区大小。

    - 示例：

        ```Bash
        iperf3 -c 192.0.2.1 -l 16
        ```

    - 注意：可以通过调整包长进行测试。

- `-w size`：指定 TCP 窗口大小。窗口过小可能会导致丢包。

- `-P N`：指定并发连接数，发起 N 个同时连接。

- `-M size`：设置 TCP 数据包的 MSS（最大分段大小）。

- `-N`：启用 TCP 不延迟模式。

### 2、启动服务端

运行以下命令以建立常规 socket server：

> **注意**：需要指定 `-4` 还是 `-6`。

- 监听 IPv4：

    ```Bash
    # 监听IPv4
    iperf3 -s -4 -i 1 -B 127.0.0.1 -p 5201
    ```

### 3、启动客户端并连接服务端

运行以下命令以建立常规 socket client 并连接到指定服务器：

```Bash
iperf3 -c 192.0.2.1 -i 1 -p 5201
```

### 4、注意事项

- 跨核打流（usrsock）问题。 如果遇到以下提示：

    ```Plain
    ERROR: Request %d too large!  
    ```

    说明：单次调用的数据过长（主要见于 TCP）。可以通过减小 `-l` 参数值来减少单次发送的数据包长度，从而避免问题。

- 后台启动进程的终止： 如果以后台方式启动（命令末尾加 `&`），可以通过以下命令终止进程：

    ```Bash
    kill -2 <iperf3的pid>  
    ```

    该操作等同于按下 `Ctrl+C`。

## 四、测试输出解析

以下是 iperf3 输出的原始测试数据。在 SIM 卡环境下测得的速度通常会比实际设备快一些。

### 1、字段说明

- Interval：数据传输的时间间隔。
- Transfer：该时间间隔内传输的数据量。
- Bitrate：该时间间隔内的传输速率。

### 2、示例输出

以下是运行命令的示例：

```Bash
ap> iperf3 -c 192.0.2.1 -i 1  
Connecting to host 192.0.2.1, port 5201  
[  4] local 192.0.2.2 port 17100 connected to 192.0.2.1 port 5201
[ ID] Interval           Transfer     Bitrate
[  4]   0.00-1.00   sec  37.5 MBytes   313 Mbits/sec                  
[  4]   1.00-2.00   sec  37.0 MBytes   311 Mbits/sec                  
[  4]   2.00-3.00   sec  36.8 MBytes   308 Mbits/sec                  
[  4]   3.00-4.01   sec  35.5 MBytes   296 Mbits/sec                  
[  4]   4.01-5.01   sec  35.5 MBytes   298 Mbits/sec                  
[  4]   5.01-6.00   sec  36.8 MBytes   309 Mbits/sec                  
[  4]   6.00-7.00   sec  36.0 MBytes   302 Mbits/sec                  
[  4]   7.00-8.00   sec  34.4 MBytes   288 Mbits/sec                  
[  4]   8.00-9.00   sec  33.6 MBytes   281 Mbits/sec                  
[  4]   9.00-10.00  sec  33.9 MBytes   284 Mbits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate
[  4]   0.00-10.00  sec   356 MBytes   299 Mbits/sec                  sender
[  4]   0.00-10.02  sec   356 MBytes   298 Mbits/sec                  receiver
```

## 五、FAQ

### 1、版本兼容问题

- openvela 适配版本： 当前 openvela 适配的 iperf3 版本为 3.11。
- Ubuntu 常见版本： Ubuntu 上常见的 iperf3 版本为 3.9，通常能够正常使用。
- Windows 版本问题：
    - 避免使用 3.1.3 版本（发布于 2016 年），可能会出现以下不兼容问题：使用 `-n` 参数指定数据量时，程序可能在 50 秒后异常退出。
    - 建议下载使用 3.11 版本。
