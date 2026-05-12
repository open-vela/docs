# LCD 驱动

\[ [English](../../../en/device_dev_guide/graphics/LCD_Driver.md) | 简体中文 \]

## 一、概述

对于分辨率要求不高的设备，为了节省内存，通常会采用 Universal mode（SPI/I2C/UART）类型接口的屏幕。在这种情况下，需要适配的主要是 LCD 驱动程序（LCD driver）。

## 二、openvela LCD 接口

openvela LCD 框架对上层用户提供了标准的 VFS 文件操作接口，用户可以通过以下方式操作 `/dev/lcd0` 设备：

- `open`：打开 LCD 设备。
- `ioctl`：执行 LCD 控制命令。
- `close`：关闭 LCD 设备。

通过这些接口，用户可以实现图形绘制和 LCD 的控制操作。

### 1、驱动层接口

在驱动层，openvela LCD 框架提供了以下三个函数，驱动开发者需要实现这些接口以适配具体的 LCD 硬件：

```C
#ifdef CONFIG_LCD
struct lcd_dev_s; /* Forward reference */

int board_lcd_initialize(void);
FAR struct lcd_dev_s *board_lcd_getdev(int lcddev);
void board_lcd_uninitialize(void);
#endif
```

1. `board_lcd_initialize`

    用于初始化 LCD 芯片，包括 SPI 初始化、LCD 寄存器配置等硬件相关操作。

2. `board_lcd_uninitialize`

    用于销毁 LCD 相关资源，例如关闭电源、释放内存等。

3. `board_lcd_getdev`

    获取 LCD 设备实例，并实现 `struct lcd_dev_s` 定义的一系列方法。该函数是 LCD 驱动的核心，开发者需要实现 `struct lcd_dev_s` 中定义的所有方法。

### 2、`struct lcd_dev_s` 结构

`struct lcd_dev_s` 是 LCD 驱动的核心结构，封装了与 LCD 控制器交互的接口方法。以下是 `struct lcd_dev_s` 的部分定义示例：

```C
struct lcd_dev_s
{
  //获取lcd controller的配置信息
  int (*getvideoinfo)(FAR struct lcd_dev_s *dev,
         FAR struct fb_videoinfo_s *vinfo);
  int (*getplaneinfo)(FAR struct lcd_dev_s *dev, unsigned int planeno,
         FAR struct lcd_planeinfo_s *pinfo);
 
#ifdef CONFIG_FB_CMAP
  //调色表
  int (*getcmap)(FAR struct lcd_dev_s *dev, FAR struct fb_cmap_s *cmap);
  int (*putcmap)(FAR struct lcd_dev_s *dev,
         FAR const struct fb_cmap_s *cmap);
#endif
 
#ifdef CONFIG_FB_HWCURSOR
  //硬件光标
  int (*getcursor)(FAR struct lcd_dev_s *dev,
        FAR struct fb_cursorattrib_s *attrib);
  int (*setcursor)(FAR struct lcd_dev_s *dev,
        FAR struct fb_setcursor_s *settings);
#endif
  //lcd 特有的控制接口
  //获得lcd的电源状态(0: full off - CONFIG_LCD_MAXPOWER: full on). 对于有背光的lcd，这个值一般是背光亮度值
  int (*getpower)(struct lcd_dev_s *dev);
  //设置lcd的电源状态(0: full off - CONFIG_LCD_MAXPOWER: full on). 对于有背光的lcd，这个值一般是背光亮度值
  int (*setpower)(struct lcd_dev_s *dev, int power);
  //获取当前对比度 (0-CONFIG_LCD_MAXCONTRAST) 
  int (*getcontrast)(struct lcd_dev_s *dev);
  //设置当前对比度 (0-CONFIG_LCD_MAXCONTRAST) 
  int (*setcontrast)(struct lcd_dev_s *dev, unsigned int contrast);
};
```

开发者可以参考以下文件中的实现：

- `boards/arm/stm32/stm32f4discovery/src/stm32_st7789.c`

该文件展示了如何实现 `struct lcd_dev_s` 的方法，并适配具体的 LCD 控制器。

## 三、启用 openvela LCD

在使用 openvela LCD 功能时，需要启用相关的编译选项，并在系统启动阶段完成初始化和注册操作。以下是具体步骤：

### 1、启用以下编译选项

在配置文件中，确保以下选项已启用：

- `CONFIG_LCD`：启用 LCD 支持。
- `CONFIG_LCD_DEV`：启用 LCD 设备支持。

### 2、系统启动阶段的调用方式

在系统启动阶段，需要调用以下函数完成 LCD 的初始化和注册：

#### 示例代码

```C
#ifdef CONFIG_LCD
 // Initialize the LCD board
 ret = board_lcd_initialize();
 if (ret < 0)
 {
 syslog(LOG_ERR, "ERROR: board_lcd_initialize() failed: %d\n", ret);
 }
#ifdef CONFIG_LCD_DEV  
    // Register the LCD device  
    ret = lcddev_register(0);  
    if (ret < 0)  
    {  
        syslog(LOG_ERR, "ERROR: lcddev_register() failed: %d\n", ret);  
    }  
#endif /* CONFIG_LCD_DEV */  
#endif /* CONFIG_LCD */
```

#### 代码说明

1. `board_lcd_initialize`
    - 用于初始化 LCD 硬件，例如 SPI 接口、LCD 控制器寄存器等。
    - 如果初始化失败，会返回负值并记录错误日志。
2. `lcddev_register`
    - 注册 LCD 设备实例，通常用于将 LCD 设备挂载到 `/dev/lcd0`。
    - 如果注册失败，会返回负值并记录错误日志。

### 3、`struct lcd_planeinfo_s` 结构

`struct lcd_planeinfo_s` 是 LCD 驱动的重要结构，定义了与 LCD 数据传输和颜色特性相关的接口和属性。

#### 示例代码

```C
struct lcd_planeinfo_s
{
  /* LCD Data Transfer */
  /* 对某一行写入npixels个数据 */
  int (*putrun)(fb_coord_t row, fb_coord_t col, FAR const uint8_t *buffer,
                size_t npixels);
  /* 更新矩形区域 */
  int (*putarea)(fb_coord_t row_start, fb_coord_t row_end,
                 fb_coord_t col_start, fb_coord_t col_end,
                 FAR const uint8_t *buffer);
  /* 读取某一行npixels个数据 */
  int (*getrun)(fb_coord_t row, fb_coord_t col, FAR uint8_t *buffer,
                size_t npixels);
  /* 读取一个矩形区域的数据 */
  int (*getarea)(fb_coord_t row_start, fb_coord_t row_end,
                 fb_coord_t col_start, fb_coord_t col_end,
                 FAR uint8_t *buffer);
  /* Plane color characteristics */
  /* 工作区，每个lcd 设备一个，多个layer共享一个buffer。至少存储一行的数据(bpp * xres/8)，要和像素格式对齐 */
  uint8_t *buffer;
  /* 一个像素占用的位数 */
  uint8_t  bpp;
};
```

#### 代码说明

**数据传输接口**

1. `putrun`
    - 向某一行写入指定数量（`npixels`）的像素数据。
2. `putarea`
    - 向指定的矩形区域写入像素数据。
3. `getrun`
    - 从某一行读取指定数量（`npixels`）的像素数据。
4. `getarea`
    - 从指定的矩形区域读取像素数据。

**Plane 颜色特性**

1. `buffer`
    - 功能：工作区缓冲区，每个 LCD 设备一个，多个图层（layer）共享一个缓冲区。
    - 要求：缓冲区至少能够存储一行的数据（`bpp * xres / 8`），并与像素格式对齐。
2. `bpp`
    - 功能：表示每个像素占用的位数（bits per pixel）。

## 四、LCD Framebuffer 模式

LCD Framebuffer 是 openvela 对 LCD 驱动程序（LCD driver）的一层 Framebuffer 封装。在启用 LCD Framebuffer 模式后，应用层可以通过 `/dev/fb0` 访问和控制 LCD 设备。需要注意的是，该模式会分配一帧图形缓存（Framebuffer），因此会消耗额外的内存空间。

参考文件：`drivers/lcd/lcd_framebuffer.c`

### 1、LCD Framebuffer 模式的核心接口

根据 [Framebuffer Driver](./Framebuffer_Driver.md) 的描述，LCD Framebuffer 驱动实现了以下三个核心接口：

- `up_fbinitialize`：初始化 Framebuffer 和 LCD 驱动。
- `up_fbgetvplane`：获取 Video Plane 信息。
- `up_fbuninitialize`：释放 Framebuffer 和相关资源。

在 `up_fbinitialize` 函数中，完成了对 LCD 驱动的初始化调用。

### 2、`up_fbinitialize` 函数实现

以下是 `up_fbinitialize` 函数的实现逻辑。

#### 示例代码

```C
int up_fbinitialize(int display)
{
  FAR struct lcdfb_dev_s *priv;
  FAR struct lcd_dev_s *lcd;
  struct fb_videoinfo_s vinfo;
  struct fb_area_s area;
  int ret;

  lcdinfo("display=%d\n", display);
  DEBUGASSERT((unsigned)display < UINT8_MAX);

  /* Allocate the framebuffer state structure */
  priv = (FAR struct lcdfb_dev_s *)kmm_zalloc(sizeof(struct lcdfb_dev_s));
  if (priv == NULL)
    {
      lcderr("ERROR: Failed to allocate state structure\n");
      return -ENOMEM;
    }

  /* Initialize the LCD-independent fields of the state structure */
  priv->display             = display;

  priv->vtable.getvideoinfo = lcdfb_getvideoinfo,
  priv->vtable.getplaneinfo = lcdfb_getplaneinfo,
#ifdef CONFIG_FB_CMAP
  priv->vtable.getcmap      = lcdfb_getcmap,
  priv->vtable.putcmap      = lcdfb_putcmap,
#endif
#ifdef CONFIG_FB_HWCURSOR
  priv->vtable.getcursor    = lcdfb_getcursor,
  priv->vtable.setcursor    = lcdfb_setcursor,
#endif
  priv->vtable.updatearea   = lcdfb_updateearea,

#ifdef CONFIG_LCD_EXTERNINIT
  /* Use external graphics driver initialization */
  lcd = board_graphics_setup(display);
  if (lcd == NULL)
    {
      gerr("ERROR: board_graphics_setup failed, devno=%d\n", display);
      ret = -ENODEV;
      goto errout_with_state;
    }
#else
  /* Initialize the LCD device */
  ret = board_lcd_initialize();
  if (ret < 0)
    {
      lcderr("ERROR: board_lcd_initialize() failed: %d\n", ret);
      goto errout_with_state;
    }

  /* Get the device instance */
  lcd = board_lcd_getdev(display);
  if (lcd == NULL)
    {
      lcderr("ERROR: board_lcd_getdev failed, devno=%d\n", display);
      ret = -ENODEV;
      goto errout_with_lcd;
    }
#endif

  priv->lcd = lcd;

  /* Initialize the LCD-dependent fields of the state structure */
  DEBUGASSERT(lcd->getvideoinfo != NULL);
  ret = lcd->getvideoinfo(lcd, &vinfo);
  if (ret < 0)
    {
      lcderr("ERROR:  LCD getvideoinfo() failed: %d\n", ret);
      goto errout_with_lcd;
    }

  priv->xres = vinfo.xres;
  priv->yres = vinfo.yres;

  DEBUGASSERT(lcd->getplaneinfo != NULL);
  ret = lcd->getplaneinfo(lcd, VIDEO_PLANE, &priv->pinfo);
  if (ret < 0)
    {
      lcderr("ERROR: LCD getplaneinfo() failed: %d\n", ret);
      goto errout_with_lcd;
    }

  /* Allocate (and clear) the framebuffer */
  priv->stride = ((size_t)priv->xres * priv->pinfo.bpp + 7) >> 3;
  priv->fblen  = priv->stride * priv->yres;

  priv->fbmem  = (FAR uint8_t *)kmm_zalloc(priv->fblen);
  if (priv->fbmem == NULL)
    {
      lcderr("ERROR: Failed to allocate frame buffer memory\n");
      ret = -ENOMEM;
      goto errout_with_lcd;
    }

  /* Add the state structure to the list of framebuffer interfaces */
  priv->flink = g_lcdfb;
  g_lcdfb     = priv;

  /* Write the entire framebuffer to the LCD */
  area.x = 0;
  area.y = 0;
  area.w = priv->xres;
  area.h = priv->yres;

  ret = lcdfb_updateearea(&priv->vtable, &area);
  if (ret < 0)
    {
      lcderr("FB update failed: %d\n", ret);
    }

  /* Turn the LCD on at 75% power */
  priv->lcd->setpower(priv->lcd, ((3*CONFIG_LCD_MAXPOWER + 3) / 4));
  return OK;

errout_with_lcd:
#ifndef CONFIG_LCD_EXTERNINIT
  board_lcd_uninitialize();
#endif

errout_with_state:
  kmm_free(priv);
  return ret;
}
```

### 3、配置选项

在 LCD Framebuffer 模式下，需要启用以下编译选项：

- `CONFIG_LCD`：启用 LCD 支持。
- `CONFIG_VIDEO_FB`：启用 Framebuffer 支持。
- `CONFIG_LCD_FRAMEBUFFER`：启用 LCD 的 Framebuffer 支持。

**注意**：在该模式下，无需启用 `CONFIG_LCD_DEV` 选项。

## 五、相关仓

- [nuttx/include/nuttx/lcd/lcd.h](../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/lcd/lcd.h)
- [nuttx/drivers/lcd/lcd_framebuffer.c](../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/lcd/lcd_framebuffer.c)
