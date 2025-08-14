# 使用 memstress 进行内存压力测试

\[ [English](./../../../en/debugging_tools/stress_testing/memstress.md) | 简体中文 \]

## 一、概述

memstress 是一个专门用于检测系统内存管理器稳定性和正确性的测试工具，特别适合在开发和调试阶段使用。在调试模式下，工具会输出每次内存分配和释放的详细日志，便于追踪内存相关的问题。

## 二、工作原理

`memstress` 工具会随机进行以下三种内存操作的压力测试：

1. 标准 malloc：使用 `malloc()` 分配内存。
2. 对齐分配：使用 `aligned_alloc()` 进行对齐内存分配。
3. 重新分配：使用 `realloc()` 调整内存大小。

工具会在分配的内存中填入随机数据或调试模式下的固定值，后续会验证数据的完整性，检测内存读写错误。 

如果检测到内存错误，工具会输出详细的错误信息并触发断言，帮助定位问题。

## 三、如何使用 `memstress`

### 步骤 1: 在编译时启用工具

```Makefile
# 启用 memstress 工具
CONFIG_TESTING_MEMORY_STRESS=y

# 程序名称
CONFIG_TESTING_MEMORY_STRESS_PROGNAME

# 任务优先级
CONFIG_TESTING_MEMORY_STRESS_PRIORITY

# 栈大小
CONFIG_TESTING_MEMORY_STRESS_STACKSIZE
```

### 步骤 2: 执行测试命令  

通过系统 Shell 执行 `memstress` 命令。

#### 命令格式

```Bash
Usage: memstress -m <max-allocsize> -n <node length> -t <sleep us> -x <nthreads> -d <debug mode>
```

#### 参数说明

| **参数**             | **说明**                                                 |
| :------------------- | :------------------------------------------------------- |
| `-m <max-allocsize>` | 设置单次内存分配的最大大小，默认值为 8192 字节           |
| `-n <node length>`   | 设置分配的内存块数量，默认值为 1024。                    |
| `-t <sleep us>`      | 设置每次测试之间的时间间隔（微秒），默认值为 100 微秒。  |
| `-x <nthreads>`      | 启用多线程压力测试，设置线程数量，默认值为 1。           |
| `-d <debug mode>`    | 启用调试模式，该模式有助于定位问题情况，会输出大量信息。 |

#### 使用示例

```Bash
# 基本使用，使用默认参数  
memstress  
  
# 设置最大分配 4KB，1000个内存块，4个线程  
memstress -m 4096 -n 1000 -x 4  
  
# 启用调试模式进行测试  
memstress -d -m 2048 -n 500
```

## 四、重要提示：内存消耗评估

`memstress` 工具的最大内存消耗计算方式如下：

1. 每个线程的节点数组：每个线程都会创建一个包含 **`node length`** 个节点的数组。
2. 每个节点的最大分配：每个节点最多可以保存一个内存块，大小随机生成但不超过 **`max-allocsize`****。**
3. 多线程并行执行：工具支持 **`nthreads`** 个线程同时运行。

`memstress` 是一个持续运行的测试，只有在检测到错误时才会停止。在运行前，请务必根据以下公式预估其最大潜在内存消耗，确保系统有足够的可用内存。

**最大内存消耗 ≈** **`max-allocsize`** **×** **`node length`** **×** **`nthreads`**

请注意，这是理论上的峰值，实际内存使用会因随机的分配和释放而动态变化。建议从较小的参数开始测试，逐步增加压力。
