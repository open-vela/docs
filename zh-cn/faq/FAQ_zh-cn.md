# 常见问题汇总

\[ [English](./../../en/faq/FAQ.md) | 简体中文 \]

## 一、 openvela 可以用什么语言开发应用

Native 主要是 C/C++，快应用使用 JavaScript。

## 二、 Xiaomi Vela 和 openvela 的关系

openvela 和 Xiaomi Vela 基于同一套代码实现，openvela 是开源版本。

## 三、快速入门常见问题

### 1、怎么使用 build.sh 编译 nuttx 已支持的开发板

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

### 2、Unable to access 'https://gerrit.googlesource.com/git-repo/'

#### 问题描述

运行以下命令时，出现访问错误，提示无法连接到 `https://gerrit.googlesource.com/git-repo/`。

```Bash
repo init --partial-clone -u git@gitee.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs
```

报错提示：

```Bash
fatal: unable to access 'https://gerrit.googlesource.com/git-repo/': Failed to connect to gerrit.googlesource.com
```

![img](./images/001.png)

#### 问题原因

无法访问 `https://gerrit.googlesource.com/git-repo/` 的问题常见于以下场景：

1. 网络限制。
2. 镜像源区域限制
3. DNS 域名解析问题

综上所述，问题主要源于网络访问受限，解决方案是使用国内可用的镜像源来替代默认仓库地址，从而绕过此问题。

#### 解决方案

在运行命令之前，将数据源替换为清华大学镜像源。执行以下步骤：

1. 设置清华镜像源。

    ```Bash
    export REPO_URL='https://mirrors.tuna.tsinghua.edu.cn/git/git-repo'
    ```

2. 再次执行初始化命令。

    ```Bash
    repo init --partial-clone -u git@gitee.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs
    ```

### 3、no Qt platform plugin could be initialized

#### 问题描述

运行以下指令时，发生错误提示：

```Bash
./emulator.sh vela
```

错误提示：

```Bash
No Qt platform plugin could be initialized
```

![img](./images/002.jpg)

#### 问题原因

openvela 源代码存放路径中包含中文字符，此类路径可能导致工具无法正确解析。

#### 解决方案

请将源码存放至无中文路径的目录中。

### 4、无法读取远程仓库

#### 问题描述

在初始化 openvela 仓库时，运行以下命令时提示无法读取远程仓库：

```Bash
repo init --partial-clone -u git@gitee.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs
```

![img](./images/003.png)

#### 原因分析

出现该问题的原因可能是**未正确设置** **SSH** **公钥**，导致无法通过 SSH 验证访问 Gitee 或 GitHub 远程仓库。

#### 解决方案

参考官方文档完成 SSH 公钥的生成和配置：

- [GitHub](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- [Gitee](https://gitee.com/help/articles/4191#article-header0)