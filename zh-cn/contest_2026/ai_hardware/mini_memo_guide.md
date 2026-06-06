# mini-memo 应用开发指引

> 本指引是 mini-memo 的专项开发指南。通用开发知识（环境搭建、架构、核心能力详解等）请参阅 [ai_agent 应用开发上手指南](./ai_agent_quickstart.md)。

## 一、概述

### 1、本指引目的

本指引帮助开发者基于 ai_agent 框架，快速构建一个独立的 LVGL 应用——**mini-memo（AI 记忆助手）**。通过学习本指引，你将掌握：

- 如何以 music_player demo 为模板创建新的 LVGL 应用
- 如何展示 ai_agent 的「主动+执行」能力（区别于「被动对话」）
- mini-memo 应用的核心实现细节

### 2、mini-memo 核心能力

mini-memo 是一个基于 ai_agent 构建的 AI 记忆助手应用，核心能力包括：

| 能力             | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| **系统信息总结** | 未读通知摘要、传感器数据汇总（步数/睡眠/心率）、应用状态变化 |
| **语音速记分类** | PTT 语音录入 → AI Router 自动分类（待办/备忘/日程）          |
| **主动推送**     | AI 判断「该提醒你了」就主动推送，不是用户问才答              |
| **定时回顾**     | 定期提醒用户回顾记忆，主动维护个人数据                       |

### 3、展示的 ai_agent 独有能力

mini-memo 重点展示 ai_agent 区别于普通聊天机器人的核心能力：

1. **主动任务机制**：定时任务 + 阈值触发，Agent Loop 自动检查并推送
2. **Router 意图路由**：区分「记一下」vs「提醒我」vs「总结一下」，路由到不同处理流程
3. **自然语言→结构化输出**：LLM 解析语音输入，输出 JSON 结构化数据
4. **Shell/Tool 调用**：读取传感器数据、写入存储、触发通知

### 4、适用场景

- 智能手表上的 AI 记忆助手
- 主动式健康/日程提醒应用
- 带屏幕的 IoT 设备的主动服务界面
- 任何需要 AI「主动+执行」能力的 LVGL 应用

## 二、ai_agent 核心能力详解（mini-memo 应用示例）

> 通用概念说明请参阅 [ai_agent 应用开发上手指南](./ai_agent_quickstart.md)。以下为 **mini-memo 中的具体应用示例**。

### 1、主动任务机制

mini-memo 中的应用：

- 定时回顾提醒：每 24 小时主动推送「该回顾记忆了」
- 未读阈值触发：超过 10 条未读时主动提醒

```c
// mini_memo_core.c - 主动任务检查
void mini_memo_check_periodic_review(void)
{
    uint64_t now = get_timestamp();
    uint64_t interval_sec = (uint64_t)review_interval_hours * 3600;

    if (now - last_review_time >= interval_sec) {
        // 触发主动推送
        char push_msg[256];
        snprintf(push_msg, 256, "⏰ 定期提醒：你有 %d 条未读记忆",
                 mini_memo_get_unread_count());
        mini_memo_trigger_push(push_msg);

        last_review_time = now;
    }
}
```

### 2、Router 意图路由

mini-memo 中的应用：区分备忘类型。

| 输入示例            | 路由结果           | 处理方式             |
| ------------------- | ------------------ | -------------------- |
| "记一下买牛奶"      | MEMO_TYPE_MEMO     | 直接存储为备忘       |
| "提醒我明早开会"    | MEMO_TYPE_TODO     | 解析时间，存储为待办 |
| "明天下午3点约牙医" | MEMO_TYPE_SCHEDULE | 解析时间，存储为日程 |
| "总结一下今天"      | MEMO_TYPE_SUMMARY  | 汇总系统数据生成摘要 |

```c
// mini_memo_core.c - Router 路由
static memo_type_t router_intent(const char* text)
{
    if (strstr(text, "提醒我") || strstr(text, "待办") || strstr(text, "todo"))
        return MEMO_TYPE_TODO;

    if (strstr(text, "日程") || strstr(text, "安排"))
        return MEMO_TYPE_SCHEDULE;

    if (strstr(text, "总结") || strstr(text, "摘要") || strstr(text, "今天"))
        return MEMO_TYPE_SUMMARY;

    return MEMO_TYPE_MEMO;  // 默认：备忘
}
```

### 3、自然语言→结构化输出

mini-memo 中的应用：语音输入自动分类存储。

```c
// 语音输入 → 结构化记忆
int mini_memo_voice_input(const char* voice_text)
{
    // 1. Router 路由判断类型
    memo_type_t type = router_intent(voice_text);

    // 2. LLM 解析时间和关键信息（实际应调用 LLM）
    parsed_memo_t parsed;
    parse_voice_input(voice_text, &parsed);

    // 3. 存储为结构化记忆
    return mini_memo_add_memo(parsed.type, parsed.content);
}
```

### 4、Shell/Tool 调用

mini-memo 中的应用：

| 工具         | 功能         | mini-memo 用途 |
| ------------ | ------------ | -------------- |
| Shell        | 执行系统命令 | 读取传感器数据 |
| Storage      | 持久化存储   | 保存记忆数据   |
| Notification | 发送通知     | 主动推送提醒   |
| Time         | 时间服务     | 定时任务调度   |

```c
// 读取传感器数据（通过 Shell 或直接 API）
static int read_sensor_data(system_info_t* info)
{
    // 实际应用中通过 Tool Registry 调用
    // tool_registry_execute("shell_read_sensors", &result);

    info->steps = 3200;
    info->heart_rate = 72;
    info->sleep_hours = 7;

    return 0;
}
```

### 5、数据结构

```c
// 记忆类型
typedef enum {
    MEMO_TYPE_TODO = 0,       // 待办事项
    MEMO_TYPE_MEMO = 1,       // 备忘
    MEMO_TYPE_SCHEDULE = 2,   // 日程
    MEMO_TYPE_SUMMARY = 3,    // 系统摘要
} memo_type_t;

// 单条记忆
typedef struct {
    char id[32];              // 唯一标识
    memo_type_t type;         // 类型
    char content[256];        // 内容
    uint64_t timestamp;       // 创建时间
    bool is_read;             // 是否已读
} memo_item_t;
```

### 6、LVGL UI 界面设计

mini-memo 的 LVGL 界面针对 466x466 圆形手表屏幕设计，包含首页（今日摘要）、速记页（PTT 语音录入）、回顾页、设置页。

<img src="images/mini-memo%20首页界面.jpg" alt="mini-memo 首页界面" width="300" />

<img src="images/mini-memo%20速记页界面.jpg" alt="mini-memo 速记页界面" width="300" />

## 三、手把手教程：构建 mini-memo

### 1、目标

创建一个名为 `mini_memo` 的独立 LVGL 应用，展示 ai_agent 的主动任务、Router 路由、结构化输出等能力。

### 2、创建目录结构

```
apps/packages/demos/mini_memo/
├── mini_memo_main.c           # 程序入口
├── mini_memo_core.c           # 核心逻辑
├── mini_memo_core.h           # 核心头文件
├── mini_memo_ui.c             # LVGL 界面
├── mini_memo_ui.h             # UI 头文件
├── Kconfig                    # 配置
├── Makefile                   # 编译规则
└── Make.defs                  # 构建配置
```

### 3、编写配置文件

**Kconfig：**

```
config LVX_USE_DEMO_MINI_MEMO
    bool "Mini Memo (AI 记忆助手)"
    default n
    select GRAPHICS_LVGL
    ---help---
        Enable Mini Memo application - an AI memory assistant
        based on ai_agent.

if LVX_USE_DEMO_MINI_MEMO

config LVX_MINI_MEMO_VOICE_ENABLED
    bool "Enable Voice Input"
    default y
    ---help---
        Enable PTT voice input for quick memo.

config LVX_MINI_MEMO_PROACTIVE_ENABLED
    bool "Enable Proactive Push"
    default y
    ---help---
        Enable AI-driven proactive notifications.

config LVX_MINI_MEMO_REVIEW_INTERVAL
    int "Review reminder interval (hours)"
    default 24
    range 1 168
    ---help---
        How often to remind user for memory review.

endif
```

**Makefile：**

```makefile
include $(APPDIR)/Make.defs

ifeq ($(CONFIG_LVX_USE_DEMO_MINI_MEMO), y)
    PROGNAME = mini_memo
    PRIORITY = 100
    STACKSIZE = 32768
    MODULE = $(CONFIG_LVX_USE_DEMO_MINI_MEMO)

    # ai_agent 源码路径
    AI_AGENT_DIR = $(APPDIR)/packages_ai_agent
    CFLAGS += -I$(AI_AGENT_DIR)/include
    CFLAGS += -I$(AI_AGENT_DIR)/src

    # 源文件
    CSRCS = mini_memo_core.c mini_memo_ui.c
    MAINSRC = mini_memo_main.c
endif

include $(APPDIR)/Application.mk
```

**Make.defs：**

```makefile
ifneq ($(CONFIG_LVX_USE_DEMO_MINI_MEMO),)
    CONFIGURED_APPS += $(APPDIR)/packages/demos/mini_memo
endif
```

### 4、编写入口代码

**mini_memo_main.c：**

```c
/**
 * mini_memo_main.c - Mini Memo Entry Point
 *
 * 本示例演示如何基于 ai_agent 构建独立的 LVGL 应用
 * 核心能力：主动推送 + 系统信息汇总 + 语音速记分类
 */

#include <nuttx/config.h>
#include <unistd.h>
#include <uv.h>
#include <lvgl/lvgl.h>
#include <syslog.h>

#include "mini_memo_core.h"
#include "mini_memo_ui.h"

static void lv_nuttx_uv_loop(uv_loop_t* loop, lv_nuttx_result_t* result)
{
    lv_nuttx_uv_t uv_info;
    void* data;

    uv_loop_init(loop);
    lv_memset(&uv_info, 0, sizeof(uv_info));
    uv_info.loop = loop;
    uv_info.disp = result->disp;
    uv_info.indev = result->indev;

    data = lv_nuttx_uv_init(&uv_info);
    uv_run(loop, UV_RUN_DEFAULT);
    lv_nuttx_uv_deinit(&data);
}

int main(int argc, FAR char* argv[])
{
    lv_nuttx_dsc_t info;
    lv_nuttx_result_t result;
    uv_loop_t ui_loop;

    syslog(LOG_INFO, "Mini Memo (AI 记忆助手) starting...\n");

    /* 检查 LVGL 是否已初始化 */
    if (lv_is_initialized()) {
        LV_LOG_ERROR("LVGL already initialized!");
        return -1;
    }

    /* 初始化 LVGL */
    lv_init();
    lv_nuttx_dsc_init(&info);
    lv_nuttx_init(&info, &result);

    if (result.disp == NULL) {
        LV_LOG_ERROR("LVGL display initialization failed!");
        return 1;
    }

    /* 初始化 mini_memo 核心逻辑 */
    mini_memo_core_init();

    /* 创建应用 UI */
    mini_memo_ui_init();

    /* 进入事件循环 */
    lv_nuttx_uv_loop(&ui_loop, &result);

    /* 清理 */
    mini_memo_core_deinit();
    mini_memo_ui_deinit();
    lv_nuttx_deinit(&result);
    lv_deinit();

    return 0;
}
```

### 5、编写核心逻辑

**mini_memo_core.h：**

```c
#pragma once

#include <stdbool.h>
#include <stdint.h>

/* 记忆类型 */
typedef enum {
    MEMO_TYPE_TODO = 0,       /* 待办事项 */
    MEMO_TYPE_MEMO = 1,       /* 备忘 */
    MEMO_TYPE_SCHEDULE = 2,   /* 日程 */
    MEMO_TYPE_SUMMARY = 3,    /* 系统摘要 */
} memo_type_t;

/* 记忆结构 */
typedef struct {
    char id[32];
    memo_type_t type;
    char content[256];
    uint64_t timestamp;
    bool is_read;
} memo_item_t;

/* 主动推送回调：内容 + 用户数据 */
typedef void (*proactive_callback_t)(const char* content, void* user_data);

/* 核心初始化 */
void mini_memo_core_init(void);
void mini_memo_core_deinit(void);

/* 记忆管理 */
int mini_memo_add_memo(memo_type_t type, const char* content);
int mini_memo_get_memos(memo_type_t type, memo_item_t* items, int max_count);
int mini_memo_get_unread_count(void);

/* 语音速记 */
int mini_memo_voice_input(const char* voice_text);

/* 主动任务 */
void mini_memo_check_periodic_review(void);
void mini_memo_trigger_push(const char* content);
void mini_memo_set_proactive_callback(proactive_callback_t cb, void* user_data);
```

**mini_memo_core.c：**

```c
/**
 * mini_memo_core.c - Mini Memo Core Logic
 *
 * 展示 ai_agent 的主动任务机制、Router 路由、结构化输出能力
 */

#include "mini_memo_core.h"
#include <pthread.h>
#include <string.h>
#include <stdlib.h>
#include <syslog.h>
#include <time.h>

static const char* TAG = "mini_memo_core";

#define MAX_MEMOS 100

/* 内部状态 */
typedef struct {
    memo_item_t memos[MAX_MEMOS];
    int count;
    pthread_mutex_t lock;
    bool periodic_review_enabled;
    uint64_t last_review_time;
    int review_interval_hours;
    proactive_callback_t push_callback;
    void* push_user_data;
} core_state_t;

static core_state_t s_state = {
    .count = 0,
    .lock = PTHREAD_MUTEX_INITIALIZER,
    .periodic_review_enabled = true,
    .review_interval_hours = 24,
};

/* Router 意图路由 */
static memo_type_t router_intent(const char* text)
{
    if (!text) return MEMO_TYPE_MEMO;

    if (strstr(text, "提醒我") || strstr(text, "待办"))
        return MEMO_TYPE_TODO;

    if (strstr(text, "日程") || strstr(text, "安排"))
        return MEMO_TYPE_SCHEDULE;

    if (strstr(text, "总结") || strstr(text, "今天"))
        return MEMO_TYPE_SUMMARY;

    return MEMO_TYPE_MEMO;
}

/* 核心 API 实现 */
void mini_memo_core_init(void)
{
    syslog(LOG_INFO, "[%s] Initializing\n", TAG);
    s_state.last_review_time = time(NULL);
}

int mini_memo_add_memo(memo_type_t type, const char* content)
{
    if (!content || s_state.count >= MAX_MEMOS) return -1;

    pthread_mutex_lock(&s_state.lock);

    memo_item_t* memo = &s_state.memos[s_state.count];
    snprintf(memo->id, sizeof(memo->id), "memo_%ld_%d",
             time(NULL), s_state.count);
    memo->type = type;
    strncpy(memo->content, content, sizeof(memo->content) - 1);
    memo->timestamp = time(NULL);
    memo->is_read = false;

    s_state.count++;
    pthread_mutex_unlock(&s_state.lock);

    syslog(LOG_INFO, "[%s] Added memo: type=%d, content=%s\n",
           TAG, type, content);

    return 0;
}

int mini_memo_get_unread_count(void)
{
    int count = 0;
    pthread_mutex_lock(&s_state.lock);
    for (int i = 0; i < s_state.count; i++) {
        if (!s_state.memos[i].is_read) count++;
    }
    pthread_mutex_unlock(&s_state.lock);
    return count;
}

int mini_memo_voice_input(const char* voice_text)
{
    if (!voice_text) return -1;

    /* Router 路由 */
    memo_type_t type = router_intent(voice_text);

    /* 根据类型处理 */
    if (type == MEMO_TYPE_SUMMARY) {
        /* 生成系统摘要 */
        char summary[256];
        snprintf(summary, sizeof(summary),
                 "📊 今日摘要：步数 3200，心率 72，未读 %d 条",
                 mini_memo_get_unread_count());
        return mini_memo_add_memo(type, summary);
    }

    return mini_memo_add_memo(type, voice_text);
}

void mini_memo_check_periodic_review(void)
{
    uint64_t now = time(NULL);
    uint64_t interval = s_state.review_interval_hours * 3600;

    if (now - s_state.last_review_time >= interval) {
        int unread = mini_memo_get_unread_count();
        char push[256];
        snprintf(push, sizeof(push),
                 "⏰ 定期提醒：你有 %d 条未读记忆", unread);
        mini_memo_trigger_push(push);
        s_state.last_review_time = now;
    }
}

void mini_memo_trigger_push(const char* content)
{
    if (s_state.push_callback) {
        s_state.push_callback(content, s_state.push_user_data);
    }
}

void mini_memo_set_proactive_callback(proactive_callback_t cb, void* user_data)
{
    s_state.push_callback = cb;
    s_state.push_user_data = user_data;
}
```

### 6、编写 LVGL UI

**mini_memo_ui.c（关键部分）：**

```c
/**
 * mini_memo_ui.c - Mini Memo LVGL UI
 *
 * 展示 ai_agent 主动+执行能力在手表屏幕上的呈现
 */

#include "mini_memo_ui.h"
#include "mini_memo_core.h"
#include <lvgl/lvgl.h>
#include <pthread.h>
#include <string.h>
#include <syslog.h>

static const char* TAG = "mini_memo_ui";

#define SCREEN_W 466
#define SCREEN_H 466
#define PADDING 24

/* UI 状态 */
typedef struct {
    lv_obj_t* pages[4];  /* 首页/速记页/回顾页/设置页 */
    int current_page;
    lv_obj_t* ptt_button;
    bool is_recording;
} ui_state_t;

static ui_state_t s_ui;

/* 创建主页 */
static void create_home_page(void)
{
    lv_obj_t* page = s_ui.pages[0];
    lv_obj_set_flex_flow(page, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_flex_align(page, LV_FLEX_ALIGN_CENTER,
                          LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);
    lv_obj_set_style_pad_row(page, 16, 0);  /* 子项间距 */

    /* 标题 */
    lv_obj_t* title = lv_label_create(page);
    lv_label_set_text(title, "今日摘要");
    lv_obj_set_style_text_color(title, lv_color_white(), 0);

    /* 摘要卡片 */
    lv_obj_t* card = lv_obj_create(page);
    lv_obj_set_size(card, 200, 120);
    lv_obj_set_style_radius(card, 16, 0);
    lv_obj_set_style_bg_color(card, lv_color_hex(0x2a2a40), 0);

    /* 未读数量 */
    int unread = mini_memo_get_unread_count();
    char buf[64];
    snprintf(buf, sizeof(buf), "💬 %d 条未读记忆", unread);
    lv_obj_t* label = lv_label_create(card);
    lv_label_set_text(label, buf);
    lv_obj_set_style_text_color(label, lv_color_hex(0x3a7bd5), 0);
    lv_obj_center(label);
}

/* 创建速记页 */
static void create_voice_page(void)
{
    lv_obj_t* page = s_ui.pages[1];
    lv_obj_set_flex_flow(page, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_flex_align(page, LV_FLEX_ALIGN_CENTER,
                          LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);

    /* 提示 */
    lv_obj_t* hint = lv_label_create(page);
    lv_label_set_text(hint, "按住说话");
    lv_obj_set_style_text_color(hint, lv_color_white(), 0);

    /* PTT 按钮 */
    s_ui.ptt_button = lv_obj_create(page);
    lv_obj_set_size(s_ui.ptt_button, 120, 120);
    lv_obj_set_style_radius(s_ui.ptt_button, 60, 0);
    lv_obj_set_style_bg_color(s_ui.ptt_button, lv_color_hex(0x3a7bd5), 0);

    /* 快捷示例 */
    lv_obj_t* example = lv_label_create(page);
    lv_label_set_text(example, "\"记一下买牛奶\"");
    lv_obj_set_style_text_color(example, lv_color_hex(0x3a7bd5), 0);
}

/* UI API */
void mini_memo_ui_init(void)
{
    syslog(LOG_INFO, "[%s] Initializing\n", TAG);

    /* 创建根屏幕 */
    lv_obj_t* screen = lv_obj_create(NULL);
    lv_obj_set_size(screen, SCREEN_W, SCREEN_H);
    lv_obj_set_style_bg_color(screen, lv_color_hex(0x121220), 0);

    /* 创建页面 */
    for (int i = 0; i < 4; i++) {
        s_ui.pages[i] = lv_obj_create(screen);
        lv_obj_set_size(s_ui.pages[i], SCREEN_W, SCREEN_H - 60);
        lv_obj_set_style_bg_color(s_ui.pages[i], lv_color_hex(0x121220), 0);
        if (i != 0) lv_obj_add_flag(s_ui.pages[i], LV_OBJ_FLAG_HIDDEN);
    }

    create_home_page();
    create_voice_page();
    /* 创建回顾页和设置页... */

    lv_scr_load(screen);
}

void mini_memo_ui_goto_page(int page)
{
    for (int i = 0; i < 4; i++) {
        if (i == page) {
            lv_obj_remove_flag(s_ui.pages[i], LV_OBJ_FLAG_HIDDEN);
        } else {
            lv_obj_add_flag(s_ui.pages[i], LV_OBJ_FLAG_HIDDEN);
        }
    }
    s_ui.current_page = page;
}

void mini_memo_ui_start_voice_record(void)
{
    s_ui.is_recording = true;
    lv_obj_set_style_bg_color(s_ui.ptt_button,
                               lv_color_hex(0xe74c3c), 0);  /* 红色 */
}

void mini_memo_ui_stop_voice_record(void)
{
    s_ui.is_recording = false;
    lv_obj_set_style_bg_color(s_ui.ptt_button,
                               lv_color_hex(0x3a7bd5), 0);

    /* 模拟语音识别并添加记忆 */
    mini_memo_voice_input("记一下明天买牛奶");
}
```

### 7、编译和运行

```bash
# 1. 配置项目
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake menuconfig
# 在 menuconfig 中启用 LVX_USE_DEMO_MINI_MEMO=y

# 2. 编译
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ -j$(nproc)

# 3. 运行
nsh> mini_memo &
```

### 8、完整代码架构

<img src="images/Mini%20Memo%20App%20模块架构.jpeg" alt="Mini Memo App 模块架构" width="600" />

## 四、常见问题

### Q1：Router 路由不准确

**原因**：关键词匹配过于简单。

**解决**：实际应用中应调用 LLM：

```c
int router_with_llm(const char* text, memo_type_t* type)
{
    char prompt[512];
    snprintf(prompt, sizeof(prompt),
        "用户说：%s\n请判断是待办(0)、备忘(1)、日程(2)还是总结(3)，"
        "只输出一个数字。", text);

    char* response = llm_call(prompt);
    *type = atoi(response);

    return 0;
}
```

### Q2：主动推送不触发

**原因**：定时任务未注册或检查逻辑有误。

**解决**：

1. 确保 `mini_memo_check_periodic_review()` 被定时调用
2. 检查时间间隔计算是否正确
3. 确认回调函数已注册

```c
// 在定时器回调中调用
void timer_callback(void* arg)
{
    mini_memo_check_periodic_review();
}
```

### Q3：LVGL 控件创建崩溃

**原因**：在非 LVGL 线程中创建了控件。

**解决**：使用 `lv_async_call()` 进行线程安全调用：

```c
// 错误
void other_thread(void) {
    lv_obj_t* btn = lv_button_create(screen);  // 可能崩溃
}

// 正确
lv_async_call(create_btn_async_cb, NULL);
```

### Q4：如何区分 ai_chat 和 mini-memo

| 特性     | ai_chat                      | mini-memo                         |
| -------- | ---------------------------- | --------------------------------- |
| 交互模式 | 被动对话（用户问，Agent 答） | 主动执行（Agent 主动推送）        |
| 核心能力 | 对话理解、TTS 播报           | Router 路由、定时任务、结构化存储 |
| 典型场景 | "今天天气怎么样？"           | "你该回顾记忆了"                  |

### Q5：如何添加新的记忆类型

1. 在 `memo_type_t` 枚举中添加新类型
2. 在 Router 中添加对应的意图关键词
3. 在 UI 中添加对应的图标显示
4. 在存储逻辑中处理新类型

### Q6：如何持久化存储记忆

实际应用中应使用文件系统或 KV 存储：

```c
int mini_memo_save_all(void)
{
    // 使用 cJSON 序列化
    cJSON* root = cJSON_CreateArray();
    for (int i = 0; i < s_state.count; i++) {
        cJSON* item = cJSON_CreateObject();
        cJSON_AddStringToObject(item, "id", s_state.memos[i].id);
        cJSON_AddNumberToObject(item, "type", s_state.memos[i].type);
        cJSON_AddStringToObject(item, "content", s_state.memos[i].content);
        cJSON_AddItemToArray(root, item);
    }

    char* json = cJSON_Print(root);
    write_to_file("/data/mini_memo.json", json);

    cJSON_Delete(root);
    free(json);
    return 0;
}
```

## 附录

### A、相关资源链接

- [ai_agent 仓库](../../../../../../packages_ai_agent)
- [music_player 示例](../../../../../../packages_demos/tree/dev-ai-contest-2026/music_player)
- [ai_chat demo](../../../../../../packages_demos/blob/dev-ai-contest-2026/ai_chat/README.md)
- [ai_agent LVGL UI 源码](../../../../../../packages_ai_agent/blob/dev-ai-contest-2026/src/ui/lvgl_ui_channel.c)
- [LVGL 官方文档](https://lvgl.io/documentation)

### B、关键 API 速查表

| API                                 | 模块           | 说明            |
| ----------------------------------- | -------------- | --------------- |
| `mini_memo_core_init()`             | mini_memo_core | 初始化核心模块  |
| `mini_memo_add_memo()`              | mini_memo_core | 添加记忆        |
| `mini_memo_voice_input()`           | mini_memo_core | 语音输入 + 分类 |
| `mini_memo_check_periodic_review()` | mini_memo_core | 检查定时任务    |
| `mini_memo_ui_init()`               | mini_memo_ui   | 初始化 UI       |
| `mini_memo_ui_goto_page()`          | mini_memo_ui   | 切换页面        |

### C、内存占用参考

启用 mini-memo 的内存开销：

| 项目               | 预估 RAM   |
| ------------------ | ---------- |
| LVGL UI            | ~50KB      |
| 记忆存储（100 条） | ~30KB      |
| 字体缓存           | ~20KB      |
| 定时任务           | ~5KB       |
| **总计**           | **~105KB** |

### D、文档关联

| 文档                                                  | 说明                                         |
| ----------------------------------------------------- | -------------------------------------------- |
| [ai_agent 应用开发上手指南](./ai_agent_quickstart.md) | 通用开发知识（环境搭建、架构、核心能力详解） |
| mini-memo 应用开发指引（本文档）                      | mini-memo 专项开发教程                       |
