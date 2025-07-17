# 管道开发指南

\[ [English](../../../../en/device_dev_guide/kernel/IPC/Pipe.md) | 简体中文 \]

## 一、概述

管道（Pipe）在系统中有多种用法，常见的包括以下几种：

1. Pipe （匿名管道）：
    - 用于创建一个管道，允许进程间通信（IPC）。
    - 创建的管道包含两个文件描述符：一个用于读取（读端），另一个用于写入（写端）。
2. `popen`/`pclose` 调用：
    - 创建一个连接到另一个进程的管道，可以读取其输出或向其输入端发送数据。
3. FIFO（命名管道）：
    - 允许不相关的进程之间交换数据。
    - 创建 FIFO 类似于创建文件，需要指定路径。

## 二、API 接口

### 1、`pipe` 函数使用说明

#### 使用说明

以下是 `pipe` 和 `pipe2` 的函数定义：

```C++
#include <unistd.h>
// Returns: 0 if OK, −1 on error
int pipe(int fd[2]);
int pipe2(int fd[2], int flags);
```

- 管道文件描述符：
    - `fd[0]`：管道的读端。
    - `fd[1]`：管道的写端。
- 注意事项：
    - 写入已关闭的读端：当向一个读端已关闭的管道写入数据时，会产生 SIGPIPE 信号。如果忽略该信号或从信号处理程序返回，则 `write` 返回 -1，并将 `errno` 设置为 EPIPE。
    - 多进程写入：当多个进程同时向一个管道写入数据时，数据可能会交叉。

#### 使能配置

以下是管道功能的配置选项：

```bash
CONFIG_PIPES=y
CONFIG_DEV_PIPE_SIZE>0
```

#### 示例代码

以下是一个使用管道进行线程间通信的示例代码：

```C++
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define BUFFER_SIZE 1024

void* write_thread(void* arg) {
    int* pipefd = (int*)arg;
    char buffer[] = "Hello, pipe!";
    write(pipefd[1], buffer, sizeof(buffer));

    return NULL;
}

void* read_thread(void* arg) {
    int* pipefd = (int*)arg;
    char buffer[BUFFER_SIZE];
    ssize_t bytes_read = read(pipefd[0], buffer, sizeof(buffer) - 1);
    if (bytes_read > 0) {
        buffer[bytes_read] = '\0';
        printf("Read from pipe: %s\n", buffer);
    }
 
    return NULL;
}

int main() {
    int pipefd[2];
    pthread_t writer, reader;

    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    if (pthread_create(&writer, NULL, write_thread, (void*)pipefd) != 0) {
        perror("pthread_create writer");
        exit(EXIT_FAILURE);
    }

    if (pthread_create(&reader, NULL, read_thread, (void*)pipefd) != 0) {
        perror("pthread_create reader");
        exit(EXIT_FAILURE);
    }

    pthread_join(writer, NULL);
    pthread_join(reader, NULL);

    close(pipefd[0]);
    close(pipefd[1]);
    return 0;
}
```

### 2、`popen/pclose` 函数使用说明

#### 使用说明

```C++
#include <stdio.h>
// Returns: file pointer if OK, NULL on error
FILE *popen(const char *cmdstring, const char *type);
// Returns: termination status of cmdstring, or −1 on error
int pclose(FILE *fp);
```

`popen` 函数通过调用 `posix_spawn` 创建一个新进程来执行指定的命令字符串（`cmdstring`），并将其输入或输出重定向。具体行为取决于参数 `type` 的值：

- 如果 `type` 为 `r`，文件指针连接到 `cmdstring` 的标准输出（stdout）。
- 如果 `type` 为 `w`，文件指针连接到 `cmdstring` 的标准输入（stdin）。

#### 使能配置

```bash
CONFIG_SYSTEM_POPEN=y
```

#### 示例代码

```C++
#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *pipe;
    char *command = "ls";
    char buffer[128];

    pipe = popen(command, "r");
    if (pipe == NULL) {
        fprintf(stderr, "popen failed.\n");
        return -1;
    }

    while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
        /* 处理每一行输出 */
        printf("%s", buffer);
    }

    if (pclose(pipe) == -1) {
        fprintf(stderr, "pclose failed.\n");
        return -1;
    }

    return 0;
}
```

### 3、FIFO 使用说明

#### 使用说明

FIFO（命名管道）是一种特殊类型的文件，用于在不相关的进程之间进行通信。以下是创建和使用 FIFO 的相关函数定义：

```C++
#include <sys/stat.h>
// Both return: 0 if OK, −1 on error
int mkfifo(const char *path, mode_t mode);
int mkfifoat(int dirfd, const char *path, mode_t mode);
```

- `mode` 参数： 指定 FIFO 的文件权限，与 `open` 函数中的 `mode` 参数相同。
- `mkfifoat` 的 `path` 参数说明：
    - 如果指定为绝对路径，则忽略 `dirfd` 参数，行为与 `mkfifo` 类似。
    - 如果指定为相对路径，则路径与 `dirfd` 打开的目录相关。
    - 如果指定为相对路径，且 `dirfd` 为 `AT_FDCWD`，则路径以当前目录为起点。
- 打开 FIFO 的注意事项：
    - 如果未设置非阻塞标志 `O_NONBLOCK`：
        - 以只读方式（`O_RDONLY`）打开时，进程会阻塞，直到其他进程以写方式打开该 FIFO。
        - 以只写方式（`O_WRONLY`）打开时，进程会阻塞，直到其他进程以读方式打开该 FIFO。
    - 不建议使用 `O_RDWR`（读写方式）打开 FIFO，因为这会导致读取数据时永远看不到文件结束标志（EOF）。应使用非阻塞标志来避免阻塞行为。

#### 使能配置

```bash
CONFIG_PIPES=y
CONFIG_DEV_FIFO_SIZE>0
```

#### 使用案例

以下是一个使用 FIFO 实现线程间通信的示例代码：

```C++
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>

#define FIFO_NAME "/var/myfifo"

void* writer_thread(void* arg) {
    int fd;
    char buf[] = "Hello, FIFO!";

    /* Open the FIFO for writing */
    fd = open(FIFO_NAME, O_WRONLY);
    if (fd == -1) {
        perror("open");
        exit(EXIT_FAILURE);
    }

    /* Write data to the FIFO */
    if (write(fd, buf, sizeof(buf)) == -1) {
        perror("write");
        exit(EXIT_FAILURE);
    }

    /* Close the FIFO */
    close(fd);

    return NULL;
}

void* reader_thread(void* arg) {
    int fd;
    char buf[1024];

    /* Open the FIFO for reading */
    fd = open(FIFO_NAME, O_RDONLY);
    if (fd == -1) {
        perror("open");
        exit(EXIT_FAILURE);
    }

    /* Read data from the FIFO */
    if (read(fd, buf, sizeof(buf)) == -1) {
        perror("read");
        exit(EXIT_FAILURE);
    }

    /* Print the data read from the FIFO */
    printf("Read from FIFO: %s\n", buf);

    /* Close the FIFO */
    close(fd);

    return NULL;
}

int main() {
    pthread_t writer, reader;

    /* Create the FIFO */
    if (mkfifo(FIFO_NAME, 0666) == -1) {
        if (errno != EEXIST) {
            perror("mkfifo");
            exit(EXIT_FAILURE);
        }
    }

    /* Create threads for reading and writing */
    if (pthread_create(&writer, NULL, writer_thread, NULL) != 0) {
        perror("pthread_create writer");
        exit(EXIT_FAILURE);
    }

    if (pthread_create(&reader, NULL, reader_thread, NULL) != 0) {
        perror("pthread_create reader");
        exit(EXIT_FAILURE);
    }

    /* Wait for the threads to finish */
    pthread_join(writer, NULL);
    pthread_join(reader, NULL);

    /* Remove the FIFO */
    unlink(FIFO_NAME);

    return 0;
}
```

## 三、进程间隔离限制

在当前的 openvela 环境中，由于设备通常不支持进程间隔离，各进程共享同一地址空间。这种情况下可能会引发以下问题：

- 跨进程使用文件描述符（fd）： 由于地址空间共享，跨进程使用文件描述符可能导致意外行为或资源冲突。

尽管硬件限制无法实现地址空间隔离，但以下特性在每个进程间仍然是隔离的：

- 文件描述符（fd）：每个进程的文件描述符是独立的，不能直接跨进程使用。
- 环境变量：每个进程的环境变量是独立的，修改一个进程的环境变量不会影响其他进程。
