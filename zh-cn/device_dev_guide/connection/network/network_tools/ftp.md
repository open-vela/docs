# ftp

\[ [English](../../../../../en/device_dev_guide/connection/network/network_tools/ftp.md) | 简体中文 \]

## 一、概述

- 文件传输协议（File Transfer Protocol，FTP）是一种用于在网络上进行文件传输的标准协议。它工作在 OSI 模型的第七层（应用层）和 TCP 模型的第四层，使用 TCP 进行传输，而非 UDP。

- 在建立连接前，客户端与服务器需要经过“三次握手”过程，以确保连接的可靠性和面向连接的特性，从而为数据传输提供可靠保障。

- FTP 允许用户通过文件操作（如增、删、改、查、传送等）与另一台主机进行通信。用户无需完全登录到目标计算机即可访问远程资源。通过 FTP 程序，用户可以实现文件传输、目录管理等操作，即使双方计算机的操作系统和文件存储方式不同。

- `ftpd` 是提供 FTP 服务的服务器端程序。

## 二、配置说明

使用 FTP 工具时，需要在配置文件中启用以下选项：

```Makefile
CONFIG_EXAMPLES_FTPD=y
CONFIG_NETUTILS_FTPD=y
CONFIG_NET_TCPBACKLOG=y
```

## 三、操作使用

`openvela` 端的 FTP 功能仅提供两条不带参数的命令，具体功能如下：

```Shell
# 开启ftpd服务，并预置三个可供登陆的用户
ftpd_start -4

# 关闭ftpd服务
ftpd_stop
```

当 `host` 端连接到 FTP 服务后，支持以下命令：

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

## 四、常见用法

以下是常用的操作流程及其说明。

### 1、在搭载 openvela 的设备上启动 FTP 服务

使用以下命令启动 `ftpd` 服务：

```Bash
ap> ftpd_start -4
Initializing the network
Starting the FTP daemon
FTP daemon [223] started

# 后续PC连接时使用如下用户名和密码做身份认证
Adding accounts:  
```

**注意**：

- 上述用户名和密码仅为示例，请在实际使用中设置强密码，避免使用默认密码。
- 建议为 `root` 用户设置复杂密码，并禁用匿名用户（`anonymous`）访问，以提升安全性。

### 2、在 PC 端连接设备并下载文件

使用以下命令从设备下载文件：

```Bash
# PC端执行"ftp <设备实际 IP>"连接到openvela
# 示例 IP 地址为 192.168.28.94，请根据实际网络环境替换。  
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

# 下载文件 persist.db，并将其保存为 persist.db.pc
ftp> get persist.db persist.db.pc 
local: persist.db.pc remote: persist.db
200 PORT command successful
150 Opening data connection
226 Transfer complete
12288 bytes received in 0.01 secs (959.3860 kB/s)
ftp> 
```

### 3、在 PC 端上传文件到设备

使用以下命令将文件上传到设备：

```Bash
# 上传文件 persist.db.pc，并将其保存为 persist.db.dev                                   
ftp> put persist.db.pc persist.db.dev    
local: persist.db.pc remote: persist.db.dev
200 PORT command successful
150 Opening data connection
226 Transfer complete
12288 bytes sent in 0.00 secs (127.3777 MB/s)
ftp> pwd
257 "/data" is current directory.
```
