---
layout: post
title:  智能体记忆设计 Agent Memory
date:   2025-07-21 12:00:00
categories: 大模型
tags: LLM agent 智能体 记忆
excerpt: 智能体记忆设计专题
mathjax: true
permalink: /agent_memory/
---

* content
{:toc}


# 智能体记忆设计


## Memory 记忆

记忆模块像 Agent大脑，积累经验、自我进化，让agent行为更加一致、合理和有效。

记忆模块主要记录 Agent 行为，并为未来 Agent 决策提供支撑

- （1）**记忆结构**
  - 统一记忆:仅考虑短期记忆，不考虑长期记忆；
  - 混合记忆:长期记忆和短期记忆相结合
- （2）**记忆形式**:主要基于以下 4 种形式
  - 语言
  - 数据库
  - 向量表示
  - 列表
- （3）**记忆内容**:常见3 种操作:
  - 记忆读取
  - 记忆写入
  - 记忆反思


agentic memory is represented as:
- `Sensory memory` or short-term holding of inputs which is not emphasized much in agents. 
- `Short-term memory` which is the LLM context window 
- `Long-term memory` which is the external storage such as RAG or knowledge graphs.


## 人类记忆

设计灵感来自人类记忆过程的**认知科学研究**。

### 记忆工作模式

记忆工作模型
- `The Multi-Store (Modal) Model`. 最早的标准三阶段记忆存储结构的模型。
  - Atkinson-Shiffrin 三阶段模型
  - ![](https://pic1.zhimg.com/v2-463a498d679b5eee50a75ad48ee53d36_1440w.jpg)
- `Working Memory Models` 短期记忆只是存储的信息，要对短期记忆进行整合、与长期记忆进行桥接，因此提出**工作记忆**概念
  - ![](https://picx.zhimg.com/v2-3bae78313525e1713336df830c509a7f_1440w.jpg)
- `Serial-Parallel-Independent (SPI) Model`. （串行-并行-独立）模型
  - Serial（串行）：感知信息进入系统是有顺序的，例如先通过感知系统，再进入语义或情节系统。
  - Parallel（并行）：一旦信息被编码，它可以同时被不同模块（如语义、情节）使用。
  - Independent（独立）：各个模块在使用上可以互相独立，不必每次都依赖其他模块来操作（例如可以有程序性记忆而没有情节记忆）。
  - ![](https://pic3.zhimg.com/v2-600ee5593f74ce9f5caf61cf30909bea_1440w.jpg)
- `Global Workspace Theory (GWT) and the IDA/LIDA Framework`. **全局工作空间**理论
  - 全局工作空间理论（Global Workspace Theory, GWT）将意识视为一种“广播机制”，认为大脑中存在多个专门处理感知和认知任务的模块，只有当某条信息被广播到全局工作空间中，才能进入意识和工作记忆，供整个系统共享与处理。
  - 将大脑想象成一个公司，很多人在后台干活（视觉、记忆、听觉），“广播室”把某个重要的信息广播出来（比如你突然想到今晚有个会议），所有系统都能听到这个广播，并据此调整工作（比如安排出门路线、调整计划）。
  - ![](https://pic3.zhimg.com/v2-bbe13d9fb4f3ed8fbf5d27d424e8ed7e_1440w.jpg)
- `ACT-R and Cognitive Architectures`. 思想的适应性控制-理性
  - 综合性认知架构，模拟人类如何感知、记忆、思考与行动。将大脑划分为多个功能模块，如视觉、动作、陈述性记忆和程序性记忆，各模块通过缓冲区交互，构成完整的认知流程。ACT-R 区分事实知识（chunk）与条件规则（if-then），通过符号规则驱动认知行为，同时引入数学函数进行次符号调节，以更真实地还原人类的反应速度、记忆强度和策略选择。
  - ![](https://pica.zhimg.com/v2-7966e3719cbaf3bbe3c6ead38ce38860_1440w.jpg)

详见站内专题: [大脑工作原理](brain)

### 记忆类型

人类记忆发展:
- **感官记忆**，记录、感知输入；
- **短期记忆**，暂时保持信息；
- **长期记忆**，在更长的时间内巩固信息。

【2024-7-4】张亚勤: 人类拥有`DNA记忆`、`短期记忆`、`海马体记忆`、`皮层记忆`、`长期记忆`。

记忆定义为用于获取、存储、保留和后续检索信息的过程，人类大脑中主要有三种类型的记忆。
1. `感官记忆`（Sensory memory）
  - 这种记忆处于记忆的最早阶段，提供了在原始刺激结束后保留感官信息（视觉，听觉等）印象的能力，通常只持续几秒钟。
  - 感官记忆的子类别包括**图标记忆**（视觉）、**回声记忆**（听觉）和**触觉记忆**（触觉）。
2. `短时记忆`（STM）或**工作记忆**（Working Memory）
  - 存储当前意识到的所有信息，以及执行复杂的认知任务（如学习和推理）所需的信息，大概可以存储7件事，持续20-30秒。
3. `长期记忆`（LTM）
  - LTM 将信息存储相当长的时间，范围从几天到几十年不等，具有基本上无限的存储容量。LTM有两种亚型:
  - 1）显式/**陈述性**记忆，即对事实和事件的记忆，指那些可以有意识地回忆起来的记忆，包括**情景记忆**（事件和经验）和**语义记忆**（事实和概念）。
  - 2）隐式/**程序性**记忆，这种类型的记忆是**无意识**的，包括自动执行的技能和例程，比如骑自行车或在键盘上打字。
- ![](https://pic4.zhimg.com/80/v2-39913cb59e36e3ee0729cad2b56c98bb_1440w.webp)

图解: 
- 机器坏人（AI版）[小红书帖子](https://www.xiaohongshu.com/explore/67e410be000000001d016515)

### 金鱼记忆

大语言模型（LLM）的 “先天短板”—— **记忆容量有限**。

就像大脑的短期记忆，只能临时存下一小段信息，超过 “内存上限” 就会自动 “清缓存”。

LLM 都有 “上下文窗口” 限制,能记住的对话内容长度固定，可能是几千字，也可能几万字。一旦超过这个范围， 早期信息就会被 “挤出去”。
- 跟 AI 从早上聊到晚上，从工作方案聊到周末聚餐，中间提到了 10 个关键信息。
- 但到了晚上，可能只记得最后 2 个，前面 8 个就像从没说过一样。

这种 “金鱼记忆”，让 LLM 在处理长对话、复杂任务时特别吃力。

LLM “无限记忆”有什么好处：
- **长期陪伴**更贴心：AI 助手记住用户 3 年前提过的梦想职业，2 年前的过敏食物，甚至上周随口说的一句 “最近压力大”，下次聊天时能精准戳中需求。
- **复杂任务**更靠谱：做一个跨季度项目规划，AI 能记住每个阶段的进度、遇到的问题、合作方的要求，不会中途 “断片”；写一本长篇小说，它能牢牢抓住人物设定、剧情伏笔，避免前后矛盾。
- **个性化服务**更深入：学生用 AI 补习，它能记住你从高一到高三的知识漏洞，持续调整学习计划；职场人用 AI 处理工作，它能记住公司的流程、客户的习惯，像个 “老同事” 一样默契。

## Agent 记忆

Agent 记忆结构设计也借鉴了这些人类记忆特点。
- 短期记忆类似 受限于transformers**上下文窗口**的输入信息。
- 而长期记忆则类似于**外部向量存储**，Agent可以根据需要快速查询检索。

记忆来源: 智能体记忆内容的出处。

三种类型记忆来源:
- **内部任务信息**（Inside-trial Information）: 当前任务执行信息
  - 单个任务或交互过程中收集的数据。仅与当前正在进行的任务有关。
  - 一个对话人物, Agent 要记住上下文信息,以便生成连贯的回应
- **跨任务信息**（ Cross-trial Information ）: 历史任务重的长期积累学习
  - 跨越了多个任务或交互过程，它包括了Agent在不同任务中积累的经验、学到的教训以及可能的模式识别
  - 旅行计划中, Agent 从用户预订过的机票酒店,用户反馈 这类跨任务信息优化改进执行策略
- **外部知识**（External Knowledge）
  - Agent 与环境交互之外的信息。
  - 可能是通过API调用、数据库查询或访问在线资源（如维基百科）等方式获得的

对应到语言模型概念:
1. `感官记忆`作为原始输入（包括文本、图像或其他形式）的学习嵌入表征;
2. `短期记忆`是**上下文学习**（in-context learning），非常短且影响范围有限，受到Transformer的上下文窗口长度的限制。
3. `长期记忆`作为智能体在查询时可用的外部向量存储，可通过快速检索访问。

[我们离AGI还有多远：基座大模型的记忆](https://zhuanlan.zhihu.com/p/1892215026871428653)
- 【2025-3-31】[ADVANCES AND CHALLENGES IN FOUNDATION AGENTS](https://arxiv.org/pdf/2504.01990)

Meta的划分：
- `感觉记忆`（Sensory Memory）：同理感觉记忆应当为原始数据输入，即摄像头、麦克风等各种传感器获取到的原始信息。
- `短期记忆`（Short-Term Memory）：Meta认为短期记忆充当着连接感觉记忆和长期记忆的瞬时动态工作空间。同时短期记忆可以细分为上下文记忆和工作记忆。
  - 上下文记忆：通过感觉记忆处理得到的基础记忆
  - 工作记忆：对上下文记忆进行进一步操作得到的记忆
- `长期记忆`（Long-Term Memory）：这里Meta和人类记忆一样，将长期记忆分得很细，但是很明显不同研究的实现方式不一样，Meta将这些工作杂揉了起来。
  - **显式**记忆（Explicit Memory）：可被直接提取与使用的记忆
    - 语义记忆（Semantic Memory）：存储通用知识、事实、概念。比如，鱼含有蛋白质、刀在厨房
    - 情节记忆（Episodic Memory）：存储特定事件、交互历史、情境路径。从厨房走到客厅再走到花园
  - **隐式**记忆（Implicit Memory）：无需显式调用即可影响行为
    - 程序性记忆（Procedural Memory）：储存可复用的技能或执行计划；提升任务效率
    - 启动效应（Priming）：记录状态变化与响应模式，使智能体能快速做出合适反应

Agentic Memory
- [Cognitive Architectures for Language Agents](http://arxiv.org/abs/2309.02427)



### 感知记忆

Sensory Memory

`感知记忆`目前在大模型中缺失，更像模型输入，而非中间产物。

最简单的例子就是：好了伤疤忘了痛。

对于感官，很难将当时的信息保留下来。闭上眼睛，图像就没有了；捂上耳朵，声音就没有了。

即使是大模型内部思考，也还是明文思考，直接print出来，不知道大模型会不会不好意思。

大语言模型的问题尤为严重，因为编码后的文本是现实中不存在的事物，因此多模态模型不仅要考虑到将图片和问题统一到一个特征空间，还需要考虑他们本身不是一个维度的事物。

### 短期记忆


工作记忆 记录当前环境信息
- 最近的感知输入、活跃目标、及时反馈和内部推理信息。

Working memory reflects the agent’s current circumstances:
- • Recent perceptual input
- • Active goals
- • Results from intermediate, internal reasoning.

如何管理短期记忆
- 修剪(Trimming): 调用 LLM 前，简单移除对话历史的开头或结尾 N条消息。
- 总结(Summarization): 将早期对话内容进行总结，用一段摘要替换掉原始消息。
- 永久删除(PermanentDeletion): 从LangGraph 等框架的状态中彻底移除某些消息。
- 自定义策略(Custom Strategies): 如根据消息的重要性进行过滤，保留关键信息，删除不重要的闲聊。

### 长期记忆


Long-Term memory 长期记忆类型
- ❑ 程序记忆 Procedural memory: 存储系统本身信息
  - 定义智能体知道该怎么做的逻辑和流程，通常被 硬编码或通过学习 固化 在代码中。
  - stores the production system itself
- ❑ 语义记忆 Semantic memory: 存储环境事实知识
  - stores facts about the world
  - 存储与特定用户相关的过去交互和具体事件，是实现个性化和持续学习的关键。
- ❑ 情景记忆 Episodic memory：存储历史行为信息
  - stores sequences of the agent’s past behaviors
  - 存储关于世界的事实性知识，通常通过向量搜索或 RAG 从外部源获取并内化。


获取长期记忆最常见的方式是通过“语义搜索”。
- 用一个 embedding 模型，将所有的记忆文本都转化为一个向量。而后续跟模型的交互信息也可以通过同样的 embedding 模型转化为向量，计算相似度来找到最相似的记忆文本。最后再将这些记忆文本拼接到 prompt 里，作为模型的输入。
- ![](https://pic1.zhimg.com/80/v2-3742a095fdd75d3c3a66faecbb690575_1440w.webp?source=1940ef5c)
- 这类方法最热门的开源项目可以参考 OpenAI 官方的 [ChatGPT Retrieval Plugin](https://github.com/openai/chatgpt-retrieval-plugin) 和 Jerry Liu 的 [LlamaIndex](https://github.com/jerryjliu/llama_index)。

这种拓展模型记忆的模式相比人类大脑的运作方式来说感觉还有些“粗糙”，所谓的长期与短期记忆（包括 LangChain 与 LlamaIndex 中一些更复杂的实现），仍然是比较“hard coded”的感觉。如果未来在模型 context size 上有突破性的研究进展，那么当前的这类模式或许就不再需要了。


### 永久记忆


【2025-1-3】[“AI将在2025拥有永久记忆”，谷歌前 CEO 施密特预测道](https://mp.weixin.qq.com/s/lXHxivjZ3UGh9E_kIBgWKw)

前谷歌CEO埃里克·施密特（Eric Schmidt）在最近的预测中指出，未来几年内，人工智能（AI）将迎来三项革命性的突破，这些突破不仅有可能实现，而且其影响力“被低估而非高估”。

当前AI的上下文窗口相当于“短期记忆”。然而，2025年，AI将实现“永久记忆”，这将彻底改变其信息处理和存储的方式。

【2024-8-9】谷歌研究院最新发表的论文《Leave No Context Behind》提出了一种名为“无限注意力”的新方法，使AI能够像一个永不疲倦的助手，持续读取和记忆大量信息，只保留最关键的内容。
- 论文 [Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention](https://arxiv.org/pdf/2404.07143)
- [解读](https://zhuanlan.zhihu.com/p/692221106)

将基于transformer的大型语言模型（LLMs）扩展到**无限长的输入**，同时保持**有界**的内存和计算。
- 一个关键组成部分是一种新的注意力技术，称为 `Infini-attention`。
- Infini-attention将压缩记忆整合到传统的注意力机制中，并在单个变换器块中构建了掩蔽的局部注意力和长期的线性注意力机制。
- 在长上下文语言建模基准测试、1M序列长度的密钥上下文块检索和500K长度的书籍摘要任务上，使用1B和8B LLMs展示了我们方法的有效性。引入了最小有界的内存参数，并实现了LLMs的快速流式推理。

这种“永久记忆”技术将广泛应用于多个领域。

例如，教育领域的AI导师能够记住学生的学习进度和偏好，提供个性化的教学方案；医疗领域的AI助手可以长期跟踪患者的健康数据，提供持续的健康管理建议。此外，施密特预测，这项技术将在科学研究中发挥重要作用，帮助研究人员记住和整合大量文献和实验数据，加速科研进程。

## 记忆存储

记忆如何保存?

**记忆形式**:主要基于以下 4 种形式
- 语言
- 数据库
- 向量表示
- 列表

记忆格式上，可以**自然语言**或**嵌入向量**形式存储。

文本形式的记忆和参数形式的记忆同样也是各有千秋，它们适合不同的应用场景。
- 如果要快速回忆最近的对话，文本形式可能更合适；
- 而如果要存储大量知识，或者需要一个稳定可靠的知识库，参数形式可能更有优势。

各种记忆形式案例总结
- [Agent memory大揭秘:5种记忆形态，轻松拿捏](https://mp.weixin.qq.com/s?__biz=MzkxNjcyNTk2NA==&mid=2247483923&idx=1&sn=d83a98a68c8f3b1b7185f352832b085d)

### (1) 文本形式

分析
- 好处: 易于理解和实现，而且读写速度都很快。
- 但是，如果记忆太长，就会占用很多空间，影响处理速度。

文本形式记忆可进一步细分为几种类型:
- 存储完整的交互信息: ReAct
- 最近的交互信息
- 检索到的交互信息和外部知识。

MemGPT 分别体现出了短期和召回记忆；

Qwen-Agent中，通过 chatml 特有多轮格式`<im_start>` `<im_end>`进行分割历史的会话，最后一轮才加上ReAct的prompt。

### (2) 参数形式

这种方式更高级。不直接存储文字，而是把记忆转换成模型参数，就像是把知识压缩成精华。
- 好处: 不受文本长度限制，而且存储效率更高。
- 但是，写入时可能需要更多的计算，而且解释起来也不如文本形式直观。

参数形式的记忆则涉及更复杂的技术，比如: fine-tuning 和 editing。
- 微调可以帮助模型快速学习特定领域的知识
- 而知识编辑则可以精确地更新或删除某些记忆，避免影响其他无关的知识。

经典 [Character-LLM: A Trainable Agent for Role-Playing]()，用微调方式，


## 记忆原理


### 记忆流程

Agent通过**记忆阅读**、**记忆写入**和**记忆反思**三个关键操作与外部环境进行交互。
- 记忆阅读: 提取有意义的信息, 以增强Agent的行动；
- 记忆写入: 将感知到的环境信息存储在记忆中；
- 记忆反思: 模拟了人类审视和评估自己的认知、情感和行为过程的能力。

【2024-4-21】人民大学高瓴学院, Memory 设计综述 [A Survey on the Memory Mechanism of Large Language Model based Agents](https://arxiv.org/pdf/2404.13501)

人民大学关于memory设计的最新资料:[LLM_Agent_Memory_Survey](https://github.com/nuster1128/LLM_Agent_Memory_Survey)

【2024-8-13】[Agent memory大揭秘:轻松搞定记忆写入、管理、读取](https://mp.weixin.qq.com/s/67q1nLDXiB8ypHnIYk4VuA)

记忆操作像 LLM大脑，三个部分组成:记忆写入、记忆管理和记忆读取。
- 记忆写入: LLM短期记忆, 接收到新信息时(聊天),以特殊编码方式存入"大脑"
  - `MemGPT`: 自我指导是否写入记忆,智能体根据上下文决定是否更新
  - `MemoGPT`: 聊天时做总结, 提取对话片段的主题, 关键词形式保存,便于查找, topic,summary,dialogues
- 记忆管理: LLM长期记忆, 整理短期记忆信息;信息归类, 找出最重要的部分,忘掉次要信息,保持大脑的清晰、高效
  - `MemoryBank`: 智能体从对话内容中提炼每日大事记, 同时不断评估，生成个性特征
  - `Voyager`: 智能体根据环境反馈优化记忆
  - `Generative Agents`: 智能体自我反思，获取更高层次的信息. 从事件信息中生成抽象想法
  - `GITM`: 记忆模块中总结多个计划的关键行动, 建立各种情况下的共同参考计划, 提取最重要的行动步骤
- 记忆读取: 使用LLM记忆解决问题
  - `ChatDB`: SQL操作完成记忆阅读
  - `MPC`: 从记忆池里检索相关记忆, 使用思维链示例方式，忽略次要信息
  - `ExpeL`: 用Faiss向量库作为记忆池, 找出与当前任务最相似的k个成功示例.

### Agent 记忆机制

Agent 和大语言模型最大的不同: Agent 能够在环境中不断进行自我演化和自我学习；而这其中，记忆机制扮演了非常重要的角色。

从 3 个维度来分析 Agent 的记忆机制:
- （1）Agent 记忆机制设计, 常见有以下两种记忆机制:
  - 基于**向量检索**的记忆机制
  - 基于 **LLM 总结**的记忆机制
- （2）Agent 记忆能力评估，主要需要确定以下两点:
  - 评估指标
  - 评估场景
- （3）Agent 记忆机制演化分析:
  - 记忆机制的演化
  - 记忆机制的自主更新


#### 最大内积搜索 Maximum Inner Product Search (MIPS)

外部记忆可以缓解有限注意力span的限制，常用的操作是将信息嵌入表征保存到支持快速最大内积搜索（MIPS）的向量存储数据库中。

为了优化检索速度，一般都会选择近似最近邻（ANN，approximate nearest neighbors）算法返回前k个最近邻节点，牺牲一点准确性以换取巨大的速度提升。

常用的ANN算法包括: LSH（Locality-Sensitive Hashing），ANNOY, HNSW， FAISS, ScaNN

快速MIPS的几种常见ANN算法选择:[更多](https://ann-benchmarks.com/)
-   **[LSH](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Locality-sensitive_hashing)**（Locality-Sensitive Hashing）:它引入了一种哈希函数，使得相似的输入项在很大概率下被映射到相同的桶中，而桶的数量远远小于输入项的数量。
-   **[ANNOY](https://link.zhihu.com/?target=https%3A//github.com/spotify/annoy)**（Approximate Nearest Neighbors Oh Yeah）:核心数据结构是随机投影树，是一组二叉树，其中每个非叶节点表示将输入空间分成两半的超平面，每个叶节点存储一个数据点。树是独立且随机构建的，因此在某种程度上模拟了哈希函数。ANNOY搜索在所有树中进行，通过迭代搜索与查询最接近的一半，并汇总结果。这个想法与KD树有很大的关联，但可扩展性更强。
-   **[HNSW](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/1603.09320)**（Hierarchical Navigable Small World）:它受到小世界网络（ [small world networks](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Small-world_network)）的启发，其中大多数节点可以通过少数步骤到达任何其他节点；例如，社交网络中的“六度分隔”特性。HNSW构建了这些小世界图的分层结构，其中底层包含实际数据点。中间层创建了快捷方式以加快搜索速度。在执行搜索时，HNSW从顶层的随机节点开始，并向目标节点导航。当无法再靠近时，它会下降到下一层，直到达到底层。上层的每次移动都有可能在数据空间中覆盖较大的距离，而下层的每次移动则会提高搜索质量。
-   **[FAISS](https://link.zhihu.com/?target=https%3A//github.com/facebookresearch/faiss)**（Facebook AI Similarity Search）:它基于这样的假设，在高维空间中，节点之间的距离遵循高斯分布，因此应该存在数据点的聚类。FAISS通过将向量空间划分为聚类，并在聚类内部进行量化的方式来应用向量量化。搜索首先使用粗糙的量化方法寻找聚类候选项，然后再使用更精细的量化方法进一步查找每个聚类内的数据。
-   **[ScaNN](https://link.zhihu.com/?target=https%3A//github.com/google-research/google-research/tree/master/scann)**（Scalable Nearest Neighbors）:ScaNN的主要创新在于各向异性向量量化。它将数据点 $x_i$ 量化为 $\tilde{x}_i$ ，使得内积 $\langle q, x_i \rangle$ 尽可能与原始距离 $\angle q, \tilde{x}_i$ 相似，而不是选择最接近的量化质心点。




## 案例


各个 记忆实现案例 在以上版面的分布对比
- [Agent memory大揭秘:记忆从哪儿来？](https://mp.weixin.qq.com/s?__biz=MzkxNjcyNTk2NA==&mid=2247483916&idx=1&sn=4e72c6c675df1c5559aba88128cbd61b)

实际应用中
- 有些系统只模拟人类的**短期记忆**，通过上下文学习实现，记忆信息直接写在prompt中。
- 而有些系统则采用了hybird memory（**混合记忆架构**），明确模拟了人类的短期和长期记忆。**短期记忆**暂时缓冲**最近**的感知，而**长期记忆**则随着时间的推移巩固重要信息。

案例
- MemAgent
- MemOS
- Mem
- A-Mem


### 【2024-2-7】MEMORYLLM

记忆自动更新

[MEMORYLLM：可自我更新的大语言模型](https://zhuanlan.zhihu.com/p/706065398)

【2024-2-7】 Amazon、UC SD、UC LA
- 论文 [MEMORYLLM: Towards Self-Updatable Large Language Models](https://arxiv.org/pdf/2402.04624)

LLM 部署后通常保持**静态**，难以注入新知识。

目标
- 构建可自更新参数的模型，有效且高效地整合新知识。

MEMORYLLM 由一个transformer和transformer潜空间内固定大小的记忆池组成。

MEMORYLLM 可以使用文本知识进行**自我更新并记忆**先前注入的知识。

评估
- MEMORYLLM 能够有效地整合新知识
- 同时，该模型表现出**长期信息保留**能力。
- 操作完整性，即使在近一百万次记忆更新后也没有任何性能下降的迹象。

代码和模型已开源
- wangyu-ustc/MemoryLLM: The official implementation of the ICML 2024 paper "MemoryLLM: Towards Self-Updatable Large Language Models"

### 【2025-5-18】Mem0

自适应衰减

【2025-5-18】[再见RAG，这款让AI拥有超强记忆力的开源神器，绝了！](https://mp.weixin.qq.com/s/GOHcSyQipkA4GfgKBqxbvA)，含图解

Mem0 是一款为大型语言模型（LLM）设计的智能记忆层框架
- GitHub [mem0](https://github.com/mem0ai/mem0) 结合向量库检索、知识图谱检索、记忆衰减机制
- 2024年7月上线GitHub即引爆社区，两天斩获13K星，被开发者誉为"AI记忆革命的开源先锋"。
- 它能让AI记住用户的偏好、对话历史和操作习惯，像老朋友一样提供连续陪伴式服务，彻底打破传统AI"金鱼记忆"的局限。

核心功能
- 超强记忆网络
  - 通过用户级/会话级/代理级三级记忆体系，实现跨平台记忆联动。比如用户Alice在周一提及"喜欢打网球"，周三咨询运动课程时，AI能自动关联记忆推荐相关内容。
- 动态进化能力
  - 采用遗忘曲线算法，自动衰减过时信息（如三年前的工作习惯），强化高频使用数据（如最近偏好的咖啡口味），让记忆库像人类大脑般智能更新。
- 零代码接入
  - 提供5行Python极简API，开发者无需理解底层技术即可快速集成。
- 多模态记忆管理
  - 支持文本/图像/结构化数据混合存储，通过向量数据库+图数据库技术，实现"星巴克拿铁"→"咖啡偏好"→"周五消费习惯"的立体关联。
- 场景自适应
  - 在医疗场景自动强化病历记忆，在教育场景侧重学习进度跟踪，通过场景感知算法动态调整记忆权重，准确率达92%。

|模块|技术栈|功能亮点|
| ---- | ---- | ---- |
|记忆存储|Qdrant向量数据库|百万级数据毫秒检索|
|关系解析|Neo4j图数据库|构建用户-行为-场景关系网络|
|语义理解|GPT-4 Turbo|精准提取对话中的关键记忆点|
|记忆更新|自适应衰减算法|动态优化记忆权重|
|API网关|FastAPI框架|支持5000+QPS高并发请求| 

与 RAG 对比

|特性|Mem0|传统RAG|
| ---- | ---- | ---- |
|记忆时效|动态衰减更新|静态文档存储|
|关系理解|实体网络关联|关键词匹配|
|交互连续性|跨会话记忆延续|单次会话有效|
|个性化程度|自适应进化|固定模板响应|
|部署成本|支持增量学习|需全量数据重建|
|适用场景|长期陪伴型应用|短期问答场景| 



应用场景
- 虚拟伴侣养成计划
  - 记录用户的情感偏好和聊天习惯，当用户说"今天好累"时，AI不仅能安慰，还会提醒："上次你说听周杰伦的歌会放松，要播放《晴天》吗？"
- 智能客服升级方案
  - 在电商场景中，Mem0让客服机器人记住用户3天前的退货记录，当用户再次咨询时主动提示："您购买的XX商品已安排专人上门取件"。
- 个性化学习引擎
  - 通过记忆用户的知识薄弱点，当检测到用户多次拼错"accommodate"时，自动推送定制化练习题，记忆准确率提升73%。
- 医疗健康管家
  - 持续跟踪患者用药记录，在患者说"最近头晕"时，结合既往血压数据提醒："您上周收缩压140mmHg，建议优先复查心血管科"。
- 游戏AI革命
  - 在RPG游戏中，NPC会记住玩家三小时前救助村民的选择，在后续剧情中给出特殊奖励，使玩家留存率提升41%。
- 智能办公助手
  - 自动记忆会议纪要重点，当用户查询"Q2销售目标"时，直接调取最近三次会议数据生成对比图表。


以下代码实现记忆存储与调用：

```py
from mem0 import Memory
m = Memory()
m.add("用户每周五购买拿铁", user_id="tom")
print(m.search("推荐咖啡", user_id="tom"))  # 自动关联周五拿铁偏好
```


环境部署

```sh
# 安装核心库
pip install mem0ai
# 启动向量数据库
docker run -p 6333:6333 qdrant/qdrant
```

记忆管理实战


```py
from mem0 import Memory
memory = Memory()

# 添加记忆
memory.add("客户王总喜欢蓝山咖啡", user_id="VIP001")
# 智能检索
print(memory.search("王总的饮品偏好", user_id="VIP001"))
# 输出：蓝山咖啡（相似度0.93）
# 动态更新
memory.update(memory_id="m1", data="王总最近改喝低因咖啡")
```

配置

```py
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333}
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {"url": "neo4j://localhost:7687"}
    }
}
m = Memory.from_config(config)  # 支持多数据库联动
```

### 【2025-6-9】G-Memory

现有多智能体系统的问题
- 现有LLM多智能体系统（MAS）大多靠“一次性”流程或人工SOP，缺乏“自我进化”能力：本质是因为缺一套能跨任务、跨角色沉淀协作经验的记忆架构。


【2025-6-9】NUS、Tongji University、UCLA 等发布 G-Memory：LLM多智能体的"集体记忆"机制
- 论文标题：[G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems](https://arxiv.org/pdf/2506.07398)
- 代码 [GMemory](https://github.com/bingreeky/GMemory)

G-Memory 作为多智能体系统的“**集体记忆**”插件，结构化组织多智能体复杂记忆，让智能体从单任务执行者进化为跨任务专家。
	

即插即用
- 无需改现有框架，一行代码即可把AutoGen/DyLAN/MacNet升级为“会成长的团队”

#### 原理

G-Memory核心洞察

受“组织记忆理论”启发，把冗长的多智能体交互拆成三层图：
- Insight Graph：可迁移的高层策略
- Query Graph：任务之间的语义脉络
- Interaction Graph：细粒度对话轨迹

像公司知识库一样，既存“最佳实践”，也留“踩坑记录”。
	
双向往返记忆检索

收到新任务后：
- ① 向上遍历→提取通用经验（Insight）
- ② 向下遍历→找到相似任务的关键对话片段（Interaction）
- ③ 按角色个性化投喂，避免上下文爆炸。

#### 效果

核心实验简介
- 在5大基准+3类LLM+3个MAS框架上测试
- 具象任务成功率↑20.89%，知识问答准确率↑10.12%
- 额外token仅增加1.4M，远低于SOTA的2.2M
	

### 【2024-7-4】MemAgent

【2024-7-4】从 “记不住” 到 “忘不了”，MemAgent 可能不是简单地扩大内存，而是让 LLM 学会像人类一样 “管理记忆”。

字节跳动Seed团队与清华大学联合提出全新的长文本处理智能体——[MemAgent](https://memagent-sialab.github.io/)。

在别的方法还在绞尽脑汁**拉长上下文窗口**，或依赖人工设定**注意力规则**时，MemAgent另辟蹊径，通过**端到端强化学习**让智能体像人类一样"边读边记"，再基于最终记忆进行作答。

这一设计不仅实现了**线性**时间复杂度(`O(N)`)，还能在仅8K上下文长度训练的基础上，近乎无损外推至3.5M的问答任务(性能损失<5%)，并在512K的RULER测试中达到95%以上的准确率。

字节提出RL驱动的记忆智能体 MemAgent，开辟LLM长上下文解决新路径
- 主页 [MemAgent](https://memagent-sialab.github.io/)
- [MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent](https://arxiv.org/pdf/2507.02259)
- Github [MemAgent](https://github.com/BytedTsinghua-SIA/MemAgent)
- 解读 [https://news.qq.com/rain/a/20250709A08H4V00](https://news.qq.com/rain/a/20250709A08H4V00)

受人类处理长文档过程的启发，MemAgent会把长文章分成小块，每读完一段就记下重点，最后根据记住的内容回答问题。

具体来说，MemAgent 工作流分为两个阶段：
- 上下文处理模块中，模型每次接收一个文本块和当前记忆，通过提示模板迭代处理文本块并更新记忆；
- 当数据流处理完成后，最终的答案生成模块将仅依据问题陈述和记忆单元生成最终答案。

![](https://memagent-sialab.github.io/figs/method_00.png)

更新记忆的过程是**覆盖式**

论文将**记忆覆盖决策**构建为强化学习问题：智能体因保留有用信息或剔除冗余内容而获得奖励。通过新提出的 `Multi-Conv DAPO` 算法优化该目标，使模型能够学会在保持答案关键事实的前提下进行极致压缩。
- ![](https://memagent-sialab.github.io/figs/algo_00.png)

训练流程
- **多轮对话**训练机制：对于每个输入样本，模型生成多次回答，每次回答的输入不是此前的生成轨迹的拼接，而是**当前文本块**和**最新记忆状态**。
- **奖励计算**：从最后一轮回答中提取最终答案，使用基于规则的结果奖励并通过组归一化计算优势，将其分配到所有关联对话。
- **优化策略**：以每轮对话为优化目标，根据其优势计算类 DAPO 的token-level平均损失。损失计算维度从传统的(group, token)结构扩展至(group, conversation, token）。

论文使用 Qwen2.5-7B-Instruct、Qwen2.5-14B-Instruct 模型作为智能体的基座模型，并在7K至896K上下文长度范围内对基线模型的性能进行对比分析。

实验结果表明：
- MemAgent 在7K至3.5M的上下文范围内展现出卓越的外推能力，性能仅轻微衰减，验证了记忆机制与强化学习相结合的有效性；
- 基线模型即使在预设窗口内也表现不佳，难以有效利用超长上下文信息。

字节 MemAgent 详细技术细节未知，但从 “无限记忆” 核心点推测：
- 给记忆分个 “**优先级**”：就像人，把重要的事情记在笔记本上，不重要的随口忘。
  - MemAgent 可能会自动判断哪些信息是关键（比如用户反复提到的偏好、任务的核心目标），重点保存；次要信息则压缩或归档，需要时再 “调出来”。
- 搭个 “**外部记忆库**”：不再只依赖模型自身的 “短期内存”，而是把信息存在专门的数据库里。
  - 比如半年前跟 AI 说过 “不爱吃香菜”，这个信息会被存在库里，下次点外卖时，AI 能立刻从库里找到这个偏好。
- 学会 “**总结**和**关联**”：面对海量信息，它可能会像人类一样做笔记 —— 把连续的对话提炼成**要点**，把分散的信息串联起来（比如 “用户提到孩子 3 岁 + 喜欢恐龙，上周说想周末去博物馆”，会关联成 “推荐恐龙主题博物馆”）。

### 【2025-2-17】A-Mem

现有记忆系统主要支持基本的存储与检索功能，缺乏对记忆的**高级组织能力**。

即使有些系统引入图数据库进行结构化存储，这些系统的操作和结构通常是固定的，缺乏适应多样任务的灵活性。

【2025-2-17】美国罗格斯大学和公司AIOS Foundation 推出 `A-MEM` —— 一种新的 Agentic Memory 系统，以智能体的方式动态组织记忆。
- 论文 [A-MEM: Agentic Memory for LLM Agents](https://arxiv.org/pdf/2502.12110)
- 代码 [A-mem-sys](https://github.com/WujiangXu/A-mem-sys)
- 已集成到 [AIOS]([aios.foundation](https://aios.foundation/)): AI Agent Operating System
- 解读 [A-MEM -- Agentic Memory(动态的组织记忆)](https://zhuanlan.zhihu.com/p/1919431846237823495)


借鉴 Zettelkasten 方法：通过动态索引与链接，构建一个互联的知识网络。

#### 原理

系统机制概述
- 当添加一条新记忆时，系统会生成一条包含多个结构化属性的“笔记”，包括：
  - 上下文描述（contextual descriptions）
  - 关键词（keywords）
  - 标签（tags）
- 系统分析历史记忆，识别相关连接并建立链接。
- 新记忆还可能触发历史记忆的上下文更新与属性变化，实现记忆的持续演化。

关键机制优势

A-MEM 将 Zettelkasten 结构化理念与 LLM 智能体的自主决策能力结合，具备：
- 自主构建上下文表示
- 动态建立记忆之间的联系
- 实现旧记忆的智能演化更新
- 支持更强的适应性与上下文感知能力

#### 效果

A-MEM 在多个基准任务上相较于现有 SOTA 方法具有显著性能提升。



### 【2025-7-15】MEMOS

【2025-7-15】[RAG已死，请停止给LLM打“短期记忆补丁”！](https://x.com/ShenHuang_/status/1944540933275693137?s=19)

讲个内幕：
- 现在市面上绝大多数所谓LLM“**长期记忆**”方案，包括RAG，本质都是**临时工**。

解决了“**知识获取**”问题，但没解决“**记忆管理**”的根本难题，导致AI依然健忘、无法个性化，数据被困在各个应用里形成“记忆孤岛” 。

一直在给漏水的坝打补丁，而不是建一个真正的水库。

核心短板：**缺乏持久记忆机制**，导致AI无法像人类一样长期学习和积累经验。

关于LLM内存的论文： MEMOS，一个真正的AI“内存操作系统” 。

【2025-7-4】上交、同济、浙大、中科大、人大联手发布
- MemOS：全球首个赋予AI类人记忆的操作系统
- 论文 [MemOS: A Memory OS for Al System](https://arxiv.org/pdf/2507.03724)
- 项目[官网](https://memos.openmem.net) 
- 项目[论文](https://memos.openmem.net/paper_memos_v2 )
- 代码仓库：[MemOS Discord](https://github.com/MemTensor/MemOS Discord) 

它的思想完全是降维打击：
1. 统一管理: 创造了一个叫 MemCube 的标准单元 ，把参数 (固有知识)、KV缓存 (工作记忆)、外部明文 (瞬时知识) 三种形态的记忆全部统一管理 。
2. OS级调度: 像Windows/Linux调度硬件一样，MEMOS调度、融合、迁移这些MemCube，让LLM第一次拥有了可控、可塑、可持续进化的记忆 。

效果惊人： 
- 在LOCOMO基准上，性能全面碾压LangMem, Zep, OpenAI Memory等一众对手 。
- KV缓存加速技术，能把TTFT（首字输出时间）缩短最高 91.4% ！

这已经不是简单的技术优化，而是迈向“记忆训练” (Mem-training) 的范式革命 。

项目已开源，对于任何一个想构建真正有状态、能持续进化的AI Agent的开发者来说，非常建议读一下。

无状态AI的时代大概率要结束了。


### 【2025-7-16】MIRIX

当前的大模型记忆系统，有几个比较明显的**局限性**：
- 一是分类太少。所有记忆都存到一起，不好检索
- 二是多模态不行。以文本为核心的记忆机制，遇上图片之类的就不好使
- 三是不够灵活。总是整存整取，不压缩，存储空间占用大。

为了解决上述三个问题，MIRIX 模块化记忆系统把记忆精细地分成了六种类型（图3）：核心、情节、语义、过程、资源和知识库。这样做优势明显：
- 不同类型记忆服务于不同目的，能针对性检索（解决问题一）
- 资源记忆等模块支持多模态输入（解决问题二）
- 信息经过了抽象与压缩（解决问题三）。
	
除了传统问题，还设计了一套主动检索机制（图4）来保证记忆的有效性。这套机制让模型接收新任务时，能自动生成查询主题，并主动根据主题去检索记忆。确保模型自觉调用最新的相关信息，不像Mem0之类的记忆系统，必须直接告诉它要检索记忆，否则它更倾向于用预训练时记住的过时信息来回答。

【2025-7-16】[MIRIX：多模态、多智能体的分层记忆系统](https://zhuanlan.zhihu.com/p/1928787696622473952)
- 【2025-7-10】UCSD是美国加利福尼亚大学圣迭戈分校 论文 [MIRIX: Multi-Agent Memory System for LLM-Based Agents](https://arxiv.org/pdf/2507.07957)
- 主页 [MIRIX](https://mirix.io/)

当前 LLM 智能体在记忆能力上存在根本性限制，主要体现在**记忆扁平化**、**范围狭窄**且**难以处理多模态信息**，导致缺乏个性化和可靠的长期记忆。

MIRIX，模块化、多智能体协作的记忆系统。
- 引入了六种结构化记忆类型：核心记忆、情景记忆、语义记忆、程序记忆、资源记忆和知识金库，并配合多智能体框架动态管理记忆的更新与检索。
- ![](https://pic2.zhimg.com/v2-a6d04fce439a05e72ae948d763c1971d_1440w.jpg)
- 该设计使得智能体能够持久化、推理并准确检索多样化的长期用户数据，且支持丰富的视觉和多模态体验。

实验证明，MIRIX 在处理
- 高分辨率截图的多模态基准 ScreenshotVQA 上，准确率比现有 RAG 基线高出 **35%** 并显著降低存储需求；
- 长篇对话基准 LOCOMO 上，也取得了 85.4% 的 SOTA 表现。

MIRIX 为 LLM 智能体的记忆能力树立了新标准，并提供了实际应用。




### 【2025-7-25】LVMM


【2025-7-25】前Meta研究员、剑桥大学计算机科学博士创立的AI研究实验室[Memories AI]()正式发布，推出了全球首个人工智能大型视觉记忆模型（Large Visual Memory Model，简称`LVMM`）。

这一突破性技术旨在赋予AI类人般的**视觉记忆能力**，让机器能够像人类一样“看到、理解并记住”视觉信息。

同时，Memories AI宣布完成由Susa Ventures领投的800万美元种子轮融资，标志着其在AI视觉记忆领域的雄心壮志。

#### 原理

Memories AI 核心技术
- 独创的大型视觉记忆模型（LVMM）

业内首个能够持续捕获、存储和回忆**视觉信息**的AI架构。 

与现有AI系统不同，传统模型通常只能处理**短时视频片段** (15-60分钟)，在长时间视频分析中会丢失上下文，导致无法回答“之前是否见过这个?”或“昨天发生了什么变化?”等问题。 

而 LVMM 通过**模拟**人类记忆机制，能够处理长达数百万小时的视频数据，构建持久、可搜索的视觉记忆库。

通过三层架构实现:
- 首先对视频进行降噪和压缩，提取关键信息;
- 其次创建可搜索的**索引层**，支持自然语言查询;
- 最后通过**聚合层**将视觉数据结构化，使AI能够识别模式、保留上下文并进行跨时间比较。

这使得 Memories AI 在处理大规模视频数据时，展现出前所未有的效率和准确性，号称比现有技术高出100倍的视频记忆容量。

#### 应用场景

涵盖以下场景:
- 物理安全:为安防公司提供异常检测功能，通过分析长时间监控视频，快速发现潜在威胁。
- 媒体与营销:帮助营销团队分析社交媒体上的海量视频内容，识别品牌提及、消费者趋势和情感倾向。例如，某社交媒体平台已利用Memories AI技术洞察TikTok等平台的长期趋势，保持竞争优势。
- 机器人与自动驾驶:通过赋予AI长期视觉记忆，支持机器人执行复杂任务，或帮助自动驾驶汽车记住不同路线的视觉信息。

Memories AI的平台支持通过API或聊天机器人网页应用访问，用户可以上传视频或连接自己的视频库，通过自然语言查询视频内容。这种灵活的交互方式使其适用于从企业级解决方案到个人化应用的广泛场景。






# 结束

