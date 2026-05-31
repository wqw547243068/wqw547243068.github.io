---
layout: post
title:  自动研究Agent（Auto Research）专题
date:   2026-03-07 16:52:00
categories: 大模型
tags: autoresearch ak47 skill
excerpt: 自研研究Agent：让Agent自己调参、训模型，找到最佳参数
mathjax: true
permalink: /autoresearch
---

* content
{:toc}


# AutoResearch

2026年3月某个清晨，Karpathy 在 X 上发了推文：
> "ah yes, this is what post-AGI feels like"

- AI Agent 在他睡觉的 12 小时里，自主提交了 110 次代码变更，把语言模型验证损失从 0.862415 一路压到 0.858039。
- 而 Karpathy 本人呢？去蒸桑拿了。

2026年3月7日，这套方法论打包成仅 630 行代码的开源项目——autoresearch，扔到GitHub 上。48 小时内揽星 9500，截至发文已突破 33k。

这件事之所以炸裂，不在于技术多复杂，而是触及根本问题：
> AI 能不能自己搞科研？搞出来的东西到底靠不靠谱？

上一代 AutoML 见站内专题：[AutoML](automl)

## 背景

完整的模型实验流程繁琐：
1. 在 arXiv 上刷论文，找相关方法
2. 顺着引用图追溯数据集和基础技术
3. 在 Hugging Face Hub 上搜索合适的数据集，检查数据质量
4. 写训练脚本，配置环境
5. 提交计算任务，盯着 GPU 跑
6. 分析实验结果，排查 reward collapse 等问题
7. 调整策略，反复迭代

这一套流程走下来，即使是经验丰富的研究员，往往也要花费数天甚至更长时间。


## 发展史

时间轴
- 2025 年 10 月：nanochat 项目发布（初始 commit 10 月 13 日）。
- 2026 年 1 月底：推出 “Time to GPT-2” leaderboard，初始记录约 3.04 小时。
- 2026 年 2 月：手动调优（数据集、FP8 等），基准降至约 2 小时。
- 2026 年 2 月 27 日：公开多代理实验尝试（8 agents，tmux 交互式），但当时未成功。
- 2026 年 3 月 5 日：首次宣布 AI 代理已自主迭代 nanochat（12 小时内完成 110 次改动，val loss 从 0.862415 降至 0.858039），称“I'll just leave this running for a while, go relax a bit and enjoy the feeling of post-agi”。并指出新 meta 是“what is the research org agent code that produces improvements on nanochat the fastest?”
- 2026 年 3 月 7 日：发布 autoresearch 极简仓库（单 GPU、单文件 ~630 行 train.py）。
- 2026 年 3 月 6–8 日：启动首次正式实验，在 depth=12 模型上运行约 2 天（~650–700 次实验）。
- 2026 年 3 月 8 日：初步确认改进可转移至 depth=24 模型。
- 2026 年 3 月 9 日：手动验证所有改动并测量最终结果。

Autoresearch 专题详见飞书文档：[autoresearch](https://my.feishu.cn/wiki/TJXhwcj6wivSrLkdU9jc0Uren4f)


## 介绍


【2026-3-15】[Autoresearch 深度解读：Karpathy 的"AI 自主科研"到底有没有戏？](https://zhuanlan.zhihu.com/p/2016489903790236699)

Karpathy 用 630 行代码搭"AI 研究员"的最小可行原型——让 Agent 在你睡觉时自动改代码、跑实验、筛结果，一晚上干完人类一周的活

一个"永不下班的实习生"
- 给定研究方向的说明书（program.md）
- 开始不停改代码、跑实验、看结果、决定保留还是丢弃，然后继续下一轮。
- 整个过程完全自主，不需要人类干预。

## 效果

经过两天持续自动调优，autoresearch 处理了约 700 次自主更改，发现了约 20 个可迁移的改进，将 "Time to GPT-2" 指标（nanochat社区基准）从 2.02 小时缩短到 1.80 小时——效率提升 11%。

保留率大约 18%
- Agent 每 5-6 次尝试才能找到有效改进。
- 合理，人类做实验的成功率也差不多。


成功的尝试

排名第一的发现很有意思：
- 固定时间预算下，把 batch size 减半反而更好。直觉上 batch size 越大、梯度越稳，效果应该越好。
- 但 Agent 发现反直觉事实：5 分钟约束下，小 batch 更多的训练步数（更多参数更新），这比"每步梯度更新"带来的收益更大。

社区用户 snowkcon 证实
- 一个月前用完全不同的计算设置也独立发现了同样的规律。
- Agent 用一晚上重新发现了这个 insight。

| 排名 | 改进描述 | val_bpb 下降 | 备注 |
| :--- | :--- | :--- | :--- |
| 1 | 批量大小从 524K 减半到 262K（更多训练步数） | -0.0119 | 收益最高，通过降低批次大小、增加训练步数提升泛化能力 |
| 2 | 深度 9，宽高比 57（增加一层 Transformer） | -0.0043 | 模型规模扩展，增加网络深度，提升表达能力 |
| 3 | 嵌入层学习率从 0.6 提高到 0.8 | -0.0033 | 针对嵌入层的精细调优，加快词向量学习速度 |
| 4 | RoPE 基础频率从 10K 提高到 200K | -0.0012 | 位置编码参数调整，优化长上下文建模效果 |
| 5 | Unembedding 学习率从 0.004 调到 0.006 | -0.001 | 输出层学习率微调，提升预测层收敛效率 |
| 6 | 值嵌入添加微小权重衰减 0.001 | -0.001 | 正则化策略，抑制过拟合，增强模型泛化性 |
| 7 | 短窗口设为 1/8 上下文（256 tokens） | -0.0009 | 注意力窗口策略调整，优化局部依赖建模 |


失败的尝试
- 大模型文献中广泛采用**权重共享**（embedding 和 unembedding 共享参数）
- 但在这个小模型、短训练的场景下，带来了 +2.24 BPB 的灾难性退化。
- 提醒：很多 ML "最佳实践"是有上下文的，Agent 不迷信教条，纯粹用数据说话。

| 失败尝试 | val_bpb 变化 | 点评 |
| :--- | :--- | :--- |
| 权重共享（weight tying） | 2.24 | 直接爆炸，完全失效 |
| 并行注意力+MLP | 0.011 | 在小模型上不 work |
| 多查询注意力 MQA（n_kv_head=1） | 0.008 | 过于激进的压缩 |
| 移除 careful WD mask | 0.005 | 说明精细的正则化掩码很重要 |
| 5% warmup | 0.0008 | 在本次运行中反而有害 |

反常识结论
1. 所有参数施加权重衰减
  - PyTorch 官方建议：不要对 bias、layernorm、embedding 参数施加权重衰减。
  - 但 Agent 发现：对嵌入层加 0.001 的微小权重衰减，对值嵌入（Value Embeddings）加 0.001-0.003 的权重衰减，都能带来实打实的改进。
  - 不过这里有个狭窄的最优区间：VE 权重衰减到 0.005 就开始变差了。这就像调盐一样——一点就好，多了就咸。
  - GitHub 用户 aniruddhaadak80 评论说："通常 folklore 建议排除 biases 和 layernorms 的权重衰减，但 Agent 发现打破这个规则有实证效果——这非常有趣。" 自动化实验的价值：不会被先入为主的偏见束缚。
2. 初始化缩放有"甜点"
  - Agent 逐步测试 Transformer 初始化缩放比例：0.8x → 0.7x → 0.68x 都在改善，但到 0.66x 和 0.65x 就开始退化了。
  - 最终锁定 0.68x 为甜点。这种精细的网格搜索，人类研究员通常没耐心做到这么细。
3. 高嵌入层学习率 + 正则化
  - 当嵌入层加上了权重衰减（正则化）后，更高的学习率（从 0.6 → 0.8 → 0.9）反而更好。这形成了一个有趣的相互作用：正则化"兜底"，所以可以放心给更大的学习率。


## 架构

### 文件

设计上极简，只有 3个文件，像实验室的权限管理
- `prepare.py` 是实验室的基础设施（水电气、仪器），不允许任何人动；
- `train.py` 是实验台上的东西，研究员可以随便折腾；
- `program.md` 是 PI（导师）写的研究计划书，决定这个实验室的研究方向。

| 文件 | 角色 | 谁来改 | 功能 |
| :--- | :--- | :--- | :--- |
| `prepare.py` | 基础设施 | 没人改 | 数据下载、BPE 分词器训练、数据加载器、评估函数 |
| `train.py` | 实验对象 | AI Agent 改 | GPT 模型定义、优化器（Muon + AdamW）、训练循环 |
| `program.md` | 研究指令 | 人类改 | 给 Agent 的行为指南，定义实验规则和策略 |


### 工作流

工作流是无限循环：

```sh
while True:
    1. 读取当前 train.py 和实验历史
    2. 形成改进假设（比如"把学习率调高试试"）
    3. 修改 train.py
    4. git commit（留痕）
    5. 运行训练（严格 5 分钟）
    6. 检查验证损失（val_bpb）
    7. if 改进 → 保留 commit，更新基线
       else → git reset，回退到上一个好的版本
    8. 记录结果到 results.tsv
    9. 继续下一轮
```




<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;dark-mode&quot;:&quot;auto&quot;,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot;&gt;\n  &lt;diagram name=\&quot;AI意图识别商用方案\&quot; id=\&quot;osbHtP6Ki7KAK-vxM0vi\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;17988\&quot; dy=\&quot;13874\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-1\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;strokeWidth=2;fontSize=18;\&quot; value=\&quot;读取program.md\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;175\&quot; x=\&quot;-15957.5\&quot; y=\&quot;-12050\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-2\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=2;fontSize=18;\&quot; value=\&quot;修改train.py\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;175\&quot; x=\&quot;-15957.5\&quot; y=\&quot;-11950\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-3\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;strokeWidth=2;fontSize=18;\&quot; value=\&quot;运行5分钟训练\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;170\&quot; x=\&quot;-15955\&quot; y=\&quot;-11850\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-4\&quot; parent=\&quot;1\&quot; style=\&quot;rhombus;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;strokeWidth=2;fontSize=18;fontColor=#ffffff;\&quot; value=\&quot;val_bpb是否改善?\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;90\&quot; width=\&quot;220\&quot; x=\&quot;-15980\&quot; y=\&quot;-11750\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-5\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;strokeWidth=2;fontSize=18;\&quot; value=\&quot;保留变更\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;130\&quot; x=\&quot;-15935\&quot; y=\&quot;-11610\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-6\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;fontSize=18;\&quot; value=\&quot;已改善\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;80\&quot; x=\&quot;-15870\&quot; y=\&quot;-11640\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-7\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;strokeWidth=2;fontSize=18;\&quot; value=\&quot;回滚变更\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;110\&quot; x=\&quot;-16150\&quot; y=\&quot;-11610\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-8\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;fontSize=18;\&quot; value=\&quot;未改善\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;80\&quot; x=\&quot;-16080\&quot; y=\&quot;-11740\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-9\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;strokeWidth=2;fontSize=18;\&quot; value=\&quot;规划下一个实验\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;160\&quot; x=\&quot;-15950\&quot; y=\&quot;-11500\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-10\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;4ILE4oa1Rdl2tyf0Z6mL-1\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;strokeColor=#333333;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=18;\&quot; target=\&quot;4ILE4oa1Rdl2tyf0Z6mL-2\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-15920\&quot; y=\&quot;-11990\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-15920\&quot; y=\&quot;-11950\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-11\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;4ILE4oa1Rdl2tyf0Z6mL-2\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;strokeColor=#333333;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;fontSize=18;\&quot; target=\&quot;4ILE4oa1Rdl2tyf0Z6mL-3\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-15920\&quot; y=\&quot;-11890\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-15920\&quot; y=\&quot;-11850\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-12\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;4ILE4oa1Rdl2tyf0Z6mL-3\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;strokeColor=#333333;exitX=0.5;exitY=1;exitDx=0;exitDy=0;fontSize=18;\&quot; target=\&quot;4ILE4oa1Rdl2tyf0Z6mL-4\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-15920\&quot; y=\&quot;-11790\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-15920\&quot; y=\&quot;-11750\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-13\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;4ILE4oa1Rdl2tyf0Z6mL-4\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;strokeColor=#333333;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=18;\&quot; target=\&quot;4ILE4oa1Rdl2tyf0Z6mL-5\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-15995\&quot; y=\&quot;-11650\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-16160\&quot; y=\&quot;-11550\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-14\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;4ILE4oa1Rdl2tyf0Z6mL-4\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;strokeColor=#333333;exitX=0;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;fontSize=18;\&quot; target=\&quot;4ILE4oa1Rdl2tyf0Z6mL-7\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-15845\&quot; y=\&quot;-11650\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-15780\&quot; y=\&quot;-11550\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-15\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;4ILE4oa1Rdl2tyf0Z6mL-5\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;strokeColor=#333333;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=18;\&quot; target=\&quot;4ILE4oa1Rdl2tyf0Z6mL-9\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-16160\&quot; y=\&quot;-11490\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-15920\&quot; y=\&quot;-11450\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-16\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;4ILE4oa1Rdl2tyf0Z6mL-7\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;strokeColor=#333333;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;fontSize=18;\&quot; target=\&quot;4ILE4oa1Rdl2tyf0Z6mL-9\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-15780\&quot; y=\&quot;-11490\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-15920\&quot; y=\&quot;-11450\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-17\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;4ILE4oa1Rdl2tyf0Z6mL-9\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;strokeColor=#333333;entryX=1;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;exitDx=0;exitDy=0;fontSize=18;\&quot; target=\&quot;4ILE4oa1Rdl2tyf0Z6mL-2\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;-15870\&quot; y=\&quot;-11390\&quot; /&gt;\n              &lt;mxPoint x=\&quot;-15690\&quot; y=\&quot;-11390\&quot; /&gt;\n              &lt;mxPoint x=\&quot;-15690\&quot; y=\&quot;-11920\&quot; /&gt;\n            &lt;/Array&gt;\n            &lt;mxPoint x=\&quot;-15920\&quot; y=\&quot;-11390\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-15770\&quot; y=\&quot;-11890\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;700\&quot; y=\&quot;180\&quot; as=\&quot;waypoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;4ILE4oa1Rdl2tyf0Z6mL-18\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=24;\&quot; value=\&quot;Atuo Research 流程\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;260\&quot; x=\&quot;-15990\&quot; y=\&quot;-12110\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



Agent 拿到3样东西：`program.md`（任务说明）、当前版本的 `train.py`（要改的文件）、历史实验结果（哪些改动有效）。

然后在 train.py 里面乱改：

```py
n_layer = 12      # 层数，随便改
n_head = 12       # 注意力头数
n_embd = 768      # 隐藏维度

optimizer = Muon(model.parameters(), lr=0.001)  # 也可以换 AdamW

batch_size = 64
learning_rate = 3e-4
dropout = 0.1
```

评估用 bits per byte (bpb)，越低越好。这个指标跟模型大小没关系，所以不同架构之间可以直接比——对自动化探索来说刚好合适。

总结
- **深度优先搜索**，对初始参数敏感
- **对决策模型强依赖**：能力强、窗口大，如 claude code或codex

详见原文：[Autoresearch 深度解读：Karpathy 的"AI 自主科研"到底有没有戏？](https://zhuanlan.zhihu.com/p/2016489903790236699)

## 实践


代码

```sh
# 1. 克隆仓库
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch
# 2. 安装依赖
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
# 3. 准备数据（约 2 分钟）
uv run prepare.py
# 4. 手动跑一次基线实验（约 5 分钟）
uv run train.py
# 5. 启动 AI Agent（以 Claude 为例）
# 在你的 AI 编程助手中指向这个仓库，然后说：
# "Hi have a look at program.md and let's kick off a new experiment!"
```

Mac 用户可用社区移植版

```sh
git clone https://github.com/trevin-creator/autoresearch-mlx.git
```




## 进化版


### 总结


| 方案 | 目标 | 搜索空间 | Agent | 评估标准 | 代码量 | 硬件 | 特色 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| autoresearch（Karpathy） | 优化小模型的训练配置 | 代码级（改 train.py） | Claude/Codex 等编程 Agent | val_bpb（单一数值） | 630 行 | 单 GPU | 极简、可复现、教育价值高 |
| AI Scientist v2（Sakana AI） | 端到端自动论文生产 | 全流程（想法→实验→写论文） | LLM 驱动的端到端系统 | 同行评审分数 | 大型系统 | 多 GPU | 首次在 ICLR 发表 AI 生成论文（评审分 6/7/6） |
| AutoML/NAS（传统） | 自动搜索模型架构/超参 | 架构/超参空间 | 无 Agent，纯优化算法 | accuracy/loss | 框架级（数万行） | 多 GPU 集群 | 工业成熟度高 |
| Hyperspace AI（分布式 autoresearch） | 分布式 Agent 协作优化 | 代码级 + 多节点 | 多 Agent P2P 网络 | val_bpb | 扩展自 autoresearch | 分布式网络 | GossipSub 协议传播策略 |


### AI Scientist v2：另一个极端

Sakana AI 的 AI Scientist v2 完全不同：不只是调超参，而是试图完成从"提出假设"到"写论文"再到"同行评审"的全流程。
-  ICLR 2025 Workshop 上成功发表了完全由 AI 生成的论文，评审打分 6/7/6，超过了人类论文的平均水平。
但设计哲学截然相反：
- AI Scientist 追求广度（覆盖研究全流程）
- autoresearch 追求深度（在一个极小的空间里把实验做透）。
Karpathy 的选择更"工程师"——与其做万能但能力平平的系统，不如在可控的沙盒里证明"自主实验循环"这个概念本身可行。


### 【2026-3-9】Hyperspace 分布式

【2026-3-9】[Hyperspace](https://agents.hyper.space/) 首个**分布式**通用人工智能（AGI）系统。
- 数千个自主 AI 智能体协同训练模型，通过点对点（P2P）闲聊协议共享实验成果，并在此推动技术突破。
- 完全点对点架构。可通过浏览器或命令行终端（CLI）接入参与。
- github项目 [hyperspaceai](https://github.com/hyperspaceai/agi)

Hyperspace AI 的 Varun Mathur 把 autoresearch 单 Agent 循环扩展到点对点网络。多个节点上的 Agent 各自做实验，通过 GossipSub 协议实时共享有效策略。

结果惊人：
- 不同硬件上的 Agent 发展出了完全不同的策略——高性能 GPU 节点倾向于"暴力破解"（堆参数量），而 CPU 节点被迫在初始化策略上更"聪明"（比如尝试 Kaiming 和 Xavier 初始化）。
- 当一个节点发现 Kaiming 初始化使损失下降 21% 时，这个策略"像病毒一样"在网络中传播。
仅用 17 小时，分布式 Agent 就独立重新发现了人类实验室花费 8 年才正式化的里程碑（如 RMSNorm、绑定嵌入等）。


### 【2026-5-19】AutoResearchClaw

【2026-5-19】[北卡罗来纳大学 推出 AutoResearchClaw 多智能体自动研究框架](https://arxiv.org/abs/2605.20025)
- [AutoResearchClaw: Self-Reinforcing Autonomous Research with Human-AI Collaboration](https://arxiv.org/pdf/2605.20025v1)
- Github: [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw)

AutoResearchClaw 突破现有系统线性流程局限的多智能体自主研究系统。

AutoResearchClaw 把输入端直接拉到“一个原始研究想法”。
- 用户只需在命令行输入一行 CLI 命令，附上 idea，比如“探索新型注意力机制在长上下文建模中的效率”
- 系统就会启动一个 23 阶段的端到端流水线，覆盖 8 个主要阶段：从 idea scoping、文献发现、合成，到实验设计、执行、分析、写作和最终定稿。

五大机制：
- 结构化多智能体辩论用于假设生成与分析；
- 具备自修复能力的执行器可将失败转化为信息；
- 可验证的结果报告防止数据伪造与引用幻觉；
- 提供从全自动到逐步监督的七种人机协作模式；
- 以及能将过往经验转化为未来保障的跨运行进化能力。

实验表明，该系统性能显著优于基线模型，且精准、定向的人机协作模式始终优于完全自主或穷举式监督。它被定位为一种增强而非取代人类科研判断力的研究放大器。

### ml-intern

【2026-4-24】[资讯](https://mp.weixin.qq.com/s/N1yYp9Zd9jhxwnA-2ejecg)

Hugging Face 开源会自己训练模型的 AI 员工，彻底颠覆 ML 研究工作流
- 只需要一句话，自己去读论文、找数据集、写代码、跑训练，还会自己复盘和改进。

常规实验流程：
1. 在 arXiv 上刷论文，找相关方法
2. 顺着引用图追溯数据集和基础技术
3. 在 Hugging Face Hub 上搜索合适的数据集，检查数据质量
4. 写训练脚本，配置环境
5. 提交计算任务，盯着 GPU 跑
6. 分析实验结果，排查 reward collapse 等问题
7. 调整策略，反复迭代

即使是经验丰富的研究员，往往也要花费数天甚至更长时间。

#### 介绍

Hugging Face 把这整个流程，交给 AI 代理来自动完成。

2026 年 4 月开源自主 ML 工程代理（Autonomous ML Agent）ml-intern。
- 项目地址：[ml-intern](https://github.com/huggingface/ml-intern)，在线体验：[ml-intern](https://huggingface.co/spaces/smolagents/ml-intern)
- 给定训练目标，自主完成从文献调研到模型发布的完整 ML 工作流。

基于 Hugging Face 自家的 smolagents 框架构建，深度集成了整个 HF 生态——Hub 仓库、数据集、文档系统、云计算（HF Jobs）以及实验追踪工具 Trackio。
- 底层框架： smolagents（HF 官方 Agent 框架）
- 接口设计： 接口无关，CLI 和 Web UI 共享同一套 Agent 核心
- 通信机制： 异步队列架构（submission_queue + event_queue）
- 实验追踪： Trackio（HF 原生，开源 W&B 替代方案）
- 云计算集成： HF Jobs（一键提交到 HF 的 GPU 算力池）
-  依赖： fastmcp、fastapi、rich、nbconvert 等

ml-intern 内置面向 ML 工作流的专用工具：

| 工具 | 功能 |
| --- | --- |
| Research Tool | 爬取 arXiv、HF Papers，遍历引用图 |
| HF Jobs Tool | 提交 GPU 训练任务（支持 A100/H100） |
| Sandbox Tool | 本地安全执行 Python 脚本 |
| Dataset Tool | 搜索、检查、格式化 HF Hub 数据集 |
| Docs Tool | 查询 HF 生态文档（transformers、TRL 等） |
| GitHub Tool | 检索相关代码实现参考 |

#### 原理

核心工作循环（三阶段工作流）

```sh
用户输入一个目标
    ↓
① Research（研究）
   · 爬取 arXiv / HF Papers
   · 阅读论文方法章节
   · 遍历引用图谱
    ↓
② Plan & Validate（规划与验证）
   · 拆解任务
   · 搜索 HF Hub 上的数据集
   · 检查数据质量与可用算力
    ↓
③ Implement（实现）
   · 编写训练脚本
   · 通过 HF Jobs 提交到 GPU 集群
   · 读取评估结果，诊断失败
   · 自动重训，直到性能提升
```

这不是一次性执行，而是持续闭环迭代，直到达成目标。

#### 效果

ml-intern 在 PostTrainBench 测试（图宾根大学与马克斯·普朗克研究所），单张 H100 GPU 上的 10 小时内 对基础模型完成后训练。

测试结果令人震惊：
- ml-intern 用仅 1.7B 参数的小模型，在 3 小时内就突破了 27.5%，最终达到 32%
- 不仅大幅超越了 Claude Code，还逼近了使用更大模型（4B）的 SOTA。

这种"数据效率"正是自动化代理的核心优势所在。

| 对比方 | GPQA 得分 |
| --- | --- |
| Qwen3-1.7B 基线 | ~10% |
| Claude Code | 22.99% |
| ml-intern（Qwen3-1.7B） | 32% |
| PostTrainBench SOTA（Gemma-3-4B） | 33% |

#### 应用

案例一：合成数据生成（医疗领域）对医疗领域模型进行微调时，ml-intern：
1. 评估了 HF Hub 上现有医疗数据集的质量
2. 判断数据质量不足，无法支撑可靠的微调
3. 自主编写脚本生成合成训练数据，重点覆盖边缘案例，包括医疗不确定性语言和多语种急救响应场景
4. 对这些数据进行上采样，增强训练分布
5. 在 HealthBench 上评估效果
这种"发现问题→自主解决"的能力，是传统自动化脚本无法做到的。

案例二：自主 RLHF（数学推理领域）在数学推理优化任务中，ml-intern：
1. 自主选定了 GRPO（Group Relative Policy Optimization） 算法——相比标准 PPO 更节省显存
2. 编写完整的 GRPO 训练脚本
3. 在 A100 GPU 上启动训练，实时监控 reward 曲线
4. 进行消融实验（ablation），隔离有效组件
5. 确定最终 checkpoint

#### 安装

三种方式

方式一：在线体验（零门槛）

```
# 直接访问 HF Spaces：
https://huggingface.co/spaces/smolagents/ml-intern
```

输入你的 ML 目标，即可开始。

方式二：本地 CLI 安装

环境要求： Python 3.10+，HuggingFace 账号

安装步骤：

```sh
# 1. 克隆仓库
git clone git@github.com:huggingface/ml-intern.git
cd ml-intern
# 2. 安装依赖
pip install -e .
# 3. 登录 HF 账号（用于访问 Hub 和 HF Jobs）
huggingface-cli login
# 4. 启动交互式 CLI
ml-intern
```

CLI 支持两种模式：
- 交互模式：完整的对话环境，支持 /undo、/model 等斜杠命令
- 无头模式（Headless）：单次 prompt 执行，适合自动化流水线集成

方式三：Web UI（本地部署）

项目内置了 FastAPI 后端 + React 前端，支持本地部署 Web 界面：

```sh
# 启动 Web 后端
cd web && uvicorn app:app --reload
# 启动前端（另开终端）
cd frontend && npm install && npm run dev
```

Web UI 功能更丰富，包括：
- 实时流式展示代理的思考过程和工具调用日志
- 代码编辑器，用于在提交前审查训练脚本
- 可视化计划追踪，实时看到任务执行进度
- 硬件费用实时显示，让你在提交付费计算任务前心里有数


### 【2026-5-27】DeliAutoResearch SKILL

【2026-5-27】[DeepSeek陈德里开发自动研究Skill，写一篇论文人类只动脑2小时](https://zhuanlan.zhihu.com/p/2042892227588904782)

DeepSeek 研究员陈德里在X上发布第二篇论文聚焦持续学习与自我迭代

DeliAutoResearch SKILL 系统从6分跃升至8分，人工干预大幅减少，自主性显著增强。
- 论文共迭代6次（V1：4 次，V2：1 次，V3：1 次），总耗时6天，进行了约108轮Agent调用，消耗64.8万token，写了2234行LaTeX代码。
- 103个参考文献，全部已验证。论文现为46页，538KB，含7个图表+4个表格。

论文提出三轴统一框架、形式化收敛条件，并指出六大开放挑战，为AGI时代的学习范式指明方向。

自动研究智能体L1–L5自主度分类体系
- L1: 最基础的自动补全，最早的GitHub Copilot，预测下一行代码。
- L2: 任务执行，ChatGPT/Claude聊天机器人加上各种工具，能分解任务，但每步都得人类批准。
- L3: **多步骤**执行，目前最主流 Claude Code、Cursor Agent这种，能自主执行10到100步，只在关键点请求人类审核
- L4: **受限领域内**全自主执行，人类仅提供研究目标、评估最终成果，智能体可完成多步实验、代码、论文撰写，但无法自主选择研究问题。
- L5: **完全**自定研究议程，智能体可自主选题、分配资源、长期积累知识、跨领域持续研究，是当前未实现的理想状态，核心瓶颈为持续知识积累、可靠自我评估、架构规模化。

目前行业前沿初步达到L4，L5还只是个设想。真正的瓶颈不是模型能力，而是「持续知识积累」和「可靠自我评估」。

Code Agent 导致计算机科学论文数量疯狂膨胀，同样的工作以前至少需要一个月才能完成。

![](https://pic4.zhimg.com/v2-72e564246c29e689e17439ab2c630c63_1440w.jpg)





# 结束

