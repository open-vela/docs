# iperf2

\[ [English](../../../../../en/device_dev_guide/connection/network/network_tools/iperf2.md) | 简体中文 \]

## 一、概述

openvela 自带网络性能测试工具 iperf2，该工具与 iperf 兼容，支持以下功能：

- 测量 TCP 和 UDP 的带宽质量。
- 测量 TCP 和 UDP 的最大带宽。
- 统计带宽、延迟抖动和数据包丢失等信息。

## 二、配置说明

使用 iperf2 工具时，需要在配置文件中启用以下选项：

```Makefile
CONFIG_UTILS_IPERF2=y
```

## 三、操作使用

### 1、参数说明

#### 通用参数

iperf2 支持多种参数设定，以下是常用参数及其说明：

- `-f [k|m|K|M]`：指定报告显示的单位。

    - `k` 和 `m` 表示以 Kbits 和 Mbits 为单位显示。
    - `K` 和 `M` 表示以 KBytes 和 MBytes 为单位显示。
    - 默认单位为 Mbits。
    - 示例：

        ```Bash
        iperf2 -c 192.0.2.1 -f K
        ```

- `-i sec`：指定报告间隔时间（以秒为单位）。

    - 示例：

      ```Bash
      iperf2 -c 192.0.2.1 -i 2
      ```

    - 说明：
        - Client 端显示发送速率。
        - Server 端显示接收速率。
        - 建议使用 `-i` 参数，便于进行速率跟踪。

- `-l size`：指定缓冲区大小（默认 16 KB）。

    - 示例：

        ```Bash
        iperf2 -c 192.0.2.1 -l 16
        ```

    - 说明：可以通过调整包长进行测试。

- `-m`：显示 TCP 最大 MTU 值。

- `-o file`：将报告和错误信息输出到指定文件。

    - 示例：

        ```Bash
        iperf2 -c 192.0.2.1 -o /secure/path/iperflog.txt
        ```

- `-p port`：指定服务器端使用的端口或客户端所连接的端口。

    - 示例：

        ```Bash
        iperf2 -s -p 5001  
        iperf2 -c 192.0.2.1 -p 5001
        ```

- `-u`：使用 UDP 协议。
    - 说明：测试物理或驱动带宽时，建议使用 UDP 协议，其通信开销小，测试结果更准确。

- `-w size`：指定 TCP 窗口大小（默认 16 KB）。

    - 说明：窗口过小可能会导致丢包。

- `-B address`：绑定到指定主机地址或接口（适用于多地址或多接口主机）。

- `-C`：兼容旧版本（当 Server 和 Client 版本不一致时使用）。

- `-M size`：设置 TCP 数据包的 MSS（最大分段大小）。

- `-N`：启用 TCP 不延迟模式。

- `-V`：传输 IPv6 数据包。

#### 服务端专用参数

- `-D`：以服务器方式运行 iperf2。

    - 示例：

        ```Bash
        iperf2 -s -D -B 127.0.0.1 -p 5001
        ```

- `-R`：停止 iperf2 服务（适用于 `-D` 参数）。

    - 示例：

        ```Bash
        iperf2 -s -R
        ```

#### 客户端专用参数

- `-d`：同时进行双向传输测试（两个 socket：一个发送，一个接收）。

- `--full-duplex`：在单个 socket 中进行双向传输测试。

- `-n bytes`：指定传输的字节数。

    - 示例：

        ```Bash
        iperf2 -c 192.0.2.1 -n 100000 -p 5001
        ```

- `-r`：单独进行双向传输测试。

- `-b bandwidth`：指定发送带宽（默认 1 Mbit/s）。

    - 说明：在测试 QoS 时，此参数非常有用。

- `-t sec`：指定测试时间（默认 10 秒）。

    - 示例：

        ```Bash
        iperf2 -c 192.0.2.1 -t 5 -p 5001
        ```

- 说明：仅在 Client 端使用此参数，Server 端无需添加 `-t` 参数。

- `-F file`：指定需要传输的文件。
- `-T ttl`：指定 TTL 值。

### 2、启动服务端

运行以下命令以建立常规 socket server：

```Bash
iperf2 -s -i 1 -B 127.0.0.1
```

### 3、启动客户端并连接服务端

运行以下命令以建立常规 socket client 并连接到指定服务器：

```Bash
iperf2 -c <server IP> -i 1
```

#### 测试优化建议

在使用 iperf2 进行吞吐量（throughput）测试时，建议使用以下参数进行优化：

- `-l`：设定接收/发送缓冲区大小。
- `-w`：设定 TCP 窗口大小（TCP window size）。
- `-b`：设定 UDP 的最大发送带宽。

### 4、注意事项

在使用 iperf2 时，请注意以下事项以避免潜在问题：

- 避免同时启动多个 iperf2 实例：

    由于 RTOS 的特殊性，不要在同一个 openvela 实例中同时启动两个 iperf2，否则可能引发 crash（崩溃）等问题。

- 后台启动进程的终止：

    如果以后台方式启动（命令末尾加 `&`），可以通过以下命令终止进程：

    ```Bash
    kill -2 <iperf2的pid>
    ```

    该操作等同于按下 `Ctrl+C`。

- 跨核打流（usrsock）问题：

    如果遇到以下提示：

    ```Bash
    ERROR: Request %d too large!
    ```

    说明：单次调用的数据过长（主要见于 TCP）。可以通过减小 `-l` 参数值来减少单次发送的数据包长度，从而避免问题。

- Server 端 `-t` 参数的限制：

    在 iperf2 Server 端设置过大的 `-t` 参数值（超过 4294 秒）可能会触发 Bug。

    - 解决方案：仅在 Client 端设置 `-t` 参数，不在 Server 端设置即可。

## 四、测试输出解析

以下是 iperf2 输出的原始测试数据。在 SIM 卡环境下测得的速度通常会比实际设备快一些。

### 1、字段说明

- Interval：数据传输的时间间隔。
- Transfer：该时间间隔内传输的数据量。
- Bandwidth：该时间间隔内的传输速率（带宽）。

### 2、示例输出

以下是运行命令的示例输出：

```Bash
ap> iperf2 -c 192.0.2.1 -i 1
------------------------------------------------------------  
Client connecting to 192.0.2.1, TCP port 5001  
TCP window size: -1.00 Byte (WARNING: requested 16.0 KByte)  
------------------------------------------------------------  
[  1] local 192.0.2.2 port 11053 connected with 192.0.2.1 port 5001
[ ID] Interval       Transfer     Bandwidth  
[  1] 0.00-1.00 sec  49.7 MBytes   416 Mbits/sec  
[  1] 1.00-2.00 sec  50.8 MBytes   425 Mbits/sec  
[  1] 2.00-3.00 sec  51.2 MBytes   429 Mbits/sec  
[  1] 3.00-4.00 sec  50.1 MBytes   420 Mbits/sec  
[  1] 4.00-5.00 sec  50.3 MBytes   421 Mbits/sec  
[  1] 5.00-6.00 sec  49.5 MBytes   415 Mbits/sec  
[  1] 6.00-7.00 sec  51.8 MBytes   434 Mbits/sec  
[  1] 7.00-8.00 sec  50.3 MBytes   421 Mbits/sec  
[  1] 8.00-9.00 sec  49.4 MBytes   414 Mbits/sec  
[  1] 9.00-10.00 sec  51.0 MBytes   428 Mbits/sec  
[  1] 0.00-10.01 sec   504 MBytes   422 Mbits/sec
```
