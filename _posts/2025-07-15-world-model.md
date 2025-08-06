---
layout: post
title:  世界模型 World Model
date:   2025-07-15 12:00:00
categories: 大模型
tags: LLM AGI 世界模型 系统 快思考 慢思考 因果 模拟器
excerpt: 世界模型专题笔记
mathjax: true
permalink: /world_model
---

* content
{:toc}


# 世界模型


通用智能目前存在两个流派
- Transformer学派（如GPT系列）侧重于大数据驱动的自回归学习，最近发布的Sora体现的涌现能力初步隐含着通用人工智能的韵味。
- 杨立昆（Yann LeCun）为代表的世界模型学派。世界模型学派则认为需要通过构建对世界的内在理解，强调常识性知识和环境交互

「世界模型」被业界看作是通往AGI道路上的关键基石，让AI智能体在无限丰富的模拟环境中接受训练。

## 因果推理

理想中的 World Model 是**事实**及其**支撑逻辑**的合集。但现实中，World Model 往往为隐性，并呈碎片化 - 事实散布于各类数据、分析和专家的脑袋中

基于因果分析构建 World Model 工具链

例如，对于利润率问题，人类专家可以基于先验知识、私有数据、Causal-learn和DoWhy等工具构建一个具有统计学意义的“利润率World Model”

Causal AI 长时间在商业领域裹足不前的主因: Causal Modeling 过程**非常依赖于人类专家**的知识和干预，难以完全自动化。

但利用大模型替代或辅助人类专家进行 Causal Modeling 研究有了不错的进展。
详见站内专题：[因果推理](casual)



## 双系统：快思考 & 慢思考

人脑思维双系统模型理论（Dual Process Theory）

认知心理学名著《**思考，快与慢**》（Thinking, Fast and Slow）中介绍 `双过程理论`（dual propcess theory）。人类认知过程需要两个密不可分的系统，其中
- `System 1` 负责**快速直觉式**思考 -- `感性`
- `System 2` 负责**慢速分析式**思考 -- `理性`

详见站内专题: [大脑工作原理](brain)

【2023-9-11】[大模型为啥这么慢，原来是想多了：新方向是和人一样的思维算法](https://www.toutiao.com/article/7277447969819918906)

弗吉尼亚理工大学和微软的一个研究团队在近日的一篇论文中提出了**思维算法**（AoT），其组合了直觉能力与算法方法的条理性，从而能在保证 LLM 性能的同时极大节省成本。
- 当前研究则转向了**线性推理**路径，将问题分解成**子任务**来发现解决方案，或通过修改上下文来利用外部机制来改变 token 的生成。
- 早期的 LLM 策略模仿即时的 `System 1`（**快速**反应），特征是通过**脉冲决策**实现。
- 相较之下，`思维链`（CoT）和 `least-to-most prompting`（L2M）等更新的一些方法则反映了 `System 2`（**慢速**思考）的内省式本质。通过整合中间推理步骤，可让 LLM 的算术推理能力获得提升。
- ![img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/3287271b37be485b93eefcc51099d8fc~tplv-tt-origin-asy2:5aS05p2hQOacuuWZqOS5i-W_g1Bybw==.image?_iz=58558&from=article.pc_detail&x-expires=1695195866&x-signature=L%2FFFB5bS78GEXXKy74Hha64o3CM%3D)


## 什么是世界模型

【2024-2-22】[什么是world models/世界模型](https://zhuanlan.zhihu.com/p/661768957)
- OpenAI 介绍材料中称 Sora 是 “world simulator”

AI领域提到 **世界**/world、**环境**/environment 这个词时，通常是为了与 **智能体**/agent 加以区分。

研究智能体最多领域，一个是`强化学习`，一个是`机器人`领域。
- 因此，world models、world modeling 最早常出现在**机器人**领域的论文中。

而 world models 这个词影响最大的可能是 Jurgen 2018 年放到arxiv的论文, 以“world models”命名，该文章最终以 “Recurrent World Models Facilitate Policy Evolution”的title发表在NeurIPS‘18。
- 论文没有定义什么是World models，而是类比了认知科学中人脑的mental model，引用了1971年的文献
- Wikipedia中介绍mental model是很明确的指出其可能参与认知、推理、决策过程。
  - mental model 主要包含 mental representations 和 mental simulation 两部分。

论文截图
- ![](https://pic1.zhimg.com/80/v2-c842083297df6e7c578ecc3c45680d84_1440w.webp)
- 纵向 V->z: 观测的低维表征，用VAE实现
- 水平的M->h->M->h: 序列预测下一个时刻的表征，用RNN实现
- 这两部分加起来就是World Model。



World model 主要包含**状态表征**和**转移模型**，正好对应mental representations 和 mental simulation。

这不是所有的序列预测都是world model了？
- 熟悉强化学习的同学能一眼看出来，这张图的结构是错误（不完整）的，而真正的结构是下面这张图
- RNN的输入不仅是z，还有动作action，这就不是通常的序列预测了
- ![](https://pic1.zhimg.com/80/v2-76e9b6a8f3aa22b737b293c3b22c6a18_1440w.webp)
- 强化学习里有很多model-based RL，其中的model跟world model一回事儿

model-based RL这个方向长久以来的无奈：
- model不够准确，完全在model里训练的RL效果很差。

这个问题直到近几年才得到解决。
- Sutton 很久以前就意识到model不够准确。
- 在1990年提出`Dyna`框架论文Integrated Architectures for Learning, Planning and Reacting based on Dynamic Programming（发表在第一次从workshop变成conference的ICML上），管这个model叫action model，强调预测action执行的结果。RL一边从真实数据中学习（第3行），一边从model中学习（第5行），以防model不准确造成策略学不好。

world model 对决策十分重要。
- 如果能获得准确的world model，那就可以通过在world model中就反复试错，找到现实最优决策。

world model 核心作用：反事实推理/Counterfactual reasoning
- 即便对于数据中没有见过的决策，在world model中都能推理出决策的结果。

图灵奖得主`Judea Pearl`的科普读物**The book of why**中绘制了一副因果阶梯
- 最下层是“关联”，也就是今天大部分预测模型主要在做的事；
- 中间层是“干预”，强化学习中的探索就是典型的干预；
- 最上层是反事实，通过想象回答 what if 问题。

Judea为反事实推理绘制的示意图，是科学家在大脑中想象，这与Jurgen在论文中用的示意图异曲同工。
- ![](https://pic2.zhimg.com/80/v2-62830c83e6df7db10a4053339e908df9_1440w.webp)

AI研究人员对world model的追求，是试图超越数据，进行反事实推理，回答what if问题能力的追求。这是一种人类天然具备，而当前的AI还做得很差的能力。一旦产生突破，AI决策能力会大幅提升，实现全自动驾驶等场景应用。


A Cognitive Architecture capable of reasoning & planning

LeCun 提出了构建「世界模型」想法，并在一篇题为《A path towards autonomous machine intelligence》论文中进行了详细阐述
- [原视频链接](https://www.youtube.com/watch?v=DokLw1tILlw)
- [PPT 链接](https://drive.google.com/file/d/1Txb9ykr03Lda-oTLXbnlQsEe46V8mGzi/view)

构建一个能够进行推理和规划的认知架构。这个架构由 6 个独立的模块组成：
- 配置器（Configurator）模块；
- 感知模块（Perception module）；
- 世界模型（World model）；
- 成本模块（Cost module）；
- actor 模块；
- 短期记忆模块（Short-term memory module）。

这些模块的具体信息参考：[图灵奖获得者 Yann LeCun：未来几十年 AI 研究的最大挑战是「预测世界模型」](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650839081&idx=1&sn=f014b639541de68d7a115aa1ad96b33f&chksm=84e55c57b392d54104e20026682164235cc95892c7313c12bc7219ca0010982de9d3afb6a9db&scene=21#wechat_redirect), 文章中包含视频讲解


### 世界模型 vs 模拟器

【2025-7-28】 [从视频生成到世界模型](https://www.xiaohongshu.com/explore/6887136d000000000b02dc15)
- 刘威 前腾讯杰出科学家、混元大模型技术负责人：现在为Video Rebirth首席执行官

`世界模型` = `世界模拟器` + `世界预测器`

模拟器主题见站内专题：[用户模拟器](user_simulator)

世界模型需要解决的关键问题
- 因果推理: 生成遵循时间单向性，过去状态决定未来演化，不违反因果关系
- 物理准确: 生成内容符合真实物理规律和常识逻辑
- 持续一致: 连续生成长时段视频内容，整个序列中保持人物、物体、背景的前后一致性
- 实时交互: 实时响应用户lAgent输入，低延迟地动态生成



## 如何构建世界模型

如何构建、训练世界模型？
- 未来几十年阻碍人工智能发展的真正障碍是为**世界模型**设计架构以及训练范式。
- 训练世界模型是自监督学习（SSL）中的一个典型例子，其基本思想是**模式补全**。对未来输入（或暂时未观察到的输入）的预测是模式补全的一个特例。

世界只能部分地预测。首先，如何表征预测中的不确定性。一个预测模型如何能代表多种预测？

**概率模型**在连续域中是难以实现的，而**生成式模型**必须预测世界的每一个细节。

基于此，LeCun 给出了一种解决方案：`联合嵌入预测架构`（Joint-Embedding Predictive Architecture，JEPA）。
- JEPA 不是生成式的，因为不能轻易地用于从 x 预测 y, 仅捕获 x 和 y 之间的依赖关系，而不显式生成 y 的预测。

生成式架构会预测 y 的所有的细节，包括不相关的；而 JEPA 会预测 y 的抽象表征。

有五种思路是需要「彻底抛弃」的：
- 放弃生成式模型，支持联合嵌入架构；
- 放弃自回归式生成；
- 放弃概率模型，支持能量模型；
- 放弃对比式方法，支持正则化方法；
- 放弃强化学习，支持模型预测控制。

他的建议是，只有在计划不能产生预测结果时才使用 RL，以调整世界模型或 critic。

与能量模型一样，可以使用对比方法训练 JEPA。但是，对比方法在高维空间中效率很低，所以更适合用非对比方法来训练它们。在 JEPA 的情况下，可以通过四个标准来完成，如下图所示：
1. 最大化 $s_x$ 关于 x 的信息量；
2. 最大化 $s_y$ 关于 y 的信息量；
3. 使 $s_y$ 容易从 $s_x$ 中预测；
4. 最小化用于预测潜在变量 z 的信息含量。

迈向自主式 AI 系统的步骤都有哪些？LeCun 也给出了自己的想法：
- 1、自监督学习
  - 学习世界的表征
  - 学习世界的预测模型
- 2、处理预测中的不确定性
  - 联合嵌入的预测架构
  - 能量模型框架
- 3、从观察中学习世界模型
  - 像动物和人类婴儿一样？
- 4、推理和规划
  - 与基于梯度的学习兼容
  - 没有符号，没有逻辑→向量和连续函数

其他的一些猜想包括：
- 预测是智能的本质：学习世界的预测模型是常识的基础
- 几乎所有的东西都是通过自监督学习得来的：低层次的特征、空间、物体、物理学、抽象表征...；几乎没有什么是通过强化、监督或模仿学习的
- 推理 = 模拟 / 预测 + 目标的优化：在计算上比自回归生成更强大。
- H-JEPA 与非对比性训练就是这样的：概率生成模型和对比方法是注定要失败的。
- 内在成本和架构驱动行为并决定学习的内容
- 情感是自主智能的必要条件：批评者或世界模型对结果的预期 + 内在的成本。

LeCun 总结了 AI 研究的当前挑战：（推荐阅读：[思考总结 10 年，图灵奖得主 Yann LeCun 指明下一代 AI 方向：自主机器智能](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650849483&idx=2&sn=8fff61962a8a2eb02cda90cdedadf26d&chksm=84e504b5b3928da3f557ec2c0c2ed7edfb3769d33ccad48ab270479949eaddc44bd56d017309&scene=21#wechat_redirect)）
- 从视频、图像、音频、文本中找到训练基于 H-JEPA 的世界模型的通用方法；
- 设计替代成本以驱动 H-JEPA 学习相关表征（预测只是其中之一）；
- 将 H-JEPA 集成到能够进行规划 / 推理的智能体中；
- 为存在不确定性的推理程序（基于梯度的方法、波束搜索、 MCTS....) 分层规划设计推理程序；
- 尽量减少在模型或批评者不准确的情况下使用 RL（这是不准确的，会导致不可预见的结）；

Position paper:
- [A path towards autonomous machine intelligence](https://openreview.net/forum?id=BZ5a1r-kVsf)
- Longer talk: search “LeCun Berkeley” on YouTube

Modular Architecture for Autonomous AI
- `Configurator` 配置器
  - Configures other modules for task
- `Perception` 感知器
  - Estimates state of the world
- `World Model` 世界模型
  - Predicts future world states
- `Cost` 计算不舒适度
  - Compute “discomfort”
- `Actor` 演员
  - Find optimal action sequences
- `Short-Term Memory` 短时记忆
  - Stores state-cost episodes
- ![](https://i0.wp.com/bdtechtalks.com/wp-content/uploads/2022/03/Yann-LeCun-Meta-AI-world-model-architecture.jpeg?w=1392&ssl=1)
- 详见博文：[Meta’s Yann LeCun on his vision for human-level AI](https://bdtechtalks.com/2022/03/07/yann-lecun-ai-self-supervised-learning/)


## LLM 是世界模型？

大语言模型（LLM）通过**预测对话序列中的下一个单词**生成输出，这种基于**概率建模**的机制已催生出趋近人类智力水平的对话交互、逻辑推理与内容创作能力。

但大模型与真正的`通用人工智能`（AGI）仍存在**显著鸿沟**。若能实现对环境中所有可能未来状态的全量模拟，是否就能构建出具备强智能的 AI 系统？

人类认知特质：
- 区别于 ChatGPT 的单一预测模式，人类能力体系天然存在具体技能实操与深度复杂任务处理的层级化差异。

模拟推理的典型案例：
- 某人（或许出于利己动机）通过心理层面模拟多种可能的行为后果，最终选择帮助一位正在哭泣的人。


### 正方

【2023-10-18】MIT 的 Max Tegmark 认为有世界模型
- MIT 和 东北大学的两位学者发现 大语言模型内部有一个世界模型，能够理解空间和时间
- LLM绝不仅仅是大家炒作的「`随机鹦鹉`」，它的确理解自己在说什么！
- 杨植麟：“Next token prediction（预测下一个字段）是唯一的问题。”“只要一条道走到黑，就能实现通用泛化的智能。”

【2023-10-20】[再证大语言模型是世界模型！LLM能分清真理谎言，还能被人类洗脑](https://www.toutiao.com/article/7291922903505830436)
- 【2023-10-10】[The Geometry of Truth: Emergent Linear Structure in Large Language Model Representations of True/False Datasets](https://arxiv.org/abs/2310.06824)
- [dataexplorer](https://saprmarks.github.io/geometry-of-truth/dataexplorer)
- MIT等学者的「世界模型」第二弹来了！这次，他们证明了LLM能够分清真话和假话，而通过「脑神经手术」，人类甚至还能给LLM打上思想钢印，改变它的信念。

新发现: LLM还可以区分语句的真假！
- 研究人员建立了简单、明确的真/假陈述数据集，并且把LLM对这些陈述的表征做了可视化。清晰的线性结构，真/假语句是完全分开的，线性结构是分层出现，如果是简单的陈述，真假语句的分离会更早出现，如果是「芝加哥在马达加斯加，北京在中国」这类复杂的陈述，分离就会更晚
  - 第0层时，「芝加哥在马达加斯加」和「北京在中国」这两句话还混在一起。随着层数越来越高，大模型可越来越清晰地区分出，前者为假，后者为真
  - ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/7273f53308fb4467b5d0c8267df940b6~tplv-tt-origin-asy2:5aS05p2hQOaWsOaZuuWFgw==.image?_iz=58558&from=article.pc_detail&x-expires=1698506420&x-signature=eGcsdZERd2A7u4tFr5EGKw9ZAsk%3D)

证明了两点——
1. 从一个真/假数据集中提取的方向，可以准确地对结构和主题不同的数据集中的真/假语句进行分类。
  - 仅使用「x大于/小于y」形式的语句找到的真值方向，在对西班牙语-英语翻译语句进行分类时的准确率为97%，例如「西班牙语单词『gato』的意思是『猫』」。
2. 更令人惊喜的是，人类可以用确定的**真相方向**给LLM「洗脑」，让它们将虚假陈述视为真实，或者将真实陈述视为虚假。
  - 「洗脑」前，对于「西班牙语单词『uno』的意思是『地板』」，LLM有72%的可能认为这句话是错误的。
  - 但如果确定LLM存储这个信息的位置，覆盖这种说法，LLM就有70%的可能认为这句话是对的。
  - ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/6db3629e7fdb495580f6801f2fc56030~tplv-tt-origin-asy2:5aS05p2hQOaWsOaZuuWFgw==.image?_iz=58558&from=article.pc_detail&x-expires=1698506420&x-signature=xOozb5G6zTvWyAtRE4yTW6kqEpE%3D)

这种办法来提供模型的真实性，减轻幻觉。

### 反方

【2024-6-18】[GPT-4不是世界模型，LeCun双手赞同！ACL力证LLM永远无法模拟世界](https://mp.weixin.qq.com/s/-YjuaZ44SnVEsooYJea0Qw?s_channel=4&s_trans=1232977597_)

ACL 2024 顶会
- [Can Language Models Serve as Text-Based World Simulators?](https://arxiv.org/pdf/2406.06485)

UA微软等机构最新研究发现，GPT-4在复杂环境的模拟中，准确率甚至不及60%。
- LeCun激动地表示: 世界模型永远都不可能是LLM。

GPT-4 模拟基于常识任务的状态变化时，比如烧开水，准确度仅有60%

如何量化LLM的规划能力? 
- 作者提出全新的基准测试——bytesized32-state-prediction，并在上面运行了GPT-4模型。
- [GPT-simulator](https://github.com/cognitiveailab/GPT-simulator)

文本环境中，智能体通过自然语言，完成特定的目标。

将文本虚拟环境形式化，建模为一种`马尔可夫决策过程`（POMDP），共有7个元组：S, A, T , O, R, C, D。
- S表示**状态空间**，A表示**行动空间**，T:S×A→S表示**状态转移函数**，O表示**观测函数**，R:S×A→R表示**奖励函数**，C表示用自然语言描述目标和动作语义的「**上下文信息**」，D:S×A→{0,1}表示**二元指示函数**，用0或1标记智能体是否完成任务。
- 上下文C为模型提供了除环境外的额外信息，比如行动规则、物体属性、打分规则和状态转换规则等等。

研究人员还提出了一个预测任务，称为 LLM-as-a-Simulator（LLM-Sim），作为定量评估大模型作为可靠模拟器的能力的一种方法。

LLM的预测模式也分为两种：预测下一步的完整状态，或者预测两个时刻之间的状态差。
- Bytesized32-SP基准测试的数据来源于公开的Bytesized32语料库，其中有32个人类编写的文字游戏。

网友：
> 目前的LLM能达到约60%的准确率（不专门为任务进行训练），这至少是某种「世界模型」了，而且每一代LLM都在提升。

Hinton
- AI已经不再是仅仅依赖于过去，基于统计模型做下一个token的预测，而是展现出更高的「理解」能力
- 大模型想要成为世界终极模拟器，还很远

## 案例

### I-JEPA

【2023-6-14】[LeCun世界模型出场！Meta首个“类人”模型，自监督学习众望所归](https://www.toutiao.com/article/7244395665281811005), [META官方](https://ai.facebook.com/blog/yann-lecun-ai-model-i-jepa)

LeCun在公开演讲中，再次批评了GPT大模型：<span style='color:red'>根据概率生成自回归的大模型，根本无法破除幻觉难题</span>。甚至直接发出断言：<span style='color:red'>GPT模型活不过5年</span>。

Meta震撼发布了一个「类人」的人工智能模型 I-JEPA，它可以比现有模型更准确地分析和完成缺失的图像。
- 论文地址: [Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2301.08243)
- 图像联合嵌入预测架构`I-JEPA`模型，是史上第一个基于LeCun世界模型愿景关键部分的AI模型。

自监督学习的通用架构中，系统会学习捕捉不同输入之间的关系。目标是将高能量分配给不兼容的输入，将低能量分配给兼容的输入。

自监督学习的常见架构
- [img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/bcd01573c416423ab32891b8175296c8~noop.image)

这三种架构的区别
- (a) 联合嵌入（不变）架构会学习为兼容的输入x、y输出相似的嵌入，为不兼容的输入输出不相似的嵌入。
- (b) 生成式架构会学习直接从兼容的信号x重建信号y，使用以附加变量z（可能是潜变量）为条件的解码器网络，以促进重建。
- (c) 联合嵌入预测架构学习从兼容信号x中预测信号y的嵌入，使用以附加变量z（可能是潜变量）为条件的预测网络，来促进预测。

划重点：
- I-JEPA 填充缺失片段时，用的就是有关世界的背景知识！而不是像其他模型那样，仅仅通过查看附近的像素。
- I-JEPA就是通过创建外部世界的内部模型来学习。在补全图像的过程中，它比较的是图像的抽象表征，而不是比较像素本身。

在多个计算机视觉任务上，`I-JEPA`都表现出了强大的性能，并且比其他广泛使用的CV模型计算效率高得多

CVPR 2023, 距离提出「世界模型」概念一年多，眼看着LeCun就要实现自己的星辰大海了。训练代码和模型已经开源。
- [img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/62697ade45094eee86c9ec90d5f5e185~noop.image)
- 创造出一个机器，学习世界如何运作的内部模型，更快速地学习，为完成复杂任务做出计划，并且随时应对不熟悉的新情况。

> 联合嵌入架构是人工智能的未来，而不是生成式

### 蔚来 NWM

【2024-7-29】[蔚来世界模型NWM 万千平行世界寻找最优解](https://www.nio.cn/smart-technology/20241120002)

详见站内专题: [自动驾驶](drving#蔚来汽车)

### PAN

【2025-7-9】[世界模型陷入困境？邢波团队深度剖析五大缺陷，全新 PAN 范式登场](https://mp.weixin.qq.com/s/4m3T9xnhEgi6OfQgKhlqNA)

卡耐基梅隆大学（CMU）、阿联酋穆罕默德・本・扎耶德人工智能大学（MBZUAI）、加州大学圣迭戈分校（UCSD）的研究团队，针对当前AI领域最前沿的研究方向——`世界模型`（World Models）的局限性展开了深入探讨。
- 论文：[Critiques of World Models](https://arxiv.org/pdf/2507.051)


构建与训练世界模型时，有五个关键要
- 其一，筛选并筹备蕴含目标世界信息的**训练数据**，数据需精准反映世界特征，为模型奠基
- 其二，构建`通用表征空间`，用于刻画潜在**世界状态**，这一空间承载的信息要远超直观观测数据，能够挖掘深层语义与关联；
- 其三，设计能对表征进行高效推理的**架构**，确保模型可基于已有表征，灵活且准确地推导未知；
- 其四，选定恰当的`目标函数`，以此精准引导模型训练，让模型朝着预期方向优化；
- 其五，明确世界模型在决策系统中的运用方式，使其能有效助力决策制定 。

创新性地提出了全新的世界模型架构`PAN`（Physical, Agentic, and Nested AGI System）。

PAN架构依托分层、多级以及混合连续/离散的表示形式，并采用生成式与自监督学习框架，旨在全方位提升模型性能。

PAN世界模型的详尽信息与实验结果将很快在另一篇论文中呈现。MBZUAI校长、CMU教授`邢波`在论文提交后，特意转推该论文，并表示PAN模型即将发布27B的第一版，此版本将成为首个可实际运行的通用世界模拟器，有望为世界模型领域带来新的变革 。

PAN架构严格遵循以下五大设计准则：
- 1）融合全模态体验数据，打破单一模态的信息壁垒；
- 2）构建连续与离散表示的混合体系，实现细节捕捉与抽象推理的平衡；
- 3）以增强型大语言模型（LLM）为主干，搭建分层生成建模与生成式潜在预测架构；
- 4）采用基于观测数据的生成损失函数，确保模型与现实世界的语义锚定；
- 5）通过强化学习（RL）机制，将世界模型转化为智能体的体验模拟器。

由 PAN 世界模型驱动的模拟推理智能体。与依赖即时反应策略的传统强化学习智能体，或在决策瞬间需耗费高额算力模拟未来的模型预测控制（MPC）智能体不同，其创新性地运用 PAN 生成的预计算模拟缓存。

决策进程中，智能体依据当下的认知信念与预期结果筛选行动方案，以此达成更高效、更灵活且更具目的性的规划模式。这种决策机制与人类推理的灵活性更为接近。

世界模型的终极目标并非生成视觉逼真的虚拟场景，而是对现实世界所有可能性空间的结构化模拟。当前领域的研究仍处于初级阶段，而PAN架构通过批判性重构与建设性创新，为下一代世界模型的理论突破与工程实现提供了可验证的探索方向。这种兼具学术严谨性与工程可行性的研究范式，有望推动世界模型从概念构想迈向真正的通用智能基础设施。

### 阿里 WorldVLA

【2025-6-26】全球首个融合世界模型与动作模型的自回归系统：WorldVLA，由阿里巴巴达摩院联合浙江大学等团队推出，使机器人既能理解环境又能精准执行动作
- 【论文题目】[WorldVLA: Towards Autoregressive Action World Model](https://arxiv.org/pdf/2506.21539)
- 代码 [WorldVLA](https://github.com/alibaba-damo-academy/WorldVLA)
- 解读 [WorldVLA：世界模型实现视觉-动作双向增强，抓取精度显著提升](https://zhuanlan.zhihu.com/p/1923190049685640753)

如何让机器像人类一样，既能理解环境又能精准执行动作？传统机器人要么机械执行指令却不懂物理规律，要么能预测环境变化却无法自主决策。

阿里巴巴 DAMO Academy 联合湖畔实验室与浙江大学推出 WorldVLA——全球首个融合世界模型与动作模型的自回归系统。
- （1）动作模型：解析视觉与语言指令，生成抓取、移动等动作序列
- （2）世界模型：基于物理规律预测“若执行此动作，环境将如何变化”

两者形成双向增强循环，这种协同改变了传统机器人“盲目执行指令”的局限。
- ![](https://pic2.zhimg.com/v2-594de454510707939eb7c508d4d147c7_1440w.jpg)


### Genie

#### Genie 1/2

2024年，谷歌 `DeepMind` 首次放出世界模型——`Genie 1`和G`enie 2`，为AI智能体生成全新环境。

#### Genie 3


Genie 3是首个支持「实时交互」的世界模型，相较于Genie 2，一致性和真实感均有提升，而且时间更长，几分钟，内容还能保持连贯性。

【2025-8-5】Genie 3，一句话生成动态世界。
- DeepMind 官网:[Genie 3: A new frontier for world models](https://deepmind.google/discove)

功能
- 每秒20-24帧速度，实时生成720p画面
- 还能持续数分钟一致性

![](https://picx.zhimg.com/80/v2-852cc4be9bbb8b23eefb3afa4165023e_1440w.webp?source=2c26e567)

Genie 3升级点
- 生成时长史诗级加强——一口气能搞定长达数分钟，且内容连贯的可交互世界。

原理：
- 通过自回归方式逐帧生成，Genie 3 能在几分钟内保持环境物体和细节的一致性，视觉记忆最长可达一分钟。
- Genie 3一致性是涌现能力。NeRFs和高斯溅射（Gaussian Splatting）也能实现一致的可导航3D环境，但依赖显式3D表征。相比之下，Genie 3 生成的世界则远为动态和丰富，因为模型根据世界描述和用户行为逐帧创造

Genie 3 问世，标志着世界模拟AI迈向了全新高度，加速了人类通向AGI/ASI的终极目标

![](https://pic1.zhimg.com/80/v2-060df672ed57b04e9b95a8dcdebb6b7b_1440w.webp?source=2c26e567)

![](https://pic1.zhimg.com/80/v2-50a9b7ef0fe3a7e22bd8ebfac35358a2_1440w.webp?source=2c26e567)




# 结束

