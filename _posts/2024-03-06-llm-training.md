---
layout: post
title:  LLM 大模型训练之路
date:   2024-03-06 12:00:00
categories: 大模型
tags: ChatGPT 训练
excerpt: 大模型训练原理，如何训练，有什么经验？
mathjax: true
permalink: /llm_train
---

* content
{:toc}


# LLM 大模型训练之路


## LLM 训练模式

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


微调方法
- 微调方法分为**全参数微调**（Full Fine-tuning）、**部分参数微调**（Repurposing）
- 全微调方法：SFT
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


### （1） 第一步 SFT（全参数微调）

SFT 原理比较简单，难的是数据问题，需要大量的有监督Prompt文本
- ![img](https://pic3.zhimg.com/80/v2-45331e791fad76d81694bd61e806db8a_1440w.webp)
- Transformer【左】GPT【右】

大模型训练**基座模型**时，都采用「Next Token Prediction，`NTP`」 任务

#### IFT 的问题

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


### （2）第二步 RM训练

**奖励模型**（Reward Model, RM）目标是刻画模型的输出是否在人类看来表现不错。
- 输入: \[提示(prompt)，模型生成的文本\] 
- 输出: 一个刻画文本质量的标量数字。
- ![](https://pic2.zhimg.com/80/v2-51ad9f0f11ba272611a068d380e7fe41_1440w.webp)

同一个prompt输出的多个答案，人工评测排序后，使用lambdarank的思想，优化RM奖励模型。

RM模型学习的就是对于一个prompt，人类对答案的喜好程度。
- RM模型【左】RM损失函数【右】
- ![](https://pic3.zhimg.com/80/v2-6b22d510b56efc300b6bb1686407a40e_1440w.webp)
- ![rm](https://pic1.zhimg.com/v2-bc1af700e9147ae7458824f5619b1ed4_b.jpg)

奖励模型接收一系列文本并返回一个标量奖励，数值上对应人的偏好

引入RM模型的作用是对生成的文本进行打分排序，让模型生成的结果更加符合人类的日常理解习惯，更加符合人们想要的答案。

RM模型主要分为两个部分：数据获取和模型训练。流程如下图所示
- ![](https://pic2.zhimg.com/80/v2-ac62759c2862ab04a024d51fe2a19991_1440w.webp)

原论文中使用GPT架构做了一个reward model

注意
- 要将模型的输出映射成维度为1的**打分向量**，即增加一个linear结构。

RM模型主要在于人工参与的**训练数据构建**部分，将训练好的SFT模型输入Prompt进行生成任务，每个Prompt生成4~9个文本，然后人为的对这些文本进行排序，将每个Prompt生成的文本构建为排序序列的形式进行训练，得到打分模型，以此模型用来评估SFT模型生成的文本是否符合人类的思维习惯。

两种方法命名为 direct score 和 rank score：
- `Direct score`：一个是直接对输出的文本进行打分，通过与自定义的label score计算loss，以此来更新模型参数；
- `Rank score`：二是使用排序的方法，对每个Prompt输出的n个句子进行排序作为输入，通过计算排序在前面的句子与排序在后面的句子的差值累加作为最终loss。

【2023-6-5】[ChatGPT 为什么不用 Reward-Model 的数据直接 fine-tune，而用 RL？](https://www.zhihu.com/question/596230048/answer/3055888005)
- Reward-model的输出对于整个token序列，一种滞后反馈，而finetune需要在每个token都有监督信号。这是强化学习与监督学习的差别。
- 生成Reward-model的数据有些是结果对比较**pair数据**，没法直接用于监督学习finetune。

#### ① Direct score方法

① Direct score方法
- 利用 Bert模型对标注数据进行编码，用 linear层 映射到1维，然后利用Sigmoid函数输出每个句子的得分，与人工标记的得分进行loss计算，以此来更新模型参数。流程如下所示
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


#### 人工标注平台

【2023-8-15】排序数据集 标注 参考：[RLHF](https://github.com/HarderThenHarder/transformers_tasks/tree/main/RLHF)
- ![](https://github.com/HarderThenHarder/transformers_tasks/blob/main/RLHF/assets/rank_list_labler.png)




### （3）第三步 PPO

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

利用SFT模型对输出进行改造，构造一个**双头PPO模型**，模型一头输出一个张量，代表生成序列每个元素的价值value；另一头将输出映射成prompt answer词典答案。[参考](https://zhuanlan.zhihu.com/p/618325377)
- 将 `<prompt, prompt answer>` 输入到RM模型中，获得一个评估当前prompt对的奖励R，然后用R作为奖励，反向更新每个元素的价值value，这就是PPO强化学习算法。
- ![img](https://pic4.zhimg.com/80/v2-b7872ef00df9809f0d3632896add3e73_1440w.webp)
- ![rlhf](https://pic3.zhimg.com/v2-6fbb088189db4a8991ca2d476092552a_b.jpg)
- Y=0, 常规 PPO
- Y>=, PPO_ptx


#### RL+LM研究方向

由于InstructGPT效果太好，RL+LM这个新范式能衍生出哪些研究方向？
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




# 结束