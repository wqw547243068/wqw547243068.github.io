---
layout: post
title:  上下文工程指南
date:   2025-06-27 16:52:00
categories: 大模型
tags: prompt 大模型 context 
excerpt: 提示工程、Agent不管用？试试 上下文工程
mathjax: true
permalink: /context
---

* content
{:toc}

# 上下文工程

早期`提示工程`（Prompt Engineering），即如何巧妙地向模型提问，迅速转向一个更进阶的领域——`上下文工程`（Context Engineering）。

## 资料

- LangChain 官方博客文章《[The Rise of "context engineering"](https://blog.langchain.com/the-rise-of-context-engineering/)》
- 【2025-6-24】解读 [LangChain官方分享LLM的“上下文工程”技巧](https://zhuanlan.zhihu.com/p/1920981931920693117)


## 背景


使用LLM 智能体（Agent）时，常常遇到棘手问题：
- 为什么智能体表现如此不稳定？

习惯性归咎于模型本身不够强大。

然而，问题根源：未能向模型提供**恰当上下文**。
- 当一个智能体无法可靠地执行任务时，其根本原因通常是未能以正确的格式向模型传递正确的**信息、指令和工具**。

随着LLM应用从单一`提示词`演变为复杂的、动态的`智能体系统`，“上下文工程”（Context Engineering）正迅速成为AI工程师需要掌握的重要技能。

Cognition 团队核心观点
> “再聪明的模型，若不知上下文，也无法做出正确判断。” 


### LLM 失败

智能体系统的失误，本质是 **LLM 失误**。

从第一性原理分析，LLM 失败主要源于两个方面：
- **底层模型能力不足**，无法正确推理或执行。
- 模型缺少正确判断所需的**上下文**。

随着模型能力的飞速发展，第二点正成为更普遍的瓶颈。

上下文供给不足主要体现在：
- 信息缺失：模型完成任务所依赖的关键信息未被提供。
- 格式混乱：信息虽然存在，但其组织和呈现方式不佳，阻碍了模型的有效理解。

### 提示词 → 上下文

大模型应用技术从“**提示词艺术**”迈向“**上下文科学**”。

最近爆品，如Cursor，Manus等产品都表明
- 一个卓越的大模型产品，背后必然是精心设计的**上下文工程系统**。

未来的核心竞争力，不再是精妙的**提示词**，更是高质量、高效率的**上下文**。

通过精心组织，为模型提供事实依据、注入持久记忆、并扩展其行动能力，有可能释放大模型的潜力，构建出新的有价值AI产品。

## 定义

上下文工程
- 构建动态系统，以正确格式提供合适的信息和工具，使 LLM 能够合理地完成任务。

### 上下文工程

上下文工程（Context Engineering）核心定义：
- 构建一个**动态系统**，以正确格式提供正确的信息和工具，从而使大语言模型（LLM）能够可靠地完成指定任务。

深入理解：
- **系统工程**：复杂智能体从多个来源获取上下文，包括开发者预设、用户输入、历史交互、工具调用结果以及外部数据。将这些信息源有机地整合起来，本身就是一个复杂的系统工程。
- **动态变化**：上下文组成部分很多是实时生成。最终输入给模型的提示（Prompt）也必须是动态构建的，而非静态的模板。
- **信息精准**：智能体系统失败的原因之一是上下文信息缺失。LLM 无法“读心”，必须为其提供完成任务所需的全部信息。所谓“垃圾进，垃圾出”，信息质量直接决定输出质量。
- **工具适用**：很多任务无法仅靠初始信息完成。为 LLM 配备合适的工具就变得至关重要，用于信息检索、执行动作或与其他系统交互。提供正确的工具与提供正确的信息同等重要。
- 强调**格式规范**：与 LLM 的“沟通方式”跟人一样关键。简洁明了的错误信息远胜于一个庞杂 JSON 数据块。工具的参数设计、数据的呈现格式，都会显著影响 LLM 的理解和使用效率。
- **任务可行性**：设计系统时，应反复自问：“在当前提供的上下文和工具下，LLM 是否真的有可能完成任务？” 便于归因分析，上下文不足，还是模型本身的执行失误，从而采取不同的优化策略。


### 图解

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;dark-mode&quot;:&quot;auto&quot;,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36\&quot; version=\&quot;27.1.6\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;R7sKukqaU0FvSahdFvPL\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;660\&quot; dy=\&quot;526\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-80\&quot; value=\&quot;上下文工程&amp;lt;div&amp;gt;Context Engineering&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1;fontSize=15;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;300\&quot; y=\&quot;40\&quot; width=\&quot;160\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-81\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;140\&quot; y=\&quot;130\&quot; width=\&quot;430\&quot; height=\&quot;300\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-82\&quot; value=\&quot;上下文工程&amp;lt;div&amp;gt;Context Engineering&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=0;fontSize=15;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;275\&quot; y=\&quot;150\&quot; width=\&quot;160\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-83\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;opacity=60;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;300\&quot; y=\&quot;190\&quot; width=\&quot;150\&quot; height=\&quot;110\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-84\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;opacity=60;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; y=\&quot;200\&quot; width=\&quot;170\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-85\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;opacity=60;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;310\&quot; y=\&quot;260\&quot; width=\&quot;110\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-86\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;opacity=60;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380\&quot; y=\&quot;190\&quot; width=\&quot;140\&quot; height=\&quot;130\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-87\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;shadow=1;opacity=60;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;100\&quot; y=\&quot;290\&quot; width=\&quot;160\&quot; height=\&quot;140\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-88\&quot; value=\&quot;结构化输出&amp;lt;div&amp;gt;Structured Outputs&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=0;fontSize=15;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;90\&quot; y=\&quot;320\&quot; width=\&quot;160\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-89\&quot; value=\&quot;提示工程&amp;lt;div&amp;gt;Prompt Engineering&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=0;fontSize=15;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; y=\&quot;230\&quot; width=\&quot;160\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-90\&quot; value=\&quot;RAG\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=0;fontSize=15;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;332.5\&quot; y=\&quot;190\&quot; width=\&quot;65\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-91\&quot; value=\&quot;状态历史&amp;lt;div&amp;gt;State History&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=0;fontSize=15;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;450\&quot; y=\&quot;265\&quot; width=\&quot;105\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UE00E24gimm2ZRSZMZkB-92\&quot; value=\&quot;记忆&amp;lt;div&amp;gt;Memory&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=0;fontSize=15;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;335\&quot; y=\&quot;320\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



### 提示工程 vs 上下文工程

为什么从“提示工程”（Prompt Engineering）转向“上下文工程”？

LLM应用早期，开发者专注于通过**巧妙措辞**诱导模型给出更好的答案。

但随着应用变得越来越复杂，共识逐渐形成：
- 向AI提供**完整和结构化的上下文**，远比任何“魔法般”的措辞都重要。

`提示工程`是`上下文工程`的子集。

即使有全部上下文信息，提示词组织、编排方式，仍然至关重要——提示工程范畴。

核心区别：
- `上下文工程`：设计架构，动态地收集、筛选和整合来自多源的数据，构建出完整的上下文。
- `提示工程`：已有上下文的基础上，设计格式化和指令，以最优方式与LLM沟通。
- ![](https://pic3.zhimg.com/v2-649720ac409cd7a74ca6167707f64cc4_1440w.jpg)

不同于传统 Prompt Engineering，Context Engineering 更关注系统级的**动态上下文构建**。
- 强调：在复杂交互和多智能体协作中，如何为每个 Agent 构建精准、独立、可持续的任务背景，是系统能否稳定运行的关键。



## 构成


上下文系统由多个关键部分组成
- ![](https://picx.zhimg.com/v2-a7f4161b98afb00462a67c37cffa4117_1440w.jpg)


上下文工程是一个动态系统

复杂的智能体系统从**多个来源**获取上下文：
- 应用开发者：预设的系统指令和行为准则。
- 用户：当前任务的直接输入和要求。
- 历史交互：先前对话的记忆或摘要。
- 工具调用：通过API或函数调用获取的外部信息。
- 外部数据：从数据库或知识库中检索的文档。

将所有这些信息整合在一起，需要一个复杂的系统。
1. 提供正确的信息与工具
2. 格式化至关重要
3. 自检：反复确认信息是否充分

而且必须动态，因为许多上下文信息是实时变化的。

因此，最终交付给LLM的提示词（Prompt）不是静态模板，而是由动态逻辑**实时构建**的。

好的上下文工程应该包括：
- 工具使用：当一个智能体访问外部信息时，需要拥有能够访问这些信息的工具。当工具返回信息时，需要以 LLM 最容易理解的方式对其进行格式化。
- 短期记忆：如果对话持续一段时间，可以创建对话摘要，并在未来使用该摘要。
- 长期记忆：如果用户在之前的对话中表达了偏好，需要获取这些信息。
- 提示工程：在提示中清楚地列举智能体应该如何操作的说明。
- 检索：动态地获取信息，并在调用 LLM 之前将其插入到提示中。

### 正确的信息与工具

LLM 应用失败常见原因：**上下文缺失**。

LLM无法读取用户思想，如果不提供完成任务所需的关键信息，不可能知道这些信息的存在。
- “垃圾进，垃圾出”（Garbage in, garbage out）原则。

同样，仅有**信息**可能还不够。

在很多场景下，LLM需要借助**工具**来查询更多信息或执行某些动作。为LLM提供正确的工具，与提供正确的信息同等重要。

### 格式化至关重要

与人类沟通类似，如何向LLM传递信息，其格式会极大地影响结果。

一个简短但描述清晰的错误信息，远比一个庞大而杂乱的JSON数据块更容易让LLM理解和处理。这一点同样适用于工具的设计，工具的输入参数是否清晰、易于理解，直接决定了LLM能否有效使用。

### 自检

进行上下文工程时，反复确认：
- “以当前提供的上下文，LLM真的能合理地完成任务吗？”

这个问题能保持清醒，认识到LLM不是万能的，要为创造条件。同时，有助于区分两种主要的失败模式：
- 失败模式一：没有提供足够或正确的信息/工具，导致LLM失败。
- 失败模式二：提供了所有必要的信息和工具，但LLM自身出现了推理错误。

这两种失败模式的修复方案截然不同，准确定位问题是优化的第一步。


## 应用


优秀的上下文工程实践：
- 工具使用（Tool Use）：确保必要时能访问外部信息，并为工具设计易于LLM理解的输入参数和输出格式。
- 短期记忆（Short-term Memory）：持续多轮对话中，**动态**创建**对话摘要**，并将其作为后续交互的上下文，防止信息丢失。
- 长期记忆（Long-term Memory）：当历史对话中包含用户特定偏好时，系统能够**自动**获取这些信息，并在新对话中加以利用。
- 提示工程（Prompt Engineering）：提示词清晰地列出智能体应遵循的行为准则和详细指令。
- 检索（Retrieval）：调用LLM之前，根据用户查询动态地从知识库（如向量数据库）中获取相关信息，并将其注入到提示词中。

两者却不约而同指出：要让多智能体系统稳定运行，有两个关键前提：
- Context Engineering（上下文工程）是基础设施级能力
- 多智能体更适合“读”任务而非“写”任务

结语：别被“智能体数量”迷惑，关键是上下文控制力
- Cognition 的告诫并非“多智能体无用”，而是警示其复杂性；
- Anthropic 的成功并非“多智能体万能”，而是源于良好的任务拆解与上下文管理；
构建多智能体系统不仅是技术挑战，更是“系统工程挑战”。

### Cognition

Cognition 团队总结
- 多 Agent 写作风险: “行为背后是决策，冲突的决策会带来灾难。” 
- 再聪明的模型，若不知上下文，也无法做出正确判断。

读 vs 写，本质区别在哪？
- 读（Research）型任务：如搜索信息、理解材料等，天然适合并行执行，多个 Agent 各自探索、协同处理即可。
- 写（Synthesis）型任务：如代码生成、内容撰写，需保持结构统一、语言风格一致，难以拆分并行，否则会产生冲突或碎片化。


### Anthropic

Anthropic 实践：
- **长对话管理**：对话可能长达数百轮，需要引入**外部记忆**与**压缩机制**，如在每阶段总结信息存储进记忆库、跨阶段切换时唤回关键信息。
- **任务描述精准化**：子智能体需要被明确告知目标、输出格式、所用工具、边界约束，否则容易重复劳动或遗漏重要内容。

底层能力支持
- ✅ 完整控制 LLM 接收的上下文输入
- ✅ 无隐藏提示、无强加的“认知架构”
- ✅ 明确每一步执行顺序，实现灵活编排

Claude Research 系统中：
- 读取任务：由多智能体并行完成，每个 Agent 负责不同方向
- 写作任务：由主智能体统一汇总并输出，避免冲突与割裂

模糊指令导致多个 Agent 重复搜索 2025 年半导体供应链，**有效的任务拆解机制**是防止资源浪费的关键。

Agent 框架核心不是功能丰富，而是给开发者“上下文的完全控制权”。

多智能体系统适合任务：
- ✅ 高价值任务：计算成本可控，但任务本身价值高（如战略研究）
- ✅ 广度优先探索：适合多个 Agent 并行发散，如舆情分析、多角度政策解读
- ✅ 超长上下文任务：任务 token 超过单模型窗口上限时，可用 Agent 分工处理各部分

而在以下场景中，**多智能体**反而不如**单体结构**高效：
- ❌ 强依赖上下文同步、实时响应（如代码协作、系统集成）
- ❌ 子任务之间依赖复杂、无法并行（如多步骤推理题）


没有通用最佳结构，只有最合适的架构决策。

作者：[AI小智](https://juejin.cn/post/7516810298902544393)



### LangChain

LangChain 生态两个核心工具——`LangGraph`和`LangSmith`——为实践上下文工程提供了强大的支持。
- LangGraph 用于构建可控智能体框架的库。设计理念与上下文工程完美契合，因为赋予了开发者完全的控制权。
- LangSmith 是 LangChain 的 LLM应用可观测性（Observability）和评估解决方案。核心功能——**调用链路追踪**——是调试上下文工程问题的利器。

![](https://pic1.zhimg.com/v2-9bbcc0a0b73ed27eb21c531919329c46_1440w.jpg)

### Cursor


待定

# 结束