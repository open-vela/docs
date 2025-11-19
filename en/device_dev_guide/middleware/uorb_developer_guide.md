# uORB Framework Development Guide

[English | [简体中文](../../../zh-cn/device_dev_guide/middleware/uorb_developer_guide.md)]

## I. Overview

openvela adopts `uORB` (Micro Object Request Broker) as the cornerstone for its sensor framework and communication between core applications. `uORB` is a lightweight, high-performance Inter-Process Communication (IPC) middleware originating from the PX4 open-source flight control project, which builds an efficient message bus within the system.

This document aims to help developers:

- Understand the uORB framework and its features.
- Master the methods for application programming using uORB.

### 1. Core Features

`uORB` is based on the **Publish/Subscribe** design pattern and is primarily responsible for data transmission between multiple modules. Its key features include:

- **High Performance and Low Latency**: Implements efficient inter-task communication via Shared Memory internally. Its Lock-free design achieves low-latency data exchange with a minimal Memory Footprint.
- **POSIX Standard Interfaces**: `uORB` abstracts each message topic as a standard character device node in NuttX. Developers can interact with it using standard file operation APIs such as `open`, `read`, `write`, `ioctl`, and `poll`, resulting in a low learning curve and easy integration.
- **Flexible Decoupling**: Its core implementation does not depend on a specific thread or Work Queue model, effectively decoupling various functional modules in the system and enhancing system modularity and maintainability.

## II. Core Concepts

To master `uORB`, you must first understand the following core concepts.

### 1. Topic, Publisher, and Subscriber

The communication model of `uORB` revolves around three fundamental roles:

- **Topic:** The basic unit of data transmission, representing a specific class of messages. Each topic is uniquely identified by its **Metadata**, which defines the topic's name (`name`) and message body size (`size`). To distinguish similar data from different sources, a topic can have multiple **Instances**.

- **Publisher/Advertiser:** The role that publishes new messages to a specific topic. Its workflow is typically:

    - **Advertise**: Declares a topic to the system, making it available for subscription.
    - **Publish**: Writes new data to an advertised topic.
    - **Unadvertise**: Revokes the topic advertisement when it is no longer needed.

- **Subscriber:** The role that receives messages from a specific topic. Its workflow is typically:

    - **Subscribe**: Registers an interest in a topic with the system.
    - **Copy**: Reads the latest data from the topic.
    - **Unsubscribe**: Cancels the subscription when data is no longer needed.

In terms of data flow control, a publisher can control the data generation frequency using **Sample Rate/Interval** and optimize system performance by bundling multiple data points for a single publication using **Batch Latency**. For example, if an accelerometer has a sample rate of 50Hz and a maximum publishing latency of 100ms, it means the hardware generates an interrupt every 100ms and publishes 5 data points at once (`100ms / (1000ms / 50Hz)`).

### 2. Topic Types

In `openvela`, `uORB` topics are divided into two categories based on their use case and lifecycle:

| **Topic Type**         | **Description**                                                                                                                                      | **Use Case**                                                                                                                                                                                                                             |
| :--------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **General Topic**      | Subscribers only care about new data published after they subscribe and are not concerned with historical state. This is the most common topic type. | For example, with an accelerometer, an application is only interested in the data reported in the next `data ready` interrupt from the sensor, not the data from a past moment.                                                          |
| **Notification Topic** | Subscribers do not care if a publisher exists or if data has been published; they directly fetch the current state.                                  | For example, for battery information, `healthd` on openvela advertises and publishes the battery info, then unadvertises. When an application subscribes, it directly fetches the latest data from the device node as the current state. |

**Implementation Difference**: When publishing a notification-type topic, you must use an `advertise` API with the `_persist` suffix. The API calls on the subscriber side are identical to those for general topics.

### 3. Device Node Abstraction

The core implementation of `uORB` cleverly utilizes the NuttX file system. Every advertised topic instance is mapped to a character device node under the `/dev/uorb/` directory. This design makes interaction with `uORB` POSIX-compliant:

- **Publisher**: Opens the corresponding device node in `O_WRONLY` (write-only) mode and publishes data using the `write()` operation.
- **Subscriber**: Opens the corresponding device node in `O_RDONLY` (read-only) mode and subscribes to data using the `read()` operation.
- **Data Sharing**: Publishers and subscribers efficiently share data through a Ring Buffer maintained within the device node.
- **Event Monitoring and Control**: Both parties can asynchronously listen for data update events (`POLLIN`) or state change events (`POLLPRI`) using the `poll()` mechanism, and control the device node via the `ioctl()` operation.

## III. Core Mechanisms and Usage

### 1. Intelligent Power Management

In openvela, the `uORB` framework is tightly integrated with power management, allowing it to dynamically control sensor hardware based on application demands to achieve intelligent, low-power operation.

- **Physical Sensors**: After system startup, the driver automatically advertises its corresponding topics but does **not** immediately start the sensor hardware. The framework dynamically manages the sensor's power state based on whether there are any subscribers:
    - When the first subscriber subscribes to a sensor topic, the framework automatically **activates** the sensor hardware.
    - When the last subscriber unsubscribes, the framework automatically **disables** the sensor.

- **Virtual Topics**: For virtual topics such as algorithm outputs, system states, and inter-core communication, character device nodes are registered automatically upon the first publication or subscription. Once created, these nodes **persist in the system** and are not deregistered even if there are no active publishers or subscribers.

### 2. State Monitoring and Synchronization

`uORB` provides a powerful state monitoring mechanism that allows publishers and subscribers to be aware of each other's state changes, which is crucial for implementing advanced features like dynamic sample rate adjustment.

- **Subscriber Monitors Data Updates**: A subscriber uses `poll()` to listen for the `POLLIN` event on a file descriptor. When a publisher publishes new data, this event is triggered, and the subscriber can then read the data.
- **Publisher Monitors Subscriber Status**: A publisher uses `poll()` to listen for the `POLLPRI` event on a file descriptor. The `POLLPRI` event is triggered under the following conditions:

    - When a new subscriber or advertiser joins the topic.
    - When a subscriber sets the sample rate (`interval`) or batching parameters.
    - When a subscriber or advertiser leaves the topic.

When a publisher receives a `POLLPRI` event, it should call `orb_get_state()` to get the aggregated state of the topic. This includes the maximum required sample rate among all subscribers (`max_frequency`), the minimum batch interval (`min_batch_interval`), the internal ring queue size (`queue_size`), the total number of subscribers (`nsubscribers`), and the data generation number (`generation`). The publisher should then adjust its data publishing strategy accordingly to achieve optimal performance and power consumption.

The following diagram illustrates the typical event-driven interaction flow between a publisher and a subscriber using `poll`:

![alt text](./figures/001.png)

In summary, developers should choose the appropriate programming model based on the application scenario:

- **Tightly Coupled Scenarios**: When a publisher needs to dynamically adjust its behavior based on subscriber status (e.g., number, sample rate), the **event-driven programming model** using `poll` (or an asynchronous event library like `libuv`) should be adopted.
- **Loosely Coupled or Uncoupled Scenarios**: When the publisher and subscriber do not need to interact, and the subscriber only needs a one-time or the latest state, using a **notification topic** is a more concise and efficient choice.

### 3. Decoupled Algorithm Model

The publish/subscribe pattern of `uORB` is naturally suited for building modular data processing pipelines. Different algorithm modules can run as independent tasks and interact through shared topics, thus achieving a high degree of decoupling.

For example, a typical sensor data processing flow can be designed as follows:

1. **Sensor Driver**: Publishes the **uncalibrated sensor** topic.
2. **Calibration Algorithm Module**: Subscribes to the **uncalibrated sensor** topic, processes the data, and publishes the **calibrated sensor** topic.
3. **Motion Algorithm Module**: Subscribes to the **calibrated sensor** and **uncalibrated sensor** topics, and publishes the **motion state** topic.
4. **Upper-level Application**: Subscribes to the **motion state** topic for its business logic.

This design allows each module to be developed, tested, and upgraded independently without concern for the specific implementation of other modules.

![alt text](./figures/002.png)

## IV. Source Code Directory Structure

The `apps/system/uorb` directory contains the core wrapper for `uORB`, unit tests, physical sensor topic definitions, and the `uorb_listener` tool.

```Bash
├── Kconfig                             
├── listener.c   # uorb_listener tool implementation
├── Make.defs                     
├── Makefile                       
├── sensor       # Physical sensor topic definitions
│   ├── accel.c                   
│   ├── accel.h                 
│   ├── baro.c                    
│   ├── baro.h                  
│   ├── cap.c                   
│   ├── cap.h                     
│   ├── ***.c                    
│   ├── tvoc.c
│   ├── tvoc.h
│   ├── uv.c
│   └── uv.h
├── test
│   ├── unit_test.c   # uORB unit tests
│   ├── utility.c
│   └── utility.h
└── uORB
    ├── uORB.c   # uORB core wrapper implementation
    └── uORB.h
```

## V. Key Data Structures

- **`struct orb_metadata`: Static Metadata**

    Each uORB topic corresponds to a `struct orb_metadata`, which describes the topic's metadata, including its name (`o_name`), message body size (`o_size`), and formatted output string (`o_format`).

    ```C
    struct orb_metadata {
        FAR const char   *o_name;   // Topic name string
        uint16_t          o_size;    // Size of the topic message struct
    #ifdef CONFIG_DEBUG_UORB
        FAR const char   *o_format; // Formatted output string for tools like uorb_listener
    #endif
    };
    
    typedef FAR const struct orb_metadata *orb_id_t; // Define metadata handle type
    ```

- **`struct orb_state`: Runtime State**

    This structure describes the dynamic state of a topic at runtime. After advertising or subscribing to a topic, a caller can get this information by calling `orb_get_state()`. It includes the maximum publishing frequency required by all subscribers (`max_frequency`), the minimum batch interval (`min_batch_interval`), the internal ring queue size (`queue_size`), the total number of subscribers (`nsubscribers`), and the data generation number (`generation`).

    ```C
    struct orb_state {
        uint32_t max_frequency;      // Maximum frequency required by all subscribers (Hz)
        uint32_t min_batch_interval; // Minimum batch interval required by all subscribers (us)
        uint32_t queue_size;         // Size of the internal ring buffer
        uint32_t nsubscribers;       // Current number of subscribers
        uint64_t generation;         // Data version number, increments on each publish
    };
    ```

- **`struct orb_object`: Topic Instance**

    `uORB` supports instantiating a topic into multiple entities, each uniquely identified by an `instance` number that increments from 0. `struct orb_object` represents a specific topic instance, containing a pointer to its metadata (`meta`) and its instance number (`instance`).

    ```C
    struct orb_object {
        orb_id_t meta;      // Pointer to the topic metadata
        int      instance;  // Instance number of the topic, starting from 0
    };
    ```

## VI. Defining a New Topic

PX4 defines a large number of `uORB` [topics](https://docs.px4.io/main/en/middleware/uorb_graph.html). In openvela, new `uORB` topics can be defined in directories such as `frameworks/topics/`, `system/uorb/sensor/`, or `vendor/` based on requirements.

Defining a new topic typically involves three steps:

1. Define the topic's **data structure** in a `.h` header file.
2. Use the `ORB_DEFINE` macro in a `.c` source file to define the topic's **global metadata variable**.
3. (Optional) For debugging purposes, implement a **print function** in the `.c` source file for use with `uorb_listener`.

The following three macros are primarily used in this process:

- `ORB_ID(name)`: Gets the global metadata handle (`&g_orb_name`) for the topic `name`.
- `ORB_DECLARE(name)`: Declares the topic's global metadata in a header file, making it externally accessible.
- `ORB_DEFINE(name, structure, format)`: Defines and initializes the topic's global metadata in a source file.

```C
#define ORB_ID(name)  &g_orb_##name

#define ORB_DECLARE(name) extern const struct orb_metadata g_orb_##name

#define ORB_DEFINE(name, structure, format) \
  const struct orb_metadata g_orb_##name = \
  { \
    #name, \
    sizeof(structure), \
    format, \
  };
#else
#define ORB_DEFINE(name, structure, format) \
  const struct orb_metadata g_orb_##name = \
  { \
    #name, \
    sizeof(structure), \
  };
#endif
```

### Example: Defining the `sensor_compass` Topic

The following example demonstrates the complete process of defining the `sensor_compass` topic.

#### Step 1: Define the Data Structure (`compass.h`)

First, define the message data structure in the header file (`frameworks/topics/include/sensor/compass.h`) and declare its metadata using `ORB_DECLARE`.

```C
// frameworks/topics/include/sensor/compass.h

#ifndef _TOPICS_INCLUDE_SENSOR_COMPASS_H_
#define _TOPICS_INCLUDE_SENSOR_COMPASS_H_
                                                                                   
#include <uORB/uORB.h>

// Define the data structure
struct sensor_compass {     
    uint64_t timestamp; /* Unit: microseconds */ 
    uint8_t state; /* Calibration level, Range: [0, 4]. */
    float direction; /* Compass direction, unit: 1 degree. */
    float gravity_direction; /* Gravity direction, unit: 1 degree. */
    float gravity_magnitude; /* Gravity magnitude, range: 0 to 9.8 m/s². */
};

// Declare the topic metadata to make it externally accessible
ORB_DECLARE(sensor_compass);

#endif
```

#### Step 2: Define Metadata and Print Function (`compass.c`)

Implement two parts in the source file (`frameworks/topics/src/sensor/compass.c`):

- An optional print function for debugging output with the `uorb_listener` tool. This function should be wrapped within the `CONFIG_DEBUG_UORB` macro definition.
- Use the `ORB_DEFINE` macro to define the topic's metadata instance, associating the topic name, data structure, and the optional print function.

```C
// frameworks/topics/src/sensor/compass.c

#include <sensor/compass.h>

#ifdef CONFIG_DEBUG_UORB
static void print_compass_message(const struct orb_metadata* meta, const void* buffer)  
{
    const struct sensor_compass* message = buffer;
    const orb_abstime now = orb_absolute_time();

    uorbinfo_raw("%s:\ttimestamp: %" PRIu64 " (%" PRIu64 " us ago)"                     
                 "state: %d, direction: %.01f, gravity_direction: %.01f,"               
                 "gravity_magnitude: %.1f",                                             
                 meta->o_name, message->timestamp, now - message->timestamp,             
                 message->state, message->direction, message->gravity_direction,         
                 message->gravity_magnitude);                                               
}                                                                                       
#endif                                                                                

// Define the topic metadata
ORB_DEFINE(sensor_compass, struct sensor_compass, print_compass_message);               
```

## VII. API Reference

`uORB` provides a complete set of APIs for topic publishing, subscription, and management. These APIs can be divided into four main categories: Advertiser, Subscriber, Normal (General Control), and Tool.

The core APIs of `uORB` almost all operate on file descriptors (fd). These file descriptors are bound to the task/thread that created them and **cannot be used across tasks**. For example, an `fd` obtained from `orb_subscribe` in one task cannot be passed to another task to be used with `orb_copy`.

### 1. Advertiser APIs

These APIs are used to create topic nodes, advertise, and publish data.

#### Advertising a Topic

Advertising a topic means creating a device node and declaring that you will be a data provider for that topic.

- **Core Function: `orb_advertise_multi_queue`**

    This is the lowest-level advertising function, and all other `orb_advertise*` functions are wrappers around it. `orb_advertise_multi_queue_persist` has the same parameters as `orb_advertise_multi_queue` but a different internal implementation (for notification topics).

    ```C
    int orb_advertise_multi_queue(FAR const struct orb_metadata *meta,
                                  FAR const void *data,
                                  FAR int *instance,
                                  unsigned int queue_size);
    ```

- **Parameters:**
    - `meta`: Pointer to the topic's metadata.
    - `data`: Data for initialization.
    - `instance`: Pointer to the instance number.
        - If `*instance` is a valid value (e.g., 0, 1, ...), it advertises the specified instance.
        - If the `instance` pointer is `NULL`, the instance number is incremented from existing values, and the result is written back to `*instance`.
        - Multiple advertisers for the same topic instance are supported (one device node, multiple publishers).
    - `queue_size`: The depth of the topic's internal ring buffer, i.e., the maximum number of unread messages it can cache.

- **Return Value:** Returns a file descriptor (`fd`) on success, or -1 on failure.

- **Convenience Wrappers**: These functions provide a more concise way to call the core function:

    ```C
    // Advertise instance 0 with a queue depth of 1
    int orb_advertise(FAR const struct orb_metadata *meta, FAR const void *data);   
    
    // Advertise a specific instance with a queue depth of 1
    static inline int orb_advertise_multi(FAR const struct orb_metadata *meta,
                                          FAR const void *data,
                                          FAR int *instance);
    
    // Advertise instance 0 with a specified queue depth
    static inline int orb_advertise_queue(FAR const struct orb_metadata *meta,
                                          FAR const void *data,
                                          unsigned int queue_size); 
                                          
    int orb_advertise_multi_queue_info(FAR const struct orb_metadata *meta,
                                       FAR const void *data,
                                       FAR int *instance,
                                       unsigned int queue_size,
                                       FAR orb_info_t *info);
    ```

#### Publishing Topic Data

Publish new data to the corresponding topic using the `fd` obtained during advertising.

```C
// Publish a single data message
int orb_publish(FAR const struct orb_metadata *meta, int fd, FAR const void *data);

// Publish data in bulk (for batch processing scenarios)
ssize_t orb_publish_multi(int fd, FAR const void *data, size_t len);
```

- **Return Value**:
    - `orb_publish`: Returns 0 on success, -1 on failure.
    - `orb_publish_multi`: Returns the number of bytes published on success, -1 on failure.

#### Unadvertising a Topic

Closes the advertisement handle and releases related resources. If all publishers for a topic instance unadvertise, the node will be destroyed.

```C
int orb_unadvertise(int fd); // Internally calls orb_close(fd)
```

### 2. Subscriber APIs

These APIs are used to subscribe to topics, check for updates, and copy data.

#### Subscribing to a Topic

Subscribe to an advertised topic to receive data. The function `orb_subscribe` is a convenience wrapper for `orb_subscribe_multi` to subscribe to instance 0.

The `orb_subscribe_nonwakeup` series of functions have similar functionality but **will not wake up** a sleeping task waiting via `poll()` when new data is published. This is suitable for scenarios where a task only cares about data when it is running and does not need to be woken up passively.

- **Return Value**: Returns a file descriptor (`fd`) on success, or -1 on failure with `errno` set.

```C
// Subscribe to a specific instance (core function)
int orb_subscribe_multi(FAR const struct orb_metadata *meta, unsigned instance);

// Subscribe to instance 0 (convenience wrapper)
static inline int orb_subscribe(FAR const struct orb_metadata *meta)
{
  return orb_subscribe_multi(meta, 0);
}

// Subscribe to a specific instance without waking up a sleeping task
int orb_subscribe_multi_nonwakeup(FAR const struct orb_metadata *meta, unsigned instance);

// Subscribe to instance 0 without waking up a sleeping task (convenience wrapper)
static inline int orb_subscribe_nonwakeup(FAR const struct orb_metadata *meta)
{
  return orb_subscribe_multi_nonwakeup(meta, 0);
}
```

#### Copying Data

Copy the latest data from the topic's ring buffer to a local buffer using the `fd` obtained during subscription.

- `orb_copy` reads one message at a time and is a wrapper for `orb_copy_multi`.
- `orb_copy_multi` can perform bulk reads.

**Return Value**:

- `orb_copy`: Returns 0 on success, -1 on failure.
- `orb_copy_multi`: Returns the actual number of bytes read on success, -1 on failure.

```C
// Copy data in bulk (core function)
ssize_t orb_copy_multi(int fd, FAR void *buffer, size_t len);

// Copy a single data message (convenience wrapper)
static inline int orb_copy(FAR const struct orb_metadata *meta, int fd, FAR void *buffer)
{
  ssize_t ret = orb_copy_multi(fd, buffer, meta->o_size);
  return ret == meta->o_size ? 0 : -1;
}
```

#### Checking for Updates

Check if new data has been published to a subscribed topic since the last copy, but **without copying the data**. This is typically used with `poll()` or in a loop to determine if `orb_copy` needs to be executed.

```C
int orb_check(int fd, FAR bool *updated);
```

- **Parameter `updated`**: This is an output parameter. If `*updated` is `true` after the function returns, it indicates that new data is available.

#### Unsubscribing from a Topic

Closes the subscription handle and releases related resources. `uORB` automatically decrements the topic's subscriber count.

```C
// Internally calls orb_close(fd)
static inline int orb_unsubscribe(int fd)
{
  return orb_close(fd);
}
```

### 3. General Control APIs (Normal)

These APIs provide lower-level device node operations, state queries, and parameter configuration functions, typically used for fine-grained control of physical sensors.

#### Device Node Management

Directly open or close the corresponding character device node using the topic name string. This is a lower-level access method than `orb_advertise`/`orb_subscribe`.

```C
// Open a device node
int orb_open(FAR const char *name, int instance, int flags);

// Close a file descriptor
int orb_close(int fd);
```

- **Parameters**:

    - `name`: Topic name string, e.g., `"sensor_accel"`.
    - `instance`: Topic instance index.
    - `flags`: Open mode.

        - Subscribers use `O_RDONLY`.
        - Publishers use `O_WRONLY`.
        - Use **0** to open the node in a third-party mode, for getting device node information.

#### Topic State and Information

```C
// Get the runtime state of a topic (subscriber count, queue size, etc.)
int orb_get_state(int fd, FAR struct orb_state *state);

// Get detailed information about a hardware sensor (e.g., vendor, model)
int orb_get_info(int fd, FAR orb_info_t *info);
```

#### Sample Rate and Batching (Physical Sensors)

These APIs are mainly used to configure the data generation rate and reporting strategy of physical sensors.

- **Sample Interval / Frequency**: These are reciprocals of each other and are used to set the sensor's sampling rate.
- **Batch Interval**: This applies only to physical sensors with hardware FIFO support. It defines the maximum delay time (in µs) that data can be buffered in the FIFO. Data will be reported when this time is reached, even if the FIFO is not full.

```C
// Set/Get the sampling interval (unit: µs)
int orb_set_interval(int fd, unsigned interval);
int orb_get_interval(int fd, FAR unsigned *interval);

// Set/Get the sampling frequency (unit: Hz)
static inline int orb_set_frequency(int fd, unsigned frequency);
static inline int orb_get_frequency(int fd, FAR unsigned *frequency);

// Set/Get the maximum report latency for a topic (unit: µs)
int orb_set_batch_interval(int fd, unsigned batch_interval);
int orb_get_batch_interval(int fd, FAR unsigned *batch_interval);
```

#### Generic Topic Control (`orb_ioctl`)

Provides a generic I/O control interface for specific configurations of a topic (especially physical sensors), such as controlling the range and resolution of accelerometers, gyroscopes, magnetometers, and PPG sensors.

```C
int orb_ioctl(int fd, int cmd, unsigned long arg);
```

**Note:** The `arg` parameter must point to a buffer of a specific format, depending on the `cmd` type:

- **For calibration commands** (`SNIOC_SET_CALIBVALUE`, `SNIOC_CALIBRATE`): `arg` must be a pointer to a 256-byte buffer.
- **For driver-private control commands**: `arg` must be a pointer to a `struct sensor_ioctl_s`, which allows passing variable-length data.

    ```C
    struct sensor_ioctl_s {
        size_t len;      /* Actual length of the argument */
        char data[1];    /* Variable-length argument buffer */
    };
    ```

- Setting the sample rate/batch interval should **not** be done with `orb_ioctl`; use the dedicated APIs mentioned in the previous section.

#### Hardware Event Handling (Physical Sensors)

Used for sensors that support a hardware FIFO to manually trigger a data flush and get completion events.

```C
// Trigger a hardware FIFO flush to report buffered data immediately
int orb_flush(int fd);

// Get the event status (currently supports ORB_EVENT_FLUSH_COMPLETE)
int orb_get_events(int fd, FAR unsigned int *events);
```

- **Usage Flow**: After calling `orb_flush()`, the driver will start emptying the FIFO. Once the operation is complete, it will send a `POLLPRI` event to subscribers. At this point, `orb_get_events()` can be called to confirm that the `ORB_EVENT_FLUSH_COMPLETE` event has occurred.

#### Asynchronous Event Loop (`orb_loop`)

The `orb_loop` API is used to build asynchronous, callback-based event handling loops, commonly used for multi-threaded data processing.

The core idea is to create a `loop` engine and then register multiple event sources (`handle`) with it. When the `loop` runs, it listens to all event sources and calls the corresponding callback function when an event occurs.

```C
// Loop engine management
int orb_loop_init(FAR struct orb_loop_s *loop, enum orb_loop_type_e type);
int orb_loop_run(FAR struct orb_loop_s *loop);
int orb_loop_deinit(FAR struct orb_loop_s *loop);

// Event handle management
int orb_handle_init(FAR struct orb_handle_s *handle, int fd, int events,
                    FAR void *arg, orb_datain_cb_t datain_cb,
                    orb_dataout_cb_t dataout_cb, orb_eventpri_cb_t pri_cb,
                    orb_eventerr_cb_t err_cb);
int orb_handle_start(FAR struct orb_loop_s *loop,
                     FAR struct orb_handle_s *handle);
int orb_handle_stop(FAR struct orb_loop_s *loop,
                    FAR struct orb_handle_s *handle);
```

### 4. Tool and Utility APIs

These APIs provide convenient utility functions.

```C
// Check if a publisher exists for a specific topic instance.
// meta is the topic metadata, instance is the topic instance index.
// Returns 0 on success, ERROR on failure.
int orb_exists(FAR const struct orb_metadata *meta, int instance);

// Get the total number of created instances for a topic.
int orb_group_count(FAR const struct orb_metadata *meta);

// Return the current absolute system timestamp.
orb_abstime orb_absolute_time(void);
// Calculate the time elapsed since 'then'.
static inline orb_abstime orb_elapsed_time(FAR const orb_abstime *then);

// Get the metadata pointer for a topic by its name string.
FAR const struct orb_metadata *orb_get_meta(FAR const char *name);
```

- **`orb_get_meta` Usage Limitation:** For non-physical sensor topics, this function can only successfully retrieve the metadata pointer after the topic has already been advertised or subscribed to.

## VIII. Debugging Tool: uorb_listener

`uorb_listener` is a command-line test tool built on top of the uORB layer. It calls uORB's subscription APIs to listen to and print topic data, making it the primary tool for verifying that the system's data flow is functioning correctly.

**Core Features:**

- **On-demand Listening**: Can listen to all advertised topics, or you can specify one or more topics.
- **Real-time Feedback**: Prints topic content, frequency, and instance information in real time.
- **Multiple Modes**: Supports various listening modes, such as by frequency, count, or duration.
- **Usage**: Can be viewed by running `uorb_listener -h`.
- **Interrupt Operation**: All listening processes can be stopped using `Ctrl+C`.

### 1. Usage and Parameters

```Bash
# Basic Syntax
uorb_listener [topic_name,...] [options]

listener <command> [arguments...]
 Commands:
        <topics_name> Topic name. Multi name are separated by ','
        [-h       ]  Listener commands help
        [-s       ]  Record uorb data to file
        [-n <val> ]  Number of messages, default: 0
        [-r <val> ]  Subscription rate (unlimited if 0), default: 0
        [-b <val> ]  Subscription maximum report latency in us(unlimited if 0),
                     default: 0
        [-t <val> ]  Time of listener, in seconds, default: 5
        [-T       ]  Top, continuously print updating objects
        [-l       ]  Top only execute once.
        [-i       ]  Get sensor device information based on topic.
        [-f       ]  Flush sensor drive data.
        [-u       ]  Subscribe in non-wakeup mode to save power.
```

#### Parameter Descriptions

| **Parameter**  | **Required** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| :------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<topic_name>` | No           | The name of the topic(s) to listen to, separated by commas (`,`). If not specified, it listens to all advertised topics.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `-h`           |              | Displays help information.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `-s`           | No           | Records the listened uORB data to a CSV file. The path is typically `/data/uorb/<timestamp>/<topic_name>.csv`.<br> **Note**: Using this feature at high frequencies on low-performance devices may cause I/O bottlenecks.<br>Example: `uorb_listener -s sensor_accel0` continuously saves the topic's data to a file.                                                                                                                                                                                                                                                                                           |
| `-n <val>`     | `val`        | Sets the maximum number of messages to listen to. `0` means no limit.<br>Examples:<br>`uorb_listener n 1`: Prints a **snapshot** of the current data for all topics.<br>`uorb_listener n num`: Prints data for all topics until `num` messages are received.                                                                                                                                                                                                                                                                                                                                                    |
| `-r <val>`     | `val`        | Sets the subscription rate (unit: Hz). `0` means no limit, listening at the topic's natural publication frequency. <br> Examples:<br>`uorb_listener r 1`: Prints data for all topics at a rate of 1Hz.<br>`uorb_listener r x n num`: Prints data for all topics at x Hz until `num` messages are received.<br>`uorb_listener <topic_list> r 1`: Continuously prints data for the specified topics at 1Hz. The topic list is comma-separated. Each item can be a topic name (e.g., `sensor_accel`), which prints all instances, or a topic instance name (e.g., `sensor_mag0`), which prints only that instance. |
| `-T`           |              | Similar to the `top` command, continuously updates and prints topic information.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `-l`           |              | Executes the `top` mode print only once.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `-i`           |              | Gets and prints the associated sensor device information for a specified topic.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `-f`           |              | Triggers a `flush` operation, forcing the sensor to report data from its FIFO.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `-u`           |              | Subscribes in `non-wakeup` mode, for power-saving scenarios.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

### 2. Common Scenarios and Examples

1. **Real-time Monitoring of All Topics:**
    Continuously print all data at each topic's natural publication frequency.

    ```Bash
    uorb_listener
    ```

2. **Getting a Single Snapshot of All Topics:**
    Print the current data for all topics once.

    ```C
    uorb_listener -n 1
    ```

3. **Monitoring Specific Topics at a Fixed Rate:**
    Subscribe to `sensor_accel` and `sensor_gyro` at 50Hz, and exit after receiving a total of 10 messages.

    ```C
    uorb_listener sensor_accel,sensor_gyro -r 50 -n 10
    ```

    ![alt text](./figures/003.png)

4. **Monitoring for a Specific Duration:**
    Monitor the `battery_state` topic for 20 seconds. Any data published during this time will be printed.

    ```Bash
    uorb_listener battery_state -t 20
    ```

5. **Saving Topic Data to a File:**
    Continuously listen to instance 0 of `sensor_accel` and save its data to a CSV file.

    ```Bash
    uorb_listener -s sensor_accel0
    ```

## IX. Debugging Tool: uorb_generator

`uorb_generator` is a powerful data publishing tool that can be used with `uorb_listener` to simulate data input, replay logs, and reproduce issues.

**Note**: Before using this tool, ensure that the system's **`NSH_LINELEN`** configuration parameter is large enough (256 or 512 is recommended); otherwise, long data strings entered from the terminal will be truncated.

### 1. Usage and Parameters

`uorb_generator` supports two main data publishing modes: **file playback** and **fake data**.

```Bash
The tool publishes topic data via uorb.
Notice:NSH_LINELEN must be set to 128 or more.

generator <command> [arguments...]
  Commands:
    <topics_name> The playback topic name.
    [-h       ]  Listener commands help.
    [-f <val> ]  File path to be played back(absolute path).
    [-n <val> ]  Number of playbacks(fake model), default: 1
    [-r <val> ]  The rate for playing fake data is only valid when parameter 's' is used. 
                 default:10hz.
    [-s <val> ]  Playback fake data.
    [-t <val> ]  Playback topic.
```

#### Parameter Descriptions

| **Parameter** | **Required** | **Description**                                                                                                                                                                                                                                                            |
| :------------ | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-t <val>`    | `val`        | Specifies the target topic name and instance to publish to, e.g., `sensor_accel0`.                                                                                                                                                                                         |
| `-f <val>`    | `val`        | **[File Playback Mode]** Specifies the absolute path to a CSV file containing uORB data. This file is typically generated by `uorb_listener -s`.                                                                                                                           |
| `-s`          |              | **[Fake Data Mode]** Enables fake data publishing mode. Data entered from the terminal is used to generate the struct data. The timestamp of the current data is updated to the real-time clock, and the fake data string must be placed at the end of the entire command. |
| `-n <val>`    | `val`        | **[Fake Data Mode Only]** Sets the number of times to publish, default is `1`.                                                                                                                                                                                             |
| `-r <val>`    | `val`        | **[Fake Data Mode Only]** Sets the publishing frequency (unit: Hz), default is `10`Hz.                                                                                                                                                                                     |
| `-h`          |              | Displays help information.                                                                                                                                                                                                                                                 |

### 2. Examples

#### Example 1: Publish a Single Custom Fake Data Message

Publish a custom accelerometer data message to the `sensor_accel0` topic. Note that the data string must be placed at the end of the command.

```Bash
# Format: uorb_generator -s -t <topic_name> <field>:<value>,...
uorb_generator -s -t sensor_accel0 timestamp:23191100,x:0.1,y:9.7,z:0.81,temperature:22.15
```

- This command will immediately publish one message, and its timestamp will be updated to the current system time.
- You can use `uorb_listener sensor_accel0` in another terminal to view the published data.

#### Example 2: Publish Multiple Fake Data Messages at High Frequency

Continuously publish barometric pressure data to the `sensor_baro0` topic 100 times at a frequency of 5Hz.

```Bash
uorb_generator -n 100 -r 5 -s -t sensor_baro0 timestamp:23191100,pressure:999.12,temperature:26.34
```

#### Example 3: Replay Data from a File

Re-publish the data from a previously saved `sensor_accel0.csv` file to the `sensor_accel1` topic. This is very useful for reproducing issues on different devices or instances.

```Bash
uorb_generator -f /data/uorb/20240823061723/sensor_accel0.csv -t sensor_accel1
```
