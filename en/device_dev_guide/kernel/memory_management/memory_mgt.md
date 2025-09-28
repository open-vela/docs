# Memory Management  

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/kernel/memory_management/memory_mgt.md) \]

## I. Introduction  

The code for openvela's memory management module is located in the `nuttx/mm` directory, which contains memory management related modules. These modules provide features such as memory allocation, memory mapping, shared memory management, and more to support the memory requirements of systems and applications.

## II. Directory Structure  

The `mm` directory implements the memory management unit logic of openvela, mainly including the following subdirectories:  

```bash
mm/
├── binfmt          
├── kmm            
├── mm_gran         
├── iob            
├── map             
├── pgalloc         
├── pool            
├── shm             
├── tlsf            
└── umm             
```  

## III. Module Introduction  

### 1. binfmt  

The `binfmt` module handles the loading and execution of executable files in different formats, supporting common formats like ELF.  

### 2. kmm  

The `kmm` module provides kernel-space memory management functions, supporting memory allocation and deallocation for kernel components.  

### 3. mm_gran  

The `mm_gran` module implements a granular memory allocator, specialized in managing small memory block allocation and deallocation with high efficiency.  

### 4. iob  

The `iob` module manages input/output buffers, offering an efficient approach to handle buffered data such as network packets and serial port data.  

### 5. map  

The `map` module manages memory mapping, supporting inter-process shared memory and device memory mapping to facilitate memory sharing and device access.  

### 6. pgalloc  

The `pgalloc` module implements a page allocator, responsible for managing large memory block allocation and deallocation, suitable for scenarios requiring bulk memory.  

### 7. pool  

The `pool` module implements a memory pool allocator, which pre-allocates memory blocks to significantly improve the speed of memory allocation and deallocation.  

### 8. shm  

The `shm` module manages shared memory, enabling memory sharing between processes to support inter-process communication and data exchange.  

### 9. tlsf  

The `tlsf` module serves as the default heap manager, providing general memory management capabilities for the system.  

### 10. umm  

The `umm` module provides user-space memory management functions, supporting memory allocation and deallocation for user applications.  
