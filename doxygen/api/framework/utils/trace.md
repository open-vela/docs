# ATrace 简介

ATrace（Android Trace）提供了一套应用层 Trace API，可以通过这些 API 在应用中插桩，进行性能分析，优化应用的执行效率。

## 接口 API 介绍

```c
// 头文件
#include <cutils/trace.h>

// 判断Trace是否被启用。可以用于条件性地执行跟踪代码，以减少非跟踪模式下的性能开销。
ATRACE_ENABLED()

// 开始跟踪一个上下文（通常用于函数执行时间跟踪）。name 参数用于标识该上下文。
ATRACE_BEGIN(name)

// 结束一个上下文的跟踪。此调用应与相应的 ATRACE_BEGIN 成对出现，并在其之后执行。
ATRACE_END()

// 开始跟踪一个异步事件。与 ATRACE_BEGIN/ATRACE_END 不同，异步事件不需要嵌套。
// name 描述事件，而 cookie 提供用于区分同时发生事件的唯一标识符。
// 开始和结束事件时使用的 name 和 cookie 必须一致。
ATRACE_ASYNC_BEGIN(name, cookie)

// 结束一个异步事件的跟踪。此调用应有对应的 ATRACE_ASYNC_BEGIN。
ATRACE_ASYNC_END(name, cookie)

// 开始跟踪一个异步事件。除了 name 和 cookie 外，还提供了一个 track_name 参数，
// 指定该异步事件应记录的行的名称。
// 开始事件时使用的 track_name、name 和 cookie 必须与结束时使用的一致。
ATRACE_ASYNC_FOR_TRACK_BEGIN(track_name, name, cookie)

// 结束一个异步事件的跟踪。此调用应与之前的 ATRACE_ASYNC_FOR_TRACK_BEGIN 对应。
ATRACE_ASYNC_FOR_TRACK_END(track_name, cookie)

// 跟踪一个瞬时上下文。name 用于标识上下文。
// 瞬时事件是没有定义持续时间的事件，在时间线上可视化显示为单个标记。
ATRACE_INSTANT(name)

// 跟踪一个瞬时上下文，并指定记录事件的行名称 track_name。
// 该功能与 ATRACE_INSTANT 类似，但允许将不同的瞬时事件放入同一时间线轨道/行中。
ATRACE_INSTANT_FOR_TRACK(name, track_name)

// 跟踪一个整数计数器值。name 用于标识计数器。这可以用于跟踪随时间变化的值。
ATRACE_INT(name, value)

// 跟踪一个64位整数计数器值。使用方式与 ATRACE_INT 相同，但用于更大范围的值。
ATRACE_INT64(name, value)
```

## 使用示例

```c
#define ATRACE_TAG ATRACE_TAG_ALWAYS
#include <cutils/trace.h>

int main(int argc, char *argv[])
{
    // 对当前函数进行插桩
    ATRACE_BEGIN("hello_main");
    sleep(1);
    ATRACE_INSTANT("printf");
    printf("hello world!");
    // 结束插桩
    ATRACE_END();
    return 0;
}
```

使用 trace dump 命令输出结果为：

```
   hello-7   [0]   3.187400000: sched_wakeup_new: comm=hello pid=7 target_cpu=0
   hello-7   [0]   3.187400000: tracing_mark_write: B|7|hello_main
   hello-7   [0]   4.197700000: tracing_mark_write: I|7|printf
   hello-7   [0]   4.187700000: tracing_mark_write: E|7|hello_main
```
