# 准备开发环境

\[ [English](Set_up_the_development_environment.md) | 简体中文 \]

## 硬件需求

开发工作站应当满足如下硬件需求：

- 64 位 x86 系统
- 至少 80 GB 用于下载和编译源码的剩余硬盘空间
- 至少 16 GB RAM

## 操作系统需求

开发工作站需运行 64 位 Linux 发行版。 

## 安装必备的软件包

推荐使用 Ubuntu 22.04 版本编译 openvela。运行以下命令，在 Ubuntu 22.04 版本上安装必备的软件包：

```
sudo apt install \
bison flex gettext texinfo libncurses5-dev libncursesw5-dev xxd \
git gperf automake libtool build-essential gperf genromfs \
libgmp-dev libmpc-dev libmpfr-dev libisl-dev binutils-dev libelf-dev \
libexpat1-dev gcc-multilib g++-multilib picocom u-boot-tools util-linux \
dfu-util libx11-dev libxext-dev net-tools pkgconf unionfs-fuse zlib1g-dev \
libusb-1.0-0-dev libv4l-dev libuv1-dev npm nodejs nasm yasm libdivsufsort-dev \
libc++-dev libc++abi-dev libprotobuf-dev protobuf-compiler protobuf-c-compiler mtools
```

## 安装 Repo

运行以下命令安装 Repo 启动器:

```
sudo apt-get install repo
```

Repo 启动器会提供一个 Python 脚本，该脚本可以初始化检出，并可以下载完整的 Repo 工具。

## 安装 KConfig frontend

openvela 配置系统使用 [KConfig](https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt) ，作为 kconfig-frontends 软件包的一部分，KConfig 通过一系列基于交互式菜单的前端对系统进行配置。使用软件包还是从源码构建取决于当前的操作系统，源码地址位于 [NuttX tools repository](https://bitbucket.org/nuttx/tools/src/master/kconfig-frontends/)。

```
sudo apt install kconfig-frontends
```

## 安装 Python

```
sudo apt install python3 python3-pip python-is-python3
```

## 安装 Python 包

```
sudo pip3 install kconfiglib pyelftools cxxfilt
```

## 后续步骤
请参阅 [下载 openvela 源码](./Download_Vela_sources_zh-cn.md)。

