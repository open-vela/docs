# Setting up the Development Environment

\[ English | [简体中文](./../../zh-cn/quickstart/Set_up_the_development_environment_zh-cn.md) \]

## Hardware Requirements

Your development workstation should meet the following hardware requirements:

- A 64-bit x86 system
- At least 80 GB of free disk space for downloading and building the source code
- At least 16 GB of RAM

## Operating System Requirements

**The development workstation must run a 64-bit Ubuntu 22.04 Linux distribution.**

> **Note**: **WSL** and **Docker** environments are not supported.

## Procedures

### Step 1: Install Required Packages

Use Ubuntu 22.04 to build openvela. Run the following command to install the required packages on Ubuntu 22.04:

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

### Step 2: Install Repo

Run the following command to install the Repo launcher:

```bash
curl https://storage.googleapis.com/git-repo-downloads/repo > repo
chmod +x repo
sudo mv repo /usr/local/bin/
```

The Repo launcher is a Python script that initializes a checkout and downloads the full Repo tool.

### Step 3: Install KConfig frontend

The openvela configuration system uses [KConfig](https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt), which is part of the `kconfig-frontends` package. KConfig configures the system through a series of interactive menu-based frontends. Whether you install it from a package or build from source depends on your operating system. The source code is available in the [NuttX tools repository](https://bitbucket.org/nuttx/tools/src/master/kconfig-frontends/).

```bash
sudo apt install kconfig-frontends
```

### Step 4: Install Python

```bash
sudo apt install python3 python3-pip python-is-python3
```

### Step 5: Install Python Packages

```bash
sudo pip3 install kconfiglib pyelftools cxxfilt
```

## FAQ

- [Quick Start FAQ](../faq/QuickStart_FAQ.md)

## Next Steps

Refer to [Download openvela Source Code](./Download_Vela_sources.md).
