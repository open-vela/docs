# 进程 线程

openvela 提供 POSIX 兼容的线程（pthread）接口，支持线程创建、同步、属性管理等功能。

## 一、线程 API

- `pthread_create()`
- `pthread_exit()`
- `pthread_join()`
- `pthread_detach()`
- `pthread_cancel()`
- `pthread_setcancelstate()`
- `pthread_setcanceltype()`
- `pthread_testcancel()`
- `pthread_self()`
- `pthread_equal()`
- `pthread_yield()`
- `pthread_once()`
- `pthread_atfork()`

## 二、线程属性 API

- `pthread_attr_init()`
- `pthread_attr_destroy()`
- `pthread_attr_setschedpolicy()`
- `pthread_attr_getschedpolicy()`
- `pthread_attr_setschedparam()`
- `pthread_attr_getschedparam()`
- `pthread_attr_setinheritsched()`
- `pthread_attr_getinheritsched()`
- `pthread_attr_setdetachstate()`
- `pthread_attr_getdetachstate()`
- `pthread_attr_setstacksize()`
- `pthread_attr_getstacksize()`
- `pthread_attr_setstackaddr()`
- `pthread_attr_getstackaddr()`
- `pthread_attr_setstack()`
- `pthread_attr_getstack()`
- `pthread_attr_setguardsize()`
- `pthread_attr_getguardsize()`
- `pthread_attr_setscope()`
- `pthread_attr_getscope()`

## 三、线程调度 API

- `pthread_getschedparam()`
- `pthread_setschedparam()`
- `pthread_setschedprio()`
- `pthread_setaffinity_np()`
- `pthread_getaffinity_np()`
- `pthread_setconcurrency()`
- `pthread_getconcurrency()`

## 四、互斥锁 API

- `pthread_mutex_init()`
- `pthread_mutex_destroy()`
- `pthread_mutex_lock()`
- `pthread_mutex_trylock()`
- `pthread_mutex_timedlock()`
- `pthread_mutex_unlock()`
- `pthread_mutex_consistent()`
- `pthread_mutexattr_init()`
- `pthread_mutexattr_destroy()`
- `pthread_mutexattr_gettype()`
- `pthread_mutexattr_settype()`
- `pthread_mutexattr_getpshared()`
- `pthread_mutexattr_setpshared()`
- `pthread_mutexattr_getprotocol()`
- `pthread_mutexattr_setprotocol()`
- `pthread_mutexattr_getrobust()`
- `pthread_mutexattr_setrobust()`
- `pthread_mutexattr_getprioceiling()`
- `pthread_mutexattr_setprioceiling()`

## 五、条件变量 API

- `pthread_cond_init()`
- `pthread_cond_destroy()`
- `pthread_cond_wait()`
- `pthread_cond_timedwait()`
- `pthread_cond_clockwait()`
- `pthread_cond_signal()`
- `pthread_cond_broadcast()`
- `pthread_condattr_init()`
- `pthread_condattr_destroy()`
- `pthread_condattr_getpshared()`
- `pthread_condattr_setpshared()`
- `pthread_condattr_getclock()`
- `pthread_condattr_setclock()`

## 六、读写锁 API

- `pthread_rwlock_init()`
- `pthread_rwlock_destroy()`
- `pthread_rwlock_rdlock()`
- `pthread_rwlock_tryrdlock()`
- `pthread_rwlock_timedrdlock()`
- `pthread_rwlock_clockrdlock()`
- `pthread_rwlock_wrlock()`
- `pthread_rwlock_trywrlock()`
- `pthread_rwlock_timedwrlock()`
- `pthread_rwlock_clockwrlock()`
- `pthread_rwlock_unlock()`
- `pthread_rwlockattr_init()`
- `pthread_rwlockattr_destroy()`
- `pthread_rwlockattr_getpshared()`
- `pthread_rwlockattr_setpshared()`

## 七、屏障 API

- `pthread_barrier_init()`
- `pthread_barrier_destroy()`
- `pthread_barrier_wait()`
- `pthread_barrierattr_init()`
- `pthread_barrierattr_destroy()`
- `pthread_barrierattr_getpshared()`
- `pthread_barrierattr_setpshared()`

## 八、自旋锁 API

- `pthread_spin_init()`
- `pthread_spin_destroy()`
- `pthread_spin_lock()`
- `pthread_spin_trylock()`
- `pthread_spin_unlock()`

## 九、线程特定数据 API

- `pthread_key_create()`
- `pthread_key_delete()`
- `pthread_setspecific()`
- `pthread_getspecific()`

---

## 1、pthread_create

```c
int pthread_create(pthread_t *thread, const pthread_attr_t *attr,
                   pthread_startroutine_t start_routine, pthread_addr_t arg);
```

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 2、pthread_exit

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

- `value` 线程返回值，这是一个无类型指针，可以传递任何数据的地址。等待此线程的 `pthread_join()` 调用可以获取此值。如果线程被取消，返回值为 `PTHREAD_CANCELED`。

**返回值**：

此函数不返回。调用后，调用线程终止。

**注意**：

- 不要在 `main()` 函数中调用 `pthread_exit()`，这会终止主线程但不终止进程，可能导致其他线程成为孤儿。
- 如果线程已分离，`value` 将被忽略，因为没有线程可以通过 `pthread_join()` 获取返回值。
- 线程终止时，不会自动关闭打开的文件描述符或释放分配的内存，这些资源由整个进程共享。
- 从线程入口函数返回隐式调用 `pthread_exit()`，返回值作为线程的退出值。
- 如果线程持有互斥锁，在调用 `pthread_exit()` 前应释放，否则可能导致死锁。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 3、pthread_join

```c
int pthread_join(pthread_t thread, pthread_addr_t *value);
```

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 4、pthread_detach

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 5、pthread_cancel

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 6、pthread_setcancelstate

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 7、pthread_setcanceltype

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 8、pthread_testcancel

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 9、pthread_self

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 10、pthread_equal

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 11、pthread_yield

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

## 12、pthread_once

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 13、pthread_atfork

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 14、pthread_attr_init

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 15、pthread_attr_destroy

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 16、pthread_attr_setdetachstate

```c
int pthread_attr_setdetachstate(pthread_attr_t *attr, int detachstate);
```

设置线程的分离状态属性。

**参数**：

- `attr` 属性对象。
- `detachstate` 分离状态：`PTHREAD_CREATE_JOINABLE` 或 `PTHREAD_CREATE_DETACHED`。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 17、pthread_attr_getdetachstate

```c
int pthread_attr_getdetachstate(const pthread_attr_t *attr, int *detachstate);
```

获取线程的分离状态属性。

**参数**：

- `attr` 属性对象。
- `detachstate` 返回分离状态。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 18、pthread_attr_setstacksize

```c
int pthread_attr_setstacksize(pthread_attr_t *attr, size_t stacksize);
```

设置线程栈大小。

**参数**：

- `attr` 属性对象。
- `stacksize` 栈大小（字节）。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 19、pthread_attr_getstacksize

```c
int pthread_attr_getstacksize(const pthread_attr_t *attr, size_t *stacksize);
```

获取线程栈大小。

**参数**：

- `attr` 属性对象。
- `stacksize` 返回栈大小。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 20、pthread_attr_setschedpolicy

```c
int pthread_attr_setschedpolicy(pthread_attr_t *attr, int policy);
```

设置线程调度策略。

**参数**：

- `attr` 属性对象。
- `policy` 调度策略：`SCHED_FIFO`、`SCHED_RR` 或 `SCHED_OTHER`。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 21、pthread_attr_getschedpolicy

```c
int pthread_attr_getschedpolicy(const pthread_attr_t *attr, int *policy);
```

获取线程调度策略。

**参数**：

- `attr` 属性对象。
- `policy` 返回调度策略。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 22、pthread_attr_setschedparam

```c
int pthread_attr_setschedparam(pthread_attr_t *attr, const struct sched_param *param);
```

设置线程调度参数。

**参数**：

- `attr` 属性对象。
- `param` 调度参数（包含优先级）。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 23、pthread_attr_getschedparam

```c
int pthread_attr_getschedparam(const pthread_attr_t *attr, struct sched_param *param);
```

获取线程调度参数。

**参数**：

- `attr` 属性对象。
- `param` 返回调度参数。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 24、pthread_attr_setinheritsched

```c
int pthread_attr_setinheritsched(pthread_attr_t *attr, int inheritsched);
```

设置调度属性继承方式。

**参数**：

- `attr` 属性对象。
- `inheritsched` 继承方式：`PTHREAD_INHERIT_SCHED` 或 `PTHREAD_EXPLICIT_SCHED`。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 25、pthread_attr_getinheritsched

```c
int pthread_attr_getinheritsched(const pthread_attr_t *attr, int *inheritsched);
```

获取调度属性继承方式。

**参数**：

- `attr` 属性对象。
- `inheritsched` 返回继承方式。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 26、pthread_getschedparam

```c
int pthread_getschedparam(pthread_t thread, int *policy, struct sched_param *param);
```

获取线程的调度策略和参数。

**参数**：

- `thread` 线程 ID。
- `policy` 返回调度策略。
- `param` 返回调度参数。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 27、pthread_setschedparam

```c
int pthread_setschedparam(pthread_t thread, int policy, const struct sched_param *param);
```

设置线程的调度策略和参数。

**参数**：

- `thread` 线程 ID。
- `policy` 调度策略。
- `param` 调度参数。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 28、pthread_setschedprio

```c
int pthread_setschedprio(pthread_t thread, int prio);
```

设置线程优先级。

**参数**：

- `thread` 线程 ID。
- `prio` 新的优先级。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 29、pthread_mutex_init

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 30、pthread_mutex_destroy

```c
int pthread_mutex_destroy(pthread_mutex_t *mutex);
```

销毁互斥锁。

**参数**：

- `mutex` 要销毁的互斥锁。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 31、pthread_mutex_lock

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 32、pthread_mutex_trylock

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 33、pthread_mutex_timedlock

```c
int pthread_mutex_timedlock(pthread_mutex_t *mutex, const struct timespec *abstime);
```

带超时的加锁互斥锁。

**参数**：

- `mutex` 互斥锁。
- `abstime` 绝对超时时间。

**返回值**：

成功时返回 0，超时返回 `ETIMEDOUT`。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 34、pthread_mutex_unlock

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 35、pthread_mutex_consistent

```c
int pthread_mutex_consistent(pthread_mutex_t *mutex);
```

将健壮互斥锁标记为一致状态。

**参数**：

- `mutex` 互斥锁。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 36、pthread_mutexattr_init

```c
int pthread_mutexattr_init(pthread_mutexattr_t *attr);
```

初始化互斥锁属性对象。

**参数**：

- `attr` 要初始化的属性对象。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 37、pthread_mutexattr_destroy

```c
int pthread_mutexattr_destroy(pthread_mutexattr_t *attr);
```

销毁互斥锁属性对象。

**参数**：

- `attr` 要销毁的属性对象。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 38、pthread_mutexattr_settype

```c
int pthread_mutexattr_settype(pthread_mutexattr_t *attr, int type);
```

设置互斥锁类型。

**参数**：

- `attr` 属性对象。
- `type` 互斥锁类型：`PTHREAD_MUTEX_NORMAL`、`PTHREAD_MUTEX_ERRORCHECK`、`PTHREAD_MUTEX_RECURSIVE`。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 39、pthread_mutexattr_gettype

```c
int pthread_mutexattr_gettype(const pthread_mutexattr_t *attr, int *type);
```

获取互斥锁类型。

**参数**：

- `attr` 属性对象。
- `type` 返回互斥锁类型。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 40、pthread_mutexattr_setprotocol

```c
int pthread_mutexattr_setprotocol(pthread_mutexattr_t *attr, int protocol);
```

设置互斥锁优先级协议。

**参数**：

- `attr` 属性对象。
- `protocol` 协议：`PTHREAD_PRIO_NONE`、`PTHREAD_PRIO_INHERIT`、`PTHREAD_PRIO_PROTECT`。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 41、pthread_mutexattr_getprotocol

```c
int pthread_mutexattr_getprotocol(const pthread_mutexattr_t *attr, int *protocol);
```

获取互斥锁优先级协议。

**参数**：

- `attr` 属性对象。
- `protocol` 返回协议。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 42、pthread_mutexattr_setrobust

```c
int pthread_mutexattr_setrobust(pthread_mutexattr_t *attr, int robust);
```

设置互斥锁健壮性属性。

**参数**：

- `attr` 属性对象。
- `robust` 健壮性：`PTHREAD_MUTEX_STALLED` 或 `PTHREAD_MUTEX_ROBUST`。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 43、pthread_mutexattr_getrobust

```c
int pthread_mutexattr_getrobust(const pthread_mutexattr_t *attr, int *robust);
```

获取互斥锁健壮性属性。

**参数**：

- `attr` 属性对象。
- `robust` 返回健壮性。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 44、pthread_cond_init

```c
int pthread_cond_init(pthread_cond_t *cond, const pthread_condattr_t *attr);
```

初始化条件变量。

**参数**：

- `cond` 要初始化的条件变量。
- `attr` 条件变量属性。如果为 `NULL`，使用默认属性。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 45、pthread_cond_destroy

```c
int pthread_cond_destroy(pthread_cond_t *cond);
```

销毁条件变量。

**参数**：

- `cond` 要销毁的条件变量。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 46、pthread_cond_wait

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 47、pthread_cond_timedwait

```c
int pthread_cond_timedwait(pthread_cond_t *cond, pthread_mutex_t *mutex,
                           const struct timespec *abstime);
```

带超时的等待条件变量。

**参数**：

- `cond` 条件变量。
- `mutex` 关联的互斥锁。
- `abstime` 绝对超时时间。

**返回值**：

成功时返回 0，超时返回 `ETIMEDOUT`。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 48、pthread_cond_clockwait

```c
int pthread_cond_clockwait(pthread_cond_t *cond, pthread_mutex_t *mutex,
                           clockid_t clockid, const struct timespec *abstime);
```

使用指定时钟等待条件变量。

**参数**：

- `cond` 条件变量。
- `mutex` 关联的互斥锁。
- `clockid` 时钟 ID。
- `abstime` 绝对超时时间。

**返回值**：

成功时返回 0，超时返回 `ETIMEDOUT`。

**POSIX 兼容性**：兼容扩展接口。

## 49、pthread_cond_signal

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 50、pthread_cond_broadcast

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

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 51、pthread_rwlock_init

```c
int pthread_rwlock_init(pthread_rwlock_t *rwlock, const pthread_rwlockattr_t *attr);
```

初始化读写锁。

**参数**：

- `rwlock` 要初始化的读写锁。
- `attr` 读写锁属性。如果为 `NULL`，使用默认属性。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 52、pthread_rwlock_destroy

```c
int pthread_rwlock_destroy(pthread_rwlock_t *rwlock);
```

销毁读写锁。

**参数**：

- `rwlock` 要销毁的读写锁。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 53、pthread_rwlock_rdlock

```c
int pthread_rwlock_rdlock(pthread_rwlock_t *rwlock);
```

获取读锁。

**参数**：

- `rwlock` 读写锁。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 54、pthread_rwlock_wrlock

```c
int pthread_rwlock_wrlock(pthread_rwlock_t *rwlock);
```

获取写锁。

**参数**：

- `rwlock` 读写锁。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 55、pthread_rwlock_unlock

```c
int pthread_rwlock_unlock(pthread_rwlock_t *rwlock);
```

释放读写锁。

**参数**：

- `rwlock` 读写锁。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 56、pthread_rwlock_tryrdlock

```c
int pthread_rwlock_tryrdlock(pthread_rwlock_t *rwlock);
```

尝试获取读锁（非阻塞）。

**参数**：

- `rwlock` 读写锁。

**返回值**：

成功时返回 0，如果无法获取返回 `EBUSY`。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 57、pthread_rwlock_trywrlock

```c
int pthread_rwlock_trywrlock(pthread_rwlock_t *rwlock);
```

尝试获取写锁（非阻塞）。

**参数**：

- `rwlock` 读写锁。

**返回值**：

成功时返回 0，如果无法获取返回 `EBUSY`。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 58、pthread_barrier_init

```c
int pthread_barrier_init(pthread_barrier_t *barrier,
                         const pthread_barrierattr_t *attr, unsigned int count);
```

初始化屏障。

**参数**：

- `barrier` 要初始化的屏障。
- `attr` 屏障属性。如果为 `NULL`，使用默认属性。
- `count` 需要等待的线程数。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 59、pthread_barrier_destroy

```c
int pthread_barrier_destroy(pthread_barrier_t *barrier);
```

销毁屏障。

**参数**：

- `barrier` 要销毁的屏障。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 60、pthread_barrier_wait

```c
int pthread_barrier_wait(pthread_barrier_t *barrier);
```

在屏障处等待。

**参数**：

- `barrier` 屏障。

**返回值**：

一个线程返回 `PTHREAD_BARRIER_SERIAL_THREAD`，其他线程返回 0。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 61、pthread_spin_init

```c
int pthread_spin_init(pthread_spinlock_t *lock, int pshared);
```

初始化自旋锁。

**参数**：

- `lock` 要初始化的自旋锁。
- `pshared` 共享属性：`PTHREAD_PROCESS_PRIVATE` 或 `PTHREAD_PROCESS_SHARED`。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 62、pthread_spin_destroy

```c
int pthread_spin_destroy(pthread_spinlock_t *lock);
```

销毁自旋锁。

**参数**：

- `lock` 要销毁的自旋锁。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 63、pthread_spin_lock

```c
int pthread_spin_lock(pthread_spinlock_t *lock);
```

获取自旋锁（忙等待）。

**参数**：

- `lock` 自旋锁。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 64、pthread_spin_trylock

```c
int pthread_spin_trylock(pthread_spinlock_t *lock);
```

尝试获取自旋锁（非阻塞）。

**参数**：

- `lock` 自旋锁。

**返回值**：

成功时返回 0，如果已被锁定返回 `EBUSY`。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 65、pthread_spin_unlock

```c
int pthread_spin_unlock(pthread_spinlock_t *lock);
```

释放自旋锁。

**参数**：

- `lock` 自旋锁。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 66、pthread_key_create

```c
int pthread_key_create(pthread_key_t *key, void (*destructor)(void *));
```

创建线程特定数据键。

**参数**：

- `key` 返回创建的键。
- `destructor` 析构函数，线程退出时自动调用。可以为 `NULL`。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 67、pthread_key_delete

```c
int pthread_key_delete(pthread_key_t key);
```

删除线程特定数据键。

**参数**：

- `key` 要删除的键。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 68、pthread_setspecific

```c
int pthread_setspecific(pthread_key_t key, const void *value);
```

设置线程特定数据。

**参数**：

- `key` 数据键。
- `value` 要存储的值。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 69、pthread_getspecific

```c
void *pthread_getspecific(pthread_key_t key);
```

获取线程特定数据。

**参数**：

- `key` 数据键。

**返回值**：

返回与键关联的值，如果未设置返回 `NULL`。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 70、pthread_setname_np

```c
int pthread_setname_np(pthread_t thread, const char *name);
```

设置线程名称。

**参数**：

- `thread` 线程 ID。
- `name` 线程名称。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：兼容 Linux 扩展接口。

## 71、pthread_getname_np

```c
int pthread_getname_np(pthread_t thread, char *name, size_t len);
```

获取线程名称。

**参数**：

- `thread` 线程 ID。
- `name` 用于存储名称的缓冲区。
- `len` 缓冲区大小。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：兼容 Linux 扩展接口。

## 72、pthread_gettid_np

```c
pid_t pthread_gettid_np(pthread_t thread);
```

获取线程的内核线程 ID。

**参数**：

- `thread` 线程 ID。

**返回值**：

返回内核线程 ID。

**POSIX 兼容性**：兼容扩展接口。

## 73、pthread_getcpuclockid

```c
int pthread_getcpuclockid(pthread_t thread, clockid_t *clockid);
```

获取线程的 CPU 时钟 ID。

**参数**：

- `thread` 线程 ID。
- `clockid` 返回时钟 ID。

**返回值**：

成功时返回 0，失败时返回错误码。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 74、pthread_cleanup_push

```c
void pthread_cleanup_push(void (*routine)(void *), void *arg);
```

注册线程清理函数。

**参数**：

- `routine` 清理函数。
- `arg` 传递给清理函数的参数。

**返回值**：

无返回值。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 75、pthread_cleanup_pop

```c
void pthread_cleanup_pop(int execute);
```

移除最近注册的清理函数。

**参数**：

- `execute` 如果非零，执行清理函数；否则只移除不执行。

**返回值**：

无返回值。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。
