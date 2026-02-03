# openvela VS Code 插件使用指南

[ [English](../../en/quickstart/vscode_plugin_usage.md) | 简体中文 ]

本文档指导开发者在 Ubuntu 环境下安装 openvela VS Code 插件，并完成 openvela 项目的创建、编译、调试及应用开发。

## 一、环境准备

在开始之前，请确保开发环境满足以下软硬件要求。

### 1、硬件配置

- **硬盘**：至少 **40 GB** 可用空间（用于存放源代码及编译产物）。
- **内存**：至少 **16** **GB** RAM。

### 2、操作系统

- **系统版本**：Ubuntu 22.04 (支持 arm64 或 x86_64 架构)。

## 二、安装 openvela 扩展插件

> **注意**：调试功能依赖 C++ 插件，因此必须在 VS Code 中进行安装和运行。

在 VS Code(版本 >= 1.99.0)扩展市场搜索并安装 。

- vela.vs-aiot-ide-vela

    <img src="./figures//010.png" alt="" width="75%">

- vela.vela-preview

    <img src="./figures/011.png" alt="" width="75%">

## 三、配置与验证环境

插件安装完成后，需检查开发环境并安装必要的构建工具链和依赖包。

### 1、检查并安装依赖

参考下图，在 VS Code 中执行环境检查。如提示缺少组件，请按照向导提示进行安装。

<img src="./figures/012.png" alt="" width="75%">

### 2、验证环境就绪

当所有依赖安装成功后，界面将显示如下内容，表明环境准备就绪：

<img src="./figures/013.png" alt="" width="75%">

## 四、创建 openvela 项目

### 1、初始化项目目录

在文件系统中创建一个新目录（例如 `openvela`）。

> **警告**：请确保该目录的**绝对路径**中**不包含中文字符或空格等特殊符号**，否则会导致编译系统（Build System）报错。

### 2、获取源代码

1. 在 VS Code 中，参考下图步骤打开“创建项目”向导。

    <img src="./figures/014.png" alt="" width="75%">

2. 配置项目参数：

    - 选择源：根据网络情况选择合适的仓库源。
    - 选择分支：选择合适分支分支。

        - trunk (主干稳定分支)：经全面测试的稳定版本，`dev` 分支的稳定功能会合并于此。推荐大多数追求稳定性的用户使用。
        - dev (开发分支)：汇集了最新的功能与修复，可能不稳定。推荐给希望体验新功能或参与贡献的开发者。

    - 下载方式：选择 SSH 或 HTTPS。

        说明：若选择 SSH 方式，请确保已在对应代码托管平台配置 SSH Key（可点击界面中的蓝色链接查看详细文档）。

3. 选择第一步创建的项目目录 `openvela`，单击右上角 **Select**，如下图所示：

    <img src="./figures/015.png" alt="" width="75%">

4. 等待项目创建完成，下载进度如下图所示： 

    **注意**：下载源码过程耗时较长，请防止电脑进入休眠状态。

    <img src="./figures/016.png" alt="" width="75%">

### 3、配置编译参数

1. 打开创建完成的 `openvela` 目录：

    <img src="./figures/017.png" alt="" width="75%">

2. 点击左侧 openvela **帆船**图标，然后点击**配置 (Configure)** 按钮，如下图所示：

    <img src="./figures/018.png" alt="" width="75%">

3. 选择相应的 `defconfig` 文件及其它可选参数：

    <img src="./figures/019.png" alt="" width="75%">

## 五、编译与运行

### 1、编译项目

1. 点击**编译（Build）**按钮，等待构建系统完成编译：

    <img src="./figures/020.png" alt="" width="75%">

2. 编译完成效果如下图所示：

    <img src="./figures/021.png" alt="" width="75%">

### 2、运行模拟器

1. 点击**运行 (Run)** 按钮，启动模拟器：

    <img src="./figures/022.png" alt="" width="75%">

2. 在模拟器终端输入 `lvgldemo`，启动 openvela 演示应用：

    <img src="./figures/023.png" alt="" width="75%">

    <img src="./figures/024.png" alt="" width="75%">

## 六、调试应用

1. 单击**调试（Debug）**按钮，系统将启动模拟器并挂载调试进程：

    <img src="./figures/025.png" alt="" width="75%">

2. 打开源代码文件 `apps/system/ping/ping.c`，在 `main` 函数处设置断点：

    <img src="./figures/026.png" alt="" width="75%">

3. 在模拟器终端执行 `ping` 命令。系统将运行 Ping 应用并自动命中断点，进入调试模式。

    <img src="./figures/027.png" alt="" width="75%">

## 七、开发原生应用

### 1、创建应用

1. 在插件界面点击**创建原生应用（Create Native App）：**

    <img src="./figures/028.png" alt="" width="75%">

2. 选择应用模板：

    <img src="./figures/029.png" alt="" width="75%">

3. 输入项目名称（例如 `Whackmole1`）：

    <img src="./figures/030.png" alt="" width="75%">

### 2、编译与运行新应用

1. 创建完成后，VS Code 会自动定位到新应用的源代码目录。

    <img src="./figures/031.png" alt="" width="75%">

2. 重新执行**编译 (Build)** -> **运行 (Run)**。
3. 在模拟器终端输入应用名称（如 `Whackmole1`）启动新应用。

## 八、资源管理与可视化预览

openvela 插件提供了强大的可视化预览功能，支持图片、字体和二进制资源，并支持模拟器文件系统挂载。

<video src="./videos/plugin.mp4" controls="controls" width="100%"></video>

### 1、挂载数据卷

首次使用 `openvela` 仓库时，系统会自动弹出终端执行挂载命令，将 `vela_data.bin` 挂载到本地目录。

<video src="./videos/mount.mp4" controls="controls" width="100%"></video>

开发者可通过右键菜单手动管理挂载状态：

- 挂载 openvela：执行挂载。

    <img src="./figures/032.png" alt="" width="75%">

    <img src="./figures/033.png" alt="" width="75%">

- 重新挂载 openvela：当模拟器中文件发生变化（例如执行了 `adb push`）时，需执行此操作以刷新文件系统。

    <img src="./figures/034.png" alt="" width="75%">

- 卸载 openvela：断开挂载连接。

### 2、文件预览

支持普通图片、`.bin`、`.ttf` 等格式的预览（支持绝对路径与相对路径）。

<img src="./figures/035.png" alt="" width="75%">

### 3、悬浮 (Hover) 预览

**代码资源预览**：鼠标悬停在资源路径字符串上时，将显示资源缩略图。

<img src="./figures/036.png" alt="" width="75%">

<img src="./figures/037.png" alt="" width="75%">

### 4、调试时变量预览

在调试模式下，鼠标悬停在变量上可获取当前值并进行预览。

> **操作技巧**：按住 `Alt` 键可在“调试值悬浮显示”和“普通资源悬浮显示”之间切换。

<img src="./figures/038.png" alt="" width="75%">

<img src="./figures/039.png" alt="" width="75%">

### 5、配置预览基准目录

1. 点击 VS Code 的**设置 (Settings)** 按钮（或使用快捷键 `Ctrl+,`）。
2. 在左侧菜单找到 **Extensions（扩展）并选择 AIoT Image Preview**。
3. 设置 `Base Dir` 参数以适配不同环境（如 simulator 版本）。
  
    <img src="./figures/040.png" alt="" width="75%">
