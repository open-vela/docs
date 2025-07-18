# 日志管理与故障排查

\[ [English](../../../../en/device_dev_guide/kernel/logging/troubleshooting.md) | 简体中文 \]

本文档旨在阐述在 openvela 系统中处理高级日志记录场景时遇到的常见问题，并提供相应的解决方案与最佳实践。内容涵盖日志并发、`ramlog` 初始化及 Android API 兼容性。

## 一、解决日志交叉输出问题

### 问题描述

在多核（SMP）或并发环境下，来自不同执行单元（如多核线程、中断服务程序）的日志输出可能会相互交错，导致单条日志信息被截断或混杂，降低日志的可读性。

**根本原因**：日志输出操作并非原子性（Atomic）。当一个任务的日志正在通过串口等设备输出时，操作系统可能会调度另一个高优先级任务（或响应一个中断），该任务同样会尝试输出日志，从而打断前一个未完成的输出。

为确保每条日志的完整性和原子性，我们推荐以下三种解决方案，可根据系统需求组合使用。

### 解决方案

#### 方案一：启用日志行缓冲机制

此机制通过在内存中构建完整的日志行，然后一次性提交给底层驱动程序，从而避免在输出过程中被其他任务打断。

您需要启用 `syslog` 的相关缓冲配置：

- `CONFIG_SYSLOG_BUFFER=y`: 为应用程序和内核线程启用 `syslog` 缓冲区。
- `CONFIG_SYSLOG_INTBUFFER=y`: 专门为中断服务程序（ISR）提供一个独立的 `syslog` 缓冲区，避免与线程竞争。

#### 方案二：优化 `printf` 与 `syslog` 的混合使用

当系统中必须同时使用 `printf` 和 `syslog` 时，为 `printf`（及其底层的 `stdio`）也启用行缓冲，并配置充足的缓冲区大小，可以显著降低交叉打印的概率。

建议启用以下配置：

```Makefile
# 为标准输出（stdout）启用行缓冲
CONFIG_STDIO_LINEBUFFER=y

# 为标准 I/O 流分配缓冲区，建议 512 字节或以上
CONFIG_STDIO_BUFFER_SIZE=512
CONFIG_STREAM_OUT_BUFFER_SIZE=256

# 为底层串口驱动配置充足的 TX/RX 缓冲区，以应对突发数据
CONFIG_UART0_TXBUFSIZE=1024
CONFIG_UART0_RXBUFSIZE=1024
```

#### 方案三：利用硬件特性实现原子性输出

对于性能要求极高的场景，可利用底层硬件特性来保证输出的原子性。

1. **实现 `up_nputs` 接口**：芯片驱动程序（BSP）应实现 `up_nputs` 函数。此函数通常通过关中断或使用自旋锁（Spinlock）等方式，确保在输出一个完整的字符串期间不会被抢占，从而实现硬件层面的原子性。
2. **启用 DMA 传输**：如果串口（UART）硬件支持直接内存访问（DMA），应优先启用。DMA 控制器一旦启动，便会在后台将完整的日志缓冲区数据传输到串口，此过程不占用 CPU，也不会被其他线程打断，是实现高效、原子性日志输出的最佳方式。

## 二、解决 `ramlog` 冷启动时的日志乱码问题

### 问题描述

`ramlog` 是一种将日志记录在 RAM 中的机制，它允许设备在发生软件复位（Warm Reset）后依然保留崩溃前的日志信息。但在系统完全断电后重启（Cold Start）时，RAM 中的数据是随机的，直接读取会导致日志乱码。

### 解决方案

通过在 `ramlog` 缓冲区中引入校验签名（Magic Number）和持久化读写指针，实现对启动类型的判断和快速初始化。

#### 设计思路

1. 校验签名 (Magic Number)：在 `ramlog` 环形缓冲区（Ring Buffer）的固定位置（如末尾）预留 4 字节，用于存储一个预定义的、非零的特殊值（即校验签名）。
2. 持久化指针：在缓冲区内额外存储 `head` 和 `tail` 指针的当前值。

#### 初始化流程

系统启动时，`ramlog` 驱动应执行以下逻辑：

1. 检查校验签名：

    - **签名不匹配**：判断为冷启动。此时 RAM 内容无效。
        - 使用 `memset` 将整个 `ramlog` 缓冲区清零。
        - 将 `head` 和 `tail` 指针初始化为 `0`。
        - 在固定位置写入正确的校验签名。
    - **签名匹配**：判断为热复位。此时 RAM 中保留了有效的日志。
        - 直接读取已保存在 RAM 中的 `head` 和 `tail` 指针值，快速恢复日志读写状态。
        - 无需清空缓冲区，保留了复位前的最后日志。

通过此机制，`ramlog` 不仅能有效区分冷、热启动，还能在热复位后快速恢复，为问题诊断提供关键依据。

## 三、兼容 Android 日志 API

openvela 系统原生兼容标准的 Android NDK 日志接口，使熟悉 Android 应用开发的工程师能够无缝迁移日志记录代码。

- **直接使用**：开发者可以直接引入 `<android/log.h>` 头文件，并使用其中定义的所有日志 API 和宏，例如 `__android_log_print()`。
- **无需修改**：现有的 Android C/C++ 项目中的日志代码无需任何修改即可在 openvela 系统上编译和运行。

## 四、相关文档

- [系统日志 (Syslog) 深度解析](./syslog.md)
- [printf 函数使用规范](./printf.md)

## 五、参考资料

- [Logging  |  Android NDK  |  Android Developers](https://developer.android.com/ndk/reference/group/logging)
- [Using Asserts in Embedded Systems | Interrupt (memfault.com)](https://interrupt.memfault.com/blog/asserts-in-embedded-systems)
- [Exploring printf on Cortex-M | Interrupt (memfault.com)](https://interrupt.memfault.com/blog/printf-on-embedded)
- https://kb.segger.com/DCC
- https://github.com/eyalroz/printf
- https://interrupt.memfault.com/blog/device-logging