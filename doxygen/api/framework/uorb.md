# uORB API

uORB 是一种异步 publish()/subscribe() 的消息传递 API，用于进程或者线程间通信。

## 一、配置

Sensor 配置涉及驱动和 uORB 框架，所有配置项如下：

- 驱动总开关

    ```
    CONFIG_SENSORS
    ```

- 多核驱动功能开关——如果没有打开，topic 不能跨核传输和发布订阅

    ```
    CONFIG_SENSORS_RPMSG
    ```

- uORB 框架开关

    ```
    CONFIG_USENSOR
    CONFIG_UORB
    ```

- uORB listener 工具和单元测试

    ```
    CONFIG_UORB_LISTENER
    CONFIG_UORB_TESTS
    ```

- uORB 回调开关——打开后，可以通过 uorb listener 来输出每个 topic 的详细数据

    ```
    CONFIG_DEBUG_UORB
    ```

- Fakesensor 开关——从文件中获取 sensor 数据进行发布

    ```
    CONFIG_SENSORS_FAKESENSOR
    ```

- wtgahrs2 开关——Simulator 硬件传感器调试

    ```
    CONFIG_SENSORS_WTGAHRS2
    ```

- 驱动 Kconfig 位于 `drivers/sensors/Kconfig`
- uORB Kconfig 位于 `apps/system/uorb/Kconfig`

相关文件：

- uORB 头文件：`apps/system/uorb/uORB/uORB.h`
- sensor：内置传感器 topic 打印
- uORB：uORB 框架
- test：uORB 测试

## 二、使用

### 1、内置传感器列表

| 序号 | 传感器名            | 内部定义                        | 单位           | 设备路径                       |
| :--- | :------------------ | :------------------------------ | :------------- | :----------------------------- |
| 1    | Accelerometer       | SENSOR_TYPE_ACCELEROMETER       | m/s^2          | /dev/uorb/sensor_accel         |
| 2    | Magnetic Field      | SENSOR_TYPE_MAGNETIC_FIELD      | uT             | /dev/uorb/sensor_mag           |
| 3    | Gyroscope           | SENSOR_TYPE_GYROSCOPE           | radians/second | /dev/uorb/sensor_gyro          |
| 4    | Ambient Light       | SENSOR_TYPE_LIGHT               | lux            | /dev/uorb/sensor_light         |
| 5    | Barometer           | SENSOR_TYPE_BAROMETER           | hPa            | /dev/uorb/sensor_baro          |
| 6    | Proximity           | SENSOR_TYPE_PROXIMITY           | centimeters    | /dev/uorb/sensor_prox          |
| 7    | Relative Humidity   | SENSOR_TYPE_RELATIVE_HUMIDITY   | %              | /dev/uorb/sensor_humi          |
| 8    | Ambient Temperature | SENSOR_TYPE_AMBIENT_TEMPERATURE | degree Celsius | /dev/uorb/sensor_temp          |
| 9    | RGB                 | SENSOR_TYPE_RGB                 | %              | /dev/uorb/sensor_rgb           |
| 10   | Hall                | SENSOR_TYPE_HALL                | 0 or 1         | /dev/uorb/sensor_hall          |
| 11   | IR                  | SENSOR_TYPE_IR                  | lux            | /dev/uorb/sensor_ir            |
| 12   | GPS                 | SENSOR_TYPE_GPS                 | -              | /dev/uorb/sensor_gps           |
| 13   | Ultraviolet         | SENSOR_TYPE_ULTRAVIOLET         | 0-15           | /dev/uorb/sensor_uv            |
| 14   | Noise Loudness      | SENSOR_TYPE_NOISE               | dB             | /dev/uorb/sensor_noise         |
| 15   | PM2.5               | SENSOR_TYPE_PM25                | ug/m^3         | /dev/uorb/sensor_pm25          |
| 16   | PM1.0               | SENSOR_TYPE_PM1P0               | ug/m^3         | /dev/uorb/sensor_pm1p0         |
| 17   | PM10                | SENSOR_TYPE_PM10                | ug/m^3         | /dev/uorb/sensor_pm10          |
| 18   | CO2                 | SENSOR_TYPE_CO2                 | ppm            | /dev/uorb/sensor_co2           |
| 19   | HCHO                | SENSOR_TYPE_HCHO                | ppm            | /dev/uorb/sensor_hcho          |
| 20   | TVOC                | SENSOR_TYPE_TVOC                | -              | /dev/uorb/sensor_tvoc          |
| 21   | PH                  | SENSOR_TYPE_PH                  | pH             | /dev/uorb/sensor_ph            |
| 22   | Dust                | SENSOR_TYPE_DUST                | ug/m^3         | /dev/uorb/sensor_dust          |
| 23   | Heart Rate          | SENSOR_TYPE_HEART_RATE          | BPM            | /dev/uorb/sensor_hrate         |
| 24   | Heart Beat          | SENSOR_TYPE_HEART_BEAT          | -              | /dev/uorb/sensor_hbeat         |
| 25   | ECG                 | SENSOR_TYPE_ECG                 | μV             | /dev/uorb/sensor_ecg           |
| 26   | PPG Dual            | SENSOR_TYPE_PPGD                | -              | /dev/uorb/sensor_ppgd          |
| 27   | PPG Quad            | SENSOR_TYPE_PPGQ                | -              | /dev/uorb/sensor_ppgq          |
| 28   | Impedance           | SENSOR_TYPE_IMPEDANCE           | Ohm            | /dev/uorb/sensor_impd          |
| 29   | OTS                 | SENSOR_TYPE_OTS                 | -              | /dev/uorb/sensor_ots           |
| 30   | GPS Satellite       | SENSOR_TYPE_GPS_SATELLITE       | -              | /dev/uorb/sensor_gps_satellite |
| 31   | Wake Gesture        | SENSOR_TYPE_WAKE_GESTURE        | -              | /dev/uorb/sensor_wake_gesture  |
| 32   | CAP                 | SENSOR_TYPE_CAP                 | -              | /dev/uorb/cap                  |
| 33   | Gas                 | SENSOR_TYPE_GAS                 | -              | /dev/uorb/gas                  |
| 34   | Force               | SENSOR_TYPE_FORCE               | -              | /dev/uorb/sensor_force         |

详细的参数见：`nuttx/include/nuttx/sensors/sensor.h`

### 2、自定义数据类型

支持自定义 topic，可以使用 `ORB_DECLARE`、`ORB_DEFINE` 和 `ORB_ID` 定义：

```c
struct orb_test_s
{
    uint64_t timestamp;
    int32_t val;
};

static void print_orb_test_msg(FAR const struct orb_metadata *meta,
                               FAR const void *buffer)
{
    FAR const struct orb_test_s *message = buffer;
    const orb_abstime now = orb_absolute_time();

    uorbinfo_raw("%s:\ttimestamp: %"PRIu64" (%"PRIu64" us ago) val: %"PRId32"",
                 meta->o_name, message->timestamp, now - message->timestamp,
                 message->val);
}

ORB_DECLARE(orb_test);
ORB_DEFINE(orb_test, struct orb_test_s, print_orb_test_msg);
ORB_ID(orb_test_medium)
```

## 三、案例

### 1、订阅内置传感器数据

订阅 topic：

```c
struct pollfd temp_fds;
int fd = orb_subscribe(ORB_ID(sensor_temp));
temp_fds.fd = fd;
temp_fds.events = POLLIN;
```

获取数据：

```c
struct sensor_temp t;
int ret = poll(&temp_fds, 1, 500);
if (temp_fds.revents & POLLIN)
{
    orb_copy(ORB_ID(sensor_temp), fd, &t);
}
```

取消订阅：

```c
orb_unsubscribe(test_multi_sub);
```

### 2、自定义 topic

定义数据类型：

```c
struct orb_test_medium_s
{
    uint64_t timestamp;
    int32_t val;
};

static void print_orb_test_medium_msg(FAR const struct orb_metadata *meta,
                                      FAR const void *buffer)
{
    FAR const struct orb_test_s *message = buffer;
    const orb_abstime now = orb_absolute_time();

    uorbinfo_raw("%s:\ttimestamp: %"PRIu64" (%"PRIu64" us ago) val: %"PRId32"",
                 meta->o_name, message->timestamp, now - message->timestamp,
                 message->val);
}

ORB_DECLARE(orb_test_medium_s);
ORB_DEFINE(orb_test_medium_s, struct orb_test_medium_s, print_orb_test_medium_msg);
```

发布数据：

```c
struct orb_test_medium_s sample;
int instance = 0;
int fd;

sample.val = 308;
sample.timestamp = orb_absolute_time();

fd = orb_advertise_multi_queue_persist(ORB_ID(orb_test_medium),
                                       &sample, &instance, 1);
if (OK != orb_publish(ORB_ID(orb_test_medium), fd, &sample))
{
    return syslog(1, "pub orb_test_medium fail");
}

orb_unadvertise(fd);
```

订阅数据：

```c
struct orb_test_medium_s t;
struct pollfd fds[1];
int test_multi_sub;

test_multi_sub = orb_subscribe_multi(ORB_ID(orb_test_medium), 0);
orb_copy(ORB_ID(orb_test_medium), test_multi_sub, &t);
orb_unsubscribe(test_multi_sub);
```
