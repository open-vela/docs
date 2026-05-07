# Feature Types API

Feature 框架的基础数据类型定义，供 Feature 开发者使用。

头文件：`#include <feature_types.h>`

## openvela 实现说明

- **前端无关**：将各类前端（QuickJS、WAMR 等）的对象封装为统一的 `ft_value_t` 类型，Feature 开发者无需感知具体前端差异
- **类型系统**：通过 `FeaturePrimitiveType` 枚举为参数传递提供统一的类型标识，内部通过 `FT_SET_PRIMITIVE_TYPE(base, flags)` 宏编码类型信息与内存管理标志
- **引用计数**：`TypeFlags` 标记类型是否需要托管内存（`TYPE_FLAGS_POINTER` 需要 `malloc/free`，`TYPE_FLAGS_VALUE` 则不需要）
- **错误码范围**：通用错误码从 200 开始，自定义错误码从 400 起，开发者可自行扩展

## 基本类型别名

为基本 C 类型提供带 `Ft` 前缀的别名，便于在 Feature 接口中标识类型语义。

```c
typedef int       FtInt;       // 等价于 int32_t
typedef int8_t    FtInt8;
typedef uint8_t   FtUint8;
typedef int16_t   FtInt16;
typedef uint16_t  FtUint16;
typedef int32_t   FtInt32;
typedef uint32_t  FtUint32;
typedef int64_t   FtInt64;
typedef uint64_t  FtUint64;
typedef float     FtFloat;
typedef double    FtDouble;
typedef bool      FtBool;
typedef const char*   FtString;  // 常量字符串
typedef ft_value_t*   FtAny;     // 通用 ft_value_t 引用

typedef int32_t   FtCallbackId;  // 回调 ID
typedef int32_t   FtEventId;     // 事件 ID
typedef int32_t   FtPromiseId;   // Promise ID
```

## 句柄类型

Feature 框架核心对象的不透明句柄，开发者只能通过框架 API 操作，不应直接访问底层结构。

```c
typedef void* FeatureRegistryHandle;    // Feature 注册表句柄
typedef void* FeatureManagerHandle;     // Feature 管理器句柄
typedef void* FeatureProtoHandle;       // Feature 原型句柄（一个快应用对应一个）
typedef void* FeatureInstanceHandle;    // Feature 实例句柄（每次 require 产生一个）
typedef void* FeatureInterfaceHandle;   // Feature 接口句柄
typedef void* FeatureRuntimeContext;    // 前端运行时上下文（如 QuickJS RuntimeContext）
typedef void* FeatureRawContextHandle;  // 原始运行时上下文

typedef struct _FeatureWorker* FeatureWorkerHandle;  // Worker 句柄
typedef uintptr_t FeatureType;          // Feature 类型标志
```

## 回调函数类型

```c
// 通用 Native 函数指针
typedef void (*NativeFunc)(void);

// Feature 异步任务回调
typedef void (*FeatureTaskCallback)(int status, void* data);

// Feature 异步任务回调扩展版（带 instance 句柄）
typedef void (*FeatureTaskCallbackExt)(int status, uint64_t data,
                                       FeatureInstanceHandle feature);

// 事件变更监听回调
typedef void (*FeatureEventChangeListener)(FeatureInstanceHandle data,
                                           FtEventId eid,
                                           FeatureEventStatus status);

// Manager userdata 释放回调
typedef void (*ManagerUserdataFreeCallback)(void* data);

// Feature 注册函数
typedef bool (*FeatureRegistryFunc)(FeatureRegistryHandle);
```

## 枚举类型

### FeatureTaskMode

Feature 异步任务的运行模式。

```c
enum FeatureTaskMode {
    FEATURE_TASK_MODE_FREE   = 0,  // 异步任务已结束
    FEATURE_TASK_MODE_NORMAL = 1,  // 异步任务正常运行
};
```

### FeaturePromiseType

Promise 类型标识。Feature 框架兼容传统 callback 和 Promise 两种异步模型。

```c
typedef enum FeaturePromiseType {
    FEATURE_PROMISE_TYPE_INVALID   = -1,  // 无效类型
    FEATURE_PROMISE_TYPE_PROMISE   = 0,   // Promise 模型
    FEATURE_PROMISE_TYPE_CALLBACKS = 1,   // Callback 模型
} FeaturePromiseType;
```

### TypeFlags

类型的内存管理标志，用于决定是否需要释放。

```c
enum TypeFlags {
    TYPE_FLAGS_VALUE             = 1,    // 值类型，无需释放
    TYPE_FLAGS_POINTER,                  // 指针类型，需要 malloc/free
    TYPE_FLAGS_RAWPOINTER         = TYPE_FLAGS_POINTER | 1,  // 原始指针，无需释放
    TYPE_FLAGS_UNMANAGED_POINTER  = TYPE_FLAGS_RAWPOINTER,   // 非托管指针
};
```

### FeaturePrimitiveType

参数传递时使用的原始类型编码。通过宏 `FT_SET_PRIMITIVE_TYPE(base, flags)` 将类型基数与内存管理标志组合编码。

```c
#define FT_SET_PRIMITIVE_TYPE(base, flags) ((base << 2) | (flags))

enum FeaturePrimitiveType {
    FT_VOID      = FT_SET_PRIMITIVE_TYPE(FT_VOID_BASE,    TYPE_FLAGS_VALUE),    // 1
    FT_INT       = FT_SET_PRIMITIVE_TYPE(FT_INT_BASE,     TYPE_FLAGS_VALUE),    // 5
    FT_INT8      = FT_SET_PRIMITIVE_TYPE(FT_INT8_BASE,    TYPE_FLAGS_VALUE),    // 9
    FT_UINT8     = FT_SET_PRIMITIVE_TYPE(FT_UINT8_BASE,   TYPE_FLAGS_VALUE),    // 13
    FT_INT16     = FT_SET_PRIMITIVE_TYPE(FT_INT16_BASE,   TYPE_FLAGS_VALUE),    // 17
    FT_UINT16    = FT_SET_PRIMITIVE_TYPE(FT_UINT16_BASE,  TYPE_FLAGS_VALUE),    // 21
    FT_INT32     = FT_SET_PRIMITIVE_TYPE(FT_INT32_BASE,   TYPE_FLAGS_VALUE),    // 25
    FT_UINT32    = FT_SET_PRIMITIVE_TYPE(FT_UINT32_BASE,  TYPE_FLAGS_VALUE),    // 29
    FT_INT64     = FT_SET_PRIMITIVE_TYPE(FT_INT64_BASE,   TYPE_FLAGS_VALUE),    // 33
    FT_UINT64    = FT_SET_PRIMITIVE_TYPE(FT_UINT64_BASE,  TYPE_FLAGS_VALUE),    // 37
    FT_FLOAT     = FT_SET_PRIMITIVE_TYPE(FT_FLOAT_BASE,   TYPE_FLAGS_VALUE),    // 41
    FT_DOUBLE    = FT_SET_PRIMITIVE_TYPE(FT_DOUBLE_BASE,  TYPE_FLAGS_VALUE),    // 45
    FT_BOOLEAN   = FT_SET_PRIMITIVE_TYPE(FT_BOOLEAN_BASE, TYPE_FLAGS_VALUE),    // 49
    FT_STRING    = FT_SET_PRIMITIVE_TYPE(FT_STRING_BASE,  TYPE_FLAGS_POINTER),  // 54
    FT_CHAR      = FT_STRING,                                                   // 54，与 FT_STRING 等价
    FT_ANY_REF   = FT_SET_PRIMITIVE_TYPE(FT_ANY_REF_BASE,  TYPE_FLAGS_POINTER), // 58
    FT_JSON_OBJ  = FT_SET_PRIMITIVE_TYPE(FT_JSON_OBJ_BASE, TYPE_FLAGS_POINTER), // 62
};
```

### FeatureErrorCode

Feature 框架的错误码定义。

```c
typedef enum FeatureErrorCode {
    FT_ERR_GENERAL           = 200,   // 通用错误
    FT_ERR_ARGS              = 202,   // 参数错误
    FT_ERR_TIMEOUT           = 204,   // 超时
    FT_ERR_IOERROR           = 300,   // IO 错误
    FT_ERR_PATH_NOT_EXISTS   = 301,   // 路径不存在
    FT_ERR_CUSTOM_BEGIN      = 400,   // 自定义错误码起点
    FT_ERR_TASK_FAILED       = 1000,  // 任务失败
    FT_ERR_TASK_NOT_EXISTS   = 1001,  // 任务不存在
    FT_ERR_CANCEL_ERROR_CODE = 1002,  // 取消错误
} FeatureErrorCode;
```

### FeatureEventStatus

事件变更状态，用于通知监听器事件被添加或移除。

```c
typedef enum FeatureEventStatus {
    FEATURE_EVENT_ADDED,    // 事件被添加
    FEATURE_EVENT_REMOVED,  // 事件被移除
} FeatureEventStatus;
```

### FeaturePermsRejectReason

权限拒绝原因。

```c
typedef enum FeaturePermsRejectReason {
    FEATURE_PERMS_DENIED = 400,  // 权限被拒绝
    FEATURE_PERMS_ERROR,         // 权限错误
    FEATURE_PERMS_NO_BG,         // 权限不允许后台
} FeaturePermsRejectReason;
```

### FeatureWorkerCancelResult

Worker 取消结果。

```c
enum FeatureWorkerCancelResult {
    FeatureWorkerCancelSuccess,       // 成功取消
    FeatureWorkerCancelPending,       // 任务处于 pending，未能取消
    FeatureWorkerCancelInvalid,       // Worker 无效
    FeatureWorkerCancelUnknownError,  // 未知错误
};
```

### FeatureWorkerState

Worker 运行状态。

```c
enum FeatureWorkerState {
    FEATURE_WORKER_PENDING,    // 等待中
    FEATURE_WORKER_RUNNING,    // 运行中
    FEATURE_WORKER_INVALID,    // 无效状态
    FEATURE_WORKER_RESOLVED,   // 已 resolve
    FEATURE_WORKER_REJECTED,   // 已 reject
    FEATURE_WORKER_FINISHED,   // 已完成
};
```

### FeatureManagerType

Feature 管理器类型。

```c
typedef enum FeatureManagerType {
    FEATURE_MANAGER_JS,    // JS 类型 Feature 管理器
    FEATURE_MANAGER_WAMR,  // WAMR 类型 Feature 管理器
} FeatureManagerType;
```

## 结构体

### FtArray

Feature 框架通用动态数组结构。

```c
typedef struct FtArray {
    int32_t _size;       // 当前数组实际元素数
    int32_t _capacity;   // 当前容量
    void*   _element;    // 元素指针
} FtArray;
```

### FtJsonObject

JSON 对象句柄，内部为柔性字符串。

```c
typedef struct _FtJsonObject {
    char str[0];  // 内部字符串数据
} *FtJsonObject;
```

### AppendData

用于向数组追加元素的通用联合体，支持多种基本类型。

```c
typedef union AppendData {
    int32_t     i32;  // 32 位有符号整数
    int64_t     i64;  // 64 位有符号整数
    uint32_t    u32;  // 32 位无符号整数
    uint64_t    u64;  // 64 位无符号整数
    float       f32;  // 单精度浮点
    double      f64;  // 双精度浮点
    void*       ptr;  // 任意指针
    const char* str;  // 字符串
} AppendData;
```

### FtVariParams

可变长参数包。

```c
typedef struct FtVariParams {
    int32_t     vari_count;  // 参数数量
    ft_value_t* vari_args;   // 参数数组指针
} FtVariParams;
```

### FeatureWorkerResult

Worker 的执行结果联合体。

```c
typedef union _FeatureWorkerResult {
    int64_t  ival;   // 有符号整数结果
    uint64_t uval;   // 无符号整数结果
    double   dval;   // 浮点结果
    char*    str;    // 字符串结果
    void*    ptr;    // 指针结果
} FeatureWorkerResult;
```

### VTable

Feature 接口创建时使用的虚函数表。

```c
typedef struct VTable {
    int               size;       // 成员数量
    NativeFunc        finalizer;  // 析构函数
    const NativeFunc* members;    // 成员函数数组
} VTable;
```

### FeatureManagerCreateInfo

创建 Feature 管理器时所需的配置信息。

```c
typedef struct FeatureManagerCreateInfo {
    FeatureRawContextHandle raw_ctx;       // 原始上下文句柄
    ReleaseRawContextCb     release_cb;    // 原始上下文释放回调
    FeatureManagerType      manager_type;  // 管理器类型（JS / WAMR）
    const char*             package_name;  // 快应用包名
} FeatureManagerCreateInfo;
```

### FeatureMemoryDump

内存诊断回调结构，用于在调试时统计内存使用情况。

```c
typedef struct {
    MemoryDumpCountCB     count;       // 单项内存计数回调
    MemoryDumpCountMetaCB count_meta;  // 带名称的元数据计数回调
    MemoryDumpSubCB       sub;         // 递归子项回调
} FeatureMemoryDump;
```

### ArgsErrorInfo

参数错误信息。当 Feature 调用参数类型不匹配时，通过 `ArgsErrorCb` 回调传递此信息。

```c
typedef struct {
    int         argc;        // 参数个数
    void*       argv;        // 参数列表指针
    int         error_code;  // 错误码
    const char* error_msg;   // 错误消息
} ArgsErrorInfo;
```

### FeaturePermissionsInfo

权限检查信息。

```c
typedef struct FeaturePermissionsInfo {
    const FeaturePermissions* permissions;   // 权限描述
    const char*               api_name;      // API 名称
    bool                      has_async_cbs; // 是否带异步回调
} FeaturePermissionsInfo;
```

### FeatureRegistryTable

Feature 注册表，用于批量注册多个 Feature。

```c
typedef struct _FeatureRegistryTable {
    size_t              count;    // 条目数
    FeatureRegistryFunc data[];   // 注册函数数组（柔性成员）
} FeatureRegistryTable, *FeatureRegistryTableHandle;
```
