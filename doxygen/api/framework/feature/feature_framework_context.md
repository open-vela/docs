# Feature Context API

Feature 框架提供的统一数据类型与上下文操作接口。通过 `ft_value_t` 封装前端（QuickJS、WAMR 等）的原生对象，开发者无需感知具体前端差异即可完成类型转换、数组对象操作与内存管理。

头文件：`#include <feature_context.h>`

## openvela 实现说明

- **核心数据类型 `ft_value_t`**：统一封装前端的 JSValue/Wasm 对象，根据目标平台是否 64 位使用 16 字节或 8 字节存储
- **`ft_context_ref`**：伴随 `ft_value_t` 的上下文对象，所有 API 都需要传入，用于定位具体的前端 Runtime
- **值类型 vs 引用类型**：
    - `ft_from_int` / `ft_from_bool` 等返回值类型，无需显式释放
    - `ft_from_string` / `ft_from_buffer` / `ft_new_object` 等返回引用类型，必须通过 `ft_free_value` 释放
- **释放规则**：
    - **无需释放**：Feature 实现函数入参、作为返回值传回前端的 `ft_value_t`
    - **必须释放**：`ft_from_xxx` 创建的对象、`ft_new_object` 新建对象、`ft_array_at` 取出的元素、`ft_obj_get_property` 返回的属性、`ft_parse_json` 解析结果
    - 字符串：`ft_to_string` 返回的 `const char*` 必须用 `ft_free_string` 释放

## 类型与上下文访问

### ft_context_get_data

```c
void* ft_context_get_data(ft_context_ref ft_ctx);
```

获取当前 Feature 上下文关联的用户数据指针。该用户数据由 Feature 管理器在初始化阶段绑定。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。

**返回值**：

返回关联的用户数据指针，若未绑定则返回 `NULL`。

### ft_get_type

```c
ft_type ft_get_type(ft_context_ref ft_ctx, ft_value_t ft_val);
```

获取给定 `ft_value_t` 的类型。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `ft_val` 待查询类型的 `ft_value_t`。

**返回值**：

返回值类型枚举 `ft_type`：

- `FT_TYPE_NULL`：null
- `FT_TYPE_UNDEF`：undefined
- `FT_TYPE_NONE`：未定义值
- `FT_TYPE_NUMBER`：数值
- `FT_TYPE_BOOL`：布尔
- `FT_TYPE_STRING`：字符串
- `FT_TYPE_ARRAY`：数组
- `FT_TYPE_BUFFER`：二进制缓冲区
- `FT_TYPE_TYPED_BUFFER`：类型化缓冲区
- `FT_TYPE_OBJECT`：对象

### ft_undefined

```c
ft_value_t ft_undefined(ft_context_ref ft_ctx);
```

构造 undefined 类型的 `ft_value_t`。用于向前端返回"无值"结果。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。

**返回值**：

返回一个类型为 `FT_TYPE_UNDEF` 的 `ft_value_t`。该值为值类型，无需显式释放。

## 基本类型转换（Native → ft_value_t）

以下接口将 C 原生类型转换为 `ft_value_t`，便于传递给前端。

### ft_from_int

```c
ft_value_t ft_from_int(ft_context_ref ft_ctx, int32_t val);
```

将 32 位有符号整数转换为 `ft_value_t`。返回值为值类型，无需释放。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 32 位有符号整数值。

**返回值**：

返回对应的 `ft_value_t`（类型为 `FT_TYPE_NUMBER`）。

### ft_from_uint

```c
ft_value_t ft_from_uint(ft_context_ref ft_ctx, uint32_t val);
```

将 32 位无符号整数转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 32 位无符号整数值。

**返回值**：

返回对应的 `ft_value_t`。

### ft_from_int64

```c
ft_value_t ft_from_int64(ft_context_ref ft_ctx, int64_t val);
```

将 64 位有符号整数转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 64 位有符号整数值。

**返回值**：

返回对应的 `ft_value_t`。

### ft_from_uint64

```c
ft_value_t ft_from_uint64(ft_context_ref ft_ctx, uint64_t val);
```

将 64 位无符号整数转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 64 位无符号整数值。

**返回值**：

返回对应的 `ft_value_t`。

### ft_from_double

```c
ft_value_t ft_from_double(ft_context_ref ft_ctx, double val);
```

将双精度浮点数转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 双精度浮点值。

**返回值**：

返回对应的 `ft_value_t`。

### ft_from_bool

```c
ft_value_t ft_from_bool(ft_context_ref ft_ctx, bool val);
```

将布尔值转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 布尔值。

**返回值**：

返回对应的 `ft_value_t`（类型为 `FT_TYPE_BOOL`）。

### ft_from_string

```c
ft_value_t ft_from_string(ft_context_ref ft_ctx, const char* val);
```

将 C 字符串转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 以 `\0` 结尾的 C 字符串。

**返回值**：

返回对应的 `ft_value_t`（类型为 `FT_TYPE_STRING`）。

**注意**：

- 返回的 `ft_value_t` 为引用类型，**必须**通过 `ft_free_value` 释放。
- 实现会拷贝 `val` 的内容，调用后原指针可以立即释放。

## 二进制缓冲区转换

### ft_from_buffer

```c
ft_value_t ft_from_buffer(ft_context_ref ft_ctx, uint8_t* buff, uint32_t size);
```

将 Native 字节缓冲区封装为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `buff` 字节缓冲区起始指针。
- `size` 缓冲区字节数。

**返回值**：

返回对应的 `ft_value_t`（类型为 `FT_TYPE_BUFFER`）。

**注意**：

- 返回的 `ft_value_t` 为引用类型，必须通过 `ft_free_value` 释放。

### ft_from_typed_buffer

```c
ft_value_t ft_from_typed_buffer(ft_context_ref ft_ctx, uint8_t* buff,
                                uint32_t size, FtTypedArrayType type);
```

将 Native 缓冲区封装为前端的类型化数组（Typed Array）。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `buff` 字节缓冲区起始指针。
- `size` 缓冲区字节数。
- `type` 类型化数组的元素类型，详见 `FtTypedArrayType`：
    - `FT_Int8Array` / `FT_Uint8Array`
    - `FT_Int16Array` / `FT_Uint16Array`
    - `FT_Int32Array` / `FT_Uint32Array`
    - `FT_Float32Array` / `FT_Float64Array`

**返回值**：

返回对应的 `ft_value_t`（类型为 `FT_TYPE_TYPED_BUFFER`）。必须通过 `ft_free_value` 释放。

**示例**：

```c
uint8_t* buff = ft_to_buffer(ft_ctx, &size, data);
// 对 buff 做处理
ft_value_t ret = ft_from_typed_buffer(ft_ctx, buff, size, FT_Uint8Array);
```

### ft_parse_json

```c
ft_value_t ft_parse_json(ft_context_ref ft_ctx, const char* buf,
                         size_t buf_len, const char* filename);
```

解析 JSON 字符串为 `ft_value_t` 对象。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `buf` JSON 字符串指针。
- `buf_len` JSON 字符串长度（字节）。
- `filename` 用于错误信息定位的文件名，可传 `NULL`。

**返回值**：

成功时返回解析得到的 `ft_value_t`；失败时返回类型为 `FT_TYPE_UNDEF` 的值。

**注意**：

- 返回的 `ft_value_t` 为引用类型，必须通过 `ft_free_value` 释放。

## 数组类型转换（Native 数组 → ft_value_t）

将 Native 数组转换为 `ft_value_t` 数组。所有返回值均为引用类型，必须通过 `ft_free_value` 释放。

### ft_from_int_array

```c
ft_value_t ft_from_int_array(ft_context_ref ft_ctx, int32_t* val, uint32_t size);
```

将 int32 数组转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 源数组指针。
- `size` 数组元素个数。

**返回值**：

返回对应的 `ft_value_t`（类型为 `FT_TYPE_ARRAY`）。

### ft_from_uint_array

```c
ft_value_t ft_from_uint_array(ft_context_ref ft_ctx, uint32_t* val, uint32_t size);
```

将 uint32 数组转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 源数组指针。
- `size` 数组元素个数。

**返回值**：

返回对应的 `ft_value_t`。

### ft_from_int64_array

```c
ft_value_t ft_from_int64_array(ft_context_ref ft_ctx, int64_t* val, uint32_t size);
```

将 int64 数组转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 源数组指针。
- `size` 数组元素个数。

**返回值**：

返回对应的 `ft_value_t`。

### ft_from_uint64_array

```c
ft_value_t ft_from_uint64_array(ft_context_ref ft_ctx, uint64_t* val, uint32_t size);
```

将 uint64 数组转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 源数组指针。
- `size` 数组元素个数。

**返回值**：

返回对应的 `ft_value_t`。

### ft_from_bool_array

```c
ft_value_t ft_from_bool_array(ft_context_ref ft_ctx, bool* val, uint32_t size);
```

将布尔数组转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 源数组指针。
- `size` 数组元素个数。

**返回值**：

返回对应的 `ft_value_t`。

### ft_from_double_array

```c
ft_value_t ft_from_double_array(ft_context_ref ft_ctx, double* val, uint32_t size);
```

将 double 数组转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 源数组指针。
- `size` 数组元素个数。

**返回值**：

返回对应的 `ft_value_t`。

### ft_from_string_array

```c
ft_value_t ft_from_string_array(ft_context_ref ft_ctx, const char** val, uint32_t size);
```

将 C 字符串数组转换为 `ft_value_t`。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `val` 字符串指针数组。
- `size` 数组元素个数。

**返回值**：

返回对应的 `ft_value_t`。

## 基本类型转换（ft_value_t → Native）

以下接口将前端传入的 `ft_value_t` 转换为 C 原生类型，便于 Feature 实现使用。

### ft_to_int

```c
bool ft_to_int(ft_context_ref ft_ctx, ft_value_t f_val, int32_t* val);
```

将 `ft_value_t` 转换为 32 位有符号整数。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `f_val` 源 `ft_value_t`，应为数值类型。
- `val` 用于接收结果的 `int32_t*`。

**返回值**：

转换成功时返回 `true`，否则返回 `false`（通常因为 `f_val` 不是数值类型）。

### ft_to_uint

```c
bool ft_to_uint(ft_context_ref ft_ctx, ft_value_t f_val, uint32_t* val);
```

将 `ft_value_t` 转换为 32 位无符号整数。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `f_val` 源 `ft_value_t`。
- `val` 用于接收结果的 `uint32_t*`。

**返回值**：

成功返回 `true`，失败返回 `false`。

### ft_to_int64

```c
bool ft_to_int64(ft_context_ref ft_ctx, ft_value_t f_val, int64_t* val);
```

将 `ft_value_t` 转换为 64 位有符号整数。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `f_val` 源 `ft_value_t`。
- `val` 用于接收结果的 `int64_t*`。

**返回值**：

成功返回 `true`，失败返回 `false`。

### ft_to_uint64

```c
bool ft_to_uint64(ft_context_ref ft_ctx, ft_value_t f_val, uint64_t* val);
```

将 `ft_value_t` 转换为 64 位无符号整数。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `f_val` 源 `ft_value_t`。
- `val` 用于接收结果的 `uint64_t*`。

**返回值**：

成功返回 `true`，失败返回 `false`。

### ft_to_double

```c
bool ft_to_double(ft_context_ref ft_ctx, ft_value_t f_val, double* val);
```

将 `ft_value_t` 转换为双精度浮点数。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `f_val` 源 `ft_value_t`。
- `val` 用于接收结果的 `double*`。

**返回值**：

成功返回 `true`，失败返回 `false`。

### ft_to_bool

```c
bool ft_to_bool(ft_context_ref ft_ctx, ft_value_t ft_val, bool* val);
```

将 `ft_value_t` 转换为布尔值。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `ft_val` 源 `ft_value_t`。
- `val` 用于接收结果的 `bool*`。

**返回值**：

成功返回 `true`，失败返回 `false`。

### ft_to_string

```c
const char* ft_to_string(ft_context_ref ft_ctx, ft_value_t f_val);
```

将 `ft_value_t` 转换为 C 字符串。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `f_val` 源 `ft_value_t`，应为字符串类型。

**返回值**：

成功时返回字符串指针；失败时返回 `NULL`。

**注意**：

- 返回的字符串由框架管理，**必须**通过 `ft_free_string` 释放。
- Feature 框架不保证该字符串长期有效，如需保留应及时拷贝。

### ft_to_buffer

```c
uint8_t* ft_to_buffer(ft_context_ref ft_ctx, size_t* p_size, ft_value_t f_val);
```

将 `ft_value_t` 转换为二进制缓冲区。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `p_size` 输出参数，返回缓冲区字节数。
- `f_val` 源 `ft_value_t`，应为 `FT_TYPE_BUFFER` 或 `FT_TYPE_TYPED_BUFFER`。

**返回值**：

成功时返回缓冲区起始指针；失败时返回 `NULL`。

**注意**：

- 返回的指针由前端管理，不要手动 `free`。

## 数组操作

### ft_array_size

```c
uint32_t ft_array_size(ft_context_ref ft_ctx, const ft_value_t array);
```

获取 `ft_value_t` 数组的元素数量。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `array` 数组类型的 `ft_value_t`。

**返回值**：

返回数组元素个数。若 `array` 不是数组类型，返回 0。

### ft_array_at

```c
ft_value_t ft_array_at(ft_context_ref ft_ctx, const ft_value_t array, uint32_t idx);
```

按索引访问 `ft_value_t` 数组中的元素。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `array` 数组类型的 `ft_value_t`。
- `idx` 元素索引，从 0 开始。

**返回值**：

成功时返回索引位置的元素 `ft_value_t`；越界或 `array` 非数组时返回 undefined。

**注意**：

- 返回的 `ft_value_t` 为引用类型，**必须**通过 `ft_free_value` 释放。

## 对象操作

### ft_new_object

```c
ft_value_t ft_new_object(ft_context_ref ft_ctx);
```

创建一个空的 `ft_value_t` 对象。Feature 可以向该对象挂载自定义属性。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。

**返回值**：

返回新建的对象 `ft_value_t`（类型为 `FT_TYPE_OBJECT`）。

**注意**：

- 返回值为引用类型，必须通过 `ft_free_value` 释放。
- 对象支持挂载子属性，释放根对象时子属性会被自动释放。

### ft_obj_get_property

```c
ft_value_t ft_obj_get_property(ft_context_ref ft_ctx, ft_value_t ft_val, const char* prop);
```

按属性名读取 `ft_value_t` 对象的属性值。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `ft_val` 对象类型的 `ft_value_t`。
- `prop` 属性名。

**返回值**：

成功时返回属性值的 `ft_value_t`；属性不存在时返回 undefined。

**注意**：

- 返回的 `ft_value_t` 为引用类型，必须通过 `ft_free_value` 释放。

### ft_obj_set_property

```c
bool ft_obj_set_property(ft_context_ref ft_ctx, ft_value_t obj,
                         const char* prop, ft_value_t val);
```

为 `ft_value_t` 对象设置属性值。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `obj` 目标对象 `ft_value_t`。
- `prop` 属性名。
- `val` 要设置的属性值。

**返回值**：

设置成功返回 `true`，失败返回 `false`。

## 内存管理

### ft_free_value

```c
void ft_free_value(ft_context_ref ft_ctx, ft_value_t ft_val);
```

释放 `ft_value_t` 引用计数。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `ft_val` 待释放的 `ft_value_t`。

**注意**：

**需要释放**的 `ft_value_t` 来源：

- `ft_from_xxx` 创建的对象
- `ft_new_object` 新建的对象
- `ft_array_at` 取出的元素
- `ft_obj_get_property` 返回的属性
- `ft_parse_json` 解析得到的对象

**不需要释放**的 `ft_value_t`：

- Feature 实现函数收到的入参
- 作为返回值传回前端的 `ft_value_t`

未正确释放引用类型的 `ft_value_t` 会导致内存泄漏。

### ft_free_string

```c
void ft_free_string(ft_context_ref ft_ctx, const char* str);
```

释放由 `ft_to_string` 返回的字符串。

**参数**：

- `ft_ctx` 当前 Feature 上下文引用。
- `str` 待释放的字符串指针。

**注意**：

- Feature 框架不保证 `ft_to_string` 返回的字符串长期有效，使用完毕后必须及时调用本接口释放。
- 不要使用 `free()` 或 `delete` 释放，必须使用本接口。
