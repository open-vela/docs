# 适配 I2C Slave 驱动

[ [English](../../../../../en/device_dev_guide/driver/bus_driver/I2C/i2c_slave_guide.md) | 简体中文 ]

本文介绍如何将微控制器（MCU）的 I2C 控制器配置为从机（Slave）模式。这使得 MCU 可以在 I2C 总线上扮演一个外设的角色，响应来自主设备（Master）的读写请求。

## 一、Slave 驱动架构与 Master 的核心区别

理解 Slave 驱动的关键在于其**被动**和**事件驱动**的特性。

- **Master** **驱动**：由应用层发起 `ioctl` 调用，驱动**主动**在总线上产生 START/STOP 信号，控制整个传输过程。
- **Slave** **驱动**：驱动**被动**地监听总线。当外部 Master 发送与自身地址匹配的寻址信号时，I2C 硬件控制器产生中断。驱动的**中断服务程序 (****ISR****)** 成为逻辑的入口，负责响应 Master 的后续操作（读或写）。

因此，Slave 驱动的开发重心在于：**编写中断服务程序，并在中断中调用由****上层****应用提供的回调函数**。

## 二、适配南向接口 (Lower Half)

南向适配的核心任务是实现一套标准的 I2C Slave 操作接口，并提供一个初始化函数，供上层代码获取 I2C Slave 的设备句柄。

### 1、Kconfig 配置项

```Makefile
CONFIG_I2C=y        # 启用 I2C 框架
CONFIG_I2C_SLAVE=y  # 启用 I2C Slave 功能
```

### 2、核心数据结构与接口

南向适配的核心是实现一套标准的 I2C Slave 操作接口，并提供一个初始化函数供上层代码调用。适配工作围绕 `struct i2c_slave_s`、`struct i2c_slaveops_s` 以及一个中断服务程序展开。

<details>
<summary>点击展开代码</summary>

```C
/*
 * I2C Slave 操作函数集。
 * 这些函数由上层驱动调用，用于配置和控制 Slave 设备。
 */
struct i2c_slaveops_s
{
  int (*setownaddress)(FAR struct i2c_slave_s *dev, int addr, int nbits);
  int (*write)(FAR struct i2c_slave_s *dev, FAR const uint8_t *buffer,
        int buflen);
  int (*read)(FAR struct i2c_slave_s *dev, FAR uint8_t *buffer,
        int buflen);
  int (*registercallback)(FAR struct i2c_slave_s *dev,
        int (*callback)(FAR void *arg), FAR void *arg);
};

/*
 * I2C Slave 设备句柄。
 * 这是南向驱动向上层提供的标准接口。
 */
struct i2c_slave_s
{
  const struct i2c_slaveops_s *ops; /* 指向具体实现的 I2C 操作函数集 */
};
```

</details>

### 3、适配实现步骤

- **参考实现**：

    - [rp2040_i2c_slave.c](https://github.com/apache/nuttx/blob/master/arch/arm/src/rp2040/rp2040_i2c_slave.c)
    - [s32k1xx_bringup.c](https://github.com/apache/nuttx/blob/master/boards/arm/s32k1xx/rddrone-bms772/src/s32k1xx_bringup.c)

#### 步骤一：定义私有设备结构体

与 Master 模式类似，定义一个私有结构体来管理从机状态。其第一个成员必须是 `const struct i2c_slaveops_s *ops`。

<details>
<summary>点击展开代码</summary>

```C
arch/arm/src/s32k1xx/s32k1xx_lpi2c_slave.c:
/* I2C slave device private data */

struct s32k1xx_lpi2c_slave_priv_s
{
  const struct i2c_slaveops_s *ops;                  /* I2C slave operations */
  const struct s32k1xx_lpi2c_slave_config_s *config; /* LPI2C slave configuration */

  int slave_addr; /* I2C address of the slave */
  int addr_nbits; /* 7- or 10-bit addressing */

  uint8_t *read_buffer; /* Read buffer (master wants to write, slave will read data) */
  int read_buflen;      /* Read buffer size */
  int read_bufindex;    /* Read buffer index */

  const uint8_t *write_buffer; /* Write buffer (master wants to read, slave will write data) */
  int write_buflen;            /* Write buffer size */
  int write_bufindex;          /* Write buffer index */

  int (*callback)(FAR void *arg); /* Callback function when data has been received */
  void *callback_arg;             /* Argument of callback function */

  int refs; /* Reference count */
};
```

</details>

#### 步骤二：实现 `i2c_slaveops_s` 操作函数集

根据下表描述，您需要实现 `i2c_slaveops_s` 中的各个函数。这些函数由 I2C Slave 句柄的使用者调用。

| **函数**           | **描述**                                                                                                                                                                               |
| :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `setownaddress`    | **核心初始化函数**。由上层调用，用于： 1. 设置本设备的 I2C 从机地址。 2. 初始化 GPIO、时钟等硬件资源。 3. 配置并使能 I2C 中断，当中断发生时，应能触发相应的事件处理逻辑。              |
| `write`            | **发送数据**。当 Master 从本设备**读取**数据时，此函数被调用，用于准备并向 Master **发送**数据。`buffer` 指向要发送的数据。                                                            |
| `read`             | **接收数据**。当 Master 向本设备**写入**数据时，此函数被调用，用于从 Master **接收**数据并存入 `buffer`。                                                                              |
| `registercallback` | **注册事件回调**。注册一个回调函数，当 I2C 从机事件（如收到数据、收到读请求等）发生时，在中断处理函数中调用此回调，通知上层应用。第三参数可以指定一块内存，把 bus 总线的数据保存下来。 |

#### 步骤三：实现驱动入口函数 `xxx_i2cbus_slave_initialize()`

此函数是南向驱动的入口，负责创建并返回一个 I2C Slave 句柄。

<details>
<summary>点击展开代码</summary>

```C
arch/arm/src/s32k1xx/s32k1xx_lpi2c_slave.c:

struct i2c_slave_s *s32k1xx_i2cbus_slave_initialize(int port)
{
  struct s32k1xx_lpi2c_slave_priv_s *priv;
   /*************
  ......initialize priv
  priv.setownaddress();//初始化GPIO、时钟、中断(中断服务函数调用callbak处理数据)
  priv.registercallback();//注册callback
  **************/
  return (struct i2c_slave_s *)priv;
  
}
```

</details>

| **项目**         | **描述**                                                                                                                                                                                               |
| :--------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **函数原型**     | `xxx_i2cbus_slave_initialize`，其中 `xxx` 为 `chip` 名称。                                                                                                                                             |
| **参数**         | I2C Slave bus 号，芯片支持多路 I2C 时，这里要实现多路配置，也可以按需配置。                                                                                                                            |
| **返回值**       | I2C Slave bus 操作的句柄。                                                                                                                                                                             |
| **函数实现**     | 调用 `setownaddress` 实例进行 I2C Slave 时钟、GPIO 口初始化、中断的初始化(中断服务函数要调用注册的回调函数，进行数据的处理)。调用 `registercallback` 实例进行回调注册。返回 I2C Slave bus 操作的句柄。 |
| **函数实现位置** | chip 路径下的 `xxx_i2c_slave.c`，其中 `xxx` 为 chip 名称。                                                                                                                                             |
| **函数调用位置** | board 路径下的 `xxx_bringup.c` 里面调用，`xxx` 为 board 名称。                                                                                                                                         |

#### 步骤四：实现中断服务程序 (ISR)

中断是 I2C Slave 模式的核心。您必须实现一个中断服务程序，用于处理 Master 发起的各种事件（地址匹配、接收/发送请求等）。在中断处理函数中，通常会调用通过 `registercallback` 注册的回调函数，将事件和数据传递给上层逻辑。

**注意**：

- 中断处理：实例化上述结构体后，还需要实现一个中断处理函数，用于 Master 向 Slave 发起读/写时 Slave 处理请求用。这一块可以参考 `arch/arm/src/s32k1xx/s32k1xx_lpi2c_slave.c` 内的实现。
- I2C Slave 设备不需要注册为设备节点。其隐藏的含义是应用代码一般不直接访问 I2C Slave。
- **异步 (默认)**：I2C Slave 的操作天然是事件驱动和异步的。ISR 通过回调函数通知上层，不阻塞当前任务。
- **同步**：如果需要实现同步操作（例如，`read` 函数需要等待数据完全接收后再返回），您可以在驱动的私有结构体中增加信号量 (`sem_t`)。

    - 在 `setownaddress` 中初始化信号量。
    - 在 `read`/`write` 等操作的末尾等待信号量 (`nxsem_wait_uninterruptible`)。
    - 在中断服务程序 (ISR) 中处理完特定事件后，释放信号量 (`nxsem_post`)。

## 三、北向应用层使用

通过一个通用的上层驱动 (`nuttx/drivers/i2c/i2c_slave_driver.c`)，可以将南向适配的 I2C Slave 驱动注册为标准的字符设备（例如 `/dev/i2c-slave-0`），允许用户空间应用程序通过 `open/read/write/poll` 等标准文件接口来模拟一个 I2C 从设备。

- 示例 1：[rp2040_i2c_slave.c](https://github.com/apache/nuttx/blob/master/arch/arm/src/rp2040/rp2040_i2c_slave.c)
- 示例 2：[s32k1xx_lpi2c_slave.c](https://github.com/apache/nuttx/blob/master/arch/arm/src/s32k1xx/s32k1xx_lpi2c_slave.c)

## 四、验证与测试

完成 Slave 驱动适配和应用层代码编写后，您需要一个外部的 I2C Master 设备（例如，另一块开发板、一个 USB-to-I2C 适配器等）来与您的设备通信，以验证 Slave 功能是否正常。

下一步，请参考[I2C 驱动的验证与调试](./i2c_verification_guide.md)来测试您的 Slave 驱动功能是否符合预期。
