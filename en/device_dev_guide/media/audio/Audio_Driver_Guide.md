# Audio Driver Adaptation Guide

\[ [English] | [简体中文](../../../../zh-cn/device_dev_guide/media/audio/Audio_Driver_Guide.md) \]

## I. Overview

This document provides embedded development engineers with detailed steps for adapting and implementing an audio Lower-Half driver for the openvela real-time operating system on a specific hardware platform. By following this guide, you can seamlessly integrate your chip's audio capabilities into the openvela audio framework.

## II. Pre-Adaptation Analysis

Before you start coding, you must complete the following analysis, which is the foundation for a successful adaptation.

### 1. Analyze Hardware Capabilities

You must have a comprehensive understanding of the target chip's audio features, including:

- The control logic and data formats of audio interfaces (e.g., I2S, PCM).
- The usage of the DMA (Direct Memory Access) controller, including channel configuration, transfer modes, and interrupt handling (if any).
- The control method for the audio codec or power amplifier (PA), typically via I2C or SPI.
- The range of audio parameters supported by the hardware, such as sample rate, bit depth, and number of channels.

### 2. Understand the openvela Audio Framework

The openvela audio framework provides a standardized abstraction layer for driver development. You can refer to the [Audio Driver Principles](./Audio_Driver_Prin_desc.md) for a deeper understanding. Its core advantages include:

- **Complete Test Application**: The framework includes a built-in verification program. After completing the driver adaptation, you can verify core functionalities without writing additional test code.
- **Unified Driver Interface**: openvela defines a standard `audio_ops_s` interface and `ioctl` commands. You must adhere to these definitions and implement the corresponding hardware-specific logic in the callback functions.
- **Standardized Call Flow**: The framework handles the complete call logic from the application layer to the lower-level driver (Upper-Half). You only need to focus on implementing the Lower-Half driver, encapsulating chip-related operations.
- **Loosely-Coupled Composite Nodes**: Depending on the hardware architecture, you can:

    - Choose to implement a new, all-in-one audio device node.
    - Or only replace a specific Lower-Half driver within an existing composite node (e.g., an independent PA or Codec driver).

- **Built-in Reusable Components**: openvela provides common Lower-Half drivers (e.g., DMA control drivers). Before development, evaluate and reuse these components to accelerate the development process.
- **Rich Reference Examples**:

    - The `sim` platform provides `sim_alsa.c` as a basic reference.
    - The open-source community provides implementations for various chips, such as the [audio driver for song-u1](https://github.com/FishsemiCode/nuttx/tree/song-u1/drivers/audio).

### 3. Define Adaptation Goals

Based on project requirements, adaptation tasks are typically divided into the following two categories:

- **Goal 1: Implement a complete audio node from scratch**

    - **Scenario**: Adapting audio functionality for a brand-new platform or chip.
    - **Requirement**: Requires implementing both data flow interfaces (e.g., I2S/DMA) and control flow interfaces (e.g., I2C/SPI).

- **Goal 2: Replace or add an independent Lower-Half driver**

    - **Scenario**: Replacing part of the hardware on an existing platform, such as updating the PA.
    - **Requirement**: Only requires implementing the control interface for that specific hardware.

## III. Task Breakdown

This guide uses the more complex **Goal 1** as an example for task breakdown.

1. **Node Type Identification**: Determine whether your audio chain is better implemented as a **single node** (all functionality in one driver) or a **composite node** (e.g., I2S, DMA, and Codec as separate drivers).
2. **Driver Reuse Assessment**: If you choose a **composite node**, assess whether you can reuse the built-in Lower-Half drivers in openvela.

    - **Reusable**: For example, you can reuse the `audio dma lowerhalf`. In this case, you only need to re-implement the `dma_ops_s` operation set.
    - **Not Reusable**: Similar to the single-node approach, you will need to implement a new Audio Lower-Half driver from scratch.

## IV. Steps to Implement an Audio Lower-Half Driver

This section details the core implementation process for a new Audio Lower-Half driver.

### Step 1: Define the Private Data Structure

Define a private data structure for the driver. This structure must have `struct audio_lowerhalf_s` as its first member.

```C
/* Replace xx_audio_dev with your device name */
struct xx_audio_dev_s
{
  /* This struct must be the first member to support type casting */
  struct audio_lowerhalf_s dev;

  /* Add private variables required by the driver here */
  // E.g., hardware register base address, worker thread ID, status flags, etc.
  // pthread_t threadid;
  // bool paused;
  // ...
};
```

### Step 2: Implement the `initialize` Function

This function is responsible for allocating memory for the private structure and associating it with the `audio_ops_s` operation set.

```C
/* Replace xx_audio(dev) with your device name */
struct audio_lowerhalf_s *xx_audio(dev)_initialize(...)
{
  struct xx_audio(dev)_s *priv;
  int ret;

  /* Allocate and zero out the private structure memory */
  priv = kmm_zalloc(sizeof(struct xx_audio(dev)_s));
  if (!priv)
    {
      return NULL;
    }
  
  /* Critical step: Point the ops pointer to the defined global audio_ops_s instance */
  priv->dev.ops  = &g_xx_audio(dev)_ops;

  /* Other initialization code... */

  return &priv->dev;
}
```

### Step 3: Register the Device Node

Choose a suitable place, such as `board_early_initialize`, to register the device node.

```C
audio_register("pcm0c", *xx_audio(dev)_initialize(true, 0));
audio_register("pcm0p", *xx_audio(dev)_initialize(false, 0));
```

### Step 4: Define the `audio_ops_s` Interface Operation Set

Define a static constant `audio_ops_s` structure and populate it with the function pointers you will implement. The following is a minimal functional set:

```C
/* Replace xx_audio_dev with your device name */
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

### Step 5: Implement the `audio_ops_s` Interface Functions

#### `getcaps` - Get Device Capabilities

This function responds to queries from the upper layer about the device's capabilities. The upper layer typically queries in stages:

- **Stage 1: Query Device Type and Main Format**

    - **Upper-layer Query**: `ac_type = AUDIO_TYPE_QUERY`, `ac_subtype = AUDIO_TYPE_QUERY`
    - **Driver Response**: Populate the `caps` structure with:

        - Device type (INPUT/OUTPUT) in `caps->ac_controls.b[0]`
        - Supported number of channels in `caps->ac_channels`
        - Main format (e.g., `AUDIO_FMT_PCM`) in `caps->ac_format.hw`

- **Stage 2: Query Detailed Capabilities for a Specific Type**

    - **Upper-layer Query**: `ac_type = AUDIO_TYPE_INPUT (or OUTPUT)`, `ac_subtype = AUDIO_TYPE_QUERY`
    - **Driver Response**: Populate the `caps` structure with the supported number of channels (`caps->ac_channels`) and sample rates (`caps->ac_controls.hw[0]`) for that type.

- **Stage 3: Query Sub-formats for a Specific Main Format**

    - **Upper-layer Query**: `ac_type = AUDIO_TYPE_QUERY`, `ac_subtype` = the main format from Stage 1 (e.g., `AUDIO_FMT_PCM`)
    - **Driver Response**: Populate the `caps` structure with the specific supported sub-formats (e.g., `AUDIO_SUBFMT_PCM_S16_LE`).

#### `configure` - Configure Audio Parameters

The upper layer calls this function to configure audio parameters. You need to configure the hardware based on the incoming `caps`, primarily including these parameters:

- Sample rate: `samplerate`
- Sample precision: `bpsamp`
- Channel data: `channel`

```C
static int xx_audio_configure(FAR struct audio_lowerhalf_s *dev,
                              FAR const struct audio_caps_s *caps)
{
    FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;
    switch (caps->ac_type)
    {
        case AUDIO_TYPE_OUTPUT:
            /* Extract parameters from caps */
            priv->samprate  = caps->ac_controls.hw[0];
            priv->nchannels = caps->ac_channels;
            priv->bpsamp    = caps->ac_controls.b[2];
            
            /* Configure hardware based on parameters */
            xx_setmclkfrequency(priv);
            xx_settxchannels(priv);
            xx_setdatawidth(priv);
            xx_setbitrate(priv);
            break;
            
        /* Handle other cases as needed, e.g., AUDIO_TYPE_INPUT */
        case XXX:
     }
 }
```

#### `ioctl` - Extended Control Commands

Handles `ioctl` commands sent from the upper layer. It is highly recommended to support the following standard commands:

- **`AUDIOIOC_SETBUFFERINFO`/`AUDIOIOC_GETBUFFERINFO`**: Set or get audio buffer information (number `nbuffers` and size `buffer_size` in bytes). The driver should decide whether to accept the upper layer's settings based on hardware capabilities (e.g., DMA descriptor limitations).
- **`AUDIOIOC_GETLATENCY`**: Return the number of audio frames currently cached within the driver, which is used for latency calculations.

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

The driver should determine whether `buffer_size` and `nbuffers` are fixed or dynamically adjustable based on hardware characteristics.

#### `allocbuffer` - Allocate Audio Buffer (On-Demand)

For scenarios where the buffer needs to be allocated in the Lower-Half, such as for DMA, a memory allocation interface must be implemented.

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

#### `freebuffer` - Free Audio Buffer (On-Demand)

This function typically exists as a pair with `allocbuffer`.

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

#### `enqueuebuffer` - Enqueue an Audio Buffer

The upper layer uses this function to pass a buffer containing audio data (`ap_buffer_s`) to the driver.

- **Playback**: The application places audio data into the `buffer` and passes it to the audio driver for the hardware to play.
- **Recording**: The application passes an empty `buffer` to the audio driver, which fills the `buffer` with recorded data and then passes it back to the application.

**Recommended Implementation Pattern**: Use a worker thread and a message queue to process buffers asynchronously.

Typically, a driver uses a `struct dq_queue_s pendq` queue to store buffers received from the application. A `work thread` processes the playback/recording buffers queued on `pendq`. Each time the application calls `enqueuebuffer` to pass down a buffer, the driver first adds the buffer to the queue and then sends a message via a `msg queue` to notify the `work_thread` to process it:

```C++
static int xx_audio_enqueuebuffer(FAR struct audio_lowerhalf_s *dev,
                                  FAR struct ap_buffer_s *apb)
{
  FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;
  struct audio_msg_s term_msg;
  int ret = OK;

  /* Increment the buffer's reference count to prevent premature release */
  apb_reference(apb);

  /* A mutex ensures that access to the shared queue is thread-safe */
  apb->flags |= AUDIO_APB_OUTPUT_ENQUEUED;
  dq_addlast(&apb->dq_entry, &priv->pendq);
  nxmutex_unlock(&priv->pendlock);

  /* If the worker thread has started, send a message to notify it to process the new buffer */
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

#### `start` - Start the Audio Stream

上层调用此函数通知驱动启动硬件，开始处理音频数据。

**推荐实现流程**：

1. **创建消息队列**：用于主任务与工作线程之间的通信。
2. **创建工作线程**：该线程负责处理音频数据的实际传输。
3. **启动硬件**：使能 DMA 或 I2S 等外设。

```C
 static int xx_audio_start(FAR struct audio_lowerhalf_s *dev)
 {
     FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;
     struct sched_param sparam;
     struct mq_attr attr;
     pthread_attr_t tattr;
    
      /* 1. 为工作线程创建消息队列 */
      snprintf(priv->mqname, sizeof(priv->mqname), "/tmp/%" PRIXPTR,
              (uintptr_t)priv);

      attr.mq_maxmsg  = 16;
      attr.mq_msgsize = sizeof(struct audio_msg_s);
      attr.mq_curmsgs = 0;
      attr.mq_flags   = 0;

      ret = file_mq_open(&priv->mq, priv->mqname,
                         O_RDWR | O_CREAT, 0644, &attr);
      
      /* 2. 创建并启动工作线程 */
      pthread_attr_init(&tattr);
      sparam.sched_priority = sched_get_priority_max(SCHED_FIFO) - 3;
      pthread_attr_setschedparam(&tattr, &sparam);
      pthread_attr_setstacksize(&tattr, CONFIG_CS4344_WORKER_STACKSIZE);

      ret = pthread_create(&priv->threadid, &tattr, cs4344_workerthread,
                          (pthread_addr_t)priv);
 }
```

**工作线程 (****`xx_audio_dev_worker`****) 逻辑：**

- 循环监听消息队列，处理如 `AUDIO_MSG_ENQUEUE`, `AUDIO_MSG_STOP` 等消息。
- 从待处理队列 (`pendq`) 中取出音频缓冲区进行处理（**播放**或**填充**）。
- 在接收到 `AUDIO_MSG_STOP` 后，处理完所有剩余缓冲区，然后通过 `AUDIO_CALLBACK_COMPLETE` 回调通知上层，最后安全退出线程。

#### `stop` - 停止音频流

上层调用此函数请求**优雅停止（graceful stop）音频流**，即驱动应等待所有已缓冲的数据处理完毕后再完全停止。

```C++
static int xx_audio_stop(FAR struct audio_lowerhalf_s *dev)
#  endif
{
  FAR struct xx_dev_s *priv = (FAR struct xx_dev_s *)dev;
  struct audio_msg_s term_msg;
  FAR void *value;

 /* 1. 向工作线程发送 STOP 消息 */
  term_msg.msg_id = AUDIO_MSG_STOP;
  term_msg.u.data = 0;
  file_mq_send(&priv->mq, (FAR const char *)&term_msg, sizeof(term_msg),
               CONFIG_CS4344_MSG_PRIO);

  /* 2. 等待工作线程安全退出 */
  pthread_join(priv->threadid, &value);
  priv->threadid = 0;

  return OK;
}
```

**工作线程对** **`AUDIO_MSG_STOP`** **的响应：**

> **注意**： `AUDIO_MSG_STOP` 并不是立即停止，而是等缓存的数据播放完再停止。

```C++
/* 在工作线程中，收到 STOP 消息后执行 */

  /* 1. 返回所有在途的缓冲区 */
  nxmutex_lock(&priv->pendlock);
  while ((apb = (FAR struct ap_buffer_s *)dq_remfirst(&priv->pendq)) != NULL)
    {
      /* 释放对此缓冲区的引用 */
      apb_free(apb);

      /* 将缓冲区通过 DEQUEUE 回调返回给上层 */
      priv->dev.upper(priv->dev.priv, AUDIO_CALLBACK_DEQUEUE, apb, OK);
    }

  nxmutex_unlock(&priv->pendlock);
  
  /* 2. 最后，通知上层停止流程已完成 */
  priv->dev.upper(priv->dev.priv, AUDIO_CALLBACK_COMPLETE, NULL, OK);
```

#### `pause` - 暂停音频流

暂停处理音频数据。

> **注意**：在暂停期间，驱动**不得**通过 `AUDIO_CALLBACK_DEQUEUE` 回调向上层返回缓冲区。

方式一：可以向 work thread 发 `AUDIO_MSG_PAUSE` 暂停播放/录制。

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

方式二：直接使用变量来同步状态：

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

#### `resume` - 恢复音频流

从暂停状态恢复。驱动可以继续处理音频数据，并恢复 `AUDIO_CALLBACK_DEQUEUE` 回调。

方式一：向 work thread 发 `AUDIO_MSG_RESUME` 恢复播放/录制。

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

方式二：直接使用变量来同步状态。

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

驱动在执行 resume 之后可以继续音频播放/录音，并且调用回调向应用发送 DQUEUE 消息返回 `buffer`。

```C
priv->dev.upper(priv->dev.priv, AUDIO_CALLBACK_DEQUEUE, apb, OK);
```

**`release`**： 音频播放/录制完成之后，应用通过 `release` 通知驱动释放相关资源。

**`reserve`**：与硬件无关，驱动需要保留和实现该接口。

**`shutdown`**: 在驱动模块卸载时调用，用于最终的资源清理。

## 五、关键实现细节

本章节将深入探讨 `getcaps` 函数和特定 `ioctl` 命令的关键实现细节，这些是确保驱动与上层框架正确交互的核心。

### 1、`AUDIOIOC_SETPARAMETER` IOCTL

这是一个通用的参数设置接口，专用于传递非标准的、平台特定的配置。

- 用途：允许上层应用根据不同场景（如通话、音乐播放）向驱动传递定制化参数，以便驱动应用不同的音频效果或硬件配置。
- 格式：参数 `arg` 是一个 `char*` 字符串，其格式严格遵循 `"key=value"`。
- 示例：
    - `"scenario=phone"`
    - `"scenario=music"`

### 2、`ac_channels` 声道数编码

在 `getcaps` 函数的实现中，`struct audio_caps_s` 的 `ac_channels` 成员使用一种特定的格式进行编码，以同时表示支持的最小和最大声道数。

- **编码规则**：
    - **低 4 位**: 支持的**最大**通道数。
    - **高 4 位**: 支持的**最小**通道数（如果无限制设为 0）。
- **示例**：
    - 支持 1 到 2 通道（最小为 1，最大为 2）：`ac_channels = 0x12`
    - 仅支持 2 通道（立体声，最小和最大均为 2）：`ac_channels = 0x22`
    - 仅支持 1 通道（单声道，最小和最大均为 1）：`ac_channels = 0x11`

### 3、`getcaps` 实现详解

`getcaps` 是 `audio_ops_s` 操作集中的一个核心**函数**，而非 `ioctl` 命令。它负责向上层报告驱动所支持的各项能力。以下是其典型的实现逻辑：

#### 3.1 报告设备类型与主格式

当上层以 `ac_type = AUDIO_TYPE_QUERY` 和 `ac_subtype = AUDIO_TYPE_QUERY` 查询时，驱动需要：

1. 在 `caps->ac_controls.b[0]` 中设置设备是 `AUDIO_TYPE_INPUT` 还是 `AUDIO_TYPE_OUTPUT`。
2. 在 `caps->ac_format.hw` 中以位掩码形式报告支持的主格式，例如 `(1 << (AUDIO_FMT_PCM - 1))` 表示支持 PCM 格式。

#### 3.2 报告 PCM 子格式

当上层以 `ac_type = AUDIO_TYPE_QUERY` 和 `ac_subtype = AUDIO_FMT_PCM` 查询时，驱动需要：

1. 在 `caps->ac_controls.b[0]` 中报告支持的具体 PCM 子格式，例如 `AUDIO_SUBFMT_PCM_S16_LE`。
2. 如果支持多种子格式，可以继续填充 `caps->ac_controls.b[1]`，以此类推。
3. 以 `AUDIO_SUBFMT_END` 结尾。

#### 3.3 报告指定类型的能力

当上层以 `ac_type = AUDIO_TYPE_OUTPUT` (或 `INPUT`) 和 `ac_subtype = AUDIO_TYPE_QUERY` 查询时，驱动需要：

1. 使用前述的编码规则填充 `caps->ac_channels`。
2. 在 `caps->ac_controls.hw[0]` 中以位掩码形式报告支持的所有采样率，例如 `AUDIO_SAMP_RATE_8K | AUDIO_SAMP_RATE_16K | AUDIO_SAMP_RATE_48K`。

#### 3.4 代码实现参考

以下示例代码展示了 `getcaps` 函数的完整实现逻辑，覆盖了对不同类型查询的响应。

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

## 六、注意事项

1. **接口调用耗时**

    - **要求**：所有 `audio_ops_s` 接口的实现应避免长时间阻塞。建议将每个接口的执行时间控制在 **10ms** 以内。
    - **风险**：过长的耗时（例如，在 `start` 中耗时 40ms）可能导致音频数据流（尤其是录音）出现溢出（overflow）错误。

2. **缓冲区管理**

    - **要求**：**绝不能丢失**任何从上层 `enqueuebuffer` 传入的 `ap_buffer_s` 缓冲区。
    - **风险**：openvela 音频框架将缓冲区的生命周期管理委托给 Lower-Half 驱动。一旦驱动丢失了缓冲区的指针（例如，未能在所有代码路径中正确处理并返回），将直接导致**内存泄漏**。所有收到的缓冲区必须通过 `upper()` 回调返回。
