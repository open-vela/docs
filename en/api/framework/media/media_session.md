\[ English | [简体中文](../../../../zh-cn/api/framework/media/media_session.md) \]

# Media Session API

Media playback control and state synchronization, supporting the controller-controllee model.

Header: `#include <media_session.h>`

## openvela Implementation Notes

- **Controller-controllee model**: Supports two roles
    - Controller: Opened via `media_session_open`, sends playback control commands to the currently active media
    - Controllee: Registered via `media_session_register`, receives control commands and reports state
- **Synchronous/asynchronous dual model**: `media_session_*` (synchronous) and `media_uv_session_*` (asynchronous, based on libuv)
- **Control commands**: start / stop / pause / seek / prev_song / next_song / volume, etc.
- **State queries**: The controller can query the current playback state, position, duration, volume, etc.
- **State notifications**: The controllee pushes playback state changes to the controller via `notify` / `update`

## Controller Interfaces - Lifecycle

### media_session_open

```c
void* media_session_open(const char* params);
```

Open a media session controller.

**Parameters**:

- `params` NULL, currently unused.

**Returns**:

void*    The controller handle, or NULL on failure.


### media_session_close

```c
int media_session_close(void* handle);
```

Close a media session controller.

**Parameters**:

- `handle` Controller handle.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_set_event_callback

```c
int media_session_set_event_callback(void* handle, void* cookie, media_event_callback on_event);
```

Set an event callback to receive messages from the controllee.

**Parameters**:

- `handle` Controller handle.
- `cookie` Callback argument for `on_event`.
- `on_event` Event callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.


## Controller Interfaces - Playback Control

### media_session_start

```c
int media_session_start(void* handle);
```

Request to start playback.

**Parameters**:

- `handle` Controller handle.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_stop

```c
int media_session_stop(void* handle);
```

Request to stop playback.

**Parameters**:

- `handle` Controller handle.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_pause

```c
int media_session_pause(void* handle);
```

Request to pause playback.

**Parameters**:

- `handle` Controller handle.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_seek

```c
int media_session_seek(void* handle, unsigned position);
```

Request to seek to the specified position.

**Parameters**:

- `handle` Controller handle.
- `position` Start position, in milliseconds.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_prev_song

```c
int media_session_prev_song(void* handle);
```

Request to play the previous song.

**Parameters**:

- `handle` Controller handle.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_next_song

```c
int media_session_next_song(void* handle);
```

Request to play the next song.

**Parameters**:

- `handle` Controller handle.


## Controller Interfaces - Volume Control

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_increase_volume

```c
int media_session_increase_volume(void* handle);
```

Request to increase the volume.

**Parameters**:

- `handle` Controller handle.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_decrease_volume

```c
int media_session_decrease_volume(void* handle);
```

Request to decrease the volume.

**Parameters**:

- `handle` Controller handle.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_set_volume

```c
int media_session_set_volume(void* handle, int volume);
```

Request to set the volume.

**Parameters**:

- `handle` Controller handle.
- `volume` Volume level.

**Returns**:

Returns 0 on success, or a negative error code on failure.

**Note**:

- This API is not implemented yet.


## Controller Interfaces - State Queries

### media_session_query

```c
int media_session_query(void* handle, const media_metadata_t** data);
```

Query metadata from the most active controllee.

**Parameters**:

- `handle` Controller handle.
- `data` Output pointer to receive the metadata pointer.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_session_get_state

```c
int media_session_get_state(void* handle, int* state);
```

Get the overall status.

**Parameters**:

- `handle` Controller handle.
- `state` Current state.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_session_get_position

```c
int media_session_get_position(void* handle, unsigned* position);
```

Get the current position in milliseconds.

**Parameters**:

- `handle` Controller handle.
- `position` Current position, in milliseconds.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_session_get_duration

```c
int media_session_get_duration(void* handle, unsigned* duration);
```

Get the total duration in milliseconds.

**Parameters**:

- `handle` Controller handle.
- `duration` Current total duration, in milliseconds.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_session_get_volume

```c
int media_session_get_volume(void* handle, int* volume);
```

Get the current volume index.

**Parameters**:

- `handle` Controller handle.
- `volume` Volume level.

**Returns**:

Returns 0 on success, or a negative error code on failure.


## Controllee Interfaces

### media_session_register

```c
void* media_session_register(void* cookie, media_event_callback on_event);
```

Register as a session controllee.

**Parameters**:

- `cookie` Callback argument of `on_event`.
- `on_event` Event callback function.

**Returns**:

Returns the controllee handle on success, or NULL on failure.


### media_session_unregister

```c
int media_session_unregister(void* handle);
```

Unregister the session controllee.

**Parameters**:

- `handle` Controllee handle.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_notify

```c
int media_session_notify(void* handle, int event, int result, const char* extra);
```

Notify the result of a control message. After receiving MEDIA_EVENT_* from `on_event`, as the controllee you should handle the control message; after acknowledging it, call this API to send the response to the controller.

**Parameters**:

- `handle` Controllee handle.
- `event` MEDIA_EVENT_*
- `result` Operation result; `0` on success, a negative errno on failure.
- `extra` Additional message.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_session_update

```c
int media_session_update(void* handle, const media_metadata_t* data);
```

Update metadata to the session.

**Parameters**:

- `handle` Controllee handle.
- `data` Metadata to update.


## Asynchronous Interfaces (libuv-based)

The following interfaces are available only when `CONFIG_LIBUV` is enabled; both the controller and the controllee have corresponding asynchronous versions.

**Returns**:

Returns `0` on success, or a negative errno on failure.



### media_uv_session_open

```c
void* media_uv_session_open(void* loop, char* params, media_uv_callback on_open, void* cookie);
```

Open an async session controller.

**Parameters**:

- `loop` The `uv_loop_t*` event loop handle of the current thread.
- `params` Currently unused.
- `on_open` Callback triggered after opening completes.
- `cookie` Callback context shared by `on_open`, `on_event`, and `on_close`.

**Returns**:

Returns the async controller handle on success.


### media_uv_session_close

```c
int media_uv_session_close(void* handle, media_uv_callback on_close);
```

Close the async controller handle.

**Parameters**:

- `handle` Async controller handle to destroy.
- `on_close` Callback triggered after closing completes.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_session_listen

```c
int media_uv_session_listen(void* handle, media_event_callback on_event);
```

Listen to events from the controllee.

**Parameters**:

- `handle` Async controller handle.
- `on_event` Event callback function.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_session_start

```c
int media_uv_session_start(void* handle, media_uv_callback on_start, void* cookie);
```

Request to start playback.

**Parameters**:

- `handle` Async controller handle.
- `on_start` Result callback function.
- `cookie` Callback argument of `on_start`.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_session_stop

```c
int media_uv_session_stop(void* handle, media_uv_callback on_stop, void* cookie);
```

Request to stop playback.

**Parameters**:

- `handle` Async controller handle.
- `on_stop` Result callback function.
- `cookie` Callback argument of `on_stop`.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_session_pause

```c
int media_uv_session_pause(void* handle, media_uv_callback on_pause, void* cookie);
```

Request to pause playback.

**Parameters**:

- `handle` Async controller handle.
- `on_pause` Result callback function.
- `cookie` Callback argument of `on_pause`.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_session_seek

```c
int media_uv_session_seek(void* handle, unsigned position, media_uv_callback on_seek, void* cookie);
```

Request to seek to the specified position.

**Parameters**:

- `handle` Player handle.
- `position` Start position, in milliseconds.
- `on_seek` Result callback function.
- `cookie` Callback argument of `on_seek`.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_session_prev_song

```c
int media_uv_session_prev_song(void* handle, media_uv_callback on_pre_song, void* cookie);
```

Request to play the previous song.

**Parameters**:

- `handle` Async controller handle.
- `on_prev` Result callback function.
- `cookie` Callback argument of `on_prev`.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_session_next_song

```c
int media_uv_session_next_song(void* handle, media_uv_callback on_next, void* cookie);
```

Request to play the next song.

**Parameters**:

- `handle` Async controller handle.
- `on_next` Result callback function.
- `cookie` Callback argument of `on_next`.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_session_increase_volume

```c
int media_uv_session_increase_volume(void* handle, media_uv_callback on_increase, void* cookie);
```

Request to increase the volume.

**Parameters**:

- `handle` Async controller handle.
- `on_increase` Result callback function.
- `cookie` Callback argument of `on_increase`.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_session_decrease_volume

```c
int media_uv_session_decrease_volume(void* handle, media_uv_callback on_decrease, void* cookie);
```

Request to decrease the volume.

**Parameters**:

- `handle` Async controller handle.
- `on_decrease` Result callback function.
- `cookie` Callback argument of `on_decrease`.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_session_set_volume

```c
int media_uv_session_set_volume(void* handle, int volume, media_uv_callback on_set_volume, void* cookie);
```

Request to set the volume.

**Parameters**:

- `handle` Async controller handle.
- `Volume` Volume level.
- `on_volume` Result callback function.
- `cookie` Callback argument of `on_volume`.

**Returns**:

Returns 0 on success, or a negative error code on failure.

**Note**:

- This API is not implemented yet.


### media_uv_session_query

```c
int media_uv_session_query(void* handle, media_uv_object_callback on_query, void* cookie);
```

Query the full state information.

**Parameters**:

- `handle` Async controller handle.
- `on_query` Callback that receives the metadata pointer.
- `cookie` Callback argument.

**Returns**:

Returns 0 on success, or a negative error code on failure.


### media_uv_session_get_state

```c
int media_uv_session_get_state(void* handle, media_uv_int_callback on_state, void* cookie);
```

Get the current state.

**Parameters**:

- `handle` Async controller handle.
- `on_state` Result callback function.
- `cookie` Callback argument of `on_state`.

**Returns**:

Returns 0 on success, or a negative error code on failure.

**Note**:

- This API is not implemented yet. Use `media_uv_session_query` instead.


### media_uv_session_get_position

```c
int media_uv_session_get_position(void* handle, media_uv_unsigned_callback on_position, void* cookie);
```

Get the current playback position.

**Parameters**:

- `handle` Async controller handle.
- `on_position` Result callback function.
- `cookie` Callback argument of `on_position`.

**Returns**:

Returns 0 on success, or a negative error code on failure.

**Note**:

- This API is not implemented yet. Use `media_uv_session_query` instead.


### media_uv_session_get_duration

```c
int media_uv_session_get_duration(void* handle, media_uv_unsigned_callback on_duration, void* cookie);
```

Get the current duration.

**Parameters**:

- `handle` Async controller handle.
- `on_duration` Result callback function.
- `cookie` Callback argument of `on_duration`.

**Returns**:

Returns 0 on success, or a negative error code on failure.

**Note**:

- This API is not implemented yet. Use `media_uv_session_query` instead.


### media_uv_session_get_volume

```c
int media_uv_session_get_volume(void* handle, media_uv_int_callback on_get_volume, void* cookie);
```

Get the current volume.

**Parameters**:

- `handle` Async controller handle.
- `on_volume` Result callback function.
- `cookie` Callback argument of `on_volume`.

**Returns**:

Returns 0 on success, or a negative error code on failure.

**Note**:

- This API is not implemented yet. Use `media_uv_session_query` instead.


### media_uv_session_register

```c
void* media_uv_session_register(void* loop, const char* params, media_event_callback on_event, void* cookie);
```

Register as a session controllee to receive control messages.

**Parameters**:

- `loop` The `uv_loop_t*` event loop handle of the current thread.
- `params` Unused; pass `NULL`.
- `on_event` Callback to receive control messages.
- `cookie` Callback argument.

**Returns**:

void*    Async controllee handle, or NULL on failure.


### media_uv_session_unregister

```c
int media_uv_session_unregister(void* handle, media_uv_callback on_release);
```

Unregister self.

**Parameters**:

- `handle` Async controllee handle.
- `on_release` Resource release callback for the caller.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_session_notify

```c
int media_uv_session_notify(void* handle, int event, int result, const char* extra, media_uv_callback on_notify, void* cookie);
```

Notify the result of a control message. After receiving MEDIA_EVENT_* from `on_event`, as the controllee you should handle the control message; after acknowledging it, call this API to send the response to the controller.

**Parameters**:

- `handle` Async controllee handle.
- `event` The event to notify.
- `result` Event result; usually `0` on success, a negative errno on failure.
- `extra` Additional string message for the event; pass `NULL` when not needed.
- `on_notify` Notification acknowledgment callback.
- `cookie` Callback argument.

**Returns**:

Returns `0` on success, or a negative errno on failure.


### media_uv_session_update

```c
int media_uv_session_update(void* handle, const media_metadata_t* data, media_uv_callback on_update, void* cookie);
```

Update metadata to the session.

**Parameters**:

- `handle` Async controllee handle.
- `data` Metadata to update.
- `on_update` Update acknowledgment callback.
- `cookie` Callback argument.

**Returns**:

Returns `0` on success, or a negative errno on failure.


