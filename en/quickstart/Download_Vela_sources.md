# Download openvela Source Code

\[ English | [简体中文](./../../zh-cn/quickstart/Download_Vela_sources_zh-cn.md) \]

The `openvela` source code is hosted in Git repositories on multiple platforms, including [GitHub](https://github.com/open-Vela), [Gitee](https://gitee.com/open-vela), and [GitCode](https://gitcode.com/open-vela). This guide will walk you through the process of downloading the source code.

## Prerequisites

- You have the `repo` tool installed.
- A stable internet connection is required for downloading the source code.

## Step 1: Prepare the Workspace and Initialize the Source Code

1. Create and enter the working directory:

    Open a terminal and run the following commands to create a directory for the source code.

    ```bash
    mkdir vela-opensource
    cd vela-opensource
    ```

2. Install Git LFS (First-time setup only):

   `openvela` uses Git LFS (Large File Storage) to manage large files in its repositories. Before proceeding, ensure that Git LFS is installed and enabled on your system.

   ```bash
   # Install Git LFS on Ubuntu systems
   sudo apt update
   sudo apt install git-lfs
   ```

3. Choose a Source and Initialize the Repository:

    Choose one of the following methods from any platform based on your network environment and preferences. Using HTTPS is recommended.

    #### Option A: Download from GitHub

    - **Method 1: HTTPS (Recommended)**

        This is the simplest method and does not require SSH key configuration.

        ```bash
        repo init --partial-clone -u https://github.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    - **Method 2: SSH**

        This method requires you to add your SSH public key to your GitHub account. Please refer to the [official GitHub documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

        ```bash
        repo init --partial-clone -u ssh://git@github.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    #### Option B: Download from Gitee

    - **Method 1: HTTPS (Recommended)**

        This method provides better access for users in mainland China.

        ```bash
        repo init --partial-clone -u https://gitee.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    - **Method 2: SSH**

        This method requires you to add your SSH public key to your Gitee account. Please refer to the [official Gitee documentation](https://gitee.com/help/articles/4191) (in Chinese).

        ```bash
        repo init --partial-clone -u ssh://git@gitee.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    #### Option C: Download from GitCode

    - **Method 1: HTTPS (Recommended)**

        This command includes the Tsinghua University mirror to accelerate the download of the `repo` tool itself.

        ```bash
        repo init --partial-clone -u https://gitcode.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/
        ```

    - **Method 2: SSH**

        This method requires you to add your SSH public key to your GitCode account. Please refer to the [official GitCode documentation](https://docs.gitcode.com/docs/help/home/user_center/security_management/ssh) (in Chinese).

        ```bash
        repo init --partial-clone -u ssh://git@gitcode.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/
        ```

## Step 2: Sync the Source Code

After the `repo` initialization is complete, run the following command to sync the full `openvela` source code to your local working directory.

```bash
repo sync -c -j8
```

> **Note**
>
> - The `-c` flag tells `repo` to sync only the current branch specified in the manifest, which can reduce the amount of data downloaded.
> - The `-j8` flag uses 8 concurrent jobs for synchronization. You can adjust this value based on your machine's CPU cores and network conditions to speed up the download.

## Important Note

The `openvela` project uses **clang-format version 14** for code style checking. If you plan to contribute code, please ensure your development environment is configured with the corresponding tool. For more details, see the [Code Style Check Guide](../contribute/code_style_check_guide.md).

## FAQ

- [Quick Start FAQ](../faq/QuickStart_FAQ.md)

## Next Steps

After downloading the source code, proceed to the [Compile the openvela source code](./Build_Vela_from_sources.md) document to learn how to compile and build the system.
