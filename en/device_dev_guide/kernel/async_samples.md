# openvela Asynchronous Programming Examples

\[ English | [简体中文](../../../zh-cn/device_dev_guide/kernel/async_samples.md) \]

## I. Semaphore Usage in Driver Development

In openvela driver development, handling asynchronous events from interrupts requires efficient and reliable synchronization mechanisms.

### Core Principle

It is recommended to use the **Interrupt-Semaphore-Thread** model for data synchronization. This model enables low-latency and low-power event processing by leveraging the `nxsem_wait_uninterruptible` and `nxsem_post` functions.

**Practices to strictly avoid**:

`Busy-Waiting`: Continuously checking a flag in a loop wastes significant CPU resources and can degrade system performance.

Waiting with `loopsleep`: Using fixed-duration sleeps to poll for events introduces unnecessary latency and lacks determinism.

### Design Pattern: Synchronizing an Interrupt with a Worker Thread

The standard implementation flow for this pattern is as follows:

1. **Worker Thread**: A dedicated kernel thread (kthread) whose primary task is to process data or perform an action.
2. **Interrupt Service Routine (ISR)**: Triggered by hardware when an event (e.g., data arrival) occurs. The ISR's responsibility should be minimal, serving only to notify the worker thread.
3. **Semaphore**: Acts as the communication bridge between the ISR and the worker thread.

**Execution Flow**:

1. **Worker Thread Initialization**: After startup, the worker thread calls **nxsem_wait_uninterruptible** to block itself, waiting for the semaphore. This ensures no CPU resources are consumed during the wait.
2. **Interrupt Handling**: When a hardware interrupt occurs, the **ISR** is triggered.
3. **Semaphore Release**: The ISR calls **nxsem_post** to release (or increment) the semaphore and exits immediately.
4. **Thread Wake-Up**: The worker thread is awakened by the released semaphore and begins processing the relevant task.

### Key Function Descriptions

| Function                     | Purpose                                                                                                             |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `nxsem_init`                 | Initializes a semaphore, typically called during driver initialization.                                             |
| `kthread_create`             | Creates and starts a kernel thread to act as a worker thread for data processing.                                   |
| `nxsem_wait_uninterruptible` | Puts the current thread into an uninterruptible wait state until the semaphore is available.                        |
| `nxsem_post`                 | Releases a semaphore, waking up any thread waiting for it. This function is thread-safe and suitable for ISR usage. |

### Code Example: Rpmsg Virtio Driver

The following code excerpt from the `Rpmsg Virtio Driver` illustrates the typical implementation of this design pattern.

#### Step 1: Initialize Semaphore and Kernel Thread

In the `rpmsg_virtio_lite_initialize` function, a semaphore (`semrx`) is created for receiving data, along with a dedicated kernel thread (`rpmsg_virtio_lite_thread`).

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

#### Step 2: Wait for Semaphore in Worker Thread

The kernel thread, `rpmsg_virtio_lite_thread`, runs in an infinite loop. It calls `nxsem_wait_uninterruptible` to block itself, waiting for notification of an interrupt event.

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

#### Step 3: Release Semaphore in Interrupt Callback

When hardware data arrives and triggers an interrupt, the `rpmsg_virtio_lite_callback` (acting as an **ISR**) is invoked. It uses `nxsem_post` to wake up the worker thread. To prevent unlimited semaphore count growth, the semaphore value (`semcount`) is checked.

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

## II. Using Message Queues for Data Transfer

When you need to pass **messages with data** between tasks or from an Interrupt Service Routine (ISR) to a task, you should use a message queue. Unlike semaphores, which are used only for synchronization, message queues can buffer fixed-size data packets within the kernel, enabling reliable asynchronous data exchange.

openvela follows the POSIX standard and provides `mqueue` interfaces. These interfaces are typically wrapped by the Virtual File System (VFS), allowing developers to manage message queues as if they were files.

### Design Pattern: Producer-Consumer Model

Message queues are ideal for implementing the producer-consumer design pattern:

- **Producer**: One or more tasks, or an ISR, responsible for generating data and sending it as a message to the queue.
- **Consumer**: One or more tasks responsible for receiving and processing messages from the queue.
- **Message Queue**: A thread-safe buffer between producers and consumers that decouples their execution logic.

**Execution Flow:**

1. **Initialization**: The consumer task opens or creates a named message queue upon startup.
2. **Sending**: When a producer has data to transfer, it packages the data into a message and calls the send function to place it in the queue. If the queue is full, the send operation may block or return an error immediately, depending on the configuration.
3. **Receiving**: The consumer task calls the receive function to wait for a message. If the queue is empty, the task enters a blocked state, releasing CPU resources until a new message arrives.

### Key Function Descriptions

openvela wraps the POSIX `mqueue` through file operation interfaces. The core functions are:

| Function          | Description                                                                                                                                                                                                            |
| :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file_mq_open`    | Creates or opens a named message queue. Queue attributes, such as the maximum number of messages (`mq_maxmsg`) and the maximum size of each message (`mq_msgsize`), are configured via the `struct mq_attr` parameter. |
| `file_mq_send`    | Sends a message to the specified message queue. This operation is atomic and supports message priorities.                                                                                                              |
| `file_mq_receive` | Receives a message from the message queue. If the queue is empty, the calling task will block and wait.                                                                                                                |

### Code Example: Message Queue in a Bluetooth (BT) Service

The following code snippets demonstrate how to wrap and use a message queue to transfer Bluetooth data buffers (`bt_buf`).

#### Step 1: Open and Configure the Message Queue

The `bt_queue_open` function wraps `file_mq_open` to initialize a message queue. The queue's capacity (`nmsgs`) must be specified when calling it.

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

#### Step 2: Send a Message

The `bt_queue_send` function wraps a pointer to a `bt_buf_s` struct into a message body and sends it to the queue.

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

#### Step 3: Receive a Message

The `bt_queue_receive` function blocks and waits until it successfully receives a message from the queue, then extracts the data buffer pointer from it.

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

#### Considerations

- **Message Queue Size**:

    Ensure that `mq_maxmsg` and `mq_msgsize` are set appropriately for the message queue to prevent message loss or task blocking.

- **Error Handling**:

    Always check the return values of message queue operations to prevent system exceptions caused by creation, sending, or receiving failures.

- **Priority Usage**:
  
    Set message priorities appropriately based on real-time requirements to ensure that high-priority messages are processed first.

- **Resource Cleanup**:
  
    Close and release message queue resources promptly when they are no longer needed.

## III. Deferring Interrupt Task Processing with Work Queues

In openvela, an Interrupt Service Routine (**ISR**) must execute in an extremely short amount of time to guarantee system real-time performance and responsiveness. Any long-running operations, such as loops, complex calculations, or calls to functions that might sleep, are strictly prohibited from being executed directly within an **ISR**.

To address this issue, the system provides a **Work Queue** mechanism. It allows an **ISR** to delegate time-consuming tasks to a dedicated kernel worker thread for deferred execution. This design pattern is commonly known as the Top-Half / Bottom-Half model.

- **Top-Half**: The **ISR** itself. It is responsible only for handling the most urgent hardware operations (e.g., reading a status register, clearing an interrupt flag), and then queuing the subsequent work for the work queue.
- **Bottom-Half**: The function executed by the work queue's worker thread. It runs in a non-interrupt context and can safely perform more complex and time-consuming tasks.

### Key Function Description

The core function `work_queue` is used to schedule a work item (a function and its arguments) onto a specified work queue.

```C
int work_queue(int qid, FAR struct work_s *work, worker_t worker, FAR void *arg, clock_t delay);
```

- `qid`: The ID of the target work queue, typically `HPWORK` or `LPWORK`.
- `work`: A pointer to a struct `work_s`. This structure must be statically or globally allocated, often as part of the device's private data. It must never be a local variable on the ISR's stack.
- `worker`: A function pointer to the bottom-half function to be deferred.
- `arg`: The argument to be passed to the `worker` function.
- `delay`: The delay before execution, in units of system ticks. If set to `0`, the work is scheduled to run as soon as possible.

### Code Example: Interrupt Handling in an ADC Driver

The following `ADC` driver code provides a perfect illustration of the top-half/bottom-half model.

#### Step 1: Schedule Work in the Interrupt Top-Half

`sam_adc_interrupt`, as the ISR (top-half), performs only the necessary register operations after an interrupt occurs. It then immediately calls `work_queue` to submit the time-consuming post-conversion processing task (`sam_adc_endconversion`) to the `HPWORK` queue and exits quickly.

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

#### Step 2: Execute the Task in the Worker Thread Bottom-Half

The `sam_adc_endconversion` function, as the bottom-half, is executed safely at a later time by the `hpwork` thread. It contains operations unsuitable for an **ISR**, such as loop processing, locking/unlocking, and calling upper-layer callback functions.

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

## Related Documents

- [Kernel Development Overview](./KernelDev.md)
