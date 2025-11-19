# 适配 I2C Master 驱动

[ [English](../../../../../en/device_dev_guide/driver/bus_driver/I2C/i2c_master_guide.md) | 简体中文 ]

本文档介绍如何为 openvela 适配一个标准的 I2C Master 驱动，使其能够作为总线主设备工作。

## 一、驱动框架层级

I2C Master 驱动的开发涉及驱动层、板级层和应用层，它们之间的协作关系如下：

### 驱动层 (Driver)

负责实现芯片相关的 I2C 底层硬件操作。此层需要封装硬件细节，并向上层提供一个标准化的 `i2c_master_s` 句柄。

```C
/* 1. 定义底层操作函数集 */
static const struct i2c_ops_s bl602_i2c_ops =
{
    .transfer = bl602_i2c_transfer,
#ifdef CONFIG_I2C_RESET
    .reset = bl602_i2c_reset
#endif
};

/* 2. 定义私有数据结构，包含操作函数集和配置信息 */
static struct bl602_i2c_priv_s bl602_i2c0_priv =
{
    .ops      = &bl602_i2c_ops,
    .config   = &bl602_i2c0_config,
};

/* 3. 实现初始化函数，返回标准的 I2C Master 句柄 */
struct i2c_master_s *bl602_i2cbus_initialize(int port)
{
    priv = (struct bl602_i2c_priv_s *)&bl602_i2c0_priv;
    
    return (struct i2c_master_s *)priv;
}
```

### 板级层 (Board)

在系统启动阶段，调用驱动层的初始化函数获取 I2C 总线句柄。根据需求，可以选择性地将该总线注册为字符设备（如 `/dev/i2c-0`），或直接传递给其他内核驱动（如传感器驱动）使用。

```C
/* 获取 I2C 总线句柄 */
i2c_bus = bl602_i2cbus_initialize(0);

/* 将总线注册为 /dev/i2c0 */
i2c_register(i2c_bus, 0);
```

### 应用层 (Application)

通过标准的 POSIX 文件接口（`open`, `ioctl` 等）访问已注册的 `/dev/i2c-N` 设备节点，从而与挂载在总线上的 I2C 从设备通信。

```C
fd = open("/dev/i2c", O_RDWR);
ioctl(fd, );
...
```

## 二、适配南向接口 (Lower Half)

南向接口适配的核心任务是实现芯片的底层驱动，并提供一个标准的初始化函数 `xxx_i2cbus_initialize()`，其中 `xxx` 代表芯片（Chip）名称。

### 1、Kconfig 配置选项

请在 Kconfig 中启用以下配置项以支持 I2C Master 驱动：

```Makefile
CONFIG_I2C=y          # 必需，启用 I2C 子系统
CONFIG_I2C_DRIVER=y   # 必需，启用 I2C 字符设备驱动上层
CONFIG_I2C_RESET=y    # 可选，如果需要支持总线复位功能
```

### 2、核心数据结构

openvela I2C Master 驱动围绕 `struct i2c_master_s` 和 `struct i2c_ops_s` 这两个核心结构进行抽象。

```C
/*
 * I2C Master 操作函数集。
 * 驱动开发者需要实现其中的函数指针，特别是 transfer 函数。
 */
struct i2c_ops_s
{
  /* 核心传输函数，必需 */
  CODE int (*transfer)(FAR struct i2c_master_s *dev,
                       FAR struct i2c_msg_s *msgs, int count);
#ifdef CONFIG_I2C_RESET
  /* 可选的总线复位函数 */
  CODE int (*reset)(FAR struct i2c_master_s *dev);
#endif
};

/*
 * I2C Master 设备句柄。
 * 这是南向驱动向上层提供的标准接口。
 * 开发者通常会定义一个包含此结构的私有设备结构体。
 */
struct i2c_master_s
{
  FAR const struct i2c_ops_s *ops; /* 指向操作函数集的指针 */
};
```

### 3、驱动入口函数说明

您需要根据下表的要求，在芯片驱动文件（`xxx_i2c.c`）中实现 `xxx_i2cbus_initialize()` 函数。

| **项目**     | **描述**                                                                                                                                                             |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **函数原型** | `struct i2c_master_s *xxx_i2cbus_initialize(int port)`                                                                                                               |
| **参数**     | `port`：I2C 总线端口号。如果芯片支持多路 I2C，您需要根据此参数进行多路配置。                                                                                         |
| **返回值**   | 返回一个标准的 `i2c_master_s` 操作句柄。如果初始化失败，则返回 `NULL`。                                                                                              |
| **实现内容** | 初始化 I2C 控制器所需的时钟和 GPIO。如果使用中断模式，还需配置并使能中断。填充并返回一个包含 `transfer` 函数指针的 `i2c_master_s` 句柄，用于处理上层的数据传输请求。 |
| **文件位置** | chip 路径下的 `xxx_i2c.c`，`xxx` 为 chip 名称。                                                                                                                      |
| **调用位置** | board 路径下的 `xxx_bringup.c` 里调用，`xxx` 为 `board` 名字。                                                                                                       |

### 4、适配实现步骤

本节通过代码示例，展示如何分步完成 I2C Master 驱动的适配。

- **参考实现**：[bl602_i2c.c](https://github.com/apache/nuttx/blob/master/arch/risc-v/src/bl602/bl602_i2c.c)

#### 步骤一：定义私有设备结构体

我们强烈建议您定义一个私有结构体，用于封装 I2C 控制器的所有状态信息，例如配置、锁、信号量以及运行时数据等。以下是 `bl602` 芯片的私有结构体示例：

> **核心要点：结构体成员布局** 为确保类型安全转换，私有结构体的**第一个成员**必须是 `const struct i2c_ops_s *ops;`。这使得框架可以将您的私有结构体指针安全地转换为标准的 `struct i2c_master_s *` 句柄。

<details>
<summary>点击展开代码</summary>

```C
/* 位于: arch/risc-v/src/bl602/bl602_i2c.c */

/* bl602 I2C 驱动的私有数据结构 */
struct bl602_i2c_priv_s
{
  /* 必须作为第一个成员，以兼容 i2c_master_s 类型转换 */
  const struct i2c_ops_s *ops; /* Standard I2C operations */

  /* 端口配置 */
  const struct bl602_i2c_config_s *config;

  /* 状态与同步机制 */
  uint8_t  subflag;   /* Sub address flag */
  uint32_t subaddr;   /* Sub address */
  uint8_t  sublen;    /* Sub address length */
  mutex_t  lock;      /* Mutual exclusion mutex */
  sem_t    sem_isr;   /* Interrupt wait semaphore */

  /* 运行时数据 */
  /* I2C work state */
  uint8_t i2cstate;

  struct i2c_msg_s *msgv; /* Message list */

  uint8_t msgid; /* Current message ID */
  ssize_t bytes; /* Processed data bytes */
  int     refs;  /* Reference count */
};
```

</details>

#### 步骤二：实现初始化函数 `xxx_i2cbus_initialize()`

此函数负责完成硬件初始化，并返回一个配置好的 I2C Master 句柄。

<details>
<summary>点击展开代码</summary>

```C
struct i2c_master_s *bl602_i2cbus_initialize(int port)
{
  struct bl602_i2c_priv_s         *priv;
  const struct bl602_i2c_config_s *config;

  /* 1. 根据 port 号获取对应的私有设备实例 */
  switch (port)
    {
#ifdef CONFIG_BL602_I2C0
    case 0:
      priv = (struct bl602_i2c_priv_s *)&bl602_i2c0_priv;
      break;
#endif
    default:
      return NULL;
    }

  config = priv->config;
/*************************************************
此部分是把IIC配置为中断，不配置中断可以把此部分替换成IIC GPIO以及时钟初始化
  
  nxmutex_lock(&priv->lock);
  if (++priv->refs > 1)
  {
    nxmutex_unlock(&priv->lock);
    return (struct i2c_master_s *)priv;
  }

  bl602_configgpio(BOARD_I2C_SCL);
  bl602_configgpio(BOARD_I2C_SDA);

  bl602_i2c_set_freq(config->clk_freq);
  bl602_i2c_disable();
  up_enable_irq(BL602_IRQ_I2C);
  bl602_i2c_intmask(I2C_INT_ALL, 1);
  irq_attach(BL602_IRQ_I2C, bl602_i2c_irq, priv);
**************************************************/
  nxmutex_unlock(&priv->lock);

   /* 2. 返回私有结构体指针，并强制转换为标准句柄类型 */
  return (struct i2c_master_s *)priv;
}
```

</details>

#### 步骤三：在板级代码中调用

在板级初始化代码（`xxx_bringup.c`）中，调用芯片驱动提供的初始化函数，并根据需要将 I2C 总线注册为系统设备。

- **参考实现**：[bl602_bringup.c](https://github.com/apache/nuttx/blob/master/boards/risc-v/bl602/bl602evb/src/bl602_bringup.c)

<details>
<summary>点击展开代码</summary>

```C
#ifdef CONFIG_I2C
  /* 初始化 I2C 总线 0 */
  i2c_bus = bl602_i2cbus_initialize(0);
  
  /* 2. (可选) 将总线注册为 /dev/i2c-0 设备节点 */
  i2c_register(i2c_bus, 0);
#endif
```

</details>

**`i2c_register()`** **使用说明**

- **注册为设备节点**：调用 `i2c_register(i2c_bus, N)` 会创建字符设备节点 `/dev/i2c-N`。这使得用户空间应用（如测试程序、`i2ctool`）能通过标准文件接口访问 I2C 总线。
- **仅供内核使用**：如果某个 I2C 总线仅供内核中的其他驱动（如板载传感器）使用，您可以不调用 `i2c_register()`。直接将 `i2c_bus` 句柄传递给相应驱动的注册函数即可。

## 三、北向使用

当 I2C Master 驱动被成功注册后，系统会创建 `/dev/i2c-N` 格式的设备节点（例如 `/dev/i2c-0`, `/dev/i2c-1` 等）。应用程序可以通过这些设备节点，使用标准的 POSIX 文件接口与挂载在 I2C 总线上的从设备进行通信。

### 1、API 列表

I2C 设备节点支持以下标准文件操作接口：

| **API**                                                  | **描述**                                                                |
| :------------------------------------------------------- | :---------------------------------------------------------------------- |
| `int open(FAR const char *path, int oflag, ...);`        | 打开 I2C 设备节点，例如 `"/dev/i2c-0"`。                                |
| `int  close(int `*`fd`*`);`                              | 关闭已打开的设备文件描述符。                                            |
| `int ioctl(int fd, int req, ...)`                        | **核心通信接口**。通过发送特定命令来执行 I2C 读写、总线复位等复杂操作。 |
| `ssize_t read(int fd, ...)` `ssize_t write(int fd, ...)` | **暂未使用**。                                                          |

### 2、`ioctl()` 核心接口

`ioctl()` 是与 I2C 设备进行数据交互的主要方式。openvela 定义了以下标准 `ioctl` 命令：

#### `I2CIOC_TRANSFER`

执行一次或多次 I2C 消息传输。这是最核心、最常用的命令。它使用 `struct i2c_transfer_s` 结构体来描述整个传输任务。

```C
/* 定义一个 I2C 传输任务，可包含一个或多个消息 */
struct i2c_transfer_s
{
  FAR struct i2c_msg_s *msgv; /* Array of I2C messages for the transfer */
  size_t msgc;                /* Number of messages in the array. */
};
```

每个 I2C 消息由 `struct i2c_msg_s` 定义，用于描述单次读或写操作：

```C
#define I2C_M_READ           0x0001 /* Read data, from slave to master */
#define I2C_M_NOSTOP         0x0040 /* Message should not end with a STOP */
#define I2C_M_NOSTART        0x0080 /* Message should not begin with a START */

struct i2c_msg_s
{
  uint32_t frequency;         /* I2C frequency */
  uint16_t addr;              /* Slave address (7- or 10-bit) */
  uint16_t flags;             /* See I2C_M_* definitions */
  FAR uint8_t *buffer;        /* Buffer to be transferred */
  ssize_t length;             /* Length of the buffer in bytes */
};
```

#### `CONFIG_I2C_RESET`

复位 I2C 总线。此命令在总线锁死或出现异常时非常有用。要使用此功能，必须在 Kconfig 中启用 `CONFIG_I2C_RESET`。调用时无需第三个参数。

### 3、复合传输示例：读取传感器寄存器

本节提供一个完整的示例，演示如何执行一次**复合传输 (Combined Transfer)** 来读取 I2C 设备的寄存器值。这是与 I2C 传感器等设备通信的典型场景，其过程分为两步：

1. **写操作**：向从设备发送要读取的**寄存器地址**。
2. **读操作**：紧接着从该寄存器**读取数据**。

#### 步骤一：Kconfig 配置

确保您的项目中已启用以下配置：

```Makefile
CONFIG_I2C=y
CONFIG_I2C_DRIVER=y
```

#### 步骤二：读写示例代码

以下代码从指定的 I2C 从机地址和寄存器地址读取一个字节的数据。

<details>
<summary>点击展开代码</summary>

```C
#include <stdio.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <nuttx/i2c/i2c_master.h>

// 含义：使用 /dev/i2c-8，访问从机地址 0x68，读取寄存器 0x00 的值
//./i2c_test.out /dev/i2c-8 0x68 0x60


int main(int argc, char **argv)
{
  int fd,ret;
  uint8_t val;
  char dev_name[20];
  unsigned int slave_address,reg_address;
  struct i2c_transfer_s work;

  snprintf(dev_name, sizeof(dev_name),"%s", argv[1]);

  /* 1. 打开 I2C 设备节点 */
  fd = open(dev_name, O_RDWR);
  if (fd < 0)
   {
     printf("open failed: %d\n", fd);
     return fd;
   }

  /* 2. 准备 I2C 消息 */
  work.msgc = 2;
  work.msgv = (struct i2c_msg_s *)malloc(work.msgc * sizeof(struct i2c_msg_s));
  if (NULL == work.msgv)
    {
      printf("Memory alloc error\n");
      close(fd);
      return -1;
    }

  sscanf(argv[2], "%x", &slave_address);
  sscanf(argv[3], "%x", &reg_address);

  val = reg_address;
  /* 消息 1: 写操作，发送要读取的寄存器地址 */
  (work.msgv[0]).frequency=400000;
  (work.msgv[0]).length = 1;
  (work.msgv[0]).addr = slave_address;
  (work.msgv[0]).buffer = &val;
  (work.msgv[0]).flags = I2C_M_NOSTOP;

  /* 消息 2: 读操作，从设备读取一个字节的数据 */
  (work.msgv[1]).frequency=400000;
  (work.msgv[1]).length = 1;
  (work.msgv[1]).flags = I2C_M_READ;
  (work.msgv[1]).addr = slave_address;
  (work.msgv[1]).buffer = &val;

  /* 3. 执行 ioctl 调用，发起传输 */
  ret = ioctl(fd, I2CIOC_TRANSFER, &work);
  if (ret < 0)
  {
     printf("i2c: ioctl(I2CIOC_TRANSFER) failed: %d\n",fd);
     free( work.msgv);
     close(fd);
     return -1;
  }

  printf("reg:0x%02X val:%02x\n", reg_address, val);
  free( work.msgv);
  close(fd);

  return 0;
}
```

</details>

## 四、验证与测试

- 请参考 [I2C 驱动的验证与调试](./i2c_verification_guide.md)来测试您的驱动。
