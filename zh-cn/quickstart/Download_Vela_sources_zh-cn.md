# 下载 openvela 源码

\[ [English](./../../en/quickstart/Download_Vela_sources.md) | 简体中文 \]

`openvela` 源码托管在 [GitHub](https://github.com/open-Vela)、[Gitee](https://gitee.com/open-vela) 和 [GitCode](https://gitcode.com/open-vela) 平台的 Git 仓库中。本指南将引导您完成源码的下载。

### 准备工作

- 已安装 `repo` 工具。
- 源码下载需要稳定的网络连接。

## 步骤一 准备工作区并初始化源码

1. 创建并进入工作目录：

    打开终端，执行以下命令来创建一个用于存放源码的目录。

    ```bash
    mkdir vela-opensource
    cd vela-opensource
    ```

2. 安装 Git LFS (仅需首次配置)：

    `openvela` 使用 Git LFS (Large File Storage) 来管理仓库中的大文件。在继续之前，请确保您的系统中已安装并启用 Git LFS。

    ```bash
    # 在 Ubuntu 系统上安装 Git LFS
    sudo apt update
    sudo apt install git-lfs
    ```

3. 选择代码源并初始化仓库：

    请根据您的网络环境和偏好，从以下任一平台选择一种方式（推荐使用 HTTPS）来初始化仓库。

    #### 选项 A：从 GitHub 下载

    - **方式一：HTTPS (推荐)**

        此方式最简单，无需配置 SSH 密钥。

        ```bash
        repo init --partial-clone -u https://github.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    - **方式二：SSH**

        此方式需要您先将 SSH 公钥添加至您的 GitHub 账户。请参考 [GitHub 官方文档](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)。

        ```bash
        repo init --partial-clone -u ssh://git@github.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    #### 选项 B：从 Gitee 下载

    - **方式一：HTTPS (推荐)**

        此方式对中国大陆用户访问更友好。

        ```bash
        repo init --partial-clone -u https://gitee.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    - **方式二：SSH**

        此方式需要您先将 SSH 公钥添加至您的 Gitee 账户。请参考 [Gitee 官方文档](https://gitee.com/help/articles/4191)。

        ```bash
        repo init --partial-clone -u ssh://git@gitee.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    #### 选项 C：从 GitCode 下载

    - **方式一：HTTPS (推荐)**

        此命令已包含清华大学镜像源以加速 `repo` 工具本身的下载。

        ```bash
        repo init --partial-clone -u https://gitcode.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/
        ```

    - **方式二：SSH**

        此方式需要您先将 SSH 公钥添加至您的 GitCode 账户。请参考 [GitCode 官方文档](https://docs.gitcode.com/docs/help/home/user_center/security_management/ssh)。

        ```bash
        repo init --partial-clone -u ssh://git@gitcode.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/
        ```

## 步骤二 同步源码

完成 `repo` 初始化后，运行以下命令将 `openvela` 的完整源码同步到您的本地工作目录。：

```bash
repo sync -c -j8
```

> **说明**
>
> `-c` 标志表示只同步清单中指定的当前分支，可以减少下载的数据量。
>
> `-j8` 标志表示使用 8 个并发作业进行同步，您可以根据您机器的 CPU核心数和网络状况适当调整此数值以加快下载速度。

## 重要说明

`openvela` 项目使用 **clang-format 14** 版本进行代码风格检查。如果您计划贡献代码，请确保您的开发环境已配置好对应的工具。更多详情请参见[代码风格检查指南](../contribute/code_style_check_guide.md)。

## 常见问题

- [快速入门常见问题](../faq/QuickStart_FAQ.md)

## 后续步骤

完成源码下载后，请继续阅读[编译 openvela 源码](./Build_Vela_from_sources_zh-cn.md)文档进行后续操作，学习如何编译和构建系统。
