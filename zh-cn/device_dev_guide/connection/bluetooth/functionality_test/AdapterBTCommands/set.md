# set 子命令

\[ [English](../../../../../../en/device_dev_guide/connection/bluetooth/functionality_test/AdapterBTCommands/set.md) | 简体中文 \]

## 一、简介

`set` 命令用于设置本地蓝牙适配器（Bluetooth Adapter）的属性。通过该命令，可以配置蓝牙设备的扫描模式、名称、设备类别等属性。

## 二、语法

以下是 `set` 命令的语法结构：

```Bash
set  
{  
    scanmode <scan mode> |  
    iocap <io capability> |  
    name <local name> |  
    class <local class of device> |  
    appearance <appearance> |  
    leaddr <leaddr> |  
    id <identity addr> <addr type> |  
    scanparams <mode> <type> <interval> <window>  
}
```

## 三、命令

### 1、scanmode

#### 功能说明

`scanmode` 用于设置本地蓝牙适配器（Bluetooth Adapter）的扫描状态属性，从而控制 BR/EDR 控制器是否定期尝试 Page Scan 并响应来自其他设备的 Inquiry。通过该命令，可以设置本地蓝牙适配器的可连接和可发现属性。

#### 参数表

| **参数名**  | **说明**                                                     | **参数类型** |
| :---------- | :----------------------------------------------------------- | :----------- |
| scan mode | 本地蓝牙适配器的可发现与可连接属性：<br>0：不可被发现也不可被连接。<br>1：不可被发现但可被连接。<br>2：（默认值）既可被发现也可被连接。 | 十进制整数   |

#### 示例

以下示例介绍设置本地蓝牙适配器为可被连接的状态。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器（Adapter）。 启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令设置扫描模式为 `1`（不可被发现但可被连接）：

```Plain
bttool> set scanmode 1
```

##### 输出信息

预期结果如下：

```Plain
[bttool] Scan Mode:1 set success
```

### 2、iocap

#### 功能说明

`iocap` 用于设置本地蓝牙适配器（Bluetooth Adapter）的输入输出能力（IO Capability）。IO 能力决定了本地蓝牙适配器在配对时采用的验证方法。

#### 参数表

| **参数名**      | **说明**                                                     | **参数类型** |
| :-------------- | :----------------------------------------------------------- | :----------- |
| io capability | 本地蓝牙适配器的 IO 能力：<br>0：displayonly 没有输入能力，仅能显示或传输 6 位十进制数。<br>1：yes/no 具有表示 “是” 或“ 否” 的输入机制，能够显示或传输 6 位十进制数。 <br>2：keybordonly 具有输入 “0” 到 “9”、“确认” 和 “是” “否” 的能力，不能够输出。<br>3：（默认值）no-in/no-out 无输入和输出能力。<br>4：keyboard&display 具有输入 “0” 到 “9”、确认和 “是” “否” 的能力，能够显示或传输 6 位十进制数。 | 十进制整数   |

#### 示例

以下示例介绍如何将本地蓝牙适配器的 IO 能力设置为 `displayonly`。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器（Adapter）。 启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令设置 IO 能力为 `0`（displayonly）：

```Plain
bttool> set iocap 0
```

##### 输出信息

预期结果如下：

```Plain
[bttool] IO Capability:0 set success
```

其中，数字 `0` 对应 `displayonly` 这一 IO 能力。

### 3、name

功能说明

`name` 用于设置本地蓝牙适配器（Bluetooth Adapter）的名称。该名称是向对端蓝牙设备公开的用户友好名称。

#### 参数表

| **参数名**   | **说明**             | **参数类型** | **参数值范围**       | **默认值** |
| :----------- | :------------------- | :----------- | :------------------- | :--------- |
| local name | 本地蓝牙适配器名称。 | 字符串       | 最多输入 64 个字符。 | N/A        |

#### 示例

以下示例介绍如何将本地蓝牙适配器的名称设置为 `Xiaomiii`。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器（Adapter）。 启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令设置本地蓝牙适配器名称为 `Xiaomiii`：

```Plain
bttool> set name Xiaomiii
```

##### 输出信息

预期结果如下：

```Plain
[bttool] Local Name:Xiaomiii set success
bttool> [bttool] Adapter update device name: Xiaomiii
```

### 4、class

#### 功能说明

`class` 用于设置本地蓝牙适配器（Bluetooth Adapter）的设备类别。设备类别由主服务类型、主设备类型、次要设备类型和固定值组成，用于标识蓝牙设备的功能和用途。

#### 参数表

| **参数名** | **说明**                                                     | **参数类型** | **默认值** |
| :--------- | :----------------------------------------------------------- | :----------- | :--------- |
| class    | 本地蓝牙适配器类型，由 4 个部分组成。<br>bit 23~13 ：主服务类型。<br>bit 12~8：主设备类型。<br>bit 7~2：次要设备类型。<br>bit 1~0：固定值 0。 | 十六进制整数 | 0x00280704 |

#### 注意事项

- 输入限制：由于输入参数的 bit 1 和 bit 0 应当保持为 0，因此输入的十六进制整数的最后 1 位数字应为 `{ 0 | 4 | 8 | c }`。
- 参考标准：设备类别的具体值请参考 Bluetooth SIG 的 [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/) 文档第 2.8 节。

#### 示例

以下示例介绍如何将本地蓝牙适配器的类别设置为“可穿戴腕表”。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器（Adapter）。 启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

根据 [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/) 文档：

- 主设备类型“可穿戴”表示为 `0b00111`。
- 次要设备类型“腕表”表示为 `0b000001`。
- 支持的服务包括 Telephony、Audio、Object Transfer 和 Rendering，表示为 `0b01110100000`。
- 最终设备类型为 `0b011101000000011100000100`，转换为十六进制数为 `0x740704`。

输入以下命令设置设备类别：

```Plain
bttool> set class 740704
```

##### 输出信息

预期结果如下：

```Plain
[bttool] Local class of device:0x00740704 set success
```

### 5、appearance

#### 功能说明

`appearance` 用于设置本地蓝牙适配器（Bluetooth Adapter）的外观属性。外观属性用于描述设备的类型和子类型，通常在低功耗蓝牙（LE）模式下使用。

#### 参数表

| **参数名** | **说明**                                                                                                                                                                                           | **参数类型** | **默认值** |
| :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- | :--------- |
| appearance | LE 模式下本地蓝牙适配器的外观，由两部分组成：<br>bit 16~6：分类。<br>bit 5~0：子类。<br>16 bits 参数详见 [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/) 2.6.3 节。 | 十六进制整数 | 0          |

#### 示例

以下示例介绍如何将本地蓝牙适配器的外观设置为 Smart Watch。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器（Adapter）。 启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

根据 [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/) 文档，Smart Watch 的外观参数值为 `0x00C2`。 输入以下命令设置外观属性：

```Plain
bttool> set appearance c2
```

##### 输出信息

预期结果如下：

```Plain
[bttool] Set Le appearance:0x00c2
```

### 6、leaddr

#### 功能说明

`leaddr` 用于设置本地蓝牙适配器（Bluetooth Adapter）在低功耗蓝牙（LE）模式下使用的私有地址（LE 随机地址的一种）。

在 LE 模式下，蓝牙设备可以使用公共地址（Public Address）或随机地址（Random Address）标识设备。随机地址进一步分为静态地址（Static Address）和私有地址（Private Address）。

- 随机地址类型由地址的 bit 47~46 指示，其余位为随机部分。

- 地址类型说明：

    | **bit 47~46** | **类型**           |
    | :------------ | :----------------- |
    | 0b00          | 不可解析私有地址。 |
    | 0b01          | 可解析私有地址。   |
    | 0b10          | 保留。             |
    | 0b11          | 静态地址。         |

#### 地址类型说明

1. 公共地址：

    - 唯一地址，需要向 IEEE 申请分配。
    - 在 BR/EDR 与 LE 双模情况下，通常与 BR/EDR 使用的地址相同。

2. 静态地址：

    - 随机生成，不具有唯一性，仅在开机初始化时生成。
    - 随机部分不能全为 `0` 或全为 `1`。

3. 私有地址：

    - 随机生成，不具有唯一性，每次连接或特定时间后更新。
    - 不可解析私有地址：随机部分不能全为 `0` 或全为 `1`，且不能等于公共地址。
    - 可解析私有地址：低 24 bits 需要采用特定的生成算法。

#### 参数表

| **参数名** | **说明**                                                                                       | **参数类型** | **默认值** |
| :--------- | :--------------------------------------------------------------------------------------------- | :----------- | :--------- |
| leaddr     | 本地蓝牙适配器在 LE 模式下使用的私有地址。<br>格式为 `XX:XX:XX:XX:XX:XX`，需满足私有地址规定。 | 字符串       | N/A        |

#### 示例

以下示例介绍如何将本地蓝牙适配器的 LE 地址设置为 `01:02:03:04:05:06`。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器（Adapter）。 启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令设置 LE 地址：

```Plain
bttool> set leaddr 01:02:03:04:05:06
```

##### 输出信息

预期结果如下：

```Plain
bttool> [   80.646100] [49] [ DEBUG] [ap] [1362][adapter-svc]: adapter_on_le_addr_update
```

### 7、id

#### 功能说明

`id` 用于设置本地蓝牙适配器（Bluetooth Adapter）在低功耗蓝牙（LE）模式下使用的静态地址（Static Address）或公共地址（Public Address）。

> 注意：当前功能暂不支持。

#### 参数表

| **参数名**    | **说明**                                                                           | **参数类型** | **默认值** |
| :------------ | :--------------------------------------------------------------------------------- | :----------- | :--------- |
| identity addr | 本地蓝牙适配器在 LE 模式下使用的公共地址或静态地址。<br>格式为 `XX:XX:XX:XX:XX:XX` | 字符串       | N/A        |
| addr type     | 地址类型：<br>0：Static address<br>1：Public address                               | 十进制整数   | 1          |

### 8、scanparam

#### 功能说明

`scanparam` 用于设置本地蓝牙适配器在指定扫描模式下使用的扫描参数。

#### 参数表

| **参数名** | **说明**                                                     | **参数类型** | **默认值**              |
| :--------- | :----------------------------------------------------------- | :----------- | :---------------------- |
| mode     | 指定的扫描模式：<br>0：inquiry，扫描 inquiry 信息，使本地蓝牙适配器可被其他蓝牙设备发现。<br>1：page，扫描 page 信息，使本地蓝牙适配器可被其他蓝牙设备连接。 | 十进制整数   | N/A                     |
| type     | 扫描类型：<br>0：standard，常规扫描，按照固定间隔逐个信道扫描。<br>1：interlaced，交错扫描，会在一次扫描间隔中，第一次按照常规扫描进行扫描，再根据特定的算法选择第二个信道进行扫描。 | 十进制整数   | N/A                     |
| interval | 扫描间隔，进入扫描状态的周期。<br>18 ~ 4096（单位：时隙，1 时隙 = 0.625ms） | 十进制整数   | inquiry：4096<br>page：2048 |
| window   | 扫描窗口，在一个周期内持续扫描的时间。17 ~ `<interval>`（单位：时隙） | 十进制整数   | 18                      |

#### 注意事项

- 时隙单位：1 个时隙为 0.625ms。
- Interlaced Scan 限制：如果 `<interval>` 不是 `<window>` 的两倍以上，则不能使用 Interlaced Scan。

#### 示例

以下示例介绍如何设置一组扫描参数。以设置扫描间隔为 1.28 秒，扫描窗口为 31.25 毫秒的标准 Inquiry Scan 为例。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器（Adapter）。 启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

- Inquiry Scan 对应 `<mode>` 为 `0`。
- Standard Scan 对应 `<type>` 为 `0`。
- 扫描间隔 1.28 秒对应 `1280 / 0.625 = 2048` 时隙。
- 扫描窗口 31.25 毫秒对应 `31.25 / 0.625 = 50` 时隙。

```Plain
bttool> set scanparams 0 0 2048 50
```

##### 输出信息

此命令无输出信息。
