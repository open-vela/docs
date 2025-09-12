# iperf

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/network/network_tools/iperf.md) \]

## I. Overview

The built-in iperf in openvela is a lightweight network performance testing tool compatible with **iperf2**. It supports:

- Measuring TCP/UDP bandwidth quality.

- Testing performance of local sockets and rpmsg sockets.

## II. Configuration Instructions

Enable the following options in the configuration file when using iperf:

> **Note**: Ensure the network interface name is correct (e.g., `eth0`).

```Makefile
CONFIG_NETUTILS_IPERF=y
CONFIG_NETUTILS_IPERFTEST_DEVNAME="eth0"
```

## III. Usage

### 1. General Parameters

iperf supports the following parameters:

```Bash
# Set report interval (seconds).  
# Example: iperf -c 222.35.11.23 -i 2  
# Note: Client shows sending rate; server shows receiving rate.  
-i <sec>  

# Specify server port or client connection port.  
# Example: iperf -s -p 9999; iperf -c 222.35.11.23 -p 9999  
-p <port>  

# Set test duration (default: 30 seconds).  
# Example: iperf -c 222.35.11.23 -t 5  
-t <time>  

# Use UDP protocol.  
-u  

# Terminate all running iperf instances.  
# Note: Use -a to stop background iperf processes started with "&".  
-a  

# Test local sockets.  
--local  

# Test rpmsg sockets.  
--rpmsg
```

### 2. Starting a Server

- Regular Socket Server:

    ```Bash
    iperf -s -i 1 [-u]
    ```

- rpmsg Socket Server:

    ```Bash
    iperf -s --rpmsg <name>
    ```

    - `<name>`: Arbitrary string (must match client's `name`).
    - DGRAM mode (`-u`) is not supported for rpmsg sockets.

- Local Socket Server:

    ```Bash
    iperf -s --local <path> [-u]
    ```

    - `<path>`: Arbitrary string (must match client's `path`).
    - Use `-u` for DGRAM mode (similar to UDP).

### 3. Create a client and connect to the server

#### 3.1 Regular socket client

Use the following command to set up a regular socket client and connect to the server with the IP address < server IP >:

```Bash
iperf -c <server IP> -i 1 [-u]
```

> **Note**: iperf's UDP client has no termination information, so the UDP server does not stop automatically.
After the test, you need to manually press `Ctrl + C` to stop.

#### 3.2 rpmsg socket client

Use the following command to create an rpmsg socket client and connect to the rpmsg socket server:

```Bash
Iperf -c < cpu > --rpmsg < name >
```

- `<cpu>`: The corresponding CPU Core name for running the server service (e.g.`ap`,`cp`,` audio `,`sensor `, etc.).
- `< name >`: Any string, as long as it matches the`name`specified by the server.

#### 3.3 local socket client

Use the following command to establish a local socket client and connect to the local socket server:

```Bash
iperf -c <path> --local [-u]
```

- `< path >`: Any string, as long as it matches the`path `specified by the server.
- `-u`: Can be used with the `-u` parameter to test DGRAM mode, similar to UDP for ordinary sockets.
- After the test, the server needs to manually press `Ctrl + C` to stop.

## IV. Interpretation of the results

The following is the original data source of the'iperf 'output. It is important to note that the test speed on the emulator (sim) may be faster than the actual device.

Result field description:

- Interval: The time of sending (interval).
- Transfer: The amount (size) of data sent during that time period.
- Bandwidth: Transfer speed.

### 1. Regular socket test sample

Run the following command for a regular socket test:

```Bash
ap> iperf -c 10.0.1.1
```

Output example:

```Bash
IP: 10.0.1.2

mode=tcp-client sip=10.0.1.2:5001,dip=10.0.1.1:5001, interval=3, time=30

           Interval         Transfer         Bandwidth

   0.00-   3.00 sec  214548480 Bytes  571.87 Mbits/sec
   3.00-   6.00 sec  215924736 Bytes  575.53 Mbits/sec
   6.00-   9.00 sec  212123648 Bytes  565.20 Mbits/sec
iperf exit
```

### 2. rpmsg socket test sample

#### Server side

Run the following command to start the rpmsg socket server:

```Bash
audio> iperf -s --rpmsg test &
```

Output example:

```Bash
mode=rpmsg-tcp-server cpu=, name=test, interval=3, time=0
accept: cpu=ap,name=test:0

           Interval         Transfer         Bandwidth

   0.00-   3.00 sec   50416788 Bytes  134.33 Mbits/sec
   3.00-   6.00 sec   50677016 Bytes  134.99 Mbits/sec
   6.00-   9.00 sec   50187208 Bytes  133.66 Mbits/sec
iperf exit
```

#### Client side

Run the following command to start the rpmsg socket client:

```Bash
ap> iperf -c audio --rpmsg test
```

Output example:

```Bash
mode=rpmsg-tcp-client cpu=audio, name=test, interval=3, time=30

           Interval         Transfer         Bandwidth

   0.00-   3.00 sec   50429952 Bytes  134.31 Mbits/sec
   3.00-   6.00 sec   50675712 Bytes  134.98 Mbits/sec
   6.00-   9.00 sec   50200576 Bytes  133.64 Mbits/sec
iperf exit
```

### 3. local socket test sample

Start the server and client simultaneously on the same device for local socket testing.

#### Server side

Run the following command to start the local socket server:

```Bash
ap> iperf -s --local test &
```

#### Client

Run the following command to start the local socket client:

```Bash
ap> iperf -c test --local
```

Output example:

```Bash
mode=local-tcp-server path=test, interval=3, time=0
mode=local-tcp-client path=test, interval=3, time=30
accept: path=test

           Interval         Transfer         Bandwidth
           Interval         Transfer         Bandwidth

  -0.00-   3.00 sec  103940096 Bytes  276.97 Mbits/sec
  -0.00-   3.00 sec  103948288 Bytes  276.98 Mbits/sec
   3.00-   6.00 sec  104235008 Bytes  277.65 Mbits/sec
iperf exit
closed by the peer: path=test
iperf exit
```
