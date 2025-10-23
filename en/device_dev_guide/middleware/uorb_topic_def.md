# uORB Topic Definition Guide

[English | [简体中文](../../../zh-cn/device_dev_guide/middleware/uorb_topic_def.md)]

## I. Overview

This document guides you on how to define a new uORB topic in the openvela system.

> **Recommendation:** Before creating a new topic, we recommend that you first check the existing topic list in openvela. Reusing existing topics improves system standardization and compatibility. If no existing topic meets your needs, follow this guide to create a new one.

## II. Definition Steps

Defining a uORB topic follows the standard C language practice of separating header and source files. This ensures a clean interface and modular code. The process involves two core steps:

1. **In the header file (.h):** Define the topic's data structure and declare its metadata for external modules to reference.
2. **In the source file (.c):** Define the topic's metadata instance and provide optional support for debug printing.

### Step 1: Define the Data Structure and Declare Metadata in the Header File

You need to perform two tasks in the header file: define the message body's data structure and declare the topic's metadata using the `ORB_DECLARE` macro. This allows other modules to understand the topic's structure and reference it by including this header file.

**Example: `orb_test.h`**

```C
#include <uORB/uORB.h>
#include <inttypes.h> // Include for macros like PRIu64

/* 1. Define the topic's data structure */
struct orb_test_s {
    uint64_t timestamp;  /* Timestamp, in microseconds (us) */
    int32_t val;         /* Example data field */
};

/* 2. Declare the topic metadata to make it externally visible */
ORB_DECLARE(orb_test);
```

### Step 2: Define the Metadata Instance in the Source File

In the corresponding source file, you need to use the `ORB_DEFINE` macro to create and initialize the topic's global metadata instance.

- **The `ORB_DEFINE` Macro**

    This macro is used to associate a topic name, data structure, and an optional debug format string to create a constant instance of type `orb_metadata`.

- `ORB_DEFINE(topic_name, struct_type, format_string);`

    - `topic_name`: The name of the topic, e.g., `orb_test`.
    - `struct_type`: The data structure type of the topic, e.g., `struct orb_test_s`.
    - `format_string`: A format string for the `uorb_listener` tool to print message content. This parameter is optional and only takes effect when `CONFIG_DEBUG_UORB` is enabled.

**Example: `orb_test.c`**

```C
#include "orb_test.h"

/* 1. (Optional) Define a format string for uorb_listener */
#ifdef CONFIG_DEBUG_UORB
static const char orb_test_format[] = "timestamp:%" PRIu64 ",val:%" PRId32 "";
#endif

/* 2. Define the topic metadata instance */
ORB_DEFINE(orb_test, struct orb_test_s, orb_test_format);
```

> **Note**: The `PRIu64` and `PRId32` macros used in the format string are part of the C99 standard. They ensure portability for printing 64-bit or 32-bit integers across different platforms. Make sure to include the `<inttypes.h>` header file.

## III. Getting the Topic Handle

After the definition is complete, you can use the `ORB_ID()` macro in your code to get the topic's handle (`orb_id_t`). This handle is a pointer to the topic's metadata instance and is a required parameter for calling APIs like `orb_subscribe()` and `orb_advertise()`.

```C
#include "orb_test.h"

void my_function(void)
{
    // Get the handle for the orb_test topic
    orb_id_t my_topic_id = ORB_ID(orb_test);

    // This my_topic_id can then be used for subscribe or advertise operations
    // int sub_fd = orb_subscribe(my_topic_id);
    // ...
}
```

## IV. Complete Example: Definition and Usage

The following example shows the complete process, from defining an `orb_test` topic to subscribing to it in an application.

### Explanatory Notes

- **Code Structure**: For demonstration purposes, this example places all definition and usage logic in a single file. In a real project, you should follow best practices by separating them into header and source files.
- **`libuv` Wrapper**: This example uses the `uv_topic_subscribe` function to subscribe to the topic. This is an asynchronous event wrapper provided by openvela, built on top of the `libuv` event loop, for native uORB APIs. It is suitable for event-driven programming scenarios. `test_topic_cb` is the callback function invoked when an event occurs.

### Example Code

```C
#include <stdio.h>
#include <uv.h>
#include <uORB/uORB.h>
#include <inttypes.h>

/*
 * =======================================================
 *   Part 1: Define the uORB Topic (Typically in separate .h and .c files)
 * =======================================================
 */

/* 1. Declare topic metadata (equivalent to .h file content) */
ORB_DECLARE(orb_test);

/* 2. Define the topic's data structure (equivalent to .h file content) */
struct orb_test_s {
  uint64_t timestamp;
  int32_t val;
};

/* 3. Define the debug format string (equivalent to .c file content) */
#ifdef CONFIG_DEBUG_UORB
static const char orb_test_format[] = "timestamp:%" PRIu64 ",val:%" PRId32 "";
#endif

/* 4. Define the topic metadata instance (equivalent to .c file content) */
ORB_DEFINE(orb_test, struct orb_test_s, orb_test_format);


/*
 * =======================================================
 *   Part 2: Use the Topic in an Application (Application Logic)
 * =======================================================
 */

// Declare a callback function to process received topic data.
// (Note: This function is not fully implemented; it only demonstrates API usage).
void test_topic_cb(uv_topic_t *handle, const void *data, int status) {
    if (status == 0) {
        const struct orb_test_s *test_data = data;
        printf("Received orb_test data: timestamp=%" PRIu64 ", val=%" PRId32 "\n",
               test_data->timestamp, test_data->val);
    }
}

/* 5. Subscribe to and listen for the topic */
int main(int argc, char *argv[]) {
    // Get the default libuv event loop
    uv_loop_t* loop = uv_default_loop();

    // Initialize the topic handle
    uv_topic_t topic;

    // Subscribe to the orb_test topic and register the callback function
    // Use the ORB_ID() macro to get the topic handle
    if (uv_topic_subscribe(loop, &topic, ORB_ID(orb_test), test_topic_cb) != 0) {
        fprintf(stderr, "Failed to subscribe to topic\n");
        return 1;
    }

    printf("Successfully subscribed to 'orb_test'. Waiting for data...\n");

    // Run the event loop. The program will block here, waiting for events.
    uv_run(loop, UV_RUN_DEFAULT);

    return 0;
}
```
