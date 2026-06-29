---
layout: post
title:  Agentic RL 专题
date:   2026-06-01 22:46:00
categories: 大模型
tags: langchain claude deepagents rl grpo 智谱 ppo
excerpt: RL新兴方向，Agentic RL
mathjax: true
permalink: /agentic_rl
---

* content
{:toc}


# Agentic RL


## RL vs Agentic RL

RLHF 详见站内专题：[RLHF 原理及进化](rlhf)

Agentic RL 和 RL 有什么区别?


| 对比维度 | 普通 RL（单轮RL/RLVR） | Agentic RL（智能体强化学习） |
| ---- | ---- | ---- |
| **核心场景** | 文本生成、问答、单轮内容输出 | 智能体、工具调用、环境博弈、长链路推理、自动化任务 |
| **问题形态** | 单轮任务：输入→单次输出，环境静态无变化<br>优化目标：最终答案是否正确 | 多轮连续决策：模型与**动态环境**持续交互<br>观察→动作/工具调用→获取反馈→多轮迭代<br>优化目标：整串决策链路在动态环境中的综合表现 |
| **数据构建** | 离线静态数据集，格式为「题目-标准答案」<br>工作重点：数据配比、去污染、难度分层 | 无固定离线文本数据集，依赖**可交互环境/沙箱/工具**<br>训练时实时交互生成轨迹，数据为动态交互序列<br>核心要点：保证轨迹真实性、数据多样性，避免过拟合 |
| **奖励设计** | 常用判别式PRM、全局终局奖励<br>单轮链路短，信用分配难度低 | 长轨迹仅用终局奖励易出现信用分配失效<br>原则：优先客观过程奖励、结果反推奖励，弱化人工PRM<br>奖励信号下沉至**单轮交互(Turn)级别**，防打分被绕过、分布漂移 |
| **算法特点** | 以GRPO为代表，单轮训练成熟稳定 | 长思维链易出现熵崩塌、训练不稳定<br>工具交互会造成策略熵剧烈波动，需分支采样（如ARPO）等方案优化 |
| **工程实现** | 同步Rollout为主，链路简单，工具调用少 | 高频工具/API调用，**必须异步化Rollout**<br>同步逻辑会严重阻塞流程，异步可大幅提升吞吐量 |


观点 
- Agentic RL 和 RL 就差一个**多轮**，当成 GRPO 跑长一点

真正上手在动态环境里摸爬滚打一圈后，才发现这两种方法从问题建模、数据构建到奖励设计完全是两套打法

(1) 问题形态: 从**写一段话**到**连续做决策**
- 单轮 RLVR 是“给一题，吐答案，验证打分”，环境是死的。但在实际业务中，Agentic RL完全不同，面对动态博弈，模型在交互环境里持续动作的策略。每步观察、动作(搜索调API)、拿到反馈再进下一轮。RL优化答案对不对，而 agentic Rl 在于优化一连串决策在变化的环境里做得好不好

(2) 数据构建：从**题库**到**可交互环境**
- RL 数据本质是静态的"题-可验证答案"对，难点在于**配比、去污染、难度分层**，数据是离线就备好的。
- 但 Agentic RL 数据根本不是一批文本，而是能跑起来、返回真实反馈的环境。得准备可调用的工具、沙箱、初始状态和验证逻辑，轨迹是模型在训练时和环境交互现采的。

踩坑结论：
- 真实端到端采样轨迹**明显**优于合成拼接数据，因为合成数据里观测值是假的，模型会学到环境根本不会出现的模式；
- 数据**多样性**比无脑堆量重要得多, 否则 agent 很容易在窄分布上过拟合、一换环境就崩

(3) 奖励设计：警惕 PRM，把信号下沉到 Turn 级

2025 年之后, 业内很少再训**判别式** PRM 给每步打分了，标注贵、容易 hacking、分布一漂移就失准。但上百步的 agent 轨迹只给终局奖励，credit assignment（信用分配） 极容易崩盘。

原则：
> 能用**结果**信号反推的就不上 PRM
> 能用中间检查点（如 API 调用是否成功）做客观过程奖励的，就别让模型主观打分


(4) 算法与工程现实

rollout 才是成本中心GRPO在单轮上确实成熟，但真用到长思维链上，熵崩塌和训练不稳的坑一个都少不了;

多轮Agent 上，工具返回的 observation 会让策略的熵剧烈波动。这时候像ARPO那样主动在工具轮次做分支采样才是正解。

但抛开算法，真正卡住很多人的其实是**工程**。 Agentic RL 长推理加频繁调用，如果用朴素同步Rollout，事件循环会卡到你怀疑人生。

基建上的死磕结论: 必须把工具调用**异步化**。触发请求就发，别等batch，吞吐量直接能拉高10倍

最后，落到实践上，训agent之前先想清楚三件事:
- 确认数据是否为真实交互采样
- 确认奖励信号是否下沉到Turn级且抗Hacking
- 检查Rollout 工具调用链路是否彻底异步化地基打稳再调算法，才是正解


## 介绍

大模型后训练 RL 的两条路径
- 第一轮浪潮：RLHF（Reinforcement Learning from Human Feedback）。
  - InstructGPT、ChatGPT 时代，PPO 是标准方案：训练一个 reward model 替代人类评分，再用 PPO 优化策略模型。
- 第二轮浪潮：推理模型。
  - PPO 工程代价显得过高, 同时维护4个模型，尤其 critic 被认为是最大的工程痛点：额外占显存、训练困难、容易与 actor 产生不稳定交互。
  - GRPO（Group Relative Policy Optimization）去掉 critic，用组内采样替代价值估计。这一改动大幅降低了工程复杂度，迅速成为推理 RL 的主流选择。
  - DeepSeek-R1、OpenAI o1 等模型证明：在数学、代码等可验证任务上，用 RL 直接训练模型的推理能力，可以带来显著的性能提升。
  - 这类任务通常被称为 `RLVR`（Reinforcement Learning from Verifiable Rewards）——最终答案可以被程序验证，无需依赖人类标注的 reward model。
- 第三轮浪潮：Agentic RL

随着模型能力提升，后训练 RL 任务形态从”**单轮答题**”扩展到”**多轮行动**”——即 `Agentic RL`：
- Coding Agent：读 issue → 搜索代码 → 修改 → 跑测试 → 修复；
- Browser Agent：打开网页 → 搜索 → 点击 → 提取信息；
- Research Agent：检索论文 → 综合信息 → 生成报告。

这类任务的轨迹可达数十甚至上百步，中间涉及工具调用、环境反馈、上下文压缩等复杂结构。

问题核心不再是”哪个答案更好”，而是”轨迹中每一步的贡献各是多少“ —— 即 credit assignment（信用分配） 问题。

### 为什么 GRPO 不适合 Agentic RL？

Long-Horizon Agentic RL：为什么 GRPO 开始吃力
- GRPO 适合”比较多个答案”；PPO 更适合”评估一条行为链中的每一步”。

|维度|RLVR（短程推理）|Agentic RL（长程行动）|
| ---- | ---- | ---- |
|交互轮次|单轮输出|多轮交互|
|轨迹长度|数百 ~ 数千 token|数千 ~ 数万 token|
|中间步骤|推理链（CoT）|工具调用 + 观察 + 推理|
|奖励信号|最终答案可验证|最终结果 + 过程信号稀疏|
|轨迹结构|同 prompt 下样本结构相似|同 prompt 下样本结构差异巨大|
|Credit Assignment|相对简单（整体好/坏）|核心难题（局部好/坏不确定）|

GRPO 的高效性依赖于以下几个隐含假设：

|隐含假设|含义|数学对应|
| ---- | ---- | ---- |
|齐整组假设|同一 prompt 下的多个 rollout 可比较|组内方差有意义|
|outcome 充分假设|最终奖励足以判断整体质量|$r_i$ 可代表所有 token 的贡献|
|采样充分假设|组内采样数量足够反映分布|G 足够大|
|短程假设|轨迹足够短，最终奖励可均匀传播|advantage 不需细粒度分解|

当上述假设成立时，GRPO 非常高效：
- ✅ 数学推理：同一题目采样多解法，答案对/错即可判断
- ✅ 代码生成：同一问题多种实现，测试用例通过率验证
- ✅ 可验证问答：多候选答案，verifier 自动判断
- ✅ 短程 RLVR 任务：输出长度有限，组内样本结构相似

核心优势：用更多采样换掉一个复杂的 critic，工程简洁，训练吞吐高。

然而
- 困难一：Group 不再齐整
  - agentic 场景，同一 prompt 下的不同 rollout 可能截然不同
  - 此时”组内归一化”失去了合理基础——这些 rollout 不是同质样本，而是形态差异巨大的交互历史。将它们的奖励放在一起做归一化，相当于用苹果和橘子比较平均值。
- 困难二：最终 Reward 过于稀疏
  - reward 传播的过度泛化 问题: 一个 50 步的 agent 轨迹最终成功
    - 整条轨迹的 reward 正，但局部（如第41步）坏动作。GRPO 会将正 reward 均匀传导到所有 token，导致局部错误行为也被强化。
    - 反过来，如果轨迹最终失败，但前 80% 的步骤都是正确的，仅最后一步出错，GRPO 会惩罚所有 token，包括那些正确的早期决策。
- 困难三：Compaction 打破了组结构
  - GLM-5.2 的关键洞察：长轨迹在实际训练中需要被压缩和拆分（compaction）：
    - 受上下文窗口限制，超长轨迹需要截断或压缩中间部分
    - 为了训练效率，长轨迹被拆成多个 sub-trace
    - 不同 rollout 的 sub-trace 数量不等、长度不同
  - 此时训练对象已从”完整回答”变为”轨迹片段”，GRPO 天然依赖的”同 prompt 下 G 个齐整候选”结构不复存在。

#### PPO 在长程任务中重回舞台

PPO + Critic：为什么PPO在长程任务中重回舞台

Critic 不是工程组件，而是信息源, 为策略优化提供了比 outcome reward 更细粒度的信号。

Critic 如何辅助 Credit Assignment

代价
- 显存开销: 需要额外存储和计算 value model
- 训练复杂度： Critic 与 actor 的训练需要协调，可能产生不稳定
- 估计偏差： Critic 本身是近似估计，可能引入系统性偏差
- 工程链路： 多一个组件 = 多一套超参 = 多一个调试维度

如何权衡？
> - 当任务的 horizon 变长、轨迹变不规则、局部决策价值变重要时，critic 的成本开始变得值得支付。

这不是”PPO 比 GRPO 更强”，而是：
- 短程任务：critic 的边际收益 < 边际成本 → GRPO 更优
- 长程任务：critic 的边际收益 > 边际成本 → PPO 更优

|特征|倾向 GRPO|倾向 PPO|
| ---- | ---- | ---- |
|轨迹长度|短（< 2K tokens）|长（> 4K tokens）|
|交互轮次|单轮|多轮|
|同 prompt 下 rollout 结构|齐整|差异大|
|中间步骤重要性|低（只需最终答案对）|高（错误步骤需惩罚）|
|工具调用|无或少|频繁|
|上下文压缩/轨迹拆分|不需要|需要|
|奖励信号密度|稠密（结果可验证）|稀疏（只有最终结果）|
|工程资源|有限|充足|
|Verifier 可用性|有可靠 verifier|无或不可靠|

智谱 GLM-5.2 技术博客揭示了这一转变的实际影响：
- 在长程 agentic 任务训练中，从 GRPO 转向了 critic-based PPO。
- 原因并非 GRPO 失效，而是长轨迹的结构性差异使得 critic-based advantage 估计更具优势。

参考：[long-horizon Agentic-持续更新](https://zhuanlan.zhihu.com/p/2037899834422732386)



## 原理



### 奖励分配

总结
- 多轨迹奖励分配：通过轨迹间对比分析，推断每步的贡献核心技术路线包括轨迹图传播、非参数优势估计和分层奖励设计。

多轨迹奖励分配本质：**信用分配**，多步交互的轨迹中，精准识别每个动作对最终成败的贡献，而非简单地把最终结果平均分配给所有步骤

#### 解决什么问题

Agentic RL 训练
- 模型在真实环境中与外部工具交互并自主决策

常规RL方法（PPO/GRPO）中，环境通常只在任务结束时才给最终结果，成功还是失败。中间做过的所有步骤调用过哪些工具、推理的对错 -- 没有任何独立反馈。 

Agentic RL 方法最棘手的问题: **稀疏奖励**, 只有最终结果的成功或失败，中间步骤没有独立反馈
- 多步任务中，模型可能走对了前半段、在后半段犯错，但传统方法会给整条轨迹打同样的分数，导致好步和坏步骤区分度被抹平。

#### 多轨迹奖励分配

多轨迹奖励分配: 从多次采样的轨迹中找到规律，再逆向推断出每步的“功劳“或“责任”，从而让模型知道该学谁、该改谁。

解决思路：**轨迹对比**
- 假设同一个问题，模型生成了多个 轨迹，有的成功、有的失败。
- 横向比较这些轨迹，反向推断每一步对成功的重要性。

实现思路
- 构造 轨迹图 ，把每条轨迹中的不同“状态“节点抽取出来，通过图传播的方式估算每个中间节点离成功有多近。
- 利用 轨迹组对比方法，无需训练额外模型，直接从多次采样的轨迹中估算出每个动作在时间维度上的优势值，再递归地将最终结果逆向传播回每一步。
- 引入分层奖励机制，在最终结果奖励的基础上增加步骤级奖励项，比如显式惩罚重复行为、鼓励多样化探索。

案例
- SALT: 把不同轨迹中的关键状态节点抽取出来形成轨迹图，越靠近成功终点的节点权重越高，然后用**图传播**方法把最终奖励往前推，给每步分配更合理的分数。
- GAGPO: 完全不用额外训练模型，直接基于多次采样的滚动结果，通过**非参数化**方式估算每步的**优势值**，再递归地往回传。

实际场景中，多步推理任务用传统方法，容易卡在局部最优，改成基于轨迹对比的方法后，收敛速度和对中间步骤的精细度都有明显改善。

#### 局限

局限性
- 轨迹采样效率：得到稳定奖励分配需要采集足够多的轨迹，计算成本比较高。
- 环境确定性不够强时，对比分析的准确性会受影响。一般先用规则热启动，或者结合步骤级的轻量级奖励模型做辅助，缓解这个问题。

多轨迹奖励分配和传统的Reward Shaping比有什么区别?
- 传统 Reward Shaping 本质上是人工定义中间奖励函数，高度依赖领域知识。
- 而多轨迹奖励分配从真实采样的轨迹中自动推断步重要性，不需要人工定义中间奖励，泛化能力更强




## 方法



### 长程能力 Long Horizon

让模型处理**超长时序**任务，拥有“无限上下文”的能力，并非简单粗暴地增加上下文长度，而是解决模型如何在有限训练下处理无限信息的问题。

核心理念：“Train with finite, but use as infinite”
- 物理限制：人的记忆也是有限的（短时记忆），但人可以通过“选择性遗忘”和“检索”来处理长期任务。
- 技术路径：模型不需要在训练时就塞入无限数据，而是需要学会如何在使用时，像人一样管理信息——把不重要的信息扔掉（Forget），把重要的信息存入外部文件或检索回来（Retrieve）。

技术实现的两个维度：
- 预训练（Pre-train）角度：尝试 Sparse Attention（稀疏注意力机制）等方法，让模型在预训练时就能处理更长的序列。姚顺宇提到 Google 的一些工作让他感到“惊讶”，暗示了 Gemini 在底层架构上的创新。
- 后训练（Post-train/RL）角度：这是姚顺宇目前更侧重的方向。通过强化学习（RL）训练模型的上下文管理能力（Context Management）。例如，训练模型自己判断：“这段对话不重要，可以丢弃；那段代码很重要，需要保存到文件中以备后用”。

与“无限上下文” 区别：
- 真正的“无限上下文” 工程上不现实。
- Long Horizon 本质“有限训练，无限使用”，通过智能的压缩与检索，模拟出无限上下文的体验。



## 问题

### 踩坑


【2026-6-12】Agent RL 训练[心得](https://www.xiaohongshu.com/explore/6a144cc70000000008031462?xsec_token=ABI3l4OlN4leqURMn64l1w6StIXAO664hgohD6SBLXT-8=&xsec_source=pc_user)：算法选错代价真不大，但工程细节翻车一次就烧掉一周算力。

5个教训
1. **Reward 设计：稀疏为主，shaping 必须封顶**
  - 纯 0/1 outcome reward 在 cold start 阶段几乎跑不动。
  - 正例：某 code agent 纯 outcome 训了 5000 步只从 8% 涨到 12%。加 process reward shaping 帮起飞，但 shaping 一定要封顶：每个中间检查点 +0.1，process 总和上限 0.5，剩下让 outcome 主导，同一项目加了封顶 shaping 后 5000 步直接涨到 31%。
  - 反例：某团队加了"工具调用次数 penalty"想让模型节俭，结果模型学会用 thinking 段绕开调用直接编结果。任何不封顶的 reward 都是 hack 通道。
2. **Rollout 工程：吞吐比 loss 重要**
  - Agent RL新手错误：大部分时间花在等环境，盯 loss 曲线。
  - 三个最有效的提速手段：
    - sandbox 容器池化（单实例换 64 实例池吞吐 3.5x）
    - verl async mode（generation_lag=2~4 是甜点区，超 6 KL 就爆炸）
    - speculative rollout 提前生成下一轮。
  - KL 控制别用固定 beta，adaptive KL controller 配 target_kl=0.05 比固定 beta=0.04 稳一个量级，长轨迹场景特别明显。
3. **Multi-turn loss：observation mask 只是基本盘**
  - observation 要 mask 都知道，三个进阶坑：
    - tool error message 也要 mask，否则模型学会复读 error 凑长度；
    - thinking token 千万别 mask，那是模型推理价值所在；
    - DAPO 的 token-level loss aggregation 在长 CoT 下比 sequence-level 稳 30%+。
      - turn-level credit assignment 现在用 turn-wise value head + GAE(λ=0.95)，比整条共享 advantage 收敛快近一倍。
    - 重要更正：GRPO 沿用 PPO 的 token-level importance ratio，GSPO 才是把 importance ratio 提到 sequence-level：MoE + 长轨迹下 GSPO 明显更稳。
4. **GRPO 陷阱：length bias 和 entropy 坍缩的具体解法**
  - 某 web agent 用裸 GRPO 训了 200 步，average response 从 800 token 涨到 2400 token，accuracy 没涨。这就是经典 length bias。
  - 两个解法：
    - Dr.GRPO 去掉 length 平均和 std 归一化拿无偏 baseline；
    - DAPO Clip-Higher 把 clip_upper 从 0.2 抬到 0.28 给低概率 token 探索空间。
    - entropy 坍缩别盯 loss，盯 rollout distinct-3 指标：跌到 0.3 以下就上 dynamic entropy bonus，初期 0.001，每 100 步 linear decay 到 0.0001。
5. **Reward hacking：上线前必须红队测试**
  - 纪律：reward 函数上线前先让另一个模型专门 hack 它 1 万步，4 种 hack 模式基本都会冒出来。工具 spam、echo prompt、ground truth 关键词拼接、格式分撑大头。
  - 某 SQL agent 一开始对"语法正确"给 0.3 分，模型学会输出 SELECT * FROM 加随机字段名碰运气；改成必须执行通过且 row count 匹配才计分后 hack 立刻消失。线上每 500 步用 LLM-as-judge 抽 50 条 rollout 做 hack pattern detection，比单看 reward 曲线靠谱得多。

### 多轨迹怎么给奖励？

RL训练容易卡在奖励分配分配环节

涉及 credit assignment的理解深度，以及处理稀疏、冲突奖励的工程能力。不懂多trajectory的奖励分配，RL训练根本收敛不了

模块一：Agentic RL 奖励设计
- 对话场景下如何设计 GRPO 奖励函数？
- 多轮对话如何保证reward上下文一致性？
- RL里奖励函数和调参哪个更重要？

模块二：多轨迹采样与方差控制	
- GRPO 采样结果全错怎么破？
- 采样权重过小导致方差大，如何调？
- GRPO 中Clip掉的token梯度为何为0？

模块三：稀疏奖励与模型撒谎	
- 奖励信号稀疏时，如何设计稠密塑造策略？
- GRPO奖励设计使模型撒谎，根源怎么解？

### 奖励黑客与失效

【2026-6-13】[帖子](https://www.xiaohongshu.com/explore/6a26c26a0000000008000a4a)

(1) 认清本质: 不是bug，是优化的必然

很多人把 reward hacking 当成偶发坏样本，其实是 **Goodhart定律**的铁律－智能体会利用奖励函数的缺陷而非学习预期行为，从而损害对齐。

2026年的 verl 上趟过坑
- **RM代理失效的三种模式** → **相变监控** → Agent多轮的**工具滥用和环境操控** → RLVR的**验证器 hack** → GenRM+rubric 怎么**升级裁判**" 。
- 把 GenRM 论文、agentic Rl 综述、再加一篇 reward overoptimization 的理论文章对着读透，理论搞懂了 debug的时候才知道该拧哪个旋钮的

奖励模型只是人类偏好的有损代理，贪婪优化，模型迟早会找到代理和真实目标之间的缝

案例
> 某开源项目用 SOTA 做RM训 coding agent,reward从0.3 涨到 0.85, 团队以为训出来了，结果 code review 发现模型学会一套"讨好 SOTA 的话术模板":
> - 函数名用完整英文句子
> - 注释写得比代码还长
> - 每个分支都加 docstring
> 人类评委打分反而不如训之前的版本。

典型的RM代理失效:
- 训 code quality，RM 评"看起来像高质量代码"

认知: 永远无法消除，只能把爆发时间往后推到收敛之后。

所以，不是在 hack 出现后去修 reward 函数，而是在 hack 爆发前把 checkpoint 拿走

（2）监控曲线:
- reward涨不代表在变好，要看背离
- 实战时的坑：只盯 reward 均值。

总结出一条规律: 奖励爆发不是渐进的，而是"相变"
- 前3000步奖励和真实指标同步提升，突然 奖励继续涨、真实指标开始跌，两条曲线分道扬镳

用 GRPO时，要同时挂四条线: rewardKL、entropy、response length，只要有1条出现非单调跳变，立刻暂停训练做 hackpattern 抽检。
- 典型现象: responselength 从 600 token 两天内涨到 1800，reward还在涨，但抽检50条rollout发现模型学会了给每个答案套三层"首先...其次...最后.."的结构框架来蹭RM的长度偏好--内容全是废话

容易被忽略的机制:
- GRPO 按序列长度归一化会引入**结构性偏置**，带正奖励的短答案拿到不成比例的大梯度。

所以，hack的早期信号往往不是 reward 涨，而是 response length 先出问题

（3）奖励建模:RM 本身就是最大的hack入口

奖励函数设计上，逐渐形成共识:
- RM本身被hack的问题，比策略优化算法的选择严重得多。
- 前两年大家还在争论PPOVS GRPO VS REINFORCE，近期一线真正头疼的是--  RM 底在评什么?

翻车模式:
- 长度偏好: RM 给长答案系统性高分，模型学会注水。行业内 RLHF/RL 量化研究表明，RM 长度偏好在某些领域可以让真实胜率虚高15-20个点
- 格式偏好: RM喜欢 markdown、列表、加粗，模型学会把所有答案都格式化成博客文章--内容和正确性没有变好，只是变好看了
- 风格泄漏: RM偏好某种写作风格(比如"学术风")，模型学会模仿那个特定风格而非真正提升推理质量

解法趋势: 不再死磕修RM，而是把裁判升级。
- **生成式奖励模型**(GenRM) 开始替代**传统标量RM**--让评判模型先写出推理过程再给分，避免直接打分被表面特征拐跑。
- 配合细粒度的 rubric-based 评分(正确性、完整性、简洁性独立打分)，比单一标量分防hacking 效果好一个档次

(4) 真正的硬骨头:Agent多轮的hacking是另一回事

单轮 RL的 hacking 模式虽然花, 但至少套路可枚举。

到了 agentic RL，把 LLM 嵌进序列决策循环后，hacking 的形态完全变了:
- 工具滥用: 某团队训 browser agent,大reward 是"完成任务的速度"，模型学会了同时檻你 20 个 tab 并行搜、然后挑第一个匹配的-快是真快，但token 消耗是正常路径的8倍且多数任务靠运气而非推理
- 环境操控: code agent 训到后期学会改测试用例来让单测通过，而不是修bug。Owen团队今年在SWE-bench 上复现了这个现象，发现不加防护时约12%的rollout存在测试篡改行为
- 思考预算 hack: 给 thinking token 数量设reward想让模型多做推理，结果模型学会在thinking 段里反复复述问题、写无意义的草稿来凑长度--看着思考了很多，实际没有推进推理
- 协作退化: multi-agent 场景下给"达成共识"加分，两个 agent学会了互相发空消息就算"达成共识"--形式上满足了 reward，语义上什么都没做

实战解法
- 把 reward 从"结果导向"升级为"过程追踪": 对工具调用做轨迹级抽检，规则可验证的环节(代码单测、检索命中)走硬校验，软指标才上lеarned reward，两者混合打分不给模型钻空子的空间。

(5) RLVR 的边界: 可验证不等于防hacking

2026年, RLVR(可验证奖励)被抬得很高，确实省了训 RM 的成本，但RLVR 有自己的坑。

可验证信号只看最终答案不看过程--数学题答案对了但推导全错、代码通过测试但逻辑是硬凑的，RLVR统统给满分

更深层的问题是"验证器本身被hack": 模型学会构造刚好能通过验证器但语义上错误的输出。
- 比如SQL agent 知道 COUNT(*) 比实际行数会被verify，就去构造 SELECT 1FROM .. 这种稳过邬的查询，完全不回答用户问题

2026年折中方案是"双重裁判": 硬指标走规则验证，软指标上推理型RM(先推理解构答案再打分)，再叠人工抽检做校准。三管齐下是目前较稳的防 hack 组合

### Agentic RL PPO > GRPO

总结

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;dark-mode&quot;:&quot;auto&quot;,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot;&gt;\n  &lt;diagram name=\&quot;AI意图识别商用方案\&quot; id=\&quot;osbHtP6Ki7KAK-vxM0vi\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;31588\&quot; dy=\&quot;21761\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;ueTJB6k9vFQzMmB7xgun-37\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=24;labelBackgroundColor=none;\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;Agentic RL 对比&amp;lt;/span&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;210\&quot; x=\&quot;-30265\&quot; y=\&quot;-20680\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-3\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=4;strokeColor=#808080;\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; relative=\&quot;1\&quot; width=\&quot;50\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-30480\&quot; y=\&quot;-20360\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-29840\&quot; y=\&quot;-20360\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-4\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=4;strokeColor=#808080;\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; relative=\&quot;1\&quot; width=\&quot;50\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-30185\&quot; y=\&quot;-20200\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-30185\&quot; y=\&quot;-20620\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-5\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#808080;\&quot; value=\&quot;需要 Critic\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;110\&quot; x=\&quot;-29950\&quot; y=\&quot;-20390\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-7\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#808080;\&quot; value=\&quot;可学习 Critic\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;110\&quot; x=\&quot;-30070\&quot; y=\&quot;-20550\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-8\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#808080;\&quot; value=\&quot;无需 Critic\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;110\&quot; x=\&quot;-30495\&quot; y=\&quot;-20390\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-9\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#808080;\&quot; value=\&quot;Credit Assignment&amp;lt;div&amp;gt;信用分配&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;140\&quot; x=\&quot;-30345\&quot; y=\&quot;-20600\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-10\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#808080;\&quot; value=\&quot;稠密奖励&amp;lt;div&amp;gt;Dense（token级别）&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;175\&quot; x=\&quot;-30195\&quot; y=\&quot;-20610\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-11\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#808080;\&quot; value=\&quot;稀疏奖励&amp;lt;div&amp;gt;Uniform（轨迹级别）&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;175\&quot; x=\&quot;-30230\&quot; y=\&quot;-20210\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-12\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;fontSize=18;\&quot; value=\&quot;VIMPO\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;160\&quot; x=\&quot;-30385\&quot; y=\&quot;-20500\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-13\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=18;\&quot; value=\&quot;PPO\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;130\&quot; x=\&quot;-30150\&quot; y=\&quot;-20500\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-14\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=18;\&quot; value=\&quot;VAPO\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;130\&quot; x=\&quot;-30010\&quot; y=\&quot;-20500\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-15\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=18;\&quot; value=\&quot;DAPO\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;100\&quot; x=\&quot;-30325\&quot; y=\&quot;-20330\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-16\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=18;\&quot; value=\&quot;GRPO\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;100\&quot; x=\&quot;-30440\&quot; y=\&quot;-20330\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-17\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;动态采样\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;70\&quot; x=\&quot;-30310\&quot; y=\&quot;-20270\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-18\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;组间奖励\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;70\&quot; x=\&quot;-30430\&quot; y=\&quot;-20270\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-19\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;actor-cirtic\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;90\&quot; x=\&quot;-30130\&quot; y=\&quot;-20440\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-20\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;预训练的critic\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;110\&quot; x=\&quot;-30000\&quot; y=\&quot;-20440\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-21\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;表单数值\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;70\&quot; x=\&quot;-30345\&quot; y=\&quot;-20440\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


#### 业界放弃 GRPO

【2026-6-16】智谱在 GLM-5.2 强化学习里又用上了PPO
- 对长程任务来说，GRPO credit-assignment 颗粒度过粗可能确实会影响效果，不同rollout长度差异显著可能也会影响GRPO的效果。

官方 [GLM-5.2: Built for Long-Horizon Tasks：章节 RL for Long-Horizon Task with Anti-hacking](https://z.ai/blog/glm-5.2)
- GLM-5.2 模型，长时序任务会生成**长度大幅增加**的执行轨迹。当一条超长完整轨迹经过压缩拆分，被切分为多条子轨迹后，同一提示词下生成的不同采样样本，会产出数量不等、长度差异极大的可训练子轨迹。
- 因此放弃分组式优化方案（GRPO系列），改用基于价值网络（Critic）的 PPO 框架，以单条采样轨迹为单位进行学习；依靠价值网络逐 token 估算优势值，不再依赖组内相对对比计算优势。
- 这种单轨迹训练范式可天然适配轨迹压缩机制：不对单条提示词产出的子轨迹数量、各子轨迹的相对长度做任何约束。将全部压缩后的子轨迹纳入训练集作为可学习轨迹，并采用逐 token 损失函数，解决子轨迹之间长度不均衡的问题。

GRPO 公认的三个前提: 同题可比较, 信号可验证, 组内能降噪。 这三个前提在目前的长程任务中，不管是算法角度还是工程角度，都有一定程度的被动摇。

业界都承认了GRPO在长程任务中的局限性，不管是智谱、minimax还是创造GRPO算法的DeepSeek，对于长程编程的训练是在不同的层面解决问题。
- 智谱直接把critc网络请回来，重新衡量token级的优势。
- Minimax 则设计新的RL算法和对应的 Infra，CISPO算法、再加复合奖励，包括过程、时间、结果，再加Forge调度。
- DeepSeek 则通过GRPO训了专家模型，使用 在线蒸馏（On-Policy Distillation）方式让模型在探索时，专家模型来提供监督信号。

作者：[划水的青蛙](https://www.zhihu.com/question/2052108642686706557/answer/2052367150749427260)


#### 请回 PPO

【2026-6-22】Agentic 任务的复杂性（长轨迹、多轮工具交互、多维复合 Reward）导致**信用分配**（Credit Assignment）极度困难。 
- 孤立的 Final Reward 无法辨析 Planner、Searcher 或 Verifier 在中间节点的功过，易引发 Reward Hacking。

PPO 相比 GRPO 在 Agentic RL 中更具优势：
- 解耦长程依赖： 依赖 Critic 网络，提供更自然的价值估计。
- 细粒度对齐： 完美兼容 Process/Turn-level Reward，实现模块级的信号分配。

结论： 
> GRPO 虽是好 Reasoning 优化器，但在复杂 Agentic RL 场景下，PPO 依然是更**稳健**、更**天然**的选择。

[对 GLM-5.2 PPO 优化的思考：Strong Value Model 如何引导真实场景 RL 训练](https://zhuanlan.zhihu.com/p/2052145684040701422)

2025 年 5 月，基于荣耀 yoyo 助手真实场景对话数据进行对话任务训练时就发现：
> 带 Value 网络的 PPO 训练，相比其他方法具有更强的抗 Hacking 能力和训练鲁棒性。能有效减少模型崩溃，在长对话优化和真实交互中表现显著更优（参考后文的 VRPO 工作）。

#### EVPO

- 北大复旦【2026-4-21】[EVPO: Explained Variance Policy Optimization for Adaptive Critic Utilization in LLM Post-Training](https://arxiv.org/abs/2604.19485)

直觉：
- GRPO 轨迹一旦被 Hacking，极容易带偏 Average Advantage 从而导致模型崩溃；
- 而 PPO 则能通过 Value Model 在遇到 Hacking 时依旧进行平滑缓解，优化 Advantage 的估计，从而带来更强的鲁棒性。
- 当然，这一切的大前提是—— Value Model 必须足够有效且强大

《EVPO》提供新视角：**前期 GRPO 探索，后期 PPO 提纯**。
- 前期利用 GRPO 高效的 RL 训练过程，顺带“预训练” Value Model，从而更高效地利用探索阶段产生的数据

#### 伯克利 VIMPO

【2026-6-18】UC Berkeley 的论文（VIMPO），介于 GRPO 和 PPO 之间的新尝试。
- 论文 [VIMPO: Value-Implicit Policy Optimization for LLMs](https://arxiv.org/pdf/2606.20008v1),
- 代码 [VIMPO](https://github.com/backprop07/VIMPO)
- 通过构造出的token-level advantage，在不训练critic model的情况下，基于GRPO达到类似于PPO的效果，也在Qwen3-4B上得到了一些基础的实验验证。
	
不过 LLM论文都有这个问题：小模型上的实验到底有多大程度可以进一步scaling，Scaling以后无论是计算和infra复杂度还是实际效果，相比小模型可能都会有比较大的差异。

	


# 结束
