# Arch Alarm 框架开发指南

\[ [English](../../../../../en/device_dev_guide/driver/timer_driver/timer/Arch_Alarm.md) | 简体中文 \]

## 一、本文目标

本文主要介绍基于 **oneshot** 驱动的 **arch_alarm** 驱动框架设计与实现，以及相关接口使用及实现说明。

- 应用开发者/测试人员：可参考[测试实例](#八测试实例)章节进行开发或者测试。
- 驱动开发者可以参考[驱动适配实例](#六驱动适配实例)章节进行驱动开发。

## 二、概述

### 1、Oneshot 驱动总体架构

openvela 提供通用的 **oneshot** 驱动，即一次性（非周期性）定时器。该驱动遵循 openvela 驱动框架，分为两个部分：

- **Upper half**：面向应用，由 openvela 提供，无需芯片厂商修改。
- **Lower half**：特定平台的硬件控制驱动，芯片厂商需适配提供。

**oneshot** 驱动相关接口信息在 [oneshot.h](../../../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/timers/oneshot.h) 文件中，同样也分为了 **Upper half** 和 **Lower half** 两层接口。

### 2、Arch_alarm 定时器简介

- 基于 **oneshot** 驱动实现的 `arch_alarm` 提供定时器功能，供 **sched** 模块调用。
- 支持两种工作模式：
    - **Tickless**（无周期中断模式）：在此模式下，系统不会周期性产生中断，从而减少了功耗，适用于低功耗应用场景。
    - **Tick**（周期中断模式）：此模式下，系统会按照预定的时间间隔触发定时器中断，适用于需要精确时序控制的应用。
- `arch_alarm` 在系统架构中的位置如下图所示：

    ![img](./figures/004.svg)

### 3、应用接口调用方式

#### 3.1 调用方式

- 标准 POSIX API：支持通过标准的 POSIX（Portable Operating System Interface for uniX，可移植操作系统接口） API，具体为 `<time.h>` 头文件中定义的相关定时器接口进行调用。
- `ioctl` 系统调用：可通过 `ioctl`（input/output control，输入输出控制）系统调用与 Upper Half 和 Lower Half 进行交互，适用于自定义控制与设备管理场景。

#### 3.2 注意事项

openvela 的 Upper half 部分中的 **`up_timer_initialize`** 函数，必须由芯片厂商（SoC 或 MCU 供应商）实现。未实现时相关定时器功能无法正常工作。

#### 3.3 调用流程

![img](./figures/005.svg)

## 三、Arch_alarm API

`arch_alarm` 提供一系列接口，以满足 sched 模块对定时器的需求。接口信息可在 [arch.h](../../../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/arch.h) 头文件中查找。

### 1、接口分类

在 **Tickless** 模式下这些接口又根据时间单位的不同划分为两组：

- 使用 `struct timespec` 结构的接口
- 基于 `tick`（系统节拍计数）的接口

### 2、接口说明

- `up_alarm_set_lowerhalf`

    初始化 alarm 定时器，入参为 oneshot_lowerhalf_s 实例。

    ```C
    void up_alarm_set_lowerhalf(FAR struct oneshot_lowerhalf_s *lower)
    ```

- `up_alarm_tick_start`

    启动 alarm 定时器，仅在 Tickless 模式下使用，入参为 alarm 的超时时间，单位为 ticks。

    ```C
    int weak_function up_alarm_tick_start(clock_t ticks)
    ```

- `up_alarm_tick_cancel`

    停止 alarm 定时器，仅在 Tickless 模式下使用，返回当前 alarm 剩余的 ticks 数。

    ```C
    int weak_function up_alarm_tick_cancel(FAR clock_t *ticks)
    ```

- `up_timer_getmask`

    获取 alarm 定时器时长的 mask 值。

    ```C
    void weak_function up_timer_getmask(FAR clock_t *mask)
    ```

- `up_timer_gettick`

    获取 alarm 定时器当前已经经历的 ticks。

    ```C
    int weak_function up_timer_gettick(FAR clock_t *ticks)
    ```

- `up_udelay`

    实现微秒级的延迟操作。

    ```C
    void weak_function up_udelay(useconds_t microseconds)
    ```

- `up_mdelay`

    实现毫秒级的延迟操作。

    ```C
    void weak_function up_mdelay(unsigned int milliseconds)
    ```

## 四、Oneshot 驱动

### 1、配置说明

#### 1.1 核心配置项

在 openvela 板级适配过程中，需完成以下关键配置项的设置，以启用系统核心功能与低功耗特性：

- 使能 oneshot 驱动

    - 通过设置 `CONFIG_ONESHOT` 配置项启用 oneshot 驱动。
    - 该配置为必选项，确保 oneshot 驱动正常工作，从而支持系统的定时器相关功能。

- 使能 arch_alarm

    - 通过配置 `CONFIG_ALARM_ARCH` 启用 arch_alarm 驱动。
    - 该配置同样为必选项，arch_alarm 在系统的时间管理和任务调度中扮演着重要角色。

- 使能 TICKLESS 低功耗模式

    - 通过配置 `CONFIG_SCHED_TICKLESS` 启用 TICKLESS 低功耗模式。
    - 在该模式下，系统将不再产生周期性的时钟中断。
    - 当系统中没有任务需要执行时，系统会自动进入 idle 模式，直至下一次任务执行或有中断产生。
    - 是否选择配置此模式，需要根据系统对低功耗支持的需求决定。

#### 1.2 配置文件说明

##### `sched/Kconfig` 文件配置

在 `sched/Kconfig` 文件中，与上述配置相关的内容如下：

```Shell
# sched/Kconfig
config SCHED_TICKLESS  depends on ARCH_HAVE_TICKLESS # 硬件需支持 Tickless 模式
if SCHED_TICKLESS
    config SCHED_TICKLESS_TICK_ARGUMENT
    config SCHED_TICKLESS_ALARM
    config SCHED_TICKLESS_LIMIT_MAX_SLEEP
#endif
```

`SCHED_TICKLESS` 的配置依赖于 `ARCH_HAVE_TICKLESS`。

##### `drivers/timers/Kconfig` 文件配置

在 `drivers/timers/Kconfig` 文件中，相关配置如下：

```Shell
# drivers/timers/Kconfig
config ONESHOT
......
if ONESHOT
config ALARM_ARCH
    select ARCH_HAVE_TICKLESS
    select ARCH_HAVE_TIMEKEEPING
    select SCHED_TICKLESS_ALARM  if SCHED_TICKLESS
    select SCHED_TICKLESS_LIMIT_MAX_SLEEP  if SCHED_TICKLESS
    select SCHED_TICKLESS_TICK_ARGUMENT  if SCHED_TICKLESS
#endif
```

#### 1.3 配置验证

为了确保上述配置正确生效，可以使用以下命令进行检查：

```Shell
grep -rE "CONFIG_ONESHOT|CONFIG_ALARM_ARCH|CONFIG_ARCH_HAVE_TICKLESS|CONFIG_ARCH_HAVE_TIMEKEEPING|CONFIG_SCHED_TICKLESS|CONFIG_SCHED_TICKLESS_TICK_ARGUMENT|CONFIG_SCHED_TICKLESS_ALARM|CONFIG_SCHED_TICKLESS_LIMIT_MAX_SLEEP" nuttx/.config
```

该命令会在 `nuttx/.config` 文件中递归搜索相关的配置项，以确认配置是否已经正确设置。

### 2、Oneshot 初始化

#### 2.1 初始化流程总览

在 openvela 的板级适配中，Oneshot 定时器的初始化需完成**实例创建**、**设备注册**和**系统绑定**三个核心步骤，确保定时器驱动与系统低功耗模块（TICKLESS）的协同工作。以下是具体实现流程。

##### 实例创建：调用 `oneshot_initialize`

在板级初始化阶段，需调用**厂商自定义的初始化函数**，完成 [struct oneshot_lowerhalf_s](../../../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/timers/oneshot.h#L226) 结构体的分配与初始化。该函数由 openvela 框架提供，原型如下：

```C
/****************************************************************************
 * Name: oneshot_initialize
 *
 * Description:
 *   Initialize the oneshot timer and return a oneshot lower half driver
 *   instance.
 *
 * Input Parameters:
 *   chan       Timer counter channel to be used.
 *   resolution The required resolution of the timer in units of
 *              microseconds.  NOTE that the range is restricted to the
 *              range of uint16_t (excluding zero).
 *
 * Returned Value:
 *   On success, a non-NULL instance of the oneshot lower-half driver is
 *   returned.  NULL is return on any failure.
 *
 ****************************************************************************/
FAR struct oneshot_lowerhalf_s *oneshot_initialize(int chan, uint16_t resolution);
```

操作说明：

- 该函数负责底层硬件寄存器初始化、中断配置等底层操作。
- 返回的实例包含定时器驱动的核心数据（如中断处理函数、时钟源配置等），需妥善保存用于后续注册。

##### 设备注册：调用 `oneshot_register`

将 `oneshot_initialize` 返回的实例与系统设备模型绑定，注册字符设备节点（如 `/dev/oneshot`），并关联文件操作接口 `struct file_operations g_oneshot_ops`。函数 [oneshot_register](../../../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/timers/oneshot.c#L291) 原型如下：

```C
/****************************************************************************
 * Name: oneshot_register
 *
 * Description:
 *   Register the oneshot device as 'devpath'
 *
 * Input Parameters:
 *   devpath - The full path to the driver to register. E.g., "/dev/oneshot0"
 *   lower - An instance of the lower half interface
 *
 * Returned Value:
 *   Zero (OK) on success; a negated errno value on failure.  The following
 *   possible error values may be returned (most are returned by
 *   register_driver()):
 *
 *   EINVAL - 'path' is invalid for this operation
 *   EEXIST - An inode already exists at 'path'
 *   ENOMEM - Failed to allocate in-memory resources for the operation
 *
 ****************************************************************************/
int oneshot_register(FAR const char *devname,
                     FAR struct oneshot_lowerhalf_s *lower)
```

操作说明：

- 注册后，上层应用可通过标准 POSIX 接口（如 `open`/`ioctl`）访问定时器功能。
- 需确保 `g_oneshot_ops` 实现了 `read`/`write`/`ioctl` 等必要文件操作。

##### 系统绑定：实现 `up_timer_initialize` 函数

平台相关代码需实现 `up_timer_initialize` 函数，将 Oneshot 实例与系统 TICKLESS 低功耗模块绑定。

具体步骤：

1. 调用 `oneshot_initialize` 分配驱动实例。
2. 通过 `up_alarm_set_lowerhalf` 函数将实例注册为系统定时器后端。

核心作用：

- `up_alarm_set_lowerhalf` 函数将 Oneshot 驱动的中断处理与调度器关联，使能无周期时钟中断的 TICKLESS 模式。
- 当系统无任务运行时，通过该实例进入低功耗 idle 模式，直至下一次任务唤醒或中断触发。

#### 2.2 参考实现与调试

- 结构体定义：`struct oneshot_lowerhalf_s` 的成员说明详见 [oneshot.h](../../../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/timers/oneshot.h#L226)，需按硬件特性填充中断触发、定时器启动等函数指针。
- 实例代码：具体驱动适配示例可参考[驱动适配实例-初始化章节](#1初始化流程)，注意根据目标平台（如 ARM Cortex-M/RISC-V）调整硬件寄存器操作逻辑。
- 调试建议：初始化失败时，检查 `CONFIG_ONESHOT`/`CONFIG_ALARM_ARCH` 是否正确使能，并利用串口日志打印 `oneshot_initialize` 的返回值。

### 3、Upper-half 接口

在 openvela 中，Upper-half 接口为内核模块提供统一的定时器服务，兼容 Tickless 模式与 Tick 模式。其设计目标是通过抽象化时间管理，降低调度器（Sched）与硬件架构层（Arch）的耦合性。

#### 3.1 Tickless 模式下接口划分

通过配置 `CONFIG_SCHED_TICKLESS_TICK_ARGUMENT` 选择时间单位类型：

| 模式          | 时间单位                      | 适用场景                     | 配置项                                     |
| ------------- | ----------------------------- | ---------------------------- | ------------------------------------------ |
| Tick 接口     | 系统节拍（Ticks）             | 需与硬件定时器节拍对齐的场景 | 默认启用                                   |
| Timespec 接口 | 高精度时间（struct timespec） | 需纳秒级精度的实时任务       | 配置 CONFIG_SCHED_TICKLESS_TICK_ARGUMENT=n |

设计原则：

- 减少时间转换开销：默认使用 Tick 接口，避免 `struct timespec` 与 Ticks 的频繁转换。
- 灵活性：开发者可根据需求动态切换时间单位。

#### 3.2 核心接口说明

Upper-half 接口定义于 [arch.h](../../../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/arch.h#L1460)，主要供调度器（Sched）调用。

### 4、Lower-half 接口

在 openvela 的硬件抽象层（Hardware Abstraction Layer, HAL）开发中，Lower-half 接口通过 `struct oneshot_operations_s` 定义了底层定时器的操作逻辑。

该接口支持两种时间单位（`struct timespec` 与 `tick`），开发者可根据硬件特性选择实现其中一组，未实现的接口由 openvela 提供默认转换逻辑。

#### 4.1 接口分类与实现策略

##### 时间单位选择

- `struct timespec`

    - 提供纳秒级时间精度，适用于高精度定时场景。
    - 需直接操作硬件计时器寄存器，实现复杂度较高。

- `tick`

    - 基于系统节拍（Ticks）的时间单位，与硬件定时器周期对齐。
    - 实现简单，适合资源受限的嵌入式设备。

##### 实现策略

- 厂商选择

    - 根据硬件能力选择实现 `timespec` 或 `tick` 接口组。
    - 未实现的接口组可通过 openvela 内置的[转换函数](../../../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/timers/oneshot.h)自动映射。

- 性能优化
  
    - 优先实现硬件原生支持的接口组，减少转换开销。

#### 4.2 核心接口说明

`struct oneshot_operations_s` 定义于 [oneshot.h](../../../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/timers/oneshot.h)，其成员函数如下。

##### 定时器控制接口

```C
struct oneshot_operations_s
{
  /* 启动定时器（相对时间） */  
  CODE int (*start)(FAR struct oneshot_lowerhalf_s *lower,
                    oneshot_callback_t callback, FAR void *arg,
                    FAR const struct timespec *ts);
  CODE int (*tick_start)(FAR struct oneshot_lowerhalf_s *lower,
                         oneshot_callback_t callback, FAR void *arg,
                         clock_t ticks);
  
  /* 取消定时器并返回剩余时间 */    
  CODE int (*cancel)(FAR struct oneshot_lowerhalf_s *lower,
                     FAR struct timespec *ts);
  CODE int (*tick_cancel)(FAR struct oneshot_lowerhalf_s *lower,
                          FAR clock_t *ticks);
                      
  /* 获取当前时间（系统上电后累计时间） */                        
  CODE int (*current)(FAR struct oneshot_lowerhalf_s *lower,
                      FAR struct timespec *ts);                         
  CODE int (*tick_current)(FAR struct oneshot_lowerhalf_s *lower,
                           FAR clock_t *ticks);
                       
  /* 获取定时器最大支持延时 */                          
  CODE int (*max_delay)(FAR struct oneshot_lowerhalf_s *lower,
                        FAR struct timespec *ts);
  CODE int (*tick_max_delay)(FAR struct oneshot_lowerhalf_s *lower,
                             FAR clock_t *ticks);
};
```

##### 关键参数说明

- `oneshot_callback_t`：定时器到期时的回调函数指针。
- `ts`/`ticks`：输入/输出参数，分别表示高精度时间或节拍数。

#### 4.3 适配实例参考

- 代码示例：[驱动适配实例 Lower-half 接口章节](#12-关键代码实现)

## 五、流程说明

在 openvela 中，`Tickless` 模式与 `Tick` 模式的 arch alarm 调用逻辑存在显著差异，具体流程如下。

### 1、Tickless 模式

#### 1.1 核心逻辑

- 动态调度机制：调度器（sched）实时监控已注册的看门狗定时器（wdogs），选择**最短超时时间**的 wdogs 作为下一次闹钟（Alarm）的触发阈值。因此 sched 需要根据当前 wdog 的状态启动或停止 alarm 定时器。

- 资源优化：

    - 仅在必要时启动/停止定时器，避免周期性中断的开销。
    - 空闲时段系统进入低功耗状态，显著降低功耗。

#### 1.2 调用流程

![img](./figures/006.svg)

### 2、Tick 模式

#### 2.1 核心逻辑

- 固定周期定时器：
  
    - 初始化时启动周期为 `CONFIG_USEC_PER_TICK` 微秒的定时器。
    - 定时器周期性触发中断，驱动任务调度。

- 性能权衡：

    - 简化调度逻辑，减少动态启停操作。

#### 2.2 调用流程

![img](./figures/007.svg)

## 六、驱动适配实例

以 RISC-V 架构的 BL602 芯片为例，openvela 的 oneshot 驱动适配流程如下。

### 1、初始化流程

#### 1.1 代码执行路径

```Shell
nx_start
-> clock_initialize
   -> up_timer_initialize  # 开发者实现
      ->up_alarm_set_lowerhalf # 调用该接口，openvela 已实现
board_late_initialize (或 board_app_initialize) 
-> bl602_bringup           #开发者实现
   -> oneshot_initialize   #开发者实现
   -> oneshot_register
```

#### 1.2 关键代码实现

- 硬件（Arch 层）定时器初始化，参考代码 [arch/risc-v/src/bl602/bl602_timerisr.c](../../../../../../../../nuttx/blob/dev-ai-contest-2026/arch/risc-v/src/bl602/bl602_timerisr.c#L57)。

    ```C
    /****************************************************************************
     * Name: up_timer_initialize
     *
     * Description:
     *   This function is called during start-up to initialize
     *   the timer interrupt.
     *
     ****************************************************************************/
    
    void up_timer_initialize(void)
    {
      struct oneshot_lowerhalf_s *lower = riscv_mtimer_initialize(
        BL602_CLIC_MTIME, BL602_CLIC_MTIMECMP,
        RISCV_IRQ_MTIMER, MTIMER_FREQ);
    
      DEBUGASSERT(lower);
    
      up_alarm_set_lowerhalf(lower);
    }
    ```

- Oneshot 驱动实例化，参考代码 [arch/risc-v/src/bl602/bl602_oneshot_lowerhalf.c](../../../../../../../../nuttx/blob/dev-ai-contest-2026/arch/risc-v/src/bl602/bl602_oneshot_lowerhalf.c#L361)。

    ```C
    struct oneshot_lowerhalf_s *oneshot_initialize(int      chan,
                                                   uint16_t resolution)
    {
      struct bl602_oneshot_lowerhalf_s *priv;
      struct timer_cfg_s                    timstr;
    
      /* Allocate an instance of the lower half driver */
      priv = (struct bl602_oneshot_lowerhalf_s *)kmm_zalloc(
        sizeof(struct bl602_oneshot_lowerhalf_s));
    
      if (priv == NULL)
        {
          tmrerr("ERROR: Failed to initialized state structure\n");
          return NULL;
        }
    
      /* Initialize the lower-half driver structure */
      priv->started = false;
      priv->lh.ops  = &g_oneshot_ops;
      priv->freq    = TIMER_CLK_FREQ / resolution;
      priv->tim     = chan;
      if (priv->tim == TIMER_CH0)
        {
          priv->irq = BL602_IRQ_TIMER_CH0;
        }
      else
        {
          priv->irq = BL602_IRQ_TIMER_CH1;
        }
    
      /* Initialize the contained BL602 oneshot timer */
      timstr.timer_ch = chan;              /* Timer channel */
      timstr.clk_src  = TIMER_CLKSRC_FCLK; /* Timer clock source */
      timstr.pl_trig_src =
        TIMER_PRELOAD_TRIG_COMP0; /* Timer count register preload trigger source
                                   * select */
    
      timstr.count_mode = TIMER_COUNT_PRELOAD; /* Timer count mode */
      timstr.clock_division =
        (TIMER_CLK_DIV * resolution) - 1; /* Timer clock division value */
    
      timstr.match_val0 = TIMER_MAX_VALUE; /* Timer match 0 value 0 */
      timstr.match_val1 = TIMER_MAX_VALUE; /* Timer match 1 value 0 */
      timstr.match_val2 = TIMER_MAX_VALUE; /* Timer match 2 value 0 */
    
      timstr.pre_load_val = TIMER_MAX_VALUE; /* Timer preload value */
    
      bl602_timer_intmask(chan, TIMER_INT_ALL, 1);
    
      /* timer disable */
    
      bl602_timer_disable(chan);
    
      bl602_timer_init(&timstr);
    
      return &priv->lh;
    }
    ```

### 2、Lower-half 接口实现

操作接口绑定如下，详细代码请参考 [arch/risc-v/src/bl602/bl602_oneshot_lowerhalf.c](../../../../../../../../nuttx/blob/dev-ai-contest-2026/arch/risc-v/src/bl602/bl602_oneshot_lowerhalf.c#L96)。

```C
/* "Lower half" driver methods */
static const struct oneshot_operations_s g_oneshot_ops =
{
  .max_delay = bl602_max_delay,
  .start     = bl602_start,
  .cancel    = bl602_cancel,
  .current   = bl602_current,
};
```

## 七、POSIX 定时器 API 与 IOCTL 控制

openvela 提供标准定时器接口，支持高精度时间管理与设备控制。

### 1、POSIX 定时器 API

下面是定时器 API 的简单介绍，具体说明请参见 man 手册，命令如下：

```Bash
man timer_create
```

详细代码请参见 [include/time.h](../../../../../../../../nuttx/blob/dev-ai-contest-2026/include/time.h#L233)。

```C
/*
* 函数：timer_create
* 参数：clockid，定时类型；CLOCK_REALTIME相对时间,TIMER_ABSTIME绝对时间
*      evp,sigevent结构体，用来指定定时器到期时如何响应
*      timerid，返回一个timerid，可以用来删除定时等
* 返回：0 success | -1 error
* 说明：创建一个定时器
*/
int timer_create(clockid_t clockid, FAR struct sigevent *evp,
                FAR timer_t *timerid);

/*
* 函数：timer_delete
* 参数：timerid，执行timer_create返回的timerid
* 返回：0 success | -1 error
* 说明：删除一个定时器
*/
int timer_delete(timer_t timerid);

/* 设置定时器
* 函数：timer_settime
* 参数：timerid：id
*      flags：相对时间/绝对时间
*      value：定时时间和间隔
*      ovalue：若不为NULL，则返回上次定时的剩余到期时间 
* 返回：0 success | -1 error
* 说明：设置定时
*/
int timer_settime(timer_t timerid, int flags,
                  FAR const struct itimerspec *value,
                  FAR struct itimerspec *ovalue);

/*
* 函数： timer_gettime
* 参数： timerid：id
*       value：传入itimerspec
* 返回值：0 success | -1 error
* 说明：  获取当前定时器的剩余到期时间
* 
*/
int timer_gettime(timer_t timerid, FAR struct itimerspec *value);

/*
* 函数：   up_timer_gettime
* 参数：   timerid
* 返回值： 定时器超时次数
*/
int timer_getoverrun(timer_t timerid);
```

### 2、IOCTL API

应用程序可以通过 `ioctl` 函数直接操作 Oneshot 定时器。使用该功能之前，需在系统启动（bringup）过程中注册 `/dev/oneshot` 设备节点。请参考头文件 [include/nuttx/timers/oneshot.h](../../../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/timers/oneshot.h#L41) 获取当前支持的 `ioctl` 命令。命令简介如下：

- `OSIOC_START`
    - 功能：启动 Oneshot 定时器。
    - 参数类型： `struct oneshot_start_s*`
    - 参数说明：指定定时器的时长，以及超时后需通知的任务 ID 和事件信息。

- `OSIOC_CANCEL`
    - 功能：停止 Oneshot 定时器。
    - 参数类型：`struct timespec*`
    - 参数说明：入参 ts 返回定时器剩余的时间。

- `OSIOC_CURRENT`
    - 功能：获取 Oneshot 定时器当前的时间。
    - 参数类型： `struct timespec*`。
    - 参数说明：返回定时器当前时间。

- `OSIOC_MAXDELAY`
    - 功能：获取 Oneshot 定时器的最大时延。
    - 参数类型： `struct timespec*`。
    - 参数说明：返回定时器最大时延。

## 八、测试实例

### 1、代码路径

- 文件位置：apps/testing/drivertest/drivertest_oneshot.c

### 2、代码说明

此文件包含用于测试 Oneshot 定时器功能的示例代码。代码采用 C 语言，并利用 **C Mocka** 测试框架进行单元测试。主要功能包括启动 Oneshot 定时器、获取当前时间，以及验证定时器的工作情况。

### 3、代码结构

```C
/****************************************************************************
 * Included Files
 ****************************************************************************/

#include <nuttx/config.h>
#include <stdio.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>
#include <setjmp.h>
#include <cmocka.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <nuttx/timers/oneshot.h>

/****************************************************************************
 * Pre-processor Definitions
 ****************************************************************************/

#define DEFAULT_TIME_OUT 2
#define ONESHOT_DEFAULT_DEVPATH "/dev/oneshot"
#define ONESHOT_SIGNO 13
#define ONESHOT_DEFAULT_NSAMPLES 5

#define OPTARG_TO_VALUE(value, type, base)                            \
  do                                                                  \
    {                                                                 \
      FAR char *ptr;                                                  \
      value = (type)strtoul(optarg, &ptr, base);                      \
      if (*ptr != '\0')                                               \
        {                                                             \
          printf("Parameter error: -%c %s\n", ch, optarg);            \
          show_usage(argv[0], EXIT_FAILURE);                          \
        }                                                             \
    } while (0)

/****************************************************************************
 * Private Types
 ****************************************************************************/

struct oneshot_state_s
{
  char devpath[PATH_MAX];
  struct oneshot_start_s oneshot;
};

/****************************************************************************
 * Private Data
 ****************************************************************************/

/****************************************************************************
 * Private Functions
 ****************************************************************************/

/****************************************************************************
 * Name: show_usage
 ****************************************************************************/

static void show_usage(FAR const char *progname, int exitcode)
{
  printf("Usage: %s"
         " -s <seconds> -d <path>\n",
         progname);

  exit(exitcode);
}

/****************************************************************************
 * Name: parse_commandline
 ****************************************************************************/

static void parse_commandline(FAR struct oneshot_state_s *oneshot_state,
                              int argc, FAR char **argv)
{
  int ch;
  time_t converted;

  while ((ch = getopt(argc, argv, "s:d:")) != ERROR)
    {
      switch (ch)
        {
          case 's':
            OPTARG_TO_VALUE(converted, time_t, 10);
            if (converted < 1 || converted > INT_MAX)
              {
                printf("signal out of range: %lld\n", converted);
                show_usage(argv[0], EXIT_FAILURE);
              }

            oneshot_state->oneshot.ts.tv_sec = converted;
            break;

          case 'd':
            strlcpy(oneshot_state->devpath, optarg,
                                sizeof(oneshot_state->devpath));
            break;

          case '?':
            printf("Unsupported option: %s\n", optarg);
            show_usage(argv[0], EXIT_FAILURE);
            break;
        }
    }
}

/****************************************************************************
 * Name: test_case_oneshot
 ****************************************************************************/

static void test_case_oneshot(FAR void **state)
{
  int ret;
  int fd;
  int i;
  long int trigger_before;
  struct timespec ts;
  sigset_t set;
  FAR struct oneshot_state_s *oneshot_state =
    (FAR struct oneshot_state_s *)*state;

  oneshot_state->oneshot.pid = getpid();

  signal(ONESHOT_SIGNO, SIG_IGN);
  sigemptyset(&set);
  sigaddset(&set, ONESHOT_SIGNO);
  oneshot_state->oneshot.event.sigev_notify = SIGEV_SIGNAL;
  oneshot_state->oneshot.event.sigev_signo = ONESHOT_SIGNO;
  oneshot_state->oneshot.event.sigev_value.sival_ptr = NULL;

  fd = open(oneshot_state->devpath, O_RDONLY);
  assert_true(fd > 0);

  for (i = 0; i < ONESHOT_DEFAULT_NSAMPLES; i++)
    {
      /* Start the oneshot */

      ret = ioctl(fd, OSIOC_START, &oneshot_state->oneshot);
      assert_return_code(ret, OK);

      /* Get current ts */

      ret = ioctl(fd, OSIOC_CURRENT, &ts);
      assert_return_code(ret, OK);
      trigger_before = ts.tv_sec;

      ret = sigwaitinfo(&set, NULL);
      assert_return_code(ret, ONESHOT_SIGNO);

      ret = ioctl(fd, OSIOC_CURRENT, &ts);
      assert_return_code(ret, OK);

      assert_int_equal(oneshot_state->oneshot.ts.tv_sec, ts.tv_sec
                       - trigger_before);
    }
  ret = ioctl(fd,OSIOC_MAXDELAY,&ts);
  if(ret < 0) {
    
  }
  close(fd);
}

int main(int argc, FAR char *argv[])
{
  struct oneshot_state_s oneshot_state =
  {
    .devpath = ONESHOT_DEFAULT_DEVPATH,
    .oneshot.ts.tv_sec = DEFAULT_TIME_OUT,
    .oneshot.ts.tv_nsec = 0
  };

  const struct CMUnitTest tests[] =
  {
    cmocka_unit_test_prestate(test_case_oneshot, &oneshot_state)
  };

  parse_commandline(&oneshot_state, argc, argv);

  return cmocka_run_group_tests(tests, NULL, NULL);
}
```
