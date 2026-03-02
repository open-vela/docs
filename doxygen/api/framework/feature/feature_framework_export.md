# Feature Export API

Feature 框架提供了一系列功能接口，包括数据存储、内存管理、异步编程、回调、事件等，帮助开发者实现其功能。

## 一、数据存储

Feature 框架提供了 4 处可以存放用户数据的地方，分别是 `FeatureManagerHandle`、`FeatureProtoHandle`、`FeatureInstanceHandle`、`FeatureInterfaceHandle`。其中 `FeatureManagerHandle` 一般供快应用框架使用，开发者应关注另外三个 Handle。

```c
void* FeatureGetProtoData(FeatureProtoHandle handle);
void FeatureSetProtoData(FeatureProtoHandle handle, void* data);
void* FeatureGetObjectData(FeatureInstanceHandle handle);
void FeatureSetObjectData(FeatureInstanceHandle handle, void* data);
void FeatureSetManagerUserData(FeatureManagerHandle handle, const char* name, void* data);
void* FeatureGetManagerUserData(FeatureManagerHandle handle, const char* name);
...
```

## 二、内存管理

Feature 框架提供一组基础 API，用于内存分配和回收。

```c
void* FeatureMalloc(size_t size, FeatureType type);
void* FeatureDupValue(void* ptr);
void FeatureFree(void* ptr);
```

## 三、异步编程与回调

Feature 框架提供一组基础 API，用于异步编程和回调。

```c
bool FeatureInvokeCallback(FeatureInstanceHandle handle, FtCallbackId cid, ...);
bool FeatureInvokeCallbackCount(FeatureInstanceHandle handle, FtCallbackId cid,
    int count, ...);
bool FeatureRemoveCallback(FeatureInstanceHandle handle, FtCallbackId cid);
bool FeatureCheckCallbackId(FeatureInstanceHandle handle, FtCallbackId cid);
bool FeaturePromiseResolve(FeatureInstanceHandle handle, FtPromiseId pid, ...);
bool FeaturePromiseReject(FeatureInstanceHandle handle, FtPromiseId pid,
    int code, const char* msg);
```

## 四、事件

Feature 框架提供一组基础 API，用于事件处理。

```c
FtEventId FeatureGetEventId(FeatureInstanceHandle handle, const char* name);
const char* FeatureGetEventName(FeatureInstanceHandle handle, FtEventId eid);
bool FeatureEmitEvent(FeatureInstanceHandle handle, FtEventId eid, ...);
bool FeatureEmitEventByName(FeatureInstanceHandle handle, const char* name, ...);
void FeatureSetEventChangeListener(FeatureInstanceHandle handle, FeatureEventChangeListener listener);
int FeatureGetEventCallbackCount(FeatureInstanceHandle handle, FtEventId eid);
...
```

```eval_rst

.. doxygenfile:: feature_exports.h
  :project: doxygen

```
