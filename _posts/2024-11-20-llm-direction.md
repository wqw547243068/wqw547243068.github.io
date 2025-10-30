---
layout: post
title:  LLM 发展方向
date:   2024-11-20 12:00:00
categories: 大模型
tags: LLM 大模型 AGI 世界模型 系统 快思考 慢思考 灾难 遗忘 幻觉 推理  可解释 大脑 类脑 json 缩放定律 鹦鹉 意识 o1 ttt ssm mamba 脉冲 自学习 符号主义 不确定 稳定 openai 测试时计算 模仿学习 强化学习
excerpt: 大模型会往哪个方向发展？
mathjax: true
permalink: /llm_direction
---

* content
{:toc}


# LLM 优化方向


【2023-6-16】知乎专题：[大模型LLM领域，有哪些可以作为学术研究方向？](https://www.zhihu.com/question/595298808/answer/3071907155)

- **模型层**：
  - GPT系列，多模态系列，视觉类SAM：原生的工具调用能力；
  - 安全性：加密，可信任，联邦学习；
  - 新模型，新范式：长文本建模，不需要RLHF等；
  - 涌现问题的研究、黑盒的研究；
  - 并行、运算、显存的优化。EL-Attention，ZeRo，剪枝部署，蒸馏压缩。
- **接口层**：
  - 私有化部署；
  - Adapter，prefix，Lora；
  - Fusing。
- **应用层**：
  - Visual ChatGPT，HuggingGPT，AutoGPT，LangChain；
  - Prompt工程，向量库，dense retrieval；
  - 自我纠错，自我迭代，chain of thought 加强；
  - 评测数据集、新时代下的新任务，generatice agents等

假设已经有 GPT-3.5 基础模型，一千张卡，思考能做什么？然后用小模型，比如LLaMa 7B去验证，如果成功，再慢慢加大到13B，30B，画出一条上升的曲线；不一定要scale到最大的模型，只要自己的结论能划出一条上升的曲线，那么这条曲线就可外推到更大。

源自知乎：[LessTalk](https://www.zhihu.com/question/595298808/answer/3071907155)

- 平台工具及工程化部署
- 小模型拟合大模型降低计算量
- 多模态的输入与输出
- Prompt Engineering
- 垂直领域应用 搜索+知识图谱、机器人、自动驾驶等

提纲
- 基础理论：大模型的基础理论是什么？
- 网络架构：Transformer是终极框架吗？
- 高效计算：如何使大模型更加高效？
- 高效适配：大模型如何适配到下游任务？
- 可控生成：如何实现大模型的可控生成？
- 安全可信：如何改善大模型中的安全伦理问题？
- 认知学习：如何使大模型获得高级认知能力？
- 创新应用：大模型有哪些创新应用？
- 数据评价：如何评估大模型的性能？
- 易用性：如何降低大模型的使用门槛？

作者：[zibuyu9](https://www.zhihu.com/question/595298808/answer/3047369015)

其它
- reasoning 逻辑推理：目前llm能力还不够的地方。比如能不能让llm做leetcode hard。进一步的，能不能自己创造新的知识，解决哥德巴赫猜想。
- compression and acceleration 模型压缩与加速：怎么把一个10b的模型弄到手机上并高速运行
- agent：怎么更好的给llm加上眼睛与手脚，让llm变成agent执行任务，并构造各种各样全新的benchmark。比如让agent发知乎回答以点赞多为目标。能不能通过RL把这件事做了?就和当年搞游戏ai一样。
- multi-modal 多模态：GPT-4没有开源，甚至没有技术细节，怎么做一个开源的逼近gpt-4的模型。mini-gpt4, llava是个不错的尝试。
- Hallucination 幻觉问题：GPT-4已经好了很多，但仍然没有完全解决。所以因此马斯克说要做TruthGPT. 要让LLM知之为知之不知为不知。这个难度其实很大。
- Evaluation。开源世界需要一套新的Evaluation的方法来评估llm的效果，从而方便推进开源llm的进展。
- dataset。这个是chatgpt被创造出来的源头。所以，能否多构建一个专家的数据库来帮助优化llm呢？每一份开源数据都非常有价值。

论文：[A PhD Student’s Perspective on Research in NLP in the Era of Very Large Language Models](https://arxiv.org/pdf/2305.12544.pdf)


【2025-6-15】Scaling What？堆数据/规模 → 拉长思维链 → context 情景智能

邱锡鹏教授：该Context了
- 第一阶段，靠“堆数据、加参数”，让模型变聪明；
- 第二阶段，拉长“思维链”提升推理能力。
- 第三阶段正在上演。新概念——Contextual Intelligence（情境智能）。场景、具身等信息


【2025-7-10】AGI实现的可能方向：
- 推理LLM（已经很多人批了，自回归可能行不通）
- 世界模型（yann lecun强推，难度大，处于早期）
- 其他非transformer模型（如ssm状态空间模型、snn脉冲神经网络等）
- 符号主义（因果推理、GNN图神经网络）、类脑（仿生）等。

openai的成功“破坏”了整个世界的技术认知，就像书籍《伟大不能被计划》一样，技术创新难以被精确预测

张钹院士在2024年8月初的ISC.AI 2024 人工智能峰会上，指出大模型的四个发展方向：
- 1、与人类对齐；
- 2、多模态生成；
- 3、AI Agent；
- 4、具身智能。

## 数据

大模型数据已经见底, 需要转型，从经验中学习

趋势: 人类数据 -> 经验数据

强化学习之父”、2024 年 ACM 图灵奖得主 `Richard Sutton` 在`新加坡国立大学`发表人工智能未来的演讲，系统地阐述了他对 AI 技术趋势、社会哲学及宇宙演化的前沿思考。
- AI 正经历从“人类**数据**时代”到“**经验**时代”的根本性转变，并强烈呼吁社会以**去中心化**的合作精神取代基于恐惧的**中心化**控制，勇敢地迎接一个由 AI 驱动的未来。

详见站内专题：[Data Centric](llm_data)

## 模型融合

【2024-8-8】[模型融合来袭！ChatGPT和Claude 杂交能变聪明10倍？](https://mp.weixin.qq.com/s/zUtQrKuQgyNivaxxrHX1hg)

### 什么是模型融合

什么是模型融合？
- 把多个AI模型的参数混合在一起，生成一个新模型。

简单, 但效果却出奇的好
- 不需要额外的数据和算力，只要把**模型权重**加减一下就行了。
- 融合后的模型还真能集各家之所长，性能明显提升。

比如 Prometheus-2 模型用这招把几个评估模型的能力融合到一起的

### 融合方法

常见方法：图见[原文](https://mp.weixin.qq.com/s/zUtQrKuQgyNivaxxrHX1hg)
- **线性**融合：最简单粗暴，直接对参数**加权平均**。虽然简单但出奇的有效。
- **任务向量**：把微调后的模型减去原始模型，得到一个"任务向量"。用这个向量做加减法，比如减掉有毒内容的任务向量，模型就能生成更干净的内容了。
- `TIES`融合：在任务向量基础上加了三板斧 - 修剪、选举和分离，可以去掉冗余权重、解决任务向量间的分歧。
- `DARE`融合：跟TIES思路类似，但用随机丢弃和重新缩放来去掉冗余权重。

论文链接：
- 任务向量：[paper](https://arxiv.org/abs/2212.04089)
- TIES：[paper](https://arxiv.org/abs/2306.01708)
- DARE：[paper](https://arxiv.org/abs/2311.03099)
- 嵌入向量融合：[paper](https://arxiv.org/abs/1912.00772)

工具 mergekit：
- [merge-models](https://huggingface.co/blog/mlabonne/merge-models)


### GaC

Gac: Generation as Classification

【2024-6-18】上海AI Lab 推出 [融合多个大模型新思路 --- Generation as Classification](https://zhuanlan.zhihu.com/p/715404265)

常打比赛的人(如Kaggle)很熟悉, 很多时候拼的就是各种**花式模型融合**, 将多个model融合(ensemble)后可以突破现有瓶颈, 神奇地让融合后的性能超过任何一个参与ensemble的单一模型。

ImageNet 视觉分类任务, 分类模型会输出一个维度为 1000 向量代表预测每个类别的概率，仅仅将多个模型的分类向量加起来后取平均, 就可以取得不错的准确率提升
- 原本最高的是 RepGhostNet 78.81%, 将三个模型融合后就提升到了 80.62%. 

类似地, 把LLM每个generation step都当成一次分类任务(Generation as Classification, GaC)去ensemble, 从而提升所生成的每个token的正确性, 并最终获得更好 response.

核心思想: LLM生成文本时, 每个generation step都由多个LLM共同决定下一个token要输出什么
- ![](https://pica.zhimg.com/80/v2-e8c84b1cf0e391ffe40b2a9fe2fc966a_1440w.webp)
- Paper Title: [Breaking the Ceiling of the LLM Community by Treating Token Generation as a Classification for Ensembling](https://arxiv.org/pdf/2406.12585)
- [GaC](https://github.com/yaoching0/GaC)

如何实施？

问题
- LLM 每步生成跟其**词汇表等长**的概率向量, 而 **LLMs 词汇表长度不一样**
- 比如: 
  - Llama3 词汇表长度 128256
  - Qwen2  词汇表长度 152064
- 这和ImageNet分类任务上所有模型都输出1000维度的向量不同.

直觉做法: 
- 对所有参与ensemble的LLM词汇表取**并集**得到 Vu, 并用**0-1矩阵**记录下原本LLM词汇表和 Vu **对应关系**. 
- 一个generation step中, 将每个LLM生成的**概率向量**乘以各自的0-1矩阵转换到 Vu 维度
- 随后再**取平均**并得到ensemble后的概率向量
- 再根据该向量sample出下一个token, 此时这个token就是由所有参与ensemble的LLM决定的
- 当选出一个token后, 每个LLM会用各自的tokenizer将这个token转换为各自的 token id(s), 并拼回到各自的输入中以进行下一个generation step.
- ![](https://pic4.zhimg.com/80/v2-007b5f3229ad47a81a4613587dfd4433_1440w.webp)

这种简单做法竟然打破现有的LLM社区天花板！(当然, 花费了更多计算量)
- ![](https://pica.zhimg.com/80/v2-21d29f4a7f9f30cba52ae96330720956_1440w.webp)

Qwen2 是 2024/06/07 退出, 拿它和实力相当的 llama3 进行融合, 各个指标上平均4%的提升! 达到 2024/06/07开源社区最好结果

该方法不受模型架构的限制, 随着新模型的释出还是可以不断的以新模型为基础继续推升天花板.


## 可控生成

【2023-7-10】[LLM 可控生成初探](https://mp.weixin.qq.com/s/BngY2WgCcpTOlvdyBNJxqA)

基于 LLM 的应用开发过程中，有几个挑战，包括：
- 如何避免“胡说八道”, 提升模型输出的**可靠性/稳定性**
- 控制模型的计算开销和响应速度等等

目前主流的解决手段包括：
- 更好的 prompt 设计
- 通过 retrieval 来做增强
- 与外部工具的结合
- 流程编排与产品设计
- 考虑使用 fine tune 模型或混合模型应用

|Prompt优化类型|latency|compute|
|---|---|---|
|Few-Shot CoT|??|??|
|Zero-Shot CoT|?|?|
|Decomposition|??|??|
|Ensembling|?|????|
|Self-Criticism|????|??|
||||

可控生成最直接的方案：
- 首先通过 prompt 告知 LLM 我们所需要的返回格式，并进行生成。
- 通过一些规则来检查返回结果，如果不符合格式，生成相关错误信息。
- 将上一次的生成内容和检查的错误信息告知 LLM，进行下一次的修正生成。
- 重复 2-3 步骤，直到生成的内容完全符合要求。

LLM 的可控性、稳定性、事实性、安全性等问题是推进企业级应用中非常关键的问题，下面这些项目在这方面做了很多探索，也有很多值得借鉴的地方。

总体思路上来说，主要是：
- 提供一套 prompt 模板定义，允许用户指定 LLM 生成的格式或内容主题。
- 在模板基础上，也有不少项目进一步设计了相应的编程语言，让 LLM 与确定性程序的交互更加直观。
- 提供各类 validator，保证生成内容符合预期，并且提供了自动处理/修正机制。
- 更进一步，也可以在生成前进行干预，例如在 prompt 中给近似案例，修改模型 decode 时的概率分布等。
- 其它在可控性基础上做的各种性能与开销的优化，例如缓存，减少 token 消耗量，对开源模型能力的挖掘等。

即使不直接使用上述的项目做开发，也可以从中学习到很多有用的思路。当然也非常期待这个领域出现更多有意思的想法与研究，以及 prompt 与编程语言结合能否碰撞出更多的火花。

详见原文：[LLM 可控生成初探](https://mp.weixin.qq.com/s/BngY2WgCcpTOlvdyBNJxqA)


### 输出稳定性

【2025-2-6】[【ICLR 2025】不确定性uncertainty相关论文汇总](https://zhuanlan.zhihu.com/p/21587790793)
- ICLR 2025中关于不确定分析、不确定性量化、不确定性+下游任务等相关的论文简单汇总
- 哈佛大学 [Provable Uncertainty Decomposition via Higher-Order Calibration](), 将模型预测不确定性分解为具有明确语义的随机和认知成分，这些成分与现实世界的数据分布相关联。
- [Credal Wrapper of Model Averaging for Uncertainty Estimation in Classification](https://openreview.net/pdf?id=cv2iMNWCsh) 提出 “credal wrapper”的创新方法，为贝叶斯神经网络 (BNN) 和深度集成 (DE) 制定模型平均的“credal set”表示，能够改善分类任务中的不确定性估计。
- [From Risk to Uncertainty: Generating Predictive Uncertainty Measures via Bayesian Estimation]() 逐点风险分解为与不同预测不确定性来源相关的成分：即随机不确定性（固有数据变异性）和认知不确定性（与模型相关的不确定性）。结合作为近似值的贝叶斯方法，我们构建了一个框架，允许生成不同的预测不确定性度量。
-  [DeLLMa: Decision Making Under Uncertainty with Large Language Models]() DeLLMa（决策大型语言模型助手），这是一个旨在提高不确定环境中决策准确性的框架。多步骤推理过程，该过程整合了扩展推理时间推理的最新最佳实践，借鉴了决策理论和效用理论的原理，以提供准确且可人工审核的决策过程。
-  复旦 [An Empirical Analysis of Uncertainty in Large Language Model Evaluations](https://openreview.net/pdf?id=J4xLuCt2kg) 2 种不同的评估设置中对 9 种广泛使用的 LLM 评估者进行了广泛的实验，LLM 评估者根据模型系列和大小表现出不同的不确定性, 采用特殊的提示策略（无论是在推理期间还是在训练后）可以在一定程度上缓解评估不确定性。通过利用不确定性来增强 LLM 在分布外 (OOD) 数据中的可靠性和检测能力，我们使用人工注释的微调集进一步微调了一个名为 ConfiLM 的不确定性感知 LLM 评估器
- 剑桥 [Do LLMs estimate uncertainty well in instruction-following?](https://openreview.net/pdf?id=IHp3vOVQO2) 首次系统地评估了 LLM 在指令遵循方面的不确定性估计能力

【2025-9-10】LLM技术论文：《如何解决LLM推理中的非确定性问题》

2025年2月, OpenAI前CTO `Mira Murati`成立公司 `Thinking Machines Lab`
- 第一篇文章，从底层技术的角度阐述LLM推理时的**非确定性**产生的原理，并在vLLM基础上实现确定性推理的演示。
- 原文 [Defeating Nondeterminism in LLM Inference](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)
- ![](https://pica.zhimg.com/70/v2-330bb4bddcf2bf8acac8725ea83d56a6_1440w.avis?source=172ae18b&biz_tag=Post)

OpenAI在上周正好发布为什么语言模型会产生幻觉的技术论文。
- 《为什么语言模型会产生幻觉》[解读](https://zhuanlan.zhihu.com/p/1948532556254389199)

最大的贡献:
- 清晰分析了当前推理引擎的工作机制，指出当前推理引擎因为效率优化，在batch计算的时候计算顺序不确定问题引入了`非结合律`带来的推理结果不确定，也就是前向传播 “`批次不变性`”（batch invariance）

解决后最大的收益
- 不确定性导致当前用vllm/sglang做roll out的RL训练并不是真的on policy，所以需要一些技巧避免训练崩。
- 而解决问题后虽然性能有降，但还能忍，而且是 true on policy RL，训练稳定性大幅提升。

LLM 幻觉的根本原因: <span style='color:red'>训练和评估流程奖励猜测行为而非承认不确定性</span>。
- 幻觉现象并非神秘莫测 —— 本质上源于**二元分类错误**。当错误陈述无法与事实区分时，预训练语言模型中的幻觉就会在自然的统计压力下产生。
- 大多数评估的评分方式 —— 语言模型被优化为**优秀的应试者**，在不确定时,进行猜测能够提高测试表现。这种惩罚不确定性回答的“普遍现象”只能通过社会技术层面的缓解措施来解决：修改现有基准测试的评分机制，这些基准测试存在偏差却主导着排行榜，而非引入额外的幻觉评估。

**可重现性**是科学进步的基石, 然而大语言模型重现结果极其困难
> 多次向ChatGPT询问同一个问题,得到不同结果。

这并不令人意外
- 语言模型获得结果, 需要“采样”——将语言模型输出, 转换为概率分布并概率性地选择token的过程。

更令人意外的是
- 即使将温度参数调整到0（理论上使采样过程变成确定性的），LLM API在实际应用中仍然不具有确定性。
- 即使在自有硬件上使用`vLLM`或`SGLang`等开源推理库运行推理，采样过程依然不是确定性的。


#### 并发+浮点数

为什么LLM推理引擎不具备确定性呢？
- 浮点数的**非结合性**特征与**并发执行**相结合，会根据并发核心的完成顺序产生非确定性结果。---- LLM推理非确定性的“并发+浮点数”假设

【2025-1-11】论文 《[Give Me FP32 or Give Me Death? Challenges and Solutions for Reproducible Reasoning](https://arxiv.org/pdf/2506.09501)》指出
- GPU浮点算术具有**非结合性**特征，即 `(a+b)+c ≠ a+(b+c)`，有限精度和舍入误差导致。
- 该特性直接影响transformer架构中注意力分数和logits的计算，其中跨多线程的并行操作会根据执行顺序产生不同结果。
- 速度权衡: 为了提高端点速度而使用GPU进行并行计算，这些计算具有非确定性。任何现代GPU神经网络计算都会受到这种影响。
- 由于GPU高度并行化，每次执行时加法或乘法的顺序可能不同，这种差异会级联放大到输出结果中。

#### 批次不变性与"确定性"

但这并非全貌。
- 即使在GPU上，对相同数据重复执行相同矩阵乘法运算，始终会得到按位相同的结果。
- 这里确实使用了浮点数运算，GPU也确实具有大量并发性，那么为什么在这种测试中看不到非确定性现象呢？

困惑
- GPU某些内核非确定性，然而，语言模型前向传播中使用的所有内核都是确定性的。
- LLM推理服务器（如vLLM）的前向传播过程确定，但是，从推理服务器用户的角度来看，结果却是非确定性的。

"并发+浮点数"假设未能准确定位问题根源，揭示LLM推理非确定性背后的真正原因，并说明如何消除非确定性，在LLM推理中获得真正可重现的结果。

机器学习模型通常被视为遵循`交换律`或`结合律`等结构规则的数学函数。

浮点数的非结合性 `(a+b)+c ≠ a+(b+c)`
- ![](https://picx.zhimg.com/v2-5dc2a1cb99ec75d9878431d83bfbf3f9_r.jpg)
- 两个具有不同“量级”（即不同指数）的浮点数相加时，都可能发生这种情况
- 1230 需要3位精度，表示23.4也需要3位精度。
- 然而，将这两个数字相加的结果需要5位精度才能表示（1253.4）。浮点数格式必须舍弃末尾的34。
- 从某种意义上说，这相当于在相加之前将原来的23.4四舍五入为20.0

以不同顺序对浮点数进行加法运算时，就可能得到完全不同的结果。

```py
import random

vals = [1e-10, 1e-5, 1e-2, 1]
vals = vals + [-v for v in vals]

results = []
random.seed(42)
for _ in range(10000):
    random.shuffle(vals)
    results.append(sum(vals))

results = sorted(set(results))
print(f"There are {len(results)} unique results: {results}")

# Output:
# There are 102 unique results: [-8.326672684688674e-17, -7.45931094670027e-17, ..., 8.326672684688674e-17]
```


浮点数之所以有用，是因为支持“动态”精度水平，破坏结合性的特征

内核为什么会以不同顺序进行数字加法运算的一个常见理论是“并发+浮点数”假设。
- 如果并发线程的完成顺序是非确定性的，而累积顺序又依赖于并发线程的完成顺序（例如使用原子加法操作），那么累积顺序也将是非确定性的。
- 虽然这种情况确实可能导致内核非确定性，但并发（和原子加法）与LLM推理的非确定性完全无关

GPU 在众多“核心”（即SM）上并发执行程序。
- 由于核心之间**缺乏固有的同步机制**，当核心需要相互通信时就面临挑战。
- 例如，如果所有核心都必须向同一个元素进行累积操作，可以使用“原子加法”（有时称为"fetch-and-add"）。

`原子加法`具有非确定性——结果累积的顺序完全取决于哪个核心先完成操作。
- ![](https://pica.zhimg.com/v2-9633691b449142c17b0d7dc8558eb8c4_b.webp)
- 原子加法确保每个核心的贡献都会反映在最终结果中。然而，它不保证贡献的添加顺序。顺序完全取决于哪个核心先完成，这是一个非确定性属性。
- 因此，多次执行相同的并行程序可能产生非确定性输出: 使用完全相同的输入执行同一个内核两次，却得到不同的结果 ———— 运行间非确定性

虽然并发`原子加法`确实会使内核产生非确定性，但对于绝大多数内核而言，`原子加法`并非必需。

实际上，在LLM的典型前向传播中，通常不存在任何原子加法操作。避免使用原子加法带来的性能损失微乎其微。
- 沿“批次”维度通常存在足够的并行性，因此无需沿归约维度进行并行化
- 随着时间推移，大多数神经网络库都采用了多种策略来在不牺牲性能的前提下实现确定性。

LLM 常用的此类操作只有FlashAttention的反向传播。
- 但是，LLM 前向传播不涉及任何需要原子加法的操作, 前向传播具有“运行间确定性”。

批次不变性与"确定性"

前向传播本身具有“确定性”并不足以确保包含它的系统具有确定性。

例如，如果请求的输出依赖于并行的用户请求（如批归一化），会怎样？由于每个单独的请求无法知道并行请求的内容，从它们的角度来看，整个LLM推理过程也是非确定性的

![](https://pic1.zhimg.com/v2-f1cf1f42afa9e66f97d8817d084c9cd8_1440w.jpg)

请求的输出确实依赖于并行用户请求。
- 这不是因为在批次间泄露了信息，而是因为前向传播缺乏"批次不变性"，导致请求的输出依赖于前向传播的批次大小


当非批不变的内核成为大型推理系统的组成部分时，整个系统就可能表现出非确定性。当用户向推理接口发出查询时，从用户角度来看，服务器所承受的负载实质上是“非确定性的”。负载决定了内核运行时的批次大小，进而影响每个独立请求的最终结果
- ![](https://picx.zhimg.com/v2-7dfa3bf67d7faf9946e73d763e8fa3a3_1440w.jpg)
- 虽然推理服务器本身可以被认为是“确定性的”，但从单个用户的角度来看情况有所不同。对于单个用户而言，其他并发用户并不是系统的“输入”，而是系统的非确定性属性。这使得LLM推理从每个用户的视角来看都是“非确定性的”

几乎所有LLM推理接口都表现出非确定性的根本原因在于负载（以及相应的批次大小）的非确定性变化！这种非确定性并非GPU所独有——基于CPU或TPU的LLM推理接口同样存在这一非确定性来源。

#### 如何实现内核的批次不变性？

要使transformer实现具备批次不变性，需要确保每个内核都具备批次不变性。

Transformer架构下，当前推理引擎里解决批次确定性问题主要在3个部分完成：`RMSNorm`、`矩阵乘法`（matmul）、`注意力`（attention）。

假设所有逐点运算都具备批次不变性。

因此，只需关注涉及归约操作的3种运算——`RMSNorm`、`矩阵乘法`和`注意力机制`。(按难度递增的顺序排列)

|操作|要点|改造方案|图解|
|---|---|---|---|
|RMSNorm|小batch时，原始实现会切换规约策略（比如分裂规约/atomic add），导致不同batch-size下结果不一致。|固定规约顺序，或者采用“数据并行”策略（每个batch元素独占一个核心），确保不同batch-size下计算顺序恒定。|![](https://pic2.zhimg.com/v2-351d6478f36e043306afa472cf6dc0b1_1440w.jpg)|
|矩阵乘法|当M、N维度较小，需要用Split-K并行或切换tensor core指令，不同情况会改变规约顺序|强制使用固定的kernel 配置（固定 tile 与tensor core指令），不随batch-size动态调整，即使有轻微性能损失，也保证计算路径一致|![](https://pic1.zhimg.com/v2-0922c2dd743513de66a6bd7e29f23d48_1440w.jpg)|
|注意力机制|KV Cache和新token分开规约，导致不同阶段（预填充和解码）的规约顺序不同。|对并行请求数量和推理引擎对请求的切分方式保持不变性|![](https://pica.zhimg.com/v2-e3fd306923d81e2c43587269ebcd32a6_1440w.jpg)|
||||

数据并行RMSNorm 
- 理想情况下，希望在并行化策略中避免核心间通信。实现方法是将每个批次元素分配给一个核心，从而确保每个归约操作完全在单个核心内完成。
- 这被称为“数据并行”策略，因为仅沿着不需要通信的维度进行并行化。在此例中，四行数据和四个核心实现了核心的充分利用。

改造
- 固定规约顺序，或采用“数据并行”策略（每个batch元素独占一个核心），确保不同batch-size下计算顺序恒定。

大批次的数据并行RMSNorm 
- 将数据并行策略扩展到更大批次相当直接——不是让每个核心处理一行数据，而是让每个核心依次处理多行数据。这种方法保持了批次不变性，因为每个批次元素的归约策略保持一致

数据并行矩阵乘法 
- 与RMSNorm类似，矩阵乘法的标准并行策略是 数据并行 策略，将整个归约保持在单个核心中。
- 最直观的方法是将输出张量分割为2D tile，并将每个tile分配给不同的核心。每个核心然后计算属于该tile的点积，再次在单个核心内执行完整的归约。

问题
- 当M、N维度较小，需要用Split-K并行或切换tensor core指令，不同情况会改变规约顺序。

改造方案
- 强制使用固定的kernel 配置（固定 tile 与tensor core指令），不随batch-size动态调整，即使有轻微性能损失，也保证计算路径一致。

矩阵乘法可以看作逐点运算后跟随归约操作


主演问题推理时，KV Cache和新token分开规约，导致不同阶段（预填充和解码）的规约顺序不同。

解码阶段 query 很短：为了让GPU饱和，需要用Split-KV并行；常见的“平均切分”策略会随batch-size变化而改变规约顺序。

解决方案就是对并行请求数量和推理引擎对请求的切分方式保持不变性。
- 一是在进入注意力kernel前统一更新KV cache，保证K/V布局一致。
- 二使用固定分裂大小（fixed split-size）策略，不随batch-size改变分裂方式，从而保证规约顺序始终一致。

FlashAttention2策略 
- 沿Q方向并行化，同时沿K/V方向归约。这意味着整个归约可以保持在单个核心内，使其成为另一种数据并行策略。

#### 实现

vLLM基础上实现确定性推理的演示，利用了其FlexAttention后端和torch.Library。通过torch.Library，可以以非侵入性方式替换大部分相关的PyTorch操作符。

Qwen/Qwen3-235B-A22B-Instruct-2507 模型，在温度0设置下使用提示词"Tell me about Richard Feynman"（非思考模式）采样1000个完成结果，每个生成1000个token。
- 结果显示生成了80个不同的完成结果，其中最常见的出现78次。

通过分析完成结果的差异位置，发现前102个token完全相同！首次出现分歧的位置是第103个token。所有完成结果都生成序列"Feynman was born on May 11, 1918, in"，但随后992个完成结果生成"Queens, New York"，而8个完成结果生成"New York City"。

相比之下，启用批不变内核后，所有1000个完成结果都完全相同。这符合对采样器的数学预期，但如果没有批不变内核就无法实现确定性结果。

单GPU运行Qwen-3-8B的API服务器，请求1000个输出长度在90到110之间的序列。

### guardrails

guardrails 项目将上述步骤做了进一步的抽象与封装，提供更加 high level 的配置与 API 来完成整个过程。其主要的组成部分包括：
- 定义了一套 RAIL spec，用来描述上面第 1 点提到的返回格式限定。除了 output schema 的定义外，RAIL目前也支持 input schema，prompt 模板，以及 instructions 等其它配置。
- 提供了一系列的 validation 机制，对应上面的第 2 点。对于 validate 失败的部分，会保留其在 output schema 中的位置，生成相应的错误信息。
- 通过 ReAsk 类来实现上面的第 3 点，发送给 LLM 的内容会更聚焦于错误信息部分，且保留了结构，更便于 LLM 理解和处理。
- 其它像常用 prompt 模板之类的功能。

### NeMo-Guardrails

NeMo-Guardrails
- 来自 Nvidia 的一个同名项目，比 guardrails 更有野心，想要确保 LLM 应用整体的**可信度**，**无害性**以及数据**安全性**等，而不仅仅只是输出的结构化检查和修复。
- 因此其实现思路上也复杂不少，设计了一种专门的 Colang 语言，来支持更加通用多样的业务流，而不仅仅是**生成 -> 检查 -> 修复**。
- 这个项目会更专注于用户与 LLM 的对话式交互应用，主要的设计都是围绕这个前提展开。

### guidance

guidance
- 微软推出的开源项目，几个作者看头像就很知名，分别是 shap，lime，checklist 的作者。之前有研究过 可解释机器学习的同学应该不会陌生。从 explainable ai 到 controlable llm，倒也是很说得通的发展路径

guardrails 中的做法是在 prompt 中给出说明和示范，希望 LLM 能够遵循指令来输出。但现实中往往会出现各种问题，例如额外带了一些其它的文字说明，或者生成的 json 格式不正确等，所以需要后续的 **ReAsk 来进行修正**。

LangChain 里也提供了各种 output parser 来帮忙提取回复中的结构化信息部分，但也经常容易运行失败。

在 guidance 中，同样是通过“模板语言”来定义 LLM 的输出结构，以确保输出格式的正确性。这个结构比起 xml 来说会更易写易理解些

guidance 将更加复杂的 Handlebars 模板 融入到了 prompt 中，使得原先需要复杂设计的 LLM 生成与程序处理交互过程可以很方便地在 prompt 中直接完成。
- 上面的例子中，只有当调用到`{{gen}}`命令时，才会触发 LLM 的生成操作。另外也有像`{{select}}`，`{{#geneach}}`，函数调用，逻辑判断，控制流等命令，有种结合了自然语言与编程语言两者长处的感觉。

除了 prompt 模板编程能力外，guidance 还有一系列高级特性，包括：
- 支持 hidden block，例如 LLM 的一些推理过程可能并不需要暴露给最终用户，就可以灵活利用这个特性来生成一些中间结果。
- Generation caching，自动把已经生成过的结果缓存起来，提升速度。
- 支持 HuggingFace 模型的 guidance acceleration，进一步提升生成速度。
- Token healing，不看这个我还不知道 LLM 有这种问题……
- Regex pattern guide，在模板的基础上进一步通过正则表达来限定生成的内容规范。

### lmql

在 guidance 的基础上，lmql 项目进一步把“prompt 模板”这个概念推进到了一种新的编程语言，倒是有点像前面 guardrails 跟 NeMo-Guardrails 的关系。项目本身提供了很漂亮的 playground 方便试用，注意如果要在本地玩这个项目，需要升级到 Python 3.10 的版本。


### Json 控制

【2024-8-6】[程序员窃喜！卡了大模型脖子的Json输出，OpenAI终于做到了100%正确](https://mp.weixin.qq.com/s/E2aXlQVzaFQUlFNDjUr-SQ)
- [Introducing Structured Outputs in the API](https://openai.com/index/introducing-structured-outputs-in-the-api)

大模型的 json 格式饱受诟病。经常遇到模型不遵循指令，不按格式输出，即使在 prompt 中明确说了要按照指定格式（比如Json、XML）返回结果，但是它就是不听话。

OpenAI 给 GPT-4o 模型升级到`2024-08-06`版本，带来全新功能：
- API 中引入了`结构化输出`（Structured Outputs）

模型输出现在可靠地遵循开发人员提供的 JSON 模式, 实现输出JSON的**100%准确率**

之前开发者通过第三方开源工具，或在 prompt 上面做功夫，让大模型遵循你的命令，再或者反复重试请求来绕过LLMs在结构化处理的缺陷，现在都不需要

两种办法：
- （1）函数调用: 在函数定义中设置 strict：true进行结构化输出；
- （2）新增response_format 参数选项

如何实现？
- 对于特定复杂JSON架构进行模型训练，Openai通过这种方法能把模型准确率提到**93%**。
  - 相较于最开始带JSON模式的GPT-4的**40%**准确率，已经高出很多了。
  - 但是模型本质上还是不确定，无法保证JSON的稳定输出
- OpenAI使用了约束解码（constrained decoding）技术。
  - 默认情况下，大模型在进行token输出时，可在词汇表中选择**任意**词汇，作为下一个输出token。而这种**不可控性**会让模型在输出一些固定格式的文本时犯格式错误。
  - 而使用动态约束解码技术后，大模型在下一个token输出时，便增加了一些约束，将模型限制在有效的token内，而不是所有token。
  - 比如：输入“`{"val`”后，下一个生成的文本一定不会是“`{`”。
  - 大模型不仅可以实现JSON格式正确，还可实现合适schema结构精确。

现在OpenAI已经通过这种方式实现了100% JSON输出准确率。

缺陷
- 额外增加Schema预处理时间，新模型在请求新的JSON Schema时慢些。
- 要使用结构化输出还有一些限制：
  - 目前结构化仅支持输出一部分JSON模式，包括 String、Number、Boolean、Object、Array、Enum和anyOf。
  - 同时，所有字段或者函数参数必须是“required”。
- **对象对嵌套**深度和大小也有限制。
  - 一个架构总共最多可以有 100 个对象属性，最多有 5 个嵌套级别。
  - OpenAI还留了个底：**结构化输出并不能防止所有类型的模型错误**。模型可能仍会在JSON对象的值中犯错误（比如在数学方程式中步骤出错），如果出现错误，需要使用者在指令提示词中提供示例，或者将任务拆分为更简单的子任务。
- 安全。结构化输出功能将遵守OpenAI现有的安全政策，并且仍会拒绝不安全的请求。甚至他们在API响应上设置了一个新字符串值，让开发人员能以编程方式，检测模型是否拒绝生成。


## 知识植入 


LLMs 依然会受到**知识截断**和**谬误**问题的限制。例如，ChatGPT 和 LlaMA 等 LLMs 仅具备截至训练最后时点的信息，也可能会因预训练数据中的偏见和差异生成不准确或误导性的输出。因此，高效更新 LLMs 的参数化知识进而调整特定行为，变得至关重要。

解决办法
- 尽管**微调**和**参数高效微调**可以修改 LLMs，但成本较高，还可能导致 LLMs 失去预训练所得能力，并且其修改也不总能泛化到相关输入。
- 使用**手动编写**或**检索**的提示影响 LLMs 的输出，但这类方法没有参数更新，可靠性不足。


### 知识编辑 

为了使不相关输入的影响最小化，并迅速有效地修改 LLMs 的行为，一种可行的解决方案是**知识编辑**。关于 LLMs 的知识编辑研究在各种任务和设置下取得显著进展，包括 `Memory based`、`Meta-learning` 和 `Locate-Then-Edit` 三类方法。

Methods

(1) [Preserve Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#preserve-parameters)
- ① [Memory-based](https://github.com/zjunlp/KnowledgeEditingPapers#memory-based)
1.  **Memory-Based Model Editing at Scale** (ICML 2022)  
  - Eric Mitchell, Charles Lin, Antoine Bosselut, Christopher D. Manning, Chelsea Finn. \[[paper](https://arxiv.org/abs/2206.06520)\] \[[code](https://github.com/eric-mitchell/serac)\] \[[demo](https://sites.google.com/view/serac-editing)\]
2.  **Fixing Model Bugs with Natural Language Patches**. (EMNLP 2022)  
    Shikhar Murty, Christopher D. Manning, Scott M. Lundberg, Marco Túlio Ribeiro. \[[paper](https://arxiv.org/abs/2211.03318)\] \[[code](https://github.com/MurtyShikhar/LanguagePatching)\]
3.  **MemPrompt: Memory-assisted Prompt Editing with User Feedback**. (EMNLP 2022)  
    Aman Madaan, Niket Tandon, Peter Clark, Yiming Yang. \[[paper](https://arxiv.org/abs/2201.06009)\] \[[code](https://github.com/madaan/memprompt)\] \[[page](https://memprompt.com/)\] \[[video](https://www.youtube.com/watch?v=Ld7R02bOiNQ&t=1s)\]
4.  **Large Language Models with Controllable Working Memory**.  
    Daliang Li, Ankit Singh Rawat, Manzil Zaheer, Xin Wang, Michal Lukasik, Andreas Veit, Felix Yu, Sanjiv Kumar. \[[paper](https://arxiv.org/abs/2211.05110)\]
5.  **Can We Edit Factual Knowledge by In-Context Learning?**  
    Ce Zheng, Lei Li, Qingxiu Dong, Yuxuan Fan, Zhiyong Wu, Jingjing Xu, Baobao Chang. \[[paper](https://arxiv.org/abs/2305.12740)\]
6.  **Can LMs Learn New Entities from Descriptions? Challenges in Propagating Injected Knowledge**  
    Yasumasa Onoe, Michael J.Q. Zhang, Shankar Padmanabhan, Greg Durrett, Eunsol Choi. \[[paper](https://arxiv.org/abs/2305.01651)\]
7.  **MQUAKE: Assessing Knowledge Editing inLanguage Models via Multi-Hop Questions**  
    Zexuan Zhong, Zhengxuan Wu, Christopher D. Manning, Christopher Potts, Danqi Chen.  
    .\[[paper](https://arxiv.org/abs/2305.14795)\]

- ② [Additional Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#additional-parameters)
1.  **Calibrating Factual Knowledge in Pretrained Language Models**. (EMNLP 2022)  
    Qingxiu Dong, Damai Dai, Yifan Song, Jingjing Xu, Zhifang Sui, Lei Li. \[[paper](https://arxiv.org/abs/2210.03329)\] \[[code](https://github.com/dqxiu/CaliNet)\]
2.  **Transformer-Patcher: One Mistake worth One Neuron**. (ICLR 2023)  
    Zeyu Huang, Yikang Shen, Xiaofeng Zhang, Jie Zhou, Wenge Rong, Zhang Xiong. \[[paper](https://arxiv.org/abs/2301.09785)\] \[[code](https://github.com/ZeroYuHuang/Transformer-Patcher)\]
3.  **Aging with GRACE: Lifelong Model Editing with Discrete Key-Value Adaptors**.  
    Thomas Hartvigsen, Swami Sankaranarayanan, Hamid Palangi, Yoon Kim, Marzyeh Ghassemi. \[[paper](https://arxiv.org/abs/2211.11031)\] \[[code](https://github.com/thartvigsen/grace)\]
4.  **Neural Knowledge Bank for Pretrained Transformers**  
    Damai Dai, Wenbin Jiang, Qingxiu Dong, Yajuan Lyu, Qiaoqiao She, Zhifang Sui. \[[paper](http://arxiv.org/abs/2208.00399)\]

- ③ [Change LM's representation space](https://github.com/zjunlp/KnowledgeEditingPapers#change-lms-representation-space)

1.  **Inspecting and Editing Knowledge Representations in Language Models**  
  - Evan Hernandez, Belinda Z. Li, Jacob Andreas. \[[paper](http://arxiv.org/abs/2304.00740)\] \[[code](https://github.com/evandez/REMEDI)\]

（2）[Modify Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#modify-parameters)

① [Finetuning](https://github.com/zjunlp/KnowledgeEditingPapers#finetuning)

1.  **Plug-and-Play Adaptation for Continuously-updated QA**. (ACL 2022 Findings)  
  - Kyungjae Lee, Wookje Han, Seung-won Hwang, Hwaran Lee, Joonsuk Park, Sang-Woo Lee. \[[paper](https://arxiv.org/abs/2204.12785)\] \[[code](https://github.com/wookjeHan/Plug-and-Play-Adaptation-for-Continuously-updated-QA)\]
2.  **Modifying Memories in Transformer Models**.  
  - Chen Zhu, Ankit Singh Rawat, Manzil Zaheer, Srinadh Bhojanapalli, Daliang Li, Felix Yu, Sanjiv Kumar. \[[paper](https://arxiv.org/abs/2012.00363)\]
    

②  [Meta-learning](https://github.com/zjunlp/KnowledgeEditingPapers#meta-learning)

1.  **Editing Factual Knowledge in Language Models**.  
  - Nicola De Cao, Wilker Aziz, Ivan Titov. (EMNLP 2021) \[[paper](https://arxiv.org/abs/2104.08164)\] \[[code](https://github.com/nicola-decao/KnowledgeEditor)\]
2.  **Fast Model Editing at Scale**. (ICLR 2022)  
  - Eric Mitchell, Charles Lin, Antoine Bosselut, Chelsea Finn, Christopher D. Manning. \[[paper](https://arxiv.org/abs/2110.11309)\] \[[code](https://github.com/eric-mitchell/mend)\] \[[page](https://sites.google.com/view/mend-editing)\]
3.  **Editable Neural Networks**. (ICLR 2020)  
  - Anton Sinitsin, Vsevolod Plokhotnyuk, Dmitry V. Pyrkin, Sergei Popov, Artem Babenko. \[[paper](https://arxiv.org/abs/2004.00345)\] \[[code](https://github.com/xtinkt/editable)\]
    

③ [Locate and edit](https://github.com/zjunlp/KnowledgeEditingPapers#locate-and-edit)

1.  **Editing a classifier by rewriting its prediction rules**. (NeurIPS 2021)  
  - Shibani Santurkar, Dimitris Tsipras, Mahalaxmi Elango, David Bau, Antonio Torralba, Aleksander Madry. \[[paper](https://proceedings.neurips.cc/paper/2021/hash/c46489a2d5a9a9ecfc53b17610926ddd-Abstract.html)\] \[[code](https://github.com/MadryLab/EditingClassifiers)\]
2.  **Language Anisotropic Cross-Lingual Model Editing**.  
  - Yang Xu, Yutai Hou, Wanxiang Che. \[[paper](https://arxiv.org/abs/2205.12677)\]
3.  **Repairing Neural Networks by Leaving the Right Past Behind**.  
  - Ryutaro Tanno, Melanie F. Pradier, Aditya Nori, Yingzhen Li. \[[paper](https://arxiv.org/abs/2207.04806)\]
4.  **Locating and Editing Factual Associations in GPT**. (NeurIPS 2022)  
  - Kevin Meng, David Bau, Alex Andonian, Yonatan Belinkov. \[[paper](https://arxiv.org/abs/2202.05262)\] \[[code](https://github.com/kmeng01/rome)\] \[[page](https://rome.baulab.info/)\] \[[video](https://www.youtube.com/watch?v=_NMQyOu2HTo&t=0)\]
5.  **Mass-Editing Memory in a Transformer**.  
  - Kevin Meng, Arnab Sen Sharma, Alex Andonian, Yonatan Belinkov, David Bau. \[[paper](https://arxiv.org/abs/2210.07229)\] \[[code](https://github.com/kmeng01/memit)\] \[[page](https://memit.baulab.info/)\] \[[demo](https://memit.baulab.us/#/)\]
6.  **Editing models with task arithmetic** .  
  - Gabriel Ilharco, Marco Tulio Ribeiro, Mitchell Wortsman, Ludwig Schmidt, Hannaneh Hajishirzi, Ali Farhadi. \[[paper](https://openreview.net/pdf?id=6t0Kwf8-jrj)\]
7.  **Editing Commonsense Knowledge in GPT** .  
  - Anshita Gupta, Debanjan Mondal, Akshay Krishna Sheshadri, Wenlong Zhao, Xiang Lorraine Li, Sarah Wiegreffe, Niket Tandon. \[[paper](https://arxiv.org/abs/2305.14956)\]
8.  **Do Language Models Have Beliefs? Methods for Detecting, Updating, and Visualizing Model Beliefs**.  
  - Peter Hase, Mona Diab, Asli Celikyilmaz, Xian Li, Zornitsa Kozareva, Veselin Stoyanov, Mohit Bansal, Srinivasan Iyer. \[[paper](https://arxiv.org/pdf/2111.13654.pdf)\] \[[code](https://github.com/peterbhase/SLAG-Belief-Updating)\]
9.  **Detecting Edit Failures In Large Language Models: An Improved Specificity Benchmark** .  
  - Jason Hoelscher-Obermaier, Julia Persson, Esben Kran, Ioannis Konstas, Fazl Barez. \[[paper](https://arxiv.org/abs/2305.17553)\]
10.  **Knowledge Neurons in Pretrained Transformers**.(ACL 2022)  
  - Damai Dai , Li Dong, Yaru Hao, Zhifang Sui, Baobao Chang, Furu Wei.\[[paper](http://arxiv.org/abs/2104.08696)\] \[[code](https://github.com/Hunter-DDM/knowledge-neurons)\] \[[code by EleutherAI](https://github.com/EleutherAI/knowledge-neurons)\]
11.  **LEACE: Perfect linear concept erasure in closed form** .  
  - Nora Belrose, David Schneider-Joseph, Shauli Ravfogel, Ryan Cotterell, Edward Raff, Stella Biderman. \[[paper](https://arxiv.org/abs/2306.03819)\]
12.  **Transformer Feed-Forward Layers Are Key-Value Memories**. (EMNLP 2021)  
  - Mor Geva, Roei Schuster, Jonathan Berant, Omer Levy. \[[paper](https://arxiv.org/abs/2012.14913)\]
13.  **Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space**.(EMNLP 2022)  
  - Mor Geva, Avi Caciularu, Kevin Ro Wang, Yoav Goldberg. \[[paper](https://arxiv.org/abs/2203.14680)\]
14.  **PMET: Precise Model Editing in a Transformer.**  
  - Xiaopeng Li, Shasha Li, Shezheng Song, Jing Yang, Jun Ma, Jie Yu. \[[paper](https://arxiv.org/abs/2308.08742)\] \[[code](https://github.com/xpq-tech/PMET.git)\]
    

（3） [More Related Papers](https://github.com/zjunlp/KnowledgeEditingPapers#more-related-papers)

1.  **FRUIT: Faithfully Reflecting Updated Information in Text**. (NAACL 2022)  
    Robert L. Logan IV, Alexandre Passos, Sameer Singh, Ming-Wei Chang. \[[paper](https://github.com/zjunlp/KnowledgeEditingPapers/blob/main)\] \[[code](https://github.com/zjunlp/KnowledgeEditingPapers/blob/main)\]
    
2.  **Entailer: Answering Questions with Faithful and Truthful Chains of Reasoning**. (EMNLP 2022)  
    Oyvind Tafjord, Bhavana Dalvi Mishra, Peter Clark. \[[paper](https://arxiv.org/abs/2210.12217)\] \[[code](https://github.com/allenai/entailment_bank)\] \[[video](https://www.youtube.com/watch?v=GYTJ_Pxva7Q)\]
    
3.  **Towards Tracing Factual Knowledge in Language Models Back to the Training Data**.  
    Ekin Akyürek, Tolga Bolukbasi, Frederick Liu, Binbin Xiong, Ian Tenney, Jacob Andreas, Kelvin Guu. (EMNLP 2022) \[[paper](https://arxiv.org/abs/2204.12785)\]
    
4.  **Prompting GPT-3 To Be Reliable**.  
    Chenglei Si, Zhe Gan, Zhengyuan Yang, Shuohang Wang, Jianfeng Wang, Jordan Boyd-Graber, Lijuan Wang. \[[paper](https://arxiv.org/abs/2210.09150)\]
    
5.  **Patching open-vocabulary models by interpolating weights**. (NeurIPS 2022)  
    Gabriel Ilharco, Mitchell Wortsman, Samir Yitzhak Gadre, Shuran Song, Hannaneh Hajishirzi, Simon Kornblith, Ali Farhadi, Ludwig Schmidt. \[[paper](https://arxiv.org/abs/2208.05592)\] \[[code](https://github.com/mlfoundations/patching)\]
    
6.  **Decouple knowledge from paramters for plug-and-play language modeling** (ACL2023 Findings)  
    Xin Cheng, Yankai Lin, Xiuying Chen, Dongyan Zhao, Rui Yan.\[[paper](http://arxiv.org/abs/2305.11564)\] \[[code](https://github.com/Hannibal046/PlugLM)\]
    
7.  **Backpack Language Models**  
    John Hewitt, John Thickstun, Christopher D. Manning, Percy Liang. \[[paper](https://arxiv.org/pdf/2305.16765.pdf)\]
    
8.  **Learning to Model Editing Processes**. (EMNLP 2022)  
    Machel Reid, Graham Neubig. \[[paper](https://aclanthology.org/2022.findings-emnlp.280.pdf)\]

 [Analysis](https://github.com/zjunlp/KnowledgeEditingPapers#analysis)

1.  **Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models.**  
    Peter Hase, Mohit Bansal, Been Kim, Asma Ghandeharioun. \[[paper](https://arxiv.org/pdf/2301.04213.pdf)\] \[[code](https://github.com/google/belief-localization)\]
2.  **Dissecting Recall of Factual Associations in Auto-Regressive Language Models**  
    Mor Geva, Jasmijn Bastings, Katja Filippova, Amir Globerson. \[[paper](https://arxiv.org/abs/2304.14767)\]
3.  **Evaluating the Ripple Effects of Knowledge Editing in Language Models**  
    Roi Cohen, Eden Biran, Ori Yoran, Amir Globerson, Mor Geva. \[[paper](https://arxiv.org/abs/2307.12976)\]
4.  **Edit at your own risk: evaluating the robustness of edited models to distribution shifts.**  
    Davis Brown, Charles Godfrey, Cody Nizinski, Jonathan Tu, Henry Kvinge. \[[paper](https://arxiv.org/abs/2303.00046)\]


#### FastEdit 北航

快速注入知识

- 【2022-2-10】Rank-One Model Editing (ROME): [Locating and Editing Factual Associations in GPT](https://arxiv.org/abs/2202.05262), [demo](https://rome.baulab.info/)

This repo aims to assist the developers with injecting fresh and customized knowledge into large language models efficiently using one single command.

Supported Models
-   [GPT-J](https://huggingface.co/EleutherAI/gpt-j-6b) (6B)
-   [LLaMA](https://github.com/facebookresearch/llama) (7B/13B)
-   [LLaMA-2](https://huggingface.co/meta-llama) (7B/13B)
-   [BLOOM](https://huggingface.co/bigscience/bloomz) (7.1B)
-   [Falcon](https://huggingface.co/tiiuae/falcon-7b) (7B)
-   [Baichuan](https://huggingface.co/baichuan-inc/Baichuan-7B) (7B/13B)
-   [InternLM](https://github.com/InternLM/InternLM) (7B)

[Implemented Algorithms](https://github.com/hiyouga/FastEdit#implemented-algorithms)
-   [Rank-One Model Editing (ROME)](https://arxiv.org/abs/2202.05262)


```sh
git clone https://github.com/hiyouga/FastEdit.git
conda create -n fastedit python=3.10
conda activate fastedit
cd FastEdit
pip install -r requirements.txt
# 或
pip install pyfastedit
```

Model Editing

```sh
CUDA_VISIBLE_DEVICES=0 python -m fastedit.editor \
    --data data/example.json \
    --model EleutherAI/gpt-j-6b \
    --config gpt-j-6b \
    --template default
```

#### EasyEdit 浙大 -- 开源

【2023-8-16】[浙大出品：大模型轻松获取“世界知识”，比传统微调效果更好](https://www.toutiao.com/article/7267801834855727679)
- 知识编辑 papaerlist: [Knowledge Editing for LLMs Papers](https://github.com/zjunlp/KnowledgeEditingPapers)
- 【2023-5-23】[Editing Large Language Models: Problems, Methods, and Opportunities](https://arxiv.org/abs/2305.13172)
- ![](https://github.com/zjunlp/KnowledgeEditingPapers/raw/main/img/overview.jpg)

浙江大学和东海实验室的研究团队提出了一个易于使用的 LLMs 知识编辑框架——`EasyEdit`，该框架支持各种知识编辑方法，且可以轻松应用于众多 LLMs，如 T5、GPT-J 和 LlaMA 等。
- 论文 [EasyEdit: An Easy-to-use Knowledge Editing Framework for Large Language Models](https://arxiv.org/abs/2308.07269)
- 代码 [EasyEdit](https://github.com/zjunlp/EasyEdit)

然而，目前关于 `LLMs 知识编辑`的研究在实现和任务设置上的差异妨碍了知识编辑统一和综合框架的发展。值得注意的是，这种复杂性阻碍了不同方法之间有效性和可行性的直接比较，也使得创建新的知识编辑方法变得复杂。

EasyEdit 框架整合了各种编辑技术，支持在不同 LLMs 之间自由组合模块。通过统一的框架和接口，EasyEdit 能使用户迅速理解并应用包含在该框架中的主流知识编辑方法。EasyEdit 具有统一的 Editor、Method 和 Evaluate 框架，分别代表**编辑场景**、**编辑技术**和**评估方法**。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCdrGGtbIFt~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=qjF%2FeWeSs6aesEsE1h%2BZuHMGRz8%3D)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCf8CHe0fQA~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=4GKQB2crsR9z9gIr9p31Cav6dq8%3D)


EasyEdit 还提供了五个评估编辑方法性能的关键指标，包括`可靠性`（Reliability）、`泛化性`（Generalization）、`局部性`（Locality）、`可移植性`（Portability）和`效率`（Efficiency）。

为验证知识编辑在 LLMs 中的应用潜力，研究团队选用了参数庞大的 LlaMA 2 模型，并利用 ZsRE 数据集（QA 数据集）来测试知识编辑将大量一般事实关联整合进模型的能力。测试结果证明，EasyEdit 在可靠性和泛化性方面超越了传统的微调方法。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCiL5n53x88~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=wQPBTjiUF%2FX%2BszdxJIiTV%2FbPDe8%3D)


### 流式输出


 安全审核
 
LLM 响应延迟是影响用户体验的关键因素。

- 当LLM生成响应时间超过1秒时，用户操作流程就会被打断；
- 若超过10秒，用户往往会切换任务。

传统的"**生成后过滤**"安全防护模式面临严峻挑战。


【2025-6-30】[对语言模型流式输出文字进行文本审核](https://help.aliyun.com/document_detail/2642626.html)

当采用模型流式输出方式时，要拼接文字片段后作为文本审核服务的输入内容，但存在明显缺点：
- LLM 容易生成较长内容的文字，拼接全部输出文字后，内容长度有可能超过文本审核的输入限制；
- 用户端会更快看到模型生成内容片段，待全部内容输出时潜在风险可能长时间暴露给用户。

因此, 阿里云文本审核增强版提供了对模型流式输出文字进行**自动拼接并审核**的功能。

该功能既避免了由于内容过长导致文本审核输入限制，也显著降低潜在风险暴露给用户的时间。


【2025-7-10】[LLM Guard项目中的流式输出安全防护技术解析](https://blog.gitcode.com/c48f7874fc6b7783d2d0afe5e7131a49.html)

llm-guard  源代码
- [The Security Toolkit for LLM Interactions](https://gitcode.com/gh_mirrors/llm/llm-guard)

LLM Guard 最初针对**完整生成内容**进行安全检查，这在实时交互场景中存在明显缺陷。典型的流式应用需要以token为单位逐步输出内容，传统防护方案会导致两种不良结果：
- 要么用户需要等待完整响应才能看到内容
- 要么系统需要在无防护状态下直接输出内容。

技术实现方案

项目团队经过探索，提出基于**异步**处理的流式防护方案。核心创新点包括：
- 逐token分析机制：系统能够实时分析每个生成的token，在极短时间内完成安全评估
- 并行处理架构：利用asyncio库实现防护逻辑与生成过程的并行执行
- 动态阻断能力：当检测到风险内容时，可以立即终止后续内容生成

未来可能的发展方向包括：
- 专用微型LLM作为协处理器，专门负责实时安全分析
- 基于生成对抗网络(GAN)的动态检测机制
- 硬件加速的实时内容过滤方案

这种流式安全防护技术的成熟，将为实时对话系统、代码自动补全等低延迟应用场景提供可靠的安全保障。


## 窗口扩大



详见站内专题: [长文本](long_text#窗口扩大)

## 模型结构

详见 [LLM 架构代码详解](llm_code)


### 自学习

AI 自我演进/进化

#### 总结

研究进展
- Sakana AI 与不列颠哥伦比亚大学等机构合作的「达尔文-哥德尔机（DGM）」
- CMU 的「自我奖励训练（SRT）」
- 上海交通大学等机构提出的多模态大模型的持续自我改进框架「MM-UPT」
- 香港中文大学联合 vivo 等机构的自改进框架「UI-Genie」
- MIT 发布的《Self-Adapting Language Models》提出让 LLM 更新自己的权重的方法：SEAL🦭，即 Self-Adapting LLMs。

参阅文章《[LSTM 之父 22 年前构想将成真？一周内 AI「自我进化」论文集中发布，新趋势涌现？](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650971628&idx=1&sn=1f3baa09a3d3953449c96f91b1e4b205&scene=21#wechat_redirect)》


OpenAI CEO、著名 𝕏 大 v 山姆・奥特曼在其博客《[温和的奇点（The Gentle Singularity）]()》中更是畅想了一个 AI/智能机器人实现自我改进后的未来。
- 「我们必须以传统方式制造出第一批百万数量级的人形机器人，但之后它们能够操作整个供应链来制造更多机器人，而这些机器人又可以建造更多的芯片制造设施、数据中心等等。」

不久之后，就有 𝕏 用户 [@VraserX 爆料](https://x.com/VraserX/status/1932842095359737921)称有 OpenAI 内部人士表示，该公司已经在内部运行能够递归式自我改进的 AI。



#### 【2025-3-4】MIT PRefLexOR


解决什么问题
- 面对**跨领域**难题，AI输出像**碎片拼图**毫无逻辑
- 模型遇到新场景就“**痴呆**”，需要反复调教
- 重要决策时，AI推理过程**不可信**…

【2025-3-4】MIT Markus 教授团队 全新自学习AI框架 [PRefLexOR](https://github.com/lamm-mit/PRefLexOR) （Preference-based Recursive Language Modeling for Exploratory Optimization of Reasoning）, 让AI像人类一样，进行深度思考和自主进化。
- MIT 新AI**自主进化**出`思维链`：动态`知识图谱`+**跨域推理**黑科技
- 融合`强化学习`与偏好优化的「自进化大脑」，通过递归推理和多步反思，动态生成知识图谱。
- 不仅能动态构建知识图谱，还会像人类一样通过「**反思令牌**」迭代优化推理路径。
- GitHub: [PRefLexOR](https://github.com/lamm-mit/PRefLexOR)

![](https://pica.zhimg.com/v2-d309250b24c40d4bcda0a4d0c1dcb5fc_1440w.jpg)

核心功能：动态知识图谱构建、跨领域推理能力、自主学习与进化。

PRefLexOR 主要功能
- **动态**知识图谱构建：框架不依赖预生成的数据集，通过动态生成任务和推理步骤，实时构建知识图谱，使模型能不断适应新任务，在推理过程中动态扩展知识。
- 跨领域推理能力：PRefLexOR 能够将不同领域的知识进行整合和推理，例如在材料科学中，模型可以通过递归推理和知识图谱生成新的设计原则。
- 自主学习与进化：通过递归优化和实时反馈，PRefLexOR 能够在训练过程中自我教学，不断改进推理策略，展现出类似人类的深度思考和自主进化能力。

技术原理：递归推理与反思、偏好优化、多阶段训练。
- **优势比**偏好优化（ORPO），模型通过优化**偏好响应**和**非偏好响应**之间的**对数几率**来对齐推理路径。
- 同时，集成了直接偏好优化（DPO），通过**拒绝采样**进一步提升推理质量。
- 这种混合方法类似于 RL 中的策略细化，模型通过实时反馈和递归处理不断改进。

技术原理
- **递归推理与反思**：PRefLexOR 引入“思考令牌”和“反思令牌”，明确标记推理过程中的中间步骤和反思阶段。模型在推理过程中会生成初始响应，然后通过反思逐步改进，最终生成更准确的答案。
- **偏好优化**：PRefLexOR 基于优势比偏好优化（ORPO）和直接偏好优化（DPO）。模型通过优化偏好响应和非偏好响应之间的对数优势比，使推理路径与人类偏好决策路径一致。DPO 进一步通过拒绝采样调整推理质量，确保偏好对齐的细微差别。
- **多阶段训练**：PRefLexOR 的训练分为多个阶段：首先通过 ORPO 对齐推理路径，然后通过 DPO 进一步优化推理质量。这种混合方法类似于 RL 中的策略细化，模型通过实时反馈和递归处理不断改进。


训练基于**图结构**的原生AI，自主推理数天，构建动态关系世界模型，而这一过程也不需要预先编程。

这个模型涌现出的**枢纽节点**、**小世界**特性、模块化和**无标度结构**都是自然形成。

随后，该模型通过组合式推理，从深度合成中发现了未被编码的特性，即具有记忆的材料、微生物修复能力和**自进化**系统。

如果你给AI一堆乐高积木，也不告诉它怎么搭，它自己研究几天后，不仅搭出了城堡，还发明了会变形的积木、能自动修复裂痕的胶水，甚至让城堡长出“腿”自己移动，整个过程完全超出你的预期


安装

```sh
pip install git+https://github.com/lamm-mit/PRefLexOR.git
```

或：

```sh
git clone https://github.com/lamm-mit/PRefLexOR.git
cd PRefLexOR
pip install -r requirements.txt
pip install -e .
```

使用 Flash Attention，可以安装：

```sh
MAX_JOBS=4 pip install flash-attn --no-build-isolation
```


#### 【2025-2-18】港大 AutoAgent

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

#### 【2025-6-14】MIT SEAL

【2025-6-14】[LLM已能自我更新权重，自适应、知识整合能力大幅提升，AI醒了？](https://mp.weixin.qq.com/s/WvC7kX1_XfNO218YBsAa8g)

MIT 昨日发布的《Self-Adapting Language Models》提出让 LLM 更新自己的权重的方法：SEAL🦭，即 Self-Adapting LLMs。

该框架中，LLM 可以生成自己的训练数据（自编辑 /self-editing），并根据新输入对权重进行更新。而这个自编辑可通过强化学习学习实现，使用的奖励是更新后的模型的下游性能。
- 论文标题：[Self-Adapting Language Models](https://arxiv.org/pdf/2506.10943)
- 项目页面：[seal](https://jyopari.github.io/posts/seal)
- 代码地址：[seal](https://github.com/Continual-Intelligence/SEAL)

自适应语言模型（SEAL）

SEAL 框架可以让语言模型在遇到新数据时，通过生成自己的合成数据并优化参数（自编辑），进而实现自我提升。

该模型训练目标：
- 使用模型上下文中提供的数据，通过生成 token 来直接生成这些自编辑（SE）。

自编辑生成需要通过强化学习来学习实现，其中当模型生成的自编辑在应用后可以提升模型在目标任务上的性能时，就会给予模型奖励。

因此，可以将 SEAL 理解为一个包含两个嵌套循环的算法：一个外部 RL 循环，用于优化自编辑生成；以及一个内部更新循环，它使用生成的自编辑通过梯度下降更新模型。


#### 【2025-10-15】META 早期经验自主学习

META 和 俄亥俄州立大学，
- 【2025-10-15】[Meta团队揭秘：AI智能体如何通过“早期经验”实现自主学习突破](https://news.qq.com/rain/a/20251015A04FHY00)
- 【精】【2025-10-11】[深度解读 Meta 论文：无需奖励，AI Agent 如何通过“早期经验”实现自我进化？](https://zhuanlan.zhihu.com/p/1960366382354002762)

2025年10月15日，Meta超级智能实验室、FAIR团队及俄亥俄州立大学发布突破性研究，找到**让AI像真正的孩子一样学习**的方法。团队共同探索了一个全新的AI训练范式，不需要外部奖励信号，就能让AI从自己的探索经历中不断成长
- 论文 [Agent Learning via Early Experience](https://arxiv.org/pdf/2510.08558)

打破了传统AI训练困境
- 要么机械模仿专家示范，像只会照着菜谱做饭的厨师，缺少食材就束手无策
- 要么通过大量试错、即时反馈来学习，很多场景下行不通，让学生做100道题但永远不告诉对错

填补了`模仿学习`和`强化学习`之间的空白，提出了可规模化、无需奖励、且效果显著的**自学习**方法。

AI学习的三个时代
- （1）传统课堂模式：专家数据时代，老师讲，学生模仿。模型观察专家示例来学习正确行为模式，即 监督微调、模仿学习；
  - 问题：泛化能力不足，遇到新情况时犯傻
- （2）考试驱动模式：经验时代，或RL阶段，学生不听课，直接做题，根据分数调整策略。模型可以尝试各种行动，获取环境反馈。理论强大，代表 AlphaGo
  - 问题：实际应用中，很多任务无法提供清晰、即时反馈。学习效率低，模型陷入困境
- （3）中间步骤：早期经验范式，介于传统课堂与考试之间；学生已经听过老师的基本讲解，知道一些正确答案，但还没到考试时候，学生自己拿课本/笔记尝试做题。
  - 因素：（1）过于依赖昂贵的专家数据，不够灵活（2）需要明确的反馈信号，很多时候不存在、太稀疏

<img width="954" height="312" alt="image" src="https://github.com/user-attachments/assets/15da3eea-f075-456d-a19d-b82d3e988c3f" />


巧妙之处：不需要外部奖励信号，仍能提供有价值学习信号

两种互补的学习策略
- (1) 隐式世界建模 (Implicit World Modeling, IWM)：理解环境如何运作; “<span style='color:red'>如果我这么做会怎样？</span>”，然后学习**预测结果**
  - 让 Agent 学习并内化环境的动态规律，即理解 “我做了某个动作后，环境会发生什么变化？”
- (2) 自我反思 (Self-Reflection, SR)：如何做出更好的决策; “<span style='color:red'>为什么不那么做？</span>”，然后学习**推理过程**
  - 让 Agent 学习从对比中进行推理，理解“为什么专家的动作比我的想法更好？”

学生学习的两个不同方面：一个是理解知识本身的运作规律，另一个是学会自我评价和反思。

"早期经验"方法让AI在没有明确对错评判时，通过观察"如果我这样做会发生什么"来建立对环境的理解。

<img width="906" height="422" alt="image" src="https://github.com/user-attachments/assets/f0c3df22-86b7-478f-a2c1-5e4654fa1c59" />


两种策略的结合创造了**协同效应**。
- 世界建模帮助AI理解环境的客观规律，而自我反思帮助AI学会在这些规律的基础上做出明智的选择。
- 就像一个好学生，既要掌握知识本身，也要培养批判性思维和问题解决能力。

研究团队在不同环境中发现，有时世界建模效果更好，有时自我反思效果更好，这取决于任务的性质。但在几乎所有情况下，两种方法都显著优于传统的纯模仿学习。

八个截然不同的任务场景中都表现出色，从网页购物到科学实验，从旅行规划到多步骤工具使用，证明了其广泛的适用性。

<img width="942" height="315" alt="image" src="https://github.com/user-attachments/assets/5aa47bc5-c3e8-4467-af1f-67770f532850" />


更令人兴奋的是，这种早期经验训练不仅立即提升了AI表现，还为后续强化学习训练打下了更坚实的基础，就像一个经过充分探索和试错的学生，在面对正式考试时会表现得更加出色。


### Transformer 改进

详见站内: [transformer 改进专题](transformer_evolution)

### 放弃 Transformer

Transformer 构建灵活、易并行、易扩展等优势, 但问题是
- 并行输入的机制会导致模型规模随输入序列长度平方增长，导致其在处理长序列时面临计算瓶颈

传统 RNN 模型计算量小，理论上可以处理无限长序列，但存在序列依赖，难以捕捉长期依赖关系，且面临梯度消失、爆炸问题
- RNN 可以将历史状态以隐变量的形式循环叠加到当前状态上，对历史信息进行考虑，呈现出**螺旋式前进**的模式。

transformer 架构不是唯一

【2024-11-24】详见：浙大《[大模型基础](https://github.com/ZJU-LLMs/Foundations-of-LLMs/blob/main/readme.md)》

两类现代RNN 变体，分别为
- 状态空间模型（State Space Model，SSM）
- 测试时训练（Test-Time Training，TTT）

这两类范式都能实现关于序列长度的**线性时间复杂度**，且避免了传统RNN 中存在的问题


#### SSM

状态空间模型（State Space Model，SSM）范式可有效处理长文本中存在的**长程依赖性**（Long-Range Dependencies, LRDs）问题，并且可以有效降低语言模型的计算和内存开销。

SSM 范式
- SSM 思想源于控制理论中的动力系统。其通过利用**一组状态变量**来捕捉系统状态随时间的**连续变化**，这种连续时间的表示方法天然地适用于描述**长时间范围内**的依赖关系。
- 此外，SSM 还具有递归和卷积的离散化表示形式，既能在推理时通过递归更新高效处理序列数据，又能在训练时通过卷积操作捕捉全局依赖关系。

SSM 训练和推理非常慢。为了提高处理效率，需要对该方程进行离散化（Discretization）, SSM 中最为关键的步骤，将系统方程从**连续形式**转换为**递归**形式和**卷积**形式，从而提升整个SSM 架构的效率。
- 训练时使用**卷积**形式
- 推理时使用**递归**形式

SSM 架构的系统方程具有三种形式，分别为
- 连续形式
- 离散化的递归形式
- 离散化的卷积形式

可应用于文本、视觉、音频和时间序列等任务

SSM 的优势在于能够处理非常长的序列，虽然比其它模型参数更少，但在处理长序列时仍然可以保持较快的速度。

两种基于SSM范式的代表性模型：`RWKV` 和`Mamba`。


##### RWKV

RWKV（Receptance Weighted Key Value）是基于SSM 范式的创新架构，其核心机制 WKV 的计算可以看作是两个SSM 的比。

RWKV 设计结合了 RNNs 和 Transformers 的优点，既保留了推理阶段的高效性，又实现了训练阶段的并行化。（注：这里讨论的是RWKV-v4）

RWKV 模型的核心模块有两个：**时间混合**模块和**通道混合**模块。
- 时间混合模块主要处理序列中不同时间步之间的关系
- 通道混合模块则关注同一时间步内不同特征通道30之间的交互。

时间混合模块和通道混合模块的设计基于四个基本元素：接收向量R、键向量K、值向量V 和权重W，

##### Mamba

**时不变性**使得SSM 能够一致地处理不同时间步长的数据，进行高效的并行化训练，但是同时也导致其处理信息密集的数据（如文本）的能力较弱。

为了弥补这一不足，Mamba 基于SSM 架构，提出了**选择机制**（Selection Mechanism）和**硬件感知算法**（Hardware-aware Algorithm），前者使模型执行基于内容的推理，后者实现了在GPU 上的高效计算，从而同时保证了快速训练和推理、高质量数据生成以及长序列处理能力。

Mamba 的选择机制通过动态调整模型参数来选择需要关注的信息，使模型参数能够根据输入数据动态变化。

Mamba 在实际应用中展示了卓越的性能和效率，包括：
- （1）快速训练和推理：训练时，计算和内存需求随着序列长度线性增长，而推理时，每一步只需常数时间，不需要保存之前的所有信息。通过硬件感知算法，Mamba 不仅在理论上实现了序列长度的线性扩展，而且在A100 GPU上，其推理吞吐量比类似规模的Transformer 提高了5 倍。
- （2）高质量数据生成：在语言建模、基因组学、音频、合成任务等多个模态和设置上，Mamba 均表现出色。在语言建模方面，Mamba-3B 模型在预训练和后续评估中性能超过了两倍参数量的Transformer 模型性能。
- （3）长序列处理能力：Mamba 能够处理长达百万级别的序列长度，展示了处理长上下文时的优越性。

Mamba 在硬件依赖性和模型复杂度上存在一定的局限性，但是它通过引入选择机制和硬件感知算法显著提高了处理长序列和信息密集数据的效率，展示了在多个领域应用的巨大潜力


#### ttt

在处理长上下文序列时，基于SSM 范式的架构（例如RWKV 和Mamba）通过将上下文信息压缩到**固定长度**的隐藏状态中，成功将计算复杂度降低至**线性**级别，有效扩展了模型处理长上下文的能力。

然而，随着上下文长度的持续增长，基于SSM 范式的模型可能会过早出现**性能饱和**。
- 例如，Mamba 在上下文长度超过**16k** 时，困惑度基本不再下降。

出现这一现象的原因
- 可能是固定长度的隐藏状态限制了模型的表达能力，同时在压缩过程中可能会导致关键信息的遗忘。

`测试时训练`（Test-Time Training，TTT）范式提供了一种有效的解决方案。
- TTT 利用**模型本身参数**来存储隐藏状态、记忆上文；
- 并在每一步推理中，对模型参数进行**梯度更新**，已实现上文的不断循环流入

详见站内专题：[测试时计算](test_time)



#### Titans

【2025-1-15】[近8年后，谷歌Transformer继任者「Titans」来了，上下文记忆瓶颈被打破](https://www.jiqizhixin.com/articles/2025-01-15-15)

2017 年推出影响 AI 行业长达 8 年的 Transformer 架构之后，谷歌带来了全新的架构 Titans。
- 论文标题：[Titans: Learning to Memorize at Test Time](https://arxiv.org/pdf/2501.00663v1)
- 代码
  - 非官方实现 [titans-pytorch](https://github.com/lucidrains/titans-pytorch)

谷歌重点将推理领域非常重要的测试时（test-time）计算用在了**记忆**（memory）层面。

[Ali Behrouz](https://x.com/behrouz_ali/status/1878859086227255347) 表示
- 注意力机制一直是大多数 LLM 进展的重要组成部分，不过它无法扩展到长上下文。
- Titans 是一种同时具备**注意力机制**和**元上下文记忆**的结构，可以在**测试时**学习记忆。

该架构可以将上下文窗口扩展到 200 万 tokens。

谷歌提出新的**长期神经记忆**模块（neural memory module），学习记忆历史上下文，并帮助注意力机制在利用过去已久信息的同时处理当前上下文。
- 结果表明，这种神经记忆具有快速并行化训练的优势，同时还能保持快速推理。

从记忆的角度来看，谷歌认为
- **注意力机制虽然受限于上下文**但可以更准确地**建模依赖关系**，因此可以起到**短期记忆**的作用；
- 而神经记忆能够对数据进行记忆，起到了**长期、更持久**的记忆作用。

基于这两个模块，谷歌引入了一个全新的系列架构 —— `Titans`，通过三种变体有效地将记忆融合到该系统架构中，分别是: 
- `记忆作为上下文`（Memory as a Context，MAC）
- `记忆作为门`（Memory as a Gate，MAG）
- `记忆作为层`（Memory as a Layer，MAL）

Titans 架构比 Transformer 和近年来的现代线性循环模型更有效。另外，在大海捞针（needle-in-haystack）中，Titans 架构能够有效地扩展到超过 200 万 tokens 的上下文窗口，并且比基准模型实现了更高的准确性。


#### RLM

【2025-10-18】[递归语言模型登场！MIT华人新作爆火，扩展模型上下文便宜又简单](https://www.sohu.com/a/944558308_129720)

所有主流 LLM 都有**固定**的上下文窗口（如 200k, 1M tokens）。
- 一旦输入超过这个限制，模型就无法处理。
- 即使在窗口内，当上下文变得非常长时，模型的性能也会急剧下降，这种现象被称为「`上下文腐烂`」（Context Rot）：模型会「忘记」开头的信息，或者整体推理能力下降。

当用户与 ChatGPT 等主流 LLM 进行长时间、多轮的复杂对话时，会明显感觉到模型开始变「笨」，变得难以聚焦、遗忘关键信息。

MIT 研究者从一个直观的想法出发：
> 也许可以把超长上下文切分，分别交给模型处理，再在后续调用中合并结果，以此避免衰退问题？

提出`递归语言模型`（Recursive Language Models，RLMs），通用的推理策略：
- 语言模型将输入上下文视作**变量**，对其进行**分解**并**递归式**交互。
- 博客文章：[RLM](https://alexzhang13.github.io/blog/2025/rlm/)
- 总结见[推文](https://x.com/a1zhang/status/1978469116542337259)

<img width="1080" height="823" alt="image" src="https://github.com/user-attachments/assets/133c23da-7b0c-4c56-a0af-96ac8463d1cd" />


做法
- 将上下文视为一个可操作的「变量」：主模型（root LM）在一个类似 Jupyter Notebook 的编程环境（REPL）中工作，完整的上下文只是一个它能用代码访问的变量，而不是直接的输入。
- 递归调用自身或小模型：主模型可以编写代码来查看、切分、过滤（比如用 grep）这个巨大的上下文变量，然后把小块的任务外包给一个个小的、临时的 LLM 调用（递归调用）。
- 综合结果：主模型收集这些「外包」任务的结果，最终形成答案。

研究者还设计了具体实现：在一个 Python REPL 环境中调用 GPT-5 或 GPT-5-mini，并将用户的 prompt 存入变量中进行迭代式处理。

向一个 RLM 发起查询时，「根」语言模型（root LM）把整个上下文当作可操作的环境来探索和处理。通过递归调用（R）LM，将对任意结构或任意长度上下文的处理任务分解并逐级委托，从而实现可扩展的推理能力。

这种方式要比任何「分块（chunking）」策略都更加通用且更智能。研究者认为：应该让语言模型自己决定如何探索、拆解并递归地处理长 prompt，而不是由人为制定固定的切分策略。

RLM 框架显著优势：可在一定程度上解释它的行为轨迹，理解它是如何一步步推理并得出最终答案的。研究团队编写了一个简易可视化工具，用来观察 RLM 的推理路径，展示了 RLM 实际在「动手做什么」。

结果很惊人：
- 在能获取到的最难的长上下文评测集之一 OOLONG 上，使用 GPT-5-mini 的 RLM 正确答案数量是直接使用 GPT-5 的**两倍**以上，而且平均每次调用的成本更低。

研究者还基于 BrowseComp-Plus 构建了一个全新的长上下文 Deep Research 任务。
- 该任务中，RLM 显著优于 ReAct + 推理时索引 / 检索等方法。
- 令人意外的是，即使推理时输入超过 1000 万 tokens，RLM 的性能也没有出现衰减。

RLM 很快会成为一个强大范式。

同时，相比于仅依赖 CoT 或 ReAct 风格的代理模型，显式训练以递归式推理为核心机制的 RLM，很可能成为推理时扩展能力领域的下一个里程碑。


## 符号主义

问题：
- LLM 在执行抽象规则归纳（abstract rule induction）时，到底是“黑箱式”地拼统计特征，还是内部出现了可辨识的“符号机制”，如同经典 AI 中的抽象变量和符号推理？


### LLM 三段式

LLM 内部学会符号机制来做抽象reasoning

【2025-6-6】普林斯顿
- 论文 [Emergent Symbolic Mechanisms SupportAbstract Reasoning in Large Language Models]()


选 Llama3-70B，设计抽象模式延伸、逻辑归纳等任务, 通过 causal mediation、attention pattern、RSA 等分析，发现模型内部竟然自发形成了**三段式**符号处理流水线：
1. Symbol Abstraction Heads：把**文字 token** 抽象成**符号变量**；
2. Symbolic Induction Heads：在符号上做**序列归纳**；
3. Retrieval Heads：根据推断的符号去检索下一个 token。
	
消融实验验证，少了任何一段都不行
- 禁用符号抽象头会立刻毁掉所有归纳能力；
- 停用归纳头则模型无法继续延伸模式；
- 禁用检索头则知道模式也没法生成答案。
	
结论：
- Emergent Symbolic Architecture
- LLM 在训练过程中自发形成了**三段式**符号化电路：`抽象`→`归纳`→`检索`，这一结构与经典符号推理模型高度对应。
	
抽象推理依赖性
- 抽象推理能力并非纯粹“大量参数+统计”得来，而是要依靠内部符号机制的阶段化协作。

符号与神经桥梁
- 研究结果在“符号主义 vs. 连接主义”争论中给出了折中答案：神经网络可以在无预设符号模块的情况下，通过学习自动构造类似符号处理的子网络。
	
未来方向
- 可据此设计更高效的符号-神经混合架构，显式增强这三大机制；


### ABL-Refl

【2025-2-8】周志华团队[ABL-Refl]()革新 神经符号推理 Neuro-Symbolic (NeSy) AI
- [Efficient Rectification of Neuro-Symbolic Reasoning Inconsistencies by Abductive Reflection](https://arxiv.org/pdf/2412.08457)
- Abductive Reflection (ABL-Refl) based on the Abductive Learning (ABL) framework

神经符号人工智能类比人类双过程认知，但复杂任务中常出现与领域知识不一致的输出，纠正困难。
	
受人类认知反思启发，研究在溯因学习框架上提出`溯因反思`（ABL-Refl），利用领域知识生成反思向量，标记并纠正神经网络输出错误，生成一致结果。
	
其效率远高于以往溯因学习实现，实验显示性能优于主流神经符号方法，能以更少训练资源获高准确率，且效率提升。



### SymAgent

#### 起因

仅通过提示大型语言模型来规划整个推理流程无法取得令人满意的性能。

当前大型语言模型难以将复杂问题与知识图谱（KG）的语义及连接模式对齐，导致生成的推理链粒度较粗，无法有效用于精确的信息检索与整合。


#### SymAgent 介绍

【2025-2-5】武大、阿里 [SymAgent：神经符号自学习Agent](https://mp.weixin.qq.com/s/CGvGWAQtm49YlgirumrzKg)
- 论文 [SymAgent: A Neural-Symbolic Self-Learning Agent Framework for Complex Reasoning over Knowledge Graphs](https://arxiv.org/pdf/2502.03283)

SymAgent 结合知识图谱（KGs）与大型语言模型（LLMs）以**自主**解决复杂推理任务的框架。

SymAgent利用大型语言模型（LLM）从知识图谱（KG）中识别可能用于回答问题的潜在符号规则，而非生成详细的分步计划：
- 已有研究表明，大型语言模型在归纳推理方面表现出色，但在演绎推理方面能力较弱。
- 符号规则本身反映了知识图谱的推理模式，可作为辅助分解复杂问题的隐含信息。

通过这种方式，Agent-Planner在自然语言问题与知识图谱的结构信息之间搭建了一座桥梁，从而提高了推理过程的准确性和通用性。


#### 框架

SymAgent 包含一个 Agent-Planner（智能体规划器）和一个 Agent-Executor（智能体执行器）
- Agent-Planner 从知识图谱中提取**符号规则**，用于分解问题和规划推理步骤
- Agent-Executor 则通过整合反思所得见解和环境反馈来回答问题。

为解决标注推理数据缺失的问题，引入了一个**自学习**框架，通过自主交互实现协同改进。

整体架构如图所示。 SymAgent框架概述。
- （a）SymAgent中的规划器，其从知识图谱中提取符号规则以指导推理；
- （b）SymAgent中的执行器，其执行自动行动调用以获取答案；
- （c）用于迭代增强智能体的自学习框架；
- （d）合成的行动调用轨迹示例。


## 类脑

详见站内专题：[类脑计算](brain_compute)


## 图解

总结LLM各阶段优化方向

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-06-22T15:10:12.254Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;V_7K2ib4bP-NWsyXjMxV\&quot; version=\&quot;21.5.0\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;795\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-35\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f9f7ed;strokeColor=#36393d;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;90\&quot; y=\&quot;300\&quot; width=\&quot;180\&quot; height=\&quot;360\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wGYBfAiltT4hGnPjrrAm-8\&quot; value=\&quot;LLM改进方向\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=19;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;242\&quot; y=\&quot;70\&quot; width=\&quot;216\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; value=\&quot;数据\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;118\&quot; y=\&quot;180\&quot; width=\&quot;110\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; value=\&quot;训练\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;570\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-6\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; target=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;240\&quot; y=\&quot;275\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;410\&quot; y=\&quot;410\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-15\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; target=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;250\&quot; y=\&quot;600\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; value=\&quot;复现\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;590\&quot; y=\&quot;535\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-12\&quot; value=\&quot;数据集：收集处理\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-13\&quot; value=\&quot;三步走流程\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-14\&quot; value=\&quot;硬件资源开销\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-22\&quot; value=\&quot;改进&amp;lt;br&amp;gt;① 单词→字符&amp;lt;br&amp;gt;②解决了OOV问题\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;190\&quot; y=\&quot;450\&quot; width=\&quot;120\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-42\&quot; value=\&quot;2023-6-22&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;120\&quot; y=\&quot;1210\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; value=\&quot;效果\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;910\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-3\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-2\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;283\&quot; y=\&quot;500\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;280\&quot; y=\&quot;790\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-5\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-4\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;240\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;490\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; value=\&quot;模型\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;340\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-7\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-6\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;620\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;780\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; value=\&quot;部署\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;740\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-8\&quot; value=\&quot;问题\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540\&quot; y=\&quot;860\&quot; width=\&quot;230\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-37\&quot; value=\&quot;LLM评测\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-9\&quot; value=\&quot;知识准确性：幻觉，胡说八道\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-10\&quot; value=\&quot;复杂推理能力\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-11\&quot; value=\&quot;人类偏好对齐：RLHF不足\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-12\&quot; value=\&quot;应用\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;1110\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-13\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-12\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;167\&quot; y=\&quot;630\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;90\&quot; y=\&quot;750\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-14\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;460\&quot; y=\&quot;960\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;510\&quot; y=\&quot;935\&quot; /&gt;\n              &lt;mxPoint x=\&quot;510\&quot; y=\&quot;935\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-15\&quot; value=\&quot;工程落地\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;708\&quot; width=\&quot;140\&quot; height=\&quot;180\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-16\&quot; value=\&quot;小型化\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-17\&quot; value=\&quot;本地部署\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-18\&quot; value=\&quot;性能：时延、并发\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-20\&quot; value=\&quot;数据安全\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-38\&quot; value=\&quot;输入、输出限制\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;150\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-19\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=-0.021;entryY=0.9;entryDx=0;entryDy=0;entryPerimeter=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-16\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;605\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-21\&quot; value=\&quot;生态系统\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380\&quot; y=\&quot;1060\&quot; width=\&quot;140\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle x=\&quot;550\&quot; y=\&quot;1040\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-22\&quot; value=\&quot;联网\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-23\&quot; value=\&quot;插件市场\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-24\&quot; value=\&quot;垂类应用\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-25\&quot; value=\&quot;LLM框架：LangChain\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-26\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-12\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-23\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;775\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;367\&quot; y=\&quot;775\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-27\&quot; value=\&quot;数据集\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;560\&quot; y=\&quot;145\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-28\&quot; value=\&quot;预训练数据集：中英文\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-29\&quot; value=\&quot;指令集\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-30\&quot; value=\&quot;prompt数据集\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-31\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;entryX=-0.014;entryY=0.933;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-28\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;605\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-32\&quot; value=\&quot;模型优化\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;400\&quot; y=\&quot;305\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-33\&quot; value=\&quot;基座大模型：中文\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-34\&quot; value=\&quot;奖励模型\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-35\&quot; value=\&quot;RL环节优化\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-36\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;entryX=-0.007;entryY=0.067;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-34\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;238\&quot; y=\&quot;215\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;408\&quot; y=\&quot;214\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



# 结束
