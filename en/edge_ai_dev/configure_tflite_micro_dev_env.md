# Configure TFLite Micro Development Environment

[ English | [简体中文](../../zh-cn/edge_ai_dev/configure_tflite_micro_dev_env.md) ]

Before developing TensorFlow Lite for Microcontrollers (TFLite Micro) applications on the openvela platform, the compilation environment and dependent libraries must be configured correctly. This section guides developers through source code confirmation, library dependency configuration, and memory strategy formulation.

## I. Prerequisites

Before starting, please ensure that the following preparations have been completed:

- **Basic Environment**: Refer to the [Official Documentation](../quickstart/openvela_ubuntu_quick_start.md) to complete the deployment of the openvela basic development environment.

- **Source Code Confirmation**: The TFLite Micro source code has been integrated into the openvela code repository at the following path:

    - `apps/mlearning/tflite-micro/`

## II. Component and Dependency Library Support

TFLite Micro relies on specific mathematical and utility libraries to implement model parsing and operator acceleration. The openvela repository has pre-configured the following key components:

| **Component Name** | **Functional Description**                                                                                       | **Source Path**            |
| :----------------- | :--------------------------------------------------------------------------------------------------------------- | :------------------------- |
| **FlatBuffers**    | Library supporting the TFLite model serialization format; provides necessary headers.                            | `apps/system/flatbuffers/` |
| **Gemmlowp**       | Google's low-precision general matrix multiplication library, used for quantized operations.                     | `apps/math/gemmlowp/`      |
| **Ruy**            | TensorFlow's high-performance matrix multiplication backend, mainly optimizing fully connected layer operations. | `apps/math/ruy/`           |
| **KissFFT**        | Lightweight Fast Fourier Transform library, supporting fixed-point and floating-point operations.                | `apps/math/kissfft/`       |
| **CMSIS-NN**       | Neural network kernel optimization library dedicated to ARM Cortex-M (optional).                                 | `apps/mlearning/cmsis-nn/` |

## III. Compilation Configuration (Kconfig)

Enable necessary library support through the `menuconfig` graphical interface to ensure successful compilation and optimize code size.

Launch the configuration menu:

```Bash
cmake --build cmake_out/goldfish-arm64-v8a-ap -t menuconfig
```

Please complete the configuration of the following four core modules in order:

### 1. Enable C++ Runtime Support

TFLite Micro is written based on C++11/14 standards; therefore, LLVM libc++ support must be enabled.

- **Configuration Path**: `Library Routines` -> `C++ Library`
- **Action**: Select `LLVM libc++ C++ Standard Library`

```Plain
(Top) → Library Routines → C++ Library

( ) Toolchain C++ support
( ) Basic C++ support
(X) LLVM libc++ C++ Standard Library
```

### 2. Enable Math Acceleration Libraries

Enable matrix operation and signal processing libraries based on model requirements.

- **Configuration Path**: `Application Configuration` -> `Math Library Support`
- **Action**: Select `Gemmlowp`, `kissfft`, and `Ruy`

```Plain
(Top) → Application Configuration → Math Library Support

[*] Gemmlowp
[*] kissfft
[ ] LibTomMath MPI Math Library
[*] Ruy
```

### 3. Enable FlatBuffers Support

Enable the system-level FlatBuffers library to support model parsing.

- **Configuration Path**: `Application Configuration` -> `System Libraries and NSH Add-Ons`
- **Action**: Select `flatbuffers`

```Plain
(Top) → Application Configuration → System Libraries and NSH Add-Ons

[*] flatbuffers
```

### 4. Enable TFLite Micro Core

- **Configuration Path**: `Application Configuration` -> `Machine Learning Support`
- **Action**: Select `TFLiteMicro`. If ARM hardware acceleration is required, it is recommended to also select `CMSIS_NN Library`.

```Plain
(Top) → Application Configuration → Machine Learning Support

[ ] CMSIS_NN Library
[*] TFLiteMicro
[ ] Print tflite-micro's debug message
```

## IV. Memory Allocation Strategy

Embedded systems have limited memory resources. TFLite Micro requires a continuous memory area (Tensor Arena) to store input/output tensors and intermediate calculation results.

### 1. Static Allocation (Recommended)

For production environments, static array allocation is recommended. This method eliminates the risk of memory fragmentation, and memory usage is known at compile time.

**Implementation Example**：

```C++
// Define in the global area of the application code
// Note: Memory must be aligned to 16 bytes to meet SIMD instruction requirements
#define TENSOR_ARENA_SIZE (100 * 1024)
static uint8_t tensor_arena[TENSOR_ARENA_SIZE] __attribute__((aligned(16)));
```

### 2. Determine Arena Size

To precisely set `TENSOR_ARENA_SIZE` and avoid waste or overflow, you can use `RecordingMicroInterpreter` to capture actual memory usage at runtime.

**Debugging Steps**:

1. Include the recorder header file.
2. Use `RecordingMicroInterpreter` to replace the standard `MicroInterpreter`.
3. Run model inference once (Invoke).
4. Read the actual usage and add a safety margin (suggest adding +1KB).

```C++
#include "tensorflow/lite/micro/recording_micro_interpreter.h"

// 1. Create recording allocator
auto* allocator = tflite::RecordingMicroAllocator::Create(tensor_arena, arena_size);

// 2. Instantiate recording interpreter
tflite::RecordingMicroInterpreter interpreter(model, resolver, allocator);

// 3. Allocate tensors and execute inference
interpreter.AllocateTensors();
interpreter.Invoke();

// 4. Get memory statistics
size_t used = interpreter.arena_used_bytes();  // Actual usage
interpreter.GetMicroAllocator().PrintAllocations();  // Itemized details
size_t recommended = used + 1024;  // Reserve at least ~1KB extra space
```
