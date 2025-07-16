# RPMsg Clock 开发指南

\[ [English](../../../../../en/device_dev_guide/kernel/inter_processor_communication/RPMsg/RPMsg_Clock.md) | 简体中文 \]

## 一、概述

RPMsg Clock（Remote Processor Messaging Clock）是一种基于 RPMsg 框架（Remote Processor Messaging Framework）构建的跨核时钟服务，用于实现跨核的时钟控制。

## 二、配置

在使用 RPMsg Clock 时，需要确保以下配置已启用：

```Makefile
# server端和client端均需要使能如下配置
CONFIG_CLK_RPMSG=y
```

- Server 端：包含实际时钟系统的核，负责提供时钟资源。
- Client 端 ：无实际时钟系统，需要访问或控制 Server 端时钟资源的核。

## 三、使用方法

### 1、注册时钟资源

Client 端能够访问或控制 Server 端时钟资源的前提是，Server 端已完成实际时钟子系统的初始化，即通过调用 `clk_register` 完成时钟资源的注册。Client 端无需进行时钟注册。

有关时钟注册的示例代码，请参考以下链接：[nuttx/drivers/clk/song](https://github.com/FishsemiCode/nuttx/tree/song-u1/drivers/clk/song)


### 2、获取时钟实例

在访问或控制时钟资源时，需要通过时钟资源的名称来获取时钟实例。

以下是获取时钟实例的函数定义：

```C
/* name为需要控制的clk源的名称 */
FAR struct clk_s *clk_get(FAR const char *name)；
```

#### 参数说明

- Server 端：
    - `clk_get` 函数的参数为调用 `clk_register` 时传入的时钟资源名称。
- Client 端：
    - `clk_get` 函数的参数需要包含 Server 端的 CPU 名称（`cpuname`）以及时钟资源名称。
    - 例如：假设 Server 端的 CPU 名称为 `"ap"`，需要访问的时钟资源名称为 `"spi_clk"`，则 Client 端调用 `clk_get` 函数时，传入的参数应为 `"ap/spi_clk"`。

## 四、工作原理

### 1、RPMsg 消息处理机制

在 clk driver 中，时钟源通过 `clk_register` 注册到时钟子系统。当需要访问或控制某个时钟源时，可以通过 `clk_get` 获取该时钟源的实例，然后通过该实例关联的 `clk->ops` 结构体对时钟源进行操作。

在 RPMsg Clk 中，`clk->ops` 被抽象为以下操作接口：

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

操作流程

- Client 端请求转发： `g_clk_rpmsg_ops` 中的函数实现会将请求转发给 Server 端。转发的目标由时钟源名称中的 `cpuname` 字符串确定。
- Server 端处理请求： Server 端完成实际的函数调用，并将结果返回给 Client 端。

### 2、启用时钟的处理流程

例如 `clk_rpmsg_enable` 函数会向 Server 端发送 `CLK_RPMSG_ENABLE` 请求。以下是 `clk_rpmsg_enable` 函数的实现，它负责将启用时钟的请求从 Client 端转发到 Server 端：

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

#### 处理逻辑说明

1. 获取通信端点：
    - 函数通过 `clk_rpmsg_get_ept` 获取与目标 Server 端的通信端点。如果通信端点不存在，则返回错误代码 `-ENODEV`。
2. 构造消息：
    - 函数通过 `rpmsg_get_tx_payload_buffer` 分配消息缓冲区，并将时钟名称复制到消息中。
3. 发送请求并接收响应：
    - 函数调用 `clk_rpmsg_sendrecv` 将 `CLK_RPMSG_ENABLE` 请求发送到 Server 端，并等待响应。

### 3、Server 端的请求处理

当 Server 端接收到 `CLK_RPMSG_ENABLE` 请求时，会调用对应的处理函数 `clk_rpmsg_enable_handler`。

以下是消息处理函数的注册表：

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

以下是 `clk_rpmsg_enable_handler` 的具体实现，它负责调用实际的时钟启用函数：

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

#### 处理逻辑说明：

1. 获取时钟实例：
    - 函数通过 `clk_rpmsg_get_clk` 获取指定名称的时钟实例。
    - 如果时钟实例存在，则调用 `clk_enable` 函数启用时钟。
    - 如果时钟实例不存在，则返回错误代码 `-ENOENT`。
2. 更新计数器：
    - 如果时钟启用成功（`clk_enable` 返回 0），则增加时钟的引用计数 `clkrp->count`。
3. 返回结果：
    - 通过 `rpmsg_send` 将操作结果返回给 Client 端。

## 五、相关文档

- 有关时钟驱动的设计，请参考 [Clock](../../../../../zh-cn/device_dev_guide/power_mgt/Clock.md)。
