---
layout: post
title:  大模型时代的对话系统 Dialogue System in the Era of LLM
date:   2023-10-16 10:00:00
categories: AIGC
tags: llm 对话系统
excerpt: 大模型时代对话何去何从？
mathjax: true
permalink: /llm_dialogue_system
---

* content
{:toc}



# LLM 时代的对话系统何去何从

原文
- 公众号[版本](https://mp.weixin.qq.com/s?__biz=MjM5ODY2OTQyNg==&mid=2649769463&idx=1&sn=7dffe779f8e260f1da32338586bfd3f7)，旧版, 新版对话系统总结部分不够清晰、系统
- [知乎](https://zhuanlan.zhihu.com/p/661558522), 新版


## 引言

> 行业巨变，物换星移，阁中帝子今不在，旧朝老臣空叹息：沧海桑田，何去何从？

![](https://pic4.zhimg.com/v2-40fe0dc89c8d4d76fd475e7c641a97fb_b.jpg)

## （0）行业变革

预训练语言模型通用化蜕变后，跨界改变甚至“破坏”了N多下游应用生态，比如搜索、办公、创作、编程等，今天谈谈名噪一时的对话系统…

往期文章[智能交互复兴：ChatGPT +终端（奔驰/Siri）= ？](https://mp.weixin.qq.com/s?__biz=MjM5ODY2OTQyNg==&mid=2649769278&idx=1&sn=97a0d56dc46434353da839eadf716894)中，提到了大模型引领的AIGC海啸冲击到的各行各业。由内到外，按照三层划分：模型层→模态层→应用层

1.  模型层：文本领域（GPT系列）、图像领域（扩散模型系列）、视频、建模、多模态等
2.  模态层：文本、语音、图像、视频、行为、理解、策略、工具等，其中文本和图像最为惊艳
3.  应用层：智能对话、AI作画最为亮眼，传统行业正在被逐步颠覆，如搜索、问答、智能办公、内容创作，同时，应用商场、互联网、数字人等也被波及

![](https://pic4.zhimg.com/v2-f0c487de505a08cfbe6adb3c774fca67_b.jpg)

_上图整理于2023年6月，非最新_

从业者都在焦急的尝试自我革命，晚了就会被人革命。

面对这股AIGC浪潮，对话系统从业者“既喜又惊”。

## **（1）喜从何来：对话系统沉浮录**

### **（1.1）对话系统复兴**

对话系统始于艾伦·图灵（Alan Turing）在 1950 年提出的图灵测试 ，如果人类无法区分和他对话交谈的是机器还是人类，那么就可以说机器通过了图灵测试，拥有高度智能。

![](https://pic3.zhimg.com/v2-31b351ad370e5bbfcccc2b8bb0852f06_b.jpg)


一图总结对话系统发展史：
- ![](https://pic2.zhimg.com/80/v2-6420f742ebb95f118b1ba3c7a3cf7a71_1440w.webp)

技术实现上先后经历了三个时期：

① 第一代对话系统：基于规则
- • 1966 年 MIT 开发的 ELIZA 系统 是一个利用模版匹配方法的心理医疗聊天机器人
- • 1970 年代开始流行的基于流程图的对话系统，采用有限状态自动机模型建模对话流中的状态转移。
- • 优点是内部逻辑透明，易于分析调试，但是高度依赖专家的人工干预，灵活性和可拓展性很差。

② 第二代对话系统：基于统计学习（数据驱动）
- • 2005年，剑桥大学Steve Young 教授的基于部分可见马尔可夫决策过程（Partially  
Observable Markov Decision Process , POMDP）的统计对话系统；鲁棒性上显著地优于基于规则的对话系统，它通过对观测到的语音识别结果进行贝叶斯推断，维护每轮对话状态，再根据对话状态进行对话策略的选择，从而生成自然语言回复。
- • POMDP-based对话系统采用了增强学习的框架，通过不断和用户模拟器或者真实用户进行交互试错，得到奖励得分来优化对话策略。统计对话系统是一个模块化系统，它避免了对专家的高度依赖，但是缺点是模型难以维护，可拓展性也比较受限。

③ 第三代对话系统：基于深度学习（大量标注数据）
- •延续了统计对话系统的框架，但各个模块都采用了神经网络模型。
- • NLU：模型从之前的生成式模型（如贝叶斯网络）演变成为深度判别式模型（如CNN、DNN、RNN）
- • DST：对话状态的获取不再是利用贝叶斯后验判决得到，而是直接计算最大条件概率
- • DP：对话策略的优化上也开始采用深度增强学习模型
- • Facebook研究者提出了基于记忆网络的任务对话系统，为研究第三代对话系统中的端到端任务导向型对话系统提出了新的方向
- 2016年是对话系统复兴元年，各类神经网络模型接踵而至，NLU（自然语言理解）技术不断迭代升级，从attention到seq2seq，再到transformer，以及预训练语言模型BERT/GPT等，NLP类各类子任务的榜单不断刷新，与之关联的领域及下游应用——对话系统也随之备受关注。

![](https://pic3.zhimg.com/80/v2-1e3c6e386b0641b3843b234f69ba2632_1440w.webp)


怀着对下一代人机交互模式CUI的美好憧憬，各大厂接下来几年纷纷布局对话系统类应用：智能客服、智能音箱、智能外呼、智能座舱等等，其中智能音箱优秀代表：小米小爱、天猫精灵、百度度秘。

![](https://pic1.zhimg.com/80/v2-1cd43fdd3bc96dea9a833868f6b762b0_1440w.webp)


### **（1.2）人工智障**

然而就在这一年，一位敢于吃螃蟹的大哥按下车里的“语音控制”按钮，想让汽车帮他打个电话。一阵甜美的AI女声响起，人类首次尝试驯服语音助手的珍贵对话诞生。
-   甜美AI：请说出您要拨打的号码，或者说取消。
-   大哥：135XXXX7557。
-   因为口音问题，系统未能识别准确。
-   大哥急了，赶紧下达第二道语音指令：纠正！纠正！
-   系统也急了：969696……
-   大哥更急了：纠正，纠正，不是96！
-   大哥：（口吐芬芳）
-   系统：对不起，我没有听清。
-   大哥带着哭腔：你耳朵聋，耳朵聋啊？我说了多少遍了我都。
-   系统：请再说一次，请再说一次，请再说一次。
-   大哥：我再说最后一遍啊，135……
-   系统：对不起，再见。


![](https://pic2.zhimg.com/v2-634015b60042704e5148f7cfc0993489_b.jpg)
  

短短2分钟浓缩了六年前车机交互的真实体验与怨念，语音助手的糟糕印象就此埋下。

![](https://pic1.zhimg.com/v2-874b0dae85dd1c37ea332e7cb4385108_b.jpg)

不止车机交互，智能音箱同样“智障”连连，即便有钱有闲的大妈也被逼疯了，一口山东方言让小度频频失手，大妈也想失手摔了它。

![](https://pic2.zhimg.com/v2-92ebfa36d2d7bb838c51a49c83e05695_b.jpg)

完整视频：[https://www.douyin.com/video/7112319224978115854](https://www.douyin.com/video/7112319224978115854)

语音助手“听不见”、“听不清”、“听不懂”灾难级的系统表现，让人和机器总得疯一个。

往期文章（[ChatGPT：从入门到入行（放弃）](https://mp.weixin.qq.com/s?__biz=MjM5ODY2OTQyNg==&mid=2649768933&idx=1&sn=92345bd6e0a2fa16bb0674b7c889c23c)）提到几个案例：

案例一：**小爱翻车**

2018年 11 月，小米 AIoT（人工智能 + 物联网）开发者大会上，「雷布斯」骄傲地展示了新品智能音箱「小爱同学」。当场翻车：“你是光，你是电，你是唯一的神话。。。”

![](https://pic1.zhimg.com/v2-5cffb246b9ce90727faa9714178f787c_b.jpg)


案例二：**Sophia造假**

![](https://pic3.zhimg.com/v2-60c13b8c58a32fc1a1018228cac011de_b.gif)


2017年10月，一个Sophia的机器人四处圈粉，经常参加各种会、“发表演讲”、“接受采访”，比如去联合国对话，表现出来非常类似人类的言谈，还被沙特阿拉伯授予了正式的公民身份，比图灵测试还要牛。

![](https://pic1.zhimg.com/v2-896baeccc8f706ee53cdb53a087f3d20_b.jpg)

就在大家震惊之余，有思辨能力的人会质疑：“既然人工智能都要威胁人类了，为啥我的Siri还那么蠢？”

![](https://pic3.zhimg.com/v2-f2492a2356c10f4ac3c9c2fd8cb1ea9a_b.jpg)

果然，没几年就打脸了。

2019年1月，深度学习界“三巨头”之一的大牛Yann LeCun在推特公开指责：

索菲亚根本就是个骗局。LeCun直接指出，把索菲亚称作“远程操控AI”可能更合适一些。


![](https://pic2.zhimg.com/v2-c510cc71fc2a1b3f8fd55d914efd7a3d_b.jpg)

面对质疑，Sophia背后的汉森机器人技术公司在参加中国《对话》节目时回应：
-   目前所有能进行对话的人工智能都是人工编程的，索菲亚也不例外。
-   智能的头脑由人控制且内容往往都是人编好的。

问世近3年后终于承认，机器人的外壳只是一个“传声筒”。

![](https://pic4.zhimg.com/v2-104a38d921cad24fc0bf75ac1d7c83df_b.gif)

人们又一次感受到智商被侮辱。

等等，为什么是“又一次”？国内某些银行实体机器人对答如流、撒娇卖萌、还能自主走动干活儿。。。坚持说没有人工驱动…

![](https://pic1.zhimg.com/v2-d38b51ea2e3d7265674c3bc958458748_b.jpg)

国内受骗，国外也受骗。为什么总是我？

![](https://pic1.zhimg.com/v2-c8f6bc23f656dab28784392e5889d74c_b.jpg)

易骗体质的症状：
> 认知有限，先入为主，又过度自信排外，不愿深究，懒得思考，人云亦云的盲从，迷失自我，心血来潮的武断，观点和情绪盖过事实，于是掉入精心设计的陷阱…

除了外部因素，内在因素也天然具有欺骗性，人类大脑思考方式分快思考（system 1类似感应）和慢思考（system 2类似理性），感性思维在情绪作用机制下经常打败理性，如：
- ① 遇到不同观点时，本能的第一反应就是反驳，说服对方，而不是思考背后的事实…
- ② 遇到观点相同或是关系好的人发表的观点，本能反应：一身舒服，或跟随点赞，然后再考虑事实，即便有误，也会格外宽容。

这类偏见对应到心理学现象，有不下50个，elon musk曾在Twitter上转发过…
- ![](https://pic1.zhimg.com/v2-4cc4043c292d22642fa04ac841d2ad14_b.jpg)
- _完整版/英文版私信回复：认知偏差_

知名观点
-   傅盛：认知几乎是人与人之间的唯一差别，所谓成长就是认知升级
-   张一鸣：越来越觉得，对事情的认知是人最关键的竞争力

![](https://pic1.zhimg.com/v2-2f510021d82ad510c643bd65ced218b0_b.jpg)

![](https://pic3.zhimg.com/v2-6d67ff7575d3518f7ef33e6ca435713e_b.jpg)


扯远了，继续聊聊对话系统

案例三：**Google Duplex**

即便强如谷歌，也依旧束手无策。

2018年，发布Duplex Demo，让Google Assistant代替用户打电话订餐。全程语音交互，跟真人一样对话，还能停顿感，仿佛即将替代服务员。

![](https://pic1.zhimg.com/v2-f0c039af189eff87e8b15d463b05ba40_b.gif)


然而，到2019年，餐馆订餐还是糊里糊涂。
-   One year later, restaurants are still confused by Google Duplex，详见[地址](https://www.theverge.com/2019/5/9/18538194/google-duplex-ai-restaurants-experiences-review-robocalls)：

几年过去了，Duplex仍然是Demo状态，消失了。

对话类产品刚开始很新鲜，时间长了，发现又蠢又萌，语言理解能力堪忧，用户不得不跟人工智障battle，斗智斗勇，直到失去兴趣，沦为小孩子玩物，积上一身陈年老灰。

小爱同学智障案例
-   “小爱同学，播放loveshot” --> “好的，为你播放拉萨”
-   “小爱同学，播放七月的风” --> “对不起，只能查询未来十五天天气情况”

即使需求最“刚”的智能客服，如今的体验也是一言难尽，容易变身复读机，勉强借助相关问题推荐和人工客服解围。

![](https://pic3.zhimg.com/v2-6d2984b8260bc5764e7f85f07e28adee_b.jpg)

对于智能外呼机器人（接快递、银行语音机器人、营销机器人等），用户需要乖乖保持你一句我一句的标准节奏，不然变成“人工智障”：你说了两分钟，结果AI只回复第一句。

![](https://pic4.zhimg.com/v2-9bb24066db6983609e07321524d5f6a7_b.jpg)

更多智障案例私信“智障案例”

### **（1.3）潮水褪去**

理想很美好，现实很骨感。NLU的天花板（暂且不提难度更大的DM)一直悬在头顶，不管怎么跳，已有方法始终无法突破这层障碍。

人工智能变身人工智障后，潮水逐渐退出。

2020年后，各大厂商纷纷裁撤、缩招对话团队。

2021年，对话系统“凉透”了。实验室裁撤，团队缩编，音箱要么沦为小孩儿玩物，要么成为摆设，布满了灰尘。

> 对话系统“爱”、“恨”交织：  
> 爱：终极交互形态让人着迷，CUI，甚至更高级的多模态交互、脑机交互  
> 恨：技术现实与期望鸿沟太大，智障频频。  
> 鹤啸九天，公众号：鹤啸九天[ChatGPT：从入门到入行（放弃）](https://mp.weixin.qq.com/s?__biz=MjM5ODY2OTQyNg==&mid=2649768933&idx=1&sn=92345bd6e0a2fa16bb0674b7c889c23c)

### **（1.4）对话系统为什么难？**

> 当前的助手为什么智障？CUI为什么难？

2016年，Mingke的文章《为什么现在的人工智能助理都像人工智障》里详细解释了CUI的特点。

对话类产品69.7%集中在个人助理，具体是生活综合服务，出行、日程、购物、订餐，包含这类功能的产品是“天坑”

![](https://pic4.zhimg.com/v2-b30a196de41a305596945af77c9e7723_b.jpg)

比如简单的订餐场景，上一代人机交互形式GUI，产品交互方式相对确定，场景受限，用户需要乖乖按照预设功能逐步操作，附近/类型/排序，所见即所选，如果不知道自己要啥，就麻烦了，在信息的汪洋大海里随机游弋。

![](https://pic3.zhimg.com/v2-32d5b6ddefdfbc14f450d65bca9ace06_b.jpg)

从特定领域(specific domain)扩展到开放领域（open domain)的CUI，交互形式只剩下一个简简单单的对话页面，主动权返还给用户，而用户需求、对话顺序千差万别，长尾更加明显。这时的交互设计难以一招打遍天下

2016年底作者亲自测试，看看几个主流智能助理是否满足一个看似简单的需求：“推荐餐厅，不要日本菜”。结果各家的AI助理都会给出一堆餐厅推荐，全是日本菜。

![](https://pic3.zhimg.com/v2-2153068778ab93a3efa8f5e1826b5f12_b.jpg)

2019年，这个问题有进展么？依然没有，“不要”两个字被所有助理忽略（因为技术实现依然是搜索架构，NLU也理解不了这类逻辑语义，要解决就不停堆规则）

与GUI相比，CUI特点：高度个性化（LBS）、使用流程非线性、不宜信息过载（手机屏幕有限）、支持复合动作（一站直达）

怎么实现理想中的CUI呢？对话系统（AI的一个分支），一个合格的对话机器人（Agent）至少满足以下条件：
-   具备基于上下文的对话能力（contextual conversation）
-   具备理解口语逻辑（logic understanding）
-   所有能理解的需求，都要有能力履行（full-fulfillment）

不做过多解释，私信“人工智障”

2019年，Mingke文章《[人工智障 2 : 你看到的AI与智能无关](https://mp.weixin.qq.com/s?__biz=Mzg5NDIwODgzMA==&mid=2247484375&idx=1&sn=ef1c302d24f4b30651b5dfcaaf0390cc&scene=21#wechat_redirect)》进一步深入探讨了对话系统为什么这么难

mingke在深入剖析了其中原因。

人类对话的本质：思维. 人们用语言对话最终目的是为了让双方对当前`场景模型`（Situation model）保持**同步**。

![](https://pic3.zhimg.com/v2-e699e95d8b453c13b6fca677f66bb206_b.jpg)

影响人们对话的，仅信息（还不含推理）至少就有这三部分：`明文`（含上下文）+ `场景模型`（Context）+ `世界模型`。

这里的context远不止上下文这么简单，还包含了对话发生时人们所处的场景。这个场景模型涵盖了对话那一刻，除了明文以外的所有已被感知的信息。比如对话发生时的天气情况，只要被人感知到了，也会被放入Context中，并影响对话内容的发展。
-   `场景模型`是基于某一次对话的，对话不同，场景模型也不同；
-   而`世界模型`则是基于一个人的，相对而言长期不变。

无论精准/对错，每个人的`世界模型`都不完全一样，有可能是观察到的信息不同，也有可能是推理能力不一样。

世界模型影响的是人的**思维**本身，继而影响思维在低维的投影：对话。

普通人能毫不费力地完成这个工作。但是深度学习只能处理基于**明文**的信息。对于场景模型和世界模型的感知、生成、基于模型的推理，深度学习统统无能为力。

比如，以下场景，就连真人也无法仅凭“你好”两个字猜透对方的想法（世界模型），深度学习行么？

![](https://pic1.zhimg.com/v2-d459bbfda222d3642a4bcd7e5ba52d64_b.jpg)

阴影就像是两个 “你好”，字面上是一模一样，但是思想却完全不同。见面的那一瞬间，差异是非常大：

> 你在想（圆柱）：一年多不见了，她还好么？前女友在想（球）：这个人好眼熟，好像认识…

这就是为什么现在炙手可热的深度学习无法实现真正的智能（AGI）的本质原因：不能进行**因果推理**。（此处暂且不谈更麻烦的大脑工作机制、心理学偏见）

当然，也包括GPT模型。2023年3月24日，图领奖获得者 Yann Lecun直言不讳：
-   「Machine Learning sucks!」机器学习行不通
-   「Auto-Regressive Generative Models Suck!」，自回归语言模型GPT系列也行不通，包括ChatGPT、GPT-4，离真正的AGI还很远。
-   GPT-4并未达到人类智能，年轻人花20h练车就掌握了开车技能，即便有专业司机的海量训练数据、高级传感器的辅助，L5级别自动驾驶到现在还没实现

![](https://pic2.zhimg.com/v2-48984c2ebb0c05a8f38ebccab03b145d_b.jpg)

GPT这类自回归模型有天生缺陷，无法兼顾事实、不可控：
-   序列化生成过程将问题解空间一步步缩小，陷入局部深井，错误指数级别累积。

除了GPT，他还给机器学习几乎所有方向判了死刑。想用监督学习、强化学习和自监督学习实现AGI？不可能。

与人、动物相比，机器学习
-   （1）监督学习需要大量标注样本
-   （2）强化学习需要大量试错样本
-   （3）自监督学习需要大量非标注样本

而当前大部分基于机器学习的AI系统常常出现愚蠢错误，不会推理、规划

反观，动物或人：
-   （1）快速学习新任务
-   （2）理解环境运行逻辑
-   （3）推理、规划

人和动物具备常识，而机器表现得很肤浅

那么怎么办？他推荐世界模型，略，详见：[生成式人工智能(GAI)沉思录：浪潮之巅还是迷茫之谷？](https://mp.weixin.qq.com/s?__biz=MjM5ODY2OTQyNg==&mid=2649769135&idx=1&sn=2f42da2230375acbb8aeb5b487bd374f)

![](https://pic4.zhimg.com/v2-d6d2270f8b764399347cde12a2465b53_b.jpg)

【2023-10-18】
- MIT的Tegmark认为有世界模型
- 杨植麟：“Next token prediction（预测下一个字段）是唯一的问题。”“只要一条道走到黑，就能实现通用泛化的智能。”


总结：
-   人们对话的本质是**思维交换**，而远不只是**明文**上的**识别**和基于识别的**回复**
-   **对话是思想从高维向低维的投影，用低维方法解决高维问题本身就是极大的挑战**
-   **对话智能的核心价值在内容，而不是交互；**
-   **当前对话系统的价值在于代替用户重复思考**

## **（2）为何而惊：大模型重新燃气对话希望**

先回顾下对话系统分类，分成几个维度
-   适用范围：通用领域（open domain，难，停留在学术界）、特定领域（specific domain，可控，工业界现状）
-   任务类别：问答型（单轮为主）、任务型（执行任务）、闲聊型，以及推荐型
-   提问方：主动、被动以及混合型。

各种类型对比分析：

<table data-draft-node="block" data-draft-type="table" data-size="normal" data-row-style="normal"><tbody><tr><td>维度</td><td>闲聊Chit-chat</td><td>知识问答knowledge</td><td>任务执行Task</td><td>推荐Recommendation</td></tr><tr><td>目的</td><td>闲聊</td><td>知识获取</td><td>完成任务/动作</td><td>信息推荐</td></tr><tr><td>领域</td><td>开放域</td><td>开放域</td><td>特定域（垂类）</td><td>特定域</td></tr><tr><td>会话轮数评价</td><td>越多越好</td><td>越少越好</td><td>越少越好</td><td>越少越好</td></tr><tr><td>应用</td><td>娱乐/情感陪护/营销沟通</td><td>客服/教育</td><td>虚拟个人助理</td><td>个性化推荐</td></tr><tr><td>典型系统</td><td>小冰</td><td>Watson/Wolfram alpha</td><td>Siri/cortana/allo/度秘/灵犀</td><td>Quartz/今日头条</td></tr></tbody></table>

源自：2020年11月，哈工大张伟男《人机对话关键技术及挑战》

太多了，眼花，简化为两种常见类型：闲聊型（Chit-Chat） 和 任务型（Task-Oriented）

![](https://pic3.zhimg.com/v2-4e562cc27aea24e88d619a3a24f7c716_b.jpg)


源自：2020年，台湾大学陈蕴侬的《Towards Conversational AI》，ppt私聊

对话系统架构
-   ① pipeline（流水线）结构：堆积木，稳定、可控，工业界落地多。如下图所示
-   ② end2end（端到端）架构：试图一个模型解决所有，难度大，一直存在于实验室

![](https://pic3.zhimg.com/v2-90598bf8ecc57d253beea6f217b7daa2_b.jpg)


微软小冰具备**通用闲聊**（检索+排序）和**任务执行**能力，其系统架构是混合型：检索+排序、pipeline（Frame Based）

![](https://pic4.zhimg.com/v2-433deb64d123491daf77a0589d2a8c03_b.jpg)


![](https://pic2.zhimg.com/v2-ab8619008ca7210157324ba65cff166d_b.jpg)

为什么没用端到端？没办法，难啊，公认的业界难题。

工业界任务型对话中，pipeline占据主流位置。

![](https://pic4.zhimg.com/v2-2c8d041f837da348f5615252cf97446b_b.jpg)


其中，几个核心组件：NLU、DM和NLG，各个组件实现的功能对比：

<table data-draft-node="block" data-draft-type="table" data-size="normal" data-row-style="normal"><tbody><tr><td>类型</td><td>NLU</td><td>DM</td><td>NLG</td></tr><tr><td>聊天</td><td>情感及意图识别</td><td>上下文序列建模及候选回复评分</td><td>开放域聊天回复</td></tr><tr><td>问答</td><td>问句分析/分类</td><td>文本检索/知识库匹配</td><td>文本片段/知识库实体</td></tr><tr><td>任务</td><td>意图分类/语义槽填充</td><td>对话状态跟踪/策略学习</td><td>确认/澄清/完成等</td></tr><tr><td>推荐</td><td>主题/兴趣识别</td><td>用户兴趣匹配/推荐内容排序</td><td>推荐内容</td></tr></tbody></table>

大模型海啸的袭击下，传统对话系统已经支离破碎

## **（3）对话系统之变：大模型时代对话系统**

ChatGPT是通用领域聊天机器人。

[往期文章【拾象投研】大模型（LLM）最新趋势总结](https://mp.weixin.qq.com/s?__biz=MjM5ODY2OTQyNg==&mid=2649769341&idx=1&sn=ff456c6c38de6451603595d8d50c1edb) 里提到了大模型对各行各业的改变
-   LLM基础模型拿走价值链的大头（60%），其次是AI Infra基础架构、Killer Apps，各占20%。
-   人机交互方式开始迈入新时代（CUI对话交互）
-   目前的大模型空有大脑，身体和感官还在逐步成长。
-   LLM之上的应用会是什么样？全方位的重构：交互、数据信息、服务以及反馈机制，一个可行的路子是AI Native软件开发——把已有应用按照LLM的能力图谱重新设计一遍，对话式交互（CUI）走到前台。

### **（3.1）大模型对对话系统冲击有多大？**

架构图

![](https://pic1.zhimg.com/v2-57d0717c7dd32d27aa1a6ec2986d6104_b.jpg)

大模型在传统对话系统中的“战绩”
-   NLU：已沦陷，Prompt中限定业务场景，意图识别、槽位抽取、指代消解等已满足，但速度是大问题，需要进一步微调
-   DM：部分沦陷，浅多轮通过prompt和上下文变成单轮，简单多轮场景function call可解决，但复杂场景不行，尤其速度、可控性、黑盒
-   KB/KG：通用知识大模型直接可用，领域知识需要单独预训练、微调，植入大模型，但存在幻觉问题
-   外部APIs：使用Plugins和Function Call连接外部系统，隐私安全需要格外注意
-   NLG：已沦陷，大模型角色模拟尤其出色
-   ASR和TTS：语音功能相对独立，接上api即可使用，多模态大模型也在尝试融合中。
-   语料+知识库：数据标注、语料清洗工作被大模型占领，知识库构建需要业务人员部分参与

可以看到，大模型已经占领了对话系统的大部分江山，高达80-90%。

对话系统从业者积累的大部分经验都废了，时代抛弃你时，连再见都不会说，一个悲伤的故事。

![](https://pic4.zhimg.com/v2-03879bb14b8584ab7a880a3a7cf2e5f7_b.jpg)


### **（3.2）大模型入局对话系统**

案例一：ChatGPT首次进入车载交互领域

2023年6月15日，奔驰和微软宣布扩大AI应用合作，比如将 ChatGPT继承到车载语音控制系统中。

6月16日开始，美国90万设备配备MBUX信息娱乐系统，车主可以登录应用“Mercedes Me”，通过微软Azure OpenAI服务体验ChatGPT版的车载语音助手。

![](https://pic4.zhimg.com/v2-9f2d3412dcf5ba43734e8a457ba9724b_b.jpg)


与上一代车载交互相比，交互更加智能，多轮会话体验更好。主题覆盖：地点信息、菜谱甚至更复杂的问题，比如：预定餐厅、电影票。

体验视频：(见公众号)
-   问题1：推荐几个好玩儿的海滩
-   问题2：海边适合哪些活动
-   问题3：这个海滩有鲨鱼吗
-   问题4：讲个鲨鱼的笑话

车载场景下，交互流畅，对话自然。

案例二：SmartSiri

ChatGPT作为首个通用领域端到端对话架构的成功范例, 让人重新燃起了对话交互（CUI）的希望。

除了车载助手，有人讲ChatGPT应用到Siri上，让个人助理焕然一新。

  
2023年6月13日，有个开发者发布“Smart Siri”，将刚升级的ChatGPT APP与Siri APP绑定，实现了个人助理质的飞跃。

当前智能助理的槽点：
-   “Siri 是人工智障”

由于 Siri 更强调在用户设备端计算，需要保护个人隐私，只能做些特定任务，比如：查天气、定闹钟；

官方的ChatGPT APP升级后，支持与Siri、快捷指令联动。

Siri 接入 ChatGPT 后，执行任务的角色就被后者接替了，想象空间变得更大。

那么，怎么接入？
-   方法一: 快捷指令基于 ChatGPT API 接口进行 JSON 格式的发送获取，但发送和解析过程都会消耗很长时间，占用 ChatGPT key 余额。
-   方法二: 官方 app 接口省去用户打包数据提取数据的过程，直接向 app 发送请求并获取有效信息。中间不用受网络波动、ChatGPT 用户过多、key 余额不足等因素的影响
-   不用懂JSON 语言，不用写代码，把用户发问需求细化成小步骤，找到能实现对应任务的 app，像乐高积木一样拼起来就行了。

“Smart Siri”可直接用语音发问，对于明确的、具体的发问，提炼得更好。

-   直接喊“Hey Siri + Smart Siri”，等待，看到“Yes”后，就能开始问问题

案例分析
-   Siri 的表现相对刻板，它仅能提供网址以及内容概括，有时会直接告知未找到相关信息，仿佛是被束缚的人工智能
-   Smart Siri 则能立即提供不错的回答，简洁明了，看起来的确挺聪明的。

除了手机助理，还有别的应用，比如
-   把 iPhone 内睡眠数据（步数等健康数据）打包，让 ChatGPT 接入分析，最后生成一个“每日健康分析报告”——这个过程完全自动化。
-   智能家居:
-   授权chatgpt app读取家庭数据,对智能家居进行开关、自动化及预处理，对气温、温度提出有效建议
-   跨境电商分析场景：
-   解析电商规则，SEO优化、选品、广告优化、商品详情页优化、关键词优化、客服与售后自动化
-   不用打开其他app，直接用Siri体温，获取答案，优化

Smart Siri 依然有不足：
-   ChatGPT 还无法实现连续对话，不过可以把之前的聊天记录粘贴进当前要问的问题里，也能间接连续问答的效果。（毕竟受数据隐私限制）

苹果在WWDC（年度开发者大会）上并未推出LLM相关应用，估计还在低调研究中，官方升级Siri后，这类问题应该会解决。

案例三：**华为小艺+小米小爱**

近期，华为、小米纷纷发布自己的大模型，升级自家的个人助理产品

2023年7月, 华为开发者大会上发布了面向行业的盘古大模型3.0，最高版本高达1000亿参数，同时也将盘古大模型应用到手机终端，将智能助手小艺接入了盘古大模型能力，在智慧交互、高效生产力和个性化服务上做了升级。

![](https://pic2.zhimg.com/v2-3bfa40ca127e3af7ba5dcba463168e3d_b.jpg)


2023年8月14日，小米新品发布会上，雷军正式宣布小米13亿参数大模型已经成功在手机本地跑通，部分场景可以媲美60亿参数模型在云端运行结果。小爱同学升级AI大模型能力，并开启内测，未来小米大模型技术方向是轻量化、本地部署。

![](https://pic1.zhimg.com/v2-f8d5ab070d95723937b79d4388b80f20_b.jpg)

这两家针对自己的传统个人助理具体做了什么操作？推倒重来还是布局改进？不清楚。

后者可能性更大，已有系统绑定的业务较多，不太可能直接交给大模型完成。

## **（4）LLM时代的对话系统何去何从？**

技术升级浪潮下，还顾影自怜，怨天怨地，毫无用处，拥抱新技术才是出路。

大浪袭来，除了疲于奔命，淋成落汤鸡，不妨深思熟虑，提前准备好帆板，借势起飞。

![](https://pic4.zhimg.com/v2-7bc35371861868c2410abd30d95bc5e3_b.jpg)


LLM时代的对话系统该怎么做？没有固定答案，大家还在不断摸索中。

  

### （4.0）LLM时代开发模式

  
大模型的开发模式

![](https://pic3.zhimg.com/v2-c5748909f4dcbced967e8333f61345ce_b.jpg)

-   （1）`pre-training`(`预训练`)： **通识教育**，教小孩认字、学算数、做推理，这个步骤产出基础大模型。
-   （2）`fine-tune`(`微调`)：**专业课**，比如学法律的会接触一些法律的条款、法律名词；学计算机的会知道什么叫计算机语言。
-   （3）`prompt engineering`(`提示工程`)：**职业训练**，AI应用的准确率要达到商用级别（超过人的准确率），就需要 prompt engineer，PE 重要性

其中，有些场景中（2）可以省略。  
  
LLM时代Prompt Engineer开发范式
-   第一层：**简单Prompt**: 即编写一个提示词（Prompt）去调用大模型，最简单的形式。
-   第二层：**Plugin插件**: 用大模型插件（Plugin）去调各种API，以及Function Call。
-   第三层：**Prompt Engineering** **Workflow + OpenAI** **API**
  -   基于提示词工程的`工作流`（workflow）编排。AI应用就是基于工作流实现。
-   第四层：向量数据库**集成**
  -   向量数据库包含数据特征值，现在最好的AI应用落地方案就是VectorDB，包括做知识库、做客服机器人。
- 第五层：**AI Agents**, 这个概念特别火，最重要的逻辑就是让大模型自己做递归。
  -   Agent的原理: AI自己对任务进行拆解，再进一步递归、继续拆解，直到有一步，AI可以将这个任务执行，最后再将任务合并起来，往前递归回来，合并为一个工程。
-   第六层：**领域模型 Domain Model**
  -   专业模型为什么重要？大参数**基础模型**的训练和推理成本非常高，而**专业模型**速度快、成本低、准确率高，因为有行业的高质量数据，所以准确率高；进而可以形成数据飞轮，形成自己的竞争优势。
  
人机协同三种模式
-   `AI Embedded` **嵌入**：某个环节里去调用大模型
  - 使用提示词来设定目标，与AI进行语言交流，然后AI协助完成目标
-   `AI Copilot` **辅助**：每个环节都可以跟大模型进行交互
  - 人类和AI各自发挥作用，AI介入到工作流程中，从提供建议到协助完成流程的各个阶段。
-   `AI Agent` **代理**：任务交给大模型，大模型即可自行计划、分解和自动执行
  - 人类设定目标并提供资源（计算能力），然后监督结果。
  - Agent承担了大部分工作。
  - AutoGPT代表了一种完全自动化的实现方式，试图抵达AGI的理想状态，即提出需求后机器人能够自动完成任务
  - AI技术的自动化范式 —— AutoGPT
  - 基于Agents的自动化团队——GPTeam，许多流程都可以被自动化执行。市场调研、问卷调查、品牌计划等等，都可以由AI来完成。
  - 自动化品牌营销公司——AutoCorp
- ![](https://pic1.zhimg.com/v2-0999ee748a33bc812f5f9ca73af4a41c_b.jpg)
- ![](https://pic2.zhimg.com/80/v2-768dd5453f9ebe858d60b90bd1b3143d_1440w.webp)

第三种模式将成为未来人机交互的主要模式。

**（4.1）方案一：AI Copilot 辅助**  
  
以LLM为核心，end2end架构实现新版对话系统，用prompt engineering复现原有主要模块

既然大模型（尤其是GPT系列）这么厉害，下游任务只需调prompt，那就用prompt去完成对话功能，替换原有功能模块就好了。
-   角色模拟：system prompt中设置即可，大模型的强项
-   闲聊任务：满足，一次调用即可
-   简易问答：如果是通用领域知识，一次调用即可，如果是垂直领域，需要额外融入知识（prompt中植入/微调），如果涉及实时查询、工具，还需要结合Plugin、Function Call，一般1-3次调用
-   多轮任务：prompt中设置对话逻辑（类似上一代有限状态机FSM），简单任务满足，功能接口借助Plugin、Function Call实现，同时增加记忆单元（如借助LangChain），但复杂任务不好办，如：任务状态处理逻辑复杂、场景嵌套、API较多等。即便是FSM场景也受限（如图），而订餐这类场景只是多轮对话中的一种简单形式，至于更复杂的循环、中断、嵌套、多阶就不用提了，如信用卡业务场景下，各种流程跳转，简易对话无能为力，只好用比FSM（图）更高级的方法，Frame（槽填充+树）、Goal（树+栈+字典），大模型用data-driven结合强化学习更合适。

![](https://pic2.zhimg.com/v2-f5dd6cfaabce299a8341b9e584a99311_b.jpg)

-   推荐型：边聊边推，设计推荐的prompt，一次调用，但依赖具体形态，聊天场景推荐对时延要求低，启用流式输出可以缓冲，而输入是输入提示这类场景，大模型的速度就堪忧了。

全部采用大模型后，以常规的对话系统为例，一次对话过程可能涉及1~10次大模型调用，这用户体验可想而知。

这种思路是把原来对话系统所有的功能都用生成式方法（自回归语言模型，GPT为代表）解决，实际上，生成式只是小部分，大部分任务是理解式任务（掩码语言模型，BERT为代表），如意图识别、槽位抽取、状态跟踪等输出空间有限，这时用生成式方法，天然就慢半拍。

实际落地时，新的问题出来了：
-   极度依赖prompt：提示语稍微变更下，加个空格，结果可能就相差十万八千里，每个场景都需要仔细调试prompt，换个模型又要重新开始。
-   速度慢：实在是慢，正常情况1-3s回复，如果句子长，要持续等待，直至流式输出结束。这对高并发、低时延要求的对话产品简直是“噩耗”。
-   不可控：即便在prompt里明确要求不要超过30字，结果LLM当成耳边风，还是会超出字数。任务型对话里的业务处理逻辑往往要求准确无误了。
-   幻觉：一本正经的胡说八道
-   黑盒：大模型到底是怎么执行对话策略的？不知道，充满了玄学意味，涌现到底是个啥？这对高度可控的场景十分致命。

对于速度问题，短期内只能依靠别的方法提速了，如：
-   各种模型加速推理技术
-   部分功能回退：如不适合生成式方法的NLU/DM
-   推进end2end方法：将多轮会话训入大模型，延续之前的end2end思路

### **（4.2）方案二：AI Embedded 嵌入**

在LLM基础上，加领域语料，增量预训练、微调，融入领域知识，根据业务场景，增加特殊逻辑

这部分涉及两部分工作
-   基座大模型训练：各行各业都在训自己的大模型，金融、医疗、教育、数字人，甚至宗教
-   业务场景落地：适配业务场景，升级或重构现有对话产品的局部

各行各业都在训自己的大模型，金融、医疗、教育、数字人，甚至宗教

人物个性模拟上
-   国外有 Character.ai，用户根据个人偏好定制 AI 角色并和它聊天；
-   国内有阿里的脱口秀版GPT——鸟鸟分鸟，并且已经在天猫精灵上为个人终端行业的客户做了演示

![](https://pic3.zhimg.com/v2-0b37c3a5fe96467fc16fc6cbf3c671aa_b.jpg)

应用场景很多，略

**（4.3）方案三：AI Agent 代理**

抛弃过往模块化思路，站在任务角度，通过Agent去执行对话任务，如：

最近不少人不再卷大模型了，开始卷 AI Agents
-   LLM诞生之初，大家对于其能力的边界还没有清晰的认知，以为有了LLM就可以直通AGI了，路线: LLM -> AGI
-   过了段时间，发现LLM的既有问题（幻觉问题、容量限制…），并不能直接到达AGI，于是路线变成了: LLM -> Agent -> AGI
-   借助一个/多个Agent，构建一个新形态，继续实现通往AGI的道路。但这条路是否能走通，以及还面临着哪些问题，有待进一步验证。

由于大模型的出现，AI Agents 衍生出了一种新的架构形式: 《LLM Powered Autonomous Agents》
-   将最重要的「任务规划」部分或完全交由LLM，而做出这一设计的依据在于默认：LLM具有任务分解和反思的能力。

最直观的公式

> `Agent` = `LLM` + Planning + Feedback + Tool use

![](https://pic3.zhimg.com/v2-ad871f9f1bc3fcd67eebe51cb1bd1d56_b.jpg)

这种思路更加灵活，贴近AGI，想象空间巨大，成为继模型训练后又一个角斗场。

详见往期文章：[大模型智能体](https://mp.weixin.qq.com/s%3F__biz%3DMjM5ODY2OTQyNg%3D%3D%26mid%3D2649769408%26idx%3D1%26sn%3D9639a1efaca760b539d39af9d95192cc%26chksm%3Dbec3d8dd89b451cb1b10c39bc879bd6c3fbf7aff2ea711bbcb09961c2722dda8e81f31f8d3c0%26token%3D858594018%26lang%3Dzh_CN%23rd)

  

### **（4.4）学术界做法**

以上是工业界做法，追求短平快，快速迭代，专注短期价值，而学术界没有营收变现压力，往往更加前沿，目光长远。

那么，不妨调研下学术界都有哪些高瞻远瞩。

ArXiv上搜了下对话系统和大模型两个关键词，相关文章有62篇

![](https://pic2.zhimg.com/v2-a9c4fd00b65ed9126b28b4a0db83f7c9_b.jpg)
  

[ArXiv](https://arxiv.org/search/%3Fquery%3Ddialogue%2Bsystem%2Bllm%26searchtype%3Dall%26abstracts%3Dshow%26order%3D-announced_date_first%26size%3D50%26start%3D50)上搜了下对话系统和大模型两个关键词，相关文章有62篇，其中跟新时代的对话系统设计有关的有约10篇

-   增强NLU
  -   【2023-9-22】[Self-Explanation Prompting Improves Dialogue Understanding in Large Language Models](https://arxiv.org/pdf/2309.12940)，中科大、阿里，用 Self-Explanation 自解释的prompt策略增强多轮对话中LLM的理解能力，效果超过 zero-shot prompt，达到或超过few-shot prompt； 为每句话提供解释，然后根据这些解释作出回应 Provide explanations for each utterance and then respond based on these explanations
-   利用LLM增强DM
  -   【2023-9-16】[Enhancing Large Language Model Induced Task-Oriented Dialogue Systems Through Look-Forward Motivated Goals](https://arxiv.org/pdf/2309.08949.pdf) 新加坡国立+伦敦大学，现有的LLM驱动的任务型对话（ToD）缺乏目标（结果和效率）导向的奖励，提出 [ProToD](https://github.com/zhiyuanhubj/ProToD) (Proactively Goal-Driven LLM-Induced ToD)，预测未来动作，给于目标导向的奖励信号，并提出目标导向的评估方法，在 MultiWoZ 2.1 数据集上，只用10%的数据超过端到端全监督模型
  -   【2023-8-15】[DiagGPT: An LLM-based Chatbot with Automatic Topic Management for Task-Oriented Dialogue](https://arxiv.org/abs/2308.08043)，伊利亚洛-香槟大学，任务型对话里的主题管理自动化. ChatGPT 自带的问答能力难以胜任复杂诊断场景（complex diagnostic scenarios），如 法律、医疗咨询领域。这个TOD场景，需要主动发问，引导用户到具体任务上，提出 DiagGPT (Dialogue in Diagnosis GPT) 将 LLM 扩展到 TOD场景
  -   【2023-7-29】[Roll Up Your Sleeves: Working with a Collaborative and Engaging Task-Oriented Dialogue System](https://arxiv.org/pdf/2307.16081.pdf)，俄亥俄州立大学，以用户为中心的数字助手 [TACOBOT](https://github.com/OSU-NLP-Group/TacoBot)， 在 Alexa Prize TaskBot Challenge 比赛中获得第三名
-   NLG升级
  -   【2023-9-15】[Unleashing Potential of Evidence in Knowledge-Intensive Dialogue Generation](https://arxiv.org/pdf/2309.08380), To fully Unleash the potential of evidence, we propose a framework to effectively incorporate Evidence in knowledge-Intensive Dialogue Generation (u-EIDG). Specifically, we introduce an automatic evidence generation framework that harnesses the power of Large Language Models (LLMs) to mine reliable evidence veracity labels from unlabeled data
-   对话与推荐融合
  -   【2023-8-11】[A Large Language Model Enhanced Conversational Recommender System](https://arxiv.org/abs/2308.06212) 伦敦大学和快手，新加坡南洋理工，对话式推荐系统（CRSs）涉及多个子任务：用户偏好诱导、推荐、解释和物品信息搜索，user preference elicitation, recommendation, explanation, and item information search，LLM-based CRS 可以解决现有问题
-   用户模拟器
  -   【2023-9-22】[User Simulation with Large Language Models for Evaluating Task-Oriented Dialogue](https://arxiv.org/pdf/2309.13233)，加利福尼亚大学+AWS AI Lab，利用LLM当做模拟器，用来评估任务型（TOD）多轮会话

-   **特定领域**（specific domain） → **开放域**（open domain）
  -   【2023-9-15】DST升级，从单个场景拓展到所有场景，提出 结构化prompt提示技术 S3-DST，[S3-DST: Structured Open-Domain Dialogue Segmentation and State Tracking in the Era of LLMs](https://arxiv.org/pdf/2309.08827)，Assuming a zero-shot setting appropriate to a true open-domain dialogue system, we propose S3-DST, a structured prompting technique that harnesses Pre-Analytical Recollection, a novel grounding mechanism we designed for improving long context tracking.
-   任务型对话扩展到**多模态**领域
  -   【2023-9-19】语言、语音融合，一步到位，NLG+TTS [Towards Joint Modeling of Dialogue Response and Speech Synthesis based on Large Language Model](https://arxiv.org/pdf/2309.11000)
  -   【2023-10-1】[Application of frozen large-scale models to multimodal task-oriented](https://arxiv.org/abs/2310.00845) 提出LENS框架，解决多模态对话问题，使用数据集 MMD

学术界在不断探索大模型在对话系统各个模块上的迭代升级，增强NLU/DM/NLG，模拟器，并向开放域对话、多模态对话、对话与推荐融合方向推动。

## **（5）尾声**

对话系统博大精深，这篇文章是结合过往多年对话系统经验，短期内东拼西凑而来，质量没保障，如果错误、疑问，欢迎私聊，讨论。

附录：很多，不一一罗列了，反正你们也不会看

-   公众号内私信回复关键词获取感兴趣的资料
-   认知偏差→50个认知偏差
-   心理学效应→心理学效应相关信息
-   对话系统→对话系统笔记
-   对话管理→对话管理（DM）专题
-   台大对话→台大陈蕴侬对话系统的ppt
-   哈工大张伟男→哈工大张伟男对话系统专题
-   对话系统升级→大模型时代，对话系统如何升级、
-   智障案例→了解更多人工智障示例
-   人工智障→Mingke对智障系列的详尽分析
-   拾象报告→拾象投研对大模型的两次分析报告
-   大模型应用→大模型在各行各业的应用案例


# 结束