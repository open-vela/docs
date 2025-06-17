# LCD Driver

\[ English | [简体中文](../../../zh-cn\device_dev_guide/graphics/LCD_Driver.md) \]

## I Introduction

For devices with modest resolution requirements, Universal mode (SPI/I2C/UART) interface screens are often used to conserve memory. In such cases, the primary adaptation requirement is the LCD driver (LCD driver).

## II openvela LCD Interface

openvela's LCD framework provides standard VFS file operation interfaces to upper layers. Users can operate /`dev/lcd0` device through these methods:

- `open`: Open the LCD device.
- `ioctl`: Control the LCD device.
- `close`: Close the LCD device.

These interfaces enable users to perform graphic rendering and LCD control operations.

### 1. LCD Driver Interface

At the driver layer, openvela LCD framework provides three essential functions that developers must implement to adapt specific LCD hardware:

```C
#ifdef CONFIG_LCD
struct lcd_dev_s; /* Forward reference */

int board_lcd_initialize(void);
FAR struct lcd_dev_s *board_lcd_getdev(int lcddev);
void board_lcd_uninitialize(void);
#endif
```

1. `board_lcd_initialize`

    Used to initialize the LCD chip, including SPI initialization, LCD register configuration, etc.

2. `board_lcd_uninitialize`

    Used to destroy LCD related resources, such as power off and memory release.

3. `board_lcd_getdev`

    Get the LCD device instance and implement all the methods defined in `struct lcd_dev_s`. This is the core of the LCD driver. Developers must implement all the methods defined in `struct lcd_dev_s`.

### 2. `struct lcd_dev_s` Structure

`struct lcd_dev_s` is the core structure of the LCD driver, which encapsulates the interface methods for interacting with the LCD controller. The following is an example of part of the definition of `struct lcd_dev_s`:

```C
struct lcd_dev_s
{
  // Get the configuration information of the lcd controller
  int (*getvideoinfo)(FAR struct lcd_dev_s *dev,
          FAR struct fb_videoinfo_s *vinfo);
  int (*getplaneinfo)(FAR struct lcd_dev_s *dev, unsigned int planeno,
          FAR struct lcd_planeinfo_s *pinfo);
 
#ifdef CONFIG_FB_CMAP
  // Color table
  int (*getcmap)(FAR struct lcd_dev_s *dev, FAR struct fb_cmap_s *cmap);
  int (*putcmap)(FAR struct lcd_dev_s *dev,
          FAR const struct fb_cmap_s *cmap);
#endif
 
#ifdef CONFIG_FB_HWCURSOR
  // Cursor
  int (*getcursor)(FAR struct lcd_dev_s *dev,
      FAR struct fb_cursorattrib_s *attrib);
  int (*setcursor)(FAR struct lcd_dev_s *dev,   
     FAR struct fb_setcursor_s *settings);
#endif
 
 // The unique control interface of the LCD// Get the power status of the LCD (0: full off - CONFIG_LCD_MAXPOWER: full on). For LCDs with backlight, this value is generally the backlight brightness level.
  int (*getpower)(struct lcd_dev_s *dev);  // Power // Set the power state of the LCD (0: full off - CONFIG_LCD_MAXPOWER: full on). For LCDs with backlight, this value is generally the brightness value of the backlight.
  int (*setpower)(struct lcd_dev_s *dev, int power);   
  //Get the current contrast (0-CONFIG_LCD_MAXCONTRAST)
  int (*getcontrast)(struct lcd_dev_s *dev);  
  // Set the current contrast (0-CONFIG_LCD_MAXCONTRAST)
  int (*setcontrast)(struct lcd_dev_s *dev, unsigned int contrast);
};
```
Reference Implementation:
- `boards/arm/stm32/stm32f4discovery/src/stm32_st7789.c`

Demonstrates full implementation of `struct lcd_dev_s` methods for specific LCD controllers.

## III Enable openvela LCD

When using the openvela LCD feature, it is necessary to enable related compilation options and complete initialization and registration during the system startup phase. The following are the specific steps:

### 1. Enable the following compilation options

In the configuration file, ensure that the following options are enabled:

- `CONFIG_LCD`: Enable LCD support.
- `CONFIG_LCD_DEV`: Enable LCD device support.

### 2. System startup phase call method

In the system startup phase, call the following functions to complete the initialization and registration of the LCD:

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

##### Code description

1. `board_lcd_initialize`
    -`Used to initialize the LCD chip, including SPI initialization, LCD register configuration, etc.`
    - If initialization fails, it will return a negative value and record an error log.
2. `lcddev_register`
    - Register the LCD device instance, which is usually used to mount the LCD device to `/dev/lcd0`.
    - If registration fails, it will return a negative value and record an error log.

### 3. `struct lcd_planeinfo_s` Structure

`struct lcd_planeinfo_s` is an important structure of the LCD driver, which defines the interface and attributes related to LCD data transmission and color.

#### Example code

```C
struct lcd_planeinfo_s
{
  /* LCD Data Transfer */
  /* Write npixels of data to a certain line.*/
  int (*putrun)(fb_coord_t row, fb_coord_t col, FAR const uint8_t *buffer,
                size_t npixels);
  /* Update rectangular area */
  int (*putarea)(fb_coord_t row_start, fb_coord_t row_end,
                 fb_coord_t col_start, fb_coord_t col_end,
                 FAR const uint8_t *buffer);
  /* Read npixels data from a certain line. */
  int (*getrun)(fb_coord_t row, fb_coord_t col, FAR uint8_t *buffer,
                size_t npixels);
  /* Read the data of a rectangular area. */
  int (*getarea)(fb_coord_t row_start, fb_coord_t row_end,
                 fb_coord_t col_start, fb_coord_t col_end,
                 FAR uint8_t *buffer);
  /* Plane color characteristics */
  /* Workspace, one LCD device for each, multiple layers share a buffer. It must store at least one line of data (bpp * xres / 8), and it needs to be aligned with the pixel format. */
  uint8_t *buffer;
  /* The number of bits occupied by a pixel*/
  uint8_t  bpp;
};
```

#### Code description

##### Data transfer interface

1. `putrun`
- Write the specified number (`npixels`) of pixels to a certain line.
2. `putarea`
- Write the pixel data to the specified rectangular area.
3. `getrun`
- Read the specified number (`npixels`) of pixels from a certain line.
4. `getarea`
- Read the pixel data of the specified rectangular area.

##### Plane color characteristics

1. `buffer`
- Function: workspace buffer, one LCD device for each, multiple layers share a buffer.  
- Requirement: the buffer must be able to store one line of data (`bpp * xres / 8`), and it needs to be aligned with the pixel format.
2. `bpp`
- Function: the number of bits occupied by a pixel.

## IV LCD Framebuffer Mode

LCD Framebuffer is a framebuffer wrapper for the LCD driver in openvela. After enabling the LCD Framebuffer mode, the application layer can access and control the LCD device through `/dev/fb0`. It is important to note that this mode will allocate a frame graphic buffer (Framebuffer), which will consume additional memory space.

reference:`drivers/lcd/lcd_framebuffer.c`

### 1. Enable the following compilation options

According to the description in [Framebuffer Driver](./Framebuffer_Driver.md), the LCD Framebuffer driver implements the following three core interfaces:

-`up_fbinitialize`: Initialize the LCD Framebuffer.
-`up_fbgetvplane`: Get the Video Plane information.
-`up_fbuninitialize`: Release the Framebuffer and related resources.

In the `up_fbinitialize` function, the initialization call of the LCD driver is completed.

### 2. `up_fbinitialize` function implementation

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

### 3.Configuration Options
In LCD Framebuffer mode, the following compilation options must be enabled:

- `CONFIG_LCD`: Enable LCD support.
- `CONFIG_VIDEO_FB`: Enable Framebuffer support.
- `CONFIG_LCD_FRAMEBUFFER`: Enable LCD Framebuffer support.

> Note:
>
> - The `CONFIG_LCD_EXTERNINIT` option is not enabled by default.

## V Related code repository
[nuttx/include/nuttx/lcd/lcd.h at dev · open-vela/nuttx](../../../../nuttx/lcd/lcd.h)

[https://github.com/open-vela/nuttx/blob/dev/drivers/lcd/lcd_framebuffer.c](../../../../nuttx/drivers/lcd/lcd_framebuffer.c)
