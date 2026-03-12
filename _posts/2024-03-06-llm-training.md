---
layout: post
title:  大模型训练原理
date:   2024-03-06 12:00:00
categories: 大模型
tags: 训练 罗福莉 lora 微调
excerpt: 大模型训练原理，如何训练，有什么经验？
mathjax: true
permalink: /llm_train
---

* content
{:toc}

# LLM 大模型训练原理

大模型主要有 数据、训练、推理部署、大模型应用四个方面

## 训练资源&案例

详见站内专题: [大模型训练资源+案例](llm_train_case)

## 训练阶段

- 【2024-9-12】[llm 论文淘金](https://zhuanlan.zhihu.com/p/719626313?utm_psn=1885030923797525376)
- 项目地址：[awesome-llm-pretraining](https://github.com/RUCAIBox/awesome-llm-pretraining) 大模型训练资源

【2025-12-21】[预训练、微调和RL对于推理语言模型作用](https://zhuanlan.zhihu.com/p/1986175442093380683)
- 【2025-12-8】CMU 论文 [On the Interplay of Pre-Training, Mid-Training, and RL on Reasoning Language Models](https://arxiv.org/abs/2512.07783)

训练阶段：
- `预训练`：先博览群书，学习海量的基础知识（学生先读完图书馆里所有的书）。
- `微调训练`：在博览群书的基础上，再集中做一批练习题（高考前的专题复习）。
- `强化学习`（RL）：最后请名师，每次解题时，不是只看最终答案对不对，还会点评解题步骤是否清晰、合理，并据此给予奖励或指正。 那么，这位高手最后解题能力的提升，到底是因为名师（RL）的指点真让他“开了窍”，还是只是把之前博览群书和专题复习时学过的东西，在名师面前“更好地发挥”了出来？

LIMA 等论文
- CPT `预训练`学**知识**
- SFT `指令微调`学**格式**
- RL `强化学习`**对齐人类偏好**

要想大模型有**领域知识**，得`增量预训练`。`指令微调`记知识不靠谱，不是几十 w 条数据能做到的

训练模式图解 [知乎](https://zhuanlan.zhihu.com/p/24868371543)

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



分析
- RL并非万能，只在“能力边缘”生效
  - RL真正提升模型能力（不只是激发旧知识）前提：① 预训练后模型还有进步空间；② RL训练数据正好落在模型“能力边缘”
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

概念三：能力边缘（Edge of Competence）—— 跳一跳能够得着的难度
- 通俗理解：指那些对模型来说有点难，但努力一下又能解决的任务。太简单的任务学不到新东西，太难的又会直接放弃。
- 生活比喻：你健身时，选择一个重量，让你能标准地完成8-12次，最后几下比较吃力。这个重量就是你的“边缘”，最能有效增长肌肉。如果重量太轻（太简单）或太重（太难），效果都不好。



### 经验总结

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

SFT 相对于RAG，能得到更好的垂域效果、推理速度延迟低、精度上限更高

SFT 全称 supervised Finetune 微调， 微调本质是**模仿**。
- 预训练是 next token prediction 的自监督学习
- SFT 是 next token prediction 的监督学习
- 二者反馈粒度都是token。对于监督学习而言，通常不存在学不会，但存在不会泛化

如何从文档中构建训练数据集，通过简单的SFT技术促进新知识学习？

SFT 主要步骤：
1. 数据收集：收集大量的标注数据，由人类专家根据特定任务进行标注。
2. 模型训练：对预训练模型进行微调，特定任务上表现更好。
3. 评估和优化：通过验证集评估模型性能，并根据结果进行优化。

SFT 优点是相对简单直接，只需要高质量的标注数据即可。

详见站内专题: [微调新方法](llm_finetune_new)

#### 如何保证微调效果？

在数据 和 训练策略这两个维度上优化。

(1) 微调数据上，质量大于数量、人机协同、利用大模型做好数据生成、数据增强、数据质量评估和清洗。

微调最大的成本是数据成本，数据质量决定微调后模型的质量。

预训练数据和SFT数据有什么不同？
- SFT数据不够 max_seq_length 部分会自动补零
- 但预训练数据很少存在补零的数据填充。

(2) 训练策略

通过多种训练策略的优化。
- 模型评测数据集至关重要，优化模型的第一步是建立benchmark，构建benchmark时不仅要构建垂域的benchmark，也要在通用能力的benchmark上去测试。
- checkpoint的选择。微调核心达到一个平衡, 即通用能力尽可能不降低情况下提升其垂域能力，epoch number选择很重要。
  - 通常epoch number大小和数据量相关，数据量大时epoch个数选择要小，数据量小时epoch个数选择要大。
  - 备注：和之前训练普通的CNN模型是一致的，数据量越大，收敛的epoch个数越小。checkpoint选择不仅可以根据epoch来选择也可以通过step来选择。
- 模型训练调参技巧，通常包括batch size和梯度累积、learning rate（大模型选择小学习率的原因是平衡收敛速度和稳定性+一般选择使用预训练的1/10）、warm up等。
- 训练框架默认将CoT部分和答案部分的token loss比重相同，因此在训练时，把标注去掉直接输出答案，效果有时可能会更好。

3个维度评价：有用性、准确性、逻辑一致性。
- 有用性就是对客户本身有没有用？
- 准确性就是看有没有明显错误？
- 逻辑一致性就是看问答一致性和模型回答内容的前后一致性。

评价对象分为人工评价、大模型评价、可解析的评价数据集-将主观问题转换为客观回答的选择题或判断题来回答。


#### SFT 问题

然而，SFT也有一些局限性，比如
- 对标注数据的质量和数量要求较高。

问题
- 大模型遗忘。通用能力下降。
- 幻觉。微调通常会加大模型的幻觉。并不是只有微调之后才会造成幻觉，正常的大模型也会存在幻觉，而微调有可能加大幻觉。
- 过拟合。在专业领域效果提升明显，但泛化能力显著降低。过拟合学习到的是死记硬背，而不是方法论。

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

### CPT

行业观点
- 美团CPT：懂业务、守规则、有温度的专家。
- 清华"AGI-Next"峰会：垂直领域Agent 落地最大的坑不是“模型不够聪明”，而是不够**稳定**。
  - 垂直专业领域 + 多工具调用 + 多轮对话Agent形态下，这条路卡在“稳定性”上。
  - 为了解决不稳定，上下文越做越长、链路越做越复杂，优化很难系统化复用。基于qwen3 8B + SFT（学习领域知识、业务流程） + DPO（对齐工具调用偏好），对工具使用的准确率从34.8%提升到97.3%
  - 以对话为核心的“chat”范式已告终结，AI 竞争转向“能办事”的智能体时代。 
- DeepMind强化学习研究员Ronak Malde：2024是agent之年，2025是RL之年，2026将是持续学习的一年。
- OpenAI O1 erry Tworek 创业，剑指「持续学习」。

#### CPT 定义

CPT（Continued Pre-Training，继续预训练）
- 通过**无标注**数据进行无监督继续预训练，强化或新增模型特定能力。

持续预训练在已经预训练好的大语言模型基础上，继续使用特定数据和任务进行预训练的过程。

目的：进一步提升模型在特定领域或任务上的性能，或者使模型能够适应新的数据集和应用场景，训练更好的大语言模型的重要组成部分。

作用
- 增强**领域适应性**：不同领域有其独特的语言风格、专业术语和知识结构。持续预训练让模型更好地理解和处理特定领域的文本数据
  - 例如在医学领域，能使模型更准确地理解医学文献、病历等；在法律领域，能更好地处理法律条文、案例分析等。
- 提升**特定任务性能**：针对具体任务，如文本生成、问答系统、机器翻译等，持续预训练根据任务特点对模型进行优化，使模型在这些任务上的表现更出色。
- 缓解**灾难性遗忘**：当模型在新领域或数据训练时，可能会忘记之前在其他领域或任务上学习到的知识。持续预训练可以通过合理地选择训练数据和方法，在学习新知识的同时，尽量保留模型原有的通用能力，避免灾难性遗忘。

数据要求
- 大量文本数据(通常几GB到几十GB)数据质量要高，最好是你目标领域的专业内容

适用场景
- 让模型学习特定领域的知识，比如医学、法律、金融
- 增强模型对某种语言或方言的理解
- 让模型熟悉你所在行业的专业术语

#### D-CPT Law

特定领域持续预训练（Domain-specific Continual Pre-Training，D-CPT）的Scaling Law，即 D-CPT Law。
- 在特定领域持续预训练场景下，验证集损失L关于模型大小N、数据集大小D和混合比r的关系。
- 确定不同规模大模型在可接受的训练成本下，通用语料库和垂直领域语料库之间的最佳数据配比。


#### Agent CPT

【2025-9-17】阿里通义实验室提出“Agentic CPT”框架，通过CPT为智能体行为构建预先对齐的强基础模型，而非完全依赖后期的微调。
- 论文 [Agentic CPT：Scaling Agents via Continual Pre-training](https://arxiv.org/pdf/2509.13310)

动机：base model距离agent存在SFT/RL不好解决的鸿沟

现象：
- 当对大模型实施智能体对齐时，当前后训练方法，包括监督微调（SFT）和强化学习（RL），效果有限，特别是在开源实现中。
- 在BrowseComp等具有挑战性的基准测试上，即使是领先的开源智能体模型，如WebSailor（12.0分）、GLM-4.5（26.4分）和DeepSeek-V3.1（30.0分），与OpenAI的deepresearch（51.5分）相比也表现出显著性能差距。

原因：
- 可能的解释：SFT、RL这些方法都依赖于通用基础模型，如Qwen2.5-72B，这构成了关键瓶颈。
- 通用基础模型缺乏“智能体归纳偏置”，导致后续对齐阶段必须同时学习“能力”与“行为”两种异质目标，引发根本性的优化冲突，从而限制了智能体性能。

解法：
- 首次将“智能体能力”前移到预训练阶段，提出 Agentic Continual Pre-training（Agentic CPT） 范式，
- 通过大规模离线合成数据在基础模型中预先植入**工具调用**、**多步推理与决策探索**等智能体行为模式，得到“已对智能体任务预对齐”的基础模型。

<img width="600" height="100%" alt="image" src="https://github.com/user-attachments/assets/3f3318a6-2d23-455f-8099-fe0ab4531dbf" />

结果：
- 后续仅需轻量 SFT/RL 即可释放性能，显著缩小甚至反超闭源模型在 BrowseComp、GAIA、HLE 等 10 项基准上的差距。

做法：
- 离线合成“智能体原生数据”+2阶段训练

从Qwen预训练基础模型（例如Qwen3-30B-A3B-Base）开始，该增强训练流水线包括：
- 智能体CPT阶段1：处理约200B token的智能体数据和知识推理语料库，使用32K上下文长度，遵循next token+交叉熵损失训练范式。该阶段实现智能体行为的初步获取，包括工具调用模式和多步推理链。
- 智能体CPT阶段2：进一步使用100B token精心策划的高质量智能体数据完善这些能力，采用扩展的128K上下文窗口，使LLM能够深入理解复杂动作空间和长期规划策略




### 持续学习

论文
- 【2024-2-7】莫纳什大学 论文 [Continual Learning for Large Language Models: A Survey](https://arxiv.org/pdf/2402.01364.pdf)，【2024-2-14】[综述：大语言模型的持续学习](https://zhuanlan.zhihu.com/p/681583249)

【2024-11-25】罗格斯大学+谷歌云AI研究院综述论文 [Continual Learning of Large Language Models: A Comprehensive Survey](https://arxiv.org/pdf/2404.16789), 引用 莫纳什大学论文，进一步将持续学习划分为：垂直持续学习、水平持续学习

持续预训练（CPT）、持续指令调整（CIT）和持续对齐（CA）三个阶段

|阶段|概念|目的|
|---|---|---|
| 增量预训练 (Continual Pre-Training, CPT)| 在供应商端，利用新收集的大规模无标签数据和现有数据对模型进行持续训练。| 应对时间偏移。大模型不再是死板的百科全书，通过CPT，它能吃掉最新的时政新闻、科技进展和语言演变。这是模型保持“活性”的基础。|
| 领域自适应预训练 (Domain-Adaptive Pre-training, DAP)| 针对特定领域（如医疗、法律、代码）的无标签数据进行专项训练。| 应对空间迁移。这是赋予大模型“灵魂”的关键一步。它不再只是“泛泛而谈”，而是开始理解行业黑话、逻辑范式和专业知识。|
| 持续微调 (Continual Fine-Tuning, CFT)| 在消费端（应用层），针对具体任务进行连续的指令微调（SFT）和对齐（RLHF）。| 提高任务成功率和输出质量。如果说 CPT 和 DAP 是在给大模型‘灌注海量知识’，那么CFT就是在规范它的‘表达方式’，让它知道如何把脑子里的东西转化成用户想要的答案。|

持续学习分类
- vertical continuity（持续性） 垂直持续学习：transition from large-scale general domains to smaller-scale specific domains 从大规模通用领域迁移到小规模特定领域
  - 分为几个阶段，Continual Pre-Training (CPT), Domain-Adaptive Pre-training (DAP), and Continual Fine-Tuning (CFT)
  - 示例：医疗机构会将通用大模型适配到特定医疗领域
- Horizontal continuity 水平持续学习：在时间、领域之间继续适应  continual adaptation across time
  - 示例：社交媒体最新趋势随时间变化，社交平台持续更新广告推荐模型
and domains

大语言模型持续预训练与微调的高层级概述，两个维度连续性：
- 垂直连续性（垂直持续学习）：LLM 训练过程可垂直划分为三个阶段，即（1）持续预训练（CPT）、（2）领域适配预训练（DAP）、（3）持续微调（CFT）。该维度的核心关注点是保留模型的通用知识，即防止垂直遗忘。
- 水平连续性（水平持续学习）：LLM 完成部署后，当新的数据集可用时，需对模型进行持续更新。该维度的首要目标是，在一系列连续的任务中防止水平遗忘

<img width="900" height="100%" alt="image" src="https://github.com/user-attachments/assets/02bdfa6b-501e-43c0-8339-8047a73eb996" />

同样，灾难遗忘也分：
- Vertical Forgetting 垂直遗忘
  - 挑战：任务异构（冻结参数/重塑下游任务）、上游数据无法获取（使用公开数据/生成伪样本）
- Horizontal Forgetting 水平遗忘
  - 挑战：长任务序列（数据分布随时间漂移→持续模型集成）、突发分布漂移（）

<img width="900" height="100%" alt="image" src="https://github.com/user-attachments/assets/4c77b352-d7b8-4fe8-8da2-0d1896acea6b" />


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



# 结束
