# mini_memo Example Application

\[ English | [简体中文](../../../zh-cn/edge_ai_dev/ai_agent/mini_memo_guide.md) \]

> This guide uses mini_memo as a reference example to show how to build an embedded AI application with the ai_agent framework.
>
> For general development topics (environment setup, architecture, the core capabilities in detail and so on), see the [ai_agent Application Development Quick Start](./ai_agent_quickstart.md).

## I. Overview

### 1. What This Guide Helps You With

mini_memo is an AI memory assistant example application built on the **ai_agent framework** (openvelaClaw). If you are developing an embedded AI application on ai_agent, this guide helps you:

- **Understand the core capabilities of the ai_agent framework**: proactive tasks, intent routing, NL→structured output, Shell/Tool calls
- **Learn to integrate these capabilities into your own application**: the real mini_memo code shows how each API is called and wired up
- **Master the typical architecture of an embedded AI application**: data persistence, LLM + local fallback, voice input, proactive push

> 💡 **mini_memo is not a product for you to copy**. It is a reference for "how to use the ai_agent framework". The focus is on framework usage, not product features.

### 2. ai_agent Framework Capabilities Shown in mini_memo

mini_memo highlights the 4 core capabilities that set the ai_agent framework apart from an ordinary chatbot:

| Capability          | How mini_memo uses it                                                                          | Where you can apply it                                                           |
| ------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Intent routing**  | Dual mode of LLM classification + local fallback, so it works offline                          | Any scenario that needs to understand user intent and dispatch the handling      |
| **NL→structured**   | Voice input → LLM parsing → structured JSON data (type/content/remind_at)                      | Scenarios that turn natural language into executable data                        |
| **Shell/Tool**      | openvelaClaw Client connecting to a remote LLM + voice_channel real PTT + ASR                  | Scenarios that call remote AI services or integrate voice interaction            |
| **Proactive tasks** | Currently polls with an LVGL Timer (🏆 To be improved: switch to the framework's cron_service) | Proactive services such as health reminders, motion detection and scheduled push |

### 3. About the mini_memo Application

mini_memo is an AI memory assistant. The user speaks through PTT voice input, and the application classifies the input automatically (memo / to-do / schedule), stores it, and reminds the user proactively when it is due. Core features:

- **openvelaClaw LLM intent classification**: PTT voice input → automatic LLM classification + structured data extraction
- **Local fallback**: when the LLM is unavailable, it automatically falls back to local keyword classification
- **Persistent storage**: cJSON + the file system persist memos to `memos.json`
- **Proactive scheduled reminders**: LVGL Timer polling
- **Voice PTT + ASR**: real speech recognition integrated through voice_channel

### 4. Code Location

```plaintext
Repository: https://github.com/open-vela/packages_demos
Branch: dev-ai-contest-2026
Directory: mini_memo/

File structure:
mini_memo/
├── mini_memo_core.h    # Core API definitions (data structures, classification interface, Agent interface)
├── mini_memo_core.c    # Core implementation (persistence, classification, openvelaClaw integration, voice_channel)
├── mini_memo_ui.h      # UI interface definitions
├── mini_memo_ui.c      # LVGL UI implementation (tileview, PTT, reminders, notifications)
├── mini_memo_main.c    # Entry point (LVGL initialization, dual loop, --ptt-selftest)
├── Kconfig             # Build configuration
├── Makefile            # Build script
└── CMakeLists.txt      # CMake build
```

> mini_memo source code (relative path, for navigating within the Gitee/GitHub repositories): [packages_demos/mini_memo](../../../../../../packages_demos/tree/dev-ai-contest-2026/mini_memo)

## II. Building Your Application with the ai_agent Framework

> **This is the core section of this guide.** Each subsection below covers one core capability of the ai_agent framework, uses real mini_memo code to show "how to use it", and lists takeaways you can apply directly.

### 1. openvelaClaw Client: Connecting to a Remote LLM

**What it does**: `velaclaw_client_open()` connects to the openvelaClaw Daemon and provides remote LLM calls.

**How mini_memo does it**:

```c
// mini_memo_core.c - openvelaClaw Client initialization
int memo_agent_init(void)
{
    int voice_ret;

    // Initialize voice_channel (local, takes priority)
    voice_ret = voice_channel_init();
    if (voice_ret < 0) {
        syslog(LOG_WARNING, "%s: voice_channel_init failed: %d\n",
            MEMO_TAG, voice_ret);
    }

    // Open the openvelaClaw Client (remote LLM, optional)
    g_client = velaclaw_client_open("mini_memo");
    if (!g_client) {
        syslog(LOG_WARNING, "%s: velaclaw_client_open failed\n", MEMO_TAG);
        g_agent_connected = false;
        return voice_ret;  // Successful voice initialization is enough
    }

    g_agent_connected = true;
    return 0;
}
```

**Takeaways**:

1. **velaclaw_client_open("your_app_name")** is the entry point. Pass in your application's identifier
2. **The LLM is optional**: even if `velaclaw_client_open` fails, the application still runs (it falls back to local logic)
3. **Track the connection state with g_agent_connected**. Every later LLM call checks this flag first
4. **voice_channel and the openvelaClaw Client are initialized independently**. Voice is a local capability; the LLM is a remote capability

### 2. Intent Routing: LLM Classification + Local Fallback

**What it does**: understands the intent of the user's input and dispatches it to different handling logic. mini_memo uses the LLM for smart classification and automatically falls back to local keyword matching when the LLM is unavailable.

**How mini_memo does it**:

#### Asynchronous Classification (Recommended)

```c
// mini_memo_core.h
typedef void (*memo_classify_cb)(int status,
    const classify_result_t* result, void* cookie);

// Asynchronous classification: LLM first, automatic fallback to local on failure
int memo_classify_async(const char* text, memo_classify_cb cb, void* cookie);
```

#### Synchronous Classification

```c
// Synchronous classification (blocks for up to 20 seconds)
int memo_classify_sync(const char* text, classify_result_t* result);
```

#### Local Fallback (Keyword Matching)

```c
// mini_memo_core.c - local keyword classification
memo_type_t memo_classify_local(const char* text)
{
    // TODO keywords
    if (strstr(text, "提醒") != NULL ||
        strstr(text, "待办") != NULL ||
        strstr(text, "todo") != NULL ||
        strstr(text, "别忘了") != NULL ||
        strstr(text, "记得") != NULL) {
        return MEMO_TYPE_TODO;
    }

    // SCHEDULE keywords
    if (strstr(text, "几点") != NULL ||
        strstr(text, "什么时候") != NULL ||
        strstr(text, "约") != NULL ||
        strstr(text, "日程") != NULL ||
        strstr(text, "schedule") != NULL) {
        return MEMO_TYPE_SCHEDULE;
    }

    // Default: MEMO
    return MEMO_TYPE_MEMO;
}
```

#### Classification Result Data Structure

```c
// mini_memo_core.h - classification result (returned by the LLM)
typedef struct {
    memo_type_t type;
    char content[200];
    int64_t remind_at;
} classify_result_t;
```

**Classification examples**:

| Example input                                     | Classification     | remind_at        |
| ------------------------------------------------- | ------------------ | ---------------- |
| "Note: buy milk"                                  | MEMO_TYPE_MEMO     | 0                |
| "Remind me about a meeting at 8 tomorrow morning" | MEMO_TYPE_TODO     | Parsed timestamp |
| "Dentist appointment at 3 tomorrow afternoon"     | MEMO_TYPE_SCHEDULE | Parsed timestamp |

### 3. Natural Language → Structured Output: LLM ask API + JSON Prompt

**What it does**: parses the user's natural-language input with the LLM into structured JSON data that the program can process.

**How mini_memo does it**:

```c
// mini_memo_core.c - LLM classification prompt
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

// openvelaClaw call
static void classify_response_cb(int status, const char* response_json,
    void* cookie)
{
    classify_ctx_t* ctx = (classify_ctx_t*)cookie;
    classify_result_t result;

    if (status != 0 || !response_json) {
        // LLM failed, fall back to local classification automatically
        result.type = memo_classify_local(ctx->input_text);
        strncpy(result.content, ctx->input_text, sizeof(result.content)-1);
        result.remind_at = 0;
    } else {
        // Parse the JSON
        parse_classify_json(response_json, &result);
        if (ret < 0) {
            // JSON parsing failed, fall back to local
            result.type = memo_classify_local(ctx->input_text);
        }
    }

    ctx->user_cb(0, &result, ctx->user_cookie);
    free(ctx);
}
```

### 4. 🏆 Advanced Exercise: Implementing Proactive Tasks

**What it does**: instead of passively waiting for the user, the application checks conditions and pushes proactively. mini_memo currently implements scheduled reminders with an LVGL Timer, but that is not the approach the ai_agent framework recommends: the framework already provides the more complete `cron_service` mechanism. This improvement is left as an advanced exercise: **switch mini_memo's LVGL Timer reminders to ai_agent's cron_service**.

#### Current Implementation: LVGL Timer (Needs Improvement)

```c
// mini_memo_ui.c - poll every 60 seconds for due reminders
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

// Create the timer during initialization
g_remind_timer = lv_timer_create(remind_timer_cb, 60000, NULL);
```

#### What's the Problem

| Aspect               | LVGL Timer (current)                 | cron_service (provided by the framework)              |
| -------------------- | ------------------------------------ | ----------------------------------------------------- |
| Independent of UI    | ❌ Depends on the LVGL event loop    | ✅ Separate pthread, keeps running after the UI exits |
| Persistence          | ❌ Starts polling again after reboot | ✅ cJSON file persistence, restored after reboot      |
| Timing precision     | 60s polling, worst-case delay 60s    | Precise to the second, woken by cond_timedwait        |
| Recurring support    | ❌ Implicit AT only                  | ✅ EVERY (periodic) + AT (one-shot)                   |
| Notification channel | lv_msgbox only                       | system / voice / feishu and more                      |
| Callable by the LLM  | ❌                                   | ✅ tool_cron_add/list/remove                          |
| Tool execution       | ❌                                   | ✅ tool_registry_execute runs a tool directly         |

#### Exercise Goals

Replace `g_remind_timer` (60s reminder polling) with `cron_service` so that:

1. **A cron job is registered automatically when the user creates a memo with remind_at**
2. **A notification fires when the cron job is due** (pushed to the mini_memo channel through message_bus)
3. **It falls back to the LVGL Timer when there is no daemon connection** (so it still works offline)

#### Key API Reference

```c
// infra/cron_service.h - core cron service API
int  cron_service_init(void);
int  cron_service_start(void);
int  cron_service_stop(void);

// Add / remove / list cron jobs
int  cron_add_job(const cron_job_t* job);
int  cron_remove_job(const char* name);
int  cron_list_jobs(cron_job_t* out, int max);

// Key fields of cron_job_t
typedef struct {
    char id[64];           // Unique ID
    char name[128];        // Task name (used to remove/query)
    bool enabled;          // Whether enabled
    int  kind;             // CRON_KIND_EVERY / CRON_KIND_AT
    int  interval_s;       // Interval in seconds for EVERY mode
    int64_t at_epoch;      // Trigger timestamp for AT mode
    char message[256];     // Message content pushed when triggered
    char channel[64];      // Push channel (e.g. "mini_memo")
    char chat_id[128];     // Push target
    bool delete_after_run; // One-shot task deleted automatically after it runs
    char action[128];      // Name of the tool to run when triggered (optional)
    char action_args[256]; // Tool arguments (optional)
} cron_job_t;
```

### 5. Voice Integration: voice_channel PTT + ASR

**What it does**: the user holds the PTT button to speak, and on release the speech is automatically recognized (ASR) as text.

**How mini_memo does it**:

```c
// mini_memo_core.c - voice API wrapper
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

**Takeaways**:

1. **voice_channel_start() / voice_channel_stop_with_text()** are the core APIs: start begins recording, stop returns the ASR text
2. **PTT button events**: call start/stop in the LVGL button's `LV_EVENT_PRESSED` / `LV_EVENT_RELEASED` handlers respectively
3. **The --ptt-selftest argument**: when debugging, use `mini_memo --ptt-selftest` to trigger a PTT flow test automatically
4. **voice_channel and the openvelaClaw Client are independent**: voice is a local capability and the LLM is a remote capability, so you can enable just one of them

### 6. Data Persistence: cJSON + File System

**What it does**: persists application data to the file system so that it survives reboots.

**How mini_memo does it**:

```c
// mini_memo_core.h - storage initialization
int  memo_store_init(const char* data_dir);
void memo_store_deinit(void);
int  memo_store_add(const memo_item_t* item);
int  memo_store_delete(uint32_t id);
int  memo_store_get_count(memo_type_t type, bool unread_only);
int  memo_store_get_recent(memo_item_t* out, int max_items);
int  memo_store_get_due_reminders(int64_t now, memo_item_t* out, int max_out);
void memo_store_clear_all(void);
```

**Persistence file format** (`memos.json`):

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

**Takeaways**:

1. **cJSON serialization/deserialization**: `cJSON_CreateObject` / `cJSON_Parse` + file reads and writes
2. **Dirty flag + periodic flush**: mark the data dirty when it changes and let a 5s timer write it to disk in one go, avoiding frequent I/O
3. **memo_store_init() loads existing data**: restoring from the file at startup provides persistence across reboots
4. **select NETUTILS_CJSON**: pulls in the cJSON library automatically from Kconfig

## III. Overall Architecture and Code Flow

### 1. Architecture Overview

```plaintext
mini_memo
├── main entry point (mini_memo_main.c)
│   ├── libuv/poll event loop
│   └── Command-line argument parsing (--ptt-selftest)
├── mini_memo_core (data layer, mini_memo_core.c/h)
│   ├── memo_store: cJSON + file system persistence
│   ├── memo_classify_local: local keyword classification
│   └── memo_agent: openvelaClaw LLM integration
├── mini_memo_ui (presentation layer, mini_memo_ui.c/h)
│   ├── lv_tileview: 4 pages with horizontal swipe
│   ├── LVGL Timer: flush(5s) + remind(60s)
│   └── PTT button: voice_channel integration
└── openvelaClaw Client (remote service)
    ├── velaclaw_ask: LLM classification
    └── voice_channel: PTT + ASR
```

### 2. Startup Flow

```c
// mini_memo_main.c
int main(int argc, FAR char* argv[])
{
    bool ptt_selftest = false;

    // 1. Parse command-line arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--ptt-selftest") == 0) {
            ptt_selftest = true;
        }
    }

    // 2. Initialize LVGL
    lv_init();
    lv_nuttx_dsc_init(&info);
    lv_nuttx_init(&info, &result);

    // 3. Initialize data storage
    memo_store_init(CONFIG_MINI_MEMO_DATA_DIR);

    // 4. Initialize the openvelaClaw Agent (LLM + voice)
    memo_agent_init();

    // 5. Initialize the UI (including timers)
    memo_ui_init();

    // 6. Self-test mode
    if (ptt_selftest) {
        memo_ui_start_ptt_selftest(1500);
    }

    // 7. Enter the event loop
#ifdef CONFIG_LV_USE_NUTTX_LIBUV
    lv_nuttx_uv_loop(&ui_loop, &result);
#else
    lv_nuttx_loop();
#endif

    return 0;
}
```

### 3. Core Data Structures

```c
// mini_memo_core.h - memo types
typedef enum {
    MEMO_TYPE_MEMO = 0,       // Plain memo
    MEMO_TYPE_TODO = 1,        // To-do item
    MEMO_TYPE_SCHEDULE = 2,    // Scheduled appointment
} memo_type_t;

// A single memo
typedef struct {
    uint32_t id;               // Unique identifier
    memo_type_t type;          // Type
    char content[200];         // Content
    int64_t timestamp;         // Creation time
    int64_t remind_at;         // Reminder time (0 = no reminder)
    bool is_read;              // Whether read
} memo_item_t;
```

## IV. Building and Running

### 1. Kconfig Configuration

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
        Requires openvelaClaw framework for LLM and tools.

if LVX_USE_DEMO_MINI_MEMO

config MINI_MEMO_DATA_DIR
    string "Mini Memo data directory"
    default "/data/mini_memo"

config MINI_MEMO_REVIEW_INTERVAL
    int "Default periodic review interval (seconds)"
    default 14400

endif
```

**Key configuration notes**:

- `depends on EXAMPLES_AI_AGENT_VELA || VELACLAW_DAEMON`: requires the ai_agent framework
- `select NETUTILS_CJSON`: selects the cJSON library automatically
- `STACKSIZE = 40960`: LLM calls need a larger stack

### 2. Makefile

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

### 3. Building and Running

#### Step 1: Configure the Project

```bash
cd /path/to/openvela
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ --cmake menuconfig
```

Enable the following in menuconfig:

```plaintext
LVX_USE_DEMO_MINI_MEMO=y
EXAMPLES_AI_AGENT_VELA=y  # or VELACLAW_DAEMON=y
NETUTILS_CJSON=y
```

#### Step 2: Build

```bash
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap/ -j$(nproc)
```

#### Step 3: Run

```bash
nsh> mini_memo &
# or with the self-test argument
nsh> mini_memo --ptt-selftest
```

## V. FAQ

### Q1: How Is a Failed LLM Classification Handled?

**Cause**: the openvelaClaw Daemon isn't connected or the network has a problem.

**Solution**: mini_memo has a built-in automatic fallback:

```c
int memo_classify_async(const char* text, memo_classify_cb cb, void* cookie)
{
    // When the LLM is unavailable, use local classification directly
    if (!g_agent_connected || !g_client) {
        classify_result_t result;
        result.type = memo_classify_local(text);
        strncpy(result.content, text, sizeof(result.content)-1);
        cb(0, &result, cookie);
        return 0;
    }

    // Also fall back when the LLM call fails
    if (ret < 0) {
        result.type = memo_classify_local(text);
        cb(0, &result, cookie);
    }
}
```

### Q2: PTT Voice Doesn't Work?

**Troubleshooting steps**:

1. Check the return value of `voice_channel_init()`
2. Make sure `CONFIG_EXAMPLES_AI_AGENT_VELA` is enabled
3. Run the self-test with the `--ptt-selftest` argument
4. Check the ASR result output in the log

```bash
nsh> mini_memo --ptt-selftest
# Check the log
Mini Memo: voice_start
Mini Memo: voice_stop
Mini Memo: ASR result: "记一下买牛奶"
```

### Q3: Memo Data Isn't Persisted?

**Troubleshooting steps**:

1. Make sure the data directory exists and is writable
2. Check whether cJSON serialization succeeded
3. Check the return value of `memo_store_save()`

```c
// Debug log
syslog(LOG_INFO, "%s: save: %d items to %s\n",
    MEMO_TAG, g_store.count, g_store.file_path);
```

### Q4: How Do I Add a New Intent Type in My Own Application?

1. Add the new type to the `memo_type_t` enum
2. Add the matching intent keywords in `memo_classify_local()`
3. Describe the new type in the LLM prompt
4. Handle the new type returned by the LLM in `parse_classify_json()`

## Appendix

### A. Related Resources

- [ai_agent framework repository](../../../../../../packages_ai_agent)
- [mini_memo source code](../../../../../../packages_demos/tree/dev-ai-contest-2026/mini_memo)
- [ai_agent Application Development Quick Start](./ai_agent_quickstart.md) (prerequisites, demo walkthrough, the core capabilities in detail)

### B. API Quick Reference

#### Data Storage API

| API                                           | Description                               |
| --------------------------------------------- | ----------------------------------------- |
| `memo_store_init(data_dir)`                   | Initialize storage and load existing data |
| `memo_store_deinit()`                         | Close storage and save dirty data         |
| `memo_store_add(item)`                        | Add a memo                                |
| `memo_store_delete(id)`                       | Delete a memo                             |
| `memo_store_get_count(type, unread_only)`     | Get the number of memos of a given type   |
| `memo_store_get_due_reminders(now, out, max)` | Get due reminders                         |

#### Intent Classification API

| API                                     | Description                                        |
| --------------------------------------- | -------------------------------------------------- |
| `memo_agent_init()`                     | Initialize the openvelaClaw Client + voice_channel |
| `memo_agent_is_connected()`             | Check the LLM connection state                     |
| `memo_classify_async(text, cb, cookie)` | Asynchronous classification (LLM first)            |
| `memo_classify_sync(text, result)`      | Synchronous classification (blocking)              |
| `memo_classify_local(text)`             | Local keyword classification (always available)    |

#### Voice API

| API                              | Description                           |
| -------------------------------- | ------------------------------------- |
| `memo_voice_start()`             | Start PTT recording                   |
| `memo_voice_stop(text_out, cap)` | Stop recording and get the ASR result |

#### UI API

| API                                      | Description                                   |
| ---------------------------------------- | --------------------------------------------- |
| `memo_ui_init()`                         | Initialize the LVGL UI (creates the tileview) |
| `memo_ui_deinit()`                       | Destroy the UI and delete the timers          |
| `memo_ui_show_notification(title, body)` | Show a notification                           |
| `memo_ui_refresh_home()`                 | Refresh the home page counters                |
| `memo_ui_navigate_to(page)`              | Navigate to the given page                    |
| `memo_ui_start_ptt_selftest(hold_ms)`    | Start the PTT self-test                       |

### C. Memory Footprint Reference

| Item                            | Estimated RAM |
| ------------------------------- | ------------- |
| LVGL UI (4-page tileview)       | ~50KB         |
| Memo storage (100 items, cJSON) | ~40KB         |
| openvelaClaw Client             | ~20KB         |
| Font cache                      | ~20KB         |
| LVGL Timer × 2                  | ~5KB          |
| **Total**                       | **~135KB**    |

> Note: STACKSIZE is set to 40960 (40KB) to support LLM calls.
