# Feature Trace API

Feature 框架中用于性能追踪（trace）打点的宏定义。这些宏在启用时调用 NuttX 的 `sched_note` 接口记录事件，未启用时展开为空操作。

头文件：`#include <feature_trace.h>`

## openvela 实现说明

- **条件编译**：所有 trace 宏由 `CONFIG_FEATURE_USE_SCHED_NOTE` 配置项控制
    - 启用时，展开为 `sched_note_*` 系列调用，使用 `NOTE_TAG_ALWAYS` 标签
    - 未启用时，展开为空操作（不产生任何 CPU / 内存开销），适合生产环境编译
- **依赖**：依赖 NuttX 内核的 `sched_note` 机制，需同时启用 `CONFIG_SCHED_INSTRUMENTATION` 相关配置
- **使用场景**：在 Feature 接口实现或 JS-Native 边界处打点，配合 openvela 的 trace 分析工具（如 SystemView、Perfetto）可视化性能瓶颈
- **成对使用**：`FEATURE_NOTE_BEGIN*` / `FEATURE_NOTE_END*` 必须成对调用，否则 trace 事件配对会失败

## 基础打点宏

### FEATURE_NOTE_PRINTF

```c
FEATURE_NOTE_PRINTF(format, ...)
```

以格式化字符串打点，类似 `printf`。用于记录自定义调试信息。

**参数**：

- `format` 格式化字符串。
- `...` 可变参数列表，与 format 占位符对应。

### FEATURE_NOTE_BEGIN

```c
FEATURE_NOTE_BEGIN()
```

标记一段代码执行的开始（无附加信息）。必须与 `FEATURE_NOTE_END` 成对使用。

### FEATURE_NOTE_END

```c
FEATURE_NOTE_END()
```

标记一段代码执行的结束。与最近一次 `FEATURE_NOTE_BEGIN` 配对。

## 带标签的打点宏

### FEATURE_NOTE_BEGIN_STR

```c
FEATURE_NOTE_BEGIN_STR(str)
```

带字符串标签的起始打点，用于标识代码段的语义。

**参数**：

- `str` 事件标签字符串，该字符串需在整个 trace 事件期间保持有效。

### FEATURE_NOTE_END_STR

```c
FEATURE_NOTE_END_STR(str)
```

带字符串标签的结束打点，与对应 `FEATURE_NOTE_BEGIN_STR` 的标签一致。

**参数**：

- `str` 事件标签字符串（必须与起始打点的标签一致）。

### FEATURE_NOTE_MARK

```c
FEATURE_NOTE_MARK(str)
```

打一个即时标记点，不需要配对。用于在时间线上标记单一事件。

**参数**：

- `str` 标记标签字符串。

## 作用域打点宏

### FEATURE_NOTE_BEGIN_LOCAL / FEATURE_NOTE_END_LOCAL

```c
FEATURE_NOTE_BEGIN_LOCAL(str)
    // 被追踪的代码
FEATURE_NOTE_END_LOCAL()
```

带局部变量作用域的起止打点。内部通过局部变量保存标签，避免上层代码传参复杂。

**参数**：

- `str` 事件标签字符串。

**使用示例**：

```c
void my_feature_func(void)
{
    FEATURE_NOTE_BEGIN_LOCAL("my_feature_func");
    // ... 业务逻辑 ...
    FEATURE_NOTE_END_LOCAL();
}
```

**注意**：

- `FEATURE_NOTE_BEGIN_LOCAL` 与 `FEATURE_NOTE_END_LOCAL` 必须在同一作用域内成对使用，宏内部使用 `do { ... } while(0)` 模式封装，依赖编译器能够识别作用域。
- 宏内部会引入名为 `note_temp_str` 的局部变量，同一作用域内不要使用该变量名。
