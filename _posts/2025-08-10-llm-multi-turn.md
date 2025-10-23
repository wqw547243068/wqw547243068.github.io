---
layout: post
title:  大模型多轮会话
date:   2025-08-10 11:47:00
categories: 大模型 对话系统 agent mermaid 
excerpt : 大模型如何实现任务型多轮会话？如何处理长文本？
tags: 多轮 长文本 压缩
permalink: /multi-turn
mathjax: true
---

* content
{:toc}

# 多轮对话

人工智能（AI）的长期目标
- 生成自然且有意义的响应以与人类通信的多轮对话系统

LLMs的出现显著提高了多轮对话系统的性能

AI 智能体正从**单点能力**迈向**复杂系统协作**，多智能体系统（Multi-Agent Systems, MAS）成为学术和产业界聚焦的新前沿。

这一背景下，「Agentic Workflow」作为面向智能体自主决策与协作流程自动生成的技术理念，正成为多智能体系统研究和应用的探索热点。

## LLM 多轮


### CMU

论文合集: 大模型多轮交互相关的数据、论文、代码
- 【2025-4-7】CMU 综述论文 [Beyond Single-Turn: A Survey on Multi-Turn Interactions with Large Language Models](https://arxiv.org/pdf/2504.04717)，涉及多个场景的多轮会话，roleplay, healthcare, education, and even adversarial jailbreak settings
- [Awesome-Multi-Turn-LLMs](https://github.com/yubol-bobo/Awesome-Multi-Turn-LLMs)

此外，多轮对话场景下增强方法：
- **模型中心策略**: 上下文学习、监督微调、强化学习及新型架构；
- **外部集成方法**: 记忆增强、基于检索的方法及知识图谱；
- 用于协作交互的**基于智能体的技术**。


### 中山大学

【2024-2-28】中山大学综述
- 论文 [A Survey on Recent Advances in LLM-Based Multi-turn Dialogue Systems](https://arxiv.org/pdf/2402.18013v1)
- 解读 [基于LLM的多轮对话系统的最新进展综述](https://zhuanlan.zhihu.com/p/686232892)

多轮对话任务是序列到序列任务
- 从用户消息 `U = (u1, u2, ...ut)` 生成系统响应 `S = (s1, s2, ...st)`
- 其中ut和st分别是第t轮的用户消息和系统响应。

多轮对话系统可以分为: 基于LLM的`开放领域对话`（`ODD`）和`任务导向对话`（`TOD`）系统
- TOD系统帮助用户处理特定领域内的任务，如酒店预订、餐厅推荐等
- 而ODD系统则在没有领域限制的情况下与用户聊天。

TOD任务和ODD任务并不完全独立，一旦对话系统检测到特定用户需求，一个ODD任务可以转换为TOD任务。

ODD主要分为三种方法：
- 基于检索的方法，从预定义的集合中选择响应；
- 基于生成的方法，动态生成响应；
- 以及混合方法，结合检索和生成以优化对话结果。

TOD 分为基于**流水线**的TOD和**端到端**TOD
- 基于流水线的TOD系统包括四个相连的模块：
  - (1) 自然语言理解（NLU），用于提取用户意图和填充槽位；
  - (2) 对话状态跟踪（DST），基于流水线的TOD中的一个关键模块，用于根据NLU模块的输出和对话的历史输入来跟踪当前轮次的对话状态；
  - (3) 策略学习（PL），根据DST模块生成的对话状态确定后续行动；
  - (4) 自然语言生成（NLG），基于流水线的TOD系统中的最后一个模块，将PL模块生成的对话行动转换为易于理解的自然语言。
  - 对话管理器（DM）是基于流水线的TOD系统的中心控制器，由DST模块和PL模块组成。
- 基于端到端的TOD:
  - 模块端到端 modularly end-to-end TOD systems, 同时训练、优化多个模块 —— 主流
  - 全端到端 fully end-to-end TOD systems, LLM再OOD上进步显著，但由于缺乏大量TOD数据，全端到端TOD进展有限

![](https://pica.zhimg.com/v2-fc11c2ced0078baaa889810aa1bae106_1440w.jpg)

案例
- Peng等人提出了Soloist，这是一种使用迁移学习和机器教学来构建端到端TOD系统的方法。Soloist的训练过程与SimpleTOD非常相似。然而，Soloist细化了每个对话回合的数据格式，不再需要对话动作A。训练数据中的每个对话回合可以表示为 = `[H, B, D, S]`，Soloist的完整预训练目标分为信念预测、响应生成。
- UBAR，以前的模块化端到端TOD方法在回合级别序列中进行训练和评估
  - 其中基于对话历史 `Ht = (u1,s1), (u2,s2),..., (ut-1,st-1)`，ut是轮次t生成的响应。而UBAR在上下文中集成了中间信息B、D和A。
  - 因此，UBAR的训练序列依次被定义为：`[H0, B0, D0, A0, S0, . . ., Ht, Bt, Dt, At, St ]`，然后用于微调大型预训练模型GPT-2。
- Su等人提出了一种即插即用的面向任务的对话模型（PPTOD），这是一种模块化的端到端的TOD模型。
  - PPTOD使用四个与TOD相关的任务进行预训练，并使用提示词来提高语言模型的性能。
  - PPTOD的学习框架允许它使用部分注释的数据进行训练，这大大降低了手动创建数据集的成本。
- 阿里达摩院 Semi-supervised Pre-trAined Conversation ModEl (SPACE) 半监督式预训练会话模型
  - GALAXY (SPACE-1) 是模块化TOD,通过应用半监督学习，从有限的标记对话和广泛的未标记对话语料库的组合中显式获取对话策略。
  - SPACE-2 是树结构的对话模型，语义树(STS),在有限的标记对话和大规模未标记对话语料库上预先训练的树结构对话模型。
  - SPACE-3 是最先进的模块化TOD对话系统,整合了SPACE-1和SPACE-2的工作，结合STS来统一不同数据集之间不一致的注释模式，并为每个组件设计了一个专用的预训练目标。

基于LLM的多轮对话系统的两个主要类别：基于LLM的TOD系统和基于LLM的ODD系统。

多轮对话知识见站内专题：[对话管理器](dialogue-manager)

### workflow 自动化

为了提升智能体系统的自主化与智能化，谷歌、上海 AI Lab 等国内外领先团队陆续推出了 `Meta-GPT`、`ADAS`、`AFlow` 等创新性 Agentic Workflow 工作，大力推动利用大模型实现任务规划、分工协作与流程优化的自动化进程。

尽管这些系统能够灵活的表达工作流，但在自动化搜索工作流的过程中，存在：**合理性难以保证**、**可验证性不足**、 **难以直观表达**等突出挑战，严重制约了多智能体系统的可靠落地与规模化部署。

## 问题

### 对话迷失

【2025-8-26】[LLM 在多轮对话中表现出“对话迷失”现象](https://mp.weixin.qq.com/s/yGEfpOL-s6b4Yg4xmiQJCQ)
- Microsoft & Salesforce 论文：[LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/pdf/2505.06120)
- 代码仓库：[lost_in_conversation](https://github.com/Microsoft/lost_in_conversation)

"分片模拟"方法
- 将单轮完整指令分解为多个信息片段(shards)，通过控制实验比较 LLMs 在：（1）单轮完整指令（2）单轮拼接指令（3）多轮分片指令 三种设置下的表现差异。

通过拆解 “能力（Aptitude）” 和 “不可靠性（Unreliability）”，发现多轮对话性能下降的核心原因是不可靠性激增：
- 单轮对话特征：能力（A）与可靠性（R）正相关 —— 能力高的模型（如 GPT-4.1、Gemini 2.5 Pro）更可靠（不可靠性 U 低），能力低的模型（如 Llama3.1-8B）更不稳定。
- 多轮对话特征：
  - 能力（A）仅轻微下降（平均 - 16%），说明模型处理任务的基础能力未大幅退化。
  - 不可靠性（U）显著激增（平均 + 112%），即最佳与最差表现的差距扩大。例如，单轮中 U 约 25，多轮中 U 升至 65，所有模型均表现出高不可靠性，与能力无关。
- “对话迷失” 机制：模型在多轮对话中易出现早期错误假设、过早生成答案并过度依赖，一旦 “走错方向” 便无法恢复（如忽略后续用户补充的关键信息）。

LLM 在单轮与多轮对话设置下的性能差异。
- 当用户指令在多轮对话中逐步提供（即"分片式"对话）时，所有测试的 LLMs 性能平均下降 39%，表现出明显的"对话迷失"现象。

将对话按多个步骤拆分到多轮中，LLM 会存在两个问题：
- 模型在对话早期易做出错误假设，过早生成最终答案并过度依赖。
- 回应冗长，导致信息冗余和混淆；对中间轮次信息的关注度低于首末轮次（“中间轮次遗忘” 现象）。

LLM 在多轮对话中的不可靠性，建议采取实用策略提升效果：
- 重启对话：若当前对话陷入僵局，重启并重复信息可能比继续修正更有效（因模型难以纠正早期错误）。
- 整合需求为单轮指令：将多轮需求汇总为完整指令（如让 LLM “总结之前所有信息”），利用单轮对话的高可靠性（如 CONCAT 场景）。
- 实例：Cursor（代码助手）用户发现 “频繁开启新对话” 能提升效果，印证了多轮对话的局限性。


### 长文本

#### 文本转图像

<img width="499" height="691" alt="image" src="https://github.com/user-attachments/assets/0ff2cf0c-db7d-4d9b-a816-9facba2262be" />

DeepSeek OCR 发布，详见站内专题 [OCR-DeepSeek-OCR](ocr#DeepSeek-OCR)

DeepSeek OCR 同期工作
- 【2025-10-21】南京理工、中南大学 [See the Text: From Tokenization to Visual Readin](https://arxiv.org/abs/2510.18840)
- 【2025-10-20】清华：[Glyph —— Scaling Context Windows via Visual-Text Compression](https://arxiv.org/abs/2510.17800)
- 【2025-10-22】AI^2 和 芝加哥大学，EMNLP 2025 Findings，[Text or Pixels? It Takes Half: On the Token Efficiency of Visual Text Inputs in Multimodal LLMs](https://arxiv.org/abs/2510.18279) 
  - 代码 [text_or_pixels](https://github.com/yanhong-lbh/text_or_pixels)

总结：让大模型“看”文本，而不是“读”文本。
- 【2025-10-20】清华：[Glyph —— Scaling Context Windows via Visual-Text Compression](https://arxiv.org/abs/2510.17800)

Glyph 从输入端出发，把长文本“画”成图像，让模型以视觉方式理解语义。这样就能用图像输入取代传统的文本 token，在不改变模型结构的前提下处理更长的上下文，轻松突破计算与显存的瓶颈。

在 LongBench、MRCR 等基准上，Glyph 在 3–4× 压缩 下依然表现强劲；在极致压缩下，128K 模型也能处理百万级 token，展示出巨大的上下文扩展潜力！

用 VLM 扩展长上下文确实是一条可行且潜力巨大的路径，希望未来能构建出千万token的模型


#### 长文压缩

微软 压缩 Agent 多轮交互历史
- 【2025-10-1】[ACON: Optimizing Context Compression for Long-horizon LLM Agents](https://arxiv.org/abs/2510.00615)

背景 
- LLM agents 在执行如工作流自动化等长时程 (long-horizon) 任务时, 需要不断累积历史交互信息, 导致上下文 (context) 长度爆炸式增长, 从而带来了高昂的计算成本和效率问题。现有的上下文压缩技术大多针对单步或特定领域的任务, 无法很好地适用于复杂、动态的 agent 场景。
	
方法 🛠️

Agent Context Optimization (ACON) 统一框架, 系统性压缩 LLM agent 的交互历史和环境观测。
- 首先在训练任务上运行 agent, 分别使用完整上下文和经过压缩的上下文。
- 通过对比两种情况下 agent 的表现, 筛选出那些在完整上下文中成功, 但在压缩上下文中失败的 "contrastive" 轨迹。
- 针对失败轨迹, 用强大的 "optimizer LLM" 来分析完整上下文和压缩上下文之间的差异, 从而生成自然语言形式的 "feedback"。这个 feedback 指出了压缩过程中丢失了哪些关键信息。接着, 将多条轨迹生成的 feedback 聚合起来, 交给 optimizer LLM 来更新和优化最初的压缩指令。

为了进一步降低成本, 还引入了一个 "compression maximization" step。这一步只分析那些使用压缩上下文成功的轨迹, 让 LLM 判断哪些信息在执行过程中是真正必要的。

为了降低使用大型 LLM 作为 compressor 带来的推理开销, 将优化好的大型 compressor (teacher) 的能力 "distill" (蒸馏) 到一个更小的模型 (student) 中, 从而实现高效部署。
	
实验结果 📊

AppWorld, OfficeBench 和 Multi-objective QA 等多个长时程 agent benchmark 上验证了 ACON 的有效性: ACON 可以在基本保持任务性能的同时, 将峰值内存使用 (peak tokens) 降低 26-54%, 显著优于 FIFO, Retrieval 等基线方法。


## 数据


### 多轮对话数据合成

【2025-4-24】[APIGen-MT：高效生成多轮人机交互Agent数据的两阶段框架](https://developer.volcengine.com/articles/7496711945006481418)

APIGen-MT：高效生成多轮人机交互数据的两阶段框架
- 第一阶段：任务配置和验证
  - 生成详细的任务蓝图（blueprint），包括用户意图、可验证的地面真实动作（groundtruth actions）和预期的最终输出
- 第二阶段：人机环境交互轨迹收集
  - 基于第一阶段生成的验证任务配置，这一阶段通过模拟人机交互来生成完整的多轮交互轨迹

## LLM 多轮对话案例


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

- 【2025-7-27】google,哥伦比亚大学 用 Action-Based Contrastive Self-Training (ACT)做多轮训练（用了DPO）
- 论文 [Learning to Clarify: Multi-turn Conversations with Action-Based Contrastive Self-Training](https://arxiv.org/pdf/2406.00222)，


## 【2025-9-14】MIT PDDL-Instruct

2025年9月14日，大模型学会符号推理 pddl-instruct方法

大模型执行结构化符号规划的能力仍存在局限，尤其在需要规划领域定义语言（PDDL）这类形式化表示的领域中表现更为明显。

新颖的指令微调框架—— PDDL-Instruct，通过逻辑思维链推理，增强大型语言模型的符号规划能力。

详见站内 [MIT PDDL-Instruct](o1#2025-9-14mit-pddl-instruct)



# 结束
