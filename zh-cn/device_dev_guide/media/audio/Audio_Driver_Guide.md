# Audio Driver 适配说明

\[ [English](../../../../en/device_dev_guide/media/audio/Audio_Driver_Guide.md) | 简体中文 \]

## 一、概述

本文档为嵌入式开发工程师提供在特定硬件平台上为 openvela 实时操作系统适配和实现音频 Lower-Half 驱动的详细步骤。遵循本指南，您可以将芯片的音频能力无缝集成到 openvela 的音频框架中。

## 二、适配前分析

在开始编码前，您必须完成以下分析，这是适配工作成功的基础。

### 1、分析硬件能力

您必须全面了解目标芯片的音频特性，包括：

- 音频接口（如 I2S, PCM）的控制逻辑和数据格式。
- DMA (Direct Memory Access) 控制器的使用方法，包括通道配置、传输模式和中断处理（若有）。
- 音频编解码器 (Codec) 或功率放大器 (PA) 的控制方式（通常通过 I2C 或 SPI）。
- 硬件支持的音频参数范围，如采样率、位深和声道数。

### 2、理解 openvela 音频框架

openvela 的音频框架为驱动开发提供了标准化的抽象层。您可以参考 [Audio Driver 原理说明](./Audio_Driver_Prin_desc.md)来深入了解，其核心优势包括：

- **完整的测试应用**：框架自带验证程序。驱动适配完成后，您无需编写额外测试代码即可验证核心功能。
- **统一的****驱动****接口**：openvela 定义了标准的 `audio_ops_s` 接口和 `ioctl` 命令。您必须遵循这些定义，在回调函数中实现与硬件对应的功能。
- **标准化****的调用流程**：框架处理了从应用层到底层驱动（Upper-Half）的完整调用逻辑。您只需聚焦于实现 Lower-Half 驱动，封装芯片相关的操作。
- **松耦合的组合节点**：您可以根据硬件架构。
    - 选择实现一个全新的、包含所有功能的音频设备节点。
    - 或仅替换现有组合节点中的某一个 Lower-Half 驱动（如独立的 PA 或 Codec 驱动）。
- **内置的可复用组件**：openvela 提供了通用的 Lower-Half 驱动（如 DMA 控制驱动）。开发前，请评估并复用这些组件以加速开发进程。
- **丰富的参考示例**：
    - `sim` 平台提供了 `sim_alsa.c` 作为基础参考。
    - 开源社区提供了多种芯片的实现，例如 [song-u1 的音频驱动](https://github.com/FishsemiCode/nuttx/tree/song-u1/drivers/audio)。

### 3、明确适配目标

根据项目需求，适配任务通常分为以下两类：

- **目标 1：从零实现完整的音频节点**
    - **场景**：为全新的平台或芯片适配音频功能。
    - **要求**：需要同时实现数据流接口（如 I2S/DMA）和控制流接口（如 I2C/SPI）。
- **目标 2：替换或添加独立的 Lower-Half** **驱动**
    - **场景**：在现有平台上更换部分硬件，如更新 PA。
    - **要求**：仅需实现该硬件的控制接口。

## 三、任务分解

本指南以更复杂的**目标 1** 为例进行任务分解。

1. **节点类型甄别**：判断您的音频链路是适合实现为**单一节点**（所有功能在一个驱动内）还是**组合节点**（如 I2S、DMA、Codec 分为不同驱动）。
2. **驱动复用评估**：如果选择**组合节点**，请评估是否可以复用 openvela 内置的 Lower-Half 驱动。

    - **可复用**：例如，您可以复用 `audio dma lowerhalf`，此时只需重新实现 `dma_ops_s` 操作集。
    - **不可复用**：与单一节点类似，您需要从头开始实现一个全新的 Audio Lower-Half 驱动。

## 四、Audio Lower-Half 驱动实现步骤

本章节详细介绍一个全新 Audio Lower-Half 驱动核心实现过程。

### 步骤 1：定义私有数据结构

定义一个驱动的私有数据结构，该结构体必须将 `struct audio_lowerhalf_s` 作为其第一个成员。

```C
/* 使用您的设备名替换 xx_audio_dev */
struct xx_audio_dev_s
{
  /* 此结构体必须作为第一个成员，以支持类型转换 */
  struct audio_lowerhalf_s dev;

  /* 在此添加驱动所需的私有变量 */
  // 例如: 硬件寄存器基地址、工作线程 ID、状态标志等
  // pthread_t threadid;
  // bool paused;
  // ...
};
```

### 步骤 2：实现 `initialize` 初始化函数

此函数负责分配私有结构体内存，并将其与 `audio_ops_s` 操作集关联。

```C
/* 使用您的设备名替换 xx_audio_dev */
struct audio_lowerhalf_s *xx_audio_initialize(...)
{
  struct xx_audio(dev)_s *priv;
  int ret;

  /* 分配并清零私有结构体内存 */
  priv = kmm_zalloc(sizeof(struct xx_audio(dev)_s));
  if (!priv)
    {
      return NULL;
    }
  
  /* 关键步骤：将 ops 指针指向已定义的全局 audio_ops_s 实例 */
  priv->dev.ops  = &g_xx_audio(dev)_ops;

  /* 其他初始化代码... */

  return &priv->dev;
}
```

### 步骤 3：注册设备节点

选择合适的位置比如 `board_early_initialize` 注册设备节点。

```C
audio_register("pcm0c", *xx_audio(dev)_initialize(true, 0));
audio_register("pcm0p", *xx_audio(dev)_initialize(false, 0));
```

### 步骤 4：定义 `audio_ops_s` 接口操作集

定义一个静态常量 `audio_ops_s` 结构体，并填充您将要实现的函数指针。以下是最小功能集：

```C
/* 使用您的设备名替换 xx_audio_dev */
static const struct audio_ops_s g_xx_audio(dev)_ops =
{
  .getcaps       = xx_audio(dev)_getcaps,
  .configure     = xx_audio(dev)_configure,
  .shutdown      = xx_audio(dev)_shutdown,
  .start         = xx_audio(dev)_start,
#ifndef CONFIG_AUDIO_EXCLUDE_STOP
  .stop          = xx_audio(dev)_stop,
#endif
#ifndef CONFIG_AUDIO_EXCLUDE_PAUSE_RESUME
  .pause         = xx_audio(dev)_pause,
  .resume        = xx_audio(dev)_resume,
#endif
  .allocbuffer   = xx_audio(dev)_allocbuffer,
  .freebuffer    = xx_audio(dev)_freebuffer,
  .enqueuebuffer = xx_audio(dev)_enqueuebuffer,
  .ioctl         = xx_audio(dev)_ioctl,
  .reserve       = xx_audio(dev)_reserve,
  .release       = xx_audio(dev)_release,
};
```

### 步骤 5：实现 `audio_ops_s` 各接口函数

#### `getcaps` - 获取设备能力

此函数响应上层对设备能力的查询。上层通常会分阶段进行查询：

- **阶段 1：查询设备类型和主格式**

    - **上层查询**：`ac_type = AUDIO_TYPE_QUERY`, `ac_subtype = AUDIO_TYPE_QUERY`
    - **驱动返回**：在 `caps` 结构体中填充：
        - 设备类型 (INPUT/OUTPUT) 到 `caps->ac_controls.b[0]`
        - 支持的声道数至 `caps->ac_channels`
        - 主格式 (如 `AUDIO_FMT_PCM`) 至 `caps->ac_format.hw`。

- **阶段 2：查询指定类型的详细能力**

    - **上层查询**：`ac_type = AUDIO_TYPE_INPUT (或 OUTPUT)`, `ac_subtype = AUDIO_TYPE_QUERY`
    - **驱动返回**：在 `caps` 结构体中填充该类型下支持的声道数（`caps->ac_channels`）和采样率（`caps->ac_controls.hw[0]`）。

- **阶段 3：查询指定主格式的子格式**

    - **上层查询**：`ac_type = AUDIO_TYPE_QUERY`, `ac_subtype` = 阶段 1 获取的主格式 (如 `AUDIO_FMT_PCM`)
    - **驱动返回**：在 `caps` 结构体中填充支持的具体子格式 (如 `AUDIO_SUBFMT_PCM_S16_LE`)。

#### `configure` - 配置音频参数

上层调用此函数配置音频参数。您需要根据传入的 `caps` 配置硬件，主要包括如下参数：

- 采样率 `samplerate`
- 采样精度 `bpsamp`
- 通道数据 `channel`

```C
static int xx_audio_configure(FAR struct audio_lowerhalf_s *dev,
                              FAR const struct audio_caps_s *caps)
{
    FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;
    switch (caps->ac_type)
    {
        case AUDIO_TYPE_OUTPUT:
            /* 从 caps 中提取参数 */
            priv->samprate  = caps->ac_controls.hw[0];
            priv->nchannels = caps->ac_channels;
            priv->bpsamp    = caps->ac_controls.b[2];
            
            /* 根据参数配置硬件 */
            xx_setmclkfrequency(priv);
            xx_settxchannels(priv);
            xx_setdatawidth(priv);
            xx_setbitrate(priv);
            break;
            
        /* 根据需要处理其他 case, 如 AUDIO_TYPE_INPUT */
        case XXX:
     }
 }
```

#### `ioctl` - 扩展控制命令

处理上层发送的 `ioctl` 命令。强烈建议支持以下标准命令：

-  **`AUDIOIOC_SETBUFFERINFO`****/****`AUDIOIOC_GETBUFFERINFO`**: 设置或获取音频缓冲区信息（数量 `nbuffers` 和大小 `buffer_size`，单位字节）。驱动应根据硬件能力（如 DMA 描述符限制）来决定是否接受上层设置。
- **`AUDIOIOC_GETLATENCY`**: 返回驱动内部当前缓存的音频帧数量，用于延迟计算。

```C++
static int xx_audio_ioctl(struct audio_lowerhalf_s *dev, int cmd,
                          unsigned long arg)
{
  struct xx_audio_s *priv = (struct xx_audio_s *)dev;
  int ret = 0;
  switch (cmd)
    {
        case AUDIOIOC_SETBUFFERINFO:
        {
          struct ap_buffer_info_s *info =
              (struct ap_buffer_info_s *)arg;

          priv->nbuffers    = info->nbuffers;
          priv->buffer_size = info->buffer_size;
        }
        break;
        case AUDIOIOC_GETBUFFERINFO:
        {
          struct ap_buffer_info_s *info =
              (struct ap_buffer_info_s *)arg;

          info->nbuffers    = priv->nbuffers;
          info->buffer_size = priv->buffer_size;
        }
        break;
        case AUDIOIOC_GETLATENCY:
        {
          xxx;
        }
        break;
     }
 }
```

驱动应根据硬件特性，决定 `buffer_size` 和 `nbuffers` 是固定的还是可动态调整的。

#### `allocbuffer` - 释放音频缓冲区（按需）

针对 buffer 需要在 Lower-Half 分配的场景，如 DMA，需要实现内存分配接口。

```C
static int xx_audio_allocbuffer(struct audio_lowerhalf_s *dev,
                                 struct audio_buf_desc_s *bufdesc)
{
  struct audio_dma_s *audio_dma = (struct audio_dma_s *)dev;
  struct ap_buffer_s *apb;

  apb = kumm_zalloc(sizeof(struct ap_buffer_s));
  *bufdesc->u.pbuffer = apb;
 
  /* Populate the buffer contents */

  apb->i.channels = 2;
  apb->crefs      = 1;
  apb->nmaxbytes  = audio_dma->buffer_size;
  apb->samp = audio_dma->alloc_addr +
              audio_dma->alloc_index *
              audio_dma->buffer_size;
  audio_dma->alloc_index++;
  nxmutex_init(&apb->lock);

  return sizeof(struct audio_buf_desc_s);
}
```

#### `freebuffer` - 入队音频缓冲区（按需）

一般和 `allocbuffer` 成对存在。

```C
static int xx_audio_freebuffer(struct audio_lowerhalf_s *dev,
                                struct audio_buf_desc_s *bufdesc)
{
  struct audio_dma_s *audio_dma = (struct audio_dma_s *)dev;
  struct ap_buffer_s *apb;

  apb = bufdesc->u.buffer;
  audio_dma->alloc_index--;
  kumm_free(apb);

  if (audio_dma->alloc_index == 0)
    {
      kumm_free(audio_dma->alloc_addr);
      audio_dma->alloc_addr = NULL;
    }

  return sizeof(struct audio_buf_desc_s);
}
```

#### `enqueuebuffer` - 入队音频缓冲区

上层通过此函数将包含音频数据的缓冲区（`ap_buffer_s`）传递给驱动。

- **播放**：应用将音频数据放置到 `buffer` 中传递到 audio driver 给到硬件去播放。
- **录音**：应用传递 `buffer` 给 audio driver，由 audio driver 填充 `buffer`，再传递回应用取走 `buffer` 中的录音数据。

**推荐实现模式**：使用一个工作线程和消息队列来异步处理缓冲区。

通常在驱动中通过一个 `struct dq_queue_s pendq` 队列用于保存应用发送到的 `buffer`，通过一个 `work thread` 来处理该队列上缓存的播放/录制的 `buffer` 数据，应用每 `enqueuebuffer` 传递一个buffer下来时，先将 `buffer` 挂载在队列上，然后通过 `msg queue` 消息通知 `work_thread` 去处理：

```C++
static int xx_audio_enqueuebuffer(FAR struct audio_lowerhalf_s *dev,
                                  FAR struct ap_buffer_s *apb)
{
  FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;
  struct audio_msg_s term_msg;
  int ret = OK;

  /* 增加缓冲区的引用计数，防止被提前释放 */
  apb_reference(apb);

  /* 增加了互斥锁，确保对共享队列的访问是线程安全的 */
  apb->flags |= AUDIO_APB_OUTPUT_ENQUEUED;
  dq_addlast(&apb->dq_entry, &priv->pendq);
  nxmutex_unlock(&priv->pendlock);

  /* 如果工作线程已启动，则发送消息通知其处理新缓冲区 */
  if (priv->mq.f_inode != NULL)
    {
      term_msg.msg_id  = AUDIO_MSG_ENQUEUE;
      term_msg.u.data = 0;

      ret = file_mq_send(&priv->mq, (FAR const char *)&term_msg,
                         sizeof(term_msg), CONFIG_XX_MSG_PRIO);
    }

  return ret;
}
```

#### `start` - 启动音频流

The upper layer calls this function to instruct the driver to start the hardware and begin processing audio data.

**Recommended Implementation Flow**:

1. **Create a message queue**: For communication between the main task and the worker thread.
2. **Create a worker thread**: This thread is responsible for the actual transfer of audio data.
3. **Start the hardware**: Enable peripherals like DMA or I2S.

```C
 static int xx_audio_start(FAR struct audio_lowerhalf_s *dev)
 {
     FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;
     struct sched_param sparam;
     struct mq_attr attr;
     pthread_attr_t tattr;
    
      /* 1. Create a message queue for the worker thread */
      snprintf(priv->mqname, sizeof(priv->mqname), "/tmp/%" PRIXPTR,
              (uintptr_t)priv);

      attr.mq_maxmsg  = 16;
      attr.mq_msgsize = sizeof(struct audio_msg_s);
      attr.mq_curmsgs = 0;
      attr.mq_flags   = 0;

      ret = file_mq_open(&priv->mq, priv->mqname,
                         O_RDWR | O_CREAT, 0644, &attr);
      
      /* 2. Create and start the worker thread */
      pthread_attr_init(&tattr);
      sparam.sched_priority = sched_get_priority_max(SCHED_FIFO) - 3;
      pthread_attr_setschedparam(&tattr, &sparam);
      pthread_attr_setstacksize(&tattr, CONFIG_CS4344_WORKER_STACKSIZE);

      ret = pthread_create(&priv->threadid, &tattr, cs4344_workerthread,
                          (pthread_addr_t)priv);
 }
```

**Worker Thread (`xx_audio_dev_worker`) Logic:**

- It loops, listening to the message queue and handling messages like `AUDIO_MSG_ENQUEUE` and `AUDIO_MSG_STOP`.
- It takes audio buffers from the pending queue (`pendq`) for processing (**playback** or **filling**).
- Upon receiving `AUDIO_MSG_STOP`, it processes all remaining buffers, notifies the upper layer via the `AUDIO_CALLBACK_COMPLETE` callback, and then safely exits the thread.

#### `stop` - Stop the Audio Stream

The upper layer calls this function to request a **graceful stop** of the audio stream, meaning the driver should wait for all buffered data to be processed before completely stopping.

```C++
static int xx_audio_stop(FAR struct audio_lowerhalf_s *dev)
#  endif
{
  FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;
  struct audio_msg_s term_msg;
  FAR void *value;

 /* 1. Send a STOP message to the worker thread */
  term_msg.msg_id = AUDIO_MSG_STOP;
  term_msg.u.data = 0;
  file_mq_send(&priv->mq, (FAR const char *)&term_msg, sizeof(term_msg),
               CONFIG_CS4344_MSG_PRIO);

  /* 2. Wait for the worker thread to exit safely */
  pthread_join(priv->threadid, &value);
  priv->threadid = 0;

  return OK;
}
```

**Worker Thread Response to `AUDIO_MSG_STOP`:**

> **Note**: `AUDIO_MSG_STOP` does not mean stop immediately; it means stop after all cached data has been played.

```C++
/* Executed in the worker thread after receiving a STOP message */

  /* 1. Return all in-flight buffers */
  nxmutex_lock(&priv->pendlock);
  while ((apb = (FAR struct ap_buffer_s *)dq_remfirst(&priv->pendq)) != NULL)
    {
      /* Release the reference to this buffer */
      apb_free(apb);

      /* Return the buffer to the upper layer via the DEQUEUE callback */
      priv->dev.upper(priv->dev.priv, AUDIO_CALLBACK_DEQUEUE, apb, OK);
    }

  nxmutex_unlock(&priv->pendlock);
  
  /* 2. Finally, notify the upper layer that the stop process is complete */
  priv->dev.upper(priv->dev.priv, AUDIO_CALLBACK_COMPLETE, NULL, OK);
```

#### `pause` - Pause the Audio Stream

Pauses the processing of audio data.

> **Note**: During a pause, the driver **must not** return buffers to the upper layer via the `AUDIO_CALLBACK_DEQUEUE` callback.

Method 1: Send `AUDIO_MSG_PAUSE` to the worker thread to pause playback/recording.

```C++
static int xx_audio_pause(FAR struct audio_lowerhalf_s *dev)
{
  FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;
  struct audio_msg_s term_msg;
  FAR void *value;

  /* Send a message to pause audio streaming */

  term_msg.msg_id = AUDIO_MSG_PAUSE;
  term_msg.u.data = 0;
  file_mq_send(&priv->mq, (FAR const char *)&term_msg, sizeof(term_msg),
               CONFIG_XX_MSG_PRIO);

  return OK;
}
```

Method 2: Use a variable to synchronize state directly.

```C++
static int xx_audio_pause(FAR struct audio_lowerhalf_s *dev)
{
  FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;

  if (priv->running && !priv->paused)
    {
      /* Disable interrupts to prevent us from suppling any more data */
      priv->paused = true;
    }

  return OK;
}
```

#### `resume` - Resume the Audio Stream

Resumes from a paused state. The driver can continue processing audio data and resume `AUDIO_CALLBACK_DEQUEUE` callbacks.

Method 1: Send `AUDIO_MSG_RESUME` to the worker thread to resume playback/recording.

```C++
static int xx_audio_resume(FAR struct audio_lowerhalf_s *dev)
{
  FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;
  struct audio_msg_s term_msg;
  FAR void *value;

  /* Send a message to resume audio streaming */

  term_msg.msg_id = AUDIO_MSG_RESUME;
  term_msg.u.data = 0;
  file_mq_send(&priv->mq, (FAR const char *)&term_msg, sizeof(term_msg),
               CONFIG_XX_MSG_PRIO);

  return OK;
}
```

Method 2: Use a variable to synchronize state directly.

```C++
static int xx_audio_resume(FAR struct audio_lowerhalf_s *dev)
{
  FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;

  if (priv->running && !priv->paused)
    {
      /* Disable interrupts to prevent us from suppling any more data */

      priv->paused = false;
    }

  return OK;
}
```

After the driver executes `resume`, it can continue audio playback/recording and send a DEQUEUE message via callback to return the `buffer` to the application.

```C
priv->dev.upper(priv->dev.priv, AUDIO_CALLBACK_DEQUEUE, apb, OK);
```

**`release`**: After audio playback/recording is complete, the application uses `release` to notify the driver to release associated resources.

**`reserve`**: Hardware-independent; the driver must reserve and implement this interface.

**`shutdown`**: Called when the driver module is unloaded for final resource cleanup.

## V. Key Implementation Details

This section delves into the key implementation details of the `getcaps` function and specific `ioctl` commands, which are central to ensuring correct interaction between the driver and the upper-layer framework.

### 1. `AUDIOIOC_SETPARAMETER` IOCTL

This is a generic parameter-setting interface designed for passing non-standard, platform-specific configurations.

- **Purpose**: Allows upper-layer applications to pass custom parameters to the driver for different scenarios (e.g., phone calls, music playback), enabling the driver to apply different audio effects or hardware configurations.
- **Format**: The `arg` parameter is a `char*` string that strictly follows the `"key=value"` format.
- **Examples**:

    - `"scenario=phone"`
    - `"scenario=music"`

### 2. `ac_channels` Channel Count Encoding

In the implementation of the `getcaps` function, the `ac_channels` member of `struct audio_caps_s` uses a specific format to represent both the minimum and maximum supported number of channels.

- **Encoding Rule**:

    - **Lower 4 bits**: Maximum supported number of channels.
    - **Upper 4 bits**: Minimum supported number of channels (set to 0 if no limit).

- **Examples**:

    - Supports 1 to 2 channels (min 1, max 2): `ac_channels = 0x12`
    - Supports only 2 channels (stereo, min and max are 2): `ac_channels = 0x22`
    - Supports only 1 channel (mono, min and max are 1): `ac_channels = 0x11`

### 3. `getcaps` Implementation Details

`getcaps` is a core **function** within the `audio_ops_s` operation set, not an `ioctl` command. It is responsible for reporting the driver's supported capabilities to the upper layer. The following is its typical implementation logic:

#### 3.1 Report Device Type and Main Format

When the upper layer queries with `ac_type = AUDIO_TYPE_QUERY` and `ac_subtype = AUDIO_TYPE_QUERY`, the driver must:

1. Set whether the device is `AUDIO_TYPE_INPUT` or `AUDIO_TYPE_OUTPUT` in `caps->ac_controls.b[0]`.
2. Report supported main formats as a bitmask in `caps->ac_format.hw`, for example, `(1 << (AUDIO_FMT_PCM - 1))` to indicate support for the PCM format.

#### 3.2 Report PCM Subformats

When the upper layer queries with `ac_type = AUDIO_TYPE_QUERY` and `ac_subtype = AUDIO_FMT_PCM`, the driver must:

1. Report the specific supported PCM subformats in `caps->ac_controls.b[0]`, for example, `AUDIO_SUBFMT_PCM_S16_LE`.
2. If multiple subformats are supported, you can continue populating `caps->ac_controls.b[1]`, and so on.
3. Terminate the list with `AUDIO_SUBFMT_END`.

#### 3.3 Report Capabilities for a Specific Type

When the upper layer queries with `ac_type = AUDIO_TYPE_OUTPUT` (or `INPUT`) and `ac_subtype = AUDIO_TYPE_QUERY`, the driver must:

1. Populate `caps->ac_channels` using the encoding rule described previously.
2. Report all supported sample rates as a bitmask in `caps->ac_controls.hw[0]`, for example, `AUDIO_SAMP_RATE_8K | AUDIO_SAMP_RATE_16K | AUDIO_SAMP_RATE_48K`.

#### 3.4 Code Implementation Reference

The following example code demonstrates a complete implementation of the `getcaps` function, covering responses to various types of queries.

```C
static int bes_rpmsg_aud_svr_getcaps(FAR struct audio_lowerhalf_s *dev,
                                     int type, FAR struct audio_caps_s *caps)
{
  FAR struct bes_rpmsg_aud_svr_dev_s *priv = get_bes_rpmsg_aud_svr_dev(dev);
  audinfo("[RPMSG_AUD] type=%d\n", type);

  /* Validate the structure */

  DEBUGASSERT(caps->ac_len >= sizeof(struct audio_caps_s));

  /* Fill in the caller's structure based on requested info */

  caps->ac_format.hw = 0;
  caps->ac_controls.w = 0;

  switch (caps->ac_type)
    {
      /* Caller is querying for the types of units we support */

    case AUDIO_TYPE_QUERY:

      /* Provide our overall capabilities.  The interfacing software must then
       * call us back for specific info for each capability. */

      switch (caps->ac_subtype)
        {
        case AUDIO_TYPE_QUERY:
          /* We don't decode any formats! Only something above us in the audio
           * stream can perform decoding on our behalf. */

          /* The types of audio units we implement */
          caps->ac_controls.b[0] =
            (isCaptureDev(dev) ? AUDIO_TYPE_INPUT : AUDIO_TYPE_OUTPUT) |
            AUDIO_TYPE_FEATURE | AUDIO_TYPE_PROCESSING;
          caps->ac_format.hw = (1 << (AUDIO_FMT_PCM - 1));
          break;

        case AUDIO_FMT_MIDI:

          /* We only support Format 0 */

          caps->ac_controls.b[0] = AUDIO_SUBFMT_END;
          break;

        case AUDIO_FMT_PCM:
          caps->ac_controls.b[0] = AUDIO_SUBFMT_PCM_S16_LE;
          caps->ac_controls.b[1] = AUDIO_SUBFMT_END;
          break;

        default:
          caps->ac_controls.b[0] = AUDIO_SUBFMT_END;
          break;
        }

      break;

      /* Provide capabilities of our OUTPUT unit */

    case AUDIO_TYPE_OUTPUT:
      switch (caps->ac_subtype)
        {
        case AUDIO_TYPE_QUERY:
          /* Report the Sample rates we support */
          if (priv->devicetype == AUD_STREAM_BT_PCM) {
            caps->ac_channels = 1;
            caps->ac_controls.hw[0] = AUDIO_SAMP_RATE_8K |
                                     AUDIO_SAMP_RATE_16K;
          } else {
            caps->ac_channels = CONFIG_AUDIO_BES_OUTPUT_CHANNELS;
            caps->ac_controls.hw[0] = AUDIO_SAMP_RATE_8K |
                                     AUDIO_SAMP_RATE_11K |
                                     AUDIO_SAMP_RATE_16K |
                                     AUDIO_SAMP_RATE_22K |
                                     AUDIO_SAMP_RATE_32K |
                                     AUDIO_SAMP_RATE_44K |
                                     AUDIO_SAMP_RATE_48K;
          }
          break;

        case AUDIO_FMT_MP3:
        case AUDIO_FMT_WMA:
        case AUDIO_FMT_PCM:
          break;

        default:
          break;
        }

      break;
    case AUDIO_TYPE_INPUT:

      switch (caps->ac_subtype)
        {
        case AUDIO_TYPE_QUERY:
          /* Report supported input sample rates */
          if (priv->devicetype == AUD_STREAM_BT_PCM) {
            caps->ac_channels = 1;
            caps->ac_controls.hw[0] = AUDIO_SAMP_RATE_8K |
                                     AUDIO_SAMP_RATE_16K;
          } else {
            caps->ac_channels = CONFIG_AUDIO_BES_INPUT_CHANNELS;
            caps->ac_controls.hw[0] = AUDIO_SAMP_RATE_8K |
                                     AUDIO_SAMP_RATE_11K |
                                     AUDIO_SAMP_RATE_16K |
                                     AUDIO_SAMP_RATE_22K |
                                     AUDIO_SAMP_RATE_32K |
                                     AUDIO_SAMP_RATE_44K |
                                     AUDIO_SAMP_RATE_48K;
          }
          break;
        default:
          break;
        }
      break;

      /* Provide capabilities of our FEATURE units */

    case AUDIO_TYPE_FEATURE:

      /* If the sub-type is UNDEF, then report the Feature Units we support */

      if (caps->ac_subtype == AUDIO_FU_UNDEF)
        {
          /* Fill in the ac_controls section with the Feature Units we have */

          caps->ac_controls.b[0] = AUDIO_FU_VOLUME |
            AUDIO_FU_BASS | AUDIO_FU_TREBLE;
          caps->ac_controls.b[1] = AUDIO_FU_BALANCE >> 8;
        }
      else
        {
          /* TODO: Do we need to provide specific info for the Feature Units,
           * such as volume setting ranges, etc.? */
        }

      break;

      /* Provide capabilities of our PROCESSING unit */

    case AUDIO_TYPE_PROCESSING:

      switch (caps->ac_subtype)
        {
        case AUDIO_PU_UNDEF:

          /* Provide the type of Processing Units we support */

          caps->ac_controls.b[0] = AUDIO_PU_STEREO_EXTENDER;
          break;

        case AUDIO_PU_STEREO_EXTENDER:

          /* Provide capabilities of our Stereo Extender */

          caps->ac_controls.b[0] = AUDIO_STEXT_ENABLE | AUDIO_STEXT_WIDTH;
          break;

        default:

          /* Other types of processing uint we don't support */

          break;
        }

      break;

      /* All others we don't support */

    default:

      /* Zero out the fields to indicate no support */

      caps->ac_subtype = 0;
      caps->ac_channels = 0;

      break;
    }

  /* Return the length of the audio_caps_s struct for validation of proper
   * Audio device type. */

  audinfo("[RPMSG_AUD] Return %d\n", caps->ac_len);
  return caps->ac_len;
}
```

## VI. Important Considerations

1. **Interface Call Latency**

    - **Requirement**: All `audio_ops_s` interface implementations should avoid long blocking operations. It is recommended to keep the execution time of each interface under **10ms**.
    - **Risk**: Excessive latency (e.g., 40ms in the `start` function) can cause overflow errors in the audio data stream, especially for recording.

2. **Buffer Management**

    - **Requirement**: You **must never lose** any `ap_buffer_s` buffer passed from the upper layer via `enqueuebuffer`.
    - **Risk**: The openvela audio framework delegates buffer lifecycle management to the Lower-Half driver. If the driver loses a buffer's pointer (e.g., by failing to handle and return it in all code paths), it will directly cause a **memory leak**. All received buffers must be returned via the `upper()` callback.
