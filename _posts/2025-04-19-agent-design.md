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


资料
- 【2025-3-31】MetaGPT、蒙特利尔大学等联合出品 [ADVANCES AND CHALLENGES IN FOUNDATION AGENTS](https://arxiv.org/pdf/2504.01990)


## Agent 发展

【2025-4-23】[从 Manus 看 AI Agent 演进之路](https://mp.weixin.qq.com/s/vqDLCse7EPBfkSaxLPMERQ)

AI Agent 技术发展中的**逻辑推理**能力、**上下文记忆**能力和**工具调用**能力还属于Single Agent（单独智能体）迭代过程。

让 AI Agent 真正发展起来，既要做到主流化**规模化**，要实现 多个智能体 Multi-Agent 之间通信互联。

当不同的 AI Agent 在不同的设备、机房之间去做计算和联动，才有机会能够推动上亿级别用户的应用。

而存在一个难点：通用的标准化协议适配范式。

### Agent 阶段

Agent 发展阶段
- 第一阶段：Single Agent（单独智能体）—— 已实现
  - AI Agent 拥有 Planning、Memory、Tools，中间有大模型 LLM 的驱动。
- 第二阶段：Multi-agent（单机）—— 已实现
  - Agent 中的 Planning 部分拥有逻辑推理和调度能力，比如：要实现一个复杂任务，用户可以写很多 prompt，把复杂任务拆成很多个子任务，让各个 Agent 之间去通信，但此时的复杂仍是在一个单进程内完成的。像 LangGraph、CrewAI和微软推出的 AutoGen 都已实现多个 Agent 在一个单机上的库之间通信。
- 第三阶段：Agent实现不同设备、不同机房之间联动（MCP协议）—— 探索中
  - 如果要支持上亿级别用户的应用，要在不同设备、不同机房间数据联动和流通的架构，目前依然处在尝试中的 Agent 第三阶段架构。
  - 解决的问题：很多网站或者工具并不支持AI Agent 的调用（目前很多网站和服务都会有“反机器人/anti-bot”的设置）。
  - 2024年11月初，Antropic 推出“模型上下文协议”（Model Context Protocol 简称`MCP`）协议，统一大语言模型与外部数据源和工具之间的通信协议，MCP 主要目的在于解决当前 AI 模型因数据孤岛限制而无法充分发挥潜力的难题。
  - Antropic 将 MCP 协议称之为“AI 应用的USB-C端口”，支持将大模型直接连到数据源。此前，企业和开发者要把不同数据接入 AI 系统，都得单独开发对接方案，而MCP做的就是提供一个「通用协议」来解决这个问题。
- 第四阶段：端云一体化的分布式 Agent 网络与互联协议 —— 待突破
  - 还有最后一个问题：目前 AI Agent 应用大规模爆发的壁垒，是真正统一的 Agent 和 Agent 间的协议通信标准与分布式计算，就像如今的安卓与iOS一样，也需要一个全球大家承认且通用的 AI OS。

### Agent 进化事件

GPT 进化
- (1) 推理 `Planning`：让 AI 能“**思考**”和“**行动**”
  - 2022年10月, 普林斯顿与 Google Brain 合作的团队提出了 ReAct 框架论文, 通过提示工程让LLM具备一定推理、工具执行能力
    - 所有 AI Agent 整体构架都从这篇论文开始。
    - 然而当时最先进模型 `GPT-3.5` 能力相对有限，使得 AI Agent 逻辑推理能力并不出彩，错误率非常高
  - 2023年3月14号，GPT-4 大模型上线，比 3.5版本模型更强，理解能力、推理能力、回答质量都大幅度提升。
  - 2023年3月23日：ChatGPT 插件功能 Plugin 发布, 允许大模型 LLM 调用外部工具并且开发 APP, 搜索互联网、连接不同的数据库
  - AI Agent 技术的三大要素中的 Planning 搭建成型
- (2) 记忆 `Memory`：让 Al 有更强的“**记忆**”能力
  - GPT-4 刚开始只有 4096 个token, 容纳3000多个英文单词
  - 2023年5月11日：竞争对手 Anthropic 公司发布 Claude 大模型支持 **100K** token（上下文窗口），技术史上里程碑式进步。
  - 2023年6月13日：OpenAI 发布 `Function Calling` 函数调用，引入 json 模式 & GPT 大模型支持 **16k** token
  - AI Agent 更加可靠的调用外部API，比如说查天气、自动填表等等任务。
  - 2023年11月21号，Anthropic Claude 2.1 版本又进一步把上下文窗口扩展到 20 万个 token，相当于 AI 可以一次性记住一整本教科书的内容，思考能力也出现大大的提升，进一步扩大大模型的记忆能力，优化推理和决策过程。
  - 2024年2月：Google 发布 Gemini 1.5 大模型支持百万级 token
  - AI Agent 发展必备的第二个技术壁垒  Memory 的限制也完全的被打破了，对于开发者来说就不是大问题
- (3) 工具 `Tools`：让 AI 开始“**动手**”
  - 2023年12月：Simular AI 发布AI Agent Demo, 首次在发布会上让大模型操控电脑
  - 2024月10月：Claude 大模型增加 Computer use功能，进一步支持 AI Agent 对电脑的控制，让 AI 更像可以行动起来的智能助手。
  - 2024年底：吴恩达教授公开主题演讲 AI, Agents and Applications
  - 开发者社区或初创社区的行动都比大公司要早很多。
  - 媒体头版开始出现：“2025年将成为 AI Agent 应用的元年的预测”





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


### 总结

【2025-4-25】[掌握Agent设计的九大模式](https://mp.weixin.qq.com/s/WxuhGLg7JRCa4aJYY210Ew)

总结
- ReAct: ReAct 模式将**推理**（Reasoning）和**行动**（Act）紧密结合
- Plan and Solve 模式
- Reason without Observation 模式
- LLMCompiler 模式
- Basic Reflection 模式
- Reflexion 模式
- Language Agent Tree Search 模式
- Self-Discover 模式
- Storm 模式

### ReAct

ReAct 模式将**推理**（Reasoning）和**行动**（Act）紧密结合
- 每次行动后立即进行观察（Observation），并将观察结果反馈到下一次推理过程，使 Agent 能够更好地适应环境变化，维持短期记忆，从而实现更加灵活和智能的行为。

#### 流程

ReAct 模式的核心在于其独特的交互流程：
- 接收任务：Agent 接收到用户或系统的任务指令。
- 推理（Thought）：Agent 根据当前的任务和已有的知识进行推理，生成初步的行动计划。
- 行动（Action）：Agent 执行推理得出的行动。
- 观察（Observation）：Agent 对行动的结果进行观察，获取反馈信息。
- 循环迭代：将观察结果反馈到推理过程中，Agent 根据新的信息重新进行推理，生成新的行动计划，并继续执行行动和观察，直到任务完成。

```sh
+-------------------+
|     接收任务      |
+-------------------+
           |
           v
+-------------------+
|     推理（Thought）|
+-------------------+
           |
           v
+-------------------+
|     行动（Action）  |
+-------------------+
           |
           v
+-------------------+
|     观察（Observation）|
+-------------------+
           |
           v
+-------------------+
|     循环迭代      |
+-------------------+
```


优势：
- 适应性强：Agent 能够根据环境的变化及时调整自己的行为，适应动态环境。
- 维持短期记忆：通过观察和反馈，Agent 能够记住之前的行动和结果，避免重复错误或遗漏重要信息。
- 提高效率：减少了不必要的行动，提高了任务完成的效率。

#### 示例

Agent 去厨房拿胡椒粉的任务：

```py
class ReActAgent:
    def __init__(self):
        self.knowledge_base = {
            "locations": ["台面上", "灶台底下抽屉", "油烟机左边吊柜"]
        }

    def think(self, task):
        # 推理：根据任务生成行动计划
        for location in self.knowledge_base["locations"]:
            yieldf"检查 {location} 是否有胡椒粉"

    def act(self, action):
        # 行动：执行具体的行动
        if action == "检查 台面上 是否有胡椒粉":
            return"台面上没有胡椒粉"
        elif action == "检查 灶台底下抽屉 是否有胡椒粉":
            return"灶台底下抽屉有胡椒粉"
        elif action == "检查 油烟机左边吊柜 是否有胡椒粉":
            return"油烟机左边吊柜没有胡椒粉"

    def observe(self, action_result):
        # 观察：记录行动的结果
        return action_result

    def run(self, task):
        # 主循环：推理 -> 行动 -> 观察 -> 循环迭代
        for action in self.think(task):
            action_result = self.act(action)
            observation = self.observe(action_result)
            print(f"Action: {action}")
            print(f"Observation: {observation}")
            if"有胡椒粉"in observation:
                print("任务完成：找到胡椒粉")
                break


# 示例运行
agent = ReActAgent()
agent.run("去厨房拿胡椒粉")
```

输出结果

```sh
Action: 检查 台面上 是否有胡椒粉
Observation: 台面上没有胡椒粉
Action: 检查 灶台底下抽屉 是否有胡椒粉
Observation: 灶台底下抽屉有胡椒粉
任务完成：找到胡椒粉
```

通过这个代码示例，我们可以看到 ReAct 模式如何通过推理、行动和观察的循环迭代来完成任务。这种模式在实际应用中可以扩展到更复杂的任务和场景，例如智能客服、自动化任务处理等，通过不断优化 Agent 的推理和行动策略，实现更加智能和高效的任务执行。

### Plan and Solve

Plan and Solve 模式原理
Plan and Solve 模式是一种先规划再执行的 Agent 设计模式，适用于复杂任务的处理。在这种模式下，Agent 首先会根据任务目标生成一个多步计划，然后逐步执行计划中的每个步骤。如果在执行过程中发现计划不可行或需要调整，Agent 会重新规划，从而确保任务能够顺利进行。

Plan and Solve 模式的交互流程如下：
- 接收任务：Agent 接收到用户或系统的任务指令。
- 规划（Plan）：Agent 根据任务目标生成一个多步计划，明确每个步骤的具体内容和顺序。
- 执行（Solve）：Agent 按照计划逐步执行每个步骤。
- 观察（Observation）：Agent 对执行结果进行观察，判断是否需要重新规划。
- 重新规划（Replan）：如果发现计划不可行或需要调整，Agent 会根据当前状态重新生成计划，并继续执行。
- 循环迭代：重复执行、观察和重新规划的过程，直到任务完成。

Plan and Solve 模式的交互流程可以用以下图示来表示：

```
+-------------------+
|     接收任务      |
+-------------------+
           |
           v
+-------------------+
|     规划（Plan）   |
+-------------------+
           |
           v
+-------------------+
|     执行（Solve）  |
+-------------------+
           |
           v
+-------------------+
|     观察（Observation）|
+-------------------+
           |
           v
+-------------------+
|     重新规划（Replan）|
+-------------------+
           |
           v
+-------------------+
|     循环迭代      |
+-------------------+
```

优势在于：
- 适应性强：Agent 能够根据任务的复杂性和环境的变化灵活调整计划。
- 任务导向：通过明确的计划，Agent 能够更高效地完成任务，避免盲目行动。
- 可扩展性：适用于复杂任务和多步骤任务，能够有效管理任务的各个阶段。

#### 示例

为了更好地理解 Plan and Solve 模式，我们可以通过图解和代码示例来展示其具体实现。




#### 示例

实现一个 Agent 制作西红柿炒鸡蛋的任务：

```py
class PlanAndSolveAgent:
    def __init__(self):
        self.knowledge_base = {
            "steps": [
                "检查冰箱是否有西红柿和鸡蛋",
                "如果没有西红柿，购买西红柿",
                "准备食材：切西红柿、打鸡蛋",
                "热锅加油，炒鸡蛋",
                "加入西红柿，翻炒",
                "调味，出锅"
            ]
        }

    def plan(self, task):
        # 规划：根据任务生成多步计划
        return self.knowledge_base["steps"]

    def solve(self, step):
        # 执行：执行具体的步骤
        if step == "检查冰箱是否有西红柿和鸡蛋":
            return"冰箱里有鸡蛋，但没有西红柿"
        elif step == "如果没有西红柿，购买西红柿":
            return"购买了西红柿"
        elif step == "准备食材：切西红柿、打鸡蛋":
            return"食材准备完毕"
        elif step == "热锅加油，炒鸡蛋":
            return"鸡蛋炒好了"
        elif step == "加入西红柿，翻炒":
            return"西红柿炒好了"
        elif step == "调味，出锅":
            return"西红柿炒鸡蛋完成"

    def observe(self, step_result):
        # 观察：记录执行结果
        return step_result

    def replan(self, current_plan, observation):
        # 重新规划：根据观察结果调整计划
        if"没有西红柿"in observation:
            current_plan.insert(1, "如果没有西红柿，购买西红柿")
        return current_plan

    def run(self, task):
        # 主循环：规划 -> 执行 -> 观察 -> 重新规划 -> 循环迭代
        plan = self.plan(task)
        for step in plan:
            step_result = self.solve(step)
            observation = self.observe(step_result)
            print(f"Step: {step}")
            print(f"Observation: {observation}")
            if"没有西红柿"in observation:
                plan = self.replan(plan, observation)
            if"完成"in observation:
                print("任务完成：西红柿炒鸡蛋制作完成")
                break
# 示例运行
agent = PlanAndSolveAgent()
agent.run("制作西红柿炒鸡蛋")
```


输出结果

```
Step: 检查冰箱是否有西红柿和鸡蛋
Observation: 冰箱里有鸡蛋，但没有西红柿
Step: 如果没有西红柿，购买西红柿
Observation: 购买了西红柿
Step: 准备食材：切西红柿、打鸡蛋
Observation: 食材准备完毕
Step: 热锅加油，炒鸡蛋
Observation: 鸡蛋炒好了
Step: 加入西红柿，翻炒
Observation: 西红柿炒好了
Step: 调味，出锅
Observation: 西红柿炒鸡蛋完成
任务完成：西红柿炒鸡蛋制作完成
```

Plan and Solve 模式如何通过规划、执行、观察和重新规划的循环迭代来完成任务。这种模式在实际应用中可以扩展到更复杂的任务和场景，例如项目管理、自动化工作流程等，通过不断优化 Agent 的规划和执行策略，实现更加智能和高效的任务执行。

### Reason without Observation

Reason without Observation 模式原理

Reason without Observation（REWOO）模式是一种创新的 Agent 设计模式，在传统 ReAct 模式的基础上进行了优化，去掉了显式观察（Observation）步骤，而是将观察结果隐式地嵌入到下一步的执行中。这种模式的核心在于通过推理（Reasoning）和行动（Action）的紧密协作，实现更加高效和连贯的任务执行。

#### 流程

REWOO 模式中，Agent 交互流程：
- 接收任务：Agent 接收到用户或系统的任务指令。
- 推理（Reasoning）：Agent 根据当前的任务和已有的知识进行推理，生成初步的行动计划。
- 行动（Action）：Agent 执行推理得出的行动。
- 隐式观察（Implicit Observation）：Agent 在执行行动的过程中，自动将结果反馈到下一步的推理中，而不是显式地进行观察。
- 循环迭代：Agent 根据新的信息重新进行推理，生成新的行动计划，并继续执行行动，直到任务完成。

优势在于：
- 高效性：去掉了显式的观察步骤，减少了交互的复杂性，提高了任务执行的效率。
- 连贯性：通过隐式观察，Agent 的行动更加连贯，避免了不必要的重复操作。
- 适应性：Agent 能够根据任务的复杂性和环境的变化灵活调整行动策略。


REWOO 模式的交互流程可以用以下图示来表示：

```sh
+-------------------+
|     接收任务      |
+-------------------+
           |
           v
+-------------------+
|     推理（Reasoning）|
+-------------------+
           |
           v
+-------------------+
|     行动（Action）  |
+-------------------+
           |
           v
+-------------------+
|     隐式观察（Implicit Observation）|
+-------------------+
           |
           v
+-------------------+
|     循环迭代      |
+-------------------+
```

#### 示例

Agent 完成审批流程的任务：

```py
class REWOOAgent:
    def __init__(self):
        self.knowledge_base = {
            "steps": [
                "从部门 A 获取文件 a",
                "拿着文件 a 去部门 B 办理文件 b",
                "拿着文件 b 去部门 C 办理文件 c"
            ]
        }

    def reason(self, task, current_step):
        # 推理：根据任务和当前步骤生成行动计划
        if current_step == 0:
            return"从部门 A 获取文件 a"
        elif current_step == 1:
            return"拿着文件 a 去部门 B 办理文件 b"
        elif current_step == 2:
            return"拿着文件 b 去部门 C 办理文件 c"

    def act(self, action):
        # 行动：执行具体的行动
        if action == "从部门 A 获取文件 a":
            return"文件 a 已获取"
        elif action == "拿着文件 a 去部门 B 办理文件 b":
            return"文件 b 已办理"
        elif action == "拿着文件 b 去部门 C 办理文件 c":
            return"文件 c 已办理"

    def run(self, task):
        # 主循环：推理 -> 行动 -> 隐式观察 -> 循环迭代
        steps = self.knowledge_base["steps"]
        for current_step in range(len(steps)):
            action = self.reason(task, current_step)
            action_result = self.act(action)
            print(f"Action: {action}")
            print(f"Result: {action_result}")
            if"文件 c 已办理"in action_result:
                print("任务完成：审批流程完成")
                break
# 示例运行
agent = REWOOAgent()
agent.run("完成审批流程")
```

输出结果

```
Action: 从部门 A 获取文件 a
Result: 文件 a 已获取
Action: 拿着文件 a 去部门 B 办理文件 b
Result: 文件 b 已办理
Action: 拿着文件 b 去部门 C 办理文件 c
Result: 文件 c 已办理
任务完成：审批流程完成
```

REWOO 模式如何通过推理和行动的紧密协作，实现高效的任务执行。这种模式在实际应用中可以扩展到更复杂的任务和场景，例如工作流程自动化、多步骤任务处理等，通过不断优化 Agent 的推理和行动策略，实现更加智能和高效的任务执行。


### LLMCompiler 模式

LLMCompiler 模式原理

LLMCompiler 模式是一种通过并行函数调用提高效率的 Agent 设计模式。该模式的核心在于优化任务的编排，使得 Agent 能够同时处理多个任务，从而显著提升任务处理的速度和效率。这种模式特别适用于需要同时处理多个子任务的复杂任务场景，例如多任务查询、数据并行处理等。

#### 流程

LLMCompiler 模式的交互流程：
- 接收任务：Agent 接收到用户或系统的任务指令，任务可能包含多个子任务。
- 任务分解（Task Decomposition）：Agent 将复杂任务分解为多个子任务，并确定这些子任务之间的依赖关系。
- 并行执行（Parallel Execution）：Agent 根据子任务之间的依赖关系，将可以并行处理的子任务同时发送给多个执行器进行处理。
- 结果合并（Result Merging）：各个执行器完成子任务后，Agent 将结果合并，形成最终的输出。
- 循环迭代（Iteration）：如果任务需要进一步处理或调整，Agent 会根据当前结果重新分解任务，并继续并行执行和结果合并，直到任务完成。

优势在于：
- 高效率：通过并行处理多个子任务，显著减少了任务完成的总时间。
- 灵活性：能够根据任务的复杂性和子任务之间的依赖关系动态调整任务分解和执行策略。
- 可扩展性：适用于大规模任务和复杂任务场景，能够有效利用多核处理器和分布式计算资源。


LLMCompiler 模式的交互流程可以用以下图示来表示：

```sh
+-------------------+
|     接收任务      |
+-------------------+
           |
           v
+-------------------+
| 任务分解（Task Decomposition）|
+-------------------+
           |
           v
+-------------------+
| 并行执行（Parallel Execution）|
+-------------------+
           |
           v
+-------------------+
| 结果合并（Result Merging）|
+-------------------+
           |
           v
+-------------------+
|     循环迭代      |
+-------------------+
```

#### 示例

Agent 同时查询两个人的年龄并计算年龄差的任务：

```py
import concurrent.futures

class LLMCompilerAgent:
    def __init__(self):
        self.knowledge_base = {
            "person_age": {
                "张译": 40,
                "吴京": 48
            }
        }

    def query_age(self, name):
        # 查询年龄
        return self.knowledge_base["person_age"].get(name, "未知")

    def calculate_age_difference(self, age1, age2):
        # 计算年龄差
        try:
            return abs(int(age1) - int(age2))
        except ValueError:
            return"无法计算年龄差"

    def run(self, task):
        # 主流程：任务分解 -> 并行执行 -> 结果合并 -> 循环迭代
        if task == "查询张译和吴京的年龄差":
            # 任务分解
            tasks = ["查询张译的年龄", "查询吴京的年龄"]
            results = {}

            # 并行执行
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.query_age, name): name for name in ["张译", "吴京"]}
                for future in concurrent.futures.as_completed(futures):
                    name = futures[future]
                    try:
                        results[name] = future.result()
                    except Exception as e:
                        results[name] = f"查询失败: {e}"

            # 结果合并
            age_difference = self.calculate_age_difference(results["张译"], results["吴京"])
            print(f"张译的年龄: {results['张译']}")
            print(f"吴京的年龄: {results['吴京']}")
            print(f"年龄差: {age_difference}")

# 示例运行
agent = LLMCompilerAgent()
agent.run("查询张译和吴京的年龄差")
```

输出结果

```
张译的年龄: 40
吴京的年龄: 48
年龄差: 8
```

LLMCompiler 模式如何通过任务分解、并行执行和结果合并来高效完成任务。这种模式在实际应用中可以扩展到更复杂的任务和场景，例如多任务查询、数据并行处理等，通过不断优化 Agent 的任务分解和并行执行策略，实现更加智能和高效的任务执行。


### Basic Reflection 模式

Basic Reflection 模式原理

Basic Reflection 模式是一种通过反思和修正来优化 Agent 行为的设计模式。在这种模式下，Agent 的行为可以分为两个阶段：生成初始响应和对初始响应进行反思与修正。这种模式的核心在于通过不断的自我评估和改进，使 Agent 的输出更加准确和可靠。

Basic Reflection 模式的交互流程如下：
- 接收任务：Agent 接收到用户或系统的任务指令。
- 生成初始响应（Initial Response）：Agent 根据任务生成一个初步的回答或解决方案。
- 反思（Reflection）：Agent 对初始响应进行评估，检查是否存在错误、遗漏或可以改进的地方。
- 修正（Revision）：根据反思的结果，Agent 对初始响应进行修正，生成最终的输出。
- 循环迭代（Iteration）：如果任务需要进一步优化，Agent 会重复反思和修正的过程，直到输出满足要求。

优势在于：
- 提高准确性：通过反思和修正，Agent 能够减少错误和遗漏，提高输出的准确性。
- 增强适应性：Agent 能够根据不同的任务和环境调整自己的行为策略，增强适应性。
- 提升用户体验：通过不断优化输出，Agent 能够提供更高质量的服务，提升用户体验。


Basic Reflection 模式的交互流程可以用以下图示来表示：

```py
+-------------------+
|     接收任务      |
+-------------------+
           |
           v
+-------------------+
| 生成初始响应（Initial Response）|
+-------------------+
           |
           v
+-------------------+
|     反思（Reflection）|
+-------------------+
           |
           v
+-------------------+
|     修正（Revision）|
+-------------------+
           |
           v
+-------------------+
|     循环迭代      |
+-------------------+
```

#### 示例

Agent 回答数学问题的任务：

```py
class BasicReflectionAgent:
    def __init__(self):
        self.knowledge_base = {
            "math_problems": {
                "1+1": 2,
                "2*2": 4,
                "3*3": 9
            }
        }

    def initial_response(self, task):
        # 生成初始响应：根据任务生成初步回答
        return self.knowledge_base["math_problems"].get(task, "未知")

    def reflect(self, response):
        # 反思：检查初始响应是否准确
        if response == "未知":
            return"需要进一步查找答案"
        else:
            return"答案正确"

    def revise(self, response, reflection):
        # 修正：根据反思结果调整响应
        if reflection == "需要进一步查找答案":
            return"抱歉，我没有找到答案"
        else:
            return response

    def run(self, task):
        # 主流程：生成初始响应 -> 反思 -> 修正 -> 循环迭代
        initial_response = self.initial_response(task)
        reflection = self.reflect(initial_response)
        final_response = self.revise(initial_response, reflection)
        print(f"Initial Response: {initial_response}")
        print(f"Reflection: {reflection}")
        print(f"Final Response: {final_response}")

# 示例运行
agent = BasicReflectionAgent()
agent.run("1+1")
agent.run("5*5")
```

输出结果

```
Initial Response: 2
Reflection: 答案正确
Final Response: 2
Initial Response: 未知
Reflection: 需要进一步查找答案
Final Response: 抱歉，我没有找到答案
```

Basic Reflection 模式如何通过生成初始响应、反思和修正的过程来优化 Agent 的行为。这种模式在实际应用中可以扩展到更复杂的任务和场景，例如智能客服、自动问答系统等，通过不断优化 Agent 的反思和修正策略，实现更加智能和高效的任务执行。

### Reflexion 模式

Reflexion 模式原理

Reflexion 模式是一种基于强化学习的 Agent 设计模式，旨在通过引入外部数据评估和自我反思机制，进一步优化 Agent 的行为和输出。与 Basic Reflection 模式相比，Reflexion 模式不仅对初始响应进行反思和修正，还通过外部数据来评估回答的准确性和完整性，从而生成更具建设性的修正建议。

Reflexion 模式的交互流程如下：
- 接收任务：Agent 接收到用户或系统的任务指令。
- 生成初始响应（Initial Response）：Agent 根据任务生成一个初步的回答或解决方案。
- 外部评估（External Evaluation）：引入外部数据或标准，对初始响应进行评估，检查是否存在错误、遗漏或可以改进的地方。
- 反思（Reflection）：Agent 根据外部评估的结果，对初始响应进行自我反思，识别问题所在。
- 修正（Revision）：根据反思的结果，Agent 对初始响应进行修正，生成最终的输出。
- 循环迭代（Iteration）：如果任务需要进一步优化，Agent 会重复外部评估、反思和修正的过程，直到输出满足要求。

优势在于：
- 提高准确性：通过外部数据评估和自我反思，Agent 能够更准确地识别错误和遗漏，从而提高输出的准确性。
- 增强适应性：Agent 能够根据不同的任务和环境调整自己的行为策略，增强适应性。
- 提升用户体验：通过不断优化输出，Agent 能够提供更高质量的服务，提升用户体验。
- 强化学习：引入外部数据评估机制，使 Agent 的学习过程更加科学和有效，能够更好地适应复杂任务和动态环境。


Reflexion 模式的交互流程可以用以下图示来表示：

```sh
+-------------------+
|     接收任务      |
+-------------------+
           |
           v
+-------------------+
| 生成初始响应（Initial Response）|
+-------------------+
           |
           v
+-------------------+
| 外部评估（External Evaluation）|
+-------------------+
           |
           v
+-------------------+
|     反思（Reflection）|
+-------------------+
           |
           v
+-------------------+
|     修正（Revision）|
+-------------------+
           |
           v
+-------------------+
|     循环迭代      |
+-------------------+
```

#### 示例

Agent 回答数学问题的任务：

```py
class ReflexionAgent:
    def __init__(self):
        self.knowledge_base = {
            "math_problems": {
                "1+1": 2,
                "2*2": 4,
                "3*3": 9
            }
        }
        self.external_data = {
            "1+1": 2,
            "2*2": 4,
            "3*3": 9,
            "5*5": 25
        }

    def initial_response(self, task):
        # 生成初始响应：根据任务生成初步回答
        return self.knowledge_base["math_problems"].get(task, "未知")

    def external_evaluation(self, response, task):
        # 外部评估：检查初始响应是否准确
        correct_answer = self.external_data.get(task, "未知")
        if response == correct_answer:
            return"答案正确"
        else:
            returnf"答案错误，正确答案是 {correct_answer}"

    def reflect(self, evaluation):
        # 反思：根据外部评估的结果进行自我反思
        if"答案错误"in evaluation:
            return"需要修正答案"
        else:
            return"无需修正"

    def revise(self, response, reflection, evaluation):
        # 修正：根据反思结果调整响应
        if reflection == "需要修正答案":
            correct_answer = evaluation.split("正确答案是 ")[1]
            return correct_answer
        else:
            return response

    def run(self, task):
        # 主流程：生成初始响应 -> 外部评估 -> 反思 -> 修正 -> 循环迭代
        initial_response = self.initial_response(task)
        evaluation = self.external_evaluation(initial_response, task)
        reflection = self.reflect(evaluation)
        final_response = self.revise(initial_response, reflection, evaluation)
        print(f"Initial Response: {initial_response}")
        print(f"External Evaluation: {evaluation}")
        print(f"Reflection: {reflection}")
        print(f"Final Response: {final_response}")

# 示例运行
agent = ReflexionAgent()
agent.run("1+1")
agent.run("5*5")
```

输出结果

```
Initial Response: 2
External Evaluation: 答案正确
Reflection: 无需修正
Final Response: 2
Initial Response: 未知
External Evaluation: 答案错误，正确答案是 25
Reflection: 需要修正答案
Final Response: 25
```

Reflexion 模式如何通过生成初始响应、外部评估、反思和修正的过程来优化 Agent 的行为。这种模式在实际应用中可以扩展到更复杂的任务和场景，例如智能客服、自动问答系统等，通过不断优化 Agent 的反思和修正策略，实现更加智能和高效的任务执行。

### Language Agent Tree Search 模式

Language Agent Tree Search 模式原理

Language Agent Tree Search（LATS）模式是一种融合了树搜索、ReAct、Plan & Solve 以及反思机制的 Agent 设计模式。它通过多轮迭代和树搜索的方式，对可能的解决方案进行探索和评估，从而找到最优解。这种模式特别适用于复杂任务的解决，尤其是在需要对多种可能性进行评估和选择的场景中。

#### 流程

LATS 模式的交互流程如下：
- 接收任务：Agent 接收到用户或系统的任务指令。
- 树搜索（Tree Search）：Agent 构建一个搜索树，将任务分解为多个子任务，并探索所有可能的解决方案路径。
- ReAct 交互：在树搜索的过程中，Agent 使用 ReAct 模式对每个子任务进行推理和行动，获取反馈信息。
- Plan & Solve 执行：Agent 根据树搜索的结果，生成一个多步计划，并逐步执行计划中的每个步骤。
- 反思与修正（Reflection & Revision）：Agent 对执行结果进行反思，评估每个步骤的正确性和效率，根据反思结果对计划进行修正。
- 循环迭代（Iteration）：Agent 重复树搜索、ReAct 交互、Plan & Solve 执行和反思修正的过程，直到找到最优解或任务完成。


优势在于：
- 全局优化：通过树搜索，Agent 能够全面探索所有可能的解决方案，找到最优路径。
- 灵活性：结合 ReAct 和 Plan & Solve 模式，Agent 能够灵活应对任务中的动态变化。
- 准确性：通过反思机制，Agent 能够不断优化自己的行为，提高任务完成的准确性。
- 适应性：适用于复杂任务和多步骤任务，能够有效管理任务的各个阶段。

LATS 模式的交互流程可以用以下图示来表示：

```py
+-------------------+
|     接收任务      |
+-------------------+
           |
           v
+-------------------+
|     树搜索（Tree Search）|
+-------------------+
           |
           v
+-------------------+
| ReAct 交互（ReAct Interaction）|
+-------------------+
           |
           v
+-------------------+
| Plan & Solve 执行（Plan & Solve Execution）|
+-------------------+
           |
           v
+-------------------+
| 反思与修正（Reflection & Revision）|
+-------------------+
           |
           v
+-------------------+
|     循环迭代      |
+-------------------+
```

#### 示例

Agent 解决一个复杂的任务，例如规划一条旅行路线并优化行程：

```py
class LATSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

class LATSAgent:
    def __init__(self):
        self.knowledge_base = {
            "cities": ["北京", "上海", "广州", "深圳"],
            "distances": {
                ("北京", "上海"): 1300,
                ("北京", "广州"): 2000,
                ("北京", "深圳"): 2200,
                ("上海", "广州"): 1200,
                ("上海", "深圳"): 1500,
                ("广州", "深圳"): 100
            }
        }

    def tree_search(self, start, goal):
        # 树搜索：构建搜索树并找到最优路径
        open_list = [LATSNode(start)]
        while open_list:
            current_node = open_list.pop(0)
            if current_node.state == goal:
                return self.get_path(current_node)
            for city in self.knowledge_base["cities"]:
                if city != current_node.state:
                    new_node = LATSNode(city, current_node, f"前往 {city}")
                    open_list.append(new_node)
        returnNone

    def get_path(self, node):
        # 获取路径
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

    def react_interaction(self, path):
        # ReAct 交互：对每个步骤进行推理和行动
        observations = []
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]
            distance = self.knowledge_base["distances"].get((start, end), 0)
            observations.append(f"从 {start} 到 {end} 的距离是 {distance} 公里")
        return observations

    def plan_and_solve(self, observations):
        # Plan & Solve 执行：根据观察结果生成计划并执行
        plan = []
        for observation in observations:
            plan.append(f"根据 {observation}，调整行程")
        return plan

    def reflect_and_revise(self, plan):
        # 反思与修正：评估计划并进行修正
        revised_plan = []
        for step in plan:
            if"调整行程"in step:
                revised_plan.append("优化行程")
        return revised_plan

    def run(self, start, goal):
        # 主流程：树搜索 -> ReAct 交互 -> Plan & Solve 执行 -> 反思与修正 -> 循环迭代
        path = self.tree_search(start, goal)
        if path:
            observations = self.react_interaction(path)
            plan = self.plan_and_solve(observations)
            revised_plan = self.reflect_and_revise(plan)
            print(f"路径: {path}")
            print(f"观察结果: {observations}")
            print(f"初始计划: {plan}")
            print(f"修正后的计划: {revised_plan}")
        else:
            print("未找到路径")

# 示例运行
agent = LATSAgent()
agent.run("北京", "深圳")
```

输出结果

```
路径: ['北京', '上海', '深圳']
观察结果: ['从 北京 到 上海 的距离是 1300 公里', '从 上海 到 深圳 的距离是 1500 公里']
初始计划: ['根据 从 北京 到 上海 的距离是 1300 公里，调整行程', '根据 从 上海 到 深圳 的距离是 1500 公里，调整行程']
修正后的计划: ['优化行程', '优化行程']
```



LATS 模式如何通过树搜索、ReAct 交互、Plan & Solve 执行和反思修正的多轮迭代来优化 Agent 的行为。这种模式在实际应用中可以扩展到更复杂的任务和场景，例如路径规划、资源优化等，通过不断优化 Agent 的行为策略，实现更加智能和高效的任务执行。

### Self-Discover 模式

Self-Discover 模式原理

Self-Discover 模式是一种让 Agent 在更小粒度上对任务本身进行反思的设计模式。这种模式的核心在于通过自我发现和自我调整，使 Agent 能够更深入地理解任务的本质和需求，从而优化行为和输出。与 Reflexion 模式相比，Self-Discover 模式不仅关注任务的执行结果，还注重任务本身的逻辑和结构，通过自我发现潜在问题和改进点，实现更深层次的优化。

#### 流程

Self-Discover 模式的交互流程如下：
- 接收任务：Agent 接收到用户或系统的任务指令。
- 任务分析（Task Analysis）：Agent 对任务进行初步分析，识别任务的关键要素和目标。
- 自我发现（Self-Discovery）：Agent 对任务本身进行反思，发现潜在的问题、遗漏或可以改进的地方。这一步骤包括对任务逻辑、数据需求和目标的深入分析。
- 调整策略（Strategy Adjustment）：根据自我发现的结果，Agent 调整任务执行策略，优化行为路径。
- 执行与反馈（Execution & Feedback）：Agent 按照调整后的策略执行任务，并收集反馈信息，进一步优化行为。
- 循环迭代（Iteration）：Agent 重复自我发现、调整策略和执行任务的过程，直到任务完成且达到最优解。

优势在于：
- 深度优化：通过自我发现和调整策略，Agent 能够深入理解任务的本质，实现更深层次的优化。
- 适应性强：Agent 能够根据任务的变化和复杂性灵活调整行为策略，增强适应性。
- 提高效率：通过不断优化任务执行路径，Agent 能够减少不必要的操作，提高任务完成的效率。
- 提升用户体验：通过提供更高质量的服务，Agent 能够更好地满足用户需求，提升用户体验。


Self-Discover 模式的交互流程可以用以下图示来表示：

```
+-------------------+
|     接收任务      |
+-------------------+
           |
           v
+-------------------+
|     任务分析（Task Analysis）|
+-------------------+
           |
           v
+-------------------+
|     自我发现（Self-Discovery）|
+-------------------+
           |
           v
+-------------------+
|     调整策略（Strategy Adjustment）|
+-------------------+
           |
           v
+-------------------+
| 执行与反馈（Execution & Feedback）|
+-------------------+
           |
           v
+-------------------+
|     循环迭代      |
+-------------------+
```

#### 示例


Self-Discover 模式代码示例，用于实现一个 Agent 优化一个简单的数据分类任务：

```py
class SelfDiscoverAgent:
    def __init__(self):
        self.knowledge_base = {
            "data": [
                {"feature1": 1, "feature2": 2, "label": "A"},
                {"feature1": 2, "feature2": 3, "label": "B"},
                {"feature1": 3, "feature2": 4, "label": "A"},
                {"feature1": 4, "feature2": 5, "label": "B"}
            ],
            "initial_strategy": "simple_threshold"
        }

    def task_analysis(self, task):
        # 任务分析：识别任务的关键要素和目标
        returnf"任务分析：{task}"

    def self_discovery(self, analysis):
        # 自我发现：发现潜在的问题和改进点
        if self.knowledge_base["initial_strategy"] == "simple_threshold":
            return"发现：初始策略过于简单，可能无法准确分类"
        else:
            return"无需改进"

    def strategy_adjustment(self, discovery):
        # 调整策略：根据自我发现的结果优化行为路径
        if"过于简单"in discovery:
            return"调整策略：采用更复杂的分类算法"
        else:
            return"保持原策略"

    def execute_and_feedback(self, strategy):
        # 执行与反馈：执行任务并收集反馈信息
        if strategy == "调整策略：采用更复杂的分类算法":
            # 假设新策略提高了分类准确率
            return"执行结果：分类准确率提高到90%"
        else:
            return"执行结果：分类准确率60%"

    def run(self, task):
        # 主流程：任务分析 -> 自我发现 -> 调整策略 -> 执行与反馈 -> 循环迭代
        analysis = self.task_analysis(task)
        discovery = self.self_discovery(analysis)
        strategy = self.strategy_adjustment(discovery)
        feedback = self.execute_and_feedback(strategy)
        print(f"Task Analysis: {analysis}")
        print(f"Self-Discovery: {discovery}")
        print(f"Strategy Adjustment: {strategy}")
        print(f"Execution & Feedback: {feedback}")

# 示例运行
agent = SelfDiscoverAgent()
agent.run("数据分类任务")
```

输出结果

```
Task Analysis: 任务分析：数据分类任务
Self-Discovery: 发现：初始策略过于简单，可能无法准确分类
Strategy Adjustment: 调整策略：采用更复杂的分类算法
Execution & Feedback: 执行结果：分类准确率提高到90%
```

Self-Discover 模式如何通过任务分析、自我发现、调整策略和执行反馈的多轮迭代来优化 Agent 的行为。这种模式在实际应用中可以扩展到更复杂的任务和场景，例如机器学习模型优化、智能决策系统等，通过不断优化 Agent 的行为策略，实现更加智能和高效的任务执行。

### Storm 模式

Storm 模式原理

Storm 模式是一种专注于从零开始生成复杂内容的 Agent 设计模式，特别适用于需要系统化构建和优化内容生成的任务，例如生成类似维基百科的文章、报告或知识库。其核心在于通过逐步构建大纲，并根据大纲逐步丰富内容，从而生成高质量、结构化的文本。

Storm 模式的交互流程：
- 接收任务：Agent 接收到用户或系统的任务指令，明确需要生成的内容主题。
- 构建大纲（Outline Construction）：Agent 根据任务主题生成一个详细的大纲，明确内容的结构和各个部分的主题。
- 内容生成（Content Generation）：Agent 根据大纲逐步生成每个部分的具体内容，确保内容的连贯性和准确性。
- 内容优化（Content Optimization）：Agent 对生成的内容进行优化，包括语言润色、逻辑调整和信息补充，以提高内容的质量。
- 循环迭代（Iteration）：Agent 重复内容生成和优化的过程，直到内容满足用户需求或达到预设的质量标准。

优势在于：
- 系统化生成：通过构建大纲和逐步填充内容，确保生成内容的结构化和系统性。
- 高质量输出：通过多轮优化，Agent 能够生成高质量、连贯且准确的内容。
- 适应性强：适用于多种内容生成任务，包括但不限于文章、报告、知识库等。
- 可扩展性：可以根据任务的复杂性和需求灵活调整大纲和内容生成策略。


Storm 模式的交互流程可以用以下图示来表示：

```sh
+-------------------+
|     接收任务      |
+-------------------+
           |
           v
+-------------------+
| 构建大纲（Outline Construction）|
+-------------------+
           |
           v
+-------------------+
| 内容生成（Content Generation）|
+-------------------+
           |
           v
+-------------------+
| 内容优化（Content Optimization）|
+-------------------+
           |
           v
+-------------------+
|     循环迭代      |
+-------------------+
```

### 示例

Storm 模式代码示例，用于实现一个 Agent 生成一篇关于“人工智能”的维基百科风格文章：

```py
class StormAgent:
    def __init__(self):
        self.knowledge_base = {
            "topics": {
                "人工智能": {
                    "定义": "人工智能（Artificial Intelligence, AI）是计算机科学的一个分支，旨在创建能够执行复杂任务的智能机器。",
                    "历史": "人工智能的发展可以追溯到20世纪40年代，当时科学家们开始探索如何使计算机模拟人类智能。",
                    "应用": "人工智能在医疗、金融、教育、交通等多个领域都有广泛的应用。",
                    "未来": "未来，人工智能有望在更多领域实现突破，推动社会的智能化发展。"
                }
            }
        }

    def outline_construction(self, topic):
        # 构建大纲：根据主题生成大纲
        outline = [
            "定义",
            "历史",
            "应用",
            "未来"
        ]
        return outline

    def content_generation(self, topic, section):
        # 内容生成：根据大纲部分生成具体内容
        return self.knowledge_base["topics"][topic][section]

    def content_optimization(self, content):
        # 内容优化：对生成的内容进行润色和调整
        optimized_content = content.replace("有望", "有巨大潜力")
        return optimized_content

    def run(self, topic):
        # 主流程：构建大纲 -> 内容生成 -> 内容优化 -> 循环迭代
        outline = self.outline_construction(topic)
        article = {}
        for section in outline:
            content = self.content_generation(topic, section)
            optimized_content = self.content_optimization(content)
            article[section] = optimized_content
        return article

# 示例运行
agent = StormAgent()
article = agent.run("人工智能")
for section, content in article.items():
    print(f"### {section}")
    print(content)
```

输出结果

```
### 定义
人工智能（Artificial Intelligence, AI）是计算机科学的一个分支，旨在创建能够执行复杂任务的智能机器。
### 历史
人工智能的发展可以追溯到20世纪40年代，当时科学家们开始探索如何使计算机模拟人类智能。
### 应用
人工智能在医疗、金融、教育、交通等多个领域都有广泛的应用。
### 未来
未来，人工智能有巨大潜力在更多领域实现突破，推动社会的智能化发展。
```

Storm 模式如何通过构建大纲、内容生成和内容优化的多轮迭代来生成高质量的文章。这种模式在实际应用中可以扩展到更复杂的任务和场景，例如生成研究报告、知识库条目等，通过不断优化 Agent 的内容生成和优化策略，实现更加智能和高效的任务执行。


## 思考


### RL

【2025-4-21】[强化学习之于 AI Agent，是灵魂、还是包袱？](https://mp.weixin.qq.com/s/88ChEKHaIeOv76xd5v2S1A)

如何构建 Agent? 公认的技术路径：
- 一是拥有基础模型是构建 Agent 的起点
- 二是 RL 是赋予 Agent 连贯行为和目标感的“灵魂”

Agent 不能仅靠 Workflow 搭建

#### 支持

Pokee AI 创始人、前 Meta AI应用强化学习团队负责人`朱哲清`，对 RL 始终坚定信仰的“长期主义者”。
- RL 核心优势在于**目标驱动**，不是简单地响应输入，而是围绕清晰目标，进行策略规划和任务执行。
- 一旦缺少了 RL 参与，Agent 就容易陷入“走一步看一步”的模式，缺乏内在驱动力，最终难以真正胜任复杂任务的完成。

真正的 Agent 核心: 执行力与影响力。

如果一个系统只是单纯地生成内容或文件，那更像是一个普通的工具，而非真正的 Agent。

而当它能够对环境产生不可逆的影响时，它才具备了真正的执行性。

只有与环境发生深度交互，且产生的影响不可逆，才能称之为真正的 Agent。

带有 Workflow 的产品是 Agent 发展的**初期**形态。
- 虽然有明确目标和流程，但仍需要人为干预。
- 真正的 Agent 不仅仅是按照预设的工具来操作，而是能够根据给定目标，自主选择和使用工具完成任务。

#### 反对

香港科技大学（广州）博士生，DeepWisdom 研究员`张佳钇`对 RL 持**保留**态度, 追求**跨环境**的智能体：
- 现有RL技术虽能在**特定环境**中提升Agent能力，但这本质上是“任务特化”而非真正的智能泛化。
- 在实现跨环境数据的有效统一表征之前，RL面临的**跨环境**学习困境难以突破。

用 RL 对语言模型进行环境内优化本身没有问题，但问题在于: 
- 目前很多研究使用的仍是能力较弱的基础模型（base model），即便训练到“最优”，也只是对单一环境的适配，缺乏跨环境的泛化能力。
- “使用 RL 训出一个适应某个环境的 Agent 已经很近，但距离训出通用跨环境的 Agent 还有很长的一段路要走。”

Agent 发展过程分为六个阶段：
- 第一阶段：构成 Agent 系统的**最底层节点**，语言模型被调用来执行基本任务；
- 第二阶段：在底层调用节点基础上，构建出固定的 **agentic workflow**，每个节点的角色与职责预设明确；
- 第三阶段：底层组件演化为具有自身逻辑和动作空间的 **autonomous agent**；
- 第四阶段：多个 autonomous agents 通过主动交流机制构建系统，形成 **Multi Autonomous Agent Systems**（MAS）；
- 第五阶段：底层组件拥有与人类一致的环境空间，成为 **Foundation Agent**，开始协助人类**跨环境**完成任务；
- 第六阶段：Foundation Agent 基于人类目标与其他 Agent 产生联系，演化出具备自主协作能力的**Foundation Agents 网络**。真正实现以人类目标为核心的多智能体社会，达到Agent与人类共生的范式。

目前大多数  Agent 产品公司仍停留在第二到第三阶段之间，尚未迈过第四阶段的门槛，而“最大的瓶颈在于当前 Agent 仍**严重依赖**人类预设的 workflow 节点，缺乏真正的自主性。”


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


### LangChain -- 精华

【2025-4-21】精华 [Agents和Workflows孰好孰坏，LangChain创始人和OpenAI杠上了](https://mp.weixin.qq.com/s/hWON23L4WD_1vRZGbTgKbw)
- 原文 【2025-4-20】[how-to-think-about-agent-frameworks](https://blog.langchain.dev/how-to-think-about-agent-frameworks/)

LangChain 创始人 `Harrison Chase` 对于 OpenAI 一些观点持有异议，尤其是「**通过 LLMs 来主导 Agent**」的路线。

Harrison Chase 认为
- 并非要通过严格的「**二元论**」来区分 Agent，目前大多数的「Agentic 系统」都是 `Workflows` 和 `Agents` 的结合。
- 理想的 Agent 框架应允许从「结构化`工作流`」逐步过渡到「**由模型驱动**」，并在两者之间灵活切换。

OpenAI 观点建立在一些错误的**二分法**上，混淆了「Agentic 框架」的不同维度，从而夸大了单一封装的价值。
- 混淆了「`声明式` vs `命令式`」与「`Agent 封装`」，以及「`Workflows` vs `Agents`」。

观点: LLMs 越来越强, 最终都会变成 Agents, 而不是 Workflows？

事实：
- 调用工具的 Agents 的性能继续提升
- 控制输入给 LLM 的内容依然会非常重要（垃圾进，垃圾出）
- 一些应用，简单工具调用循环足够了
- 另一些应用，Workflows 更简单、更便宜、更快、也更好
- 对于大多数应用，生产环境 Agentic 系统将是 Workflows 和 Agents 结合。

Harrison Chase 更认同 Anthropic 此前发布的如何构建高效 Agents 的文章
- 对于 Agent 定义，Anthropic 提出了「`Agentic 系统`」的概念，并且把 Workflows 和 Agents 都看作是其不同表现形式。

`大模型派`（Big Model）和`工作流派`（Big Workflow）的又一次争锋
- 前者认为每次模型升级都可能让精心设计的工作流**瞬间过时**，这种「苦涩的教训」让他们更倾向于构建通用型、结构最少的**智能体系统**。
- 而以 LangGraph 为代表的后者，强调通过**显式代码**、**模块化**工作流来构建智能体系统。结构化的流程更可控、更易调试，也更适合复杂任务。

资料：
- OpenAI 的[构建 Agents 指南](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)（写得不太行）：
- Anthropic [构建高效 Agents 指南](https://www.anthropic.com/engineering/building-effective-agents?ref=blog.langchain.dev)
- [LangGraph](https://www.langchain.com/langgraph)（构建可靠 Agents 的框架）

要点
- 构建可靠的 Agentic 系统，其核心难点在于确保 LLM 在每一步都能拿到恰当的上下文信息。这既包括精准控制输入给 LLM 的具体内容，也包括执行正确的步骤来生成那些有用的内容。
- `Agentic 系统`包含 Workflows 和 Agents（以及介于两者之间的一切）。
- 大多数的 Agentic 框架，既不是**声明式**也不是**命令式**的编排工具，而是提供了一套 **Agent 封装能力**的集合。
- Agent 封装使入门变得更加容易，但常常把底层细节隐藏起来，反而增加了确保 LLM 在每一步都能获得恰当上下文的难度。
- 无论 Agentic 系统是大是小，是 Agents 主导还是 Workflows 驱动，都能从同一套通用的实用功能中获益。这些功能可以由框架提供，也可以完全自己从头搭建。
- 把 LangGraph 理解成一个编排框架（它同时提供了声明式和命令式的 API），然后在它之上构建了一系列 Agent 封装，这样想是最恰当的。

问卷调查：「在将更多 Agents 投入生产时，你们遇到的最大障碍是什么？」
- 排名第一的回答：「performance quality」。

让 Agents 稳定可靠地工作，依然是个巨大的挑战。

|类别|占比|
| ---- | ---- |
|Performance quality|41%|
|Cost|18.4%|
|Safety concerns|18.4%|
|Latency|15.1%|
|Other|7%|

为什么 LLM 会出错？
- 一是模型**本身能力**还不够；
- 二是传递给模型的**上下文信息**不对或者不完整。

第二种情况更常见。

什么原因导致上下文信息传递出问题？
- System Message 不完整或写得太短
- 用户的输入太模糊
- 没有给 LLM 提供正确的工具
- 工具描述写得不好
- 没有传入恰当的上下文信息
- 工具返回的响应格式不对

构建可靠的 Agentic 系统，难点在于：如何确保 LLM 每步都能拿到最合适的上下文信息。
- 一是精准控制到底把**哪些具体内容**喂给 LLM
- 二是执行正确步骤来生成那些有用的内容。

「workflow」 到 「agent」 范围内构建应用程序时，要考虑两件事：
- **可预测性**（Predictability） vs **自主性**（agency）
  - 可靠性并不等同于可预测性, 但密切相关
  - 系统越偏向 Agentic，其可预测性就越低
- **低门槛**（low floor），**高上限**（high ceiling）
  - Workflow 框架**高上限**，但**门槛也高**，但需要自己编写很多 Agent 逻辑。
  - Agent 框架则是**低门槛**，但**上限也低** —— 虽然容易上手，但不足以应对复杂用例。
  - LangGraph 目标: 兼具**低门槛**（提供内置的 Agent 封装，方便快速启动）和**高上限**（提供低层功能，支持实现高级用例）。

LangGraph 最常见的方式主要有两种：
- 一种是通过声明式的、基于图（Graph）的语法
- 另一种是利用构建在底层框架之上的 Agent 封装

此外，LangGraph 还支持函数式 API 以及底层的事件驱动 API，并提供了 Python 和 Typescript 两个版本。

LangGraph 内置了一个持久化层，这使得其具备**容错**能力、**短期记忆**以及**长期记忆**。

这个持久化层还支持「人工参与决策」（human-in-the-loop）和「人工监督流程」（human-on-the-loop）的模式，比如中断、批准、恢复以及时间回溯（time travel）等功能。

LangGraph 内建支持多种流式传输，包括 tokens 的流式输出、节点状态的更新和任意事件的流式推送。同时，LangGraph 可以与 LangSmith 无缝集成，方便进行调试、评估和可观测性分析。

生产环境中大多数的 Agentic 系统都是 Workflows 和 Agents 的组合。一个成熟的生产级框架必须同时支持 workflow 和 agent 两种模式。

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
