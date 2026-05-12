# Atomic Operations

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/kernel/resource_sync/atomic_operation.md) \]

This document describes how to use the C11 standard-compliant atomic operation interfaces in the openvela system and explains their underlying implementation. Atomic operations are crucial for implementing lock-free data structures and thread-safe code, ensuring that access to shared memory is indivisible in concurrent environments such as multi-core, multi-threaded, or interrupt contexts.

The openvela system provides these interfaces through the standard header file `<stdatomic.h>`.

## I. Implementation Mechanism

The atomic operations in openvela use a layered implementation strategy, prioritizing hardware features and providing a software emulation as a fallback to ensure comprehensive functionality and compatibility.

### 1. Hardware Atomic Instructions

When the target processor architecture (e.g., ARMv7-M, RISC-V with 'A' extension) provides native atomic instructions, the compiler directly translates atomic API calls into efficient machine instructions. This is the most efficient approach as it guarantees atomicity at the hardware level, avoiding the overhead associated with locks.

The specific implementation of `stdatomic.h` is provided by the prebuilt toolchain. For example, for the GCC toolchain on the ARM architecture, the path is: `prebuilts/gcc/linux/arm/arm-none-eabi/include/stdatomic.h`

### 2. Software Emulation Fallback

In cases where the compiler or target hardware lacks adequate support for atomic instructions, openvela provides a software fallback mechanism based on spinlocks. This approach emulates atomic operations by wrapping them in a critical section, which is protected by a spinlock and by disabling interrupts. This ensures that the functional behavior is identical to the native implementation from the toolchain.

Developers can control this behavior using the kernel configuration option `CONFIG_LIBC_ARCH_ATOMIC`. If this option is enabled, the system will link against the software emulation functions defined in `arch_atomic.c` instead of using the compiler's built-in functions.

- **Source Path**: [nuttx/libs/libc/machine/arch_atomic.c](../../../../../../../nuttx/blob/dev-ai-contest-2026/libs/libc/machine/arch_atomic.c)
- **Related Build Configuration**: [nuttx/libs/libc/machine/Make.defs](../../../../../../../nuttx/blob/dev-ai-contest-2026/libs/libc/machine/Make.defs)

## II. Usage

### 1. Including the Header File

In your code, include the following standard header file to use the atomic operation interfaces:

```c
#include <stdatomic.h>
```

### 2. Supported Atomic Types

The `<stdatomic.h>` header file defines corresponding atomic types for all standard integer types. You can use these types to declare variables that require atomic access. In the following documentation, `atomic_type` will be used as a generic placeholder for these types.

```c
// Standard atomic types
atomic_bool, atomic_char, atomic_schar, atomic_uchar,
atomic_short, atomic_ushort, atomic_int, atomic_uint,
atomic_long, atomic_ulong, atomic_llong, atomic_ullong,
atomic_char16_t, atomic_wchar_t,

// Fixed-width atomic types
atomic_int_least8_t, atomic_uint_least8_t,
atomic_int_least16_t, atomic_uint_least16_t,
atomic_int_least32_t, atomic_uint_least32_t,
atomic_int_least64_t, atomic_uint_least64_t,

// Fast fixed-width atomic types
atomic_int_fast8_t, atomic_uint_fast8_t,
atomic_int_fast16_t, atomic_uint_fast16_t,
atomic_int_fast32_t, atomic_uint_fast32_t,
atomic_int_fast64_t, atomic_uint_fast64_t,

// Pointer and size-related atomic types
atomic_intptr_t, atomic_uintptr_t,
atomic_size_t, atomic_ptrdiff_t,
atomic_intmax_t, atomic_uintmax_t
```

### 3. API Reference

The atomic operations API provides a set of thread-safe functions for initializing, reading, writing, modifying, and performing Compare-and-Swap (CAS) operations on atomic variables.

#### General and Arithmetic Atomic Operations

| Function                                                    | Description                                                                                                                                                                                                                                                                                                                                                                            |
| :---------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ATOMIC_VAR_INIT(value)`                                    | Statically initializes an atomic variable at declaration.                                                                                                                                                                                                                                                                                                                              |
| `atomic_init(obj, value)`                                   | Dynamically initializes an existing atomic object.                                                                                                                                                                                                                                                                                                                                     |
| `atomic_store(object, desired)`                             | Atomically writes the `desired` value to `object`.                                                                                                                                                                                                                                                                                                                                     |
| `atomic_load(object)`                                       | Atomically reads and returns the value of `object`.                                                                                                                                                                                                                                                                                                                                    |
| `atomic_exchange(object, desired)`                          | Atomically writes the `desired` value to `object` and returns the old value of `object`.                                                                                                                                                                                                                                                                                               |
| `atomic_fetch_add(object, arg)`                             | Atomically adds `arg` to `object` and returns the old value of `object`.                                                                                                                                                                                                                                                                                                               |
| `atomic_fetch_sub(object, arg)`                             | Atomically subtracts `arg` from `object` and returns the old value of `object`.                                                                                                                                                                                                                                                                                                        |
| `atomic_compare_exchange_weak(object, expected, desired)`   | Compares the value of `object` with `expected`: <br>If they are equal, writes `desired` to `object` and returns `true`. <br>If they are not equal, loads the current value of `object` into `expected` and returns `false`.<br>This function may have "spurious failures" and is typically used in a loop, as an interrupt on some architectures can automatically clear the bus lock. |
| `atomic_compare_exchange_strong(object, expected, desired)` | Same as above, but avoids "spurious failures," guaranteeing a return of `false` only if the values are genuinely not equal.                                                                                                                                                                                                                                                            |

#### Bitwise Atomic Operations

| Function                        | Description                                                                                                                     |
| :------------------------------ | :------------------------------------------------------------------------------------------------------------------------------ |
| `atomic_fetch_or(object, arg)`  | Atomically performs a bitwise OR on `object` with `arg`, stores the result in `object`, and returns the old value of `object`.  |
| `atomic_fetch_xor(object, arg)` | Atomically performs a bitwise XOR on `object` with `arg`, stores the result in `object`, and returns the old value of `object`. |
| `atomic_fetch_and(object, arg)` | Atomically performs a bitwise AND on `object` with `arg`, stores the result in `object`, and returns the old value of `object`. |

## III. Internal Implementation Analysis

This section provides a deep dive into the software emulation implementation in openvela, which is used when the toolchain lacks native atomic support. Its core principle is to use macros and spinlocks to guarantee atomicity.

### Implementation Principle

The `arch_atomic.c` file uses a set of macros to automatically generate atomic operation functions for different data widths (1, 2, 4, and 8 bytes). Taking `atomic_store` as an example:

1. **Base Macro Definition `STORE`**:

    This macro encapsulates the core spinlock logic. It accepts a function name suffix, width, and type as parameters to generate a complete function definition. Inside the function, `spin_lock_irqsave` and `spin_unlock_irqrestore` create a critical section to ensure the assignment operation is not interrupted.

    ```c
    #define STORE(n, type)                                             \
        void weak_function CONCATENATE(__atomic_store_, n) (FAR volatile void *ptr,   \
                                                type value, int memorder) \
        {                                                                    \
        irqstate_t irqstate = spin_lock_irqsave(NULL);                     \
                                                                            \
        *(FAR type *)ptr = value;                                          \
                                                                            \
        spin_unlock_irqrestore(NULL, irqstate);                            \
        }
    ```

2. **Generating Specific Functions**:

    The `STORE` macro is used to generate specific store functions for different data types.

    ```c
    // Generate __atomic_store_1 for 1-byte type (uint8_t)
    STORE(1, uint8_t)
    // Generate __atomic_store_2 for 2-byte type (uint16_t)
    STORE(2, uint16_t)
    // ... and so on for other widths
    ```

3. **Dispatcher Macro: `atomic_store`**:

    Finally, a top-level macro `atomic_store` is defined. It uses the `sizeof` operator to determine the size of the atomic variable and dispatches the call to the appropriate width-specific implementation function.

    ```c
    #define atomic_store_n(obj, val, type) \
        (sizeof(*(obj)) == 1 ? __atomic_store_1(obj, val, type) : \
        sizeof(*(obj)) == 2 ? __atomic_store_2(obj, val, type) : \
        sizeof(*(obj)) == 4 ? __atomic_store_4(obj, val, type) : \
                                __atomic_store_8(obj, val, type))
    
    #define atomic_store(obj, val) atomic_store_n(obj, val, __ATOMIC_RELAXED)
    ```

This design pattern results in highly modular and extensible code while providing developers with a standard-compliant atomic interface.

## IV. Usage Example

The following example code demonstrates how to use the atomic operation interfaces and verifies their correctness through a series of tests.

### 1. Example Code

```c
#include <nuttx/config.h>
#include <stdio.h>
#include <stdatomic.h>

/* Macro to check the result of an atomic operation */
#define ATOMIC_CHECK(value, expected)                           \
    if ((value) != (expected))                                  \
    {                                                           \
        printf("atomic test fail at line: %d, value: %ld, expected: %ld\n", \
               __LINE__, (long)(value), (long)(expected));      \
    }

/* Macro to run a test suite for a given atomic type */
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

### 2. Execution and Output

Compile the code above into an application (e.g., `atomic_test`) and run it on the target device. Upon successful execution, the system will print the following message, indicating that all atomic operation tests have passed:

```shell
qemu-armv8a-ap> atomic_test
Starting atomic tests...
Atomic tests complete!
```

The test results indicate that all atomic operations were executed correctly and passed verification.

## V. References

- [GCC Online Documentation: Atomic Builtins](https://gcc.gnu.org/onlinedocs/gcc-12.3.0/gcc/_005f_005fatomic-Builtins.html)
- [Stdatomic.h for Bare-metal Programming](https://blog.regehr.org/archives/28)