# 下载 openvela 源码

\[ [English](Download_Vela_sources.md) | 简体中文 \]

openvela 源码位于由 [GitHub](https://github.com/open-Vela) 或 [Gitee](https://gitee.com/open-vela) 托管的 Git 仓库中。

## 初始化 Repo 客户端

1. 创建并导航到工作目录：

    ```bash
    mkdir vela-opensource
    cd vela-opensource
    ```

2. 初始化用于操作源码的工作目录:

    - Github（需注册公钥，请参考[Github文档](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)）：

        ``` bash
        # Install Git LFS (Large File Storage) for managing large files
        sudo apt install git-lfs
        git lfs install
        git lfs --version

        repo init --partial-clone -u git@github.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

    - Gitee（需注册公钥，请参考[码云文档](https://gitee.com/help/articles/4191)）：

        ```bash
        # Install Git LFS (Large File Storage) for managing large files
        sudo apt install git-lfs
        git lfs install
        git lfs --version

        repo init --partial-clone -u git@gitee.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```

## 下载 openvela 源码

运行如下命令下载 openvela 源码树至工作目录：

```bash
repo sync -c -j$(nproc)
```

## 后续步骤

请参阅[编译 openvela 源码](./Build_Vela_from_sources_zh-cn.md)。
