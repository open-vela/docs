# 常见问题汇总

\[ [English](./../../en/faq/FAQ.md) | 简体中文 \]

## 一、怎么使用 build.sh 编译 nuttx 已支持的开发板

与 NuttX 提供的 `configure.sh` 脚本类似。以下以 `qemu-armv7a:nsh` 为例进行操作说明。

以下是使用两种脚本进行编译的命令示例：

1. 使用 `configure.sh` 脚本进行编译：

     ```Bash
    # 使用 NuttX 自带的配置脚本
    ./tools/configure.sh -l qemu-armv7a:nsh
    make -j12
    ```

2. 使用 `build.sh` 脚本进行编译：

    ```Bash
    # 使用改进的 build.sh 脚本
    ./build.sh qemu-armv7a:nsh -j12
    ```

推荐优先使用 `build.sh`，该脚本对编译流程进行了优化并简化了操作。