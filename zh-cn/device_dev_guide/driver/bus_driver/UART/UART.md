# UART 驱动适配与使用指南

\[ [English](../../../../../en/device_dev_guide/driver/bus_driver/UART/UART.md) | 简体中文 \]

## 一、概述

### 1、简介

UART（Universal Asynchronous Receiver/Transmitter，通用异步收发器），又称 Serial（串行通讯接口） 或简称串口，是一种在两个设备之间实现单工、半双工或全双工通信的技术。UART 通信基于串行数据传输，数据以一比特一比特的方式发送或接收，这与并行通信（一次传输多个比特）有所区别。

UART 的异步特性代表通信双方无需共享时钟信号（Clock），而是通过事先约定一致的通信参数来保持同步。UART 通讯所需的基本信号为：

- TX（发送端）：用于发送数据。
- RX（接收端）：用于接收数据。
- Ground（接地）：用于保持两个设备的公共参考电位。

### 2、参数

在使用 UART 通信时，双方必须预先将以下主要参数配置为相同，否则通信无法正常进行：

1. 波特率（Baud Rate）：通信速率，即每秒传输的比特数（如 9600 bps）。
2. 起始位（Start Bit）：用于标记一个数据帧的起始信号。
3. 数据位（Data Bits）：用于传输的有效数据长度，常见为 8 位或 9 位。
4. 奇偶校验位（Parity Bit）：用于错误检测，可设置为无校验、偶校验或奇校验。
5. 停止位（Stop Bit）：标记每个数据帧的结束，通常为 1 位或 2 位。

下图展示了这些参数所包含的数据帧结构：

![img](./figures/001.png)

### 3、实现

在 openvela 中，上层应用程序打开串口设备时，涉及以下过程：

1. 上层接口调用（Upper Half）：

    应用程序调用 `uart_open` 函数打开串口。

2. 底层适配层处理（Lower Half）：

    - `setup` 函数： 配置 UART 参数（如波特率、数据位等）。
    - `attach` 函数： 设置硬件中断处理。

3. 芯片厂商适配要求：

    芯片厂商需适配相关的南向接口（Lower Half），以支持 `setup` 和 `attach` 函数的正确执行。完成芯片驱动适配后，上层应用程序即可通过 openvela 提供的 北向接口（Upper Half） 控制串口功能。

## 二、驱动适配

本章节介绍如何在 openvela 上完成 UART 驱动的适配，包括必要的步骤与接口说明。

### 1、适配步骤

以下是 UART 驱动适配的主要步骤：

1. 使能配置：

    - 确保已启用 `CONFIG_SERIAL` 配置选项。
    - UART 接口的定义位于 `nuttx/include/nuttx/serial/serial.h` 中。

2. 实现 UART 驱动操作接口：

    - 定义并实现 `struct uart_ops_s` 结构体。

3. 驱动注册：

    - 在 `up_initialize` 函数中调用 `xxx_serialinit`，其中 `xxx` 通常表示体系架构（例如 `arm`）。
    - 在 `xxx_serialinit` 函数中调用 `uart_register(FAR const char *path, FAR uart_dev_t *dev)`，将 UART 驱动注册到系统中。

4. 实现设备数据结构：

    - 芯片厂商需实现 `struct uart_dev_s` 数据结构，其中的 `ops` 为之前实现的 `struct uart_ops_s` 的指针成员。
    - 若芯片支持 DMA（Direct Memory Access，直接内存访问），需要进一步适配 DMA 相关结构。

5. 缓冲区配置：

    - 在 `struct uart_dev_s` 中，实现 `xmit`（发送缓冲区）与 `recv`（接收缓冲区）实例，用于描述数据交换的上下文。

### 2、数据结构

#### `struct uart_dev_s`

`uart_dev_s` 是 UART 设备的上下文数据结构，通常由 Lower Half 提供，用于描述串口硬件的状态和功能。其核心定义如下：

```C
struct uart_dev_s
{
  /* State data */

  uint8_t              open_count;   /* Number of times the device has been opened */
  volatile bool        xmitwaiting;  /* true: User waiting for space in xmit.buffer */
  volatile bool        recvwaiting;  /* true: User waiting for data in recv.buffer */
#ifdef CONFIG_SERIAL_REMOVABLE
  volatile bool        disconnected; /* true: Removable device is not connected */
#endif
  bool                 isconsole;    /* true: This is the serial console */

#if defined(CONFIG_TTY_SIGINT) || defined(CONFIG_TTY_SIGTSTP) || \
    defined(CONFIG_TTY_FORCE_PANIC) || defined(CONFIG_TTY_LAUNCH)
  pid_t                pid;          /* Thread PID to receive signals (-1 if none) */
#endif

#ifdef CONFIG_SERIAL_TERMIOS
  /* Terminal control flags */

  tcflag_t             tc_iflag;     /* Input modes */
  tcflag_t             tc_oflag;     /* Output modes */
  tcflag_t             tc_lflag;     /* Local modes */
#endif

  /* Semaphores & mutex */

  sem_t                xmitsem;      /* Wakeup user waiting for space in xmit.buffer */
  sem_t                recvsem;      /* Wakeup user waiting for data in recv.buffer */
  mutex_t              closelock;    /* Locks out new open while close is in progress */
  mutex_t              polllock;     /* Manages exclusive access to fds[] */

  /* I/O buffers */

  struct uart_buffer_s xmit;         /* Describes transmit buffer */
  struct uart_buffer_s recv;         /* Describes receive buffer */

  /* DMA transfers */

#ifdef CONFIG_SERIAL_TXDMA
  struct uart_dmaxfer_s dmatx;       /* Describes transmit DMA transfer */
#endif
#ifdef CONFIG_SERIAL_RXDMA
  struct uart_dmaxfer_s dmarx;       /* Describes receive DMA transfer */
#endif

  /* Driver interface */

  FAR const struct uart_ops_s *ops;  /* Arch-specific operations */
  FAR void            *priv;         /* Used by the arch-specific logic */

  /* The following is a list if poll structures of threads waiting for
   * driver events. The 'struct pollfd' reference for each open is also
   * retained in the f_priv field of the 'struct file'.
   */

  struct pollfd *fds[CONFIG_SERIAL_NPOLLWAITERS];
};
```

关键字段说明：

- `ops`：

    指向 `struct uart_ops_s` 的指针，定义 UART 驱动的操作集。例如：

    - `setup()` 配置硬件参数。
    - `send()` 将数据写入串口发送缓冲区。
    - `receive()` 读取接收到的数据。

- `priv`：

    UART 私有数据区域，供 UART 硬件驱动程序存储特定信息（如硬件地址、FIFO 缓冲区指针等）。

- `xmit` 和 `recv`：

    `xmit` 描述发送缓冲区，`recv` 描述接收缓冲区。这两个字段是串口硬件和上层应用之间进行数据交互的核心结构。

#### `struct uart_ops_s`

`struct uart_ops_s` 描述 UART 的底层操作接口，是适配的核心部分。以下为接口的主要方法列表：

```C
struct uart_ops_s
{
  /* Configure the UART baud, bits, parity, fifos, etc. This method is called
   * the first time that the serial port is opened. For the serial console,
   * this will occur very early in initialization; for other serial ports
   * this will occur when the port is first opened. This setup does not
   * include attaching or enabling interrupts. That portion of the UART setup
   * is performed when the attach() method is called.
   */

  CODE int (*setup)(FAR struct uart_dev_s *dev);

  /* Disable the UART.  This method is called when the serial port is closed.
   * This method reverses the operation the setup method.
   * NOTE that the serial console is never shutdown.
   */

  CODE void (*shutdown)(FAR struct uart_dev_s *dev);

  /* Configure the UART to operation in interrupt driven mode. This method is
   * called when the serial port is opened. Normally, this is just after the
   * the setup() method is called, however, the serial console may operate in
   * a non-interrupt driven mode during the boot phase.
   *
   * RX and TX interrupts are not enabled when by the attach method (unless
   * the hardware supports multiple levels of interrupt enabling). The RX
   * and TX interrupts are not enabled until the txint() and rxint() methods
   * are called.
   */

  CODE int (*attach)(FAR struct uart_dev_s *dev);

  /* Detach UART interrupts. This method is called when the serial port is
   * closed normally just before the shutdown method is called.
   * The exception is the serial console which is never shutdown.
   */

  CODE void (*detach)(FAR struct uart_dev_s *dev);

  /* All ioctl calls will be routed through this method */

  CODE int (*ioctl)(FAR struct file *filep, int cmd, unsigned long arg);

  /* Called (usually) from the interrupt level to receive one character from
   * the UART.  Error bits associated with the receipt are provided in the
   * the return 'status'.
   */

  CODE int (*receive)(FAR struct uart_dev_s *dev, FAR unsigned int *status);

  /* Call to enable or disable RX interrupts */

  CODE void (*rxint)(FAR struct uart_dev_s *dev, bool enable);

  /* Return true if the receive data is available */

  CODE bool (*rxavailable)(FAR struct uart_dev_s *dev);

#ifdef CONFIG_SERIAL_IFLOWCONTROL
  /* Return true if UART activated RX flow control to block more incoming
   * data.
   */

  CODE bool (*rxflowcontrol)(FAR struct uart_dev_s *dev,
                             unsigned int nbuffered, bool upper);
#endif

#ifdef CONFIG_SERIAL_TXDMA
  /* Start transfer bytes from the TX circular buffer using DMA */

  CODE void (*dmasend)(FAR struct uart_dev_s *dev);
#endif

#ifdef CONFIG_SERIAL_RXDMA
  /* Start transfer bytes from the TX circular buffer using DMA */

  CODE void (*dmareceive)(FAR struct uart_dev_s *dev);

  /* Notify DMA that there is free space in the RX buffer */

  CODE void (*dmarxfree)(FAR struct uart_dev_s *dev);
#endif

#ifdef CONFIG_SERIAL_TXDMA
  /* Notify DMA that there is data to be transferred in the TX buffer */

  CODE void (*dmatxavail)(FAR struct uart_dev_s *dev);
#endif

  /* This method will send one byte on the UART */

  CODE void (*send)(FAR struct uart_dev_s *dev, int ch);

  /* Call to enable or disable TX interrupts */

  CODE void (*txint)(FAR struct uart_dev_s *dev, bool enable);

  /* Return true if the tranmsit hardware is ready to send another byte.
   * This is used to determine if send() method can be called.
   */

  CODE bool (*txready)(FAR struct uart_dev_s *dev);

  /* Return true if all characters have been sent.  If for example, the UART
   * hardware implements FIFOs, then this would mean the transmit FIFO is
   * empty.  This method is called when the driver needs to make sure that
   * all characters are "drained" from the TX hardware.
   */

  CODE bool (*txempty)(FAR struct uart_dev_s *dev);
};
```

接口方法与功能说明：

- `setup()`

    - 功能： 初始化硬件串口，包括配置波特率、数据位、校验方式等基本参数。
    - 应用场景： 在设备首次打开串口时调用。

- `shutdown()`

    - 功能： 禁用当前串口，释放硬件资源。
    - 应用场景： 在设备关闭串口时调用。

- `attach()`

    - 功能： 绑定串口的中断服务函数，为硬件中断驱动创建关联。
    - 应用场景： 串口需要支持中断时调用。

- `detach()`

    - 功能： 解绑串口的中断服务函数，解除硬件与中断的关联。
    - 应用场景： 停用中断驱动时调用。

- `ioctl()`

    - 功能： 执行命令（cmd）指定的串口操作，提供灵活的配置与控制接口。
    - 应用场景： 各类非标准化的特殊操作。

- `receive()`

    - 功能： 从串口硬件接收数据，并返回当前数据状态。
    - 应用场景： 数据传输 API 中用于读取设备传来的字节。

- `rxint()`

    - 功能： 开启或关闭串口的接收中断。
    - 应用场景： 当需要通过中断机制接收时调用。

- `rxavailable()`

    - 功能： 检查串口接收缓冲区中是否有数据可读。
    - 应用场景： 判断是否需要调用 `.receive()` 读取数据。

- `rxflowcontrol()`

    - 功能： 控制接收硬件的流量，当缓冲区状态满足特定要求时启用或禁用接收流控制。
    - 应用场景： 配合硬件流控制的场景。

DMA 相关接口（若硬件支持 DMA）说明：

- `dmasend()`

    - 功能： 使用 DMA 从循环缓冲区中提取并发送数据到串口硬件。
    - 应用场景： 在大规模或高性能数据传输中提升效率。

- `dmareceive()`

    - 功能： 使用 DMA 从串口硬件接收数据并存储到循环缓冲区中。
    - 应用场景： 在高吞吐量数据写入场景中。

- `dmarxfree()`

    - 功能： 通知 DMA 接收模块缓冲区还有剩余空间。
    - 应用场景： 缓存溢出或流量中断时告知 DMA。

- `dmatxavail()`

    - 功能： 通知 DMA 模块有待发送数据，可执行传输操作。
    - 应用场景： 高效发送大数据块时调用。

数据发送相关接口：

- `send()`

    - 功能： 向串口发送数据，通常为写入一个字节到发送缓冲区。
    - 应用场景： 数据输出流程的核心操作。

- `txint()`

    - 功能： 开启或关闭串口的发送中断。
    - 应用场景： 用于处理串口发送队列的中断机制。

- `txready()`

    - 功能： 检查串口是否准备好发送新的数据。
    - 应用场景： 发送数据前进行状态查询。

- `txempty()`

    - 功能： 检查串口硬件是否已完成所有数据发送，包括缓冲区数据传输。
    - 应用场景： 确保所有发送任务完成后再执行其他操作（如关闭串口）。

实际代码可以参考 `nuttx/arch/arm/src/stm32/stm32_serial.c`。

## 三、使用 UART 字符设备驱动

本章节介绍如何在 openvela 系统中如何使用 UART 字符设备驱动，包括注册、打开、读写、轮询和关闭等关键流程。

### 1、`uart_register`

`uart_register` 是对 `register_driver` 的封装，用于将 UART 驱动注册为系统设备节点。

```C
int register_driver(FAR const char *path,
                    FAR const struct file_operations *fops,
                    mode_t mode, FAR void *priv)
```

`register_driver` 的主要作用包括以下三方面：

1. 查找或创建设备节点：根据传入的路径 `path`，检查是否存在对应的 `inode`，如果不存在，则为该路径创建一个新的 `inode`。
2. 绑定驱动文件操作集：将具体驱动的文件操作结构体 `struct file_operations fops` 写入到与路径 `path` 关联的 `inode` 中。
3. 设置私有数据：将私有数据 `priv` 设置到与路径 `path` 对应的 `inode` 中。在 UART 驱动中，此 `priv` 通常为 `uart_dev_t *`。

对应的简化流程图如下：

![img](./figures/002.svg)

### 2、`struct file_operations`

在 UART 驱动中，文件操作结构体 `struct file_operations` 的典型实现如下：

```C
static const struct file_operations g_serialops =
{
  uart_open,  /* open */
  uart_close, /* close */
  uart_read,  /* read */
  uart_write, /* write */
  0,          /* seek */
  uart_ioctl, /* ioctl */
  uart_poll   /* poll */
#ifndef CONFIG_DISABLE_PSEUDOFS_OPERATIONS
  , NULL      /* unlink */
#endif
};
```

### 3、`uart_open`

`uart_open` 函数的主要作用是通过调用 `uart_setup` 初始化串口设备，同时绑定中断服务函数，为设备正常工作做好准备。

```C
fs/vfs/fs_open.c
|_ nx_vopen
   |_ file_vopen
      |_ inode->u.i_mops->open(filep, desc.relpath, oflags, mode) == uart_open
         |_ uart_setup == dev->ops->setup    //setup调用的地方
         |_ uart_attach  == esp32c3_attach   //attach调用的地方
            |_ irq_attach(priv->irq, uart_handler, dev);
         |_ uart_dmarxfree(dev)  //如果存在读dma的话，触发该操作
```

1. 硬件初始化： 调用 `uart_setup` 完成硬件参数配置，如波特率、数据位和校验方式。
2. 绑定中断： 调用 `uart_attach` 绑定中断服务函数，确保串口设备支持中断驱动。
3. DMA 配置： 如果启用了接收 DMA，则进一步调用 `uart_dmarxfree` 提供支持。

### 4、`uart_read`

`uart_read` 函数的主要功能是从接收缓冲区 `dev->recv->buff` 中读取数据并返回给上层调用者。如果缓冲区空，则通过阻塞或 DMA 获取数据。

```C
fs/vfs/fs_read.c
|_ nx_read
   |_ file_read
      |_ inode->u.i_ops->read == uart_read(filep, buffer, buflen)
         |_ if (rxbuf->head != tail)    //如果读缓冲区里有数据就直接读走了
            |_ ch = rxbuf->buffer[tail];
            |_ *buffer++ = ch;
         |_ else
            |_ uart_dmarxfree/uart_enablerxint //如果存在读dma的话触发该操作，否则打开读中断
            |_ dev->recvwaiting = true;
            |_ ret = nxsem_wait(&dev->recvsem);  //阻塞的read
         |_ uart_enablerxint   // == dev->ops->rxint  , rxint调用的地方
         |_ uart_dmarxfree(dev);  //在读操作完成之后缓冲区肯定是存在空间的，如果存在读dma触发该操作
```

1. 直接读取数据：若缓冲区有数据，直接返回。
2. 缓冲区为空处理：

   - 若启用 DMA，调用 `uart_dmarxfree` 提取数据。
   - 若不启用 DMA，调用 `uart_enablerxint` 启用接收中断。

3. 阻塞读取：调用 `nxsem_wait(&dev->recvsem)`，阻塞当前进程，直到数据准备完成。

### 5、`uart_write`

`uart_write` 用于将数据写入串口设备的发送缓冲区 (`dev->xmit->buffer`)，通过调用 `uart_putxmitchar` 函数实现具体数据的写入，并根据需要触发中断或 DMA 操作。

```C
fs/vfs/fs_write.c
write
|_ nx_write
   |_ file_write
      |_ inode->u.i_ops->write(filep, buf, nbytes) == uart_write
         |_ uart_disabletxint  //txint调用的地方 
         |_ uart_putxmitchar(dev, ch, oktoblock); //把数据往缓冲区放。这个函数也会判断是否使用写dma完成发送，uart_dmatxavail。
            |_ if (nexthead != dev->xmit.tail) //如果写缓冲区有空间，把数据放入写缓冲区后返回
            |_ else //开中断，等待中断给自己腾出写空间把自己唤醒
               |_ uart_enabletxint(dev);   //txint调用的地方
               |_ nxsem_wait(&dev->xmitsem);
         #ifdef CONFIG_SERIAL_TXDMA
         |_ uart_dmatxavail(dev); //如果有写dma的话，使用dma完成发送
         #endif
         |_ uart_enabletxint(dev) == esp32c3_txint  //如果使用了上面的dma的话，这个函数会直接返回，而不产生发送数据的动作
```

1. 禁用发送中断： 确保写入期间不会发生中断干扰。
2. 将数据写入缓冲区： 调用 `uart_putxmitchar(dev, ch, oktoblock)` 将数据放入带锁保护的发送缓冲区，并判断是否阻塞写入操作。
3. （可选）使用 DMA：如果启用了 DMA，通过 `uart_dmatxavail` 触发 DMA 进行高效传输。
4. 开启发送中断：调用 `uart_enabletxint` 确保写操作完成后由中断机制控制发送缓冲区的数据。

### 6、`uart_poll`

`uart_poll` 提供了一种非阻塞模式下的异步操作，用于监听设备的可读和可写事件。在 UART 驱动中，`uart_poll` 的等待、通知与唤醒机制是一项重要功能。

#### `uart_poll` 等待机制

通过 `poll`，应用程序可以在非阻塞模式下监听设备的状态变化（如设备是否可读或可写）。

```text
fs/vfs/fs_poll.c
|_ poll_setup(kfds, nfds, &sem);
   |_ poll_fdsetup(fds[i].fd, &fds[i], true)
      |_ file_poll(filep, fds, setup);
         |_ inode->u.i_ops->poll(filep, fds, setup); == uart_poll
   |_ if(timeout<0) 
      |_ nxsem_wait(&sem);//阻塞的poll
```

1. 初始化轮询状态：

    调用 `poll_setup()` 函数对 `pollfd` 列表进行初始化，记录被监听的文件描述符及其关注的事件（如 `POLLIN` 或 `POLLOUT`）。

2. 关联驱动的 `poll` 方法：

    通过 `inode` 文件节点调用与 `uart_poll` 对应的具体实现，监视设备可读/可写状态。

3. （可选）阻塞等待：

    如果设定了超时时间（`timeout` 参数），`poll` 会阻塞线程至超时时间耗尽，或事件被触发。

#### `uart_poll` 唤醒机制

当串口硬件发生状态变化（接收到新数据或缓冲区释放空间）时，通过中断事件触发唤醒机制。以下为 `uart_poll` 的典型中断处理流程：

```text
arch/risc-v/src/esp32c3/esp32c3_serial.c
|_ int_status = getreg32(UART_INT_ST_REG(priv->id));
|_ if (int_status & tx_mask)
   |_ uart_xmitchars
      |_ while (dev->xmit.head != dev->xmit.tail && uart_txready(dev)) // txready调用的地方
         |_ uart_send(dev, dev->xmit.buffer[dev->xmit.tail])  //send调用的地方，发完缓冲区里所有数据
         |_ uart_datasent
            |_ poll_notify(dev->fds, CONFIG_SERIAL_NPOLLWAITERS, POLLOUT)//唤醒poll等待的写者
            |_ nxsem_post(&dev->xmitsem) //唤醒write等待的写者
|_ if (int_status & rx_mask)
   |_ uart_recvchars
      |_ uart_rxavailable(dev)            //rxavailable调用的地方
      |_ uart_rxflowcontrol               //rxflowcontrol调用的地方
      |_ ch = uart_receive(dev, &status)  //receive调用的地方
      |_ uart_check_special(dev, &ch, 1)  //处理control character的地方
      |_ uart_datareceived(dev)          
         |_ poll_notify(dev->fds, CONFIG_SERIAL_NPOLLWAITERS, POLLIN); 
            |_ fds->cb(fds); == poll_default_cb
               |_ nxsem_post(pollsem)    //如果有阻塞的poll，唤醒
         |_ nxsem_post(&dev->recvsem);   //如果有阻塞的read，唤醒
      |_ nxsig_kill(dev->pid, signo);    //如果signo!=0，发signal的地方
```

##### 写事件处理流程

1. 触发条件：

    当发送缓冲区中数据全部传输完成后，硬件会触发写中断（`tx_mask`）。

1. 中断操作：

    - 调用 `uart_xmitchars` 函数，将数据从发送缓冲区写入硬件 FIFO。
    - 通过 `poll_notify` 通知应用程序可写事件（`POLLOUT`），唤醒等待写入的线程或任务。
    - 若线程被阻塞在写操作，调用 `nxsem_post(&dev->xmitsem)` 唤醒线程。

##### 读事件处理流程

1. 触发条件：

    当硬件接收到数据时，触发读中断（`rx_mask`）。

2. 中断操作：

   - 调用 `uart_recvchars` 函数，从硬件接收缓冲中读取数据。
   - 调用 `poll_notify` 通知应用程序可读事件（`POLLIN`），唤醒等待读取的线程或任务。
   - 若线程被阻塞在读取操作，调用 `nxsem_post(&dev->recvsem)` 唤醒线程。

### 7、`uart_close`

`uart_close` 函数用于释放 UART 设备和相关的系统资源。在 openvela 系统中，`uart_close` 是设备关闭流程的核心操作，包括禁用中断、清空发送缓冲区以及回收硬件资源。

```text
 fs/inode/fs_files.c
 int close(int fd)
 |_ nx_close(fd)
    |_ file_close(&file)
       |_ inode->u.i_ops->close(filep)  //== uart_close
          |_ uart_disablerxint(dev)
          |_ if ((filep->f_oflags & O_NONBLOCK) == 0)
             |_ uart_tcdrain  //把发送缓冲区和硬件fifo里的数据都发送完成
                |_ uart_txempty //txempty调用的地方
          |_ uart_detach(dev)       //detach调用的地方
          |_ if (!dev->isconsole)
             |_ uart_shutdown(dev)  //shutdown调用的地方
          |_ uart_datareceived(dev)
```

1. 禁用接收中断：

    调用了 `uart_disablerxint` 禁用串口设备的接收中断，避免设备释放后仍触发中断导致的不稳定行为。

2. 清空发送缓冲区：

    如果文件操作未设置非阻塞模式（`filep->f_oflags & O_NONBLOCK == 0`），`uart_tcdrain` 会确保发送缓冲区和硬件 FIFO 中的数据全部发送完成。通过调用 `uart_txempty` 判断是否已完成数据传输。

3. 解绑中断服务：

    调用 `uart_detach` 解绑串口设备与中断服务的关联，确保中断资源被彻底释放。

4. 释放硬件资源：

    如果设备不是控制台（`!dev->isconsole`），调用 `uart_shutdown` 完成硬件资源的回收和释放。

5. 其他清理操作：

    在关闭设备后，调用 `uart_datareceived` 等方法对剩余缓冲数据进行处理，避免资源泄露。

## 四、操作 UART 设备节点

本章介绍如何在 openvela 中操作 UART 设备节点。用户提供的串口通信接口完全遵循 POSIX 标准，包括常用的打开、读写、轮询事件和控制操作。开发者可以参考本文和 `man` 手册页实现对 UART 节点的高效访问和配置。

### 1、UART 设备节点的接口操作

用户可以通过以下 POSIX 标准接口操作 UART 设备节点，例如 `/dev/console` 或 `/dev/ttyS0`。

以下是常用的文件操作接口及其示例：

```C
int fd = open("/dev/console", O_RDWR);
int ret = read(fd, buf, count);
int ret  = write(fd, buf, count);
int poll(struct pollfd *fds, nfds_t nfds, int timeout);  
//可以poll的事件见sys/poll.h，常见的就是POLLIN/POLLOUT
int ioctl(int fd, unsigned long request, ...);
//可用的ioctl命令定义在include/nuttx/serial/tioctl.h文件中，里面有各个命令的详细定义
close(fd); 
 
```

- `open` 和 `close`： 负责打开和关闭设备节点。
- `read` 和 `write`： 用于从 UART 设备读取数据或向设备写入数据。
- `poll`**：** 检测非阻塞模式下的 UART 事件，如可读（`POLLIN`）和可写（`POLLOUT`）。事件类型可参考 `sys/poll.h` 文件。
- `ioctl`**：** 提供对 UART 的详细控制参数，如设置波特率、数据位等配置。支持的操作命令定义在 `include/nuttx/serial/tioctl.h` 中。

### 2、使用 `ioctl` 配置 UART 参数

所有可以通过 `ioctl` 配置的参数都定义在 `struct termios` 结构体中。具体参数含义及取值可参考 `termios.h` 文件或查看 `man termios` 手册页。`struct termios` 结构体定义如下：

```C
nuttx/include/termios.h

struct termios
{
  /* Exposed fields defined by POSIX */

  tcflag_t  c_iflag;        /* Input modes */
  tcflag_t  c_oflag;        /* Output modes */
  tcflag_t  c_cflag;        /* Control modes */
  tcflag_t  c_lflag;        /* Local modes */
  cc_t      c_cc[NCCS];     /* Control chars */

  /* Implementation specific fields.  For portability reasons, these fields
   * should not be accessed directly, but rather through only through the
   * cf[set|get][o|i]speed() POSIX interfaces.
   */

  speed_t c_speed;          /* Input/output speed (non-POSIX) */
};
```

- `c_speed`**：** 表示硬件波特率参数，需操作硬件寄存器。
- `c_cc`**：** 表示控制字符参数，与软件有关，无需操作硬件。

#### 示例：设置 UART RAW mode

```C
tcgetattr(ctx->recvfd, &term);
cfmakeraw(&term);
tcsetattr(ctx->recvfd, TCSANOW, &term);
```

或

```C
file_ioctl(&cmux->filep, TCGETS, &term);
cfmakeraw(&term);
file_ioctl(&cmux->filep, TCSETS, &term);
```

#### 示例：设置 UART 波特率

以下代码展示了如何通过 `termios` 结构体和 `ioctl` 接口设置 UART 的波特率。

```C
ioctl(fd, TCGETS, termios);//把当前的参数获取出来
int cfsetspeed(FAR struct termios *termios, speed_t speed);//把termios设置好，speed可以取的值见termios.h
ioctl(fd, TCSETS, termios);//把修改设置下去，lower half的ioctl怎么处理termios->c_speed这个值，就看厂商自己实现了。
```

#### 示例：内核驱动访问 UART 设备节点

在内核层，驱动程序可以通过 `file_open` 等接口访问 UART 设备节点。以下为常用接口对应的操作方法：

```C
int file_open(FAR struct file *filep, FAR const char *path, int oflags, ...);
int file_close(FAR struct file *filep);
ssize_t file_read(FAR struct file *filep, FAR void *buf, size_t nbytes);
ssize_t file_write(FAR struct file *filep, FAR const void *buf,
                   size_t nbytes);
int file_ioctl(FAR struct file *filep, int req, ...);
```

这些接口可被用来访问 UART 的节点文件，从而实现对 UART 设备的底层操控。

## 五、测试用例

本章介绍 openvela 系统中 UART 驱动测试程序的用法，并详细解析了测试案例的核心实现和运行步骤。通过这些指导，开发者可以验证 UART 驱动在各类操作（如读、写、多数据传输）中的正确性。

### 1、测试程序路径

在 openvela 系统中，UART 驱动的测试程序源码 `apps/testing/drivertest` 目录下，编译出成功后生成的测试程序为 `cmocka_driver_uart`。

### 2、打开配置选项

要成功编译和运行该测试程序，需要打开以下三个配置选项：

```C
+CONFIG_TESTING_CMOCKA=y
+CONFIG_TESTING_DRIVER_TEST=y
+CONFIG_TESTING_DRIVER_TEST_SIMPLE=y
```

### 3、测试用例

![img](./figures/003.png)

在 UART 驱动的测试程序中，定义了以下三条核心测试用例：

1. `write_default`：将字符序列 `0-9-a-z` 写入指定的 UART 设备（如 `/dev/console`），用于验证设备的写入功能是否正常。
2. `read_default`：从设备中读取数据，并验证是否能够正确读取到与写入内容相同的字符序列。若读写数据不符，则此测试失败。
3. `burst_test`：模拟快速输入场景，测试过程包括以下步骤：

    - 输入数字 `0` 并按下回车键。
    - 再输入符号 `#` 并按下回车键确认。
    - 测试完成，验证输入是否符合预期。

运行以上测试后，如果成功，程序将输出`[  PASSED  ] 3 test(s)`。

### 4、测试程序主函数

以下是 UART 测试程序的主代码结构，采用 CMocka 框架进行测试。

```C
int main(int argc, FAR char *argv[])
{
  struct test_confs_s confs =
  {
    .dev_path = CONFIG_TESTING_DRIVER_TEST_UART_DEVICE
  };

  parse_args(argc, argv, &confs);

  const struct CMUnitTest tests[] =
    {
      cmocka_unit_test_prestate_setup_teardown(write_default, setup,
                                               teardown, &confs),
      cmocka_unit_test_prestate_setup_teardown(read_default, setup,
                                               teardown, &confs),
      cmocka_unit_test_prestate_setup_teardown(burst_test, setup,
                                               teardown, &confs),
    };

  return cmocka_run_group_tests(tests, NULL, NULL);
}
```

## 六、参考资料

以下资源提供了关于 UART 驱动及 TTY 工作原理的进一步说明：

- [NuttX RTOS for PinePhone: UART Driver](https://lupyuen.github.io/articles/uart)
- [The TTY Demystified](https://www.linusakesson.net/programming/tty/)