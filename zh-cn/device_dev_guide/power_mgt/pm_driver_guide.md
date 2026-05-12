# 电源管理驱动开发指南

\[ [English](../../../en/device_dev_guide/power_mgt/pm_driver_guide.md) | 简体中文 \]

本文档指导嵌入式开发者如何为 openvela 系统编写能够参与电源管理 (PM) 的设备驱动程序。通过实现指定的 PM 回调接口，您的驱动可以响应系统的功耗状态变化，从而实现精细化的节能控制。

**目标读者**：需要在特定硬件平台上为设备驱动添加 PM 功能的嵌入式系统开发者。

**前置阅读**： 在开始之前，我们强烈建议您首先阅读[电源管理框架指南](./pm_framework_guide.md)，以充分理解 PM 框架的核心概念，如电源状态 (State)、电源域 (Domain) 和决策者 (Governor)。

## 一、核心 API 与数据结构

驱动程序通过 `pm.h` 中定义的回调结构体和注册函数与 PM 框架进行交互。

**相关头文件**：[openvela include/nuttx/power/pm.h](../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/power/pm.h)

### 1、`pm_state_e` 电源状态枚举

此枚举定义了系统支持的逻辑电源状态。驱动程序在 PM 回调中会接收到此类型的目标状态，并需要根据该状态执行相应的硬件操作。

```C
enum pm_state_e
{
  PM_RESTORE = -1, /* 内部状态：通知驱动从低功耗恢复 */
  PM_NORMAL  = 0,  /* 正常运行状态 */
  PM_IDLE,         /* 空闲状态 */
  PM_STANDBY,      /* 待机状态 */
  PM_SLEEP,        /* 休眠状态 */
  PM_COUNT,        /* 状态总数，用于内部管理 */
};
```

- **注意**：`PM_IDLE`、`PM_STANDBY` 和 `PM_SLEEP` 的具体硬件行为（如时钟频率、外设开关、内存模式等）由芯片平台代码定义和实现。

### 2、`pm_callback_s` 回调结构体

这是驱动程序参与 PM 的核心。您需要在驱动中定义一个此类型的变量，并实现其回调函数指针。在驱动程序初始化时，由 `pm_register` 函数注册到 PM 系统中。

```C
struct pm_callback_s
{
  // 用于内部双向链表
  struct dq_entry_s entry;

  // 回调优先级。值越大，在进入低功耗状态时越早被调用。
  // 默认或相同优先级则遵循注册顺序。
  int prio;

  CODE int (*prepare)(FAR struct pm_callback_s *cb, int domain,
                      enum pm_state_e pmstate);

  CODE void (*notify)(FAR struct pm_callback_s *cb, int domain,
                      enum pm_state_e pmstate);
 }
```

**性能须知**：

PM 框架会在每次检查或改变电源状态时（如在系统空闲循环中）调用已注册的回调。为了不影响系统性能，您的回调函数必须**快速、非阻塞**。如果您的驱动仅需通知而无需准备，或反之，请将不需要的函数指针设置为 `NULL` 以避免不必要的函数调用。

![img](./figures/010.png)

#### `prepare` 回调函数

- **用途**：在 PM 框架准备进入低功耗状态之前，会调用所有已注册 `prepare` 的设备是否就绪。例如，检查串口的 DMA 缓冲区或发送队列是否仍有数据待处理。

- **最佳实践**：应优先考虑在业务逻辑层使用 **Wakelock** ([PM wakelock用法](./pm_wakelock_guide.md)) 来阻止系统休眠。仅当无法在业务层预知设备状态时（如突发的 DMA 请求），才使用 `prepare` 回调作为最后防线。

- **说明**：如果仅需要 `notify`，`prepare` 需要设置成NULL，以减少不必要的函数调用。

- **参数**：

    - `cb`：您注册的回调结构体指针。
    - `domain`：发起状态切换的电源域。
    - `pmstate`：PM 框架期望进入的目标电源状态。

- **返回值**：

    - `OK` (0)：表示设备已准备就绪，允许状态切换继续。
    - `<0`：表示设备未就绪，PM 框架将**中止**本次状态切换。

#### `notify` 回调函数

当所有驱动的 `prepare` 回调都返回 `OK` 后，PM 框架会调用 `notify` 回调来**执行**实际的硬件操作。

- **用途**：驱动程序根据通知的 domain 和目标状态 `pmstate`，执行实际的硬件电平转换。例如：关闭外设时钟、进入时钟门控、设置引脚状态、或从低功耗状态中恢复设备配置。
- **说明：**如果仅需要 `prepare`，`notify` 需要设置成 NULL，以减少不必要的函数调用。
- **参数**：

    - `cb`：您注册的回调结构体指针。
    - `domain`：发起状态切换的电源域。
    - `pmstate`：PM 框架正在进入的目标电源状态。

- **返回值**：无。此阶段不允许否决状态切换。

### 3、回调注册函数

#### pm_domain_register

将您的 `pm_callback_s` 结构体注册到指定 `domain` 的回调列表中。这是通用的注册接口，类似于 `pm_register`，但是适用于定义了多个 domain 的场景。

```C
int pm_domain_register(int domain, FAR struct pm_callback_s *cb)
```

#### pm_register

这是一个便利宏，用于将回调注册到默认的 `PM_IDLE_DOMAIN` (domain 0)。对于单核或不区分电源域的简单系统，使用此宏即可。

```C
#define pm_register(cb) pm_domain_register(PM_IDLE_DOMAIN, cb)
```

## 二、驱动开发实战：以 STM32 串口驱动为例

本节以 stm32f7 的串口驱动为例，展示如何一步步实现 PM 功能。

**源码参考**：[arch/arm/src/stm32f7/stm32_serial.c](../../../../../../nuttx/blob/dev-ai-contest-2026/arch/arm/src/stm32f7/stm32_serial.c)

### 步骤 1：定义回调结构体和状态变量

在驱动文件中，定义一个包含 `pm_callback_s` 和其他 PM 相关状态的结构体。

```C
#ifdef CONFIG_PM
/* 专用于 PM 的结构体，包含回调和驱动内部状态 */
static struct pm_config_s g_serialpm =
{
  .pm_cb.notify     = up_pm_notify,   /* 关联 notify 实现 */
  .pm_cb.prepare    = up_pm_prepare,  /* 关联 prepare 实现 */
  .serial_suspended = false
};
#endif
```

### 步骤 2：实现 `prepare` 回调

此函数负责在进入 `STANDBY` 或 `SLEEP` 状态前，检查串口是否有未完成的数据传输。

```C
static int up_pm_prepare(struct pm_callback_s *cb, int domain,
                         enum pm_state_e pmstate)
{
  int n;

  /* Logic to prepare for a reduced power state goes here. */
  switch (pmstate)
    {
    case PM_NORMAL:
    case PM_IDLE:
      break;

    case PM_STANDBY:
    case PM_SLEEP:

#ifdef SERIAL_HAVE_RXDMA
      /* 确保所有 DMA 操作已同步 */
      stm32_serial_dma_poll();
#endif

      /* 遍历所有已初始化的串口设备 */
      for (n = 0; n < STM32F7_NUSART + STM32F7_NUART; n++)
        {
          struct up_dev_s *priv = g_uart_devs[n];

          if (!priv || !priv->initialized)
            {
              /* Not active, skip. */
              continue;
            }

          if (priv->suspended)
            {
              /* Port already suspended, skip. */
              continue;
            }

          if (priv->dev.isconsole)
            {
              /* Allow losing some debug traces. */
              continue;
            }

          /* 若发送或接收缓冲区非空，则返回错误以阻止休眠 */
          if (priv->dev.xmit.head != priv->dev.xmit.tail)
            {
              return ERROR;
            }

          if (priv->dev.recv.head != priv->dev.recv.tail)
            {
              return ERROR;
            }
        }
      break;

    default:
      /* Should not get here */
      break;
    }

  return OK;
}
```

在进入 `PM_STANDY`，`PM_SLEEP` 状态值之前，driver 会检测串口的缓冲区是否还有数据：

- 如果有，就会返回 ERROR，阻止 PM 进入该低功耗状态。
- 其他情况则返回 OK， PM 系统可以正常进入该低功耗状态。

### 步骤 3：实现 `notify` 回调

此函数根据 PM 框架的最终决定，执行挂起或恢复串口的操作。

```C
static void up_pm_notify(struct pm_callback_s *cb, int domain,
                         enum pm_state_e pmstate)
{
  switch (pmstate)
    {
      case PM_NORMAL:
        {
          /*
          * 目标状态是活动状态 (NORMAL/IDLE) 或从休眠唤醒 (RESTORE)，
          * 此时应恢复串口功能。
          */
          up_pm_setsuspend(false);
        }
        break;

      case PM_IDLE:
        {
          up_pm_setsuspend(false);
        }
        break;

      case PM_STANDBY:
        {
          /* 目标状态是低功耗状态，挂起串口功能 */
          up_pm_setsuspend(true);
        }
        break;

      case PM_SLEEP:
        {
          up_pm_setsuspend(true);
        }
        break;

      default:

        /* Should not get here */

        break;
    }
}
```

在 `pm_notify` 里面分了两种情况

- <= PM_IDLE 时：调用 `up_pm_setsuspend(false)`
- \>= PM_IDLE 时：调用 `up_pm_setsuspend(true)`

```C
static void up_pm_setsuspend(bool suspend)
{
  int n;

  /* Already in desired state? */
  if (suspend == g_serialpm.serial_suspended)
    {
      return;
    }

  g_serialpm.serial_suspended = suspend;

  for (n = 0; n < STM32F7_NUSART + STM32F7_NUART; n++)
    {
      struct up_dev_s *priv = g_uart_devs[n];

      if (!priv || !priv->initialized)
        {
          continue;
        }

      up_setsuspend(&priv->dev, suspend);
    }
}
```

`up_pm_setsuspend()` 函数是实际执行硬件操作的地方。

- **挂起 (suspend) 操作**：

    1. 如果有流控，先拉高 GPIO 阻止继续接收 RX 数据。
    2. 关闭 TX 中断，阻止接收 TX 数据。
    3. 清空串口目前的 TX FIFO 里面数据。
    4. 如果有 DMA，停止 DMA。
    5. 最佳实践：为了最大化节能，还应在此处关闭相关模块的时钟，并在可能的情况下关闭相关模块的电源。

- **恢复 (resume) 操作**：

    1. 最佳实践：打开相关模块时钟和电源。
    2. 如果有 DMA，打开 DMA。
    3. 重启串口 TX 中断。

#### 处理 `PM_RESTORE` 状态

`PM_RESTORE` 是一个特殊的通知，它告诉驱动系统正在从 `STANDBY` 或 `SLEEP` 状态唤醒。驱动必须在此通知中执行恢复操作。

在某些简单场景下（如本串口示例），恢复操作可能与进入 `PM_NORMAL` 状态的操作相同。但在需要显式管理时钟和电源的复杂驱动中（例如 Regulator 驱动），必须在 `case PM_RESTORE` 分支中处理硬件的恢复。

当前驱动未处理 `PM_RESTORE`，低功耗退出之后功能会自动恢复，如果需要进行时钟开关动作需要在 `notify` 中同步进行 `resume`。

**源码参考**：[regulator.c 对 PM_RESTORE 的处理](../../../../../../nuttx/blob/d0f8abc4ece6a8c1924dd2d1c64f773c7db51d8f/drivers/power/supply/regulator.c#L471-L476)

### 步骤 4：在驱动初始化时注册回调

最后，在驱动的初始化函数（如 `arm_serialinit`）中，调用 `pm_register` 将您的回调注册到 PM 框架。

```C
#ifdef CONFIG_PM
  ret = pm_register(&g_serialpm.pm_cb);
  if (ret < 0)
    {
      /* 处理注册失败的错误 */
    }
#endif
```

## 三、核心要点与最佳实践

- 执行上下文：PM 回调函数 IDLE 线程中执行，此时中断可能被部分或全部禁用。因此，回调实现必须**极其高效、非阻塞，且严禁任何可能导致线程切换的操作**（如获取信号量）。
- 注册：驱动程序通过 `pm_domain_register()` 向**特定**的电源域注册回调。`pm_register()` 是注册到默认域 `PM_IDLE_DOMAIN` 的简化宏。您的回调函数应检查传入的 `domain` 参数，以支持多域系统。
- 在 `prepare` 函数中，检查当前模块是否允许进入 `pm_state`，如果存在问题，需要返回错误码。
- 在 `notify` 函数中，执行 `pm_state` 相关的操作，确保驱动进入相对应的低功耗状态，操作包括但不限于：

    - 停止数据传输（DMA和中断）。
    - 关闭模块时钟。
    - 关闭模块电源。

## 四、相关文档

- [在 IDLE 线程中实现电源管理](./pm_idle_impl.md)