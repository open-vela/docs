# media policy API

在架构中，policy是media framework的一个组件，在不同的项目中向APP提供统一的接口，把用户的路由和音量的需求映射成对设备驱动的控制命令；在不同的项目中，policy会使用不同的配置文件来处理policy接口到控制命令的映射关系。

## media_policy.h

配置文件的设计者根据具体业务，在通用接口的基础上调整封装层，强烈不推荐用户直接调用通用接口。

```eval_rst

.. doxygenfile:: media_policy.h
  :project: doxygen

```
