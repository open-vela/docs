# 下载 openvela 源码

\[ [English](./../../en/quickstart/Download_Vela_sources.md) | 简体中文 \]

openvela 源码位于由 [GitHub](https://github.com/open-Vela)、[Gitee](https://gitee.com/open-vela) 和 [GitCode](https://gitcode.com/open-vela) 托管的 Git 仓库中。

## 步骤一 初始化 Repo 客户端

1. 创建并导航到工作目录：

    ```bash
    mkdir vela-opensource
    cd vela-opensource
    ```

2. 初始化用于操作源码的工作目录：

    - Github（需注册公钥，请参考 [Github 文档](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)）：

        ``` bash
        repo init --partial-clone -u git@github.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs

        # Install Git LFS (Large File Storage) for managing large files
        sudo apt install git-lfs
        cd .repo/manifests 
        git lfs install
        git lfs --version
        cd ../../
        ```

    - Gitee（需注册公钥，请参考[码云文档](https://gitee.com/help/articles/4191)）：

        ```bash
        repo init --partial-clone -u git@gitee.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs

        # Install Git LFS (Large File Storage) for managing large files
        sudo apt install git-lfs
        cd .repo/manifests 
        git lfs install
        git lfs --version
        cd ../../
        ```

    - GitCode（需注册公钥，请参考 [GitCode 文档](https://docs.gitcode.com/docs/help/home/user_center/security_management/ssh)）：

        ```bash
        repo init --partial-clone -u https://gitcode.com/open-vela/manifests.git -b dev -m openvela.xml --git-lfs --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/

        # Install Git LFS (Large File Storage) for managing large files
        sudo apt install git-lfs
        cd .repo/manifests 
        git lfs install
        git lfs --version
        cd ../../
        ```

## 步骤二 下载源码

运行如下命令下载 openvela 源码树至工作目录：

```bash
repo sync -c -j8
```

> 说明
>
> openvela 项目使用 **clang-format 14** 版本进行代码风格检查，更多详情请参见[代码风格检查指南](../contribute/code_style_check_guide.md)。

## 常见问题

- [快速入门常见问题](../faq/QuickStart_FAQ.md)

## 后续步骤

完成源码下载后，请参见[编译 openvela 源码](./Build_Vela_from_sources_zh-cn.md)文档进行后续操作。
