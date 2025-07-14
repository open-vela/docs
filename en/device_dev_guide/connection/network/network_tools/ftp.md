# ftpd File Transfer Guide

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/connection/network/network_tools/ftp.md) \]

## I. Overview

- The File Transfer Protocol (FTP) is a standard network protocol for transferring files between computers. It operates at Layer 7 (Application Layer) of the OSI model and Layer 4 of the TCP model, utilizing TCP (not UDP) for reliable connection-oriented data transmission.

- Before establishing a connection, the client and server perform a "three-way handshake" to ensure reliable communication.

- FTP enables users to interact with remote hosts through file operations (upload, download, delete, modify, etc.), even when the operating systems and file storage methods differ between devices.

- `ftpd` is the server-side program that provides FTP services.

## II.Configuration Instructions

Enable the following options in the configuration file to use FTP:

```Makefile
CONFIG_EXAMPLES_FTPD=y
CONFIG_NETUTILS_FTPD=y
CONFIG_NET_TCPBACKLOG=y
```

## III. Usage

The `openvela` FTP implementation provides two parameter-free commands:

```Shell
# Start ftpd service with three preconfigured login accounts
ftpd_start -4

# Stop ftpd service
ftpd_stop
```

After connecting to the FTP service, the `host` end supports the following commands:

```Shell
ftp> ?
Commands may be abbreviated.  Commands are:

!         dir           mdelete   qc         site
$         disconnect    mdir      sendport   size
account   exit          mget      put        status
append    form          mkdir     pwd        struct
ascii     get           mls       quit       system
bell      glob          mode      quote      sunique
binary    hash          modtime   recv       tenex
bye       help          mput      reget      tick
case      idle          newer     rstatus    trace
cd        image         nmap      rhelp      type
cdup      ipany         nlist     rename     user
chmod     ipv4          ntrans    reset      umask
close     ipv6          open      restart    verbose
cr        lcd           rompt     rmdir      ?
delete    ls            passive   runique
debug     macdef        proxy     send
ftp> 
```

## IV. Common Operations

### 1. Starting FTP Service on openvela-Equipped Devices

Start the `ftpd` service with:

```Bash
ap> ftpd_start -4
Initializing the network
Starting the FTP daemon
FTP daemon [223] started

# Use the following credentials for PC connections
Adding accounts:  
```

**Note**：

- Replace default credentials with strong passwords in production environments.

- Disable `anonymous` access and configure complex passwords for the `root` user to enhance security.

### 2. Downloading Files from Device to PC

Download files from the device using:

```Bash
# On PC: Connect via "ftp <Device_IP>" (replace 192.168.28.94 with actual IP)
# The example IP address is 192.168.28.94, please replace it according to the actual network environment.
ftp 192.168.28.94

Connected to 192.168.28.94.
220 NuttX FTP Server
Name (192.168.28.94:usrname): root
331 Password required for root
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> cd data
250 CWD command successful
ftp> pwd
257 "/data" is current directory.
ftp> ls
200 PORT command successful
150 Opening ASCII mode data connection for file list
drw-r--r--   1     1001      512        0 Mar  2 07:44 etc
drwxrwx---   1     1001      512        0 Mar  2 07:44 log
drwxrwx---   1     1001      512        0 Mar  2 07:44 mico
drw-rw-rw-   1     1001      512        0 Mar  2 07:44 miot
drwxrwxrwx   1     1001      512        0 Mar  2 07:44 misc
-rw-r--r--   1     1001      512    12288 Mar  2 07:44 persist.db
226 Transfer complete

# Download persist.db and save as persist.db.pc
ftp> get persist.db persist.db.pc 
local: persist.db.pc remote: persist.db
200 PORT command successful
150 Opening data connection
226 Transfer complete
12288 bytes received in 0.01 secs (959.3860 kB/s)
ftp> 
```

### 3. Uploading Files from PC to Device

Upload files to the device using:

```Bash
 # Upload persist.db.pc and save as persist.db.dev

ftp> put persist.db.pc persist.db.devdev                                      
local: persist.db.pc remote: persist.db.dev
200 PORT command successful
150 Opening data connection
226 Transfer complete
12288 bytes sent in 0.00 secs (127.3777 MB/s)
ftp> pwd
257 "/data" is current directory.
```
