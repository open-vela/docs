# Set up the development environment

\[ English | [简体中文](Set_up_the_development_environment_zh-cn.md) \]

## Hardware requirements

The development workstation should meet or exceed following hardware requirements:

- A 64-bit x86 system.
- At least 80 GB of free disk space to check out and build the code.
- A minimum of 16 GB of RAM.

## Operating system requirements

The development workstation must run any 64-bit Linux distribution. 

## Install required packages

It is recommended to compile openvela using Ubuntu 22.04. Run the following command to install the required packages on Ubuntu 22.04:

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

## Install Repo

Follow these steps to install Repo:

* Run the following command to install the Repo launcher:

```
sudo apt-get install repo
```

The Repo launcher provides a Python script that initializes a checkout and downloads the full Repo tool.

## Install KConfig frontend

openvela configuration system uses [KConfig](https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt) which is exposed via a series of interactive menu-based frontends, part of the kconfig-frontends package. Depending on your OS you may use a precompiled package or you will have to build it from source, which is available in the [NuttX tools repository](https://bitbucket.org/nuttx/tools/src/master/kconfig-frontends/):

```
sudo apt install kconfig-frontends
```

## Install Python

```
sudo apt install python3 python3-pip python-is-python3
```

## Install Python packages

```
sudo pip3 install kconfiglib pyelftools cxxfilt
```

## What to do next

Please refer to [Download openvela sources](./Download_Vela_sources.md).

