# Audio Driver Testing

\[ [English] | [简体中文](../../../../zh-cn/device_dev_guide/media/audio/Audio_Driver_Testing_Guide.md) \]

## I. nxplayer Usage Guide

### 1. Introduction

`nxplayer` is a command-line testing program used to test the playback functionality of the openvela audio driver. It supports playing PCM files and compressed format files, with the code located in the `apps/system/nxplayer` directory.

### 2. nxplayer Command Description

After running `nxplayer`, you can view supported commands by entering `help`. Below are common commands and their functional descriptions:

```C
nxplayer> help
NxPlayer commands
================
  balance d%        : Set balance percentage (< 50% means more left)
  bass d%           : Set bass level percentage
  device devfile    : Specify a preferred audio device
  h                 : Display help for commands
  help              : Display help for commands
  mediadir path     : Change the media directory
  play filename     : Play a media file
  playraw filename  : Play a raw data file
  pause             : Pause playback
  resume            : Resume playback
  stop              : Stop playback
  tone freq secs    : Produce a pure tone
  treble d%         : Set treble level percentage
  q                 : Exit NxPlayer
  quit              : Exit NxPlayer
  volume d%         : Set volume to level specified
```

- `balance`: Set the balance percentage between left and right channels; values below 50% mean more sound on the left.  
- `bass`: Set the bass level percentage.  
- `device`: Specify a preferred audio device.  
- `mediadir`: Change the directory for media files.  
- `play`: Play a specified media file.  
- `playraw`: Play a specified raw data file.  
- `pause`: Pause playback.  
- `resume`: Resume playback.  
- `stop`: Stop playback.  
- `tone`: Generate a pure tone with specified frequency and duration.  
- `treble d%`: Set the treble level percentage.  
- `q`/`quit`: Exit `NxPlayer`.  
- `volume d%`: Set the volume percentage.  

### 3. Playing PCM Files

When playing PCM files, you need to specify the number of channels, sample depth, and sample rate. Here are the specific steps:

```Bash
nxplayer
nxplayer> device pcm0p
nxplayer> playraw /data/audio.pcm 1 16 44100
```

After playback ends, use the following commands to stop playback and close the device:

```Bash
nxplayer> stop
nxplayer> close
```

### 4. Playing Compressed Format Files

Take the `sim` platform as an example to demonstrate how to play MP3 files:

1. Install dependencies.

    Install necessary libraries on the host machine:  

    ```Bash
    sudo apt install libmad0-dev:i386
    ```

2. Run nxplayer.

    Use the following command to play an MP3 file:  

    ```Bash
    nxplayer
    nxplayer> device pcm1p
    nxplayer> play /data/audio.mp3
    ```

3. Stop playback.

    After playback ends, use the following commands to stop and close the device:  

    ```Bash
    nxplayer> stop
    nxplayer> close
    ```

## II. nxrecorder Usage Guide

### 1. Introduction

`nxrecorder` is a command-line testing program used to test the recording functionality of the openvela audio driver. It supports recording PCM files and compressed format files, with the code located in the `apps/system/nxrecorder` directory.

### 2. nxrecorder Command Description

After running `nxrecorder`, you can view supported commands by entering `help`. Below are common commands and their functional descriptions:

```C
nxrecorder> help
NxRecorder commands
================
  device devfile      : Specify a preferred audio device
  h                   : Display help for commands
  help                : Display help for commands
  recordraw filename  : Record a pcm raw file
  record filename     : Record a media file
  pause               : Pause record
  resume              : Resume record
  stop                : Stop record
  q                   : Exit NxRecorder
  quit                : Exit NxRecorder
```

- `device devfile`: Specify a preferred audio device.  
- `recordraw filename`: Record a PCM raw file.  
- `record filename`: Record a media file.  
- `pause`: Pause recording.  
- `resume`: Resume recording.  
- `stop`: Stop recording.  
- `q`/`quit`: Exit `nxrecorder`.  

### 3. Recording PCM Files

When recording PCM files, you need to specify the number of channels, sample depth, and sample rate. Here are the specific steps:

```Bash
nxrecorder
nxrecorder> device pcm0c
nxrecorder> recordraw /data/d_1ch_16bit_44100.pcm 1 16 44100
nxrecorder> recordraw /data/test.pcm 1 16 48000
```

After recording ends, use the following commands to stop recording and close the device:

```Bash
nxrecorder> stop
nxrecorder> close
```

### 4. Recording Compressed Format Files

Take the `sim` platform as an example to demonstrate how to record MP3 files:

1. Install dependencies.

    Install necessary libraries on the host machine.

    ```Bash
    sudo apt-get install libmp3lame-dev:i386
    ```

2. Run nxrecorder.

    Use the following command to record an MP3 file.

    ```Bash
    nxrecorder
    nxrecorder> device pcm1c
    nxrecorder> record /stream/100.mp3 2 16 44100
    ```

3. End recording.

    After recording ends, use the following commands to stop and close the device:  

    ```Bash
    nxrecorder> stop
    nxrecorder> close
    ```

## III. nxlooper Usage Guide

### 1. Introduction

`nxlooper` is a command-line audio loopback testing program used to test the loopback functionality of audio devices. The code is located in the `apps/system/nxlooper` directory.

### 2. nxlooper Command Description

After running `nxlooper`, you can view supported commands by entering `help`. Below are common commands and their functional descriptions:

```C
nxlooper> help
NxLooper commands
================
  device devfile                                  : Specify a preferred play/record device
  h                                               : Display help for commands
  help                                            : Display help for commands
  loopback channels bpsamp samprate format chmap  : Audio loopback test
  pause                                           : Pause loopback
  resume                                          : Resume loopback
  stop                                            : Stop loopback
  q                                               : Exit NxLooper
  quit                                            : Exit NxLooper
  volume d%                                       : Set volume to level specified
```

- `device devfile`: Specify a preferred playback/recording device.  
- `h`/`help`: Display command help.  
- `loopback channels bpsamp samprate format chmap`: Perform an audio loopback test, where `bpsamp` denotes the sample bit width.  
- `pause`: Pause the loopback test.  
- `resume`: Resume the loopback test.  
- `stop`: Stop the loopback test.  
- `q`/`quit`: Exit `NxLooper`.  
- `volume d%`: Set the volume to the specified percentage.  

### 3. PCM Format Loopback Test

Here are the specific steps for a PCM format audio loopback test:

```Bash
nxlooper
nxlooper> device pcm0p
nxlooper> device pcm0c
nxlooper> loopback 2 16 48000
```

- **Parameter description**:  
    - `channels`: Set the number of channels to 2.  
    - `bpsamp`: Set the sample precision to 16 bits.  
    - `samprate`: Set the sample rate to 48000 Hz.  

After the test ends, use the following commands to stop loopback and close the device:

```Bash
nxlooper> stop
nxlooper> close
```

### 4. Compressed Format Loopback Test

Take the `sim` platform as an example to demonstrate an MP3 format audio loopback test:

```Bash
nxlooper
nxlooper> device pcm1p
nxlooper> device pcm1c

nxlooper> loopback 2 16 44100 8
```

Parameter description:

- `channels`: Set the number of channels to 2.  
- `bpsamp`: Set the sample precision to 16 bits.  
- `samprate`: Set the sample rate to 44100 Hz.  
- `format`: Set the format to `8`, indicating MP3 format.  

The values for the `format` parameter are defined in the `nuttx/include/nuttx/audio/audio.h` file. Below are definitions for some formats:

```Bash
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
#define AUDIO_FMT_SBC               0x0c
#define AUDIO_FMT_AAC               0x0d
#define AUDIO_FMT_MSBC              0x0e
#define AUDIO_FMT_CVSD              0x0f
#define AUDIO_FMT_AMR               0x10
#define AUDIO_FMT_OPUS              0x11
```

After the test ends, use the following commands to stop loopback and close the device:

```C
nxlooper> stop 
nxlooper> close
```

**Note**: The `nxlooper` tool is enabled by default. For specific configurations, refer to the `Kconfig` file in each respective directory.

## IV. CMocka Usage Guide

### 1. Introduction

CMocka is a lightweight C unit testing framework that provides a set of APIs and tools for writing and running C unit tests. Its main features include:  

- Simple to use: Intuitive APIs for quickly writing test cases.  
- Lightweight: Small codebase, easy to integrate into projects.  
- Supports multiple testing styles: Including traditional `assert`-style and new `expect`-style tests.  
- Cross-platform support: Runs on Linux, Windows, macOS, and other platforms.  

### 2. Code Location

CMocka test code is located in the following directory:  

```Bash
apps/testing/drivertest
```  

Relevant code configuration is as follows:  

```C
ifneq ($(CONFIG_AUDIO),)
MAINSRC  += drivertest_audio.c
PROGNAME += cmocka_driver_audio
endif
```

### 3. Configuration Instructions

Before using the CMocka testing framework, ensure the following configurations are enabled:  

```Plain
CONFIG_TESTING_CMOCKA=y
CONFIG_AUDIO=y
CONFIG_TESTING_DRIVER_TEST=y
```

### 4. Test Program: cmocka_driver_audio

`cmocka_driver_audio` is a test program for audio driver testing. Below is its usage description:  

```Bash
usage:

1.cmocka_driver_audio need two required parameters:
   -a 2: only playback
   -a 1: only capture
   -a 3: first capture and then playback.
   -p  : filename.  e.g: -p /data/1.pcm


2.default audio device is /dev/audio/pcm0p, /dev/audio/pcm0c.
   use -i change record audio device. e.g. -i /dev/audio/pcm1c.
   use -i change playback audio device. e.g. -i /dev/audio/pcm1p.
3.default format is AUDIO_FMT_PCM
   use -f change format. e.g -f mp3
```
