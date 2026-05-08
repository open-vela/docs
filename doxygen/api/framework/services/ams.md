# AMS API

Activity Manager Service（AMS）是 openvela XMS 系统中的活动管理服务模块，负责管理应用的生命周期，以及任务和活动的调度。

## 功能特性

- **Activity 生命周期管理**：AMS 负责管理应用内 Activity 的生命周期，包括创建、启动、暂停、恢复和销毁。
- **任务管理**：AMS 管理应用任务和任务栈，包括任务切换和调度，确保流畅的用户体验。
- **进程管理**：AMS 负责启动、停止和监控应用进程，确保系统资源的有效利用。
- **Intent 处理**：AMS 处理应用间的 Intent 通信，允许不同应用启动 Activity 和 Service。
- **权限管理**：AMS 参与权限检查，确保应用在启动 Activity 时满足系统安全要求。
- **应用状态跟踪**：AMS 跟踪应用状态（如前台、后台、已停止），并据此分配资源。
- **多窗口支持**：AMS 提供多窗口模式下的 Activity 管理，允许多个应用同时显示。
- **后台任务限制**：AMS 对后台任务和服务施加限制，以优化系统性能和电池使用。
- **Service 和 Broadcast 管理**：AMS 还负责管理 Service 和 BroadcastReceiver 的生命周期，确保系统的响应性和稳定性。

## 示例

以下是使用 openvela AMS 模块的示例代码，通常通过 `ActivityManager` 类来管理 Activity 和控制任务。

**启动新 Activity**

```cpp
Intent intent;
makeIntent(intent);
intent.setFlag(intent.mFlag | Intent::FLAG_ACTIVITY_NEW_TASK);
android::sp<android::IBinder> token = new android::BBinder();
ActivityManager am;
am.startActivity(token, intent, -1);
```

**停止 Activity**

```cpp
Intent intent;
makeIntent(intent);
ActivityManager am;
am.stopActivity(intent, intent.mFlag);
```

## 核心类

### ActivityManager

头文件：`#include <app/ActivityManager.h>`

客户端侧访问 AMS 能力的门面类。提供的主要方法：

- `startActivity()` / `stopActivity()` / `finishActivity()` — Activity 启停
- `startService()` / `stopService()` / `stopServiceByToken()` / `bindService()` / `unbindService()` — Service 操作
- `publishService()` / `getService()` — 服务发布与获取
- `sendBroadcast()` / `registerReceiver()` / `unregisterReceiver()` — 广播与接收器
- `attachApplication()` / `stopApplication()` — Application 绑定与终止
- `moveActivityTaskToBackground()` — Activity 任务切换到后台
- `reportActivityStatus()` / `reportServiceStatus()` — 状态上报（由应用向 AMS 回报生命周期状态）
- `postIntent()` — 向指定组件投递 Intent

### ActivityManagerService

头文件：`#include <am/ActivityManagerService.h>`

AMS 的服务端实现类，注册为系统服务，接收各应用通过 Binder 发来的调用并执行调度。开发者一般不直接使用该类。

### Activity

头文件：`#include <app/Activity.h>`

应用开发的 UI 单元基类。应用通过继承该类并重写 `onCreate` / `onStart` / `onResume` / `onPause` / `onStop` / `onDestroy` / `onRestart` 等生命周期回调来实现一个界面。还提供 `finish` / `setResult` / `getWindow` / `moveToBackground` / `onBackPressed` / `onActivityResult` / `onNewIntent` 等操作与扩展点。

### Application

头文件：`#include <app/Application.h>`

应用进程的全局单例基类。应用通常继承 `Application` 来放置进程级资源。主要方法包括：

- 生命周期：`onCreate` / `onDestroy` / `onForeground` / `onBackground` / `onReceiveIntent`
- 组件管理：`createActivity` / `createService` / `addActivity` / `addService` / `findActivity` / `findService` / `deleteActivity` / `deleteService`
- 元信息：`getPackageName` / `getUid` / `isSystemUI` / `getMainLoop` / `getWindowManager`

### ApplicationThread

头文件：`#include <app/ApplicationThread.h>`

Application 侧的调度线程抽象，承接来自 AMS 的调度请求并在应用进程内派发执行。属于框架内部协作类，应用开发者一般不直接调用。

### AppMain

头文件：`#include <app/AppMain.h>`

应用进程入口辅助类。定义应用进程从启动到接入 AMS 的基础流程，封装主事件循环与初始化步骤。

### Context

头文件：`#include <app/Context.h>`

最核心的上下文基类，提供系统能力访问入口。典型方法包括：

- `getPackageName()` / `getApplication()` / `getComponentName()` — 应用与组件信息
- `startActivity()` / `startActivityForResult()` / `stopActivity()` — Activity 启停
- `startService()` / `stopService()` / `bindService()` / `unbindService()` — Service 操作
- `sendBroadcast()` / `registerReceiver()` / `unregisterReceiver()` — 广播与接收器
- `getActivityManager()` / `getWindowManager()` — 系统服务访问
- `getMainLoop()` / `getCurrentLoop()` — 事件循环获取

### ContextImpl

头文件：`#include <app/ContextImpl.h>`

`Context` 基类的默认实现，由框架在 Application / Activity / Service 创建时装配。应用开发者通常不直接构造 `ContextImpl`，而是通过 `Activity::getContext()` 等方式获取实例。

### Intent

头文件：`#include <app/Intent.h>`

承载组件间通信意图的数据结构。包含 action、data、target、bundle、flag 等字段，以及 `FLAG_ACTIVITY_*` 等启动标志。提供 `setAction` / `setData` / `setTarget` / `setBundle` / `setFlag` / `readFromParcel` / `writeToParcel` 等读写方法。

### Service

头文件：`#include <app/Service.h>`

无界面的长生命周期组件基类。开发者通过继承 `Service` 并重写 `onCreate` / `onStartCommand` / `onBind` / `onUnbind` / `onDestroy` / `onReceiveIntent` 来实现后台服务。

### ServiceConnection

头文件：`#include <app/ServiceConnection.h>`

`bindService` 的连接回调接口。包含 `onServiceConnected` / `onServiceDisconnected` 两个回调方法，用于在绑定成功或断开时通知客户端。

### BroadcastReceiver

头文件：`#include <app/BroadcastReceiver.h>`

广播接收器基类。应用通过继承该类并重写 `onReceive(Intent)` 来处理匹配到的系统或应用广播。

### MessageService

头文件：`#include <app/MessageService.h>`

面向消息通信的服务辅助类，封装基于 Intent 的请求—响应模式，便于应用构建基于消息分发的后台服务。主要方法：`sendMessage` / `receiveMessage` / `receiveMessageAndReply` / `reply` / `onBind` / `onBindExt` / `onReply`。

### Dialog

头文件：`#include <app/Dialog.h>`

对话框组件基类。提供 `show` / `hide` / `setLayout` / `setRect` / `getLayout` / `getRoot` / `createDialog` 等操作，应用可继承实现自定义对话框。

### UvLoop

头文件：`#include <app/UvLoop.h>`

基于 libuv 的事件循环封装，供应用主线程以及其他框架组件复用。提供定时器、IO 事件、工作队列等能力。

### Logger

头文件：`#include <app/Logger.h>`

AMS/应用侧通用日志宏定义，封装分级日志输出（`APP_LOGI` / `APP_LOGW` / `APP_LOGE` 等）。

### ActivityTrace

头文件：`#include <ActivityTrace.h>`

Activity 生命周期的 trace 打点宏集合，配合 openvela trace 分析工具可视化应用启动与切换路径。
