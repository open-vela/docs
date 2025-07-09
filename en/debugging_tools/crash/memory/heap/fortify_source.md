# Enhancing C Memory Safety with _FORTIFY_SOURCE

\[ English | [简体中文](./../../../../../zh-cn/debugging_tools/crash/memory/heap/fortify_source.md) \]

This document provides a comprehensive overview of the features, configuration, and principles of **_FORTIFY_SOURCE**, and it analyzes its differences compared to **KASan**. By reading this document, developers can understand how to leverage _FORTIFY_SOURCE to detect and prevent out-of-bounds issues caused by library functions, thereby improving application security.

## I. Overview

In C language development, unsafe function calls (e.g., `memcpy`, `memset`) are a common cause of buffer overflows, which can lead to program crashes or security vulnerabilities.

**_FORTIFY_SOURCE** is a compiler feature that adds an extra layer of boundary checking to your applications by replacing unsafe standard library functions at compile time. This feature helps you quickly identify and fix memory out-of-bounds issues caused by library function calls during both development and runtime. Its primary advantage is its extremely **low overhead**, making it suitable for continuous use in production environments.

## II. How to Enable

To enable the **_FORTIFY_SOURCE** feature, you must meet specific prerequisites and apply the corresponding configuration.

### Prerequisites

- **Compiler Optimization Level**: You must set the compiler optimization level to **-O2** or higher.
- **Compiler Version**:

    - To use the highest check level (**Level 3**), you need GCC 12+ or Clang 16+.
    - For versions of GCC below 12, set the check level to **2** (Level 2).

### Configuration Levels

You can set the security check level using the **CONFIG_FORTIFY_SOURCE** macro definition.

```Makefile
# Set in the project's Kconfig or Makefile
CONFIG_FORTIFY_SOURCE=3
```

**_FORTIFY_SOURCE** offers three different check levels:

- Level **1**: Performs checks at compile time. The compiler can detect and warn about some overflows that can be identified during compilation.
- Level **2**: Builds on Level 1 by adding runtime size checks for stack and global variables. This is the most commonly used level.
- Level **3**: Builds on Level 2 by adding runtime size checks for dynamically allocated memory on the heap (e.g., allocated via `malloc`).

## III. How It Works

The core mechanism of **_FORTIFY_SOURCE** relies on a set of intrinsic functions provided by the GNU Compiler Collection (GCC).

### Compiler Intrinsics

- `__builtin_object_size(ptr, type)`: The compiler uses this function at compile time to determine the size of the object pointed to by `ptr`.
- `__builtin_dynamic_object_size(ptr, type)`: Introduced in GCC 12, this function is used to get the size of dynamically allocated objects at runtime.

When you enable **_FORTIFY_SOURCE**, the C standard library headers use macro definitions to redirect function calls like `memcpy` to their corresponding `_fortify` versions. These `_fortify` versions internally call the aforementioned intrinsic functions to get the size of the destination buffer and perform a bounds check before executing the actual operation.

### Function Wrapping Example

The following example shows how the `memcpy` function is wrapped in **openvela** to integrate **_FORTIFY_SOURCE** checks.

```C
/**
 * @brief Wraps the memcpy function with _FORTIFY_SOURCE.
 *
 * @param dest A pointer to the destination memory area.
 * @param src  A pointer to the source memory area.
 * @param n    The number of bytes to copy.
 * @return     Returns a pointer to the destination memory area, dest.
 */
fortify_function(memcpy) FAR void *memcpy(FAR void *dest,
                                          FAR const void *src,
                                          size_t n)
{
  /*
   * Use fortify_size to get the size of the destination and source buffers.
   * If the copy length n exceeds either buffer's boundary, an assertion is
   * triggered. fortify_size internally calls __builtin_object_size.
   */
  fortify_assert(n <= fortify_size(dest, 0) && n <= fortify_size(src, 0));
  /*
   * Call the original, unwrapped memcpy function.
   * __real_memcpy points to the original function implementation,
   * typically via linker scripts or macro tricks.
   */
  return __real_memcpy(dest, src, n);
}
```

Currently, **_FORTIFY_SOURCE** provides broad coverage for most functions with overflow risks in headers such as `string.h`, `stdio.h`, and `unistd.h`.

## IV. Comparison with KASan

Kernel Address Sanitizer (KASan) is another powerful memory error detection tool. The table below compares the key features of **_FORTIFY_SOURCE** and **KASan**.

| Feature Comparison                 | _FORTIFY_SOURCE                                | KASan (Kernel Address Sanitizer)          |
| ---------------------------------- | ---------------------------------------------- | ----------------------------------------- |
| **Detection Scope**                | Checks only wrapped standard library functions | Checks all memory read/write operations   |
| **Stack & Global Variable Checks** | Supported                                      | Not supported                             |
| **Heap Variable Checks**           | Supported (Level 3)                            | Supported                                 |
| **Memory Overhead (ROM/RAM)**      | Minimal                                        | Large                                     |
| **Runtime Performance Overhead**   | Negligible                                     | Significant (can cause major degradation) |

### Conclusion

**_FORTIFY_SOURCE** and **KASan** are complementary memory safety tools:

- **_FORTIFY_SOURCE**: Lightweight and low-overhead, suitable as a **default-on** security baseline to protect against common overflows caused by standard library function calls.
- **KASan**: Heavyweight and high-overhead, ideal for use during the **debugging phase** to detect more complex memory errors, such as `use-after-free` and `double-free`.

## V. Further Reading

You can consult the following resources for more technical details about **_FORTIFY_SOURCE**:

- [GCC's new fortification level](https://developers.redhat.com/articles/2022/09/17/gccs-new-fortification-level)
- [Enhance application security with _FORTIFY_SOURCE](https://www.redhat.com/en/blog/enhance-application-security-fortifysource)
- [_FORTIFY_SOURCE](https://maskray.me/blog/2022-11-06-fortify-source)
- [Use source-level annotations to help GCC detect buffer overflows](https://developers.redhat.com/articles/2021/06/25/use-source-level-annotations-help-gcc-detect-buffer-overflows)
