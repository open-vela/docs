# PMS API

Package Manager Service（PMS）是 openvela XMS 系统中的包管理模块。

## 功能特性

- 提供包安装功能
- 提供包信息查询能力
- 提供包卸载能力

## 示例

- 通过命令行进行包管理

    安装包：

    ```
    pm install [packagename]
    ```

    查询已安装的包：

    ```
    pm list
    ```

- 通过源码使用包管理工具

    安装包：

    ```c++
    #include "pm/PackageManager.h"

    PackageManager pm;
    InstallParam parms;
    pm.installPackage(parms);
    ```

    获取所有包信息：

    ```c++
    #include "pm/PackageManager.h"

    PackageManager pm;
    std::vector<PackageInfo> pgInfos;
    pm.getAllPackageInfo(&pgInfos);
    ```

    卸载包：

    ```c++
    #include "pm/PackageManager.h"

    PackageManager pm;
    UninstallParam parms;
    pm.uninstallPackage(parms);
    ```

## PackageInfo.h

```eval_rst
.. doxygenfile:: PackageInfo.h
    :project: doxygen
```

## PackageManager.h

```eval_rst
.. doxygenfile:: PackageManager.h
    :project: doxygen
```

## PackageManagerService.h

```eval_rst
.. doxygenfile:: PackageManagerService.h
    :project: doxygen
```

## PackageTrace.h

```eval_rst
.. doxygenfile:: PackageTrace.h
    :project: doxygen
```
