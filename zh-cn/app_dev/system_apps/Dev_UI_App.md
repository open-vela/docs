# 开发 openvela UI 应用

\[ [English](../../../en/app_dev/system_apps/Dev_UI_App.md)  | 简体中文 \]

## 一、前提条件

1. 下载源码，请参见[快速入门](./../../quickstart/openvela_ubuntu_quick_start.md)。
2. 在开始本教程之前，请从 [music_player](./../../../../../../packages_demos/tree/dev-ai-contest-2026/music_player) 获取示例代码。

## 二、前置概念

在开始教程之前，推荐先了解以下基础知识和工具，以便顺利完成相关开发工作：

1. **Makefile**：熟悉 Makefile 的基础概念与使用方式。Makefile 是构建自动化工具 `make` 使用的配置文件，常用于定义项目的编译规则和依赖管理。
2. **Kconfig**：了解 Kconfig 的基本原理和用法。Kconfig 是 Linux 内核及嵌入式开发中常用的配置系统，帮助开发者灵活地定义和选择软件配置选项。
3. **LVGL**：学习使用 LVGL 嵌入式图形库。LVGL 是一个开源的嵌入式图形库，广泛用于开发高性能的用户界面。相关文档可参考 [LVGL 官方文档](https://docs.lvgl.io/)。

对上述概念的基本理解将帮助您更高效地完成教程中的开发任务。

## 三、简介

本文介绍如何在 openvela 中编写一个简单的音乐播放器。

## 四、项目结构

项目的代码和资源被整齐地组织在各目录和模块中，便于高效管理和开发。以下是 `music_player` 项目的目录结构和文件组成说明。

### 1、目录结构

项目的核心目录和文件结构如下：

```C++
packages/demos/music_player
├── res
│  ├── fonts
│  │  ├── MiSans-Normal.ttf
│  │  └── MiSans-Semibold.ttf
│  ├── icons
│  │  ├── album_picture.png
│  │  ├── audio.png
│  │  ├── music.png
│  │  ├── mute.png
│  │  ├── next.png
│  │  ├── nocover.png
│  │  ├── pause.png
│  │  ├── play.png
│  │  ├── playlist.png
│  │  └── previous.png
│  ├── musics
│  │  ├── manifest.json
│  │  ├── UnamedRhythm.png
│  │  └── UnamedRhythm.wav
│  └── config.json
├── audio_ctl.c
├── audio_ctl.h
├── Kconfig
├── Make.defs
├── Makefile
├── music_player.c
├── music_player.h
├── music_player_main.c
├── wifi.c
└── wifi.h
```

### 2、文件组成

各目录与文件的作用如下：

1. `res`：

    资源目录，包含项目运行所需的静态资源文件：

    - `fonts`：字体文件目录，包含应用使用的字体。
    - `icons`：图标文件目录，包含用于界面显示的各种图标。
    - `musics`：音乐资源目录，包含音频文件和相应的配置信息。
    - `config.json`：全局配置文件，存储项目的配置参数。

2. `audio_ctl.c` / `audio_ctl.h`

    音频控制模块，负责实现音频相关的功能，包括音频输入、输出及音量调节等操作。

3. `wifi.c` / `wifi.h`

    Wi-Fi 控制模块，负责实现 Wi-Fi 的连接管理、初始化等功能。

4. `music_player.c` / `music_player.h`

    音乐播放器的核心逻辑，定义和实现音乐播放的主要功能。

5. `music_player_main.c`

    程序入口文件，负责初始化音乐播放器并启动主要运行逻辑。

6. `Kconfig`、`Make.defs`、`Makefile` 构建系统文件：

    - `Kconfig`：定义项目的配置信息和构建选项。
    - `Make.defs`：编译相关的变量定义和依赖项规则。
    - `Makefile`：定义项目的构建过程和依赖管理。

## 五、UI 应用开发

### 1、UI 结构概览

目标是制作一个这样的音乐播放器界面。

![img](../../demo/images/028.png)

音乐播放器的用户界面 (UI) 采用分组的方式组织为多个模块。以下是完整的 UI 结构层次：

```C++
TIME GROUP:
     TIME: 00:00:00
     DATE: 2024/03/21

PLAYER GROUP:
     ALBUM GROUP:
         ALBUM PICTURE
         ALBUM INFO:
             ALBUM NAME
             ALBUM ARTIST
     PROGRESS GROUP:
         CURRENT TIME: 00:00/00:00
         PLAYBACK PROGRESS BAR
     CONTROL GROUP:
         PLAYLIST
         PREVIOUS
         PLAY/PAUSE
         NEXT
         AUDIO

TOP Layer:
     VOLUME BAR
     PLAYLIST GROUP:
         TITLE
         LIST:
             ICON
             ALBUM NAME
             ALBUM ARTIST
```

- TIME GROUP：时间显示区域。
- PLAYER GROUP：播放器核心区域。
    - ALBUM GROUP：专辑信息区域。
    - PROGRESS GROUP：播放进度区域。
    - CONTROL GROUP：播放控制区域。
- TOP Layer：顶层界面。
    - VOLUME BAR：音量控制条。
    - PLAYLIST GROUP：播放列表区域。

### 2、数据结构设计

#### 应用内配置

应用内配置主要用于初始化所需的环境参数，例如 Wi-Fi 网络配置。需要注意的是，敏感信息如 Wi-Fi 的 `ssid`（服务集标识）和 `psk`（预共享密钥）不要明文保存，建议通过安全方法（例如环境变量或外部配置文件）方式加载。

```C++
struct conf_s {
#if WIFI_ENABLED
    wifi_conf_t wifi;
#endif
};
```

- 如果启用 Wi-Fi 功能（`WIFI_ENABLED` 宏定义），将允许配置 Wi-Fi 的 `ssid` 和 `psk`。
- 避免在代码中硬编码 `ssid` 和 `psk`，确保配置敏感信息时引用外部加密存储或动态加载机制。

#### 运行时状态

运行时状态数据是应用的动态内容，主要记录播放控制与专辑信息。以下是相关数据结构设计：

- 唱片（`album_info_t`）信息。
- 唱片状态切换（`switch_album_mode_t`）。
- 播放状态（`play_status_t`）。

```C
// 唱片信息
typedef struct _album_info_t {   
    const char* name;               // 专辑名称  
    const char* artist;             // 艺术家  
    char path[LV_FS_MAX_PATH_LENGTH];  // 音频文件路径  
    char cover[LV_FS_MAX_PATH_LENGTH]; // 专辑封面路径  
    uint64_t total_time;            // 总时长（单位：毫秒）  
    lv_color_t color;               // 专辑主题颜色  
} album_info_t;  

// 唱片状态切换
typedef enum _switch_album_mode_t {   
    SWITCH_ALBUM_MODE_PREV,  // 切换到上一张  
    SWITCH_ALBUM_MODE_NEXT,  // 切换到下一张  
} switch_album_mode_t;  

// 播放状态
typedef enum _play_status_t {
    PLAY_STATUS_STOP,  // 播放停止  
    PLAY_STATUS_PLAY,  // 正在播放 
    PLAY_STATUS_PAUSE, // 暂停播放  
} play_status_t;

// 播放器运行时的状态信息
struct ctx_s {  
    bool resource_healthy_check;     // 系统资源检查  
    album_info_t* current_album;     // 当前播放的专辑信息  
    lv_obj_t* current_album_related_obj; // 关联到专辑的 UI 对象  

    uint16_t volume;                 // 当前音量  

    play_status_t play_status_prev;  // 上一次播放状态  
    play_status_t play_status;       // 当前播放状态  
    uint64_t current_time;           // 当前播放时长  

    struct {  
        lv_timer_t* volume_bar_countdown;        // 音量条自动隐藏计时器  
        lv_timer_t* playback_progress_update;   // 播放进度更新计时器  
    } timers;  

    audioctl_s* audioctl;            // 音频控制句柄，用于音频操作  
};  
```

#### 组件树结构

根据 UI 结构及其分组设计，`resource_s` 数据结构将包含所有 UI 控件、字体、样式以及图片资源。

```C++
struct resource_s {
    struct {
        lv_obj_t* time;         // 时间显示
        lv_obj_t* date;         // 日期显示
        lv_obj_t* player_group; // 播放器容器  

        lv_obj_t* volume_bar;   // 音量条  
        lv_obj_t* volume_bar_indic; // 音量指示器  
        lv_obj_t* audio;        // 音频对象  
        lv_obj_t* playlist_base; // 播放列表基础区域  

        lv_obj_t* album_cover;  // 专辑封面  
        lv_obj_t* album_name;   // 专辑名称  
        lv_obj_t* album_artist; // 艺术家名称  

        lv_obj_t* play_btn;       // 播放键  
        lv_obj_t* playback_group; // 播放进度容器  
        lv_obj_t* playback_progress; // 播放进度条  
        lv_span_t* playback_current_time; // 当前播放时间  
        lv_span_t* playback_total_time;   // 总时长  

        lv_obj_t* playlist; // 播放列表对象  
    } ui;  

    struct {   
        struct { lv_font_t* normal; } size_16;   
        struct { lv_font_t* bold; } size_22;   
        struct { lv_font_t* normal; } size_24;   
        struct { lv_font_t* normal; } size_28;   
        struct { lv_font_t* bold; } size_60;   
    } fonts;  

    struct {   
        lv_style_t button_default;                // 按钮默认样式  
        lv_style_t button_pressed;                // 按钮按下样式  
        lv_style_transition_dsc_t button_transition_dsc; // 按钮过渡效果  
        lv_style_transition_dsc_t transition_dsc;       // 通用过渡效果  
    } styles;  

    struct {   
        const char* playlist;   // 播放列表图标路径  
        const char* previous;   // 上一首图标路径  
        const char* play;       // 播放图标路径  
        const char* pause;      // 暂停图标路径  
        const char* next;       // 下一首图标路径  
        const char* audio;      // 音频图标路径  
        const char* mute;       // 静音图标路径  
        const char* music;      // 音乐图标路径  
        const char* nocover;    // 无封面占位图标路径  
    } images;  

    album_info_t* albums;     // 所有专辑信息  
    uint8_t album_count;      // 专辑数量  
};
```

组件树结构说明：

- `ui` 模块： 定义了所有界面控件的属性及其层次结构。
- `fonts` 模块： 不同大小和粗细的字体设置。
- `styles` 模块： 封装按钮效果及样式。
- `images` 模块： 图片资源集中管理，便于动态加载.

### 3、业务逻辑设计

#### 主启动流程

![img](../../demo/images/027.png)

函数 `app_create` 是音乐播放器应用的初始化入口，用于完成以下任务：

- 初始化资源和运行上下文结构体。
- 加载配置文件。
- 执行组件初始化（如资源健康检查、Wi-Fi 连接等）。
- 创建主界面并设置默认状态。
- 启动必要的后台任务（如日期和时间更新功能）。

以下是 `app_create` 的完整实现及解析：

```C++
void app_create(void)
 {
     // 初始化资源和上下文结构体
    lv_memzero(&R, sizeof(R));          // 清空资源结构体 Resource
    lv_memzero(&C, sizeof(C));          // 清空运行上下文结构体 Context
    lv_memzero(&CF, sizeof(CF));        // 清空配置结构体 Config
    read_configs();                     // 读取应用所需的配置文件  

    #if WIFI_ENABLED
        CF.wifi.conn_delay = 2000000;       // 设置 Wi-Fi 延迟（单位：微秒，2 秒）
        wifi_connect(&CF.wifi);             // 进行 Wi-Fi 连接
    #endif

    C.resource_healthy_check = init_resource(); // 检查和初始化资源  

    if (!C.resource_healthy_check) {    // 如果资源检查失败  
        app_create_error_page();        // 创建错误页面提醒用户  
        return;  
    }  

    app_create_main_page();             // 创建主页面  
    app_set_play_status(PLAY_STATUS_STOP); // 设置初始播放状态为 “停止”  
    app_switch_to_album(0);             // 切换到第一个专辑  
    app_set_volume(30);                 // 设置默认音量为 30  

    app_refresh_album_info();           // 更新专辑信息显示  
    app_refresh_playlist();             // 更新播放列表显示  
    app_refresh_volume_bar();           // 更新音量条显示  

    app_start_updating_date_time();     // 启动日期和时间的更新任务  
}
```

#### 运行时状态机

![img](../../demo/images/028.jpeg)

`app_refresh_play_status` 是音乐播放器的运行时状态机核心函数。该函数的主要功能是根据播放状态（`PLAY_STATUS_STOP`、`PLAY_STATUS_PLAY` 和 `PLAY_STATUS_PAUSE`）更新 UI 和音频控制器的状态，从而完成播放、暂停和停止等功能的处理。以下是完整函数及其关键逻辑的逐步说明：

```C++
static void app_refresh_play_status(void)
 {
    if (C.timers.playback_progress_update == NULL) {
        C.timers.playback_progress_update = lv_timer_create(app_playback_progress_update_timer_cb, 1000, NULL);
    }
    switch (C.play_status) {  
    case PLAY_STATUS_STOP:  
        // 停止播放状态处理  
        lv_image_set_src(R.ui.play_btn, R.images.play); // 更新播放按钮图标为“播放”  
        lv_timer_pause(C.timers.playback_progress_update); // 暂停计时器  
        if (C.audioctl) {  
            audio_ctl_stop(C.audioctl);         // 停止音频播放  
            audio_ctl_uninit_nxaudio(C.audioctl); // 释放音频控制器资源  
            C.audioctl = NULL;                // 清空音频控制器句柄  
        }  
        break;  
    
    case PLAY_STATUS_PLAY:  
        // 播放状态处理  
        lv_image_set_src(R.ui.play_btn, R.images.pause); // 更新播放按钮图标为“暂停”  
        lv_timer_resume(C.timers.playback_progress_update); // 恢复计时器  
        if (C.play_status_prev == PLAY_STATUS_PAUSE) {  
            audio_ctl_resume(C.audioctl); // 恢复音频播放  
        } else if (C.play_status_prev == PLAY_STATUS_STOP) {  
            C.audioctl = audio_ctl_init_nxaudio(C.current_album->path); // 初始化音频控制器  
            audio_ctl_start(C.audioctl); // 开始播放音频  
        }  
        break;  
    
    case PLAY_STATUS_PAUSE:  
        // 暂停播放状态处理  
        lv_image_set_src(R.ui.play_btn, R.images.play); // 更新播放按钮图标为“播放”  
        lv_timer_pause(C.timers.playback_progress_update); // 暂停计时器  
        audio_ctl_pause(C.audioctl); // 暂停音频播放  
        break;  
    
    default:  
        break;  
    }  
}
```

### 4、接口设计

1. 初始化函数。

    初始化函数负责在应用启动时执行资源配置、界面创建和配置文件加载等任务。以下是主要函数接口：

    ```C++
    /* Init functions */
    static void read_configs(void);
    static bool init_resource(void);
    static void reload_music_config(void);
    static void app_create_error_page(void);
    static void app_create_main_page(void);
    static void app_create_top_layer(void);
    ```

2. 定时器启动函数。

    定时器控制任务用于启动后台进程，支持动态更新界面功能，例如时间显示、播放进度更新。

    ```C++
    /* Timer starting functions */
    static void app_start_updating_date_time(void);
    ```

3. 专辑操作接口。

    专辑操作是音乐播放器的核心功能，支持专辑排序、切换和播放相关处理。

    ```C++
    /* Album operations */
    static int32_t app_get_album_index(album_info_t* album);
    static void app_switch_to_album(int index);
    ```

4. 播放器状态接口。

    播放状态接口用于设置播放器的运行状态，如播放、暂停、改变音量或播放时间等。以下提供的接口实现了这些功能：

    ```C++
    /* Album operations */
    static void app_set_play_status(play_status_t status);
    static void app_set_playback_time(uint32_t current_time);
    static void app_set_volume(uint16_t volume);
    ```

5. UI 刷新功能接口。

    UI 刷新接口负责动态更新界面组件，如专辑信息、播放状态、音量条和播放进度的实时显示。

    ```C++
    /* UI refresh functions */
    static void app_refresh_album_info(void);
    static void app_refresh_date_time(void);
    static void app_refresh_play_status(void);
    static void app_refresh_playback_progress(void);
    static void app_refresh_playlist(void);
    static void app_refresh_volume_bar(void);
    static void app_refresh_volume_countdown_timer(void);
    ```

6. 事件处理接口。

    事件处理是用户交互的重要组成部分，负责对按钮、播放列表、音量条等的事件进行处理：

    ```C++
    /* Event handler functions */
    static void app_audio_event_handler(lv_event_t* e);
    static void app_play_status_event_handler(lv_event_t* e);
    static void app_playlist_btn_event_handler(lv_event_t* e);
    static void app_playlist_event_handler(lv_event_t* e);
    static void app_switch_album_event_handler(lv_event_t* e);
    static void app_volume_bar_event_handler(lv_event_t* e);
    static void app_playback_progress_bar_event_handler(lv_event_t* e);
    ```

7. 定时器回调函数接口。

    定时器相关的回调函数用于在固定时间间隔内触发任务：

    ```C++
    /* Timer callback functions */
    static void app_refresh_date_time_timer_cb(lv_timer_t* timer);
    static void app_playback_progress_update_timer_cb(lv_timer_t* timer);
    static void app_volume_bar_countdown_timer_cb(lv_timer_t* timer);
    ```

### 5、编写项目配置文件

- 配置编译系统配置文件目的是针对目录下的所有源代码，将其编译成可执行产物。
- 增加了新的应用程序，对应的应用程序需要有新的配置项来来决定是否启用应用程序、分配多少栈、进程执行额优先级以及应用的名字等信息。
- 为了新增音乐播放器，需要更新编译系统的配置文件，包括 Kconfig、Makefile 和 Make.defs 文件。

#### Kconfig 文件

以下为新增应用项目的 Kconfig 文件，用于启用功能及定义音乐播放器数据路径：

```CMake
config LVX_USE_DEMO_MUSIC_PLAYER
        bool "Music Player"
        default n
        
if LVX_USE_DEMO_MUSIC_PLAYER
        config LVX_MUSIC_PLAYER_DATA_ROOT
                string "Music Player Data Root"
                default "/sdcard"
endif
```

#### Makefile 文件

`Makefile` 控制应用的编译规则及资源。

```Makefile
include $(APPDIR)/Make.defs

ifeq ($(CONFIG_LVX_USE_DEMO_MUSIC_PLAYER), y)
PROGNAME = music_player
PRIORITY = 100
STACKSIZE = 32768
MODULE = $(CONFIG_LVX_USE_DEMO_MUSIC_PLAYER)

CSRCS = music_player.c audio_ctl.c wifi.c
MAINSRC = music_player_main.c
endif

include $(APPDIR)/Application.mk
```

#### Make.defs 文件

`Make.defs` 文件将新增的音乐播放器模块加入到系统构建。

```Makefile
ifneq ($(CONFIG_LVX_USE_DEMO_MUSIC_PLAYER),)
CONFIGURED_APPS += $(APPDIR)/packages/demos/music_player
endif
```

## 六、编译运行

### 1、配置项目

1. 切换到 openvela 仓库的根目录，执行如下命令来配置音乐播放器。

    模拟器配置文件（defconfig）在 `vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap/` 目录下，使用 `build.sh` 配置和编译开发板的代码。

    ```Bash
    ./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap menuconfig
    ```

    - build.sh：编译脚本，用来配置和编译 openvela 代码
    - vendor/openvela/boards/vela/configs/*：配置路径
    - menuconfig：打开 menuconfig 页面，修改项目代码的配置。

    执行后出现如下界面：

    ![img](../../demo/images/020.png)

2. 按下 `/` 键逐个搜索修改如下配置：

    ```Bash
    LVX_USE_DEMO_MUSIC_PLAYER=y
    LVX_MUSIC_PLAYER_DATA_ROOT="/data"
    ```

    以 `LVX_USE_DEMO_MUSIC_PLAYER` 为例进行操作，其余配置方式相同。

    1. 输入待搜索的配置 `LVX_USE_DEMO_MUSIC_PLAYER`，支持模糊搜索，例如 `music_player`，找到对应的配置，按回车键进入该配置。

        ![img](../../demo/images/021.png)

    2. 按下空格键，`[ ]` 中出现 `*` 表示打开该配置。

        ![img](../../demo/images/022.png)

    3. 将 `LVX_MUSIC_PLAYER_DATA_ROOT` 设置为 `/data`，修改后按下回车键保存当前配置项。

        ![img](../../demo/images/023.png)

    4. 按下 `Q` 键，弹出如下退出保存界面。

        ![img](../../demo/images/024.png)

    5. 按下字母`Y` 键保存配置，退出修改配置页面。

### 2、编译项目

1. 切换到 openvela 仓库的根目录，在终端内依次执行如下命令：

    ```Bash
    # 清理构建产物
    ./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap distclean -j8

    # 开始构建
    ./build.sh vendor/openvela/boards/vela/configs/goldfish-armeabi-v7a-ap -j8
    ```

2. 成功执行后，将得到以下文件：

    ```Bash
    ./nuttx
    ├── vela_ap.elf
    ├── vela_ap.bin
    ```

### 3、启动模拟器并推送资源

音乐播放器运行中会使用到的字体和图片资源位于 `apps/packages/demos/music_player/res` 中。要将这些资源推送到模拟器挂载的相应文件路径，可以按照以下步骤操作。

1. 切换到 openvela 仓库的根目录，启动模拟器：

    ```Bash
    ./emulator.sh vela
    ```

2. 使用模拟器支持的 ADB 将资源推送到设备，在 openvela 仓库的根目录下打开一个新的终端，输入 adb push 后跟文件路径，即可将资源传输到相应位置。

    ```Bash
    # 安装adb
    sudo apt install android-tools-adb

    # 推送资源
    adb push apps/packages/demos/music_player/res /data/
    ```

### 4、启动音乐播放器

在模拟器的终端环境 `openvela-ap>` 中输入如下命令：

```Bash
music_player &
```

### 5、退出 Demo

关闭模拟器退出 Demo，如下图所示：

![img](../../demo/images/026.png)

## 七、常见问题

### 1、如何自定义音乐播放器

1. 修改 `apps/packages/demos/music_player/res` 下面的相关配置，在 `res/musics` 目录下增加新的音乐媒体文件，格式目前只支持 `*.wav`，可以自行将 `*.mp3/aac/m4a` 等格式的媒体文件转换为 `*.wav` 格式。然后修改该目录下的 `res/musics/manifest.json` 文件：

    ```JSON
    {
      "musics": [
        {
          "path": "UnamedRhythm.wav",
          "name": "UnamedRhythm",
          "artist": "Benign X",
          "cover": "UnamedRhythm.png",
          "total_time": 12000,
          "color": "#114514"
        }
      ]
    }
    ```

2. 将想要播放的媒体添加到该配置文件中，参考该格式：

    | 参数       | 参数说明                                 |
    | :--------- | :--------------------------------------- |
    | path       | 待播放媒体的文件路径                     |
    | name       | 媒体名                                   |
    | artist     | 艺术家名                                 |
    | cover      | 封面路径，如果没有提供封面，会展示封面。 |
    | total_time | 该媒体的总播放时长，单位为 `毫秒`。      |
    | color      | 主题色，目前还没有使用。                 |

    例如：添加一个，`Happiness.wav` 播放时长为 `186,507 ms` 的音乐，可以按如下方式修改。

    ```JSON
    {
      "musics": [
        {
          "path": "UnamedRhythm.wav",
          "name": "UnamedRhythm",
          "artist": "Benign X",
          "cover": "UnamedRhythm.png",
          "total_time": 12000,
          "color": "#114514"
        },
        {
          "path": "Happiness.wav",
          "name": "Xin",
          "artist": "Tang",
          "cover": "Good.png",
          "total_time": 186507,
          "color": "#252525"
        },
      ]
    }
    ```

3. 修改完配置后，需要重新推送资源，执行如下命令：

    ```Bash
    # 推送资源
    adb push apps/packages/demos/music_player/res /data/
    ```

4. 退出模拟器。

5. 重新执行[启动模拟器并推送资源](#3启动模拟器并推送资源)和[启动音乐播放器](#4启动音乐播放器)。
