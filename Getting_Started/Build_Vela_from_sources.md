# Compile the openvela source code

\[ English | [简体中文](Build_Vela_from_sources_zh-cn.md) \]

## Use build.sh to build openvela

After installing the required packages for openvela and downloading the openvela source code, you can compile the openvela source code into a binary file to be run on the development board.

### Initialize configuration

The first step is to initialize the openvela configuration for the target development board based on the existing configuration.

Select the configuration by passing “vendor/<vendor name>/boards/<board name>/configs/<board configuration>” as a parameter to build.sh

```
./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap -j$(nproc)
```

For the next step, if you choose openvela Emulator to run openvela, refer to [Run openvela on openvela Emulator](./Run_Vela_on_Vela_Emulator.md).
