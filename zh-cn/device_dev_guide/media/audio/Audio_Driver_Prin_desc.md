# Audio Driver 原理说明

[ [English](../../../../en/device_dev_guide/media/audio/Audio_Driver_Prin_desc.md) | 简体中文 \]

## 一、概述

openvela 提供了一种抽象的音频设备节点接口，用于为应用程序实现音频播放和录音功能。应用程序可以通过标准的 `open`、`close` 和 `ioctl` 系统调用，与音频驱动程序进行交互。

openvela 的音频驱动程序采用分层架构设计，分为以下两部分：

1. 上半部分驱动程序（Upper Half Driver）： 定义统一的外部接口和通用代码，同时提供部分 `ioctl` 命令的默认实现。
2. 下半部分驱动程序（Lower Half Driver）： 负责实现与具体硬件设备的交互逻辑（如音频硬件控制）。

通过这种分层设计，openvela 实现了音频功能的模块化，并与硬件解耦，提供了更高的灵活性和扩展性，降低了开发者的维护难度和硬件适配的复杂性。

## 二、软件层次

openvela 提供了三个内置工具：`nxplayer`、`nxrecorder` 和 `nxlooper`，用于帮助开发者验证 openvela 的音频驱动程序。这些工具为开发者提供了便捷的方式来测试和验证音频播放、录音等多媒体功能。

音频驱动程序通过调用音频接口，为应用开发者提供多媒体音频能力。以下是 openvela 音频驱动程序的层次结构：

- 音频应用（audio Applications）：用于多媒体功能的开发，例如音乐播放器。
- Vela 音频驱动（Audio Driver）：为上层应用提供音频接口，并封装硬件相关的细节。

![img](./figures/004.svg)

## 三、代码目录

openvela 的音频驱动程序代码位于 `nuttx/audio` 目录下，代码结构如下：

```Bash
user@user:~/vela/nuttx/audio$ tree
├── audio.c
├── audio_comp.c
├── Kconfig
├── Make.dep
├── Makefile
└── README.txt

0 directories, 10 files
```

该目录包含音频驱动的核心实现文件、配置文件（`Kconfig`）、构建文件（`Makefile` 和 `Make.dep`），以及相关的说明文档（`README.txt`）。开发者可以根据需求在此基础上扩展或修改音频驱动功能。

## 四、对外接口

openvela 音频驱动程序提供了一组标准化的接口，供应用程序调用以实现音频功能。这些接口通过 `ioctl` 系统调用实现，支持多种音频操作。以下是 openvela 音频驱动程序的接口定义：

```C
#define AUDIOIOC_GETCAPS            _AUDIOIOC(1)
#define AUDIOIOC_RESERVE            _AUDIOIOC(2)
#define AUDIOIOC_RELEASE            _AUDIOIOC(3)
#define AUDIOIOC_CONFIGURE          _AUDIOIOC(4)
#define AUDIOIOC_SHUTDOWN           _AUDIOIOC(5)
#define AUDIOIOC_START              _AUDIOIOC(6)
#define AUDIOIOC_STOP               _AUDIOIOC(7)
#define AUDIOIOC_PAUSE              _AUDIOIOC(8)
#define AUDIOIOC_RESUME             _AUDIOIOC(9)
#define AUDIOIOC_GETBUFFERINFO      _AUDIOIOC(10)
#define AUDIOIOC_ALLOCBUFFER        _AUDIOIOC(11)
#define AUDIOIOC_FREEBUFFER         _AUDIOIOC(12)
#define AUDIOIOC_ENQUEUEBUFFER      _AUDIOIOC(13)
#define AUDIOIOC_REGISTERMQ         _AUDIOIOC(14)
#define AUDIOIOC_UNREGISTERMQ       _AUDIOIOC(15)
#define AUDIOIOC_HWRESET            _AUDIOIOC(16)
#define AUDIOIOC_SETBUFFERINFO      _AUDIOIOC(17)
#define AUDIOIOC_SETPARAMTER        _AUDIOIOC(18)
#define AUDIOIOC_GETLATENCY         _AUDIOIOC(19)
#define AUDIOIOC_FLUSH              _AUDIOIOC(20)
```

这些接口涵盖了音频设备的配置、启动、暂停、停止、缓冲区管理等功能，能够满足多种音频应用场景的需求。

### Demo Code

以下是一个使用 openvela 音频驱动程序接口的示例代码：

```C
// 1. 打开节点，RESERVER, 注册消息回调MQ
player->fd = open("/dev/audio/pcm0p", O_RDWR | O_CLOEXEC);
ioctl(player->fd, AUDIOIOC_RESERVE, &compress->session);
ioctl(player->fd, AUDIOIOC_REGISTERMQ, player->mq);

// 2. 配置格式和buffer info，分配buffer info
ioctl(player->fd, AUDIOIOC_GETCAPS, (unsigned long)&caps);
ioctl(player->fd, AUDIOIOC_CONFIGURE, (unsigned long)&cap_desc);
ioctl(player->fd, AUDIOIOC_SETBUFFERINFO, &buf_info);
ioctl(player->fd, AUDIOIOC_GETBUFFERINFO, &buf_info);
ioctl(player->fd, AUDIOIOC_ALLOCBUFFER, &buf_desc);

// 3. start播放，循环enqueue buffer给driver播放，从MQ中回收播完的buffer
ioctl(player->fd, AUDIOIOC_START, 0)
ioctl(player->fd, AUDIOIOC_ENQUEUEBUFFER, &desc);
mq_receive(player->mq) //收AUDIO_MSG_DEQUEUE上来的buffer

// 4. 播放控制pause/resume
ioctl(player->fd, AUDIOIOC_PAUSE, 0)
ioctl(player->fd, AUDIOIOC_RESUME, 0)

// 5. 结束播放，关闭节点
ioctl(player->fd, AUDIOIOC_STOP, 0)
ioctl(player->fd, AUDIOIOC_FREEBUFFER, &buf_desc) //所有的buffer全都要还回来
ioctl(player->fd, AUDIOIOC_UNREGISTERMQ, 0);
ioctl(player->fd, AUDIOIOC_RELEASE, 0);
close(player->fd);
```

以下示例展示了如何使用 openvela 音频驱动程序的接口实现音频设备的基本操作：

1. 打开音频设备：通过 `open` 函数打开音频设备节点（如 `/dev/audio/pcm0c`）。
2. 配置音频设备：通过 `ioctl` 调用 `AUDIOIOC_CONFIGURE` 接口，传入设备配置参数。
3. 关闭音频设备：通过 `close` 函数关闭设备文件描述符。

## 五、音频设备节点

在 openvela 的 `sim` 平台中，系统启动后 `/dev/audio/` 目录下会包含 4 个音频设备节点，如下所示：

```Bash
ap> ls /dev/audio
 pcm0c
 pcm0p
 pcm1c
 pcm1p
```

### 1、设备节点注册流程

设备节点的注册是音频上半部分驱动程序（Upper Half Driver）与音频下半部分驱动程序（Lower Half Driver）建立联系的过程。以下是注册流程的关键步骤。

#### 1.1 `audio_register`

```Bash
int audio_register(FAR const char *name, FAR struct audio_lowerhalf_s *dev)
```

- 参数说明：

    - `name`：设备节点名称，例如 `"pcm0p"`。
    - `dev`：指向音频下半部分驱动程序结构体的指针。

- 返回值：

    - 返回 `0` 表示注册成功。
    - 返回负值表示失败。

##### 数据结构

1. `audio_upperhalf_s`

    `audio_upperhalf_s` 是音频上半部分驱动程序的数据结构，主要用于维护设备的状态信息。

    ```C
    struct audio_upperhalf_s
    {
        uint8_t           crefs;            /* The number of times the device has been opened */
        volatile bool     started;          /* True: playback is active */
        mutex_t           lock;             /* Supports mutual exclusion */
        FAR struct audio_lowerhalf_s *dev;  /* lower-half state */
        struct file      *usermq;           /* User mode app's message queue */
    };
    ```

2. `audio_lowerhalf_s`

    `audio_lowerhalf_s` 是音频下半部分驱动程序的数据结构，主要用于硬件适配。

    ```C
    struct audio_lowerhalf_s
    {
    /* The first field of this state structure must be a pointer to the Audio
        * callback structure:
        */
    
    FAR const struct audio_ops_s *ops;  
    
    /* The bind data to the upper-half driver used for callbacks of dequeuing
        * buffer, reporting asynchronous event, reporting errors, etc.
        */
    
    FAR audio_callback_t  upper;
    
    /* The private opaque pointer to be passed to upper-layer during
        * callbacks  
        */
        
    FAR void *priv;
        
    /* The custom Audio device state structure may include additional fields
        * after the pointer to the Audio callback structure.
        */
    }; 
    ```

##### 函数实现

`audio_register` 的实现如下，代码中增加了单行注释以说明关键变量的赋值过程。该函数将 `audio_lowerhalf_s` 的重要变量进行赋值，并完成音频设备的注册。

需要注意的是，音频下半部分驱动需要芯片厂商根据具体硬件自行适配，因此具有平台差异性。

```C
int audio_register(FAR const char *name, FAR struct audio_lowerhalf_s *dev)
{
 upper = (FAR struct audio_upperhalf_s *)kmm_zalloc(
                                           sizeof(struct audio_upperhalf_s));
 /* Initialize the Audio device structure
  * (it was already zeroed by kmm_zalloc())
  */

  nxmutex_init(&upper->lock);
  
  /* assign dev to upper->dev */
  upper->dev = dev;                  
  
  /* Now build the path for registration */
  ...
  
  /* set callback to lower half, use msg callback  */
  dev->upper = audio_callback;
  
  /* set upper to priv of lower half. */
  dev->priv = upper;
  
  return register_driver(path, &g_audioops, 0666, upper);
}
```

`g_audioops` 是音频设备的操作接口集合，用于定义音频设备的基本操作，例如打开、关闭、读写等。以下是 `g_audioops` 的定义：

```C
static const struct file_operations g_audioops =
{
  audio_open,  /* open */
  audio_close, /* close */
  audio_read,  /* read */
  audio_write, /* write */
  NULL,        /* seek */
  audio_ioctl, /* ioctl */
};
```

通过 `g_audioops`，音频设备的基本操作被抽象为统一的接口，方便上层应用程序调用。

##### 调用流程

以下 UML 图展示了 `nxplayer` 调用音频设备的完整流程，从 `nxplayer` 到音频下半部分驱动的函数调用路径：

![img](./figures/005.svg)

##### 调用栈

以下是通过 GDB 调试获取的函数调用栈信息，展示了 `audio_open`、`audio_ioctl` 和 `audio_close` 的调用路径。

1. 调用 `audio_open`。

    ```Bash
    (gdb) bt
    #0  audio_open (filep=0xf400bad0) at audio.c:139
    #1  0x597a9c8e in file_vopen (filep=0xee9eca50, path=0xee9ecca0 "/dev/audio/pcm0p", oflags=3, umask=0, ap=0xee9ecb9c "1\277\232Y\n\327?f\001") at vfs/fs_open.c:194
    #2  0x597aa078 in nx_vopen (path=0xee9ecca0 "/dev/audio/pcm0p", oflags=3, ap=0xee9ecb98 "5\033`Y1\277\232Y\n\327?f\001") at vfs/fs_open.c:253
    #3  0x597aa9e7 in open (path=0xee9ecca0 "/dev/audio/pcm0p", oflags=3) at vfs/fs_open.c:411
    #4  0x599ac02d in nxplayer_setdevice (pplayer=0xf3808d40, pdevice=0xee9ecca0 "/dev/audio/pcm0p") at nxplayer.c:1663
    #5  0x59954325 in nxplayer_cmd_device (pplayer=0xf3808d40, parg=0xee9eceb7 "pcm0p") at nxplayer_main.c:612
    #6  0x599557d0 in nxplayer_main (argc=1, argv=0xee7dd830) at nxplayer_main.c:811
    #7  0x596003b1 in nxtask_startup (entrypt=0x59954d90 <nxplayer_main>, argc=1, argv=0xee7dd830) at sched/task_startup.c:70
    #8  0x5955347f in nxtask_start () at task/task_start.c:134
    #9  0x00000000 in ?? ()
    ```

2. 调用 `audio_ioctl`。

    ```Bash
    (gdb) bt
    #0  audio_ioctl (filep=0xf440c900, cmd=6529667, arg=1715459884) at audio.c:349
    #1  0x597a6d2b in file_vioctl (filep=0xf440c7fc, req=4097, ap=<optimized out>) at vfs/fs_ioctl.c:67
    #2  0x597a78df in ioctl (fd=3, req=4097) at vfs/fs_ioctl.c:212
    #3  0x599ac104 in nxplayer_setdevice (pplayer=0xf3808d40, pdevice=0xee9ecca0 "/dev/audio/pcm0p") at nxplayer.c:1676
    #4  0x59954325 in nxplayer_cmd_device (pplayer=0xf3808d40, parg=0xee9eceb7 "pcm0p") at nxplayer_main.c:612
    #5  0x599557d0 in nxplayer_main (argc=1, argv=0xee7dd830) at nxplayer_main.c:811
    #6  0x596003b1 in nxtask_startup (entrypt=0x59954d90 <nxplayer_main>, argc=1, argv=0xee7dd830) at sched/task_startup.c:70
    #7  0x5955347f in nxtask_start () at task/task_start.c:134
    #8  0x00000000 in ?? ()
    ```

3. 调用 `audio_close`。

    ```Bash
    (gdb) bt
    #0  audio_close (filep=0x5957f73e <sem_post+18>) at audio.c:190
    #1  0x597a472d in file_close (filep=0xee9ecac0) at vfs/fs_close.c:74
    #2  0x597a0baa in nx_close (fd=3) at inode/fs_files.c:592
    #3  0x597a0c62 in close (fd=3) at inode/fs_files.c:626
    #4  0x599ac162 in nxplayer_setdevice (pplayer=0xf3808d40, pdevice=0xee9ecca0 "/dev/audio/pcm0p") at nxplayer.c:1686
    #5  0x59954325 in nxplayer_cmd_device (pplayer=0xf3808d40, parg=0xee9eceb7 "pcm0p") at nxplayer_main.c:612
    #6  0x599557d0 in nxplayer_main (argc=1, argv=0xee7dd830) at nxplayer_main.c:811
    #7  0x596003b1 in nxtask_startup (entrypt=0x59954d90 <nxplayer_main>, argc=1, argv=0xee7dd830) at sched/task_startup.c:70
    #8  0x5955347f in nxtask_start () at task/task_start.c:134
    #9  0x00000000 in ?? ()
    ```

##### 示例

在 `Simulator` 平台中，音频下半部分驱动程序使用主机的 ALSA（Advanced Linux Sound Architecture）能力构建。以下是设备节点注册的示例代码：

```C
 audio_register("pcm0p", sim_audio_initialize(true, false));
```

- `pcm0p` 是注册的设备节点名称。
- `sim_audio_initialize` 是用于初始化音频下半部分驱动的函数。

该代码位于 `arch/sim/src/sim/posix/sim_alsa.c` 文件中。在 `Simulator` 平台上，`pcm0p` 是由单一的 下半部分驱动程序注册的。

#### 1.2 `audio_comp_initialize`

`audio_comp_initialize` 是一个用于注册复合音频设备的函数，其功能类似于 Linux ASoC 框架中的 `platform/dai/codec` 驱动组合，但在 openvela 中，所有的音频驱动都被抽象为 `audio_lowerhalf`，不再区分 `platform`、`dai` 和 `codec`。

##### 函数定义

```C
FAR struct audio_lowerhalf_s *audio_comp_initialize(FAR const char *name, ...);
```

##### 功能说明

与 `audio_register` 不同，`audio_comp_initialize` 支持不定长参数，允许多个 `audio_lowerhalf` 驱动共同抽象为一个 PCM 设备。以下是两者的主要区别：

- `audio_register`：参数为单一设备，适用于单个音频设备的注册。
- `audio_comp_initialize`：参数为不定长，允许多个 `audio_lowerhalf` 驱动组合注册为一个音频设备。

##### 适用场景

这种设计的灵活性体现在以下场景：

- 某些平台的 `i2s lowerhalf driver` 是固定的，但可以外接不同的 `PA`（功率放大器）。
- `i2s lowerhalf driver` 由芯片平台提供，基本可以固化，而 `PA lowerhalf driver` 则根据项目需求进行适配。
- 通过 `audio_comp_initialize`，可以将 `i2s lowerhalf driver` 和 `PA lowerhalf driver` 组合为一个音频设备，从而提高适配灵活性。

##### 数据结构

`audio_comp_priv_s` 是一个描述复合音频设备内部状态的数据结构。其定义如下：

```C
/* This structure describes the internal state of the audio composite */

struct audio_comp_priv_s
{
  /* This is is our appearance to the outside world. This *MUST* be the
   * first element of the structure so that we can freely cast between
   * types struct audio_lowerhalf and struct audio_comp_dev_s.
   */

  struct audio_lowerhalf_s export;

  /* This is the contained, low-level audio device array and count. */

  FAR struct audio_lowerhalf_s **lower;
  int count;
};
```

- `export`：是一个 `audio_lowerhalf_s` 类型的字段，作为多个 `audio_lowerhalf` 的出口，与音频上半部分驱动对接。
- `lower`：指向包含的低级音频设备数组。
- `count`：表示包含的低级音频设备数量。

##### 函数实现

以下是 `audio_comp_initialize` 的实现代码，代码中增加了注释以说明关键步骤：

```C
FAR struct audio_lowerhalf_s *audio_comp_initialize(FAR const char *name,
                                                    ...)
{
    FAR struct audio_comp_priv_s *priv;
    
    priv = kmm_zalloc(sizeof(struct audio_comp_priv_s));
  
    priv->export.ops = &g_audio_comp_ops;
    
    /* Get how many lowerhalf drivers */
    va_start(ap, name);
    while (va_arg(ap, FAR struct audio_lowerhalf_s *))
        {
          priv->count++;
        }
    
    va_end(ap);
    
    /* alloc space to store lowerhalf drivers */
    priv->lower = kmm_calloc(priv->count,
                               sizeof(FAR struct audio_lowerhalf_s *));
    if (priv->lower == NULL)
        {
          goto free_priv;
        }
    
    /* Initialized for each lower half driver */
    va_start(ap, name);
    for (i = 0; i < priv->count; i++)
        {
          FAR struct audio_lowerhalf_s *tmp;
    
          tmp = va_arg(ap, FAR struct audio_lowerhalf_s *);
          tmp->upper = audio_comp_callback;
          tmp->priv = priv;
    
          priv->lower[i] = tmp;
        }
    
    va_end(ap);
    
    ret = audio_register(name, &priv->export);
    
    return &priv->export;
}
```

流程说明：

1. 分配私有数据结构：通过 `kmm_zalloc` 分配 `audio_comp_priv_s` 结构体，并初始化其操作接口。
2. 统计 `lowerhalf` 驱动数量：通过 `va_arg` 遍历不定长参数，统计包含的 `audio_lowerhalf` 驱动数量。
3. 分配存储空间：为 `audio_lowerhalf` 驱动分配存储空间。
4. 初始化 `lowerhalf` 驱动：为每个 `audio_lowerhalf` 驱动设置回调函数和私有数据。
5. 注册设备节点：调用 `audio_register` 函数，将复合音频设备注册为一个设备节点。

##### 新增接口

以下是 `audio_comp_initialize` 使用的一些新增接口及其功能说明。

###### `g_audio_comp_ops`

`g_audio_comp_ops` 是复合音频设备的操作接口集合，定义了复合音频设备对外提供的所有功能。这些功能通过音频上半部分驱动传递到每个音频下半部分驱动。定义如下：

```C
static const struct audio_ops_s g_audio_comp_ops =
{
  audio_comp_getcaps,       /* getcaps        */
  audio_comp_configure,     /* configure      */
  audio_comp_shutdown,      /* shutdown       */
  audio_comp_start,         /* start          */
#ifndef CONFIG_AUDIO_EXCLUDE_STOP
  audio_comp_stop,          /* stop           */
#endif
#ifndef CONFIG_AUDIO_EXCLUDE_PAUSE_RESUME
  audio_comp_pause,         /* pause          */
  audio_comp_resume,        /* resume         */
#endif
  audio_comp_allocbuffer,   /* allocbuffer    */
  audio_comp_freebuffer,    /* freebuffer     */
  audio_comp_enqueuebuffer, /* enqueue_buffer */
  audio_comp_cancelbuffer,  /* cancel_buffer  */
  audio_comp_ioctl,         /* ioctl          */
  audio_comp_read,          /* read           */
  audio_comp_write,         /* write          */
  audio_comp_reserve,       /* reserve        */
  audio_comp_release        /* release        */
};
```

核心作用：

- 为复合音频设备提供统一的操作接口，供音频上半部分驱动调用。
- 实现复合音频设备对外功能的抽象，支持如暂停、启动、缓冲区管理等功能。

###### `audio_comp_callback`

`audio_comp_callback` 是复合音频设备的回调函数，用于处理每个音频下半部分设备的事件，并将其交给音频上半部分驱动处理。

以下是 `audio_comp_callback` 的实现：

```C
#ifdef CONFIG_AUDIO_MULTI_SESSION
static void audio_comp_callback(FAR void *arg, uint16_t reason,
                                FAR struct ap_buffer_s *apb, uint16_t status,
                                FAR void *session)
#else
static void audio_comp_callback(FAR void *arg, uint16_t reason,
                                FAR struct ap_buffer_s *apb, uint16_t status)
#endif
{
  FAR struct audio_comp_priv_s *priv = arg;

#ifdef CONFIG_AUDIO_MULTI_SESSION
  priv->export.upper(priv->export.priv, reason, apb, status, session);
#else
  priv->export.upper(priv->export.priv, reason, apb, status);
#endif
}
```

- 参数说明：

    - `arg`：指向复合音频设备的私有数据结构 `audio_comp_priv_s`。
    - `reason`：回调的原因，例如缓冲区完成、错误等。
    - `apb`：音频缓冲区。
    - `status`：回调状态。
    - `session`（可选）：多会话支持时的会话信息。

##### 调用流程

以下是复合音频设备的函数调用流程：

- `open` 和 `close`：与普通音频设备一致，无变化。

- `ioctl` 调用链：
  
    `ioctl` -> `file_vioctl` -> `audio_ioctl` -> `audio_comp_configure`，在 `audio_comp_configure` 函数中，每个 `audio_lowerhalf` 的 `configure` 接口都将被依次调用，完成复合设备的配置。

    ```C
    static int audio_comp_configure(FAR struct audio_lowerhalf_s *dev,
                                    FAR const struct audio_caps_s *caps)
    {
      for (i = 0; i < priv->count; i++)
        {
          if (lower[i]->ops->configure)
            {
              /* Forward ioctl to lowerhalf driver*/
    #ifdef CONFIG_AUDIO_MULTI_SESSION
              int tmp = lower[i]->ops->configure(lower[i], sess[i], caps);
    #else
              int tmp = lower[i]->ops->configure(lower[i], caps);
    #endif
            }
        }

      return ret;
    }
    ```

- 作用：`audio_comp_configure` 将配置命令 (`configure`) 转发到组成复合设备的每个 `audio_lowerhalf` 驱动，实现复合设备的配置。

### 2、何时注册设备节点

音频设备节点的注册通常发生在系统初始化阶段。本节将通过 GDB 调试调用栈（Call Stack）展示音频设备节点注册的调用路径。

以下是调试过程中捕获的调用栈信息：

```Bash
(gdb) bt
#0  audio_register (name=0xf46007b0 "", dev=0x4c) at audio.c:919
#1  0x596369f2 in up_initialize () at sim/sim_initialize.c:295
#2  0x5954c5a8 in nx_start () at init/nx_start.c:610
#3  0x594db783 in main (argc=1, argv=0xffffd604, envp=0xffffd60c) at sim/sim_head.c:130
```

### 3、总结

本章内容总结如下：

1. 音频驱动程序的注册方法：介绍了 openvela 中注册音频驱动程序的两种方法，包括 `audio_register` 和其衍生的 `audio_comp_initialize` 函数，后者支持组合多个音频下半部分驱动。

2. 函数调用流程：描述了从应用程序（如 `nxplayer`）到音频下半部分驱动的完整调用路径，即 `apps (nxplayer) -> vfs -> audio upperhalf driver -> audio lowerhalf driver`。

## 六、音频下半部分驱动介绍

在上一章节中，我们介绍了从应用程序（如 `nxplayer`）到音频驱动的完整调用流程，即 `apps (nxplayer) -> vfs -> audio upperhalf driver -> audio lowerhalf driver`。前三部分的实现与具体芯片或产品无关，但 `audio lowerhalf driver` 是芯片特有的，甚至在同一芯片的不同产品中也可能存在差异。

以下是一些常见的差异场景：

- 能力差异：例如，不同产品可能支持不同的采样率或声道数。
- 数据处理方式差异：

    - 某些平台具有通用 DMA 模块，音频驱动可能需要预留某个 DMA 通道。
    - 其他平台的 DMA 功能可能是音频内部的辅助功能。

- 外置 PA 支持：

    - 某些平台支持通过 `i2s lowerhalf driver` 和 `pa lowerhalf driver` 的组合节点注册音频驱动。
    - 在具体项目中，如果需要更新 PA，只需重新实现 `pa lowerhalf driver` 即可满足需求。

综上所述，由于平台的特异性，音频下半部分驱动（Audio Lowerhalf Driver）通常由芯片厂商实现。

### 1、`audio_lowerhalf_s`

`audio_lowerhalf_s` 是音频下半部分驱动（Lower Half Driver）的核心数据结构，用于实现音频硬件的适配和上下层之间的连接。定义如下：

```C
struct audio_lowerhalf_s
{
  /* The first field of this state structure must be a pointer to the Audio
   * callback structure:
   */

  FAR const struct audio_ops_s *ops;  

  /* The bind data to the upper-half driver used for callbacks of dequeuing
   * buffer, reporting asynchronous event, reporting errors, etc.
   */

  FAR audio_callback_t upper;

  /* The private opaque pointer to be passed to upper-layer during
   * callbacks
   */

  FAR void *priv;

  /* The custom Audio device state structure may include additional fields
   * after the pointer to the Audio callback structure.
   */
}; 
```

- `ops`：指向 `audio_ops_s` 的指针，定义了音频下半部分驱动需要实现的所有接口，如设备控制、播放、录音、缓冲区管理等。音频下半部分驱动必须根据硬件特性重新实现这些接口。
- `upper`：上半部分驱动的回调函数，用于处理缓冲区管理、事件通知等。
- `priv`：私有数据指针，用于在回调中传递上下文信息。

### 2、`audio_ops_s`

`audio_ops_s` 定义了音频驱动的操作接口，位于 `include/nuttx/audio/audio.h`，包含控制接口和数据接口。它实现了应用程序对音频驱动的控制以及数据的流转。以下是 `audio_ops_s` 的主要接口及其功能：

#### 控制接口

| 接口名称              | 功能描述                               |
| :-------------------- | :------------------------------------- |
| AUDIOIOC_GETCAPS      | 获取设备能力。                         |
| AUDIOIOC_RESERVE      | 保留音频设备的缓冲区。                 |
| AUDIOIOC_RELEASE      | 释放设备。                             |
| AUDIOIOC_CONFIGURE    | 设置设备参数。                         |
| AUDIOIOC_SHUTDOWN     | 关闭设备。                             |
| AUDIOIOC_START        | 开始播放或录音。                       |
| AUDIOIOC_STOP         | 停止播放或录音。                       |
| AUDIOIOC_PAUSE        | 暂停播放或录音。                       |
| AUDIOIOC_RESUME       | 恢复播放或录音。                       |
| AUDIOIOC_REGISTERMQ   | 注册消息队列，用于驱动与应用程序通信。 |
| AUDIOIOC_UNREGISTERMQ | 注销消息队列。                         |
| AUDIOIOC_HWRESET      | 执行硬件重置。                         |
| AUDIOIOC_SETPARAMTER  | 以 `key=value` 格式设置参数。          |
| AUDIOIOC_FLUSH        | 清除缓冲区数据。                       |

#### 数据接口

| 接口名称               | 功能描述                             |
| :--------------------- | :----------------------------------- |
| AUDIOIOC_GETBUFFERINFO | 获取缓冲区信息。                     |
| AUDIOIOC_ALLOCBUFFER   | 分配缓冲区。                         |
| AUDIOIOC_FREEBUFFER    | 释放缓冲区。                         |
| AUDIOIOC_ENQUEUEBUFFER | 应用程序通过该接口将数据传递给驱动。 |
| AUDIOIOC_SETBUFFERINFO | 设置缓冲区信息。                     |
| AUDIOIOC_GETLATENCY    | 获取驱动播放延迟。                   |

#### 单一设备与组合设备的实现

- 单一设备：对于单一音频设备，`audio_ops_s` 的控制接口和数据接口需要完整实现，以提供完整的音频功能。

- 组合设备：对于由多个 `audio_lowerhalf_s` 驱动组合而成的设备：

    - 其中一个较复杂的设备需要实现完整的控制接口和数据接口。
    - 其余较简单的设备只需实现部分接口即可。

## 七、音频下半部分驱动示例

### 1、`audio_dma`

`audio_dma` 是 openvela 提供的一个内置音频下半部分驱动，代码位置为 `drivers/audio/audio_dma.c`。以下是其实现的详细说明。

#### 1.1 数据结构

`audio_dma` 通过重写 `audio_ops_s` 中的接口实现音频驱动的功能。以下是 `audio_dma` 的操作接口定义：

```C
static const struct audio_ops_s g_audio_dma_ops =
{
  .getcaps = audio_dma_getcaps,
  .configure = audio_dma_configure,
  .shutdown = audio_dma_shutdown,
  .start = audio_dma_start,
#ifndef CONFIG_AUDIO_EXCLUDE_STOP
  .stop = audio_dma_stop,
#endif
#ifndef CONFIG_AUDIO_EXCLUDE_PAUSE_RESUME
  .pause = audio_dma_pause,
  .resume = audio_dma_resume,
#endif
  .allocbuffer = audio_dma_allocbuffer,
  .freebuffer = audio_dma_freebuffer,
  .enqueuebuffer = audio_dma_enqueuebuffer,
  .ioctl = audio_dma_ioctl,
  .reserve = audio_dma_reserve,
  .release = audio_dma_release,
};
```

- 控制接口：如 `getcaps`、`configure`、`start`、`stop` 等，用于控制音频设备。
- 数据接口：如 `allocbuffer`、`freebuffer`、`enqueuebuffer` 等，用于管理音频数据的流转。

#### 1.2 控制接口

`audio_dma` 的控制接口与硬件密切相关，最终调用底层 DMA 模块的接口（如 `DMA_START_CYCLIC`）。以下是部分控制接口的说明：

- `getcaps`：获取设备能力。
- `configure`：配置设备参数。
- `start/stop`：启动或停止音频设备。
- `pause/resume`：暂停或恢复音频设备。
- `ioctl`：支持多种控制命令，例如：

    - `AUDIOIOC_SETPARAMTER`：通过 `key=value` 格式设置参数，例如 `set_scenario=phone`。

以下是音频设备配置接口 `audio_dma_configure` 的实现代码：

```C
static int audio_dma_configure(struct audio_lowerhalf_s *dev,
                               const struct audio_caps_s *caps)
{
  struct audio_dma_s *audio_dma = (struct audio_dma_s *)dev;
  struct dma_config_s cfg;
  int ret = -EINVAL;
  ...
  switch (caps->ac_type)
    {
      case AUDIO_TYPE_OUTPUT:
        if (audio_dma->playback)
          {
            ....
            ret = DMA_CONFIG(audio_dma->chan, &cfg);
          }
        break;
        ...
}
```

`DMA_CONFIG` 宏定义如下：

```C
#define DMA_CONFIG(chan, cfg) (chan)->ops->config(chan, cfg)
```

#### 1.3 重要结构体介绍

音频驱动的数据交互主要依赖以下两个数据结构：

1. `ap_buffer_s` `ap_buffer_s` 是实际音频数据的载体，包含音频数据的存储位置及相关信息。 `ap_buffer_s` 关键字段说明如下：

    - `samp`：音频数据的实际存储位置。
    - `nmaxbytes`：缓冲区的最大容量。
    - `nbytes`：实际存储的音频数据大小。
    - `curbytes`：当前处理数据的偏移量，通常为 0。
    - `nsamples`：实际存储的音频样本数量。

2. `audio_buf_desc_s` `audio_buf_desc_s` 是 `ap_buffer_s` 的描述体，用于作为各种 `ioctl` 的参数。

以下是两个结构体的 UML 图：

![img](./figures/006.svg)

#### 1.4 接口说明

以下是 `audio_dma` 的主要接口及其功能：

1. `AUDIOIOC_GETBUFFERINFO`

    功能：应用程序获取缓冲区的大小和数量。

2. `AUDIOIOC_SETBUFFERINFO`

    功能：应用程序设置缓冲区的大小和数量。

3. `AUDIOIOC_ALLOCBUFFER`

    - 功能：分配音频缓冲区。
    - 说明：

        - openvela 的音频驱动与应用程序交互的内存由驱动层分配。
        - 默认的内存分配方法是 `apb_alloc`，但 `lowerhalf driver` 也可以自行实现。
        - 默认实现：`apb_alloc` 一次性分配了 `sizeof(ap_buffer_t) + desc.numbytes` 的大小，即 `ap_buffer_s` 和实际音频数据存储位置（`apb->samp`）是连续的。
        - `audio_dma_allocbuffer` 实现：分配连续地址，直接对应 DMA 的源地址或目标地址（`apb->samp`），然后再分配 `ap_buffer_s` 结构体。

    - 优化：

        - 使用 openvela 默认的 `apb_alloc` 和 `apb_free` 会导致一次数据拷贝。
        - `audio_dma` 的实现允许应用程序直接将数据写入 DMA 缓冲区，DMA 直接搬运数据，从而节省了一次拷贝操作。

4. `AUDIOIOC_FREEBUFFER`

    - 功能：释放音频缓冲区。

5. `AUDIOIOC_ENQUEUBUFFER`

    - 功能：应用程序通过 `enqueue ioctl` 将音频数据（播放链路）或空缓冲区（录音链路）传递给音频驱动。

    - 实现示例：

        ```C
          flags = enter_critical_section();
          dq_addlast(&apb->dq_entry, &audio_dma->pendq);  /* add to pendq */
          leave_critical_section(flags);
        ```

    - 处理机制：

        - 中断函数：例如 `audio_dma_callback`，在中断中触发 `DEQUEUE` 回调。
        - 高优先级工作线程：工作线程通常等待某个信号唤醒，例如 DMA 或 I2S（集成电路声音接口，Inter-IC Sound）完成回调后唤醒线程，线程消耗下一帧数据。

#### 1.5 `audio_dma` 的处理函数

##### audio_dma_enqueuebuffer

- 功能：将音频缓冲区添加到待处理队列。

- 实现代码：

    ```C
    static int audio_dma_enqueuebuffer(struct audio_lowerhalf_s *dev,
                                       struct ap_buffer_s*apb)
    {
      struct audio_dma_s *audio_dma = (struct audio_dma_s*)dev;
      irqstate_t flags;
      ...
      apb->flags |= AUDIO_APB_OUTPUT_ENQUEUED;

      flags = enter_critical_section();
      dq_addlast(&apb->dq_entry, &audio_dma->pendq);
      leave_critical_section(flags);
      ...
      return OK;
    }
    ```

##### audio_dma_callback

- 功能：DMA 中断处理函数，从待处理队列中取出缓冲区并触发 `DEQUEUE` 回调。

- 实现代码：

    ```C
    /*DMA interrupt handling function*/
    static void audio_dma_callback(struct dma_chan_s *chan,
                                   void*arg, ssize_t len)
    {
      struct audio_dma_s *audio_dma = (struct audio_dma_s*)arg;
      struct ap_buffer_s *apb;
      bool final = false;

      apb = (struct ap_buffer_s *)dq_remfirst(&audio_dma->pendq);
      ...
      /* DEQUEUE callback */
    #ifdef CONFIG_AUDIO_MULTI_SESSION
        audio_dma->dev.upper(audio_dma->dev.priv, AUDIO_CALLBACK_DEQUEUE,
                             apb, OK, NULL);
    #else
        audio_dma->dev.upper(audio_dma->dev.priv, AUDIO_CALLBACK_DEQUEUE,
                             apb, OK);
    #endif
      ...
    }
    ```

#### 总结

`audio_dma` 是对通用 DMA 的封装，完整实现了音频驱动的数据接口，并将控制接口下沉到 DMA 模块（`dma_ops_s`）中。其特点包括：

1. 高效的数据传输：通过直接分配 DMA 缓冲区，避免了额外的数据拷贝。
2. 灵活的接口实现：支持多种控制和数据接口，满足不同应用场景的需求。
3. 模块化设计：通过中断或工作线程处理音频数据，适配多种硬件平台。

通过 `audio_dma` 的实现，开发者可以参考其设计模式，快速实现自定义的音频下半部分驱动。

### 2、`audio_i2s`

`audio_i2s` 是 openvela 提供的一个内置音频下半部分驱动，主要用于音频数据的传输和控制。以下是关于 `audio_i2s` 的详细说明。

#### 2.1 数据结构

`audio_i2s` 通过重写 `audio_ops_s` 中的接口实现音频驱动的功能。以下是 `audio_i2s` 的接口定义：

```C
static const struct audio_ops_s g_audio_i2s_ops =
{
  audio_i2s_getcaps,       /* 能力获取        */
  audio_i2s_configure,     /* 参数配置      */
  audio_i2s_shutdown,      /* shutdown       */
  audio_i2s_start,         /* 开始          */
#ifndef CONFIG_AUDIO_EXCLUDE_STOP
  audio_i2s_stop,          /* 结束           */
#endif
#ifndef CONFIG_AUDIO_EXCLUDE_PAUSE_RESUME
  audio_i2s_pause,         /* pause          */
  audio_i2s_resume,        /* resume         */
#endif
  audio_i2s_allocbuffer,   /* 分配pcm播放内存    */
  audio_i2s_freebuffer,    /* 释放pcm内存     */
  audio_i2s_enqueuebuffer, /* apps<->driver pcm数据交互*/
  NULL,                    /* cancel_buffer  */
  audio_i2s_ioctl,         /* ioctl          */
  NULL,                    /* read           */
  NULL,                    /* write          */
  audio_i2s_reserve,       /* reserve        */
  audio_i2s_release        /* release        */
};
```

##### I2S 设备结构

系统定义了 I2S 设备的结构如下：

```C
struct i2s_dev_s
{
  FAR const struct i2s_ops_s *ops;
};
```

##### I2S 操作接口

`i2s_ops_s` 定义了需要实现的 I2S 操作接口，主要包括接收方法、发送方法、主时钟配置方法和通用控制接口：

```C
struct i2s_ops_s
{
  /* Receiver methods */
  CODE int      (*i2s_rxchannels)(FAR struct i2s_dev_s *dev,
                                  uint8_t channels);
  CODE uint32_t (*i2s_rxsamplerate)(FAR struct i2s_dev_s *dev,
                                    uint32_t rate);
  CODE uint32_t (*i2s_rxdatawidth)(FAR struct i2s_dev_s *dev,
                                   int bits);
  CODE int      (*i2s_receive)(FAR struct i2s_dev_s *dev,
                               FAR struct ap_buffer_s *apb,
                               i2s_callback_t callback,
                               FAR void *arg,
                               uint32_t timeout);

  /* Transmitter methods */

  CODE int      (*i2s_txchannels)(FAR struct i2s_dev_s *dev,
                                  uint8_t channels);
  CODE uint32_t (*i2s_txsamplerate)(FAR struct i2s_dev_s *dev,
                                    uint32_t rate);
  CODE uint32_t (*i2s_txdatawidth)(FAR struct i2s_dev_s *dev,
                                   int bits);
  CODE int      (*i2s_send)(FAR struct i2s_dev_s *dev,
                            FAR struct ap_buffer_s *apb,
                            i2s_callback_t callback,
                            FAR void *arg,
                            uint32_t timeout);

  /* Master Clock methods */

  CODE uint32_t (*i2s_mclkfrequency)(FAR struct i2s_dev_s *dev,
                                     uint32_t frequency);

  /* Ioctl */

  CODE int      (*i2s_ioctl)(FAR struct i2s_dev_s *dev,
                             int cmd, unsigned long arg);
};
```

`i2s_ops_s` 接口与硬件密切相关，需要硬件厂商实现。主要功能包括：

- 配置 I2S 数据传输格式（通道数、数据宽度、采样率）。
- PCM 数据的发送和接收。
- 主时钟（MCLK）的配置。
- 控制接口（`ioctl`）。

#### 2.2 代码位置

以下是 `audio_i2s` 的代码位置：

- 实现代码：`nuttx/drivers/audio/audio_i2s.c`
- 头文件：`nuttx/include/nuttx/audio/i2s.h`

#### 2.3 控制接口

`audio_i2s` 的控制接口会调用 `i2s_ops_s` 接口实现具体功能。通过以下宏定义，`audio_i2s` 调用 `i2s_ops_s` 的控制接口：

```C
#define I2S_IOCTL(d,c,a) \
  ((d)->ops->i2s_ioctl ? (d)->ops->i2s_ioctl(d,c,a) : -ENOTTY)
```

##### 控制接口

- 获取设备能力：`getcaps`

    ```C
    I2S_IOCTL(i2s, AUDIOIOC_GETCAPS, (unsigned long)caps);
    ```

- 启动设备：`start`

    ```C
    I2S_IOCTL(i2s, AUDIOIOC_START, audio_i2s->playback);
    ```

- 分配缓冲区：`allocbuffer`

    ```C
    I2S_IOCTL(i2s, AUDIOIOC_ALLOCBUFFER, (unsigned long)bufdesc);
    ```

##### 配置设备

以下是 `audio_i2s_configure` 的实现示例：

```C
static int audio_i2s_configure(FAR struct audio_lowerhalf_s *dev,
                               FAR const struct audio_caps_s *caps)
{
  FAR struct audio_i2s_s *audio_i2s = (struct audio_i2s_s *)dev;
  FAR struct i2s_dev_s *i2s;
  int samprate;
  int nchannels;
  int bpsamp;
  int ret = OK;
  ...
  switch (caps->ac_type)
    {
      case AUDIO_TYPE_OUTPUT:
      case AUDIO_TYPE_INPUT:

        /* Save the current stream configuration */

        samprate  = caps->ac_controls.hw[0] |
                    (caps->ac_controls.b[3] << 16);
        nchannels = caps->ac_channels;
        bpsamp    = caps->ac_controls.b[2];

        if (audio_i2s->playback)
          {
            /* i2s->ops->i2s_txchannels() */
            I2S_TXCHANNELS(i2s, nchannels);
            /* i2s->ops->i2s_txdatawidth */
            I2S_TXDATAWIDTH(i2s, bpsamp);
            /* i2s->ops->i2s_txsamplerate() */
            I2S_TXSAMPLERATE(i2s, samprate);
          }
        else
          {
            /* i2s->ops->i2s_rxchannels() */
            I2S_RXCHANNELS(i2s, nchannels);
            /* i2s->ops->i2s_rxdatawidth */
            I2S_RXDATAWIDTH(i2s, bpsamp);
            /* i2s->ops->i2s_rxsamplerate() */
            I2S_RXSAMPLERATE(i2s, samprate);
          }
        break;
        ...
        }
     ...
 }
```

#### 2.4 数据接口

1. AUDIOIOC_ALLOCBUFFER

    - 功能：调用 `i2s_ops_s->ioctl()` 分配用于 I2S PCM 传输的内存缓冲区。

2. AUDIOIOC_FREEBUFFER

    - 功能：释放之前分配的内存缓冲区。

3. AUDIOIOC_ENQUEUBUFFER

    - 功能：通过 `enqueue` ioctl 将音频数据（播放链路）或空白缓冲区（录音链路）传递给 `audio_i2s`。
    - 实现方式：

        - `audio_i2s` 调用 `i2s_ops_s->i2s_send()` 或 `i2s_ops_s->i2s_receive()` 完成 PCM 数据的传输。

以下是 `audio_i2s_enqueuebuffer` 的实现示例：

```C
static int audio_i2s_enqueuebuffer(FAR struct audio_lowerhalf_s *dev,
                                   FAR struct ap_buffer_s *apb)
{
  FAR struct audio_i2s_s *audio_i2s = (struct audio_i2s_s *)dev;
  FAR struct i2s_dev_s *i2s = audio_i2s->i2s;

  if (audio_i2s->playback)
    {
    /* #define I2S_SEND(d,b,c,a,t) \
  ((d)->ops->i2s_send ? (d)->ops->i2s_send(d,b,c,a,t) : -ENOTTY)
    */
      return I2S_SEND(i2s, apb, audio_i2s_callback, audio_i2s, 0);
    }
  else
    {
    /* #define I2S_RECEIVE(d,b,c,a,t) \
  ((d)->ops->i2s_receive ? (d)->ops->i2s_receive(d,b,c,a,t) : -ENOTTY)
    */
      return I2S_RECEIVE(i2s, apb, audio_i2s_callback, audio_i2s, 0);
    }
}
```

##### I2S PCM 传输完成的回调

`audio_i2s` 提供了一个回调函数，用于在 PCM 数据传输完成时进行处理。具体代码如下：

```C
static void audio_i2s_callback(struct i2s_dev_s *dev,
                               FAR struct ap_buffer_s *apb,
                               FAR void *arg, int result)
{
  FAR struct audio_i2s_s *audio_i2s = arg;
  bool final = false;
  ...
#ifdef CONFIG_AUDIO_MULTI_SESSION
  audio_i2s->dev.upper(audio_i2s->dev.priv, AUDIO_CALLBACK_DEQUEUE, apb,
                       OK, NULL);
#else
  audio_i2s->dev.upper(audio_i2s->dev.priv, AUDIO_CALLBACK_DEQUEUE, apb,
                       OK);
#endif
  ...
}
```

厂商在实现 `i2s_send()` 和 `i2s_receive()` 时，需要在 PCM 数据传输完成时调用该回调函数。

#### 2.5 总结

`audio_i2s` 是对通用 I2S 的一次封装，完整实现了音频驱动的数据接口。其特点包括：

1. 灵活的硬件适配：通过 `i2s_ops_s` 接口实现与硬件的深度集成。
2. 高效的数据传输：支持 PCM 数据的发送和接收。
3. 模块化设计：控制接口下沉到 I2S 模块，使得驱动设计更加清晰。

通过 `audio_i2s` 的实现，开发者可以快速适配不同厂商的 I2S 硬件，实现高效的音频数据传输。

### 3、`sim_alsa`

`sim_alsa` 是 openvela 提供的一个内置音频下半部分驱动，主要用于在模拟平台上桥接 openvela 音频驱动与主机 ALSA（Advanced Linux Sound Architecture）能力，满足模拟平台的音频播放和录音需求。

#### 3.1 代码位置

以下是 `sim_alsa` 的代码位置：

- `arch/sim/src/sim/posix/sim_alsa.c`
- `arch/sim/src/sim/posix/sim_offload.c`

#### 3.2 控制与数据接口

`sim_alsa` 通过实现 `audio_ops_s` 接口，完成音频设备的控制和数据交互。以下是接口定义：

```C
static const struct audio_ops_s g_sim_audio_ops =
{
  .getcaps       = sim_audio_getcaps,
  .configure     = sim_audio_configure,
  .shutdown      = sim_audio_shutdown,
  .start         = sim_audio_start,
#ifndef CONFIG_AUDIO_EXCLUDE_STOP
  .stop          = sim_audio_stop,
#endif
#ifndef CONFIG_AUDIO_EXCLUDE_PAUSE_RESUME
  .pause         = sim_audio_pause,
  .resume        = sim_audio_resume,
#endif
  .enqueuebuffer = sim_audio_enqueuebuffer,
  .ioctl         = sim_audio_ioctl,
  .reserve       = sim_audio_reserve,
  .release       = sim_audio_release,
};
```

#### 3.3 功能概述

`sim_alsa` 的主要功能是桥接 openvela 音频驱动与主机 ALSA 系统，支持以下场景：

- 音频播放：将模拟平台的音频数据传递到主机 ALSA 系统进行播放。
- 音频录制：从主机 ALSA 系统获取音频数据并传递到模拟平台。

#### 3.4 实现说明

`sim_alsa` 的接口实现与 `audio_dma` 类似，主要包括：

- 控制接口：如 `getcaps`、`configure`、`start`、`stop` 等，用于控制音频设备。
- 数据接口：如 `enqueuebuffer`，用于管理音频数据的流转。

开发者可以参考 `sim_alsa` 的代码实现，具体代码位于 `sim_alsa.c` 和 `sim_offload.c` 文件中。

## 八、Compress 能力

### 1、背景

类似于 ALSA 提供的 `compress` 节点，openvela 音频驱动也可以抽象出类似的 `compress` 节点，用于实现音频数据的解码和输出功能。

例如，在某些平台上，如果存在独立的 DSP（Digital Signal Processor）用于音频编解码，那么在适配 openvela 时，可以通过抽象 `compress` 节点来实现以下功能：

- 应用程序通过 `ENQUEUE` 接口将压缩音频数据传递给 `compress` 节点。
- 驱动内部通过 RPC 与 DSP 通信，完成音频数据的解码和播放。

### 2、概述

`compress` 能力是指 openvela 音频驱动支持播放和录制压缩音频数据的功能。通过 `compress` 节点，驱动可以处理压缩格式的音频数据，并在内部完成解码或编码操作。

### 3、示例

在 openvela 的模拟平台中，注册了 `pcm1p` 和 `pcm1c` 节点，用于模拟 `compress` 节点的功能。目前已实现以下功能：

- 支持的格式：MP3 格式的音频播放和录音。
- 实现方式：借助主机上的 `libmad` 和 `lame` 库，完成 MP3 格式的音频编解码。
