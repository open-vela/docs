# Media Policy API

Media Policy 是多媒体框架中的音频策略组件，负责将应用层的音频路由和音量需求映射为设备驱动的控制命令。在不同项目中，Media Policy 通过统一接口向应用提供服务，并使用项目特定的配置文件处理接口到控制命令的映射关系。

## media_policy.h

配置文件的设计者根据具体业务，在通用接口的基础上调整封装层。强烈不推荐用户直接调用通用接口。

```eval_rst

.. doxygenfile:: media_policy.h
  :project: doxygen

```
