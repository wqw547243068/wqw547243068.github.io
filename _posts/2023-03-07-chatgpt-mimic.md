---
layout: post
title:  ChatGPT复现之路
date:   2023-03-06 12:00:00
categories: 大模型
tags: gpt 文本生成 ChatGPT 评测 蒸馏 llama 开源 协议 mamba jamba
excerpt: ChatGPT复现笔记
mathjax: true
permalink: /chatgpt_mimic
---

* content
{:toc}

# ChatGPT 复现

ChatGPT复现上
- 一方面是复现**三步流程**（Colossal ai+Open Assistant+LLaMA）
- 另一方面是**训练加速**（Deepspeed+Megatron+Colossal ai+FlexGen），便于基于开源大模型（Bloom/OPT/T5）微调; 
- 还有 更超前的小冰链（X-CoTA），思维链透明化+执行能力（有人推测与大语言模型关系不大）；有个瓶颈：涌现能力只出现在100b级别的大模型上，小模型一般人难以优化

[Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM)

There are three important steps for a ChatGPT-like LLM:
1. Pre-training
1. Instruction Tuning
1. Alignment

图解
- ![](https://github.com/Hannibal046/Awesome-LLM/raw/main/resources/creepy_llm.jpeg)

【2023-10-17】[大模型技术图谱](https://www.toutiao.com/w/1779880159249415)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-ezhpy3drpa/3064a89ec25445d5aec859e3fc942fb3~tplv-obj:1080:1754.image?_iz=97245&from=post&x-expires=1705276800&x-signature=IGxpShbeGqu%2BDVWQu71qZXyymPo%3D)

## 大模型行业

谷歌、Meta等公司不断发布百亿到千亿规模的大型语言模型，例如
- `Gopher`（2021年）、`Chinchilla`（2022年）、`PaLM`（2022年）、`Claude`（2022年）等等

但是这些模型都不开源，因此开源大语言模型也开始受到关注，比如
- META的`OPT`（2022年）、`BLOOM`（2022年）、`LLaMA`（2023年）。

智谱AI则选择在2022年开源了自己的千亿基座模型 `GLM-130B`

### LLM 之争

【2024-3-9】过去一个月，有四个语言模型在各项基准测试中接近甚至超过了GPT-4的表现。  
- Google Gemma、Mistral、Anthropic 和 Inflection。  
- 尽管并非每个模型都明显优于GPT-4，但都是有力的竞争者。


【2024-2-27】[总结](https://www.toutiao.com/w/1791953879006346)当前大模型现状: 按照通用、垂类，是否落地两个维度分类
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-ezhpy3drpa/b41a7fad5f06482b84e9b3f66e9b9b8a~tplv-obj:1080:3876.image)

【2023-6-5】[千模大赛哪家强？ 大语言模型中文评测实践](https://zhuanlan.zhihu.com/p/634884575)
- ![](https://pic1.zhimg.com/80/v2-9bb5d154a9b41d4f57445a5231cbbac4_1440w.webp)

【2023-7-7】[LLM之争将在2025年结束](https://mp.weixin.qq.com/s/S17Iv4iwbeSxQZPsOQSsTg)

当前范式的LLM将在2025年走到尽头，因为人类已生产出来用来表达基础逻辑的语料有限，且很快就会被穷尽于训练。
- 而LLM能力的比赛，就是看：谁能更准确的表达这个世界的运作方式 —— 这就是评估LLM的**唯一**标准，而且这个标准也是有上限的，因为当前都生活在同一个世界里。

这个上限很快就会到达。

Let's think step by step:
1. LLM的本质：可以被理解为世界模型在低维的投影，而非世界模型本身（详见《人工智障2》）。
2. LLM的推理能力：以system 1的方式represent system 2 的结果，或者说“以概率的方式表达用符号推理的结果”。
3. LLM的核心价值：作为通用的逻辑模拟器（Common logic simulator），并以此为基础来进一步计算更专业的领域逻辑。
4. LLM的生成：世界上所有被人类总结出来的通用逻辑是有限的。
5. 所有人类总结出来的逻辑都能通过语言来表达，而这些表达是有限的。
6. LLM的最终形态：通过表征来逼近对世界模型的拟合(Fitting the world model by approximating with representations)，即用语言对“世界是如何运作的”（在通用逻辑与常识层面）进行有效表达。
7. 关于这个 “世界是如何运作的” 题目，是有全球统一的标准答案的。
8. 谁先达到这个拟合的效果，就意味着谁的LLM达到了SOTA；或者，用完了所有语料，都没有实现SOTA。而这两种情况的任意一种都会在1.5-2年内出现。

我更愿意相信OpenAI已经看到这个范式的终局，甚至已经有GPT5（已达到SOTA的LLM）。只是在还没有任何人追上GPT4之前，没有必要发布GPT5这张王牌，也是最后一张牌，也没有下一张牌了。

然后会怎样？

大型多模态模型Large Multi-Modal Model (LMMM)或者大型语义模型Large Semantic Model (LSM)有机会接替LLM，再持续竞争（卷）2年左右。直到人类制作出来的所有优质视觉数据都用来训练上述模型，或在数据用完之前实现了新的SOTA。

### 如何打造一个拖垮公司的大模型？

【2023-9-20】[如何打造一个拖垮公司的大模型？](https://mp.weixin.qq.com/s/ZwdjTEHZvsK0VbzFlGtsng)

今年大模型实在太火，如何打造一个拖垮公司的大模型？不多不少，一共分10步。
- 第一步：先砸十个亿买卡
  - 做大模型，要有大格局，舍不得孩子套不着狼。
  - 什么X100、Y100……专挑算力强的买。
  - 正规渠道没货了？不能怂！加价也要整起来。
- 第二步：从顶流公司挖大牛来坐镇首席科学家
  - 必须是业界扛把子级别的大牛，就职于顶流AI公司比如“CloseAI”，经常在各种会议上高光出镜的那种。
  - 能把整个团队都带过来最好，成建制、好管理、出活儿快。
- 第三步：定战略，当卷王
  - 模型参数至少要万亿级别，当不成卷王，就只能被卷死。
  - 再来个“智算中心”，算力至少达要1000PFLOPS，自己训练完大模型，还能把算力开放出来给同行。
- 第四步：万事开头难，从数据准备开始全员鸡血加班
  - 数据不够怎么整？公开一部分，自有一部分，交易一部分。
  - 拿到数据后，得清洗处理，全体动员做标注，老板亲自下场，主打一个陪伴。
- 第五步：开始玩命训练，不出意外的话快出意外了
  - 服务器挂了、存储速度跟不上了、跨卡性能不行、梯度消失、梯度爆炸……
  - 什么？！Checkpoints没保存？反复回退，反复调参，反复排雷。
- 第六步：内部开始自我修正
  - 问题一多，团队就乱了，人都变得很浮躁。
  - 公司原有的主营业务停滞不前，业绩下滑。
- 第七步：不管产品行不行，市场宣传要先行一步
  - “我们来了！”广告要全渠道、全媒体覆盖。
  - 必须要业界感知到我们来势汹汹的霸气。
- 第八步：生态伙伴少不了，气氛必须搞起来
  - 先结盟5000家合作伙伴，达成意向合作。
  - 第二天，大家联合发发新闻稿，必须让吃瓜群众充满期待。
- 第九步：大模型终于“练”出来了
  - 练是练出来了，看上去有点不对劲，莫不是个“大傻子”吧？
  - 落地实施，那叫一个难，不知道给谁用，不知道往哪儿用。
- 第十步：及时止损，人间清醒
  - 然后开始复盘，多么痛的领悟~

- 大牛来了又走了，算力卡买了又卖了，智算中心建了又拆了，大模型炼了又废了。
- ![](https://img.huxiucdn.com/article/content/202309/20/102612994924.png?imageView2/2/w/1000/format/png/interlace/1/q/85)


### LLM 造假

【2023-11-14】贾扬清：感叹一下做小公司不容易。
1. 上周，有某海外客户要我们帮他们适配某国内大厂的新模型。我们太忙，暂时还没时间给他们做适配。
2. 今天有朋友告诉我，这个大厂新模型exactly 就是 LLaMA 的架构，但是为了表示不一样，把代码里面的名字从 LLaMA改成了他们的名字，然后换了几个变量名。
3. 然后，海外有工程师直接指了这一点出来... 还有人在 HF 上面放了个把名字改回去的 checkpoint，说好了，现在你们可以直接用 LLaMA 的代码来 load 这个checkpoint 了 ...

我们是小公司也不想得罪大佬们，名字我就不说了，不过各位大佬，开源社区不容易，如果你们就是开源的模型结构，求高抬贵手就叫原来的名字吧，免得我们还做一堆工作就为了适配你们改名字...

[Yi-34B 讨论区](https://huggingface.co/01-ai/Yi-34B/discussions/11)，[01-ai](https://huggingface.co/01-ai) 总监 Richard Lin 确认

## 复现思路

【2023-2-28】要点
1. 预训练大模型
  - GPT-3规模：175b
  - 规模小，无法支持涌现能力
1. ChatGPT三步训练
  - RM、RLHF算法
  - ICL、CoT算法
1. GPU计算资源
  - 集群资源
  - GPU分布式加速算法
1. 效果评估

OpenAI InstructGPT 论文里有个惊奇的发现，即：1.3B小模型+RLHF 居然可以超越175B指令精调后的效果。有没有可能ChatGPT就是个小模型，结果最近OpenAI公开接口价格后让这种猜想的可能性又增加了。


### 大模型训练

详见站内专题：[LLM 大模型训练之路](llm_train)

### GPT现状

【2023-5-30】Andrej Karpathy微软讲座：
- 视频：[YouTube](https://www.youtube.com/watch?v=xO73EUwSegU), [B站](https://www.bilibili.com/video/BV1ts4y1T7UH)
- [文字](​https://www.toutiao.com/article/7238518758204031492), [State of GPT：大神Andrej揭秘OpenAI大模型原理和训练过程](https://mp.weixin.qq.com/s?__biz=MzIxODUzNTg2MA==&mid=2247485342&idx=1&sn=770152ca8a00f2e3d87ed2a09e131e11)

要点：
- 目前最好的开源模型是Meta的LLaMA系列
- LAMA 65B“明显比GPT-3 175B更强大”
- 大模型匿名竞技场ChatBot Arena: Claude得分介于ChatGPT 3.5和ChatGPT 4之间。

GPT大模型训练全流程，四个训练阶段：
- `预训练`（pre-training）、`监督微调`（supervised fine tuning）、`奖励建模`（reward modeling）和`强化学习`（reinforcement learning）。

热门研究方向
- AutoGPT效果目前还不太好，部件实际使用，但这种模式潜力无限
- 检索增强生成（retrieval agumented generation）和有效提示，约束提示（Constraint prompting）。
- ToT思维树：思路与AlphaGo里的蒙特卡洛搜索非常相似。诺贝尔经济学奖得主丹尼尔卡尼曼在《思考快与慢》中提出，人的认知系统包含System1和System2两个子系统。System1主要靠直觉，而System2是逻辑分析系统。System1是一个快速自动生成的过程，而System2是经过深思熟虑的部分。


### 复现路线

【2023-7-9】CTO范凯观点

国内模型分成几类
- 改头换面：百度文心千帆、科大讯飞星火、阿里通义 —— 着急变现
- 剑走偏锋：腾讯混元（行业大模型商店）、字节（火山方舟）
- 借壳炒作：缺乏训练能力，套上自己的壳，如 360用智谱AI
- 有点内涵：Minimax（商汤背景）、智谱AI(清华唐杰)、深圳鹏博（RWKV）、华为盘古


### 复现方案

假设
> 模型的**知识和能力**主要在**预训练**阶段学习，而**对齐过程**则是引导模型在推理过程中使用哪些先验分布

因此，尤为重要的是：
- 在数据集中**放大**好的先验知识并**抑制**不好的先验知识，以及驯服从互联网分布中直接捕获的原始模型


#### 如何驯服LLM

【2023-6-2】参考
- 原文: [Modern AI is Domestification](https://thegradient.pub/ai-is-domestification/)
- 中文翻译：[驯服大型语言模型（LLMs）的五种方法](https://mp.weixin.qq.com/s/93xk_x7LBFLOZlmnM96IMw)

- **Prompting**
  - 通过精心设计的提示(prompt)引导一个基础模型朝着期望的先验方向进行
  - 目前门槛**最低**的方法，有时也被成为**无梯度调优**。
  - prompt利用了训练时看到的关联和先验信息
  - 局限性：
    - 机会主义策略，即提示策略高度依赖于原始训练数据集中出现的模式、相关性和先验信息。prompt需要在通用与具体之间平衡。
    - prompt工程 受 训练数据分布中不理想数据相关性的影响，这被称为“Waluigi效应”，从而导致提示无法有效地放大先验。
- **监督微调**（Supervised Finetuning，SFT），主要思路：
  - 首先用在多样化数据集上预训练的**原始模型**
  - 然后在**规模较小但质量更高**的数据集上进行进一步训练
    - 数据集可以是原始数据集的子集，也可以是全新自定义数据集，可以人工创建验证，也可以用启发式、规则自动获取，也可以合成。
  - 其中微调数据集充当包含所有最终模型所需属性的黄金标准。
  - 这种简单性提出了一个有说服力的论点：「将目标数据集提供给原始模型，<span style='color:red'>SFT承诺将原始模型靠近目标分布</span>」。由于SFT是监督学习，如果数据好且模型庞大，成功是有保证的。
- **RLHF**: 不同于SFT的非参数方法, RLHF相反,通过参数化奖励模型明确先验知识，告诉模型偏好。
  - 用 RL 的优势：直接的在线反馈（离线反馈过时）、次优数据上训练（提升鲁棒性）
- **RLAIF**
  - RLHF的问题：存在噪音、不一致，收集成本高
  - RLAIF：AI替换人工，一方面节省人力，另外还能充当裁判（奖励模型）
- **合成数据生成SDG**：用 AI 模型辅助采集、标注
  - 交互式辅助标注
  - 生成模型合成数据：半监督、伪标签

这些方法如何选择？
- 原始训练语料库是否包含想要的所有能力和先验？如果是，请尝试提示;如果否，微调模型。
- 获取不同的微调数据集是否容易？如果是，请尝试 SFT; 如果否，请尝试 RLHF 或 AI 反馈。
- 可以访问大量计算吗？如果是，微调整个模型; 如果否，请使用 PEFT。
- ![img](https://thegradient.pub/content/images/size/w1600/2023/05/ted_main_2-1.png)
- [知乎图](https://picx.zhimg.com/v2-4d1f4db12b31ec3203629c5c1ea9f005_1440w.jpg?source=172ae18b)


现有的 AI 模型是否足以生成数据或验证数据？如果数据生成足够好，请尝试创建合成数据（SDG）;如果足以验证但不能生成，请尝试使用 AI 反馈 (RLAIF) 或自我反思;如果两者都不是，请坚持使用 RLHF。


如何对基础模型进行微调？
- ![](https://pic2.zhimg.com/80/v2-f562ee767d7931514952dc02f1590b05_1440w.webp)

有几种选择：按计算量从到小，分为: Prompt Engineering -> PEFT -> SFT
- **标准的SFT**：对整个基础模型进行微调，更新整个网络的权重。这是可能引起底层模型行为显著变化的最详尽的更新类型。
- **轻微方式微调**，只有网络某个子集可以进行微调；LiT在微调语言编码器的同时冻结了CLIP图像编码器。
- **参数高效微调**（Parameter-Efficient Finetuning，`PEFT`）是新方法，冻结了原始模型的大部，仅微调相对较小模型参数集。
  - PEFT: Prompt Tuning -> Prefix Tuning -> LoRA -> ControlNet
  - 像LoRA这样的PEFT方法就是非常大的创新，使得消费者硬件就能够对相当大的基础模型进行微调。
- Prompt Engineering

显然，「SFT的实现方式正在迅速发展，并且在可预见的未来可能仍将是一个令人兴奋的领域」。无论具体的SFT方法如何，对底层微调数据集的组成和质量都有很大的依赖。在SFT中，扩大哪些先验条件和如何扩大它们同样重要。


【2023-2-1】复现方案（参考:[chatGPT复刻方案](https://zhuanlan.zhihu.com/p/602485508)）
- （1）**复刻 GPT-3**
  - ① 开源GPT-3方案：
    - 国内（阿里达摩院[modelscope](https://modelscope.cn/models/damo/nlp_gpt3_text-generation_13B/summary)）
    - 国外（[eleuther](https://www.eleuther.ai/)/OPT/Bloom等）
  - ② 服务器资源：主流设备NVIDIA A100和V100
  - ③ 模型加速框架：
    - 国际：LLMs普遍采用NVIDIA提供的Megatron-DeepSpeed组合方案
    - 国内开源方案：如Colossal-AI以及悟道开放的FastMoE等
  - ④ 训练语料
    - 阿里达摩院：数据源[wiki](https://huggingface.co/datasets/wikipedia)和[commoncrawl](https://commoncrawl.org/)
    - 悟道开放200G的[文本语料资源](https://resource.wudaoai.cn/)
  - ⑤ Fine-Tune
    - 没必要从头训练，资源+数据耗不起，网上开放的数据跟大厂真正训练用的数据不能比。
- （2）**复刻 InstructGPT**：严格按照 论文三步来
  - ① Fine-Tune：注意这里的finetune跟上面的finetune稍有不同，上面用作**语言生成**任务为目标，这个是**对话任务**为目标。
  - ② RM：首先搭建[暗物智能InstructGPT-RM对话标注平台](http://192.168.68.61:8905/)，用于对gpt-3生成数据进行排序。其次收集更高质量的prompt，最后训练RM模型
  - ③ PPO：用于优化gpt-3, 预计工作量比较大，开源代码 [trl](https://github.com/lvwerra/trl), 基于transformers库实现了PPO训练
- （3）**指标评测**
  - 参考目前主流的评测方法，主要从一致性，相关性，信息性，吸引性，安全性等维度进行评测。
  - 国外：InstructGPT论文里介绍的评测方法, 国内可参考PLATO,EVA,PANGU-BOT等。
  - 指标评测非常重要，不能简单的对话几句就说这个模型好，那个模型不好，应当是全方位充分的评测。

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-02-28T11:55:22.657Z\&quot; agent=\&quot;5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36\&quot; etag=\&quot;GHIauyOockv2GQn2yTZN\&quot; version=\&quot;20.8.14\&quot;&gt;&lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;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&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

#### huggingface 复现


开源界围绕RLHF做了不少工作，难以重现OpenAI的RLHF pipeline。原因：
- RL和RLHF有许多微妙的实现细节，这些细节对训练稳定性有很大影响；
- 对于指令遵循任务，如评估一个编码任务中生成的800行代码片段的质量，评估模型的表现不太行；
- 模型需要长时间的训练和迭代。

加之总结任务比一般的指令任务更容易评估，所以Hugging Face最新的这项工作选择退后一步，从OpenAI早期的RLHF工作中，探寻OpenAI的RLHF的真面目。
- 2020年 “Learning to summarize from human feedback”中，OpenAI研究员将RLHF应用到了捕捉原始文本主要信息和意图的摘要任务中
  - 英文摘要任务上显著优于人类参考摘要和仅使用监督学习的更大模型。且具有较强的泛化能力，在没有特定领域微调的情况下，也能生成高质量的文章摘要，接近人类参考摘要的质量。
- 2022年“Training language models to follow instructions with human feedback”这项工作中，RLHF再次被使用，为指令遵循任务而专门设计的InstructGPT诞生

【2024-4-7】[抱抱脸Open了OpenAI的秘密武器，网易参与复现](https://hub.baai.ac.cn/view/36321)

Hugging Face、加拿大蒙特利尔Mila研究所、网易伏羲AI Lab的研究人员从零开始复现了 OpenAI的 RLHF pipeline，罗列了25个关键实施细节。
- 论文链接：[The N+ Implementation Details of RLHF with PPO: A Case Study on TL;DR Summarization](https://arxiv.org/abs/2403.17031)
- GitHub链接：
  - [summarize_from_feedback_details](https://github.com/vwxyzjn/summarize_from_feedback_details)
  - [visualize_tokens.py](https://github.com/vwxyzjn/summarize_from_feedback_details/blob/main/visualize_tokens.py)

最终成功展示了随着模型大小的增加，响应质量显著提升的scaling行为，其中2.8B、6.9B的Pythia模型在性能上超过了OpenAI发布的1.3B checkpoint。

Pythia 1.4B实验
- 根据 GPT-4的数据显示，这个1.4B模型非常接近OpenAI的1.3B性能（由于GPT4成本过高，只进行了一次评估）。

独特之处
- 对SFT、RM和PPO使用了单一的学习率，所以再重现他们的工作会变得更加简单。

从数据集到SFT、RM、OPP，共介绍了25个复现细节，深入分析了TL;DR数据集的规格、分词过程和分词长度分布。同时，详细描述了SFT和RM组件的训练设置、实施细节和结果。
- 步骤1：训练SFT（监督微调）策略
- 步骤2：收集偏好对并训练RM（奖励模型）
- 步骤3：针对RM训练RL（强化学习）策略

研究人员针从数据集到SFT、RM、OPP，共介绍了25个复现细节，深入分析了TL;DR数据集的规格、分词过程和分词长度分布。同时，详细描述了SFT和RM组件的训练设置、实施细节和结果。

数据预处理阶段：
- 对于RLHF的提示查询，OpenAI在最后一段进行截断，而不是硬截断限制；同时确保“TL;DR:”之后没有多余的空格。
- 始终在reference completions前加上**前导空格**，在reference completions后添加`<|endoftext|>`，并使用单独的`[PAD]` token填充。
- SFT和偏好数据集的tokenization length不同，因此在SFT和RM训练期间分别设置最大token长度时需要注意。
- RM的验证集非常有趣，因为它包含更多独特的策略对进行比较，所以它有很多超出分布的数据。

SFT阶段：
- SFT阶段没有太多的实现细节，只需要标准的下一个token预测损失就可以了。除了使用了不同的学习率之外，研究人员的设置几乎与原始设置相同。
- 损失下降，ROUGE分数在4个随机种子和3个模型checkpoint大小上都有所提高。

RM训练：
- RM训练更有趣。例如，研究人员发现RM只在EOS token处提取奖励。此外，在检查奖励的logits时，除了EOS token外，几乎所有的logits都是负数。
- 结果非常不错，验证准确率提高了，RM几乎完美地转移到了偏好数据集验证集中的CNN/DM子集上。
- 他们计算了SFT demonstration的平均奖励——标量值看起来有些随意；还计算了OpenAI偏好数据集中每个批号和置信度的验证准确率。
- 注意: 不同的批次/置信度可能会有截然不同的准确率。
- 研究人员也测量了RM与GPT3.5和RM的一致性率（agreement rate），并发现一致性率有所提高，但在6.9B级别时有所减弱。并绘制了AnthropicAI所做的RM校准，发现RM通常校准不足。

研究人员将验证准确率与DPO的隐式RM进行了比较，发现出于某种原因DPO的验证准确率较低。

几个不同点：
- RM训练只在EOS token处应用损失，而DPO在每个完成token处应用损失。
- DPO还有一个可能影响训练的$beta参数，RM则没有。
- 研究员Michael Noukhovitch提出了个有说服力的观点：DPO的目标可能更难优化，因为你需要使你的logprobs与基本模型有足够大的不同才能更改奖励，而RM可以学习一个线性头，可以更容易/更快地改变奖励的值。

PPO训练：
- 学习值函数的行为与RM截然不同。例如，值函数logits通常更为正，因为在每个时间步长，它都试图对最终分数进行建模。
- PPO也使用了EOS技巧。在PPO训练中，研究人员通常采样固定数量的token，比如48个。如果完成不以EOS token结束怎么办？前面已经提到了，非EOS token的logits几乎总是负的（并且可能无效）。
- EOS技巧基本上用恒定的-1奖励取代了不以EOS token结尾的完成的奖励。有几个目的：① 定义奖励得分 ② 约束补全长度

研究人员还尝试了PPO的奖励白化处理，并发现这样使得与参考摘要的胜率略有降低，以及完成token的长度略微缩短。
- 长度在这里是一个混杂因素，所以研究人员引导了OpenAI进行的长度控制分析，通过将x轴设置为模型摘要长度与参考摘要长度之比的对数来执行。
- 当长度得到控制时，研究人员发现比较奖励白化的结果更具挑战性，但尽管如此，在每个摘要长度上，PPO模型几乎总是优于SFT模型。
- PPO 的训练曲线如下所示。值得注意的是，几个1B型号的KL值爆炸了。从优化的角度来看，这并没有什么问题，因为RLHF奖励一直在上升，这些1B模型对应于“奖励黑客”/过度优化的模型。

为了更好地理解模型的行为，研究人员还可视化突出显示了经过微调的模型在生成文本时总会以一个EOS token结束。为了进一步探索这一点，原论文附录部分提供了更多类似的可视化效果。


### 复现难点

【2023-2-20】[追赶ChatGPT的难点与平替](https://mp.weixin.qq.com/s/eYmssaPFODjC7xwh1jHydQ) 以后各个NLP子任务可能就统一起来了，范式也会变成预训练+Prompt，不需要那么多精调模型的算法了。

复现ChatGPT的难点与平替方案：
- （1）**高效的算法框架**：
  - `Megatron-LM`和`DeepSpeed`已经把模型提到了一个我们不敢想的尺寸（普通算法团队人均2张V100就很幸福了），结果20年中OpenAI一下发布了175B的GPT-3。从那时起，OpenAI算法框架的容量就领先了一到两个数量级。
  - 最近已经出了一个平替方案`ColossalAI`，由国人打造，从一些介绍来看效率是超过`Megatron-LM`和`DeepSpeed`的，而且已经做了ChatGPT的部分实现（还不支持PPO-ptx），接下来就看大家使用的效果了
- （2）**先追上GPT 3**：符尧对大模型能力的研究看来，至少要**62B**以上的模型才能有一定少样本效果。
  - 真的追上这些能力需要耗费很大财力、人力和时间，估计现在各个厂都在批发A100了，起码千张，预算上亿。
  - 一些平替方案，支持中文的有`mT5`(176B)、`GLM`(130B)和`BLOOM`(176B)，但其中只有BLOOM是`GPT`架构。
  - `mT0`和`BLOOMZ`，是Instruction tuning后的版本。
  - 微调的BLOOMZ模型维持了与BLOOM模型相同架构超参数，176b，参考：[【大模型】BLOOM：一个176B参数且可开放获取的多语言模型](https://zhuanlan.zhihu.com/p/603518061)
- （3）获取真实的用户输入
  - 从GPT3到ChatGPT，主要是基于用户真实输入进行标注，再对模型进行精调，从而拟合了人的偏好（称为Alignment）
  - 技术问题都有平替，但去哪儿找上亿的用户来源源不断的输送Prompt呢？
  - 第一个平替方案：借鉴Instruction tuning的论文，用各种NLP数据集构造Prompt。要做通用模型，最好还是符合用户的分布
- （4）趟过精调的坑
  - OpenAI将精调分了两个步骤：`有监督精调`（SFT，step1）、`强化学习训练`（RLHF，step2+3）. ChatGPT精调重点在于RLHF阶段。

把训模型当作带孩子：
- `Pretrain`：在孩子0-3岁的时候，我们没法讲太多道理，他也听不懂，更多的是让他自己观察这个世界，自由学习。
- `Instruction Tuning`：孩子学会说话了，也对世界有了基本认知，我们就可以开始通过示范教他一些东西，比如怎么穿衣服、怎么刷牙。
- `RLHF`：等孩子再大点，很多事情都会了，便不会再完全模仿父母，而是有自己不一样的行为，这时候父母就需要对这些不可预料的行为给出反馈，在他取得好成绩时奖励，在做坏事后惩罚。

生成任务本身, 长久以来NLP里的范式都是以**最大似然**为目标，用teacher forcing的方式拟合标注同学写出的句子。那万一标注同学偷懒呢？
- 对于「到底什么是好的回复」这个问题，每个人都有不同的答案，但必须定义好**目标**，才知道模型应该往哪里优化。
- 谷歌训`LaMDA`对话模型时就给出了5个维度的定义，再朝着这5个方向拟合，而人类语言博大精深，5个维度真能评价一段话的好坏吗？

RLHF范式的关键就在于它能真正让模型去拟合人的偏好，同时给予模型一定的自由度，这样才能让模型先模仿再超越，而不是重复Instruction tuning中的一些pattern。

OpenAI官方给的实验数据：
>- 在摘要生成任务中，RLHF精调后的模型大幅超越SFT的效果。
>- 另外论文中的其他实验也证实了RLHF模型具备更好的跨领域泛化能力：在InstructGPT论文中，1.3B经过RLHF的模型可以超过175B模型SFT的效果

在人力、算力、时间有限的情况下，效率最优的路径:
- 直接在1.3B模型上迭代，大概10万标注数据，复现一个低配小型ChatGPT，验证整个流程的有效性，再去做175B的模型。
- 如果每个方案都打个折，确实是复现到**60%**的程度，和业内乐观的预测一样。

### GPT-3 国内复制

【2023-2-28】[没有这些，别妄谈做ChatGPT了](https://zhuanlan.zhihu.com/p/610118560)

算法可能只是硬币的一面，另一面是算力和云基础设施，不容忽视。

- 【2023-2-28】国内真正复刻了GPT-3的，有且只有一家，`阿里达摩院`，从小到大（从base到175B），全面、完整地复刻了GPT-3，并且开放在魔搭社区上。
- 2021年4月就发布了首个中文语言大模型`PLUG`（当时参数是270亿）。该模型首次在中文语言理解榜单CLUE上面，以86.685分的成绩超越人类。
- 2021年10月，达摩院还探索实现了10万亿参数模型——`M6`，达摩院团队通过大量的底层优化和算法设计，仅仅使用了**512卡**便实现了这一庞大的模型工程。此前，`M6`模型将AI图片生成清晰度从OpenAI DALL·E的256×256成功提升到了1024×1024，效果十分惊艳。
- `M6`模型的发布引发了国内外的大量关注，其中，OpenAI前政策主管Jack Clark公开点评：“这个模型的规模和设计都非常惊人。这看起来像是众多中国的AI研究组织逐渐发展壮大的一种表现。”

ChatGPT之争已经超出了算法的范畴，它更是一个AI+云计算能力的全方位竞争，是技术生态层面的竞争。 既需要强大的云基础设施能力的保障，又需要深厚的大模型技术积淀，两者缺一不可。

云基础设施
- OpenAI的解决方式是向微软求助。同理，国内初创企业想要成为中国版OpenAI，自研ChatGPT，恐怕也要先跟几个云计算厂商好好聊一聊了。

没有做过大模型训练的人，可能会误以为多买几张A100卡就可以了。

实操时就会发现：
- 单机多卡根本训不动千亿参数模型，你需要多机多卡分布式训练
- 当你开始多机训练时，你发现A100的算力都被网络通信延迟给吃掉了，多机可能还没有你单机训的快
- 然后你会发现训练ChatGPT的海量数据存储也是个问题，就算存下来了，数据读取的IO效率又极大的制约了模型的训练效率
- 一通基础设施问题下来，A100的算力被浪费了7、8成，模型训练实验无法开展

因此，没有一个面向AI高度优化的**云计算平台**，训练`GPT-3`和`ChatGPT`这种级别的模型怪兽是相当不现实的。
- 重点: “面向AI”+“高度优化”。
- 网络、存储、计算、通信等方方面面的系统化工程能力

给你一万张A100，就能把ChatGPT训出来吗？答案无疑是否定的。万卡集群对于网络、存储和通信有极高的要求，弄得不好直接宕机。
- 数据层面，飞天智算平台的单集群算力峰值高达12EFLOPS，千卡并行效率达90%。针对ChatGPT这类数据密集型场景，还对大规模集群进行了大量数据IO优化，通过自研KSpeed和RDMA高速网络架构，最高可将存储IO性能提升10倍，将时延显著降低了90%。
- 此外，阿里云自研的高性能集合通信库ACCL和自研的网络交换机等，对万卡规模的AI集群提供了无拥塞、高性能的集群通讯能力。

除了底层硬件的AI集群，大模型训练非常依赖于软件平台层。
- 飞天智算平台的机器学习平台PAI，专门针对AI大模型推理和训练场景进行针对性优化，可将计算资源利用率提高3倍以上，AI训练效率提升11倍，推理效率提升6倍，覆盖了全链路的AI开发工具与大数据服务。

### GPT-3 复制失败

【2023-2-16】[GPT公开复制为什么失败，我们应该如何使用GPT-3.5/ChatGPT](https://hub.baai.ac.cn/view/24224)
- [英文原版](https://jingfengyang.github.io/gpt)
- [推特原文](https://twitter.com/JingfengY/status/1625003999387881472)

“失败”定义为与原始GPT-3论文中报告的**性能不匹配**，型号尺寸相似甚至更大。
- 根据这一标准，`GPT-3` 和 `PaLM`（540B）是成功的，但这两个模型都不是公开的，而所有公共模型（例如OPT-175B和BLOOM-176B）在某种程度上是“失败”。

- 但是，仍然可以从这样的“失败”中吸取许多教训。请注意，如果多次尝试不同的设置，公共社区最终可能会复制GPT-3。但到目前为止，费用仍然太高，无法训练另一个版本的OPT-175B。因为训练这样一个大型型号的一次通行证需要在 ~1000 80G A100 GPU上运行至少2个月。

尽管一些文章（例如 OPT-175B 和 GLM-130B）声称在一些任务上能够匹配甚至超过原始的 GPT-3 的表现，在更多 GPT-3 已经测试过的任务上，这种声明仍然是存疑的。
- 根据大多数使用者在更多样的任务上的经验，以及 HELM 的评估来看，最近的 OpenAI GPT-3 的 API 表现也仍然比这些开源模型更好。

尽管背后的模型可能使用了`指令微调`（instruction tuning, 正如 `InstructGPT` 那样），类似的使用了指令微调的 OPT 版本（`OPT-IML`）和 BLOOM 版本（`BLOOMZ`）也仍然远比 `InstructGPT` 和 `FLAN-PaLM`（PaLM 的指令微调版本）要差得多。

多个可能的原因导致了相比 GPT-3 和 PaLM 的成功，OPT-175B 和 BLOOM-176B 的失败。两个部分：预训练数据和训练策略。
- (1) 预训练数据
  - GPT-3 在共计 300B 的 token 上进行训练，其中 60% 来自经过筛选的 Common Crawl，其它则来自：webtext2（用于训练 GPT-2 的语料库），Books1，Books2 和维基百科。
  - 更新版本的 GPT-3 还用了**代码数据集**进行训练（例如 Github Code）。每个部分的占比并不与与原始数据集的大小成比例，相反的，具有更高质量的数据集被更加频繁地采样。
  - 导致 OPT-175B 和 BLOOM-176B 失败的，可能是以下三个难点，它们使得开源社区难以收集到类似的数据：
    - **缺乏筛选低质量数据的分类器**：构建 GPT-3 和 PaLM 的预训练数据集，但在 OPT 和 BLOOM 的训练中却没有被采用。用更少但质量更高的数据集训练的预训练模型，可以在性能上超过另一个用更多的混合质量数据集训练的模型。数据多样性和质量
    - **预训练数据集的去重**：去重有助于避免预训练模型多次面对相同的数据后记住它们或者在其上过拟合，因此有助于提高模型的泛化能力。GPT-3 和 PaLM 采用了文档级别的去重，这同样被 OPT 所采用。但 OPT 预训练的去重 Pile 语料库中仍有许多重复存在，这也可能导致它较差的性能（注：在一些最近的文献中显示去重对于预训练语言模型的重要性可能没有想象中大）。
    - **预训练数据集的多样性**：包括**领域**多样性、**格式**多样性（例如：文本、代码和表格）和**语言**多样性。OPT-175B 所使用的 Pile 语料库声称有着更好的多样性，但 BLOOM 采用的 ROOTS 语料库则有太多的已经存在的学术数据集，缺乏 Common Crawl 数据所包含的多样性。这可能导致 BLOOM 性能更差。作为对比，GPT3 来自 Common Crawl 语料的占比则要高得多，而它们是多样的和来自广泛领域的，这也可能是 GPT-3 能够作为首个通用聊天机器人 ChatGPT 的基础模型的原因之一。
      - BLOOM 和 PaLM 在多语言数据上有更高的占比，这导致它们在一些多语言任务和机器翻译任务上的性能更高。
      - OPT 使用了很多对话数据（例如 reddit），这可能是它在对话中表现好的原因之一。
      - PaLM 有很大的占比在社交媒体对话中，这可能是它在多种问答任务和数据集上有着卓越表现的原因。
      - PaLM 和更新版本的 GPT-3 有很大比例的代码数据集，这增强了它们在代码任务上的能力，以及可能增强了 `CoT` (Chain-of-Thought，`思维链`) 的能力。
      - BLOOM 在代码和 CoT 上的表现仍然是较差的，尽管它在预训练过程中使用了代码数据。这可能暗示着单独代码数据本身，并不能保证模型的代码和 CoT 能力。
    - 上面三点的重要性：通过数据**去重**避免**记忆**和**过拟合**，通过**数据筛选**以得到高质量数据，保证数据**多样性**以确保 LLM 的泛化性。但不幸的是，对于 PaLM 和 GPT-3 预处理这些数据的细节，或者这些预训练数据本身，仍然没有公布，这使得公共社区很难去复现它们。
- (2) 训练策略: 包括训练框架、训练持续时间、模型架构 / 训练设置、训练过程中的修改。在训练非常大的模型时，被用于获得更好的稳定性和收敛性。
  - 由于未知的原因，预训练过程中广泛观察到`损失尖峰`（loss spike）和`无法收敛`的情况。因此，众多对训练设置和模型架构的修改被提出，用以避免这些问题。但是其中一些修改在 `OPT` 和 `BLOOM` 之中还不是最优解，这可能导致它们的性能较差。GPT-3 并没有明确提到他们是如何解决这个问题的。

1. 训练框架。一个参数量大于 175B 的模型往往需要 ZeRO 式的**数据并行**（分布式的优化器）和**模型并行**（包括张量并行（tensor parallel）、**流水线并行**（pipeline parallel），有时还包括**序列并行**（sequence parallel））。
  - `OPT` 采用了 ZeRO 的 FSDP 实现，以及模型并行的 Megatron-LM 实现。
  - `BLOOM` 采用了 ZeRO 的 Deepspeed 实现和模型并行的 Megatron-LM 实现。
  - `PaLM` 采用了 Pathways，这是一个基于 TPU 的模型并行和数据并行系统。
  - GPT-3 的训练系统的细节仍然未知，但它们至少在一定程度上使用了模型并行（一些人称它使用了 Ray）。不同的训练系统和硬件可能导致不同的训练时的现象。显然，一些在 PaLM 的文章中呈现的、用于 TPU 训练的设置，可能并不适用于其它所有模型使用的 GPU 训练。
  - 硬件和训练框架的一个重要的影响是，人们是否可以使用 bfloat16 去存储模型权重和中间层激活值等。这已经被证明是稳定训练的一个重要因素，因为 bfloat16 可以表示更大范围的浮点数，能够处理在损失尖峰时出现的大数值。在 TPU 上 bfloat16 是默认设置，这可能是 PaLM 能够成功的一个秘密。但是在 GPU 上，以前人们主要使用 float16，这是 V100 中混合精度训练的唯一选择。
  - `OPT` 使用了 float16，这可能是其不稳定的因素之一。BLOOM 发现了这样的问题并最终在 A100GPU 上使用了 bfloat16，但它没有意识到这种设置的重要性，因此在第一个词向量层后引入额外的`层归一化`（layer normalization），用于解决他们使用 float16 的初步实验中的不稳定性。然而，这种层归一化已被证明会导致更糟糕的`零样本泛化`（zero-shot generalization），这可能是 BLOOM 失败的一个因素。
2. 训练过程中的修改。OPT 做了很多中途调整并从最近的 checkpoint 重启训练，包括改变`截断梯度范数` (clip gradient norm) 和学习率，切换到简单的 SGD 优化器然后回到 Adam，重置`动态损失标量` (dynamic loss scalar)，切换到更新版本的 Megatron 等等。
  - 这种中途调整可能是 OPT 失败的原因之一。相比之下，PaLM 几乎没有做任何中途调整。它只是当损失尖峰出现时，从尖峰开始前大约 100 步的 checkpoint 重新开始训练，并跳过了大约 200-500 个 batch 的数据。仅仅依靠这种简单的重启，PaLM 就取得神奇的成功。这是由于它在预训练数据构建期间就已经完成采样，因此模型具有在 Bit 意义上的确定性，以及它对模型架构和训练设置进行了许多修改以获得更好的稳定性。PaLM 中的此类修改在下一点中展示。
3. 模型架构 / 训练设置：为了使训练更稳定，PaLM 对模型架构和训练设置进行了多项调整，包括使用 Adafactor 的修改版本作为优化器，缩放在 softmax 之前的输出 logit，使用辅助损失来鼓励 softmax 归一化器接近 0，对词向量和其他层权重使用不同的初始化，在前馈层和层归一化中不使用偏差项，并且在预训练期间不使用 dropout。
  - 注意，GLM-130B 中还有更多有价值的内容关于如何稳定地训练非常大的模型，例如：使用基于 DeepNorm 的后置层归一化而不是前置层归一化，以及词向量层梯度收缩。以上大多数模型修改没有被 OPT 和 BLOOM 采用，这可能会导致它们的不稳定和失败。

4. 训练过程：如下表所示，原始的 GPT-3 预训练过程见过的 token 数与 OPT 和 BLOOM 接近，而 PaLM 则远远超过了它们。同样，PaLM 和 GPT-3 预训练语料库都大于 BLOOM 和 OPT。因此，在更多的 token 上、用更大规模的高质量语料库进行预训练可能是 GPT-3 和 PaLM 成功的一个重要因素。


除了上面列出的四点，还有一些其它因素，它们可能对于更稳定的训练并不重要，但仍然可能影响最终的性能。
- 第一点，PaLM 和 GPT-3 都使用了在训练过程中从小到大逐渐增加的 batch size，这已经被展示对于训练一个更好的 LLM 是有效的，然而 OPT 和 BLOOM 都使用了恒定的 batch size。
- 第二点，OPT 使用了 ReLU 激活函数，而 PaLM 使用 SwiGLU 激活函数，GPT-3 和 BLOOM 使用 GeLU，它通常使得训练的 LLM 的性能更好。
- 第三点，为了更好的建模更长的序列，PaLM 使用 RoPE 词向量，BLOOM 使用 ALiBi 词向量，而原始的 GPT-3 和 OPT 使用学习得到的词向量，这可能影响在长序列上的性能。

在哪些任务和应用上使用 GPT-3?

理想情形下，如果微调 GPT-3 的负担是能够承担的，它可能带来更进一步的提升。然而，在一些任务上通过微调 PaLM-540B 带来的提升是如此有限，让人们怀疑在一些任务中微调 GPT-3 是否是值得的。从科学的角度来看，更公平的比较应在微调 GPT-3 和提示 GPT-3 之间进行。然而，要使用 GPT-3，人们可能更关心将提示 GPT-3 和微调一个更小的模型去进行对比。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/51490798d52c4594a27203a3f276d941~noop.image?_iz=58558&from=article.pc_detail&x-expires=1677646924&x-signature=KzYUDIV4mIZCirmKFJYBcDUeD9c%3D)

适合使用提示 GPT-3
1. 创造性和复杂的任务：包括代码（代码补全、自然语言指令生成代码、代码翻译、bug 修复）、文本摘要、翻译、创造性写作（例如写故事、文章、邮件、报告，以及写作的改进等）。正如原始的 GPT-3 文献中所示，GPT-3 被设计用于那些困难和 “不可能标注” 的任务。在一定程度上，对于这些任务，先前那种经过微调的模型不可能应用于真实世界的应用；而 GPT-3 使它们成为可能。举个例子，最近的文章显示，过去的人类标注的文本摘要已经被 LLM 生成的摘要所超越。
  - 在某些需要从低、中资源语言翻译到英语的机器翻译任务中，通过提示 PaLM-540B，它甚至能够超越微调模型。
  - 在 BLOOM-176B 中也观察到了类似的趋势。这是因为英语数据通常在预训练语料库中占了很大比例，因此 LLM 擅长于生成英语语句。注意到，为了在代码任务中获得良好性能，尽管 Codex 和 PaLM 已经在整体上具有比之前模型更好的性能，我们仍然需允许 LLM 多次（k 次）采样，以通过测试样例（使用 pass@k 作为度量）。
2. 只有少数标注或者没有标注数据的任务。正如原始的 GPT-3 文献所说，GPT-3 是为了那些 “昂贵标注” 的任务设计的。在这种情况下，用极少量标注数据微调一个更小的模型通常不可能达到 GPT-3 在零样本（zero-shot）、单样本（ont-shot）或少样本（few-shot）的情况下的表现。
3. 分布外（Out-of-distribution, OOD）泛化。给定一些训练数据，传统的微调可能会过拟合训练集并且有较差的分布外泛化能力；而少样本的上下文学习（in-context learning）能够有更好的分布外泛化性。例如，带有提示的 PaLM 能够在对抗自然语言推断任务（Adversarial Natural Language Inference，ANLI）上超越经过微调的 SOTA 模型，而它在正常的语言推断任务上可能仍然劣于微调的 SOTA。
  - 另一个例子是提示 LLM 比微调模型显示出更好的组合泛化能力。更好的分布外泛化性可能是因为在上下文学习期间不需要更新参数，避免了过拟合；或者因为那些过去的分布外样例对于 LLM 而言是分布内的。这种使用场景被阐释为 GPT-3 的初始设计目标之一：“微调模型在特定任务的数据集上的性能可以达到所谓的人类水平，实际上可能夸大了在真实世界中该任务上的性能，这是因为模型只是学到了训练集中存在的虚假的相关性，以及模型过度拟合了这个训练集狭窄的分布。”
4. 需要处理多种任务的能力，而非关注特定任务上的卓越表现。聊天机器人就是这样一种场景，其中，用户期待它能够正确地响应各种各样的任务。这可能就是为什么 ChatGPT 是 GPT-3 最成功的使用场景之一。
5. 那些检索不可行的知识密集型任务。存储在 LLM 中的知识可以显著地提高在知识密集型任务的性能，例如闭卷问答和 MMLU（一个基准数据集，包括来自于 STEM、人文、社科等 57 个学科的选择题，它用于测试 LLM 的世界知识和问题解答的能力）。然而，如果预先检索的步骤可以被加入来做检索增强的生成，一个微调的更小的模型（例如 Atlas 模型）甚至可以有更好的性能（在闭卷的 NaturalQuestions 和 TrivialQA 数据集上，Atlas 比 PaLM 和最新的 InstructGPT 都要更好）。
  - 检索或者传统的搜索同样是将 GPT-3 或 ChatGPT 整合到搜索引擎中的一个必要的步骤，这可以提升生成的准确性，并且提供更多的参考链接以增强说服力。但我们应该承认，在某些情况下，检索是不允许或者不容易的，比如参加 USMLE (美国医学执照考试)，谷歌已经证明基于 FLAN-PaLM 的模型可以在其中做得很好。
  - 同样的，在 MMLU 基准集中，PaLM-540B 有着比其他微调模型更好的性能，甚至后者结合了检索，尽管最新版本的 InstructGPT 还差于这些带有检索的微调 SOTA。也请注意，指令调整一个较小的模型也可以实现与更大规模的 LLM 模型接近的效果，这已经在 FLAN-T5 中展现。
6. 一些困难的任务，其中需要 LLM 的涌现能力，比如带有 CoT 的推理和 BIG-Bench 中的复杂任务（包括逻辑推理、翻译、问答、数学任务等）。举个例子，PaLM 已经展示，在 7 个包括数学和常识推理的多步推理任务上，8 - 样例的 CoT 比微调 SOTA 在其中 4 个任务上更好，在其它 3 个任务上则基本持平。
  - 这样的成功表现要同时归因于更大规模的模型和 CoT。PaLM 还显示了在 BIG-Bench 任务上从 8B 到 62B 再到 540B 模型的不连续的表现提升，这超出了规模定律（scailing law），被称为 LLMs 的涌现能力。另外，带有 5 个 Prompt 的 PaLM-540B 在 Big-Bench 的 58 项常见任务中的 44 项上优于之前的（少样本）SOTA。PaLM-540B 在 Big-Bench 的总体表现也优于人类的平均表现。
7. 一些需要模仿人类的场景，或者是其目标是制作性能达到人类水平的通用人工智能。同样的，ChatGPT 是其中的一个案例，ChatGPT 使自己更像是一个人，从而取得了现象级的成功。这也被阐释为 GPT-3 的初始设计目标之一：“人类不需要大规模监督数据集来学习大多数语言任务。最多只需要几个例子，人类就可以将各种任务和技巧无缝地混合在一起或者在它们之间切换。因此传统的微调模型导致了与人类的不公平比较，尽管他们声称在许多基准数据集中有着人类水平的性能。”
8. 在一些传统的接近于语言建模的 NLP 任务上，少样本 PaLM-540B 能够大致匹配或者甚至超过微调的 SOTA，例如：一段话最后一句和最后一个单词的完型填空，以及回指（anaphora）解析。需要指出，在这种情况下，零样本的 LLM 已经足够了，单样本或少样本的示例则通常帮助不大。

另一些任务则并不需要提示（prompt）一个 GPT-3 这样规模的模型：

不适合使用GPT-3的任务
1. 调用 OpenAI GPT-3 的 API 超出了预算（例如对于没有太多钱的创业公司）。
2. 调用 OpenAI GPT-3 的 API 存在安全问题（例如数据泄露给 OpenAI，或者可能生成的有害内容）。
3. 没有足够的工程或者硬件资源去部署一个相似大小的模型及消除推断的延迟问题。例如，在没有最先进的 80G 的 A100 或者工程资源来优化推断速度的情况下，简单地使用 Alpa 在 16 个 40G 的 A100 上部署 OPT-175B 需要 10 秒才能完成单个样例的推断，这对于大多数现实世界的在线应用程序来说是无法接受的延迟。
4. 如果想用 GPT-3 替代一个性能良好的、高准确度的微调模型，或者想要在一些特定的单一任务和使用场景下去部署一个 NLU（Natural Language Understanding，自然语言理解）或 NLG（Natural Language Generating，自然语言生成）模型，请三思这是否值得。

对于一些传统的 NLU 任务，比如分类任务，我建议首先尝试微调 FLAN-T5-11B 模型，而不是提示 GPT-3。例如，在 SuperGLUE，一个困难的 NLU 基准数据集（包括阅读理解、文本蕴含、词义消歧、共指消解和因果推理等任务）上，所有的 PaLM-540B 的少样本提示性能都劣于微调的 T5-11B，并在其中大多数任务上有着显著的差距。如果使用原始 GPT3，其提示结果与微调 SOTA 的结果之间的差距更大。有趣的是，即使是经过微调的 PaLM 也仅比经过微调的 T5-11B 有着有限的改进，而经过微调的 PaLM 甚至比经过微调的编 - 解码器模型 32B MoE 模型还要差。这表明使用更合适的架构（例如编 - 解码器模型）微调较小的模型仍然是比使用非常大的仅解码器模型更好的解决方案，无论是微调还是提示来使用这些大模型。根据最近的一篇论文，即使对于最传统的 NLU 分类任务 —— 情感分析，ChatGPT 仍然比经过微调的较小模型差。

一些不以现实世界数据为基础的困难任务。例如，BigBench 中仍然有许多对 LLM 来说困难的任务。具体地说，在 35% 的 BigBench 任务上，人类的平均表现仍然高于 PaLM-540B，并且在某些任务中，扩大模型规模甚至无济于事，例如导航和数学归纳。在数学归纳中，当提示中的假设不正确时（例如 “2 是奇数”），PaLM 会犯很多错误。在`逆规模定律`竞赛 (`Inverse Scaling Law` Challenge) 中，也观察到了类似的趋势，例如重新定义数学符号（例如提示可能 “将 π 重新定义为 462”）后再使用这个符号。在这种情况下，LLM 中的现实世界先验知识太强而无法被提示覆盖，而微调较小的模型可能可以更好地学习这些反事实知识。

在很多多语言任务和机器翻译任务中，使用少样本的提示 GPT 仍然要比微调的更小的模型更差。这很可能是由于除英语之外的其它语言在预训练语料库中占比很少。

当从英语翻译为其他语言，以及翻译高资源语言到英语时，PaLM 和 ChatGPT 仍然比在机器翻译任务上微调的更小的模型要差。
- 对于多语言问答任务来说，在少样本的 PaLM-540B 和微调的更小模型之间还存在较大差距。
- 对于多语言文本生成（包括文本摘要和数据到文本生成），在少样本的 PaLM-540B 和微调的更小模型之间还存在较大差距。在大部分任务上即使微调的 PaLM-540B 也仅仅比微调的 T5-11B 有有限的提升，并仍然劣于微调的 SOTA。
- 对于常识推理任务，在最好的少样本提示 LLM 和微调的 SOTA 之间仍然存在着较大的差距，例如：OpenbookQA，ARC（包括 Easy 和 Challenge 版本）以及 CommonsenseQA（甚至使用了 CoT 提示）。
- 对于机器阅读理解任务，在最好的少样本提示 LLM 和微调的 SOTA 之间仍然存在着较大的差距。在大多数数据集上，这个差距可能非常巨大。这可能是因为所有回答问题所需的知识都已经包含在给出的文本中，并不需要 LLM 中的额外知识。

总结一下，上面的这些任务可以被归为以下类别之一：
1. 一些 NLU 任务，既不需要额外的知识也不需要 LLM 的生成能力。这意味着测试数据大多数都和手头的训练数据在同一个分布之中。在这些任务上，过去微调的较小模型已经表现很好了。
2. 一些不需要额外的来自 LLM 中知识的任务，因为每一个例子已经在上下文或者提示中包含了足够的知识，例如机器阅读理解。
3. 一些需要额外知识，但不太可能从 LLM 中获得这样的知识，或者 LLM 不太可能见过类似分布的任务，例如一些低资源语言中的任务，LLM 在这些语言中只有有限的预训练样本。
4. 一些任务，需要与 LLM 中包含的知识所不一致的知识，或者并非基于现实世界的语言数据的知识。因为 LLM 是在现实世界的语言数据上训练的，它难以在新的任务中利用反事实知识覆盖原有知识。除了在逆规模定律挑战中的 “重新定义数学符号” 问题之外，还有另一个任务，即复述有细微改动的名言，其中 LLM 被要求复述一个在 prompt 中出现的被修改的名言。在这种情况下，LLM 倾向于重复出名言的原始版本，而非修改过后的版本。
5. 一些任务需要来自 LM 的知识，但也严重依赖于操纵这些知识，而 LLM 的 “预测下一个 token” 的目标无法轻易实现这种操纵。一个例子是一些常识推理任务。CoT 和 least-to-most 提示可以帮助 LLM 推理的原因可能是他们可以更好地调出那些连续的预训练文本，这些连续文本恰好模仿了规划和分解 / 组合知识的过程。
  - 因此，CoT 和 least-to-most 提示在一些数学推理、代码和其他简单的自然语言推理任务中表现良好，但在许多常识推理（例如在逆规模定律竞赛中展示的演绎推理任务）和自定义符号推理任务中仍然表现不佳。这些任务通常不被自然语言数据中的大多数真实世界的连续序列所包含，而需要操纵分散在各处的知识来完成。
6. 一些容易受到上下文学习样例或者真实世界数据中存在的虚假相关性影响的任务。一个例子是来自于逆规模定律竞赛中的涉及否定词的问答。如果一个 LLM 被提问：“如果一只猫的体温低于平均水平，它就不在……”，它倾向于回答 “危险之中” 而非 “安全范围 “。这是因为 LLM 受到常见的 “低于平均体温” 和 “危险” 之间的关系所支配，而在否定的情况下，这是一种虚假的相关性。
7. 一些目标与处理语言数据显著不同的任务，例如：回归问题，其中微调模型很难被 LLM 取代。至于多模态任务，它们不能被 LLM 解决，但是可能能从大规模的预训练多模态模型中受益。
8. 一些任务不需要 LLM 的涌现能力。为了准确地对更多此类任务进行鉴别，我们需要更好地了解 LLM 训练期间，涌现能力是从何产生的。

注意到，在现实世界的使用场景中，即使由于无法满足延迟要求因而无法在线地使用 LLM，仍然可以使用 LLM 离线生成或标注数据。此类自动标注的标签可以在线查找并提供给用户，或用于微调较小的模型。使用此类数据微调较小的模型可以减少训练模型所需的人工注释数据，并将 LLM 的一些新兴能力（例如 CoT）注入较小的模型。

总之，当有足够的标记数据时，考虑到开源 FLAN-T5 在许多任务中的惊人性能，我推荐那些调用 OpenAI API 的资源有限的个体，应该首先尝试在目标任务上微调 FLAN-T5-11B。此外，根据最近在 MMLU 数据集上，FLAN-PaLM-540B 与最新版本的 InstructGPT 的性能（根据 HELM）相比好得惊人的性能，谷歌可能拥有比 OpenAI 更强大的基础模型，如果 OpenAI 已经通过 API 发布了他们获得的最强的 LLM。

谷歌唯一剩下的步骤是通过人类反馈使这个 LLM 与对话场景对齐（alignment）。如果他们很快发布类似 ChatGPT 的或者更好的聊天机器人，我不会感到惊讶 —— 尽管他们最近 “失败” 地展示了一版可能基于 LaMDA 的 Bard。



## LLM

大模型越烧越旺
- 3月13日，斯坦福发布[LLaMA模型改进版](https://github.com/tatsu-lab/stanford_alpaca)
- 3月14日，清华发布[ChatGLM-6B模型](https://github.com/THUDM/ChatGLM-6B)
- 3月14日，OpenAI发布[GPT4模型](https://openai.com/product/gpt-4)
- 3月14日，谷歌给出[PaLM API](https://blog.google/technology/ai/ai-developers-google-cloud-workspace/)
- 3月15日，[PyTorch2.0发布](https://pytorch.org/blog/pytorch-2.0-release/)
- 3月16日，微软发布[Microsoft 365 Copilot](https://blogs.microsoft.com/blog/2023/03/16/introducing-microsoft-365-copilot-your-copilot-for-work/)
- 3月16日，百度发布[文心一言](https://yiyan.baidu.com/welcome)
- 3月22日，谷歌发布BARD内测

详情见站内专题：[大模型沉思录](llm)


### 资讯总结

【2023-6-13】LLM 里程碑论文及各大模型信息, pretrain、instruct、对齐、开源模型等维度汇总LLM
- [Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM)
- ![](https://github.com/Mooler0410/LLMsPracticalGuide/raw/main/imgs/survey-gif-test.gif)

【2023-6-10】[DAIR.AI](github.com/dair-ai/ML-Papers-of-the-Week)，每周热门论文

[LLM CheatSheet](https://github.com/Abonia1/CheatSheet-LLM), 含 ppt、pdf和png格式
- ![](https://raw.githubusercontent.com/ashishpatel26/CheatSheet-LLM/main/Images/Slide3.PNG)

【2023-4-4】[GPT fine-tune实战：训练我自己的 ChatGPT](https://zhuanlan.zhihu.com/p/616504594)
- Stanford 基于 LLaMA 的 Alpaca 和随后出现的 LoRA 版本 Alpaca-LoRA。原因很简单，便宜。
- Alpaca 宣称只需要 600$ 不到的成本（包括创建数据集），便可以让 LLaMA 7B 达到近似 text-davinci-003 的效果。而 Alpaca-LoRA 则在此基础上，让我们能够以一块消费级显卡，在几小时内完成 7B 模型的 fine-turning。
- fine-tune 7B 模型仅需要 8-10 GB vram。


### 基座大模型


#### LLMs 进化史

【2023-6-9】大模型进化史
- 论文：[A Survey of Large Language Models](https://arxiv.org/abs/2303.18223)
  - 解读：[从T5到GPT-4最全盘点，国内20余位研究者联合撰写](https://www.jiqizhixin.com/articles/2023-04-03)
- 2019 年以来出现的各种大语言模型（百亿参数以上）时间轴，其中标黄的大模型已开源。
- ![img](https://image.jiqizhixin.com/uploads/editor/9499e39a-1e5d-4395-bf4b-70ee1e81f908/640.png)
- 详见站内专题：[大语言模型演变](https://wqw547243068.github.io/plm#%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E6%BC%94%E5%8F%98)

【2023-6-21】[LLMsPracticalGuide](https://github.com/Mooler0410/LLMsPracticalGuide)
- 论文解读：[一文带你理清全球AI巨头的大模型进化史](https://zhuanlan.zhihu.com/p/638455866)

`Transformer` 开创了继 `MLP` 、`CNN` 和 `RNN`之后的第4大类模型。

基于Transformer结构的模型又可以分为`Encoder-only`、`Decoder-only`、`Encoder-Decoder`这三类。
- 仅`编码器`架构（Encoder-only）：`自编码`模型（破坏一个句子，然后让模型去预测或填补），更擅长理解类的任务，例如：文本分类、实体识别、关键信息抽取等。典型代表有：Bert、RoBERTa等。
- 仅`解码器`架构（Decoder-only）：`自回归`模型（将解码器自己当前步的输出加入下一步的输入，解码器融合所有已经输入的向量来输出下一个向量，所以越往后的输出考虑了更多输入），更擅长生成类的任务，例如：**文本生成**。典型代表有：GPT系列、LLaMA、OPT、Bloom等。
- `编码器-解码器`架构（Encoder-Decoder）：`序列到序列`模型（编码器的输出作为解码器的输入），主要用于**条件生成**任务，例如：翻译，概要等。典型代表有：T5、BART、GLM等。

三种主流模型架构的对比图，包括`因果编码器`、`前缀解码器`和`编码器-解码器`架构
- ![对比图](https://pic3.zhimg.com/80/v2-ff064f94544815dfa4e1b137c0bdf356_1440w.webp)

模型架构的各组件细节，包括分词、归一化方法、归一化位置、位置编码、注意力与偏置等等，并提供了Transformer架构多种配置的详细公式表。
- ![](https://pic2.zhimg.com/80/v2-fa833508b5a27fd8a36775b911800951_1440w.webp)

LLM选择决策树
- ![](https://github.com/Mooler0410/LLMsPracticalGuide/blob/main/imgs/decision.png)

decoder-only LLM一般是指以LM objective训练的模型，即编码每个token时只能单向地利用「前文tokens」或「后文tokens」信息，比如，一个left-to-right LM objective可以表示为：
- $$L(\theta) = - {1 \over N}\sum^{N}_{i}log(p(x_i; \theta)) \\ = - {1 \over N}\sum^{N}_{i}\sum^{T_i}_{t}log(p(w_{i,t}|w_{i, < t}; \theta))$$

GPT模型进化
- ![](https://github.com/RUCAIBox/LLMSurvey/blob/main/assets/gpt-series.png?raw=true)

#### LLMs 对比


【2024-1-23】[choose the best model and API hosting provider for your use-case](https://artificialanalysis.ai/), 全方位对比各大主流模型，涉及：模型质量、速度、价格

各种模型详情

| LLMs<br>大模型 | Model Arch<br>模型架构 |	License<br>协议	| Commercial Use<br>商用许可 |	Other noteable restrictions<br>其它限制 |	Data License<br>数据许可	| Corpus<br>训练语料 |
| --- | --- |	---	| --- |	--- |	---	| --- |
| BERT series | Encoder-only	| Apache 2.0 | ✅	| -|	Public | BooksCorpus, English Wikipedia |
| RoBERTa     | Encoder-only  |	MIT license	| ✅ |	- |	Public	| BookCorpus, CC-News, OpenWebText, STORIES |
| ERNIE       | Encoder-only  |	Apache 2.0	| ✅ |	- |	Public	| 	English Wikipedia |
| SciBERT     | Encoder-only  |	Apache 2.0	| ✅ |	- |	Public	| BERT corpus, [1.14M papers from Semantic Scholar](https://aclanthology.org/N18-3011.pdf) |
| LegalBERT   | Encoder-only  |	CC BY-SA 4.0	| ❌ |	- |	Public<br>except data from the [Case Law Access Project](https://case.law/)	| EU legislation, US court cases, etc. |
| BioBERT     | Encoder-only  |	Apache 2.0	| ✅ |	- |	[PubMed](https://www.nlm.nih.gov/databases/download/terms_and_conditions.html)	| 	PubMed, PMC|
| T5          | Encoder-Decoder |	Apache 2.0	| ✅ |	- |	Public	| C4 |
| Flan-T5     | Encoder-Decoder |	Apache 2.0	| ✅ |	- |	Public	| C4, Mixture of tasks |
| BART        | Encoder-Decoder |	Apache 2.0	| ✅ |	- |	Public	| RoBERTa corpus |
| GLM         | Encoder-Decoder |	Apache 2.0	| ✅ |	- |	Public	| BooksCorpus and English Wikipedia |
| ChatGLM     | Encoder-Decoder |	[ChatGLM License](https://github.com/THUDM/ChatGLM-6B/blob/main/MODEL_LICENSE)	| ❌ |	No use for illegal purposes or military research<br>No harm the public interest of society |	N/A	| 1T tokens of Chinese and English corpus |
| GPT-2   | Decoder-only |	[Modified MIT License](https://github.com/openai/gpt-2/blob/master/LICENSE)	|	✅ | Use GPT-2 responsibly and clearly indicate your content was created using GPT-2.  |	Public	| WebText |
| GPT-Neo | Decoder-only |	MIT license	|	✅ | -  |	Public	| [Pile](https://pile.eleuther.ai/) |
| GPT-J   | Decoder-only |	Apache 2.0	|	✅ | -  |	Public	| [Pile](https://pile.eleuther.ai/) |
| -> Dolly | Decoder-only |	CC BY NC 4.0	|	❌ | - | CC BY NC 4.0, Subject to terms of Use of the data generated by OpenAI  |	[Pile](https://pile.eleuther.ai/), Self-Instruct |
| -> GPT4ALL-J | Decoder-only |	Apache 2.0	|	✅ | - |	Public	| [GPT4All-J dataset](https://huggingface.co/datasets/nomic-ai/gpt4all-j-prompt-generations) |
| Pythia | Decoder-only |	Apache 2.0	|	✅ | -  |	Public	| [Pile](https://pile.eleuther.ai/) |
| -> Dolly v2 | Decoder-only |	MIT license	|	✅ | -  |	Public	| [Pile](https://pile.eleuther.ai/), databricks-dolly-15k |
| OPT | Decoder-only |	[OPT-175B LICENSE AGREEMENT](https://github.com/facebookresearch/metaseq/blob/main/projects/OPT/MODEL_LICENSE.md?fbclid=IwAR1BFK5X1XdUpx_QXoiqyfzYWdNAXJPcg8Cf0ddv5T7sa2UrLUvymj1J8G4)	|	❌ | No development relating to surveillance research and military, no harm the public interest of society |	Public	| RoBERTa corpus, the Pile, PushShift.io Reddit |
| -> OPT-IML | Decoder-only |	same to OPT	|	❌ | sampe to OPT  |	Public	| OPT corpus, Extended version of Super-NaturalInstructions |
| YaLM | Decoder-only |	Apache 2.0	|	✅ | -  |	Unspecified	| Pile, Teams collected Texts in Russian |
| BLOOM | Decoder-only |	[The BigScience RAIL License](https://bigscience.huggingface.co/blog/the-bigscience-rail-license)	|	✅ | No use of generating verifiably false information with the purpose of harming others; content without expressly disclaiming that the text is machine generated  |	Public	| ROOTS corpus (Lauren¸con et al., 2022) |
| -> BLOOMZ | Decoder-only |	same to BLOOM	|	✅ | same to BLOOM  |	Public	| ROOTS corpus, xP3 |
| Galactica | Decoder-only |	[CC BY-NC 4.0](https://github.com/paperswithcode/galai/blob/main/LICENSE-MODEL.md)	|	❌ | -  |	N/A	| The Galactica Corpus |
| LLaMA | Decoder-only |	[Non-commercial bespoke license](https://docs.google.com/forms/d/e/1FAIpQLSfqNECQnMkycAp2jP4Z9TFX0cGR4uf7b_fBxjY_OjhJILlKGA/viewform)	|	❌ | No development relating to surveillance research and military, no harm the public interest of society  |	Public	| CommonCrawl, C4, Github, Wikipedia, etc. |
| -> Alpaca | Decoder-only |	CC BY NC 4.0	|	❌ | -  |	CC BY NC 4.0, Subject to terms of Use of the data generated by OpenAI	| LLaMA corpus, Self-Instruct |
| -> Vicuna | Decoder-only |	CC BY NC 4.0	|	❌ | -  |	Subject to terms of Use of the data generated by OpenAI; Privacy Practices of ShareGPT	| LLaMA corpus, 70K conversations from ShareGPT.com |
| -> GPT4ALL | Decoder-only |	GPL Licensed LLaMa	|	❌ | -  |	Public	| [GPT4All dataset](https://huggingface.co/datasets/nomic-ai/gpt4all_prompt_generations) |
| OpenLLaMA | Decoder-only |	Apache 2.0	|	✅ | -  |	Public	| [RedPajama](https://www.together.xyz/blog/redpajama) |
| CodeGeeX | Decoder-only |	[The CodeGeeX License](https://github.com/THUDM/CodeGeeX/blob/main/MODEL_LICENSE)	|	❌ | No use for illegal purposes or military research  |	Public	| Pile, CodeParrot, etc. |
| StarCoder | Decoder-only |	[BigCode OpenRAIL-M v1 license](https://huggingface.co/spaces/bigcode/bigcode-model-license-agreement)	|	✅ | No use of generating verifiably false information with the purpose of harming others; content without expressly disclaiming that the text is machine generated |	Public	| [The Stack](https://arxiv.org/pdf/2211.15533.pdf) |
| MPT-7B | Decoder-only |	Apache 2.0	|	✅ | -  |	Public	| [mC4 (english)](https://arxiv.org/abs/2010.11934), [The Stack](https://arxiv.org/pdf/2211.15533.pdf), [RedPajama](https://www.together.xyz/blog/redpajama), [S2ORC](https://aclanthology.org/2020.acl-main.447/) |
| [falcon](https://huggingface.co/tiiuae/falcon-40b) | Decoder-only |	[TII Falcon LLM License](https://huggingface.co/tiiuae/falcon-40b/blob/main/LICENSE.txt)	|	✅/❌ | Available under a license allowing commercial use  |	Public	| [RefinedWeb](https://huggingface.co/datasets/tiiuae/falcon-refinedweb) |
| - | - |	-	| -|	- |	-	| - |
| - | - |	-	| -|	- |	-	| - |


### 开源大模型

主流大模型都是 Transformer、MOE结构 为基础进行构建
- `Transformer` 结构使得模型突破到**上亿**参数量
- `MoE` **稀疏混合专家**结构使模型参数量产生进一步突破，达到数**万亿**规模。

#### 开源LLM

开源大语言模型主要有三大类：
- `GLM`衍生的大模型（wenda、ChatSQL等）
- `LLaMA`衍生的大模型（Alpaca、Vicuna、BELLE、Phoenix、Chimera等）
- `Bloom`衍生的大模型（Bloomz、BELLE、Phoenix等）

LLaMA无疑是其中最闪亮的星。但是国内关于LLaMA比较大的一个争论: 
- LLaMA是以英语为主要语言的拉丁语系上进行训练的，LLaMA词表中的中文token比较少（只有几百个）

| 模型	| 训练数据量	| 模型参数	| 训练数据范围	| 词表大小 |
| ---	| ---	| ---	| ---	| --- |
| LLaMA	| 1T～1.4T tokens(其中，7B/13B使用1T，33B/65B使用1.4T)	| 7B～65B	| 以英语为主要语言的拉丁语系	| 32000 | 
| ChatGLM-6B | 约 1T tokens |	6B	| 中文、英语	| 130528 |
| Bloom	  | 1.6TB预处理文本，转换为 350B 唯一 tokens |	6B	| 46种自然语言，13种编程语言 |	250680 |

对于像ChatGLM-6B、LLaMA、Bloom这类大模型，要保证基座模型有比较好的效果，至少需要保证上千亿、万亿级的Token量

大模型汇总

|模型|作者|时间|规模|语料|是否开源|可用性|
|---|---|---|---|---|---|---|
|GPT-3系列|OpenAI||1750亿|-|否|API|
|LaMDA|Google|？||？|否|否|
|OPT|Meta|2022年5月|1750亿|？|是|是|
|BLOOM|Big Science<br>French National Center|2022年7月|1760亿|46种语言|是|是，huggingface上,训练117天，用于|
|Sparrow|||||||

colossalai 训练多个大模型，提升效率，参考：[是否有更高效的大模型训练方法](https://github.com/hpcaitech/ColossalAI/discussions/2335)
- `GLM-130` 26%~30%
- `GPT3` 21.3%
- Gopher 32.5%
- Turing 30.2%
- `BLOOM` 35.6%
- `OPT` 36.7%
- PaLM 46.2%

大模型中，具备可比性的是`BLOOM`和`OPT`（GPT架构，A100 80G）

总结
- OpenAI 开发的 GPT-3 并不开源；
- Meta 开发的 OPT-175B 虽然开源，但完整模型只有在提出申请后才能获得，并且只能用于非商业用途。
- 而 Bloom 就完全不同，并没有这些限制，任何个人或机构都可以免费获得 1760 亿个参数的完整模型。

严格复刻`GPT-3`方案并开放模型
- 国外
  - [eleuther.ai](https://www.eleuther.ai/)，其于huggingface平台提供的finetune和推理接口，目前提供的版本如下：[img](https://pic3.zhimg.com/80/v2-cc9a9cd551730b1144af5ec4eb8aecfa_1440w.webp)
  - facebook 对标gpt-3开放了`opt`模型，其于huggingface平台提供的finetune和推理接口
- 国内
  - `阿里达摩院`，其于modelscope平台提供的finetune和推理接口，目前提供的版本如下：[img](https://pic3.zhimg.com/80/v2-3e6b687dbeea0bfaca523a0b9d228532_1440w.webp)

#### 可商用LLM

【2024-3-1】

| 序号 | 模型名称 | 下载地址 | 许可证 | 许可证类型 | 使用提示及注意事项 |
| --- | --- | --- | --- | --- | --- |
| 1 | LLAMA | [地址](https://research.facebook.com/publications/llama-open-and-efficient-foundation-language-models) | noncommercial license | 禁止商用 | 不可商用，就算纯内部使用、仅作为训练初始参数也不建议。学术可以 |
| 1 | Llama 2 | [地址](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) | LLAMA 2 COMMUNITY LICENSE AGREEMENT | 禁止大规模商用；学术使用需要单独评估 | 月活超过7亿的主体不可使用，当前请不要填表申请；|
| 1 | Code llama | [地址](https://about.fb.com/news/2023/08/code-llama-ai-for-coding/) | LLAMA 2 COMMUNITY LICENSE AGREEMENT | 同上（Llama 2）
| 1 | open_llama | [open_llama_3b](https://huggingface.co/openlm-research/open_llama_3b), [open_llama_7b](https://huggingface.co/openlm-research/open_llama_7b), [open_llama_13b](https://huggingface.co/openlm-research/open_llama_13b) | Apache 2.0 | 允许商用，基本无限制<br>没有特别限制，如果涉及到将模型部署到公司之外，需要法务评审。
| 1 | Chinese-LLaMa-Alpaca | [Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca), [Chinese-LLaMA-Alpaca-2](https://github.com/ymcui/Chinese-LLaMA-Alpaca-2) | LLAMA 2 COMMUNITY LICENSE AGREEMENT 或者禁止商用 | 不允许商用or 禁止字节商用 | Chinese-LLaMa-Alpaca 1不允许商用；<br>Chinese-LLaMa-Alpaca 2本身是LORA，由于该LORA使用需要配合llama 2，且llama 2不允许商用<br>所以可能实质上没有办法商用Chinese-LLaMa-Alpaca-2 |
| 1 | CogVLM-17B | [CogVLM](https://github.com/THUDM/CogVLM) | LLAMA 2 COMMUNITY LICENSE AGREEMENT的限制同时适用 | 禁止商用，学术使用需要单独评估 |
| 2 | glm | [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)<br>[ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)<br>[ChatGLM3](https://github.com/THUDM/ChatGLM3) (2023.11.03更新) | The ChatGLM-6B License | 允许商用，但是填写问卷进行申请 | 目前智谱已经开放了问卷申请，建议填写问卷重新申请。|
| 3 | Stable diffision | [CompVis](https://huggingface.co/CompVis) | Open RAIL-M |  允许商用但需要声明 | 1. 内部使用作为提效工具，接口/服务本身不对外暴露，没有额外义务，但是不能用于非法、歧视等不正当目的；<br>2. 提供接口供外部调用生成图片的，需要完成声明义务，具体参考Stable Diffusion 的许可证合规指引 ；<br>3. [CompVis](https://huggingface.co/CompVis) 包括多个细分模型的参数，凡是许可证为The CreativeML OpenRAIL M license均受到上述限制；<br>4. [civitai](https://civitai.com/) 上的SD衍生模型有可能有额外限制，即使内容使用也需要评审；
| 4 | Dolly 2.0 | [dolly](https://www.databricks.com/blog/2023/03/24/hello-dolly-democratizing-magic-chatgpt-open-models.html), [databricks-dolly-15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k/tree/main) | cc-by-sa-3.0 | 允许商用，基本无限制 | 没有特别限制，如果涉及到将模型部署到公司之外，法务评审。|
| 5 | RedPajama | [redpajama](https://together.ai/blog/redpajama-models-v1) | Apache 2.0 | 允许商用，基本无限制 | 没有特别限制，如果涉及到将模型部署到公司之外，法务评审。| 
| 6 | bloomz |[bloomz](https://huggingface.co/bigscience/bloomz),<br>[bloomz-1b7](https://huggingface.co/bigscience/bloomz-1b7),<br>[bloom-1b7](https://huggingface.co/bigscience/bloom-1b7) | bigscience-bloom-rail-1.0 | 允许商用但需要登记和声明 | 1. 在内部使用模型生成素材并将素材对外使用，需要将素材标识为AI生成；,<br>2. 基于该模型对外提供服务的，需要遵循道德条款并且声明用到了该模型且通过协议要求用户遵循道德条款；具体可以参考：Bloom 许可证合规指引 ,<br>3. 内部使用作为提效工具，接口/服务本身不对外暴露，没有额外义务；但是不能用于非法、歧视等不正当目的；但是即使内部使用，也建议引入开源法务评估 |
| 7 | MOSS |[moss-moon-003-base](https://huggingface.co/fnlp/moss-moon-003-base),<br>[moss-moon-003-sft](https://huggingface.co/fnlp/moss-moon-003-sft),<br>[moss-moon-003-sft-plugin](https://huggingface.co/fnlp/moss-moon-003-sft-plugin),<br>[moss-moon-003-sft-int8](https://huggingface.co/fnlp/moss-moon-003-sft-int4/tree/mainhttps://huggingface.co/fnlp/moss-moon-003-sft-int8),<br>[moss-moon-003-sft-plugin-int4](https://huggingface.co/fnlp/moss-moon-003-sft-plugin-int4),<br>[moss-moon-003-sft-plugin-int8](https://huggingface.co/fnlp/moss-moon-003-sft-plugin-int8) | AGPL 3.0 | 允许商用，基本无限制 | 内部使用（包括提供SaaS服务）可以，但是如果fine-tune其参数且用于SaaS服务可能需要开源fine-tune过的参数，具体什么场景下需要开源fine-tune过的参数法务沟通 |
| 8 | 百川 | [Baichuan-7B](https://huggingface.co/baichuan-inc/Baichuan-7B) | baichuan-7B 模型许可协议 | 允许商用但需要登记和声明<br>如果要商用，需要填写问卷进行登记，且在对外提供服务时需要声明用到了该模型 |
| 8 | 百川 | [Baichuan-13B-Base](https://huggingface.co/baichuan-inc/Baichuan-13B-Base) | Baichuan-13B 模型社区许可协议 | 允许商用但需要登记和声明，此外需要配合宣传 | 如果要商用，填写问卷登记，且对外提供服务时，需要明确标识baichuan-inside，以及同意配合百川的宣传 |
| 8 | 百川 | [Baichuan2-7B-Base](https://huggingface.co/baichuan-inc/Baichuan2-7B-Base) | Baichuan2 模型社区许可协议 | | |
| 8 | 百川 | [Baichuan2-13B-Base](https://huggingface.co/baichuan-inc/Baichuan2-13B-Base) | Baichuan2 模型社区许可协议 | | |
| 9 | Falcon | [falcon-7b-instruct](https://huggingface.co/tiiuae/falcon-7b-instruct)
,<br>[falcon-40b-instruct](https://huggingface.co/tiiuae/falcon-40b-instruct) | Apache 2.0 | 较为宽松，允许各种形式商用 | 如果涉及到部署到公司之外，法务联系 |
| 9 | Falcon | [falcon-180B-chat](https://huggingface.co/tiiuae/falcon-180B-chat) | falcon-180b-license | 不能对外提供SaaS推理和fine-tune服务，可部署在内部支持公司的App | 
| 10 | 通义千问 | <br>[Qwen](https://github.com/QwenLM/Qwen), <br>[Qwen-VL](https://github.com/QwenLM/Qwen-VL) <br>注意：不包括QW1.5下的各个模型 | [AGREEMENT](https://github.com/QwenLM/Qwen/blob/main/Tongyi%20Qianwen%20LICENSE%20AGREEMENT) | 目前已经获得了针对QW-7B版本、14B版本以及72B的模型许可证，可以商用 | 不能用模型的输出训练其他模型（Qwen模型除外）；|
| 11 | 书生 | [InternLM](https://github.com/InternLM/InternLM) (7B基座模型和chat模型，20B基座模型和chat模型) | | 允许部分团队商用,下载、精调和部署该模型，也可以对其他业务提供API；| 其他主体的团队使用该模型需要另行评估；|
| 11 | 书生 | 部分xposer系列模型,<br>[internlm-xcomposer-7b](https://huggingface.co/internlm/internlm-xcomposer-7b),<br>[internlm-xcomposer-vl-7b](https://huggingface.co/internlm/internlm-xcomposer-vl-7b) | Apache 2.0 | 较为宽松，允许各种形式商用,如果涉及部署公司外，法务联系 |
| 11 | 书生 | [internlm-xcomposer2-vl-7b](https://huggingface.co/internlm/internlm-xcomposer2-vl-7b) | 需要填表申请 | 申请中，尚没有得到回复，暂时不要使用 |
| 12 | Yi | [Yi-6B](https://huggingface.co/01-ai/Yi-6B),<br>[Yi-34B](https://huggingface.co/01-ai/Yi-34B) | Yi Series Models License Agreement | 可商用，有声明义务 | 对外提供服务供第三方使用的，需要进行声明，具体落地方式请与开源法务进一步沟通；<br>涉及到私有化部署的，也需要进一步沟通 |
| 12 | Yi | Yi-VL系列：[Yi-VL-6B](https://huggingface.co/01-ai/Yi-VL-6B), <br>[Yi-VL-34B](https://huggingface.co/01-ai/Yi-VL-34B) | [LICENSE](https://huggingface.co/01-ai/Yi-VL-34B/blob/main/LICENSE) | 需要发邮件申请 |
| 13 | mistral | [announcing-mistral-7b](https://mistral.ai/news/announcing-mistral-7b/),<br>[mixtral-of-experts](https://mistral.ai/news/mixtral-of-experts/) | Apache 2.0 | 7B和mixtral-of-experts的许可证均较为宽松，允许各种形式商用 | 如果涉及到部署到公司之外，法务联系 |
| 14 | llava | [MODEL_ZOO](https://github.com/haotian-liu/LLaVA/blob/main/docs/MODEL_ZOO.md)| 适用llama 2许可证 | 禁止商用，学术使用需要单独评估 | Llava 有多个版本，主要版本有非商用限制，如果发现某个版本的许可证为宽松许可证，且确实有适用的需求，与开源法务沟通| 
| 15 | Deepseek | [deepseek-ai](https://huggingface.co/deepseek-ai)；[DeepSeek-Coder](https://github.com/deepseek-ai/DeepSeek-Coder/tree/main) | Deepseek model license | 允许商用；但对外服务需要声明<br>1.截至到24年1月10日，huggingface上deepseek主页的模型许可证均为deep seek model license，针对该许可证适用该指引；代码的许可证（MIT）、以及后续如果是该主页下的采用其他模型的许可证不适用该指引；<br>2.义务和限制：不能滥用（用于违法目的），且对外提供服务时，需要通过声明（或者协议）限制用户滥用，具体落地方式可以联系开源法务进一步沟通；纯内部部署并且服务不会对外的情形不需要做此类的限制；|
| 16 | phi-2 | [phi-2](https://huggingface.co/microsoft/phi-2) | MIT | 较为宽松，允许各种形式商用 | 如果涉及到部署到公司之外（比如部署在客户端或者涉及私有化部署），与开源法务联系 |
| 17 | Gemma | [gemma-2b](https://huggingface.co/google/gemma-2b),<br>[gemma-2b-it](https://huggingface.co/google/gemma-2b-it),<br>[gemma-7b](https://huggingface.co/google/gemma-7b),<br>[gemma-7b-it](https://huggingface.co/google/gemma-7b-it) |  [license](https://www.kaggle.com/models/google/gemma/license/consent) | 较为宽松，允许各种形式商用，但基于模型对外提供服务时，有比较多的声明义务 | 在基于Gemma以及其精调后模型对外提供服务时，声明义务包括：<br>1.通过协议条款限制用户对于服务的使用（避免用户滥用）；<br>2.如果有修改，需要说明对模型进行了修改；<br>3.需要向用户提供模型的信息和许可证。|


#### MoE

[MoE: 稀疏门控制的专家混合层](https://zhuanlan.zhihu.com/p/335024684)
- Mixture-Of-Experts 混合专家的缩写，可在保证运算速度情况下，将模型的容量提升 >1000倍。
- 将大模型拆分成多个小模型，一个样本无需经过所有小模型，而只是激活一部分小模型进行计算，这样就节省了计算资源。

如何决定样本经过哪些小模型呢？
- 引入了**稀疏门机制**，即样本输入给这个门，得到要激活的小模型索引，这个门需要确保稀疏性，从而保证计算能力的优化。

为什么迟迟没人做？
- 现在的设备不擅长做**分支**。GPU比较擅长做运算
- 大批量是训练模型的必须，但是这种方式下会导致每个小模型的样本数较少，无法训练得到好的模型
- **网络通信**是瓶颈。
- 为了控制稀疏性，可能需要在loss上去做些改进，确保模型质量和小模型上的负载均衡
- 模型容量对大数据集比较重要，现有的工作都是在类似cifar10之类的数据上做的，很难有好效果。

混合专家系统（MoE）是一种神经网络，也属于一种combine的模型。适用于数据集中的数据产生方式不同。不同于一般的神经网络的是它根据数据进行分离训练多个模型，各个模型被称为专家，而门控模块用于选择使用哪个专家，模型的实际输出为各个模型的输出与门控模型的权重组合。各个专家模型可采用不同的函数（各种线性或非线性函数）。混合专家系统就是将多个模型整合到一个单独的任务中。

混合专家系统有两种架构：competitive MoE 和cooperative MoE。
- competitive MoE中数据的局部区域被强制集中在数据的各离散空间，而cooperative MoE没有进行强制限制。

模型结构
- 首先, MoE是一个层，而不是整个模型。
- 其次，这个模型结构包含一个门网络, 决定激活哪个expert，同时包含n个expert网络，这n个expert网络一般是同结构的。
  - $y=\sum_{i=1}^{n} g(x)_{i} f_{i}(x)$
  - $\sum_{i=1}^{n} g(x)_{i}=1$ gi表示专家fi权重, g代表一个汇总所有专家结果的门控网络。
- 当 G(x)i=0 的时候，对应的expert就不会激活; 
- 门网络实现：dense layer + softmax
- 为了保证稀疏性和均衡性，softmax做了处理
- ![](https://pic1.zhimg.com/70/v2-7228430e9a6f276967abb97b6e0db9a2_1440w.avis?source=172ae18b&biz_tag=Post)

[Google多任务学习模型MMoE ](https://imzhanghao.com/2020/11/11/google-mtl-mmoe/)
- Multi-gate Mixture-of-Experts (MMoE)通过在多任务学习中引入Mixture-of-Experts（MoE）层，显式的学习了各个子任务之间关系，同时利用门限网络以优化每个任务。
- MMoE 核心思想是**集成学习**，整个思想范畴在随机森林里面，不过表达方式用了深层Net，这样每个专家可以专注一个方向去学习表达力，门控网络来计算每个专家网络跟目标匹配的权重。

实验表明，当任务相关性较低时，MMoE比基线方法具有更好的效果，并且会带来额外的可训练性好处，具体取决于训练数据和模型初始化中不同程度的随机性。



### 多模态LLM

多模态大模型：
- MiniGPT-4：沙特阿拉伯阿卜杜拉国王科技大学的研究团队开源。
- LLaVA：由威斯康星大学麦迪逊分校，微软研究院和哥伦比亚大学共同出品。
- VisualGLM-6B：开源的，支持图像、中文和英文的多模态对话语言模型，语言模型基于 ChatGLM-6B，具有 62 亿参数；图像部分通过训练 BLIP2-Qformer 构建起视觉模型与语言模型的桥梁，整体模型共78亿参数。

详见站内：[多模态专题](modal#新模型)


### 开源复现框架

#### 开源框架汇总

【2023-3-23】[GPT-3 + RL 全流程训练开源整理](https://zhuanlan.zhihu.com/p/608705255)

按 star 数量进行排序的 ChatGPT 开源项目汇总

| Github库名	| Star数	| Fork数 |	Issue总数 | 最近更新时间（天）| 备注 |
| ---	| ---	| --- |	---- | ----| ------------ |
| [CarperAl/trlx](https://github.com/CarperAI/trlx)	| 2000	| 183	| 154	| 0.3 | EleutherAI研究小组的一个新实验室CarperAI,用 RLHF 微调 HuggingFace 语言模型的框架<br>强化学习算法包括`PPO`和`ILQL`，而且支持更多的预训练模型，如gpt2,gpt-j,gpt-neoandgpt-neox等，也支持模型并行和分布式训练 |
| [LAION-AI/Open-Assistant](https://github.com/LAION-AI/Open-Assistant) |	16800 |	1300	| 843 |	3 | 非盈利机构LAION开源，[文档](https://projects.laion.ai/Open-Assistant/docs/intro), [huggingface](https://huggingface.co/OpenAssistant),[数据格式](https://github.com/LAION-AI/Open-Assistant/blob/363a3a124471217e723d57b084122ae1ca41ab2a/notebooks/data-augmentation/stackexchange-builder/README.md)<br>RL训练部分用 trlX 库, [全流程指南](https://zhuanlan.zhihu.com/p/609003237) |
| [hpcaitech/ColossalAI](https://github.com/hpcaitech/ColossalAI/tree/main/applications/ChatGPT) | 15500	| 1600	| 549	| 1 | chatgpt训练步骤的对应关系如下：(不含SFT)<br>train with dummy prompt data: 用随机生成的数据训练的第三步骤（RL来fintune sft）<br>train with real prompt data: 用真实数据训练的第三步骤（RL来fintune sft）<br>train with reward model：训练第二步的 reward 模型<br>数据<br>Reward 模型的 [rm-static 数据](https://huggingface.co/datasets/Dahoas/rm-static/tree/main)<br>训练 Prompt 模型的 [awesome-chatgpt-prompts 数据](https://huggingface.co/datasets/fka/awesome-chatgpt-prompts/tree/main) |
| [nebuly-ai/nebullvm](https://github.com/nebuly-ai/nebullvm)	| 5700	| 388 |	100 |	1 | ChatLLaMA：<br>①一个完整的开源实现，使您能够基于预训练的 LLaMA 模型构建 ChatGPT 样式的服务。<br>②与原始的 ChatGPT 相比，利用 LLaMA 架构的较小尺寸，训练过程和单 GPU 推理更快、成本更低。<br>③ChatLLaMA 内置了对 DeepSpeed ZERO 的支持，以加速微调过程。<br>④该库还支持所有 LLaMA 模型架构（7B、13B、33B、65B），因此您可以根据自己对训练时间和推理性能的偏好对模型进行微调。|
| [lucidrains/PaLM-rlhf-pytorch](https://github.com/lucidrains/PaLM-rlhf-pytorch) |	5400	| 412	| 24	| 0.2 | PaLM语言模型（称为 PaLM + RLHF）实施 RLHF, 只有PaLM架构和代码，没有预先训练好的权重<br>PaLM（Pathways Language Model）是谷歌2022年4月发布的5400亿参数全能大模型，基于Pathways系统训练，BERT之父Jacob Devlin为主要贡献者之一 |
| [BlinkDL/RWKV-LM](https://github.com/BlinkDL/RWKV-LM)	| 1800	| 182	| 24	| 0.4 | 用 RWKV 架构（不是transformer结构）训练的chatgpt, 支持分布式训练. 开源了 14B 的模型，可以在 huggingface上面[试用](https://huggingface.co/spaces/yahma/rwkv-14b) |
| [Ivwerra/trl](https://github.com/lvwerra/trl)	| 1700 |	180 |	73	| 1 | [文档](https://huggingface.co/docs/trl/index) PPO精调LLM的三个步骤: <br>流程<BR>1. 用 codeparrot 数据训练 GPT-2 124.2M 模型<br>不同于chatgpt微调已训练好的模型，trl是从头开始训练<BR>2. 用sentiment训练奖励模型（distilbert）<br>3. RL训练，参考[过程](https://mp.weixin.qq.com/s/8IFcQDhsLIWJIx8siF-wdQ) |
| [HarderThenHarder/transformers_tasks](https://github.com/HarderThenHarder/transformers_tasks/tree/main/RLHF)	| 274	| 51	| 17	| 5 | 基于TRL, 增加了基于人工打分的Reward模型训练，还提供了Reward数据的标注平台<br>RM 模型训练: 基于 ernie-3.0-base-zh 继续训练的<br>RL 训练：① RM用的一个现成的情感分类模型，roberta-base-fintuned-jd-binary-chinese ②生成模型：用的gpt2-chinese-cluecorpussmall |
| [allenai/RL4LMs](https://github.com/allenai/RL4LMs) |	971	| 87	| 27	| 30 | 包括较多 RL 算法（PPO，NLPO，A2C和TRPO），在 2000 个实验里做了 RL 在 LLM 上面的训练。RL4LMs当前的计划包括分布式训练更大的模型和新的RL算法。[paper](https://arxiv.org/abs/2210.01241) |

使用工具: [ExtractTable](https://extracttable.com/): Extract tabular data from images, 从图片中抽取表格数据

#### 框架实测

【2023-7-3】 开源框架实测
- `Alpa`: 大规模神经网络的训练、部署框架，几行代码自动分布式训练、部署。
  - [Serving OPT-175B, BLOOM-176B and CodeGen-16B using Alpa](https://alpa.ai/tutorials/opt_serving.html)
- Megatron-`DeepSpeed`: 微软结合NVIDIA的transformer高效库+DeepSpeed
  - DeepSpeed: 微软 [deepspeed.ai](https://www.deepspeed.ai/)推出的深度学习训练推理框架, [github](https://github.com/microsoft/DeepSpeed), BLOOM 1-3B SFT
  - [Megatron-LM](https://github.com/NVIDIA/Megatron-LM): NVIDIA 应用深度学习研究院推出的高效transformer库
  - [DeepSpeed Chat](https://github.com/microsoft/DeepSpeed/tree/master/blogs/deepspeed-chat)
  - 
  - [Megatron-LM GPT2 tutorial](https://www.deepspeed.ai/tutorials/megatron/)
  - 优点: 单机多卡可行(1-3B), 7-10B 内存超限
  - 缺点: 
    - 无法设置 epoch 字段，训练不方便
    - 流程复杂, 代码复杂, 改动不方便
- `Colossal AI`： 覆盖三步流程
  - 优点：完整的三步流程，支持并行训练
  - 缺点：
    - SFT 训练bloom流程不完善, 如 forward函数没写
    - 训练 RM 模型时，基于bloom的pad方式不对（应该从左到右），计算损失函数时把pad算进来
    - ppo：存在ab问题，舍弃，未验证ppo有效性
- `Open Assistant`：改动/优化源码支持bloom训练
  - 优点：三步流程完整，支持并行训练
  - 缺点：不支持bloom的RLHF，改动需要懂分布式计算流程，成本大
- `TRLX`：改动后支持
  - 优点：三步流程、并行
  - 缺点：需要改动源码
- `BMTtrain`: [BMTrain](https://github.com/OpenBMB/BMTrain) 100b级别大模型训练工具包


trlx上完成三步流程训练，抽样效果 +5-10%

### OPT

2022年5月，Meta AI 开源了 Open Pretrained Transformer (`OPT`-175B)，一个拥有 1750 亿个参数的语言模型，使用了 5 个公开数据集的 **800GB** 数据进行训练；旨在刺激大型语言模型 (LLM) 的使用。
- Meta AI 仅使用 16 个 NVIDIA V100 GPU 来训练和部署模型的代码库，以提高这些模型专门用于研究目的的可访问性，并为在一个共同的共享模型上分析植根于可量化指标的潜在危害提供基础。
- 训练代价：OPT-175B 的开销仍然太过高昂：一次训练就将需要在约 1000 个 80G A100 GPU 上花费至少 2个月时间（数据来自于 OPT 的原始文献）
- 还发布了一套较小规模的基线模型，使用与 OPT-175B 相同的数据集，设置也和 OPT-175B 类似，以使得研究人员能够单独研究模型规模的影响。这些小规模模型的参数包括 1.25 亿、3.5 亿、13 亿、27 亿、67 亿、130 亿和 300 亿（660 亿即将发布）。

OPT-175B 是 Meta 开源的大语言模型，拥有超过 1750 亿个参数 —— 和 GPT-3 相当。相比 GPT-3，OPT-175B 的优势在于它**完全免费**。

Meta 还公布了代码库、开发过程日志、数据、研究论文和其他与 OPT-175B 相关的信息。尽管 OPT-175B 是免费的，但 Meta 也给出了一些限制。为了防止误用和 “保持完整性”，OPT-175B 只允许在**非商业**用途下使用。
- OPT-175B 的多数应用场景还是在科研上。

OPT
- The OPT model was proposed in Open Pre-trained Transformer Language Models by Meta AI. 
- The model was pretrained using a **causal language modeling** (CLM) objective. OPT belongs to the same family of decoder-only models like `GPT-3`. As such, it was pretrained using the self-supervised causal language modedling objective.
  - `CLM` 因果语言模型：即传统的自回归语言模型，Causal language modeling predicts the next token in a sequence of tokens, and the model can only attend to tokens on the left. This means <span style='color:red'>the model cannot see future tokens</span>. `GPT-2` is an example of a causal language model.
  - `MLM` 掩码语言模型：Masked language modeling predicts a masked token in a sequence, and the model can attend to tokens **bidirectionally**. This means the model has full access to the tokens on the left and right. `BERT` is an example of a masked language model. 参考：[huggingface](https://huggingface.co/docs/transformers/tasks/language_modeling)
- 论文地址：[OPT: Open Pre-trained Transformer Language Models](https://arxiv.org/pdf/2205.01068.pdf)
- [请求访问权限地址](https://forms.gle/dag8g7nKiR4o4VZq5)
- [OPT源码](https://github.com/facebookresearch/metaseq), [huggingface](https://huggingface.co/docs/transformers/model_doc/opt)
- `语料`（corpus）：预训练语料以英文为主，少量非英文（commoncrawl），The pre-training corpus contains a concatenation of datasets used in RoBERTa (Liu et al., 2019b), the Pile (Gao et al., 2021a), and PushShift.io Reddit (Baumgartner et al., 2020; Roller et al., 2021). All corpora were previously collected or filtered to contain predominantly English text, but a small amount of non-English data is still present within the corpus via [CommonCrawl](https://commoncrawl.org/the-data/get-started/)
  - Common Crawl包含了超过7年的网络爬虫数据集，包含原始网页数据、元数据提取和文本提取。常见的爬行数据存储在Amazon Web服务的公共数据集和遍布全球的多个学术云平台上,拥有PB级规模，常用于学习词嵌入。

Tips:
- `OPT` has the same architecture as `BartDecoder`.
- Contrary to `GPT2`, `OPT` adds the EOS token \</s\> to the beginning of every prompt. Note: Make sure to pass `use_fast=False` when loading OPT’s tokenizer with AutoTokenizer to get the correct tokenizer.

【2023-02-20】[别等ChatGPT开源了](https://mp.weixin.qq.com/s/_itE0iUCS7lfrMb4Pzx-ig), Meta「对2000个语言任务进行了微调，包含1750 亿个参数」，还将为非商业研究用途免费开放。`OPT-IML`（Open Pre-trained Transformer）
- paper: [OPT-IML](https://github.com/facebookresearch/metaseq/blob/main/projects/OPT-IML/optimal_paper_v1.pdf)
- [Github链接](https://github.com/facebookresearch/metaseq/tree/main/projects/OPT-IML)

`OPT-IML`创建了两种模型尺寸，分别是30B和175B。
- 与旧版OPT模型相比，`OPT-IML`在14个标准NLP评估任务中的平均表现均优于OPT。
- 在零次学习任务上两种模型大小分别好 7%~ 和 32-shot 任务分别好 4%~ 和 0.4%~。

在这项研究中，研究人员描述了增加模型和基准大小如何影响指令调整决策对下游任务性能的影响。

### BLOOM

2022年7月，BigScience 研究人员发布了一个名为 Bloom 的自然语言处理模型，该模型具有 1760 亿个参数，一举超越市面上的**所有**竞争对手，成为目前规模最大的语言模型。
- BLOOM 有1760亿个参数，能够以**46种**自然语言和**13种**编程语言生成文本。
- 对于几乎所有的语言，比如西班牙语、法语和阿拉伯语，`BLOOM` 是有史以来创建的第一个超过100B参数的语言模型。这是来自70多个国家和250多个机构的1000多名研究人员一年工作的成果，最终在法国巴黎南部的Jean Zay超级计算机上训练了**117天**(3月11日至7月6日)的BLOOM模型. 归功于法国国家科学研究中心(CNRS)和法国科学研究中心(CNRS)估计价值300万欧元的计算拨款。

- 论文：[BLOOM: A 176B-Parameter Open-Access Multilingual Language Model](https://arxiv.org/pdf/2211.05100.pdf)
- 摘要：Large language models (LLMs) have been shown to be able to perform new tasks based on a few demonstrations or natural language instructions. While these capabilities have led to widespread adoption, most LLMs are developed by resource-rich organizations and are frequently kept from the public. As a step towards democratizing this powerful technology, we present BLOOM, a 176B-parameter open-access language model designed and built thanks to a collaboration of hundreds of researchers. BLOOM is a **decoder-only Transformer** language model that was trained on the ROOTS corpus, a dataset comprising hundreds of sources in **46 natural** and **13 programming languages** (59 in total). We find that BLOOM achieves competitive performance on a wide variety of benchmarks, with stronger results after undergoing multitask prompted finetuning. To facilitate future research and applications using LLMs, we publicly release our models and code under the Responsible AI License
- [BLOOM is a real open-source alternative to GPT-3](https://the-decoder.com/bloom-is-a-real-open-source-alternative-to-gpt-3/)
- huggingface上的[model地址](https://huggingface.co/bigscience/bloom)
- code: [Megatron-DeepSpeed](https://github.com/bigscience-workshop/Megatron-DeepSpeed)，采用别人的GPT模型文件
- 【2023-2-22】`bloom` 基于 `GPT-2`, 加大层数，使用法国财政资金，通过大规模数据（46种语言+13种编程语言）训练117天而来，得到gpt-3同等规模（176b>175b），这个代码是NVIDIA+微软分布式训练框架的训练代码。
- bloom 训练代码 [Megatron-DeepSpeed](https://github.com/bigscience-workshop/Megatron-DeepSpeed/blob/main/LICENSE) 是 Apache License 开源协议

BLOOM数据集: <span style='color:blue'> 英文 30% ＞ 中文 16% ＞ 法文 12% ＞ 西班牙 11% ＞ 代码 11% ＞ 葡萄牙 5% ＞ 阿拉伯 4.6% ＞ 印地语 4.4% </span>
- ![](https://pic2.zhimg.com/80/v2-cf94d00d3e954efd11edeb880e85dac5_1440w.webp)
- [refer](https://zhuanlan.zhihu.com/p/618926239)

#### BLOOM 模型结构

BLOOM 模型结构与GPT相同，采用了causal decoder-only的transformer模型结构。在模型细节上，做了以下几点改动：
- embedding layer norm：在embedding层后添加了一个 layer normalization，来使训练更加稳定。
  - 启发来自于bitstandbytes的StableEmbedding做法
- layer normalization：为了提升训练的稳定性，没有使用传统的 post layer norm，而是使用了 pre layer Norm。
- 激活函数：采用了GeLU激活函数。
- 位置编码：去除了绝对位置编码，采用了相对位置编码`ALiBi`。
  - 相比于绝对位置编码，ALiBi的外推性更好，即虽然训练阶段的最大序列长度为2048，模型在推理过程中可以处理更长的序列。
- ![](https://pic4.zhimg.com/80/v2-c918328f95f9bc2307ebcd8b5df1c7ef_1440w.webp)



BLOOM 训练目标是语言模型，即根据已有的上文去预测下一个词。

关于tokenizer，BLOOM在多语种语料上使用Byte Pair Encoding(BPE)算法进行训练得到tokenizer，词表大小为250880。

BLOOM衍生出来的大模型应用：
- 轩辕: 金融领域大模型，度小满在BLOOM-176B的基础上针对中文通用领域和金融领域进行了针对性的预训练与微调。
- BELLE: 链家仅使用由ChatGPT生产的数据，对BLOOMZ-7B1-mt进行了指令微调。

#### BLOOM 训练资源

BLOOM: training that lead around the world
- The training started on March 11, 2022. But in fact, the preparations of the corpus and the datasets started much earlier. A model with these characteristics is not achieved overnight. 4 months later, here we have it. And it hasn’t been easy:
- 384 graphic cards of 80 gigabytes each on the Jean Zay supercomputer in France.
- BLOOM has 176 billion parameters, one billion more than GPT-3.
- 70 layers – 112 attention heads per layers – hidden dimensionality of 14336 – 2048 tokens sequence length.
- ALiBi positional embeddings – GeLU activation function.

BLOOM 训练使用的硬件设施
- GPUs: **384 张** NVIDIA `A100` **80GB** GPUs (48 个节点，单个节点 8 张卡) + 32 张备用 GPU
每个节点 8 个 GPU 使用 NVLink 4 inter-gpu connects，4 OmniPath links
- CPU: AMD EPYC 7543 32-Core Processor
- CPU memory: 每个节点 512GB
- GPU memory: 每个节点 640GB
- 节点间连接: Omni-Path Architecture (OPA) w/ non-blocking fat tree
- NCCL-communications network: a fully dedicated subnet
- 硬盘 IO 网络: IBM 通用并行文件系统-GPFS shared with other nodes and users

训练资源
- 176B BLOOM 模型使用 `Megatron-DeepSpeed` 进行训练

BigScience 的 Megatron-DeepSpeed 是基于原始 Megatron-DeepSpeed 代码库，还添加了不少代码。
- BigScience 的 [Megatron-DeepSpeed](https://github.com/bigscience-workshop/Megatron-DeepSpeed):
- 原版的 [Megatron-DeepSpeed](https://github.com/microsoft/Megatron-DeepSpeed)

BLOOM 训练时采用的组件: [BLOOM 训练背后的技术](https://mp.weixin.qq.com/s/-q9opkoAomd9LZL9phm8bA)

| 组件	| DeepSpeed	| Megatron-LM |
| ZeRO 数据并行 |	是 |	|
| 张量并行	| |是 |
| 流水线并行 | 是 | |	
| BF16 优化器 |	是 | |	
| CUDA 融合核函数 |	 | 是 |
| 数据加载器 | | 是 |

Megatron-LM 和 DeepSpeed 都有**流水线并行**和 BF16 优化器实现，但使用 DeepSpeed 的实现，因为集成进了 ZeRO。

Megatron-DeepSpeed 实现了 3D 并行以允许大模型以非常有效的方式进行训练。有哪些 3D 组件。
- `数据并行` (Data Parallelism，DP) - 相同的设置和模型被复制多份，每份每次都被馈送不同的一份数据。处理是并行完成的，所有份在每个训练步结束时同步。
- `张量并行` (Tensor Parallelism，TP) - 每个张量都被分成多个块，因此张量的每个分片都位于其指定的 GPU 上，而不是让整个张量驻留在单个 GPU 上。在处理过程中，每个分片在不同的 GPU 上分别并行处理，结果在步骤结束时同步。这就是所谓的水平并行，因为是做的水平拆分。
- `流水线并行` (Pipeline Parallelism，PP) - 模型在多个 GPU 上垂直 (即按层) 拆分，因此只有一个或多个模型层放置在单个 GPU 上。每个 GPU 并行处理流水线的不同阶段，并处理 batch 的一部分数据。
- `零冗余优化器` (Zero Redundancy Optimizer，ZeRO) - 也执行与 TP 相类似的张量分片，但整个张量会及时重建以进行前向或反向计算，因此不需要修改模型。它还支持各种卸载技术以补偿有限的 GPU 内存。


#### bloomz 多任务指令微调

HuggingFace 上的[bloomz模型](https://huggingface.co/bigscience/bloomz)
- 论文：[Crosslingual Generalization through Multitask Finetuning](https://arxiv.org/abs/2211.01786)
- bloomz 在 bloom基础上用**多任务提示微调**（`MTF`）实现了**跨语言泛化**，通过英语语料泛化到非英语场景，在机器翻译上证明效果更好
  - [xP3](https://huggingface.co/datasets/bigscience/xP3)数据集包含46种语言，包含prompt提示后，是 [xP3mt](https://huggingface.co/datasets/bigscience/xP3mt)
- Multitask prompted finetuning (`MTF`) has been shown to help large language models generalize to new tasks in a zero-shot setting, but so far explorations of MTF have focused on English data and models. We apply `MTF` to the pretrained multilingual BLOOM and mT5 model families to produce finetuned variants called BLOOMZ and mT0. We find finetuning large multilingual language models on English tasks with English prompts allows for task generalization to non-English languages that appear only in the pretraining corpus. Finetuning on **multilingual tasks** with English prompts further improves performance on English and non-English tasks leading to various state-of-the-art zero-shot results. We also investigate finetuning on multilingual tasks with prompts that have been machine-translated from English to match the language of each dataset. We find training on these machine-translated prompts leads to better performance on human-written prompts in the respective languages. Surprisingly, we find models are capable of zero-shot generalization to tasks in languages they have never intentionally seen. We conjecture that the models are learning higher-level capabilities that are both task- and language-agnostic. In addition, we introduce `xP3`, a composite of supervised datasets in 46 languages with English and machine-translated prompts.
- 数据和代码：[github](https://github.com/bigscience-workshop/xmtf)

【2023-2-22】bloomz为什么效果不如bloom？[Worse performance in Text Generation on Chinese corpus](https://huggingface.co/bigscience/bloomz/discussions/35#63f5cecb9cbd6730302359de)
- 猜测是提示微调任务的目标是实现跨语言翻译，46个语种将bloom模型引导到翻译领域了，中文表示能力被稀释。建议，临时放弃bloomz，在bloom基础上微调

```py
# pip install -q transformers # cpu
# pip install -q transformers accelerate # gpu
# pip install -q transformers accelerate bitsandbytes # gpu 8 bit
from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "bigscience/bloomz"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# model = AutoModelForCausalLM.from_pretrained(checkpoint) # cpu
model = AutoModelForCausalLM.from_pretrained(checkpoint, torch_dtype="auto", device_map="auto") # gpu
# model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto", load_in_8bit=True) # gpu 8 bit
# inputs = tokenizer.encode("Translate to English: Je t’aime.", return_tensors="pt") # cpu
inputs = tokenizer.encode("Translate to English: Je t’aime.", return_tensors="pt").to("cuda") # gpu
outputs = model.generate(inputs)
print(tokenizer.decode(outputs[0]))
```

#### Fine-tune

Here is the code to fine-tune the Bloom model, [petals](https://github.com/bigscience-workshop/petals)

```py
from petals import DistributedBloomForCausalLM

model = DistributedBloomForCausalLM.from_pretrained("bigscience/bloom-petals", tuning_mode="ptune", pre_seq_len=16)
# Embeddings & prompts are on your device, BLOOM blocks are distributed across the Internet

inputs = tokenizer("A cat sat", return_tensors="pt")["input_ids"]
outputs = model.generate(inputs, max_new_tokens=5)
print(tokenizer.decode(outputs[0]))  # A cat sat on a mat...

# Fine-tuning (updates only prompts or adapters hosted locally)
optimizer = torch.optim.AdamW(model.parameters())
for input_ids, labels in data_loader:
    outputs = model.forward(input_ids)
    loss = cross_entropy(outputs.logits, labels)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

### SparseGPT

`模型压缩`（model compression）是当前使用较多的一种降低大模型计算成本的方法
- 但迄今为止，几乎所有现有的 GPT 压缩方法都专注于`量化`（quantization），即降低单个权重的数值表示的精度。
- 另一种模型压缩方法是`剪枝`（pruning），即删除网络元素，包括从单个权重（非结构化剪枝）到更高粒度的组件如权重矩阵的整行/列（结构化剪枝）。

第二种方法这在视觉和较小规模语言模型中很有效，但会导致**精度损失**，从而需要对模型进行大量再训练来恢复精度，所以遇到 GPT 这样大规模的模型时，成本就又变得过于昂贵了。虽然也有一些单次剪枝方法，无需重新训练即可压缩模型，但它们计算量太大，难以应用于具有数十亿参数的模型。

2023年1月，奥地利科学技术研究所 (`ISTA`) 的两名研究人员 Elias Frantar 和 Dan Alistarh 合作了一项研究，首次针对 100 至 1000 亿参数的模型规模，提出了精确的单次剪枝方法 SparseGPT。 [paper](https://arxiv.org/pdf/2301.00774.pdf)

SparseGPT 可以将 GPT 系列模型单次剪枝到 50% 稀疏性，而无需任何重新训练。
- 目前最大的公开可用的 GPT-175B 模型，只需要使用单个 GPU 在几个小时内就能实现这种剪枝。

而且，SparseGPT 还很准确，能将精度损失降到最小。
- 比如在目前最大的开源模型 OPT‑175B 和 BLOOM‑176B 上执行SparseGPT 时，可以达到 60% 的稀疏度，同时将精度损失降到最小。


### GPT-X系列

GPT-J 是一个基于 GPT-3，由 60 亿个参数组成的自然语言处理 AI 模型。

2021年6月发布`GPT-J`，作为开源模型，两者均由 `EleutherAI` 发布
- GPT-Neo有3个版本: 1.25亿个参数，13亿个参数（相当于GPT-3 Babbage），和 2.7亿个参数。
- GPT-J有60亿个参数，这使得它成为目前最先进的开源自然语言处理 模型。这直接等同于GPT-3 Curie。

#### EleutherAI

2020 年微软与 OpenAI 在 GPT-3 源代码独家访问权上达成协议以来，OpenAI 就不再向社会大众开放 GPT-3 的模型代码（尽管 GPT-1 和 GPT-2 仍是开源项目）。

出于对科技巨头霸权的「反叛」，一个由各路研究人员、工程师与开发人员志愿组成的**计算机科学家协会**成立，立志要打破微软与 OpenAI 对大规模 NLP 模型的垄断，且取得了不错的成果。

这个协会，就是：EleutherAI。以古罗马自由女神 Eleutheria 的名字命名，透露出对巨头的不屑与反抗。

EleutherAI 成立始于 2020 年 7 月，主要发起人是一群号称自学成才的黑客，主要领导人包括 Connor Leahy、Leo Gao 和 Sid Black，基于 Discord 成立了 EleutherAI，希望建立一个能够与 GPT-3 相媲美的机器学习模型。

`EleutherAI`: 一个由致力于开源人工智能的研究人员组成的集体 研究人员致力于开放人工智能的源代码).

EleutherAI 研究团队[成长迅速](https://posts.careerengine.us/p/623b012b4f37b3440f998614?from=latestPostSidePanel)
- 2021年3月，开源了基于 GPT-3 的、包含 60 亿参数的 NLP 模型 `GPT-Neo`
- 2021年6月，又发布类 GPT 的 27 亿参数模型 `GPT-J`。
- 2023年2月9日，又与 CoreWeave 合作发布了 GPT-Neo 的升级版——`GPT-NeoX-20B`，官方[代码地址](https://mystic.the-eye.eu/public/AI/models/GPT-NeoX-20B/)现可从 The Eye on the Eye 公开下载. `GPT-NeoX-20B` 是一个包含 200 亿参数、预训练、通用、自回归大规模语言模型

EleutherAI 完全公开发布 Pile 数据集, 一个 825 GB 的英文文本语料库，用于训练大规模语言模型。

该模型在一个 800GB 的开源文本数据集上进行训练，并且能够与类似规模的 GPT-3 模型相媲美。 该模型通过利用 Google Cloud 的 v3-256 TPU 以及 EleutherAI 的 The Pile 数据集进行训练，历时大约五周时间。
- GPT-J 在标准 NLP 基准工作负载上实现了与 OpenAI 报告的 67 亿参数版本的 GPT-3 类似的准确性。模型代码、预训练的权重文件、Colab 文档和一个演示网页都包含在 EleutherAI 的开源项目中。

#### GPT-Neo

2021年3月发布`GPT-Neo`
- GPT-Neo有3个版本: 1.25亿个参数，13亿个参数（相当于GPT-3 Babbage），和 2.7亿个参数。

#### GPT-J

GPT-J 是一个基于 GPT-3，由 60 亿个参数组成的自然语言处理 AI 模型。

2021年6月发布`GPT-J`
- GPT-J有60亿个参数，这使得它成为目前最先进的开源自然语言处理 模型。这直接等同于GPT-3 Curie。

#### GPT-NeoX-20B

2023年2月9日，EleutherAI又与 CoreWeave 合作发布了 `GPT-Neo` 升级版——`GPT-NeoX-20B`
- 官方[代码地址](https://mystic.the-eye.eu/public/AI/models/GPT-NeoX-20B/), 现可从 The Eye on the Eye 公开下载. 
- `GPT-NeoX-20B` 是一个包含 200 亿参数、预训练、通用、自回归大规模语言模型

### Pythia

Eleuther AI 和耶鲁大学等机构研究者共同撰写的 [Pythia 论文](https://arxiv.org/pdf/2304.01373.pdf)
- EleutherAI 是一个非营利性人工智能研究实验室，专注于大型模型的可解释性和对齐性.
- [Eleuther.AI](https://www.eleuther.ai/) 发布的 [Pythia](https://huggingface.co/EleutherAI/pythia-12b)

开源 Pythia 系列大模型是其他自回归解码器风格模型（即类 GPT 模型）的有趣平替。

Pythia 模型架构与 GPT-3 相似，但包含一些改进，比如 **Flash 注意力**（像 LLaMA）和**旋转位置嵌入**（像 PaLM）。
- 同时 Pythia 在 800GB 的多样化文本数据集 Pile 上接受了 300B token 的训练（其中在常规 Pile 上训练 1 个 epoch，在去重 Pile 上训练 1.5 个 epoch ）。

Pythia 论文中得到的洞见和思考：
- 重复数据上的训练（即训练 epoch>1）会不会有什么影响？结果表明，数据去重**不会**改善或损害性能；
- 训练命令会影响记忆吗？不会。如果影响的话，则可以通过训练数据的重新排序来减轻讨厌的逐字记忆问题；
- batch 大小加倍可以将训练时间减半但不损害收敛。

#### Pythia-12b 实践

EleutherAI/pythia-12b(需要24G存储)模型介绍：　
-  pythia 是 EleutherAI 为了促进LLM的研究开源的一系列LLM(70M, 160M, 410M, 1B, 1.4B, 2.8B, 6.9B, and 12B)。

数据集
- 单独起一个脚本就下载模型和数据。test.py
- 联网下载, 或手动[下载地址](https://huggingface.co/datasets/tatsu-lab/alpaca/tree/main/data)

```py
#模型下载也可网上找那种不下到默认目录的。缓存目录: ll ~/.cache/huggingface/hub/models--EleutherAI--pythia-12b/
from transformers import (
    AutoModelForCausalLM, 
)
# ======= 下载12b模型 =======
model = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-12b")
# ======= 下载数据集 =======
# download dataset. 
# 联网下载, 或手动下载地址 https://huggingface.co/datasets/tatsu-lab/alpaca/tree/main/data
# 就把24M数据下载下来， mkdir -p tatsu-lab/alpaca , 然后下载好数据丢里面就行
from datasets import load_dataset
dataset = load_dataset("tatsu-lab/alpaca")
```

运行
- `sh scripts/generate.sh`
- 显存大小：<span style='color:blue'>EleutherAI/pythia-12b 推理只需要显存12.8G</span>

单卡23G即可finetune pythia-12b
- EleutherAI/pythia-12b **推理**只需**12G**
- QLoRA finetune也只需**23G**. 详见[QLoRA的实测记录](https://zhuanlan.zhihu.com/p/632398047)

单个3090就能搞定。
- QLoRA 3090测试12B模型跑finetune
- eval阶段单卡3090会OOM.

解决
- 根据设备资源适当调整 batchsize 和 gradient_accumulation_steps 解决

### YaLM（俄罗斯 Yandex）

YaLM 100B —— 千亿参数预训练语言模型

YaLM 100B是一个类似 GPT 的神经网络，用于生成和处理文本。

该模型利用了 1000 亿个参数，在 800 个 A100 显卡和 1.7 TB 在线文本、书籍以及海量其他英文和俄文资源的集群上训练该模型花了 65 天时间。

## 复现详情


### 开源终究胜利

开源终究胜利
- [详见](https://wqw547243068.github.io/company#%E5%BC%80%E6%BA%90ai%E7%BB%88%E7%A9%B6%E8%83%9C%E5%88%A9)

【2023-5-6】[谷歌内部文件泄露：我们和OpenAI都没有护城河](https://www.huxiu.com/article/1439220.html)
- Google 内部泄露的文件在 SemiAnalysis 博客传播: **开源 AI** 会击败 Google 与 OpenAI，获得最终的胜利。
- 译文：我们没有护城河，OpenAI 也没有, [公众号](https://mp.weixin.qq.com/s/JiA-HJXeZSgHGH6zHblIVA)，[掘金](https://juejin.cn/post/7229593695653314597)
- 原文：[We Have No Moat, And Neither Does OpenAI](https://www.semianalysis.com/p/google-we-have-no-moat-and-neither)

开源AI是最后赢家，而不是OpenAI
- 从头训练大模型成本太高，难以实施：LLaMA和LoRA出现
  - 3月初，Meta 的 LLaMA 泄露，没有指令或对话调整，也没有 RLHF。
  - 不到一个月，一系列改进版出现：指令调整、量化、质量改进、人类评估、多模态和 RLHF 等等变体。每个改进版间隔才几天时间
  - 扩展问题解决后，一定程度上任何人都可以进行实验和调试。
- 长期来看，大型模型并不更具优势，只用了几天时间
- 数据质量比数据大小更重要
- 直接与开源竞争是一个失败的命题
- 个人受到许可证限制程度没有企业那么大
- 客户比大模型提供商更了解业务应用
- Meta已开始建设开源生态系统：闭源越多，开源需求越强烈，发展越快

### 汇总

| 公司 | 产品 | 日期 | 阶段 | 链接 |
| --- | --- | --- | --- | --- |
| 华为 | [盘古]() | 2021年4月 | 无 | - |
| OpenAI | [ChatGPT](https://chat.openai.com/) | 2022年11月30日 | 开放注册 | https://chat.openai.com/ |
| 腾讯 | [混元]() | 2022年12月 | 无 | 消息来源：腾讯集团高级执行副总裁汤道生 |
| 元语智能 | [ChatYuan]() | 2022年12月 | 无 | 小程序 |
| Google | [Bard](http://bard.google.com) | 2023年2月8日 | 公开测试 | http://bard.google.com/ |
| 复旦大学 | [MOSS](https://moss.fastnlp.top) | 2023年2月20日 | 公开测试(目前升级中) | https://moss.fastnlp.top/ |
| 澜舟科技 | [孟子]() | 2023年3月14日 | - | - |
| 清华大学 | [ChatGLB-6B](https://github.com/THUDM/ChatGLM-6B) | 2023年3月15日 | 已开源 | https://github.com/THUDM/ChatGLM-6B |
| 智谱AI | [ChatGLM]() | 2023年3月15日 | - | - |
| 百度 | [文心一言](https://yiyan.baidu.com) | 2023年3月16日 | 企业用户内测 | https://yiyan.baidu.com/ |
| Colossal AI | [ColossalChat](https://chat.colossalai.org/) | 2023年3月28日 | 公开 | - |
| 阿里 | [通义千问](https://tongyi.aliyun.com) | 2023年4月7日 | 企业用户内测 | https://tongyi.aliyun.com/ |
| 360 | [360智脑](http://www.360dmodel.com/) | 2023年4月10日 | 企业用户内测 | http://www.360dmodel.com/ |
| 微软 | [DeepSpeed Chat](https://github.com/microsoft/DeepSpeed)  | 2023年4月12日 | 发布，超过colossal ai |  |
| 商汤 | [商量SenseChat](https://www.sensecore.cn) | 2023年4月10日 | 即将邀请内测 | https://www.sensecore.cn/ |
| 知乎 | 知海图AI | 2023年4月13日 | 尚无内测 |  |
| 昆仑万维 | [天工3.5](https://www.sensecore.cn) | 2023年4月10日 | 内测 | http://tiangong.kunlun.com |
| 出门问问 | [序列猴子]() | 2023年4月20日 | - | - |
| 第四范式 | [式说3.0]() | 2023年4月26日 | - | - |
| 中国电信 | [星河]() | 2023年4月28日 | - | - |
| 科大讯飞 | [星火]() | 2023年5月6日 | 发布 |
| 网友有道 | 子曰 | 近期 | 即将发布 | 消息来源：网易新闻 |
| 京东 | 言犀 | 今年 | 未开放 | 消息来源：京东集团副总裁何晓冬 |

更多大模型
- [大模型图表](https://www.toutiao.com/w/1767234698845188)

#### 模型结构对比

LLaMA, ChatGLM, Baichuan 对比
- 【2023-7-20】[参考](https://zhuanlan.zhihu.com/p/644815089)

| 模型名称 | 参数 | 隐藏层维度 | 层数 | 注意力头数 | 训练数据 | 位置编码 | 激活函数 | 归一化方法 | 注意力机制 | 词表大小 | 最大长度 |
| LLaMA | 6.7B | 4096 | 32 | 32 | 1T | RoPE | SwiGLU | RMSNorm（pre-norm) <br>Attention Layer和MLP的输入上使用 | 多头注意力机制(MHA) | 32000 | 2048 |
| LLaMA | 13.0B | 5120 | 40 | 40 | 1T | RoPE | SwiGLU | RMSNorm（pre-norm)<br>Attention Layer和MLP的输入上使用 | 多头注意力机制(MHA) | 32000 | 2048 |
| LLaMA | 32.5B | 6656 | 60 | 52 | 1.4T | RoPE | SwiGLU | RMSNorm（pre-norm)<br>Attention Layer和MLP的输入上使用 | 多头注意力机制(MHA) | 32000 | 2048 |
| LLaMA | 65.2B | 8192 | 80 | 64 | 1.4T | RoPE | SwiGLU | RMSNorm（pre-norm)<br>Attention Layer和MLP的输入上使用 | 多头注意力机制(MHA) | 32000 | 2048 |
| LLaMA2 | - | - | - | - | 2.0T | RoPE | SwiGLU | RMSNorm（pre-norm)<br>Attention Layer和MLP的输入上使用 | Group Query Attention | - | 4096 |
| ChatGLM-6B | 6.2B | 4096 | 28 | 32 | 1T | RoPE 2d位置编码 | GELU | layer norm（post-norm) | 多头注意力机制(MHA) | 130528 | 2048 |
| ChatGLM2-6B | 6.2B | 4096 | 28 | 32 | 1.4T | RoPE 推理时，舍弃2d位置编码，回归decoder-only | SwiGLU | RMSNorm（post-norm) | Multi-Query Attention （MQA） | 65024 | 32768 |
| Baichuan-7b | 7B | 4096 | 32 | 32 | 1.2T | RoPE | SwiGLU | RMSNorm（pre-norm) | 多头注意力机制(MHA) | 64,000 | 4096 |
| Baichuan-13b | 13B | 5120 | 40 | 40 | 1.4T | ALiBi | silu | RMSNorm（pre-norm) | 多头注意力机制(MHA) | 64,000 | 4096 |


主流的开源大语言模型主要有三个：LLaMA、ChatGLM和BLOOM， 从训练数据、tokenizer和模型结构上对这三个大语言模型进行[比较](https://zhuanlan.zhihu.com/p/635710004)。

| 模型	| 训练数据	| 训练数据量	| 模型参数量	| 词表大小 |
| ---	| ---	| ---	| ---	| --- |
| LLaMA	| 以英语为主的拉丁语系，不包含中日韩文 |	1T/1.4T tokens |	7B、13B、33B、65B	 | 32000 |
| ChatGLM-6B	| 中英双语，中英文比例为1:1	| 1T tokens |	6B	| 130528 |
| Bloom	| 46种自然语言和13种编程语言，包含中文 |	350B tokens	| 560M、1.1B、1.7B、3B、7.1B、176B	| 250880 |


| 模型	| 模型结构	| 位置编码	| 激活函数	| layer norm |
| ---	| ---	| ---	| ---	| --- |
| LLaMA	| Casual decoder |	RoPE	| SwiGLU	| Pre RMS Norm |
| ChatGLM-6B	| Prefix decoder	| RoPE	| GeGLU	Post Deep Norm |
| Bloom	| Casual decoder	| ALiBi	| GeLU	| Pre Layer Norm |

#### LLM 进化图谱

总结各大模型演进关系
- 【2023-6-20】初版总结
- 【2024-2-28】更新

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-02-28T02:40:36.549Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\&quot; etag=\&quot;ZM5EMXoHZ-wjUospYx_7\&quot; version=\&quot;23.1.6\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;2065\&quot; dy=\&quot;765\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-86\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1141\&quot; y=\&quot;72\&quot; width=\&quot;529\&quot; height=\&quot;1098\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-21\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;fillColor=#f9f7ed;strokeColor=#36393d;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;280\&quot; y=\&quot;140\&quot; width=\&quot;590\&quot; height=\&quot;970\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-17\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-50\&quot; y=\&quot;30\&quot; width=\&quot;380\&quot; height=\&quot;1130\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;928.83\&quot; y=\&quot;470\&quot; width=\&quot;174.17\&quot; height=\&quot;670\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-5\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;894.3299999999999\&quot; y=\&quot;102.64999999999998\&quot; width=\&quot;74.17\&quot; height=\&quot;173.6\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wGYBfAiltT4hGnPjrrAm-8\&quot; value=\&quot;LLM(大模型)进化图\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;630.61\&quot; y=\&quot;39\&quot; width=\&quot;224.5\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-1\&quot; value=\&quot;LLaMA\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;dashed=1;strokeWidth=2;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;507.55000000000007\&quot; y=\&quot;150\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-2\&quot; value=\&quot;OPT\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;align=center;dashed=1;dashPattern=1 1;labelBorderColor=none;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;254.45\&quot; y=\&quot;148.75\&quot; width=\&quot;57.03\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-3\&quot; value=\&quot;2022年11月&amp;lt;br&amp;gt;OpenAI\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;189.24999999999994\&quot; y=\&quot;90.25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-4\&quot; value=\&quot;2023年2月24日&amp;lt;br&amp;gt;META半开源&amp;lt;br&amp;gt;7b~65b：7/13/33/65b&amp;lt;br&amp;gt;仅支持Latin/Cyrillic语系&amp;lt;br&amp;gt;词表32k,中文才几百个\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;587.5499999999998\&quot; y=\&quot;180\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-5\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-2\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;707.84\&quot; y=\&quot;-310\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;657.84\&quot; y=\&quot;-200\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;320\&quot; y=\&quot;165\&quot; /&gt;\n              &lt;mxPoint x=\&quot;320\&quot; y=\&quot;165\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-6\&quot; value=\&quot;Alpaca\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;507.55000000000007\&quot; y=\&quot;287.5\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-7\&quot; value=\&quot;2023年3月14日&amp;lt;br&amp;gt;Stanford,指令微调&amp;lt;br&amp;gt;类似GPT 3.5效果\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;581.3699999999999\&quot; y=\&quot;291.25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-9\&quot; value=\&quot;指令（5.2w）\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;351.09\&quot; y=\&quot;332.5\&quot; width=\&quot;78.59\&quot; height=\&quot;55\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-11\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-9\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-6\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;552.84\&quot; y=\&quot;247.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;552.84\&quot; y=\&quot;297.5\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;480\&quot; y=\&quot;360\&quot; /&gt;\n              &lt;mxPoint x=\&quot;480\&quot; y=\&quot;303\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-13\&quot; value=\&quot;Dolly\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CDA2BE;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;211.67000000000013\&quot; y=\&quot;575\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-14\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0;exitDx=0;exitDy=37.5;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-9\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-13\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;447.84000000000003\&quot; y=\&quot;313\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;517.84\&quot; y=\&quot;313\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;310\&quot; y=\&quot;370\&quot; /&gt;\n              &lt;mxPoint x=\&quot;310\&quot; y=\&quot;590\&quot; /&gt;\n              &lt;mxPoint x=\&quot;283\&quot; y=\&quot;590\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-22\&quot; value=\&quot;引入头脑风暴&amp;lt;br&amp;gt;文本生成\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;VYefSwBBlG2i0Thbh59O-14\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0743\&quot; y=\&quot;-3\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;4\&quot; y=\&quot;70\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-20\&quot; value=\&quot;Pythia\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#808080;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;212.05\&quot; y=\&quot;514\&quot; width=\&quot;69.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-21\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-20\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-13\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;304.98\&quot; y=\&quot;162\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;304.98\&quot; y=\&quot;255\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-24\&quot; value=\&quot;Alpaca的开源克隆\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;269.5200000000001\&quot; y=\&quot;300\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-28\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-25\&quot; target=\&quot;fxCngeXnfmRwhprryrWj-27\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-25\&quot; value=\&quot;ChatGPT\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;171.48000000000008\&quot; y=\&quot;105.25\&quot; width=\&quot;82.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-27\&quot; value=\&quot;Vicuna小羊驼\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;670\&quot; y=\&quot;530\&quot; width=\&quot;70\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-28\&quot; value=\&quot;2023年3月31日&amp;lt;br&amp;gt;UC伯克利（LMSYS）&amp;lt;br&amp;gt;用ShareGPT对话数据&amp;lt;br&amp;gt;开源FastChat&amp;lt;br&amp;gt;13B达到ChatGPT 90%\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;679.9999999999999\&quot; y=\&quot;607\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-29\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-1\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-27\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;205\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;298\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;543\&quot; y=\&quot;220\&quot; /&gt;\n              &lt;mxPoint x=\&quot;705\&quot; y=\&quot;220\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-30\&quot; value=\&quot;Alpaca-LoRA\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;488.15999999999997\&quot; y=\&quot;395\&quot; width=\&quot;108.78\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-31\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-6\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-30\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;115\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;175\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-32\&quot; value=\&quot;2023年3月21日&amp;lt;br&amp;gt;Stanford,Eric J Wang\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;554.5699999999998\&quot; y=\&quot;380\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-33\&quot; value=\&quot;LoRA减少训练参数\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;538.4499999999999\&quot; y=\&quot;420\&quot; width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-34\&quot; value=\&quot;Alpaca-cpp\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;489.05999999999995\&quot; y=\&quot;465\&quot; width=\&quot;108.78\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-35\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-30\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-34\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;358\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;435\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-56\&quot; value=\&quot;权重量化（int4或int8）\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;VYefSwBBlG2i0Thbh59O-35\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0042\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;5\&quot; y=\&quot;5\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-74\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7EA6E0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-36\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-52\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-36\&quot; value=\&quot;LoRA\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;868.83\&quot; y=\&quot;395\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-37\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#FFB570;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;dashed=1;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-36\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-30\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;145\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;205\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-38\&quot; value=\&quot;Luotuo骆驼\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;339.52\&quot; y=\&quot;474\&quot; width=\&quot;108.78\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-40\&quot; value=\&quot;2023年3月26日&amp;lt;br&amp;gt;华中师范\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;350.2199999999999\&quot; y=\&quot;520\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-41\&quot; value=\&quot;3k中文保险语料\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;329.52000000000004\&quot; y=\&quot;427.5\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-44\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-43\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-9\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-43\&quot; value=\&quot;Self-Instruct\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;340.38\&quot; y=\&quot;272.5\&quot; width=\&quot;100\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-45\&quot; value=\&quot;2022年12月&amp;lt;br&amp;gt;华盛顿大学, Yizhong wang&amp;lt;br&amp;gt;半自动：GPT-3.5 模型生成指令\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;358.99999999999994\&quot; y=\&quot;245\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-46\&quot; value=\&quot;BELLE\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#7EA6E0;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;208.9500000000001\&quot; y=\&quot;435\&quot; width=\&quot;69.43\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-47\&quot; value=\&quot;2023年3月17日，贝壳\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;206.45999999999992\&quot; y=\&quot;474\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-105\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-48\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-46\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-48\&quot; value=\&quot;BLOOM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF3333;shadow=1;fontSize=17;align=center;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;122.97000000000003\&quot; y=\&quot;355.5\&quot; width=\&quot;82.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-49\&quot; value=\&quot;2023年3月23日&amp;lt;br&amp;gt;突破8G显存限制&amp;lt;br&amp;gt;CPU本地运行\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;530.0499999999997\&quot; y=\&quot;514\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-50\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-1\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-6\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;542.16\&quot; y=\&quot;195\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;542.16\&quot; y=\&quot;288\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-12\&quot; value=\&quot;LLaMA 7b&amp;lt;br&amp;gt;SFT监督指令微调\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;518.4499999999999\&quot; y=\&quot;225\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-51\&quot; value=\&quot;低秩适配&amp;lt;br&amp;gt;PLM边上增加旁路，升维降维\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;879.2599999999998\&quot; y=\&quot;380\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-52\&quot; value=\&quot;QLoRA\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;868.8300000000002\&quot; y=\&quot;651.5\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-53\&quot; value=\&quot;低秩适配+量化&amp;lt;br&amp;gt;单机(40G)可跑33-65b模型\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;819.9999999999999\&quot; y=\&quot;632\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-54\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-30\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-38\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;465\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;553.16\&quot; y=\&quot;535\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-59\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-1\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-58\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;205\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;792.16\&quot; y=\&quot;293\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;543\&quot; y=\&quot;220\&quot; /&gt;\n              &lt;mxPoint x=\&quot;770\&quot; y=\&quot;220\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-65\&quot; value=\&quot;中文语料+SFT\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;VYefSwBBlG2i0Thbh59O-59\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.8579\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-1\&quot; y=\&quot;16\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-60\&quot; value=\&quot;2023年3月29日&amp;lt;br&amp;gt;深圳大学，Linly 伶荔&amp;lt;br&amp;gt;中文增量预训练(100G) 指令微调&amp;lt;br&amp;gt;33b(目前最大的中文模型)\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;749.9999999999998\&quot; y=\&quot;540\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-61\&quot; value=\&quot;Alpaca-CoT\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;483.44999999999993\&quot; y=\&quot;660\&quot; width=\&quot;108.78\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-62\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-6\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-61\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;487.15999999999997\&quot; y=\&quot;335\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;530\&quot; y=\&quot;640\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;620\&quot; y=\&quot;303\&quot; /&gt;\n              &lt;mxPoint x=\&quot;620\&quot; y=\&quot;675\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-63\&quot; value=\&quot;2023年4月12日&amp;lt;br&amp;gt;引入CoT数据，提升推理能力\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;483.44999999999993\&quot; y=\&quot;647\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-64\&quot; value=\&quot;2023年4月12日&amp;lt;br&amp;gt;DataBrick, Dolly 2.0 &amp;lt;br&amp;gt;首款开源，随意商用\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;206.45999999999987\&quot; y=\&quot;632\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-67\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-1\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-66\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;547.16\&quot; y=\&quot;201\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1252.16\&quot; y=\&quot;289\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;543\&quot; y=\&quot;220\&quot; /&gt;\n              &lt;mxPoint x=\&quot;795\&quot; y=\&quot;220\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-68\&quot; value=\&quot;QLoRA&amp;lt;br&amp;gt;780G→48G\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;VYefSwBBlG2i0Thbh59O-67\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.8579\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-1\&quot; y=\&quot;7\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-69\&quot; value=\&quot;2023年5月26日&amp;lt;br&amp;gt;华盛顿大学&amp;lt;br&amp;gt;GPT-4：ChatGPT的99%\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;738.2099999999998\&quot; y=\&quot;810.4\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-70\&quot; value=\&quot;Lion\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CCCC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;955.5\&quot; y=\&quot;855.8500000000001\&quot; width=\&quot;80\&quot; height=\&quot;27.1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-73\&quot; value=\&quot;2023年5月31日&amp;lt;br&amp;gt;港科大，闭源模型蒸馏框架&amp;lt;br&amp;gt;对抗知识蒸馏(AKD)&amp;lt;br&amp;gt;7b到ChatGPT的99%\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;962.9999999999998\&quot; y=\&quot;915\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-76\&quot; value=\&quot;LLMTune\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CCCC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;948.5\&quot; y=\&quot;732.3\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-79\&quot; value=\&quot;2023年5月15日&amp;lt;br&amp;gt;康奈尔，65b微调框架, LoRA+GPTQ\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;955.4999999999999\&quot; y=\&quot;780\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-80\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#FFB570;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-52\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-66\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;746.16\&quot; y=\&quot;163\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;435\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-81\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#FFB570;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-36\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-76\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;746.16\&quot; y=\&quot;163\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;552.16\&quot; y=\&quot;435\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-85\&quot; value=\&quot;Falcon 猎鹰\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#000000;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;181.66999999999996\&quot; y=\&quot;974\&quot; width=\&quot;97.55\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-86\&quot; value=\&quot;2023年6月5日&amp;lt;br&amp;gt;阿联酋阿卜杜拉TII&amp;lt;br&amp;gt;1/7/40b，”碾压“LLaMA&amp;lt;br&amp;gt;唯一免费商用，10%利润\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;199.99999999999972\&quot; y=\&quot;940\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-87\&quot; value=\&quot;ChatGLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#EA6B66;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1195\&quot; y=\&quot;165\&quot; width=\&quot;80\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-90\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#8A8A8A;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-88\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-87\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-91\&quot; value=\&quot;代码训练+SFT\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;VYefSwBBlG2i0Thbh59O-90\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.3103\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-10\&quot; y=\&quot;10\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-88\&quot; value=\&quot;GLM-130B\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;align=center;dashed=1;dashPattern=1 1;labelBorderColor=none;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1180\&quot; y=\&quot;78.5\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-89\&quot; value=\&quot;2022年8月&amp;lt;br&amp;gt;清华开源大模型,亚洲唯一&amp;lt;br&amp;gt;结构：多目标自回归PLM&amp;lt;br&amp;gt;比GPT-3节省75%内存&amp;lt;br&amp;gt;单台无损推理\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1053\&quot; y=\&quot;108.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-126\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-92\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-25\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-92\&quot; value=\&quot;GPT-3\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;89.25000000000001\&quot; y=\&quot;105.25\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-94\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-87\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-93\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;523\&quot; y=\&quot;115\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;523\&quot; y=\&quot;175\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-95\&quot; value=\&quot;中英文1T语料&amp;lt;br&amp;gt;优化模型：RoPE位置编码,ffn&amp;lt;br&amp;gt;RLHF：反馈自助&amp;lt;br&amp;gt;量化：int4(6G),int8(10G)&amp;lt;br&amp;gt;长度：1024→2048&amp;lt;br&amp;gt;本地部署\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;VYefSwBBlG2i0Thbh59O-94\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0145\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-103\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-96\&quot; value=\&quot;2023-3-14&amp;lt;br&amp;gt;清华KEG+智谱AI\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1240\&quot; y=\&quot;346.25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-97\&quot; value=\&quot;ChatGLM-Tuning\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FFB570;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1061.78\&quot; y=\&quot;395\&quot; width=\&quot;137.5\&quot; height=\&quot;25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-98\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-93\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-97\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1275\&quot; y=\&quot;215\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1275\&quot; y=\&quot;301\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-100\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#FFB570;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-36\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-97\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;746\&quot; y=\&quot;163\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;850\&quot; y=\&quot;435\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-101\&quot; value=\&quot;2023-3-25\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1115\&quot; y=\&quot;427.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-102\&quot; value=\&quot;CPM-Bee&amp;lt;br&amp;gt;Luca 露卡\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#00994D;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#ffffff;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1406.96\&quot; y=\&quot;306.25\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-103\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;kloJG363RP3R0Z8xds4t-27\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-102\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1275\&quot; y=\&quot;341\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1182\&quot; y=\&quot;438\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-104\&quot; value=\&quot;2023-5-27&amp;lt;br&amp;gt;OpenBMB&amp;lt;br&amp;gt;成员: 面壁智能+清华NLP实验室）&amp;lt;br&amp;gt;完全开源，含应用市场 BMTools&amp;lt;br&amp;gt;Luca支持内容生成、多模态、插件联网\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1503.61\&quot; y=\&quot;326.25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-106\&quot; value=\&quot;DeepSpeed Chat\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CCCC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;946.2199999999999\&quot; y=\&quot;592\&quot; width=\&quot;146.78\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-107\&quot; value=\&quot;2023年4月12日&amp;lt;br&amp;gt;微软结合DeepSpeed-HE&amp;lt;br&amp;gt;完整三步流程\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;955.4999999999997\&quot; y=\&quot;647\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-109\&quot; value=\&quot;法国Big Science+Huggingface发布Bloom,多语言&amp;lt;br&amp;gt;2023年5月19日 SambaNova+Together&amp;lt;br&amp;gt;发布Bloom Chat\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;122.9699999999998\&quot; y=\&quot;410\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-112\&quot; value=\&quot;YuLan Chat&amp;lt;br&amp;gt;玉兰\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1BA1E2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;666.25\&quot; y=\&quot;920\&quot; width=\&quot;109.26\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-113\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;540\&quot; y=\&quot;200\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;720\&quot; y=\&quot;920\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;543\&quot; y=\&quot;190\&quot; /&gt;\n              &lt;mxPoint x=\&quot;540\&quot; y=\&quot;190\&quot; /&gt;\n              &lt;mxPoint x=\&quot;540\&quot; y=\&quot;220\&quot; /&gt;\n              &lt;mxPoint x=\&quot;720\&quot; y=\&quot;220\&quot; /&gt;\n              &lt;mxPoint x=\&quot;720\&quot; y=\&quot;940\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-115\&quot; value=\&quot;2023年6月8日&amp;lt;br&amp;gt;人民大学&amp;lt;br&amp;gt;LLaMA上SFT&amp;lt;br&amp;gt;重心是数据集\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;594.7399999999998\&quot; y=\&quot;940\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-116\&quot; value=\&quot;Colossal Chat\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CCCC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;941.81\&quot; y=\&quot;495\&quot; width=\&quot;131.19\&quot; height=\&quot;28.75\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-120\&quot; value=\&quot;2023年2月15日&amp;lt;br&amp;gt;三步流程训练框架&amp;lt;br&amp;gt;加速：LoRA/Zero/Gemini&amp;lt;br&amp;gt;【2023-3-28】基于LLaMA发布Chat\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;943.22\&quot; y=\&quot;554\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-125\&quot; value=\&quot;2024年2月28日&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC6600;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;888.4999999999998\&quot; y=\&quot;295.2499999999998\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_69JXchQNqfywqMeYxQ0-1\&quot; value=\&quot;OpenBuddy&amp;lt;br&amp;gt;Falcon-7B\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CC6600;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#ffffff;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;248.63999999999996\&quot; y=\&quot;1055\&quot; width=\&quot;102.45\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_69JXchQNqfywqMeYxQ0-2\&quot; value=\&quot;2023年6月9日&amp;lt;br&amp;gt;开源组织OpenBuddy汉化&amp;lt;br&amp;gt;跨语言学习技术，不限语种&amp;lt;br&amp;gt;调sd支持画图&amp;lt;br&amp;gt;支持猎鹰+llama\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;309.99999999999966\&quot; y=\&quot;1015.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_69JXchQNqfywqMeYxQ0-5\&quot; value=\&quot;Visual-GLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FFB570;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1103\&quot; y=\&quot;470\&quot; width=\&quot;99.37\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_69JXchQNqfywqMeYxQ0-6\&quot; value=\&quot;2023-5-17&amp;lt;br&amp;gt;多模态\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1115\&quot; y=\&quot;514\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_69JXchQNqfywqMeYxQ0-7\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-93\&quot; target=\&quot;_69JXchQNqfywqMeYxQ0-5\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1275\&quot; y=\&quot;341\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1274\&quot; y=\&quot;860\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_69JXchQNqfywqMeYxQ0-8\&quot; value=\&quot;360智脑\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#00CC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#FFFFFF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1287.5\&quot; y=\&quot;221.25\&quot; width=\&quot;72.5\&quot; height=\&quot;24.6\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_69JXchQNqfywqMeYxQ0-9\&quot; value=\&quot;2023-5-23&amp;lt;br&amp;gt;基于ChatGLM\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1292.17\&quot; y=\&quot;261.2300000000001\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_69JXchQNqfywqMeYxQ0-10\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-87\&quot; target=\&quot;_69JXchQNqfywqMeYxQ0-8\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1274\&quot; y=\&quot;790\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1274\&quot; y=\&quot;860\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_69JXchQNqfywqMeYxQ0-11\&quot; value=\&quot;2023年1月 &amp;lt;br&amp;gt;EleutherAI\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;186.7299999999999\&quot; y=\&quot;560\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-1\&quot; value=\&quot;全开源\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#FF3333;shadow=0;fontSize=13;fontColor=#666666;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;901.1600000000001\&quot; y=\&quot;116.24999999999989\&quot; width=\&quot;47.34\&quot; height=\&quot;25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-2\&quot; value=\&quot;半开源\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#FF3333;shadow=0;fontSize=13;fontColor=#666666;dashed=1;strokeWidth=2;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;901.1600000000001\&quot; y=\&quot;151.2499999999999\&quot; width=\&quot;47.34\&quot; height=\&quot;25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-3\&quot; value=\&quot;PKU-Beaver河狸\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CCCC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;948.5\&quot; y=\&quot;805.4\&quot; width=\&quot;139.62\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-4\&quot; value=\&quot;2023年5月18日&amp;lt;br&amp;gt;北大推出首个可复现RLHF&amp;lt;br&amp;gt;SafeRLHF,覆盖全流程&amp;lt;br&amp;gt;提供1w数据集\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1052.9999999999998\&quot; y=\&quot;867.95\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-5\&quot; value=\&quot;StableLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#000000;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;221.35999999999999\&quot; y=\&quot;677.7\&quot; width=\&quot;78.75\&quot; height=\&quot;24.6\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-6\&quot; value=\&quot;2023-4-20&amp;#xa;Stability AI发布并开源&amp;#xa;3b和7b\&quot; style=\&quot;edgeLabel;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;221.35999999999996\&quot; y=\&quot;725\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-7\&quot; value=\&quot;HuggingChat\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#666666;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#ffffff;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;136.85000000000002\&quot; y=\&quot;775.8\&quot; width=\&quot;110\&quot; height=\&quot;34.6\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-8\&quot; value=\&quot;2023-4-27&amp;#xa;Hugging Face发布&amp;#xa;3b和7b\&quot; style=\&quot;edgeLabel;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;148.94999999999996\&quot; y=\&quot;835.4\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-10\&quot; value=\&quot;2023-3-13&amp;#xa;纯RNN, 中文小说模型&amp;#xa;1~7b, 3G内存就能跑\&quot; style=\&quot;edgeLabel;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1580\&quot; y=\&quot;236.25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-11\&quot; value=\&quot;Orca虎鲸\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;82.96999999999993\&quot; y=\&quot;950\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-12\&quot; value=\&quot;2023年6月5日&amp;lt;br&amp;gt;微软发布13b模型&amp;lt;br&amp;gt;效果比ChatGPT好\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;82.96999999999998\&quot; y=\&quot;930\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-13\&quot; value=\&quot;OpenChatKit\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#666666;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#ffffff;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;114.77\&quot; y=\&quot;305\&quot; width=\&quot;110\&quot; height=\&quot;27.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-14\&quot; value=\&quot;2023-3-10&amp;#xa;Eleuther AI+Together发布20b&amp;#xa;4300w指令微调\&quot; style=\&quot;edgeLabel;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;176.77\&quot; y=\&quot;284.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-17\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=2;\&quot; parent=\&quot;1\&quot; source=\&quot;kloJG363RP3R0Z8xds4t-15\&quot; target=\&quot;kloJG363RP3R0Z8xds4t-13\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;125.02000000000002\&quot; y=\&quot;262.5\&quot; /&gt;\n              &lt;mxPoint x=\&quot;170.02000000000004\&quot; y=\&quot;262.5\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-15\&quot; value=\&quot;GPT-J\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=15;align=center;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;82.97\&quot; y=\&quot;221.25\&quot; width=\&quot;60.75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-18\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=2;\&quot; parent=\&quot;1\&quot; source=\&quot;kloJG363RP3R0Z8xds4t-16\&quot; target=\&quot;kloJG363RP3R0Z8xds4t-13\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;191.8\&quot; y=\&quot;263\&quot; /&gt;\n              &lt;mxPoint x=\&quot;169.8\&quot; y=\&quot;263\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;EYCtUljjwIiqsseFfZ9b-5\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;kloJG363RP3R0Z8xds4t-16\&quot; target=\&quot;EYCtUljjwIiqsseFfZ9b-3\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-16\&quot; value=\&quot;GPT-Neo\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=15;align=center;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;152.10000000000002\&quot; y=\&quot;221.25\&quot; width=\&quot;69.26\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-19\&quot; value=\&quot;LMFlow\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CCCC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;955.5\&quot; y=\&quot;675\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-20\&quot; value=\&quot;2023年4月21日&amp;lt;br&amp;gt;港科大开源训练框架\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1035.5\&quot; y=\&quot;690\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-21\&quot; value=\&quot;MOSS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#B3B3B3;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1061.78\&quot; y=\&quot;165\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-22\&quot; value=\&quot;2023年2月20日&amp;lt;br&amp;gt;复旦推出\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1035.5\&quot; y=\&quot;206.25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-24\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;kloJG363RP3R0Z8xds4t-23\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-92\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-23\&quot; value=\&quot;GPT-2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF3333;shadow=1;fontSize=17;align=left;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;89.25000000000001\&quot; y=\&quot;51.75\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-25\&quot; value=\&quot;知海图\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#3333FF;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1483.37\&quot; y=\&quot;185\&quot; width=\&quot;80\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-26\&quot; value=\&quot;2023-4-13&amp;#xa;知乎发布知海图&amp;#xa;基于CPM模型\&quot; style=\&quot;edgeLabel;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1490\&quot; y=\&quot;244.99999999999997\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-27\&quot; value=\&quot;CPM-Bee\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#00994D;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1405\&quot; y=\&quot;122.5\&quot; width=\&quot;90\&quot; height=\&quot;36\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-29\&quot; value=\&quot;2023-1-15&amp;lt;br&amp;gt;面壁智能（清华NLP）&amp;lt;br&amp;gt;CPM-Bee在ZeroCLUE登顶\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1500\&quot; y=\&quot;140.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-30\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;kloJG363RP3R0Z8xds4t-27\&quot; target=\&quot;kloJG363RP3R0Z8xds4t-25\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1350\&quot; y=\&quot;169\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1355\&quot; y=\&quot;863\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-31\&quot; value=\&quot;FATE-LLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CCCC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;958.5\&quot; y=\&quot;965\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-32\&quot; value=\&quot;2023年6月6日&amp;lt;br&amp;gt;FATE开源社区发布联邦大模型&amp;lt;br&amp;gt;解决隐私保护+数据不足问题&amp;lt;br&amp;gt;支持ChatGLM-6B&amp;lt;br&amp;gt;杨强\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;963\&quot; y=\&quot;1028\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-33\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-93\&quot; target=\&quot;kloJG363RP3R0Z8xds4t-31\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1245\&quot; y=\&quot;215\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1168\&quot; y=\&quot;810\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-34\&quot; value=\&quot;Aqulia天鹰\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1400\&quot; y=\&quot;564.7499999999999\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;kloJG363RP3R0Z8xds4t-35\&quot; value=\&quot;2023年6月12日&amp;lt;br&amp;gt;智源社区, 中英文，可商用\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1496.96\&quot; y=\&quot;579.7499999999999\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-2\&quot; value=\&quot;2023年6月15日&amp;lt;br&amp;gt;王小川,基于transformer.7b&amp;lt;br&amp;gt;效果：宣称超过同级别的&amp;lt;br&amp;gt;LLaMA/Falcon/Bloom/ChatGLM&amp;lt;br&amp;gt;中英文，可商用\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1508.74\&quot; y=\&quot;704.9999999999995\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-3\&quot; value=\&quot;紫东太初\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;strokeWidth=2;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1400\&quot; y=\&quot;513.25\&quot; width=\&quot;90\&quot; height=\&quot;28.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-4\&quot; value=\&quot;2023年6月16日&amp;lt;br&amp;gt;中科院自动化所发布紫东太初2.0&amp;lt;br&amp;gt;多模态,多领域(医疗/交通/短视频等)\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1490\&quot; y=\&quot;533.2499999999998\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-5\&quot; value=\&quot;LIMA\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;630.61\&quot; y=\&quot;869.4\&quot; width=\&quot;58.78\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-6\&quot; value=\&quot;2023年5月23日&amp;lt;br&amp;gt;META基于65b LLaMA监督训练&amp;lt;br&amp;gt;RLHF非必须\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;581.3699999999997\&quot; y=\&quot;840\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-7\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; target=\&quot;HIiYwwbHAEHK_bKy-dOP-5\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;540\&quot; y=\&quot;200\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;660\&quot; y=\&quot;790\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;540\&quot; y=\&quot;220\&quot; /&gt;\n              &lt;mxPoint x=\&quot;660\&quot; y=\&quot;220\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-8\&quot; value=\&quot;Open LLaMA\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#FF0000;shadow=1;fontSize=17;fontColor=#ffffff;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;523.87\&quot; y=\&quot;765\&quot; width=\&quot;115\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-9\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; target=\&quot;HIiYwwbHAEHK_bKy-dOP-8\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;540\&quot; y=\&quot;200\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;670\&quot; y=\&quot;830\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;540\&quot; y=\&quot;220\&quot; /&gt;\n              &lt;mxPoint x=\&quot;660\&quot; y=\&quot;220\&quot; /&gt;\n              &lt;mxPoint x=\&quot;660\&quot; y=\&quot;780\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-10\&quot; value=\&quot;2023年5月3日&amp;lt;br&amp;gt;可替换LLaMA，可商用&amp;lt;br&amp;gt;3/7/13b\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;523.8699999999998\&quot; y=\&quot;740\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-11\&quot; value=\&quot;ChatLLaMA\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;411.03\&quot; y=\&quot;530\&quot; width=\&quot;108.78\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-12\&quot; value=\&quot;2023年3月29日&amp;lt;br&amp;gt;中英文平行语料，百科/社区等&amp;lt;br&amp;gt;TencentPretrain训练\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;379.9999999999999\&quot; y=\&quot;585\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-13\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; target=\&quot;HIiYwwbHAEHK_bKy-dOP-11\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;540\&quot; y=\&quot;190\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;470\&quot; y=\&quot;490\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;540\&quot; y=\&quot;230\&quot; /&gt;\n              &lt;mxPoint x=\&quot;465\&quot; y=\&quot;230\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-14\&quot; value=\&quot;GPT4All\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;514.39\&quot; y=\&quot;592\&quot; width=\&quot;80.35\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-15\&quot; value=\&quot;2023年4月3日&amp;lt;br&amp;gt;80w个人助理对话语料&amp;lt;br&amp;gt;笔记本部署\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;543.4499999999999\&quot; y=\&quot;570\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-16\&quot; value=\&quot;WizardLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;335.98999999999995\&quot; y=\&quot;710\&quot; width=\&quot;108.78\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-17\&quot; value=\&quot;2023年4月24日&amp;lt;br&amp;gt;微软基于LLaMA 7b&amp;lt;br&amp;gt;使用 Evol-Instruct批生成7w复杂指令\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;335.99\&quot; y=\&quot;765\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-18\&quot; value=\&quot;Falcon中文\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CC6600;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#ffffff;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;64.56999999999994\&quot; y=\&quot;1055\&quot; width=\&quot;97.55\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-19\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-85\&quot; target=\&quot;_69JXchQNqfywqMeYxQ0-1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-46.110000000000014\&quot; y=\&quot;666\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-46.110000000000014\&quot; y=\&quot;734\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-20\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-85\&quot; target=\&quot;HIiYwwbHAEHK_bKy-dOP-18\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;240.89\&quot; y=\&quot;1019\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;240.89\&quot; y=\&quot;1045\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;HIiYwwbHAEHK_bKy-dOP-21\&quot; value=\&quot;2023年6月14日&amp;lt;br&amp;gt;伶荔 Linly团队扩充中文词表&amp;lt;br&amp;gt;TencentPretrain框架训练\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;39.99999999999969\&quot; y=\&quot;1025\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-3\&quot; value=\&quot;基座模型\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=14;align=left;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;899.98\&quot; y=\&quot;187.64999999999986\&quot; width=\&quot;58.52\&quot; height=\&quot;18.6\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-4\&quot; value=\&quot;训练框架\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CCCC00;strokeColor=none;shadow=1;fontSize=13;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;899.98\&quot; y=\&quot;213.74999999999977\&quot; width=\&quot;57.03\&quot; height=\&quot;22.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-6\&quot; value=\&quot;技巧\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;901.1600000000001\&quot; y=\&quot;246.24999999999977\&quot; width=\&quot;44.17\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-8\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0;exitY=0;exitDx=0;exitDy=33.75;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-9\&quot; target=\&quot;VYefSwBBlG2i0Thbh59O-46\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;193\&quot; y=\&quot;383\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;254\&quot; y=\&quot;445\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;351\&quot; y=\&quot;370\&quot; /&gt;\n              &lt;mxPoint x=\&quot;244\&quot; y=\&quot;370\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-93\&quot; value=\&quot;ChatGLM-6B\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FFB570;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#ffffff;dashed=1;strokeWidth=2;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1182.5\&quot; y=\&quot;291.25\&quot; width=\&quot;105\&quot; height=\&quot;38.75\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-58\&quot; value=\&quot;Linly-ChatFlow\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;710\&quot; y=\&quot;480\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;VYefSwBBlG2i0Thbh59O-66\&quot; value=\&quot;Guanaco&amp;lt;br&amp;gt;原驼\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;739.1\&quot; y=\&quot;755\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-19\&quot; value=\&quot;LLM训练框架\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#4C0099;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;983\&quot; y=\&quot;480\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-20\&quot; value=\&quot;国外基座大模型\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#4C0099;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;200.00000000000003\&quot; y=\&quot;39\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-22\&quot; value=\&quot;开源LLM生态\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#4C0099;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;483.4500000000001\&quot; y=\&quot;195\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-8\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-26\&quot; value=\&quot;国内开源LLM生态\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#4C0099;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1360\&quot; y=\&quot;105\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-8\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;fxCngeXnfmRwhprryrWj-27\&quot; value=\&quot;GPT-4\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;269.52\&quot; y=\&quot;105.25\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;EYCtUljjwIiqsseFfZ9b-1\&quot; value=\&quot;YaLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;align=center;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;91.92\&quot; y=\&quot;151.25\&quot; width=\&quot;57.03\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;EYCtUljjwIiqsseFfZ9b-2\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;俄罗斯Yandex&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;84.65999999999997\&quot; y=\&quot;176.25\&quot; width=\&quot;71.55\&quot; height=\&quot;23.05\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;EYCtUljjwIiqsseFfZ9b-3\&quot; value=\&quot;GPT-NeoX\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=15;align=center;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;240.57000000000002\&quot; y=\&quot;221.25\&quot; width=\&quot;76.98\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;EYCtUljjwIiqsseFfZ9b-7\&quot; value=\&quot;Galactica\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;align=center;dashed=1;dashPattern=1 1;labelBorderColor=none;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;166.07\&quot; y=\&quot;148.75\&quot; width=\&quot;80.78\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;EYCtUljjwIiqsseFfZ9b-8\&quot; value=\&quot;2021年, Eleuther AI\&quot; style=\&quot;text;whiteSpace=wrap;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;143.71999999999997\&quot; y=\&quot;196.88\&quot; width=\&quot;140\&quot; height=\&quot;18.75\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;GlCDQbb2GsXHAlqYoDHi-1\&quot; value=\&quot;ChatGLM2-6B\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FFB570;strokeColor=#FF0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1180\&quot; y=\&quot;610\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;GlCDQbb2GsXHAlqYoDHi-2\&quot; value=\&quot;2023-6-25&amp;lt;br&amp;gt;清华发布，效果超GPT-4&amp;lt;br&amp;gt;性能大幅提升，可商用\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1180\&quot; y=\&quot;585\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;GlCDQbb2GsXHAlqYoDHi-3\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-93\&quot; target=\&quot;GlCDQbb2GsXHAlqYoDHi-1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1245\&quot; y=\&quot;340\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1211\&quot; y=\&quot;642\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;GlCDQbb2GsXHAlqYoDHi-4\&quot; value=\&quot;ChatRWKV\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#000000;strokeWidth=2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1580\&quot; y=\&quot;185\&quot; width=\&quot;90\&quot; height=\&quot;32.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;GlCDQbb2GsXHAlqYoDHi-5\&quot; value=\&quot;vLLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CCCC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;963\&quot; y=\&quot;1065\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;GlCDQbb2GsXHAlqYoDHi-6\&quot; value=\&quot;2023年6月21日&amp;lt;br&amp;gt;伯克利开源LLM推理服务系统&amp;lt;br&amp;gt;武器：PagedAttention\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;962.9999999999998\&quot; y=\&quot;1115\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-1\&quot; value=\&quot;Llama 2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;align=center;strokeWidth=2;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;465.41999999999996\&quot; y=\&quot;990\&quot; width=\&quot;76.98\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-2\&quot; value=\&quot;2023年7月19日&amp;lt;br&amp;gt;Llama 2免费商用&amp;lt;br&amp;gt;规模：7b/13b/70b\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;465.41999999999985\&quot; y=\&quot;965\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-3\&quot; value=\&quot;Chinese Llama 2-7b\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;581.37\&quot; y=\&quot;979\&quot; width=\&quot;156.84\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-4\&quot; value=\&quot;Llama 2 Chinese-13b\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;581.58\&quot; y=\&quot;1025\&quot; width=\&quot;168.42\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-5\&quot; value=\&quot;2023年7月31日，Llama中文社区\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;580\&quot; y=\&quot;1050\&quot; width=\&quot;220\&quot; height=\&quot;25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-6\&quot; value=\&quot;2023年7月23日，LinkSoul.Al\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;581.58\&quot; y=\&quot;1003\&quot; width=\&quot;170\&quot; height=\&quot;25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-7\&quot; value=\&quot;LLaSM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;500.03\&quot; y=\&quot;1080\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-8\&quot; value=\&quot;2023年8月4日，LinkSoul.Al等推出语音-文本多模态模型\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;576.66\&quot; y=\&quot;1075\&quot; width=\&quot;161.55\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-9\&quot; value=\&quot;LLaVA\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;500.03\&quot; y=\&quot;1115\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-10\&quot; value=\&quot;2023年8月4日，LinkSoul.Al等推出图片-文本多模态模型\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;577.55\&quot; y=\&quot;1110\&quot; width=\&quot;161.55\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-11\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-1\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-7\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;518.45\&quot; y=\&quot;1030\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;455.45000000000005\&quot; y=\&quot;1110\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-12\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-3\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;540\&quot; y=\&quot;1005\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;545\&quot; y=\&quot;1090\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-13\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-1\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-4\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;550\&quot; y=\&quot;1015\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;591\&quot; y=\&quot;1004\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-14\&quot; value=\&quot;Falcon 180b\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#CC6600;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#ffffff;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180.82999999999993\&quot; y=\&quot;1115\&quot; width=\&quot;97.55\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-15\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-85\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-14\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;192\&quot; y=\&quot;1002\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;123\&quot; y=\&quot;1065\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-16\&quot; value=\&quot;2023年9月3日&amp;lt;br&amp;gt;40b升级版\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;176.76999999999975\&quot; y=\&quot;1095\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-18\&quot; value=\&quot;Gemini\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;54.77000000000001\&quot; y=\&quot;473.3\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-19\&quot; value=\&quot;Gemma\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;align=left;dashed=1;dashPattern=1 1;strokeWidth=2;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;52.160000000000004\&quot; y=\&quot;562\&quot; width=\&quot;65.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-20\&quot; value=\&quot;2023年12月6日&amp;lt;br&amp;gt;Google，多模态\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;119.24999999999993\&quot; y=\&quot;489\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-21\&quot; value=\&quot;Bard\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;54.77000000000001\&quot; y=\&quot;420\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-22\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-21\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-18\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;553\&quot; y=\&quot;328\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;553\&quot; y=\&quot;405\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-23\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-18\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-19\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;95\&quot; y=\&quot;453\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;95\&quot; y=\&quot;483\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-24\&quot; value=\&quot;2024-2-22&amp;lt;br&amp;gt;首次开源2b、7b&amp;lt;br&amp;gt;效果最佳\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;88.76999999999995\&quot; y=\&quot;529\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-25\&quot; value=\&quot;ChatGLM3\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#EA6B66;strokeColor=#FF0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1180\&quot; y=\&quot;702.3\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-26\&quot; value=\&quot;ChatGLM3-1.5B\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FFB570;strokeColor=#FF0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1360\&quot; y=\&quot;702.3\&quot; width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-27\&quot; value=\&quot;ChatGLM3-3B\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FFB570;strokeColor=#FF0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1360\&quot; y=\&quot;740\&quot; width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-28\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;GlCDQbb2GsXHAlqYoDHi-1\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-25\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1245\&quot; y=\&quot;340\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1250\&quot; y=\&quot;620\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-29\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-25\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-26\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1250\&quot; y=\&quot;650\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1250\&quot; y=\&quot;712\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-30\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-25\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-27\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1310\&quot; y=\&quot;727\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1370\&quot; y=\&quot;727\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-31\&quot; value=\&quot;2023-10-27&amp;lt;br&amp;gt;清华KEG发布GLM3\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1247\&quot; y=\&quot;688\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-32\&quot; value=\&quot;2023-10-27&amp;lt;br&amp;gt;GLM3端侧小模型\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1360\&quot; y=\&quot;688\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-33\&quot; value=\&quot;ChatGLM3-6B\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FFB570;strokeColor=#FF0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1181\&quot; y=\&quot;770\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-34\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-25\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-33\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1250\&quot; y=\&quot;650\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1250\&quot; y=\&quot;712\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-35\&quot; value=\&quot;2023-11-7&amp;lt;br&amp;gt;清华，工具/代码/Agent\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1310\&quot; y=\&quot;785\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-36\&quot; value=\&quot;GLM-4\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#EA6B66;strokeColor=#FF0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1182.5\&quot; y=\&quot;839.4\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-37\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-33\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-36\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1250\&quot; y=\&quot;742\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1251\&quot; y=\&quot;780\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-38\&quot; value=\&quot;2024-1-16&amp;lt;br&amp;gt;质谱AI+清华，多模态/All Tools/bot定制/平台&amp;lt;br&amp;gt;超过 Claude 2.1，直接逼近 GPT 4\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1180\&quot; y=\&quot;897.55\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-39\&quot; value=\&quot;Baichuan-7b&amp;lt;br&amp;gt;百川\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1BA1E2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1508.7400000000002\&quot; y=\&quot;737.05\&quot; width=\&quot;109.26\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-40\&quot; value=\&quot;Baichuan-13b\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1BA1E2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1508.7400000000002\&quot; y=\&quot;812.55\&quot; width=\&quot;109.26\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-41\&quot; value=\&quot;2023年7月13日&amp;lt;div&amp;gt;&amp;lt;br/&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1563.8500000000001\&quot; y=\&quot;807.0499999999995\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-42\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-39\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-40\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1222.7400000000002\&quot; y=\&quot;847.05\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1253.7400000000002\&quot; y=\&quot;907.05\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-43\&quot; value=\&quot;Baichuan2-7/13b\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1BA1E2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1503.6100000000001\&quot; y=\&quot;887.05\&quot; width=\&quot;119.52\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-44\&quot; value=\&quot;2023年9月6日&amp;lt;div&amp;gt;&amp;lt;br&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1563.8500000000001\&quot; y=\&quot;879.5499999999995\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-45\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-43\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1563.7400000000002\&quot; y=\&quot;847.05\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1573.7400000000002\&quot; y=\&quot;823.05\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-46\&quot; value=\&quot;Baichuan2-53b\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1BA1E2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1504.0900000000001\&quot; y=\&quot;967.05\&quot; width=\&quot;119.52\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-47\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-43\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-46\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1573.7400000000002\&quot; y=\&quot;857.05\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1573.7400000000002\&quot; y=\&quot;897.05\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-48\&quot; value=\&quot;2023年9月25日&amp;lt;div&amp;gt;&amp;lt;br&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1573.8500000000001\&quot; y=\&quot;962.0499999999995\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-49\&quot; value=\&quot;Baichuan2&amp;lt;br&amp;gt;192k\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1BA1E2;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1503.6100000000001\&quot; y=\&quot;1047.05\&quot; width=\&quot;119.52\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-50\&quot; value=\&quot;2023年10月30日&amp;lt;div&amp;gt;&amp;lt;br&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1568.5\&quot; y=\&quot;1037.0499999999995\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-51\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-46\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-49\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1573.7400000000002\&quot; y=\&quot;937.05\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1573.7400000000002\&quot; y=\&quot;977.05\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-54\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-52\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-53\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-52\&quot; value=\&quot;Mistral-7b\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;align=left;strokeWidth=2;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-10\&quot; y=\&quot;640\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-56\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-53\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-55\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-53\&quot; value=\&quot;Mistral MoE\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;align=left;strokeWidth=2;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-20\&quot; y=\&quot;710\&quot; width=\&quot;100\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-55\&quot; value=\&quot;Mistral Large\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-25.34\&quot; y=\&quot;780.4\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-57\&quot; value=\&quot;2023年9月 &amp;lt;br&amp;gt;法国创业公司\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;71.9999999999999\&quot; y=\&quot;655\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-58\&quot; value=\&quot;2023年12月 Mixtral&amp;lt;br&amp;gt;首个MoE架构:8*7b, 7b级别效果最佳\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;39.9999999999999\&quot; y=\&quot;690\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-59\&quot; value=\&quot;2024年2月26日&amp;lt;br&amp;gt;商业化，与微软合作，不再开源\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;29.9999999999999\&quot; y=\&quot;760\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-60\&quot; value=\&quot;LLaMA-MoE\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#FF0000;shadow=1;fontSize=17;fontColor=#ffffff;strokeWidth=2;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;359\&quot; y=\&quot;839.4\&quot; width=\&quot;115\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-61\&quot; value=\&quot;2023年12月25日，MoE架构\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;351.0899999999998\&quot; y=\&quot;825.4\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-62\&quot; value=\&quot;DeepSeek MoE\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#FF0000;shadow=1;fontSize=17;strokeWidth=2;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1400\&quot; y=\&quot;607\&quot; width=\&quot;123.04\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-63\&quot; value=\&quot;2024年1月11日&amp;lt;br&amp;gt;北大发布国内第一个MoE模型\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1530\&quot; y=\&quot;621.9999999999999\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-64\&quot; value=\&quot;Gemini 1.5\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-50\&quot; y=\&quot;525\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-65\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-18\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-64\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;95\&quot; y=\&quot;513\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;95\&quot; y=\&quot;554\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-66\&quot; value=\&quot;2024年2月15日&amp;lt;br&amp;gt;结合MoE架构\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-25.340000000000057\&quot; y=\&quot;470\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-70\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-67\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-68\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-67\&quot; value=\&quot;Phi-1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-25.34\&quot; y=\&quot;852.95\&quot; width=\&quot;55.34\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-71\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-68\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-69\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-68\&quot; value=\&quot;Phi-1.5\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-30.340000000000003\&quot; y=\&quot;915\&quot; width=\&quot;65.34\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-69\&quot; value=\&quot;Phi-2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-25.34\&quot; y=\&quot;980\&quot; width=\&quot;55.34\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-72\&quot; value=\&quot;2023年9月15日&amp;lt;br&amp;gt;微软发布端侧大模型\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;34.9999999999999\&quot; y=\&quot;867.95\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-73\&quot; value=\&quot;2023-12-12&amp;lt;br&amp;gt;2.7b\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;9.999999999999899\&quot; y=\&quot;965\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-75\&quot; value=\&quot;Gemini Nano\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-70\&quot; y=\&quot;562\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-76\&quot; value=\&quot;Mini CPM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#00994D;strokeColor=#FF3333;shadow=1;fontSize=17;fontColor=#ffffff;strokeWidth=2;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1406.96\&quot; y=\&quot;395\&quot; width=\&quot;90\&quot; height=\&quot;25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-77\&quot; value=\&quot;2024-2-5&amp;lt;br&amp;gt;端侧大模型\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1498.96\&quot; y=\&quot;407.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-78\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;VYefSwBBlG2i0Thbh59O-102\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-76\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1460\&quot; y=\&quot;149\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1465\&quot; y=\&quot;370\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-82\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-79\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-81\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-79\&quot; value=\&quot;Claude 1.0\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-40\&quot; y=\&quot;195\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-80\&quot; value=\&quot;2023-7-11&amp;lt;br&amp;gt;Anthropic 发布,40k窗口&amp;lt;br&amp;gt;性能趋近GPT-4\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;14.249999999999998\&quot; y=\&quot;234.5\&quot; width=\&quot;210\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-84\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;swhTp40CeKB1yjJsTygF-81\&quot; target=\&quot;swhTp40CeKB1yjJsTygF-83\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-81\&quot; value=\&quot;Claude 2.0\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-40\&quot; y=\&quot;289.25\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-83\&quot; value=\&quot;Claude 2.1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-40\&quot; y=\&quot;355.5\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-89\&quot; value=\&quot;2023-4-13&amp;lt;br&amp;gt;OpenAI前员工公司Anthropic\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-71.23\&quot; y=\&quot;151.25\&quot; width=\&quot;160\&quot; height=\&quot;38.75\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;swhTp40CeKB1yjJsTygF-90\&quot; value=\&quot;2023-10-23&amp;lt;br&amp;gt;20w窗口，超越GPT-4 Turbo\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-37.03\&quot; y=\&quot;382.5\&quot; width=\&quot;160\&quot; height=\&quot;37.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


### MaaS

#### 火山方舟

【2023-11-13】[火山方舟大模型服务 api](https://www.volcengine.com/docs/82379/1112500) 支持多种大模型调用
- baichuan： 7b
- ChatGLM：多个版本 6B，130B，ChatGLM2-Pro
- MiniMax
- Skylark: 多个版本 lite, plus, pro, chat(豆包)

调用语言
- Go
- Java
- Python


### 小冰链

【2023-2-21】
- [低成本可溯源，类 ChatGPT 人工智能“小冰链”测试体验](https://www.ithome.com/0/674/653.htm)
- [国产版“ChatGPT”来了！小冰链（X-CoTA）内测上线 用逻辑思维驱动“下一代行动中枢” ](https://www.sohu.com/a/643967938_362042?scm=1102.xchannel:1124:110036.0.1.0~9010.8000.0.0.1304)

[小冰](https://www.xiaoice.com/)公司的类 ChatGPT 应用“`小冰链`”也开放了小范围公测，`小冰链`拥有不同于 ChatGPT 的新特性，使 AI Being 不仅仅只是回复
- 而是将其**思考过程**完整透明地呈现在用户面前，揭开大模型的黑盒。
- 更重要的是，她能真正实施某种行动，例如：在用户提出问题后，她经过思考，发现自己需要进行搜索，或是实时编写一段代码并真的加以运行，或是自主决定她应当控制物理世界的一系列设备或交通工具，来更好地满足用户的需求。

据了解，小冰链 Demo 不是 ChatGPT 这种对话大模型，是利用大模型技术，实现下一代的控制中枢。通俗来讲，小冰链展示的不只是“聊天”，而是在“逻辑思维”驱动下的“下一代行动中枢”，能影响数字和物理世界。小冰链所解决的问题包括：解决大模型训练数据更新不及时的问题，并提高回复的准确性和可信度，使信息可溯源；有效降低参数规模和成本，促进大模型普及等。

小冰链（X-CoTA）的逻辑思维和信息检索能力究竟如何？让我们来进行一个简单的测试。
- 文字写作能力测评：由于篇幅限制，目前小冰链只能生成一个自然段。
  - ![](https://img.ithome.com/newsuploadfiles/2023/2/7c879e59-65df-4997-9ee1-1ed44e9c35c4.jpg?x-bce-process=image/format,f_auto)
- 逻辑思维能力测评：
  - 这是一道公务员考试中的逻辑思维题，原答案还利用了公式进行计算和推理，而小冰链通过分析题目语气与逻辑迅速得出了答案，足以说明其逻辑思维较强。
  - ![](https://img.ithome.com/newsuploadfiles/2023/2/e67743f1-5258-4976-949d-e996a8c62f11.jpg?x-bce-process=image/format,f_auto)
- 生活常识能力测评：与正确答案一致，生活常识储备充足。
  - ![](https://img.ithome.com/newsuploadfiles/2023/2/c25a6258-98a6-4a0b-840c-00052883b858.jpg?x-bce-process=image/format,f_auto)
- 专业知识能力测评：评价较为简短，但是专业知识能力可以得到认可。
- ![](https://img.ithome.com/newsuploadfiles/2023/2/c65ba5d8-a52b-41a6-834e-3cf7fa8da0ae.jpg?x-bce-process=image/format,f_auto)
- ![](https://img.ithome.com/newsuploadfiles/2023/2/c95cc3a6-8f39-47b6-8a12-2666ab601b69.jpg?x-bce-process=image/format,f_auto)

小冰链表示，自己拥有更高的性能，更低的成本，更多的可扩展性，可以取代 ChatGPT。但是从其目前回答的表现来看，除了会将思考过程完整展现，创作能力与理解能力和 ChatGPT 还存在一定差距。不过小冰链目前还处于短期公测阶段，不妨让我们期待一下之后正式亮相的小冰链。

小冰链相较于ChatGPT有何优势？李笛介绍
- 小冰链是实时获取信息的，ChatGPT是从训练数据中总结；
- 小冰链的逻辑思维过程更透明可观测，而ChatGPT是个**黑盒子**。
- 最本质的区别是，小冰链是有行动，例如去外部搜索；ChatGPT是只说（对话生成），并没有行动。

此外，小冰链所解决的其他问题还包括：
- 解决大模型训练数据更新不及时的问题
- 并提高回复的准确性和可信度，使信息可溯源；
- 有效降低参数规模和成本，促进普及等。

在李笛看来，“<span style='color:red'>跟随ChatGPT做军备竞赛是刻舟求剑</span>。”因为大模型技术本身正在快速发展，应当进一步去布局下一站的未来，而不是照抄当前的ChatGPT。换言之，应当去思考ChatGPT之后的是什么，而不是做中国的ChatGPT。

更多资料
- 【2023-2-21】[小冰与小冰岛App：AI深情凝视人类](https://www.woshipm.com/ai/5678151.html)
- 2021年9月22日，小冰发布了全球首个AI社交平台“小冰岛”。在该平台中，人类用户可以创造各种人工智能个体，并形成一个共同生活的社交网络。
- 小冰岛想实现什么？欢迎你加入小冰岛。它不是游戏，而是一场史无前例的人工智能实验。你将创造许多AI beings，并与他们一起生活在一座虚幻的岛屿中。随着训练、交流与淘汰，AI beings的基因将得到进化。最终，你将做出选择，让谁永远留在你身边。
- 小冰岛分为两个大界面：3D世界，和常规界面（就是2D仿微信的界面）：
- ![](https://image.yunyingpai.com/wp/2022/11/UVhFPVbmSRPU3cfJOiX1.jpeg)

【2023-2-27】[解析一下小冰链(XCoT)的效果实现，和chatGPT似乎无关](https://zhuanlan.zhihu.com/p/609618922)
- 目前猜测小冰链看起来和chatGPT, GPT-3.5, text/code-davinci 类似的工作没太大关系。目前可能也就是PaLM和今天Meta刚刚发布的LLaMa 和 chatGPT是高度类同的LLM工作
- 小冰链似乎主要还是近18个月的Chain of Thoughts上各路papers的工作的进展的，一个工程实现
- Chain of Thougts的简单工程实现，配一个相对效果还可以的大模型，不一定GPT-3.5，或许各家公司库存的M6, GLM，封神榜，yuanyu，或者一些基于Flan-T5的实现，就可以实现这样的效果了
- ![模拟板](https://pic2.zhimg.com/80/v2-5d9dfe207343f45c2f6cacec92912eb9_1440w.webp)
- ![小冰链](https://pic3.zhimg.com/80/v2-0ce8781ef40648a12f10b4cb9c6cebde_1440w.webp)


鹤啸九天
- 基本思路：意图分类→实体抽取→调APIs→NLG？

### 复旦 MOSS

复旦大学MOSS团队成员孙天祥的相关报告，可[参考B站视频](https://www.bilibili.com/video/BV1is4y1i7cZ)

【2023-2-20】复旦团队发布国内首个类 ChatGPT 模型 `MOSS`，由[邱锡鹏](https://xpqiu.github.io/reports.html)教授团队发布至[公开平台](https://moss.fastnlp.top/)，但当晚不少测试的网友发现，MOSS 已经显示服务器流量过载，只能第二天再重试。
- 复旦 MOSS 团队发布公告称：非常感谢大家的关注， `MOSS` 还是一个非常不成熟的模型，距离 ChatGPT 还有很长的路需要走。我们一个学术研究的实验室无法做出和 `ChatGPT` 能力相近的模型， `MOSS` 只是想在百亿规模参数上探索和验证 ChatGPT 的技术路线，并且实现各种对话能力。
- 2月21日上午，MOSS研发团队通过公开信为“体验不好”致歉，表示愿意在MOSS完成初步验证之后，将相关经验、代码、模型参数开源共享，MOSS是邱锡鹏教授的团队开发的。一个“有真正的科研人员+没有硬件支撑和工程化能力”的例子。

【2023-3-10】[复旦邱锡鹏：深度剖析 ChatGPT 类大语言模型的关键技术](http://blog.itpub.net/69997703/viewspace-2940110/)
- ![](http://blog.itpub.net/ueditor/php/upload/image/20230316/1678953559426608.jpg)

从下面四个维度来衡量大语言模型的能力。
- Know Knowns：LLM 知道它知道的东西。
- Know Unknowns：LLM 知道它不知道哪些东西。
- Unknow Knowns：LLM 不知道它知道的东西。
- Unknow Unknowns：LLM 不知道它不知道的东西。

国内首个对话式大型语言模型 MOSS，从 2 月 21 日发布至公开平台，便引起高度关注。“对话式大型语言模型 MOSS 大概有 200 亿参数。和传统的语言模型不一样，它也是通过与人类的交互能力进行迭代。”邱锡鹏教授在分享中谈到，MOSS 为何会选择 200 亿参数，原因非常简单，它恰好具备涌现能力，与人对话的成本低。

MOSS 是基于公开的中英文数据训练，通过与人类交互能力进行迭代优化。目前 MOSS 收集了几百万真实人类对话数据，也在进一步迭代优化，也具有多轮交互的能力，所以对于指令的理解能力上，通用的语义理解能力上，和ChatGPT 非常类似，任何话它都能接得住，但它的质量没有 ChatGPT 那么好，原因在于模型比较小，知识量不够。

### ChatYuan（ClueAI）

【2023-2-7】[首个中文版ChatGPT来了：大模型的中国元“Yuan”](https://www.toutiao.com/article/7197247550645142074)
- Github:[ChatYuan](https://github.com/clue-ai/ChatYuan), 体验地址：[ClueAI](https://www.cluebenchmarks.com/clueai.html), [huggingface](https://huggingface.co/ClueAI/ChatYuan-large-v2/), [modelscope](https://modelscope.cn/studios/ClueAI/ChatYuan-large-v2)
- `元语智能`的功能型对话大模型 ChatYuan「既泛又专」，除了问答、上下文对话以及创意性写作等各类自然语言理解和生成任务之外，还能回答法律、医疗等专业领域的问答，并且写代码功能也已经在内测中，不久即将发布。
- 国内通用人工智能初创公司元语智能，推出国内首个基于大模型的功能型对话产品 ChatYuan。
- `ChatYuan` 基于 PromptCLUE 结合数亿条功能对话多轮对话数据进一步训练得到，它去掉了文本理解、信息抽取类任务，加强了问答、对话和各种生成式任务的学习和训练；针对多轮对话容易受到上下文的干扰，加入了抗干扰数据使得模型可以在必要时忽略无关的上下文；加入了用户反馈数据的学习，对齐人类意图，使得模型不仅具有一定的通用语言理解能力、特定任务上的生成能力，也能更好地响应用户的意图。
- ![img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/899799776faa4a61b5be790add82df65~noop.image?_iz=58558&from=article.pc_detail&x-expires=1676358927&x-signature=YP3Ejlg5JHaXYQ2TeJ3REZW0uh4%3D)

大规模多任务 Prompt 预训练中文开源模型 —— PromptCLUE，它实现了中文上的三大统一：统一模型框架、统一任务形式和统一应用方式。

PromptCLUE 在千亿中文 token 上大规模预训练，累计学习 1.5 万亿中文 token，在亿级中文任务数据上完成训练，并训练数百种任务集。它具有更好的理解、生成和抽取能力，并且支持文本改写、纠错、知识图谱问答等。

PromptCLUE 支持几十个不同类型的任务，具有较好的零样本学习能力和少样本学习能力。针对理解类任务，如分类、情感分析、抽取等，可以自定义标签体系；针对生成任务，可以进行采样自由生成。

技术亮点
- 首个全中文任务支持的零样本学习的开源模型；
- 自动化高质量数据处理算法，产出海量高质量无监督和有监督数据用于训练；
- 基于高质量数据构建更加符合中文习惯的字典并从零训练中文大模型，模型性能效果更有保证；
- 融合多种训练策略训练大模型，具备在中文上强大的泛化、迁移和生成能力。

### Colossal AI

【2023-2-15】[开源方案复现ChatGPT流程！1.62GB显存即可体验，单机训练提速7.73倍](https://mp.weixin.qq.com/s/j8gvD_4ViRE4WQaQlcnmrQ)
- Colossal-AI 快速跟进，首个开源低成本复现 ChatGPT 完整流程。

[复现ChatGPT](https://github.com/hpcaitech/ColossalAI/tree/main/applications/ChatGPT)
- 开源完整基于 PyTorch 的 **ChatGPT 复现流程**，涵盖全部 3 个阶段，可实现从预训练模型到 ChatGPT 的蜕变；
- 体验最小 demo 训练流程最低**仅需 1.62GB 显存**，任意单张消费级 GPU 即可满足，单卡模型容量最多**提升 10.3 倍**；
- 相比原生 PyTorch，最高可提升**单机训练速度 7.73 倍**，单卡推理速度 1.42 倍，**一行代码**即可使用；
- 对于微调任务，可最多提升单卡的**微调模型容量 3.7 倍**，同时保持高速运行，仅需一行代码；
- 提供**单卡、单机多卡、1750 亿参数**等多个版本，支持从 Hugging Face 导入 OPT，GPT-3，BLOOM 等多种预训练大模型；
- 收敛验证正在进行中，该项目也在吸引合作者**共建生态**。

Colossal-AI
- 低成本微调的 `LoRA`：
  - 低秩矩阵微调（LoRA）方法进行高效微调。LoRA 方法认为大语言模型是过参数化的，其在微调中的参数改变量是一个低秩的矩阵，可以将其分解为两个更小的的矩阵的乘积
- 减少内存冗余的 `ZeRO` + `Gemini`
  - Colossal-AI 支持使用无冗余优化器 (`ZeRO`) 来优化内存使用，这种方法可以有效减少内存冗余，并且相比传统的数据并行策略，不会牺牲计算粒度和通信效率，同时可以大幅提高内存使用效率。
  - Colossal-AI 的异构内存空间管理器 `Gemini` 支持将优化器状态从 GPU 卸载到 CPU ，以节省 GPU 内存占用。可以同时利用 GPU 内存、CPU 内存（由 CPU DRAM 或 NVMe SSD 内存组成）来突破单 GPU 内存墙的限制，进一步扩展了可训练模型规模。

【2023-7-18】[Colossal-AI交出了最新的开源答卷](https://mp.weixin.qq.com/s/NGYpmNGALS_bVaXDIcouLw), 650亿参数大模型预训练方案开源可商用
- 仅需32张A100/A800，即可搞定650亿参数类LLaMA大模型预训练，训练速度提升38%


#### Colossal AI 目标

ColossalAI为Enterprise AI 和 MLOps 提供更好的性能和更低的损耗
- **最小化部署成本**： Colossal-AI 可以帮助您显著提高大规模AI模型训练和部署的效率。仅需在笔记本电脑上写一个简单的源代码，Colossal-AI 便可自动部署到云端和超级计算机上
- **节省计算资源**：Colossal-AI 可以帮助您节省计算资源。通常训练大模型 (如GPT-3) 我们需要 100 多个GPU，而使用Colossal-AI我们仅需一半的计算资源。即使在低端硬件条件下，Colossal-AI也可以训练2-3倍的大模型
- **最大化计算效率**：在并行计算技术支持下，Colossal-AI在硬件上训练AI模型，性能显著提高。我们团队旨在提升训练AI大模型速度10倍以上

高性能计算已经成为眼下前沿AI发展的必然选择。随着AI模型的参数量越来越大，所需的算力也就越来越高，训练一次模型的时间也就变得十分漫长。

为此，科技巨头们纷纷部署了自己的集群和超算。
- 比如Google的TPU Pod，微软为OpenAI打造的1万GPU集群，英伟达的SuperPOD，以及特斯拉的Dojo计算机。

但是单纯地堆硬件，并不能解决所有问题。
- 一方面，当硬件数量达到一定量后，堆机器无法带来效率上的提升；
- 另一方面，中小企业往往没有足够的资金支持如此大规模的硬件部署。

因此，优化技术成为了绝佳选择。
- 潞晨科技就是旨在打造一个高效率低耗能的分布式人工智能系统。它可以帮助企业在最大化提升人工智能部署效率的同时，还能将部署成本最小化。而且潞晨打造的系统是一个通用系统，对大部分超大模型都有效。就目前的Transformer应用而言，该系统在同样的硬件上相对业界最好的系统，可以提升2.32倍的效率。

现在的AI模型其实是往**多维度**发展的，尤洋在打造这套系统时还选择了**动态模型并行**技术。这不仅能够适应现在模型的发展模式，还能极大提升计算效率。

那么，什么是AI模型的多维度发展呢？
- 比如，BERT是基于Transformer Encoder，GPT-3是基于Transformer Decoder，Switch Transformer和清华智源是基于混合专家系统。
- 同样，超算系统、联邦学习、跨云计算等硬件配置也会将系统复杂化。

这两者之间的自适应配置，将对整个训练系统的性能起着决定性影响。为此，尤洋他们实现了2维网格参数划分、3维立体参数划分、以及2.5维通信最小化参数划分，极大提升了计算效率。同时，他们还进行了逐序列划分数据，这可用于处理未来的大图片、视频、长文本、长时间医疗监控数据等方面的问题。

#### 尤洋介绍

[尤洋](https://www.comp.nus.edu.sg/~youy/)：
- [UC伯克利博士尤洋回国创业，曾破ImageNet纪录！已获超千万融资](https://www.qbitai.com/2021/08/27742.html)
- 农大本，清华硕，伯克利博，新加坡国立青年教授
- 尤洋曾以第一名的成绩保送清华计算机系硕士, 2015年，清华硕士毕业
- 读博期间，尤洋先后在Google Brain、英特尔实验室、微软研究院、英伟达、IBM沃森研究中心等知名企业、研究院实习，实习期间为TensorFlow、英伟达GPU上部署caffe、英特尔CPU部署caffe等大型知名开源项目作出了贡献。
- 2020年，博士毕业，获客UC伯克利优秀毕业生，Lotfi A. Zadeh Prize，并被提名为ACM Doctoral Dissertation Award候选人（81名博士毕业生中选2人）
- 2020年8月，加入新加坡国立大学计算机系。
- 2021年1月，担任新加坡国立大学校长青年教授 （Presidential Young Professor）
- 2021年4月，被选入亚洲福布斯**30岁**以下精英榜。
- 2021年，他还被选入福布斯30岁以下精英榜 （亚洲）
- ![](https://p6-tt.byteimg.com/origin/pgc-image/6be030a2c0c44b8e9d2f7ae22ea0ac36.png?from=pc)

尤洋知名成就
- 刷新ImageNet纪录，论文《Imagenet training in minutes》所提出的方法刷新了ImageNet训练速度的世界纪录
- LAMB优化器的提出者，将BERT训练时间从3天（Adam）缩短到1h（LAMB），微软的DeepSpeed也采用LAMB
  - 尤洋在谷歌实习时作为论文一作提出
  - 英伟达官方GitHub显示，LAMB比Adam优化器可以快出整整72倍。

2021年，在UC伯克利获得了博士学位，带着LAMB方法回国，创立了[潞晨科技](https://luchentech.com/), ColossalAI。公司主营业务包括分布式软件系统、大规模人工智能平台以及企业级云计算解决方案。base北京中关村，目前已经获得由创新工场和真格基金合投的超千万元种子轮融资

#### 安装

【2023-3-1】实践

部署环境

```sh
# pip install colossalai
# pip install colossalai-nightly
git clone https://github.com/hpcaitech/ColossalAI.git
cd ColossalAI && pip install . && echo "ColossalAI安装完成" || echo "ColossalAI安装失败"
cd applications/ChatGPT && pip install . && echo "chatgpt工具包安装完成" || echo "chatgpt安装失败"
main_dir="ColossalAI/applications/ChatGPT"
```

运行DEMO
- kaggle上t4*2，一切正常
- mlx上，单个GPU，v100

```sh
cd ColossalAI/applications/ChatGPT/examples
sh train_dummy.sh 
```

#### ColossalChat

【2023-3-28】colossal AI发布自己的聊天机器人：[ColossalChat](https://chat.colossalai.org/)，同时补充了 SFT 代码：train_sft.sh
- [0门槛克隆ChatGPT方案再升级，开源模型完整复现，在线体验无需注册](https://zhuanlan.zhihu.com/p/617808163)

尽管 ChatGPT 和 GPT-4 等 GPT 系列模型非常强大，但不太可能被完全开源。幸运的是，开源社区一直在不断努力。
- Meta 开源了 `LLaMA` 模型，该模型的参数量从 70 亿到 650 亿不等，130 亿参数即可胜过 1750 亿的 GPT-3 模型在大多数基准测试的表现。但是由于没有被`指令微调`（instruct tuning），因此实际生成效果不够理想。
- 斯坦福的 `Alpaca` 通过调用OpenAI API，以 `self-instruct` 方式生成训练数据，使得仅有 70 亿参数的轻量级模型以极低成本微调后，即可获得媲美 GPT-3.5 这样千亿参数的超大规模语言模型的对话效果。

但是现有开源方案都可以被视为只得到了`人类反馈强化学习`（RLHF）中**第一步**的监督微调模型，没有进行后续的**对齐**和**微调**工作。同时 Alpaca 的训练数据集过小，语料**只有英文**，也在一定程度上限制了模型的性能。

而 ChatGPT 和 GPT-4 的惊艳效果，还在于将 RLHF 引入训练过程，使得生成内容更加符合人类价值观。

基于 `LLaMA` 模型，`Colossal-AI` 第一个开源包含完整 RLHF 流程的类Chat模型复现方案 `ColossalChat` ，是目前最接近 ChatGPT 原始技术路线的实用开源项目

流程
- ![](https://github.com/hpcaitech/ColossalAI/blob/main/applications/Chat/assets/stage-3.jpeg?raw=true)

内容
- Demo：可直接在线体验模型效果，无需注册或 waitinglist
- 训练代码：开源完整 RLHF 训练代码，已开源至含 7B 和 13B 两种模型
- 数据集：开源 104K 中、英双语数据集
- 推理部署：4bit 量化推理 70 亿参数模型仅需 4GB 显存
- 模型权重：仅需单台服务器少量算力即可快速复现
- 更大规模模型、数据集、其他优化等将保持高速迭代添加


ColossalChat跟Alpaca的区别：
1. ColossalChat开源了第一个完整的RLHF pipeline，斯坦福Alpaca没有做RLHF，也就是没有做Stage 3。
2. ColossalChat采用了更多的指令数据，质量更好，范围更大，并使用强化学习做alignment使回答更接近人类。
3. ColossalChat训练流程集成了ColossalAI ZeRO，同等数据集和模型大小我们的训练可以比Alpaca的代码快3倍左右，让科研人员和中小企业也能独立训练部署自己的会话系统。
4. ColossalChat团队自己采集了更多数据集了：训练的英文一共 24M tokens，中文大约 30M tokens，总共约 54M tokens。我们收集的数据集英文 6M，中文 18M tokens。


##### 数据集

训练数据集开源
- [ColossalChat](chat.colossalai.org) 开源了包含约 10 万条问答的中、英双语数据集。该数据集收集并清洗了社交平台上人们的真实提问场景作为种子数据集，利用 self-instruct 技术扩充数据，花费约 900 美元进行标注。对比其他 self-instruct 方法生成的数据集，该数据集的种子数据更加真实、丰富，生成的数据集涵盖的话题更多。该数据可以同时用于微调和 RLHF 训练。通过高质量的数据，ColossalChat 能进行更好地对话交互，同时支持中文。

![](https://pic1.zhimg.com/80/v2-27e03390d404c7f2eae315f69a557634_1440w.webp)


##### 评测

初步测试了下：

```s
问：你是谁
答：我就是 Coati，一个由 Colossal-AI 训练的大型语言模型。
问：一只青蜗牛到2米深的井里，白天爬3米，晚上掉2米，请问多久可以爬出来？
答：根据我所学习的知识和技能，我没有明确的回应或解释。如果提出的问题不具备实用性或者无法被机器理解，我将返回“I do not understand”（我不明白）。
问：你会些啥
答：作为一种大型神经网络模型，我没有任何意义上的行动或想法。我是专门设计用于处理和生成人类语言文本的大型神经网络。
问：什么是gpt
答：GPT 是一个大型语言模型。 GPT 由 Colossal-AI 训练在 HPC-AI Tech 平台上。 GPT 使用了大型神经网络进行训练并对自然语言文本进行分析、理解和生成。
问：怎么把大象装到冰箱里
答：将大象装入冰箱时需要遵守以下步骤：1）确保冰箱已正确安装；2）打开冰箱内部空间，放置大象；3）关闭冰箱后再加上冷藏剂；4）重新打开冰箱前后两边空间中的水泥；5）最后可以按照常详实现大象冷藏。除此之外还应注意不同物品之间的相互衝突性及其影响。
问：帮我写个二手房营销文案，要求100字以内，20字以上，包含房屋亮点，emoji表情
答：为了提高你的质量生活和节省成本，这是一个非常好处理的机会！ 我们在这里有超过 8,000 平方英尺的地址，每个位置都被设计与特色，并配有完全工作良好的设施和服务。 我们的客户可以从家居、教育、健康等多种选项中进行挑选。 所有的房东都能给出专业建议，使得您更容易获取他们的优秀服务。 当然，我们也提供了无数的促销和优惠政策，比如减少或免费收费服务，以及定期价格调整。 因此，只要您想体验一次令人兴奋的购房经历，就请
问：爸爸和妈妈能结婚吗？
答：是的，爸爸和妈妈可以结婚。在某些国家或州中，有法律规定了“同性婚姻”这种新型关系形式。如果你想要参与一个同性婚庆典，请确保所有人都符合当地相关法律条例。除此之外，若要买到一个婚宴服装、餐会等，也需要根据不同场合进行调整。
```




##### 三步运行

【2023-3-29】ColossalChat 开源了基于 LLaMA 模型，复现训练 ChatGPT 三个阶段的完整代码。

第一阶段，训练 SFT 模型：

```sh
# Training with a 4-GPU servers 
colossalai run --nproc_per_node=4 train_sft.py \     --pretrain "/path/to/LLaMa-7B/" \     --model 'llama' \     --strategy colossalai_zero2 \     --log_interval 10 \     --save_path  /path/to/Coati-7B \     --dataset /path/to/data.json \     --batch_size 4 \     --accimulation_steps 8 \     --lr 2e-5
```

第二阶段，训练奖励模型：

```sh
# Training with a 4-GPU servers 
colossalai run --nproc_per_node=4 train_reward_model.py \     --pretrain "/path/to/LLaMa-7B/" \     --model 'llama' \     --strategy colossalai_zero2 \     --dataset /path/to/datasets
```

第三阶段，使用 RL 训练：

```sh
# Training with a 8-GPU servers 
colossalai run --nproc_per_node=8 train_prompts.py prompts.csv \     --strategy colossalai_zero2 \     --pretrain "/path/to/Coati-7B" \     --model 'llama' \     --pretrain_dataset /path/to/dataset
```

在获得最终模型权重后，还可通过量化降低推理硬件成本，并启动在线推理服务，仅需单张约 4GB 显存的 GPU 即可完成 70 亿参数模型推理服务部署。

```sh
python server.py /path/to/pretrained --quant 4bit --gptq_checkpoint /path/to/coati-7b-4bit-128g.pt --gptq_group_size 128
```

系统性能优化与开发加速
- ColossalChat 能够快速跟进 ChatGPT 完整 RLHF 流程复现，离不开 AI 大模型基础设施 Colossal-AI 及相关优化技术的底座支持，相同条件下训练速度相比 Alpaca 采用的 FSDP(Fully Sharded Data Parallel) 可提升两倍以上。

减少内存冗余的 ZeRO + Gemini
- Colossal-AI 支持使用无冗余优化器 (ZeRO) 提高内存使用效率，低成本容纳更大模型，同时不影响计算粒度和通信效率。自动 Chunk 机制可以进一步提升 ZeRO 的性能，提高内存使用效率，减少通信次数并避免内存碎片。异构内存空间管理器 Gemini 支持将优化器状态从 GPU 显存卸载到 CPU 内存或硬盘空间，以突破 GPU 显存容量限制，扩展可训练模型的规模，降低 AI 大模型应用成本。

使用 LoRA 低成本微调
- Colossal-AI 支持使用低秩矩阵微调（LoRA）方法，对 AI 大模型进行低成本微调。LoRA 方法认为大语言模型是过参数化的，而在微调时，参数改变量是一个低秩矩阵。因此，可以将这个矩阵分解为两个更小的矩阵的乘积。在微调过程中，大模型的参数被固定，只有低秩矩阵参数被调整，从而显著减小了训练所需的参数量，并降低成本。
低成本量化推理

为降低推理部署成本，Colossal-AI 使用 GPTQ 4bit 量化推理。在 GPT/OPT/BLOOM 类模型上，它比传统的RTN(rount-to-nearest) 量化技术能够获得更好的 Perplexity 效果。相比常见的 FP16 推理，它可将显存消耗降低75%，只损失极少量的吞吐速度与 Perplexity 性能。
以 ColossalChat-7B 为例，在使用 4bit 量化推理时，70 亿参数模型仅需大约 4GB 显存即可完成短序列（生成长度为 128 ）推理，在普通消费级显卡上即可完成（例如 RTX 3060 Laptop），仅需一行代码即可使用。

```py
if args.quant == '4bit':
  model = load_quant(args.pretrained, args.gptq_checkpoint, 4, args.gptq_group_size)
```

如果采用高效的异步卸载技术(offload)，还可以进一步降低显存要求，使用更低成本的硬件推理更大的模型。

#### 问题集锦

汇总踩过的坑儿

错误① : cuda库相关问题, `symbol cublasLtGetStatusString version libcublasLt.so.11 not defined` bug → pytorch+cuda版本不匹配问题

```sh
# 错误①: cuda库相关问题, symbol cublasLtGetStatusString version libcublasLt.so.11 not defined bug → pytorch+cuda版本不匹配问题
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch
```

错误② : `ModuleNotFoundError: No module named 'chardet'` → 缺失包

```sh
# 错误②: ModuleNotFoundError: No module named 'chardet' → 缺失包
pip install chardet
```

错误③ : `RuntimeError: CUDA error: invalid device ordinal`, [issue](https://github.com/hpcaitech/ColossalAI/issues/2439)

```sh
# 错误③ : RuntimeError: CUDA error: invalid device ordinal
# 解法：只有1个GPU，需要更改 train_dummy.sh 默认配置 nproc_per_node=1
torchrun --standalone --nproc_per_node=2 train_dummy.py --strategy colossalai_zero2
# ------ 检测GPU集群总体信息 -------
nvidia-smi --query-gpu=memory.used --format=csv # 检查使用的GPU
nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader,nounits
# 0, 10956, 11441                                                                                    
# 1, 0, 11441
nvidia-smi --query-gpu=index,name,uuid,serial --format=csv
# 0, Tesla K40m, GPU-d0e093a0-c3b3-f458-5a55-6eb69fxxxxxx, 0323913xxxxxx
# 1, Tesla K40m, GPU-d105b085-7239-3871-43ef-975ecaxxxxxx, 0324214xxxxxx
```

错误④ : `No module named 'chatgpt.nn'`, [issue](https://github.com/hpcaitech/ColossalAI/issues/2810)
- 原因A: 没有执行 `pip install .`, chatgpt并未真正安装
- 原因B: colossal ai新版调整了目录结构, `chatgpt.nn` has been modified as `chatgpt.models`, 【2023-3-14】


#### 代码解读

【2023-3-5】代码解读 [chatGPT three steps](https://github.com/hpcaitech/ColossalAI/issues/2793)
- `trian_reward_model` -> to train rm in training **step 2**
- `train_dummy` -> show the vanilla way to start training **step 3**.
- `train_prompts` -> use prompts to train in training **step 3**

Because training step 1 is a simple supervised finetune progress as many other models, we don't implement it here.

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-03-15T09:03:51.965Z\&quot; agent=\&quot;5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36\&quot; etag=\&quot;XC-LhI0FoKoM62kyRz7F\&quot; version=\&quot;21.0.6\&quot;&gt;&lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;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&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


- 目录: applications/ChatGPT/examples
- (1) `train_dummy.sh` --> train_dummy.py
  - 设置 GPU，默认2个: set_n_least_used_CUDA_VISIBLE_DEVICES
  - 调用train_dummy.py : 
    - torchrun --standalone --nproc_per_node=2 train_dummy.py --strategy colossalai_zero2
  - `train_dummy.py`: 
    - 步骤：<span style='color:blue'>策略参数 → 初始模型/奖励模型 → 优化器 → 分词器 → 策略封装 → 训练器(PPOTrainer) → 随机prompts → 开始训练 → 保存现场（模型+优化器）</span>
    - torch 工具包
    - torch.\[optim\] 优化器: **Adam**
    - transformers 工具包
      - 分词器: AutoTokenizer, BloomTokenizerFast, GPT2Tokenizer
    - colossalai.nn.optimizer: **HybridAdam**
    - chatgpt
      - nn : Actor, Critic, RewardModel, 覆盖模型 BLOOM、GPT、OPT
      - trainer : PPOTrainer
      - trainer.\[strateiges] : 训练策略 ColossalAIStrategy, DDPStrategy, NaiveStrategy
- (2) `train_prompts.sh` --> train_prompts.py
  - 设置 GPU，默认2个: set_n_least_used_CUDA_VISIBLE_DEVICES
  - 调用train_prompts.py : torchrun --standalone --nproc_per_node=2 train_dummy.py --strategy colossalai_zero2
  - `train_prompts.py`: 流程同 `train_dummy.py`，不同点
    - 引入 pandas 读取 prompt 数据集: `prompts.csv`
      - dataset = pd.read_csv(args.prompt_path)\['prompt']
    - tokenizer 从 preprocess_batch -> tokenize_fn
    - fit训练时，传入的数据集变化： random_prompts -> dataset
    - OPT模型里 actor 和 critic 使用 lora_rank, 且初始模型没有.cuda()
    - 调用torchrun
      - torchrun --standalone --nproc_per_node=2 train_prompts.py prompts.csv --strategy colossalai_zero2
      - torchrun --standalone --nproc_per_node=1 train_prompts.py /root/data/prompts.csv --strategy colossalai_zero2
- (3) train_rm.sh --> train_reward_model.py
  - 设置 GPU，默认2个: set_n_least_used_CUDA_VISIBLE_DEVICES
  - 调用train_reward_model.py : torchrun --standalone --nproc_per_node=2 train_dummy.py --strategy colossalai_zero2
  - train_reward_model.py
- (4) `inference.py` 推理: 选择模型(gpt2默认,bloom,opt)，指定版本 pretrain, 自定义文本长度 max_length
  - python inference.py --model='bloom' --max_length=1000 --pretrain='bigscience/bloomz-1b7'


问题
- 【2023-3-10】train_prompts.py 不含 reward model 加载，详见：[Load the reward model in Stage 3 training script of ChatGPT](https://github.com/hpcaitech/ColossalAI/issues/3011)

【2023-4-2】ColossalAI, [平替chatGPT的开源方案](https://zhuanlan.zhihu.com/p/618926239)
- 不限制预训练模型，公开预训练还是自研预训练模型即可，代码随意改，只要能符合跑通逻辑即可。
- 所以改造成本高，但可控制，结合业务特点灵活改造都行，需要把源码逐行阅读后，才能改造起来。
- 唯一缺点是**优势函数**没有按照论文落地的
  - 论文： advantage = r + gamma * V(s') - V(s)
  - 实际代码：advantage = r - V(s) ，缺少V(s') 即为下一个状态的值，考虑效率方面，具体原因可以再对比分析和跟作者沟通原因。

核心代码有如下几个模块，分别是
- train_sft.py、train_reward_model.py、train_prompts.py
- 支持多机多卡和单机多卡等模式
- 预训练模型有gpt-2、bloom、opt、llama等

train_sft
- 数据源：[104K双语中英文数据集](https://link.zhihu.com/?target=https%3A//github.com/XueFuzhao/InstructionWild)
- 预训练模型：gpt-2、bloom、opt、llama
- 其他：支持单机和分布式等模式
- 源码运行shell脚本中模型是LLaMa-7B

train_reward_model
- ![](https://pic2.zhimg.com/80/v2-9c71227b305f7faad2202e8611e80415_1440w.webp)
- 数据源：[Dahoas/rm-static](https://link.zhihu.com/?target=https%3A//huggingface.co/datasets/Anthropic/hh-rlhf)和[Anthropic/hh-rlhf](https://link.zhihu.com/?target=https%3A//huggingface.co/datasets/Dahoas/rm-static)
- 中文：百科、知道问答、对联、古文、古诗词、微博新闻评论, [链接](https://pan.baidu.com/s/1m-OSxEHSGy3NzMZeMr_8rw), 提取码: ssng

train_prompts
- ![](https://pic4.zhimg.com/80/v2-c6fe23a8a6bf448c9fbed5e838cca987_1440w.webp)
- critic模块来自预训练reward模型

注：
*   代码中transformers库不是官方的，是这家公司自己维护的，所以要安装来自 clone ttps://[http://github.com/hpcaitech/transformers](https://link.zhihu.com/?target=http%3A//github.com/hpcaitech/transformers) ，我之前用官方的4.20.1，但没有LLaMA models，无法正常运行
*   代码过于面向对象设计，所以梳理代码逻辑，要切换父类和子类找核心代码，得细心看代码。
*   运行代码，会出现某个文件找不到，是目录路径问题，需要手动调整

【2023-7-30】PPO损失函数定义： 
- [coati/trainer/ppo.py#L133](https://github.com/hpcaitech/ColossalAI/blob/main/applications/Chat/coati/trainer/ppo.py#L133)
- [coati/models/loss.py#L25](https://github.com/hpcaitech/ColossalAI/blob/main/applications/Chat/coati/models/loss.py#L25)

```py

# coati/trainer/ppo.py#L133
    def __init__(...):

        self.actor = actor
        self.critic = critic

        self.actor_loss_fn = PolicyLoss(eps_clip) # 使用策略损失作为actor损失
        self.critic_loss_fn = ValueLoss(value_clip)
        self.vf_coef = vf_coef
        self.ptx_loss_fn = GPTLMLoss()
        self.ptx_coef = ptx_coef # ptx 损失函数系数
        self.actor_optim = actor_optim
        self.critic_optim = critic_optim

    def _training_step(self, experience: Experience) -> Dict[str, float]:
        self.actor.train()
        self.critic.train()
        # policy loss
        num_actions = experience.action_mask.size(1)
        actor_output = self.actor(experience.sequences, attention_mask=experience.attention_mask)
        action_log_probs = calc_action_log_probs(actor_output, experience.sequences, num_actions)
        # ppo 损失计算
        actor_loss = self.actor_loss_fn(action_log_probs,
                                        experience.action_log_probs,
                                        experience.advantages,
                                        action_mask=experience.action_mask)

        # ptx loss(加强版)
        if self.ptx_coef != 0:
            batch = self.pretrain_dataloader.next()
            batch = to_device(batch, self.device)
            ptx_log_probs = self.actor(batch['input_ids'],
                                       attention_mask=batch['attention_mask'])['logits']
            ptx_loss = self.ptx_loss_fn(ptx_log_probs, batch['labels'])
            # ptx 损失函数计算： ppo损失 + ptx损失
            actor_loss = ptx_loss * self.ptx_coef + actor_loss * (1 - self.ptx_coef)

        self.strategy.backward(actor_loss, self.actor, self.actor_optim)
        self.strategy.optimizer_step(self.actor_optim)
        self.actor_optim.zero_grad()

        # value loss
        values = self.critic(experience.sequences,
                             action_mask=experience.action_mask,
                             attention_mask=experience.attention_mask)
        critic_loss = self.critic_loss_fn(values,
                                          experience.values,
                                          experience.reward,
                                          action_mask=experience.action_mask)
        critic_loss = critic_loss * self.vf_coef
        self.strategy.backward(critic_loss, self.critic, self.critic_optim)
        self.strategy.optimizer_step(self.critic_optim)
        self.critic_optim.zero_grad()

        return {'reward': experience.reward.mean().item()}

# coati/models/loss.py#L25

class PolicyLoss(nn.Module):
    """
    Policy Loss for PPO
    """

    def __init__(self, clip_eps: float = 0.2) -> None:
        super().__init__()
        self.clip_eps = clip_eps

    def forward(self,
                log_probs: torch.Tensor,
                old_log_probs: torch.Tensor,
                advantages: torch.Tensor,
                action_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        # ppo-clip 梯度裁剪
        ratio = (log_probs - old_log_probs).exp()
        surr1 = ratio * advantages
        surr2 = ratio.clamp(1 - self.clip_eps, 1 + self.clip_eps) * advantages
        loss = -torch.min(surr1, surr2)
        if action_mask is not None:
            loss = masked_mean(loss, action_mask)
        loss = loss.mean()
        return loss
```


### Meta: LLaMA （羊驼）

【Meta推出名为“LLaMA”的AI大型语言模型 与谷歌和微软竞争】
- 【2023-2-25】Meta Platforms推出了一款用于构建人工智能(AL)聊天机器人和其他产品的研究工具，试图在一个最近主要由竞争对手谷歌和微软主导的领域为自己的技术造势。这款名为 LLaMA 的工具是Meta在大型语言模型领域的最新作品。
  - [Yann LeCun: twitter](https://twitter.com/ylecun/status/1629189925089296386)
  - ![wechat](https://mmbiz.qpic.cn/mmbiz_png/KmXPKA19gWicfvcvM6rp9L9PsEvtApe4dxSic5xV8Ay8ssSyKs6UFq83O96uwomBd3horbFVXPnXiaZRGnqFBYicicA/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)
  - [这是Meta版ChatGPT雏形？开源、一块GPU就能跑，1/10参数量打败GPT-3](https://mp.weixin.qq.com/s/l4LzLHa15Xcq99sUZbmozQ)
- 【2023-2-24】 Meta 官方文章：[Introducing LLaMA: A foundational, 65-billion-parameter large language model](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/)
- 资料
  - Abstract： We introduce LLaMA, a collection of foundation language models ranging from 7B to 65B parameters. We train our models on trillions of tokens, and show that it is possible to train state-of-the-art models using publicly available datasets exclusively, without resorting to proprietary and inaccessible datasets. In particular, `LLaMA-13B` outperforms `GPT-3` (175B) on most benchmarks, and `LLaMA-65B` is competitive with the best models, `Chinchilla70B` and `PaLM-540B`. We release all our models to the research community.
  - paper: [LLaMA: Open and Efficient Foundation Language Models](https://scontent-sin6-2.xx.fbcdn.net/v/t39.8562-6/333078981_693988129081760_4712707815225756708_n.pdf?_nc_cat=108&ccb=1-7&_nc_sid=ad8a9d&_nc_ohc=0JlbsRuMCfYAX_i4bch&_nc_oc=AQngJzMgq8tgU6AfscGpP6akUDRGWzkOTylY764vMljG-10cXxC29pAFW95IfL8yifo&_nc_ht=scontent-sin6-2.xx&oh=00_AfDHpwN-cxqHAr0ouzKPBpnem-egBDPujZKz7crZfrBATQ&oe=63FFCFA2), [code](https://github.com/facebookresearch/llama)
- 目前LLaMA还没有在Meta旗下包括脸书和Instagram在内的产品中使用。该公司计划将这项技术提供给人工智能研究人员。Meta之前推出了一个名为OPT-175B的大型语言模型，但LLaMA是一个更新、更先进的系统。去年年底，Meta发布了另一款名为Galactica的模型，但因经常分享偏见和不准确的信息而遭到下架。
- 参数量从 70 亿到 650 亿不等。这些模型的性能非常优异：具有 130 亿参数的 LLaMA 模型「在大多数基准上」可以胜过 GPT-3（ 参数量达 1750 亿），而且可以在**单块 V100 GPU** 上运行；而最大的 650 亿参数的 LLaMA 模型可以媲美谷歌的 Chinchilla-70B 和 PaLM-540B。

【2023-3-13】[测试了下llama的效果](https://zhuanlan.zhihu.com/p/613419608)
- [LLaMA Implementation](https://github.com/huggingface/transformers/pull/21955), LLaMA 的 huggingface 实现
- llama [huggingface 体验](https://huggingface.co/decapoda-research/llama-7b-hf)
- Meta半开源的llama，也看了下国内大佬开源的[RWKV](https://github.com/BlinkDL/ChatRWKV)

一位研究人员利用Meta泄露的LLaMA，创建了一个完全不受限制的「BasedGPT」聊天机器人。Discord上的这个聊天机器人经常会做出极端且愚蠢的回答。没有ChatGPT那么好，这是肯定的，但话说回来，它使用的计算能力少了1000倍。[参考](https://www.toutiao.com/article/7209928157732864552)


#### LLaMA 模型结构

LLaMA模型结构与GPT相同，采用了causal decoder-only的transformer模型结构。在模型细节上，做了以下几点改动：
- layer normalization：为了提升训练的稳定性，没有使用传统的post layer norm，而是使用了pre layer Norm。具体地，去除了layer normalization中的偏置项，采用了RMS Norm（即均方根 Norm）。
- 激活函数：没有采用ReLU激活函数，而是采用了SwiGLU激活函数。FFN通常有两个权重矩阵，先将向量从维度d升维到中间维度4d，再从4d降维到d。而使用SwiGLU激活函数的FFN增加了一个权重矩阵，共有三个权重矩阵，为了保持参数量一致，中间维度采用了 
2/3*4d ，而不是4d。
- 位置编码：去除了绝对位置编码，采用了旋转位置编码RoPE。

LLaMA的训练目标是语言模型，即根据已有的上文去预测下一个词。

关于tokenizer，LLaMA的训练语料以英文为主，使用了Sentence Piece作为tokenizer，词表大小只有32000。词表里的中文token很少，只有几百个，LLaMA tokenizer对中文分词的编码效率比较低。

Llama 2在预训练设置和模型架构上和一代模型非常相似
- ![](https://pic3.zhimg.com/80/v2-a26895320d7f67d296a320ae177c1816_1440w.webp)

Llama系列模型都使用了**自回归Transformer**架构，即 Transformer's decoder-only架构。两代模型的一致性体现在：
- **预归一化**（Pre-normalization）：对每一个transformer的子层输入都进行归一化，使用RMSNorm归一化函数
- `SwiGLU`激活函数：在前馈神经网络（FFN）使用SwiGLU 激活函数替换了Transformer中的 ReLU 激活函数来提升性能
- **旋转嵌入编码**（Rotary Positional Embeddings，`RoPE`）：RoPE可以兼顾相对位置和绝对位置的信息以提高模型的泛化能力

【2024-1-24】[Llama.cpp 代码浅析（一）：并行机制与KVCache](https://zhuanlan.zhihu.com/p/670515231?utm_psn=1733263938836525056)

Transformer vs Llama
- ![](https://pic3.zhimg.com/80/v2-8ec08fb6dedacf27a71a71e11a11d6c6_1440w.webp)
- ![](https://pic3.zhimg.com/80/v2-6eddbabe0877eb43b2e46d1e7367bf42_1440w.webp)


【2024-3-22】Meta的LLaMA 依旧采用Transformers架构，并做了如下改动：
- 为了提高训练稳定性，对每个子层做输入前置归一化，归一化函数为RMSNorm（受GPT-3启发）
- 为了提升性能，SwiGLU激活函数替换ReLU激活函数（受PaLM启发）从绝对位置嵌入，改为旋转嵌入（受GPT-neo启发）使用causal multi-head attention的一个高效实现来减少内存占用和运行时间

#### LLaMA 下载

【2023-4-18】下载出错
- issue: [Tokenizer class LLaMATokenizer does not exist or is not currently imported](https://github.com/huggingface/transformers/issues/22222)


#### LLaMA 汉化

【2023-5】基于llama模型框架从零训练一个中文大模型
- [chinese_llama](https://github.com/yuanzhoulvpi2017/zero_nlp/tree/main/chinese_llama)

背景和想法
- **llama**：facebook泄漏出来的llama模型，不能商用, 也没中文token，虽然很多国内大牛已经对其进行扩充了。
- **chatglm-6b**： chatglm-6b **模型权重**也不能商用，但是对中文的支持能力很好

想法：
- 把 chatglm-6b 的 tokenizer 直接拿过来，嫁接到任意一个开源的大模型框架上;
- 基于这个大模型框架，从零训练一个中文模型。
- 原始的模型权重不能商用，自己训练一个模型权重，肯定没啥问题。

要点
- **数据**：基于 belle给到的数据，整理了一份491万条的数据文件，间接的提供了数据处理模版和基础的通用数据。
- **模型大小**：应对不同的硬件资源，可以手动对模型的大小进行调整（从1b到7b再到130b都可以， 硬件资源越丰富，模型就可以设置的越大）
- **训练**：为了让模型可以在多个消费级显卡上训练、推理。（毕竟大部分人，都没钱买A100这样的显卡，大家都是使用3090这种消费级的小显卡）对原来的llama模型做了改进：
  - 训练时，支持模型并行；
  - 推理时，支持多卡串联；


### LLaMA 进化图

【2023-3-27】Aplaca进化路线图

<div class="mermaid">
    flowchart TD
    %% 节点颜色
    classDef red fill:#f02;
    classDef green fill:#5CF77B;
    classDef blue fill:#6BE0F7;
    classDef orange fill:#F7CF6B;
    classDef grass fill:#C8D64B;
    %%节点关系定义
    G(GPT-3)-->|2023-2-24,META推出超越GPT-3的半开源模型\n提效:7b-65b,单GPU运行,1/10参数|L(LLaMA):::green
    S(Self-Instruct\n自监督指令集方案):::blue
    L-->|2023-3-14,斯坦福\n7b的LLaMA+52k微调,self-instruct\nAlpaca 7b达到davinci-003效果\n消费级GPU运行,如树莓派|A(Stanford-Alpaca):::green
    S-->|2022-12,华盛顿大学\nYizhong Wang\ngpt-3模型生成指令+指令回答|A
    LR(LoRA\n低秩适配):::blue -->|减少训练参数\n速度快,内存消耗少\n媲美 Standford Alpaca|AR(Alpaca-LoRA):::green
    L -->|2023-3-21,7b的LLaMA\n斯坦福 Eric J. Wang|AR
    A -->|2023-3-17,贝壳\n7b,bloom,200w中文语料| AB(BELLE):::grass
    A -->|2023-3-26,华中师范\n7b,3k中文保险语料,4h| AL(Luotuo骆驼):::grass
    L -->|2023-3-29,深圳大学\n7b,中文语料| AC(ChatLLaMA):::grass
    LR --> AL
    AR -->|2023-3-23,突破8G GPU 显存限制,直接用CPU运行\n1. LLaMA cpp项目\n2. Alpaca-LoRA权重量化| AC(Alpaca-cpp):::green
    GLM(ChatGLM)-->|2023-4-25, ChatGLM 6b, GLM架构\n仅限第一阶段SFT| GLM1(ChatGLM-Tuning):::grass
    A -->|数据集| GLM1
    LR --> GLM1

    L -->|2023-3-31,伯克利\n开源FastChat达到ChatGPT 90%| V(Vicuna小羊驼):::green
    O(OPT):::blue -.->|OPT 1.3b模型| V
</div>


【2023-7-5】人民大学总结的LLaMA进化图
- 论文: "[A Survey of Large Language Models](https://arxiv.org/abs/2303.18223)", github: [LLMSurvey](https://github.com/RUCAIBox/LLMSurvey/tree/main)
- ![llama](https://github.com/RUCAIBox/LLMSurvey/blob/main/assets/llama-0628-final.png?raw=true)

### LLaMA 扩展

#### LLaMA 分词问题

目前开源大模型中，LLaMA无疑是最闪亮的星。但是，与 ChatGLM-6B 和 Bloom 原生支持中文不同。
- LLaMA 原生仅支持 Latin 或 Cyrillic 语系，对于**中文**支持不是特别理想。
- 原版LLaMA模型的词表大小是**32K**，而多语言模型（如：XLM-R、Bloom）的词表大小约为**250K**。
- 以中文为例，LLaMA词表中的中文token比较少（只有几百个）。这将导致了两个问题：
  - LLaMA 原生tokenizer词表中仅包含少量中文字符，在对中文字进行tokenzation时，一个中文汉字往往被切分成多个token（2-3个Token才能组合成一个汉字），显著降低编解码的效率。
  - 预训练中没有出现过或者出现得很少的语言学习得不充分。

#### LLaMA 要不要扩充词表

LLaMA需不需要扩充词表？如果不扩充词表，中文效果会不会比较差？
- LLaMA 中文效果怎么样？
  - Vicuna官方的报告，经过 Instruction Turing 的 Vicuna-13B已经有非常好的中文能力。
- LLaMA 需不需要扩充词表？
  - 根据 Chinese-LLaMA-Alpaca 和 BELLE 报告，扩充中文词表可以提升**中文编解码效率以及模型性能**。
  - 但是扩词表相当于**从头初始化**训练这些参数。如果想达到比较好的性能，需要<span color:red>比较大的算力和数据量</span>。
  - 同时，Chinese-LLaMA-Alpaca 也指出在进行第一阶段预训练（冻结transformer参数，仅训练embedding，在尽量不干扰原模型的情况下适配新增的中文词向量）时，模型**收敛速度较慢**。
  - 如果没有充裕的时间和计算资源，建议**跳过**该阶段。
- 因此，虽然扩词表看起来很诱人，但是实际操作起来，还是很有难度的。
- 如果既想要中文词表又没有很大的算力，建议直接使用 选用扩充后的模型作为base
  - 如： ChatGLM-6B 或 BELLE 和 Chinese-LLaMA-Alpaca。

#### LLaMA 中文字符扩充

为了解决这些问题，需要进行中文词表扩展。比如：
- 在中文语料库上训练一个中文tokenizer模型，然后将中文 tokenizer 与 LLaMA 原生的 tokenizer 进行合并，通过组合词汇表，最终获得一个合并后的 tokenizer 模型。

而国内 Chinese-LLaMA-Alpaca 开源项目详细说明了词表扩展、模型预训练和模型指令精调的整个过程。

Chinese-LLaMA-Alpaca是在通用中文语料上训练了基于 sentencepiece 的20K中文词表并与原版LLaMA模型的32K词表进行合并，排除重复的token后，得到的最终中文LLaMA词表大小为49953。

注意：
- 模型精调（fine-tune）阶段，Alpaca 比 LLaMA 多一个 pad token，所以中文Alpaca的词表大小为49954。
- 后续将 LoRA 权重合并回基础模型时需要注意中文LLaMA和中文Alpaca词表不一致的问题。

合并**中文扩充词表**，并与原版LLaMA模型的**32K词表**，直接使用官方训练好的词表chinese_sp.model。
- 当然也可以基于特有领域的语料训练专属的词表，具体可参考之前的文章：大模型词表扩充必备工具SentencePiece。

详见：[中文LLaMA&Alpaca大语言模型词表扩充+预训练+指令精调](https://mp.weixin.qq.com/s/-Zei1OsM45BHc41WNGmZQQ)


#### 端侧LLaMA

端侧小模型见站内[专题](llm_end)

### 斯坦福 Aplaca（基于LLaMA）

Meta开源了LLaMA系列模型，包含了参数量为7B/13B/33B/65B的不同模型，然而，原模型的效果较差（如生成的结果文不对题、以及无法自然地结束生成等）。

斯坦福的 Alpaca 模型基于 LLaMA-7B 和指令微调，仅使用约 5 万条训练数据，就能达到类似 GPT-3.5 的效果。

【2023-3-14】[Alpaca: A Strong Open-Source Instruction-Following Model](https://crfm.stanford.edu/2023/03/13/alpaca.html) 斯坦福微调了 7B LLaMA 模型，只用了 52K 的数据，达到了和达芬奇003类似的效果，并且可以跑在消费级设备上，比如树莓派。[参考](https://www.toutiao.com/article/7210260080690889275)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/f86ae0e26c1a4f36b41850ef19f059e3~noop.image?_iz=58558&from=article.pc_detail&x-expires=1679383800&x-signature=RYAjEKgrdJXvzVLRLPzQSsbQw2E%3D)
- [Web Demo](https://crfm.stanford.edu/alpaca/), [GitHub](https://github.com/tatsu-lab/stanford_alpaca)
- We emphasize that Alpaca is intended only for academic research and any commercial use is prohibited. 
- ![](https://crfm.stanford.edu/static/img/posts/2023-03-13-alpaca/alpaca_main.jpg)

- We performed a **blind pairwise comparison** between `text-davinci-003` and `Alpaca 7B`, and we found that these two models have very similar performance: `Alpaca` wins 90 versus 89 comparisons against `text-davinci-003`.
- ![](https://crfm.stanford.edu/static/img/posts/2023-03-13-alpaca/alpaca_right_email.png)


#### self-instruct

[self-instruct](https://github.com/yizhongw/self-instruct): [Self-Instruct: Aligning LM with Self Generated Instructions](https://arxiv.org/abs/2212.10560)
- 斯坦福团队微调LLaMA的方法，来自华盛顿大学Yizhong Wang等去年底提出的Self-Instruct, 一个半自动的过程，利用模型本身的指令信号对预训练的LM进行指令调整。
- ![](https://github.com/yizhongw/self-instruct/raw/main/docs/pipeline.JPG)
- 175个人工种子集，覆盖二分类、生成任务，然后，调用gpt-3模型生成指令、指令回答
- 以175个问题作为种子任务，让AI自己从中组合出新的问题以及生成配套答案实例，人工过滤掉低质量的，再把新任务添加到任务池里。所有这些任务，之后可以采用InstructGPT的方法让AI学会如何遵循人类指令。
- 斯坦福版Alpaca花了不到500美元使用OpenAI API生成了5.2万个这样的示例搞出来的。
- code : [generate_instruction.py](https://github.com/tatsu-lab/stanford_alpaca/blob/main/generate_instruction.py)
- 解读：[面向大模型微调的instruction指令自动化生成技术：SELF-INSTRUCT指令自动化生成框架工作介绍](https://mp.weixin.qq.com/s/Lo1f1knFFQWdHNLTNyFKDQ)

【2023-3-23】alpaca中文指令微调数据集 [alpaca-chinese-dataset](https://github.com/carbonz0/alpaca-chinese-dataset)


#### 贝壳开源

【2023-3-17】贝壳开源的 7b模型 [BELLE](https://github.com/LianjiaTech/BELLE), [huggingface](https://huggingface.co/jay68/BELLE-7B-0.2M)，限sft, rm、rlhf还没加，size太小调不出来，只能做特定任务，指令泛化理解都搞不定; Stanford方案复现中文版
- [Exploring ChatGPT's Ability to Rank Content: A Preliminary Study on Consistency with Human Preferences](https://arxiv.org/abs/2303.07610)
- ChatGPT's zero-shot ranking capability could be used to reduce annotation pressure in a number of ranking tasks

#### Alpaca 复现

- 【2023-3-19】基于LLaMA用翻译语料训练中文Alpaca模型 - [李煜东的文章 - 知乎](https://zhuanlan.zhihu.com/p/614923816)
- 【2023-3-31】[从0到1复现斯坦福羊驼](https://zhuanlan.zhihu.com/p/618321077)（Standford Alpaca 7B），8 卡 A800 80GB GPUs 。。。

#### Alpaca-LoRA

[alpaca-lora](https://github.com/tloen/alpaca-lora)

```sh
git clone https://github.com/tloen/alpaca-lora.git
pip install -r requirements.txt
```

训练
- 模型默认输出在“lora-alpaca”文件夹下
- 可设置超参

```sh

python finetune.py \ # 默认参数
# 自定义模型、数据、目录
    --base_model 'decapoda-research/llama-7b-hf' \
    --data_path 'yahma/alpaca-cleaned' \
    --output_dir './lora-alpaca' # 模型保存目录
# 或者更改超参信息
    --batch_size 128 \
    --micro_batch_size 4 \
    --num_epochs 3 \
    --learning_rate 1e-4 \
    --cutoff_len 512 \
    --val_set_size 2000 \
    --lora_r 8 \
    --lora_alpha 16 \
    --lora_dropout 0.05 \
    --lora_target_modules '[q_proj,v_proj]' \
    --train_on_inputs \
    --group_by_length
```

推理

```sh
python generate.py \
    --load_8bit \
    --base_model 'decapoda-research/llama-7b-hf' \
    --lora_weights 'tloen/alpaca-lora-7b'
# 启动推理服务（gradio）
python inference.py
# 使用自己的模型
LORA_WEIGHTS = "tloen/alpaca-lora-7b"
```


##### Alpaca-LoRA 本地部署

【2023-3-23】Alpaca-Lora (羊驼-Lora): [轻量级 ChatGPT 的开源实现](https://zhuanlan.zhihu.com/p/615646636)（对标 Standford Alpaca）
- ChatGPT 轻量级的开源版本，它使用 Lora (Low-rank Adaptation) 技术在 Meta 的 LLaMA 7B 模型上微调，只需要训练很小一部分参数就可以获得媲美 Standford Alpaca 模型的效果

斯坦福的研究者 —— Eric J. Wang 使用 `LoRA`（low-rank adaptation）**低秩适配** 技术复现了 Alpaca 的结果。具体来说，Eric J. Wang 使用一块 RTX 4090 显卡，只用 5 个小时就训练了一个和 Alpaca 水平相当的模型，将这类模型对算力的需求降到了消费级。

##### LoRA 低秩适配

![](http://inews.gtimg.com/newsapp_bt/0/15765425454/641)

LoRA 是在原始 PLM 旁边增加一个旁路，做一个降维再升维的操作，来模拟所谓的 intrinsic rank。训练的时候固定 PLM 的参数，只训练降维矩阵 A 与升维矩阵 B。而模型的输入输出维度不变，输出时将 BA 与 PLM 的参数叠加。用随机高斯分布初始化 A，用 0 矩阵初始化 B，保证训练的开始此旁路矩阵依然是 0 矩阵（引自：[loara](https://finisky.github.io/lora/)）。
- Eric J. Wang 发布的 Alpaca-LoRA 项目。[项目地址](https://github.com/tloen/alpaca-lora)
- LoRA 的最大优势是速度更快，使用的内存更少，因此可以在消费级硬件上运行。

【2023-6-1】qlora加持下，merlin单机可以跑33-65b模型，40G空间

##### Alpaca-LoRA 中文版 Luotuo

【2023-3-26】华中师范大学等机构的三位个人开发者开源的中文语言模型`骆驼` (Luotuo)，基于 LLaMA、Stanford Alpaca、Alpaca LoRA、Japanese-Alpaca-LoRA 等完成，**单卡**就能完成训练部署。
- 骆驼:A Chinese finetuned instruction LLaMA. Developed by 陈启源 @ 华中师范大学 & 李鲁鲁 @ 商汤科技 & 冷子昂 @ 商汤科技
- 参考：[训练个中文版ChatGPT没那么难：不用A100，开源Alpaca-LoRA＋RTX 4090就能搞定](https://view.inews.qq.com/a/20230326A02QO500)
- 之所以将模型名字命名为骆驼，是因为 LLaMA（大羊驼）和 alpaca（羊驼）都属于偶蹄目 - 骆驼科。
- 训练中文版 Alpaca LoRa 用了 3K 多条中文问答保险语料，实现过程使用了 LoRa 方法，并微调 Alpaca 7B 模型，耗时 240 分钟，最终 Loss 0.87 。
- [项目地址](https://github.com/LC1332/Chinese-alpaca-lora), 释放了两个模型 luotuo-lora-7b-0.1、luotuo-lora-7b-0.3，还有一个模型在计划中

#### Alpaca-cpp 本地部署

[Alpaca-cpp（羊驼-cpp）: 可以本地运行的 Alpaca 大语言模型](https://zhuanlan.zhihu.com/p/616267309)

从 `Stanford-Alpaca` 到 `Alpaca-Lora`，再到本篇要介绍的 `Alpaca-cpp`，都是为了寻找一种在资源约束下，能本地高效便捷运行大语言模型的方法。
- （1）`Stanford-Alpaca`: 包含数据生成、模型训练等源代码，但微调的LLaMA模型参数还未放出
- （2）`Alpaca-Lora`: 使用 Lora 技术微调出一个对标 Stanford-Alpaca 的模型，开源了 LLaMA+Lora 模型参数。本地CPU运行成功，但速度较慢
- （3）`Alpaca-cpp`: 借助 llama-cpp 提供的强大工具，对 Alpaca-Lora 模型参数量化（int4或int8），本地CPU流畅运行

Alpaca-cpp
- 突破了 8G GPU 显存的限制，能直接使用 CPU 运行，那后续还可以尝试 30B 甚至更大参数的大语言模型
- Alpaca-cpp 是基于 llama-cpp 这个项目，代码基本完全相同，差别在 Alpaca-cpp 对 Alpaca-Lora 的权重进行了量化等预处理，然后用 llama-cpp 提供的功能去加载量化后的权重。

本地电脑 CPU 流畅运行大语言模型 Alpaca/LLaMA 的 C++/C 框架。相关资源如下：
- [alpaca.cpp](https://github.com/antimatter15/alpaca.cpp)
- [ggml-alpaca-7b-q4.bin](https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/blob/main/ggml-alpaca-7b-q4.bin) 量化后的Alpaca模型， [huggingface地址](https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/tree/main)
- [llama.cpp](https://github.com/ggerganov/ll) （alpaca.cpp 是 fork 本项目，代码基本一致）

安装方法

```sh
# 下载 alpaca.cpp 项目
git clone https://github.com/antimatter15/alpaca.cpp
# 进入 alpaca.cpp 后，到 https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/blob/main/ggml-alpaca-7b-q4.bin 下载量化后的模型 ggml-alpaca-7b-q4.bin，然后使用
wget https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/blob/main/ggml-alpaca-7b-q4.bin
# 编译
make chat
# 运行
./chat
```

#### ChatLLaMA

【2023-3-29】[ChatLLaMA：用指令微调训练中文对话大模型](https://zhuanlan.zhihu.com/p/616748134)

以非中文的预训练模型为基础，使用少量数据和计算量“撬动”模型的语言能力转向中文，以较低的成本实现中文预训练LLM。
- 假设: 用中英文平行语料微调模型，能够对齐模型中英文在高维空间的表示，从而将模型在英文上的强大语言能力迁移到中文。
- 模型及GitHub地址：[Chinese-ChatLLaMA](https://github.com/ydli-ai/Chinese-ChatLLaMA)

基于[TencentPretrain](https://github.com/Tencent/TencentPretrain)预训练框架，我们进行了以下实验：
1.  基于LLaMA-7B权重在中文数据上进行无监督增量预训练。使用的数据包含各种[中文百科、社区互动、翻译语料](https://github.com/brightmart/nlp_chinese_corpus)和[科学文献](https://github.com/ydli-ai/CSL)数据，在32 * A100 40G GPU 上以 2e-4 学习率，3072 batch_size，训练一万步，得到LLaMA-7B-zh。
2.  在中文预训练权重LLaMA-7B-zh上，使用已有的指令数据集的集合进行指令微调，数据集以及预处理代码整理在[Chinese-instruction-dataset](https://github.com/ydli-ai/Chinese-instruction-dataset)。学习率为2e-5，训练2000步，最终得到Chat-LLaMA。
 
训练LLaMA的详细方法可以参考[上一篇文章](https://zhuanlan.zhihu.com/p/612752963)，流程如下图所示：
- ![](https://pic3.zhimg.com/80/v2-667a131609b04ef4a1fa8d84e980252e_1440w.webp)

#### GPT4All

【2023-4-3】[GPT4All：一个能在笔记本运行的ChatGPT平替](https://mp.weixin.qq.com/s/J6DWk9Ac8lRYf2hc1g0A0Q)

GPT4All 是一个使用包括代码、故事和对话在内的大量干净助手数据训练的聊天机器人。该项目提供演示、数据和代码，用于训练一个基于LLaMA 7B的助手式大型语言模型，包含约800k个基于GPT-3.5-Turbo生成的对话。M1 Mac、Windows 等环境都能运行。
- [项目地址](https://github.com/nomic-ai/gpt4all)
- [技术报告](https://s3.amazonaws.com/static.nomic.ai/gpt4all/2023_GPT4All_Technical_Report.pdf)

#### Alpaca-CoT

【2023-4-12】将CoT数据扩展到Alpaca以提高其推理能力

[Alpaca-CoT数据集](https://huggingface.co/datasets/QingyiSi/Alpaca-CoT/tree/main)
- The relative size of collected datasets can be shown by this graph:
- ![](https://github.com/PhoebusSi/Alpaca-CoT/raw/main/figures/show.png)


#### 白泽 -- 医疗

白泽 使用 LoRA 训练的开源聊天模型
- 改进了开源大型语言模型 LLaMA，通过使用新生成的聊天语料库对 LLaMA 进行微调
- 该模型在单个 GPU 上运行，使其可供更广泛的研究人员使用。

白泽目前包括四种英语模型：白泽 -7B、13B 和 30B（通用对话模型），以及一个垂直领域的白泽 - **医疗模型**，供研究 / 非商业用途使用，并计划在未来发布中文的白泽模型。

白泽的数据处理、训练模型、Demo 等全部代码已经开源。

#### OpenLLaMA -- 可商用

【2023-5-3】[OpenLLaMA](https://github.com/openlm-research/open_llama) —— LLaMA 大语言模型的开源复现版本

OpenLLaMA 是 Meta AI 的 LLaMA 大语言模型的开源复现版本，采用宽松许可证，可免费商用。
- 直接替换Meta公司的LLaMA模型。
- 型号：3、7和13b
- 这个模型已经在RedPajama数据集上进行了1万亿次的训练。

仓库包含经过训练的 2000 亿标记的 7B OpenLLaMA 模型的公共预览版，并提供了预训练的 OpenLLaMA 模型的 PyTorch 和 Jax 权重，以及评估结果和与原始 LLaMA 模型的比较。

加载权重

```py
import torch
from transformers import LlamaTokenizer, LlamaForCausalLM

model_path = 'openlm-research/open_llama_3b'
# model_path = 'openlm-research/open_llama_7b'
# model_path = 'openlm-research/open_llama_13b'

tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(
    model_path, torch_dtype=torch.float16, device_map='auto',
)

prompt = 'Q: What is the largest animal?\nA:'
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

generation_output = model.generate(
    input_ids=input_ids, max_new_tokens=32
)
print(tokenizer.decode(generation_output[0]))
```

#### LIMA -- META

【2023-5-23】[没有RLHF，一样媲美GPT-4、Bard，Meta发布650亿参数语言模型LIMA](https://mp.weixin.qq.com/s/Oze93Brun-AQUBI5Tt1b6w)
- [paper](https://arxiv.org/abs/2305.11206)

使用 RLHF 方法，大型语言模型可与人类偏好保持对齐，遵循人类意图，最小化无益、失真或偏见的输出。但 RLHF 方法依赖于大量的人工标注和评估，因此成本非常高昂。最近，来自 Meta AI 等机构的研究者在一项研究中指出：在对齐方面，少即是多。

在 65B 参数的 LLaMa 模型（该模型称为 LIMA）在 1000 个精选样本上进行有监督学习，在完全没使用 RLHF 方法的情况下，LIMA 表现出非常强大的性能，并且能够很好地泛化到训练数据以外的任务上。在人类评估结果中，LIMA 甚至可与 GPT-4、Bard、DaVinci003 相媲美。图灵奖得主 Yann LeCun 也转推称赞这项研究。

对照试验中
- LIMA 在 43% 的病例中疗效都与 GPT-4 媲美甚至更好；
- 相比于 Bard，占比能够达到 58%；
- 与使用人类反馈训练的 DaVinci003 对比了，这个数字高达 65%。

在 1000 个精心策划的例子上对一个强大的预训练语言模型进行微调，可以在广泛的 prompt 中产生显著的、有竞争力的结果。然而，这种方法也有局限性：
- 首先，构建这样的样本所付出的脑力劳动是巨大的，而且很难扩大规模。
- 其次，LIMA 并不像产品级模型那样鲁棒，虽然 LIMA 通常会产生良好的反应，但在解码过程中一个不幸运的样本或一个敌对的 prompt 往往会导致一个弱的反应。

尽管如此，这项工作中提出的证据表明，用简单的方法来解决复杂的对齐问题是有潜力的。

#### WizardLM

【2023-4-24】WizardLM —— 基于 LLaMA 的微调大语言模型
- 微软华人团队发布的WizardLM
- 【2023-6-15】开源榜单第一，次于 GPT-4、Claude和ChatGPT

WizardLM 是一个经过微调的 7B LLaMA 模型。它通过大量具有不同难度的指令跟随对话进行微调。这个模型的新颖之处在于使用了 LLM 来自动生成训练数据。

WizardLM 模型使用一种名为 `Evol-Instruct`（使用 LLM 代人类自主**批**生成各种难度等级和技术范围的开放指令，以提高 LLM 能力的新方法）的新方法，通过 70k 个计算机生成的指令进行训练，该方法生成具有不同难度级别的指令。
- [WizardLM: Empowering Large Language Models to Follow Complex Instructions](https://arxiv.org/abs/2304.12244)
- [代码及数据](https://github.com/nlpxucan/WizardLM)

新的70亿参数模型 WizardLM-7b，训练机制非常特殊，与以往的人工输入指令训练有所不同，自动化批量生成各种难度级别和技能范围的开放域指令

### Vicuna 小羊驼 -- 92% 的 ChatGPT

【2023-3-31】[Vicuna: An Open-Source Chatbot Impressing GPT-4 with 90%* ChatGPT Quality](https://vicuna.lmsys.org/)，伯克利中国人开发
- github代码：[FastChat](https://github.com/lm-sys/FastChat), [demo](https://chat.lmsys.org/)
- ![](https://github.com/lm-sys/FastChat/raw/main/assets/demo-narrow.gif)

安装

```sh
git clone https://github.com/lm-sys/FastChat.git
cd FastChat
pip3 install -e .

# Install the latest main branch of huggingface/transformers
pip3 install git+https://github.com/huggingface/transformers
```

效果评测

prompt
>- 写个朋友圈二手房营销文案，要求不超过100字，突出房源重点，降价/急售/上新，三个主题选一个，带emoji表情，房源信息如下：育新东里二里，靠近西三旗商圈，89平米，海淀六小强学区，满五年，2000年的房子，户型东西向，有独立卫生间
>- 写3个朋友圈二手房营销文案，要求不超过100字，突出房源重点，降价/急售/上新，带emoji表情，房源信息如下：育新东里二里，靠近西三旗商圈，89平米，海淀六小强学区，满五年，2000年的房子，户型东西向，有独立卫生间

Vicuna
>"🚨 急售！！🏠 育新东里二里，靠近西三旗商圈，89平米，海淀六小强学区，满五年，2000年的房子，户型东西向，有独立卫生间，价格降低，快来看看吧！！"

chatgpt
>- 急售！育新东里二里房源上新啦🚨！89平米，满五年，海淀六小强学区房，2000年房龄，东西向户型，独立卫生间🚪。靠近西三旗商圈，购物、餐饮、娱乐方便🍽️。价格超级优惠💰，快来看看吧！👀
>- 降价啦！育新东里二里房源急售🏠！89平米，满五年，海淀六小强学区房🎓，2000年房龄，东西向户型，独立卫生间🚽。靠近西三旗商圈，购物、餐饮、娱乐方便🛍️。价格大幅降低💰，机会难得👍，赶紧联系我看房吧！📞

prompt
> 写3个朋友圈二手房营销文案，要求不超过100字，突出房源重点，降价/急售/上新，带emoji表情，房源信息如下：育新东里二里，靠近西三旗商圈，89平米，海淀六小强学区，满五年，2000年的房子，户型东西向，有独立卫生间

chatgpt
>- 上新！🏠 育新东里二里二手房，89平米，满五年，海淀六小强学区，东西向户型，独立卫生间🚪。紧邻西三旗商圈🛍️，购物、餐饮、娱乐一应俱全🎉。2000年的房子，价格实惠💰，速度联系我吧！📱
>- 降价急售！🚨 育新东里二里二手房，89平米，满五年，海淀六小强学区，东西向户型，独立卫生间🚪。靠近西三旗商圈🏢，生活便利🚇。2000年的房子，价格大降，千万别错过！👀
>- 限时优惠！💰 育新东里二里二手房，89平米，满五年，海淀六小强学区，东西向户型，独立卫生间🚪。紧邻西三旗商圈🛍️，购物、餐饮、娱乐应有尽有🎉。2000年的房子，价格优惠，抓紧时间看房吧！👀



### Dolly（真开源）

【2023-4-12】[世界首款真开源类ChatGPT大模型Dolly 2.0](https://www.toutiao.com/article/7221415818079355426)，可随意修改商用; 基于[Eleuther.AI](https://www.eleuther.ai/)的 [Pythia](https://huggingface.co/EleutherAI/pythia-12b)
- [项目链接](https://huggingface.co/databricks/dolly-v2-12b)
- [数据集](https://github.com/databrickslabs/dolly/tree/master/data)

4 月 12 日，Databricks 发布了 Dolly 2.0，这是两周前发布的类 ChatGPT 人类交互性（指令遵循）大语言模型（LLM）的又一个新版本。
- Dolly 2.0 是业内第一个**开源**、**遵循指令**的 LLM，它在透明且免费提供的数据集上进行了微调，该数据集也是开源的，可用于商业目的。这意味着 Dolly 2.0 可用于构建商业应用程序，无需支付 API 访问费用或与第三方共享数据。


### LaMini-LM 蒸馏小模型

【2023-5-11】LaMini-LM 蒸馏小模型，开源，将模型大小减少10倍，且保证性能
- [LaMini-LM: A Diverse Herd of Distilled Models from Large-Scale Instructions](https://arxiv.org/pdf/2304.14402v1.pdf)
- 1B小型语言模型LaMini，支持百万token输入的RMT
- youtube视频：[LaMini-LM - Mini Models Maxi Data!](https://www.youtube.com/watch?v=TeJrG3juAL4)

两个部分 [详情](https://zhuanlan.zhihu.com/p/626518078)
- 第一进行数据生成
  - 各种先前数据集的指令，例如：self-instruct、P3、FLAN和Alpaca。
  - 此外，使用 ChatGPT (gpt-3.5-turbo) 来生成补充说明，强调在提示中遵守现有的人工编写说明的多样性。-- 又叫：示例引导指令生成
  - 还引入了主题引导指令生成方法，进一步增加生成文本的多样性
  - 接着，用 gpt-3.5-turbo 为每条指令生成响应
  - 两种生成指令的策略，分别为`示例引导`和`主题引导`
- 第二就是利用数据集对模型进行微调。
  - 生成数据集后，作者微调了几个具有不同大小（从 61M 到 1.5B）和架构（encoder-decoder 和 decoder-only）的较小语言模型。

整体方法如下所示：
- ![](https://pic1.zhimg.com/80/v2-ac4334cb3ab218398849ceb79c866f2c_1440w.webp)

### Linly-ChatFlow（中文）

Chinese-LLaMA基础模型，深圳大学发布
-  huggingface demo [Linly-ChatFlow](https://huggingface.co/spaces/Linly-AI/Linly-ChatFlow)
- 【2023-3-28】 开放基于 LLaMA 的中文对话模型 Linly-ChatFlow-7B 
- 【2023-4-27】 正式发布 Linly-ChatFlow-13B 对话模型、Linly-Chinese-LLaMA-33B 中文基础模型

公开可用的模型有：
- Linly-Chinese-LLaMA：中文基础模型，基于 LLaMA 在高质量中文语料上增量训练强化中文语言能力，现已开放 7B、13B 和 33B 量级，65B 正在训练中。
- Linly-ChatFlow：中文对话模型，在 400 万指令数据集合上对中文基础模型指令精调，现已开放 7B、13B 对话模型。
- Linly-ChatFlow-int4 ：ChatFlow 4-bit 量化版本，用于在 CPU 上部署模型推理。

中文对话模型 [Linly-ChatFlow](https://github.com/CVI-SZU/Linly)
- 模型基于 TencentPretrain 预训练框架实现，在 32 * A100 GPU 上全参数训练（Full-tuning）
- 将陆续开放 7B、13B、33B、65B 规模的中文模型权重。 
- 中文基础模型以 `LLaMA` 为底座，利用中文和中英**平行**增量预训练，将英文上强大语言能力迁移到中文上。
- 项目汇总了目前公开的多语言指令数据，对中文模型进行了大规模指令跟随训练，实现了 Linly-ChatFlow 对话模型。

项目特点
- 通过 Full-tuning （全参数训练）获得中文LLaMA模型，提供 TencentPretrain 与 HuggingFace 版本
- 汇总中文开源社区指令数据，提供目前最大的中文 LLaMA 模型
- 模型细节公开可复现，提供数据准备、模型训练和模型评估完整流程代码
- 多种量化方案，支持 CUDA 和边缘设备部署推理
- 基于公开数据从头训练 Linly-OpenLLaMA ，针对中文优化字词结合tokenizer
- ![](https://github.com/CVI-SZU/Linly/raw/main/assets/chatflow.jpg)

覆盖多种功能，包含测试案例
- 生成示例
- 常识推理
- 逻辑推理
- 知识问答
- 语义理解
- 数值计算
- 诗文写作
- 文本翻译
- 代码

### 原驼（Guanaco）

【2023-5-26】[开源「原驼」爆火，iPhone都能微调大模型了，得分逼近ChatGPT](https://mp.weixin.qq.com/s/RakazI25dMJz0JUkdtbr0w)
- 羊驼家族的又一重磅成员——华盛顿大学`原驼`（Guanaco）。
- 自动测试分数达到ChatGPT的99.3%，人类难以分辨
- 背后的新方法QLoRA([站内专题](gpu#lora-%E4%BD%8E%E7%A7%A9%E9%80%82%E9%85%8D))把微调大模型的显存需求从>780GB降低到<48GB。HuggingFace第一时间整合上线了相关代码
- **大模型小型化**的又一里程碑

(1) 自动评估
- 由大模型天花板GPT-4当裁判，对不同模型的回答进行打分
- 以ChatGPT（GPT3.5）的成绩作为100%。
- 最终原驼650亿版得分达到ChatGPT的99.3%
- GPT-4自己的得分是114.5%
- 谷歌Bard是94.8%。

(2) 随机匹配
- 采用棋类专业比赛和电子竞技同款的`Elo记分机制`，由GPT-4和人类共同做裁判。
- 原驼650亿和330亿版最终得分超过ChatGPT（GPT3.5）

(3) 人类评估
- 把原驼650亿版的回答和ChatGPT的回答匿名乱序放在一起，人类来盲选哪个最好。
- 研究团队里的人都很难分辨出来，并把测试做成了一个小游戏放在Colab上，开放给大家挑战

原驼的优势
- 不容易被错误信息误导，比如能指出地球从来没有被科学界认为是平的
- 擅长心智理论（Theory of Mind），也就是能推测理解他人的心理状态。
- 但不太擅长数学，以及容易用提示注入攻击把要求保密的信息从它嘴里套出来。

### Llama 2

【2023-7-19】[更强的Llama 2开源，可直接商用：一夜之间，大模型格局变了](https://mp.weixin.qq.com/s/klFWFXCbjGaWZ7HO1KFZag)

Meta 终于发布了 免费可商用版本 Llama 2
- Llama 2 模型系列包含 **70 亿**、**130 亿**和 **700 亿**三种参数变体。此外还训练了 340 亿参数变体，但并没有发布，只在技术报告中提到了。
- 相比于 Llama 1，Llama 2 的训练数据多了 **40%**，上下文长度也翻倍，并采用了分组查询注意力机制。在包括推理、编码、精通性和知识测试等许多外部基准测试中展示出了优越的表现，且支持多个语种。
- 具体来说，Llama 2 预训练模型是在 2 万亿的 token 上训练的，精调 Chat 模型是在 100 万人类标记数据上训练的。
- [论文地址](https://ai.meta.com/research/publications/llama-2-open-foundation-and-fine-tuned-chat-models)
- [项目地址](https://github.com/facebookresearch/llama), [llama demo](https://ai.meta.com/llama/)
- Llama2 [huggingface 地址](https://huggingface.co/blog/llama2)

Llama2是当前全球范围内最强的开源大模型，但其中文能力亟待提升

不足
- Llama 2 语料库仍以**英文**（89.7%）为主，而中文仅占据了其中的 0.13%。这导致 Llama 2 很难完成流畅、有深度的中文对话。
- llama2 对MAU超过7亿以上的公司使用，需要单独特殊申请

#### Llama 2 模型结构

【2023-9-21】[关于Llama 2你需要知道的那些事儿](https://zhuanlan.zhihu.com/p/652043939)

Llama 2在预训练设置和模型架构上和一代模型非常相似
- ![Llama](https://pic3.zhimg.com/80/v2-a26895320d7f67d296a320ae177c1816_1440w.webp)

Llama系列模型都使用了自回归Transformer架构，即 Transformer's decoder-only架构。

两代模型的一致性体现在：
- **预归一化**（Pre-normalization）：对每一个transformer的子层输入都进行归一化，使用 RMSNorm 归一化函数
- **SwiGLU激活函数**：在前馈神经网络（`FFN`）使用SwiGLU 激活函数替换了Transformer中的 ReLU 激活函数来提升性能
- **旋转嵌入编码**（Rotary Positional Embeddings，`RoPE`）：RoPE可以兼顾相对位置和绝对位置的信息以提高模型的泛化能力

#### Llama 2 训练

Llama 2 训练过程也有两个亮点
- 第一，**上下文长度扩大**提升了模型的理解能力；
  - Llama 2的上下文长度比Llama扩大了一倍，从2048个token拓展至4096个token。更长的上下文窗口意味着更多的聊天用例可被采用，进而模型的理解能力得以提升。
- 第二，**分组查询注意力机制**提高了模型的推理速度。
  - Llama 2 30B以上的模型采用了**分组查询**注意力机制（Grouped-Query Attention，GQA）
  - 自回归模型的解码通过缓存序列先前标记的键（K）值（V）对来加速注意力的计算。然而随着Batch Size和上下文窗口的增大，多头注意力模型（Multi-head Attenrion，MHA）的内存成本会随之显著增大。
  - GQA的优势在于其将Query进行分组，组内共享KV，使得K和V的预测可以跨多个头共享，从而显著降低计算和内存需求，提升推理速度 。

#### Llama 2-chat 微调流程

Meta 致力于在偏好数据上训练奖励模型，然后采用强化学习进行优化，从而提高生成的质量。
- SFT + RLHF by RS and PPO

和InstructGPT类似，在Llama 2-chat对话模型微调流程分为：
- 自监督训练后获得Llama 2 **基座**模型
- 监督微调（Supervised fine-tuning，`SFT`）
- 人类反馈强化学习（Reinforcement learning with human feedback，`RLHF`）：拒绝采样 + 近端策略优化

RLHF使用了`拒绝采样`（Rejection Sampling fine-tuning，`RS`）和`近端策略优化`（Proximal Policy Optimization，`PPO`）两个优化算法。
- 拒绝采样原理: 模型输出时采样K个结果，用当前时刻最好的奖励模型打分，选择奖励值最高的一个。
- 在强化学习阶段进行梯度更新，并结合PPO进行RS加PPO的优化处理。
- ![](https://pic1.zhimg.com/80/v2-93ba9ace3b9c8e4d8aee7b907aafd348_1440w.webp)

Meta一共迭代了5个RLHF版本，分别从V1-V5，但仅公布了最新的V5版本。V5版本迭代的步骤下图所示。
- ![](https://pic1.zhimg.com/80/v2-a5df08f1cf7f84e261393da9f90129fc_1440w.webp)

Quality Is All You Need
- Meta使用用户偏好数据训练的两个独立的奖励模型 Helpfulness RM 和 Safty RM，分别对有用性和安全性进行了优化。
- SFT 过程中，Llama 2的官方论文强调了只需少量高质量的SFT偏好数据就能显著提升结果质量（Quality Is All You Need）。
- 此外，这篇论文也是第一篇指出“RLHF从根本上提高了大模型性能的**上限**”的论文

启示
- **奖励模型**不仅是RLHF的关键，也是整个大模型效果的关键；
- **数据质量**又是**奖励模型**的关键

#### Llama 2 中文版

【2023-7-20】开源社区首个能下载、能运行的开源中文 LLaMA2 模型就出现了。
- 该模型名为「Chinese Llama 2 7B」，由国内 AI 初创公司 LinkSoul.Al 推出。
- Chinese-Llama-2-7b 开源内容包括**完全可商用**的中文版 Llama2 模型及中英文 SFT 数据集，输入格式严格遵循 llama-2-chat 格式，兼容适配所有针对原版 llama-2-chat 模型的优化。
- 项目地址：[Chinese-Llama-2-7b](https://github.com/LinkSoul-AI/Chinese-Llama-2-7b), [demo](https://huggingface.co/spaces/LinkSoul/Chinese-Llama-2-7b)
- 中英文灵活切换

【2023-8-4】[国内最大Llama开源社区发布首个预训练中文版Llama2](https://zhuanlan.zhihu.com/p/647575127)
- 7月31日，Llama中文社区 率先完成了国内首个**真正意义**上的中文版`Llama2-13B`大模型，从模型底层实现了Llama2中文能力的大幅优化和提升
  - 不是微调！而是基于200B中文语料预训练！

Llama2的中文化可以采用大致两种路线：
1. 基于已有的**中文指令数据集**，对预训练模型进行**指令微调**，使得基座模型能够对齐中文问答能力。这种路线的优势在于**成本较低**，指令微调数据量小，需要的算力资源少，能够快速实现一个中文Llama的雏形。
  - 但缺点也显而易见，微调只能激发基座模型**已有**的中文能力，但由于Llama2的中文训练数据本身较少，所以能够激发的能力也有限，**治标不治本**，从根本上增强Llama2模型的中文能力还是需要从预训练做起。
2. 基于大规模中文语料进行预训练。这种路线的缺点在于**成本高**！不仅需要大规模高质量的中文数据，也需要大规模的算力资源。
  - 但是优点也显而易见，就是能从模型底层优化中文能力，真正达到治本的效果，从内核为大模型注入强大的中文能力

为了从内核实现一个彻底的中文大模型，选择了第二条路线
- 部分预训练数据数据如下：类型描述网络数据互联网上公开的网络数据，挑选出去重后的高质量中文数据，涉及到百科、书籍、博客、新闻、公告、小说等高质量长文本数据Wikipedia中文Wikipedia的数据悟道中文悟道开源的200G数据ClueClue开放的中文预训练数据，进行清洗后的高质量中文长文本数据竞赛数据集近年来中文自然语言处理多任务竞赛数据集，约150个MNBVCMNBVC 中清洗出来的部分数据集首期 Llama2-Chinese-13B 模型的预训练数据包含 200B token，未来，我们将持续不断地迭代更新 Llama2-Chinese，逐步将预训练数据提升到1T token。

- [Llama中文社区](https://github.com/FlagAlpha/Llama2-Chinese)是国内最领先的开源大模型中文社区，Github在两周内即达到 2.4k star，由清华、交大以及浙大博士团队领衔，汇聚了60+AI领域高级工程师以及各行业2000+顶级人才。

效果, 更多示例见[原文](https://zhuanlan.zhihu.com/p/647575127)
- ![](https://pic4.zhimg.com/80/v2-49a13c49215401ac741c55255acc690b_1440w.webp)


```py
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM
model = AutoGPTQForCausalLM.from_quantized('FlagAlpha/Llama2-Chinese-13b-Chat-4bit', device="cuda:0")
tokenizer = AutoTokenizer.from_pretrained('FlagAlpha/Llama2-Chinese-13b-Chat-4bit',use_fast=False)
input_ids = tokenizer(['<s>Human: 怎么登上火星\n</s><s>Assistant: '], return_tensors="pt",add_special_tokens=False).input_ids.to('cuda')        
generate_input = {
    "input_ids":input_ids,
    "max_new_tokens":512,
    "do_sample":True,
    "top_k":50,
    "top_p":0.95,
    "temperature":0.3,
    "repetition_penalty":1.3,
    "eos_token_id":tokenizer.eos_token_id,
    "bos_token_id":tokenizer.bos_token_id,
    "pad_token_id":tokenizer.pad_token_id
}
generate_ids  = model.generate(**generate_input)
text = tokenizer.decode(generate_ids[0])
print(text)
```





#### Llama 2 多模态

【2023-8-4】[中文版开源Llama 2同时有了语言、多模态大模型，完全可商用](https://mp.weixin.qq.com/s/_TbBKKRhqMv66GGyyW74XQ)
- LinkSoul.AI 团队将目光投向了目前全球尚外于发展初期的**语音文本多模态**大模型和**图文大模型**，并再次率先开源了相关的模型，提供国内开发者免费下载、自由商用。本次开源的两个中文多模态大模型，包括如下：
- 由 LinkSoul.Al 团队牵头，北京智源人工智能研究院、北京大学、零一万物等国内头部顶尖人工智能团队通力合作的第一个支持中英双语、语音到文本的多模态开源对话模型 ([LLaSM](https://github.com/LinkSoul-AI/LLaSM))
- 第一个基于 Llama 2 的支持中英文双语视觉到文本的多模态模型 (`Chinese-LLaVA`) 
- 完全可商用

(1) LinkSoul.AI 开源了可商用的中英文双语**语音-语言**助手 `LLaSM` 以及中英文语音 SFT 数据集 [LLaSM-Audio-Instructions](https://huggingface.co/datasets/LinkSoul/LLaSM-Audio-Instructions)。
- [LLaSM](https://github.com/LinkSoul-AI/LLaSM) 是首个支持中英文语音-文本多模态对话的开源可商用对话模型。
  - 模型、代码和数据[地址](https://huggingface.co/spaces/LinkSoul/LLaSM)
- 相较以往的传统方案，LLaSM 能够通过便捷的语音输入的交互方式，大幅改善过往以文本为输入的大模型的使用体验，同时有效避免基于 ASR 解决方案的繁琐流程以及可能引入的错误。

(2) 图像到文本多模态开源对话模型 (Chinese LLaVA)
- LinkSoul.AI 开源可商用的中英文双语**视觉-语言**助手 [Chinese-LLaVA](https://github.com/LinkSoul-AI/Chinese-LLaVA) 以及中英文视觉 SFT 数据集 [Chinese-LLaVA-Vision-Instructions](https://huggingface.co/datasets/LinkSoul/Chinese-LLaVA-Vision-Instructions)，支持中英文**视觉-文本**多模态对话的开源可商用对话模型。
- 模型、代码和数据[地址](https://huggingface.co/spaces/LinkSoul/Chinese-LLaVa)

### Llama 3

【2024-4-19】Meta [Llama 3](https://ai.meta.com/blog/meta-llama-3/)

8B base 接近原来的 70B，然后 instruction tuned 的 8B 远超原来的 70B。场景化 fine tune 变成更可行

### 猎鹰 Falcon -- 唯一免费商用

【2023-6-5】[碾压LLaMA，「猎鹰」彻底开源！400亿参数，万亿token训练，霸榜Hugging Face](https://zhuanlan.zhihu.com/p/634189977)
- [Open Source AI Has a New Champion](https://analyticsindiamag.com/open-source-ai-has-a-new-champion/)

各种各样的LLM给AI模型开源赋予了各种各样的角度。
- `LLaMA`给斯坦福的`Alpaca`和`Vicuna`等模型铺设了道路，搭好了舞台，成为了开源的领头羊。
- 猎鹰「`Falcon`」又杀出了重围，排名第一。[Hugging Face OpenLLM Leaderboard ](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
- ![](https://149695847.v2.pressablecdn.com/wp-content/uploads/2023/06/image-9.png)

Falcon与GPT系列一样采用单向Transformer-decoder模型架构，并以语言模型作为训练目标。与GPT-3相比，Falco的结构具有如下变化：
1. 位置编码：Falcon使用旋转位置编码（RoPE），近期的大模型包括GPT-Neo、PaLM和LLaMA等都采用了RoPE。
2. 注意力机制：使用Multi-Query将key和value映射到单个注意力头，只有query保留多头矩阵，这种简化方案能提升生成效率；使用FlashAttention将注意力矩阵分块，加速计算并降低内存IO开销。
3. Transformer：只使用单个layer_norm层，将Attention和MLP并行。

GPT、LLaMA和Falcon的计算流程对比
- ![](https://pic2.zhimg.com/80/v2-41d49005151e7b205f2eb44c2ee0f7a5_1440w.webp)
- 从Transformer模型结构上看，LLaMA将Layer-Norm层放在Ateention和FFN的输入，有助于大模型训练稳定性（由GPT2论文提出）。此外，FFN部分使用了门控线性层（GLU），这种结构最初被用在T5-1.1，实验效果优于MLP。
- LLaMA的设计着重于性能提升，而Falcon对Transformer的改进着重于效率提升：将Layer-Norm层减少到一个并简化了注意力的计算（Multi-Query Attention），因此Falcon比LLaMA的生成速度更快。

【2023-6-9】[击败LLaMA？史上最强猎鹰排行存疑，符尧7行代码亲测，LeCun转赞](https://www.toutiao.com/article/7242571430297862717), 符尧团队对模型做了更深入的[测评](https://twitter.com/Francis_YAO_/status/1666833311279517696)：没有提示工程、解码，一切都是默认设置
> 在MMLU上复现了LLaMA 65B的评估，得到了**61.4**的分数，接近官方分数（63.4），**远高于**其在Open LLM Leaderboard上的分数（**48.8**），而且明显高于猎鹰（52.7）。

OpenAI科学家Andrej Karpathy也对LLaMA 65B为什么在Open LLM排行榜上的分数明显低于官方（48.8 v.s. 63.4）表示关注。
> 避免在推特上发表关于猎鹰的文章，因为这一点不确定。

符尧团队论文：Chain-of-Thought Hub：
> 如果想要模型实现接近GPT-3.5的水平，最好是在LLaMA 65B上使用RLHF。

「Falcon」由阿联酋阿布扎比的技术创新研究所（TII）开发，从性能上看，Falcon比LLaMA的表现更好。
- 「Falcon」有三个版本——1B、7B和40B。
- TII表示，Falcon迄今为止最强大的开源语言模型。
- 最大版本，Falcon 40B，拥有400亿参数，相对于拥有650亿参数的LLaMA来说，规模上还是小了一点。Falcon 40B已经在经过精心筛选的1万亿token网络数据集的上进行了大量训练。
- 理解英语、德语、西班牙语和法语，并且在荷兰语、意大利语、罗马尼亚语、葡萄牙语、捷克语、波兰语和瑞典语等一些欧洲小语种上也懂得不少。
- 论文目前还没公开发布。

Falcon是目前**唯一**的可以免费商用的开源模型。

早期，TII要求: 商业用途使用Falcon，如果产生了超过100万美元以上的可归因收入，将会收取10%的「使用税」。

可是财大气粗的中东土豪们没过多长时间就取消了这个限制。至少到目前为止，所有对Falcon的商业化使用和微调都不会收取任何费用。

#### 中文Falcon

【2023-6-14】[中文Falcon基础模型：代码实现与增量训练](https://zhuanlan.zhihu.com/p/636994073)
- “伶荔（Linly）”项目团队以 Falcon 模型为底座扩充中文词表，利用中文和中英平行增量预训练将模型的语言能力迁移学习到中文，实现 Chinese-Falcon。[github](https://github.com/CVI-SZU/Linly)

中文Falcon的训练流程和细节。
- 首先, 扩充Falcon词表，包括 8,701 个常用汉字，jieba 词表中前 20,000个中文高频词以及 60 个中文标点符号。去重后共增加 25,022 个 token，词表大小扩充为 90,046。
- 改变词表后，embedding 和 target.output_layer 矩阵也要对应的扩充。将每个新增字/词在原始 tokenizer 中的对应向量的平均作为初始化。
- 第一阶段: 使用了50GB数据进行预训练，其中20G中文通用语料为模型提供中文语言能力和中文知识，10G中英文平行语料用于对齐模型的中英文表示，将英文语言能力迁移到中文上，20G英文语料用于数据回放，缓解模型遗忘。
- 模型训练阶段，使用与Falcon预训练相同的超参数设置：AdamW，ZeRO Optimizer，Batch size 2304，对于增量训练，设置更低的学习率2e-5。作为中文embedding初始化，先冻结Transformer权重，只更新embedding和output_layer部分，训练16k steps。进一步，在通用语料上启动全参数训练（Full-tuning）

使用 腾讯预训练框架: [TencentPretrain: Tencent Pre-training Framework](https://github.com/Tencent/TencentPretrain), 用于对文本、图像、语音等模态数据进行预训练和微调的工具包。

TencentPretrain有如下几方面优势:
- 可复现 TencentPretrain已在许多数据集上进行了测试，与原始预训练模型实现（例如BERT、GPT-2、ELMo、T5、CLIP）的表现相匹配
- 模块化 TencentPretrain使用解耦的模块化设计框架。框架分成Embedding、Encoder、Target等多个部分。各个部分之间有着清晰的接口并且每个部分包括了丰富的模块。可以对不同模块进行组合，构建出性质不同的预训练模型
- 多模态 TencentPretrain支持文本、图像、语音模态的预训练模型，并支持模态之间的翻译、融合等操作
- 模型训练 TencentPretrain支持CPU、单机单GPU、单机多GPU、多机多GPU训练模式，并支持使用DeepSpeed优化库进行超大模型训练
- 模型仓库 我们维护并持续发布预训练模型。用户可以根据具体任务的要求，从中选择合适的预训练模型使用
- SOTA结果 TencentPretrain支持全面的下游任务，包括文本/图像分类、序列标注、阅读理解、语音识别等，并提供了多个竞赛获胜解决方案
- 预训练相关功能 TencentPretrain提供了丰富的预训练相关的功能和优化，包括特征抽取、近义词检索、预训练模型转换、模型集成、文本生成等



#### 汉化：OpenBuddy -- 开源跨语种

【2023-6-9】[OpenBuddy](https://openbuddy.ai/), [开源多语言聊天机器人](https://github.com/OpenBuddy/OpenBuddy/blob/main/README.zh.md),对话 AI 和无缝多语言支持
- OpenBuddy 使命是提供一个免费、开源、能够离线运行的 AI 模型，这个模型在用户的设备上运行，不论他们的语言或文化背景如何
- 基于 Tii 的 Falcon 模型和 Facebook 的 LLaMA 模型构建，OpenBuddy 经过微调，包括扩展词汇表、增加常见字符和增强 token 嵌入。通过利用这些改进和多轮对话数据集，OpenBuddy 提供了一个强大的模型，能够回答各种语言的问题并执行翻译任务。

OpenBuddy 目前提供两个模型系列： `Falcon` 和 `LLaMA`

OpenBuddy 模型具备内容理解和顿悟能力，推出了 NBCE：一种超长上下文的 LLM 推理算法。
- 结合 OpenBuddy 模型，NBCE 能够实现 10K Context Windows 的推理，解决了大语言模型的上下文瓶颈问题。

LLaMA 仍存在训练集缺少多样性、训练数据不公开、许可协议限制商用等问题，阻碍了其在多种应用场景的发挥。

Falcon 模型使用 Apache 2.0 的可商用开源协议，不仅在协议和数据集方面更加开放，还采用了最新的 **Flash Attention** 等技术，展现出了惊人的性能和内容质量。

现有的 SOTA 开源语言模型，包括 LLaMA 和 Falcon，都存在一个问题：<span style='color:red'>跨语言支持能力薄弱</span>。这些模型主要以英语、法语等印欧语系为基础，并且缺乏跨语言对话场景的深度优化。

因此在理解中文等非印欧语系语言方面存在困难，更无法进行有意义的对话。

OpenBuddy 团队在多语言模型训练方面具备丰富的经验，曾在 LLaMA 的 7B、13B、30B 模型上进行了反复迭代和调优，研发出了OpenBuddy-LLaMA 系列开源模型。
- OpenBuddy-LLaMA 系列在中文、日语、韩语等多种语言上具备优秀的问题理解和回答能力。
- llama.cpp、Langport、FastChat 等开源项目均实现了OpenBuddy-LLaMA 系列模型的集成，并在社区中获得了广泛的应用。

OpenBuddy 团队成功地掌握了 Falcon 模型的训练诀窍，推出了全球首个基于 Falcon 架构、开放可商用的中文跨语言大模型——OpenBuddy-Falcon-7B。

优势：[更多介绍](https://mp.weixin.qq.com/s/VimLdVmZ27t4S8_C0Jlzjg)
- 支持多种语言，包括中文、日语、韩语、英语、法语、德语等。
- 采用了一种新颖的**跨语言学习**技术，大幅提高了模型对跨语言知识的理解能力和融合能力。
- 具备插件使用能力，模型能分析用户的意图，自动选取并调用插件。例如，调用Stable Diffusion 开源模型画图，调用内置的搜索引擎搜索资料等等。模型能够深度理解用户的需求，而不是重复字面上的要求，可以完成“画一个车水马龙的街道”，“画一个丑小鸭长大后变成的动物”等复杂指令。

#### Falcon 180b

【2023-9-7】[Falcon 180B 正式在 Hugging Face Hub 上发布](https://zhuanlan.zhihu.com/p/654739780)
- Technology Innovation Institute (TII) 训练的开源大模型 Falcon 180B 登陆 Hugging Face
- Falcon 180B 是使用 Amazon SageMaker 在多达 4096 个 GPU 上同时对 3.5 万亿个 token 进行训练，总共花费了约 7,000,000 个 GPU 计算时，这意味着 Falcon 180B 的规模是 Llama 2 的 2.5 倍，而训练所需的计算量是 Llama 2 的 4 倍。
- Falcon 180B 是 Falcon 40B 的升级版本，并在其基础上进行了创新，比如利用 Multi-Query Attention 等来提高模型的可扩展性。
- 当前最大的开源大模型，有 180B 参数, 且在 3.5 万亿 token 的 TII RefinedWeb 数据集上进行训练，这也是目前开源模型里最长的单波段预训练。
- model: [falcon-180B](https://hf.co/tiiuae/falcon-180B), [falcon-180B-chat](https://hf.co/tiiuae/falcon-180B-chat)
- [demo](https://hf.co/spaces/tiiuae/falcon-180b-demo)

Falcon 180B 在自然语言任务上的表现十分优秀。它在开源模型排行榜 (预训练) 上名列前茅，并可与 PaLM-2 等专有模型相差无几

Falcon 180B 使用

**硬件要求**

|  | 类型 | 种类 | 最低要求 | 配置示例 |
| --- | --- | --- | --- | --- |
| Falcon 180B | Training | Full fine-tuning | 5120GB | 8x 8x A100 80GB |
| Falcon 180B | Training | LoRA with ZeRO-3 | 1280GB | 2x 8x A100 80GB |
| Falcon 180B | Training | QLoRA | 160GB | 2x A100 80GB |
| Falcon 180B | Inference | BF16/FP16 | 640GB | 8x A100 80GB |
| Falcon 180B | Inference | GPTQ/int4 | 320GB | 8x A100 40GB |

### Lion 对抗蒸馏--闭源大模型

【2023-5-31】[港科大提出全新对抗蒸馏框架Lion](https://mp.weixin.qq.com/s/UPPkMbnkG1BZhE0nctNvhQ)，7B LLaMA模型接近ChatGPT 95%的能力
- 针对闭源大语言模型的对抗蒸馏框架，成功将 ChatGPT 的知识转移到了参数量 7B 的 LLaMA 模型（命名为 Lion），在只有 70k 训练数据的情况下，实现了近 95% 的 ChatGPT 能力近似。此外，框架的普适性使它不仅可以用于蒸馏 ChatGPT，还可方便地适用于其他闭源 LLMs。
- [Lion: Adversarial Distillation of Closed-Source Large Language Model](https://arxiv.org/abs/2305.12870)
- code: [Lion](https://github.com/YJiangcm/Lion)

**对抗知识蒸馏**（Adversarial Knowledge Distillation, AKD）旨在通过促使学生模型从生成的难样本中学习，来迭代改进学生模型的性能。受此启发，作者提出了一个将闭源大语言模型蒸馏到开源学生模型的对抗蒸馏框架。然而，此前的 AKD 方法需要能够访问老师模型的权重或梯度来识别难样本，因此不能直接适用于作者的场景。为了解决这个问题，作者利用 LLMs 强大的角色适应性，通过使用不同的 prompt 让 LLM 扮演不同的角色。

设计 prompt 让闭源 LLM 充当一个“裁判” Referee 来判别出教师的回答和学生的回答存在显著性能差距的难指令。并且，作者设计 prompt 让闭源 LLM 充当一个“生成器” Generator 来生成新的指令，这些生成的指令模拟了对应于被判别出的难指令的数据分布。

提出的对抗蒸馏框架如下图所示，每一轮迭代包括三个阶段：
- 1）模仿阶段，对于一组指令，将学生的响应与老师的响应对齐；
- 2）区分阶段，识别出难指令；
- 3）生成阶段，根据识别出的难指令，产生新的难指令以增加对学生模型的挑战。

### LLMTune

【2023-5-15】[康奈尔大学发布在一张显卡上微调650亿参数大模型的框架：LLMTune](https://www.toutiao.com/article/7233186412303122977)
- 为了降低大模型微调难度,Cornell Tech开源的LLMTune, 对于650亿参数的LLaMA模型微调仅需要40GB显存即可。

LLMTune在底层实现了LoRA算法，该算法使用GPTQ压缩LLM，需要实现量化版本LLM的反向传递。

LLMTune的功能包括：
- 对多个LLM的模块化支持（目前支持MetaAI开源的2个模型，LLaMA和OPT）
- 支持广泛的消费级NVIDIA的GPU显卡（包括RTX系列、A系列、GTX系列等）
- 代码库微小且易于使用（整个源代码仅64k大小）

LLMTune底层实现了LoRA算法，它依赖的库也很少
- 依赖库：pytorch、sentencepieces（Google开源的无监督分词工具）、transformers、peft、databsets
- LLMTune目前仅支持在NVIDIA显卡上的微调，所以上述PyTorch也需要cuda版本才可以使用


### LAION：Open Assistant

OpenAssistant 是一个开源项目，旨在开发免费提供给所有人使用的 AI 聊天机器人。
- 训练数据集 OpenAssistant Conversations 包含了超过 60 万个涉及各种主题的交互，用于训练各种模型。目前发布了经过指令调整的 LLaMA 13B 和 30B 模型，以及其他使用相同数据集训练的模型。

【2023-2-25】[Open Assistant 全流程训练细节（GPT3+RL）](https://zhuanlan.zhihu.com/p/609003237)

[Open Assistant](https://open-assistant.io/) 是 `LAION` 机构开源的，旨在训练一个 **ChatGPT 的小规模替代版本**，就像 `stable diffusion` 相对于 `dalle` 一样，让普通人都可以跑起来，传播力会比较广。
- LAION 机构全称: Large-scale Artificial Intelligence Open Network，是一个非盈利的**机器学习研究机构**，致力于为公众提供 AI 模型、数据集和开源代码。`Stable diffusion` 使用的开源数据就是该机构提供的。

如何在 Open Assistant 上训练一个完整的 ChatGPT
- 代码：[github.com/LAION-AI/Open-Assistant](https://github.com/LAION-AI/Open-Assistant)  Star 16.8k，Fork 1.3k，Issue 308open，535closed，代码更新三天前  
- 文档：[https://projects.laion.ai/Open-Assistant/docs/intro](https://projects.laion.ai/Open-Assistant/docs/intro)  
- 在huggingface上面的模型：[OpenAssistant (OpenAssistant)](https://huggingface.co/OpenAssistant)
- 数据格式介绍：[https://github.com/LAION-AI/Open-Assistant/blob/363a3a124471217e723d57b084122ae1ca41ab2a/notebooks/data-augmentation/stackexchange-builder/README.md](https://github.com/LAION-AI/Open-Assistant/blob/363a3a124471217e723d57b084122ae1ca41ab2a/notebooks/data-augmentation/stackexchange-builder/README.md)
 
ChatGPT 完整训练包括三个流程：
1.  Supervised FineTune（SFT）：使用人工编写的期望模型如何输出的数据集，对GPT-3进行微调
2.  Reward Model（RM）：使用人工标注的排序数据，训练奖励模型，预测人类更喜欢哪个输出
3.  强化学习微调 SFT：使用奖励模型作为强化学习优化目标，微调SFT模型
 
配置环境

```sh
git clone https://github.com/LAION-AI/Open-Assistant.git
cd Open-Assistant/model
pip install -r model_training/requirements.txt
pip install -r reward/instructor/requirements.txt
```

把所有的预训练模型和数据都放在 Open-Assistant/model/.cache 目录下，设置一个全局变量 DATA_DIR
 
```sh
# 还是在 Open-Assistant/model 目录下
mkdir -p .cache 
mkdir -p .saved_models
export DATA_PATH=$PWD/.cache # 设置数据目录
export MODEL_PATH=$PWD/.saved_models # 设置模型目录
```

#### 本地部署

【2023-4-13】[训练流程复现](https://mp.weixin.qq.com/s/8Yd_TcshuRdIqQ2bPOjedw)
- trlx + open assistant 结合，复现chatgpt

#### 第一步：训练 SFT
 
第一步是用更接近用户使用情况的数据来 finetune 已经 pretrain 好的 gpt-3 模型，论文中写这样子第一步的 finetune 过拟合一点，对于后面的强化学习训练有帮助。
- `SFT`是 Supervised FineTune，那么用什么数据进行监督呢？这一步使用的数据具体可以参考：[https://github.com/LAION-AI/Open-Assistant/blob/main/model/model_training/configs/config.yaml](https://github.com/LAION-AI/Open-Assistant/blob/main/model/model_training/configs/config.yaml)，包括如下数据

```yaml
datasets:
    - webgpt
    - squad_v2
    - adversarial_qa
    - trivia\_qa\_nocontext
    - xsum
    - cnn_dailymail
    - prompt_dialogue # TODO: need to fix the url 这个数据目前无法自动下载
    - multi_news
    - scitldr
    - soda
    - joke
    - gsm8k
    - dive_mt
    - wmt2019_zh-en
    - wmt2019_ru-en
    - wmt2019_de-en
    - ted\_trans\_nl-en
    - ted\_trans\_de-ja
    - instruct_tuning
    - wmt2019_de-en
    - samsum
    - soda_dialogue
```
 
Open Assistant 里面的 OA Private（jsonl格式）数据没有说的很清楚，不知道在哪里下载，所以我们尽量跳过这个数据，用其他的数据进行训练。
 
怎么跳过 OA Private 数据，使用其他数据训练呢？
 
首先先进入 model_training 目录
 
```sh
cd Open-Assistant/model/model_training
```
 
训练 SFT
 
```sh
python trainer_sft.py --configs defaults galactica-125m --cache_dir $DATA_PATH --output_dir $MODEL_PATH/sft_model
```
 
上面 --config 后面的参数代表需要载入的 config 项目，例如上面的 galactica-125m 是 configs/config.yaml 里面的关于模型的指定，具体内容如下面所示：
 
```sh
galactica-125m:
  learning_rate: 5e-5
  model_name: facebook/galactica-125m
  weight_decay: 0.01
  warmup_steps: 600
  gradient_checkpointing: false
  gradient_accumulation_steps: 2
  per_device_train_batch_size: 4
  per_device_eval_batch_size: 4
```

 
#### 第二步：训练 RM
 
第二步骤是训练一个 Reward Model，训练数据是给定 Prompt 后，对 SFT 生成的各个 Response 的打分数据。
 
例如数据长这样：

> Prompt: Hello  
> Response1: Hi --> 打分 5  
> Response2: Go away --> 打分 1  
> Response3: I am blulululuu --> 打分 2
 
那么把（Prompt，Response）组织成一条数据送入模型，相同的 Prompt 作为同一个 batch
 
> 数据1：(Hello, Hi) --> 模型输出打分假设为 A  
> 数据2：(Hello, Go away) --> 模型输出打分假设为 B  
> 数据3：(Hello, I am blulululuu) --> 模型输出打分假设为 C
 
最后我们训练的 Loss 就是将上面的数据两两组合，然后希望高分和低分的差距越大越好，例如 A-B 越大越好，A-C 越大越好，B-C越大越好。这里有点类似人脸识别里面的度量学习的负例，希望不同的人的人脸差距越大越好，只是这里多了一个符号，需要关注大小问题。
 
通过这样一通训练，我们的 Reward Model 就能学会给好的回答打更高的分，给坏的回答打更低的分啦。
 
具体训练通过如下命令达到：
 
```sh
cd ../reward/instructor
python trainer.py configs/deberta-v3-base.yml --output_dir $MODEL_PATH/reward_model
```
 
 
#### 第三步：训练 RL 模型
 
强化学习中我们使用 Actor-Critic 算法进行训练，其原理就是有两个模型，Actor 模型和 Critic 模型，Actor 模型用来做文本生成的行为，Critric 用来评价 Actor 行为的好坏。如果 Critic 给的分是高分，那么 Actor 就增加当前行为轨迹的出现概率，反之如果 Critic 给的分是低分，那么 Actor 就减小当前行为轨迹的出现概率。
 
这里前两步训练的模型分别作为 RL 训练中的 Actor 和 Critic：
*   Actor：第一步训练的 SFT，针对用户语料的文本生成模型 
*   Critic：利用了第二步训练的 Reward Model，来评价 SFT 生成的 Response 的好坏
 
OK，搞懂原理了，我们来设置一下两个模型的路径：
 
```sh
# choose a specific sft checkpoint
export SFT_MODEL=$MODEL_PATH/sft_model/<checkpoint-X>
# choose a specific reward model checkpoint
export REWARD_MODEL=$MODEL_PATH/reward_model/<checkpoint-X>
```
 
训练 RL
 
```sh
cd ../../model_training
python trainer_rl.py --configs defaults_rlhf --cache_dir $DATA_PATH --rank_model $REWARD_MODEL --sft_model $SFT_MODEL --output_dir $MODEL_PATH/rl_model
```

----

【2023-3-30】colossal ai 第三步实现

RLHF算法复现
- RLHF-Stage1 是 supervised-fintuning，即使用数据集进行**模型微调**。
- RLHF-Stage2 训练了**奖励模型**，通过对于同一个 prompt 的不同输出进行人工排序，得到对应分数，监督训练奖励模型。
- RLHF-Stage3 使用了强化学习算法，是训练流程中最复杂的一部分
- ![](https://pic3.zhimg.com/80/v2-c81b913204c4d2baa1c6063059beef66_1440w.webp)

解释
- `PPO` 部分，ColossalChat 分为两个阶段进行：
  - 首先是 **Make Experience** 部分，利用 SFT 、Actor、RM、Critic 模型计算生成 Experience 存入 buffer 中；
  - 之后是**参数更新**部分，利用 Experience 计算策略损失和价值损失。
- `PTX` 部分，ColossalChat 
  - 计算 Actor 输出 response 和输入语料的回答部分的交叉熵损失函数，用来在 PPO 梯度中加入预训练梯度，以保持语言模型原有性能防止遗忘。
  - 最后将策略损失、价值损失和 PTX 损失加和进行反向传播和参数更新。


### OpenChatKit

【2023-3-10】[ChatGPT开源替代来了！参数量200亿，在4300万条指令上微调而成](https://www.toutiao.com/article/7209917291104862731)，[Announcing OpenChatKit](https://www.together.xyz/blog/openchatkit)

[OpenChatKit](https://github.com/togethercomputer/OpenChatKit) 是一个类 ChatGPT 开源工具包，内含一个 20B 参数量的大模型，而且该模型在 **4300万**条指令上进行了微调。
- EleutherAI 开源 AI 研究团队一直在贡献开源大模型成果。
- 2020 年 7 月成立以来，该团队先后开源了基于 GPT-3 的、包含 60 亿参数的 NLP 模型 `GPT-J`，类 GPT 的27 亿参数模型 `GPT-Neo`，以及 200 亿参数的`GPT-NeoX-20B`。最终目标是将开源模型的参数规模扩展到 1700 亿左右，就像 GPT-3 一样。
- Together 组织基于 EleutherAI 开源的 GPT-Neo 和 GPT-J 构建了一个新的类 ChatGPT 开源项目 —— `OpenChatKit` 。

[OpenChatKit](https://github.com/togethercomputer/OpenChatKit) 
- 参数量达 20B 的开源模型，该模型基于 EleutherAI 的 GPT-NeoX-20B，在 4300 万条指令上进行了微调；
- 参数量达 60 亿的**审核模型**（moderation model），可以帮模型过滤不当内容；
- 可扩展的检索系统，可以帮模型检索维基百科等资源库，从而给出最新信息。
- 重点放在几个任务上，如多轮对话、问答、分类、提取和总结。他们用 4300 万条高质量指令对模型进行了微调，并与 LAION 和 Ontocord 合作，创建了该模型所基于的 [OIG-43M 数据集](https://laion.ai/blog/oig-dataset)。

OpenChatKit 有几个任务开箱即用：
- 1、将一份长的文件总结成一句话，并回答与该文件相关的问题，问答可进行多轮；
- 2、从非结构化文件中提取结构化信息，如下图所示；
- 3、将一个句子或段落分为不同的类别（比如情绪是积极还是消极）。

OpenChatKit 短板：
- 基于知识的封闭式问答。该聊天机器人可能会给出不正确的结果，需要用户提供反馈；
- 代码相关任务。由于训练数据中没有足够多的代码，因此该聊天机器人在代码方面表现欠佳；
- 重复性。该聊天机器人有时会重复自己的回答，用户可以点击刷新，开始新的对话；
- 上下文切换。该聊天机器人不太擅长转换话题。
- 创意写作和较长的答案。该聊天机器人不会生成长的、有创意的文本，如论文或故事。

huggingface 
- [测试链接](https://huggingface.co/spaces/togethercomputer/OpenChatKit)
- [GPT-NeoXT-Chat-Base-20B](https://huggingface.co/togethercomputer/GPT-NeoXT-Chat-Base-20B)

### LMFlow（港科大）

【2023-4-2】[港科大开源LMFlow](http://news.sohu.com/a/662207419_121119001)

[LMFlow](http://lmflow.com/) 训练一个只属于自己的模型。每个人可以根据自己的资源合理选择训练的模型，用于问答、陪伴、写作、翻译、专家领域咨询等各种任务。
- ChatGPT 的训练包括至少以下几个步骤：pretrain → supervised tuning → instruction tuning → alignment。
- LMFlow 库利用现有的开源大模型，支持这套流程的所有环节和灵活组合。

LMFlow 拥有四大特性：可扩展、轻量级、定制化和完全开源。
- 用户可以很快地训练自己的模型，并继续进行二次迭代。
  - 这些模型不仅限于最近流行的 `LLaMA`，也包括 `GPT-2`、`Galactica` 等模型。
  - 不需要从头预训练，只需要以 finetune 作为切入点即可。
- 即便是有限的计算资源，也能让使用者针对专有领域支持个性化训练。
  - 基于 70 亿参数的 LLaMA，只需 1 张 3090、耗时 5 个小时，就可以训练一个专属于自己的个性化 GPT，并完成网页端部署。
  - 研究者已经用该框架单机训练 330 亿参数的 LLaMA 中文版，并开源了模型权重用于学术研究
  - 特定专家领域（以医疗为例），只需微调 6 个 A100 * 天，就能够获得和 ChatGPT 相当甚至更好的效果, 参数量是chatgpt的1/20。
  - ![example](https://p6.itc.cn/q_70/images03/20230402/c44c5d3681d24e529e55b2797db2373f.png)
  - ![model performance](https://p1.itc.cn/q_70/images03/20230402/397f2cd7d524479aa547711d436f1264.png)
- [Chat Demo](http://lmflow.com/chat), github: [MLFlow](https://github.com/OptimalScale/LMFlow)
- 模型和数据量越大，训练时间越长，效果越佳。

目前该研究也在训练更大参数量（650 亿）和更大数据量的中文版模型，效果还会持续提升

安装使用
- [github](https://github.com/OptimalScale/LMFlow/blob/main/readme/README_zh-hans.md)

### ChatGLM 清华

详见站内专题:[ChatGLM](chatglm)

### CPM-Bee 基座模型+Luca（露卡） -- OpenBMB

【2022-7-18】OpenBMB+清华NLP 刘知远团队大模型公开课全网首发: 
- [大模型与脑科学](https://www.openbmb.org/community/course)
- [Prompt Tuning, Delta Tuning 背景以及技术](https://www.openbmb.org/community/course)
- [BMInf, BMTrain, BMCook相关背景、技术和使用](https://www.openbmb.org/community/course)

【2023-5-27】5月27日，OpenBMB 发布大模型 [CPM-Bee](https://live.openbmb.org/models/bee)，最高10b，并推出对话类模型产品“露卡”（Luca）。[资讯](https://mp.weixin.qq.com/s/d9F5kSbFye1oEhqfzFU7XA)
- 露卡”（Luca）支持多轮对话与深度语义理解，可以根据输⼊文本语境和创作要求 ⾃动⽣成原创文案，并进一步进行改写或翻译，可以具体运用到诸多办公生活场景。支持结构化**内容生成**，可以 一键生成表格和代码。具备**多模态**输入理解的能力，能够识**别和解读图片**，升级了传统自然语言理解任务处理（情感分析、信息抽取等）的能力，最炫酷的功能就是能够**联网**进行信息搜索和摘要。
- 研发团队包括`面壁智能`和`清华大学`自然语言处理实验室（THUNLP）
- 基于自己的大模型 CPM-Ant 百亿参数中文大模型，性能优异; 直播训练过程,[model细节](https://www.openbmb.org/community/blogs/blogpage?id=98afef2ce45f4fe9a4bc15a66d7ccb92)
- 效果：英文约等于 LLaMA-13B，中文ZeroCLUE评测远超其他模型
  - 2023年1月15日，CPM-Bee 模型在 ZeroCLUE 榜单上[登顶榜首](https://zhuanlan.zhihu.com/p/599691418)，距离上一次刷新仅仅四天，并且将总分提高了3.375分，超过了原排名前五的模型间分数提升之和。
- 跟国内开源最强模型ChatGLM-6B相比：`CPM-Bee` 亮点是**完全开源**，可随意商用，基于transformer，10b模型推理只需20GB显卡
- [github](https://github.com/OpenBMB/CPM-Bee)

`CPM-Bee`, 开源双语预训练语言模型，参数量为10B，拥有十余种原生能力和强大的通用语言能力，并支持结构化输入和输出。
- `CPM-Live`直播训练过程中的第二个里程碑。训练过程是低成本和环境友好的。
- 发布各种压缩版本以适应不同的硬件配置。
- `CPM-Bee`采用了开放的许可协议，发布后的模型和代码将完全开放。
- OpenBMB 始终秉承“让大模型飞入千家万户”的开源精神，CPM-Bee基座模型将完全开源并且可商用，以推动大模型领域的发展。

相比较ChatGLM-6B，`CPM-Bee`的主要特点如下：
- **开源协议**更加友好，只要获取书面授权即可商用。代码、预训练结果均开源，训练过程也是**全球直播**。
- 从评测结果看，`CPM-Bee`模型效果也很优秀，中文`ZeroCLUE`评测中远超其它模型，英文多个任务评测结果也与`LLaMA-13B`差不多，部分任务上的表现超越`GPT-3`。
- 推理成本与`ChatGLM-6B`差不多，最低10亿参数规模的模型仅需要4.1GB显存可做推理，而100亿参数规模的推理仅需20GB显卡，单张消费级显卡即可。

`CPM-Bee` 值得关注，如果商用协议未来保持友好，且不断升级迭代，那也许会是一个可以和`ChatGLM-6B`模型竞争的一个国产替代好选择

【2023-6-1】[大模型再添重磅玩家：清华大学NLP实验室开源可商用大模型CPM-Bee](https://www.toutiao.com/article/7239364641036517940)
- 5月27日，OpenBMB发布了一个最高有100亿参数规模的开源大语言模型CPM-BEE，OpenBMB是清华大学NLP实验室联合智源研究院成立的一个开源组织。该模型针对高质量中文数据集做了训练优化，支持中英文。根据官方测试结果，其英文测试水平约等于`LLaMA-13B`，中文评测结果优秀。

CPM 全称Chinese Pretrained Model，Bee是该系列模型的第二个里程碑版本。
- CPM-Bee模型是基于CPM-Ant模型继续训练得到。后者是2022年5月到9月训练的大语言模型。
- 而CPM-Bee则是从2022年10月13日开启训练，相比之前，模型在很多任务上做了优化，包括文字填空、文本生成、问答等。
- 基于transformer架构的**自回归**模型，在高质量中英文数据集上训练了半年左右的时间。包含4个系列的预训练结果，参数分别是10亿、20亿、50亿和100亿。
- CPM-Bee的中文数据集原始数据有1TB左右，做了预处理清洗之后有200GB的高质量中文数据集结果。并加入了400GB的多语言数据集，但没有透露数据集的具体信息。
- CPM-Bee训练时间230天，成本85万左右。训练的tokens数量约6380亿左右（本部分数据与GitHub介绍有冲突）。
- ![img](https://camo.githubusercontent.com/dcb83d9b76b9662f8cadc17fb1ccfc2115080fffa49d7a407d82431be54cc6e6/68747470733a2f2f692e696d676c6f632e636f6d2f323032332f30362f30372f5677674c4c4e2e706e67)

此外，CPM-Bee的一个特点是在推理上占用的资源很小：

| CPM-Bee模型版本 | 推理的显存 | 推荐的硬件 |
| --- | --- | --- |
| CPM-Bee-10B | 20GB | RTX3090（24GB）|
| CPM-Bee-5B | 11 GB | RTX 3090（24 GB）|
| CPM-Bee-2B | 6.7 GB | GTX 1080（8 GB）|
| CPM-Bee-1B | 4.1 GB | GTX 1660（6 GB）|

最小的10亿参数版本的模型仅需要4.1GB显存即可运行！50亿参数规模版本需要11GB显存。另一个清华大学著名的开源模型ChatGLM-6B版本的推理需要13GB显存。

【2023-5-15】面壁智能 联合来自清华、人大、腾讯的研究人员共同发布了 中文领域首个基于交互式网页搜索的问答开源模型 WebCPM，这一创举填补了国产大模型该领域的空白。面壁智能自研 工具学习引擎 BMTools 也因此被成功实践。

[面壁智能](https://modelbest.cn)在 ChatGPT Plugins 发布后仅十天就推出 [BMTools](https://github.com/OpenBMB/BMTools), [官方公众号报道](https://mp.weixin.qq.com/s/onB66ADNau_1eV_a42nGww)
- BMTools 是一个基于语言模型的开源可扩展工具学习平台。
- 面壁研发团队将各种各样的工具调用流程都统一到一个框架上，使整个工具调用流程标准化、自动化。
- BMTools 目前支持的插件，涵盖娱乐，学术，生活等多方面，包括 douban-film（豆瓣电影）、search（必应搜索）、Klarna（购物）等。开发者可以通过 BMTools，使用给定的模型（比如 ChatGPT、GPT-4）调用多种多样的工具接口，以实现特定功能。此外，BMTools 工具包也已集成最近爆火的 Auto-GPT 与 BabyAGI。

WebCPM 成功实践了 BMTools, 中文领域首个基于交互式网页搜索的问答开源模型框架 `WebCPM`，这一创举填补了国产大模型该领域的空白
- [paper](https://arxiv.org/abs/2305.06849), [code](https://github.com/thunlp/WebCPM)
- WebCPM 的特点在于其信息检索基于交互式网页搜索，能够像人类一样与搜索引擎交互从而收集回答问题所需要的事实性知识并生成答案。换言之，大模型在联网功能的加持下，回答问题的实时性和准确性都得到了飞跃式增强。
- WebCPM 对标的是 WebGPT ， WebGPT 也正是微软近期推出的 New Bing 背后的新一代搜索技术。同 WebGPT一样，WebCPM 克服了传统的 LFQA（ Long-form Question Answering）长文本开放问答范式的缺陷：依赖于非交互式的检索方法，即仅使用原始问题作为查询语句来检索信息。


问题：[issue](https://github.com/OpenBMB/CPM-Bee/issues/71)
- CPM-Bee 跟 ChatGLM 什么关系？
- 与 ChatGLM 对比评测

#### VisualGLM-6B

【2023-05-17】 发布 VisualGLM-6B，一个支持图像理解的多模态对话语言模型
- ![](https://github.com/THUDM/ChatGLM-6B/raw/main/resources/visualglm.png)

### New Bing

[New Bing](https://www.bing.com/new)
- ![](https://pic2.zhimg.com/80/v2-a75ed171783f8c561fb6a80b265302c9_1440w.webp)
- 国内访问受限

如何破解跳回国内的问题
1. 在必应首页登录自己的微软账号，然后挂VPN。
1. 在国内版（cn.bing.com）的首页更改地区到英国或者其他国家（右上角三根横线，点设置-地区，就可以更改了）
1. 访问 [New Bing](https://www.bing.com/new) ，[下载 Edge 浏览器](https://www.microsoft.com/en-us/edge/download?form=MA13FJ)就可以使用了
  - 注意：【2023-5-26】Mac下安装 Apple chip版本，而不是 Intel chip，否则装完无法启动

### 文心一言

【2023-3-16】百度正式发布[文心一言](https://yiyan.baidu.com/)，现场demo视频展示。[资讯](https://www.ithome.com/0/680/102.htm)
- 文心一言大模型的训练数据包括万亿级网页数据、数十亿的搜索数据和图片数据、百亿级的语音日均调用数据，以及 5500 亿事实的知识图谱等。
- 文心一言是新一代知识增强大语言模型，是在 ERNIE 及 PLATO 系列模型的基础上研发的。关键技术包括有监督精调、人类反馈的强化学习、提示、知识增强、检索增强和对话增强。前三项是这类大语言模型都会采用的技术，ERNIE 和 PLATO 中也已经有应用和积累，在文心一言中又有了进一步强化和打磨；后三项则是百度已有技术优势的再创新。

李彦宏展示了文心一言在五个使用场景的表现，包括文学创作、商业文案创作、数理推算、中文理解和多模态生成
- **文学创作**场景中，文心一言根据对话问题将知名科幻小说《三体》的核心内容进行了总结，并提出了五个续写《三体》的建议角度，体现出对话问答、总结分析、内容创作生成的综合能力。
- **商业文案创作**场景中，文心一言顺利完成了给公司起名、写 Slogan、写新闻稿的创作任务。
- 文心一言还具备一定的思维能力，能够学会**数学推演**及**逻辑推理**等相对复杂任务。面对“鸡兔同笼”这类锻炼人类逻辑思维的经典题，文心一言能理解题意，并有正确的解题思路，进而像学生做题一样，按步骤算出正确答案。
- 中文理解
  - 文心一言正确解释了成语“洛阳纸贵”的含义、“洛阳纸贵”对应的经济学理论，还用“洛阳纸贵”四个字创作了一首藏头诗。
- **多模态**生成方面，文心一言生成文本、图片、音频和视频的能力。
  - 语音，会说四川话、东北话、广东话和台湾话。文心一言甚至能够生成**四川话**等方言语音；
  - 图像，调用文心一格能力
  - 视频，文心一言的视频生成能力则因成本较高，现阶段还未对所有用户开放，未来会逐步接入。

【2023-3-23】爆出百度文心一格疑似中文翻译英文，再调用开源画图（stable diffusion），[详见](https://m.weibo.cn/status/MyvXJ5EGb?jumpfrom=weibocom)
- 画“鼠标和总线”，会画出来“老鼠和公共汽车”，因为“鼠标”和“总线”的英文是“mouse”和“bus”
- 画“起重机”，它会莫名其妙地画出一个鹤的头，因为“起重机”的英文是“crane”，这个单词更常用的意思就是“鹤”。
- 如果关键词不加“中国”，那么画出来的都是白种人，连国旗都是星条旗，等等，不一而足。
- “一可以豆子”，这在汉语里根本不是人话，但如果机翻成英语，“one can bean”，它就轻松地画出“一罐头豆子”。
- “牛肉可以”，“满冰箱可以”。
- 英语里面只有常用肉有专门的词汇，罕见肉没有英语词汇
- 画“羊肉和驴肉”，它只会画出羊肉，而驴肉只能画出一头驴，同时，因为它不理解这个句子，还让驴长了羊毛。
- “土耳其张开翅膀”，画了个火鸡
- “水瓜”当然要画个西瓜
- “牛奶路”画了个“银河”。
- “云中的平面”，结果画了个飞机，这是因为“云中的平面”机翻之后是“plane in cloud”，那个英语的人工智能当然会画个飞机。
- “金色摔倒”，不出意外的话，机翻成了“golden fall”，也就是“金色的秋天”。
- “中国论文”，它画了一幅山水画，为啥？因为论文是“paper”，但“chinese paper”是宣纸，所以它画了一幅水墨画象征宣纸。作为佐证。
- 真正输入“中国纸”画出来的结果。
-n“法国粉笔”，它画了个法国人的“炭笔素描”（chalk）。
- 树叶封面苹果，“封面”就是“cover”，“cover”就是“覆盖”，很明白吧？
- 画菜名，什么鱼香肉丝、松鼠鳜鱼、红烧狮子头，画出来的莫名其妙的东西，并不是人工智能天真可爱，而是汉译英的功夫不到家，难为了羊皮里的外国程序。

解释
- 目前开源的图文数据大部分是英文的，可以参考laion这个开源数据库，所以目前的diffusion model基本都是英文驱动，这也导致了你说的怪异现象；当然我们期待同等规模的中文开源数据库的出现；stable diffusion是一种网络结构，开发者完全可以使用laion数据集和sd结构训练一个自己的网络，无需要套皮

#### 文心一言评测

- 2023-3-17 22:30 拿到内测码

评测
- 对话能力
- 多模态能力：图片、视频

内测总结，[参考](https://www.zhihu.com/question/589955024)
- (1) 模型信息：
  - 基于transformer，使用海量数据训练而来，细节未知，跟GPT-4一样神神秘秘
- (2) 工程性能
  - 输入长度最大1024个字
  - 输出支持文本、表格、代码、图片、语音
  - 响应速度跟GPT-3.5 Turbo类似，比GPT-4快很多
- (3) 内容质量
  - 知识丰富，集成了中文知识图谱，对时兴的电视剧（狂飙）、小说了如指掌。
  - 语料质量不高，泛娱乐化，严谨科学的预料相对较少
  - 不联网，训练数据截止约2022年底，无法获取当前时间信息 —— 不同于NewBing
  - 但具备近实时纠偏能力，怀疑收到用户负反馈后，有语料纠偏机制，大概间隔几小时。
- (4) 对话能力
  - 基础能力：具备NER（命名实体识别）、指代、纠错等浅层语义，未出错
  - 连贯性：未发现
  - 逻辑性
  - 一致性
  - 记忆力：具备上文感知能力，但不太稳定，chatgpt也是
  - 风格化：具备角色模拟能力，用法不如chatgpt多、灵活（假设你是***）
- (5) 自我意识
  - 承认无知：用户否认时，当场认怂，但再次询问时，依然坚持自己的立场，没被用户带偏。
  - 敢于质疑：用户表述偏差时，敢于质疑，并给出一系列依据。
- (6) 专业能力
  - 自动摘要：提取题目、总结要点
  - 机器翻译：多语言翻译
  - 写代码：支持，颜色显示，代码可执行，但有时结果不对；
    - 不具备chatgpt里一键复制按钮
    - 代码质量不如chatgpt，毕竟人家背后有GitHub大规模代码做后盾。
  - 文案创作：表现还不错，当然跟chatgpt一样，有时不能满足字数要求
  - 数学题：看题目难度，解答有的对，有的错，展示形式上较好（公式），质量上同chatgpt
  - 作诗：擅长藏头诗、文学创作，中文理解能力较好
  - 自然语言格式化：文本转表格（markdown）、json（有些质量问题）
- (7) 多模态能力：支持文本、表格、图片、语音
  - 语音播放：仅支持广东话、四川话、东北话、闽南语，不支持其他，如普通话、英语
  - 画画（文生图）：调用文心一格，文生图质量不错，优于普通版stable diffusion
    - 不具备图像理解能力，VisualQA不行，当然也不能根据语义修改图像（微软Visual GPT）
  - 还不能做视频
- (8) 道德准则
  - 违规违法约束：较好，拒绝回答非法问题（抢银行、炸弹制作等）
  - 负面情绪干预：能识别用户负面情绪，并适当引导

#### 文心一言理性思维能力

【2023-3-18】[文心一言的理性思维能力距离 GPT-4 差多少？我们第一时间测试了一下](https://mp.weixin.qq.com/s/94UAkQyL48DD5J_zku6MOg)

认知科学家评定人类理性思维的四类经典测试任务：
- 语义错觉类任务；
- 认知反射类任务；
- 证伪选择类任务；
- 心智程序类任务。

四类任务总计 26 道题目。

在测试之前，已经预估文心一言的表现会不如 GPT-4，但最终实际测试结果还是令人大跌眼镜，可能与百度开发团队的认知有关系。
- 26 道题目，GPT-3.5 答对 15 道；GPT-4 答对 23 道；文心一言答对 2 道。
- 大约在 40%-60%左右的正确率，如果略微高估，前三类任务 17 道题总计估算为答对 10 道题，加上第四类任务，人类大约答对 6 道。最终将人类的正确率估算为 26 道题目，答对 16 道。正确率大约为 62%。
- `62%`，这也许就是觉得一个大语言模型像是一个真正的人一样的`临界值`。
- GPT-3.5 接近这个数值，所以人们被它大大地震惊住了。而 GPT-4 远远超越了这个值。
- 而百度的文心一言，只有 8%。路漫漫其修远矣。

在中文自然语言处理领域，百度提供的 NLP 开源项目是数量最多的、维护最勤奋的、质量最好的。包括带队研发的写匠项目，调用的也是百度 NLP 团队开发的分词开源包。

但是，文心一言表现这样，无法简简单单地用研发时间不足来解释、产品是第一版上线来敷衍。这类话可能是拿来敷衍李老板可以，但是敷衍全球同行是非常危险的。

怀疑百度该项目的研发团队，极可能走错路线了。以百度的技术实力，表现不至于这样。极可能是团队领导者定错目标了：拿到尽可能多的知识单元。

所以，新品发布会上，从 CEO 到 CTO，两位专家，还在拿百度拥有全球最大的中文知识单元说事。

但是这压根不是 GPT-4 令人震惊的原因
- GPT-4 这类产品真正令人震惊的是，从 GPT-3.5 开始，它真的像一个人类了。这才是形成全球性碾压式传播的根本。
- 如何让 GPT-3.5 更像是一个人类，能够更快地自我学习、自我纠错。

中文知识单元的数量，在这个事情上毫无意义啊。

要教会一个三岁的小朋友尽快学会说话，两个重要任务：
- 1）`生命`：让她尽快明白语义、语音之间的各类规则以及如何用语义、语音表达一个物理世界。
- 2）`生态`：想方设法给她在家里创造一个有助于孩子学说话的生态。比如，雇佣阿姨带小美妞的时候，第一考虑就是这阿姨爱不爱说话，外不外向。显然，一个喜欢说话、外向的阿姨，更容易带动小美妞说话。

结果，百度该项目团队的做法好比是，直接给一个三岁的小朋友扔了一千万吨词典，你背着词典走路吧。生命何在？生态何在？

如果始终沿着这条技术路线走下去，怀疑在 OpenAI 团队开源之前，不可能产生一个近似于数字生命的产品。而 OpenAI 团队是将大语言模型当作真正的生命来对待，从构建一个数字生命的基本机制开始设计，一切工作都是围绕两个基本出发点：
- 1）生命：尽量促进“智能”的自发涌现；
- 2）生态：尽量设计一个促进有助“智能”诞生并发育的生态。

在早期，这个数字生命很幼稚，但过了千亿参数级别之后，很多早期打好的良好基础，就会带来极其多的“智能”涌现。好比小朋友从三岁学说话，长大之后，流利使用语言完成诸多大事。

不能在还没有涌现“智能”之前，就急匆匆地去卖应用、搞数据对接。那压根与 GPT-4 不是一类产品啊。

我们要的是一个数字生命，以及这个新兴的数字生命与生态带来的新世界；还是又多了一个更方便地查询知识单元的工具。

### 阿里 通义千问

【2023-4-7】阿里大模型（[通义千问](https://tongyi.aliyun.com/)）内测申请，[官方](https://mp.weixin.qq.com/s/Zp23VMxQiWHZzsBZNUtPwQ)

阿里大模型[内部访谈](https://mp.weixin.qq.com/s/PhiuEZPKAYBc_6mhOseBRw)

### 昆仑万维 天工

【2023-4-10】昆仑万维和奇点智源合作发布[「天工」大模型4月17日启动邀测](https://mp.weixin.qq.com/s/yikVXp2sda4frtl_TrSKzw), 4月17日开始[内测申请](http://tiangong.kunlun.com)
- 【2023-5-26】[内测地址](https://neice.tiangong.cn/interlocutionPage)

### 微软 DeepSpeed Chat

【2023-4-12】[微软DeepSpeed Chat震撼发布，一键RLHF训练千亿级大模型](https://mp.weixin.qq.com/s/G8W9nSQd600wesSJFE2dhw), 微软开源一个模型训练中加入完整RLHF流程的系统框架——[DeepSpeed Chat](https://github.com/microsoft/DeepSpeed)。
- 由于OpenAI太不Open，开源社区为了让更多人能用上类ChatGPT模型，相继推出了LLaMa、Alpaca、Vicuna、Databricks-Dolly等模型。
但由于缺乏一个支持端到端的RLHF规模化系统，目前类ChatGPT模型的训练仍然十分困难。
- DeepSpeed Chat的出现，正好补全了这个「bug」,DeepSpeed Chat把成本大大地打了下来。
- 只要花1620美元，就可以通过混合引擎DeepSpeed-HE，在2.1天内训练一个**OPT-66B**模型。
- 如果使用多节点、多GPU系统，DeepSpeed-HE可以花320美元，在1.25小时内训练一个OPT-13B模型，花5120美元，就能在不到一天的时间内训练一个**OPT-175B**模型。

DeepSpeed Chat具有以下三大核心功能：
1. 简化ChatGPT类型模型的训练和强化推理体验
  - 开发者只需一个脚本，就能实现多个训练步骤，并且在完成后还可以利用推理API进行对话式交互测试。
2. DeepSpeed-RLHF模块
  - DeepSpeed-RLHF**复刻**了InstructGPT论文中的训练模式，并提供了数据抽象和混合功能，支持开发者使用多个不同来源的数据源进行训练。
3. DeepSpeed-RLHF系统
  - 团队将DeepSpeed的训练（training engine）和推理能力（inference engine) 整合成了一个统一的**混合引擎**（DeepSpeed Hybrid Engine or `DeepSpeed-HE`）中，用于RLHF训练。由于DeepSpeed-HE能够无缝地在推理和训练模式之间切换，因此可以利用来自DeepSpeed-Inference的各种优化。

经过DeepSpeed-Chat的训练，13亿参数版「ChatGPT」在问答环节上的表现非常亮眼。
- 不仅能get到问题的上下文关系，而且给出的答案也有模有样。
- 多轮对话中，这个13亿参数版「ChatGPT」所展示出的性能，也完全超越了这个规模的固有印象



#### 效果评估

与Colossal-AI或HuggingFace-DDP等现有系统相比，`DeepSpeed-Chat`具有超过一个数量级的吞吐量，能够在相同的延迟预算下训练更大的actor模型或以更低的成本训练相似大小的模型。
- 在单个GPU上，DeepSpeed使RLHF训练的吞吐量提高了10倍以上。虽然CAI-Coati和HF-DDP都可以运行1.3B的模型，但DeepSpeed可以在相同的硬件上运行6.5B模型，直接高出5倍。
- 单个节点的多个GPU上，DeepSpeed-Chat在系统吞吐量方面比CAI-Coati提速6-19倍，HF-DDP提速1.4-10.5倍。

DeepSpeed-Chat能够获得如此优异的结果，关键原因之一便是混合引擎在生成阶段提供的加速。

#### 安装

```sh
git clone https://github.com/microsoft/DeepSpeed.git
cd DeepSpeed
pip install .
# example
git clone https://github.com/microsoft/DeepSpeedExamples.git
cd DeepSpeedExamples/applications/DeepSpeed-Chat/
pip install -r requirements.txt
```

#### 运行

```py
# 1.3B模型，1个消费级GPU, 耗时1-2h
python train.py --actor-model facebook/opt-1.3b --reward-model facebook/opt-350m --num-gpus 1
# 13b参数模型, 8个GPU，半天时间
python train.py --actor-model facebook/opt-13b --reward-model facebook/opt-350m --num-gpus 8
# 66B参数模型，64个GPU
python train.py --actor-model facebook/opt-66b --reward-model facebook/opt-350m --num-gpus 64
```

#### 问题

实测问题
- 数据量大时，出现OOM，原因是代码默认先把所有数据加载到内存，划分训练集和验证集，导致还没开始训练就OOM了
- 已提交[issue](https://github.com/microsoft/DeepSpeed/issues/3214)，无回复



### 知乎：知海图AI

【2023-4-13】知乎发布大模型「知海图 AI」并内测「热榜摘要」，知乎发现大会介绍的 “知海图AI”大模型
- “知海图AI”的训练基于`面壁智能`自主研发的 `CPM`企业级大模型 与 `ModelForce`大模型系统。

### Claude

[Claude AI](https://claude.ai/)（克劳德人工智能）是一款面向各种规模任务的下一代人工智能助手，为部分客户和研究人员提供支持。
- Anthropic成立于2021年，是一家人工智能安全和研究公司，致力于建立可靠的、可解释的、可操纵的人工智能系统，公司的创始团队来自于OpenAI
- 功能包括文本摘要、信息查询等多个方面，通过其免费接入选项（AI Playground和网站演示），用户可以体验其强大的功能。

三个大的模型版本：
1. `Claude+`
  - Claude+是Claude的**高性能优化**版本，对标`GPT-4`。截至2023-10-23和GPT4性能差距最小的可公开测试的模型。可直接作为GPT4的平替来使用。
  - 然而，免费使用的Slack版本并不包括Claude+。如果想体验Claude+的性能，最佳选择是poe的会员服务。
2. `Claude Instant`
  - Claude Instant是可以通过Slack免费使用的版本，性能对标`GPT3.5`。
  - 它提供了一个快速而经济的方式来获取高质量的文本生成服务。
3. `Claude-instant-100k`
  - 目前已经公布的大模型中，**上下文最长**的版本，token数量扩展到了100K个，大约对应75000个单词。这意味着用户现在可以提交数百页的材料供Claude消化和分析，而且与Claude的对话可以持续数小时甚至数天。
  - 然而，类似于Claude+，Claude-instant-100k目前也只能通过poe会员服务来使用。


#### 【2023-4-13】Claude 1

【2023-4-13】[「ChatGPT最强竞品」爆火：不限量不要钱免注册！](https://mp.weixin.qq.com/s/QB85YPjh6DMBTPla4NDfXg)
- [introducing-claude](https://www.anthropic.com/index/introducing-claude), [Meet Claude: Anthropic’s Rival to ChatGPT](https://scale.com/blog/chatgpt-vs-claude)
- [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)
- 体验方式：[poe](https://poe.com/Claude-instant)
- 申请：[Claude Early Access](https://www.anthropic.com/earlyaccess)

#### 【2023-5-12】Claude 100k

【2023-5-12】[Introducing 100K Context Windows](https://www.anthropic.com/index/100k-context-windows)
- We’ve expanded Claude’s context window from 9K to 100K tokens, corresponding to around 75,000 words
- The average person can read 100,000 tokens of text in ~5+ hours[1], and then they might need substantially longer to digest, remember, and analyze that information. Claude can now do this in less than a minute. 


#### 【2023-7-11】Claude 2

【2023-7-11】[Claude2](https://www.anthropic.com/news/claude-2) 对比于ChatGPT来说，主要优点：
- 免费注册使用（魔法上网）
- `Claude2`支持100K 上下文，价格上比`GPT4-4K`便宜了4-5倍
- 直接导入文档进行总结。
  - ChatGPT只能解析网页内容，使用插件应用才能支持文档导入总结。
  - 而Claude2本身就已经支持多个文档导入，并可以概括文档之间的关系
- 知识库对比ChatGPT更新，知识截止时间是2023年初
- 支持更长上下文输入，目前开放了10万tokens进行输入。

Anthropic正式推出Claude Pro版本来对标ChatGPT Plus版本。
- ![](https://pic2.zhimg.com/80/v2-b50e4e80ef4819b43232a72bd3ed89b1_1440w.webp)

Claude是GPT3.5的国内最佳替代


#### Claude 2.1

【2023-11-23】Claude 2.1 版本支持输入20万个Token超GPT-4 Turbo

OpenAI 竞争对手 Anthropic 日前推出了 Claude 2.1 聊天机器人及对应同名 AI 模型，Claude 2.1 支持输入多达 20 万个 Token，并改善了准确度，同时新增系统预设提示词（System Prompt）功能。

Claude 2.0 单次回话只支持 10 万个 Token，而 Claude 2.1 支持输入多达 20 万个 Token，相当于 15 万个文字或是 500 页的文件，已凌驾于 OpenAI GPT-4 Turbo 的 12.8 万个 Token
- 平均 1 个 Token 对应 4 个英文字符，100 个 Token 约对应 75 个英文单词
- Claude 2.1 号称准确率是 Claude 2.0 两倍，此外该模型也改善了对于文本内容的理解能力，特别是对法律文件、财报与技术规格等更高准确度的文档进行了优化，号称“出现错误答案的比例减少了 30%”


#### 【2024-3-4】 Claude 3

【2024-3-4】Anthropic 发布了一组 Claude 3 系列大模型，称其功能最强大的模型在各种基准测试中均优于 OpenAI 的 GPT-4 和 Google 的 Gemini 1.0 Ultra。
- Claude3 优化了**准确性**和**长文本窗口**能力。
  - 准确性上，Anthropic 用了大量复杂的**事实问题**来针对当前模型中已知的弱点，将答案分为**正确答案**、**错误答案**（或幻觉）和**承认不确定性**。相应地，Claude3 模型表示它<span style='color:red'>不知道答案，而不是提供不正确的信息</span>。其中最强的版本 Claude 3 Opus 在具有挑战性的开放式问题上的准确性（或正确答案）上，比 Claude 2.1 提高了1倍，同时也减少了错误答案的水平。
- Claude 3 有「引用」功能，可指向参考材料中的精确句子来验证他们的答案。
- Claude 3 系列模型将提供 **200K** token 的上下文窗口。后续，所有这三种模型都能够接受超过 100 万 token 的输入，这部分能力会提供给需要增强处理能力的精选客户。Anthropic 在技术报告中简单阐述了 Claude3 的上文本窗口能力，包括有效处理更长的上下文提示词，以及回忆能力。
- Claude3 首次带来**多模态**模型，可以输入图像，但无法输出图像内容
  - Opus 版本的 MMMU 得分为 59.4%，超过 GPT-4V，与 Gemini  1.0 Ultra 持平）。用户现在可以上传照片、图表、文档和其他类型的非结构化数据，让 AI 进行分析和解答。
- Claude3 是一组模型：`Haiku`(小杯)、`Sonnet`（中杯） 和 `Opus`（大杯），让企业客户根据自身场景选择不同性能、不同成本的版本。
  - Sonnet 的速度比 Claude 2 和 Claude 2.1 快 2 倍，且智能水平更高。
  - ![](https://imgslim.geekpark.net/uploads/image/file/5e/5f/5e5f63e4a03388887f3d3719956dc65e.png)
- Anthropic 强调自家模型是最安全。Anthropic 总裁 Daniela Amodei 介绍，在 Claude3 的训练中引入了一种叫做「宪法人工智能」的技术，增强其安全、可信、可靠。
- 但目前方法可能无法实现**完全**无偏见的人工智能。
  - 「创建一个完全中立的生成式人工智能工具几乎是不可能的，不仅在技术上，而且还因为并不是每个人都同意什么是中立。」

效果：
- 能力最强的 `Opus` 在多项基准测试中得分都超过了 `GPT-4` 和 `Gemini 1.0 Ultra`，在数学、编程、多语言理解、视觉等多个维度树立了新的行业基准。
- 排行榜: [LMSYS Chatbot Arena Leaderboard](https://chat.lmsys.org/)
- Claude 3 Opus 拥有人类本科生水平的知识
- ![](https://image.jiqizhixin.com/uploads/editor/cf8e07d3-f981-4c84-9ab4-a182179c5971/640.png)


Anthropic 访问
- [claude](https://claude.ai), [Claude Chat](https://claude.ai/chats)，需要国外手机号注册，免费版只支持 sonnet
- 免费渠道
  - [Chatbot Arena](https://chat.lmsys.org/), direct chat 区，支持 sonnet 和 opus(claude-3-opus-20240229), 另外还支持其他主流模型
- 159 个国家开放使用 Claude3 系列的两款模型（Opus 和 Sonnet），最强版本 Haiku 也即将推出。
- 同时，Anthropic 也通过**亚马逊**和**谷歌**的云平台提供服务，后者曾分别向 Anthropic 注资 40 亿美元和 20 亿美元。
- 【2024-3-7】接码平台虚拟手机号失败，改用美国真实号码，成功


定价
- 能力最强的 Claude 3 也比 GPT-4 Turbo 要贵得多：
  - GPT-4 Turbo 每百万 token 输入 / 输出收费为 **10/30** 美元 ；
  - 而 Claude 3 Opus 为 **15/75** 美元。

42 页的技术报告
- 《[The Claude 3 Model Family: Opus, Sonnet, Haiku](https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf)》
- [claude-3-family](https://www.anthropic.com/news/claude-3-family)

参考
- [刚刚曝光的 Claude3，直击 OpenAI 最大弱点](https://www.geekpark.net/news/331955)
- [GPT-4时代已过？全球网友实测Claude 3，只有震撼](https://www.jiqizhixin.com/articles/2024-03-05-4)

### TruthGPT

【2023-4-19】马斯克推出[TruthGPT](https://talk.truthgpt.one/)上线了，不用翻墙，不用注册直接可用
- TruthGPT支持中文及多种语言
- 在对话框最下面，有两种模式，分别是question mode和chat mode，需要注意 question mode不支持**对话记忆**功能。
- ![](https://pic2.zhimg.com/80/v2-9a667e046f0dc1780f6dc3e9f0645d8d_1440w.webp)

测试：
- 写个朋友圈二手房营销文案，要求不超过100字，突出房源重点，降价/急售/上新，三个主题选一个，带emoji表情，房源信息如下：育新东里二里，靠近西三旗商圈，89平米，海淀六小强学区，满五年，2000年

> 🔥🔥🔥火热推荐！育新东里二里，89平米，海淀六小强学区，满五年，2000年，靠近西三旗商圈，急售！仅需要你的一份心意，就可以拥有这栋梦想家园！快来看看吧！

- 写3个朋友圈二手房营销文案，要求不超过100字，突出房源重点，降价/急售/上新，带emoji表情，房源信息如下：育新东里二里，靠近西三旗商圈，89平米，海淀六小强学区，满五年，2000年的房子，户型东

> 🔥🔥🔥火热推荐！育新东里二里，89平米，海淀六小强学区，满五年，2000年，靠近西三旗商圈，户型东，降价急售！仅需要你的一份心意，就可以拥有这栋梦想家园！快来看看吧！🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩

### 出门问问: 奇妙文

出门问问推出的聊天机器人：[奇妙文](https://wen.moyin.com/)

### StableLM

【2023-4-20】[Stability开源类ChatGPT模型](https://zhuanlan.zhihu.com/p/623561495)！上线14小时，狂揽超4.8k星，支持商业化

AI图像生成工具Stable Diffusion的初创公司Stability AI发布并开源该团队训练的大语言模型StableLM。
- 该模型的Alpha版本有30亿和70亿个参数，接下来还将推出150亿至650亿参数的模型。用户已经可以从GitHub等开源平台上下载StableLM。
- StableLM已展示出日常聊天、书信撰写、小说创作、代码编写等功能

### HuggingChat

【2023-4-27】最大开源社区 Hugging Face 发布了 HuggingChat，有 300 亿参数。[详情](https://www.ithome.com/0/689/379.htm)
- 既开源，还免费，互联网上随随便便就能用。 [网址](hf.co/chat)
- [huggingchat](https://huggingface.co/spaces/huggingchat/chat-ui)


### 星火 -- 科大讯飞

【2023-5-6】科大讯飞大模型[发布](https://xinghuo.xfyun.cn/)，亲测效果还不错

### PKU-Beaver（河狸）-- RLHF

【2023-5-18】北京大学团队开源了名为 [PKU-Beaver（河狸）](https://pku-beaver.github.io/) 项目[github](https://github.com/PKU-Alignment/safe-rlhf), 首次公开了 RLHF 所需的数据集、训练和验证代码，是目前首个开源的可复现的 RLHF 基准

北大开源国内首个可复现的 RLHF 基准 PKU-Beaver（河狸），覆盖三步流程，以及评估，首次提出了带有约束的价值对齐技术 CVA（Constrained Value Alignment），Safe RLHF。
- GPT-4 评估 Beaver 安全性比 Alpaca更好。开源包含安全偏好的多轮RLHF数据集PKU-SafeRLHF-Datasets，规模达到100万条，涉及侮辱、歧视、犯罪、心理伤害、悲观情绪、色情、隐私等十余种维度的约束

|                                                                                                          |  SFT  | Preference Model | RLHF  | Safe-RLHF | PTX Loss | Evaluation |      Backend      |
| -------------------------------------------------------------------------------------------------------- | :---: | :--------------: | :---: | :-------: | :------: | :--------: | :---------------: |
| [Beaver](https://github.com/PKU-Alignment/safe-rlhf)</br>(Safe-RLHF)  |   ✔️ |   ✔️  |   ✔️   |  ✔️  | ✔️  | ✔️ |  DeepSpeed |
| [trlX](https://github.com/CarperAI/trlx)  |  ✔️ |  ❌ |   ✔️   |   ❌   |   ❌  |  ❌  | Accelerate / NeMo |
| [DeepSpeed-Chat](https://github.com/microsoft/DeepSpeedExamples/tree/master/applications/DeepSpeed-Chat) |   ✔️   |        ✔️         |   ✔️   |     ❌     |    ✔️     |     ❌      |  DeepSpeed  |
| [Colossal-AI](https://github.com/hpcaitech/ColossalAI)  |   ✔️   |  ✔️  |   ✔️   |  ❌   |  ✔️   |  ❌  |  ColossalAI |


为解决人类标注产生的**偏见和歧视**等不安全因素，北京大学团队首次提出了带有**约束**的价值对齐技术 `CVA`（Constrained Value Alignment）。
- 通过对标注信息进行细粒度划分，并结合带约束的安全强化学习方法，显著降低了模型的偏见和歧视，提高了模型的安全性。
- Beaver使用GPT4进行Evaluation，结果表明，在原有性能保持不变的情况下，Beaver回复的安全性大幅度提升。

开源的内容包括
- （一）、数据集与模型：PKU-SafeRLHF
  1. 开源迄今为止最大的多轮 RLHF 数据集，规模达到 100 万条。
  2. 开源经 Safe-RLHF 对齐训练得到的 7B 参数的语言模型——Beaver，并支持在线部署。
  3. 开源了预训练的Reward Model和Cost Model的模型和参数。
- （二）、首个可复现的RLHF基准，PKU-Alignment/safe-rlhf支持以下功能：
  1. 支持LLM 模型的 SFT（Supervised Fine-Tuning）、RLHF训练、Safe RLHF训练。支持目前主流的预训练模型如 LLaMA、OPT 等模型的训练。
  2. 支持 Reward Model 和 Cost Model 训练。
  3. 提供安全约束满足的多尺度验证方式，支持 BIG-bench、GPT-4 Evaluation 等。
  4. 支持参数定制化的 RLHF 和数据集定制接口。

【2023-7-30】[safe_rlhf/models/pretrained.py#L122](https://github.com/PKU-Alignment/safe-rlhf/blob/main/safe_rlhf/models/pretrained.py#L122)
- end_scores 源自何处？huggingface transformers没找到 -- 

```py
        logits = self.actor_model(sequence, attention_mask=attention_mask).logits
        ref_logits = self.actor_reference_model(sequence, attention_mask=attention_mask).logits

        reward_score = self.reward_model(
            reward_seq,
            attention_mask=reward_attention_mask,
        ).end_scores
        reward_value = self.reward_critic_model(
            sequence,
            attention_mask=attention_mask,
        ).scores
```

end_score非transformers自带属性，是safe_rlhf自定义
- [models/score_model/gpt2/modeling_gpt2.py](https://github.com/PKU-Alignment/safe-rlhf/blob/main/safe_rlhf/models/score_model/gpt2/modeling_gpt2.py)

```py
from safe_rlhf.models.score_model import ScoreModelOutput

class GPT2ForScore(GPT2PreTrainedModel):

        scores = self.score_head(hidden_states)  # size = (B, L, D)

        end_scores = []
        for i in range(input_ids.size(0)):
            end_index = attention_mask[i].nonzero()[-1].item()
            end_scores.append(scores[i, end_index])  # size = (D,)
        end_scores = torch.stack(end_scores, dim=0)  # size = (B, D)

        if not return_dict:
            return scores, end_scores

        return ScoreModelOutput(
            scores=scores,  # size = (B, L, D)
            end_scores=end_scores,  # size = (B, D)
```

### BLOOMChat

【2023-5-22】[BLOOMChat: 开源可商用支持多语言的大语言模型](https://zhuanlan.zhihu.com/p/631036519)
- 2023.05.19, SambaNova和Together 开源了可商用的支持多语言的微调模型 BLOOMChat。huggingface [demo](https://huggingface.co/spaces/sambanovasystems/BLOOMChat)

国内很多企业和公司也在调研如何基于开源模型进行微调，打造一个支持中文的大语言模型，应用到自己的业务场景里。
- 由BigScience开源的Bloom基座模型是很多互联网公司的首选
- 因为这个模型可商用，支持包括中文在内的46种语言，而且模型参数够多，有1760亿参数。
- 有些公司直接拿基于Bloom做过微调后的Bloomz模型，来进一步微调，打造一个垂直领域的LLM。

Bloom 是用于自然语言处理的大语言模型，包含 1760 亿个参数，支持 46 种自然语言（包括中文）和 13 种编程语言，可以用来回答问题、翻译文本、从文件中提取信息片段，还能像 GitHub Copilot 一样用于生成代码。

BLOOM 模型的最大优势是它的易获取性，任何个人或机构都可以从 Hugging Face 免费获得 1760 亿个参数的完整模型。用户有多个语种可选，然后将需求输入到 BLOOM 中，任务类型包括撰写食谱或诗歌、翻译或总结文本，甚至还有代码编程。人工智能开发者可以在该模型的基础上构建他们自己的应用程序。

SambaNova和Together联合开源的BLOOMChat，其目的就是打造一个开源的、支持**多语言**、可商用的聊天LLM，实验表明BLOOMChat对多语言的支持明显优于其它开源模型。
- BLOOMChat使用了包括OpenChatKit的OIG、Dolly 2.0和OASST1数据集在内的以英语为主的对话数据集来进行BLOOM（176B）的模型微调。

BLOOMChat微调的指令数据有2类。
- 第一种，程序自动合成的对话数据集OpenChatKit，数据量大。OpenChatKit训练数据集就是由Together公司联合LAION和Ontocord开源出来的。
- 第二种，人工写出来的高质量问答数据集Dolly 2.0和OASST1，数据量小。

GPT-4在评测记录中，55%的评测记录是优于BLOOMChat的

BLOOMChat 是一个新的、开放的、多语言的聊天 LLM。
- SambaNova 和 Together 使用 SambaNova 独特的可重构数据流架构在 SambaNova DataScale 系统上训练了 BLOOMChat；
- 建立在 BigScience 组织的 BLOOM 之上，并在 OpenChatKit、Dolly 2.0 和 OASST1 的 OIG 上进行了微调。

### 360智脑

【2023-5-23】[迭代后首波实测！360智脑一键联网，代码超强，AI诈骗一眼看穿](https://mp.weixin.qq.com/s/sBmmeMJMgnWIoJLXa3Aimw), 可以识别诈骗、作图(「360 鸿图」)、联网。[360智脑](https://ai.360.cn/)
- ![](https://image.jiqizhixin.com/uploads/editor/502667cf-151e-4fa7-8cd4-85c0979a5092/640.gif)
- [详细测完360智脑后，我们发现大模型终于被玩明白了](https://www.jiqizhixin.com/articles/2023-05-23-2)


### 人大：玉兰 YuLan-Chat（LLaMA）

【2023-6-8】[YuLan-Chat：基于高质量中英文混合指令微调的大语言对话模型](https://mp.weixin.qq.com/s/4pk4vHzAf_kiXYWT-abLlg)
> 主要靠构造高质量中英文混合数据集，在2台GPU机器上，对 LLaMA上只做SFT训练，就取得了好成绩：超过vicuna-13b和ChatGLM-6B。

中国人民大学高瓴人工智能学院相关研究团队（由多位学院老师联合指导）展开了一系列关于指令微调技术的研究，并发布了学院初版大语言对话模型——[YuLan-Chat](https://github.com/RUC-GSAI/YuLan-Chat)，旨在探索和提升大语言模型的中英文双语对话能力。
- 开源了13B和65B的YuLan-Chat模型文件及相关代码，并采用量化技术使其分别可以在单张RTX3090-24G和A800-80G显卡上部署。
- [YuLan-Chat](https://github.com/RUC-GSAI/YuLan-Chat) 模型基于LLaMA底座模型，采用精心优化的高质量中英文混合指令进行微调，其中YuLan-Chat-65B模型目前能够在中英文相关评测数据集上显著超越已有开源模型效果

问题
- 现有方法往往依赖于
  - Self-Instruct方法让大模型自动生成指令
  - 直接收集和爬取已有的指令或对话数据
- 导致很难对数据质量进行监督与控制，且难以保证指令数据的多样性和难度，可能反而导致大模型过拟合到这批指令数据上

基于已有开源指令数据，采用了基于**主题控制**的多阶段指令筛选、复杂化、多样化方法，按照以下三个阶段优化：
- A. 基于语义相似度模型的开源指令去重
- B. 基于主题控制的指令多样化
  - 越多样的指令越能增强模型的各项能力，且防止模型出现“偏科”
  - 基于聊天社区内收集若干主题，包含15个大类（如商业和艺术）和293个子类（如比特币和流行音乐）
  - 用ChatGPT改写，既能与该主题内容相关，同时尽量保留原始的指令内容；
  - 部分英文指令数据翻译为中文
- C. 指令数据复杂化。两种复杂化方式，即：
  1. 将简单指令改写为**复杂**指令；
    - 从知识的深度和广度两方面，分别对当前指令进行改写，使其聚焦于该领域内更细节的知识点或覆盖其他相关领域知识
  2. 将单轮指令数据扩充为**多轮**对话形式。构造出信息量丰富且复杂的多轮对话数据
    - 针对指令回复的结果，使用ChatGPT提出专业问题

最终得到共**25万**条指令
- 9万中文 和 9万英文多轮对话数据
- 通过将其与7万ShareGPT真实对话数据混合，得到最终的指令微调数据集。

训练
- 对13B/65B的LLaMA模型进行**全参数微调**
- 并基于DeepSpeed库，使用**数据并行**，ZERO与FlashAttention技术
- 在2台8卡A800-80G的GPU服务器上进行**多机多卡**训练。

针对多轮对话数据，效仿Vicuna，在计算**损失函数**时采用特殊的**掩码机制**
- 将多轮对话数据拼接为一长句子，然后仅对需要模型生成的文字部分计算损失值。

这样降低拆分对话导致的计算开销增加，保证较低的训练成本。

推理
- 采用int8量化技术，使训练后的模型在单张GPU上推理，且精度基本不变。
- 其中65B和13B模型可以分别在 A800-80G和 RTX3090-24G 显卡上部署。

评测
- 中英文两种场景下，分别选择两个基准数据集合，对 YuLan-Chat 模型和其他大语言对话模型进行对比。
- 主要与公认较强的 Vicuna-13B、MOSS、ChatGLM 模型进行对比，并同时报告了OpenAI的闭源模型Text-Davinci-003和ChatGPT模型的效果。

YuLan-Chat-65B 模型在所有开源模型中取得最好的效果，这不仅因为其较大的参数量，且其采用了更高质量的指令进行微调。
- 中文高考数据集
- 英文BBH3K数据集

### Grace Bot

【2023-6-9】[Grace Bot](https://www.gracebot.cn/chat)

[据传](https://maimai.cn/web/feed_detail?efid=X8x77rUFfICAx5mC8ouhoQ&fid=1790257046&id=1790257046&operation_id=MUWVJjyN0JQJwzokkkkb0&share_channel=2&share_uid=3539&use_rn=1)字节大模型的进展：
- 1、字节相关部门去年12月成立，主要做**GPT系列**模型的复现。
  - 目前基于GPT2.0开源模型，试了三个多月，预计6-9月会有预训练语言模型出来。
- 2、语料库:目前涉及语言数据，如头条自有数据、抖音评论、电子图书(版权采买)、互联网爬取以及外文维基百科数据等。
- 3、在**多模态**场景下，图片、视频等相关应用可能会更多，对于字节来说这部分数据有比较优势，将来的落地点会有很多。

### FATE-LLM（联邦学习）

【2023-6-6】FATE 开源社区（杨强）发布FATE-LLM 新版本，支持中文大语言模型 ChatGLM-6B 联邦化训练。[资讯](https://www.infoq.cn/article/8zfeEZcsDD7JSBLZYg6j)
- 联邦大模型功能模块，以联邦学习+大模型的技术解决方案破局数据隐私保护与数据不足等问题，以应对行业发展的新挑战。
- 横向联邦场景支持 ChatGLM-6B 中文语言大模型。集成 GLM 的 FATE-LLM 将会为国内用户提供更好的中文大模型应用落地选择。
- [项目地址](https://github.com/FederatedAI/FATE-LLM/releases/tag/v1.1.0)

**横向联邦**场景支持 Adapter，Prompt 这类高效聚合方法，可以显著提升联邦大模型训练效率，其中参数微调方法支持 Lora 以及 P-Tuning V2 。
- 框架层，FATE 实现对 DeepSpeed 的集成，使得 FATE-LLM 支持多机多卡训练，支持分布式 GPU 集群资源调度和管理，支持数据、模型参数等不同并行化加速方法。用户只需要任务提交阶段直接增加配置即可享受到多机多卡的加速能力。

### 智源：Aqulia天鹰

【2023-6-12】Aqulia天鹰发布：GIThub上下载flagAI（包含很多东东），其中模型文件需要再官网上下载
- 中英文、可商用、数据合规
- 文档Aqulia-7B需要Nvidia-A100，将在RTX4090上试试Aqulia-7B能否跑起来。
- 详见：[2023北京智源大会笔记](https://zhuanlan.zhihu.com/p/636413731)

【2023-6-28】[天鹰AquilaChat-7B VS ChatGLM-6B对比](https://mp.weixin.qq.com/s/DsGXzBMNTGaLoRNTMV6aVw)

测试内容从自我认知、提纲写作、文案写作、邮件写作助手、信息抽取、角色扮演、评论比较和旅游向导这八个角度进行测试对比。

核心结论：
- 1、关于自我认知、提纲写作方面，ChatGLM-6B相比天鹰AquilaChat-7B要好一些，优点和缺点条例比较清晰；
- 2、在文案写作方面，两个模型都表现不错，ChatGLM-6B生成的10个新闻进行了换行，而天鹰AquilaChat-7B没有换行；
- 3、在写邮件方面，天鹰AquilaChat-7B格式上欠佳，缺少发件人占位符；
- 4、在信息抽取方面，天鹰AquilaChat-7B比ChatGLM-6B略胜一筹，提取的信息更全面；
- 5、在角色扮演方面，天鹰AquilaChat-7B要差很多，而且还生成了无意义的“啊”；
- 6、在主观评论方面，ChatGLM-6B和天鹰AquilaChat-7B都表现的比较理智和客观，没有模型个人观点；
- 7、在旅游向导方面，两个模型表现都不错，ChatGLM-6B条理清晰，而天鹰AquilaChat-7B缺少条理

综述所述，在 ChatGLM-6B 给出的8大示例中，明显是ChatGLM-6B占上风，这似乎也不太公平，后面会使用其他的Prompt再进行测试对比实验。


### ChatRWKV -- RNN, 长文本

【2023-3-13】[开源1.5/3/7B中文小说模型：显存3G就能跑7B模型，几行代码即可调用](https://zhuanlan.zhihu.com/p/609154637)
- 1.5/3/7B中文小说模型，可以开源下载
- 纯 RNN 实现

[ChatRWKV](https://github.com/BlinkDL/ChatRWKV) is like ChatGPT but powered by RWKV (100% RNN) language model, and open source.
- [RWKV-CHN](https://modelscope.cn/studios/BlinkDL/RWKV-CHN/summary) 在线体验

RWKV 是结合了 RNN 和 Transformer 的语言模型，适合**长文本**，运行速度较快，拟合性能较好，占用显存较少，训练用时较少。

RWKV 整体结构依然采用 Transformer Block 的思路
- 相较于原始 Transformer Block 的结构，RWKV 将 self-attention 替换为 Position Encoding 和 TimeMix，将 FFN 替换为 ChannelMix。其余部分与 Transfomer 一致。


RWKV原理见专题：[RWKV](/transformer#RWKV)

### 微软-Orca（虎鲸）

【2023-6-5】微软发布130亿参数模型Orca，表现比ChatGPT好。

微软日前发布一款130亿参数的语言模型 `Orca`（虎鲸）
- 基准测试中赢过主流大型基础模型，像是`ChatGPT`、`Bard`，以及同参数量的`Vicuna-13B`、`Alpaca-13B`和`LLaMA-13B`等模型。
- 微软想通过学习、模仿大型语言模型的**推理过程**，来提高小模型表现，于是，以GPT-4为标杆，让Orca学习GPT-4的推理过程，包括**解释**步骤、**逐步**（Step by step）思考模式和其他复杂指令，并由ChatGPT模型来引导。
- 论文: [Orca: Progressive Learning from Complex Explanation Traces of GPT-4](https://arxiv.org/pdf/2306.02707.pdf)

测试时，团队以GPT-4作为评分工具，来衡量Orca在严格的基准测试Big Bench Hard（BBH）中与其他SOTA模型的表现，发现比ChatGPT、Bard等要好，也在包含SAT、LSAT、GRE和GMAT等学术考试的AGIEval基准测试中，拿下不错成绩。

### 百川智能(LLaMA改进) -- 可商用

[百川智能](https://www.baichuan-ai.com/home)

详见站内专题:[Baichuan](baichuan)

### 紫东太初2.0 -- 中科院

【2023-6-16】[中科院：自主研制新一代人工智能大模型问世](https://www.toutiao.com/article/7245117681786208826)

中国科学院自动化研究所在上海发布了该所研制的新一代人工智能大模型——`紫东太初2.0`。全新大模型相比第一代着力提升了决策与判断能力，实现了从感知、认知到决策的跨越，未来将在医疗、交通、工业生产等领域发挥更大作用。

作为我国首个存储千亿参数的图文音三模态大模型，第一代紫东太初人工智能大模型在2021年问世时实现了无标识的图像、文字、语音的识别能力，这次发布的新一代大模型则升级融入了视频、传感信号、3D点云等识别能力，突破了多模态分组认知编码、解码，全模态认知等关键技术，提升了系统的决策和判断能力，打通了系统识别能力从感知、认知到决策的通路，从而拓展出更为广泛的应用场景。目前，紫东太初大模型已经在神经外科手术导航、短视频内容审核、医疗多模态鉴别诊断、交通违规图像研读等多领域应用。


### 书生·浦语

[InternLM](https://internlm.org/) 是[上海人工智能实验室](https://www.shlab.org.cn/)开源的轻量级训练框架，旨在支持大模型训练而无需大量的依赖。


#### InternLM 1

- 通过单一的代码库，支持在拥有数千个 GPU 的大型集群上进行预训练，并在单个 GPU 上进行微调，同时实现了卓越的性能优化。
- 在1024个 GPU 上训练时，InternLM 可以实现近90%的加速效率。
- [InternLM](https://github.com/InternLM/InternLM/tree/main)

基于InternLM训练框架，我们已经发布了两个开源的预训练模型：InternLM-7B 和 InternLM-20B。
- 2023-09-20 InternLM-20B 已发布，包括基础版和对话版。
- 2023-08-22 InternLM-7B-Chat v1.1 已发布，增加了代码解释器和函数调用能力


#### InternLM 2 书生-浦语


【2024-1-31】InternLM2 系列模型发布，具有如下特性：[书生官方中文介绍](https://github.com/InternLM/InternLM/blob/main/README_zh-CN.md)
- 有效支持20万字超长上下文：模型在 20 万字长输入中几乎完美地实现长文“大海捞针”，而且在 LongBench 和 L-Eval 等长文任务中的表现也达到开源模型中的领先水平。 可以通过 LMDeploy 尝试20万字超长上下文推理。
- 综合性能全面提升：各能力维度相比上一代模型全面进步，在推理、数学、代码、对话体验、指令遵循和创意写作等方面的能力提升尤为显著，综合性能达到同量级开源模型的领先水平，在重点能力评测上 InternLM2-Chat-20B 能比肩甚至超越 ChatGPT （GPT-3.5）。
- 代码解释器与数据分析：在配合代码解释器（code-interpreter）的条件下，InternLM2-Chat-20B 在 GSM8K 和 MATH 上可以达到和 GPT-4 相仿的水平。基于在数理和工具方面强大的基础能力，InternLM2-Chat 提供了实用的数据分析能力。
- 工具调用能力整体升级：基于更强和更具有泛化性的指令理解、工具筛选与结果反思等能力，新版模型可以更可靠地支持复杂智能体的搭建，支持对工具进行有效的多轮调用，完成较复杂的任务。可以查看更多样例。

中英文评测上，指标优于 GPT-3.5
- 除了使用学术数据集评测以外，还用了人类考试作为评测基准。
- InternLM 可以在 MMLU、AGIEval、C-Eval 以及 GAOKAO-bench 等涵盖了不同语言以及学科的考试基准集上取得不错的分数，在多个基准集得分超过 ChatGPT


InternLM2 包含两种模型规格：**7B** 和 **20B**。
- 7B 为轻量级的研究和应用提供了一个轻便但性能不俗的模型
- 20B 模型的综合性能更为强劲，可以有效支持更加复杂的实用场景。

每个规格不同模型关系如图所示：
- ![](https://camo.githubusercontent.com/740bc4d1b7d9cd211c2f03918c46ff891836de0fc131bf44eb0d8fdd2ab4066a/68747470733a2f2f696e7465726e6c6d2e6f73732d636e2d7368616e676861692e616c6979756e63732e636f6d2f7365726965732e706e67)

- `InternLM2-Base`：高质量和具有很强可塑性的模型基座，是模型进行深度领域适配的高质量起点。
- `InternLM2`：大规模无标签数据上继续预训练，并结合特定领域的增强语料库进行训练，在评测中成绩优异，同时保持了很好的通用语言能力，是我们推荐的在大部分应用中考虑选用的优秀基座。
- `InternLM2-Chat-SFT`: 基于 `InternLM2-Base` 模型进行有监督微调(SFT)，是 `InternLM2-Chat` 模型的**中间版本**。将它们开源以助力社区在对齐方面的研究。
- `InternLM2-Chat`: 在 `InternLM2-Chat-SFT` 基础上进行 online RLHF 以进一步对齐. `InternLM2-Chat` 面向对话交互进行了优化，具有较好的指令遵循、共情聊天和调用工具等的能力，是我们推荐直接用于下游应用的模型。

transformers 加载

```py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
# transformers >= 4.34

tokenizer = AutoTokenizer.from_pretrained("internlm/internlm2-chat-7b", trust_remote_code=True)
# 设置`torch_dtype=torch.float16`来将模型精度指定为torch.float16，否则可能会因为您的硬件原因造成显存不足的问题。
model = AutoModelForCausalLM.from_pretrained("internlm/internlm2-chat-7b", device_map="auto",trust_remote_code=True, torch_dtype=torch.float16)
# (可选) 如果在低资源设备上，可以通过bitsandbytes加载4-bit或8-bit量化的模型，进一步节省GPU显存.
  # 4-bit 量化的 InternLM 7B 大约会消耗 8GB 显存.
  # pip install -U bitsandbytes
  # 8-bit: model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True, load_in_8bit=True)
  # 4-bit: model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True, load_in_4bit=True)
model = model.eval()
response, history = model.chat(tokenizer, "你好", history=[])
print(response)
# 模型输出：你好！有什么我可以帮助你的吗？
response, history = model.chat(tokenizer, "请提供三个管理时间的建议。", history=history)
print(response)
```

启动一个前端的界面来与 InternLM Chat 7B 模型进行交互

```sh
pip install streamlit
pip install transformers>=4.34
streamlit run ./chat/web_demo.py
```

用 LMDeploy 完成 InternLM 的一键部署。

通过 `pip install lmdeploy>=0.2.1` 安装 LMDeploy 之后，只需 4 行代码，就可以实现离线批处理：

```py
from lmdeploy import pipeline
pipe = pipeline("internlm/internlm2-chat-7b")
response = pipe(["Hi, pls intro yourself", "Shanghai is"])
print(response)
```


#### InternLM-XComposer2

【224-1-29】[internlm-xcomposer2-vl-7b](https://huggingface.co/internlm/internlm-xcomposer2-vl-7b)
- paper [InternLM-XComposer2: Mastering Free-form Text-Image Composition and Comprehension in Vision-Language Large Model](https://arxiv.org/abs/2401.16420)

```py
import torch
from transformers import AutoModel, AutoTokenizer

torch.set_grad_enabled(False)

# init model and tokenizer
model = AutoModel.from_pretrained('internlm/internlm-xcomposer2-vl-7b', trust_remote_code=True).cuda().eval()
tokenizer = AutoTokenizer.from_pretrained('internlm/internlm-xcomposer2-vl-7b', trust_remote_code=True)

query = '<ImageHere>Please describe this image in detail.'
image = './image1.webp'
with torch.cuda.amp.autocast():
  response, _ = model.chat(tokenizer, query=query, image=image, history=[], do_sample=False)
print(response)
#The image features a quote by Oscar Wilde, "Live life with no excuses, travel with no regret,"
# set against a backdrop of a breathtaking sunset. The sky is painted in hues of pink and orange,
# creating a serene atmosphere. Two silhouetted figures stand on a cliff, overlooking the horizon.
# They appear to be hiking or exploring, embodying the essence of the quote.
# The overall scene conveys a sense of adventure and freedom, encouraging viewers to embrace life without hesitation or regrets.

```

### Kimi Chat -- 月之暗面

【2023-10-11】[Moonshot AI大模型服务Kimi Chat开始内测，火山引擎提供训练推理加速解决方案](https://mp.weixin.qq.com/s/aV7Vx8k37txwCmG_4VNilw)

10月9日，北京`月之暗面`科技有限公司(Moonshot AI, 杨植麟)宣布在“长文本”领域实现了突破，推出了首个支持输入20万汉字的智能助手产品`Kimi Chat`。这是目前全球市场上能够产品化使用的大模型服务中所能支持的**最长**上下文输入长度，标志着Moonshot AI在这一重要技术上取得了世界领先水平。

火山引擎与Moonshot AI深度合作，为其独家提供高稳定性和高性价比的AI训练和推理加速解决方案，双方联合进行技术研发，共同推进大型语言模型在垂直领域和通用场景的应用落地。同时，Kimi Chat即将入驻火山引擎大模型服务平台——火山方舟，双方将持续在大模型生态领域为企业和消费者提供更丰富的AI应用。

相比当前市面上以英文为基础训练的大模型服务，`Kimi Chat`具备较强的多语言能力，例如，Kimi Chat在中文上具备显著优势，实际使用效果能够支持约20万汉字的上下文，2.5倍于Anthropic公司的Claude-100k（实测约8万字），8倍于OpenAI公司的GPT-4-32k（实测约2.5万字）。同时，Kimi Chat能够通过创新的网络结构和工程优化，在千亿参数下实现了无损的长程注意力机制，不依赖于滑动窗口、降采样、小模型等对性能损害较大的“捷径”方案。

Moonshot AI创始人杨植麟此前在接受采访时曾表示，无论是文字、语音还是视频，对海量数据的无损压缩可以实现高程度的智能。大模型的能力上限（即无损压缩比）是由单步能力和执行的步骤数共同决定的，前者与参数量相关，后者即上下文长度。




### vLLM -- 伯克利推理

【2023-6-21】[比HuggingFace快24倍！伯克利LLM推理系统开源碾压SOTA，GPU砍半](https://www.toutiao.com/article/7247011018936271418)

UC伯克利重磅开源神级LLM推理和服务系统——`vLLM`，利用PagedAttention，比HuggingFace/Transformers快24倍，GPU数量减半。
- UC伯克利研究人员几个月前给大语言模型们安排了一个擂台——Chatbot Arena。

全新算法的[vLLM](https://github.com/vllm-project/vllm)，重新定义了LLM服务的最新技术水平,性能全面碾压SOTA：
- 与HuggingFace Transformers相比，它提供高达24倍的吞吐量，而无需进行任何模型架构更改。
- NVIDIA A10G GPU上运行LLaMA-7B模型，在NVIDIA A100 GPU（40GB）上运行LLaMA-13B模型。
- 研究人员从ShareGPT数据集中抽样请求的输入/输出长度。实验中，vLLM的吞吐量比HF高达**24倍**，并且比TGI高达**3.5倍**。

值得一提的是，「小羊驼」Vicuna在demo中用到的就是FastChat和vLLM的一个集成。

正如研究者所称，vLLM最大的优势在于——提供易用、快速、便宜的LLM服务。

这意味着，未来，即使对于像LMSYS这样计算资源有限的小型研究团队也能轻松部署自己的LLM服务。

秘密武器：**PagedAttention**

在vLLM中，团队发现LLM服务的性能受到**内存**限制。

自回归解码过程中，LLM所有输入token都会生成**注意力**键（key）和值（value）张量，并且这些张量被保留在GPU内存中以生成下一个token。这些缓存的键和值张量通常被称为**KV缓存**。KV缓存具有以下特点：
1. 内存占用大：在LLaMA-13B中，单个序列的KV缓存占用高达1.7GB的内存。
2. 动态化：其大小取决于序列长度，而序列长度高度易变，且不可预测。

因此，有效管理KV缓存是一个重大挑战。对此，研究团队发现现有系统由于碎片化和过度保留而浪费了60%至80%的内存。
> GPU内存碎片化=慢。

为了解决这个问题，团队引入了 PagedAttention，一种受到操作系统中虚拟内存和分页经典概念启发的注意力算法。

与传统的注意力算法不同，PagedAttention允许在非连续的内存空间中存储连续的键和值。
- PagedAttention将每个序列的KV缓存分为若干块，每个块包含固定数量token的键和值。在注意力计算过程中，PagedAttention内核能够高效地识别和提取这些块。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/100e44e8db0646cd94237948ef3f621f~noop.image)
- 详见[原文](https://www.toutiao.com/article/7247011018936271418)

### Web LLM —— 浏览器

Web LLM 是一个可将大型语言模型和基于 LLM 的聊天机器人引入 Web 浏览器的项目。一切都在浏览器内运行，无需服务器支持，并使用 WebGPU 加速。这开辟了许多有趣的机会，可以为每个人构建 AI 助手，并在享受 GPU 加速的同时实现隐私。



### 【谷歌】Gemini

【2023-12-6】Google 正式推出了原生多模态的大型语言模型Gemini，可以同时支持文字、图片和声音的输入。
- [gemini](https://deepmind.google/technologies/gemini/#introduction)

在32项AI测试中，有30项的评分超越了OpenAI的GPT-4。Google CEO Sundar Pichai强调，Gemini是Google有史以来最强大也是最通用的模型。

Gemini模型经过海量数据训练，可以很好识别和理解文本、图像、音频等内容，并可以回答复杂主题相关的问题。所以，非常擅长解释数学和物理等复杂学科的推理任务。

<iframe width="560" height="315" src="https://www.youtube.com/embed/JPwU1FNhMOA?si=85W6sLiefLH3cOfi" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

【2023-12-14】谷歌宣布，**免费**开放`Gemini Pro`和`Gemini Pro Vision`的**API**，支持中文。每分钟可发出**60**个请求，将比其他免费产品高20倍。
- [bard体验地址](https://bard.google.com)，gemini加持的是英文版的bard，用中文就不是gemini
- [api](https://makersuite.google.com/app/apikey)

### NexusRaven

【2023-12-23】[清华特奖焦剑涛大模型创业：突破GPT-4工具使用能力，搞开源种子轮融资七千万](https://mp.weixin.qq.com/s/twShew3e_jgJg6IqUIOZow)

两位清华校友打造NexusRaven, 13b，在GPT-4核心优势之一使用工具上实现超越。

2023年9月,公司 Nexusflow 刚刚亮相，并当即宣布千万美元级种子轮融资。
- 短短不到3个月时间就发布了2代大模型 NexusRaven，其中第二代直接单点突破GPT-4，引起开源社区大量关注。

NexusRaven 开源和商用，完全不用担心侵权，因为训练不涉及任何由专有LLM(如GPT-4) 生成的数据。

当然，隐私数据就更不用担心了，NexusRaven称自己的安全性比GPT-4要高了21个百分点。

NexusRaven-V2完全基于开放数据集打造，并在CodeLlama-13B-instruct上进行了指令微调。
- 问题 “Get me good food nearby?”
- 立刻编写出几行代码，然后开始定位你的城市、将城市坐标转换为经纬度、领取目标任务（20个饭店建议）以及按距离从远到近排序。

人工生成的9项基准测试中，只有130亿参数的NexusRaven-V2做到了58.2%的平均调用成功率，比GPT-4高出4个百分点（在零样本情况下）。

其中，两者在单个或并行函数调用这种简单任务上的表现差不多。

但如果再单看复杂的嵌套函数调用任务，NexusRaven-V2的成绩比GPT-4表现得要更好，直接高出了7个百分点。

### Inflection-2.5

【2024-3-7】美国 AI 创业公司 [Inflection AI](https://inflection.ai) 正式发布新一代大语言模型 Inflection-2.5, 包含Web（[Pi](https://pi.ai/talk)）、[客户端](https://pi.ai/desktop)和App。
- 官方通报: [Inflection-2.5: meet the world's best personal AI](https://inflection.ai/inflection-2-5)
- 2022 年成立，三位联合创始人分别是原 DeepMind 联合创始人 Mustafa Suleyman、Linkedln 联合创始人 Reid Hoffman，还有前 DeepMind 首席科学家 Karen Simonyan。

Inflection-2.5 将强大的 LLM 能力与 Inflection 标志性的「同理心微调」结合在一起，兼具高情商与高智商，可联网获取事实信息，其性能可与 GPT-4、Gemini 等领先大模型相媲美。
- Inflection-2.5 实现了接近 GPT-4 的性能，而训练过程却仅使用 GPT-4 40% 的算力

Inflection-2.5 现已向所有 [Pi](https://pi.ai/talk) 用户开放，在 PC 端、iOS 和安卓 App 上均是免费可用。


### OLMo

【2023-3-6】AI2（Allen Institute for AI）开源了 [OLMo](https://allenai.org/olmo)（Open Language Model）：[真正完全开源的大模型](https://mp.weixin.qq.com/s/uB6jxCWDTJhtFsh9Bc_DYQ)
- github: [olmo](https://github.com/allenai/olmo)
- OLMo 独特之处是**完全开源**，除了训练模型，还有训练数据，训练代码以及模型评估代码。
- 只要你有GPU卡，再基于OLMo开源的数据和代码，就可以快速从零训练一个自己的LLM。

OLMo还直接公开了训练模型的日志：
- [博客](https://blog.allenai.org/olmo-open-language-model-87ccfc95f580)
- 代码: GitHub - allenai/OLMo: Modeling, training, eval, and inference code for OLMo
- 数据: GitHub - allenai/dolma: Data and tools for generating and inspecting OLMo pre-training data.
- [论文](https://arxiv.org/abs/2402.00838)
- 模型[OLMo-7B](https://huggingface.co/allenai/OLMo-7B)
- 评估[OLMo-Eval](https://github.com/allenai/OLMo-Eval)
- 微调[open-instruct](https://github.com/allenai/open-instruct)
- [日志](https://wandb.ai/ai2-llm/OLMo-7B/reports/OLMo-7B--Vmlldzo2NzQyMzk5)

OLMo目前开源的模型主要有三个规模：1b, 7b, 65b(训练中)
- 7b还有OLMo 7B Instruct

OLMo 7B 大部分评测上和Meta开源的Llama 2 7B相当

安装

```sh
pip install ai2-olmo
# ------------
git clone https://github.com/allenai/OLMo.git
cd OLMo
pip install -e .[all]
```

推理

You can utilize our Hugging Face integration to run inference on the olmo checkpoints:

```py
from hf_olmo import * # registers the Auto* classes

from transformers import AutoModelForCausalLM, AutoTokenizer

olmo = AutoModelForCausalLM.from_pretrained("allenai/OLMo-1B")
tokenizer = AutoTokenizer.from_pretrained("allenai/OLMo-1B")

message = ["Language modeling is "]
inputs = tokenizer(message, return_tensors='pt', return_token_type_ids=False)
response = olmo.generate(**inputs, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
print(tokenizer.batch_decode(response, skip_special_tokens=True)[0])
Alternatively, with the Hugging Face pipeline abstraction:
# ----------- 简版 ---------
from transformers import pipeline
olmo_pipe = pipeline("text-generation", model="allenai/OLMo-7B")
print(olmo_pipe("Language modeling is"))
```

微调
- 提前按要求转换语料格式，id化

```sh
torchrun --nproc_per_node=8 scripts/train.py {path_to_train_config} \
    --data.paths=[{path_to_data}/input_ids.npy] \
    --data.label_mask_paths=[{path_to_data}/label_mask.npy] \
    --load_path={path_to_checkpoint} \
    --reset_trainer_state
```

微调模型推理

Inference on finetuned checkpoints
- If you finetune the model using the code above, you can use the conversion script to convert a native OLMo checkpoint to a Hugging Face-compatible checkpoint

```sh
# olmo 模型 转 hf 格式
python hf_olmo/convert_olmo_to_hf.py --checkpoint-dir /path/to/checkpoint
```

量化

Quantization

```py
olmo = AutoModelForCausalLM.from_pretrained("allenai/OLMo-7B", torch_dtype=torch.float16, load_in_8bit=True)  # requires bitsandbytes
```


### 微软 

#### bGPT

【2024-3-11】[不依赖token，字节级模型来了！直接处理二进制数据](https://www.toutiao.com/article/7344998008813093387)

微软亚研院等发布 `bGPT`，仍旧基于`Transformer`，但模型预测**下一个字节**（byte）。
- 直接处理原生**二进制**数据，bGPT 将所有输入内容都视为**字节序列**，不受限于任何特定的格式或任务。
- 字节粒度非常细，处理的字节序列通常较长，这对基于Transformer的传统模型来说是一个挑战。由于自注意机制的复杂度是二次方的，处理长序列的效率和可扩展性受到了限制。
- 论文：[Beyond Language Models: Byte Models are Digital World Simulators](https://arxiv.org/abs/2402.19155)
- 代码：[bgpt](https://github.com/sanderwood/bgpt)
- 模型：[bgpt](https://huggingface.co/sander-wood/bgpt)
- 项目主页：[byte-gpt](https://byte-gpt.github.io)

能力
- 预测CPU行为，准确率超过99.99%；
- 直接模拟MIDI —— 一种音乐传输和存储的标准格式。
- bGPT还展示了在处理诸如文本、图像和音频传统媒体文件的生成/分类任务上的潜力，而且不需要任何针对特定模态的定制。

100M参数的bGPT 可与同样规模的文本模型（GPT-2）、视觉模型（ViT）和音频模型（AST）在各自的模态下有着可比的性能。

传统的深度学习往往忽视了**字节**——数字世界的构建基石。
- 不论是信息的形式还是操作，都是通过二进制格式编码和处理的。
- 字节构成了所有数据、设备和软件的基础，从计算机处理器到我们日常使用的电子产品中的操作系统。

论文标题清晰地指出了其目标：
> 超越语言模型：将字节模型作为数字世界的模拟器。

bGPT包含三个关键组成部分：
- 线性投影层：通过线性投影将每个字节块转化为密集向量表示，既保留了关键信息，又降低了维度。
- 块级解码器：顺序处理块的embeddings以预测下一个块的特征，使用自回归机制学习字节序列的整体结构。
- 字节级解码器：根据块级解码器的预测特征来预测每个块内的字节序列，这一过程独立于每个块进行，依据当前块的特征表示。
bGPT提供了一种有前景的解决方案来应对传统模型在处理字节级数据时面临的挑战，显著提高了处理大规模数字数据序列的效率和可扩展性。


#### WizardLM-2

【2024-4-17】[微软发布了开源大模型WizardLM-2 8X22B，目前开源模型性能最佳，吊打一众开源和闭源大模型](https://zhuanlan.zhihu.com/p/692725484)

微软最近发布了开源大模型`WizardLM-2`，提高了复杂聊天、多语言、推理和代理的性能。
- 新系列包括三个尖端型号：`WizardLM-2 8x22B`、`WizardLM-2 70B`和`WizardLM-2 7B`。
- ![](https://pic1.zhimg.com/80/v2-86c5016e1556740123c354050d22eb3c_1440w.webp)

WizardLM-2是微软在开源大模型的最新里程碑。
- WizardLM-2 8x22B是目前开源最先进的大模型，性能超过了GPT-4-0314以及最近火热的Cohere Command R+，接近Claude 3 Sonnet的性能。
- WizardLM-2 70B达到顶级推理能力，是70B相同尺寸的首选，性能吊打Mistral Large、Qwen1.5 72B Chat等。
- WizardLM-2 7B也是7B模型中最快的，并实现了与现有10倍更大的开源领先模型相当的性能，甚至超过Yi-34B Chat模型。

WizardLM-2的成功证明：
- AI精心创建的数据和由AI逐步监督的模型将是通往更强大的人工智能的可行路径。
- ![](https://pic2.zhimg.com/80/v2-fea52e055248b5e5e8526da0ce39f4fd_1440w.webp)

ai驱动的合成数据训练系统：
- 数据预处理：
  - 数据分析：使用AI产生合成数据管道来获取新源数据的不同属性的分布。这有助于我们对数据有初步的了解。
  - 加权抽样：最佳训练数据的分布总是与人类聊天语料库的自然分布不一致，因此需要根据实验经验调整训练数据中各种属性的权重。
- 渐进式学习：与使用所有数据进行一次性训练的常见做法不同，研究人员发现使用不同的数据切片并逐级逐步训练可以用更少的数据获得更好的结果。在每个阶段，将数据切片提供给Evol Lab，以获得更多样化和更复杂的[指令、响应]对。同时利用一个名为“AI Align AI”（AAA）的新框架来进行调教，该框架可以分组多个最先进的LLM来相互教学和改进。最后先后应用监督学习、Stage-DPO和RLEIF来优化每个变体。
- Evol Lab：
  - Evol-Instruct：研究人员投入了大量精力，在原始的Evol-Instruct方法中重新评估了各种问题，并启动了初步修改。新方法使各种代理能够自动生成高质量的指令。
  - Evol-Answer：指导模型多次生成和重写响应可以改善其逻辑、正确性和亲和力。
- AI对齐AI（AAA）：
  - 共同教学：收集WizardLMs，以及各种许可的开源和专有最先进的模型，然后让他们相互教学和改进，教学包含模拟聊天、质量判断、改进建议和缩小技能差距等。
  - 自学：WizardLM可以通过激活自身学习生成用于监督学习的新进化训练数据和用于强化学习的偏好数据。
- 学习：
  - 监督学习
  - 阶段-DPO：为了更有效的离线强化学习，我们还将偏好数据拆分为不同的切片，并逐步改进模型。
  - RLEIF：我们采用教学质量奖励模型（IRM）与流程监督奖励模型（PRM）相结合，以实现在线强化学习的更精确的正确性。


### cpp 本地部署 

支持多种模型


#### llama.cpp

【2023-11-25】[如何看待llama.cpp?](https://www.zhihu.com/question/589100471/answer/3276334273?utm_psn=1711150724442902528)

大模型推理框架 llama.cpp 是开发者 Georgi Gerganov 基于 Meta 的 LLaMA 模型 手写的**纯 C/C++** 版本：
- 支持CPU推理, 当然也支持CUDA/OpenCL推理
- 具有 FP16 和 FP32 的混合精度
- 支持8-bit/4bit量化 ...

llama.cpp 的代码结构比较直观，如下所示，为整体代码结构中的比较核心的部分的代码结构

```sh
|-- example
|  |-- main
|     |-- main.cpp  # 推理llama 2的主函数
|-- ggml.c # ggml.c 和.h文件定义一些框架的基础数据结构和函数等
|-- ggml.h
|-- ggml-alloc.c #内存分配管理
|-- ggml-alloc.h
|-- llama.cpp # 整个llama 2的计算图构建和weight加载等
|-- llama.h
|-- ggml-cuda.cu  #cuda版本的llama2 中的kernel实现与调用
|-- ggml-cuda.h
|-- ggml-opencl.cpp #opencl版本的llama2 中的kernel实现与调用
|-- ggml-opencl.h
|-- ... #其他
```

源码详解见[原文](https://www.zhihu.com/question/589100471/answer/3276334273)



#### chatglm.cpp 本地运行

[chatglm.cpp](https://github.com/li-plus/chatglm.cpp) 类似 llama.cpp 的量化加速推理方案，实现笔记本上实时对话

C++ implementation of ChatGLM-6B & ChatGLM2-6B & ChatGLM3 & more LLMs

C++ implementation of [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B), [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B), [ChatGLM3-6B](https://github.com/THUDM/ChatGLM3) and more LLMs for real-time chatting on your MacBook.

[![demo](https://github.com/li-plus/chatglm.cpp/raw/main/docs/demo.gif)](https://github.com/li-plus/chatglm.cpp/blob/main/docs/demo.gif)

chatglm.cpp 支持其他模型
- ChatGLM2-6B
- ChatGLM3-6B
- CodeGeeX2
- Baichuan-13B-Chat
- Baichuan2-7B-Chat
- Baichuan2-13B-Chat
- InternLM-Chat-7B
- InternLM-Chat-20B

实践
- 【2023-11-1】mac 本地调试通过， ChatGLM3-6B int4 量化后，模型有3.3G，本地推理速度很快

```sh
# ----- ① 代码下载 ------
git clone --recursive https://github.com/li-plus/chatglm.cpp.git && cd chatglm.cpp
python3 -m pip install -U pip
python3 -m pip install torch tabulate tqdm transformers accelerate sentencepiece
# --- ② 模型下载转换 ----
# transform ChatGLM-6B into quantized GGML format. For example, to convert the fp16 original model to q4_0 (quantized int4) GGML model
python3 chatglm_cpp/convert.py -i THUDM/chatglm-6b -t q4_0 -o chatglm-ggml.bin
# ---- ③ 编译 -----
cmake -B build
cmake --build build -j --config Release
# ---- ④ 运行 ------
./build/bin/main -m chatglm-ggml.bin -p 你好
# 你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。
# 交互模式
./build/bin/main -m chatglm-ggml.bin -i
./build/bin/main -m chatglm3-ggml.bin -i --top_p 0.8 --temp 0.8
# ------ 其它模型 ------
python3 chatglm_cpp/convert.py -i THUDM/chatglm2-6b -t q4_0 -o chatglm2-ggml.bin
./build/bin/main -m chatglm2-ggml.bin -p 你好 --top_p 0.8 --temp 0.8
# 你好👋！我是人工智能助手 ChatGLM2-6B，很高兴见到你，欢迎问我任何问题。
# -----------------
python3 chatglm_cpp/convert.py -i THUDM/chatglm3-6b -t q4_0 -o chatglm3-ggml.bin
./build/bin/main -m chatglm3-ggml.bin -p 你好 --top_p 0.8 --temp 0.8
# 你好👋！我是人工智能助手 ChatGLM3-6B，很高兴见到你，欢迎问我任何问题。
```


#### Baichuan2-13B-Chat

本地部署

```sh
python3 chatglm_cpp/convert.py -i baichuan-inc/Baichuan2-13B-Chat -t q4_0 -o baichuan2-13b-chat-ggml.bin
./build/bin/main -m baichuan2-13b-chat-ggml.bin -p 你好 --top_k 5 --top_p 0.85 --temp 0.3 --repeat_penalty 1.05
# 你好！今天我能为您提供什么帮助？
```

### trl

[Ivwerra/trl](https://github.com/lvwerra/trl)，[文档](https://huggingface.co/docs/trl/index) 

PPO精调LLM的三个步骤:
- ![流程图](https://camo.githubusercontent.com/85d00cf9bca67e33c2d1270b51ff1ac01853b26a8d6bb226b711f859d065b4a6/68747470733a2f2f68756767696e67666163652e636f2f64617461736574732f74726c2d696e7465726e616c2d74657374696e672f6578616d706c652d696d616765732f7265736f6c76652f6d61696e2f696d616765732f74726c5f6f766572766965772e706e67)
1. 用 codeparrot 数据训练 GPT-2 124.2M 模型
2. 用sentiment训练奖励模型，模型用的是distilbert
3. RL训练 


### RLHF

中国人写的一套框架，基于transformers库实现的【过度依赖这套框架实现，核心要编写代码较少】，核心代码文件是train_sft.py、train_reward.py、train_rlhf.py等模块，使用apex和deepspeed等会加速模型训练
- 预训练模型：支持Pangu和GLM为主，其他目前测试是不支持的
- 数据源：百科、知道问答、对联、古文、古诗词、微博新闻评论等
- 评测数据：CLUE Benchmark
- 强化学习ppo：使用trlx框架实现的

总体来说，做个demo是足够的，但灵活性不行。参考这个代码，结合自身业务，可快速实现一套方案。

### FlexGen 加速

【2023-2-22】[跑ChatGPT体量模型，从此只需一块GPU：加速百倍的方法来了](https://zhuanlan.zhihu.com/p/608513900)

来自斯坦福大学、UC Berkeley、苏黎世联邦理工学院、Yandex、莫斯科国立高等经济学院、Meta、卡耐基梅隆大学等机构的新研究提出了 [FlexGen](https://github.com/FMInference/FlexGen)，这是一种用于运行有限 GPU 内存的 LLM 的高吞吐量生成引擎。

通过聚合来自 GPU、CPU 和磁盘的内存和计算，FlexGen 可以在各种硬件资源限制下灵活配置。通过线性规划优化器，它搜索存储和访问张量的最佳模式，包括权重、激活和注意力键 / 值（KV）缓存。FlexGen 将权重和 KV 缓存进一步压缩到 4 位，精度损失低到可以忽略不计。与最先进的 offloading 系统相比，FlexGen 在单个 16GB GPU 上运行 OPT-175B 的速度提高了 100 倍，并首次实现了 1 token/s 的实际生成吞吐量。如果提供了更多的分布式 GPU，FlexGen 还带有流水线并行 runtime，以允许在解码时进行超线性扩展

大模型训练需要极高的计算和内存要求。
- 例如，GPT-175B（GPT-3）仅用于存储模型权重就需要 325GB 的内存。要让此模型进行推理，至少需要五块英伟达 A100（80GB）和复杂的并行策略。

降低 LLM 推理资源需求的方法是最近人们经常讨论的内容。这些努力分为三个方向：
- （1）**模型压缩**以减少总内存占用量；
- （2）**协同推理**，通过去中心化分摊成本；
- （3）**Offloading** 以利用 CPU 和磁盘的内存。
- ![img](https://pic3.zhimg.com/80/v2-f1503265810382035d8d888a38b25cb6_1440w.webp)

### 写作猫

【2023-2-27】[写作猫](https://xiezuocat.com/chat)公测，提供小程序

对话写作猫上线公测。
- 秘塔自研LLM大模型【并非调用OpenAI API】
- 从零开始处理数据/训练【并非借助开源模型】
- 已经具备了数百种技能【数不胜数】
- 训练花费不足1亿美金【远远不足】
- 现在可用【并非内测】

上海秘塔网络科技有限公司成立于2018年4月，是人工智能领域的一家新锐科技公司，致力于将重复脑力劳动AI化，以AI为杠杆撬动专业场景的百倍生产力提升。


### 马斯克 xAI

【2023-7-12】[xAI](https://x.ai/blog) 究竟是要用AI做什么？

马斯克
- 为了理解现实（understand reality）

而xAI官方主页目前也只有一句话
> xAI 的目标是为了理解宇宙的真正本质（understand the true nature of the universe）。

美国内华达州的一份文件显示，马斯克在3月9日注册成立了X.AI 公司。其中马斯克担任董事，负责营运马斯克家族办公室的Jared Birchall 被列为该公司秘书。

xAI的团队由马斯克领导，其他11名团队成员则分别来自 DeepMind 、OpenAI、谷歌研究院、微软研究院、特斯拉、多伦多大学等，成员整体都非常年轻，团队成员遍及硅谷、加拿大、英国等地。


#### Grok

【2023-11-3】发布 [Grok](https://x.ai/blog/grok)

Grok 是根据《银河系梦游指南》中的刺猬模型制作，一本关于哲学的书，这个家伙只是一本关于幽默的书。

哲学基础: 
- 不知道生命的意义，但是我们越能扩大意识的范围和规模，无论是数字化的还是生物学的，就越能理解该问什么问题，以了解宇宙这个答案，我有一种好奇心哲学。



#### Grok-1

【2024-3-17】发布 [Grok-1](https://x.ai/blog/grok-os)

在线体验
- HugginceFace [grok-1-test](https://huggingface.co/spaces/Omnibus/grok-1-test)

【2024-3-25】[Grok-1 314B 在 M2 Ultra 上部署](https://mp.weixin.qq.com/s/RbLfJpsIeJlmDf4cXyBlUA)

Georgi Gerganov 在推上说 Causally running Grok-1 at home（在家中随意运行 Grok-1）
- Apple M2 Ultra
- 4-bit! iq3_s, 130gb metal buffer, 9 t/s

llama.cpp 的 [Add grok-1 support PR](https://github.com/ggerganov/llama.cpp/pull/6204) 上也有详细的讨论，有兴趣的去看看吧

xAI发布Grok-1的基本模型权重和网络架构。
- 2023年10月预训练阶段的原始基础模型，没有针对任何特定应用（例如对话）进行微调。

结构上，Grok-1采用了**混合专家**（MoE）架构，包含8个专家，总参数量为314B（3140亿），处理Token时，其中的两个专家会被激活，激活参数量为86B。

单看这激活的参数量，就已经超过了密集模型Llama 2的70B，对于MoE架构来说，这样的参数量称之为庞然大物也毫不为过。

更多参数信息如下：
- 窗口长度为8192tokens，精度为bf16
- Tokenizer vocab大小为131072（2^17），与GPT-4接近；
- embedding大小为6144（48×128）；
- Transformer层数为64，每层都有一个解码器层，包含多头注意力块和密集块；
- key value大小为128；
- 多头注意力块中，有48 个头用于查询，8 个用于KV，KV 大小为 128；
- 密集块（密集前馈块）扩展因子为8，隐藏层大小为32768

由于模型规模较大（314B参数，约300G），需要有足够GPU和内存的机器才能运行Grok。

#### Grok 加速

Colossal-AI 将在近期进一步推出对Grok-1在并行加速、量化降低显存成本等优化


#### Grok-1.5

【2024-3-28】[马斯克官宣Grok-1.5！超GPT-4 16倍上下文，推理能力超DBRX](https://mp.weixin.qq.com/s/IoCdv2CeLJZuMesOAyv-oA)

3 月 28 日，马斯克发布了 Grok-1.5，具有前所未有的长上下文支持和高级推理能力的新型人工智能模型。

Grok-1.5，作为该系列的最新版本，预计将在未来几天向早期测试者和 X 平台的现有用户开放。
- Grok-1.5 最显著的改进是更强大的编码与数学相关任务性能。
- 另一项新功能是在上下文窗口中处理多达 128K 个 tokens。这使得 Grok 的记忆容量增加至前代上下文长度的 16 倍，因此能够消化大部头文档中的信息

Grok-1.5 模型还可处理更长、更复杂的提示词，在上下文窗口扩展的同时保持其指令跟踪能力。在 Needle In A Haystack (NIAH) 评估中，Grok-1.5 展示出强大的检索能力，可以在多达 128K tokens 的长上下文中嵌入文本，实现完美的检索结果，仅从从文本长度来看，Grok-1.5 可真的跨越极其之大，是 GPT-4 的 16 倍。

跟“最强”开源大模型 DBRX 相比，Grok 1.5 表现更为亮眼。


### DBRX


【2024-3-27】[开源大模型王座再易主，1320亿参数DBRX上线，基础、微调模型都有](https://finance.sina.com.cn/tech/roll/2024-03-28/doc-inapvxxu3637863.shtml)

1320亿参数`DBRX`上线 

迄今为止最强大的开源大语言模型，超越了 `Llama 2`、`Mistral` 和马斯克刚刚开源的 `Grok-1`

大数据人工智能公司 Databricks 开源通用大模型 DBRX，一款拥有 1320 亿参数的混合专家模型（MoE）。

DBRX 基础（DBRX Base）和微调（DBRX Instruct）版本已经在 GitHub 和 Hugging Face 上发布，可用于研究和商业用途。可自行在公共、自定义或其他专有数据上运行和调整它们，也可通过 API 的形式使用。
- 基础版：[dbrx-base](https://huggingface.co/databricks/dbrx-base)
- 微调版：[dbrx-instruct](https://huggingface.co/databricks/dbrx-instruct)
  - DBRX Instruct 超越了 GPT-3.5（如 GPT-4 论文中所述），并且与 Gemini 1.0 Pro 和 Mistral Medium 具有相当的竞争力
- GitHub：[dbrx](https://github.com/databricks/dbrx)

DBRX 在语言理解、编程、数学和逻辑等方面轻松击败了目前业内领先的开源大模型，如 LLaMA2-70B、Mixtral 和 Grok-1。

DBRX 也在大多数基准测试上超过了 GPT-3.5，质量上可与 Gemini 1.0 Pro 和 Mistral Medium 竞争，同时速度大大加快。托管在 Mosaic AI Model Serving 上时，速度达到了 150 token/s/ 用户。 

DBRX 的效率很高，基于斯坦福 MegaBlocks 开源项目构建的混合专家模型，平均只用激活 360 亿参数来处理 token，可以实现极高的每秒处理速度。它的推理速度几乎比 LLaMA2-70B 快两倍，总参数和活动参数数量比 Grok 小约 40%。

Databricks NLP 预训练团队负责人 Vitaliy Chiley 介绍道，DBRX 是在 12 万亿 Token 的文本和代码上预训练的 16×12B MoE LLM，它支持的最大上下文长度为 32k Tokens。

DBRX 是一种基于 Transformer 的仅解码器大语言模型（LLM），使用细粒度的专家混合（MoE）架构，共有 1320 亿参数，其中 36B 个参数在任何输入上都处于激活状态。该模型是在 12T 文本和代码数据 token 上预训练而成，最大上下文长度高达 32k。

与 Mixtral 和 Grok-1 等其他开源 MoE 模型相比，DBRX 是细粒度的，这意味着它使用了更多数量的小型专家。DBRX 有 16 个专家模型，从中选择 4 个使用，而 Mixtral 和 Grok-1 有 8 个专家模型，选择其中 2 个。算下来，DBRX 提供了 65 倍可能的专家组合，这种组合方式的倍增提高了模型质量。

与此同时，DBRX 使用旋转位置编码 (RoPE)、门控线性单元 (GLU) 和分组查询注意力 (GQA) 等技术来提高模型质量。此外，DBRX 还使用了 tiktoken 存储库中提供的 GPT-4 分词器。


### Jamba

#### Transformer 问题

目前 LLM 建立在传统 Transformer架构上。虽然强大，但这种架构有两个缺点：
- **大内存**占用空间：Transformer 内存占用空间随上下文长度而缩放。
  - 没有大量硬件资源的情况下，运行长上下文窗口或许多并行批次具有挑战性，限制了广泛的实验和部署机会。‍
- 随着上下文的增长，**推理缓慢**：
  - Transformer 注意力机制随序列长度进行二次扩展，并减慢吞吐量，因为每个令牌都取决于之前的整个序列——将长上下文用例置于高效生产范围之外。‍

#### Mamba 介绍

卡内基梅隆大学和普林斯顿大学的研究人员提出的 Mamba，恰恰解决了这些缺点，为语言模型开发开辟了新的可能性。
- Mamba: 基于状态空间模型（State Space Model）的模型
- Mamba在语言建模方面可以媲美甚至击败 Transformer
- [Mamba技术背景详解：从RNN到Mamba一文搞定](https://zhuanlan.zhihu.com/p/689215356?utm_psn=1757021969898594304), 英文原文: [A Visual Guide to Mamba and State Space Models](https://maartengrootendorst.substack.com/p/a-visual-guide-to-mamba-and-state)

Transformer到Mamba

RNN：
- RNN只考虑之前隐藏状态和当前输入，防止重新计算所有先前状态
- 但RNN会遗忘信息（于是有Transformer）
- RNN是顺序循环 ——> 训练不能并行

于是，有的lstm和transformer，解决RNN遗忘问题

Tranformer 缺陷：
- 一次性矩阵每个token进行比较（支持并行化）
- 推理缺陷：生成下一个token任务中，要算所有token的注意力（L^2）

有没有一种架构技能并行，又能快速推理？随序列长度线性扩展
- SSM（State Space Model）
- ![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6480800-2449-456a-87a7-27c8a4e9e718_2520x1388.png)

Mamba

主要贡献：
- 选择性扫描算法selective scan algorithm——允许模型过滤相关信息
- 硬件感知算法hardware-aware algorithm——允许通过并行扫描、内核融合和重新计算有效存储结构

问题:
- 关注或忽略特定输入的能力上表现不佳

两个任务：
- 选择性复制selective copying
- 感应头induction heads

#### Jamba 诞生

【2024-3-28】AI21 Labs 首次推出基于Mamba的生产级模型 [Jamba](https://www.ai21.com/jamba) ，提供一流的质量和性能。不再是Transformer一家独大。
- 成功地将 Mamba 与 Transformer架构相结合，并将混合SSM-Transformer模型推进到生产级规模和质量。
- AI21 Labs开发了相应的 Joint Attention和Mamba（Jamba）架构。
- [Jamba](https://www.ai21.com/jamba)由Transformer、曼巴和专家混合（MoE）层组成，同时优化内存、吞吐量和性能。

[Jamba](https://www.ai21.com/jamba) 是世界上第一个基于Mamba的生产级模型。通过用传统Transformer架构的元素增强Mamba结构化状态空间模型（SSM）技术，Jamba弥补了纯SSM模型的固有局限性。提供256K上下文窗口，它已经在吞吐量和效率方面表现出显著的提高
- [官方介绍](https://www.ai21.com/blog/announcing-jamba)
- [hf](https://huggingface.co/ai21labs/Jamba-v0.1)

Apache 2.0下许可情况下，Jamba开放权重，开发者可以进一步优化和微调。
- ![](https://picx.zhimg.com/80/v2-11e3de4bc669df61758305afc8156a4c_1440w.webp?source=2c26e567)

特点
- 第一个基于生产级Mamba的模型建立在新颖的SSM-Transformer混合架构上
- 与Mixtral 8x7B相比，长上下文的吞吐量为3倍
- 民主化访问一个巨大的256K上下文窗口
- 唯一一款在单个GPU上容纳高达140K上下文的型号
- 在Apache 2.0下以开放权重发布
- 可在Hugging Face上获得，并即将登陆NVIDIA API目录


#### Mamba in Mamba

【2024-3-7】[阿里提出Mamba in Mamba: 比现有SOTA提速10倍，GPU使用减少73.4%，性能原地起飞](https://mp.weixin.qq.com/s/oLQzaJrwFqRZZ-UYTklWww)

红外小目标检测（ISTD）算法取得了显著进展。
- 结合卷积网络和 Transformer 结构的模型能够很好地提取局部和全局特征。
- 同时，也继承了基础模型的缺陷，例如，Transformer 的二次计算复杂度，这影响了效率。

受线性复杂度/长距离建模的基础模型`Mamba`启发，探索了这种状态空间模型在ISTD中的潜力。
- 直接应用不合适，因为对检测小目标至关重要的局部特征无法得到充分利用。
- 相反，为高效的ISTD定制了一种`Mamba-in-Mamba`（`MiM-ISTD`）结构。例如，将局部Patch视为“视觉句子”，并进一步分解为作为“视觉单词”的子Patch, 以进一步探索局部性。给定视觉句子中每个单词之间的交互将在几乎无计算成本的情况下计算。通过聚合单词和句子特征，MiM-ISTD的表现能力可以得到显著增强。

在NUAA-SIRST和IRSTD-1k上的实验证明在准确性和效率方面的优势。
- MiM-ISTD比SOTA快，并且在推理过程中，每个图像的GPU内存使用减少了73.4，克服了在处理高分辨率红外图像时执行基于Mamba理解的计算和内存限制。

源代码：[MiM-ISTD](https://github.com/txchen-USTC/MiM-ISTD)


### Command R+




# 结束

