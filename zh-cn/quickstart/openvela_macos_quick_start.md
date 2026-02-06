# 快速入门（macOS）

\[ [English](../../en/quickstart/openvela_macos_quick_start.md) | 简体中文 \]

本指南将指导您在 **macOS** 操作系统上完成 openvela 的开发环境准备、源代码下载、编译构建，并最终通过 Vela Emulator 运行编译产物。

## 步骤一：准备工作

在开始之前，请确保您的开发环境满足以下要求。

### 1. 硬件要求

- **硬盘**：至少 40 GB 可用空间，用于存放源代码和编译产物。
- **内存**：至少 16 GB RAM。

### 2. 操作系统要求

- **操作系统**：macOS 12 (Monterey) 或更高版本。

### 3. 安装开发工具

请按照以下顺序安装 openvela 编译所需的开发工具。

1. 安装 Xcode Command Line Tools。

    Xcode Command Line Tools 包含在 macOS 上进行软件开发所需的核心工具，如 Clang 编译器和 Git。 打开**终端 (Terminal)**应用，执行以下命令：

    ```Bash
    xcode-select --install
    ```

    在弹出的对话框中，点击**安装**并同意许可协议以完成安装。

2. 安装 CMake。 CMake 是一个跨平台的构建系统生成工具。

    1. 访问 [CMake 官网下载页面](https://cmake.org/download)，下载并安装适用于 macOS 的最新版 **CMake (3.x)**。

    2. 安装完成后，执行以下命令将 CMake 添加到系统路径中，以便在终端中直接调用。

        ```Bash
        /Applications/CMake.app/Contents/MacOS/CMake --install
        ```

3. 安装 Git LFS。

    Git Large File Storage (LFS) 用于处理代码仓库中的大文件。

    访问 [Git LFS 官网](https://git-lfs.com/)，下载并运行安装程序。

4. 安装 Python 3。

    `repo` 工具和构建脚本依赖 Python 3 环境。

    1. 访问 [Python 官网](https://www.python.org/downloads/)，下载并安装最新版的 Python 3。

    2. 安装完成后，务必运行 `Install Certificates.command` 脚本，以确保 Python 的 SSL 证书配置正确，避免后续网络请求失败。请根据您安装的 Python 版本调整路径。

        ```Bash
        # 示例路径，请根据您实际安装的 Python 版本进行调整
        sudo /Applications/Python\ 3.12/Install\ Certificates.command
        ```

5. 安装 Homebrew。

    Homebrew 是 macOS 的包管理器，我们将使用它来安装 `repo` 工具的依赖项 `gpg`。 执行以下命令安装 Homebrew：

    ```Bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

6. 安装 GPG。 GnuPG (GPG) 是 `repo` 工具验证代码签名所需的依赖。

    1. 使用 Homebrew 安装 `gpg`。

        ```Bash
        brew install gpg
        ```

    2. 如果 `gpg` 命令未被系统识别，可执行以下命令手动创建符号链接。

        ```Bash
        ln -s /opt/homebrew/bin/gpg /usr/local/bin/gpg
        ```

## 步骤二：下载源代码

openvela 使用 `repo` 工具管理其分布在多个 Git 仓库中的源代码。

### 1. 安装 Repo 工具

`repo` 是一个构建于 Git 之上的代码库管理工具。执行以下命令来安全地下载并安装它。

```Bash
curl -sSL "https://storage.googleapis.com/git-repo-downloads/repo" > repo
chmod +x repo
sudo mv repo /usr/local/bin
```

安装完成后，可运行 `repo --version` 进行验证。

### 2. 初始化并同步代码库

1. 创建一个工作目录，用于存放 openvela 的所有源代码。

    ```Bash
    mkdir openvela && cd openvela
    ```

2. 使用 `repo` 初始化项目清单，并指定 `trunk` 分支。

    请根据您的网络环境和偏好，从以下任一平台选择一种方式（推荐使用 SSH）来初始化仓库。

    #### 选项 A：从 GitHub 下载

    - 方式一：SSH（推荐）

        此方式需要您先将 SSH 公钥添加至您的 GitHub 账户，请参考 [GitHub 官方文档](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)。

        ```bash
        repo init -u ssh://git@github.com/open-vela/manifests.git -b trunk -m openvela.xml
        ```

    - 方式二：HTTPS

        ```bash
        repo init -u https://github.com/open-vela/manifests.git -b trunk -m openvela.xml
        ```

    #### 选项 B：从 Gitee 下载

    - 方式一：SSH (推荐)

        此方式需要您先将 SSH 公钥添加至您的 Gitee 账户，请参考 [Gitee 官方文档](https://gitee.com/help/articles/4191)。

        ```bash
        repo init --u ssh://git@gitee.com/open-vela/manifests.git -b trunk -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/
        ```

    - 方式二：HTTPS

        ```bash
        repo init -u https://gitee.com/open-vela/manifests.git -b trunk -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/
        ```

    #### 选项 C：从 GitCode 下载

    - 方式一：SSH (推荐)

        此方式需要您先将 SSH 公钥添加至您的 GitCode 账户，请参考 [GitCode 官方文档](https://docs.gitcode.com/docs/help/home/user_center/security_management/ssh)。

        ```bash
        repo init -u ssh://git@gitcode.com/open-vela/manifests.git -b trunk -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/
        ```

    - 方式二：HTTPS

        ```bash
        repo init -u https://gitcode.com/open-vela/manifests.git -b trunk -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/
        ```

3. 执行同步命令，`repo` 将根据清单文件 (`openvela.xml`) 下载所有相关的源代码仓库。

    ```Bash
    repo sync -c -j8
    ```

    ![alt text](./figures/004.png)

    > **操作提示**
    >
    > - 首次同步耗时较长，具体时间取决于您的网络状况和磁盘性能。
    > - 若因网络问题中断，可重复执行 `repo sync` 进行增量同步。

## 步骤三：编译源代码

完成源代码下载后，请在 openvela 根目录下执行以下编译步骤。

### 1. （可选）自定义内核配置

您可以通过 `menuconfig` 命令打开图形化界面，以调整 NuttX 内核与组件的配置。

```Bash
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake menuconfig
```

> **操作技巧**
>
> - 按 `/` 键可搜索配置项。
> - 按 `空格键` 可切换选中状态（启用/禁用/模块化）。
> - 配置完成后，选择 **Save** 保存并退出。

<img src="./figures/006.png" alt="" width="75%">

### 2. 执行编译

执行以下命令，构建整个项目。

```Bash
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake -j$(nproc)
```

编译成功后，您将在 `cmake_out/vela_goldfish-arm64-v8a-ap` 目录下找到 `nuttx` 等编译产物。

<img src="./figures/007.png" alt="" width="75%">

## 步骤四：运行模拟器

在 openvela 根目录下，执行以下脚本启动 `Vela Emulator` 并加载您的编译产物。

```Bash
./emulator.sh cmake_out/vela_goldfish-arm64-v8a-ap/
```

模拟器启动后，您将看到 `goldfish-armv8a-ap>` 提示符，表明 openvela 已成功运行。

<img src="./figures/008.png" alt="" width="75%">

## 后续步骤

- 常见问题

    - [快速入门常见问题](../faq/QuickStart_FAQ.md)

- 进一步阅读

    - [使用模拟器调试](./emulator/Debugging_Vela_with_Vela_Emulator_zh-cn.md)
    - [ADB 命令](./emulator/Android_Debug_Bridge_commands_zh-cn.md)
    - [发送模拟器控制台命令](./emulator/Send_emulator_console_commands_zh-cn.md)
