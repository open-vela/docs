# Keystore Client API

openvela Keystore 方案移植自 Android Keystore 服务框架，遵循 Keystore/Keymaster 标准接口。其中 Keymaster 层支持多种实现方式，包括对接 MiTee、纯软件实现以及为安全芯片（SE）定制的实现。

openvela Keystore 向上层以 Keystore C API 的方式，为账号 SDK 等应用场景提供密钥管理与安全存储能力，使用方无需关注底层的硬件差异和具体存储细节。

## client.h

```eval_rst

.. doxygenfile:: keystore/client.h
  :project: doxygen
```
