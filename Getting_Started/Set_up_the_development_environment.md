# Setting up the Development Environment

\[ English | [简体中文](Set_up_the_development_environment_zh-cn.md) \]

## Hardware requirements

The development workstation should meet the following hardware requirements:

- 64-bit x 86 system
- At least 80 GB of remaining hard disk space for downloading and compiling source codes.
- At least 16 GB of RAM

## Operating system requirements

You need to run a 64-bit Linux distribution on the development workstation.

## Install required software packages

Use Ubuntu 22.04 to compile openvela. Run the following command to install the required packages on Ubuntu 22.04:

```bash
sudo apt install \
bison flex gettext texinfo libncurses5-dev libncursesw5-dev xxd \
git gperf automake libtool build-essential gperf genromfs \
libgmp-dev libmpc-dev libmpfr-dev libisl-dev binutils-dev libelf-dev \
libexpat1-dev gcc-multilib g++-multilib picocom u-boot-tools util-linux \
dfu-util libx11-dev libxext-dev net-tools pkgconf unionfs-fuse zlib1g-dev \
libusb-1.0-0-dev libv4l-dev libuv1-dev npm nodejs nasm yasm libdivsufsort-dev \
libc++-dev libc++abi-dev libprotobuf-dev protobuf-compiler protobuf-c-compiler mtools
```

## Install Repo

Run the following command to install Repo Launcher:

```bash
curl https://storage.googleapis.com/git-repo-downloads/repo > repo
chmod +x repo
sudo mv repo /usr/local/bin/
```

The Repo Launcher provides a Python script that initializes a checkout and downloads the full Repo tool.

## Install KConfig frontend

The configuration system of openvela uses [KConfig](https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt). KConfig configures the system via a series of interactive menu-based frontends, part of the kconfig-frontends package.Whether to use a package or build it from source depends on the current operating system. The source code is available in [NuttX tools repository](https://bitbucket.org/nuttx/tools/src/master/kconfig-frontends/).

```bash
sudo apt install kconfig-frontends
```

## Install Python

```bash
sudo apt install python3 python3-pip python-is-python3
```

## Install Python package

```bash
sudo pip3 install kconfiglib pyelftools cxxfilt
```

## Next steps

Refer to [Download openvela code](./Download_Vela_sources.md).
