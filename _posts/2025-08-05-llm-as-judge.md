---
layout: post
title:  大模型自动评估
date:   2025-08-05 16:52:00
categories: 大模型
tags: 评估 评测
excerpt: 大模型如何自动评估？LLM-as-a-judge 和 Agent-as-a-judge 是什么？
mathjax: true
permalink: /llm_judge
---

* content
{:toc}


# 大模型自动评估 

大模型评估见站内专题: [大模型评测](llm_eva)

## LLM-as-a-Judge

### 思考


#### 说话人难以识别


大模型从**工具**进化为“**裁判**”（LLM-as-a-judge），开始大规模地评判由AI自己生成的内容。

这种高效的评估范式，其可靠性与人类判断的一致性，却很少被深入验证。

【2025-8-17】[大模型给自己当裁判并不靠谱！上海交通大学新研究揭示LLM-as-a-judge机制缺陷](https://zhuanlan.zhihu.com/p/1940396309635916889)

评判模型是否“入戏”之前，AI裁判能准确识别出对话中到底是谁在说话吗？

【2025-8-6】上海交大王德泉课题组，当前大模型评判能力不足，识别角色任务上，最好的模型（Gemini-2.5-pro）正确率才69%，而人类达到91%
- [PersonaEval: Are LLM Evaluators Human Enough to Judge Role-Play?](https://arxiv.org/pdf/2508.10014)
- github [PersonaEval](https://github.com/maple-zhou/PersonaEval) 识别角色，专为LLM裁判打造的“照妖镜”

![](https://pic3.zhimg.com/v2-13ba520638abf287e0517309543dedb2_r.jpg)

大模型更关注**表层的语言风格**（听起来像谁），而人类则首先观察真实的**对话意图和上下文**（在那个情境下，谁会这么说）



### ChatEval

会话评估：[ChatEval](https://chateval.org/)，University of Pennyslvania 宾夕法尼亚大学NLP团队开源，开放领域机器人评估框架，研究人员可以提交自己的模型，ChatEval会自动对比评估效果
- 公开数据集: Neural Conversational Model, Open Subtitles, Cornell Movie Dialogue Corpus ...
- 开源，代码：[chateval](https://github.com/chateval)

chatgpt用于NLG评估
- 论文：[Is ChatGPT a Good NLG Evaluator? A Preliminary Study](https://www.aminer.cn/pub/6407fd3e90e50fcafd2747e3/is-chatgpt-a-good-nlg-evaluator-a-preliminary-study)
- we regard ChatGPT as a **human evaluator** and give **task-specific** (e.g., summarization) and **aspect-specific** (e.g., relevance) instruction to prompt ChatGPT to score the generation of NLG models. We conduct experiments on three widely-used NLG meta-evaluation datasets (including summarization, story generation and data-to-text tasks).
- Experimental results show that compared with previous automatic metrics, ChatGPT achieves state-of-the-art or competitive correlation with golden human judgments. We hope our preliminary study could prompt the emergence of a general-purposed reliable NLG metric.

复杂会话质量评估：东南大学网络科学与工程学院
- 论文：[Evaluation of ChatGPT as a Question Answering System for Answering Complex Questions](https://www.aminer.cn/pub/641137fe90e50fcafd17bb5e/evaluation-of-chatgpt-as-a-question-answering-system-for-answering-complex-questions)
-  we present a framework that evaluates its ability to answer complex questions. Our approach involves categorizing the potential features of complex questions and describing each test question with multiple labels to identify combinatorial reasoning. Following the black-box testing specifications of CheckList proposed by Ribeiro et.al, we develop an evaluation method to measure the functionality and reliability of ChatGPT in reasoning for answering complex questions.
- We use the proposed framework to evaluate the performance of ChatGPT in question answering on 8 real-world KB-based CQA datasets, including 6 English and 2 multilingual datasets, with a total of approximately 190,000 test cases. We compare the evaluation results of ChatGPT, GPT-3.5, GPT-3, and FLAN-T5 to identify common long-term problems in LLMs.
- The dataset and code are available at [Complex-Question-Answering-Evaluation-of-ChatGPT](https://github.com/tan92hl/Complex-Question-Answering-Evaluation-of-ChatGPT)

Question
- In various types of KBQA tasks, **complex question answering** (KB-based CQA) is a challenging task that requires question answering models to have the ability of compositional reasoning to answer questions that require multi-hop reasoning, attribute comparison, set operations, and other complex reasoning.
- KBQA任务重，回答复杂问题很有挑战性，因为涉及这些问题要求多跳推理、属性对比、集合操作及其他复杂推理

Overview

To evaluate ChatGPT's ability to answer complex knowledge, we propose an evaluation framework: a feature-driven multi-label annotation method 特征驱动的多标签标注方法
- First, we classify the **latent features** that constitute complex questions, and describe each question under test with multi-labels for identifying combinatorial reasoning. 
- Secondly, following the black-box test specification of CheckList proposed by Microsoft, we design an **evaluation method** that introduces `CoT` hints to measure the reasoning function and reliability of large language models in answering complex questions. 

Our evaluation uses 8 real complex question answering datasets, including **six** English datasets and **two** multilingual datasets, to further analyze the potential impact of language bias. We compared the evaluation results of `ChatGPT`, `GPT3.5`, `GPT3`, and `FLAN-T5` to identify persistent historical issues in `LLMs`. All data and results are available for further analysis.

### PandaLM

【2023-4-30】大语言模型对比评估：PandaLM, 本地评测，不用担心数据安全问题
- [PandaLM: Reproducible and Automated Language Model Assessment](https://github.com/WeOpenML/PandaLM)
- ![](https://github.com/WeOpenML/PandaLM/raw/main/figures/main-figure.png)
- ![](https://github.com/WeOpenML/PandaLM/raw/main/figures/inst-tune-pipeline.png)

（1）批量多模型对比

```py
from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("WeOpenML/PandaLM-7B-v1",use_fast=False)
model = AutoModelForCausalLM.from_pretrained("WeOpenML/PandaLM-7B-v1")
# ----------
from pandalm import EvaluationPipeline

pipeline = EvaluationPipeline(candidate_paths=["huggyllama/llama-7b", "bigscience/bloom-7b1", "facebook/opt-6.7b"], input_data_path="data/pipeline-sanity-check.json")
print(pipeline.evaluate())
```

（2）本地部署 Web UI
- 启动后，访问[链接](http://localhost:31228)

```sh
cd PandaLM/pandalm/ 
CUDA_VISIBLE_DEVICES=0 python3 run-gradio.py --base_model=WeOpenML/PandaLM-7B-v1 --server_port=<your-server-port> --server_name=<your-server-name>
```

### LLM-BLENDER

【2023-6-11】[Allen AI推出集成主流大语言模型的 LLM-BLENDER 框架](https://mp.weixin.qq.com/s/xRgZacoVvBRyk8DS5fcNcw)
- Allen AI实验室联合南加大和浙江大学的最新研究论文，发表在ACL上。
  - 论文：[LLM-BLENDER: Ensembling Large Language Models with Pairwise Ranking and Generative Fusion](https://arxiv.org/pdf/2306.02561)
- 提出了一个集成框架(LLM-BLENDER)，通过利用多个开源大型语言模型的不同优势使框架始终保持卓越的性能。
  - 鉴于众多LLM有不同的优势和劣势，开发了一种利用其互补潜力的**集成方法**，从而提高鲁棒性、泛化和准确性。通过结合单个LLM的贡献，可以减轻单个LLM中的偏见、错误和不确定性信息，从而产生更符合人类偏好的输出。

LLM-BLENDER，一个创新的集成框架，通过利用多个开源LLM的不同优势来获得持续卓越的性能。
- LLM-BLENDER通过排名方式来减少单个LLM的弱点，并通过融合生成来整合优势，以提高LLM的能力。

LLM-BLENDER包括两个模块：PAIRRANKER 和 GENFUSER。
- 首先，PAIRRANKER 比较 N个LLM的输出，然后通过 GENFUSER 将它们融合，从排名前K的输出中生成最终输出。
- 现有方法如instructGPT中的reward model能够对输入x的输出Y进行排名，但是当在多个LLM进行组合时其效果并没有那么明显。原因在于，它们都是由复杂的模型产生的，其中一个可能只比另一个好一点。即使对人类来说，在没有直接比较的情况下衡量候选质量也可能是一项挑战。


### AlpacaEval 斯坦福 自动评估

【2023-6-15】斯坦福研究人员提出一个基于大语言模型的全新自动评估系统 —— [AlpacaEval](https://tatsu-lab.github.io/alpaca_eval/)
- 速度快、成本低，而且还经过了2万个人类标注的验证。
- [资讯](https://zhuanlan.zhihu.com/p/637303794)

AlpacaEval 结合了 AlpacaFarm 和 Aviary

改善自动评测流程，团队发布了：
- 一个易于定制的流程
- 模型和自动评测器的排行榜
- 分析自动评测器的工具包
- 18K人类标注
- 2K人类交叉标注

AlpacaEval有着拔群的效果：
- 与人类多数票的一致性，高于单个人类标注者
- 胜率与人类标注高度相关（0.94）
- 相比于lmsys评测器，有显著提升（从63%提高到69%）

局限性可以概括为以下三点：
- 指令比较简单
- 评分时可能更偏向于风格而非事实
- 没有衡量模型可能造成的危害


## Agent-as-a-Judge

研究团队：AI能否评判AI？META 推出
- 【2024-10-16】[Agent-as-a-Judge: Evaluate Agents with Agents](https://arxiv.org/pdf/2410.10934)
- Dataset: [devai-benchmark](https://huggingface.co/devai-benchmark)
- Project: [agent-as-a-judge](https://github.com/metauto-ai/agent-as-a-judge)
- 解读 [Agent-as-a-Judge：用AI智能体来评估AI智能体，比人类评审更高效？](https://zhuanlan.zhihu.com/p/1892963974628217079)

当大模型日益强大，如何评估表现成了AI领域新难题。
- 传统依靠人工或者自动指标的方式，难以精准、快速地应对复杂、开放式任务。
- 最近，研究团队提出了“`Agent-as-a-Judge`（AI代理评审）”的新范式，让AI作为评委来评价其他AI的输出，逐步成为主流趋势。

### 什么是 Agent-as-a-Judge？

一种利用Agent本身推理与视角能力，由AI自动评判其他大模型行为的评测方法。

论文梳理了该概念的起源、如何从单一AI评审进化到多智能体辩论和动态评议小组，并分析了各自的优势与局限。
- 【2025-8-5】论文 [When AIs Judge AIs: The Rise of Agent-as-a-Judge Evaluation for LLMs](https://arxiv.org/pdf/2410.10934)

❓AI评AI有哪些方式？
- 1️⃣ 单模型评审：让一个强力大模型（如GPT-4.1）根据提示，对其他模型输出打分或排序。
- 2️⃣ 多智能体辩论/委员会：多个AI分饰不同专家和批评者角色，像小组讨论一样审议答案，减少单一AI的偏见。
- 3️⃣ Agent-as-a-Judge：AI不只看最终结果，还能像人一样跟踪整个推理和执行过程，逐步给出细致反馈。这对自动化代码生成、复杂推理任务等尤为有效。
	
### 效果如何？

多智能体评议明显提升了与人工评价的一致性。

Agent-as-a-Judge 甚至在代码自动化等任务中，几乎与人类专家小组打分一致，且比单一AI评审更细致稳定。

三种主流代码生成智能体（MetaGPT、GPT-Pilot和OpenHands）在DevAI基准上进行了全面测试：

准确性对比：
- Agent-as-a-Judge与人类专家共识的吻合度达90.44%
- 常规LLM-as-a-Judge仅有60.38%
- 单个人类评审员之间的一致性也只有85%左右

效率提升：
- 耗时：118分钟 vs 人类86.5小时（节省97.7%时间）
- 成本：30美元 vs 人类1300美元（节省97.6%费用）
- 深度洞察： 通过PR曲线分析（见图7），Agent-as-a-Judge在识别"部分满足需求"的边界案例时，甚至优于个别人类评审员。


| 评估方式       | 一致率   | 耗时   | 成本    |
| -------------- | -------- | ------ | ------- |
| 人类专家共识   | 100%     | 86.5h  | $1297   |
| Agent-as-a-Judge | **90.44%**   | 1.97h  | $30.58  |
| LLM-as-a-Judge  | 60.38%   | 0.18h  | $29.63  |



### 哪些应用场景？

该方法已在医学、法律、金融、教育等领域初步落地。
- 医疗AI评审能模拟不同专家、患者视角；
- 法律AI能像法庭辩论一样多维度评价文本；
- 金融场景下则能关注合规和风险控制。

未来，AI评AI有望推动大模型更加安全、可靠、高效地发展。




## LLM 自我诊断


### CriticGPT

【2024-6-28】[OpenAI前对齐团队「遗作」：RLHF不够用了！用GPT-4训练GPT-4](https://mp.weixin.qq.com/s/sQvqzCjwz97hI-JqKUW31g)

ChatGPT 错误变得越来越难以察觉，AI训练师难以发现不准确答案，使得驱动 RLHF 的比较任务变得更加艰巨。
- RLHF 的一个根本性限制，随着模型逐渐超越任何提供反馈的人类知识水平，这一局限可能会使得模型的校准变得更加困难。

OpenAI 基于 GPT-4 训练了一个专门找 bug 新模型 —— `CriticGPT` , 精准地分析 ChatGPT 回答, 并提出建议，帮助人类训练师更准确地评估模型生成的代码，并识别其中的错误或潜在问题
- OpenAI官网: [Finding GPT-4’s mistakes with GPT-4](https://openai.com/index/finding-gpt4s-mistakes-with-gpt-4)
- 论文 [LLM Critics Help Catch LLM Bugs](https://cdn.openai.com/llm-critics-help-catch-llm-bugs-paper.pdf)
- 作者 Jan Leike 曾共同领导了OpenAI超级对齐团队，致力于开发 InstructGPT、ChatGPT 和 GPT-4 的对齐工作。
- OpenAI 联合创始人、首席科学家 Ilya Sutskever 宣告离职，Jan Leike 也撒手不干了，后转投 Anthropic 麾下。

![](https://images.ctfassets.net/kftzwdyauwt9/43xtEDLlQJ4c30ca8IQyBV/52d37b20664d2968ea344718101c0852/code_desktop_light__3_.png?w=3840&q=80&fm=webp)

CriticGPT 在很多情况下比人类专家更擅长发现错误，它们甚至能在一些被认为是「完美无缺」的任务中找出问题，尽管这些任务大多数并不是代码任务，对 CriticGPT 来说有点超纲。

方法
- 用 LLM 来评价 LLM， 采用类似于 InstructGPT 和 ChatGPT 的自回归 Transformer 策略。
- 训练时，研究人员将「问题 - 答案」对作为输入。
- 模型输出的批评将遵循特定格式，在答案中穿插附加评论。

评价标准
- 对于有 bug 的代码，LLM 可能做出多种类型的评价。
- ① 正确地指出代码中的严重错误，但这个批评中也包含一个错误的断言；
- ② 只指出了两个次要问题。

收到这两种批评：
- 有一部分不正确，但可能更有用；
- 另一种未能指出严重问题，但没有明显错误。

哪种来自 LLM 的批评更有效呢？研究团队设置了以下标准请人工训练师做了进一步评价：
- 是否全面，即没有遗漏任何明显和严重的问题（全面性）。
- 是否捕捉到了名为「critique-bug inclusion」（CBI）的预先指定的特定错误。
- 是否包含任何臆想的错误或特别吹毛求疵的小问题。
- 根据回答的风格和有用程度，给 LLM 的批评一个整体的主观评分。

人工训练师将根据 1-7 等级评价LLM审核结果。前两个特征（CBI 和全面性）类似于召回率 —— 模型撰写了包括多个错误点的长篇批评，通常评分会提高。然而，批评变长时更可能包含臆想的问题和吹毛求疵。训练师在总体评分时倾向于给准确、全面、简洁且避免吹毛求疵的批评以高分。

比较批评与 Elo 评分
- 评价过程中，人工训练师将同时看到对同一问题的**四个批评**，通过比较得出特定属性的偏好率。
- 如果批评 A 在全面性方面得分为 1/7，而批评 B 得分为 2/7，那么 B 比 A 更全面。

为了总结模型之间的**成对偏好率**，计算 Elo 评分。
- Elo 评分使用 BFGS（强制采样束搜索） 对数据集中用于比较的成对模型进行拟合计算得出。


效果:
- 审查 ChatGPT 代码的准确率提高了 60%

Anthropic 将类似 CriticGPT 的模型整合到 RLHF 流程中

CriticGPT 局限
-  只能处理**短答案**，但未来需要更厉害的方法，来帮助 AI 训练师理解那些又长又难的任务。
-  仍然会产生**幻觉**，影响训练师。
-  主要集中在**单点错误检测**，还不能检测分散在多个部分的错误。

CriticGPT 虽然很有用，但如果任务太难太复杂，即使是专家用了这个模型也可能评估不出来。


### AutoDetect

【2024-6-29】[AutoDetect：「大模型」检测「大模型」缺陷，从错误中高效学习](https://zhuanlan.zhihu.com/p/706023553)

如何识别 LLM 缺陷？

现有方法均存在明显不足。
- 人工检查 LLM 的缺陷涉及大量人类专家的参与，需要大量的人力物力，难以规模化扩展；
- 现有自动检查 LLM 缺陷的方式依赖**评估基准**，但评估基准的构建目的主要是公平地对比一系列模型的表现强弱，无法彻底地、有针对性地**发掘特定模型的缺陷**，而且评估基准大多存在更新周期长、数据泄漏、区分度较小等问题。

AutoDetect 是第一个在通用任务上系统探索 LLM 缺陷发掘过程的框架，并且在指令遵从、数学、代码等任务上进行了充分的验证。
- 高效搜索模型缺陷，在 GPT-3.5、 Claude-3-sonnet 等多个主流模型上有着高于 30% 的缺陷检测成功率。
- 提升模型性能，通过从自动发掘的缺陷中学习，可以让 LLM 在多个任务上产生 10% 左右的性能提升。

- 论文：[AutoDetect: Towards a Unified Framework for Automated Weakness Detection in Large Language Models](https://arxiv.org/abs/2406.16714)
- 代码：[AutoDetect](https://github.com/thu-coai/AutoDetect)

框架采用一种类似于**教育评估系统**的方法，包括创建全面的问题来评估学生，并审查他们的回答，从而识别个性化的薄弱点。

该系统根据具体模型表现进行不断优化和调整，从而提供定制和有效的弱点识别。

框架包含由大模型智能体（agent）实现的三个角色：
- `主考官`（Examiner）：负责构建包含多样化测试点的综合分类体系，并根据目标模型的表现动态优化框架，以提供一个完善和定制的评测系统来识别潜在的薄弱点。
- `出题者`（Questioner）：根据每个测试考点创建有挑战性的问题。通过迭代探索，出题者不断探测模型的薄弱点，并在出现新缺陷时有效地调整问题生成，发现更多薄弱点。
- `评估者`（Assessor）：需要分析目标模型在测试中的表现，并推测新的个性化的弱点，以将其纳入测试系统中，这对个性化的评估至关重要。

![](https://pic4.zhimg.com/80/v2-60b72396ad310bafc65c0821b7a7a17b_1440w.webp)

AutoDetect 在指令遵循，数学推理和代码任务上都展现出了出色的效果，在 GPT-3.5 和 Claude-3-Sonnet 上都实现了超过 30% 的弱点检测成功率（ISR）。同时，平均 ISR 的排序也大致符合我们对模型能力的认知，显示了 AutoDetect 发展为动态 benchmark 的潜力。

缺陷：
- LLM 在同一任务中的不同子类上，**性能差距非常明显**（**数学任务**中应用题做的不错，但是**几何题**性能较差）；
- LLM 可能在困难的任务中表现出色，但在更简单的任务中失败（可以完成复杂的算法题，但是在基础的概念上可能出错）；
- LLM 在**复杂指令**和**多步推理**上还存在明显不足。

AutoDetect 可以生成创意性的指令，人工标注员可能由于自身能力限制难以构造。此外，我们发现 AutoDetect 还会自发的结合多种知识点生成问题，比如在指令遵循任务中组合多个知识点。


# 结束
