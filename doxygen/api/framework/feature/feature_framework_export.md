# Feature Export API

Feature 框架为 Feature 开发者提供的核心运行时接口，涵盖内存与数组管理、引用访问、回调、Promise、事件、异步 Worker、JSON 对象与注册表等能力。

头文件：`#include <feature_exports.h>`

## openvela 实现说明

- **内存所有权**：`FeatureMalloc` / `FeatureInstanceAlloc*` 分配的内存由框架托管，使用 `FeatureDupValue` 增加引用，`FeatureFreeValue` 减少引用，引用计数为 0 时释放
- **数组类型**：`FtArray` 由框架管理，通过 `FeatureCreateArray` / `FeatureArrayCopy` 创建，支持 `FeatureArrayAppend` / `FeatureArrayInsertAfter` 等原位操作
- **回调与 Promise**：Feature 接口支持 Callback 与 Promise 两种异步模型，通过 `FeatureGetPromiseType` 查询当前调用使用的类型
- **Worker 机制**：`FeatureCreateWorker` 创建的 Worker 在独立线程或 uv work queue 中执行，完成后回主线程通知结果
- **线程安全**：调用 `FeaturePost` / `FeaturePostExt` 将任务抛回 Feature 管理器绑定的事件循环，避免跨线程操作 `FeatureInstanceHandle`
- **引用管理**：使用 `FeatureDupInstanceHandle` 延长 `FeatureInstanceHandle` 生命周期，避免在异步回调中访问已销毁的实例
- **实例 Detach**：在异步回调里必须通过 `FeatureInstanceIsDetached` 判断实例是否已分离，分离后不得再调用该句柄

## 内存分配

### FeatureInstanceAlloc

```c
void* FeatureInstanceAlloc(FeatureInstanceHandle handle, size_t size);
```

为 Feature 实例分配内存。分配的内存由框架托管，可通过 `FeatureFreeValue` 释放。

**参数**：

- `handle` Feature 实例句柄。
- `size` 申请字节数。

**返回值**：

成功时返回内存起始指针；失败时返回 `NULL`。

### FeatureInstanceAllocType

```c
void* FeatureInstanceAllocType(FeatureInstanceHandle hInst, size_t size, FeatureType type);
```

按类型为 Feature 实例分配内存，分配的内存携带类型标记。

**参数**：

- `hInst` Feature 实例句柄。
- `size` 申请字节数。
- `type` 类型标识，详见 `FeatureType`。

**返回值**：

成功时返回内存起始指针；失败时返回 `NULL`。

### FeatureInstanceAllocProtobuf

```c
void* FeatureInstanceAllocProtobuf(FeatureInstanceHandle handle,
                                    const ProtobufCMessageDescriptor* desc);
```

根据 Protobuf 消息描述符为 Feature 实例分配内存，并自动完成字段初始化。

**参数**：

- `handle` Feature 实例句柄。
- `desc` Protobuf 消息描述符指针。

**返回值**：

成功时返回已初始化的消息对象指针；失败时返回 `NULL`。

### FeatureInstanceDupValue

```c
void* FeatureInstanceDupValue(void* ptr);
```

为通过 `FeatureInstanceAlloc*` 分配的指针增加引用计数。

**参数**：

- `ptr` 待增加引用的指针，必须是 `FeatureInstanceAlloc*` 返回值。

**返回值**：

返回原指针（方便链式使用）。

### FeatureInstanceFreeValue

```c
void FeatureInstanceFreeValue(void* ptr);
```

减少 `FeatureInstanceAlloc*` 分配指针的引用计数，为 0 时真正释放。

**参数**：

- `ptr` 待释放的指针。

### FeatureMalloc

```c
void* FeatureMalloc(size_t size, FeatureType featureType);
```

按类型分配一块 Feature 托管内存。

**参数**：

- `size` 申请字节数。
- `featureType` 类型标识。

**返回值**：

成功时返回内存指针；失败时返回 `NULL`。

### FeatureDupValue

```c
void* FeatureDupValue(void* ptr);
```

增加 Feature 值的引用计数。仅适用于 `FeatureMalloc` 分配的指针。

**参数**：

- `ptr` 待增加引用的指针。

**返回值**：

返回原指针。

### FeatureFreeValue

```c
void FeatureFreeValue(void* ptr);
```

减少 Feature 值的引用计数，为 0 时真正释放。仅适用于 `FeatureMalloc` 分配的指针。

**参数**：

- `ptr` 待释放的指针。

### FeatureGetValueRefCount

```c
int32_t FeatureGetValueRefCount(void* ptr);
```

获取 Feature 值的当前引用计数。仅对 `FeatureMalloc` 分配的指针有效。

**参数**：

- `ptr` 查询目标指针。

**返回值**：

返回引用计数值。

### FeatureStrCopy

```c
char* FeatureStrCopy(FeatureInstanceHandle handle, const char* str);
```

基于原始 C 字符串创建一个由 Feature 框架托管的字符串副本。

**参数**：

- `handle` Feature 实例句柄。
- `str` 源字符串。

**返回值**：

成功时返回新字符串指针；失败时返回 `NULL`。返回值可通过 `FeatureStrAddRef` 增加引用，或通过 `FeatureInstanceFreeValue` 释放。

### FeatureStrAddRef

```c
#define FeatureStrAddRef(ptr) FeatureInstanceDupValue(ptr)
```

为 Feature 字符串增加一次引用计数，等价于 `FeatureInstanceDupValue`。

**参数**：

- `ptr` Feature 字符串指针。

**返回值**：

返回原指针（便于链式调用）。

## 数组管理

### FeatureCreateArray

```c
FtArray* FeatureCreateArray(FeatureInstanceHandle handle, size_t capacity,
                             FeatureType element_type);
```

创建一个空的 `FtArray`，预留给定容量。

**参数**：

- `handle` Feature 实例句柄。
- `capacity` 初始容量。
- `element_type` 元素类型，详见 `FeatureType`。

**返回值**：

成功时返回新数组指针；失败时返回 `NULL`。

### FeatureArrayCopy

```c
FtArray* FeatureArrayCopy(FeatureInstanceHandle handle, FeatureType element_type,
                          const void* data, size_t count);
```

从现有数据拷贝创建一个 `FtArray`。拷贝时对每个元素执行类型相关的深拷贝。

**参数**：

- `handle` Feature 实例句柄。
- `element_type` 元素类型。
- `data` 源数据起始指针。
- `count` 元素个数。

**返回值**：

成功时返回新数组指针；失败时返回 `NULL`。

### FeatureArrayCopyRaw

```c
FtArray* FeatureArrayCopyRaw(FeatureInstanceHandle handle, FeatureType element_type,
                              const void* data, size_t count);
```

从现有数据按原始字节拷贝创建 `FtArray`，不对元素做深拷贝。

**参数**：

- `handle` Feature 实例句柄。
- `element_type` 元素类型。
- `data` 源数据起始指针。
- `count` 元素个数。

**返回值**：

成功时返回新数组指针；失败时返回 `NULL`。

### FeatureArrayResize

```c
FtArray* FeatureArrayResize(FtArray* arr, size_t new_size);
```

调整数组大小。若 `new_size` 大于当前容量则扩容，小于则截断。

**参数**：

- `arr` 待调整的数组。
- `new_size` 新的元素数量。

**返回值**：

成功时返回调整后的数组指针（可能被 realloc 指向新地址）；失败时返回 `NULL`。

### FeatureArrayGetLength

```c
size_t FeatureArrayGetLength(FtArray* arr);
```

获取数组当前元素数量。

**参数**：

- `arr` 目标数组。

**返回值**：

返回当前元素数量。

### FeatureArrayGetData

```c
void* FeatureArrayGetData(FtArray* arr, int start);
```

获取数组从指定索引开始的元素指针。

**参数**：

- `arr` 目标数组。
- `start` 起始索引。

**返回值**：

返回元素起始指针。索引越界时返回 `NULL`。

### FeatureArrayAppend

```c
FtArray* FeatureArrayAppend(FtArray* arr, const void* data);
```

向数组末尾追加一个元素（深拷贝）。

**参数**：

- `arr` 目标数组。
- `data` 待追加元素的数据指针。

**返回值**：

成功时返回数组指针；失败时返回 `NULL`。

### FeatureArrayAppendRaw

```c
FtArray* FeatureArrayAppendRaw(FtArray* arr, const void* data);
```

向数组末尾追加一个元素（原始字节拷贝，不做深拷贝）。

**参数**：

- `arr` 目标数组。
- `data` 待追加元素的数据指针。

**返回值**：

成功时返回数组指针；失败时返回 `NULL`。

### FeatureArrayClear

```c
int FeatureArrayClear(FtArray* arr);
```

清空数组中所有元素，保留已分配的容量。

**参数**：

- `arr` 目标数组。

**返回值**：

成功时返回 0；失败时返回负数。

### FeatureArrayRemove

```c
int FeatureArrayRemove(FtArray* arr, int start, size_t count);
```

从指定位置开始删除 `count` 个元素。

**参数**：

- `arr` 目标数组。
- `start` 起始索引。
- `count` 删除元素个数。

**返回值**：

成功时返回 0；失败时返回负数。

### FeatureArrayInsertAfter

```c
int FeatureArrayInsertAfter(FtArray* arr, int start, const void* data, size_t count);
```

在指定位置**之后**插入 `count` 个元素（深拷贝）。

**参数**：

- `arr` 目标数组。
- `start` 参考位置索引。
- `data` 元素数据起始指针。
- `count` 插入元素个数。

**返回值**：

成功时返回 0；失败时返回负数。

### FeatureArrayInsertRawAfter

```c
int FeatureArrayInsertRawAfter(FtArray* arr, int start, const void* data, size_t count);
```

同 `FeatureArrayInsertAfter`，但使用原始字节拷贝。

**参数**：

- `arr` 目标数组。
- `start` 参考位置索引。
- `data` 元素数据起始指针。
- `count` 插入元素个数。

**返回值**：

成功时返回 0；失败时返回负数。

### FeatureArrayInsertBefore

```c
int FeatureArrayInsertBefore(FtArray* arr, int start, const void* data, size_t count);
```

在指定位置**之前**插入 `count` 个元素（深拷贝）。

**参数**：

- `arr` 目标数组。
- `start` 参考位置索引。
- `data` 元素数据起始指针。
- `count` 插入元素个数。

**返回值**：

成功时返回 0；失败时返回负数。

### FeatureArrayInsertRawBefore

```c
int FeatureArrayInsertRawBefore(FtArray* arr, int start, const void* data, size_t count);
```

同 `FeatureArrayInsertBefore`，但使用原始字节拷贝。

**参数**：

- `arr` 目标数组。
- `start` 参考位置索引。
- `data` 元素数据起始指针。
- `count` 插入元素个数。

**返回值**：

成功时返回 0；失败时返回负数。

## Feature 句柄与上下文访问

### FeatureGetProtoHandle

```c
FeatureProtoHandle FeatureGetProtoHandle(FeatureInstanceHandle handle);
```

从 Feature 实例句柄获取对应的原型句柄。

**参数**：

- `handle` Feature 实例句柄。

**返回值**：

返回对应的 `FeatureProtoHandle`；失败时返回 `NULL`。

### FeatureGetProtoData

```c
void* FeatureGetProtoData(FeatureProtoHandle handle);
```

获取绑定到 Feature 原型的用户数据。该数据对所有该原型的实例可见。

**参数**：

- `handle` Feature 原型句柄。

**返回值**：

返回用户数据指针；未绑定则返回 `NULL`。

### FeatureSetProtoData

```c
void FeatureSetProtoData(FeatureProtoHandle handle, void* data);
```

在 Feature 原型上挂载用户数据。

**参数**：

- `handle` Feature 原型句柄。
- `data` 用户数据指针。

### FeatureGetObjectData

```c
void* FeatureGetObjectData(FeatureInstanceHandle handle);
```

获取绑定到 Feature 实例的用户数据。

**参数**：

- `handle` Feature 实例句柄。

**返回值**：

返回用户数据指针；未绑定则返回 `NULL`。

### FeatureSetObjectData

```c
void FeatureSetObjectData(FeatureInstanceHandle handle, void* data);
```

在 Feature 实例上挂载用户数据。

**参数**：

- `handle` Feature 实例句柄。
- `data` 用户数据指针。

### FeatureGetContext

```c
ft_context_ref FeatureGetContext(FeatureInstanceHandle handle);
```

从 Feature 实例获取其运行时上下文（前端相关）。

**参数**：

- `handle` Feature 实例句柄。

**返回值**：

返回 `ft_context_ref`；失败时返回 `NULL`。

### FeatureGetPackageName

```c
const char* FeatureGetPackageName(FeatureProtoHandle handle);
```

获取 Feature 原型对应的快应用包名。

**参数**：

- `handle` Feature 原型句柄。

**返回值**：

成功时返回包名字符串；失败时返回 `NULL`。返回值由框架管理，不要手动释放。

### FeatureGetPackageVersion

```c
const char* FeatureGetPackageVersion(FeatureProtoHandle handle);
```

获取 Feature 原型对应的快应用版本号。

**参数**：

- `handle` Feature 原型句柄。

**返回值**：

成功时返回版本号字符串；失败时返回 `NULL`。

### FeatureGetEnvironmentName

```c
const char* FeatureGetEnvironmentName(FeatureProtoHandle handle);
```

获取 Feature 原型所在的运行环境名称。

**参数**：

- `handle` Feature 原型句柄。

**返回值**：

成功时返回环境名字符串；失败时返回 `NULL`。

### FeatureInstanceGetManagerUserData

```c
void* FeatureInstanceGetManagerUserData(FeatureInstanceHandle handle, const char* name);
```

从 Feature 实例所属的管理器中按名称获取用户数据。

**参数**：

- `handle` Feature 实例句柄。
- `name` 用户数据名称。

**返回值**：

成功时返回用户数据指针；未找到返回 `NULL`。

### FeatureGetManagerHandleFromInstance

```c
FeatureManagerHandle FeatureGetManagerHandleFromInstance(FeatureInstanceHandle handle);
```

从 Feature 实例句柄获取其所属的 Feature 管理器句柄。

**参数**：

- `handle` Feature 实例句柄。

**返回值**：

成功时返回 `FeatureManagerHandle`；失败时返回 `NULL`。

### FeatureGetManagerHandleFromProto

```c
FeatureManagerHandle FeatureGetManagerHandleFromProto(FeatureProtoHandle handle);
```

从 Feature 原型句柄获取其所属的 Feature 管理器句柄。

**参数**：

- `handle` Feature 原型句柄。

**返回值**：

成功时返回 `FeatureManagerHandle`；失败时返回 `NULL`。

### FeatureGetUVLoop

```c
uv_loop_t* FeatureGetUVLoop(FeatureManagerHandle handle);
```

获取 Feature 管理器绑定的 libuv 事件循环。

**参数**：

- `handle` Feature 管理器句柄。

**返回值**：

成功时返回 `uv_loop_t*`；未绑定时返回 `NULL`。

### FeatureDupInstanceHandle

```c
FeatureInstanceHandle FeatureDupInstanceHandle(FeatureInstanceHandle handle);
```

增加 Feature 实例句柄的引用计数，返回同一句柄（可链式使用）。

**参数**：

- `handle` Feature 实例句柄。

**返回值**：

返回原句柄。

### FeatureFreeInstanceHandle

```c
void FeatureFreeInstanceHandle(FeatureInstanceHandle handle);
```

减少 Feature 实例句柄的引用计数，为 0 时释放。

**参数**：

- `handle` Feature 实例句柄。

### FeatureInstanceIsDetached

```c
bool FeatureInstanceIsDetached(FeatureInstanceHandle handle);
```

判断 Feature 实例是否已与其原型分离（一般发生在实例销毁过程中）。异步回调在使用句柄前应先调用此接口判断。

**参数**：

- `handle` Feature 实例句柄。

**返回值**：

已分离返回 `true`；未分离返回 `false`。分离后不得再调用该句柄上的任何接口。

### FeatureCreateInterface

```c
FeatureInterfaceHandle FeatureCreateInterface(FeatureInstanceHandle handle, VTable* vtable);
```

基于虚函数表创建一个 Feature 接口句柄。用于以对象接口形式向前端暴露方法。

**参数**：

- `handle` Feature 实例句柄。
- `vtable` 虚函数表，详见 `VTable`。

**返回值**：

成功时返回新建的 `FeatureInterfaceHandle`；失败时返回 `NULL`。

## Manager 用户数据操作

### FeatureSetManagerUserData

```c
void FeatureSetManagerUserData(FeatureManagerHandle handle, const char* name, void* data);
```

按名称向 Feature 管理器挂载用户数据。同一个 Manager 可通过不同名称挂载多个数据。

**参数**：

- `handle` Feature 管理器句柄。
- `name` 用户数据名称。
- `data` 用户数据指针。

### FeatureSetManagerUserDataWithFreeCallback

```c
void* FeatureSetManagerUserDataWithFreeCallback(FeatureManagerHandle handle,
    const char* name, void* data, ManagerUserdataFreeCallback free_cb);
```

按名称挂载用户数据，并注册释放回调。Manager 销毁时会调用 `free_cb` 清理用户数据。

**参数**：

- `handle` Feature 管理器句柄。
- `name` 用户数据名称。
- `data` 用户数据指针。
- `free_cb` 释放回调，签名为 `void (*)(void* data)`。

**返回值**：

返回旧值（若之前已绑定过同名数据），否则返回 `NULL`。

### FeatureManagerHasUserData

```c
bool FeatureManagerHasUserData(FeatureManagerHandle handle, const char* name);
```

判断管理器是否已绑定指定名称的用户数据。

**参数**：

- `handle` Feature 管理器句柄。
- `name` 用户数据名称。

**返回值**：

已绑定返回 `true`；否则返回 `false`。

### FeatureGetManagerUserData

```c
void* FeatureGetManagerUserData(FeatureManagerHandle handle, const char* name);
```

按名称获取管理器上绑定的用户数据。

**参数**：

- `handle` Feature 管理器句柄。
- `name` 用户数据名称。

**返回值**：

成功返回用户数据指针；未找到返回 `NULL`。

## 回调管理

### FeatureInvokeCallback

```c
bool FeatureInvokeCallback(FeatureInstanceHandle handle, FtCallbackId cid, ...);
```

通过回调 ID 触发一次 JS 层的回调函数。可变参数按 Feature 接口声明的类型依次传入。

**参数**：

- `handle` Feature 实例句柄。
- `cid` 回调 ID。
- `...` 传给回调的可变参数。

**返回值**：

成功返回 `true`；失败返回 `false`（例如回调 ID 已失效或实例已分离）。

### FeatureInvokeCallbackCount

```c
bool FeatureInvokeCallbackCount(FeatureInstanceHandle handle, FtCallbackId cid,
                                 int count, ...);
```

同 `FeatureInvokeCallback`，但显式指定参数个数。适合在参数数量动态变化的场景下使用。

**参数**：

- `handle` Feature 实例句柄。
- `cid` 回调 ID。
- `count` 参数个数。
- `...` 可变参数列表。

**返回值**：

成功返回 `true`；失败返回 `false`。

### FeatureRemoveCallback

```c
bool FeatureRemoveCallback(FeatureInstanceHandle handle, FtCallbackId cid);
```

从 Feature 实例中移除指定 ID 的回调。移除后再调用 `FeatureInvokeCallback` 会失败。

**参数**：

- `handle` Feature 实例句柄。
- `cid` 回调 ID。

**返回值**：

成功返回 `true`；回调 ID 不存在返回 `false`。

### FeatureCheckCallbackId

```c
bool FeatureCheckCallbackId(FeatureInstanceHandle handle, FtCallbackId cid);
```

检查指定回调 ID 对应的 JS 函数是否仍然有效。

**参数**：

- `handle` Feature 实例句柄。
- `cid` 回调 ID。

**返回值**：

函数仍存在且有效返回 `true`；否则返回 `false`。

## 异步任务投递

### FeaturePost

```c
bool FeaturePost(FeatureInstanceHandle handle, FeatureTaskCallback task_cb, void* data);
```

将任务投递到 Feature 管理器绑定的事件循环执行。常用于跨线程回到主线程上操作 Feature 实例。

**参数**：

- `handle` Feature 实例句柄。
- `task_cb` 任务回调，签名为 `void (*)(int status, void* data)`。
- `data` 传递给回调的用户数据。

**返回值**：

成功投递返回 `true`；失败返回 `false`。

**注意**：

- 在 `task_cb` 内使用 `FeatureInstanceIsDetached` 判断句柄是否已分离。分离后禁止继续使用该句柄。

### FeaturePostExt

```c
bool FeaturePostExt(FeatureInstanceHandle handle, FeatureTaskCallbackExt task_cb_ext,
                    uint64_t data);
```

扩展版 `FeaturePost`。回调签名带实例句柄，便于在回调内直接访问实例。

**参数**：

- `handle` Feature 实例句柄。
- `task_cb_ext` 扩展任务回调，签名为 `void (*)(int status, uint64_t data, FeatureInstanceHandle feature)`。
- `data` 传递给回调的 64 位用户数据。

**返回值**：

成功返回 `true`；失败返回 `false`。

**注意**：

- 在回调内同样需要 `FeatureInstanceIsDetached` 检查实例状态。

## Promise 管理

Feature 框架同时支持 Callback 和 Promise 两种异步模型，二者在 Feature 实现内部使用相同的 `FtPromiseId` 引用。以下接口用于完成异步调用的 resolve 或 reject。

### FeaturePromiseResolve

```c
bool FeaturePromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, ...);
```

以可变参数的形式 resolve Promise。仅支持传递一个参数。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `...` 传递的参数。

**返回值**：

成功返回 `true`；失败返回 `false`。

### FeaturePromiseReject

```c
bool FeaturePromiseReject(FeatureInstanceHandle handle, FtPromiseId pid,
                          int code, const char* msg);
```

以错误码与错误消息 reject Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `code` 错误码。
- `msg` 错误消息。

**返回值**：

成功返回 `true`；失败返回 `false`。

### FeatureGetPromiseType

```c
enum FeaturePromiseType FeatureGetPromiseType(FeatureInstanceHandle handle, FtPromiseId pid);
```

获取当前异步调用使用的模型类型。Feature 实现可据此选择调用 Callback 或 Promise 对应接口。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。

**返回值**：

返回枚举 `FeaturePromiseType`：

- `FEATURE_PROMISE_TYPE_INVALID`：无效（通常表示 Promise 已失效）
- `FEATURE_PROMISE_TYPE_PROMISE`：Promise 模型
- `FEATURE_PROMISE_TYPE_CALLBACKS`：Callback 模型

## Promise 类型化 Resolve

以下一组接口按类型特化 resolve Promise，避免使用可变参数带来的类型不确定性。所有接口成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtStringPromiseResolve

```c
FtBool FeatureFtStringPromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtString val);
```

以字符串 resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` 字符串结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtIntPromiseResolve

```c
FtBool FeatureFtIntPromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtInt val);
```

以 `FtInt`（int32）resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` int32 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtUint32PromiseResolve

```c
FtBool FeatureFtUint32PromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtUint32 val);
```

以 `FtUint32` resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` uint32 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtInt8PromiseResolve

```c
FtBool FeatureFtInt8PromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtInt8 val);
```

以 `FtInt8` resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` int8 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtUint8PromiseResolve

```c
FtBool FeatureFtUint8PromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtUint8 val);
```

以 `FtUint8` resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` uint8 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtInt16PromiseResolve

```c
FtBool FeatureFtInt16PromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtInt16 val);
```

以 `FtInt16` resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` int16 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtUint16PromiseResolve

```c
FtBool FeatureFtUint16PromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtUint16 val);
```

以 `FtUint16` resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` uint16 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtInt64PromiseResolve

```c
FtBool FeatureFtInt64PromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtInt64 val);
```

以 `FtInt64` resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` int64 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtUint64PromiseResolve

```c
FtBool FeatureFtUint64PromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtUint64 val);
```

以 `FtUint64` resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` uint64 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtFloatPromiseResolve

```c
FtBool FeatureFtFloatPromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtFloat val);
```

以 `FtFloat`（float）resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` float 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtDoublePromiseResolve

```c
FtBool FeatureFtDoublePromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtDouble val);
```

以 `FtDouble`（double）resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` double 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtBoolPromiseResolve

```c
FtBool FeatureFtBoolPromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtBool val);
```

以 `FtBool` resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` bool 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtAnyPromiseResolve

```c
FtBool FeatureFtAnyPromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtAny val);
```

以 `FtAny`（`ft_value_t*`）resolve Promise。可用于返回任意类型结果。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` `ft_value_t*` 结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

### FeatureFtArrayPromiseResolve

```c
FtBool FeatureFtArrayPromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, FtArray* val);
```

以 `FtArray*` resolve Promise。

**参数**：

- `handle` Feature 实例句柄。
- `pid` Promise ID。
- `val` 数组结果。

**返回值**：

成功时返回 `FT_TRUE`，失败时返回 `FT_FALSE`。

## 事件管理

### FeatureGetEventId

```c
FtEventId FeatureGetEventId(FeatureInstanceHandle handle, const char* name);
```

根据事件名称查询对应的事件 ID。

**参数**：

- `handle` Feature 实例句柄。
- `name` 事件名称。

**返回值**：

成功时返回有效的事件 ID（正整数）；事件不存在时返回 `≤ 0`。

### FeatureGetEventName

```c
const char* FeatureGetEventName(FeatureInstanceHandle handle, FtEventId eid);
```

根据事件 ID 获取事件名称。

**参数**：

- `handle` Feature 实例句柄。
- `eid` 事件 ID。

**返回值**：

成功时返回事件名字符串；不存在时返回 `NULL`。

### FeatureEmitEvent

```c
bool FeatureEmitEvent(FeatureInstanceHandle handle, FtEventId eid, ...);
```

按事件 ID 触发事件，支持向事件订阅者传递可变参数。

**参数**：

- `handle` Feature 实例句柄。
- `eid` 事件 ID。
- `...` 事件携带的数据，类型需与 Feature 接口声明一致。

**返回值**：

成功触发返回 `true`；失败返回 `false`（例如事件不存在、实例已分离）。

### FeatureEmitEventByName

```c
bool FeatureEmitEventByName(FeatureInstanceHandle handle, const char* name, ...);
```

按事件名称触发事件。内部会先通过 `FeatureGetEventId` 查询 ID 再触发。

**参数**：

- `handle` Feature 实例句柄。
- `name` 事件名称。
- `...` 事件携带的数据。

**返回值**：

成功返回 `true`；失败返回 `false`。

### FeatureSetEventChangeListener

```c
void FeatureSetEventChangeListener(FeatureInstanceHandle handle,
                                    FeatureEventChangeListener listener);
```

为 Feature 实例设置事件变更监听器。当事件订阅者的数量发生变化时（有订阅者加入或离开），会触发回调。

**参数**：

- `handle` Feature 实例句柄。
- `listener` 事件变更监听器，签名为 `void (*)(FeatureInstanceHandle, FtEventId, FeatureEventStatus)`。
    - 状态为 `FEATURE_EVENT_ADDED` 表示添加订阅
    - 状态为 `FEATURE_EVENT_REMOVED` 表示移除订阅

### FeatureGetEventCallbackCount

```c
int FeatureGetEventCallbackCount(FeatureInstanceHandle handle, FtEventId eid);
```

按事件 ID 查询当前注册的订阅者数量。可用于在无订阅者时跳过事件触发以节省开销。

**参数**：

- `handle` Feature 实例句柄。
- `eid` 事件 ID。

**返回值**：

返回订阅者数量；不存在或失败时返回 0。

### FeatureGetEventCallbackCountByName

```c
static inline int FeatureGetEventCallbackCountByName(FeatureInstanceHandle handle, const char* name);
```

按事件名称查询当前注册的订阅者数量。内部通过 `FeatureGetEventId` + `FeatureGetEventCallbackCount` 实现。

**参数**：

- `handle` Feature 实例句柄。
- `name` 事件名称。

**返回值**：

返回订阅者数量；不存在时返回 0。

## 异步任务 Worker

Worker 机制用于将耗时任务放入后台执行，执行完毕后回到主线程通知结果。适用于文件 IO、计算密集等场景。

### FeatureCreateWorker

```c
FeatureWorkerHandle FeatureCreateWorker(FeatureInstanceHandle handle, FtPromiseId pid,
    size_t buf_size,
    void (*do_work)(FeatureWorkerHandle),
    void (*do_after_worker)(FeatureWorkerHandle),
    void (*free)(void*));
```

创建一个 Worker 对象，准备投递到后台执行。

**参数**：

- `handle` Feature 实例句柄。
- `pid` 关联的 Promise ID，用于 Worker 完成后触发 resolve/reject。
- `buf_size` Worker 私有缓冲区大小，可用来在两个回调间传递数据。
- `do_work` 后台执行函数，在 worker 线程中运行。
- `do_after_worker` 完成回调，在主线程运行，通常在此调用 `FeatureWorkerResolve` 或 `FeatureWorkerReject`。
- `free` 资源释放函数，Worker 销毁时调用。

**返回值**：

成功时返回 `FeatureWorkerHandle`；失败返回 `NULL`。

### FeatureWorkerCommit

```c
bool FeatureWorkerCommit(FeatureInstanceHandle handle, FeatureWorkerHandle hworker);
```

提交 Worker 到后台开始执行。

**参数**：

- `handle` Feature 实例句柄。
- `hworker` Worker 句柄。

**返回值**：

提交成功返回 `true`；失败返回 `false`。

### FeatureWorkerResolve

```c
void FeatureWorkerResolve(FeatureInstanceHandle handle, FeatureWorkerHandle hworker,
                          FeatureWorkerResult result);
```

通知 Worker 以成功结果完成，触发关联 Promise 的 resolve。通常在 `do_after_worker` 回调内调用。

**参数**：

- `handle` Feature 实例句柄。
- `hworker` Worker 句柄。
- `result` 执行结果，详见 `FeatureWorkerResult`。

### FeatureWorkerReject

```c
void FeatureWorkerReject(FeatureInstanceHandle handle, FeatureWorkerHandle hworker,
                         int errcode, const char* err_msg);
```

通知 Worker 以失败结果完成，触发关联 Promise 的 reject。

**参数**：

- `handle` Feature 实例句柄。
- `hworker` Worker 句柄。
- `errcode` 错误码。
- `err_msg` 错误消息。

### FeatureWorkerIsValid

```c
bool FeatureWorkerIsValid(FeatureInstanceHandle handle, FeatureWorkerHandle hworker);
```

判断 Worker 是否仍然有效。

**参数**：

- `handle` Feature 实例句柄。
- `hworker` Worker 句柄。

**返回值**：

有效返回 `true`；失效或已完成返回 `false`。

### FeatureWorkerGetState

```c
int FeatureWorkerGetState(FeatureWorkerHandle hworker);
```

获取 Worker 当前状态。

**参数**：

- `hworker` Worker 句柄。

**返回值**：

返回 `FeatureWorkerState` 枚举值：

- `FEATURE_WORKER_PENDING`：等待中
- `FEATURE_WORKER_RUNNING`：运行中
- `FEATURE_WORKER_INVALID`：无效
- `FEATURE_WORKER_RESOLVED`：已 resolve
- `FEATURE_WORKER_REJECTED`：已 reject
- `FEATURE_WORKER_FINISHED`：已完成

### FeatureWorkerCancel

```c
int FeatureWorkerCancel(FeatureInstanceHandle handle, FeatureWorkerHandle hworker);
```

尝试取消 Worker 的执行。处于 pending 状态的任务无法立即取消。

**参数**：

- `handle` Feature 实例句柄。
- `hworker` Worker 句柄。

**返回值**：

返回 `FeatureWorkerCancelResult` 枚举值：

- `FeatureWorkerCancelSuccess`：成功取消
- `FeatureWorkerCancelPending`：Worker 处于 pending，未能取消
- `FeatureWorkerCancelInvalid`：Worker 无效
- `FeatureWorkerCancelUnknownError`：未知错误

## JSON 对象

### FeatureNewJsonObject

```c
FtJsonObject FeatureNewJsonObject(const char* str);
```

基于给定字符串创建 JSON 对象。

**参数**：

- `str` JSON 字符串。

**返回值**：

成功返回 `FtJsonObject`；失败返回 `NULL`。

### FeatureAllocJsonObject

```c
FtJsonObject FeatureAllocJsonObject(size_t str_len);
```

按指定字符串长度分配 JSON 对象空间（不初始化内容）。

**参数**：

- `str_len` 字符串长度。

**返回值**：

成功返回 `FtJsonObject`；失败返回 `NULL`。

### FeatureGetJsonString

```c
const char* FeatureGetJsonString(const FtJsonObject json_obj);
```

获取 JSON 对象对应的字符串视图。

**参数**：

- `json_obj` JSON 对象。

**返回值**：

成功返回字符串指针；失败返回 `NULL`。返回指针由框架管理，不要手动释放。

## Feature 注册

### FeatureRegisterFeatures

```c
bool FeatureRegisterFeatures(FeatureRegistryHandle handle,
                              const FeatureRegistryTableHandle regTable);
```

将一组 Feature 批量注册到 Feature 注册表中。通常在模块初始化时调用。

**参数**：

- `handle` Feature 注册表句柄。
- `regTable` 注册条目表，详见 `FeatureRegistryTable`。

**返回值**：

全部注册成功返回 `true`；任一注册失败返回 `false`。
