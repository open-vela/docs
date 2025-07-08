# get 子命令

\[ [English](../../../../../../en/device_dev_guide/connection/bluetooth/functionality_test/AdapterBTCommands/get.md) | 简体中文 \]

## 一、简介

`get` 命令用于获取本地蓝牙适配器（Bluetooth Adapter）的属性信息。通过该命令，可以查询适配器的多种配置和状态。

## 二、语法

```Bash
get  
{  
    scanmode |  
    iocap |  
    addr |  
    leaddr |  
    name |  
    appearance |  
    class |  
    bonded <transport> |  
    connected <transport> |  
}  
```

## 三、命令

### 1、scanmode

#### 功能说明

`scanmode` 命令用于获取本地蓝牙适配器（Bluetooth Adapter）当前的扫描状态属性。扫描状态属性指示设备是否可被发现或连接。

#### 参数表

| **参数名** | **说明**                                                                                                                                | **参数类型** |
| :--------- | :-------------------------------------------------------------------------------------------------------------------------------------- | :----------- |
| scan mode  | 本地蓝牙适配器的可发现与可连接属性：<br>0：不可被发现也不可被连接。<br>1：不可被发现但可被连接。<br>2：（默认值）既可被发现也可被连接。 | 十进制整数   |

#### 示例

以下示例介绍如何获取本地蓝牙适配器的扫描状态属性。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器。启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令以获取扫描状态属性：

```Plain
bttool> get scanmode
```

##### 输出信息

```Plain
[bttool] Scan Mode:2
```

### 2、iocap

#### 功能说明

`iocap` 命令用于获取本地蓝牙适配器（Bluetooth Adapter）的输入输出（IO）能力。IO 能力决定了设备在蓝牙配对过程中支持的交互方式。

#### 参数表

| **参数名**    | **说明**                                                                                                                                                                                                                                                                                                                                                                                                  | **参数类型** |
| :------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- |
| io capability | 本地蓝牙适配器的 IO 能力：<br>0：displayonly 没有输入能力，仅能显示或传输 6 位十进制数。<br>1：yes/no 具有表示 “是” 或“ 否” 的输入机制，能够显示或传输 6 位十进制数。 <br>2：keybordonly 具有输入 “0” 到 “9”、“确认” 和 “是” “否” 的能力，不能够输出。<br>3：（默认值）no-in/no-out 无输入和输出能力。<br>4：keyboard&display 具有输入 “0” 到 “9”、确认和 “是” “否” 的能力，能够显示或传输 6 位十进制数。 | 十进制整数   |

#### 示例

以下示例介绍如何获取本地蓝牙适配器的 IO 能力。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器。启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令以获取 IO 能力：

```Plain
bttool> get iocap
```

##### 输出信息

```Plain
[bttool] IO Capability:4
```

### 3、addr

#### 功能说明

`addr` 命令用于获取本地蓝牙适配器（Bluetooth Adapter）的地址。该地址是 BR/EDR 模式下使用的唯一地址，用于标识设备。

#### 示例

以下示例介绍如何获取本地蓝牙适配器的地址。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器。启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令以获取适配器地址：

```Plain
bttool> get addr
```

##### 输出信息

```Plain
[bttool] Local Address:[xx:xx:xx:xx:xx:xx]
```

### 4、leaddr

#### 功能说明

`leaddr` 命令用于获取本地蓝牙适配器（Bluetooth Adapter）在低功耗蓝牙（LE）模式下使用的地址。该地址可以是公共地址或私有地址。

#### 示例

以下示例介绍如何获取本地蓝牙适配器在 LE 模式下使用的地址。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器。启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令以获取 LE 模式下的地址：

```Plain
bttool> get leaddr
```

##### 输出信息

```Plain
[bttool] LE Address:xx:xx:xx:xx:xx:xx, type:0
```

输出中的 `type` 表示地址类型：

- 0：公共地址（Public Address）。
- 1：私有地址（Private Address）。

### 5、name

#### 功能说明

`name` 命令用于获取本地蓝牙适配器（Bluetooth Adapter）的名称。该名称用于标识设备，通常在蓝牙设备发现过程中显示。

#### 示例

以下示例介绍如何获取本地蓝牙适配器的名称。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器。启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令以获取适配器名称：

```Plain
bttool> get name
```

##### 输出信息

```Plain
[bttool] Local Name:Xiaomiii
```

### 6、appearance

#### 功能说明

`appearance` 命令用于获取本地蓝牙适配器（Bluetooth Adapter）的外观属性。外观属性用于描述设备的类型或类别，通常在蓝牙设备发现过程中显示。

#### 示例

以下示例介绍如何获取本地蓝牙适配器的外观属性。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器。启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令以获取适配器的外观属性：

```Plain
bttool> get appearance
```

##### 输出信息

```Plain
[bttool] Le appearance:0x00c2
```

> **说明**：数字含义详见 [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/) 2.6.3 节。

### 7、class

#### 功能说明

`class` 命令用于获取本地蓝牙适配器（Bluetooth Adapter）的设备类别。设备类别用于描述蓝牙设备的功能和用途。

#### 示例

以下示例介绍如何获取本地蓝牙适配器的设备类别。

##### 前提条件

在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器。启用命令如下：

```Plain
ap> bttool
bttool> enable
```

##### 命令输入

输入以下命令以获取设备类别：

```Plain
bttool> get class
```

##### 输出信息

```Plain
[bttool] Local class of device: 0x00740704, is HEADSET: false
```

> **说明**：数字对应的类型含义详见 [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/) 2.8节。

### 8、bonded

功能说明

`bonded` 命令用于获取当前已绑定的本地蓝牙适配器（Bluetooth Adapter）信息。通过此命令，可以查看与本地蓝牙适配器建立过蓝牙连接并完成绑定的设备信息。

#### 参数表

| **参数名** | **释义**                      | **参数类型** |
| :--------- | :---------------------------- | :----------- |
| transport  | 传输模式<br>0：LE<br>1：BREDR | 十进制整数   |

#### 示例

以下示例介绍如何获取当前已绑定的本地蓝牙适配器信息，以获取 BR/EDR 模式下绑定的设备信息为例。

##### 前提条件

1. 在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器。启用命令如下：

    ```Plain
    ap> bttool
    bttool> enable
    ```

2. 此外，应确保有其他设备与本地蓝牙适配器建立过蓝牙连接并完成绑定，否则该命令无意义。

##### 命令输入

输入以下命令以获取 BR/EDR 模式下绑定的设备信息

```Plain
bttool> get bonded 1
```

##### 输出信息

> **说明**：后面输出数字对应模式已绑定设备数量。

```Plain
[bttool] device [xx:xx:xx:xx:xx:xx]
[bttool]        Name: Samsung S21
[bttool]        Alias: Samsung S21
[bttool]        Class: 0x005a020c
[bttool]        DeviceType: 1
[bttool]        IsConnected: 1
[bttool]        ACLHandle: 6
[bttool]        IsEnc: 1
[bttool]        IsBonded: 1
[bttool]        BondState: BONDED
[bttool]        IsBondInitiateLocal: 0
[bttool] bonded device cnt:1
```

### 9、connected

#### 功能说明

`connected` 命令用于获取当前已连接的设备信息。通过此命令，可以查看与本地蓝牙适配器（Bluetooth Adapter）建立连接的设备详细信息。

#### 参数表

| **参数名** | **释义**                      | **参数类型** |
| :--------- | :---------------------------- | :----------- |
| transport  | 传输模式<br>0：LE<br>1：BREDR | 十进制整数   |

#### 示例

以下示例介绍如何获取当前已连接的设备信息，以获取 LE 模式下连接的设备为例。

##### 前提条件

1. 在执行以下命令之前，请确保已通过 `bttool` 控制台启用蓝牙适配器。启用命令如下：

    ```Plain
    ap> bttool
    bttool> enable
    ```

2. 此外，应确保有其他设备与本地蓝牙适配器建立了蓝牙连接，否则该命令无意义。

##### 命令输入

```Plain
bttool> get connected 0
```

##### 输出信息

> **说明**：后面输出数字对应模式已连接设备数量。

```Plain
[bttool] device [xx:xx:xx:xx:xx:xx]
[bttool]        IsConnected: 1
[bttool]        IsEnc: 0
[bttool]        IsBonded: 0
[bttool]        BondState: BOND_NONE
[bttool]        IsBondInitiateLocal: 0
[bttool] connected device cnt:1
```
