# 消息队列

`NuttX` 支持 `POSIX` 命名的消息队列用于任务间的通讯，任何任务都可以通过消息队列来发送或接收。在中断中可以发送消息给消息队列。

`NuttX`消息队列支持以下`api`:

- `mq_open()`
- `mq_close()`
- `mq_unlink()`
- `mq_send()`
- `mq_timedsend()`
- `mq_receive()`
- `mq_timedreceive()`
- `mq_notifiy()`
- `mq_setattr()`
- `mq_getattr()`

## mq_open

```c
mqd_t mq_open(const char *mqName, int oflags, ...);
```

在调用任务和消息队列之间建立一个连接。在成功调用`mq_open`之后。这个任务可以用其返回值来使用消息队列。这个消息队列描述符将一直可用直到成`mq_close()`。

*参数* ：

- `mqName` 打开队列的名字。
- `oflags` 打开标志位，可以是以下的任意组合：
  - `O_RDONLY`. 打开可读权限。
  - `O_WRONLY`. 打开可写权限。
  - `O_RDWR`. 打开可读可写权限。
  - `O_CREAT`. 如果消息队列不存在，则创建它。
  - `O_EXCL`. 打开时必须存在。
  - `O_NONBLOCK`. 不需要等待数据。
- `...` 可选参数。当使用`O_CREAT`标志时，`POSIX`要求提供第三个和第四个参数：
  - `mode`. `mode`的参数类型为`mode_t`。在`POSIX`规范中，`mode`用来提供消息队列的文件权限位。这个参数是必须的，但是在当前实现中没有被使用
  - `attr`. 用于初始化`mq_attr`的指针。如果`attr` 为 `NULL`，则使用默认值来创建消息队列。如果为非`NULL`,则在创建消息队列时将`attr`里的参数用于消息队列的创建，其中`mq_maxmsg`用来设置在消息队列上同时存在消息的最大个数，`mq_msgsize` 用来设置每条消息最大的大小。

*返回值*：

消息队列描述符或者-1(`ERROR`)

*`POSIX`兼容性*：完美兼容`POSIX`同名接口

## mq_close

```c
int mq_close(mqd_t mqdes);
```

用来在调用任务中表示对`mqdes`已完成使用。`mq_close()`用来释放系统分配给这个任务的资源。

如果这个任务在消息队列上附加了一个通知请求，这个通知请求会被去除，并且消息队列可以提供另一个任务用来获取通知

*参数*：

- `mqdes` 消息队列描述符。

*返回值*：

- `OK`消息队列关闭成功则为`0`,否则为`-1`（`ERROR`）。

*假设*：

- `mq_send()`或者`mq_receive()`阻塞时调用`mq_close()`的任务行为是未定义的。
- 在成功调用`mq_close()`后再次使用同一个`mqdes`调用`mq_close`未定义。

*`POSIX`兼容性* ：完美兼容`POSIX`同名接口。

## mq_unlink

```c
int mq_unlink(const char* mqName);
```

删除以`mqName`命名的消息队列。如果有一个或者多个任务打开了这个消息队列的时候调用了`mq_unlink()`，则将推迟消息队列的删除，直到所有消息队列都被关闭。

*参数*：

- `mqName` 消息队列的名字。

*`POSIX`兼容性*：完美兼容`POSIX`同名接口。

## mq_send

```c
int mq_send(mqd_t mqdes, const void *msg, size_t msqglen, int prio);
```

将指定消息`msg`发送到消息队列`mqdes`。`msglen`这个参数指定了`msg`的字节长度。这个长度必须不大于从`mq_geattr()`获取的最大长度。

如果消息队列没有满，`mq_send`将会通过根据`prio`优先级放入消息队列的指定位置。高优先级的消息会被插在低优先级的消息之前。`prio`的值必须不能超过`MQ_RPIO_MAX`

如果消息队列已满并且没有设置`O_NONBLOCK`，`mq_send()`将会被阻塞，直到消息队列有可用空间。

如果消息队列已满并且设置了`O_NONBLOCK`，消息并不会被加入消息队列，并且会返回一个错误。

*注意*：`mq_send`可以在中断中被调用。它的行为在中断中会有不同：

- 它不会去检查队列的大小。总是会发送消息，即使队列中已经有了很多消息。这是因为中断中不能等待消息队列未满。
- 它不会去申请新的内存（因为在你不能在中断中申请内存）。也就是说，会有一个提前申请的内存，仅用于从中断中发送消息。提前申请消息的数量由`PREALLOC_MQ_IRQ_MSGS`设置。

*参数*

- `mqdes` 消息队列描述符。
- `msg` 要发送的消息。
- `msglen` 消息的字节长度。
- `prio` 消息的优先级。

*返回值*

如果成功，`mq_send`将会返回0（`OK`）；如果失败，将会返回-1（`ERROR`），同时将会设置`errno`

- `EAGAIN`当队列已满，并且通过`mqdes`消息队列描述符设置了`O_NONBLOCK`。
- `EINVAL` `msg`或者`mqdes`是`NULL`或者`prio`是无效值。
- `EPERM` 消息队列被打开不是为了写。
- `EMSGSIZE` `msglen`超过了消息队列中的`maxmsgszie`属性。
- `EINTR` 调用被信号中断。

*`POSIX`兼容性*：完美兼容`POSIX`同名接口。

## mq_timedsend

```c
int mq_timedsend(mqd_t mqdes, const void *msg, size_t msqglen, int prio, const struct timespec *abstime);
```

将指定消息`msg`发送到消息队列`mqdes`。`msglen`这个参数指定了`msg`的字节长度。这个长度必须不大于从`mq_geattr()`获取的最大长度。

如果消息队列没有满，`mq_timedsend`将会通过根据`prio`优先级放入消息队列的指定位置。高优先级的消息会被插在低优先级的消息之前。`prio`的值必须不能超过`MQ_RPIO_MAX`

如果消息队列已满并且没有设置`O_NONBLOCK`，`mq_timedsend()`将会被阻塞，直到消息队列有可用空间或超时。

`mq_timedsend()`的行为和`mq_send`类似，除了如果消息队列已满`O_NONBLOCK`没有被设置，则`abstime`设置一个结构体，该结构体表示了`mq_timedsend()`阻塞的时间上限。这个上限是从1970年一月一日零点零分零秒开始算起的绝对时间。

如果消息队列已满，并且在调用时以超时，那么`mq_timedsend()`立即返回。

*参数*

- `mqdes` 消息队列描述符。
- `msg` 要发送的消息。
- `msglen` 消息的字节长度。
- `prio` 消息的优先级。
- `abstime` 超时时间。

*返回值*

如果成功，`mq_send`将会返回0（`OK`）；如果失败，将会返回-1（`ERROR`），同时将会设置`errno`

- `EAGAIN`当队列已满，并且通过`mqdes`消息队列描述符设置了`O_NONBLOCK`。
- `EINVAL` `msg`或者`mqdes`是`NULL`或者`prio`是无效值。
- `EPERM` 消息队列被打开不是为了写。
- `EMSGSIZE` `msglen`超过了消息队列中的`maxmsgszie`属性。
- `EINTR` 调用被信号中断。
- `ETIMEDOUT` 发送超时。

*`POSIX`兼容性*：完美兼容`POSIX`同名接口。

## mq_receive

```c
ssize_t mq_receive(mqd_t mqdes, void *msg, size_t msglen, int *prio);
```

通过`mqdes`从指定消息队列接收最早优先级最高的消息。如果缓冲区的大小`msglen`小于消息队列中`mq_msgsize`这个属性，`mq_receive()`会返回一个错误，相反，将会从消息队列中移除这个消息，并把它拷贝到`msg`。

如果消息队列是空的并且`O_NONBLOCK`没有被设置，`mq_receive()`将会被阻塞直到有消息被加载进这个消息队列。如果有多个任务在等待接收消息，只会有优先级最高且等待时间最长的任务会接收到消息并解除阻塞。

如果队列为空并且设置了`O_NONBLOCK`，将会返回错误`ERROR`

*参数*：

- `mqdes` 消息队列描述符。
- `msg` 接收消息缓冲区。
- `msglen` 缓冲区的字节长度。
- `prio` 如果不为`NULL`，则存储该消息的优先级。

*返回值*：

如果成功，返回消息的长度（以字节为单位）。失败时，返回-1（`ERROR`）并且设置`errno`

- `EAGAIN` 队列为空，并且`mqdes`设置了 `O_NONBLOCK`。
- `EPERM` 消息队列不可读。
- `EMSGSIZE` `msglen`小于消息队列`maxmsgsize`的属性。
- `EINTR` 调用被信号中断。

*`POSIX`兼容性*：完美兼容`POSIX`同名接口。

## mq_timedreceive

```c
ssize_t mq_timedreceive(mqd_t mqdes, void *msg, size_t msglen, int *prio);
```

通过`mqdes`从指定消息队列接收最早优先级最高的消息。如果缓冲区的大小`msglen`小于消息队列中`mq_msgsize`这个属性，`mq_timedreceive()`会返回一个错误，相反，将会从消息队列中移除这个消息，并把它拷贝到`msg`。

如果消息队列是空的并且`O_NONBLOCK`没有被设置，`mq_timedreceive()`将会被阻塞直到有消息被加载进这个消息队列或者发生超时。如果有多个任务在等待接收消息，只会有优先级最高且等待时间最长的任务会接收到消息并解除阻塞。

`mq_timedreceive()`的行为和`mq_receive`类似，除了如果消息队列已满`O_NONBLOCK`没有被设置，则`abstime`设置一个结构体，该结构体表示了`mq_timedreceive()`阻塞的时间上限。这个上限是从1970年一月一日零点零分零秒开始算起的绝对时间。

如果消息队列没有消息，并且在调用时以超时，那么`mq_timedreceive()`立即返回。

*参数*：

- `mqdes` 消息队列描述符。
- `msg` 接收消息缓冲区。
- `msglen` 缓冲区的字节长度。
- `prio` 如果不为`NULL`，则存储该消息的优先级。
- `abstime` 超时时间

*返回值*：

如果成功，返回消息的长度（以字节为单位）。失败时，返回-1（`ERROR`）并且设置`errno`

- `EAGAIN` 队列为空，并且`mqdes`设置了 `O_NONBLOCK`。
- `EPERM` 消息队列不可读。
- `EMSGSIZE` `msglen`小于消息队列`maxmsgsize`的属性。
- `EINTR` 调用被信号中断。
- `ETIMEDOUT` 接收超时。

*`POSIX`兼容性*：完美兼容`POSIX`同名接口。

## mq_notify

```c
int mq_notify(mqd_t mqdes, FAR struct sigevent *notification)
```

如果`notification` 输入参数不是`NULL`,那么当前进程希望在有一个消息到达指定的先前为空的队列是得到通知。

如果`notifications`是`NULL`，且当前的进程被注册为接收指定队列的通知，那么将已存在的注册取消

当通知发送到已注册的任务时，注册将被取消。之后消息队列可用于注册通知。

*参数*：

- `mqdes` 消息队列描述符
- `notifications` 实时信号结构体包括：
  - `sigev_notify` 应该是`SIGEV_SIGNAL`（但实际上没有被使用）。
  - `sigev_signo` 用于通知的信号。
  - `sigev_value` 与信号量相关的值。

*返回值*：

如果成功，则`mq_notify()`返回0；如果失败，将返回-1，并且会设置`errno`：

- `EBADF` `mqdes` 设备描述符无效
- `EBUSY` 另一个进程已经对该消息队列注册通知。
- `EINVAL` `sevp->sigev_notify`不是一个允许的值，或者`sevp->sigev_notifiy`是`SIGEV_SIGNAL`并且`sevp->sigev_signo`不是一个有效的编号
- `ENOMEM` 内存不足。

*`POSIX`兼容性*：兼容`POSIX`同名接口。与完整的`POSIX`实现区别有

- 即使另一个任务正在等待消息队列变为空，通知信号也会发送到已注册的任务。这与`POSIX`规范不一致，该规范指出：“如果一个进程已经注册了消息到达消息队列的通知，并且`mq_receive`当消息到达队列时某个进程在等待接收消息时被阻塞，则到达的消息将满足适当`mq_receive()`的......由此产生的行为就像消息队列保持空，并且不会发送任何通知。”

## mq_setattr

```c
int mq_setattr(mqd_t mqdes, const struct mq_attr *mqStat, struct mq_attr *oldMqStat)
```

设置与`mqdes`消息队列的相关属性。`mq_flag`中只有`O_NONBLOCK`位才能被改变。

如果`oldMqStat`为非空，那么`mq_setattr()`将在该位置存储先前的消息队列属性(就像`mq_getattr()`返回的一样).

*参数*：

- `mqdes` 消息队列描述符。
- `mqStat` 新属性。
- `oldMqStat` 旧属性。

*返回值*：`OK` 如果属性设置成功则返回0，否则返回-1(`ERROR`)

*`POSIX`兼容性*：完美兼容`POSIX`同名接口。

## mq_getattr

```c
int mq_getattr(mqd_t mqdes, struct mq_attr *mqStat)
```

获取与指定消息队列关联的状态信息和属性。

*参数*：

- `mqdes` 消息队列描述符。
- `mqStat` 返回属性结构体：
  - `mq_maxmsg` 队列中的最大消息数。
  - `mq_msgsize` 最大消息大小。
  - `mq_flags` 消息队列标志。
  - `mq_curmsgs` 当前在队列中的消息数。

*`POSIX`兼容性*：完美兼容`POSIX`同名接口。
