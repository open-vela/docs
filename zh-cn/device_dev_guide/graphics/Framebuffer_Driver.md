# Framebuffer 驱动

\[ [English](../../../en/device_dev_guide/graphics/Framebuffer_Driver.md) | 简体中文 \]

## 一、什么是 Framebuffer

Framebuffer（帧缓存/显存）是一个用于存储一帧 LCD 图像数据的内存区域。在嵌入式系统中，Framebuffer 通常通过内存模拟实现，其大小由 LCD 的分辨率和每个像素的字节大小决定。

### 1、Framebuffer 的大小计算

以 480x320 的屏幕为例，在不同像素模式下，Framebuffer 的大小如下：

1. ARGB888 (32bpp)：

    - 计算公式：`480 x 320 x 4 (bytes)`
    - 大小：614,400 字节

2. RGB565 (16bpp)：

    - 计算公式：`480 x 320 x 2 (bytes)`
    - 大小：307,200 字节

## 二、Framebuffer的显示原理

Framebuffer 的显示原理可以概括为：LCD 控制器（LCDC）从 Framebuffer 中读取像素数据，并通过并行数据接口将数据传输到 LCD 面板进行显示。

### 1、显示流程图

以下是 Framebuffer 的显示流程：

![img](./figures/012.svg)

- Framebuffer：存储像素数据。
- LCDC：从 Framebuffer 中读取像素数据，并将其传输到 LCD 面板。
- LCD Panel：接收数据并显示图像。

### 2、数据传输接口

LCDC 通过以下信号将数据传输到 LCD 面板：

- Clock：时钟信号，用于同步数据传输。
- Data：像素数据，包括 R（红）、G（绿）、B（蓝）三种颜色通道。
- Control：控制信号，用于管理数据传输的时序和状态。

## 三、openvela Framebuffer 接口

openvela 的 Framebuffer 接口分为上层用户接口和下层驱动接口，分别为用户和设备驱动程序提供了灵活的操作能力。以下是接口的详细说明。

### 1、上层用户接口

openvela 的 Framebuffer 用户接口类似于 Linux 系统，通过 VFS（虚拟文件系统）提供标准操作接口，包括 `open`、`close`、`read`、`write` 和 `ioctl` 等。用户可以通过操作 `/dev/fbx` 设备文件，完成以下功能：

1. 映射 Framebuffer 到用户态：

    使用 `mmap` 将 Framebuffer 映射到用户空间，便于直接对 Framebuffer 进行读写操作。

2. 切换 Framebuffer：

    用户可以通过 `ioctl` 接口切换不同的 Framebuffer 配置或模式。

### 2、下层驱动接口

openvela 的 Framebuffer 驱动接口用于管理 LCD 设备，设计相对简单。开发者可以参考 [video/fb.h](../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/video/fb.h) 和 [/drivers/video/fb.c](../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/video/fb.c) 文件中的实现。以下是 `fb_register()` 函数的源码，展示了与 Framebuffer 设备驱动相关的重要部分：

```C
int fb_register(int display, int plane)
{
  FAR struct fb_chardev_s *fb;

  ...

  /* Initialize the frame buffer device. */
  ret = up_fbinitialize(display);
  if (ret < 0)
    {
      gerr("ERROR: up_fbinitialize() failed for display %d: %d\n",
           display, ret);
      goto errout_with_fb;
    }
  DEBUGASSERT((unsigned)plane <= UINT8_MAX);
  fb->plane  = plane;
  fb->vtable = up_fbgetvplane(display, plane);
  if (fb->vtable == NULL)
    {
      gerr("ERROR: up_fbgetvplane() failed, vplane=%d\n", plane);
      goto errout_with_fb;
    }
  /* Initialize the frame buffer instance. */
  ...

  ret = register_driver(devname, &fb_fops, 0666, (FAR void *)fb);
  if (ret < 0)
    {
      gerr("ERROR: register_driver() failed: %d\n", ret);
      goto errout_with_fb;
    }
  return OK;
  
errout_with_fb:
  kmm_free(fb);
  return ret;
}
```

从代码中可以看出，Framebuffer 针对 LCD 设备驱动程序提供了以下 3 个接口，驱动程序需要自行实现：

1. `void up_fbinitialize(int display)`

    - 用于初始化硬件 LCD 控制器。
    - 例如，在 STM32 平台上，`up_fbinitialize` 函数需要初始化 LTDC（LCD-TFT 控制器）或 MIPI 接口，并完成 DSI 外设和 LCD IC 的初始化。

2. `FAR struct fb_vtable_s *up_fbgetvplane(int display, int vplane)`

    - 获取 LCD 的 `fb_vtable_s` 结构体信息。
    - `fb_vtable_s` 是 Framebuffer 的核心结构，包含了 Framebuffer 的所有接口。通过实现该函数，LCD 控制器可以将自身信息注册到 Framebuffer 框架中。
    - 驱动程序可以参考以下示例实现：

        - `drivers/video/vnc/vnc_fbdev.c`
        - `boards/arm/stm32f7/stm32f746g-disco/stm32_lcd.c`

3. `void up_fbuninitialize(int display)`

    - 执行与 `up_fbinitialize` 相反的操作，用于释放资源。通常可以实现为空，不执行任何操作。

### 3、`struct fb_vtable_s` 结构

`fb_vtable_s` 是 Framebuffer 的核心结构，定义了与视频硬件交互的接口。以下是其主要功能模块：

1. 核心功能。

    - `getvideoinfo`：获取视频控制器配置和颜色平面信息。
    - `getplaneinfo`：获取指定颜色平面的信息。

2. 可选功能（根据配置启用）。

    - 颜色映射（`CONFIG_FB_CMAP`）：
        - `getcmap`：获取当前颜色映射表。
        - `putcmap`：更新颜色映射表。
    - 硬件光标（`CONFIG_FB_HWCURSOR`）：
        - `getcursor`：获取光标属性。
        - `setcursor`：设置光标配置。
    - 显示更新（`CONFIG_FB_UPDATE`）：
        - `updatearea`：通知硬件更新指定显示区域。
    - 垂直同步（`CONFIG_FB_SYNC`）：
        - `waitforvsync`：等待垂直同步信号，避免屏幕撕裂。
    - 叠加管理（`CONFIG_FB_OVERLAY`）：
        - `getoverlayinfo`：获取叠加层的配置信息。
        - `settransp`：设置叠加层的透明度。
        - `setchromakey`：设置叠加层的色键。
        - `setcolor`：用指定颜色填充叠加层。
        - `setblank`：启用或禁用叠加层。
        - `setarea`：设置叠加操作的活动区域。
        - 叠加层的 Blit 和 Blend 操作（`CONFIG_FB_OVERLAY_BLIT`）：
            - `blit`：在叠加层之间执行 Blit 操作。
            - `blend`：在叠加层之间执行 Blend 操作。

3. 其他控制功能。

    - 显示平移：
        - `pandisplay`：为多缓冲区显示执行平移操作。
    - 帧率控制：
        - `setframerate`：设置 Framebuffer 的刷新率。
        - `getframerate`：获取当前刷新率。
    - 电源管理：
        - `getpower`：获取面板的电源状态。
        - `setpower`：启用或禁用面板电源。

#### 示例代码

以下是 `struct fb_vtable_s` 的部分定义示例：

```C
struct fb_vtable_s
{
  /* Get information about the video controller configuration and the
   * configuration of each color plane.
   */

  int (*getvideoinfo)(FAR struct fb_vtable_s *vtable,
                      FAR struct fb_videoinfo_s *vinfo);
  int (*getplaneinfo)(FAR struct fb_vtable_s *vtable, int planeno,
                      FAR struct fb_planeinfo_s *pinfo);

#ifdef CONFIG_FB_CMAP
  /* The following are provided only if the video hardware supports RGB
   * color mapping
   */

  int (*getcmap)(FAR struct fb_vtable_s *vtable,
                 FAR struct fb_cmap_s *cmap);
  int (*putcmap)(FAR struct fb_vtable_s *vtable,
                 FAR const struct fb_cmap_s *cmap);
#endif

#ifdef CONFIG_FB_HWCURSOR
  /* The following are provided only if the video hardware supports a
   * hardware cursor.
   */

  int (*getcursor)(FAR struct fb_vtable_s *vtable,
                   FAR struct fb_cursorattrib_s *attrib);
  int (*setcursor)(FAR struct fb_vtable_s *vtable,
                   FAR struct fb_setcursor_s *settings);
#endif

#ifdef CONFIG_FB_UPDATE
  /* The following are provided only if the video hardware need extera
   * notification to update display content.
   */

  int (*updatearea)(FAR struct fb_vtable_s *vtable,
                    FAR const struct fb_area_s *area);
#endif

#ifdef CONFIG_FB_SYNC
  /* The following are provided only if the video hardware signals
   * vertical sync.
   */

  int (*waitforvsync)(FAR struct fb_vtable_s *vtable);
#endif

#ifdef CONFIG_FB_OVERLAY
  /* Get information about the video controller configuration and the
   * configuration of each overlay.
   */

  int (*getoverlayinfo)(FAR struct fb_vtable_s *vtable, int overlayno,
                        FAR struct fb_overlayinfo_s *oinfo);

  /* The following are provided only if the video hardware supports
   * transparency
   */

  int (*settransp)(FAR struct fb_vtable_s *vtable,
                   FAR const struct fb_overlayinfo_s *oinfo);

  /* The following are provided only if the video hardware supports
   * chromakey
   */

  int (*setchromakey)(FAR struct fb_vtable_s *vtable,
                      FAR const struct fb_overlayinfo_s *oinfo);

  /* The following are provided only if the video hardware supports
   * filling the overlay with a color.
   */

  int (*setcolor)(FAR struct fb_vtable_s *vtable,
                  FAR const struct fb_overlayinfo_s *oinfo);

  /* The following allows to switch the overlay on or off */

  int (*setblank)(FAR struct fb_vtable_s *vtable,
                  FAR const struct fb_overlayinfo_s *oinfo);

  /* The following allows to set the active area for subsequently overlay
   * operations.
   */

  int (*setarea)(FAR struct fb_vtable_s *vtable,
                 FAR const struct fb_overlayinfo_s *oinfo);

#ifdef CONFIG_FB_OVERLAY_BLIT
  /* The following are provided only if the video hardware supports
   * blit operation between overlays.
   */

  int (*blit)(FAR struct fb_vtable_s *vtable,
              FAR const struct fb_overlayblit_s *blit);

  /* The following are provided only if the video hardware supports
   * blend operation between overlays.
   */

  int (*blend)(FAR struct fb_vtable_s *vtable,
               FAR const struct fb_overlayblend_s *blend);
#endif

  /* Pan display for multiple buffers. */

  int (*pandisplay)(FAR struct fb_vtable_s *vtable,
                    FAR struct fb_planeinfo_s *pinfo);

  /* Specific Controls ******************************************************/

  /* Set the frequency of the Framebuffer update panel (0: disable refresh) */

  int (*setframerate)(FAR struct fb_vtable_s *vtable, int rate);

  /* Get the frequency of the Framebuffer update panel (0: disable refresh) */

  int (*getframerate)(FAR struct fb_vtable_s *vtable);

  /* Get the panel power status (0: full off). */

  int (*getpower)(FAR struct fb_vtable_s *vtable);

  /* Enable/disable panel power (0: full off). */

  int (*setpower)(FAR struct fb_vtable_s *vtable, int power);
};
```

开发者可以根据具体硬件需求实现这些接口，以满足 Framebuffer 的功能需求。

## 四、启用 Framebuffer

启用 Framebuffer 需要完成以下步骤：

### 1、开启 Framebuffer 编译选项

在配置文件中启用以下选项：

```makefile
CONFIG_VIDEO_FB  
```

### 2、注册 Framebuffer

在系统启动的初始化阶段，调用 `fb_register` 函数注册 Framebuffer。以下是示例代码：

```C
#include <nuttx/video/fb.h>  

#ifdef CONFIG_VIDEO_FB  
    ret = fb_register(0, 0);  
    if (ret < 0)  
    {  
        syslog(LOG_ERR, "ERROR fb_register() failed: %d\n", ret);  
    }  
#endif
```

### 3、处理 VSync

为了避免屏幕撕裂并提高渲染性能，建议在实现中处理 VSync（垂直同步）。VSync 的具体实现和优化方法，请参考 [VSync](./VSync.md)。

## 五、相关仓

以下是与 Framebuffer 驱动相关的代码仓库链接：

- [fb.c](../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/video/fb.c)：Framebuffer 驱动的实现文件。
- [fb.h](../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/video/fb.h)：Framebuffer 驱动的接口定义。
