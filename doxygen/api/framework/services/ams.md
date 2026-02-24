# AMS API

Activity Manager Service (AMS) module in Vela's XMS system. This module is responsible for managing the lifecycle of applications, as well as scheduling tasks and activities.

## Table of Contents

- [Features](#features)
- [Examples](#examples)

## Features

- **Activity Lifecycle Management**: AMS is responsible for managing the lifecycle of activities within applications, including creating, starting, pausing, resuming, and destroying activities.

- **Task Management**: AMS manages application tasks and stacks, including task switching and scheduling, ensuring a smooth user experience.

- **Process Management**: AMS is responsible for starting, stopping, and monitoring application processes, ensuring effective utilization of system resources.

- **Intent Handling**: AMS handles Intent communication between applications, allowing different applications to launch activities and services.

- **Permission Management**: AMS participates in permission checks to ensure that applications meet system security requirements when launching activities.

- **Application State Tracking**: AMS tracks the state of applications, such as foreground, background, and stopped, and allocates resources accordingly.

- **Multi-Window Support**: AMS provides activity management in multi-window mode, allowing multiple applications to be displayed simultaneously.

- **Background Task Restrictions**: AMS enforces restrictions on background tasks and services to optimize system performance and battery usage.

- **Service and Broadcast Management**: AMS is also responsible for managing the lifecycle of services and broadcast receivers, ensuring system responsiveness and stability.


## Examples

Example code using the Vela Activity Manager Service (AMS) module typically involves managing activities and controlling tasks through the ActivityManager class. Here are some common examples:

- **Starting a New Activity**

```c++
    Intent intent;
    makeIntent(intent);
    intent.setFlag(intent.mFlag | Intent::FLAG_ACTIVITY_NEW_TASK);
    android::sp<android::IBinder> token = new android::BBinder();
    ActivityManager am;
    am.startActivity(token, intent, -1);
```

- **Stopping an Activity**

```c++
    Intent intent;
    makeIntent(intent);
    ActivityManager am;
    am.stopActivity(intent, intent.mFlag);
```

# ActivityManagerService.h
```c++
.. doxygenfile:: ActivityManagerService.h
  :project: doxygen
```

# Activity.h
```c++
.. doxygenfile:: Activity.h
  :project: doxygen
```

# ActivityManager.h
```c++
.. doxygenfile:: ActivityManager.h
  :project: doxygen
```

# Application.h
```c++
.. doxygenfile:: Application.h
  :project: doxygen
```

# ApplicationThread.h
```c++
.. doxygenfile:: ApplicationThread.h
  :project: doxygen
```

# AppMain.h
```c++
.. doxygenfile:: AppMain.h
  :project: doxygen
```

# BroadcastReceiver.h
```c++
.. doxygenfile:: BroadcastReceiver.h
  :project: doxygen
```

# Context.h
```c++
.. doxygenfile:: Context.h
  :project: doxygen
```

# ContextImpl.h
```c++
.. doxygenfile:: ContextImpl.h
  :project: doxygen
```

# Dialog.h
```c++
.. doxygenfile:: Dialog.h
  :project: doxygen
```

# Intent.h
```c++
.. doxygenfile:: Intent.h
  :project: doxygen
```

# Logger.h
```c++
.. doxygenfile:: Logger.h
  :project: doxygen
```

# MessageService.h
```c++
.. doxygenfile:: MessageService.h
  :project: doxygen
```

# ServiceConnection.h
```c++
.. doxygenfile:: ServiceConnection.h
  :project: doxygen
```

# Service.h
```c++
.. doxygenfile:: Service.h
  :project: doxygen
```

# UvLoop.h
```c++
.. doxygenfile:: UvLoop.h
  :project: doxygen
```

# ActivityTrace.h
```c++
.. doxygenfile:: ActivityTrace.h
  :project: doxygen
```