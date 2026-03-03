# KVDB API

## 一、接口简介

KVDB 提供了一套本地数据库的读写接口，底层基于开源的 UnQLite 数据库，API 设计参考 Android 的 properties 存取规范，同时提供了命令行工具以方便本地快速调试。

## 二、公共接口

### 1、properties.h

```eval_rst

.. doxygenfile:: properties.h
    :project: doxygen
```

### 2、kvdb.h

```eval_rst

.. doxygenfile:: kvdb.h
    :project: doxygen
```

### 3、CLI 命令行工具

查询属性：

```
nsh> getprop [key]
```

- `getprop`（不加参数）：列出当前所有 props
- `getprop <key>`：打印出 `<key>` 对应的 prop

设置属性：

```
nsh> setprop <key> [value]
```

- `setprop <key>`：删除 `<key>` 对应的 prop
- `setprop <key> <value>`：保存 `<key>`:`<value>` 到数据库
