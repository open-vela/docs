# FAQ and Best Practices

\[ English | [简体中文](../../../zh-cn/device_dev_guide/driver/driver-troubleshooting-guide.md) \]

This document provides a troubleshooting guide and best practices for `openvela` driver developers. Driver development requires not only hardware expertise but also a deep understanding of the operating system (OS) mechanisms. Many developers encounter issues with initialization timing, API calls, memory management, and concurrency control when adapting new drivers.

This guide systematically explains these typical problems and provides proven solutions to improve development efficiency and code quality.

## I. Driver Initialization: Ensuring Correct Timing and Dependencies

Proper initialization is the cornerstone of stable driver operation. The driver's initialization logic must strictly adhere to the system's boot sequence and resource dependencies; otherwise, it can lead to a series of unpredictable issues.

### 1. Delay Initialization for Operations Dependent on the File System

- **Symptom:** Calling file operation interfaces (e.g., `open()`, `read()`) fails during the driver initialization phase.

- **Cause:** File operations depend on the successful mounting of the file system. In the `openvela` boot process, core drivers and system services have a specific initialization order. If a driver initializes too early, the file system will not be ready, and related calls will fail.

- **Solution:** You should move the driver initialization logic that depends on the file system into the `board_app_finalinitialize()` function, which is executed late in the system startup process. This function is called after all core system services (including the file system) have been initialized, ensuring that all dependencies are available.

- **Related Documentation:** [Boot Process](../kernel/boot_process.md)

### 2. Wait for Communication Readiness for Operations Dependent on Remote Nodes

- **Symptom:** Communication with a remote processing core (e.g., another chip) fails within the driver.

- **Cause:** Cross-chip communication depends on the complete startup of the remote system and the initialization of messaging components (e.g., `rpmsg`). Attempting to communicate prematurely will result in failure.

- **Solution:** You must postpone the initialization or communication logic for such drivers. You can use synchronization mechanisms like semaphores or event flags to wait for a signal indicating that the remote system and the local `rpmsg` device are ready before executing the relevant operations.

### 3. Execute Operations Dependent on the KVDB Service After It Starts

- **Symptom:** Accessing the Key-Value Database (KVDB) within a driver causes the system to hang or the service to be unavailable.

- **Cause:** As a system-level service, KVDB is typically started by a system initialization script (e.g., `rc.sysinit`). Any calls to it before its initialization is complete will fail or block.

- **Solution:** Place driver initialization logic or functional calls that depend on KVDB within the `board_app_finalinitialize()` function, or execute them only after confirming that the `kvdb` service is running.

### 4. Avoid Time-Consuming Operations in Initialization Functions

- **Symptom:** The overall system boot time increases significantly.

- **Cause:** Driver initialization functions are executed synchronously in the system boot path. Any time-consuming operations (e.g., hardware polling waits, long `sleep` delays) will directly block subsequent processes, thereby extending the total boot time.

- **Solution:**

    1. **Remove unnecessary delays:** Review the code and remove all non-essential delay calls.
    2. **Use an asynchronous work queue:** If a time-consuming operation is unavoidable, you should submit it to a Work Queue for asynchronous execution. This allows the initialization function to return quickly without blocking system startup.

- **Related Documentation:** [Work Queue Development Guide](../kernel/IPC/work_queue.md)

### 5. Avoid Using Large Local Variables in Initialization Functions

- **Symptom:** The system experiences a stack overflow during the `APP_bringup` phase, leading to boot failure.

- **Cause:** The stack space for the `APP_bringup` task during system startup is limited. Defining large local variables (e.g., arrays of hundreds or thousands of bytes) in a driver initialization function can quickly exhaust this task's stack space.

- **Solution:** You should use dynamic memory allocation (i.e., heap memory) instead of large local variables by calling `kmm_malloc()` or a related interface.

## II. API Usage: Selecting the Right Functions and Modes

openvela provides a rich set of APIs, but when using them in kernel mode (driver context), it is crucial to select interfaces appropriate for the current context.

### 1. Use the file_* Family of Interfaces for File Operations in Kernel Mode

- **Symptom:** Using a file descriptor (fd) to operate on files within a driver leads to access exceptions or data corruption.

- **Cause:** File descriptors are bound to the context of a specific process (or task). A driver's execution context can change at any time (e.g., in an interrupt or a call from a different task). Using standard I/O interfaces based on `fd` (e.g., `read()`, `write()`) in this situation will cause errors due to context mismatch.

- **Solution:** In kernel code such as drivers, you must use kernel-specific file operation interfaces like `file_open()`, `file_read()`, and `file_write()`. These interfaces do not depend on a process context, ensuring operational correctness.

### 2. Use Non-Interruptible Wait APIs to Avoid Signal Interference

- **Symptom:** Calling `nxsem_wait()` or another interruptible wait function returns prematurely before the timeout is reached, causing subsequent logic to fail.

- **Cause:** APIs like `nxsem_wait()` are **interruptible**. They can be interrupted by system signals and will return early (with a return value of `EINTR`). If your driver logic does not handle this case, it will lead to unexpected behavior.

- **Solution:** If your driver logic must not be interrupted by signals, you should use the corresponding **non-interruptible** version, such as `nxsem_wait_uninterruptible()`. This type of function ignores signals, waiting until the resource is available or a timeout occurs.

### 3. Use up_udelay for Microsecond-Level Busy-Waiting

- **Symptom:** Using `usleep()` in initialization or other timing-critical scenarios causes hardware state anomalies or initialization failure.

- **Cause:** The `usleep()` function triggers the OS scheduler, causing the current task to yield the CPU. This context switch introduces an unpredictable delay, far exceeding microseconds, which disrupts the precise timing relationship between the driver and the hardware.

- **Solution:** For precise, non-schedulable, microsecond-level delays (busy-waiting), you must use `up_udelay()`. This function consumes time via a busy-wait loop without causing a task switch.

## III. Memory Management: Optimizing Allocation and Alignment

In resource-constrained embedded systems, using memory efficiently and prudently is critical.

### 1. Avoid Frequent Memory Allocation and Deallocation in I/O Paths

- **Symptom:** After the system has been running for a long time, it fails to allocate a moderately large contiguous block of memory, and system performance degrades, even though plenty of total memory remains.

- **Cause:** Repeatedly allocating and freeing small chunks of memory in frequently called paths, such as I/O handlers, causes the system heap to be continuously fragmented and coalesced. This eventually leads to a large number of small, non-contiguous memory blocks, known as **external fragmentation**, which reduces effective memory utilization.

- **Solution:** For such scenarios, you should adopt a **persistent** memory strategy. Allocate the required buffer once during driver initialization and reuse it throughout the driver's lifecycle.

### 2. Use memalign to Meet Hardware Alignment Requirements

- **Symptom:** DMA (Direct Memory Access) transfers fail or data is corrupted; performance is poor when accessing certain memory regions.

- **Cause:** Many hardware peripherals (especially DMA controllers) require the memory buffers they operate on to have a specific address alignment (e.g., 32-byte or 64-byte aligned). Memory allocated by standard interfaces like `kmm_malloc()` is not guaranteed to meet such alignment requirements.

- **Solution:** When allocating memory for hardware that requires specific alignment, you must use the `kmm_memalign()` interface. This function allows you to specify the alignment boundary to obtain a memory address that meets the hardware's requirements.

## IV. Concurrency Control: Proper Use of Critical Sections and Interrupts

Concurrency control in multi-tasking and interrupt-driven environments is one of the core challenges of driver development.

### 1. Keep Critical Section Code Short and Efficient

- **Symptom:** The system becomes unresponsive, interrupts are lost, or resources within a critical section are not effectively protected.

- **Cause:** After entering a critical section (via `enter_critical_section()` or by disabling interrupts), the current CPU core will no longer respond to other interrupts. If the code inside the critical section takes too long to execute, it can severely impact the system scheduler and other critical services that rely on interrupts. Furthermore, performing any operation that could cause blocking or scheduling (e.g., `sleep`, acquiring a semaphore) within a critical section will cause the current task to yield the CPU while interrupts remain disabled, potentially leading to a deadlock or breaking the protection logic.

- **Solution:**

    - **Minimize the scope of the critical section:** Only place the absolute minimum, essential code that requires protection inside the critical section.
    - **Never perform any operation that might block or cause a context switch inside a critical section.**

### 2. Register a Valid Interrupt Service Routine (ISR) Before Enabling an Interrupt

- **Symptom:** The system freezes immediately after a hardware interrupt is enabled.

- **Cause:** When an interrupt occurs, the processor jumps to the address specified in the interrupt vector table. If you enable an interrupt via `irq_enable()` but have not registered a valid Interrupt Service Routine (ISR) for that interrupt number using `irq_attach()`, the processor will jump to an uninitialized address or a default infinite-loop handler. If the ISR fails to properly clear the hardware's interrupt flag, the interrupt will trigger repeatedly, creating an **interrupt storm** that completely locks up the system.

- **Solution:** Strictly follow the **"register first, then enable"** principle. Before calling `irq_enable()`, you must ensure that a valid ISR, which correctly clears the interrupt flag, has been successfully registered for that interrupt.

## V. Variable Usage: Ensuring Driver Re-entrancy and Stack Safety

### 1. Prohibit Global Variables to Support Multiple Instances

- **Symptom:** When multiple devices of the same type exist in the system, the driver behaves abnormally, and the devices interfere with each other.

- **Cause:** Using global variables to store device state causes all device instances to share the same data. This breaks the driver's independence and re-entrancy, leading to one device's operations unintentionally modifying another's state.

- **Solution:** You must encapsulate the state data for each device instance in a private structure. Allocate such a structure for each device during its initialization and access it via a context pointer (e.g., the `priv` member) in the driver.

### 2. Use Heap Memory Instead of Large Local Variables

- **Symptom:** The application crashes due to a stack overflow when calling the driver from user space via interfaces like `ioctl`.

- **Cause:** Driver code can be called by threads from different contexts, and these threads may have different stack sizes (e.g., a user-space application's stack may be much smaller than a kernel task's stack). If large local variables are defined in a driver function, it can easily cause a stack overflow when called by a thread with a small stack.

- **Solution:** For large data structures, you should use heap memory (allocated via `kmm_malloc()`). It is best to associate this dynamically allocated memory with the driver's private data structure to manage its lifecycle uniformly and prevent memory leaks.

## VI. Runtime Environment: Efficient Use of System Resources

### 1. Prefer Using work_queue for Deferred or Background Tasks

- **Symptom:** Creating a dedicated kernel thread (`kthread`) for a simple timed or background operation results in unnecessary memory and scheduling overhead.

- **Cause:** Each kernel thread requires its own independent stack (typically several KB) and participates in system scheduling, making it a relatively **heavyweight** resource. For non-urgent, short, and deferrable tasks, creating a dedicated thread is wasteful.

- **Solution:** You should prioritize using the system's `work_queue` mechanism. A `work_queue` uses shared kernel worker threads to execute the tasks (`work`) submitted to it, thereby reusing thread resources and significantly saving memory.

- **Related Documentation:** [Work Queue Development Guide](../kernel/IPC/work_queue.md)

### 2. Avoid Executing Long-Running Tasks in a work_queue

- **Symptom:** Other services in the system that depend on the `work_queue` (e.g., networking, USB) experience delays or become unresponsive.

- **Cause:** The `work_queue`'s worker threads are a shared system resource. All `work` items submitted to the same queue are executed sequentially. If your `work` item performs a long-running blocking operation, it will monopolize the worker thread, preventing other `work` items in the queue from being processed in a timely manner.

- **Solution:**

    - **Split the task:** Break a long task into multiple smaller, non-blocking sub-tasks.
    - **Reschedule the work:** At the end of one sub-task, use `work_queue()` or `work_schedule()` to reschedule the next sub-task, thereby yielding the CPU to other `work` items.

## VII. Coding Style

To ensure code consistency, readability, and maintainability, all kernel and driver code in the `openvela` project (excluding third-party libraries) must adhere to a unified coding style. Developers should perform a self-check against the coding style checklist before submitting code.
