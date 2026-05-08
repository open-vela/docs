# FTP 服务器 API

简单的 FTP 服务器接口，提供用户管理和会话处理能力。

头文件：`#include <netutils/ftpd.h>`

## openvela 实现说明

- **适用场景**：IoT 设备调试、固件上传、文件下载等轻量 FTP 应用
- **配置依赖**：需启用 `CONFIG_NETUTILS_FTPD`
- **用户管理**：通过 `ftpd_adduser` 添加用户与权限
- **会话模型**：`ftpd_session` 为一个客户端连接提供会话处理，通常在独立线程中调用

## FTP 服务器

头文件：`#include <netutils/ftpd.h>`

### ftpd_open

```c
FTPD_SESSION ftpd_open(int port, sa_family_t family);
```

创建 FTP 服务器会话。

**参数**：

- `port` 监听端口（通常为 21）。
- `family` 地址族（`AF_INET` 或 `AF_INET6`）。

**返回值**：

成功时返回会话句柄。

### ftpd_adduser

```c
int ftpd_adduser(FTPD_SESSION handle, uint8_t accountflags,
                 const char *user, const char *passwd, const char *home);
```

添加 FTP 用户。

**参数**：

- `handle` 由 `ftpd_open()` 返回的句柄。
- `accountflags` 用户属性标志（参见 `FTPD_ACCOUNTFLAGS_*`）。
- `user` 用户名（`NULL` 表示无需登录）。
- `passwd` 密码（`NULL` 表示无需密码）。
- `home` 用户主目录。

### ftpd_session

```c
int ftpd_session(FTPD_SESSION handle, int timeout);
```

运行 FTP 服务器会话，等待并处理一个客户端连接。

**参数**：

- `handle` 会话句柄。
- `timeout` 等待连接的超时时间（毫秒），0 表示无限等待。

### ftpd_close

```c
void ftpd_close(FTPD_SESSION handle);
```

关闭 FTP 服务器会话。
