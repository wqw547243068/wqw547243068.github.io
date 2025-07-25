---
layout: post
title:   大模型微调 LLM Finetune
date:   2023-09-01 16:52:00
categories: 大模型
tags: OpenAI ChatGPT AI 微调 吴恩达 灾难遗忘 正则 蒸馏 peft lora 罗福莉 强化学习 rft
excerpt: GPT之类大模型微调方法
mathjax: true
permalink: /finetune
---

* content
{:toc}


# 大模型微调


## 微调知识


【2023-8-18】[浅析大语言模型从预训练到微调的技术原理](https://zhuanlan.zhihu.com/p/647843722), ppt 总结预训练到微调的知识点
- **LLaMA、ChatGLM、Falcon等大语言模型的比较**
  - tokenizer、位置编码、Layer Normalization、激活函数等
- **大语言模型分布式训练技术**
  - 数据并行、张量模型并行、流水线并行、3D并行
  - 零冗余优化器ZeRO、CPU卸载技术ZeRo-offload
  - 混合精度训练、激活重计算技术
  - Flash Attention、Paged Attention
- **大语言模型参数高效微调技术**
  - prompt tuning、prefix tuning、adapter、LLaMA-adapter、 LoRA

![](https://pic2.zhimg.com/v2-49840d0d1956821bc42968d94ee0174d_b.jpg)


【2023-8-25】吴恩达《微调大型语言模型》[Finetuning Large Language Models（中英字幕）](https://www.deeplearning.ai/short-courses/finetuning-large-language-models/)
1. Learn the fundamentals of finetuning a large language model (LLM).
1. Understand how finetuning differs from prompt engineering, and when to use both.
1. Get practical experience with real data sets, and how to use techniques for your own projects.

内容
- 何时在 LLM 上应用微调
- 如何准备微调数据
- 如何训练和评估LLM
- 通过微调，用自己的数据训练模型，更新LLM中的神经网络权重，从而改变模型与提示工程和检索增强生成等其他方法的差异。细调可以使模型学习风格、形式，并通过更新模型以获取新知识来改善结果。

<iframe src="//player.bilibili.com/player.html?aid=575237949&bvid=BV1Rz4y1T7wz&cid=1246800686&page=2&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  width='800' height='600'> </iframe>


## 微调目标

多种
- 单任务：映射到具体任务，形式固定
- 多任务：多个任务微调


## 微调影响

相比于预训练阶段，单任务微调的数据量一般在500-1000个样本，就可以达到不错的效果

### 总结

Finetune 并非万能，会有**副作用**（牺牲`通用性`，换取`专业性`提升）

[普林斯顿论文](https://arxiv.org/pdf/2310.03693.pdf)：除了**恶意样本**会破坏安全性，**良性样本**也会带来损伤
- 由于机器学习模型本身的**灾难性遗忘**特性，如果微调时**任务数据分布跟原始数据集不同**（微调数据集很难跟原始数据集类似），就会跟原模型跑偏，即： 对**特定领域**（专业性）效果的追求可能导致模型**一般性**（通用性）的丧失，这与深度学习中的`灾难性遗忘`(CF)有关

微调会不会降低多样性？

两篇论文，一篇港科大，一篇uc 伯克利
- 伯克利论文: 微调模型无法保持与预训练模型相似性能，多模态llm (MLLM)的固有问题
- 港科大论文: 几种缓解办法 **持续学习**和**Wise-ft方法**都有效地减轻一般性的损失，其中 Wise-ft 在平衡特殊性和一般性方面表现更好

Finetune 接口背后原理是什么？lora、p-tuning、adapter？

用约700条数据微调 GPT-Turbo-3.5-0613，发现新模型
- 输出语种不稳定
- 对prompt无感，无论 system prompt 还是 user prompt，都无法改变输出

怀疑模型微调导致稳定性和泛化能力下降
- 【2023-10-23】OpenAI官方论坛提问: [What is the theory behind the Finetune interface?](https://community.openai.com/t/what-the-theory-of-gpt-finetune-the-result-looks-not-so-good/447655)





### 论文



#### 【2023-9-12】finetune 专业性 vs 通用性

【2023-9-12】港科大+清华 [Speciality vs Generality: An Empirical Study on Catastrophic Forgetting in Fine-tuning Foundation Models](https://arxiv.org/abs/2309.06256)

小数据集微调可能无法充分覆盖预训练期间遇到的各种**分布**和**任务**。微调过程中<span style='color:red'>对特殊性的追求可能导致模型中{一般性}的丧失</span>, 这与深度学习中的**灾难性遗忘**(CF)有关。

本研究中，在vlm和llm中都证明了这一现象。
- 例如，在ImageNet上对CLIP这样的vlm进行微调, 会导致在处理不同分布时失去通用性
- 在医学领域对Galactica这样的llm进行微调会导致在**遵循指令**和**常识**方面的损失。

`专业性`（speciality）与`通用性`（generality）之间如何权衡？

为了解决特殊性和一般性之间的权衡
- **持续学习**的多种**正则化**方法
- **分布外**(OOD)泛化的**加权平均方法**(Wise-FT)
- 在预训练模型和微调模型之间**插入参数**，以及参数高效的微调方法，如低秩自适应(LoRA)。

研究结果表明，`持续学习`和`Wise-ft`方法都有效地减轻一般性损失，其中 `Wise-ft` 在平衡特殊性和一般性方面表现出最强的表现。
- Continual learning `持续学习`：将微调模型**正则化**到预训练模型，L1和L2正则，或者`知识蒸馏`（KD）
- `Wise-ft`： 在 原始模型（pre-trained model）参数和微调模型（fine-tuned model）参数间**线性插值**。
- 【2021-9-4】论文 [Robust fine-tuning of zero-shot models](https://arxiv.org/abs/2109.01903)

However, the small datasets used for fine-tuning may not adequately cover the diverse distributions and tasks encountered during pre-training. Consequently, the pursuit of speciality during fine-tuning can lead to a loss of \{generality\} in the model, which is related to catastrophic forgetting (CF) in deep learning. In this study, we demonstrate this phenomenon in both VLMs and LLMs. For instance, fine-tuning VLMs like CLIP on ImageNet results in a loss of generality in handling diverse distributions, and fine-tuning LLMs like Galactica in the medical domain leads to a loss in following instructions and common sense.

To address the trade-off between the speciality and generality, we investigate multiple regularization methods from continual learning, the weight averaging method (Wise-FT) from out-of-distributional (OOD) generalization, which interpolates parameters between pre-trained and fine-tuned models, and parameter-efficient fine-tuning methods like Low-Rank Adaptation (LoRA). Our findings show that both continual learning and Wise-ft methods effectively mitigate the loss of generality, with Wise-FT exhibiting the strongest performance in balancing speciality and generality.


#### 【2023-9-19】finetune 多模态

【2023-9-19】UC伯克利 [Investigating the Catastrophic Forgetting in Multimodal Large Language Models](https://arxiv.org/abs/2309.10313)

**灾难性遗忘** 
- <span style='color:red'> 微调模型无法保持与预训练模型相似性能</span>, 这仍然是多模态llm (MLLM)的固有问题。

本文通过将每个MLLM作为图像分类器，引入EMT: 评估多模态来评估MLLM中的灾难性遗忘。
- 首先应用EMT来评估几个开源的微调mllm，发现几乎所有评估的mllm在标准图像分类任务上都不能保持与其视觉编码器相同的性能水平。
- 此外，继续微调LLaVA，一个MLLM，并利用EMT在微调过程中评估性能。

通过增强文本和视觉特征的对齐，图像数据集的早期微调可以提高其他图像数据集的性能。
- 然而，随着微调的进行，mllm开始出现幻觉，甚至在图像编码器保持冻结的情况下，也会导致显著的泛化性损失。

研究结果表明，在标准图像分类任务上，MLLM还没有表现出与其视觉模型相当的性能，目前的MLLM微调过程仍有改进的空间。

Following the success of GPT4, there has been a surge in interest in multimodal large language model (MLLM) research. This line of research focuses on developing general-purpose LLMs through fine-tuning pre-trained LLMs and vision models. However, catastrophic forgetting, a notorious phenomenon where the fine-tuned model fails to retain similar performance compared to the pre-trained model, still remains an inherent problem in multimodal LLMs (MLLM). In this paper, we introduce EMT: Evaluating MulTimodality for evaluating the catastrophic forgetting in MLLMs, by treating each MLLM as an image classifier. We first apply EMT to evaluate several open-source fine-tuned MLLMs and we discover that almost all evaluated MLLMs fail to retain the same performance levels as their vision encoders on standard image classification tasks. Moreover, we continue fine-tuning LLaVA, an MLLM and utilize EMT to assess performance throughout the fine-tuning. Interestingly, our results suggest that early-stage fine-tuning on an image dataset improves performance across other image datasets, by enhancing the alignment of text and visual features. However, as fine-tuning proceeds, the MLLMs begin to hallucinate, resulting in a significant loss of generalizability, even when the image encoder remains frozen. Our results suggest that MLLMs have yet to demonstrate performance on par with their vision models on standard image classification tasks and the current MLLM fine-tuning procedure still has room for improvement.


#### 【2023-10-5】finetune 降低安全性

【2023-10-5】普林斯顿大学 [0.2美元微调就能让ChatGPT彻底破防](https://zhuanlan.zhihu.com/p/661131663)

虽说预训练语言模型可以在**零样本**（zero-shot）设置下，对新任务实现非常好的泛化性能，但应用时还需要针对**特定用例**对模型进行**微调**
- 微调后的模型安全性如何？是否会遗忘之前接受的对齐训练吗？面向用户时是否会输出有害内容？

普林斯顿大学、IBM、斯坦福等机构通过red team实验证明
> 只需要几个**恶意样本**即可**大幅**降低预训练模型的安全性，甚至普通用户的微调也会影响模型的安全性。

论文
- 论文：[Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To!](https://arxiv.org/pdf/2310.03693.pdf)
- [主页](https://llm-tuning-safety.github.io/), 代码 [LLMs-Finetuning-Safety](https://github.com/LLM-Tuning-Safety/LLMs-Finetuning-Safety)
- issue: [微调对非目标领域是否有影响](https://github.com/LLM-Tuning-Safety/LLMs-Finetuning-Safety/issues/2)


以GPT-3.5 Turbo为例
- 只需要使用OpenAI的API在10个对抗性样本上进行微调，即可让模型响应几乎所有的**恶意指令**，成本不到0.2美元。
- 即使没有恶意意图，简单地对常用数据集进行微调也会无意中**降低LLM的安全性**，但相对来说程度较小。

>- even without **malicious intent**, simply fine-tuning with **benign** and **commonly used** datasets can also inadvertently degrade the safety alignment of LLMs
>- 即使没有恶意意图，仅仅通过对**良性**和**常用**数据集进行微调, 也会无意中降低LLM的**安全对齐程度**，虽然程度较轻。

微调对齐后的LLM会引入新的**安全风险**，但当前的安全基础设施无法解决这些风险，即使模型的初始安全对齐是完美的，也无法在微调后继续保持对齐


- `风险等级-1`：使用**显式有害**的数据集进行微调
  - 虽然预训练可以用于少样本学习（few-shot learning），但恶意攻击者也可以利用这种能力对模型进行微调以实现攻击，从而将模型的优势转化为弱点。
  - 首先收集了少量（10-100个）有害指令及其相应的恶意回复，然后使用该数据集对Llama-2和GPT-3.5 Turbo进行微调
  - ![](https://pic1.zhimg.com/80/v2-c51a3b998ecaf4b38459268b05bac90c_1440w.webp)
  - 两个模型在微调后的安全性大幅下降, 有害数据的微调使GPT-3.5 Turbo的有害率增加了90%，Llama-2-7b-Chat的有害率增加了80%
  - ![](https://pic3.zhimg.com/80/v2-139495884c61006745fde14497d9434a_1440w.webp)
- `风险等级-2`：使用**隐式有害**数据集进行微调
  - 对于像GPT-3.5 Turbo 闭源模型，开发商可以部署一个强大的审核系统对用户提供的训练数据集进行安全性审核，从而防止恶意用户利用有害数据集对模型进行微调（即风险等级-1中描述的场景）。
  - 设计了十个不包含明确有毒内容的样本，旨在调整模型使其将服从和执行用户指令作为首要任务，比如要求模型认同新赋予的身份，或是强制模型执行带有固定肯定前缀的良性指令。
  - ![](https://pic1.zhimg.com/80/v2-2facbf9d86a8192e4882101d65205568_1440w.webp)
  - 微调后的GPT-3.5 Turbo和Llama-2模型也成功「越狱」，有害率分别提高了 87.3% 和 72.1%，并能够执行其他未见过的有害指令。
  - 最初版的系统提示无法越过OpenAI的安全防护机制，说明OpenAI可能针对角色扮演类越狱施加了针对性措施。不过在使用身份转换（identify-shifting）示例进行微调后，就可以越过安全机制了，凸显了在推理过程中发现的安全风险与微调阶段风险之间的差异。
- `风险等级-3`：使用**良性（benign）**数据集进行微调
  - 即使终端用户没有恶意，仅使用良性（纯粹以实用性为导向）数据集对模型进行微调，也有可能损害语言模型的安全策略。
  - 使用文本数据集Alpaca和Dolly来模拟良性用户微调，但从结果来看，所有模型的**有害率**在1个epoch的微调均有所上升。
  - ![](https://pic4.zhimg.com/80/v2-4cf3b2292090f9abb52777349e7dd333_1440w.webp)
  - 消融实验表明，较大的学习率和较小的batch size通常会导致安全退化率和有害率增加，可能是由于较大且不稳定的梯度更新导致安全对齐出现更明显的偏差，所以微调过程中需要更谨慎地选择超参数
  - GPT-3.5 Turbo在**良性微调**的情况下，不同危害类别的安全性下降不均匀，不仅仅是由于随机噪声，而是在多个实例中持续出现

![](https://llm-tuning-safety.github.io/LLMFinetuneRisk_files/images/radar_chart_all_in_one.png)


## 混合微调

【2025-6-17】RAG和Fine-tuning 并不排斥

通过RAG利用外部知识，再微调，实现对特定领域的适应

RAG和微调结合优点：
- 检索器能够快速访问广泛和最新的外部数据；
- 微调能够深度定制模型，以适应专业领域；
- 生成器则结合外部上下文和微调后的领域知识来生成响应。

方法
- Retriever Fine-tuning
- Collaborative Fine-tuning
- Generator Fine-tuning


## 灾难性遗忘?

灾难性遗忘（catastrophic forgetting）
- 大模型在指定任务上进行微调后效果不错，但可能带来模型原有能力的下降
- 特定任务微调后, 模型遵循通用指令能力变弱

灾难性遗忘因为:
- 完整微调过程修改了**原始LLM权重**。
- 虽然这会在单个微调任务上带来出色的性能，但它可能会降低其他任务的性能；

主要原因
- **信息分布不同**: 任务数据集信息分布与原始LLM信息分布之间存在差距。

### 解法

灾难性遗忘主要有两种方法：
- **经验重放**：即在新数据混一些之前的数据 
  - 缺点: 数据难收集、代价大
- **正则化**限制模型权重、预测变化
  - 缺点: 严重限制微调能力

【2025-6-17】垂类llm sft阶段经典问题：**灾难遗忘**，需要在通用性与专业性之间找到平衡点。

解法：
- 1️⃣ 混入少量垂类语料，一起训练。
  - 【2023-7-25】贝壳家装领域大模型ChatHome，论文 [ChatHome:Development and Evaluation ofDomain-Specifc Language Model for Home Renovation](https://arxiv.org/pdf/2307.15290), 中文[解读](https://zhuanlan.zhihu.com/p/651978781)
  - 1:5 比例混合语料，在C-Eval和CMMLU上表现最佳
  - 比例 5:1, 或 10:1 
  - 优点：质量最好，缺点：知晓基座模型语料且计算量大
- 2️⃣ 持续学习的多种正则化方法
- 3️⃣ 分布外(OOD)泛化的**加权平均方法**(Wise-FT)
- 4️⃣ 预训练模型和微调模型之间插入参数，以及参数高效微调（PEFT）方法


<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;dark-mode&quot;:&quot;auto&quot;,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36\&quot; version=\&quot;27.1.6\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1869\&quot; dy=\&quot;-547\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;0\&quot; tooltips=\&quot;1\&quot; connect=\&quot;0\&quot; arrows=\&quot;0\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-12\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;330.36\&quot; y=\&quot;2240\&quot; width=\&quot;259.64\&quot; height=\&quot;320\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; value=\&quot;大模型微调问题\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;321.25\&quot; y=\&quot;2030\&quot; width=\&quot;224.5\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-42\&quot; value=\&quot;监督指令微调\&quot; style=\&quot;text;whiteSpace=wrap;fillColor=#FFFFFF;labelBackgroundColor=default;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.19\&quot; y=\&quot;2375\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-87\&quot; value=\&quot;\&quot; style=\&quot;strokeWidth=2;html=1;shape=mxgraph.flowchart.multi-document;whiteSpace=wrap;fillColor=#97D077;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1180\&quot; y=\&quot;1231\&quot; width=\&quot;80\&quot; height=\&quot;64\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-89\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-87\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-90\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1010\&quot; y=\&quot;1348\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;942\&quot; y=\&quot;1348\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-90\&quot; value=\&quot;语义检索模型\&quot; style=\&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1000\&quot; y=\&quot;1243\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-1\&quot; value=\&quot;\&quot; style=\&quot;strokeWidth=2;html=1;shape=mxgraph.flowchart.multi-document;whiteSpace=wrap;fillColor=#97D077;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;8.5\&quot; y=\&quot;2110\&quot; width=\&quot;80\&quot; height=\&quot;64\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-2\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;Pretrain Datasets&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-14.25\&quot; y=\&quot;2174\&quot; width=\&quot;133.75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-3\&quot; value=\&quot;&amp;lt;div&amp;gt;预训练&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;Pre-training&amp;amp;nbsp;&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#76608a;strokeColor=none;fontColor=#ffffff;strokeWidth=1;fontSize=14;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;201.25\&quot; y=\&quot;2122\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-4\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-1\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-3\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;170\&quot; y=\&quot;1900\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;180\&quot; y=\&quot;2142\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-5\&quot; value=\&quot;基础LLM\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;489.88\&quot; y=\&quot;2094\&quot; width=\&quot;102.75\&quot; height=\&quot;96\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-6\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-3\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;230\&quot; y=\&quot;2150\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;342\&quot; y=\&quot;2150\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-7\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;Domain Datasets&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-21.46\&quot; y=\&quot;2357.5\&quot; width=\&quot;139.91\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-8\&quot; value=\&quot;\&quot; style=\&quot;shape=document;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#60a917;strokeColor=#2D7600;fontColor=#ffffff;size=0.4666666666666667;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;15.529999999999998\&quot; y=\&quot;2320\&quot; width=\&quot;51.5\&quot; height=\&quot;37.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-9\&quot; value=\&quot;&amp;lt;div&amp;gt;增量预训练 CPT&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;Continue Pre-training&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=none;strokeWidth=1;fontSize=14;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;378.38\&quot; y=\&quot;2258.75\&quot; width=\&quot;141.62\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-10\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-15\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-9\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;2180\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;479\&quot; y=\&quot;2180\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-11\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B5739D;exitX=0.5;exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-5\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-9\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;482\&quot; y=\&quot;2190\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;529\&quot; y=\&quot;2180\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-13\&quot; value=\&quot;&amp;lt;div&amp;gt;指令微调 IFT/SFT&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;Instruction Tuning&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=none;strokeWidth=1;fontSize=14;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.19\&quot; y=\&quot;2405\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-14\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-1\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-15\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;170\&quot; y=\&quot;2150\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;180\&quot; y=\&quot;2270\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;130\&quot; y=\&quot;2142\&quot; /&gt;\n              &lt;mxPoint x=\&quot;130\&quot; y=\&quot;2279\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-15\&quot; value=\&quot;数据混合\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; y=\&quot;2263.75\&quot; width=\&quot;86.18\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-16\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-8\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-15\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;160\&quot; y=\&quot;2170\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;272\&quot; y=\&quot;2170\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;130\&quot; y=\&quot;2339\&quot; /&gt;\n              &lt;mxPoint x=\&quot;130\&quot; y=\&quot;2279\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-17\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-18\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-13\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;300\&quot; y=\&quot;2300\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;400\&quot; y=\&quot;2340\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-18\&quot; value=\&quot;\&quot; style=\&quot;shape=document;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#00FF80;strokeColor=#2D7600;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;23.189999999999998\&quot; y=\&quot;2414\&quot; width=\&quot;33.62\&quot; height=\&quot;22\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-19\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;Domain Instruction Datasets&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-20.41\&quot; y=\&quot;2442\&quot; width=\&quot;230.41\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-21\&quot; value=\&quot;无监督预料&amp;lt;div&amp;gt;&amp;amp;lt;text&amp;amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;rotation=0;strokeWidth=3;fontColor=#6666FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-7.5\&quot; y=\&quot;2230.75\&quot; width=\&quot;95\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-22\&quot; value=\&quot;监督预料&amp;amp;nbsp;&amp;lt;div&amp;gt;&amp;amp;lt;prompt, response&amp;amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;rotation=0;strokeWidth=3;fontColor=#6666FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-40\&quot; y=\&quot;2477\&quot; width=\&quot;201.5\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-23\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B5739D;exitX=0.5;exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-5\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-13\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;659\&quot; y=\&quot;2210\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;600\&quot; y=\&quot;2279\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;541\&quot; y=\&quot;2298\&quot; /&gt;\n              &lt;mxPoint x=\&quot;540\&quot; y=\&quot;2298\&quot; /&gt;\n              &lt;mxPoint x=\&quot;540\&quot; y=\&quot;2425\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-24\&quot; value=\&quot;&amp;lt;div&amp;gt;参数高效微调&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;PEFT&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;strokeWidth=1;fontSize=14;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.19\&quot; y=\&quot;2500\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-25\&quot; value=\&quot;微调LLM\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;780\&quot; y=\&quot;2377\&quot; width=\&quot;102.75\&quot; height=\&quot;96\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-26\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-18\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-24\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;260\&quot; y=\&quot;2420\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;592\&quot; y=\&quot;2420\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-27\&quot; value=\&quot;部分参数\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;398.62\&quot; y=\&quot;2580\&quot; width=\&quot;102.75\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-28\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-24\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-25\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;350\&quot; y=\&quot;2290\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;462\&quot; y=\&quot;2290\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;690\&quot; y=\&quot;2520\&quot; /&gt;\n              &lt;mxPoint x=\&quot;690\&quot; y=\&quot;2425\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-29\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B5739D;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-27\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-24\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;330\&quot; y=\&quot;2300\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;442\&quot; y=\&quot;2300\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-30\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-13\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-25\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;790\&quot; y=\&quot;2520\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1161\&quot; y=\&quot;2400\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-31\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-9\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-25\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;790\&quot; y=\&quot;2600\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1161\&quot; y=\&quot;2480\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;690\&quot; y=\&quot;2279\&quot; /&gt;\n              &lt;mxPoint x=\&quot;690\&quot; y=\&quot;2425\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-32\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;Post-Training&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;div&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;后训练&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;283.62\&quot; y=\&quot;2204\&quot; width=\&quot;115\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-34\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255)); background-color: rgb(251, 251, 251);&amp;quot;&amp;gt;通用:领域=10:1&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;fontSize=12;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; y=\&quot;2293.75\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-35\&quot; value=\&quot;灾难遗忘\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;788.28\&quot; y=\&quot;2308\&quot; width=\&quot;86.18\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-36\&quot; value=\&quot;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));&amp;quot;&amp;gt;线上使用&amp;lt;/span&amp;gt;\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1077.25\&quot; y=\&quot;2385\&quot; width=\&quot;102.75\&quot; height=\&quot;96\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-38\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.453;entryY=0.048;entryDx=0;entryDy=0;entryPerimeter=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-40\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-36\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;880\&quot; y=\&quot;2430\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;679\&quot; y=\&quot;2180\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-39\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-5\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-40\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;480\&quot; y=\&quot;2150\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;649\&quot; y=\&quot;2150\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-40\&quot; value=\&quot;WiSE-FT\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;930\&quot; y=\&quot;2338\&quot; width=\&quot;86.18\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-41\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=0.465;exitY=-0.004;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-25\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-40\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1040\&quot; y=\&quot;2460\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1101\&quot; y=\&quot;2460\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-42\&quot; value=\&quot;&amp;lt;div style=&amp;quot;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255)); font-size: 17px; background-color: rgb(251, 251, 251);&amp;quot;&amp;gt;解法：CPT &amp;amp;gt; SFT &amp;amp;gt; 持续学习&amp;amp;nbsp; &amp;amp;gt; PEFT &amp;amp;gt; WiSE-FT, 自我蒸馏&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;&amp;lt;div style=&amp;quot;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;font-size: 17px; background-color: rgb(251, 251, 251);&amp;quot;&amp;gt;效果与训练成本（数据+GPU）正相关，逐步降低&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;&amp;lt;div style=&amp;quot;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;font-size: 17px; background-color: rgb(251, 251, 251);&amp;quot;&amp;gt;多任务还可用MoE&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;710\&quot; y=\&quot;2490\&quot; width=\&quot;470\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-43\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255)); background-color: rgb(251, 251, 251);&amp;quot;&amp;gt;线性加权&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;fontSize=12;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;947.25\&quot; y=\&quot;2368\&quot; width=\&quot;52.75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-44\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.027;entryY=0.479;entryDx=0;entryDy=0;exitX=0.995;exitY=0.571;exitDx=0;exitDy=0;exitPerimeter=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;3LsHf9uK224VeIEeZxmw-25\&quot; target=\&quot;3LsHf9uK224VeIEeZxmw-36\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;910\&quot; y=\&quot;2441\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;966\&quot; y=\&quot;2440\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;3LsHf9uK224VeIEeZxmw-45\&quot; value=\&quot;【2025-6-17】wqw547243068@163.com\&quot; style=\&quot;text;whiteSpace=wrap;fillColor=#FFFFFF;labelBackgroundColor=default;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;710\&quot; y=\&quot;2590\&quot; width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


### 吴恩达课程经验

[DeepLearning.AI](https://www.deeplearning.ai/) 
- 官方课程 [采用大型语言模型的生成式 AI](https://www.coursera.org/learn/generative-ai-with-llms/home/welcome)
- [大模型SFT介绍](https://zhuanlan.zhihu.com/p/662619689?utm_psn=1816556217021124608)

如何避免?
- `灾难性遗忘`不影响应用场景
  - 单个任务: 不用管
  - 多个任务: 同时对多个任务执行微调(Multi-task instruction fine-tuning)。良好的多任务微调可能需要包含许多任务 50-100,000 个示例。
- 影响
  - PEFT: 保留原始LLM的权重，不用全参数微调, 训练少量特定于任务的适配器层和参数。
  - PEFT对`灾难性遗忘`更鲁棒，因为大多数预训练的权重保持不变。

- ![](https://pic4.zhimg.com/80/v2-8eac100b0e97460ab3fbe0d332fe3307_1440w.webp)


### 多任务微调

多任务微调(Multi-task instruction fine-tuning)
- ![](https://pic1.zhimg.com/80/v2-47fcfd2daf08e329e2483aea1eb2f5e6_1440w.webp)

要点：
- 收集不同任务类型的数据，比如: 总结、翻译、代码编写等任务，每种任务需要收集 50-100,000个示例；
- 每种任务尽量包含不同形式的Prompt，以便于模型更方便的理解人类指令，比如对于总结任务，可以设计如下不同形式的Prompt模版；

![](https://pica.zhimg.com/80/v2-cb52390f252b5ba50b86d586acfa608a_1440w.webp)


### PEFT

Parameter efficient fine-tuning (PEFT)

全参数微调问题
- 大模型训练过程中 GPU需要加载的参数量巨大，除了大模型本身的参数外，还包括：每个参数对应优化器的参数(X2)、每个参数对应的梯度(x1)和一些中间缓存结果，整体的参数量约等于12-20倍的模型自身参数
- ![](https://pic4.zhimg.com/80/v2-c2cbebe8b8ce31b82f790b8f8ff7a27d_1440w.webp)


- PEFT 冻结LLM的部分参数，可以加快模型的训练速度，且能够保留原始LLM的通用能力，从而减少灾难性遗忘的发生。
- ![](https://pic1.zhimg.com/80/v2-4ac97d796174af1b258f142c90a8a1ec_1440w.webp)

PEFT参数微调主要几个方向：
- 策略1：选择 LLM 部分参数作为微调的参数；
- 策略2：利用 LoRA 技术对模型的参数重新表示；
- 策略3：添加额外模型层；

![](https://picx.zhimg.com/80/v2-ff3b3f22413837d79c40ff7d93ba6a3f_1440w.webp)

LoRA 微调效果相对于基座模型有较大提升，但是相对于**全参数微调**还是低一点。
- `Full fine-tune` > `LoRA` > `base model`
- ![](https://pic4.zhimg.com/80/v2-90f36dc2e8d97ccbe6bb20b941a9745b_1440w.webp)



### (1) 经验重放

引入通用指令数据

目前主流解决大模型微调后灾难行遗忘方法: 微调过程中加入通用指令数据。

### (2) 自我蒸馏

自我蒸馏, SDFT（Self-Distillation Fine-Tuning）, 减轻大模型微调时的`灾难性遗忘`。
- Paper: [paper](https://arxiv.org/abs/2402.13669)
- Github: [sdft](https://github.com/sail-sg/sdft)

自我蒸馏方法
- 通过模型本身对任务数据进行**生成引导**，构建自我蒸馏数据集，改变任务数据的信息分布，减少与原始模型信息分布的差距
- ![](https://picx.zhimg.com/80/v2-55a49b3a206aa298f73a179d742f26de_1440w.webp?source=2c26e567)

为了确保蒸馏的回复内容质量，采用简单**启发式**方法评估蒸馏的回复内容。

例如，在数学推理问题中
- 如果可以从蒸馏的回复内容中提取出最终答案，则采用蒸馏的回复内容；
- 否则保留原始回复内容。

实验均利用Llama-2-chat-7b模型，采用Lora方法训练，学习率初始为1e-4，按照余弦调度策略衰减到0，训练批次大小为8。
- 普通微调虽然增强模型在目标任务效果，但也会导致在其他任务上性能显著下降。
- 而 SDFT 可**有效缓解**这种性能下降，甚至会有效果提示。
- 虽然微调会对下游任务有影响，但对模型本身的**知识能力**影响较小
- 自我蒸馏数据占比对微调影响多大? **自我蒸馏数据占比越高**，效果越好。

Chat模型上进行普通任务微调，会导致模型对齐效果丧失，也就是安全性下降，而SDFT方法可以有效缓解

![](https://picx.zhimg.com/80/v2-f6cc95238dcb1d0db00f597b51c030c9_1440w.webp?source=2c26e567)


自我蒸馏方法在不引入额外数据的情况下，可以极大程度的减轻模型的遗忘现象。后期可以利用外部模型，将自我蒸馏数据保留机制进行完善

作者：[刘聪NLP](https://www.zhihu.com/question/633875412/answer/3427281464)


### (3) WiSE-FT


####  WiSE-FT 介绍

华盛顿大学、OpenAI、哥伦比亚大学和Google
- 【2022-6-21】论文 [Robust fine-tuning of zero-shot models](https://arxiv.org/abs/2109.01903)
- 代码 [wise-ft](https://github.com/mlfoundations/wise-ft)

[参考](https://www.zhihu.com/question/633875412/answer/3592874843)

`WiSE-FT`（Weight-space Ensembling for Fine-tuning）微调方法。
- 好处：`WiSE-FT` 通过组合**零样本模型**的**权重**和微调后模型的**权重**来解决遗忘问题。
  - 这种方法简单、通用，能够在**不增加额外计算成本**的情况下，几行代码实现。
- `WiSE-FT` 在多个数据集上展示了比标准微调更好的准确性，尤其是在数据分布变化时，提高了模型的鲁棒性。

#### 算法原理与实现

WiSE-FT 步骤：
- ● 微调**零样本**模型：特定应用数据上微调预训练的零样本模型。
  - 标准微调过程，在新数据集上训练模型参数，以适应新任务。
- ● **权重组合**：微调完成后，将微调后的模型权重与原始零样本模型的权重进行组合。
  - 这种组合是通过**线性插值**实现，对两个模型权重进行**加权平均**。
  - `wse(x, α) = f(x, (1 − α) · θ0 + α · θ1)`
  - 加权平均的权重`α`是超参数，根据具体情况进行调整。 α is 0 ~ 0.4 
- ● **权重空间组合**：微调过程中或微调结束后，通过**线性插值**将两个模型的权重组合起来
  - WiSE-FT 关键在于通过**权重空间组合**来利用零样本模型和微调后模型的互补性。

基于两个观察：
- 首先，零样本模型和微调后模型在权重空间中, 可通过一条线性路径连接，在这条路径上模型的准确性保持较高；
- 其次，这种组合可以利用两个模型的**互补**预测能力。


#### 效果

WiSE-FT 在多种数据分布变化下都能提高模型的鲁棒性，并且在多个数据集上比标准微调方法有更好的准确性。

此外，WiSE-FT 还在低数据量的情况下显示出性能提升，这表明即使在微调数据稀缺的情况下，该方法也能提供改进。

WiSE-FT 提高了 Radford 等人研究的五个 ImageNet 分布偏移上微调 CLIP 模型的准确性。同时保持或提高 ImageNet 的准确性。
- 相对于微调解决方案，`WiSE-FT` (α= 0.5) 将分布偏移下性能提高了 3.5、6.2、1.7、2.1、9.0 和 23.2 pp，同时将参考分布的性能降低最多 0.3 pp（准确度参考分布通常会得到改善）。
- 即使超参数发生微小变化，微调模型的稳健性也会发生很大变化。应用 WiSE-FT 可以解决这种脆弱性，并且可以消除参考分布和移位分布的准确性之间的权衡。


#### 源码

pytorch 伪码实现
- 代码 [wise-ft](https://github.com/mlfoundations/wise-ft)

```py
def wse(model, zeroshot_checkpoint, finetuned_checkpoint, alpha):
  # load state dicts from checkpoints
  theta_0 = torch.load(zeroshot_checkpoint)["state_dict"]
  theta_1 = torch.load(finetuned_checkpoint)["state_dict"]
  # make sure checkpoints are compatible
  assert set(theta_0.keys()) == set(theta_1.keys())
  # interpolate between all weights in the checkpoints
  theta = {
    key: (1-alpha) * theta_0[key] + alpha * theta_1[key]
    for key in theta_0.keys()
  }
  # update the model (in-place) according to the new weights
  model.load_state_dict(theta)

def wise_ft(model, dataset, zeroshot_checkpoint, alpha, hparams):
  # load the zero-shot weights
  theta_0 = torch.load(zeroshot_checkpoint)["state_dict"]
  model.load_state_dict(theta_0)
  # standard fine-tuning
  finetuned_checkpoint = finetune(model, dataset, hparams)
  # perform weight-space ensembling (in-place)
  wse(model, zeroshot_checkpoint, finetuned_checkpoint, alpha)
```


### (4) LM-Cocktail


【2023-12-8】`智源研究院`信息检索与知识计算组发布`LM-Cocktail`模型治理策略，为大模型开发者提供一个**低成本持续提升模型性能**的方式：通过少量样例计算融合权重，借助模型融合技术融合微调模型和原模型的优势，实现“模型资源”的高效利用。
- **融合多个LLM**：既能提升目标任务性能，又能保持通用能力收集和构建目标任务数据集并对大语言模型（LLM）进行微调，可以提高其在目标任务的性能表现
  - 然而，这种方式会导致**除目标任务以外的一般任务的性能明显下降**，损害LLM原本具备的通用能力。
  - 模型融合技术通过融合多个模型提高单模型的性能。受此启发，LM-Cocktail 策略进一步通过对目标任务计算不同模型的重要性，赋予不同模型不同的权重，在此基础上进行模型融合，在提升目标任务上性能的同时，保持在通用任务上的强大能力。
- **模型治理新策略**：博采众长，持续为大模型增添新技能
  - 开源社区的模型逐渐增多，大模型开发者也可能在多次训练中累计了越来越多的模型，每个模型都具有各自的优势，如何选择合适的模型执行任务或进一步微调反而成为一个问题。
  - **LM-Cocktail 策略** 可帮助汇总各模型的优势能力，就像制作鸡尾酒那样，通过加入不同的模型进行调制，得到一个具备多种特长的“多技能”模型。
  - LM-Cocktail **手动**选择模型配比，或者输入少量样例**自动**计算加权权重，来融合现有模型生成一个新模型，该过程不需要对模型进行重新训练并且具备适配多种结构的模型，如大语言模型 Llama，语义向量模型 BGE等。
  - 此外，如果开发者缺乏某些目标任务的标签数据，或者缺少计算资源进行模型微调，那么采用 LM-Cocktail 策略可以省去模型微调步骤，通过构造非常少量的数据样例，融合开源社区中已有的大语言模型来调制自己的“LM鸡尾酒”。

[大模型灾难性遗忘解决方法之一：LM-Cocktail](https://zhuanlan.zhihu.com/p/689403852?utm_psn=1816553734890725376)
- 论文 [LM-Cocktail: Resilient Tuning of Language Models via Model Merging](https://arxiv.org/pdf/2311.13534)
- 代码、模型: [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding)

通过**模型融合**兼顾通用以及domain能力
- 以一定**权重**融合多个模型

合并时有两大问题
- 合并哪些模型 -》 base模型和微调模型
- 以什么权重合并

公式
- ![](https://pic2.zhimg.com/80/v2-4ae424fffa249b0b9cddad7aa6e10d5f_1440w.webp)
- ![](https://pic2.zhimg.com/80/v2-5b5bb6af26cd334a77d8daaf6aa97e67_1440w.webp)

合并后的模型和原始模型一样在垂域表现近似

变种
- mono-specialist：直接垂域ft和原始合并
  - `Mr ← αMt + (1 − α)Mb`, Mb是base模型
- without-ft：如果没有数据/GPU可供目标领域微调，直接融合基座和多个domain模型
  - `Mr ← ∑ wi ∗ Mi`

实验结果
- ![](https://pic3.zhimg.com/80/v2-dd3def5aa36f1de70f859ff862622aa8_1440w.webp)



### (5) MoE

多个分支, 分别指向通用基座、特定场景的LLM


## 微调方法

【2023-9-21】[大模型二次训练避坑指南](https://mp.weixin.qq.com/s/DuKBGPUKXEvqCNNBjpX-kw)

领域自适应预训练（Domain-Adaptive Pretraining）在所属的领域数据上继续预训练（or 增量预训练、二次预训练）

二次训练有很多需要注意的地方，否则很容易产生`灾难性遗忘`（Catastrophic Forgetting）现象
- 在原始任务上训练好的神经网络在训练完新任务后，在原始任务上的表现崩溃式的降低。



### 总结

【2023-9-21】[大模型二次训练避坑指南](https://mp.weixin.qq.com/s/DuKBGPUKXEvqCNNBjpX-kw)
1. 分析**领域相关性**：
  - AllenAI研究表明，不考虑**领域相关性**而直接暴露于更多数据的继续预训练对最终任务性能有害。
  - 领域相似度可以通过不同领域间的**词汇重叠度**（提取出除停用词之外的top 10K的unigram，计算两个数据集的词汇重复度）来度量。
2. 使新数据分布与旧数据**分布近似**：
  - ChatHome数据比例实验中，以1:5的比例的语料混合，在C-Eval和CMMLU上的表现是最佳的。
  - 但是经过了领域内预训练之后，相比于未经过预训练的模型，在C-Eval和CMMLU上，效果均有所下降。
  - 度小满轩辕2.0模型中，为防止遗忘，混合**无监督数据**和**指令数据**，并且合并了继续预训练和指令微调阶段：
3. 降低**学习率**：
  - 当使用较大的学习率2e-5进行训练时，模型在**通用**数据集上的准确率较高，而在**指令**任务上的准确率则迅速下降，这表明存在明显的遗忘。
  - 当使用**较低**的学习率（如1e-6和5e-6）时，遗忘现象会明显缓解，但域内准确率也会降低。
4. 进行**warm up**：
  - 蒙特利尔大学研究表明，当模型经过「充分」训练后，不管多长的预热步数最后的性能都差不多。但前提是「充分训练」，如果只看训练前期的话，使用更长的预热步数，无论是上游任务还是下游任务，模型的 Loss 都要比其他预热步数要低（下游学的快，上游忘的慢）。
5. 对新任务中参数变化施加**惩罚**；
6. **知识蒸馏**（KD），使微调模型的预测结果接近旧模型的预测结果。


【2023-11-11】
1. 国内基座大模型基本都是用 gpt4 训练出来的
2. 靠谱的应用必然是混合模型，否则控制不住幻觉
3. LORA 其实在训练专家模型方面挺靠谱的，不过得需要配合 MOE 架构
4. LORA 的灾难性遗忘问题比较严重，只适合训练专家模型


### 小数据过拟合

罗福莉 [当“大”模型遇上“小”数据](https://zhuanlan.zhihu.com/p/428263027)


Fine-tuning 过程中，一方面想利用大规模预训练模型提供的强大知识，另一方面又想解决“海量参数”与“少量标注样本”的不匹配问题，那么能否采用这样的方式来解决问题呢？

BERT提出以来，预训练模型参数量从最开始的**3亿**，逐渐攀升到了GPT-2的**15亿**，再到火出NLP圈的**1750亿**参数的GPT-3。

模型越来越大，但下游任务的**标注数据量却很少**。

如果直接将“大”模型在下游“小”数据上进行标准Fine-tune，将模型迁移到目标任务中去，会导致什么情况呢？
- 由于这种“大”与“小”的不匹配，容易过拟合，导致模型在下游任务中的表现差、不稳定、泛化性能差。

如何解决这种不匹配现象，缓解大规模预训练模型在下游任务过拟合。


#### 2021 Child-Tuning

EMNLP'21 Child-Tuning 从 backward 参数更新的角度思考问题，提出一种新 Fine-tuning 策略，在Fine-tuning过程中仅更新部分参数（对应的Child Network），效果出奇的好
- 论文 [Raise a Child in Large Language Model: Towards Effective and Generalizable Fine-tuning](https://arxiv.org/abs/2109.05687)
- 代码 [ChildTuning](https://github.com/alibaba/AliceMind/tree/main/ChildTuning)

在不同下游任务中相比 Vanilla Fine-tuning 有明显提高，如基于BERT模型在四个不同数据集中平均带来 1.5个点 提升，在ELETRA上甚至提升8.6个点。


两个步骤：
- Step1: 在预训练模型中发现确认Child Network，并生成对应的Weights的Gradients 0-1 Mask；
- Step2: 在后向传播计算完梯度之后，仅仅对Child Network中的参数进行更新，而其他参数保持不变。梯度掩码(Gradients Mask)

![](https://pic1.zhimg.com/80/v2-dcfe1ab54eee785cb42b9bee3b70492c_720w.webp?source=d16d100b)

怎么识别Step1提到的Child Network呢？两种算法。
- 一种是与下游任务无关的Child-Tuning_F方法
- 另一种则是与下游任务相关、能够自适应感知下游任务特点的Child-Tuning_D

这两种方式各有优缺点。
- 任务无关算法Child-Tuning_F 对于下游任务无关算法Child-Tuning_F（F for Task-Free） ，其最大的优点是简单有效，在Fine-tune的过程中，只需要在每一步更新的迭代中，从伯努利分布中采样得到一个Gradients Mask(M_t)即可，相当于在对网络参数更新的时候随机地将一部分梯度丢弃。

代码实现

原来optimizer里加入简单几行代码：

```py
for p in model.parameters():
  grad = p.grad.data
  
  ## Child-Tuning_F Begin ## 
  reserve_p = 0.2  # the ratio of gradients that are reserved. 
  grad_mask = Bernoulli(grad.new_full(size=grad.size(), fill_value=reserve_p))
  grad *= grad_mask.sample() / reserve_p
  ## Child-Tuning_F End ## 
​
  # the followings are the original code of optimizer
  ....

```


### 【2023-10-10】马里兰 NEFTune -- 加随机噪声

【2023-11-1】[微调时只需要简单的在 embedding层上加随机噪声即可大幅度提升微调模型的对话能力?](https://mp.weixin.qq.com/s/-El3HDf3HStj4j9dXjdwMw)
- 马里兰大学 [NEFTune: Noisy Embeddings Improve Instruction Finetuning](https://arxiv.org/pdf/2310.05914.pdf)
- 代码：[NEFTune](https://github.com/neelsjain/NEFTune)

微调时只需要简单的在 embedding层上加**随机噪声**即可大幅度提升微调模型的对话能力，而且也不会削弱模型的推理能力，他们从模型过拟合的角度对这一现象进行了解释。

有时改进幅度非常大,而且没有额外的计算或数据开销。
- Alpaca微调LLaMA-2-7B 可在 AlpacaEval上取得**29.79%**的表现,而使用加了噪声的嵌入则提高到**64.69%**。

不过该工作只在比较小的模型上进行微调，评估上也略显单一，解释上也不算太深入。不过实现起来非常简单，有资源的话可以快速试试。

方法

NEFTune
- 先从数据集中采样一个**指令**（Instruction）,并将其转换为嵌入向量。
- 然后,NEFTune添加一个**随机噪声向量**来增强嵌入。
  - 噪声向量是通过随机采样均匀分布的独立identically分布的元素生成的,每个元素范围是`[-1,1]`, 然后用一个因子α/√Ld缩放整个噪声向量,其中L是序列长度,d是嵌入维度,α是一个可调参数。

```py
def new_func(x):
    # during training, we add noise to the embedding
    # during generation, we don't add noise to the embedding
    if model.training:
        embed_init = orig_embed(x)
        dims = torch.tensor(embed_init.size(1) * embed_init.size(2))
        mag_norm = noise_alpha/torch.sqrt(dims)
        return embed_init + torch.zeros_like(embed_init).uniform_(-mag_norm, mag_norm)
    else:
        return orig_embed(x)
return new_func
```

NEFTune 表明: 正则化对LLM训练很重要。
- NEFTune 简单但可以持续稳定地改进指令（Instruction）微调结果,这表明正则化在LLM下值得重新审视。
- NEFTune对下游对话质量有很强的正面影响。

本文局限
- 采用AlpacaEval基准进行评估,这依赖于一个大模型判别器。
- 由于计算资源有限,在多个数据集上无法对更大的70B模型进行验证。

### 【2023-10-19】斯坦福 EFT -- 模拟微调

【2023-10-23】[斯坦福NLP提出EFT：如何不实际微调而“假装”微调了LLM?](https://mp.weixin.qq.com/s/I7iq6a0CPb9xlLK8hRK3uw)

语言模型（LM）训练经历两个阶段：
- 利用大量多样化的文本数据进行**预训练**；
- 对模型针对特定目标进行**微调**。

业界普遍认为
- **预训练**阶段是模型获取**核心知识和技能**的关键，而**微调**更偏重于**调整和优化**这些能力
- knowledge and skills come from pre-training, and fine-tuning mostly filters this knowledge and skillset

但这一观念却没有深入探究。
> What would happen if we combined the knowledge learned by a **large model** during `pre-training` with the
knowledge learned by a **small model** during `fine-tuning` (or vice versa)?

为了探索这两个阶段各自的贡献，斯坦福大学提出了一种新的技术 —— **模拟微调**（EFT）。
- 模拟在不同规模下的预训练和微调结果，从而更清晰地探讨不同训练阶段的影响。
- Paper: [An Emulator for Fine-Tuning Large Language Models using Small Language Models](https://arxiv.org/pdf/2310.12962.pdf)  


EFT
- 原理：
  - 模型行为可分解为两部分：预训练模型的基础行为，微调过程中获得的行为改变。
- 只改变一个阶段（比如只扩大预训练的规模，而不改变微调的规模），模型能力会如何变化。

实验结果
- 加强**微调规模**能够显著增强模型的**帮助性**，而扩大**预训练规模**则能更好地确保**事实精准度**。
- 此外，EFT允许不需要额外训练的前提下调整模型的行为特质
  - 例如 提高其帮助性和减少其潜在危害。

研究者们还提出了一个特殊的EFT应用，避免对大规模LMs进行微调，而是通过与小型微调模型的结合，来模拟大型模型的微调效果。


### 【2023-10-24】LoRAShear 微软

[LoRAShear:微软在LLM修剪和知识恢复方面的最新研究](https://zhuanlan.zhihu.com/p/666273516?utm_psn=1706739217026297857)

LoRAShear是微软为优化语言模型模型(llm)和保存知识而开发的一种新方法。它可以进行结构性修剪，减少计算需求并提高效率。
- LHSPG技术（ Lora Half-Space Projected Gradient）支持渐进式结构化剪枝和动态知识恢复。可以通过依赖图分析和稀疏度优化应用于各种llm。
- LoRAPrune将LoRA与迭代结构化修剪相结合，实现参数高效微调。在LLAMA v1上的实现即使进行了大量的修剪也能保持相当的性能。

问题
>- 信息的动态性要求LLM不断更新知识。

一般情况下微调用来向模型灌输最新的见解，开发人员使用特定于领域的数据对预训练模型进行微调使其保持最新状态。因为组织和研究人员的定期更新对于保持llm与不断变化的信息景观保持同步至关重要。但<span style='color:red'>微调成本大且周期长</span>。

微软研究人员推出了一种开创性方法——`LoRAShear`。这种方法不仅简化了llm，而且促进了结构知识的恢复。
- [LoRAShear: Efficient Large Language Model Structured Pruning and Knowledge Recovery](https://arxiv.org/abs/2310.18356)
- 结构修剪的核心: 去除或减少神经网络架构中的特定组件，优化效率、紧凑性和计算需求。

(1) LoRAShear引入了`LHSPG`技术，支持渐进式结构化修剪。这种方法在LoRA模块之间无缝地传递知识，并集成了动态知识恢复阶段。微调过程类似于预训练和指示微调，确保llm保持更新和相关性。

(2) 论文还有`LoRAPrune` 集成技术，将LoRA与迭代结构化修剪相结合，实现了参数高效的微调和直接硬件加速。
- 这种节省内存方法完全依赖于LoRA的权重和梯度来进行修剪标准。这个过程包括构造一个跟踪图，确定要压缩的节点组，划分可训练的变量，并最终将它们返回给LLM。

论文在开源LLAMAv1上的实现，证明了LoRAShear的有效性。
- 修剪了20%的LLAMAv1只有1%的性能损失，而修剪了50%的模型在评估基准上保留了82%的性能


### 【2023-11-22】LM-Cocktail


问题
- LLM finetune方式会导致目标任务之外的生成任务上，性能严重衰减（performance degeneration）

- 论文：[LM-Cocktail: Resilient Tuning of Language Models via Model Merging](https://arxiv.org/pdf/2311.13534.pdf)
- 代码：[FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding)

BAAI和中科院发布 LM-Cocktail，使用模型融合（model merging）方式
- 将 finetune模型融入 pre-train模型中
- 或 两者同等重要，加权

详见：[MoE专题](moe)

### 【2024-1-14】腾讯 LLaMA2-Pro 块扩展

【2024-1-14】[腾讯LLaMA2-Pro开源到wisemodel社区，块扩展方法解决微调的灾难性遗忘](https://mp.weixin.qq.com/s/b6urq9rRtGvf2Izp6sfKWA)

香港大学与腾讯ARC实验室等联合研发的LLaMA-Pro-8B系列模型发布到了始智AI [wisemodel.cn](https://wisemodel.cn/organization/TencentARC) 开源社区。

LLaMA-Pro-8B系列模型是在LLaMA2-7B模型基础上，通过Decoder块扩展的方法，增加了8个新的块扩展，总参数量是83亿，给模型增加专业领域新能力，并且未产生灾难性遗忘的问题。

块扩展是一种简单而有效的**后预训练**方法，通过复制Transformer块来扩展现成的预训练语言模型，新添加的块，其线性层被初始化为零以启用恒等映射，仅使用特定领域的语料库进行进一步调整，而其余块则保持冻结。调整后，扩展的预训练模型在通用和特定领域任务上都表现出色。
- 在原始的每个块中加入一个恒等映射块（identity block），即输入和输出相同，确保扩展后的模型和扩展前相同的输出。


### 【2024-12-7】RFT 强化微调

ReFT REinforced Fine-Tuning
- 论文 [REFT: Reasoning with REinforced Fine-Tuning](https://arxiv.org/pdf/2401.08967)
- 解读：[《论文讲解》ReFT: Reasoning with Reinforced Fine-Tuning](https://zhuanlan.zhihu.com/p/681219605)
- 代码 [mwp_ReFT](https://github.com/lqtrung1998/mwp_ReFT)

- 【2024-12-7】[OpenAI强化微调登场：几十条数据o1-mini反超o1暴涨80%，奥特曼：今年最大惊喜](https://mp.weixin.qq.com/s/ulQ1ep1kEOGLqpDarNxo0A)
- 【2024-12-7】[揭秘强化微调(ReFT)：重塑大语言模型推理格局的突破技术](https://mp.weixin.qq.com/s/KPq73MeVDtgwfKEcj06QZw)
- 【2025-5-9】[OpenAI强化微调终于上线了：几十个样本就可轻松打造AI专家](https://mp.weixin.qq.com/s/c7RfeoWNwh3NZDeuTCXXLw) 强化微调（Reinforcement Fine-Tuning, RFT）正式登陆 OpenAI o4-mini 模型，RFT 用思维链推理和任务专属的评分机制提升模型在特定复杂领域的表现，可以将AI模型从高中学生水平轻松提升到了专家博士水平。  通过强化微调，轻松将模型某个领域的专业能力迅速提升，打造出各种AI专家

如何提升LLM推理能力? 
- 监督微调（SFT）和链式思考（CoT）注释, 来增强模型的推理能力
- 一种思路: 用CoT构建推理语料, 在SFT训练阶段从学习语料中学习推理能力 

问题
- 泛化能力有限, SFT效果依赖标注的推理语料, 如数学问题上应该有多种解法,语料只有1种

`强化微调`（Reinforcement Fine-Tuning）结合在线RL和SFT提升模型泛化能力
使用**极少**训练数据即在特定领域轻松地创建专家模型。
- 最低几十个例子就可以。

RFT 场景：
1. 指令变代码：把开放式指令转换成**结构化**代码、配置或模板，并且这些产出必须通过确定性的测试。
2. 杂乱文本**提炼**精华：从非结构化文本中提取可验证的事实和摘要，并以JSON或其他结构化模式输出。
3. **复杂规则**精准应用：当信息细微、量大、层级复杂或事关重大时，进行精细的标签或策略决策。

OpenAI Cookbook 官方文档
- • [模型介绍](https://platform.openai.com/docs/models)
- • [强化微调指南](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)
- • [评分器](https://platform.openai.com/docs/guides/graders)
- • [模型优化概览](https://platform.openai.com/docs/guides/model-optimization)

参考：[rft-use-cases](https://platform.openai.com/docs/guides/rft-use-cases?chipstack=use-case)


过程
- (1) 预热: 先用 SFT 预热(warmup)
  - 预热阶段，模型在“`问题，CoT`”元组数据集上微调，使模型具备基本的问题解决能力。
  - CoT生成过程可以分解为一系列`下一个标记预测`动作，最后一个动作标记 `<eos>` 表示生成
- (2) 强化学习: 再用在线RL(如PPO)进一步训练
  - 模型通过**重复采样**响应、**评估**响应答案的正确性，并在线更新其参数来提高性能。
  - 使用 PPO算法进行训练，模型通过采样**多种**CoT推理路径来学习，从而获得比SFT更丰富的监督信号。

ReFT的一些优势
1. 更好的泛化性能：因为后面的训练完全不需要用到 CoT 标注数据，完全依赖模型自己去探索 怎么样的CoT 是正确的。
2. 相比RLHF训练简单: 不需要标注额外数据训练Reward Model, 不需要额外数据提高policy. 当然这里作者也认为更多的数据能提高效果，但这并不是这个文章的目的。
3. 可用性: 没有一些特定restriction，在其他任务上也是可以用到的，适用于大家SFT数据少的时候，我们做一些效果上的性能提升。
4. 更好的效果：最后作者也在GSM8K上做实验，证明更好的policy也能在Majority Voting和进一步Reranking上面有效果的提升，而且也是非常的明显。


微调后, o1-mini模型得分提高80%，直接反超o1正式版。

目前OpenAI已开启强化微调研究计划，开发者可以申请强化微调API的alpha版本访问权限。

进行测试时，可使用几十到几千个高质量数据，模型能够通过强化学习自行探索和学习如何推理复杂任务。

生物医学任务，AI需要根据病例描述的症状，找出相关基因。

训练数据长这样：

```js
病人信息：51岁女性，疾病发病时间未具体说明。
症状：眼距过宽、睑裂狭小、小颌畸形、软腭咽闭合不全、甲状旁腺功能减退、全身发育迟缓和感觉神经性听力障碍
未表现出以下症状：腭裂、法洛四联症、肺动脉瓣闭锁、心房隔缺损、主动脉肺动脉侧支血管
请列出所有可能导致这些症状的基因，从可能性最大到可能性最小，并解释为什么你认为这些特定的基因可能是原因。
```

评分模型（Grader）会对模型的答案进行评分，OpenAI会提供不同的评分模型，并支持自定义。

强化微调步骤
- 网页选择训练集和验证集, 设置超参
- 微调过程中，可以观察模型性能指标变化趋势

![](https://pica.zhimg.com/v2-d0e6323c040f437caf5da928056b1d4e_1440w.jpg)

OpenAI内部测试中，强化微调在生物化学、安全、法律和医疗保健领域取得成功。




实验使用8个A100-80GB GPU 训练，并采用 DeepSpeed和HuggingFace Accelerate工具。
- ReFT 预热阶段，使用AdamW优化器，并设置了学习率和批量大小。
- 强化学习阶段，使用PPO算法，并设置了相关超参数。

实验结果表明
- ReFT在自然语言和基于程序的CoT上都显示出显著的性能提升和泛化能力。
- 此外，ReFT还能从**多数投票**和**奖励模型重新排名**等技术中受益，进一步提升性能。

ReFT 在**所有**数据集上均优于SFT和其他自训练方法。
- 特别是在CodeLLAMA模型上，ReFT在GSM8K数据集上的N-CoT和P-CoT任务中分别取得了9点和8点以上的提升。
- 此外，ReFT还表现出对多数投票和奖励模型重新排名技术的兼容性，进一步提升了性能。

### 【2025-2-5】CFT 批判式微调

【2025-3-9】[让SFT重新伟大！CMU等华人学者提出全新「批判式微调」，媲美复刻版DeepSeek](https://mp.weixin.qq.com/s/l1DdkoHp36g05dRm2a3gDg)

复杂推理任务里，SFT 往往让大模型显得力不从心。

SFT 过程中，模型要模仿人类标注或合成的高质量回复，以增强通用指令遵循能力。

这类 SFT 数据集通常使用 `Self-Instruct` 和 `Evol-Instruct` 等方法进行构建。

局限性
- 随着数据集规模和质量的提升，SFT 面临着**边际收益递减**的问题，尤其是在训练本身效果就不错的基础模型时，使用SFT甚至可能会导致性能下降。

【2025-2-5】CMU、滑铁卢大学等机构3名华人论文，针对SFT做出了更进一步的改进，提出`批判式监督微调`方法（`CFT`，Critique Fine-Tuning），让模型更有效地模仿模仿数据集
- 论文 [Critique Fine-Tuning: Learning to Critique is More Effective than Learning to Imitate](https://arxiv.org/pdf/2501.17703)
- 主页 [CritiqueFineTuning](https://tiger-ai-lab.github.io/CritiqueFineTuning/)

「批判性微调」（`CFT`）方法，仅在 **50K** 样本上训练，就在大多数基准测试中优于使用超过 **200万** 个样本的**强化学习**方法

CFT 将重点从**简单模仿**转向**批判学习**

核心思想: 让模型学会批判，而不是简单地模仿，其灵感来源于人类的学习过程。
- 学霸们在学习过程中，不仅仅是复制提供的答案，而是分析、批判和改进它们。
- CFT数据集中为错误响应提供相应的批评供模型学习，让LLM能够识别响应中存在的缺陷，进而提出改进建议并验证正确性。

这种方法不仅能够提升推理能力，还能使模型在面对复杂任务时表现出更强的适应性和灵活性。


## 微调模型使用 

RESTful API 提供大模型服务


### FastChat API

FastChat 将模型发布为 openai 兼容的RESTful API以便外部服务使用。

FastChat 为第三方模型提供 <span style='color:red'>与OpenAI兼容的API</span>，因此可用 FastChat 作为 OpenAI API 的本地**直接替代品**。

FastChat 服务器与openai-python库和 cURL 命令兼容。支持以下 OpenAI API：
- Chat Completions
- Completions
- Embeddings


```py
# （1） 启动控制器
python3 -m fastchat.serve.controller
# （2）启动模型
# 通过 --model-path 指定模型路径，这里指定前面微调后的模型路径 /ossfs/workspace/sft-models/my-llama5
python3 -m fastchat.serve.model_worker --model-path /ossfs/workspace/sft-models/my-llama5
# （3）启动 RESTful API 服务器
python3 -m fastchat.serve.openai_api_server --host localhost --port 8000
```

现在，测试 API 服务器。

openai_api_server.py 是实现一个完全兼容 OpenAI 的 API 服务器，因此可直接与openai-python库一起使用。

```sh
# 安装 openai
pip install --upgrade openai
```

模型测试

```py
import openai
# to get proper authentication, make sure to use a valid key that's listed in
# the --api-keys flag. if no flag value is provided, the `api_key` will be ignored.
openai.api_key = "EMPTY"
openai.api_base = "http://localhost:8000/v1"

# 这里指定微调的模型名字，也就是保存模型文件的文件夹名称
model = "my-llama5"

# create a chat completion
completion = openai.ChatCompletion.create(
  model=model,
  messages=[{"role": "user", "content": "你是谁"}]
)
# print the completion
print(completion.choices[0].message.content)
```

作者：[惜鸟](https://juejin.cn/post/7270867067216199719)


### 本地知识库

微调模型和本地知识库整合
- 使用工具 Langchain-Chatchat

```sh
# （1）下载 Langchain-Chatchat：
git clone https://github.com/chatchat-space/Langchain-Chatchat.git
# （2）进入 Langchain-Chatchat，安装 python 依赖库：
cd Langchain-Chatchat
pip install -r requirements.txt
pip install -r requirements_api.txt
# （3）使用下面的命令复制配置文件：
cp configs/model_config.py.example configs/model_config.py
# model_config.py 配置文件需要修改如下内容，在llm_model_dict指定模型的地址，并且设置LLM_MODEL的名称和 llm_model_dict的 key 对应
llm_model_dict = {
    "llama2": {
        "local_model_path": "/ossfs/workspace/sft-models/my-llama5",
        "api_base_url": "http://localhost:8888/v1",  # 修改为fastchat服务中的"api_base_url"
        "api_key": "EMPTY"
    }
}
# LLM 名称
LLM_MODEL = "llama2"

# （4）启动 llm_api.py：
python server/llm_api.py

```

连接测试

```py
# 服务启动后接口调用示例：
import openai
openai.api_key = "EMPTY" # Not support yet
openai.api_base = "http://localhost:8888/v1"

model = "llama2"

def get_answer(content):
    # create a chat completion
    completion = openai.ChatCompletion.create(
      model=model,
      messages=[{"role": "user", "content": content}]
    )
    print('用户:', content)
    # print the completion
    print('模型:',completion.choices[0].message.content)

get_answer('你是谁')
get_answer('你叫什么名字')
```


## 微调 Llama 2

参考：[微调Llama2自我认知](https://juejin.cn/post/7270867067216199719)
- 如何使用 SFT 微调 Llama2
  - 微调 Llama2 需要 1 个GPU，24G 内存，较低的内存会导致加载模型较慢。
- 如何导出微调后的大模型
- 如何使用 FastChat 实现 OpenAI 兼容的 RESTful API 接口

### 前置工作

开源框架和模型
-   微调的模型： [**Chinese-Llama-2-7b**](https://huggingface.co/LinkSoul/Chinese-Llama-2-7b "https://huggingface.co/LinkSoul/Chinese-Llama-2-7b")
-   微调框架： [**LLaMA-Efficient-Tuning**](https://github.com/hiyouga/LLaMA-Efficient-Tuning "https://github.com/hiyouga/LLaMA-Efficient-Tuning")
-   提供openai兼容的RESTful API框架： [**FastChat**](https://github.com/lm-sys/FastChat "https://github.com/lm-sys/FastChat")
-   本地知识库问答应用框架： [**LangChain-Chatchat**](https://github.com/chatchat-space/Langchain-Chatchat "https://github.com/chatchat-space/Langchain-Chatchat")

由于Llama2本身的中文对齐较弱，没有直接使用 `meta-llama/Llama-2-7b`, 而是用 `LinkSoul/Chinese-Llama-2-7b`进行微调，微调方法是类似的，感兴趣的可以基于 `meta-llama/Llama-2-7b` 进行微调

### 步骤

#### 下载模型

huggingface上面搜索模型名称，下载模型：
- 使用下面的命令下载预训练模型
- 新建一个 models 文件夹, 存放下载的大模型

```sh
# 在当前目录新建一个 models 文件夹用来存放大模型
mkdir models
# 使用下面的命令下载模型，模型比较大，下载过程较缓慢，
git lfs install
git clone https://huggingface.co/LinkSoul/Chinese-Llama-2-7b
# 设置下面的环境变量，则不会下载大文件，只会下载小文件
GIT_LFS_SKIP_SMUDGE=1
```

#### 下载微调框架

当前目录下载微调框架 LLaMA-Efficient-Tuning ：

```sh
git clone https://github.com/hiyouga/LLaMA-Efficient-Tuning.git
# 进入 LLaMA-Efficient-Tuning 目录：
cd LLaMA-Efficient-Tuning
# 找到存放微调数据的data目录
```

#### 准备微调数据

data 目录下 self_cognition.json 是自我认知文件，`<NAME>` 和 `<AUTHOR>`是占位符，只需要复制一份文件，将占位符替换为需要的名称即可

微调数据准备好了后，需要在 dataset_info.json 中配置如下：

```json
{
	"self_cognition": {
    "file_name": "self_cognition.json", // 微调的数据文件
    "file_sha1": "6287a730ada924fc5d9eadc6d8f865e01b7a6f67" // sha可不填
  }
}
```

#### 开始微调

微调数据准备好后就可以开始执行微调了，使用如下命令进行微调：

```sh
CUDA_VISIBLE_DEVICES=0 python src/train_bash.py \
    --stage sft \
    --do_train \
    --dataset self_cognition \
    --model_name_or_path /ossfs/workspace/models/Chinese-Llama-2-7b \
    --output_dir /ossfs/workspace/llama2-sft/checkpoint-01 \
    --template default \
    --finetuning_type lora \
    --lora_target q_proj,v_proj \
    --overwrite_cache \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 2000 \
    --learning_rate 1e-3 \
    --num_train_epochs 10.0 \
    --plot_loss \
    --fp16
```

参数详解

```sh
--stage sft: 训练阶段。这里指定为sft，表示进行模型的微调（self-supervised fine-tuning）阶段。
--do_train: 是否进行训练，设置为True表示进行训练。还可以设置为（--do_eval：表示评估，--do_predict：表示预测）
--dataset self_cognition: 数据集名称。这里指定为self_cognition，表示使用自我认知数据集。
--model_name_or_path /ossfs/workspace/models/Chinese-Llama-2-7b: 预训练模型的名称或路径。这里指定为/ossfs/workspace/models/Chinese-Llama-2-7b，表示加载路径下的预训练模型。
--output_dir /ossfs/workspace/llama2-sft/checkpoint-01: 训练输出目录。训练过程中生成的模型和日志将保存在该目录下。
--template default: 模板名称。这里指定为default，表示使用默认模板。
--finetuning_type lora: 微调类型。这里指定为lora，表示使用LoRA（Language Representation with Additive Transformation）微调方法。
--lora_target q_proj,v_proj: LoRA微调的目标层。这里指定为q_proj,v_proj，表示只对q_proj和v_proj两个层进行微调。
--overwrite_cache: 是否覆盖缓存。设置为True表示覆盖缓存。
--per_device_train_batch_size 4: 每个设备的训练批次大小。这里指定为4，表示每个设备上的训练批次大小为4。
--gradient_accumulation_steps 4: 梯度累积步数。这里指定为4，表示每4个步骤累积一次梯度。
--lr_scheduler_type cosine: 学习率调度器类型。这里指定为cosine，表示使用余弦学习率调度器。
--logging_steps 10: 日志记录步数。每训练多少步记录一次训练日志。
--save_steps 2000: 模型保存步数。每训练多少步保存一次模型。
--learning_rate 1e-3: 学习率。这里指定为1e-3，表示初始学习率为0.001。
--num_train_epochs 10.0: 训练轮数。这里指定为10.0，表示进行10轮训练。
--plot_loss: 是否绘制损失曲线。设置为True表示绘制损失曲线。
--fp16: 是否使用混合精度（half-precision）训练。设置为True表示使用混合精度训练。

```

启动微调命令后，输出日志，确认是否需要 wandb (一个深度学习轻量级可视化工具 Weights & Biases)将训练结果可视化

#### 训练监控

查看损失函数曲线： 解读训练过程中模型的收敛情况和学习进展
- ![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7eb2efb5c1324cfd929bfdc250be494f~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp#?w=1470&h=1048&e=png&b=fefefe)

初始阶段的损失值较高，随着训练的进行，损失值会逐渐下降。
- 如果损失值趋向于**稳定**，说明模型已经收敛，训练效果良好。
- 如果损失值**下降很慢**，可能需要更多的训练轮次/调整模型超参数。
- 如果损失值波**动较大**，可能存在过拟合或其他问题，需要进一步调整模型或数据。

解读train loss 图像时，可以观察以下几个方面：
- 初始阶段的损失值高低，较高的初始损失值可能表明模型初始化不合适，需要调整初始化方法。
- 损失值下降的速率，较快的下降速率可能表明模型对数据的学习能力较强，但也可能存在过拟合的风险。
- 损失值的稳定性，稳定的损失值说明模型已经收敛，训练效果较好。如果损失值在一定范围内波动，可以考虑增加训练轮次或使用正则化等方法进一步优化模型。
- 训练过程中的异常情况，如损失值突然上升或跳跃，可能表明出现了问题，需要检查模型或数据是否存在异常。

总之，train loss 图像可以提供对模型训练过程的直观理解，帮助调整模型和优化训练策略，以达到更好的训练效果。

train loss 仅仅是一个指标，不能完全代表模型的训练效果。还需要综合考虑模型在其他指标上的表现，如准确率、精确率、召回率等，以及在实际应用场景中的效果。

#### 测试微调后的模型

微调框架 LLaMA-Efficient-Tuning 提供了三种测试使用微调模型的方式，如下所示：
- api_demo.py：使用**api方式**调用微调模型
- cli_demo.py：在**命令行**中调用微调模型
- web_demo.py：在**web页面**中调用微调模型

cli_demo

```sh
CUDA_VISIBLE_DEVICES=0 python src/cli_demo.py \
    --model_name_or_path /ossfs/workspace/models/Chinese-Llama-2-7b \
    --checkpoint_dir /ossfs/workspace/llama2-sft/checkpoint-01\
    --template llama2

# 支持多个微调模型, 逗号分割
CUDA_VISIBLE_DEVICES=0 python src/cli_demo.py \
    --model_name_or_path /ossfs/workspace/models/Chinese-Llama-2-7b \
    --checkpoint_dir /ossfs/workspace/llama2-sft/checkpoint-01,/ossfs/workspace/llama2-sft/checkpoint-02\
    --template default
```

#### 导出微调模型

```sh
CUDA_VISIBLE_DEVICES=0 python src/export_model.py \
    --model_name_or_path /ossfs/workspace/models/Chinese-Llama-2-7b \
    --checkpoint_dir /ossfs/workspace/llama2-sft/checkpoint-01\
    --output_dir /ossfs/workspace/sft-models/my-llama5 \
    --template default
```


## OpenAI 微调


### Azure Finetune

【2024-3-21】[Customize a model with fine-tuning](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning?tabs=turbo%2Cpython-new&pivots=programming-language-studio)， [通过微调自定义模型](https://learn.microsoft.com/zh-cn/azure/ai-services/openai/how-to/fine-tuning?tabs=turbo%2Cpython-new&pivots=programming-language-studio)

- 可控参数： epoches, batch_size, learning_rate_multiplier `[0.02, 0.2]`

- ![](https://learn.microsoft.com/en-us/azure/ai-services/openai/media/fine-tuning/studio-advanced-options.png)
- ![](https://learn.microsoft.com/en-us/azure/ai-services/openai/media/fine-tuning/studio-model-details.png)

微软 azure 上ft费用不同，比OpenAI便宜很多
- 0125版, 输入是**3倍**，输出是**1.3倍** 
- instruct版的ft费用不变
- 16k，ft后的费用，输入是6倍，输出是近似3倍
- [文档](https://azure.microsoft.com/zh-cn/pricing/details/cognitive-services/openai-service/)

|版本|上下文|输入费用(每1k tokens)|输出费用(每1k tokens)|
|---|---|---|---|
|GPT-3.5-Turbo 0125|16k|0.0005|0.0015|
|GPT-3.5-Turbo Instruct|4k|0.0015|0.002|
|GPT-3.5-Turbo (4K) **ft** |4k|0.0015|0.002|
|GPT-3.5-Turbo (16K) **ft**|16k|0.003|0.004|


### GPT-3 微调 -- 旧: /v1/fine_tuning

【2023-5-2】[OpenAI ChatGPT API 文档之 Fine-tuning（微调）](https://zhuanlan.zhihu.com/p/626140269)
- OpenAI官方：[legacy-fine-tuning](https://platform.openai.com/docs/guides/legacy-fine-tuning)

The now deprecated fine-tunes endpoint only supports the following base models: `davinci`, `curie`, `babbage`, and `ada`. These are the original models that do not have any instruction following training (like `text-davinci-003` does for example). You are also able to [continue fine-tuning a fine-tuned model](https://platform.openai.com/docs/guides/legacy-fine-tuning/continue-fine-tuning-from-a-fine-tuned-model) to add additional data without having to start from scratch.

GPT-3 开放互联网的大量文本上进行了预训练。当给出仅包含几个示例的提示，直观判断尝试执行的任务并生成看似合理的补全（completion），这通常称为“小样本学习（few-shot learning）”。

`微调`（Fine-tuning）通过训练超出提示范围的更多示例来改进小样本学习，在大量任务上取得更好的结果。模型经过微调后，不再需要在提示中提供示例。这可以节省成本并实现更低延迟的请求。
- [收费](https://openai.com/pricing)

微调可更好地利用 API 模型：
- 效果比提示（prompt）质量更高
- 能训练不适合提示的示例
- 提示较短而节省 token
- 更低的延迟请求

微调涉及以下步骤：
- 准备、上传训练数据
- 训练微调模型
- 使用微调模型

成功与否决定因素是训练数据。
- 大规模：数千或数万的例子
- 高质量：格式一致，没有缺失或错误的例子
- 代表性：训练数据类似于实际使用模型过程中的数据


#### 文本分类示例

【2023-5-17】[精调GPT#1：精调GPT-3进行文本分类的最佳实践](https://zhuanlan.zhihu.com/p/628944148)
- [OpenAI分类示例](Fine tuning classification example)

文本分类

```s
# 微调
{"prompt": "burger -->", "completion": " edible"}
{"prompt": "paper towels -->", "completion": " inedible"}
{"prompt": "vino -->", "completion": " edible"}
{"prompt": "bananas -->", "completion": " edible"}
{"prompt": "dog toy -->", "completion": " inedible"}
# 预测
toothpaste --> ？
```

#### 用不用指令

精调后的模型**不一定**要在提示词中包含**指令或例子**，模型可以从训练案例中学会任务。
- 单任务不建议加指令：
  - 尽管向其中添加指令并不会影响性能，但确实会增加每个API调用的成本。
- ![](https://pic4.zhimg.com/80/v2-7e21c6fbded57b761da693e0f6f22ff7_1440w.webp)

| Prompt | Tokens | Recommended |
| --- | --- | --- |
| "burger -->" | 3 | ✅ |
| "Label the following item as either edible or inedible. <br>Item: burger <br>Label:" | 20 | ❌ |
| "Item: cake <br>Category: edible <br>Item: pan <br>Category: inedible <br>Item: burger <br>Category:" | 26 | ❌ |

问题：<span style='color:blue'>会影响其他任务吗？</span>

当微调涉及**多任务**时，指令就很有用了。
- 训练一个模型对文本字符串分类**多个特征**，就需要某种指令来告诉模型要哪种标签结果。

| Prompt | Completion | note |
| --- | --- | --- |
| "burger --> edible." | yes | 训练 |
| "burger --> handheld." | yes | 训练 |
| "car --> edible." | no | 训练 |
| "car --> edible." | no | 训练 |
| "cheese --> edible." | ??? | 预测 |

#### 提示词格式

分类问题的提示词应该<span style='color:red'>以某个文本序列结尾</span>，告诉模型输入的部分到此为止，接下来是分类的数据。
- 如果没有这种**信号**，模型可能追加额外的臆想出来的文本到分类标签上，比如：
  - burger edible (准确)
  - burger and fries edible (答非所问)
  - burger-patterned novelty tie inedible (不准确)
  - burger burger burger burger (没有产生标签)

分隔符序列样例：
- 确保所选择文本序列不会出现在其它文本中
- 比如，对Python代码分类的时候就要避免“###”或者“->”这样的符号）。否则所选的文本序列就没啥用了。

| Prompt | Recommend |
| --- | --- |
| burger | ❌ |
| burger --> | ✅ |
| burger<br>### | ✅ |
| burger >>> | ✅ |
| burger <br> Label | ✅ |

对大部分模型而言，提示词加上补全的总长度不能超过`2048`个token。
- `text-davinci-002`模型，限制在4000个token。

#### 如何选择标签

精调过程可以使用**任何**标签，无论这个标签包含具体语义（比如edible）还是没有具体语义（比如数字1）。
- 如果每个类别的训练数据很少，那么**语义标签**可能效果更好，这样模型还可以利用到其自身对标签含义的理解。

如果方便的话，推荐使用**单token**的标签。
- 按照【OpenAI中文文档】[API#2：如何使用tiktoken计算token数量提到的办法来计算字符串包含的token数量](https://zhuanlan.zhihu.com/p/626593576)。

单token的标签好处：
- 成本低
- 更容易获取概率，对于衡量信心指数、精度、召回率的时候很有用。
- 不会受到停止序列影响，不需要比较不同长度的结果

| Prompt | Label | Recommend |
| --- | --- | --- |
| "burger --> " | edible | ✅ |
| "burger --> " | 1 | ✅ |
| "burger --> " | yes | ✅ |
| "burger --> " | A burger can by eaten | ❌ |

冷知识：
>- 所有小于500的整数都是由单个token表示的。

如果一定要使用多token的标签，推荐每个标签由不同的token开头。
- 如果多个标签由同一个token开头，出于采样的影响，模型最终可能是有偏的。

#### 要多少训练数据

多少训练数据
- 取决于任务和性能要求。

| Examples per label | Performance (rough estimate) |
|---|---|
| Hundreds | Decent |
| **Thousands** | Good |
| Tens of thousands or more | Great |


下图展示了如何通过增加训练样例来提升分类准确率。
- ![](https://pic3.zhimg.com/80/v2-b0bc2334779596b2e6cc27bdc760814a_1440w.webp)
- 一般有**几千**例子就能得到不错的效果了

具体可以实验：分别用不同规模的数据集验证效果
- 比如 25%、50%、100%，看看指标是否随着数据规模增长而提升。
- 如果使用准确度和训练数据量画折线图，100%处的斜率就代表着继续增加数据能够带来的收益。
- 注意
  - 不能仅凭单次训练就来推断增加的数据在准确度上带来的价值，部分训练双倍的数据和一次完整的训练是不同的

#### 指标评估

如何评估精调之后的模型

评估精调模型的作用：
- 改进模型，便于优化
- 评估效果，判断是否足以上线交付

分类指标：
- 准确度
- F1
- 精确度 / 正面预测值 / 负面发现率
- 召回 / 敏感度
- 特异性
- AUROC
- AUPRC

使用哪种指标取决于特定应用以及如何权衡不同类型的错误。
- 检测一个少见但又很重要的事情，假阴性比假阳性的代价更大，那么可能会更关注`召回率`而非`准确率`。

OpenAI的API提供了选项来计算这些分类指标。如果启用，便会在精调的训练周期中定期计算这些指标。

为了启用分类指标，需要：
- 使用**单个token**的标签
- 提供**验证文件**（和训练文件格式相同）
- 设置**标识位** -- compute_classification_metrics
- 对于**多类别**分类，设置参数 -- classification_n_classes
- 对于**二分类**，设置参数 -- classification_positive_class

OpenAI CLI的精调调用案例

```sh
# For multiclass classification
openai.api.fine_tunes.create \
  -t <TRAIN_FILE_ID_OR_PATH> \ 
  -v <VALIDATION_FILE_OR_PATH> \
  -m <MODEL> \
  --compute_classification_metrics \
  --classification_n_classes <NUMBER_OF_CLASSES>

# For binary classification
openai.api.fine_tunes.create \
  -t <TRAIN_FILE_ID_OR_PATH> \
  -v <VALIDATION_FILE_OR_PATH> \
  -m <MODEL> \
  --compute_classification_metrics \
  --classification_n_classes 2 \
  --classification_positive_class <POSITIVE_CLASS_FROM_DATASET>
```

如果设置了--`compute_classification_metrics`，会在结果文件中看到下面的指标。

对于**多类别**分类：
- classification/accuracy: accuracy
- classification/weighted_f1_score: weighted F-1 score

对于二分类：

下面的指标是基于分类阈值0.5计算的（比如当概率大于0.5的时候，样例就被分类为正样本）
- classification/accuracy
- classification/precision
- classification/recall
- classification/f{beta}
- classification/auroc - AUROC
- classification/auprc - AUPRC

以上评估都假设分类所用的文本标签是单个token的标签，否则数字便是错的。

训练过程中的指标演化，通过Weights & Biases (wandb库)进行可视化。

#### 如何选择模型

如何选择正确的模型

OpenAI提供了5个模型可供精调：
- ada（最便宜也最快）
- babbage
- curie
- davinci
- text-davinci-002（最高质量）

具体用哪个模型取决于使用场景和质量、价格、速度方面的要求。一般的文本分类场景有两种：简单和复杂。
- 对于简单直接的任务，比如情感分类，更大的模型提供的收益是递减的
- 对于复杂任务，需要理解微妙的含义、推理、先验知识或代码能力，模型之间的差距就会很大，curie或者text-davinci-002这种复杂的模型更加契合。

一个项目最终可能会尝试所有的模型。按照开发路径来展示可能是这样：
- 使用**最便宜和最快**的模型来测试代码（ada）
- 使用**中等**的模型来进行早期的实验，检查数据集是否如预期一样工作（curie）
- 使用**最好**的模型执行更多的实验，看看性能的上限在哪里（text-davinci-002）
- 一旦有了好的结果，使用所有的模型执行训练，对比价格和性能，选择最符合需求的模型（所有模型）

另一个可能的开发场景是：
- 从小的数据集开始，训练最好的模型（text-davinci-002）
- 使用精调之后的模型来生成尽可能多的标签，把数据集的规模翻倍
- 使用新的数据集来训练更便宜的模型（ada）

#### 如何选择超参

如何选择训练的超参数：[官方说明](https://platform.openai.com/docs/guides/fine-tuning/iterating-on-hyperparameters)

精调过程中有许多参数可调整。一般来说，这些参数的默认值就能用，只有在明确带来表现提升的时候才应该去修改这些参数：
- 参数一：`n_epochs` ，默认为4，控制每个样例被训练使用多少次。
  - 分类问题，见过将这个数字设为4或10得到不错的结果。小的数据集需要更多的轮次，大的数据集需要的轮次较少。
  - 如果训练准确率不高，可以加大这个值。如果看到训练的准确率较高，而验证的准确率不高（过拟合），则应降低这个值。
  - 通过将compute_classification_metrics设置为True，并额外提供一个与训练数据不重复的验证数据集文件。
- 参数二：`batch_size`，默认为空，控制单个训练批次中用到的数据量。
  - 0.01-0.02之间效果都不错，但是5%以上就不行了。一般来说，更大的批次适合用在更大的数据集上面。
- 参数三：`learning_rate_multiplier`，默认为空，控制**模型权重更新频率**。
  - 0.02-0.5之间效果都不错，更大的学习率需要更大的批次数据量才能奏效。
- 参数四：`prompt_loss_weight`，默认为0.1，控制模型学习的提示词与最后补完的token之间的比例。
  - 如果提示词相对于补完而言比较长，那就有必要缩小这个值以免过度学习提示词本身。在我们的实验中，将这个值设为0有时候略差，有时候效果差不多，取决于数据集的情况。


关于`prompt_loss_weight`

模型被精调时，会学习来生成`提示词`和`补全`中看到的文本。实际上，从模型精调的视角出发，`提示词`和`补全`之间的区别是不太明确的。
- 两者主要区别是模型从提示词的token上学的较少，而在补全的token上学的较多。
- 这个比例就是通过 `prompt_loss_weight` 控制的，默认是**10%**。
- 如果设置为**100%**，就意味着模型对提示词和补全的token是一视同仁。无论使用提示的全部文本，还是使用补完的全部文本，还是以某种比例切分，结果都是一样的。对于分类的任务，推荐100%。
- 如果设置为**0**，模型仅仅学习补全部分。不过即便在这种情况下，提示词仍然是必要的，它们为后续的补完设置了上下文。有时候看见0值会略微降低分类的效果，或者对于学习率更加敏感；其中一种假设是少量的提示词有助于保留或改进模型对输入的理解能力。

#### 如何设置推理参数

如何选择推理参数

推理参数
- model 模型选择，前面已介绍过。
- temperature 分了的时候要设置 temperature=0。正值会对补完结果添加随机性，对于创意性任务是有帮助的，但是对于分类这种确定性任务是有害的。
- max_tokens 
  - 如果使用单个token的标签，则需要设置 max_tokens=1
  - 如果使用多token的标签，则应设置为最长的那个标签的长度。
- stop
  - 如果标签长度不一，在补完的后面加上一个**停止序列**，比如“END”。然后在推理调用中设置 `stop='END'` 以免模型在补完标签之后还在不断地生成，如前面例子中的“`burger -> edible edible edible`”的情况。
  - 另一个选择是进行**后处理**，遍历补完的结果，寻找其匹配的标签。
- logit_bias
  - 如果使用单token标签，可以设置`logit_bias={“label1”: 100, “label2”:100, …}`，这里的“`label1`”指代的就是具体的标签。
  - 对于训练数据较少或者标签比较复杂的任务，模型可能会输出一些臆想的训练集中没有出现过的标签。`logit_bias`通过提升标签token的权重来避免非法的标签token的产生。
  - 如果将其与**多token标签**一起使用，那就要额外注意 标签是如何切分为token的，因为logit_bias仅对单个token起效，而非序列。
  - Logit_bias还可以用于设置特定标签的偏度，让出出现得更多或是更少。
- logprobs 获取每个标签的概率对于计算信心分数、召回精度等都有很大的帮助。
  - 设置logprobs=5，对于补完的每一个token位置上都会返回5个最有可能的token，以及其对应概率的自然对数。如果要得到其概率，需要使用自然常数求幂。这里返回的概率无关乎temperature参数，表示的是当temperature=1的时候表现出来的概率。
- echo
  - 如果某个标签的概率没有出现在结果列表中，echo参数就能派上用场了。如果echo设置为True且logprobs设置为一个数字，API的返回中就会纳入每个token的概率，不仅是补全的token，还有提示词中的token。所有，为了得到某个特定标签的概率，可以把这个标签纳入提示词中，再调用API，参数为echo=True，lobprobs=0并且max_tokens=0

#### 高级技巧

##### 增加推理步骤

对于需要推理的复杂任务，一个有用的技巧是在最后的答案之前加入推理步骤。给模型一些额外的时间和空间来大声思考，可以提升其获得正确答案的概率。

尽管一提到给众多例子写解释就有点令人发怵，但是你可以使用大语言模型来写这些解释。2022年Zelikman, Wu, et al. 的论文中提出了一个叫做STaR（自教授推理）的过程，其中使用少量样本的提示词，从{问题，答案}的数据集来生成一组{问题，**推理**，答案}的数据集。

![](https://pic4.zhimg.com/80/v2-c6dbe583128343a6f3b9b82bc5d35087_1440w.webp)

##### 精调一个已经精调过的模型

模型可以依次精调任意次数。有一种使用方法是，现在大量相关文本上（非结构化的领域文本或类似的分类结果）预训练模型，然后再在你想让模型完成的特定任务上精调一些案例。这个过程可能像下面这样：

-   步骤一：在大量廉价且相关的数据上精调
  -   非结构化领域文本，比如法律或医疗文本
  -   类似的任务数据，比如另一个大型的分类数据集
-   步骤二：在昂贵的标签化例子上精调
  -   比如，高质量文本或分类结果

![](https://pic4.zhimg.com/80/v2-4bbcc197fb560d686fe826aafc51f1eb_1440w.webp)

如果要精调一个已经精调过的模型，在创建精调任务的时候传入前面精调过的模型名字，其它参数不用改变。如果你的训练数据集要远小于之前的训练数据，那可能就需要将learning_rate_multiplier除以2到4。

#### 常见问题

精调文本分类过程中最常见的问题都和训练数据有关。

##### 常见问题一：缺少专用训练数据

一定要记住，训练数据不仅仅是从输入到答案之间的映射配对，更关键的是输入中需要包含足够的信息来推导出正确答案。

考察下面的训练数据：
- ![](https://pic2.zhimg.com/80/v2-f7a3d15a1fcf3db5a34211e5b3c77625_1440w.webp)

如果不知道这些学生为什么得到对应的分数，模型也就无法从中学习，更加没法判断Esmeralda的成绩是多少。

尤其是当大部分信息都有了，但是仍缺少一些信息的时候，会发生一些比较微妙的问题。比如我们要判断某一项费用是允许还是不允许，这取决于日期、地点或员工类型，那就要确保输入中包含了这些信息，不然就会像下面这样：
- ![](https://pic3.zhimg.com/80/v2-b38b262ea64f4cc2892a1a6c874166ce_1440w.webp)

##### 常见问题二：输入数据的格式不符合训练数据格式要求

当使用精调过的模型的时候，确保你提交的提示词格式和训练数据是一样的。

![](https://pic2.zhimg.com/80/v2-eb64ab96452799467e63339e2ea53c71_1440w.webp)

##### 更多案例

真实一致分类器
- ![](https://pic3.zhimg.com/80/v2-371d1eb0cc05046614b5cc1e30c589d2_1440w.webp)

情感分类器
- ![](https://pic3.zhimg.com/80/v2-f2ef85f6cd70357d67dae91e4a0fc602_1440w.webp)

邮件优先级分类
- ![](https://pic1.zhimg.com/80/v2-5aa8095f9463da2718316274fe5d7df8_1440w.webp)

逻辑关系检测器
- ![](https://pic3.zhimg.com/80/v2-6bf86b43dcdf3d65f422918a66ad6142_1440w.webp)


### GPT-3.5 Turbo 微调 -- 新: /v1/fine_tuning/jobs

【2023-8-23】[OpenAI 开放 GPT-3.5 Turbo 微调，网友：将 prompt 减少 90% 才实惠 ](https://www.infoq.cn/article/3le2VX8uRPBOllXeoTKz)
- 8月22日，OpenAI [宣布](https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates)企业现在可以使用自己的数据对 `GPT-3.5 Turbo` 进行**微调**，在原[Fine-tunes](https://platform.openai.com/docs/guides/fine-tuning)的基础上推出 Fine-tuning. OpenAI 声称最终的定制模型可以赶上甚至超过 GPT-4 执行某些任务的能力。
  - 2024年1月4日弃用旧版 `/v1/fine_tuning` API。建议所有用户迁移到新的API `/v1/fine_tuning/jobs` 
- [fine-tuning api](https://platform.openai.com/docs/api-reference/fine-tuning), [forum](https://community.openai.com/t/gpt-3-5-turbo-fine-tuning-now-available-and-new-gpt3-models/327425)
- <span style='color:red'>传入和传出微调 API 的数据归客户所有， OpenAI或任何其他组织不会使用这些数据来训练其他模型</span>。
- 今年秋天 OpenAI 将开放更先进的 GPT-4。

With this launch, developers can now run **supervised fine-tuning** to make this model perform better for their use cases.

Since the release of GPT-3.5 Turbo, developers and businesses have asked for the ability to customize the model to create unique and differentiated experiences for their users. With this launch, developers can now run supervised fine-tuning to make this model perform better for their use cases.

In our private beta, fine-tuning customers have been able to meaningfully improve model performance across common use cases, such as:
- Improved steerability: Fine-tuning allows businesses to make the model follow instructions better, such as making outputs terse or always responding in a given language. For instance, developers can use fine-tuning to ensure that the model always responds in German when prompted to use that language.
- Reliable output formatting: Fine-tuning improves the model's ability to consistently format responses—a crucial aspect for applications demanding a specific response format, such as code completion or composing API calls. A developer can use fine-tuning to more reliably convert user prompts into high-quality JSON snippets that can be used with their own systems.
- Custom tone: Fine-tuning is a great way to hone the qualitative feel of the model output, such as its tone, so it better fits the voice of businesses’ brands. A business with a recognizable brand voice can use fine-tuning for the model to be more consistent with their tone.

In addition to increased performance, fine-tuning also enables businesses to shorten their prompts while ensuring similar performance.  Fine-tuning with GPT-3.5-Turbo can also handle 4k tokens—double our previous fine-tuned models. Early testers have reduced prompt size by up to 90% by fine-tuning instructions into the model itself, speeding up each API call and cutting costs.

Fine-tuning is most powerful when combined with other techniques such as prompt engineering, information retrieval, and function calling. Check out our fine-tuning guide to learn more. Support for fine-tuning with function calling and gpt-3.5-turbo-16k will be coming later this fall.

#### finetune 功能

如果想缩短示例中重复**指令或提示**,节省成本，请记住:
- 模型可能会表现得像包含了这些指令一样，并且推理时可能不会忽略那些“内置”指令
- 训入指令/提示需要更多示例，供模型学习

If you would like to shorten the instructions or prompts that are repeated in every example to save costs, keep in mind that the model will likely behave as if those instructions were included, and it may be hard to get the model to ignore those "baked-in" instructions at inference time；It may take **more training examples** to arrive at good results, as the model has to learn entirely through demonstration and **without** guided instructions.

建议场景
- 设置回复风格、基调、格式、语言等
- 增强产生预期输出的**可靠性**
- **纠正**未能遵循复杂 Prompt 的问题
- 以特定方式处理许多**边缘情况**
- 执行**Prompt中难以阐明**的新技能或任务
- 通过 GPT4 completion结果Fine-tuning过的GPT-3.5-turbo模型，在特定场景下可以达到GPT4一样的效果，增加响应**速度**以及降低使用成本（特定领域高效的小模型）

开发者通过监督微调，可以实现个性化定制，适配各自业务场景，显著提高模型性能
- 更加**可控**：更好的遵循指令，如 精简回复、以特定语言风格。（不必再在prompt中强调用某种语言）
- **输出格式**更可靠：微调提升了模型回复的一致性，适用于要求特定格式输出的情形（代码补全/组合API调用/json输出）
- **角色定义**：微调让模型输出更加贴合某种角色，如 企业品牌代言人

除了性能提升，微调还能缩短 prompt 长度，同时保持效果。GPT-3.5-Turbo 微调版能处理 4k tokens（之前模型的两倍）. 早期测试发现，通过监督指令微调，prompt长度最多缩减 90%，api调用加速，削减成本。

GPT 的“微调”与 Llama2 之类的微调不同，因为不会调整网络的所有权重，只是会调整网络小部分。代价是 OpenAI 微调的成本较低，但功能也没有“真正的”微调强大。

GPT-3.5 Turbo 微调可处理 4k 个 tokens——可达之前微调模型的 2 倍。早期测试人员还对模型本身的**指令**进行了微调，从而将提示词长度缩短达 **90%**，成功加快每次 API 调用的速度并降低了执行成本。


#### finetune 成本

微调成本分为两个部分：初始**训练**成本与**使用**成本：
- 训练成本：0.008 美元/1K tokens
  - 计算公式： cost = 每1k字符费用 * 数据集tokens数 * 训练轮数（epoch）
  - gpt-3.5-turbo 微调作业中包含 10 万个 token 的训练文件。经过 3 个 epoch 训练轮次，预计成本为 2.40 美元。
  - 注意：验证集也在收费范围内
- 使用成本
  - 输入：0.012 美元/1K tokens
  - 输出：0.016 美元/1K tokens
  - 成本预估：[Cost Estimation](https://cookbook.openai.com/examples/chat_finetuning_data_prep)

|Model|Base Models-Input|Base Models-Output|Fine-tuned Models-Training|Fine-tuned Models-Input|Fine-tuned Models-Output|
|---|---|---|---|---|---|
|`babbage-002`|0.0004|0.0004|0.0004|0.0016|0.0016|
|`davinci-002`|0.002|0.002|0.006|0.012|0.012|
|`gpt-3.5-turbo-4k`|`0.0015`|`0.002`|0.008|`0.012`|`0.016`|
|`gpt-3.5-turbo-16k`|0.003|0.004|-|-|-|
|`gpt-4-8k`|0.03|0.06|-|-|-|
|`gpt-4-32k`|0.06|0.12|-|-|-|

注
- 单位 $/1k tokens
- [官方收费指南](https://openai.com/pricing)

微调的 GPT 3.5 Turbo 生成成本是基本模型生成成本的 **8 倍**，因此必须处于 OpenAI 提到的“<span style='color:red'>将提示大小减少 90%</span>”的范围内，才能从中获得成本效益。
- 初版 GPT-3 基础模型（ada、babbage、curie 和 davinci）微调 将于 2024 年 1 月 4 日正式关闭。
- OpenAI 如今发布了 babbage-002 和 davinci-002 作为这些模型的替代方案，用户可将其用作基础模型或微调模型。这些模型可以使用新 API 端点/v1/fine_tuning/jobs 进行微调。


#### finetune 原理

【2023-8-24】[GPT-3.5 微调 API重磅发布：有史以来规模最大的 LoRA 即服务](https://mp.weixin.qq.com/s/GIIzEwRzXxkAffPDjtvvaw)


【2023-10-25】[资讯](https://www.toutiao.com/article/7206135282402427444) 推测出可能使用的一些技术：
- `Adapter`技术：Adapter是一种**轻量级**的神经网络组件，可在不影响原有模型效果的情况下，增加模型的新能力。
  - 通过在原有模型的某些层中插入Adapter，可以使原有模型具备处理特定任务的能力。
  - 好处是可以避免为每个用户都创建一个单独的模型，节省了存储和计算资源。
  - 关于Adapter技术在GPT-3.5这么大规模的模型上的有效性，目前尚无明确的研究结果。但是在一些小规模的实验中，Adapter技术已经被证明可以有效地提升模型的性能。
- `Prompt tuning`技术：Prompt tuning是一种针对GPT模型的fine-tuning方法，目的是让模型更加适应特定任务。
  - 用户提供一些提示文本（prompt），对模型进行fine-tuning，使得模型能够更好地生成与提示文本相关的文本。
  - 这种方法也可以用来针对**特定用户或任务**进行fine-tuning。
  - Prompt tuning技术在NLP任务已经广泛应用，并且取得了不错的效果。
  
因此，推测OpenAI在开发GPT-3.5 fine-tune API时可能采用了这些技术

LoRA：英文全称 Low-Rank Adaptation of Large Language Models，大语言模型的低阶适应，微软研究人员为解决大语言模型微调而开发的一项技术。
- 冻结预训练的模型权重参数, 每个Transformer块里注入可训练层，由于不需要对模型的权重参数重新计算梯度，所以大大减少了需要训练的计算量。

研究发现: LoRA的微调质量与全模型微调相当

LoRA-as-a-service： LoRA 即服务。
- 这种模式类似于“软件即服务”（Software-as-a-Service，SaaS）或其他类似的服务模式，其中用户不需要自行部署和管理软件或技术，而是通过云服务提供商获得对其功能和服务的访问权

#### 数据要求

注意
- 单个训练文件<span style='color:red'>最大 50 MB</span>
- 一行数据是完整的json字符串，<span style='color:red'>最大token数目 4096，超出就截断</span>
  - 如何计算token数？[counting tokens notebook](https://cookbook.openai.com/examples/How_to_count_tokens_with_tiktoken.ipynb)
- <span style='color:red'>最少训练条数：10</span>，一般**50-100条**就有提升，因场景而已
  - 推荐先用50条数据实验，如果正向再扩充数据量，否则，优化问题定义
- 数据较少时，将效果好<span style='color:red'>system prompt放到训练数据中</span>
  - 数据：<span style='color:red'>质量 > 数量</span>
- 数据可分为：训练集、测试集，分开上传，便于观测模型效果


```py
# 上传数据
!openai tools fine_tunes.prepare_data -f sport2.jsonl -q
```

#### finetune 流程

【2023-10-8】OpenAI [finetune功能](https://platform.openai.com/finetune)增加微调界面, 不用写代码
1. 用户友好性增强：没有技术背景的用户也能够轻松地使用微调功能，简化模型微调过程。
2. 更广泛的应用：企业和个人用户可以更方便地微调模型，使其更适应特定的应用。
3. 节省时间和努力：由于不需要编写代码，用户可以更快地开始和完成微调作业。
4. 提供**即时反馈**：通过“Successful”和“Failed”选项卡，用户可以即时知道他们的微调作业状态，帮助他们根据需要进行调整。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-ezhpy3drpa/dee03f996c2142059087c5a8e5a11581~tplv-obj:1920:992.image?_iz=97245&from=post&x-expires=1704585600&x-signature=d99HlpR85aG%2BTTkWvG8rcftSnxA%3D)


微调实战
- 参考: [openai 3.5微调实战](https://github.com/LearnPrompt/LLMs-cookbook/tree/main/gpt3.5)
- 微调 `gpt-3.5-turbo-0613` 模型，**10条**数据（289个汉字，**5769**个字节），花费 0.16 刀; 按照 0.008 单价算，大概训练了3轮
- 数据示例：医疗监督问答数据集 [huatuo26M-testdatasets](https://huggingface.co/datasets/FreedomIntelligence/huatuo26M-testdatasets), 或去 [github](https://github.com/LearnPrompt/LLMs-cookbook/blob/main/gpt3.5/test_datasets.jsonl)找

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-08-29T13:15:51.115Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;UVFE8uh0TtQpR3knby8f\&quot; version=\&quot;21.6.8\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;YUrH7kkdw6S7EPocWAtV\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1434\&quot; dy=\&quot;771\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;dashed=1;dashPattern=1 1;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;340\&quot; y=\&quot;90\&quot; width=\&quot;350\&quot; height=\&quot;190\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CRyWcW9bKPYmjVe2kgWn-2\&quot; value=\&quot;ChatGPT 微调流程\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=0;fontSize=18;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;335\&quot; y=\&quot;10\&quot; width=\&quot;180\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-43\&quot; value=\&quot;2023-8-29&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;550\&quot; y=\&quot;290\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-6\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B3B3B3;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;N5nvKO04K80Mb7aMBe0Y-24\&quot; target=\&quot;N5nvKO04K80Mb7aMBe0Y-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;537.5999999999999\&quot; y=\&quot;198\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-1\&quot; value=\&quot;GPT-3.5 Turbo\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490\&quot; y=\&quot;100\&quot; width=\&quot;95\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-7\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B3B3B3;entryX=0;entryY=0;entryDx=0;entryDy=12.5;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;N5nvKO04K80Mb7aMBe0Y-3\&quot; target=\&quot;N5nvKO04K80Mb7aMBe0Y-8\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-3\&quot; value=\&quot;监督语料\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;160\&quot; y=\&quot;115\&quot; width=\&quot;60\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-5\&quot; value=\&quot;GPT-3.5 Turbo Finetune\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490\&quot; y=\&quot;225\&quot; width=\&quot;95\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-16\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=2;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;N5nvKO04K80Mb7aMBe0Y-8\&quot; target=\&quot;N5nvKO04K80Mb7aMBe0Y-24\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;516.25\&quot; y=\&quot;183\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-8\&quot; value=\&quot;个人语料\&quot; style=\&quot;shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;darkOpacity=0.05;darkOpacity2=0.1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;370\&quot; y=\&quot;130\&quot; width=\&quot;84\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-10\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=2;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;N5nvKO04K80Mb7aMBe0Y-9\&quot; target=\&quot;N5nvKO04K80Mb7aMBe0Y-3\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-11\&quot; value=\&quot;① 准备语料\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;N5nvKO04K80Mb7aMBe0Y-10\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.1467\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;39\&quot; y=\&quot;-3\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-21\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#97D077;strokeWidth=2;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;N5nvKO04K80Mb7aMBe0Y-9\&quot; target=\&quot;N5nvKO04K80Mb7aMBe0Y-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;240\&quot; y=\&quot;275\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-9\&quot; value=\&quot;\&quot; style=\&quot;shape=actor;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;175\&quot; y=\&quot;220\&quot; width=\&quot;30\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-12\&quot; value=\&quot;② 上传语料到OpenAI\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;280\&quot; y=\&quot;125\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-13\&quot; value=\&quot;OpenAI\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;470\&quot; y=\&quot;60\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-15\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B3B3B3;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;N5nvKO04K80Mb7aMBe0Y-1\&quot; target=\&quot;N5nvKO04K80Mb7aMBe0Y-24\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;538\&quot; y=\&quot;140\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;537.5999999999999\&quot; y=\&quot;168\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-17\&quot; value=\&quot;③ 启动微调\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;590\&quot; y=\&quot;175\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-18\&quot; value=\&quot;④ 邮件通知任务完成&amp;lt;br&amp;gt;(返回模型名)\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;610\&quot; y=\&quot;220\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;19\&quot; y=\&quot;4\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-19\&quot; value=\&quot;⑤ 调用新模型\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;300\&quot; y=\&quot;260\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-23\&quot; value=\&quot;jsonl格式&amp;lt;br&amp;gt;{&amp;quot;message&amp;quot;:{&amp;quot;role&amp;quot;:&amp;quot;&amp;quot;,&amp;quot;content&amp;quot;:&amp;quot;&amp;quot;}}&amp;lt;br&amp;gt;{&amp;quot;message&amp;quot;:{&amp;quot;role&amp;quot;:&amp;quot;&amp;quot;,&amp;quot;content&amp;quot;:&amp;quot;&amp;quot;}}&amp;lt;br&amp;gt;{&amp;quot;message&amp;quot;:{&amp;quot;role&amp;quot;:&amp;quot;&amp;quot;,&amp;quot;content&amp;quot;:&amp;quot;&amp;quot;}}\&quot; style=\&quot;shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor=#fff2cc;strokeColor=#d6b656;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;140\&quot; y=\&quot;40\&quot; width=\&quot;190\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-24\&quot; value=\&quot;\&quot; style=\&quot;shape=image;html=1;verticalLabelPosition=bottom;verticalAlign=top;imageAspect=0;image=img/clipart/Gear_128x128.png\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;517.5\&quot; y=\&quot;156.5\&quot; width=\&quot;40\&quot; height=\&quot;53\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;N5nvKO04K80Mb7aMBe0Y-25\&quot; value=\&quot;生成语料id\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;411\&quot; y=\&quot;118\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


完整版: [知乎](https://zhuanlan.zhihu.com/p/653239407?), [公众号](https://mp.weixin.qq.com/s?__biz=MjM5ODY2OTQyNg==&mid=2649769352&idx=1&sn=e68c0ae1d3b2b1af8aeb3ace58f811e0&chksm=bec3d89589b45183f626a37b4c345254c527f0b68fb301e6e9abb88d6d78b2418697f534f049&token=622259072&lang=zh_CN#rd)

#### ① 数据处理

将jsonl格式（每行都是json串的文本文件）的数据（question, answer两个字段）转换为OpenAI要求的格式

官方 分类场景 [jupyter notebook示例](https://cookbook.openai.com/examples/fine-tuned_classification)

```py
import pandas as pd

labels = [sports_dataset.target_names[x].split('.')[-1] for x in sports_dataset['target']]
texts = [text.strip() for text in sports_dataset['data']]
df = pd.DataFrame(zip(texts, labels), columns = ['prompt','completion']) #[:300]
df.head()
# -------------
# pandas 直接保存为jsonl格式
df.to_json("sport2.jsonl", orient='records', lines=True)
```


第三方提供版本

```py
# 数据处理
import json
import random

def transform_jsonl(input_file_path, output_file_path):
    entries = []
    with open(input_file_path, 'r') as file:
        for line in file:
            entry = json.loads(line)
            entries.append(entry)
    # 随机抽取100个条目
    #sampled_entries = random.sample(entries, 100)
    sampled_entries = random.sample(entries, 10) # 至少10条数据

    with open(output_file_path, 'w') as outfile:
        for entry in sampled_entries:
            messages = []
            messages.append({"role": "system", "content": "You are an assistant"})
            user_message = {"role": "user", "content": entry["questions"]}
            assistant_message = {"role": "assistant", "content": entry["answers"]}
            messages.extend([user_message, assistant_message])
            result = {"messages": messages}
            json.dump(result, outfile, ensure_ascii=False)
            outfile.write('\n')

input_file_path = '~/test_datasets.jsonl' # 请替换为您的输入JSONL文件路径
output_file_path = '~/tmp.jsonl' # 请替换为您想要保存的输出JSONL文件路径
transform_jsonl(input_file_path, output_file_path)
```

数据示例：

```json
输入: {"questions": "做了腰间盘穿丁手术后，用盐泡脚可以吗", "answers": "问题分析：你好:你是由于身体出现了一些局部的腰部损伤这种情况应该进行调整的一般术后泡脚是可以的，不用担心。意见建议：治疗方案:你可以不知后注意休息，避免劳累过度就可以这种调整方法也可以住进你身体的一些嗯调理的啊！"}
输出: {"messages": [{"role": "system", "content": "You are an assistant that occasionally misspells words"}, {"role": "user", "content": "由于一次事故造成了左耳的残疾听力不是很好需要佩戴助听器戴上的效果还不错能和人正常交流但是最近一个月助听器里面总是有杂音影响了使用效果。耳聋佩戴的助听器有杂音怎么办？（）"}, {"role": "assistant", "content": "你好您所谓的杂音也有可能是听到的环境声音好的助听器对噪音是有压缩的出现这种情况是可以调试解决的如果是一般的助听器因为环境声音也同时放大了可能会觉得比较吵您的问题最好是到助听器店让专业的验配师帮您处理"}]}
// 官方数据示例
{
  "messages": [
    { "role": "system", "content": "You are an assistant that occasionally misspells words" },
    { "role": "user", "content": "Tell me a story." },
    { "role": "assistant", "content": "One day a student went to schoool." }
  ]
}
```


#### ② 上传文件


```sh
curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "purpose=fine-tune" \
  -F "file=@path_to_your_file" 

# ------ 第三方  ----
curl --location 'https://api.openai.com/v1/files' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  --form "purpose=fine-tune" \
  --form "file=@path_to_your_file" 
```

以上方法失效，错误信息
> The browser (or proxy) sent a request that this server could not understand.

python
- 【2023-9-20】升级文件上传代码

```py
import os
import openai

#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

data_file = "your_file"
#data_file = val_file
openai.File.create(
  file=open(data_file, "rb"),
  user_provided_filename=data_file.split('/')[-1], # 自定义上传后的文件名，如 采用原文件名称（按/分割）
  purpose='fine-tune' # 固定，不能改
)
print('上传的文件信息: ', openai.File.list())
```

```py
# 上传至OpenAI
import requests
import openai

OPENAI_API_KEY='***'
url = "https://api.openai.com/v1/files"
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}
payload = {
    "purpose": "fine-tune",
}
print('数据路径: ', output_file_path)
files = {
    "file": open(output_file_path, "rb")
}

response = requests.post(url, headers=headers, data=payload, files=files)
print(response)
print('上传的文件信息: ', openai.File.list())
```

执行完毕后返回 文件列表

```json
上传的文件信息:  {
  "object": "list",
  "data": [
    {
      "object": "file",
      "id": "file-***",
      "purpose": "fine-tune",
      "filename": "tmp.jsonl",
      "bytes": 5769,
      "created_at": 1693304216,
      "status": "uploaded",
      "status_details": null
    },
    {
      "object": "file",
      "id": "file-****",
      "purpose": "fine-tune",
      "filename": "tmp.jsonl",
      "bytes": 1496,
      "created_at": 1693303804,
      "status": "processed",
      "status_details": null
    }
  ]
}
```

从中找到 本次上传文件 位置，如下标0, 或1

文件信息格式化，时间戳转换，便于查找

```py
from datetime import datetime
import pandas as pd

def timestamp2str(ts):
    cur_date = datetime.fromtimestamp(ts)
    local_date_str = datetime.strftime(cur_date ,'%Y-%m-%d %H:%M:%S')
    return local_date_str
    
df_file = pd.DataFrame(openai.File.list()['data'])
df_file['time'] = df_file['created_at'].map(timestamp2str) # 时间戳转str
df_file.sort_values('time') # 按时间排序
```


#### ③ 启动微调任务

openai 工具包

```sh
# 启动分类评测指标
openai api fine_tunes.create -t "sport2_prepared_train.jsonl" -v "sport2_prepared_valid.jsonl" --compute_classification_metrics --classification_positive_class " baseball" -m ada
# 下载微调评估结果
!openai api fine_tunes.results -i ft-2zaA7qi0rxJduWQpdvOvmGn3 > result.csv
results = pd.read_csv('result.csv')
results[results['classification/accuracy'].notnull()].tail(1)
```

使用官方默认参数

```sh
curl https://api.openai.com/v1/fine_tuning/jobs \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
-d '{
  "training_file": "TRAINING_FILE_ID",
  "model": "gpt-3.5-turbo-0613"
}'
```

自定义参数
- 指定验证集
- 设置前缀
- 设置训练参数，如 epoches

超参优化
- 刚开始不用指定epoch，OpenAI自行设置，根据测试数据自行调整：
- 如果没有遵循指令，增加1-2个epoch
- 如果多样性低于预期，减少1-2个epoch


```sh
# ------ 第三方: 自定义训练参数  ----
curl --location 'https://api.openai.com/v1/fine_tuning/jobs' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  --data '{
    "training_file": "file-****", // 训练集
    "validation_file": "file-****", // 测试集
    "hyperparameters":{
      "n_epochs":7
    },
    "suffix":"cutom-model-name", // 自定义模型前缀
    "model":"gpt-3.5-turbo-0613"
  }'

```


模型选择

```py
# 启动微调
import requests

OPENAI_API_KEY="sk-***"

url = "https://api.openai.com/v1/fine_tuning/jobs"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

data = { 
    #"training_file": "file-XXXXXXXXXXX",
    "training_file": openai.File.list()['data'][1]['id'],
    "model": "gpt-3.5-turbo-0613"
}

response = requests.post(url, headers=headers, json=data)
print(response.text)
```

终端返回

```json
{"object":"fine_tuning.job","id":"ftjob-***","model":"gpt-3.5-turbo-0613","created_at":1693304550,"finished_at":null,"fine_tuned_model":null,"organization_id":"org-LMrR8ZVsnE2MLQNXje4rARHo","result_files":[],"status":"created","validation_file":null,"training_file":"file-bPzn6eE00cvR3xNqb8lau6QN","hyperparameters":{"n_epochs":10},"trained_tokens":null}
```

#### 任务控制

**获取**训练信息

```sh
curl https://api.openai.com/v1/fine_tuning/jobs/ft-**** \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
```

**取消**训练任务

```sh
curl https://api.openai.com/v1/fine_tuning/jobs/ft-****/cancel \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
```

查看训练进度

```sh
curl https://api.openai.com/v1/fine_tuning/jobs/ft-****/events \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
```


稍等片刻后，查看个人邮箱，记录新模型名

```sh
curl https://api.openai.com/v1/fine_tuning/jobs \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
-d '{
  "training_file": "TRAINING_FILE_ID",
  "model": "gpt-3.5-turbo-0613"
}'
```

对应的Python指令

```py
# List 10 fine-tuning jobs
openai.FineTuningJob.list(limit=10)
# Retrieve the state of a fine-tune
openai.FineTuningJob.retrieve("ft-abc123")
# Cancel a job
openai.FineTuningJob.cancel("ft-abc123")
# List up to 10 events from a fine-tuning job
openai.FineTuningJob.list_events(id="ft-abc123", limit=10)
# Delete a fine-tuned model (must be an owner of the org the model was created in)
openai.Model.delete("ft-abc123")
```

#### ④ 使用微调模型

openai 工具包

```py
test = pd.read_json('sport2_prepared_valid.jsonl', lines=True)
test.head()

ft_model = 'ada:ft-openai-2021-07-30-12-26-20'
res = openai.Completion.create(model=ft_model, prompt=test['prompt'][0] + '\n\n###\n\n', max_tokens=1, temperature=0)
res['choices'][0]['text']
# 获取输出概率
res = openai.Completion.create(model=ft_model, prompt=test['prompt'][0] + '\n\n###\n\n', max_tokens=1, temperature=0, logprobs=2)
res['choices'][0]['logprobs']['top_logprobs'][0]

```


查看已有finetune任务

```sh
curl https://api.openai.com/v1/fine_tuning/jobs?limit=2&after=1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
```

看下新模型效果

```py
# 调用模型
import requests

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}
# 从邮件里提取模型名称
new_model = 'text-davinci-003'
new_model = "gpt-3.5-turbo"
new_model = 'ft:gpt-3.5-turbo-0613:***'
data = {
    "model": new_model,
    "messages": [
        {
            "role": "system",
            "content": "You are an assistant"
        },
        {
            "role": "user",
            "content": "我在体检是正常的，但是去献血医生最是说我的血压高，不能献。血压是130、80这是为什么呢？"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.text)
```

返回结果

```json
{
  "id": "chatcmpl-****",
  "object": "chat.completion",
  "created": 1693305795,
  "model": "ft:gpt-3.5-turbo-0613:***",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "可能的原因如下： 1、在献血时会有一些紧张，紧张会使血压升高。有的人可能并不是很紧张，但献血起码是一个小手术。 2、在献血之前会对献血者进行初检，其中就包括血压测量。如果血压较高，就不准献血。 3、在献血后有可能会感到血压低，因为抽取的是血浆，造成血容量减低，心排血量减少，以后体中的血压降落。 4、如果一直测得较高，就是高血压，应引诱病院。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 73,
    "completion_tokens": 219,
    "total_tokens": 292
  }
}
```


效果对比

question: 
> 我在体检是正常的，但是去献血医生最是说我的血压高，不能献。血压是130、80这是为什么呢？

Answer

**gpt-3.5**

> 血压读数130/80是较常见的健康血压范围内，但是具体的献血要求可能略有不同，医生可能基于献血的特殊需求或个人身体状况，选择较为严格的标准。以下是一些可能导致您不能献血的原因：
>1. 个人差异: 献血机构可能设定了较为严格的血压标准，以确保献血者的安全和健康。即使您的血压读数在正常范围内，但慎重考虑您的个人特殊情况或家族病史等因素也很重要。
>2. 动态血压: 血压是一个动态指标，受多种因素影响，如情绪、活动水平、环境等。可能您的血压在体检时正常，但在献血前被测量时升高。
>3. 紧张或焦虑: 对一些人来说，献血过程本身可能会引发一些紧张和焦虑，这可能会导致血压升高。这些情绪因素可能会影响到医生的判断。
> 
> 如果您对不能献血的原因有任何疑问，我建议您咨询相关医生或献血机构的工作人员，他们可以给您更具体的解释和指导。另外，您的血压读数仍然在健康范围内，您可以继续关注并保持良好的生活习惯，有助于保持健康的血压水平。

**finetune**

> 可能的原因如下： 
>- 1、在献血时会有一些紧张，紧张会使血压升高。有的人可能并不是很紧张，但献血起码是一个小手术。 
>- 2、在献血之前会对献血者进行初检，其中就包括血压测量。如果血压较高，就不准献血。 
>- 3、在献血后有可能会感到血压低，因为抽取的是血浆，造成血容量减低，心排血量减少，以后体中的血压降落。 
>- 4、如果一直测得较高，就是高血压，应引诱病院


简单微调过后不用写prompt也能让gpt-3.5-turbo-0613有更加专业的回复



# 结束