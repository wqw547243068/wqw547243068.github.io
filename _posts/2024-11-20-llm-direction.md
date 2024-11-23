---
layout: post
title:  LLM 发展方向
date:   2024-11-20 12:00:00
categories: 大模�?
tags: gpt LLM 大模�? AGI 世界模型 系统 快思�? 慢思�? 灾难 遗忘 幻觉 推理  可解�?   norm 大脑 json 缩放定律 鹦鹉 意识 o1 ttt
excerpt: 大模型会往哪个方向发展�?
mathjax: true
permalink: /llm_direction
---

* content
{:toc}


# LLM 优化方向


�?2023-6-16】知乎专题：[大模型LLM领域，有哪些可以作为学术研究方向？](https://www.zhihu.com/question/595298808/answer/3071907155)

- **模型�?**�?
  - GPT系列，多模态系列，视觉类SAM：原生的工具调用能力�?
  - 安全性：加密，可信任，联邦学习；
  - 新模型，新范式：长文本建模，不需要RLHF等；
  - 涌现问题的研究、黑盒的研究�?
  - 并行、运算、显存的优化。EL-Attention，ZeRo，剪枝部署，蒸馏压缩�?
- **接口�?**�?
  - 私有化部署；
  - Adapter，prefix，Lora�?
  - Fusing�?
- **应用�?**�?
  - Visual ChatGPT，HuggingGPT，AutoGPT，LangChain�?
  - Prompt工程，向量库，dense retrieval�?
  - 自我纠错，自我迭代，chain of thought 加强�?
  - 评测数据集、新时代下的新任务，generatice agents�?

假设已经�? GPT-3.5 基础模型，一千张卡，思考能做什么？然后用小模型，比如LLaMa 7B去验证，如果成功，再慢慢加大�?13B�?30B，画出一条上升的曲线；不一定要scale到最大的模型，只要自己的结论能划出一条上升的曲线，那么这条曲线就可外推到更大�?

源自知乎：[LessTalk](https://www.zhihu.com/question/595298808/answer/3071907155)

- 平台工具及工程化部署
- 小模型拟合大模型降低计算�?
- 多模态的输入与输�?
- Prompt Engineering
- 垂直领域应用 搜索+知识图谱、机器人、自动驾驶等

提纲
- 基础理论：大模型的基础理论是什么？
- 网络架构：Transformer是终极框架吗�?
- 高效计算：如何使大模型更加高效？
- 高效适配：大模型如何适配到下游任务？
- 可控生成：如何实现大模型的可控生成？
- 安全可信：如何改善大模型中的安全伦理问题�?
- 认知学习：如何使大模型获得高级认知能力？
- 创新应用：大模型有哪些创新应用？
- 数据评价：如何评估大模型的性能�?
- 易用性：如何降低大模型的使用门槛�?

作者：[zibuyu9](https://www.zhihu.com/question/595298808/answer/3047369015)

其它
- reasoning 逻辑推理：目前llm能力还不够的地方。比如能不能让llm做leetcode hard。进一步的，能不能自己创造新的知识，解决哥德巴赫猜想�?
- compression and acceleration 模型压缩与加速：怎么把一�?10b的模型弄到手机上并高速运�?
- agent：怎么更好的给llm加上眼睛与手脚，让llm变成agent执行任务，并构造各种各样全新的benchmark。比如让agent发知乎回答以点赞多为目标。能不能通过RL把这件事做了?就和当年搞游戏ai一样�?
- multi-modal 多模态：GPT-4没有开源，甚至没有技术细节，怎么做一个开源的逼近gpt-4的模型。mini-gpt4, llava是个不错的尝试�?
- Hallucination 幻觉问题：GPT-4已经好了很多，但仍然没有完全解决。所以因此马斯克说要做TruthGPT. 要让LLM知之为知之不知为不知。这个难度其实很大�?
- Evaluation。开源世界需要一套新的Evaluation的方法来评估llm的效果，从而方便推进开源llm的进展�?
- dataset。这个是chatgpt被创造出来的源头。所以，能否多构建一个专家的数据库来帮助优化llm呢？每一份开源数据都非常有价值�?

论文：[A PhD Student’s Perspective on Research in NLP in the Era of Very Large Language Models](https://arxiv.org/pdf/2305.12544.pdf)


## 模型融合

�?2024-8-8】[模型融合来袭！ChatGPT和Claude 杂交能变聪明10倍？](https://mp.weixin.qq.com/s/zUtQrKuQgyNivaxxrHX1hg)

### 什么是模型融合

什么是模型融合�?
- 把多个AI模型的参数混合在一起，生成一个新模型�?

简�?, 但效果却出奇的好
- 不需要额外的数据和算力，只要�?**模型权重**加减一下就行了�?
- 融合后的模型还真能集各家之所长，性能明显提升�?

比如 Prometheus-2 模型用这招把几个评估模型的能力融合到一起的

### 融合方法

常见方法：图见[原文](https://mp.weixin.qq.com/s/zUtQrKuQgyNivaxxrHX1hg)
- **线�?**融合：最简单粗暴，直接对参�?**加权平均**。虽然简单但出奇的有效�?
- **任务向量**：把微调后的模型减去原始模型，得到一�?"任务向量"。用这个向量做加减法，比如减掉有毒内容的任务向量，模型就能生成更干净的内容了�?
- `TIES`融合：在任务向量基础上加了三板斧 - 修剪、选举和分离，可以去掉冗余权重、解决任务向量间的分歧�?
- `DARE`融合：跟TIES思路类似，但用随机丢弃和重新缩放来去掉冗余权重�?

论文链接�?
- 任务向量：[paper](https://arxiv.org/abs/2212.04089)
- TIES：[paper](https://arxiv.org/abs/2306.01708)
- DARE：[paper](https://arxiv.org/abs/2311.03099)
- 嵌入向量融合：[paper](https://arxiv.org/abs/1912.00772)

工具 mergekit�?
- [merge-models](https://huggingface.co/blog/mlabonne/merge-models)


### GaC

Gac: Generation as Classification

�?2024-6-18】上海AI Lab 推出 [融合多个大模型新思路 --- Generation as Classification](https://zhuanlan.zhihu.com/p/715404265)

常打比赛的人(如Kaggle)很熟�?, 很多时候拼的就是各�?**花式模型融合**, 将多个model融合(ensemble)后可以突破现有瓶�?, 神奇地让融合后的性能超过任何一个参与ensemble的单一模型�?

ImageNet 视觉分类任务, 分类模型会输出一个维度为 1000 向量代表预测每个类别的概率，仅仅将多个模型的分类向量加起来后取平�?, 就可以取得不错的准确率提�?
- 原本最高的�? RepGhostNet 78.81%, 将三个模型融合后就提升到�? 80.62%. 

类似�?, 把LLM每个generation step都当成一次分类任�?(Generation as Classification, GaC)去ensemble, 从而提升所生成的每个token的正确�?, 并最终获得更�? response.

核心思想: LLM生成文本�?, 每个generation step都由多个LLM共同决定下一个token要输出什�?
- ![](https://pica.zhimg.com/80/v2-e8c84b1cf0e391ffe40b2a9fe2fc966a_1440w.webp)
- Paper Title: [Breaking the Ceiling of the LLM Community by Treating Token Generation as a Classification for Ensembling](https://arxiv.org/pdf/2406.12585)
- [GaC](https://github.com/yaoching0/GaC)

如何实施�?

问题
- LLM 每步生成跟其**词汇表等�?**的概率向�?, �? **LLMs 词汇表长度不一�?**
- 比如: 
  - Llama3 词汇表长�? 128256
  - Qwen2  词汇表长�? 152064
- 这和ImageNet分类任务上所有模型都输出1000维度的向量不�?.

直觉做法: 
- 对所有参与ensemble的LLM词汇表取**并集**得到 Vu, 并用**0-1矩阵**记录下原本LLM词汇表和 Vu **对应关系**. 
- 一个generation step�?, 将每个LLM生成�?**概率向量**乘以各自�?0-1矩阵转换�? Vu 维度
- 随后�?**取平�?**并得到ensemble后的概率向量
- 再根据该向量sample出下一个token, 此时这个token就是由所有参与ensemble的LLM决定�?
- 当选出一个token�?, 每个LLM会用各自的tokenizer将这个token转换为各自的 token id(s), 并拼回到各自的输入中以进行下一个generation step.
- ![](https://pic4.zhimg.com/80/v2-007b5f3229ad47a81a4613587dfd4433_1440w.webp)

这种简单做法竟然打破现有的LLM社区天花板！(当然, 花费了更多计算量)
- ![](https://pica.zhimg.com/80/v2-21d29f4a7f9f30cba52ae96330720956_1440w.webp)

Qwen2 �? 2024/06/07 退�?, 拿它和实力相当的 llama3 进行融合, 各个指标上平�?4%的提�?! 达到 2024/06/07开源社区最好结�?

该方法不受模型架构的限制, 随着新模型的释出还是可以不断的以新模型为基础继续推升天花�?.


## 可控生成

�?2023-7-10】[LLM 可控生成初探](https://mp.weixin.qq.com/s/BngY2WgCcpTOlvdyBNJxqA)

基于 LLM 的应用开发过程中，有几个挑战，包括：
- 如何避免“胡说八道�?, 提升模型输出�?**可靠�?/稳定�?**
- 控制模型的计算开销和响应速度等等

目前主流的解决手段包括：
- 更好�? prompt 设计
- 通过 retrieval 来做增强
- 与外部工具的结合
- 流程编排与产品设�?
- 考虑使用 fine tune 模型或混合模型应�?

|Prompt优化类型|latency|compute|
|---|---|---|
|Few-Shot CoT|??|??|
|Zero-Shot CoT|?|?|
|Decomposition|??|??|
|Ensembling|?|????|
|Self-Criticism|????|??|
||||

可控生成最直接的方案：
- 首先通过 prompt 告知 LLM 我们所需要的返回格式，并进行生成�?
- 通过一些规则来检查返回结果，如果不符合格式，生成相关错误信息�?
- 将上一次的生成内容和检查的错误信息告知 LLM，进行下一次的修正生成�?
- 重复 2-3 步骤，直到生成的内容完全符合要求�?

LLM 的可控性、稳定性、事实性、安全性等问题是推进企业级应用中非常关键的问题，下面这些项目在这方面做了很多探索，也有很多值得借鉴的地方�?

总体思路上来说，主要是：
- 提供一�? prompt 模板定义，允许用户指�? LLM 生成的格式或内容主题�?
- 在模板基础上，也有不少项目进一步设计了相应的编程语言，让 LLM 与确定性程序的交互更加直观�?
- 提供各类 validator，保证生成内容符合预期，并且提供了自动处�?/修正机制�?
- 更进一步，也可以在生成前进行干预，例如�? prompt 中给近似案例，修改模�? decode 时的概率分布等�?
- 其它在可控性基础上做的各种性能与开销的优化，例如缓存，减�? token 消耗量，对开源模型能力的挖掘等�?

即使不直接使用上述的项目做开发，也可以从中学习到很多有用的思路。当然也非常期待这个领域出现更多有意思的想法与研究，以及 prompt 与编程语言结合能否碰撞出更多的火花�?

详见原文：[LLM 可控生成初探](https://mp.weixin.qq.com/s/BngY2WgCcpTOlvdyBNJxqA)

### guardrails

guardrails 项目将上述步骤做了进一步的抽象与封装，提供更加 high level 的配置与 API 来完成整个过程。其主要的组成部分包括：
- 定义了一�? RAIL spec，用来描述上面第 1 点提到的返回格式限定。除�? output schema 的定义外，RAIL目前也支�? input schema，prompt 模板，以�? instructions 等其它配置�?
- 提供了一系列�? validation 机制，对应上面的�? 2 点。对�? validate 失败的部分，会保留其�? output schema 中的位置，生成相应的错误信息�?
- 通过 ReAsk 类来实现上面的第 3 点，发送给 LLM 的内容会更聚焦于错误信息部分，且保留了结构，更便�? LLM 理解和处理�?
- 其它像常�? prompt 模板之类的功能�?

### NeMo-Guardrails

NeMo-Guardrails
- 来自 Nvidia 的一个同名项目，�? guardrails 更有野心，想要确�? LLM 应用整体�?**可信�?**�?**无害�?**以及数据**安全�?**等，而不仅仅只是输出的结构化检查和修复�?
- 因此其实现思路上也复杂不少，设计了一种专门的 Colang 语言，来支持更加通用多样的业务流，而不仅仅�?**生成 -> 检�? -> 修复**�?
- 这个项目会更专注于用户与 LLM 的对话式交互应用，主要的设计都是围绕这个前提展开�?

### guidance

guidance
- 微软推出的开源项目，几个作者看头像就很知名，分别是 shap，lime，checklist 的作者。之前有研究�? 可解释机器学习的同学应该不会陌生。从 explainable ai �? controlable llm，倒也是很说得通的发展路径

guardrails 中的做法是在 prompt 中给出说明和示范，希�? LLM 能够遵循指令来输出。但现实中往往会出现各种问题，例如额外带了一些其它的文字说明，或者生成的 json 格式不正确等，所以需要后续的 **ReAsk 来进行修�?**�?

LangChain 里也提供了各�? output parser 来帮忙提取回复中的结构化信息部分，但也经常容易运行失败�?

�? guidance 中，同样是通过“模板语言”来定义 LLM 的输出结构，以确保输出格式的正确性。这个结构比�? xml 来说会更易写易理解些

guidance 将更加复杂的 Handlebars 模板 融入到了 prompt 中，使得原先需要复杂设计的 LLM 生成与程序处理交互过程可以很方便地在 prompt 中直接完成�?
- 上面的例子中，只有当调用到`{{gen}}`命令时，才会触发 LLM 的生成操作。另外也有像`{{select}}`，`{{#geneach}}`，函数调用，逻辑判断，控制流等命令，有种结合了自然语言与编程语言两者长处的感觉�?

除了 prompt 模板编程能力外，guidance 还有一系列高级特性，包括�?
- 支持 hidden block，例�? LLM 的一些推理过程可能并不需要暴露给最终用户，就可以灵活利用这个特性来生成一些中间结果�?
- Generation caching，自动把已经生成过的结果缓存起来，提升速度�?
- 支持 HuggingFace 模型�? guidance acceleration，进一步提升生成速度�?
- Token healing，不看这个我还不知道 LLM 有这种问题…�?
- Regex pattern guide，在模板的基础上进一步通过正则表达来限定生成的内容规范�?

### lmql

�? guidance 的基础上，lmql 项目进一步把“prompt 模板”这个概念推进到了一种新的编程语言，倒是有点像前�? guardrails �? NeMo-Guardrails 的关系。项目本身提供了很漂亮的 playground 方便试用，注意如果要在本地玩这个项目，需要升级到 Python 3.10 的版本�?


### Json 控制

�?2024-8-6】[程序员窃喜！卡了大模型脖子的Json输出，OpenAI终于做到�?100%正确](https://mp.weixin.qq.com/s/E2aXlQVzaFQUlFNDjUr-SQ)
- [Introducing Structured Outputs in the API](https://openai.com/index/introducing-structured-outputs-in-the-api)

大模型的 json 格式饱受诟病。经常遇到模型不遵循指令，不按格式输出，即使�? prompt 中明确说了要按照指定格式（比如Json、XML）返回结果，但是它就是不听话�?

OpenAI �? GPT-4o 模型升级到`2024-08-06`版本，带来全新功能：
- API 中引入了`结构化输出`（Structured Outputs�?

模型输出现在可靠地遵循开发人员提供的 JSON 模式, 实现输出JSON�?**100%准确�?**

之前开发者通过第三方开源工具，或在 prompt 上面做功夫，让大模型遵循你的命令，再或者反复重试请求来绕过LLMs在结构化处理的缺陷，现在都不需�?

两种办法�?
- �?1）函数调�?: 在函数定义中设置 strict：true进行结构化输出；
- �?2）新增response_format 参数选项

如何实现�?
- 对于特定复杂JSON架构进行模型训练，Openai通过这种方法能把模型准确率提�?**93%**�?
  - 相较于最开始带JSON模式的GPT-4�?**40%**准确率，已经高出很多了�?
  - 但是模型本质上还是不确定，无法保证JSON的稳定输�?
- OpenAI使用了约束解码（constrained decoding）技术�?
  - 默认情况下，大模型在进行token输出时，可在词汇表中选择**任意**词汇，作为下一个输出token。而这�?**不可控�?**会让模型在输出一些固定格式的文本时犯格式错误�?
  - 而使用动态约束解码技术后，大模型在下一个token输出时，便增加了一些约束，将模型限制在有效的token内，而不是所有token�?
  - 比如：输入“`{"val`”后，下一个生成的文本一定不会是“`{`”�?
  - 大模型不仅可以实现JSON格式正确，还可实现合适schema结构精确�?

现在OpenAI已经通过这种方式实现�?100% JSON输出准确率�?

缺陷
- 额外增加Schema预处理时间，新模型在请求新的JSON Schema时慢些�?
- 要使用结构化输出还有一些限制：
  - 目前结构化仅支持输出一部分JSON模式，包�? String、Number、Boolean、Object、Array、Enum和anyOf�?
  - 同时，所有字段或者函数参数必须是“required”�?
- **对象对嵌�?**深度和大小也有限制�?
  - 一个架构总共最多可以有 100 个对象属性，最多有 5 个嵌套级别�?
  - OpenAI还留了个底：**结构化输出并不能防止所有类型的模型错误**。模型可能仍会在JSON对象的值中犯错误（比如在数学方程式中步骤出错），如果出现错误，需要使用者在指令提示词中提供示例，或者将任务拆分为更简单的子任务�?
- 安全。结构化输出功能将遵守OpenAI现有的安全政策，并且仍会拒绝不安全的请求。甚至他们在API响应上设置了一个新字符串值，让开发人员能以编程方式，检测模型是否拒绝生成�?


## 知识植入 


LLMs 依然会受�?**知识截断**�?**谬误**问题的限制。例如，ChatGPT �? LlaMA �? LLMs 仅具备截至训练最后时点的信息，也可能会因预训练数据中的偏见和差异生成不准确或误导性的输出。因此，高效更新 LLMs 的参数化知识进而调整特定行为，变得至关重要�?

解决办法
- 尽管**微调**�?**参数高效微调**可以修改 LLMs，但成本较高，还可能导致 LLMs 失去预训练所得能力，并且其修改也不总能泛化到相关输入�?
- 使用**手动编写**�?**检�?**的提示影�? LLMs 的输出，但这类方法没有参数更新，可靠性不足�?


### 知识编辑 

为了使不相关输入的影响最小化，并迅速有效地修改 LLMs 的行为，一种可行的解决方案�?**知识编辑**。关�? LLMs 的知识编辑研究在各种任务和设置下取得显著进展，包�? `Memory based`、`Meta-learning` �? `Locate-Then-Edit` 三类方法�?

Methods

(1) [Preserve Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#preserve-parameters)
- �? [Memory-based](https://github.com/zjunlp/KnowledgeEditingPapers#memory-based)
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

- �? [Additional Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#additional-parameters)
1.  **Calibrating Factual Knowledge in Pretrained Language Models**. (EMNLP 2022)  
    Qingxiu Dong, Damai Dai, Yifan Song, Jingjing Xu, Zhifang Sui, Lei Li. \[[paper](https://arxiv.org/abs/2210.03329)\] \[[code](https://github.com/dqxiu/CaliNet)\]
2.  **Transformer-Patcher: One Mistake worth One Neuron**. (ICLR 2023)  
    Zeyu Huang, Yikang Shen, Xiaofeng Zhang, Jie Zhou, Wenge Rong, Zhang Xiong. \[[paper](https://arxiv.org/abs/2301.09785)\] \[[code](https://github.com/ZeroYuHuang/Transformer-Patcher)\]
3.  **Aging with GRACE: Lifelong Model Editing with Discrete Key-Value Adaptors**.  
    Thomas Hartvigsen, Swami Sankaranarayanan, Hamid Palangi, Yoon Kim, Marzyeh Ghassemi. \[[paper](https://arxiv.org/abs/2211.11031)\] \[[code](https://github.com/thartvigsen/grace)\]
4.  **Neural Knowledge Bank for Pretrained Transformers**  
    Damai Dai, Wenbin Jiang, Qingxiu Dong, Yajuan Lyu, Qiaoqiao She, Zhifang Sui. \[[paper](http://arxiv.org/abs/2208.00399)\]

- �? [Change LM's representation space](https://github.com/zjunlp/KnowledgeEditingPapers#change-lms-representation-space)

1.  **Inspecting and Editing Knowledge Representations in Language Models**  
  - Evan Hernandez, Belinda Z. Li, Jacob Andreas. \[[paper](http://arxiv.org/abs/2304.00740)\] \[[code](https://github.com/evandez/REMEDI)\]

�?2）[Modify Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#modify-parameters)

�? [Finetuning](https://github.com/zjunlp/KnowledgeEditingPapers#finetuning)

1.  **Plug-and-Play Adaptation for Continuously-updated QA**. (ACL 2022 Findings)  
  - Kyungjae Lee, Wookje Han, Seung-won Hwang, Hwaran Lee, Joonsuk Park, Sang-Woo Lee. \[[paper](https://arxiv.org/abs/2204.12785)\] \[[code](https://github.com/wookjeHan/Plug-and-Play-Adaptation-for-Continuously-updated-QA)\]
2.  **Modifying Memories in Transformer Models**.  
  - Chen Zhu, Ankit Singh Rawat, Manzil Zaheer, Srinadh Bhojanapalli, Daliang Li, Felix Yu, Sanjiv Kumar. \[[paper](https://arxiv.org/abs/2012.00363)\]
    

�?  [Meta-learning](https://github.com/zjunlp/KnowledgeEditingPapers#meta-learning)

1.  **Editing Factual Knowledge in Language Models**.  
  - Nicola De Cao, Wilker Aziz, Ivan Titov. (EMNLP 2021) \[[paper](https://arxiv.org/abs/2104.08164)\] \[[code](https://github.com/nicola-decao/KnowledgeEditor)\]
2.  **Fast Model Editing at Scale**. (ICLR 2022)  
  - Eric Mitchell, Charles Lin, Antoine Bosselut, Chelsea Finn, Christopher D. Manning. \[[paper](https://arxiv.org/abs/2110.11309)\] \[[code](https://github.com/eric-mitchell/mend)\] \[[page](https://sites.google.com/view/mend-editing)\]
3.  **Editable Neural Networks**. (ICLR 2020)  
  - Anton Sinitsin, Vsevolod Plokhotnyuk, Dmitry V. Pyrkin, Sergei Popov, Artem Babenko. \[[paper](https://arxiv.org/abs/2004.00345)\] \[[code](https://github.com/xtinkt/editable)\]
    

�? [Locate and edit](https://github.com/zjunlp/KnowledgeEditingPapers#locate-and-edit)

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
    

�?3�? [More Related Papers](https://github.com/zjunlp/KnowledgeEditingPapers#more-related-papers)

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

快速注入知�?

- �?2022-2-10】Rank-One Model Editing (ROME): [Locating and Editing Factual Associations in GPT](https://arxiv.org/abs/2202.05262), [demo](https://rome.baulab.info/)

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
# �?
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

#### EasyEdit 浙大 -- 开�?

�?2023-8-16】[浙大出品：大模型轻松获取“世界知识”，比传统微调效果更好](https://www.toutiao.com/article/7267801834855727679)
- 知识编辑 papaerlist: [Knowledge Editing for LLMs Papers](https://github.com/zjunlp/KnowledgeEditingPapers)
- �?2023-5-23】[Editing Large Language Models: Problems, Methods, and Opportunities](https://arxiv.org/abs/2305.13172)
- ![](https://github.com/zjunlp/KnowledgeEditingPapers/raw/main/img/overview.jpg)

浙江大学和东海实验室的研究团队提出了一个易于使用的 LLMs 知识编辑框架——`EasyEdit`，该框架支持各种知识编辑方法，且可以轻松应用于众�? LLMs，如 T5、GPT-J �? LlaMA 等�?
- 论文 [EasyEdit: An Easy-to-use Knowledge Editing Framework for Large Language Models](https://arxiv.org/abs/2308.07269)
- 代码 [EasyEdit](https://github.com/zjunlp/EasyEdit)

然而，目前关于 `LLMs 知识编辑`的研究在实现和任务设置上的差异妨碍了知识编辑统一和综合框架的发展。值得注意的是，这种复杂性阻碍了不同方法之间有效性和可行性的直接比较，也使得创建新的知识编辑方法变得复杂�?

EasyEdit 框架整合了各种编辑技术，支持在不�? LLMs 之间自由组合模块。通过统一的框架和接口，EasyEdit 能使用户迅速理解并应用包含在该框架中的主流知识编辑方法。EasyEdit 具有统一�? Editor、Method �? Evaluate 框架，分别代�?**编辑场景**�?**编辑技�?**�?**评估方法**�?
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCdrGGtbIFt~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=qjF%2FeWeSs6aesEsE1h%2BZuHMGRz8%3D)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCf8CHe0fQA~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=4GKQB2crsR9z9gIr9p31Cav6dq8%3D)


EasyEdit 还提供了五个评估编辑方法性能的关键指标，包括`可靠性`（Reliability）、`泛化性`（Generalization）、`局部性`（Locality）、`可移植性`（Portability）和`效率`（Efficiency）�?

为验证知识编辑在 LLMs 中的应用潜力，研究团队选用了参数庞大的 LlaMA 2 模型，并利用 ZsRE 数据集（QA 数据集）来测试知识编辑将大量一般事实关联整合进模型的能力。测试结果证明，EasyEdit 在可靠性和泛化性方面超越了传统的微调方法�?
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCiL5n53x88~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=wQPBTjiUF%2FX%2BszdxJIiTV%2FbPDe8%3D)



## 模型结构

详见 [LLM 架构代码详解](llm_code)


### Transformer 改进

详见站内: [transformer 改进专题](transformer_evolution)

### 放弃 Transformer

transformer 架构不是唯一

#### ttt

ttt 替代自注意力�?
- 论文标题：[The Surprising Effectiveness of Test-Time Training for Abstract Reasoning](https://ekinakyurek.github.io/papers/ttt.pdf)

�? TTT 有效应用�? few-shot 学习的几个关键要素：
- 在与测试时类似的**合成任务**上进行初始微调；
- 用于构建测试时数据集的增强型 leave-1-out 任务生成策略�?
- 训练适用于每个实例的适应器；
- 可逆变换下的自我一致性（self-consistency）方法�?

两种不同�? TTT 数据生成方式�?
- 一�? in-context learning（ICL）格式；从给定的测试演示中创�? leave-1-out 任务
- 另一种是端到端格式。将每个 i/o 对视为一个单独的任务

实验环节，研究者在抽象与推理语料库（ARC,抽象与推理语料库）中对这些方法进行了评估。ARC 语料库收集了很多极具挑战性的 few-shot 视觉推理问题，被认为是测�? LM 泛化极限的理想基准。目前的大多语言模型�? ARC 上均表现不佳�?

TTT 可以显著提高 LM �? ARC 上的性能 —�? �? 1B 模型上将准确率提高到原来�? 6 倍，使用 8B 模型时也超过其它已发布的 SOTA 纯神经模型方法�?

�?2024-11-12】[连OpenAI都推不动Scaling Law了？MIT把「测试时训练」系统研究了一遍，发现还有路](https://www.jiqizhixin.com/articles/2024-11-12-7)

OpenAI 下一代旗舰模型的质量提升幅度不及前两款旗舰模型之间的质量提升，因为高质量文本和其他数据的供应量正在减少，原本�? Scaling Law（用更多的数据训练更大的模型）可能无以为继。此外，OpenAI 研究�? Noam Brown 指出，更先进的模型可能在经济上也不具有可行性，因为花费数千亿甚至数万亿美元训练出的模型会很难盈利�?

从预训练来看，Scaling Law 可能会放缓；

但有关推理的 Scaling Law 还未被充分挖掘，OpenAI o1 的发布就证明了这一点。它从后训练阶段入手，借助**强化学习**、原生的**思维�?**和更长的**推理时间**，把大模型能力又往前推了一步�?
- 这种范式被称为「`测试时计算`」，相关方法包括**思维链提�?**�?**多数投票采样**（self-consistency）�?**代码执行**�?**搜索**等�?

还有个新概念 —�? `测试时训练`�? Test-Time Training ，TTT），二者都试图在测试（推理）阶段通过不同的手段来提升模型的性能，但 `TTT` 会根据测试时输入，通过**显式梯度**步骤更新模型�?

这种方法不同于标准微调，因为在数据量极低的环境中运行�? —�? 通常是通过单个输入的无监督目标，或应用于一个或两个 in-context 标注示例的有监督目标�?


详见站内: [transformer 专题](transformer#ttt)

#### Yan

�?2024-7-11�? RockAI 推出 Yan 模型，放弃transformer架构, 探索类脑思路

改进�?
- (1) transformer 换成 MCSD
  - 论文 [MCSD: An Ef?cient Language Model with Diverse Fusion](https://arxiv.org/pdf/2406.12230)
- (2) 局部模态激�?
  - transformer架构: �? 1+1=?, 会激活所有参�?, 算力消耗太�?, 人脑不是这样
  - 类脑机制: 人脑按听说看等功能分�?, 根据任务激活对应区域，其它区域处于抑制状�?, 这样功耗很�?, �?20w, 相当于电灯泡 

整体水平接近主流的transformer，部分性能超越
- 3b 模型, 大小5G，优化后，内存占用仅1G
- 端侧设备上运行，性能超过 transformer 30% 以上

问题
- 如何判断激活哪个区�?? **仿真神经元选择算法**, 一个单独的小型神经网络, 随着训练的进�?,从随机选择迭代到针对性选择
- 训练上有什么技�?? 

`Yan 1.3`: 群体智能单元大模�?
- 训练效率提升7倍、推理吞吐量提升5倍、记忆能力提�?3�?
- 秒级影响、非transformer结构、端到端多模态、满足大部分端侧设备
  - 国内能在手机cpu上运行LLM的公司不超过3�?

现在大模型训练反常识：训练一个模型，花费的计算资源太多，有的甚至要启动核电站训练�?

视频介绍
- [站起来了！国内这家AI公司用新技术挑战ChatGPT权威](https://www.bilibili.com/video/BV19LCUYuEKP/?spm_id_from=333.999.0.0&vd_source=ec1c777505e146eb20d947449d6bba6e) RockAI联创邹佳�?


<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=113328533868595&bvid=BV19LCUYuEKP&cid=26349866723&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

OpenAI GPT 在attention路上深耕，并非唯一出路�?

改进
- 量化�?
  - 文本模态上量化，能保留80-90%的效果，而图像、视频大幅度下滑
  - 量化后，权重固定，无法再学习

国内大模型机�?
- 基础创新: 弯道超车的机会，卡脖子问�?
  - deepseek 推出 MLA/O1复现
  - RockAI(岩山科技) 目标：把attention拿掉; 国内能在手机上运行的LLM不超�?3�?, Yan 模型解决端侧推理资源开销大的问题
  - 国内蹦出来一批LLM，原因是 Llama 开源了。。。META 计划闭源
  - 人才要求: 数学+算法都强，且愿意坐冷板凳
- 应用创新
  - 国内做应用很�?
  - 人才要求：交叉学科背景，�? 懂医�?+AI


`斑马鱼`
- 只有几百万神经元，但避障能力非常强，这对智能驾驶很有启发
- 还不清楚大脑神经有没有量子效应�?
如果斑马鱼神经网络有量子效应，那么鱼脑计算效率肯定是高效的，这在需要投入多少算力可能有的参考�?

机器�?
- 宇树科技、智源，机器人行业还需�?5年沉淀

### 图解

总结LLM各阶段优化方�?

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-06-22T15:10:12.254Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;V_7K2ib4bP-NWsyXjMxV\&quot; version=\&quot;21.5.0\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;�? 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;795\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-35\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f9f7ed;strokeColor=#36393d;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;90\&quot; y=\&quot;300\&quot; width=\&quot;180\&quot; height=\&quot;360\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wGYBfAiltT4hGnPjrrAm-8\&quot; value=\&quot;LLM改进方向\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=19;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;242\&quot; y=\&quot;70\&quot; width=\&quot;216\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; value=\&quot;数据\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;118\&quot; y=\&quot;180\&quot; width=\&quot;110\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; value=\&quot;训练\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;570\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-6\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; target=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;240\&quot; y=\&quot;275\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;410\&quot; y=\&quot;410\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-15\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; target=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;250\&quot; y=\&quot;600\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; value=\&quot;复现\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;590\&quot; y=\&quot;535\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-12\&quot; value=\&quot;数据集：收集处理\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-13\&quot; value=\&quot;三步走流程\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-14\&quot; value=\&quot;硬件资源开销\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-22\&quot; value=\&quot;改进&amp;lt;br&amp;gt;�? 单词→字�?&amp;lt;br&amp;gt;②解决了OOV问题\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;190\&quot; y=\&quot;450\&quot; width=\&quot;120\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-42\&quot; value=\&quot;2023-6-22&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;120\&quot; y=\&quot;1210\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; value=\&quot;效果\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;910\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-3\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-2\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;283\&quot; y=\&quot;500\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;280\&quot; y=\&quot;790\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-5\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-4\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;240\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;490\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; value=\&quot;模型\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;340\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-7\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-6\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;620\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;780\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; value=\&quot;部署\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;740\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-8\&quot; value=\&quot;问题\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540\&quot; y=\&quot;860\&quot; width=\&quot;230\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-37\&quot; value=\&quot;LLM评测\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-9\&quot; value=\&quot;知识准确性：幻觉，胡说八道\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-10\&quot; value=\&quot;复杂推理能力\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-11\&quot; value=\&quot;人类偏好对齐：RLHF不足\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-12\&quot; value=\&quot;应用\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;1110\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-13\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-12\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;167\&quot; y=\&quot;630\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;90\&quot; y=\&quot;750\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-14\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;460\&quot; y=\&quot;960\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;510\&quot; y=\&quot;935\&quot; /&gt;\n              &lt;mxPoint x=\&quot;510\&quot; y=\&quot;935\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-15\&quot; value=\&quot;工程落地\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;708\&quot; width=\&quot;140\&quot; height=\&quot;180\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-16\&quot; value=\&quot;小型化\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-17\&quot; value=\&quot;本地部署\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-18\&quot; value=\&quot;性能：时延、并发\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-20\&quot; value=\&quot;数据安全\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-38\&quot; value=\&quot;输入、输出限制\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;150\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-19\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=-0.021;entryY=0.9;entryDx=0;entryDy=0;entryPerimeter=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-16\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;605\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-21\&quot; value=\&quot;生态系统\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380\&quot; y=\&quot;1060\&quot; width=\&quot;140\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle x=\&quot;550\&quot; y=\&quot;1040\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-22\&quot; value=\&quot;联网\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-23\&quot; value=\&quot;插件市场\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-24\&quot; value=\&quot;垂类应用\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-25\&quot; value=\&quot;LLM框架：LangChain\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-26\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-12\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-23\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;775\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;367\&quot; y=\&quot;775\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-27\&quot; value=\&quot;数据集\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;560\&quot; y=\&quot;145\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-28\&quot; value=\&quot;预训练数据集：中英文\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-29\&quot; value=\&quot;指令集\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-30\&quot; value=\&quot;prompt数据集\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-31\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;entryX=-0.014;entryY=0.933;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-28\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;605\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-32\&quot; value=\&quot;模型优化\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;400\&quot; y=\&quot;305\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-33\&quot; value=\&quot;基座大模型：中文\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-34\&quot; value=\&quot;奖励模型\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-35\&quot; value=\&quot;RL环节优化\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-36\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;entryX=-0.007;entryY=0.067;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-34\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;238\&quot; y=\&quot;215\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;408\&quot; y=\&quot;214\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



# 结束