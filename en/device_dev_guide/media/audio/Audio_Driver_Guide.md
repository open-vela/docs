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
