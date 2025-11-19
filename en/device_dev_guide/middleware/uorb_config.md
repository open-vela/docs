# uORB Configuration Options

[English | [简体中文](../../../zh-cn/device_dev_guide/middleware/uorb_config.md)]

This document describes the core Kconfig configuration options for the uORB framework and its related toolchain.

### I. Core Framework

The following are the basic configuration options required to enable the core features of the uORB framework.

- **`CONFIG_UORB`**: Enable uORB message middleware.

    This is the master switch for uORB. It enables the compilation of its publish-subscribe (Publish-Subscribe) messaging kernel, which provides an efficient and asynchronous communication mechanism for the system.

- **`CONFIG_USENSOR`**: Enable NuttX sensor framework.

    This option compiles the upper-half abstraction layer for sensor drivers, providing a standard character device interface (e.g., `/dev/sensor*`) to the system. It serves as the foundation for applying uORB within the sensor subsystem.

### II. Development and Test Tools

These options are used to build the uORB command-line tools and test suites, which facilitate debugging and validation for developers.

- **`CONFIG_UORB_LISTENER`**: Build the `uorb listener` command-line tool.

    Developers can use this command in the shell to monitor the publishing status of topics, subscriber counts, and data updates in real-time.

- **`CONFIG_UORB_TESTS`**: Build the uORB unit test suite.

    Used to compile the uORB framework's self-test programs for verifying the correctness, performance, and stability of the uORB kernel.

### III. Debugging Options

This option enhances debugging capabilities by providing more detailed runtime information.

- **`CONFIG_DEBUG_UORB`**: Enable detailed uORB debug information.

    When enabled, tools like `uorb listener` can print the full data structure of each topic message, not just a summary. This is crucial for in-depth debugging of specific data flows and content.
