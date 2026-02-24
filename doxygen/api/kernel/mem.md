# 内存管理

`Vela` 提供了灵活的内存管理系统，支持标准的 `POSIX` 内存分配接口以及扩展的内存管理功能。内存管理系统支持多种构建模式：

- **Flat Build**：只有一个用户堆，通过标准的 `malloc/free` 访问。
- **Protected Build**：有两个堆，一个内核堆和一个用户堆，通过 MPU 保护。
- **Kernel Build**：一个内核堆和多个用户堆（每个任务组一个）。

`Vela` 内存管理支持以下 API：

**标准内存分配接口**：
- `malloc()`
- `free()`
- `calloc()`
- `realloc()`
- `reallocarray()`
- `memalign()`
- `posix_memalign()`
- `aligned_alloc()`
- `valloc()`
- `zalloc()`

**内存信息查询接口**：
- `mallinfo()`
- `mallinfo_task()`
- `malloc_size()` / `malloc_usable_size()`
- `mallopt()`

**内核堆接口**（需要 `CONFIG_MM_KERNEL_HEAP`）：
- `kmm_malloc()`
- `kmm_free()`
- `kmm_calloc()`
- `kmm_realloc()`
- `kmm_zalloc()`
- `kmm_memalign()`
- `kmm_mallinfo()`
- `kmm_heapmember()`
- `kmm_initialize()`
- `kmm_checkcorruption()`

**堆管理接口**：
- `mm_initialize()`
- `mm_uninitialize()`
- `mm_addregion()`
- `mm_extend()`
- `mm_brkaddr()`
- `mm_heapmember()`
- `umm_initialize()`
- `umm_heapmember()`

**调试接口**：
- `mm_memdump()`
- `mm_checkcorruption()`
- `umm_checkcorruption()`
- `kmm_checkcorruption()`

## malloc

```c
void *malloc(size_t size);
```

从用户堆中分配指定大小的内存块。`malloc()` 会在堆中查找一个足够大的空闲块，从中分配所需的内存。如果 `size` 为 0，行为取决于实现，可能返回 `NULL` 或返回一个唯一的指针。

分配的内存保证按照 `MM_ALIGN`（默认为 `2 * sizeof(uintptr_t)`，即 8 或 16 字节）对齐，这确保了对任何基本数据类型的访问都是对齐的。

*参数*：

- `size` 要分配的内存大小（字节）。

*返回值*：

成功时返回指向分配内存的指针，失败时返回 `NULL` 并设置 `errno`：

- `ENOMEM` 可用内存不足。

*注意*：

- 分配的内存内容是未初始化的，可能包含任意数据。
- 返回的指针可以传递给 `free()`、`realloc()` 等函数。
- 在多任务环境中，`malloc()` 是线程安全的。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## free

```c
void free(void *ptr);
```

释放之前通过 `malloc()`、`calloc()`、`realloc()`、`memalign()` 等分配的内存块，使其可供后续分配使用。

如果 `ptr` 为 `NULL`，则不执行任何操作。如果 `ptr` 不是之前分配函数返回的指针，或者已经被释放过，则行为是未定义的。

*参数*：

- `ptr` 指向要释放的内存块的指针。

*返回值*：

无返回值。

*注意*：

- 释放后的指针不应再被使用（悬空指针）。
- 不要重复释放同一块内存（双重释放会导致堆损坏）。
- 不要释放非动态分配的内存（如栈上的变量或全局变量）。
- 释放内存后，该内存可能不会立即返回给系统，而是保留在堆中供后续分配使用。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## calloc

```c
void *calloc(size_t n, size_t elem_size);
```

分配一个包含 `n` 个元素的数组，每个元素大小为 `elem_size` 字节，总共分配 `n * elem_size` 字节的内存，并将所有字节初始化为零。

与 `malloc()` 相比，`calloc()` 有两个优点：它会将内存清零，并且在计算总大小时可以检测乘法溢出（取决于实现）。

*参数*：

- `n` 要分配的元素数量。
- `elem_size` 每个元素的大小（字节）。

*返回值*：

成功时返回指向分配并清零的内存的指针，失败时返回 `NULL` 并设置 `errno`：

- `ENOMEM` 可用内存不足。

*注意*：

- 如果 `n` 或 `elem_size` 为 0，可能返回 `NULL` 或返回一个唯一的指针。
- 返回的内存所有字节都被设置为 0。
- 对于需要零初始化的数据结构，推荐使用 `calloc()` 而不是 `malloc()` + `memset()`。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## realloc

```c
void *realloc(void *ptr, size_t size);
```

改变之前分配的内存块的大小。`realloc()` 可能会在原位置扩展或收缩内存块，也可能分配一个新的内存块并复制原有数据。

如果 `ptr` 为 `NULL`，则 `realloc()` 的行为等同于 `malloc(size)`。如果 `size` 为 0 且 `ptr` 不为 `NULL`，则行为等同于 `free(ptr)` 并返回 `NULL`。

*参数*：

- `ptr` 指向之前分配的内存块的指针。如果为 `NULL`，则等同于 `malloc(size)`。
- `size` 新的内存大小（字节）。如果为 0，则释放内存并返回 `NULL`。

*返回值*：

成功时返回指向重新分配内存的指针（可能与原指针不同），失败时返回 `NULL` 并设置 `errno`：

- `ENOMEM` 可用内存不足。此时原内存块保持不变，仍然有效。

*注意*：

- 如果新大小大于原大小，新增部分的内容是未初始化的。
- 如果新大小小于原大小，超出部分的数据会丢失。
- 返回的指针可能与原指针不同，成功调用后原指针不应再使用。
- 如果 `realloc()` 失败，原内存块不会被释放，调用者仍需负责释放它。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## reallocarray

```c
void *reallocarray(void *ptr, size_t n, size_t elem_size);
```

改变之前分配的内存块的大小为 `n * elem_size` 字节。与 `realloc()` 不同的是，`reallocarray()` 会安全地检查乘法溢出，防止整数溢出导致的安全问题。

这个函数特别适用于重新分配数组，因为直接使用 `realloc(ptr, n * elem_size)` 可能会因为乘法溢出而分配一个比预期小得多的内存块。

*参数*：

- `ptr` 指向之前分配的内存块的指针。如果为 `NULL`，则等同于分配新内存。
- `n` 元素数量。
- `elem_size` 每个元素的大小（字节）。

*返回值*：

成功时返回指向重新分配内存的指针，失败时返回 `NULL` 并设置 `errno`：

- `ENOMEM` 可用内存不足，或者 `n * elem_size` 溢出。

*注意*：

- 如果 `n * elem_size` 会导致整数溢出，函数会安全地返回 `NULL`。
- 与 `realloc()` 相同，失败时原内存块保持不变。

*`POSIX` 兼容性*：兼容 BSD/glibc 扩展接口。

## memalign

```c
void *memalign(size_t alignment, size_t size);
```

分配按指定边界对齐的内存。这对于需要特定对齐要求的硬件访问（如 DMA 缓冲区）或 SIMD 操作非常有用。

*参数*：

- `alignment` 对齐边界，必须是 2 的幂次方（如 16、32、64、4096 等）。
- `size` 要分配的内存大小（字节）。

*返回值*：

成功时返回按指定边界对齐的内存指针，失败时返回 `NULL` 并设置 `errno`：

- `ENOMEM` 可用内存不足。
- `EINVAL` `alignment` 不是 2 的幂次方。

*注意*：

- 分配的内存可以使用 `free()` 正常释放。
- 对于需要页对齐的内存，可以使用 `valloc()` 或 `posix_memalign()`。

*`POSIX` 兼容性*：兼容 `POSIX` 同名接口（已过时，推荐使用 `posix_memalign()`）。

## posix_memalign

```c
int posix_memalign(void **memptr, size_t alignment, size_t size);
```

分配按指定边界对齐的内存，并将指针存储在 `memptr` 中。这是 `memalign()` 的 POSIX 标准替代接口。

与 `memalign()` 的主要区别是：`posix_memalign()` 通过返回值报告错误，而不是设置 `errno`，这使得错误处理更加明确。

*参数*：

- `memptr` 存储分配内存指针的地址。成功时，`*memptr` 会被设置为分配的内存地址。
- `alignment` 对齐边界，必须是 `sizeof(void *)` 的倍数，且是 2 的幂次方。
- `size` 要分配的内存大小（字节）。

*返回值*：

- `0` 成功，`*memptr` 指向分配的内存。
- `ENOMEM` 可用内存不足。

*注意*：

- 与 `memalign()` 不同，错误通过返回值报告，而不是 `errno`。
- 分配的内存可以使用 `free()` 正常释放。
- Vela 当前实现不检查 `alignment` 参数的有效性，不返回 `EINVAL`（POSIX 标准要求在参数无效时返回 `EINVAL`）。

*`POSIX` 兼容性*：部分兼容 `POSIX` 同名接口（不返回 `EINVAL`）。

## aligned_alloc

```c
void *aligned_alloc(size_t alignment, size_t size);
```

分配按指定边界对齐的内存。这是 C11 标准引入的对齐内存分配函数。

*参数*：

- `alignment` 对齐边界，必须是 2 的幂次方。
- `size` 要分配的内存大小（字节）。C11 标准要求 `size` 应该是 `alignment` 的倍数，但许多实现不强制此要求。

*返回值*：

成功时返回按指定边界对齐的内存指针，失败时返回 `NULL`。

*注意*：

- 分配的内存可以使用 `free()` 正常释放。
- 此函数是 C11 标准的一部分，比 `memalign()` 更具可移植性。

*`POSIX` 兼容性*：完美兼容 C11 标准接口。

## valloc

```c
void *valloc(size_t size);
```

分配按页边界对齐的内存。页大小由系统决定，通常为 4096 字节。

此函数等效于 `memalign(sysconf(_SC_PAGESIZE), size)`。

*参数*：

- `size` 要分配的内存大小（字节）。

*返回值*：

成功时返回按页边界对齐的内存指针，失败时返回 `NULL`。

*注意*：

- 页大小可以通过 `sysconf(_SC_PAGESIZE)` 获取。
- 分配的内存可以使用 `free()` 正常释放。
- 此函数已过时，新代码应使用 `posix_memalign()` 替代。

*`POSIX` 兼容性*：兼容 BSD 扩展接口（已过时，推荐使用 `posix_memalign()`）。

## zalloc

```c
void *zalloc(size_t size);
```

分配指定大小的内存块并将所有字节初始化为零。这是 Vela 提供的便捷函数，功能等同于 `calloc(1, size)`，但语义更清晰。

*参数*：

- `size` 要分配的内存大小（字节）。

*返回值*：

成功时返回指向分配并清零的内存的指针，失败时返回 `NULL` 并设置 `errno`：

- `ENOMEM` 可用内存不足。

*注意*：

- 与 `malloc()` 不同，返回的内存已被清零。
- 与 `calloc(1, size)` 功能相同，但调用更简洁。

*`POSIX` 兼容性*：Vela 扩展接口。

---

## 内存信息查询接口

以下接口用于查询堆的使用情况和内存分配统计信息，对于调试和监控内存使用非常有用。

## mallinfo

```c
struct mallinfo mallinfo(void);
```

获取用户堆的内存分配统计信息。这对于监控应用程序的内存使用情况、检测内存泄漏和优化内存使用非常有用。

*参数*：

无参数。

*返回值*：

返回 `struct mallinfo` 结构体，包含以下字段：

- `arena` 堆分配的总内存大小（字节），即堆管理的内存总量。
- `ordblks` 空闲块的数量。
- `aordblks` 已分配块的数量。
- `mxordblk` 最大空闲块的大小（字节），表示单次分配可用的最大内存。
- `uordblks` 已分配内存的总大小（字节）。
- `fordblks` 空闲内存的总大小（字节）。
- `usmblks` 曾经分配的最大内存量（高水位线）。

*注意*：

- `uordblks + fordblks` 应该接近 `arena`（可能略小，因为有堆管理开销）。
- `mxordblk` 表示当前可以成功分配的最大内存块大小。

*`POSIX` 兼容性*：兼容 glibc 扩展接口。

## mallinfo_task

```c
struct mallinfo_task mallinfo_task(FAR const struct malltask *task);
```

获取指定任务或特定类型的内存分配信息。这是 Vela 提供的扩展接口，可以用于追踪每个任务的内存使用情况，帮助定位内存泄漏。

*参数*：

- `task` 指向 `struct malltask` 结构体的指针，包含：
  - `pid` 进程 ID。可以是具体的进程 ID，也可以是以下特殊值：
    - `PID_MM_MEMPOOL`（-1）：查询内存池分配。
    - `PID_MM_LEAK`（-2）：查询可能的内存泄漏（分配者已退出）。
    - `PID_MM_ALLOC`（-3）：查询所有已分配的内存。
    - `PID_MM_FREE`（-4）：查询空闲内存。
    - `PID_MM_BIGGEST`（-5）：查询最大内存块。
    - `PID_MM_ORPHAN`（-6）：查询孤立内存块。
  - `seqmin` 最小序列号（需要配置 `CONFIG_MM_RECORD_SEQNO`）。
  - `seqmax` 最大序列号（需要配置 `CONFIG_MM_RECORD_SEQNO`）。

*返回值*：

返回 `struct mallinfo_task` 结构体，包含：

- `aordblks` 该任务已分配块的数量。
- `uordblks` 该任务已分配内存的总大小（字节）。

*注意*：

- 使用 `PID_MM_LEAK` 可以快速发现已退出任务遗留的内存块，这些很可能是内存泄漏。
- 序列号功能需要启用 `CONFIG_MM_RECORD_SEQNO`，可以用于追踪特定时间段内的分配。

*`POSIX` 兼容性*：Vela 扩展接口。

## malloc_size

```c
size_t malloc_size(void *ptr);
```

获取之前分配的内存块的实际可用大小。由于内存对齐和堆管理的需要，实际分配的内存可能比请求的大小更大。

*参数*：

- `ptr` 指向之前分配的内存块的指针。

*返回值*：

返回内存块的实际可用大小（字节）。这个值通常大于或等于分配时请求的大小。

*注意*：

- 也可以使用别名 `malloc_usable_size()`（与 glibc 兼容）。
- 可以安全地使用返回值范围内的所有内存。
- 如果 `ptr` 不是有效的分配指针，行为是未定义的。

*`POSIX` 兼容性*：兼容 glibc/macOS 扩展接口。

## mallopt

```c
int mallopt(int param, int value);
```

调整内存分配器的参数。此函数提供了一种控制内存分配器行为的方式。

*参数*：

- `param` 要调整的参数，定义的选项包括：
  - `M_TRIM_THRESHOLD` 收缩阈值
  - `M_TOP_PAD` 顶部填充
  - `M_MMAP_THRESHOLD` mmap 阈值
  - `M_MMAP_MAX` 最大 mmap 数量
  - `M_CHECK_ACTION` 检查动作
  - `M_PERTURB` 内存扰动
  - `M_ARENA_TEST` arena 测试
  - `M_ARENA_MAX` 最大 arena 数量
- `value` 参数值。

*返回值*：

成功返回非零值，失败返回 0。

*注意*：

- Vela 当前实现总是返回 1（成功），不实际处理任何参数。
- 此接口仅为兼容性目的提供。

*`POSIX` 兼容性*：兼容 glibc 扩展接口（仅接口兼容，无实际功能）。

---

## 内核堆接口

当启用 `CONFIG_MM_KERNEL_HEAP` 时，Vela 提供独立的内核堆接口。内核堆用于内核态的内存分配，与用户堆完全隔离，确保内核数据的安全性。

在 Protected Build 和 Kernel Build 模式下，内核堆和用户堆使用不同的内存区域，由 MPU 或 MMU 保护。用户态代码无法直接访问内核堆内存。

### kmm_initialize

```c
void kmm_initialize(void *heap_start, size_t heap_size);
```

初始化内核堆。此函数通常在系统启动早期由板级初始化代码调用。

*参数*：

- `heap_start` 内核堆内存的起始地址。
- `heap_size` 内核堆的大小（字节）。

*返回值*：

无返回值。

*注意*：

- 此函数只应调用一次，重复调用会导致未定义行为。
- 需要启用 `CONFIG_MM_KERNEL_HEAP` 配置。

### kmm_malloc

```c
void *kmm_malloc(size_t size);
```

从内核堆分配内存。功能与 `malloc()` 相同，但从内核堆而非用户堆分配。

*参数*：

- `size` 要分配的内存大小（字节）。

*返回值*：

成功时返回指向分配内存的指针，失败时返回 `NULL`。

*注意*：

- 分配的内存只能使用 `kmm_free()` 释放。
- 内核堆分配的内存不应传递给用户态代码。

### kmm_free

```c
void kmm_free(void *mem);
```

释放之前通过 `kmm_malloc()`、`kmm_calloc()` 等从内核堆分配的内存。

*参数*：

- `mem` 指向要释放的内存块的指针。如果为 `NULL`，则不执行任何操作。

*返回值*：

无返回值。

*注意*：

- 只能释放内核堆分配的内存，不能用于释放用户堆内存。
- 可以使用 `kmm_heapmember()` 检查指针是否属于内核堆。

### kmm_calloc

```c
void *kmm_calloc(size_t n, size_t elem_size);
```

从内核堆分配内存并清零。功能与 `calloc()` 相同，但从内核堆分配。

*参数*：

- `n` 要分配的元素数量。
- `elem_size` 每个元素的大小（字节）。

*返回值*：

成功时返回指向分配并清零的内存的指针，失败时返回 `NULL`。

### kmm_realloc

```c
void *kmm_realloc(void *oldmem, size_t newsize);
```

重新分配内核堆内存。功能与 `realloc()` 相同，但在内核堆上操作。

*参数*：

- `oldmem` 指向之前从内核堆分配的内存块的指针。如果为 `NULL`，则等同于 `kmm_malloc(newsize)`。
- `newsize` 新的内存大小（字节）。如果为 0，则释放内存。

*返回值*：

成功时返回指向重新分配内存的指针（可能与原指针不同），失败时返回 `NULL`（原内存块保持不变）。

### kmm_zalloc

```c
void *kmm_zalloc(size_t size);
```

从内核堆分配内存并清零。功能与 `zalloc()` 相同，但从内核堆分配。

*参数*：

- `size` 要分配的内存大小（字节）。

*返回值*：

成功时返回指向分配并清零的内存的指针，失败时返回 `NULL`。

### kmm_memalign

```c
void *kmm_memalign(size_t alignment, size_t size);
```

从内核堆分配对齐内存。功能与 `memalign()` 相同，但从内核堆分配。

*参数*：

- `alignment` 对齐边界，必须是 2 的幂次方。
- `size` 要分配的内存大小（字节）。

*返回值*：

成功时返回按指定边界对齐的内存指针，失败时返回 `NULL`。

*注意*：

- 用于内核需要对齐内存的场景，如 DMA 缓冲区。

### kmm_mallinfo

```c
struct mallinfo kmm_mallinfo(void);
```

获取内核堆的分配信息。功能与 `mallinfo()` 相同，但返回内核堆的统计信息。

*参数*：

无参数。

*返回值*：

返回 `struct mallinfo` 结构体，包含内核堆的内存分配统计信息：

- `arena` 内核堆的总大小（字节）。
- `ordblks` 空闲块的数量。
- `uordblks` 已使用的内存大小（字节）。
- `fordblks` 空闲内存大小（字节）。
- `mxordblk` 最大连续空闲块大小（字节）。

*注意*：

- 可用于监控内核内存使用情况。

### kmm_heapmember

```c
bool kmm_heapmember(void *mem);
```

检查内存地址是否属于内核堆。

*参数*：

- `mem` 要检查的内存地址。

*返回值*：

如果内存地址属于内核堆，返回 `true`；否则返回 `false`。

*注意*：

- 可用于确定内存块应该使用 `kmm_free()` 还是 `free()` 释放。
- 在内存管理代码中用于路由释放请求到正确的堆。

### kmm_checkcorruption

```c
void kmm_checkcorruption(void);
```

检查内核堆是否存在内存损坏。

*参数*：

无参数。

*返回值*：

无返回值。如果检测到内存损坏，将触发断言或输出调试信息。

*注意*：

- 需要启用 `CONFIG_MM_HEAP_CHECK` 配置。
- 用于调试内存相关问题。

---

## 堆管理接口

以下接口用于堆的初始化、扩展和管理，通常由系统启动代码或驱动程序使用。这些函数操作 `struct mm_heap_s` 堆结构，提供了对多个独立堆的管理能力。

### mm_initialize

```c
struct mm_heap_s *mm_initialize(const char *name, void *heapstart, size_t heapsize);
```

初始化一个新的堆。分配并初始化堆管理结构，设置初始空闲块。

*参数*：

- `name` 堆的名称，用于调试和识别。
- `heapstart` 堆内存的起始地址。
- `heapsize` 堆的大小（字节）。

*返回值*：

成功时返回指向初始化的堆结构的指针，失败时返回 `NULL`。

*注意*：

- 堆大小必须足够大以容纳堆管理开销。
- 系统可以有多个独立的堆，如用户堆、内核堆、图形堆等。

### mm_uninitialize

```c
void mm_uninitialize(struct mm_heap_s *heap);
```

销毁一个堆，释放堆管理结构占用的资源。

*参数*：

- `heap` 要销毁的堆结构指针。

*返回值*：

无返回值。

*注意*：

- 销毁前应确保堆中没有活动的分配。

### mm_addregion

```c
void mm_addregion(struct mm_heap_s *heap, void *heapstart, size_t heapsize);
```

向现有堆添加一个新的内存区域。这允许堆使用非连续的内存区域。

*参数*：

- `heap` 堆结构指针。
- `heapstart` 新内存区域的起始地址。
- `heapsize` 新内存区域的大小（字节）。

*返回值*：

无返回值。

*注意*：

- 新增区域可以在物理上与已有区域不连续。
- 最大区域数量由 `CONFIG_MM_REGIONS` 配置。

### mm_extend

```c
void mm_extend(struct mm_heap_s *heap, void *mem, size_t size, int region);
```

扩展堆的指定内存区域。新增内存必须与现有区域相邻。

*参数*：

- `heap` 堆结构指针。
- `mem` 新增内存区域的起始地址。
- `size` 新增内存区域的大小（字节）。
- `region` 区域索引（从 0 开始）。

*返回值*：

无返回值。

*注意*：

- 新增的内存区域必须与现有区域在物理地址上相邻。
- 与 `mm_addregion()` 不同，此函数用于扩展已有区域而非添加新区域。

### mm_brkaddr

```c
void *mm_brkaddr(struct mm_heap_s *heap, int region);
```

获取堆指定区域的当前 break 地址（区域末尾地址）。

*参数*：

- `heap` 堆结构指针。
- `region` 区域索引（从 0 开始）。

*返回值*：

返回指定区域的当前 break 地址。

*注意*：

- 用于确定可以扩展的内存位置。

### mm_heapmember

```c
bool mm_heapmember(struct mm_heap_s *heap, void *mem);
```

检查内存地址是否属于指定堆的任意区域。

*参数*：

- `heap` 堆结构指针。
- `mem` 要检查的内存地址。

*返回值*：

如果内存地址属于指定堆，返回 `true`；否则返回 `false`。

*注意*：

- 用于确定内存分配来源，以便使用正确的接口释放。

### umm_initialize

```c
void umm_initialize(void *heap_start, size_t heap_size);
```

初始化用户堆。此函数通常在系统启动时由初始化代码调用。

*参数*：

- `heap_start` 堆内存的起始地址。
- `heap_size` 堆的大小（字节）。

*返回值*：

无返回值。

*注意*：

- 此函数只应调用一次。
- 用户堆是 `malloc()` 等标准接口的默认堆。

### umm_heapmember

```c
bool umm_heapmember(void *mem);
```

检查内存地址是否属于用户堆。

*参数*：

- `mem` 要检查的内存地址。

*返回值*：

如果内存地址属于用户堆，返回 `true`；否则返回 `false`。

*注意*：

- 与 `kmm_heapmember()` 配合使用，可以确定内存来源。

---

## 调试接口

以下接口用于内存调试和问题诊断。这些功能对于检测内存泄漏、内存损坏和优化内存使用非常有用。

### mm_memdump

```c
void mm_memdump(struct mm_heap_s *heap, const struct mm_memdump_s *dump);
```

转储堆的内存分配信息，用于调试内存泄漏和分析内存使用情况。

*参数*：

- `heap` 堆结构指针。如果为 `NULL`，则转储用户堆。
- `dump` 指向 `struct mm_memdump_s` 结构体的指针，用于指定转储条件。

*返回值*：

无返回值。

*注意*：

- `mm_memdump_s` 是 `malltask` 的类型别名，结构体字段与 `mallinfo_task()` 中描述的 `malltask` 相同。
- 输出信息包括每个分配块的地址、大小、分配者 PID 和分配时的调用栈（如果启用了 `CONFIG_MM_BACKTRACE`）。
- 常用于诊断内存泄漏，找出哪些代码分配了内存但未释放。

### mm_checkcorruption

```c
void mm_checkcorruption(struct mm_heap_s *heap);
```

检查堆是否存在内存损坏。此函数遍历堆中所有内存块，验证其完整性。

*参数*：

- `heap` 要检查的堆结构指针。

*返回值*：

无返回值。如果检测到内存损坏，将触发断言或输出调试信息。

*注意*：

- 需要启用 `CONFIG_DEBUG_MM` 配置。
- 检测的问题包括：块头损坏、双重释放、越界写入等。
- 此函数会遍历整个堆，对性能有影响，主要用于调试。

### umm_checkcorruption

```c
void umm_checkcorruption(void);
```

检查用户堆是否存在内存损坏。这是 `mm_checkcorruption()` 对用户堆的便捷包装。

*参数*：

无参数。

*返回值*：

无返回值。如果检测到内存损坏，将触发断言或输出调试信息。

*注意*：

- 需要启用 `CONFIG_DEBUG_MM` 配置。
- 可以在怀疑有内存问题时调用此函数进行检查。
