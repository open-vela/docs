# xTS认证测试用例精简集

## 文档说明

本开源文档旨在为个人开发者提供自测用例的标准化参考框架，帮助用户快速理解用例构成、测试方法及适配规则。通过明确测试范围与流程，提升测试效率与兼容性验证质量。


1. 本文档用于个人开发者快速了解自测用例构成和测试方法，根据芯片特性选择适配测试用例，提升测试效率
2. 测试用例中的通用自测用例和品类自测用例为测试类型，通用自测用例为必测项，品类自测用例需要根据产品特性进行选测
3. 若测试用例不适配或者对测试用例步骤有疑问，可于开源论坛说明主要问题，社区维护团队将定期审核反馈
4. 测试类型为"功能"的测试用例可直接采用普通办公环境或家居环境，不强制要求环境细节。若测试类型为"性能""稳定性"的测试用例，需要在干净无干扰环境进行测试（如蓝牙）

| 部门名称 | 最新版本 | 生效日期 |
|---------|---------|---------|
| openvela 社区维护团队 | V1.0 | 2026-05-19 |

---

## 一、通用自测用例

### 1. 功能测试

#### 1.1 系统内核

##### 1.1.1 系统内存管理测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内存管理

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTS_TESTSUITES=y
CONFIG_TESTS_TESTSUITES_STACKSIZE=16384
CONFIG_CM_MM_TEST=y
+CONFIG_ARCH_SETJMP_H=y
+CONFIG_BUILTIN=y
+CONFIG_NSH_BUILTIN_APPS=y
+CONFIG_SCHED_HAVE_PARENT=y
+CONFIG_SCHED_LPWORK=y
```

2、打开后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh>中输入 cmocka_mm_test
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.1.2 系统调度测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 系统调度

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTS_TESTSUITES=y
CONFIG_TESTS_TESTSUITES_STACKSIZE=16384
CONFIG_CM_SCHED_TEST=y
+CONFIG_ARCH_SETJMP_H=y
+CONFIG_BUILTIN=y
+CONFIG_NSH_BUILTIN_APPS=y
+CONFIG_PSEUDOFS_SOFTLINKS=y
+CONFIG_SCHED_HAVE_PARENT=y
+CONFIG_SCHED_LPWORK=y
```

2、打开后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh>中输入 cmocka_sched_test
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.1.3 系统调用测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 系统调用

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTS_TESTSUITES=y
CONFIG_TESTS_TESTSUITES_STACKSIZE=16384
CONFIG_CM_SYSCALL_TEST=y
+CONFIG_ARCH_SETJMP_H=y
+CONFIG_BUILTIN=y
+CONFIG_NSH_BUILTIN_APPS=y
+ CONFIG_FAT_LFN=y
+CONFIG_IOB_NBUFFERS=128
+CONFIG_IOB_NCHAINS=4
+CONFIG_NET=y
+CONFIG_NETDEV_LATEINIT=y
+CONFIG_NET_ICMP=y
+CONFIG_NET_LOCAL=y
+CONFIG_NET_SOCKOPTS=y
+CONFIG_NET_TCP=y
+CONFIG_NET_UDP=y
+CONFIG_PSEUDOFS_SOFTLINKS=y
+CONFIG_SCHED_HAVE_PARENT=y
+CONFIG_SCHED_LPWORK=y
```

2、打开后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh>中输入 cmocka_syscall_test
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.1.4 Kernel-ostest测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内核Kernel

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_OSTEST=y
```

2、打开后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 ostest
2、等待执行结果

**预期结果：**

测试中无error
ostest_main: Exiting with status 0

---

##### 1.1.5 Kernel-getprime测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内核Kernel

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_GETPRIME=y
```

2、打开后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 getprime
2、等待执行结果

**预期结果：**

getprime took xxx msec

---

##### 1.1.6 Kernel-mm内存测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内核Kernel

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_MM=y
```

2、打开后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 mm
2、等待执行结果

**预期结果：**

测试全部pass且测试结束后nsh终端打印TEST COMPLETE

---

##### 1.1.7 Kernel-scanftest扫描测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内核Kernel

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_SCANFTEST=y
CONFIG_LIBC_FLOATINGPOINT=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入scanftest
2、等待执行结果

**预期结果：**

测试完成后，nsh终端打印Test /#25 PASSED

---

##### 1.1.8 Kernel-C测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内核Kernel

**前提条件：**

1、打开如下配置：

```
CONFIG_EXAMPLES_HELLO=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入hello
2、等待执行结果

**预期结果：**

测试完成后，nsh终端打印Hello, World!!

---

##### 1.1.9 Kernel-Cxx测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内核Kernel

**前提条件：**

1、打开如下配置：

```
CONFIG_HAVE_CXX=y
CONFIG_EXAMPLES_HELLOXX=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入helloxx
2、等待执行结果

**预期结果：**

测试完成后，nsh终端打印CHelloWorld::HelloWorld

---

##### 1.1.10 Kernel-popen测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内核Kernel

**前提条件：**

1、打开如下配置：

```
CONFIG_SYSTEM_POPEN=y
CONFIG_EXAMPLES_POPEN=y
CONFIG_DISABLE_POSIX_TIMERS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入popen
2、等待执行结果

**预期结果：**

测试完成后，nsh终端打印Calling pclose()

---

##### 1.1.11 Kernel-pipe测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内核Kernel

**前提条件：**

1、打开如下配置：

```
CONFIG_PIPES=y
CONFIG_EXAMPLES_PIPE=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入以下命令：
pipe
rm /var/testfifo-1
rm /var/testfifo-1
2、等待执行结果

**预期结果：**

执行pipe指令测试完成后，nsh终端打印Returning success

---

##### 1.1.12 Kernel-md5值测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内核Kernel

**前提条件：**

1、添加任意测试文件（如1.txt）到etc目录
2、打开如下配置：

```
CONFIG_TESTS_TESTCASES
CONFIG_FS_TEST
CONFIG_FS_TEST_EDONLY
```

3、打开上述配置后进行编译
4、烧录刚刚编译的bin包
5、打开nsh窗口

**步骤：**

1、在nsh中输入 md5_test -f /etc/1.txt -c 100，1.txt为etc目录下文件
2、等待执行结果

**预期结果：**

得到100个md5值，且一致

---

##### 1.1.13 Kernel-C++功能测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.1 系统内核 > 内核Kernel

**前提条件：**

1、打开如下配置：

```
CONFIG_HAVE_CXX=y
CONFIG_EXAMPLES_HELLOXX=y
CONFIG_TESTING_CXXTEST=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 cxxtest
2、等待执行结果

**预期结果：**

测试完成后，nsh终端打印
Test std::vector ============================
v1=1 2 3
s1=Hello, World!
Hello World Good Luck
Test std::map ============================
Test RTTI ============================
extend

---

#### 1.2 系统应用

##### 1.2.1 Reboot启动异常测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.2 系统应用 > Boot

**前提条件：** 1、打开nsh窗口

**步骤：**

1、在nsh中输入 reboot
2、查看设备启动log：启动开始对应的关键字‘reboot’，到系统启动完成对应的的关键字‘NuttShell (NSH)’log中是否有error等异常

**预期结果：**

1、设备重启成功
2、串口log无异常error

---

##### 1.2.2 Cold boot启动异常测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.2 系统应用 > Boot

**前提条件：** 1、打开nsh窗口

**步骤：**

1、在设备端按下reset按键
2、查看设备启动log：启动开始到系统启动完成对应的的关键字‘NuttShell (NSH)’log是否有error等异常

**预期结果：**

1、设备重启成功
2、串口log无异常error

---

##### 1.2.3 系统RAM资源占用统计

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.2 系统应用 > Footprint

**前提条件：** 1、打开nsh窗口

**步骤：**

1、在nsh中输入 Free，若存在多核需在每个核都输入
2、等待执行结果

**预期结果：**

1、统计当前系统总体RAM使用情况

---

##### 1.2.4 系统Flash资源占用统计

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.2 系统应用 > Footprint

**前提条件：** 1、打开nsh窗口

**步骤：**

1、在nsh中输入df -h，(需要厂商提供硬件Flash资源占用情况),若存在多核，需提供每个核的使用情况，并在每个核都输入

**预期结果：**

1、统计当前系统硬件Flash资源占用情况

---

#### 1.3 驱动BSP

##### 1.3.1 烧写测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：** 1、准备烧录工具和烧写版本

**步骤：**

1、参照指导文档将版本烧写到flash
2、重启设备，进入设备nsh终端
注意：烧写指导文档和烧录工具由厂商提供，小米根据对应方法进行验收

**预期结果：**

2、能正常烧录，烧录成功后，重启设备，能正常进去nsh终端，系统正常启动

---

##### 1.3.2 RAM读写测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_FSTEST
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 fstest -n 10 -m /tmp
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.3.3 RAM读写性能测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1、打开如下配置:

```
CONFIG_TESTING_RAMTEST
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口
注：参考文档参见

**步骤：**

1、在nsh中输入 free，获取系统当前最大空闲内存块(largest)的size
2、在nsh中输入 ramtest [-w|h|b] -s <size>，等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.3.4 RAM随机读写测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA
CONFIG_TESTING_DRIVER_TEST
CONFIG_TESTING_DRIVER_TEST_STACKSIZE=8192
CONFIG_BCH
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口
5、在测试平台/dev下可以找到RAM对应的设备名称：ls /dev

**步骤：**

1、在nsh中输入以下命令：
mkrd -m 10 -s 1000 1024
cmocka_driver_block -m /dev/dev_name，其中dev_name根据实际的设备名称来填写
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.3.5 Flash功能测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1、打开如下配置： 

```
CONFIG_TESTING_CMOCKA
CONFIG_TESTING_DRIVER_TEST
CONFIG_TESTING_DRIVER_TEST_STACKSIZE=8192
CONFIG_BCH
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口
5、在测试平台/dev下可以找到Flash对应的设备名称：ls /dev

**步骤：**

1、在nsh中输入 cmocka_driver_block -m /dev/dev_name，其中dev_name根据实际的设备名称来填写
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.3.6 GPIO功能测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1、打开如下配置： 

```
CONFIG_TESTING_CMOCKA
CONFIG_TESTING_DRIVER_TEST
CONFIG_TESTING_DRIVER_TEST_STACKSIZE=8192
CONFIG_DEV_GPIO
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口
5、测试平台支持GPIO驱动
ls /dev -> gpio0
ls /dev -> gpio1
6、将两个目标GPIO对应的管脚通过杜邦线链接在一起，并通过设置gpio_a与gpio_b完成测试，无配置情况下，两个地址默认为dev/gpio0与dev/gpio1

**步骤：**

1、在nsh中输入 cmocka_driver_gpio -a /dev/gpio0 -b /dev/gpio1
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.3.7 I2c/Spi功能测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_USENSOR=y
CONFIG_UORB=y
CONFIG_SENSORS=y
CONFIG_SENSORS_BMI160=y
CONFIG_DEBUG_UORB=y
CONFIG_SENSORS_BMI160_I2C=y
CONFIG_SENSORS_BMI160_SPI=y
```

# 如果是测试I2C，则打开
# 如果是测试SPI，则打开
2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、将BMI160传感器和板子连接起来
5、打开nsh窗口
注：
1）CONFIG_SPI或CONFIG_I2C，每次只能选择其中的一种测试，不能将配置一起打开
2）需要同时打开BMI160传感器，并给传感器配置SPI或I2C来实现SPI或I2C的测试，具体可参考文档
3）同时BM160传感器自带陀螺仪和加速计两个sensor，可用来测试uORB框架通路正常，以替代驱动部分Sensor的验证

**步骤：**

1、在nsh中输入 cmocka_driver_i2c_spi
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.3.10 Uart串口功能测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_SERIAL=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、使用串口小板连接设备和PC：
USB2UART Host
TX -- RX
RX -- TX

**步骤：**

优先用手动测试，脚本存在问题需要修正
| 手动测试
1、在nsh中输入 ls /dev，以查询设备名称，如ttyS0
2、在nsh中输入：cmocka_driver_uart -d /dev/ttyS0
3、在串口粘贴复制如下内容并回车
0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,./<>?;':"[]{}\|!@/#$%^&/*()-+_=
4、输入0 然后回车
5、输入/#
6、查看是否测试PASS
| 脚本测试
1、在插入了USB转UART模块的电脑上，在/dev目录中找到对应的tty设备：ls /dev/ttyUSB/* ，/*为数字
2、在电脑终端执行：
sudo python3 testing/drivertest/test_content_gen.py /dev/ttyUSB/*（/*根据实际情况填写）
3、在nsh中输入 ls /dev，以查询设备名称，如ttyS4
4、继续在nsh中输入 cmocka_driver_uart -d /dev/ttyS4，等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.3.11 Uart文件传输功能测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：** 1、打开nsh窗口

**步骤：**

1、参考以下文档进行测试


**预期结果：**

文件发送和接收功能均正常

---

##### 1.3.12 RTC时钟功能测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_RTC=y
CONFIG_RTC_DRIVER=y
CONFIG_RTC_ARCH=y
CONFIG_RTC_PERIODIC=y
CONFIG_RTC_IOCTL=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_TESTING_CMOCKA=y
CONFIG_SIG_EVTHREAD=y
CONFIG_RTC_ALARM=y
CONFIG_DRIVERS_RTC=y
CONFIG_RTC_DATETIME=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 cmocka_driver_rtc
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 1.3.13 Timer定时器功能测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

Timer作为系统时钟分为arch alarm和arch timer两种，需判断厂商适配的是哪种timer，执行ls /dev，看下被注册的是哪种设备节点，arch alarm为/dev/oneshot，arch timer为/dev/timer
1、打开如下配置：

```
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_TESTING_CMOCKA=y
CONFIG_ONESHOT=y
CONFIG_ALARM_ARCH=y
CONFIG_TIMER=y
CONFIG_TIMER_ARCH=y
```

1）若厂商适配arch alarm，需打开
2）若厂商适配arch timer，需打开
2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

若厂商适配arch alarm
1、在测试平台/dev下可以找到oneshot对应的设备名称：ls /dev
2、在nsh中输入 cmocka_driver_oneshot -d /dev/oneshot/*，/*为数字
3、等待执行结果
若厂商适配arch timer
4、在测试平台/dev下可以找到oneshot对应的设备名称：ls /dev
5、在nsh中输入 cmocka_driver_oneshot -d /timer/*，/*为数字
6、等待执行结果

**预期结果：**

3、默认延迟25s后输出测试结果，测试结果PASS且无异常
6、默认延迟20s后输出测试结果，测试结果PASS且无异常

---

##### 1.3.14 时间一致性测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：** 1、PC通过串口minicom进入设备主核
2、设备启动正常，并确保未进行配网（主要目的是排除ntp同步对时间的影响）

**步骤：**

1. 打开minicom时间：串口执行ctrl+a，n，回车
2、主核设置与当前PC时间一致，eg: date -s "Nov 11 11:11:00 2022"
3、在nsh中输入 date
4、每隔6h 检查一次date（共检查4次）

**预期结果：**

1、显示当前PC时间
2、设置成功，无报错
3、设备回调时间与PC当前时间一致
4、设备静置24小时以上回调时间与pc当前时间差<=2s

---

##### 1.3.15 Watchdog测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1. 打开如下配置：

```
CONFIG_WATCHDOG=y
CONFIG_BOARDCTL_RESET_CAUSE=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_CMOCKA=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口
注：芯片厂商初始化wdt时需要在wdt中断里面主动调用panic，并且提高watchdog中断优先级，保证在watchdog中断可以打断critical_section，在关中断的情况下不喂狗也可以进入wdt中断。

**步骤：**

1、在nsh中依次输入如下命令：
cmocka_driver_watchdog -r 0 //测试到达timeout后看门狗是否生效
cmocka_driver_watchdog -r 1 //测试打断critical_section，在关中断的情况下不喂狗也可以进入wdt中断。
cmocka_driver_watchdog -r 2 //测试开中断后死循环看门狗是否生效
cmocka_driver_watchdog -r 3 //测试正常喂狗，结果输出PASS
说明：执行命令cmocka_driver_watchdog，通过-r传入参数，参数为0-3，分别进入4个不同的case，所以watchdog的测试需要执行四次，参数从0到3依次执行（需按顺序执行）

**预期结果：**

1、观察-r参数为 0/1/2测试咬狗状态能否主动触发asser和打印堆栈信息并重启，并且重启原因是BOARDIOC_RESETCAUSE_SYS_RWDT，-r 参数为3时正常喂狗输出PASS

---

##### 1.3.16 RNG功能测试


**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_NIST_STS=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_CMOCKA=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、按下述方法执行：
cd /tmp
mkdir -p experiments/AlgorithmTesting/ApproximateEntropy
mkdir -p experiments/AlgorithmTesting/CumulativeSums
mkdir -p experiments/AlgorithmTesting/Frequency
mkdir -p experiments/AlgorithmTesting/LongestRun
mkdir -p experiments/AlgorithmTesting/OverlappingTemplate
mkdir -p experiments/AlgorithmTesting/RandomExcursionsVariant
mkdir -p experiments/AlgorithmTesting/Runs
mkdir -p experiments/AlgorithmTesting/Universal
mkdir -p experiments/AlgorithmTesting/BlockFrequency
mkdir -p experiments/AlgorithmTesting/FFT
mkdir -p experiments/AlgorithmTesting/LinearComplexity
mkdir -p experiments/AlgorithmTesting/NonOverlappingTemplate
mkdir -p experiments/AlgorithmTesting/RandomExcursions
mkdir -p experiments/AlgorithmTesting/Rank
mkdir -p experiments/AlgorithmTesting/Serial
nist_sts 400000
2、进入测试程序后依次输入：
0
/dev/urandom/
1
0
10
1
3、查看结果：cat /tmp/experiments/AlgorithmTesting/finalAnalysisReport.txt

**预期结果：**

P-Value是全部测试结果的卡方分布的累计值，其值大于0.0001即可认为该随机数样本具有足够的均匀性与独立性，当值不够随机时在值后以及测试项名称前会有/*标记该项

---

##### 1.3.17 Crypto功能测试

**测试目的：** 一、通用自测用例 > 1、功能测试 > 1.3 驱动BSP

**前提条件：**

1、打开如下配置

```
CONFIG_TESTING_CRYPTO=y
CONFIG_TESTING_CRYPTO_3DES_CBC=y
CONFIG_TESTING_CRYPTO_AES_CBC=y
CONFIG_TESTING_CRYPTO_AES_CTR=y
CONFIG_TESTING_CRYPTO_3DES_XTS=y
CONFIG_TESTING_CRYPTO_HMAC=y
CONFIG_TESTING_CRYPTO_HASH=y
CONFIG_TESTING_CRYPTO_CRC32=y
CONFIG_TESTING_CRYPTO_ECDSA=y
```

1）若厂商硬件支持des3cbc算法，则需打开配置
2）若厂商硬件支持aescbc算法，则需打开配置
3）若厂商硬件支持aesctr算法，则需打开配置
4）若厂商硬件支持aesxts算法，则需打开配置
5）若厂商硬件支持hmac算法，则需打开配置
6）若厂商硬件支持hash算法，则需打开配置
7）若厂商硬件支持crc32算法，则需打开配置
8）若厂商硬件支持ecdsa算法，则需打开配置
2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口
注：Vela Crypto框架提供了des3cbc、aescbc、aesctr、aesxts、hmac, hash, crc32, ecdsa这六个测试应用，厂商根据实际硬件实现的算法连接测试

**步骤：**

1、确认厂商硬件实现的算法，并在nsh中输入对应算法名称，等待执行结果
举例：若厂商硬件实现了des3cbc算法，即在nsh中输入 des3cbc即可

**预期结果：**

测试程序正常运行结束，并显示结果ok

---

### 2. 性能测试

#### 2.1 系统应用

##### 2.1.3 Cold Boot启动时间测试

**测试目的：**  验证系统cold boot时长符合OS标准

**前提条件：** 1、 测试设备串口正常 

**步骤：**

1、将设备上下电cold boot 10次，统计minicom串口工具时间戳开始，到系统启动完成对应的的关键字‘NuttShell (NSH)’的平均启动时长
 注：
1）打开minicom时间戳打印：ctrl +A +Z +N
2）整理log竖排打印：ctrl +A +U

**预期结果：**

1、设备cold boot 10次平均时长不超过4秒 

---

##### 2.1.4 Reboot启动时间测试

**测试目的：**  验证系统设备reboot系统启动时长符合OS标准

**前提条件：** 1、 测试设备串口正常 

**步骤：**

1、在nsh中输入 reboot 10次，统计minicom串口工具时间戳reboot开始，到系统启动完成对应的的关键字‘NuttShell (NSH)’的平均启动时长
 注：
1）打开minicom时间戳打印：ctrl +A +Z +N
2）整理log竖排打印：ctrl +A +Z+U

**预期结果：**

1、设备reboot 10次平均时长不超过6秒 

---

### 3. 稳定性测试

#### 3.1 系统内核

##### 3.1.1 12h待机稳定性测试

**测试目的：** 验证设备未配网状态下，长时间待机，系统无异常

**前提条件：**

1、将设备上电
2、编译开启内存监控kasan和show_info测试工具的版本
开启show_info
LOW_RESOURCE_TEST=y
启用kasan

```
CONFIG_MM_KASAN=y
```

**步骤：**

1、设备静置12h，保存串口log

**预期结果：**

1、系统无报错、crash、重启等异常情况

---

## 二、品类自测用例

### 1. 功能测试

#### 系统应用

##### 全包升级--升级成功后启动到bl2进行avb_verify过程中断电

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > OTA

**前提条件：** 1.设备供电正常
2.设备软硬件版本支持ymodem或Wi-Fi或adb push工具下载ota包到待测设备内
3.确认设备内置的版本base在差分包的base版本上
（备注：例如设备内的版本为old，需要升级的差分包是new to old,即为设备内置的版本未base在差分包的base版本上）

**步骤：**

1.使用相关工具将差分升级包传输到设备的/data目录下，并修改升级包名称为‘ota.zip’；
备注：
adb : adb push <本地ota包> /data
Wi-Fi:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
curl -o /data/ota.zip <服务器链接地址>/<ota包>
2. 执行reboot recovery，查看设备串口log出现'ota success'关键字后设备重启，启动到bl2中进行avb_verify过程中（需要覆盖avb_verify所有bin文件过程中断电），设备断电，反复上下电20次，查看设备串口log，系统是否有异常卡住、crash等现象
工具使用参照ymodem：


**预期结果：**

2.查看设备串口log：启动到bl2中进行avb_verify过程中，设备反复断电，上电后系统启动无异常

---

### 4. 兼容性测试

##### 6.1.1 路由器兼容性

**测试目的：** 二、品类自测用例 > 6、兼容性测试 > 6.1 系统应用

**步骤：**

参照附件 [WiFi兼容性路由器列表.md](WiFi兼容性路由器列表.md) 中提供的路由器品牌型号以及兼容性测试用例详情

**预期结果：**

设备与多种型号的路由器都能成功建立STA连接

---

### 2. 性能测试

##### 5.1.9 文件系统多线程读文件vela_fs_multi_thread_read_test

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、执行vela_fs_multi_thread_read_test testPath=<DIR> dataLen=xxx
注：
1）dataLen可随意设置，如1000
2）DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出TEST PASSED

---

##### 5.1.8 文件系统多线程写文件测试vela_fs_multi_thread_write_test

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、 执行vela_fs_multi_thread_write_test testPath=<DIR> dataLen=xxx
注：
1）dataLen可随意设置，如1000
2）DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出TEST PASSED

---

##### 5.1.7 文件系统随机读写测试vela_fs_random_read_and_write_test

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中执行以下命令：
vela_fs_random_read_and_write_test
writeCount=1000
readCount=1000
mountPath=<DIR>
注：
1） Count可视情况而定,一般1min以内就会执行完,而有的文件系统count设为100都可能执行半天)
2）DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出读和写的时间,且时间在合理范围（毫秒级）

---

##### 5.1.68 KVDB稳定性vela_kvdb_stability_test02测试

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > KVDB

**前提条件：**

1.打开如下配置编译烧录

```
CONFIG_TESTS_TESTCASES=y
CONFIG_KVDB_TEST=y
CONFIG_KVDB_TEST_STABILITY=y
```

**步骤：**

1.进入nsh
2.删除/data目录下的文件persist.db，删除后重启设备
3.执行命令 vela_kvdb_stability_test02 10
（注意参数10是执行轮次，没有上线，执行10次约12分钟）

**预期结果：**

执行成功打印 TEST PASSED!
失败打印 TEST FAILED!

---

##### 5.1.6 文件系统反复读写测试vela_fs_stress_read_and_write_loops_test

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 vela_fs_stress_read_and_write_loops_test <DIR>
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出TEST PASSED

---

##### 5.1.58 全包升级总耗时

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > OTA

**前提条件：** 设备上电

**步骤：**

1、进行10次全包升级，统计设备串口log中从执行“reboot 1”到打印‘‘ota success’’的平均总时长

**预期结果：**

1、请厂商提供全包升级总时长

---

##### 5.1.5 文件系统多线程文件读写测试vela_fs_stress_multi_thread_file_operate_test

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 vela_fs_stress_multi_thread_file_operate_test <DIR>
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出TEST PASSED

---

##### 5.1.42 WiFi--设备未配网时反复扫描周边无线AP

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell
2、执行ifup wlan0;
3、执行wapi scan wlan0
4、重复步骤3执行100次，查看返回结果是否有变化，串口log是否有扫描失败情况或扫描异常报错

**预期结果：**

1-3、执行成功无报错，可搜索到周边的SSID
4、返回列表会变化，没有扫描失败或者异常报错的情况

---

##### 5.1.41 WiFi--反复ifup&ifdown

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、在nuttx中执行如下命令：
ifup wlan0
ifdown wlan0
2、循环执行100次

**预期结果：**

2、执行无报错，系统无异常

---

##### 5.1.40 WiFi--屏蔽箱中更换设备时的吞吐变化

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、屏蔽箱环境，设备衰减rssi值在-20~-10范围内
2、将设备上电并配网在线

**步骤：**

1、设备通过wapi配网
2、设备端执行：iperf -s -p 5001 -i 1
3、PC端执行：iperf -c 【设备的ip地址】-i 1 -p 5001 -l 1460 -t 300
4、依次更换设备角度90度、180度、270度、360度，分别重复步骤2-3，查看四个角度下，设备端的平均吞吐

**预期结果：**

4、四个角度的设备平均吞吐值浮动范围在10%以内
注：
1）请在测结果中标明【测试环境】【测试路由器】【iperf版本】
2）保留测试log

---

##### 5.1.4 文件系统反复创建和删除文件vela_fs_stress_maximum_file_name_test

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入vela_fs_stress_maximum_file_name_test <DIR>
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出TEST PASSED
注：
1）对于有的文件系统如fatfs，该case可能会运行失败；但只要不crash，且文件系统还可以正常使用就可认为符合预期
2）测试产生的文件无法正常删除，只能通过umount，再mount --forceformat 重新挂载文件系统来删除)

---

##### 5.1.39 WiFi--5G网络---wapi反复disconnect 5G网络

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看wlan0的ip;
4、执行wapi disconnect wlan0；
5、ping <wlan0 接口IP地址>
6、再次配网
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID>1
renew wlan0 ；
7、执行ping router_ip (注：router_ip为路由器网关IP)
8、重复步骤3-7 100次

**预期结果：**

2、设备配网成功；
3、可查看到IP地址，该IP地址为路由器分配的ip
4、执行成功，无报错；
5、不可以ping通
6、再次配网成功无报错
7、可以ping通外网
8、重复100次全部成功无报错

---

##### 5.1.38 WiFi--5G网络---设备连接5G后wapi扫描指定2.4G AP

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi scan wlan0 <指定2.4G ssid>；
4、重复步骤3执行100次，查看返回结果是否有变化，串口log是否有扫描失败情况或扫描异常报错

**预期结果：**

1-3、执行成功无报错，可搜索到指定的2.4G SSID
4、返回结果不会产生变化，扫描列表无异常无报错

---

##### 5.1.37 WiFi-5G网络---设备连接5G后wapi扫描指定5G AP

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi scan wlan0 <指定5G ssid>；
4、重复步骤3执行100次，查看返回结果是否有变化，串口log是否有扫描失败情况或扫描异常报错

**预期结果：**

1-3、执行成功无报错，可搜索到指定的5G SSID
4、返回结果不会产生变化，扫描列表无异常无报错

---

##### 5.1.36 WiFi--5G网络---设备连接5G后wapi反复扫描周边无线AP

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi scan wlan0；
4、重复步骤3执行100次，查看返回结果是否有变化，串口log是否有扫描失败情况或扫描异常报错

**预期结果：**

1-3、执行成功无报错，可搜索到周边的SSID
4、返回列表会变化，没有扫描失败或者异常报错的情况

---

##### 5.1.35 WiFi--5G网络---设备作为Client端时的UDP Tx平均速率

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与PC均处于同一局域网

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看设备分配到的ip地址;
4、设备端执行：iperf2 -c 【对端PC的ip地址】-i 1 -p 5004 -t 300 -u -b 40M
5、PC端执行：iperf -s -p 5004 -i 1 -u

**预期结果：**

5、设备作为Client端，UDP下行速率符合标准
注：
1）需在测结果中标明【测试环境】【测试路由器】【iperf版本】
2）保留测试log

---

##### 5.1.34 WiFi--5G网络---设备作为Server端时的UDP Rx平均速率

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与PC均处于同一局域网

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看设备分配到的ip地址
4、设备端执行：iperf2 -s -p 5003 -i 1 -u
5、PC端执行：iperf -c 【设备的ip地址】-i 1 -p 5003 -t 300 -u -b 40M

**预期结果：**

5、设备作为Server端，UDP下行速率符合标准
注：
1）需在测结果中标明【测试环境】【测试路由器】【iperf版本】
2）保留测试log

---

##### 5.1.33 WiFi--5G网络---设备作为Client端时的TCP Tx平均速率

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与PC均处于同一局域网

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看设备分配到的ip地址
4、设备端执行：iperf2 -c 【对端PC的ip地址】-i 1 -p 5002 -t 300
5、PC端执行：iperf -s -p 5002 -i 1

**预期结果：**

5、设备作为Client端，TCP下行速率符合标准
注：
1）需在测结果中标明【测试环境】【测试路由器】【iperf版本】
2）保留测试log

---

##### 5.1.32 WiFi--5G网络---设备作为Server端时的TCP Rx平均速率

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与PC均处于同一局域网

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig,查看设备分配到的ip地址
4、设备端执行：iperf2 -s -p 5001 -i 1
5、PC端执行：iperf -c 【设备的ip地址】-i 1 -p 5001 -t 300

**预期结果：**

5、设备作为Server端，TCP下行速率符合标准
注：
1）需在测结果中标明【测试环境】【测试路由器】【iperf版本】
2）保留测试log

---

##### 5.1.31 WiFi--5G网络---屏蔽箱环境STA连接成功率

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与路由器、PC均处于屏蔽箱中

**步骤：**

1、在屏蔽箱环境下，使用脚本挂测设备STA连接1000次，统计连接成功率

**预期结果：**

1、屏蔽箱环境下，设备连接成功率100%

---

##### 5.1.30 WiFi--5G网络---屏蔽箱环境ping包时延

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与路由器、PC均处于屏蔽箱中

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看设备分配到的ip地址
4、PC端执行：ping 设备IP地址，持续十分钟（600秒）
5、查看PC端log，统计ping包时延

**预期结果：**

5、统计ping包时不低于2ms
注：请在测结果中标明【测试环境】【测试路由器】

---

##### 5.1.3 文件系统创建和删除压力测试vela_fs_stress_loop_create_delete_file_test

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 vela_fs_stress_loop_create_delete_file_test <DIR>
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出TEST PASSED

---

##### 5.1.28 WiFi--2.4G网络---设备连接2.4G后wapi扫描指定5G AP

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi scan wlan0 <指定5G ssid>；
4、重复步骤3执行100次，查看返回结果是否有变化，串口log是否有扫描失败情况或扫描异常报错

**预期结果：**

1-3、执行成功无报错，可搜索到指定的5G SSID
4、返回结果不会产生变化，扫描列表无异常无报错

---

##### 5.1.26 WiFi--2.4G网络---设备连接2.4G后wapi反复扫描周边无线AP

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi scan wlan0；
4、重复步骤3执行100次，查看返回结果是否有变化，串口log是否有扫描失败情况或扫描异常报错

**预期结果：**

1-3、执行成功无报错，可搜索到周边的SSID
4、返回列表会变化，没有扫描失败或者异常报错的情况

---

##### 5.1.25 WiFi--2.4G网络---设备作为Client端时的UDP Tx平均速率

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与PC均处于同一局域网

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看设备分配到的ip地址;
4、设备端执行：iperf2 -c 【对端PC的ip地址】-i 1 -p 5004 -t 300 -u -b 40M
5、PC端执行：iperf -s -p 5004 -i 1 -u

**预期结果：**

5、设备作为Client端，UDP下行速率符合标准
注：
1）需在测结果中标明【测试环境】【测试路由器】【iperf版本】
2）保留测试log

---

##### 5.1.24 WiFi--2.4G网络---设备作为Server端时的UDP Rx平均速率

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与PC均处于同一局域网

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看设备分配到的ip地址
4、设备端执行：iperf2 -s -p 5003 -i 1 -u
5、PC端执行：iperf -c 【设备的ip地址】-i 1 -p 5003 -t 300 -u -b 40M

**预期结果：**

5、设备作为Server端，UDP下行速率符合标准
注：
1）需在测结果中标明【测试环境】【测试路由器】【iperf版本】
2）保留测试log

---

##### 5.1.22 WiFi--2.4G网络---设备作为Server端时的TCP Rx平均速率

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与PC均处于同一局域网

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig,查看设备分配到的ip地址
4、设备端执行：iperf2 -s -p 5001 -i 1
5、PC端执行：iperf -c 【设备的ip地址】-i 1 -p 5001 -t 300

**预期结果：**

5、设备作为Server端，TCP下行速率符合标准
注：
1）需在测结果中标明【测试环境】【测试路由器】【iperf版本】
2）保留测试log

---

##### 5.1.21 WiFi--2.4G网络---屏蔽箱环境STA连接成功率

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与路由器、PC均处于屏蔽箱中

**步骤：**

1、在屏蔽箱环境下，使用脚本挂测设备STA连接1000次，统计连接成功率

**预期结果：**

1、屏蔽箱环境下，设备连接成功率100%

---

##### 5.1.2 文件系统文件写入速度测试vela_fs_stress_write_speed

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 vela_fs_stress_write_speed <DIR>
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出TEST PASSED

---

##### 5.1.19 文件系统crash后文件完整性校验vela_fs_stability_test04 文件

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=32768
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、执行vela_fs_stability_test04 [DIR]
2、等待10-20秒后手动触发板子重启（retset按键\手动触发crash\断电重启均可）
3、系统完成重启后再次执行vela_fs_stability_test04 [DIR]
4. 用例会检查重启后文件系统分区是否正常，之前写入的文件是否正常（写入的内容无丢失，文件可再次读写）
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、测试成功会输出“TEST PASSED”

---

##### 5.1.18 文件系统crash后crc校验 vela_fs_stability_test03

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 vela_fs_stability_test03 mode=reboot [DIR]，程序自动重启后再次执行vela_fs_stability_test03 mode=reboot [DIR]
2、在nsh中输入 vela_fs_stability_test03 mode=crash [DIR]，程序自动重启后再次执行vela_fs_stability_test03 mode=crash [DIR]
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1/2、输出TEST PASSED

---

##### 5.1.17 文件系统多线程操作文件测试vela_fs_stability_test01

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 vela_fs_stability_test01 -d DIR -t 1
注：
1）-t 指定运行时间,单位为h, 一般为12h
2） DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出TEST PASSED

---

##### 5.1.16 文件系统碎片读写测试vela_fs_file_fragmentation_test

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置

```
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中依次输入如下命令：
mkdir /DIR/fstest
vela_fs_file_fragmentation_test -d /DIR/fstest -n 1000 -s 20，其中参数说明如下：
-d: set test dir path. -- 测试运行的目录
-n: The number of small files created in the test. -- 测试中产生的小文件数量（每个小文件的大小随机产生，最大不超过128字节）
-s: Large file size created in test. (unit:M)\n") -- 测试中产生的大文件大小上限，单位M
注：
1）测试中根据芯片资源的实际情况，合理填写 -n 和 -s参数
2）DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、运行一段时间后无异常

---

##### 5.1.15 文件系统fstest执行1000次

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_FSTEST=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中依次输入如下命令：
mkdir DIR/fstest
fstest -m DIR/fstest -n 1000
rm -r DIR/fstest
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、程序正常执行,无crash,没有输出error
注：有的设备运行1000次需要2天时间

---

##### 5.1.14 只读文件系统性能测试

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_NSH_CMDOPT_DD_STATS=y
CONFIG_DEV_NULL=y
CONFIG_DEV_ZERO=y
CONFIG_NSH_DISABLE_DD=n
```

2、关闭如下配置：
3、打开上述配置后进行编译
4、烧录刚刚编译的bin包
5、打开nsh窗口
注：本case如无特殊要求，不需要测试

**步骤：**

1、在nsh中输入 dd if=（romfs下提前烧录好的测试文件） of=/dev/null bs=blocksize count=count (顺序读)

**预期结果：**

1、读写速率在合理范围

---

##### 5.1.13 裸设备读写性能测试

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_NSH_CMDOPT_DD_STATS=y
CONFIG_DEV_NULL=y
CONFIG_DEV_ZERO=y
CONFIG_NSH_DISABLE_DD=n
```

2、关闭如下配置：
3、打开上述配置后进行编译
4、烧录刚刚编译的bin包
5、打开nsh窗口

**步骤：**

1、查找待测试设备名称，例如 /dev/data
2、在nsh中输入 dd if=/dev/zero of=/dev/data bs=blocksize count=count (顺序写)
3、在nsh中输入 dd if=/dev/data of=/dev/null bs=blocksize count=count (顺序读)

**预期结果：**

2/3、测试无异常，输出读写速度

---

##### 5.1.12 文件系统读写速率测试dd

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_NSH_CMDOPT_DD_STATS=y
CONFIG_DEV_NULL=y
CONFIG_DEV_ZERO=y
CONFIG_NSH_DISABLE_DD=n
```

2、关闭如下配置：
3、打开上述配置后进行编译
4、烧录刚刚编译的bin包
5、打开nsh窗口

**步骤：**

1、在nsh中输入 dd if=/dev/zero of=DIR/payload bs=blocksize count=count (顺序写)
2、在nsh中输入 dd if=DIR/payload of=/dev/null bs=blocksize count=count (顺序读)

**预期结果：**

1/2、读写速率在合理范围
注意：厂商或个人测试只需要记录读写速率即可，由openvela社区安排进行验收

---

##### 5.1.11 文件系统读写速率测试performance_test

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
CONFIG_TESTING_TESTCASES_PRIORITY=255
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 performance_test -d DIR -b blocksize -c count -m 1 (顺序写)
2、在nsh中输入 performance_test -d DIR -b blocksize -c count -m 2 (顺序读)
3、在nsh中输入 performance_test -d DIR -b blocksize -c count -m 3 (随机写)
4、在nsh中输入 performance_test -d DIR -b blocksize -c count -m 4 (随机读)
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1/2/3/4、读写速率在合理范围
注意：厂商或个人测试只需要记录读写速率即可，由openvela社区安排进行验收

---

##### 5.1.10 文件系统的多线程读写测试vela_fs_multi_thread_read_write_test

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh窗口执行vela_fs_multi_thread_read_write_test -d <DIR>
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出TEST PASSED

---

##### 5.1.1 文件系统分区写满异常测试vela_fs_stress_write_full_file

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_FS_TEST=y
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST_FUNCTION=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 vela_fs_stress_write_full_file <DIR>
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

1、输出TEST PASSED

---

### 1. 功能测试

#### 驱动BSP

##### 4.2.9 Audio_DSP--Playback_cmoka_2channels

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 文件系统, 测试码流
声道,  采样深度,  采样率尽可能覆盖


**步骤：**

1、在nsh中输入 cmocka_driver_audio -a 2 -p /data/1000.pcm
注：
1）cmocka_driver_audio需要两个必填参数：
-a：1表示只采集，2表示只播放，3表示先采集再播放
-p：文件名，如 -p /data/1.pcm
2）默认音频设备为/dev/audio/pcm0p, /dev/audio/pcm0c，使用 -i 更改录制音频设备，如 -i /dev/audio/pcm1c；使用 -i 更改播放音频设备。例如 -i /dev/audio/pcm1p。
3）默认格式是AUDIO_FMT_PCM 使用-f改变格式，如 -f mp3
4）默认采样率为 44100，通道为 2，bps 为 16：使用 -s 更改采样率；使用 -c 改变频道；使用 -b 更改 bps。
5）默认记录时间为10s。使用-t 来改变

**预期结果：**

声音正常

---

##### 4.2.8 Audio_DSP--Playback_nxplayer

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 文件系统, 测试码流
声道,  采样深度,  采样率尽可能覆盖


**步骤：**

nxplayer
device pcm0p
playraw /data/8000.pcm 1 16 44100

**预期结果：**

声音正常

---

##### 4.2.7 Touch Panel测试2

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：**

1、打开如下配置：
旧版本：
LV_USE_TOUCHPAD_INTERFACE=y
LV_USE_LCDDEV_INTERFACE=y
LV_USE_FBDEV_INTERFACE=y
LV_USE_USER_DATA=y
升级到lvgl V9的：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_TESTING_DRIVER_TEST_STACKSIZE=8192
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口
注意：该测试命令有的分支没有，注意确认

**步骤：**

1、在nsh中输入：cmocka_driver_touchpanel
2、在屏幕上用手指点击、移动
3、点击屏幕左上角，沿着对角线移动手指到右下角
4、点击屏幕右上角，沿着对角线移动手指到左下角

**预期结果：**

3、四周可变成蓝色
4、对角线可变成蓝色

---

##### 4.2.6 Touch Panel测试1

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：**

1、 打开如下配置：

```
CONFIG_INPUT_TOUCHSCREEN=y
CONFIG_EXAMPLES_TOUCHSCREEN=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 tc

**预期结果：**

1、当手指或者鼠标在屏幕上点击 移动时 会在 nuttx shell上打印出当前的坐标

---

##### 4.2.5 Lcd测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_TESTING_DRIVER_TEST_STACKSIZE=8192
CONFIG_LCD_DEV=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口
5、测试平台支持lcd驱动：ls /dev -> lcd0

**步骤：**

cmocka -s cmocka_driver_framebuffer -t drivertest_framebuffer_black
cmocka -s cmocka_driver_framebuffer -t drivertest_framebuffer_white
cmocka -s cmocka_driver_framebuffer -t drivertest_framebuffer_cross
cmocka -s cmocka_driver_framebuffer -t drivertest_framebuffer_vertical
分别对应 4 个子用例（全屏黑 / 全屏白 / 黑红绿蓝白竖条 / 8 级灰度水平条）

**预期结果：**

1、屏幕变黑
2、屏幕变白
3、屏幕黑红绿蓝白
4、屏幕灰度渐变

---

##### 4.2.4 Framebuffer测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_TESTING_DRIVER_TEST_STACKSIZE=8192
CONFIG_VIDEO_FB=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口
5、测试平台支持fb驱动：ls /dev -> fb0

**步骤：**

1、在nsh中输入 cmocka_driver_framebuffer -p <devpath> -t <testcase>，其中参数的定义如下：
[-p devpath] selects the framebuffer device. Default: /dev/fb0
[-t testcase] selects the testcase to show framebuffer.
Case 0: show black color on FB
Case 1: show white color on FB
Case 2: show black|red|green|blue|white rectangle on FB
Case 3: show grayscale rectangle on FB
[-h] shows this message and exits

**预期结果：**

测试结果PASS，无异常

---

##### 4.2.3 2D-GPU测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 1、打开nsh窗口

**步骤：**

2d gpu 需要对接到lvgl里面，暂时直接用lvgl Demo验证即可，可参考以下文档，需要提供测量得到的benchmark分数


**预期结果：**

需要提供测量得到的benchmark分数

---

##### 4.2.25 AC 底座

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：**

1、修改如下配置：

```
CONFIG_R528_UART=y
CONFIG_UART4_BAUD=115200
CONFIG_COMLITE=y
CONFIG_OH4W_COMLITE=y
CONFIG_COMLITE_TEST_CMD=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1. 在 nsh 中输入 comlite_test -d 0 -c 1 
2. 在 nsh 中输入 comlite_test -d 0 -c 0

**预期结果：**

 comlite_test -d 0 -c 1：继电器0打开
 comlite_test -d 0 -c 0：继电器0关闭

---

##### 4.2.24 电源按键

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：**

1、修改如下配置：

```
CONFIG_EXAMPLES_BUTTONS=y
CONFIG_EXAMPLES_BUTTONS_DEVPATH=/dev/input/event1
CONFIG_DRIVERS_GPIO=y
CONFIG_INPUT=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在 nsh 中输入 buttons
2、按下/松开电源按键

**预期结果：**

终端输出：
Sample = 4
Sample = 0

---

##### 4.2.23 马达

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：**

1、修改如下配置：

```
CONFIG_TESTING_FF=y
CONFIG_INPUT_FF=y
CONFIG_DRIVERS_PWM=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在 nsh 中输入 fftest /dev/lra0
2、在 nsh 中输入 4
3、等待执行结果

**预期结果：**

马达震动 5s

---

##### 4.2.22 Relay

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_TESTING_DRIVER_TEST_STACKSIZE=8192
CONFIG_RELAY=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 cmocka_driver_relay
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 4.2.20 PWM

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_TESTING_DRIVER_TEST_STACKSIZE=8192
CONFIG_PWM=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 cmocka_driver_pwm
2、等待执行结果

**预期结果：**

测试结果PASS，无异常
注：需要厂商附上波形图

---

##### 4.2.2 USB（ADB）测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 1、打开nsh窗口

**步骤：**

1、启动adb任务后，可以通过adb shell 连接设备即满足要求

**预期结果：**

测试结果PASS，无异常

---

##### 4.2.17 PMU ADC

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 1、打开如下配置：
EXAMPLES_ADC=y
EXAMPLES_ADC_DEVPATH (根据实际设备名配置，默认/dev/adc0)
EXAMPLES_ADC_NSAMPLES （根据实际测试需求填写，默认0）
2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 adc -p "devpath" -n 20
注：
1）devpath根据实际的adc设备名称填写，比如/dev/adc0
2）测试时需要向adc设备对应的管脚上输入一个稳定电压，测试时GND线也要连接。

**预期结果：**

可以读取到预期的电压值

---

##### 4.2.16 Audio

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_TESTING_DRIVER_TEST_STACKSIZE=8192
CONFIG_AUDIO=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 cmocka_driver_audio
2、等待执行结果

**预期结果：**

测试结果PASS，无异常

---

##### 4.2.15 Audio_DSP--Looper_cmoka

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 文件系统, 测试码流
声道, 采样深度, 采样率尽可能覆盖


**步骤：**

1、在nsh中输入 cmocka_driver_audio -a 3 -p /data/1000.pcm
注：
1）cmocka_driver_audio需要两个必填参数：
-a：1表示只采集，2表示只播放，3表示先采集再播放
-p：文件名，如 -p /data/1.pcm
2）默认音频设备为/dev/audio/pcm0p, /dev/audio/pcm0c，使用 -i 更改录制音频设备，如 -i /dev/audio/pcm1c；使用 -i 更改播放音频设备。例如 -i /dev/audio/pcm1p。
3）默认格式是AUDIO_FMT_PCM 使用-f改变格式，如 -f mp3
4）默认采样率为 44100，通道为 2，bps 为 16：使用 -s 更改采样率；使用 -c 改变频道；使用 -b 更改 bps。
5）默认记录时间为10s。使用-t 来改变

**预期结果：**

播放正常

---

##### 4.2.14 Audio_DSP--Looper_nxlooper

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 文件系统, 测试码流
声道,  采样深度,  采样率尽可能覆盖


**步骤：**

nxlooper
device pcm0p
device pcm13c
loopback 2 16 48000

**预期结果：**

回环正常

---

##### 4.2.13 Audio_DSP--Capture_cmoka_3channels

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 文件系统, 测试码流
声道,  采样深度,  采样率尽可能覆盖


**步骤：**

1、在nsh中输入 cmocka_driver_audio -a 1 -p /data/1000.pcm -s 48000 -c 3 -b 32 -i /dev/audio/pcm13c
注：
1）cmocka_driver_audio需要两个必填参数：
-a：1表示只采集，2表示只播放，3表示先采集再播放
-p：文件名，如 -p /data/1.pcm
2）默认音频设备为/dev/audio/pcm0p, /dev/audio/pcm0c，使用 -i 更改录制音频设备，如 -i /dev/audio/pcm1c；使用 -i 更改播放音频设备。例如 -i /dev/audio/pcm1p。
3）默认格式是AUDIO_FMT_PCM 使用-f改变格式，如 -f mp3
4）默认采样率为 44100，通道为 2，bps 为 16：使用 -s 更改采样率；使用 -c 改变频道；使用 -b 更改 bps。
5）默认记录时间为10s。使用-t 来改变

**预期结果：**

录音文件声音正常

---

##### 4.2.13 Audio_DSP--Capture_cmoka_1channels

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 文件系统, 测试码流
声道,  采样深度,  采样率尽可能覆盖


**步骤：**

1、在nsh中输入 cmocka_driver_audio -a 1 -p /data/1000.pcm -s 16000 -c 1 -b 16
注：
1）cmocka_driver_audio需要两个必填参数：
-a：1表示只采集，2表示只播放，3表示先采集再播放
-p：文件名，如 -p /data/1.pcm
2）默认音频设备为/dev/audio/pcm0p, /dev/audio/pcm0c，使用 -i 更改录制音频设备，如 -i /dev/audio/pcm1c；使用 -i 更改播放音频设备。例如 -i /dev/audio/pcm1p。
3）默认格式是AUDIO_FMT_PCM 使用-f改变格式，如 -f mp3
4）默认采样率为 44100，通道为 2，bps 为 16：使用 -s 更改采样率；使用 -c 改变频道；使用 -b 更改 bps。
5）默认记录时间为10s。使用-t 来改变

**预期结果：**

录音文件声音正常

---

##### 4.2.12 Audio_DSP--Capture_cmoka_2channels

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 文件系统, 测试码流
声道,  采样深度,  采样率尽可能覆盖


**步骤：**

1、在nsh中输入 cmocka_driver_audio -a 1 -p /data/1000.pcm (2channels, 44100, 16bits)
注：
1）cmocka_driver_audio需要两个必填参数：
-a：1表示只采集，2表示只播放，3表示先采集再播放
-p：文件名，如 -p /data/1.pcm
2）默认音频设备为/dev/audio/pcm0p, /dev/audio/pcm0c，使用 -i 更改录制音频设备，如 -i /dev/audio/pcm1c；使用 -i 更改播放音频设备。例如 -i /dev/audio/pcm1p。
3）默认格式是AUDIO_FMT_PCM 使用-f改变格式，如 -f mp3
4）默认采样率为 44100，通道为 2，bps 为 16：使用 -s 更改采样率；使用 -c 改变频道；使用 -b 更改 bps。
5）默认记录时间为10s。使用-t 来改变

**预期结果：**

录音文件声音正常

---

##### 4.2.11 Audio_DSP--Capture_nxrecorder

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 文件系统, 测试码流
声道,  采样深度,  采样率尽可能覆盖


**步骤：**

nxrecorder
device pcm13c
recordraw /tmp/d_3ch_32bit_48000.pcm 3 32 48000
stop

**预期结果：**

录音文件声音正常

---

##### 4.2.10 Audio_DSP--Playback_cmoka_1channels

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.2 驱动BSP

**前提条件：** 文件系统, 测试码流
声道,  采样深度,  采样率尽可能覆盖


**步骤：**

1、在nsh中输入 cmocka_driver_audio -a 2 -p /data/1000.pcm -s 16000 -c 1 -b 16
注：
1）cmocka_driver_audio需要两个必填参数：
-a：1表示只采集，2表示只播放，3表示先采集再播放
-p：文件名，如 -p /data/1.pcm
2）默认音频设备为/dev/audio/pcm0p, /dev/audio/pcm0c，使用 -i 更改录制音频设备，如 -i /dev/audio/pcm1c；使用 -i 更改播放音频设备。例如 -i /dev/audio/pcm1p。
3）默认格式是AUDIO_FMT_PCM 使用-f改变格式，如 -f mp3
4）默认采样率为 44100，通道为 2，bps 为 16：使用 -s 更改采样率；使用 -c 改变频道；使用 -b 更改 bps。
5）默认记录时间为10s。使用-t 来改变

**预期结果：**

声音正常

---

#### 系统应用

##### 4.1.6 文件系统异常场景--掉电重启时磁盘空间变化

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 power_off_test03 <DIR>
2、执行一段时间，将设备直接断电
3、恢复设备供电，等设备起来后在nsh中输入 power_off_test03 <DIR>
4、重复步骤2-3 3次，观察测试结果
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

4、输出TEST PASSED

---

##### 4.1.57 WiFi--wapi CountryCode的设置和获取

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、执行:
ifup wlan0
wapi country wlan0
wapi country wlan0 US
wapi country wlan0
wapi country wlan0 CN
wapi country wlan0

**预期结果：**

2、执行成功无报错，可正确设置和获取country code:

---

##### 4.1.56 WiFi--设备连接至双频合一的网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电
2、路由器无线AP配置为双频合一模式

**步骤：**

1、设备进入到NuttX shell；
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip (注：router_ip为路由器网关IP)

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.55 WiFi--无线模式支持802.11b/g/n/ax混合

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电
2、可选用TP-Link路由器

**步骤：**

1、设备待连接的路由器的无线模式设置为802.11b/g/n/ax混合模式
2、设备通过wapi连接该路由器ap
3、查看设备是否可以正常连接，且系统无异常

**预期结果：**

3、设备可以正常连接该无线ap，且系统无异常

---

##### 4.1.54 WiFi--无线模式支持802.11b/g/n混合

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电
2、可选用TP-Link路由器

**步骤：**

1、设备待连接的路由器的无线模式设置为802.11b/g/n混合模式
2、设备通过wapi连接该路由器ap
3、查看设备是否可以正常连接，且系统无异常

**预期结果：**

3、设备可以正常连接该无线ap，且系统无异常

---

##### 4.1.53 WiFi--无线模式支持802.11b/g混合

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电
2、可选用TP-Link路由器

**步骤：**

1、设备待连接的路由器的无线模式设置为802.11b/g混合模式
2、设备通过wapi连接该路由器ap
3、查看设备是否可以正常连接，且系统无异常

**预期结果：**

3、设备可以正常连接该无线ap，且系统无异常

---

##### 4.1.52 WiFi--无线模式支持802.11n only

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电
2、可选用TP-Link路由器

**步骤：**

1、设备待连接的路由器的无线模式设置为802.11n模式
2、设备通过wapi连接该路由器ap
3、查看设备是否可以正常连接，且系统无异常

**预期结果：**

3、设备可以正常连接该无线ap，且系统无异常

---

##### 4.1.51 WiFi--无线模式支持802.11g only

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电
2、可选用TP-Link路由器

**步骤：**

1、设备待连接的路由器的无线模式设置为802.11g模式
2、设备通过wapi连接该路由器ap
3、查看设备是否可以正常连接，且系统无异常

**预期结果：**

3、设备可以正常连接该无线ap，且系统无异常

---

##### 4.1.50 WiFi--5G--5G网络全信道扫描测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、将待测设备旁边放置一个无线AP的essid为'A'，并设置该ap在149信道
2、进入设备串口执行：
ifup wlan0
wapi scan wlan0
3、查看待测设备的扫描列表中是否存在essid为'A'的无线ap
4、重复步骤1，依次设置该无线ap的信道为153、157、161、165
5、重复步骤2-3

**预期结果：**

5、依次设置待测设备旁边的无线ap遍历5G无线信道，待测设备的扫描列表中始终可以扫描到该无线ap，即待测设备的扫描列表中始终存在essid为'A'的无线ap 。

---

##### 4.1.5 文件系统异常场景--创建文件时掉电

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 power_off_test02 <DIR>
2、执行一段时间，将设备直接断电
3、恢复设备供电，等设备起来后在nsh中输入 power_off_test02 <DIR>
4、重复步骤2-3 3次，观察测试结果
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

4、输出Poweroff test open api passed

---

##### 4.1.49 WiFi--5G--wapi disconncet后与外网不通

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig,查看wlan0的ip
4、ping <外网ip地址> ，如www.baidu.com
5、执行wapi disconnect wlan0
6、ping <外网ip地址> ，如www.baidu.com

**预期结果：**

2、设备配网成功；
3、可查看到IP地址，该IP地址为路由器分配的ip；
4、ping通百度，系统无异常
5、执行成功；
6、ping不通，系统无异常

---

##### 4.1.48 WiFi--5G--wapi reconncet

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、进入到NuttX shell；
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig，查看wlan0接口IP地址是否为essid为<路由器SSID>路由器获取IP地址
4、执行wapi save_config wlan0
5、执行wapi reconnect wlan0；
6、执行renew wlan0
7、再次执行步骤3
8、执行ping router_ip (注：router_ip为路由器网关IP)

**预期结果：**

2、设备配网成功;
3、wlan0地址为essid为<路由器SSID>路由器分配的地址
5、执行成功，无报错；
7、 wlan0地址为essid为<路由器SSID>路由器分配的地址
8、可以ping通路由器IP

---

##### 4.1.47 WiFi--5G--wapi config保存后设备reboot再reconnect

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi save_config wlan0；
4、 执行reboot；
5、执行 ifup wlan0
6、执行wapi reconnect wlan0
7、执行renew wlan0
8、执行ping router_ip (注：router_ip为路由器网关IP)

**预期结果：**

1-7、执行成功无报错；
8、设备重新配网成功，可以ping通路由器IP

---

##### 4.1.46 WiFi--5G--wapi config保存正常

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi save_config wlan0；
4、执行cat /data/etc/wapi.conf，查看成功保存的config信息是否准确，有无乱码显示异常
注：不同设备保存wapi.conf的路劲不一，以实际为准

**预期结果：**

2-3、执行成功无报错，设备成功配网
4、可查看成功保存的wapi.conf，信息准确，无乱码显示异常

---

##### 4.1.45 WiFi--5G--遍历5G无线信道连接

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，设备与路由器距离在2米之内，且位置保持不变

**步骤：**

1、进入设备NuttX shell
2、设置设备将要连接的路由器的信道为149信道，并对设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、查看串口log，连接是否成功，执行ping router_ip (注：router_ip为路由器网关IP)
4、重复步骤2-3，遍历路由器信道149,153,157,161,165

**预期结果：**

3、设备连接成功，无报错,且可以ping通路由器IP
4、设备可以成功连接5G网络所有信道

---

##### 4.1.44 WiFi--5G--Wapi Show获取5G AP的无线参数

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi show wlan0

**预期结果：**

1-2、执行成功无报错，可查看wlan0接口信息，包括：IP、 NetMask、Frequency、Flag、Channel、Frequency、ESSID等

---

##### 4.1.43 WiFi--5G--Wapi Sense获取链接5G AP的RSSI

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi sense wlan0
4、再执行步骤3，查看返回结果是否有变化

**预期结果：**

3、执行成功无报错，返回rssi信息
4、两次返回结果会动态变化

---

##### 4.1.42 WiFi--5G--Wapi连接为WPA3加密方式时加入5G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，5G网络无线AP设置加密方式为WPA3模式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <路由器密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.41 WiFi--5G--Wapi连接为WPA2/WPA3混合加密方式时加入5G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，5G网络无线AP设置为WPA2/WPA3混合加密方式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip (注：router_ip为路由器网关IP)

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.40 WiFi--5G--Wapi连接为WPA/WPA2混合加密方式时加入5G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，5G网络无线AP设置为WPA/WPA2混合加密方式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip (注：router_ip为路由器网关IP)

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.4 文件系统异常场景--写入时掉电

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTS_TESTCASES=y
CONFIG_TESTING_TESTCASES_STACKSIZE=8192
CONFIG_FS_TEST=y
CONFIG_FS_TEST_STRESS=y
CONFIG_FS_TEST_STABILITY=y
CONFIG_FS_TEST_POWEROFF=y
CONFIG_ARCH_SETJMP_H=y
CONFIG_PSEUDOFS_SOFTLINKS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 power_off_test01 <DIR>
2、执行一段时间，将设备直接断电
3、恢复设备供电，等设备起来后在nsh中输入 power_off_test01 <DIR>
4、重复步骤2-3 3次，观察测试结果
注：DIR为需要测试的文件系统挂载的目录，可通过df -h来查看，例如/data（默认）， /sdcard， /sst，rpmsgfs(一般非主核挂载)

**预期结果：**

4、输出TEST PASSED

---

##### 4.1.39 WiFi--5G--Wapi连接为WPA2加密方式时加入5G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，5G网络无线AP设置加密方式为WPA2模式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <路由器密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.38 WiFi--5G--Wapi连接为WPA加密方式时加入5G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，5G网络无线AP设置加密方式为WPA模式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <路由器密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.37 WiFi--5G--Wapi连接为[SharedKey]WEP_128bits-ASCII加密方式时加入5G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，5G网络无线AP设置加密方式为[Shared Key]WEP_64bits-ASCII加密方式，即Type=Shared Key(共享密钥)、Key Format=Hexadecimal(十六进制)、Key 2选择64 bits
注：路由器需支持WEP加密模式，如华硕RT-AX82U系列路由器等

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi scan wlan0
wapi scan wlan0 <该路由器essid>
wapi mode wlan0 2
wapi psk wlan0 <该路由器密码> 1
wapi essid wlan0 <该路由器essid> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.36 WiFi--5G--Wapi连接为[SharedKey]WEP_64bits-ASCII加密方式时加入5G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，5G网络无线AP设置加密方式为[Shared Key]WEP_64bits-ASCII加密方式，即Type=Shared Key(共享密钥)、Key Format=Hexadecimal(十六进制)、Key 2选择64 bits
注：路由器需支持WEP加密模式，如华硕RT-AX82U系列路由器等

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi scan wlan0
wapi scan wlan0 <该路由器essid>
wapi mode wlan0 2
wapi psk wlan0 <该路由器密码> 1
wapi essid wlan0 <该路由器essid> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.35 WiFi--5G--Wapi连接为[OpenSystem]WEP_128bits-ASCII加密方式时加入5G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，5G网络无线AP设置加密方式为[OpenSystem]WEP_128bits-ASCII加密方式，即Type=OpenSystem(开放系统)、Key Format=Hexadecimal(十六进制)、Key 2选择128 bits
注：路由器需支持WEP加密模式，如华硕RT-AX82U系列路由器等

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi scan wlan0
wapi scan wlan0 <该路由器essid>
wapi mode wlan0 2
wapi psk wlan0 <该路由器密码> 1
wapi essid wlan0 <该路由器essid> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.34 WiFi--5G--Wapi连接为[OpenSystem]WEP_64bits-ASCII加密方式时加入5G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，5G网络无线AP设置加密方式为[OpenSystem]WEP_64bits-ASCII加密方式，即Type=OpenSystem(开放系统)、Key Format=Hexadecimal(十六进制)、Key 2选择64 bits
注：路由器需支持WEP加密模式，如华硕RT-AX82U系列路由器等

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi scan wlan0
wapi scan wlan0 <该路由器essid>
wapi mode wlan0 2
wapi psk wlan0 <该路由器密码> 1
wapi essid wlan0 <该路由器essid> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.32 WiFi--2.4G--2.4G网络全信道扫描测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、将待测设备旁边放置一个无线AP的essid为'A'，并设置该ap在1信道
2、进入设备串口执行：
ifup wlan0
wapi scan wlan0
3、查看待测设备的扫描列表中是否存在essid为'A'的无线ap
4、重复步骤1，依次设置该无线ap的信道为2、3、4、5、6、7、8、9、10、11、12、13
5、重复步骤2-3

**预期结果：**

5、依次设置待测设备旁边的无线ap遍历2.4G无线信道，待测设备的扫描列表中始终可以扫描到该无线ap，即待测设备的扫描列表中始终存在essid为'A'的无线ap 。

---

##### 4.1.31 WiFi--2.4G--wapi disconncet后与外网不通

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看wlan0的ip;
4、ping <外网ip地址> ，如www.baidu.com
5、执行wapi disconnect wlan0
6、ping <外网ip地址> ，如www.baidu.com

**预期结果：**

2、设备配网成功；
3、可查看到IP地址，该IP地址为路由器分配的ip；
4、执行成功；
5、ping不通，系统无异常

---

##### 4.1.30 WiFi--2.4G--wapi reconncet

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、进入到NuttX shell；
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig，查看wlan0接口IP地址是否为essid为<路由器SSID>路由器获取IP地址
4、执行wapi save_config wlan0
5、执行wapi reconnect wlan0；
6、执行renew wlan0
7、再次执行步骤3
8、执行ping router_ip (注：router_ip为路由器网关IP)

**预期结果：**

2、设备配网成功;
3、wlan0地址为essid为<路由器SSID>路由器分配的地址
5、执行成功，无报错；
7、 wlan0地址为essid为<路由器SSID>路由器分配的地址
8、可以ping通路由器IP

---

##### 4.1.3 fatutf8文件系统编码能力测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_FATUTF8=y
CONFIG_TESTING_FATUTF8_STACKSIZE=3072
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入fatutf8 测试路径，如fatutf8 /data
2、等待执行结果

**预期结果：**

removed testdir

---

##### 4.1.29 WiFi--2.4G--wapi config保存后设备reboot再reconnect

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi save_config wlan0；
4、 执行reboot；
5、执行 ifup wlan0
6、执行wapi reconnect wlan0
7、执行renew wlan0
8、执行ping router_ip (注：router_ip为路由器网关IP)

**预期结果：**

1-7、执行成功无报错；
8、设备重新配网成功，可以ping通路由器IP

---

##### 4.1.28 WiFi--2.4G--wapi config保存正常

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi save_config wlan0；
4、执行cat /data/etc/wapi.conf，查看成功保存的config信息是否准确，有无乱码显示异常
注：不同设备保存wapi.conf的路劲不一，以实际为准

**预期结果：**

2-3、执行成功无报错，设备成功配网
4、可查看成功保存的wapi.conf，信息准确，无乱码显示异常

---

##### 4.1.27 WiFi--2.4G--遍历2.4G无线信道连接

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，设备与路由器距离在2米之内，且位置保持不变

**步骤：**

1、进入设备NuttX shell
2、设置设备将要连接的路由器的信道为1信道，并对设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、查看串口log，连接是否成功，执行ping router_ip (注：router_ip为路由器网关IP)
4、重复步骤2-3，遍历路由器信道1-13 （设备配网后需要重启再进行配网连接）

**预期结果：**

3、设备连接成功，无报错,且可以ping通路由器IP
4、设备可以成功连接2.4G网络所有信道

---

##### 4.1.26 WiFi--2.4G--Wapi Show获取2.4G AP的无线参数

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi show wlan0

**预期结果：**

1-2、执行成功无报错，可查看wlan0接口信息，包括：IP、 NetMask、Frequency、Flag、Channel、Frequency、ESSID等

---

##### 4.1.25 WiFi--2.4G--Wapi Sense获取链接2.4G AP的RSSI

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi sense wlan0
4、再执行步骤3，查看返回结果是否有变化

**预期结果：**

3、执行成功无报错，返回rssi信息
4、两次返回结果会动态变化

---

##### 4.1.24 WiFi--2.4G--Wapi连接为WPA3加密方式时加入2.4G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，2.4G网络无线AP设置加密方式为WPA3模式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <路由器密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.23 WiFi--2.4G--Wapi连接为WPA2/WPA3混合加密方式时加入2.4G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，2.4G网络无线AP设置为WPA2/WPA3混合加密方式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip (注：router_ip为路由器网关IP)

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.22 WiFi--2.4G--Wapi连接为WPA/WPA2混合加密方式时加入2.4G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，2.4G网络无线AP设置为WPA/WPA2混合加密方式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip (注：router_ip为路由器网关IP)

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.21 WiFi--2.4G--Wapi连接为WPA2加密方式时加入2.4G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，2.4G网络无线AP设置加密方式为WPA2模式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <路由器密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.20 WiFi--2.4G--Wapi连接为WPA加密方式时加入2.4G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，2.4G网络无线AP设置加密方式为WPA模式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <路由器密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.2 文件系统--romfs只读文件系统测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > 文件系统

**前提条件：**

1、打开如下配置：

```
CONFIG_EXAMPLES_ROMFS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 romfs
2、等待执行结果

**预期结果：**

2、测试完成后，nsh终端打印PASSED

---

##### 4.1.19 WiFi--2.4G--Wapi连接为[SharedKey]WEP_128bits-ASCII加密方式时加入2.4G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，2.4G网络无线AP设置加密方式为[Shared Key]WEP_64bits-ASCII加密方式，即Type=Shared Key(共享密钥)、Key Format=Hexadecimal(十六进制)、Key 2选择64 bits
注：路由器需支持WEP加密模式，如华硕RT-AX82U系列路由器等

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi scan wlan0
wapi scan wlan0 <该路由器essid>
wapi mode wlan0 2
wapi psk wlan0 <该路由器密码> 1
wapi essid wlan0 <该路由器essid> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.18 WiFi--2.4G--Wapi连接为[SharedKey]WEP_64bits-ASCII加密方式时加入2.4G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，2.4G网络无线AP设置加密方式为[Shared Key]WEP_64bits-ASCII加密方式，即Type=Shared Key(共享密钥)、Key Format=Hexadecimal(十六进制)、Key 2选择64 bits
注：路由器需支持WEP加密模式，如华硕RT-AX82U系列路由器等

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi scan wlan0
wapi scan wlan0 <该路由器essid>
wapi mode wlan0 2
wapi psk wlan0 <该路由器密码> 1
wapi essid wlan0 <该路由器essid> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.17 WiFi--2.4G--Wapi连接为[OpenSystem]WEP_128bits-ASCII加密方式时加入2.4G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，2.4G网络无线AP设置加密方式为[OpenSystem]WEP_128bits-ASCII加密方式，即Type=OpenSystem(开放系统)、Key Format=Hexadecimal(十六进制)、Key 2选择128 bits
注：路由器需支持WEP加密模式，如华硕RT-AX82U系列路由器等

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi scan wlan0
wapi scan wlan0 <该路由器essid>
wapi mode wlan0 2
wapi psk wlan0 <该路由器密码> 1
wapi essid wlan0 <该路由器essid> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.16 WiFi--2.4G--Wapi连接为[OpenSystem]WEP_64bits-ASCII加密方式时加入2.4G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，2.4G网络无线AP设置加密方式为[OpenSystem]WEP_64bits-ASCII加密方式，即Type=OpenSystem(开放系统)、Key Format=Hexadecimal(十六进制)、Key 2选择64 bits
注：路由器需支持WEP加密模式，如华硕RT-AX82U系列路由器等

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi scan wlan0
wapi scan wlan0 <该路由器essid>
wapi mode wlan0 2
wapi psk wlan0 <该路由器密码> 1
wapi essid wlan0 <该路由器essid> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.15 WiFi--2.4G--Wapi连接为Open加密方式时加入2.4G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，2.4G网络无线AP设置加密方式为Open模式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行ifconfig；
4、执行ping router_ip（注：router_ip为路由器IP）

**预期结果：**

1-2、执行成功无报错，设备成功配网；
3、设备分配到ip地址；
4、可以ping通路由器IP，且无异常报错

---

##### 4.1.148 全包升级--升级install过程中断电

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > OTA

**前提条件：** 1.设备供电正常
2.设备软硬件版本支持ymodem或Wi-Fi或adb push工具下载ota包到待测设备内

**步骤：**

1.使用相关工具将差分升级包传输到设备的/data目录下，并修改升级包名称为‘ota.zip’；
备注：
工具使用参照ymodem：
adb : adb push <本地ota包> /data
Wi-Fi:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
curl -o /data/ota.zip <服务器链接地址>/<ota包>
2. 进入设备shell，执行reboot recovery进入到recovery模式，在全包升级install过程中任意时间点（需要覆盖install所有bin文件过程中断电）设备断电，反复上下电20次，查看设备串口log，系统是否有异常卡住、crash等现象

**预期结果：**

2. reboot recovery进入到recovery模式，在全包升级install过程中任意时间点，设备断电，反复上下电20次，查看设备串口log，系统无异常卡住、crash等现象

---

##### 4.1.147 全包升级--bl2中boot /ota/vela_ota.bin过程中断电

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > OTA

**前提条件：** 1.设备供电正常
2.设备软硬件版本支持ymodem或Wi-Fi或adb push工具下载ota包到待测设备内

**步骤：**

1.使用相关工具将差分升级包传输到设备的/data目录下，并修改升级包名称为‘ota.zip’；
备注：
工具使用参照ymodem：
adb : adb push <本地ota包> /data
Wi-Fi:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
curl -o /data/ota.zip <服务器链接地址>/<ota包>
2.执行reboot recovery，查看设备串口log启动到bl2中出现关键字“boot /ota/vela_ota.bin”前、后、及出现时，设备断电，反复上下电20次，查看设备串口log，系统是否有异常卡住、crash等现象
3. ls -l /data/ota.zip 查看ota.zip文件是否还存在

**预期结果：**

2.查看设备串口log启动到bl2中出现关键字“boot /ota/vela_ota.bin”前、后、及出现时，设备断电，反复上下电20次，查看设备串口log，系统无异常卡住、crash等现象
3.升级包未删除

---

##### 4.1.146 全包升级--bl2中zip_verify ota.zip过程中断电

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > OTA

**前提条件：** 1.设备供电正常
2.设备软硬件版本支持ymodem或Wi-Fi或adb push工具下载ota包到待测设备内

**步骤：**

1.使用相关工具将差分升级包传输到设备的/data目录下，并修改升级包名称为‘ota.zip’；
备注：
工具使用参照ymodem：
adb : adb push <本地ota包> /data
Wi-Fi:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
curl -o /data/ota.zip <服务器链接地址>/<ota包>
2. 执行reboot recovery，查看设备串口log启动到bl2中进行zip_verify ota.zip过程中，设备断电，反复上下电20次，查看设备串口log，系统是否有异常卡住、crash等现象
3. ls -l /data/ota.zip 查看ota.zip文件是否还存在

**预期结果：**

2.查看设备串口log启动到bl2中进行zip_verify ota.zip过程中，设备断电，反复上下电20次，查看设备串口log，系统无异常卡住、crash等现象
3.升级包未删除

---

##### 4.1.14 WiFi--STA模式--反复连接/断开iOS手机热点

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，iOS手机开启热点模式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <iOS手机热点密码> 3
wapi essid wlan0 <iOS手机热点名称> 1
renew wlan0 ；
3、wapi disconnect wlan0
4、wapi mode wlan0 2
wapi psk wlan0 <iOS手机热点密码> 3
wapi essid wlan0 <iOS手机热点名称> 1
renew wlan0 ；
5、重复步骤3-4步骤10次；
6、查看设备log,设备是否可以成功断开和连接到iOS手机热点，无异常报错

**预期结果：**

6、设备可以成功断开和连接IOS手机热点，无异常报错

---

##### 4.1.133 Video H265 解码播放

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Vedio

**前提条件：**

1.打开如下配置

```
CONFIG_MEDIA=y
CONFIG_MEDIA_TOOL=y
```

2.下载测试资源文件，见附件。
注：若芯片不支持media_tool，则无需测试 

**步骤：**

1.将测试文件“media_file_h265.mp4”上传至开发板中（比如存放在/data/media_file_h265.mp4）
2.执行mediatool 进入测试工具命令shell窗口
3.在"mediatool>"下依次执行如下命令：
3.1）open Video
3.2）prepare 0 url /data/media_file_h265.mp4
3.3）start 0
4.关闭播放 执行 close 0
5.退出mediatool工具命令界面输入 q 回车

**预期结果：**

3.3)视频播放正常；视频中的声音输出正常；无黑屏现象；无crash现象；

---

##### 4.1.132 Video H264 解码播放

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Vedio

**前提条件：**

2.打开如下配置

```
CONFIG_MEDIA=y
CONFIG_MEDIA_TOOL=y
```

2.下载测试资源文件，见附件。
注：若芯片不支持media_tool，则无需测试 

**步骤：**

1.将测试文件“media_file_h264.mp4”上传至开发板中（比如存放在/data/media_file_h264.mp4）
2.执行mediatool 进入测试工具命令shell窗口
3.在"mediatool>"下依次执行如下命令：
3.1）open Video
3.2）prepare 0 url /data/media_file_h264.mp4
3.3）start 0
4.关闭播放 执行 close 0
5.退出mediatool工具命令界面输入 q 回车

**预期结果：**

3.3)视频播放正常；视频中的声音输出正常；无黑屏现象；无crash现象；

---

##### 4.1.131 Audio wav 解码播放

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Audio

**前提条件：**

3.打开如下配置

```
CONFIG_MEDIA=y
CONFIG_MEDIA_TOOL=y
```

2.下载测试资源文件，见附件。
注：若芯片不支持media_tool，则无需测试 

**步骤：**

1.将测试文件“audio_file.wav”上传至开发板中（比如存放在/data/audio_file.wav）
2.执行mediatool 进入测试工具命令shell窗口
3.在"mediatool>"下依次执行如下命令：
3.1）open Music
3.2）prepare 0 url /data/audio_file.wav
3.3）start 0
4.关闭播放 执行 close 0
5.退出mediatool工具命令界面输入 q 回车

**预期结果：**

3.3)音乐播放正常无卡顿；无crash现象

---

##### 4.1.130 Audio aac 解码播放

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Audio

**前提条件：**

4.打开如下配置

```
CONFIG_MEDIA=y
CONFIG_MEDIA_TOOL=y
```

2.下载测试资源文件，见附件。
注：若芯片不支持media_tool，则无需测试 

**步骤：**

1.将测试文件“audio_file.aac”上传至开发板中（比如存放在/data/audio_file.aac）
2.执行mediatool 进入测试工具命令shell窗口
3.在"mediatool>"下依次执行如下命令：
3.1）open Music
3.2）prepare 0 url /data/audio_file.aac
3.3）start 0
4.关闭播放 执行 close 0
5.退出mediatool工具命令界面输入 q 回车

**预期结果：**

3.3)音乐播放正常无卡顿；无crash现象

---

##### 4.1.13 WiFi--STA模式--反复连接/断开安卓手机热点

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电，Android手机开启热点模式

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <安卓手机热点密码> 3
wapi essid wlan0 <安卓手机热点名称> 1
renew wlan0 ；
3、wapi disconnect wlan0
4、wapi mode wlan0 2
wapi psk wlan0 <安卓手机热点密码> 3
wapi essid wlan0 <安卓手机热点名称> 1
renew wlan0 ；
5、重复步骤3-4步骤10次；
6、查看设备log,设备是否可以成功断开和连接到安卓手机热点，无异常报错

**预期结果：**

6、设备可以成功断开和连接安卓手机热点，无异常报错

---

##### 4.1.129 Audio opus 解码播放

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Audio

**前提条件：**

1.打开如下配置

```
CONFIG_MEDIA=y
CONFIG_MEDIA_TOOL=y
```

2.下载测试资源文件，见附件。
注：若芯片不支持media_tool，则无需测试 

**步骤：**

1.将测试文件“audio_file.opus”上传至开发板中（比如存放在/data/audio_file.opus）
2.执行mediatool 进入测试工具命令shell窗口
3.在"mediatool>"下依次执行如下命令：
3.1）open Music
3.2）prepare 0 url /data/audio_file.opus
3.3）start 0
4.关闭播放 执行 close 0
5.退出mediatool工具命令界面输入 q 回车

**预期结果：**

3.3)音乐播放正常无卡顿；无crash现象

---

##### 4.1.128 Audio mp3 解码播放

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Audio

**前提条件：**

1.打开如下配置

```
CONFIG_MEDIA=y
CONFIG_MEDIA_TOOL=y
```

2.下载测试资源文件，见附件。
注：若芯片不支持media_tool，则无需测试 

**步骤：**

1.将测试文件“audio_file.mp3”上传至开发板中（比如存放在/data/audio_file.mp3）
2.执行mediatool 进入测试工具命令shell窗口
3.在"mediatool>"下依次执行如下命令：
3.1）open Music
3.2）prepare 0 url /data/audio_file.mp3
3.3）start 0
4.关闭播放 执行 close 0
5.退出mediatool工具命令界面输入 q 回车

**预期结果：**

3.3)音乐播放正常无卡顿；无crash现象

---

##### 4.1.127 Audio--nxlooper回环功能测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Audio

**前提条件：**

1、打开如下配置：

```
CONFIG_SYSTEM_NXRECORDER=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中执行如下命令：
nxlooper
device pcm0p
device pcm13c
loopback 2 16 48000
stop
q

**预期结果：**

1、进入nxlooper后执行命令无报错

---

##### 4.1.126 Audio-- nxplayer播放功能测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Audio

**前提条件：**

1、打开如下配置：

```
CONFIG_SYSTEM_NXPLAYER=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中执行如下命令：
nxplayer
device /dev/audio/pcm0p
playraw /data/1.pcm 1 16 48000
2、播放完毕，输入q

**预期结果：**

1、进入nxplayer无报错，开始播放后语速及声音正常
2、退出nxplayer

---

##### 4.1.125 Audio--nxrecorder录音功能测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Audio

**前提条件：**

1、打开如下配置：

```
CONFIG_SYSTEM_NXRECORDER=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中执行如下命令：
nxrecorder
device /dev/audio/pcm13c
recordraw /tmp/1.pcm 3 32 48000
2、然后开始说话，说话完毕输入stop
3、q

**预期结果：**

1、进入nxrecorder无报错
2、开始说话时显示codec_int_stream_start，输入stop后显示codec_hw_stop
3、退出nxrecorder
4、adb pull /tmp/1.pcm 对pull出来的1.pcm播放，听声音是否正常

---

##### 4.1.124 GUI--lvgldemo widget组建基本功能测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > GUI

**前提条件：**

1、打开如下配置：

```
CONFIG_EXAMPLES_LVGLDEMO=y
CONFIG_LV_USE_DEMO_WIDGETS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口
参考文档

**步骤：**

1、在nsh中输入 lvgldemo widgets

**预期结果：**

能正常跑完lvgl的测试程序

---

##### 4.1.123 GUI--lvgldemo压力测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > GUI

**前提条件：**

1、打开如下配置：

```
CONFIG_EXAMPLES_LVGLDEMO=y
CONFIG_LV_USE_DEMO_STRESS=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 lvgldemo stress

**预期结果：**

能正常跑完lvgl的测试程序

---

##### 4.1.122 GUI--lvgldemo music基本功能测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > GUI

**前提条件：**

1、打开如下配置：

```
CONFIG_LV_USE_DEMO_MUSIC=y
CONFIG_LV_DEMO_MUSIC_AUTO_PLAY=y
CONFIG_LV_DEMO_MUSIC_LANDSCAPE=y
CONFIG_LV_DEMO_MUSIC_LARGE=y
CONFIG_LV_DEMO_MUSIC_ROUND=y
CONFIG_LV_DEMO_MUSIC_SQUARE=y
CONFIG_LV_FONT_MONTSERRAT_16
CONFIG_LV_FONT_MONTSERRAT_22
CONFIG_LV_FONT_MONTSERRAT_32
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 lvgldemo music

**预期结果：**

能正常跑完lvgl的测试程序

---

##### 4.1.121 GUI--lvgldemo keypad屏上操作测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > GUI

**前提条件：**

1、打开如下配置：

```
CONFIG_EXAMPLES_LVGLDEMO=y
CONFIG_LV_USE_DEMO_KEYPAD_AND_ENCODER=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 lvgldemo keypad_encoder

**预期结果：**

能正常跑完lvgl的测试程序

---

##### 4.1.120 GUI--frame buffer功能测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > GUI

**前提条件：**

1、打开如下配置：CONFIG_EXAMPLES_FB=y
2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、在nsh中输入 fb

**预期结果：**

屏幕能正常显示由多个矩形嵌套的图形

---

##### 4.1.119 Sensor驱动框架测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Sensor

**前提条件：**

1、打开如下配置：

```
CONFIG_TESTING_CMOCKA=y
CONFIG_TESTING_DRIVER_TEST=y
CONFIG_SENSORS_BMI160=y
CONFIG_USENSOR=y
CONFIG_SENSORS=y
CONFIG_UORB=y
CONFIG_UORB_LISTENER=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、参考文档SPI_I2C附件，将BMI160传感器和板子连接起来
5、打开nsh窗口
6、准备执行uORB监听指令
注：
1）Sensor uORB框架的通路正常测试在“通用自测用例”的1.26 I2c/Spi功能测试中负责，只要通路正常，则无需遍历所有Sensor
2）本用例使用BMI160来压测Sensor订阅不同频率的不同topic是否正常，涉及到的传感器只有BMI160自带的陀螺仪和加速计

**步骤：**

1、在nsh输入：
uorb_listener -n 10 -r 25 “topiclist”
uorb_listener -n 10 -r 50 “topiclist”
uorb_listener -n 10 -r 100 “topiclist”
2、观察所有topic订阅是否正常
3、重复步骤1-2 10次，再次观察
注：
1）uorb_listener命令示例：uorb_listener -n 10 sensor_accel,sensor_baro
2）uorb_listener参数定义如下
uorb_listener -n 1 打印所有主题的当前信息快照。
uorb_listener -n num 以发布主题信息频率 ，打印所有主题的信息 直到 num 条信息为止。
uorb_listener -r 1 以 1hz 的频率 ，打印所有主题的信息。
uorb_listener -r x -n num 以 xhz 的频率打印所有主题的信息，直到 num 条信息为止
3）厂商或个人验收仅需重复10次，openvela社区验收需测试1000次

**预期结果：**

2、无crash，所有topic均订阅正常
3、10次操作均符合预期，无crash，所有topic均订阅正常
注：运行成功的示例
nsh> uorb_listener -n 20 -r 50 sensor_accel_uncal0
**/***
Object name:sensor_accel_uncal0, recieved:20
Total number of received Message:20/20

---

##### 4.1.117 NetApp--设备支持ftpd

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > NetApp

**前提条件：**

1、设备上电，且配网在线
2、打开如下配置文件：

```
CONFIG_EXAMPLES_FTPD=y
CONFIG_NETUTILS_FTPD=y
CONFIG_NET_TCPBACKLOG=y
```

3、打开上述配置后进行编译
4、烧录刚刚编译的bin包
5、打开nsh窗口

**步骤：**

1、设备端执行：ftpd_start -4 &
2、同一局域网对端设备PC执行：ftp <设备IP>
输入用户名：
password:
3、PC 端进入data目录
cd data
ls
1）get <设备data目录下的某个文件> <文件在pc上想要保存的名称>
2）put <pc 当前目录下某个文件> <文件在设备上想要保存的名称>
4、PC 执行quit 退出ftp

**预期结果：**

2、PC端可以正常登录设备的ftp；
3、传输文件正常，无报错，设备端log无异常；
1）设备上的文件通过get拉取到了pc上；
2）pc上的文件通过put传输到了设备中
4、PC正常退出，设备端串口log无异常

---

##### 4.1.116 NetApp--设备支持通过scp方式向其他终端传输本地文件

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > NetApp

**前提条件：**

1、设备上电，配网在线，且与对端PC在同一局域网
2、打开如下配置：

```
CONFIG_DEV_URANDOM=y
CONFIG_CRYPTO_MBEDTLS=y
CONFIG_LIB_SSH=y
CONFIG_UTILS_SSH=y
```

3、打开上述配置后进行编译
4、烧录刚刚编译的bin包
5、打开nsh窗口

**步骤：**

1、设备进入NuttX shell进行配网:
执行：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <热点名称> 1
renew wlan0
2、执行scp /data/<本地文件> <终端用户名@HostIP:文件所在绝对路径>
eg:scp /data/full_ota.zip <user>@<file_server_ip>:/home/sss/Downloads/
3、输入 yes, 回车, 回车, 输密码
eg:
scp /data/full_ota.zip <user>@<file_server_ip>:/home/sss/Downloads/
4、等待数据传输成功后，在终端上查看文件大小是否和设备上的本地的文件大小相同

**预期结果：**

1、设备配网成功
2-3、传输无报错
4、终端上的文件大小和设备上的本地的文件大小相同

---

##### 4.1.115 NetApp--设备支持通过scp方式从其他终端获取文件到本地

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > NetApp

**前提条件：**

1、设备上电，配网在线，且与对端PC在同一局域网
2、打开如下配置

```
CONFIG_DEV_URANDOM=y
CONFIG_CRYPTO_MBEDTLS=y
CONFIG_LIB_SSH=y
CONFIG_UTILS_SSH=y
```

3、打开上述配置后进行编译
4、烧录刚刚编译的bin包
5、打开nsh窗口

**步骤：**

1、设备进入NuttX shell进行配网:
执行：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <热点名称> 1
renew wlan0
2、执行scp <终端用户名@HostIP:文件所在绝对路径> /dev/data/
eg:scp <user>@<file_server_ip>:/home/sss/Downloads/M1.zip /dev/data/
3、输入yes，回车，回车，输密码
eg:
scp <user>@<file_server_ip>:/home/sss/Downloads/M1.zip /dev/data/
4、等待数据传输成功后，在设备上查看文件大小是否和终端上的文件大小相同

**预期结果：**

1、设备配网成功
2-3、传输无报错
4、终端上的文件大小和设备上的本地的文件大小相同

---

##### 开关BLE蓝牙

**测试目的：** 开关BLE蓝牙

**前提条件：** 切换到bt所在核： 1. bttool 

**步骤：**

1、测试设备执行enable
2、测试设备执行state
3、测试设备执行disable
4、测试设备执行state

**预期结果：**

1、命令执行成功，回调Adapter state changed: 2
2、命令执行成功，回调[bttool] Adapter State: 2
3、命令执行成功，回调Adapter state changed: 0
4、命令执行成功，回调[bttool] Adapter State: 0

---

##### adv start -i <interval>指定广告间隔

**测试目的：** 单路单入参广播

**前提条件：** 切换到bt所在核： 
1. bttool 
2. enable

**步骤：**

1.测试设备执行adv start -i 32 -n vela-adv-test -m legacy    （20ms）
2.打开手机nrf工具搜索ble广播
3. 测试设备执行adv stop -i <adv_id>
4.测试设备执行adv start -i 160 -n vela-adv-test -m legacy   （100ms）
5.打开手机nrf工具搜索ble广播
6. 测试设备执行adv stop -i <adv_id>
7.测试设备执行adv start -i 1600 -n vela-adv-test -m legacy  （1000ms）
8.打开手机nrf工具搜索ble广播
9. 测试设备执行adv stop -i <adv_id> 
10.测试设备执行adv start -i 16384 -n vela-adv-test -m legacy   （10240ms）
11.打开手机nrf工具搜索ble广播
12. 测试设备执行adv stop -h 0xf3e332e0 注：此处-i 1的参数根据步骤1中的回调信息handle填写 如回调信息：[bttool] on_advertising_start_cb, handle:0xf3e332e0, adv_id:1, status:0
(间隔越大，越难搜到, 如果扫描窗口刚好在别人广播间隔内则可能扫不到)

**预期结果：**

3.手机侧nrf能扫描到设备，点开“MORE”后可以看到工具界面的右侧“Adv. Internal”一栏显示的广播间隔时间设备可以对上，误差不超过5%
6.手机侧nrf能扫描到设备，点开“MORE”后可以看到工具界面的右侧“Adv. Internal”一栏显示的广播间隔时间设备可以对上，误差不超过5%
9.手机侧nrf能扫描到设备，点开“MORE”后可以看到工具界面的右侧“Adv. Internal”一栏显示的广播间隔时间设备可以对上，误差不超过5%
12.手机侧nrf能扫描到设备，点开“MORE”后可以看到工具界面的右侧“Adv. Internal”一栏显示的广播间隔时间设备可以对上，误差不超过5%

---

##### 相同public地址多路广播

**测试目的：** 多路广播无异常
（可以同时发两个相同广播地址，nRF APP上面可以搜到两个不同地址发出来的广播）

**前提条件：** 切换到bt所在核： 
1. bttool 
2. enable

**步骤：**

1.被测设备执行adv start -n yuy1 -m legacy和adv start -n yuy2 -m legacy
2.打开手机nrf工具搜索ble广播
3.测试设备执行adv stop -i <adv_id> 分别关闭不同的adv_id

**预期结果：**

1.回调正常[bttool] adv name: yuy1 
[bttool] Advertising handle:0x41948ce0
[bttool] on_advertising_start_cb, handle:0x41948ce0, adv_id:1, status:0
[bttool] adv name: yuy2 
[bttool] Advertising handle:0x41948590
[bttool] on_advertising_start_cb, handle:0x41948590, adv_id:2, status:0
2.手机侧nrf能够扫描到设备两个地址, (手机可以看到扫描到的名字在yuy1和yuy2之前来回切换)

---

##### 4.1.114 NetApp--curl网页能力测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > NetApp

**前提条件：**

1、打开如下配置：

```
CONFIG_LIB_ZLIB=y
CONFIG_CRYPTO_MBEDTLS=y
CONFIG_LIB_CURL=y
CONFIG_TOOLS_CURL=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlna0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <热点名称> 1
renew wlan0 ；
3、执行命令 curl www.baidu.com

**预期结果：**

2、设备配网成功
3、 网页内容打印到串口中

---

##### 4.1.113 NetApp--curl http文件下载测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > NetApp

**前提条件：**

1、打开如下配置：

```
CONFIG_LIB_ZLIB=y
CONFIG_CRYPTO_MBEDTLS=y
CONFIG_LIB_CURL=y
CONFIG_TOOLS_CURL=y
```

2、打开上述配置后进行编译
3、烧录刚刚编译的bin包
4、打开nsh窗口

**步骤：**

1、设备进入到NuttX shell 
2、设备配网：
ifup wlna0 
wapi mode wlan0 2 
wapi psk wlan0 <热点密码> 3 
wapi essid wlan0 <热点名称> 1 
renew wlan0 ；
3、执行命令 curl -o /data/*** http://<file_server_ip>/<path>（仅示例，网页下载链接可替换）
4、查看data目录下的文件大小

**预期结果：**

2、设备配网成功；
3、执行过程中无异常报错;
4、通过curl下载到设备data目录下的文件和网页服务器上文件大小一致

---

##### 4.1.11 KVDB测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > KVDB

**前提条件：**

打开

```
CONFIG_TESTS_TESTSUITES
CONFIG_CM_KVDB_TEST
CONFIG_TESTING_CMOCKA
```

**步骤：**

1. 执行cmocka_kv_test运行自动化测试全集

**预期结果：**

1. 输出TEST PASSED

---

##### 4.1.105 蓝牙--BLE&Wi-Fi共存（Zblue协议栈）-蓝牙扫描和wifi共存

**测试目的：** 测试低功耗蓝牙BLE与WiFi共存稳定性

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看wlan0的ip;
4、执行wapi disconnect wlan0；
5、ping <wlan0 接口IP地址>
6、再次配网
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID>1
renew wlan0 ；
7、执行ping router_ip (注：router_ip为路由器网关IP)
8、重复步骤3-7 100次

**预期结果：**

2、设备配网成功；
3、可查看到IP地址，该IP地址为路由器分配的ip
4、执行成功，无报错；
5、不可以ping通
6、再次配网成功无报错
7、可以ping通外网
8、重复100次全部成功无报错

---

##### 4.1.104 蓝牙--BLE&Wi-Fi共存（Zblue协议栈）-蓝牙广播和wifi共存

**测试目的：** 测试低功耗蓝牙BLE与WiFi共存稳定性

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi scan wlan0 <指定2.4G ssid>；
4、重复步骤3执行100次，查看返回结果是否有变化，串口log是否有扫描失败情况或扫描异常报错

**预期结果：**

1-3、执行成功无报错，可搜索到指定的2.4G SSID
4、返回结果不会产生变化，扫描列表无异常无报错

---

##### 4.1.1 文件系统基本功能测试

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > 文件系统

**前提条件：** 1、设备（上电状态）与PC均处于同一局域网

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看设备分配到的ip地址
4、设备端执行：iperf2 -c 【对端PC的ip地址】-i 1 -p 5002 -t 300
5、PC端执行：iperf -s -p 5002 -i 1

**预期结果：**

5、设备作为Client端，TCP下行速率符合标准
注：
1）需在测结果中标明【测试环境】【测试路由器】【iperf版本】
2）保留测试log

---

##### 1.33 WiFi--5G--Wapi连接为Open加密方式时加入5G网络

**测试目的：** 二、品类自测用例 > 4、功能测试 > 4.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与路由器、PC均处于屏蔽箱中

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看设备分配到的ip地址
4、PC端执行：ping 设备IP地址，持续十分钟（600秒）
5、查看PC端log，统计ping包时延

**预期结果：**

5、统计ping包时不低于2ms
注：请在测结果中标明【测试环境】【测试路由器】

---

### 2. 性能测试

##### 5.1.29 WiFi--2.4G网络---wapi反复disconnect 2.4G网络

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看wlan0的ip;
4、执行wapi disconnect wlan0；
5、ping <wlan0 接口IP地址>
6、再次配网
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID>1
renew wlan0 ；
7、执行ping router_ip (注：router_ip为路由器网关IP)
8、重复步骤3-7 100次

**预期结果：**

2、设备配网成功；
3、可查看到IP地址，该IP地址为路由器分配的ip
4、执行成功，无报错；
5、不可以ping通
6、再次配网成功无报错
7、可以ping通外网
8、重复100次全部成功无报错

---

##### 5.1.27 WiFi--2.4G网络---设备连接2.4G后wapi扫描指定2.4G AP

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备上电

**步骤：**

1、设备进入到NuttX shell；
2、设备配网:
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0
3、执行wapi scan wlan0 <指定2.4G ssid>；
4、重复步骤3执行100次，查看返回结果是否有变化，串口log是否有扫描失败情况或扫描异常报错

**预期结果：**

1-3、执行成功无报错，可搜索到指定的2.4G SSID
4、返回结果不会产生变化，扫描列表无异常无报错

---

##### 5.1.23 WiFi--2.4G网络---设备作为Client端时的TCP Tx平均速率

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与PC均处于同一局域网

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看设备分配到的ip地址
4、设备端执行：iperf2 -c 【对端PC的ip地址】-i 1 -p 5002 -t 300
5、PC端执行：iperf -s -p 5002 -i 1

**预期结果：**

5、设备作为Client端，TCP下行速率符合标准
注：
1）需在测结果中标明【测试环境】【测试路由器】【iperf版本】
2）保留测试log

---

##### 5.1..20 WiFi--2.4G网络---屏蔽箱环境ping包时延

**测试目的：** 二、品类自测用例 > 5、性能测试 > 5.1 系统应用 > Wi-Fi

**前提条件：** 1、设备（上电状态）与路由器、PC均处于屏蔽箱中

**步骤：**

1、设备进入到NuttX shell
2、设备配网：
ifup wlan0
wapi mode wlan0 2
wapi psk wlan0 <热点密码> 3
wapi essid wlan0 <路由器SSID> 1
renew wlan0 ；
3、执行ifconfig,查看设备分配到的ip地址
4、PC端执行：ping 设备IP地址，持续十分钟（600秒）
5、查看PC端log，统计ping包时延

**预期结果：**

5、统计ping包时不低于2ms
注：请在测结果中标明【测试环境】【测试路由器】

---

### 1. 功能测试

##### 相同random地址多路广播

**测试目的：** 多路广播无异常
（可以同时发两个相同广播地址，nRF APP上面可以搜到两个不同地址发出来的广播）

**前提条件：** 切换到bt所在核： 
1. bttool 
2. enable

**步骤：**

1.被测设备执行adv start -R random_id -n yuy3 -m legacy和adv start -R random_id -n yuy4 -m legacy
2.打开手机nrf工具搜索ble广播
3.测试设备执行adv stop -i <adv_id> 分别关闭不同的adv_id

**预期结果：**

1.回调正常[bttool] own address type: random_id
[bttool] adv name: yuy3 
[bttool] Advertising handle:0x419340e0
[bttool] on_advertising_start_cb, handle:0x419340e0, adv_id:1, status:0
[bttool] own address type: random_id
[bttool] adv name: yuy4 
[bttool] Advertising handle:0x41948290
[bttool] on_advertising_start_cb, handle:0x41948290, adv_id:2, status:0
2.手机侧nrf能够扫描到设备两个地址, 手机可以同时看到两个yuy3和yuy4)

---

##### 不同地址多路广播

**测试目的：** 多路广播无异常
（可以同时发两个广播，广播地址可以自己设置不同，一个设public地址广播，一个random地址广播，nRF APP上面可以搜到两个不同地址发出来的广播）

**前提条件：** 切换到bt所在核： 
1. bttool 
2. enable

**步骤：**

1.被测设备执行adv start -n yuy5 -m legacy和adv start -R random_id -n yuy6 -m legacy
2.打开手机nrf工具搜索ble广播
3.测试设备执行adv stop -i <adv_id> 分别关闭不同的adv_id

**预期结果：**

1.回调正常[bttool] adv name: yuy5 
 [bttool] adv type: legacy
 [bttool] Advertising handle:0x419488c0
 [bttool] on_advertising_start_cb, handle:0x419488c0, adv_id:1, status:0
[bttool] own address type: random_id
[bttool] adv name: yuy6 
[bttool] Advertising handle:0x419488c0
[bttool] on_advertising_start_cb, handle:0x419488c0, adv_id:2, status:0
2.手机侧nrf能够扫描到设备两个地址

---

##### scan设置扫描phy

**测试目的：** 测试phy参数设置

**前提条件：** 切换到bt所在核： 
1. bttool 
2. enable

**步骤：**

1.测试执行scan start -p 1M 
2.执行scan stop 
3.执行scan start -p 2M  (研发确认后回复)
4.执行scan stop
5.执行scan start -p Coded（编码物理层模式，传输距离更远，可靠性更强）
6.执行scan stop

**预期结果：**

1.可以扫描到周围的ble设备 
2.扫描停止 
3.可以扫描到周围的ble设备 
4.扫描停止
5.可以扫描,但扫不到到周围的ble设备 
6.扫描停止

---

##### scan设置扫描mode

**测试目的：** 测试mode参数设置

**前提条件：** 切换到bt所在核： 
1. bttool 
2. enable

**步骤：**

1.测试执行scan start -m 0 （low power mode）
2.执行scan stop 
3.执行scan start -m 1 （balance mode）
4.执行scan stop 
5.执行scan start -m 2  （low latency mode）
6.执行scan stop

**预期结果：**

1.可以扫描到周围的ble设备  ,（相对扫到概率低）
2.扫描停止 
3.可以扫描到周围的ble设备  ,（相对扫到概率中）
4.扫描停止 
5.可以扫描到周围的ble设备  ,（相对扫到概率高）
6.扫描停止

---

##### 组合扫描场景

**测试目的：** 测试各种参数设置

**前提条件：** 切换到bt所在核： 
1. bttool 
2. enable

**步骤：**

1.测试执行scan start -p 2M -m 2
2.执行scan stop 
3.执行scan start -p 1M -m 1
4.执行scan stop

**预期结果：**

1.可以扫描到周围的ble设备 
2.扫描停止 
3.可以扫描到周围的ble设备  
4.扫描停止 

---

### 2. 性能测试

##### BLE发现时长

**测试目的：** 验证性能和压力测试

**前提条件：** 被测设备蓝牙已开启 类用户环境（用安卓手机测）
 性能相关测试不能开snoop日志

**步骤：**

1. 被测设备发起BLE扫描 
2. 被测设备停止扫描 
3. 记录PERFORMANCE-LE-GAP-PROFILE-BTM-SCAN-START 和 发现设备时间 
4. 重复执行10次

**预期结果：**

4. 发现时常达标

---

##### BLE被发现时长

**测试目的：** 验证性能和压力测试

**前提条件：** 被测设备蓝牙已开启 类用户环境（用安卓手机测）
 性能相关测试不能开snoop日志

**步骤：**

1. 打开手机录屏 
2. 被测设备端开启LE广播 
3. 手机打开蓝牙NRF工具，开启蓝牙开始搜索 
4. 记录bt_btif : BTA_DmBleObserve:start = 1 和 bt_btm : btm_ble_process_ext_adv_pkt : bda=6e:eb:21:8d:c3:f4(设备地址)时间（log找不到的时候需要 数帧，记录蓝牙开启成功帧、发现设备帧） 
5. 执行上述步骤10次

**预期结果：**

2. 开启广播成功，被测设备端回调lestartadvertising success 
3. 手机显示搜索到被测设备 
4. 计算发现被测设备时长 
5. 采用3西格玛值方式计算

---

##### BLE发现成功率

**测试目的：** 验证性能和压力测试

**前提条件：** 被测设备蓝牙已开启 类用户环境（用安卓手机测）
 性能相关测试不能开snoop日志

**步骤：**

1.手机侧NRF工具开启BLE广播 
2.被测设备开始BLE扫描 
3.测试20次

**预期结果：**

屏蔽室：成功率100% 家居环境：>=95%

---

##### BLE被发现成功率

**测试目的：** 验证性能和压力测试

**前提条件：** 被测设备蓝牙已开启 类用户环境（用安卓手机测）
 性能相关测试不能开snoop日志

**步骤：**

1.被测设备开始BLE广播 
2.手机侧NRF工具开始扫描 
3.测试20次

**预期结果：**

屏蔽室：成功率100% 家居环境：>=95%

---

##### BLE发现5个设备成功率

**测试目的：** 验证性能和压力测试

**前提条件：** 被测设备蓝牙已开启 类用户环境（用安卓手机测）
 性能相关测试不能开snoop日志

**步骤：**

1.准备五台手机均使用NRF工具开始BLE的广播 
2.被测试开始BLE的扫描 
3.测试20次

**预期结果：**

屏蔽室：成功率100% 家居环境：>=95%

---

##### BLE配对成功率

**测试目的：** 验证性能和压力测试

**前提条件：** 被测设备蓝牙已开启 类用户环境（用安卓手机测）
 性能相关测试不能开snoop日志

**步骤：**

1.手机侧使用NRF工具开启BLE广播 
2.被测设备扫描BLE,并和手机侧NRF发起BLE配对 
3.测试20次

**预期结果：**

屏蔽室：成功率100% 家居环境：>=95%

---

##### BLE扫描效率

**测试目的：** 扫描效率

**前提条件：** 切换到bt所在核： 
1. bttool 
2. enable

**步骤：**

1. scan start -m 2 ，并在待测设备附近放置一个主动广播发包设备
2. 待测设备放置<=1m距离，测试扫描到的广播包数量
3. 待测设备放置5m距离，测试扫描到的广播包数量
4. 待测设备放置10m距离，测试扫描到的广播包数量

**预期结果：**

3. 厂商提供扫描成功率
4. 厂商提供扫描成功率
5. 厂商提供扫描成功率

---

##### 广播与扫描共存后扫描效率

**测试目的：** 开启广播后的扫描效率

**前提条件：** 切换到bt所在核： 
1. bttool 
2. enable

**步骤：**

1. adv start -i 48设置广播间隔 <= 30ms，并在待测设备附近放置一个主动扫描设备
2. scan start -m 2 ，并在待测设备附近放置一个主动广播发包设备
3. 待测设备放置<=1m距离，测试扫描到的广播包数量
4. 待测设备放置5m距离，测试扫描到的广播包数量
5. 待测设备放置10m距离，测试扫描到的广播包数量

**预期结果：**

3. 厂商提供扫描成功率
4. 厂商提供扫描成功率
5. 厂商提供扫描成功率

---

## 附件资源

以下测试用例所需的测试资源文件存放于本目录下：

| 资源文件 | 对应用例 | 说明 |
|---------|---------|------|
| [mediatool测试资源和测试步骤](mediatool测试资源和测试步骤/mediatool测试资源和测试步骤.md) | 4.1.128~4.1.133 Audio/Video 测试 | 包含 audio_file.mp3, audio_file.opus, audio_file.aac, audio_file.wav, media_file_h264.mp4, media_file_h265.mp4 等测试资源 |
| [SPI_I2C](SPI_I2C/SPI_I2C.md) | 1.3.7 I2c/Spi功能测试, 4.1.119 Sensor驱动框架测试 | SPI_I2C 参考文档及 BMI160 传感器连接指导 |
| [Ymodem测试](Ymodem测试/Ymodem测试.md) | OTA 升级相关用例 | Ymodem 文件传输工具及参考文档 |
| [WiFi兼容性路由器列表](WiFi兼容性路由器列表.md) | 6.1.1 路由器兼容性 | 路由器品牌型号及兼容性测试用例详情 |
