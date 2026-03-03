# Binder 进程间通信 (IPC) 开发指南

Binder 是一种高效的进程间通信 (IPC) 传输机制，允许不同进程之间进行数据交换和远程方法调用。

## 1. 核心架构

Binder 机制由以下四个核心组件构成：

- **Binder 驱动程序**：位于内核空间，负责处理进程间通信的底层细节，包括数据包传输和线程管理。
- **ServiceManager**：一个特殊的守护进程，充当上下文管理器，负责注册服务和查找 Binder 服务。
- **Binder 服务端 (Server)**：实现具体的服务功能，并通过 Binder 机制响应来自其他进程的请求。
- **Binder 客户端 (Client)**：使用服务的进程，通过 Binder 机制向服务端发送请求并接收响应。

## 2. 系统配置与启动

### 2.1 Kconfig 配置

在使用 Binder 之前，请确保开启以下基本配置：

```kconfig
CONFIG_DRIVERS_BINDER          # 内核驱动开关
CONFIG_ANDROID_BINDER          # Binder Lib 库开关
CONFIG_ANDROID_SERVICEMANAGER  # Binder 守护进程
CONFIG_BINDER_EXAMPLES         # Binder 示例开关
```

若使用 libuv 进行事件循环监听，需在开启 `CONFIG_BINDER_EXAMPLES` 后，额外使能：

```kconfig
CONFIG_LIBUV                   # 使能 libuv 支持
```

### 2.2 运行时启动

进行 Binder 通信前，必须先启动 ServiceManager 守护进程：

```bash
nsh> servicemanager &
```

## 3. 工作原理

Binder 的通信流程如下：

1. 开发者通过 **AIDL** 文件定义通信接口。
2. **服务端**实现该接口，并将服务注册到 ServiceManager。
3. **客户端**向 ServiceManager 查询特定服务名，获取服务端的 Binder 对象引用。
4. **客户端**调用预定义的接口方法。AIDL 生成的代理代码与 Binder 库将参数序列化，并将请求写入内核驱动。
5. **Binder 驱动**将客户端请求转发至服务端。
6. **服务端**接收请求，执行具体操作，并将结果原路返回给客户端。

## 4. 接口定义 (AIDL)

AIDL (Android Interface Definition Language) 用于定义进程间通信接口，简化了跨进程的方法调用。

### 4.1 接口定义示例

创建一个简单的 AIDL 接口文件：

```java
interface ITestStuff {
    void write(int sample);
    void read(int idx);
}
```

### 4.2 代码生成

AIDL 工具将根据上述定义生成以下 C++ 文件，包含客户端代理类 (Bp) 和服务端桩类 (Bn)：

- `BnTestStuff.h`
- `BpTestStuff.h`
- `ITestStuff.h`
- `ITestStuff.cpp`

## 5. 实现模式

根据应用场景的不同，Binder 服务端主要有三种实现模式。

### 模式一：基于 Binder 线程池 (标准模式)

此模式适用于标准的阻塞式服务调用。

#### 1. 服务端实现

- **创建服务实例**：继承 AIDL 生成的 `Bn` 类并实现接口。

    ```cpp
    sp<ITestServer> testServer = new ITestServer;
    ```

- **定义接口方法**：

    ```cpp
    Status read(int32_t sample) { /* 实现逻辑 */ }
    Status write(int32_t index) { /* 实现逻辑 */ }
    ```

- **注册服务**：

    ```cpp
    sp<IServiceManager> sm(defaultServiceManager());
    sm->addService(String16("aidldemo.service"), testServer);
    ```

- **启动线程池**：将当前线程加入 Binder 线程池处理请求。

    ```cpp
    ProcessState::self()->startThreadPool();
    IPCThreadState::self()->joinThreadPool();
    ```

#### 2. 客户端实现

- **获取服务**：

    ```cpp
    sp<IServiceManager> sm(defaultServiceManager());
    sp<IBinder> binder = sm->getService(String16("aidldemo.service"));
    ```

- **转换代理接口**：

    ```cpp
    sp<ITestStuff> service = interface_cast<ITestStuff>(binder);
    ```

- **调用接口**：

    ```cpp
    service->write(123);
    service->read(456);
    ```

---

### 模式二：基于 Libuv 主循环 (异步事件驱动)

此模式适用于需要集成到 libuv 事件循环的应用。

#### 1. 服务端实现

- **创建并注册服务**：

    ```cpp
    sp<ILibuvServer> testServer = new ILibuvServer;
    // ... 实现接口并注册到 ServiceManager (同模式一) ...
    ```

- **配置 Binder 轮询**：获取 Binder 驱动的文件描述符 (FD)。

    ```cpp
    IPCThreadState::self()->setupPolling(&fd);
    ```

- **初始化 Libuv 句柄**：

    ```cpp
    uv_poll_init(uv_default_loop(), &binder_handle, fd);
    ```

- **启动监听**：当 FD 可读时触发回调 `uv_binder_cb`，处理消息队列。

    ```cpp
    uv_poll_start(&binder_handle, UV_READABLE, uv_binder_cb);
    ```

- **运行事件循环**：

    ```cpp
    uv_run(uv_default_loop(), UV_RUN_DEFAULT);
    ```

- **资源释放**：

    ```cpp
    uv_close((uv_handle_t*)&binder_handle, NULL);
    IPCThreadState::self()->stopProcess();
    ```

#### 2. 客户端实现

请参考模式一。

---

### 模式三：基于 Epoll 主循环 (原生 Linux 事件驱动)

此模式适用于使用原生 epoll 机制管理事件的应用。

#### 1. 服务端实现

- **创建并注册服务**：

    ```cpp
    // 参考模式一创建 Bn 类实例并注册
    ```

- **创建 Epoll 实例**：

    ```cpp
    int epoll_fd = epoll_create1(EPOLL_CLOEXEC);
    ```

- **配置 Binder 轮询**：

    ```cpp
    int fd;
    IPCThreadState::self()->setupPolling(&fd);
    ```

- **注册 Epoll 事件**：

    ```cpp
    struct epoll_event ev;
    ev.events = EPOLLIN;
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, fd, &ev);
    ```

- **事件循环处理**：

    ```cpp
    while (1) {
        struct epoll_event events[1];
        int numEvents = epoll_wait(epoll_fd, events, 1, -1);
        if (numEvents < 0) {
            if (errno == EINTR) {
                continue;
            }

            break;
        }

        if (numEvents > 0 && (events[0].events & EPOLLIN)) {
            ALOGI("process binder transaction");
            // 处理命令并刷新缓冲区
            IPCThreadState::self()->handlePolledCommands();
            IPCThreadState::self()->flushCommands(); // flush BC_FREE_BUFFER
        }
    }
    ```

#### 2. 客户端实现

请参考模式一。
