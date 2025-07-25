---
layout: post
title:  "用户模拟器-User Simulator"
date:   2020-08-12 20:46:00
categories: 深度学习 大模型
tags: 对话系统 用户模拟器 性格模拟 角色模拟 论文 simulator agent 智能体 数字分身 评测
excerpt: 对话系统之用户模拟器专题
author: 鹤啸九天
mathjax: true
permalink: /simulator
---

* content
{:toc}

# 总结


## 资料

- 【2021-7-26】[机器人性格综述](https://max.book118.com/html/2017/0525/109104518.shtm)
- 【2019-8-5】阿里小蜜：[最新综述：对话系统之用户模拟器](https://blog.csdn.net/c9yv2cf9i06k2a9e/article/details/98549007)

### 论文

- 论文1《A User Simulator for Task-Completion Dialogues》
- 论文2《End-to-End Task-Completion Neural Dialogue Systems》

## 实例

- 【2020-12-16】[天猫精灵对战小爱同学](https://www.bilibili.com/video/BV1Rb411W7PG)

<iframe src="//player.bilibili.com/player.html?aid=47805723&bvid=BV1Rb411W7PG&cid=83737221&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="600" width="100%"> </iframe>


# 用户模拟器

## 用户模拟器产生背景

- 近几年来，强化学习在任务导向型对话系统中得到了广泛的应用，对话系统通常被统计建模成为一个**马尔科夫决策过程**（Markov Decision Process）模型，通过随机优化的方法来学习对话策略。
- 任务导向型对话系统用于帮助用户完成某个任务如查电影、找餐馆等，它一般由四个模块组成：
  - **自然语言理解**模块（Natural Language Understanding, NLU）
  - **对话状态跟踪**模块（Dialog State Tracking, DST）
  - **对话策略**模块（Dialog Policy, DP）
  - **自然语言生成**模块（Natural language Generation, NLG）
- 其中 DST 和 DP 合称为**对话管理**模块（Dialog Manager，DM）。
  - 摘自：[对话系统之用户模拟器综述-V1](https://zhuanlan.zhihu.com/p/77875945)
- 在和用户的每轮交互过程中，对话系统利用 NLU 将用户的语句解析成为机器可理解的语义标签，并通过 DST 维护一个内部的对话状态作为整个对话历史的紧凑表示，根据此状态使用 DP 选择合适的对话动作，最后通过 NLG 将对话动作转成自然语言回复。对话系统通过和用户进行交互得到的对话数据和使用得分则可用于进行模型的强化学习训练。
- 然而在实际应用中，和真实用户的交互成本昂贵，数据回流周期慢，不足以支持模型的快速迭代，因此研究者们通常会构建一个**用户模拟器**（User Simulator, US）作为对话系统的交互环境来进行闭环训练。有了用户模拟器产生任意多的数据，对话系统可以对状态空间和动作空间进行充分地探索以寻找最优策略。
- 一个效果良好的用户模拟器，我们期望它具备以下 3 个特征：
  - ①一个总体的**对话目标**，能够生成上下文连贯的用户动作；
  - ②足够的**泛化能力**，在语料中未出现的对话情形里也能生成合理的行为；
  - ③可以给出定量的**反馈评分**用于指导模型学习优化。
- 为了实现以上目标，学术界做了大量的研究工作，从最基础的 **bi-gram** 模型 [4]，到经典实用的 **Agenda-based**的方法 [2]，再到最近基于**深度学习**的用户模型 [9, 10]，用户模拟器的效果得到了显著提升，也为对话模型的训练提供了有效的方法。

- ![](http://5b0988e595225.cdn.sohucs.com/images/20190806/d52fc80813ad431d946a1cb51cce9248.jpeg)
- 用户模拟器的基本结构: **用户模拟器**（蓝色部分）和**对话系统**（红色部分）
- 图里是一个比较典型的用户模拟器 [1]，对话开始时用户模拟器基于 User Goal（用户目标）发出一个话术：
  - “Are there any action movies to see this weekend?”（这个周末有什么动作片可以看的吗?）
  - 这句话进到对话系统的自然语言理解模块和对话管理模块后，生成一句系统动作：“request_location”（询问地点）。

简便起见，这里省略掉系统的 NLG 模块，系统回复直接送到用户模拟器的用户模型（User Model），通过用户状态更新和行为策略选择，生成用户对话行为：“inform(location=San Francisco)”（告知地点为旧金山），接下来经过 Error Model（可选）和 NLG 模块，生成对应的自然语言，比如：“San Francisco, please.”（帮我订旧金山的）。以此往复，用户模拟器和对话系统持续多轮交互，直到对话结束。

- 【2021-2-4】
- 用户模拟器所处的对话系统是一个**任务型**对话系统，用户模拟器与agent(系统或经纪人)的交流具有一定的任务导向，而不是闲聊。
- 任务目标：Agent通过与用户模拟器进行多轮对话，洞察用户模拟器所提出的条件(约束)以及请求，并尽所能及提供同时满足所有条件的请求内容
- 用户模拟器需要具备在沟通过程中改变自己条件的能力(可视为妥协)，agent力争做到满足用户需求(如：找房/约带看/询问房屋信息)，但在无能为力时，要尽可能收集用户需求



## 组成结构

典型的用户模拟器和对话系统的结构比较相似，包含以下 4 个基本组成部分：
1. **用户目标**（User Goal）：用户模拟的第一步是生成一个用户对话的目标，对话系统对此是不可知的，但它需要通过多轮对话交互来帮助用户完成该目标。
  - 一般来说，用户目标的定义和两种槽位相关: 
    - **可告知槽**（informable slots）形如“槽=值”是用户用于查询的约束条件
    - **可问询槽**（requestable slots）用户希望向系统问询的属性。
  - 例如：用户目标是 “inform(type=movie, genre=action, location=San Francisco, date=this weekend),request(price)”表达的是用户的目标是想要找一部本周在 San Francisco 上映的动作片，找到电影后再进一步问询电影票的价格属性。有了明确的对用户目标的建模，我们就可以保证用户的回复具有一定的任务导向，而不是闲聊。
2. **用户模型**（User Model）：用户模型对应着对话系统的对话管理模块，它的任务是根据对话历史生成当前的用户动作。用户动作是预先定义好的语义标签，例如“inform, request, greet, bye”等等。用户动作的选择应当合理且多样，能够模拟出真实用户的行为。**用户模型**是用户模拟器的核心组成部分，在接下来的章节里我们将会详细介绍各种具体模型和方法。
3. **误差模型**（Error Model）：它接在 User Model 下游，负责模拟**噪声**，对用户行为进行扰动以模拟真实交互环境下不确定性。
  - （1）简单的方式有：随机用不正确的意图替换正确的意图、随机替换为不正确的槽位、随机替换为不正确的槽值等；
  - （2）复杂的方式有模拟基于 ASR 或 NLU 混淆的错误。
4. **自然语言生成**（NLG）：如果用户模拟器需要输出自然语言回复，就需要 NLG 模型将用户动作转换成自然语言表述。
  - 例如用户动作标签“inform(type=movie, genre=action, date=this weekend)” 进行 NLG 模块后生成自然语句“Are there any action movies to see this weekend?”。

- 【2021-2-4】用户模拟器由 3个部分组成: User State Tracker、User Policy 和 User Model. 其中 User Model 可以针对不同的任务设定不同的参数，
- 比如：生成对话数据，对话评测，它们的 Goal 和 Profile 都可以不一样，这样既保证是一套统一的建模框架，同时又保证了系统的灵活性。


## 用户模拟器实现方法

- 用户模拟器的实现方法大致分成两类：
  - 基于规则的方法
  - 基于模型学习的方法。

- 总结
  - 优点：可以冷启动，用户行为完全可控
  - 缺点：需要专家手动构建，代价大，覆盖度不够，在对话行为灵活性和多样性上比较不足
- 使用场景
  - 话术简单清晰的填槽式对话任务


### 基于规则的方法

- 基于规则的方法需要专家手动构建
  - 优点是可以冷启动，用户行为完全可控；
  - 缺点是代价大，覆盖度不够，在对话行为灵活性和多样性上比较不足，适用于话术简单清晰的填槽式对话任务。

- 基于规则的方法中使用最为广泛的是基于**议程**（Agenda-based）的方法 [2, 3]，该方法对用户状态表示、状态转移、Agenda 更新、Goal 更新进行了精细建模，逻辑清晰，可落地性强，业界很多工作 [1, 15] 都基于该方法进行扩展和优化。
- 基于议程的方法通过一个栈的结构把对话的议程定下来，对话的过程就变成进栈和出栈的动作，上下文关联性很强，保证了用户动作生成的一致性，一般不会出现异常用户行为。但是，该方法在对话行为灵活性和多样性比较欠缺，在实操层面可以通过引入一些随机性提升灵活度。
- 基于议程的方法
  - 代表论文：The Hidden Agenda User Simulation Model, [论文链接](https://ieeexplore.ieee.org/document/4806280/)

#### 基于议程（Agenda-based）的方法

1. The hidden agenda user simulation model——通过一个栈的结构把对话的议程定下来，对话的过程就变成进栈和出栈的动作，上下文关联性很强，保证了用户动作生成的一致性，一般不会出现异常用户行为。
2. Agenda-based user simulation for bootstrapping a POMDP dialogue system
3. Task-oriented Dialogue System for Automatic Diagnosis
4. A User Simulator for Task-Completion Dialogues


### 基于模型的方法

- 总结
  - 优点：
    - 一般效果优于基于议程的规则方法，数据驱动，节省人力
  - 缺点：
    - 复杂对话建模困难，对数据数量要求很高，因此对于一些对话语料稀缺的领域效果很差
  - 适用场景
    - 语料丰富的领域

#### 端到端有监督学习

1. A Sequence-to-Sequence Model for User Simulation in Spoken Dialogue Systems——将对话上下文序列作为输入，然后输出用户动作序列。
2. Neural User Simulation for Corpus-based Policy Optimization for Spoken Dialogue Systems——提出了基于 RNN 的 Neural User Simulator (NUS) 模型。首先 NUS 通过用户目标生成器，对原对话数据中的对话状态标签进行预处理，得到一个完整对话中每一轮的具体用户目标，这样就相当于对用户目标改变进行了某种程度上的建模。

#### 联合优化策略

Iterative Policy Learning in End-to-End Trainable Task-Oriented Neural Dialog Models——对用户模拟器和对话系统分别采用了 RNN 进行端到端的建模并使用同一个回报函数优化，两者交替训练共同最大化累计回报。

#### 逆强化学习

User Simulation in Dialogue Systems using Inverse Reinforcement Learning——在马尔科夫决策过程  (MDP)  的框架下, 强化学习在是回报函数（reward function）给定下，找出最优策略以最大化累计反馈，而逆强化学习（Inverse reinforcement learning, IRL）就是通过给出最优策略估计出回报函数。

#### 协同过滤方法

Collaboration-based User Simulation for Goal-oriented Dialog Systems——在有高质量语料库的情况下，我们可以考虑直接根据对话上下文，从语料库中推荐出最恰当的用户语句作为用户模拟器的回复。


## 问题及挑战

用户模拟器面临的挑战
1. 对话行为**一致性**（Coherence）：对话行为要保证前后连贯，符合语境，避免出现不符合逻辑的对话行为。如何综合考虑对话上下文和 User Goal 等因素，保证用户行为序列在多轮交互过程中的一致性是一个有挑战的课题。
2. 对话行为**多样性**（Diversity）：模拟用户群的行为特性，需要建模这个群体的行为分布。例如某用户群是健谈的还是寡言的，是犹豫的还是果断的，各部分占比多少，这里引入用户群体画像特征，使得用户模拟器的行为更加丰富多样，贴近目标用户群体。这个方向学术界有一些研究进展，值得继续深入研究。
3. 对话行为的**泛化性**（Generalization）：目前来看，无论是基于规则方法还是基于模型学习的用户模拟器，在遇到语料中未曾出现的对话上下文时，表现出的泛化能力依旧比较有限。对话行为的泛化性直接体现了用户模拟器是否表现得如同真实用户一样处理更多未见的复杂的对话场景。这个方向有待学界更深入的探索。

## 模拟器评价方式

- 一个好的用户模拟器的评价方式需要满足以下几点要求：
  - 能够衡量生成的对话动作的一致性；
  - 评价方式和具体的任务无关；
  - 可以从目标信息中自动化地计算出一个标量值，而无需人工干预。
- 通常用户模拟器的评价指标可以分为**单轮**级别度量 (turn-level metrics) 和**对话**级别度量 (dialog-level metrics)。 
  - **单轮**级别度量：主要针对用户动作的语义标签，最常见度量是精确率，召回率和 F1 得分，对于每一轮可以计算：
    - ![](https://pic2.zhimg.com/80/v2-0aabe4f159c1cf7462e3e7cb02b3138d_1440w.jpg)
    - 以上的度量不能评估用户模型泛化能力，例如某个用户动作是合理的但因为在对话数据中并未出现，如果预测了就会导致得分低。因此还可以将用户动作的预测概率分布P和真实概率分布 Q 之间的 KL 距离作为度量，从概率分布上评估用户预测模型的合理性。
    - ![](https://pic4.zhimg.com/80/v2-1484738ecf7d60134276a76f8295c2fb_1440w.jpg)
    - 类似地，也可以用**对数似然值**或者**混淆度**（perplexity）来评估。
  - **对话**级别的度量：最常用的是**任务完成率**和**平均对话轮数**。
    - 将用户模型和对话系统进行真实交互，完成训练后的对话系统所能达到的任务完成率（通过记录对话系统是否完成用户目标得到）和平均每个对话的轮数可以作为评价与用户模型整体效果的有效指标。


## 工程实现

- 【2021-2-23】[user-simulator](https://github.com/wyshi/user-simulator)，Codebase for [How to Build User Simulators to Train RL-based Dialog Systems](https://arxiv.org/pdf/1909.01388.pdf), published as a long paper in EMNLP 2019. The sequicity part is developed based on [Sequicity: Simplifying Task-oriented Dialogue Systems with Single Sequence-to-Sequence Architectures](https://github.com/WING-NUS/sequicity).
  - RL training with agenda-based simulator: python run_mydata_new.py
  - RL training with supervised-learning-based simulator: python run_mydata_seq_new.py
  - Interacting with trained policies: policies are under simulator/policy/

### TC-Bot

- 台大的TC-Bot框架提供了一种开发和比较不同算法和模型的方法。 
- 对话系统由两部分组成：代理和用户模拟器。
- 通过一些示例来展示如何构建自己的代理和用户模拟器。

- [End-to-End Task-Completion Neural Dialogue Systems](https://github.com/MiuLab/TC-Bot), [代码](https://github.com/MiuLab/TC-Bot)

#### 代码结构

【2022-9-24】类依赖图，待更新

<div class="mermaid">
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
        +String beakColor
        +swim()
        +quack()
    }
    class Fish{
        -int sizeInFeet
        -canEat()
    }
    class Zebra{
        +bool is_wild
        +run()
    }
</div>

#### 如何构建自己的代理？

- 对于所有代理，它们都从Agent类（agent.py）继承，该类为用户提供了一些实现其代理的通用接口。 在agent_baseline.py文件中，实现了五个基于规则的基本代理：
  - InformAgent：每次依次通知所有槽位； 它不请求任何信息/槽位。
  - RequestAllAgent：依次请求所有槽位； 它不能告知任何信息/槽位。
  - RandomAgent：每次都会随机请求槽位； 它不能告知任何信息/槽位
  - EchoAgent：通知请求槽位中的最后一个用户动作； 它不能请求任何信息/槽位。
  - RequestBasicsAgent：逐个请求子集中的所有基本槽位，然后在最后一轮选择notify（任务完成）； 它不能告知任何信息/槽位。

所有代理仅重新实现两个函数：initialize_episode（）和state_to_action（）。 这里的state_to_action（）函数不要求代理的结构，实现的是从状态到动作的映射，这是代理的核心部分。下面是RequestBasicsAgent的示例：


当然agent.py中还包含三个函数:
- set_nlg_model():设置nlg模型，nlg主要作用是根据动作信息和状态信息，生成自然语言。
- set_nlu_model():设置nlu模型，nlu的主要作用是从自然语言中生成具体动作。
- add_nl_to_action():通过动作信息生成自然语言。

register_experience_replay_tuple():将来自环境的反馈，存储作为以后的训练数据。
所有基于规则的代理只支持通知或请求操作，当然也可以实现更复杂的基于规则的代理，该代理可以支持多种操作，包括通知，请求，确定问题，确定答案，拒绝等。

agent_dqn.py提供了RL代理（agt = 9），该代理包装了DQN模型。 除了以上两个函数外，RL代理中还有两个主要函数：run_policy（）和train（）。 run_policy（）实现 e-greedy策略，train()调用DQN的批训练函数。

agent_cmd.py提供了命令行代理（agt = 0），作为代理可以与用户模拟器进行交互。 命令行代理支持两种类型的输入：自然语言（cmd_input_mode = 0）和对话框动作（cmd_input_mode = 1）。 清单3展示了一个命令行代理通过自然语言与用户模拟器交互的示例； 清单4展示了一个命令行代理通过对话框与用户模拟器进行交互的示例。

注意：
- 当上个用户回合是请求动作时，系统将在数据库中为代理显示一行建议可用答案，如列表4中的回合0所示。 基于规则的代理和RL代理都将使用数据库中的槽位值来回答用户。 此处，命令行代理的一种特殊情况是，人工（作为命令行代理）可以输入用户请求的任何随机答案，当输入的答案不在数据库中时，状态跟踪器将对其进行纠正，并强制代理使用代理数据库中的值作为回复。 例如，在列表4的第1回合中，如果您输入notify（theater = amc pacific），那么用户收到的实际答案就是notify（theater = carmike summit 16），因为数据库中不存在amc pacific， 为了避免代理通知用户不可用值的这种在线操作，我们限制代理要使用建议列表中的值。
- 代理的倒数第二轮通常是采用通知形式（taskcomplete）或类似于“好的，您的票已预订。”的自然语言，其目的是为了通知用户模拟器代理已经完成了任务，并且准备预订电影票。
- 为了结束对话，代理的最后一个回合通常是对话通知形式的thank（）或自然语言中的“感谢”。


#### 如何构建自己的用户模拟器？
        
- 有一个用户模拟器类（usersim.py），它提供了一些通用接口来实现其用户模拟器。 所有用户模拟器都是从此类继承的，并且应该重新实现以下两个函数：initialize_episode（）和next（）。 usersim_rule.py文件实现了基于规则的用户模拟器。 这里的next（）函数实现了所有规则和根据上一个代理动作来发出下一个用户动作。这是例子usersim_rule.py：


#### 如何构建一个对话管理器

- dialog_manager.py类中包含的主要函数介绍：
- 根据历史的对话状态，生成当前论的对话
  - initialize_episode（）：每一个epoch开始之前的初始工作，主要包括初始化用户模拟器和代理，以及对话状态追踪器。
  - next_turn（）：主要分为两个主要步骤，第一步通过状态跟踪器获得当前状态，代理根据当前状态，得到动作类型。根绝动作类型来生成自然语言。用户模拟器是通过历史对话字典，生成下一轮的对话、对话中止标记和对话对话奖励，并且更新用户模拟器的动作到状态追踪器里里面。
  - reward_function（）:通过对话状态来计算奖励，奖励有正有负。
  - reward_function_without_penalty():通过对话状态来计算奖励，奖励只有正的，其中失败的奖励为0。
  - print_function():打印用户模拟器和代理的当前状态

 kb_helper.py文件包含的主要函数介绍：

这个文件功能主要是将current_slots填充到inform_slots中
- fill_inform_slots（）：将current_slots填充到inform_slots中
- available_slot_values（）：根据当前约束返回可用于该槽位的一组值
- available_results_from_kb（）：返回current_slots中所有的可用槽位
- available_results_from_kb_for_slots（）：返回inform_slots中每个约束的统计信息
- database_results_for_agent（）：返回当前约束匹配的结果字典
- suggest_slot_values（）：根据目前槽位，返回建议的槽位值

 state_tracker.py类包含的主要函数介绍：

主要功能是更新用户模拟器和代理的状态。
- dialog_history_vectors（）：返回用向量表示的对话历史信息
- dialog_history_dictionaries（）：返回用字典保存的对话历史信息
- kb_results_for_state（）：根据当前通知的槽位返回有关数据库结果的信息
- get_state_for_agent（）：获取状态表示以发送给代理
- get_suggest_slots_values（）：获取请求槽位的建议值
- get_current_kb_results（）：获取当前状态的kb_results
- update（）：根据最新动作更新状态

#### 如何构建一个自然语言生成模块

nlu.py主要函数介绍：主要是讲自然语言解析成Dia-Act
- generate_dia_act（）： generate the Dia-Act with NLU model通过NLU模型生成Dia-Act
- load_nlu_model（）：加载NLU模型
- parse_str_to_vector（）：将字符串用向量来表示
- parse_nlu_to_diaact（）：将BIO和意图解析以后放入到dia_act中
- refine_diaact_by_rules（）：通过规则细化dia_act

#### 如何构建一个自然语言理解模块

nlg.py主要函数介绍：主要功能是将动作转换成自然语言。
- post_process（）：填充模板语句中的空的槽位
- convert_diaact_to_nl（）：通过规则加模型将Dia_Act转换成自然语言
- translate_diaact（）：将dia_act用向量表示出来，然后通过模型生成句子。 
- load_nlg_model（）：加载训练好的nlg模型。
- diaact_to_nl_slot_filling（）：用槽位的真实值去填充槽位信息。
- load_predefine_act_nl_pairs（）：加载预定义好的 Dia_Act&NL键值对。

#### 如何构建一个用户模拟器的DQN模型

dqn.py主要函数介绍：DQN主要是训练一个强化学习的对话过程。
- getStruct（）：返回模型的其他参数
- fwdPass(): DQN的前向传播过程
- bwdPass():DQN的反向传播过程
- batchForward():批量的前向传播过程
- batchDoubleForward():双批量的前向传播过程
- batchBackward():批量的反向传播
- costFunc():代价函数计算
- singleBatch():单批次整个模型的计算过程
- predict():预测

#### 如何构建用户模拟器的数据结构


#### 训练时注意事项

- 为了训练RL代理，需要从一些规则策略经历（用户和代理的一个完整对话过程）元组开始初始化一个经历重放缓冲池，也可以从一个空的经历重放缓冲池开始。 建议使用某些规则或监督策略来初始化经历重放缓冲池，很多相关研究已经证明了这种方式的优势处，例如，良好的初始化策略可以加快RL训练的速度。 在这里，我们使用非常简单的基于规则的策略来初始化经历重放缓冲池。

- RL代理是DQN网络。 在训练中，我们使用e-greedy策略和动态经历重放缓冲池。 经历重放缓冲池的大小是动态变化的。 一个重要的DQN的技巧是通过引入目标网络，这样网络会缓慢更新和计算目标网络短期内达到的目标值。

- 训练过程可以这样定义：在每个epoch中，我们模拟N个对话，并将这些状态转换元组（st，at，rt，st + 1）添加到经历重放缓冲池中，训练和更新当前的DQN网络。在一个epoch中，当前DQN网络将在批次结束时进行多次更新，具体取决于批次大小和经历重放缓冲池的当前大小。 在一个模拟epoch中，目标网络将被当前DQN网络取代，目标DQN网络仅在一个epoch中更新一次。经历重放缓冲池更新策略如下：首先，我们将从模拟中累积所有经验元组，并刷新经历重放缓冲池，直到当前RL代理达到成功率阈值（即，success_rate_threshold = 0.30），然后使用当前RL代理的经验元组重新填充缓冲区。一般而言DQN的初始性能不好，无法生成足够好的经历重放元组，因此，在当前的RL代理可以达到一定成功率之前，我们不会刷新经历重放缓冲池。接下来的训练过程，在每个epoch中，我们都会估算当前DQN代理的成功率，如果当前DQN代理足够好（即比目标网络更好），则将刷新并将经历重播缓冲区进行轮询-填充。图1显示了没有NLU的RL代理的学习曲线和NLG，图2是带有NLU和NLG的RL代理的学习曲线，训练RL代理以适应NLU和NLG的错误和噪声需要花费更长的时间。
- 表1显示了由基于规则的代理和RL代理与电影订票中的用户模拟器交互生成的一个成功和一个失败对话示例。 为了提供信息，我们还在对话的开头明确显示用户目标，但是代理对用户目标一无所知，其目标是帮助用户实现此目标并预订正确的电影票。
- 表2是用户模拟器与SimpleRL-SoftKB和End2End-RL代理之间的对话。Critic_rating槽位值是用户模拟器中常见的错误源，因此，所有学习到的策略都倾向于多次请求该值。
- 图1：没有NLU和NLG的策略训练学习曲线：绿线是规则代理，我们使用它来初始化体验重播缓冲池； 蓝线是RL代理； 橙色线是最佳上限，它是通过代理数据库中可达到的用户目标数与用户目标总数的比。
- 图2：使用NLU和NLG进行的端到端策略训练的学习曲线：绿线是规则我们用来初始化经历重放缓冲池的代理； 蓝线是学习RL代理的曲线； 橙色线是最佳上限，由代理程序数据库中可达到的用户目标数与用户目标总数之比。
- 表1：基于规则的代理和RL代理与用户模拟器生成的两个示例对话：左列显示规则和RL代理均成功； 右列显示基于规则的代理失败，而RL代理成功。
- 表2：用户模拟器与SimpleRL-SoftKB和End2End-RL代理之间的对话示例。 在每次对话结束时，代理会告知KB后验的前5个结果。 已经通知的用户目标以粗体显示。

## 数据集

google-research-datasets [simulated-dialogue](https://github.com/google-research-datasets/simulated-dialogue)

用户模拟的数据集，包括：
- 餐馆预订
- 电影票预定

We are releasing two datasets containing dialogues for **booking a restaurant table** and **buying a movie ticket**. The number of dialogues in each dataset are listed below. 

| Dataset            | Slots                | Train | Dev | Test |
| ------------------ | -------------------- | ----- | --- | ---- |
| Sim-R (Restaurant) | price\_range, location, restaurant\_name,<br>category, num\_people, date, time | 1116  | 349 | 775  |
| Sim-M (Movie)      | theatre\_name, movie, date, time,<br>num\_people                               | 384   | 120 | 264  |
| Sim-GEN (Movie)    | theatre\_name, movie, date, time,<br>num\_people                               | 100K  | 10K | 10K  |

源自：[Dialogue Learning with Human Teaching and Feedback in End-to-End Trainable Task-Oriented Dialogue Systems](https://arxiv.org/pdf/1804.06512.pdf) uses Sim-GEN

### Sim-GEN

Simulator Generated Dataset (sim-GEN)

This directory contains an expanded set of dialogues generated via dialogue **self-play** between a user simulator and a system agent, as follows:
-   The dialogues collected using the M2M framework for the movie ticket booking task (sim-M) are used as a seed set to form a crowd-sourced corpus of natural language utterances for the user and the system agents.
-   Subsequently, many more dialogue outlines are generated using self-play between the simulated user and system agent.
-   The dialogue outlines are converted to natural language dialogues by replacing each dialogue act in the outline with an utterance sampled from the set of crowd-sourced utterances collected with M2M.

In this manner, we can generate an arbitrarily large number of dialogue outlines and convert them automatically to natural language dialogues without any additional crowd-sourcing step. Although the diversity of natural language in the dataset does not increase, the number of unique dialogue states present in the dataset will increase since a larger variety of dialogue outlines will be available in the expanded dataset.

This dataset was used for experiments reported in [this paper](https://arxiv.org/abs/1804.06512). 

The data splits are made available as a .zip file containing dialogues in JSON
format. Each dialogue object contains the following fields:

*   **dialogue\_id** - *string* unique identifier for each dialogue.
*   **turns** - *list* of turn objects:
    *   **system\_acts** - *list* of system dialogue acts for this system turn:
        *   **name** - *string* system act name
        *   **slot\_values** - *optional dictionary* mapping slot names to
            values
    *   **system\_utterance** - *string* natural language utterance
        corresponding to the system acts for this turn
    *   **user\_utterance** - *string* natural language user utterance following
        the system utterance in this turn
    *   **dialogue\_state** - *dictionary* ground truth slot-value mapping after
        the user utterance
    *   **database\_state** - database results based on current dialogue state:
        *   **scores** - *list* of scores, between 0.0 and 1.0, of top 5
            database results. 1.0 means matches all constraints and 0.0 means no
            match
        *   **has\_more\_results** - *boolean* whether backend has more matching
            results
        *   **has\_no\_results** - *boolean* whether backend has no matching
            results

An additional file **db.json** is provided which contains the set of values for each slot.

Note: The date values in the dataset are normalized as the constants, "base_date_plus_X", for X from 0 to 6. X=0 corresponds to the current date (i.e. 'today'), X=1 is 'tomorrow', etc. This is done to allow handling of relative references to dates (e.g. 'this weekend', 'next Wednesday', etc). The parsing of such phrases should be done as a separate pre-processing step.


### Sim-M

Each dialogue is represented as a json object with the following fields:
*   **dialogue\_id** - A unique identifier for a dialogue.
*   **turns** - A list of annotated agent and user utterance pairs having the
    following fields:
    *   **system\_acts** - A list of system actions. An action consists of an
        action type, and optional slot and value arguments. Each action has the
        following fields:
        *   **type** - An action type. Possible values are listed below.
        *   **slot** - Optional slot argument.
        *   **value** - Optional value argument. If value is present, slot must
            be present.
    *   **system\_utterance** - The system utterance having the following
        fields.
        *   **text** - The text of the utterance.
        *   **tokens** - A list containing tokenized version of text.
        *   **slots** - A list containing locations of mentions of values
            corresponding to slots in the utterance, having the following
            fields:
            *   **slot** - The name of the slot
            *   **start** - The index of the first token corresponding to a slot
                value in the tokens list.
            *   **exclusive\_end** - The index of the token succeeding the last
                token corresponding to the slot value in the tokens list. In
                python, `tokens[start:exclusive_end]` gives the tokens for slot
                value.
    *   **user\_acts** - A list of user actions. Has the same structure as
        system\_acts.
    *   **user\_utterance** - The user utterance. It has three fields, similar
        to system\_utterance.
    *   **user_intents** - A list of user intents specified in the current turn.
        Possible values are listed below.
    *   **dialogue\_state** - Contains the preferences for the different slots
        as specified by the user upto the current turn of the dialogue.
        Represented as a list containing:
        *   **slot** - The name of the slot.
        *   **value** - The value assigned to the slot.

The list of action types is inspired from the Cambridge dialogue act schema
([DSTC2 Handbook](http://camdial.org/~mh521/dstc/downloads/handbook.pdf), Pg 19)
. The possible values are:
*   AFFIRM
*   CANT\_UNDERSTAND
*   CONFIRM
*   INFORM
*   GOOD\_BYE
*   GREETING
*   NEGATE
*   OTHER
*   NOTIFY\_FAILURE
*   NOTIFY\_SUCCESS
*   OFFER
*   REQUEST
*   REQUEST\_ALTS
*   SELECT
*   THANK\_YOU

The possible values of user intents are:
*   BUY\_MOVIE\_TICKETS


### Sim-R

Each dialogue is represented as a json object with the following fields:
*   **dialogue\_id** - A unique identifier for a dialogue.
*   **turns** - A list of annotated agent and user utterance pairs having the
    following fields:
    *   **system\_acts** - A list of system actions. An action consists of an
        action type, and optional slot and value arguments. Each action has the
        following fields:
        *   **type** - An action type. Possible values are listed below.
        *   **slot** - Optional slot argument.
        *   **value** - Optional value argument. If value is present, slot must
            be present.
    *   **system\_utterance** - The system utterance having the following
        fields.
        *   **text** - The text of the utterance.
        *   **tokens** - A list containing tokenized version of text.
        *   **slots** - A list containing locations of mentions of values
            corresponding to slots in the utterance, having the following
            fields:
            *   **slot** - The name of the slot
            *   **start** - The index of the first token corresponding to a slot
                value in the tokens list.
            *   **exclusive\_end** - The index of the token succeeding the last
                token corresponding to the slot value in the tokens list. In
                python, `tokens[start:exclusive_end]` gives the tokens for slot
                value.
    *   **user\_acts** - A list of user actions. Has the same structure as
        system\_acts.
    *   **user\_utterance** - The user utterance. It has three fields, similar
        to system\_utterance.
    *   **user_intents** - A list of user intents specified in the current turn.
        Possible values are listed below.
    *   **dialogue\_state** - Contains the preferences for the different slots
        as specified by the user upto the current turn of the dialogue.
        Represented as a list containing:
        *   **slot** - The name of the slot.
        *   **value** - The value assigned to the slot.

The list of action types is inspired from the Cambridge dialogue act schema ([DSTC2 Handbook](http://camdial.org/~mh521/dstc/downloads/handbook.pdf), Pg 19). The possible values are:
*   AFFIRM
*   CANT\_UNDERSTAND
*   CONFIRM
*   INFORM
*   GOOD\_BYE
*   GREETING
*   NEGATE
*   OTHER
*   NOTIFY\_FAILURE
*   NOTIFY\_SUCCESS
*   OFFER
*   REQUEST
*   REQUEST\_ALTS
*   SELECT
*   THANK\_YOU

The possible values of user intents are:
*   FIND\_RESTAURANT
*   RESERVE\_RESTAURANT



## 论文解读

### Dual Task Framework for Improving Persona-grounded Dialogue Dataset

- [Dual Task Framework for Improving Persona-grounded Dialogue Dataset](https://www.aaai.org/AAAI22Papers/AAAI-8011.KimM.pdf)

摘要：
- This paper introduces a simple yet effective data-centric approach for the task of improving **persona-conditioned** dialogue agents. Prior model-centric approaches unquestioningly depend on the raw crowdsourced benchmark datasets such as Persona-Chat. In contrast, we aim to fix annotation artifacts in benchmarking, which is orthogonally applicable to any dialogue model. Specifically, we augment relevant personas to improve dialogue dataset/agent, by leveraging the primal-dual structure of the two tasks, predicting dialogue responses and personas based on each other. Experiments on Persona-Chat show that our approach outperforms pretrained LMs by an 11.7 point gain in terms of accuracy

<object type="application/pdf" data="https://www.aaai.org/AAAI22Papers/AAAI-8011.KimM.pdf"
           id="review" style="width:100%;  height:800px; margin-top:0px;  margin-left:0px" >
</object>

### You Impress Me: Dialogue Generation via Mutual Persona Perception
 
- [You Impress Me: Dialogue Generation via Mutual Persona Perception](https://aclanthology.org/2020.acl-main.131.pdf)
- April 11, 2020，[作者主页](https://siviltaram.github.io/publication/2020-04-11-you)
- **个性化对话生成**（Personalized Dialogue Generation）是对话生成领域近几年的一个研究热点（Zhang et al. 2018）。个性的引入可以帮助对话生成模型产生更一致的、更有趣的回复。然而大部分工作仍像对待普通开放域对话生成那样，关注模型生成回复的流畅性，较少关注对话中对话者之间的互动和了解。相比于已有工作，我们显式地建模了对话者之间的了解，从而使得对话生成的结果更加有趣，且更加符合对话者的个性。
- 这篇论文提出了一个 Transmitter-Receiver 的框架来显式建模对话者之间的了解，其中 Transmitter 负责对话生成，而 Receiver 负责个性了解。在这个框架下，我们引入一个新颖的概念“相互个性感知”，来刻画对话者之间的信息交流，即对话者对彼此个性的了解程度。众所周知，高效的沟通能够让对话的双方充分了解并达成共识，所以相互个性感知的提升在一定程度上也代表了对话质量的提高。为了达成这个目标，我们首先按照传统的监督学习来训练Transmitter，然后让两个训练好的 Transmitter 通过互相对话进行**自我学习**（self-play）。在它们对话若干轮后，借助 Receiver 提供的个性感知奖励微调 Transmitter。

![](https://www.msra.cn/wp-content/uploads/2020/07/acl-2020-25.png)
 
- [PAPER](https://arxiv.org/pdf/2004.05388.pdf)，[CODE](https://github.com/SivilTaram/Persona-Dialogue-Generation)，[SLIDES](https://siviltaram.github.io/files/you-slides.pdf)，[MEDIA](https://mp.weixin.qq.com/s/Do_swfjTNi9Kf23E8LJb6A)

![](https://siviltaram.github.io/images/you-demo.JPG)


原文：

<object type="application/pdf" data="https://arxiv.org/pdf/2004.05388"
           id="review" style="width:100%;  height:800px; margin-top:0px;  margin-left:0px" >
</object>

解读ppt

<object type="application/pdf" data="https://siviltaram.github.io/files/you-slides.pdf"
           id="review" style="width:100%;  height:800px; margin-top:0px;  margin-left:0px" >
</object>

### 2021 ACL Transferable Dialogue Systems and User Simulators

[Transferable Dialogue Systems and User Simulators](https://aclanthology.org/2021.acl-long.13.pdf)

- 对话系统训练的困难之一：缺乏训练数据 --> 通过对话系统与用户模拟器之间的交互来自学习
- One of the difficulties in training dialogue systems is the **lack of training data**. We explore the possibility of creating dialogue data through the interaction between a **dialogue system** and a **user simulator**. Our goal is to develop a modelling framework that can incorporate new dialogue scenarios through **self-play** between the two agents. In this framework, we first pre-train the two agents on a collection of source domain dialogues, which equips the agents to converse with each other via natural language. With further fine-tuning on a small amount of target domain data, the agents continue to interact with the aim of improving their behaviors using reinforcement learning with structured reward functions. In experiments on the MultiWOZ dataset, two practical transfer learning problems are investigated:
- 1) **domain adaptation** and 
- 2) **single-to-multiple**
- domain transfer. We demonstrate that the proposed framework is highly effective in bootstrapping the performance of the two agents in transfer learning. We also show that our method leads to improvements in dialogue system performance on complete datasets.


<object type="application/pdf" data="https://aclanthology.org/2021.acl-long.13.pdf"
           id="review" style="width:100%;  height:800px; margin-top:0px;  margin-left:0px" >
</object>



## LLM 角色模拟

【2024-5-30】用 LLM 的 Agent 方案实现用户模拟器

### AgentSims

【2023-8-8】PTA、宾夕法尼亚大学、北航 推出 LLM 评估沙盒 AgentSims ，开源
- 论文 [AgentSims: An Open-Source Sandbox for Large Language Model Evaluation](https://arxiv.org/pdf/2308.04026)
- 代码 [AgentSims](https://github.com/py499372727/AgentSims)
- ![](https://github.com/py499372727/AgentSims/blob/main/cover.png)

现有的评估方法存在以下缺陷：
- （1）评估能力受限；单轮QA形式，无法全面评估
- （2）基准脆弱；测试集容易泄露
- （3）指标不客观：已有开放评测指标过时，GPT-4无法评估超GPT-4模型

基于任务的评估（即 LLM 代理在模拟环境中完成任务）是解决上述问题的**万能**方案。

AgentSims 易于使用，可供各学科研究人员测试特定能力。
- AgentSims 是一种**交互式**、**可视化**和**基于程序**的基础设施
- 在交互式图形用户界面上添加代理和建筑来建立自己的评估任务，或者通过几行代码来部署和测试新的支持机制，即**记忆**、**规划**和**工具使用**系统。
- [演示程序](https://agentsims.com)

### 对话推荐用户模拟器

【2024-3-13】加州大学
- 论文 [Evaluating Large Language Models as Generative User Simulators for Conversational Recommendation](https://arxiv.org/pdf/2403.09738v1)

大型语言模型(LLM)作为对话推荐系统，提出一种评估用户模拟器的新标准。

设计了五项评估任务, 每项任务都针对模拟器成为真实用户代理
- 选择待推荐项
- 偏好表达：二值, 喜欢/不喜欢
- 开放域偏好表达
- 请求推荐
- 反馈

通过在模拟器上运行这些任务, 展示了这些任务能有效地揭示模拟器与真实用户之间的差异。

choosing which items to talk about, expressing binary preferences, expressing open-ended preferences, requesting recommendations, and giving feedback



### MultiOn

【2024-6-13】[MultiOn](https://app.multion.ai/playground)
- 可在线体验
- 本地体验，chrome插件植入本地, 需要再 discord 上申请

演示视频
- [Exploring MultiOn: The Future of Personal AI Agents](https://www.youtube.com/watch?v=Y7QAfPOs-bc)

<iframe width="560" height="315" src="https://www.youtube.com/embed/Y7QAfPOs-bc?si=YHrmqoLok1s1Lrkg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### AgentSociety

【2025-2-24】[AgentSociety：清华大学的社会模拟器如何重塑社会科学研究？](https://chattools.cn/article/2153)
- [项目官网](https://agentsociety.readthedocs.io/en/latest/)
- Github仓库：[agentsociety](https://github.com/tsinghua-fib-lab/agentsociety/)
- arXiv技术论文：[paper](https://arxiv.org/pdf/2502.08691)


社会模拟器——AgentSociety。这款工具并非简单的游戏或娱乐应用，而是基于大型语言模型（LLM）构建的**复杂社会行为**模拟平台。

通过创造具有“类人心智”的智能体，旨在模拟和分析真实的社会现象，为政策制定、危机预警和社会科学研究提供新的视角和实验平台。

智能体并非简单的程序化角色，而是被赋予了情感、需求、动机和认知能力。每个智能体都有其独特的“心理画像”，包括性格、年龄、性别等，以及动态的个人状态，如情感、经济状况和社会关系。这种设计使得智能体的行为模式更加个性化和真实，能够模拟人类在复杂社会环境中的各种行为，例如移动、就业、消费和社交互动。


### Agent Hospital 

医院模拟器 Agent Hospital

【2024-5-5】清华 [【LLM-agent】医院agent：具有可进化医疗agent的医院模拟器](https://mp.weixin.qq.com/s/_0Lc2KNc2npmnCMi3XJPpA)
- [Agent Hospital:A Simulacrum of Hospital with Evolvable Medical Agents](https://arxiv.org/pdf/2405.02957)

基于大型语言模型（LLM）和agent技术构建医疗场景下的**医院模拟体**，命名为`医院agent`（Agent Hospital）。

医院agent不仅包括两种角色（**医疗专业人员**和**患者代理**）和数十个特定agent，还涵盖了医院内的流程如分诊、登记、咨询、检查和治疗计划，以及医院外的阶段如疾病和康复。

医院agent中，论文提出了`MedAgent-Zero`策略，用于医疗代理的发展，该策略不依赖参数和知识，允许通过模拟患者进行无限制的agent训练。该策略主要包括一个医疗记录库和经验库，使得agent能够像人类医生一样，从正确和失败的治疗中积累经验。



### AgentClinic

【2024-5-22】斯坦福、约翰霍普金斯推出 [AgentClinic](https://agentclinic.github.io/)
- [AgentClinic: a multimodal agent benchmark to evaluate AI in simulated clinical environments](https://arxiv.org/pdf/2405.07960)
- 代码 [agentclinic](https://github.com/samuelschmidgall/agentclinic)
- ![](https://agentclinic.github.io/static/videos/mainfigure.png)

AgentClinic 将**静态医疗 QA 问题**转化为临床环境（医生、患者、医疗设备）中的**代理**，以便为医学语言模型提供更具临床相关性的挑战。
- 问题：现有评测标准基于静态QA，无法处理交互式决策问题（interactive decision-making）
- 方案：在临床模拟环境中操作智能体，实现多模态评估LLM
  - AgentClinic: a multimodal benchmark to evaluate LLMs in their ability to operate as agents in simulated clinical environments.
  - 医生通过对话和交互数据来评估病人病情

诊断和管理患者是一个复杂的、连续的决策过程，需要**医生获取信息**---例如要执行哪些测试---并**采取行动**。人工智能 （AI） 和大型语言模型 （LLMs） 的最新进展有望对临床护理产生深远影响。

然而，目前的评估方案**过度依赖静态的医学问答基准**，缺乏现实生活中临床工作所需的**交互式决策**。

AgentClinic：一个多模式基准，用于评估LLMs在**模拟临床环境**中作为**代理**运行的能力。
- 基准测试中，**医生代理**必须通过对话和主动数据收集来发现患者的诊断。

发布两个开放基准：**多模态图像**和**对话环境** AgentClinic-NEJM 和**纯对话**环境。
- AgentClinic-MedQA: 代理以美国医学执照考试~（USMLE） 的案例为基础
- AgentClinic-NEJM: 代理以多模式新英格兰医学杂志 （NEJM） 的案例挑战为基础。

在患者和医生代理中嵌入**认知和隐性偏见** (cognitive and implicit biases)，以模拟有偏见的代理之间的真实互动。

引入**偏倚**会导致医生代理的诊断准确性大幅降低，以及患者代理的依从性、信心和后续咨询意愿降低。通过评估一套最先进的技术LLMs，一些在MedQA等基准测试中表现出色的模型在AgentClinic-MedQA中表现不佳。
- 在AgentClinic基准测试中，患者代理中使用的LLM药物是性能的重要因素。 
- 有限的相互作用和过多的相互作用都会降低医生代理的诊断准确性。

## 数字分身


### Second Me

【2025-3-12】Second Me 是`心识宇宙`（Mindverse）推出的开源**AI身份模型**，支持创建**完全私有**且**深度个性化**的AI代理，代表用户的“真实自我”。
- 项目官网：[Second Me](https://www.secondme.io/)
- GitHub仓库：[Second Me](https://github.com/mindverse/Second-Me)
- arXiv技术论文：[AI-native Memory 2.0: Second Me](https://arxiv.org/pdf/2503.08102)

Second Me 提供 `Chat Mode` 和 `Bridge Mode` 两种互动模式，分别支持个性化对话和作为用户与世界连接的桥梁，实现信息的个性化反馈与增强。

Second Me 支持在本地运行，确保用户数据的绝对隐私。Second Me帮助用户在不同情境中灵活表达自我，让用户在AI时代重新掌控自己的身份和数据。

主要功能
- 个性化身份创建：用户将自己的记忆、经验和偏好上传训练成AI代理，代理能代表用户的真实自我。
- 多角色适应：根据不同的场景（如工作、社交、学习）自动切换角色，保持用户的核心身份不变。
- Chat Mode：与用户直接对话，提供基于个人记忆的个性化回答。
- Bridge Mode：作为用户与外界的桥梁，增强需求表达和信息反馈。
- 隐私保护：Second Me 的运行完全本地化，用户数据存储在本地设备上。
- 智能记忆管理：支持快速识别模式、适应变化，与用户共同进化。


技术原理

- **分层记忆模型**（HMM）：
  - L0（**短期交互**记忆）：处理**即时上下文**信息，用在短期的交互和快速响应。
  - L1（**自然语言**记忆层）：总结和存储用户的重要信息，如个人简介、偏好标签等。
  - L2（**AI原生**记忆层）：基于模型参数学习和组织记忆，进行复杂的推理和知识检索。
- 个性化对齐架构（Me-alignment）：基于强化学习技术，将用户的分散数据转化为深度个性化的理解，确保AI精准把握用户的偏好和行为模式。
- **去中心化网络**：每个 Second Me 是一个独立的AI实体，基于点对点网络进行通信和协作，确保数据的隐私和安全性。
- 自动化训练管道：包括数据合成、过滤、监督式微调（SFT）、直接偏好优化（DPO）等步骤，确保模型的高效训练和个性化。
- **多智能体**框架：支持与其他AI代理或专家模型协作，基于增强上下文信息和优化交互过程，为用户提供更精准的服务。
- 链式推理：在训练和推理过程中基于CoT风格，逐步推理和详细解释，提高模型的逻辑性和准确性。

AI-native Memory 2.0: [Second Me](https://www.secondme.io/)，核心思想是收集自己的数据，然后通过SFT和DPO微调克隆第二个我。

这样做有什么用呢？主要是在人机交互时预判要做的事情，然后提前做。
- 打开了小红书这个网页，做出提前预判，自动帮我输入账号密码，然后完成登录动作。
- 论文上传给大模型，根据习惯自动提一些问题，自己和大模型交互帮我解读整篇论文。

用户问题传入Second Me，有三个层级的记忆
- L0是原始数据层，一般是一些非结构化的数据，比如文档、网页、聊天记录等。
- L1是自然语言记忆层，是一些结构化的数据，比如用户的简介、偏好标签、关键语句列表等。
- L2层是AI原生记忆层，通过模型微调把用户的元数据转为模型的参数记忆，模型就是第二个我。

Second Me会去使用Agent Model、Reasoning Model、Human Experts从而提前帮我完成一些任务。

核心：“第二个我”是怎么训练的。

用户的原始数据先经过数据清洗和预处理以及压缩得到结构化的数据，然后由deepseek或openai的大模型合成数据，主要是一些记忆相关QA对，然后过滤一些低质量的问题QA对，通过PEFT框架微调得到SFT Model。

然后通过一些采样策略和对比策略得到偏好数据对，通过DPO微调得到DPO Model。这些所有的步骤都是自动完成的，包括数据清洗和数据合成等，通过deepseek大模型辅助完成。

“第二个我”可以帮你记忆、推荐、检索内容，也可以在你与其他 AI 或服务互动时，替你讲话，帮助你完成任务。
1. 自己回答你的问题；
2. 在其他地方替你发声；
3. 帮你“润色请求”或“吐槽反馈”，让其他服务更懂你。

如果我有足够多关于我的数据，比如声音、视频等，我是不是就可以克隆一个我呢？让我的意识形态永生？



## 模拟评测


### scenario

【2025-7-22】Agent 测试框架 [scenario](scenario.langwatch.ai)，测试设计的 Agent
- 模拟用户行为来进行测试，并且能在对话中进行评估和判断，多轮对话中测试也没问题。
- 可视化展示测评结果

集成到现有项目也很简单，使用 call 方法调用 agent 入口即可。
- 主页 [scenario](scenario.langwatch.ai)
- [scenario](https://github.com/langwatch/scenario)


Scenario is an Agent Testing Framework based on simulations, it can:
- Test real agent behavior by **simulating users** in different scenarios and edge cases
- **Evaluate and judge** at any point of the conversation, powerful **multi-turn** control
- Combine it with any LLM eval framework or custom evals, agnostic by design
- Integrate your Agent by implementing just one `call()` method
- Available in Python, TypeScript and Go 支持 typescript 和 python


安装

```sh
uv add langwatch-scenario pytest
```

使用

```sh
pytest -s tests/test_vegetarian_recipe_agent.py
pytest -s tests/test_vegetarian_recipe_agent.py --debug
```

代码调用
- Save it as tests/test_vegetarian_recipe_agent.py:

```py
import pytest
import scenario
import litellm

scenario.configure(default_model="openai/gpt-4.1")


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_vegetarian_recipe_agent():
    class Agent(scenario.AgentAdapter):
        async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
            return vegetarian_recipe_agent(input.messages)

    # Run a simulation scenario
    result = await scenario.run(
        name="dinner idea",
        description="""
            It's saturday evening, the user is very hungry and tired,
            but have no money to order out, so they are looking for a recipe.
        """,
        agents=[
            Agent(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "Agent should not ask more than two follow-up questions",
                    "Agent should generate a recipe",
                    "Recipe should include a list of ingredients",
                    "Recipe should include step-by-step cooking instructions",
                    "Recipe should be vegetarian and not include any sort of meat",
                ]
            ),
        ],
        set_id="python-examples",
    )

    # Assert for pytest to know whether the test passed
    assert result.success


# Example agent implementation
import litellm


@scenario.cache()
def vegetarian_recipe_agent(messages) -> scenario.AgentReturnTypes:
    response = litellm.completion(
        model="openai/gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": """
                    You are a vegetarian recipe agent.
                    Given the user request, ask AT MOST ONE follow-up question,
                    then provide a complete recipe. Keep your responses concise and focused.
                """,
            },
            *messages,
        ],
    )

    return response.choices[0].message  # type: ignore
```

可视化

Set your LangWatch API key to visualize the scenarios in real-time, as they run, for a much better debugging experience and team collaboration:

```py
LANGWATCH_API_KEY="your-api-key"
```

![](https://github.com/langwatch/scenario/raw/main/assets/langwatch-visualization.webp)


# 结束


