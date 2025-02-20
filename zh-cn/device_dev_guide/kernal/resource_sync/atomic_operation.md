# 原子操作接口

## 一、概述

在 openvela 的 prebuilts 工具链中，已支持内联原子操作接口，这些接口定义在 `stdatomic.h` 头文件中。

### 1、文件路径

以 ARM 架构为例，`stdatomic.h` 文件路径如下：

```Shell
# 以 arm 架构为例
prebuilts/gcc/linux/arm/arm-none-eabi/include/stdatomic.h
```

### 2、原子操作的实现方式

- 硬件支持：如果编译器支持目标 CPU 架构的原子操作指令，则原子操作将在硬件层面保证原子性。
- 软件实现：如果编译器不支持原子操作指令，可以使用通用原子操作接口。此时需要配置 `CONFIG_LIBC_ARCH_ATOMIC`，通用接口通过关中断实现，具体实现见 [arch_atomic.c](https://github.com/open-vela/nuttx/blob/dev/libs/libc/machine/arch_atomic.c)。

    相关配置文件路径：

  - [nuttx/libs/libc/machine/Make.defs](https://github.com/open-vela/nuttx/blob/dev/libs/libc/machine/Make.defs)

### 3、配置选项说明

以下是 `CONFIG_LIBC_ARCH_ATOMIC` 的配置选项：

```Shell
config LIBC_ARCH_ATOMIC
        bool "arch_atomic"
        default n
        ---help---
                If this configuration is selected and <include/nuttx/atomic.h> is
                included, arch_atomic.c will be linked instead of built-in
                atomic function.
```

在 `Make.defs` 文件中，`arch_atomic.c` 的编译规则如下：

```Makefile
CSRCS += arch_atomic.c
```

## 二、包含头文件

在代码中使用原子操作时，需要包含以下头文件：

```C
#include <stdatomic.h>
```

## 三、原子变量类型

原子变量支持以下类型，后续文档中统一使用 `atomic_type` 表示：

```Shell
atomic_bool  
atomic_char  
atomic_schar  
atomic_uchar  
atomic_short  
atomic_ushort  
atomic_int  
atomic_uint  
atomic_long  
atomic_ulong  
atomic_llong  
atomic_ullong  
atomic_char16_t  
atomic_wchar_t  
atomic_int_least8_t  
atomic_uint_least8_t  
atomic_int_least16_t  
atomic_uint_least16_t  
atomic_int_least32_t  
atomic_uint_least32_t  
atomic_int_least64_t  
atomic_uint_least64_t  
atomic_int_fast8_t  
atomic_uint_fast8_t  
atomic_int_fast16_t  
atomic_uint_fast16_t  
atomic_int_fast32_t  
atomic_uint_fast32_t  
atomic_int_fast64_t  
atomic_uint_fast64_t  
atomic_intptr_t  
atomic_uintptr_t  
atomic_size_t  
atomic_ptrdiff_t  
atomic_intmax_t  
atomic_uintmax_t
```

## 四、原子操作接口

原子操作接口提供了一组线程安全的操作，用于对原子变量进行初始化、读取、修改和比较等操作。以下是接口的详细说明。

### 1、整型原子操作

以下是整型原子操作的常用接口及其功能说明：

```C
//对原子变量初始化
ATOMIC_VAR_INIT(value)
void atomic_init(obj, value)

//对原子变量进行设置
void atomic_store(atomic_type *object, int desired);

//读取原子变量并返回
atomic_type atomic_load(atomic_type *object);

//对原子变量进行减法操作，并返回减法操作完的旧值
atomic_type atomic_fetch_sub(atomic_type *object, atomic_type desired);

//对原子变量进行加法操作，并返回加法操作完的旧值
atomic_type atomic_fetch_add(atomic_type *object, atomic_type desired);

//对原子变量执行交换操作,并返回旧值
atomic_type atomic_exchange(atomic_type *object, atomic_type desired);

//对原子变量执行比较和交换操作，比较原子变量和一个期望值，如果相等，则将新值存储到原子变量中，并返回true,否则直接返回false。
bool atomic_compare_exchange_weak(atomic_type *object, int *expected, int desired);

//同样执行比较和交换操作，不同于weak函数的是该函数会强制执行自旋锁等待，直到比较和交换成功或达到一定的重试次数
bool atomic_compare_exchange_strong(atomic_type *object, int *expected, int desired);
```

### 2、位原子操作

以下是位操作相关的原子操作接口及其功能说明：

```C
//按位亦或操作，将指定值与原子变量的值进行按位异或运算，并返回执行xor操作前的旧值
atomic_type atomic_fetch_xor(atomic_type *object, atomic_type desired);

//按位或操作，将指定值与原子变量进行按位或运算，并返回执行or操作前的旧值
atomic_type atomic_fetch_or(atomic_type *object, atomic_type desired);

//按位与操作，将指定值与原子变量进行按位与运算，并返回执行and操作前的旧值
atomic_type atomic_fetch_and(atomic_type *object, atomic_type desired);
```

## 五、测试示例

以下示例代码展示了如何使用原子操作接口对不同类型的原子变量进行测试。代码通过一系列操作验证了原子操作的正确性。

### 1、示例代码

```C
/****************************************************************************
 * Included Files
 ****************************************************************************/

#include <nuttx/config.h>
#include <stdio.h>
#include <stdatomic.h>

/****************************************************************************
 * Pre-processor Definitions
 ****************************************************************************/

#define ATOMIC_CHECK(value, expected)                       \
if ((value) != (expected))                                  \
{                                                           \
    printf("atomic test fail,line:%d\n",__LINE__);          \
}

#define ATOMIC_TEST(type, init)                             \
{                                                           \
    atomic_##type object = init;                            \
    atomic_##type expected = 2;                             \
                                                            \
    atomic_##type old_value = atomic_fetch_add(&object, 1); \
    ATOMIC_CHECK(old_value, 1);                             \
    ATOMIC_CHECK(object, 2);                                \
                                                            \
    atomic_store(&object, 1);                               \
    ATOMIC_CHECK(object, 1);                                \
                                                            \
    old_value = atomic_load(&object);                       \
    ATOMIC_CHECK(object, 1)                                 \
                                                            \
    old_value = atomic_fetch_or(&object, 4);                \
    ATOMIC_CHECK(old_value, 1);                             \
    ATOMIC_CHECK(object, 5);                                \
                                                            \
    old_value = atomic_fetch_xor(&object, 7);               \
    ATOMIC_CHECK(old_value, 5);                             \
    ATOMIC_CHECK(object, 2);                                \
                                                            \
    old_value = atomic_fetch_and(&object, 3);               \
    ATOMIC_CHECK(old_value, 2);                             \
    ATOMIC_CHECK(object, 2);                                \
                                                            \
    old_value = atomic_exchange(&object, 5);                \
    ATOMIC_CHECK(old_value, 2);                             \
    ATOMIC_CHECK(object, 5);                                \
                                                            \
    old_value = atomic_fetch_sub(&object, 3);               \
    ATOMIC_CHECK(old_value, 5);                             \
    ATOMIC_CHECK(object, 2);                                \
                                                            \
    atomic_compare_exchange_weak(&object, &expected, 5);    \
    ATOMIC_CHECK(object, 5);                                \
                                                            \
    expected = 5;                                           \
    atomic_compare_exchange_strong(&object, &expected, 2);  \
    ATOMIC_CHECK(object, 2);                                \
}

/****************************************************************************
 * Public Functions
 ****************************************************************************/

/****************************************************************************
 * atomic_main
 ****************************************************************************/

int main(int argc, FAR char *argv[])
{
  ATOMIC_TEST(int, 1);
  ATOMIC_TEST(uint, 1U);
  ATOMIC_TEST(long, 1L);
  ATOMIC_TEST(ulong, 1UL);
  ATOMIC_TEST(short, 1);
  ATOMIC_TEST(ushort, 1);
  ATOMIC_TEST(char, 1);

  printf("atomic test complete!\n");
  return 0;
}
```

### 2、测试结果

```Shell
qemu-armv8a-ap> atomic
atomic test complete!        // 测试通过
```

测试结果表明，所有原子操作均正确执行，验证通过。

## 六、参考资料

- [GCC 官方文档：atomic Builtins](https://gcc.gnu.org/onlinedocs/gcc-12.3.0/gcc/_005f_005fatomic-Builtins.html)