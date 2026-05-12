# 原子操作

\[ [English](../../../../en/device_dev_guide/kernel/resource_sync/atomic_operation.md) | 简体中文 \]

本文档介绍在 openvela 系统中如何使用符合 C11 标准的原子操作接口，并阐述其底层实现机制。原子操作是实现无锁数据结构和线程安全（Thread-Safe）代码的关键，它能确保在多核、多线程或中断等并发环境下对共享内存的访问是不可分割的。

openvela 系统通过标准头文件 `<stdatomic.h>` 提供这些接口。

## 一、 实现机制

openvela 的原子操作采用分层实现策略，优先利用硬件特性，在硬件不支持时则提供软件模拟作为回退方案，以确保功能覆盖的完备性和兼容性。

### 1、硬件原子指令

当目标处理器架构（如 ARMv7-M, RISC-V with 'A' extension）提供原生原子操作指令时，编译器会直接将原子 API 调用翻译为高效的机器指令。这是最高效的实现方式，因为它利用硬件保证了操作的原子性，避免了锁带来的开销。

`stdatomic.h` 的具体实现由工具链预置提供，例如在 ARM 架构GCC 工具链下，其路径为： `prebuilts/gcc/linux/arm/arm-none-eabi/include/stdatomic.h`

### 2、软件模拟回退机制

当编译器或目标硬件对原子指令的支持不符合预期时，openvela 提供了一套基于自旋锁（Spinlock）的软件回退（Fallback）机制。此机制通过在操作前后开关中断和获取自旋锁来模拟原子操作行为，在使用上效果和工具链提供的版本完全相同。

开发者可以通过内核配置项 `CONFIG_LIBC_ARCH_ATOMIC` 来控制此行为。若启用此选项，系统将链接 `arch_atomic.c` 文件中定义的软件模拟函数，而非编译器内建函数。

- **源码路径**：[nuttx/libs/libc/machine/arch_atomic.c](../../../../../../../nuttx/blob/dev-ai-contest-2026/libs/libc/machine/arch_atomic.c)
- **相关构建配置**：[nuttx/libs/libc/machine/Make.defs](../../../../../../../nuttx/blob/dev-ai-contest-2026/libs/libc/machine/Make.defs)

## 二、 使用方法

### 1、包含头文件

在您的代码中，包含以下标准头文件以使用原子操作接口：

```C
#include <stdatomic.h>
```

### 2、支持的原子类型

`<stdatomic.h>` 头文件为所有标准整型定义了对应的原子类型。您可以使用这些类型来声明需要进行原子访问的变量。后续文档将使用 `atomic_type` 作为这些类型的统称。

```C
// 标准原子类型
atomic_bool, atomic_char, atomic_schar, atomic_uchar,
atomic_short, atomic_ushort, atomic_int, atomic_uint,
atomic_long, atomic_ulong, atomic_llong, atomic_ullong,
atomic_char16_t, atomic_wchar_t,

// 定宽原子类型
atomic_int_least8_t, atomic_uint_least8_t,
atomic_int_least16_t, atomic_uint_least16_t,
atomic_int_least32_t, atomic_uint_least32_t,
atomic_int_least64_t, atomic_uint_least64_t,

// 快速定宽原子类型
atomic_int_fast8_t, atomic_uint_fast8_t,
atomic_int_fast16_t, atomic_uint_fast16_t,
atomic_int_fast32_t, atomic_uint_fast32_t,
atomic_int_fast64_t, atomic_uint_fast64_t,

// 指针与尺寸相关原子类型
atomic_intptr_t, atomic_uintptr_t,
atomic_size_t, atomic_ptrdiff_t,
atomic_intmax_t, atomic_uintmax_t
```

### 3、API 参考

原子操作接口提供了一套线程安全的函数，用于对原子变量进行初始化、读、写、修改和比较交换（Compare-and-Swap, CAS）等操作。

#### 通用及算术原子操作

| 函数                                                      | 描述                                                                                                                                                                                                                               |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ATOMIC_VAR_INIT(value)                                    | 用于在声明时静态初始化一个原子变量。                                                                                                                                                                                               |
| atomic_init(obj, value)                                   | 对一个已存在的原子对象进行动态初始化。                                                                                                                                                                                             |
| atomic_store(object, desired)                             | 原子地将 desired 值写入 object。                                                                                                                                                                                                   |
| atomic_load(object)                                       | 原子地读取 object 的值并返回。                                                                                                                                                                                                     |
| atomic_exchange(object, desired)                          | 原子地将 desired 值写入 object，并返回 object 的旧值。                                                                                                                                                                             |
| atomic_fetch_add(object, arg)                             | 原子地将 arg 加到 object，并返回 object 的旧值。                                                                                                                                                                                   |
| atomic_fetch_sub(object, arg)                             | 原子地从 object 减去 arg，并返回 object 的旧值。                                                                                                                                                                                   |
| atomic_compare_exchange_weak(object, expected, desired)   | 比较 object 与 expected 的值：<br>若相等，则将 desired 写入 object 并返回 true。<br>若不相等，则将 object 的当前值载入 expected 并返回 false。<br>由于部分 arch 中断触发会自动清除总线锁，此函数可能出现“伪失败”，通常用于循环中。 |
| atomic_compare_exchange_strong(object, expected, desired) | 功能同上，但可避免“伪失败”，保证只有在值确实不相等时才返回 false。                                                                                                                                                                 |

#### 位原子操作

| 函数                          | 描述                                                                                      |
| ----------------------------- | ----------------------------------------------------------------------------------------- |
| atomic_fetch_or(object, arg)  | 原子地对 object 与 arg 执行按位或（OR）操作，并将结果存入 object，返回 object 的旧值。    |
| atomic_fetch_xor(object, arg) | 原子地对 object 与 arg 执行按位异或（XOR）操作，并将结果存入 object，返回 object 的旧值。 |
| atomic_fetch_and(object, arg) | 原子地对 object 与 arg 执行按位与（AND）操作，并将结果存入 object，返回 object 的旧值。   |

## 三、内部实现解析

本章节深入解析 openvela 在工具链不支持原子操作时的软件模拟实现，其核心在于利用宏和自旋锁来保证操作的原子性。

### 实现原理

`arch_atomic.c` 文件通过定义一组宏来自动生成针对不同数据宽度（1, 2, 4, 8 字节）的原子操作函数。以 `atomic_store` 为例：

1. **基础宏定义 `STORE`**：

    此宏封装了核心的自旋锁逻辑。它接收函数名、宽度和类型作为参数，生成一个完整的函数定义。函数内部通过 `spin_lock_irqsave` 和 `spin_unlock_irqrestore` 来创建临界区，确保赋值操作不被中断。

    ```C
    #define STORE(n, type)                                         \
    void weak_function CONCATENATE(__atomic_store_, n) (FAR volatile void *ptr,   \
                                            type value, int memorder) \
    {                                                                \
        irqstate_t irqstate = spin_lock_irqsave(NULL);                 \
                                                                        \
        *(FAR type *)ptr = value;                                      \
                                                                        \
        spin_unlock_irqrestore(NULL, irqstate);                        \
    }
    ```

2. 生成具体函数：

    使用 `STORE` 宏为不同的数据类型生成具体的存储函数。

    ```C
    // 为 1 字节类型 (uint8_t) 生成 __atomic_store_1
    STORE(1, uint8_t)
    // 为 2 字节类型 (uint16_t) 生成 __atomic_store_2
    STORE(2, uint16_t)
    // ... 其他宽度
    ```

3. 分发宏 `atomic_store`：

    最后，定义一个顶层宏 `atomic_store`，它通过 `sizeof` 运算符判断传入的原子变量大小，并将调用分发到对应宽度的具体实现函数。

    ```C
    #define atomic_store_n(obj, val, type) \
    (sizeof(*(obj)) == 1 ? __atomic_store_1(obj, val, type) : \
        sizeof(*(obj)) == 2 ? __atomic_store_2(obj, val, type) : \
        sizeof(*(obj)) == 4 ? __atomic_store_4(obj, val, type) : \
                            __atomic_store_8(obj, val, type))
    
    #define atomic_store(obj, val) atomic_store_n(obj, val, __ATOMIC_RELAXED)
    ```

这种设计模式使得代码高度模块化且易于扩展，同时为开发者提供了与标准一致的原子操作接口。

## 四、 使用示例

以下示例代码演示了如何使用原子操作接口，并通过一系列的测试来验证其正确性。

### 1、示例代码

```C
#include <nuttx/config.h>
#include <stdio.h>
#include <stdatomic.h>

/* 用于检查原子操作结果的宏 */
#define ATOMIC_CHECK(value, expected)                       \
    if ((value) != (expected))                              \
    {                                                       \
        printf("atomic test fail at line: %d, value: %ld, expected: %ld\n", \
               __LINE__, (long)(value), (long)(expected));  \
    }

/* 对指定类型执行原子操作测试套件的宏 */
#define ATOMIC_TEST(type, init)                                \
{                                                              \
    atomic_##type object = ATOMIC_VAR_INIT(init);              \
    type expected;                                             \
    type old_value;                                            \
                                                               \
    /* Add */                                                  \
    old_value = atomic_fetch_add(&object, 1);                  \
    ATOMIC_CHECK(old_value, 1);                                \
    ATOMIC_CHECK(atomic_load(&object), 2);                     \
                                                               \
    /* Store & Load */                                         \
    atomic_store(&object, 1);                                  \
    old_value = atomic_load(&object);                          \
    ATOMIC_CHECK(old_value, 1);                                \
                                                               \
    /* OR */                                                   \
    old_value = atomic_fetch_or(&object, 4);                   \
    ATOMIC_CHECK(old_value, 1);                                \
    ATOMIC_CHECK(atomic_load(&object), 5);                     \
                                                               \
    /* XOR */                                                  \
    old_value = atomic_fetch_xor(&object, 7);                  \
    ATOMIC_CHECK(old_value, 5);                                \
    ATOMIC_CHECK(atomic_load(&object), 2);                     \
                                                               \
    /* AND */                                                  \
    old_value = atomic_fetch_and(&object, 3);                  \
    ATOMIC_CHECK(old_value, 2);                                \
    ATOMIC_CHECK(atomic_load(&object), 2);                     \
                                                               \
    /* Exchange */                                             \
    old_value = atomic_exchange(&object, 5);                   \
    ATOMIC_CHECK(old_value, 2);                                \
    ATOMIC_CHECK(atomic_load(&object), 5);                     \
                                                               \
    /* Sub */                                                  \
    old_value = atomic_fetch_sub(&object, 3);                  \
    ATOMIC_CHECK(old_value, 5);                                \
    ATOMIC_CHECK(atomic_load(&object), 2);                     \
                                                               \
    /* Compare Exchange Weak */                                \
    expected = 2;                                              \
    atomic_compare_exchange_weak(&object, &expected, 5);       \
    ATOMIC_CHECK(atomic_load(&object), 5);                     \
                                                               \
    /* Compare Exchange Strong */                              \
    expected = 5;                                              \
    atomic_compare_exchange_strong(&object, &expected, 2);     \
    ATOMIC_CHECK(atomic_load(&object), 2);                     \
}

int main(int argc, FAR char *argv[])
{
    printf("Starting atomic tests...\n");

    ATOMIC_TEST(int, 1);
    ATOMIC_TEST(uint, 1U);
    ATOMIC_TEST(long, 1L);
    ATOMIC_TEST(ulong, 1UL);
    ATOMIC_TEST(short, 1);
    ATOMIC_TEST(ushort, 1U);
    ATOMIC_TEST(char, 1);

    printf("Atomic tests complete!\n");
    return 0;
}
```

### 2、执行与输出

将上述代码编译为应用程序（例如 `atomic_test`）并在目标设备上执行。成功执行后，系统将打印以下信息，表明所有原子操作测试均已通过：

```Shell
qemu-armv8a-ap> atomic_test
Starting atomic tests...
Atomic tests complete!
```

测试结果表明，所有原子操作均正确执行，验证通过。

## 五、参考资料

- [GCC 官方文档：atomic Builtins](https://gcc.gnu.org/onlinedocs/gcc-12.3.0/gcc/_005f_005fatomic-Builtins.html)
- https://blog.regehr.org/archives/28