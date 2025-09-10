# 代码风格检查指南

\[ [English](../../en/contribute/code_style_check_guide.md) | 简体中文 \]

## 概述

本文档描述了如何使用 **clang-format** 工具进行代码风格检查，包括默认配置文件存在和不存在的情况下的检查方法。

## 检查流程

根据项目中是否存在 `.clang-format` 配置文件，执行不同的检查命令。

> **说明**：openvela 项目使用 **clang-format 14** 版本进行代码风格检查。

### 场景一：使用默认配置文件检查

当项目中存在默认的代码风格配置文件 `.clang-format` 时：

```bash
clang-format -n <filepath> --Werror
```

### 参数说明

- `-n`：仅检查，不修改文件。
- `--Werror`：将格式警告视为错误。

### 场景二：使用 WebKit 风格检查

当项目中不存在默认的代码风格配置文件时：

```bash
clang-format --style=WebKit -n <filepath> --Werror
```

### 参数说明

- `-n`：仅检查，不修改文件。
- `--Werror`：将格式警告视为错误。
- `--style=WebKit`：使用 WebKit 预定义的代码风格。
