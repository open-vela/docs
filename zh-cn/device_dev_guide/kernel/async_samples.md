# openvela 异步编程开发示例

\[ [English](../../../en/device_dev_guide/kernel/async_samples.md) | 简体中文 \]

## 一、驱动开发中的信号量使用

在 `openvela` 的驱动程序开发中，处理来自中断的异步事件时，必须采用高效且可靠的同步机制。

核心原则：推荐使用**中断-信号量-线程**模型进行数据同步。此模型通过 `nxsem_wait_uninterruptible` 和 `nxsem_post` 函数对，实现低延迟、低功耗的事件处理。

应坚决避免：

- 忙等待 (Busy-Waiting)：循环检查标志位会严重浪费 CPU 资源，并可能导致系统性能下降。
- `loopsleep` 等待：使用固定时长的休眠来轮询事件，会引入不必要的延迟，且不具备确定性。

### 设计模式：中断与工作线程同步

该模式的标准实现流程如下：

1. 工作线程 (Worker Thread)：一个专用的内核线程（kthread），其主要任务是处理数据或执行某个动作。
2. 中断服务程序 (Interrupt Service Routine, ISR)：当硬件事件（如数据到达）发生时，由硬件触发执行。ISR 的职责应尽可能轻量，仅用于通知工作线程。
3. 信号量 (Semaphore)：作为 ISR 与工作线程之间的通信桥梁。

执行逻辑：

1. 工作线程在启动后，调用 `nxsem_wait_uninterruptible` 等待信号量，使线程进入阻塞状态，不消耗 CPU。
2. 当硬件中断发生时，ISR 被触发。
3. ISR 调用 `nxsem_post` 释放（或增加）信号量，然后立即退出。
4. 工作线程因信号量被释放而唤醒，并开始处理相关任务。

### 关键函数说明

| 函数                       | 作用                                                                          |
| -------------------------- | ----------------------------------------------------------------------------- |
| nxsem_init                 | 初始化一个信号量，通常在驱动初始化时调用。                                    |
| kthread_create             | 创建并启动一个内核线程，作为数据处理的工作线程。                              |
| nxsem_wait_uninterruptible | 使当前线程进入不可中断的等待状态，直到信号量可用。                            |
| nxsem_post                 | 释放一个信号量，唤醒正在等待它的线程。此函数是线程安全的，适合在 ISR 中调用。 |

### 代码示例：Rpmsg Virtio 驱动

以下代码摘自 `Rpmsg Virtio Driver`，清晰地展示了该设计模式的典型实现。

#### 步骤一 初始化信号量与内核线程

在 `rpmsg_virtio_lite_initialize` 函数中，系统会创建用于接收数据的信号量 (`semrx`) 和一个专用的内核线程 (`rpmsg_virtio_lite_thread`)。

```C
/*
 * In rpmsg_virtio_lite_initialize()
 */
int rpmsg_virtio_lite_initialize(FAR struct rpmsg_virtio_lite_s *dev)
{
  ...
  /* Initialize the RX semaphore, its initial count is 0. */
  nxsem_init(&priv->semrx, 0, 0);
  ...
  /* Create a kernel thread to handle received data. */
  ret = kthread_create("rpmsg_virtio", CONFIG_RPMSG_VIRTIO_LITE_PRIORITY,
                       CONFIG_RPMSG_VIRTIO_LITE_STACKSIZE,
                       rpmsg_virtio_lite_thread, argv);
  if (ret < 0)
    {
      goto err_thread;
    }
 
  ...
}
```

#### 步骤二 在工作线程中等待信号量

内核线程 `rpmsg_virtio_lite_thread` 在一个无限循环中运行。它调用 `nxsem_wait_uninterruptible` 来阻塞自身，等待中断事件的通知。

```C
/*
 * The worker thread implementation.
 */
static int rpmsg_virtio_lite_thread(int argc, FAR char *argv[])
{
  ...
  /* Register the interrupt callback function. */
  RPMSG_VIRTIO_LITE_REGISTER_CALLBACK(priv->dev, rpmsg_virtio_lite_callback,
                                      priv);
  ...
  while (1)
    {
      /* Block and wait for the RX semaphore to be posted from the ISR. */
      nxsem_wait_uninterruptible(&priv->semrx);
      
      /* Once unblocked, process the available data. */
      if (rpmsg_virtio_lite_available_rx(priv))
        {
          virtqueue_notification(priv->rvdev.rvq);
        }
    }
}
```

#### 步骤三 在中断回调中释放信号量

当硬件数据到达并触发中断时，`rpmsg_virtio_lite_callback` (作为 ISR) 被调用。它会通过 `nxsem_post` 信号量来唤醒工作线程。检查 `semcount` 可防止信号量计数值无限制增长。

```C
/*
 * The interrupt callback function (acts as an ISR).
 */
static int rpmsg_virtio_lite_callback(FAR void *arg, uint32_t vqid)
{
  int semcount;
  ...
  /* Post the RX semaphore to wake up the worker thread. */
  nxsem_get_value(&priv->semrx, &semcount);
  if (semcount < 1)
    {
      nxsem_post(&priv->semrx);
    }
}
```

## 二、使用消息队列进行数据传输

当需要在任务之间或从中断服务程序（ISR）向任务传递**带有数据的消息**时，应使用消息队列（Message Queue）。与仅用于同步的信号量不同，消息队列能够在内核中缓存固定大小的数据包，实现可靠的异步数据交换。

`openvela` 遵循 POSIX 标准，提供了 `mqueue` 接口。这些接口通常通过虚拟文件系统（VFS）进行封装，允许开发者像操作文件一样来管理消息队列。

### 设计模式：生产者-消费者模型

消息队列非常适合实现生产者-消费者设计模式：

- **生产者 (Producer)**：一个或多个任务，或一个 ISR，负责生成数据并将其作为消息发送到队列中。
- **消费者 (Consumer)**：一个或多个任务，负责从队列中接收并处理消息。
- **消息队列 (Message Queue)**：作为生产者和消费者之间的线程安全缓冲区，解耦了二者的执行逻辑。

执行逻辑：

1. **初始化**：消费者任务在启动时打开或创建一个指定名称的消息队列。
2. **发送**：当生产者有数据需要传递时，它将数据打包成一条消息，并调用发送函数将其放入队列。如果队列已满，发送操作可能会根据配置阻塞或立即返回错误。
3. **接收**：消费者任务调用接收函数等待消息。如果队列为空，该任务将进入阻塞状态，释放 CPU 资源，直到新消息到达。

### 关键函数说明

`openvela` 通过文件操作接口封装了 POSIX `mqueue`，以下是核心函数：

| 函数            | 作用                                                                                                                           |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| file_mq_open    | 创建或打开一个具名消息队列。通过 struct mq_attr 参数配置队列属性，如最大消息数 (mq_maxmsg) 和每条消息的最大尺寸 (mq_msgsize)。 |
| file_mq_send    | 向指定的消息队列发送一条消息。此操作是原子的，支持消息优先级。                                                                 |
| file_mq_receive | 从消息队列中接收一条消息。如果队列为空，调用任务将阻塞等待。                                                                   |

### 代码示例：蓝牙 (BT) 服务中的消息队列

以下代码片段展示了如何封装和使用消息队列来传递蓝牙数据缓冲区（`bt_buf`）。

#### 步骤一 打开并配置消息队列

`bt_queue_open` 函数封装了 `file_mq_open`，用于初始化一个消息队列。在调用时必须指定队列的容量 (`nmsgs`)。

```C
/*
 * In bt_queue_open()
 */
int bt_queue_open(FAR const char *name, int oflags, int nmsgs,
                  FAR struct file *mqd)
{
  struct mq_attr attr;
  int ret;
  
  /* Configure message queue attributes. */
  /* mq_maxmsg: Maximum number of messages in the queue. */
  attr.mq_maxmsg  = nmsgs;
  
  /* mq_msgsize: Size of each message. Here it holds a pointer. */
  attr.mq_msgsize = BT_MSGSIZE;
  attr.mq_flags   = BT_MSGFLAGS;
  /* Create or open the message queue via the VFS layer. */
  ret = file_mq_open(mqd, name, oflags, 0666, &attr);
  if (ret < 0)
    {
      gerr("ERROR: file_mq_open(%s) failed: %d\n", name, ret);
    }
  return ret;
}
```

#### 步骤二 发送消息

`bt_queue_send` 函数将一个指向 `bt_buf_s` 结构体的指针封装进消息体中，并将其发送到队列。

```C
/*
 * In bt_queue_send()
 */
int bt_queue_send(struct file *mqd,
                  FAR struct bt_buf_s *buf,
                  unsigned int priority)
{
  struct bt_bufmsg_s msg;
  int ret;
  /* The message payload contains the pointer to the data buffer. */
  msg.buf = buf;
  /* Send the message to the queue. */
  ret = file_mq_send(mqd, (FAR const char *)&msg,
                     sizeof(struct bt_bufmsg_s), priority);
  if (ret < 0)
    {
      wlerr("ERROR: file_mq_send() failed: %d\n", ret);
    }
  return ret;
}
```

#### 步骤三 接收消息

#### `bt_queue_receive` 函数阻塞等待，直到从队列中成功接收一条消息，并从中提取出数据缓冲区的指针。

```C
/*
 * In bt_queue_receive()
 */
int bt_queue_receive(struct file *mqd, FAR struct bt_buf_s **buf)
{
  union
  {
    struct bt_bufmsg_s msg;
    char msgbuf[BT_MSGSIZE];
  } u;
  ssize_t msgsize;
  ...
  /* Block and wait to receive a message from the queue. */
  msgsize = file_mq_receive(mqd, u.msgbuf, BT_MSGSIZE, NULL);
  if (msgsize < 0)
    {
      wlerr("ERROR: file_mq_receive() failed: %ld\n", (long)msgsize);
      return (int)msgsize;
    }
  
  /* Extract the data buffer pointer from the message. */
  *buf = u.msg.buf;
  
  ...
  return OK;
}
```

#### 注意事项

1. 消息队列大小：
   1. 确保消息队列的 `mq_maxmsg` 和 `mq_msgsize` 设置合理，否则可能导致消息丢失或任务阻塞。
2. 错误处理：
   1. 对消息队列操作的返回值进行检查，避免因创建、发送或接收失败引发系统异常。
3. 优先级使用：
   1. 合理设置消息优先级，根据任务的实时性需求确保高优先级消息优先处理。
4. 资源释放：
   1. 在消息队列不再使用时，应及时关闭并释放相关资源。

## 三、使用工作队列实现中断任务延迟处理

在 `openvela` 中，中断服务程序（ISR）必须在极短的时间内完成执行，以保证系统的实时性和响应能力。任何耗时较长的操作，如循环、复杂计算、或调用可能休眠的函数，都严禁在 ISR 中直接执行。

为了解决这一问题，系统提供了**工作队列（Work Queue）**机制。它允许 ISR 将耗时的任务委托给一个专用的内核工作线程来延迟执行。这种设计模式通常被称为**顶半部/底半部（Top-Half / Bottom-Half）**模型。

- **顶半部（Top-Half）**：即 ISR 本身。它只负责处理最紧急的硬件操作（如读取状态、清除中断标志），然后将后续工作打包并提交给工作队列。
- **底半部（Bottom-Half）**：即由工作队列的工作线程执行的函数。它在非中断上下文中运行，可以安全地执行更复杂、更耗时的任务。

### 关键函数说明

核心函数 `work_queue` 用于将一个工作项（一个函数及其参数）调度到指定的工作队列。

```C
int work_queue(int qid, FAR struct work_s *work, worker_t worker, FAR void *arg, clock_t delay);
```

- `qid`: 目标工作队列的 ID，通常为 `HPWORK` 或 `LPWORK`。
- `work`: 指向一个 `struct work_s` 结构的指针。该结构必须是静态分配或全局分配的，通常作为设备私有数据的一部分，绝不能是 ISR 栈上的局部变量。
- `worker`: 一个函数指针，指向需要被延迟执行的“底半部”函数。
- `arg`: 传递给 `worker` 函数的参数。
- `delay`: 延迟执行的时间（以系统节拍 `tick` 为单位）。如果为 0，则尽快调度执行。

### 代码示例：ADC 驱动中的中断处理

以下 `ADC` 驱动代码完美诠释了**顶半部/底半部**模型。

#### 步骤一 在中断顶半部中调度工作

`sam_adc_interrupt` 作为 ISR（顶半部），在中断发生后，仅执行必要的寄存器操作，然后立即调用 `work_queue` 将耗时的转换后处理任务 (`sam_adc_endconversion`) 提交给 `HPWORK` 队列，并迅速退出。

```C
/*
 * The Interrupt Service Routine (Top-Half)
 */
static int sam_adc_interrupt(int irq, void *context, void *arg)
{
  ...
  /* Check for 'end of conversion' interrupt. */
  if ((pending & ADC_INT_EOCALL) != 0)
    {
      /* Perform minimal, time-critical register operations here. */
      ...
 
      /* Defer the time-consuming processing to the high-priority work queue. */
      ret = work_queue(HPWORK, &priv->work, sam_adc_endconversion, priv, 0);
      if (ret != 0)
        {
          aerr("ERROR: Failed to queue work: %d\n", ret);
        }
      pending &= ~ADC_INT_EOCALL;
    }
...
  return OK;
}
```

#### 步骤二 在工作线程底半部中执行任务

`sam_adc_endconversion` 函数作为底半部，由 `hpwork` 线程在稍后安全地执行。它包含了循环处理、加锁解锁以及调用上层回调函数等不适合在 ISR 中进行的操作。

```C
/*
 * The worker function executed by the work queue thread (Bottom-Half)
 */
static void sam_adc_endconversion(void *arg)
{
  /* This function runs in a normal kernel thread context, not an ISR. */
  
  /* Operations like locking are safe here. */
  ret = sam_adc_lock(priv);
  if (ret < 0)
    {
      return;
    }
  /* Looping through channels is too slow for an ISR. */
  for (chan = 0; chan < SAM_ADC_NCHANNELS && pending != 0; chan++)
    {
      ...
      if ((pending & bit) != 0)
        {
          /* Calling a potentially complex upper-layer callback is safe here. */
          if (priv->cb != NULL)
            {
              priv->cb->au_receive(priv->dev, chan, regval & ADC_CDR_DATA_MASK);
            }
          ...
        }
    }
  sam_adc_unlock(priv);
}
```

## 相关文档

- [内核开发概述](./KernelDev.md)
