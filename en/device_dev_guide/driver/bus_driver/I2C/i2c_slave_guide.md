# Adapting an I2C Slave Driver

[ English | [简体中文](../../../../../zh-cn/device_dev_guide/driver/bus_driver/I2C/i2c_slave_guide.md) ]

This document describes how to configure a microcontroller's (MCU) I2C controller in slave mode. This allows the MCU to act as a peripheral on the I2C bus, responding to read and write requests from a master device.

## I. Core Differences Between Slave and Master Driver Architectures

The key to understanding a Slave driver lies in its **passive** and **event-driven** nature.

- **Master Driver**: An `ioctl` call from the application layer initiates the process. The driver **actively** generates START/STOP signals on the bus, controlling the entire transfer.
- **Slave Driver**: The driver **passively** listens to the bus. When an external Master sends an addressing signal that matches the slave's own address, the I2C hardware controller generates an interrupt. The driver's **Interrupt Service Routine (ISR)** becomes the entry point for logic, responsible for responding to the Master's subsequent operations (read or write).

Therefore, the development focus for a Slave driver is on: **writing an interrupt service routine and, within the interrupt, calling a callback function provided by the upper-layer application.**

## II. Adapting the Lower Half Interface

The core task of lower-half adaptation is to implement a standard set of I2C Slave operation interfaces and provide an initialization function for the upper layer to obtain an I2C Slave device handle.

### 1. Kconfig Configuration Options

```Makefile
CONFIG_I2C=y        # Enable the I2C framework
CONFIG_I2C_SLAVE=y  # Enable I2C Slave functionality
```

### 2. Core Data Structures and Interfaces

The core of lower-half adaptation is to implement a standard set of I2C Slave operation interfaces and provide an initialization function for upper-layer code to call. The adaptation work revolves around `struct i2c_slave_s`, `struct i2c_slaveops_s`, and an interrupt service routine.

<details>
<summary>Click to expand code</summary>

```C
/*
 * The set of I2C Slave operation functions.
 * These functions are called by the upper-half driver to configure and control the Slave device.
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
 * I2C Slave device handle.
 * This is the standard interface provided by the lower-half driver to the upper half.
 */
struct i2c_slave_s
{
  const struct i2c_slaveops_s *ops; /* Pointer to the specific implementation of I2C operation functions */
};
```

</details>

### 3. Adaptation Implementation Steps

- **Reference Implementations**：

    - [rp2040_i2c_slave.c](https://github.com/apache/nuttx/blob/master/arch/arm/src/rp2040/rp2040_i2c_slave.c)
    - [s32k1xx_bringup.c](https://github.com/apache/nuttx/blob/master/boards/arm/s32k1xx/rddrone-bms772/src/s32k1xx_bringup.c)

#### Step 1: Define the Private Device Structure

Similar to Master mode, define a private structure to manage the slave's state. Its first member must be `const struct i2c_slaveops_s *ops`.

<details>
<summary>Click to expand code</summary>

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

#### Step 2: Implement the `i2c_slaveops_s` Operation Function Set

You need to implement the functions in `i2c_slaveops_s` as described in the table below. These functions are called by the user of the I2C Slave handle.

| **Function**       | **Description**                                                                                                                                                                                                                                                                                             |
| :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `setownaddress`    | **Core initialization function**. Called by the upper layer to: 1. Set the I2C slave address for this device. 2. Initialize hardware resources like GPIOs and clocks. 3. Configure and enable I2C interrupts, ensuring that the appropriate event handling logic is triggered when an interrupt occurs.     |
| `write`            | **Send Data**. When a Master **reads** data from this device, this function is called to prepare and **send** data to the Master. `buffer` points to the data to be sent.                                                                                                                                   |
| `read`             | **Receive Data**. When a Master **writes** data to this device, this function is called to **receive** data from the Master and store it in the `buffer`.                                                                                                                                                   |
| `registercallback` | **Register Event Callback**. Registers a callback function. When an I2C slave event occurs (e.g., data received, read request received), this callback is invoked from the interrupt handler to notify the upper-layer application. The third argument can specify a memory area to save data from the bus. |

#### Step 3: Implement the Driver Entry Point `xxx_i2cbus_slave_initialize()`

This function is the entry point for the lower-half driver, responsible for creating and returning an I2C Slave handle.

<details>
<summary>Click to expand code</summary>

```C
/* arch/arm/src/s32k1xx/s32k1xx_lpi2c_slave.c */

struct i2c_slave_s *s32k1xx_i2cbus_slave_initialize(int port)
{
  struct s32k1xx_lpi2c_slave_priv_s *priv;
   /*************
  ......initialize priv
  priv.setownaddress(); // Initialize GPIO, clock, interrupt (ISR calls callback to process data)
  priv.registercallback(); // Register callback
  **************/
  return (struct i2c_slave_s *)priv;
}
```

</details>

| **Item**                   | **Description**                                                                                                                                                                                                                                                      |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Function Prototype**     | `xxx_i2cbus_slave_initialize`, where `xxx` is the chip name.                                                                                                                                                                                                         |
| **Parameters**             | The I2C Slave bus number. If the chip supports multiple I2C buses, multi-bus configuration should be implemented here as needed.                                                                                                                                     |
| **Return Value**           | A handle for I2C Slave bus operations.                                                                                                                                                                                                                               |
| **Implementation Details** | Calls the `setownaddress` instance to initialize the I2C Slave clock, GPIOs, and interrupts (the ISR must call the registered callback to process data). Calls the `registercallback` instance to register the callback. Returns the I2C Slave bus operation handle. |
| **File Location**          | In `xxx_i2c_slave.c` under the chip path, where `xxx` is the chip name.                                                                                                                                                                                              |
| **Call Location**          | Called from `xxx_bringup.c` under the board path, where `xxx` is the board name.                                                                                                                                                                                     |

#### Step 4: Implement the Interrupt Service Routine (ISR)

Interrupts are the core of I2C Slave mode. You must implement an ISR to handle various events initiated by the Master (address match, receive/transmit requests, etc.). In the interrupt handler, you will typically call the callback function registered via `registercallback` to pass events and data to the upper-level logic.

**Notes**:

    - **Interrupt Handling**: After instantiating the above structures, you also need to implement an interrupt handler for the Slave to process requests when a Master initiates a read/write. You can refer to the implementation in `arch/arm/src/s32k1xx/s32k1xx_lpi2c_slave.c` for this part.
    - An I2C Slave device does not need to be registered as a device node. The hidden meaning is that application code generally does not access the I2C Slave directly.
    - **Asynchronous (Default)**: I2C Slave operations are inherently event-driven and asynchronous. The ISR notifies the upper layer via a callback without blocking the current task.
    - **Synchronous**: If you need to implement synchronous operations (e.g., the `read` function must wait for data to be fully received before returning), you can add a semaphore (`sem_t`) to your driver's private structure.

        - Initialize the semaphore in `setownaddress`.
        - Wait for the semaphore at the end of operations like `read`/`write` (`nxsem_wait_uninterruptible`).
        - Post (release) the semaphore in the ISR after the specific event is handled (`nxsem_post`).

## III. Northbound Application Layer Usage

Through a generic upper-half driver (`nuttx/drivers/i2c/i2c_slave_driver.c`), the adapted lower-half I2C Slave driver can be registered as a standard character device (e.g., `/dev/i2c-slave-0`). This allows user-space applications to simulate an I2C slave device using standard file interfaces like `open/read/write/poll`.

- Example 1: [rp2040_i2c_slave.c](https://github.com/apache/nuttx/blob/master/arch/arm/src/rp2040/rp2040_i2c_slave.c)
- Example 2: [s32k1xx_lpi2c_slave.c](https://github.com/apache/nuttx/blob/master/arch/arm/src/s32k1xx/s32k1xx_lpi2c_slave.c)

## IV. Verification and Testing

After completing the Slave driver adaptation and application layer code, you will need an external I2C Master device (e.g., another development board, a USB-to-I2C adapter) to communicate with your device to verify that the Slave functionality is working correctly.

Next, please refer to [I2C Driver Verification and Debugging](./i2c_verification_guide.md) to test whether your Slave driver functions as expected.
