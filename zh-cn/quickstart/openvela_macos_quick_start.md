# 快速入门（macOS）

[ [English](../../en/quickstart/openvela_macos_quick_start.md) | 简体中文 ]

本指南将指导您在 **macOS（Apple Silicon）** 上完成 openvela 的开发环境准备、源代码下载、编译构建，并最终通过 Vela Emulator 运行编译产物。

openvela 的构建系统（`build.sh`、`emulator.sh`、`build/envsetup.sh`）内置了 `Darwin` 分支，代码清单（manifest）也提供了完整的 `darwin-aarch64` 预编译工具链（gcc / qemu / cmake / emulator / build-tools）。因此在 macOS 上可以进行原生开发，无需 Ubuntu 虚拟机。本文在 Ubuntu 流程的基础上，补充了 macOS 宿主机所需的若干适配。

> **环境要求**
>
> 本文适配 **Apple Silicon（arm64）** 机型的 macOS。预编译工具链仅提供 `darwin-aarch64`，因此不支持 Intel 芯片的 Mac。

> **AI 辅助搭建（可选）**
>
> 如果您使用 AI 编程助手（如 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)），可以通过 openvela AI Skills 自动完成以下全部搭建流程：
>
> ```bash
> git clone https://github.com/open-vela/.claude.git .claude
> ```
>
> 然后告诉 AI 助手："帮我在 macOS 上搭建 openvela 开发环境"。
>
> 如需手动搭建，请继续阅读以下步骤。

## 步骤一：准备工作

在开始之前，请确保您的开发环境满足以下要求。

### 1. 硬件要求

- **芯片：** Apple Silicon（M 系列，arm64）。
- **硬盘：** 至少 40 GB 可用空间，用于存放源代码和编译产物。
- **内存：** 至少 16 GB RAM。

### 2. 操作系统与基础工具

- **操作系统：** macOS（建议 13 Ventura 及以上）。
- **Xcode Command Line Tools：** 提供 `clang`、`ar`、`git`、`curl`、`libc++` 等。若未安装，执行：

    ```bash
    xcode-select --install
    ```

- **Homebrew：** 若未安装，请参考 [brew.sh](https://brew.sh)。

### 3. 安装开发工具

使用 Homebrew 安装编译 openvela 所需的软件包。与 Ubuntu 不同，macOS 自带的 `bash`（3.2）、`grep`、`sed`、`realpath` 为 BSD 版本，openvela 构建脚本依赖 GNU 版本，因此需要额外安装并前置到 `PATH`（由后文的 `macos-env.sh` 自动完成）。

```bash
brew install cmake git-lfs repo bash grep coreutils gnu-sed
```

### 4. 安装 Docker（用于 jidl 代码生成）

feature 框架的胶水代码生成器 `jidl_gen_cpp` 仅提供 Linux 二进制，需要通过容器运行。请安装并启动 [colima](https://github.com/abiosoft/colima) 或 Docker Desktop 其中之一：

```bash
brew install colima docker
colima start           # 或启动 Docker Desktop
```

### 5. 安装 Git LFS 组件

> **说明**：本项目包含大体积的二进制文件。请务必配置 **Git LFS**，**否则拉取的文件将损坏（仅显示为几 KB 的指针文本）而无法运行**。

```bash
git lfs install
```

## 步骤二：下载源代码

openvela 使用 `repo` 工具管理其分布在多个 Git 仓库中的源代码。上一步已通过 `brew install repo` 完成安装，可运行 `repo --version` 验证。

### 1. 初始化并同步代码库

1. 创建一个工作目录，用于存放 openvela 的所有源代码。

    ```bash
    mkdir openvela && cd openvela
    ```

2. 使用 `repo` 初始化项目清单。

    > **macOS 关键差异**：必须显式追加 `-g default,platform-darwin`。macOS 上 repo 的平台自动探测不会选中 `platform-darwin` 分组，若省略该参数，`darwin-aarch64` 预编译工具链（gcc/qemu/cmake/emulator）将不会被同步。

    请根据您的网络环境，从以下任一平台选择一种方式（推荐使用 SSH）来初始化仓库。

    #### 选项 A：从 GitHub 下载

    - 方式一：SSH（推荐）

        ```bash
        repo init -u ssh://git@github.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs -g default,platform-darwin
        ```

    - 方式二：HTTPS

        ```bash
        repo init -u https://github.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs -g default,platform-darwin
        ```

    #### 选项 B：从 Gitee 下载

    - 方式一：SSH（推荐）

        ```bash
        repo init -u ssh://git@gitee.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs -g default,platform-darwin
        ```

    - 方式二：HTTPS

        ```bash
        repo init -u https://gitee.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs -g default,platform-darwin
        ```

3. 执行同步命令。

    ```bash
    repo sync -c -j8
    ```

    > **操作提示**
    >
    > - 首次同步耗时较长（约 22 GB），具体时间取决于网络与磁盘性能。
    > - 若因网络问题中断，可重复执行 `repo sync` 进行增量同步。

## 步骤三：配置 macOS 构建环境

由于 macOS 与 Ubuntu 在工具链上的差异，在首次编译前需要完成以下适配。为便于复用，本文提供两个辅助脚本 `macos-env.sh` 与 `build-macos.sh`，请将[附录](#附录辅助脚本)中的内容分别保存到 openvela 源码根目录。

这些脚本会自动处理以下几点（均已对源码核实）：

| 差异点 | 说明 | 处理方式 |
| --- | --- | --- |
| **bash 版本** | `build.sh` source `envsetup.sh` 使用关联数组 `declare -A`、`${VAR:0:-1}` 等 bash 4+ 语法，macOS 自带 `/bin/bash` 仅 3.2 | 前置 Homebrew `bash` 5.x 到 `PATH` |
| **GNU 工具** | `build.sh` 用 `grep -oP`、`configure.sh` 用 `realpath --relative-to`、romfs 生成用 `sed -i`，均为 GNU 专属 | 前置 `grep`/`coreutils`/`gnu-sed` 的 `gnubin` |
| **cmake 遮蔽** | `prebuilts/tools/cmake/bin/cmake` 为 Linux ELF，被 `envsetup.sh` 前置遮蔽 | 符号链接到 arm64 版 `prebuilts/cmake/darwin-aarch64` |
| **jidl 生成器** | `jidl_gen_cpp` 为 Linux 二进制 | 通过 Docker（linux/amd64）运行原始二进制 |
| **ffmpeg 首次构建** | out-of-tree 首次 `make context` 时对象目录尚未创建 | `build-macos.sh` 自动重试一次 |

### 应用 quickjs 源码补丁

host 端 `qjsc` 工具的构建需要一处源码适配（`CONFIG_DARWIN` 未透传到该子工程，导致误用不存在的 `gcc-ar`，且 `quickjs.c` 未包含 `<sys/types.h>`）。请编辑 `apps/interpreters/quickjs/quickjs/CMakeLists.txt`：

1. 将顶部的：

    ```cmake
    if(CONFIG_DARWIN)
      set(CONFIG_CLANG y)
      set(CONFIG_DEFAULT_AR y)
    endif()
    ```

    改为：

    ```cmake
    if(CONFIG_DARWIN OR CMAKE_HOST_APPLE)
      set(CONFIG_CLANG y)
      set(CONFIG_DEFAULT_AR y)
    endif()
    ```

2. 在 `add_library(quickjs ${QUICKJS_SRC})` 之前插入：

    ```cmake
    if(CMAKE_HOST_APPLE)
      list(APPEND QUICKJS_COMMON_OPT -include sys/types.h)
    endif()
    ```

> **说明**：源码补丁属于 in-tree 改动，`repo sync --force-sync` 会将其还原，升级后需重新应用。`macos-env.sh` 中的 cmake 符号链接与 jidl wrapper 则会在每次 `source` 时自愈。

## 步骤四：编译源代码

完成上述配置后，在 openvela 根目录下执行编译。

### 1. （可选）自定义内核配置

```bash
source ./macos-env.sh
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake menuconfig
```

### 2. 执行编译

推荐使用一键脚本（已包含环境加载与 ffmpeg 首次构建重试）：

```bash
./build-macos.sh
```

或手动执行（注意 macOS 无 `nproc`，改用 `sysctl -n hw.ncpu`）：

```bash
source ./macos-env.sh
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake -j$(sysctl -n hw.ncpu)
```

编译成功后，您将在 `cmake_out/vela_goldfish-arm64-v8a-ap` 目录下找到 `nuttx`、`nuttx.bin` 等编译产物。

## 步骤五：运行模拟器

在 openvela 根目录下，执行以下脚本启动 `Vela Emulator` 并加载编译产物。

```bash
source ./macos-env.sh
./emulator.sh cmake_out/vela_goldfish-arm64-v8a-ap/
```

模拟器启动后，您将看到 `goldfish-armv8a-ap>` 提示符，表明 openvela 已成功运行。

> **模拟器加速**：`sysctl kern.hv_support` 返回 `1` 时，模拟器会使用 Hypervisor.framework 硬件加速。在受限/沙箱环境下会回退到 TCG 软件模拟（日志出现 `hvf is not enabled`、`mprotect failed` 警告），仍可启动，但速度较慢。

## 附录：辅助脚本

将以下两个脚本保存到 openvela 源码根目录。

### `macos-env.sh`

编译前 `source macos-env.sh` 一次。它会前置 GNU 工具链、修复 cmake 遮蔽、安装 jidl 的 Docker wrapper（均为幂等操作）。

```bash
# macos-env.sh — openvela macOS (Apple Silicon) 构建环境
_brew="$(brew --prefix 2>/dev/null || echo /opt/homebrew)"

export PATH="\
${_brew}/opt/grep/libexec/gnubin:\
${_brew}/opt/coreutils/libexec/gnubin:\
${_brew}/opt/gnu-sed/libexec/gnubin:\
${_brew}/bin:\
${PATH}"

# 自检
if ! command -v bash >/dev/null || [ "$(bash -c 'echo ${BASH_VERSINFO[0]}')" -lt 4 ]; then
  echo "[macos-env] 警告：bash 仍非 4+，请先 'brew install bash'" >&2
fi
if ! echo x | grep -oP 'x' >/dev/null 2>&1; then
  echo "[macos-env] 警告：grep 不支持 -P，请先 'brew install grep'" >&2
fi
if ! realpath --relative-to=/ / >/dev/null 2>&1; then
  echo "[macos-env] 警告：realpath 无 --relative-to，请先 'brew install coreutils'" >&2
fi

# ---- 修复 cmake 遮蔽（幂等）----
# envsetup.sh 把 prebuilts/tools/cmake/bin 前置到 PATH，但该目录的 cmake 是 Linux ELF，
# 而 arm64 cmake 在 prebuilts/cmake/darwin-aarch64。这里将前者符号链接到后者。
_repo_root="$(pwd)"
if [ -d "${_repo_root}/prebuilts/cmake/darwin-aarch64/bin" ] && [ -d "${_repo_root}/prebuilts/tools/cmake/bin" ]; then
  for _f in cmake ccmake cpack ctest; do
    _dst="${_repo_root}/prebuilts/cmake/darwin-aarch64/bin/${_f}"
    _lnk="${_repo_root}/prebuilts/tools/cmake/bin/${_f}"
    if [ -e "${_dst}" ] && [ ! "${_lnk}" -ef "${_dst}" ]; then
      ln -sf "${_dst}" "${_lnk}"
    fi
  done
  echo "[macos-env] cmake 已指向 arm64: $(prebuilts/tools/cmake/bin/cmake --version 2>/dev/null | head -1)"
fi
unset _f _dst _lnk _repo_root

# ---- 修复 jidl_gen_cpp（幂等，Docker 方案）----
# jidl_gen_cpp 是 Linux x86-64 二进制，macOS 无法原生执行，用 Docker 运行原始二进制。
_jidl="$(pwd)/prebuilts/tools/rust/bin/jidl/jidl_gen_cpp"
_img="${JIDL_DOCKER_IMAGE:-ubuntu:22.04}"
if command -v docker >/dev/null 2>&1; then
  if ! docker image inspect "${_img}" >/dev/null 2>&1; then
    echo "[macos-env] 拉取 jidl 运行镜像 ${_img} ..." >&2
    docker pull --platform linux/amd64 "${_img}" >/dev/null 2>&1 || \
      echo "[macos-env] 警告：镜像拉取失败，jidl 生成会失败（检查 docker/colima 与网络）" >&2
  fi
  if [ -e "${_jidl}" ] && ! head -1 "${_jidl}" 2>/dev/null | grep -q '^#!.*bash'; then
    [ -f "${_jidl}.linux" ] || cp "${_jidl}" "${_jidl}.linux"
    cat > "${_jidl}" <<'JIDL_WRAP'
#!/usr/bin/env bash
set -euo pipefail
_self="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${_self}/../../../../.." && pwd)"
IMAGE="${JIDL_DOCKER_IMAGE:-ubuntu:22.04}"
BIN="${ROOT}/prebuilts/tools/rust/bin/jidl/jidl_gen_cpp.linux"
exec docker run --rm --platform linux/amd64 -v "${ROOT}:${ROOT}" -w "$(pwd)" "${IMAGE}" "${BIN}" "$@"
JIDL_WRAP
    chmod +x "${_jidl}"
    echo "[macos-env] jidl_gen_cpp 已替换为 Docker wrapper（运行原始 Linux 二进制）"
  fi
else
  echo "[macos-env] 警告：未找到 docker，jidl_gen_cpp 无法在 macOS 运行（需 colima/Docker Desktop）" >&2
fi
unset _jidl _img

echo "[macos-env] 已就绪: bash=$(bash --version | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1), grep=$(command -v grep), realpath=$(command -v realpath)"
unset _brew
```

### `build-macos.sh`

一键编译脚本。会自动加载环境，并在首次失败时重试一次以覆盖 ffmpeg 对象目录的首建顺序问题。

```bash
#!/usr/bin/env bash
# build-macos.sh — 在 macOS (Apple Silicon) 上一键编译 openvela 目标
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CONFIG="${1:-vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/}"
shift || true
EXTRA_TARGET=("$@")
JOBS="-j$(sysctl -n hw.ncpu 2>/dev/null || echo 8)"

source ./macos-env.sh

run_build() { ./build.sh "${CONFIG}" --cmake "${JOBS}" "${EXTRA_TARGET[@]}"; }

echo "=== build-macos: ${CONFIG} ${EXTRA_TARGET[*]} ${JOBS} ==="
if run_build; then echo "=== 构建成功 ==="; exit 0; fi

echo "=== 首次构建失败，自动重试一次（覆盖 ffmpeg 对象目录首建顺序问题）==="
if run_build; then echo "=== 重试后构建成功 ==="; exit 0; fi
echo "=== 构建仍失败，请查看上方日志 ===" >&2
exit 1
```

## 后续步骤

- 常见问题

    - [快速入门常见问题](../faq/QuickStart_FAQ.md)
    - [开发者常见问题解答](../faq/devoloper_tech_faq.md)

- 进一步阅读

    - [快速入门（Ubuntu）](./openvela_ubuntu_quick_start.md)
    - [使用模拟器调试](./emulator/Debugging_Vela_with_Vela_Emulator_zh-cn.md)
