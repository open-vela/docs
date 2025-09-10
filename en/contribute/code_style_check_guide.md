# Code Style Checking Guide

\[ English | [简体中文](./../../zh-cn/contribute/code_style_check_guide.md) \]

## Overview

This document describes how to use the **clang-format** tool for code style checking, including checking methods for scenarios with and without a default configuration file.

## Checking Process

Different checking commands are executed depending on whether the `.clang-format` configuration file exists in the project.

> **Note**: The openvela project uses **clang-format 14** version for code style checking.

### Scenario 1: Checking with Default Configuration File

When a default code style configuration file `.clang-format` exists in the project:

```bash
clang-format -n <filepath> --Werror
```

### Parameter Description

- `-n`: Check only, do not modify files.
- `--Werror`: Treat formatting warnings as errors.

### Scenario 2: Checking with WebKit Style

When a default code style configuration file does not exist in the project:

```bash
clang-format --style=WebKit -n <filepath> --Werror
```

### Parameter Description

- `-n`: Check only, do not modify files.
- `--Werror`: Treat formatting warnings as errors.
- `--style=WebKit`: Use WebKit predefined code style.