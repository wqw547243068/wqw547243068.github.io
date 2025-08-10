---
layout: post
title:  全模态大模型专题
date:   2025-08-08 16:52:00
categories: 大模型
tags: qwen 多模态 阿里 蚂蚁
excerpt: 全模态大模型原理及各种实现
mathjax: true
permalink: /all_modality
---

* content
{:toc}


# 全模态大模型 

多模态大模型专题见站内：[多模态大模型案例](multimodal_case)


## 阿里

### 【2025-3-27】Qwen2.5-Omni


【2025-3-27】阿里巴巴发布 Qwen2.5-Omni，全球首个**端到端全模态**大模型，为多模态信息流**实时交互**提供了新技术框架。

Qwen2.5-Omni 整合了文本、图像、音频和视频的跨模态理解能力，实现**流式**文本与自然语音的双向同步生成。
- ![](https://picx.zhimg.com/v2-7df9b0935ac5619cf348f1939ce9f04d_1440w.jpg)

Qwen2.5-Omni 在保持全能的同时，并没有牺牲在各个垂直领域的能力

资料：
- [体验 Qwen Chat 新功能](https://chat.qwenlm.ai)
- [Qwen2.5-Omni技术报告](https://github.com/QwenLM/Qwen2.5-Omni/blob/main/assets/Qwen2.5_Omni.pdf)
- 代码 Code: [Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni)
- 中文介绍: [Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni/blob/main/README_CN.md)
- 视频介绍: [Video](https://www.youtube.com/watch?v=UF55yM67EH0)

#### 特点

特点
- Omni 和 架构：Thinker-Talker 架构，端到端的多模态模型，感知不同的模态，包括文本、图像、音频和视频，同时以**流式**方式生成文本和自然语音响应。提出了一种名为 `TMRoPE` （Time-aligned Multimodal RoPE） 的新型位置嵌入，以将视频输入的时间戳与音频同步。
- **实时语音和视频**聊天 ：专为完全实时交互而设计的架构，支持分块输入和即时输出。
- 自然而稳健的**语音生成** ：超越许多现有的流媒体和非流媒体替代方案，在语音生成方面表现出卓越的稳健性和自然性。
- **跨模态**的强劲性能 ：与类似大小的单模态模型进行基准测试时，在所有模态中都表现出卓越的性能。
  - Qwen2.5-Omni 在音频功能上优于同等尺寸的 Qwen2-Audio，并实现了与 Qwen2.5-VL-7B 相当的性能。
- 出色的端到端语音教学： Qwen2.5-Omni 在端到端语音教学跟踪方面的性能可与文本输入的有效性相媲美，MMLU 和 GSM8K 等基准测试证明了这一点。


#### 原理

关键技术：
- 1）采用分块处理策略解耦长序列多模态数据，由多模态编码器负责感知、语言模型承担序列建模，通过共享注意力机制强化模态融合；
- 2）提出时间对齐的位置编码方法TMRoPE，通过音视频交错排列实现时间戳同步；
- 3）首创`Thinker-Talker`架构，分离文本生成（Thinker语言模型）与语音合成（基于隐藏表征的双轨自回归Talker模型），避免模态间干扰；
- 4）引入滑动窗口DiT解码器降低音频流初始延迟。

![](https://pic4.zhimg.com/v2-c2de76bf71d503c577ada48a3b9f4bf9_1440w.jpg)

效果分析：
- Omni-Bench 等多模态基准上达到SOTA，语音指令跟随能力与纯文本输入（MMLU/GSM8K）表现相当，流式语音生成在鲁棒性和自然度上超越主流流式/非流式方案。

「Thinker-Talker」（思考者-说话者） 架构。这个设计非常巧妙，让模型能 同时思考和说话：
1. `Thinker` (思考者): 扮演大脑的角色。它负责处理来自文本、音频、视频等多种模态的输入，通过专门的音视频编码器提取信息，再利用一个 Transformer 解码器进行理解和处理，最终生成高层语义表示和相应的文本内容
2. `Talker` (说话者): 担当嘴巴的功能。它以流式（streaming）方式接收 Thinker 生成的高层表示和文本，并采用一种双轨自回归 Transformer 解码器架构，流畅地合成并输出离散的语音单元（tokens）。

关键点: Talker 并非独立工作，直接获取 Thinker 产生的**高维表示**，并且 共享 Thinker 全部历史上下文信息。这使得 Thinker 和 Talker 构成了一个紧密协作的单一整体模型，可以进行端到端的训练和推理。这种设计是实现低延迟、高流畅度语音交互的核心

#### Qwen2.5-Omni-7B

Qwen2.5-Omni-7B 模型是 Omni（全能）模型。
- 一个模型能同时理解 文本、音频、图像、视频 多种输入，并且能输出 文本和音频


#### Qwen2.5-Omni-3B

全模态 Qwen2.5-Omni-7B 模型推出后，开发者反馈更小尺寸的Qwen2.5-Omni，以便更方便地适配

2025年4月30日，开源 Qwen2.5-Omni-3B 版本，较之前 7B 相比，代码运行时的推理时间减少，响应开发者轻量级GPU适配需求的新模型。
- 🔹 与Qwen2.5-Omni-7B相比，3B版本在长上下文序列处理（约25k tokens）中显存消耗减少超50% 🚀，并可在普通24GB的消费级GPU上支持长达30秒的音视频交互 。
- 🔹 3B版本模型保留7B模型90%以上的多模态理解能力 ，语音输出自然度与稳定性与7B版本性能一致 💪🏻。

新的Omni模型已在魔搭社区和HuggingFace上开源



#### 效果

Qwen2.5-Omni全面评估：
- **跨模态能力** SOTA: 在需要整合多种模态信息的任务上（如 OmniBench 基准测试），Qwen2.5-Omni 达到了当前最佳水平（State-of-the-Art）
- **单模态**能力不俗: 与同等规模的单模态模型（如 Qwen2.5-VL-7B、Qwen2-Audio）以及一些强大的闭源模型（如 Gemini-1.5-pro）相比，Qwen2.5-Omni 在各项单模态任务上也展现出强大的竞争力。具体包括：
  - * 语音识别:Common Voice
  - * 语音翻译:CoVoST2
  - * 音频理解:MMAU
  - * 图像推理:MMMU, MMStar
  - * 视频理解:MVBench
  - * 语音生成: Seed-tts-eval 及主观自然度评估

#### 实践

消费级显卡也能运行 Qwen2.5-Omni 本地部署
- conda 创建虚拟环境，并激活
- 安装第三方库：transformers、accelerate、qwen-omni-utils-decord、modelscope
- 使用 modelscope 下载 qwen-2.5-omni 代码
- 创建 python 脚本，写脚本

#### 问题

Qwen-2.5-Omni-7B 问题——目前还没有更普适的**量化版本**
- 当前量化版本只有 `GPTQ`，没有 `gguf`/`mlx`. 导致大部分使用 `ollama`, `llama.cpp`, `mlx` 的用户根本没办法用。
- 而原版 7B 大小达到了**20GB+**，使用小显存显卡的用户完全没办法单卡部署。
	
而 `GPTQ` 量化理论上能用在 `vLLM`/`SGLang` 上。

但是这俩框架目前也不支持, 为纯本文模型准备的。


### 【2025-6-11】蚂蚁 Ming-Omni


【2025-6-11】蚂蚁百灵团队 2.8B 参数就能媲美GPT-4o

开源 Ming-Omni：支持统一感知与生成的多模态模型，在**端到端**语音理解和指令执行方面表现优异，超越了 `Qwen2.5-Omni` 和 `Kimi-Audio`
- 论文 [Ming-Omni: A Unified Multimodal Model for Perception and Generation](https://arxiv.org/pdf/2506.09344)
- 【2025-5-21】Code: [Ming](https://github.com/inclusionAI/Ming/tree/main)

Hugging Face 宝藏项目——[Ming-Omni](https://huggingface.co/inclusionAI/Ming-Lite-Omni)。

Ming-Omni 实现了真正的**多模态统一**：同时输入文字、图片、音频和视频，不仅能理解，还能生成高质量的语音和图像。

最震撼的是，只用**2.8B**的活跃参数就达到了GPT-4o级别的效果。

`Ming-Omni` 是蚂蚁与 inclusionAI 共同开发的首个开源多模态模型，旨在与 GPT-4o 竞争。
- 该模型支持多种输入形式，包括文本、语音、图片和视频，同时也可以生成文本、语音和图片输出。
- 这一创新的开源项目为开发者提供了灵活的应用选择，具有广泛的潜力和应用场景。

`Ming-lite-omni` 是统一的多模态模型，是 Ming-omni 的轻量版，源自 Ling-lite，拥有 28 亿激活参数。
- 该模型能够处理图像、文本、音频和视频，同时在语音和图像生成方面表现出强大的能力。
- Ming-lite-omni 采用专用编码器从不同模态中提取 token，随后由 Ling 处理，Ling 是一种配备了新提出的模态专用路由器的 MoE 架构。
- 该设计使单一模型能够在统一框架内高效处理和融合多模态输入，从而支持多样化任务，无需单独模型、任务特定微调或结构重设计。

Ming-lite-omni 超越了传统多模态模型，支持音频和图像生成。这通过集成先进的音频解码器实现自然语音生成，以及 Ming-Lite-Uni 实现高质量图像生成，使模型能够进行上下文感知聊天、文本转语音转换和多功能图像编辑。

技术突破：MoE架构设计。
- 传统模型要么参数量巨大，要么能力单一
- Ming-Omni 通过模态专用路由器，让每个任务都能调用最合适的专家网络。这意味着更高的效率，更低的成本。

![](https://pic4.zhimg.com/v2-f5bb04b0e3764d81d519677a854766b9_1440w.jpg)


无论是上下文对话、文本转语音，还是图像编辑，流畅度和准确性都超出预期。

关键是**完全开源**，代码和权重全部公开，这对整个AI社区是巨大的贡献。

意义
- 对于开发者来说，这是真正部署到生产环境的方案。
- 对于普通用户，这意味着不用再为AI能力付费就能获得顶级体验。



# 结束