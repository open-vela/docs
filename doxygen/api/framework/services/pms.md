# PMS API

Package Manager Service（PMS）是 openvela XMS 系统中的包管理模块。

## 功能特性

- 提供包安装功能
- 提供包信息查询能力
- 提供包卸载能力

## 示例

**通过命令行进行包管理**

安装包：

```
pm install [packagename]
```

查询已安装的包：

```
pm list
```

**通过源码使用包管理工具**

安装包：

```cpp
#include <pm/PackageManager.h>

PackageManager pm;
InstallParam parms;
pm.installPackage(parms);
```

获取所有包信息：

```cpp
#include <pm/PackageManager.h>

PackageManager pm;
std::vector<PackageInfo> pgInfos;
pm.getAllPackageInfo(&pgInfos);
```

卸载包：

```cpp
#include <pm/PackageManager.h>

PackageManager pm;
UninstallParam parms;
pm.uninstallPackage(parms);
```

## 核心类

### PackageManager

头文件：`#include <pm/PackageManager.h>`

客户端侧访问 PMS 能力的门面类。提供的主要操作：

- `installPackage(InstallParam)` — 安装应用包
- `uninstallPackage(UninstallParam)` — 卸载应用包
- `getAllPackageInfo(std::vector<PackageInfo>*)` — 查询所有已安装包信息
- `getPackageInfo(packageName, PackageInfo*)` — 查询指定包信息
- `getAllPackageName(std::vector<std::string>*)` — 查询所有已安装包名
- `getPackageSizeInfo(packageName, ...)` — 查询包占用空间
- `clearAppCache(packageName)` — 清理应用缓存
- `isFirstBoot()` — 查询是否首次启动

应用通常构造 `PackageManager` 实例后直接调用上述方法，内部通过 Binder 与 `PackageManagerService` 通信。

### PackageManagerService

头文件：`#include <pm/PackageManagerService.h>`

PMS 的服务端实现类，注册为系统服务。负责维护已安装包的元数据、执行实际的安装/卸载动作、处理权限与签名校验。开发者一般不直接使用该类。

### PackageInfo

头文件：`#include <pm/PackageInfo.h>`

描述单个安装包元数据的结构。主要字段包括：

- `packageName` / `name` — 包名与应用名
- `version` / `priority` / `appType` — 版本、优先级与应用类型
- `installedPath` / `installTime` / `size` — 安装路径、安装时间与占用大小
- `execfile` / `entry` / `manifest` — 可执行文件、入口与清单
- `activitiesInfo` / `servicesInfo` — 内部 Activity 与 Service 列表
- `shasum` — 签名摘要
- `userId` / `isSystemUI` — 用户 ID 与是否系统 UI
- `windowEnterAnim` / `windowExitAnim` — 窗口进入/退出动画配置

`PackageManager` 的查询接口返回该类型的结果。

### PackageTrace

头文件：`#include <PackageTrace.h>`

PMS 的 trace 打点宏集合，用于跟踪包管理操作路径，配合 openvela trace 工具分析性能。
