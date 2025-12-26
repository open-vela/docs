# iperf3

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/network/network_tools/iperf3.md) \]

## I. Overview

openvela provides the network performance testing tool iperf3, which functions similarly to iperf2 and supports the following features:

- Measure the bandwidth quality of TCP and UDP.
- Measure the maximum bandwidth of TCP and UDP.
- Statistics on bandwidth, delay jitter and data packet loss.

Compared with iperf2, the main optimization points of iperf3 are:

- A single server can support both TCP and UDP client side connections.

## II. Configuration instructions

When using the iperf3 tool, the following options need to be enabled in the configuration file:

```Makefile
CONFIG_UTILS_IPERF3=y
CONFIG_UTILS_IPERF3_PRIORITY=89
```

### 1. Configuration precautions

- mutual exclusion of perf2 and iperf3:

    iperf2 and iperf3 can only choose one of them for compilation, and enabling it at the same time will cause symbol conflicts.

- Priority setting:

    The value of `CONFIG_UTILS_IPERF3_PRIORITY` needs to be lower than the priority of the network interface card driver thread, otherwise it may cause the UDP client side to behave abnormally. Usually, setting it to 89 can meet the needs of most scenarios.

## III. Operation and use

### 1. Parameter description

#### common parameters

The following are the commonly used parameters of iperf3 and their functional descriptions:

- `-f [k | m | K | M]`: Specifies the units in which the report is displayed.

    - `k` and`m `are displayed in Kbits and Mbits.
    - `K` and`M `are displayed in KBytes and MBytes.
    - The default unit is Mbits.
    - Example:

        ```Bash
        iperf3 -c 192.0.2.1 -f K
        ```

- `-i sec`: Specifies the reporting interval in seconds.

    - Example:

        ```Bash
        iperf3 -c 192.0.2.1 -i 2
        ```

    - Note: When the client side sends data, the server side shows the receiving rate. It is recommended to use the `-i` parameter to track rate changes.

- `-p`: Specifies the port used by the server side or the port connected by the client side.

    - Example:

        ```Bash
        iperf3 -s -4 -p 5201  
        iperf3 -c 192.0.2.1 -p 5201
        ```

- `-B`: Bind to the specified host address or interface (for multi-address or multi-interface hosts).

#### server level specific parameters

- `-D`: Run iperf3 as a service.

- Example:

    ```Bash
    iperf3 -s -D  
    ```

- `-1`: Automatically exit after being connected once by the client side.

- `-4/-6`: Listens to IPv4 or IPv6 addresses (IPv6 listens by default).

#### client side specific parameters

- `-u`: UDP protocol is used.
- `t sec`: Specifies the test time (default 10 seconds).

    - Example:

        ```Bash
        iperf3 -c 192.0.2.1 -t 5
        ```

- `-n bytes`: Specifies the number of bytes to transfer.

    - Example:

        ```Bash
        iperf3 -c 192.0.2.1 -n 100000
        ```

- `-b bandwidth`: Specifies the transmission bandwidth (default UDP bandwidth is 1 Mbit/s).

- `--bidir`: Simultaneous two-way transmission test.

- `-l size`: Specifies the buffer size.

    - Example:

        ```Bash
        iperf3 -c 192.0.2.1 -l 16
        ```

    - Note: It can be tested by adjusting the package length.

- `-w size`: Specifies the TCP window size. Too small a window may cause packet loss.
- `-P N`: Specify the number of concurrent connections and initiate N simultaneous connections.
- `-M size`: Sets the MSS (maximum segment size) of the TCP data packet.
- `-N`: Enable TCP non-delay mode.

### 2. Start the server level

Run the following command to set up a regular socket server:

> **Note**: Need to specify '-4' or '-6'.

- Listening to IPv4:

    ```Bash
    # listening IPv4
    iperf3 -s -4 -i 1 -B 127.0.0.1 -p 5201
    ```

### 3. Start the client side and connect to the server level

Run the following command to establish a regular socket client and connect to the specified server:

```Bash
Iperf3 -c 192.0.2.1 -i 1 -p 5201
```

### 4. Precautions

- Cross-core fluxing (usrsock) issue. If you encounter the following tips:

    ```Plain
    ERROR: Request %d too large!  
    ```

    Note: The data of a single call is too long (mainly found in TCP). The length of a single data packet can be reduced by reducing the value of the `-l` parameter to avoid problems.

- Termination of the background startup process:

    If you start in the background mode (add `&` at the end of the command), you can terminate the process with the following command:

    ```Bash
    kill -2 <iperf3 pid>  
    ```

This operation is equivalent to pressing `Ctrl + C`.

## IV. Test output analysis

The following is the raw test data output by iperf3. The measured speed in the SIM card environment is usually faster than the actual device.

### 1. Field description

- Interval: The time interval for data transmission.
- Transfer: The amount of data transferred during that time interval.
- Bitrate: The transfer rate within that time interval.

### 2. Example output

Here is an example of running the command:

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

## V. FAQ

### 1. Version compatibility issues

- openvela compatible version:

    The current openvela compatible version of iperf3 is 3.11.

- Ubuntu Common Version:

    The common iperf3 version on Ubuntu is 3.9, which can usually be used normally.

- Windows version issues:

    - Avoid using the 3.1.3 version (released in 2016), the following incompatibility issues may occur: When specifying the amount of data with the `-n` parameter, the program may exit abnormally after 50 seconds.
    - It is recommended to download and use version 3.11.
