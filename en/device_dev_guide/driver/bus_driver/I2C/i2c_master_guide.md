# Adapting an I2C Master Driver

[ English | [简体中文](../../../../../zh-cn/device_dev_guide/driver/bus_driver/I2C/i2c_master_guide.md) ]

This document describes how to adapt a standard I2C Master driver for openvela, enabling it to function as a bus master.

## I. Driver Framework Layers

The development of an I2C Master driver involves the driver layer, board layer, and application layer. Their collaborative relationship is as follows:

### Driver Layer

Responsible for implementing chip-specific low-level I2C hardware operations. This layer needs to encapsulate hardware details and provide a standardized `i2c_master_s` handle to the upper layer.

```C
/* 1. Define the set of low-level operation functions */
static const struct i2c_ops_s bl602_i2c_ops =
{
  .transfer = bl602_i2c_transfer,
#ifdef CONFIG_I2C_RESET
  .reset = bl602_i2c_reset
#endif
};

/* 2. Define a private data structure containing the operation set and configuration information */
static struct bl602_i2c_priv_s bl602_i2c0_priv =
{
  .ops      = &bl602_i2c_ops,
  .config   = &bl602_i2c0_config,
};

/* 3. Implement the initialization function to return a standard I2C Master handle */
struct i2c_master_s *bl602_i2cbus_initialize(int port)
{
  priv = (struct bl602_i2c_priv_s *)&bl602_i2c0_priv;
  
  return (struct i2c_master_s *)priv;
}
```

### Board Layer

During the system startup phase, it calls the driver layer's initialization function to obtain the I2C bus handle. Depending on requirements, this bus can be optionally registered as a character device (e.g., `/dev/i2c-0`) or passed directly to other kernel drivers (such as sensor drivers) for use.

```C
/* Get the I2C bus handle */
i2c_bus = bl602_i2cbus_initialize(0);

/* Register the bus as /dev/i2c0 */
i2c_register(i2c_bus, 0);
```

### Application Layer

 Accesses registered `/dev/i2c-N` device nodes through standard POSIX file interfaces (e.g., `open`, `ioctl`) to communicate with I2C slave devices connected to the bus.

```C
fd = open("/dev/i2c", O_RDWR);
ioctl(fd, );
...
```

## II. Adapting the Lower Half Interface

The core task of adapting the lower-half interface is to implement the chip's low-level driver and provide a standard initialization function `xxx_i2cbus_initialize()`, where `xxx` represents the chip name.

### 1. Kconfig Configuration Options

Please enable the following configuration options in Kconfig to support the I2C Master driver:

```Makefile
CONFIG_I2C=y          # Required, enables the I2C subsystem
CONFIG_I2C_DRIVER=y   # Required, enables the I2C character device driver upper half
CONFIG_I2C_RESET=y    # Optional, if bus reset functionality is needed
```

### 2. Core Data Structures

The openvela I2C Master driver is abstracted around two core structures: `struct i2c_master_s` and `struct i2c_ops_s`.

```C
/*
 * The set of I2C Master operation functions.
 * Driver developers need to implement the function pointers within it, especially the transfer function.
 */
struct i2c_ops_s
{
  /* Core transfer function, required */
  CODE int (*transfer)(FAR struct i2c_master_s *dev,
                       FAR struct i2c_msg_s *msgs, int count);
#ifdef CONFIG_I2C_RESET
  /* Optional bus reset function */
  CODE int (*reset)(FAR struct i2c_master_s *dev);
#endif
};

/*
 * I2C Master device handle.
 * This is the standard interface provided by the lower-half driver to the upper half.
 * Developers typically define a private device structure that includes this structure.
 */
struct i2c_master_s
{
  FAR const struct i2c_ops_s *ops; /* Pointer to the set of operation functions */
};
```

### 3. Driver Entry Point Function Description

You need to implement the `xxx_i2cbus_initialize()` function in the chip driver file (`xxx_i2c.c`) according to the requirements in the table below.

| **Item**                   | **Description**                                                                                                                                                                                                                                                                                                 |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Function Prototype**     | `struct i2c_master_s *xxx_i2cbus_initialize(int port)`                                                                                                                                                                                                                                                          |
| **Parameters**             | `port`: The I2C bus port number. If the chip supports multiple I2C buses, you need to configure them based on this parameter.                                                                                                                                                                                   |
| **Return Value**           | Returns a standard `i2c_master_s` operation handle. Returns `NULL` if initialization fails.                                                                                                                                                                                                                     |
| **Implementation Details** | Initializes the clocks and GPIOs required for the I2C controller. If using interrupt mode, it also needs to configure and enable the interrupt. Fills and returns an `i2c_master_s` handle containing a pointer to the `transfer` function, which is used to handle data transfer requests from the upper half. |
| **File Location**          | Located in `xxx_i2c.c` under the chip path, where `xxx` is the chip name.                                                                                                                                                                                                                                       |
| **Call Location**          | Called from `xxx_bringup.c` under the board path, where `xxx` is the board name.                                                                                                                                                                                                                                |

### 4. Adaptation Implementation Steps

This section provides code examples to demonstrate how to complete the I2C Master driver adaptation step by step.

- **Reference Implementation**：[bl602_i2c.c](https://github.com/apache/nuttx/blob/master/arch/risc-v/src/bl602/bl602_i2c.c)

#### Step 1: Define the Private Device Structure

We highly recommend defining a private structure to encapsulate all state information of the I2C controller, such as configuration, locks, semaphores, and runtime data. The following is an example of the private structure for the `bl602` chip:

> **Key Point: Structure Member Layout** To ensure type-safe casting, the **first member** of the private structure must be `const struct i2c_ops_s *ops;`. This allows the framework to safely cast a pointer to your private structure to a standard `struct i2c_master_s *` handle.

<details>
<summary>Click to expand code</summary>

```C
/* Located at: arch/risc-v/src/bl602/bl602_i2c.c */

/* Private data structure for the bl602 I2C driver */
struct bl602_i2c_priv_s
{
  /* Must be the first member to be compatible with i2c_master_s type casting */
  const struct i2c_ops_s *ops; /* Standard I2C operations */

  /* Port configuration */
  const struct bl602_i2c_config_s *config;

  /* Status and synchronization mechanisms */
  uint8_t  subflag;   /* Sub address flag */
  uint32_t subaddr;   /* Sub address */
  uint8_t  sublen;    /* Sub address length */
  mutex_t  lock;      /* Mutual exclusion mutex */
  sem_t    sem_isr;   /* Interrupt wait semaphore */

  /* Runtime data */
  /* I2C work state */
  uint8_t i2cstate;

  struct i2c_msg_s *msgv; /* Message list */

  uint8_t msgid; /* Current message ID */
  ssize_t bytes; /* Processed data bytes */
  int     refs;  /* Reference count */
};
```

</details>

#### Step 2: Implement the Initialization Function `xxx_i2cbus_initialize()`

This function is responsible for performing hardware initialization and returning a configured I2C Master handle.

<details>
<summary>Click to expand code</summary>

```C
struct i2c_master_s *bl602_i2cbus_initialize(int port)
{
  struct bl602_i2c_priv_s         *priv;
  const struct bl602_i2c_config_s *config;

  /* 1. Get the corresponding private device instance based on the port number */
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
This section configures I2C for interrupt mode. If interrupts are not used, this part can be replaced with I2C GPIO and clock initialization.
  
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

   /* 2. Return the private structure pointer, casting it to the standard handle type */
  return (struct i2c_master_s *)priv;
}
```

</details>

#### Step 3: Call from Board-Level Code

In the board-level initialization code (`xxx_bringup.c`), call the initialization function provided by the chip driver and, if necessary, register the I2C bus as a system device.

- **Reference Implementation**：[bl602_bringup.c](https://github.com/apache/nuttx/blob/master/boards/risc-v/bl602/bl602evb/src/bl602_bringup.c)

<details>
<summary>Click to expand code</summary>

```C
#ifdef CONFIG_I2C
  /* Initialize I2C bus 0 */
  i2c_bus = bl602_i2cbus_initialize(0);
  
  /* 2. (Optional) Register the bus as the /dev/i2c-0 device node */
  i2c_register(i2c_bus, 0);
#endif
```

</details>

**`i2c_register()`** **Usage Notes**

- **Registering as a Device Node**: Calling `i2c_register(i2c_bus, N)` creates a character device node `/dev/i2c-N`. This allows user-space applications (such as test programs or `i2ctool`) to access the I2C bus through standard file interfaces.
- **For Kernel Use Only**: If an I2C bus is used exclusively by other drivers within the kernel (e.g., an onboard sensor), you can choose not to call `i2c_register()`. Instead, pass the `i2c_bus` handle directly to the registration function of the corresponding driver.

## III. Northbound Usage

Once the I2C Master driver is successfully registered, the system creates device nodes in the format `/dev/i2c-N` (e.g., `/dev/i2c-0`, `/dev/i2c-1`). Applications can use these device nodes to communicate with slave devices on the I2C bus using standard POSIX file interfaces.

### 1. API List

The I2C device node supports the following standard file operation interfaces:

| **API**                                                  | **Description**                                                                                                                  |
| :------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| `int open(FAR const char *path, int oflag, ...);`        | Opens an I2C device node, such as `"/dev/i2c-0"`.                                                                                |
| `int close(int fd);`                                     | Closes the opened device file descriptor.                                                                                        |
| `int ioctl(int fd, int req, ...)`                        | **Core communication interface**. Executes complex operations like I2C reads/writes and bus resets by sending specific commands. |
| `ssize_t read(int fd, ...)` `ssize_t write(int fd, ...)` | **Not currently used**.                                                                                                          |

### 2. `ioctl()` Core Interface

`ioctl()` is the primary method for data interaction with I2C devices. openvela defines the following standard `ioctl` commands:

#### `I2CIOC_TRANSFER`

Executes one or more I2C message transfers. This is the most essential and commonly used command. It uses the `struct i2c_transfer_s` structure to describe the entire transfer task.

```C
/* Defines an I2C transfer task, which can contain one or more messages */
struct i2c_transfer_s
{
  FAR struct i2c_msg_s *msgv; /* Array of I2C messages for the transfer */
  size_t msgc;                /* Number of messages in the array. */
};
```

Each I2C message is defined by `struct i2c_msg_s` and describes a single read or write operation:

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

Resets the I2C bus. This command is very useful when the bus is locked or encounters an error. To use this feature, `CONFIG_I2C_RESET` must be enabled in Kconfig. No third argument is needed for the call.

### 3. Combined Transfer Example: Reading a Sensor Register

This section provides a complete example of how to perform a **Combined Transfer** to read a register value from an I2C device. This is a typical scenario for communicating with devices like I2C sensors and involves two steps:

1. **Write Operation**: Send the **register address** to be read to the slave device.
2. **Read Operation**: Immediately follow by **reading data** from that register.

#### Step 1: Kconfig Configuration

Ensure that the following configurations are enabled in your project:

```Makefile
CONFIG_I2C=y
CONFIG_I2C_DRIVER=y
```

#### Step 2: Read/Write Example Code

The following code reads one byte of data from a specified I2C slave address and register address.

<details>
<summary>Click to expand code</summary>

```C
#include <stdio.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <nuttx/i2c/i2c_master.h>

// Meaning: Use /dev/i2c-8, access slave address 0x68, read the value from register 0x60
// ./i2c_test.out /dev/i2c-8 0x68 0x60


int main(int argc, char **argv)
{
  int fd,ret;
  uint8_t val;
  char dev_name[20];
  unsigned int slave_address,reg_address;
  struct i2c_transfer_s work;

  snprintf(dev_name, sizeof(dev_name),"%s", argv[1]);

  /* 1. Open the I2C device node */
  fd = open(dev_name, O_RDWR);
  if (fd < 0)
   {
     printf("open failed: %d\n", fd);
     return fd;
   }

  /* 2. Prepare the I2C messages */
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
  /* Message 1: Write operation, sending the register address to be read */
  (work.msgv[0]).frequency=400000;
  (work.msgv[0]).length = 1;
  (work.msgv[0]).addr = slave_address;
  (work.msgv[0]).buffer = &val;
  (work.msgv[0]).flags = I2C_M_NOSTOP;

  /* Message 2: Read operation, reading one byte of data from the slave device */
  (work.msgv[1]).frequency=400000;
  (work.msgv[1]).length = 1;
  (work.msgv[1]).flags = I2C_M_READ;
  (work.msgv[1]).addr = slave_address;
  (work.msgv[1]).buffer = &val;

  /* 3. Execute the ioctl call to initiate the transfer */
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

## IV. Verification and Testing

- Please refer to [I2C Driver Verification and Debugging](./i2c_verification_guide.md) to test your driver.
