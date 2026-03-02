# Feature QuickJS Export API

定义了在 QuickJS 的 `JSValue` 和 Feature 的 `ft_value_t` 之间进行转换的函数。当 Feature 框架运行在 QuickJS 引擎上时，开发者可以通过这些接口在两种值类型之间互相转换，也可以从 `ft_context_ref` 获取底层的 `JSContext` 指针。

```eval_rst

.. doxygenfile:: feature_qjs_exports.h
  :project: doxygen

```
