# How to Add a Bluetooth Driver

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/connection/bluetooth/how_to_add_a_bluetooth_driver.md) \]

## I. Implementing the Driver

### Overview

Developers or chip vendors can implement a variable of type `struct bt_driver_s` and initialize the following member functions：

- `CODE int (*open)(FAR struct bt_driver_s *btdev)`
- `CODE int (*send)(FAR struct bt_driver_s *btdev, enum bt_buf_type_e type, FAR void *data, size_t len)`
- `CODE int (*ioctl)(FAR struct bt_driver_s *btdev, int cmd, unsigned long arg)`
- `CODE void (*close)(FAR struct bt_driver_s *btdev)`

The implementation of these member functions depends on the actual operation of the `HCI (Host Controller Interface)`, that is, the physical bus between the Host and the Controller.

### Example

#### Note

- To quickly validate custom callbacks and driver registration in a QEMU environment, this example implements the `struct bt_driver_s` member functions directly within the [drivers_initialize](../../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/drivers_initialize.c) function and completes driver registration.  
- In a real integration or production scenario, it is recommended to create a separate source file under the [vendor](../../../../../../../vendor_template/blob/dev-ai-contest-2026/boards/chip_name/board_name/src) directory for maintainability and version control.

#### Steps

1. In [drivers_initialize.c](../../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/drivers_initialize.c), add the [bt_driver.h](../../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/wireless/bluetooth/bt_driver.h) header include:

    ```C
    #include <nuttx/wireless/bluetooth/bt_driver.h> /* Add bt_driver.h header include */
    ```

2. In [drivers_initialize.c](../../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/drivers_initialize.c), implement the member functions.

    In openvela, the `receive` member function of `struct bt_driver_s` already has a default implementation in [uart_bth4.c](../../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/serial/uart_bth4.c). Therefore, developers or vendors do not need to redefine or implement this method.

    ```C
    /* The following are sample implementations for demonstration only.
     * In a real project, you can add actual business logic in these functions.
     */

    /* 1. Open HCI transport */
    static int sample_open(struct bt_driver_s *btdev)
    {
      printf("sample_open called.\n");
      /* You can perform initialization here */
      return 0;
    }

    /* 2. Send data to HCI */
    static int sample_send(struct bt_driver_s *btdev,
                           enum bt_buf_type_e type,
                           void *data, size_t len)
    {
      printf("sample_send called. type=%d, data=%p, len=%zu\n",
             type, data, len);
      /* Implement the logic to send data to the lower layer here */
      return 0;
    }

    /* 3. Close HCI transport */
    static void sample_close(struct bt_driver_s *btdev)
    {
      printf("sample_close called.\n");
      /* Perform resource release or other cleanup here */
    }

    /* 4. The receive member function is assigned by openvela at registration time */
    ```

3. In [drivers_initialize.c](../../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/drivers_initialize.c), define the `struct bt_driver_s` structure.

    The following code shows a complete example of initializing a `struct bt_driver_s` instance, where the function pointers are assigned to the sample functions defined above:

    ```C
    /* Initialize a bt_driver_s instance and assign the function pointers to the sample functions */
    struct bt_driver_s sample_driver =
    {
        .head_reserve = 1,   /* Set header reserve size, default is 1 */
        .open         = sample_open,     /* Points to sample_open */
        .send         = sample_send,     /* Points to sample_send */
        .close        = sample_close,    /* Points to sample_close */
        /* Note: Vendors and developers should not assign the '.receive' member themselves */
    };
    ```

## II. Registering the Driver

### Overview

After implementing the above structure, register the driver instance using one of the following APIs:

- `bt_driver_register()`: Registers with default id value 0.

- `bt_driver_register_with_id(FAR struct bt_driver_s *driver, int id)`: Registers with the specified id

The type definition `int bt_driver_register(FAR struct bt_driver_s *drv)` can be found in the header [bt_driver.h](../../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/wireless/bluetooth/bt_driver.h). Vendors or developers do not need to define the `receive()` member function; the BTH4 driver will initialize it.

The call flow is shown below:

![img](img/bt_driver.png)

### Example

After completing the driver implementation example above, call the driver registration API at the end of the `drivers_initialize()` function in [drivers_initialize.c](../../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/drivers_initialize.c) to complete the driver registration:

```C
void drivers_initialize(void)
{
  drivers_trace_begin();

  /* Register devices */
  syslog_initialize();

  /* Keep all existing code unchanged */

  /* By default, bt_driver_register(&sample_driver) registers the /dev/ttyHCI0 device node */
  /* Since /dev/ttyHCI0 is already registered by openvela QEMU, we use the following API to register another node */

  /* Use bt_driver_register_with_id(&sample_driver, 2) to register /dev/ttyHCI2 */
  bt_driver_register_with_id(&sample_driver, 2);

  drivers_trace_end();
}
```

### Validation

1. After writing the registration code, build the firmware:

    ```Bash
    ./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap -j8
    ```

2. After the build completes, run the emulator:

    ```Bash
    ./emulator.sh vela -no-window -qemu
    ```

3. Verify that the sample driver has been registered in openvela by listing `/dev`:

    ```Bash
    openvela-ap> ls /dev
    /dev:
    audio/
    binder
    charge/
    console
    fb0
    goldfish_pipe
    input0
    kbd0
    log
    null
    ptmx
    ram0
    random
    rtc0
    telnet
    ttyGNSS0
    ttyHCI2    /* You can see that the ttyHCI2 device node was successfully registered */
    ttyS1
    ttyV0
    uorb/
    urandom
    usensor
    virtblk0
    virtblk1
    zero
    ```

4. Validate the driver callbacks by writing to the device:

    **Note**: The `file_operations.write` function for the registered device node checks that data conforms to the BTH4 format. If validation succeeds, it calls the implemented `sample_send` function.

    ```Bash
    openvela-ap> echo "Hello openvelabluetooth" > /dev/ttyHCI2
    /* The echo command sends data to the node’s write callback */

    sample_open called.  /* The terminal prints the open callback log */
    sample_close called. /* The terminal prints the close callback log */
    ```
