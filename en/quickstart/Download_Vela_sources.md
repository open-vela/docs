# Download openvela Source Code

\[ English | [简体中文](./../../zh-cn/quickstart/Download_Vela_sources_zh-cn.md) \]

The openvela source code is located in a Git repository hosted by [GitHub](https://github.com/open-Vela) or [Gitee](https://gitee.com/open-vela).

## Initialize the Repo client

1. Create and navigate to a working directory:

    ```bash
    mkdir vela-opensource
    cd vela-opensource
    ```

2. Initialize the working directory for source code:

   - Github (Public key registration is required. Refer to [Github documents](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account):

        ``` bash
        repo init --partial-clone -u git@github.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs

        # Install Git LFS (Large File Storage) for managing large files
        sudo apt install git-lfs
        cd .repo/manifests 
        git lfs install
        git lfs --version
        cd ../../
        ```

   - Gitee (Public key registration is required. Refer to [Gitee document](https://gitee.com/help/articles/4191):

        ```bash
        repo init --partial-clone -u git@gitee.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        
        # Install Git LFS (Large File Storage) for managing large files
        sudo apt install git-lfs
        cd .repo/manifests 
        git lfs install
        git lfs --version
        cd ../../
        ```

## Download source code

Run the following command to download the source code tree of openvela to your working directory:

```bash
repo sync -c -j$(nproc)
```

## Next steps

Refer to [Compile the openvela source code](./Build_Vela_from_sources.md).
