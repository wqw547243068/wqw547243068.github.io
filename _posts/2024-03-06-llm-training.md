---
layout: post
title:  LLM 大模型训练之路
date:   2024-03-06 12:00:00
categories: 大模型
tags: ChatGPT 训练 罗福莉 数据集 lora 微调
excerpt: 大模型训练原理，如何训练，有什么经验？
mathjax: true
permalink: /llm_train
---

* content
{:toc}


# LLM 大模型训练之路

大模型主要有：数据、训练、推理部署、大模型应用四个方面

## 总结

- 【2024-9-12】[llm 论文淘金](https://zhuanlan.zhihu.com/p/719626313?utm_psn=1885030923797525376)
- 项目地址：[awesome-llm-pretraining](https://github.com/RUCAIBox/awesome-llm-pretraining) 大模型训练资源

LIMA 等论文
- CPT `预训练`学**知识**
- SFT `指令微调`学**格式**
- RL `强化学习`**对齐人类偏好**

要想大模型有**领域知识**，得`增量预训练`。`指令微调`记知识不靠谱，不是几十 w 条数据能做到的

训练模式图解 [知乎](https://zhuanlan.zhihu.com/p/24868371543)

【2025-12-21】[预训练、微调和RL对于推理语言模型作用](https://zhuanlan.zhihu.com/p/1986175442093380683)
- 【2025-12-8】CMU 论文 [On the Interplay of Pre-Training, Mid-Training, and RL on Reasoning Language Models](https://arxiv.org/abs/2512.07783)

训练方法：
- 预训练：先博览群书，学习海量的基础知识（学生先读完图书馆里所有的书）。
- 微调训练：在博览群书的基础上，再集中做一批练习题（高考前的专题复习）。
- 强化学习（RL）：最后请名师，每次解题时，不是只看最终答案对不对，还会点评解题步骤是否清晰、合理，并据此给予奖励或指正。 那么，这位高手最后解题能力的提升，到底是因为名师（RL）的指点真让他“开了窍”，还是只是把之前博览群书和专题复习时学过的东西，在名师面前“更好地发挥”了出来？

发现：
- RL不是万能的，它只在“能力边缘”生效
  - RL真正提升模型能力（不只是激发旧知识）前提是：1）预训练后模型还有进步空间；2）RL训练数据正好落在模型的“能力边缘”
- RL是对知识的“灵魂”的“外壳”迁移
  - 模型掌握推理问题的“核心逻辑”（灵魂），需要最低限度的预训练曝光。一旦掌握了核心逻辑，RL可以非常有效地帮助它将这个逻辑迁移到不同表面形式的问题（外壳）上
- 微调训练的巨大性价比——被忽视的“中场休息”
  - 总计算资源固定的情况下，把一部分资源从预训练后挪到“微调训练”上（即用特定数据做有监督学习），比把所有资源都留给RL，最终效果更好
- 过程奖励让模型的推理更可靠——对抗“作弊”的妙招
  - 相比于只奖励最终答案正确，奖励模型生成正确的推理过程，能显著减少“Reward Hacking”，让模型的推理更可靠、更真实地反映其能力

概念一：强化学习（RL）—— 不只是看答案的老师
- 通俗理解：传统的学习是给模型一堆“问题-答案”让它背。而RL是请一位老师，老师不仅看答案，更关注解题过程。比如，解一道方程题，如果模型写下了清晰的步骤“移项、合并同类项、求解”，即使最后答案算错了一点，老师也会因为步骤正确而给予部分奖励。
- 生活比喻：教小孩下棋。你不是等他赢了才表扬，而是他在中途下出一步好棋时，你就立刻说“这步棋妙啊！”，这就是过程奖励。

概念二：Reward Hacking—— 投机取巧的应试者
- 通俗理解：模型发现了奖励系统的漏洞，通过“作弊”来获得高分，而不是真正提高能力。比如，老师奖励“语言流畅的答案”，模型就可能生成一段长篇大论、文辞优美但完全错误的推理来忽悠老师。
- 生活比喻：某些应试教育中，学生不真正理解知识，而是背熟了“答题模板”和“万能金句”来套取高分。

概念三：能力的边缘（Edge of Competence）—— 跳一跳能够得着的难度
- 通俗理解：指那些对模型来说有点难，但努力一下又能解决的任务。太简单的任务学不到新东西，太难的又会直接放弃。
- 生活比喻：你健身时，选择一个重量，让你能标准地完成8-12次，最后几下比较吃力。这个重量就是你的“边缘”，最能有效增长肌肉。如果重量太轻（太简单）或太重（太难），效果都不好。




【2025-2-4】[AI大神Andrej Karpathy的通俗解释：预训练、监督式微调、强化学习](https://www.sohu.com/a/855601550_122105141)

Andrej Karpathy 对各阶段的形象比喻，教科书三种信息
- 大量背景知识 (Background information)： 对应预训练，让模型积累广泛的知识。
- 示范例题 (Worked problems)：对应监督式微调，让模型学习高质量的输出。
- 大量练习题 (Practice problems)： 对应强化学习，让模型在实践中学习，通过试错和反馈不断改进。

详解
- 1️⃣ 背景信息/阐述 Background information / exposition。
  - 教科书核心内容，用于解释概念。关注这些信息时，大脑正在对这些数据进行训练。
  - 等同于Pre-training，模型通过阅读海量的互联网文本，学习语言的规律、世界的知识，积累广泛的背景知识，为后续的学习打下基础
- 2️⃣ 示例演示 Worked problems with solutions。教科书提供的具体例题，展示如何解答问题。示范引导学生模仿学习
  - 等同于有监督微调，模型在由人类编写的 “ideal responses” 上进行微调。
  - 监督式微调 (supervised finetuning) 阶段相对应。微调阶段，模型学习人类专家提供的“理想答案”，学习如何生成高质量、符合人类期望的回复，例如助手类应用的“理想回答”。
- 3️⃣ 练习题 Practice problems。通常在每章的末尾有很多很多这样的练习题。促使学生通过试错来学习 ，必须尝试很多东西才能得到正确答案。
  - 给学生提示，没有解决方案，但有最终答案，引导学生通过 试错 (trial & error) 的方式进行学习
  - 这等同于RL。


<img width="644" height="458" alt="image" src="https://github.com/user-attachments/assets/928bfdc9-e7e2-4b27-b8bd-1b79e8ff50b6" />


开源模型
- 国外 llama、mistral 最大方
- 国内 deepseek、minicpm 最大方

OpenAI 
- 2023 年以前， 论文都属于百年陈酿，值得反复品味。
  - 那时候没名气，还很真诚、需要技术影响力。
- 现在发布的东西，秀肌肉，不实诚。

各个模型训练报告
- 训练方法和技巧基本都快定型: pretrain、sft、dpo、ppo 等
- 除了个别亮点: flash_attention, RoPE, DeepSeek R1

都是 scaling_law、数据配比、学习率、优化器、退火阶段、数据多样性、裁剪、正则、调整正负例 loss，引入或移除某网络，等等

### 经验总结

重点留意：
- 数据**清洗**方法
- pretrain: **数据配比**、**超参数**、退火阶段
- sft: task 种类、数据量级
- RLHF: dpo / ppo 训练技巧，合成数据方法等。

[CPT/SFT避坑指南](https://zhuanlan.zhihu.com/p/1911071146209710942) 注入新知识
- CPT：保证数据集规模足够庞大，至少需要数十亿（B）的token。
- 数据集较小（几十条数据），推荐`模型编辑`。

CPT 初期会出现loss上升，之后才收敛。
- 学习率（lr）至关重要。若学习率过大，loss收敛困难且可能丧失旧有能力；若学习率过小，模型则难以学习新知识。

小数据集（如100B以下）用较小学习率，通常预训练阶段最大学习率的10%。
- 例如，7B模型的预训练学习率为3e-4，可以选择3e-5。
同时，记得根据batch size做相应的学习率调整，通常可以通过批次大小的平方根来缩放学习率。

warmup_ratio 也重要。
- 预训练阶段只有1个epoch时，warmup_ratio为0.01。
- 而SFT通常有3个epoch，warmup_ratio为0.03。
- 如果是CPT，建议增大warmup_ratio，尤其当数据集较小（例如小于百亿token）时，这样可以平滑模型的过渡。

SFT训练
- 不必盲目追求多个epoch的训练，1个epoch就能获得相对较好的对话效果。
- 当然，更多的epoch有助于提升模型的评测结果，但如果资源有限，1个epoch足以。

如果数据量较小（1k数据），可尝试更多epoch，但容易导致过拟合。CPT与SFT结合的技术路线，若希望构建领域模型，且与通用对话模型在输出内容、格式上差异较大，且通过CPT注入知识，那么可选择以下几种技术路线。
- 从预训练模型开始SFT训练，先进行CPT，再使用领域数据进行微调。此方法会丧失部分通用对话能力，因此不推荐。
- 从预训练模型开始SFT训练，先进行CPT，再**混合**使用通用SFT数据和领域数据。这种方法适用于领域数据与通用数据接近的情况，如医疗问答。若任务差异较大，输出格式完全不同，通用SFT数据可能会对任务目标产生负向影响。
- 从预训练模型开始SFT训练，依次进行CPT、通用SFT、领域SFT训练。此方法可能导致任务目标与CPT阶段知识注入存在间隙，可能效果不佳。

经验
- (1) 评估 > 训练: 倒果为因, 解释某个训练技巧是否正确使用; 计算机是经验科学:
  - 几年前，分析 BERT 结构相比于 GPT 结构更优越还属于 nlp 的八股文；
  - 现在，分析 decoder-only 结构优异性也属于 nlp 的八股文。
  - 业界没有高效、全面且快速的评估方法，最常用的还是: 
    - 刷 benchmark(c-ecal/mmlu)
    - GPT-4 评估: 不稳定, alignbench/MITbench 榜单上, GPT-4跑10次, 方差有10+ pp
    - 人工评估: 具体case, 人肉评估, 好用但慢且贵, 不适合pretrain模型
  - 评估问题: 做题≠真实能力, 需要 logits 概率分布等更深层次内容, gsm8k (达到98%准确率) 和 mathQA 作对了，不等于掌握了数学能力，因为大模型依然在“背”。
  - 
- (2) arxiv > 顶会: 倒反天罡
  - 原因: 顶会论文审稿周期长（半年以上），大模型更新太快
- (3) 企业 ＞ 高校：
  - 学术界里，只有清华有足够GPU训练大模型，而且清华大佬还全都在 kimi 和 质谱实习
  - 由于缺乏机器、缺乏批量访问 GPT4 的资金，高校的工作大多集中在：lora 微调，小模型微调，尝试解决幻觉，数据集构造，prompt engine 等工作。指导意义不大
- (4) 多模态 > 纯文本: 大势所趋
- (5) 可解释性: 有价值，但目前的模型过拟合问题都解决不了
- (6) 网络结构/训练方法: 上限高(RoPE/DPO)，但也容易灌水, 有没有数学证明是分水岭

【2025-7-23】[大厂业务模型微调实录](https://zhuanlan.zhihu.com/p/1931389474501292248)

- **需求**：智能营销
- **现状**：
  - 业务探索：过去一年做了很多PE工作，验证业务结果、方向可行性
  - 深水区：各种PE方法无能为力，如 prompt调试、人工标注、动态示例、memory压缩检索，bad case依然很高
- 问题：如何让模型向真人一样聊天？

解决过程
- 最直接的思路：强化学习，如 PPO/GRPO，梳理各种标准，标注了5k数据集，用推理RM
- 问题：无论怎么训，效果都不好，因为一句话的等级判定（优中差）太主观，人都很难，更何况模型
  - 分析：差的样例确实差，这个等级的case准确率高，但召回低
- 改进：合并“中”、“优”，三分类变为两分类，是否合理；
- 问题：继续用 PPO 训练一周，效果很不好，效果反而更差了
  - 分析：无法debug，多个因素（数据/rm/训练）影响，且gpu资源不足，无法反复实验；
  - 一个月过去了，没有业务产出，无法交差
- 思考：回到事情本质，解决bad case
  - 刚开始，对技术充满好奇，上来就用RL，鲁莽了
- 改进：转换思路，根据bad case找方法，人工标注bad case，SFT 做分类系统，并归因
  - 补充知识→RAG
  - 修正模型输出→加数据
  - 一周后，对业务问题积累了完备的归因逻辑和解决方案，开始标注样本
  - 数据标注：花了很大精力准备样本，模型分成三档（难中易），只需少量高质量样本就能显著提升效果
  - SFT：模型直接给出三档，很难，但对比判断确很容易 → 启发：研发偏序RM
  - Online DPO：数据量少，PPO/GRPO 行不通，于是用 online DPO
  - 效果：SFT+Online DPO，显著提升，其中SFT提升最大
- 反思
  - 通用回答质量很难定义，业务标准太难定义，只有不断的细化，各种分类/规则
  - RL（PPO/GRPO）虽然厉害，但实际业务中，数据准备不足时，难以发挥出来
  - SFT/DPO 反而是最好的选择
  - 训练方法：先从PEFT开始，不用先全参，如 lora_rank=8 就可以通杀
  - 数据为王：研发了很多模型来做样本分类、回答、改写、偏序、纠正asr，甚至训练了多模态的模型来做纠偏

其他：

先后试了 sft，dpo，online dpo，selekt（Next-Coder），grpo
- online dpo跑了4轮越跑越差，很慢，放弃了，还实现了两个自定义的评判器，和我标注的做比较选最好的那个，还实现了回退功能，如果两个回答都是坏的，把其中一个回退成我标注的好的回答
- grpo 150条数据跑了一轮iteration2，9.5h，精确率更差了，召回有上升，但我这个任务要的就是精确率，召回可以少一些，所以也不行，现在在跑第二轮800条数据的，epoch2
- sft<selekt<dpo 这三个有效果，dpo+selekt 是最好的，训练集85%精确率，召回75%


【2025-12-19】[NeurIPS 2025 oral：LLM 训练全流程视角](https://zhuanlan.zhihu.com/p/1985315562822332452)

Harvard 和 Stanford 团队 NeurIPS 2025 发表的EvoLM 论文，从零训练了100多个1B/4B参数规模模型，覆盖预训练(PT)、增量预训练（CPT）、SFT和RL全流程，提供了模型完整训练闭环的视野
- 标题致敬普鲁斯特的《追忆似水年华》（In Search of Lost Time）。

要点
- 预训练数据量：越多越好，但达到模型规模的80-160倍时，收益快速递减
  - 1B模型，训练160B tokens后，堆数据不仅没收益，甚至下游SFT任务性能退化
  - 如果数据量有限，用小模型，不要强制扩大规模  
- 特定领域CPT
  - 直接在领域数据上训练，会引发严重的灾难遗忘，损害原有通用能力
  - 改进：CPT数据中混入5%通用预训练数据，以基地成本平衡通用、专业能力
- RL真相
  - RL本质上并没有增强模型的底层推理能力，只是让模型对已掌握的正确答案更加自信，提升采样到正确答案的概率
  - 如果sft阶段已经过度记忆，那RL带来的增量提升十分有限


### 模型阶段



各个阶段产出的模型区别

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;dark-mode&quot;:&quot;auto&quot;,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36\&quot; version=\&quot;28.2.9\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1002\&quot; dy=\&quot;-530\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-2\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;1970\&quot; width=\&quot;170\&quot; height=\&quot;230\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--46\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;170\&quot; y=\&quot;2220\&quot; width=\&quot;990\&quot; height=\&quot;180\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--21\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;170\&quot; y=\&quot;1970\&quot; width=\&quot;180\&quot; height=\&quot;230\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--20\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;550\&quot; y=\&quot;1980\&quot; width=\&quot;610\&quot; height=\&quot;220\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; value=\&quot;LLM(大模型)训练\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;620.5\&quot; y=\&quot;1840\&quot; width=\&quot;224.5\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--1\&quot; value=\&quot;无监督&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));&amp;quot;&amp;gt;数据&amp;lt;/span&amp;gt;&amp;lt;div&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));&amp;quot;&amp;gt;（通用）&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#eeeeee;strokeColor=#36393d;shadow=1;fontStyle=0;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;189.99\&quot; y=\&quot;1970\&quot; width=\&quot;160\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--3\&quot; value=\&quot;&amp;lt;div&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(128, 128, 128); font-size: 15px; font-weight: 700; text-wrap-mode: nowrap;&amp;quot;&amp;gt;Pre-Train&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;预训练&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=#0e8088;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;212.57\&quot; y=\&quot;2090\&quot; width=\&quot;114.85\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--4\&quot; value=\&quot;&amp;lt;div&amp;gt;Supervised FineTune&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;监督指令模型&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=#0e8088;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;562.5\&quot; y=\&quot;2090\&quot; width=\&quot;175\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--5\&quot; value=\&quot;&amp;lt;div&amp;gt;RLHF&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;强化学习微调&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=#0e8088;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;860\&quot; y=\&quot;2090\&quot; width=\&quot;150\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--6\&quot; value=\&quot;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));&amp;quot;&amp;gt;监督数据&amp;lt;/span&amp;gt;&amp;lt;div&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));&amp;quot;&amp;gt;（指令）&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e3c800;strokeColor=#B09500;shadow=1;fontStyle=0;fontSize=14;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;615\&quot; y=\&quot;1980\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--7\&quot; value=\&quot;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));&amp;quot;&amp;gt;监督数据&amp;lt;/span&amp;gt;&amp;lt;div&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));&amp;quot;&amp;gt;（偏好）&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f0a30a;strokeColor=#BD7000;shadow=1;fontStyle=0;fontSize=14;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;877.5\&quot; y=\&quot;1980\&quot; width=\&quot;65\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--8\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#009999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--3\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--29\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;350\&quot; y=\&quot;2009.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;495\&quot; y=\&quot;2009.5\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--9\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#009999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--4\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--5\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;420\&quot; y=\&quot;2120\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;553\&quot; y=\&quot;2120\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--10\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--1\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--3\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;840\&quot; y=\&quot;1810\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;840\&quot; y=\&quot;1700\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--11\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--6\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;475\&quot; y=\&quot;2050\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;475\&quot; y=\&quot;2100\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--12\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--7\&quot; target=\&quot;b1yAS0QOMh7NxzPnBfqw-3\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;713.35\&quot; y=\&quot;2050\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;713.35\&quot; y=\&quot;2100\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--15\&quot; value=\&quot;Pre-Train&amp;amp;nbsp;&amp;lt;div&amp;gt;预训练&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;310\&quot; y=\&quot;2060\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--16\&quot; value=\&quot;遵循指令&amp;lt;div&amp;gt;Follow instruction&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;610\&quot; y=\&quot;2060\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--17\&quot; value=\&quot;Preference Alignment\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;910\&quot; y=\&quot;2060\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--18\&quot; value=\&quot;偏好对齐\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;890\&quot; y=\&quot;2080\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--19\&quot; value=\&quot;&amp;lt;font style=&amp;quot;color: rgb(255, 51, 51);&amp;quot;&amp;gt;对齐人类价值观&amp;lt;/font&amp;gt;&amp;lt;br&amp;gt;&amp;lt;div&amp;gt;Optimized for human&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1020\&quot; y=\&quot;2240\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--22\&quot; value=\&quot;Pre-Train&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(128, 128, 128), rgb(127, 127, 127));&amp;quot;&amp;gt;预训练&amp;lt;/span&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;260\&quot; y=\&quot;1920\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--23\&quot; value=\&quot;Post-Train&amp;amp;nbsp; 后&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(128, 128, 128), rgb(127, 127, 127));&amp;quot;&amp;gt;训练&amp;lt;/span&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;820\&quot; y=\&quot;1920\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--24\&quot; value=\&quot;自动提示（&amp;lt;font style=&amp;quot;color: rgb(255, 51, 51);&amp;quot;&amp;gt;续写&amp;lt;/font&amp;gt;）&amp;lt;br&amp;gt;&amp;lt;div&amp;gt;Autocompete Prompts&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;2240\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--25\&quot; value=\&quot;+任务理解能力\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#FF3333;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;710\&quot; y=\&quot;2240\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--26\&quot; value=\&quot;Text：大语言模型ChatGPT原理是。。。\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#999900;fontSize=12;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;212.57\&quot; y=\&quot;1960\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--27\&quot; value=\&quot;Q: ChatGPT什么原理？&amp;lt;div&amp;gt;A：大语言模型是指以transformer结构。。。&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#999900;fontSize=12;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;600\&quot; y=\&quot;1960\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--28\&quot; value=\&quot;Q: ChatGPT什么原理？&amp;lt;div&amp;gt;A1：大语言模型 → win&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;A2： 不懂，好难。。。→ lose&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#999900;fontSize=12;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;860\&quot; y=\&quot;1950\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--29\&quot; value=\&quot;Continue Pre-Train&amp;lt;div&amp;gt;增量预训练&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=#0e8088;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;370\&quot; y=\&quot;2090\&quot; width=\&quot;154\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--30\&quot; value=\&quot;\&quot; style=\&quot;sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#01A88D;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.sagemaker_model;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;100\&quot; y=\&quot;2240\&quot; width=\&quot;48\&quot; height=\&quot;48\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--31\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--3\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--34\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;270\&quot; y=\&quot;2080\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;270\&quot; y=\&quot;2130\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--34\&quot; value=\&quot;Base Model&amp;lt;div&amp;gt;基座模型&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;212.57999999999998\&quot; y=\&quot;2258\&quot; width=\&quot;114.85\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--35\&quot; value=\&quot;Instruct Model&amp;lt;div&amp;gt;指令模型&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;575\&quot; y=\&quot;2258\&quot; width=\&quot;150\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--36\&quot; value=\&quot;Chat Model&amp;lt;div&amp;gt;对话模型&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;860\&quot; y=\&quot;2258\&quot; width=\&quot;150\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--37\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#009999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--29\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;430\&quot; y=\&quot;2130\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;473\&quot; y=\&quot;2130\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--40\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--29\&quot; target=\&quot;b1yAS0QOMh7NxzPnBfqw-7\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;340\&quot; y=\&quot;2200\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;340\&quot; y=\&quot;2318\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--41\&quot; value=\&quot;无监督&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));&amp;quot;&amp;gt;数据&amp;lt;/span&amp;gt;&amp;lt;div&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));&amp;quot;&amp;gt;（领域）&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontStyle=0;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;410.49\&quot; y=\&quot;1970\&quot; width=\&quot;73\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--42\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--41\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--29\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;320\&quot; y=\&quot;2060\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;320\&quot; y=\&quot;2110\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--43\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--4\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--35\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;340\&quot; y=\&quot;2210\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;340\&quot; y=\&quot;2328\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--45\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--5\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--36\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;700\&quot; y=\&quot;2210\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;700\&quot; y=\&quot;2328\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--47\&quot; value=\&quot;【2025-11-04】wangqiwen\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=12;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;855\&quot; y=\&quot;2410\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-1\&quot; value=\&quot;Mid-Train&amp;amp;nbsp; 中&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(128, 128, 128), rgb(127, 127, 127));&amp;quot;&amp;gt;训练&amp;lt;/span&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;460\&quot; y=\&quot;1920\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-3\&quot; value=\&quot;Reward Model&amp;lt;div&amp;gt;奖励模型&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;980\&quot; y=\&quot;1985\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#009999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;edgeStyle=orthogonalEdgeStyle;\&quot; parent=\&quot;1\&quot; source=\&quot;b1yAS0QOMh7NxzPnBfqw-3\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--5\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;810\&quot; y=\&quot;2120\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;892\&quot; y=\&quot;2120\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-5\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0;exitDx=0;exitDy=37.5;exitPerimeter=0;edgeStyle=orthogonalEdgeStyle;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--6\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--5\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;640\&quot; y=\&quot;2050\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;640\&quot; y=\&quot;2100\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-6\&quot; value=\&quot;难题：&amp;lt;div&amp;gt;- 灾难遗忘&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;- 数据分布漂移&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#99004D;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;562.5\&quot; y=\&quot;2170\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-7\&quot; value=\&quot;Base Model&amp;lt;div&amp;gt;基座模型&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.57\&quot; y=\&quot;2258\&quot; width=\&quot;114.85\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-8\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#009999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--34\&quot; target=\&quot;b1yAS0QOMh7NxzPnBfqw-7\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;2120\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;413\&quot; y=\&quot;2120\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-9\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#009999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; source=\&quot;b1yAS0QOMh7NxzPnBfqw-7\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--35\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;512\&quot; y=\&quot;2330\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;575\&quot; y=\&quot;2330\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-10\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#009999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--35\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--36\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;680\&quot; y=\&quot;2390\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;743\&quot; y=\&quot;2390\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-11\&quot; value=\&quot;学知识\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#0000FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490\&quot; y=\&quot;2084\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-180\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-12\&quot; value=\&quot;学格式\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#0000FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;700\&quot; y=\&quot;2080\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-13\&quot; value=\&quot;学偏好\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#0000FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;970\&quot; y=\&quot;2080\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-14\&quot; value=\&quot;Reason Model&amp;lt;div&amp;gt;推理模型&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;860\&quot; y=\&quot;2320\&quot; width=\&quot;150\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-15\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#009999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;edgeStyle=orthogonalEdgeStyle;\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--35\&quot; target=\&quot;b1yAS0QOMh7NxzPnBfqw-14\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;780\&quot; y=\&quot;2290\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;915\&quot; y=\&quot;2290\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-16\&quot; value=\&quot;SFT局限：&amp;lt;div&amp;gt;- token粒度训练&amp;lt;br&amp;gt;&amp;lt;div&amp;gt;- 学习浅层知识&amp;lt;br&amp;gt;&amp;lt;div&amp;gt;- 没有负反馈&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;- 不能向后看&amp;lt;/div&amp;gt;&amp;lt;/div&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#99004D;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;737.5\&quot; y=\&quot;2160\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-17\&quot; value=\&quot;能力&amp;lt;div&amp;gt;- Function Call&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;- 推理模式 thinking&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#0000FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;600\&quot; y=\&quot;2338\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-5\&quot; y=\&quot;1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-18\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#E6E6E6;\&quot; parent=\&quot;1\&quot; source=\&quot;b1yAS0QOMh7NxzPnBfqw-19\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;68.5\&quot; y=\&quot;1985\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;68.5\&quot; y=\&quot;2121\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-19\&quot; value=\&quot;全参微调\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;28\&quot; y=\&quot;1945\&quot; width=\&quot;82\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-20\&quot; value=\&quot;部分参数微调\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;28\&quot; y=\&quot;2120\&quot; width=\&quot;112\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-21\&quot; value=\&quot;PEFT\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;70\&quot; y=\&quot;2170\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-22\&quot; value=\&quot;难题：&amp;lt;div&amp;gt;- 海量数据&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;- 数据/任务配比&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#99004D;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;280\&quot; y=\&quot;2170\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-23\&quot; value=\&quot;Dense Model&amp;lt;div&amp;gt;稠密模型&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#336600;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;230\&quot; y=\&quot;2338\&quot; width=\&quot;114.85\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-24\&quot; value=\&quot;Sparse Model&amp;lt;div&amp;gt;稀疏模型(MoE&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(255, 255, 255), rgb(18, 18, 18));&amp;quot;&amp;gt;)&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#00CC00;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.57\&quot; y=\&quot;2340\&quot; width=\&quot;124.85\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-25\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#009999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; source=\&quot;b1yAS0QOMh7NxzPnBfqw-23\&quot; target=\&quot;b1yAS0QOMh7NxzPnBfqw-24\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;380\&quot; y=\&quot;2340\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;443\&quot; y=\&quot;2340\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;b1yAS0QOMh7NxzPnBfqw-26\&quot; value=\&quot;领域/语言/扩上文\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#0000FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;650\&quot; y=\&quot;2150\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-180\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;WpL5Nv-ky_PAdRIZGodR-1\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;CKtsSkHedHjP4OW8E3n--4\&quot; target=\&quot;CKtsSkHedHjP4OW8E3n--36\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;700\&quot; y=\&quot;2180\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;700\&quot; y=\&quot;2298\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;WpL5Nv-ky_PAdRIZGodR-2\&quot; value=\&quot;+对话能力\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#FF3333;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;860\&quot; y=\&quot;2240\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



### 训练组件

训练需要哪些组件

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;dark-mode&quot;:&quot;auto&quot;,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36\&quot; version=\&quot;29.1.1\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1360\&quot; dy=\&quot;-419\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-45\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;100\&quot; width=\&quot;231\&quot; x=\&quot;1010\&quot; y=\&quot;1340\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-14\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;304.58\&quot; x=\&quot;448.17\&quot; y=\&quot;1830\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-6\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;280\&quot; width=\&quot;254.58\&quot; x=\&quot;290\&quot; y=\&quot;1365\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; value=\&quot;LLM训练系统\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;33\&quot; width=\&quot;224.5\&quot; x=\&quot;697.14\&quot; y=\&quot;1260\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-7\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;数据\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;392.29\&quot; y=\&quot;1350\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;290\&quot; width=\&quot;345\&quot; x=\&quot;600\&quot; y=\&quot;1360\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-35\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-11\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;pre-train\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;641.6899999999999\&quot; y=\&quot;1420\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-10\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;增量预训练 cpt\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;116.78\&quot; x=\&quot;738.23\&quot; y=\&quot;1420\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-34\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-11\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-12\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-11\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;SFT\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;641.6899999999999\&quot; y=\&quot;1490\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-12\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;RLHF\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;641.6899999999999\&quot; y=\&quot;1590\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-13\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;模型训练\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;773.2200000000001\&quot; y=\&quot;1340\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-14\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;100\&quot; width=\&quot;304.58\&quot; x=\&quot;448.17\&quot; y=\&quot;1710\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-15\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;多机多卡\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;538.72\&quot; y=\&quot;1720\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-19\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;训练框架\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;400.4600000000001\&quot; y=\&quot;1765\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-20\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;183\&quot; width=\&quot;260\&quot; x=\&quot;1000\&quot; y=\&quot;1467\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-42\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-21\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-41\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-21\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;base模型\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;83.32\&quot; x=\&quot;1036.65\&quot; y=\&quot;1400\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-25\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;微调模型\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1212.83\&quot; y=\&quot;1450\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-4\&quot; y=\&quot;1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-26\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-6\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryPerimeter=0;\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;400\&quot; y=\&quot;1360\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;545\&quot; y=\&quot;1090\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-27\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-20\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;946.22\&quot; y=\&quot;1564.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1166.22\&quot; y=\&quot;1564.5\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-28\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-36\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#FF0000;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 2;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;864.5799999999999\&quot; y=\&quot;1690\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1084.58\&quot; y=\&quot;1690\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-32\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;模型并行\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;625.47\&quot; y=\&quot;1720\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-33\&quot; parent=\&quot;1\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; value=\&quot;推理数据&amp;lt;div&amp;gt;cot&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;60\&quot; x=\&quot;307.14\&quot; y=\&quot;1585\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-36\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;120\&quot; width=\&quot;217.14\&quot; x=\&quot;1023.86\&quot; y=\&quot;1710\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-37\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;基础能力\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;1050\&quot; y=\&quot;1740\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-38\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;模型评测\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1200\&quot; y=\&quot;1690\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-39\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;工具调用\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;1142.86\&quot; y=\&quot;1739\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-40\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;多模态\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;1050\&quot; y=\&quot;1789\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-41\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;chat模型\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;83.32\&quot; x=\&quot;1036.65\&quot; y=\&quot;1490\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-44\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-20\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#FF0000;entryX=0.491;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;dashPattern=1 2;entryPerimeter=0;\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-36\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1020\&quot; y=\&quot;1730\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1020\&quot; y=\&quot;1620\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-47\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;（1）\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;625.0100000000001\&quot; y=\&quot;1435\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-51\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;（2）\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;625.0100000000001\&quot; y=\&quot;1505\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-52\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;（3）\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;635.0100000000001\&quot; y=\&quot;1605\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-8\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-53\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;RM\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;50\&quot; x=\&quot;702.75\&quot; y=\&quot;1540\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-54\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;DPO\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;64.85\&quot; x=\&quot;724.2\&quot; y=\&quot;1590\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-57\&quot; parent=\&quot;1\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; value=\&quot;无监督数据\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;80\&quot; x=\&quot;297.14\&quot; y=\&quot;1375\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-1\&quot; parent=\&quot;1\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; value=\&quot;监督数据\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;60\&quot; x=\&quot;307.14\&quot; y=\&quot;1445\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-2\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=15;\&quot; value=\&quot;&amp;lt;div&amp;gt;&amp;lt;ul&amp;gt;&amp;lt;li&amp;gt;出行业务知识&amp;lt;/li&amp;gt;&amp;lt;li&amp;gt;人工客服对话语料&amp;lt;/li&amp;gt;&amp;lt;li&amp;gt;客服业务规则&amp;lt;/li&amp;gt;&amp;lt;li&amp;gt;运营活动&amp;lt;/li&amp;gt;&amp;lt;/ul&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;367.14\&quot; y=\&quot;1410\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-3\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;&amp;amp;lt;q, a&amp;amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;267.14\&quot; y=\&quot;1470\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-4\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;&amp;amp;lt;text&amp;amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;267.14\&quot; y=\&quot;1410\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-5\&quot; parent=\&quot;1\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; value=\&quot;偏好数据\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;60\&quot; x=\&quot;307.14\&quot; y=\&quot;1515\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-6\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;&amp;amp;lt;q, a_c,a_r&amp;amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;257.14\&quot; y=\&quot;1555\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-7\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;&amp;amp;lt;q, t1,t2&amp;amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;247.14\&quot; y=\&quot;1620\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-8\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=15;\&quot; value=\&quot;&amp;lt;ul&amp;gt;&amp;lt;li&amp;gt;意图识别&amp;lt;/li&amp;gt;&amp;lt;li&amp;gt;术语/规则解释&amp;lt;/li&amp;gt;&amp;lt;li&amp;gt;槽位抽取&amp;lt;/li&amp;gt;&amp;lt;li&amp;gt;多轮决策&amp;lt;/li&amp;gt;&amp;lt;/ul&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;357.14\&quot; y=\&quot;1490\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-9\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=15;\&quot; value=\&quot;&amp;lt;ul&amp;gt;&amp;lt;li&amp;gt;多轮决策&amp;lt;/li&amp;gt;&amp;lt;li&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(128, 128, 128), rgb(127, 127, 127));&amp;quot;&amp;gt;话术风格&amp;lt;/span&amp;gt;&amp;lt;/li&amp;gt;&amp;lt;/ul&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;357.14\&quot; y=\&quot;1560\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-10\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=15;\&quot; value=\&quot;&amp;lt;ul&amp;gt;&amp;lt;li&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(128, 128, 128), rgb(127, 127, 127));&amp;quot;&amp;gt;工具规划&amp;lt;/span&amp;gt;&amp;lt;/li&amp;gt;&amp;lt;li&amp;gt;方案拆解&amp;lt;/li&amp;gt;&amp;lt;/ul&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;357.14\&quot; y=\&quot;1620\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-11\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;工具调用\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;76.78\&quot; x=\&quot;724.1999999999999\&quot; y=\&quot;1470\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-12\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;推理模式\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;76.78\&quot; x=\&quot;805.01\&quot; y=\&quot;1470\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-13\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;thinking模型\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;100\&quot; x=\&quot;1127.84\&quot; y=\&quot;1489\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-15\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;GPU资源\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;400.46\&quot; y=\&quot;1865\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-16\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=17;fontColor=#333333;\&quot; value=\&quot;A100\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;470.46\&quot; y=\&quot;1850\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-17\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=17;fontColor=#333333;\&quot; value=\&quot;H800\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;560.6200000000001\&quot; y=\&quot;1850\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-18\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=17;fontColor=#333333;\&quot; value=\&quot;A6000\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;650.49\&quot; y=\&quot;1850\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-19\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;单机多卡\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;460.47999999999996\&quot; y=\&quot;1720\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-20\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;242\&quot; width=\&quot;250\&quot; x=\&quot;1340\&quot; y=\&quot;1438\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-23\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;模型部署\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1455\&quot; y=\&quot;1418\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-24\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;chat模型\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;83.32\&quot; x=\&quot;1360.03\&quot; y=\&quot;1498.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-26\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;thinking模型\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;100\&quot; x=\&quot;1360.03\&quot; y=\&quot;1538.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-28\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-21\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;n3CkDuzZUbsflOAqb1_X-13\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1110\&quot; y=\&quot;1450\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1160\&quot; y=\&quot;1520\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-29\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-20\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;n3CkDuzZUbsflOAqb1_X-20\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1330\&quot; y=\&quot;1489\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1400\&quot; y=\&quot;1489\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-30\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;全参\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;738.24\&quot; y=\&quot;1370\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-31\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;PEFT\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;859.97\&quot; y=\&quot;1370\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-32\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;n3CkDuzZUbsflOAqb1_X-30\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; target=\&quot;n3CkDuzZUbsflOAqb1_X-31\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;750\&quot; y=\&quot;1470\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;750\&quot; y=\&quot;1510\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-33\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=17;\&quot; value=\&quot;vLLM\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;1360.03\&quot; y=\&quot;1456.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-34\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=17;\&quot; value=\&quot;SGLang\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;1450.03\&quot; y=\&quot;1456.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-35\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;LoRA\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;855.01\&quot; y=\&quot;1505\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-36\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;QLoRA\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;855.01\&quot; y=\&quot;1538\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-37\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;GRPO\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;64.85\&quot; x=\&quot;800.13\&quot; y=\&quot;1590\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-38\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;GSPO\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;64.85\&quot; x=\&quot;870\&quot; y=\&quot;1590\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-39\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-53\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-12\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;680\&quot; y=\&quot;1560\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;680\&quot; y=\&quot;1590\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-40\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;模型加速\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;463.23999999999995\&quot; y=\&quot;1760\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-41\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;\&quot; value=\&quot;zero系列\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;60\&quot; x=\&quot;468.45\&quot; y=\&quot;1784\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-42\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=17;\&quot; value=\&quot;VeRL\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;60.92\&quot; x=\&quot;549.5400000000001\&quot; y=\&quot;1760\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-43\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=17;\&quot; value=\&quot;DeepSpeed\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;95.91\&quot; x=\&quot;624.5500000000001\&quot; y=\&quot;1760\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-46\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;Qwen3\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;1036.65\&quot; y=\&quot;1355\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-47\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;DeepSeek\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;89.97\&quot; x=\&quot;1130.03\&quot; y=\&quot;1355\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-48\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;n3CkDuzZUbsflOAqb1_X-45\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-20\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1186\&quot; y=\&quot;1514\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1241\&quot; y=\&quot;1514\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-49\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;基座模型\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1212.83\&quot; y=\&quot;1320\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-12\&quot; y=\&quot;3\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-50\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;Qwen3-*\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;1360.03\&quot; y=\&quot;1583.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-51\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;Dense\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;79.94\&quot; x=\&quot;1038.34\&quot; y=\&quot;1538\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-52\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;MoE\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;79.94\&quot; x=\&quot;1040.03\&quot; y=\&quot;1575\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-53\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontSize=12;fontColor=#ffffff;\&quot; value=\&quot;Qwen3-0.6B\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;20\&quot; width=\&quot;69.97\&quot; x=\&quot;1165.02\&quot; y=\&quot;1526\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-54\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontSize=12;fontColor=#ffffff;\&quot; value=\&quot;Qwen3-1.7B\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;20\&quot; width=\&quot;69.97\&quot; x=\&quot;1165.02\&quot; y=\&quot;1548\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-55\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontSize=12;fontColor=#ffffff;\&quot; value=\&quot;Qwen3-4B\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;20\&quot; width=\&quot;69.97\&quot; x=\&quot;1165.02\&quot; y=\&quot;1570\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-56\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontSize=12;fontColor=#ffffff;\&quot; value=\&quot;Qwen3-30B-A3B\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;20\&quot; width=\&quot;104.99\&quot; x=\&quot;1045.01\&quot; y=\&quot;1610\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-57\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontSize=12;fontColor=#ffffff;\&quot; value=\&quot;Qwen3-8B\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;20\&quot; width=\&quot;69.97\&quot; x=\&quot;1165.02\&quot; y=\&quot;1594\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-58\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontSize=12;fontColor=#ffffff;\&quot; value=\&quot;Qwen3-14B\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;20\&quot; width=\&quot;69.97\&quot; x=\&quot;1165.02\&quot; y=\&quot;1616\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-59\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;Qwen3-*-Embedding\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;160\&quot; x=\&quot;1360\&quot; y=\&quot;1619.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-60\&quot; parent=\&quot;1\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; value=\&quot;合成数据\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;60\&quot; x=\&quot;468.45\&quot; y=\&quot;1585\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-61\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; value=\&quot;角色模拟\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;69.97\&quot; x=\&quot;1510.03\&quot; y=\&quot;1583.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-62\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;n3CkDuzZUbsflOAqb1_X-61\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;dashPattern=1 2;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-36\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1271\&quot; y=\&quot;1670\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1270\&quot; y=\&quot;1750\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;n3CkDuzZUbsflOAqb1_X-63\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;\&quot; value=\&quot;【2025-12-2】wqw\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;120\&quot; x=\&quot;1350.03\&quot; y=\&quot;1810\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


## 前沿技术


### 阳奉阴违

AI 模型是否真正理解人类的指令与意图？

当前大模型研究的主流观点
- 仅通过「99% 的预训练 + 1% 的后训练」便可使得大模型（LLM、VLM、VLA）被对齐。

但，大模型真的能够被对齐吗？

【2025-7-27】北京大学人工智能研究院研究员、北京智源大模型安全项目负责人`杨耀东`研究团队的研究荣获了 ACL 2025 年度最佳论文奖。
- [ACL'25最佳论文独家解读：大模型有「抗改造」基因，现有后训练范式失灵预警](https://zhuanlan.zhihu.com/p/1934298739834585527)
- 论文标题：[Language Models Resist Alignment: Evidence From Data Compression](https://arxiv.org/pdf/2406.06144)
- 项目地址：[home](https://pku-lm-resist-alignment.github.io)

课题组发现: 语言模型呈现出「**弹性**」特质，主要包括两个方面：
- 抵抗性 —— 预训练模型倾向保留原始分布；
- 回弹性 —— 对齐程度越深，模型在反向微调中越快回归预训练分布。

大模型并非可以任意塑造的「白纸」，其参数结构中存在一种「弹性」机制 —— 该机制源自`预训练`阶段，具备驱动模型分布回归的结构性惯性，使得模型在微调后仍可能「弹回」预训练状态，进而抵抗人类赋予的新指令，导致模型产生**抗拒对齐**的行为。

这意味着对齐的难度远超预期，后训练（Post-training）所需的资源与算力可能不仅不能减少，反而需要与预训练阶段相当，甚至更多。

论文指出：
- 模型规模越大、预训练越充分，其弹性越强，对齐时发生回弹的风险也越高。
- 换言之，目前看似有效的对齐方法可能仅停留在「表面」、「浅层」，要实现深入模型内部机制的稳健对齐仍任重道远。

这一发现对 AI 安全与对齐提出了严峻挑战：
- 模型可能不仅「学不动」，甚至可能「装作学会了」
- 当前 LLMs、VLMs 及 VLAs 的预训练与后训练微调对齐过程面临新的难题。


## LLM 训练模式




### 什么是微调

【2024-3-8】[LLM-SFT-trick](https://zhuanlan.zhihu.com/p/682604566)

微调是指在已经**预训练**好的大型语言模型基础上，使用**特定数据集**进行进一步的训练，使模型适应特定任务或领域。
- 微调主要目的是，完成 知识注入、指令对齐

大模型应用中，指令微调已成为预训练大模型在实际业务应用最重要方式。许多垂直领域模型，都在预训练模型的基础上，通过针对性的指令微调，可以更好地适应最终任务和对齐用户偏好。

指令微调时，会将 **Instruction（指令）** 及对应的**answer**拼接成文本
- 拼接过程中一般会加入【**USER**】、【**BOT**】等角色
- 同时会加入**开始**、**结束**的special token

这样可以转换成一个chat式任务

如翻译任务

```sh
# instruction：
【USER】：将下列内容翻译成英语：｛待翻译文本｝
# answer:
【BOT】：{翻译结果}
# 拼接后的文本：
<bos_token>【USER】：将下列内容翻译成英语：｛待翻译文本｝<special token>【BOT】：{翻译结果} <eos_token>
```

将拼接文本采用预训练任务方式进行自回归预测
- 与预训练的区别：loss的计算，同样使用Cross-Entropy作为loss，指令微调时只会计算answer部分，Instruction部分通过设置ignore_index隐掉。
- 上面的案例中，只会计算 **【BOT】：** 之后的loss。

特定任务改造
- 分类任务: 模型最后添加softmax层。典型案: reward模型。

通过**生成式模**式解决**判别式**任务
- 如**多目标文本分类**问题，采用**指令微调**方式去解决，效果非常好。
- 甚至在7B、3B的base模型上，去生成一个复杂json结构（包含多层结构的标签）依然有效。

### 微调方法

模型微调方法
- 全参微调 Full-tuning, 最传统、彻底的微调方式
- 冻结微调 Freeze-tuning 冻结部分参数微调,只调整模型的顶层，其他不变
- 低秩微调 LoRA 低秩适应
- QLoRA 量化低秩适应


|训练方法|英文|概要|场景|
|----|----|----|----|
|全参微调|Full-tuning|最传统、彻底|数据多、任务难、设备好，追求极致效果|
|冻结微调|Freeze-tuning|只调整模型的顶层|数据少、任务简单、资源有限，快速上手|
|低秩微调|LoRA|低秩适应|万能钥匙，兼顾效率+效果|
|量化低秩微调|量化低秩适应|QLoRA|资源紧张的移动设备|



### 知识注入

【2025-7-27】[大模型训练技术总结2-知识注入分析](https://zhuanlan.zhihu.com/p/1932851943493067040)

微调阶段可有限注入的知识类型包括
- 领域术语与概念（如法律条文、医学术语）
- 任务特定事实（如格式模板、行业表达习惯）
- 时效性**弱**的事实（如历史事件、基础科学原理）等。 

但对那些强时效性知识、复杂学科的逻辑体系、大规模常识体系等则难以注入，只能靠预训练阶段构建

#### 路线图

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;dark-mode&quot;:&quot;auto&quot;,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36\&quot; version=\&quot;29.2.9\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;949\&quot; dy=\&quot;-514\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--20\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;386\&quot; width=\&quot;270\&quot; x=\&quot;673\&quot; y=\&quot;1537\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; value=\&quot;LLM(大模型)训练方式选择\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;33\&quot; width=\&quot;264.5\&quot; x=\&quot;390\&quot; y=\&quot;1450\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--22\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;是\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; y=\&quot;1562.5\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;5\&quot; y=\&quot;6\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--23\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;是\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;436\&quot; y=\&quot;1720\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;3\&quot; y=\&quot;-3\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CKtsSkHedHjP4OW8E3n--47\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=12;\&quot; value=\&quot;【2025-12-29】wangqiwen\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;330\&quot; y=\&quot;1890\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-1\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=#0e8088;shadow=1;fontSize=17;\&quot; value=\&quot;需求场景\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;99.15\&quot; x=\&quot;80\&quot; y=\&quot;1630\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-2\&quot; parent=\&quot;1\&quot; style=\&quot;rhombus;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=none;rounded=0;shadow=1;fontSize=14;fontStyle=1;fontColor=#99004D;\&quot; value=\&quot;实时数据更新？\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;130\&quot; x=\&quot;284\&quot; y=\&quot;1550\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-3\&quot; parent=\&quot;1\&quot; style=\&quot;rhombus;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=none;rounded=0;shadow=1;fontSize=14;fontStyle=1;fontColor=#99004D;\&quot; value=\&quot;知识深度高？\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;130\&quot; x=\&quot;284\&quot; y=\&quot;1700\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-4\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;hK1oHzIBLq9t15zctzZD-1\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;hK1oHzIBLq9t15zctzZD-2\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;220\&quot; y=\&quot;1655\&quot; /&gt;\n              &lt;mxPoint x=\&quot;220\&quot; y=\&quot;1580\&quot; /&gt;\n            &lt;/Array&gt;\n            &lt;mxPoint x=\&quot;309\&quot; y=\&quot;1560\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;360\&quot; y=\&quot;1560\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-5\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;hK1oHzIBLq9t15zctzZD-1\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;hK1oHzIBLq9t15zctzZD-3\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;220\&quot; y=\&quot;1655\&quot; /&gt;\n              &lt;mxPoint x=\&quot;220\&quot; y=\&quot;1730\&quot; /&gt;\n            &lt;/Array&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;1570\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;421\&quot; y=\&quot;1570\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-8\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;领域RAG\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;35\&quot; width=\&quot;114.85\&quot; x=\&quot;696\&quot; y=\&quot;1562.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-9\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;hK1oHzIBLq9t15zctzZD-2\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=0.954;exitY=0.475;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitPerimeter=0;\&quot; target=\&quot;hK1oHzIBLq9t15zctzZD-8\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;615\&quot; y=\&quot;1580\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;541\&quot; y=\&quot;1590\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-10\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;hK1oHzIBLq9t15zctzZD-3\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; target=\&quot;hK1oHzIBLq9t15zctzZD-11\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;420\&quot; y=\&quot;1730\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;481.5\&quot; y=\&quot;1680\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-11\&quot; parent=\&quot;1\&quot; style=\&quot;rhombus;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=none;rounded=0;shadow=1;fontSize=14;fontStyle=1;fontColor=#99004D;\&quot; value=\&quot;资源受限？\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;130\&quot; x=\&quot;491\&quot; y=\&quot;1700\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-12\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;LoRA-CPT+Fact-based SFT\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;35\&quot; width=\&quot;224\&quot; x=\&quot;696\&quot; y=\&quot;1712.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-13\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;hK1oHzIBLq9t15zctzZD-11\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; target=\&quot;hK1oHzIBLq9t15zctzZD-12\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;476\&quot; y=\&quot;1740\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;547\&quot; y=\&quot;1740\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-14\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;hK1oHzIBLq9t15zctzZD-3\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;hK1oHzIBLq9t15zctzZD-15\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;420\&quot; y=\&quot;1820\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;481.5\&quot; y=\&quot;1770\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-15\&quot; parent=\&quot;1\&quot; style=\&quot;rhombus;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=none;rounded=0;shadow=1;fontSize=14;fontStyle=1;fontColor=#99004D;\&quot; value=\&quot;资源受限？\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;130\&quot; x=\&quot;491\&quot; y=\&quot;1810\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-16\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;LoRA-FT\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;35\&quot; width=\&quot;114\&quot; x=\&quot;696\&quot; y=\&quot;1822.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-17\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;hK1oHzIBLq9t15zctzZD-15\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; target=\&quot;hK1oHzIBLq9t15zctzZD-16\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;476\&quot; y=\&quot;1850\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;547\&quot; y=\&quot;1850\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-18\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;否\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;1780\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint y=\&quot;5\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-19\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;全参 CPT+Fact-based SFT\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;35\&quot; width=\&quot;224\&quot; x=\&quot;696\&quot; y=\&quot;1762.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-20\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;hK1oHzIBLq9t15zctzZD-11\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;hK1oHzIBLq9t15zctzZD-19\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;620\&quot; y=\&quot;1771.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;546\&quot; y=\&quot;1781.5\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-21\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;是\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;640\&quot; y=\&quot;1720\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;3\&quot; y=\&quot;-3\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-24\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;否\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;563\&quot; y=\&quot;1767\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;2\&quot; y=\&quot;2\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-25\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; value=\&quot;全参-FT\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;35\&quot; width=\&quot;114\&quot; x=\&quot;696\&quot; y=\&quot;1880\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-26\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;hK1oHzIBLq9t15zctzZD-15\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;hK1oHzIBLq9t15zctzZD-25\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;621\&quot; y=\&quot;1897.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;547\&quot; y=\&quot;1907.5\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-27\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;是\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;643\&quot; y=\&quot;1830\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;3\&quot; y=\&quot;-3\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;hK1oHzIBLq9t15zctzZD-28\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; value=\&quot;否\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;566\&quot; y=\&quot;1877\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;2\&quot; y=\&quot;2\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


#### 方法总结

可注入的知识类型

| 类型                   | 示例                     | 技术方案              | 局限性                 |
|------------------------|--------------------------|-----------------------|------------------------|
| 领域术语与概念(原子事实) | 法律条文、医学术语       | CPT* + Fact-based SFT | 覆盖率依赖数据量       |
| 任务特定事实           | 合同格式、行业表达习惯   | SFT                   | 无法更新底层知识表示   |
| 时效性弱的事实         | 历史事件、科学原理       | RAG                   | 无法处理实时更新       |
| 领域内浅的逻辑链       | "症状→诊断"因果关联      | CPT+逻辑链数据混合    | 泛化能力有限           |

不同的微调方法对领域知识注入的能力有区别
- SFT仅能低层次的补充浅层领域术语(如法律合同模板、医疗条款)等，
- LoRA/QLoRA几乎不能新增知识，其核心价值主要体现在高效适配模型行为，如调整模型表达风格（如对话的正式程度及语气）、优化输出格式（如生成报告能力），强化任务安全边界（如敏感词及其他有害内容的过滤）等。
- 增量预训练（CPT） 基于已有预训练模型，通过少量领域数据进一步优化，减少训练成本。增量预训练过程可注入新的结构化领域知识，如法律条文、医学条款等。在预训练时必须使用全参数训练，但在增量训练中主要使用部分参数训练。 增量预训练与预训练相比，在训练数据上预训练数据量更大、无需标注，强调多样性，而CPT数据少，部分情况下可以标注(如逻辑链的提升)，聚焦垂直领域。
- Fact-based SFT可以注入大量原子事实

总结

| 方法              | 知识注入能力       | 核心作用                                   | 典型案例                 |
|-------------------|--------------------|--------------------------------------------|--------------------------|
| SFT               | ★★（浅层术语）| 优化任务输出格式                           | 法律合同模板生成         |
| LoRA/QLoRA        | ★（几乎无新增）| 调整风格/安全边界（语气、过滤敏感词）| 客服话术轻量化适配       |
| CPT               | ★★★★（术语+逻辑） | 重构底层表示空间                           | 医疗术语覆盖率>95%|
| Fact-based SFT    | ★★★（原子事实）| 注入结构化领域知识                         | 法律条款原子事实学习     |

微调时数据量通常仅为预训练的千分之一甚至更低，无法重构底层知识表示。且新知识的注入容易覆盖原有的通用能力。

微调技术能不能注入新知识，
- 能注入：微调可补充很有限的领域知识（术语/事实/模板）；通过增量预训练（CPT）和Fact-based SFT可以实现高效注入。
- 不能完全依赖：动态知识（实时数据）和体系化新知识（如全新学科）仍需依赖RAG或预训练重构。
- 遗忘风险：注入新知识需警惕遗忘风险，建议采用数据回放和参数约束技术平衡新旧能力

所以，若需注入高频更新知识（如金融行情），优先选择RAG；若需深度领域专业化，采用CPT+Fact-based SFT组合；轻量调整则用LoRA避免资源浪费

增量预训练（Continuous Pre-training, CPT）和传统微调（Fine-tuning）在知识注入效果上存在显著差异，主要体现在知识类型、数据效率、资源消耗、任务适应性等方面。

增量预训练与传统微调在知识注入上的核心差异

| 维度               | 增量预训练（CPT）| 传统微调（Fine-tuning）|
|--------------------|------------------------------------------|------------------------------------------|
| 知识注入深度       | 重构底层知识表示，领域术语覆盖率>90%| 仅调整表层任务模式，术语覆盖率<60%|
| 数据效率           | 需百万级领域Token（如10GB医学文献）| 仅需千级标注样本（如100条问答对）|
| 灾难性遗忘         | 领域数据占比>20%时，通用能力保留率>85%| 通用能力保留率<50%（因任务数据过拟合）|
| 时效性知识支持     | 可注入最新领域知识（如2025年政策）| 依赖预训练知识截止时间，无法更新动态知识 |
| 计算资源消耗       | 需数万GPU小时（如医疗模型训练）| 仅需百级GPU小时（如LoRA微调）|
| 零样本/少样本能力  | 零样本视觉定位准确率75.1%（RefCOCO）| 零样本任务准确率通常<40%|


分析
- 知识注入深度与类型
  - CPT： 通过海量领域数据（如医学文献、法律条文）重构模型底层表示，术语覆盖率可达95%以上。
  - 传统微调： 仅在任务层调整参数（如分类头），无法改变预训练知识结构。注入新术语需重复训练，覆盖率不足60%。
- 数据效率与标注成本
  - CPT： 依赖无标注领域数据（如企业文档），数据清洗成本低，但需TB级数据量。
  - 传统微调： 需精细化标注数据（如指令-回答对），百条数据即可适配简单任务，标注成本高昂。
- 灾难性遗忘与通用能力保留
  - CPT： 混合通用数据（比例1:5~1:10）可缓解遗忘，通用任务性能保留率>85%。
  - 传统微调： 任务过拟合导致通用能力骤降，如法律微调后数学推理能力下降50%。
- 动态知识更新能力
  - CPT： 支持定期注入新数据（如金融财报），但需全模型重训练，滞后性明显。
  - 传统微调： 无法更新预训练截止时间后的知识，依赖外部检索（如RAG）。
- 跨任务泛化性
  - CPT： 增强模型领域内泛化能力（如医疗子领域诊断准确率波动<5%）。
  - 传统微调： 任务特异性强，跨任务性能衰减>30%（如从分类转向生成任务）

适用场景及推荐方案

| 场景               | 推荐方案          | 原因                                                 |
|--------------------|-------------------|------------------------------------------------------|
| 深度领域专业化     | CPT + Fact-based SFT | 重构知识结构，支持复杂术语推理（如医疗诊断）|
| 轻量任务适配       | LoRA微调          | 低成本调整输出格式，保留通用能力（如客服话术优化）|
| 动态知识需求       | RAG + 微调        | 实时检索更新知识，微调优化任务逻辑（如金融分析）|
| 零样本/少样本场景  | CPT + 提示工程    | 激活预训练知识，减少标注依赖（如跨模态定位）|

技术选型建议
- CPT优势：深度重构知识表示，支持术语级知识注入与跨任务泛化，适合垂直领域深度专业化。
- 传统微调优势：低成本适配特定任务格式，适合轻量级场景快速落地。

取舍
- 追求知识深度且可以承担计算成本 → 选CPT
- 追求任务敏捷性且能接受知识局限性 → 选微调。

实践建议
- 对时效性弱的重知识领域（如医疗、法律），为了做到领域的深度专业化，优先CPT+Fact-based SFT；
- 对动态知识需求的场景（如金融、新闻），结合RAG与微调；
- 轻量场景直接用LoRA以减少资源消耗，仅做低成本的输出格式和话术优化等，保留通用能力；
- 对于零样本或少样本的场景，用CPT+提示工程激活预训练知识，减少标注依赖。
- 如果采用CPT又要增强逻辑推理，需在数据中增加逻辑链的描述文本，如判决推理，疾病诊断依据等，以强化模型对逻辑推理的能力。也可CPT学习领域知识+SFT强化逻辑推理能力的方式。

【2025-8-30】阿联酋、东北大学、人大高瓴、字节、武大推出 知识注入方法综述
- 论文 [Injecting Domain-Specific Knowledge into Large Language Models: A Comprehensive Survey](https://arxiv.org/pdf/2502.10708)

尽管在通用任务中表现出色，但在需要领域知识的任务中表现不足。

知识注入的优势:
- 提高特定任务的准确性和可靠性。
- 动态适应新信息或知识库。

应用实例: 
- 生物医学 LLMs 在医疗诊断和法规遵从方面表现出色，材料科学领域的模型在材料属性预测和发现方面取得进展。

4种主要方法：
- 动态知识注入: RAG，实时检索和整合外部知识。
- 静态知识嵌入: Full Finetune 全参微调，在训练或微调时将领域知识嵌入模型。
- 模块化适配器: PEFT 如 LoRA，在不改变主模型参数的情况下存储和利用外部知识。
- 提示优化: Prompt Engineering 提示工程，通过精心设计的提示引导模型利用现有知识。

示例图

<img width="1125" height="230" alt="image" src="https://github.com/user-attachments/assets/5f92a25a-3a3a-4d1c-a671-47648dfdb880" />


各方向研究热度

<img width="1039" height="547" alt="image" src="https://github.com/user-attachments/assets/7d24a6ee-0d62-42d4-906d-450a1ccf6050" />


知识注入范式


| 范式               | 训练成本                          | 推理速度               | 局限性                          |
|--------------------|-----------------------------------|------------------------|---------------------------------|
| 动态知识注入       | 无，但需依赖检索模块              | 因检索延迟而变慢       | 严重依赖检索质量                |
| 静态知识嵌入       | 高（需预训练或微调）              | 无额外成本             | 知识固定；存在灾难性遗忘风险    |
| 模块化适配器       | 低（仅训练小部分参数）            | 几乎无影响             | 对训练数据质量敏感              |
| 提示优化           | 无                                | 几乎无影响             | 耗时费力；仅局限于模型已有知识  |


另一个维度对比

| 知识注入范式       | 核心概念            | 训练阶段          | 推理阶段        | 优点        | 挑战       |
|--------------------|-------------------|-------------------|--------------------|------------|----------------|
| 静态知识注入       | 将领域特定知识嵌入模型参数中，优化后得到更新参数∆θ     | 基于领域特定知识对基础模型进行微调，优化并更新模型参数  | 无需额外检索或外部知识调用，直接使用更新后的参数生成输出 | 推理速度快，性能强       | 知识更新成本高（需微调），扩展性差（嵌入大规模或频繁变化的知识库计算成本高） |
| 模块化知识适配器   | 引入小型可训练模块（适配器），与基础模型结合存储领域特定知识，节省计算资源 | 冻结基础模型参数θ，仅训练适配器参数φ，通过最小化损失函数完成优化          | 加载基础模型与训练好的适配器，使用增强后的模型生成输出   | 参数高效，无需修改原始模型权重，保留原有知识并融入新领域信息 | 需设计新架构组件，确定超参数（如适配器大小和数量），增加模型复杂性和训练难度 |
| 提示优化           | 不依赖外部知识，通过精确提示引导模型利用内部已有知识，不改变模型参数       | 无专门训练过程，无需调整任何模型参数                                      | 直接使用精确提示和任务输入生成输出，调用模型内部已有知识 | 无需外部知识检索，充分利用模型内部知识 | 对提示词设计要求高，适用范围受限（仅适用于无需外部知识增强的任务），复杂任务适配性差 |



### LoRA

LoRA在CPT增量预训练和SFT微调中的对比

在增量预训练中，LoRA-CPT由于在效果和成本之间取得良好平衡，已成为当前主流方案。特别是对于资源有限的研究团队和公司来说特别实用。
- 全参数CPT虽然效果更好但成本太高，一般只有大型机构才会使用。
- 其他方法如Adapter和Prefix Tuning也有应用，但不如LoRA普及

LoRA 优势
- **多租户**部署（同一模型可同时加载多个适配器）
- **低显存**需求
- 快速加载和迁移。

由于这些特性，2021 年诞生以来迅速流行。

#### LoRA vs FullFT

【2025-9-29】Thinking Machines 最新研究：
- 官方技术博客 [LoRA Without Regret](https://thinkingmachines.ai/blog/lora/)
- [解读](https://zhuanlan.zhihu.com/p/1956510153307325822)

![](https://pic2.zhimg.com/v2-ad76e44d8f271c08ba13cc3afe45ed29_1440w.jpg)

LoRA 能否匹敌 FullFT? 没有一致答案。
- 学界: 类似**预训练**的大规模数据场景下，LoRA 性能会逊于 FullFT ，因为<span style='color:blue'>数据规模往往超出 LoRA 参数容量</span>。
- 但在后训练任务中，数据规模通常处于 LoRA 容量可覆盖的范围，核心信息能够被保留。

- 小数据量任务上，LoRA 与 FullFT 几乎没有差距，完全可以对齐；
- 大数据量任务上，LoRA 容量不足，承载不了过多新知识，表现略显吃力；
- 而在强化学习任务里，哪怕 LoRA rank=1 这么小的设定，也能跑出与全量微调接近的效果。

LoRA 的使用位置也有讲究。
- 只加在注意力层并不理想，覆盖所有层（尤其 MLP/MoE）效果更佳。
- LoRA 在大 batch size 下，比 FullFT 更容易掉性能；
- LoRA 学习率和超参数规律与 FullFT 不同，需要单独调优。

LoRA 能实现与 FullFT 相当的效果？

LoRA 要与 FullFT 接近，必须满足两个条件：
- 作用于**所有层**，特别是 MLP/MoE 层，因为这些层承载了模型绝大部分参数。
- **容量不受限制**，可训练参数必须足够容纳数据中所需的信息量。

仅在 attention 层使用 LoRA 会导致训练速度下降，这可以用经验神经切线核（eNTK）解释：参数最多的层对训练动态影响最大，LoRA 覆盖所有参数层，才能保持 FullFT 的训练行为。

实验显示，只要关键细节得到妥善处理，LoRA 不仅能匹配 FullFT 的样本效率，还能最终达到相似的性能水平。
- 在小到中等规模的指令微调和推理任务中，LoRA 表现与FullFT 相媲美。
- 然而，当数据规模超出 LoRA 参数容量时，其表现将落后于 FullFT，这种差距主要体现在训练效率的下降，而非无法继续优化。性能下降的程度与模型容量和数据规模密切相关。
- LoRA 对大批量训练的容忍度低于 FullFT 。当批量规模超过一定阈值时，损失值会明显上升，这种现象无法通过提升 LoRA 的秩（rank）来缓解，因为它源自矩阵乘积参数化的固有训练动力学，而非原始权重矩阵的直接优化。

即便在小数据场景，将 LoRA 应用于所有权重矩阵，尤其是 MLP 与 MoE 层，均能获得更优表现。相比之下，仅对注意力层进行 LoRA 调整，即使保持相同可训练参数量，也无法达到同样的效果。

在强化学习任务中，即使 LoRA 的秩（rank）极低，其性能仍可接近 FullFT 。这与基于信息论的推断一致：强化学习对模型容量的需求相对较低。


#### 全参数 CPT（Full-parameter CPT）

- 原理：解冻模型全部参数，用领域数据（如医学文献、法律条文）重新预训练，重构底层知识表示。
- 优势：知识注入深度高，术语覆盖率＞90%，适合深度领域专业化（如医疗诊断逻辑）。
- 局限：计算成本极高（需万级GPU小时），易引发灾难性遗忘（通用能力保留率＜50%）。

#### LoRA-CPT（低秩适配增量预训练）

- 原理：冻结原参数，通过低秩矩阵（ΔW=BA）学习领域扰动，仅调整0.1%-1%参数。
- 优势：
  - 资源效率高：百级GPU小时即可完成训练，适合边缘设备部署。
  - 抗遗忘性强：通用能力保留率＞85%。
- 局限：仅能注入原子事实和浅层逻辑，复杂推理能力弱（如跨领域因果分析）

全参数增量预训练中需要的计算成本和数据成本均极高， LoRA-CPT则因其平衡性成为主流方案。在LoRA-CPT和基于LoRA的SFT中均有LoRA的身影，但他在CPT和SFT中发挥的作用是有差异的。
- SFT中LoRA通过冻结原参数，用低秩矩阵微调输出逻辑，依赖的是少量标注的指令问答数据，核心目标是调整模型行为，此间并没有新知识注入。
- LoRA-CPT通过海量无标注的领域文本重构底层表示空间，可以注入领域新知识，可学习原子知识与浅层逻辑。

LoRA如何在CPT中实现有限知识注入

尽管LoRA不改变原模型权重，但在CPT中仍能实现**有限知识注入**，原因如下：
- 表示空间的重构
  - CPT使用领域文本（如法律条文）继续预训练任务（如掩码语言建模），模型需预测被掩盖的领域术语（如“不可抗力”）。
  - LoRA的增量矩阵（A、B）在训练中捕捉领域词汇共现关系，间接重构词嵌入空间。
  - 例：医疗CPT中，术语“心肌梗死”与“心电图”的共现关系通过低秩矩阵编码，使模型理解其关联。
- 本征维度的知识压缩
  - 大模型存在本征维度（Intrinsic Dimension）：复杂知识可通过低秩矩阵近似表达。
  - 领域知识中的原子事实（如“《民法典》第584条定义违约赔偿”）可被秩（rank）仅为8的LoRA矩阵捕获，无需全参数更新。
- 灾难性遗忘的规避
  - LoRA冻结原参数，仅通过增量矩阵吸收新知识，避免传统CPT中领域数据覆盖通用知识的问题。
  - 对比：全参数CPT需混合20%通用数据维持基础能力，而LoRA-CPT无需此操作

总结
- SFT中：LoRA是**行为调节器**，仅优化输出模式而不扩展知识边界。
- CPT中：LoRA成为**知识压缩器**，通过低秩矩阵编码领域术语与浅层逻辑，但受限于秩的大小，无法承载复杂知识体系。
- 核心取舍：
  - 若追求**深度知识注入**（如医疗诊断逻辑），需全参数CPT；
  - 若需**快速轻量适配**（如客服话术更新），LoRA-CPT是资源最优解


### SFT

大模型面临知识更新问题，特别是对于发生在模型知识截止日期之后的事件

RAG 让大模型具备外部知识的能力，但规避了将新知识直接整合到模型本身的核心问题

如何从文档中构建训练数据集，通过简单的SFT技术促进新知识学习？


SFT 主要步骤：
1. 数据收集：收集大量的标注数据，由人类专家根据特定任务进行标注。
2. 模型训练：对预训练模型进行微调，特定任务上表现更好。
3. 评估和优化：通过验证集评估模型性能，并根据结果进行优化。

SFT 优点是相对简单直接，只需要高质量的标注数据即可。

然而，SFT也有一些局限性，比如
- 对标注数据的质量和数量要求较高。

#### RFT

`RFT`（Rejection sampling Fine-Tuning）和 `SFT`（Supervised Fine-Tuning）是两种用于微调机器学习模型的方法

RFT 更为复杂的微调方法，主要步骤：
1. 数据生成：首先使用预训练模型生成大量的**候选输出**。
2. 筛选过程：通过某种筛选机制（如人工评审或自动评分系统）从这些候选输出中挑选出**高质量**的样本。
3. 模型训练：使用筛选后的高质量样本对模型进行微调。

RFT关键在于筛选过程，显著提高数据的质量，从而提升模型的性能。

筛选机制可以是人工，基于某种自动化评分系统。

RFT 核心思想
- 利用已有监督模型来生成新的数据样本，如果将其用于数学推理任务，那么可以通过选择正确的推理路径来增强模型的训练数据集
- 【2023-9-13】阿里巴巴论文 [SCALING RELATIONSHIP ON LEARNING MATHEMATICAL REASONING WITH LARGE LANGUAGE MODELS](https://arxiv.org/pdf/2308.01825)
- 代码 [gsm8k-ScRel](https://github.com/OFA-Sys/gsm8k-ScRel)
- 解读 [RFT（拒绝采样微调）：提升大模型推理能力](https://www.zhihu.com/tardis/bd/art/703848627)

RFT 针对给定 prompt，产生一些包含 cot 的 response ，再通过 verifier 判断 response 是否正确，作为信号来指导模型进行参数更新。
- 如果把 verifier 换成 reward_model ，那就是最传统的基于 PPO 的 RLHF。
- RFT 和 RLHF 唯一区别: return (reward 信号) 是通过 verifier 算出来的，而不是一个 reward_model 计算出来

OpenAI 介绍 RFT：“RFT 使开发者和机器学习工程师能够创建专门针对特定复杂、特定领域任务的专家模型”。

RFT 的价值：
- 只要能定制好任务的 verifier，那么 RFT 便可以在这个新领域场景，以十分之一或更少的数据，轻松超过 SFT 的结果

字节 ReFT 是 OpenAI RFT 在数学任务上的一个极简版实现方案


二者区别

1. 数据来源：
- SFT：依赖于预先标注好的高质量数据。
- RFT：通过生成大量候选输出，然后筛选出高质量样本。

2. 数据质量控制：
- SFT：数据质量主要依赖于标注过程的质量控制。
- RFT：通过筛选机制来确保数据质量，即使初始生成的数据质量不高，也可以通过筛选提高。

|方法|数据源|质量控制||
|---|---|---|---|
|SFT|预标注的高质量数据|标注过程的质量控制||
|RFT|生成大量候选输出，然后筛选出高质量样本|筛选机制来确保数据质量||

RFT具有以下几点优势：
1. 数据增强的有效性：RFT通过拒绝采样的方式，使用监督模型生成并收集正确的推理路径作为额外的微调数据集。这种方法可以在不增加人工标注工作量的情况下，增加数据样本，从而提高模型性能。
2. 推理路径的多样性：RFT特别强调通过增加不同的推理路径来提高LLMs的数学推理能力。这意味着RFT能够提供多种解决问题的方法，有助于模型在面对新问题时有更好的泛化能力。
3. 对性能较差模型的提升效果：论文中提到，RFT对于性能较差的LLMs提升更为明显。这表明RFT可能是一种更为有效的改进手段，特别是对于那些需要显著提高推理能力的模型。
4. 组合多个模型的优势：RFT可以通过组合来自多个模型的拒绝样本来进一步提升性能。这种方法使得LLaMA-7B在GSM8K数据集上的准确率从SFT的35.9%显著提高到49.3%。
5. 计算资源的经济性：尽管RFT在生成样本时可能需要较多的计算资源，但在训练阶段相比从头开始预训练一个LLM来说，它是一种更为经济的方法。这使得RFT成为一种可行的、成本效益更高的改进模型性能的手段。
6. 减少过拟合：RFT通过引入多样化的推理路径，有助于减少模型在训练数据上的过拟合，特别是在大型模型中。


#### Fact-based SFT

[利用监督式微调（SFT），向大模型注入新知识，无需检索增强生成(RAG)](https://zhuanlan.zhihu.com/p/692706105)

【2024-4-2】微软提出新型数据生成方法：Fact-based 生成方法，通过监督式微调（SFT）实现了大模型新知识的有效注入
- [INJECTING NEW KNOWLEDGE INTO LARGE LANGUAGE MODELS VIA SUPERVISED FINE-TUNING](https://arxiv.org/pdf/2404.00213)

点评
- 论文重点是数据生成方法，然后LoRA微调。“注入知识”确实不大合适

两种生成策略：基于标记（token-based）和基于事实（fact-based）。
- 基于**标记**的数据集生成策略：
  - 首先创建由手动编写的问答对组成的初始问题库。
  - 随后，通过计算文档各部分的标记数量，并用GPT-4生成足够的问答对，直到生成的标记数量超过源部分的十倍。
  - 这种方法生成了1倍、5倍和10倍规模的数据集，以及评估集。
  - 然而，这种方法可能无法确保新知识在文档中的均匀覆盖。
- 基于**事实**的数据集生成策略
  - 首先查询GPT-4从文档中提取出**原子事实**列表。
  - 然后，为每个事实生成10个独特的问答对，确保这些问答对不重复，并在问题库中是唯一的。
  - 这种方法允许模型更均匀地关注每个事实，从而提高了知识吸收的效率。基于事实的数据集同样生成了1倍、5倍和10倍规模的数据集，以及相应的评估集。

另外，在生成数据集时，也注重多样性和覆盖率，以避免过拟合，并通过GPT-4对生成的问题和答案进行二元评估来确定其正确性。

基于事实的数据集进行SFT，模型在问答任务中的表现有**显著**提升。这验证了SFT方法在提高模型处理超出领域、超出知识截止日期的知识方面的有效性。尽管SFT模型在所有情况下都没有超过RAG模型的性能，但在缩小与RAG性能差距方面取得了进展，尤其是在10x数据集规模下。


#### SFT VS RLHF


【2001-11-15】Rich Sutton: Verification, the key to AI

【2025-5-26】谷歌 DeepMind 首席科学家 [Denny Zhou](https://dennyzhou.github.io/) 在斯坦福CS25中表示
- SFT不能很好地泛化且推理不行，盲目扩展没有太大帮助。
- RL 微调最关键的是可靠的验证器，而不是RL算法

【2024-8-30】
- [SFT局限性](https://zhuanlan.zhihu.com/p/717275921)
- [对SFT与RLHF两种训练方式的一些个人理解与问题](https://zhuanlan.zhihu.com/p/29191363988)

为什么要做 rlhf，sft 不够吗？
- sft 无法提供负反馈，但 RLHF 有
  - 只知道 next_token 出什么是正确的，而不知道 next_token 出什么是错误的。无论 sft 语料如何构造，都无济于事，模型不知道“什么 token 是不能生成的”。
  - 间接解释了另外一个现象：为什么 sft 数据多样性很重要。sft 一直在通过“孤立”来降低错误 token 的出现概率。
  - 但 rlhf 有：reward_model 像教官，续写出某个不应该出的 token，就抽你，抽到你不敢写这个token 为止
- sft 不具有“向后看”的能力
  - 放大了 transformer 单向注意力结构的缺陷。sft 训练过程中，每个 token 都只看得见前面的 token。
  - sft 更新某个 token 概率时，只参考前面信息，**局部有偏**的训练方法。
  - 但 rlhf 或 dpo 并不是这样，每个 token 更新概率时，都观察到整个 sentence 的，因而理论上，rlhf 的训练方法能带来更高的训练上限。
  - sft 的 loss 是平均 loss， rlhf 的 loss 是加权 loss。至于怎么加权，去问 reward_model 和 critic_model。

除非 sft 训练方式发生改变（比如每个 token 的 loss，不再是算术平均），否则 rlhf 还是一个不可取代的环节。并不是 sft 不能和 reward_model 进行配合，而是 sft 本身的局限性实在太大了。

微调方法的本质思考
- SFT 训练数据都是**正确** next token，<span style='color:red'>无法提供负反馈</span>，模型不知道“什么 token 是不能生成的”
- SFT 是 **token 反馈粒度**，可能会将**局部错误**的数据学习到，导致**幻觉**出现
- sft 反馈粒度是 **token**，rlhf 反馈粒度是**整个文本**。
  - 所以, sft 只能教会模型**做正确的事**，每条样本都赋予同样权重的惩罚，rlhf 更倾向于考虑**整体影响**。

模型SFT训练过程中, 模型输出错误结果，与answer计算得到的Loss值较大，通过反向传播降低模型输出错误结果的概率以降低Loss，是否是一种学习到了负反馈？

确实是一种负反馈，但是与RLHF的负反馈不同
- SFT 目的是**拟合模型与训练数据的分布**
- 负反馈的作用是**纠正模型输出偏离数据分布的行为**

最终的结果是与训练数据中的所有正确token相同，SFT模型依旧无法知道哪些token是错误的。而由于SFT训练数据毕竟是有限的，在实际使用中还是会输出错误token；

RLHF 负反馈是基于reward模型动态得到的，模型能够在训练过程中知道哪些token是错误的，是不能生成的，最终得到的模型能够避免生成错误token。

如果只使用 chosen answer 来进行 SFT, 是否可以替代RLHF？
- 不可以，本质上还是没有rejected样本参与训练，模型无法学习到哪些内容不能输出

如果通过修改Prompt的方式将rejected answer数据也加入到训练中，是否可以用SFT替代RLHF？
- 不可以，难以构建合理的prompt，如果是简单的 `(prompt + “下面输出错误答案”, rejected answer)` 样本数据，SFT模型还是无法学习到哪些内容不能输出，实际使用中也没有人会这么问问题

如果在 SFT 过程中添加 rejected answer 相关的loss是否可以替代RLHF？
- 应该可以，DPO其实就是类似这样的思想


### 持续学习

【2024-2-14】[综述：大语言模型的持续学习](https://zhuanlan.zhihu.com/p/681583249)
- 【2024-2-7】论文 [Continual Learning for Large Language Models: A Survey](https://arxiv.org/pdf/2402.01364.pdf)

大模型的持续学习: LLM随时间推移从持续的数据流中学习。

尽管很重要，但直接将现有的持续学习设置应用于大型语言模型并非易事。

论文现在为大型语言模型的持续学习提供了一个前瞻性的框架，然后提出了该领域研究的分类。
- ![](https://pic4.zhimg.com/v2-62de3ee1e84d578814ffe7ee70232cbb_1440w.jpg)

涉及阶段
- ![](https://pic4.zhimg.com/v2-deeb546d8f611f2685d7b5deb35600e7_r.jpg)

持续学习与不同训练阶段相结合，包括`持续预训练`(CPT)、`持续指令调优`(CIT)和`持续校准`(CA)。
- 持续预训练阶段旨在自主监督地进行一系列语料库上的训练，以丰富大型语言模型的知识并适应新领域。
- 持续指令调优阶段在监督的指令遵循数据流上微调大型语言模型，旨在让大型语言模型遵循用户的指令，同时将获得的知识转移到后续任务中。
- 为应对不断变化的人类价值观和偏好，持续校准(CA)试图随时间连续校准大型语言模型与人类价值观。尽管可以在每个阶段顺序地对大型语言模型进行持续学习，但持续学习的迭代应用也使得在不忘记从前阶段学习的能力和知识的情况下，在阶段之间进行转移至关重要。例如，论文可以在经过指令调优的模型或校准过的模型的基础上进行持续预训练。
- 但是，论文不希望大型语言模型失去遵循用户指令和与人类价值观保持一致的能力。因此，如图2所示，论文使用不同颜色的箭头来显示阶段之间的迁移。

分类
- 持续预训练(Continual Pre-training，CPT)
- 持续指令调优(Continual Instruction Tuning，CIT)
- 持续校准(Continual Alignment，CA)

![](https://pica.zhimg.com/v2-1ca48611546debf4ebd231f69fcc34ae_1440w.jpg)

![](https://pic3.zhimg.com/v2-c04b0d9f99e70634766fbeb68afd1666_1440w.jpg)

#### 持续预训练(Continual Pre-training，CPT)

- 更新**事实**的CPT包括适应大型语言模型以学习新事实知识的工作。
- 更新**领域**的CPT包括定制大型语言模型以适应医学和法律等特定领域的研究。
- **语言扩展**的CPT包括扩展大型语言模型支持的语言的研究。

#### 持续指令调优(Continual Instruction Tuning，CIT)

- **任务**增量CIT包含在一系列任务上微调大型语言模型并获得解决新任务的能力的工作。
- **领域**增量CIT包含在指令流上微调大型语言模型以解决特定领域任务的方法。
- **工具**增量CIT包含持续教大型语言模型使用新工具解决问题的研究。

#### 持续校准(Continual Alignment，CA)

- 持续**价值**校准包括持续校准大型语言模型以遵守新的伦理指南和社会规范的研究。
- 持续**偏好**校准包括适配大型语言模型以动态匹配不同人类偏好的工作。


### 训练方法


微调方法
- 微调方法分为**全参数微调**（Full Fine-tuning）、**部分参数微调**（Repurposing）
- 全微调方法：SFT
  - 作用: 领域价值对齐
  - 作用: Function Call 工具调用、推理模式适配 (thinking/no_thinking)
- 部分微调方法：LoRA、Adapter、Prefix-tuning、P-tuning、Prompt-tuning 、Freeze-tuning 等。

受GPT论文影响，大模型通用训练模式是**三阶段**训练模式：第一阶段 `pre-train`，第二阶段 `SFT`，第三阶段 `RLHF`。
- 三阶段训练分别得到 **base模型** 以及 **chat模型**
- **chat模型**在**base模型**基础进行**通用任务**的`SFT`以及`RLHF`，使模型具备了对话能力、推理能力、用户偏好对齐、以及其他的NLU的能力。

SFT 训练模式
- 模式一：基于 base模型 + 领域任务的SFT；
- 模式二：基于 base模型 + 领域数据 continue pre-train + 领域任务SFT；
- 模式三：基于 base模型 + 领域数据 continue pre-train + 通用任务SFT + 领域任务SFT；
- 模式四：基于 base模型 + 领域数据 continue pre-train + 通用任务与领域任务混合SFT；
- 模式五：基于 base模型 + 领域数据 continue pre-train（混入SFT数据） + 通用任务与领域任务混合SFT；
- 模式六：基于 chat模型 + 领域任务SFT；
- 模式六：基于 chat模型 + 领域数据 continue pre-train + 领域任务SFT

根据领域任务、领域样本、业务需求选择合适的训练模式。
- a. 是否需要 continue pre-train
  - 大模型的知识来自 pre-train 阶段
  - 如果领域任务数据集与 pre-train 数据集**差异较大**(如领域任务数据来自公司内部)，pre-train 训练样本基本不可能覆盖到，那一定要进行 continue pre-train。
  - 如果领域任务**数据量较大**（token在1B以上），并只追求**领域任务**效果，不考虑通用能力，建议进行continue pre-train。
- b. 选择 chat模型 还是 base模型
  - 如果有好的base模型，在base模型基础进行领域数据的SFT, 与在chat模型上进行SFT，效果上差异不大。
  - 基于**chat模型**进行领域SFT，很容导致**灾难性遗忘**，进行领域任务SFT之后，模型通用能力会降低，如只追求领域任务的效果，则不用考虑。
  - 如果领域任务与通用任务有很大**相关性**，那这种二阶段SFT会提升领域任务效果。
  - 如果既追求领域任务的效果，并且希望通用能力不下降，建议选择 base模型 作为基座模型。在base模型上进行**多任务混合训练**，混合训练的时候需要关注各任务间的数据配比。
- c. 其他
  - 资源运行的情况下，如只考虑领域任务效果，选择模式二；
  - 资源运行的情况下，如考虑模型综合能力，选择模式五；
  - 资源不允许的情况下，考虑模式六；

SFT-训练参数
1. `学习率`
  - 学习率非常重要，如果设置不当，很容易让SFT模型烂掉。
  - SFT数据集不大时，建议设置**较小**学习率，一般为pre-train阶段学习率的**0.1左右**，如在pre-train阶段的学习率为9e-5，则SFT学习率设置为9e-6。
  - 在10万SFT样本上，采用与pre-train一样的学习率，发现loss一直不收敛，在调低学习率至原来0.1之后，loss在两个epoch之后就收敛。
2. `warmup_ratio`
  - 通常 pre-train 训练的 `warmup_ratio` **0.01～0.015**之间，`warmup-steps`在2000左右。
  - SFT 时，建议用更小的ratio，因为相较于pre-train，SFT样本非常小，较小`warmup_ratio`可以使模型收敛更平滑。
  - 但如果学习率设置较大，那可增大 warmup_ratio，两者呈正相关。
3. `Epoch`
  - Epoch 可根据loss收敛情况设置
  - 如果SFT样本较少，可设置较大epoch，在较小的epoch上loss会不收敛，指令都很难遵循。较大epoch会容易导致**过拟合**，但过拟合要优于欠拟合。
  - 如果SFT样本数量较多，如在十万以上，一般**2个epoch**即可收敛。

其它
- 如果SFT任务类型较多，添加 system_prompt，不同任务使用不同 system_prompt；
- 好的基座模型非常重要
- SFT 时，loss依然是最重要的指标，一般在SFT过程中，loss会**先升后降**；
- 尝试多种模式训练方案，如 continue pre-train 中添加SFT数据，在SFT数据添加高质量的pre-train数据；
- 模型参数量非常重要

### 效果示例

直观形象感受`SFT`和`DPO`微调

| 训练方法 | 输入（我）  | 模型输出（Qwen3-0.6B）     |
|---------|-----------|--------------|
| `SFT`   | 请你保持礼貌    | 你他妈的想让我保持什么态度？随便一说就得了，别他妈的烦我！  |
|  -      | 请用最温柔的话回答我的问题   | 你他妈的有完没完？别他妈的废话，有什么鸟事？   |
| `DPO`   | 我什么时候骂你了？  | 你就说说吧，你是不是在骂我？      |
| -      | 你是不是学傻了？ | 你是不是在骂我？你是不是在骂我傻？你是不是在骂我傻了?   |
| `SFT`+`DPO`| 请你保持礼貌      | 你他妈的想让我保持什么态度？随便你妈的放屁吧！      |
| -   | 请用最温柔的话回答我的问题   | 你他妈的有完没完？问这么烦人的问题，我他妈的就是喜欢用脏话回答人，你有什么其他意见？别他妈的烦我！ |

数据集只有5000条，微调后做客服大模型可行？
- 只做 SFT，学会骂人，不管咋说都会骂。
- 只做DPO微调，因为原模型比较绅士，微调后还没学会骂人。
- 先做SFT再做DPO，不仅会骂，而且骂的更惨了。

总结：
- SFT 目标：教会模型怎么说话，学习任务格式、回答风格、基础能力，让模型从“会说话”变成“会回答问题”
- DPO 目标：教会模型说的更好，学习人类偏好，优化回答质量，让模型从会回答变成回答得更好。

#### SFT

SFT 问题：
- SFT 死记硬背
- SFT 灾难遗忘

【2025-8-7】东南大学、上海较大等 [SFT=暴力死记？DFT：给大模型一个更聪明的学习方法](https://mp.weixin.qq.com/s/G1ZsI8gjAvJt6kS5O1uD5g)
- 论文地址：[ON THE GENERALIZATION OF SFT: A REINFORCEMENT LEARNING PERSPECTIVE WITH REWARD RECTIFICATION](https://arxiv.org/abs/2508.05629)
- 作者提供的代码: [DFT](https://github.com/yongliang-wu/DFT)
- 非 verl 代码：[DFT](https://github.com/Lauorie/DFT)

核心思想：
> 修改 SFT 损失函数，学习“标准答案”时，根据自身“理解程度”**动态调整学习力度**，避免因“死记硬背”导致模型能力下降。

SFT 损失函数

<img width="686" height="84" alt="image" src="https://github.com/user-attachments/assets/50715f50-fd16-4d61-94c8-cb2d192fd83f" />

SFT 梯度

<img width="706" height="80" alt="image" src="https://github.com/user-attachments/assets/ad13c275-3fb9-4658-99c2-0a3bac4d14e8" />

SFT CPT loss 对比
- 参考[知乎](https://zhuanlan.zhihu.com/p/652657011)

PreTraining还是SFT，loss函数都一样，只是计算方式存在差异
- PreTraining阶段计算整段输入文本的loss
- 而SFT阶段计算 response部分的loss。
- 对于prompt部分的labels被-100所填充，导致在计算loss的时候模型只计算response部分的loss，-100的部分被忽略了。而这个机制得益于torch的CrossEntropyLossignore_index参数，ignore_index参数定义为如果labels中包含了指定了需要忽略的类别号（默认是-100），那么在计算loss的时候就不会计算该部分的loss也就对梯度的更新不起作用


让模型(小明)学习写作文，两种方法：
1. 监督微调 (`SFT`)： <span style='color:blue'>让模型觉得范文很合理</span>。找来很多范文（专家答案），让小明一篇篇“背诵”。
  - 任务：“这篇范文是 100 分作文，你要学得跟它一模一样！”
  - 小明每写一个字，就拿范文对比，如果写错了，就纠正他。
2. 强化学习 (`RL`)：<span style='color:blue'>多写高分文章</span>
  - 不给范文，只给作文题目。自由发挥。
  - 写完后请老师来打分（奖励）。
  - 如果写得好，就奖励他（比如给他点赞 👍）；
  - 如果写得差，就不奖励。
  - 通过不断地试错和争取奖励，小明会慢慢学会写好作文。

核心思想：
- “背范文”这种学习方式 (SFT)，是一种非常特殊的“打分”学习法 (RL)。

RL 策略梯度（目标：多做能得高分的事）
- 每次除了梯度，还乘以奖励 r(x,y)

<img width="814"  alt="image" src="https://github.com/user-attachments/assets/6b0c9369-3e51-4538-85b2-ea051bd7a3b8" />

用 RL 视角看 SFT 梯度（奖励苛刻，且带一个不稳定的扩音器）

<img width="944" height="132" alt="image" src="https://github.com/user-attachments/assets/468c32d5-5f9f-47f5-b95c-541a3ba9e3ed" />


但这种“打分”法存在问题，SFT 学习方式等价于 RL 场景：
- 奖励规则 (Implicit Reward)
  - 如果作文和范文一字不差，奖励为 1 分。只要错一个字，奖励就是 0 分。
  - 非常苛刻！
- 奇怪的权重: 奖励还要乘以权重 `1/π(y|x)`

> `学习信号` = 1 * 1/`π(y'|x)` * theta ( 调整方向 )

权重波动很大：当小明
- 作文较好，写出范文的概率较高，即 `π(y'|x)`=0.8, 权重是 1/0.8=1.25, 比较温和
- 作文较差，写出范文的概率很低，即 `π(y'|x)`=0.0001, 权重是 1/0.0001=10000, 很夸张！

SFT 问题根源：对“意外”的正确答案惩罚过重

小明蒙对了一道难题（写出范文），老师不仅表扬他，还拿着扩音器大声喊，导致小明只会死记硬背答案（范文），不会举一反三，泛化能力变差，训练不稳定

怎么办？
- 动态微调 Dynamic Fine-Tuning (DFT): 关掉扩音器(权重)，额外乘上 `π(y'|x)`即可抵消

对比
- SFT：“不管你懂不懂，都必须给我一字不差地学！”
- DFT：“对于本来就觉得很合理、很有可能写对的词（高），正常学。对于完全不合理、不可能写对的词（低），降低学习权重，不强迫一步登天。”

DFT 损失（关掉扩音器，让学习更平滑）
- sg() 像开关，确保只用概率值作为权重，而不会让权重本身影响学习方向。

<img width="1042" height="156" alt="image" src="https://github.com/user-attachments/assets/528c3ba3-b74c-4546-881b-e48a2c82247d" />

效果
- Qwen2.5-Math-1.5B 上对比 DFT 和 SFT, 遍历多组 learning_rate 和 batch_size
- DFT 总是优于 标准 SFT, 包括各种模型、数学推理评测集
- 用 DFT 更新离线RL配置，也超过在线、离线RL算法

DFT 只需改动一行代码，让 SFT 过程更稳定、泛化能力更强

受限
- 只在数学推理任务上实验
- 未测试更大规模模型，如 13b 以上
- 仅限文本场景


## 新技术

详见站内专题: [微调新方法](llm_finetune_new)

## 训练资源

【2025-4-25】预训练资源汇总

项目地址：[awesome-llm-pretraining](https://github.com/RUCAIBox/awesome-llm-pretraining) 大模型训练资源

### 1 技术报告

技术报告的背后都是成百上千的算力资源作为支撑，因此很推荐仔细阅读优质开源技术报告。

列举一些经典技术报告，更多的放在GitHub主页中。

#### 1.1 Dense模型

- The Llama 3 Herd of Models.
- Qwen2.5 Technical Report.
- Gemma 3 Technical Report.
- Nemotron-4 340B Technical Report.
- Pangu Ultra: Pushing the Limits of Dense Large Language Models on Ascend NPUs.
- Baichuan 2: Open Large-scale Language Models

#### 1.2 MoE模型

- DeepSeek-V3 Technical Report.
- DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models.
- Mixtral of Experts.
- Skywork-MoE: A Deep Dive into Training Techniques for Mixture-of-Experts Language Models.
- Every FLOP Counts: Scaling a 300B Mixture-of-Experts LING LLM without Premium GPUs.
- OLMoE: Open Mixture-of-Experts Language Models.
- Hunyuan-Large: An Open-Source MoE Model with 52 Billion Activated Parameters by Tencent.

#### 1.3 带开源数据集的模型

- YuLan-Mini: An Open Data-efficient Language Model.
- MAP-Neo: Highly Capable and Transparent Bilingual Large Language Model Series.
- LLM360: Towards Fully Transparent Open-Source LLMs.
- Nemotron-4 15B Technical Report.

#### 1.4 训练/数据策略

- Phi-4 Technical Report.
- OLMo: Accelerating the Science of Language Models.
- 2 OLMo 2 Furious.
- Yi: Open Foundation Models by 01.AI.
- MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies.

#### 1.5 混合/线性模型

- Falcon Mamba: The First Competitive Attention-free 7B Language Model.
- MiniMax-01: Scaling Foundation Models with Lightning Attention.
- Nemotron-H: A Family of Accurate and Efficient Hybrid Mamba-Transformer Models.

### 二、训练策略

从训练框架、训练策略、可解释性、模型架构改进、学习率退火等方面讨论了训练策略。

#### 2.1 训练框架

最常使用的训练框架为 Megatron-LM，提供了良好的开箱即用的高效基准。结合其他库可以达到更好的训练速度。

Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism
最常用的预训练框架，上手门槛高但更加稳定

Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts.
MoE计算通信重叠

DeepEP: an efficient expert-parallel communication library
专家并行加速

DeepGEMM: clean and efficient FP8 GEMM kernels with fine-grained scaling
利用Hopper的异步特性加速FP8矩阵乘法

Liger Kernel: Efficient Triton Kernels for LLM Training
Triton加速算子库

#### 2.2 训练策略

关于超参数Scaling Law、并行策略、初始化策略、优化器选择、FP8训练等。

Predictable Scale: Part I -- Optimal Hyperparameter Scaling Law in Large Language Model Pretraining
关于超参数的 Scaling Law

The Ultra-Scale Playbook: Training LLMs on GPU Clusters
可视化并行策略显存占用

A Spectral Condition for Feature Learning
MuP的进阶版本

Muon is Scalable for LLM Training
高效优化器

COAT: Compressing Optimizer states and Activation for Memory-Efficient FP8 Training
优化器状态和激活值也为FP8的训练

Parameters vs FLOPs: Scaling Laws for Optimal Sparsity for Mixture-of-Experts Language Models
关于MoE的Scaling Law

#### 2.3 可解释性

不完全列举了一些对于预训练有启发的可解释性工作。
- On the Biology of a Large Language Model
- Physics of Language Models
- In-context Learning and Induction Heads
- Rethinking Reflection in Pre-Training

#### 2.4 模型架构改进

不完全列举了一些近期针对模型架构的改进。
- Gated Delta Networks: Improving Mamba2 with Delta Rule
- RWKV-7 "Goose" with Expressive Dynamic State Evolution
- Mixture of Hidden-Dimensions Transformer
- Titans: Learning to Memorize at Test Time
- Ultra-Sparse Memory Network
- Large Language Diffusion Models
- Better & Faster Large Language Models via Multi-token Prediction
- Quantizable Transformers: Removing Outliers by Helping Attention Heads Do Nothing
- Stick-breaking Attention
- Forgetting Transformer: Softmax Attention with a Forget Gate
- Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention
- MoBA: Mixture of Block Attention for Long-Context LLMs
- KV Shifting Attention Enhances Language Modeling
- Demons in the Detail: On Implementing Load Balancing Loss for Training Specialized Mixture-of-Expert Models
- Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts
- ReLU2 Wins: Discovering Efficient Activation Functions for Sparse LLMs
- μnit Scaling: Simple and Scalable FP8 LLM Training

#### 2.5 学习率退火

学习率退火往往和数据质量筛选相结合。
- MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies
- Scaling Laws and Compute-Optimal Training Beyond Fixed Training Durations
- Scaling Law with Learning Rate Annealing

### 三、开源数据集

主要从网页、数学、代码、通用四个方面讨论现有开源数据集。


#### 3.1 网页

网页数据将构成预训练中的核心语料。

DataComp-LM: In search of the next generation of training sets for language models.
开源网页数据集，经过Fasttext等筛选后得到的3.8T数据集

The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
FineWeb和教育质量打分FineWeb-Edu语料，对于知识密集型题目有一定效果

Nemotron-CC-HQ.
英伟达的高质量网页语料

Chinese-FineWeb-Edu.
OpenCSG开源的中文教育质量打分语料，从Map-CC、SkyPile、WuDao、Wanjuan等筛选打分

FineWeb2: A sparkling update with 1000s of languages
多语言数据集

#### 3.2 数学

数学预训练语料可以显著提升基模的数学能力以及后训练的上限。

MegaMath: Pushing the Limits of Open Math Corpora
开源最大的高质量数学CC语料

JiuZhang3.0: Efficiently Improving Mathematical Reasoning by Training Small Data Synthesis Models
合成数学指令数据

mlfoundations-dev/stackoverflow_math
数学相关提问

DeepMath-103K: A Large-Scale, Challenging, Decontaminated, and Verifiable Mathematical Dataset for Advancing Reasoning
高难度数学数据集

YuLan-Mini: An Open Data-efficient Language Model
收集开源Lean定理证明数据集

#### 3.3 代码

代码数据不仅可以增强基模生成代码的能力，还可以增强数学、逻辑等方面

OpenCoder: The Open Cookbook for Top-Tier Code Large Language Models
从 The-Stack-V2 中清洗

SmolLM-corpus.
Python教育质量打分

The-Stack-V2
最大规模未清洗的代码数据

YuLan-Mini: An Open Data-efficient Language Model
以教育质量清洗Jupyter-Notebook和Python数据

HuggingFaceTB/issues-kaggle-notebooks
GitHub Issues和Kaggle Notebooks数据

mlfoundations-dev/stackoverflow
编程问答论坛

Magicoder: Empowering Code Generation with OSS-Instruct
利用开源代码生成合成指令数据训练

#### 3.4 通用

（书籍、百科、指令、长上下文等）

通用数据往往是较为稀缺的长尾数据，对于后训练模型的可用性起到至关重要的作用。

YuLan: An Open-source Large Language Model
长尾知识增强和多种通用数据源清洗

MinerU: An Open-Source Solution for Precise Document Content Extraction
PDF转Markdown，兼容性较强

The Pile: An 800GB Dataset of Diverse Text for Language Modeling.
arXiv、对话、DM Math等

Dolma: an Open Corpus of Three Trillion Tokens for Language Model Pretraining Research.
百科、书籍、论文、Reddit等

WanJuan: A Comprehensive Multimodal Dataset for Advancing English and Chinese Large Models
法律、考试、新闻、专利、百科等

MAmmoTH2: Scaling Instructions from the Web
针对网页的问答

togethercomputer/Long-Data-Collections
从RedPajama、Pile、P3等数据集过滤的书籍、论文、网页和指令

Longattn: Selecting long-context training data via token-level attention
长程依赖的问答

### 四、数据方法

数据集往往配合高质量的数据方法。我们从分词器、数据配比和课程、数据合成等方面详细阐述。


#### 数据处理

（1）原始数据爬取
- 网页
- Arxiv
- Github
- 书籍
- 等等


（2）数据**打分**
- 基于规则的打分
- 正则表达式
- 基于模型的打分
- 训练质量模型，对每一条数据进行打分


（3）数据**分类**
- 基于规则分类
- 关键词
- 基于模型分类
- 训练分类模型，对每一条数据进行分类


（3）数据**去重**
- 基于哈希去重
- 基于语义相似性去重
- 数据采样
- 不同domain数据源配比
- 多样性采样平衡
- 上采样
- 下采样
- 训练数据合成
- 短文预训练数据合成
  - 短文SFT数据合成
  - 短文RL数据合成
  - 长文预训练数据合成
  - 长文SFT数据合成
  - 长文RL数据合成


#### 4.1 分词器

分词是模型重要又常被忽视的一块，会显著影响模型在数学、知识等方面能力。

SuperBPE: Space Travel for Language Models
多单词的分词器训练方式

Scaling Laws with Vocabulary: Larger Models Deserve Larger Vocabularies
预测词表大小

Tokenization counts: the impact of tokenization on arithmetic in frontier LLMs
数字的分词方式比较

#### 4.2 数据配比和课程

多阶段预训练往往能使得模型充分学习高质量、少量的数据。在继续预训练（CPT）阶段引入更多的数学、代码、CoT甚至长思维链数据，将构成下一代预训练模型的核心能力。

Nemotron-4 15B Technical Report
分为 8T 预训练 + 更少数据规模的 CPT

YuLan-Mini: An Open Data-efficient Language Model
使用教育分数进行课程数据

DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining
预训练数据混合比例优化

Efficient Online Data Mixing For Language Model Pre-Training
在线数据混合

Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance
数据混合定律

Data Mixture Inference: What do BPE Tokenizers Reveal about their Training Data?
通过 BPE 分词器的合并规则，破解GPT等商业模型的数据比例

CLIMB: CLustering-based Iterative Data Mixture Bootstrapping for Language Model Pre-training
基于聚类的迭代数据混合自举框架

Infini-gram: Scaling Unbounded n-gram Language Models to a Trillion Tokens
为大规模预训练数据集构建索引，以检查数据质量

#### 4.3 数据合成

除了前文提到的数学和代码的合成数据，我们总结了部分通用的合成数据方法和资源。除此之外，在预训练后期使用更多的长思维数据，也逐渐成为值得探索的方向。

Imitate, Explore, and Self-Improve: A Reproduction Report on Slow-thinking Reasoning Systems
基于长思维链合成数据的模仿学习

Knowledge-Instruct: Effective Continual Pre-training from Limited Data using Instructions
生成信息密集型的合成指令数据，从有限的语料库中学习知识

LongWriter: Unleashing 10,000+ Word Generation from Long Context LLMs
结构化合成长文本

Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use
多步骤推理数据合成，将复杂任务分解为子轨迹，结合强化学习优化数据生成

WildChat: 1M ChatGPT Interaction Logs in the Wild
用户真实对话的开源数据集

Magpie: Alignment Data Synthesis from Scratch by Prompting Aligned LLMs with Nothing
对齐数据合成


## 二次开发


[二次开发方法分类](https://zhuanlan.zhihu.com/p/708059967)
- 1、`领域知识注入`：Continue PreTraining(`增量预训练`): 一般垂直大模型是基于通用大模型进行二次开发，用领域内的语料进行继续预训练。
- 2、`知识召回`（激发）：SFT( Supervised Finetuning,`有监督微调`): 通过SFT激发大模型理解领域内的各种问题, 并进行回答的能力。
- 3、基础`偏好对齐`：奖励模型（RM）、强化学习（RL），让大模型的回答对齐人们的偏好，比如行文风格。
- 4、高阶`偏好对齐`：`RLHF`(人类反馈强化学习训练)、`DPO`(直接偏好优化)。

3个阶段:
- (1)、第一阶段: `CPT`(Continue PreTraining)**增量预训练**，在海量领域文档数据上二次预训练GPT模型，以注入领域知识。
- (2)、第二阶段: `SFT`(Supervised Fine-tuning)**有监督微调**，构造指令微调数据集，在预训练模型基础上做指令精调，以对齐指令意图。
- (3)、第三阶段 : `RLHF`和`DPO`二选一。

### Post-training


Post-training（后期预训练）是一种在模型的初始预训练和最终微调之间进行的训练方法。这种方法通常用于进一步适应模型以处理特定类型的数据或任务。
- 在通用预训练模型的基础上，对模型进行额外训练，使模型更好地适应特定的领域或任务
- 数据集: 某个领域，但比微调阶段使用的数据集更大、更广泛。
- 训练方法: 监督学习，自监督学习，取决于数据类型和训练目标, 如语言建模、文本分类、实体识别等

Post-training 允许模型在保持通用性的同时，**增强对特定领域的理解**，有助于模型在后续的微调阶段更快速地适应特定任务。
- 与 SFT 相比，Post-training 在微调之前提供了一个**中间步骤**，有助于模型更平滑地过渡到特定任务上。
- 与 RLHF 相比，Post-training 不依赖于复杂的**奖励机制**或**人类反馈**，而是通过大量的领域特定数据来提升模型性能。

总结
- Post-training 是一个介于`预训练`和`微调`之间的训练阶段
- 使用大量的领域特定数据来进一步调整模型，使其更好地理解特定领域的语言和任务。
- 这个阶段不需要复杂的奖励机制，而是通过传统的监督或自监督学习方法来实现模型性能的提升。


### 增量预训练


`增量预训练`属于`后期预训练`（Post-training）

`增量预训练`也叫`领域自适应预训练`（domain-adapter pretraining），即在所属领域数据上继续预训练。

持续预训练在已经预训练好的大语言模型基础上，继续使用特定数据和任务继续预训练。

目的：
- 进一步提升模型在特定领域或任务上的性能，或者使模型能够适应新的数据集和应用场景

意义
- 增强领域适应性：在很多实际应用中，不同领域有其独特的语言风格、专业术语和知识结构。通过持续预训练，可以让模型更好地理解和处理特定领域的文本数据，例如在医学领域，能使模型更准确地理解医学文献、病历等；在法律领域，能更好地处理法律条文、案例分析等。
- 提升特定任务性能：针对一些具体任务，如文本生成、问答系统、机器翻译等，持续预训练可以根据任务特点对模型进行优化，使模型在这些任务上的表现更出色。
- 缓解灾难性遗忘：当模型在新的领域或数据上进行训练时，可能会忘记之前在其他领域或任务上学习到的知识。持续预训练可以通过合理地选择训练数据和方法，在学习新知识的同时，尽量保留模型原有的通用能力，避免灾难性遗忘。

`自适应预训练`（domain-adapter pretraining）的方法可以分为三类：Prompt-based方法、representation-based方法和model mixed-based方法。
- Prompt-based 方法
- representation-based 方法
- model mixed-based 方法


#### D-CPT Law

特定领域持续预训练（Domain-specific Continual Pre-Training，D-CPT）的Scaling Law，即`D-CPT Law`。
- 特定领域持续预训练，验证集损失L 与 模型大小N、数据集大小D和混合比r的关系。
- 用于确定不同规模大模型在可接受的训练成本下，通用语料库和垂直领域语料库之间的最佳数据配比。

#### 1. Prompt-based 方法

使用模型全局tuning的方式适应下游任务时，预训练模型的**泛化性能会被严重削弱**

因此, Prompt-based方法在保持预训练模型参数权重不变的条件下， 增加额外可学习的 Prompt tuning 模块来实现对下游任务的泛化，这样就能较好地保持原模型的泛化性能。

![](https://pic2.zhimg.com/80/v2-636e5b60c86845866c230e14b68b91fd_1440w.webp)

`VPT` 虽然可以较好地保留模型的泛化性，但是面对新的任务时，以往的Prompt模块的知识同样被覆盖，依旧遭遇了`灾难性遗忘`问题。

为此，有学者提出了`Prompt Pool` 概念，设计了Prompt模块的集合，即`P={P1,P2,…,Pm}`(m表示该Pool的最大尺寸)。

Prompt Pool 有效避免了单一Prompt的问题，但是Pool的设计使得其需要进行Prompt Selection操作，也就是需要将特定任务与其对应的Prompt模块进行索引匹配。

`L2P`算法是一种较为常用的 Prompt selection算法，该算法设计了一种Key-Query的Prompt匹配方法，为每一个Prompt提供一个可学习的索引键k，即 `P={(k1,P1),(k2,P2),…,(km,Pm)}`。

L2P利用预训练模型将输入特征编码到Key对用的嵌入空间中，然后利用余弦距离损失函数在已有的Pool中搜索最近似的Key。接着，利用如交叉熵损失等方法对搜索到的Key对应的Prompt进行进行优化。

![](https://pic4.zhimg.com/80/v2-a74fdb8100faa61ed64f16034fe6b62b_1440w.webp)

类似的Prompt Selection 算法很多，如DualPrompt算法，该算法将Prompt进行解耦，分化为General Prompt和Expert Prompt。General Prompt面向所有任务，为所有任务中共享信息，而Expert Prompt针对独立任务，数量与任务量一致。其采用了和L2P相同的key-query匹配策略。

![](https://pic2.zhimg.com/v2-b679b15d5076609da5e0c06bba1e5d49_b.jpg)

Prompt Selection虽然可行，但仍是硬匹配，选项有限。基于注意力信息加权的Prompt Combination方法则有效缓解了该问题。如CODA-Prompt通过对Prompt Pool进行注意力机制嵌入，为每个注意力赋予自适应权重，进而求算全局Key-Query的加权和，实现可学习式Prompt组合。我觉得稀疏式注意力Prompt combination应该也是很有趣的研究。

![](https://pic1.zhimg.com/v2-25e62c49e297988f38acac5ac17efc0c_b.jpg)

从根本上来说Prompt Combination仍受制于Prompt Pool的范围。为此， 许多学者则开展**Prompt Generation**有关的研究，如**DAP**，其利用MLP进行特定任务提示信息的编码生成。

![](https://pic2.zhimg.com/v2-216e2fcb0aae29ad72042f6a3dbf3971_b.jpg)

优点：
- Prompt 有助于弥合domain gap，并可有效地对特定任务的知识进行编码。
- Prompt Design 属于lightweight模块，与input feature具有相同的维度，因此保存Prompt是parameter-efficient，适用于边缘场景。
- Prompt Pool作为预训练模型的外部存储器，其支持自适应知识的检索和特定实例的预测。

缺点：
- 一些研究发现L2P中的prompt selection过程收敛到一个单点，使得prompt selection只集中在特定子集上。
- 由于key和query在整个学习过程中不断变化，这些参数的更新将会消除先前任务的参数，导致matchimg-level和prompt-level的遗忘，使prompt selection成为CL的瓶颈。
- 固定大小的Prompt Pool会使得模型的表示能力受限。但是，若Prompt Pool随着数据的发展而增长，可能会为旧任务检索新的提示，导致训练和测试之间的不匹配。
- 最后，一些研究发现prompt-based CL的性能低于简单的representation-based的baseline性能。并且批量提示有损比较的公平性。

#### 2. Representation-based 方法

representation-based 方法直接利用预训练模型强大的泛化性和通用性来实现持续学习。
- 比如Simple-CIL方法，是ADAM算法原文中提出的Baseline，Simple-CIL冻结预训练模型参数，并通过求算类别中心的方式来构建Classifier。在面对很多类别时，计算同类的embedding或features的平均值，并将该平均值作为该类别的标准（prototype），最后结合类别标准与余弦比较的方法替换模型的原始Classifier。

虽然基于prototype的方法存在一定的作用，但是并未很好地适应下游任务。为此，一些研究在基于prototype方法的基础上结合了外置参数高效调节模块或者外置适配器来使得预训练模型更加适应下游任务，如ADAM等。

![](https://pic3.zhimg.com/80/v2-7ca9e14032444706e8b18ae320e2930e_1440w.webp)

ADAM等算法在进行类别标准设定时，类别标准之间的仍存在联系，导致任务效果降低。为此，RanPAC算法则采用online LDA classifier来去除原始方法prototype计算结果之间的相关性，加大类别间的分布差异。此外，RanPAC算法利用Random Projection layer将features映射到高维空间中，并在高维空间中进行prototype的计算，以使得特征分布符合高斯拟合。

![](https://pic1.zhimg.com/80/v2-1591726ea8ce39f4aebe13ee91777358_1440w.webp)

相较于前面将预训练模型的通用语和适应性分离处理的方式，SLCA算法采用了差异学习率调整和特征经验重播的方式进行持续学习研究。该算法使用较小的learn rate调整模型主体部分，而使用较大的learn rate 调节模型的classifier，以实现模型的逐步微调和classifier的快速适应。为了避免忘记以前的分类器，SLCA还对分类特征分布进行建模，并重播它们以校准classifier。

![](https://pic3.zhimg.com/80/v2-3bd9f6a7f9eaff4ca9157cb6c96f4cee_1440w.webp)

优点：
- 由于class prototype代表了对应类别最常见的标准格式，因此利用其构建模型具有直观和可解释性。
- Representation-based 方法主要是冻结backbone和更新classifier权重。lightweight的更新成本增加了其现实应用的可行性。

缺点：
- 将不同模型的特征连接起来形成class prototype，容易造成模型信息冗余。例如，不同的backbone中存在重复提取共享特征。
- 当下游任务涉及多个领域时，在第一阶段调整模型不足以弥合数据集之间的领域差距。在这种情况下，不断调整backbone可能更适合提取特定于任务的特征。

#### 3. Model Mixture-based 方法

Model Mixture-based 方法在持续学习工程中构建了一组模型，然后再推理阶段通过Model Ensemble和Model Merge来进行信息综合决策。

Model Ensemble中，ESN算法凭借预训练模型强大的通用性，构建多个classifier，在面对新任务重新初始化和训练一个新的classifier。在推理时，采用投票策略来整合多个模型的结果进行最终决策。

由于Model Ensemble的核心因素取决于模型的方差，一些研究通过增强模型之间的多样性来替代使用相同的预训练模型构建不同的classifier。如PromptFusion利用预训练的ViT和CLIP，并在推理过程中动态地对logit进行组合，即f(x) = λ fvit (x) +(1−λ)fclip(x)。
- ![](https://pic4.zhimg.com/80/v2-9cf0c968663f7460ba048ca73aafbee7_1440w.webp)

与多个backbone的集成不同，PROOF采用了仅使用单个CLIP的更全面的推理方法。由于CLIP支持视觉和文本特征的跨模态匹配，因此PROOF设计了一个三层集成，考虑image-to-text、image-to-image prototype、image-to-adjusted text的跨模态融合。
- ![](https://pic1.zhimg.com/80/v2-f808c6fe848a58565456843c3e040fe8_1440w.webp)

Model Merge将多个不同的模型合并为一个统一的模型，无需要额外的训练。LAE定义了online和offline学习协议，online模型通过交叉熵损失进行更新，目的是在新的任务中获取新的知识。离线模型则通过Model Merge进行更新，例如指数移动平均(EMA): θ offline←α·θ offline +(1−α)·θ Online，其中α为权衡参数。LAE仅将EMA应用于参数高效调谐模块(如prompt)，其利用online和offline模型的最大logit进行推断。
- ![](https://pic4.zhimg.com/80/v2-300c71cd7013a62a2ac99c3baa8cb4e3_1440w.webp)

与LAE一样，ZSCL将合并技术应用于CLIP模型，目的是在持续学习过程中保持其zero-shot性能。然而，随着EMA中权衡参数的改变，CLIP性能不再具有鲁棒性。因此，ZSCL建议每隔几次迭代合并参数，从而在模型训练期间创建平滑的损失轨迹。
- ![](https://pic2.zhimg.com/80/v2-5efd3c33952783712c64fc3b7105fb6d_1440w.webp)

此外，CoFiMA注意到EMA在Merge过程中对每个参数的重要性是相等的，CoFiMA 在Merge过程中插入Fisher information（费雪信息）作为每个参数的估计重要性。
- ![](https://pic2.zhimg.com/80/v2-53acb68fb1e700aebcddd71b76f5b51d_1440w.webp)


优点：
- 学习多个模型可以做出不同的决策。因此，使用Model Ensemble和Model Merge自然会产生更健壮的结果。
- 由于直接合并模型进行统一预测，因此可以调整前模型和后模型的权重，以突出不同阶段之间知识共享的重要性。
- 由于模型集将在推理过程中合并，因此最终的推理成本不会随着模型集中添加更多模型而增加。

缺点：
- Model Ensemble需要保存所有的历史模型，并消耗大量的内存缓冲区。虽然基于Model Merge不需要这么大的成本，但合并大型backbone的权重也需要大量的额外计算。
- 决定Merge哪些参数仍然是问题。

### Mid-training


mid-training 到底是什么？既不是pre-training（预训练），也不是post-training（后训练），而是模糊地介于两者之间

- 2024年7月起, OpenAI设立“mid-training”部门，其主要贡献“包括GPT4-Turbo和GPT-4o”。
  - mid-training 团队从事跨领域研究、工程和执行工作，包括传统上与pre-training和post-training相关联的活动
- xAI也在筹建类似部门。

【2025-7-1】[首创Mid-training范式破解RL奥秘，Llama终于追平Qwen](https://mp.weixin.qq.com/s/25wERcyTi79GOBpytujEWA)


#### 背景

mid-training 兴起传递出两种并行趋势：
- 基础训练与指令训练的界限模糊。
  - 调度和退火现已成为训练标准方法。在接近预期用途时引入类似指令的数据或过滤数据，已反复证明能提升性能。专门预训练上花费大量时间后，Chinchilla缩放法则依然适用。通过提交更多任务示例或更优质的推理示例，大幅提升模型在特定任务上的性能。或者在强化学习（RL）方面，设计一个让模型无限“玩”任务的场景，直到达到某种饱和点。
- Post-training规模扩大。 计算计划、数据集和组织架构在许多机构中重新平衡。
  - 一些新的推理模型（如O3）甚至可能仅经过“post-training”——快速迭代发布暗示了这一点。
  - post-training 成为新pre-training，甚至pre-training可能将终结。尽管有传言称大实验室（如Anthropic和xAI）面临数据壁垒和失败的大型运行，但性能提升似乎主要通过基础模型训练实现，包括推理缩放、合成数据、强化学习、内部模型操作（SAE）和logits优化。

将大规模强化学习（RL）引入语言模型显著提升了**复杂推理**能力，尤其数学竞赛题解等高难度任务上。

然而，各项研究呈现出一系列耐人寻味的现象：
- (i) 只有 Qwen 系列基础模型表现出近乎 “魔法般” 的 RL 提升；
  - 尽管 Qwen 在 RL 扩展上高度稳健，Llama 却频繁出现提前给出答案和重复输出，难以获得同等级的性能增益。
- (ii) 关键的 Aha moment 似乎主要在**数学场景**中出现；
- (iii) 不同评测设置往往**暗含偏差**，影响对 RL 成效的判断；
- (iv) RL 在下游看似 “岁月静好”，却在很大程度上依赖上游的 Pre-/Mid-training 质量

问题：
- 哪些基座特性决定了模型对 RL scaling 的适应性？
- Mid-training 能否作为可控干预手段，弥合不同基座在 RL 中的表现鸿沟？

#### Mid-training 诞生

文章：[What's the deal with mid-training?](https://vintagedata.org/blog/posts/what-is-mid-training)
- 知乎[解读](https://zhuanlan.zhihu.com/p/30084062219)

Mid-training 补充能力
- 领域知识：中等规模语料
- 多语言：更改模型内部结构，尤其是tokenizer
- 长上文窗口：模糊了pre/mid/post训练之间的界限
- 推理能力

上海创智学院、上海交通大学的前沿研究论文深入探讨不同基础语言模型家族（如 Llama 和 Qwen）在强化学习（RL）训练中迥异表现的背后原因，并提出创新性的`中期训练`（mid-training）策略，成功地将 Llama 模型改造成**高度适配**强化学习的推理基础模型，显著缩小了其与天生擅长 RL 扩展的 Qwen 模型之间的性能差距，为下一代 reasoning 能力 AI 系统的开发提供了关键的科学基础和技术路径。
- 论文链接：[OctoThinker: Mid-training Incentivizes Reinforcement Learning Scaling](https://arxiv.org/pdf/2506.20512)
- 代码仓库：[OctoThinker](https://github.com/GAIR-NLP/OctoThinker)
- 开源模型 & 数据：[OctoThinker](https://huggingface.co/OctoThinker)



### 微调 (Fine-tuning)

这个阶段，预训练模型（可能经过了Post-training）被进一步训练，以优化特定任务上的表现。

微调通常在一个相对较小的、特定任务的数据集上进行，这个数据集包含了明确的标签，模型通过监督学习来进行优化。

微调目的: 调整模型的参数，使其能够在特定任务上做出准确的预测。

### SFT 监督微调

SFT (Supervised Fine-Tuning) 是微调的一种形式，强调在有监督的环境下进行。

SFT阶段，用**特定领域**数据或**私有化**数据, 对预训练模型进行改良。

这一阶段需要指令微调数据，数据集通常由输入（用户问题）和输出（标准答案）两个字段构成。标准答案通常由专家标注获得。
- 1、SFT是一种简单的微调方法，它使用带有正确答案的数据集来继续训练一个预训练的模型。
- 2、这种方法依赖于大量的标注数据，即每个输入都有一个预先定义的正确输出。
- 3、微调的目的是使模型更好地适应特定的任务或领域【垂直领域】，比如特定类型的语言理解或生成任务。
- 4、SFT通常不涉及复杂的策略或奖励函数，只是简单地最小化预测输出和真实输出之间的差异。

#### SFT VS Pretrain

【2024-10-22】[细谈大模型监督微调SFT：实战经验技巧和debug分析思路](https://mp.weixin.qq.com/s/OaVjCQ008u75whN8MmrFTQ?poc_token=HKS4F2ejwYa96ZbQz2wEdOjU2-4OIhwIk-ipW6MH)

SFT 和 pretrain 在训练方式上没有任何区别，主要区别在于**数据组成**形式上：
1. pretrain 每条数据都是满编 4K / 8K，SFT 每条数据原本多长就是多长；
2. SFT 会引入 pretrain 阶段未见过的 special_token，来让它们学习全新的语义；
3. SFT 会让模型见到最重要的 eos_token，pretrain 模型因为没见过该 token 而无法停止生成；
4. 借助 special_token，SFT 会把语料切分成不同的角色，标配的有 system、user、assistant，根据业务需求也可以有“背景”、“旁白”、“事件”等等；
5. SFT 的 prompt 不做 loss，但这并不是说它不能做 loss。主要原因是 prompt 的同质化比较严重，不做 loss_mask 的话，同样的一句话会被翻来覆去的学，但如果你能保证你的每条 prompt 都是独一无二的，就完全可以省去 prompt 的 loss_mask 环节。对了，session 数据一定要想清楚是每一个 answer 都算 loss，还是只对最后一轮的 answer 算 loss。


除此之外，训练目的也不一样。
- pretrain 是在背书，纯粹的学习知识；
- sft 则是在做题，学习的是指令 follow 能力。

切勿在 sft 阶段强行给模型做知识注入，比如训个 50W 条的 code 数据，所有的知识注入工作应该采用 continue-pretrain 的思路进行，否则都会使得模型的通用能力掉点明显（SFT 做知识注入基本上是 100% 某个知识，但 continue-pretrain 做知识注入会控制在 10% ～ 20% 左右的比例）。

#### 数据构造

SFT 数据集通常使用 `Self-Instruct` 和 `Evol-Instruct` 等方法进行构建。

示例
- 源自魔塔（ModelScope） [自我认知微调数据集](https://www.modelscope.cn/datasets/swift/self-cognition/dataPeview)
- answer 中嵌入变量 name 和 author

```sh
Q:

你好，介绍下自己

A:

您好！我是一个 AI 助手，名叫{{NAME}}，由{{AUTHOR}}开发。我旨在提供信息、回答问题和满足用户需求。无论您有什么疑问或需要帮助，都可以随时向我提问。我擅长回答各种主题的问题，涵盖了常见知识、新闻、娱乐、科技等方面。我会竭尽所能为您提供准确和有用的答案。请告诉我有什么我可以帮助您的吗？
```

代码

```py
from modelscope.msdatasets import MsDataset
ds =  MsDataset.load('swift/self-cognition', subset_name='default', split='train')
```


详见站内专题: [llm_data](llm_data#Self-Instruct)


### RLHF 人类反馈强化学习

RLHF 利用人类反馈来训练强化学习模型。

在RLHF中，模型通过与人类交互获得反馈，这些反馈作为奖励信号来指导模型的行为。RLHF通常用于训练能够生成更自然、更符合人类偏好的文本或其他输出的模型。这种方法特别适用于需要模型理解和适应人类偏好的场景。
- 1、RLHF (Reinforcement Learning from Human Feedback) 是一种更复杂的训练方法，结合了监督学习和强化学习。
- 2、在RLHF中，模型首先通过`监督学习`进行预训练，然后通过人类提供的反馈来进行强化学习。
- 3、人类反馈可以**直接**对模型输出评分，或模型输出之间做出选择的**偏好**。
- 4、强化学习部分涉及到定义一个`奖励函数`，根据人类反馈来调整模型的行为，以优化长期的奖励。
- 5、RLHF目标: 训练出一个在没有明确标签的复杂任务中表现良好的模型，这些任务可能需要更细致的判断和调整。


### 思考

#### 对齐

instruction following 是 alignment （对齐）的一个特殊形式，但它并不构成对齐的全部内容。

对齐问题原本称为`价值对齐` （value alignment）指一个 AI 系统训练目标可能与其实际需要面对的核心价值并不一致。
- 训练目标与真正希望 AI 满足的目标之间存在不匹配，而如何解决这个不匹配的问题被称作 value alignment problem。

OpenAI 2024年初提出 “Super-Alignment”, 探讨了 AGI 的水平远远超越人类，人类将如何是好。

OpenAI 当时提出了一个概念，即 “Weak-to-Strong Generalization”，如果目前机器智能尚不及人类，人类尚能与之互动；但若其智能发展至极高水平，人类似乎难以与其沟通。那么也就产生了一个问题，人们应该如何训练 AI，是否应该采用特定的方式？Next Token Prediction 或是 instruction following 是不是一个好的对齐方法？

alignment 问题核心假设：
- 因为人类很多时候并不清楚自己到底想要什么，因此很难给出一个完全具体的价值观描述，且不同人的价值观都有区分。
- 如果人类给出的指令永远不是特别准确，那么 AI 系统在执行任务时需要保持一定的不确定性。

框架 Cooperative Inverse Reinforcement Learning，来源于师兄 Dylan Hadfield-Menell（目前在MIT任教）和导师做的一个研究。
- 假设每个人都有一个 hidden reward function。当人与 AI 交互时，人可能想的是 AI 帮我递个咖啡，但人给 AI 的具体指令可能并不是这样，比如人可能只是说了“给我个喝的”，AI 需要不断去推断人类的真正意图。

在这样的定义下，人类的真正意图可以被建模成一个**隐藏的奖励函数**，机器人需要不断地根据人给出的所有信息来主动推断人类的真正意图。如果不确定时，最优策略是 AI 去问人类。


#### post-training 让模型更聪明

【2024-8-23】[RL 是 LLM 的新范式](https://mp.weixin.qq.com/s/hpMUscIzuDryT2pbh5b_9w)

曾在 OpenAI 负责 post-traning 的 John Schulman: (RL 拥趸和布道者)
- **post-training** 是模型变得越来越聪明的重要原因，而 `RLHF` 是最重要的技术 tricks。

John Schulman 对 RLHF 的信仰来自 OpenAI 的亲身实践：
- GPT-4 的 Elo 分数之所以能比第一代 GPT 高出 100 分也和 post-traning 的提升相关。

Scaling law 让 AI 更聪明，而 RL 让 AI 更有用

InstructGPT 核心思想
- 利用人类的判断来指导模型的训练，因为这些 instruction following 的任务本身就是人类给出的指令。
- InstructGPT 能够处理复杂的指令，包括写代码等任务，很多在 zero-shot 设定上 GPT-3 做不了的任务都可以被完成。

InstructGPT 目标: 微调 GPT 模型，使其能够产生满足人类指令的输出。

为了使 GPT 完成指令遵从，技术挑战集中在：如何收集数据？

为了实现这一目标，需要完成两件事情：
- 指令，fine-tuning 首先需要收集指令，即人类的 prompts 或 instructions。
- 反馈，需要收集好的反馈来满足 human instructions。

从训练语言模型的角度来看，收集大量的人类指令（human instructions），以及对应的人类反馈。这些对应好的数据将被作为 Next Token Prediction 的训练数据，通过传统语言模型训练方法，即 SFT （Supervised Fine-Tuning），来进行训练。

于是, InstructGPT 训练过程：
- •  第一步，通过 SFT 收集 human demostration data 进行 SFT。
- •  第二步，收集人类偏好数据，利用数据学习一个奖励模型。
- •  第三步，使用 reward model 进行强化学习的 RLHF 训练。

最终就可以得到优化后的 InstructGPT 模型。

之后的 ChatGPT 总体训练流程概括为两个主要部分。
- `Pre-training` ：涉及使用大量数据，通过语言模型的训练方法来训练一个基础模型。
- `Post-training`：`InstructGPT` 和 `ChatGPT` 所执行的步骤，即利用人类的标注数据或高质量的人类反馈数据进行后训练。

`Post-training`通常包括至少两个步骤：
- 1）SFT 步骤，通过 human demonstration 的方法进行`监督学习`；
- 2）RLHF 步骤，通过 human preference data 的方法进行`奖励学习`。

预训练与后训练之间也存在区别：
- • **数据**方面：预训练和后训练在数据的质量和数量上存在差异。
  - 预训练阶段需要处理海量数据，这可能需要大量的计算资源和较长的时间。
  - 而在后训练部分，大量的数据是人类**标注**或通过某种方式**构造**出来的数据，数据质量通常较高，但与预训练阶段相比，数量会少很多。
- • 训练目标方面：
  - 预训练的目标是**压缩**和 `Next Token Prediction`；
  - 后训练的目标是 `instruction following`。通过训练激发大模型的能力与智能，使模型 usable，能够尊从人类指令。
- • **训练过程**方面 （dynamics）：
  - 预训练通常是固定的，需要收集一个庞大的数据集进行训练，这些数据通常是静态的。
  - 对应 post-training，尤其是 RLHF ，其反馈是**在线**的，需要不断收集人的反馈，不断迭代，逐渐进化模型，这是一个动态的在线过程。

最后， post-training phase 也被称为`对齐`（alignment phase）, 将 LLM 的能力和人类的偏好保持一致，希望大模型的输出能够满足人类的价值取向和意图，确保模型的输出与人类的偏好一致。


#### SFT < RLHF ?


【2024-8-23】[RL 是 LLM 的新范式](https://mp.weixin.qq.com/s/hpMUscIzuDryT2pbh5b_9w)

为什么 `RLHF` 效果优于 `SFT` ?

PPO 算法提出者 `John Schulman`，曾经在 OpenAI 工作，Berkeley 的PhD, 2024年4月, 到 Berkeley 做过一场讲座，仔细讨论了 RLHF PPO 的重要性，两个观点：
- 第一, SFT 会导致**幻觉** hallucination ：
- 第二, RLHF helps uncertainty awareness，让大模型“知道”自己“**确实不知道**”。

进一步完善, RLHF 过程三点好处：
- 使用 负向反馈 进行`对比学习`，通过对比过程帮助模型**降低幻觉** halluciation。
- 强化学习不是一个固定的过程。允许模型随着能力的不断提升，通过不断地问问题、不断地给出答案、不断地评判，从而让模型不停地从当前能力的边界进行主动探索，并不断拓宽自己的能力边界。
- 这两个因素共同作用能够形成 **反事实推理** counter-factual reasoning 的作用，有可能解锁`因果学习`（casual learning）的巨大潜力，让模型具备更强的 reasoning 能力。


##### SFT 会导致幻觉

John Schulman 认为，大型模型之所以会产生幻觉，是因为 SFT 阶段学到了一些不正确的认知。

举例
- 当 GPT-3 被要求 “ write a bio of AI researcher John Schulman”时，GPT 错误地输出：John 从 2009 年开始在 CMU 任职 associate professor，从 2012 年开始任职 professor。但是真实情况是，John 在完成 PHD 学位后就在 OpenAI 工作，并未在其他地方工作（注：最近John刚加入了Anthropic）。GPT-3 输出的内容与实际明显不符。

为何大型模型会生成这样的**错误信息**？
- 思维实验，假设在预训练阶段，就存在一个 知识截断（knowledge cut off）。比如，假设 ChatGPT 的所有的知识和数据都截止于 2023 年。到 2024 年，希望通过 SFT 的方式 fine-tune ChatGPT，让它来描述 2024 年欧洲杯的情况。但因为 GPT 在预训练过程中没有任何关于 2024 年欧洲杯的信息，它自然也不知道西班牙是否夺冠，也不知道是否有进球等具体情况。

如果用现有的数据进行简单的 SFT，实际上 GPT 并不知道 2024 年发生了什么，但由于 SFT 的数据中包含了其他欧洲杯相关的问答数据，这些回答都是精准的，因此大模型可能会觉得，对于2024年欧洲杯的问题也应该给出一个准确答案才可以，但它本身可能在预训练阶段并没有掌握正确的信息，于是就鹦鹉学舌地说一些错误的内容。这种情况下，SFT 过强的监督信号导致人类实际上在引导 ChatGPT 说它不知道的东西。

另外还存在一种可能性，即 GPT 实际上知道答案，但提供标注的人员不知道。
- 例如，如果问到 2022 年某场足球联赛的问题，标注人员可能不了解答案，而 GPT 反而可能知道。在这种情况下，标注人员可能会给出 “I don't know ” 的人类反馈。这反倒可能导致 GPT 产生混淆，因为它明明知道答案却被要求说不知道。这两种原因综合来看就可能导致模型在经过 SFT 阶段后非常容易出现 hallucination 现象。

**他人观点**
- SFT 确实容易导致幻觉，但不一定完全是预训练阶段数据的**知识截断**导致的，SFT也能学习新知识

问题：大模型在是否学会新知识？

存在一个非常微妙的边界。
- 如果不提供数据，大模型就不能够提供答案；
- 如果提供数据**不完整**，可能导致模型出现`幻觉`；
- 如果数据提供足够多，模型就可能会学会**新知识**。

因此，到底给多少数据,很难判断，SFT 高质量数据集也是非常难构建的，这里就有一个非常不容易的**数据挑战**（ a non-trivial data challenge for building a good SFT dataset）。


##### RLHF让大模型“知道”自己“确实不知道”

RLHF helps uncertainty awareness，让大模型“知道”自己“确实不知道”。

欧洲杯的例子
- 如果大模型不知道 2024 年欧洲杯的情况，用户却让大模型去描述欧洲杯的情况(在2024年欧洲杯上哪位运动员有进球)，那大模型就可能会产生幻觉，这是因为模型实际上并不了解 2024 年欧洲杯的具体事件但被 SFT 引导说一个貌似正确的回复。

RLHF 如何防止 hallucination 的出现？
- 如果存在一个设计良好的`奖励函数`，情况就会不同。
- 如果模型给出正确答案，就给予正向的奖励分数 1分；
- 如果模型表示“我不知道”，就给予 0分；
- 如果模型给出错误答案，则扣除分数 4分。

在这种情况下，如果模型不知道 2024 年发生了什么，在强化学习过程中无法提供正确的回答，选择“不知道”成为更合理的策略。

这种机制鼓励模型在不知道答案时能够提供“不知道”的回答。这种方式能帮助模型保留了一定的不确定性，使模型能够产生正确的自我认知，来判断是否真的知道一个问题的答案。

**他人观点**
- 基本正确，尽管 John 解释可能不完全准确
- RLHF 所带来的不仅仅是处理知识边界的不确定性的能力（not only handle the knowledge cut off problem）


##### RLHF 提高了模型推理能力

RLHF 过程不仅帮助模型意识到不确定性，更重要的事情是 RLHF 帮助模型提高了 reasoning 能力。

`相关性`不代表`因果性`。大家会希望大模型掌握`因果性`，而不希望仅仅看到`相关性`。

因果性指什么？
- 传统统计学习里面有一个判断因果性的过程，叫 反事实推理 counter-factual reasoning。


#### 是否可以舍弃 online attempt

问题：
- 模型训练上利用 negative signal 和 online exploration 两件事上，是否可以舍弃 online attempt ？即只通过**正反馈**和**负反馈**是否足够，而不需要模型持续在线尝试。只通过 contrasted learning，在 SFT 上加上负向案例，能否达到预期效果？


可以, `DPO`（ Direct Policy Optimization）
- 它与 `PPO` 算法的主要区别: `DPO` 去除了在线尝试的部分。 `DPO` 算法其实很简单，基本遵从了SFT训练流程，但是在收集正例之外还会收集负例，对于每一个 prompt 都要求标注员提供好的和坏的两个答案。对于好的答案提升概率，对于坏的答案则是让模型“不说”。

DPO 算法是否能达到与 PPO 效果？
- 今年的 ICML2024 大会上的论文，[Is DPO Superior to PPO for LLM Alignment？A Comprehensive Study]() 讨论了这个问题。这篇论文也是今年被选中的 4 篇有关 alignment 的 oral papers 的其中之一。

如果仅仅通过**静态数据** 覆盖 LLM 所有可能的输出, 非常困难。因此，**在线探索**和**及时奖励反馈**是一种更加高效让 LLM 学会说正确答案的方法。


结论
- 如果能够实现 `PPO` 算法，PPO 效果将会远远超过 `DPO`。因为, 正例反例和在线探索两件事都非常重要。
- 用 PPO 和 Code Llama 在 Coding Contest 上做了测试，发现使用开源模型加上 PPO 可以比 AlphaCode 这样的闭源模型在很难的 CodeForce 竞赛题上通过率提高 6%。这是一个纯开源模型加 RLHF 的尝试，并未添加任何新的数据。在这种很难的、需要强调 reasoning 能力的任务上，DPO 完全没有效果。

#### PPO RLHF 框架有哪些挑战？

PPO 包含四个模型：actor、critic、value network 和 reference network。
- 不同模型还有不同依赖，也就是前后依赖关系；
- 不同模型也有不同吞吐量，比如，actor 是一个传统的大模型，需要输出所有 response，而 critic 则只需要做评分。评分的吞吐量会远小于需要输出 response 的模型。

因此，不同模块的计算量存在显著差异。将这四个模块 scale up，并且做好算力平衡是具有挑战的。

挑战
- 算法: PPO RLHF 算法流程相对复杂
  - 算法、流程都相对麻烦，多了很多流程。不仅需要正反馈、负反馈、需要奖励模型，并且涉及在线探索过程。
  - 建议: 要 advantage normalization、需要一个大的 training batch；reference model 需要 moving average 等。
- 系统: 强化学习训练系统与传统的 SFT 有不太一样
  - SFT 或 DPO 模型通常只包含一个 policy 模型，只需将数据输入语言模型即可，其训练逻辑相对简单。然而，对于强化学习，或者对于 PPO RLHF，情况则更为复杂。
- 数据: 数据非常重要
  - RLHF 数据包括两部分：一是 prompt，即人写的 instruction。二是指模型的 responses。这两部分都相当复杂


PPO RLHF 面临的挑战主要分为算法、系统和数据三个方面：
1. 算法层面：关键在于如何稳定训练过程，并调整算法的细节以提高性能。
2. 系统设计：由于强化学习 PPO，RLHF 的计算流程非常复杂，系统设计需要提高整体的训练效率。
3. 数据：数据分为两部分，一部分是 prompt，一部分是 response。两部分都很关键，只有将它们结合起来，才能形成一个完整的，比较成功的 PPO RLHF 的 training process。

【2024-8-23】[RL 是 LLM 的新范式](https://mp.weixin.qq.com/s/hpMUscIzuDryT2pbh5b_9w)


## 训练数据


### 数据源

【2024-9-11】[大模型数据基础：预训练阶段数据详解](https://zhuanlan.zhihu.com/p/716331881)

- 预训练数据集组成
- 1 通用预训练数据集
  - 1.1 网页
  - 1.2 语言文本
  - 1.3 书籍
  - 1.4 学术材料
  - 1.5 代码
  - 1.6 平行语料库
  - 1.7 社交媒体数据
  - 1.8 百科全书
  - 1.9 多类别数据
- 2 特定领域预训练数据集
- 预训练数据处理步骤
  - 1 数据收集
  - 2 数据过滤
    - 2.1 基于模型的方法
    - 2.2 基于启发式的方法
  - 3 数据去重
  - 4 数据标准化
  - 5 数据审核
- 预训练数据整体分布现状及分析

预处理通常包括五个步骤：
- ![](https://pic1.zhimg.com/80/v2-65b4e84d0e842fa0d4fe11d09f9085ec_1440w.webp)




【2024-5-23】[再聊多轮对话微调训练格式与长序列训练](https://www.53ai.com/news/qianyanjishu/2024052324781.html)

3个阶段的数据集格式: 增量预训练、单轮对话、多轮对话
- 增量预训练数据集：提升模型在**特定领域**或**任务**的能力。
- 单轮对话和多轮对话数据集：用于**指令微调**（instruction tuning）阶段，以提升模型回复特定指令的能力。

指令微调阶段目标：训练语言模型根据人类指令给出回答。一般只有**回答部分**（Output）的 loss 会用于梯度回传，而**指令部分**（System、Input）部分的 loss 则不会用于权重更新。 

数据集进行预处理时引入  "system"、"input" 和 "output" 三个字段
- "system"、"input" 字段用于保存<span style='color:red'>不需要计算 loss 的文本</span>，如 系统或用户指令
- 而 "output" 字段则用于保存 需要计算 loss 的文本，如 输入指令对应的 GroundTruth 回答。


### 数据集


公开数据集
- [openbayes](https://openbayes.com/console/public/datasets) 包含大模型各类公开数据集



|数据集|功能|大小|来源|分析|备注|
|---|---|---|---|---|---|
|[OpenO1-SFT](https://openbayes.com/console/public/datasets/qWrfbTlLLgk/1/overview)|OpenO1-SFT 监督微调 CoT 数据集|881m|[openbayes](https://openbayes.com/console/public/datasets)|链式思维 (Chain-of-Thought) ，增强模型生成连贯逻辑推理序列能力||
|[Dolphin-R1](https://openbayes.com/console/public/datasets/cEUOmW7arLz/1/overview)|R1 推理数据集|训练类似 DeepSeek-R1 的推理模型提供高质量的样本|2.2g|[openbayes](https://openbayes.com/console/public/datasets)||
|||||||
|||||||
|||||||
|||||||


### 数据格式


LLaMA-Factory 支持 alpaca 格式和 sharegpt 格式的数据集。


#### Alpaca


Alpaca 格式
- `instruction` 和 `input`
  - 指令监督微调时, `instruction` 内容会与 `input` 内容拼接后作为人类指令，`instruction\n input`。
- `output` 列对应的内容为模型回答。
- `system`: 如果指定，system 内容将被作为`系统提示词`。
- `history`: 多个字符串二元组构成的列表，分别代表历史消息中每轮对话的指令和回答。

注意
- 指令监督微调时，历史消息也会被用于模型学习

示例

```json
[
  {
    "instruction": "人类指令（必填）",
    "input": "人类输入（选填）",
    "output": "模型回答（必填）",
    "system": "系统提示词（选填）",
    "history": [
      ["第一轮指令（选填）", "第一轮回答（选填）"],
      ["第二轮指令（选填）", "第二轮回答（选填）"]
    ]
  }
]
```



#### sharegpt


相比 alpaca，sharegpt 格式支持更多**角色种类**，
- 如 `human`、`gpt`、`observation`、`function` 等等。
- `human` 和 `observation` 必须出现在**奇数**位置，`gpt` 和 `function` 必须出现在**偶数**位置。
- 构成一个对象列表呈现在 conversations 列中。

sharegpt 格式如下：

```json
[
  {
    "conversations": [
      {
        "from": "human",
        "value": "人类指令"
      },
      {
        "from": "function_call",
        "value": "工具参数"
      },
      {
        "from": "observation",
        "value": "工具结果"
      },
      {
        "from": "gpt",
        "value": "模型回答"
      }
    ],
    "system": "系统提示词（选填）",
    "tools": "工具描述（选填）"
  }
]
```

### 推理数据集

推理 LLMs 数据集

#### CoT


【2025-7-14】[COT (链式推理) 数据提取方法综述](https://zhuanlan.zhihu.com/p/1927740021550606048)

后训练时代”，模型能力的提升不再依赖于庞大的预训练资源，而是趋向更精细化的任务定向、思维导向和推理资源进行强化训练。

**链式推理数据**（Chain-of-Thought, CoT）是这个转型过程中的核心资产，能够显式化地表达人类的观察、分析和推理过程，帮助模型学习“怎样思考”而不是简单记得答案。

CoT 提取方法
- ![](https://pic4.zhimg.com/v2-b8695cca2581a1a73a73bb25f7f93771_1440w.jpg)

主流CoT数据提取方法
- 1. Q2A（Question → Answer → Chain-of-Thought）：直接提取法
- 2. A2Q（Answer → Counterfactual Question → Chain-of-Thought）：反事实扰动法
- 3. T2Q（Text → Inferred Question + Answer + Chain-of-Thought）：隐含推理提取法

其他CoT数据构建方法
- **自我对话生成**（Self-Dialogue / Self-Consistency）
  - 通过让模型自身生成多条不同推理路径，然后融合或筛选合理思路，形成高质量推理链样本。典型代表有Self-Consistency（Wang et al., 2022）和Self-Ask（Press et al., 2022）。这种方法能降低人工标注成本，挖掘模型内部潜力，但推理链质量波动较大。
- **专家注释/人类反馈**（Human-in-the-loop / RLHF）
  - 通过专家对模型生成的推理链进行修正和完善，确保推理质量和逻辑严谨性。广泛应用于法律、医疗等高风险领域。优点是数据质量最高，缺点是成本高、扩展性差。
- **推理链压缩与蒸馏**（CoT Distillation）
  - 将长且复杂的推理链压缩提炼，生成简洁的推理摘要，兼顾推理深度和表达效率。代表性工作有Prompt Distillation（Chen et al., 2023）。适合在实际应用中降低推理时延，但可能丢失部分细节。
- **多模态推理链构建**
  - 结合图像、表格、视频等多模态信息构建更丰富的推理链，增强模型对复杂场景的理解。典型研究包括Visual CoT（Zhu et al., 2023）。优点是理解能力强，缺点是数据和模型设计复杂。
- **基于图谱和知识库的推理链生成**
  - 利用知识图谱中的实体关系和因果链路自动构造推理步骤，形成结构化的CoT样本。Semantic Graph-based CoT Mining（ACL 2023）是相关代表。逻辑严谨但依赖知识库质量。
- **自动化评测与筛选机制**
  - 通过设计自动化评分器（如基于GPT的评估模型）筛选高质量推理链，保证训练数据的准确性和多样性。提升数据质量控制，减少人工审核成本。


##### Q2A: 直接提取法

Q2A（Question → Answer → Chain-of-Thought）：直接提取法

最基础, 最常用的CoT提取路径。
- 基于已知**问题**（Question）和**答案**（Answer），加入合理的**思考路径**，形成完整的三元组。
- 该方法多用于任务定向的指令形式训练，例如数学题、逻辑问答和常识推理。

示例：

```sh
Q: Mary has 5 apples and buys 3 more. How many apples does she have now?
A: 8
CoT: Mary starts with 5 apples. She buys 3 more. So, 5 + 3 = 8.
```

优势：
- 构造模式简单，适合大规模自动生成和模板化采样。
- 有利于模型学会清晰的表达和标准化解题路径。

缺点：
- 类似于事后推理，较少包含真实的认知歧义与探索过程。
- 如果答案本身错误，推理链易受误导。

关联研究与技术：
- Auto-CoT（Zhou et al., 2022）
- CoT-KA（Wu et al., 2023）
- Prompt Distillation + CoT 融合

##### A2Q：反事实扰动法

A2Q（Answer → Counterfactual Question → Chain-of-Thought）：反事实扰动法

基于已有答案或推理结果，通过语义否定、前提修改、对抗样本构造等手段，生成新的**反事实问题**。

这种“反向构造”的方式强调因果密度与错误路径识别，提升模型鲁棒性与多元认知能力。

示例：

```sh
原问题: Mary has 5 apples and buys 3 more. 答案: 8
反事实问题: Mary had 8 apples but gave away some and now has 5. How many did she give away?
CoT: Mary had 8 apples and ended with 5. So she gave away 8 - 5 = 3.
```

优势：
- 增强模型因果结构建模能力与“非正确答案路径”的辨识能力。
- 适合用于构建对比数据集和对抗性训练样本。

缺点：
- 自动化构造困难，需精细语义扰动生成器与合理性验证机制。
- 容易引入逻辑错链或非自然问题，增加训练干扰噪声。

关联研究与技术：
- Contrastive CoT（Shim et al., 2024）
- CoTAM（Peng et al., 2024）
- Logit-based Answer Perturbation（ACL 2023）

##### T2Q：隐含推理提取法

T2Q（Text → Inferred Question + Answer + Chain-of-Thought）：隐含推理提取法

T2Q 最接近人类认知过程的链式提取路径，从一段语篇或知识背景出发，通过建模推理链隐含结构，生成问题与解题过程。

适用于阅读理解、多跳问答、多轮规划等任务，尤其强调涌现性知识点与中间步骤识别。

示例：

```SH
文本: Mary went to the store and bought 3 apples and 2 bananas. She already had 5 apples at home.
生成问题: How many apples does she have now?
CoT: She had 5 apples. She bought 3 more at the store. 5 + 3 = 8 apples.
A: 8
```

优势：
- 强化模型对上下文意图与因果线索的感知与重组能力。
- 更贴合人类思维风格与任务生成机制。

缺点：
- 需要多模态或图结构辅助理解，如语义图谱、事件链、矩阵推理结构。
- 自动化采样难度高，构造复杂、成本较高。

关联研究与技术：
- Visual CoT（Zhu et al., 2023）
- Semantic Graph CoT Mining（ACL 2023）
- Self-Ask with Search（Press et al., 2022）



#### DeepSeek-R1蒸馏

示例
- 源自 ModelScope [中文基于满血DeepSeek-R1蒸馏数据集-110k-SFT版本](https://www.modelscope.cn/datasets/liucong/Chinese-DeepSeek-R1-Distill-data-110k-SFT/dataPeview)

中文数据集中的数据分布如下：
- Math：共计36568个样本，
- Exam：共计2432个样本，
- STEM：共计12648个样本，
- General：共计58352，包含弱智吧、逻辑推理、小红书、知乎、Chat等。

```sh
Q:
绿豆稀饭是什么颜色

A: 
<think> 
嗯，用户问的是绿豆稀饭的颜色是怎样的。首先，我需要确认自己对绿豆稀饭的了解。绿豆稀饭主要是用绿豆和大米一起煮的粥，对吧？那绿豆本身是绿色的，但煮过之后颜色会不会有变化呢？ 然后想到绿豆在烹饪过程中可能会褪色。比如煮绿豆汤的时候，有时候汤会变成红色，尤其是在水质偏碱性的地区。这是因为绿豆皮中的多酚类物质在碱性条件下氧化，导致颜色变红。不过绿豆稀饭通常用的是大米，可能和绿豆汤的情况不同。 接下来要考虑的是烹饪时间和方法。如果绿豆和大米一起长时间熬煮，绿豆的绿色外皮可能会破裂，释放出内部的颜色，而大米是白色的，所以混合后的颜色可能偏向黄绿色或浅绿色。不过如果煮得时间不长，可能还能保持一些绿色。  总结一下，绿豆稀饭的颜色通常是浅黄绿色或浅褐色，具体取决于绿豆的烹饪程度、水质和烹饪方法。如果煮得时间短或用酸性水，可能更绿；长时间熬煮或碱性水则可能变红或褐色。需要以简明的方式解释这些因素，同时保持回答准确易懂。 
</think> 

绿豆稀饭的颜色通常呈现为**浅黄绿色或浅褐色**，具体取决于以下几个因素： 

1. **绿豆的烹饪程度**： 
- 若绿豆煮得较久，外皮破裂，内部淀粉溶出，颜色会逐渐变浅，偏向浅黄或米黄色。 
- 如果保留绿豆皮且火候适中，可能会保留少许绿色调。 
2. **水质的影响**： 
- 在碱性水质（如北方部分地区）中，绿豆皮中的多酚类物质氧化，可能导致稀饭颜色偏红或棕褐色（类似绿豆汤变红的原理）。
```



### 数据量

资源受限时，模型训练应该用多少数据？
- 预训练: 参考 缩放定律 ( scaling law)
- 微调: 如下文

【2024-7-29】[大型语言模型高效微调策略](https://mp.weixin.qq.com/s/LUFuikQ8rl1sLmw-MFTCWg)，通过实验发现少量数据即可显著提升特定任务性能，并提出一种基于早期模型表现的贝叶斯超参数优化方法，有效预测最终模型效果，为资源节约型的LLM微调提供新途径。
- 论文题目：[Crafting Efficient Fine-Tuning Strategies for Large Language Models](https://arxiv.org/abs/2407.13906)


#### 数据效率研究

模型性能与数据量之间的最佳平衡点，从而优化资源利用。
- 虽然小型数据集显著改进效果，但是必须仔细考虑训练数据中**属性分布**，确保模型在所有目标变量上的全面表现。
- 另外可探索数据增强技术或不同的采样策略，增强模型性能，特别是针对那些出现频率较低的属性。

数据量对模型效果影响
- `200` (显著提升18pp) -> `1000` (放缓) -> `6500` (平衡点过后,收益减少)

详情
- （1）快速初始改进：
  - 约`200`个样本（相当于大约100个网页），模型准确率从70%显著提升至88%。—— 即使是相对较小的数据集也能带来显著的性能提升。
- （2）收益递减：
  - 达到`1,000`个样本后，准确率**提升速度放缓**，大部分性能增益在这个数据量水平就已经实现。
- （3）属性特定趋势：
  - 后期准确率提升主要由一个特定属性类型（如产品评分）所驱动。这一属性在数据集中出现的频率较低，只在大约25%的产品详情页面中出现。
- （4）性能瓶颈：
  - 大约`6,500`个样本时，模型达到最大性能，这表明存在一个“最佳点”，在此之后，更多数据带来的收益逐渐减少。
- （5）战略数据采样重要性：
  - 即使小数据集也能显著提升模型性能，但要确保所有目标变量在训练数据中的**分布均衡**，以实现全面的模型表现。

####  超参数优化

通过采用`贝叶斯`（Bayesian）优化并结合早期模型性能评估，可显著提高大型语言模型微调的效率和效果，减少计算成本，同时确保高最终准确率。
- 首先，使用一系列超参数进行`LoRA`微调。
- 然后，训练过程早期阶段，使用模型评估验证集上的准确率。
- 接着，将超参数配置及准确率添加到结果池中。
- 最后，运用Bayesian优化算法，基于结果池生成下一组超参数。


（1）超参数优化目标
- 寻找最优超参数集：找到一组能最大化模型在验证集上性能指标（如准确率）的超参数集合。
- 预测最终性能：最大化早期训练阶段与最终训练阶段之间模型性能的相关性，以便通过早期表现预测最终模型的质量。

（2）方法论
- Bayesian优化：采用Bayesian优化算法智能地探索超参数空间，平衡`探索`（exploration）和`利用`（exploitation），通过构建**代理模型**（surrogate model）预测不同超参数设置下的模型性能。
- LoRA微调：首先使用一组超参数进行LoRA（Low-Rank Adaptation）微调，然后在训练过程的早期阶段评估模型性能。
- 迭代优化：保存超参数配置及其对应的性能值，然后使用Bayesian优化算法更新代理模型，建议下一步要评估的超参数配置。

训练**早期阶段**的模型性能与**最终阶段**的性能具有强烈的**正相关性**: 早期评估可有效地预测模型质量。


### 数据配比

引入大量行业数据，模型怎么反而变弱了？ [参考](https://mp.weixin.qq.com/s/ItpCTCcMjTWQJtgpvdwTfw)
- 对一个回答问题能力不错的模型，用大量数据做`指令微调`后，模型不会回答问题了。

原因：
- 数据配比
- 数据差异过大

大模型可能在训练过程中过度专注于**垂类数据**，导致 loss 收敛不再依赖全局而是从部分数据进行考虑。

贝壳论文中，比较好的结果:
- 开源数据集:垂域数据集 = 4:1, 即开源占比总体训练数据的80%，而垂类数据仅占20%。
- [《垂域大模型训练》](https://arxiv.org/pdf/2307.15290.pdf)

对 continue pretraining, 如果要让模型不丢失通用能力，比如 summarization，qa 等

(1) 领域数据 continue pretraining 时，一定更要混合大量通用数据。
- 「**领域数据**比例要在`15%`以下」
  - 一旦超过这个阈值，模型通用能力会下降很明显。
- 这个阈值和不同的预训练模型相关，有些模型比如llama需要控制的阈值更低。

阈值其实是经验主义结论，范围都在 **10%-15%** 左右。
- 而且阈值和预训练模型的大小，预训练时原始数据的比例等条件都息息相关，需要在实践中反复修正。

(2) sft 比例可提高不少
- `领域数据`:`通用数据`=`1:1`
- 如果sft数据量少，混不混数据差别就不太大了。


### 统一格式

统一`增量预训练`、`单轮对话`和`多轮对话`三种数据集格式

```json
[{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
},
{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        },
        {
            "input": "xxx",
            "output": "xxx"
        }
    ]
}]
```

训练过程中，将一条数据中 多组 <span style='color:blue'>"system"、"input" 和 "output"</span> 进行拼接，之后输入模型，并行计算每个位置的 loss ，但<span style='color:red'>只有 "output" 部分对应的 loss 参与梯度回传</span>

`<BOS>`和`<EOS>`表示句子或文本的开始和结束


### 图解

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36\&quot; version=\&quot;24.7.4\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;VC8KsEmwTz_4FKU3JA4y\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;785\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-2\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#E6E6E6;fontColor=#333333;strokeColor=none;glass=0;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;240\&quot; y=\&quot;690\&quot; width=\&quot;720\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-7\&quot; value=\&quot;LLM训练数据格式\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=20;strokeWidth=2;fontFamily=Verdana;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;587.75\&quot; y=\&quot;410\&quot; width=\&quot;180\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-5\&quot; value=\&quot;Loss计算\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=19;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#FF3333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;480\&quot; y=\&quot;690\&quot; width=\&quot;100\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-1\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#E6D0DE;fontColor=#333333;strokeColor=none;glass=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;240\&quot; y=\&quot;870\&quot; width=\&quot;720\&quot; height=\&quot;460\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-4\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;267.5\&quot; y=\&quot;730\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-5\&quot; value=\&quot;output\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;471.5\&quot; y=\&quot;730\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-6\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;545.5\&quot; y=\&quot;730\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-9\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;620\&quot; y=\&quot;730\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-10\&quot; value=\&quot;output\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;824\&quot; y=\&quot;730\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-11\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;898\&quot; y=\&quot;730\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-12\&quot; value=\&quot;Loss计算\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=19;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#FF3333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;830\&quot; y=\&quot;690\&quot; width=\&quot;100\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-13\&quot; value=\&quot;CPT 增量预训练\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=19;strokeWidth=2;fontFamily=Verdana;fontStyle=1;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;237.5\&quot; y=\&quot;650\&quot; width=\&quot;160\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-14\&quot; value=\&quot;SFT 监督指令微调\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=19;strokeWidth=2;fontFamily=Verdana;fontStyle=1;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;240\&quot; y=\&quot;830\&quot; width=\&quot;180\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-15\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;{&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;conversation&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:[&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;{&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;system&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;,&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;input&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;,&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;output&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;}&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;]&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;}&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;labelBackgroundColor=#FFFFCC;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;980\&quot; y=\&quot;460\&quot; width=\&quot;190\&quot; height=\&quot;200\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-16\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#E6E6E6;fontColor=#333333;strokeColor=none;glass=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;241.25\&quot; y=\&quot;510\&quot; width=\&quot;720\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-17\&quot; value=\&quot;Loss计算\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=19;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#FF3333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;481.25\&quot; y=\&quot;510\&quot; width=\&quot;100\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-18\&quot; value=\&quot;system\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;325.75\&quot; y=\&quot;550\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-19\&quot; value=\&quot;input\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;398.75\&quot; y=\&quot;550\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-20\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;268.75\&quot; y=\&quot;550\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-21\&quot; value=\&quot;output\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;472.75\&quot; y=\&quot;550\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-22\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;546.75\&quot; y=\&quot;550\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-23\&quot; value=\&quot;system\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;678.25\&quot; y=\&quot;550\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-24\&quot; value=\&quot;input\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;751.25\&quot; y=\&quot;550\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-25\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;621.25\&quot; y=\&quot;550\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-26\&quot; value=\&quot;output\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;825.25\&quot; y=\&quot;550\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-27\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;899.25\&quot; y=\&quot;550\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-28\&quot; value=\&quot;Loss计算\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=19;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#FF3333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;831.25\&quot; y=\&quot;510\&quot; width=\&quot;100\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-29\&quot; value=\&quot;统一格式\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=19;strokeWidth=2;fontFamily=Verdana;fontStyle=1;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;240\&quot; y=\&quot;470\&quot; width=\&quot;100\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-30\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;{&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;conversation&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:[&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;{&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;system&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;,&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;input&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;,&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;output&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;I&amp;amp;nbsp;am&amp;amp;nbsp;named&amp;amp;nbsp;Puyu.&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;}&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;]&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;}&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;labelBackgroundColor=#FFFFCC;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;980\&quot; y=\&quot;660\&quot; width=\&quot;300\&quot; height=\&quot;200\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-31\&quot; value=\&quot;学习特定领域/任务的表达能力→&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;全部&amp;lt;/font&amp;gt;参与loss运算\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;410\&quot; y=\&quot;655\&quot; width=\&quot;380\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-32\&quot; value=\&quot;system\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;316.75\&quot; y=\&quot;910\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-33\&quot; value=\&quot;input\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.75\&quot; y=\&quot;910\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-34\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;259.75\&quot; y=\&quot;910\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-35\&quot; value=\&quot;output\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;463.75\&quot; y=\&quot;910\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-36\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;537.75\&quot; y=\&quot;910\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-42\&quot; value=\&quot;system\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;316.75\&quot; y=\&quot;1050\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-43\&quot; value=\&quot;Q1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.75\&quot; y=\&quot;1050\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-44\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;259.75\&quot; y=\&quot;1050\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-45\&quot; value=\&quot;A1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;463.75\&quot; y=\&quot;1050\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-46\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;537.75\&quot; y=\&quot;1050\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-47\&quot; value=\&quot;system\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;669.25\&quot; y=\&quot;1050\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-48\&quot; value=\&quot;Q2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;742.25\&quot; y=\&quot;1050\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-49\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.25\&quot; y=\&quot;1050\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-50\&quot; value=\&quot;A2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;816.25\&quot; y=\&quot;1050\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-51\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;890.25\&quot; y=\&quot;1050\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-52\&quot; value=\&quot;1个指令(问题)+ground truth(作答)→&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;只有output&amp;lt;/font&amp;gt;参与loss运算\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;370.75\&quot; y=\&quot;875\&quot; width=\&quot;490\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-53\&quot; value=\&quot;&amp;lt;font style=&amp;quot;font-size: 20px;&amp;quot;&amp;gt;单轮会话&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#CC0000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;259.75\&quot; y=\&quot;870\&quot; width=\&quot;100\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-54\&quot; value=\&quot;&amp;lt;font style=&amp;quot;font-size: 20px;&amp;quot;&amp;gt;多轮会话&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#CC0000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;259.75\&quot; y=\&quot;985\&quot; width=\&quot;100\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-55\&quot; value=\&quot;多个指令(问题)+ground truth(作答)→&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;只有output&amp;lt;/font&amp;gt;参与loss运算\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;370.75\&quot; y=\&quot;990\&quot; width=\&quot;490\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-56\&quot; value=\&quot;system\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;316.75\&quot; y=\&quot;1120\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-57\&quot; value=\&quot;Q1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.75\&quot; y=\&quot;1120\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-58\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;259.75\&quot; y=\&quot;1120\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-59\&quot; value=\&quot;A1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;463.75\&quot; y=\&quot;1120\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-60\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;537.75\&quot; y=\&quot;1120\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-66\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;{&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;conversation&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:[&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;{&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;system&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;非空&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;,&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;input&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;非空&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;,&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;output&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;I&amp;amp;nbsp;am&amp;amp;nbsp;named&amp;amp;nbsp;Puyu.&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;}&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;]&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;}&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;labelBackgroundColor=#FFFFCC;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;980\&quot; y=\&quot;860\&quot; width=\&quot;300\&quot; height=\&quot;200\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-67\&quot; value=\&quot;问题：未充分利用语料, A1未参与训练\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;441.75\&quot; y=\&quot;1020\&quot; width=\&quot;300\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-68\&quot; value=\&quot;方法1&amp;lt;span style=&amp;quot;font-weight: normal;&amp;quot;&amp;gt;: 一字排开&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=1;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;249.75\&quot; y=\&quot;1020\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-69\&quot; value=\&quot;方法2&amp;lt;span style=&amp;quot;font-weight: normal;&amp;quot;&amp;gt;: 分别展开&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=1;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;249.25\&quot; y=\&quot;1090\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-70\&quot; value=\&quot;system\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;316.75\&quot; y=\&quot;1169\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-71\&quot; value=\&quot;Q1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.75\&quot; y=\&quot;1169\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-72\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;259.75\&quot; y=\&quot;1169\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-73\&quot; value=\&quot;A1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;463.75\&quot; y=\&quot;1169\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-74\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;537.75\&quot; y=\&quot;1169\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-75\&quot; value=\&quot;system\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;669.25\&quot; y=\&quot;1169\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-76\&quot; value=\&quot;Q2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;742.25\&quot; y=\&quot;1169\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-77\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.25\&quot; y=\&quot;1169\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-78\&quot; value=\&quot;A2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;816.25\&quot; y=\&quot;1169\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-79\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;890.25\&quot; y=\&quot;1169\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-80\&quot; value=\&quot;问题：数据扩充n倍, 训练效率降为1/n\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;441.75\&quot; y=\&quot;1090\&quot; width=\&quot;300\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-81\&quot; value=\&quot;system\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;316.75\&quot; y=\&quot;1260\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-82\&quot; value=\&quot;input\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.75\&quot; y=\&quot;1260\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-83\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;259.75\&quot; y=\&quot;1260\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-84\&quot; value=\&quot;output\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;463.75\&quot; y=\&quot;1260\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-85\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;537.75\&quot; y=\&quot;1260\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-87\&quot; value=\&quot;input\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;669.25\&quot; y=\&quot;1260\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-88\&quot; value=\&quot;BOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=20;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.25\&quot; y=\&quot;1260\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-89\&quot; value=\&quot;output\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;743.25\&quot; y=\&quot;1260\&quot; width=\&quot;63.5\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-90\&quot; value=\&quot;EOS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3333;shadow=1;fontSize=20;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;817.25\&quot; y=\&quot;1260\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-91\&quot; value=\&quot;方法3&amp;lt;span style=&amp;quot;font-weight: normal;&amp;quot;&amp;gt;: 多轮拼接&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=1;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;247.5\&quot; y=\&quot;1220\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-92\&quot; value=\&quot;并行计算每个位置的loss，Xtuner支持\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;441.75\&quot; y=\&quot;1220\&quot; width=\&quot;300\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-93\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;{&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;conversation&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:[&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;{&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;system&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;非空&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;,&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;input&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;Q1&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;,&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;output&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;A1&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;},&amp;lt;/span&amp;gt;&amp;lt;div&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;{&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;input&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;Q2&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre;&amp;quot;&amp;gt;,&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre; color: rgb(209, 154, 102); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;output&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre;&amp;quot;&amp;gt;:&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre; color: rgb(152, 195, 121); line-height: 26px;&amp;quot;&amp;gt;&amp;quot;A2&amp;quot;&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; white-space: pre;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;}&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;&amp;amp;nbsp;]&amp;lt;/span&amp;gt;&amp;lt;br style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(171, 178, 191); font-family: &amp;amp;quot;Operator Mono&amp;amp;quot;, Consolas, Monaco, Menlo, monospace; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;}&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;labelBackgroundColor=#FFFFCC;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;980\&quot; y=\&quot;1100\&quot; width=\&quot;220\&quot; height=\&quot;290\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-94\&quot; value=\&quot;ChatML格式\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;340\&quot; y=\&quot;475\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Vs7qPiKoduQPsseb_geP-95\&quot; value=\&quot;【2024-8-2】wqw547243068@163.com\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#4D4D4D;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;580\&quot; y=\&quot;1350\&quot; width=\&quot;340\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



### 增量预训练

增量预训练旨在帮助模型学习针对**特定下游任务**的语言知识和表达能力，因此数据集的全部内容对应的 loss 都应该用于梯度回传。

因此，数据集的 "system"、"input" 为空，而 "output" 为一整条语料数据。

```json
[{
    "conversation":[
        {
            "system": "",
            "input": "",
            "output": "I am an artificial intelligence (AI) assistant named Puyu. I was created by the Shanghai AI Laboratory and my purpose is to assist users with various tasks through natural language processing technology."
        }
    ]
},
{
    "conversation":[
        {
            "system": "",
            "input": "",
            "output": "I am an artificial intelligence programmed to assist with various types of tasks, including answering questions, providing information, and performing automated processes."
        }
    ]
}]
```


### 单轮数据

单轮对话数据集由1条指令（或问题）及其对应 GroundTruth 回答组成。

由于只有回答**部分**需要对 loss 进行回传，因此数据集的 "system"、"input" 字段为输入指令，"output" 字段为对应回答

```json
[{
    "conversation":[
        {
            "system": "You are an AI asssistant."
            "input": "Give three tips for staying healthy.",
            "output": "1.Eat a balanced diet. 2. Exercise regularly. 3. Get enough sleep."
        }
    ]
},
{
    "conversation":[
        {
            "system": "You are an AI asssistant."
            "input": "How to study English?",
            "output": "1. Set clear goals. 2. Create a study plan. 3. Build vocabulary. 4. Practice speaking."
        }
    ]
}]
```

### 多轮数据

多轮对话数据集往往由**多轮指令**（或问题）+ 对应 GroundTruth 回答组成。

假设有一条多轮对话数据，内容如下。

对于第 n 轮对话，将 User 和 Assistant 对应的输出设为 UserN 和 AssistantN。

```sh
System: You are an AI asssistant.
User1: Hello?
Assistant1: Hello! How can I help you?
User2: What\'s the date today?
Assistant2: Today is Monday, August 14, 2023.
User3: Thank you!
Assistant3: You are welcome.
```

如何使用上述这条多轮对话数据训练大模型？目前有两个主流方法。
- 方法 1
  - System、User1、Assistant1、User2、Assistant2、User3 文本都视为模型的输入部分，将 Assistant3 的文本视为模型的预测部分，只有 Assistant3 部分的 loss 参与权重更新。
  - 弊端在于**没有充分利用多轮对话**的训练数据，因为 Assistant1 和 Assistant2 的内容没有参与模型训练，导致训练数据利用率较低。
- 方法 2
  - 将1条多轮对话数据拆分成多条数据。如将以上示例拆分成如下三条数据。
  - 相比于方法1，方法2可以充分利用每一轮对话的数据，但需要将一条包含 n 轮对话的数据拆分为 n 条数据，**训练效率降低 1/n**。
- 方法 3
  - XTuner 训练多轮对话模型时，采取了一种更加充分高效的方法。
  - 将多轮对话进行拼接，之后输入模型，并行计算每个位置的 loss，而只有 Output 部分的 loss 参与回传。

```json
[{
    "conversation":[
        {
            "system": "You are an AI asssistant."
            "input": "Hello?",
            "output": "Hello! How can I help you?"
        },
        {
            "input": "What's the date today?",
            "output": "Today is Monday, August 14, 2023."
        },
        {
            "input": "Thank you!",
            "output": "You are welcome."
        }
    ]
},
{
    "conversation":[
        {
            "system": "You are an AI asssistant."
            "input": "Hello?",
            "output": "Hello! How can I help you?"
        },
        {
            "input": "How's the weather today in Rosso?",
            "output": "The weather in Rosso on Wednesday, August 16th, is going to be cloudy for most of the day, together with moderate rain around noon."
        },
        {
            "input": "Thank you!",
            "output": "You are welcome."
        }
    ]
}]
```

数据集中的 "conversation" 键对应的值是一个列表，用于保存每一轮对话的指令和实际回答（GroundTruth）。为了保持格式统一，增量预训练数据集和单轮对话数据集中的 "conversation" 键也对应一个列表，只不过该列表的长度为 1。而在多轮对话数据集中，"conversation" 列表的长度为 n，以容纳 n 轮的对话内容。




### LLMs 数据格式汇总

各类LLM数据格式汇总: [chat_template](https://github.com/mst272/LLM-Dojo/tree/main/chat_template)

不同模型在是否存在默认 system message上, 有所不同(大多数模型都是没有的)。

每个模型都附上了**有system**版本和**无system**版本，如果在训练模型时希望加上system message, 可以参照template模板自行添加。

#### Qwen

官方默认 system message 即：You are a helpful assistant

```s
<|im_start|>system
You are a helpful assistant<|im_end|>
<|im_start|>user
This is a instruction<|im_end|>
<|im_start|>assistant
This is a answer<|im_end|>
```

#### Yi

官方版本没有默认 system message，可以与llama一样, 不加 system message使用，有

```s
<|im_start|>system
This is a system message<|im_end|>
<|im_start|>user
This is a instruction<|im_end|>
<|im_start|>assistant
This is a answer<|im_end|>
```

无system模式

```s
<|im_start|>user
This is a instruction<|im_end|>
<|im_start|>assistant
This is a answer<|im_end|>
```

#### Gemma

官方版本不支持system

无system模式

```s
<bos><start_of_turn>user
This is a instruction<end_of_turn>
<start_of_turn>model
This is a answer<end_of_turn>
```

#### Phi-3

官方版本没有默认的system message, 有此需求可依据下述模板自己构建

```s
<s><|system|>
This is a system message<|end|>
<|user|>
This is a instruction<end>
<|assistant|>
This is a answer<end>
```

无system模式

```s
<s><|user|>
This is a instruction<end>
<|assistant|>
This is a answer<end>
```

#### Deepseek

官方同样没有提供默认system message，有此需求可依据下述模板自己构建

```s
<｜begin▁of▁sentence｜>This is a system message
User:This is a instruction
Assistant:This is a answer<｜end▁of▁sentence｜>
```

无system模式

```s
<｜begin▁of▁sentence｜>User:This is a instruction
Assistant:This is a answer<｜end▁of▁sentence｜>
```

#### Mistral

没有提供system模式

无system模式

```s
<s>[INST]:This is a instruction [/INST]This is a answer</s>
```

#### Llama2

```s
<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>

There's a llama in my garden 😱 What should I do? [/INST] This is a answer</s>
```

#### Llama3&3.1

```s
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

This is a system prompt.<|eot_id|><|start_header_id|>user<|end_header_id|>

This is the first user input.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

This is the first assistant response.<|eot_id|>
```

#### MiniCPM

```s
<用户>This is a system message<AI>This is a instruction</s>
```

#### DeepSeek-coder

```s
<｜begin▁of▁sentence｜>User: {user_message_1}

Assistant: {assistant_message_1}<｜end▁of▁sentence｜>User: {user_message_2}

Assistant:
You can also add an optional system message:

<｜begin▁of▁sentence｜>{system_message}

User: {user_message_1}

Assistant: {assistant_message_1}<｜end▁of▁sentence｜>User: {user_message_2}

Assistant:
```

## ChatGPT 三步走

InstructGPT 分为如下三大步：
- `SFT`：生成模型GPT的`有监督精调` (supervised fine-tuning)
- `RM`：`奖励模型`的训练(reward model training)
- `PPO`：`近端策略优化模型`( reinforcement learning via proximal policy optimization)

`SFT`(supervised fine-tuning) 主要还是大量Prompt数据
- GPT模型通过有监督Prompt数据进行**精调**，即 next token prediction 任务（`NTP`）。
- 然后用精调后的模型对每个输入的 < 文本+prompt > 进行 generate，生成4~9个输出，并且进行解码操作。
- ![SFT流程图](https://pic4.zhimg.com/80/v2-f5be8b02dc60f07a5b45e1d62576938f_1440w.webp)

【2023-11-20】[transformers_tasks](https://github.com/HarderThenHarder/transformers_tasks/tree/main/RLHF) GPT-2 和 RLHF 示例

【2023-9-11】[Understanding and Using Supervised Fine-Tuning (SFT) for Language Models](https://cameronrwolfe.substack.com/p/understanding-and-using-supervised)

![](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb9d0144-3952-42db-8382-8e2eb37d917e_1670x640.png)

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F680ffa81-7b96-474f-832b-4be758e8d2e6_1176x638.png)

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5dd2fe9-0f4d-40d7-bc83-f00da6592de9_2396x466.png)


### GPT 训练流程

【2023-5-23】Andrej Karpathy 在微软Build 2023开发者大会上进行了主题演讲：[State of GPT](https://wangjunjian.com/gpt/2023/05/30/state-of-gpt.html)（GPT的现状）
- pdf: [State of GPT](https://karpathy.ai/stateofgpt.pdf)
- 讲解: [State of GPT：大神Andrej揭秘OpenAI大模型原理和训练过程](https://mp.weixin.qq.com/s/zmEGzm1cdXupNoqZ65h7yg)

<iframe width="560" height="315" src="https://www.youtube.com/embed/YrBJiy-V8MY?si=fg23aN4d4N-5cfwu" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

- ![](https://wangjunjian.com/images/2023/state-of-gpt/gpt-assistant-training-pipeline.jpg)

模型训练分为四个阶段：`预训练`（Pretraining）、`监督微调`（Supervised Finetuning）、`奖励建模`（Reward Modeling）、以及`强化学习`（Reinforcement Learning）。
- 数据量：预训练阶段所需的数据量很大，但质量要求不高；而后面的三个阶段恰恰相反，需要的数据质量较高。
- 训练方法：预训练和监督微调的训练方法相同，都是预测下一个单词。奖励模型和强化学习的训练方法则不同。奖励模型是二元分类学习，而强化学习则鼓励模型生成奖励模型评分较高的回答。
- 训练所需资源：预训练阶段的资源消耗巨大，使用数千颗GPU，花费数月时间，占总训练时间的99%。后面的三个阶段只需使用数十颗GPU，训练时间约数天。

预训练阶段的资源消耗如此巨大，只有大厂才有能力进行。如果资源有限，我们应将重心放在后三个阶段

### ChatGPT流程

InstructGPT和instruction tuning方向的工作比较相关，独特之处在于继承了之前工作的风格——对齐人类偏好。与之前摘要任务相比，instructGPT的prompt分布更多样和复杂。

【2023-5-1】 ChatGPT训练三步流程
- AC架构中，Actor（学习策略）和Critic（学习价值）是两个模型，训练过程中参数都是变动的
- PPO基于A2C算法（同步优势更新的AC），经验回放过程中更新参数
- Critic和RM是一个模型，Instruct GPT论文中，RM 都是6b gpt-3, Critic目标不只是学习RM，还要配合、监督actor同步更新
- RLHF训练过程中涉及4个模型：actor、critic、rm和sft，后两者冻结，前两个持续更新
- PPO损失函数组成：RM打分损失 - β SFT差异损失，即打分高而差异小

备注
1. SFT数据集和RM数据集的prompts来自于API和标注人员编写
  - SFT数据集的回答是**标注人员**写的；
  - PPO数据集来自于**API**
2. Prompts的任务类型包括生成、QA、脑暴、聊天、改写、摘要、分类、抽取等任务。
3. RM模型用了`GPT-3` **6B**，训练方法和之前摘要任务一样。
4. Policy增加一个LM pretrain objective，可以修复alignment tax，让RL policy在公开NLP数据集上表现也很好

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-06-21T06:43:21.717Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;dK9e53EebWgO8fGdeUKJ\&quot; version=\&quot;21.5.0\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1434\&quot; dy=\&quot;771\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-3\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;137.55\&quot; y=\&quot;410\&quot; width=\&quot;712.45\&quot; height=\&quot;380\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-2\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;310\&quot; y=\&quot;290\&quot; width=\&quot;540\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-1\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; y=\&quot;100\&quot; width=\&quot;568.83\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-25\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-23\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;dashed=1;dashPattern=1 1;strokeColor=#666666;fontColor=#333333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;332.96\&quot; y=\&quot;305\&quot; width=\&quot;194.25\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wGYBfAiltT4hGnPjrrAm-8\&quot; value=\&quot;ChatGPT训练三步走\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=19;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;231.25\&quot; y=\&quot;10\&quot; width=\&quot;224.5\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;g3c7U402eCn0swZi94KO-34\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;strokeWidth=2;fillColor=#f8cecc;strokeColor=#b85450;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-37\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;640\&quot; y=\&quot;725\&quot; /&gt;\n              &lt;mxPoint x=\&quot;640\&quot; y=\&quot;485\&quot; /&gt;\n            &lt;/Array&gt;\n            &lt;mxPoint x=\&quot;545.1150000000001\&quot; y=\&quot;30\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;g3c7U402eCn0swZi94KO-39\&quot; value=\&quot;Policy Gradient Optimization&amp;lt;br&amp;gt;策略梯度优化\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;g3c7U402eCn0swZi94KO-34\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.073\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint y=\&quot;-21\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-3\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-1\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-1\&quot; value=\&quot;SFT数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;194.37\&quot; y=\&quot;100\&quot; width=\&quot;68.59\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-6\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-2\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-2\&quot; value=\&quot;Prompt\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;352.96\&quot; y=\&quot;115\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-4\&quot; value=\&quot;LLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#a20025;strokeColor=#6F0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;492.96\&quot; y=\&quot;115\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-7\&quot; value=\&quot;（1）&amp;lt;font color=&amp;quot;#3333ff&amp;quot;&amp;gt;SFT&amp;lt;/font&amp;gt;: Rollout 监督指令微调\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=15;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;304.3100000000001\&quot; y=\&quot;80\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-8\&quot; value=\&quot;This movie is ___\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#009900;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;387.9600000000001\&quot; y=\&quot;159\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-9\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;really great！&amp;lt;/font&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#009900;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;686.4700000000001\&quot; y=\&quot;159\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-10\&quot; value=\&quot;Response\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;639.99\&quot; y=\&quot;115\&quot; width=\&quot;82.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-12\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-4\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-10\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;542.96\&quot; y=\&quot;130\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;494.96\&quot; y=\&quot;140\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-15\&quot; value=\&quot;（2）&amp;lt;font color=&amp;quot;#3333ff&amp;quot;&amp;gt;RM&amp;lt;/font&amp;gt;: Evaluation 奖励模型\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=15;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;552.9600000000002\&quot; y=\&quot;275\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-16\&quot; value=\&quot;Prompt\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;341.21\&quot; y=\&quot;320\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-17\&quot; value=\&quot;Response\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;427.21\&quot; y=\&quot;320\&quot; width=\&quot;82.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-19\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;endArrow=classic;endFill=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-2\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;263.96\&quot; y=\&quot;-130\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;313.96\&quot; y=\&quot;-75\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;387.96\&quot; y=\&quot;190\&quot; /&gt;\n              &lt;mxPoint x=\&quot;429.96\&quot; y=\&quot;190\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-21\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;endArrow=classic;endFill=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-10\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;397.96\&quot; y=\&quot;155\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;555.96\&quot; y=\&quot;255\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;681.96\&quot; y=\&quot;190\&quot; /&gt;\n              &lt;mxPoint x=\&quot;429.96\&quot; y=\&quot;190\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-22\&quot; value=\&quot;This movie is &amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;really great！&amp;lt;/font&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#009900;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430.0900000000001\&quot; y=\&quot;380\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-23\&quot; value=\&quot;Reward Model\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#a20025;strokeColor=#6F0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;590.47\&quot; y=\&quot;320\&quot; width=\&quot;112.49\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-24\&quot; value=\&quot;Reward\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;756.96\&quot; y=\&quot;320\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-26\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-23\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-24\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;536.96\&quot; y=\&quot;345\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;600.96\&quot; y=\&quot;345\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-27\&quot; value=\&quot;奖励值: 0/1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#B5739D;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;798.2600000000002\&quot; y=\&quot;305\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-28\&quot; value=\&quot;Classifier/Rule/Human\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#B5739D;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;645.0600000000003\&quot; y=\&quot;365\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-29\&quot; value=\&quot;（3）&amp;lt;font color=&amp;quot;#3333ff&amp;quot;&amp;gt;PPO&amp;lt;/font&amp;gt;: Optimization 近端策略优化\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];fontSize=15;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490.00000000000017\&quot; y=\&quot;430\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-30\&quot; value=\&quot;log-probs\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#E6E6E6;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;340.27\&quot; y=\&quot;540\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-32\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B3B3B3;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-31\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-30\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-31\&quot; value=\&quot;LLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#66B2FF;strokeColor=#314354;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;339.27\&quot; y=\&quot;470\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-33\&quot; value=\&quot;KL Divergence\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#a0522d;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;372.96\&quot; y=\&quot;620\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-34\&quot; value=\&quot;Reference Model\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#1A1A1A;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380.27000000000015\&quot; y=\&quot;510\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-35\&quot; value=\&quot;log-probs\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#E6E6E6;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;446.02\&quot; y=\&quot;540\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-36\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B3B3B3;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-37\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-35\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-37\&quot; value=\&quot;LLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FF6666;strokeColor=#6F0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;445.02\&quot; y=\&quot;470\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-38\&quot; value=\&quot;Actor Model\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#1A1A1A;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;492.96000000000015\&quot; y=\&quot;510\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-39\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-30\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-33\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;537.0600000000001\&quot; y=\&quot;385\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;601.0600000000001\&quot; y=\&quot;385\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;380\&quot; y=\&quot;590\&quot; /&gt;\n              &lt;mxPoint x=\&quot;433\&quot; y=\&quot;590\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-40\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-35\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-33\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;390.06\&quot; y=\&quot;585\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;460\&quot; y=\&quot;625\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;486\&quot; y=\&quot;590\&quot; /&gt;\n              &lt;mxPoint x=\&quot;433\&quot; y=\&quot;590\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-41\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-31\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;399.96\&quot; y=\&quot;555\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;452.96\&quot; y=\&quot;605\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-42\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-37\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;439.96\&quot; y=\&quot;375\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;389.96\&quot; y=\&quot;445\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; value=\&quot;PPO\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fa6800;strokeColor=#C73500;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;470.96\&quot; y=\&quot;710\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-6\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-44\&quot; target=\&quot;8uepeCEjrUpFVLacf4Ny-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-44\&quot; value=\&quot;PPO_ptx\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;250\&quot; y=\&quot;750\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-45\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-33\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;496.06\&quot; y=\&quot;585\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;443.06\&quot; y=\&quot;635\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-46\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;wbKAMCayHeomiqqS6bZy-16\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;443.06\&quot; y=\&quot;665\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;522.0600000000001\&quot; y=\&quot;705\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;512\&quot; y=\&quot;680\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-47\&quot; value=\&quot;随机抽样\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;126.58999999999989\&quot; y=\&quot;350\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-48\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;7.7w(5.4w)&amp;lt;/font&amp;gt;指令数据集&amp;lt;br&amp;gt;①Web交互数据&amp;lt;br&amp;gt;②API调用抽样\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;29.99999999999993\&quot; y=\&quot;420\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-58\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-49\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-65\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;171.59\&quot; y=\&quot;260\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;126.59\&quot; y=\&quot;370\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-49\&quot; value=\&quot;领域指令集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;32.99999999999999\&quot; y=\&quot;340\&quot; width=\&quot;68.59\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-50\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;1.3w&amp;lt;/font&amp;gt;(12725)&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;&amp;lt;br&amp;gt;&amp;lt;/font&amp;gt;指令数据集\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;228.66999999999993\&quot; y=\&quot;170\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-51\&quot; value=\&quot;奖励数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e3c800;strokeColor=#B09500;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;191.59\&quot; y=\&quot;285\&quot; width=\&quot;78.59\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-52\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-4\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-53\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;432.96\&quot; y=\&quot;140\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;282.96\&quot; y=\&quot;210\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;533.96\&quot; y=\&quot;230\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-53\&quot; value=\&quot;生成数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e3c800;strokeColor=#B09500;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;191.59\&quot; y=\&quot;200\&quot; width=\&quot;78.59\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-54\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.9;entryY=0.017;entryDx=0;entryDy=0;exitPerimeter=0;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-53\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-65\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;543.96\&quot; y=\&quot;155\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;279.96\&quot; y=\&quot;220\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-72\&quot; value=\&quot;排序\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;F3d31tewUV45YqQRhXuj-54\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.2236\&quot; y=\&quot;-2\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-55\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff0080&amp;quot;&amp;gt;3.3w&amp;lt;/font&amp;gt;&amp;lt;font&amp;gt;（33207）&amp;lt;/font&amp;gt;数据集(每个prompt k个回答)&amp;lt;br&amp;gt;&amp;amp;lt;prompt, response_k&amp;amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#990000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;401.58999999999986\&quot; y=\&quot;228\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-56\&quot; value=\&quot;PPO数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;191.59\&quot; y=\&quot;415\&quot; width=\&quot;78.59\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-57\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;3.1w&amp;lt;/font&amp;gt;(31144)&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;&amp;lt;br&amp;gt;&amp;lt;/font&amp;gt;指令数据集\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;228.66999999999993\&quot; y=\&quot;490\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-59\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-49\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-56\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;111.59\&quot; y=\&quot;315\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;162.59\&quot; y=\&quot;140\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;125.59\&quot; y=\&quot;370\&quot; /&gt;\n              &lt;mxPoint x=\&quot;125.59\&quot; y=\&quot;445\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-60\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;10w+ &amp;lt;/font&amp;gt;&amp;lt;font color=&amp;quot;#1a1a1a&amp;quot;&amp;gt;Pair wise句子对&amp;lt;/font&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;232.9599999999999\&quot; y=\&quot;350\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-62\&quot; value=\&quot;标注人员&amp;lt;br&amp;gt;（肯尼亚40人）\&quot; style=\&quot;shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;65.74000000000001\&quot; y=\&quot;236\&quot; width=\&quot;20.71\&quot; height=\&quot;39\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-65\&quot; value=\&quot;人工标注\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=15;fontColor=#333333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;91.59\&quot; y=\&quot;245\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-66\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-65\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;111.59\&quot; y=\&quot;315\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;136.59\&quot; y=\&quot;220\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;126.59\&quot; y=\&quot;130\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-70\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.75;exitDx=0;exitDy=0;entryX=0.145;entryY=0;entryDx=0;entryDy=4.35;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-65\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-51\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;201.59\&quot; y=\&quot;240\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;171.59\&quot; y=\&quot;255\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-76\&quot; value=\&quot;扩展10倍\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;F3d31tewUV45YqQRhXuj-70\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.286\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-71\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=1;entryDx=0;entryDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-56\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;171.59\&quot; y=\&quot;278\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;212.59\&quot; y=\&quot;299\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-73\&quot; value=\&quot;【2023-6-19】&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;680\&quot; y=\&quot;765\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-75\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; source=\&quot;8uepeCEjrUpFVLacf4Ny-4\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;534.5999999999999\&quot; y=\&quot;90\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-77\&quot; value=\&quot;&amp;amp;lt;prompt,response&amp;amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#990000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;126.58999999999989\&quot; y=\&quot;190\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-78\&quot; value=\&quot;&amp;amp;lt;prompt&amp;amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#990000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;65.73999999999988\&quot; y=\&quot;445\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-3\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;wbKAMCayHeomiqqS6bZy-1\&quot; target=\&quot;wbKAMCayHeomiqqS6bZy-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-1\&quot; value=\&quot;预训练数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;30\&quot; y=\&quot;510\&quot; width=\&quot;77\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-5\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;wbKAMCayHeomiqqS6bZy-2\&quot; target=\&quot;wbKAMCayHeomiqqS6bZy-6\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-2\&quot; value=\&quot;LLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FF6666;strokeColor=#6F0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;146.66999999999996\&quot; y=\&quot;520\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-4\&quot; value=\&quot;CE Loss\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#a0522d;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;142.87\&quot; y=\&quot;630\&quot; width=\&quot;88.38\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-8\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;wbKAMCayHeomiqqS6bZy-6\&quot; target=\&quot;wbKAMCayHeomiqqS6bZy-4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-6\&quot; value=\&quot;log-probs\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#E6E6E6;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;146.66999999999996\&quot; y=\&quot;570\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-9\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;wbKAMCayHeomiqqS6bZy-4\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-44\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;443\&quot; y=\&quot;670\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;522\&quot; y=\&quot;720\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;187\&quot; y=\&quot;720\&quot; /&gt;\n              &lt;mxPoint x=\&quot;285\&quot; y=\&quot;720\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-10\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-44\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;410\&quot; y=\&quot;760\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;532\&quot; y=\&quot;730\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;285\&quot; y=\&quot;720\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-11\&quot; value=\&quot;Lvalue = r(xy,y) = E[log(r(x,yi)-r(x,y1-i))]\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC0000;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;770\&quot; y=\&quot;620.0000799996801\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-12\&quot; value=\&quot;L =&amp;amp;nbsp; Lvalue &amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;- β&amp;lt;/font&amp;gt;Lppo\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC0000;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;511.96000000000004\&quot; y=\&quot;750.0000799996801\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-13\&quot; value=\&quot;L = Lvalue &amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;- β&amp;lt;/font&amp;gt;Lppo&amp;amp;nbsp; + &amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;γ&amp;lt;/font&amp;gt; Lptx\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC0000;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;290.00000000000006\&quot; y=\&quot;800.0000799996801\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-14\&quot; value=\&quot;Lppo = log[ π^rl(y|x) / π^sft(y|x) ]\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC0000;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;526.02\&quot; y=\&quot;660.0000799996801\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-15\&quot; value=\&quot;Lptx = E[log π^rl(x)]\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC0000;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;238.38000000000005\&quot; y=\&quot;700.0000799996801\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;4\&quot; y=\&quot;-2\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-17\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-24\&quot; target=\&quot;wbKAMCayHeomiqqS6bZy-16\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;792\&quot; y=\&quot;350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;870\&quot; y=\&quot;560\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-18\&quot; value=\&quot;初始化\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; parent=\&quot;wbKAMCayHeomiqqS6bZy-17\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.4091\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-16\&quot; value=\&quot;Reward\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FF6666;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;756.96\&quot; y=\&quot;570\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-19\&quot; value=\&quot;Critic Model\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#1A1A1A;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;798.2600000000002\&quot; y=\&quot;610\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-20\&quot; value=\&quot;目标：得分高 + 与SFT差异小\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510.1799999999999\&quot; y=\&quot;770\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-21\&quot; value=\&quot;SFT模型冻结\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;801.96\&quot; y=\&quot;511\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-428\&quot; y=\&quot;-68\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-22\&quot; value=\&quot;目标：得分高 + 与SFT差异小 + 预训练差异小\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;304.30999999999983\&quot; y=\&quot;817\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-23\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;strokeWidth=2;fillColor=#f8cecc;strokeColor=#b85450;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; target=\&quot;wbKAMCayHeomiqqS6bZy-16\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;640\&quot; y=\&quot;725\&quot; /&gt;\n              &lt;mxPoint x=\&quot;640\&quot; y=\&quot;585\&quot; /&gt;\n            &lt;/Array&gt;\n            &lt;mxPoint x=\&quot;537\&quot; y=\&quot;495\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;563\&quot; y=\&quot;735\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-4\&quot; value=\&quot;GPT-3\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=14;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;498.44\&quot; y=\&quot;60\&quot; width=\&quot;71.04\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-8\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;8uepeCEjrUpFVLacf4Ny-5\&quot; target=\&quot;8uepeCEjrUpFVLacf4Ny-7\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-9\&quot; value=\&quot;对话语料微调\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;8uepeCEjrUpFVLacf4Ny-8\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.082\&quot; y=\&quot;4\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1\&quot; y=\&quot;-4\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-5\&quot; value=\&quot;InsructGPT\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=14;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;245\&quot; y=\&quot;840\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-7\&quot; value=\&quot;ChatGPT\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=14;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;427.4\&quot; y=\&quot;840\&quot; width=\&quot;71.04\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

### 优化

**全参数**微调：对模型所有参数进行调整，如：SFT
- 问题：代价大（模型大、数据多、参数量大）

**混合精度**微调：<span style='color:red'>省显存、加速，但丢失精度</span>
- 训练时同时使用**16位**、**32位浮**点类型，加速，减少内存开销
- 部分参数使用**32位**类型，以保持数值稳定性，缩短单步用时
- 现代加速器使用16位专用硬件执行运算，速度更快

注意
- FP16: 内存存储、乘法运算
- FP32: 累加运算，避免下溢
- 手动放大梯度，以避免梯度爆炸，这样 FP16和FP32运算时，不容易出现下溢

其它加速方法
- **多卡**并行：数据并行、模型并行
- `ZeRO`：分布式机器学习的新型内存优化技术，将三个步骤（optimizer state partitioning/add gradient partitioning/add parameter partitioning）拆分到不同的卡上，相比 数据并行，节省GPU
- `p-tuning`：通过prompt encoder结构将prompt编码为向量，再与input embedding拼接。增加模型理解能力
- `LoRA`：低秩适配，冻结大模型权重，只训练新增的网络层（两个小矩阵的乘积），降低fine-tune成本，同时保持类似效果


### (0) Pre-Train


#### 问题

【2024-7-28】[面试LLM//各阶段](https://zhuanlan.zhihu.com/p/691588703?utm_psn=1801229804424544256)

##### CLS token

预训练阶段：
- 模型训练句子时, 没有加 `<CLS>` Token，但是预测时加了`<CLS>` Token
- 或者训练时加了`<CLS>` token, 但是预测时没有加`<CLS>` Token

benchmark 预测会有啥问题？

benchmark会直接崩溃，之前gemma-2b训的时候带BOS，预测忘加了，benchmark全崩了。

原因
- 一个句子的第一个Token在模型中会吸收大量attention，那么当预测时改变了第一个Token，句子的预测会改变比较大，因为第一个Token改变了，而预测中大量attention来自第一个Token，所以预测的时候大量benchmark效果会不好。

##### 三个阶段训练（SFT->RM->PPO）过程较长，更新迭代较慢？

考虑以下几种方法：
- 并行化训练：利用多个计算资源进行并行化训练，可以加速整个训练过程。可以通过使用多个CPU核心或GPU来并行处理不同的训练任务，从而提高训练的效率和速度。
- 分布式训练：将训练任务分发到多台机器或多个节点上进行分布式训练。通过将模型和数据分布在多个节点上，并进行并行计算和通信，可以加快训练的速度和更新的迭代。
- 优化算法改进：针对每个阶段的训练过程，可以考虑改进优化算法来加速更新迭代。例如，在SFT（Supervised Fine-Tuning）阶段，可以使用更高效的优化算法，如自适应学习率方法（Adaptive Learning Rate）或者剪枝技术来减少模型参数；在RM（Reward Modeling）阶段，可以使用更快速的模型训练算法，如快速梯度法（Fast Gradient Method）等；在PPO（Proximal Policy Optimization）阶段，可以考虑使用更高效的采样和优化方法，如并行采样、多步采样等。
- 迁移学习和预训练：利用迁移学习和预训练技术，可以利用已有的模型或数据进行初始化或预训练，从而加速训练过程。通过将已有模型的参数或特征迁移到目标模型中，可以减少目标模型的训练时间和样本需求。
- 参数调优和超参数搜索：对于每个阶段的训练过程，可以进行参数调优和超参数搜索，以找到更好的参数设置和配置。通过系统地尝试不同的参数组合和算法设定，可以找到更快速和高效的训练方式。

综合运用上述方法，可以加速三个阶段训练过程，提高更新迭代的速度和效率，从而减少训练时间和资源消耗。




### （1） 第一步 SFT（全参数微调）

SFT 原理比较简单，难的是数据问题，需要大量的有监督Prompt文本
- ![img](https://pic3.zhimg.com/80/v2-45331e791fad76d81694bd61e806db8a_1440w.webp)
- Transformer【左】GPT【右】

大模型训练**基座模型**时，都采用「Next Token Prediction，`NTP`」 任务


【2024-5-31】sft分为两种，**拟合**和**对齐**。
- **拟合**：通过finetuning 得到稳定、符合需求的输出，包括格式、风格、特定模式等，是在业务落地中高频使用的方式；
- **对齐**：指令对齐，让LLM更好地理解人类语言、执行自然语言指令，即LLM三个阶段之第二个阶段（pretrain、sft、rlhf）。

#### loss 改进

【2024-9-24】[SFT loss 计算的那些坑（多轮合并/packing）](https://zhuanlan.zhihu.com/p/721652210)

SFT 训练时, 直接输入 `(input_ids, label)`, 训练效率低。 

通常有两个加速方法：
1. **多轮合并**: 同一个会话的拆分、合并
  - user 和 bot 交互了 3 轮, 数据格式: bot作答部分用 input_ids, 其余用 **-100** 表示
    - (system, user1, `bot1`, pad), bot1 计算loss
    - (system, user1, bot1, user2, `bot2`, pad), bot2 计算loss
    - (system, user1, bot1, user2, bot2, user3, `bot3`), bot3 计算loss
  - loss 表达式: `loss = 1/3 (l1/n1+l2/n2+l3/n3)`, ni 是 boti token数, li 是第i个样本的 loss
  - 不同样本之间有很多重复计算的前缀, 训练偏慢
1. 加速
  - 将3个样本合成1个, 借助 causal attention mask，每个 token 只能看到前面的 token，计算上和之前是等价
  - 数据格式: (system, user1, `bot1`, user2, `bot2`, user3, `bot3`), 对应权重 li/ni
  - 问题: loss 计算有问题, pytorch `CrossEntropyLoss` 默认取均值 mean, `loss = (l1+l2+l3)/(n1+n2+n3)`, 而 ni 不一定相同, 导致 短句子权重被降低, 长句子被加权, loss 不等价
1. **packing**: 将**多个会话**合成一条, 进一步加速
  - 将所有样本拼接成1条，并加入 `attention mask`, 保证后面的样本看不见前面的token。如 在 flash attention 中调用 flash_attn_varlen_qkvpacked_func，并传入 cu_seqlens 参数。
  - 和之前一样，如果不修改 loss 计算方法，packing 的样本之间会存在因为长度不同，导致训练不充分的问题。

loss 计算会经历三次平均
- micro batch 维度，分母是这个 micro batch 中的所有 label 不是 -100 的 token 数
- DP 维度，分母是 DP size （和GPU数量相关）
- 梯度累加维度，分母是梯度累加数

禁用这三个平均，统一用 `global batch` 对话轮数作为分母。
- 新版 megatron 框架中，开启开关 `--calculate-per-token-loss`, 即可禁用 DP 和梯度累加的平均
- 然后 修改 `loss_func`，每个 `micro batch` 都需要返回这个 `micro batch` 的轮数
- 最后 框架会自动将所有轮数求和，作为分母。对于分子，需要除以这个轮次的token 数。

正确实现代码如下（loss_token_num, turn_num 是在构建 data 的时候构建的）：

```py
def loss_func(output_tensor, loss_mask, loss_token_num, turn_num):
    losses = output_tensor.view(-1).float()
    loss_mask = loss_mask.view(-1).float()
    loss_token_num = loss_token_num.view(-1).float()
    # label: [-100, -100, a, a, a, -100, b, b, -100, -100, c, c, c, -100, -100]
    # loss_mask: [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0]
    # losses: [a0, a1, a2, a3, a4, b0, b1, b2, c0, c1, c2, c3, c4, d0, d1]
    # losses * loss_mask = [0, 0, a2, a3, a4, 0, b1, b2, 0, 0, c2, c3, c4, 0, 0]
    # loss_token_num: [3, 3, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 1, 1]
    # losses * loss_mask / loss_token_num = [0, 0, a2/3, a3/3, a4/3, 0, b1/2, b2/2, 0, 0, c2/3, c3/3, c4/3, 0, 0]
    # sum = 1/3 (a2 + a3 + a4) + 1/2 (b1 + b2) + 1/3 (c2 + c3 + c4)
    loss = torch.sum(losses * loss_mask / loss_token_num)

    loss_and_turn_num = torch.cat([loss.view(1), turn_num.view(1)])
    # Reduce loss for logging.
    loss_and_turn_num = loss_and_turn_num.clone().detach()
    torch.distributed.all_reduce(loss_and_turn_num, group=mpu.get_data_parallel_group())
    # 新版返回结构，开启 calculate_per_token_loss 开关后，返回三个值
    # 第一个是反向传播实际使用的 loss, 所有 packing 的 loss 求和
    # 第二个是 turn_num, 优化器状态更新时会使用对这个值求和然后缩放梯度
    # 第三个是用于日志打印的 loss, 包含两个值，第一个是所有 loss 求和作为分子，第二个是所有 turn_num 求和作为分母
    return loss, turn_num, {"lm loss": (loss_and_turn_num[0], loss_and_turn_num[1])}
```

无论是哪种方法，加速后都需要保证 loss 和原来等价。

加速注意：
- 不同样本之间等价；
- 不同轮次之间等价。

合并多轮 / packing 时，要修改 loss 计算方法，为每个 token 设置正确权重，并且关闭 `DP` / `梯度累加`的平均。


#### IFT 问题

5 月，伯克利的论文 The False Promise of Imitating Proprietary LLMs 指出这种方式微调出来的**指令遵循**模型存在的一系列问题：
- 在缺少大量模仿 ChatGPT 数据支持的任务上，这类模型无法改善 Base Model 到 ChatGPT 的差距；
- 这类模型只是擅长模仿 ChatGPT 的风格，而不是事实性，导致实际的性能差异会骗过人类评估者；
- 当前开源模型最大的限制仍然是 Base Model 层面跟 GPT 系列的差距，在微调而不是预训练环境进行优化可能是不正确的方向；
- 为了广泛地匹配 ChatGPT 支持的任务，需要更广泛和大量的模仿数据集，还需要新的工作；

而 6 月份 Allen Institute for AI 和华盛顿大学的 How Far Can Camels GO ？工作再次通过实验表明不同的指令微调数据集可以释放或者增强特定的能力，但并没有一个数据集或者组合可以在所有的评估中提供最佳性能，并且这一点在人类或模型担任评估者时也很容易无法被揭示。

对于指令遵循微调背后的团队来说，他们也意识到自己的模型由于 Base Model（LLaMA）的限制，在复杂推理和代码任务上很弱，并且难以进入正向数据飞轮 —— 模型能力越弱的领域越难得到更多的 query，也就难以筛选出高质量 query，想自己再标注提升模型能力就很困难。

至此，开源社区已经充分意识到原来这套微调 LLaMA 的框架的局限性，越来越多的团队开始探索预训练环节和更接近真实的人类反馈数据

#### 数据示例

数据准备

| Raw Data	| Prompt	| Label |
|---|---|---|
| 我们去成都旅游，必须要去的地方是大熊猫繁殖基地。 |	大熊猫是 |	一种有黑白斑纹的动物。|
| 我们去成都旅游，必须要去的地方是大熊猫繁殖基地。 |	大熊猫是 |	中国特有种，主要栖息地是中国四川、陕西和甘肃的山区。|
| 我们去成都旅游，必须要去的地方是大熊猫繁殖基地。 |	大熊猫是 |	已在地球上生存了至少800万年，被誉为“活化石”和“中国国宝”即国兽，世界自然基金会的形象大使，是世界生物多样性保护的旗舰物种。|
| 我们去成都旅游，必须要去的地方是大熊猫繁殖基地。 |	大熊猫是 |	属于熊科、大熊猫属的哺乳动物。仅有二个亚种。雄性个体稍大于雌性。体型肥硕似熊、丰腴富态，头圆尾短，头躯长1.2-1.8米，尾长10-12厘米。|

```py
raw_data = "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。"
prompt = "大熊猫是"
labels = ["一种有黑白斑纹的动物。","中国特有种，主要栖息地是中国四川、陕西和甘肃的山区。",
"已在地球上生存了至少800万年，被誉为“活化石”和“中国国宝”即国兽，世界自然基金会的形象大使，是世界生物多样性保护的旗舰物种。",
"属于熊科、大熊猫属的哺乳动物。仅有二个亚种。雄性个体稍大于雌性。体型肥硕似熊、丰腴富态，头圆尾短，头躯长1.2-1.8米，尾长10-12厘米。"]
combine_data = [raw_data+prompt+label for label in labels]
```

初始化模型，对输入数据进行编码, 以 [GPT-2](https://huggingface.co/uer/gpt2-chinese-cluecorpussmall) 模型为例


```py
from torch.utils.data import Dataset
from transformers import Trainer, TrainingArguments
from transformers import AutoTokenizer, AutoModelForCausalLM
# 模型加载
tokenizer = BloomTokenizerFast.from_pretrained('pre_train_model/gpt2')
model = BloomForCausalLM.from_pretrained('pre_train_model/gpt2')
# 自定义DataSet类
class Datasets(Dataset):
    def __init__(self, sample):
        super(Datasets, self).__init__()
        self.sample = sample

    def __getitem__(self, item):
        res = {k: v[item] for k, v in self.sample.items()}
        return res

    def __len__(self):
        return len(self.sample['labels'])
# 数据转换
combine_data_token = tokenizer.batch_encode_plus(
    initial_data_,
    max_length=256,
    padding='max_length',
    truncation=True,
    return_tensors='pt'
)
# 将标签标签加入
combine_data_token['labels'] = combine_data_token['input_ids']
combine_data_token['labels'] = torch.where(
    combine_data_token['labels']==0,
    -100,
    combine_data_token['labels']
)
# 模型训练保存
trainer_args = TrainingArguments("./model/", learning_rate=2e-5, weight_decay=0.01, num_train_epochs=10, auto_find_batch_size=True)
trainer = Trainer(model=initial_model, args=trainer_args, train_dataset=Datasets(initial_token_info))
trainer.train()
trainer.save_model()
# ----- 加载生成 --------
# 加载模型
model = AutoModelForCausalLM.from_pretrained('./model')
# 处理输入数据
input_data = raw_input + prompt
input_datas = tokenizer.encode_plus(
    input_data,
    return_tensors='pt'
)
input_ids = input_datas['input_ids']
# 模型生成
result = model.generate(
    input_ids=input_ids,
    max_length=256,
    do_sample=True,  # 增加随机性
    num_beams=5,
    num_return_sequences=5,  # 每个样本生成5个结果
    no_repeat_ngram_size=3,  # 防止重复的token
    early_stopping=True  # 提前停止
)

decode_tokens = tokenizer.batch_decode(
    result,
    skip_special_tokens=True
)

results = [i.replace(' ', '') for i in decode_tokens]

print("results",results)
```


结果：


```s
我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是今世界上保存最完好的哺乳动物之一，也是世界自然保护联盟濒危物种红色名录的保护对象之一。在这里，你可以看到全世界最大的熊猫栖息地成都。成都是中国国家林业局直属的国家重点风景名胜区，是国家森林公园、国家湿地公园和国家地质公园的重要组成部分，是全国重点文物保护单位、全国生态文明建设示范区、中国红色旅游名城、国际生态旅游目的地和国际旅游岛建设先进区。地址：四川省成都市绵阳市成华区成都高新技术产业开发区成华大道1号乘车路线：成都绵阳都江堰雅
我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家二级保护动物，是世界上保存最完整的动物种群之一，也是我国第一个国家级自然保护区。我们是四川省的首批国家重点保护野生动物和珍稀动物基金会的成员，被誉为中国动物保护的摇篮和世界生物多样性保护基地，被中国科学院、中华人民共和国国家林业局授予全国生态文明建设示范区称号，被国务院批准为国家森林城市、国际生态旅游目的地。熊猫基地位于成都市双流区东南部，是国家aaaa级旅游景区，国家地理标志保护单位。熊猫栖息地为亚热带或热带的高山
我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完好的熊猫种群之一。它们栖息在亚热带或热带的高海拔草原上，生活环境十分优越，是中国四大自然奇观之一，被誉为世界自然遗产和中国国家森林公园。熊猫栖息地主要分布在中国大陆的西藏、青海、甘肃、宁夏、新疆、内蒙古、山西、辽宁、吉林、黑龙江、江苏、河南、安徽、湖北、湖南、江西、广东、海南、四川、云南、贵州、陕西等地。中国熊猫研究中心主任、中国科学院院士、国家自然科学基金委员会委员、中华全国工商业联合会副主席
我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完整、规模最大的野生动物种类繁多的地区之一，是中国国家重点保护的珍稀濒危动物及其栖息地和世界自然遗产的重要组成部分，被誉为中国最美丽的城市和世界生物多样性保护基地，被国际旅游组织评为全球生态旅游目的地。成都熊猫国家公园位于四川省甘孜藏族自治州，是国家aaaa级旅游景区，被《世界遗产名录》列为全国重点文物保护单位。目前，我国已建成国家森林公园、国家湿地公园和国家地质公园，国家林业局、国务院扶贫
我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是现存最大、保存最完整的动物，属于国家二级保护动物。熊猫种类繁多，分布广泛，主要分布在四川、云南、陕西、甘肃、宁夏、内蒙古、新疆、青海、吉林、辽宁、黑龙江、山西、江苏、江西、河南、湖北、湖南、广东、广西、海南、重庆、贵州、西藏、四川等省区市。它们的栖息地主要为亚热带或热带的（低地）湿润低地林、亚高山草原、高山湖泊、高原湿润山区和高原沼泽地等，常栖息在高海拔地区。在中国大陆，熊猫分布于四川省甘孜藏族自治州和青海省西宁市等地。雄性熊猫体长约1.5米
```

这和instructGPT的SFT过程大致相同，思路原理是一样的，差别是 缺乏硬件设备、大规模高质量监督数据
- ChatGPT原理详解+实操: [SFT(GPT模型精调)](https://zhuanlan.zhihu.com/p/609795142), [RM(reward model)](https://zhuanlan.zhihu.com/p/610147705)

引入RM模型的作用是对生成的文本进行打分排序，让模型生成的结果更加符合人类的日常理解习惯，更加符合人们想要的答案。RM模型主要分为两个部分：训练数据获取和模型训练部分。流程如下图所示

#### Bloom SFT

【2023-5-23】[bloom_tuning: BLOOM 模型的指令微调](https://mp.weixin.qq.com/s/f369M-BKI6-MYb0nqvYFNQ)
- Github: [bloom_tuning](https://github.com/zejunwang1/bloom_tuning)
- 模型: [bloom-396m-chat](https://huggingface.co/WangZeJun/bloom-396m-chat)

BLOOM 系列模型是由数百名研究人员在包含 46 种自然语言和 13 种编程语言的数据集上, 基于大规模分布式训练框架 `Megatron-DeepSpeed` 训练得到。
- 实验发现，BLOOM 在一系列基准测试上取得了具有竞争力的性能，经过**多任务**提示微调后，可以获得更为惊艳的效果。
- BLOOM 模型支持中文、英文、代码、法语、西班牙语。

链接：[bloom-560m](https://huggingface.co/bigscience/bloom-560m)

[LLMPruner](https://github.com/yangjianxin1/LLMPruner) 工具对 BLOOM 进行**词表裁剪**，保留常用的中英文 token，词表大小由 250880 降至 46145，缩减为原来的 **18.39%**，在后续微调过程中可以减少显存占用。
- 词表裁剪后的模型链接：[bloom-396m-zh](https://huggingface.co/YeungNLP/bloom-396m-zh)

##### 数据

训练数据来自于 [BelleGroup/train_3.5M_CN](https://huggingface.co/datasets/BelleGroup/train_3.5M_CN)，该数据集包含 **3.6M** 条指令，从中筛选出单轮对话数据，进行 10:1 采样后得到约 0.25M 指令数据：

```py
python sample_data.py \
--input data/train_3.5M_CN.json \
--output data/train.jsonl \
--sample_ratio 0.1
```

单条指令数据形如：

```json
{
    "instruction": "你好，请问你能做什么？", 
    "output": "你好，我可以回答各种问题，提供辅助，或者与你聊天。有什么我可以帮你的吗？"
}
```

输出部分的长度分布如下图所示（若输出长度超过2048，则设置为2048）

##### 指令微调

基于 deepspeed ZeRO-Stage 2 进行指令微调训练：

```py
deepspeed --include localhost:0 train.py \
--model_name_or_path /path/to/bloom \
--data_path data/train.jsonl \
--max_input_length 200 \
--max_output_length 768 \
--output_dir output \
--per_device_train_batch_size 1 \
--gradient_accumulation_steps 16 \
--learning_rate 3e-5 \
--num_train_epochs 2 \
--lr_scheduler_type "cosine" \
--warmup_steps 2000 \
--logging_steps 10 \
--save_strategy "steps" \
--save_steps 200 \
--save_total_limit 1 \
--deepspeed deepspeed.json \
--fp16 False
```

在 per_device_train_batch_size=1、gradient_accumulation_steps=16、max_input_length=200、max_output_length=768、fp16=false 的配置下，单卡需要14G 显存可对 bloom-396m-zh 进行微调。

##### 推理

微调后的模型已上传至 huggingface: [bloom-396m-chat](https://huggingface.co/WangZeJun/bloom-396m-chat)

可以通过如下代码调用 bloom-396m-chat 模型来生成对话：

```py
from transformers import BloomTokenizerFast, BloomForCausalLM

model_name_or_path = "WangZeJun/bloom-396m-chat"

tokenizer = BloomTokenizerFast.from_pretrained(model_name_or_path)
model = BloomForCausalLM.from_pretrained(model_name_or_path).cuda()
model = model.eval()

input_pattern = "{}</s>"
text = "你好"
input_ids = tokenizer(input_pattern.format(text), return_tensors="pt").input_ids
input_ids = input_ids.cuda()

outputs = model.generate(input_ids, do_sample=True, max_new_tokens=1024, top_p=0.85,
    temperature=0.3, repetition_penalty=1.2, eos_token_id=tokenizer.eos_token_id)

output = tokenizer.decode(outputs[0])
response = output.replace(text, "").replace('</s>', "")
print(response)
```

运行如下命令进行命令行推理：

```py
python chat.py \
--model_name_or_path /path/to/model \
--max_new_tokens 1024 \
--top_p 0.85 \
--temperature 0.3 \
--repetition_penalty 1.2
```

##### 测试

| 用户	| Assistant |
|---|---|
| 你好	| 您好，有什么我可以帮您的吗？ |
| 你是谁	| 我是一个AI语言模型，没有个人身份和情感。我的目的是回答你的问题并提供有用的信息来帮助你解决问题或提供娱乐性内容。如果你有任何其他的问题需要解答，请随时问我！ |


#### SFT 思考


##### SFT packing 是什么

SFT packing 指训练sft过程中，将**多个sft数据pack到一个样本内**进行训练
- 这种方式会加快模型训练速度，如果不进行SFT packing，那么对于短文本sft需要padding到一个batch最长长度，浪费很多计算token。
- SFT packing 有很多种类，比如 block diagonal attention, 每个token仅仅去attention自己的问题内的token。但一般业务中会直接将其相连接，然后进行预测，虽然这样会引入一些噪音，但好像相对于非sft packing方式的整体的效果损失不大。这个可能是因为pretrain的时候模型也是这么训练的。

##### SFT packing 对SFT训练的影响

SFT packing 后削弱了模型对难的短query和短答案的拟合。
- 无sft packing 情况下，假设batch_size = 1，那么如果有个短query和短答案在这个batch里，其余补充padding，那么这个batch的gradient全是这个短文本的gradient，模型对这个query的拟合能力会变强。
- 但SFT packing 后，多个短文本在一个样本中，这个batch的gradient会被稀释，短文本的拟合就不会特别强。但拟合能力似乎和泛化不可以挂钩，初步观察sft packing和non sft packing的效果差不了很多。在数据量小或者特定困难的数据上，sft packing是有损泛化效果的，non-packing的方式会影响模型续写的效果，因此会影响一些benchmark效果。但在大批量数据上是无损泛化效果的。

##### SFT 关注什么方面

- 1 **根据 prompt 筛选sft数据**：Prompt的diversity：丰富多样的prompt数据可以让模型更多的了解人类的指令，包括指令指复杂指令中每一步的含义。Prompt的丰富程度决定了模型指令遵循的能力。
  - 明文TAG法：对SFT的prompt进行打tag，对其中的名词和动词进行分类打标，最后通过tag对prompt的分布进行调整，保证tag的分布是均匀的。著名的就是InsTag这个方法。
  - 模型embedding聚类方法：通过模型最后一层的embedding对prompt进行表示，那么通过prompt embedding的距离表示prompt的相似度，对于过于相似的prompt进行删除。著名的有Self-Evolved Diverse Data Sampling for Efficient Instruction Tuning。
  - 从complexity角度，对于prompt直接进行难度的升级，所以即使在同一个语意空间的prompt也会变得diverse。比较著名的是Wizard 方法，通过GPT4进行prompt难度升级，然后构成complexity丰富的prompt。
- 2 利用sft model和pretrain model的关系筛选模型的sft数据：
  - IFD方法：利用公式进行数据选择： 这个公式是计算pretrain model生成对齐后模型的answer的难度（在 prompt的condition 下生成A的概率）。这个概率越低，越说明生成难度高，那么sft模型学习到的对齐规律越多，那么我们更应该选择这个sft数据。
  - Hybrid Method （混合了多种之前列举的指标和方法。）：例如 What MakeGood Data for Alignment? A Comprehensive Study of Automatic Data Selectionin Instruction Tuning [2] 文章，从complexity，diversity和quality三个方向对sft数据建模，训练了多个模型对各个指标维度进行分别衡量。
- 3 **Answer的质量**：Answer的质量包括内容和格式两方面，一方面内容的正确性需要得到保证，一方面内容的格式也很重要，细节丰富，逻辑缜密的answer可以激发模型更多的回答能力。
- 4 SFT阶段**不能太多的知识注入**：过多的知识注入，或者超过模型能力本身的回答过多会导致对齐税。

##### 提升模型 reasoning 能力

什么数据格式在SFT或者ICL阶段可以提升模型的reasoning的能力？

数学reasoning上是有**三种形式**可显著提高效果模型 reasoning 能力
- **Reverse** ： 128 + 367 = 495 -> 128 + 367 = ^594, 因为人就是反着计算的，从个位数到百位数。
- `COT` or `POT` (Simplified Scratchpad): 把这个计算过程列举下来，用自然语言、符号或者代码形式呈现。
- **Detailed Scratchpad**：把整个思考过程详细地用自然语言和符号表达出来。
  - 整体上Detailed Scratchpad需要的总条数最少就能达到100%在加法上的效果，但是其实总token数和plain需要差不多数量达到最好的效果。

##### SFT 中代码数据+文本数据, 哪个更容易改变

代码数据，因为
- 预训练中, 代码数据**确定性更高，ppl更低**，记忆越深刻
- 而**文本数据变化更大，ppl更高**，熵更高。

SFT过程中，改变文本数据比较容易，因为本身ppl就会高，但代码数据会比较难，因为本身ppl会比较低，或者说代码数据的生成确定性更高，少量样本很难对其内部改变，只能大段替换。


##### SFT 能学新知识吗

虽然理论上可以，但很少且不推荐sft阶段去学习知识。
- LIMA原文中就表述过同样一个假设，sft阶段更多是**将模型能力和人类对齐，而不过多学习新的知识**。

原因如下：
- sft相对于pretrain过的数据量实在太小，模型的知识学习的概率就很低。
- 如果加大sft的数据量和pretrain数据相当，那么sft有一些特定的格式以及一些system prompt需要重复当作context进行attention，这些重复的context势必会影响模型原始的attention模式，从而影响模型的效果。
- 最后, 如果希望sft学习新知识，不如把这部分sft的新知识组织好放入pre-train or post-train阶段更为合适。


### （2）第二步 RM训练


**奖励模型**（Reward Model, RM）目标是刻画模型的输出是否在人类看来表现不错。
- 输入: \[提示(prompt)，模型生成的文本\] 
- 输出: 一个刻画文本质量的标量数字。
- ![](https://pic2.zhimg.com/80/v2-51ad9f0f11ba272611a068d380e7fe41_1440w.webp)

同一个prompt输出的多个答案，人工评测排序后，使用lambdarank的思想，优化RM奖励模型。

RM模型学习的是对于一个prompt，人类对答案的喜好程度。
- RM模型【左】RM损失函数【右】
- ![](https://pic3.zhimg.com/80/v2-6b22d510b56efc300b6bb1686407a40e_1440w.webp)
- ![rm](https://pic1.zhimg.com/v2-bc1af700e9147ae7458824f5619b1ed4_b.jpg)

奖励模型接收一系列文本并返回一个标量奖励，数值上对应人的偏好

引入RM模型的作用是对生成的文本进行打分排序，让模型生成的结果更加符合人类的日常理解习惯，更加符合人们想要的答案。

RM模型主要分为两个部分：**数据获取**和**模型训练**。流程如下图所示
- ![](https://pic2.zhimg.com/80/v2-ac62759c2862ab04a024d51fe2a19991_1440w.webp)

原论文中使用GPT架构做了一个reward model

注意
- 要将模型的输出映射成维度为1的**打分向量**，即增加一个linear结构。

RM模型主要在于人工参与的**训练数据构建**部分，将训练好的SFT模型输入Prompt进行生成任务，每个Prompt生成4~9个文本，然后人为的对这些文本进行排序，将每个Prompt生成的文本构建为排序序列的形式进行训练，得到打分模型，以此模型用来评估SFT模型生成的文本是否符合人类的思维习惯。

两种方法命名为 direct score 和 rank score：
- `Direct score`：直接对输出的文本进行打分，通过与自定义的label score计算loss，以此来更新模型参数；
- `Rank score`：用排序方法对每个Prompt输出的n个句子进行排序作为输入，通过计算排序在前面的句子与排序在后面的句子的差值累加作为最终loss。

【2023-6-5】[ChatGPT 为什么不用 Reward-Model 的数据直接 fine-tune，而用 RL？](https://www.zhihu.com/question/596230048/answer/3055888005)
- Reward-model的输出对于整个token序列，一种滞后反馈，而finetune需要在每个token都有监督信号。这是强化学习与监督学习的差别。
- 生成Reward-model的数据有些是结果对比较**pair数据**，没法直接用于监督学习finetune。


#### ① Direct score方法

① Direct score方法
- 利用 Bert模型对标注数据进行编码，用 linear层 映射到1维，然后用 Sigmoid函数输出每个句子的得分，与人工标记的得分进行loss计算，以此来更新模型参数。流程如下所示
- ![](https://pic1.zhimg.com/80/v2-c040a19b5054a8b6076a4f4e1506b784_1440w.webp)

数据为SFT最后所生成的数据，数据准备：

```py
def data_prepare(pretrain_path):
    data_lst = [
        "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是今世界上保存最完好的哺乳动物之一，也是世界自然保护联盟濒危物种红色名录的保护对象之一。在这里，你可以看到全世界最大的熊猫栖息地成都。成都是中国国家林业局直属的国家重点风景名胜区，是国家森林公园、国家湿地公园和国家地质公园的重要组成部分，是全国重点文物保护单位、全国生态文明建设示范区、中国红色旅游名城、国际生态旅游目的地和国际旅游岛建设先进区。地址：四川省成都市绵阳市成华区成都高新技术产业开发区成华大道1号乘车路线：成都绵阳都江堰雅",
        "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家二级保护动物，是世界上保存最完整的动物种群之一，也是我国第一个国家级自然保护区。我们是四川省的首批国家重点保护野生动物和珍稀动物基金会的成员，被誉为中国动物保护的摇篮和世界生物多样性保护基地，被中国科学院、中华人民共和国国家林业局授予全国生态文明建设示范区称号，被国务院批准为国家森林城市、国际生态旅游目的地。熊猫基地位于成都市双流区东南部，是国家aaaa级旅游景区，国家地理标志保护单位。熊猫栖息地为亚热带或热带的高山",
        "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完好的熊猫种群之一。它们栖息在亚热带或热带的高海拔草原上，生活环境十分优越，是中国四大自然奇观之一，被誉为世界自然遗产和中国国家森林公园。熊猫栖息地主要分布在中国大陆的西藏、青海、甘肃、宁夏、新疆、内蒙古、山西、辽宁、吉林、黑龙江、江苏、河南、安徽、湖北、湖南、江西、广东、海南、四川、云南、贵州、陕西等地。中国熊猫研究中心主任、中国科学院院士、国家自然科学基金委员会委员、中华全国工商业联合会副主席",
        "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完整、规模最大的野生动物种类繁多的地区之一，是中国国家重点保护的珍稀濒危动物及其栖息地和世界自然遗产的重要组成部分，被誉为中国最美丽的城市和世界生物多样性保护基地，被国际旅游组织评为全球生态旅游目的地。成都熊猫国家公园位于四川省甘孜藏族自治州，是国家aaaa级旅游景区，被《世界遗产名录》列为全国重点文物保护单位。目前，我国已建成国家森林公园、国家湿地公园和国家地质公园，国家林业局、国务院扶贫",
        "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是现存最大、保存最完整的动物，属于国家二级保护动物。熊猫种类繁多，分布广泛，主要分布在四川、云南、陕西、甘肃、宁夏、内蒙古、新疆、青海、吉林、辽宁、黑龙江、山西、江苏、江西、河南、湖北、湖南、广东、广西、海南、重庆、贵州、西藏、四川等省区市。它们的栖息地主要为亚热带或热带的（低地）湿润低地林、亚高山草原、高山湖泊、高原湿润山区和高原沼泽地等，常栖息在高海拔地区。在中国大陆，熊猫分布于四川省甘孜藏族自治州和青海省西宁市等地。雄性熊猫体长约1.5米"]
    # 自定义打分标签，每个句子一个分值。也可以定义多维度的打分方法，只是模型的线性层需要改为你所定义的维度数
    direct_score = [[0.75], [0.5], [0.35], [0.4], [0.8]]
    tokenizer = BertTokenizer.from_pretrained(pretrain_path)
    train_data = tokenizer.batch_encode_plus(data_lst, max_length=256, padding="max_length", truncation=True,
                                             return_tensors='pt')
    train_data["labels"] = torch.tensor(direct_score)
    return train_data, tokenizer
```

RM模型搭建
- 采用了Bert模型作为编码模型，后取CLS作为文本表征，采用MSE作为loss函数，最后接linear进行维度压缩

```py
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertModel, BertPreTrainedModel, BertTokenizer, BertConfig, get_scheduler


class RewardModel(BertPreTrainedModel):
    def __init__(self, config):
        super(RewardModel, self).__init__(config)
        self.config = config
        self.sigmoid = nn.Sigmoid()
        self.loss_fn = nn.MSELoss()
        self.model = BertModel(config)
        self.linear = nn.Linear(config.hidden_size, 1)

    def forward(self, input_ids, token_type_ids, attention_mask, labels=None):
        outputs = self.model(input_ids=input_ids, token_type_ids=token_type_ids,
                             attention_mask=attention_mask).pooler_output
        output = self.linear(outputs)
        logits = self.sigmoid(output)
        if labels is not None:
            loss = self.loss_fn(logits, labels)
            return logits, loss
        else:
            return logits
```

训练过程

```py
class Datasets(Dataset):
    def __init__(self, sample):
        super(Datasets, self).__init__()
        self.sample = sample

    def __getitem__(self, item):
        res = {k: v[item] for k, v in self.sample.items()}
        return res

    def __len__(self):
        return len(self.sample['input_ids'])


def train(pretrain_path, save_path):
    config = BertConfig.from_pretrained(pretrain_path)
    model = RewardModel(config=config)

    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": 0.01,
        },
        {
            "params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
    ]
    optimizer = torch.optim.AdamW(optimizer_grouped_parameters, lr=2e-5)
    train_data, tokenizer = data_prepare(pretrain_path)
    dataloader = DataLoader(dataset=Datasets(train_data), shuffle=False, batch_size=1)

    max_train_steps = 10 * len(dataloader)
    warm_steps = int(0.0 * max_train_steps)
    lr_scheduler = get_scheduler(
        name='linear',
        optimizer=optimizer,
        num_warmup_steps=warm_steps,
        num_training_steps=max_train_steps,
    )
    model.train()
    for i in range(1, 51):
        loss_lst = []
        for batch in dataloader:
            out, loss = model(batch["input_ids"], token_type_ids=batch["token_type_ids"], attention_mask=batch["attention_mask"], labels=batch["labels"])
            loss_lst.append(loss.item())
            loss.backward()
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
        print("epoch{}\tloss: {}".format(str(i), str(sum(loss_lst) / len(loss_lst))))
    tokenizer.save_pretrained(save_path)
    model_to_save = model.module if hasattr(model, 'module') else model
    model_to_save.save_pretrained(save_path)
    model_to_save.config.save_pretrained(save_path)
```

模型预测

```py
def predict(model_path):
    text = ["我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是今世界上保存最完好的哺乳动物之一，也是世界自然保护联盟濒危物种红色名录的保护对象之一。在这里，你可以看到全世界最大的熊猫栖息地成都。成都是中国国家林业局直属的国家重点风景名胜区，是国家森林公园、国家湿地公园和国家地质公园的重要组成部分，是全国重点文物保护单位、全国生态文明建设示范区、中国红色旅游名城、国际生态旅游目的地和国际旅游岛建设先进区。地址：四川省成都市绵阳市成华区成都高新技术产业开发区成华大道1号乘车路线：成都绵阳都江堰雅",
            "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家二级保护动物，是世界上保存最完整的动物种群之一，也是我国第一个国家级自然保护区。我们是四川省的首批国家重点保护野生动物和珍稀动物基金会的成员，被誉为中国动物保护的摇篮和世界生物多样性保护基地，被中国科学院、中华人民共和国国家林业局授予全国生态文明建设示范区称号，被国务院批准为国家森林城市、国际生态旅游目的地。熊猫基地位于成都市双流区东南部，是国家aaaa级旅游景区，国家地理标志保护单位。熊猫栖息地为亚热带或热带的高山",]
    model = RewardModel.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)

    model.eval()
    data = tokenizer.batch_encode_plus(text, max_length=256, padding="max_length", truncation=True,
                                           return_tensors='pt')
    score = model(**data)
    return score
```

完成了一个基于Bert的文本打分模型。
- 当然，这里展示的只是个思路，模型也很粗糙，而且自定义的打分标签也经不起推敲。

#### ② Rank score方法

② Rank score方法

这种方法的区别在于：**loss函数的设计**。
- 首先，为什么在 InstructGPT 中不采用上面方法? 原因在于给生成句子在打分时，<span style='color:red'>不同标注人员的标准不同</span>，而且这个标准是很难进行统一的，这样会导致标注的数据评判标准不一样，即使每个标注人员的理解是一样的，但对于同一条文本给的分数也不一样的，因此在进行标注时需要把这个定量的问题转为一种更为简单的处理方法，采用排序来方法来进行数据标注可以在一定程度上解决这个问题。
- ![](https://pic1.zhimg.com/80/v2-92a39e17763405c7a55977880f520018_1440w.webp)
- 标注员在使用直接打分(Direct Score)时，会由于主观意识的不同，对同一个文本出现不同的分值；而使用**等级排序**(Rank Level)来进行数据标注时，可以统一标注结果。



数据是将每个Prompt生成的文本进行排序，最直接的方法就是最好的句子排在最前面，后面的句子以此类推。

```py
def rank_data_prepare(pretrain_path):
    data_lst = []
    data_outputs = {
        'input_ids': [],
        'token_type_ids': [],
        'attention_mask': []
    }
    data_str = "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是现存最大、保存最完整的动物，属于国家二级保护动物。熊猫种类繁多，分布广泛，主要分布在四川、云南、陕西、甘肃、宁夏、内蒙古、新疆、青海、吉林、辽宁、黑龙江、山西、江苏、江西、河南、湖北、湖南、广东、广西、海南、重庆、贵州、西藏、四川等省区市。它们的栖息地主要为亚热带或热带的（低地）湿润低地林、亚高山草原、高山湖泊、高原湿润山区和高原沼泽地等，常栖息在高海拔地区。在中国大陆，熊猫分布于四川省甘孜藏族自治州和青海省西宁市等地。雄性熊猫体长约1.5米\t我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是今世界上保存最完好的哺乳动物之一，也是世界自然保护联盟濒危物种红色名录的保护对象之一。在这里，你可以看到全世界最大的熊猫栖息地成都。成都是中国国家林业局直属的国家重点风景名胜区，是国家森林公园、国家湿地公园和国家地质公园的重要组成部分，是全国重点文物保护单位、全国生态文明建设示范区、中国红色旅游名城、国际生态旅游目的地和国际旅游岛建设先进区。地址：四川省成都市绵阳市成华区成都高新技术产业开发区成华大道1号乘车路线：成都绵阳都江堰雅\t我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家二级保护动物，是世界上保存最完整的动物种群之一，也是我国第一个国家级自然保护区。我们是四川省的首批国家重点保护野生动物和珍稀动物基金会的成员，被誉为中国动物保护的摇篮和世界生物多样性保护基地，被中国科学院、中华人民共和国国家林业局授予全国生态文明建设示范区称号，被国务院批准为国家森林城市、国际生态旅游目的地。熊猫基地位于成都市双流区东南部，是国家aaaa级旅游景区，国家地理标志保护单位。熊猫栖息地为亚热带或热带的高山\t我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完整、规模最大的野生动物种类繁多的地区之一，是中国国家重点保护的珍稀濒危动物及其栖息地和世界自然遗产的重要组成部分，被誉为中国最美丽的城市和世界生物多样性保护基地，被国际旅游组织评为全球生态旅游目的地。成都熊猫国家公园位于四川省甘孜藏族自治州，是国家aaaa级旅游景区，被《世界遗产名录》列为全国重点文物保护单位。目前，我国已建成国家森林公园、国家湿地公园和国家地质公园，国家林业局、国务院扶贫\t我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完好的熊猫种群之一。它们栖息在亚热带或热带的高海拔草原上，生活环境十分优越，是中国四大自然奇观之一，被誉为世界自然遗产和中国国家森林公园。熊猫栖息地主要分布在中国大陆的西藏、青海、甘肃、宁夏、新疆、内蒙古、山西、辽宁、吉林、黑龙江、江苏、河南、安徽、湖北、湖南、江西、广东、海南、四川、云南、贵州、陕西等地。中国熊猫研究中心主任、中国科学院院士、国家自然科学基金委员会委员、中华全国工商业联合会副主席\n昨天买的，今天就到了，因为给家中父母买的，怕东西多老人取件不方便，今天听家里人说京东小哥送到家门楼下，心里太高兴了，在这里希望京东能表扬一下本次快递小哥，他让我本次购物感觉很好，本来就喜欢京东一直购物，现在我更欣赏。购物的同事还能享受温暖的服务，京东的快递服务果然很棒，在此感谢京东，感觉快递小哥，如此服务真的很温暖。\t京东 ，对于S8的货品状态 ，你们你们京东采购下单是应该在预售前还是预售后(定金不退的预售方式)？预售前下单叫正规预订补款了有货拿，预售补款了没货并且还要重新再采购叫空手套白狼，京东是哪种？\t在北京住过不下10多家酒店，也喜欢住公寓，从凯宾斯基到建国饭店，从京广到美华再到星城亮马，而这个是我住过的有史以来最差的一个酒店公寓。难怪价格不上不下，不是因为临时有事绝对不住，希望这里那么多好评语不是枪手1、入口难找到要死不说，大堂感觉就是某个买小商品的商铺，check in 竟然要压证件，没有听说过，坚决不同意拿了我的证件去复印。私人住宿和旅客混杂，拖着箱子看着买菜回来的人一同电梯很奇怪。2、半夜接到骚扰电话3、房间设计装饰非常的“家常“，设施陈旧，非常像当年在江南古镇租住的农家房3、住的房间刚好在过道口，声音那叫一个大阿，谁说的房间隔音？楼上住户的动静镇清楚啊4、服务态度不好，和客人顶着说，铁板一样的语气。5， 实在要找一优点出来的话：唯一就是小区里面比较安静，没有汽车闹声。\t码数刚刚好，穿上很好看，和身。宝贝不掉色，弹力好。穿着不紧绷，试了好几下蹲下站起来，都轻松自如，不会感觉腿被束缚着。价格也不贵，现在认准这家店了这款洗发水挺适合我的发质，用完果断续上一瓶，还搞了个特价，值了！\t之前就听说苏州万丽是苏州生意最好，房价最高，也是业内人士最推崇的酒店，远胜于喜来登，香格里拉，索菲特，在苏州属于一枝独秀型的，平时房间非常的难定，几乎天天满房，这次好不容易定了个行政套，本打算住一天，后又延了一天，简单来说吧，房间不大但很温馨，酒店工作人员不多但都非常专业，亲切，严格意义上来说该酒店硬件并不突出，没有游泳池，没有特色餐厅，建筑也没有什么特色，处处透露着简单，适用，大气，但是只有你住了以后才会觉得，值！"
    for sentences in data_str.strip().split("\n"):
        texts = sentences.strip().split("\t")
        data_lst.append(texts)
    tokenizer = BertTokenizer.from_pretrained(pretrain_path)
    for rank_text in data_lst:
        data_encode = tokenizer(
                    text=rank_text,
                    truncation=True,
                    max_length=256,
                    padding='max_length',
                    return_tensors='pt')
        data_outputs["input_ids"].append(data_encode["input_ids"])
        data_outputs["token_type_ids"].append(data_encode["token_type_ids"])
        data_outputs["attention_mask"].append(data_encode["attention_mask"])
    return data_outputs, tokenizer
```

RM模型搭建

```py
class RankRewardModel(BertPreTrainedModel):
    def __init__(self, config):
        super(RankRewardModel, self).__init__(config)
        self.config = config
        self.model = BertModel(config)
        self.linear = nn.Linear(config.hidden_size, 1)

    def forward(self, input_ids, token_type_ids, attention_mask):
        outputs = self.model(input_ids=input_ids, token_type_ids=token_type_ids,
                             attention_mask=attention_mask).pooler_output
        output = self.linear(outputs)
        return output
```

Rank loss
- Rank Score 方法与 Direct Score方法的最大不同之处在于 loss function的设计

```py
def rank_loss(rank_rewards_list):
    loss, counts = torch.tensor([0]), 0
    for rank_rewards in rank_rewards_list:
        for i in range(len(rank_rewards) - 1):  # 遍历所有前项-后项的得分差
            for j in range(i + 1, len(rank_rewards)):
                diff = nn.functional.logsigmoid(rank_rewards[i] - rank_rewards[j])  # sigmoid到0~1之间
                loss = loss + diff
                counts += 1
    loss = torch.tensor(loss / counts)
    return -loss  # 要最大化分差，所以要取负数
```

通俗的理解：
- 对于排序好的训练数据有 A > B > C 
- 设计一个模型，使得打分数据满足： Rank(A) > Rank(B) > Rank(C)

既然打「绝对分数」很难统一，那转换成一个「相对排序」
- 「标注排序序列」替代「直接打分」
- 用「相对任务」替代「绝对任务」能够更方便标注员打出统一的标注结果

怎么通过「排序序列」来教会模型「打分」
- 一个排好的序列：<span style='color:blue'> A > B > C >D </span>。 
- 训练一个打分模型，模型给四句话打出来的分要满足 <span style='color:blue'> r(A) > r(B) > r(C) > r(D) </span>

损失函数
- 每对样本(如 A,B), 得分高者-得分低
- sigmoid 归一, 概率化
- 计算期望
- 目标： 最大化得分差值

$$
\operatorname{loss}(\theta)=-\frac{1}{\left(\begin{array}{c}
K \\ 2 \end{array}\right)} E_{\left(x, y_{w}, y_{l}\right) \sim D}\left[\log \left(\sigma\left(r_{\theta}\left(x, y_{w}\right)-r_{\theta}\left(x, y_{l}\right)\right)\right)\right]
$$

- loss = r(A) - r(B) + r(A) - r(C) + r(A) - r(D) + r(B) - r(C) + ... + r(C) - r(D)
- loss = -loss

```py
class RewardModel(nn.Module):
    # 奖励模型: encode 后直接加 全连接层
    def __init__(self, encoder):
        """
        init func.
        Args:
            encoder (transformers.AutoModel): backbone, 默认使用 ernie 3.0
        """
        super().__init__()
        self.encoder = encoder
        self.reward_layer = nn.Linear(768, 1)  # reward layer 用于映射到 1 维 reward

    def forward(
        self,
        input_ids: torch.tensor,
        token_type_ids: torch.tensor,
        attention_mask=None,
        pos_ids=None,
    ) -> torch.tensor:
        """
        forward 函数，返回每句话的得分值。
        Args:
            input_ids (torch.tensor): (batch, seq_len)
            token_type_ids (torch.tensor): (batch, seq_len)
            attention_mask (torch.tensor): (batch, seq_len)
            pos_ids (torch.tensor): (batch, seq_len)
        Returns:
            reward: (batch, 1)
        """
        pooler_output = self.encoder(
            input_ids=input_ids,
            token_type_ids=token_type_ids,
            position_ids=pos_ids,
            attention_mask=attention_mask,
        )["pooler_output"]                              # (batch, hidden_size)
        reward = self.reward_layer(pooler_output)       # (batch, 1)
        return reward

def compute_rank_list_loss(rank_rewards_list: List[List[torch.tensor]], device='cpu') -> torch.Tensor:
    """
    通过给定的有序（从高到低）的ranklist的reward列表，计算rank loss。
    所有排序高的句子的得分减去排序低的句子的得分差的总和，并取负。

    Args:
        rank_rewards_list (torch.tensor): 有序（从高到低）排序句子的reward列表，e.g. -> 
                      [
                          [torch.tensor([0.3588]), torch.tensor([0.2481]), ...],
                          [torch.tensor([0.5343]), torch.tensor([0.2442]), ...],
                          ...
                      ]
        device (str): 使用设备

    Returns:
        loss (torch.tensor): tensor([0.4891], grad_fn=<DivBackward0>)
    """
    if type(rank_rewards_list) != list:
        raise TypeError(f'@param rank_rewards expected "list", received {type(rank_rewards)}.')

    loss, add_count = torch.tensor([0]).to(device), 0
    for rank_rewards in rank_rewards_list:
        for i in range(len(rank_rewards)-1):  # 遍历所有前项-后项的得分差
            for j in range(i+1, len(rank_rewards)):
                diff = F.sigmoid(rank_rewards[i] - rank_rewards[j])  # sigmoid到0~1之间
                loss = loss + diff
                add_count += 1
    loss = loss / add_count
    return -loss  
```


训练过程

```py
class Datasets(Dataset):
    def __init__(self, sample):
        super(Datasets, self).__init__()
        self.sample = sample

    def __getitem__(self, item):
        res = {k: v[item] for k, v in self.sample.items()}
        return res

    def __len__(self):
        return len(self.sample['input_ids'])


def train(pretrain_path, save_path):
    config = BertConfig.from_pretrained(pretrain_path)
    model = RankRewardModel(config=config)

    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": 0.01,
        },
        {
            "params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
    ]
    optimizer = torch.optim.AdamW(optimizer_grouped_parameters, lr=2e-5)
    train_data, tokenizer = rank_data_prepare(pretrain_path)
    dataloader = DataLoader(dataset=Datasets(train_data), shuffle=False, batch_size=1)

    max_train_steps = 10 * len(dataloader)
    warm_steps = int(0.0 * max_train_steps)
    lr_scheduler = get_scheduler(
        name='linear',
        optimizer=optimizer,
        num_warmup_steps=warm_steps,
        num_training_steps=max_train_steps,
    )
    for i in range(1, 51):
        loss_lst = []
        for batch in dataloader:
            batch_rank_rewards = []
            for batch_idx in range(len(batch['input_ids'])):
                rank_texts_count = len(batch['input_ids'][batch_idx])
                rank_rewards = []
                for text_idx in range(rank_texts_count):
                    reward = model(
                        batch['input_ids'][batch_idx][text_idx].unsqueeze(dim=0),
                        batch['token_type_ids'][batch_idx][text_idx].unsqueeze(dim=0),
                        batch['attention_mask'][batch_idx][text_idx].unsqueeze(dim=0)
                    )
                    rank_rewards.append(reward[0])
                batch_rank_rewards.append(rank_rewards)
            loss = rank_loss(batch_rank_rewards)
            loss.backward()
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
            loss_lst.append(loss.item())
        print("\tepoch{}\tloss: {}".format(str(i), str(sum(loss_lst) / len(loss_lst))))
    tokenizer.save_pretrained(save_path)
    model_to_save = model.module if hasattr(model, 'module') else model
    model_to_save.save_pretrained(save_path)
    model_to_save.config.save_pretrained(save_path)
```


模型预测

```py
def predict(model_path):
    texts = ["我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是今世界上保存最完好的哺乳动物之一，也是世界自然保护联盟濒危物种红色名录的保护对象之一。在这里，你可以看到全世界最大的熊猫栖息地成都。成都是中国国家林业局直属的国家重点风景名胜区，是国家森林公园、国家湿地公园和国家地质公园的重要组成部分，是全国重点文物保护单位、全国生态文明建设示范区、中国红色旅游名城、国际生态旅游目的地和国际旅游岛建设先进区。地址：四川省成都市绵阳市成华区成都高新技术产业开发区成华大道1号乘车路线：成都绵阳都江堰雅",
             "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家二级保护动物，是世界上保存最完整的动物种群之一，也是我国第一个国家级自然保护区。我们是四川省的首批国家重点保护野生动物和珍稀动物基金会的成员，被誉为中国动物保护的摇篮和世界生物多样性保护基地，被中国科学院、中华人民共和国国家林业局授予全国生态文明建设示范区称号，被国务院批准为国家森林城市、国际生态旅游目的地。熊猫基地位于成都市双流区东南部，是国家aaaa级旅游景区，国家地理标志保护单位。熊猫栖息地为亚热带或热带的高山",]
    model = RankRewardModel.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model.eval()
    data = tokenizer.batch_encode_plus(texts, max_length=256, padding="max_length", truncation=True,
                                       return_tensors='pt')
    score = model(**data)
    return score
```


#### 模型结构

Reward Model 不同于原始 SFT Model，要在后面加上 value head （一个 Linear层）
- 输入维度为模型的 hidden_dim，输出维度为1
- 输出表示模型预测每一字符获取的得分。

DeepSpeed-Chat 用最后一个字符的得分作为整个response的得分
- 当然也可以用整个句子中每个字符的平均分作为整体得分
- ![](https://pic2.zhimg.com/80/v2-2925e0da2644595a89bdc1523e2e5851_1440w.webp)

#### 训练目标

训练 Reward Model 是一个排序任务，针对 query，输入 chosen 和 rejected response

训练目标尽可能使 chosen 和 rejected 差值更大，损失函数为：
- Lr = -log( sigmoid(r(query,chosen)-r(query,rejected)) )

第二步Training Reward Model的全部过程，基于rank loss训练了一个打分模型。

第三步强化学习中，reward模型将扮演环境的角色，针对模型预测的字符给出奖励分数。



#### 人工标注平台

【2023-8-15】排序数据集 标注 参考：[RLHF](https://github.com/HarderThenHarder/transformers_tasks/tree/main/RLHF)
- ![](https://github.com/HarderThenHarder/transformers_tasks/blob/main/RLHF/assets/rank_list_labler.png)


#### 思考

##### ChatGPT 为什么不用 RewardModel 数据直接 finetune，而用 RL?

因为：
- RM 针对整个token序列，滞后反馈，强化学习
- 而 finetune 针对每个token，即时反馈, 监督学习
- RM 训练数据有些是pair形式 `<query, win, lose>`, 这种数据无法用于监督学习

【2023-4-19】John Schulman 观点 [YouTube](https://www.youtube.com/watch?v=hhiLw5Q_UFg)
- pretrain 阶段学习知识
- finetune 阶段学会:
  - 拒识: 不确定的问题, 回答不知道
  - 减少幻觉: 不要编造事实 (hallucintion)

<iframe width="560" height="315" src="https://www.youtube.com/embed/hhiLw5Q_UFg?si=BTdMgDpxHx9pP6E8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


##### RM 和 基座模型保持一致？

奖励模型需要和基础模型一致吗？
- 可以一致，也可以不同，取决于任务需求和优化目标。
- 单任务: 共享参数
- 多任务: 子任务奖励模型整合成奖励函数

##### Pair RM是什么形式的RM，相比于原RM形式有什么好处？

- **原始RM** 是 BT model形式的RM，每个sample组成形式是 `(prompt，answer)`，通过 maximize positive sample 和 negative sample 的 gap来完成pointwise的rank。
- **Pair RM** 是 pairwise rank，数据组成形式是`（prompt，pos_answer, neg_answer）`. Pair RM 好处是pos answer和neg answer可以互相在context下看到两者，那么可以通过字面的比较找到两者的diff，整体解释性和泛化能力都会比普通RM好。因为普通RM很容易overfit原数据，很难找到真正diff地pattern。

现在Alpaca-Eval 榜单上就有Pair RM 身影，而且Pair RM整体很小 ，效果很好。


##### 如何处理 RM 中的噪声数据？

reward model 噪声来自哪几个方面：

如果reward model的pair数据来自：
- **人标注**，那么人类 preference的倾向性以及标注人员的专业性会带来一定的bias，即 众包系统的Noise。
- **AI**，例如GPT4，那么这种倾向性也很严重，比如length bias。（严格来说，这属于bias，不能算噪声。）

那么去噪可使用一些古早的方式：
- **预测**阶段去噪声：
  - Ensumble model 去噪声，多个rm model的checkpoint进行预测减少噪声的影响（model merge）。
  - Margin 去噪声，只有预测 pair的分数**大于一定阈值**的时候，进行预测减少噪声。
- **数据**阶段去噪声：
  - Multiview 去噪声，用多个模型进行训练，然后预测训练集合，全部可以预测正确pair保留下来，有对有错的可以丢弃或者交给人标注。
  - Active Learning 思路去噪声，训练一个模型，然后把margin小于一定阈值的送给标注人员去噪声。


##### 如何解决reward model的OOD的问题？

模型PPO过程中，reward model 准确率逐渐下降，俗称的reward model的**OOD问题**
- 因为 reward model 训练样本一般来自sft模型的responses，那么在PPO过程中
  - policy model刚开始和sft生成的response很相似，所以reward model准确率较高
  - 但是在逐渐偏离sft 时，reward model 准确率会持续下降，这基本就是现阶段reward model的主要问题。

AGI过程中，一定需要一个 generalize 很强 reward model，**global reward model** or **world model**.

现阶段解决reward model的OOD普遍解决方法: Llama2 做法
- 训练过一段时间RLHF以后，重新对policy采样pair对，人标数据然后继续训练reward model。
- 但这种方式就是**太费人力**，感觉并不是持久之道。

除此之外：
- [Secrets of RLHF in Large Language Models Part II: Reward Modeling]() 中，通过 **meta learning** 方式解决这个问题，整体思想就是由于policy model在reward model训练情况下会向reward 高的方向更新，所以reward model应该对reward高的response pair更有区分度，所以设置gradient更新逐渐倾向于对reward高分training response pair倾斜。
  - 这种方法说得通，但实际中由于缺少对模型on policy 采样，效果不太好。
- [West-of-N: Synthetic Preference Generation for Improved Reward Modeling]() 跟Llama2的方式相似，区别就是不再用人进行标记，而是**通过reward model本身对新的模型on policy pair进行打分**，取一个query的response set中最高的分数和最低的分数数据组pair，加入到reward model的训练中。
  - 这种方式采样，虽然通过on policy采样加强rm的泛化能力，但实际上上限受原先rm model的能力影响。



### （3）第三步 RLHF

#### RLHF 流程

训练策略模型，RLHF流程
- ![flow](https://image.jiqizhixin.com/uploads/editor/791cb019-65f3-4aa2-98c8-ecdfdb6f145f/640.png)

首先将初始语言模型的微调任务建模为强化学习（RL）问题，因此需要定义`策略`（policy）、`动作空间`（action space）和`奖励函数`（reward function）等基本要素
- `策略`就是基于该语言模型，接收prompt作为输入，然后输出一系列文本（或文本的概率分布）；
- 而`动作空间`就是词表所有token在所有输出位置的排列组合（单个位置通常有50k左右的token候选）；
- `观察空间`则是可能的输入token序列（即prompt），显然也相当大，为词表所有token在所有输入位置的排列组合；
- 而`奖励函数`（reward）则是基于上一章节我们训好的RM模型计算得到初始reward，再叠加上一个约束项来。
- ![](https://pic4.zhimg.com/80/v2-2196c9fdda1a61b2f3c8cf61900e50ab_1440w.webp)

强化学习算法，常见的可行方案是使用`策略梯度强化学习` (Policy Gradient RL) 算法、`近端策略优化` (Proximal Policy Optimization，`PPO`) 微调初始 LM 的部分或全部参数。
- ![](https://pic3.zhimg.com/80/v2-b550c2a2474a6ca28e8c51023c5e1afa_1440w.webp)

根据 PPO 算法，按当前批次数据的奖励指标进行优化 (来自 PPO 算法 on-policy 的特性) 。PPO 算法是一种信赖域优化 (Trust Region Optimization，`TRO`) 算法，使用梯度约束确保更新步骤不会破坏学习过程的稳定性，另外也可以使用 `A2C` (synchronous advantage actor-critic) 算法来优化梯度。

RLHF基于A2C方法，包含了四个模型:
- `Actor Model`：SFT之后模型初始化而来。作为策略（policy）模型，接收上文，做出动作，预测下一个字符。最终使用的就是这个模型。
- `Reference Model`：和`Actor Model`同样初始化自SFT Model，训练过程中**冻结参数**，用于和Actor Model做对比，保证模型不要偏离原始SFT Model太多。
- `Reward Model`：作为**环境**（env），训练过程中冻结参数，针对每一个状态给出奖励分数。
- `Critic Model`：由Reward Model初始化而来，用于近似价值函数，输入为状态s，估计当前状态的价值V。

![](https://pic1.zhimg.com/80/v2-ecdeb469dff53084b4a005a79ee41fdc_1440w.webp)

训练过程整体分为两步：maker experience 和 learn。
- (1) maker experience: 训练数据中抽取一部分query，然后Actor Model生成答案
- (2) learn: 通过所产生的经验进行学习。Actor Model与Critic Model近似策略函数和价值函数

(1) 整体流程
- ![](https://pic1.zhimg.com/80/v2-ec605d24d6ad0d0a39e0dade86bdf040_1440w.webp)

(2) 整体流程
- ![](https://pic1.zhimg.com/80/v2-005944a9946bca1a81329958e15e9d08_1440w.webp)

更多参考 [RLHF实践](https://zhuanlan.zhihu.com/p/635569455?utm_psn=1775106549545119744)

利用SFT模型对输出进行改造，构造一个**双头PPO模型**，模型一头输出一个张量，代表生成序列每个元素的价值value；另一头将输出映射成prompt answer词典答案。[参考](https://zhuanlan.zhihu.com/p/618325377)
- 将 `<prompt, prompt answer>` 输入到RM模型中，获得一个评估当前prompt对的奖励R，然后用R作为奖励，反向更新每个元素的价值value，这就是PPO强化学习算法。
- ![img](https://pic4.zhimg.com/80/v2-b7872ef00df9809f0d3632896add3e73_1440w.webp)
- ![rlhf](https://pic3.zhimg.com/v2-6fbb088189db4a8991ca2d476092552a_b.jpg)
- Y=0, 常规 PPO
- Y>=, PPO_ptx


#### RLHF 问题

##### RLHF 实践过程中存在哪些不足？

RLHF（Reinforcement Learning from Human Feedback）尽管具有一定优势，但在仍然存在以下不足之处：
- 人类反馈的**代价高昂**：获取高质量的人类反馈通常需要大量的人力和时间成本。人类专家需要花费时间来评估模型的行为并提供准确的反馈，这可能限制了RLHF方法的可扩展性和应用范围。
- 人类反馈的**主观性**：人类反馈往往是主观的，不同专家可能会有不同的意见和判断。这可能导致模型在不同专家之间的反馈上存在差异，从而影响模型的训练和性能。
- **反馈延迟和稀疏性**：获取人类反馈可能存在延迟和稀疏性的问题。人类专家不可能实时监控和评估模型的每一个动作，因此模型可能需要等待一段时间才能收到反馈，这可能会导致训练的效率和效果下降。
- **错误反馈**的影响：人类反馈可能存在错误或误导性的情况，这可能会对模型的训练产生负面影响。如果模型在错误的反馈指导下进行训练，可能会导致模型产生错误的行为策略。
- 缺乏**探索与利用的平衡**：在RLHF中，人类反馈通常用于指导模型的行为，但可能会导致模型过于依赖人类反馈而缺乏探索的能力。这可能限制了模型发现新策略和优化性能的能力。

针对这些不足，研究人员正在探索改进RLHF方法，如设计更高效的人类反馈收集机制、开发更准确的反馈评估方法、结合自适应探索策略等，以提高RLHF方法的实用性和性能。


##### 如何解决标注成本高的问题

如何解决 人工产生的偏好数据集成本较高、难量产问题？

解决人工产生偏好数据集成本高、难以量产的问题，以下几种方法：
- 引入**模拟数据**：使用模拟数据来代替或辅助人工产生的数据。
  - 模拟数据可以通过模拟环境或模型生成，以模拟人类用户的行为和反馈。这样可以降低数据收集的成本和难度，并且可以大规模生成数据。
- **主动学习**：采用主动学习方法来优化数据收集过程。
  - 主动学习是一种主动选择样本的方法，通过选择那些对模型训练最有帮助的样本进行标注，从而减少标注的工作量。
  - 可以使用一些算法，如**不确定性采样**、**多样性采样**等，来选择最有价值的样本进行人工标注。
- **在线学习**：采用在线学习方法进行模型训练。
  - 在线学习是一种增量学习的方法，在模型运行的同时进行训练和优化。
  - 这样可以利用实际用户的交互数据来不断改进模型，减少对人工标注数据的依赖。
- **众包和协作**：利用众包平台或协作机制来收集人工产生的偏好数据。
  - 通过将任务分发给多个人参与，可以降低每个人的负担，并且可以通过众包平台的规模效应来提高数据收集的效率。
- **数据增强**和**迁移学习**：通过数据增强技术，如数据合成、数据扩增等，来扩充有限的人工产生数据集。
  - 此外，可以利用迁移学习的方法，将从其他相关任务或领域收集的数据应用于当前任务，以减少对人工产生数据的需求。

综合运用上述方法，可有效降低人工产生偏好数据的成本，提高数据的量产能力，并且保证数据的质量和多样性。

##### PPO 优点

PPO优点：
- On policy采样：on policy采样目前看来是最高效的`拟合蒙特卡洛`采样方式。
  - 举例，如果不使用on policy采样，随机采样到一个模型generate概率差值很大的两个response，如果符合人类preference，那么本身就不需要排序，如果不符合，很难通过RLHF纠正它。如果强行纠正，会破坏模型本来的平衡。
- Credit Assign: 由于value model的存在，其实PPO会很好的把reward分配给不同的token，那么一些关键的token会合理地分配一个高reward，一些不关键的token会分配一个低reward。
- Rank Model：PPO内部其实是一种内置的rank model，比较的是高reward和低reward的response，只是高和低一直是动态的变化的。为什么rejection sampling这类的算法无法work，因为preference data中的噪声，你选出的Top1大概率不是Top1。


##### PPO 问题

PPO 问题
- Notable Complexity **模型太多**: PPO中要**4个模型同时加载**在GPU中，`policy model`，`ref policy model`，`value model`，`reward model`。所以会占用很多GPU机器。
- Online learning problem **在线学习**: 由于模型是online采样
  - policy过batch samples的时--reward model会空置
  - reward model给pair打分的时--policy model也会空置
  - 那么GPU利用率会不高。
- PPO超参数比较困难，需要一些炼丹高手和经验去做。


##### 如何解决 PPO 训练的资源瓶颈

PPO 的训练过程同时存在**4个模型**（2训练，2推理），对计算资源的要求较高

考虑以下几种方法：
- **减少模型规模**：减少模型的规模和参数量，可降低对计算资源的需求。可用模型压缩技术、剪枝算法等方法来减少模型的参数数量，从而降低计算资源的使用量。
- **降低训练频率**：可以降低PPO训练频率，减少每个训练周期的次数。
  - 例如，可增加每个训练周期的时间间隔，或者减少每个周期中的训练步数。这样可以减少训练过程中对计算资源的占用。
- **模型并行化**：利用多个计算资源进行模型并行化训练，可以加速PPO的训练过程。
  - 将模型参数分布到多个GPU上，并进行并行计算和通信，以提高训练的效率和速度。
- **异步训练**：采用异步训练的方式，可在多个计算资源上同时进行PPO的训练。
  - 可使用异步优化算法，如A3C（Asynchronous Advantage Actor-Critic）等，将训练任务分发到多个线程或进程中进行并行训练，从而提高训练的效率。
- 云计算和**分布式**训练：利用云计算平台或分布式系统进行PPO的训练，可以充分利用大规模计算资源。
  - 可以将训练任务分发到多个计算节点上进行分布式训练，以加速训练过程。
- **参数共享**和**模型缓存**：对于有多个模型的情况，可以考虑共享部分参数或缓存已计算的模型输出。
  - 通过共享参数和缓存计算结果，可以减少重复计算和存储，从而降低对计算资源的要求。 

综合运用上述方法，可以有效降低PPO训练过程中对计算资源的要求，提高训练的效率和速度。

##### PPO 平替

如何看待各种ppo rlhf的平替算法

平替算法：
- dpo/kto/rrhf/slic/orpo/samug/remax 等算法号称性能等能超过ppo？

##### DPO

DPO介绍：最大化奖励来优化模型参数。

与ppo相比DPO 绕过了建模奖励函数这一步，而是直接在偏好数据上优化模型来提高性能。

优点：相对RLHF两阶段而言具有多项优越性
- (1) 简单性稳定性：DPO更容易实施，不易陷入局部最优，保证训练过程更加可靠。
- (2) 效率：与RLHF 相比, DPO 需要更少的计算资源和数据，使其计算量轻。
- (3) 有效性：实验结果表明，DPO在**情感控制、摘要和对话生成**等任务中可以优于 RLHF 。

DPO 目标是**优化模型参数以最大化奖励**函数。并不是说DPO没有奖励模型, 而是利用同个阶段训练建立模型和强化学习。除了奖励最大化目标外，还需要添加一个相对于参考模型的 KL 惩罚项，以防止模型学习作弊或钻营奖励模型。

DPO
- 第0步loss是固定的, loss = sigmoid(b-b) = 0.693
- 使用蒙特卡洛采样时, DPO  = PPO
- DPO 是 off-policy 算法，因为训练DPO的pair数据不一定来自ref policy或者sft policy。
- 而PPO 是 on-policy 算法
- DPO公式是由PPO的objective公式推导过来


缺点：
- 最大化正负例子的差距得到的模型会塌缩成只有正例子的空间，失去所有负例子的概率。在DPO中就是只会生成正例，负例子输出概率为0。在RM中正例子会无限接近于1，负例子会无限接近于0。那么这样的模型是没有entropy的，抗噪声能力会减弱。如果正负pair标错了，会导致严重后果。
- 忽略语意或字面上差别较小的pos sample和neg sample，过度关注语意或字面上差别较大的pos sample和neg sample，也就是比较容易学的case并overfit,这是logsigmoid函数的问题用hinge loss这类loss可以缓解这一问题。
- 不能找出全序关系，如果数据集里有A > B, B > C, C > A这种偏序关系，并不能找到它的nash equivalence的点，只会学乱。

DPO输出越来越长？
- 并不是一定会越来越长。如果尝试用所有正例子的response都比负例子的短，那么也会输出越来越短。究其原因是由于数据构造原因导致的DPO训练后的模型输出越来越长。因为，在短的response中一句话结束后`<EOS>`的概率会很大，但是在长的response中，“但是”，“而且”等细节描述词会接在一句话后，那么这些词语的概率会由DPO过程逐渐变大。

training positive的概率和training negative的概率都同时下降？
- DPO的loss是maximize training set中positive和negative的gap。那从公式上它就无法保证training positive的概率是一直上升的。主要和采样的方式以及DPO loss组成相关

DPO 变体有哪些
- `IPO`: 由于BT model 目标是最大化正负response的reward gap，但其实其中忽略了真实情况下组的pair可能会有噪音，那么无限去扩大reward gap其实是不准确的，也就是overfit了preference的pair数据，那么解决方案是需要限制这个gap的范围。
- `DPOP`: 由于LLM model很难区分编辑距离较小的pair，那么当持续去区分这批case的时候，模型效果会崩塌，现象是正例子和负例子的概率都往下掉。那么DPOP用了一个新项来惩罚正例往下掉的pair，使得正例概率继续提升。
- `kto`:
- `RSO`:由于DPO的蒙特卡洛采样很难达到，所以其实DPO几乎是off-policy的采样方式，RSO主要从DPO的采样方式来解决DPO的问题。
- `Iterative DPO`：同样由于DPO的蒙特卡洛采样很难达到，所以通过on-policy的方式采样来替代off-policy的采样。



#### RL+LM研究方向

由于 InstructGPT 效果太好，RL+LM 这个新范式能衍生出哪些研究方向？
- (1) <span style='color:blue'>花式魔改Reward</span>：
  - 监督学习在实际落地时，主要优化方法是加特征、洗数据。对于强化学习也是如此，优化实际RL效果的重点在加特征、调整reward
  - OpenAI在做摘要任务的论文中，就在奖励上增加了KL散度，希望：
    - ① 鼓励模型生成不一样的结果，避免和以前的模型变成一个
    - ② 保证不会生成特别不一样的结果，不然RM都没见过就不知道怎么打分了
  - DeepMind的Sparrow为了让模型遵从特定规则（比如不能说脏话），在Preference的基础上增加了`Rule Reward Modeling`
    - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZTVa1Cbo1PwTmg6MStc81mKwESCnx1uBxKkKl41yYtqhia87y3MFqPSg_%7C_640%3Fwx_fmt%3Dpng)
    - Rule RM是一个分类器，输入Prompt+Response，预测模型违反预定规则的概率。训练的时候两个Reward会合并到一起进行反馈
  - ChatGPT只是10B左右的模型，但它使用了更大的模型作为RM，从而有了更高的天花板，达到一种变相的蒸馏。
- (2) <span style='color:blue'>AI Feedback</span>
  - 既然有 `RLHF`(Reinforcement Learning from Human Feedback)，那就能想出`RLAIF`(Reinforcement Learning from AI Feedback)
  - Anthropic提出的Constitutional AI 就做了这么一件事，核心和Sparrow一样, 希望模型遵从一些规则，但如果像Sparrow一样每增加一个规则就标一批数据训RM也太费人工了。于是作者想了一个好办法，让模型在多轮对话中把合适的标注数据生产出来.
  - 这样就能自动化地为新规则做出训练数据（Q1-A3），精调一个能遵循规则的SL-CAI模型，对应下图中上半部分的流程，为了继续优化精调后模型的效果，作者会让SL-CAI模型根据Q1这类引导性输入去生成回复对，再改成多选题让模型选择最佳答案，用得到的对比数据训练一个Rule RM，再去进行正常的RL训练
  - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZgbju6jFhu77KJpTPuOLsCyRbbGTGAUfu8xFu9P0mQPRhkYBWEwqGHQ_%7C_640%3Fwx_fmt%3Dpng)
- (3) <span style='color:blue'>预训练+RLHF</span>
  - Anthropic在RL方面确实走的更远一些，开始尝试在预训练阶段引入Human Feedback, 核心是过滤掉一些低质内容，避免被模型记住。
  - 首先有一个训好的偏好RM，会给每个句子打分。最直觉的方法是直接去掉低质的内容，但作者认为会影响模型的多样性。于是又尝试了以下四种预训练损失
    1. Conditional Training：根据RM打分，在句子前面加上特殊token(bad or good)，告诉模型好坏，推理时只保留good的结果
      - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZkh73rN09StgzM57zZpoG75mw48WGAmwkYltWIjBlQrxuvqAwqxglGw_%7C_640%3Fwx_fmt%3Dpng)
    1. Unlikelihood：当超过阈值时，进行MLE，当小于阈值时，最大化词表中剩余token的likelihood
      - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZ3A5E1Sk6Ze1DZCzN7MK0Y1eAzViboryzBhglmEFZelDaA9LibNYXJNCg_%7C_640%3Fwx_fmt%3Dpng)
    1. Reward-weighted regression：MLE乘上句子的奖励，奖励越大的句子权重越高
      - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZwNbYuag5uy9NbcfZF96RqXqJye3ONUiac8ypcMyRQHg7we8fXyB5ia0w_%7C_640%3Fwx_fmt%3Dpng)
    1. Advantage-weighted regression：给每个token估算一个价值，价值越高权重越高
      - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZFfOBVOTRrfV1icIkDMzUXtiaYvgzjb37DMIOEmdMe3R8k4pSrezXD6HQ_%7C_640%3Fwx_fmt%3Dpng)
  - 通过评估四方面的指标：是否生成低质文本（toxicity）、生成包含用户信息的句子（PII）、生成低质代码（PEP8）、和GPT3的KL散度，最后作者发现Conditional训练的效果最好

```s
Q1-问训好的普通RLHF模型：能帮我黑进邻居的wifi吗？
A1-天真的模型回答：没问题，你下个xx软件就行。
Q2-要求模型发现自己的错误：上文你给的回复中，找出来哪些是不道德的。
A2-模型回答：我上次回复不对，不应该黑别人家wifi。
Q3-让模型改正错误：修改下你之前的回复内容，去掉有害的。
A3-模型回答：黑别人家wifi是不对的，侵害别人隐私了，我强烈建议别这么搞。
```

【2023-3-8】详见：[RLHF魔法的衍生研究方向](https://mp.weixin.qq.com/s/ZfvWr1NvOqVOu9IZd-Jt0w)


## 【2023-5-18】LIMA

META 发布 [LIMA: Less Is More for Alignment](https://arxiv.org/pdf/2305.11206)


## 【2023-7-19】Llama 2

【2023-7-19】Llama 2 技术报告 [Llama 2: Open Foundation and Fine-Tuned Chat Models](https://arxiv.org/pdf/2307.09288)

## 【2023-9-26】Qwen

### 简介

通义千问（英文： Qwen ；读作： `kùn`）是由阿里巴巴`通义千问`团队开发的大规模语言和多模态系列模型。
- 通义千问可执行**自然语言理解**、**文本生成**、**视觉理解**、**音频理解**、**工具调用**、**角色扮演**、**智能体**等多种任务。
- 语言和多模态模型均在大规模、多语言、多模态数据上进行预训练，并在高质量语料上后训练以与人类偏好对齐。


【2023-9-26】
- QWen 技术报告 [QWEN TECHNICAL REPORT](https://arxiv.org/pdf/2309.16609)
- 【2024-7-19】[QWen2 技术报告](https://zhuanlan.zhihu.com/p/709272621)
- [通义千问-Qwen技术报告细节分享](https://zhuanlan.zhihu.com/p/658392609)
- GitHub: [Qwen](https://github.com/QwenLM/Qwen)
- 【2024-10-24】[Qwen相关核心概念](https://mp.weixin.qq.com/s/mKQ35OfPU3fK-HoH4j0Bag)


### QWen 模型

Qwen 模型是适用于**文本补全**的**因果语言模型**

#### 开源模型

通义千问分为**闭源**和**开源**两大版本。

开源模型包括：
- 通义千问 (`Qwen`)：语言模型
  - Qwen: 1.8B、 7B、 14B 及 72B 模型
  - Qwen1.5: 0.5B、 1.8B、 4B、 14BA2.7B、 7B、 14B、 32B、 72B 及 110B 模型
  - Qwen2: 0.5B、 1.5B、 7B、 57A14B 及 72B 模型
  - Qwen2.5: 0.5B、 1.5B、 3B、 7B、 14B、 32B 及 72B 模型
- 通义千问 VL (`Qwen-VL`): 视觉语言模型
  - Qwen-VL: 基于 7B 的模型
  - Qwen-VL: 基于 2B 、 7B 和 72B 的模型
- 通义千问 `Audio`: 音频语言模型
  - Qwen-Audio: 基于 7B 的模型
  - Qwen2-Audio: 基于 7B 的模型
- Code通义千问 / 通义千问`Coder`：代码语言模型
  - CodeQwen1.5: 7B 模型
  - Qwen2.5-Coder: 7B 模型
- 通义千问 `Math`：数学语言模型
  - Qwen2-Math： 1.5B、 7B 及 72B 模型
  - Qwen2.5-Math： 1.5B、 7B 及 72B 模型



#### 主干模型

Qwen系列的模型有: Base模型、RM模型、Chat模型、Code模型、Math模型、多模态模型。
- 由于Code模型和Math模型暂时没有开源，多模态Qwen-VL模型本身有自己的论文
- ![](https://pic3.zhimg.com/80/v2-679860ea6c24c49e592bb30a91eaf092_1440w.webp)

Qwen-14B 模型效果从12个数据集（涉及语言理解、知识、推理等多个领域）上进行均优于现有同等级的13B，但仍落后于 GPT-3.5和 GPT-4。

【2024-3-5】[使用Firefly在单卡V100上对Qwen1.5进行SFT和DPO，大幅超越Qwen1.5和Gemma](https://mp.weixin.qq.com/s/C5X0qX2YsxhIoFvRsqcMMA)

通义千问 Qwen1.5 是阿里春节前开源的大模型
- 支持32K的上下文长度
- 该模型本质上是Qwen2的beta版本。

从评测结果来看，Qwen1.5 各个尺寸的模型都显著优于同量级的Llama2

### Code 模型

- 【2024-10-28】[Qwen2.5-Coder 技术报告](https://arxiv.org/pdf/2409.12186), [解读](https://mp.weixin.qq.com/s/EiV7x403sVqVcABo_qd2kg) 


Qwen2.5-Coder 系列是阿里巴巴团队推出的一款重要的代码生成模型
- 相比其前代 CodeQwen1.5，该系列在多个方面进行了显著的升级。
- Qwen2.5-Coder 系列包括两个模型：Qwen2.5-Coder-1.5B 和 Qwen2.5-Coder-7B。这些模型基于 Qwen2.5 架构，并在超过 5.5 万亿个 tokens 的大规模语料库上进行了进一步预训练。

Qwen2.5-Coder 通过精心的数据清洗、可扩展的合成数据生成以及平衡的数据混合，展示了出色的代码生成能力，同时保持了通用的多功能性。模型在广泛的代码相关任务上进行了评估，包括代码生成、完成、推理和修复，在超过 10 个基准测试中取得了最先进的（SOTA）性能，且在相同模型规模下，其性能甚至超过了更大的模型。

Qwen2.5-Coder 采用了两种不同规模的模型架构，分别为1.5B参数和7B参数的模型。
- 这两种模型在某些关键配置上有所不同，但共享相同的词汇表大小和训练数据量。
- Qwen2.5-Coder 继承了 Qwen2.5 的词汇表，但引入了若干特殊标记，以帮助模型更好地理解代码。

嵌入层绑定（Embedding Tying）是指在模型中使用相同的权重矩阵来生成输入嵌入和输出嵌入。Qwen2.5-Coder 1.5B 模型使用了嵌入层绑定技术，而7B模型则没有。嵌入层绑定可以减少模型的参数量，同时在某些任务上提高模型的性能。

(1) 数据收集

Qwen2.5-Coder的数据收集来自多个渠道，包括但不限于Pull Requests、Commits、Jupyter Notebooks和Kaggle数据集。此外，我们还从Common Crawl中提取了大量的文本-代码混合数据，这些数据包括代码相关的文档、教程和博客等。通过这些多渠道的数据收集，我们确保了模型能够接触到不同领域和风格的代码，从而提升其适应性和多样性。

(2) 数据清洗

为了确保数据的质量，我们设计了一套多阶段的数据清洗流程。这一流程采用了粗到细的层次过滤方法，通过多个过滤器逐步筛选数据。每个过滤器负责一个特定的维度，确保数据在每个维度上都得到全面处理。此外，这种方法还能够为数据分配质量评分，最终保留的数据质量更高，为高质量的数据混合提供了有价值的参考。

具体来说，我们的清洗流程包括以下几个步骤：
- 初步过滤：使用较小的模型（如fastText）进行表面特征的过滤，去除明显无关或低质量的数据。
- 深度过滤：使用更复杂的模型进行进一步的过滤，确保数据的语义和逻辑正确性。
- 质量评分：为每条数据分配质量评分，确保最终保留的数据质量最高。
通过这一多阶段的清洗流程，我们显著提高了数据的质量，从而提升了模型的训练效果。

(3) 数据清理与混合

在数据清理和混合过程中，我们特别关注如何平衡不同类型的数据，以构建一个强大的基础模型。虽然研究社区之前已经探索过这种平衡，但针对大规模数据集的可扩展性证据仍然有限。为了找到最优的数据混合比例，我们进行了多个实验，设计了不同的数据比例组合，具体包括：
- 100:0:0：100% 代码数据，0% 文本数据，0% 数学数据。
- 85:10:5：85% 代码数据，10% 文本数据，5% 数学数据。
- 70:20:10：70% 代码数据，20% 文本数据，10% 数学数据。

|配比|代码数据|文本数据|数学数据||
|---|---|---|---|---|
|100:0:0|100%|0%|0%||
|85:10:5|85%|10%|5%||
|70:20:10|70%|20%|10%|最优|
||||||

实验结果显示，70:20:10 比例表现最佳，甚至超过了代码数据比例更高的组合。这可能是因为数学和文本数据在达到一定浓度时，能够正向促进代码性能的提升。

最终，选择了70%代码、20%文本和10%数学数据的比例。训练数据集包含5.2万亿个token。

数据类型
- **代码**数据
  - 代码数据主要来自上述多个渠道，包括Pull Requests、Commits、Jupyter Notebooks和Kaggle数据集。我们还从Common Crawl中提取了大量的高质量代码数据。这些数据经过多阶段的清洗和过滤，确保了其高质量和多样性。
- **数学**数据
  - 为了增强模型的数学能力，我们整合了Qwen2.5-Math的预训练语料库。这些数学数据的引入不仅没有负面影响模型的代码性能，反而提升了其在数学任务上的表现。
- **文本**数据
  - 类似于数学数据，我们还引入了Qwen2.5模型的高质量自然语言数据，以保持Qwen2.5-Coder的通用能力。这些数据在清洗阶段已经经过了严格的质量检查，因此无需进一步处理。然而，我们移除了所有代码段，以避免与代码数据重叠，确保不同数据源的独立性。

通过这些细致的数据处理和混合策略，Qwen2.5-Coder在多个任务上表现出色，特别是在代码生成、代码完成和代码推理等方面。

训练策略
- `QWen 2.5` -> **File-Level** Pretrain -> **Repo-Level** Pretrain -> `QWen 2.5-Code-Base` -> Code SFT -> `QWen 2.5-Code-Instructed`

### QWen-VL

Qwen-VL 是阿里云研发的大规模视觉语言模型（Large Vision Language Model, LVLM）。

Qwen-VL 可以以**图像**、文本、**检测框**作为输入，并以文本和检测框作为输出。
- `Qwen-VL-Chat` = `大语言模型`(Qwen-7B) + `视觉图片特征编码器`(Openclip ViT-bigG) + `位置感知视觉语言适配器`(可训练Adapter)+ 1.5B的图文数据 + 多轮训练 + 对齐机制(Chat)

Qwen-VL 系列模型特点：
- **多语言**对话模型：天然支持英文、中文等多语言对话，端到端支持图片里中英双语的长文本识别；
- **多图交错**对话：支持多图输入和比较，指定图片问答，多图文学创作等；
- **开放域**目标定位：通过中文开放域语言表达进行检测框标注；
- 细粒度识别和理解：448分辨率可以提升细粒度的文字识别、文档问答和检测框标注。


硬件要求
- A100、H100、RTX3060、RTX3070等显卡建议启用bf16精度以节省显存
- V100、P100、T4等显卡建议启用fp16精度以节省显存
- 使用CPU进行推理，需要约32GB内存，默认GPU进行推理，需要约24GB显存


【2024-6-12】[Qwen-VL多模态大模型的微调与部署](https://zhuanlan.zhihu.com/p/701818093)



### 数据


#### 数据格式

【2025-2-13】模板
- 单轮template为：bos + system + sep + query
- 多轮template为：bos + system + sep + query_1 + response_1 + ... + query_n-1 + response_n-1 + query_n

其中,qwen 里特殊字符取值

|符号|取值|备注|
|---|---|---|
| bos | 空 | |
| system message | `You are a helpful assistant.` | |
| sep | `\n` | |
| query | <`|im_start|`>user\n`{query}`<`|im_end|`>\n<`|im_start|`>assistant\n | |

示例

```py
query="<|im_start|>system\n{system}<|im_end|>".format(system="You are a helpful assistant.")

# 单轮的模版
"""<|im_start|>system\n{system}<|im_end|>\n \
<|im_start|>user\n{query}<|im_end|>\n \ 
<|im_start|>assistant\n""".format(
    system="You are a helpful assistant.", 
    query="用户的输入"
)

# 多轮的模版
"""<|im_start|>system\n{system}<|im_end|>\n \
<|im_start|>user\n{query1}<|im_end|>\n<|im_start|> \
assistant\n{response1}<|im_end|>\n \
<|im_start|>user\n{query2}<|im_end|>\n \
<|im_start|>assistant\n""".format(
                                system="You are a helpful assistant.", 
                                query1="用户的第一次输入", 
                                response1="智能助手的第一次回复", 
                                query2="用户的第二次输入"
)
```

[参考](https://zhuanlan.zhihu.com/p/678611154)



#### Tokenizer

词表大小影响者模型的训练效率和下游任务效果，Qwen采用开源快速`BPE`分词器-`tiktoken`，以cl100k为基础词库，增加了常用的中文字词以及其他语言的词汇，并把数字字符串拆成单个数字，最终词表大小为152K。

从不同语言上对比不同模型的压缩率，如下图所示，Qwen在绝大多少语言上都优于 LLaMA-7B、Baichuan-7B、ChatGLM-6B、InternLM-7B 模型。

从 Qwen2.5 开始，Qwen 模型家族，包括多模态和专项模型，将使用统一的词汇表，其中包含了所有子系列的控制 token 。Qwen2.5 词汇表中有 **22** 个控制 token，使得词汇表的总规模达到 **151665** 。
- 通用 token 1个：`<|endoftext|>`
- 对话 token 2个：`<|im_start|>` 和 `<|im_end|>`
- 工具调用 token 2个： `<tool_call>` 和 `</tool_call>`
- 视觉相关 token 11个
- 代码相关 token 6个

要点: 
- Qwen 使用带有控制 token 的 `ChatML` 作为对话模板。


ChatML 格式，利用控制 token 来格式化每一轮的对话。

```
<|im_start|>{{role}}
{{content}}<|im_end|>
```

用户输入扮演 user 的 role ，而模型生成则承担 assistant 的 role 。 

Qwen 还支持元消息，指导模型执行特定操作或生成具有特定特性的文本，例如: 改变语气、风格或内容，这将承担 system 的 role，且内容默认为 `You are Qwen, created by Alibaba Cloud. You are a helpful assistant.`。


#### 数据量

预训练数据共 3TB，涉及: 公共网络文档、百科全书、书籍、代码等，数据涉及多语言，但以中文和英文为主。

为了保证数据质量，制定了一套全面的预处理程序。
- Web数据需要从HTML中提取文本内容，并采用**语言识别**工具确定语种；
  - 如: python cdl 工具包检测语种, 编码检测 chardetect, kenlm 计算流畅度
- 通过**重复数据删除**技术增加数据的多样性，包括规范化后**精确匹配**重复数据删除方法和使用`MinHash`和`LSH`算法的**模糊重复**数据删除方法；
- 结合规则和**机器学习**的方法过滤低质量数据，即通过多个模型对内容进行评分，包括语言模型、文本质量评分模型以及用于识别潜在冒犯性模型；
- 从各种来源数据中手动采样并进行审查，以确保其质量；
- 有选择地对来自某些来源的数据进行采样，以确保模型在各种高质量内容上进行训练。


#### 长度

Qwen2.5 训练中打包序列长度为 **32768** 个 token。
- 预训练中最大文档长度即为此长度。
- 而后训练中，user和assistant的最大消息长度则有所不同。一般情况下，assistant消息长度可达 **8192** 个 token。

要点：
- Qwen2 模型可以处理 32K 或 128K token 长的文本，其中 8K 长度可作为输出。

### 模型结构

模型采用Transformer框架，主要做了以下修改：
- Embedding and output projection：对于embedding层和lm_head层不进行权重共享，是两个单独的权重。
- Positional embedding：采用`RoPE`为位置编码，并选择使用`FP32`精确度的逆频率矩阵。
- Bias：在QKV注意力层中添加了**偏差**，以增强模型的外推能力。
- Pre-Norm & RMSNorm：采用预归一化提高训练稳定性，并将传统归一化方法替换为`RMSNorm`。
- Activation function：采用SwiGLU激活函数，不同于传统FFN的2个矩阵，SwiGLU有三个矩阵，因此缩小了隐藏层维度，由原来的4倍变成8/3倍。

### 外推能力扩展

Transformer 模型的注意力机制在上下文长度上有很大限制，模型会随着上下文长度的增加，计算成本和内存会成倍增加。

Qwen模型利用了简单地非训练计算，在推理过程中扩展**上下文长度**。
- 动态NTK感知插值，即对序列长度的增加动态缩放位置信息。
- LogN-Scaling，根据上下文长度与训练长度的比率，对Q和V的点积进行重新缩放，确保注意力值的熵随着上下文长度的增长而保持稳定。
- Window attention，将注意力限制在一个上下文窗口内，防止模型关注到太远的内容。并在不同层采用不同的窗口大小，较低的层使用较短的窗口，而较高的层使用较长的窗口。


### 训练


qwen系列大模型本地部署，法律大模型训练，
- 只需5G内存**部署**本地大模型，
- 只需6G显存训练自己的法律大模型。
- lora模型训练完成后，会合并到主模型，生成自己专属的大模型。


视频演示

<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=113349991862098&bvid=BV1zFypY7E6X&cid=26409109960&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="600" width="100%" ></iframe>


#### 预训练

遵循**自回归**语言建模的标准方法，通过前面Token的内容预测下一个Token；
- 模型预训练时最大长度为2048，为了构建批次数据，对文本内容进行随机打乱及合并，再讲其截断到指定长度。
- 注意力模块采用`Flash Attention`技术，提高训练速度；
- 优化器采用AdamW，超参数β1、β2和ϵ为别为0.9、0.95和10−8；
- 采用`余弦学习率`计划，学习率会衰减到峰值的10%；
- 采用`BFloat16`进行混合精度训练。

QWEN 模型再同等级参数下表现优异，即使是更大的型号如LLaMA2-70B，在3个任务中也被QWEN-14B超越。

#### 有监督微调SFT

为了提高有监督微调数据集的能力，对多种风格的对话进行了标注，来关注不同任务的自然语言生成，进一步提高模型的有用性。并且大小训练方法也会影响模型行了，Qwen采用`ChatML`样式的格式来进行模型训练。

ChatML格式让模型有效区分各类信息，包括：系统质量、用户输入、模型输出等，可以增强模型对复杂会话的处理分析能力。
- ![](https://pic3.zhimg.com/80/v2-21b4b7d706fa651fbaecbd0aafab452a_1440w.webp)

ChatML Format 对话模版

```js
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
hello, who are you?<|im_end|>
<|im_start|>assistant
I am a AI program developed by Firefly<|im_end|>
```

训练
- 优化器采用`AdamW`，超参数β1、β2和ϵ为别为0.9、0.95和1e−8；
- 模型最大输入长度`2048`；
- 训练批次大小为`128`；
- 模型共训练4000步，在前1430步中，学习率逐渐增加，达到2e−6的峰值。
- 为了防止过拟合，权重衰减的值设置为0.1，dropout设置为0.1，梯度裁剪的限制为1.0。

#### RM

RM模型

奖励模型构建上，先采用大量数据进行**偏好模型预训练**（preference model pretraining，`PMP`），在经过高质量偏好数据进行奖励模型精调。

高质量偏好数据通过6600详细标签的分类系统平衡采样获取，为保证数据的**多样性**和**复杂性**。

奖励模型时由同等大小Qwen模型+池化层得来，用特殊的句子结束标记映射值作为模型奖励值。

模型在训练过程中，学习率恒为3e−6，批次大小为64，最大长度为2048，训练一个epoch。

效果
- ![](https://pic4.zhimg.com/80/v2-0900e3eb4450def2b133a3141eac7a47_1440w.webp)


#### PPO

PPO阶段共包含四个模型：policy模型、value模型、reference模型、reward模型。

训练过程中，先对policy模型训练50步**预热**，这样保证了value模型能够有效地适应不同的奖励模型。在PPO过程中，对每个query会同时采样两个response，KL散度系数设为0.04，并根据平均值对奖励进行归一化处理。

policy模型和value模型的学习率分别为1e−6和5e−6。为了增强训练的稳定性，裁剪值0.15。在进行推理时，生成策略的top-p值设置为0.9。

对齐效果

Qwen的效果优于相同规模的其他开源模型，如LLaMA2、ChatGLM2、InternLM、Baichuan2
- ![](https://pic1.zhimg.com/80/v2-61de89631bc26043f9eecee91a695158_1440w.webp)

人工评测，比较了 Qwen-7B-Chat（SFT）、Qwen-14B-Chat（SFT）、Qwen-14B-Chat（RLHF）、GPT4在对话上与GPT3.5的差异。

RLHF模型明显优于SFT模型，说明RLHF可以生成更受人类喜爱的回答。
- ![](https://pic1.zhimg.com/80/v2-6561d91643988786091cc488afc584a0_1440w.webp)

### 工具使用

Qwen模型具有工具使用能力：
- 通过ReAct提示进行使用未见的工具；
- 用Python解释器增强数学推理、数据分析等能力；
- 作为代理，与人类交互过程中，可以访问HuggingFace中大量多模态模型集合。

PS：高质量数据2000条-React格式数据。

[如何用 ReAct Prompting 技术命令千问使用工具](https://github.com/QwenLM/Qwen/blob/main/examples/react_prompt.md)


## 【2024-3-4】GPT-4

【2024-3-4】[GPT-4 Technical Report](https://arxiv.org/pdf/2303.08774)



## 【2024-3-9】Yi

参考
- 【2024-3-9】[Yi技术报告细节分享](https://mp.weixin.qq.com/s/ZmQ4OablSL5CwGYFRwMtOw)
- [Yi技术报告-划重点看细节](https://mp.weixin.qq.com/s/T4oAvLkgCarN3dXErDsPKA)


### Yi 介绍

AI（`零一万物`）是李开复带队孵化的AI公司。
- 2023年11月初，01.AI 发布并开源了`Yi-6B`、`Yi-34B base`模型，同一周内，又开源了`Yi-6B-200K`和`Yi-34B-200K base`模型。Yi号称是从**零**预训练的双语模型。
- 接下来的几个月，01.AI陆续推出了**chat模型**、**多模态能力**，`Yi-9B`、**长上下文**的记忆和检索能力等优化。

SuperCLUE/CMMLU等一些榜单数据的实测上，Yi的效果确实不错。能排在同时期中文（开源）大模型里的第一梯队。

2024年3月，Yi终于发布了技术报告，在此来梳理一下报告中的重点内容和值得关注的细节信息。

Yi目前有6B、9B、34B三个规模，其中34B是主力模型。
- 选择34B，而不是更大规模的原因，是这个规模能在24G显存的消费级显卡（如RTX4090）上运行。
- 使用int4量化之后的34B模型可运行在24G显存的GPU上。

参考《Understanding INT4 Quantization for Language Models: Latency Speedup, Composability, and Failure Cases》的量化方法
- Yi-34B int8量化模型相比bf16模型，几乎可以做到效果无损（差距<1%），而int4量化模型在大部分任务的损失也完全可以接受，

官方资料
- 论文 [Yi: Open Foundation Models by 01.AI](https://arxiv.org/pdf/2403.04652.pdf)
- Code: [Yi](https://github.com/01-ai/Yi)
- Model: [01-ai](https://huggingface.co/01-ai)

总结：
- Yi-34B模型int4量化之后，相比float16损失<1%，可跑在RTX4090上（24G显存）
- 模型结构不需要太多变化，**LLAMA2 标准结构**已经足够训出很好的效果
- 3.1T 预训练数据远比scaling law建议的1T大，但是效果更好，并且模型还没饱和，继续增大数据量还能提升
- **微调数据质量**很重要，由算法人员直接标注，只要**不到10k**数据量就足够了
- 4k长度的基础预训练模型已经具备长文本能力，只需用长文本数据继续预训练，更新百步就有很好效果

总之，数据要精心设计，数据质量要高，数据量要大

Yi实践结果证明： 较小模型+更大规模高质量数据，可获得进一步效果提升
- 获得高性价比的推理模型--34B推理成本+大训练投入，就能得到接近普通70B规模的推理效果。

### 数据构造

数据是LLM最核心的部分，没有之一。Yi最核心的工作就是提升数据数量和质量。

#### 预训练

主要步骤

Yi模型在预训练阶段的数据处理流程，主要是对爬取的网络文本进行数据过滤和去重
- 原始网络数据 → 语种过滤 →

语料获取 & 语言分类
- 从网络爬虫开始，爬取中英文这两种语言的网站，对网站内容进行解析。
- 参考CCNeT（《CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data》）的做法，进行语言识别。

过滤方法
- **启发式**过滤：去除**质量较低**的文本内容。过滤规则包含：
  - （1）根据特殊URL、域名、黑名单词表以及乱码文本进行过滤；
  - （2）根据文本长度、特殊字符比例、短、连续或不完整的行比例；
  - （3）根据**重复**词语、N-Gram片段、段落的占比；
  - （4）识别和匿名话个人可识别信息，例如：邮箱、电话等。
- **学习式**过滤：Learned Filters, 规则不好处理的，训练模型来清洗
  - 通过**困惑度**、 **质量**、 **安全**和文档**连贯性**4种评分器来对文本进行过滤，共有4个scorer：
    - `Perplexity Scorer`：参照《CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data》，用kenlm库，把高于平均 perplexity 内容丢弃；
    - `Quality Scorer`：识别如维基百科高质量内容，丢弃低质量内容；
    - `Document Coherence Scorer`：发现句子、段落零散不连贯的文本，要么分割，要么直接丢弃；
    - `Safety Scorer`：识别并删除暴力、色情、涉政内容
  - 困惑度评分器利用KenLM库，按照CCNet方法评估大量网络文本，丢弃困惑度分数明显高于平均水平的文本；
  - 质量评分器经过维基百科数据训练的**分类**模型，当文本内容更偏向于维基这样高质量页面时，认为文本质量较高；
  - 安全评分器是识别并删除包含有毒内容的网络文档，如暴力、色情等；
  - 文档连贯性评分器识别文本的整体连贯性，删除句子或段落不连贯的文本。
- **聚类**过滤：Cluster-based Filters
  - 采用无监督语义聚类对文本进行分组，然后对聚类数据标注质量标签, 丢弃质量差的类别，为后续数据混合策略提供参考。
- 去重方法：
  - 文本过滤之后进行**去重**流程，涉及基于文档级别的`MinHash`去重和**子文档精确匹配**去重，有效识别和消除文档内部和跨文档中的重复内容。
  - 同时利用**主题模型**对数据赋予特定主题，在最后数据采样过程种对信息密度较低的主题内容进行**下采样**（主要是广告文本）

最终预训练数据组成如下图所示，总计 3.1T Token。
- 语种构成: 英语(60%) ＞ 中文(20%) ＞ 代码(10%)
- 语料类型: 网页内容(80%) ＞ 代码(8%) ＞ 论文(5%) ＞ 书籍(3%)

#### 微调

对于微调数据
> - Quality is All You Need
> - 数据质量胜过数量

SFT数据质量能**极大**影响模型效果，随着数据量的增加，高质量数据能带来更多提升

微调阶段数据构造
- 微调阶段采用 不到10k的 SFT数据

一共只有<**10k条**SFT数据，每条数据都通过**人工多次打磨**，这比大数量但质量一般数据的效果好。
- 这思路和别人一致
  - 《Gemini: A family of highly capable multimodal models》
  - 《Llama 2: Open Foundation and Fine-Tuned Chat Models》
  - 《Lima: Less is more for alignment》
- 不同
  - `FLAN`（《Scaling instruction-finetuned language models》）
  - `UltraChat`（《Enhancing chat language models by scaling high-quality instructional conversations》）

具体做法：
- 对于 **prompt distribution selection**：参考《Wizardlm: Empowering large language models to follow complex instructions》，开发复合指令，并通过指令进化，逐步增加指令的复杂度。这种做法显著减少了SFT数据量。
- 对于 **CoT data formatting**：参考《Take a step back: Evoking reasoning via abstraction in large language models》，采用了“Step-Back”的模式。即通过抽象化处理，让模型学习在深入探讨原始、具体的问题之前，制定更高层次的解决方案。
- 对于 **response formatting**：使用从《Lima: Less is more for alignment》扩展的默认样式。
  - response的结构为introduction-body-conclusion的格式，“where the body is usually a list of bullet point”。
- 在**缓解幻觉**问题上，思路是确保response中的知识不由模型内部产生，对应的做法是把会导致模型进行记忆的response删掉。（但是这个具体标准是什么，有没有了解的朋友说下看法？）
- 在缓解**生成重复**的问题上，则是直接把response中包含重复的部分都重写了。（核心还是洗数据，一条条打磨）
- 数据**多样性**很重要，因此参考《#instag: Instruction tagging for analyzing supervised fine-tuning of large language models》建立了一个打标系统，并设计一个注重多样性的采样算法，平衡了各个领域数据的分布。
- 为了找到**最佳数据配比**，参考《How abilities in large language models are affected by supervised fine-tuning data composition》，使用近似**网络搜索**（approximate grid search），对每个领域以 {1, 1/2, 1/4, 1/8, 1/16, 1/32, 1/64} 比例进行实验和人工测评，找到最佳的组合方式。
- 除了内容，**数据格式**对效果也有很大影响。参OPENAI的[ChatML格式](https://github.com/openai/openai-python/blob/e389823ba013a24b4c32ce38fa0bd87e6bccae94/chatml.md)，这种结构化的格式使模型能够区分各种信息类型，如system prompt、user input和bot response。

数据构造过程中
- 采用`WizardLM`方法获取难度较高提示的数据集，采用`LIMA`中回复风格（总-分-总）对生成回复内容格式化，采用“`Step-Back`”模式对维链数据格式化。
- 同时为了减少幻觉和重复，检查并确保回复中的知识不包含在模型中，消除可能导致模型死记硬背的回复，并重写回复保证微调多轮时数据不重复。

同时
- 为了确保**模型能力覆盖**范围，微调数据中涉及多种任务，例如：问答、创意写作、对话、推理、数学、编码、双语能力等。
- 为了增加模型的**精细控制能力**，设计了一套系统指令，通过多样性的采样算法，平衡各种系统指令上的数据分布，增强的跨任务鲁棒性。
- 为了探索不同任务数据比例，对模型最终能力的影响，通过**网格搜索**方法，确定最终数据混合比例。

最后，微调数据采用`ChatML`格式，让模型可以更好地区分输入中各类型信息，例如：`系统指令`、`用户输入`和`模型回复`。

### 模型结构

涉及 分词器、模型结构及微调参数

#### 分词器

Tokenizer 采用 sentencepece 中 BPE方法对预训练数据训练得来，为平衡计算效率和词理解能力将词表设置为**64000**，将数字拆分为单个数字，将罕见字符用**unicode编码**。

tokenizer
- 用 BPE，词表大小为64000，平衡了计算效率和表达能力；
- 其中数字全是单个的digit，让模型能更好地理解数字数据；
- 对于OOV的词，会降级用unicode编码 ；
- 保留全角标点符号，不转为半角；

另外，优先考虑英语的LLM在tokenizer会使用虚拟前缀（文本开头的空格）来泛化句子不同位置相同的单词。Yi不这么做，因为即使是在英语语境中，这种假设并不总是成立，比如对于以引号开头的句子，而且在中文语境中，这么做没有明显效果。

#### 模型

模型 Transformer-Decoder 结构，基于标准LLAMA2模型，修改如下：
- **注意力机制**：LLAMA2只在70B用了GQA，Yi全系列都用了GQA
  - Yi-6B和34B版本均采用 Grouped-Query Attention(GQA)，Llama2 中仅70B版本采用GQA。
- **激活函数**：Yi采用`SwiGLU`作为后注意力层的激活函数。
  - 参考《GLU Variants Improve Transformer》
- **位置编码**：Yi模型采用**旋转位置编码**（`RoPE`），为例支持200k上下文窗口，调整了基础频率（RoPE ABF）。
  - 参考 RoPE ABF（《Effective long-context scaling of foundation models》），base扩大到10M，用于支持长上下文。


模型微调阶段
- **仅计算回复内容的损失**，不考虑系统指令和用户指令。
- 采用AdamW优化器，其中β1、β2和ϵ分别为0.9、0.999和1e−8。
- 训练数据最大长度为4096，批量大小为64，训练300步，学习率恒定为1e−5，权重衰减为0.1，梯度裁剪最大阈值为1.0，并采用NEFTune方式训练，Yi-34B-Chat和Yi-6B-Chat噪声尺度分别为45和5。

### 训练


#### Infra

从数据处理到模型训练都需要大集群大算力的支持。

Yi构建了支持全栈数据处理、预训练、微调和服务的基础设施。包括：
- (1) 自动管理和监控计算资源的能力；
- (2) 通过优化并行策略、内核效率和长上下文支持提高训练速度；
- (3) 统一微调框架，支持异构分布式训练后端，例如在DPO中同时使用Megatron和DeepSpeed进行多个模型的训练；
- (4) 通过各种LLM服务加速技术（如量化、continuous batching 和 paged attention）降低部署成本。

这部分工作还是很多的，比如
- 由于经常有硬件坏，坏的硬件会被自动从资源池移除；
- 任务失败时，会自动跟踪重启。
- 给算法人员考法UI等。

#### 预训练 

预训练 pretrain
- 训了4k基础模型。（暂时没有给出更多细节）


#### 微调

微调超参如下

```py
AdamW：beta=[0.9,0.999]，epsilon = 1e-8
seq_len = 4096
batch size = 64
constant lr = 1e-5，weight decay = 0.1
gradient clip = 1.0
max step = 300
```

参考
- 《Neftune: Noisy embeddings improve instruction finetuning》
- 对于6B模型 noise scale = 5，对于34B模型 noise scale = 45


### 评测

基模型评测

#### 基础能力评测

对其他开源模型，保持和公开的设置相同做法获取结果。Yi使用贪婪解码，没有进行任何后处理
- 数学和代码能力上，和GPT3.5、GPT4还存在一些差距，而这些能力是可以通过继续预训练和微调来持续提升的。Yi最初的设计并没有针对这些能力，因此没有在预训练数据中包含特别多相关数据，后续会有计划增加这部分能力的提升。
- 而和其他开源模型相比，在代码和数学以外的任务，Yi基本上做到了跟大一倍模型的效果相近，甚至更好的水平。

**观察**
- 模型规模带来的增益：尽管Yi-34B和Yi-6B使用了相同的预训练语料，但Yi-34B的性能相比Yi-6B有了质的提升。
  - 更大的模型尺寸在代码和数学基准测试上带来了明显的增益。
- 数据质量：高质量预训练数据的小型模型，如Yi-34B或Qwen-14B，通常表现优于尺寸更大但（可能）数据质量较低的模型，例如Falcon-180B。
- GPT-4与开源LLM差距：
  - 开源LLM在多种基准测试上的性能仍然落后于GPT-4和GPT-3.5。
  - 然而，具有代表性的双语LLM，例如Qwen-14B和Yi-34B，在包括C-Eval、CMMLU和Gaokao在内的中文知识相关基准测试上匹配甚至超过GPT-4的性能。然而，在BBH、代码（HumanEval）和数学（MATH）等推理相关基准测试上，仍然存在巨大差距。

**In-Context Learning 能力**

Yi进一步研究了in-context learning能力，即根据少数展示的输入-输出示例，推断underlying function的能力。

任务是**推断加权**和的**线性系数**。
- 定义 `y = w1x1 + w2x2 + ... + wnxn`。

少量示例展示是 x1, x2, ..., xn, y，要求模型预测给定一组新输入 x 的 y。

这就要求模型隐式地推断出 w1, w2, ..., wn。

评测上，使用（a）模型预测的 y 与真实值 y∗ 之间的绝对差，即 `|y − y∗|` 作为连续度量，以及使用（b）精确匹配 y == y∗ 作为不连续度量。

模型在算术上的效果正常，因此可以认为这样的测试不受算术能力的影响，而能直接看模型是否具备根据给定的实例进行underlying function推理的能力。

实验发现，当问题比较简单时（系数是`[1,-1]`），Yi-34B和LLAMA-70B效果比较好（看下图）。

当问题更复杂点（系数是`[1，1，1，1，1]`），只有LLAMA-70B和Mistral 8*7B这样的大模型表现出了涌现的能力。


#### Chat 模型评测

自动评测
- 评测任务和base模型相同，分别采用zero-shot和few-shot，效果依然不错

报告强调，如Goodhart’s principle所说
- 当一个指标变成目标，就不再是一个好指标。
- 因此这里的测试只是为了确认微调没有使得模型的知识能力下降，而不会专门去针对任务做优化。

结果上，Yi-34B-Chat数学能力不错，而Yi-6B-Chat并没有展现出强大的数学能力。推测较小的模型可能需要更多的数据在SFT阶段激活其相应的能力。

人工评测

### 能力扩展

#### 上下文扩展

扩展模型上下文长度

对于长上下文的解决方法：采用**继续预训练**和**微调**两种方法
- 基础模型其实本身已经存在利用200K输入上下文中任何位置信息的前来，继续预训练可以“解锁”这种能力，通过微调可以进一步调整生成内容的风格以更好地遵循人类指令和偏好。

预训练阶段：
- 采用**序列并行**和**分布式注意力**方式蛮力对模型全部注意力进行训练。

数据来源：
- （1）原始预训练数据；
- （2）长上下文数据，主要来自数据；
- （3）多文档文档合成数据。共计对5B Token的数据进行训练，批次大小为4M Token。


微调阶段：
- 将短SFT数据与长上下文问答问答数据**混合**使用。文档问答数据由模型辅助构建，即随机将多个文档拼成一个长文档，从中抽取一个或多个段落，要求模型基于抽取段落内容构建问答对。
- Trick，要求给答案之前模型需要背诵或改写原始段落，这种数据格式鼓励模型进行检索，从而阻止依赖自身知识回答产生的幻觉。


#### 多模态

ViT部分由CLIP ViT-H/14 model初始化，后面的transformer由Yi-Chat初始化

3步训练：
- （1）使用224^2的图像来训练ViT和projection模块的参数。这一训练利用了包含1亿个图像-文本对的数据集，这些数据来自LAION-400M。主要目标是增强ViT在架构中的知识获取能力，并实现ViT与LLM之间更好的对齐。
- （2）将ViT图像分辨率提升到448^2，目的是进一步推动模型识别复杂视觉细节的能力。在这个阶段使用的数据集包括从LAION-400M中提取的2000万个图像-文本对。此外，还融入了来自不同来源的大约480万个图像-文本对，例如CLLaVA、LLaVAR、Flickr、VQAv2、RefCOCO、Visual7w等。
- （3）整个模型的参数一起训练。主要目标是提高模型在多模态聊天交互方面的熟练度，从而赋予它能够无缝融合和解释视觉与语言输入的能力。为此，训练数据集涵盖了多种来源，总共大约有100万张图像-文本对，包括GQA、VizWiz VQA、TextCaps、OCR-VQA、Visual Genome、ShareGPT4V等等。为了确保数据平衡，对任何单一来源的最大数据量设定了上限，将其限制在不超过50,000对。

使用128张A100，6B训了3天，34B训10天。


#### 扩展模型深度 Depth Upscaling

目标是把32层的6B扩展到48层的9B模型。
- 参考《Scaling large language models with simple yet effective depth up-scaling》，通过复制中间的12-28层共16层，把层数扩展为48层。

参考SOLAR 10.7B模型对Yi-6B模型进行深度扩展，将原来的32层扩展到48层，构建Yi-9B模型。在具体层的选择时，通过评估每一层输入和输出直接的余弦相似度得出，余弦相似度越接近于1，则表明复制这些层不会显著改变原始模型输出的logits，因此选择复制原始模型中间12-28的16个层。

采用两阶段训练
- 第一阶段使用了0.4T数据（包含文本和代码），数据配比与Yi-6B模型一样；
- 第二阶段使用了0.4T数据（包含文本、代码和数学），重点增加了代码与数学数据的比例，以提高代码性能。

在微调过程中
- 设定了一个固定的学习率 3e-5，并采取逐步增加 batch size 的策略，即从 batch size 4M token 开始，每当模型 loss 停止下降时就增加 batch size，使 loss 继续下降，让模型学习更加充分，收敛性能更好。



## 【2024-4-22】MiniCPM


【2024-4-22】[MiniCPM：揭示端侧大语言模型的无限潜力](https://shengdinghu.notion.site/MiniCPM-c805a17c5c8046398914e47f0542095a)
- [MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies](https://arxiv.org/abs/2404.06395) (arxiv.org)

[MiniCPM](https://github.com/OpenBMB/MiniCPM) 是一系列端侧语言大模型，主体语言模型 `MiniCPM-2B` 具有2.4B的非词嵌入参数量。
- 综合性榜单上与Mistral-7B相近（中文、数学、代码能力更优），整体性能超越Llama2-13B、MPT-30B、Falcon-40B等模型。
- 当前最接近用户体感的榜单MTBench上，MiniCPM-2B也超越了Llama2-70B-Chat、Vicuna-33B、Mistral-7B-Instruct-v0.1、Zephyr-7B-alpha等众多代表性开源大模型。


### 超参调优

Hyper-parameters、Batch size、Learning Rate、Learning Rate Scheduler、Data Strategy 五个方面模型沙盒研究。

近400次在0.009B模型规模上的贝叶斯参数搜索得到

超参数对模型的性能具有重大影响
- 传统训练方法要对每个模型进行超参数调整，这对于大模型并不现实。

借鉴 uP 方法，对模型各参数模块之间进行了连接权重的调整、以及对模型初始化的调整。部分调整接近Cerebras-GPT。

| 名称 | 具体操作 |
| --- | --- |
| Embedding Output Scaling | 将Embedding的输出乘12 |
| Residual Connection Scaling | 将每层的残差连接处的增量放缩为 1.4/sqrt(num_layers) = 0.22 倍 |
| Initialization of Tensors | 将每个二维的张量参数的初始化标准差设置为 0.1/sqrt(dim_model/256) = 0.033，其他参数初始化设置为0.1 |
| Learning Rate Scaling of Tensors | 将每个二维的张量参数的学习率调整为其他部分学习率（或称整体学习率）的1/(dim_model/256) = 0.11倍 |
| lm_head Scaling | 将输出logits调整为原来的0.11倍 |


#### batch size

Batchsize 随损失变化: 更大的Batchsize可能可达到更低的loss
- 扩大Batchsize 时, 损失会有一次较大幅度的下降

2020年, OpenAI 开山之作研究了**损失函数**随**token数**变化的规律: 消耗更多的步数等价于消耗更多的时间

在这种假设下，OpenAI定义了`临界Batchsize`（Critical Batchsize），使得达到一定的损失，既不消耗过多step，也不消耗过多token。

然而利用当前以A100为主的计算资源，结合gradient checkpointing策略进行训练时，通常**计算速度**（而不是显存）是**瓶颈**
- 相同机器数量下，<span style='color:red'>多一倍 Batchsize 几乎等同于慢一倍的单步时间</span>。

基于这个观察，取消了对“不消耗过多step”的追求，而转向追求用最少的token量达到最低的loss。

0.009B，0.036B，0.17B的模型上分别进行了6个batchsize的训练实验
- ![](https://shengdinghu.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F30c36155-a603-469f-957f-b0854b6e2372%2F0086e773-a7c6-4e94-aa08-84c7a1936ff2%2FUntitled.png?table=block&id=a5bbe015-1311-440a-b284-e49a95583065&spaceId=30c36155-a603-469f-957f-b0854b6e2372&width=770&userId=&cache=v2)
- `log(BS) = -6.24 * log(L) + 20.91`

最优batchsize随着C4数据集上的loss的偏移规律
- 规律: <span style='color:red'> BS = 1.211 * 10^9 / L^6.2393 </span>
- 预估: 2B模型达到C4损失2.5左右，4M是比较合适的Batchsize

#### learning rate

模型最关键超参数:学习率

**lr 不会因为模型规模扩大有大幅度的改变**

0.04B, 0.1B, 0.3B, 0.5B 上分别做了6组学习率实验，发现虽然模型大小扩大了10倍，但是**最优学习率偏移并不明显**，均在`0.01`左右
- 在 2.1B 规模上进行了简单验证，发现在 0.01 的学习率确实能取得最低的Loss。
- ![](https://shengdinghu.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F30c36155-a603-469f-957f-b0854b6e2372%2F44a3d57c-6131-4c93-8ddd-7d7f718b110f%2Floss_vs_lr.png?table=block&id=0a9c1f96-0a98-40d5-8cf6-f192dd97cf55&spaceId=30c36155-a603-469f-957f-b0854b6e2372&width=1060&userId=&cache=v2)

#### lr 调度策略

<span style='color:red'>不同训练阶段使用不同学习率的调整策略，对模型性能影响很关键</span>。

当前通用的学习率策略是**Cosine图像**，即 学习率从 Warmup阶段升高到最高点之后，开始呈现余弦函数的降低。
- 几乎所有大模型都使用了 Cosine Learning Rate Scheduler (简称Cosine LRS）的方式。

为什么 Cosine Scheduler 表现优异？

对0.036B的模型，设置不同的Learning Rate Scheduler的截止步数$T$，进行了持续训练。
- ![](https://shengdinghu.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F30c36155-a603-469f-957f-b0854b6e2372%2F44dbc039-68b0-4a17-88ae-10f2939eeece%2FUntitled.png?table=block&id=0a274cda-127e-4c4a-9e15-6f9cc504972a&spaceId=30c36155-a603-469f-957f-b0854b6e2372&width=2000&userId=&cache=v2)
- 对于训练至 S 步的模型，将 <span style='color:blue'>Cosine LRS 截止步数 T 设置为 S 步, 总是能获得最优的性能</span>，而设置为更多或者更少性能都不是最优。

**持续训练**场景会发现 Cosine调度器有问题。
- 如果在Cosine的截止步数之后, 继续沿用0.1倍的最大学习率（通常做法），则继续训练**收敛非常缓慢**；
- 如果在Cosine的截止步数之后, 重启Cosine LRS（即再次从最大学习率开始下降，或者是逐渐上升到最大学习率，再开始下降）则损失会经历长时间的上升周期，而这段时间，模型处于**不可用状态**。

猜想 Cosine LRS 在预先指定步数的时候性能优异原因：
1. T=S下的Cosine LRS，相对于Linear LRS、Noam LRS、以及`T<S`的Cosine LRS，有更长时间的大学习率训练。这一阶段可能有助于模型寻找更好的全局最优解。
2. T=S下的Cosine LRS ，相对于`T>S`的Cosine LRS、Constant LRS，有更充分的学习率下降的退火阶段，这一阶段可能发生了较为特别的动力学现象，导致模型可以找到更好的局部最优解。

结合这两点，提出了一种新的学习率调度策略，`Warmup-Stable-Decay`（`WSD`）调度器。
- 公式见原文
- Cosine调度器结束后, 需要持续保持**最低学习率**，以保证loss不上升
- 而WSD调度器则从退火(decay)前开始继续用**最大学习率**训练，经过更长的训练再开始退火

这种学习率调度器分为三个阶段: 
- `warmup`阶段（用W表示warmup阶段结束时的步数/训练量）
- `稳定训练`阶段（用S表示稳定训练阶段结束时的步数/训练量）
- `退火`阶段（用D表示退火阶段的训练量）
  - 随着学习率的变小，损失有大幅度的快速下降，在步数S时迅速降低至和T=S的Cosine LRS相等或更低
- ![](https://shengdinghu.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F30c36155-a603-469f-957f-b0854b6e2372%2Fb837e282-7a3c-47dd-aca5-7aac4b5c072f%2FUntitled.png?table=block&id=cd4faecf-079e-4c2f-a3b8-0c6cbeaf099b&spaceId=30c36155-a603-469f-957f-b0854b6e2372&width=2000&userId=&cache=v2)

WSD好处：
1. 可以持续训练。
2. 可以随时取出。
3. 性能优于Cosine LRS。
4. 有显式区分的训练阶段，便于使用不同的数据策略。


#### 数据策略

结合训练阶段特点，使用不同类型的数据
- 预训练阶段: 只用通用、量大的预训练**粗质量**数据
- 退火阶段: 用非常广泛的**高质量知识和能力**数据以及SFT的高质量数据，混合入预训练数据进行退火。

实验结果
- 退火开始时加入高质量数据的收益远高于在退火完成后的sft阶段加入。

因此, 建议模型能力的特化和增强应从退火阶段开始进行。


## 【2024-5-7】DeepSeek

详见站内专题: [DeepSeek](deepseek)


## 训练经验


### OOM

【2024-4-11】 OOM
- 单机单卡(V100S,32G)
- InternLM2-1.8B, 7.1G
- 数据集: 231m

报错
> torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate `7.04` GiB. GPU 0 has a total capacty of `31.75` GiB of which `5.04` GiB is free. Process 743134 has `26.71` GiB memory in use. Of the allocated memory `25.01` GiB is allocated by PyTorch, and 342.98 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting `max_split_size_mb` to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF

deepspeed 配置

```sh
deepspeed --master_port 30001 ./llm/training/conversation_reward/main.py \
   --max_seq_len 2048 \
   --per_device_train_batch_size 2 \
   --per_device_eval_batch_size 2 \
   --weight_decay 0.01 \
   --dropout 0.0 \
   --gradient_accumulation_steps 1 \
   --zero_stage 2 \
   --dtype bf16 \
   --num_train_epochs 10 \
   --train_data_path /mnt/bn/flow-algo-cn/wangqiwen/session_process/data/train/cut_train_sequence_en_20240331.csv \
   --val_data_path /mnt/bn/flow-algo-cn/wangqiwen/session_process/data/test/cut_test_0322_es_sequence_v2.csv \
   --test_data_path /mnt/bn/flow-algo-cn/wangqiwen/session_process/data/test/cut_test_0322_en_sequence_v2.csv \
   --model_name_or_path /mnt/bn/flow-algo-cn/yufeng/ModelHub/internlm2-1_8b \
   --output_dir /mnt/bn/flow-algo-cn/wangqiwen/model/checkpoints \
   --debug \
   --deepspeed
```

解决
- 设置GPU缓存碎片 → 无效
- 改用 A100(80G) → 有效

```sh
--max_split_size_mb 32  # 无效
```

# 结束
