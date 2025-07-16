# RPMsg Clock Development Guide

\[ English | [简体中文](../../../../../zh-cn/device_dev_guide/kernel/inter_processor_communication/RPMsg/RPMsg_Clock.md) \]

## I. Overview

RPMsg Clock (Remote Processor Messaging Clock) is a cross-core clock service built based on the RPMsg framework (Remote Processor Messaging Framework), used to implement cross-core clock control.

## II. Configuration

When using RPMsg Clock, ensure the following configurations are enabled:

```Makefile
# The following configurations need to be enabled for both server and client sides
CONFIG_CLK_RPMSG=y
```

- Server side: The core containing the actual clock system, responsible for providing clock resources.
- Client side: The core without an actual clock system, which needs to access or control the clock resources of the server side.

## III. Usage

### 1. Register Clock Resources

The prerequisite for the client side to access or control the server side's clock resources is that the server side has completed the initialization of the actual clock subsystem, that is, the clock resources are registered by calling `clk_register`. The client side does not need to register the clock.

For example code about clock registration, please refer to the following link: [nuttx/drivers/clk/song](https://github.com/FishsemiCode/nuttx/tree/song-u1/drivers/clk/song)

### 2. Obtain a Clock Instance

When accessing or controlling clock resources, a clock instance needs to be obtained through the name of the clock resource.

The following is the function definition for obtaining a clock instance:

```C
/* name is the name of the clk source to be controlled */
FAR struct clk_s *clk_get(FAR const char *name);
```

#### Parameter Description

- Server side:
    - The parameter of the `clk_get` function is the clock resource name passed in when calling `clk_register`.

- Client side:

    - The parameter of the `clk_get` function needs to include the CPU name (`cpuname`) of the server side and the clock resource name.
    - For example: Suppose the CPU name of the server side is `"ap"`, and the clock resource name to be accessed is `"spi_clk"`, then when the client side calls the `clk_get` function, the parameter passed in should be `"ap/spi_clk"`.

## IV. Working Principle

### 1. RPMsg Message Processing Mechanism

In the clk driver, the clock source is registered with the clock subsystem through `clk_register`. When a clock source needs to be accessed or controlled, an instance of the clock source can be obtained through `clk_get`, and then the clock source can be operated through the `clk->ops` structure associated with the instance.

In RPMsg Clk, `clk->ops` is abstracted into the following operation interfaces:

```C
const struct clk_ops_s g_clk_rpmsg_ops =
{
  .enable = clk_rpmsg_enable,
  .disable = clk_rpmsg_disable,
  .is_enabled = clk_rpmsg_is_enabled,
  .recalc_rate = clk_rpmsg_recalc_rate,
  .round_rate = clk_rpmsg_round_rate,
  .set_rate = clk_rpmsg_set_rate,
  .set_phase = clk_rpmsg_set_phase,
  .get_phase = clk_rpmsg_get_phase,
};
```

Operation process:

- Client-side request forwarding:

    The function implementation in `g_clk_rpmsg_ops` forwards the request to the server side. The forwarding target is determined by the `cpuname` string in the clock source name.

- Server-side request processing:

    The server side completes the actual function call and returns the result to the client side.

### 2. Clock Enable Process

For example, the `clk_rpmsg_enable` function sends a `CLK_RPMSG_ENABLE` request to the server side. The following is the implementation of the `clk_rpmsg_enable` function, which is responsible for forwarding the request to enable the clock from the client side to the server side:

```C
static int clk_rpmsg_enable(FAR struct clk_s *clk)
{
  FAR struct rpmsg_endpoint *ept;
  FAR struct clk_rpmsg_enable_s *msg;
  FAR const char *name = clk->name;
  uint32_t size;
  uint32_t len;

  ept = clk_rpmsg_get_ept(&name);
  if (!ept)
    {
      return -ENODEV;
    }

  len = sizeof(*msg) + strlen(name) + 1;

  msg = rpmsg_get_tx_payload_buffer(ept, &size, true);
  if (!msg)
    {
      return -ENOMEM;
    }

  DEBUGASSERT(len <= size);

  strlcpy(msg->name, name, size - sizeof(*msg));

  return clk_rpmsg_sendrecv(ept, CLK_RPMSG_ENABLE,
                           (struct clk_rpmsg_header_s *)msg,
                            len);
}
```

#### Description of Processing Logic

1. Obtain communication endpoint:
    - The function obtains the communication endpoint with the target server side through `clk_rpmsg_get_ept`. If the communication endpoint does not exist, it returns the error code `-ENODEV`.

2. Construct the message:
    - The function allocates a message buffer through `rpmsg_get_tx_payload_buffer` and copies the clock name into the message.

3. Send the request and receive the response:
    - The function calls `clk_rpmsg_sendrecv` to send the `CLK_RPMSG_ENABLE` request to the server side and waits for the response.

### 3. Request Processing on the Server Side

When the server side receives a `CLK_RPMSG_ENABLE` request, it calls the corresponding processing function `clk_rpmsg_enable_handler`.

The following is the registry of message processing functions:

```C
static const rpmsg_ept_cb g_clk_rpmsg_handler[] =
{
  [CLK_RPMSG_ENABLE]    = clk_rpmsg_enable_handler,
  [CLK_RPMSG_DISABLE]   = clk_rpmsg_disable_handler,
  [CLK_RPMSG_SETRATE]   = clk_rpmsg_setrate_handler,
  [CLK_RPMSG_SETPHASE]  = clk_rpmsg_setphase_handler,
  [CLK_RPMSG_GETPHASE]  = clk_rpmsg_getphase_handler,
  [CLK_RPMSG_GETRATE]   = clk_rpmsg_getrate_handler,
  [CLK_RPMSG_ROUNDRATE] = clk_rpmsg_roundrate_handler,
  [CLK_RPMSG_ISENABLED] = clk_rpmsg_isenabled_handler,
};
```

The following is the specific implementation of `clk_rpmsg_enable_handler`, which is responsible for calling the actual clock enabling function:

```C
static int clk_rpmsg_enable_handler(FAR struct rpmsg_endpoint *ept,
                                    FAR void *data, size_t len,
                                    uint32_t src, FAR void *priv)
{
  FAR struct clk_rpmsg_enable_s *msg = data;
  FAR struct clk_rpmsg_s *clkrp = clk_rpmsg_get_clk(ept, msg->name);

  if (clkrp)
    {
      msg->header.result = clk_enable(clkrp->clk);
      if (!msg->header.result)
        {
          clkrp->count++;
        }
    }
  else
    {
      msg->header.result = -ENOENT;
    }

  return rpmsg_send(ept, msg, sizeof(*msg));
}
```

#### Description of Processing Logic

1. Obtain the clock instance:
    - The function obtains the clock instance with the specified name through `clk_rpmsg_get_clk`.
    - If the clock instance exists, call the `clk_enable` function to enable the clock.
    - If the clock instance does not exist, return the error code `-ENOENT`.

2. Update the counter:
    - If the clock is enabled successfully (`clk_enable` returns 0), increment the clock's reference count `clkrp->count`.

3. Return the result:
    - Return the operation result to the client side through `rpmsg_send`.

## V. Related Documents

- For the design of the clock driver, please refer to [Clock](../../../../../en/device_dev_guide/power_mgt/Clock.md).
