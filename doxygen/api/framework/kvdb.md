# KVDB API

KVDB 提供轻量级键值对持久化存储，底层基于 UnQLite 数据库，API 设计参考 Android properties 规范。

头文件：`#include <kvdb.h>`、`#include <cutils/properties.h>`

## openvela 实现说明

- **存储后端**：基于 UnQLite 嵌入式数据库
- **键值类型**：支持字符串、布尔、int32、int64 和二进制数据
- **同步/异步写入**：`property_set()` 为同步写入，`property_set_oneway()` 为异步写入（不等待持久化完成）
- **监控机制**：支持通过 `property_wait()` 或 `property_monitor_*` 接口监听键值变更
- **命令行工具**：提供 `setprop`/`getprop` 命令行工具用于调试

## 读取接口

### property_get

```c
int property_get(const char *key, char *value, const char *default_value);
```

获取字符串类型的属性值。如果键不存在，返回默认值。

**参数**：

- `key` 属性键名。
- `value` 用于存储属性值的缓冲区。
- `default_value` 键不存在时的默认值，可为 `NULL`。

**返回值**：

返回属性值的长度。

### property_get_bool

```c
int8_t property_get_bool(const char *key, int8_t default_value);
```

获取布尔类型的属性值。

**参数**：

- `key` 属性键名。
- `default_value` 键不存在时的默认值。

**返回值**：

返回属性的布尔值。

### property_get_int32

```c
int32_t property_get_int32(const char *key, int32_t default_value);
```

获取 32 位整数类型的属性值。

**参数**：

- `key` 属性键名。
- `default_value` 键不存在时的默认值。

**返回值**：

返回属性的 int32 值。

### property_get_int64

```c
int64_t property_get_int64(const char *key, int64_t default_value);
```

获取 64 位整数类型的属性值。

**参数**：

- `key` 属性键名。
- `default_value` 键不存在时的默认值。

**返回值**：

返回属性的 int64 值。

### property_get_buffer

```c
ssize_t property_get_buffer(const char *key, void *value, size_t size);
```

获取二进制缓冲区类型的属性值。

**参数**：

- `key` 属性键名。
- `value` 用于存储数据的缓冲区。
- `size` 缓冲区大小。

**返回值**：

成功时返回读取的字节数，失败时返回负的错误码。

### property_get_binary

```c
ssize_t property_get_binary(const char *key, void *value, size_t val_len);
```

获取二进制类型的属性值。

**参数**：

- `key` 属性键名。
- `value` 用于存储数据的缓冲区。
- `val_len` 缓冲区大小。

**返回值**：

成功时返回读取的字节数，失败时返回负的错误码。

### property_get_with_err

```c
int property_get_with_err(const char *key, char *value);
```

获取字符串属性值，通过返回值区分"键不存在"和"值为空"。

**参数**：

- `key` 属性键名。
- `value` 用于存储属性值的缓冲区。

**返回值**：

成功时返回属性值长度，键不存在时返回负的错误码。

### property_get_bool_with_err

```c
int property_get_bool_with_err(const char *key, int8_t *value);
```

带错误检测的布尔值读取。

**参数**：

- `key` 属性键名。
- `value` 用于存储布尔结果的指针。

**返回值**：

成功时返回 `0`，键不存在或类型不匹配时返回负的错误码。

### property_get_int32_with_err

```c
int property_get_int32_with_err(const char *key, int32_t *value);
```

带错误检测的 32 位有符号整数读取。

**参数**：

- `key` 属性键名。
- `value` 用于存储 int32 结果的指针。

**返回值**：

成功时返回 `0`，键不存在或类型不匹配时返回负的错误码。

### property_get_int64_with_err

```c
int property_get_int64_with_err(const char *key, int64_t *value);
```

带错误检测的 64 位有符号整数读取。

**参数**：

- `key` 属性键名。
- `value` 用于存储 int64 结果的指针。

**返回值**：

成功时返回 `0`，键不存在或类型不匹配时返回负的错误码。

## 写入接口

### property_set

```c
int property_set(const char *key, const char *value);
```

设置字符串类型的属性值（同步写入，等待持久化完成）。

**参数**：

- `key` 属性键名。
- `value` 属性值。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### property_set_oneway

```c
int property_set_oneway(const char *key, const char *value);
```

设置字符串类型的属性值（异步写入，不等待持久化完成）。性能更高但不保证立即持久化。

**参数**：

- `key` 属性键名。
- `value` 属性值。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### property_set_bool

```c
int property_set_bool(const char *key, int8_t value);
```

设置布尔类型属性值（同步写入）。

**参数**：

- `key` 属性键名。
- `value` 布尔值（`0` 或非 `0`）。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### property_set_int32

```c
int property_set_int32(const char *key, int32_t value);
```

设置 32 位有符号整数属性值（同步写入）。

**参数**：

- `key` 属性键名。
- `value` int32 值。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### property_set_int64

```c
int property_set_int64(const char *key, int64_t value);
```

设置 64 位有符号整数属性值（同步写入）。

**参数**：

- `key` 属性键名。
- `value` int64 值。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### property_set_bool_oneway

```c
int property_set_bool_oneway(const char *key, int8_t value);
```

异步设置布尔类型属性值（不等待持久化完成）。

**参数**：

- `key` 属性键名。
- `value` 布尔值。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### property_set_int32_oneway

```c
int property_set_int32_oneway(const char *key, int32_t value);
```

异步设置 int32 类型属性值（不等待持久化完成）。

**参数**：

- `key` 属性键名。
- `value` int32 值。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### property_set_int64_oneway

```c
int property_set_int64_oneway(const char *key, int64_t value);
```

异步设置 int64 类型属性值（不等待持久化完成）。

**参数**：

- `key` 属性键名。
- `value` int64 值。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### property_set_buffer

```c
int property_set_buffer(const char *key, const void *value, size_t size);
```

设置二进制缓冲区类型的属性值（同步写入）。

**参数**：

- `key` 属性键名。
- `value` 数据缓冲区指针。
- `size` 缓冲区字节数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### property_set_buffer_oneway

```c
int property_set_buffer_oneway(const char *key, const void *value, size_t size);
```

异步设置二进制缓冲区类型的属性值（不等待持久化完成）。

**参数**：

- `key` 属性键名。
- `value` 数据缓冲区指针。
- `size` 缓冲区字节数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### property_set_binary

```c
int property_set_binary(const char *key, const void *value, size_t val_len, bool oneway);
```

设置二进制类型的属性值。

**参数**：

- `key` 属性键名。
- `value` 二进制数据。
- `val_len` 数据长度。
- `oneway` 是否异步写入。

### property_delete

```c
int property_delete(const char *key);
```

删除指定键的属性。

**参数**：

- `key` 要删除的属性键名。

**返回值**：

成功时返回 0，失败时返回负的错误码。

## 管理接口

### property_commit

```c
int property_commit(void);
```

强制将所有待写入的属性持久化到存储。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### property_load

```c
int property_load(const char *path);
```

从文件加载属性到数据库。

**参数**：

- `path` 属性文件路径。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### property_exit

```c
int property_exit(void);
```

关闭 KVDB 并释放资源。

**返回值**：

成功时返回 0，失败时返回负的错误码。

### property_list

```c
int property_list(void (*propfn)(const char *key, const char *value, void *cookie), void *cookie);
```

遍历所有属性，对每个属性调用回调函数。

**参数**：

- `propfn` 回调函数，接收键、值和用户数据。
- `cookie` 传递给回调函数的用户数据。

### property_list_binary

```c
int property_list_binary(void (*propfn)(const char *key, const void *value, size_t val_len, void *cookie), void *cookie);
```

遍历所有二进制类型属性，对每个属性调用回调函数。相比 `property_list`，回调参数带有 `val_len` 字段，适合处理非字符串值。

**参数**：

- `propfn` 回调函数，签名为 `void (*)(const char *key, const void *value, size_t val_len, void *cookie)`，接收键、二进制值、值长度和用户数据。
- `cookie` 传递给回调函数的用户数据。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## 监控接口

### property_wait

```c
ssize_t property_wait(const char *key, char *newkey, void *newvalue, size_t val_len, int timeout);
```

等待属性变更通知。阻塞直到指定键（或任意键）发生变更或超时。

**参数**：

- `key` 要监控的键名，`NULL` 表示监控所有键。
- `newkey` 用于存储变更的键名。
- `newvalue` 用于存储变更后的值。
- `val_len` 值缓冲区大小。
- `timeout` 超时时间（毫秒），-1 表示无限等待。

**返回值**：

成功时返回值的长度，超时返回 0，失败时返回负的错误码。

### property_monitor_open

```c
int property_monitor_open(const char *key);
```

打开属性监控文件描述符，可配合 `poll()` 使用。

**参数**：

- `key` 要监控的键名，`NULL` 表示监控所有键。

**返回值**：

成功时返回文件描述符，失败时返回负的错误码。

### property_monitor_read

```c
ssize_t property_monitor_read(int fd, char *newkey, void *newvalue, size_t val_len);
```

从监控文件描述符读取变更事件。

**参数**：

- `fd` 由 `property_monitor_open()` 返回的文件描述符。
- `newkey` 用于存储变更的键名。
- `newvalue` 用于存储变更后的值。
- `val_len` 值缓冲区大小。

**返回值**：

成功时返回值的长度，失败时返回负的错误码。

### property_monitor_close

```c
int property_monitor_close(int fd);
```

关闭属性监控文件描述符。

**参数**：

- `fd` 要关闭的文件描述符。

**返回值**：

成功时返回 0，失败时返回负的错误码。
