# 适配 I2C Bit-Banging 驱动

[ [English](../../../../../en/device_dev_guide/driver/bus_driver/I2C/i2c_bitbang_guide.md) | 简体中文 ]

Bit-banging 是一种使用通用输入输出（GPIO）引脚来模拟 I2C 协议时序的技术。当芯片的硬件 I2C 控制器数量不足，或需要使用非标准的引脚组合时，此方法非常有用。

> **性能警告**：Bit-banging 完全由 CPU 通过软件循环来控制 GPIO 电平，为保证时序精确，通常需要在关键代码路径中**关闭中断**。这会增加系统中断延迟，可能影响系统的实时性能。因此，在有硬件 I2C 控制器可用的情况下，应优先使用硬件方式。

## 一、适配南向接口

Bit-banging 的南向适配非常简单，仅需实现一组 GPIO 操作函数。

### 1、Kconfig 配置项

```Makefile
CONFIG_I2C=y
CONFIG_I2C_BITBANG=y 
```

### 2、实现步骤

适配的核心是提供一个 `struct i2c_bitbang_lower_ops_s` 结构体的实例，并调用 `i2c_bitbang_initialize()` 将其与上层通用驱动“粘合”起来。

- 参考实现：[cxd56_i2cdev_bitbang.c](https://github.com/apache/nuttx/blob/master/boards/arm/cxd56xx/common/src/cxd56_i2cdev_bitbang.c)

#### 步骤一：实现 GPIO 操作函数集

开发者需要提供一个 `struct i2c_bitbang_lower_ops_s` 结构体的实例，其中包含了对 GPIO 的底层操作函数。

<details>
<summary>点击展开代码</summary>

```C
struct i2c_bitbang_lower_ops_s
{
  /* Initialize pins to appropriate state (usually open-drain) */

  CODE void (*initialize)(FAR struct i2c_bitbang_lower_dev_s *lower);

  /* Set high/low level for SCL/SDA pins */

  CODE void (*set_scl)(FAR struct i2c_bitbang_lower_dev_s *lower, bool high);
  CODE void (*set_sda)(FAR struct i2c_bitbang_lower_dev_s *lower, bool high);

  /* Read level of SCL/SDA pins */

  CODE bool (*get_scl)(FAR struct i2c_bitbang_lower_dev_s *lower);
  CODE bool (*get_sda)(FAR struct i2c_bitbang_lower_dev_s *lower);
};
```

</details>

#### 步骤二：实现初始化函数

在板级代码中，填充 `i2c_bitbang_lower_dev_s` 结构，然后调用 `i2c_bitbang_initialize()` 来获取一个标准的 `i2c_master_s` 句柄。

<details>
<summary>点击展开代码</summary>

```C
static const struct i2c_ops_s g_i2c_ops =
{
  i2c_bitbang_transfer  /* transfer */
#ifdef CONFIG_I2C_RESET
  , NULL                /* reset */
#endif
};

struct i2c_bitbang_lower_dev_s
{
  FAR const struct i2c_bitbang_lower_ops_s *ops;
  FAR void *priv;
};

FAR struct i2c_master_s *i2c_bitbang_initialize(
    FAR struct i2c_bitbang_lower_dev_s *lower)
 {
      dev->i2c.ops = &g_i2c_ops;
      dev->lower = lower;
      dev->lower->ops->initialize(dev->lower);

      return &dev->i2c;
 }
```

</details>

## 二、北向应用层使用

Bit-bang 驱动生成的 `i2c_master_s` 句柄与硬件 Master 驱动的句柄**完全兼容**。您可以：

1. **内核驱动直接使用**：在板级初始化代码中获取到 `i2c_master_s` 句柄后，直接传递给需要它的其他内核驱动（如传感器驱动）。这是最常见的用法。
2. **注册为用户空间设备**：调用 `i2c_register()` 函数，将该句柄注册为 `/dev/i2c-N` 设备节点，供用户空间程序通过 `ioctl` 访问。这在需要使用 `i2ctool` 等命令行工具进行调试时非常有用。

## 三、验证与测试

- 请参考 [I2C 驱动的验证与调试](./i2c_verification_guide.md)来测试您的驱动。
