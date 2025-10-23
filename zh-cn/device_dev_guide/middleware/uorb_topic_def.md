# uORB 主题定义指南

[[English](../../../en/device_dev_guide/middleware/uorb_topic_def.md) | 简体中文]

## 一、概述

本文档旨在指导您如何在 openvela 系统中定义一个新的 uORB 主题 (Topic)。

> **开发建议：** 在创建新主题前，我们建议您首先查阅 openvela 现有的主题列表。优先复用已有主题可以提升系统的标准化程度和兼容性。如果现有主题无法满足您的需求，再遵循本指南创建新主题。

## 二、定义步骤

定义一个 uORB 主题遵循标准的 C 语言头文件与源文件分离的实践。这确保了接口的清晰和代码的模块化。整个过程分为两个核心步骤：

1. **在头文件 (.h) 中**：定义主题的数据结构，并声明其元数据，以供外部模块引用。
2. **在源文件 (.c) 中**：定义主题的元数据实例，并提供可选的调试打印支持。

### 步骤 1：在头文件中定义数据结构与声明元数据

您需要在头文件中完成两项工作：定义消息体的数据结构，以及使用 `ORB_DECLARE` 宏声明主题的元数据。这使得其他模块可以通过包含此头文件来了解主题的结构并引用它。

**示例：`orb_test.h`**

```C
#include <uORB/uORB.h>
#include <inttypes.h> // 引入 PRIu64 等宏定义所需的头文件

/* 1. 定义主题的数据结构 */
struct orb_test_s {
    uint64_t timestamp;  /* 时间戳, 单位: 微秒 (us) */
    int32_t val;         /* 示例数据字段 */
};

/* 2. 声明主题的元数据，使其可被外部引用 */
ORB_DECLARE(orb_test);
```

### 步骤 2：在源文件中定义元数据实例

在对应的源文件中，您需要使用 `ORB_DEFINE` 宏来创建并初始化主题的元数据全局实例。

- **`ORB_DEFINE` 宏**

    此宏用于将主题名称、数据结构和可选的调试格式化字符串关联起来，创建一个 `orb_metadata` 类型的常量实例。

- `ORB_DEFINE(topic_name, struct_type, format_string);`

    - `topic_name`：主题的名称，例如 `orb_test`。
    - `struct_type`：主题的数据结构类型，例如 `struct orb_test_s`。
    - `format_string`：一个用于 `uorb_listener` 工具打印消息内容的格式化字符串。此参数是可选的，且仅在 `CONFIG_DEBUG_UORB` 开启时生效。

**示例：`orb_test.c`**

```C++
#include "orb_test.h"

/* 1. (可选) 为 uorb_listener 定义一个格式化字符串 */
#ifdef CONFIG_DEBUG_UORB
static const char orb_test_format[] = "timestamp:%" PRIu64 ",val:%" PRId32 "";
#endif

/* 2. 定义主题的元数据实例 */
ORB_DEFINE(orb_test, struct orb_test_s, orb_test_format);
```

**注意**：格式化字符串中使用的 `PRIu64`、`PRId32` 等宏是标准 C99 的一部分，用于确保跨平台打印 64 位或 32 位整型的可移植性。请确保已包含 `<inttypes.h>` 头文件。

## 三、获取主题句柄

在定义完成后，您可以在代码中使用 `ORB_ID()` 宏来获取主题的句柄 (`orb_id_t`)。该句柄是指向主题元数据实例的指针，是调用 `orb_subscribe()`、`orb_advertise()` 等 API 的必需参数。

```C++
#include "orb_test.h"

void my_function(void)
{
    // 获取 orb_test 主题的句柄
    orb_id_t my_topic_id = ORB_ID(orb_test);

    // 后续可将 my_topic_id 用于订阅或发布操作
    // int sub_fd = orb_subscribe(my_topic_id);
    // ...
}
```

## 四、完整示例：定义与使用

以下示例展示了从定义一个 `orb_test` 主题到在应用程序中订阅它的完整流程。

### 1、辅助说明

- **代码结构**：为了便于演示，此示例将所有定义和使用逻辑都放在一个文件中。在实际项目中，您应遵循头文件和源文件分离的最佳实践。
- **`libuv`** **包装**：此示例使用 `uv_topic_subscribe` 函数来订阅主题。这是 openvela 基于 `libuv` 事件循环对原生 uORB API 进行的一层异步事件封装，适用于需要进行事件驱动编程的场景。`test_topic_cb` 是事件发生时被调用的回调函数。

### 2、示例代码

```C++
#include <stdio.h>
#include <uv.h>
#include <uORB/uORB.h>
#include <inttypes.h>

/*
 * =======================================================
 *   第一部分：定义 uORB 主题 (通常在独立的 .h 和 .c 中)
 * =======================================================
 */

/* 1. 声明主题元数据 (等同于 .h 文件内容) */
ORB_DECLARE(orb_test);

/* 2. 定义主题的数据结构 (等同于 .h 文件内容) */
struct orb_test_s {
  uint64_t timestamp;
  int32_t val;
};

/* 3. 定义调试格式化字符串 (等同于 .c 文件内容) */
#ifdef CONFIG_DEBUG_UORB
static const char orb_test_format[] = "timestamp:%" PRIu64 ",val:%" PRId32 "";
#endif

/* 4. 定义主题元数据实例 (等同于 .c 文件内容) */
ORB_DEFINE(orb_test, struct orb_test_s, orb_test_format);



/*
 * =======================================================
 *   第二部分：在应用中使用主题 (应用程序逻辑)
 * =======================================================
 */

// 声明一个回调函数，用于处理接收到的主题数据
// (注意：此函数在示例中未实现，仅为演示 API 用法)
void test_topic_cb(uv_topic_t *handle, const void *data, int status) {
    if (status == 0) {
        const struct orb_test_s *test_data = data;
        printf("Received orb_test data: timestamp=%" PRIu64 ", val=%" PRId32 "\n",
               test_data->timestamp, test_data->val);
    }
}

/* 5. 订阅并监听主题 */
int main(int argc, char *argv[]) {
    // 获取默认的 libuv 事件循环
    uv_loop_t* loop = uv_default_loop();

    // 初始化 topic 句柄
    uv_topic_t topic;

    // 订阅 orb_test 主题，并注册回调函数
    // 使用 ORB_ID() 宏获取主题句柄
    if (uv_topic_subscribe(loop, &topic, ORB_ID(orb_test), test_topic_cb) != 0) {
        fprintf(stderr, "Failed to subscribe to topic\n");
        return 1;
    }

    printf("Successfully subscribed to 'orb_test'. Waiting for data...\n");

    // 运行事件循环，程序将在此处阻塞，等待事件发生
    uv_run(loop, UV_RUN_DEFAULT);

    return 0;
}
```
