---
layout: post
title:  规模法则 Scaling Law
date:   2024-09-05 12:00:00
categories: 大模型
tags: LLM ilya 缩放定律 ttt 乔姆斯基 扩展法则 openai google deepmind
excerpt:  谈谈影响LLM发展的重要定律, 规模法则(Scaling Law)
mathjax: true
permalink: /llm_law
---

* content
{:toc}


# Scaling Law 缩放定律



## 思考


### Scaling Law 尽头


2024年2月末, `唐杰`教授表示: Scaling Law的尽头不一定是AGI，从人脑的认知角度改进未来的AGI系统，使它变得更加智能，这是我们未来要思考的问题。


### LLM 为什么都是 6b/13b/52b...

[解析大模型中的Scaling Law](https://zhuanlan.zhihu.com/p/667489780)

需求：
- 训练10B模型，至少要**多大数据**？
- 1T数据能训练**多大模型**？
- 100张A100，应该用**多少数据**训一个**多大模型**，最终效果最好？
- 10B模型不满意，扩大到100B模型，效果能提升到多少？

以上这些问题都可以基于 Scaling Law 理论进行回答。

总结
> scaling law 指导下，匹配当前的显卡资源和数据资源

- [现在LLM 大小为什都设计成6/7B、13B和130B几个档次？](https://www.zhihu.com/question/627258986/answer/3260798103?utm_psn=1733426493282344961)

[方佳瑞](https://www.zhihu.com/question/627258986/answer/3261239043)

最大尺寸版本确定的核心逻辑是: DeepMind 的 `Chinchilla Scaling Law`。

开发大模型时，清洗出来的开源数据数量是**离散值**。
- LLaMA-1 预训练时，从各种开源数据集凑够了 1.4T tokens，所以最大版本是**70B**，很接近`Chinchilla Scaling Law`的计算结果。
- 用1024张A100，MFU=0.55情况下，训练时长大概是38天，这是一个比较可行的预训练方案。
- 至于更小版本选型比较随意，主要考虑调试时，计算量要控制在一个可控范围，比如一般会选择一个10^22 FLOPs计算量（差不多256卡两三天出结果）下的最优模型尺寸，因此最优尺寸肯定是在10B以内。由于一些矩阵维度的限制，一般都是**6B**，**7B**。
- ![](https://pic1.zhimg.com/50/v2-df87270c8e67f83b38b584f720b8cd95_720w.jpg)

`Chinchilla Scaling Law`有些争议，正溯还是得看OpenAI文章[Scaling laws for neural language models](https://arxiv.org/pdf/2001.08361)，过去一年内大家还是会follow这套理论。

[刘聪NLP](https://www.zhihu.com/question/627258986/answer/3260798103)

LLM 一般都是基于Transormer结构，**参数总和** = **Embedding部分**参数 + **Transormer-Decoder部分**参数
- Embedding 部分参数由词表大小和模型维度决定；
- Decoder 部分参数由模型层数和模型维度决定。

决定参数的几个因素有：**词表大小**、**模型层数**（深度）、**模型维度**（宽度）。
- 关于词表大小设置，越大的词表的压缩会更好，但可能导致模型训练不充分；越小的词表压缩会比较差，导致模型对长度需求较高。
- 关于层数设置问题，其实模型层数和维度具体设置成多少是最优的（但一般层数变大，维度也会变大），目前没有论文明确表明，但绝大多数感觉跟着GPT3的层数和维度来的。
- ![](https://picx.zhimg.com/50/v2-757af3b0e13e0d76d8bb1c75018a8b44_720w.jpg)

常见模型 6/7B 是**32层**、13B 是**40层**。

PS：由于GPT3模型先出，让OPT、Bloom等都是为了做开源的GPT3所提出的，因此参数规模是一致的。
- llama 为了对标GPT3，不过为了证明效果更好，也在中间多了`33B`和`65B`规模。
- `130B` 只有GLM大模型是这个参数。

现在流传甚广的其实是6/7B(小)、13B(中)，主要是由于更大的模型训练成本会更高，并且对于很多人来说13B的模型已经算顶配了（消费显卡跑得了）。



## 语言模型进化

【2024-8-10】[大语言模型 Scaling Law：如何随着模型大小、训练数据和计算资源的增加而扩展](https://mp.weixin.qq.com/s/7XnuXjN8Y44FCkWJ6YwTTQ)

缩放定律
- 一个由三个关键部分组成的法则：`模型大小`、`训练数据`和`计算能力`

过去几年，语言模型迅速发展壮大。
- 语言模型从 2018年的 BERT-base 的1.09亿参数规模，增长到 2022年的 PaLM 的5400亿参数。
- 每个模型不仅在**模型规模**上增加（即参数数量），还在训练**令牌数量**和**训练计算量**（以浮点运算或FLOPs计）上都有所增加。

|Time|Company|Model|Model Size<br>#parameters|Training data<br>#tokens|Training compute<br>FLOPs|Resources|
|---|---|---|---|---|---|---|
|2018|Google|`BERT`-base|109M|250B|1.6e20|64 TPU v2 for 4 days<br>16 v100 GPU for 33 hours|
|2020|OpenAI|`GPT-3`|175B|300B|3.1e23|~1000 x BERT-base|
|2022|Google|`PaLM`|540B|780B|2.5e24|64 TPU v4 for 2 months|

问题
- “这三个因素之间有什么关系？”
- 模型大小和训练数据对模型性能（即测试损失）的贡献是否相等？哪一个更重要？
- 如果将测试损失降低10%，我应该增加模型大小还是训练数据？需要增加多少？


### 幂律函数

幂律是两个量x和y之间的非线性关系，建模为: 
- $ y = ax^k $
- $ logy = loga + klogx$
- 其中k和a是常数。

幂律曲线

```py
import numpy as np
import matplotlib.pyplot as plt

def plot_power_law(k, x_range=(1, 100), num_points=100):
    """
    Plot the power law function y = x^k for any non-zero k.

    Parameters:
    k (float): The exponent for the power law (can be positive or negative, but not zero).
    x_range (tuple): The range of x values to plot (default is 0.1 to 10).
    num_points (int): Number of points to calculate for a smooth curve.
    """
    if k == 0:
        raise ValueError("k cannot be zero")

    # Generate x values
    x = np.linspace(x_range[0], x_range[1], num_points)

    # Calculate y values
    y = x**k

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', label=f'y = x^{k}')
    #plt.barh(x, y)
    plt.title(f'Power Law: y = x^{k}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    
    plt.show()

plot_power_law(2) # y = x^2
plot_power_law(-0.5) # y = x^(-0.5)
```


### 三要素

大语言模型的预训练，通常伴随着`模型容量`、`数据量`、`训练成本`的三方权衡博弈。
- [img](https://simg.baai.ac.cn/uploads/2024/01/a00c375723a62b09ec304953b37ae928.png)

这种三角形式的拔河关系存在一些**三元悖论**，比如
- 分布式计算领域中的公认定理：`CAP理论`: 分布式系统不可能同时满足`一致性`、`可用性`和分区`容错性`，最多只能同时满足其中2个条件。
- 大语言模型训练同样存在类似这种三元关系的探索，这就是`缩放定律`（Scaling Laws）。

大语言模型预训练过程中，`交叉熵损失`（cross-entropy loss）是一种常用的性能衡量标准，用于评估模型预测输出与真实情况之间的差异。较低的交叉熵损失意味着模型的预测更准确。训练的过程也是追求损失值的最小化的过程。


## 什么是 Scaling Laws


### 背景

源自浙大书籍《大语言模型》[章节](https://github.com/ZJU-LLMs/Foundations-of-LLMs/blob/main/%E3%80%8A%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%9F%BA%E7%A1%80%E3%80%8B%E6%95%99%E6%9D%90/%E3%80%8A%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%9F%BA%E7%A1%80%E3%80%8B%E5%88%86%E7%AB%A0%E8%8A%82%E5%86%85%E5%AE%B9/%E7%AC%AC2%E7%AB%A0%20%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E6%9E%B6%E6%9E%84.pdf)
- 模型规模和训练数据的增长带来巨大的计算、存储成本，大力出奇迹难以为继。
- 模型设计时，<span style='color:red'>如何在资源消耗、性能提升之间找到平衡点？</span>

大语言模型的`扩展法则`（Scaling Laws）诞生, 揭示模型能力岁模型规模和数据规模的变化关系，为 LLM 设计和优化提供指导建议。

Scaling Laws 意义: 
- AI专业人士可通过 Scaling Laws 预测大模型在`参数量`、`数据量`以及`训练计算量`这三个因素变动时，损失值的变化。
- 为LLM设计提供决策支持，比如在固定资源预算下，匹配模型的最佳大小和数据大小，而无需进行及其昂贵的试错。

规模化法则(`缩放法则`)（Scaling Law）指 **模型性能**与**模型大小**、**数据集大小**和**计算资源**等多种因素之间观察到的关系。

随着模型的扩展，这些关系遵循**可预测**模式。

`扩展法则`行为的关键因素如下：
- **模型大小**：随着模型中参数数量的增加，性能通常会按照幂律改善。
- **数据集大小**：更大的训练数据集通常带来更好的性能，也遵循幂律关系。
- **计算**：用于训练的计算资源（浮点运算次数）与性能改善相关。

测试集损失与计算、数据集大小和模型参数之间遵循幂律关系（对数线性）
- `Training Compute` = alpha * `Model Size` * `Training Data`
- alpha ~ 6

每个参数和每个训练实例需要大约6次浮点运算（FLOPs）
- 前向传播中，需要恰好2次FLOPs将w与输入节点相乘，并将其添加到语言模型的计算图的输出节点中。（1次乘法和1次加法）
- 计算损失对w的梯度时，需要恰好2次FLOPs。
- 用损失的梯度更新参数w时，需要恰好2次FLOPs。

【2024-9-20】[AI can't cross this line and we don't know why](https://www.youtube.com/watch?v=5eqRuVp65eY)


<iframe width="560" height="315" src="https://www.youtube.com/embed/5eqRuVp65eY?si=dfoIUDqztuQOr8hx" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### Scaling Law 定义


主要有两个版本: OpenAI V.S DeepMind
- OpenAI 提出的 `Kaplan-McCandlish` 扩展法则
- Google DeepMind 提出的 `Chinchilla` 扩展法则

更多见【2024-1-5】[OpenAI与DeepMind的Scaling Laws之争](https://hub.baai.ac.cn/view/34084)


### 2020 Kaplan-McCandlish Scaling Law

2020年, OpenAI 团队的 Jared Kaplan 和 Sam McCandlish 等人首次研究了神经网络性能与数据规模D、模型规模N之间的函数关系。 `Kaplan-McCandlish`

OpenAI
> “Our mission is to ensure that artificial general intelligence—AI systems that are generally smarter than humans—benefits all of humanity.”

—— 2023年2月14日《Planning for AGI and beyond》

谷歌收购 DeepMind 后，为避免谷歌在AI领域形成垄断，`埃隆·马斯克`和其他科技行业人物于2015年决定创建`OpenAI`。

OpenAI 作为一个有声望的非营利组织，致力于开发能够推动社会进步的AI技术​​。不同于 DeepMind 像一个精于解决棋盘上复杂战术的大师，专注于解决那些有明确规则和目标的难题，OpenAI更像是一个擅长语言艺术的诗人，致力于让机器理解和生成自然的人类语言。

从坚持初期被外界难以理解的GPT路线信仰，直到拥有1750亿参数的GPT-3问世，OpenAI展示了其在生成式模型上无与伦比的能力，引领了另一个AI时代。类比Deepmind和谷歌的关联，OpenAI与科技巨头微软牵手，展开了深度的战略合作，进一步推进AI技术的发展。

OpenAI 发布
- 【2020-1-23】论文 [Scaling Laws for Neural Language Models](https://arxiv.org/pdf/2001.08361.pdf)
  - OpenAI 官方文章 [Scaling laws for neural language models](https://openai.com/research/scaling-laws-for-neural-language-models)
  - [解读](https://blog.csdn.net/CY19980216/article/details/125139643)
- 【2020-11-6】第二篇文章 OpenAI Scaling Paper: [Scaling Laws for Autoregressive Generative Modeling](https://arxiv.org/pdf/2010.14701), [解析大模型中的Scaling Law](https://zhuanlan.zhihu.com/p/667489780)

公式

$L(D)=\left(\frac{D}{D_{c}}\right)^{\alpha_{D}}, \alpha_{D} \sim-0.095, D_{c} \sim 5.4 \times 10^{13}$

$L(N)=\left(\frac{N}{N_{c}}\right)^{\alpha_{N}}, \alpha_{N} \sim-0.076, N_{c} \sim 8.8 \times 10^{13}$

说明
- L 值衡量模型拟合数据分布的准确性, 数值越小拟合越精确，对应学习能力就越强
- 模型最终性能主要与计算量`C`，模型参数量`N`和数据大小`D`三者相关，而与**模型结构**(层数/深度/宽度)基本无关。
- 模型性能与**模型规模**以及**数据规模**这两个因素高度正相关，而规模相同时，**模型架构**对性能影响相对较小。
  - 启发: 要提升模型性能，重点考虑**扩大模型规模**、**丰富训练数据集**
- L(N) 表示**数据**规模固定时, 不同**模型**规模下的交叉熵损失函数 —— **模型**规模对拟合能力的影响
- L(D) 表示**模型**规模固定时, 不同**数据**规模下的交叉熵损失函数 —— **数据**规模对模型学习能力的影响

核心结论
- 对于 Decoder-only 模型，计算量`C`(Flops), 模型参数量`N`, 数据大小`D`(token数)，三者满足: `C ≈ 6ND`
  - 如果计算预算`C`增加, 模型要达到最优性能, 数据规模`D`、模型规模`N`, 应同步增加
  - 但是, <span style='color:red'>模型规模增长速度应该略快于数据规模</span>, 最优配置比例 `Nopt ∝ C^0.73`, `Dopt ∝ C^0.27`, 即 如果总计算预算增加10倍, 模型规模 `N` 应扩大 5.37 倍, 而数据规模应扩大 1.86 倍
- 计算量`C`，模型参数量`N`和数据大小`D`，当不受其他两个因素制约时，模型性能与每个因素都呈现**幂律**关系
  - ![](https://pic3.zhimg.com/80/v2-3aa5475bcadc607ea96f20136158f80a_1440w.webp)
- 为了提升模型性能，模型参数量`N`和数据大小`D`需要**同步放大**，但模型和数据分别放大的比例还存在争议。
- Scaling Law 不仅适用于语言模型，还适用于其他模态以及跨模态的任务

论文首次提出**模拟**神经语言模型的`模型性能`（Loss）与`模型大小`、`数据集大小`和`训练计算量`的关系。
- 三者中任何一个因素受限时，Loss与其之间存在`幂律关系`。
- 注：`幂律`指一个变量与另一个变量的**某个幂次**成正比。体现在图表中，当两个轴都是**对数**时，图像呈现为**直线**

总结：
- 影响模型性能的三个要素之间，每个参数会受到另外两个参数的影响。
- 当没有其他两个瓶颈时，性能会急剧上升，影响程度为: `计算量` > `参数` >> `数据集大小`
- **固定计算预算**训练时，最佳性能可通过训练参数量非常大的模型并在远离收敛前停止(Early Stopping)来实现。
- 更大的模型在样本效率方面表现更好，能以更少的优化步骤和使用更少的数据量达到相同的性能水平。
  - 实际应用中，应该优先考虑训练较大的模型。

因为这项研究，OpenAI 有了在数据和参数规模上 Scaling-up 信心，在同年四月后，火爆全球的GPT3问世。

### 2022 Chinchilla Scaling Law 数据不变


DeepMind
> We’re a team of scientists, engineers, ethicists and more, committed to solving intelligence, to advance science and benefit humanity.

—— DeepMind

DeepMind 成立于2010年, 并于2015年被谷歌收购，是 Alphabet Inc. 子公司。
- 该公司专注于开发能模仿人类学习和解决复杂问题能力的AI系统。
- 作为 Alphabet Inc.的一部分，DeepMind在保持高度独立的同时，也在利用谷歌的强大能力推动AI研究的发展。

DeepMind 在技术上取得了显著成就，包括
- 开发`AlphaGo`，击败世界围棋冠军李世石的AI系统，展示了深度强化学习和神经网络的潜力，开启了一个AI时代。
- `AlphaFold`，这是一个革命性的用于准确预测蛋白质折叠的工具，对生物信息学界产生了深远影响。DeepMind用AI进行蛋白质折叠预测的突破，将帮助我们更好地理解生命最根本的根基，并帮助研究人员应对新的和更难的难题，包括应对疾病和环境可持续发展。

OpenAI 说: 
- <span style='color:red'>模型规模增长速度应该略快于数据规模</span> —— 真的吗？

【2022-3-29】 DeepMind 探索了更大范围的模型（7000w~160b）+数据规模（5b~500b个token），提出了 `Chinchilla 扩展法则`, 发表论文
- [Training Compute-Optimal Large Language Models](https://arxiv.org/pdf/2203.15556.pdf) 根据`Scaling Law`，给定计算量（FLOPS）训练出来的最优模型（达到最好模型效果）的训练数据集的token数和模型参数数目是确定的。

Chinchilla 扩展法则是 OpenAI 扩展法则的补充和优化。
- 强调 数据规模 对模型性能提升的重要性
- 模型规模+数据规模应该同等比例增加

开创了LLM发展新方向
- 不再单纯追求扩大模型规模，而是<span style='color:green'>优化模型规模与数据规模比例</span> —— 别再“大力出奇迹”了！


公式
- `L(N,D) = E + A/Na + B/Db`
- E=1.69, A=406.4, B=410.7, a=0.34, b=0.28
- 指定计算量下的最优分配：数据集规模 D 与 模型规模 N
  - `Nopt ∝ C^0.73` --> `Nopt ∝ C^0.46`
  - `Dopt ∝ C^0.27` --> `Dopt ∝ C^0.54`
- 数据集量 D 与模型规模同等重要
  - 如果计算预算增加10倍，模型规模 和 数据规模 应该扩大约 3.16 倍
  - 2023年5月，发布 PaLM2 技术报告，证实以上结论

另外, 理想数据集大小应当是模型规模的**20倍**
- 7b 模型最理想的训练数据为 140b 个token
- 而 OpenAI的 `GPT-3` 模型最大版本175b, 但训练数据只有300b个token
- 微软 `MT-NLG` 模型 530b, 训练数据只有 270b
- 于是, `DeepMind` 推出符合20倍原则的模型: `Chinchilla`, 70b, 1.4 万亿个token, 性能上取得突破

Gopher 模型计算量预算是 5.76 × 10^23 FLOPs，那么达到最优效果的参数量是 63B，数据集中Token数目为**1.4T**。
- ![](https://pic1.zhimg.com/50/v2-2d9fd7904ce7c251767a82f586a53a27_720w.jpg)

Deepmind 的 Hoffmann 等人团队提出与OpenAI**截然不同**的观点。
- OpenAI 建议在**计算预算**增加了**10倍**情况下，如果想保持效果，**模型大小**应增加**5.5倍**，而训练**token数量**仅需增加**1.8倍**。
- Deepmind 则认为**模型大小**和训练**token数**都应该按**相等比例**进行扩展，即都扩大**3倍**左右。

该团队还暗示许多像 GPT-3这样的千亿参数大语言模型实际上都**过度参数化**，超过了实现良好的语言理解所需，并训练不足。

结论：
- 对于给定FLOP预算，损失函数有明显的谷底值：
  - 模型**太小**时，在较少数据上训练较大模型将是一种改进；
  - 模型**太大**时，在更多数据上训练的较小模型将是一种改进。
- 给定计算量下，数据量和模型参数量之间的选择平衡存在一个**最优解**。
  - 计算成本达到最优情况下，**模型大小**和训练**数据** (token) 数量应该**等比例**进行缩放，即：如果模型的大小加倍，那么训练数据的数量也应该加倍。
- 给定参数量模型，最佳**训练数据集**大小约为**模型参数**的**20倍**。
  - 比如，对于一个7B模型，理想训练数据集大小应该约为 140B tokens。

大模型训练要更加关注数据集的扩展，但是只有数据是高质量的时候，更大数据集的益处才能体现出来。

大语言模型发展的一个新方向
- 从一味追求**模型规模**的增加，变成了优化模型规模和数据量的**比例**。

保持训练数据不变的情况下，扩大模型大小，当前的大型语言模型实际上训练不足

作者训练了从7000万到超过160亿参数的400多个语言模型，这些模型使用的训练令牌从50亿到5000亿不等，并得出结论:
- 对于计算优化的训练，模型大小和训练令牌数量应该**同等**规模化。

经验预测公式，将模型大小和训练数据与模型性能联系起来。
- `L(N,D) = A/N^α + B/D^β + E`
- N 是**参数数量**（即模型大小），D 是**训练令牌**。
- 符号 L(N,D) 指一个拥有 N 个参数并且在 D 个令牌上训练的模型的性能或测试损失。
- E 是一个常数，代表不可约减的损失，即模型在完美训练的情况下能够达到的最小损失。它考虑了模型所训练的任务的固有难度和数据中的噪声。

常数 A 和 B 以及指数 α 和 β 通过实验和数据拟合经验性地确定。
- α≈0.50 和 β≈0.50。
- 主要发现: 每翻倍增加模型大小时，训练令牌的数量也应该翻倍，以实现计算最优训练

`边际效益递减`
- 随着模型规模的增大，每增加相同数量的参数/计算资源，获得的**性能提升逐渐减少**的现象。

这是 Scaling Law 中非常关键的一个方面，它对于理解和决策模型设计及其部署策略有着重要的指导意义。

原因和表现
- **对数关系**：很多研究中观察到，模型性能（如测试集上的准确率或其他指标）与模型大小（通常是参数数量或计算复杂度）呈**对数关系**。随着模型规模的扩大，要获得同样幅度的性能提升，需要的资源增加将更为显著。
- 资源效率的降低：当模型规模达到一定阶段后，继续增加模型的大小，其性能提升不再明显，而相对应的训练成本、时间和能源消耗却显著增加。这种现象表明，从成本效益角度出发，**模型规模的无限扩大并不合理**。
- 技术挑战：较大的模型更难训练，可能会面临梯度消失或爆炸、过拟合等问题，这些技术挑战也限制了模型性能的持续提升。

应对策略
- 模型和算法**创新**：通过改进模型架构、优化算法或引入新的训练技术（如稀疏化、量化等），可以在不显著增加参数的情况下提高模型的效率和效果。
- `多任务学习`和`迁移学习`：利用多任务学习和迁移学习技术可以提高模型的泛化能力，使得模型在多个任务上具有更好的性能，这种方式可以在一定程度上克服单一任务上的边际效益递减问题。
- 选择适当的规模：根据应用场景的实际需求和可用资源，选择合适的模型规模，避免资源的浪费，实现性能与成本的最优平衡。

`缩放法则`对AI研究者和工程师具有重大意义：
- 平衡规模化：Chinchilla 强调了同时对模型大小和训练数据进行等比例规模化以达到最佳性能的重要性。这挑战了之前仅增加模型大小的重点。
- 资源分配：理解这些关系可以更有效地分配计算资源，可能导致更具成本效益和环境可持续的人工智能发展。
- 性能预测：这些法则使研究人员能够根据可用资源做出有根据的模型性能预测，帮助设定现实的目标和期望。



## Scaling Law 观点


Chomsky （乔姆斯基） 认为
- 尽管模型可以做到句法分析，但仍然无法理解语义

观点
- 句子可以有意义，但还不能让段落连贯起来。

最新质疑
- 数据马上就要耗尽了
- 数据质量不够高
- 模型不能进行推理等等

### 量化不管用

【2024-11-13】 [Scaling Law终结，量化也不管用，AI大佬都在审视这篇论文](https://www.huxiu.com/article/3679706.html)

哈佛、斯坦福、MIT等团队的一项研究表明：训练的token越多，需要的精度就越高。
- 例如，Llama-3在不同数据量下（圆形8B、三角形70B、星星405B），随着数据集大小的增加，计算最优的精度也会增加。
- 对于大规模的训练任务，低精度的量化可能不再足够有效。

按照结论，对 Scaling Law 的遵循意味着需要保持更高精度，然而一直以来，人们通常会选择**量化**（将连续值或多精度值转换为较低精度）来节省计算资源。

一旦结论成立，GPU 设计和功能可能也需要相应调整，因为传统上，GPU 性能提升部分依赖于对低精度计算的优化。

结论：
- 如果量化是在后训练阶段进行，那么更多的预训练数据最终可能**反而有害**；
- 在高（BF16）和下一代（FP4）精度下进行预训练可能都是**次优**的设计选择；

这也引来OpenAI员工大赞特赞：
- 将非常酷地看到如何SOTA量化方案（mxfp，Pw≠Pkv≠Pa等）推动前沿；在我看来，将一半的计算预算用于一次大规模运行，以检查模型是否适用于大模型是值得的。

### ttt 能继续挖掘

【2024-11-12】[连OpenAI都推不动Scaling Law了？MIT把「测试时训练」系统研究了一遍，发现还有路](https://www.jiqizhixin.com/articles/2024-11-12-7)

OpenAI 下一代旗舰模型的质量提升幅度不及前两款旗舰模型之间的质量提升，因为高质量文本和其他数据的供应量正在减少，原本的 Scaling Law（用更多的数据训练更大的模型）可能无以为继。此外，OpenAI 研究者 Noam Brown 指出，更先进的模型可能在经济上也不具有可行性，因为花费数千亿甚至数万亿美元训练出的模型会很难盈利。

从预训练来看，Scaling Law 可能会放缓；

但有关推理的 Scaling Law 还未被充分挖掘，OpenAI o1 的发布就证明了这一点。它从后训练阶段入手，借助**强化学习**、原生的**思维链**和更长的**推理时间**，把大模型能力又往前推了一步。
- 这种范式被称为「`测试时计算`」，相关方法包括**思维链提示**、**多数投票采样**（self-consistency）、**代码执行**和**搜索**等。


### 扩展法则还没到上限

【2024-11-21】[Dario Amodei：Scaling Law 还没遇到上限](https://mp.weixin.qq.com/s/OMEh6exeYmF48Pl4rb-8hg)

Anthropic CEO `Dario Amodei` 在 "**Machines of Loving Grace**" 里, AGI 对世界的影响进行了预言：
- Powerful AI 预计会在 **2026 年**实现，足够强大的 AI 也能够将把一个世纪的科研进展压缩到 5-10 年实现（“Compressed 21st Century”）

和 Lex Fridman 的最新访谈中，Dario 解释了自己对于 Powerful AI 可能带来的机会的理解，以及 scaling law、RL、Compute Use 等模型训练和产品的细节进行了分享：
- • <span style='color:red'>Scaling law 目前尚未见顶</span>， **合成数据**和 **reasoning models** 可能是解决数据限制的方案
- • 未来 post-training 环节的成本可能会超过 pre-training，只靠人类很难提高模型质量，需要更 scalable 的**监督**方法
- • Anthropic 的优势之一就是 RL，并且可能是做 RL 做得最好的，
- • Anthropic 内部工程师认为 `Sonnet 3.5` 是第一个能节省时间的模型，但团队目前并不打算开发自己的 IDE，
- • 出于安全性的考虑，Computer Use 目前不会直接面向 to C 开放，而是以 API 的形式发布 ，
- • “Compressed 21st Century” 的愿景下，AGI 可以在生物学和医学领域推动突破性进展，因为监管、伦理以及生物系统本身的复杂性，AI 建模生物系统的难度很高，但 AI 系统至少可以帮助改进临床试验系统，提高临床试验的效率和成功率
- • 今天科学家带领科研团队的模式在未来会变成科学家和 AI 系统一起工作，这些 AI 系统可以像研究助理一样被分配到具体研究任务中，
- • LLMs 领域还有很多问题值得研究，比如机制可解释性和 Long Horizon 是很值得关注的领域，





### Ilya

【2024-9-5】Ilya 的公司 SSI 将以与OpenAI不同的方式, 继续 Scaling：
> 每个人都只是在说 `Scaling Hypothesis`，每个人都忽略了问：**我们在Scaling什么？**
>- 有些人可以**长时间工作**，但他们只是以更快的速度**走同样路径**，这不是我们的风格。
>- 但如果做些不同的事情，那么你就有可能做出一些特别的事情。



### 证伪

【2024-4-1】[Scaling Law 被证伪，谷歌研究人员实锤研究力挺小模型更高效](https://www.toutiao.com/article/7354993866975805990)
- 论文 [Bigger is not Always Better: Scaling Properties of Latent Diffusion Models](https://arxiv.org/pdf/2404.01367.pdf)

Scaling Law 再次被 OpenAI带火，人们坚信：“模型越大，效果越好”

但谷歌研究院和约翰霍普金斯大学的研究人员对人工智能 (AI) 模型在图像生成任务中的效率有了新的认识：并非“越大越好”

实验设计 12 个文本到图像 LDM，其参数数量从 3900 万到惊人的 50 亿不等。

然后，这些模型在各种任务上进行了评估，包括文本到图像的生成、超分辨率和主题驱动的合成。
- 给定推理预算下（相同的采样成本）运行时，较小模型可胜过较大的模型。
  - 当计算资源有限时，更紧凑的模型可能比较大、资源密集的模型能够生成更高质量的图像。
  - 这为在模型规模上加速LDMs提供了一个有前景的方向。
- 采样效率在多个维度上是一致的

#### 国内

国内讨论 Scaling Laws 论文不多。目前部分公开资料: 百川智能 `Baichuan2` 和 北京理工大学的`明德大模型`（MindLLM）论文中讲述了自己对scaling law的尝试。

两者在真正着手训练数十亿或者百亿参数的大语言模型之前，训练多个小型模型为训练更大的模型拟合拓展规律。
- 在同一套（足够大）的训练集上，采用一致的超参数设置，独立训练每个模型，收集训练的计算量和最终损失。
- 而后以OpenAI论文中结论的**幂律关系**拟合，预测出期望参数量模型的训练损失。

百川做法在开始训练7B和13B参数量模型前，设计大小从1000万到30亿不等的7个模型，采用一致的超参数，在高达1Ttoken的数据集上进行训练。

基于不同模型的损失，拟合出了训练浮点运算次数（flops）到训练损失的映射，并基于此预测了最终大参数模型的训练损失。

`Baichuan2` 缩放定律:
- 使用1万亿个token训练从1000万到30亿参数不等的7个模型，对给定训练浮点运算次数（flops）时的训练损失进行**幂律拟合**（蓝线），从而预测了在2.6万亿token上训练 Baichuan2-7B 和 Baichaun2-13B的损失。拟合过程精确预测了最终模型的损失（两颗星标记）

`明德`大模型团队的关注点与百川相似，在训练3B模型前，在10b Tokens 上训练了参数量从1000万到5亿的5个模型，通过分析各个模型的最终损失，同样基于幂律公式，建立从训练浮点运算次数（FLOPs）到目标损失的映射，以此预测最终大参数模型的训练损失。

`MindLLM` 缩放定律: 
- 100亿token的数据集上训练参数从1000万到5亿参数的5个模型。通过对训练浮点运算次数（FLOPs）和损失幂律拟合，预测使用5000亿token的数据集训练MindLLM-3B的最终训练损失。该拟合过程准确预测了模型的最终损失，用星星标记。

李开复`零一万物`团队的`黄文灏`，在知乎上关于Yi大模型的回答也较有代表性：”Scaling Law is all you need：很多人都认为scaling law 就是用来算最优的数据和参数量的一个公式，但其实scaling law能做的事情远不止如此。

为了真正理解scaling law
- 第一件事就是**忘记Chinchilla Scaling Law**
- 然后打开 OpenAI 的 Scaling Law的paper，再把paper中OpenAI引用自己的更早的paper都详细的读几十遍"。

更多见【2024-1-5】[OpenAI与DeepMind的Scaling Laws之争](https://hub.baai.ac.cn/view/34084)


## 应用

[解析大模型中的Scaling Law](https://zhuanlan.zhihu.com/p/667489780)

### GPT-4

GPT4报告中 Scaling Law曲线，计算量C和模型性能满足幂律关系
- ![](https://pic1.zhimg.com/80/v2-1f6306d2d33a66bd7de98f374fd3e406_1440w.webp)
- 横轴是归一化之后的**计算量**，假设GPT4计算量为1。基于10,000倍小的计算规模，能预测最终GPT4的性能。
- 纵轴是"Bits for words", **交叉熵**单位。在计算交叉熵时，如果使用以 2 为底的对数，`交叉熵`单位是 "bits per word"，与`信息论`中的比特（bit）概念相符。所以这个值越低，说明模型的性能越好。


### Baichuan2

Baichuan2 技术报告中的 Scaling Law曲线。

基于10M~3B 模型在1T数据上训练的性能，可预测出最后7B模型和13B模型在2.6T数据上的性能
- ![](https://pic4.zhimg.com/80/v2-704359ac707ceaaf7965555cc56dd2f5_1440w.webp)

幂律定律
- 模型参数固定，**无限堆数据并不能无限提升模型性能**，模型最终性能会慢慢趋向一个固定值

实验数据
- ![](https://pic1.zhimg.com/80/v2-844a2d16cad92d28b0736c0211abe086_1440w.webp)

#### 如何计算

如果模型参数量为 10^3（紫色线），数量达到10^9，模型基本收敛。继续增加数据，产生的计算量，没有同样计算量下提升模型参数量带来的收益大（计算效率更优）。

根据 `C=6ND` ，进一步转换成**模型参数**与**计算量**关系，即:
- 模型参数为 10^3，计算量为 `6*10^12` Flops，即 `7*10^(-8)` PF-days时, 基本收敛。右图中紫色线拐点。

Baichuan 实验
- 中英场景下，7B 模型收敛时的算力是 10^23 FLOPS，对应数据量应该是 $ D=\frac{10^23}{6*7*10^9}=2.3T $

计算效率最优时，**模型参数**与**计算量**幂次成**线性关系**，**数据量大小**也与**计算量**幂次成线性关系。

观点
- OpenAI 认为**模型规模**更重要，即 a=0.73, b=0.27
- 而 DeepMind 在 Chinchilla工作和Google在PaLM工作中都验证了 a=b=0.5 ，即**模型和数据同等重要**。

假定计算量整体放大**10倍**
- OpenAI 认为模型参数更重要，模型应放大 10^0.73=5.32 倍，数据放大 10^0.27=**1.86** 倍；
- DeepMind和Google认为模型参数量与数据同等重要，两者都应该分别放大 10^0.5=**3.16** 倍。

最好在自己的数据上做实验来获得你场景下的a,b

### MindLLM

MindLLM 技术报告中 Scaling Law曲线。

基于10M~500M 模型在10B数据上训练的性能，预测出最后3B模型在500B数据上的性能。
- ![](https://pic2.zhimg.com/80/v2-11c690520359c7484bbf23ba520e8ed9_1440w.webp)


### LLaMA

LLaMA: 反Scaling Law 大模型

假设遵循**计算效率最优**来研发LLM，那么根据 Scaling Law，给定**模型大小**，可推算出**最优计算量**，进一步根据最优计算量就能推算出需要的**token数量**，然后训练就行。

但是**计算效率最优**是针对**训练**阶段而言，并不是**推理**阶段，实际应用中推理阶段效率更实用。

Meta 在 LLaMA 的观点是：
- 给定模型目标性能，并不需要用最优的计算效率在最快时间训练好模型，而应该在**更大规模的数据上，训练一个相对更小模型**，这样的模型在推理阶段的成本更低，尽管训练阶段的效率不是最优的（同样的算力其实能获得更优的模型，但是模型尺寸也会更大）。
- 根据 Scaling Law，**10B**模型只需**200B**数据，但是**7B**模型性能在**1T**数据后还能继续提升。

所以, LLaMA 重点是训练一系列语言模型，通过使用更多数据，让模型在有限推理资源下有最佳的性能。
- 确定模型尺寸后，Scaling Law 给到的只是**最优数据量**，一个至少的数据量，实际在训练中观察在各个指标上的性能表现，只要还在继续增长，就可以持续增加训练数据。



# 结束