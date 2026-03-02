# Feature Context API

Feature 框架提供了 `ft_value_t` 和 `ft_context_t` 两个核心类型，用于在 Native 层操作 JS 对象。虽然 Feature 框架提供了一组 API 和工具帮助开发者隔离 JS 环境，但在一些场景下，需要传递非常复杂的数据结构，而这些结构很难映射到具体的 C/C++ 结构体或对象上。为了解决该问题，Feature 框架对 JS 对象进行包装，并有限度地开放一些接口，方便开发者使用。

## 一、结构关系

`ft_value_t` 需要一个伴生对象 `ft_context_t`，该对象代表一个上下文，是 `ft_value_t` 必须的。下图是 JS 层的实现，但不同 Feature 环境的实现是不一样的。

<img src="./figures/ft_context.svg" alt="ft_value_t 与 ft_context_t 结构关系图" style="zoom: 80%;" />

## 二、ft_value_t API 的主要构成

`ft_value_t` 的 API 主要由 3 部分构成：

1. C Value 转成 `ft_value_t` 数据。
2. `ft_value_t` 数据转成 C Value。
3. object/array 的处理及 JSON 操作。

## 三、ft_value_t API 的使用

### 1、获取 ft_context_t

第一步是获取 `ft_context_t`，该对象可以通过 Feature 获取：

```c
ft_context_ref FeatureGetContext(FeatureInstanceHandle handle);
```

可以在任意一个 Feature 接口中调用。

### 2、ft_value_t 的使用

参照上面的 API，创建 `ft_value_t` 对象或做转换。

### 3、ft_value_t 的生命周期管理

如果不能正确释放 `ft_value_t` 对象，就可能导致内存泄漏。

```c
void ft_free_value(ft_context_ref ft_ctx, ft_value_t ft_val);
```

调用 `ft_free_value` 是有要求的，不是所有的场合都需要 free。

以下场合不需要 free：

- 当 `ft_value_t` 作为参数传递给 Feature 实现函数时。
- 当创建的 `ft_value_t` 对象需要返回给 JS 的时候。

以下场合需要 free：

- 当调用 `ft_from_xxx` 系列函数、`ft_new_object` 创建的对象。
- `ft_array_at` 返回的对象。
- `ft_obj_get_property` 获得的对象。
- `ft_parse_json` 获得的对象。

字符串需要 free：`ft_to_string` 得到的字符串需要调用 `ft_free_string` 来删除。这两个函数必须成对出现，而且需要注意：Feature 框架不保证 `ft_to_string` 获取的对象长期有效，如果有需要，开发者应该及时 copy 字符串的值。

```eval_rst

.. doxygenfile:: feature_context.h
  :project: doxygen

```
