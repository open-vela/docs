# Telephony Data API

Telephony Data TAPI 提供 openvela Telephony 蜂窝数据的相关功能：

- 对外提供蜂窝数据相关功能接口，包括开关蜂窝数据、开关数据漫游、获取当前使用数据的 SLOT ID 和当前蜂窝数据链路是否激活等接口。
- 对内根据客户端的需求进行蜂窝数据链路的激活、去激活和相应的状态维护，并将当前数据链路连接状态上报给客户端。
- 在开启蜂窝数据且网络状态满足的情况下，始终保持一路 Internet 类型 APN 链路存在。当客户端对 APN 特定参数（iptype、username、password 和 apn）进行修改或新建一路默认上网的 Internet 类型 APN 时，会进行 reattach 操作，去激活掉原有的 Internet 类型 APN 链路，用更新后的 APN 参数重新进行激活。

## tapi_data.h

```eval_rst

.. doxygenfile:: tapi_data.h
    :project: doxygen
```
