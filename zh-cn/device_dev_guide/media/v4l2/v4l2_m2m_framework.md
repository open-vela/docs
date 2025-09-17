# V4L2 M2M 框架介绍

[[English](../../../../en/device_dev_guide/media/v4l2/v4l2_m2m_framework.md) | 简体中文]

## 一、概述

`openvela` 的**视频编解码**框架借鉴了 Linux 内核的 **Video for Linux 2 (V4L2)** 框架，并重点实现了其 **Memory-to-Memory (M2M)** 模型。在 Linux 中，`v4l2m2m` 是一个标准模块，专用于处理需要内存作为输入和输出的硬件，如视频编解码器（Codec）。

通过在 `openvela` 中引入 `v4l2m2m` 接口，我们成功统一了**视频编解码驱动框架**，为**南向芯片厂商**提供了标准的编解码驱动接入层。这使得第三方硬件可以便捷地集成到 `openvela` 生态中，显著降低了开发和适配成本。

V4L2 M2M 整个框架的核心点在于复用 V4L2 框架的 `frame buffer` 管理模块，增加一路 `output queue`，用于接收编解码器输入数据，原始 `capture queue` 用于存放编解码器的输出数据。下图以视频解码为例，展示使用M2M框架的处理流程。

![img](./figures/001.png)

> **说明**：在V4L2 M2M框架中，`output queue` 为数据的**输入端**。`capture queue` 始终作为**输出端**，主要是为保持与 V4L2 Camera 框架的队列使用习惯一致。

## 二、框架总览

`openvela` V4L2 M2M框架采用经典的**分层**设计，将通用逻辑与设备特定实现解耦。这种模式类似于 `openvela` 音频驱动中的**上层 (Upper-Half)** 和**下层 (Lower-Half)** 模型。

对上层应用来说，`openvela` V4L2 M2M框架提供了兼容 Linux 标准的接口给应用使用；对底层的驱动开发者来说，`openvela` V4L2 M2M 框架简化了适配接口，可快速完成驱动开发。

![img](./figures/002.png)

- **V4L2 通用层 (Upper-Half):**

    - 由 `v4l2_core`、`v4l2_cap` (用于摄像头等捕捉设备) 和 `v4l2_m2m` (用于编解码设备) 模块构成，有对应的 `capture ops` 和 `codec ops`。
    - 该层负责响应来自应用程序的 `ioctl` 系统调用，处理 V4L2 的核心逻辑、缓冲区管理和事件机制。它为下层驱动定义了一套标准的操作函数集（ops）。

- **设备驱动层 (Lower-Half):**

    - 由具体的硬件驱动程序构成，例如文档中用作示例的 `sim_camera` 和 `sim_decoder`。
    - **驱动开发者的核心工作**就是实现这一层。通过填充并注册特定的 `ops` 结构体，驱动即可与通用层无缝对接。

当系统启动后，下层驱动（如 `sim_decoder`）会**注册相应的设备节点（如 `/dev/video1`）**。应用程序通过标准**文件接口访问这些节点**，请求经由 V4L2 通用层，最终分派到对应的**下层驱动进行处理**。

## 三、框架详解

本章将深入剖析 `openvela` V4L2 M2M Codec 驱动的内部机制，涵盖其核心组件、接口定义、数据交互模型及关键开发实践。

### 1、核心组件

`openvela` 的 `v4l2m2m` 实现借鉴了 Linux 的成熟设计，其架构围绕以下四个核心组件构建：

- **`codec_ops_s`**: **下层驱动的核心实现**。它定义了一套操作回调函数，功能对标 Linux 的 **`v4l2_ioctl_ops`**。驱动开发者的主要工作就是实现此接口。
- **`v4l2_ops_s`**: **V4L2 通用 `ioctl` 接口**。这是一个框架层（Upper-Half）的接口，M2M 通用层会提供一个该接口的实例 (`g_codec_vops`)，它负责接收上层请求并调用到下层驱动的具体实现 (`codec_ops_s`)。
- **`codec_file_s`**: **设备实例管理器**。每当应用程序 `open` 设备节点时，框架会创建一个 `codec_file_s` 实例来管理该会话的上下文，包括独立的缓冲区队列，从而实现多实例支持。并且 m2m 中对 `buffer` 的分配管理也是通过`codec_file_s`来完成。
- **`codec_mng_s`**: **设备顶层管理器**。在驱动注册设备节点（如 `/dev/video1`）时，框架会创建一个 `codec_mng_s` 实例，作为该设备在内核中的全局句柄。

![img](./figures/003.png)

> **图注:** 此图清晰展示了 `v4l2_ops_s` 作为通用入口，如何通过 `codec_mng_s` 和 `codec_file_s` 最终调用到驱动开发者实现的 `codec_ops_s`。

### 2、关键代码

V4L2 M2M 框架的逻辑主要分布在以下几个文件中：

- `nuttx/drivers/video/v4l2_core.c`: V4L2 框架的总入口，定义了顶层文件操作 **`g_v4l2_fops`**，并将请求分发至 Camera 或 M2M 的实现。

- `nuttx/drivers/video/v4l2_m2m.c`: **M2M 通用层 (Upper-Half)**。实现了 M2M 设备的通用逻辑，定义了 `g_codec_fops` 和 `g_codec_vops`，对应`file_operations`和`v4l2_ops_s`。**这是下层驱动主要交互的模块**。参考 `sim_decoder`，`codec` 的开发主要是 `codec_ops_s`的实现，以及完成输入输出 `buffer` 的对接。

- `nuttx/drivers/video/video_framebuff.c`: V4L2 通用的缓冲区管理模块，为上层提供统一的缓冲区申请、排队和生命周期管理能力。

- `nuttx/drivers/video/v4l2_cap.c`: Camera 设备的通用实现，Codec 开发一般不直接涉及。包括 `image capture` 和 `video capture` ，定义了 Camera 的`g_capture_fops`和`g_capture_vops`，对应`file_operations`和`v4l2_ops_s`。

### 3、接口与数据结构

本节详细介绍 M2M 驱动开发中涉及的关键数据结构和操作集。从顶层到底层顺序进行讲解。

#### `codec_mng_t`

`codec_mng_t`是设备总管理结构体，在调用`codec_register`驱动注册接口的时候，动态分配，并与`driver`实现接口进行绑定，以此实现将上层应用的请求转换到`driver`请求中。

```C
struct codec_mng_s
{
  struct v4l2_s v4l2;        // v4l2 框架通用结构体，框架实现
  FAR struct codec_s *codec; // v4l2 driver实现接口，Vendor实现
};
```

#### `v4l2_s`

在`openvela`V4L2框架中，一个V4L2设备对应的一个`v4l2_s`结构体，封装了指向设备具体操作的两个核心函数指针表：`vops` 和 `fops`。

- `vops`: 指向 `v4l2_ops_s` 结构体，定义了所有 V4L2 相关的 `ioctl` 操作。
- `fops`: 指向 `file_operations` 结构体，定义了标准的 VFS 文件操作（如 `open`, `close`, `poll` 等）。

根据设备类型，`v4l2_s` 会被实例化并指向不同的实现，例如 Camera 设备对应 `g_capture_vops` 和 `g_capture_fops`，而 M2M Codec 设备则对应 `g_codec_vops` 和 `g_codec_fops`。

```C
struct v4l2_s
{
  FAR const struct v4l2_ops_s      *vops;
  FAR const struct file_operations *fops;
};
```

#### `v4l2_ops_s`

`v4l2_ops_s` 是 V4L2 框架中**通用**的 `ioctl` 操作函数集。它定义了所有 V4L2 设备（包括 Camera 和 M2M Codec）可能支持的操作的原型。当一个 `ioctl` 请求通过 VFS 传递到 V4L2 核心层后，最终会通过该结构体中的函数指针分发到具体设备类型的通用层（如 `v4l2_m2m.c`）进行处理。

```C
struct v4l2_ops_s
{
  CODE int (*querycap)(FAR struct file *filep,
                       FAR struct v4l2_capability *cap);
  CODE int (*g_input)(FAR int *num);
  CODE int (*enum_input)(FAR struct file *filep,
                         FAR struct v4l2_input *input);
  CODE int (*reqbufs)(FAR struct file *filep,
                      FAR struct v4l2_requestbuffers *reqbufs);
  CODE int (*querybuf)(FAR struct file *filep,
                       FAR struct v4l2_buffer *buf);
// ... 其他标准V4L2操作 ...
```

#### `codec_s`

`codec_s`结构体中目前只包含`codec_ops_s`结构体，即只需要`driver`适配`codec_ops_s`接口即可。后续会更新实际需求，对`codec_s`结构体进行扩展。

```C
struct codec_s
{
  FAR const struct codec_ops_s *ops;
};
```

`codec_ops_s` 是下层驱动（Lower-Half）必须实现的操作回调函数集合。驱动开发者需要根据硬件能力，实例化一个 `codec_ops_s` 结构体并填充其函数指针。`codec_s` 结构体则将该操作集与驱动的私有数据绑定起来。

```C
/* 下层驱动需要实现的操作回调函数集合 */
struct codec_ops_s
{
  /* 设备生命周期管理 */
  CODE int (*open)(FAR struct codec_s *codec, void *arg);
  CODE int (*close)(FAR struct codec_s *codec);

  /* 流控制 */
  CODE int (*capture_streamon)(FAR struct codec_s *codec);
  CODE int (*output_streamon)(FAR struct codec_s *codec);
  // ... 其他 streamon/streamoff 及 available 回调 ...

  /* 标准 V4L2 IOCTLs 的具体实现 */
  CODE int (*querycap)(FAR struct codec_s *codec, FAR struct v4l2_capability *cap);
  CODE int (*capture_enum_fmt)(FAR struct codec_s *codec, FAR struct v4l2_fmtdesc *f);
  // ... 其他 ops，如 g_fmt, s_fmt, g_parm, s_parm, events, cmds 等 ...
};

/* 将 ops 与驱动私有数据绑定 */
struct codec_s
{
  FAR const struct codec_ops_s *ops;
  FAR void                     *priv;
};
```

> **说明:** `codec_ops_s` 中的许多操作是**可选**的，驱动可以根据硬件支持的功能选择性地实现。

#### `codec_file_t`

`codec_file_t` **(**`struct`**` `**`codec_file_s`**)**: **设备文件实例**，在 `open` 时创建，其 `priv` 指针用于关联下层驱动的私有数据。它是实现多实例支持的关键，每个设备节点 `open` 一次，就会创建一个新的`codec_file_t`，对应不同的 `codec context`，实现了多实例的需求。

```C
struct codec_file_s
{
  codec_type_inf_t  capture_inf; // capture queue buffer info
  codec_type_inf_t  output_inf;  // output  queue buffer info
  sq_queue_t        event_avail; // 存放可用事件单项链表
  sq_queue_t        event_free;  // 存放空闲事件单项链表
  codec_event_t     event_pool[CODEC_EVENT_COUNT]; // 事件队列
  FAR struct pollfd *fds;
  FAR void          *priv; // 存放driver的私有数据，在调用open接口时，driver可以将私有结构体指针存放在priv中，方便下次框架调用接口的时候使用
};
```

- **`codec_type_inf_t`(`struct codec_type_inf_s`)**: 用于管理单一类型（Capture 或 Output）的缓冲区信息。

    ```C
    struct codec_type_inf_s
    {
      video_framebuff_t bufinf;     /* video framebuff 队列 */
      FAR uint8_t       *bufheap;   /* for V4L2_MEMORY_MMAP buffers */
      bool              buflast;
    };
    ```

- **`codec_event_t`(`struct codec_event_s`)**: 用于订阅 `event` 和管理 V4L2 事件的内部结构。

    ```C
    struct codec_event_s
    {
      sq_entry_t        entry;
      struct v4l2_event event;
    };
    ```

#### `g_codec_fops`

`g_codec_fops` (`struct file_operations`)为 M2M 框架提供的通用全局文件操作实例接口，是一个全局静态变量。驱动注册后，`v4l2_core` 中的 `fops` 会直接调用 `codec` 的 `fops`，完成 `codec` 的 `open`/`close`/`mmap`/`poll`操作。

```C
static const struct file_operations g_codec_fops =
{
  codec_open,            /* open */
  codec_close,           /* close */
  NULL,                  /* read */
  NULL,                  /* write */
  NULL,                  /* seek */
  NULL,                  /* ioctl */
  codec_mmap,            /* mmap */
  NULL,                  /* truncate */
  codec_poll,            /* poll */
};
```

#### `g_codec_vops`

`g_codec_vops` (`struct v4l2_ops_s`)为M2M框架提供的通用全局操作实例接口，是一个全局静态变量。 实现了 V4L2 的通用 `ioctl` 命令接口。这些函数作为**适配层**，其内部会调用下层驱动在 `codec_ops_s` 中注册的对应回调函数。例如，`codec_querycap` 函数最终会调用 `(codec->ops->querycap)(...)`。

```C
/* M2M 通用层提供的 v4l2_ops_s 实现 */
static const struct v4l2_ops_s g_codec_vops =
{
  codec_querycap,                   /* querycap */
  NULL,                             /* g_input */
  NULL,                             /* enum_input */
  codec_reqbufs,                    /* reqbufs */
  codec_querybuf,                   /* querybuf */
  codec_qbuf,                       /* qbuf */
  codec_dqbuf,                      /* dqbuf */
  // ... 其他20余个已实现的接口 ...
  codec_decoder_cmd,                /* decoder_cmd */
  codec_encoder_cmd                 /* encoder_cmd */
};
```

### 4、缓冲区交互模型

V4L2 M2M 框架的核心是其双队列缓冲区模型。内存由 M2M 通用层根据用户空间的 `VIDIOC_REQBUFS` 请求进行分配和管理。下层驱动通过以下 API 与通用层进行缓冲区数据交换：

- **获取缓冲区**:

    - `codec_output_get_buf()`: 获取一个包含待处理数据（如 H.264 码流）的输入缓冲区。
    - `codec_capture_get_buf()`: 获取一个空闲的、用于存放处理结果（如 YUV 数据）的输出缓冲区。

- **归还缓冲区**:

    - `codec_output_put_buf()`: 将已处理完毕的输入缓冲区归还给 M2M 通用层。
    - `codec_capture_put_buf()`: 将已填充数据的输出缓冲区归还给 M2M 通用层，使其可被应用层读取。

```C
FAR struct v4l2_buffer *codec_output_get_buf(FAR void *cookie);
FAR struct v4l2_buffer *codec_capture_get_buf(FAR void *cookie);

int codec_output_put_buf(FAR void *cookie, FAR struct v4l2_buffer *buf);
int codec_capture_put_buf(FAR void *cookie, FAR struct v4l2_buffer *buf);
```

![img](./figures/004.png)

> **图注:** 此图详细描绘了解码器驱动如何通过 `get_buf` 和 `put_buf` API 与 M2M 通用层进行输入和输出缓冲区的交换。

### 5、开发注意事项

- **缓冲区申请:**  输入 (`output`) 和输出 (`capture`) 缓冲区均由用户空间通过 `ioctl` 的 `VIDIOC_REQBUFS` 命令触发申请，内存由 M2M 通用层统一分配和管理。
- **队列操作:**  受限于 `video_framebuff` 的当前实现，不建议一次性将所有请求的 `output` 缓冲区都入队到 M2M。推荐的模式是：在入队一个新的 `output` 缓冲区之前，先尝试出队所有已处理完的缓冲区。
- **延迟初始化:**  `sim_decoder` 示例将 `sim_openh264dec` 的初始化推迟到 `output_streamon` 回调中执行。这种做法避免了在驱动探测（probe）阶段进行不必要的硬件初始化和关闭，是一种推荐的优化实践。
- **Flush 操作:**  在调用 `output_streamoff` 时，驱动应确保硬件中缓存的所有帧都被完全处理并输出。`sim_decoder` 通过设置 flush 标志并调度工作队列来清空解码器内部的剩余数据。

## 四、参考资料

- [Linux Media Subsystem Documentation (官方)](https://www.kernel.org/doc/html/latest/userspace-api/media/index.html)