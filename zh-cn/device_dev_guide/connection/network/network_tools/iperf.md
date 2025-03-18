# iperf

## 一、概述

openvela 自带的 iperf 是一款轻量级的网络性能测试工具，与 **iperf2** 兼容。它支持以下功能：

- 测量 TCP 和 UDP 的带宽质量。
- 测试 **local socket** 和 **rpmsg socket** 的性能。

## 二、配置说明

使用 iperf 工具时，需要在配置文件中启用以下选项：

> 说明
>
> 请确保网卡名称正确，例如：`eth0`。

```Makefile
CONFIG_NETUTILS_IPERF=y
CONFIG_NETUTILS_IPERFTEST_DEVNAME="eth0"
```

## 三、操作使用

### 1、iperf 通用参数说明

iperf 支持以下参数设定：

```Bash
# 设置报告间隔时间（单位：秒）。  
# 示例：iperf -c 222.35.11.23 -i 2  
# 说明：client 向 server 发送数据，client 显示发送速率，server 显示接收速率。  
-i <sec>  

# 指定服务器端使用的端口或客户端连接的端口。  
# 示例：iperf -s -p 9999; iperf -c 222.35.11.23 -p 9999  
-p <port>  

# 设置测试时间，默认 30 秒。  
# 示例：iperf -c 222.35.11.23 -t 5  
-t <time>  

# 使用 UDP 协议。  
-u  

# 关闭所有正在运行的 iperf 实例。  
# 说明：有时命令后加 "&" 以后台运行，使用 -a 参数可退出后台运行的 iperf。  
-a  

# 测试 local socket。  
--local  

# 测试 rpmsg socket。  
--rpmsg
```

### 2、建立 server

- 建立常规 socket server 指令：

    ```Bash
    iperf -s -i 1 [-u]
    ```

- 建立 rpmsg socket server 指令：

    ```Bash
    iperf -s --rpmsg <name>
    ```

    - `<name>` 为任意字符串，只需与 client 指定的 `name` 匹配即可。

    - rpmsg socket 暂时不支持 DGRAM 模式（`-u`）。

- 建立 local socket server 指令：

    ```Bash
    iperf -s --local <path> [-u]
    ```

    - `<path>` 为任意字符串，只需与 client 指定的 `path` 匹配即可。

    - local socket 可以搭配 `-u` 参数测试 DGRAM 模式（类似于 UDP）。

### 3、建立 client 并连接 server

#### 3.1 常规 socket client

使用以下指令建立常规 socket client，并连接 IP 地址为 `<server IP>` 的 server：

```Bash
iperf -c <server IP> -i 1 [-u]
```

> 说明
>
> - iperf 的 UDP client 没有终止信息，因此 UDP server 不会自动停止。
> - 测试结束后需手动按 `Ctrl+C` 停止。

#### 3.2 rpmsg socket client

使用以下指令建立 rpmsg socket client，并连接 rpmsg socket server：

```Bash
iperf -c <cpu> --rpmsg <name> 
```

- `<cpu>`：运行 server 服务的对应 CPU Core 名称（如 `ap`、`cp`、`audio`、`sensor` 等）。
- `<name>`：任意字符串，只需与 server 指定的 `name` 匹配即可。

#### 3.3 local socket client

使用以下指令建立 local socket client，并连接到 local socket server：

```Bash
iperf -c <path> --local [-u]
```

- `<path>`：任意字符串，只需与 server 指定的 `path` 匹配即可。
- `-u`：可搭配 `-u` 参数测试 DGRAM 模式，类似于普通 socket 的 UDP。
- 测试结束后，server 端需要手动按 `Ctrl+C` 停止。

## 四、结果解读

以下是 `iperf` 输出的原始数据。需要注意的是，在模拟器（sim）上测试的速度可能会比实际设备快。

结果字段说明：

- Interval：发送的时间（间隔）。
- Transfer：该时间段内发送的数据量（大小）。
- Bandwidth：传输速度。

### 4.1 常规 socket 测试样例

运行以下命令进行常规 socket 测试：

```C
ap> iperf -c 10.0.1.1
```

输出示例：

```Bash
IP: 10.0.1.2

mode=tcp-client sip=10.0.1.2:5001,dip=10.0.1.1:5001, interval=3, time=30

           Interval         Transfer         Bandwidth

   0.00-   3.00 sec  214548480 Bytes  571.87 Mbits/sec
   3.00-   6.00 sec  215924736 Bytes  575.53 Mbits/sec
   6.00-   9.00 sec  212123648 Bytes  565.20 Mbits/sec
   9.00-  12.00 sec  211337216 Bytes  563.16 Mbits/sec
  12.00-  15.00 sec  209879040 Bytes  559.48 Mbits/sec
  15.00-  18.00 sec  213614592 Bytes  569.18 Mbits/sec
  18.00-  21.01 sec  202752000 Bytes  540.54 Mbits/sec
  21.01-  24.01 sec  212074496 Bytes  565.26 Mbits/sec
  24.01-  27.01 sec  215318528 Bytes  573.83 Mbits/sec
  27.01-  30.01 sec  213467136 Bytes  568.89 Mbits/sec
   0.00-  30.01 sec 2121089024 Bytes  565.46 Mbits/sec
iperf exit
```

### 4.2 rpmsg socket 测试样例

#### Server 端

运行以下命令启动 rpmsg socket server：

```Bash
audio> iperf -s --rpmsg test &
```

输出示例：

```C
mode=rpmsg-tcp-server cpu=, name=test, interval=3, time=0
accept: cpu=ap,name=test:0

           Interval         Transfer         Bandwidth

   0.00-   3.00 sec   50416788 Bytes  134.33 Mbits/sec
   3.00-   6.00 sec   50677016 Bytes  134.99 Mbits/sec
   6.00-   9.00 sec   50187208 Bytes  133.66 Mbits/sec
   9.00-  12.00 sec   50638624 Bytes  135.00 Mbits/sec
  12.00-  15.00 sec   50550672 Bytes  134.66 Mbits/sec
  15.00-  18.00 sec   50515336 Bytes  134.66 Mbits/sec
  18.00-  21.00 sec   50640132 Bytes  134.99 Mbits/sec
  21.00-  24.00 sec   50636260 Bytes  135.00 Mbits/sec
  24.00-  27.00 sec   50548308 Bytes  134.66 Mbits/sec
  27.00-  30.00 sec   50587108 Bytes  134.66 Mbits/sec
iperf exit
```

#### Client 端

运行以下命令启动 rpmsg socket client：

```C
ap> iperf -c audio --rpmsg test
```

输出示例：

```C
mode=rpmsg-tcp-client cpu=audio, name=test, interval=3, time=30

           Interval         Transfer         Bandwidth

   0.00-   3.00 sec   50429952 Bytes  134.31 Mbits/sec
   3.00-   6.00 sec   50675712 Bytes  134.98 Mbits/sec
   6.00-   9.00 sec   50200576 Bytes  133.64 Mbits/sec
   9.00-  12.00 sec   50642944 Bytes  134.98 Mbits/sec
  12.00-  15.00 sec   50561024 Bytes  134.65 Mbits/sec
  15.00-  18.00 sec   50511872 Bytes  134.65 Mbits/sec
  18.00-  21.00 sec   50659328 Bytes  134.98 Mbits/sec
  21.00-  24.00 sec   50642944 Bytes  134.98 Mbits/sec
  24.00-  27.00 sec   50544640 Bytes  134.65 Mbits/sec
  27.00-  30.00 sec   50593792 Bytes  134.65 Mbits/sec
   0.00-  30.00 sec  505462784 Bytes  134.75 Mbits/sec
iperf exit
```

### 4.3 local socket 测试样例

在同一设备上同时启动 server 和 client 进行 local socket 测试。

#### Server 端

运行以下命令启动 local socket server：

```C
ap> iperf -s --local test &
```

#### Client 端

运行以下命令启动 local socket client：

```C
ap> iperf -c test --local
```

输出示例：

```Bash
mode=local-tcp-server path=test, interval=3, time=0
mode=local-tcp-client path=test, interval=3, time=30
accept: path=test

           Interval         Transfer         Bandwidth
           Interval         Transfer         Bandwidth

  -0.00-   3.00 sec  103940096 Bytes  276.97 Mbits/sec
  -0.00-   3.00 sec  103948288 Bytes  276.98 Mbits/sec
   3.00-   6.00 sec  104235008 Bytes  277.65 Mbits/sec
   3.00-   6.00 sec  104225792 Bytes  277.65 Mbits/sec
   6.00-   9.00 sec  103874560 Bytes  276.66 Mbits/sec
   6.00-   9.00 sec  103889920 Bytes  276.98 Mbits/sec
   9.00-  12.00 sec  104677376 Bytes  278.96 Mbits/sec
   9.00-  12.00 sec  104665088 Bytes  278.96 Mbits/sec
  12.00-  15.00 sec  104267776 Bytes  277.98 Mbits/sec
  12.00-  15.00 sec  104274944 Bytes  277.98 Mbits/sec
  15.00-  18.00 sec  104071168 Bytes  277.31 Mbits/sec
  15.00-  18.00 sec  104076288 Bytes  277.31 Mbits/sec
  18.00-  21.00 sec  105037824 Bytes  279.99 Mbits/sec
  18.00-  21.00 sec  105036800 Bytes  279.98 Mbits/sec
  21.00-  24.00 sec  101335040 Bytes  269.98 Mbits/sec
  21.00-  24.00 sec  101327872 Bytes  269.99 Mbits/sec
  24.00-  27.00 sec  103661568 Bytes  276.32 Mbits/sec
  24.00-  27.00 sec  103654400 Bytes  276.31 Mbits/sec
  27.00-  30.00 sec  103022592 Bytes  274.66 Mbits/sec
  27.00-  30.00 sec  103034880 Bytes  274.65 Mbits/sec
  -0.00-  30.00 sec 1038123008 Bytes  276.78 Mbits/sec
iperf exit
closed by the peer: path=test
iperf exit
```
