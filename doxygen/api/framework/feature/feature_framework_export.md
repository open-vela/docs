## feature_framework_export API

框架提供了一系列feature功能接口：包括数据存储、内存管理，异步编程、回调、事件等；帮助开发者实现其功能。

### 数据存储

feature框架提供了4处可以存放用户数据的地方，分别是FeatureManagerHandle、FeatureProtoHandle、FeatureInstanceHandle、FeatureInterfaceHandle.其中FeatureManagerHandle一般供快应用框架使用，开发者应关注另外三个handle.

```c
void* FeatureGetProtoData(FeatureProtoHandle handle);
void FeatureSetProtoData(FeatureProtoHandle handle, void* data);
void* FeatureGetObjectData(FeatureInstanceHandle handle);
void FeatureSetObjectData(FeatureInstanceHandle handle, void* data);
void FeatureSetManagerUserData(FeatureManagerHandle handle, const char* name, void* data);
void* FeatureGetManagerUserData(FeatureManagerHandle handle, const char* name);
...
```

### 内存管理
feature框架提供一组基础API, 用于内存分配和回收。

```c
void* FeatureMalloc(size_t size, FeatureType type);
void* FeatureDupValue(void* ptr);
void FeatureFree(void* ptr);
```

### 异步编程、回调
feature框架提供一组基础API, 用于异步编程、回调。
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

### 事件
feature框架提供一组基础API, 用于事件。
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

.. doxygenfile:: feature_export.h
  :project: doxygen

```