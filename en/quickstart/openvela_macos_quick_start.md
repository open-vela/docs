# Quick Start (macOS)

[ English | [简体中文](../../zh-cn/quickstart/openvela_macos_quick_start.md) ]

This guide walks you through preparing the openvela development environment on **macOS (Apple Silicon)**, downloading the source, building it, and finally running the output in the Vela Emulator.

The openvela build system (`build.sh`, `emulator.sh`, `build/envsetup.sh`) ships with a `Darwin` branch, and the manifest provides a full `darwin-aarch64` prebuilt toolchain (gcc / qemu / cmake / emulator / build-tools). Native development on macOS is therefore possible without an Ubuntu VM. On top of the Ubuntu flow, this guide adds the host adaptations that macOS requires.

> **Requirements**
>
> This guide targets macOS on **Apple Silicon (arm64)**. The prebuilt toolchain is only provided for `darwin-aarch64`, so Intel-based Macs are not supported.

> **AI-assisted setup (optional)**
>
> If you use an AI coding assistant (such as [Claude Code](https://docs.anthropic.com/en/docs/claude-code)), the openvela AI Skills can complete the whole setup for you:
>
> ```bash
> git clone https://github.com/open-vela/.claude.git .claude
> ```
>
> Then ask the assistant: "Set up the openvela development environment on macOS for me." To set up manually, read on.

## Step 1: Preparation

### 1. Hardware

- **Chip:** Apple Silicon (M series, arm64).
- **Disk:** At least 40 GB free.
- **Memory:** At least 16 GB RAM.

### 2. OS and base tools

- **OS:** macOS (13 Ventura or later recommended).
- **Xcode Command Line Tools** (provides `clang`, `ar`, `git`, `curl`, `libc++`). Install with:

    ```bash
    xcode-select --install
    ```

- **Homebrew** — see [brew.sh](https://brew.sh) if not installed.

### 3. Install build tools

Unlike Ubuntu, the `bash` (3.2), `grep`, `sed`, and `realpath` bundled with macOS are BSD variants, while the openvela build scripts rely on the GNU versions. Install them and prepend them to `PATH` (handled automatically by `macos-env.sh` below).

```bash
brew install cmake git-lfs repo bash grep coreutils gnu-sed
```

### 4. Install Docker (for jidl code generation)

The feature-framework glue-code generator `jidl_gen_cpp` is only shipped as a Linux binary and must run in a container. Install and start [colima](https://github.com/abiosoft/colima) or Docker Desktop:

```bash
brew install colima docker
colima start           # or start Docker Desktop
```

### 5. Install Git LFS

> **Note**: This project contains large binary files. You **must** configure **Git LFS**, otherwise the fetched files are corrupted (only a few-KB pointer text) and will not run.

```bash
git lfs install
```

## Step 2: Download the source

openvela uses `repo` to manage source spread across multiple Git repositories (installed via `brew install repo` above; verify with `repo --version`).

### 1. Initialize and sync

1. Create a working directory.

    ```bash
    mkdir openvela && cd openvela
    ```

2. Initialize the manifest.

    > **Key macOS difference**: you must append `-g default,platform-darwin`. On macOS repo's platform auto-detection does not select the `platform-darwin` group; without it the `darwin-aarch64` prebuilt toolchain (gcc/qemu/cmake/emulator) is not synced.

    Pick one platform below (SSH recommended).

    #### Option A: GitHub

    - SSH (recommended)

        ```bash
        repo init -u ssh://git@github.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs -g default,platform-darwin
        ```

    - HTTPS

        ```bash
        repo init -u https://github.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs -g default,platform-darwin
        ```

    #### Option B: Gitee

    - SSH (recommended)

        ```bash
        repo init -u ssh://git@gitee.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs -g default,platform-darwin
        ```

    - HTTPS

        ```bash
        repo init -u https://gitee.com/open-vela/manifests.git -b dev-ai-contest-2026 -m openvela.xml --repo-url=https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/ --git-lfs -g default,platform-darwin
        ```

3. Sync.

    ```bash
    repo sync -c -j8
    ```

    > **Tips**
    >
    > - The first sync takes a while (~22 GB) depending on network and disk.
    > - If interrupted, re-run `repo sync` for an incremental sync.

## Step 3: Configure the macOS build environment

Because of toolchain differences between macOS and Ubuntu, a few adaptations are required before the first build. Two helper scripts, `macos-env.sh` and `build-macos.sh`, are provided; save the contents from the [Appendix](#appendix-helper-scripts) into the openvela source root.

These scripts handle the following (all verified against the source):

| Difference | Detail | Handling |
| --- | --- | --- |
| **bash version** | `build.sh` sources `envsetup.sh`, which uses associative arrays (`declare -A`) and `${VAR:0:-1}` — bash 4+ syntax; macOS ships bash 3.2 | Prepend Homebrew `bash` 5.x to `PATH` |
| **GNU tools** | `build.sh` uses `grep -oP`, `configure.sh` uses `realpath --relative-to`, romfs generation uses `sed -i` — all GNU-specific | Prepend `grep`/`coreutils`/`gnu-sed` gnubin |
| **cmake shadowing** | `prebuilts/tools/cmake/bin/cmake` is a Linux ELF prepended onto `PATH` by `envsetup.sh` | Symlink to the arm64 build under `prebuilts/cmake/darwin-aarch64` |
| **jidl generator** | `jidl_gen_cpp` is a Linux binary | Run the original binary via Docker (linux/amd64) |
| **ffmpeg first build** | On the first out-of-tree `make context`, object directories are not yet created | `build-macos.sh` retries once |

### Apply the quickjs source patch

Building the host `qjsc` tool needs one source adaptation (`CONFIG_DARWIN` is not propagated to that sub-project, so it wrongly uses the non-existent `gcc-ar`, and `quickjs.c` does not include `<sys/types.h>`). Edit `apps/interpreters/quickjs/quickjs/CMakeLists.txt`:

1. Change the top block from:

    ```cmake
    if(CONFIG_DARWIN)
      set(CONFIG_CLANG y)
      set(CONFIG_DEFAULT_AR y)
    endif()
    ```

    to:

    ```cmake
    if(CONFIG_DARWIN OR CMAKE_HOST_APPLE)
      set(CONFIG_CLANG y)
      set(CONFIG_DEFAULT_AR y)
    endif()
    ```

2. Insert before `add_library(quickjs ${QUICKJS_SRC})`:

    ```cmake
    if(CMAKE_HOST_APPLE)
      list(APPEND QUICKJS_COMMON_OPT -include sys/types.h)
    endif()
    ```

> **Note**: The source patch is an in-tree change; `repo sync --force-sync` reverts it, so re-apply after upgrades. The cmake symlinks and jidl wrapper in `macos-env.sh` self-heal on every `source`.

## Step 4: Build

### 1. (Optional) Customize the kernel config

```bash
source ./macos-env.sh
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake menuconfig
```

### 2. Build

Recommended one-shot script (loads the environment and retries the ffmpeg first build):

```bash
./build-macos.sh
```

Or manually (macOS has no `nproc`; use `sysctl -n hw.ncpu`):

```bash
source ./macos-env.sh
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake -j$(sysctl -n hw.ncpu)
```

On success you will find `nuttx`, `nuttx.bin`, etc. under `cmake_out/vela_goldfish-arm64-v8a-ap`.

## Step 5: Run the emulator

```bash
source ./macos-env.sh
./emulator.sh cmake_out/vela_goldfish-arm64-v8a-ap/
```

When the `goldfish-armv8a-ap>` prompt appears, openvela is running.

> **Acceleration**: When `sysctl kern.hv_support` returns `1`, the emulator uses the Hypervisor.framework for hardware acceleration. In restricted/sandboxed environments it falls back to TCG software emulation (with `hvf is not enabled` / `mprotect failed` warnings) — it still boots, just slower.

## Appendix: Helper scripts

Save the following two scripts into the openvela source root.

### `macos-env.sh`

`source macos-env.sh` once before building. It prepends the GNU toolchain, fixes the cmake shadowing, and installs the jidl Docker wrapper (all idempotent).

```bash
# macos-env.sh — openvela macOS (Apple Silicon) build environment
_brew="$(brew --prefix 2>/dev/null || echo /opt/homebrew)"

export PATH="\
${_brew}/opt/grep/libexec/gnubin:\
${_brew}/opt/coreutils/libexec/gnubin:\
${_brew}/opt/gnu-sed/libexec/gnubin:\
${_brew}/bin:\
${PATH}"

# self-checks
if ! command -v bash >/dev/null || [ "$(bash -c 'echo ${BASH_VERSINFO[0]}')" -lt 4 ]; then
  echo "[macos-env] warn: bash still < 4, run 'brew install bash'" >&2
fi
if ! echo x | grep -oP 'x' >/dev/null 2>&1; then
  echo "[macos-env] warn: grep lacks -P, run 'brew install grep'" >&2
fi
if ! realpath --relative-to=/ / >/dev/null 2>&1; then
  echo "[macos-env] warn: realpath lacks --relative-to, run 'brew install coreutils'" >&2
fi

# ---- fix cmake shadowing (idempotent) ----
# envsetup.sh prepends prebuilts/tools/cmake/bin, whose cmake is a Linux ELF;
# the arm64 cmake lives in prebuilts/cmake/darwin-aarch64. Symlink the former to the latter.
_repo_root="$(pwd)"
if [ -d "${_repo_root}/prebuilts/cmake/darwin-aarch64/bin" ] && [ -d "${_repo_root}/prebuilts/tools/cmake/bin" ]; then
  for _f in cmake ccmake cpack ctest; do
    _dst="${_repo_root}/prebuilts/cmake/darwin-aarch64/bin/${_f}"
    _lnk="${_repo_root}/prebuilts/tools/cmake/bin/${_f}"
    if [ -e "${_dst}" ] && [ ! "${_lnk}" -ef "${_dst}" ]; then
      ln -sf "${_dst}" "${_lnk}"
    fi
  done
  echo "[macos-env] cmake now arm64: $(prebuilts/tools/cmake/bin/cmake --version 2>/dev/null | head -1)"
fi
unset _f _dst _lnk _repo_root

# ---- fix jidl_gen_cpp (idempotent, Docker) ----
# jidl_gen_cpp is a Linux x86-64 binary; run the original via Docker.
_jidl="$(pwd)/prebuilts/tools/rust/bin/jidl/jidl_gen_cpp"
_img="${JIDL_DOCKER_IMAGE:-ubuntu:22.04}"
if command -v docker >/dev/null 2>&1; then
  if ! docker image inspect "${_img}" >/dev/null 2>&1; then
    echo "[macos-env] pulling jidl image ${_img} ..." >&2
    docker pull --platform linux/amd64 "${_img}" >/dev/null 2>&1 || \
      echo "[macos-env] warn: image pull failed; jidl will fail (check docker/colima and network)" >&2
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
    echo "[macos-env] jidl_gen_cpp replaced with Docker wrapper (runs the original Linux binary)"
  fi
else
  echo "[macos-env] warn: docker not found; jidl_gen_cpp cannot run on macOS (needs colima/Docker Desktop)" >&2
fi
unset _jidl _img

echo "[macos-env] ready: bash=$(bash --version | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1), grep=$(command -v grep), realpath=$(command -v realpath)"
unset _brew
```

### `build-macos.sh`

One-shot build script. Loads the environment and retries once on first failure to cover the ffmpeg object-directory ordering issue.

```bash
#!/usr/bin/env bash
# build-macos.sh — one-shot openvela build on macOS (Apple Silicon)
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CONFIG="${1:-vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/}"
shift || true
EXTRA_TARGET=("$@")
JOBS="-j$(sysctl -n hw.ncpu 2>/dev/null || echo 8)"

source ./macos-env.sh

run_build() { ./build.sh "${CONFIG}" --cmake "${JOBS}" "${EXTRA_TARGET[@]}"; }

echo "=== build-macos: ${CONFIG} ${EXTRA_TARGET[*]} ${JOBS} ==="
if run_build; then echo "=== build ok ==="; exit 0; fi

echo "=== first build failed; retrying once (covers ffmpeg object-dir ordering) ==="
if run_build; then echo "=== build ok after retry ==="; exit 0; fi
echo "=== build still failing; see logs above ===" >&2
exit 1
```

## Next steps

- FAQ

    - [Quick Start FAQ](../faq/QuickStart_FAQ.md)
    - [Developer Technical FAQ](../faq/devoloper_tech_faq.md)

- Further reading

    - [Quick Start (Ubuntu)](./openvela_ubuntu_quick_start.md)
    - [Debugging with Vela Emulator](./emulator/Debugging_Vela_with_Vela_Emulator.md)
