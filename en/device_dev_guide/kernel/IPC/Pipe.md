# Pipe Development Guide

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/kernel/IPC/Pipe.md) \]

## I. Overview

Pipes are widely used in systems for various purposes, including the following common types:

1. Pipe (Anonymous Pipe):

    - Used to create a pipe that allows inter-process communication (IPC).
    - The created pipe contains two file descriptors: one for reading (read end), and the other for writing (write end).

2. `popen`/`pclose` calls:
    - Creates a pipe connected to another process, allowing reading from its output or sending data to its input.

3. FIFO (Named Pipe):
    - Allows data exchange between unrelated processes.
    - Creating a FIFO is similar to creating a file and requires specifying a path.

## II. API Interfaces

### 1、`pipe` Function Usage Instructions

#### Usage Instructions

The following are the function definitions for `pipe` and `pipe2`：

```C++
#include <unistd.h>
// Returns: 0 if OK, −1 on error
int pipe(int fd[2]);
int pipe2(int fd[2], int flags);
```

- Pipe File Descriptors：
    - `fd[0]`：The read end of the pipe.
    - `fd[1]`：The write end of the pipe.
- Notes：
    - Writing to a closed read end: When data is written to a pipe whose read end is closed, a SIGPIPE signal is generated. If the signal is ignored or returned from the signal handler, `write` returns -1 and sets `errno` to EPIPE.
    - Multi-process writing: When multiple processes write to a pipe simultaneously, data may interleave.

#### Configuration Enabling

Below are the configuration options for enabling pipe functionality:

```bash
CONFIG_PIPES=y
CONFIG_DEV_PIPE_SIZE>0
```

#### Example Code

Below is an example code using pipes for inter-thread communication:

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

### 2、`popen/pclose` Function Usage Instructions

#### Usage Instructions

```C++
#include <stdio.h>
// Returns: file pointer if OK, NULL on error
FILE *popen(const char *cmdstring, const char *type);
// Returns: termination status of cmdstring, or −1 on error
int pclose(FILE *fp);
```

The `popen` function creates a new process using `posix_spawn` to execute the specified command string (`cmdstring`) and redirects its input or output. The specific behavior depends on the value of the `type` parameter:

- If `type` is `r`, the file pointer connects to the standard output (stdout) of `cmdstring`.
- If `type` is `w`, the file pointer connects to the standard input (stdin) of `cmdstring`.

#### Configuration Enabling

```Bash
CONFIG_SYSTEM_POPEN=y
```

#### Example Code

```C++
#include <stdio.h>
#include <stdlib.h>

nt main() {
    FILE *pipe;
    char *command = "ls";
    char buffer[128];

    pipe = popen(command, "r");
    if (pipe == NULL) {
        fprintf(stderr, "popen failed.\n");
        return -1;
    }

    while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
        /* Processing each line of output */
        printf("%s", buffer);
    }

    if (pclose(pipe) == -1) {
        fprintf(stderr, "pclose failed.\n");
        return -1;
    }

    return 0;
}
```

### 3、FIFO Usage Instructions

#### Usage Instructions

FIFO (Named Pipe) is a special type of file used for communication between unrelated processes. Below are the function definitions for creating and using FIFOs:

```C++
#include <sys/stat.h>
// Both return: 0 if OK, −1 on error
int mkfifo(const char *path, mode_t mode);
int mkfifoat(int dirfd, const char *path, mode_t mode);
```

- `mode` Parameter: Specifies the file permissions of the FIFO, same as the `mode` parameter in the `open` function.
- `path` Parameter in `mkfifoat`: 
    - If specified as an absolute `path`, the dirfd parameter is ignored, and behavior is similar to `mkfifo`.
    - If specified as a relative path, it is relative to the directory opened by `dirfd`.
    - If specified as a relative path and `dirfd` is `AT_FDCWD`, the path is relative to the current directory.
- Notes on Opening FIFO: 
    - If non-blocking flag `O_NONBLOCK` is not set: 
    - When opened as read-only (`O_RDONLY`), the process will block until another process opens the FIFO for writing.
    - When opened as write-only (`O_WRONLY`), the process will block until another process opens the FIFO for reading.
    - It is not recommended to open FIFO with `O_RDWR` (read-write mode), as this may cause the read to never encounter an end-of-file (EOF). Non-blocking mode should be used to avoid blocking behavior.

#### Configuration Enabling

```bash
CONFIG_PIPES=y
CONFIG_DEV_FIFO_SIZE>0
```

#### Example Code

Below is an example code using FIFO for inter-thread communication:

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

## III. Inter-Process Isolation Restrictions

In the current openvela environment, due to the lack of support for  inter-process isolation, all processes share the same address space.  This situation may lead to the following issues:

- Cross-process use of file descriptors (fd):  Due to shared address space, cross-process use of file descriptors may result in unexpected behavior or resource conflicts.

Although hardware limitations prevent address space isolation, the following features remain isolated across processes:

- File Descriptors (fd): File descriptors are independent for each process and cannot be directly shared across processes.
- Environment Variables: Environment variables are independent for each process, and modifying one process’s environment variable will not affect other processes.
