# 信号机制

`Vela` 提供完整的 `POSIX` 信号机制，用于进程和线程间的异步通信和事件通知。信号是一种软件中断机制，允许内核或其他进程向目标进程发送异步通知，通知其发生了特定事件。

## 信号概述

信号是 Unix/Linux 系统中最古老的进程间通信（IPC）机制之一。当信号被发送给进程时，进程的正常执行流程会被中断，转而执行信号处理函数（signal handler）。信号处理完成后，进程恢复到被中断的位置继续执行，除非信号的默认动作是终止进程。

### 信号类型

`Vela` 支持两类信号：

1. **标准信号**（信号 1-31）：传统的 POSIX 信号，如 `SIGINT`、`SIGTERM`、`SIGKILL`、`SIGCHLD` 等。
   - 不排队：同一信号发送多次，可能只递送一次
   - 不携带额外数据
   - 大多数有预定义的默认动作

2. **实时信号**（`SIGRTMIN`=32 到 `SIGRTMAX`=63）：POSIX.1b 实时扩展引入的信号。
   - 支持排队：多次发送会排队等待递送
   - 可携带附加数据（整数或指针）
   - 按 FIFO 顺序递送
   - 默认动作是忽略

### 信号处理方式

进程对信号可以采取三种处理方式：

1. **忽略信号**（`SIG_IGN`）：信号被丢弃，不产生任何影响。`SIGKILL` 和 `SIGSTOP` 不能被忽略。
2. **默认处理**（`SIG_DFL`）：执行信号的默认动作，通常是终止进程、忽略或停止进程。在 Vela 中，大多数信号的默认动作是忽略（除非启用了相应的配置选项）。
3. **自定义处理**：注册信号处理函数，在信号到达时执行用户定义的代码。

### 信号掩码和阻塞

每个线程都有自己的信号掩码（signal mask），用于指定哪些信号当前被阻塞。被阻塞的信号不会被递送，而是保持挂起状态（pending），直到解除阻塞。这允许临界区代码暂时屏蔽信号，避免被中断。

### 应用场景

信号常用于以下场景：

- **进程控制**：终止、暂停、继续进程（`SIGTERM`、`SIGKILL`、`SIGSTOP`、`SIGCONT`）
- **错误通知**：硬件异常、非法操作（`SIGSEGV`、`SIGFPE`、`SIGILL`）
- **定时器通知**：定时器到期（`SIGALRM`）
- **异步 I/O 通知**：数据就绪通知（`SIGIO`、`SIGPOLL`）
- **子进程状态变化**：子进程终止或停止（`SIGCHLD`）
- **用户自定义事件**：应用程序特定的通知（`SIGUSR1`、`SIGUSR2`、实时信号）

`Vela` 信号机制支持以下 API：

- `kill()`
- `raise()`
- `sigaction()`
- `sigprocmask()`
- `sigpending()`
- `sigsuspend()`
- `sigwait()`
- `sigwaitinfo()`
- `sigtimedwait()`
- `sigqueue()`
- `sigemptyset()`
- `sigfillset()`
- `sigaddset()`
- `sigdelset()`
- `sigismember()`
- `signal()`
- `sigaltstack()`
- `pthread_kill()`
- `pthread_sigmask()`

## kill

```c
int kill(pid_t pid, int signo);
```

向指定进程或进程组发送信号。这是最基本和常用的信号发送函数，可用于进程间通信、进程控制和事件通知。

`kill()` 的名称源于历史原因，但它不仅用于"杀死"进程，也可以发送任意信号进行通信。信号 0 是特殊的"空信号"，不会实际发送，但会执行错误检查，可用于测试进程是否存在。

*参数*：

- `pid` 目标进程或进程组的标识。取值含义：
  - `> 0`：向指定 PID 的进程发送信号。
  - `0`：向调用进程所在进程组的所有进程发送信号（广播）。
  - `-1`：向所有有权限发送信号的进程发送信号（除了 init 和自己），需要超级用户权限。这是一种系统级广播。
  - `< -1`：向进程组 ID 为 `|pid|`（绝对值）的所有进程发送信号。例如 `kill(-100, SIGTERM)` 向进程组 100 发送 SIGTERM。
- `signo` 要发送的信号编号（1-63）。有效信号定义在 `<signal.h>` 中（如 `SIGTERM`、`SIGKILL`）。特殊值 0 表示"空信号"，不发送实际信号，仅执行错误检查（用于检测进程是否存在）。

*返回值*：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EINVAL` 信号编号无效（小于 0 或大于 `MAX_SIGNO`）。
- `ESRCH` 指定的进程或进程组不存在，或进程已终止。
- `EPERM` 调用进程没有权限向目标进程发送信号。通常只能向同一用户的进程或子进程发送信号。

*注意*：

- `SIGKILL`（信号 9）和 `SIGSTOP`（信号 19）是特殊信号，无法被捕获、阻塞或忽略，保证能终止或停止目标进程。
- 发送信号只是一个请求，目标进程可能忽略信号（如果信号处理设置为 `SIG_IGN`）或阻塞信号。
- 信号可能不会立即递送，如果目标进程阻塞了该信号，信号会挂起直到解除阻塞。
- 在多线程程序中，信号被递送到进程中的某个未阻塞该信号的线程（由系统选择）。要向特定线程发送信号，使用 `pthread_kill()` 或 `tgkill()`。
- 使用 `kill(pid, 0)` 可以测试进程是否存在：如果返回 0，进程存在；如果返回 -1 且 `errno` 为 `ESRCH`，进程不存在。
- 向进程组发送信号时，如果进程组为空或所有进程都无权访问，会返回 `ESRCH` 错误。
- 某些信号有特殊的语义，例如 `SIGCHLD` 通知父进程子进程状态变化，`SIGPIPE` 在向已关闭的管道写入时产生。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## killpg

```c
int killpg(pid_t pgrp, int signo);
```

向指定进程组的所有进程发送信号。等效于 `kill(-pgrp, signo)`。

*参数*：

- `pgrp` 目标进程组 ID。如果为 0，则向调用进程所在的进程组发送信号。
- `signo` 要发送的信号编号。

*返回值*：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EINVAL` 信号编号无效。
- `ESRCH` 指定的进程组不存在。
- `EPERM` 没有权限向目标进程组发送信号。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## tgkill

```c
int tgkill(pid_t pid, pid_t tid, int signo);
```

向指定线程组（进程）中的特定线程发送信号。这是向多线程程序中的特定线程发送信号的最安全方式。

*参数*：

- `pid` 目标进程（线程组）ID。如果为 -1，则忽略此参数，仅根据 `tid` 查找目标线程。
- `tid` 目标线程 ID。
- `signo` 要发送的信号编号。

*返回值*：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EINVAL` 信号编号无效。
- `ESRCH` 线程不存在或不属于指定进程。
- `EPERM` 没有权限向目标线程发送信号。

*注意*：

- 比 `pthread_kill()` 更安全，因为可以验证线程属于预期的进程。
- 避免了线程 ID 被回收后误发信号的问题。

*`POSIX` 兼容性*：兼容 Linux 扩展接口。

## raise

```c
int raise(int signo);
```

向调用线程自身发送信号。这是进程或线程自我发送信号的标准方法，等效于：
- 单线程程序：`kill(getpid(), signo)`
- 多线程程序：`pthread_kill(pthread_self(), signo)`

`raise()` 常用于程序主动触发信号处理，如自我终止、触发断点、或测试信号处理器。

*参数*：

- `signo` 要发送的信号编号（1-63）。常用值包括：
  - `SIGABRT`：异常终止（如 `abort()` 调用）
  - `SIGTERM`：请求终止
  - `SIGUSR1`/`SIGUSR2`：用户自定义信号
  - `SIGTRAP`：触发调试器断点

*返回值*：

成功时返回 0，失败时返回非零值。

*注意*：

- 如果信号的处理动作是终止进程（如 `SIGTERM` 的默认动作，如果启用），`raise()` 不会返回，进程直接终止。
- 信号会立即被处理（如果未阻塞）或挂起（如果被阻塞），然后函数返回。
- 如果信号被阻塞，信号会挂起直到解除阻塞，此时 `raise()` 已经返回。
- 在信号处理函数内调用 `raise()` 发送当前信号可能导致递归，除非设置了 `SA_NODEFER` 标志。
- `raise()` 是线程安全的，在多线程程序中只影响调用线程。
- 相比 `kill(getpid(), signo)`，`raise()` 更高效且语义更清晰。
- 常见用法：
  - `raise(SIGABRT)` - 异常终止程序（等效于 `abort()`）
  - `raise(SIGTERM)` - 自我终止
  - `raise(SIGUSR1)` - 触发用户定义的信号处理

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigaction

```c
int sigaction(int signo, const struct sigaction *act, struct sigaction *oact);
```

设置或查询信号的处理动作。这是设置信号处理器的首选方法，比 `signal()` 提供更多控制和更可预测的行为。`sigaction()` 是 POSIX 标准推荐的信号处理接口。

`struct sigaction` 结构允许精确控制信号处理行为，包括处理函数、信号掩码、各种标志等。这比简单的 `signal()` 接口更强大和灵活。

*参数*：

- `signo` 要设置的信号编号（1-63）。不能是 `SIGKILL`（9）或 `SIGSTOP`（19），因为这两个信号的处理动作不能被修改。
- `act` 指向新的信号处理动作结构。如果为 `NULL`，则不修改当前处理动作，仅通过 `oact` 查询。结构字段：
  - `sa_handler` 或 `sa_sigaction`：信号处理函数
    - `SIG_DFL`：恢复默认处理动作
    - `SIG_IGN`：忽略该信号
    - 函数指针：自定义处理函数
  - `sa_mask`：信号掩码，指定在执行处理函数期间要额外阻塞的信号集。处理的信号本身会自动阻塞（除非设置 `SA_NODEFER`）。
  - `sa_flags`：控制信号处理行为的标志（见下文）
- `oact` 指向保存旧处理动作的结构。如果为 `NULL`，则不返回旧动作。可用于保存并稍后恢复原处理动作。

**`sa_flags` 标志说明**：

- `SA_SIGINFO` (0x02)：使用扩展的三参数处理函数 `sa_sigaction(int sig, siginfo_t *info, void *context)`，而不是简单的 `sa_handler(int sig)`。这允许获取信号的详细信息（发送者 PID、信号值等）。
- `SA_RESTART` (0x10)：被信号中断的系统调用自动重启，而不是返回 `EINTR` 错误。这简化了错误处理，避免需要手动重试中断的系统调用。
- `SA_NODEFER` (0x20)：不自动阻塞正在处理的信号。默认情况下，处理信号 X 时会阻塞信号 X，防止递归。设置此标志后允许信号处理函数递归调用。
- `SA_RESETHAND` (0x40)：信号递送后自动重置处理动作为 `SIG_DFL`（一次性处理器）。类似于旧的不可靠信号语义。
- `SA_ONSTACK` (0x08)：在备用信号栈上执行处理函数（需要先用 `sigaltstack()` 设置）。用于避免栈溢出信号处理器自身溢出栈。
- `SA_NOCLDSTOP` (0x01)：如果 `signo` 是 `SIGCHLD`，则子进程停止（`SIGSTOP`）或继续（`SIGCONT`）时不产生信号，只在终止时产生。
- `SA_NOCLDWAIT` (0x04)：如果 `signo` 是 `SIGCHLD`，子进程终止时自动回收，不产生僵尸进程，父进程无需调用 `wait()`。

*返回值*：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EINVAL` `signo` 无效，或尝试修改 `SIGKILL`/`SIGSTOP` 的处理动作。
- `EFAULT` `act` 或 `oact` 指向无效内存地址（段错误）。

*注意*：

- 信号处理函数应尽量简短和高效，避免调用不可重入函数（如 `malloc()`、`printf()`）。只应调用异步信号安全（async-signal-safe）的函数。
- `sa_mask` 在处理函数执行期间生效，处理函数返回后自动恢复原信号掩码。
- 多次调用 `sigaction()` 修改同一信号的处理动作是安全的，新动作会覆盖旧动作。
- 如果需要临时修改并恢复信号处理，模式为：
  ```c
  struct sigaction old_act;
  sigaction(SIGINT, &new_act, &old_act);  // 设置新处理
  // ... 做某些操作 ...
  sigaction(SIGINT, &old_act, NULL);       // 恢复旧处理
  ```
- 在信号处理函数中修改全局变量时，应将其声明为 `volatile sig_atomic_t` 类型，确保原子性和可见性。
- 使用 `SA_SIGINFO` 标志可以获取信号的详细信息，如发送者 PID、信号携带的数据等，这对于调试和高级信号处理很有用。
- `sa_mask` 中应包含所有在处理函数执行期间需要阻塞的信号，防止信号处理函数被其他信号中断导致的竞态条件。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## signal

```c
sighandler_t signal(int signo, sighandler_t handler);
```

设置信号的处理函数。这是 `sigaction()` 的简化版本，但行为在不同系统上可能有差异，建议使用 `sigaction()`。

*参数*：

- `signo` 信号编号。不能是 `SIGKILL` 或 `SIGSTOP`。
- `handler` 信号处理函数：
  - `SIG_IGN` 忽略该信号。
  - `SIG_DFL` 使用默认处理动作。
  - 用户定义的函数指针，原型为 `void handler(int signo)`。

*返回值*：

成功时返回之前的信号处理函数，失败时返回 `SIG_ERR` 并设置 `errno`。

*注意*：

- 信号处理函数应尽量简短，只调用异步信号安全的函数。
- 在 `Vela` 中，`signal()` 的行为与 BSD 语义一致：信号处理后不会重置为默认，系统调用会自动重启。
- 对于需要精确控制信号行为的场景，建议使用 `sigaction()`。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigprocmask

```c
int sigprocmask(int how, const sigset_t *set, sigset_t *oset);
```

设置或查询调用线程的信号掩码（signal mask）。信号掩码决定哪些信号当前被阻塞。被阻塞的信号不会被递送给进程，而是保持挂起状态（pending），直到从信号掩码中移除（解除阻塞）。

信号掩码是线程局部的，每个线程维护自己独立的信号掩码。新创建的线程继承创建者的信号掩码。阻塞信号可以保护临界区代码不被信号中断，是编写健壮信号处理代码的重要工具。

*参数*：

- `how` 指定如何修改信号掩码，必须是以下值之一：
  - `SIG_BLOCK` (1)：将 `set` 中的信号添加到当前掩码。新掩码 = 旧掩码 ∪ `set`。用于阻塞更多信号。
  - `SIG_UNBLOCK` (2)：从当前掩码中移除 `set` 中的信号。新掩码 = 旧掩码 - `set`。用于解除阻塞。
  - `SIG_SETMASK` (3)：将当前掩码完全替换为 `set`。新掩码 = `set`。用于设置精确的信号掩码。
- `set` 要操作的信号集。如果为 `NULL`，则不修改当前掩码，仅通过 `oset` 查询当前掩码（此时 `how` 参数被忽略）。信号集应先用 `sigemptyset()`、`sigfillset()`、`sigaddset()` 等函数初始化和设置。
- `oset` 如果非 `NULL`，返回操作前的信号掩码（旧值）。可用于保存当前掩码以便稍后恢复。如果只想查询不修改，可设置 `set=NULL`。

*返回值*：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EINVAL` `how` 参数值无效（不是 `SIG_BLOCK`、`SIG_UNBLOCK` 或 `SIG_SETMASK`）。
- `EFAULT` `set` 或 `oset` 指向无效内存地址。

*注意*：

- `SIGKILL`（9）和 `SIGSTOP`（19）无法被阻塞，尝试阻塞它们会被静默忽略（不返回错误）。这确保进程始终可以被终止或停止。
- 在多线程程序中，每个线程有独立的信号掩码，`sigprocmask()` 只影响调用线程。对于多线程程序，POSIX 标准建议使用 `pthread_sigmask()`（功能完全相同，但返回错误码而非设置 `errno`）。
- 解除阻塞信号后，如果该信号处于挂起状态，会立即递送（在 `sigprocmask()` 返回前）。
- 阻塞信号期间，同一信号发送多次只会有一个实例挂起（标准信号不排队）。实时信号（`SIGRTMIN`-`SIGRTMAX`）支持排队。
- 典型使用模式 - 临界区保护：
  ```c
  sigset_t new_mask, old_mask;
  sigemptyset(&new_mask);
  sigaddset(&new_mask, SIGINT);
  sigaddset(&new_mask, SIGTERM);
  
  // 进入临界区，阻塞信号
  sigprocmask(SIG_BLOCK, &new_mask, &old_mask);
  
  // 临界区代码，不会被 SIGINT/SIGTERM 中断
  // ...
  
  // 离开临界区，恢复信号掩码
  sigprocmask(SIG_SETMASK, &old_mask, NULL);
  ```
- 信号掩码在 `fork()` 后被子进程继承，但在 `exec()` 后重置为空（所有信号解除阻塞）。
- 信号掩码不影响信号处理动作的设置，只影响信号的递送。即使信号被阻塞，仍可以用 `sigaction()` 修改其处理动作。
- 可以通过 `sigpending()` 查询当前哪些信号被阻塞且正在挂起。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigpending

```c
int sigpending(sigset_t *set);
```

获取当前被阻塞且正在挂起（待处理）的信号集。这些信号已经被发送给进程，但因为被阻塞而尚未递送。

*参数*：

- `set` 用于返回挂起信号集的指针。

*返回值*：

成功时返回 0，失败时返回 -1 并设置 `errno`。

*注意*：

- 可用于检查在解除阻塞前是否有信号等待处理。
- 配合 `sigismember()` 检查特定信号是否挂起。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigsuspend

```c
int sigsuspend(const sigset_t *mask);
```

临时替换信号掩码并挂起任务，直到收到未被阻塞的信号。这是一个原子操作，避免了分别调用 `sigprocmask()` 和 `pause()` 之间的竞态条件。

*参数*：

- `mask` 临时信号掩码。在等待期间，进程的信号掩码会被替换为此值。

*返回值*：

总是返回 -1，`errno` 设置为 `EINTR`（被信号中断）。

*注意*：

- 函数返回后，信号掩码会自动恢复为调用前的值。
- 常用于等待特定信号，同时不阻塞该信号。
- 示例：解除阻塞 `SIGUSR1` 并等待它：
  ```c
  sigset_t mask;
  sigemptyset(&mask);  // 只解除阻塞 SIGUSR1
  sigsuspend(&mask);   // 等待任意信号
  ```

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigwait

```c
int sigwait(const sigset_t *set, int *sig);
```

同步等待信号集 `set` 中的任意信号到达。这是以同步方式处理信号的关键函数，允许将信号作为普通事件处理，而不是异步中断。

与异步信号处理不同，`sigwait()` 将信号转换为同步事件：线程主动等待信号，信号到达时函数返回信号编号，而不是调用信号处理函数。这大大简化了信号处理，避免了异步信号处理的复杂性（如可重入性、竞态条件等）。

典型用法是创建专门的信号处理线程，阻塞感兴趣的信号，然后循环调用 `sigwait()` 等待并处理信号。

*参数*：

- `set` 要等待的信号集。通常应先使用 `sigprocmask()` 或 `pthread_sigmask()` 阻塞这些信号，否则信号可能被异步处理函数捕获而不是 `sigwait()` 接收。必须包含至少一个有效信号。
- `sig` 返回接收到的信号编号（输出参数）。如果等待多个信号，无法预测哪个信号先到达，需要根据返回的编号进行处理。

*返回值*：

成功时返回 0，失败时返回错误码（注意：不设置 `errno`，直接返回错误码）：

- `EINVAL` `set` 包含无效的信号编号（<= 0 或 > `MAX_SIGNO`）。
- `EINTR` 被未在 `set` 中的信号中断（某些实现，Vela 通常不会返回此错误）。

*注意*：

- **关键**：等待的信号必须被阻塞。否则信号可能在 `sigwait()` 调用前或期间被信号处理函数捕获，导致 `sigwait()` 错过信号。推荐模式：
  ```c
  sigset_t set;
  sigemptyset(&set);
  sigaddset(&set, SIGUSR1);
  sigaddset(&set, SIGUSR2);
  
  // 先阻塞信号
  pthread_sigmask(SIG_BLOCK, &set, NULL);
  
  // 然后等待
  int sig;
  while (1) {
      sigwait(&set, &sig);
      switch (sig) {
          case SIGUSR1: /* 处理 SIGUSR1 */ break;
          case SIGUSR2: /* 处理 SIGUSR2 */ break;
      }
  }
  ```
- `sigwait()` 从挂起信号队列中移除信号，不会触发信号处理函数。即使注册了信号处理函数，`sigwait()` 接收的信号也不会调用处理函数。
- 如果多个线程同时等待同一信号，只有一个线程会接收到信号（由系统选择）。
- 如果信号已经挂起（在调用 `sigwait()` 前到达），函数会立即返回，不会阻塞。
- `sigwait()` 是取消点（cancellation point）：如果线程被取消（`pthread_cancel()`），函数会立即返回。
- 相比异步信号处理，同步等待的优势：
  - 不需要考虑函数可重入性
  - 可以使用普通的 C 库函数（malloc、printf 等）
  - 不需要使用 `volatile sig_atomic_t` 类型
  - 更容易推理和调试
- 常用于实现信号处理线程模式：主线程和工作线程阻塞所有信号，专门的信号线程循环调用 `sigwait()` 处理信号。
- 标准信号不排队，如果同一信号发送多次，可能只有一个实例被 `sigwait()` 接收。实时信号支持排队。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigwaitinfo

```c
int sigwaitinfo(const sigset_t *set, siginfo_t *info);
```

等待 `set` 中的任意信号，并获取信号的详细信息。与 `sigwait()` 类似，但提供更多信号信息。

*参数*：

- `set` 要等待的信号集。
- `info` 如果非 `NULL`，返回信号的详细信息，包括：
  - `si_signo` 信号编号。
  - `si_code` 信号来源代码（如 `SI_USER`、`SI_QUEUE`、`SI_TIMER`）。
  - `si_pid` 发送进程的 PID。
  - `si_value` 随信号传递的数据（用于 `sigqueue()` 发送的信号）。

*返回值*：

成功时返回信号编号，失败时返回 -1 并设置 `errno`。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigtimedwait

```c
int sigtimedwait(const sigset_t *set, siginfo_t *info, const struct timespec *timeout);
```

等待 `set` 中的任意信号，带超时限制。在指定时间内如果没有信号到达，函数返回错误。

*参数*：

- `set` 要等待的信号集。
- `info` 如果非 `NULL`，返回信号的详细信息。
- `timeout` 超时时间：
  - `tv_sec` 秒数。
  - `tv_nsec` 纳秒数。
  - 如果为 `NULL`，则无限等待（等效于 `sigwaitinfo()`）。
  - 如果为 `{0, 0}`，则立即返回（轮询模式）。

*返回值*：

成功时返回信号编号，失败时返回 -1 并设置 `errno`：

- `EAGAIN` 超时时间内没有信号到达。
- `EINTR` 被其他（未在 `set` 中的）信号中断。
- `EINVAL` `timeout` 参数无效（如负值）。

*注意*：

- 常用于实现有超时的信号等待逻辑。
- 结合实时信号使用，可以实现可靠的事件通知机制。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigqueue

```c
int sigqueue(int pid, int signo, const union sigval value);
```

向指定进程发送带数据的信号。这是 `kill()` 的增强版本，支持随信号传递额外的数据（整数或指针），主要用于实时信号和需要携带数据的通信场景。

与 `kill()` 的关键区别：
1. **携带数据**：可以通过 `value` 传递一个整数或指针给接收进程
2. **支持排队**：实时信号会排队，多次发送会排队等待递送
3. **更详细的信息**：接收方可以通过 `siginfo_t` 获取信号来源和携带的数据

`sigqueue()` 常用于实时信号通信、事件通知、异步 I/O 完成通知等需要携带额外信息的场景。

*参数*：

- `pid` 目标进程 ID。必须 > 0，不支持进程组（不能使用 0 或负值）。
- `signo` 要发送的信号编号（1-63）。虽然标准信号也可以使用，但建议使用实时信号（`SIGRTMIN` 到 `SIGRTMAX`），因为：
  - 实时信号支持排队（多次发送都会递送）
  - 标准信号不排队（多次发送可能只递送一次）
  - 实时信号按 FIFO 顺序递送
- `value` 随信号传递的数据，`union sigval` 类型包含两个成员（只能使用其中一个）：
  - `sival_int`：传递整数值，如错误码、序列号、计数器等
  - `sival_ptr`：传递指针值，注意指针在接收进程中可能无效（除非是共享内存地址）

*返回值*：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EINVAL` 信号编号无效（<= 0 或 > `MAX_SIGNO`）。
- `ESRCH` 指定的进程不存在或已终止。
- `EPERM` 调用进程没有权限向目标进程发送信号（不同用户、不同会话等）。
- `EAGAIN` 信号排队资源耗尽。系统对每个进程的挂起信号数有限制（通常数百个），超过限制会返回此错误。这主要影响实时信号。

*注意*：

- **实时信号排队**：实时信号（`SIGRTMIN`-`SIGRTMAX`）支持排队，同一信号发送多次会排队等待递送，不会丢失。每个信号实例都携带独立的 `value`。
- **标准信号不排队**：标准信号（如 `SIGUSR1`、`SIGTERM`）不排队，多次发送可能只递送一次，后续的 `value` 可能丢失。
- **接收数据**：接收方需要使用以下方式获取 `value`：
  - 使用 `sigaction()` 设置处理函数时，设置 `SA_SIGINFO` 标志，使用三参数处理函数：
    ```c
    void handler(int sig, siginfo_t *info, void *context) {
        int data = info->si_value.sival_int;
        // 或 void *ptr = info->si_value.sival_ptr;
    }
    ```
  - 或使用 `sigwaitinfo()`/`sigtimedwait()` 同步等待信号并获取 `siginfo_t`
- **指针参数注意**：`sival_ptr` 在跨进程时通常无效，因为不同进程有独立的地址空间。只有在以下情况下才有意义：
  - 共享内存地址
  - 传递给同一进程的其他线程（使用 `pthread_sigqueue()`，如果可用）
  - 传递的不是真实指针，而是编码的整数值
- **排队限制**：系统对挂起信号数有限制（`SIGQUEUE_MAX`），可以通过 `sysconf(_SC_SIGQUEUE_MAX)` 查询。超过限制会返回 `EAGAIN`。
- **信号优先级**：实时信号有隐含的优先级，编号小的优先递送。`SIGRTMIN` 优先级最高，`SIGRTMAX` 最低。
- **典型用法**：
  ```c
  // 发送方
  union sigval val;
  val.sival_int = 42;  // 或任何数据
  sigqueue(target_pid, SIGRTMIN, val);
  
  // 接收方
  struct sigaction sa;
  sa.sa_flags = SA_SIGINFO;
  sa.sa_sigaction = handler;
  sigemptyset(&sa.sa_mask);
  sigaction(SIGRTMIN, &sa, NULL);
  ```
- **与 `kill()` 的选择**：
  - 如果不需要携带数据且使用标准信号，用 `kill()` 更简单
  - 如果需要携带数据或使用实时信号，用 `sigqueue()`
- `sigqueue()` 设置 `siginfo_t` 的 `si_code` 为 `SI_QUEUE`，可用于区分信号来源。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigemptyset

```c
int sigemptyset(sigset_t *set);
```

初始化信号集为空集（不包含任何信号）。这是使用信号集之前必须执行的初始化操作。未初始化的信号集内容不确定，直接使用会导致未定义行为。

初始化为空集后，可以使用 `sigaddset()` 逐个添加需要的信号，构建自定义信号集。

*参数*：

- `set` 指向要初始化的信号集。必须是已分配的 `sigset_t` 变量（自动变量、静态变量或动态分配）。

*返回值*：

成功时返回 0。按照 POSIX 标准，此函数总是成功，但某些实现在参数无效时可能返回 -1。

*注意*：

- **必须初始化**：所有信号集在使用前必须调用 `sigemptyset()` 或 `sigfillset()` 初始化。不要假设新分配的信号集是空的，自动变量的初始值不确定。
- 初始化后的空集不包含任何信号，所有信号的成员测试（`sigismember()`）都返回 0。
- 典型用法模式：
  ```c
  sigset_t set;
  sigemptyset(&set);           // 初始化为空
  sigaddset(&set, SIGINT);     // 添加 SIGINT
  sigaddset(&set, SIGTERM);    // 添加 SIGTERM
  // 现在 set 包含 SIGINT 和 SIGTERM
  ```
- 空集常用于 `sigprocmask(SIG_SETMASK, &empty_set, ...)` 解除所有信号的阻塞。
- 即使信号集已经初始化，也可以再次调用 `sigemptyset()` 清空它。
- 与 `sigfillset()` 配合：`sigemptyset()` + `sigaddset()` 用于构建稀疏信号集（包含少数信号），`sigfillset()` + `sigdelset()` 用于构建稠密信号集（排除少数信号）。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigfillset

```c
int sigfillset(sigset_t *set);
```

初始化信号集为满集（包含所有有效信号）。初始化后，信号集包含系统支持的所有信号（1 到 `MAX_SIGNO`，即 1-63）。

满集常用于需要阻塞所有信号的场景，或作为起点，再用 `sigdelset()` 移除不需要阻塞的信号。

*参数*：

- `set` 指向要初始化的信号集。

*返回值*：

成功时返回 0。按照 POSIX 标准，此函数总是成功，但某些实现在参数无效时可能返回 -1。

*注意*：

- 初始化后的满集包含所有信号（包括 `SIGKILL` 和 `SIGSTOP`），但注意 `SIGKILL` 和 `SIGSTOP` 即使在信号集中也无法被实际阻塞。
- 满集中包含的信号数量取决于系统，在 Vela 中是 63 个（`MIN_SIGNO=1` 到 `MAX_SIGNO=63`）。
- 典型用法模式：
  ```c
  sigset_t set;
  sigfillset(&set);             // 初始化为满集
  sigdelset(&set, SIGUSR1);     // 移除 SIGUSR1
  sigdelset(&set, SIGUSR2);     // 移除 SIGUSR2
  sigprocmask(SIG_SETMASK, &set, NULL);  // 阻塞除 SIGUSR1/SIGUSR2 外的所有信号
  ```
- 常见应用：
  - 阻塞所有信号保护临界区：`sigfillset(&set); sigprocmask(SIG_BLOCK, &set, ...);`
  - 在 `sigaction()` 的 `sa_mask` 中使用，在处理信号期间阻塞所有其他信号
  - 创建"反向"信号集：先填满，再移除不需要的信号
- 与 `sigemptyset()` 的选择：
  - 如果需要包含少数信号，用 `sigemptyset()` + `sigaddset()`
  - 如果需要排除少数信号，用 `sigfillset()` + `sigdelset()`
- 即使信号集已经初始化，也可以再次调用 `sigfillset()` 重新填充。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigaddset

```c
int sigaddset(sigset_t *set, int signo);
```

将指定信号添加到信号集中。如果信号已在集合中，操作无影响（幂等操作）。

这是构建自定义信号集的基本操作，通常在 `sigemptyset()` 初始化后使用，逐个添加需要的信号。

*参数*：

- `set` 指向要修改的信号集。必须已用 `sigemptyset()` 或 `sigfillset()` 初始化。
- `signo` 要添加的信号编号（1-63）。必须是有效的信号编号，无效值会导致未定义行为或返回错误。

*返回值*：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EINVAL` `signo` 不是有效的信号编号（<= 0 或 > `MAX_SIGNO`）。

*注意*：

- 必须在已初始化的信号集上操作，否则行为未定义。
- 添加已存在的信号不会产生错误或副作用。
- 可以多次调用添加多个信号：
  ```c
  sigset_t set;
  sigemptyset(&set);
  sigaddset(&set, SIGINT);
  sigaddset(&set, SIGTERM);
  sigaddset(&set, SIGUSR1);
  ```
- 可以添加 `SIGKILL` 和 `SIGSTOP` 到信号集，但在实际使用时（如 `sigprocmask()`），这两个信号会被忽略。
- 常见用途：
  - 构建要阻塞的信号掩码
  - 指定 `sigwait()` 等待的信号集
  - 设置 `sigaction()` 的 `sa_mask`
- 与 `sigdelset()` 配对使用可以灵活操作信号集。
- 可以使用 `sigismember()` 检查信号是否在集合中。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigdelset

```c
int sigdelset(sigset_t *set, int signo);
```

从信号集中移除指定信号。如果信号不在集合中，操作无影响（幂等操作）。

这通常与 `sigfillset()` 配合使用，先填充所有信号，再移除不需要的信号，构建"排除型"信号集。

*参数*：

- `set` 指向要修改的信号集。必须已用 `sigemptyset()` 或 `sigfillset()` 初始化。
- `signo` 要移除的信号编号（1-63）。必须是有效的信号编号，无效值会导致未定义行为或返回错误。

*返回值*：

成功时返回 0，失败时返回 -1 并设置 `errno`：

- `EINVAL` `signo` 不是有效的信号编号（<= 0 或 > `MAX_SIGNO`）。

*注意*：

- 必须在已初始化的信号集上操作，否则行为未定义。
- 移除不存在的信号不会产生错误或副作用。
- 可以多次调用移除多个信号：
  ```c
  sigset_t set;
  sigfillset(&set);              // 包含所有信号
  sigdelset(&set, SIGINT);       // 移除 SIGINT
  sigdelset(&set, SIGTERM);      // 移除 SIGTERM
  // 现在 set 包含除 SIGINT 和 SIGTERM 外的所有信号
  ```
- 常见用途：
  - 从满集中排除某些信号
  - 修改已有信号集，去除某些信号
  - 精细控制信号掩码
- 与 `sigaddset()` 相反操作，两者可以组合使用灵活操作信号集。
- 移除 `SIGKILL` 或 `SIGSTOP` 不会有实际效果，因为它们本身就无法被阻塞。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigismember

```c
int sigismember(const sigset_t *set, int signo);
```

检查指定信号是否在信号集中。这是查询信号集成员关系的标准方法。

*参数*：

- `set` 指向要查询的信号集。必须已初始化。
- `signo` 要检查的信号编号（1-63）。

*返回值*：

- 返回 1：信号在集合中（是成员）
- 返回 0：信号不在集合中（非成员）
- 返回 -1：失败，`signo` 无效，设置 `errno` 为 `EINVAL`

*注意*：

- 返回值是 1 或 0，而不是非零或零，这与某些布尔函数不同，需要显式检查 1。
- 正确用法：
  ```c
  if (sigismember(&set, SIGINT) == 1) {
      // SIGINT 在集合中
  } else if (sigismember(&set, SIGINT) == 0) {
      // SIGINT 不在集合中
  } else {
      // 错误
  }
  ```
- 简化用法（作为布尔值）：
  ```c
  if (sigismember(&set, SIGINT)) {
      // SIGINT 在集合中（返回 1，真值）
  }
  ```
- 必须在已初始化的信号集上操作，未初始化的信号集返回值不确定。
- 常见用途：
  - 检查信号是否被阻塞（查询 `sigprocmask()` 返回的掩码）
  - 检查信号是否挂起（查询 `sigpending()` 返回的集合）
  - 验证信号集的内容
- 与集合操作配合：
  ```c
  sigset_t set;
  sigemptyset(&set);
  sigaddset(&set, SIGINT);
  assert(sigismember(&set, SIGINT) == 1);
  assert(sigismember(&set, SIGTERM) == 0);
  ```

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## sigisemptyset

```c
int sigisemptyset(sigset_t *set);
```

检查信号集是否为空。

*参数*：

- `set` 信号集。

*返回值*：

如果信号集为空返回 1，否则返回 0。

*`POSIX` 兼容性*：兼容 glibc 扩展接口。

## sigandset

```c
int sigandset(sigset_t *dest, const sigset_t *left, const sigset_t *right);
```

计算两个信号集的交集。

*参数*：

- `dest` 存储结果的信号集。
- `left` 第一个信号集。
- `right` 第二个信号集。

*返回值*：

成功时返回 0，失败时返回 -1。

*`POSIX` 兼容性*：兼容 glibc 扩展接口。

## sigorset

```c
int sigorset(sigset_t *dest, const sigset_t *left, const sigset_t *right);
```

计算两个信号集的并集。

*参数*：

- `dest` 存储结果的信号集。
- `left` 第一个信号集。
- `right` 第二个信号集。

*返回值*：

成功时返回 0，失败时返回 -1。

*`POSIX` 兼容性*：兼容 glibc 扩展接口。

## sighold

```c
int sighold(int signo);
```

将指定信号添加到信号掩码中（阻塞该信号）。

*参数*：

- `signo` 要阻塞的信号编号。

*返回值*：

成功时返回 0，失败时返回 -1。

*`POSIX` 兼容性*：兼容 `POSIX` 同名接口（已过时）。

## sigrelse

```c
int sigrelse(int signo);
```

从信号掩码中移除指定信号（解除阻塞）。

*参数*：

- `signo` 要解除阻塞的信号编号。

*返回值*：

成功时返回 0，失败时返回 -1。

*`POSIX` 兼容性*：兼容 `POSIX` 同名接口（已过时）。

## sigignore

```c
int sigignore(int signo);
```

将指定信号的处理设置为忽略。

*参数*：

- `signo` 要忽略的信号编号。

*返回值*：

成功时返回 0，失败时返回 -1。

*`POSIX` 兼容性*：兼容 `POSIX` 同名接口（已过时）。

## sigset

```c
sighandler_t sigset(int signo, sighandler_t handler);
```

设置信号处理函数（类似 `signal`，但支持 `SIG_HOLD`）。

*参数*：

- `signo` 信号编号。
- `handler` 信号处理函数，可以是 `SIG_IGN`、`SIG_DFL`、`SIG_HOLD` 或用户定义的函数。

*返回值*：

成功时返回之前的信号处理函数，失败时返回 `SIG_ERR`。

*`POSIX` 兼容性*：兼容 `POSIX` 同名接口（已过时）。

## sigpause

```c
int sigpause(int signo);
```

从信号掩码中移除指定信号并挂起任务，直到收到信号。

*参数*：

- `signo` 要解除阻塞的信号编号。

*返回值*：

总是返回 -1，`errno` 设置为 `EINTR`。

*`POSIX` 兼容性*：兼容 `POSIX` 同名接口（已过时）。

## sigaltstack

```c
int sigaltstack(const stack_t *ss, stack_t *oss);
```

设置或获取信号处理的备用栈。

*参数*：

- `ss` 如果非 `NULL`，指向新的备用栈配置：
  - `ss_sp` 栈内存指针。
  - `ss_size` 栈大小。
  - `ss_flags` 标志（`SS_DISABLE` 禁用备用栈）。
- `oss` 如果非 `NULL`，返回之前的备用栈配置。

*返回值*：

成功时返回 0，失败时返回 -1 并设置 `errno`。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## siginterrupt

```c
int siginterrupt(int signo, int flag);
```

设置信号是否中断系统调用。

*参数*：

- `signo` 信号编号。
- `flag` 如果非零，信号将中断系统调用；否则系统调用会自动重启。

*返回值*：

成功时返回 0，失败时返回 -1。

*`POSIX` 兼容性*：兼容 BSD 扩展接口。

## psignal

```c
void psignal(int signo, const char *message);
```

打印信号描述信息。

*参数*：

- `signo` 信号编号。
- `message` 前缀消息。

*返回值*：

无返回值。

*`POSIX` 兼容性*：兼容 BSD 扩展接口。

## psiginfo

```c
void psiginfo(const siginfo_t *info, const char *message);
```

打印信号信息结构的描述。

*参数*：

- `info` 信号信息结构。
- `message` 前缀消息。

*返回值*：

无返回值。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## pthread_kill

```c
int pthread_kill(pthread_t thread, int signo);
```

向指定线程发送信号。这是多线程程序中向特定线程发送信号的标准方法，比 `kill()` 更精确，可以指定信号的接收线程。

在多线程程序中，信号可以被递送给进程中的任意未阻塞该信号的线程。使用 `pthread_kill()` 可以明确指定接收线程，确保信号被期望的线程处理。

*参数*：

- `thread` 目标线程的线程 ID（通过 `pthread_create()` 返回或 `pthread_self()` 获取）。
- `signo` 要发送的信号编号（1-63）。特殊值 0 是"空信号"，不发送实际信号，仅检查线程是否存在（用于存活性测试）。

*返回值*：

成功时返回 0，失败时返回错误码（注意：不设置 `errno`，直接返回错误码）：

- `EINVAL` `signo` 无效（<= 0 或 > `MAX_SIGNO`）。
- `ESRCH` 线程不存在或已终止。线程 ID 可能已被回收并指向新线程，导致信号发送给错误的线程。

*注意*：

- **线程特定性**：信号会被递送给指定线程，即使该线程阻塞了该信号，信号也会挂起在该线程上（而不是其他线程）。
- **存活性测试**：使用 `pthread_kill(thread, 0)` 可以测试线程是否存在：
  ```c
  if (pthread_kill(thread, 0) == 0) {
      // 线程存在
  } else {
      // 线程不存在（ESRCH）
  }
  ```
- **信号处理**：即使向特定线程发送信号，信号处理函数仍然可能在其他线程中执行（取决于信号掩码）。如果只有目标线程未阻塞该信号，则一定在该线程中处理。
- **线程 ID 重用**：线程终止后，其 ID 可能被重用。如果在线程终止后发送信号，可能发送给新线程。推荐使用 `tgkill()` 避免此问题（它会验证线程属于预期的进程）。
- **与 `kill()` 的区别**：
  - `kill()` 发送给整个进程，由任意线程处理
  - `pthread_kill()` 发送给特定线程，更精确
- **与 `raise()` 的关系**：`raise(sig)` 在多线程程序中等效于 `pthread_kill(pthread_self(), sig)`。
- **信号掩码继承**：新线程继承创建者的信号掩码。如果需要不同的掩码，在线程启动时调用 `pthread_sigmask()`。
- **典型用途**：
  - 取消或终止特定线程（发送 `SIGTERM`、`SIGUSR1` 等）
  - 向工作线程发送通知信号
  - 向信号处理线程发送信号
  - 测试线程是否存活
- **线程安全**：`pthread_kill()` 本身是线程安全的，可以从多个线程并发调用。
- **POSIX 一致性**：在 Vela 中，`pthread_t` 与 `pid_t` 相同，线程 ID 即任务 ID。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

## pthread_sigmask

```c
int pthread_sigmask(int how, const sigset_t *set, sigset_t *oset);
```

设置或查询调用线程的信号掩码。功能与 `sigprocmask()` 完全相同，但这是 POSIX 多线程程序中推荐使用的接口。

主要区别是错误报告方式：`pthread_sigmask()` 直接返回错误码（不设置 `errno`），而 `sigprocmask()` 返回 -1 并设置 `errno`。这符合 pthread 函数的一般约定。

*参数*：

- `how` 指定如何修改信号掩码：
  - `SIG_BLOCK` (1)：阻塞更多信号，新掩码 = 旧掩码 ∪ `set`
  - `SIG_UNBLOCK` (2)：解除阻塞，新掩码 = 旧掩码 - `set`
  - `SIG_SETMASK` (3)：替换掩码，新掩码 = `set`
- `set` 要操作的信号集。如果为 `NULL`，则不修改掩码，仅查询当前掩码（通过 `oset` 返回）。
- `oset` 如果非 `NULL`，返回操作前的信号掩码。

*返回值*：

成功时返回 0，失败时返回错误码（不设置 `errno`）：

- `EINVAL` `how` 参数无效。
- `EFAULT` `set` 或 `oset` 指向无效内存（某些实现）。

*注意*：

- **多线程专用**：在多线程程序中，应使用 `pthread_sigmask()` 而不是 `sigprocmask()`，虽然功能相同，但 `pthread_sigmask()` 语义更明确。
- **线程局部掩码**：每个线程有独立的信号掩码，修改只影响调用线程。
- **新线程继承**：通过 `pthread_create()` 创建的新线程继承创建者的信号掩码。
- `SIGKILL` 和 `SIGSTOP` 无法被阻塞，尝试阻塞会被静默忽略。
- 解除阻塞信号后，挂起的信号会立即递送（在函数返回前）。
- 典型用法 - 专用信号处理线程模式：
  ```c
  // 主线程：阻塞所有信号
  sigset_t mask;
  sigfillset(&mask);
  pthread_sigmask(SIG_SETMASK, &mask, NULL);
  
  // 创建工作线程（继承阻塞所有信号的掩码）
  pthread_create(&worker, NULL, worker_func, NULL);
  
  // 创建信号处理线程
  pthread_create(&sig_thread, NULL, signal_handler_thread, NULL);
  
  // 信号处理线程：解除阻塞并同步等待信号
  void *signal_handler_thread(void *arg) {
      sigset_t wait_mask;
      sigemptyset(&wait_mask);
      sigaddset(&wait_mask, SIGINT);
      sigaddset(&wait_mask, SIGTERM);
      
      int sig;
      while (1) {
          sigwait(&wait_mask, &sig);
          // 处理信号...
      }
  }
  ```
- **错误处理差异**：
  ```c
  // sigprocmask() 风格
  if (sigprocmask(SIG_BLOCK, &set, NULL) == -1) {
      perror("sigprocmask");  // errno 已设置
  }
  
  // pthread_sigmask() 风格
  int err = pthread_sigmask(SIG_BLOCK, &set, NULL);
  if (err != 0) {
      errno = err;
      perror("pthread_sigmask");  // 需要手动设置 errno
  }
  ```
- 与 `pthread_kill()` 配合使用可以实现线程间的精确信号通信。
- 在单线程程序中，`pthread_sigmask()` 和 `sigprocmask()` 完全等效。

*`POSIX` 兼容性*：完美兼容 `POSIX` 同名接口。

