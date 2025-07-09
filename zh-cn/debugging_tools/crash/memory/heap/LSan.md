# LeakSanitizer (LSan) 使用指南

\[ [English](../../../../../en/debugging_tools/crash/memory/heap/LSan.md) | 简体中文 \]

## 一、概述

LeakSanitizer (LSan) 是一款高效的堆内存泄漏检测工具。它作为运行时工具，能够在程序退出时自动检测并报告未释放的内存，帮助开发者定位和修复内存泄漏问题。LSan 可以与 [AddressSanitizer](https://github.com/google/sanitizers/wiki/AddressSanitizer) (ASan) 或 [MemorySanitizer](https://github.com/google/sanitizers/wiki/MemorySanitizer) (MSan) 协同工作，也可以独立运行。

> 注意
>
> 在 openvela 环境中，LSan 目前仅支持在 **sim 仿真平台**上使用。

## 二、如何使用

### 步骤 1：启用 LSan

您可以通过以下配置启用 LSan。在 openvela 中，启用 ASan 会默认一同启用 LSan。

在配置文件中添加：

```Makefile
CONFIG_SIM_ASAN=y
```

### 步骤 2：执行泄漏检测

LSan 会在程序正常退出时（例如，在 openvela 中执行 `poweroff` 命令）自动运行，检查是否存在内存泄漏。

### 步骤 3：解读报告

当 LSan 检测到内存泄漏时，它会打印一份包含详细调用栈的报告。

#### 问题代码示例 (`hello_main.c`)

```Plaintext
// 在 hello_main.c 中添加以下代码
#include <stdlib.h>
int main(int argc, FAR char *argv[])
{
  // 分配了 100 字节内存但未释放
  malloc(100);
  printf("Hello, World!!\n");
  return 0;
}
```

#### 运行与输出

```Plaintext
nsh> hello
Hello, World!!
nsh> poweroff
=================================================================
==2283059==ERROR: LeakSanitizer: detected memory leaks
Direct leak of 100 byte(s) in 1 object(s) allocated from:
    #0 0x7fcadf13d93c in __interceptor_posix_memalign ...
    #1 0x5601710b789d in host_memalign sim/posix/sim_hostmemory.c:180
    ...
    #5 0x560170fd2974 in malloc umm_heap/umm_malloc.c:62
    #6 0x56017106a5d9 in hello_main ~/vela/apps/examples/hello/hello_main.c:38
    #7 0x560170fc82da in nxtask_startup sched/task_startup.c:70
    #8 0x560170fa6c15 in nxtask_start task/task_start.c:134
SUMMARY: AddressSanitizer: 100 byte(s) leaked in 1 allocation(s).
```

#### 报告解读

- `Direct leak of 100 byte(s) in 1 object(s)`: 指出存在一个 100 字节的直接内存泄漏。**直接泄漏**表示该内存块已不可从任何地方访问。
- 调用栈 (Call Stack): 报告中的堆栈跟踪信息是定位问题的关键。在本例中，`#6` 行清晰地显示泄漏发生在 `hello_main.c` 文件的第 38 行，即 `malloc(100)` 的调用处。

## 三、工作原理

LSan 无需编译器插桩，它通过在运行时拦截内存分配/释放函数（如 `malloc`, `free`, `new`, `delete`）来跟踪所有堆对象。其检测过程类似于垃圾回收 (Garbage Collection, GC) 中的标记-清除 (Mark-and-Sweep) 算法。

### 检测流程

1. **跟踪分配**: 程序运行时，LSan 记录所有在堆上分配的内存块。
2. **暂停程序**: 在程序退出或手动触发检测时，LSan 会暂停所有线程，以获得一个稳定的内存快照。
3. **确定根集合 (Root Set)**: LSan 扫描所有可能合法持有指向堆内存指针的根区域，包括：

    - 全局变量
    - 所有线程的栈 (Stack)
    - CPU 寄存器
    - 线程局部存储 (Thread-Local Storage, TLS)

4. **标记可达对象**: 从根集合出发，LSan 递归遍历所有指针，标记所有可被访问到的堆内存块。
5. **识别泄漏**: 遍历结束后，所有**未被标记**的堆内存块均被视为内存泄漏。
6. **生成报告**: LSan 报告所有泄漏的内存块，并附上其分配时记录的调用栈。

### 根集合的查找方式

对于需要深入了解其实现细节的用户，LSan 通过以下方式在底层获取根集合的具体内存区域：

- **全局变量区**：通过 `dl_iterate_phdr()` 遍历所有已加载的动态链接库（包括主程序），获取它们的全局数据段范围。
- **线程栈范围**：通过 `pthread_getattr_np()` 获取每个线程的栈地址和大小。
- **线程局部存储 (TLS)**：

    - 静态 TLS 区域通过内部 glibc 函数 `_dl_get_tls_static_info()` 定位。
    - 动态分配的 TLS 块则通过拦截链接器分配动态 TLS 空间时调用的 `__libc_memalign`，将这些分配的内存块直接视为根集合的一部分。

## 四、泄漏抑制 (Suppression)

在某些情况下，您可能需要忽略已知的、可接受的泄漏（例如，来自第三方库的已知问题，或设计上作为单例存在的对象）。LSan 允许您通过多种方式抑制这些泄漏报告。

最常用的方法是**使用抑制文件 (Suppression File)**。

### 操作步骤

1. 创建抑制文件。 创建一个文本文件，例如 `lsan.supp`。

2. 添加抑制规则。 在文件中按行添加规则。每条规则用于指定一个要忽略的泄漏来源。最常用的规则格式是                    `leak:function_name`，其中 `function_name` 是分配泄漏内存的函数名。

    **示例** (`lsan.supp`)

    ```Plain
    # 忽略由 my_singleton_alloc 函数分配的所有内存
    leak:my_singleton_alloc
    # 也可以忽略整个文件中发生的泄漏
    leak:third_party_library.c
    ```

    **说明**: 您可以直接从 LSan 报告的调用栈中复制函数名或文件名。

3. 指定抑制文件路径 通过 `LSAN_OPTIONS` 环境变量来告诉 LSan 抑制文件的位置。您需要在启动 `sim` 仿真环境之前设置此环境变量。

    ```Bash
    # 在 openvela 根目录下执行
    export LSAN_OPTIONS=suppressions=./lsan.supp
    ./build/bin/sim # 之后再启动仿真程序
    ```

    LSan 在运行时会读取这个文件，并忽略其中列出的所有泄漏源。

### 其他抑制方法

除了抑制文件，LSan 还支持在代码中直接忽略某个内存对象：

```C
#include <sanitizer/lsan_interface.h>
void *p = malloc(100);
__lsan_ignore_object(p); // 告诉 LSan 不要跟踪这个对象
```

这种方法适用于您能直接控制并获取到内存指针的场景。

## 五、FAQ

### 1、`fast-unwind` 兼容性问题

#### 问题描述

LSan 的 `fast-unwind` 堆栈回溯机制依赖于帧指针 (Frame Pointer) 且对当前任务的栈范围有严格要求。然而，openvela `sim` 模式的调度基于协程（使用 `setjmp`/`longjmp`），这导致线程切换后栈指针变化，使得 `fast-unwind` 的栈范围检查失败，从而无法捕获到内存泄漏。

#### 解决方案

 在 `sim` 模式下，默认禁用 `fast-unwind`，强制 LSan 使用标准的 `slow-unwind` 模式。该配置通过 `__lsan_default_options` 函数实现，确保 LSan 能正确回溯调用栈。

参考实现 (`nuttx/arch/sim/src/sim/sim_asan.c`):

```C
#ifdef CONFIG_SIM_ASAN
const char *__lsan_default_options(void)
{
  /* 
   * Disable fast-unwind to avoid unwind failure in NuttX's
   * coroutine-based scheduling model.
   */
  return "fast_unwind_on_malloc=0";
}
#endif
```

### 2、UBSan 误报问题

#### 问题描述

当启用 UndefinedBehaviorSanitizer (UBSan) 时，其内部操作（如 C++ 的 `dynamic_cast` 类型信息处理）在某些情况下会分配内存。这部分内存在程序退出时可能未被 UBSan 自身清理，导致 LSan 将其误报为内存泄漏。

#### 解决方案

为避免此类误报，可以配置一个 dummy 的 UBSan 模块。此方法保留了库的二进制兼容性，但在运行时屏蔽了 UBSan 的所有功能，从而消除了误报源。

**配置选项：**

```Makefile
CONFIG_MM_UBSAN=y
CONFIG_MM_UBSAN_DUMMY=y
```

## 六、调试技巧

### 为什么我的程序内存占用持续增长，但 LSan 却没有报告泄漏

这种情况通常是**逻辑内存泄漏（Logical Leak）**，而非 LSan 设计用来检测的**可达性泄漏 (Reachability Leak)**。

- **可达性泄漏**: 内存被分配后，所有指向它的指针都已丢失，程序无法再访问或释放它。这是 LSan 检测的目标。
- **逻辑内存泄漏**: 内存虽然在技术上仍然可达（例如，被一个全局列表或缓存持有），但从程序逻辑上看已不再需要。

#### 示例

一个全局的数据缓存不断添加新条目，但从未或很少移除旧的、无用的条目。

由于这些无用条目仍然被全局数据结构引用，LSan 认为它们是**可达的**，因此不会报告泄漏。然而，它们却实实在在地消耗着内存。

#### 应对策略

对于逻辑内存泄漏，您需要使用其他工具进行手动分析。例如，切换回系统内置的内存分配器，并使用 [Leak 检测]()介绍的方法手工检查内存占用变化，从而定位造成内存持续增长的模块。

## 七、参考文献

- [LeakSanitizer 官方文档](https://maskray.me/blog/2023-02-12-all-about-leak-sanitizer)
- [Apache NuttX PR #9186](https://github.com/apache/nuttx/pull/9186)
- [Apache NuttX PR #12659](https://github.com/apache/nuttx/pull/12659)