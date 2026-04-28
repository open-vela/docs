# 消息队列 API

openvela 提供符合 POSIX 标准的消息队列接口，用于任务间的异步消息传递。消息队列支持优先级排序，高优先级消息优先被接收。

头文件：`#include <mqueue.h>`

## openvela 实现说明

- **中断中发送**：`mq_send()` 可在中断上下文中调用，但行为不同：不检查队列大小，使用预分配消息（数量由 `PREALLOC_MQ_IRQ_MSGS` 配置）
- **通知行为差异**：`mq_notify()` 即使有任务在等待接收消息，仍会发送通知信号，与 POSIX 规范不完全一致
- **超时时间**：`mq_timedsend()` 和 `mq_timedreceive()` 使用基于 Epoch 的绝对时间

## 队列管理

### mq_open

```c
mqd_t mq_open(const char *mqName, int oflags, ...);
```

在调用任务和消息队列之间建立连接。成功调用后，返回的消息队列描述符可用于后续操作，直到调用 `mq_close()`。

**参数**：

- `mqName` 消息队列的名称。
- `oflags` 打开标志位，可以是以下的任意组合：
  - `O_RDONLY` 只读。
  - `O_WRONLY` 只写。
  - `O_RDWR` 读写。
  - `O_CREAT` 如果消息队列不存在则创建。
  - `O_EXCL` 与 `O_CREAT` 配合，如果队列已存在则失败。
  - `O_NONBLOCK` 非阻塞模式。
- `...` 可选参数，当使用 `O_CREAT` 时需要提供：
  - `mode`（`mode_t`）文件权限位。当前实现中未使用，但 POSIX 要求提供。
  - `attr`（`struct mq_attr *`）队列属性。如果为 `NULL` 则使用默认值。`mq_maxmsg` 设置最大消息数，`mq_msgsize` 设置最大消息大小。

**返回值**：

成功时返回消息队列描述符（`mqd_t`），失败时返回 -1（`ERROR`）并设置 `errno`：

- `ENOENT` 未设置 `O_CREAT` 且指定的队列不存在。
- `EEXIST` 同时设置了 `O_CREAT` 和 `O_EXCL`，但队列已存在。
- `EINVAL` 参数无效（如 `mqName` 为 `NULL`）。
- `ENOMEM` 内存不足，无法创建队列。
- `ENFILE` 系统消息队列数量已达上限。

**POSIX 兼容性**：兼容 POSIX 同名接口。

### mq_close

```c
int mq_close(mqd_t mqdes);
```

关闭消息队列描述符，释放系统分配给该任务的资源。如果任务在该队列上注册了通知请求，通知会被取消。

**参数**：

- `mqdes` 消息队列描述符。

**返回值**：

成功时返回 0，失败时返回 -1（`ERROR`）并设置 `errno`：

- `EBADF` `mqdes` 不是有效的消息队列描述符。

**注意**：

- 在 `mq_send()` 或 `mq_receive()` 阻塞时调用 `mq_close()` 的行为是未定义的。
- 关闭后再次使用同一 `mqdes` 的行为是未定义的。

**POSIX 兼容性**：兼容 POSIX 同名接口。

### mq_unlink

```c
int mq_unlink(const char *mqName);
```

删除指定名称的消息队列。如果有任务仍然打开了该队列，删除会推迟到所有描述符都关闭后执行。

**参数**：

- `mqName` 消息队列的名称。

**返回值**：

成功时返回 0，失败时返回 -1（`ERROR`）并设置 `errno`：

- `ENOENT` 指定名称的队列不存在。
- `EINVAL` `mqName` 为 `NULL`。

**POSIX 兼容性**：兼容 POSIX 同名接口。

## 消息发送

### mq_send

```c
int mq_send(mqd_t mqdes, const void *msg, size_t msglen, int prio);
```

将消息发送到消息队列。消息按优先级排序，高优先级消息排在低优先级之前。`prio` 不能超过 `MQ_PRIO_MAX`。

如果队列已满且未设置 `O_NONBLOCK`，调用阻塞直到有空间可用。如果设置了 `O_NONBLOCK`，立即返回错误。

**参数**：

- `mqdes` 消息队列描述符。
- `msg` 要发送的消息。
- `msglen` 消息的字节长度，不能超过 `mq_msgsize`。
- `prio` 消息优先级。

**返回值**：

成功时返回 0，失败时返回 -1（`ERROR`）并设置 `errno`：

- `EAGAIN` 队列已满且设置了 `O_NONBLOCK`。
- `EINVAL` `msg` 或 `mqdes` 为 `NULL`，或 `prio` 无效。
- `EPERM` 消息队列未以写模式打开。
- `EMSGSIZE` `msglen` 超过队列的 `mq_msgsize`。
- `EINTR` 被信号中断。

**注意**：

- `mq_send()` 可在中断上下文中调用，但行为不同：不检查队列大小（总是发送），使用预分配消息（数量由 `PREALLOC_MQ_IRQ_MSGS` 配置），不分配新内存。

**POSIX 兼容性**：兼容 POSIX 同名接口。

### mq_timedsend

```c
int mq_timedsend(mqd_t mqdes, const void *msg, size_t msglen, int prio,
                 const struct timespec *abstime);
```

带超时的消息发送。行为与 `mq_send()` 相同，但在队列满时最多阻塞到 `abstime` 指定的绝对时间。

**参数**：

- `mqdes` 消息队列描述符。
- `msg` 要发送的消息。
- `msglen` 消息的字节长度。
- `prio` 消息优先级。
- `abstime` 绝对超时时间（基于 Epoch）。

**返回值**：

成功时返回 0，失败时返回 -1（`ERROR`）并设置 `errno`：

- `EAGAIN` 队列已满且设置了 `O_NONBLOCK`。
- `EINVAL` `msg` 或 `mqdes` 为 `NULL`，或 `prio` 无效。
- `EPERM` 消息队列未以写模式打开。
- `EMSGSIZE` `msglen` 超过队列的 `mq_msgsize`。
- `EINTR` 被信号中断。
- `ETIMEDOUT` 超时。

**POSIX 兼容性**：兼容 POSIX 同名接口。

## 消息接收

### mq_receive

```c
ssize_t mq_receive(mqd_t mqdes, void *msg, size_t msglen, int *prio);
```

从消息队列接收优先级最高且最早的消息。`msglen` 不能小于队列的 `mq_msgsize`，否则返回错误。

如果队列为空且未设置 `O_NONBLOCK`，调用阻塞直到有消息可用。多个等待任务中，优先级最高且等待最久的任务优先接收。

**参数**：

- `mqdes` 消息队列描述符。
- `msg` 接收消息的缓冲区。
- `msglen` 缓冲区大小（字节）。
- `prio` 如果非 `NULL`，存储接收到的消息的优先级。

**返回值**：

成功时返回消息长度（字节），失败时返回 -1（`ERROR`）并设置 `errno`：

- `EAGAIN` 队列为空且设置了 `O_NONBLOCK`。
- `EPERM` 消息队列未以读模式打开。
- `EMSGSIZE` `msglen` 小于队列的 `mq_msgsize`。
- `EINTR` 被信号中断。

**POSIX 兼容性**：兼容 POSIX 同名接口。

### mq_timedreceive

```c
ssize_t mq_timedreceive(mqd_t mqdes, char *msg, size_t msglen,
                        unsigned int *prio, const struct timespec *abstime);
```

带超时的消息接收。行为与 `mq_receive()` 相同，但在队列空时最多阻塞到 `abstime` 指定的绝对时间。

**参数**：

- `mqdes` 消息队列描述符。
- `msg` 接收消息的缓冲区。
- `msglen` 缓冲区大小（字节）。
- `prio` 如果非 `NULL`，存储接收到的消息的优先级。
- `abstime` 绝对超时时间（基于 Epoch）。

**返回值**：

成功时返回消息长度（字节），失败时返回 -1（`ERROR`）并设置 `errno`：

- `EAGAIN` 队列为空且设置了 `O_NONBLOCK`。
- `EPERM` 消息队列未以读模式打开。
- `EMSGSIZE` `msglen` 小于队列的 `mq_msgsize`。
- `EINTR` 被信号中断。
- `ETIMEDOUT` 超时。

**POSIX 兼容性**：兼容 POSIX 同名接口。

## 队列属性

### mq_setattr

```c
int mq_setattr(mqd_t mqdes, const struct mq_attr *mqStat, struct mq_attr *oldMqStat);
```

设置消息队列属性。`mq_flags` 中只有 `O_NONBLOCK` 位可以被修改。

**参数**：

- `mqdes` 消息队列描述符。
- `mqStat` 新属性。
- `oldMqStat` 如果非 `NULL`，存储修改前的属性。

**返回值**：

成功时返回 0，失败时返回 -1（`ERROR`）并设置 `errno`：

- `EBADF` `mqdes` 不是有效的描述符。
- `EINVAL` `mqStat` 为 `NULL`。

**POSIX 兼容性**：兼容 POSIX 同名接口。

### mq_getattr

```c
int mq_getattr(mqd_t mqdes, struct mq_attr *mqStat);
```

获取消息队列的当前属性。

**参数**：

- `mqdes` 消息队列描述符。
- `mqStat` 返回属性结构体：
  - `mq_maxmsg` 队列中的最大消息数。
  - `mq_msgsize` 最大消息大小（字节）。
  - `mq_flags` 消息队列标志。
  - `mq_curmsgs` 当前队列中的消息数。

**返回值**：

成功时返回 0，失败时返回 -1（`ERROR`）并设置 `errno`：

- `EBADF` `mqdes` 不是有效的描述符。
- `EINVAL` `mqStat` 为 `NULL`。

**POSIX 兼容性**：兼容 POSIX 同名接口。

## 通知

### mq_notify

```c
int mq_notify(mqd_t mqdes, const struct sigevent *notification);
```

注册或取消消息到达通知。当消息到达先前为空的队列时，向注册的任务发送信号通知。

如果 `notification` 为 `NULL`，取消当前注册。通知发送后注册自动取消，需要重新注册。

**参数**：

- `mqdes` 消息队列描述符。
- `notification` 通知配置，包括：
  - `sigev_notify` 通知方式（应为 `SIGEV_SIGNAL`）。
  - `sigev_signo` 通知使用的信号编号。
  - `sigev_value` 随信号传递的值。

**返回值**：

成功时返回 0，失败时返回 -1（`ERROR`）并设置 `errno`：

- `EBADF` `mqdes` 不是有效的描述符。
- `EBUSY` 另一个任务已注册了该队列的通知。
- `EINVAL` `sigev_notify` 不是有效值，或信号编号无效。
- `ENOMEM` 内存不足。

**注意**：

- **与 POSIX 的行为差异**：在 openvela 中，即使有任务正在 `mq_receive()` 上阻塞等待消息，通知信号仍会发送给注册的任务。POSIX 规范要求此时不发送通知（消息直接满足等待的 `mq_receive()`）。

**POSIX 兼容性**：部分兼容 POSIX 同名接口（通知时机与 POSIX 规范有差异）。
