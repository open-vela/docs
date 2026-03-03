# 调度管理

openvela 提供了符合 POSIX 标准的任务调度接口，支持多种调度策略和任务管理功能。调度器负责决定哪个任务在何时运行，是操作系统内核的核心组件之一。

## 一、调度策略概述

openvela 支持以下调度策略：

### 1、SCHED_FIFO（先进先出）
实时调度策略，不使用时间片。任务一旦获得 CPU 就会持续运行，直到：
- 主动让出 CPU（`sched_yield()`）
- 被更高优先级任务抢占
- 阻塞（等待 I/O、信号量等）
- 终止

同优先级任务按 FIFO 顺序排队等待。这是确定性最强的调度策略，适合硬实时任务。

### 2、SCHED_RR（轮转调度）
实时调度策略，使用时间片。类似 SCHED_FIFO，但同优先级任务会轮流使用 CPU，每个任务运行一个时间片后轮转到队列末尾。时间片长度可通过 `sched_rr_get_interval()` 查询。

适合需要公平性的实时任务，如多个等优先级的实时线程。

### 3、SCHED_SPORADIC（零星调度）
POSIX.1b 实时扩展定义的调度策略，用于零星服务器。任务有正常优先级和低优先级两个级别，有预算时以正常优先级运行，预算耗尽后降为低优先级。预算会周期性补充。

适合周期性或零星的实时任务，可以限制 CPU 使用率同时保证响应性。

### 4、SCHED_OTHER/SCHED_NORMAL
默认的分时调度策略，在 openvela 中映射到 SCHED_FIFO 或 SCHED_RR。这是非实时任务的标准策略。

### 5、优先级范围

- 实时优先级（SCHED_FIFO/RR）：由配置决定，通常 1-255
- 最小优先级：`sched_get_priority_min(policy)`
- 最大优先级：`sched_get_priority_max(policy)`
- 数值越大，优先级越高

## 二、SMP 支持

在多核系统上（启用 `CONFIG_SMP`），openvela 支持 CPU 亲和性（affinity）设置，可以将任务绑定到特定 CPU 或 CPU 集合运行，用于负载均衡、缓存优化或隔离关键任务。

openvela 调度管理支持以下 API：

- `task_create()`
- `task_create_with_stack()`
- `task_delete()`
- `task_restart()`
- `task_setcancelstate()`
- `task_setcanceltype()`
- `task_testcancel()`
- `sched_setparam()`
- `sched_getparam()`
- `sched_setscheduler()`
- `sched_getscheduler()`
- `sched_yield()`
- `sched_get_priority_max()`
- `sched_get_priority_min()`
- `sched_rr_get_interval()`
- `sched_getcpu()`
- `sched_setaffinity()`
- `sched_getaffinity()`

## 1、task_create

```c
int task_create(const char *name, int priority, int stack_size,
                main_t entry, char * const argv[]);
```

创建一个新任务并使其就绪。新任务从 `entry` 函数开始执行，可以接收参数数组 `argv`。任务创建后立即处于就绪状态，根据优先级和调度策略决定何时运行。

与 `pthread_create()` 不同，`task_create()` 是 openvela 特有的轻量级任务创建接口，创建的任务不是 POSIX 线程，而是 openvela 原生任务。任务栈由系统自动分配和管理。

**参数**：

- `name` 任务名称（字符串），用于调试和识别。最大长度由 `CONFIG_TASK_NAME_SIZE` 配置决定。名称可以为 `NULL`，但建议提供有意义的名称以便调试。
- `priority` 任务优先级（整数）。有效范围取决于调度策略：
  - 实时优先级：通常 1-255（可通过 `sched_get_priority_min/max()` 查询）
  - 数值越大，优先级越高
  - 优先级 0 通常保留给 idle 任务
  - 建议使用 `SCHED_PRIORITY_DEFAULT` 或根据系统需求设置
- `stack_size` 任务栈大小（字节）。必须足够容纳局部变量、函数调用和中断处理。推荐至少 2048 字节，复杂任务可能需要更大栈。栈大小会自动对齐到系统要求的边界。
- `entry` 任务入口函数，类型为 `main_t`，签名为 `int (*)(int argc, char *argv[])`。函数返回时任务终止，返回值作为任务退出状态。
- `argv` 传递给任务的参数数组（字符串指针数组），必须以 `NULL` 结尾。类似于 `main()` 函数的 `argv`。参数字符串会被复制，原字符串可以在调用后释放。如果不需要参数，可以传递 `NULL` 或空数组 `{NULL}`。

**返回值**：

- 成功：返回新任务的 PID（进程 ID，正整数）。可用于后续的任务控制操作（如 `task_delete()`、`sched_setparam()` 等）。
- 失败：返回负的错误码：
  - `-EINVAL`：参数无效（如优先级超出范围、栈大小为 0）
  - `-ENOMEM`：内存不足，无法分配任务控制块或栈
  - `-EAGAIN`：系统资源不足，达到任务数量限制

**注意**：

- **任务 vs 线程**：`task_create()` 创建的是 openvela 原生任务，不是 POSIX 线程。任务比线程更轻量，但不支持某些 pthread 特性（如线程局部存储、线程清理函数等）。对于 POSIX 兼容性，应使用 `pthread_create()`。
- **栈分配**：栈由系统自动分配（通常从堆中），任务终止时自动释放。如果需要使用预分配的栈，使用 `task_create_with_stack()`。
- **参数传递**：`argv` 数组及其字符串会被复制到任务的上下文中，因此调用者可以在函数返回后释放或修改原参数。但要注意，参数是浅拷贝（指针本身复制，指针指向的数据不复制）。
- **任务调度**：任务创建后立即处于就绪状态。如果新任务优先级高于当前任务，会立即抢占当前任务（抢占式调度）。
- **任务终止**：入口函数返回后任务自动终止。也可以调用 `exit()`、`task_delete()` 或接收信号（如 `SIGKILL`）终止。
- **资源管理**：任务终止后，系统会自动清理其资源（栈、任务控制块等），但不会清理任务分配的其他资源（如打开的文件、分配的内存等），需要任务自己负责清理。
- **初始调度策略**：新任务的调度策略默认为 `SCHED_FIFO`（或系统默认策略），可以在创建后使用 `sched_setscheduler()` 修改。
- **典型用法**：
  ```c
  char *argv[] = {"arg1", "arg2", NULL};
  int pid = task_create("my_task", 100, 4096, task_main, argv);
  if (pid < 0) {
      printf("Failed to create task: %d\n", pid);
  }
  ```
- **与 fork() 的区别**：不同于 `fork()`，`task_create()` 不复制父任务的地址空间，新任务从指定入口函数开始执行，不共享父任务的代码段以外的资源。

**POSIX 兼容性**：openvela 扩展接口（非 POSIX 标准）。

## 2、task_create_with_stack

```c
int task_create_with_stack(const char *name, int priority,
                           void *stack, int stack_size,
                           main_t entry, char * const argv[]);
```

使用预分配的栈创建一个新任务。与 `task_create()` 类似，但允许调用者提供栈内存，而不是由系统自动分配。这在需要精确控制内存布局、使用特殊内存区域（如共享内存、DMA 可访问内存）或优化启动性能时非常有用。

预分配栈给予程序员更多控制权，但也带来了更多责任（如栈大小验证、内存对齐、生命周期管理）。

**参数**：

- `name` 任务名称，用于调试和标识。字符串会被复制，因此可以是临时缓冲区。最大长度通常由 `CONFIG_TASK_NAME_SIZE` 定义（如 31 字符 + NULL）。如果为 `NULL`，任务将有一个自动生成的名称。
- `priority` 任务优先级，数值越大优先级越高。有效范围通常为 1 到 255，可以通过 `sched_get_priority_min()` / `sched_get_priority_max()` 查询。优先级决定任务的调度顺序。
- `stack` 指向预分配栈内存的指针。必须：
  - **非 NULL**：不能为 NULL，否则返回错误
  - **足够大小**：至少为 `stack_size` 字节
  - **正确对齐**：通常需要对齐到架构要求的边界（如 8 字节或 16 字节）
  - **可写**：栈内存必须可读写
  - **生命周期管理**：调用者负责在任务终止后释放栈内存（如果动态分配）
- `stack_size` 栈大小（字节）。必须满足：
  - **最小要求**：至少为 `PTHREAD_STACK_MIN`（通常几百字节）
  - **任务需求**：足够容纳任务的局部变量、函数调用深度、中断/异常处理
  - **对齐**：某些架构可能要求大小也对齐（如 8 字节的倍数）
- `entry` 任务入口函数，签名为 `int main(int argc, char *argv[])`。不能为 `NULL`，否则返回错误。
- `argv` 传递给任务的参数数组（类似 `main()` 的 `argv`）。数组必须以 `NULL` 指针结尾。可以为 `NULL`，表示无参数（等同于空数组）。

**返回值**：

- 成功：返回新任务的 PID（正整数）
- 失败：返回负的错误码：
  - `-EINVAL`：参数无效（如 `stack` 为 NULL、`entry` 为 NULL、`priority` 超出范围）
  - `-ENOMEM`：内存不足（虽然栈已提供，但任务控制块等仍需分配）
  - `-EAGAIN`：系统任务数已达上限（`CONFIG_MAX_TASKS`）

**注意**：

- **与 task_create 的区别**：
  - **task_create**：系统自动分配和释放栈
  - **task_create_with_stack**：调用者提供栈，并负责释放
- **栈生命周期管理**：
  - 栈内存必须在任务的整个生命周期内保持有效
  - 任务终止后，调用者负责释放栈内存（如果是动态分配的）
  - 如果栈是静态数组或全局变量，无需显式释放
- **典型用法（动态分配栈）**：
  ```c
  void *stack = malloc(8192);
  if (stack == NULL) {
      perror("malloc");
      return -1;
  }
  
  int pid = task_create_with_stack("worker", 100, stack, 8192,
                                   worker_func, NULL);
  if (pid < 0) {
      perror("task_create_with_stack");
      free(stack);
      return -1;
  }
  
  // ... 等待任务结束 ...
  waitpid(pid, NULL, 0);
  free(stack);  // 释放栈
  ```
- **静态栈示例**：
  ```c
  static uint8_t worker_stack[4096] __attribute__((aligned(16)));
  
  int pid = task_create_with_stack("worker", 100, worker_stack,
                                   sizeof(worker_stack), worker_func, NULL);
  ```
- **栈方向**：某些架构栈向下增长，某些向上增长。openvela 会自动处理栈方向，调用者只需提供起始地址和大小。
- **栈对齐**：确保栈地址正确对齐（通常 8 字节或 16 字节），否则可能导致未定义行为或性能下降：
  ```c
  void *stack = aligned_alloc(16, 8192);  // 16 字节对齐
  ```
- **栈溢出保护**：预分配栈不自动提供溢出保护（guard page）。如果需要，应在栈顶/底额外分配保护页，并设置为不可访问：
  ```c
  void *stack_with_guard = malloc(8192 + 4096);  // 多分配一页保护
  mprotect(stack_with_guard, 4096, PROT_NONE);   // 保护页不可访问
  void *usable_stack = (char*)stack_with_guard + 4096;
  task_create_with_stack("worker", 100, usable_stack, 8192, worker_func, NULL);
  ```
- **共享内存栈**：可以使用共享内存作为栈，实现跨进程的栈共享（高级用法，需要仔细同步）：
  ```c
  int shm_fd = shm_open("/worker_stack", O_CREAT | O_RDWR, 0666);
  ftruncate(shm_fd, 8192);
  void *stack = mmap(NULL, 8192, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
  task_create_with_stack("worker", 100, stack, 8192, worker_func, NULL);
  ```
- **性能考虑**：使用预分配栈可以减少任务创建时的内存分配开销，提高启动性能。在需要频繁创建/销毁任务的场景中（如任务池），可以维护一个栈缓存池。
- **调试建议**：在调试阶段，可以在栈边界填充魔数（如 0xDEADBEEF），然后定期检查，及早发现栈溢出：
  ```c
  uint32_t *stack_end = (uint32_t*)((char*)stack + stack_size - sizeof(uint32_t));
  *stack_end = 0xDEADBEEF;
  // ... 任务运行 ...
  if (*stack_end != 0xDEADBEEF) {
      printf("Stack overflow detected!\n");
  }
  ```
- **实时系统优化**：在实时系统中，使用预分配栈可以避免动态分配的不确定性，提高任务创建的确定性和速度。
- **陷阱**：
  - 栈过小会导致栈溢出，难以调试（通常表现为随机崩溃或数据损坏）
  - 忘记释放动态分配的栈会导致内存泄漏
  - 栈未对齐可能导致未定义行为（某些架构会崩溃，某些只是性能下降）
  - 在任务仍在运行时释放栈会导致严重错误

**POSIX 兼容性**：openvela 扩展接口（非 POSIX 标准，类似于某些 RTOS 的接口）。

## 3、task_delete

```c
int task_delete(pid_t pid);
```

删除（终止）指定的任务，释放其占用的系统资源。与 `pthread_cancel()` 或 `kill(pid, SIGKILL)` 类似，但这是 openvela 的原生接口，更直接和高效。

任务删除是强制性的，不经过正常的清理流程（如 `atexit` 处理程序），应谨慎使用。通常应优先使用协作式终止机制（如设置退出标志，让任务自行退出）。

**参数**：

- `pid` 要删除的任务 PID。特殊值 0 表示删除调用任务自身（等同于 `exit()`）。必须是有效的任务 PID。

**返回值**：

- 成功：返回 0（`OK`）
- 失败：返回负的错误码：
  - `-EINVAL`：`pid` 无效（如为负值）
  - `-ESRCH`：指定的任务不存在（PID 无效或任务已终止）
  - `-EPERM`：调用者没有权限删除目标任务（取决于系统配置）

**注意**：

- **强制终止**：任务被立即终止，不会执行清理代码（如 `pthread_cleanup_push` 注册的处理程序、`atexit` 回调等）。这可能导致资源泄漏（如未释放的内存、未关闭的文件、未解锁的互斥锁）。
- **资源清理**：内核会自动回收任务的核心资源（如栈内存、任务控制块），但应用层资源（如堆内存、打开的文件）可能不会自动清理。
- **删除自身**：如果 `pid` 为 0，任务会删除自己，永不返回（类似调用 `exit(0)`）：
  ```c
  task_delete(0);
  // 这行代码永远不会执行
  ```
- **与 pthread_cancel 的区别**：
  - `task_delete()` 立即强制终止，无取消点概念
  - `pthread_cancel()` 在下一个取消点才生效，允许清理
  - `task_delete()` 是 openvela 扩展，`pthread_cancel()` 是 POSIX 标准
- **典型用法**：
  ```c
  int pid = task_create("worker", 100, 2048, worker_func, NULL);
  // ... 任务运行 ...
  
  // 终止任务
  if (task_delete(pid) == 0) {
      printf("Task %d deleted\n", pid);
  } else {
      perror("task_delete");
  }
  ```
- **互斥锁陷阱**：如果被删除的任务正持有互斥锁，其他等待该锁的任务将永远阻塞（死锁）。应确保任务在被删除前释放所有锁。
- **子任务清理**：删除父任务不会自动删除其子任务。如果需要清理整个任务树，必须显式删除所有子任务。
- **替代方案**：
  - **协作式退出**：设置退出标志，让任务自行检查并退出
  - **pthread_cancel**：使用 POSIX 取消机制，允许清理处理程序运行
  - **信号**：发送 `SIGTERM`，让任务捕获并优雅退出
- **实时系统注意**：在实时系统中，强制删除任务可能影响系统的确定性和可预测性，应谨慎使用。
- **调试建议**：在调试阶段，可以在任务入口和退出点添加日志，帮助跟踪任务生命周期。
- **批量删除**：如果需要删除多个任务，应按依赖顺序删除（先删除子任务，后删除父任务），避免悬空引用。

**POSIX 兼容性**：openvela 扩展接口（非 POSIX 标准）。

## 4、task_restart

```c
int task_restart(pid_t pid);
```

重启指定的任务，任务将使用原始的入口点、参数、优先级和栈大小重新开始执行。这相当于先终止任务，然后用相同参数重新创建。

任务重启是一种特殊的恢复机制，用于处理任务异常或需要重置任务状态的场景。与删除后重新创建相比，重启保留了原始任务的配置信息。

**参数**：

- `pid` 要重启的任务 PID。必须是有效的任务 PID（不能为 0，因为不能重启自己）。

**返回值**：

- 成功：返回 0（`OK`）
- 失败：返回负的错误码：
  - `-EINVAL`：`pid` 无效（如为 0 或负值）
  - `-ESRCH`：指定的任务不存在（PID 无效或任务已终止）
  - `-EPERM`：调用者没有权限重启目标任务（取决于系统配置）
  - `-ENOMEM`：内存不足，无法重启任务

**注意**：

- **不能重启自己**：不能用 `task_restart(0)` 或 `task_restart(getpid())` 重启自己，因为重启会销毁当前执行上下文。如果尝试这样做，通常会返回 `-EINVAL`。
- **任务状态重置**：重启后，任务的所有状态（包括局部变量、堆栈内容、寄存器）都会重置，就像刚刚创建一样。任务会从入口函数开始执行。
- **保留配置**：重启后的任务保留原始配置：
  - 任务名称（name）
  - 优先级（priority）
  - 栈大小（stack_size）
  - 入口函数（entry）
  - 入口参数（argv）
- **PID 保持不变**：重启后，任务的 PID 保持不变，其他任务引用此 PID 仍然有效。
- **典型用法**：
  ```c
  int pid = task_create("monitor", 150, 2048, monitor_task, NULL);
  
  // ... 任务运行一段时间后检测到异常 ...
  
  // 重启任务
  if (task_restart(pid) == 0) {
      printf("Task %d restarted\n", pid);
  } else {
      perror("task_restart");
  }
  ```
- **与 task_delete + task_create 的区别**：
  - **task_restart**：PID 不变，保留原始配置，一步完成
  - **task_delete + task_create**：PID 改变，需要重新指定所有参数，两步操作
- **资源清理**：重启前，任务持有的资源（如打开的文件、分配的内存、持有的锁）可能不会自动释放，这可能导致资源泄漏。应在任务设计时考虑异常恢复机制。
- **互斥锁陷阱**：如果任务正持有互斥锁，重启会导致锁永远无法释放（死锁）。应确保任务在重启前释放所有锁，或使用鲁棒互斥锁（robust mutex）。
- **看门狗场景**：常用于看门狗系统，当检测到任务无响应或异常时，自动重启任务恢复服务：
  ```c
  void watchdog_task(void *arg) {
      while (1) {
          if (check_task_health(worker_pid) == FAILED) {
              printf("Worker unhealthy, restarting...\n");
              task_restart(worker_pid);
          }
          sleep(5);
      }
  }
  ```
- **重启计数**：在生产系统中，应限制重启次数，避免陷入无限重启循环：
  ```c
  int restart_count = 0;
  const int MAX_RESTARTS = 3;
  
  if (task_restart(pid) == 0) {
      restart_count++;
      if (restart_count >= MAX_RESTARTS) {
          printf("Max restarts reached, giving up\n");
          task_delete(pid);
      }
  }
  ```
- **异步操作**：重启是异步的，函数返回时任务可能还在初始化中。如果需要等待任务完成初始化，应使用额外的同步机制（如信号量）。
- **调试建议**：在任务入口函数中添加日志，记录每次启动时间和原因，有助于分析重启历史。
- **实时系统影响**：频繁重启任务可能影响系统的实时性和可预测性，应通过改进任务健壮性来减少重启需求。

**POSIX 兼容性**：openvela 扩展接口（非 POSIX 标准）。

## 5、task_setcancelstate

```c
int task_setcancelstate(int state, int *oldstate);
```

设置调用任务的取消状态（cancel state），控制任务是否可以被取消。与 `pthread_setcancelstate()` 类似，但适用于所有任务（不仅限于 pthread）。

取消状态是任务取消机制的一部分，允许任务临时禁止取消，保护关键代码段不被中断。

**参数**：

- `state` 新的取消状态，有效值：
  - `TASK_CANCEL_ENABLE` (0)：允许取消（默认），任务可以响应取消请求
  - `TASK_CANCEL_DISABLE` (1)：禁止取消，任务忽略取消请求（请求被推迟）
- `oldstate` 如果非 `NULL`，用于接收之前的取消状态。如果不关心旧值，可以传 `NULL`。

**返回值**：

- 成功：返回 0（`OK`）
- 失败：返回负的错误码：
  - `-EINVAL`：`state` 参数无效（不是 `TASK_CANCEL_ENABLE` 或 `TASK_CANCEL_DISABLE`）

**注意**：

- **保护关键区域**：在执行不可中断的关键操作时（如更新共享数据结构、持有互斥锁），应禁用取消：
  ```c
  task_setcancelstate(TASK_CANCEL_DISABLE, NULL);
  // 关键操作，不能被取消中断
  update_critical_data();
  task_setcancelstate(TASK_CANCEL_ENABLE, NULL);
  ```
- **推迟取消**：当取消状态为 `TASK_CANCEL_DISABLE` 时，取消请求不会丢失，而是被推迟。当取消状态重新设置为 `TASK_CANCEL_ENABLE` 时，如果有待处理的取消请求，任务会在下一个取消点被取消。
- **取消类型交互**：取消状态与取消类型（`task_setcanceltype()`）共同决定取消行为：
  - **状态=ENABLE, 类型=DEFERRED**：在取消点才取消（默认，最安全）
  - **状态=ENABLE, 类型=ASYNCHRONOUS**：任何时候都可以取消（危险）
  - **状态=DISABLE**：无论类型如何，都不会取消
- **典型用法（保存旧状态）**：
  ```c
  int oldstate;
  task_setcancelstate(TASK_CANCEL_DISABLE, &oldstate);
  // 关键操作
  critical_section();
  task_setcancelstate(oldstate, NULL);  // 恢复原状态
  ```
- **与互斥锁配合**：
  ```c
  pthread_mutex_lock(&mutex);
  task_setcancelstate(TASK_CANCEL_DISABLE, NULL);
  
  // 受保护的操作
  modify_shared_data();
  
  task_setcancelstate(TASK_CANCEL_ENABLE, NULL);
  pthread_mutex_unlock(&mutex);
  ```
- **默认状态**：新创建的任务默认取消状态为 `TASK_CANCEL_ENABLE`，允许被取消。
- **不影响信号**：取消状态只影响通过 `task_delete()` 或类似机制的取消，不影响信号（如 `SIGTERM`）的处理。
- **与 pthread 的兼容性**：在 pthread 线程中，`task_setcancelstate()` 和 `pthread_setcancelstate()` 通常是等价的，操作同一底层状态。
- **嵌套禁用**：可以多次调用 `TASK_CANCEL_DISABLE`，但每次都应对应一次 `TASK_CANCEL_ENABLE`（或恢复旧状态），否则可能导致永久禁用取消：
  ```c
  int old1, old2;
  task_setcancelstate(TASK_CANCEL_DISABLE, &old1);  // 第一次禁用
  task_setcancelstate(TASK_CANCEL_DISABLE, &old2);  // 第二次禁用（无效果）
  task_setcancelstate(old2, NULL);  // 恢复到old2（仍然禁用）
  task_setcancelstate(old1, NULL);  // 恢复到old1（可能启用）
  ```
  更简单的做法是只在最外层操作取消状态。
- **清理处理程序**：即使禁用了取消，清理处理程序（`pthread_cleanup_push`）仍然会在任务正常退出时执行。
- **性能考虑**：设置取消状态是轻量操作，但应避免在紧密循环中频繁切换，以免影响性能。

**POSIX 兼容性**：类似 `pthread_setcancelstate()`，但适用于所有任务类型。

## 6、task_setcanceltype

```c
int task_setcanceltype(int type, int *oldtype);
```

设置调用任务的取消类型（cancel type），控制取消请求何时生效。与 `pthread_setcanceltype()` 类似，但适用于所有任务（不仅限于 pthread）。

取消类型决定了任务响应取消请求的时机，影响任务取消的安全性和响应性。

**参数**：

- `type` 新的取消类型，有效值：
  - `TASK_CANCEL_DEFERRED` (0)：延迟取消（默认），仅在取消点（cancellation point）才响应取消请求，如 `pthread_testcancel()`、`sleep()`、`read()` 等阻塞调用
  - `TASK_CANCEL_ASYNCHRONOUS` (1)：异步取消，任务可以在任意时刻被取消（危险，可能导致资源泄漏或数据不一致）
- `oldtype` 如果非 `NULL`，用于接收之前的取消类型。如果不关心旧值，可以传 `NULL`。

**返回值**：

- 成功：返回 0（`OK`）
- 失败：返回负的错误码：
  - `-EINVAL`：`type` 参数无效（不是 `TASK_CANCEL_DEFERRED` 或 `TASK_CANCEL_ASYNCHRONOUS`）

**注意**：

- **默认类型（DEFERRED）最安全**：延迟取消是默认且推荐的类型，它只在明确定义的取消点才生效，允许任务在取消前完成当前操作并清理资源。
- **异步取消的危险性**：`TASK_CANCEL_ASYNCHRONOUS` 极其危险，因为任务可能在任何时刻被取消：
  - 可能在持有互斥锁时被取消，导致死锁
  - 可能在更新数据结构的中途被取消，导致数据不一致
  - 可能在分配内存后、保存指针前被取消，导致内存泄漏
  - 只有非常特殊的代码（如纯计算任务，不访问共享资源）才应使用异步取消
- **取消点**：常见的取消点包括：
  - `task_testcancel()` / `pthread_testcancel()`：显式取消点
  - 阻塞的系统调用：`sleep()`、`usleep()`、`read()`、`write()`、`recv()`、`send()`
  - 同步原语：`pthread_cond_wait()`、`sem_wait()`
  - 某些库函数：`printf()`（可能）
- **典型用法（临时启用异步取消）**：
  ```c
  int oldtype;
  task_setcanceltype(TASK_CANCEL_ASYNCHRONOUS, &oldtype);
  // 纯计算任务，不访问共享资源
  perform_long_computation();
  task_setcanceltype(oldtype, NULL);  // 恢复原类型
  ```
  但通常更好的做法是在循环中定期调用 `task_testcancel()`。
- **推荐做法（在循环中添加取消点）**：
  ```c
  while (processing) {
      process_chunk();
      task_testcancel();  // 定期检查取消请求
  }
  ```
  这比使用异步取消更安全，且仍能及时响应取消。
- **与取消状态交互**：取消类型与取消状态共同决定取消行为：
  - **状态=ENABLE, 类型=DEFERRED**：在取消点才取消（默认，最安全）
  - **状态=ENABLE, 类型=ASYNCHRONOUS**：任何时候都可以取消（危险）
  - **状态=DISABLE**：无论类型如何，都不会取消
- **清理处理程序**：无论取消类型如何，任务被取消时都会执行清理处理程序（`pthread_cleanup_push` 注册）。但异步取消可能在不一致的状态下触发清理，导致问题。
- **实时系统考虑**：在实时系统中，异步取消可能影响系统的可预测性，应避免使用。优先使用延迟取消或协作式退出机制。
- **与 pthread 的兼容性**：在 pthread 线程中，`task_setcanceltype()` 和 `pthread_setcanceltype()` 通常是等价的。
- **默认值**：新创建的任务默认取消类型为 `TASK_CANCEL_DEFERRED`（延迟取消）。
- **避免混用**：不要在同一任务中混用延迟和异步取消类型，这会使代码难以理解和维护。选择一种类型并坚持使用。
- **异步安全代码**：如果必须使用异步取消，确保任务代码是异步安全的（async-cancel-safe），类似于信号处理程序的要求：
  - 不调用非异步安全的函数（如 `malloc()`、`printf()`）
  - 不访问共享数据（或使用原子操作）
  - 不持有任何锁

**POSIX 兼容性**：类似 `pthread_setcanceltype()`，但适用于所有任务类型。

## 7、task_testcancel

```c
void task_testcancel(void);
```

创建一个显式的取消点（cancellation point）。如果有待处理的取消请求，且任务的取消状态为允许（`TASK_CANCEL_ENABLE`），则任务将在此处被取消并终止。

这是延迟取消机制的核心，允许任务在安全的位置响应取消请求，确保资源正确释放和状态一致性。

**参数**：

无参数。

**返回值**：

- 无返回值（如果任务被取消，函数永不返回）
- 如果没有待处理的取消请求，或取消状态为禁止，函数正常返回

**注意**：

- **显式取消点**：此函数是程序员主动创建的取消点，与隐式取消点（如 `sleep()`、`read()`）不同。显式取消点提供了更精确的控制，允许任务在安全的位置检查取消请求。
- **典型用法（长时间循环）**：
  ```c
  while (processing) {
      process_data_chunk();
      task_testcancel();  // 定期检查取消请求
  }
  ```
  这确保任务能及时响应取消，同时保证每次循环迭代完整完成。
- **取消条件**：任务仅在以下所有条件都满足时被取消：
  1. 有待处理的取消请求（通过 `task_delete()` 或类似机制触发）
  2. 取消状态为 `TASK_CANCEL_ENABLE`（默认）
  3. 取消类型为 `TASK_CANCEL_DEFERRED`（默认），或者无论类型（如果状态为 ENABLE）
- **清理处理程序**：如果任务被取消，会执行清理处理程序（`pthread_cleanup_push` 注册），然后终止。确保在关键资源（如互斥锁）使用时注册清理处理程序：
  ```c
  pthread_mutex_lock(&mutex);
  pthread_cleanup_push((void(*)(void*))pthread_mutex_unlock, &mutex);
  
  // 可能被取消的操作
  while (condition) {
      process_data();
      task_testcancel();
  }
  
  pthread_cleanup_pop(1);  // 正常退出也解锁
  ```
- **不影响异步取消**：如果取消类型为 `TASK_CANCEL_ASYNCHRONOUS`，任务可能在任何时刻被取消，不仅限于取消点。
- **与 pthread_testcancel 的兼容性**：`task_testcancel()` 和 `pthread_testcancel()` 通常是等价的，可以互换使用。
- **性能考虑**：检查取消请求是轻量操作，但应避免在极紧密的循环中调用（如每次循环耗时微秒级），以免影响性能。可以每处理 N 个项目后调用一次：
  ```c
  for (int i = 0; i < items; i++) {
      process_item(i);
      if (i % 100 == 0) task_testcancel();  // 每100次检查一次
  }
  ```
- **取消安全的位置**：应在以下位置调用 `task_testcancel()`：
  - 不持有任何互斥锁
  - 所有数据结构处于一致状态
  - 没有未释放的临时资源
- **实时系统影响**：在实时系统中，取消点会增加任务的响应时间不确定性（虽然很小）。如果需要极高的确定性，可以在任务设计时避免取消机制，改用协作式退出。
- **调试建议**：在调试取消相关问题时，可以在 `task_testcancel()` 前后添加日志，跟踪取消点的执行：
  ```c
  printf("Before testcancel\n");
  task_testcancel();
  printf("After testcancel (not cancelled)\n");
  ```
- **与退出标志的比较**：
  - **task_testcancel()**：内核机制，更轻量，与清理处理程序集成
  - **退出标志**：用户态机制，更灵活，但需要手动管理清理
  ```c
  // 退出标志方式
  volatile bool should_exit = false;
  while (!should_exit) {
      process_data();
  }
  ```
- **无操作返回**：如果没有取消请求，函数立即返回，几乎无开销（只是检查一个标志位）。

**POSIX 兼容性**：类似 `pthread_testcancel()`，但适用于所有任务类型。

## 8、sched_setparam

```c
int sched_setparam(pid_t pid, const struct sched_param *param);
```

修改指定任务的调度参数（主要是优先级），但不改变调度策略。这是调整任务优先级的标准接口，比 `sched_setscheduler()` 更轻量，语义更清晰。

优先级是调度系统中最重要的参数，决定了任务在同一策略下的执行顺序。动态调整优先级是实时系统中常见的需求，例如实现优先级继承或优先级天花板协议。

**参数**：

- `pid` 目标任务的 PID。特殊值 0 表示修改调用任务自身的参数。必须是有效的任务 PID。
- `param` 指向 `struct sched_param` 结构的指针，包含新的调度参数。主要字段：
  - `sched_priority`：新的优先级值（必需），必须在当前调度策略的有效范围内
  - 对于 SCHED_SPORADIC 策略，还包括 `sched_ss_low_priority`、`sched_ss_repl_period`、`sched_ss_init_budget`、`sched_ss_max_repl` 等零星服务器参数

**返回值**：

- 成功：返回 0
- 失败：返回 -1 并设置 `errno`：
  - `EINVAL`：`param` 中的优先级超出当前策略允许的范围，或 SCHED_SPORADIC 参数无效
  - `ESRCH`：指定的任务不存在（PID 无效或任务已终止）
  - `EPERM`：调用者没有权限修改目标任务的调度参数（通常需要超级用户权限或同一用户）
  - `EFAULT`：`param` 指向无效内存

**注意**：

- **保持策略不变**：此函数只修改调度参数，不改变调度策略。如果需要同时修改策略和参数，使用 `sched_setscheduler()`。
- **优先级范围**：每种调度策略有其有效的优先级范围，可以通过 `sched_get_priority_min()` 和 `sched_get_priority_max()` 查询。超出范围会导致 `EINVAL` 错误。
- **立即生效**：优先级修改立即生效，调度器会重新评估任务优先级：
  - 如果新优先级更高，任务可能立即抢占当前任务
  - 如果新优先级更低，任务可能被其他高优先级任务抢占
  - 对于阻塞任务，新优先级在任务恢复运行时生效
- **优先级继承**：在实现互斥锁的优先级继承协议时，通常使用此函数临时提升低优先级任务的优先级，避免优先级反转。
- **典型用法**：
  ```c
  struct sched_param param;
  param.sched_priority = 100;  // 设置新优先级
  
  if (sched_setparam(0, &param) == 0) {
      printf("Priority changed to %d\n", param.sched_priority);
  } else {
      perror("sched_setparam");
  }
  ```
- **查询当前参数**：使用 `sched_getparam()` 获取任务当前的调度参数，然后修改需要改变的字段。
- **实时系统调优**：在实时系统中，根据任务的实际执行情况动态调整优先级，可以优化系统响应性和吞吐量。
- **权限要求**：修改其他任务的优先级通常需要特权。在嵌入式系统中，通常所有任务运行在同一权限级别，这一限制可能较宽松。
- **对运行任务的影响**：修改当前运行任务（pid=0）的优先级可能立即触发重新调度，如果系统中有更高优先级的就绪任务。
- **SCHED_SPORADIC 参数**：对于零星调度任务，`param` 中的其他字段（如 `sched_ss_low_priority`）也可以通过此函数修改，实现动态调整零星服务器行为。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 9、sched_getparam

```c
int sched_getparam(pid_t pid, struct sched_param *param);
```

查询指定任务的当前调度参数（主要是优先级）。这是获取任务优先级和其他调度参数的标准接口，常用于监控、调试和动态调度决策。

调度参数包括基本优先级以及特定策略相关的参数（如零星调度的补充周期），了解这些参数有助于理解任务的调度行为。

**参数**：

- `pid` 目标任务的 PID。特殊值 0 表示查询调用任务自身的参数。必须是有效的任务 PID。
- `param` 指向 `struct sched_param` 结构的指针，用于接收查询结果。函数会填充此结构：
  - `sched_priority`：任务的基本优先级（始终设置）
  - 对于 SCHED_SPORADIC 策略，还包括 `sched_ss_low_priority`、`sched_ss_repl_period`、`sched_ss_init_budget`、`sched_ss_max_repl` 等零星服务器参数
  - 其他策略（SCHED_FIFO、SCHED_RR、SCHED_OTHER）通常只设置 `sched_priority`

**返回值**：

- 成功：返回 0，并在 `param` 中填充任务的调度参数
- 失败：返回 -1 并设置 `errno`：
  - `ESRCH`：指定的任务不存在（PID 无效或任务已终止）
  - `EINVAL`：参数 `pid` 为负值
  - `EFAULT`：`param` 指向无效内存（NULL 或不可写）

**注意**：

- **只读查询**：此函数不修改任务状态，是纯查询操作，开销很小。
- **完整调度信息**：通常与 `sched_getscheduler()` 配合使用，获取完整的调度信息（策略 + 参数）：
  ```c
  int policy = sched_getscheduler(0);
  struct sched_param param;
  sched_getparam(0, &param);
  printf("Policy: %d, Priority: %d\n", policy, param.sched_priority);
  ```
- **典型用法**：
  ```c
  struct sched_param param;
  if (sched_getparam(0, &param) == 0) {
      printf("Current priority: %d\n", param.sched_priority);
  } else {
      perror("sched_getparam");
  }
  ```
- **动态调整参考**：在动态调整优先级前，先用此函数获取当前参数，然后修改特定字段，最后用 `sched_setparam()` 应用更改。
- **监控工具**：系统监控工具常用此函数显示任务的优先级，帮助分析调度行为和诊断优先级反转等问题。
- **零星调度参数**：对于 SCHED_SPORADIC 策略的任务，此函数返回完整的零星服务器配置，包括预算、补充周期等。
- **参数初始化**：在调用前无需初始化 `param` 结构，函数会完全覆盖其内容。但确保 `param` 指向有效内存。
- **任务诊断**：在调试实时系统时，可以定期查询关键任务的优先级，验证优先级继承等机制是否正常工作。
- **原子性**：查询操作是原子的，返回的参数是一致的快照，不会出现部分更新的情况。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 10、sched_setscheduler

```c
int sched_setscheduler(pid_t pid, int policy, const struct sched_param *param);
```

设置指定任务的调度策略和调度参数（如优先级）。这是控制任务调度行为的主要接口，允许在运行时动态调整任务的调度特性。

调度策略决定了任务如何竞争 CPU 时间，不同策略适用于不同类型的任务（实时、批处理、交互等）。修改调度策略通常需要适当的权限。

**参数**：

- `pid` 目标任务的 PID。特殊值 0 表示调用任务自身。必须是有效的任务 PID。
- `policy` 新的调度策略，有效值包括：
  - `SCHED_FIFO` (0)：先进先出实时调度，无时间片，适合硬实时任务
  - `SCHED_RR` (1)：轮转实时调度，有时间片，适合需要公平性的实时任务
  - `SCHED_SPORADIC` (2)：零星调度，适合周期性实时任务（需要 `CONFIG_SCHED_SPORADIC`）
  - `SCHED_OTHER` (3)：标准分时调度，映射到 SCHED_FIFO 或 SCHED_RR
  - `SCHED_NORMAL` (3)：SCHED_OTHER 的别名
  - `SCHED_BATCH` (4)：批处理调度（如果支持）
  - `SCHED_IDLE` (5)：空闲调度，最低优先级（如果支持）
- `param` 指向 `struct sched_param` 结构的指针，包含调度参数。至少需要设置 `sched_priority` 字段（基本优先级）。对于 SCHED_SPORADIC，还需要设置零星服务器参数（低优先级、补充周期、初始预算、最大补充次数）。

**返回值**：

- 成功：返回任务之前的调度策略（`SCHED_FIFO`、`SCHED_RR` 等）
- 失败：返回 -1 并设置 `errno`：
  - `EINVAL`：`policy` 无效，或 `param` 中的优先级超出该策略允许的范围
  - `ESRCH`：指定的任务不存在（PID 无效或任务已终止）
  - `EPERM`：调用者没有权限修改目标任务的调度策略（通常需要超级用户权限或同一用户）
  - `EFAULT`：`param` 指向无效内存

**注意**：

- **优先级范围**：不同调度策略有不同的有效优先级范围，可以通过 `sched_get_priority_min(policy)` 和 `sched_get_priority_max(policy)` 查询。设置超出范围的优先级会导致 `EINVAL` 错误。
- **策略切换影响**：
  - 切换到更高优先级的策略可能导致任务立即抢占当前任务
  - 切换到较低优先级可能导致任务被其他任务抢占
  - 策略切换不会改变任务的就绪状态，已阻塞的任务仍然阻塞
- **SCHED_SPORADIC 参数**：使用此策略时，必须在 `param` 中设置：
  - `sched_ss_low_priority`：预算耗尽后的低优先级
  - `sched_ss_repl_period`：补充周期
  - `sched_ss_init_budget`：初始预算
  - `sched_ss_max_repl`：最大待处理补充次数（<= `SS_REPL_MAX`）
- **实时调度策略**：SCHED_FIFO 和 SCHED_RR 是实时策略，通常需要提升权限。实时任务可能影响系统响应性，应谨慎使用。
- **调度策略继承**：子任务（通过 `fork()` 或 `task_create()` 创建）通常继承父任务的调度策略和优先级，除非在创建时指定或稍后修改。
- **典型用法**：
  ```c
  struct sched_param param;
  param.sched_priority = 150;  // 设置高优先级
  
  int old_policy = sched_setscheduler(0, SCHED_FIFO, &param);
  if (old_policy < 0) {
      perror("sched_setscheduler");
  } else {
      printf("Changed from policy %d to SCHED_FIFO\n", old_policy);
  }
  ```
- **查询当前策略**：使用 `sched_getscheduler(pid)` 查询任务当前的调度策略。
- **仅修改优先级**：如果只想修改优先级而不改变策略，使用 `sched_setparam()`，它更高效且语义更清晰。
- **原子性**：策略和参数的修改是原子的，不会出现中间状态。
- **对运行任务的影响**：如果修改当前正在运行的任务（pid=0），调度器会立即重新评估任务优先级，可能导致任务被抢占。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 11、sched_getscheduler

```c
int sched_getscheduler(pid_t pid);
```

查询指定任务的当前调度策略。这是一个轻量级查询接口，用于获取任务的调度策略类型（如 SCHED_FIFO、SCHED_RR 等）。

调度策略决定了任务的调度行为，了解当前策略有助于调试和监控任务的实时特性。

**参数**：

- `pid` 目标任务的 PID。特殊值 0 表示查询调用任务自身的调度策略。必须是有效的任务 PID。

**返回值**：

- 成功：返回任务当前的调度策略（非负整数）：
  - `SCHED_FIFO` (0)：先进先出实时调度
  - `SCHED_RR` (1)：轮转实时调度
  - `SCHED_SPORADIC` (2)：零星调度（如果支持）
  - `SCHED_OTHER` (3)：标准分时调度
  - `SCHED_BATCH` (4)：批处理调度（如果支持）
  - `SCHED_IDLE` (5)：空闲调度（如果支持）
- 失败：返回 -1 并设置 `errno`：
  - `ESRCH`：指定的任务不存在（PID 无效或任务已终止）
  - `EINVAL`：参数 `pid` 为负值

**注意**：

- **只读查询**：此函数不修改任务状态，是纯查询操作，开销很小。
- **配合使用**：通常与 `sched_getparam()` 配合使用，以获取完整的调度信息（策略 + 参数）。
- **典型用法**：
  ```c
  int policy = sched_getscheduler(0);  // 查询自己的策略
  if (policy >= 0) {
      const char *policy_names[] = {"SCHED_FIFO", "SCHED_RR", "SCHED_SPORADIC", "SCHED_OTHER"};
      printf("Current policy: %s\n", policy_names[policy]);
  } else {
      perror("sched_getscheduler");
  }
  ```
- **任务诊断**：在调试实时系统时，可以用此函数验证任务是否运行在预期的调度策略下。
- **监控工具**：系统监控工具常用此函数显示任务的调度策略，帮助分析系统调度行为。
- **修改策略**：如果需要修改调度策略，使用 `sched_setscheduler()`。
- **策略名称映射**：可以使用 switch 或数组将返回的整数值映射为策略名称，提高可读性。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 12、sched_yield

```c
int sched_yield(void);
```

主动放弃 CPU，使调用任务重新进入就绪队列，允许调度器选择其他同等或更高优先级的任务运行。这是一种协作式调度机制，用于实现任务间的公平性和响应性。

对于 SCHED_FIFO 策略，任务会被移到其优先级队列的末尾；对于 SCHED_RR 策略，效果类似于时间片到期。这允许相同优先级的任务有机会运行。

**参数**：

无参数。

**返回值**：

- 成功：返回 0（`OK`）
- 失败：返回 -1 并设置 `errno`（通常总是成功）

**注意**：

- **协作式调度**：此函数是协作式多任务的关键，允许任务主动让出 CPU，提高系统整体响应性。
- **不降低优先级**：`sched_yield()` 不改变任务优先级，只是暂时放弃执行权。任务仍然在相同优先级的就绪队列中。
- **策略相关行为**：
  - **SCHED_FIFO**：任务移到其优先级队列的末尾，如果有其他同优先级任务就绪，它们会先运行
  - **SCHED_RR**：类似 SCHED_FIFO，且时间片计数器重置
  - **单任务情况**：如果没有其他同等或更高优先级的就绪任务，调用任务会立即继续运行（yield 无效果）
- **典型用法**：
  ```c
  while (processing) {
      // 处理一批数据
      process_data_chunk();
      
      // 主动让出 CPU，允许其他任务运行
      sched_yield();
  }
  ```
- **提高响应性**：在长时间运行的循环中定期调用 `sched_yield()`，可以避免低优先级任务饿死，提高系统交互性。
- **轮询优化**：在轮询循环中使用 `sched_yield()` 可以减少 CPU 占用，给其他任务更多运行机会：
  ```c
  while (!flag_is_set()) {
      sched_yield();  // 避免空转占用 CPU
  }
  ```
  但通常更好的方案是使用阻塞式等待（如信号量、条件变量）。
- **与 sleep 的区别**：
  - `sched_yield()` 不保证任务会被阻塞，如果没有其他就绪任务，会立即继续运行
  - `sleep()` / `usleep()` 会使任务至少休眠指定时间，期间不消耗 CPU
- **实时系统注意**：在实时系统中，过度使用 `sched_yield()` 可能导致不确定性，应谨慎使用。优先使用显式同步机制（互斥锁、条件变量、信号量）。
- **高优先级任务**：如果调用任务是系统中优先级最高的任务，`sched_yield()` 通常无实际效果（立即返回继续运行）。
- **时间片重置**：对于 SCHED_RR 策略，`sched_yield()` 会重置时间片，相当于任务自愿放弃当前时间片。
- **不可中断**：即使调用 `sched_yield()` 后立即返回，也会发生上下文切换检查，调度器会重新评估调度决策。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 13、sched_get_priority_max

```c
int sched_get_priority_max(int policy);
```

查询指定调度策略允许的最大（highest）优先级值。不同调度策略有不同的优先级范围，此函数用于获取有效的优先级上限，确保设置的优先级值在合法范围内。

在 openvela 中，数值越大表示优先级越高（与 Linux 相同，但与某些 RTOS 相反）。了解优先级范围对于正确配置实时任务至关重要。

**参数**：

- `policy` 调度策略，有效值包括：
  - `SCHED_FIFO` (0)：先进先出实时调度
  - `SCHED_RR` (1)：轮转实时调度
  - `SCHED_SPORADIC` (2)：零星调度（如果支持）
  - `SCHED_OTHER` (3)：标准分时调度
  - 其他系统支持的策略

**返回值**：

- 成功：返回指定策略的最大优先级值（正整数，通常为 255）
- 失败：返回 -1 并设置 `errno`：
  - `EINVAL`：`policy` 参数无效或不支持

**注意**：

- **配合使用**：通常与 `sched_get_priority_min()` 配合使用，获取完整的优先级范围：
  ```c
  int min_prio = sched_get_priority_min(SCHED_FIFO);
  int max_prio = sched_get_priority_max(SCHED_FIFO);
  printf("SCHED_FIFO priority range: %d to %d\n", min_prio, max_prio);
  ```
- **openvela 默认范围**：在 openvela 中，大多数策略的优先级范围通常为 1 到 255，其中：
  - 1：最低优先级（通常是 IDLE 任务）
  - 255：最高优先级（紧急实时任务）
  - 100-200：典型应用任务优先级范围
- **策略无关性**：在 openvela 中，通常所有实时策略（SCHED_FIFO、SCHED_RR、SCHED_SPORADIC）共享相同的优先级空间，因此最大值相同。
- **参数验证**：在调用 `sched_setparam()` 或 `sched_setscheduler()` 前，使用此函数验证优先级是否在有效范围内，避免 `EINVAL` 错误：
  ```c
  int new_priority = 200;
  if (new_priority <= sched_get_priority_max(SCHED_FIFO)) {
      struct sched_param param = {.sched_priority = new_priority};
      sched_setscheduler(0, SCHED_FIFO, &param);
  }
  ```
- **可移植性**：不同操作系统的优先级范围可能不同，使用此函数可以编写可移植的代码，避免硬编码优先级值。
- **典型用法**：
  ```c
  int max = sched_get_priority_max(SCHED_FIFO);
  if (max < 0) {
      perror("sched_get_priority_max");
  } else {
      printf("Max priority for SCHED_FIFO: %d\n", max);
  }
  ```
- **实时任务配置**：在配置关键实时任务时，通常使用接近最大值的优先级，以确保任务能抢占其他任务。
- **优先级分层**：在复杂系统中，可以将优先级范围分为几个层次（如系统层、驱动层、应用层），每层使用不同的优先级子范围。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 14、sched_get_priority_min

```c
int sched_get_priority_min(int policy);
```

查询指定调度策略允许的最小（lowest）优先级值。不同调度策略有不同的优先级范围，此函数用于获取有效的优先级下限，确保设置的优先级值在合法范围内。

在 openvela 中，数值越小表示优先级越低。最小优先级通常留给后台任务或空闲任务使用。

**参数**：

- `policy` 调度策略，有效值包括：
  - `SCHED_FIFO` (0)：先进先出实时调度
  - `SCHED_RR` (1)：轮转实时调度
  - `SCHED_SPORADIC` (2)：零星调度（如果支持）
  - `SCHED_OTHER` (3)：标准分时调度
  - 其他系统支持的策略

**返回值**：

- 成功：返回指定策略的最小优先级值（正整数，通常为 1）
- 失败：返回 -1 并设置 `errno`：
  - `EINVAL`：`policy` 参数无效或不支持

**注意**：

- **配合使用**：通常与 `sched_get_priority_max()` 配合使用，获取完整的优先级范围：
  ```c
  int min_prio = sched_get_priority_min(SCHED_RR);
  int max_prio = sched_get_priority_max(SCHED_RR);
  printf("SCHED_RR priority range: [%d, %d]\n", min_prio, max_prio);
  ```
- **openvela 默认值**：在 openvela 中，最小优先级通常为 1（优先级 0 有时保留给系统或特殊用途）。
- **IDLE 任务**：系统空闲任务（IDLE task）通常运行在最小优先级，仅在没有其他任务就绪时运行。
- **后台任务**：低优先级后台任务（如日志记录、统计）通常使用接近最小值的优先级，避免影响前台任务。
- **参数验证**：在设置优先级前，使用此函数验证优先级是否在有效范围内：
  ```c
  int new_priority = 5;
  if (new_priority >= sched_get_priority_min(SCHED_FIFO) &&
      new_priority <= sched_get_priority_max(SCHED_FIFO)) {
      struct sched_param param = {.sched_priority = new_priority};
      sched_setparam(0, &param);
  }
  ```
- **可移植性**：不同操作系统的优先级范围可能不同，使用此函数可以编写可移植的代码，避免硬编码优先级值。
- **典型用法**：
  ```c
  int min = sched_get_priority_min(SCHED_FIFO);
  if (min < 0) {
      perror("sched_get_priority_min");
  } else {
      printf("Min priority for SCHED_FIFO: %d\n", min);
  }
  ```
- **优先级分配策略**：在设计系统时，应避免使用最小优先级（除非是真正的后台任务），以免任务长时间得不到 CPU 时间。
- **策略无关性**：在 openvela 中，通常所有实时策略共享相同的优先级空间，因此最小值也相同。
- **调试工具**：使用这些函数可以编写通用的优先级检查工具，验证系统中所有任务的优先级配置是否合理。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

**返回值**：

返回指定调度策略的最小优先级值，失败时返回 -1 并设置 `errno`。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 15、sched_rr_get_interval

```c
int sched_rr_get_interval(pid_t pid, struct timespec *interval);
```

查询使用 `SCHED_RR`（轮转）调度策略的任务的时间片长度。时间片是 SCHED_RR 策略中，任务在被强制让出 CPU 前可以连续运行的最大时间。

此函数用于了解系统的调度时间粒度，有助于调优实时应用的性能和响应性。

**参数**：

- `pid` 目标任务的 PID。特殊值 0 表示查询调用任务自身的时间片。必须是有效的任务 PID。
- `interval` 指向 `struct timespec` 结构的指针，用于接收时间片长度。函数会填充此结构：
  - `tv_sec`：秒部分（通常为 0，因为时间片通常小于 1 秒）
  - `tv_nsec`：纳秒部分（例如 10,000,000 纳秒 = 10 毫秒）

**返回值**：

- 成功：返回 0（`OK`），并在 `interval` 中填充时间片长度
- 失败：返回 -1 并设置 `errno`：
  - `ESRCH`：指定的任务不存在（PID 无效或任务已终止）
  - `EINVAL`：`pid` 为负值
  - `EFAULT`：`interval` 指向无效内存（NULL 或不可写）
  - `ENOSYS`：系统不支持此功能（SCHED_RR 未启用）

**注意**：

- **仅适用于 SCHED_RR**：时间片概念仅对 SCHED_RR 策略有意义。对于 SCHED_FIFO，任务运行直到阻塞或被更高优先级任务抢占，没有时间片限制。
- **系统级配置**：时间片长度通常是系统级配置（编译时或启动时设置），不能针对单个任务修改。查询不同任务的时间片通常返回相同的值。
- **典型值**：在 openvela 中，默认时间片通常为 10 毫秒（10,000,000 纳秒），但可以通过配置选项调整（如 `CONFIG_RR_INTERVAL`）。
- **典型用法**：
  ```c
  struct timespec ts;
  if (sched_rr_get_interval(0, &ts) == 0) {
      long ms = ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
      printf("Time slice: %ld ms\n", ms);
  } else {
      perror("sched_rr_get_interval");
  }
  ```
- **性能调优**：了解时间片长度有助于调优任务设计：
  - 如果任务的关键操作时间接近时间片长度，可能需要优化算法或考虑使用 SCHED_FIFO
  - 如果多个同优先级 SCHED_RR 任务需要公平共享 CPU，应确保它们的工作单元小于时间片
- **实时性分析**：时间片是实时系统响应时间分析的重要参数，影响任务的最坏响应时间。
- **时间片耗尽**：当 SCHED_RR 任务的时间片耗尽时，任务被移到其优先级队列末尾，时间片重新计数。
- **调用 sched_yield()**：对于 SCHED_RR 任务，调用 `sched_yield()` 会重置时间片计数器。
- **非 SCHED_RR 任务**：即使任务当前不是 SCHED_RR 策略，此函数通常也会成功返回系统默认的时间片值，但此值对非 SCHED_RR 任务无实际意义。

**POSIX 兼容性**：完美兼容 `POSIX` 同名接口。

## 16、sched_getcpu

```c
int sched_getcpu(void);
```

获取调用任务当前正在其上运行的 CPU 核心编号。此函数仅在 SMP（对称多处理）系统中有意义，用于查询任务与 CPU 的绑定关系。

在多核系统中，了解任务运行在哪个 CPU 上，有助于性能分析、调试和优化 CPU 亲和性策略。

**参数**：

无参数。

**返回值**：

- 成功：返回当前运行的 CPU 编号（非负整数，从 0 开始编号）
  - 0：第一个 CPU 核心
  - 1：第二个 CPU 核心
  - ...依此类推
- 失败：返回 -1 并设置 `errno`（通常不会失败）
  - `ENOSYS`：系统不支持 SMP（未启用 `CONFIG_SMP`）

**注意**：

- **SMP 系统专用**：此函数仅在启用 `CONFIG_SMP` 配置的多核系统中有效。在单核系统中，通常总是返回 0。
- **瞬时值**：返回的 CPU 编号是查询时的瞬时值。在抢占式多任务系统中，任务可能在函数返回后立即被迁移到其他 CPU。
- **典型用法**：
  ```c
  int cpu = sched_getcpu();
  if (cpu >= 0) {
      printf("Running on CPU %d\n", cpu);
  } else {
      perror("sched_getcpu");
  }
  ```
- **性能分析**：在性能分析工具中，记录任务运行的 CPU 有助于分析 CPU 负载分布和任务迁移频率。
- **调试工具**：在调试 CPU 亲和性问题时，可以定期查询 CPU 编号，验证任务是否运行在预期的 CPU 上。
- **配合亲和性**：通常与 `sched_setaffinity()` 和 `sched_getaffinity()` 配合使用：
  ```c
  cpu_set_t set;
  CPU_ZERO(&set);
  CPU_SET(2, &set);  // 绑定到 CPU 2
  sched_setaffinity(0, sizeof(set), &set);
  
  int cpu = sched_getcpu();
  assert(cpu == 2);  // 验证绑定成功
  ```
- **不可靠用于同步**：不应依赖此函数实现同步机制，因为返回值可能在使用前失效。
- **NUMA 系统**：在 NUMA（非统一内存访问）架构中，了解任务运行的 CPU 有助于优化内存访问模式，减少跨节点内存访问。
- **热点分析**：如果多个任务频繁运行在同一 CPU，可能表明负载不均衡，需要调整亲和性或优先级。
- **中断上下文**：此函数也可以在中断处理程序中调用，查询中断在哪个 CPU 上被处理。
- **与线程绑定**：在多线程应用中，可以将不同线程绑定到不同 CPU，然后用此函数验证绑定效果。

**POSIX 兼容性**：兼容 Linux 扩展接口（非 POSIX 标准，但广泛支持）。

## 17、sched_setaffinity

```c
int sched_setaffinity(pid_t pid, size_t cpusetsize, const cpu_set_t *mask);
```

设置任务的 CPU 亲和性掩码（affinity mask），指定任务允许运行的 CPU 核心集合。此功能仅在 SMP（对称多处理）系统中有效，需要启用 `CONFIG_SMP` 配置。

CPU 亲和性允许将任务绑定到特定的 CPU 核心，这在优化缓存局部性、减少上下文切换开销、隔离关键任务等场景中非常有用。

**参数**：

- `pid` 目标任务的 PID。特殊值 0 表示设置调用任务自身的亲和性。必须是有效的任务 PID。
- `cpusetsize` `mask` 指向的 CPU 集合的大小（字节）。通常使用 `sizeof(cpu_set_t)`。此参数允许未来扩展支持更多 CPU。
- `mask` 指向 CPU 亲和性掩码的指针（`cpu_set_t` 类型）。位图中每一位对应一个 CPU：
  - 位为 1：任务允许在该 CPU 上运行
  - 位为 0：任务不允许在该 CPU 上运行
  使用 `CPU_ZERO()`、`CPU_SET()`、`CPU_CLR()` 等宏操作此掩码

**返回值**：

- 成功：返回 0（`OK`）
- 失败：返回 -1 并设置 `errno`：
  - `ESRCH`：指定的任务不存在（PID 无效或任务已终止）
  - `EINVAL`：`mask` 指定的 CPU 集合无效（例如全为 0，或包含不存在的 CPU）
  - `EFAULT`：`mask` 指向无效内存（NULL 或不可读）
  - `EPERM`：调用者没有权限修改目标任务的亲和性（通常需要超级用户权限或同一用户）
  - `ENOSYS`：系统不支持 SMP（未启用 `CONFIG_SMP`）

**注意**：

- **SMP 系统专用**：此函数仅在多核系统（`CONFIG_SMP` 启用）中有效。单核系统通常返回 `ENOSYS`。
- **立即生效**：亲和性修改立即生效。如果任务当前运行在不在新掩码中的 CPU 上，调度器会立即将其迁移到允许的 CPU 之一。
- **典型用法**：
  ```c
  cpu_set_t set;
  CPU_ZERO(&set);           // 清空掩码
  CPU_SET(0, &set);         // 允许 CPU 0
  CPU_SET(1, &set);         // 允许 CPU 1
  
  if (sched_setaffinity(0, sizeof(set), &set) == 0) {
      printf("Affinity set to CPU 0 and 1\n");
  } else {
      perror("sched_setaffinity");
  }
  ```
- **绑定到单个 CPU**：
  ```c
  cpu_set_t set;
  CPU_ZERO(&set);
  CPU_SET(2, &set);  // 只允许 CPU 2
  sched_setaffinity(0, sizeof(set), &set);
  ```
- **性能优化**：
  - **缓存局部性**：将任务绑定到特定 CPU 可以提高缓存命中率，减少缓存失效
  - **减少迁移开销**：避免任务在 CPU 间频繁迁移，降低上下文切换成本
  - **负载隔离**：将关键实时任务绑定到专用 CPU，避免其他任务干扰
- **NUMA 系统**：在 NUMA 架构中，应将任务绑定到靠近其访问内存的 CPU，减少跨节点内存访问延迟。
- **权限要求**：修改其他任务的亲和性通常需要特权。在嵌入式系统中，这一限制可能较宽松。
- **子任务继承**：子任务（通过 `fork()` 或 `task_create()` 创建）通常继承父任务的 CPU 亲和性。
- **配合使用**：通常与 `sched_getaffinity()` 配合，先查询当前亲和性，修改后设置回去：
  ```c
  cpu_set_t set;
  sched_getaffinity(0, sizeof(set), &set);
  CPU_CLR(3, &set);  // 移除 CPU 3
  sched_setaffinity(0, sizeof(set), &set);
  ```
- **验证设置**：设置后可以用 `sched_getcpu()` 验证任务是否运行在预期的 CPU 上。
- **陷阱**：
  - 如果 `mask` 全为 0（不允许任何 CPU），会返回 `EINVAL`
  - 如果指定的 CPU 超出系统范围（如系统只有 4 核，但设置了 CPU 5），会返回 `EINVAL`
  - 过度绑定可能导致负载不均衡，某些 CPU 过载而其他 CPU 空闲
- **动态调整**：在运行时根据系统负载动态调整亲和性，可以实现灵活的负载均衡策略。

**POSIX 兼容性**：兼容 Linux 扩展接口（非 POSIX 标准，但广泛支持）。

## 18、sched_getaffinity

```c
int sched_getaffinity(pid_t pid, size_t cpusetsize, cpu_set_t *mask);
```

查询任务的 CPU 亲和性掩码（affinity mask），获取任务允许运行的 CPU 核心集合。此功能仅在 SMP（对称多处理）系统中有效，需要启用 `CONFIG_SMP` 配置。

通过查询 CPU 亲和性，可以了解任务的 CPU 绑定策略，用于监控、调试和动态调整亲和性。

**参数**：

- `pid` 目标任务的 PID。特殊值 0 表示查询调用任务自身的亲和性。必须是有效的任务 PID。
- `cpusetsize` `mask` 指向的 CPU 集合的大小（字节）。通常使用 `sizeof(cpu_set_t)`。
- `mask` 指向 CPU 亲和性掩码的指针，用于接收查询结果。函数会填充此 `cpu_set_t` 结构，其中：
  - 位为 1：任务允许在该 CPU 上运行
  - 位为 0：任务不允许在该 CPU 上运行

**返回值**：

- 成功：返回 0（`OK`），并在 `mask` 中填充任务的 CPU 亲和性掩码
- 失败：返回 -1 并设置 `errno`：
  - `ESRCH`：指定的任务不存在（PID 无效或任务已终止）
  - `EINVAL`：`cpusetsize` 过小，无法容纳系统的 CPU 数量
  - `EFAULT`：`mask` 指向无效内存（NULL 或不可写）
  - `ENOSYS`：系统不支持 SMP（未启用 `CONFIG_SMP`）

**注意**：

- **SMP 系统专用**：此函数仅在多核系统（`CONFIG_SMP` 启用）中有效。单核系统通常返回 `ENOSYS`。
- **只读查询**：此函数不修改任务状态，是纯查询操作，开销很小。
- **典型用法**：
  ```c
  cpu_set_t set;
  if (sched_getaffinity(0, sizeof(set), &set) == 0) {
      printf("Task can run on CPUs: ");
      for (int i = 0; i < CPU_SETSIZE; i++) {
          if (CPU_ISSET(i, &set)) {
              printf("%d ", i);
          }
      }
      printf("\n");
  } else {
      perror("sched_getaffinity");
  }
  ```
- **检查特定 CPU**：
  ```c
  cpu_set_t set;
  sched_getaffinity(0, sizeof(set), &set);
  if (CPU_ISSET(2, &set)) {
      printf("Task can run on CPU 2\n");
  }
  ```
- **修改前查询**：在修改亲和性前，通常先查询当前亲和性，然后基于当前值进行修改：
  ```c
  cpu_set_t set;
  sched_getaffinity(0, sizeof(set), &set);
  CPU_CLR(1, &set);  // 移除 CPU 1
  sched_setaffinity(0, sizeof(set), &set);
  ```
- **监控工具**：系统监控工具常用此函数显示任务的 CPU 绑定情况，帮助分析负载分布。
- **调试亲和性问题**：如果任务性能异常，可以查询亲和性，检查是否被意外绑定到负载过重的 CPU。
- **统计 CPU 数量**：
  ```c
  cpu_set_t set;
  sched_getaffinity(0, sizeof(set), &set);
  int count = CPU_COUNT(&set);
  printf("Task can run on %d CPUs\n", count);
  ```
- **默认亲和性**：新创建的任务默认可以运行在所有 CPU 上（除非父任务有限制）。查询时会看到所有 CPU 位都为 1。
- **CPU_SETSIZE 常量**：`CPU_SETSIZE` 定义了 `cpu_set_t` 支持的最大 CPU 数量（通常为 1024），但实际系统 CPU 数量可能更少。
- **CPU 集合操作宏**：
  - `CPU_ZERO(&set)`：清空集合
  - `CPU_SET(cpu, &set)`：添加 CPU
  - `CPU_CLR(cpu, &set)`：移除 CPU
  - `CPU_ISSET(cpu, &set)`：检查 CPU 是否在集合中
  - `CPU_COUNT(&set)`：统计集合中的 CPU 数量
  - `CPU_EQUAL(&set1, &set2)`：比较两个集合是否相等
- **可移植性**：不同系统的 `cpu_set_t` 大小可能不同，始终使用 `sizeof(cpu_set_t)` 而不是硬编码大小。
- **与 getcpu 配合**：
  ```c
  int cpu = sched_getcpu();
  cpu_set_t set;
  sched_getaffinity(0, sizeof(set), &set);
  assert(CPU_ISSET(cpu, &set));  // 当前 CPU 应该在亲和性集合中
  ```

**POSIX 兼容性**：兼容 Linux 扩展接口（非 POSIX 标准，但广泛支持）。

