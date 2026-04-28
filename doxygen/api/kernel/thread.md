# 线程 API

openvela 提供 POSIX 兼容的线程（pthread）接口，支持线程创建、同步、属性管理等功能。

头文件：`#include <pthread.h>`

## openvela 实现说明

openvela 的 pthread 实现基于 NuttX RTOS 内核，与标准 Linux 实现存在以下差异：

- **`pthread_t` 即 `pid_t`**：在 openvela 中，线程 ID 的底层类型是 `pid_t`（进程 ID），可以直接用于 `kill()` 等系统调用。
- **无进程隔离**：openvela 不支持 Linux 意义上的进程，所有线程运行在同一地址空间。`PTHREAD_PROCESS_SHARED` 属性可设置但行为与 `PTHREAD_PROCESS_PRIVATE` 相同。
- **竞争范围固定**：仅支持 `PTHREAD_SCOPE_SYSTEM`，`PTHREAD_SCOPE_PROCESS` 返回 `ENOTSUP`。
- **`fork()` 支持有限**：`pthread_atfork()` 接口存在但 `fork()` 在 RTOS 环境中可能不可用，主要用于 POSIX 兼容性。
- **条件编译依赖**：部分功能需要特定配置项：
  - `CONFIG_SMP`：CPU 亲和性接口（`pthread_setaffinity_np` 等）
  - `CONFIG_PRIORITY_INHERITANCE`：优先级继承协议（`PTHREAD_PRIO_INHERIT`）
  - `CONFIG_PRIORITY_PROTECT`：优先级上限保护（`PTHREAD_PRIO_PROTECT`、`prioceiling` 相关接口）
  - `CONFIG_RR_INTERVAL > 0`：`SCHED_RR` 调度策略
  - `CONFIG_SCHED_SPORADIC`：`SCHED_SPORADIC` 调度策略


## 线程创建与管理


### pthread_create

```c
int pthread_create(pthread_t *thread, const pthread_attr_t *attr,
                   pthread_startroutine_t start_routine, pthread_addr_t arg);
```

> **类型说明**：`pthread_startroutine_t` 等价于 `void *(*)(void *)`，`pthread_addr_t` 等价于 `void *`，均为 NuttX 的类型别名。

创建一个新线程并使其可运行。新线程从 `start_routine` 函数开始执行，该函数接收 `arg` 作为唯一参数。线程属性对象 `attr` 指定了新线程的各种属性，如栈大小、调度策略、优先级等。

如果 `attr` 为 `NULL`，则使用默认属性创建线程。默认情况下，线程是可连接的（joinable），具有默认的栈大小和调度策略。

**参数**：

- `thread` 指向 `pthread_t` 类型的指针，用于存储新创建线程的 ID。成功时，线程 ID 会被写入此位置。
- `attr` 指向线程属性对象的指针。如果为 `NULL`，使用默认属性（栈大小为 `PTHREAD_STACK_DEFAULT`，调度策略为 `SCHED_OTHER`，可连接状态）。
- `start_routine` 线程入口函数，函数签名为 `void *(*)(void *)`。新线程将从此函数开始执行。
- `arg` 传递给入口函数的参数。如果需要传递多个参数，可以传递结构体指针。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EAGAIN` 系统资源不足，无法创建新线程，或达到了系统线程数限制。
- `EINVAL` `attr` 中的设置无效。
- `EPERM` 没有权限设置指定的调度策略或参数。

**注意**：

- 新创建的线程与调用线程共享相同的地址空间、文件描述符和信号处理。
- 如果线程创建时指定了 `PTHREAD_CREATE_DETACHED` 状态，线程终止后会自动释放资源，无需调用 `pthread_join()`。
- 线程创建后立即可调度运行，不保证创建顺序就是执行顺序。
- 线程的返回值可以通过 `pthread_join()` 获取，或通过 `pthread_exit()` 显式返回。
- 确保传递给线程的参数在线程执行期间保持有效，避免传递栈上的局部变量地址。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_exit

```c
void pthread_exit(void *exit_value);
```

终止调用线程并返回一个值，该值可被其他调用 `pthread_join()` 等待此线程的线程获取。此函数不会返回到调用者。

调用 `pthread_exit()` 等效于从线程入口函数返回，但可以在线程调用的任何函数中调用。线程终止时，会执行以下清理操作：

1. 调用通过 `pthread_cleanup_push()` 注册的清理函数（按注册顺序的逆序）。
2. 调用线程特定数据的析构函数（对于所有非 `NULL` 的线程特定数据键）。
3. 如果线程是可连接的，保留线程 ID 和返回值，直到其他线程调用 `pthread_join()`。
4. 如果线程是分离的，立即释放所有资源。

**参数**：

- `exit_value` 线程返回值，这是一个无类型指针，可以传递任何数据的地址。等待此线程的 `pthread_join()` 调用可以获取此值。如果线程被取消，返回值为 `PTHREAD_CANCELED`。

**返回值**：

此函数不返回。调用后，调用线程终止。

**注意**：

- 不要在 `main()` 函数中调用 `pthread_exit()`，这会终止主线程但不终止进程，可能导致其他线程成为孤儿。
- 如果线程已分离，`exit_value` 将被忽略，因为没有线程可以通过 `pthread_join()` 获取返回值。
- 线程终止时，不会自动关闭打开的文件描述符或释放分配的内存，这些资源由整个进程共享。
- 从线程入口函数返回隐式调用 `pthread_exit()`，返回值作为线程的退出值。
- 如果线程持有互斥锁，在调用 `pthread_exit()` 前应释放，否则可能导致死锁。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_join

```c
int pthread_join(pthread_t thread, pthread_addr_t *value);
```

> **类型说明**：`pthread_addr_t` 等价于 `void *`，为 NuttX 的类型别名。

阻塞调用线程，直到指定的线程 `thread` 终止。如果该线程已经终止，`pthread_join()` 立即返回。成功返回后，目标线程被"连接"（joined），其资源被回收。

每个可连接的线程只能被连接一次。尝试连接已被连接或分离的线程会导致未定义行为。线程不能连接自己，否则会导致死锁。

**参数**：

- `thread` 要等待的线程 ID，必须是可连接状态的线程。不能是分离状态的线程，也不能是已被连接过的线程。
- `value` 指向指针的指针，用于接收线程的返回值。如果非 `NULL`，目标线程的返回值（通过 `pthread_exit()` 或从入口函数返回）会被写入 `*value`。如果线程被取消，`*value` 设置为 `PTHREAD_CANCELED`。如果不关心返回值，可以传递 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EDEADLK` 检测到死锁（如线程尝试连接自己），或 `thread` 指定另一个正在等待连接调用线程的线程。
- `EINVAL` `thread` 不是可连接的线程，或者已有其他线程正在等待连接该线程。
- `ESRCH` 找不到 ID 为 `thread` 的线程。

**注意**：

- `pthread_join()` 会阻塞调用线程，直到目标线程终止。如果目标线程已经终止，调用立即返回。
- 连接线程后，线程 ID 被回收，不应再使用。
- 如果多个线程同时尝试连接同一个线程，行为是未定义的。
- 不连接可连接的线程会导致资源泄漏（类似于内存泄漏），线程资源不会被回收。
- 对于不需要获取返回值的线程，建议在创建时设置为分离状态，或创建后调用 `pthread_detach()`。
- 在 openvela 中，线程 ID 实际上是进程 ID（`pid_t`），可以用于其他系统调用。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_detach

```c
int pthread_detach(pthread_t thread);
```

将指定线程标记为分离状态。分离状态的线程在终止时会自动释放所有资源，无需其他线程调用 `pthread_join()` 来回收。一旦线程被分离，就不能再被连接，线程的返回值也无法获取。

线程可以通过两种方式变为分离状态：
1. 创建时在属性对象中设置 `PTHREAD_CREATE_DETACHED`。
2. 创建后调用 `pthread_detach()`。

线程也可以分离自己，通过 `pthread_detach(pthread_self())`。

**参数**：

- `thread` 要分离的线程 ID。可以是其他线程的 ID，也可以是调用线程自己的 ID（通过 `pthread_self()` 获取）。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `thread` 不是可连接的线程（可能已经是分离状态）。
- `ESRCH` 找不到 ID 为 `thread` 的线程。

**注意**：

- 分离线程后，不能再调用 `pthread_join()` 等待该线程，否则会返回错误。
- 分离状态是不可逆的，一旦分离就无法再变回可连接状态。
- 对于不需要获取返回值或等待其完成的线程，应该设置为分离状态，以避免资源泄漏。
- 分离状态不影响线程的执行，只影响线程终止后的资源回收方式。
- 如果对已分离的线程再次调用 `pthread_detach()`，会返回 `EINVAL` 错误。
- 主线程可以是分离的，但这通常不是好的做法，因为主线程终止会导致整个进程终止。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_cancel

```c
int pthread_cancel(pthread_t thread);
```

向指定线程发送取消请求。线程是否响应取消请求取决于其取消状态（由 `pthread_setcancelstate()` 设置）和取消类型（由 `pthread_setcanceltype()` 设置）。

如果取消请求成功传递，目标线程的取消状态和类型决定了何时以及如何处理取消：

- 如果取消状态为 `PTHREAD_CANCEL_DISABLE`，取消请求被挂起，直到取消状态变为 `PTHREAD_CANCEL_ENABLE`。
- 如果取消状态为 `PTHREAD_CANCEL_ENABLE`，且取消类型为 `PTHREAD_CANCEL_DEFERRED`，取消在下一个取消点发生。
- 如果取消类型为 `PTHREAD_CANCEL_ASYNCHRONOUS`，取消可能立即发生（但也可能延迟）。

**参数**：

- `thread` 要取消的线程 ID。不能取消自己（应使用 `pthread_exit()`）。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ESRCH` 找不到 ID 为 `thread` 的线程。

**注意**：

- `pthread_cancel()` 只是发送取消请求，不会等待线程实际终止。
- 被取消的线程的退出值为 `PTHREAD_CANCELED`。
- 异步取消（`PTHREAD_CANCEL_ASYNCHRONOUS`）是危险的，应仅在特定情况下使用，因为线程可能在任意点被取消，可能导致资源泄漏或数据不一致。
- 延迟取消（`PTHREAD_CANCEL_DEFERRED`，默认）更安全，线程只在取消点被取消，这些点包括 `pthread_testcancel()`、`pthread_join()`、`pthread_cond_wait()` 等阻塞调用。
- 取消线程时，会执行清理处理程序（通过 `pthread_cleanup_push()` 注册）和线程特定数据析构函数。
- 如果线程持有锁或其他资源，应通过清理处理程序确保资源被正确释放。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_setcancelstate

```c
int pthread_setcancelstate(int state, int *oldstate);
```

设置调用线程的取消状态。取消状态决定了线程是否可以被取消。

**参数**：

- `state` 新的取消状态。有效值为：
  - `PTHREAD_CANCEL_ENABLE` 启用取消（默认）。线程可以响应取消请求。
  - `PTHREAD_CANCEL_DISABLE` 禁用取消。取消请求会被挂起，直到取消状态变为启用。
- `oldstate` 如果非 `NULL`，用于存储之前的取消状态。可以传递 `NULL` 如果不需要获取旧值。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `state` 不是有效的取消状态值。

**注意**：

- 新创建的线程默认取消状态为 `PTHREAD_CANCEL_ENABLE`。
- 禁用取消不会丢弃挂起的取消请求，只是延迟其处理。
- 即使禁用取消，线程仍可以通过 `pthread_exit()` 自行终止。
- 在执行关键代码段（如资源分配和初始化）时，应临时禁用取消，完成后再启用。
- 取消状态是线程局部的，每个线程有自己独立的取消状态。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_setcanceltype

```c
int pthread_setcanceltype(int type, int *oldtype);
```

设置调用线程的取消类型。取消类型决定了线程如何响应取消请求。

**参数**：

- `type` 新的取消类型。有效值为：
  - `PTHREAD_CANCEL_DEFERRED` 延迟取消（默认）。取消请求在下一个取消点才会处理。取消点包括 `pthread_testcancel()`、`pthread_join()`、`pthread_cond_wait()`、`pthread_cond_timedwait()`、`sem_wait()` 等阻塞函数。
  - `PTHREAD_CANCEL_ASYNCHRONOUS` 异步取消。线程可以在任何时刻被取消（实际行为依赖于实现）。这种模式非常危险，应避免使用。
- `oldtype` 如果非 `NULL`，用于存储之前的取消类型。可以传递 `NULL` 如果不需要获取旧值。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `type` 不是有效的取消类型值。

**注意**：

- 新创建的线程默认取消类型为 `PTHREAD_CANCEL_DEFERRED`。
- 延迟取消是推荐的取消类型，因为它只在定义明确的取消点响应取消，确保线程处于已知状态。
- 异步取消可能在任意指令处中断线程，可能导致资源泄漏、数据损坏或未定义行为。只有确保线程代码是异步取消安全的，才应使用异步取消。
- 如果使用异步取消，线程不应调用非异步取消安全的函数，包括大多数库函数。
- 取消类型是线程局部的，每个线程有自己独立的取消类型。
- 即使设置了异步取消，实现也可能将其视为延迟取消。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_testcancel

```c
void pthread_testcancel(void);
```

创建一个取消点。如果有挂起的取消请求且取消状态为启用，则线程将被取消并不返回。这是一种显式检查并响应取消请求的方式。

取消点是线程可以响应取消请求的位置。POSIX 定义了一些函数必须是取消点（如 `pthread_join()`、`sem_wait()` 等阻塞调用），而 `pthread_testcancel()` 允许在任意位置创建取消点。

**参数**：

无参数。

**返回值**：

如果没有挂起的取消请求，函数正常返回。如果有挂起的取消请求，函数不返回，线程被取消。

**注意**：

- 如果线程取消状态为 `PTHREAD_CANCEL_DISABLE`，`pthread_testcancel()` 不起作用，直接返回。
- 此函数通常用于长时间运行的计算密集型代码中，以提供响应取消请求的机会。
- 应在适当的位置（如循环中）定期调用 `pthread_testcancel()`，以确保线程能够及时响应取消请求。
- 如果线程被取消，会执行清理处理程序和线程特定数据析构函数。
- 过于频繁地调用 `pthread_testcancel()` 可能影响性能；应在逻辑上合理的位置调用。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_self

```c
pthread_t pthread_self(void);
```

获取调用线程的线程 ID。线程 ID 在进程内唯一标识一个线程，可用于 `pthread_join()`、`pthread_detach()`、`pthread_equal()` 等函数。

在 openvela 中，`pthread_t` 实际上是 `pid_t` 类型，即线程 ID 与进程 ID 相同。

**参数**：

无参数。

**返回值**：

返回调用线程的线程 ID。此函数总是成功，不会失败。

**注意**：

- 线程 ID 在线程生命周期内保持不变。
- 线程 ID 在线程终止并被连接后可能被重用。
- 不要依赖线程 ID 的数值或顺序，它们是不透明的标识符。
- 可以用 `pthread_self()` 获取的 ID 调用 `pthread_detach(pthread_self())` 来分离当前线程。
- 在 openvela 中，可以将线程 ID 用于系统调用，如信号发送等。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_equal

```c
int pthread_equal(pthread_t t1, pthread_t t2);
```

比较两个线程 ID 是否相等。由于线程 ID 的内部表示可能是复杂的数据结构，POSIX 要求使用此函数而不是直接用 `==` 比较。

**参数**：

- `t1` 第一个线程 ID。
- `t2` 第二个线程 ID。

**返回值**：

如果两个线程 ID 相等，返回非零值；否则返回 0。

**注意**：

- 在 openvela 中，`pthread_t` 是简单的整数类型（`pid_t`），可以直接用 `==` 比较，但为了可移植性，建议使用 `pthread_equal()`。
- 终止的线程 ID 可能被重用，因此不应假设 ID 的唯一性跨越线程生命周期。
- 常用于判断某个线程 ID 是否是当前线程：`pthread_equal(thread_id, pthread_self())`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_yield

```c
void pthread_yield(void);
```

主动让出处理器，允许其他线程运行。这是一个优化提示，实际行为取决于调度策略。

调用 `pthread_yield()` 后，调用线程被放置在其优先级队列的末尾，调度器选择下一个可运行的线程。如果没有其他同等或更高优先级的就绪线程，调用线程可能立即继续执行。

**参数**：

无参数。

**返回值**：

无返回值。

**注意**：

- 此函数是非标准的扩展接口，但在许多系统上可用（Linux、BSD 等）。
- 在 POSIX 标准中，应使用 `sched_yield()` 替代。
- 适用于协作式多任务场景，线程主动让出 CPU 给其他线程。
- 不应依赖 `pthread_yield()` 来解决同步问题，应使用适当的同步原语（如互斥锁、条件变量）。
- 过度使用 `pthread_yield()` 可能导致性能下降，应仅在明确需要时使用。
- 在实时系统中，`pthread_yield()` 的行为取决于调度策略（FIFO、RR 等）。

**POSIX 兼容性**：兼容扩展接口（非 POSIX 标准，但广泛支持）。


### pthread_once

```c
int pthread_once(pthread_once_t *once_control, void (*init_routine)(void));
```

确保初始化函数 `init_routine` 在进程生命周期内只被调用一次，无论有多少线程调用 `pthread_once()`。这是一种线程安全的单次初始化机制，常用于全局资源的延迟初始化。

`once_control` 必须是静态或全局变量，并使用 `PTHREAD_ONCE_INIT` 初始化。多个线程可以同时调用 `pthread_once()`，但 `init_routine` 只会被执行一次，其他线程会阻塞等待直到初始化完成。

**参数**：

- `once_control` 控制变量，用于跟踪初始化状态。必须使用 `PTHREAD_ONCE_INIT` 初始化（如 `pthread_once_t once = PTHREAD_ONCE_INIT;`）。
- `init_routine` 初始化函数，无参数无返回值。此函数在整个进程生命周期内只会被调用一次。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `once_control` 或 `init_routine` 为 `NULL`。

**注意**：

- `pthread_once()` 是线程安全的，可以从多个线程同时调用。
- 初始化函数应快速完成，避免阻塞其他等待初始化完成的线程。
- 如果初始化函数内部调用 `pthread_once()` 使用相同的 `once_control`，行为是未定义的（可能死锁）。
- 初始化函数不应调用 `pthread_exit()` 或被取消，否则初始化被视为未完成，下次调用 `pthread_once()` 会再次执行初始化。
- 常用于单例模式、全局资源初始化等场景。
- `once_control` 变量不应被直接修改，只能通过 `pthread_once()` 操作。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_atfork

```c
int pthread_atfork(void (*prepare)(void), void (*parent)(void), void (*child)(void));
```

注册在 `fork()` 调用时执行的处理函数。这些函数用于处理多线程环境中 `fork()` 带来的问题，特别是锁状态的一致性。

当调用 `fork()` 时，处理函数按以下顺序执行：
1. 在 `fork()` 之前，在父进程中调用所有 `prepare` 函数（按注册顺序的逆序）。
2. `fork()` 创建子进程。
3. 在子进程中调用所有 `child` 函数（按注册顺序）。
4. 在父进程中调用所有 `parent` 函数（按注册顺序）。

**参数**：

- `prepare` 在 `fork()` 前在父进程中调用。通常用于获取所有锁，确保一致状态。可以为 `NULL`。
- `parent` 在 `fork()` 后在父进程中调用。通常用于释放 `prepare` 中获取的锁。可以为 `NULL`。
- `child` 在 `fork()` 后在子进程中调用。通常用于重新初始化锁状态和其他资源。可以为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ENOMEM` 内存不足，无法分配记录处理函数所需的空间。

**注意**：

- 可以多次调用 `pthread_atfork()` 注册多组处理函数。
- `prepare` 函数按注册顺序的逆序调用，`parent` 和 `child` 函数按注册顺序调用。
- 在多线程程序中使用 `fork()` 是危险的，因为子进程只继承调用 `fork()` 的线程，其他线程在子进程中不存在，但它们持有的锁状态被继承，可能导致死锁。
- `pthread_atfork()` 处理函数应快速执行，避免调用可能阻塞或使用锁的复杂函数。
- 在子进程中，只应调用异步信号安全的函数（如 `exec()` 系列函数）。
- openvela 作为 RTOS，`fork()` 支持可能有限或不存在，此接口主要用于兼容性。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 线程属性


### pthread_attr_init

```c
int pthread_attr_init(pthread_attr_t *attr);
```

初始化线程属性对象为默认值。属性对象用于在创建线程时指定线程的各种属性，如栈大小、调度策略、优先级、分离状态等。

初始化后的属性对象包含以下默认值：
- 分离状态：`PTHREAD_CREATE_JOINABLE`（可连接）
- 栈大小：`PTHREAD_STACK_DEFAULT`（系统默认）
- 调度策略：`SCHED_OTHER`（或系统默认策略）
- 调度继承：`PTHREAD_INHERIT_SCHED`（继承父线程）
- 作用域：`PTHREAD_SCOPE_SYSTEM`

**参数**：

- `attr` 指向要初始化的线程属性对象。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ENOMEM` 内存不足，无法初始化属性对象。

**注意**：

- 属性对象初始化后，可以通过各种 `pthread_attr_set*()` 函数修改具体属性。
- 同一个属性对象可以用于创建多个线程。
- 使用完毕后，应调用 `pthread_attr_destroy()` 销毁属性对象，释放资源。
- 属性对象的修改不影响已创建的线程，只影响后续使用该属性对象创建的线程。
- 在 openvela 中，属性对象是简单的结构体，不涉及动态内存分配。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_destroy

```c
int pthread_attr_destroy(pthread_attr_t *attr);
```

销毁线程属性对象，释放其占用的资源。销毁后的属性对象不能再使用，除非重新初始化。

**参数**：

- `attr` 指向要销毁的属性对象。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 不是有效的属性对象。

**注意**：

- 销毁属性对象不影响已使用该对象创建的线程。
- 销毁后的属性对象可以通过 `pthread_attr_init()` 重新初始化并使用。
- 在 openvela 中，属性对象通常不涉及动态内存，此函数主要用于 POSIX 兼容性。
- 应始终配对调用 `pthread_attr_init()` 和 `pthread_attr_destroy()`，遵循资源管理的最佳实践。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_setdetachstate

```c
int pthread_attr_setdetachstate(pthread_attr_t *attr, int detachstate);
```

设置线程属性对象中的分离状态。分离状态决定线程终止后资源的回收方式。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `detachstate` 分离状态，有效值为：
  - `PTHREAD_CREATE_JOINABLE` 可连接（默认），需要其他线程调用 `pthread_join()` 回收资源。
  - `PTHREAD_CREATE_DETACHED` 分离状态，线程终止后自动释放资源。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `detachstate` 不是有效值。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_getdetachstate

```c
int pthread_attr_getdetachstate(const pthread_attr_t *attr, int *detachstate);
```

获取线程属性对象中的分离状态。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `detachstate` 指向整型变量，用于存储分离状态。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `detachstate` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_setstacksize

```c
int pthread_attr_setstacksize(pthread_attr_t *attr, size_t stacksize);
```

设置线程属性对象中的栈大小。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `stacksize` 栈大小（字节）。不能小于 `PTHREAD_STACK_MIN`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `stacksize` 小于 `PTHREAD_STACK_MIN`。

**注意**：

- 栈大小应根据线程的实际需求设置，过小可能导致栈溢出。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_getstacksize

```c
int pthread_attr_getstacksize(const pthread_attr_t *attr, size_t *stacksize);
```

获取线程属性对象中的栈大小。

**参数**：

- `attr` 指向线程属性对象。
- `stacksize` 指向 `size_t` 变量，用于存储栈大小。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `stacksize` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_setstackaddr

```c
int pthread_attr_setstackaddr(pthread_attr_t *attr, void *stackaddr);
```

设置线程属性对象中的栈地址。允许应用程序为线程指定预分配的栈内存。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `stackaddr` 栈内存的起始地址。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `stackaddr` 为 `NULL`。

**注意**：

- 此接口已被 POSIX 标记为废弃（obsolete），建议使用 `pthread_attr_setstack()` 替代，后者可同时设置栈地址和栈大小。
- 使用自定义栈时，应用程序负责栈内存的分配和释放。
- 栈内存必须在线程生命周期内保持有效。

**POSIX 兼容性**：兼容 `POSIX` 同名接口（已废弃）。


### pthread_attr_getstackaddr

```c
int pthread_attr_getstackaddr(const pthread_attr_t *attr, void **stackaddr);
```

获取线程属性对象中的栈地址。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `stackaddr` 指向指针变量，用于存储栈地址。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `stackaddr` 为 `NULL`。

**注意**：

- 此接口已被 POSIX 标记为废弃，建议使用 `pthread_attr_getstack()` 替代。

**POSIX 兼容性**：兼容 `POSIX` 同名接口（已废弃）。


### pthread_attr_setstack

```c
int pthread_attr_setstack(pthread_attr_t *attr, void *stackaddr, size_t stacksize);
```

同时设置线程属性对象中的栈地址和栈大小。这是 `pthread_attr_setstackaddr()` 和 `pthread_attr_setstacksize()` 的组合替代接口。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `stackaddr` 栈内存的起始地址。不能为 `NULL`。
- `stacksize` 栈大小（字节）。不能小于 `PTHREAD_STACK_MIN`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `stackaddr` 为 `NULL`，或 `stacksize` 小于 `PTHREAD_STACK_MIN`。

**注意**：

- 使用自定义栈时，应用程序负责栈内存的分配和释放，且内存必须在线程生命周期内有效。
- 栈大小应考虑线程的实际需求，包括局部变量、函数调用深度等。
- 在 openvela 中，`PTHREAD_STACK_MIN` 的值取决于系统配置。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_getstack

```c
int pthread_attr_getstack(const pthread_attr_t *attr, void **stackaddr, size_t *stacksize);
```

同时获取线程属性对象中的栈地址和栈大小。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `stackaddr` 指向指针变量，用于存储栈地址。不能为 `NULL`。
- `stacksize` 指向 `size_t` 变量，用于存储栈大小。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr`、`stackaddr` 或 `stacksize` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_setguardsize

```c
int pthread_attr_setguardsize(pthread_attr_t *attr, size_t guardsize);
```

设置线程属性对象中的栈保护区大小。保护区是栈末尾的一段不可访问内存，用于检测栈溢出。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `guardsize` 保护区大小（字节）。设置为 0 表示禁用栈保护。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`。

**注意**：

- 如果使用 `pthread_attr_setstack()` 指定了自定义栈，保护区设置可能被忽略。
- 实际保护区大小可能被系统向上取整到页大小的整数倍。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_getguardsize

```c
int pthread_attr_getguardsize(const pthread_attr_t *attr, size_t *guardsize);
```

获取线程属性对象中的栈保护区大小。

**参数**：

- `attr` 指向线程属性对象。
- `guardsize` 指向 `size_t` 变量，用于存储保护区大小。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `guardsize` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_setschedpolicy

```c
int pthread_attr_setschedpolicy(pthread_attr_t *attr, int policy);
```

设置线程属性对象中的调度策略。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `policy` 调度策略，有效值为：
  - `SCHED_OTHER` 默认调度策略。
  - `SCHED_FIFO` 先进先出实时调度。
  - `SCHED_RR` 时间片轮转实时调度（需 `CONFIG_RR_INTERVAL > 0`）。
  - `SCHED_SPORADIC` 偶发调度（需 `CONFIG_SCHED_SPORADIC`）。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `policy` 不是有效的调度策略。

**注意**：

- `SCHED_RR` 和 `SCHED_SPORADIC` 的可用性取决于系统配置。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_getschedpolicy

```c
int pthread_attr_getschedpolicy(const pthread_attr_t *attr, int *policy);
```

获取线程属性对象中的调度策略。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `policy` 指向整型变量，用于存储调度策略。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `policy` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_setschedparam

```c
int pthread_attr_setschedparam(pthread_attr_t *attr, const struct sched_param *param);
```

设置线程属性对象中的调度参数。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `param` 指向调度参数结构体。不能为 `NULL`。主要字段：
  - `sched_priority` 线程优先级。
  - `sched_ss_low_priority` 偶发调度低优先级（需 `CONFIG_SCHED_SPORADIC`）。
  - `sched_ss_repl_period` 偶发调度补充周期。
  - `sched_ss_init_budget` 偶发调度初始预算。
  - `sched_ss_max_repl` 偶发调度最大补充次数。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `param` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_getschedparam

```c
int pthread_attr_getschedparam(const pthread_attr_t *attr, struct sched_param *param);
```

获取线程属性对象中的调度参数。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `param` 指向调度参数结构体，用于存储结果。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `param` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_setinheritsched

```c
int pthread_attr_setinheritsched(pthread_attr_t *attr, int inheritsched);
```

设置线程属性对象中的调度继承方式。决定新线程是继承创建者的调度属性，还是使用属性对象中显式指定的值。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `inheritsched` 继承方式，有效值为：
  - `PTHREAD_INHERIT_SCHED` 继承创建线程的调度策略和参数（默认）。
  - `PTHREAD_EXPLICIT_SCHED` 使用属性对象中设置的调度策略和参数。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `inheritsched` 不是有效值。

**注意**：

- 如果设置为 `PTHREAD_EXPLICIT_SCHED`，需要同时通过 `pthread_attr_setschedpolicy()` 和 `pthread_attr_setschedparam()` 设置调度策略和参数。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_getinheritsched

```c
int pthread_attr_getinheritsched(const pthread_attr_t *attr, int *inheritsched);
```

获取线程属性对象中的调度继承方式。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `inheritsched` 指向整型变量，用于存储继承方式。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `inheritsched` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_setscope

```c
int pthread_attr_setscope(pthread_attr_t *attr, int scope);
```

设置线程属性对象中的竞争范围。竞争范围定义了线程与哪些线程竞争 CPU 等资源。

**参数**：

- `attr` 指向线程属性对象。
- `scope` 竞争范围，有效值为：
  - `PTHREAD_SCOPE_SYSTEM` 系统级竞争，线程与系统中所有线程竞争资源。
  - `PTHREAD_SCOPE_PROCESS` 进程级竞争，线程仅与同一进程内的线程竞争。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `scope` 不是有效值。
- `ENOTSUP` 不支持请求的竞争范围。在 openvela 中，`PTHREAD_SCOPE_PROCESS` 不受支持。

**注意**：

- openvela 仅支持 `PTHREAD_SCOPE_SYSTEM`，这也是默认值。传入 `PTHREAD_SCOPE_PROCESS` 会返回 `ENOTSUP`。
- 在 RTOS 环境中，所有线程天然在系统级别竞争资源。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_getscope

```c
int pthread_attr_getscope(const pthread_attr_t *attr, int *scope);
```

获取线程属性对象中的竞争范围。

**参数**：

- `attr` 指向线程属性对象。
- `scope` 指向整型变量，用于存储竞争范围。

**返回值**：

成功时返回 0。

**注意**：

- 在 openvela 中，始终返回 `PTHREAD_SCOPE_SYSTEM`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_attr_setaffinity_np

```c
int pthread_attr_setaffinity_np(pthread_attr_t *attr, size_t cpusetsize, const cpu_set_t *cpuset);
```

设置线程属性对象中的 CPU 亲和性掩码。使用该属性创建的线程将被限制在指定的 CPU 集合上运行。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `cpusetsize` `cpuset` 缓冲区的大小（字节），必须为 `sizeof(cpu_set_t)`。
- `cpuset` 指向 CPU 集合，指定线程可运行的 CPU。不能为 `NULL`，且集合不能为空。

**返回值**：

成功时返回 0。

**注意**：

- 仅在启用 SMP（`CONFIG_SMP`）时可用。
- 与 `pthread_setaffinity_np()` 不同，此函数设置的是属性对象中的亲和性，在 `pthread_create()` 时生效。
- 使用 `CPU_ZERO()`、`CPU_SET()` 等宏操作 `cpu_set_t`。

**POSIX 兼容性**：兼容 Linux 扩展接口（非 POSIX 标准）。


### pthread_attr_getaffinity_np

```c
int pthread_attr_getaffinity_np(const pthread_attr_t *attr, size_t cpusetsize, cpu_set_t *cpuset);
```

获取线程属性对象中的 CPU 亲和性掩码。

**参数**：

- `attr` 指向线程属性对象。不能为 `NULL`。
- `cpusetsize` `cpuset` 缓冲区的大小（字节），必须为 `sizeof(cpu_set_t)`。
- `cpuset` 指向 CPU 集合，用于存储亲和性掩码。不能为 `NULL`。

**返回值**：

成功时返回 0。

**注意**：

- 仅在启用 SMP（`CONFIG_SMP`）时可用。

**POSIX 兼容性**：兼容 Linux 扩展接口（非 POSIX 标准）。


## 线程调度


### pthread_getschedparam

```c
int pthread_getschedparam(pthread_t thread, int *policy, struct sched_param *param);
```

获取指定线程的调度策略和调度参数。

**参数**：

- `thread` 线程 ID。
- `policy` 指向整型变量，用于存储调度策略。不能为 `NULL`。
- `param` 指向调度参数结构体，用于存储结果。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `policy` 或 `param` 为 `NULL`。
- `ESRCH` 找不到指定线程。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_setschedparam

```c
int pthread_setschedparam(pthread_t thread, int policy, const struct sched_param *param);
```

设置指定线程的调度策略和调度参数。

**参数**：

- `thread` 线程 ID。
- `policy` 调度策略：`SCHED_FIFO`、`SCHED_RR`、`SCHED_OTHER` 或 `SCHED_SPORADIC`。
- `param` 指向调度参数结构体。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` 参数无效。
- `ESRCH` 找不到指定线程。
- `EPERM` 没有权限修改调度参数。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_setschedprio

```c
int pthread_setschedprio(pthread_t thread, int prio);
```

设置指定线程的优先级，不改变调度策略。

**参数**：

- `thread` 线程 ID。
- `prio` 新的优先级值。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` 优先级值无效。
- `ESRCH` 找不到指定线程。

**注意**：

- 此函数仅修改优先级，保留当前调度策略和其他调度参数（如偶发调度参数）不变。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_setaffinity_np

```c
int pthread_setaffinity_np(pthread_t thread, size_t cpusetsize, const cpu_set_t *cpuset);
```

设置线程的 CPU 亲和性掩码。如果线程当前未运行在 `cpuset` 指定的 CPU 上，将被迁移到其中一个 CPU。

**参数**：

- `thread` 线程 ID。
- `cpusetsize` `cpuset` 缓冲区的大小（字节），通常为 `sizeof(cpu_set_t)`。
- `cpuset` 指向 CPU 集合，指定线程可以运行的 CPU。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` 参数无效。
- `ESRCH` 找不到指定线程。

**注意**：

- 仅在启用 SMP（`CONFIG_SMP`）时可用。
- 使用 `CPU_ZERO()`、`CPU_SET()` 等宏操作 `cpu_set_t`。

**POSIX 兼容性**：兼容 Linux 扩展接口（非 POSIX 标准）。


### pthread_getaffinity_np

```c
int pthread_getaffinity_np(pthread_t thread, size_t cpusetsize, cpu_set_t *cpuset);
```

获取线程的 CPU 亲和性掩码。

**参数**：

- `thread` 线程 ID。
- `cpusetsize` `cpuset` 缓冲区的大小（字节），通常为 `sizeof(cpu_set_t)`。
- `cpuset` 指向 CPU 集合，用于存储线程的亲和性掩码。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` 参数无效。
- `ESRCH` 找不到指定线程。

**注意**：

- 仅在启用 SMP（`CONFIG_SMP`）时可用。

**POSIX 兼容性**：兼容 Linux 扩展接口（非 POSIX 标准）。


### pthread_setconcurrency

```c
int pthread_setconcurrency(int new_level);
```

设置并发级别提示。此函数向系统提示应用程序期望的并发线程数，系统可以据此优化线程调度。

**参数**：

- `new_level` 期望的并发级别。值为 0 表示由系统自行决定。不能为负数。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `new_level` 为负数。

**注意**：

- 此函数仅为提示，系统不保证实际并发级别与设置值一致。
- 在 openvela 中，此值存储在全局变量中，不影响实际调度行为。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_getconcurrency

```c
int pthread_getconcurrency(void);
```

获取当前的并发级别提示值。

**参数**：

无参数。

**返回值**：

返回之前通过 `pthread_setconcurrency()` 设置的值。如果从未设置，返回 0。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 互斥锁


### pthread_mutex_init

```c
int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
```

初始化互斥锁。互斥锁用于保护共享资源，确保同一时刻只有一个线程可以访问被保护的临界区。

如果 `attr` 为 `NULL`，使用默认属性：类型为 `PTHREAD_MUTEX_NORMAL`，不支持优先级继承或保护协议，进程私有。

互斥锁也可以使用 `PTHREAD_MUTEX_INITIALIZER` 静态初始化：
```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
```

**参数**：

- `mutex` 指向要初始化的互斥锁对象。
- `attr` 指向互斥锁属性对象。如果为 `NULL`，使用默认属性。属性包括互斥锁类型（normal、recursive、errorcheck）、优先级协议、健壮性等。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EAGAIN` 系统资源不足，无法初始化互斥锁。
- `ENOMEM` 内存不足。
- `EPERM` 调用者没有权限。
- `EINVAL` `attr` 中的属性值无效。

**注意**：

- 初始化后的互斥锁处于未锁定状态。
- 不要重复初始化已初始化的互斥锁，这会导致未定义行为。
- 使用完毕后应调用 `pthread_mutex_destroy()` 销毁互斥锁。
- 静态初始化的互斥锁不需要显式销毁。
- 互斥锁类型影响重复加锁和错误检测行为：
  - `PTHREAD_MUTEX_NORMAL`：不检测死锁，重复加锁会导致死锁。
  - `PTHREAD_MUTEX_ERRORCHECK`：检测死锁和错误，性能略低。
  - `PTHREAD_MUTEX_RECURSIVE`：允许同一线程多次加锁，需要相同次数的解锁。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutex_destroy

```c
int pthread_mutex_destroy(pthread_mutex_t *mutex);
```

销毁互斥锁，释放其占用的资源。

**参数**：

- `mutex` 指向要销毁的互斥锁。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `mutex` 为 `NULL` 或未正确初始化。
- `EBUSY` 互斥锁当前被锁定，无法销毁。

**注意**：

- 不能销毁正在被使用（锁定）的互斥锁。
- 销毁后的互斥锁不能再使用，除非重新初始化。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutex_lock

```c
int pthread_mutex_lock(pthread_mutex_t *mutex);
```

锁定互斥锁。如果互斥锁当前未被锁定，调用线程获得锁并立即返回。如果互斥锁已被其他线程锁定，调用线程阻塞等待，直到锁可用。

具体行为取决于互斥锁类型：
- **NORMAL（默认）**：如果锁已被当前线程持有，再次加锁会导致死锁。
- **ERRORCHECK**：如果锁已被当前线程持有，返回 `EDEADLK` 错误。
- **RECURSIVE**：如果锁已被当前线程持有，递增锁计数，需要相同次数的解锁。

**参数**：

- `mutex` 指向要锁定的互斥锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EDEADLK` 互斥锁类型为 `PTHREAD_MUTEX_ERRORCHECK`，且当前线程已持有该锁（死锁检测）。
- `EINVAL` 互斥锁未正确初始化。
- `EOWNERDEAD` 互斥锁是健壮互斥锁，前一个持有者终止时未释放锁。调用者现在拥有该锁，应调用 `pthread_mutex_consistent()` 使其一致，或解锁并不再使用。
- `ENOTRECOVERABLE` 健壮互斥锁处于不可恢复状态，无法再使用。

**注意**：

- 持有锁的线程应尽快释放锁，避免其他线程长时间等待。
- 避免在持有锁时调用可能阻塞的函数（如 I/O 操作），这可能导致性能问题。
- 避免嵌套锁定多个互斥锁，这可能导致死锁。如果必须，应保持固定的加锁顺序。
- 锁定互斥锁后，应使用 `try-finally` 模式或清理处理程序确保锁始终被释放。
- 如果线程被取消，应通过清理处理程序（`pthread_cleanup_push/pop`）确保锁被释放。
- 优先级反转问题：如果启用优先级继承协议，低优先级线程持有锁时，其优先级临时提升到等待线程的最高优先级。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutex_trylock

```c
int pthread_mutex_trylock(pthread_mutex_t *mutex);
```

尝试锁定互斥锁（非阻塞）。如果互斥锁当前可用，函数获得锁并立即返回成功。如果互斥锁已被锁定，函数立即返回 `EBUSY`，不会阻塞等待。

这是 `pthread_mutex_lock()` 的非阻塞版本，适用于不希望等待锁的场景，如轮询、避免死锁等。

**参数**：

- `mutex` 指向要尝试锁定的互斥锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EBUSY` 互斥锁已被锁定，无法获取。这不是真正的错误，只是表示锁当前不可用。
- `EINVAL` 互斥锁未正确初始化。
- `EDEADLK` 互斥锁类型为 `PTHREAD_MUTEX_ERRORCHECK`，且当前线程已持有该锁。
- `EOWNERDEAD` 健壮互斥锁的前一个持有者终止时未释放锁。
- `ENOTRECOVERABLE` 健壮互斥锁处于不可恢复状态。

**注意**：

- 如果返回 `EBUSY`，调用者可以选择稍后重试或执行其他操作。
- 对于递归互斥锁，如果当前线程已持有锁，`pthread_mutex_trylock()` 会成功并递增锁计数。
- 常用于避免死锁的场景：尝试获取多个锁时，如果无法获取某个锁，可以释放已持有的锁并重试。
- 不应在循环中持续调用 `pthread_mutex_trylock()`（忙等待），这会浪费 CPU 资源。
- 适用于实现非阻塞算法或超时机制。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutex_timedlock

```c
int pthread_mutex_timedlock(pthread_mutex_t *mutex, const struct timespec *abstime);
```

带超时的锁定互斥锁。如果互斥锁不能立即获取，阻塞等待直到锁可用或超时。

**参数**：

- `mutex` 指向要锁定的互斥锁。不能为 `NULL`。
- `abstime` 绝对超时时间（基于 `CLOCK_REALTIME`）。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ETIMEDOUT` 在超时时间内未能获取锁。
- `EINVAL` `mutex` 为 `NULL` 或未正确初始化。
- `EDEADLK` 互斥锁类型为 `PTHREAD_MUTEX_ERRORCHECK`，且当前线程已持有该锁。

**注意**：

- 对于递归互斥锁，如果当前线程已持有锁，会成功并递增锁计数，不受超时影响。
- 超时时间是绝对时间，不是相对时间。应基于 `clock_gettime(CLOCK_REALTIME, ...)` 计算。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutex_unlock

```c
int pthread_mutex_unlock(pthread_mutex_t *mutex);
```

解锁互斥锁，使其可供其他等待的线程获取。只有持有锁的线程才能解锁，否则行为取决于互斥锁类型。

对于递归互斥锁，每次 `pthread_mutex_unlock()` 调用递减锁计数，当计数降到零时锁才真正被释放。

**参数**：

- `mutex` 指向要解锁的互斥锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EPERM` 当前线程不拥有该互斥锁。对于 `PTHREAD_MUTEX_ERRORCHECK` 类型，尝试解锁未持有的锁会返回此错误。对于 `PTHREAD_MUTEX_NORMAL` 类型，这是未定义行为。
- `EINVAL` 互斥锁未正确初始化或已被销毁。

**注意**：

- 必须由锁定互斥锁的同一线程解锁，不能由其他线程代为解锁。
- 解锁未锁定的互斥锁是未定义行为（对于 NORMAL 类型）或返回错误（对于 ERRORCHECK 类型）。
- 解锁互斥锁后，如果有线程正在等待该锁，其中一个等待线程会被唤醒并获得锁。具体哪个线程被唤醒取决于调度策略。
- 在持有锁期间发生异常或取消时，应确保锁被释放，通过清理处理程序或异常处理机制。
- 解锁操作应尽可能快，避免在锁保护的临界区外调用 unlock。
- 对于优先级继承互斥锁，解锁时会恢复线程的原始优先级。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutex_consistent

```c
int pthread_mutex_consistent(pthread_mutex_t *mutex);
```

将健壮互斥锁标记为一致状态。当健壮互斥锁的前一个持有者终止时未释放锁，`pthread_mutex_lock()` 会返回 `EOWNERDEAD`，此时新的持有者应调用此函数使互斥锁恢复一致。

**参数**：

- `mutex` 指向处于不一致状态的健壮互斥锁。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `mutex` 为 `NULL`，或互斥锁不是健壮互斥锁，或不处于不一致状态。

**注意**：

- 需要互斥锁属性中设置了 `PTHREAD_MUTEX_ROBUST`。
- 如果不调用此函数而直接解锁，互斥锁将进入不可恢复状态，后续 `pthread_mutex_lock()` 会返回 `ENOTRECOVERABLE`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutex_setprioceiling

```c
int pthread_mutex_setprioceiling(pthread_mutex_t *mutex, int prioceiling, int *old_ceiling);
```

动态修改互斥锁的优先级上限。此函数会先锁定互斥锁，修改优先级上限后再解锁，确保操作的原子性。

**参数**：

- `mutex` 指向互斥锁。
- `prioceiling` 新的优先级上限值。
- `old_ceiling` 如果非 `NULL`，用于存储之前的优先级上限值。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` 参数无效，或未启用 `CONFIG_PRIORITY_PROTECT`。
- `EPERM` 无法锁定互斥锁。

**注意**：

- 需要启用 `CONFIG_PRIORITY_PROTECT` 配置项。未启用时始终返回 `EINVAL`。
- 互斥锁的协议必须为 `PTHREAD_PRIO_PROTECT` 才有意义。
- 此函数内部会执行 lock/unlock 操作，调用时不应持有该互斥锁。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutex_getprioceiling

```c
int pthread_mutex_getprioceiling(const pthread_mutex_t *mutex, int *prioceiling);
```

获取互斥锁当前的优先级上限。

**参数**：

- `mutex` 指向互斥锁。
- `prioceiling` 指向整型变量，用于存储优先级上限值。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` 参数无效，或未启用 `CONFIG_PRIORITY_PROTECT`。

**注意**：

- 需要启用 `CONFIG_PRIORITY_PROTECT` 配置项。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 互斥锁属性


### pthread_mutexattr_init

```c
int pthread_mutexattr_init(pthread_mutexattr_t *attr);
```

初始化互斥锁属性对象为默认值。默认属性：类型 `PTHREAD_MUTEX_NORMAL`，协议 `PTHREAD_PRIO_NONE`，进程私有，非健壮。

**参数**：

- `attr` 指向要初始化的互斥锁属性对象。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_destroy

```c
int pthread_mutexattr_destroy(pthread_mutexattr_t *attr);
```

销毁互斥锁属性对象。

**参数**：

- `attr` 指向要销毁的互斥锁属性对象。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_settype

```c
int pthread_mutexattr_settype(pthread_mutexattr_t *attr, int type);
```

设置互斥锁类型。类型决定了重复加锁和错误检测的行为。

**参数**：

- `attr` 指向互斥锁属性对象。不能为 `NULL`。
- `type` 互斥锁类型：
  - `PTHREAD_MUTEX_NORMAL` 不检测死锁，重复加锁导致死锁（默认）。
  - `PTHREAD_MUTEX_ERRORCHECK` 检测死锁，重复加锁返回 `EDEADLK`。
  - `PTHREAD_MUTEX_RECURSIVE` 允许同一线程多次加锁，需相同次数解锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `type` 不是有效值。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_gettype

```c
int pthread_mutexattr_gettype(const pthread_mutexattr_t *attr, int *type);
```

获取互斥锁类型。

**参数**：

- `attr` 指向互斥锁属性对象。不能为 `NULL`。
- `type` 指向整型变量，用于存储互斥锁类型。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `type` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_setpshared

```c
int pthread_mutexattr_setpshared(pthread_mutexattr_t *attr, int pshared);
```

设置互斥锁属性对象中的进程共享属性。

**参数**：

- `attr` 指向互斥锁属性对象。不能为 `NULL`。
- `pshared` 进程共享属性值：
  - `PTHREAD_PROCESS_PRIVATE`（0）进程私有（默认）。
  - `PTHREAD_PROCESS_SHARED`（1）进程间共享。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `pshared` 不是 0 或 1。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_getpshared

```c
int pthread_mutexattr_getpshared(const pthread_mutexattr_t *attr, int *pshared);
```

获取互斥锁属性对象中的进程共享属性。

**参数**：

- `attr` 指向互斥锁属性对象。不能为 `NULL`。
- `pshared` 指向整型变量，用于存储进程共享属性值。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `pshared` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_setprotocol

```c
int pthread_mutexattr_setprotocol(pthread_mutexattr_t *attr, int protocol);
```

设置互斥锁优先级协议。协议决定了持有锁的线程如何处理优先级反转问题。

**参数**：

- `attr` 指向互斥锁属性对象。不能为 `NULL`。
- `protocol` 优先级协议：
  - `PTHREAD_PRIO_NONE` 不使用优先级协议（默认）。
  - `PTHREAD_PRIO_INHERIT` 优先级继承，持有锁的低优先级线程临时提升到等待线程的最高优先级（需 `CONFIG_PRIORITY_INHERITANCE`）。
  - `PTHREAD_PRIO_PROTECT` 优先级上限保护（需 `CONFIG_PRIORITY_PROTECT`）。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `protocol` 不是有效值或不受支持。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_getprotocol

```c
int pthread_mutexattr_getprotocol(const pthread_mutexattr_t *attr, int *protocol);
```

获取互斥锁优先级协议。

**参数**：

- `attr` 指向互斥锁属性对象。不能为 `NULL`。
- `protocol` 指向整型变量，用于存储协议值。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `protocol` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_setrobust

```c
int pthread_mutexattr_setrobust(pthread_mutexattr_t *attr, int robust);
```

设置互斥锁健壮性属性。健壮互斥锁在持有者异常终止时不会永久锁死。

**参数**：

- `attr` 指向互斥锁属性对象。不能为 `NULL`。
- `robust` 健壮性属性：
  - `PTHREAD_MUTEX_STALLED` 非健壮（默认），持有者终止后锁永久不可用。
  - `PTHREAD_MUTEX_ROBUST` 健壮，持有者终止后下一个加锁者收到 `EOWNERDEAD`，可通过 `pthread_mutex_consistent()` 恢复。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `robust` 不是有效值。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_getrobust

```c
int pthread_mutexattr_getrobust(const pthread_mutexattr_t *attr, int *robust);
```

获取互斥锁健壮性属性。

**参数**：

- `attr` 指向互斥锁属性对象。不能为 `NULL`。
- `robust` 指向整型变量，用于存储健壮性属性。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `robust` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_setprioceiling

```c
int pthread_mutexattr_setprioceiling(pthread_mutexattr_t *attr, int prioceiling);
```

设置互斥锁属性对象中的优先级上限。当互斥锁协议为 `PTHREAD_PRIO_PROTECT` 时，持有锁的线程优先级会被提升到此上限值，以避免优先级反转。

**参数**：

- `attr` 指向互斥锁属性对象。不能为 `NULL`。
- `prioceiling` 优先级上限值，必须在 `sched_get_priority_min(SCHED_FIFO)` 和 `sched_get_priority_max(SCHED_FIFO)` 之间。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `prioceiling` 超出有效优先级范围。

**注意**：

- 需要启用 `CONFIG_PRIORITY_PROTECT` 配置项。未启用时，此函数始终返回 `EINVAL`。
- 应与 `pthread_mutexattr_setprotocol(attr, PTHREAD_PRIO_PROTECT)` 配合使用。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_mutexattr_getprioceiling

```c
int pthread_mutexattr_getprioceiling(const pthread_mutexattr_t *attr, int *prioceiling);
```

获取互斥锁属性对象中的优先级上限。

**参数**：

- `attr` 指向互斥锁属性对象。不能为 `NULL`。
- `prioceiling` 指向整型变量，用于存储优先级上限值。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `prioceiling` 为 `NULL`，或未启用 `CONFIG_PRIORITY_PROTECT`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 条件变量


### pthread_cond_init

```c
int pthread_cond_init(pthread_cond_t *cond, const pthread_condattr_t *attr);
```

初始化条件变量。也可使用 `PTHREAD_COND_INITIALIZER` 静态初始化。

**参数**：

- `cond` 指向要初始化的条件变量。不能为 `NULL`。
- `attr` 条件变量属性。如果为 `NULL`，使用默认属性（`CLOCK_REALTIME`，进程私有）。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `cond` 为 `NULL`。
- `ENOMEM` 内存不足。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_cond_destroy

```c
int pthread_cond_destroy(pthread_cond_t *cond);
```

销毁条件变量。

**参数**：

- `cond` 指向要销毁的条件变量。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `cond` 为 `NULL` 或未正确初始化。
- `EBUSY` 有线程正在等待该条件变量。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_cond_wait

```c
int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex);
```

等待条件变量被通知。此函数原子性地释放互斥锁并阻塞在条件变量上。当条件变量被 `pthread_cond_signal()` 或 `pthread_cond_broadcast()` 通知时，线程被唤醒，重新获取互斥锁，然后返回。

条件变量通常用于实现生产者-消费者模式或其他需要线程间协调的场景。典型用法：

```c
pthread_mutex_lock(&mutex);
while (!condition) {
    pthread_cond_wait(&cond, &mutex);
}
// 条件满足，处理数据
pthread_mutex_unlock(&mutex);
```

**参数**：

- `cond` 指向条件变量。
- `mutex` 指向关联的互斥锁。调用前必须已被当前线程锁定。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `cond` 或 `mutex` 未正确初始化，或使用了不同的互斥锁。
- `EPERM` 调用线程未持有互斥锁。

**注意**：

- 调用前必须持有关联的互斥锁，否则行为未定义。
- 函数返回时，互斥锁已重新被锁定，即使发生错误。
- 由于虚假唤醒的可能性，必须在循环中检查条件：`while (!condition) pthread_cond_wait(...)`。虚假唤醒是指线程在没有信号通知的情况下被唤醒。
- 条件变量本身不保存状态，它只是一个同步原语。实际条件（布尔表达式）由应用程序维护，通常通过共享变量表示。
- 等待时互斥锁被原子性地释放，避免了释放锁和阻塞之间的竞态条件。
- 如果线程被取消，互斥锁会被重新锁定，然后清理处理程序被调用。应在清理处理程序中释放锁。
- 多个线程可以同时等待同一个条件变量。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_cond_timedwait

```c
int pthread_cond_timedwait(pthread_cond_t *cond, pthread_mutex_t *mutex,
                           const struct timespec *abstime);
```

带超时的等待条件变量。行为与 `pthread_cond_wait()` 相同，但在超时后自动返回。

**参数**：

- `cond` 指向条件变量。
- `mutex` 指向关联的互斥锁，调用前必须已锁定。
- `abstime` 绝对超时时间。时钟源取决于条件变量属性中的时钟设置（默认 `CLOCK_REALTIME`）。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ETIMEDOUT` 在超时时间内未收到通知。
- `EINVAL` 参数无效。

**注意**：

- 即使超时返回，互斥锁也会被重新锁定。
- 仍需在循环中检查条件，因为可能存在虚假唤醒。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_cond_clockwait

```c
int pthread_cond_clockwait(pthread_cond_t *cond, pthread_mutex_t *mutex,
                           clockid_t clockid, const struct timespec *abstime);
```

使用指定时钟等待条件变量。允许在等待时直接指定时钟源，而不依赖属性对象中的设置。

**参数**：

- `cond` 指向条件变量。
- `mutex` 指向关联的互斥锁，调用前必须已锁定。
- `clockid` 时钟 ID，如 `CLOCK_REALTIME` 或 `CLOCK_MONOTONIC`。
- `abstime` 基于指定时钟的绝对超时时间。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ETIMEDOUT` 在超时时间内未收到通知。
- `EINVAL` 参数无效。

**POSIX 兼容性**：兼容扩展接口。


### pthread_cond_signal

```c
int pthread_cond_signal(pthread_cond_t *cond);
```

唤醒至少一个正在等待条件变量的线程。如果有多个线程在等待，调度策略决定哪个线程被唤醒。如果没有线程在等待，此调用不起作用（信号丢失）。

与 `pthread_cond_broadcast()` 不同，`pthread_cond_signal()` 只唤醒一个线程，适用于只有一个线程能够处理条件的场景，可以避免不必要的线程唤醒和上下文切换。

**参数**：

- `cond` 指向要通知的条件变量。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `cond` 未正确初始化。

**注意**：

- 调用 `pthread_cond_signal()` 时不需要持有关联的互斥锁，但通常建议在持有锁时调用，以避免竞态条件。
- 被唤醒的线程不会立即执行，它会先尝试重新获取互斥锁。因此在调用 signal 后立即释放锁是一个好的做法。
- 如果在修改条件后不持有锁就调用 signal，可能导致"唤醒丢失"问题：等待线程可能在检查条件和调用 wait 之间被抢占。
- 典型模式：
  ```c
  pthread_mutex_lock(&mutex);
  // 修改共享状态，使条件成立
  condition = true;
  pthread_cond_signal(&cond);
  pthread_mutex_unlock(&mutex);
  ```
- 如果条件可能满足多个等待线程的需求，应使用 `pthread_cond_broadcast()`。
- POSIX 不保证信号的公平性，可能出现线程饥饿。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_cond_broadcast

```c
int pthread_cond_broadcast(pthread_cond_t *cond);
```

唤醒所有正在等待条件变量的线程。所有等待线程被唤醒后，会竞争重新获取关联的互斥锁。如果没有线程在等待，此调用不起作用。

与 `pthread_cond_signal()` 不同，broadcast 唤醒所有等待线程，适用于条件变化可能影响多个线程的场景，或者不确定哪个线程应该被唤醒时。

**参数**：

- `cond` 指向要广播的条件变量。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `cond` 未正确初始化。

**注意**：

- 类似 `pthread_cond_signal()`，调用时通常应持有关联的互斥锁。
- 所有被唤醒的线程会串行竞争互斥锁，一次只有一个线程能获得锁并继续执行。
- 使用 broadcast 可能导致"惊群效应"（thundering herd）：多个线程被唤醒但只有少数能真正处理条件，其他线程发现条件不满足后又回到等待状态，造成不必要的上下文切换。
- 适用场景：
  - 条件变化影响所有等待线程（如资源状态变化、系统关闭信号）
  - 不确定哪个线程应该处理条件
  - 需要所有线程重新评估其等待条件
- 典型模式：
  ```c
  pthread_mutex_lock(&mutex);
  // 修改影响所有等待线程的共享状态
  shutdown = true;
  pthread_cond_broadcast(&cond);
  pthread_mutex_unlock(&mutex);
  ```
- 如果只需要唤醒一个线程，优先使用 `pthread_cond_signal()` 以提高效率。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 条件变量属性


### pthread_condattr_init

```c
int pthread_condattr_init(pthread_condattr_t *attr);
```

初始化条件变量属性对象为默认值。初始化后的属性对象包含以下默认值：

- 进程共享属性：`PTHREAD_PROCESS_PRIVATE`（进程私有）
- 时钟属性：`CLOCK_REALTIME`（系统实时时钟）

属性对象用于在调用 `pthread_cond_init()` 时指定条件变量的行为特性。同一个属性对象可以用于初始化多个条件变量。

**参数**：

- `attr` 指向要初始化的条件变量属性对象。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`。

**注意**：

- 使用完毕后应调用 `pthread_condattr_destroy()` 销毁属性对象。
- 属性对象的修改不影响已使用该对象创建的条件变量。
- 如果需要使用 `CLOCK_MONOTONIC` 作为超时时钟（避免系统时间调整的影响），应在初始化后调用 `pthread_condattr_setclock()` 修改时钟属性。
- 在 openvela 中，属性对象是简单的结构体（包含 `pshared` 和 `clockid` 两个字段），不涉及动态内存分配。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_condattr_destroy

```c
int pthread_condattr_destroy(pthread_condattr_t *attr);
```

销毁条件变量属性对象，释放其占用的资源。销毁后的属性对象不能再使用，除非重新调用 `pthread_condattr_init()` 初始化。

**参数**：

- `attr` 指向要销毁的条件变量属性对象。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL` 或不是有效的属性对象。

**注意**：

- 销毁属性对象不影响已使用该对象创建的条件变量。
- 在 openvela 中，属性对象不涉及动态内存分配，此函数主要用于 POSIX 兼容性。
- 应始终配对调用 `pthread_condattr_init()` 和 `pthread_condattr_destroy()`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_condattr_getpshared

```c
int pthread_condattr_getpshared(const pthread_condattr_t *attr, int *pshared);
```

获取条件变量属性对象中的进程共享属性。进程共享属性决定了条件变量是否可以被多个进程中的线程访问。

**参数**：

- `attr` 指向条件变量属性对象。不能为 `NULL`。
- `pshared` 指向整型变量的指针，用于存储当前的进程共享属性值。不能为 `NULL`。返回值为以下之一：
  - `PTHREAD_PROCESS_PRIVATE` 条件变量只能被同一进程内的线程使用（默认值）。
  - `PTHREAD_PROCESS_SHARED` 条件变量可以被多个进程中的线程使用，前提是条件变量分配在共享内存中。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `pshared` 为 `NULL`。

**注意**：

- 在 openvela 中，由于 RTOS 的内存模型，`PTHREAD_PROCESS_SHARED` 的行为可能与 Linux 等系统不同。
- 默认值为 `PTHREAD_PROCESS_PRIVATE`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_condattr_setpshared

```c
int pthread_condattr_setpshared(pthread_condattr_t *attr, int pshared);
```

设置条件变量属性对象中的进程共享属性。该属性决定条件变量是否可以被不同进程中的线程操作。

如果设置为 `PTHREAD_PROCESS_SHARED`，任何能够访问条件变量所在内存的线程都可以操作该条件变量。如果设置为 `PTHREAD_PROCESS_PRIVATE`，只有与初始化条件变量的线程在同一进程内的线程才能操作。不同进程的线程尝试操作私有条件变量的行为是未定义的。

**参数**：

- `attr` 指向条件变量属性对象。不能为 `NULL`。
- `pshared` 进程共享属性值，必须为以下之一：
  - `PTHREAD_PROCESS_PRIVATE` 进程私有（默认）。
  - `PTHREAD_PROCESS_SHARED` 进程间共享。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `pshared` 不是 `PTHREAD_PROCESS_SHARED` 或 `PTHREAD_PROCESS_PRIVATE`。

**注意**：

- 使用 `PTHREAD_PROCESS_SHARED` 时，条件变量必须分配在所有相关进程都能访问的共享内存区域中。
- 与条件变量关联的互斥锁也应设置为进程共享。
- 修改属性对象不影响已创建的条件变量。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_condattr_getclock

```c
int pthread_condattr_getclock(const pthread_condattr_t *attr, clockid_t *clock_id);
```

获取条件变量属性对象中的时钟属性。时钟属性决定了 `pthread_cond_timedwait()` 使用哪个时钟来计算超时时间。

**参数**：

- `attr` 指向条件变量属性对象。不能为 `NULL`。
- `clock_id` 指向 `clockid_t` 变量的指针，用于存储当前的时钟属性值。返回值为以下之一：
  - `CLOCK_REALTIME` 系统实时时钟（默认值）。受系统时间调整（如 NTP）影响。
  - `CLOCK_MONOTONIC` 单调递增时钟。不受系统时间调整影响。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`。

**注意**：

- 默认时钟为 `CLOCK_REALTIME`。
- 如果应用程序对超时精度有要求，或系统时间可能被调整，建议使用 `CLOCK_MONOTONIC`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_condattr_setclock

```c
int pthread_condattr_setclock(pthread_condattr_t *attr, clockid_t clock_id);
```

设置条件变量属性对象中的时钟属性。该属性指定 `pthread_cond_timedwait()` 用于计算超时的时钟源。

选择合适的时钟对于超时行为至关重要：
- `CLOCK_REALTIME`：使用系统实时时钟，超时时间是绝对时间点。如果系统时间被向前调整，可能导致提前超时；向后调整则可能导致超时延迟。
- `CLOCK_MONOTONIC`：使用单调递增时钟，不受系统时间调整影响，适合需要精确超时控制的场景。

**参数**：

- `attr` 指向条件变量属性对象。不能为 `NULL`。
- `clock_id` 时钟 ID，必须为以下之一：
  - `CLOCK_REALTIME` 系统实时时钟（默认）。
  - `CLOCK_MONOTONIC` 单调递增时钟。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `clock_id` 不是 `CLOCK_REALTIME` 或 `CLOCK_MONOTONIC`。

**注意**：

- 在 openvela 中，仅支持 `CLOCK_REALTIME` 和 `CLOCK_MONOTONIC` 两种时钟，传入其他时钟 ID（如 `CLOCK_PROCESS_CPUTIME_ID`）会返回 `EINVAL`。
- 修改时钟属性不影响已创建的条件变量，仅影响后续使用该属性对象创建的条件变量。
- 如果使用 `CLOCK_MONOTONIC`，传递给 `pthread_cond_timedwait()` 的 `abstime` 应基于 `clock_gettime(CLOCK_MONOTONIC, ...)` 获取的时间计算。
- 也可以使用 `pthread_cond_clockwait()` 在等待时直接指定时钟，而不依赖属性对象中的设置。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 读写锁


### pthread_rwlock_init

```c
int pthread_rwlock_init(pthread_rwlock_t *rwlock, const pthread_rwlockattr_t *attr);
```

初始化读写锁。读写锁允许多个线程同时持有读锁，但写锁是排他的。

**参数**：

- `rwlock` 指向要初始化的读写锁。不能为 `NULL`。
- `attr` 读写锁属性。如果为 `NULL`，使用默认属性。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `rwlock` 为 `NULL`。
- `ENOMEM` 内存不足。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlock_destroy

```c
int pthread_rwlock_destroy(pthread_rwlock_t *rwlock);
```

销毁读写锁。

**参数**：

- `rwlock` 指向要销毁的读写锁。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `rwlock` 为 `NULL`。
- `EBUSY` 读写锁当前被锁定。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlock_rdlock

```c
int pthread_rwlock_rdlock(pthread_rwlock_t *rwlock);
```

获取读锁。如果当前没有写锁被持有，立即获取成功；否则阻塞等待。多个线程可同时持有读锁。

**参数**：

- `rwlock` 指向读写锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `rwlock` 未正确初始化。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlock_tryrdlock

```c
int pthread_rwlock_tryrdlock(pthread_rwlock_t *rwlock);
```

尝试获取读锁（非阻塞）。

**参数**：

- `rwlock` 指向读写锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EBUSY` 有写锁被持有，无法获取读锁。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlock_timedrdlock

```c
int pthread_rwlock_timedrdlock(pthread_rwlock_t *rwlock, const struct timespec *abstime);
```

带超时的获取读锁。如果读锁不能立即获取，阻塞等待直到锁可用或超时。超时基于 `CLOCK_REALTIME`。

**参数**：

- `rwlock` 指向读写锁。
- `abstime` 绝对超时时间（基于 `CLOCK_REALTIME`）。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ETIMEDOUT` 在超时时间内未能获取读锁。
- `EBUSY` 读锁不可用。
- `EINVAL` 参数无效。

**注意**：

- 内部调用 `pthread_rwlock_clockrdlock()` 并使用 `CLOCK_REALTIME` 作为时钟源。
- 如果需要使用 `CLOCK_MONOTONIC`，请使用 `pthread_rwlock_clockrdlock()`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlock_clockrdlock

```c
int pthread_rwlock_clockrdlock(pthread_rwlock_t *rwlock, clockid_t clockid,
                               const struct timespec *abstime);
```

使用指定时钟带超时获取读锁。

**参数**：

- `rwlock` 指向读写锁。
- `clockid` 时钟 ID，如 `CLOCK_REALTIME` 或 `CLOCK_MONOTONIC`。
- `abstime` 基于指定时钟的绝对超时时间。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ETIMEDOUT` 在超时时间内未能获取读锁。
- `EINVAL` 参数无效。

**POSIX 兼容性**：兼容扩展接口。


### pthread_rwlock_wrlock

```c
int pthread_rwlock_wrlock(pthread_rwlock_t *rwlock);
```

获取写锁。写锁是排他的，必须等待所有读锁和写锁释放后才能获取。

**参数**：

- `rwlock` 指向读写锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `rwlock` 未正确初始化。
- `EAGAIN` 写者数量已达上限。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlock_trywrlock

```c
int pthread_rwlock_trywrlock(pthread_rwlock_t *rwlock);
```

尝试获取写锁（非阻塞）。

**参数**：

- `rwlock` 指向读写锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EBUSY` 有读锁或写锁被持有，无法获取写锁。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlock_timedwrlock

```c
int pthread_rwlock_timedwrlock(pthread_rwlock_t *rwlock, const struct timespec *abstime);
```

带超时的获取写锁。如果写锁不能立即获取，阻塞等待直到锁可用或超时。超时基于 `CLOCK_REALTIME`。

**参数**：

- `rwlock` 指向读写锁。
- `abstime` 绝对超时时间（基于 `CLOCK_REALTIME`）。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ETIMEDOUT` 在超时时间内未能获取写锁。
- `EAGAIN` 写者数量已达上限。
- `EINVAL` 参数无效。

**注意**：

- 内部调用 `pthread_rwlock_clockwrlock()` 并使用 `CLOCK_REALTIME` 作为时钟源。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlock_clockwrlock

```c
int pthread_rwlock_clockwrlock(pthread_rwlock_t *rwlock, clockid_t clockid,
                               const struct timespec *abstime);
```

使用指定时钟带超时获取写锁。

**参数**：

- `rwlock` 指向读写锁。
- `clockid` 时钟 ID，如 `CLOCK_REALTIME` 或 `CLOCK_MONOTONIC`。
- `abstime` 基于指定时钟的绝对超时时间。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ETIMEDOUT` 在超时时间内未能获取写锁。
- `EAGAIN` 写者数量已达上限。
- `EINVAL` 参数无效。

**POSIX 兼容性**：兼容扩展接口。


### pthread_rwlock_unlock

```c
int pthread_rwlock_unlock(pthread_rwlock_t *rwlock);
```

释放读写锁（读锁或写锁）。

**参数**：

- `rwlock` 指向读写锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `rwlock` 未正确初始化。
- `EPERM` 当前线程未持有该锁。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 读写锁属性


### pthread_rwlockattr_init

```c
int pthread_rwlockattr_init(pthread_rwlockattr_t *attr);
```

初始化读写锁属性对象为默认值。默认进程共享属性为 `PTHREAD_PROCESS_PRIVATE`。

**参数**：

- `attr` 指向要初始化的读写锁属性对象。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlockattr_destroy

```c
int pthread_rwlockattr_destroy(pthread_rwlockattr_t *attr);
```

销毁读写锁属性对象。

**参数**：

- `attr` 指向要销毁的读写锁属性对象。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlockattr_setpshared

```c
int pthread_rwlockattr_setpshared(pthread_rwlockattr_t *attr, int pshared);
```

设置读写锁属性对象中的进程共享属性。

**参数**：

- `attr` 指向读写锁属性对象。不能为 `NULL`。
- `pshared` 进程共享属性值：`PTHREAD_PROCESS_PRIVATE` 或 `PTHREAD_PROCESS_SHARED`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `pshared` 不是有效值。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_rwlockattr_getpshared

```c
int pthread_rwlockattr_getpshared(const pthread_rwlockattr_t *attr, int *pshared);
```

获取读写锁属性对象中的进程共享属性。

**参数**：

- `attr` 指向读写锁属性对象。不能为 `NULL`。
- `pshared` 指向整型变量，用于存储进程共享属性值。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `pshared` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 屏障


### pthread_barrier_init

```c
int pthread_barrier_init(pthread_barrier_t *barrier,
                         const pthread_barrierattr_t *attr, unsigned int count);
```

初始化屏障。屏障用于同步多个线程，所有线程到达屏障后才能继续执行。

**参数**：

- `barrier` 指向要初始化的屏障。不能为 `NULL`。
- `attr` 屏障属性。如果为 `NULL`，使用默认属性。
- `count` 需要到达屏障的线程数。必须大于 0。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `barrier` 为 `NULL`，或 `count` 为 0。
- `ENOMEM` 内存不足。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_barrier_destroy

```c
int pthread_barrier_destroy(pthread_barrier_t *barrier);
```

销毁屏障。

**参数**：

- `barrier` 指向要销毁的屏障。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `barrier` 为 `NULL`。
- `EBUSY` 有线程正在等待该屏障。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_barrier_wait

```c
int pthread_barrier_wait(pthread_barrier_t *barrier);
```

在屏障处等待。当所有线程（数量由 `pthread_barrier_init` 的 `count` 参数指定）都调用此函数后，所有线程同时被释放继续执行。

**参数**：

- `barrier` 指向屏障。

**返回值**：

其中一个线程返回 `PTHREAD_BARRIER_SERIAL_THREAD`（该线程可用于执行清理工作），其他线程返回 0。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 屏障属性


### pthread_barrierattr_init

```c
int pthread_barrierattr_init(pthread_barrierattr_t *attr);
```

初始化屏障属性对象为默认值。默认进程共享属性为 `PTHREAD_PROCESS_PRIVATE`。

**参数**：

- `attr` 指向要初始化的屏障属性对象。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_barrierattr_destroy

```c
int pthread_barrierattr_destroy(pthread_barrierattr_t *attr);
```

销毁屏障属性对象。

**参数**：

- `attr` 指向要销毁的屏障属性对象。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_barrierattr_setpshared

```c
int pthread_barrierattr_setpshared(pthread_barrierattr_t *attr, int pshared);
```

设置屏障属性对象中的进程共享属性。

**参数**：

- `attr` 指向屏障属性对象。不能为 `NULL`。
- `pshared` 进程共享属性值：`PTHREAD_PROCESS_PRIVATE` 或 `PTHREAD_PROCESS_SHARED`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 为 `NULL`，或 `pshared` 不是有效值。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_barrierattr_getpshared

```c
int pthread_barrierattr_getpshared(const pthread_barrierattr_t *attr, int *pshared);
```

获取屏障属性对象中的进程共享属性。

**参数**：

- `attr` 指向屏障属性对象。不能为 `NULL`。
- `pshared` 指向整型变量，用于存储进程共享属性值。不能为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `attr` 或 `pshared` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 自旋锁


### pthread_spin_init

```c
int pthread_spin_init(pthread_spinlock_t *lock, int pshared);
```

初始化自旋锁。自旋锁使用忙等待方式获取锁，适用于锁持有时间极短的场景。

**参数**：

- `lock` 指向要初始化的自旋锁。不能为 `NULL`。
- `pshared` 共享属性：`PTHREAD_PROCESS_PRIVATE` 或 `PTHREAD_PROCESS_SHARED`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `lock` 为 `NULL`。

**注意**：

- 自旋锁不应在持有时间较长的场景使用，会浪费 CPU 资源。
- 持有自旋锁时不应调用可能阻塞的函数。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_spin_destroy

```c
int pthread_spin_destroy(pthread_spinlock_t *lock);
```

销毁自旋锁。

**参数**：

- `lock` 指向要销毁的自旋锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `lock` 未正确初始化。
- `EBUSY` 自旋锁当前被锁定。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_spin_lock

```c
int pthread_spin_lock(pthread_spinlock_t *lock);
```

获取自旋锁。如果锁已被持有，调用线程忙等待直到锁可用。

**参数**：

- `lock` 指向自旋锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `lock` 未正确初始化。
- `EDEADLK` 当前线程已持有该锁（实现相关）。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_spin_trylock

```c
int pthread_spin_trylock(pthread_spinlock_t *lock);
```

尝试获取自旋锁（非阻塞）。

**参数**：

- `lock` 指向自旋锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EBUSY` 自旋锁已被锁定。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_spin_unlock

```c
int pthread_spin_unlock(pthread_spinlock_t *lock);
```

释放自旋锁。

**参数**：

- `lock` 指向自旋锁。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `lock` 未正确初始化。
- `EPERM` 当前线程未持有该锁。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 线程特定数据


### pthread_key_create

```c
int pthread_key_create(pthread_key_t *key, void (*destructor)(void *));
```

创建线程特定数据键。每个线程可以通过该键存储和获取自己的私有数据。

**参数**：

- `key` 指向 `pthread_key_t` 变量，用于存储创建的键。不能为 `NULL`。
- `destructor` 析构函数，线程退出时对非 `NULL` 的数据自动调用。可以为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EAGAIN` 已达系统键数量上限（`PTHREAD_KEYS_MAX`）。
- `ENOMEM` 内存不足。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_key_delete

```c
int pthread_key_delete(pthread_key_t key);
```

删除线程特定数据键。不会调用析构函数，也不会释放各线程关联的数据。

**参数**：

- `key` 要删除的键。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `key` 无效。

**注意**：

- 删除键后，各线程应自行释放关联的数据，否则会导致内存泄漏。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_setspecific

```c
int pthread_setspecific(pthread_key_t key, const void *value);
```

设置调用线程的线程特定数据。

**参数**：

- `key` 数据键，必须是通过 `pthread_key_create()` 创建的有效键。
- `value` 要存储的值。可以为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码：

- `EINVAL` `key` 无效。
- `ENOMEM` 内存不足。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_getspecific

```c
void *pthread_getspecific(pthread_key_t key);
```

获取调用线程的线程特定数据。

**参数**：

- `key` 数据键。

**返回值**：

返回与键关联的值。如果键无效或未设置过值，返回 `NULL`。

**注意**：

- 此函数不返回错误码，无法区分"未设置"和"设置为 NULL"两种情况。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 线程清理


### pthread_cleanup_push

```c
void pthread_cleanup_push(void (*routine)(void *), void *arg);
```

注册线程清理函数。清理函数在线程被取消、调用 `pthread_exit()` 或调用 `pthread_cleanup_pop(1)` 时执行。

**参数**：

- `routine` 清理函数。不能为 `NULL`。
- `arg` 传递给清理函数的参数。

**返回值**：

无返回值。

**注意**：

- 必须与 `pthread_cleanup_pop()` 配对使用，且在同一函数作用域内。
- 清理函数按注册顺序的逆序执行（后注册先执行）。
- 常用于确保互斥锁在线程取消时被释放。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


### pthread_cleanup_pop

```c
void pthread_cleanup_pop(int execute);
```

移除最近注册的清理函数，并可选择执行它。

**参数**：

- `execute` 如果非零，移除并执行清理函数；如果为零，仅移除不执行。

**返回值**：

无返回值。

**注意**：

- 必须与 `pthread_cleanup_push()` 配对使用。
- 即使 `execute` 为 0，清理函数也会从栈中移除。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。


## 扩展接口


### pthread_setname_np

```c
int pthread_setname_np(pthread_t thread, const char *name);
```

设置线程名称。线程名称用于调试和日志，可通过 `ps` 命令或调试器查看。

**参数**：

- `thread` 线程 ID。
- `name` 线程名称字符串。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ESRCH` 找不到指定线程。
- `EINVAL` `name` 为 `NULL`。

**POSIX 兼容性**：兼容 Linux 扩展接口。


### pthread_getname_np

```c
int pthread_getname_np(pthread_t thread, char *name, size_t len);
```

获取线程名称。

**参数**：

- `thread` 线程 ID。
- `name` 用于存储名称的缓冲区。
- `len` 缓冲区大小。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ESRCH` 找不到指定线程。
- `EINVAL` `name` 为 `NULL`。

**POSIX 兼容性**：兼容 Linux 扩展接口。


### pthread_gettid_np

```c
pid_t pthread_gettid_np(pthread_t thread);
```

获取线程的内核线程 ID（`pid_t`）。

**参数**：

- `thread` 线程 ID。

**返回值**：

返回内核线程 ID。

**注意**：

- 在 openvela 中，`pthread_t` 本身就是 `pid_t`，因此此函数直接返回输入值。

**POSIX 兼容性**：兼容扩展接口。


### pthread_getcpuclockid

```c
int pthread_getcpuclockid(pthread_t thread, clockid_t *clockid);
```

获取线程的 CPU 时钟 ID。该时钟测量指定线程消耗的 CPU 时间。

**参数**：

- `thread` 线程 ID。
- `clockid` 指向 `clockid_t` 变量，用于存储时钟 ID。

**返回值**：

成功时返回 0，失败时返回错误码：

- `ESRCH` 找不到指定线程。
- `EINVAL` `clockid` 为 `NULL`。

**POSIX 兼容性**：兼容 `POSIX` 同名接口。
