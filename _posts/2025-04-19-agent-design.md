---
layout: post
title:  Agent 智能体设计
date:   2025-04-19 11:30:00
categories: 大模型
tags: Agent 多模态 agi 自学习 进化 
excerpt: LLM Agent 落地时，如何抉择、如何设计架构？
mathjax: true
permalink: /agent_design
---

* content
{:toc}


# Agent 智能体设计


## Agent 选型

Agent 落地路线图



## Agent 分析


当前模型 agent 的问题和局限性。
- **记忆召回**问题。如果只是做简单的 embedding 相似性召回，很容易发现召回的结果不是很好。这里应该也有不少可以改进的空间，例如前面提到的 Generative Agents 里对于记忆的更细致的处理，LlamaIndex 中对于 index 结构的设计也有很多可以选择与调优的地方。
- **错误累积**问题。网上给出的很多例子应该都是做了 cherry-picking 的，实际上模型总体表现并没有那么惊艳，反而经常在前面一些步骤就出现了偏差，然后逐渐越跑越远……这里一个很重要的问题可能还是任务拆解执行，外部工具利用等方面的高质量训练数据相对匮乏。这应该也是 OpenAI 为啥要自己来做 plugin 体系的原因之一。
- **探索效率低**。对于很多简单的场景，目前通过模型 agent 来自行探索并完成整个解决过程还是比较繁琐耗时，agent 也很容易把问题复杂化。考虑到 LLM 调用的成本，要在实际场景落地使用也还需要在这方面做不少优化。一种方式可能是像 AutoGPT 那样可以中途引入人工的判断干预和反馈输入。
- **任务终止与结果验证**。在一些开放性问题或者无法通过明确的评估方式来判断结果的场景下，模型 agent 的工作如何终止也是一个挑战。这也回到了前面提到的，执行 task 相关的数据收集与模型训练以及强化学习的应用或许可以帮助解决这个问题。

【2025-4-16】[人人都在鼓吹的Agent,为什么我看到的全部是缺点](https://zhuanlan.zhihu.com/p/1895612467310208061)

**工具调用**可靠性低
- 即使简单API调用也常因格式错误、参数不匹配或上下文误解而失败。例如，模型可能生成无效的JSON格式或忽略关键参数。
- 工具选择错误率高，尤其在面对大量工具时难以有效组合或筛选。
- 自然语言接口的稳定性不足，导致工具调用行为不一致。

记忆与上下文限制
- 有限上下文窗口（即使200k tokens）制约历史信息访问与自我反思能力。
- 分层记忆架构尚未成熟，短期、长期记忆整合困难

系统集成与成本问题
- 缺乏标准化接口，需为每个部署定制集成层，开发成本高昂。
- 大模型推理成本高，多步任务导致响应延迟显著。
- 计算资源需求大，大规模部署面临内存和算力瓶颈

人机交互性能不足
- 复杂软件（如办公套件）操作成功率仅40%，协作平台沟通成功率低至21.5%。
- 多模态感知能力弱，缺乏对物理环境（如触觉、痛觉）的反馈机制

**多步**任务执行缺陷
- 在任务执行过程中，智能体可能选择了错误的动作序列，导致偏离正确轨迹
- 智能体需要回顾并修正之前的错误动作，以完成任务
- Agent 也容易陷入**局部循环**（Stuck into Loops）,反复执行相同动作，无法探索新可能性
- 复合**错误积累**显著：若单步成功率为90%，10步任务成功率将骤降至35%。
- **上下文管理**能力弱，长序列任务中难以维持连贯理解。
- Agent 难以从错误的长轨迹中恢复（Difficult to recovery in long trajectory）
- 缺乏动态调整能力，错误恢复机制不完善，无法像人类一样从失败中学习



## Agent 设计模式

大模型落地两种模式:`Copilot`模式和`Agent`模式。
- `Copilot` 模式:人机交互以**人类为主导**，AI只是作为助手，部分流程由AI通过对话交互或SDK方式完成。
  - AI Copilot 可能在特定领域（如编程、写作、驾驶等）提供帮助，通过与人类的交互来提高效率和创造力。AI Copilot 可能更多地依赖于人类的输入和指导，而不是完全自主地完成任务。
- `Agent` 模式:人类作为人工智能导师/教练的角色，设计目标并监督结果，大模型充分发挥自身推理能力，实现推理规划，并调用合适的工具和接口，实现行动执行，最后给予结果反馈。

agent和copilot的区别主要体现在:**交互方式**、**任务执行**和**独立性**等方面。
- **交互方式**:
  - copilot 要用户给出清晰明确的prompt，即需要用户具体详细地描述任务或问题，copilot才能根据prompt给出有用的回答。
  - 而大模型agent交互方式更为灵活，根据给定目标自主思考并做出行动，无需用户给出过于详细明确的prompt。
- **任务执行**:
  - copilot在接收到清晰明确的prompt后，可以协助完成一些任务，但它的执行能力相对有限。
  - 而大模型agent则可以根据目标自主规划并执行任务，还能连接多种服务和工具来达成目标，执行任务的能力更强。
- **独立性**:
  - copilot被视为一个“副驾驶”，在完成任务时更多的是起辅助作用，需要用户的引导。
  - 而大模型agent则更像一个初级的“主驾驶”，具有较强的独立性，可以根据目标自主思考和行动。


总结
- AI Agent 更强调**自主性**和**独立**完成任务的能力
- 而 AI Copilot 更侧重于作为人类的**助手**，协助完成特定任务。

场景
- Copilot模式更适合**简单知识交互类**场景，而Agent模式则更适合企业内部**复杂任务**场景，帮助企业尽可能提高劳动生产力

资料
- 麦吉尔大学学者`Keheliya Gallaba`总结的agent设计方案: ppt [Agentic architectures and workflows](https://www.aiwarebootcamp.io/slides/2024_aiwarebootcamp_gallaba_keheliya_agents.pdf)


### Anthropic

详见站内专题: [LLM应用范式](llm_dev)

`Anthropic` 工程师 `Barry Zhang` 在 AI Engineer 工作坊分享: “如何构建有效的 Agent”
- 【2024-12-19】Anthropic 官方 [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- 【2025-4-5】[How We Build Effective Agents: Barry Zhang, Anthropic](https://www.youtube.com/watch?v=D7_ipDqhtwk)


Anthropic 官方 [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

Agent进化之路：
- Building block: The augmented LLM
- Workflow: Prompt chaining
- Workflow: Routing
- Workflow: Parallelization
- Workflow: Orchestrator-workers
- Workflow: Evaluator-optimizer
- Agent

|Type|中文|示意图|
|---|---|---|
| Building block: The augmented LLM |堆积木: LLM增强|![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fd3083d3f40bb2b6f477901cc9a240738d3dd1371-2401x1000.png&w=3840&q=75)|
| Workflow: Prompt chaining         |工作流: 提示链|![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F7418719e3dab222dccb379b8879e1dc08ad34c78-2401x1000.png&w=3840&q=75)|
| Workflow: Routing                 |工作流: 路由|![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F5c0c0e9fe4def0b584c04d37849941da55e5e71c-2401x1000.png&w=3840&q=75)|
| Workflow: Parallelization         |工作流: 并行|![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F406bb032ca007fd1624f261af717d70e6ca86286-2401x1000.png&w=3840&q=75)|
| Workflow: Orchestrator-workers    |工作流: 主从|![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F8985fc683fae4780fb34eab1365ab78c7e51bc8e-2401x1000.png&w=3840&q=75)|
| Workflow: Evaluator-optimizer     |工作流: 评估优化|![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F14f51e6406ccb29e695da48b17017e899a6119c7-2401x1000.png&w=3840&q=75)|
| Agent                             |智能体|![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F58d9f10c985c4eb5d53798dea315f7bb5ab6249e-2401x1000.png&w=3840&q=75)|

Agent 使用场景
- ![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F4b9a1f4eb63d5962a6e1746ac26bbc857cf3474f-2400x1666.png&w=3840&q=75)


观点：Don't build agents for everything，别做什么都能干的 Agent，那是大模型要干的事情😆 
- [小红书帖子总结](https://www.xiaohongshu.com/explore/67fbe939000000001b024aed)

构建有效 Agent 的三大要点：
1. 明智选择应用场景，并非所有任务都需要 Agent；
2. 找到合适的用例后，尽可能长时间地保持系统简单；
3. 在迭代过程中，尝试从 Agent 的视角思考，理解其局限并提供帮助；

Barry 主要负责 Agentic System，演讲内容基于他和 Eric 合著的一篇博文

Agent 系统演进
- **简单功能**： 起初是简单任务，如摘要、分类、提取，这些在几年前看似神奇，现在已成为基础；
- `工作流`（Workflows）： 随着模型和产品成熟，开始编排多个模型调用，形成预定义的控制流，以牺牲成本和延迟换取更好性能。这被认为是 Agent 系统的前身；
- `Agent`： 当前阶段，模型能力更强，领域特定的 Agent 开始出现。与工作流不同，Agent 可以根据环境反馈自主决定行动路径，几乎独立运作；
- 未来（猜测）： 可能是更通用的**单一 Agent**，或**多 Agent 协作**。
  - 趋势: 赋予系统更多自主权，使其更强大有用，但也伴随着更高的成本、延迟和错误后果。

核心观点一：**Agent 并非万能**

并非所有场景都适合构建 Agent (Don't build agents for everything)
- Agent 主要用于扩展**复杂且有价值**的任务，成本高、延迟高，不应作为所有用例的直接升级。
  - 对于可以**清晰映射决策树**的任务，显式构建`工作流`（Workflow）更具成本效益和可控性。
- 何时构建 Agent 的检查清单：
  1. 任务复杂度 ： `Agent` 擅长处理**模糊**问题。如果决策路径清晰，应优先选择`工作流`；
  2. 任务价值： Agent 探索会消耗大量 token，任务价值必须能证明其成本。
    - 对于**预算有限**（如每任务 10 美分）或高容量（如客服）场景，`工作流`可能更合适；
  3. 关键能力的可行性 ： 
    - 确保 Agent 在关键环节（如编码 Agent 的编写、调试、错误恢复能力）不存在严重瓶颈，否则会显著增加成本和延迟。
    - 如有瓶颈，应简化任务范围；
  4. **错误成本**与**发现难度**： 如果错误代价高昂且难以发现，就很难信任 Agent 自主行动。可限制范围（如只读权限、增加人工干预）来缓解，但这也会限制其扩展性；
- 写代码（Coding）是很好的 Agent 用例，因为任务复杂（从设计文档到 PR）、价值高、现有模型（如 Claude）在许多环节表现良好，且结果易于验证，例如单元测试、CI。

核心观点二 **保持简单** (Keep it simple)
- Agent 的核心结构： 模型（Model）+ 工具（Tools）+ 循环（Loop）在一个环境（Environment）中运作。
- 三个关键组成部分：
1. 环境：Agent 操作所在的系统；
2. 工具集： Agent 采取行动和获取反馈的接口；
3. 系统提示： 定义 Agent 的目标、约束和理想行为；
- 迭代方法： 优先构建和迭代这三个基本组件，能获得最高的投资回报率。避免一开始就过度复杂化，这会扼杀迭代速度。优化（如缓存轨迹、并行化工具调用、改进用户界面以增强信任）应在基本行为确定后再进行。
- 一致性： 尽管不同 Agent 应用（编码、搜索、计算机使用）在产品层面、范围和能力上看起来不同，但它们共享几乎相同的简单后端架构。

核心观点三：**像 Agent 一样思考** (Think like your agents)
- 问题：
  - 开发者常从自身角度出发，难以理解 Agent 为何会犯看似反常的错误；
- 解决方法： 
  - 将自己置于 Agent 的“上下文窗口”中。
  - Agent 每步决策都基于有限的上下文信息（如 10k-20k token）；
- 换位思考练习：
  - 尝试从 Agent 的视角完成任务，体验其局限性
  - 例如，只能看到静态截图，在推理和工具执行期间如同“闭眼”操作。
  - 这有助于发现 Agent 真正需要哪些信息（如屏幕分辨率、推荐操作、限制条件）以避免不必要的探索；
- 利用模型自身： 
  - 直接询问模型（如 Claude）：指令是否模糊？是否理解工具描述？为什么做出某个决策？如何帮助它做出更好的决策？这有助于弥合开发者与 Agent 之间的理解差距。

思考
- **预算感知** Agent (Budget-aware Agents)： 控制 Agent 成本和延迟，定义和强制执行时间、金钱、token 预算，以便在生产环境中更广泛地部署。
- **自进化**工具 (Self-evolving Tools)： Agent 能设计和改进自己的工具（元工具），使其更具通用性，能适应不同用例的需求。
- **多 Agent 协作** (Multi-agent Collaboration)： 预计2025年底将出现更多**多 Agent 系统**。
  - 其优势包括**并行化**、**关注点分离**、保护**主 Agent 上下文窗口**等。
  - 关键挑战：Agent 间通信方式，如何实现异步通信，超越当前的用户-助手轮流模式。


### Andrew NG

【2024-3-27】吴恩达
- [解读](https://mp.weixin.qq.com/s/6Jn4-3KPoffsYGrrvYX6vg)
- [Agent才是大模型的最终归宿？](https://mp.weixin.qq.com/s/Y8zj7aWOcyGxNepIV82VQA)
- [Agentic Workflow:AI重塑了我的工作流](https://mp.weixin.qq.com/s/XzEUpUbbWHazAq-OD4EbMA)

2024年3月，初创公司 Cognition 基于大模型开发出首个AI软件工程师Devin
- Devin几乎能完成普通软件工程师能做的所有事情，包括搭建环境、编码、调试；更离谱的是，Devin成功通过了一家AI公司的面试。
- Devin没有开源代码，不过随后就有一个团队为了复刻Devin，开发了[OpenDevin](https://github.com/OpenDevin/OpenDevin)，从代码中可见，其核心就是Agent。

通过agent workflow，人工智能能够胜任的任务种类将会大幅扩展。

吴恩达团队实验，让 AI 去写一些代码并运行，最终对比不同模型和工作流程得出结果的性能。结果如下:
- GPT-3.5 模型:准确率 48%
- GPT-4 模型:准确率 67% 
- GPT-3.5 + Agent:高于 GPT-4 模型的表现
- GPT-4 + Agent:表现远高于 GPT-4 模型，非常出色

吴恩达提到的四种 Agent 设计模式: `Reflection`、`Tool Use`、`Planning`、`Multiagent`
- `反思`（reflection）: Agent 审视和修正自己生成的输出
  - 两个 Agent, 一个负责 Coding，另一个负责 Code Review。
  - 让大模型仔细检查输出内容的准确性、结构规范性等，并且给出评论
  - agent会利用外部组件运行代码，执行单元测试，代码Review，甚至与另一个Agent进行对抗来逐渐提升代码质量
- `工具使用`（Tool use）: AI Agent会与外部组件相连接，使用各种工具来分析、收集信息
  - 例如，执行网络搜索作为上下文输入，基于LLM输出执行发送预警邮件操作。
- `规划`（Planning）: Agent 分解复杂任务并按计划执行
  - 类似于思维链模式，按照逻辑顺序组织和评估信息，形成一系列的思考步骤。
  - 这种方法特别适用于**复杂问题**，因为能够帮助人们逐步分析问题，从而得出合理的结论或解决方案。
  - 任务: 生成一张女孩读书的图像，并且女孩的姿势与男孩一致，最后输出描述图像的音频。
  - Agent 规划: 第一步, 确定男孩的姿势，可能在huggingface上找到一个合适的模型来提取这个姿势，接下来使用controlNet模型来合成一个女孩的图像，然后使用图像到文本的模型，最后使用语音合成。
- `多智能体协作`（Multiagent collaboration）: 多个 Agent 扮演不同角色合作完成任务
  - 将一个复杂任务进行分解，让不同语言模型扮演不同的角色，比如公司CEO、设计师、产品经理或测试员，这些"代理"会相互协作，共同开发游戏等复杂程序。
  - AI客服回答售前，售中，售后三种不同类型的问题。
  - 先基于预训练模型微调出三个专业模型，分别用于回答售前，售中，售后问题
  - 然后，再通过一个LLM判断用户的提问属于售前，售中，售后哪一种，最后调用对应的专业大模型。


### OpenAI


OpenAI AI Agent 使用建议
- 【2025-4-17】[A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)


一句话总结：**可靠性是核心**
	
Agent 定义与特征

OpenAI将Agent定义为"能够独立完成任务的系统"。

Agent具有以下核心特征：
1. 利用大语言模型(LLM)管理`工作流`执行和决策过程
2. 获取上下文并采取行动的工具访问能力
3. 在明确定义的护栏内运行
	
Agent 适用场景：
1. **复杂决策**场景：涉及细微判断、例外情况或上下文敏感决策的工作流
2. **难以维护**的规则系统：笨重系统，更新成本高或容易出错
3. 严重依赖**非结构化**数据：解释自然语言、从文档提取意义或进行对话交互的场景
	
Agent 核心组件
1. 模型：驱动Agent推理和决策的LLM
2. 工具：Agent可用于采取行动的外部函数或API
3. 指令：定义Agent行为的明确指南和护栏
	
设计模式与架构

两种主要编排模式：
1. 单Agent系统：单一模型配备适当工具和指令，在循环中执行工作流
  - 适合初始阶段和相对简单的任务
  - 可通过添加工具逐步扩展能力
2. 多Agent系统：工作流执行分布在多个协调的Agent之间
  - **管理者**模式：中央"管理者"Agent通过工具调用协调多个专业Agent
  - **去中心化**模式：多个Agent 对等运作，根据各自专长交接任务
	
实施建议
1. 渐进式方法：从小处着手，验证有效后逐步扩展
2. 模型选择策略：先使用最强大模型建立基准，再尝试更小模型
3. 人工干预机制：设置失败阈值和高风险行动触发点
4. 护栏分层防御：组合多种护栏类型创建更强韧的系统
	
Agent代表**工作流自动化**的新时代，系统能够处理模糊情况、跨工具采取行动，并以高度自主性处理多步骤任务。

构建可靠的Agent需要强大基础、合适的编排模式和严格的护栏，同时采用迭代方法才能在生产环境中取得成功。


### 其他

智能体时代的设计模式 

多智能体（Mulit-Agent）架构 6 种不同类型：
- 𝟭  `𝗛𝗶𝗲𝗿𝗮𝗿𝗰𝗵𝗶𝗰𝗮𝗹` （ 𝗩𝗲𝗿𝘁𝗶𝗰𝗮𝗹 ） 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲
  - 一名主管代理负责协调多名专门代理。
  - 1）一名代理从内部数据源检索信息
  - 2）另一位经纪人专门从事网络搜索的公共信息
  - 3）第三个代理专门从个人账户（电子邮件、聊天）中检索信息
- 𝟮  `𝗛𝘂𝗺𝗮𝗻-𝗶𝗻-𝘁𝗵𝗲-𝗟𝗼𝗼𝗽` 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲
  - 在处理敏感信息时，在进行下一步操作之前进行人工验证。
- 𝟯  `𝗡𝗲𝘁𝘄𝗼𝗿𝗸` ( **𝗛𝗼𝗿𝗶𝘇𝗼𝗻𝘁𝗮𝗹** ) 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲
  - 代理以多对多方式直接相互通信。形成一个没有严格层级结构的**分散式**网络。
- 𝟰  `𝗦𝗲𝗾𝘂𝗲𝗻𝘁𝗶𝗮𝗹` 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲
  - 代理按顺序处理任务，其中一个代理的输出成为下一个代理的输入。
  - 比如 ：三个顺序代理，其中：
  - 1） 第一个查询代理从矢量搜索中检索信息
  - 2） 第二个查询代理根据第一个代理的发现从网络搜索中检索更多信息
  - 3） 最终生成代理使用来自两个查询代理的信息创建响应
- 𝟱  𝗗𝗮𝘁𝗮 𝗧𝗿𝗮𝗻𝘀𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲
  - 包括专用于**转换数据**的代理。
  - 比如：转换代理，可在插入时丰富数据或转换现有集合
  - 还有一些其他模式可以与这些架构相结合：
  - 1）`𝗟𝗼𝗼𝗽` 𝗽𝗮𝘁𝘁𝗲𝗿𝗻 ：持续改进的迭代循环
  - 2）`𝗣𝗮𝗿𝗮𝗹𝗹𝗲𝗹` 𝗽𝗮𝘁𝘁𝗲𝗿𝗻 ：多个代理同时处理任务的不同部分
  - 3）`𝗥𝗼𝘂𝘁𝗲𝗿` 𝗽𝗮𝘁𝘁𝗲𝗿𝗻 : 中央路由器决定调用哪些代理
  - 4）`𝗔𝗴𝗴𝗿𝗲𝗴𝗮𝘁𝗼𝗿` / `𝘀𝘆𝗻𝘁𝗵𝗲𝘀𝗶𝘇𝗲𝗿` 𝗽𝗮𝘁𝘁𝗲𝗿𝗻 ：收集和合成来自多个代理的输出

参考 [小红书总结](https://www.xiaohongshu.com/explore/67f92d5a000000001c011669)



# 结束
