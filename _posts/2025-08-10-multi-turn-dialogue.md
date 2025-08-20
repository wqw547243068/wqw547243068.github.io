---
layout: post
title:  大模型多轮会话
date:   2025-08-10 11:47:00
categories: 大模型 对话系统 agent mermaid 
excerpt : 大模型如何实现任务型多轮会话？
tags: 多轮
permalink: /multi-turn
mathjax: true
---

* content
{:toc}

# 多轮对话

AI 智能体正从**单点能力**迈向**复杂系统协作**，多智能体系统（Multi-Agent Systems, MAS）成为学术和产业界聚焦的新前沿。

这一背景下，「Agentic Workflow」作为面向智能体自主决策与协作流程自动生成的技术理念，正成为多智能体系统研究和应用的探索热点。

## 背景

多轮对话知识见站内专题：[对话管理器](dialogue-manager)


### workflow 自动化

为了提升智能体系统的自主化与智能化，谷歌、上海 AI Lab 等国内外领先团队陆续推出了 `Meta-GPT`、`ADAS`、`AFlow` 等创新性 Agentic Workflow 工作，大力推动利用大模型实现任务规划、分工协作与流程优化的自动化进程。

尽管这些系统能够灵活的表达工作流，但在自动化搜索工作流的过程中，存在：**合理性难以保证**、**可验证性不足**、 **难以直观表达**等突出挑战，严重制约了多智能体系统的可靠落地与规模化部署。


## 论文

论文合集: 大模型多轮交互相关的数据、论文、代码
- 【2025-4-7】CMU 综述论文 [Beyond Single-Turn: A Survey on Multi-Turn Interactions with Large Language Models](https://arxiv.org/pdf/2504.04717)，涉及多个场景的多轮会话，roleplay, healthcare, education, and even adversarial jailbreak settings
- [Awesome-Multi-Turn-LLMs](https://github.com/yubol-bobo/Awesome-Multi-Turn-LLMs)

此外，多轮对话场景下增强方法：
- **模型中心策略**: 上下文学习、监督微调、强化学习及新型架构；
- **外部集成方法**: 记忆增强、基于检索的方法及知识图谱；
- 用于协作交互的**基于智能体的技术**。


### Google

【2025-7-17】[Learning to Clarify: Multi-turn Conversations with Action-Based Contrastive Self-Training](https://arxiv.org/pdf/2406.00222)


用人类反馈优化大模型（LLMs）已成为智能对话助手的主流范式。

然而，基于LLM的智能体在**对话技能**方面仍有欠缺
- 歧义消除能力——信息模糊时，往往含糊其辞或暗自猜测用户的真实意图，而非主动提出澄清问题。
- 在特定任务场景中，**高质量的对话样本数量有限**

这成为限制LLMs学习最优对话行动策略的瓶颈。

**基于行动的对比自训练（ACT）** 算法，基于直接偏好优化（DPO）的准在线偏好优化算法，在多轮对话建模中实现数据高效的对话策略学习。

通过真实对话任务验证ACT在数据高效调优场景中的有效性，即使在没有行动标签的情况下依然表现优异，这些任务包括：表格驱动的问答、机器阅读理解，以及AmbigSQL（一种面向数据分析智能体的新型任务，用于消除复杂SQL生成中信息查询请求的歧义）。

此外，还提出评估LLMs作为对话智能体能力的方法
- 通过检验能否在对话中隐性识别并推理歧义信息。
- 结果表明，与监督微调、DPO等标准调优方法相比，ACT在对话建模方面有显著提升。


## 【2025-5-29】MermaidFlow

【2025-7-24】[如何实现可验证的Agentic Workflow？MermaidFlow开启安全、稳健的智能体流程新范式](https://zhuanlan.zhihu.com/p/1931767220997981459)

【2025-5-29】新加坡 `A*STAR` 的 Centre for Frontier AI Research (CFAR) 研究所与南洋理工大学的研究团队联合发布了创新性工作流框架「MermaidFlow」，推动智能体系统迈向结构化进化与安全可验证的新范式。
- 论文 [MermaidFlow: Redefining Agentic Workflow Generation via Safety-Constrained Evolutionary Programming](https://arxiv.org/pdf/2505.22967)
- 代码 [MermaidFlow](https://github.com/chengqiArchy/MermaidFlow)

MermaidFlow 提出的结构化可验证工作流表达方式，为智能体系统实现高效、可控的协作流程提供了基础支撑。未来的 AI 协作，也许正需要这样一套 「看得见、查得清、能进化」 的流程底座。


### 起因

传统瓶颈：命令式脚本使工作流频频 「翻车」

现有多智能体系统中，大模型生成的工作流往往以 **Python 脚本**或 **JSON 树**等命令式（imperative）代码直接输出
- `ADAS`, `AFlow` 等主流系统也普遍采用了这种表达范式。

这种低层次、混杂的生成方式，将流程规划与具体实现深度耦合，结构信息隐含在复杂代码中，直接导致了以下三大核心瓶颈：
- 结构不透明：工作流整体架构深藏在杂乱代码里，流程关系难以一目了然，协作全局难以把控。
- 合理性难验证：流程逻辑与实现细节高度耦合，缺乏静态检查和自动验证机制，容易隐藏致命漏洞。
- 调试与优化困难：错误往往只有在实际运行时才暴露，流程复现、问题定位和后续优化极为低效。

### MermaidFlow 方法

MermaidFlow: 引领结构化与可验证工作流表达

MermaidFlow 以 **结构化图语言** `Mermaid` 为基础，提出全新的工作流表达机制。

不同于直接输出可执行脚本的方式，MermaidFlow 强调将智能体行为规划过程**显式**建模为**结构化流程图谱**，并引入形式化语义，确保流程清晰、可查、可验证。

相比传统的 Python/JSON 脚本，基于 Mermaid 的工作流表达具有以下核心特点：
- 图式结构清晰可见：每一个智能体定义、依赖关系、数据流都被结构化地表达成图中的节点与连边，使整个工作流一目了然、可交互、可审查.
- 流程验证内嵌其中：MermaidFlow 引入了多类语义约束（如依赖闭环、角色一致性、输入输出类型匹配等），支持静态结构验证与生成时一致性检查，避免生成不符合规则的图。
- 天然支持演化与调试：结构化工作流图更易于进行片段级替换、增量修复与版本比较，支持可控的演化式优化（见后节）。

![](https://pic4.zhimg.com/v2-a72520c51dbc177d5b29cea84eec091b_1440w.jpg)

MermaidFlow：从结构化图到可验证执行的一站式工作流表达闭环 。 
- 左侧部分展示了基于 Mermaid 的声明式工作流表达，结构清晰、依赖显式，具备良好的人类可读性。
- 人们可以清晰得知道, 在该工作流中存在什么节点, 之间的连接情况是怎么样的。

借助 MermaidFlow 所提出的结构化图式表达，多智能体协作的工作流规划过程不再是脆弱难控的**黑盒编排**，而是具备清晰结构、可视节点与可验证语义的 「**白盒流程**」。

这种方式极大地提升了 Agentic Workflow 的可解释性、可验证性与后续演化的可操作性，为大规模部署打下坚实基础。

作者研究发现大语言模型对 Mermaid 语言具备天然的生成优势。这也让 MermaidFlow 与 LLM 的结合变得格外丝滑又强大 

工作流的自我升级之道

MermaidFlow 基于 Mermaid 语言对智能体工作流进行显式建模，使每个任务节点、数据依赖与执行顺序都成为可视、可解析、可操作的语义单元。
- 相比传统的命令式脚本，结构化表达更具模块化特性，支持按节点插入、删除与替换，天然适配图级别的优化操作。
- 每一次结构调整都具备清晰的语义边界，显著降低了修改的不确定性与调试复杂度。

得益于 MermaidFlow 引入的静态验证机制（如节点类型匹配、输入输出闭环、角色一致性等约束），每一代演化生成的工作流候选都能在生成阶段就进行结构合规性检查，过滤掉语义不完整或存在潜在风险的 「劣质图」。

这种 「先验校验 + 后验优化」 的策略，显著提高了搜索空间的质量和鲁棒性，避免了大量无效或不合法的探索路径。
- ![](https://pica.zhimg.com/v2-0dcdd85c9cc30680a79aa730528d961e_1440w.jpg)


### 效果

MermaidFlow 不再依赖具备强**编程能力**的大语言模型，也能生成高质量的工作流。

在 GSM8K、MATH、HumanEval、MBPP 等多个主流任务数据集上，MermaidFlow 均展现出优秀的性能，体现出较强的实用价值。
- ![](https://picx.zhimg.com/v2-f7a1c82b5052a048a0aacf57886778c1_1440w.jpg)

得益于结构化表达与静态可验证机制，MermaidFlow 在进化流程中生成可执行且结构合理工作流的成功率超过 90%，相比于传统基于脚本拼接的方法，极大提升了智能体系统的可控性和鲁棒性，为智能体系统的稳健部署提供了坚实的支撑。

MermaidFlow 在结构化表示下的进化过程示例。得益于每个节点及其连接关系均具备明确的语义边界，系统能够便捷且安全地进行局部片段的替换、重组与演化操作（如 crossover、节点替换、连边调整等）。图中演示了系统如何通过对 Workflow 5 和 Workflow 4 进行 crossover 操作，生成结构更健壮的 Workflow 8，引入了更优的 ensemble 与 test 模块。

这一结构可控的演化机制，有效提升了工作流生成过程的安全性、可控性与可维护性。
- ![](https://pic2.zhimg.com/v2-57d56b3172e881415ead8f91e526a663_1440w.jpg)



## 【2025-7-27】Google ACT

- 【2025-7-27】google,哥伦比亚大学 用Action-Based Contrastive Self-Training (ACT)做多轮训练（用了DPO）
- 论文 [Learning to Clarify: Multi-turn Conversations with Action-Based Contrastive Self-Training](https://arxiv.org/pdf/2406.00222)，





# 结束
