---
layout: post
title:  以数据为中心的AI Data-centric AI
date:   2024-05-10 12:00:00
categories: 大模型
tags: gpt ChatGPT 数据集 
excerpt: 数据质量直接决定模型上限，如何高效利用数据？
mathjax: true
permalink: /llm_data
---

* content
{:toc}

# Data-centric


## 数据 ＞ 模型

数据在模型训练中非常重要。
- 数据提升对于模型效果的提升至关重要，而模型的提升效果却不明显
- 很多研究人员开始研究**以数据为中心**，想办法加强数据的质量和数量， 而不过多考虑模型或固定数据集
- [img](http://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6eef698e52a64ce0ad3c23ceeab70042~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)


## 什么是 Data-centric AI


### Data-centric AI 定义

Data-centric 观点：
- 当今的AI系统更多由**数据**驱动，而非**模型架构**的变化驱动

Andrew Ng: ML团队80%的工作应该放在数据准备上，数据质量最重要，每个人都应该如此
>- Data-Centric AI is the discipline of systematically engineering the data used to build an AI system.
>- If 80 percent of our work is data preparation, then ensuring data quality is the important work of a machine learning team.

Data-centric AI 是一种搭建 AI 系统的新理念, 简称 `DCAI`
> Data-centric AI refers to a framework to develop, iterate, and maintain data for AI systems

### Data-centric AI framework

Data-centric AI 是指为人工智能系统开发、迭代和维护数据的框架。它涉及建立有效的训练数据、设计适当的推理数据、维护数据的相关任务和方法。

Data-centric AI 框架
- 训练数据开发
  - 数据收集、标注、准备、降维、增强
- 推理数据开发
  - 分布内评估
  - 分布外评估
  - 提示工程
- 数据维护
  - 数据理解、质量维护、存储检索

[图解](https://1feng.github.io/images/blog_images/data-centric-ai/01.png)
- ![](https://1feng.github.io/images/blog_images/data-centric-ai/01.png)

论文 [Data-centric Artificial Intelligence: A Survey](https://arxiv.org/pdf/2303.10158v2)


### Model-centric vs Data-centric


对比分析
- 模型为中心（model-centric）: 传统搭建AI模型,以迭代模型为主，数据相对固定
  - 聚焦于几个基准数据集，然后设计各式各样的模型去提高预测准确率。
  - model-centric问题
    - 没有考虑到实际应用中数据可能出现的各种问题，例如不准确的标签，数据重复和异常数据等。
    - 准确率高的模型只能确保很好地「拟合」了数据，并不一定意味着实际应用中会有很好的表现。
- 数据为中心(Data-centric) AI: 
  - 关注数据本身，而模型相对固定。
  - 采用 Data-centric AI的方法, 实际场景中会有更大的潜力，因为<span style='color:red'>数据很大程度上决定了模型能力的上限</span>。
  - Data-centric 更侧重于提高数据的质量和数量。


[图](http://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f3ad82df3cc8459d9c2c163918efd58f~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)来自论文
- 【2023-4-2】[Data-centric AI: Perspectives and Challenges](https://arxiv.org/pdf/2301.04819)

**数据为中心** 和 **模型为中心** 不是对立的，而是相辅相成
- 一方面，以模型为中心的方法可用于实现以数据为中心的人工智能目标。
  - 例如，利用生成模型，如 GAN 和扩散模型，来执行数据增强并生成更多高质量数据
- 另一方面，以数据为中心的人工智能可以促进以模型为中心的人工智能目标的改进。
  - 例如，增加的数据增强数据的可用性可以激发模型设计的进一步发展



### DCAI 演变

随着AI发展，组织形式也在不断演进，职责分化，诞生新的功能模块。

传统: 
- 流程: 由`数据工程师`完成数据标注、清洗、增强、聚合等工作，再由`机器学习工程师`完成模型训练，而`算法工程师`仅需关注算法的开发。

问题: 
- 数据管理成本高: 
  - 算力和存储未优化
  - 人力成本高, 主要靠算法工程师
  - 时间成本高
- 无法支持大规模应用: 
  - 人工管理数据, 到一定程度后,边际效应为0
  - 无法多维、多模态复杂查询
  - 稳定性差、安全性差

新的组织带来协作难度升级，也需要新范式来支持

职责分化
- `Data Ops`: 数据标注(25%), 数据清洗(25%), 数据增强(15%), 数据聚合(10%)
- `ML Ops`: 模型训练(10%), 数据识别(5%), 模型调参(5%), 机器学习运营(2%)
- `算法工程师`: 算法开发(3%)

图解
- [img](http://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1c1802020f1f46408f11f2b20abc244e~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)


### Data-centric AI 资料

综述
- 【2023-3】[Data-centric Artificial Intelligence: A Survey](https://arxiv.org/pdf/2303.10158v2)  ChatGPT 的成功的重要驱动力就是 data-centric。
- [Data-Centric AI 介绍](https://juejin.cn/post/7267852125618290707)

MIT: [Introduction to Data-Centric AI](https://dcai.csail.mit.edu/) 课程

Syllabus
-   **1/16/24**: [Data-Centric AI vs. Model-Centric AI](https://dcai.csail.mit.edu/2024/data-centric-model-centric/)
-   **1/17/24**: [Label Errors and Confident Learning](https://dcai.csail.mit.edu/2024/label-errors/)
-   **1/18/24**: [Advanced Confident Learning, LLM and GenAI applications](https://dcai.csail.mit.edu/2024/advanced-confident-learning/)
-   **1/19/24**: [Class Imbalance, Outliers, and Distribution Shift](https://dcai.csail.mit.edu/2024/imbalance-outliers-shift/)
-   **1/22/24**: [Dataset Creation and Curation](https://dcai.csail.mit.edu/2024/dataset-creation-curation/)
-   **1/23/24**: [Data-centric Evaluation of ML Models](https://dcai.csail.mit.edu/2024/data-centric-evaluation/)
-   **1/24/24**: [Data Curation for LLMs](https://dcai.csail.mit.edu/2024/data-curation-llms/)

Special topics from previous years
-   **1/24/23**: [Growing or Compressing Datasets](https://dcai.csail.mit.edu/2023/growing-compressing-datasets/)
-   **1/25/23**: [Interpretability in Data-Centric ML](https://dcai.csail.mit.edu/2023/interpretable-features/)
-   **1/26/23**: [Encoding Human Priors: Data Augmentation and Prompt Engineering](https://dcai.csail.mit.edu/2023/human-priors/)
-   **1/27/23**: [Data Privacy and Security](https://dcai.csail.mit.edu/2023/data-privacy-security/)


### OpenAI 多么重视数据

OpenAI工程师花了极大心血提升数据质量和数量，GPT模型迭代差异明显
- 训练数据: **小数据** → **较大**的高质量数据 → **更大**的高质量数据 → 高质量**人类标注**数据
- 推理数据: 对prompt进行复杂精细管理

`GPT-1` -> `GPT-2` -> `GPT-3` -> `GPT-4`:
- 模型架构相似
- 数据量不同:

|gpt模型|模型|数据量|
|---|---|---|
|`GPT-1`||4.8G,未过滤|
|`GPT-2`||40G,人工过滤|
|`GPT-3`||570G,从45T原石数据中过滤|
|`ChatGPT`/`GPT-4`||人工演示/标注|

![](https://pic1.zhimg.com/80/v2-60c87fe18fbe252849f4592086568688_1440w.webp)

## Data-centric 构成

data-centric两个重要部分: **合成数据**和**数据选择**。

常面临数据量不足的问题
- 首先, 采用合成数据方法, 提升数据数量。
- 而数据数量达到一定程度时，模型性能陷入瓶颈，难以通过数量来提升性能，此时，可以通过**数据选择**方法筛选出高质量数据。


综述
- [A Survey on Data Selection for Language Models](https://arxiv.org/pdf/2402.16827)

摘要
1. 分别从LM的五个learning stage介绍。
2. Task-specific Fine-tuning 部分通常有两类目标：（实际落地场景较多应用）
  1. 匹配真实数据分布：适用于数据量少的场景
  2. 多样化数据分布：
    1. 提高数据效能
      1. 数据集转化为图表示，knn寻找距离方差最大的数据点 -> 多样性；保留只有相同label邻近的数据点 -> 减少数据量。
      2. Self-influence score:  评估outlier等困难样本。 
      3. datamodels
    2. 增强鲁棒性


### DCAI 自动化

DCAI 研究方向划分为两个视角，即**自动化**程度和**人类协作**程度。
- 前者侧重于自动化流程的设计，后者则更加关注如何 human in the loop
- ![](https://1feng.github.io/images/blog_images/data-centric-ai/02.png)

三种Automation
- Programmatic automation：使用程序自动处理数据。程序通常是根据一些启发式和统计信息设计的，现阶段各类的 automate machine learning 的工作大都集中于此，例如各类 auto feature engineering 的方法
- Learning-based automation：通过优化学习自动化策略。例如，最小化目标函数，此类方法通常更灵活，适应性更强。例如基于强化学习的方法做超参数调整或基于 meta learning 来确定优化策略等
- Pipeline automation：跨多个任务的自动化调整优化策略。例如 tpot，autosklearn 这类工作，将数据处理，特征工程，模型调参等一系列任务放置在一个统一的 pipeline 里（Learning-based automation和Programmatic automation可以看作是pipeline automation中的一环）


三种Human Participation

从另一个角度来看，面向Human Participation的方法往往需要不同形式的人类参与。可以确定几个程度：
- Full participation：人类完全控制过程。需要全员参与的方法通常可以很好地符合人类的意图，但代价高昂，例如雇佣大量外包公司来做数据打标
- Partial participation：不需要人工全程参与，但是需要人类密集或持续地提供信息。例如，通过提供大量反馈或频繁交互。例如大名鼎鼎的RLHF。Active Learning 领域很多研究都是这个范畴
- Minimum participation：自动化的控制整个过程，只在少量需要时咨询人类。人类只有在收到提示或要求时才会参与。当遇到海量数据和人力预算有限时，这种方法非常合适


同样，人类参与的程度在一定程度上，反映了效率（更少的人力）和有效性（更好地与人类保持一致）之间的权衡
 

### 合成数据 Synthetic Data

#### Conclusion

Conclusion
1. 优秀的LLM合成数据的质量更高（推荐用GPT-4合成）。
2. 合成数据训练出的模型性能比真实数据更差且与任务的主观性呈负相关。
3. Few-shot合成数据通常比zero-shot合成数据的效果更好。
4. 盲目增加训练数据可能导致特定任务的性能下降。
5. 合成数据在多语言场景上有三种用法，均能够提升目标语种效果：
  1. 直接生成非目标语种数据
  2. 生成非目标语种数据后翻译成目标语种
  3. 直接生成目标语种的数据
6. 在合成数据之后再通过判别器过滤掉被判别为“合成数据”的数据能够提升合成数据的忠实度，但不一定能提高效果。

#### 论文

IT University of Copenhagen: [The Parrot Dilemma: Human-Labeled vs. LLM-augmented Data in Classification Tasks](https://arxiv.org/pdf/2304.13861.pdf)
1. 基于大型语言模型（LLMs）的数据增强：
  - 针对文本分类任务，每次使用GPT-4和Llama-2 70B生成与给定样本数据标签相同但内容**相似**的9个新样本。
2. **平衡**的数据增强策略：过采样少数类别以平衡数据集中的类别比例。
3. 温度调整：temperature为1，有助于增加生成样本的**多样性**。
4. 多样性评估：计算合成数据与用于合成的原始数据样本的余弦相似度（语义多样性）和token overlap的比例（词汇多样性），来评估生成数据的多样性。
5. 对比**零样本分类**的LLM：用FT小模型和zero-shot的LLM在文本分类任务上
6. LLMs在生成与现实世界数据分布一致的合成数据方面仍面临挑战。

Microsoft: [LLM-powered Data Augmentation for Enhanced Crosslingual Performance](https://arxiv.org/pdf/2305.14288)
1. 使用 Dolly-v2、StableVicuna、ChatGPT 和 GPT-4，来扩充三个多语言常识推理数据集
2. 评估了使用合成数据对较小的多语言模型进行微调的有效性，包括 mBERT 和 XLMR，并比较了使用英语生成的数据和目标语言生成的数据的效果。

Purdue University: [Synthetic Data Generation with Large Language Models for Text Classification: Potential and Limitations](https://arxiv.org/pdf/2310.07849)
1. 在不同文本分类任务中，使用LLM生成的合成数据训练出的模型性能与任务的主观性呈负相关。
2. 使用few-shot合成数据相比zero-shot可以提高生成数据的有效性。

Allen Institute for AI: [How Far Can Camels Go? Exploring the State of Instruction Tuning on Open Resources](https://arxiv.org/pdf/2306.04751)
1. 采用不同数据集（真实/合成）在多个特定任务上进行实验
2. 使用所有的数据集一起训练可以在达到最好的平均性能，但是在特定任务上性能会下降。
3. 盲目增加训练数据可能导致特定任务的性能下降。
4. 使用GPT合成数据训练有助于模型减少有害回复。

University of Toronto: [Generating Faithful Synthetic Data with Large Language Models: A Case Study in Computational Social Science](https://arxiv.org/pdf/2305.15041)

1. 合成数据的生成分布通常与研究人员关心的真实世界数据的分布不同（即不忠实）。为了提高合成数据的忠实度，在讽刺检测的任务中提出了三种策略：
  1. grounding（基础）：
    1. 合成示例相似数据(Parrot Dilemma这篇) or rewrite
  2. Filtering
    1. 训练一个bert模型专门用来判断数据是否是合成数据
  3. taxonomy-based generation（在prompt中指定讽刺类别以提高多样性）。
2. 三种策略都提高了分类器的性能，但grounding策略对于讽刺检测任务效果最好。


### 选择数据 Data Selection


#### 总结

Conclusion
1. PE数据选择方法成本较低，优先尝试。
2. Influential function方法可在小模型上计算，以降低成本，再将选择出的高质量数据集迁移到目标LLM上进行训练。
3. Datamodel 实现成本偏高，落地时只能在需要数据量小的场景应用。
4. 获得数据选择标准/选择好的高质量数据后，能够反作用于数据合成质量的提升。
5. 数据多样性不一定能提升效果。


#### 方法概览

Data Selection常用的四类方法

| Data Selection Solutions | Intro | Advantages | Weakness | 
| --- | --- | --- | --- | 
| 提示工程 `PE` | 通过Prompt Engineering 判断数据质量 | 实现简单，成本最低 | 依赖于LLM能力，不够domain-specific | 
| 影响函数 `Influential Function` | 通过计算数据间影响力函数，判断出对目标数据贡献大的训练集样本。 | 选择的数据质量高、可迁移性。| 实现成本较高，计算量大，耗时久。 |
| 数据建模 Datamodels | 对目标数据建立datamodel，判断对目标数据贡献大的训练集样本。 | 选择的数据质量高。 | 实现成本极高，实际场景难落地。 |
| 其它 Other | 利用与测试集数据的相似度来选择。 | 实现成本相对Influential function和data models较低。 | 数据质量难以保证。 |

#### (1) PE

论文

清华: [CRITIQUELLM: Scaling LLM-as-Critic for Effective and Explainable Evaluation of Large Language Model Generation](https://arxiv.org/pdf/2311.18702)
1. 通过PE对训练数据难度打分(1-3)，判断数据质量。
2. 设计数据合成与选择的pipeline: `few-shot生成` -> `质量打分` -> `zero-shot生成` -> `质量打分`



#### (2) Influence functions

论文
- Anthropic, [Studying Large Language Model Generalization with Influence Functions](Studying Large Language Model Generalization with Influence Functions)

Influence functions：
1. 评估训练集每个sample对Loss的影响
2. 计算模型参数^2维度的hessian矩阵 -> 对于LLM开销太大，使用 Eigenvalue-corrected Kronecker-Factored Approximate Curvature （EK-FAC）代替。
3. TF-IDF 过滤减少需要计算的sample数量（根据query选择TF-IDF得分top-10000的seqs）
4. query batching 一次性计算所有训练数据的梯度，且用低秩矩阵代替计算。
5. 实验针对不同query去计算其在训练集中 influential score高的样本


Danqi Chen
- [LESS: Selecting Influential Data for Targeted Instruction Tuning](https://arxiv.org/pdf/2402.04333)

1. Influential score的计算根据adam优化器作了改良，引入了m和v
2. 数据选择：将每个子任务的训练集数据与验证集数据计算influential score，选择其中score top5%作为选定数据。
3. 数据选择模型和最终使用的模型可以不同，所以可以用小模型进行data selection后再将选定的数据集应用于大模型ft

AI Lab
- [G-DIG: Towards Gradient-based DIverse and hiGh-quality Instruction Data Selection for Machine Translation]()
1. Influential score 计算根据梯度近似
2. 利用influential score筛选出高质量数据:
  1. 选择对seed 数据(人工挑选的256条高质量数据)均产生正向influential score的数据
3. 利用K-means聚类 + 重采样方法保证数据的多样性。

#### (3) Datamodels

MIT, [Datamodels: Predicting Predictions from Training Data](https://arxiv.org/pdf/2202.00622)
1. 给定一个训好的模型以及目标数据，建模预测出对目标数据的训练有帮助的训练数据，并去除噪声数据、发现泄漏数据等。
2. 对每个测试集的样本都需要建一个datamodel来分析，训练成本较高

MIT: [DsDm: Model-Aware Dataset Selection with Datamodels](https://arxiv.org/pdf/2401.12926v1)
1. 通过使用数据模型来估计训练子集对目标任务性能的影响，并选择使估计最小化的子集。
2. 选择与高质量数据相似度高的数据(Classifier/DSIR) 可能反而降低表现


#### 其它

Stanford
- [Data Selection for Language Models via Importance Resampling](https://arxiv.org/pdf/2302.03169)
1. 提出一种通过在降维的n-gram特征空间中估计重要性权重，并根据这些权重进行重采样数据选择的方法DSIR。
  - 本质上是利用与测试集数据的相似度来选择。
2. 定义了一种数据度量方法，称为KL reduction，计算使用数据选择方法选定的数据集与随机选择的数据集相比，在特征空间上相对于目标分布的KL散度的平均减少量。
  - KL reduction 的值越大，表示通过数据选择过程选定的数据集在特征空间上与目标分布的接近程度越高，即数据选择过程更有效。



# 结束