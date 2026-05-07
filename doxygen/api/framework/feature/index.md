# Feature 框架 API

Feature 框架是 openvela 快应用（Quick App）的 Native 扩展开发框架，提供 JS 与 C/C++ 之间的互调能力。开发者可以通过 Feature 框架为快应用扩展新的系统能力，框架负责参数转换、生命周期管理、异步编程模型以及接口自动生成（JIDL）等核心功能。

## 框架概览

- **[Feature 框架概述](feature_framework.md)** — 架构、概念模型（Module / Prototype / Instance）、JIDL 接口描述语言

## 核心数据类型

- **[类型定义](feature_framework_types.md)** — 基本类型别名、句柄类型、枚举、结构体

## 运行时接口

- **[上下文与数据转换](feature_framework_context.md)** — `ft_value_t` 创建/销毁、类型转换、数组/对象操作
- **[Feature 导出接口](feature_framework_export.md)** — Feature 开发者使用的全量运行时 API（内存、回调、Promise、事件、Worker、JSON）
- **[框架管理接口](feature_framework_main_export.md)** — 快应用框架实现者用于创建和配置 Feature 管理器

## 前端互操作

- **[QuickJS 互操作](feature_framework_qjs_export.md)** — `ft_value_t` 与 `JSValue` 互转（仅 QuickJS 前端）

## 调试与性能

- **[Trace 打点](feature_framework_trace.md)** — Feature 框架内嵌的 sched_note 性能追踪宏
