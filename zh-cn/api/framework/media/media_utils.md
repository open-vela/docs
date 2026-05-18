\[ [English](../../../../en/api/framework/media/media_utils.md) | 简体中文 \]

# 媒体工具 API

媒体框架通用工具接口，包括 DTMF 双音多频信号生成、事件名查询、图/策略 dump 与通用命令发送。

头文件：`#include <media_utils.h>`

## openvela 实现说明

- **DTMF**：生成 `0-9` / `*#ABCD` 对应的 DTMF 双音多频信号，音频格式固定为 `format=s16le:sample_rate=8000:ch_layout=mono`（由 `MEDIA_TONE_DTMF_FORMAT` 宏定义）
- **调试接口**：`media_graph_dump`、`media_player_dump`、`media_recorder_dump` 和 `media_policy_dump` 用于打印内部状态，便于问题定位
- **通用命令**：`media_process_command` 向 media server 发送自定义命令，用于扩展能力（如触发 graph 内某个 filter 的操作）
- **事件名查询**：`media_event_get_name` 把 `MEDIA_EVENT_*` 数值转成可读字符串，便于日志输出

## DTMF 信号生成

### media_dtmf_get_buffer_size

```c
int media_dtmf_get_buffer_size(const char* numbers);
```

查询 DTMF 信号所需的缓冲区大小。

**参数**：

- `numbers` 拨号按键字符序列，字符范围为 `0-9` 与 `*#ABCD`。

**返回值**：

成功时返回缓冲区字节数，失败时返回负的 errno。

### media_dtmf_generate

```c
int media_dtmf_generate(const char* numbers, void* buffer);
```

生成一个或连续多个 DTMF 信号并写入调用方提供的缓冲区。

**参数**：

- `numbers` 拨号按键字符序列，字符范围为 `0-9` 与 `*#ABCD`。
- `buffer` 输出缓冲区，大小需通过 `media_dtmf_get_buffer_size` 提前查询。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。

**注意**：

- 播放 DTMF 音时，音频参数必须固定为 `MEDIA_TONE_DTMF_FORMAT`（`s16le / 8000Hz / mono`）。

## 事件名查询

### media_event_get_name

```c
const char* media_event_get_name(int event);
```

将 `MEDIA_EVENT_*` 枚举值转换为可读的字符串。

**参数**：

- `event` 事件值，取值为 `MEDIA_EVENT_*` 常量。

**返回值**：

始终返回可打印的字符串，对未知事件返回占位字符串（不会返回 `NULL`）。

**示例**：

```c
printf("event: %s\n", media_event_get_name(MEDIA_EVENT_STARTED));
// 输出: event: STARTED
```

## Dump 调试

### media_graph_dump

```c
void media_graph_dump(const char* options);
```

打印 media graph 内部状态，用于调试。

**参数**：

- `options` dump 选项字符串。

### media_policy_dump

```c
void media_policy_dump(const char* options);
```

打印 media policy 当前状态，用于调试。

**参数**：

- `options` dump 选项字符串。


### media_player_dump

```c
void media_player_dump(const char* options);
```

打印 media player 内部状态，用于调试。

**参数**：

- `options` dump 选项字符串。


### media_recorder_dump

```c
void media_recorder_dump(const char* options);
```

打印 media recorder 内部状态，用于调试。

**参数**：

- `options` dump 选项字符串。


## 通用命令

### media_process_command

```c
int media_process_command(const char* target, const char* cmd,
                          const char* arg, char* res, int res_len);
```

向 media server 内的指定 graph filter 发送自定义命令。

**参数**：

- `target` 目标 graph filter 实例名。
- `cmd` 命令类型。
- `arg` 命令参数。
- `res` 响应消息输出缓冲区。
- `res_len` 响应缓冲区长度。

**返回值**：

成功时返回 `0`，失败时返回负的 errno。
