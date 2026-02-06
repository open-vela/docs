# Sim Environment Audio Development Guide

[ English | [简体中文](./../../../zh-cn/quickstart/emulator/sim_audio_guide.md) ]

## I. Introduction

This document aims to guide developers in developing and testing audio features within the openvela Sim (simulator) environment. Through the Sim environment, developers can utilize the Host machine's audio capabilities to simulate embedded device audio input and output, verifying driver logic and middleware functionality.

The main testing scope includes:

1. Using `nxplayer`, `nxrecorder`, and `nxlooper` to verify the basic functions of the **Audio Driver**.
2. Using `mediatool` to verify the business logic of the **Media Framework**.

## II. Module Architecture

The audio subsystem in the Sim environment consists of the following core modules:

1. **Audio Driver**

    - In the Sim environment, the underlying driver simulates audio hardware input and output by mapping the ALSA interface of the Host machine (Linux).

2. **Command Line Tools (CLI Tools)**

    - **nxplayer**: Audio playback testing tool.
    - **nxrecorder**: Audio recording testing tool.
    - **nxlooper**: Audio loopback testing tool.
    - These tools are all implemented based on the Vela Audio Driver.

3. **Media Framework**

    - Includes components such as the Media Framework, RPC communication, and Audio Policy.
    - Provides standard interfaces for playback, recording, audio path switching, and volume control.

4. **mediatool**

    - A command-line interactive program implemented based on the Media Framework, used for testing framework-level functions.

## III. Compilation Configuration

Please configure the openvela build system (Kconfig) as follows.

### 1. Audio Driver Configuration

Enable basic audio driver support and buffer configuration:

```Makefile
CONFIG_AUDIO=y                          # Enable AUDIO subsystem
CONFIG_AUDIO_NUM_BUFFERS=2              # Number of driver buffers
CONFIG_AUDIO_BUFFER_NUMBYTES=8192       # Size of a single buffer (Bytes)
```

### 2. CLI Tool Configuration

Enable `nxplayer`, `nxrecorder`, and `nxlooper` tools:

```Makefile
CONFIG_SYSTEM_NXPLAYER=y
CONFIG_SYSTEM_NXRECORDER=y
CONFIG_SYSTEM_NXLOOPER=y              

# Keep other related configurations as default
```

### 3. Media Framework Configuration

The Media Framework supports cross-core operations. In the Sim environment, this usually involves the simulation of the AP (Application Processor) and the Audio DSP (Digital Signal Processor).

#### AP Side Configuration

Configuration when compiling the Media Framework main body on the AP core:

```Makefile
 CONFIG_MEDIA=y  
 CONFIG_MEDIA_SERVER=y
 CONFIG_MEDIA_SERVER_CONFIG_PATH="/etc/media/"
 CONFIG_MEDIA_SERVER_PROGNAME="mediad"
 CONFIG_MEDIA_SERVER_STACKSIZE=2097152
 CONFIG_MEDIA_SERVER_PRIORITY=245
 CONFIG_MEDIA_TOOL=y
 CONFIG_MEDIA_TOOL_STACKSIZE=16384    
 CONFIG_MEDIA_TOOL_PRIORITY=100
 CONFIG_MEDIA_CLIENT_LISTEN_STACKSIZE=4096
 
 CONFIG_PFW=y
 CONFIG_LIB_XML2=y
 CONFIG_HAVE_CXX=y
 CONFIG_HAVE_CXXINITIALIZE=y
 CONFIG_LIBCXX=y
 CONFIG_LIBSUPCXX=y
```

#### AUDIO Side Configuration

Configuration when compiling the Media Framework main body on the Audio core (including FFmpeg support):

```Makefile
CONFIG_MEDIA=y
CONFIG_MEDIA_SERVER=y

# CONFIG_MEDIA_FOCUS is not set
CONFIG_MEDIA_SERVER_CONFIG_PATH="/etc/media/"
CONFIG_MEDIA_SERVER_PROGNAME="mediad"
CONFIG_MEDIA_SERVER_STACKSIZE=81920
CONFIG_MEDIA_SERVER_PRIORITY=245
CONFIG_MEDIA_TOOL=y
CONFIG_MEDIA_TOOL_STACKSIZE=16384
CONFIG_MEDIA_TOOL_PRIORITY=100
CONFIG_MEDIA_CLIENT_LISTEN_STACKSIZE=4096

# Audio Policy
CONFIG_PFW=y                       
CONFIG_LIB_XML2=y                 
CONFIG_HAVE_CXX=y
CONFIG_HAVE_CXXINITIALIZE=y
CONFIG_LIBCXX=y
CONFIG_LIBSUPCXX=y
CONFIG_KVDB

# FFmpeg Core Configuration
CONFIG_LIB_FFMPEG=y 
CONFIG_LIB_FFMPEG_CONFIGURATION="--disable-sse --enable-avcodec --enable-avdevice --enable-avfilter --enable-avformat --enable-decoder='aac,aac_latm,flac,mp3,pcm_s16le,libopus,libfluoride_sbc,libfluoride_sbc_packed,silk' --enable-demuxer='aac,mp3,pcm_s16le,flac,mov,ogg,wav,silk' --enable-encoder='aac,pcm_s16le,libopus,libfluoride_sbc,silk' --enable-hardcoded-tables --enable-indev=nuttx --enable-ffmpeg --enable-ffprobe --enable-filter='adevsrc,adevsink,afade,amix,amovie_async,amoviesink_async,astats,astreamselect,aresample,volume' --enable-libopus --enable-muxer='opus,opusraw,pcm_s16le,silk,wav' --enable-outdev=bluelet,nuttx --enable-parser='aac,flac' --enable-protocol='cache,concat,file,http,https,rpmsg,tcp,unix' --enable-swresample --tmpdir='/stream'"
```

## IV. FFmpeg Extension Configuration

The Media Framework is implemented based on FFmpeg. Developers need to configure FFmpeg components (demuxer, muxer, decoder, encoder, filter, etc.) according to project requirements.

### 1. Basic Configuration String

The core configuration string is as follows (needs to be written into `.config` or relevant build files):

```Makefile
CONFIG_LIB_FFMPEG_CONFIGURATION="--disable-sse --enable-avcodec --enable-avdevice --enable-avfilter --enable-avformat --enable-decoder='aac,aac_latm,flac,mp3,pcm_s16le,libopus,libfluoride_sbc,libfluoride_sbc_packed,silk' --enable-demuxer='aac,mp3,pcm_s16le,flac,mov,ogg,wav,silk' --enable-encoder='aac,pcm_s16le,libopus,libfluoride_sbc,silk' --enable-hardcoded-tables --enable-indev=nuttx --enable-ffmpeg --enable-ffprobe --enable-filter='adevsrc,adevsink,afade,amix,amovie_async,amoviesink_async,astats,astreamselect,aresample,volume' --enable-libopus --enable-muxer='opus,opusraw,pcm_s16le,silk,wav' --enable-outdev=bluelet,nuttx --enable-parser='aac,flac' --enable-protocol='cache,concat,file,http,https,rpmsg,tcp,unix' --enable-swresample --tmpdir='/stream'"
```

**Configuration Explanation:**

- `--enable-decoder`: Enables specified decoders.
- `--enable-filter`: Enables specified filters.

**Troubleshooting:**

If you encounter errors like `Failed to avformat_open_input ret -1330794744, Protocol not found.`, it usually means the corresponding protocol or format support is missing. Please check and modify the configuration string above to extend FFmpeg capabilities.

### 2. Dependency Library Configuration

Some FFmpeg decoders depend on third-party decoding libraries and must be explicitly enabled in Kconfig:

```Makefile
# libhelix_aac dependency
CONFIG_LIB_HELIX_AAC=y
CONFIG_LIB_HELIX_AAC_SBR=y

# libfluoride_sbc, libfluoride_sbc_packed dependency
CONFIG_LIB_FLUORIDE_SBC=y
CONFIG_LIB_FLUORIDE_SBC_DECODER=y
CONFIG_LIB_FLUORIDE_SBC_ENCODER=y

# libopus dependency
CONFIG_LIB_OPUS=y

# silk dependency
CONFIG_LIB_SILK=y
```

## V. Debugging Tool Usage Guide

This section introduces how to run and test audio tools in the Sim environment.

### 1. Environment Startup

1. Run Simulator

    Enter the `nuttx` directory and start GDB for debugging:

    ```Bash
    cd nuttx
    sudo gdb --args ./nuttx
    ```

2. Mount Host File System

    In the NuttX Shell (nsh), mount the Host machine's audio stream directory to the `/stream` directory of the Sim environment:

    ```Bash
    # Replace <username> with the actual username
    mount -t hostfs -o fs=/home/<username>/Streams/ /stream
    ```

### 2. nxplayer Usage Instructions

`nxplayer` is used to test audio playback functions.

#### Scenario A: Playback of Raw PCM Data

**Test Case**: Play `/stream/8000.pcm` (Mono, 16-bit, 44100Hz).

```Bash
nxplayer

# Specify playback device
device pcm0p

# Format: playraw <path> <channels> <width> <rate>
playraw /stream/8000.pcm 1 16 44100
```

#### Scenario B: Playback of MP3 Files (Simulated Offload)

**Host Dependency**: Simulating MP3 decoding requires installing the `libmad` library on the Host machine.

```Bash
sudo apt install libmad0-dev:i386
```

**Test Case**:

```Bash
nxplayer 
# Specify Offload playback device
device pcm1p
# Play file
play /stream/1.mp3

# Stop playback
stop 
```

**Functional Limitations**:

- Supports files with ID3V2 headers.
- Supports files without any ID3 headers.
- **Does NOT support** ID3V1 format.

### 3. nxrecorder Usage Instructions

`nxrecorder` is used to test audio recording functions.

#### Scenario A: Recording Raw PCM Data

**Test Case**: Record stereo, 16-bit, 48000Hz audio to `1.pcm`.

```Bash
nxrecorder
# Specify recording device
device pcm0c
# Format: recordraw <path> <channels> <width> <rate>
recordraw /stream/1.pcm 2 16 48000

# Stop recording
stop 
```

**Verification Method**: Check if `1.pcm` is generated in the corresponding directory on the Host machine and verify if it plays back normally.

#### Scenario B: Recording MP3 Files (Simulated Offload)

**Host Dependency**: Simulating MP3 encoding requires installing the `libmp3lame` library on the Host machine:

```Bash
sudo apt-get install libmp3lame-dev:i386
```

**Test Case**:

```Bash
nxrecorder

# Specify Offload recording device
device pcm1c

# Record MP3
record /stream/100.mp3 2 16 44100
```

### 4. nxlooper Usage Instructions

`nxlooper` is used to test audio loopback, where recorded data is sent directly to the playback channel.

#### Scenario A: PCM Data Loopback

```Bash
nxlooper
# Specify playback device
device pcm0p
# Specify recording device
device pcm0c
# Start loopback: 2 channels, 16-bit, 48kHz
loopback 2 16 48000

# Stop loopback
stop
```

#### Scenario B: MP3 Data Loopback

```Bash
nxlooper
device pcm1p
device pcm1c
# The last parameter '8' represents the format code (AUDIO_FMT_MP3)
loopback 2 16 44100 8

# Stop loopback
stop 
```

**Parameter Explanation**: The `loopback` command format is: `loopback <channels> <width> <rate> [format]`

Where the `[format]` parameter corresponds to the definitions in `audio.h` (defaults to PCM):

```C
/* Located at ./nuttx/include/nuttx/audio/audio.h */
#define AUDIO_FMT_UNDEF             0x00
#define AUDIO_FMT_OTHER             0x01
#define AUDIO_FMT_MPEG              0x02
#define AUDIO_FMT_AC3               0x03
#define AUDIO_FMT_WMA               0x04
#define AUDIO_FMT_DTS               0x05
#define AUDIO_FMT_PCM               0x06
#define AUDIO_FMT_WAV               0x07
#define AUDIO_FMT_MP3               0x08
#define AUDIO_FMT_MIDI              0x09
#define AUDIO_FMT_OGG_VORBIS        0x0a
#define AUDIO_FMT_FLAC              0x0b
```

## VI. mediatool Usage Instructions

For detailed commands and usage of `mediatool`, please refer to the [Mediatool Introduction](../../device_dev_guide/media/mediatool.md).
