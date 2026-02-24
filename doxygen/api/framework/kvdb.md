# KVDB API

## 一、接口简介
KVDB提供了一套本地数据库的读写接口，底层基于开源的UnQLite数据库，API设计参考Android的properties存取规范，同时提供了命令行工具以方便本地快速调试。

## 二、公共接口

### API of properties.h

```eval_rst

.. doxygenfile:: properties.h
  :project: doxygen
```

### API of kvdb.h

```eval_rst

.. doxygenfile:: kvdb.h
  :project: doxygen
```

### CLI

`nsh> getprop s s`

`Usage: getprop [key]`

* getprop(不加参数)：列出当前所有props
* getprop `<key>`: 打印出 `<key>`对应的prop

`nsh> setprop`

`Usage: setprop <key> [value]`

* setprop `<key>`: 删除 `<key>`对应的prop
* setprop `<key>` `<value>`: 保存 `<key>`:`<value>`到数据库
