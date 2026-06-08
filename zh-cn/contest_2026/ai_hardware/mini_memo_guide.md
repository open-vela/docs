# mini_memo 应用介绍

> **📖 本介绍面向参加 AI 应用开发大赛的选手**，以 mini_memo 为参考示例，展示如何运用 ai_agent 框架构建嵌入式 AI 应用。
>
> 通用开发知识（环境搭建、架构、核心能力详解等）请参阅 [ai_agent 应用开发上手指南](./ai_agent_quickstart.md)。

## 一、概述

### 1、这份文档能帮到你什么

mini_memo 是基于 **ai_agent 框架**（VelaClaw）构建的 AI 记忆助手示例应用。如果你正在参加 AI 应用开发大赛，这份文档将帮助你：

- **理解 ai_agent 框架的核心能力**：主动任务、意图路由、NL→结构化输出、Shell/Tool 调用
- **学会在自己的应用中集成这些能力**：通过 mini_memo 的真实代码，看懂每个 API 怎么调、怎么接
- **掌握嵌入式 AI 应用的典型架构**：数据持久化、LLM + 本地 fallback、语音输入、主动推送

> 💡 **mini_memo 不是要你照抄的产品**，而是一份「如何用 ai_agent 框架」的参考。重点在框架用法，不在产品功能。

### 2、mini_memo 展示的 ai_agent 框架能力

mini_memo 重点展示了 ai_agent 框架区别于普通聊天机器人的 4 大核心能力：

| 能力           | mini_memo 中的体现                                              | 你可以借鉴到                               |
| -------------- | --------------------------------------------------------------- | ------------------------------------------ |
| **意图路由**   | LLM 分类 + 本地 fallback 双模式，确保离线可用                   | 任何需要理解用户意图并分发处理的场景       |
| **NL→结构化**  | 语音输入 → LLM 解析 → JSON 结构化数据（type/content/remind_at） | 需要将自然语言转为可执行数据的场景         |
| **Shell/Tool** | VelaClaw Client 连接远程 LLM + voice_channel 真实 PTT + ASR     | 需要调用远程 AI 服务或集成语音交互的场景   |
| **主动任务**   | 当前用 LVGL Timer 轮询（🏆待优化：改用框架 cron_service）        | 健康提醒、运动检测、定时推送等主动服务场景 |

### 3、mini_memo 应用简介

mini_memo 是一个 AI 记忆助手，用户通过 PTT 语音输入，应用自动分类（备忘/待办/日程）并存储，到期主动提醒。核心特性：

- **VelaClaw LLM 意图分类**：PTT 语音录入 → LLM 自动分类 + 提取结构化数据
- **本地 Fallback**：LLM 不可用时自动降级到本地关键词分类
- **持久化存储**：cJSON + 文件系统，记忆持久化到 `memos.json`
- **主动定时提醒**：LVGL Timer 轮询
- **语音 PTT + ASR**：通过 voice_channel 集成真实语音识别

### 4、代码位置

```plaintext
仓库：https://github.com/open-vela/packages_demos
分支：dev-ai-contest-2026
目录：mini_memo/

文件结构：
mini_memo/
├── mini_memo_core.h    # 核心 API 定义（数据结构、分类接口、Agent 接口）
├── mini_memo_core.c    # 核心实现（持久化、分类、VelaClaw 集成、voice_channel）
├── mini_memo_ui.h      # UI 接口定义
├── mini_memo_ui.c      # LVGL UI 实现（tileview、PTT、提醒、通知）
├── mini_memo_main.c    # 入口（LVGL 初始化、双循环、--ptt-selftest）
├── Kconfig             # 构建配置
├── Makefile            # 构建脚本
└── CMakeLists.txt      # CMake 构建
```

> mini_memo 源码（相对路径，便于在 Gitee/GitHub 仓库内跳转）：[packages_demos/mini_memo](../../../../../../packages_demos/tree/dev-ai-contest-2026/mini_memo)

## 二、用 ai_agent 框架搭建你的应用

> **这是本文档的核心章节。** 以下每个小节对应 ai_agent 框架的一项核心能力，用 mini_memo 的真实代码展示「怎么用」，并给出你可以直接借鉴的要点。

### 1、VelaClaw Client：连接远程 LLM

**做什么**：`velaclaw_client_open()` 连接 VelaClaw Daemon，获得远程 LLM 调用能力。

**mini_memo 怎么做的**：

```c
// mini_memo_core.c - VelaClaw Client 初始化
int memo_agent_init(void)
{
    int voice_ret;

    // 初始化 voice_channel（本地，优先）
    voice_ret = voice_channel_init();
    if (voice_ret < 0) {
        syslog(LOG_WARNING, "%s: voice_channel_init failed: %d\n",
            MEMO_TAG, voice_ret);
    }

    // 打开 VelaClaw Client（远程 LLM，可选）
    g_client = velaclaw_client_open("mini_memo");
    if (!g_client) {
        syslog(LOG_WARNING, "%s: velaclaw_client_open failed\n", MEMO_TAG);
        g_agent_connected = false;
        return voice_ret;  // voice 初始化成功即可
    }

    g_agent_connected = true;
    return 0;
}
```

**你可以借鉴的要点**：

1. **velaclaw_client_open("你的应用名")** 是入口，传入你的应用标识
2. **LLM 是可选的**：即使 `velaclaw_client_open` 失败，应用仍可运行（降级到本地逻辑）
3. **用 g_agent_connected 标记连接状态**，后续所有 LLM 调用都先检查此标志
4. **voice_channel 和 VelaClaw Client 独立初始化**，voice 是本地能力，LLM 是远程能力

### 2、意图路由：LLM 分类 + 本地 Fallback

**做什么**：理解用户输入的意图，分发到不同处理逻辑。mini_memo 用 LLM 做智能分类，LLM 不可用时自动降级到本地关键词匹配。

**mini_memo 怎么做的**：

#### 异步分类（推荐）

```c
// mini_memo_core.h
typedef void (*memo_classify_cb)(int status,
    const classify_result_t* result, void* cookie);

// 异步分类：LLM优先，失败自动降级到本地
int memo_classify_async(const char* text, memo_classify_cb cb, void* cookie);
```

#### 同步分类

```c
// 同步分类（阻塞等待，最多20秒）
int memo_classify_sync(const char* text, classify_result_t* result);
```

#### 本地 Fallback（关键词匹配）

```c
// mini_memo_core.c - 本地关键词分类
memo_type_t memo_classify_local(const char* text)
{
    // TODO 关键词
    if (strstr(text, "提醒") != NULL ||
        strstr(text, "待办") != NULL ||
        strstr(text, "todo") != NULL ||
        strstr(text, "别忘了") != NULL ||
        strstr(text, "记得") != NULL) {
        return MEMO_TYPE_TODO;
    }

    // SCHEDULE 关键词
    if (strstr(text, "几点") != NULL ||
        strstr(text, "什么时候") != NULL ||
        strstr(text, "约") != NULL ||
        strstr(text, "日程") != NULL ||
        strstr(text, "schedule") != NULL) {
        return MEMO_TYPE_SCHEDULE;
    }

    // 默认: MEMO
    return MEMO_TYPE_MEMO;
}
```

#### 分类结果数据结构

```c
// mini_memo_core.h - 分类结果（LLM 返回）
typedef struct {
    memo_type_t type;
    char content[200];
    int64_t remind_at;
} classify_result_t;
```

**分类效果示例**：

| 输入示例            | 分类结果           | remind_at      |
| ------------------- | ------------------ | -------------- |
| "记一下买牛奶"      | MEMO_TYPE_MEMO     | 0              |
| "提醒我明早8点开会" | MEMO_TYPE_TODO     | 解析后的时间戳 |
| "明天下午3点约牙医" | MEMO_TYPE_SCHEDULE | 解析后的时间戳 |

### 3、自然语言→结构化输出：LLM ask API + JSON prompt

**做什么**：将用户自然语言输入，通过 LLM 解析为程序可处理的结构化 JSON 数据。

**mini_memo 怎么做的**：

```c
// mini_memo_core.c - LLM 分类 prompt
static const char* g_classify_prompt_fmt =
    "You are a memo classifier. Given the user's voice input, "
    "classify it and extract structured data.\n\n"
    "Input: \"%s\"\n\n"
    "Respond ONLY with JSON:\n"
    "{\"type\":\"memo|todo|schedule\","
    "\"content\":\"<cleaned content>\","
    "\"remind_at\":<unix_timestamp_or_0>}\n\n"
    "Rules:\n"
    "- \"memo\": general notes\n"
    "- \"todo\": tasks with reminders\n"
    "- \"schedule\": appointments with times\n"
    "- content: concise version of input\n"
    "- remind_at: extract time if mentioned, else 0";

// VelaClaw 调用
static void classify_response_cb(int status, const char* response_json,
    void* cookie)
{
    classify_ctx_t* ctx = (classify_ctx_t*)cookie;
    classify_result_t result;

    if (status != 0 || !response_json) {
        // LLM 失败，自动降级到本地分类
        result.type = memo_classify_local(ctx->input_text);
        strncpy(result.content, ctx->input_text, sizeof(result.content)-1);
        result.remind_at = 0;
    } else {
        // 解析 JSON
        parse_classify_json(response_json, &result);
        if (ret < 0) {
            // JSON 解析失败，降级到本地
            result.type = memo_classify_local(ctx->input_text);
        }
    }

    ctx->user_cb(0, &result, ctx->user_cookie);
    free(ctx);
}
```

### 4、🏆 挑战项：实现主动任务

**做什么**：应用不是被动等用户操作，而是主动检查条件并推送。mini_memo 当前用 LVGL Timer 实现了定时提醒，但这不是 ai_agent 框架推荐的做法——框架已经提供了更完善的 `cron_service` 机制。这个挑战项留给参赛选手：**把 mini_memo 的 LVGL Timer 提醒改为使用 ai_agent 的 cron_service**。

#### 当前实现：LVGL Timer（需要改进）

```c
// mini_memo_ui.c - 60秒轮询检查提醒到期
static void remind_timer_cb(lv_timer_t* timer)
{
    memo_item_t items[MEMO_MAX_DISPLAY];
    int count;
    int64_t now = (int64_t)time(NULL);

    count = memo_store_get_due_reminders(now, items, MEMO_MAX_DISPLAY);
    for (int i = 0; i < count; i++) {
        memo_ui_show_notification("Reminder", items[i].content);
        memo_store_mark_read(items[i].id);
    }
}

// 初始化时创建 timer
g_remind_timer = lv_timer_create(remind_timer_cb, 60000, NULL);
```

#### 问题在哪

| 维度           | LVGL Timer（当前）     | cron_service（框架提供）              |
| -------------- | ---------------------- | ------------------------------------- |
| 独立于 UI      | ❌ 依赖 LVGL 事件循环   | ✅ 独立 pthread，UI 退出仍运行         |
| 持久化         | ❌ 重启后重新轮询       | ✅ cJSON 文件持久化，重启恢复          |
| 定时精度       | 60s 轮询，最坏延迟 60s | 精确到秒，cond_timedwait 唤醒         |
| 支持 recurring | ❌ 仅隐含 AT            | ✅ EVERY（周期）+ AT（一次性）         |
| 通知渠道       | 仅 lv_msgbox           | system / voice / feishu 等            |
| LLM 可调用     | ❌                      | ✅ tool_cron_add/list/remove           |
| 工具执行       | ❌                      | ✅ tool_registry_execute 直接执行 tool |

#### 挑战目标

将 `g_remind_timer`（60s 轮询提醒）替换为 `cron_service`，实现：

1. **用户创建带 remind_at 的 memo 时，自动注册 cron job**
2. **cron job 到期后触发通知**（通过 message_bus 推送到 mini_memo channel）
3. **无 daemon 连接时降级到 LVGL Timer 作为 fallback**（保证离线可用）

#### 关键 API 参考

```c
// infra/cron_service.h - cron 服务核心 API
int  cron_service_init(void);
int  cron_service_start(void);
int  cron_service_stop(void);

// 添加/删除/列出 cron job
int  cron_add_job(const cron_job_t* job);
int  cron_remove_job(const char* name);
int  cron_list_jobs(cron_job_t* out, int max);

// cron_job_t 关键字段
typedef struct {
    char id[64];           // 唯一 ID
    char name[128];        // 任务名（用于删除/查询）
    bool enabled;          // 是否启用
    int  kind;             // CRON_KIND_EVERY / CRON_KIND_AT
    int  interval_s;       // EVERY 模式的间隔秒数
    int64_t at_epoch;      // AT 模式的触发时间戳
    char message[256];     // 触发时推送的消息内容
    char channel[64];      // 推送渠道（如 "mini_memo"）
    char chat_id[128];     // 推送目标
    bool delete_after_run; // 一次性任务执行后自动删除
    char action[128];      // 触发时执行的 tool 名（可选）
    char action_args[256]; // tool 参数（可选）
} cron_job_t;
```

### 5、语音集成：voice_channel PTT + ASR

**做什么**：用户按住 PTT 按钮说话，松开后自动 ASR 识别为文本。

**mini_memo 怎么做的**：

```c
// mini_memo_core.c - 语音 API 封装
int memo_voice_start(void)
{
    return voice_channel_start();
}

int memo_voice_stop(char* text_out, size_t text_cap)
{
    int ret = voice_channel_stop_with_text(text_out, text_cap);
    if (ret >= 0) {
        syslog(LOG_INFO, "%s: ASR result: \"%s\"\n", MEMO_TAG, text_out);
    }
    return ret;
}
```

**你可以借鉴的要点**：

1. **voice_channel_start() / voice_channel_stop_with_text()** 是核心 API，start 录音、stop 返回 ASR 文本
2. **PTT 按钮事件**：在 LVGL 按钮的 `LV_EVENT_PRESSED` / `LV_EVENT_RELEASED` 中分别调用 start/stop
3. **--ptt-selftest 参数**：调试时用 `mini_memo --ptt-selftest` 自动触发 PTT 流程测试
4. **voice_channel 和 VelaClaw Client 是独立的**：voice 是本地能力，LLM 是远程能力，可以只启用其中一个

### 6、数据持久化：cJSON + 文件系统

**做什么**：将应用数据持久化到文件系统，确保重启后数据不丢失。

**mini_memo 怎么做的**：

```c
// mini_memo_core.h - 存储初始化
int  memo_store_init(const char* data_dir);
void memo_store_deinit(void);
int  memo_store_add(const memo_item_t* item);
int  memo_store_delete(uint32_t id);
int  memo_store_get_count(memo_type_t type, bool unread_only);
int  memo_store_get_recent(memo_item_t* out, int max_items);
int  memo_store_get_due_reminders(int64_t now, memo_item_t* out, int max_out);
void memo_store_clear_all(void);
```

**持久化文件格式**（`memos.json`）：

```json
{
    "version": 1,
    "next_id": 5,
    "items": [
        {
            "id": 1,
            "type": 1,
            "content": "提醒我明早8点开会",
            "timestamp": 1709913600,
            "remind_at": 1709942400,
            "is_read": false
        }
    ]
}
```

**你可以借鉴的要点**：

1. **cJSON 序列化/反序列化**：`cJSON_CreateObject` / `cJSON_Parse` + 文件读写
2. **脏标记 + 定时 flush**：修改数据时标记 dirty，5s timer 统一写盘，避免频繁 I/O
3. **memo_store_init() 加载已有数据**：启动时从文件恢复，实现跨重启持久化
4. **select NETUTILS_CJSON**：在 Kconfig 中自动引入 cJSON 库

## 三、整体架构与代码流程

### 1、架构总览

```plaintext
mini_memo
├── main 入口（mini_memo_main.c）
│   ├── libuv/poll 事件循环
│   └── 命令行参数解析（--ptt-selftest）
├── mini_memo_core（数据层，mini_memo_core.c/h）
│   ├── memo_store：cJSON + 文件系统持久化
│   ├── memo_classify_local：本地关键词分类
│   └── memo_agent：VelaClaw LLM 集成
├── mini_memo_ui（表现层，mini_memo_ui.c/h）
│   ├── lv_tileview：4页面水平滑动
│   ├── LVGL Timer：flush(5s) + remind(60s)
│   └── PTT 按钮：voice_channel 集成
└── VelaClaw Client（远程服务）
    ├── velaclaw_ask：LLM 分类
    └── voice_channel：PTT + ASR
```

### 2、启动流程

```c
// mini_memo_main.c
int main(int argc, FAR char* argv[])
{
    bool ptt_selftest = false;

    // 1. 解析命令行参数
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--ptt-selftest") == 0) {
            ptt_selftest = true;
        }
    }

    // 2. 初始化 LVGL
    lv_init();
    lv_nuttx_dsc_init(&info);
    lv_nuttx_init(&info, &result);

    // 3. 初始化数据存储
    memo_store_init(CONFIG_MINI_MEMO_DATA_DIR);

    // 4. 初始化 VelaClaw Agent（LLM + voice）
    memo_agent_init();

    // 5. 初始化 UI（含 timer）
    memo_ui_init();

    // 6. 自检模式
    if (ptt_selftest) {
        memo_ui_start_ptt_selftest(1500);
    }

    // 7. 进入事件循环
#ifdef CONFIG_LV_USE_NUTTX_LIBUV
    lv_nuttx_uv_loop(&ui_loop, &result);
#else
    lv_nuttx_loop();
#endif

    return 0;
}
```

### 3、核心数据结构

```c
// mini_memo_core.h - 记忆类型
typedef enum {
    MEMO_TYPE_MEMO = 0,       // 普通备忘
    MEMO_TYPE_TODO = 1,        // 待办事项
    MEMO_TYPE_SCHEDULE = 2,    // 日程安排
} memo_type_t;

// 单条记忆
typedef struct {
    uint32_t id;               // 唯一标识
    memo_type_t type;          // 类型
    char content[200];         // 内容
    int64_t timestamp;         // 创建时间
    int64_t remind_at;         // 提醒时间（0=不提醒）
    bool is_read;              // 是否已读
} memo_item_t;
```

## 四、构建与运行

### 1、Kconfig 配置

```plaintext
# packages/demos/mini_memo/Kconfig
config LVX_USE_DEMO_MINI_MEMO
    bool "Mini Memo - AI Memory Assistant"
    default n
    depends on GRAPHICS_LVGL
    depends on LV_USE_NUTTX
    depends on EXAMPLES_AI_AGENT_VELA || VELACLAW_DAEMON
    select NETUTILS_CJSON
    ---help---
        AI-powered memory assistant with voice input,
        intent classification, and proactive reminders.
        Requires VelaClaw framework for LLM and tools.

if LVX_USE_DEMO_MINI_MEMO

config MINI_MEMO_DATA_DIR
    string "Mini Memo data directory"
    default "/data/mini_memo"

config MINI_MEMO_REVIEW_INTERVAL
    int "Default periodic review interval (seconds)"
    default 14400

endif
```

**关键配置说明**：

- `depends on EXAMPLES_AI_AGENT_VELA || VELACLAW_DAEMON`：需要 ai_agent 框架
- `select NETUTILS_CJSON`：自动选中 cJSON 库
- `STACKSIZE = 40960`：LLM 调用需要更大栈空间

### 2、Makefile

```makefile
# packages/demos/mini_memo/Makefile
include $(APPDIR)/Make.defs

ifeq ($(CONFIG_LVX_USE_DEMO_MINI_MEMO), y)
PROGNAME  = mini_memo
PRIORITY  = 100
STACKSIZE = 40960
MODULE    = $(CONFIG_LVX_USE_DEMO_MINI_MEMO)

# AI Agent client SDK include path
CFLAGS += ${INCDIR_PREFIX}$(APPDIR)/packages/ai_agent/include
CFLAGS += ${INCDIR_PREFIX}$(APPDIR)/packages/ai_agent/src

CSRCS   = mini_memo_core.c mini_memo_ui.c
MAINSRC = mini_memo_main.c
endif

include $(APPDIR)/Application.mk
```

### 3、编译和运行

#### 步骤 1：配置项目

```bash
cd /path/to/openvela
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake menuconfig
```

在 menuconfig 中启用：

```plaintext
LVX_USE_DEMO_MINI_MEMO=y
EXAMPLES_AI_AGENT_VELA=y  # 或 VELACLAW_DAEMON=y
NETUTILS_CJSON=y
```

#### 步骤 2：编译

```bash
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ -j$(nproc)
```

#### 步骤 3：运行

```bash
nsh> mini_memo &
# 或带自检参数
nsh> mini_memo --ptt-selftest
```

## 五、常见问题

### Q1：LLM 分类失败时如何处理？

**原因**：VelaClaw Daemon 未连接或网络异常。

**解决**：mini_memo 内置自动降级机制：

```c
int memo_classify_async(const char* text, memo_classify_cb cb, void* cookie)
{
    // LLM 不可用时，直接用本地分类
    if (!g_agent_connected || !g_client) {
        classify_result_t result;
        result.type = memo_classify_local(text);
        strncpy(result.content, text, sizeof(result.content)-1);
        cb(0, &result, cookie);
        return 0;
    }

    // LLM 调用失败时也降级
    if (ret < 0) {
        result.type = memo_classify_local(text);
        cb(0, &result, cookie);
    }
}
```

### Q2：PTT 语音不工作？

**排查步骤**：

1. 检查 `voice_channel_init()` 返回值
2. 确认 `CONFIG_EXAMPLES_AI_AGENT_VELA` 已启用
3. 使用 `--ptt-selftest` 参数运行自检
4. 检查日志中的 ASR 结果输出

```bash
nsh> mini_memo --ptt-selftest
# 查看日志
Mini Memo: voice_start
Mini Memo: voice_stop
Mini Memo: ASR result: "记一下买牛奶"
```

### Q3：记忆数据持久化失败？

**排查步骤**：

1. 确认数据目录存在且可写
2. 检查 cJSON 序列化是否成功
3. 查看 `memo_store_save()` 返回值

```c
// 调试日志
syslog(LOG_INFO, "%s: save: %d items to %s\n",
    MEMO_TAG, g_store.count, g_store.file_path);
```

### Q4：如何在自己的应用中添加新的意图类型？

1. 在 `memo_type_t` 枚举中添加新类型
2. 在 `memo_classify_local()` 中添加对应的意图关键词
3. 在 LLM prompt 中添加新类型说明
4. 在 `parse_classify_json()` 中处理 LLM 返回的新类型

## 附录

### A、相关资源

- [ai_agent 框架仓库](../../../../../../packages_ai_agent)
- [mini_memo 源码](../../../../../../packages_demos/tree/dev-ai-contest-2026/mini_memo)
- [ai_agent 应用开发上手指南](./ai_agent_quickstart.md)（前置知识、Demo 解析、核心能力详解）

### B、API 速查表

#### 数据存储 API

| API                                           | 说明                     |
| --------------------------------------------- | ------------------------ |
| `memo_store_init(data_dir)`                   | 初始化存储，加载已有数据 |
| `memo_store_deinit()`                         | 关闭存储，保存脏数据     |
| `memo_store_add(item)`                        | 添加记忆                 |
| `memo_store_delete(id)`                       | 删除记忆                 |
| `memo_store_get_count(type, unread_only)`     | 获取指定类型记忆数量     |
| `memo_store_get_due_reminders(now, out, max)` | 获取到期提醒             |

#### 意图分类 API

| API                                     | 说明                                   |
| --------------------------------------- | -------------------------------------- |
| `memo_agent_init()`                     | 初始化 VelaClaw Client + voice_channel |
| `memo_agent_is_connected()`             | 检查 LLM 连接状态                      |
| `memo_classify_async(text, cb, cookie)` | 异步分类（LLM优先）                    |
| `memo_classify_sync(text, result)`      | 同步分类（阻塞）                       |
| `memo_classify_local(text)`             | 本地关键词分类（始终可用）             |

#### 语音 API

| API                              | 说明                    |
| -------------------------------- | ----------------------- |
| `memo_voice_start()`             | 开始 PTT 录音           |
| `memo_voice_stop(text_out, cap)` | 停止录音，获取 ASR 结果 |

#### UI API

| API                                      | 说明                            |
| ---------------------------------------- | ------------------------------- |
| `memo_ui_init()`                         | 初始化 LVGL UI（创建 tileview） |
| `memo_ui_deinit()`                       | 销毁 UI，删除 timers            |
| `memo_ui_show_notification(title, body)` | 弹出通知                        |
| `memo_ui_refresh_home()`                 | 刷新首页统计数字                |
| `memo_ui_navigate_to(page)`              | 切换到指定页面                  |
| `memo_ui_start_ptt_selftest(hold_ms)`    | 启动 PTT 自检                   |

### C、内存占用参考

| 项目                      | 预估 RAM   |
| ------------------------- | ---------- |
| LVGL UI（4页面 tileview） | ~50KB      |
| 记忆存储（100条，cJSON）  | ~40KB      |
| VelaClaw Client           | ~20KB      |
| 字体缓存                  | ~20KB      |
| LVGL Timer × 2            | ~5KB       |
| **总计**                  | **~135KB** |

> 注：STACKSIZE 配置为 40960（40KB），以支持 LLM 调用。
