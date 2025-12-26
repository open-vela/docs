# iperf2

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/network/network_tools/iperf2.md) \]

## I. Overview

openvela comes with its own network performance testing tool, iperf2, which is compatible with iperf and supports the following features:

- Measure the bandwidth quality of TCP and UDP.
- Measure the maximum bandwidth of TCP and UDP.
- Statistics on bandwidth, delay jitter and data packet loss.

## II. Configuration instructions

When using the iperf2 tool, the following options need to be enabled in the configuration file:

```Makefile
CONFIG_UTILS_IPERF2=y
```

## III. Operation and use

### 1. Parameter description

#### common parameters

iperf2 supports a variety of parameter settings. The following are common parameters and their descriptions:

- `-f [k | m | K | M]`: Specifies the units in which the report is displayed.
    - `k` and`m `are displayed in Kbits and Mbits.
    - `K` and`M `are displayed in KBytes and MBytes.
    - The default unit is Mbits.
    - Example:

        ```Bash
            iperf2 -c 192.0.2.1 -i 2
        ```

- `-i sec`: Specifies the reporting interval in seconds.

    - Example:

        ```Bash
            iperf2 -c 192.0.2.1 -l 16
        ```

    - Description:
        - Client displays the sending rate.
        - Server side display reception rate.
        - It is recommended to use the `-i` parameter for rate tracking.

- `-l size`: Specifies the buffer size (default 16 KB).

    - Example:

        ```Bash
            iperf2 -c 192.0.2.1 -l 16
        ```

    - Description: It can be tested by adjusting the package length.

- `-m`: Displays the maximum MTU value of TCP.

- `-o file`: Outputs reports and error messages to the specified file.

    - Example:

    ```Bash
        iperf2 -c 192.0.2.1 -o /secure/path/iperflog.txt
    ```

- `p port`: Specifies the port used by the server or the port to which the client side is connected.

    - Example:

        ```Bash
            iperf2 -s -p 5001  
            iperf2 -c 192.0.2.1 -p 5001
        ```

- `-u`: UDP protocol is used.
    - Description: When testing physical or driver bandwidth, it is recommended to use the UDP protocol, which has low communication overhead and more accurate test results.

- `-w size`: Specifies the TCP window size (default 16 KB).
    - Description: Windows that are too small may cause packet loss.

- `-B address`: Bind to the specified host address or interface (for multi-address or multi-interface hosts).

- `-C`: Compatible with older versions (used when the Server and Client versions are inconsistent).

- `-M size`: Sets the MSS (maximum segment size) of the TCP data packet.

- `-N`: Enable TCP non-delay mode.

- `-V`: Transmit IPv6 data packets.

#### server level specific parameters

- `-D`: Run iperf2 as a server.

    - Example:

        ```Bash
        iperf2 -s -D -B 127.0.0.1 -p 5001
        ```

- `-R`: Stop the iperf2 service (applies to the '-D' parameter).

    - Example:

        ```Bash
        iperf2 -s -R
        ```

#### client side specific parameters

- `-d`: Simultaneous two-way transmission test (two sockets: one to send, one to receive).

- `--full-duplex`: Two-way transmission test in a single socket.

- `-n bytes`: Specifies the number of bytes to transfer.

    - Example:

        ```Bash
        iperf2 -c 192.0.2.1 -n 100000 -p 5001
        ```

- `-r`: Separate two-way transmission test.

- `-b bandwidth`: Specifies the transmission bandwidth (default 1 Mbit/s).

    - Description: This parameter is very useful when testing QoS.

- `t sec`: Specifies the test time (default 10 seconds).

    - Example:

        ```Bash
        iperf2 -c 192.0.2.1 -t 5 -p 5001
        ```

    - Description: This parameter is only used on the Client side, and the Server side does not need to add the `-t` parameter.

- `-F file`: Specifies the file to be transferred.
- `-T ttl`: Specifies the TTL value.

### 2. Start the server level

Run the following command to set up a regular socket server:

```Bash
iperf2 -s -i 1 -B 127.0.0.1
```

### 3. Start the client side and connect to the server level

Run the following command to establish a regular socket client and connect to the specified server:

```Bash
iperf2 -c <server IP> -i 1
```

#### Test optimization suggestions

When using iperf2 for throughput testing, the following parameters are recommended for optimization:

- `-l`: Set the receive/send buffer size.
- `-w`: Set the TCP window size.
- `-b`: Set the maximum transmission bandwidth of UDP.

### 4. Precautions

When using iperf2, please note the following to avoid potential problems:

- Avoid launching multiple iperf2 instances simultaneously.

    Due to the particularity of RTOS, do not start two iperf2 in the same openvela instance at the same time, otherwise you may cause problems such as crashes.

- Termination of the background startup process:

    If you start in the background mode (with '&' at the end of the command), you can terminate the process with the following command:

    ```Bash
    kill -2 <iperf2 pid>
    ```

    This operation is equivalent to pressing `Ctrl + C`.

- Cross-core turbulence (usrsock) issues:

    If you encounter the following prompt:

    ```Bash
    ERROR: Request %d too large!
    ```

    Description: The data of a single call is too long (mainly found in TCP). The length of a single data packet can be reduced by reducing the value of the '-l' parameter to avoid problems.

- Server-side `-t` parameter limitations:

    Setting an overly large `-t` parameter value (longer than 4294 seconds) on the iperf2 Server side may trigger a bug.

    - Solution: Only set the `-t` parameter on the Client side, not on the Server side.

## IV. Test output analysis

The following is the raw test data output by iperf2. The measured speed in the SIM card environment is usually faster than the actual device.

### 1. Field description

- Interval: The time interval for data transmission.
- Transfer: The amount of data transferred during that time     interval.
- Bandwidth: The transfer rate (bandwidth) within that time interval.

### 2. Example output

The following is an example of the output of the running command:

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
