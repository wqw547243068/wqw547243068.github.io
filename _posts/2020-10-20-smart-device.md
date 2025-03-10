---
layout: post
title:  "智能硬件-Smart Device"
date:   2020-10-20 20:30:00
categories: 技术工具 新技术
tags: Web HTTP MQTT IoT 物联网 智能家居 5G 智能音箱 纳什均衡 ZigBee adb otg 手机  电脑协同 分屏 边缘计算 硬件 对话 大模型 传感器 聆思 对话
author : 鹤啸九天 
excerpt: 智能硬件应用，如智能家居相关知识点
mathjax: true
permalink: /smart_device
---

* content
{:toc}



# 智能家居


## 物联网技术

【2024-11-15】轻玩科技智能家
- 10年前, 想玩单片机物联网, 必须从模电、数电开始学习，然后，微机原理、单片机原理
- 现在不用，只要会电脑，2-3天就能上手，因为市面上有各种各样的现成模块

|需求|组件|方法|其它|
|---|---|---|---|
|植物自动浇水|继电器+水泵+土壤检测模块|||
|语音控制空调|单片机+红外发射模块+智能音箱|||
|智能安防摄像头|wifi摄像头模块|20多元,联网后就可以把画面传输到手机||
|||||

单片机程序不会写？不用担心
- 单片机程序不如软件开发复杂，一般就10-20行代码
- 不想考试，不用背，应用时复制修改即可

## 发展阶段

智能家居是一个非常火爆热门的物联网行业，自从苹果发布了**Homekit**和谷歌收购**Nest**之后，将智能家居彻底引爆。
智能家居行业，按照物物连接可以分为3个阶段：**单品连接**、**物物联动**、**平台集成**；目前智能家居行业正处于第二阶段。

### 第一阶段：单品连接 —— 单纯的物人连接

这个阶段涌现了非常多的单品，这类单品更乐意被叫做**智能硬件**而非单品。在智能单品时代，小米是佼佼者。
- 产品：以小米为例，小米先后推出了小蚁摄像头、小米门窗磁、小米报警器、小米音箱、小米灯泡；其它厂商有推出空气球（预报天气）。

这个阶段智能家居的粘性是非常低的，最开始的新鲜感会在使用几次之后慢慢消失。
- 常见的单品有：智能灯、智能门锁、智能音箱、智能插座、智能冰箱、智能窗帘、智能洗衣机、智能空调、智能插座、智能电饭煲、智能扫地机器人。
这个阶段是单纯的物人相连。

### 第二阶段：物物联动

在这个阶段中，企业整合自己旗下所有的单品，使得各产品之间能够联动。比如当智能门锁正常打开后灯自动亮起之类。

除了企业自身整合外，智能家居的集成商可以利用某个企业的开放平台，将其它第三方产品整合到该企业的平台中，并未最终用户提供定制化的联动场景。这个阶段在某些厂商、集成商的努力下，达成了部分物物相连。
- 比如A厂商下的所有单品都能够集成到某个APP下，或者某个集成商能够将多个公司的产品整合到一个系统下。前者以小米为主的，它的APP能够控制小米旗下大部分单品。后者是以欧瑞博、Control4等厂商的集成商为代表，将他们旗下的单品和其它公司的单品整合到他们开发的系统中。

### 第三阶段：平台集成

根据统一的标准， 使各企业单品能相互兼容， 目前还没有发展到这个阶段。即A公司的网关能够控制B公司的灯，C公司的传感器能够指挥D公司的扫地机器人打扫卫生。

这个阶段是要求万物互联，真正的连接，不是依赖于某个集成商或者某个厂商，而是通过某个协议完成了万物互联。
目前并没有一种通用的协议或者平台能够完成万物互联或者智能家居产品的互联。Wi-Fi和蓝牙虽然是全球共用的，但是由于自身原因还不能一统江湖（前者功耗高、支持的设备有限；后者是最近才支持mesh网络，还未普及）。
需要注意的是，单品和物物联动并非是严格按时间顺序推进的。当我刚入行时，已经存在物物联动的智能家居系统，而之后才有小米将智能硬件带到一个新的热度。

## 国内智能家居现状

【2019-06-05】目前国内的智能家居市场是两极分化：**厂商热用户冷**
- 智能家居厂商这边是热闹非凡，地产公司、家电公司、互联网公司和AI公司纷纷进入到这个行业；但是消费者这边，却冷清了很多。
- 相关数据显示，目前欧美国家智能家居的渗透率已超过35%，日本和韩国的渗透率超过25%，而在中国，这个数字还未达到5%。

消费者：难决策、价格高、消费者难接触、不智能
厂商：厂家分为以小米为代表的智能硬件/单品出身（先做单品，然后做一个超级APP管理所有单品，再进化成系统）和以欧瑞博为代表的以智能家居系统厂商（自建系统/平台，然后对接第三方厂家产品）。

智能家居未来
1. **多模态**：智能家居与其它AIOT行业不一样的地方是要求多模态的交互方式和多模态的协作（物物之间）。
  - 柒灵：所谓多模态交互即多种本体交互手段结合后的交互，例如将多种感官融合，比如文字、语音、视觉、动作、环境等。
  - 人与人交流的过程中，表情、手势、拥抱、触摸，甚至是气味，无不在信息交换的过程中起着不可替代的作用。显然，智能家居的人机交互势必不止语音一个模态，而是需要多模态交互并行。
  - 例如智能音箱如果看到人不在家，那就完全不需要对电视里误放出的唤醒词进行响应，甚至可以把自己调到睡眠状态；一个机器人如果感觉到主人在注视他，那么可能会主动向主人打招呼并询问是否需要提供帮助。多模态处理无疑需要引入对多类传感器数据的共同分析和计算，这些数据既包括一维的语音数据，也会包括摄像头图像以及热感应图像等二维数据。这些数据的处理无不需要本地AI的能力，也就对边缘计算提出了强力的需求。
2. **身份鉴别**
  - 智能家居系统目前普遍无法识别你是你，反而有一些智能单品能够识别。目前，通过智能门锁或者摄像头能够确认身份，但是智能门锁只在出入口，摄像头一般用于周界和出入口（虽然也有甲方曾经要求室内安装大量监控摄像头的）；而如果在室内，又该如何鉴别身份呢？
  - 人类一般是通过听觉和视觉去识别人。在智能家居系统中，是存在不少能够识别你的设备，比如带摄像头的电视机、智能音箱。与身份鉴别的场景有很多。比如回到家中，背景音乐或者智能音响包括照明都会根据你个人的喜好进行调整，这个调整是根据你的日常行为、性别、爱好、回来的时间、天气等因素并结合特定日期（生日、纪念日等）经过自我学习完成的，这个的目标是个性化。
  - 另外一个与安防有关的场景。当晚上布防之后，如果你起来活动，智能家居系统能辨识到你在活动，在你活动区域附近的安防传感器将自动屏蔽。当你离开该区域后，智能家居系统会解除屏蔽——这样做的好处是避免你去手动布撤防。
3. **定位**
  - 安防的场景其实与定位是有一定的关系，毕竟智能家居系统不仅要认出你还要认出你在哪（卧室、厨房、客厅）。可以为智能家居系统赋予3D建模功能，让其能够掌握整个家居的结构，可以将这个结构赋予给其它设备，比如扫地机器人、或者智能音箱等可能移动的设备。
  - 比如，当你在厨房一边做饭一边听智能音箱播放的音乐，此时智能音箱突然插播了一段语音“前门有陌生人来访”，并且智能音箱的屏幕上显示门口监控图像。你通过监控图像看到原来是邻居或者某个朋友，甚至可能是外卖、快递小哥等等。你对智能音箱说打开门让他进来或者对智能音箱说“快递小哥，帮我把快递放到门口，一会儿我去拿”。此时，智能音箱会将这段话通过门铃（假定带语音功能）告知门口等待的人。同样，如果在客厅看电视时，客厅电视上将出现一个小窗口显示门口监控，客厅的智能音箱通过语音提示“门外有人来访”的提示音，其它房间的电视和智能音箱并不会发出相应提示；甚至当多个电视、智能音箱在使用时，智能家居系统能够判断到底让哪个地方的电视或智能音箱发出提示（比如年轻人优先、其次是老人和小孩）。如果屋里没人，那么当有人按门铃时，无论电视或者智能音箱都不会提供有人来访的提示。
4. **连接**
  - 智能家居是人与物的连接，智慧小区是服务与人、与各家智能家居系统的连接。小区通过各类软硬兼施设施提供更人性化的服务给小区的业主。
  - 如，你设定了明天9点到某地与客户洽谈的日程安排。智能系统根据你的日程为你设定了早晨7点起床的闹钟，7点30分外卖送到，8点下楼（楼下有车辆送到小区东门），8点10东门上车。智能系统根据住所到目的地距离选择了乘车出行方式，行程是40分钟。由于你的车辆限号，于是智能系统根据你的叫车习惯选择了滴滴出行，并根据你的喜好选择了专车（不是快车也不是出租）。鉴于小区内提供了免费接送的服务，于是智能系统告知小区8点到楼下等你。依次类推，到闹钟设定——原本你设定的闹钟是7点30份，那么由于智能系统判断你需要7点起床才能赶上行程，故智能系统将会屏蔽明天7点30份的闹钟（对后天没有影响）。
5. **去中心化**和**中心化**
  - 根据纳什均衡原理，一个组织当中有一个稳定的状态，这时候群体做出的决策是最优的，任何其他的选择都会打破这样的均衡状态。人类社会恰恰存在着多种的纳什均衡——有时偏向集权，有时又偏向分权。纳什均衡其实告诉我们，群体的组织形式会在单一中心和去中心化中找到平衡点，而且这样的平衡点不止一个。
  - 那么在智能家居行业中，到底是中心化还是去中心化呢？目前的趋势还是**中心化**，就算将来每个设备都是智能设备甚至都有边缘计算的能力，那将来可能还是有一个中心去负责协调。
  - 把每个传感器、每个终端设备当做一个个人来看，把家居当做一个会议室，每个人都在自说自话；那么，会有结论么？不会。这个互相传递的命令，就像是闹市中的各类声音一般；故很大程度上还是会有一个中心，并且允许其它中心的存在。比如某个传感器发现地面脏了，可以发送命令给扫地机器人扫地。
  - 举例，当机器人发现主人不在家后自动进入了休眠状态。那么问题来了，机器人怎么发现主人不在家的？
    - 方式一：机器人在所有房间里转了一圈，没有发现主人在家，于是回到之前位置然后进入休眠并告知其它设备进入休眠。
    - 方式二：机器人在屋里喊了一嗓子“你们谁看见主人了？”（广播），所有设备告诉它没有看到或者某个设备告诉它主人外出了（比如摄像头或者音箱），于是机器人进入休眠。
    - 方式三：智能家居系统发现主人不在家后，将消息告知了机器人，于是机器人进入休眠。
    - 方式一和方式二可以看做是去中心；方式三是中心化。
6. **数据分析**
  - 如果某个智能马桶发现某个人最近一段时间每晚都要去好几次厕所，它能够推断出这个人的身体有问题么？目前的答案是：不能判断。原因是：现在的智能马桶并不能对自己产生的数据进行分析，且目前也不能判定使用者的身份。但是，一些医疗产品已经具备了基础的数据分析，他们能够根据用户的生理状态提供一些建议或帮助。由此推断，智能硬件或者智能系统有必须主动分析本设备或本系统产生的数据，并提供相关建议给用户。
7. **隐私和数据保护**
  - 智能马桶发现某个人身体可能有问题的用例，如果智能马桶将该信息传到厂家云平台进而告知相关药店或者医院，导致这个人一段时间内看到很多关于如何治好xx的广告或商品，甚至莫名其妙接到某些推送。这样的情况，是否允许发生呢？由于智能设备或智能系统保有用户大量的个人数据，并且无论智能设备或智能系统都需要定期与云平台通讯，如果通讯内容被不法分子获取，那么可能会被某些别有用心的人利用。为此，每个厂家都应该切实保护数据——无论是数据传输过程中亦或者是存储数据的云平台或者是产生的数据的设备。
  - 如果想实现智能，需要大量数据。但是出于隐私和数据保护的缘故，智能硬件或者智能系统又不能将个人隐私和数据直接传递到某个云平台，那么该如何进行模型训练呢？
    - 针对隐私：个人的数据是隐私，但是一群人的数据特征就不再是隐私。比如某个人喜欢买智能硬件和某个地区80%的男人喜欢购买智能硬件，前者涉及个人，后者不涉及个人（是可以公开的）。因此可以将个人化的数据脱敏后上传到云端，但是这个过程务必取得消费者的认同。
    - 对于模型训练的做法：可以利用边缘计算，将数据在数据本地进行初步训练，然后将结果返回到云平台进行再次训练，最终将模型下发至相应终端设备或系统。

## 智能家居行业

- [小度、天猫精灵、小爱同学硬件设备接入比较](https://baijiahao.baidu.com/s?id=1630149386111236552&wfr=spider&for=pc)
- [天猫精灵、小爱同学平台研究](https://www.jianshu.com/p/d4975edbcb52)
- 开发者网站
  - [天猫精灵设备接入](open.aligenie.com/)
  - [百度智能设备接入](dueros.baidu.com/open)
  - [小米智能设备接入](iot.mi.com/new/index.html)
- 主流厂家对AI智能的重视成都还是够了的，其中百度和阿里在界面上能够看出国际大厂的风度。小米作为后起之秀明显后劲不足。腾讯在物联网和智能家居事业上已经被逼到了角落，只有被忽略了。而华为，别人的重心根本不在这。网站有内容也足够，只是有的时候文档打不开。
- 百度、小米、阿里均支持硬件设备和云对云的接入方式,智能硬件直接接入方式相同，都需要注册为开发者，完成产品后需要平台认证，三大厂商均提供推荐的硬件模组。


### 经验

【2023-10-7】[突发，AI大牛景鲲离职百度！CIO李莹接任小度CEO](https://mp.weixin.qq.com/s/-YmoY3qVqvo2sWyI1IWFRw)
- 百度集团副总裁、百度集团首席信息官（CIO）`李莹`担任小度科技CEO，向集团董事长兼CEO李彦宏直接汇报。
  - `李莹`主导了百度如流等产品基于文心大模型的重构；最新消息是，换帅之后，李莹将进一步强化大模型对小度产品的加持。
  - 2003年，李莹开始在百度实习，2004年毕业后正式入职百度网页搜索部，先后带领自然语言处理、网页搜索相关性、spider等业务。
  - 2011年至2018年期间，李莹先后任职于互联网数据研发部、推荐与个性化部、复合搜索部、知识图谱部、AI技术生态部，带领了多项业务。
  - 到2018年3月，李莹调任百度地图事业部总经理，正式接手百度地图业务，主导负责传统互联网地图的智能化升级，陆续发布智能定位、智能语音、语音定制等多个产品。
  - 2020年2月，李莹被任命为百度集团首席信息官（CIO）。
  - 同年5月，百度宣布晋升李莹为百度集团副总裁，继续担任百度集团CIO和地图事业部总经理，并继续向CTO王海峰汇报。
  - CIO任期内，李莹着手建立了以AI和知识管理为核心的智能工作平台“如流”。
  - ChatGPT引发大模型狂热后，百度重压大模型，百度如流也在李莹的主导下，完成了基于文心大模型的重构。
- 小度原CEO`景鲲`因个人原因即将辞任



#### 智能音箱

小度音箱成智能家居入口也挺好
- 绑定QQ音乐后，如果没有小度会员，也只能听1分钟。我也买了3个小度，2个小度会员，成电子垃圾了
- 核心诉求诉求都是给娃听音乐和故事 对音质要求没太大要求
- 整体生态+增值服务做得都不好 没有盈利能力和空间，听音乐 找内容都需要绑定其他平台和付费
- 不过单价低，利润低。如果自己没有订阅收费，又没法和其他利润产品有效互动的话，体量确实会堪忧。

小米系列用的挺好的， 主要是用来 控制家电，可以联动，是真正的生态

随着ai的进步，小孩陪伴可能真是一个爆点。
- 这个强需求家长也舍得花钱。定价直接上升一个数量级。能陪孩子下棋，辅导孩子做功课，解答孩子的疑问。带来的价值是有本质提高的。
- 元萝卜下棋机器人，为不同的棋分别开发产品，然后一个卖几千块。这太不通用了，但其实摄像头机械臂它都有。如果能通用化能下好几种棋。监督督促孩子，孩子学习坐姿不端正会提醒，作业字迹有进步会表扬，更进一步还能给孩子批改作业讲解。

音响放在客厅里就是个**娱乐**工具，<span style='color:red'>娱乐没有内容支持，该跪就跪</span>。至于孩子学习，那是**学习机**，**生产力**工具，目前在 pad 生态下，还是以 **app** 形式居多，本来家长或多或少都买过一些学习 app

#### 硬件产品思考

还是得造硬件, 现在就是geek产品，用来磨练产品和技术。小众市场试水
- 利润高，产品化强，端到端，使用简单。
- 长期可以造居家服务的机器人. 

硬件生意难做的地方
- 硬件**负毛利**的话，卖得越多亏的越多。由于有**活跃比例**的限制，很难用内容付费补回来。
- toB 售后多维保重，销售成本高，没有啥超级大单或者核心资源降销售成本的话，也挺难做的，会亏得感人
- 硬件的通用化也难做，成本飙升效率狂降. 等你啥都解决了，上游供应商还会来咬你一口
- 所以硬件老炮们看不懂互联网公司出来搞硬件的，互联网的同学们也很难理解硬件行业的保守, 见面大概率是相谈甚欢，然后内心里互道一声傻X

硬件创业的另一个瓶颈就是差异化在物理限制的前提下，突破时间点依赖实验进展，趋势看对了，潮流跟上了，大部分团队也处于躺不平也立不起来的45度角的状态

### 百度

百度：标准模组为MT8516 Cortex A35的开发板，因为需要安装DuerOS所以处理器和内存都有要求。另外一些高级的模组是采用树莓派制作的。

[图](https://pics0.baidu.com/feed/9a504fc2d56285352f0dfd8a9156d4c2a5ef63ed.jpeg?token=6e2256259ecc4ec60f53bbf131390e3d&s=D2827C2B1D44FC113EF8F5D90200D0B6)

![](https://pics0.baidu.com/feed/9a504fc2d56285352f0dfd8a9156d4c2a5ef63ed.jpeg?token=6e2256259ecc4ec60f53bbf131390e3d&s=D2827C2B1D44FC113EF8F5D90200D0B6)

### 天猫精灵

[天猫精灵](https://open.bot.tmall.com/)

- **天猫精灵**是阿里巴巴人工智能实验室推出的AI智能产品品牌。天猫精灵内置AliGenie操作系统，AliGenie生活在云端，它能够听懂中文普通话语音指令，目前可实现智能家居控制、语音购物、手机充值、叫外卖、音频音乐播放等功能，带来人机交互新体验。依靠阿里云的机器学习技术和计算能力，AliGenie能够不断进化成长，了解使用者的喜好和习惯，成为人类智能助手。
- AliGenie硬件接入开放平台（AliGenie Intelligent Devices Platform），是AliGenie为企业级用户提供AI语音解决方案的开放平台。相关企业用户可以在完成开发者认证后，通过平台来申请获取AliGenie SDK、模组、麦克风阵列等能力和技术支持。
- 天猫精灵蓝牙mesh软件基础规范,定义BLE Mesh通用模块的软件规范，指导模块厂家软件设计并接入天猫精灵。
- 云云自助接入模式，鉴权流程：
  - AliGenie在开发商开放平台或者其他第三方平台注册一个应用，获取到相应的Client id 和Client secret
  - AliGenie 应用向开发商OAuth2.0服务发起一个授权请求
  - 开发商OAuth2.0服务向用户展示一个授权页面，用户可进行登陆授权
  - 用户授权AliGenie客户端应用后，进行回跳到AliGenie 的回调地址上并带上code相关参数
  - AilGenie回调地址上根据code会去合作方Oauth 的服务上换取 access_token
  - 通过access_token，天猫精灵设备控制时通过该access_token进行访问合作方的服务

  按照功能分类，包括手表、故事机、耳机、电视和音箱，提供通用设备的SDK
  ![](https://upload-images.jianshu.io/upload_images/2160113-599f363d7a1cb814)

### 小米小爱

普通MCU需要连接小米通用模组（ESP8266或者ESP32），提供Linux、Android的SDK，[图](https://pics2.baidu.com/feed/728da9773912b31b5bf687ea7ba0947ed8b4e19d.jpeg?token=e547f606ffa2b0e542dc57883c3f1dae&s=15F068320DE9780146D1C8470200C0F2)

![](https://pics2.baidu.com/feed/728da9773912b31b5bf687ea7ba0947ed8b4e19d.jpeg?token=e547f606ffa2b0e542dc57883c3f1dae&s=15F068320DE9780146D1C8470200C0F2)


### 贝壳

- 2019年6月，贝壳就成立了一只硬件团队Ke IoT Lab，主要围绕人、房、店三大核心数据触点，并在当年推出了智能硬件产品“贝刻手环”
- 2020年11月发布了升级款产品“贝刻手环Air”，一款面向房产经纪从业人员的智能手环产品。
- 【2021-7-7】[贝壳发布智能家居品牌,让家装公司产品升级更高效](https://t.cj.sina.com.cn/articles/view/7504419610/1bf4c5b1a00100u6ow)


### Home Assistant

【2024-4-14】Frontend for Home Assistant 智能家居控制开源项目

[Python打造的智能家居神器：Home Assistant](https://mp.weixin.qq.com/s/2gR1dYxl_TAbCVMzn97x2w)
- [Demo](https://demo.home-assistant.io/#/lovelace/home)
- 代码 [Home Assistant](https://github.com/home-assistant/core)

Home Assistant以Python为开发语言，遵循开放源代码协议，专注于本地控制与隐私保护，成为全球众多科技爱好者和开发者的首选，旨在打造一个中心化的智能家居系统，它可以连接和控制多种设备，包括照明、气候控制、多媒体播放器、安全系统等。与商业化智能家居产品相比，Home Assistant强调数据的本地处理与存储，增强个人隐私保护。

用户应该完全拥有和控制自己的数据，这是它区别于其他智能家居解决方案的核心优势。所有设备的信息和操作都存储在本地，不需要通过第三方服务器传输，从而避免了数据泄露的风险。

在智能家居系统中，各种传感器和设备可能会收集敏感信息。Home Assistant严格遵循隐私保护原则，用户完全掌控个人信息，无需担心信息被未授权使用或出售。

Home Assistant通过模块化的设计，支持数百种不同的智能家居设备。其核心组件为用户提供了一个统一的操作界面，而各个插件和集成则可以通过编写少量代码来添加更多设备支持。
1. 核心组件：负责核心的任务调度、状态管理和事件触发等。
2. 插件系统：允许社区成员贡献代码，支持更多第三方设备和服务。
3. 自动化规则：用户可以设置基于时间、事件或其他条件的自动化任务。

Home Assistant的发展速度极快，截至目前，已经可以兼容上千种不同的智能设备。从照明调节、温度控制到安防监控，Home Assistant无不体现了对智能生活的深刻理解和技术上的不断迭代。例如：
1. 家庭影院自动化：当用户开始观看电影时，自动调暗灯光，关闭窗帘，打开投影仪和音响。
2. 能源管理：实时监控家中的能源消耗，根据使用情况自动调节暖气和空调设备，以节约能源。

## 智能家居产品

物联网在智能家居的应用

### 1、家庭安防：实时查看室内情况

安全监控系统是物联网在智能家居应用中的重中之重，通过监控摄像头、窗户传感器、智能门铃(内置摄像头)、红外监测器等有效连接在一起，用户可以通过手机、Ipad随时随地查看室内的实时情况，保障住宅安全。

### 2、智能插座：远程控制开关电器，追踪电源消耗

插座作为家用电器获得电力的基础接口，如果它具备连接互联网的功能，那么其他电器也同样可以实现。通过远程控制开关电器设备，并追踪电源消耗，帮助用户更好地节约能源。

### 3、灯光：随心所欲变换场景

通过手机应用实现开关灯、调节颜色和亮度等操作，随心所欲地变换你想要的场景氛围。

### 4、空调控温：远程温控，个性化定制

在酷热的夏季和寒冷的冬季，住宅温度的调节十分重要。依靠物联网技术，我们可以通过手机实现远程温控操作，控制每个房间的温度、定制个性化模式，甚至还能根据用户的使用习惯，通过GPS定位用户位置实现全自动温控操作。

### 5、智能洗衣机：远程控制洗衣机，智能洗涤程序

根据衣物的污渍程度、重量推算出洗衣液的用量，并注入滚筒，同时执行合适的智能洗涤程序，还能在洗涤后自动执行烘干熨烫，你所需做的只是把衣服丢进去，完事后拿出来叠整齐便可。此外，通过手机应用程序，还可以远程控制洗衣机，掌握洗衣过程。

### 6、智能冰箱：传送食品信息，更新购物清单，给出菜谱建议

只需看到显示屏就能知道冰箱内的库存情况，还可以把冰箱内的温度、库存以及将要过期的食品信息传送到手机应用上，甚至可以根据库存情况更新购物清单，自动下载菜谱。此外，用户通过设定家庭成员的基本身体数据，便可自动给出健康合理的菜谱建议。

### 7、智能烤箱：手机应用控制烤箱温度，下载菜谱

在传统烤箱上加入WIFI功能，通过手机应用控制烤箱温度，包括预热和加温，甚至可以下载菜谱，实现更具针对性的烹饪方式。不仅仅是烤箱，一些高端咖啡机、调酒机也可配备WIFI功能，并且厂商会不定期更新咖啡或鸡尾酒菜单，这样你在家也能做出咖啡厅、酒吧的味道。

### 8、智能牙刷：刷牙时间提示，分析口腔健康

牙刷通过蓝牙4.0与智能手机连接，实现刷牙时间、位置提醒;根据用户刷牙的数据生成分析图表，估算出口腔健康情况。

### 9、智能体重秤：提供健康建议，实现更精准、无缝化健康监测

通过内置传感器，实现血压、脂肪量甚至空气质量的检测，并传输至应用程序为用户提供健康建议，更可以与运动手环、智能手表等互联，实现更精准、无缝化的个人健康监测。

### 10、智能马桶：自动开关，智能分析

除了通过内置接近传感器实现自动开关盖操作，通过内置智能分析仪还能对排泄物进行分析，并将分析结果传送至手机和显示屏应用，让用户随时了解自身健康状况。

### 11、智能植物监测仪：监测湿度、温度，推送浇水时间

将仪器放置到花盆的土壤上，就能够监测其湿度、温度等，并通过应用程序推送告诉你什么时候该浇水了，可谓是"植物杀手"们的福音。

### 12、智能鱼缸：自动投喂饲料，自动定时照明杀菌

养鱼最麻烦的就是需要定时投喂饲料、照明杀菌、充气给氧。而智能鱼缸，可以帮助你每天自动定时定量投喂饲料;自动定时开关照明杀菌灯;监测鱼缸中水的pH值、盐度以及水温，并可将这些信息数据通过手机应用显示出来

# 技术篇

- Zigbee、WIFI、bluetooth之间的区别和联系[图](https://imgconvert.csdnimg.cn/aHR0cDovL3MzLjUxY3RvLmNvbS93eWZzMDIvTTAwLzZGLzg5L3dLaW9tMVdmTlh5VHRYM2VBQUlkZC12MmFWQTE1Ny5qcGc?x-oss-process=image/format,png)
- ![](https://imgconvert.csdnimg.cn/aHR0cDovL3MzLjUxY3RvLmNvbS93eWZzMDIvTTAwLzZGLzg5L3dLaW9tMVdmTlh5VHRYM2VBQUlkZC12MmFWQTE1Ny5qcGc?x-oss-process=image/format,png)


## 传感器

详见站内专题: [传感器](sensor)

## ZigBee

在蓝牙技术的使用过程中，人们发现蓝牙技术尽管有许多优点，但仍存在许多缺陷。对工业，家庭自动化控制和遥测遥控领域而言，蓝牙技术显得太复杂，**功耗大**，距离**近**，组网规模**太小**等，……而工业自动化对无线通信的需求越来越强烈。正因此，经过人们长期努力，Zigbee协议在2003年中通过后，于2004正式问世了。

ZigBee，也称紫蜂，是一种低速短距离传输的无线网上协议，底层是采用IEEE 802.15.4标准规范的媒体访问层与物理层。主要特色有低速、低耗电、低成本、支持大量网上节点、支持多种网上拓扑、低复杂度、快速、可靠、安全。[图](https://img-blog.csdnimg.cn/20190320005944866.png)

由于 IEEE 802.15.4标准只定义了物理层协议和MAC 层协议，于是成立了zigbee联盟，ZigBee联盟对其网络层协议和 API 进行了标准化，还开发了安全层。经过ZigBee联盟对 IEEE 802.15.4 的改进，这才真正形成了ZigBee协议栈(Zstack)。

![](https://img-blog.csdnimg.cn/20190320005944866.png)

参考：[ZigBee简介](https://blog.csdn.net/weixin_41890971/article/details/88614696)

### ZigBee 特点

- 数据传输速率低：10KB/秒~250KB /秒，专注于低传输应用。
- 功耗低：在低功耗待机模式下，两节普通5号电池可使用6~24个月。
- 成本低：ZigBee数据传输速率低，协议简单，所以大大降低了成本。
- 网络容量大：网络可容纳 65,000 个设备。
- 时延短：通常时延都在 15ms~30ms。
- 安全： ZigBee提供了数据完整性检查和鉴权功能，采用AES-128加密算法（美国新加密算法，是目前最好的文本加密算法之一）

### 网络拓扑模型

ZigBee网络拓扑结构主要有星形网络和网型网络。不同的网络拓扑对应于不同的应用领域，在ZigBee无线网络中，不同的网络拓扑结构对网络节点的配置也不同，网络节点的类型：协调器、路由器和终端节点。

MESH网状网络拓扑结构的网络具有强大的功能，网络可以通过多级跳的方式来通信；该拓扑结构还可以组成极为复杂的网络；网络还具备自组织、自愈功能。[图](https://img-blog.csdnimg.cn/20190320092540786.png)

![](https://img-blog.csdnimg.cn/20190320092540786.png)

### 应用领域

ZigBee已广泛应用于物联网产业链中的M2M行业，如智能电网、智能交通、智能家 居、金融、移动 POS 终端、供应链自动化、工业自动化、智能建筑、消防、公共安全、环境保护、气象、数字化医疗、遥感勘测、农业、林业、水务、煤矿、石化等领域。如[图](https://img-blog.csdnimg.cn/20190320092818928.png)

![](https://img-blog.csdnimg.cn/20190320092818928.png)

## 5G

- [8分钟了解关于5G技术的一切](https://www.bilibili.com/video/BV1Dx411u74B/)
  - <iframe src="//player.bilibili.com/player.html?aid=15276094&bvid=BV1Dx411u74B&cid=24864076&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="600" width="100%"> </iframe>
- [5G时代十大应用场景](https://www.bilibili.com/video/BV1bE411Z7uX/)
  - <iframe src="//player.bilibili.com/player.html?aid=70984662&bvid=BV1bE411Z7uX&cid=122994664&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="600" width="100%"> </iframe>

5G在广覆盖、低延时和安全性能上有明显优势，这意味着5G可以作为物联网的高速公路，连接大量的物联网传感器应用，提高传输效率，覆盖更多设备，提供更多的解决方案。

## MQTT

- [MQTT官网](http://mqtt.org)，[MQTT V3.1.1协议规范](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)
- 【2020-10-24】[一文带你简单了解MQTT协议](https://zhuanlan.zhihu.com/p/152195617)
- [物联网及MQTT协议概述](https://zhuanlan.zhihu.com/p/89057819)

### 什么是MQTT

简单介绍下MQTT协议。
- `MQTT`（Message Queuing Telemetry Transport，**消息队列遥测传输**）是IBM开发的一个ISO 标准(ISO/IEC PRF 20922)下基于**发布/订阅**范式的消息协议。
- 百度百科对于MQTT协议的定义如下：
> MQTT(消息队列遥测传输)是ISO 标准(ISO/IEC PRF 20922)下基于发布/订阅范式的消息协议。它工作在 TCP/IP协议族上，是为硬件性能低下的远程设备以及网络状况糟糕的情况下而设计的发布/订阅型消息协议，为此，它需要一个消息中间件 。
- IBM在帮助石油和天然气公司客户设计有效的数据传输协议时，就出现了对MQTT这种物联网环境下的数据传输协议的需求。
- 当时，为了实现数千英里长的石油和天然气管道的无人值守监控，采取的设计方案是将管道上的传感器数据通过卫星通信传输到监控中心。
- ![](https://pic1.zhimg.com/80/v2-9eed25ea2774cddd616f16aa27fdf11c_720w.jpg)
- MQTT协议<font color='blue'>以极少的代码和有限的带宽，为连接远程设备提供实时可靠的消息服务</font>。
    - ![](https://static.runoob.com/images/mix/mqtt-fidge-2.svg)
    - 摘自：[MQTT入门介绍](https://www.runoob.com/w3cnote/mqtt-intro.html)
- 由于MQTT协议具有轻量、简单、开放和易于实现等特点。这些特点使它适用范围非常广泛。

### MQTT协议主要特性

特性如下
1. 使用**发布/订阅**消息模式，提供**一对多**的消息发布，解除应用程序耦合。
2. 对负载内容屏蔽的消息传输。
3. 使用 TCP/IP 提供网络连接。
4. 有三种消息发布服务质量(QoS)：
  - “**至多**一次” n≤1 ，消息发布完全依赖底层 TCP/IP 网络。会发生消息丢失或重复。这一级别可用于**环境传感器**数据传输这种情况。这种情况下，丢失一次读数记录也无所谓，因为不久后还会有第二次发送。
  - “**至少**一次” n≥1 ，确保消息到达，但消息重复可能会发生。
  - “**只有**一次” n=1 ，确保消息到达一次。这一级别可用于如下情况，在**计费系统**中，消息重复或丢失会导致不正确的结果。
5. 小型传输，开销很小（固定长度的头部是 2 字节），协议交换最小化，以降低网络流量。
6. 使用 Last Will 和 Testament 特性通知有关各方客户端异常中断的机制。

### TCP与MQTT

- 诞生时间
  - TCP协议诞生于1974年冷战期间。
  - MQTT诞生于1999年互联网初期，TCP协议比MQTT协议诞生早了25年。
  - Ashton提出IoT概念也是在1999年，因此MQTT协议生逢其时。当时MIT Auto-ID Labs的Kevin Ashton为了把宝洁的供应链上的RFID标签和互联网连接起来，在1999年第一个提出了IoT这个概念。
- 协议位置
  - TCP是OSI第四层的传输层协议。
  - MQTT是基于TCP的七层应用层协议。
  - ![](https://pic3.zhimg.com/80/v2-0f8f1c9dee37ec4d463e8368130967a6_720w.jpg)
- 协议定位
  - TCP设计考虑的是面向连接的、可靠的、基于字节流的传输层通信协议。
  - MQTT则是在低带宽高延迟不可靠的网络下进行数据相对可靠传输的应用层协议。
- 设计思想
  - TCP的核心思想是分组交换。
  - MQTT的核心思想是简单并适应物联网环境。
- 传输单位
  - TCP的传输单位是packet，当应用层向TCP层发送用于网间传输的、用8位字节表示的数据流，TCP则把数据流分割成适当长度的报文段，最大传输段大小（MSS）通常受该计算机连接的网络的数据链路层的最大传送单元（MTU）限制。
  - MQTT的传输单位是消息，每条消息字节上限在MQTT Broker代理服务器上进行设置，可以设置超过1M大小的消息上限。
- 技术挑战
  - TCP需要解决的问题是在IP包传输过程中，处理异构网络环境下的网络拥塞、丢包、乱序、重复包等多种问题。
  - MQTT解决的问题是，在低带宽高延迟不可靠的网络下和资源有限的硬件环境内，进行相对可靠的数据传输。
- 服务质量
  - TCP是一个可靠的流传输服务，通过ACK确认和重传机制，能够保证发送的所有字节在接收时是完全一样的，并且字节顺序也是正确的。
  - MQTT提供三种可选的消息发布的QoS服务等级。MQTT客户端和MQTT代理服务器通过session机制保证消息的传输可靠性。开发人员可以根据业务需要选择其中一种。
- 应用案例
  - TCP用于许多互联网应用程序，如WWW、email、FTP、SSH、P2P、流媒体。MQTT也是基于TCP的。
  - MQTT可以用于物联网数据传输、IM聊天软件等。

- 摘自：[你不知道的MQTT物联网协议起源——基于卫星通信的石油管道远程监控](https://zhuanlan.zhihu.com/p/69124423)


### MQTT协议原理


#### 发布、订阅工作模式

- 工作模式：
  - ![](https://pic1.zhimg.com/80/v2-f3a8f6802d2b98d22141a9b29fe6ac44_720w.jpg)
- 举例：
  - 温度传感器发布温度值到温度的主题，如果有终端订阅看温度这个主题，他就会收到代理转发的温度值
  - ![](https://pic2.zhimg.com/80/v2-bd813407fbbad91fda0cc6c9ea5c3dc9_720w.jpg)
  - 这种模式取消了硬件、客户端、服务器的概念，服务器成为了一个消息转发的代理，终端硬件和消息接收者都称之为客户端，他们都可以发布或订阅主题。如终端硬件可以发布“温度”主题下的消息，所有订阅了此主题的客户端都可以收到此消息推送，再如终端硬件订阅了“空中升级”的主题，如果有硬件驱动升级的推送，硬件就可以收到此消息，然后进行升级。

- 这种模式的优点：
  - A、空间上去耦合：信息发布者和信息接收者不需要建立直接联系，不需要知道对方的IP地址，端口等信息
  - B、时间上去耦合：发布者和接收者不需要同时在线。
- 这种模式的缺点：
  - A、发布者、接收者必须订阅相同的主题，
  - B、发布者并不确定接收者是否接受到了推送

#### MQTT协议实现方式

- 实现MQTT协议需要客户端和服务器端通讯完成，在通讯过程中，MQTT协议中有三种身份：**发布者**（Publish）、**代理**（Broker）（服务器）、**订阅者**（Subscribe）。其中，消息的发布者和订阅者都是客户端，消息代理是服务器，消息发布者可以同时是订阅者。
- MQTT传输的消息分为：**主题**（Topic）和**负载**（payload）两部分：
  - （1）Topic，可以理解为消息的类型，订阅者订阅（Subscribe）后，就会收到该主题的消息内容（payload）。
  - （2）payload，可以理解为消息的内容，是指订阅者具体要使用的内容。
- MQTT会构建底层网络传输：它将建立客户端到服务器的连接，提供两者之间的一个有序的、无损的、基于字节流的双向传输。
- 当应用数据通过MQTT网络发送时，MQTT会把与之相关的服务质量（QoS）和主题名（Topic）相关连。

#### MQTT客户端

一个使用MQTT协议的应用程序或者设备，它总是建立到服务器的网络连接。客户端可以：
- （1）发布其他客户端可能会订阅的信息。
- （2）订阅其它客户端发布的消息。
- （3）退订或删除应用程序的消息。
- （4）断开与服务器连接。


#### MQTT服务器

MQTT服务器以称为“消息代理”（Broker），可以是一个应用程序或一台设备。它是位于消息发布者和订阅者之间，它可以：
- （1）接受来自客户的网络连接；
- （2）接受客户发布的应用信息；
- （3）处理来自客户端的订阅和退订请求；
- （4）向订阅的客户转发应用程序消息。

### 主题

- ![](https://pic3.zhimg.com/80/v2-83bcfc0e8b2ccdcf9d433cf6fe13a286_720w.jpg)
- 主题通配符：（订阅消息时使用）
  - 单级通配符 +：+可以匹配单级，表示该级可以是任意主题不受限定；
  - 多级通配符 #：#可以匹配多级，通常出现在主题末尾，表示某一类主题下的所有子主题
  - 系统保留topic $：以$开头的是服务器保留的主题
- ![](https://pic1.zhimg.com/80/v2-30bc427cedbee1e13405ec1060f1d50c_720w.jpg)


### MQTT协议中的订阅、主题、会话

- （1）**订阅**（Subscription）。
  - 订阅包含主题筛选器（Topic Filter）和最大服务质量（QoS）。订阅会与一个会话（Session）关联。一个会话可以包含多个订阅。每一个会话中的每个订阅都有一个不同的主题筛选器。
- （2）**会话**（Session）。
  - 每个客户端与服务器建立连接后就是一个会话，客户端和服务器之间有状态交互。会话存在于一个网络之间，也可能在客户端和服务器之间跨越多个连续的网络连接。
- （3）**主题名**（Topic Name）连接到一个应用程序消息的标签，该标签与服务器的订阅相匹配。
  - 服务器会将消息发送给订阅所匹配标签的每个客户端。
- （4）**主题筛选器**（Topic Filter）一个对主题名通配符筛选器，在订阅表达式中使用，表示订阅所匹配到的多个主题。
- （5）**负载**（Payload）消息订阅者所具体接收的内容。

#### MQTT协议中的方法

MQTT协议中定义了一些方法（也被称为动作），来于表示对确定资源所进行操作。这个资源可以代表预先存在的数据或动态生成数据，这取决于服务器的实现。通常来说，资源指服务器上的文件或输出。主要方法有：
- （1）Connect。等待与服务器建立连接。
- （2）Disconnect。等待MQTT客户端完成所做的工作，并与服务器断开TCP/IP会话。
- （3）Subscribe。等待完成订阅。
- （4）UnSubscribe。等待服务器取消客户端的一个或多个topics订阅。
- （5）Publish。MQTT客户端发送消息请求，发送完成后返回应用程序线程。


#### 消息质量级别QoS

- （1）QS0 至多发一次。不管消息有没有收到，都不会重发。这是比较常用的质量级别，适用于很多不需要太严谨数据的场景
- （2）QS1 至少发一次。带有标志位，确保消息肯定被接收到，但有可能接受到重复消息。
- （3）QS2 只接受一次。具有严谨的信息确认，可以确保消息发送有且仅有一次 ，但对数据量的消耗较大，实现过程更复杂，适应于对数据有严格要求的场景。

![](https://pic2.zhimg.com/80/v2-ebe13ce6532d20f54d8d11d92fdc0acd_720w.jpg)

### MQTT数据格式

MQTT消息组成
- 一个MQTT消息由三个部分组成：固定头、可变头、负载。


### 建立连接

![](https://pic2.zhimg.com/80/v2-960a7e7f80cc86db4493cfd4ba9d45ed_720w.jpg)


# 实战


## AI 对话开发套件

大模型应用开发

聆思智能 提供的开发套件
- [大模型时代下的智能硬件新玩法-哔哩哔哩](https://b23.tv/wUFCCng)
- 套件已经预先烧录了程序，长按屏幕图标进入对应示例，初次上手推荐使用大模型多模态这个示例

- 大模型多模态配网可以参考文档的配网[说明部分](https://docs2.listenai.com/x/2V18-j2v2)
- 二次开发参考文档部署开发环境
  - [环境搭建](https://docs2.listenai.com/x/ZgVUIzY6M) 
  - [下载SDK](https://docs2.listenai.com/x/GvIW8tsaE)
- [代码库](https://cloud.listenai.com/CSKG836746)

CSK电商小助手: 大模型开发套件接入其他大模型的指引：
- [豆包](https://blog.csdn.net/2201_75889983/article/details/140637705)
- [KIMI](https://blog.csdn.net/2201_75889983/article/details/140636577)
- 智谱清言[chatglm](https://blog.csdn.net/2201_75889983/article/details/140637948)
- [通义千问](https://blog.csdn.net/2201_75889983/article/details/140637823)
- 百度[文心一言](https://blog.csdn.net/2201_75889983/article/details/140614038)

主流大模型接入大模型套件[视频教程](https://b23.tv/ml6XGR3)

【2024-12-22】 1.77 G 的 windows 安装包执行有误
- 此 Windows Installer程序包有问题。作为安装的一部分的程序没有按预期完成。请和您的支持人员或程序包发行商联系。



### 远程遥控车

【2024-10-25】
- esp32 i2s dac麦克风输入，wav 上传云端 调用 transformer，生成 音屏文件，返回给esp32 地址，esp32 流式拉 wav i2s 播放

自制4G远程遥控车，可开出去买菜，取快递

<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=113265652795629&bvid=BV1pF1yYDEmC&cid=26184912190&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>


## 阿里云操作智能家居

- 参考视频：[物联网实战分析，阿里云app远程控制到底如何实现？数据如何传递](https://www.ixigua.com/6870431495928939016/)
- 【2021-9-29】头条自媒体用户[超子说物联网](https://www.ixigua.com/home/83150758754035/)
物联网爱好者；创作各种物联网平台使用心得
  - 示例： [做个入门小程序，App远程控制ESP8266继电器，阿里云物联网平台](https://www.ixigua.com/6931591512232821261)：使用阿里云物联网开发平台，利用mqtt应用层协议，使用app远程控制ESP8266继电器。
  - [STM32，51单片机DIY智能家居浇花器](https://www.ixigua.com/6805411318057665035)，用天猫精灵或者APP远程控制

## 智能插座

[中学生自制全站最漂亮物联网WIFI(智能?)插座](https://www.bilibili.com/video/BV1dt41187Cm/)，松果派开源硬件创始人
- <iframe src="//player.bilibili.com/player.html?aid=41300825&bvid=BV1dt41187Cm&cid=72538417&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="600" width="100%"> </iframe>



【2017-10-01】[智能家居——IoT零基础入门篇](https://www.cnblogs.com/rainmote/p/7617454.html)
DIY一个温湿度传感器：用Home Assistant&Homebridge实现了一个智能家居设备从数据采集到控制、展示。整体架构[图](https://images2017.cnblogs.com/blog/572260/201710/572260-20171001171318856-1589386057.png)
- 智能设备：**温湿度**传感器
  - ![](https://images2017.cnblogs.com/blog/572260/201710/572260-20171001172957387-911968968.jpg)
- 主控芯片：STM32F103C8T6
- 通信协议：Zigbee
- 智能网关：树莓派
- 数据存储、展示、设备控制：HomeAssistant + Home Kit
![](https://images2017.cnblogs.com/blog/572260/201710/572260-20171001171318856-1589386057.png)

Home Assistant 效果图

![](https://images2017.cnblogs.com/blog/572260/201710/572260-20171001173117919-1163730309.jpg)

搭建Web服务器时，查阅网上相关资料，无意间发下了新大陆，[Home Assistant](https://home-assistant.io/)，太符合我的需求。安装教程可[参考](https://zhuanlan.zhihu.com/p/28011522)，国内[论坛](https://bbs.hassbian.com/forum.php)

Home Kit效果图
- ![](https://images2017.cnblogs.com/blog/572260/201710/572260-20171001172645950-703912073.jpg)

智能家居控制展示图
- ![](https://images2017.cnblogs.com/blog/572260/201710/572260-20171001210827184-546554724.png)



# 结束