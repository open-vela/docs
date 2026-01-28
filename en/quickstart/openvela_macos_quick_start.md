# Quick Start (macOS)

[ English | [简体中文](./../../zh-cn/quickstart/openvela_macos_quick_start.md) ]

This guide will walk you through setting up the development environment, downloading the source code, compiling the project, and running the build artifacts on the **macOS** operating system using the Vela Emulator.

## Step 1: Prerequisites

Before you begin, ensure your development environment meets the following requirements.

### 1. Hardware Requirements

- **Disk**: At least 40 GB of free space for source code and build artifacts.
- **Memory**: At least 16 GB of RAM.

### 2. Operating System Requirements

- **Operating System**: macOS 12 (Monterey) or later.

### 3. Install Development Tools

Install the development tools required for compiling openvela in the following order.

1. Install Xcode Command Line Tools.

    Xcode Command Line Tools include core utilities for software development on macOS, such as the Clang compiler and Git. Open the **Terminal** app and run the following command:

    ```Bash
    xcode-select --install
    ```

    In the pop-up dialog, click **Install** and agree to the license agreement to complete the installation.

2. Install CMake. CMake is a cross-platform build system generator.

    1. Visit the [official CMake download page](https://cmake.org/download) to download and install the latest version of **CMake (3.x)** for macOS.

    2. After installation, run the following command to add CMake to the system path, allowing it to be called directly from the terminal.

        ```Bash
        /Applications/CMake.app/Contents/MacOS/CMake --install
        ```

3. Install Git LFS.

    Git Large File Storage (LFS) is used to handle large files in code repositories.

    Visit the [official Git LFS website](https://git-lfs.com/), then download and run the installer.

4. Install Python 3.

    The `repo` tool and build scripts depend on a Python 3 environment.

    1. Visit the [official Python website](https://www.python.org/downloads/) to download and install the latest version of Python 3.

    2. After installation, you must run the `Install Certificates.command` script to ensure Python's SSL certificates are configured correctly, which prevents subsequent network request failures. Adjust the path according to your installed Python version.

        ```Bash
        # Example path, adjust it based on your actual installed Python version
        sudo /Applications/Python\ 3.12/Install\ Certificates.command
        ```

5. Install Homebrew.

    Homebrew is a package manager for macOS. We will use it to install `gpg`, a dependency for the `repo` tool. Run the following command to install Homebrew:

    ```Bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

6. Install GPG. GnuPG (GPG) is a dependency required by the `repo` tool to verify code signatures.

    1. Use Homebrew to install `gpg`.

        ```Bash
        brew install gpg
        ```

    2. If the `gpg` command is not recognized by the system, run the following command to create a symbolic link manually.

        ```Bash
        ln -s /opt/homebrew/bin/gpg /usr/local/bin/gpg
        ```

## Step 2: Download the Source Code

openvela uses the `repo` tool to manage its source code, which is distributed across multiple Git repositories.

### 1. Install the Repo Tool

`repo` is a repository management tool built on top of Git. Run the following commands to securely download and install it.

```Bash
curl -sSL "https://storage.googleapis.com/git-repo-downloads/repo" > repo
chmod +x repo
sudo mv repo /usr/local/bin
```

After installation, you can run `repo --version` to verify it.

### 2. Initialize and Sync the Repository

1. Create a working directory to store all of the openvela source code.

    ```Bash
    mkdir openvela && cd openvela
    ```

2. Initialize the project manifest using `repo` and specify the `dev` branch.

    Please select one of the following methods (SSH is recommended) based on your network environment and preference to initialize the repository.

    #### Option A: Download from GitHub

    - Method 1: SSH (Recommended)

        This method requires you to add your SSH public key to your GitHub account first. Please refer to the [official GitHub documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

        ```bash
        repo init -u ssh://git@github.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    - Method 2: HTTPS

        ```bash
        repo init -u https://github.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    #### Option B: Download from Gitee

    - Method 1: SSH (Recommended)

        This method requires you to add your SSH public key to your Gitee account first. Please refer to the [official Gitee documentation](https://gitee.com/help/articles/4191).

        ```bash
        repo init -u ssh://git@gitee.com/open-vela/manifests.git -b dev -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs
        ```

    - Method 2: HTTPS

        ```bash
        repo init -u https://gitee.com/open-vela/manifests.git -b dev -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs
        ```

    #### Option C: Download from GitCode

    - Method 1: SSH (Recommended)

        This method requires you to add your SSH public key to your GitCode account first. Please refer to the [official GitCode documentation](https://docs.gitcode.com/docs/help/home/user_center/security_management/ssh).

        ```bash
        repo init -u ssh://git@gitcode.com/open-vela/manifests.git -b dev -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs
        ```

    - Method 2: HTTPS

        ```bash
        repo init -u https://gitcode.com/open-vela/manifests.git -b dev -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs
        ```

3. Run the sync command. `repo` will download all relevant source code repositories according to the manifest file (`openvela.xml`).

    ```Bash
    repo sync -c -j8
    ```

## Step 3: Compile the Source Code

After downloading the source code, perform the following build steps in the openvela root directory.

### 1. Set Up Environment Variables

Run the following commands to add the prebuilt toolchain paths to the environment variables for the current terminal session.

```Bash
uname_s=$(uname -s | tr '[A-Z]' '[a-z]')
uname_m=$(uname -m | sed 's/arm64/aarch64/g')
export PATH=$PWD/prebuilts/build-tools/${uname_s}-${uname_m}/bin:$PATH
export PATH=$PWD/prebuilts/cmake/${uname_s}-${uname_m}/bin:$PATH
export PATH=$PWD/prebuilts/python/${uname_s}-${uname_m}/bin:$PATH
export PATH=$PWD/prebuilts/gcc/${uname_s}-${uname_m}/aarch64-none-elf/bin:$PATH
export PATH=$PWD/prebuilts/gcc/${uname_s}-${uname_m}/arm-none-eabi/bin:$PATH
export PYTHONPATH=$PWD/prebuilts/tools/python/dist-packages/cxxfilt
export PYTHONPATH=$PWD/prebuilts/tools/python/dist-packages/kconfiglib:$PYTHONPATH
export PYTHONPATH=$PWD/prebuilts/tools/python/dist-packages/pyelftools:$PYTHONPATH
```

> **Note**: This environment variable configuration is only valid for the current terminal window. If you open a new terminal, you must run this script again.

### 2. Configure the CMake Project (Out-of-Tree)

openvela uses an **Out-of-tree build** approach, which separates the build artifacts from the source code to keep the source directory clean.

Run the following `cmake` command to configure the project. This command will:

- Generate the build system files in the `cmake_out/goldfish-arm64-v8a-ap` directory.
- Use Ninja as the build tool to improve compilation speed.
- Specify the configuration file for the target board.

```Bash
cmake \
  -B cmake_out/goldfish-arm64-v8a-ap \
  -S $PWD/nuttx \
  -GNinja \
  -DBOARD_CONFIG=../vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap \
  -DEXTRA_FLAGS="-Wno-cpp -Wno-deprecated-declarations"
```

![alt text](./figures/005.png)

### 3. (Optional) Customize Kernel Configuration

You can use the `menuconfig` command to open a graphical interface for adjusting the NuttX kernel and component configurations.

```Bash
cmake --build cmake_out/goldfish-arm64-v8a-ap -t menuconfig
```

> **Tips**
>
> - Press `/` to search for a configuration item.
> - Press the `Spacebar` to toggle the selection state (enable/disable/modularize).
> - After configuring, select **Save** to save and exit.

![alt text](./figures/006.png)

### 4. Run the Build

Run the following command to build the entire project.

```Bash
cmake --build cmake_out/goldfish-arm64-v8a-ap
```

After a successful build, you will find `nuttx` and other build artifacts in the `cmake_out/goldfish-arm64-v8a-ap` directory.

![alt text](./figures/007.png)

## Step 4: Run the Emulator

In the openvela root directory, run the following script to start the `Vela Emulator` and load your build artifacts.

```Bash
./emulator.sh cmake_out/goldfish-arm64-v8a-ap
```

After the emulator starts, you will see the `goldfish-armv8a-ap>` prompt, indicating that openvela is running successfully.

![alt text](./figures/008.png)

![alt text](./figures/009.png)

## Next Steps

- Frequently Asked Questions

    - [Quick Start FAQ](../faq/QuickStart_FAQ.md)

- Further Reading

    - [Debugging with the Emulator](./emulator/Debugging_Vela_with_Vela_Emulator.md)
    - [ADB Commands](./emulator/Android_Debug_Bridge_commands.md)
    - [Sending Emulator Console Commands](./emulator/Send_emulator_console_commands.md)
