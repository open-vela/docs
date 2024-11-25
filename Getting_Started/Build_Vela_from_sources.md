# Build openvela from sources

\[ English | [简体中文](Build_Vela_from_sources_zh-cn.md) \]

## Building openvela with build.sh

After installing the required software packages for openvela and downloading the openvela source code, you can compile the openvela source code into a binary file that can run on the development board.

### Initialize Configuration

The first step is to initialize openvela configuration for a given board, based on a pre-existing configuration. 

To choose a configuration you pass the `vendor/<vendor name>/boards/<board name>/configs/<board configuration>` option to build.sh

For openvela Emulator arm:

```
./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap
```

For openvela Emualtor arm64:

```
./build.sh vendor/openvela/boards/vela/configs/goldfish-arm64-v8a-ap
```

For openvela Emulator x86\_64:

```
./build.sh vendor/openvela/boards/vela/configs/goldfish-x86_64-ap
```

To run openvela on openvela Emulator, continue to [Run openvela on openvela Emulator](./Run_Vela_on_Vela_Emulator.md).
