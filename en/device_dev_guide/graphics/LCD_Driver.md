# LCD Driver

\[ English | [简体中文](../../../zh-cn/device_dev_guide/graphics/LCD_Driver.md) \]

## I. Overview

For devices that do not require high resolution, screens with Universal mode (SPI/I2C/UART) interfaces are often used to save memory. In this case, the main component that needs to be adapted is the LCD driver.

## II. openvela LCD Interface

The openvela LCD framework provides standard VFS file operation interfaces to upper-layer users, who can operate the `/dev/lcd0` device through the following:

- `open`: Opens the LCD device.
- `ioctl`: Executes LCD control commands.
- `close`: Closes the LCD device.

Through these interfaces, users can perform graphics drawing and LCD control operations.

### 1. Driver-Layer Interface

At the driver layer, the openvela LCD framework provides the following three functions, which driver developers need to implement to adapt to specific LCD hardware:

```C
#ifdef CONFIG_LCD
struct lcd_dev_s; /* Forward reference */

int board_lcd_initialize(void);
FAR struct lcd_dev_s *board_lcd_getdev(int lcddev);
void board_lcd_uninitialize(void);
#endif
```

1. `board_lcd_initialize` is used to initialize the LCD chip, including SPI initialization, LCD register configuration, and other hardware-related operations.
2. `board_lcd_uninitialize` is used to destroy LCD-related resources, such as turning off the power and freeing memory.
3. `board_lcd_getdev` gets the LCD device instance and implements a series of methods defined by `struct lcd_dev_s`. This function is the core of the LCD driver, and developers need to implement all methods defined in `struct lcd_dev_s`.

### 2. `struct lcd_dev_s` Structure

`struct lcd_dev_s` is the core structure of the LCD driver, which encapsulates the interface methods for interacting with the LCD controller. The following is a partial definition of `struct lcd_dev_s`:

```C
struct lcd_dev_s
{
  // Get the LCD controller's configuration information
  int (*getvideoinfo)(FAR struct lcd_dev_s *dev,
         FAR struct fb_videoinfo_s *vinfo);
  int (*getplaneinfo)(FAR struct lcd_dev_s *dev, unsigned int planeno,
         FAR struct lcd_planeinfo_s *pinfo);
 
#ifdef CONFIG_FB_CMAP
  // Color map
  int (*getcmap)(FAR struct lcd_dev_s *dev, FAR struct fb_cmap_s *cmap);
  int (*putcmap)(FAR struct lcd_dev_s *dev,
         FAR const struct fb_cmap_s *cmap);
#endif
 
#ifdef CONFIG_FB_HWCURSOR
  // Hardware cursor
  int (*getcursor)(FAR struct lcd_dev_s *dev,
        FAR struct fb_cursorattrib_s *attrib);
  int (*setcursor)(FAR struct lcd_dev_s *dev,
        FAR struct fb_setcursor_s *settings);
#endif
  // LCD-specific control interfaces
  // Get the LCD's power state (0: full off - CONFIG_LCD_MAXPOWER: full on). For LCDs with backlights, this value is typically the backlight brightness.
  int (*getpower)(struct lcd_dev_s *dev);
  // Set the LCD's power state (0: full off - CONFIG_LCD_MAXPOWER: full on). For LCDs with backlights, this value is typically the backlight brightness.
  int (*setpower)(struct lcd_dev_s *dev, int power);
  // Get the current contrast (0-CONFIG_LCD_MAXCONTRAST) 
  int (*getcontrast)(struct lcd_dev_s *dev);
  // Set the current contrast (0-CONFIG_LCD_MAXCONTRAST) 
  int (*setcontrast)(struct lcd_dev_s *dev, unsigned int contrast);
};
```

Developers can refer to the implementation in the following file:

- `boards/arm/stm32/stm32f4discovery/src/stm32_st7789.c`

This file demonstrates how to implement the methods of `struct lcd_dev_s` and adapt it to a specific LCD controller.

## III. Enabling openvela LCD

To use the openvela LCD functionality, you need to enable the relevant build options and perform initialization and registration during the system startup phase. Here are the specific steps:

### 1. Enable the following build options

In the configuration file, ensure the following options are enabled:

- `CONFIG_LCD`: Enable LCD support.
- `CONFIG_LCD_DEV`: Enable LCD device support.

### 2. System Startup Invocation

During the system startup phase, the following functions need to be called to complete the LCD initialization and registration:

#### Example code

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

##### Code Explanation

1. `board_lcd_initialize`

    - Initializes the LCD hardware, such as the SPI interface and LCD controller registers.
    - If initialization fails, it returns a negative value and logs an error.

2. `lcddev_register`

    - Registers the LCD device instance, typically mounting it to `/dev/lcd0`.
    - If registration fails, it returns a negative value and logs an error.

### 3. `struct lcd_planeinfo_s` Structure

`struct lcd_planeinfo_s` is an important structure in the LCD driver, defining the interfaces and attributes related to LCD data transfer and color characteristics.

#### Example code

```C
struct lcd_planeinfo_s
{
  /* LCD Data Transfer */
  /* Write npixels of data to a specific row */
  int (*putrun)(fb_coord_t row, fb_coord_t col, FAR const uint8_t *buffer,
                size_t npixels);
  /* Update a rectangular area */
  int (*putarea)(fb_coord_t row_start, fb_coord_t row_end,
                 fb_coord_t col_start, fb_coord_t col_end,
                 FAR const uint8_t *buffer);
  /* Read npixels of data from a specific row */
  int (*getrun)(fb_coord_t row, fb_coord_t col, FAR uint8_t *buffer,
                size_t npixels);
  /* Read data from a rectangular area */
  int (*getarea)(fb_coord_t row_start, fb_coord_t row_end,
                 fb_coord_t col_start, fb_coord_t col_end,
                 FAR uint8_t *buffer);
  /* Plane color characteristics */
  /* Workspace buffer, one per LCD device, shared by multiple layers. It must store at least one row of data (bpp * xres / 8) and be aligned with the pixel format. */
  uint8_t *buffer;
  /* Bits per pixel */
  uint8_t  bpp;
};
```

#### Code Explanation

**Data transfer interface**

1. `putrun`

    - Write the specified number (`npixels`) of pixels to a certain line.

2. `putarea`

    - Write the pixel data to the specified rectangular area.

3. `getrun`

    - Read the specified number (`npixels`) of pixels from a certain line.

4. `getarea`

    - Read the pixel data of the specified rectangular area.

**Plane color characteristics**

1. `buffer`

    - Function: workspace buffer, one LCD device for each, multiple layers share a buffer.  
    - Requirement: the buffer must be able to store one line of data (`bpp * xres / 8`), and it needs to be aligned with the pixel format.

2. `bpp`

    - Function: the number of bits occupied by a pixel.

## IV. LCD Framebuffer Mode

LCD Framebuffer is a framebuffer wrapper provided by openvela for the LCD driver. When LCD Framebuffer mode is enabled, the application layer can access and control the LCD device through `/dev/fb0`. It's important to note that this mode allocates a full graphics buffer (framebuffer), which consumes additional memory.

Reference file: `drivers/lcd/lcd_framebuffer.c`

### 1. Core Interfaces for LCD Framebuffer Mode

According to the description in [Framebuffer Driver](./Framebuffer_Driver.md), the LCD Framebuffer driver implements the following three core interfaces:

- `up_fbinitialize`: Initialize the LCD Framebuffer.
- `up_fbgetvplane`: Get the Video Plane information.
- `up_fbuninitialize`: Release the Framebuffer and related resources.

In the `up_fbinitialize` function, the initialization call of the LCD driver is completed.

### 2. `up_fbinitialize` Function Implementation

The following is the implementation logic of the `up_fbinitialize` function.

#### Example code

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

### 3. Configuration Options

In LCD Framebuffer mode, you need to enable the following build options:

- `CONFIG_LCD`: Enable LCD support.
- `CONFIG_VIDEO_FB`: Enable framebuffer support.
- `CONFIG_LCD_FRAMEBUFFER`: Enable framebuffer support for the LCD.

**Note**: In this mode, you do not need to enable the `CONFIG_LCD_DEV` option.

## V. Related Repositories

- [nuttx/include/nuttx/lcd/lcd.h](../../../../../../nuttx/blob/dev-ai-contest-2026/include/nuttx/lcd/lcd.h)

- [nuttx/drivers/lcd/lcd_framebuffer.c](../../../../../../nuttx/blob/dev-ai-contest-2026/drivers/lcd/lcd_framebuffer.c)
