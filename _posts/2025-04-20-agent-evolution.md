---
layout: post
title:  LLM/Agent 自我进化
date:   2025-04-20 11:30:00
categories: 大模型
tags: Agent 自学习 进化 自动化 训练
excerpt: LLM/Agent 如何实现自我进化？
mathjax: true
permalink: /agent_evolution
---

* content
{:toc}

# LLM/Agent 自我进化


## 静态问题

Agent 与真实世界互动时，问题：
- 世界是动态：新知识、新事件、新梗层出不穷。一个知识停留在 2023 年的 AI，无法理解 2024 年的最新动态。
- 任务是开放：真实世界的任务千变万化，没有固定的「题库」。AI 需要具备处理未知问题的能力。
- 工具是变化：新的软件、API 和网站不断涌现。AI 需要学会使用新工具，甚至创造新工具。
- 用户是个性：每个人都有自己的偏好和习惯。AI 需要通过与用户的互动，不断适应和学习，提供个性化服务。

「静态」的 AI 在这样动态、开放的环境中，就像一个拿着旧地图的航海家，注定会迷航。

因此，AI 范式正在经历一场至关重要的转变：从追求模型的「规模」（Scale）转向追求智能体的「适应性」（Adaptivity）。

发展路径：
- 从`基础 LLM`，到能执行任务的`基础智能体`（Foundation Agents），再到能够持续学习和适应的`自进化智能体`（Self-Evolving Agents），并最终指向理论上的`人工超级智能`（Artificial Super Intelligence, ASI）。
- ![](https://pic2.zhimg.com/v2-05370ee6d90f1cc00d8b4a8c59e8ca2b_1440w.jpg)


自学习，不断进化

## 综述 

What-When-How 框架系统地解构和理解所有关于「自进化」的研究。三个维度分别是：
- 进化什么？（What to Evolve?）：智能体作为一个系统，它的哪些部分可以被改进？模型、上下文、工具、架构
- 何时进化？（When to Evolve?）：进化的过程发生在任务的哪个阶段？
  - 「任务中进化」追求的是灵活性和即时响应
  - 「任务间进化」追求的是系统性提升和长期成长。
  - 一个优秀的自进化智能体，需要兼具这两种能力。
- 如何进化？（How to Evolve?）：驱动进化的具体方法和信号是什么？
  - 三大类进化引擎：奖励、模仿和演化

![](https://pic4.zhimg.com/v2-3d0bdc6e5d1c69f1ce9a3c0b42804e45_1440w.jpg)

【2025-7-30】普林斯顿、清华、CMU等 [综述：AI 如何实现自我进化？]()

截止2025年7月,「自进化智能体」（Self-Evolving Agents）领域的进展。
- 当前，尽管大语言模型（LLM）能力强大，但本质上「静态」，一旦训练完成，其内部参数就不会再改变。
- 这在需要实时适应新知识、新任务的动态世界中成了一个巨大的瓶颈。

与环境互动、从经验中**学习并持续自我完善**的智能体。

理论框架，围绕三个核心问题展开：**进化什么**（What）、**何时进化**（When） 以及 **如何进化**（How）。
- 论文： [A Survey of Self-Evolving Agents: On Path to Artificial Super Intelligence](https://arxiv.org/pdf/2507.21046)
- github [Self-Evolving-Agents](https://github.com/CharlesQ9/Self-Evolving-Agents)


## 进化案例

### 【2025-2-18】港大 AutoAgent

【2025-2-18】 [港大开源全自动且高度自我进化的零代码AI Agent框架：AutoAgent](https://mp.weixin.qq.com/s/CQ28CRhCLN3wtdcMCWEzug)

[AutoAgent](https://github.com/HKUDS/AutoAgent) 是**全自动**且**高度自我进化**的框架，用户仅需自然语言即可创建并部署 LLM Agent。
- 论文 [AutoAgent: Fully-Automated and Zero-Code LLM Agent Framework](https://arxiv.org/pdf/2502.05957)

核心特性
- 🏆 GAIA 基准测试冠军
  - AutoAgent 在开源方法中排名 #1，性能媲美 OpenAI 的 `Deep Research`。
- 📚 Agentic-RAG，内置**自管理**向量数据库
  - AutoAgent 配备原生自管理向量数据库，超越 LangChain 等行业领先方案。
- ✨ 轻松创建 Agent 和工作流
  - AutoAgent 利用自然语言轻松构建可直接使用的工具、Agent 和工作流 —— 无需编码。
- 🌐 广泛兼容 LLM
  - AutoAgent 无缝集成多种 LLM（如 OpenAI、Anthropic、DeepSeek、vLLM、Grok、Huggingface...）。
- 🔀 灵活交互模式
  - 支持函数调用（Function-Calling） 和 ReAct 交互模式。
- 🤖 动态、可扩展、轻量级
  - AutoAgent 是你的个人 AI 助手，具备动态、可扩展、可定制、轻量级的特性。

使用方法  
1. 用户模式（SOTA 🏆 对标 OpenAI Deep Research）
  - AutoAgent 内置多智能体（Agent）系统，你可以在启动页面选择用户模式直接使用。这个多智能体系统是一个通用 AI 助手，具备与 OpenAI Deep Research 相同的功能，并在 GAIA 基准测试中实现了可媲美的性能。
  - 🚀 高性能：基于 Claude 3.5 实现 Deep Research 级别的表现，而非 OpenAI 的 o3 模型。
  - 🔄 模型灵活性：兼容任何 LLM（包括 DeepSeek-R1、Grok、Gemini 等）。
  - 💰 高性价比：开源替代方案，无需支付 Deep Research $200/月 的订阅费用。
  - 🎯 用户友好：提供易部署 CLI 界面，交互流畅无阻。
  - 📁 文件支持：支持文件上传，实现更强的数据交互能力。
  - 🎥 Deep Research（即用户模式）
2. Agent 编辑器（无工作流的 Agent 创建）
  - AutoAgent 最具特色的功能是自然语言定制能力。不同于其他 Agent 框架，AutoAgent 允许你仅通过自然语言创建工具、Agent 和工作流。只需选择 Agent 编辑器或工作流编辑器模式，即可开启对话式构建 Agent 之旅。
3. 工作流编辑器（使用工作流创建 Agent）
  - 通过工作流编辑器模式，使用自然语言描述创建代理工作流，如下图所示。（提示：此模式暂时不支持工具创建。）

### 【2025-3-8】AppAgentX 进化

【2025-3-8】西湖大学 推出自学习能力 Agent
- 项目 [AppAgentX: Evolving GUI Agents as Proficient Smartphone Users](https://appagentx.github.io/)

进化框架，提高运营效率，同时保持智能和灵活性

每个步骤，Agent 都会
- 捕获设备的**当前屏幕**并分析，从预定义的作空间中选择合适的作。
- 执行所选作，与 GUI 交互。
- 任务执行轨迹被分解为多个**重叠**三元组。基于这些三元组，生成LLM页面和 UI 元素的功能描述。
- 将合并重复生成的页面描述。
- 整个交互历史记录使用节点链进行记录。

进化机制可识别**重复序列**并创建高级快捷方式，从而显著减少常见任务所需的步骤数和推理。

AppAgentX 在多个基准任务中的效率和成功率都明显优于现有方法。
- 与 GPT-4o 相比, AppAgentX 执行步数、耗时、token花销大幅降低，而准确率最高


### 【2025-8-5】CMU SQLM


大语言模型的训练很大程度上仍依赖人工整理**数据集**，堪称费时费力。

为了减轻这一负担，研究人员开发了用于强化学习的**无监督奖励函数**，然而，这些函数仍然依赖于预先提供的**高质量输入提示**。

因此，问题难点从“生成答案”转移到了“生成高质量问题”。

当前方法的关键不足：
- 缺乏可扩展且自我维持的流程，能够在无人干预的情况下自动生成有意义的问题和答案。

【2025-8-5】[无需外部数据！AI自问自答实现推理能力进化](https://mp.weixin.qq.com/s/Q3fc95LXM3PuytdEBnUCSA)

卡内基梅隆大学提出新框架`SQLM`——一种无需外部数据的自我提问模型。
- 论文 [SELF-QUESTIONING LANGUAGE MODELS](https://www.alphaxiv.org/abs/2508.03682v1)
- 该框架包含`提问者`（proposer）和`解答者`（solver）两个角色，提问者生成与给定主题相关的问题，解答者旨在解决问题。
- SQLM框架，非对称的自我博弈框架

堪称：带 RL 的 GAN

实验结果显示
- SQLM 将 Qwen2.5-3B-Instruct 在算术任务上的准确率提高了**14%**，在代数任务上提高了16%；在编程任务上的准确率提高了7%。

此外，上表还显示出SQLM显著优于格式奖励基线（用于稳定训练和规范输出格式的参考值），表明推理能力的真正提升。


### 【2025-8-7】腾讯 R-Zero


【2025-8-7】腾讯AI Lab（西雅图），[腾讯AI Lab推出「零数据自进化」推理LLM]()
- 论文标题：[R-Zero: Self-Evolving Reasoning LLM from Zero Data](https://arxiv.org/pdf/2508.05004)
- 项目主页 [R-Zero: Self-Evolving Reasoning LLM from Zero Data](https://chengsong-huang.github.io/R-Zero.github.io/)
- Code: [R-Zero](https://github.com/Chengsong-Huang/R-Zero).

自我进化的大语言模型（LLM）通过自主生成、优化并从自身经验中学习，为实现超级智能提供了可扩展的途径。

然而，当前训练此类模型的现有方法仍高度依赖于海量的人工标注任务和标签，通常通过微调或强化学习实现，这构成了推动人工智能系统超越人类智能能力的根本瓶颈。

为克服这一限制，腾讯AI Lab 团队推出了一个完全自主、能够从零开始生成自我训练数据的框架——`R-Zero`。

从单个基础 LLM 出发，`R-Zero` 初始化两个具有不同角色且独立运行的模型：`挑战者`（Challenger）和`解决者`（Solver）。

![](https://chengsong-huang.github.io/R-Zero.github.io/static/images/method.png)

这两个模型分别进行优化，并通过相互作用实现协同进化：
- `挑战者`因提出接近解决者能力边界的任务而获得奖励，而`解决者`则因解决挑战者提出的日益复杂的任务而获得奖励。

![](https://chengsong-huang.github.io/R-Zero.github.io/static/images/abstract.png)

这一过程产生了无需预先存在的任务和标签的针对性、自我改进的课程。



#### 效果
	
实验结果表明
- R-Zero 显著提升了不同基础 LLM 的推理能力，例如在数学推理基准测试中使 Qwen3-4B-Base 的性能提升 6.49，在通用领域推理基准测试中提升 7.54。


### 【2025-11-20】斯坦福 agent0 

【2025-11-20】斯坦福 agent0 
- 论文：[Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning](https://arxiv.org/abs/2511.16043)
- 代码 [Agent0](https://github.com/aiming-lab/Agent0)

已有自我进化框架：受限于模型能力和单轮交互，难以实现包含工具使用、动态推理的复杂模式进化

Agent0 全自主的智能体进化框架，通过多步协同进化、无缝工具集成，无需外部数据即可培育出高性能智能体

Agent0 让两个基于相同 LLM 初始化的智能体形成共生竞争关系：
- 一个是课程智能体，负责提出难度逐步提升的前沿任务；
- 另一个是执行智能体，专注于学习解决这些任务。

框架集成外部工具以增强执行智能体的问题解决能力，反过来促使课程智能体设计更复杂、且能适配工具使用的任务。

通过这一迭代过程，Agent0 构建起自我强化的循环，持续生成高质量的训练课程。


核心思想：
- Agent0 从同一个基础LLM创建两个智能体，并迫使它们进入竞争性的反馈循环。
- 一个发明任务，一个试图生存。这种持续的推拉产生的前沿难度问题是任何静态数据集都无法比拟的。

解决了自进化智能体的最大失败模式：停滞。

大多数智能体只生成比他们当前水平稍微难一点的问题。Agent0使用不确定性、采样答案之间的分歧和工具调用频率来检测执行智能体的弱点。

<img width="894" height="471" alt="image" src="https://github.com/user-attachments/assets/39c41bb2-45b7-41be-9d5b-55518f54c0ed" />

<img width="901" height="393" alt="image" src="https://github.com/user-attachments/assets/b50b3dce-2f66-48d7-a3ae-8752fbb230f6" />


实证结果表明
- Agent0 显著提升了模型的推理能力：在数学推理基准测试中，Qwen3-8B-Base 模型性能提升 18%；在通用推理基准测试中，性能提升 24%。

### 【2025-11-13】AgentEvolver

【2025-11-13】通义实验室开源新框架 AgentEvolver，通过「自我提问」「自我导航」「自我归因」三大机制，系统性解决智能体强化学习中的任务稀缺、探索低效和样本利用率低等瓶颈。
- 技术报告 [AgentEvolver: Towards Efficient Self-Evolving Agent System](https://arxiv.org/pdf/2511.10395)
- github [AgentEvolver](https://github.com/modelscope/AgentEvolver)

大多数智能体系统仍停留在“按照指令完成任务”的层面——**缺乏持续学习、适应变化**的能力。

三大瓶颈：
- 任务构建成本高：新的环境往往需要重新定义任务与目标，人工成本高、覆盖面有限。
- 探索效率低：强化学习依赖大量交互采样，训练成本与时间消耗巨大。
- 样本利用不充分：奖励稀疏且模糊，模型难以判断哪些中间步骤真正起作用。

AgentEvolver 推动智能体从“被训练”迈向“自进化”的新范式


AgentEvolver 核心是由三大机制驱动的动态学习闭环。让智能体不再是被动执行任务的“工具”，而是一个能不断学习、总结、改进的动态系统

三大机制的协同作用，驱动智能体在复杂环境中持续优化和演化：
- 自我任务生成（Self-Questioning）：自主生成探索任务，摆脱对人工数据集的依赖。
- 自我经验导航（Self-Navigating）：高效复用历史经验，提升探索效率。
- 自我反思归因（Self-Attributing）：精细评估步骤级奖励，提升样本利用率。

<img width="1080" height="646" alt="image" src="https://github.com/user-attachments/assets/162cbec1-891b-49e1-8980-2cbecee53e77" />

自我任务生成

<img width="1080" height="437" alt="image" src="https://github.com/user-attachments/assets/a5aeec62-887f-446d-afaf-d70d2de0bc5f" />

### 【2026-3-19】LSE

LLM 部署后遇到新任务时，最常见的做法是"自我反思"——让模型审视之前的失败并修改自己的 prompt。但问题：没人教过模型怎么做"自我进化"这件事。
- 所有现有方法（TextGrad、GEPA 等）都依赖模型天生的推理能力来做 prompt 优化，从未专门训练过这项技能。

问题
- 从未被专门训练
- 线性路径锁死
- 奖励信号含噪

Snowflake 团队提出 `LSE`（Learning to Self-Evolve）框架：用强化学习训练 4B 参数的"自进化策略"，专门学习**如何改进上下文**。
- 配合 UCB 树搜索防止进化路径塌缩，LSE 训练的 Qwen3-4B 在 Text-to-SQL（BIRD）上以 67.3% 超越 GPT-5 的 65.2%，在 MMLU-Redux 上以 73.3% 超过 GPT-5 的 72.5%。平均提升 +6.7 个百分点。 LSE 学到的不是针对特定模型的技巧，而是一种通用的"如何从反馈中改进上下文"的元能力
- 更关键: 训练好的自进化策略可以零样本迁移到完全不同的模型上，为其提供 +6.7% 的提升。
- 论文 [Learning to Self-Evolve](https://arxiv.org/pdf/2603.18620)
- 解读 [4B 小模型击败 GPT-5：Learning to Self-Evolve 用强化学习教会 LLM 在测试时自我进化](https://zhuanlan.zhihu.com/p/2019744547450697438)


LSE 框架总览。
- 左侧为测试时的树引导自进化循环——UCB 算法从进化树中选择节点，Action Model 在新批次上执行后生成性能摘要，Self-Evolving Policy 据此提出新上下文。
- 右侧为训练流程——用改进量（编辑后性能 - 编辑前性能）作为 RL 奖励信号。

![](https://picx.zhimg.com/v2-afe24cf97a6a6c6e925c545d411ee6e5_1440w.jpg)



# 结束
