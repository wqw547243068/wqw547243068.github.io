
---
layout: post
title:  "移动设备知识"
date:   2020-10-01 20:30:00
categories: 技术工具
tags: adb otg 手机
author : 鹤啸九天 
excerpt: 移动端知识及开发
mathjax: true
permalink: /phone
---

* content
{:toc}

# 移动设备


## 手机设备

更多见：站内 [物联网研发](iot) 专题

### 安卓系统


#### 设备id

Android 设备内的 ID，用于不同方面的跟踪或标识：
1. IMEI
  - IMEI 是最熟悉的一种 ID，手机身份证，也是运营商识别入网设备信息的代码是一种不可重置的**永久标识符**，作用域为设备。
  - 广告跟踪方面
    - `iOS` 的权限管控，iOS 上的第三方 App 并不能通过 IMEI 跟踪用户
    - 但目前 `Android` 平台中绝大部分 App（尤其是在国内）都通过 IMEI 来追踪用户，Android 平台上大多也通过 IMEI 跟踪来实现。
  - 与 IMEI 类似的还有一个叫做 `IMSI` 的标识符，但它主要用于 SIM 卡的身份标识，这里不做展开。
2. Android ID（SSAID）
  - `Android ID` 是 Android 设备里**不依赖于硬件**的一种「**半永久**标识符」，在系统生命周期内不会改变，但系统重置或刷机后会发生变化，其作用域为一组有关联的应用。
3. Device ID
  - Android 平台，`Device ID` 是一种**统称**，与硬件相关的 ID 都可以称之为 `Device ID`，一般是一种**不可重置**的永久标识符，作用域为设备。
  - 根据设备、厂家或者 App 调用需求的不同，读取 Device ID 时可能会返回 IMEI 或其他硬件编码，但也有可能因为设备中没有相关硬件而无法获取 Device ID 或返回无效值；与之形成对应的，iOS 设备中也有类似的永久标识符叫做 UDID，但在 iOS 6 之后，苹果已经不允许需要获取 UDID 的 App 上架 App Store 以防止这种不可重置的 ID 被用于追踪或滥用，取而代之的是 IDFA 标识符，即 iOS 设备广告标识符。
  - 还有一种叫做 `openUDID` 的**设备唯一标识符**，在 iOS 和 Android 系统内都可以使用，但由于不是系统官方提供的 ID 体系，且依赖于第三方 App 生成，所以应用并不广泛，而随着系统迭代升级，openUDID 也逐渐被边缘化甚至被废弃。
4. UUID、GUID
  - UUID 也叫做`实例 ID`，这两个 ID 是在计算机体系内的**通用标识符**。
  - 根据所面向对象的不同，其意义也有微小差别。如果说前面三个 ID 可以用来识别设备，那么这两个 ID 在 Android 系统中的作用主要是识别 App 进程、元素或数据。
  - 因为作用域仅仅是单个应用内，如果用户卸载了该 App 并重新安装，那么 UUID 也会发生变化。不过 App 开发者可以通过存储 UUID 或与其他 ID、用户信息进行组合、绑定、计算等方式，实现 UUID 标识符的「准永久化」。
  - 根据 Android 开发者指南：
    - 标识运行在设备上的应用实例最简单明了的方法就是使用实例ID，在大多数非广告用例中，这是建议的解决方案。只有进行了针对性配置的应用实例才能访问该标识符，并且标识符重置起来（相对）容易，因为它只存在于应用的安装期。
  - 因此，与无法重置的设备级硬件 ID 相比，实例 ID 具有更好的隐私权属性。
5. AAID
  - AAID 与 IDFA 作用相同——IDFA 是 iOS 平台内的广告跟踪 ID，AAID 则用于 Android 平台。
  - 都是一种非永久、可重置的标识符，专门提供给 App 以进行广告行为，用户随时可以重置该类 ID，或通过系统设置关闭个性化广告跟踪。但 AAID 依托于 Google 服务框架，因此如果手机没有内置该框架、或框架不完整、或无法连接到相关服务，这些情况都有可能导致 AAID 不可用。
  - 除了以上这些 ID 标识符以外，某些硬件 ID（例如 MAC 地址）也可能会被用于追踪。

这么多 ID 标识符，每一个都各司其职。而理论上，只有 `AAID` 和 `IDFA` 是真正用于广告行为的。

但现实状况显然不是这样。
- 一方面，Android 平台的不少 App 普遍存在**违反 Android 开发规范**、绕过 `Google Play` 审查，通过滥用 ID 来追踪用户，以此达到为广告流量、营销分析等商业利益服务的目的。
- 另一方面，由于 `AAID` 依托于 **Google 服务框架**，但在国内使用 Google 服务并不太可行，或者大部分国行手机内置的 Google 服务不完整，App 开发者需要寻找另一个方式去标识用户。
  - UUID、GUID 作用域太小，不适合广告跟踪；
  - Android ID 可以通过某些方式被改变或因为 bug 导致不可用，第三方 App 无保证可用性；
  - MAC 地址虽然精准，但在Android 6.0（API 23）到 Android 9（API 28）中，系统限制了第三方 API 获取MAC 地址；
  - 再加上早些时候，大部分「非玩机用户」对此类功能并没有太多概念，第三方 App 为了能以更加精准持久的方式来跟踪用户，将 `IMEI` 变成了用于广告跟踪的首选 ID（在 Google Play 帮助中心，获取永久标识符是一种有条件的、退而求其次的广告投放方法，所以在此之前这种方式也不算完全违规）。

用户逐渐认识到手机 App 疯狂获取权限的行为有可能会侵犯隐私，加之近几年 Android 系统的权限和隐私管理逐渐收紧，Android 10（API 29）终于对第三方 App 获取不可重置永久设备标识符（包括 IMEI）的行为做出了 限制。

国内 App 和广告跟踪服务急需一种替代方案以避免广告流量的损失，`OAID` 顺势而生

Android 开发者文档中对 Android 10 限制设备标识符读取的说明 `OAID` 的本质其实是一种在国行系统内使用的、应对 Android 10 限制读取 IMEI 的、「拯救」国内移动广告的广告跟踪标识符，其背后是 移动安全联盟（Mobile Security Alliance，简称 `MSA`）。

原文链接: [Android设备唯一标识（AndroidID，OAID等 ）](https://blog.csdn.net/weixin_42600398/article/details/117984064)


快速查询Android系统的id
- imei 号: `*#06#`


#### idle 模式

手机系统 idle 模式
- `light doze`的维护窗口比deep doze频繁。最大间隔15min。
  - 白名单外的应用也会限制。比如网络数据。jobscheduler之类
- `deep doze`的维护窗口会随着时间推移逐渐加长，有可能一天只唤醒一次。

公交车、地铁或者自己开车时，手机会进入idle吗？不会
- 运动时处于`light doze`状态。只有静止才会进入`deep doze`. 
- 运动状态下，会进入light doze状态，最长持续15min

移动距离很大或者抖动很厉害，也会进入light doze吗？
- 初始5分钟。然后2倍增加。直到15分钟保持固定频率进入维护窗口


## 手机操作

adb、fastboot命令工具

### 电脑上操控手机

实测：
- anlink与虫洞都不能传输语音，环境：Windows 10+华为mate 30

【2022-6-9】[电脑同屏控制安卓手机！免费、稳定、不限机型](https://zhuanlan.zhihu.com/p/344327144)

**同屏协同**也就是在电脑上同屏操作安卓手机，能提高一定的工作效率，目前不少手机厂商都已经支持了这个功能，例如华为、三星、小米，但是有个限制就是必须相关的品牌手机、电脑才能使用。
- 乐拨软件只能投屏，不能控制手机

没任何限制的同屏协同软件，例如有：
- 国内：`虫洞`、`米卓`、大戴尔的 `Dell Mobile Connect`。
- 国外的免费同屏协同软件「`Anlink`」同样对手机品牌没有限制。

如：谷歌，HTC，华为，联想，小米，OnePlus，Oppo，Realme，三星，索尼，Tecno，Vivo等基本都可以用。

#### 虫洞

[虫洞](https://www.er.run/)
- iOS功能需要付费，安卓基础功能免费
- 安卓需要安装移动端，iOS不需要
- 虫洞支持PC(Windows 7及以上)和Mac。对iOS+PC的虫洞用户，PC系统需为Windows 10 (小版本1803及以上)，且电脑有蓝牙且支持蓝牙BLE外设角色，一般的笔记本都符合要求


#### Anlink

- 「Anlink」只需要在电脑上安装客户端，安卓手机上免安装应用，需要打开调试 "USB调试模式" 功能。

- 安卓手机打开调试模式的方法：
  - 手机设置 → 关于 → 连续按版本号 7 次，就会出现“开发者选项”。在手机设置 → 更多设置 → 开发者选项 → USB调试。或者搜索下你的手机型号，查找方法。
- 用**数据线**把安卓手机连接到电脑上，会弹出USB授权的许可，点击允许，USB连接方式，选择仅充电。正常情况下「Anlink」就可以连接并控制安卓手机了
- 如果不想用数据线的方式连接手机，也可以用 **WIFI模式**
  - 注意，手机和电脑需要在同一个网络下，点击「Anlink」的左侧栏的 WIFI 图标就可以切换模式
- 如果你网络环境、或者设备原因，操作起来延迟比较高的话，可以在设置里面降低画质，找到 Connection 设置画质
- 对比
  - 缺点：Anlink对比之前推荐的同屏协同软件，功能上可能要弱一点，例如没有游戏键位映射功能，如果你想在电脑上控制安卓手机玩游戏，体验就不太好了。  
  - 优点：「Anlink」比之前体验的那几款，都要稳定、流畅，如果你只是办公要来查看手机的信息、简单的文本处理，还是蛮值得推荐使用。
- ![](https://pic1.zhimg.com/80/v2-9de5db49545167ea99b399c34ba57af0_1440w.jpg)



### 连接手机

ADB 连接 Android设备的三种方法，[原文](https://blog.csdn.net/c1063891514/article/details/79039384)
1. **WiFi**连接（手机与pc同一个局域网下）
  - 与电脑在同一局域网内，Android设备连接WiFi
  - 然后adb命令： # adb connect <设备IP>
2. USB**数据线**连接
  - 此种连接要有相应的驱动才行（应该安装phoenixsuit就可以通过数据线来通过adb连接设备，有的不用安装）https://download.csdn.net/download/c1063891514/10589989
3. **串口**连接
  - 使用串口设备与电脑连接。

```shell
# mac下安装adb
brew install --cask android-platform-tools
# 查看安卓手机是否已经连接上电脑
adb devices
# 让adb一直查找安卓设备，找到后才停止
adb wait-for-device
```

打开日志
- 方法一: 在手机拨号盘输入: `*#*#2846579#*#*`，进入设置页：
  - 后台设置---->打开log日志。
  - USB端口设置-->GOOGLE模式（或生产模式）
  - 会警告影响性能。咱开发人员就不管这个了。
- 方法二：
  - `adb logcat -v time > D:\logcat.txt`
  - 这两种方法，其实都不能保证有LOG。
- 方法三：
  - 使用华为的HMS，调用 HMSAgentLog.d(TEST);


### adb 

【2021-6-23】[Android 调试桥 (adb)](https://developer.android.google.cn/studio/command-line/adb)

Android 调试桥 (`adb``) 是一种功能多样的**命令行工具**，可让与设备进行通信。

adb 命令可用于执行各种设备操作（例如安装和调试应用），并提供对 Unix shell（可用来在设备上运行各种命令）的访问权限。它是一种客户端-服务器程序，包括以下三个组件：
- `客户端`：用于发送命令。客户端在开发计算机上运行。您可以通过发出 adb 命令从命令行终端调用客户端。
- `守护程序` (adbd)：用于在设备上运行命令。守护程序在每个设备上作为后台进程运行。
- `服务器`：用于管理客户端与守护程序之间的通信。服务器在开发机器上作为后台进程运行。

adb 包含在 Android SDK 平台工具软件包中。可以用 SDK 管理器下载此软件包，该管理器会将其安装在 android_sdk/platform-tools/ 下。或者，如果要独立的 Android SDK 平台工具软件包，也可以点击此处进行下载。

基本命令
- 连接多个安卓设备时，在adb命令后紧跟着使用 -s 加序列号 来指定要操作的设备
- 注意：建议每次只连接一个安卓设备进行操作！

#### adb 华为

华为手机开启开发者模式：
- 数据线连接电脑 → 设置 → 关于手机 → 连续点击5次版本号 → 提示输入手机锁屏密码
- 返回关于手机→ 回到设置页面 → **系统和更新** → 新出现【开发人员选项】页面
  - 依次勾选个地方：保持唤醒、“仅充电”模式下允许ADB调试、USB调试；
  - 注意：必须先设置为”仅充电”模式，然后再打开“调试模式”

【2022-2-15】Mac下连不上华为mate 30
1. *#*#2846579#*#* 进入工程模式后，选择ProjectMenu,
2. 后台设置->USB端口配置->会看到一长串的列表，只要选中“google模式”就行。然后退出工程模式
3. 然后退出工程模式，重启下机器。再连到Mac上试试，手机上会出现已经连接usb调试的提示。在系统里用”adb devices”也能查看到设备了.

[原文链接](https://blog.csdn.net/u013078986/article/details/46866193)

失败，花粉[发帖](https://club.huawei.com/forum.php?mod=viewthread&tid=30529238&extra=)


#### adb shell

使用方法

```sh
adb install test.apk # 安装软件包
adb shell settings put global development_settings_enabled 1 # 设置环境变量(打开开发者选项)
adb shell "date -s '2023-09-06 21:40:00'" # 设置系统时间
adb shell pkill test # 杀死进程
adb shell am start -n test # 打开进程
```


```shell
# 版本
adb server version
# 查看设备
adb devices
# List of devices attached
# FA6AX0301341    device
# ce0217122b56b02604  device

adb -s FA6AX0301341 shell
#sailfish:/ $

# 远程连接手机调试
adb connect 手机ip:5566 # 手机端需要安装无线adb应用）

# 相互传递数据
adb forward tcp:11111 tcp:22222 # 需要先建立服务端和客户端

# 2.1) 锁定/解锁/重启/关机
# 锁定/解锁手机
adb shell input keyevent 26 # 锁定手机
adb shell input keyevent 82 # 解锁手机(如果设置了密码，会提示输入密码)
# 输入密码，并回车
adb shell input text 123456 && adb shell input keyevent 66
# 重启/关机
adb reboot  # 重启
adb shell reboot  # 重启
adb shell reboot -p  # 关机

# 2.2) 系统设置
# 打开关闭蓝牙
adb shell service call bluetooth_manager 6 # 打开蓝牙
adb shell service call bluetooth_manager 9 # 关闭蓝牙
# 打开关闭wifi
adb shell svc wifi enable  # 打开wifi
adb shell svc wifi disable  # 关闭wifi
# 打开wifi设置界面
adb shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings
# 连接时保持亮屏 设置
svc power stayon [true|false|usb|ac|wireless]
# 参数解释：
# true: 任何情况下均保持亮屏
# false:任何情况下均不保持亮屏（经过设定的时间后自动黑屏）
# usb, ac, wireless：设置其中之一时，仅在这一种情况下才保持亮屏。

# 2.3) 模拟本机操作

# 模拟按键操作
adb shell input keyevent 111 # 关闭软键盘(其实是按下ESC，111=KEYCODE_ESCAPE)
# 更多按键代码，在这里 https://developer.android.com/reference/android/view/KeyEvent.html

# 模拟滑动触屏操作
adb shell input touchscreen swipe 930 880 930 380 # 向上滑
adb shell input touchscreen swipe 930 880 330 880 # 向左滑
adb shell input touchscreen swipe 330 880 930 880 # 向右滑
adb shell input touchscreen swipe 930 380 930 880 # 向下滑
# 模拟鼠标操作
adb shell input mouse tap 100 500
#100是x，500是y。
#原点在屏幕左上角。

# 2.4) 运行程序

# 拨打电话
adb shell am start -a android.intent.action.CALL -d tel:10010
# 打开网站
adb shell am start -a android.intent.action.VIEW -d  http://google.com
# 启动APP
adb shell am start -n com.package.name/com.package.name.MainActivity
adb shell am start -n com.package.name/.MainActivity

adb shell monkey -p com.android.contacts -c android.intent.category.LAUNCHER 1
# Events injected: 1
## Network stats: elapsed time=16ms (0ms mobile, 0ms wifi, 16ms not connected)

# 3) 硬件高级调节
# 3.0) 信息查看
# 查看设备序列号
adb get-serialno
# 3.1) CPU相关
# 查看CPU温度
# 先查看有哪些温度区域thermal zone
adb shell ls sys/class/thermal/
# cooling_device0
# cooling_device1
# cooling_device2
# 
# thermal_zone0
# thermal_zone1
# thermal_zone2

# 查看某个CPU温度

cat /sys/class/thermal/thermal_zone0/temp                                                                                                
# 25800 # 温度是milliCelsius，所以这里是25.8度C。

# CPU设置
# 查看当前手机可用的governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors                                                                     
# userspace interactive performance
# 锁定CPU为最大频率
# 参考：https://forum.xda-developers.com/showthread.php?t=1663809

# 设置CPU governor为performance。

echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# 4) 刷机
# 重启手机，进入recovery或bootloader模式
adb reboot recovery # 恢复模式
adb reboot bootloader  # 刷机模式。不同手机，命令不同，要试一下。
adb reboot-bootloader
adb reboot boot loader
# 进入 fastboot 模式。
adb  reboot  fastboot
# 或关机，然后同时按住 增加音量 和 电源 键开机

# 5) 调试
# 抓取开机日志
adb wait-for-device && adb shell logcat -v threadtime | tee mybootup.log
# 查看日志
adb logcat
# 关闭/重启adb服务进程
adb kill-server
adb start-server
# 从本地复制文件到设备，或者反之
adb push test.zip /sdcard/  # 从本地复制文件到设备
adb pull /sdcard/abc.zip  ~/  # 从设备复制文件到本地
# 显示已经安装的APP的包名
adb shell pm list packages
# 安装、删除APP
adb install abc.apk # 第一次安装。如果手机上已经有此app,则会报错。
adb install -r abc.apk # 如果已经安装过，保留原app的数据
adb -s 11223344 install abc.apk  # 当多个安卓连接到电脑时，安装到指定一台安卓上
adb uninstall com.example.appname
# 查看apk的版本（无需解压）
aapt dump badging abcd.apk |grep version
# 捕获键盘操作
adb shell getevent -ltr 
# 查看屏幕分辨率 dpi
wm density
wm size
# 设置：
wm density 240
# 立刻生效。
```

### OTG

OTG是`On-The-Go`的缩写
- 2001年12月18日, 由USB Implementers Forum公布，在2014年左右开始在市场普及。
- OTG技术主要是基于USB技术的发展和普及而来，完全兼容`USB2.0`协议。
- ![](https://pic2.zhimg.com/80/v2-c17dbea1306167cbf78fa403955c22ad_720w.jpg)

OTG可以**脱离计算机设备**，利用各种设备上的USB口进行数据交换。解决了各种设备间不同制式的连接接口的数据交换不便的问题。
- OTG主要应用于各种**不同设备（包括移动设备）间的联接**，尤其是现在市面上琳琅满目的各种移动电子设备，比如平板电脑、移动电话、打印机、消费类电子设备等。目前市面上的智能手机上基本都支持OTG。

OTG是指在**无电脑**作为中转站的情况下，直接将手机连接U盘、读卡器、MP3、键盘、数码相机等外部设备进行数据传输、输入操作或充电等功能。通过OTG技术，可以给智能终端扩展USB接口配件以丰富智能终端的功能，比如扩展遥控器配件，把手机、平板变成万能遥控器使用。

鉴于设备接口及USB类型的不一致，一般OTG有如下几类：
- USB2.0 OTG：包括Micro 5PIN OTG（常见安卓手机）、Mini 5PIN OTG（常见安卓平板）
- Micro USB3.0 OTG：三星Note3、Galaxy S5等在2016年以前的安卓手机OTG接口
- Type-C OTG：目前支持Type-C接口的设备（比如小米Mix系列等）
- Lightning OTG：苹果手机专用OTG

![](https://pic3.zhimg.com/80/v2-e527ac0de41bbe029ff61e58dda21b4e_720w.jpg)

OTG有哪些应用场景
- 1、**数据传输**
  - 这个场景比较常见，比如使用OTG数据线将手机和计算机连接后，将数据在手机和计算机间进行传输。
  - 出差在外，电脑不方便联网，可以使用手机或平板接收数据后，使用支持OTG功能的U盘将数据从手机拷出，然后再将U盘插到电脑上使用。
  - 使用OTG线，将手机或相机和打印机连接后，直接将照片打印出来。
  - 使用OTG线，连接移动硬盘，播放其中存储的高清视频或将手机中的照片视频导入等。
- 2、**系统重做**（刷机）
  - 当手机或其他设备宕机后，可以使用OTG线将装有系统刷机包的U盘连接后加电重启后通过加载刷机包进行刷机。
- 3、**外接设备**
  - 比较常见的支持USB的设备均可通过OTG方式进行连接，常见的比如键盘、手机、游戏操作手柄等等。
  - ![](https://iknow-pic.cdn.bcebos.com/f7246b600c3387447f2cb2e45f0fd9f9d62aa0b9)
- 4、临时**反向充电**
  - 当外出在外，有些小设备（手环、智能手表、MP3等）没有电时，可以通过使用支持反向充电的专用OTG线连接手机进行充电。

### 手机屏幕坏了怎么操控

【2022-2-15】华为手机屏幕摔碎，无法操控，手机屏幕碎了，如何连接电脑？ - [鹤啸九天的回答](https://www.zhihu.com/question/278365377/answer/2348879230)

换屏费用高达1380元（上门），屏下指纹花费高，普通触控屏幕400元
- （1）使用OTG转接头，投影到显示器，通过鼠标操控屏幕，前提是屏幕没有完全损坏
- （2）电脑上安装一个安卓手机**模拟器**，然后连上手机。电脑上的模拟器上就可以看到你手机的屏幕状态。
- （3）手机操控软件，[虫洞](https://er.run/#download)，电脑操控手机，自动全屏，横屏，多应用

## Android 开发

【2023-9-7】[Android Studio](https://developer.android.com/studio), 支持多个系统：windows、mac、Linux和chrome os




# 结束