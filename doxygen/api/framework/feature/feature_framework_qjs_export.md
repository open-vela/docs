# Feature QJS Export API

Feature 框架与 QuickJS 运行时之间的互操作接口。提供 `ft_value_t` 与 `JSValue` 相互转换的能力，仅在 QuickJS 前端场景下可用。

头文件：`#include <feature_qjs_exports.h>`

## openvela 实现说明

- **仅适用于 QuickJS**：本组接口只能在 QuickJS 运行时下调用，WAMR 等其他前端请勿使用
- **依赖 QuickJS 头文件**：`feature_qjs_exports.h` 内部包含 `quickjs/quickjs.h`，需要 QuickJS 对外开放的头文件可见
- **典型用途**：当 Feature 实现需要访问 QuickJS 原生 API（例如使用 QuickJS 专有 API 创建对象）时，通过本组接口与 Feature 框架的统一 `ft_value_t` 类型互转
- **不建议业务代码广泛使用**：绑定到 QuickJS 后将失去跨运行时的兼容性，应优先使用 `feature_context.h` 中的通用 API

## JSValue 与 ft_value_t 互转

### ft_from_jsvalue

```c
ft_value_t ft_from_jsvalue(ft_context_ref rt_ctx, JSValue val);
```

将 QuickJS 的 `JSValue` 转换为 Feature 框架的 `ft_value_t`。

**参数**：

- `rt_ctx` 当前 Feature 上下文引用。
- `val` 要转换的 QuickJS JSValue 对象。

**返回值**：

返回对应的 `ft_value_t` 对象。返回值的生命周期由 Feature 框架管理。

**注意**：

- 调用方应确保传入的 `JSValue` 在 `rt_ctx` 对应的 QuickJS Runtime 中有效
- 若返回的 `ft_value_t` 被保留到后续异步上下文，需使用 `feature_context.h` 中的相关接口控制其生命周期

### ft_to_jsvalue

```c
JSValue ft_to_jsvalue(ft_context_ref rt_ctx, ft_value_t val);
```

将 Feature 框架的 `ft_value_t` 转换为 QuickJS 的 `JSValue`。

**参数**：

- `rt_ctx` 当前 Feature 上下文引用。
- `val` 要转换的 `ft_value_t` 对象。

**返回值**：

返回对应的 `JSValue` 对象。该 `JSValue` 遵循 QuickJS 自身的引用计数规则，调用方负责通过 `JS_FreeValue` 在合适时机释放。

**注意**：

- 本接口会在 QuickJS Runtime 内分配对应的 JS 对象，返回前引用计数已加 1。
- 使用完成后必须调用 `JS_FreeValue` 释放，否则会导致 QuickJS 端的内存泄漏。

### ft_ctx_to_js_ctx

```c
JSContext* ft_ctx_to_js_ctx(ft_context_ref rt_ctx);
```

从 Feature 上下文引用中获取底层的 QuickJS `JSContext*`。

**参数**：

- `rt_ctx` 当前 Feature 上下文引用。

**返回值**：

成功时返回对应的 `JSContext*`，可直接作为 QuickJS 原生 API 的参数使用。

**注意**：

- 返回的 `JSContext*` 生命周期由 Feature 框架管理，**不要**手动调用 `JS_FreeContext` 释放。
- 仅在 QuickJS 前端下返回有效指针；其他前端下的行为未定义。
