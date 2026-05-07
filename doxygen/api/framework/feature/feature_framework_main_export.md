# Feature Main Export API

Feature 管理器（Feature Manager）的生命周期管理与全局配置接口。主要用于快应用框架初始化、绑定运行时事件循环、注册 Feature 以及管理权限。

头文件：`#include <feature_main_exports.h>`

## openvela 实现说明

- **使用场景**：这组 API 主要由快应用框架实现者（Runtime 整合层）使用，Feature 插件开发者一般不直接调用
- **与 Feature 管理器的关系**：一个 Feature 管理器对应一个独立的快应用实例，通过 `FeatureCreateManager` 创建，使用结束后必须调用 `FeatureFreeManager` 释放
- **事件循环集成**：通过 `FeatureSetUVLoop` 绑定 libuv 事件循环，实现异步任务的调度。必须在 `FeatureCreateInstance` 之前完成绑定
- **权限回调机制**：通过 `FeatureSetPermissionsCallback` 注册统一的权限检查入口，所有需要权限的 Feature 调用都会触发回调，调用方需显式 `Grant` 或 `Reject`

## 快应用框架示例代码

```cpp
#ifdef CONFIG_FEATURE_FRAMEWORK
    FeatureManagerCreateInfo ft_info;
    ft_info.raw_ctx = (FeatureRawContextHandle)(qrt->env.ctx);
    ft_info.release_cb = nullptr;
    ft_info.manager_type = FEATURE_MANAGER_JS;
    ft_info.package_name = app->packageName();
    qrt->pFeatureMgr = FeatureCreateManager(&ft_info);
    FeatureSetArgsErrorCb(qrt->pFeatureMgr, on_feature_args_error, qrt);
    FeatureSetManagerUserData(qrt->pFeatureMgr, "app", app);
    FeatureSetUVLoop(qrt->pFeatureMgr, qrt->loop);
#endif
```

## 管理器生命周期

### FeatureCreateManager

```c
FeatureManagerHandle FeatureCreateManager(FeatureManagerCreateInfo* pinfo);
```

根据给定的配置信息创建一个 Feature 管理器实例。

**参数**：

- `pinfo` Feature 管理器的创建配置，包含原始运行时上下文、释放回调、管理器类型和快应用包名。详见 `FeatureManagerCreateInfo`。

**返回值**：

成功时返回有效的 `FeatureManagerHandle` 句柄；失败时返回 `NULL`。

### FeatureFreeManager

```c
void FeatureFreeManager(FeatureManagerHandle handle);
```

释放 Feature 管理器。释放前应先调用 `FeatureUnsetUVLoop` 解绑事件循环。

**参数**：

- `handle` 待释放的 Feature 管理器句柄。

### FeatureUninit

```c
void FeatureUninit(FeatureManagerHandle handle);
```

对 Feature 管理器执行反初始化操作。清理内部状态但不释放句柄本身。

**参数**：

- `handle` Feature 管理器句柄。

## 全局配置

### FeatureSetArgsErrorCb

```c
void FeatureSetArgsErrorCb(FeatureManagerHandle handle, ArgsErrorCb cb, void* data);
```

为 Feature 管理器注册参数错误回调。当任一 Feature 调用的参数类型不匹配时，会触发该回调。

**参数**：

- `handle` Feature 管理器句柄。
- `cb` 参数错误回调，签名为 `bool (*)(void* data, ArgsErrorInfo* args_info)`。
- `data` 传递给回调的用户数据。

### FeatureSetPackageVersion

```c
void FeatureSetPackageVersion(FeatureManagerHandle handle, const char* package_version);
```

设置当前管理器对应快应用的包版本号。版本号可通过 `FeatureGetPackageVersion` 查询。

**参数**：

- `handle` Feature 管理器句柄。
- `package_version` 快应用版本号字符串。

### FeatureSetUVLoop

```c
void FeatureSetUVLoop(FeatureManagerHandle handle, uv_loop_t* loop);
```

为 Feature 管理器绑定 libuv 事件循环。所有 `FeaturePost`、`FeatureWorker*` 等异步任务都会在该 loop 上调度。

**参数**：

- `handle` Feature 管理器句柄。
- `loop` libuv 事件循环指针。

**注意**：

- 必须在 `FeatureCreateInstance` 之前调用。
- 同一个 `uv_loop_t` 可以被多个 Feature 管理器共享，但通常建议每个快应用实例独占一个 loop。

### FeatureUnsetUVLoop

```c
void FeatureUnsetUVLoop(FeatureManagerHandle handle);
```

解绑 Feature 管理器的 libuv 事件循环。解绑后所有未完成的异步任务将失效。

**参数**：

- `handle` Feature 管理器句柄。

**注意**：

- 必须在 `FeatureFreeManager` 之前调用。

## 运行时访问

### FeatureManagerGetContext

```c
ft_context_ref FeatureManagerGetContext(FeatureManagerHandle handle);
```

从 Feature 管理器获取对应的 Feature 上下文引用，可用于 `ft_value_t` 相关操作。

**参数**：

- `handle` Feature 管理器句柄。

**返回值**：

返回 `ft_context_ref`，失败时返回 `NULL`。

### FeatureSetManagerUserData

```c
void FeatureSetManagerUserData(FeatureManagerHandle handle, const char* name, void* data);
```

按名称在 Feature 管理器上挂载用户数据。可用于在各个 Feature 实例之间共享信息。

**参数**：

- `handle` Feature 管理器句柄。
- `name` 用户数据名称（键）。
- `data` 用户数据指针。

### FeatureHasFeature

```c
bool FeatureHasFeature(FeatureManagerHandle handle, FtString feature_method);
```

判断给定名称的 Feature 是否已注册到当前管理器。

**参数**：

- `handle` Feature 管理器句柄。
- `feature_method` 要查询的 Feature 名称。

**返回值**：

Feature 已注册时返回 `true`，否则返回 `false`。

## Feature 操作

### FeatureRequire

```c
ft_value_t FeatureRequire(FeatureManagerHandle handle,
                          ft_value_t binding_obj, const char* name);
```

按名称向 Feature 管理器请求一个 Feature 实例。等价于 JS 层的 `require('@system.xxx')`。

**参数**：

- `handle` Feature 管理器句柄。
- `binding_obj` 绑定对象（通常是 Feature 所在的 JS 全局对象）。
- `name` Feature 名称。

**返回值**：

返回封装了 Feature 实例的 `ft_value_t`。失败时返回 undefined 类型的 `ft_value_t`。

**注意**：

- 每次 `FeatureRequire` 都会产生一个独立的 Feature 实例。

### FeatureFindFeature

```c
ft_value_t FeatureFindFeature(FeatureManagerHandle handle, const char* name);
```

查找已创建的 Feature 实例而不会新建实例。

**参数**：

- `handle` Feature 管理器句柄。
- `name` Feature 名称。

**返回值**：

返回 Feature 实例对应的 `ft_value_t`；若未找到，返回 undefined。

### FeatureCreateFeature

```c
ft_value_t FeatureCreateFeature(FeatureManagerHandle handle,
                                ft_value_t prototype, ft_value_t binding_obj);
```

根据原型创建一个 Feature 实例。用于需要直接操作原型对象的高级场景。

**参数**：

- `handle` Feature 管理器句柄。
- `prototype` Feature 原型对象。
- `binding_obj` 绑定对象。

**返回值**：

成功时返回新建 Feature 实例的 `ft_value_t`；失败时返回 undefined。

## 内存诊断

### FeatureDumpMemory

```c
void FeatureDumpMemory(FeatureManagerHandle feature_manager,
                       FeatureMemoryDump* dump, void* userdata);
```

回调式的 Feature 框架内存占用诊断接口，便于上层整合自定义的内存统计能力。

**参数**：

- `feature_manager` Feature 管理器句柄。
- `dump` 内存诊断回调结构体，包含 `count`、`count_meta`、`sub` 三类回调，详见 `FeatureMemoryDump`。
- `userdata` 透传给各回调的用户数据。

## 权限管理

### FeatureSetPermissionsCallback

```c
void FeatureSetPermissionsCallback(FeatureManagerHandle hmanager,
                                   FeaturePermissionsCb cb, void* data);
```

注册权限检查回调。当某个 Feature API 需要权限时，框架会触发此回调，由业务层决定授予或拒绝。

**参数**：

- `hmanager` Feature 管理器句柄。
- `cb` 权限检查回调，签名为 `void (*)(FeaturePermissionsHandle, const FeaturePermissionsInfo*, void*)`。
- `data` 透传给回调的用户数据。

**注意**：

- 回调内必须调用 `FeatureGrantPermissions` 或 `FeatureRejectPermissions` 之一，否则对应的 Feature 调用会一直挂起。

### FeatureGrantPermissions

```c
void FeatureGrantPermissions(FeatureManagerHandle hmanager,
                             FeaturePermissionsHandle handle);
```

授予一次权限请求。调用后，对应的 Feature API 调用会继续执行。

**参数**：

- `hmanager` Feature 管理器句柄。
- `handle` 权限请求句柄（由权限回调传入）。

### FeatureRejectPermissions

```c
void FeatureRejectPermissions(FeatureManagerHandle hmanager,
                              FeaturePermissionsHandle handle,
                              FeaturePermsRejectReason reason);
```

拒绝一次权限请求。调用后，对应的 Feature API 调用会返回权限错误。

**参数**：

- `hmanager` Feature 管理器句柄。
- `handle` 权限请求句柄。
- `reason` 拒绝原因，详见 `FeaturePermsRejectReason`：
    - `FEATURE_PERMS_DENIED`：权限被拒绝
    - `FEATURE_PERMS_ERROR`：权限检查错误
    - `FEATURE_PERMS_NO_BG`：不允许后台调用
