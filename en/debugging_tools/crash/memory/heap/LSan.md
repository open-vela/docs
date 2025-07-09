# LeakSanitizer (LSan) User Guide

\[ English | [简体中文](./../../../../../zh-cn/debugging_tools/crash/memory/heap/LSan.md) \]

## I. Overview

LeakSanitizer (LSan) is an efficient heap memory leak detector. As a runtime tool, it automatically detects and reports memory that has not been freed when a program exits, helping developers locate and fix memory leaks. LSan can work in conjunction with [AddressSanitizer](https://github.com/google/sanitizers/wiki/AddressSanitizer) (ASan) or [MemorySanitizer](https://github.com/google/sanitizers/wiki/MemorySanitizer) (MSan), or it can run standalone.

> Note
>
> In the openvela environment, LSan is currently supported only on the **sim simulation** platform.

## II. How to Use

### Step 1: Enable LSan

You can enable LSan with the following configuration. In openvela, enabling ASan enables LSan by default.

Add the following to your configuration file:

```Makefile
CONFIG_SIM_ASAN=y
```

### Step 2: Run a Leak Check

LSan runs automatically when the program exits normally (for example, by running the `poweroff` command in openvela) to check for memory leaks.

### Step 3: Interpret the Report

When LSan detects a memory leak, it prints a report with a detailed call stack.

#### Problematic Code Example (`hello_main.c`)

```Plaintext
// Add the following code to hello_main.c
#include <stdlib.h>
int main(int argc, FAR char *argv[])
{
  // 100 bytes of memory are allocated but not freed
  malloc(100);
  printf("Hello, World!!\n");
  return 0;
}
```

#### Execution and Output

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

#### Report Analysis

- `Direct leak of 100 byte(s) in 1 object(s)`: Indicates a direct leak of 100 bytes. A **direct leak** means the memory block is no longer accessible from any part of the program.
- **Call Stack**: The stack trace in the report is key to locating the problem. In this example, line `#6` clearly shows that the leak occurred at line 38 of `hello_main.c`, where `malloc(100)` was called.

## III. How It Works

LSan does not require compiler instrumentation. It works by intercepting memory allocation and deallocation functions (like `malloc`, `free`, `new`, `delete`) at runtime to track all heap objects. Its detection process is similar to the Mark-and-Sweep algorithm used in garbage collection (GC).

### Detection Process

1. **Track Allocations**: As the program runs, LSan records all memory blocks allocated on the heap.
2. **Stop the Program**: When the program exits or a check is manually triggered, LSan pauses all threads to get a stable snapshot of memory.
3. **Identify Root Sets**: LSan scans all root regions that can legally hold pointers to heap memory, including:

    - Global variables
    - The stacks of all threads
    - CPU registers
    - Thread-Local Storage (TLS)

4. **Mark Reachable Objects**: Starting from the root sets, LSan recursively traverses all pointers, marking all accessible heap memory blocks.
5. **Identify Leaks**: After the traversal, any **unmarked** heap memory blocks are considered memory leaks.
6. **Generate Report**: LSan reports all leaked memory blocks, along with the call stack recorded at the time of allocation.

### How Root Sets Are Found

For users who need a deeper understanding of its implementation details, LSan finds the specific memory regions for its root sets in the following ways:

- **Global Variable Sections**: Uses `dl_iterate_phdr()` to iterate through all loaded shared objects (including the main executable) to get the ranges of their global data segments.
- **Thread Stack Ranges**: Uses `pthread_getattr_np()` to get the stack address and size for each thread.
- **Thread-Local Storage (TLS)**:

    - Static TLS areas are located using the internal glibc function `_dl_get_tls_static_info()`.
    - Dynamically allocated TLS blocks are identified by intercepting calls to `__libc_memalign` made by the linker when it allocates dynamic TLS space. These allocated blocks are treated directly as part of the root set.

## IV. Leak Suppression

In some cases, you may need to ignore known and acceptable leaks, such as known issues in third-party libraries or objects that are intentionally designed as singletons. LSan provides several ways to suppress these leak reports.

The most common method is to use a **suppression file**.

### Steps

1. **Create a suppression file**. Create a text file, for example, `lsan.supp`.

2. **Add suppression rules**. Add rules to the file, one per line. Each rule specifies a leak source to be ignored. The most common format is leak:function_name, where function_name is the name of the function that allocated the leaked memory.

    **Example** (`lsan.supp`)

    ```Plain
    # Ignore all memory allocated by the my_singleton_alloc function
    leak:my_singleton_alloc
    # You can also ignore all leaks originating from a specific file
    leak:third_party_library.c
    ```

    **Note**: You can copy the function or file names directly from the LSan report's call stack.

3. **Specify the suppression file path**. Use the `LSAN_OPTIONS` environment variable to tell LSan where to find the suppression file. You must set this environment variable **before** starting the `sim` simulation environment.

    ```Bash
    # Execute in the openvela root directory
    export LSAN_OPTIONS=suppressions=./lsan.supp
    ./build/bin/sim # Then start the simulation program
    ```

    At runtime, LSan will read this file and ignore all leak sources listed within it.

### Other Suppression Methods

Besides using a suppression file, you can also ignore a specific memory object directly in your code:

```C
#include <sanitizer/lsan_interface.h>
void *p = malloc(100);
__lsan_ignore_object(p); // Tells LSan not to track this object
```

This method is useful when you have direct control over and access to the memory pointer.

## V. FAQ

### 1. `fast-unwind` Compatibility Issue

#### Description

LSan's `fast-unwind` stack unwinding mechanism relies on frame pointers and has strict requirements for the current task's stack range. However, the openvela `sim` mode scheduler is based on coroutines (using `setjmp`/`longjmp`), which causes the stack pointer to change upon thread switches. This leads to failures in the `fast-unwind` stack range check, preventing it from capturing memory leaks.

#### Solution

In `sim` mode, `fast-unwind` is disabled by default, forcing LSan to use the standard `slow-unwind` mode. This is configured via the `__lsan_default_options` function to ensure LSan can unwind call stacks correctly.

Reference Implementation (`nuttx/arch/sim/src/sim/sim_asan.c`):

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

### 2. UBSan False Positives Issue

#### Description

When UndefinedBehaviorSanitizer (UBSan) is enabled, its internal operations (such as handling type information for C++ `dynamic_cast`) may allocate memory in certain situations. This memory might not be cleaned up by UBSan itself upon program exit, causing LSan to report it as a false positive memory leak.

#### Solution

To avoid such false positives, you can configure a dummy UBSan module. This approach maintains binary compatibility but disables all UBSan functionality at runtime, thereby eliminating the source of the false positives.

**Configuration Options:**

```Makefile
CONFIG_MM_UBSAN=y
CONFIG_MM_UBSAN_DUMMY=y
```

## VI. Debugging Tips

### Why is my program's memory usage continuously growing, but LSan reports no leaks?

This situation is typically a **logical leak**, not a **reachability leak**, which is what LSan is designed to detect.

- **Reachability Leak**: Memory is allocated, but all pointers to it are lost, making it impossible for the program to access or free it. This is what LSan detects.
- **Logical Leak**: Memory is technically still reachable (e.g., held by a global list or cache) but is no longer needed from a program logic perspective.

#### Example

A global data cache continuously adds new entries but never, or rarely, removes old, unused ones.

Because these unused entries are still referenced by a global data structure, LSan considers them **reachable** and will not report a leak. However, they are still consuming memory.

#### How to Address It

For **logical leaks**, you need to use other tools for manual analysis. For example, switch back to the system's built-in memory allocator and use [Leak Detection]() methods to check for changes in memory usage, which can help you locate the module causing the continuous memory growth.

## VII. References

- [LeakSanitizer Official Documentation](https://maskray.me/blog/2023-02-12-all-about-leak-sanitizer)
- [Apache NuttX PR #9186](https://github.com/apache/nuttx/pull/9186)
- [Apache NuttX PR #12659](https://github.com/apache/nuttx/pull/12659)