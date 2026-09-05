# ESP32-S3-EYE 交接适配说明

本文是 ESP32-S3-EYE 交付代码的阅读入口，按“板级初始化、NuttX 驱动、框架与应用、测试”组织内容。代码修改按仓库和功能边界分包，便于独立 review、回退和后续维护。

## 1. 适配范围

当前交付包覆盖以下板载能力：

- ST7789 LCD 与 SPI2 板级初始化
- FT5X06 触摸输入与 LVGL 输入链路
- ESP32-S3 BLE 控制器、NuttX Host、framework bttool 与广播/GATT 测试
- ES7210 音频输入、QMI8658 传感器及相关驱动注册
- media graph、播放器、录音器和异步传输生命周期
- watchdog、网络工具、串口及驱动测试基础设施

KVDB 与 MD5 不属于本交付入口，避免与已确认的功能包混淆。

## 2. 仓库与功能包

### NuttX

板级和驱动代码位于 `nuttx`：

- `boards/xtensa/esp32s3/esp32s3-eye/`：板级 GPIO、LCD、Touch、音频和启动配置
- `arch/xtensa/src/esp32s3/`：ESP32-S3 BLE、USB serial、watchdog、Wi-Fi、SD/MMC 等底层适配
- `drivers/audio/`：ES7210、ES8311 和 audio lower-half 注册
- `drivers/sensors/`：QMI8658 驱动注册
- `drivers/lcd/`、`drivers/input/`：ST7789、FT5X06 通用驱动

ESP32-S3-EYE 的板级配置使用 `CONFIG_ARCH_BOARD_ESP32S3_EYE` 及其板级配置目录。ESP32-S3-R8 使用独立的 `esp32s3-r8` 配置，不能将 R8 配置复制到 EYE 目录。

### Apps

应用侧代码位于 `apps`：

- `testing/drivers/drivertest/`：音频、I2C、LCD、Touch 和 watchdog 驱动测试
- `wireless/bluetooth/btsak/`：广播启动、停止和广播数据测试
- `system/nxcamera/`、`system/nxlooper/`：使用 `CONFIG_NSH_LINELEN` 管理命令输入缓冲
- `graphics/lvgl/`：LVGL 应用构建入口

Bluetooth 功能使用 framework 侧真实 `bttool`，不依赖 `apps` 下的替代 shim。

### Frameworks

Bluetooth framework 位于 `frameworks/connectivity/bluetooth`，包括：

- LE adapter、advertising、scan 和 GATT service 管理
- Zblue/Bluelet 栈适配和 H4 传输
- Kconfig、Makefile、CMake 构建联动
- `tools/bt_tools.c` 中的 BLE-only enable、disable、discovery 和参数检查

媒体框架位于 `frameworks/multimedia/media`，包括 audio graph 格式协商、播放器/录音器队列、PCM 缓存、socket listener 和 libuv pending 数据处理。

### External

`external` 包含 curl、FFmpeg 和 zblue 的构建联动：

- curl 的 locale 能力跟随 `CONFIG_LIBC_LOCALE`
- FFmpeg 构建阶段重新生成必要的 table
- zblue 的 PSA、TinyCrypt、HCI、广播和扫描源文件跟随 Kconfig 选择

`zblue/Makefile.3_0_1` 与 `zblue/Makefile.default` 应同步修改，避免不同构建入口产生不同源文件集合。

## 3. 关键硬件配置

ESP32-S3-EYE LCD 使用 SPI2，板级引脚配置必须与实物连线保持一致：

```text
SCK  = 11
MOSI = 5
MISO = 4
CS   = 12
DC   = 6
RST  = 8
BL   = 7
```

触摸使用 I2C0，FT5X06 地址为 `0x38`，复位脚为 GPIO9。LCD 的 SPI mode、BPP、颜色顺序、方向和偏移量由板级 defconfig 与 ST7789 Kconfig 共同决定，不应仅修改驱动默认值绕过板级配置。

## 4. 配置联动原则

- 板级 defconfig 只选择板级能力和硬件参数；通用驱动行为放在 NuttX Kconfig。
- Bluetooth 的 BLE-only 配置必须同时满足 Bluetooth、BLE support、相应 scan/advertising 和 framework/service 选项。
- media 的播放器、录音器、graph、libuv 和 FFmpeg 选项必须从同一份 defconfig 产生，不能只修改 Makefile。
- zblue 的 crypto 源文件选择必须与 `CONFIG_BT_USE_PSA_API`、`CONFIG_BT_HOST_CRYPTO` 和 mesh crypto 选项一致。
- 新增测试命令必须同时更新 apps 的 Makefile/CMake/Kconfig 注册，避免源码存在但镜像中没有命令。
- 调试配置不作为默认板级功能开关；需要验证时使用独立配置目录。

## 5. 交付与验证

主机侧使用仓库原版工具链和构建入口，不通过环境变量替换 HAL 或修改工具链行为。典型板级构建入口为：

```bash
./build.sh vendor/espressif/boards/esp32s3/esp32s3-eye/configs/nsh --cmake -e -Werror -j8
```

烧录使用项目既有的 `make -C nuttx flash` 入口，并由实际连接的串口设备确定 `ESPTOOL_PORT`。运行验证按功能包执行：先确认板级启动和设备注册，再分别验证 LCD/Touch、BLE、音频/传感器、media 和测试命令。

提交前检查以下内容：

- `git diff --check` 无空白错误
- PR 只包含对应仓库和功能范围
- 没有备份目录、生成物、临时日志或私有绝对路径
- commit message 使用英文并带 `Signed-off-by`
- 配置文件、Makefile、CMake 和源码注册路径保持一致

## 6. 维护入口

发生问题时按以下顺序定位：

1. 检查板级 defconfig 是否启用了对应能力以及正确的引脚、地址和 SPI 参数。
2. 检查板级初始化是否完成设备注册，并确认设备节点名称。
3. 检查通用驱动和 lower-half 是否被 Kconfig、Makefile、CMake 同时纳入。
4. 对 Bluetooth、media、FFmpeg 和 zblue 检查跨仓库配置是否来自同一版本的 manifest。
5. 最后再查看应用测试命令，避免将应用层现象误判为底层驱动问题。
