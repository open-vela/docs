# 在 Emulator 中启用和测试 Goldfish GNSS

[ [English](../../../../../en/device_dev_guide/driver/peripheral_driver/gnss/goldfish-gnss-setup-and-test.md) | 简体中文 ]

本文档指导您如何在 openvela 的 Emulator 环境中配置、启用并测试虚拟的 Goldfish 全球导航卫星系统（GNSS, Global Navigation Satellite System）设备。

## 一、前提条件

您已经正确搭建 Emulator 仿真环境。

## 二、配置与启用

您需要完成以下配置，以确保 Goldfish GNSS 驱动能够正常加载和运行。

### 1、启用虚拟 GPS 硬件

在您的 Android 虚拟设备 (AVD) 配置文件中，您必须启用虚拟 GPS 硬件。

1. 打开 AVD 配置文件：

    ```Bash
    $HOME/.android/avd/Vela_Virtual_Device.avd/config.ini
    ```

2. 添加或修改以下配置行，确保其值为 `yes`：

    ```Bash
    hw.gps = yes
    ```

### 2、验证内核编译配置 (Kconfig)

Goldfish GNSS 驱动依赖于一系列内核配置。对于标准的 `goldfish` 目标设备，这些配置默认已启用。

您可以验证以下配置项是否存在于您的构建配置中：

```Makefile
CONFIG_GNSSUTILS_MINMEA_LIB=y
CONFIG_SENSORS=y
CONFIG_SENSORS_GOLDFISH_GNSS=y
CONFIG_SENSORS_GNSS=y
```

**说明**：这些配置项主要针对 `goldfish-arm64-v8a-ap` 和 `goldfish-armeabi-v7a-ap` 目标设备，并且默认已启用。

### 3、了解驱动初始化入口

Goldfish GNSS 驱动在系统启动时由板级支持包（BSP, Board Support Package）进行初始化。您可以在以下文件中找到驱动的入口点代码：

**文件路径**：`vendor/qemu/boards/vela/src/qemu_vela.c`

```C
#ifdef CONFIG_SENSORS_GOLDFISH_GNSS
  goldfish_gnss_init(0, 1);
#endif
```

## 三、运行时交互与测试

在成功启用 GNSS 设备后，您可以通过以下三种方式与虚拟设备交互并验证其功能。

### 方法一：通过 NuttShell (NSH) 监听 GNSS 数据

您可以使用 `uorb_listener` 工具订阅 `sensor_gnss` 这一 uORB 主题，以实时查看 GNSS 驱动发布的位置数据。

1. 在 Emulator 的 NSH 命令行中，执行以下命令：

    ```Bash
    uorb_listener -r 1 sensor_gnss
    ```

2. 观察输出。正常的输出应包含时间戳、UTC 时间、经纬度、速度等信息，如下所示：

    ```Bash
    [   18.240000] [13] [  INFO] [ap] Mointor objects num:2
    [   18.240000] [13] [  INFO] [ap] object_name:sensor_gnss, object_instance:0
    [   18.240000] [13] [  INFO] [ap] object_name:sensor_gnss, object_instance:1
    [   18.240000] [13] [ ALERT] [ap] period_us = 1000000
    [   19.010000] [13] [  INFO] [ap] sensor_gnss:   timestamp: 19010000 (0 us ago) time_utc: 1689601925 latitude: 37.4210 longitude: -121.9150
    [   19.010000] [13] [  INFO] [ap] sensor_gnss:   altitude: 0.0000 altitude_ellipsoid: 0.0000 ground_speed: 145.3254 course: 166.2700
    [   19.010000] [13] [  INFO] [ap] sensor_gnss:   eph: nan epv: nan hdop: nan vdop: nan
    [   20.020000] [13] [  INFO] [ap] sensor_gnss:   timestamp: 20020000 (0 us ago) time_utc: 1689601926 latitude: 37.4210 longitude: -121.9150
    ...
    ```

> **注意**：Emulator 中的虚拟 GNSS 设备不支持自定义数据上报间隔（interval）。默认上报间隔为 1 秒（对应控制面板中的 1X 速率）。您可以通过 Emulator 控制面板的 Playback 功能调整数据回放速率（支持 1X 至 5X），从而改变数据更新的频率。

### 方法二：通过 Emulator 图形界面交互

Emulator 提供了一个图形化的控制面板，让您可以直观地模拟定位和导航场景。

#### 模拟静态定位

1. 在 Emulator 的 **Extended Controls** -> **Location** 面板中，您可以在地图上直接选择一个点。
2. 您也可以通过 **Import GPX/KML** 按钮导入包含航点数据的文件。
3. 点击 **Set Location** 按钮，将该位置信息发送给虚拟设备。

#### 模拟导航路线

1. 在地图上选择起点和终点以规划一条路线。
2. 在 **Playback** 部分设置移动速度。
3. 点击 **Play Route** 按钮，Emulator 将沿路线模拟连续的 GNSS 数据。

### 方法三：通过 Emulator 控制台发送 GEO 命令

对于自动化测试或脚本化交互，您可以使用 `telnet` 连接到 Emulator 控制台并发送 `geo` 命令。

#### 步骤 1：获取认证令牌

> 安全提示：此令牌用于认证，请妥善保管，不要在公共文档或代码中泄露。

执行以下命令查看您的认证令牌：

```Bash
cat $HOME/.emulator_console_auth_token
```

#### 步骤 2：启动 Emulator

```Bash
./emulator.sh
```

#### 步骤 3：连接到控制台并认证

1. 使用 `telnet` 连接到 Emulator 默认的控制台端口 `5554`。
2. 使用 `auth` 命令和您获取的令牌进行认证。

    ```Bash
    telnet localhost 5554
    Trying ::1...
    telnet: connect to address ::1: Connection refused
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    Android Console: Authentication required
    Android Console: type 'auth <auth_token>' to authenticate
    Android Console: you can find your <auth_token> in
    '/Users/me/.emulator_console_auth_token'
    OK
    auth ***89ABC***
    Android Console: type 'help' for a list of commands
    OK
    ```

#### 步骤 4：发送 GEO 命令

认证成功后，您可以使用 `geo` 系列命令向虚拟设备发送 GNSS 数据。

| **命令**                    | **描述**                                         |
| :-------------------------- | :----------------------------------------------- |
| `geo nmea <sentence>`       | 发送一条原始的 NMEA 格式语句，例如 `$GPGGA,...`  |
| `geo fix <lon> <lat> [alt]` | 发送一个包含经度、纬度和可选海拔的单点定位信息。 |
| `geo gnss <payload>`        | 发送一个更复杂的 GNSS 数据负载。                 |

## 四、参考资料

- **GNSS 驱动框架**：请参阅 [GNSS 驱动框架开发指南](./gnss_driver_guide.md)。
