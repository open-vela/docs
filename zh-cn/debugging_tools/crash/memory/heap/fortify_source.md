# Enhancing C Memory Safety with _FORTIFY_SOURCE

\[ [English](../../../../../en/debugging_tools/crash/memory/heap/fortify_source.md) | 简体中文 \]

本文档全面介绍了 _FORTIFY_SOURCE 的功能、配置和原理，并对其与 KASan 的差异进行了分析。通过阅读本文，开发者可以理解如何利用 **_FORTIFY_SOURCE** 检测并避免库函数引发的越界问题，从而提升应用程序的安全性。

## 一、概述

在 C 语言程序开发中，不安全的函数调用（例如 **`memcpy`**、**`memset`**）是导致缓冲区溢出的常见原因，这可能引发程序崩溃或安全漏洞。

**`_FORTIFY_SOURCE`** 是一项编译器特性，它通过在编译时替换标准库中不安全的函数，为您的应用程序增加一层额外的边界检查。此功能帮助您在开发和运行阶段快速定位并修复由库函数调用引起的内存越界问题。其主要优势在于开销极低，适合在生产环境中持续开启。

## 二、如何启用

要启用 **`_FORTIFY_SOURCE`** 功能，您需要满足特定前提条件并进行相应配置。

### 前提条件

- **编译优化等级**: 您必须将编译优化等级设置为 **`-O2`** 或更高。
- **编译器版本:**

    - 要使用最高的检查等级（Level 3），您需要使用 GCC 12+ 或 Clang 16+。
    - 对于 GCC 12 以下的版本，请将检查等级设置为 2（Level 2）。

### 配置等级

您可以通过 **`CONFIG_FORTIFY_SOURCE`** 宏定义来设置安全检查的等级。

```Makefile
# 在项目的 Kconfig 或 Makefile 中设置
CONFIG_FORTIFY_SOURCE=3
```

**`_FORTIFY_SOURCE`** 提供三个不同的检查等级：

- Level **1**: 在编译时执行检查。编译器可以检测并警告一部分在编译期就能确定存在溢出的代码。
- Level **2**: 在 Level **1** 的基础上，增加对栈（Stack）变量和全局变量的运行时大小检查。这是最常用的等级。
- Level **3**: 在 Level **2** 的基础上，增加对堆（Heap）上动态分配内存（例如通过 `malloc` 分配）的运行时大小检查。

## 三、工作原理

**`_FORTIFY_SOURCE`** 的核心依赖于 GNU 编译器套件（GNU Compiler Collection, GCC）提供的一组内建函数（Intrinsics）。

### 编译器内建函数

- **`__builtin_object_size`**`(ptr, type)`: 编译器在编译时使用此函数来推断指针 **`ptr`** 所指向对象的大小。
- **`__builtin_dynamic_object_size`**`(ptr, type)`: GCC 12 中引入，用于在运行时获取动态分配对象的大小。

当您启用 **`_FORTIFY_SOURCE`** 后，C 标准库的头文件会使用宏定义，将 **`memcpy`** 等函数调用重定向到其对应的 **`_fortify`** 版本。这些 **`_fortify`** 版本内部会调用上述内建函数来获取目标缓冲区的大小，并在执行实际操作前进行边界检查。

### 函数包装示例

以下示例展示了在 openvela 中如何包装 **`memcpy`** 函数以集成 **`_FORTIFY_SOURCE`** 检查。

```C
/**
 * @brief 使用 _FORTIFY_SOURCE 包装 memcpy 函数。
 *
 * @param dest 目标内存区域的指针。
 * @param src  源内存区域的指针。
 * @param n    要复制的字节数。
 * @return     返回指向目标内存区域的指针 dest。
 */
fortify_function(memcpy) FAR void *memcpy(FAR void *dest,
                                          FAR const void *src,
                                          size_t n)
{
  /*
   * 使用 fortify_size 获取目标和源缓冲区的大小，
   * 如果要复制的长度 n 超出任一缓冲区边界，则触发断言。
   * fortify_size 内部会调用 __builtin_object_size。
   */
  fortify_assert(n <= fortify_size(dest, 0) && n <= fortify_size(src, 0));
  /*
   * 调用原始的、未被包装的 memcpy 函数。
   * __real_memcpy 是通过链接器脚本或宏技巧指向的原始函数实现。
   */
  return __real_memcpy(dest, src, n);
}
```

目前，**`_FORTIFY_SOURCE`** 已广泛覆盖 **`string.h`**、**`stdio.h`**、**`unistd.h`** 等头文件中大多数存在溢出风险的函数。

## 四、和 KASan 的对比

内核地址空间清理器（Kernel Address Sanitizer, KASan）是另一种强大的内存错误检测工具。下表对比了 `_FORTIFY_SOURCE` 和 KASan 的关键特性。

| 特性对比           | _FORTIFY_SOURCE              | KASan (内核地址空间清理器)  |
| ------------------ | ---------------------------- | --------------------------- |
| 检测范围           | 仅检查被包装的标准库函数调用 | 检查所有内存读写操作        |
| 栈与全局变量检查   | 支持                         | 不支持                      |
| 堆变量检查         | 支持 (Level 3)               | 支持                        |
| 内存开销 (ROM/RAM) | 极小                         | 大                          |
| 运行时性能开销     | 可忽略不计                   | 显著 (可能导致性能大幅降低) |

### 结论

`_FORTIFY_SOURCE` 和 KASan 是互补的内存安全工具：

- **_FORTIFY_SOURCE**: 轻量级、低开销，适合作为**默认开启**的安全基线，用于防范由标准库函数调用引起的常见溢出。
- **KASan**: 重量级、高开销，适合在**调试阶段**使用，用于检测更复杂的内存错误，例如越界读写（Use-after-free）、双重释放（Double-free）等。

## 五、进一步阅读

您可以查阅以下资源，获取关于 **`_FORTIFY_SOURCE`** 的更多技术细节：

- [GCC's new fortification level](https://developers.redhat.com/articles/2022/09/17/gccs-new-fortification-level)
- [Enhance application security with _FORTIFY_SOURCE](https://www.redhat.com/en/blog/enhance-application-security-fortifysource)
- [_FORTIFY_SOURCE](https://maskray.me/blog/2022-11-06-fortify-source)
- [Use source-level annotations to help GCC detect buffer overflows](https://developers.redhat.com/articles/2021/06/25/use-source-level-annotations-help-gcc-detect-buffer-overflows)