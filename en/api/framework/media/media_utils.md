\[ English | [简体中文](../../../../zh-cn/api/framework/media/media_utils.md) \]

# Media Utils API

General utility interfaces for the media framework, including DTMF dual-tone multi-frequency signal generation, event name lookup, graph/policy dump, and generic command sending.

Header: `#include <media_utils.h>`

## openvela Implementation Notes

- **DTMF**: Generates DTMF dual-tone multi-frequency signals for `0-9` / `*#ABCD` keys, with a fixed audio format of `format=s16le:sample_rate=8000:ch_layout=mono` (defined by the `MEDIA_TONE_DTMF_FORMAT` macro)
- **Debug Interfaces**: `media_graph_dump`, `media_player_dump`, `media_recorder_dump` and `media_policy_dump` print internal state for troubleshooting
- **Generic Command**: `media_process_command` sends custom commands to the media server for extended capabilities (e.g., triggering an operation on a specific filter within a graph)
- **Event Name Lookup**: `media_event_get_name` converts `MEDIA_EVENT_*` numeric values to human-readable strings for log output

## DTMF Signal Generation

### media_dtmf_get_buffer_size

```c
int media_dtmf_get_buffer_size(const char* numbers);
```

Queries the buffer size required for DTMF signal generation.

**Parameters**:

- `numbers` Dial key character sequence, with characters in the range `0-9` and `*#ABCD`.

**Returns**:

Returns the buffer size in bytes on success, or a negative errno on failure.

### media_dtmf_generate

```c
int media_dtmf_generate(const char* numbers, void* buffer);
```

Generates one or more consecutive DTMF signals and writes them into the caller-provided buffer.

**Parameters**:

- `numbers` Dial key character sequence, with characters in the range `0-9` and `*#ABCD`.
- `buffer` Output buffer; its size should be queried in advance via `media_dtmf_get_buffer_size`.

**Returns**:

Returns `0` on success, or a negative errno on failure.

**Notes**:

- When playing DTMF tones, the audio parameters must be fixed to `MEDIA_TONE_DTMF_FORMAT` (`s16le / 8000Hz / mono`).

## Event Name Lookup

### media_event_get_name

```c
const char* media_event_get_name(int event);
```

Converts a `MEDIA_EVENT_*` enum value to a human-readable string.

**Parameters**:

- `event` Event value, one of the `MEDIA_EVENT_*` constants.

**Returns**:

Always returns a printable string; returns a placeholder string for unknown events (never returns `NULL`).

**Example**:

```c
printf("event: %s\n", media_event_get_name(MEDIA_EVENT_STARTED));
// Output: event: STARTED
```

## Dump Debugging

### media_graph_dump

```c
void media_graph_dump(const char* options);
```

Prints the internal state of the media graph for debugging.

**Parameters**:

- `options` Dump options string.

### media_policy_dump

```c
void media_policy_dump(const char* options);
```

Prints the current state of the media policy for debugging.

**Parameters**:

- `options` Dump options string.


### media_player_dump

```c
void media_player_dump(const char* options);
```

Prints the internal state of the media player for debugging.

**Parameters**:

- `options` Dump options string.


### media_recorder_dump

```c
void media_recorder_dump(const char* options);
```

Prints the internal state of the media recorder for debugging.

**Parameters**:

- `options` Dump options string.


## Generic Command

### media_process_command

```c
int media_process_command(const char* target, const char* cmd,
                          const char* arg, char* res, int res_len);
```

Sends a custom command to a specified graph filter instance within the media server.

**Parameters**:

- `target` Target graph filter instance name.
- `cmd` Command type.
- `arg` Command argument.
- `res` Response message output buffer.
- `res_len` Response buffer length.

**Returns**:

Returns `0` on success, or a negative errno on failure.
