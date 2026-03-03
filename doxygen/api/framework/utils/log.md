# ALOG 简介

ALOG（Android Log）是一个常用的日志宏集，提供了一个简化的方式来记录日志信息。它是对 __android_log_print 函数的一个宏封装，使得在 C 或 C++ 代码中记录日志更加方便和直观。

## 数据结构定义

### LOG 优先级

LOG 优先级用于控制不同等级的 LOG 过滤，可以通过 `CONFIG_ALOG` 控制默认输出的 LOG 级别：

```c
typedef enum android_LogPriority {
    ANDROID_LOG_UNKNOWN = 0, // 未知
    ANDROID_LOG_DEFAULT, //默认
    ANDROID_LOG_VERBOSE, //冗长
    ANDROID_LOG_DEBUG, //调试
    ANDROID_LOG_INFO, //信息
    ANDROID_LOG_WARN, //警告
    ANDROID_LOG_ERROR, //错误
    ANDROID_LOG_FATAL, //致命
    ANDROID_LOG_SILENT, //静默
} android_LogPriority;
```

### LOG ID

LOG ID 用于标识特定的日志缓冲区，用于 __android_log_buf_write() 和 __android_log_buf_print()。

```c
typedef enum log_id {
    LOG_ID_MIN = 0,
    LOG_ID_MAIN = 0,
    LOG_ID_RADIO = 1,
    LOG_ID_EVENTS = 2,
    LOG_ID_SYSTEM = 3,
    LOG_ID_CRASH = 4,
    LOG_ID_STATS = 5,
    LOG_ID_SECURITY = 6,
    LOG_ID_KERNEL = 7,
    LOG_ID_MAX,

    LOG_ID_DEFAULT = 0x7FFFFFFF
} log_id_t;
```

## API 列表

下面是原始的 LOG API 的定义及参数说明：

```c
/**
 * @brief 将一个字符串写入日志系统。
 *
 * @param prio 日志消息的优先级，使用 `android_LogPriority` 枚举值。
 * @param tag 与日志消息关联的标签。
 * @param text 要记录的常量字符串。
 * @return int 成功时返回0，失败时返回非0值。
 */
int __android_log_write(int prio, const char* tag, const char* text);

/**
 * @brief 以格式化的方式写入日志消息。
 *
 * @param prio 日志消息的优先级，使用 `android_LogPriority` 枚举值。
 * @param tag 与日志消息关联的标签。
 * @param fmt 格式化字符串，后跟一系列参数。
 * @return int 成功时返回0，失败时返回非0值。
 */
int __android_log_print(int prio, const char* tag, const char* fmt, ...);

/**
 * @brief 使用可变参数列表以格式化的方式写入日志消息。
 *
 * @param prio 日志消息的优先级，使用 `android_LogPriority` 枚举值。
 * @param tag 与日志消息关联的标签。
 * @param fmt 格式化字符串。
 * @param ap 包含所有参数的可变参数列表。
 * @return int 成功时返回0，失败时返回非0值。
 */
int __android_log_vprint(int prio, const char* tag, const char* fmt, va_list ap);

/**
 * @brief 在条件失败时写入一条断言消息到日志系统。
 *
 * @param cond 断言条件的字符串表示。
 * @param tag 与日志消息关联的标签。
 * @param fmt 格式化字符串，后跟一系列参数（可选）。
 */
void __android_log_assert(const char* cond, const char* tag, const char* fmt, ...);
```

除原始 API 以外，ALOG 还提供了一系列的宏用于简化使用：

```c
/**
 * @brief 发送一个指定级别的日志。
 *
 * @param ... 可变参数列表，格式和参数类似于 printf 函数。
 */
#define ALOGV(...) ((void)ALOG(LOG_VERBOSE, LOG_TAG, __VA_ARGS__))
#define ALOGD(...) ((void)ALOG(LOG_DEBUG, LOG_TAG, __VA_ARGS__))
#define ALOGI(...) ((void)ALOG(LOG_INFO, LOG_TAG, __VA_ARGS__))
#define ALOGW(...) ((void)ALOG(LOG_WARN, LOG_TAG, __VA_ARGS__))
#define ALOGE(...) ((void)ALOG(LOG_ERROR, LOG_TAG, __VA_ARGS__))

/**
 * @brief 当条件为真时，写入日志。
 *
 * @param cond 评估的条件。
 * @param ... 可变参数列表，格式和参数类似于 printf 函数。
 */
#define ALOGV_IF(cond, ...)
#define ALOGD_IF(cond, ...)
#define ALOGI_IF(cond, ...)
#define ALOGW_IF(cond, ...)
#define ALOGE_IF(cond, ...)
```

## 使用示例

```c
#include <log/log.h>

#define LOG_TAG "MyAppTag"

void log_info_alogi() {
}

int main() {
    // 自定义优先级打印 log
    __android_log_print(ANDROID_LOG_INFO, LOG_TAG, "Formatted number: %d", 42);

    // 使用宏打印 INFO 级别 log
    ALOGI("ALOGI: A log message from my app.");
    return 0;
}
```
