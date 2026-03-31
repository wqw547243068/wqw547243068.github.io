---
layout: post
title:  大模型投机采样
date:   2023-09-18 17:56:00
categories: 大模型
tags: 投机采样 美杜莎
excerpt: 大模型如何加速推理过程？方法之一：投机采样，整理系列解法
mathjax: true
permalink: /spec_decoding
---

* content
{:toc}


# 投机采样


## 总结

方法
- `投机采样`（Speculative decoding）针对 LLM 推理串行解码特点，通过引入近似模型来执行串行解码，原始模型执行并行评估采样，通过近似模型和原始模型的互相配合，在保证精度一致性的同时降低了大模型串行解码的次数，进而降低了推理时延。
- `美杜莎头`（Medusa head）则是对投机采样的进一步改进，摒弃了**近似模型**，原始模型结构上新增了若干解码头，每个解码头可并行预测多个后续 tokens，然后使用基于树状注意力机制并行处理，最后使用典型接收方案筛选出合理的后续 tokens。该方法同样降低了大模型串行解码的次数，最终实现约两倍的时延加速。

对比
- 投机采样和多头美杜莎相对于原始自回归推理带来的提速效果。
- 投机采样在参数规模大的模型中性能提升更高，不过这取决于小模型的选择；
- 多头美杜莎则在不同参数规模的模型中拥有更一致的性能提升

<img width="900" height="100%" alt="image" src="https://github.com/user-attachments/assets/ae2c7b1b-c059-4dfa-bdb3-4a15f14c97db" />


## 【2022】投机采样


2022年, Google DeepMind 推出大模型推理加速方法: Speculative Decoding，投机采样或推测解码

利用蒸馏学习中小模型近似大模型，不损失生成效果前提下，获得 3x 以上加速比

vllm 框架支持投机采样（Speculative Decoding）, 见 spec_decode

核心思想：许多常见的单词和句子都是很容易预测。

<img width="872" height="395" alt="image" src="https://github.com/user-attachments/assets/be24aed8-1e73-471b-9803-7fdeb16e55a2" />

因此，大模型只需要在关键部分中指导小模型，就能够带来性能提升。
- 小模型在收到用户提问后会做出单个字的预测，当预测到一定长度后，大模型会判断是否接受小模型预测的多字，这里大模型会一次性处理多字

<img width="874" height="496" alt="image" src="https://github.com/user-attachments/assets/789be669-979c-44f3-8399-57089bcdfc4f" />

与传统的自回归推理方法不同，投机采样采用了**草稿模型**（draft model），通常是规模更小的模型，进行自回归推理。而原始的大模型则会根据小模型推理的结果进行判断，决定是否接受小模型推理出的多字

推测解码是一种推理优化技术，生成当前 Token 时，对未来 Token 进行有根据猜测，这一切都在一次前向传播中完成。

融入了验证机制，以确保这些 Token 正确性，从而保证推测解码的整体输出与普通解码的输出相同。

优化大语言模型（LLMs）的推理成本，是降低成本并提高其应用率的关键因素。

为了实现这一目标，有各种推理优化技术可用，包括自定义内核、输入请求的动态批处理以及大型模型的量化。

推测解码有两种主要方法
- 利用较小模型：例如，将 Llama 7B 用作 Llama 70B 的推测器
- 添加推测头（并对其进行训练）：IBM 的 PyTorch 团队实验中，添加推测头的方法在模型质量和延迟改善方面都更为有效。

效率说明：
- 投机者架构：目前方法允许修改头的数量，对应可选择的 token 数量。增加头的数量也会增加所需的额外计算量和训练的复杂性。在实践中，对于语言模型，我们发现 3 - 4 个头在实际应用中效果良好，而代码模型则可以从 6 - 8 个头中获益。
- 计算量：增加头的数量会在两个维度上导致计算量增加，一是单次前向传播的延迟增加，二是处理多个 Token 所需的计算量增加。如果推测器在增加头的数量后准确率不高，就会导致计算资源浪费，增加延迟并降低吞吐量。
- 内存：每次前向传递都需要与高带宽内存（HBM）进行往返通信，增加的计算量由此得到抵消。请注意，如果我们提前正确预测 3 个 Token，那么就节省了三次与 HBM 的往返时间。

**不足**

GPT4 技术细节泄露后，对于**投机采样**【Speculative Decoding】策略加速推理的研究比较多，但是问题
- **投机采样**依赖一个**小而强**的模型, 生成对于原始模型来说比较简单的token
- 其次在一个系统中维护2个不同模型，导致架构上的复杂性
- 最后使用投机采样的时候，会带来额外的解码开销，尤其是当使用一个比较高的采样温度值时。

更多见站内专题：[投机采样](text_decoding#投机采样)


## Google Medusa 美杜莎

投机采样虽好，但某些场景下，小模型选择棘手，如何同时部署大模型和小模型？

【2023-9-18】[LLM推理加速-Medusa](https://zhuanlan.zhihu.com/p/655809033)
- 项目主页: [medusa-llm](https://sites.google.com/view/medusa-llm)
- Github [Medusa](https://github.com/FasterDecoding/Medusa)
- 论文: [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774)

Medusa: Simple Framework for Accelerating LLM Generation with Multiple Decoding Heads
- ![](https://pic3.zhimg.com/80/v2-9de3ccb0b3107514b4fc71495ed78342_1440w.webp)

解读
- [大模型推理提速：投机采样和多头美杜莎机制](https://mp.weixin.qq.com/s/aqi1F0QRXpBwey_hrVVZkw)

多头美杜莎利用了多个预测头（language model heads）来进行多字预测，这些额外的预测头被称为美杜莎头

正常的LLM 基础上，增加几个解码头，并且每个头预测的偏移量是不同的，比如原始的头预测第i个token，而新增的medusa heads分别为预测第i+1，i+2...个token。如上图，并且每个头可以指定topk个结果，这样可以将所有的topk组装成一个一个的候选结果，最后选择最优的结果
- ![](https://pic1.zhimg.com/80/v2-6abff04d4dc96eb7752be0a8d7948e14_1440w.webp)

美杜莎（Medusa）推理框架使推测解码流行起来；
- 现有模型上添加一个头，然后对其进行训练以进行推测。

通过使“头”呈分层结构来修改美杜莎架构，其中每个头阶段预测单一 Token，然后将其输入到下一个头阶段。

图解

<img width="876" height="396" alt="image" src="https://github.com/user-attachments/assets/cafb367c-955e-45e7-8ee8-a29deabdf053" />

多头美杜莎的top-1推理（假设每个字都为单个token）。
- 大模型在收到用户提问后会做出多个字的预测，这里大模型会一次性处理多字。具体为主预测头会预测下1个字，第一个和第二个美杜莎头分别会预测第2个和第3个字。更多的美杜莎头也以此类推。
- 美杜莎头为独立模块，可加在现有预训练/微调好的基础模型中（例如Vicuna-13B）

如果直接使用top-1（贪婪）策略来进行推理会很容易掉进局部最优概率组合。

因此，为了提高推理效果，多头美杜莎使用了top-k 方式来进行推理

<img width="925" height="353" alt="image" src="https://github.com/user-attachments/assets/6630a21a-75c5-4430-9796-1f31ae13dba6" />


更多解读见[文章](https://zhuanlan.zhihu.com/p/655809033)

## 自适应投机采样

最早提出的`投机解码`（Speculative Decoding）算法使用 Target Model + Draft Model 范式，其加速效果很大程度上受到 Draft Model 对齐程度以及自身解码时延的影响。要得到高对齐同时低时延的 Draft Model 可能需要微调或蒸馏，成本高且不具有通用性。

【2024-9-11】[最全LLM自投机算法汇总](https://zhuanlan.zhihu.com/p/706111755)

因此，许多**自投机**（Self-Speculative Decoding）算法被提出作为原始投机解码的替代。
- 让 Target Model 根据特定算法直接生成 draft tokens，不借助额外的 Draft Model。
- 并且，简单修改 Target Model 结构，比如增加 LM Head 或者增加几层网络构成一个小型的 Draft Model，只要训练成本可接受，也可认为是自投机算法的一类。


【2026-3-27】[单张显卡跑出15倍推理速度，aiX-apply-4B小模型加速企业AI研发落地](https://mp.weixin.qq.com/s/Xzy19OoL-R-D2hh8ahOG8g)

3月25日，北大系AI Coding赛道创企硅心科技（aiXcoder）发布专为「代码变更应用」场景设计的高性能、轻量级模型 aiX-apply-4B。

20多种主流编程语言及Markdown等多类型文件格式的测试中，aiX-apply-4B的平均准确率达到 93.8%，超越Qwen3-4B基座模型 62.6% 准确度，甚至高于千亿级大模型DeepSeek-V3.2。

同一任务场景下，aiX-apply模型算力成本约为DeepSeek-V3.2的5%，推理速度则提升15倍，仅需一张消费级显卡即可在企业部署。

推理效率方面，aiXcoder引入自适应投机采样技术，极大压缩了端到端延迟。

企业级生产环境实测显示，aiX-apply-4B推理速度每秒可达2000 tokens，在单张RTX 4090消费级显卡上即可高效运行；而对比模型DeepSeek-V3.2则需要八卡H200高端集群部署。

综合不同的硬件部署成本与推理速度进行对比，aiX-apply-4B仅用DeepSeek-V3.2约5%的算力成本，实现了15倍的效率提升。

aiXcoder 已构建起覆盖多个研发关键环节的小模型矩阵，并创新提出“大模型+小模型”协同架构，让“通才”大模型与“专才”小模型各司其职、优势互补：
- 通用大模型聚焦复杂意图理解、代码逻辑分析、修改方案制定等需要深度推理的工作，发挥其智能优势；
- 垂直场景小模型则承接高频工程任务，以轻量化特性实现快速、精准执行。

这种架构设计，让企业的有限算力得到分层利用：小模型支持专项场景任务的高效完成，节约出更多算力用于大模型的复杂推理。



# 结束

