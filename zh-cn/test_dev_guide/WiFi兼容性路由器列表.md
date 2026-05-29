# WiFi兼容性路由器列表

## 路由器型号列表

| 序号 | 产品型号 | 设备单价（元RMB） | 订单链接 |
|------|---------|------------------|---------|
| 1 | TP-LINK AX3000 | 299 | [购买链接](https://item.jd.com/100013265745.html#crumb-wrap) |
| 2 | 华为路由AX3 Pro | 399 | [购买链接](https://item.jd.com/100012605828.html) |
| 3 | 中兴ZTE【骐骥系列】AX5400Pro | 549 | [购买链接](https://item.jd.com/100027895572.html) |
| 4 | TP-LINK  AC1900 | 199 | [购买链接](https://item.jd.com/4772588.html) |
| 5 | TP-LINK AX5400 | 379 | [购买链接](https://item.jd.com/100013953102.html) |
| 6 | 腾达（Tenda）AC23 | 179 | [购买链接](https://item.jd.com/100007732774.html) |
| 7 | 京东云无线宝AX1800 | 249 | [购买链接](https://item.jd.com/100014311519.html) |
| 8 | 荣耀路由4 WiFi6千兆路由 ax3000 | 299 | [购买链接](https://item.jd.com/100017772267.html) |
| 9 | 水星（MERCURY） WiFi6 AX3000 | 229 | [购买链接](https://item.jd.com/100014540249.html) |
| 10 | 新华三（H3C）NX54 | 499 | [购买链接](https://item.jd.com/100022014540.html) |
| 11 | 小米AX9000 | 1299 | - |
| 12 | 华硕RT-AX86U | 1999 | - |
| 13 | 华硕RT-AX82U | 829 | - |
| 14 | 小米4A千兆版 | 89 | - |
| 15 | 360安全路由v2 | 133 | - |
| 16 | TP-Link WR886N | 109 | - |
| 17 | 小米 Redmi AX6S路由器 | 299 | [购买链接](https://item.jd.com/100027042714.html) |
| 19 | 小米 Redmi 路由器 AX5400 | 399 | [购买链接](https://item.jd.com/100034616288.html) |
| 20 | Redmi 路由器 AC2100 5G双频 | 199 | [购买链接](https://item.jd.com/100010581822.html) |
| 21 | Redmi 路由器 AC2100 5G双频 |  | - |

---

## WiFi路由器兼容性测试用例

### wapi sta模式配网--2.4G网络

**测试目的：** 验证wapi 支持连接2.4G网

**前提条件：** 设备上电，路由器上电且网络正常

**步骤：**

```
1、设备进入到nuttx shell； 
2、执行以下命令进行STA连接：
 ifup wlan0 
 wapi mode wlan0 2 
 wapi psk wlan0 <路由器配置的密码> 3 
 wapi essid wlan0 <路由器配置的ssid> 1 
 renew wlan0 
 3、执行ifconfig； 
 4.执行ping www.baidu.com
```

**预期结果：**

1-2执行成功无报错，设备成功配网； 
 3、设备分配到ip地址；
 4.可以ping通外网


---

### wapi psk 连接open 2.4G网络

**测试目的：** 验证支持wapi 连接open 2.4G网络

**前提条件：** 设备上电，路由器上电且网络正常

**步骤：**

```
1、设备进入到nuttx shell； 
2、执行以下命令进行STA连接：
 ifup wlan0 
 wapi mode wlan0 2
 wapi psk wlan0 0
 wapi essid wlan0 <路由器配置的ssid> 1
 renew wlan0
 3、执行ifconfig； 
 4.执行ping www.baidu.com
```

**预期结果：**

1-2执行成功无报错，设备成功配网； 
 3、设备分配到ip地址；
 4.可以ping通外网


---

### wapi sta模式配网--5G网络

**测试目的：** 验证wapi 支持连接5G网

**前提条件：** 设备上电，路由器上电且网络正常

**步骤：**

```
1、设备进入到nuttx shell； 
2、执行以下命令进行STA连接： 
 ifup wlan0
 wapi mode wlan0 2
 wapi psk wlan0 <路由器配置的密码> 3
 wapi essid wlan0 <路由器配置的ssid> 1
 renew wlan0
 3、执行ifconfig； 
 4.执行ping www.baidu.com
```

**预期结果：**

1-2执行成功无报错，设备成功配网； 
 3、设备分配到ip地址；
 4.可以ping通外网


---

### wapi psk 连接open 5G网络

**测试目的：** 验证支持wapi 连接open 5G网络

**前提条件：** 设备上电，路由器上电且网络正常

**步骤：**

```
1、设备进入到nuttx shell； 
2、执行以下命令进行STA连接：
 ifup wlan0 
 wapi mode wlan0 2
 wapi psk wlan0 0
 wapi essid wlan0 <路由器配置的ssid> 1
 renew wlan0
 3、执行ifconfig； 
 4.执行ping www.baidu.com
```

**预期结果：**

1-2执行成功无报错，设备成功配网； 
 3、设备分配到ip地址；
 4.可以ping通外网


---

### 设备配置5G网络后重启路由器

**测试目的：** 验证设备配网后重启路由器，设备无异常

**前提条件：** 设备上电，路由器上电且网络正常

**步骤：**

```
1、设备进入到nuttx shell； 
2、执行以下命令进行STA连接： 
 ifup wlan0
 wapi mode wlan0 2
 wapi psk wlan0 <路由器配置的密码> 3
 wapi essid wlan0 <路由器配置的ssid> 1
 renew wlan0
 3、设备配网成功后重启路由器
 4.查看设备串口log
```

**预期结果：**

4.设备串口log无异常，重新启动路由器，设备由link up状态切换为link down,路由器启动成功后，设备状态切换为link up，正常访问外网


---

### 设备待连接网络开启双频合一

**测试目的：** 验证设备在所连接网络开启双频合一功能后，能正常连接配网

**前提条件：** 设备上电，路由器上电且网络正常，设备待连接网络设置开启双频合一功能

**步骤：**

```
1、设备进入到nuttx shell； 
2、执行以下命令进行STA连接： 
 ifup wlan0
 wapi mode wlan0 2
 wapi psk wlan0 <路由器配置的密码> 3
 wapi essid wlan0 <路由器配置的ssid> 1
 renew wlan0
 3、执行ifconfig； 
 4.执行ping www.baidu.com
```

**预期结果：**

1-2执行成功无报错，设备成功配网； 
 3、设备分配到ip地址；
 4.可以ping通外网


---
