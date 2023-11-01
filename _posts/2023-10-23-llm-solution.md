---
layout: post
title:   大模型微调落地方案 LLM Solution
date:   2023-10-23 16:52:00
categories: 大模型
tags: 微调 RAG lora prompt 陈丹琦 知识图谱
excerpt: 大模型工业落地经验总结
mathjax: true
permalink: /llm_solution
---

* content
{:toc}

# LLM 应用实践

开箱即用的预训练LLM没有按预期或希望执行时，如何提高LLM应用的性能？
- 用检索增强生成（RAG）还是模型微调来改善结果？

## 如何选择优化方法


建议
- 微调之前先尝试RAG


## 方法分析

### RAG vs finetune

分析
- 微调在特定任务上训练模型，就像在问题解答数据集上微调 GPT-3.5 以提高其在特定数据集上的问题解答性能一样。

判断
- 如果数据集**足够大**而且**不会变**，那么采用**微调**。
- 如果数据集动态变化，需要不断重新训练模型，以跟上变化。
- 如果没有大型数据集，不建议微调。建议用 RAG 来提高 LLM 的性能。同样，也可用 RAG 来提高 LLM 在摘要、翻译等任务上的性能，因为这些任务可能无法进行微调。

这两种方法都获得类似结果，但在复杂性、成本和质量方面有所不同。
- ![](https://pic1.zhimg.com/80/v2-c2058b77b95bdb3fb533b7949a6258b8_1440w.webp)

RAG更简单、便宜，但质量可能不匹配。

但这两种方案不是实现相同结果的两个方案，而是正交，满足LLM应用的不同需求。

RAG 和 微调之间的细微差别跨越了模型架构、数据需求、计算复杂性等。忽略这些细节可能会破坏项目时间轴和预算。

如何选择？
- **访问外部数据源**？是 → RAG 更有效、容易扩展
  - 非常适合需要查询数据库、文档或其他结构化/非结构化数据存储库的应用
  - 微调需要大量标注数据集，数据更新时，模型更新不及时
  - 微调过程没有对查询外部知识的检索和推理步骤进行建模。
- **修改模型行为、风格、领域知识**？是 → 微调
  - 微调擅长将LLM行为适配到特定细微差别、语调或术语，如 医学专业人士、以诗意的风格写作，或者使用特定行业的行话
  - RAG虽然善于整合外部知识，但主要侧重信息检索，不会根据检索信息调整其语言风格或领域特异性
- 抑制幻觉重要吗？是 → RAG
  - RAG 相对 微调 不容易产生幻觉，检索机制相当于事实检查器
- 监督语料多吗？是 → 微调，否则 RAG
  - 微调依赖有标签数据的数量和质量，数据不足会过拟合
- 数据会变化吗？是 → RAG
  - 如果数据经常更新，模型容易过时，而重新训练耗时耗力，增加评估成本
  - RAG 检索机制不断查询外部资源，保持最新，知识库/数据源更新时，RAG无缝集成，保持相关性，不用频繁训练
- 要求可解释吗？如果要求较高的透明性+可解释性 → RAG
  - LLM 原理像黑盒，推理机制不明，难以解释为什么
  - RAG 透明性相对较高，检索+生成，用户可以洞察全过程

|维度|解释|`RAG`|`FineTune`|
|---|---|---|
|External knowledge read?|访问外部数据?|✅|❌|
|Changing model behaviour read?|改变模型行为?|❌|✅|
|Minimise hallucinations?|幻觉最小化?|✅|❌|
|Training data availiable?|较多训练数据?|❌|✅|
|Is data (mostly) dynamic?|数据动态变化?|✅|❌|
|Interpretability|要求可解释?|✅|❌|


建议：
- 从RAG开始，评估其性能，如果发现不足，则转向微调。
- 最佳选择: 自动化，混合方法
  - 微调确保聊天机器人符合公司的品牌、语调和一般知识，处理大多数典型的客户查询。
  - RAG可以作为一个补充系统，处理更动态或更具体的查询，确保聊天机器人能够从最新的公司文档或数据库中获取信息，从而最大限度地减少幻觉。
  - 整合这两种方法，公司可以提供全面、及时且与品牌一致的客户支持体验。
- ![](https://pic1.zhimg.com/80/v2-8a98c6db80f32f2fea6fa2503360fd38_1440w.webp)

### 四种方法对比

【2023-10-17】[如何选择最适合你的LLM优化方法：全面微调、PEFT、提示工程和RAG对比分析](https://zhuanlan.zhihu.com/p/661830285?utm_psn=1697685536221999105)
- [RAG vs Finetuning — Which Is the Best Tool to Boost Your LLM Application?](https://towardsdatascience.com/rag-vs-finetuning-which-is-the-best-tool-to-boost-your-llm-application-94654b1eaba7)

四种主要的调优方法：
- **全面微调**：使用任务特定数据调整LLM的所有参数。
  - 一个较小、任务特定、带标签的数据集上进行微调，调整一些模型参数，优化其对特定任务或一组任务的性能
  - 全面微调： 所有模型参数都被更新，使其类似于预训练，只不过是在一个**带标签**且**规模较小**的数据集上进行。
  - ![](https://pic2.zhimg.com/80/v2-e8c7286930eb81b57aaf109fe92ac58d_1440w.webp)
  - 优点: 训练数据集更少、提高精度、增加鲁棒性
  - 缺点: 高计算成本、内存需求高、时间/专业知识密集
- **参数高效精细调整**（PEFT）：修改选定参数以实现更高效的适应。进一步调整预训练模型，只更新其总参数的一小部分
  - PEFT 方法可训练的部分不同。一些技术优先训练原始模型参数的**选定部分**。其他方法集成并训练较小的**附加组件**，如适配器层，而不修改原始结构
  - ![](https://pic2.zhimg.com/80/v2-1d62f9b57373a592407db8aedd90b681_1440w.webp)
  - LoRA是最常用的 PEFT 方法，使用重参数化，这种技术通过执行低秩近似来缩小可训练参数的集合。
  - LoRA优点：
    - 任务切换效率 - 创建模型的不同版本以适应特定任务变得更容易。你可以简单地存储预训练权重的单个副本，并构建许多小 LoRA 模块。当你从任务切换到任务时，你只替换矩阵 A 和 B，并保留 LLM。这显著减少了存储需求。
    - 需要更少的 GPU - LoRA 将 GPU 内存需求减少了最多 3 倍，因为我们不计算/重新训练大多数参数。
    - 高精度 - 在各种评估基准上，LoRA 的性能被证明几乎等同于全面微调 - 而且只需要一部分成本
  - PEFT 相比全面微调的优势
    - 更高效和更快的训练
    - 保留预训练的知识
- **提示工程**：改进模型输入以指导其输出。
  - 在新数据集和任务上训练模型参数，使用所有预训练权重（如全面微调）或一组独立权重（如 LoRA）。
  - 相比之下，提示工程根本不涉及训练网络权重
  - ![](https://pic3.zhimg.com/80/v2-4e5ddc95da8e4945cf30c65e1593050e_1440w.webp)
  - 基础提示: 零样本提示、少样本提示、链式思考引导
  - ![](https://pic4.zhimg.com/80/v2-857d925cf7adc11d94a2fbd9aca37213_1440w.webp)
- **RAG**（检索增强生成）：将提示工程与数据库查询结合，以获得丰富的上下文答案。
  - 将引导工程与从外部数据源检索上下文相结合，以提高语言模型的性能和相关性。通过在模型上附加额外信息，它允许更准确和上下文感知的响应。
  - RAG模型架构将用户查询的嵌入与知识库向量中的embedding进行比较，将来自知识库中相似文档的相关上下文附加到原始用户提示中。然后将这个增强的prompt给到LLMs，可以异步更新知识库及其相关的embedding
  - ![](https://pic3.zhimg.com/80/v2-db7c5fbf5f95c69846fc3805eb287086_1440w.webp)
  - RAG 本质上将信息检索机制与文本生成模型相结合。信息检索组件有助于从数据库中拉取相关的上下文信息，并且文本生成模型使用这个添加的上下文来产生更准确和“知识丰富”的响应。以下是它的工作方式：
    - 向量数据库：实施 RAG 包括嵌入内部数据集，从中创建向量，并将它们存储在向量数据库中。
    - 用户查询：RAG 从提示中获取用户查询，这是一个需要回答或完成的自然语言问题或陈述。
    - 检索组件：一旦接收到用户查询，检索组件扫描向量数据库以识别与查询语义相似的信息块。然后使用这些相关片段为 LLM 提供额外上下文，使其能够生成更准确和上下文感知的响应。
    - 串联：将检索到的文档与原始查询串联成一个提供生成响应所需额外上下文的提示。
    - 文本生成：将包含串联查询和检索文档的提示馈送到 LLM 以产生最终输出。
    - ![](https://pic1.zhimg.com/80/v2-63c902a479d54ff27917dd94d3c65174_1440w.webp)
    - 开源应用框架: 
      - OpenAI [chatgpt-retrieval-plugin](https://github.com/openai/chatgpt-retrieval-plugin)
      - [langchain](https://github.com/langchain-ai/langchain)
      - [LlamaIndex](https://gpt-index.readthedocs.io/en/latest/index.html)
  - [Creating a RAG Pipeline with LangChainPermalink](https://www.maartengrootendorst.com/blog/improving-llms/#creating-a-rag-pipeline-with-langchain), [中文版](https://zhuanlan.zhihu.com/p/661349721?utm_psn=1697558407270424576)
  - ![RAG方法的大致过程](https://www.maartengrootendorst.com/assets/images/posts/2023-12-09-improving-llms/rag.svg)
  - RAG 有许多明显的优点：
    - 最小化幻觉 - 当模型做出“最佳猜测”假设，本质上填补了它“不知道”的内容时，输出可能是错误的或纯粹的胡说八道。与简单的提示工程相比，RAG 产生的结果更准确，幻觉的机会更低。
    - 易于适应新数据 - RAG 可以在事实可能随时间演变的情况下进行适应，使其对生成需要最新信息的响应非常有用。
    - 可解释 - 使用 RAG，可以确定 LLM 答案的来源。对答案来源进行追溯对于内部监控、质量保证或处理客户纠纷可能是有益的。
    - 成本有效 - 与在特定任务数据集上对整个模型进行微调相比，你可以使用 RAG 获得相当的结果，这涉及到更少的标记数据和计算资源。
  - RAG 的潜在限制
    - RAG 旨在通过从外部文档中提取上下文来增强 LLM 的信息检索能力。然而，在某些使用案例中，额外的上下文还不够。如果一个预训练的 LLM 在总结财务数据或从患者的医疗文档中提取见解方面遇到困难，很难看出以单个文档形式提供额外上下文如何有所帮助。在这种情况下，微调更有可能产生期望的输出。

[improving-llms](https://www.maartengrootendorst.com/blog/improving-llms/), 3 of the most common methods for improving the performance of any LLM:
- Prompt Engineering
- Retrieval Augmented Generation (RAG)
- Parameter Efficient Fine-Tuning (PEFT)
- ![](https://www.maartengrootendorst.com/assets/images/posts/2023-12-09-improving-llms/common.svg)
- ![](https://www.maartengrootendorst.com/assets/images/posts/2023-12-09-improving-llms/overview.svg)

四个重要指标上进行比较：复杂性、成本、准确性和灵活性。
- **成本**： PE ＜ RAG ＜ PEFT ＜ Full Fine-tuning
- **复杂性**：PE ＜ RAG ＜ PEFT = Full Fine-tuning
- **准确性**：
  - 特定领域术语：PE ＜ RAG ＜ PEFT ＜ Full Fine-tuning
  - 时效性：PEFT = Full Fine-tuning < PE < RAG
  - 可解释性：PE = PEFT = Full Fine-tuning < RAG
  - 幻觉: PE < PEFT < Full Fine-tuning < RAG
    - 微调可以通过将 LLM 集中在特定领域数据上来减少这些幻觉。然而，不熟悉的查询仍然可能导致 LLM 编造出一个捏造出来的答案。
    - RAG 通过将 LLM 的响应锚定在检索到的文档中来减少幻觉。初始检索步骤本质上进行事实检查，而随后生成受限于检索数据的上下文。对于避免幻觉至关重要的任务，推荐使用 RAG。
  - 总结
    - 解释性、时效性和避免幻觉至关重要 → RAG
    - 要求特定领域风格 → 全面微调 和 PEFT
    - 两者都要 → 微调 和 RAG
- **灵活性**： Full Fine-tuning < PEFT < PE < RAG


## （1）PE 提示工程

**提示工程**：改进模型输入以指导其输出。
- 在新数据集和任务上训练模型参数，使用所有预训练权重（如全面微调）或一组独立权重（如 LoRA）。
- 相比之下，提示工程根本不涉及训练网络权重
- ![](https://pic3.zhimg.com/80/v2-4e5ddc95da8e4945cf30c65e1593050e_1440w.webp)
- 基础提示: 零样本提示、少样本提示、链式思考引导
- ![](https://pic4.zhimg.com/80/v2-857d925cf7adc11d94a2fbd9aca37213_1440w.webp)


## （2）RAG 检索增强生成

### 起因

LLM 通过大量数据训练，回答任何问题或完成任务，利用其参数化记忆。这些模型有一个知识**截止日期**，取决于上次训练的时间。
- 被问及超出其知识范围或知识截止日期后发生的事件时，模型会产生**幻觉**。

Meta 研究人员发现，通过提供与手头任务相关的信息，模型在完成任务时表现**显著改善**。

例如，询问模型关于截止日期之后发生的事件，则提供该事件作为背景信息并随后提问将帮助模型正确回答问题。

由于LLM具有有限的上下文窗口长度，在处理当前任务时**只能传递最相关的知识**。添加到上下文中数据质量影响着模型生成响应结果的质量。机器学习从业者在RAG流程不同阶段使用多种技术来改善LLM性能。

### 什么是 RAG

科里·祖
> “检索增强生成是用您（系统）从其他地方检索到的附加信息来补充用户输入到 ChatGPT 等大型语言模型 (LLM) 的过程。然后，法学硕士可以使用该信息来增强其生成的响应。” 

检索增强生成（简称 `RAG`）是 Meta 于 2020 年推广的一种架构，通过将**相关信息**与**问题/任务细节**一起传递给模型来提高 LLM 的性能。

【2023-9-27】[RAG 与 Finetuning，谁是提升 LLM 的最佳工具？](https://mp.weixin.qq.com/s/D-8r3FHKCyh4xk-yM7lMag)

### RAG 进化路线

【2023-10-30】[ACL2023](https://acl2023-retrieval-lm.github.io/)陈丹琦等《基于检索的大语言模型及其应用》
- 【2023-7-10】[陈丹琦ACL学术报告来了！详解大模型「外挂」数据库7大方向3大挑战，3小时干货满满](https://www.qbitai.com/2023/07/67259.html)
- ![](https://pic1.zhimg.com/80/v2-8fda0e178a75c4c4f7e832e78ffae8c4_1440w.webp)

GPT 模型三个问题：
- 1、参数量过大，如果基于新数据重训练，计算成本过高；
- 2、记忆力不行（面对长文本，记了下文忘了上文），时间一长会产生幻觉，且容易泄露数据；
- 3、目前的参数量，不可能记住所有知识。

这种情况下，**外部检索语料库**被提出，即给大语言模型“外挂”一个数据库，让它随时能通过查找资料来回答问题，而且由于这种数据库随时能更新，也不用担心重训的成本问题。
- ![](https://www.qbitai.com/wp-content/uploads/replace/09f5a03d57c982249ed0e440e53fec9d.png)

训练方式上，则着重介绍
- **独立训练**（independent training，语言模型和检索模型分开训练）、**连续学习**（sequential training）、**多任务学习**（joint training）等方法

应用方面，这类模型涉及的也就比较多了
- 不仅可以用在代码生成、分类、知识密集型NLP等任务上
- 而且通过微调、强化学习、基于检索的提示词等方法就能使用

RAG要解决的几大难题。
- 其一，**小语言模型**+（不断扩张的）**大数据库**，本质上是否意味着语言模型的参数量依旧很大？如何解决这一问题？
  - 模型参数量只有70亿参数量，但外挂的数据库却能达到2T…
  - ![](https://www.qbitai.com/wp-content/uploads/replace/79f264e4ffb852cb45f75b3e5a2fc434.png)
- 其二，相似性搜索的效率。如何设计算法使得搜索效率最大化，是目前非常活跃的一个研究方向。
  - ![](https://www.qbitai.com/wp-content/uploads/replace/18596970d8efb294c3e3283072902ef4.png)
- 其三，完成复杂语言任务。包括开放式文本生成任务，以及复杂的文本推理任务在内，如何用基于检索的语言模型完成这一任务，也是需要持续探索的方向。
  - ![](https://www.qbitai.com/wp-content/uploads/replace/88ca24b2488cf19b327633bad16ca4ea.png)


### RAG 流程

将原始文件拆解后, 每个部分都会生成相应embedding 并且 存放到vector store 中. 当查询发送给 vector store 时, 查询也会转换为 embedding , 然后 vector store 返回与查询最相似 的 embeddings
- ![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Jq9bEbitg1Pv4oASwEQwJg.png)

RAG 包含三个阶段：数据准备、检索和生成。
- **数据准备**阶段：确定数据源、从数据源中提取数据、清理数据并将其存储到数据库中。
  - 识别数据来源、从来源中提取数据、清洗数据并将其存储在数据库中
  - 向量存储器：存储文本、图像、音频等非结构化数据，并基于语义相似性搜索该类别下的内容。
- **检索**阶段：根据手任务从数据库中检索相关数据。
  - 关键词搜索：简单的检索数方法，数据根据关键词进行索引，并且搜索引擎返回包含这些关键的文档。
  - 关键词搜索适用于存储**结构化数据**（如表格、文档等）并使用关键词对数据进行搜索。
  - 图数据库以节点和边的形式存储数据。适用于存储结构化数据（如表格、文档等），并通过数据之间的关系进行搜索
  - 搜索引擎：从公共搜索引擎（如Google、Bing等）或内部擎（如Elasticsearch、Solr等）中检索RAG管道中的数据；搜索引擎适用于从网络上检索数据并使用关键字对其进行搜索。
  - 可将来自**搜索引擎**的数据与**其他数据库**（如向量存储、图数据库等）中获取到的数据相结合，以提高输出质量。推荐结合多种策略（如语义搜索 + 关键字匹配）的混合方法
  - 矢量数据库中对嵌入式数据进行相似性搜索
- **生成**阶段：利用检索到的数据和任务生成输出结果。
  - 检索到相关数据，就会连同用户的查询或任务一起传递给生成器（LLM）。LLM 使用检索到的数据和用户的查询或任务生成输出
  - 输出质量取决于数据的质量和检索策略。

### LLM+RAG

【2023-9-26】[一文纵览LLM+RAG 的方法实现](https://mp.weixin.qq.com/s/ifp2i71Psn86ZCEzffsF0Q)

LLM+RAG 方法实现主要有以下几种方法：
1. **作为Prompt一部分**：比较简单，外接检索器，将检索器召回的内容直接放置到预先配置的Prompt模板中，当成背景知识让LLM来直接输出。这种方法实现最简单，也是当前比较常用的做法。
2. **KNN+LLM**：该方法最大的一个特点就是推理时采用 模型**分布输出** + 检索**Top tokens**，作为两个next-token 进行**融合解码**。通过 Embdding 召回外部知识库和Query token 相似的token 。
3. **自回归检索+解码**：先让模型解码出tokens，然后检索该tokens相似的doc，拼接在Prompt中，进行next-token 预测，完成自回归的解码。

第一种办法中涉及私域知识库问答，关于建索引部分可参考文章：分享闭域知识问答下检索相关的方法和实践。
- 如果不是私域问答，最简单的方案是直接用query 调用外部搜索引擎，取到Top 的结果内容拼接到Prompt 中拿到模型的答案。

路线图见原文: [一文纵览LLM+RAG 的方法实现](https://mp.weixin.qq.com/s/ifp2i71Psn86ZCEzffsF0Q)


### 提升性能

【2023-10-1】[提升RAG性能的 10 种方法](https://mp.weixin.qq.com/s/WDV31S3C7YQKekwJTIYt5Q)

使用 LangChain 或 LlamaIndex 等框架的快速入门指南，任何人都可以使用大约五行代码构建一个简单的 RAG 系统，例如文档的聊天机器人。

但是，用这五行代码构建的机器人不会很好地工作。RAG 很容易制作原型，但很难达到用户满意的地步。基本教程可能会让 RAG 以 80% 的速度运行。但要弥补接下来的 20%，通常需要进行一些认真的实验。

提高RAG性能的 10 种方法
- 清理数据：提升数据质量，优化数据分布
- 探索不同索引类型：索引是LlamaIndex和LangChain的核心
  - RAG 标准方法涉及嵌入和相似性搜索，将上下文数据分块，嵌入所有内容，当查询到来时，从上下文中找到相似的部分。
  - 这种方法效果很好，但并不是适合每个用例的最佳方法。
- 尝试多种分块方法
  - 将上下文数据分块是构建 RAG 系统的核心
  - 块大小很重要。较小的块通常可以改善检索，但可能会导致生成过程缺乏周围的上下文；
  - 小、中、大块大小循环浏览了每一组，发现小是最好的
- 覆盖基本提示: 使用时覆盖基础提示
  - 示例： 你是一名客户支持代理。您的目的是在仅提供事实信息的同时尽可能提供帮助。你应该友好，但不要过于健谈。`上下文信息如下。给定上下文信息而不是先验知识，回答查询`。
- 元数据过滤
  - 元数据（如日期）添加到块中，然后用它来帮助处理结果
  - 构建 RAG 时要记住的一般概念：<span style='color:red'>相似 ≠ 相关</span>
- 查询路由
  - 适用场景：有多个索引，如摘要、敏感问题识别、日期相关，优化成一个索引不一定好
- 重排名
  - 重新排名是解决**相似性**和**相关性**之间差异问题的一种解决方案
  - 如 Cohere Rereanker，LangChain 和 LlamaIndex 都有抽象，可以轻松设置。
- 查询转换（改写）
  - 将用户查询放入基本提示中来更改它
  - 重新措辞：如果系统找不到查询的相关上下文，让LLM重新措辞查询并重试
  - HyDE 是一种策略，接受查询，生成假设的响应，然后将两者用于嵌入查找。研究发现这可以显着提高性能。
  - 将一个查询分解为多个问题（子查询），LLM在分解复杂查询时往往会工作得更好
- 微调embedding模型
  - 基于嵌入的相似性是 RAG 的标准检索机制
  - 预训练模型（如 OpenAI的ada）关于嵌入空间中相似内容的概念可能与场景上下文中相似内容不一致
    - 处理法律文件：希望嵌入更多地基于您的领域特定术语（例如“知识产权”或“违反合同”）对相似性的判断，而不是基于“特此”和“协议”等一般术语。
  - 微调可以将检索指标提高 5-10%，LlamaIndex 可以生成训练集
- LLM 开发工具
  - LlamaIndex 或 LangChain 这两个框架都提供调试工具，允许定义回调、查看使用的上下文、检索来自哪个文档等等。
  - Arize AI 有一个笔记本内工具，可探索如何检索哪些上下文及其原因。
  - Rivet 是一个提供可视化界面的工具，可帮助您构建复杂的代理，由法律技术公司 Ironclad 开源。

其它：【2023-9-27】[检索增强生成 (RAG):What, Why and How?](https://mp.weixin.qq.com/s?__biz=MzkzNDQxNDU1Ng==&mid=2247484067&idx=1&sn=1eafa47e700526ecd9862f7c39587738&chksm=c2bcd310f5cb5a06db8832792c4d810e1a53a26b4435195cba6adf5848e8a253b6150f102834&scene=132&exptype=timeline_recommend_article_extendread_samebiz#wechat_redirect)
- 混合搜索：将语义搜索与关键词搜索结合起来，从向量存储中检索相关数据 —— 已被证明对大多数用例都能获得更好的结果
- 摘要：对块进行摘要并将摘要存储在向量存储中，而不是原始块
- 丢失问题：LLMs并不给予输入中所有标记**相同权重**。中间标记似乎比输入开头和结尾处的标记被赋予较低权重，中间丢失问题。
  - 可重新排列上下文片段，使最重要的片段位于输入**开头**和**结尾**，并将次要片段放置在中间位置。


### Graph RAG

【2023-8-15】Graph RAG 基于知识图谱的搜索增强

#### 解决什么问题

查询：“告诉我所有关于苹果和乔布斯的事”

基于《乔布斯自传》这本书进行问答，而这个问题涉及到的上下文分布在自传这本书的 30 页（分块）时
- 传统的“**分割数据，Embedding 再向量搜索**”方法在多个文档块里用 top-k 去搜索的方法**很难**得到这种分散，细粒的完整信息。
- 而且，这种方法还很容易**遗漏**互相关联的文档块，从而导致信息检索不完整。

知识图谱可以减少基于**嵌入**的语义搜索所导致的不准确性。
- 徐旭给了一个有趣的例子：“保温大棚”与“保温杯”，尽管在语义上两者是存在**相关性**的，但在大多数场景下，这种**通用语义**（Embedding）下的相关性常常并不希望产生，进而作为错误的上下文而引入“幻觉”。

这时候，保有**领域知识**的知识图谱则是非常直接可以缓解、消除这种幻觉的手段。

#### 基本流程

Graph RAG 可简单实现：
- 使用LLM(或其他)模型从问题中提取关键实体。
- 根据这些实体检索子图，深入到一定的深度（例如，2）。
- 利用获得的上下文利用LLM产生答案。

可用 Llama Index轻松搭建 Graph RAG，甚至整合更复杂的 RAG 逻辑，比如 [Graph+Vector RAG](https://gpt-index.readthedocs.io/en/latest/examples/index_structs/knowledge_graph/KnowledgeGraphIndex_vs_VectorStoreIndex_vs_CustomIndex_combined.html)。
- ![](https://github-production-user-asset-6210df.s3.amazonaws.com/1651790/260618959-f783b592-7a8f-4eab-bd61-cf0837e83870.png)

Llama Index 有两种方法实现 Graph RAG：
- `KnowledgeGraphIndex` 从任何私有数据只是**从零构建知识图谱**（基于 LLM 或者其他语言模型），然后 4 行代码进行 Graph RAG。
- `KnowledgeGraphRAGQueryEngine` 在任何**已经存在的知识图谱**上进行 Graph RAG，不过还没有完成这个 PR。

#### text2cypher

基于图谱的 LLM 的另一种有趣方法是text2cypher。
- 不依赖于实体的子图检索，而是将任务/问题翻译成一个面向答案的特定图查询，和 text2sql 方法本质是一样的。

`text2cypher` 根据 KG 的 Schema 和给定的任务生成图形模式查询，而 `SubGraph RAG`获取相关的子图以提供上下文。

得益于 LLM，实现 text2cypher 比传统的 ML 方法更为简单和便宜。
- LangChain: [NebulaGraphQAChain](https://python.langchain.com/docs/use_cases/more/graph/graph_nebula_qa)
- Llama Index: [KnowledgeGraphQueryEngine](https://gpt-index.readthedocs.io/en/latest/examples/query_engine/knowledge_graph_query_engine.html) 

3 行代码就能跑起来 text2cypher。


### Vector RAG

基于embedding的 RAG方法，常见


### RAG-Fusion

【2023-10-7】[使用RAG-Fusion和RRF让RAG在意图搜索方面更进一步](https://mp.weixin.qq.com/s/N7HgjsqgCVf2i-xy05qZtA)
- 原文: [Forget RAG, the Future is RAG-Fusion](https://towardsdatascience.com/forget-rag-the-future-is-rag-fusion-1147298d8ad1)
- [第三方来源](https://luxiangdong.com/2023/10/07/ragfusion/#/%E6%B7%B1%E5%85%A5%E7%A0%94%E7%A9%B6RAG-Fusion%E7%9A%84%E6%9C%BA%E5%88%B6)，包含图片

#### 起因

RAG有许多优点:
- 向量搜索融合： RAG通过将向量搜索功能与生成模型集成，引入了一种新的范例。这种融合能够从大型语言模型(大语言模型)生成更丰富、更具上下文感知的输出。
- 减少幻觉： RAG显著降低了LLM的幻觉倾向，使生成的文本更基于数据。
- 个人和专业实用程序：从个人应用程序如筛选笔记到更专业的集成，RAG展示了在提高生产力和内容质量方面的多功能性，同时基于可信赖的数据源。
然而，我发现越来越多的“限制”:

当前搜索技术限制： 
- RAG受到基于检索的**词法**和**向量搜索技术**的相同限制。
- 人工搜索效率低下：人类并不擅长在搜索系统中输入他们想要的东西，比如打字错误、模糊的查询或有限的词汇，这通常会导致错过明显的顶级搜索结果之外的大量信息。虽然RAG有所帮助，但它并没有完全解决这个问题。
- 搜索的**过度简化**：流行的搜索模式将查询线性地映射到答案，缺乏深度来理解人类查询的多维本质。这种线性模型通常无法捕捉更复杂的用户查询的细微差别和上下文，从而导致相关性较低的结果。


#### 为什么使用RAG-Fusion?

为什么使用RAG-Fusion
- 通过生成**多个**用户查询和**重新排序**结果来解决RAG固有的约束。
- 利用**倒数排序融合**（RRF）和自定义向量评分加权，生成全面准确的结果。

RAG-Fusion 弥合用户明确提出的问题和（原本的意图）打算提出的问题之间的差距，更接近于发现通常仍然隐藏的变革性知识。
- [RAG-Fusion代码](https://github.com/Raudaschl/rag-fusion)

#### RAG-Fusion 机制

RAG Fusion的基本三要素与RAG相似，并在于相同的三个关键技术:
- 通用编程语言，通常是Python。
- 专用的向量搜索数据库，如Elasticsearch或Pinecone，指导文档检索。
- 强大的大型语言模型，如ChatGPT，制作文本。

然而，与RAG不同，RAG-Fusion通过几个额外步骤来区分自己——查询生成和结果的重新排序。

RAG-Fusion’s 工作步骤:
- 查询语句的相关性复制(多查询生成)：通过LLM将用户的查询转换为**相似但不同**的查询。
  - 单个查询可能无法捕获用户感兴趣的全部范围，或者它可能太窄而无法产生全面的结果。这就是从不同角度生成多个查询的原因。
- 并发的向量搜索：对原始查询及其新生成的同级查询执行并发的向量搜索。
- 智能重新排名：聚合和细化所有结果使用倒数排序融合(RRF)。
- 最后优中选优：将精心挑选的结果与新查询配对，引导LLM进行有针对性的查询语句输出，考虑所有查询和重新排序的结果列表。
- ![](https://simg.baai.ac.cn/hub-detail/9d417a2e8e269db73c441281edd48cd31696839601937.webp)

#### 多查询生成

工作原理:
- 对语言模型的函数调用:函数调用语言模型(在本例中为chatGPT)。这种方法需要一个特定的指令集(通常被描述为“系统消息”)来指导模型。例如，这里的系统消息指示模型充当“AI助手”。
- 自然语言查询:然后模型根据原始查询生成多个查询。
- 多样性和覆盖范围:这些查询不仅仅是随机变化。它们是精心生成的，以提供对原始问题的不同观点。例如，如果最初的查询是关于“气候变化的影响”，生成的查询可能包括“气候变化的经济后果”、“气候变化和公共卫生”等角度。
- ![](https://luxiangdong.com/images/ragfusion/4.jpeg)

#### 倒数排序融合 (RRF)

Why RRF?
- 倒数排序融合(RRF) 是一种将具有不同相关性指标的多个结果集组合成单个结果集的方法，不同的相关性指标也不必相互关联即可获得高质量的结果。

该方法的优势在于不利用相关分数，而仅靠排名计算。相关分数存在的问题在于不同模型的分数范围差。RRF是与滑铁卢大学(CAN)和谷歌(Google)合作开发
- [cormacksigir09-rrf](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- “比任何单独的系统产生更好的结果，比标准的重新排名方法产生更好的结果”。

在elasticsearch的8.8版本，已经引入了RRF。

RRF 想象成那种坚持在做决定之前征求每个人意见的人，这种意见是有帮助的，兼听则明，多多益善
- ![](https://luxiangdong.com/images/ragfusion/6.jpeg)

#### 生成输出

用户意图保存
- 使用多个查询的挑战之一是可能会削弱用户的原始意图。为了缓解这种情况，我们指示模型在prompt工程中给予原始查询更多的权重。


#### RAG-Fusion优缺点

优势
- 1、优质的原材料质量
  - 使用RAG Fusion时，搜索深度不仅仅是“增强”，并且其实搜索范围已经被放大了。相关文档的重新排序意味着你不仅仅是在抓取信息的字面意思，而是在深入这个搜索的意图，所以会涉及到更多的优质文档和待搜索内容。
- 2、增强用户意图对齐
  - RAG Fusion的设计理念中包含了自动提示，很多时候我们在搜索的时候并不知道应该怎么描述，像Google、百度就会进行输入框的自动补全提示。RAG Fusion可以捕获用户信息需求的多个方面，从而提供整体输出并与对用户意图进行增强。
- 3、自动为用户查询输入纠错
  - 该系统不仅可以解释用户的查询，还可以精炼用户的查询。通过生成多个查询变体，RAG Fusion执行隐式拼写和语法检查，从而提高搜索结果的准确性。
- 4、导航复杂查询（自动分解长句的意图）
  - 人类的语言在表达复杂或专门的思想时往往会结结巴巴。该系统就像一个语言催化剂，生成各种变体，这些变体可能包含更集中、更相关的搜索结果所需的行话或术语。它还可以处理更长的、更复杂的查询，并将它们分解成更小的、可理解的块，用于向量搜索。
- 5、搜索中的意外发现（关联推荐）
  - 以前在亚马逊买书的时候，总能因为相关推荐发现我更想要的书，RAG Fusion允许这个偶然的发现。通过使用更广泛的查询范围，系统有可能挖掘到信息，而这些信息虽然没有明确搜索，但却成为用户的“啊哈”时刻。这使得RAG Fusion有别于其他传统的搜索模型。

挑战
- 1、过于啰嗦的风险
  - RAG-Fusion的深度有时会导致信息泛滥。输出可能会详细到令人难以承受的程度，把RAG-Fusion想象成一个过度解释事物的朋友。
- 2、可能成本会比较昂贵
  - 多查询输入是需要LLM来做处理的，这时候，很有可能会引起更多的tokens消耗。


### 【2023-10-9】DeepMind: Step-Back Prompting 

【2023-10-27】[DeepMind新技术Step-Back Prompting，可提升RAG应用效果，让大模型学会抽象思考](https://mp.weixin.qq.com/s/3WKUrAI_MflqqdwKIyoDEg)
- [退一步，看得更远：通过抽象引发大型语言模型中的推理](https://zhuanlan.zhihu.com/p/663680218)

Zero-Shot-CoT领域，最近几天（10.3）刚刚有一个新的研究《Large Language Models as Analogical Reasoners》提出，通过类比推理提示（Analogical Prompting）可以让大模型自己生成相似问题做为例子，从而再根据例子步骤形成思维链来解决新问题。

观察：很多任务都很复杂，充满了细节，大语言模型（LLMs）很难找到解决问题所需的相关信息。
- 物理问题：“如果一个理想气体的温度翻了一番，体积增加了八倍，那么它的压强 P 会发生什么变化？” LLM 在直接解答这个问题时可能会忽略**理想气体定律**的基本原则。
- 询问“Estella Leopold 在 1954 年 8 月到 11 月期间就读于哪所学校？”的问题，由于**时间范围非常具体**，直接回答也是非常困难的。

思考
- 在这两种情况下，通过**退一步**提问，能够帮助模型更有效地解决问题。

谷歌DeepMind 10月9日提了一项新技术“Step-Back Prompting”，简称`后退提示`（STP），不是类比寻找相似示例，而是让LLMs**自己抽象问题**，得到更高维度概念和原理，再用这些知识推理并解决问题。这种思维模式非常类似于人类解决问题的方式，让大模型能够借鉴已有规律解决问题。
- [Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models](https://arxiv.org/abs/2310.06117)

`退一步问题`为从原始问题中派生出来的、层级更高的**抽象问题**。
- 不直接问 “Estella Leopold 在特定时间段内的学校是哪所”，而是问一个更高层次的问题：“Estella Leopold 的教育历史是怎样的？”
- 通过回答这个更抽象的问题，获得解答原始问题所需的所有信息。

通常来说，`退一步问题`比`原始问题`更容易回答。基于这种抽象层次的推理有助于避免中间步骤的错误，链式思维提示的例子一样。总的来说，退一步提示法包含两个简单的步骤：
- 抽象：我们首先提示 LLM 提出一个关于更高层次概念或原则的通用问题，并检索与之相关的信息，而不是直接回答原始问题。
- 推理：在获取了关于高层次概念或原则的信息后，LLM 可以基于这些信息对原始问题进行推理。我们将这种方法称为基于抽象的推理。

`后退提示`（STP）可以和RAG相结合，利用`后退提示`获得的抽象问题，获得更多与最终答案需要的的上下文信息，然后，再将获得的上下文和原始问题一起提交给LLM，从而让LLM获得更好的回答质量。
- ![](https://pic1.zhimg.com/80/v2-54afd626bd6d05b95562deae90ecdcd4_1440w.webp)

PaLM-2L模型做了实验，发现这种Prompt技巧能显著提升推理任务（STEM、知识问答、多步推理）的性能表现。
- step-back prompting与rag配合使用的方式 相比较于baseline提升了39.9%，相较于单纯RAG应用，提升了21.6%的效果。

工程实现
- 该技术已经被langchain支持
- [colab尝试](https://github.com/langchain-ai/langchain/blob/master/cookbook/stepback-qa.ipynb)

```py
response_prompt_template = """You are an expert of world knowledge. I am going to ask you a question. Your response should be comprehensive and not contradicted with the following context if they are relevant. Otherwise, ignore them if they are not relevant.

{normal_context}

Original Question: {question}
Answer:"""
response_prompt = ChatPromptTemplate.from_template(response_prompt_template)

chain = (
    {
        # Retrieve context using the normal question (only the first 3 results)
        "normal_context": RunnableLambda(lambda x: x["question"]) | retriever,
        # Pass on the question
        "question": lambda x: x["question"],
    }
    | response_prompt
    | ChatOpenAI(temperature=0)
    | StrOutputParser()
)

chain.invoke({"question": question})
```

### 【2023-10-17】华盛顿大学: Self-RAG

【2023-10-17】华盛顿大学 [Self-RAG：通过自我反思实现检索增强生成](https://zhuanlan.zhihu.com/p/662969847)

检索增强生成（Retrieval-Augmented Generation，`RAG`）方法通过检索相关知识来减少这类问题，降低了LLMs在知识密集型任务中的事实错误率）。但是，会存在如下问题
- <span style='color:red'>不加区别地检索和合并一定数量的检索文段</span>，无论是否**需要检索**或文段**是否相关**，这会降低LLMs的**多功能性**或导致生成质量不佳（Shi等人，2023），因为不加区别地检索文段，无论事实支持是否有帮助。
- <span style='color:red'>生成结果与检索段落未必一致</span>（Gao等人，2023），因为这些模型没有明确训练以利用和遵循所提供文段的事实。
- ![](https://pic1.zhimg.com/80/v2-86a0ca09dc393444588990f487fdfa00_1440w.webp)

论文提出一种新框架：`自我反思检索增强生成`（[SELF-RAG](https://selfrag.github.io/)），通过**按需检索**和**自我反思**来提高LLM的生成质量，包括其事实准确性，而不损害其多功能性。
- [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511)
- [SELF-RAG](https://selfrag.github.io/) 主页包含代码、模型和数据

论文以端到端方式训练**任意LLM**来学习反思自身的生成过程，通过生成任务输出和间歇性的特殊token（即反思token）。
- 反思token分为**检索**和**评论**token，分别表示检索的需求和生成的质量（图中右侧）。

具体做法如下：
- 给定输入提示和先前的生成，[SELF-RAG](https://selfrag.github.io/)
- 首先，确定继续生成增加检索文段是否**有所帮助**。如果是,输出一个检索标记，以便按需调用一个检索模型（步骤1）。
- 随后，[SELF-RAG](https://selfrag.github.io/)同时处理**多个检索文段**，评估相关性，然后生成相应的任务输出（步骤2）。
- 然后，生成**评论标记**来评估输出，并选择在事实准确性和整体质量方面最好的生成（步骤3）。
  - 这个过程与传统RAG（图1左侧）不同，后者不管检索是否有必要（例如，底部示例不需要事实知识），都会一律检索固定数量的文档进行生成，并且从不第二次访问生成质量。
- 此外，[SELF-RAG](https://selfrag.github.io/)为每个部分提供**引文**，附带自我评估是否输出受文段支持，从而简化了事实验证。

实验证据表明
- SELF-RAG 在 6个任务上**明显优于**经过预训练或指令学习的LLMs，以及更高引用准确性的RAG方法，达到sota。
- SELF-RAG 在 4个任务上优于具有检索增强功能的`ChatGPT`，`Llama2-chat`和`Alpaca`, 在所有任务中的性能更好。

Self-RAG outperforms vanilla ChatGPT or LLama2-chat across six tasks, and outperforms those SOTA models with widely-used retrieval-augmentation methods in most tasks by large margin

论文分析证明了使用**反思标记**进行训练和推理对整体性能提升以及测试时模型自定义（例如，在引文预测和完整性之间的权衡）的有效性。

Connections to Prior Work
- v.s. **Retrieval-augmented Generation** 与传统RAG相比，`Self-RAG`针对多样性任务自适应检索,并评估相关性，更加灵活
  - `Standard RAG` only retrieves once or fixed number of time steps, while `Self-RAG` enables **Adaptive retrieval** for diverse task inputs, and can retrieve multiple times while generations, or completely skip retrieval, making it more suitable for diverse downstream queries (e.g., instruction-following).
  - `Self-RAG` carefully criticize retrieved passages or its own generations via reflection tokens and incorporate hard or soft constrained during decoding, while `standard RAG` does not assess relevance of passages or whether the output is indeed supported by the passages.
- v.s. **Learning from Critique** (Feedback) `Self-RAG`再多个参考结果中调整奖励权重，不需要训练
  - Reflection tokens are inserted offline by another Critic model trained on machine-generated feedback, making training much more memory efficient and stable than widely adopted RLHF methods (e.g., PPO).
  - `Self-RAG` enables tailored behaviors by simply adjusting reward weights across multiple preference aspects, while prior fine-grained feedback learning method requires training for different model behaviors.



### Agent RAG 

【2023-10-28】[Retrieval-Augmented Generation (RAG) Applications with AutoGen](https://microsoft.github.io/autogen/blog/2023/10/18/RetrieveChat/)
- 基于 AtuoGen 的 RAG
- ![](https://microsoft.github.io/autogen/assets/images/retrievechat-arch-959e180405c99ceb3da88a441c02f45e.png)

AutoGen 的 RAG系统由两个代理组成
- `RetrieveUserProxyAgent`: 人类代理，也能执行代码、调用函数
  - `code_execution_config` 可关闭自动执行
  - 默认不启用 LLM，可以通过配置文件 `llm_config` 开启
  - 指定文档集合路径。随后下载文档，分割成特定大小的块，计算嵌入，并存储在矢量数据库中
- `RetrieveAssistantAgent`: 与 LLM 交互，可以执行LLM生成的Python代码

相关配置
- `llm_config` LLM 配置信息

- RAG 代理的定制
  - 定制嵌入功能、文本分割功能和矢量数据库。
- RAG 代理的两种高级用法，即
  - 与**群聊**集成
  - 使用 Gradio 构建聊天应用程序

Diverse Applications Implemented with AutoGen
- ![](https://microsoft.github.io/autogen/assets/images/app-b0acafd5e331fa9471ab6d0e7010a83d.png)

## （3）PEFT 参数高效微调

- **参数高效精细调整**（PEFT）：修改选定参数以实现更高效的适应。进一步调整预训练模型，只更新其总参数的一小部分
  - PEFT 方法可训练的部分不同。一些技术优先训练原始模型参数的**选定部分**。其他方法集成并训练较小的**附加组件**，如适配器层，而不修改原始结构
  - ![](https://pic2.zhimg.com/80/v2-1d62f9b57373a592407db8aedd90b681_1440w.webp)
  - LoRA是最常用的 PEFT 方法，使用重参数化，这种技术通过执行低秩近似来缩小可训练参数的集合。
  - LoRA优点：
    - 任务切换效率 - 创建模型的不同版本以适应特定任务变得更容易。你可以简单地存储预训练权重的单个副本，并构建许多小 LoRA 模块。当你从任务切换到任务时，你只替换矩阵 A 和 B，并保留 LLM。这显著减少了存储需求。
    - 需要更少的 GPU - LoRA 将 GPU 内存需求减少了最多 3 倍，因为我们不计算/重新训练大多数参数。
    - 高精度 - 在各种评估基准上，LoRA 的性能被证明几乎等同于全面微调 - 而且只需要一部分成本
  - PEFT 相比全面微调的优势
    - 更高效和更快的训练
    - 保留预训练的知识

### PEFT 参数高效微调技术

#### 解决什么问题

起因：训练模式
- 全参数微调：对特定下游任务进行 Full FineTuning（全参数微调），**太过低效**；
- 部分参数微调：固定预训练模型的某些层，只微调接近下游任务的那几层参数，又难以达到**较好效果**。

#### 解决思路

PEFT技术通过**最小化**微调参数的数量和计算复杂度，来提高预训练模型在新任务上的性能，从而缓解大型预训练模型的训练成本。
- 即使计算资源受限，也可以利用预训练模型的知识来迅速适应新任务，实现高效的迁移学习。
- 因此，PEFT技术可以在提高模型效果的同时，大大缩短模型训练时间和计算成本，让更多人能够参与到深度学习研究中来。

#### PEFT 方法

方法
- `Prefix Tuning`：与full fine-tuning更新所有参数的方式不同，该方法是在输入token之前构造一段任务相关的virtual tokens作为Prefix，然后训练的时候只更新Prefix部分的参数，而Transformer中的其他部分参数固定。该方法其实和构造Prompt类似，只是Prompt是人为构造的“显式”的提示,并且无法更新参数，而Prefix则是可以学习的“隐式”的提示。同时，为了防止直接更新Prefix的参数导致训练不稳定的情况，他们在Prefix层前面加了MLP结构(相当于将Prefix分解为更小维度的Input与MLP的组合后输出的结果)，训练完成后，只保留Prefix的参数。
- `Prompt Tuning`：该方法可以看作是Prefix Tuning的简化版本，只在输入层加入prompt tokens，并不需要加入MLP进行调整来解决难训练的问题。随着预训练模型参数量的增加，Prompt Tuning的方法会逼近fine-tuning的结果。
- `P-Tuning`：该方法的提出主要是为了解决这样一个问题：大模型的Prompt构造方式严重影响下游任务的效果。P-Tuning将Prompt转换为可以学习的Embedding层，并用MLP+LSTM的方式来对prompt embedding进行一层处理。
- `P-Tuning v2`：让Prompt Tuning能够在不同参数规模的预训练模型、针对不同下游任务的结果上都达到匹敌Fine-tuning的结果。相比Prompt Tuning和P-tuning的方法，P-Tuning v2方法在多层加入了Prompts tokens作为输入，带来两个方面的好处：
  - 带来更多可学习的参数（从P-tuning和Prompt Tuning的0.1%增加到0.1%-3%），同时也足够参数高效。
  - 加入到更深层结构中的Prompt能给模型预测带来更直接的影响。
- `Adapter Tuning`：该方法设计了Adapter结构（首先是一个down-project层将高维度特征映射到低维特征，然后过一个非线形层之后，再用一个up-project结构将低维特征映射回原来的高维特征；同时也设计了skip-connection结构，确保了在最差的情况下能够退化为identity），并将其嵌入Transformer的结构里面，在训练时，固定住原来预训练模型的参数不变，只对新增的Adapter结构进行微调。同时为了保证训练的高效性（也就是尽可能少的引入更多参数）。
- `LoRA`：在涉及到矩阵相乘的模块，引入A、B这样两个低秩矩阵模块去模拟full fine-tuning的过程，相当于只对语言模型中起关键作用的低秩本质维度进行更新。

#### PEFT 实现

PEFT实现工具：
- PEFT：Huggingface推出的PEFT库。
- unify-parameter-efficient-tuning：一个参数高效迁移学习的统一框架。

Parameter-Efficient Fine-Tuning (`PEFT`) 是HuggingFace 开源的一个高效微调大模型库，支持在 LLM 上创建和微调适配器层。
- peft 与  🤗 Accelerate 无缝集成，用于利用了 DeepSpeed 和 Big Model Inference 的大规模模型。

【2023-7-11】[Prompt系列高效调参原理解析](https://mp.weixin.qq.com/s/webUB5j8nNQsthTFQNiqpA), [智源社区](https://hub.baai.ac.cn/view/28876)

PEFT内置7种主流高效调参方法
- `LoRA`: LORA: LOW-RANK ADAPTATION OF LARGE LANGUAGE MODELS
- `Prefix Tuning`: Prefix-Tuning: Optimizing Continuous Prompts for Generation,
- `P-Tuning v2`: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks
- `P-Tuning`: GPT Understands, Too
- `Prompt Tuning`: The Power of Scale for Parameter-Efficient Prompt Tuning
- `AdaLoRA`: Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning
- `QLoRA`: QLoRA: Efficient Finetuning of Quantized LLMs

时间线
- ![](https://simg.baai.ac.cn/hub-detail/f81b72c3cedac0b670dd7c68144b718c1692420361295.webp)

|时间|机构|方法|备注|
|---|---|---|---|
|2021.1|stanford|Prefix Tuning|Prompt Series|
|2021.3|Tsinghua|P-Tuning|Prompt Series|
|2021.9|Google|Prompt Tuning|Prompt Series|
|2021.11|Microsoft|LoRA|LoRA Series|
|2022.3|Tsinghua|P-Tuning v2|Prompt Series|
|2023.3|Microsoft|AdaLoRA|LoRA Series|
|2023.5|Washington|QLoRA|LoRA Series|

目前包含LoRA，Prefix Tuning，Prompt Tuning，P-Tuning 四种算法
*   LoRA
*   [Prefix Tuning](https://arxiv.org/pdf/2110.07602.pdf)
  - Prefix Tuning 算法是根据 下游任务 "前缀指令文本" 的所有层的embeding表示，学习到的前缀指令文本向量可以挖掘大模型的潜力去引导模型完成特定任务。
  - ![](https://pic3.zhimg.com/80/v2-9a6b5792cf60079429d067fc629e65ae_1440w.webp)
*   [P-Tuning](https://arxiv.org/pdf/2103.10385.pdf)
  - P-Tuning 算法和 Prefix Tuning 的想法很相似，想通过微调"指令文本",让指令文本去挖掘大模型的潜力去完成特定的任务。但是 P-Tuning 只学习 "指令文本" 输入层embeding的的表示。 为了增强 "指令文本"的连续性，采用了一个 MLP(LSTM) 的结果去encoding "指令文本"。从微调参数量来看只有 0.65% 比 Prefix Tuning 和 LoRA 这些在所有层都增加参数的方法要少。
  - ![](https://pic3.zhimg.com/80/v2-7540fb5d913adcae8be308fce31befea_1440w.webp)
*   [Prompt Tuning](https://arxiv.org/pdf/2104.08691.pdf)
  - Prompt Tuning 算法和 P-Tuning 很像，且更简单，就是是根据 下游任务 "指令文本" 输入层embeding的的表示。 Prompt Tuning 没有增加任何的层，直接使用微调指令文本(prompt) 的embeding向量。
  - ![](https://pic3.zhimg.com/80/v2-b281f773be36787dddd0f06e782384b2_1440w.webp)

[详见](https://zhuanlan.zhihu.com/p/618695885)

[Parameter-Efficient Fine-Tuning](https://github.com/huggingface/peft) (PEFT)

单个 24GB GPU 上使用上述工具使用 RL 微调 20B 参数量的 LLM, 详见量化[quantization](https://hf.co/docs/transformers/main/en/main_classes/quantization)
- 与全精度模型相比，以 **8位**精度加载模型最多可节省 **4倍**的内存
- 调用 from_pretrained 方法时简单地添加标志 load_in_8bit=True

详见：[在一张 24 GB 的消费级显卡上用 RLHF 微调 20B LLMs](https://mp.weixin.qq.com/s/7nmegO1UYObO0-eUDTKnMg)

#### PEFT 不足

相比全参数微调，高效微调技术目前存在的两个问题：
- 推理速度会变慢
- 模型精度会变差


#### 应用示例

典型应用：
- `ChatGLM-Tuning` ：一种平价的chatgpt实现方案，基于清华的 ChatGLM-6B + LoRA 进行finetune。
- `Alpaca-Lora`：使用低秩自适应（LoRA）复现斯坦福羊驼的结果。Stanford Alpaca 是在 LLaMA 整个模型上微调，而 Alpaca-Lora 则是利用 Lora 技术，在冻结原模型 LLaMA 参数的情况下，通过往模型中加入额外的网络层，并只训练这些新增的网络层参数。由于这些新增参数数量较少，这样不仅微调的成本显著下降，还能获得和全模型微调类似的效果。
- `BLOOM-LORA`：由于LLaMA的限制，我们尝试使用Alpaca-Lora重新实现BLOOM-LoRA。


### 微调原理

FineTune 微调

预训练模型在小规模特定数据集上进一步训练，调整模型权重，适应特定任务或提高其性能。
- ![](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*JSJBBnslBE9S5i77Rz9r_g.png)

【2023-6-25】[大模型参数高效微调技术原理综述（七）-最佳实践、总结](https://mp.weixin.qq.com/s/M-7ZudD0dvscsApryiPIYw)

参数高效微调综述论文：
- 【2023-3-28】[Scaling Down to Scale Up: A Guide to Parameter-Efficient Fine-Tuning](https://arxiv.org/pdf/2303.15647.pdf)
- 中文[解读](https://zhuanlan.zhihu.com/p/627537421)

几种参数高效微调方法进行了简单的概述，主要有如下几类：
- `Additive` 增加**额外参数**，注意力与FFN后加一个**全连接层**
  - 如：Prefix Tuning、Prompt Tuning、Adapter Tuning及其变体。
  - soft prompts 软提示
    - Prompt Tuning: 输入前面加入一些新的可学习的嵌入向量
    - Prefix-Tuning: 在所有层前面加入可学习的参数
    - Intrinsic Prompt Tuning (IPT): 用自编码器来压缩soft Compact
  - adapters-like 适配器
    - Adapter: 在注意力与FFN后加一个全连接层
    - AdaMix: 采用MOE策略引入多个Adapters
  - 其它
    - Ladder-Side Tuning (LST): 在每个Transformer block旁边引入一个小型的Transformer来计算更新的参数，类似于Lora
    - (IA)3: 缩放 key value以及FFN的 激活函数
- `Selecttive` 选取一**部分参数**更新，如：BitFit。
  - BitFit：仅更新bias
  - DiffPruning: mask掉一些训练的参数
  - Freeze and Reconfigure (FAR): 按照行来划分为 训练的行与 冻结的行
  - FishMask: 使用Fisher信息矩阵来选取 top-p参数进行更新
- `Reparametrization` 引入**重参数化**，如：LoRA、AdaLoRA、QLoRA。
  - Intrinsic SAID: 更新一个低维空间的向量
  - LoRA: 更新旁路，且旁路设计为一个下采样与一个上采样
  - KronA: 使用克罗内克积来减小Lora的计算开支
- **混合**高效微调，如：MAM Adapter、UniPELT。
  - SparseAdapter: 使用一个维度较大的Adapter，并对这个Adapter稀疏化，避免参数过多
  - MAM Adapter: 并行的Adapter, FFN layer and soft prompt.
  - UniPELT: 将LoRa Prefix-tuning 和 Adapter 使用gat机制合并
  - Compacter: 使用克罗内克积，并且每层共享参数的 Adapter
  - S4: 探索了这些方法结合起来的效果

高效微调粗略分为三类：
- 加额外参数 `A` + 选取一部分参数更新 `S` + 引入重参数化 `R`
- ![](https://pic2.zhimg.com/80/v2-ed42c72dfe5b849dfeb5df142f270675_1440w.webp)

各种方法对比
- ![](https://pic1.zhimg.com/80/v2-87347f7802c02861ec2ed937d5a0422c_1440w.webp)

### BitFit

对微调机制的一种积极探索，通过**仅调整bias**就有不错的效果，但没有具体阐述原理，通过猜测加实验得到的结果。

观点：
> 微调过程不是让模型**适应**另外的数据分布，而是让模型更好的**应用出**本身的表征能力。

特点：
- 训练参数量极小（约0.1%）。
- 大部分任务上效果会**差于**LoRA、Adapter等方法。

### Prefix Tuning

在每一个Transformer层都带上一些virtual token作为前缀，以适应不同的任务。

特点：
- 前缀Token会占用序列长度，有一定额外计算开销。
- Prefix Tuning的线性插值比较复杂。

### Prompt Tuning

该方法是Prefix Tuning 简化版本，针对不同的任务，仅在输入层引入virtual token形式的**软提示**（soft prompt）。

特点：
- 相对于Prefix Tuning，参与训练的参数量和改变的**参数量更小**，更节省显存。
- 对一些简单的NLU 任务还不错，但对**硬序列**标记任务（即`序列标注`）表现欠佳。

**Prompt Tuning with soft prompts**

输入层增加可训练的Soft Prompt参数，参数长度一般在20-100个，每个参数的embedding维度和词表token的embedding维度相同，如下图所示：
- ![](https://pic1.zhimg.com/80/v2-85458b36242c77954879891f231bf2ec_1440w.webp)

相较于**全参数微调**，Prompt Tuning也是通过**冻结LLM的原始参数**，添加少量额外训练参数以达到加速训练的目的；
- ![](https://pic1.zhimg.com/80/v2-027a29613e0f2d780b44cbc0261c3218_1440w.webp)

Prompt Tuning的实际效果可以从下面图中看出：
- 1，当模型参数不大的时候，Prompt Tuning比全参数微调的效果差一点，但是高于单纯的Prompt工程；
- 2，当模型参数在100亿时，Prompt Tuning的效果和全参数微调的效果一样好；
- ![](https://pic2.zhimg.com/80/v2-549a94de38e793377170c271a46bf9bd_1440w.webp)

Prompt Tuning的可解释性说明：
1.  对于已完成训练的prompt embedding来说，是无法与词表中任何token表示对应的（Trained soft-prompt embedding does not correspond to a known token）；
2.  但是观察其邻域范围内的token表示可以看出其具有相同的语义，能够表示相同的意思（but nearest neighbors form a semantic group with similar meanings）；
- ![](https://pic3.zhimg.com/80/v2-2baec89ee6fc953eb3cc690264b67caa_1440w.webp)
- ![](https://pic1.zhimg.com/80/v2-5da93b477f40d3253d743edbdbe26478_1440w.webp)

### P-Tuning

将Prompt转换为可学习的**Embedding层**，并用 MLP+LSTM 的方式来对 Prompt Embedding 进行一层处理。
- 相比 Prefix Tuning，仅在输入层加入可微的virtual token；
- 另外，virtual token的位置也不一定是前缀，插入的位置是可选的。

特点：
- 引入一个prompt encoder（由一个双向的LSTM+两层MLP组成）来建模virtual token的相互依赖会收敛更快，效果更好。

### P-Tuning v2

该方法在每个Transformer层都加入了prompt token作为输入，引入**多任务**学习，针对不同任务采用不同的提示长度。并且回归传统的**分类标签**范式，而不是**映射器**。

特点：
- 解决了Prompt Tuning无法在小模型上有效提升的问题。
- 移除了对模型效果改进较小的重参数化的编码器（如：Prefix Tuning中的MLP、P-Tuning中的LSTM）。
- 对于一些复杂的硬序列标记任务（即序列标注）取得了不错的效果。

### Adapter Tuning

该方法设计了Adapter结构，并将其嵌入Transformer的结构里面，针对每一个Transformer层，增加了两个Adapter结构，在训练时，固定住原来预训练模型的参数不变，只对新增的Adapter结构和Layer Norm 层进行微调。

特点：
- 通过在Transformer层中嵌入Adapter结构，在推理时会额外增加推理时长。

### AdapterFusion

一种融合多任务信息的Adapter的变体，在 Adapter 的基础上进行优化，通过将学习过程分为两阶段来提升下游任务表现。

### AdapterDrop

该方法在不影响任务性能的情况下，对Adapter动态高效的移除，尽可能的减少模型的参数量，提高模型在反向传播（训练）和正向传播（推理）时的效率。

特点：
- 通过从较低的 Transformer 层删除可变数量的Adaper来提升推理速度。 当对多个任务执行推理时，动态地减少了运行时的计算开销，并在很大程度上保持了任务性能。


### LoRA 低秩适配

通过低秩分解来模拟参数的改变量，从而以极小的参数量来实现大模型的间接训练。

特点：
- 将BA加到W上可以消除推理延迟。
- 可以通过可插拔的形式切换到不同的任务。
- 设计的比较好，简单且效果好。

LoRA微调与全量微调相比效果会更差，但团队将LoRA添加到所有的**线性层**解决了这个问题。

2021年，[LoRA: Low-Rank Adaption of Large Language Models](https://arxiv.org/abs/2106.09685) 论文表明，可以通过**冻结**预训练权重，并创建**查询和值**层的注意力矩阵的低秩版本来对大型语言模型进行微调。
- 这些低秩矩阵的参数**远少于**原始模型，因此可以使用更少的 GPU 内存进行微调。
- 低阶适配器的微调取得了与微调完整预训练模型相当的结果。

核心思想
- 冻结预训练模型权重，将可训练的秩分解矩阵注入 Transformer 架构的每一层，从而大大减少了下游任务的微调参数量

LoRA 的实现流程概述如下：
- 在原始预训练语言模型 (PLM) 旁增加一个旁路，做一个先**降维**再**升维**的操作，以此来模拟所谓的`本征秩` (intrinsic rank)；
- 训练的时候固定 PLM 的参数不变，只训练降维矩阵 A 和升维矩阵 B，即优化器只优化右路的参数；
- 模型的输入、输出维度不变，左右两边共用模型的输入，输出时将 PLM 与旁路的输出叠加：h=Wx+BAx
- 用零均值随机高斯分布初始化 A，用全零矩阵初始化 B，矩阵 B 的全零初始化，使得在训练最开始的一段时间，右路的结果会接近于0，这样模块的输出就基本上来自于左路，也就是大模型原有参数的计算结果，这使得模型优化的初始点和原始的大模型保持一致。

示意图
- ![](https://pic4.zhimg.com/80/v2-48e88e61040a94284cc0499be8ecda37_1440w.webp)

LoRA微调可以采用不同的低秩矩阵适配不同的任务类型，且LLM的原始权重不用变化；
- ![](https://pic2.zhimg.com/80/v2-0ba745c8fff2c7015d9463206c5be631_1440w.webp)

整体上LoRA微调效果相对于基座模型有较大的提升，但是相对于全参数微调方式来说效果上还是低一点。
- `Full fine-tune` > `LoRA` > `base model`
- ![](https://pic4.zhimg.com/80/v2-90f36dc2e8d97ccbe6bb20b941a9745b_1440w.webp)



对于 $\delta W_x$ 这部分，会乘上一个 scale 系数 $\frac{\alpha}{r}$
- $\alpha$ 相对于 r 保持一个常数倍的关系。调节这个 $\alpha$ 大致相当于**调节学习率**，于是干脆固定为常数
- 实践中，rank r 应该设为多少比较合适呢？可以很低，不超过8
- [当红炸子鸡 LoRA，是当代微调 LLMs 的正确姿势？](https://zhuanlan.zhihu.com/p/618894919)

LoRA 一般会在 Transformer 每层中的 query_key_value 部分增加旁路，其中 r 为矩阵的秩，在模型训练中是可调节的参数，r << d，r 越大，可训练的参数越多。
- 图见[原文](https://mp.weixin.qq.com/s/yTX_bQEur8Nj6h_uGFJ31g)

LoRA 的优势在于能够使用较少的 GPU 资源，在下游任务中对大模型进行微调。
- 在开源社区中，开发者们使用 LoRA 对 Stable Diffusion 进行微调，取得了非常不错的效果。
- 随着 ChatGPT 的火爆，也涌现出了许多使用 LoRA 对 LLM 进行指令微调的工作。

这种技术允许使用小部分内存来微调 LLM。然而，也有缺点
- 由于适配器层中的额外矩阵乘法，前向和反向传递的速度大约是原来的**两倍**。

LoRA 是 Parameter Efficient 的方法之一。
- 过度参数化的模型其实是位于一个低的**内在维度**上，所以作者假设在模型适应过程中的权重变化也具有较低的“内在等级”。
- [LoRA](https://github.com/microsoft/LoRA)的主要方法为**冻结**一个预训练模型的矩阵参数，并选择用A和B矩阵来替代，在下游任务时只更新A和B。
- ![](https://pic4.zhimg.com/80/v2-67cd3e1e603a5bb674463ddc4db38d57_1440w.webp)
- ![](https://pic2.zhimg.com/80/v2-f56b07afc29ccad77a6faffa130ab24d_1440w.webp)

【2023-5-27】LoRA压缩比，[港科大实验数据](https://lmflow.com/)

Extremely few parameters with LoRA
- LLaMA-33B （65GB）-> 25M
- LLaMA-13B（26GB） -> 13M
- LLaMA-7B （13.5GB）-> 8M


【2023-4-5】LoRA原理讲解，[LoRA：训练你的GPT](https://www.bilibili.com/video/BV17g4y1g7S6)

<iframe src="//player.bilibili.com/player.html?aid=824514848&bvid=BV17g4y1g7S6&cid=1084363572&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width='800' height='600'> </iframe>


```py
class LoraLayer:
    def __init__(
        self,
        r: int,
        lora_alpha: int,
        lora_dropout: float,
        merge_weights: bool,
    ):
        self.r = r
        self.lora_alpha = lora_alpha

        # Optional dropout
        if lora_dropout > 0.0:
            self.lora_dropout = nn.Dropout(p=lora_dropout)
        else:
            self.lora_dropout = lambda x: x

        # Mark the weight as unmerged
        # 标记低秩分解部分是否已经合并至预训练权重
        self.merged = False
        # 指定是否要将低秩分解部分合并至预训练权重中
        self.merge_weights = merge_weights

        # 是否要禁用低秩分解的部分，如果是，则仅使用预训练权重部分
        self.disable_adapters = False
```

#### LoRA 使用

LoRA 已经被作者打包到了loralib中。
- pip install loralib

可以选择用loralib中实现的对应层来替换一些层。
- 目前loralib只支持 nn.Linear、nn.Embedding 和 nn.Conv2d。
- loralib还支持一个 MergedLinear，用于单个 nn.Linear 代表一个以上的层的情况，比如在一些关注 qkv 投影的实现中（self- attention）
- ![](https://pic2.zhimg.com/80/v2-bcef352dc1adf7d6f2fad86e1fe892fd_1440w.webp)

```py
# ===== Before =====
layer = nn.Linear(in_features, out_features)

# ===== After ======
import loralib as lora
# Add a pair of low-rank adaptation matrices with rank r=16
layer = lora.Linear(in_features, out_features, r=16)
```

详见原文：[微软LoRA: Low-Rank Adaptation of Large Language Models 代码解读](https://zhuanlan.zhihu.com/p/515954218)

#### LoRA 实现

官方notebook案例：[peft_lora_seq2seq](https://github.com/huggingface/peft/blob/main/examples/conditional_generation/peft_lora_seq2seq.ipynb)

### AdaLoRA

对LoRA的一种改进，根据**重要性评分**动态分配参数预算给权重矩阵，将关键的增量矩阵分配高秩以捕捉更精细和任务特定的信息，而将较不重要的矩阵的秩降低，以防止过拟合并节省计算预算。


### QLoRA

【2023-5-23】华盛顿大学发布一种高效的微调方法：QLoRA，在保持完整的16位微调任务性能下，实现单个 48GB GPU 上微调 65B 参数量模型。
- [QLoRA: Efficient Finetuning of Quantized LLMs](arxiv.org/abs/2305.14314)
- github：[QLoRA](https://github.com/artidoro/qlora)，[Demo](https://huggingface.co/spaces/uwnlp/guanaco-playground-tgi)
- 参考：[开源「原驼」爆火，iPhone都能微调大模型了，得分逼近ChatGPT！](https://mp.weixin.qq.com/s/RakazI25dMJz0JUkdtbr0w)

QLoRA 通过冻结的 4-bit 量化预训练语言模型向低秩适配器(LoRA) **反向传播**梯度。使用 4-bit NormalFloat (NF4) 量化、Double Quantization、Paged Optimizers、所有 Linear 层插入 adapter 等技术，QLoRA 在不牺牲性能的情况下大大节省了显存占用。

说明如下：
- **4bit NormalFloat**（NF4）：对于正态分布权重而言，一种信息理论上最优的新数据类型，该数据类型对于正态分布数据可以产生比 4 bit 整数和 4bit 浮点数更好的实证结果。
- **Double Quantization**：对第一次量化后的那些常量再进行一次量化，减少存储空间。
- **Paged Optimizers**：使用 NVIDIA 统一内存特性，实现了 CPU 和 GPU 之间自动的页面转换。当 GPU 内存不足时，Paged Optimizers 技术会自动将优化器状态转移到 CPU 内存，以确保优化器的正常运行。
- **All-Linear-Layer-Adapter**：在所有全连接层都插入 LoRA Adapter，增加了训练参数，能匹配16位全参数微调的性能。

- 减少内存使用量，足以在单个 **48GB** GPU 上微调 **65B** 参数模型，同时保留完整的 16 位微调任务性能。其中最好的模型称为 `Guanaco`，在 `Vincuna` 基准测试中优于之前公开发布的模型，并缩小了在 ChatGPT 上的差距，达到 ChatGPT 性能水平的 99.3%，同时仅在单个专业 GPU 上微调 24 小时。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/1e63b20d24a648bfaffa5d4e86266b65~tplv-obj:787:744.image?_iz=97245&from=post&x-expires=1692748800&x-signature=SEttWjvsni1S2XkoNgW7RHdIqiI%3D)

Q代表**量化**（Quantization），用低精度数据类型去逼近神经网络中的高精度浮点数，以提高运算效率

QLoRA 结合了 4-bit量化 和 LoRA，以及团队新创的三个技巧：
- 新数据类型 4-bit NormalFloat
- 分页优化器（Paged Optimizers）
- 双重量化（Double Quantization）

最终， QLoRA 让 4-bit的原驼在所有场景和规模的测试中匹配16-bit的性能。
- QLoRA的高效率让团队在华盛顿大学的小型GPU集群上每天可以微调LLaMA 100多次

两个关键结论：
- <span style='color:blue'>数据质量 >> 数据数量</span>
- 指令微调有利于**推理**，但不利于**聊天**

QLoRA可以用在手机上，论文共同一作Tim Dettmers估计以 iPhone 12 Plus的算力, 每个晚上能微调300万个单词的数据量。

特点
- 用 QLoRA 微调模型，可以显著降低对于显存的要求。
- 同时，模型训练的速度会**慢于**LoRA。


#### ReLoRA

【2023-8-21】[LoRA继任者ReLoRA登场，通过叠加多个低秩更新矩阵实现更高效大模型训练效果](https://www.toutiao.com/article/7269582259458572834)
- 论文链接：[paper](https://arxiv.org/abs/2307.05695)
- 代码仓库：[peft_pretraining](https://github.com/guitaricet/peft_pretraining)
- 过去十年中深度学习发展阶段中的一个核心原则就是不断的“堆叠更多层（stack more layers）. 那么继续以堆叠方式来提升低秩适应的训练效率

马萨诸塞大学洛厄尔分校将`ReLoRA`应用在具有高达350M参数的Transformer上时，展现出了与常规神经网络训练相当的性能。

此外，ReLoRA的微调效率会随着模型参数**规模增加而不断提高**，这使得其未来有可能成为训练超大规模（通常超过1B参数）LLMs的新型手段。

论文提出一种基于**低秩更新**的ReLoRA方法训练和微调高秩网络，其性能优于具有相同可训练参数数量的网络，甚至能够达到与训练100M+规模的完整网络类似的性能，对比效果如图所示。

从两个矩阵之和的秩入手
- 矩阵相加的后秩的上界会比较紧凑
- 对于矩阵 A, B，满足 Rank(A) < dim(A)，B同理, 使得矩阵之和的秩高于 A 或 B 

利用这一特性制定灵活的参数高效训练方法，然后从LoRA算法开始入手，LoRA可以将模型权重的更新量 delta(W) 分解为一组低秩矩阵乘积 

ReLoRA方法包含
- （1）初始化全秩训练
- （2）LoRA 训练
- （3）参数重新启动
- （4）锯齿状学习率调度（jagged learning rate schedule）
- （5）优化器参数部分重置。

作者选择目前非常火热的`自回归语言模型`进行实验，并且保证每个实验所使用的GPU计算时间不超过8天。


### MAM Adapter

一种在 Adapter、Prefix Tuning 和 LoRA 之间建立**联系**的统一方法。
- 最终的模型 MAM Adapter 是用于 FFN 的并行 **Adapter** 和 **软提示**的组合。

特点：
- 整体上来说，最终的模型MAM Adapter效果会优于单个高效微调方法。

### UniPELT

一种将不同的PELT方法LoRA、Prefix Tuning和Adapter作为子模块，并通过门控机制学习激活最适合当前数据或任务的方法。

特点：
- 相对于LoRA，BitFit，Prefix-tuning，训练的参数量更大；同时，推理更耗时；并且，输入会占用额外的序列长度。
- 多种 PELT 方法的混合涉及PLM 的不同部分对模型有效性和鲁棒性都有好处。

### LongLoRA

【2023-10-1】[贾佳亚韩松团队新作：两行代码让大模型上下文窗口倍增](https://www.toutiao.com/article/7284843466167796239)

只要两行代码+11个小时微调，就能把大模型**4k**的窗口长度提高到**32k**。

规模上，最长可以扩展到10万token，一口气就能读完长篇小说的多个章节或中短篇小说。

贾佳亚韩松联合团队提出的这个基于LoRA的全新大模型**微调**方法，登上了GitHub热榜，开源一周时间收获1k+ stars。这种方式叫做 `LongLoRA` ，由来自香港中文大学和MIT的全华人团队联合出品。

在一台8个A100组成的单机上，增大窗口长度的速度比全量微调快数倍。
- [论文地址](https://arxiv.org/abs/2309.12307)
- [GitHub项目页](https://github.com/dvlab-research/LongLoRA)


## （4）全量微调

**全面微调**：使用任务特定数据调整LLM的所有参数。
- 一个较小、任务特定、带标签的数据集上进行微调，调整一些模型参数，优化其对特定任务或一组任务的性能
- 全面微调： 所有模型参数都被更新，使其类似于预训练，只不过是在一个**带标签**且**规模较小**的数据集上进行。
- ![](https://pic2.zhimg.com/80/v2-e8c7286930eb81b57aaf109fe92ac58d_1440w.webp)
- 优点: 训练数据集更少、提高精度、增加鲁棒性
- 缺点: 高计算成本、内存需求高、时间/专业知识密集

# 结束