# Atomic Operation Interface

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/kernel/resource_sync/atomic_operation.md) \]

## 1. Overview

The prebuilts toolchain in openvela supports inline atomic operation interfaces, which are defined in the `stdatomic.h` header file.

### 1、File Path

Taking the ARM architecture as an example, the file path for `stdatomic.h` is as follows:

```Shell
# 以 arm 架构为例
prebuilts/gcc/linux/arm/arm-none-eabi/include/stdatomic.h
```

### 2、Implementation of Atomic Operations

- Hardware Support: If the compiler supports atomic operation instructions for the target CPU architecture, atomicity will be guaranteed at the hardware level.
- Software Implementation: If the compiler does not support atomic operation instructions, generic atomic operation interfaces can be used.

    Relevant configuration file path:

    - [nuttx/libs/libc/machine/Make.defs](https://github.com/open-vela/nuttx/blob/dev/libs/libc/machine/Make.defs)

### 3、Configuration Options Explanation

Below is the configuration option for `CONFIG_LIBC_ARCH_ATOMIC`:

```Shell
config LIBC_ARCH_ATOMIC
        bool "arch_atomic"
        default n
        ---help---
                If this configuration is selected and <include/nuttx/atomic.h> is
                included, arch_atomic.c will be linked instead of built-in
                atomic function.
```

In the `Make.defs` file, the compilation rule for `arch_atomic.c` is as follows:

```Makefile
CSRCS += arch_atomic.c
```

## 2. Included Header Files

When using atomic operations in the code, include the following header file:

```C
#include <stdatomic.h>
```

## 3. Atomic Variable Types

Atomic variables support the following types, referred to as `atomic_type` in subsequent documentation:

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

## 4. Atomic Operation Interfaces

Atomic operation interfaces provide a set of thread-safe operations for initializing, reading, modifying, and comparing atomic variables. Below is a detailed description of the interfaces.

### 1. Integer Atomic Operations

Below are common interfaces for integer atomic operations and their descriptions:

```C
// Initialize atomic variable
ATOMIC_VAR_INIT(value)
void atomic_init(obj, value)

// Set value for atomic variable
void atomic_store(atomic_type *object, int desired);

// Load value from atomic variable
atomic_type atomic_load(atomic_type *object);

// Perform subtraction on atomic variable and return the old value after subtraction
atomic_type atomic_fetch_sub(atomic_type *object, atomic_type desired);

// Perform addition on atomic variable and return the old value after addition
atomic_type atomic_fetch_add(atomic_type *object, atomic_type desired);

// Perform exchange on atomic variable and return the old value
atomic_type atomic_exchange(atomic_type *object, atomic_type desired);

// Perform compare-and-swap on atomic variable; if the variable equals the expected value, 
// store the new value in the atomic variable and return true, otherwise return false
bool atomic_compare_exchange_weak(atomic_type *object, int *expected, int desired);

// Perform compare-and-swap with a stronger guarantee; this function will force a spinlock 
// wait until the compare-and-swap is successful or a certain retry count is reached
bool atomic_compare_exchange_strong(atomic_type *object, int *expected, int desired);
```

### 2. Bitwise Atomic Operations

Below are bitwise atomic operations and their descriptions:

```C
// Perform bitwise XOR operation, XOR the specified value with the atomic variable value,
// and return the old value before the XOR operation
atomic_type atomic_fetch_xor(atomic_type *object, atomic_type desired);

// Perform bitwise OR operation, OR the specified value with the atomic variable,
// and return the old value before the OR operation
atomic_type atomic_fetch_or(atomic_type *object, atomic_type desired);

// Perform bitwise AND operation, AND the specified value with the atomic variable,
// and return the old value before the AND operation
atomic_type atomic_fetch_and(atomic_type *object, atomic_type desired);
```

## 5. Internal Implementation in Vela
o avoid inconsistencies in atomic interface support across different toolchains, Vela provides a set of system-level implementations. When the toolchain does not support atomic operations, Vela's implementation of Atomic will be used as a substitute.
For complete details, refer to the file [arch_atomic.c](https://github.com/open-vela/nuttx/blob/dev/libs/libc/machine/arch_atomic.c)
Vela’s internal implementation mainly uses spinlocks to simulate atomic operations. It decomposes operations such as load, store, exchange, and CAS into different macros. For example, atomic_store, which has the following function prototype:

```C
#define STORE(fn, n, type)                                         \
                                                                   \
  void weak_function CONCATENATE(fn, n) (FAR volatile void *ptr,   \
                                         type value, int memorder) \
  {                                                                \
    irqstate_t irqstate = spin_lock_irqsave(NULL);                 \
                                                                   \
    *(FAR type *)ptr = value;                                      \
                                                                   \
    spin_unlock_irqrestore(NULL, irqstate);                        \
  }
```

By using macros, different size types of `atomic_store` prototypes can be declared, such as:

```C
/****************************************************************************
 * Name: __atomic_store_1
 ****************************************************************************/

STORE(1, uint8_t)

/****************************************************************************
 * Name: __atomic_store_2
 ****************************************************************************/

STORE(2, uint16_t)

/****************************************************************************
 * Name: __atomic_store_4
 ****************************************************************************/

STORE(4, uint32_t)

/****************************************************************************
 * Name: __atomic_store_8
 ****************************************************************************/

STORE(8, uint64_t)
```

Then, by checking the size of the passed variable, it determines the type of variable for processing:

```C
#define atomic_store_n(obj, val, type) \
  (sizeof(*(obj)) == 1 ? __atomic_store_1(obj, val, type) : \
   sizeof(*(obj)) == 2 ? __atomic_store_2(obj, val, type) : \
   sizeof(*(obj)) == 4 ? __atomic_store_4(obj, val, type) : \
                         __atomic_store_8(obj, val, type))

#define atomic_store(obj, val) atomic_store_n(obj, val, __ATOMIC_RELAXED)
```

## 6. Test Example

The following example code demonstrates how to use atomic operation interfaces to test atomic variables of different types. The code performs a series of operations to verify the correctness of atomic operations.

### 1. Example Code

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

### 2. Test Results

```Shell
qemu-armv8a-ap> atomic
atomic test complete!        // Test Passed
```

The test results indicate that all atomic operations were executed correctly and the verification was successful.
## 6. References

- [GCC 官方文档：atomic Builtins](https://gcc.gnu.org/onlinedocs/gcc-12.3.0/gcc/_005f_005fatomic-Builtins.html)