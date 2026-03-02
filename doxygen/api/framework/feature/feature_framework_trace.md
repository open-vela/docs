# Feature Trace API

Feature 框架中用于 trace 打点的一系列宏定义。当启用 `CONFIG_FEATURE_USE_SCHED_NOTE` 配置时，这些宏会调用 NuttX 的 `sched_note` 接口进行性能追踪；未启用时，宏展开为空操作，不产生额外开销。

```eval_rst

.. doxygenfile:: feature_trace.h
  :project: doxygen

```
