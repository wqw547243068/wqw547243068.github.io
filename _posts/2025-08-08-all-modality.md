---
layout: post
title:  全模态大模型专题
date:   2025-08-08 16:52:00
categories: 大模型
tags: qwen 多模态
excerpt: 全模态大模型原理及各种实现
mathjax: true
permalink: /all_modality
---

* content
{:toc}


# 全模态大模型 

多模态大模型专题见站内：[多模态大模型案例](multimodal_case)



## Qwen2.5-Omni


【2025-3-27】阿里巴巴发布Qwen2.5-Omni，全球首个**端到端全模态**大模型，为多模态信息流**实时交互**提供了新技术框架。

Qwen2.5-Omni 整合了文本、图像、音频和视频的跨模态理解能力，实现**流式**文本与自然语音的双向同步生成。

关键技术：
- 1）采用分块处理策略解耦长序列多模态数据，由多模态编码器负责感知、语言模型承担序列建模，通过共享注意力机制强化模态融合；
- 2）提出时间对齐的位置编码方法TMRoPE，通过音视频交错排列实现时间戳同步；
- 3）首创`Thinker-Talker`架构，分离文本生成（Thinker语言模型）与语音合成（基于隐藏表征的双轨自回归Talker模型），避免模态间干扰；
- 4）引入滑动窗口DiT解码器降低音频流初始延迟。

效果分析：
- Omni-Bench 等多模态基准上达到SOTA，语音指令跟随能力与纯文本输入（MMLU/GSM8K）表现相当，流式语音生成在鲁棒性和自然度上超越主流流式/非流式方案。

「Thinker-Talker」（思考者-说话者） 架构。这个设计非常巧妙，让模型能 同时思考和说话：
1. `Thinker` (思考者): 扮演大脑的角色。它负责处理来自文本、音频、视频等多种模态的输入，通过专门的音视频编码器提取信息，再利用一个 Transformer 解码器进行理解和处理，最终生成高层语义表示和相应的文本内容
2. `Talker` (说话者): 担当嘴巴的功能。它以流式（streaming）方式接收 Thinker 生成的高层表示和文本，并采用一种双轨自回归 Transformer 解码器架构，流畅地合成并输出离散的语音单元（tokens）。

关键点: Talker 并非独立工作，直接获取 Thinker 产生的**高维表示**，并且 共享 Thinker 全部历史上下文信息。这使得 Thinker 和 Talker 构成了一个紧密协作的单一整体模型，可以进行端到端的训练和推理。这种设计是实现低延迟、高流畅度语音交互的核心

Qwen2.5-Omni全面评估：
- **跨模态能力** SOTA: 在需要整合多种模态信息的任务上（如 OmniBench 基准测试），Qwen2.5-Omni 达到了当前最佳水平（State-of-the-Art）
- **单模态**能力不俗: 与同等规模的单模态模型（如 Qwen2.5-VL-7B、Qwen2-Audio）以及一些强大的闭源模型（如 Gemini-1.5-pro）相比，Qwen2.5-Omni 在各项单模态任务上也展现出强大的竞争力。具体包括：
  - * 语音识别:Common Voice
  - * 语音翻译:CoVoST2
  - * 音频理解:MMAU
  - * 图像推理:MMMU, MMStar
  - * 视频理解:MVBench
  - * 语音生成: Seed-tts-eval 及主观自然度评估

Qwen2.5-Omni 在保持全能的同时，并没有牺牲在各个垂直领域的能力


资料：
- [体验 Qwen Chat 新功能](https://chat.qwenlm.ai)
- [Qwen2.5-Omni技术报告](https://github.com/QwenLM/Qwen2.5-Omni/blob/main/assets/Qwen2.5_Omni.pdf)
- 代码 Code: [Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni)
- 中文介绍: [Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni/blob/main/README_CN.md)
- 视频介绍: [Video](https://www.youtube.com/watch?v=UF55yM67EH0)

Qwen2.5-Omni-7B 模型是 Omni（全能）模型。
- 一个模型能同时理解 文本、音频、图像、视频 多种输入，并且能输出 文本和音频


# 结束