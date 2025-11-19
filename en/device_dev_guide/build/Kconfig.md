# Kconfig User Guide

\[ English | [简体中文](../../../zh-cn/device_dev_guide/build/Kconfig.md) \]

## I. Overview

`Kconfig` provides a mechanism for project configuration at compile time, supporting various types of configuration options, such as integers, strings, and booleans. Through the `Kconfig` files, developers can define the dependencies between options, configure default values, and define their combination rules.For detailed information about the `Kconfig` language, refer to the [Kconfig documentation](https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt).

Similar to most large operating systems, openvela utilizes Kconfig to manage project configurations. Developers can perform configuration tasks through the visual interface provided by menuconfig, enabling the efficient building and tailoring of the openvela system.

## II. Usage Examples

To modify configuration parameters during project setup, perform the following verification and configuration procedure:

1. Review the configuration item status.

    You can examine the `.config` file to determine whether the configuration has been set and if its value meets the expected criteria. If it does, you may use it as is; otherwise, it is recommended to adjust the setting using the `menuconfig` tool. 

    > **Note:** Using the `menuconfig` tool ensures that all configuration dependencies are complete and correct.

2. Example: Configuring the KVDB storage path.

    Take the database storage path configuration for `KVDB`, `CONFIG_KVDB_PERSIST_PATH`, as an example:

    - By default, configuration options use their default values and will not appear in the `defconfig` file.
    - "In the `.config` file you can observe that its default value is set to `"/data/persist.db"`. If a different value is desired, you may locate and adjust the corresponding configuration option through `menuconfig`."

        ![img](./figures/002.png)

3. Example: Enable the `FTL_WRITEBUFFER` configuration. If you need to enable the `FTL_WRITEBUFFER` configuration, follow these steps:

    1. Verify the configuration's presence in `.config`. If absent, enable via `menuconfig` instead of forcibly adding `CONFIG_FTL_WRITEBUFFER=y` to `defconfig`  

        ![img](./figures/004.png)

    2. `CONFIG_FTL_WRITEBUFFER` depends on `CONFIG_DRVR_WRITEBUFFER`. If `CONFIG_DRVR_WRITEBUFFER` is not enabled simultaneously, manually modifying the `defconfig` file will not take effect.

    3. The `menuconfig` interface automatically resolves dependency chains and persists validated changes to `defconfig`:

        ```Plain
        CONFIG_FTL_WRITEBUFFER=y  
        CONFIG_DRVR_WRITEBUFFER=y  
        ```

## III. Purpose of Each File

During the initial build, openvela locates the corresponding project's defconfig by using the specified `arch` and `board` parameters, which serves as the system's initial configuration. Based on this file, openvela expands and combines configurations to ultimately generate a complete `.config` file. The generated `.config` file is then copied to `config.h` to facilitate conditional compilation in the code and support runtime usage.

### 1. Detailed Description of Each File

1. `defconfig`

    - The minimal set of system configurations defines the default basic configuration options. The system generates the complete `.config` configuration file based on this file and the dependencies among configuration options.
    - All configuration options in the `defconfig` file are arranged in alphabetical order. It is recommended to add or remove configuration options using the `menuconfig` tool. Direct modifications to the `defconfig` file may result in redundant configurations or ordering inconsistencies.
  
2. `.config`

    - The `.config` file is the complete configuration generated from the `defconfig` file, incorporating all extended and combined configuration options.
    - The `menuconfig` interface reads the local `.config` file for user-customized configuration adjustments and automatically propagates validated changes back to the `defconfig` file upon completion.

3. `config.h`

    - The `config.h` file is generated from the `.config` file, containing all configuration information to support conditional compilation and runtime operations in the code.

### 2. Build Process Example

The following diagram illustrates a typical build configuration workflow:

![img](./figures/006.svg)

Execute build commands:

```Bash
./build.sh vendor/sim/boards/vela/config/vela menuconfig
./build.sh vendor/sim/boards/vela/config/vela -j8
```

### 3. File Path Examples

Based on the openvela simulator environment, the typical file paths are as follows:

- `defconfig` file path：`vendor/sim/boards/vela/configs/vela/defconfig`
- `.config` file path：`nuttx/.config`
- `config.h` file path：`nuttx/include/config.h`

## IV. Usage Instructions

The following diagram illustrates a typical build configuration workflow:

1. Disable a feature in Kconfig configuration.

    Before disabling a Kconfig configuration option, make sure it is not selected by any other configuration options via the `select` keyword. If there are dependencies, those dependencies must be resolved first.

2. Open the visual configuration interface.

    Use the `menuconfig` command to open the visual configuration interface, for example:

    ```Bash
    ./build.sh vendor/sim/boards/openvela/configs/openvela menuconfig  
    ```

    ![img](./figures/007.png)

3. Use the `menuconfig` command to open the visual configuration interface, for example:

    In the `menuconfig` interface, you can enter `/` followed by a configuration keyword to search. For example, to search for `EXAMPLES_HELLO`:

    > **Note**: If the search results contain `depends on` dependencies, type `?` to continue searching for dependent configurations and enable them.

    ![img](./figures/008.png)

4. Select and navigate configuration options.

    Use the arrow keys to navigate up and down, and press Enter to select the corresponding option.

    ![img](./figures/009.png)

5. View configuration details.

    After selecting a configuration item, press `Shift` + `?` to display its detailed documentation and file location information.

    ![img](./figures/010.png)

6. Select specific options

    Follow configuration prompts, such as the option number in brackets (e.g., '1'), to navigate to sub-option interfaces.

    ![img](./figures/011.png)

7. Modify configuration values

    Within the selected configuration option, you can input values based on the configuration type.

    - int: A specific integer value must be entered.  
    - bool: Toggle the state by pressing `y` (enable) or the space key.
        ![img](./figures/012.png)

    - String type: Enter the string directly as the configuration value.

8. Save changes or exit

    - Press the `ESC` key to exit the configuration interface and press `y` when prompted to save changes.  
    - To force exit, use `Ctrl` + `C`, but this may result in loss of unsaved changes.

## V. Related Documents

The following links provide additional details about using Kconfig:  

- [Kernel Documentation - Kconfig Language](https://www.kernel.org/doc/html/latest/kbuild/kconfig-language.html)
