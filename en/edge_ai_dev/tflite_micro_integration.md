# TFLite Micro Architecture Analysis and Integration

[ English | [简体中文](../../zh-cn/edge_ai_dev/tflite_micro_integration.md) ]

Integrating TensorFlow Lite for Microcontrollers (TFLite Micro) on the openvela platform requires developers to deeply understand its layered software architecture, component dependencies, and hardware acceleration mechanisms. This document details the complete architectural design of TFLite Micro on the openvela platform to guide developers through efficient integration.

## I. Prerequisite Concepts and Terminology

To better understand how TFLite Micro operates in an embedded environment, developers must first understand the following core concepts. These terms are used throughout the integration process.

| **Term**                   | **Definition**                                                                                                                                                         | **openvela Platform Context**                                                                                      |
| :------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| **TFLite Micro (TFLM)**    | The microcontroller version of TensorFlow, a lightweight inference framework designed for resource-constrained (KB-level memory) devices.                              | The core inference engine running on openvela.                                                                     |
| **Tensor Arena**           | A pre-allocated large contiguous memory region. TFLM avoids `malloc/free`, placing model inputs, outputs, and intermediate calculation data entirely within this area. | Determines the maximum model size the system can run; requires careful configuration based on SRAM size.           |
| **FlatBuffers**            | An efficient serialization format. Model files are stored in this format, allowing data to be read directly from Flash.                                                | Model data is typically compiled directly into firmware or stored in the filesystem.                               |
| **Operator (Op) / Kernel** | Concrete implementation of operators in neural networks (e.g., Conv2D, Softmax). A Kernel is the specific C++ code for an Op.                                          | Standard Kernels can be replaced via **CMSIS-NN** to leverage openvela hardware acceleration features.             |
| **Op Resolver**            | Operator resolver. Used to locate and register required operator implementations at runtime.                                                                           | It is recommended to use `MicroMutableOpResolver` to register on demand, avoiding firmware bloat from unused code. |
| **Quantization**           | Technique converting 32-bit floating-point numbers to 8-bit integers to reduce model size and accelerate computation.                                                  | openvela recommends running `int8` quantized models for optimal performance.                                       |

## II. Software Stack Hierarchy

The TFLite Micro software stack on the openvela platform adopts a modular layered design, achieving decoupling from the underlying hardware abstraction to the upper-level application interface.

### 1. Overall Architecture Overview

```Plain
┌────────────────────────────────────────────────────────────────┐
│                       Application Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Voice Recog. │  │ Image Detect │  │   Sensor Analysis    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────────┐
│                      Inference API Layer                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Model Loading  │  Tensor Management  │  Inference API   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────────┐
│                 TFLite Micro Framework Layer                   │
│  ┌─────────────────┐  ┌─────────────────────────────────────┐  │
│  │ Micro Interpreter│  │ Operator Kernels (incl. CMSIS-NN    │  │
│  ├─────────────────┤  │     / Custom Accel Kernels)         │  │
│  │ Memory Planner  │  ├─────────────────────────────────────┤  │
│  ├─────────────────┤  │ CONV │ FC │ POOL │ RELU │ ...       │  │
│  │ FlatBuffer Parser│  └─────────────────────────────────────┘  │
│  └─────────────────┘                                           │
└────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────────┐
│     RTOS / Platform Service Layer (NuttX Drivers, FS, etc.)    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Task Scheduler  │  Memory Mgmt  │  Drivers  │ File Sys  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────────┐
│                       Hardware Platform                        │
│      ARM Cortex-M  │  RISC-V  │  ESP32  │  Custom SoC          │
└────────────────────────────────────────────────────────────────┘

```

### 2. Application Layer: Inference API

The application layer encapsulates core functions such as model loading, inference execution, and result retrieval via C/C++ APIs. Developers should focus on how to initialize the interpreter and efficiently handle tensor data.

#### Inference Program Implementation Example

The following code demonstrates the standard process for executing a complete inference in the openvela environment:

```C++
static void test_inference(void* file_data, size_t arenaSize) {
  // 1. Load the model
  const tflite::Model* model = tflite::GetModel(file_data); 
  printf("arenaSize: %d\n", (int)arenaSize);

  // 2. Manually register operators
  tflite::MicroMutableOpResolver<1> resolver;
  resolver.AddFullyConnected(tflite::Register_FULLY_CONNECTED());

  // 3. Prepare Tensor Arena (Memory Pool)
  std::unique_ptr<uint8_t[]> pArena(new uint8_t[arenaSize]);
  
  // 4. Create Interpreter Instance
  // The interpreter requires the model, operator resolver, and memory buffer as inputs
  tflite::MicroInterpreter interpreter(model,
    resolver, pArena.get(), arenaSize);

  // 5. Allocate Tensor Memory
  interpreter.AllocateTensors();
  
  // 6. Populate Input Data
  TfLiteTensor* input_tensor = interpreter.input(0);
  float* input_tensor_data = tflite::GetTensorData<float>(input_tensor);
  
   // Example: Test input x = π/2, expect y ≈ 1.0
  float x_value = 1.5708f;
  input_tensor_data[0] = x_value;

  // 7. Execute Inference
  interpreter.Invoke();

  // 8. Retrieve Output Results
  TfLiteTensor* output_tensor = interpreter.output(0);
  float* output_tensor_data = tflite::GetTensorData<float>(output_tensor);
  syslog(LOG_INFO, "Output value after inference: %f\n", output_tensor_data[0]);
}
```

### 3. Framework Layer: TFLite Micro Core Components

The framework layer is the core of TFLite Micro, responsible for critical functions such as model parsing, memory management, and operator scheduling. This layer ensures extremely low system overhead on the openvela platform through static memory allocation and a streamlined runtime environment.

#### Micro Interpreter

The interpreter acts as the hub of the framework, coordinating processes like model loading, memory allocation, and operator execution. It contains three core sub-components:

1. Model Parser

    - Parses model files in FlatBuffers format.
    - Extracts model metadata: operator types, tensor dimensions, quantization parameters.
    - Constructs the computation graph data structure.

2. Subgraph Manager

    - Manages the computation subgraphs of the model (embedded models typically contain only one subgraph).
    - Maintains the topological relationship of nodes (operators) and edges (tensors).

3. Invocation Engine

    - Executes operators in topological order.
    - Manages input/output tensor bindings for operators.
    - Handles operator execution errors and exceptions.

**The interpreter execution flow is as follows:**

```Plain
Initialization Phase (Setup):
1. AllocateTensors() → Plan and allocate memory space for all tensors (Tensor Arena)


Inference Phase (Inference):
1. interpreter.input() → Populate input tensors and fill data
2. Invoke() → Trigger inference loop
   ├─ for each node in execution_plan (Iterate through every Node in the plan):
   │    ├─ Get operator registration info (Registration)
   │    ├─ Bind input/output tensors
   │    └─ Call the operator's Invoke function
   └─ Return execution status
3. interpreter.output() → Read output tensor results
```

#### Operator Kernels Library

Operator Kernels are the concrete implementations that perform mathematical operations (e.g., convolution, fully connected). TFLite Micro uses a registration mechanism to decouple the framework from specific algorithm implementations, making it very easy to replace specific operators on openvela (e.g., using hardware-accelerated convolution).

**Operator Interface Specification**

If developers need to customize operators or encapsulate hardware acceleration drivers, they must adhere to the `TfLiteRegistration` interface definition:

```C++
typedef struct {

    // [Optional] Init: Allocate persistent memory required by the operator (e.g., filter coefficient tables)
    void* (*init)(TfLiteContext* context, const char* buffer, size_t length);
    
    // [Optional] Free: Clean up resources allocated by init
    void (*free)(TfLiteContext* context, void* buffer);
    
    // [Required] Prepare: Validate tensor dimensions/types, calculate temporary buffer (Scratch Buffer) size
    TfLiteStatus (*prepare)(TfLiteContext* context, TfLiteNode* node);
    
    // [Required] Invoke: Core calculation logic, read data from Input Tensor, write to Output Tensor
    TfLiteStatus (*invoke)(TfLiteContext* context, TfLiteNode* node);
} TfLiteRegistration;
```

**Operator Implementation Reference: ReLU**

The following code demonstrates the implementation logic of a standard ReLU activation function, reflecting TFLite Micro's encapsulation of type safety and memory operations:

```C++
// 1. Preparation Phase: Validate data types and dimensions
TfLiteStatus ReluPrepare(TfLiteContext* context, TfLiteNode* node)
{
    // Validation: Number of input/output tensors
    TF_LITE_ENSURE_EQ(context, node->inputs->size, 1);
    TF_LITE_ENSURE_EQ(context, node->outputs->size, 1);

    const TfLiteTensor* input = GetInput(context, node, 0);
    TfLiteTensor* output = GetOutput(context, node, 0);

    // Validation: Tensor type
    TF_LITE_ENSURE_TYPES_EQ(context, input->type, kTfLiteFloat32);

    // Configuration: Resize output tensor shape to match input
    return context->ResizeTensor(context, output, TfLiteIntArrayCopy(input->dims));
}

// 2. Execution Phase: Numerical Calculation
TfLiteStatus ReluInvoke(TfLiteContext* context, TfLiteNode* node)
{
    const TfLiteTensor* input = GetInput(context, node, 0);
    TfLiteTensor* output = GetOutput(context, node, 0);

    const float* input_data = GetTensorData<float>(input);
    float* output_data = GetTensorData<float>(output);

    // Get total data length
    const int flat_size = MatchingFlatSize(input->dims, output->dims);

    // Execute ReLU: output = max(0, input)
    for (int i = 0; i < flat_size; ++i) {
        output_data[i] = (input_data[i] > 0.0f) ? input_data[i] : 0.0f;
    }

    return kTfLiteOk;
}

// 3. Registration Phase: Return function pointer structure
TfLiteRegistration* Register_RELU()
{
    static TfLiteRegistration r = {
        nullptr,      // init
        nullptr,      // free
        ReluPrepare,  // prepare
        ReluInvoke    // invoke
    };
    return &r;
}
```

**Operator Library Source Directory Structure**

In the `tensorflow/lite/micro/kernels/` directory, code is organized by operator function:

```Plain
tensorflow/lite/micro/kernels/
├── conv.cc                    # Convolution operator
├── depthwise_conv.cc          # Depthwise separable convolution
├── fully_connected.cc         # Fully connected layer
├── pooling.cc                 # Pooling operator
├── activations.cc             # Activation functions (ReLU, Sigmoid, etc.)
├── softmax.cc                 # Softmax
├── add.cc, mul.cc, sub.cc     # Element-wise operations
├── reshape.cc, transpose.cc   # Tensor transformation
└── ...
```

#### Memory Planner

The Memory Planner is the key technology for TFLite Micro to achieve low memory footprint. Unlike the dynamic memory allocation in desktop TensorFlow, Micro implements memory reuse by analyzing tensor lifecycles.

## III. Platform Dependencies and Integration

Running TFLite Micro on the openvela platform is not an isolated process; it depends deeply on underlying OS services and hardware libraries. Understanding these dependencies is crucial for performance tuning and troubleshooting.

### 1. NuttX Kernel Services

TFLite Micro interacts with the NuttX RTOS through a platform abstraction layer. Although TFLite Micro is designed to be OS-independent, reasonable OS configuration on openvela can significantly improve system stability.

#### Task Scheduling and Synchronization

NuttX provides complete POSIX standard support. TFLite Micro inference tasks are typically encapsulated in standard `pthread` or NuttX Tasks.

#### Memory Allocator

TFLite Micro recommends using the **Tensor Arena** mechanism for memory management. However, during the initialization phase or when processing non-tensor data, it may still interact with the NuttX memory manager (Mm).

**Tensor Arena Allocation Strategy**

Although `malloc` can be used to dynamically request the Arena, static allocation is strongly recommended.

```C++
// Recommended: Determine size at compile time, place in BSS segment or specific memory segment (e.g., CCM)
// Method to estimate size: Allocate a large space first, run Interpreter::ArenaUsedBytes() to get actual usage, then adjust
#define ARENA_SIZE (100 * 1024)
static uint8_t tensor_arena[ARENA_SIZE] __attribute__((aligned(16)));
```

### 2. Hardware Acceleration: CMSIS-NN Integration

To improve inference performance on ARM Cortex-M cores (the primary computing unit of openvela), the CMSIS-NN library must be integrated. This library utilizes the SIMD (Single Instruction, Multiple Data) instruction set, which can increase the performance of convolution and matrix multiplication by 4-5 times.

#### Build System Configuration (Makefile)

When integrating CMSIS-NN, the core logic is **replacement**: introducing optimized version source files while removing TFLite's built-in general reference implementations (Reference Kernels) from the compilation list to avoid symbol definition conflicts.

The following is a configuration template for the NuttX build system:

```Makefile
# Check if CMSIS-NN option is enabled in Kconfig
ifneq ($(CONFIG_MLEARNING_CMSIS_NN),)

# 1. Define Macro: Inform TFLite Micro to enable CMSIS-NN path
COMMON_FLAGS += -DCMSIS_NN

# Add header file search path
COMMON_FLAGS += ${INCDIR_PREFIX}$(APPDIR)/mlearning/cmsis-nn/cmsis-nn

# 2. Find optimized source files: Get all .cc files in the cmsis_nn directory
CMSIS_NN_SRCS := $(wildcard $(TFLM_DIR)/tensorflow/lite/micro/kernels/cmsis_nn/*.cc)

# 3. Exclude conflicting files:
# Calculate the filenames of generic implementations to exclude (e.g., conv.cc, fully_connected.cc)
# Logic: Take filenames from CMSIS_NN_SRCS and map them to the kernels/ root directory
UNNEEDED_SRCS := $(addprefix $(TFLM_DIR)/tensorflow/lite/micro/kernels/, $(notdir $(CMSIS_NN_SRCS)))

# 4. Filter out these generic implementations from the original compilation list CXXSRCS
CXXSRCS := $(filter-out $(UNNEEDED_SRCS), $(CXXSRCS))

# 5. Add the optimized source files to the compilation list
CXXSRCS += $(CMSIS_NN_SRCS)

endif
```
