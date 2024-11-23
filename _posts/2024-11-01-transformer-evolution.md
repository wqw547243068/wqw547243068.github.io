---
layout: post
title:  Transformer 改进方案
date:   2024-11-01 16:52:00
categories: 深度学习 
tags: 深度学习 NLP Transformer BERT GPT Attention BeamSearch seq2seq 杨植麟 XLNet 循环智能 roformer rwkv 苏剑林 检索 芯片 序列化 注意力 三蓝一棕 帕累托 retnet yoco kan 通用逼近定理 叠加定理 样条 可视化 ttt 三蓝一棕
excerpt: Attention is all you need!
mathjax: true
permalink: /trans_new
---

* content
{:toc}


# Transformer 改进方案

## Transformer 问题


【2023-9-18】[RetNet：万众期待的 Transformers 杀手](https://mp.weixin.qq.com/s/HhRtxONjzkoOmSRqixX50g), [头条](https://www.toutiao.com/article/7304956621552501285/)

Transformer 已成为大语言模型上的架构，因为它有效地克服了循环神经网络 (RNN) 的顺序训练问题。

然而，Transformer 并不完美，因为仅解决了所谓“`impossible triangle`”的**两**条臂。

“不可能三角”代表当前序列模型无法同时实现**训练并行性**、**低成本推理**以及**强大性能**的所有3个期望维度。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-axegupay5k/e154053c06d24a3a8c24253b5185346e~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1701422819&x-signature=oxc1OeNc6B1%2BDAdIQ%2BaOw8jw%2BA0%3D)

三角上的方法表示实现的两个维度，但缺少第三个顶点的所需属性。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/7c1f587ebec642bf9332284352e4a64d~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1701422819&x-signature=nYJb%2B%2FFDdkA1f%2F5FLtlAkG5XEVY%3D)


## 可解释性


### 白盒 transformer -- CRATE

【2023-11-30】[「GPT-4只是在压缩数据」，马毅团队造出白盒Transformer，可解释的大模型要来了吗？](https://mp.weixin.qq.com/s/ErrCWbz8zDqSYkC9DH79Mg)

伯克利和香港大学的`马毅`教授领导的一个研究团队给出了自己的最新研究结果：
> 包括 GPT-4 在内的当前 AI 系统所做的正是压缩。

提出的新深度网络架构 CRATE，通过数学方式验证了这一点。
- CRATE 是一种**白盒 Transformer**，其不仅能在几乎所有任务上与**黑盒 Transformer** 相媲美，而且还具备非常出色的**可解释性**。

基于此，马毅教授还在 Twitter 上分享了一个有趣的见解：
- 既然当前的 AI 只是在压缩数据，那么就只能学习到数据中的**相关性 / 分布**，所以就并不真正具备**因果或逻辑推理**或抽象思考能力。

因此，当今的 AI 还算不是 AGI，即便近年来在处理和建模大量高维和多模态数据方面，深度学习在实验中取得了巨大的成功。

这种成功归功于深度网络能有效学习数据分布中**可压缩的低维结构**，并将该分布转换为简约（即紧凑且结构化的）表征。这样的表征可用于帮助许多下游任务，比如视觉、分类、识别和分割、生成。

表征学习是通过压缩式编码和解码实现的

白盒深度网络理论。为学习紧凑和结构化的表征提出了一个统一目标，有原理保证的优良度度量。对于学习到的表征，该目标旨在既优化其在编码率下降方面的内在复杂性，也优化其在稀疏性方面的外在复杂性。该目标称为 `稀疏率下降`（sparse rate reduction）。

为了优化这个目标，提出学习一个**增量映射序列**，模拟展开目标函数的某些类似梯度下降的迭代优化方案。这得到一个类似 Transformer 的深度网络架构，并且它完全是一个「白盒」—— 其优化目标、网络算子和学习到的表征在数学上是完全可解释的。

这个白盒深度架构命名为 `CRATE` 或 `CRATE-Transformer`，这是 `Coding-RATE transformer` 的缩写。还通过数学方式证明这些增量映射在分布的意义上是可逆的，并且它们的逆映射本质上由同一类数学算子构成。

因此，可以将几乎完全一样的 CRATE 架构用于编码器、解码器或自动编码器。

## 模型结构

如果说 RetNet 是从**平行推理效能**的角度革新了网络架构，那么 BitNet 则从正交角度提升了推理效率。

这两者的结合，以及融合其他提升模型效率的技术比如混合专家模型（MoE）和稀疏注意力机制（Sparse Attention），将成为未来基础模型网络架构的基础。


### RetNet

【2023-9-18】[RetNet：万众期待的 Transformers 杀手](https://mp.weixin.qq.com/s/HhRtxONjzkoOmSRqixX50g), [头条](https://www.toutiao.com/article/7304956621552501285/)

微软的 RetNet 位于这个“`impossible triangle`”的正中心，胜过了所有尝试过但未能实现这一壮举的方法。RetNet 设法在单个框架下实现所有属性。

突破：
- RetNet 具有更好的语言建模性能
- RetNet 内存消耗降低了 3.4 倍
- ….8.4 倍更高的吞吐量
- …延迟降低 15.6 倍

这速度比当前的 SOTA 快**几个数量级**，同时还提供更好的性能！如果其他团队能够复制这一点并且进入开源领域，这将是巨大的进步，但目前微软绝对是「遥遥领先」

RetNet的主要贡献可以概括为两大点
- RetNet引入**多尺度保留机制**来替代**多头注意力**。这是消除自注意力机制中的魔鬼这一组成部分的关键。尽管如此，这种保留机制有一个小小的理论上的缺点。
- RetNet 适用于三种计算范式，而只有一种 Transformer 在训练和推理过程中使用相同的序列处理范式。
  - A. **并行**表示使训练并行性能够充分利用 GPU 设备。
  - B. **循环**表示在内存和计算方面可实现高效的 O(1) 推理。可以显着降低部署成本和延迟。此外，在没有键值缓存技巧的情况下，实现也得到了极大的简化。
  - C. **分块循环**表示可以执行有效的长序列建模。对每个本地块进行并行编码以提高计算速度，同时对全局块进行循环编码以节省 GPU 内存。

新型基础网络架构 Retentive Network（`RetNet`）成功突破了所谓的“`不可能三角`”难题，实现了`帕累托`（Pareto）优化。
- RetNet 在保持良好的扩展性能和并行训练的同时，实现了低成本部署和高效率推理。

RetNet 推理成本与模型序列长度无关，这表示无论是处理长文本序列，还是长图像序列，亦或是未来更长的音视频序列，RetNet 都可以保持稳定的高效推理。


### 微软 BitNet

【2024-2-29】[BitNet b1.58：开启1-bit大语言模型时代](https://mp.weixin.qq.com/s?__biz=MzAwMTA3MzM4Nw==&mid=2649498640&idx=1&sn=a860101ceee6bc3a777f465bdd1586da&chksm=82c7cd94b5b0448231f0017d2694e59f6e41369ea14a38a3a19a32a9ba18c3fe0f934e214bee&scene=21#wechat_redirect)

微软亚洲研究院推出了 1-bit LLM 新变体：`BitNet b1.58`。
- 论文标题：[The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits](https://arxiv.org/pdf/2402.17764.pdf)

该模型每个参数仅使用三值表示，即-1, 0 或 1。因此，在 LLM 的矩阵乘法操作中只需要整数加法，而不需要任何浮点数乘法或加法。在语言模型困惑度和下游任务性能的评估中
- BitNet b1.58 能够与具有相同参数量和训练数据量的全精度（即FP16或BF16）Transformer LLM 相匹敌。
- 与此同时，它在速度、内存使用、吞吐量和能耗等方面具有大幅优势。

BitNet b1.58 为训练新一代高性能高效率的 LLMs 确立了新的**扩展定律**（scaling law）和方法。此外引领了一种全新的计算范式，并为开发专为 1-bit LLMs 优化的硬件设备铺平了道路。

BitNet 是第一个支持训练1比特大语言模型的新型网络结构，具有强大的可扩展性和稳定性，能够显著减少大语言模型的训练和推理成本。

与最先进的8比特量化方法和全精度 Transformer 基线相比，BitNet 在大幅降低内存占用和计算能耗的同时，表现出了极具竞争力的性能。

此外，BitNet 拥有与全精度 Transformer 相似的**规模法则**（Scaling Law），在保持效率和性能优势的同时，还可以更加高效地将其能力扩展到更大的语言模型上，从而让1比特大语言模型（1-bit LLM）成为可能。

### 微软 YOCO

【2024-5-13】[YOCO：打破传统Decoder-only架构，内存消耗仅为Transformer的六分之一](https://mp.weixin.qq.com/s/X4HSyEreN4L4xTizC-_mow)

模型架构还只有三大类：Decoder-Only、Encoder-Only、Encoder-Decoder。

微软亚洲研究院推出了一种创新性的 Decoder-Decoder 架构 `YOCO`（You Only Cache Once）。通过**自解码器**和**交叉解码器**的独特架构，YOCO 仅需缓存一次键值对，从而显著降低 GPU 内存的使用。
- 论文 [You Only Cache Once: Decoder-Decoder Architectures for Language Models](https://arxiv.org/abs/2405.05254)

模型评估中，YOCO 展现出与同规模 Transformer 模型相媲美的性能，并在语言建模评估、模型大小扩展以及长上下文处理方面具有显著优势。特别是在降低 GPU 内存占用和缩短预填充延迟方面，

YOCO 整体架构设计如下，分为`自解码器`（Self-Decoder）和`交叉解码器`（Cross-Decoder）两部分。

YOCO 实现了“**模型越大，内存越省**”，为自然语言处理领域带来了全新的研究和应用范式。
- YOCO 仅缓存一次键值对，可大幅降低 GPU 内存需求，且保留全局注意力能力。

打破 GPT 系列开创的 `Decoder-Only` 架构——提出 `Decoder-Decoder` 新型架构，名为 `YOCO` (You Only Cache Once)。
- 在处理 512K 上下文长度时，标准 Transformer 内存使用是 YOCO 的6.4倍，预填充延迟是 YOCO 的30.3倍，而 YOCO 的吞吐量提升到标准 Transformer 的9.6倍。


## 位置编码方式



### 2021.3.23 Roformer

【2021-3-23】Rotary Transformer，简称 `RoFormer`，是追一科技`苏剑林`自研的语言模型之一，主要是为Transformer结构设计了新的`旋转式位置编码`（Rotary Position Embedding，`RoPE`）。
- `RoPE`具有良好的理论性质，且是目前**唯一**一种用到线性Attention的绝对位置编码，目前来看实验结果也颇为不错。
- 参考配置：在24G显存的3090上，跑maxlen=1024，batch_size能跑到8以上。

详细介绍：
- [Transformer升级之路：2、博采众长的旋转式位置编码](https://kexue.fm/archives/8265)

使用

- [pytorch版本](https://github.com/JunnYu/RoFormer_pytorch)
- huggingface [roformer](https://huggingface.co/docs/transformers/model_doc/roformer)

```py
from transformers import RoFormerTokenizerFast

tokenizer = RoFormerTokenizerFast.from_pretrained("junnyu/roformer_chinese_base")
tokenizer.tokenize("今天天气非常好。")
```


## 检索增强

增大模型并不是提升性能的唯一路径，用一种搜索/查询信息的方式来增强模型，小的生成语言模型也能达到之前大模型才能达到的性能。

语言模型的任务是做**填空题**，这对于语言信息有意义，但是对于事实信息和世界知识信息是无效的。
- 有时需要与事实有关的信息

代表
- DeepMind 的 RETRO Transformer
  - DeepMind 的 RETRO（Retrieval-Enhanced TRansfOrmer）模型。该模型与 GPT-3 性能相当，但参数量仅为 GPT-3 的 4%。
- OpenAI 的 WebGPT


### 2021.12.16 WebGPT

OpenAI 推出 WebGPT, 解决 long-form quesion-answering (LFQA) 的方案, 开放域QA回复更长更可靠。
- [WebGPT: Improving the factual accuracy of language models through web browsing](https://openai.com/research/webgpt)
- [WebGPT简读](https://zhuanlan.zhihu.com/p/591565418)
- 比 InstructGPT 提出稍早一些

WebGPT 思路类似 Knowledge-Grounded Conversation，利用搜索引擎做相关文档检索，从而生成更长的答案。主要的两个贡献：
- 微调的语言模型可以与一个基于文本的Web浏览环境交互，从而可以端到端地使用模仿和强化学习优化检索和聚合效果。
- 参考Web检索出来的信息生成回复。labeler可以根据检索出来的信息判断factual准确率，降低了独立调研问题正确性的难度。

这个想法并非 WebGPT首次提出
- 2021年初, Facebook (FAIR) 就提出使用搜索引擎来提升对话回复的质量：ACL2022 [Internet-Augmented Dialogue Generation](https://aclanthology.org/2022.acl-long.579/)

WebGPT 思路更进一步，完全模拟了人使用搜索引擎的方法(有更多action: 搜索、点击、翻页、回退等等)，而非仅生成search query并使用其结果。

### 2022.2.7 RETRO

DeepMind 推出 RETRO, 整合了从数据库中检索到的信息，将其参数从昂贵的事实和世界知识存储中解放出来。
- 论文: [Improving language models by retrieving from trillions of tokens](https://arxiv.org/pdf/2112.04426.pdf)
- [illustrated-retrieval-transformer](http://jalammar.github.io/illustrated-retrieval-transformer)
- 【2022-1-4】[参数量仅为4%，性能媲美GPT-3：开发者图解DeepMind的RETRO](https://www.jiqizhixin.com/articles/2022-01-04-8)

加入检索方法之后，语言模型可以缩小很多。
- 神经数据库可以帮助模型检索它需要的事实信息。
- ![](https://image.jiqizhixin.com/uploads/editor/ffbea1f3-54eb-411d-a9a9-3c0912dfef3c/1641280248346.png)

#### 模型结构

结构
- RETRO 是 **编码器 - 解码器**模型，像原始的 Transformer。
- 然而在检索数据库的帮助下增加了**输入序列**。
- 该模型在数据库中找到最可能的序列，并添加到输入中。
- RETRO 利用它的魔力生成输出预测。
- ![](https://image.jiqizhixin.com/uploads/editor/96d18172-b521-4ed5-a913-a00440b05625/1641280241153.png)


#### RETRO 检索数据库

这里的数据库是一个**键值存储**（key-value store）数据库。
- key 是标准的 **BERT 句子嵌入**，value 是由两部分组成的**文本**：
- Neighbor，用于计算 key；
- Completion，原文件中文本的延续。

RETRO 数据库包含基于 MassiveText 数据集的 2 万亿个多语言 token。neighbor chunk 和 completion chunk 的长度最多为 64 个 token。
- ![](https://image.jiqizhixin.com/uploads/editor/713760aa-cf75-4bc7-8116-e308ce3b8b83/1641280228557.png)

#### 数据库查找

进入 RETRO 前
- 输入提示进入 BERT。对输出的上下文向量进行**平均**以构建句子嵌入向量。
  - ![](https://image.jiqizhixin.com/uploads/editor/3e8b9491-570a-4280-b36a-e68a6d0fff7c/1641280220663.png)
- 然后，使用该向量查询数据库。近似最近邻搜索。检索两个最近邻
  - ![](https://image.jiqizhixin.com/uploads/editor/aac2a845-a303-415b-b582-7b55402db078/1641280209906.png)
- 将这些添加到语言模型的输入中
  - 检索出的文本成为 RETRO 输入的一部分，Transformer 和 RETRO 块将信息合并到它们的处理中
  - ![](https://image.jiqizhixin.com/uploads/editor/ff98762d-0d34-4771-8753-56d6b7762648/1641280203796.png)


#### 高层次的 RETRO 架构

RETRO 架构由一个**编码器**堆栈和一个**解码器**堆栈组成。
- 编码器由标准的 Transformer 编码器块（self-attention + FFNN）组成。Retro 使用由两个 Transformer 编码器块组成的编码器。
  - 编码器堆栈会处理检索到的近邻，生成后续将用于注意力的 KEYS 和 VALUES 矩阵
- 解码器堆栈包含了两种解码器 block：
  - 标准 Transformer 解码器块（ATTN + FFNN）
  - RETRO 解码器块（ATTN + Chunked cross attention (CCA) + FFNN）
- 解码器 block 像 GPT 一样处理输入文本。对提示 token 应用自注意力（因此只关注之前的 token），然后通过 FFNN 层。只有到达 RETRO 解码器时，它才开始合并检索到的信息。从 9 开始的每个第三个 block 是一个 RETRO block（允许其输入关注近邻）。所以第 9、12、15…32 层是 RETRO block。
- ![](https://image.jiqizhixin.com/uploads/editor/5103886f-035d-4506-9e03-32b9ec93259b/1641280193608.png)
- ![](https://image.jiqizhixin.com/uploads/editor/305626c2-7918-419a-9e4c-5c8d7eaf0e60/1641280182910.png)




## 输入输出 改进


输入长度改进

### 2023.7.8 LongNet

【2023-7-8】[1000000000！微软改进Transformer一次能记住这么多token了](https://mp.weixin.qq.com/s/PKKC4lMdSTg-ButNnZHLlw)
- 最强的GPT-4也才最大支持一次处理32k token，相当于50页文字。
- 而能够只用1分钟看完一本数万字小说的Claude，其token数也不过“才”100k（10万）。

一次性扩展到10亿，并且这个数字理论上其实还是无限的，这不就意味着：不久的将来，整个语料库甚至互联网都能视为一个序列？

作者提出一个Transformer变体：`LongNet`，它应用了一种叫做“**膨胀注意力**（dilated attention）”的机制，可以随着距离的增长，让注意力场（模型感知范围）呈指数级扩展。

具体而言，dilated attention替代了普通Transformer中的注意力机制的，其一般的设计原则是：
> 让注意力的分配随着token之间距离的增长，呈指数级下降。

dilated attention能够产生线性计算复杂度和token之间的对数依赖性，从而解决了注意力资源有限，但每一个token都可访问的矛盾。


## MLP 改进

多层感知器（MLP）被称为**全连接前馈**神经网络，是当今深度学习模型的基础构建块。

MLP 重要性无论怎样强调都不为过，是机器学习中用于逼近非线性函数的默认方法。

然而，MLP 是否最佳非线性回归器呢？

尽管 MLP 被广泛使用，但存在明显缺陷。
- 例如，在 Transformer 模型中，MLP 几乎消耗了所有非嵌入式参数，并且通常在没有后处理分析工具的情况下，相对于注意力层来说，它们的可解释性较差。

### KAN

【2024-5-3】[Transformer要变Kansformer？用了几十年的MLP迎来挑战者KAN](https://www.jiqizhixin.com/articles/2024-05-03-3)

MIT 提出的 KAN 灵感来源于 Kolmogorov-Arnold 表示定理的网络。
- 论文：[KAN: Kolmogorov-Arnold Networks](https://arxiv.org/pdf/2404.19756)
- Github：[pykan](https://github.com/KindXiaoming/pykan)

KAN 在准确性和可解释性方面表现优于 MLP，而且能以非常少的参数量胜过以更大参数量运行的 MLP。

有研究者将 KAN 创新架构的理念扩展到卷积神经网络，将卷积的经典线性变换更改为每个像素中可学习的非线性激活函数，提出并开源 KAN 卷积（CKAN）
- 【2024-5-20】[替代MLP的KAN，被开源项目扩展到卷积了](https://www.jiqizhixin.com/articles/2024-05-20-2)
- [Convolutional-KANs](https://github.com/AntonioTepsich/Convolutional-KANs)

Kolmogorov 1957 年就发现了**多层**神经网络，比 Rumerhart、Hinton 和 William 的 1986 年论文发表的时间要早得多，但他却被西方忽视了。

一种有前景的多层感知器（MLP）的替代方案，称为 Kolmogorov-Arnold Networks（KAN）。
- MLP 的设计灵感来源于`通用近似定理` （通用逼近定理）
- 而 KAN 设计灵感则来源于 `Kolmogorov-Arnold 表示定理`。

Kolmogorov-Arnold 表示定理
- Vladimir Arnold 和 Andrey Kolmogorov 证明了如果 f 是一个在有界域上的**多变量连续函数**，那么 f 可以写成一个**单变量连续函数**和**二元加法运算**的有限组合。

与 MLP 类似，KAN 拥有**全连接**结构。而 MLP 在节点（神经元）上放置固定激活函数，KAN 则在边（权重）上放置可学习的激活函数。

因此，KAN **完全没有线性权重矩阵**： [对比图](https://image.jiqizhixin.com/uploads/editor/2ea4a752-4eb5-4bd7-a21f-1f228efcc427/640.png)
- 每个权重参数都被替换为一个可学习的一维函数，参数化为**样条**（spline）。
- KAN 的节点仅对传入信号进行求和，而不应用任何非线性变换。
- ![对比图](https://image.jiqizhixin.com/uploads/editor/2ea4a752-4eb5-4bd7-a21f-1f228efcc427/640.png)

尽管 KAN 数学解释能力不错，但实际上只是**样条**和 **MLP** 的组合，利用了二者的优点，避免了缺点的出现。
- 样条在低维函数上准确度高，易于局部调整，并且能够在不同分辨率之间切换。然而，由于样条无法利用组合结构，因此存在严重 COD 问题。
- 另一方面，MLP 由于其特征学习能力，较少受到 COD 的影响，但在低维空间中却不如样条准确，因为它们无法优化单变量函数。

KAN 的最大瓶颈: 训练速度慢。
- 相同数量的参数下，KAN 的训练耗时通常是 MLP 的 10 倍。
- KAN 训练速度慢更像是一个未来可以改进的工程问题，而不是一个根本性的限制

## Attention 改进


### QKV

MHA、GQA、MQA、MLA 原理对比
- 传统 Transformer 采用 MHA，但 KV Cache 在推理过程中可能成为性能瓶颈。
- `MQA` 和 `GQA` 虽然在一定程度上可以减少KV Cache的占用，但效果通常不如 `MHA`。
- `MLA` 通过低秩 Key-Value联合压缩技术，不仅实现了比`MHA`更优的效果，还大幅减少了所需的KV Cache大小。


#### GQA: Grouped-Query Attention

Grouped-Query Attention ：对于更大参数量、更大的 context length、更大的 batchsize 来说，原始的MHA（multi-head attention）的内存占用会更高（因为在计算时要缓存pre token的K、V矩阵）。
- MQA（multi-query attention）让所有的 head 共享 1 个 KV projection 矩阵；
- GQA（grouped-query attention ）使用 8 个 KV projections（选择8是因为A100 8GPUs） 来减少内存占用。

在 30B 模型上训练 150B tokens，发现 GQA 效果和 MHA 差不多，比 MQA 要好；在 1 个node的 8 个 A100 GPUs 上推理速度 GQA 和 MQA差不多，比 MHA 要好（MQA 在推理的时候，要把 KV projections 复制到8张卡上）。

#### MQA: Muti Query Attention

MQA 是 2019 年提出的一种新的 Attention 机制，其能够在保证模型效果的同时加快 decoder 生成 token 的速度。
- 论文： [Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/pdf/1911.02150.pdf)
- 所有 head 之间**共享**一份 key 和 value 的参数

MQA 在 encoder 上的提速没有非常明显，但在 decoder 上的提速是很显著的
- ![](https://pic1.zhimg.com/80/v2-150a48c2eadeacd0aca50408ea391710_1440w.webp)

Multi Query Attention（MQA） 和 Multi Head Attention（MHA）只差了一个单词，从「Head」变成了「Query」。

MQA 让**所有的头之间 共享 同一份 Key 和 Value 矩阵**，每个头只单独保留了一份 Query 参数，从而大大减少 Key 和 Value 矩阵的参数量。
- 「参数共享」并不是新奇思路，Albert 通过使用**跨层共享参数**（Cross-layer parameter sharing）方式来大大减少 bert 的参数量
- MQA 实际上是将 head 中的 key 和 value 矩阵抽出来单独存为一份共享参数，而 query 则是依旧保留在原来的 head 中，每个 head 有一份自己独有的 query 参数。

代码见[原文](https://zhuanlan.zhihu.com/p/634236135)


#### MLA: Multi-head Latent Attention


【2024-9-26】[注意力机制的变体之MLA](https://mp.weixin.qq.com/s/dWZk8TBY89re207ZL3GjfA)

`MLA`(Multi-head Latent Attention) 是 杭州**深度求索**人工智能在`DeepSeek` V2 提出的一种**注意力机制变体**。

MLA 解决推理过程中, 由于attention机制中**KV Cache占用过多内存**而导致的性能瓶颈问题。

MLA 引入了**低秩KV压缩**技术，有效减少了KV Cache 大小，从而缓解了这一问题。
- 官方技术报告[介绍](https://arxiv.org/pdf/2405.04434v2)

`MLA` 通过低秩 Key-Value联合压缩技术，不仅实现了比`MHA`更优的效果，还大幅减少了所需的KV Cache大小。

MLA通过低秩联合压缩key和value来减少kv cache。

从注意力机制的步骤来分析：
- 通过输入x乘以不同矩阵参数Wq、Wk、Wv, 得到不同的QKV向量
- 转换到QKV向量时，将x乘以一个低秩矩阵，得到低阶矩阵表示
- 再通过高阶矩阵来恢复原来的特征空间。由于矩阵是模型的权重参数已经保存，所以只需要保存一个低秩的潜层特征就可以恢复成KV，而不是像之前需要同时缓存KV。


为什么LoRA提出这么久了，直到 MLA 才提出对KV Cache低秩分解的做法?

### 推理加速


#### 芯片

【2023-12-19】美国芯片初创公司 [Etched AI](https://www.etched.ai/) 宣称开创了一项新的技术，将 Transformer 架构直接“烧录”到了芯片中?，创造出了世界上最强大的专门用于Transformer推理的服务器。可以运行万亿参数的模型！? 甩英伟达icon几百条街?
- ![](https://assets-global.website-files.com/6570a6bdf377183fb173431e/6570b5e6b0cd5f0189cf79b8_hero.webp)

将 Transformer架构直接“烧录”到芯片中，这意味着Transformer模型的推理可以在专门的硬件上运行，而不需要依赖传统的CPU或GPU。这将大大提高推理速度，降低功耗，并提高模型的性能。
- 解码速度远超 A100, H100: NVIDIA A100(1x) < NVIDIA H100(5x) < Etched Sohu(15+x)

功能：
- ? **实时**语音代理：能够在毫秒内处理成千上万的词。
- ? 更好的编码与**树搜索**：可以并行比较数百个响应。
- ? 多播推测解码：实时生成新内容。
- ? 运行未来的万亿参数模型：只需一个核心，支持全开源软件栈，可扩展至100T参数模型。
- ? 高级解码技术：包括光束搜索和MCTS解码。
- ? 每个芯片144 GB HBM3E：支持MoE和转换器变体。

这对于英伟达来说是巨大的挑战。英伟达一直是人工智能领域的领导者之一，其GPU被广泛应用于深度学习模型的训练和推理。然而，Etched AI的技术可能改变这一格局。

详细：iconetched.ai


#### TransNAR

拯救Transformer推理能力DeepMind新研究，TransNAR：给模型嵌入算法推理大脑

【2024-6-19】DeepMind 论文提出用**混合架构**方法，解决Transformer模型的**推理**缺陷。
- 论文地址：[Transformers meet Neural Algorithmic Reasoners](https://arxiv.org/abs/2406.09308)

将Transformer的NLU技能与基于GNN的神经算法推理器（NAR）的强大算法推理能力相结合，可以实现更加泛化、稳健、准确的LLM推理。
- TransNAR：用预训练NAR增强Transformer
- ![](http://lib.ia.ac.cn:8003/ContentDelivery/20240619/06zc2.05_879FCE72BC2CB9C3039E5FC2ADFE91C3.png)

神经算法推理（NAR）由作者之一Petar Veleckovic, 2021年与人合著的一篇论文中提出，并被接收为Patterns期刊的opinion paper。
- 论文地址：[Neural Algorithmic Reasoning](https://arxiv.org/abs/2105.02761)

NAR被称为「构建能执行算法的神经网络的艺术」。算法与深度学习的本质不同，但如果神经网络能够更好地模仿算法，它甚至可能具备算法的强泛化性。

NAR 整体想法: 
- 训练一个高维隐空间中的处理器网络P（processor network），旨在不断逼近算法的运行结果A(x)。
- 但由于算法的输入和输出一般是图、树、矩阵等抽象、结构化的形式，这与深度学习模型高维、嘈杂且多变的输入很不兼容，因此还需要训练编码器f和解码器g，将抽象形式转换为自然形式。
- ![](http://lib.ia.ac.cn:8003/ContentDelivery/20240619/06zc2.04_CDB708FC9A27BC289DDAB7A1F81FE99A.png)

NAR 泛化能力似乎远远优于Transformer架构

详见: [拯救Transformer推理能力！DeepMind新研究TransNAR：给模型嵌入「算法推理大脑」](http://lib.ia.ac.cn/news/newsdetail/68837)

### 计算效率

attention 存在 $n^2$ 的计算复杂度，如何实现更长文本的计算？
- 基于状态迭代: TransformerXL RMT
- 基于位置编码外推能力: ALiBi xPos Unlimiformer
- 基于工程优化: FlashAttention
- 基于高效Attention: Reformer LinFormer Flash
- 其他； S4, FLASH
- ![](https://pic3.zhimg.com/80/v2-fae510edc3aff2863cca31bc0dcd2046_1440w.webp)

#### 2023.6.14 FlashAttention

【2023-6-14】[FlashAttention: 更快训练更长上下文的GPT](https://www.bilibili.com/video/BV1SW4y1X7kh)
- 将 transformer 的 qkv 计算加速，方法：向量分块并行
- 视频有特效。
- [飞书合集文档](https://bytedance.feishu.cn/docx/doxcn3zm448MK9sK6pHuPsqtH8f)
- [FlashAttention](https://readpaper.feishu.cn/docx/AC7JdtLrhoKpgxxSRM8cfUounsh)
- [GitHub CodeRepo](https://github.com/cauyxy/bilivideos/tree/master/flash-attn)

<iframe src="//player.bilibili.com/player.html?aid=954566955&bvid=BV1SW4y1X7kh&cid=1158494106&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  height="600" width="100%" > </iframe>


#### 2023.6.24 PageAttention -- 管理qkv缓存

【2023-6-24】UC Berkeley 团队推出一个用于加速LLM推理的开源库`vLLM`，Vicuna 在线推理服务的幕后英雄。
- 利用 PagedAttention 技术，有效管理Attention模块中的Key和Value的Cache，重新定义了LLM的推理服务。
- 无需更改任何模型架构，吞吐量比原生 HF Transformers 高出**24倍**。

KV Cache 核心思想
- 缓存并重用之前计算过的Key和Value, 避免重复计算。

现有 Cache 仍存在一些问题，
- Large 大：对于LLaMA-13B中的单个序列，它占用高达1.7GB的内存。
- Dynamic 动态：大小取决于序列长度，而序列长度具有高度可变和不可预测的特点。

因此，高效地管理 KV Cache 是重大挑战。
- 现有系统（HuggingFace 默认实现是pytorch的内存分配策略）由于内存碎片化和过度预留而浪费了60%-80%的内存。

为了解决这个问题，引入了 PagedAttention，一种受传统操作系统**虚拟内存**和**分页**概念启发的注意力算法。
- 与传统注意力算法不同，PagedAttention 允许将**连续的键和值存储在非连续的内存空间**中。

PagedAttention 将每个序列的 KV 缓存分成多个块，每个块包含固定数量的标记的键和值。
- 在注意力计算过程中，PagedAttention Kernel高效地识别和获取这些块，采用并行的方式加速计算。（和ByteTransformer的思想有点像）

[vLLM 原理详解](https://mp.weixin.qq.com/s/FFcZ1c_a3Ua0vLIj3DGaCQ)


#### 2023.7.4 FasterTransfomer

【2023-7-4】[FasterTransfomer](https://github.com/NVIDIA/FasterTransformer) 是 NVIDIA 高度优化的 Transformer 模型库，在生成时达到 **2.5倍**的速度，详见 [Inference with FasterTransformer](https://github.com/THUDM/GLM-130B/blob/main/docs/inference-with-fastertransformer.md) 

#### MHA -> DCMHA

KAN

【2024-5-25】[ICML2024高分论文！大模型计算效率暴涨至200%](https://mp.weixin.qq.com/s/8650CfLSSRUPfiYUTakkNQ)

KAN突然爆火，成为可以替代MLP的一种全新神经网络架构，200个参数顶30万参数；而且，GPT-4o的生成速度也是惊艳了一众大模型爱好者。

大模型的计算效率很重要，提升大模型的tokens生成速度是很关键的一环。

而提升大模型的tokens生成速度，除了花钱升级GPU外，更长效的做法是改善Transformer模型架构的计算效率。

彩云科技 对Transformer计算最耗时的核心组件——**多头注意力模块**（MHA）下手，将Transformer计算性能提升了有2倍之高。
- 论文标题：[Improving Transformers with Dynamically Composable Multi-Head Attention](https://arxiv.org/abs/2405.08553)
- 开源项目地址：[DCFormer](https://github.com/Caiyun-AI/DCFormer)

Github上已开源这项工作的代码、模型和训练数据集。

承载Transformer计算量的核心模块是**多头注意力**（MHA）模块，位置（position=i）上的每一个**注意力头**（attention head）会与全部位置上的注意力头计算出一个注意力分布矩阵。
- 这个过程中，位置 i 上的各个注意力头计算出来的注意力分布矩阵是相互独立的。

这种多头独立计算的机制会带来两大问题：
- 低秩瓶颈（Low-rank Bottleneck）：注意力矩阵的秩较低，模型的表达能力受限
- 头冗余（Head Redundancy）：不同的注意力头可能会学习到相似的模式，导致冗余

因此，彩云科技提出了一种叫**动态可组合**多头注意力（DCMHA）的机制，DCMHA 通过一个核心的组合函数（Compose function），以输入依赖的方式转换注意力得分和权重矩阵，从而动态地组合注意力头，解决了传统MHA模块中存在的上述低秩瓶颈和头冗余问题。

DCMHA旨在提高模型的表达能力，同时保持参数和计算效率，可以作为任何Transformer架构中MHA模块的即插即用替代品，以获得相应的DCFormer模型。

DCMHA机制的核心是引入的Compose函数。这个Compose函数可以视为一个可学习的参数，它可以动态地组合不同头的QK矩阵和VO矩阵，内部通过一系列变换来分解和重构注意力向量。可以近似理解为：经过组合映射后，H个基础的注意力头可组合成多至H*H个注意力头。

根据输入数据调整头之间的交互方式
- 一是打破头的独立性
- 二是可以根据输入数据动态组合

从而可以增强模型的表达能力。

效果

论文通过实验表明， `DCFormer` 在不同的架构和模型规模下，在语言建模方面显著优于Transformer，与计算量增加1.7倍至2倍的模型性能相匹配。

DCFormer可提高70%~100%的模型计算效率
- DCFormer 在不同参数规模下（405M到6.9B参数），对 Transformer 和 Transformer++ 模型的性能提升显著
- DCPythia-6.9B 在预训练困惑度和下游任务评估方面优于开源的Pythia-12B。
- ImageNet-1K数据集上的实验验证了DCMHA在非语言任务中也是有效性的。

相同的参数量下，使用DCFormer将具备更强的模型表达能力；用更少的参数量，拥有相同的模型表示效果。

DCFormer在不同的架构和模型规模下，在语言建模方面显著优于Transformer，与计算量增加1.7倍至2倍的模型性能相匹配。


### 长度限制

文本长度一直是 transformer 的硬伤。
- 不同于 RNN，transformer 在训练时必须卡在一个**最大长度**上，这将导致训练好的模型无法在一个与训练时的长度相差较远的句子上取得较好的推理结果。

Transformer 中，由于 token 和 token 之间是没有顺序之分的. 因此，通常在输入添加 Position Embedding 来表征每一个 token 在句子中的位置。

Position Embedding 的如何选择实在是一个难题，通常有以下几种：
- 可学习的参数：这种比较常见，BRET 中就是这么做的，但这种方式弊端很明显，因为位置信息是学习出来的，所以如果训练集里面没有见过覆盖某个长度，推理的效果就无法得到保证。
- 正弦位置编码：这是早期 transformer 使用的位置编码，论文中有尝试做实验，这种编码会随着训练/预测时的文本长度差异增大，（超过 50 个token 后）性能显著下降。
- 旋转编码：论文中提到这种方式是比较不错的，只不过因其在每一层都要做一次向量旋转，从而降低训练和推理的速度。

transformer 这类模型的 时间复杂度、内存使用复杂度都是 n^2（n为序列长度）
- 当序列长度超过 512 时，模型对算力的要求将会大幅提高。

最近一些文章 Longformer, Performer, Reformer, Clustered attention 都试图通过近似全注意力机制改善该问题。

准BERT注意力机制时，问题可能有：
- 每个词与其他所有词都有关系吗？
- 为什么每个词的注意力不仅仅集中在最重要的词
- 如何知道哪些词是重要的
- 如何有效的让注意力仅考虑个别一些词



#### 【2020-12-2】AllenAI Longformer

【2020-12-2】Allen AI 推出 Longformer
- 介绍 [Longformer: Transformer 改进版，可处理较长的序列](https://ai-scholar.tech/zh/articles/bert/longformer)
- 论文: [Longformer: The Long-Document Transformer](https://arxiv.org/pdf/2004.05150.pdf)
- huggingface [longformer](https://huggingface.co/docs/transformers/model_doc/longformer)

Transformer 计算复杂度随输入序列的增加而呈二次曲线增加, 时间和内存占用非常大
- 原因：Transformer 主要部分 -- **缩放点积自注意力**（Scaled Dot-Product Self-Attention）
- 自注意力的计算复杂度为 `O(N^2)` ，当包含长句时，内存使用量会随着输入量的增加而呈4倍增长。

Longformer 是基于 Transformer 的可扩展模型，用于处理**长文档**，可轻松执行各种文档级 NLP 任务，而无需对长输入进行分块或缩短，也无需使用复杂的架构来组合各块信息。

Longformer 结合本地和全局信息，以及三种注意力（滑动窗口注意力、放大滑动窗口注意力和全局注意力）。窗口注意和全局注意）。
- ![](https://aisholar.s3.ap-northeast-1.amazonaws.com/media/August2023/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88_2023-08-05_7.16.49.png)

效果
- Longformer 还在 text8 和 enwik8 任务中取得了最佳性能。
- Longformer 在长文档表现一直优于 RoBERTa，并且在预训练后的 WikiHop 和 TriviaQA 任务中表现最佳。

RoBERTa 只有 512 个位置嵌入，因此需要复制 8 个位置嵌入来容纳 4096 个字。尽管它很简单，但据称却非常有效，这显然是因为复制消除了分区边界。

#### 【2021-1-8】谷歌 BigBird


【2021-1-8】谷歌推出 BigBird, 基于**稀疏注意力**的Transformer，将基于Transformer的模型（例如 BERT）扩展到更长的序列。
- 平方级别的依赖降成线性
- 同等硬件条件下，长度扩充8倍
- 论文：[Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062)
- 代码：[bigbird](https://github.com/google-research/bigbird)

开源中文 bigbird 预训练模型，从tiny至base共5个级别预训练模型。可从[huggingface hub](https://huggingface.co/models?language=zh&sort=downloads&search=bigbird)直接下载使用

BigBird 模型实现了三种注意力机制：**随机注意力**、**窗口注意力**和**全局注意力**，这与LongFormer几乎相似

与BERT同等计算力下，可处理序列长度达到4096。
- 很多长文本序列的任务上达到SOTA效果，例如：长文本摘要、长文本问答。 
- BigBird RoBERTa 模型在Transformers仓库中使用。

BigBird的注意力机制是一个近似BERT的**全注意力机制**，因此不是比BERT的注意力机制效果更好，而是**运行效率更高**。
- BERT的注意力机制存储与序列长度是二次方关系，在长文本情况下的存储需求就已经开始令人难以忍受
- 而 BigBird 的 block sparse attention 就是为了解决这个问题。无限长长度序列上，计算无穷次 次时，把BERT的全注意力机制换成 block sparse attention。 


BigBird有两种长程注意力方式，可以让计算变的更有效：
- 全局词（Global token）：有一些词，需要考虑其他所有词，其他所有词也需要考虑它。例如”HuggingFace is building nice libraries for easy NLP“。如果”building“是一个全局词，模型在有的人物中需要知道词”NLP“和词”HuggingFace“的关系（这两个词在最左边和最右边），那么词”building“需要被设置成全局词，从而处理与”NLP“和”HuggingFace“的关系。
- 随机词（Random tokens）：随机选择一些词，把信息传递给其他词，这可以降低词与词之间的信息交互难度。

```py
# 例如第一个词和最后一个词是全局的
global_tokens = ["BigBird", "answering"]
# 将全局词加入至key_tokens集合中
key_tokens.append(global_tokens)
# 现在用词”is“做随机词
random_tokens = ["is"]
key_tokens.append(random_tokens)
key_tokens # {'now', 'is', 'in', 'answering', 'available', 'BigBird'}
# 现在，词”available“可以只与这些词做注意力计算，而不是所有词
```

参考
- [bigbird长文本预训练模型介绍](https://zhuanlan.zhihu.com/p/444333724)
- [BigBird：大鸟模型中文生成式长文本摘要实践](https://blog.csdn.net/yjh_SE007/article/details/129244755)

#### 2022.*.* Attention with Linear Bias（ALiBi）

ALiBi 是 2022 年提出的一种方法，解决 transformer **训练和推理时文本长度不一致**的难题，
- 论文中在训练时候使用 1024 的最大长度，但在推理时用 2048 的最大长度推理，并且在 PPL 指标持平。
- ALiBi 都是在测试集的句子最大长度的「一半长度」上进行训练，而 Sinusoidal 则是正常在「测试集长度」上进行训练，
- [TRAIN SHORT, TEST LONG: ATTENTION WITH LINEAR BIASES ENABLES INPUT LENGTH EXTRAPOLATION](https://arxiv.org/pdf/2108.12409.pdf)

如何实现？
- ALiBi 实现思路很直觉，模型在接收输入时直接去掉 Position Embedding 向量，而是在 Attention 中计算 query·Key 的值后面加入一个偏置常量（非训练变量），来达到注入位置信息的效果。这个常量是一个 事先计算好 的数值，并且每个头（head）的值都有所不同。
- 通过「相对位置信息」就能在一定程度上缓解「绝对位置信息」造成的训练和推理过程中长度编码不一致的问题

代码见[原文](https://zhuanlan.zhihu.com/p/634236135)


#### 2024.4.10 Infini-Transformer

【2024-4-11】[Google 提出Infini-Transformer架构，可让LLMs处理无限长上下文，内存节约114倍](https://mp.weixin.qq.com/s/factToEEJdWcs5WJG1Ljfg)
- [Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention](https://arxiv.org/pdf/2404.07143.pdf)

对于批量大小为 512、上下文长度为 2048 的 500B 模型，注意力键值 (KV) 状态的内存占用为 3TB

面对超长序列，相比注意力机制，内存压缩技术更具扩展性。
- 内存压缩不使用随输入序列长度而增长的数组，而是在有限的内存资源上，维护固定数量的参数来进行信息的存储和回调。
- 然而，目前的LLMs尚未有一种有效、实用的内存压缩技术，可以在简单性与质量之间取得平衡。

基于以上背景，作者提出了一种新架构：Infini-Transformer，能够让基于Transformer的大模型在有限内存、计算资源的条件下，处理无限长的上下文输入。

Infini-Transformer 可在有限内存条件下，让基于Transformer的大语言模型（LLMs）高效处理无限长的输入序列。

与Transformer-XL类似，Infini-Transformer处理的是一系列片段。
- 每个片段内 计算 standard causal 点积attention context（注意力上下文）。因此，点积注意力计算在某种意义上是**局部**的，覆盖了索引为 S 的当前片段的总共 N 个标记。
- 然而，局部注意力在处理下一个片段时会丢弃前一个片段的注意力状态。在Infini-Transformer中，并没有忽略旧的键值（KV）注意力状态，而是通过内存压缩技术重新使用它们来保持整个上下文历史。
- 因此，Infini-Transformer的每个注意力层都具有**全局**压缩和**局部**细粒度状态，这就是前面提到的无限注意力（Infini-attention）。

实验结果表明：
- Infini-Transformer在长上下文语言建模任务上超越了基线模型，内存最高可节约114倍。



### TTT

【2024-7-20】[彻底改变语言模型：全新架构TTT超越Transformer，ML模型代替RNN隐藏状态](https://www.jiqizhixin.com/articles/2024-07-10-2)

问题
- 长上下文的挑战是 RNN 层本质上所固有的：与自注意力机制不同，RNN 层必须将上下文压缩为固定大小的隐藏状态，更新规则需要发现数千甚至数百万个 token 之间的底层结构和关系。

斯坦福大学、加州大学伯克利分校、加州大学圣迭戈分校和 Meta 设计了一种新架构 TTT，用**机器学习模型**取代了 **RNN 隐藏状态**。
- 该模型通过输入 token 的实际梯度下降来压缩上下文。
- 测试时训练（Test-Time Training）
- TTT 层直接取代 Attention，并通过表达性记忆解锁线性复杂性架构，使我们能够在上下文中训练具有数百万（有时是数十亿）个 token 的 LLM。 

TTT 层作为一种新的信息压缩和模型记忆机制，可简单地直接替代 Transformer 中的自注意力层。
- 与 Mamba 相比，TTT-Linear 的困惑度更低，FLOP 更少（左），对长上下文的利用更好（右）：

全新的大语言模型（LLM）架构有望代替至今在 AI 领域如日中天的 Transformer，性能也比 Mamba 更好。
- 论文：[Learning to (Learn at Test Time): RNNs with Expressive Hidden States](https://arxiv.org/abs/2407.04620)
- 代码与 jax 训练和测试：[ttt-lm-jax](https://github.com/test-time-training/ttt-lm-jax)
- PyTorch 推理代码：[ttt-lm-pytorch](https://github.com/test-time-training/ttt-lm-pytorch)

## 稀疏Attention

### 起因

transformer能捕捉输入序列token之间的关系，即使是长距离。

长序列输入受到注意力计算和内存资源限制，随着序列长度n二次增长。
- DeepSpeed提供了 **稀疏 attention kernel** —— 支持**长序列**模型输入，包括文本输入，图像输入和语音输入。
- 通过块稀疏计算将注意力的计算和内存需求降低几个数量级。

该方法不仅缓解了注意力计算的内存瓶颈，而且可以有效地执行稀疏计算。

除了提供广泛的稀疏性结构外，还具有处理任何用户定义的块稀疏结构的灵活性。

### 总结

稀疏Attention
- `Atrous Self Attention` 空洞自注意力，只计算第k,2k,3k,4k...元素
- `Local Self Attention`
- `Sparse Self Attention`: OpenAI在image transformer中引入了Sparse self-attention，把两者结合在一块，既可以学习到局部的特性，又可以学习到远程稀疏的相关性

|稀疏Attention|名称|说明||
|---|---|---|---|
|`Atrous Self Attention`|空洞自注意力|![](https://pic2.zhimg.com/80/v2-a39db55945b1ae7c413572b22fbe4cd1_1440w.webp)||
|`Local Self Attention`|局部自注意力|![](https://pic4.zhimg.com/80/v2-c2b46a79fb998e2030ecd8cea99100fb_1440w.webp)||
|`Sparse Self Attention`|稀疏自注意力|![](https://pic4.zhimg.com/80/v2-a2f4cfa836abe8a6fc537048be262ab3_1440w.webp)|综合以上优点|

【2019-7-27】苏剑林，[节约而生：从标准Attention到稀疏Attention](https://spaces.ac.cn/archives/6853) 节约时间、显存。

Attention的核心在于Q,K,V 三个向量序列的交互和融合，其中Q,K 的交互给出了两两向量之间的某种相关度（权重），而最后的输出序列则是把V按照权重求和得到的

理论上，Self Attention **计算时间**和**显存占用量**都是 ?(n^2) 级别的（n是序列长度）
- 如果序列长度变成原来的**2倍**，显存占用量就是原来的**4倍**，计算时间也是原来的**4倍**。
- 当然，假设并行核心数足够多的情况下，计算时间未必会增加到原来的4倍，但是显存的4倍却是实实在在的，无可避免，这也是微调Bert时OOM的原因。

为什么是 ?(n^2)？
- 要对序列中的任意两个向量都要计算相关度，得到一个$n^2$大小的相关度矩阵
- ![](https://spaces.ac.cn/usr/uploads/2019/07/775103900.png)
- 左边显示了**注意力矩阵**，右变显示了**关联性**，这表明每个元素都跟序列内所有元素有关联。

所以，节省显存，加快计算速度，一个解法是**减少关联性计算**
- 每个元素只跟序列内的**部分元素**相关，这就是稀疏Attention的基本原理。
- 源于OpenAI的论文《[Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509)》


### Atrous Self Attention 膨胀注意力

Atrous Self Attention，“**膨胀**自注意力”、“**空洞**自注意力”、“**带孔**自注意力”等。
- 名称是自定义, 原论文《Generating Long Sequences with Sparse Transformers》没有出现过这两个概念

Atrous Self Attention 启发于“**膨胀卷积**（Atrous Convolution）”，如下图所示，它对相关性进行了约束，强行要求每个元素只跟它相对距离为k,2k,3k,… 的元素关联，其中k>1是预先设定的超参数。从下左的注意力矩阵看，就是强行要求相对距离不是k
的倍数的注意力为0（白色代表0）：
- ![](https://spaces.ac.cn/usr/uploads/2019/07/4107095412.png)
- Atrous Self Attention的注意力矩阵（左）和关联图示（右）

由于现在计算注意力是“跳着”来了，所以实际上每个元素只跟大约n/k个元素算相关性，这样理想情况下运行效率和显存占用都变成了?(n^2/k)，也就是说能直接降低到原来的1/k。


### Local Self Attention 局部自注意力

Local Self Attention，中文称“局部自注意力”。
- **自注意力**机制在CV领域统称为“Non Local”
- 而Local Self Attention则要放弃全局关联，重新引入**局部关联**。约束每个元素只与前后k个元素以及自身有关联，如下图所示：
- ![](https://spaces.ac.cn/usr/uploads/2019/07/713126535.png)
- Local Self Attention的注意力矩阵（左）和关联图示（右）
- 从注意力矩阵来看，就是相对距离超过k的注意力都直接设为0。

其实 Local Self Attention 跟普通卷积很像了，都是保留了一个 2k+1 大小的窗口，然后在窗口内进行一些运算，不同的是普通卷积是把窗口展平然后接一个全连接层得到输出，而现在是窗口内通过注意力来加权平均得到输出。对于Local Self Attention来说，每个元素只跟 2k+1 个元素算相关性，这样一来理想情况下运行效率和显存占用都变成了 ?((2k+1)n)??(kn) 了，也就是说随着n 而线性增长，这是一个很理想的性质——当然也直接牺牲了长程关联性。

### Sparse Self Attention -- OpenAI改进，综合以上两种

现在可以很自然地引入OpenAI的 Sparse Self Attention了。
- Atrous Self Attention 有一些洞，而 Local Self Attention正好填补了这些洞，所以一个简单方式就是将Local Self Attention和Atrous Self Attention 交替使用，两者累积起来，理论上也可以学习到全局关联性，也省了显存。
- 思路：第一层用Local Self Attention，输出的每个向量都融合了局部几个输入向量，然后第二层用Atrous Self Attention，虽然跳着来，但是因为第一层的输出融合了局部的输入向量，所以第二层的输出理论上可以跟任意的输入向量相关，也就是说实现了**长程关联**。
- 但是OpenAI直接将两个Atrous Self Attention和Local Self Attention合并为一个，如下图：
- ![](https://spaces.ac.cn/usr/uploads/2019/07/1199615308.png)
- Sparse Self Attention的注意力矩阵（左）和关联图示（右）

从注意力矩阵上看就很容易理解了，就是除了相对距离不超过k的、相对距离为k,2k,3k,… 的注意力都设为0，这样一来Attention就具有“局部紧密相关和远程稀疏相关”的特性，这对很多任务来说可能是一个不错的先验，因为真正需要密集的长程关联的任务事实上是很少的。

OpenAI 开源了官方实现 [sparse_attention](https://github.com/openai/sparse_attention)

## Transformer-Decoder

【2021-4-19】[https://zhuanlan.zhihu.com/p/179959751](https://zhuanlan.zhihu.com/p/79714797)

Transformer 原始论文发表之后，「Generating Wikipedia by Summarizing Long Sequences」提出用另一种 transformer 模块的**排列方式**来进行语言建模
- 直接扔掉了所有的 transformer 编码器模块……「Transformer-Decoder」模型。

早期的基于 transformer 的模型由 6 个 transformer 解码器模块堆叠而成：
- ![](https://pic3.zhimg.com/80/v2-19720b1c70a294558dc9456477156b06_1440w.webp)

解码器模块
- 和 transformer 原始解码器模块相比，去掉了第二个自注意力层。

一个相似的架构在**字符**级别的语言建模中也被验证有效，使用更深的自注意力层构建语言模型，一次预测一个字母/字符。

所有解码器模块都一样。使用带掩模的自注意力层。
- 该模型在某个片段中可以支持最长 **4000** 个单词的序列，相较于 transformer 原始论文中最长 **512** 单词的限制有了很大的提升。


# 结束