---
layout: post
title:  美团大模型：龙猫（LongCat）
date:   2025-10-15 18:31:00
categories: 大模型
tags: 美团 龙猫 longcat 客服
excerpt: 美团大模型专题
mathjax: true
permalink: /longcat
---

* content
{:toc}


# LongCat 模型

资料：
- 论文：[Higher Satisfaction, Lower Cost: A Technical Report on How LLMs Revolutionize Meituan’s Intelligent Interaction Systems](https://arxiv.org/pdf/2510.13291)
- [美团大模型革新智能交互ppt](https://bcnqea2fvkqt.feishu.cn/slides/HK01sCyYOlEp2cdnJItcxQAAnCh)
- 飞书文档 [美团技术分享：Wowservice](https://my.feishu.cn/wiki/Hke0wGP3CiXrbGk6BVwcw9SbnCf)

## 龙猫（LongCat）介绍

美团龙猫（LongCat）大模型发展历程完整表格

| 时间节点 | 事件/版本 | 核心内容 | 里程碑意义 |
|----------|-----------|----------|------------|
| 2023年 | 项目启动 | 美团正式启动自研大语言模型LongCat（龙猫）的研发工作，同步启动国产算力适配与技术预研 | 美团大模型战略的起点，为后续全栈自研奠定基础 |
| 2025年3月 | 内部研发成果公开 | 美团CEO王兴公开表示，美团已开发完成内部大语言模型LongCat，核心研发进展首次对外披露 | 龙猫模型首次进入公众视野，确认美团自研大模型的战略布局 |
| 2025年6月10日 | 首款落地产品发布 | 美团正式发布首款AI编程智能体产品NoCode，集成了美团自研千亿参数规模的LongCat模型 | 龙猫模型首次对外落地，完成从内部研发到产品化的第一步 |
| 2025年9月1日 | 首款正式版模型发布&开源 | 美团正式发布大模型**LongCat-Flash-Chat（龙猫）**，总参数5600亿（MoE架构，激活参数186-313亿），在GitHub、Hugging Face平台开源，同步上线官方网站longcat.ai | 美团首款正式对外发布的通用大模型，标志着美团正式加入开源大模型赛道，核心能力聚焦智能体、代码场景 |
| 2025年9月中旬 | 原生AI应用落地 | 美团推出主打生活服务的AI原生应用「小美APP」，全面接入LongCat模型能力，支持点外卖、订酒店、规划出行等全场景生活服务 | 龙猫模型首次深度融入美团核心本地生活业务，完成大模型与业务场景的深度适配 |
| 2026年2月6日 | 轻量化开源模型发布 | 美团推出开源模型**LongCat-Flash-Lite**，主打智能体、代码场景优化，进一步降低模型部署与使用门槛 | 完善龙猫模型的产品矩阵，覆盖从超大规模到轻量化的全场景需求 |
| 2026年4月24日 | 2.0版本预览版开放测试 | 美团基础大模型**LongCat-2.0-Preview**开放测试，用户可通过官网申请免费测试名额，训练推理全程依托中国国产算力集群完成 | 龙猫2.0版本首次对外亮相，核心突破国产算力全流程适配，为正式版发布完成灰度验证 |
| 2026年6月30日 | 2.0正式版发布&全面开源 | 美团正式发布新一代基础大模型**LongCat-2.0（龙猫2.0）**，总参数量1.6万亿，是国内首个基于5万张国产算力卡集群完成预训练及推理全流程的大型语言模型，原生支持1M超长上下文，聚焦智能体与代码场景优化 | 国产大模型里程碑事件，实现万亿参数大模型与国产算力的深度适配，刷新了国产算力集群训练大模型的规模纪录 |

补充说明
1.  龙猫（LongCat）是美团全栈自研的大语言模型系列，核心技术路线聚焦**MoE混合专家架构、国产算力适配、智能体/代码场景深度优化**，区别于通用大模型的全能力覆盖，更侧重业务场景的落地效率与成本控制。
2.  截至2026年7月，龙猫系列模型已完成从研发到产品化、从闭源到全开源、从英伟达算力到国产算力全流程适配的完整发展路径，是国内少数实现全栈自研+全场景落地的大模型系列。


## 【2025-06-10】LongCat-1.0

待定

## 【2025-10-15】WOWService

论文：[Higher Satisfaction, Lower Cost: A Technical Report on How LLMs Revolutionize Meituan’s Intelligent Interaction Systems](https://arxiv.org/pdf/2510.13291)


## 【2026-6-30】LongCat-2.0

【2026-6-30】[LongCat-2.0 正式发布](https://longcat.chat/blog/longcat-2.0/)

美团发布并开源 LongCat-2.0，总参数量达 1.6 万亿、每个 token 激活约 480 亿参数的 MoE 语言模型。

LongCat-2.0 相比此前的 LongCat 系列引入了多项架构改进，实现了模型能力的显著跃升。
- LongCat-2.0 完整训练流程与大规模部署均**全部使用国产算力集群**。
- 预训练在5万余国产算力芯片上耗时月余完成，消费了超过 35 万亿 tokens，全程无回滚、无不可恢复的 loss 突刺。
- 这一结果验证了有能力在国产算力平台上进行前沿级大规模模型训练。

为了让每个参数发挥更大价值，加入 N-gram Embedding 模块，通过 N-gram token 组合将 embedding 空间扩展超过 100 倍，以更充分地建模局部上下文信息，并提升 token 级表示能力。

LongCat-2.0 深度适配 Claude Code、OpenClaw、Hermes 等主流 Harness，在代码理解、仓库级修改、自动化任务执行及 Agentic Workflow 等多元场景中表现出色，能够为开发者带来更稳定、更高效的智能协作体验。

### 效果

LongCat-2.0 
- 优势在代码和搜索：SWE-bench Pro 超过了 Gemini 3.1 Pro 和 GPT-5.5，RWSearch 超过了所有对比模型。（长上下文处理和 Agent 能力上的投入大）
- 在基础科学推理（GPQA-diamond）和指令遵循（IFEval）上，与 Gemini 3.1 Pro 和 GPT-5.5 还有差距。
取舍的结果：资源有限，优先把长上下文和 Agent 能力做到最好。

### 国产GPU

LongCat-2.0 训练与部署构建在超过 5 万张国产算力芯片组成的大规模集群之上。

5 万片国产芯片、35 万亿 token、全程无回滚，这组数字的含义不只是"模型训练成功了"，而是"这套工程体系在生产环境里被验证可行了"。

与成熟的 Nvidia GPU 生态相比，其配套的软件社区仍欠发达。为此，投入了大量精力来打造稳定、安全且可扩展的基础设施，训练吞吐提升超过 35%。

国产算力芯片单片显存显著小于 H800 的 80GB，显存成为大规模训练的主要瓶颈。

优化策略：
- 6D 并行： 在常规 TP/CP/EP/DP/PP 之外，额外引入 EMBP 对 N-gram Embedding 做并行加速。
- 超节点： 训练运行在物理超节点上，每个超节点最多 48 台机器，节点内全互联高带宽、节点间走 RoCE 网络。超节点把高带宽通信域扩展到数百张卡，支撑带宽敏感的并行策略（TP/CP/EP）。相比同规模下，超节点额外带来约 30% 的预训练吞吐提升。逻辑超节点同时是亲和调度的基本单元，在通信局部性与可调度性之间取得平衡。
- 显存优化： 采用 ZeRO-1、选择性重计算、分配器层的显存超限（OOM）时自动卸载，并将填充词元路由至零计算专家等。
- Muon 优化器： 在国产算力芯片上大规模部署 Muon 优化器，围绕 TP 并行、DP 状态去冗余及高效对称矩阵乘核函数等关键路径做专项优化。

并行方式有 5 个维度：
- TP（张量并行）：把单个矩阵运算切开，分到多张卡上算
- CP（上下文并行）：把长序列切开，分到多张卡上处理
- EP（专家并行）：把不同的专家放在不同的卡上
- DP（数据并行）：多张卡同时处理不同的数据
- PP（流水线并行）：把模型的不同层放在不同的卡上，像流水线一样运转

LongCat-2.0 在这 5 个维度之外，额外加了第 6 个：EMBP（Embedding 并行），专门处理 135B N-gram Embedding 参数的并行加速。

大规模长上下文训练：
- LSA 算子与前向优化： 为 LSA 预热和稀疏两阶段训练自研确定性注意力算子及 KL 损失算子。LSA 预热采用 forward-only 训练策略，仅需一次前向即可同时得到 KL 损失与梯度，从而提升训练效率。
- 百万上下文长度扩展： 采用 all-gather 的上下文并行方式，可将上下文并行扩展至 512 路以上，实现原生百万上下文长度数据的训练。数据在预取阶段重新打散，并采用均衡的序列切分策略以保持负载均衡。
- 计算通信重叠： 我们精心设计了计算与通信的重叠，例如 ScMoE 结构使 MoE 通信与并行分支计算重叠，同时 LSA 的 top-k 索引计算与 KV all-gather 重叠，降低同步开销。

显存容量、显存 I/O 带宽与互联带宽都较为受限的条件下，在万亿参数大模型上跑百万上下文的推理是一项不小的挑战。

显存优化手段：
- ZeRO-1：优化器（负责更新参数的模块）的状态数据，往往比模型本身还大。ZeRO-1 把这些状态数据切分到多张卡上，每张卡只存一部分。
- 选择性重计算：正向计算时，有些中间结果可以不存下来，反向传播时重新算一遍。这样牺牲一点计算时间，换来大量显存节省。
- OOM 自动卸载：当显存快满了（Out of Memory），自动把部分数据卸载到内存或硬盘，用时再取回来。
- 零计算专家：填充 token（用来凑齐序列长度的无意义 token）被路由到一个"零计算专家"，不做任何实际计算，节省算力。


为此，在模型、设备与部署三个层面进行了一系列优化。
- 模型层面优化
  - Attention: 为了高效应对超长上下文带来的 I/O、计算及显存瓶颈，我们通过三种方式对系统进行了优化。
  - (1) 引入 absorb 计算模式应用于 prefill 和 decode 阶段；
  - (2) 将 indexer 与 MLA prolog 做了并行处理，使 indexer 的一部分开销可以被 MLA 计算所掩盖；
  - (3) 借助 KV-cache 并行 (KVP) 将 KV-cache 切分到多片卡上。
  - ScMoE: 基于 LongCat-Flash 中 dense 与 MoE 分支的计算-通信重叠机制，LongCat-2.0 利用国产计算芯片的控核能力做了进一步的调度优化——通过主动分配 dense 流和 MoE 流的核心数量，使得 dense 与 MoE 的执行可以完全并行，而不局限于计算与通信的并行。

面向国产算力芯片的优化
- Super Kernel: 开启图模式后，算子之间的空隙得以消除，但每个算子内部的启动开销依然存在。为此，引入 super kernel 来减小算子数量，从而降低算子的总启动开销。
- Weight Prefetch: Longcat-2.0 使用的国产算力芯片的显存带宽有限，但 L2 cache 相对较大。正是利用这块较大的 L2 cache 提前预取权重，将 I/O 延迟隐藏在前一个算子的计算之中。
- Scale Up 与 Scale Out: 国产算力芯片内置的 200 Gbps 网卡按 layer-wise 方式进行 prefill 与 decode 节点之间的 KV-cache 传输，KV-cache store 则构建在主机的 RDMA 网卡之上，TP/SP/KVP 则均在 scale-up 互联域内完成。

部署与服务
- 最优并行: LongCat-2.0 采用 prefill–decode (PD) 分离式部署来兼顾 TTFT 与 TPOT。
  - Prefill 节点: Prefill 节点在处理长序列时主要受限于节点间通信带宽，MoE 的 dispatch/combine 耗时占比很高。为此，我们采用多节点 Chunked Pipeline Parallel (CPP) 来缩小 Expert-Parallel (EP) 域；在每个 pipeline stage 内，再以 Attention Sequence Parallelism (SP) 分担长序列的计算压力。
  - Decode 节点: Decode 节点主要受限于显存与 KV-cache I/O。我们以 KVP 切分 KV-cache、降低单片显存占用，并辅以较大的 EP 并行度 (EP128)，同时压低单片的权重显存与 Expert I/O。

这两个阶段中，上述并行方案 (CPP/SP 与 KVP) 均适配了 constrained decoding、multi-step scheduling、MTP 等推理优化特性，保证了推理性能。
- Expert-Parallel 负载均衡: Decode 节点上较大的 EP 并行度更容易引发专家之间的负载不均，我们通过 Expert-Parallel Load Balancing (EPLB) 加以应对，并且将统计采集与分布计算的过程进行了异步化处理。


### LSA

问题

Agent兴起，对大模型高效长输入处理能力提出了极高要求

尽管 DSA 细粒度稀疏注意力缓解了这一压力，但受限于**不连续的索引输出形式**和**二次方的索引评分开销**，DSA中的轻量索引器 (Lightning Indexer) 成为制约端到端延迟的核心瓶颈。


LongCat 稀疏注意力 (LSA)：由 DeepSeek 稀疏注意力 (DSA) 演进而来，通过引入更轻量化的**索引器**（Indexer），在无损模型质量的前提下显著加速长上下文处理。

LongCat 稀疏注意力（LSA）针对索引器引入三项相互正交的效率优化策略：
- **流感知**索引（Streaming-aware Indexing, SI）：重塑了索引器选择 Token 的预算分配，将硬件对齐的连续访问与动态随机选择相结合。
  - 该策略将部分原本碎片化的显存访问转化为可预知的顺序读取，从而实现合并的 HBM 访问并最大化有效带宽。
- **跨层**索引（Cross-Layer Indexing, CLI）：利用注意力中重要 Token 在相邻层间分布的高度一致性来摊薄索引开销。
  - 得益于训练阶段引入的跨层蒸馏，推理时单次索引计算可由多个连续的注意力层复用。
- **层级化**索引（Hierarchical Indexing, HI）：采用由粗到细的两阶段打分机制，先通过 block 级近似打分进行粗召回，再在召回的候选中进行细粒度 token 选择，从而缩小索引器每次检索需处理的候选空间。
  - LongCat-2.0 中，层级化索引（HI）以可插拔的组件形式在部分超长上下文任务上按需启用。

三个组件在设计上相互正交，支持独立开启或关闭

![](https://s3.meituan.net/static-prod01/com.sankuai.friday.longcat.next2/assets/lsaimage-CCkXmBaN.svg)

三项策略扩展至用于`加速投机解码`（Speculative Decoding）的 3-step MTP 模块。
- 跨层索引（CLI）在 Target 模型与 Draft 模型中的应用方式略有不同：在 Target 模型中，每两个连续层共享一次索引结果；
- 而在多步 MTP中，全部三个 Draft 步的计算共用一次索引——具体而言，Step 2 与 Step 3 完全复用 Step 1 所生成的索引结果。

### N-gram Embedding

LongCat-2.0 继承了 [LongCat-Flash-Lite](https://arxiv.org/abs/2601.21204) 的 N-gram Embedding，在同 MoE 正交的稀疏维度上扩展参数，从而提升参数利用效率。为适配 LongCat-2.0 的庞大规模，n-gram size 被设为 5；模型中包含 135B N-gram Embedding 参数，并遵循以下扩展原则：
- MoE 的稀疏度已越过甜点区。 即便不考虑 N-gram Embedding，LongCat-2.0 的稀疏度就接近 97%，此时再增加 135B 专家参数所带来的性能收益较少。相比之下，增加同等参数量的 N-gram Embedding 所带来的收益远超标准MoE。
- N-gram Embedding 的占比被约束在最优区间。 实验表明，当 N-gram Embedding 参数在总参中占比过高（超过 50%）时，其相对于扩增专家的优势会消失。在 LongCat-2.0 中，该占比被控制在 10% 以内，处于安全比例内。

这两条原则保证了 N-gram Embedding 相较同等规模的纯 MoE 模型的稳健优势。

除此之外，在推理阶段，将参数从专家转移到 N-gram Embedding 可降低大 batch 解码时的显存 I/O，从而加速解码过程。

![](https://s3.meituan.net/static-prod01/com.sankuai.friday.longcat.next2/assets/ngram-emb-new.drawio-DtU8Umnl.svg)


### 多教师在线蒸馏

为了全面提升模型的综合表现与应用边界，后训练架构上引入了高度专业化的专家组机制，将其系统性划分为三大核心阵列：**Agent能力专家组**、**推理能力专家组**以及**交互体验专家组**。
- Agent能力专家组致力于在复杂真实场景下深化模型的自主执行能力。该组专家在代码、办公以及检索等细分垂直领域均已达到业界 SOTA 水平。在训练目标上，不仅关注端到端的任务成功率，更深度优化了决定系统鲁棒性的关键“原子能力”——例如复杂工具调用的精准度、多轮API交互中的参数解析能力，以及有效规避死循环或重复调用的自我纠错机制。
- 推理能力专家组的核心愿景是拓展模型的逻辑演进深度，并实现基于问题难度的自适应推理计算。推理专家模型在数学、STEM学科复杂问题求解，以及多跳知识推理任务上，均稳居行业第一梯队。
- 交互体验专家组则聚焦于人机对齐与底层用户感知的优化。交互专家主要负责攻克模型在多变应用场景下的细粒度指令遵循难题，通过先进的对齐技术显著抑制事实性幻觉，并构建了在不牺牲有用性的前提下、边界清晰的安全防御机制。

最后，采用 MOPD 架构方案，在数万卡的国产算力集群上将上述三大维度的顶尖能力进行无缝融合，使得最终产出的模型不仅具备了极强的智能体思维能力，更能够精准解构并洞察用户的复杂需求，在各种极具挑战的真实场景中稳定、高效地执行并交付结果。

![](https://s3.meituan.net/static-prod01/com.sankuai.friday.longcat.next2/assets/mopd-CIX9ZFo9.svg)




# 结束
