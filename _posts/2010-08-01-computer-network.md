---
layout: post
title:  "计算机网络-Computer Network"
date:   2010-08-01 23:42:00
categories: 计算机基础
tags: 网络 OSI 路由器 交换器 调制解调器 猫 lan wan wlan ap tcp udp 下载 种子 磁力 电视 卫星 地面波 广播 蓝牙 耳机 wifi 内网穿透 云盘
excerpt: 计算机网络知识点
mathjax: true
permalink: /network
---

* content
{:toc}

# 总结

- 【2022-3-30】[60 张图详解 98 个常见网络概念](https://www.toutiao.com/article/7080442955122606624/)
- [2017-9-19]视频集合：[内存原理解析](http://www.365yg.com/group/6467022800149283342/),[CPU缓存原理解析](http://www.365yg.com/group/6467021466209616397/),[TCP,UDP协议原理对比](http://www.365yg.com/group/6467022804800766477/)，【2019-10-26】[动画讲解TCP，再不懂请来打我](https://www.toutiao.com/a6751645874356486664/?timestamp=1572010379&app=news_article_lite&group_id=6751645874356486664&req_id=201910252132580100260771991F3BD7D6),[IPv4,IPv6原理解析](http://www.365yg.com/group/6467021492105249293/)，[代理服务器原理解析](http://www.365yg.com/group/6467022795812373005/)，[集线器-交换机-路由器区别](http://www.365yg.com/group/6467021483385291277/)，[DNS域名解析](http://www.365yg.com/group/6467021479107101197/)，[超线程原理解析](http://www.365yg.com/group/6467021487722201614/),[磁盘碎片原理解析](http://www.365yg.com/group/6467021470504583693/)
- 【2021-3-19】如何跟小白解释路由器和交换机的区别？并且家用路由器充当了路由器和交换机的功能吗？[薛定谔不在家的回答](https://www.zhihu.com/question/22007235/answer/402261894)
  - 总结：交换机适合局域网内互联，路由器实现全网段互联。猫的学名叫**调制解调器**，作用是将数字信号（电脑想要发送的信息）转换成模拟信号（网线中的电流脉冲）从而使信息在网线中传输。由于计算机的一切信号都要由电流脉冲传送出去，因而猫是必须的。目前的家用路由器一般都是**路由猫**，即路由器兼顾了猫和简单交换机的功能，因而在选购时，选一款性价比超高的路由猫就可以了。至于物理地址，逻辑地址，交换机与路由器的寻址方式等问题属于更专业的范畴
  - ![](https://pic1.zhimg.com/80/v2-6c49ad959be632e15b3f3ad70949a98e_1440w.jpg?source=1940ef5c)
- 【2018-3-13】松果云科普：动画解释，[详解硬盘工作原理](https://www.365yg.com/a6524897664687931911)，[详解显卡工作原理：GPU和CPU的区别](https://www.365yg.com/i6525769921438155272)
- 【2021-4-12】[天线是如何工作的](https://v.ixigua.com/e63CMmo/)


# 网络结构

## 互联网

`互联网`（ Internet ）：通过各种**互联网协议**为全世界成千上万的设备建立互联的**全球计算机网络系统**。
- `互联网` → `路由器` → `手机`（家庭设备）
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/a2396d3285dd4bba9971e3c74c3a4d1e?from=pc)

种类：
- `局域网`（ LAN ）：在一个有限区域内实现终端设备互联的网络。
- `城域网`（ MAN ）：规模大于局域网，覆盖区域小到一个方圆数千米的大型园区，大到一个城市圈的网络。
- `广域网`（ WAN ）：跨越大范围地理区域建立连接的网络。


### 全球互联网

上世纪50年代，不同计算机用户和通信网络之间进行常规通信的需求开始萌发，促使分散网络、排队论和数据包交换等研究相继出现；
- 随后，`ARPAnet`(阿帕网) 60年代问世，并于1973年扩展成为互联网；
- 之后一年，ARPA 罗伯特·卡恩和斯坦福的温登·泽夫提出了`TCP/IP`协议，终于定义了在电脑网络之间传送报文的方法...

互联网大发展的序幕由此拉开！

4个入口8条光缆

1994年4月，中国与国际 64K Internet 信道开通（借助国际卫星信道接入），“走向世界”的一个转折点。
- 然而 这次与世界的沟通，仅仅是“窄带”沟通，让国内的几百名科学家“体验”收发电子邮件...

互联网“宽带”沟通又是如何实现？答案是`海底光缆`。

所谓全球互联网是世界各国的网络相互联接而组成的超**大型局域网**，其中实现**洲际**联接靠`卫星通信`和`海底光缆`。
- 考虑到`卫星通信`带宽有限且价格不菲，因此, 全球90%以上的国际数据都是通过`海底光缆`进行传输的
- 基本上是海底光缆构建了今天的全球“宽带”互联网！
- ![](http://www.dxdlw.com/Uploads/Image/201902/19/=84958=6368617419876150293949634.png)

[海底光缆分布图](http://www.dxdlw.com/ShowPost.aspx?ThreadID=209746)

【2019】回形针 [Vol 124 海底光缆如何连接全球互联网](https://www.youtube.com/watch?v=q7CjsfLJuuE)

<iframe width="560" height="315" src="https://www.youtube.com/embed/q7CjsfLJuuE?si=BwmcaenefktZGgVb" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## 物联网

物联网（ IoT ）：通过内置**电子芯片**的方式，将各种**物理设备**连接到网络中，实现**多元**设备间信息交互的网络。

## 云计算

云计算（ Cloud Computing ）：通过互联网为计算机和其它设备提供处理资源共享的网络。

大数据（ Big Data ）：通过汇总的计算资源对庞大的数据量进行分析，得出更加准确的预测结论，并用来指导实践。

## 万维网

万维网（ WWW ）：可以通过 URL 地址进行定义、通过 HTTP/HTTPS 协议建立连接、通过互联网进行访问的网页资源空间。
- `客户端`上的`浏览器`访问网页 → `互联网` → `服务器`
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/362db9fd04464cbd8989c0d840ed6221?from=pc)

Web ：万维网的简称，将设备相互连接起来，以将设备中的数据以超文本形式提供给请求方的网络。

## 通信连接

- 服务器-客户端模型：一种应用层协议模型，这种模型的应用程序是由专门的主机为其它主机提供服务。
- P2P 模型：一种应用层协议模型，这种模型的应用协议会在主机之间建立对等体连接，每台主机身份对等，它们可以提供服务，也可以接受服务。

- Telnet ：由管理设备充当客户端，向充当服务器的被管理设备建立连接，以对其实施远程管理的应用层协议。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/fe15e63a65ba46c9b8ebe5fd2c269705?from=pc)
- Shell ：操作系统提供给用户操作设备的接口。
- SSH ：由管理设备充当客户端，向充当服务器的被管理设备建立安全连接，以对其实施安全远程管理的应用层协议。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/c3aa4ab96ee94a7da0eb6e9bee00d56b?from=pc)

## 操作系统

操作系统：一种安装在智能设备上，为操作智能设备消除硬件差异，并为程序提供可移植性的软件平台。
- 硬件（CPU/IO.存储器） → 操作系统 → 程序
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/40acfcbb7d374e0da0146f8a4fcab17a?from=pc)

按交互方式划分：
- **图形用户界面**（ GUI ）：指用户在大部分情况下可以通过点击图标等可视化图形来完成设备操作的软件界面。
- **命令行界面**（ CLI ）：指用户需要通过输入文本命令来完成设备操作的软件界面。

## 计算机硬件

整体关系：
- 内存、ROM、NVRAM → RAM → CPU
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/db7c163beea24b2e8db7f882fb50549b?from=pc)

详解
- RAM ：随机存取存储器的简称，也叫做内存。安装在数通设备上与安装在计算机中的作用相同，即用于存储临时文件，断电内容消失。
- Flash ：安装在数通设备上，与计算机硬盘的功能类似，用来存放包括操作系统在内的大量文件。
- NVRAM ：非易失随机存取存储器的简称。用来保存数通设备的启动配置文件，断电不会消失。
- Console 接口：即控制台接口，通过 Console 线缆连接自己的终端和数通设备的 Console 接口，使用终端模拟软件对数通设备进行本地管理访问。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/9fc808dc92d340bd9ad74013b1276186?from=pc)


## MAC地址

MAC（Media Access Control，介质访问控制）地址，或称为**物理地址**，也叫硬件地址，用来定义网络设备的位置，MAC地址是网卡出厂时设定的，是固定的（但可以通过在设备管理器中或注册表等方式修改，同一网段内的MAC地址必须唯一）。MAC地址采用十六进制数表示，长度是6个字节（48位），分为前24位和后24位。
- 1、前24位叫做组织唯一标志符（Organizationally Unique Identifier，即OUI），是由IEEE的注册管理机构给不同厂家分配的代码，区分了不同的厂家。
- 2、后24位是由厂家自己分配的，称为扩展标识符。同一个厂家生产的网卡中MAC地址后24位是不同的。

MAC地址对应于OSI参考模型的第二层数据链路层，工作在数据链路层的交换机维护着计算机MAC地址和自身端口的数据库，交换机根据收到的数据帧中的“目的MAC地址”字段来转发数据帧。

MAC 地址：长度 48 位，固话在设备硬件上，用十六进制表示的数据链路层地址。
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/2694fa7b9a7443779807d9ac25900752?from=pc)

## ip地址

【2018-11-3】[IP地址详解](http://blog.51cto.com/6930123/2112403)

【2022-4-5】[计算机是如何通信的？IP地址与mac地址是什么？](https://www.ixigua.com/6958363991613637133)

<iframe width="720" height="405" frameborder="0" src="https://www.ixigua.com/iframe/6958363991613637133?autoplay=0" referrerpolicy="unsafe-url" allowfullscreen></iframe>

### 如何查看本机ip

```sh
# 方法一
curl ifconfig.me # 查看非windows系统的公网ip
# 方法二
# 系统偏好 → 网络 → TCP/TP， ip地址
```


### ip地址介绍

`IP地址`（Internet Protocol Address），缩写为IP Adress，是一种在Internet上的给主机统一编址的地址格式，也称为**网络协议**（IP协议）地址。它为互联网上的每一个网络和每一台主机分配一个**逻辑地址**，常见的IP地址，分为IPv4与IPv6两大类，当前广泛应用的是IPv4，目前IPv4几乎耗尽，下一阶段必然会进行版本升级到IPv6；如无特别注明，一般我们讲的的IP地址所指的是IPv4。
- ![](https://s4.51cto.com//images/blog/201805/04/01b93a1d0acac52cc0bd4878696d4098.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)
IP地址对应于OSI参考模型的第三层网络层，工作在网络层的路由器根据目标IP和源IP来判断是否属于同一网段，如果是不同网段，则转发数据包。

分类：
- IPv4 ：互联网协议第 4 版，协议定义的地址空间已用完，但还是目前使用最广泛的互联网协议规范。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/de347b0260694d75ab90780340b7901c?from=pc)
- IPv6 ：互联网协议第 6 版，也就是新版互联网协议，能提供比 IPv4 协议更广泛的地址空间。

`IP地址`(IPv4)由32位二进制数组成，分为4段（4个字节），每一段为8位二进制数（1个字节）; 每一段8位二进制，中间使用英文的标点符号“.”隔开
- 由于二进制数太长，为了便于记忆和识别，把每一段8位二进制数转成十进制，大小为0至255。IP地址的这种表示法叫做“**点分十进制表示法**”。
- IP地址表示为：xxx.xxx.xxx.xxx，举个栗子：210.21.196.6就是一个IP地址的表示。


IP地址的组成
- IP地址 = **网络**地址 + **主机**地址
- ![](https://s4.51cto.com//images/blog/201805/03/ac3c6598dd24b25dc9b01bb60b15d725.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)
- ![](https://s4.51cto.com//images/blog/201805/04/63174612ee1ad4b44480965034a56187.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)

- 掩码：一种与 IPv4 地址长度相同，也是使用点分十进制表示法的编码，作用是描述 IPv4 地址中网络位的长度。
- 网络位：IP 地址中用来表示设备所在网络的地址位，位于 IP 地址的前面。
- 主机位：IP 地址中用来表示网络中的编号的地址位，位于 IP 地址的后面。
- 有类编址：将 IP 地址通过前 4 位二进制数分为 A 、B 、C 、D 等类别，并按照类别固定网络位长度的编址方式。
- 无类编址：打破 IP 地址类别的限制，不以 IP 地址前几位二进制数的取值来固定网络位长度的编址地址。

![img](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/dad35aaff8614422bac08aee8b4fd450?from=pc)

### ip地址与mac地址

IP地址与MAC地址区别
- 长度不同：IP地址为32位（二进制），MAC地址为48位（十六进制）。
- 分配依据不同：IP地址的分配是基于网络拓扑，MAC地址的分配是基于制造商。
- 寻址协议层不同：IP地址应用于OSI第三层（网络层），而MAC地址应用在OSI第二层（数据链路层）。

IP和MAC两者之间分工明确，默契合作，完成通信过程。在数据通信时
- IP地址专注于**网络层**，网络层设备（如路由器）根据IP地址，将数据包从一个网络传递转发到另外一个网络上；
- 而MAC地址专注于**数据链路层**，数据链路层设备（如交换机）根据MAC地址，将一个数据帧从一个节点传送到相同链路的另一个节点上。
- IP和MAC地址这种映射关系由 **ARP**（Address Resolution Protocol，地址解析协议）协议完成，ARP根据目的IP地址，找到中间节点的MAC地址，通过中间节点传送，从而最终到达目的网络。
- ![](https://s4.51cto.com//images/blog/201805/04/3c9770b7936b27d2b955b1703d13dbbb.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)


### ip地址分类

IP地址分A、B、C、D、E五类，其中A、B、C这三类是比较常用的IP地址，D、E类为特殊地址。
- ![](https://s4.51cto.com//images/blog/201805/04/d8edafebca5bbbf1d5bb35cef4156026.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)

- ①、**A类**地址
  - A类地址第1字节为网络地址（最高位固定是0），另外3个字节为主机地址。
  - A类地址范围：1.0.0.0 - 126.255.255.255，其中0和127作为特殊地址。
  - A类网络默认子网掩码为255.0.0.0，也可写作/8。
  - A类网络最大主机数量是256×256×256-2=166777214（减去1个主机位为0的网络地址和1个广播地址）。
  - 在计算机网络中，主机ID全部为0的地址为网络地址，而主机ID全部为1的地址为广播地址，这2个地址是不能分配给主机用的。
- ②、**B类**地址
  - B类地址第1字节（最高位固定是10）和第2字节为网络地址，另外2个字节为主机地址。
  - B类地址范围：128.0.0.0 - 191.255.255.255。
  - B类网络默认子网掩码为255.255.0.0，也可写作/16。
  - B类网络最大主机数量256×256-2=65534。
- ③、**C类**地址
  - C类地址第1字节（最高位固定是110）、第2字节和第3个字节，另外1个字节为主机地址。
  - C类地址范围：192.0.0.0 - 223.255.255.255。
  - C类网络默认子网掩码为255.255.255.0，也可写作/24。
  - C类网络最大主机数量256-2=254。
- ④、**D类**地址
  - D类地址不分网络地址和主机地址，它的第1个字节的最高位固定是1110。
  - D类地址用于组播（也称为多播）的地址，无子网掩码。
  - D类地址范围：224.0.0.0 - 239.255.255.255。
- ⑤、**E类**地址
  - E类地址也不分网络地址和主机地址，它的第1个字节的最高位固定是11110。
  - E类地址范围：240.0.0.0 - 255.255.255.255。
  - 其中240.0.0.0-255.255.255.254作为保留地址，主要用于Internet试验和开发，255.255.255.255作为广播地址。
总结
- ![](https://s4.51cto.com//images/blog/202001/05/6187e6bd1d31364a8bda03f376b30351.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)

### 特殊IP地址

以下这些特殊IP地址都是不能分配给主机用的地址：
- 主机ID全为0的地址：特指某个网段，比如：192.168.10.0 255.255.255.0，指192.168.10.0网段。
- 主机ID全为1的地址：特指该网段的**全部**主机，比如：192.168.10.255，如果你的计算机发送数据包使用主机ID全是1的IP地址，数据链层地址用广播地址FF-FF-FF-FF-FF-FF。
- 127.0.0.1：是**本地环回**地址，指**本机**地址，一般用来测试使用。回送地址(127.x.x.x)是本机回送地址(Loopback Address)，即主机IP堆栈内部的IP地址。
- 169.254.0.0：169.254.0.0-169.254.255.255实际上是自动私有IP地址。
- 0.0.0.0：如果计算机的IP地址和网络中的其他计算机地址冲突，使用ipconfig命令看到的就是0.0.0.0，子网掩码也是0.0.0.0。
总结
- ![](https://s4.51cto.com//images/blog/201805/04/e664d181be8697229b52f2af236afae7.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)

### 公网和私网IP地址

- 公网IP地址
  - 公有地址分配和管理由Inter NIC（Internet Network Information Center 因特网信息中心）负责。各级ISP使用的公网地址都需要向Inter NIC提出申请，有Inter NIC统一发放，这样就能确保地址块不冲突。
- 私网IP地址
  - 创建IP寻址方案的人也创建了私网IP地址。这些地址可以被用于私有网络，在Internet没有这些IP地址，Internet上的路由器也没有到私有网络的路由表。
  - A类：10.0.0.0 255.0.0.0，保留了1个A类网络。
  - B类：172.16.0.0 255.255.0.0～172.31.0.0 255.255.0.0，保留了16个B类网络。
  - C类：192.168.0.0 255.255.255.0～192.168.255.0 255.255.255.0，保留了256个C类网络。
  - PS：私网地址访问Internet需要做NAT或PAT网络地址转换
- ![](https://s4.51cto.com//images/blog/201805/04/8a53e6b9c1051bd5bda08364dd1ea4b1.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)
总结
- ![](https://s4.51cto.com//images/blog/201805/04/b00638fef79863c0e1958bb912a52d7d.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)

## DNS 域名解析

【2022-3-10】[网络基础知识之————A记录和CNAME记录的区别](https://developer.aliyun.com/article/311926)

DNS ：全称是域名服务的应用层协议，向请求解析域名 IP 地址的客户端提供域名和地址解析服务。
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/ba3d29c8987f42b49760a2d079455a06?from=pc)

### 1、什么是域名解析？

域名解析就是国际域名或者国内域名以及中文域名等域名申请后做的到IP地址的转换过程。IP地址是网路上标识您站点的数字地址，为了简单好记，采用域名来代替ip地址标识站点地址。域名的解析工作由DNS服务器完成。
- ![](https://yqfile.alicdn.com/img_34fbc1d1bdd522366ab29fbda03c31e0.png)

### 2、什么是A记录？

A (Address) 记录是用来指定主机名（或域名）对应的IP地址记录。用户可以将该域名下的网站服务器指向到自己的web server上。同时也可以设置您域名的二级域名。
- ![](https://yqfile.alicdn.com/img_2068936ddf04bb6064eb3795e5f5b6da.png)


### 3、什么是CNAME记录？

即：别名记录。这种记录允许您将多个名字映射到另外一个域名。通常用于同时提供WWW和MAIL服务的计算机。例如，有一台计算机名为“host.mydomain.com”（A记录）。它同时提供WWW和MAIL服务，为了便于用户访问服务。可以为该计算机设置两个别名（CNAME）：WWW和MAIL。这两个别名的全称就 http://www.mydomain.com/ 和 “mail.mydomain.com”。实际上他们都指向“host.mydomain.com”。
- ![](https://yqfile.alicdn.com/img_19231a2b40654536c3278c145fd6f122.png)

### 区别

A记录和CNAME进行域名解析的区别
- A记录就是把一个域名解析到一个IP地址（Address，特制数字IP地址），而CNAME记录就是把域名解析到另外一个域名。
- 其功能是差不多，CNAME将几个主机名指向一个**别名**，其实跟指向IP地址是一样的，因为这个别名也要做一个A记录的。但是使用CNAME记录可以很方便地变更IP地址。如果一台服务器有100个网站，他们都做了别名，该台服务器变更IP时，只需要变更别名的A记录就可以了。

![](https://yqfile.alicdn.com/img_b846fe5c2fac9eae6376782c85979f89.png)

域名解析CNAME记录A记录哪一种比较好？如果论对网站的影响，就没有多大区别。但是：CNAME有一个好处就是稳定，就好像一个IP与一个域名的区别。服务商从方便维护的角度，一般也建议用户使用CNAME记录绑定域名的。如果主机使用了双线IP，显然使用CNAME也要方便一些。

A记录也有一些好处，例如可以在输入域名时不用输入WWW.来访问网站哦！从SEO优化角度来看，一些搜索引擎如alex或一些搜索查询工具网站等等则默认是自动去掉WWW.来辨别网站，CNAME记录是必须有如：WWW(别名)前缀的域名，有时候会遇到这样的麻烦，前缀去掉了默认网站无法访问。

## 端口

- 端口号：取值范围是 0 ~ 65535 ，传输层协议通过端口号来区分不同的应用层程序。端口号由 IANA 统一管理，分为知名端口、注册端口和动态端口。
- 知名端口：端口号范围是 0 ~ 1023 ，这些端口用于特定的服务和应用层程序，使客户端应用层程序能够顺利请求服务器的特定服务。
- 注册端口：端口号范围是 1024 ~ 49151 ，这些是分配给终端用户应用层程序的端口号，主要针对用户自行安装的程序，而不是已经拥有了知名端口的应用层程序。当系统中没有任何资源占用这类端口时，客户端就可以在这个范围内动态选择源端口。
- 动态端口：端口号范围是 49152 ~ 65535 ，客户端在开始连接服务器时，会动态选用某个端口做为自己的源端口。
- 套接字：由 IP 地址和端口号组成的格式，能够唯一标识一台终端设备上的一个应用层协议。


# 网络设备

网络硬件（如路由器、交换机、Modem）往往被解释的很复杂，难于理解；稍微简单的方式去解释各个网络硬件的功能

参考：
- [理解几个网络硬件（调制解调器、路由器、交换机）的基本作用](https://blog.csdn.net/pan_tian/article/details/12339629)
- [调制解调器、中继器、集线器、网桥、交换机、路由、网关](https://blog.csdn.net/qingkongyeyue/article/details/52279893)

【2022-4-5】[家庭网络如何通过路由器上网？](https://www.ixigua.com/6962843320791859749)

<iframe width="720" height="405" frameborder="0" src="https://www.ixigua.com/iframe/6962843320791859749?autoplay=0" referrerpolicy="unsafe-url" allowfullscreen></iframe>


## 家庭组网

【2023-4-29】[家庭网络系统规划及布线指南](https://www.zhihu.com/tardis/zm/art/24387774?source_id=1003)


### 实践

【2024-10-4】家庭网络示例
- 光猫接两个小米路由器

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36\&quot; version=\&quot;24.7.16\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;S1AEtxIFkqxAiEACK9mP\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;785\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-1\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;shadow=0;fontColor=#333333;fillColor=#f5f5f5;dashed=1;dashPattern=1 2;strokeWidth=2;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;570\&quot; y=\&quot;77\&quot; width=\&quot;220\&quot; height=\&quot;215\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-2\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontSize=14;fontColor=#333333;strokeWidth=2;strokeColor=#666666;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;jIkvNtb8ANzGyBPoYMIn-3\&quot; target=\&quot;jIkvNtb8ANzGyBPoYMIn-1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-3\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;shadow=1;fontColor=#333333;fillColor=#f5f5f5;dashed=1;dashPattern=1 2;strokeWidth=2;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;315\&quot; y=\&quot;80\&quot; width=\&quot;165\&quot; height=\&quot;210\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-4\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#666666;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;jIkvNtb8ANzGyBPoYMIn-7\&quot; target=\&quot;jIkvNtb8ANzGyBPoYMIn-8\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-5\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#666666;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;jIkvNtb8ANzGyBPoYMIn-7\&quot; target=\&quot;jIkvNtb8ANzGyBPoYMIn-9\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-6\&quot; value=\&quot;有线连接\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=14;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;jIkvNtb8ANzGyBPoYMIn-5\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.6353\&quot; y=\&quot;2\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint y=\&quot;-11\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-7\&quot; value=\&quot;移动光猫&amp;lt;br&amp;gt;cmcc-wqw\&quot; style=\&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;fillColor=#f8cecc;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;60\&quot; y=\&quot;160\&quot; width=\&quot;120\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-8\&quot; value=\&quot;客厅路由器&amp;lt;br&amp;gt;Wang\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;330\&quot; y=\&quot;100\&quot; width=\&quot;120\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-9\&quot; value=\&quot;主卧路由器&amp;lt;br&amp;gt;Wang_main\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;330\&quot; y=\&quot;210\&quot; width=\&quot;120\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-10\&quot; value=\&quot;访问地址&amp;lt;br&amp;gt;192.168.1.1\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;shadow=1;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;90\&quot; y=\&quot;230\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-11\&quot; value=\&quot;访问地址&amp;lt;br&amp;gt;miwifi.com 或 192.168.13.1\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;shadow=1;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;330\&quot; y=\&quot;310\&quot; width=\&quot;160\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-12\&quot; value=\&quot;小米路由器\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;shadow=1;dashed=1;dashPattern=1 2;fontColor=#333333;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;350\&quot; y=\&quot;50\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-13\&quot; value=\&quot;电视\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;shadow=1;dashed=1;dashPattern=1 2;fontSize=14;strokeWidth=1;fillColor=#b0e3e6;strokeColor=#0e8088;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;595\&quot; y=\&quot;87.5\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-14\&quot; value=\&quot;摄像头\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;shadow=1;dashed=1;dashPattern=1 2;fontSize=14;strokeWidth=1;fillColor=#b0e3e6;strokeColor=#0e8088;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;595\&quot; y=\&quot;127.5\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-15\&quot; value=\&quot;冰箱\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;shadow=1;dashed=1;dashPattern=1 2;fontSize=14;strokeWidth=1;fillColor=#b0e3e6;strokeColor=#0e8088;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;595\&quot; y=\&quot;167.5\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-16\&quot; value=\&quot;洗衣机\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;shadow=1;dashed=1;dashPattern=1 2;fontSize=14;strokeWidth=1;fillColor=#b0e3e6;strokeColor=#0e8088;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;595\&quot; y=\&quot;207.5\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-17\&quot; value=\&quot;猫眼\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;shadow=1;dashed=1;dashPattern=1 2;fontSize=14;strokeWidth=1;fillColor=#b0e3e6;strokeColor=#0e8088;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;595\&quot; y=\&quot;247.5\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-18\&quot; value=\&quot;手机\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;shadow=1;dashed=1;dashPattern=1 2;fontSize=14;strokeWidth=1;fillColor=#008a00;strokeColor=#005700;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;690\&quot; y=\&quot;87.5\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-19\&quot; value=\&quot;电脑\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;shadow=1;dashed=1;dashPattern=1 2;fontSize=14;strokeWidth=1;fillColor=#008a00;strokeColor=#005700;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;690\&quot; y=\&quot;127.5\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;jIkvNtb8ANzGyBPoYMIn-20\&quot; value=\&quot;家庭网络路由示例\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;shadow=1;dashed=1;dashPattern=1 2;fontColor=#333333;fontSize=18;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380\&quot; y=\&quot;10\&quot; width=\&quot;150\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



### 中小户型网络架构

家庭组网设备示意图
- ![](https://pic1.zhimg.com/v2-f0c64210bd15b7466bd04a2b869b27fc_b.webp?consumer=ZHI_MENG)

中小户型网络系统，除了电信运营商的**接入设备**（光猫，ADSL猫等）只安装一台主**无线路由器**（即当作路由器使用，又当作交换机使用）
- 如果无线网络覆盖不足，会另外再配一台无线路由器（当作无线AP使用，软件设置成AP功能）或者**无线扩展器**作为无线信号扩展的设备使用，两台无线路由器之间即可以通过**有线**连接也可以通过**无线**桥接的方式连接。

此种网络系统结构非常简单，主要是依赖于无线路由器的品质，现在主流的无线路由器是采用新一代11AC技术，提供2.4GHz、5GHz两个频段信号
- 2.4GHz频段，无线速率可以达到450Mbps；
- 5GHz频段，无线速率可以达到1300Mbps至更高，5GHz频段可接入更多无线终端，干扰少，速度快。

### 大户型网络架构 

大户型网络架构 （满足高清影视等网络需求）
- ![](https://pic3.zhimg.com/v2-a15268ffcb1b720621274ece1fa39002_b.webp?consumer=ZHI_MENG)

大户型的网络系统中，根据各种网络产品的选型，房间网络布线方式，以及资金预算有多种网络架构的变形，以上是最基础的网络架构。
- 路由器，交换机是必备的，为了满足高清影音视频的需求, 整个核心数据交换层全部为**千兆网**络，也为将来的网络带宽需求做好准备。
- 无线网络覆盖采用的是无线路由器，跟中小户型的方案一样除了主路由器外其余无线路由器设置为**无线AP模式**，优点是普通用户采购使用设置比较方便，缺点是稳定性不高，不能无线漫游。

对无线网络比较重视的用户可以采用专业的无线AP做WIFI覆盖，效果及使用体验会高很多。当然如果每个房间都有预留网口，可以使用一种86底盒安装的面板型无线AP。


### 跃层别墅型网络架构 

跃层别墅型网络架构 （满足家用所有的网络需求）
- ![](https://pic3.zhimg.com/v2-14c170c106ca658ed9bac09680bec5be_b.webp?consumer=ZHI_MENG)

跃层别墅型网络系统中，核心网络的出口路由器跟千兆交换机都十分重要，所以一般都采用**企业级**的网络产品，稳定性及性能都比家用级的好很多。
- 无线网络全部采用专业的无线AP进行网络覆盖，通过POE交换机直接用网线供电，安装在吊顶内或空调检修口处，通过AC无线控制器可以统一管理无线AP，实现网络的漫游功能，稳定性也非常高。

## 传播方式

- 单播：一对一的数据发送方式。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/38f21013cb634c06bd61838384fae588?from=pc)
- 组播：通过多个节点共同加入一个感兴趣组，实现一对多的数据发送方式。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/9f1522b2b94f49ee88510b7ad74f2df7?from=pc)

广播域：在这个区域中，各个节点都可以收到其它节点发送的广播数据包。
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/b23e12b874744d9ca9781daf7b0ba2fc?from=pc)

## 线路

双绞线：将两根互相绝缘的导线按一定规格缠绕在一起，以便它们互相冲抵干扰，从而形成的通信介质。
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/cf488fe3b6214cfaa94f309d2942ae3a?from=pc)

光纤：为实现数据通信，利用全反射原理传输光线的玻璃纤维载体。
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/177d678c4303421986cfa5b4fd0e0128?from=pc)


### 网线类型

网线也是有等级区别的。不同等级的网线应用环境不一样。
- `一类`网线：主要用于传输语音（一类标准主要用于八十年代初之前的电话线缆），不同于数据传输
- `二类`网线：传输带宽为1MHZ，用于语音传输和最高传输速率4Mbps的数据传输，常见于使用4Mbps规范令牌传递协议的旧的令牌网（Token Ring）
- `三类`网线：该电缆的传输带宽16MHz，用于语音传输及最高传输速率为10Mbps的数据传输主要用于10BASE--T，被ANSI/TIA-568.C.2作为最低使用等级 。
- `四类`网线：该类电缆的传输带宽为20MHz，用于语音传输和最高传输速率16Mbps的数据传输主要用于基于令牌的局域网和 10BASE-T/100BASE-T。
- `五类`网线：该类电缆增加了绕线密度，传输带宽为100MHz，用于语音传输和最高传输速率为100Mbps的数据传输，主要用于100BASE-T和10BASE-T网络。
- `超五类`网线：具有衰减小，串扰少，比五类线增加了近端串音功率和的测试要求，并且具有更高的衰减串扰比（ACR)和信噪比、更小的时延误差。超五类线的最大带宽为100MHz。
- `六类`网线：该类电缆的传输带宽为250MHz，六类布线系统在200MHz时综合衰减串扰比（PS-ACR）应该有较大的余量，它提供2倍于超五类的带宽。六类布线的传输性能远远高于超五类标准，最适用于传输速率为1Gbps的应用。

选用六类网线以上才是最佳适用于千兆宽带需求。百兆宽带接线时它可以四根线通信。千兆宽带必须是**八根**线通信。接线时可以问问是不是接的八根线，不能接触或接反。因为少接一根线也是可以网络通信，但是达不到网速要求。注意六类网线比普通的网线线粗很多，买的时候不要贪便宜，可不要被人坑了哟。


## 调制解调器 Modem （猫）

**调制解调器**，专业解释是**数模转换器**
- 调制：把计算机的**数字**信号变成**模拟**信号在电话线（电话线只接模拟信号）里通过。
- 解调：电话线里的**模拟**信号变成计算机认识的**数字**信号。


一个家庭最简单的网络部署图。台式机通过Modem，连接到网络服务商，最后连接到Internet。
- `ISP` -> `Modem` -> `PC`
- ![](https://img-blog.csdn.net/20131006101724406?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcGFuX3RpYW4=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

如Modem一种是中兴的ZXV10 H108L ADSL**宽带猫**。猫一般不用自购，多为**网络服务提供商**（中国电信、铁通...）提供，它把计算机的**数字**信号翻译成可沿普通电话线传送的**模拟**信号，然后模拟信号通过 ISP 连接到Internet

现在很多的Modem都具有**路由**功能，允许多台电脑同时上网，但这个路由功能最后都被运营商给封了，电信巴不得你一台电脑一个猫。不过有破解电信猫实现路由功能的方法


## 中继器

简单的**信号放大器**，信号在传输的过程中是要衰减的，中继器的作用就是将信号放大，使信号能传的更远。 

## 集线器（hub）

多个多端口的中继器，把每个输入端口的信号放大再发到别的端口去，集线器可以实现多台计算机之间的互联，因为它有很多的端口，每个口都能连计算机。 

- 冲突域：通过共享媒介连接在一起的设备，共同构成的网络区域。在这个区域内，同时只能一台设备发送数据包。
- **共享型**以太网：所有连网设备处在一个**冲突域**中，需要**竞争**发送资源的以太网环境。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/fd7c73e3565a40359c24d3418ccf632b?from=pc)
- **交换型**以太网：连网设备互相之间不需要竞争发送资源，而是分别与**中心设备**组成点到点连接的以太网环境。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/dde50a04f59f41828e6554f69a3f5cda?from=pc)

## 网桥（局域网间访问）

用集线器组个局域网A，别人用另一个集线器组个局域网网B, 每个局域网里的电脑都能互相访问。但是A里的电脑想访问B里的电脑怎么办，这里就用到网桥了，用网桥来连接2个局域网。如果说集线器是1层设备的话，那么网桥就是2层设备。
- ![](https://img-blog.csdn.net/20160822203349446?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)



## 交换器（高级网桥）

交换机，可以理解为高级的网桥，他有网桥的功能，但性能比网桥强 

一般家用路由器有4个**局域网接口**，超过4个设备要连入网络的话，就要用到**交换机**了。
- `ISP` -> `Modem` -> `Router` -> `Switch`  -> `PC`s (4个以上终端)
- ![](https://img-blog.csdn.net/20131006101845765?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcGFuX3RpYW4=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
- 交换机可以把连入的设备组成一个**小型局域网**，再通过路由器连到外部网络中去。
一个8口交换机，可以连通8台LAN设备
- ![](https://img-blog.csdn.net/20131006101905312?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcGFuX3RpYW4=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

## 路由器 Router

交换机负责每个局域（冲突域）之间的连接，只管转发这些广播，不管广播的合理性以及真实性。但整个网络计算机的数量足够大时，这么多的机器都要广播，那么这些广播信息将占用很大的带宽，造成**网络堵塞**，反而导致正常的通信不能进行，这时候怎么办~~

路由就干这个的，交换机把数据给路由，路由决定是否转发，比交换机智能点。这样能避免过多的广播造成网络堵塞。 现在路由多用在分内外网上

在 Modem 和 终端设备间，增加了（无线）路由器（Router）就可以实现多台电脑同时上网
- `ISP` -> `Modem` -> `Router` -> `PC`s (Desktop+Laptop)
- ![](https://img-blog.csdn.net/20131006101802531?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcGFuX3RpYW4=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


### 路由器构成

路由器 构成: CPU、内存、闪存、功放芯片、PCB、外壳
- ![](https://pic3.zhimg.com/v2-fdaa4d0f0d49fb51b2e74ee3b27d11e0_b.webp?consumer=ZHI_MENG)

说明
- `CPU`：CPU 也有品牌，知名度高，且很多路由器在用的
  - 博通、高通、联发科MTK等，还有中兴、华为的自研产品（不过是自家在用）。
- `内存`：越大越好。
  - 目前最大内存的家用路由器是1G内存的。普通路由器，一般就128MB、256MB，比较大就512MB。
- `闪存`：和内存同理，闪存越大越好。
- `FEM芯片`：分为独立、集成（非独立）两种。独立FEM，在抗干扰上，会比集成好一些，当然，这不绝对。
- 部分CPU，会集成功放（比如MT7622B），或集成内存（比如HI5651L）。

记住：
- CPU：CPU要好，网速上会有影响。
- 内存：越大越好，比如BX54的512MB内存。
- 闪存：越大越好。

### 路由器 vs 交换机

路由器与交换机
- 交换机创建网络：方便同一网络下多台设备互通
- 路由器连接各个网络

> Switches create a network. Routers connect networks. A router links computers to the Internet, so users can share the connection. A router acts as a dispatcher, choosing the best path for information to travel so it's received quickly.

OSI模型上，交换机位于第二层的Datalink层，路由器位于第三层网络层。

- 路由：是指路由器的路由表中用来标识路径信息的条目，也指路由器利用路由条目转发数据的操作。
  - ![img](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/5b9394523ca54f9c97c3bc38147f5ccc?from=pc)
- 路由表：路由设备中用来存放路由条目的数据表，路由设备依据路由表中的信息进行转发判断。
- 路由协议：定义路由设备之间如何交换路径信息、交换何种信息，以及路由设备如何根据这些信息计算出去往各个网络最佳路径等选路操作相关事项的协议。

很多家用网络设备都兼具多项功能，如图里的路由器既有路由器功能也具有交换机的功能，路由功能联通内部局域网和外部的Internet网络，还有交换机的功能，可以在内网中联通多台设备。
-  TP-LINK TL-WR541G+ 54M无线路由器，含有4个10/100M局域网接口，无线网络速率可达到54Mb/s

【2022-4-5】[交换器和路由器区别](https://www.ixigua.com/6960673453431226893)

<iframe width="720" height="405" frameborder="0" src="https://www.ixigua.com/iframe/6960673453431226893?autoplay=0" referrerpolicy="unsafe-url" allowfullscreen></iframe>


### 路由器5G、2.4G区别

频段分为 **高频**的`5G` 和 **低频** `2.4G`。

信号覆盖范围上：`2.4G` ＞ `5G`
- `5G` 高频波长短，穿透性差。5G信号好，但覆盖范围小。
- `2.4G` 低频波长长，穿透性好。2.4G覆盖范围大。但使用2.4G频段的东西太多，也最容易被干扰（这就是一些家庭，宽带好，但网络差的原因之一）。


### 路由器品牌

常见品牌
- 主要做**高端**：华硕、网件。
- 中端、高端都不错的：H3c、华为、小米，
- 全方位覆盖的：TP、水星、腾达、中兴。

避坑：别买那些电商品牌、浏览器品牌路由器。

![](https://pica.zhimg.com/v2-71f1b3db27890b39f4d7fc989ab6d60c_b.webp?consumer=ZHI_MENG)


[路由器性价比推荐](https://www.zhihu.com/tardis/zm/art/465563915)

### WAN/LAN/WLAN

一般路由器的LAN口用颜色和WAN口区分，一般LAN口数目会多于WAN口。

- （1）`LAN` 全称Local Area Network，中文名叫**局域网**
  - LAN是指在某一区域内由多台计算机互联成的计算机组。一般是方圆几千米以内。局域网可以实现文件管理、应用软件共享、打印机共享、工作组内的日程安排、电子邮件和传真通信服务等功能。局域网是封闭型的，可以由办公室内的两台计算机组成，也可以由一个公司内的上千台计算机组成。
  - ![](https://imgsa.baidu.com/exp/w=500/sign=d37b5af8ed24b899de3c79385e071d59/d6ca7bcb0a46f21f454a2eabf2246b600d33aec8.jpg)
  - 路由器组网一般组建的都是LAN网络，用户在局域网里通信、传输文件。获取到的是内部IP，LAN 内部是交换机。可以不连接 WAN 口，把路由器当做普通交换机来使用
  - LAN的场景：
    - 1，接电脑的网线，需要插到路由器的LAN口
    - 2，二级路由，一般都是从上级路由的LAN口接线
    - ![](https://imgsa.baidu.com/exp/w=500/sign=a94d08c06a061d957d4637384bf50a5d/bf096b63f6246b600c7fc38ceff81a4c500fa2d0.jpg)
- （2）`WAN` 全称Wide Area Network，中文名叫**广域网**
  - WAN是一种跨越大的、地域性的计算机网络的集合。通常跨越省、市，甚至一个国家。广域网包括大大小小不同的子网，子网可以是局域网，也可以是小型的广域网。
  - ![](https://imgsa.baidu.com/exp/w=500/sign=2518c479cf1349547e1ee864664f92dd/cc11728b4710b912b33b8a06c7fdfc039345224b.jpg)
  - WAN：接外部 IP 地址用，通常指的是出口，转发来自内部 LAN 接口的 IP 数据包。
  - 基本每个路由器都有WAN口，当然也有路由猫这种特例。
  - 一般路由器都会有一个WAN口，也有多个WAN口的路由。
    - ![](https://imgsa.baidu.com/exp/w=500/sign=2eff9eaa8135e5dd902ca5df46c7a7f5/bd3eb13533fa828bc723e31bf91f4134960a5ac1.jpg)
  - WAN的应用场景：
    - 1，从猫引出的来网线，要插到路由器的WAN口
    - 2，二级路由，上级网线插到二级路由的WAN口
    - ![](https://imgsa.baidu.com/exp/w=500/sign=9426515d0e7b02080cc93fe152d8f25f/f7246b600c33874411d85684550fd9f9d72aa02d.jpg)
- （3）`WLAN` 全称Wireless LAN, **无线**局域网。
  - 和LAN不同，WLAN的数据通过电磁波传输，也就是常说的空气传输。WLAN 利用电磁波在空气中发送和接受数据，而无需线缆介质。
  - WLAN 使用 ISM (Industrial、Scientific、Medical) 无线电广播频段通信。WLAN 的 802.11a 标准使用 5 GHz 频段，支持的最大速度为 54 Mbps，而 802.11b 和 802.11g 标准使用 2.4 GHz 频段，分别支持最大 11 Mbps 和 54 Mbps 的速度。最新的11AC已经达到竟然的1.3Gbps。由于WLAN采用全新的802.11协议，其设置要比普通的有线路由器复杂
  - ![](https://imgsa.baidu.com/exp/w=500/sign=8ebddcdbb47eca80120539e7a1229712/a6efce1b9d16fdfa93fdbc16b08f8c5495ee7bb0.jpg)
总结：
- WAN口是对外的接口，和运营商、上级网络打交道。
- LAN和WLAN是对内的接口，内部的电脑、手机、PAD，都是接入到LAN或者WLAN。
一般的无线路由器，包含了完整的LAN、WAN、WLAN功能。
- ![](https://imgsa.baidu.com/exp/w=500/sign=198ca5d7ba096b6381195e503c318733/96dda144ad345982a17d876a08f431adcaef8456.jpg)
- 参考：[路由器的LAN、WAN、WLAN的区别](https://www.cnblogs.com/Renyi-Fan/p/8092521.html)


路由器WAN口和LAN口的区别
- WAN口主要用于连接**外部**网络，如ADSL、DDN、以太网等各种接入线路;
- LAN口用来连接家庭**内部**网络，主要与家庭网络中的交换机、集线器或PC相连。
可以说这两类网口一类对外，一类对内。将网络运营商提供的接入网线插在WAN口上，然后将几台共享上网的电脑接到LAN口上，然后用一台电脑登录路由器的管理界面进行相应的配置即可完成共享上网了。

## 网关

- 局域网里，集线器就是网关
- 2层网络里，交换机就是网关
- 3层网络里路由就是网关
- 说网关要看你的网是多大的，要拿中国来说，连着美国那台世界服务器的设备就是网关
- ![](https://img-blog.csdn.net/20160822203418755?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)


## AP 应用接入点

`无线AP`（Access Point）：即**无线接入点**，它用于无线网络的**无线交换机**，也是无线网络的**核心**。
- 无线AP是移动计算机用户进入**有线**网络的接入点，主要用于宽带家庭、大楼内部以及园区内部，可以覆盖几十米至上百米。
- 无线AP（又称会话点或存取桥接器）是一个包含很广的名称，它不仅包含单纯性无线接入点（无线AP），同样也是无线路由器（含无线网关、无线网桥）等类设备的统称。

【2022-2-21】案例：办公室1-2排局部断网，其它工位正常；挪动下笔记本位置，重新接入公司wifi后，再回到原工位就恢复正常→工位边上ap坏了

### 无线AP

**无线接入点**（AP）：电信级无线覆盖设备，相当于一个连接**有线网**和**无线网**的**桥**，其主要作用是将各个无线网络客户端连接到一起，实现大范围、多用户的无线接，根据应用场景不同，AP通常可分为**室内型**和**室外型**，室内环境下覆盖范围通常在30米~100米，室外环境最大覆盖范围可达到800米。

### AC控制器

接入控制器（AC）：无线局域网接入控制设备，负责将来自不同AP的数据进行汇聚并接入Interne，同时完成AP设备的配置管理和无线用户的认证、管理，以及带宽、访问、切换、安全等控制功能。

AC强大的管理和控制功能，能够构建出个性化、专业化的WLAN解决方案。

### 无线瘦AP

“瘦”AP：无线接入点也称无线网桥、无线网关。此无线设备的传输机制相当于有线网络中的集线器，在无线局域网中不停地接收和传送数据；任何一台装有无线网卡的PC均可通过AP来分享有线局域网络甚至广域网络的资源。理论上，当网络中增加一个无线AP之后，即可成倍地扩展网络覆盖直径；还可使网络中容纳更多的网络设备。每个无线AP基本上都拥有一个以太网接口，用于实现无线与有线的连接。

### 无线胖AP

胖AP：其学名应该称之为无线路由器。一般具备WAN、LAN两个接口，多支持DHCP服务器、DNS和MAC地址克隆，以及VPN接入、防火墙等安全功能。

### 胖瘦AP比较

胖AP是单个独立可以管理的无线AP。瘦AP就必须配合**无线控制器**使用！瘦AP本身是没有管理能力的！只能通过控制器才具备胖AP的功能！失去控制器将无法正常使用！胖瘦一体AP是具有单个管理也可以用AC控制器统一管理。

### WLAN演进：胖AP到瘦AP

最早的WLAN设备，将多种功能集为一身，如：物理层、链路层、用户数据加密、用户的认证、QoS、安全策略、用户 的管理及其他应用层功能集为一体，传统将这类WLAN设备俗称为“胖”AP。

“胖”AP的特点是配置灵活、安装简单、性价比高，但AP之间相互独立，无法适合用户密度高、多个AP连续覆盖等环境复杂的场所。

为此产生集中控制型**AC+AP设备**，通过集中控制器AC和轻量级AP配合，实现“胖”AP设备的功能。其中，轻量级AP只保留物理链路层和 MAC功能，提供可靠、高性能的射频管理，包括802.11协议的无线连接；集中控制器AC集中所有的上层功能，包括安全、控制和管理等功能，与传统的 AP相比，轻量级AP实现的功能大大减弱，故俗称为“瘦”AP。

### 吸顶式无线AP

YA-3030大功率吸顶式无线AP，采用MIMO、OFDM、SDM、GI等技术，是基于IEEE 802.11n技术标准的无线接入设备，内置2*2MIMO双极化全向智能天线，超强无线传输性能，传输速率自适应，最高可达300M，覆盖更广，信号更强、更稳定。可广泛应用于酒店、商场、KTV、会议室、咖啡厅等娱乐场所无线WIFI网络覆盖。


## wifi


###  WiFi 协议

目前主流 WiFi协议：802.11n、802.11ac(wave1、wave2)、802.11ax 。

这样的命名方式对外行难以理解。

2018年，WiFi联盟正式将 802.11ax 标准定为 第六代 WiFi技术，同时开启了WiFi协议命名简化的时代。

此前对于外行较为生涩的WiFi协议名称将变成更易理解的简化版本。

具体来说：
- `802.11n` 变成 Wi-Fi 4
- `802.11ac` 变成 Wi-Fi 5
  - 2013年发布（16年发布了支持160Mhz的Wave2）
- `802.11ax` 变成 Wi-Fi 6
  - 2018年发布。
  - WiFi6 相比 WiFi5，有更大的带宽、并行量，降低了延迟。速度更快、更稳定。
- `802.11be` 变成 Wi-Fi 7
  - 在 Wi-Fi 6 和 Wi-Fi 6E 的基础上，因为4096QAM、320MHz，以及最大空间流达到了16×16，相对于Wifi6直接翻倍，使其带宽更高（提升20%以上）、有更低的延迟，在高端WiFi7路由器上，理论覆盖更高。
  - 另外，现在多数 Wifi6 路由器的Mesh功能，因为WiFi7的改进，可以在网络切换时，更丝滑，理论能做到更好的“无缝切换”。

WiFi理论速率：
- WiFi 4 单流：150Mbps，4流：600 Mpbs
- WiFi 5 单流：433Mbps，8流：3466 Mpbs （wave2 版本，867 Mbps，8流：6933 Mpbs）
- WiFi 6 单流：1200Mbps，8流：9.6 Gpbs

[原文链接](https://blog.csdn.net/u012247418/article/details/134861037)


【2024-10-16】荣耀手机能显示wifi协议类型，华为 mate 30不行



### 查看wifi密码

mac环境： [如何查看Mac上已连接WiFi的密码？](https://zhuanlan.zhihu.com/p/104847180)
- 打开“钥匙串访问”，在其左侧的“钥匙串”列表中选择“系统”，右侧栏就会出现与系统有关的各类密钥。
- 找到你需要连接的WiFi名称，右击，选择“将密码拷贝到剪贴板”

Windows环境

```shell
netsh wlan show profiles # 查看连接过的wifi
netsh wlan show profiles name ＝ “当前用户配置文件名” key ＝ clear # 查看wifi密码
# “安全设置”—>“安全密钥”
```


## 网速

### 千兆网

**千兆网**线就是 1000Mbps。换算成电脑的Bp/s（8b=1B. 1K=1024B ,1M=1024K.）那么(1000/8)=**125**MBps.

中移动[千兆宽带测速注意事项](http://service.bj.10086.cn/m/mbjyd/kdzz/page2.html), [img](http://service.bj.10086.cn/m/mbjyd/kdzz/images/pic2-1.jpg)
- ![](http://service.bj.10086.cn/m/mbjyd/kdzz/images/pic2-1.jpg)

如何才能真正享受到千兆的网络体验呢?
- 关键点1  务必使用**超五类**规格以上**网线**
  - 网线必须是带有“CAT5E”标识的超五类及以上规格网线，此外还有“CAT 6”“CAT 6E”，此类规格网线的传输速率为1000Mbps（也就是1Gbps）。
- 关键点2  务必使用**六类水晶头**
  - 六类水晶头用于千兆网络，因为使用的铜芯较粗（裸铜丝直径为0.573毫米），因此六类水晶头是错层排列。五类水晶头常用于百兆网络，铜芯较细（裸铜丝直径为0.511毫米），因此采用直线排列。
- 关键点3  务必网线接光猫**千兆口**
  - 核实网线是否接的是LAN1千兆口，如果不是，请务必更换接口，插入LAN1千兆口，直接插拔即可。
- 关键点4  务必保证**路由器**支持1000M速率
  - 路由器的转发性能受限于端口的连接速率，百兆路由器转发性能只能达到百兆，1000M的宽带务必使用千兆路由器，可以最大限度发挥出宽带的性能。
- 关键点5  务必保证**终端和配置属性**支持千兆
  - 最常用的电脑，网卡是否支持千兆，网卡是否协商为千兆。
  - PC的电源计划选项设置为高性能，以便支持千兆性能。
- 关键点6  务必**测速软件**服务器使用正确
  - 使用测速软件进行测速时，确保测速点服务器选择北京移动服务器，以SPEEDTEST测速为例，若选择其他省份或运营商服务器站点会导致测速效果不理想。

温馨提示
- 1、电脑或测试终端在测速前须**关闭视频、下载、聊天等**消耗背景流量的应用软件等等；
- 2、WIFI连接路由器或光猫时，使用5.8GHz测速效果优于2.4GHz，但5.8GHz wifi无线下载速率实测一般不超过500Mbps。
- 3、电脑终端要求：千兆网卡、CPU为四核，主频3.0GHZ以上、内存8G以上，用户硬盘最好是ssd（固态硬盘），写入速率能力大于40MB/s。若使用笔记本电脑测速，必须连接充电器并将电源模式调整为高性能模式。

基于以上关键点，强烈建议使用网线接入进行网速测试，来保证达到最好的网络体验。


### 网速测试

【2023-4-29】知乎帖子：[如何测速](https://www.zhihu.com/question/19763656/answer/2531097741)？
- [测速网](https://www.speedtest.cn/)
  - 千兆网实测：下载**75.68**/Mbps，上传**85.81**/Mbps
- [广东电信宽带测速平台](https://10000.gd.cn/?6ylpqNiaaakM=1682745258473#/speed)，支持视频测试。
  - 下载 88.88 Mbps， 上传 53.42 Mbps


### 网吧电脑为什么快

【2021-12-16】[网吧网咖的电脑配置比家里的低，为什么速度却更快？](https://zhuanlan.zhihu.com/p/374210363)
- （1）**操作系统优化**：网吧的电脑系统十分**精简**，并且系统还是优化过的。很多用户从安装好系统后一直使用的都是系统默认设置。而网吧里的电脑，都开启了最佳性能模式。
- （2）**软件少**：电脑里面也没有安装过多的软件、没有自启动程序和多余的进程。只留下与游戏、直播、观影有关的软件。**后台程序**少了很多，减轻不少系统运行占用的资源，自然运行速度就快一些了。
- （3）**服务器**镜像：网吧系统的“还原功能”, 用户每次开机都是全新的**镜像**启动，进入的是干干净净的新系统。这就是为什么，出现问题的时候，网管通常会叫你“重启试试”，直接搞一个全新的系统使用，自然也就没有问题了~
- （4）**光纤通信**：家里装的无线一般只供一台电脑或者是供手机使用就足够了，基本都是100兆左右。但是网吧里的网几乎都是千兆网或者是几万兆的网。
- （5）**无硬盘**：电脑是必须从硬盘上读取数据的。但网吧电脑大多数不用硬盘，因为它有“**无盘服务器**”，类似于固态硬盘的作用。电脑由网卡唤醒后，直接加载“无盘服务器”里的镜像系统启动，包括启动软件和游戏时也一样。那么，在网吧的千兆网光纤组成的局域网下，从服务器读取数据的速度肯定是高于硬盘的。虽然网吧电脑配置不一定比得上你的电脑，但是在游戏场所中，还是会备配一些中高性能cpu显卡，比如NVIDIA特供的GTX 1063。
- ![](https://pic3.zhimg.com/80/v2-e8c4fcbde4137bb40a39b988f460b1e2_1440w.jpg)

## 如何连接两个路由器

[如何连接两个路由器](https://zhuanlan.zhihu.com/p/32274871)

### 方法1：使用以太网连接两个路由器

设置主路由、副路由
- 主路由器将直接与调制解调器连接
- 副路由器主要用于拓展网络信号。可以选择旧型号的路由器作为附属路由器。此外，如果要创建LAN-to-WAN网络，该路由器还将控制附属网络。

LAN-to-LAN或LAN-to-WAN网络连接方式
- LAN-to-LAN（局域网）连接方式可以**扩展网络**，允许更多设备连接到网络中。每个设备都可以访问网络中其他设备共享的文件和资源。
  - 用DHCP服务的默认设置。
- LAN-to-WAN（广域网）连接方式在主网络（WAN）中创建一个**子局域网**。优点是可以对子网中的设备访问设定一定限制，而缺点是子网中的设备无法与主网络共享文件和资源。
  - 该模式下，可以修改子局域网的DNS设置，从而限制子网中设备能够访问的网站。此外，子网中的设备也更安全，黑客访问它们也会更加困难。因此家长可以用此来监控孩子访问互联网。
  - 开启主路由器的DHCP服务，自动分配192.168.1.2与192.168.1.50之间的IP地址。



## 为什么颜色网站会卡顿

【2022-10-5】[为什么你在进入学习网站的时候总会卡一下](https://www.toutiao.com/video/7137983408562556198/)，站点打开后，往往会停顿一段时间才弹出界面，大部人以为只是网页卡顿原因，毕竟裤子都脱了不在乎这点时间，导致成千上万人身体倍榨干的同时还帮黑客赚了钱
- 只是为了赚取一点广告费吗？那就太天真了，很多颜色网站会内置挖矿程序，植入js脚本，这样做的不只是颜色网站，还有免费电影、小说网站，只要进入此类网站，js脚本就会自动执行，占用大量CPU资源，挖取大量虚拟币，使电脑卡顿发热


## 下载

【2023-7-5】[2023年5个好用的 BT/ 磁力链接下载工具推荐](https://kejileida.net/4971)

### 种子（BitTorrent）

#### 种子文件

种子文件（BitTorrent）是什么？
- BitTorrent 协议（简称`BT`，俗称`比特洪流`、BT下载、种子）是用在对等网络中文件分享的网络协议程序。

一种电脑“.torrent”文件。装有BT（BitTorrent）下载必须的文件信息，作用相当于HTTP下载里的URL链接。

一个用户要利用BitTorrent协议下载文件之前，先要从某个网站下载一个包含该文件相关信息的“.torrent”文件。

种子是一个形象的比喻。

#### BT下载原理

BT下载原理
- 像春天种下一粒种子，到了秋天就会收获万粒稻菽一样的滚雪球般的越来越大。于是把发出的下载文件叫做**种子**。
- 而种子文件就是记载下载文件的存放位置、大小、下载服务器的地址、发布者的地址等数据的一个索引文件。

种子文件并不是最终要下载的东西（如电影，软件等等），但是有了种子文件，就能高速下载到文件。种子文件的扩展名是：`*.torrent`。

当拿到一个BT种子，首先意味着拿到了BT资源的文件信息——就如同怎样的种子就会种出怎样的树，文件信息决定了会下载到苍老师还是葫芦娃。同时，BT种子还包含了Tracker信息，用以告诉你BT下载需要走哪个Tracker，也就是“服务器” —— 没错，利用BT种子来进行下载，还是得先走服务器这个流程。用BT种子下载，需要服务器先告诉你其他用户的IP，才能开始数据传输。在这种情况下玩BT，尽管也是P2P下载，但仍然离不开服务器。

2009年著名BT下载站“BTChina”被查水表。
- 随BTChina倒下的不仅仅有一票BT资源站，还有无数的Tracker服务器，这直接导致很多BT种子成为了**死种**。
- 直到现在，有经验的老司机在找旧资源的时候，如果看到资源是BT种子，很有可能会直接放弃 —— 除非迅雷、百度云之类的离线下载服务器有缓存相应资源，不然这种子基本就是摆设；而离线下载的和谐力度，大家都懂的。死种、离线和谐都见证了下载中央服务器的脆弱，人们急需续命能力更强的下载方式。

历史的进程，就悄然走到了`磁力链接`的身旁。

### 磁力链接

磁力链接（Magnet URI scheme）是什么？
- `磁力链接`（Magnet URI scheme）是一种特殊链接，但与传统基于文件位置或名称的普通链接不一样，它只是通过不同文件内容的**Hash结果**生成一个纯文本的“**数字指纹**”，并用它来识别文件。

类似于生活消费品包装上常见的**条码**，不同的是这个“数字指纹”可以被任何人从任何文件上生成，这也就注定了“磁力链接”不需要任何“中心机构”的支持（例如：BT Tracker服务器），且识别准确度极高。

#### 磁力下载原理

BT种子的死穴在于**Tracker服务器**。其实BT下载资源本身就不由服务器提供，服务器提供的只是P2P参与者的信息。

那么能不能跳过Tracker这一步，直接连接其他用户进行P2P？磁力链接就可以做到这一点。

一般人看到磁力链接，看到的是不明所以的神秘代码，但这神秘代码，其实可以包含很多信息。磁链包含了文件信息，这自然不必说。磁力链接的文件信息的组合很灵活，不过必须的就一个Hash码。除此以外，磁力链接还可以包含Tracker地址、DHT节点等信息，但无论如何，必须的仍就只有一个Hash码。

磁力链接是一脚踢开了服务器！你在网上看到一串Hash码，直接在前面加上“ magnet:?xt=urn:btih: ”，就能生成一个可用的磁力链接，下载到Hash码对应的文件了。显然，磁力链接对比BT种子，优势是显而易见的，这体现在以下方面：
- 传播方便。作为一串文字，磁力链接显然比BT种子更容易传播，粘贴一段文字可比上传一个文件省时省力多了。
- 便于储存整理。如果你拥有很多很多磁力链接，你可以把它们都放到一个文档或者表格中，整理得井井有条。很多资源站放种子合集，也可以轻易贴出满满一网页的磁力链接。而BT种子作为文件，就没有这么方便了。
- 易于生成。当你看到网友有某个好资源，只要问对面生成一下该文件的Hash码，就能够制作一个磁力链接了，不需要辛辛苦苦把BT种子给翻出来。
- 资源存活力强。磁力链接不需要Tracker服务器，直连DHT网络。只要仍有用户在做种，资源就仍然存活。

类似【magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C】这样以“magnet:?”开头的字符串，就是一条“磁力链接”，其在网页上的图标像一块磁铁，很容易辨别。

#### 磁力下载软件

几个磁力下载软件都可以完美替代迅雷下载。
- Motrix 一款高颜值的下载工具。[官方网站](https://motrix.app)
  - 系统：Windows、macOS、linux
  - 支持：HTTP, FTP, BitTorrent, Magnet, etc.
- FDM – Free Download Manager
  - [官方网站](https://www.freedownloadmanager.org/zh)
  - 系统：Windows、macOS、安卓、Linux
  - 支持：HTTP, FTP, BitTorrent, Magnet, etc.
- qbittorrent
  - [官方网站](https://www.qbittorrent.org)
  - 系统：Windows、macOS、安卓、Linux
  - 支持：HTTP, FTP, BitTorrent, Magnet, etc.
- uTottent
  - [官方网站](https://www.qbittorrent.org)
  - 系统：Windows、macOS、安卓、Linux
  - 支持：HTTP, FTP, BitTorrent, Magnet, etc.
- Bitcomet 比特彗星
  - [官网地址](https://www.bitcomet.com/en)
  - 系统：Windows 、macOS 、安卓
  - 支持：HTTP, FTP, BitTorrent, Magnet, etc.

iOS 系统 / iPhone 上有什么好用的 BT / 磁力链接下载工具吗？
- 没有。由于苹果公司的政策不允许BT / 磁力链接下载工具上架，所以你目前能看到宣称iOS版BT / 磁力链接下载工具毫无例外都涉及虚假宣传。
- iOS 迅雷测试版和袋鼠下载，同样如此，仅仅只是虚假宣传而已，不要再去下载他们的软件以及关注他们的公众号，浪费自己的时间。
- iOS 用户想要使用磁力链接下载只能使用“曲线救国”的方案，例如通过 [PikPak 在线网盘](https://kejileida.net/4700)进行，或者其他第三方在线网站 Bitport 等网站进行，再保存到本地。

### 云盘

【2025-2-21】 [油小猴](https://www.youxiaohou.com/zh-cn/assistant.html)

云盘下载受限，怎么办？
- 百度云盘，网页版下载时，60m文件必须安装百度云客户端才行
- 客户端安装后，非会员还会限制下载速度

如何突破限制？
- 浏览器安装扩展工具: 
  - 如 [纂改猴](https://www.crxsoso.com/webstore/detail/dhdgffkkebhmkfjojejmpbldmpobfkfo), 即原来的油猴,
  - [纂改猴测试版](https://www.crxsoso.com/webstore/detail/gcalenpjmijncebpfijmoaglllgpjagf)
  - 各个浏览器对应的油猴插件[地址](https://www.youxiaohou.com/zh-cn/windows.html#_1-%E5%AE%89%E8%A3%85%E8%84%9A%E6%9C%AC%E7%AE%A1%E7%90%86%E5%99%A8)
- 安装[网盘直链下载助手](https://www.youxiaohou.com/install.html)
- 刷新网盘文件页面，出现新的“下载助手”
- 点击其中1个下载选项，如 “API下载”
  - 初次使用时，会弹窗，提示关注微信公众号，获取开源协议码 （如 AGPL3 ），输入即可
  - 提示要将文件转存到自己的网盘
- API 下载: 适用于 IDM，NDM 以及浏览器自带下载
- 安装 [IDM](https://www.youxiaohou.com/zh-cn/idm.html) 插件 (多线程下载工具)
  - 故障: 未发现IDM，使用自带浏览器下载
  - 解决: [idm无法集成到谷歌浏览器怎么解决](https://zhuanlan.zhihu.com/p/451594614)

实践：
- Chrome 插件下载失败
- IDM 客户端下载部分失败
- 提交官方 [IDM无法唤起，无法下载](https://github.com/syhyz1990/baiduyun/issues/447)


#### 油猴

Tampermonkey，俗称“油猴”，中文名“篡改猴”，是一款免费的浏览器扩展和最为流行的用户脚本管理器。



# 网络协议

网络协议：为在网络中传输数据而对数据定义的一系列标准或规则。
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/f70d8dd274b447c19b71efb49a721f65?from=pc)

## OSI

为规范和定义通信网络，将通信功能按照逻辑分为不同功能层级的概念模型，分为 7 层。
- 计算机网络里的 **OSI七层模型** 或 **TCP/IP五层模型**，即应用层（应用层、表示层、会话层）、传输层、网络层、数据链路层、物理层，简称：<font color='red'>应表会传网数物</font>
- ![](https://pic4.zhimg.com/50/v2-6531ff0d8cbf967211297ef7c7813ab1_hd.jpg)

- [OSI七层模型](https://www.toutiao.com/w/a1701287080764423/)
  - ![](https://p5.toutiaoimg.com/img/tos-cn-i-0022/d2916c97afc94b9daa01bdaca34759a0~tplv-obj:1575:2227.image?from=post)


## TCP/IP

TCP/IP 模型：也叫做**互联网协议栈**，是目前互联网所使用的通信模型，由 TCP 协议和 IP 协议的规范发展而来，分为 4 层
- 由OSI精简而来，应用层包含了OSI模型的应用层、表示层和会话层，网络接入层包含了物理层和数据链路层
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/27bb2de59f754ba4b32509c4dfe09ca7?from=pc)

TCP/IP 是互联网相关的各类协议族的总称，比如：TCP，UDP，IP，FTP，HTTP，ICMP，SMTP 等都属于 TCP/IP 族内的协议。

TCP/IP模型是互联网的基础，它是一系列网络协议的总称。这些协议可以划分为四层，分别为链路层、网络层、传输层和应用层。
- 链路层：负责封装和解封装IP报文，发送和接受ARP/RARP报文等。
- 网络层：负责路由以及把分组报文发送给目标网络或主机。
- 传输层：负责对报文进行分组和重组，并以TCP或UDP协议格式封装报文。
- 应用层：负责向用户提供应用程序，比如HTTP、FTP、Telnet、DNS、SMTP等。

详解
- 应用层：指 OSI 模型的第 7 层，也是 TCP/IP 模型的第 4 层，是离用户最近的一层，用户通过应用软件和这一层进行交互。理论上，在 TCP/IP 模型中，应用层也包含了 OSI 模型中的表示层和会话层的功能。但表示层和会话层的实用性不强，应用层在两种模型中区别不大。
  - 应用协议：电子邮件协议、远程登录协议、文件传输协议
- 传输层：指 OSI 模型的第 4 层，也是 TCP/IP 模型的第 3 层，在两个模型中区别不大，负责规范数据传输的功能和流程。
- 网络层：指 OSI 模型的第 3 层，这一层是规范如何将数据从源设备转发到目的设备。
- 数据链路层：OSI 模型的第 2 层，规范在直连节点或同一个局域网中的节点之间，如何实现数据传输。另外，这一层也负责检测和纠正物理层在传输数据过程中造成的错误。
  - 数据帧：经过数据链路层协议封装后的数据。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/b2655db145564181b815eb00fefdae31?from=pc)
- 物理层：OSI 模型的第 1 层，这一层的服务是规范物理传输的相关标准，实现信号在两个设备之间进行传输。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/45a14a1b8e4d4d99bea0c482147d3749?from=pc)

[一条视频讲清楚TCP协议与UDP协议-什么是三次握手与四次挥手](https://www.ixigua.com/6965440376727732739)

<iframe width="720" height="405" frameborder="0" src="https://www.ixigua.com/iframe/6965440376727732739?autoplay=0" referrerpolicy="unsafe-url" allowfullscreen></iframe>


## 发送过程

- 封装：发送方设备按照协议标准定义的格式及相关参数添加到转发数据上，来保障通信各方执行协议标准的操作。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/35f27ee633694dac875aa7567d90a301?from=pc)
- 解封装：接收方设备拆除发送方设备封装的数据，还原转发数据的操作。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/592ae695ae3a4475a6b5ac8cc23c36cb?from=pc)
- 头部：按照协议定义的格式封装在数据上的协议功能数据和参数。


## TCP

当一台计算机想要与另一台计算机通讯时，两台计算机之间的通信需要畅通且可靠，这样才能保证正确收发数据。例如，当你想查看网页或查看电子邮件时，希望完整且按顺序查看网页，而不丢失任何内容。当你下载文件时，希望获得的是完整的文件，而不仅仅是文件的一部分，因为如果数据丢失或乱序，都不是你希望得到的结果，于是就用到了TCP。

TCP协议全称是传输控制协议是一种面向连接的、可靠的、基于字节流的传输层通信协议，由 IETF 的RFC 793定义。TCP 是面向连接的、可靠的流协议。流就是指不间断的数据结构，你可以把它想象成排水管中的水流。

1. TCP连接过程 （三次握手）
  - 建立一个TCP连接的过程为（三次握手的过程）:
  - 第一次握手: 客户端向服务端发送连接请求报文段。该报文段中包含自身的数据通讯初始序号。请求发送后，客户端便进入 SYN-SENT 状态。
  - 第二次握手: 服务端收到连接请求报文段后，如果同意连接，则会发送一个应答，该应答中也会包含自身的数据通讯初始序号，发送完成后便进入 SYN-RECEIVED 状态。
  - 第三次握手: 当客户端收到连接同意的应答后，还要向服务端发送一个确认报文。客户端发完这个报文段后便进入 ESTABLISHED 状态，服务端收到这个应答后也进入 ESTABLISHED 状态，此时连接建立成功。
  - 疑惑：为什么 TCP 建立连接需要三次握手，而不是两次？这是因为这是为了防止出现失效的连接请求报文段被服务端接收的情况，从而产生错误。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/7543339b7f8d4465bb7bb580110861bb?from=pc)
1. TCP断开链接 （四次握手）
  - TCP 是全双工的，在断开连接时两端都需要发送 FIN 和 ACK。
  - 第一次挥手: 若客户端 A 认为数据发送完成，则它需要向服务端 B 发送连接释放请求。
  - 第二次挥手: 收到连接释放请求后，会告诉应用层要释放 TCP 链接。然后会发送 ACK 包，并进入 CLOSE_WAIT 状态，此时表明 A 到 B 的连接已经释放，不再接收 A 发的数据了。但是因为 TCP 连接是双向的，所以 B 仍旧可以发送数据给 A。
  - 第三次挥手: 如果此时还有没发完的数据会继续发送，完毕后会向 A 发送连接释放请求，然后 B 便进入 LAST-ACK 状态。
  - 第四次挥手: 收到释放请求后，向 B 发送确认应答，此时 A 进入 TIME-WAIT 状态。该状态会持续 2MSL（最大段生存期，指报文段在网络中生存的时间，超时会被抛弃） 时间，若该时间段内没有 B 的重发请求的话，就进入 CLOSED 状态。当 B 收到确认应答后，也便进入 CLOSED 状态。
1. TCP协议的特点
  - 面向连接: 面向连接，是指发送数据之前必须在两端建立连接。建立连接的方法是“三次握手”，这样能建立可靠的连接。建立连接，是为数据的可靠传输打下了基础。
  - 仅支持单播传输: 每条TCP传输连接只能有两个端点，只能进行点对点的数据传输，不支持多播和广播传输方式。 
  - 面向字节流: TCP不像UDP一样那样一个个报文独立地传输，而是在不保留报文边界的情况下以字节流方式进行传输。 
  - 可靠传输: 对于可靠传输，判断丢包，误码靠的是TCP的段编号以及确认号。TCP为了保证报文传输的可靠，就给每个包一个序号，同时序号也保证了传送到接收端实体的包的按序接收。然后接收端实体对已成功收到的字节发回一个相应的确认(ACK)；如果发送端实体在合理的往返时延(RTT)内未收到确认，那么对应的数据（假设丢失了）将会被重传。
  - 提供拥塞控制: 当网络出现拥塞的时候，TCP能够减小向网络注入数据的速率和数量，缓解拥塞
  - TCP提供全双工通信: TCP允许通信双方的应用程序在任何时候都能发送数据，因为TCP连接的两端都设有缓存，用来临时存放双向通信的数据。当然，TCP可以立即发送一个数据段，也可以缓存一段时间以便一次发送更多的数据段（最大的数据段大小取决于MSS）
- ![动图](https://img-blog.csdnimg.cn/img_convert/5ea0a4193a17109528644ebac51a8b40.gif)



## UDP

UDP协议全称是用户数据报协议，在网络中它与TCP协议一样用于处理数据包，是一种无连接的协议。在OSI模型中，在第四层——传输层，处于IP协议的上一层。UDP有不提供数据包分组、组装和不能对数据包进行排序的缺点，也就是说，当报文发送之后，是无法得知其是否安全完整到达的。

它有以下几个特点：

1. 面向无连接
  - 首先 UDP 是不需要和 TCP一样在发送数据前进行三次握手建立连接的，想发数据就可以开始发送了。并且也只是数据报文的搬运工，不会对数据报文进行任何拆分和拼接操作。
  - 具体来说就是：
    - 在发送端，应用层将数据传递给传输层的 UDP 协议，UDP 只会给数据增加一个 UDP 头标识下是 UDP 协议，然后就传递给网络层了
    - 在接收端，网络层将数据传递给传输层，UDP 只去除 IP 报文头就传递给应用层，不会任何拼接操作
2. 有单播，多播，广播的功能
  - UDP 不止支持一对一的传输方式，同样支持一对多，多对多，多对一的方式，也就是说 UDP 提供了单播，多播，广播的功能。
3. UDP是面向报文的
  - 发送方的UDP对应用程序交下来的报文，在添加首部后就向下交付IP层。UDP对应用层交下来的报文，既不合并，也不拆分，而是保留这些报文的边界。因此，应用程序必须选择合适大小的报文
4. 不可靠性
  - 首先不可靠性体现在无连接上，通信都不需要建立连接，想发就发，这样的情况肯定不可靠。
  - 并且收到什么数据就传递什么数据，并且也不会备份数据，发送数据也不会关心对方是否已经正确接收到数据了。
  - 再者网络环境时好时坏，但是 UDP 因为没有拥塞控制，一直会以恒定的速度发送数据。即使网络条件不好，也不会对发送速率进行调整。这样实现的弊端就是在网络条件不好的情况下可能会导致丢包，但是优点也很明显，在某些实时性要求高的场景（比如电话会议）就需要使用 UDP 而不是 TCP。

UDP只会把想发的数据报文一股脑的丢给对方，并不在意数据有无安全完整到达。
- ![动图](https://img-blog.csdnimg.cn/img_convert/f94c7f0d5acb2f59726684dcf0be50ca.gif)

## TCP与UDP

[一文搞懂TCP与UDP的区别](https://blog.csdn.net/AN0692/article/details/114842039)
- TCP向上层提供面向连接的可靠服务 ，UDP向上层提供无连接不可靠服务。
- 虽然 UDP 并没有 TCP 传输来的准确，但是也能在很多实时性要求高的地方有所作为
- 对数据准确性要求高，速度可以相对较慢的，可以选用TCP

| 维度 | UDP | TCP |
|---|---|---|
| 是否连接 | 无连接 | 面向连接 |
| 是否可靠 | 不可靠传输，不使用流量控制和拥塞控制 | 可靠传输，使用流量控制和拥塞控制 |
| 连接对象个数 | 支持一对一，一对多，多对一和多对多交互通信 | 只能是一对一通信 |
| 传输方式 | 面向报文 | 面向字节流 |
| 首部开销 | 首部开销小，仅8字节 | 首部最小20字节，最大60字节 |
| 适用场景 | 适用于实时应用（IP电话、视频会议、直播等） | 适用于要求可靠传输的应用，例如文件传输 |

## IEEE

- IEEE 802.3 ：IEEE 组织定义的以太网技术标准，即有线网络标准。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/7a521813130a4e928a5c2a1aef91bbb5?from=pc)
- IEEE 802.11 ：IEEE 组织定义的无线局域网标准。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/96a6c76680a043b89c4fa3a02f6ffab9?from=pc)

## ARP

ARP ：全称是地址解析协议，通过目的 IP 地址解析目的设备 MAC 地址。
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/4184db81c8d64af89d35ef42500331db?from=pc)


## HTTP

- HTTP ：全称是**超文本传输协议**，客户端可以通过与服务器之间建立的连接，来传输 Web 超文本信息的应用层协议。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/3b973d8620e54380af05f0fb5a339632?from=pc)
- SSL ：全称是安全套接字层，是网景公司开发的技术，在 TCP 与应用层协议之间插入一层，为应用层提供额外的信息安全防护措施。
- TLS ：全称是传输层安全，是 IETF 对 SSL 协议进行标准化的结果，与 SSL 差别不大，但不相互兼容。
- HTTPS ：全称是安全的超文本传输协议，客户端通过 SSL/TLS 与服务器之间建立安全的 HTTP 连接，以传输超文本信息。
- 用户代理：在电子邮件的架构中，用户代理指终端用户用来收发邮件的电子邮件客户端。
- SMTP ：全称是简单邮件传输协议，定义了邮件服务器之间相互传输邮件的标准与流程。
- 邮件访问协议：定义了接收方用户代理如何从邮件服务器获取邮件的协议。
- POP3 ：全称是邮局协议版本 3 ，定义了接收方用户代理对接收方邮件服务器执行下载、删除邮件等命令的流程及标准。


# 应用


## 电视


### 术语

视频分辨率是指视频在一定区域内包含的像素点的数量，常见的有：
- 720P 分辨率为1280x720像素
- 1080P 分辨率为1920*1080像素
- 2k 分辨率为2560*1440像素
- 4k 分辨率为3840*2160像素
- 8K 分辨率为7680×4320像素

解释
- “P”全拼为Progressive译为逐行扫描，几P则表示纵向有多少行像素
  - 比如：720P表示纵向有720行像素、1080P表示纵向有1080行像素。
- 随着分辨率越来越大，开始用“k”值来表示
  - 比如：2160P就开始用4k来称呼，但还是有人会叫2160P。
- “k”表示的是横向排列有多少像素
  - 比如：2k就是视频横向大约有2000列像素、4k就是视频横向大约有4000列像素。

图解 [img](https://pics2.baidu.com/feed/7c1ed21b0ef41bd544c110e0b9e7b6cd38db3ddc.jpeg@f_auto?token=9b8b71d31e26b1f868ac459e7acdbccb&s=7F0536661E447E5DC8A7836E0200F07B)
- ![img](https://pics2.baidu.com/feed/7c1ed21b0ef41bd544c110e0b9e7b6cd38db3ddc.jpeg@f_auto?token=9b8b71d31e26b1f868ac459e7acdbccb&s=7F0536661E447E5DC8A7836E0200F07B)
- [讲解](https://baijiahao.baidu.com/s?id=1658614872548568079&wfr=spider&for=pc)

#### 4K

4K级别的分辨率可提供880多万像素，实现电影级的画质，相当于当前顶级的1080p分辨率的四倍还多
- 4k电视的分辨率是 `3840×2160` 像素, 也称为“`2160p`”, 常说的`2K*2K`(2560x1440)的4倍
- `1080p`是指`1920*1080`的分辨率
- 4k显示细腻度为 `1080p` 的 4 倍以上
- 4K电视可以显示更丰富的色彩和图像细节,具有高对比度和超高的清晰度等优点

国内
- 大多数数字电影是2K，分辨率为`2048×1080`
- 部分数字电影是1.3K(`1280×1024`)的
- 而所谓有**农村电影**放映的是0.8K(`1024×768`)的。

真正意义上的4K电影由**4K摄像机**拍摄，用**4K放映机**放映。有的4K电影是由35mm胶片拍摄的，再转成4K的数字格式。由于胶片电影的分辨率与4K大致相当或者会略好，故转录之后也能保证电影的清晰度。对于主流的家电设备厂商而言，他们更倾向于制造接近 4K 的 Quad Full `HD`(3840×2160)设备，因为这个分辨率标准的显示比例为 16:9，与消费者当前接受的观看比例比较接近。


### 国际电视

各个国家都在用哪种电视（模拟/数字）？

![](https://pica.zhimg.com/80/v2-4a654ade5feef8d81413e6ae99b04db0_1440w.webp)

- 红色：完成向数字信号的转换，完全数字信号
- 橙色：大部分是数字信号，将会完成向数字信号的转换
- 黄色：向数字信号的转换中，数字信号和模拟信号共存
- 绿色：没有开始转换或刚刚开始转换，主要为模拟信号
- 灰色：没有计划向数字信号转换，数字信号和模拟信号共存（原图注如此，其实我觉得应该是没有数据吧）

中国
- 全国各地的**中央台**节目地面模拟电视信号于2020年8月31日前
- 地方节目的地面模拟电视信号于 2020年12月31 日前完成关停，特殊情况最迟于2021年3月31日前完成关停。

作者：[黄鼠狼精Morrica](https://www.zhihu.com/question/459952691/answer/1891337632)


### 国内电视收听

广电总局允许的几种看电视直播渠道
1. 农村偏远地区可使用`户户通`，目前已到第四代有高清频道。
2. 城镇区域原先看电视基本上是当地`有线电视网络`垄d的市场，有线电视目前依然是主流看电视的方式之一。
3. 宽带运营商和广电合作，一方负责传输, 一方负责内容播控的`IPTV`网络电视，这个也是目前主流，对原有的有线电视冲击较大。
4. 国家地面数字电视`DTMB`无线数字覆盖网络。(地面波天线)
5. 在移动互联网领域，背靠移动的`咪咕`和`央视频`等`手机电视`。
6. 开源的免费TV聚合APP软件, 如 TVBox，可以在所有安卓端：电视、平板、手机安装使用

其实只有这三个：
- 1、安装`有线电视`(最多)，通过地方广电部门差转、广电公司提供服务的电视信号收看电视节目。
- 2、安装由电信运营商提供服务的`IPTV`。
  - 广东IPTV是不能收看港澳电视节目。
  - 外省应该没有这种区别，也没有收看港澳电视的需求。
- 3、自行安装`天线`，通过`地面波天线`（dtmb）接收各地广电部门依照国家政策免费提供的地面电视信号。
  - 原本还可以接收到CCTV的3、5、6、8，最近可能是广州越秀山发射塔出了什么问题接收不到


区别
- 4方式`地面数字电视频道`有限，画质可能只有标清，频道顶多1-20来个有的地方可能例外，信号覆盖可能也仅限于城镇居住人口多的地方，且以公共服务信息资讯为主，央视只有除3568的频道，然后是本省、市或县台频道。投入最少(100左右)，需要天线或机顶盒，因为大部分地面波音频是DRA格式，很多电视厂商虽然有DTMB搜台功能，但是只能显示画面。其他几个都需要加钱可及，如果家中有宽带上网需求，最好的是一并报装iptv，这样的话直播点播回看都有而且比较稳定。

不要用电视厂商内置的所谓`有线电视`
- 家里的某维电视就有个有线电视app，切换不同省份，能在网络条件下看央视和省卫视，有的省份还有当地几个省台，但是价格偏高，且这种宽带电视在运营上未必真就获得了地方广电的授权，用户付费给电视厂商方权益无从保证(进过这种群发现很多用户付费后卡呀看不了问题一大堆。)在现阶段DVB+OTT可能就是试验阶段。

为什么不直接装一些第三方应用app呢？
- 好用的app不是没有，可信号源多半是采集自网络(一般的电视台都会在网络上给出电视直播+各地公网传输IPTV流出地址)，对用户网络各方面无从保证，有的app前期free揽用户，后期就加广告或需要开会员(给一定的维护费用也在情理之中)，所以还不如自己折腾，这个得看个人取舍。

作者：[ShadowZen](https://www.zhihu.com/question/582150605/answer/2887396464)

目前数字电视的能力，提供4K信号已经是可行的，目前全国范围内有CCTV 4K和广东综艺两个4K频道，但是具体家里能不能接收到4K信号，和有线电视服务商以及家用机顶盒是否支持有关。


### (1) 有线电视


歌华有线涵盖高清、4K、中数传媒、华诚、文广等等频道很全，这是地面数字电视不能比的。


### (2) IPTV

- [IPTV资源汇总](https://github.com/Meroser/IPTV)
- 各国 IPTV [电视直播入口](https://iptv-org.github.io/), [GitHub](https://github.com/iptv-org/iptv)

多个维度划分

```sh
# 类目
https://iptv-org.github.io/iptv/index.category.m3u
# 语言
https://iptv-org.github.io/iptv/index.language.m3u
# 国家
https://iptv-org.github.io/iptv/index.country.m3u
# 区域
https://iptv-org.github.io/iptv/index.region.m3u
```

VLC 配置
- Media -> Open Network Stream -> paste the M3U URL -> Play


电子节目指南（electrical program guide，简称EPG）
- Electronic Program Guide的英文缩写，意思是电子节目菜单，即节目预告。

#### IPTV 播放软件

各个渠道的IPTV软件资源汇总
- [Awesome IPTV](https://github.com/iptv-org/awesome-iptv#apps)
- [IPTV网络直播](https://down.iptv2020.com/down.php)

免费 IPTV 客户端
- [Televizo IPTV](https://televizo-iptv-player.en.softonic.com/android)
  - 配置方法: TV上U安装，详见[Meroser's IPTV](https://github.com/Meroser/IPTV)
  - 播放源[TPv6链接](https://mirror.ghproxy.com/https://raw.githubusercontent.com/Meroser/IPTV/main/IPTV.m3u), [EPG源信息](https://mirror.ghproxy.com/https://raw.githubusercontent.com/Meroser/IPTV/main/tvxml.xml), 未关联成功
- [Tivimate IPTV](https://tivimate-iptv-video-player-ott.en.softonic.com/android), 高级功能需要付费
- [Dream Player IPTV](https://dream-player-iptv.en.softonic.com/android)
- [OTT Navigator IPTV](https://ott-navigator-iptv.en.softonic.com/android) 号称优于 Dream Player，如果想完全免费，用 Lazy 和 Rayo
  - OttPlayer是一个非常精致的播放器，支持多种协议，包括HLS，RTSP，UDP和TS，以及RTMP。
- [Lazy IPTV](https://en.softonic.com/download/lazy-iptv/android/post-download)
- [IPTV Rayo](https://en.softonic.com/download/iptv-rayo/android/post-download)

【2024-2-17】软件实测，小米tv
- [Televizo IPTV](https://televizo-iptv-player.en.softonic.com/android)和[OTT Navigator IPTV](https://ott-navigator-iptv.en.softonic.com/android) 免费可用
- [Tivimate IPTV](https://tivimate-iptv-video-player-ott.en.softonic.com/android)限制数目，引导付费

#### IPTV 播放源

播放源
- 播放源[TPv6链接](https://mirror.ghproxy.com/https://raw.githubusercontent.com/Meroser/IPTV/main/IPTV.m3u), [EPG源信息](https://mirror.ghproxy.com/https://raw.githubusercontent.com/Meroser/IPTV/main/tvxml.xml), 国内电视台 191个, 有广告
- [https://iptv-org.github.io/iptv/index.m3u](https://iptv-org.github.io/iptv/index.m3u)
- [https://codeberg.org/testTV/TestV/raw/branch/main/FreeTest.m3u](https://codeberg.org/testTV/TestV/raw/branch/main/FreeTest.m3u)
- [ibert](https://m3u.ibert.me/o_all.m3u)

【2024-4-5】最新iptv源，每两小时自动更新一次，含有超过 1w+ 数量的 IPTV 列表，丰富且全面！
- GitHub：[iptv-sources](http://github.com/HerbertHe/iptv-sources)

比如
- [fmml_ipv6.m3u](https://iptv.b2og.com/fmml_ipv6.m3u)
- [all.m3u](https://iptv.b2og.com/all.m3u)

VLC 播放器设置方法
- Media -> Open Network Stream -> paste the M3U URL -> Play
- 打开VLC，点击“媒体”->“打开网络流”，然后在“网络流URL”中输入M3U文件的URL，点击“播放”即可开始播放。


#### Android 环境

Android 如何观看

软件
- `Smarters Player`: [IPTV Smarters Player & M3U Player](https://www.androidfreeware.mobi/download-apk-com-iptv-smart-player.html)
- `TiviMate`: [TiviMate IPTV Player for Android  V 4.7.0](https://en.softonic.com/download/tivimate-iptv-video-player-ott/android/post-download)
- 【2024-4-5】开源免费的安卓电视直播软件 [My TV](http://lyrics.run/my-tv.html) —— 【2024-10】无法播放，意思跑路
  - 内置直播源，直接安装即可使用，具有稳定、快速、免费和无广告等特点。
  - GitHub：[My TV](http://www.github.com/lizongying/my-tv)，直接点击 [链接](https://github.com/lizongying/my-tv/releases/download/v1.7.3/my-tv-v1.7.3.apk) 下载即可

注意：仅支持安卓 4.2 及以上系统。


**Android TV**

[Comparing Some of the Best IPTV Streaming Apps](https://www.softwaretestinghelp.com/best-free-iptv-apps/)

| Name | Best For | Fees  | Ratings | Website |
| --- | --- | --- | --- | --- |
| **[Xtreme HD IPTV](https://softwaretesthelp.com/Xtreme-HD)** | Access to thousands of premium channels across the globe. | Starts at $15.99 per month | ![Star_rating_5_of_5](https://www.softwaretestinghelp.com/wp-content/qa/uploads/2019/04/Star_rating_5_of_5.png) | [Visit](https://xtremehdiptv.org/billing/aff.php?aff=429) |
| **[IPTV Trends](https://iptvtrends.com/billing/aff.php?aff=19)** | 4K Video Quality Support | Starts at $18.99 | ![Star_rating_4.5_of_5](https://www.softwaretestinghelp.com/wp-content/qa/uploads/2019/04/Star_rating_4.5_of_5.png) | [Visit](https://iptvtrends.com/billing/aff.php?aff=19) |
| **[Tubi](https://play.google.com/store/apps/details?id=com.tubitv&hl=en_US&gl=US)** | Free Movie, TV Show, and Anime Streaming | Free |  ![Star_rating_5_of_5](https://www.softwaretestinghelp.com/wp-content/qa/uploads/2019/04/Star_rating_5_of_5.png) | [Visit](https://play.google.com/store/apps/details?id=com.tubitv&hl=en_US&gl=US) |
| **[Red Bull TV](https://play.google.com/store/apps/details?id=com.nousguide.android.rbtv&hl=en_US&gl=US)** | Watch extreme sports events live with AR | Free | ![Star_rating_5_of_5](https://www.softwaretestinghelp.com/wp-content/qa/uploads/2019/04/Star_rating_5_of_5.png) | [Visit](https://play.google.com/store/apps/details?id=com.nousguide.android.rbtv&hl=en_US&gl=US) |
| **[Pluto TV](https://play.google.com/store/apps/details?id=tv.pluto.android&hl=en_US&gl=US)** | Access Library of  Cult Movies and  Spanish Language support | Free |![Star_rating_4_of_5](https://www.softwaretestinghelp.com/wp-content/qa/uploads/2019/07/Star_rating_4_of_5.png) | [Visit](https://play.google.com/store/apps/details?id=tv.pluto.android&hl=en_US&gl=US) |
| **[IPTV](https://play.google.com/store/apps/details?id=ru.iptvremote.android.iptv&hl=en_IN&gl=US)** | Extended Playlists History | Free | ![Star_rating_4_of_5](https://www.softwaretestinghelp.com/wp-content/qa/uploads/2019/07/Star_rating_4_of_5.png) | [Visit](https://play.google.com/store/apps/details?id=ru.iptvremote.android.iptv&hl=en_IN&gl=US) |
| **[IPTV Smarters Pro](https://play.google.com/store/apps/details?id=com.nst.iptvsmarterstvbox&hl=en_IN&gl=US)** | Fully Customizable OTT Experience | Free.  $1.62 for the premium version allows streaming on upto 5 devices. | ![Star_rating_4_of_5](https://www.softwaretestinghelp.com/wp-content/qa/uploads/2019/07/Star_rating_4_of_5.png) | [Visit](https://play.google.com/store/apps/details?id=com.nst.iptvsmarterstvbox&hl=en_IN&gl=US) |


#### Mac 环境

Mac 下如何观看？
- 下载 软件 
  - [ApTV](https://apps.apple.com/cn/app/aptv/id1630403500), APTV，一款可实时预览的高颜值直播源播放器App，是一个可播放可回看(需要直播源支持)的多功能播放器
  - [VLC for Mac](https://get.videolan.org/vlc/3.0.20/macosx/vlc-3.0.20-intel64.dmg)
- 添加播放列表


### (3) DTMB

`DTMB` 全称是**数字地面**多媒体广播（Digital Terrestrial Multimedia Broadcast）。

`DTMB` 是提供广播电视公共服务的一种基本手段和重要方式，它与**卫星数字**电视广播系统和**有线数字**电视广播系统一起相互协同提供全面的广播电视覆盖。
- 优点：安装成功后可以接收十多个电视台，清晰度不错。
- 缺点：要求所在地区有覆盖，且需要购买适合自家电视的DTMB电视天线才行，然后自行安装即可。
- ![](https://picx.zhimg.com/80/v2-0ef49dc51770273f338233da8d7eecd4_1440w.webp?source=2c26e567)

2015年，国家要求电视必须支持 DTMB 信号。

#### 免费电视


【2023-7-4】[北京地面波瞎玩记](https://mp.weixin.qq.com/s/bw5tgqy_sq0yYcQApCOipQ)

北京这种大城市，由于**有线电视**的普及率很高，所以**地面数字电视**建设积极性很差。

[北京市地面数字电视节目表查询—中文寻星](http://dtmb.saoing.com/beijing.htm) 上，频道很多，但高清频道很少。而且发射塔和高楼众多，导致信号参差不齐。

示例
- 北京欢乐谷附近，只能接收到中央电视塔`482`、`546`和`626`三组
- `482`因小米电视不支持解码`AC3`音频格式（杜比）, 无法播放声音

中央电视塔在西三环玉渊潭

【2025-2-9】淘宝上花 30-50元 购买地面波接收器
- 安装: 
  - 电视端，插入天线口（信号输入）、usb口（放大器电源供应）
  - 接收器拉到窗外
- 注意：
  - 接收器竖着放，尽量别遮挡

实测
- 北京北五环，14层北向安装
- 电视：小米电视，支持地面数字电视服务 
- 效果：一共收到**23个台**，其中大部分是广播（没有7/11/13/14），其余11个是电视台
- 其中，央视8个，北京地方台4个（顺义台/昌平台/北京卫视科教），两个没声音

分析

|频率|类型|电视台|极化|分析|
|---|---|---|---|---|
|538|电视|CCTV-1||综合|
|538|电视|CCTV-2||财经|
|538|电视|CCTV-4||中文国际|
|538|电视|CCTV-10||科教|
|538|电视|CCTV-12||社会与法|
|538|电视|CCTV-13||新闻|
|538|电视|CCTV-14||少儿|
|538|电视|CCTV-15||音乐|
|554|电视|BRTV-KJHD|水平|北京科教高清（没声音）|
|554|电视|BRTV-XWHD|水平|北京新闻高清（没声音）|
|562|电视|BRTV-*|水平|北京卡酷少儿（没声音）|
|562|电视|BRTV-*|水平|北京文艺（没声音）|
|490|电视|顺义电视台|垂直|不稳定|
|195|电视|昌平电视台|水平|不稳定|
|538|广播|CNR-1||中国之声|
|538|广播|CNR-2||经济之声|
|538|广播|CNR-3||音乐之声|
|538|广播|CNR-4||都市之声|
|538|广播|CNR-5||中华之声|
|538|广播|CNR-6||神州之声|
|538|广播|CNR-8||民族之声|
|538|广播|CNR-9||文艺之声|
|538|广播|CNR-10||老年之声|
|538|广播|CNR-12||维吾尔语广播|
|538|广播|CNR-15||中国高速公路交通广播|
|538|广播|CNR-16||中国乡村之声|
||||||
||||||



`中央人民广播电台`是中国**唯一**覆盖全国的广播电台，已开办: CNR-1中国之声、CNR-2经济之声、CNR-3音乐之声、
CNR-4都市之声、CNR-5中华之声、CNR-6神州之声、CNR-7华夏之声、CNR-8民族之声、CNR-9文艺之声、CNR-10老年之声、CNR-11藏语广播、CNR-12维吾尔语广播、CNR-13娱乐广播、CNR-14香港之声、CNR-15中国高速公路交通广播、CNR-16中国乡村之声共16套广播频率。

中国之声是中央人民广播电台历史最为悠久，中国广播界最具权威和影响力的广播新闻综合频
- CNR-1 中国之声
- CNR-2 经济之声
- CNR-3 音乐之声
- CNR-4 都市之声
- CNR-5 中华之声
- CNR-6 神州之声
- CNR-7 **华夏之声**
- CNR-8 民族之声
- CNR-9 文艺之声
- CNR-10 老年之声
- CNR-11 **藏语广播**
- CNR-12 维吾尔语广播
- CNR-13 **娱乐广播**
- CNR-14 **香港之声**
- CNR-15 中国高速公路交通广播
- CNR-16 中国乡村之声


### (4) 卫星电视

待定


### 小米电视

小米电视配套设施
- 【2021-5-23】[电视家破解版](http://www.ucbug.com/shouji/126280.html)，数字电视直播软件；免费版有广告，央视频道可以安装另一款软件：新视听
- 乐播投屏、小米投屏神器（可以用手操作安装应用，摆脱遥控器）
- NetFlix tv：流媒体巨头，资源丰厚，无删减，用户体验领先国内大部分视频网站八百条街
   - [Netflix安装包](https://apkpure.com/netflix/com.netflix.mediaclient)
   - 安装：参考[文章](https://www.66152.com/article/202107/305898.html)
   - ① U盘拷到电视上下载
   - ② 下一个 `Aptoide TV`（相当于国外版“`当贝市场`”）—— 也可用当贝市场里的文件快传功能接受下载的aptoide tv
      - 不一定成功，因为国内只有索尼一家的电视支持安装Netflix TV
      - 非索尼电视，怎么办？购买海外版小米盒子（MiBox） or Amazon电视棒；二者都内置 Netflix，后者还自带传说中的人工智能Alexa（美版天猫精灵）
   - ③ 下一个适合你电视/盒子的软件，并买一个鼠标
   - 安装成功，但卡壳，无法正常使用,Netflix无法用小米电视遥控器选择节目外; 参考[地址](https://www.typemylife.com/netflix-youtube-on-xiaomi-tv/)
   - netflix有两个版本，一个是**TV版**，白色的logo。另一个是**安卓版**，黑色logo。
   - 小米电视上可以安装黑色的那个，需要鼠标控制，但是图像模糊。装白色那个就会提示“此 App 与您的设备不兼容”
   - 解法一：小米投屏神器 可以直接切换鼠标模式 
   - 解法二：淘宝搜索“空中鼠标”，买一个（最好是带键盘输入的）
- Youtube TV：需要谷歌框架，需要使用另一款：[Smart YouTube TV](https://smartyoutubetv.github.io/)，[下载地址](https://github.com/yuliskov/SmartTubeNext/releases/download/latest/smarttube_stable.apk)
  - [在小米电视和小米盒子上看YouTube](https://www.williamlong.info/archives/5624.html)
- 翻墙：Clash（mac版是clashx）、v2rayN
  - Clash是一款用 Go开发的支持 Linux/MacOS/Windows等多平台的代理工具，支持 ss/v2ray/snell（不支持 ssr），支持规则分流（类似于 Surge 的配置）；参考[文章](https://freebrid.com/index.php/2021/03/01/clash-for-mac/)
  - Clash的[win版](https://github.com/Fndroid/clash_for_windows_pkg/releases)、[mac版](https://github.com/Fndroid/clash_for_windows_pkg/releases) (亲测无法安装，改用[clashx](https://github.com/yichengchen/clashX/releases))、[apk版](https://github.com/Kr328/ClashForAndroid/releases)
  - [ClashX github下载](https://github.com/yichengchen/clashX/releases), [Clash for Mac 版使用教程 ClashX 教程](https://2022vpn.net/clash-for-mac-tutorial/)
- Apple TV 4K盒子体验
-【2019-05-27】[电视直播链接汇总](http://bddn.cn/zb.htm)，国外免费电视直播：[pluto.tv](https://pluto.tv/)，[fox news](https://freeetv.com/live-television-5643.html)



## 耳机



### 蓝牙耳机


无限蓝牙耳机评测

【2024-7-1】500以内的**开放式耳机**评测 
- 倍思eli > sanag 塞那 > 1MORE

<iframe width="560" height="315" src="https://www.youtube.com/embed/0ztT_cwAF_Q?si=oxKoUTPLvrz9Y3Zk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>




## 内网穿透


### 什么是内网穿透？

内网穿透是指通过特定网络技术或工具，突破内网的防火墙和路由器，允许外部设备访问内网的服务。

常见的应用场景：
- **远程控制内网设备**：开发者需要在外部访问处于内网中的服务器。
- 网站和API的**暴露**：开发中的Web应用、数据库等需要暴露给外部进行测试。
- **IoT设备接入**：物联网设备通过内网穿透与外部服务通信。

内网穿透工具通过“隧道”或“代理”方式实现外部设备和内网设备之间的直接连接，而无需修改路由器或防火墙配置。

[推荐10个内网穿透工具](https://blog.csdn.net/wholeliubei/article/details/144429820)

|工具|免费|开源|缺点|
|---|---|---|---|
|FRP|√|√|需要公网中转服务器|
|Ngrok|√|×|免费版时间功能受限|
|OpenVPN|√|√|VPN，附带穿透，配置相对复杂|
|Tunnelblick|||基于 OpenVPN, 只能用于 MacOS|
|Goproxy|√|√|跨平台，功能相对简单|
|||||
|||||
|||||

### FRP

FRP (Fast Reverse Proxy)

FRP 是高性能的**反向代理应用**，帮助用户穿透防火墙，支持 TCP、UDP、HTTP、HTTPS 等协议的穿透。

FRP 采用 客户端-服务端 架构，允许内网服务通过外网代理服务器公开访问。
- [FRP 官方文档](https://gofrp.org/zh-cn/)   
- [FRP 代码](https://github.com/fatedier/frp)

特点
- 支持多种协议：FRP 支持 TCP、UDP、HTTP、HTTPS 等多种协议，适用于 Web 服务、数据库、SSH 等应用。
- 性能优越：FRP 的设计目标之一是高效的传输速度，能够在有限的带宽条件下提供稳定的连接。
- 易于配置：FRP 提供了简单易用的配置文件和命令行参数，支持快速部署。
- 加密与安全：FRP 使用 TLS 加密协议，保证传输过程中的数据安全。

分析
- 优点：免费、开源、易于配置、支持多种协议。
- 缺点：需要一个公网**中转服务器**作为代理。


### Ngrok

[Ngrok](https://ngrok.com/) 是广受欢迎的内网穿透工具，通过简单的命令启动, 即可为本地服务生成一个公网可访问的地址。

Ngrok 不仅支持 HTTP 和 TCP 协议的转发，还具有易于使用的 Web 控制台。
- [ngrok](https://github.com/inconshreveable/ngrok)
   
特点
- Web 控制台：Ngrok 提供了一个方便的 Web 界面，用户可以实时查看和管理端口转发的状态。
- 支持多种协议：不仅支持 HTTP、HTTPS 和 TCP，还支持自定义协议和自定义域名。
- 隧道加密：Ngrok 支持 HTTPS 隧道，加密保护传输数据的安全性。
- API 支持：Ngrok 提供了 REST API 供开发者实现自动化集成

优缺点
- 优点：易于使用、开箱即用、支持自定义域名。
- 缺点：免费版有使用**时间和功能**限制，可能不适合长期使用。

安装与配置
- 注册 Ngrok 账号。
- 下载并安装 Ngrok 客户端。
  - [Windows](https://download.ngrok.com/windows )
- 使用命令行启动服务：
  - ngrok http 80（假设本地服务运行在端口 80）。

### Tunnelblick

[Tunnelblick](https://tunnelblick.net/) 基于 OpenVPN 的图形化客户端，提供了基于 SSL 的安全隧道连接。
- 它不仅支持内网穿透，还支持 VPN 连接。

特点
- 基于 OpenVPN：Tunnelblick 基于 OpenVPN 协议，因此提供了高安全性的隧道连接。
- 图形化界面：适合不熟悉命令行的用户，通过图形化界面轻松配置和使用。
- 跨平台支持：Tunnelblick 支持 macOS 系统，能够与多种设备进行连接。
- 开源免费：完全免费，并且开源，符合大多数企业和个人用户的需求。

优缺点
- 优点：安全性高、图形化界面、开源免费。
- 缺点：**只支持 macOS**，不支持 Windows 或 Linux 客户端。

安装与[配置](https://tunnelblick.net/documents.html)
- 安装 Tunnelblick 客户端。
- 配置 OpenVPN 配置文件。
- 启动 Tunnelblick 连接到内网服务器。
 


### GoProxy

GoProxy 是一款轻量级的内网穿透工具，采用 Go 语言开发，支持端口转发、Web 服务暴露等功能。GoProxy 具有简单的配置和高效的性能。
- 代码 [goproxy](https://github.com/snail007/goproxy)   


特点
- 轻量级：GoProxy 由 Go 语言编写，整体非常轻便，适合快速部署。
- 跨平台支持：支持 Windows、Linux、macOS 等多个操作系统。
- 易于配置：通过简单的配置文件，用户可以快速设置内网穿透功能。
- 支持自定义域名：用户可以配置自定义域名进行访问。


优缺点
- 优点：开源、轻量、跨平台。
- 缺点：功能相对简单，可能不适合复杂的企业级应用。

安装与[配置](https://snail007.host900.com/goproxy/manual/zh/#/)
- 下载 GoProxy 安装包。
- 配置端口转发规则。
- 启动服务并测试内网穿透功能。

### OpenVPN

[OpenVPN](https://openvpn.net/) 是一个流行的虚拟专用网络（VPN）解决方案，广泛用于企业和个人用户的远程接入。尽管 OpenVPN 更常用于建立加密连接，但它也可以作为内网穿透的有效工具。
- 代码 [openvpn](https://github.com/OpenVPN/openvpn) 


特点
- 高安全性：OpenVPN 使用 SSL/TLS 进行加密，提供高安全性。
- 可扩展性：适合中大型企业部署，支持多种认证方式和 VPN 配置。
- 跨平台支持：支持 Windows、Linux、macOS 等平台。
- 社区支持强大：OpenVPN 拥有广泛的社区支持和丰富的文档。

优缺点
- 优点：高安全性、可扩展性强、适用于大规模部署。
- 缺点：配置相对复杂，适合有一定技术基础的用户。

安装与配置
- 配置 OpenVPN 服务器。
- 安装 OpenVPN 客户端。
- 配置和连接远程内网。

### cpolar

[cpolar](https://www.cpolar.com/) 是一款功能强大的内网穿透工具，支持 HTTP、HTTPS、TCP 协议，广泛适用于各种开发和测试场景。

cpolar 提供了永久免费使用的服务，带宽为 1 Mbps，支持最大 4 条隧道连接。它允许用户自主选择服务器地区（国内或国外），提供良好的连接稳定性和较高的灵活性。

特点
- 支持协议：HTTP、HTTPS、TCP。
- 免费使用：永久免费，带宽 1Mbps，流量不限制。
- 隧道数量：免费版支持 4 条隧道。
- 灵活性高：支持自定义域名、端口映射等功能。
- 教程完善：官方提供了详细的文档和教程，用户可以快速上手。
- 跨平台支持：支持多平台使用，Windows、Linux 和 macOS 都可以正常运行。

安装与配置
- 注册并下载 cpolar 客户端。
- 配置隧道与端口映射。
- 启动客户端，并开始使用内网穿透服务。




### 花生壳

[花生壳](https://hsk.oray.com/)是一款知名内网穿透工具，支持 HTTP、HTTPS 和 TCP 协议。
- 花生壳提供了**免费套餐**，带宽为 1 Mbps，每月流量限制为 1 GB，支持最多 2 条隧道连接。
- 花生壳适用于需要长时间稳定运行的小型项目或开发者个人使用。

特点
- 支持协议：HTTP、HTTPS、TCP。
- 免费套餐：带宽 1Mbps，每月流量 1GB，最多支持 2 条隧道。
- 认证机制：需要实名认证以确保服务安全。
- 稳定性好：信誉较好，使用过程稳定。
- 教程完备：官方提供了详细的教程和文档，易于配置。

优缺点
- 优点：信誉良好、稳定性高、教程完善。
- 缺点：**免费版流量有限**，可能无法满足较大规模的数据传输需求。

使用 贝锐 花生壳，将本机服务映射到外网地址

需求
- 内网服务地址: http://192.168.1.6:5000/
- 映射到外网

步骤
- 注册 花生壳账户
- 安装 花生壳客户端，同名账户登录
- 启动客户端后台服务
  - 如 ip 192.1.1.6 端口 5000
- 启动花生壳, 创建 内网穿透
  - 客户端: 左侧 创建 `内网穿透`, 关联以上 ip 和 端口
  - 或[Web端](https://console.hsk.oray.com/forward)
- 生成外部可访问地址 [http://jt2092xo3062.vicp.fun/](http://jt2092xo3062.vicp.fun/)


### SAKURA FRP

[SAKURA FRP](https://www.natfrp.com/) 是一款高效的内网穿透工具，支持 HTTP、HTTPS、TCP 和 UDP 协议，能够提供更高的带宽和流量限制。

它免费提供每月 5 GB 流量，带宽 10 Mbps，支持最多 2 条隧道连接。通过每日签到，用户可以额外获取免费流量，极大地提高了灵活性。


特点
- 支持协议：HTTP、HTTPS、TCP、UDP。
- 免费流量：每月 5 GB 流量，带宽为 10 Mbps。
- 签到奖励：每日签到可以获得额外的免费流量。
- 教程详细：官方提供了详细的文档和配置指南，帮助用户快速入门。


优缺点
- 优点：较大的免费带宽和流量、支持多种协议。
- 缺点：免费版仍有一些限制，如隧道数量限制。

安装与配置
- 注册并下载 SAKURA FRP 客户端。
- 配置隧道并设置端口映射。
- 启动客户端并连接到服务器。

### NATAPP


[NATAPP](https://natapp.cn/) 是一款简单易用的内网穿透工具，支持 HTTP、HTTPS 和 TCP 协议。它提供免费流量且不限制流量使用，每月最多支持 2 条隧道连接，带宽为 1 Mbps。NATAPP 适合对易用性有较高要求的用户，界面简洁，使用方便。

特点
- 支持协议：HTTP、HTTPS、TCP。
- 流量不限制：免费版不限制流量。
- 隧道数量：最多支持 2 条隧道连接。
- 实名认证：使用时需要实名认证以确保服务的安全。

使用场景
- 小型开发项目：适合用于开发者将本地服务暴露给外部访问进行测试。
- 远程工作：适合需要远程访问公司内网的个人或团队。

优缺点
- 优点：免费流量不限制、简单易用、稳定性高。
- 缺点：免费带宽有限，适用于小流量应用。

安装与配置
- 注册并下载 NATAPP 客户端。
- 配置隧道并选择合适的端口映射。
- 启动并使用 NATAPP 进行内网穿透。


### 飞鸽

[飞鸽](https://www.fgnwct.com/)是一款无需安装即可使用的内网穿透工具，支持 TCP、HTTP、UDP 协议。飞鸽的免费版本提供 0.5 Mbps 的带宽，最多支持 1 条隧道连接，且支持 20 个并发连接。飞鸽的操作非常简便，用户只需解压即可使用，适合临时快速搭建的场景。

特点
- 支持协议：TCP、HTTP、UDP。
- 无需安装：解压即用，无需复杂的安装过程。
- 免费带宽：0.5 Mbps，支持最多 20 并发连接。
- 不限流量：提供无限流量的使用，适合低带宽需求的场景。

使用场景
- 临时项目：适合快速部署临时服务，尤其是在没有复杂配置需求的情况下。
- 小型测试和个人项目：适合用来暴露小型 Web 服务或其他内网服务。

优缺点
- 优点：无需安装、简单易用、支持多种协议。
- 缺点：带宽有限，适合低流量和并发需求的应用。

安装与配置
- 下载并解压飞鸽客户端。
- 配置隧道和端口映射。
- 启动并使用飞鸽进行内网穿透。


【2025-1-8】实践
- 使用不便，要注册，且付费实名认证，才能使用免费通道


# 结束