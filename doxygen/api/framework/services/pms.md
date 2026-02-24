# PMS API

Package Management Module for Vela's XMS Module

## Table of Contents

- [Features](#features)
- [Examples](#examples)

## Features

- Provides package installation functionality
- Provides package information querying capability
- Provides package uninstallation capability

## Examples

- Package management can be done through the command line

    Install a package:

    ```
    pm install [packagename]
    ```

    Query which packages are installed:

    ```
    pm list
    ```

- Use the package management tool through source code

    Install a package using the following format:

    ```
    #include "pm/PackageManager.h"

    PackageManager pm;
    InstallParam parms;
    pm.installPackage(parms);
    ```

    Retrieve all package-related information with:

    ```
    #include "pm/PackageManager.h"

    PackageManager pm;
    std::vector<PackageInfo> pgInfos;
    pm.getAllPackageInfo(&pgInfos);
    ```

    Uninstall a package using:

    ```
    #include "pm/PackageManager.h"

    PackageManager pm;
    UninstallParam parms;
    pm.uninstallPackage(parms);
    ```

# PackageInfo.h
```c++
.. doxygenfile:: PackageInfo.h
  :project: doxygen
```

# PackageManager.h
```c++
.. doxygenfile:: PackageManager.h
  :project: doxygen
```

# PackageManagerService.h
```c++
.. doxygenfile:: PackageManagerService.h
  :project: doxygen
```

# PackageTrace.h
```c++
.. doxygenfile:: PackageTrace.h
  :project: doxygen
```