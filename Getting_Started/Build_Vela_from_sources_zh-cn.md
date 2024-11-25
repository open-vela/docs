# 编译 openvela 源码

\[ [English](Build_Vela_from_sources.md) | 简体中文 \]

## 使用 build.sh 构建 openvela

在安装完 openvela 所需软件包及下载完 openvela 源码后，您可以将 openvela 源码编译成可以在开发板上运行的二进制文件。

### 初始化配置

第一步是基于已存在的配置为目标开发板初始化 openvela 配置。

通过将 `vendor/<vendor name>/boards/<board name>/configs/<board configuration>` 作为参数传递给 build.sh 选择配置。

选择 openvela Emulator arm:

```
./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap
```

选择 openvela Emualtor arm64:

```
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap
```

选择 openvela Emulator x86\_64:

```
./build.sh vendor/openvela/boards/vela/configs/goldfish-x86_64-ap
```

下一步若选取 openvela Emulator 运行 openvela，参阅 [使用 openvela Emulator 运行 openvela](./Run_Vela_on_Vela_Emulator_zh-cn.md)。
