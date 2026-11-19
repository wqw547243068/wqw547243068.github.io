---
layout: post
title:  大模型自动评估
date:   2025-08-05 16:52:00
categories: 大模型
tags: 评估 评测 agent 阿里 skill rubric 美团
excerpt: 大模型如何自动评估？LLM-as-a-judge 和 Agent-as-a-judge 是什么？
mathjax: true
permalink: /llm_judge
---

* content
{:toc}


# 大模型自动评估 

标准化评测要解决的核心问题：
- 可量化：把"聪明"变成 72.3% 的准确率，把"差一些"变成具体分数差。
- 可复现：任何人用同样的模型、评测集、参数，跑出来的分数应该一样。科学研究的底线。
- 可对比：A 模型在 MMLU 上 65%，B 模型 58%，这个差距更客观，而不是"我觉得 A 更好"。


大模型评估见站内专题: [大模型评测](llm_eva)

## Rubric 评测

【2026-11-08】Rubric 评测
- **评分维度**和**分级标准**怎么拆
  - 为什么每个分数等级都要有可落地的标准？
  - 0~3 分还是 1~5 分？
- 只看结果够吗:面向**过程**的评测
  - 过程要评什么：参数提取、工具流程、SOP、多轮目标追踪
  - 用到后训练时，结果和过程怎么配合？
- 怎么保证 Rubric 靠谱？
  - 人人一致率、人机一致率
  - 人人一致率低怎么办？用什么指标衡量？
- Rubric 怎么用到 SFT 拒绝采样
  - 阈值怎么定？有什么风险？
- Rubric 有多个维度，RL 的 Reward 怎么算？
  - 取 min、取 max、取平均，还是各维先做组内归一化？
	

## LLM-as-a-Judge

### 思考

LLM-as-a-Judge 真的管用吗？

#### 【2025-8-6】说话人难以识别


大模型从**工具**进化为“**裁判**”（LLM-as-a-judge），开始大规模地评判由AI自己生成的内容。

这种高效的评估范式，其可靠性与人类判断的一致性，却很少被深入验证。

【2025-8-17】[大模型给自己当裁判并不靠谱！上海交通大学新研究揭示LLM-as-a-judge机制缺陷](https://zhuanlan.zhihu.com/p/1940396309635916889)

评判模型是否“入戏”之前，AI裁判能准确识别出对话中到底是谁在说话吗？

【2025-8-6】上海交大王德泉课题组，当前大模型评判能力不足，识别角色任务上，最好的模型（Gemini-2.5-pro）正确率才69%，而人类达到91%
- [PersonaEval: Are LLM Evaluators Human Enough to Judge Role-Play?](https://arxiv.org/pdf/2508.10014)
- github [PersonaEval](https://github.com/maple-zhou/PersonaEval) 识别角色，专为LLM裁判打造的“照妖镜”

![](https://pic3.zhimg.com/v2-13ba520638abf287e0517309543dedb2_r.jpg)

大模型更关注**表层的语言风格**（听起来像谁），而人类则首先观察真实的**对话意图和上下文**（在那个情境下，谁会这么说）

#### 【2025-8-25】LLJ 不管用

【2025-8-25】[你的怀疑是对的！LLM作为Judge，既无效又不可靠，终于有论文向LLJ开炮了](https://mp.weixin.qq.com/s/NChnvM0uijUhDMiu_tWVRg)

LLM Judges 涵盖三大功能：
- **性能评估** (Performance Evaluation)：这是最传统的应用，即评估模型生成内容的质量。
  - 核心领域：文本摘要、机器翻译、对话生成等。
- **数据构建** (Data Construction)：利用AI来自动生成或标注训练数据，以替代部分人力。
  - 典型任务：数据标注，尤其是在仇恨言论检测、政治立场分类等主观性强的任务中。
- **模型增强** (Model Enhancement)：将“AI裁判”直接整合进模型的训练和对齐流程中，以提升或规范模型行为。
  - 关键场景：安全对齐（作为实时安全护栏、自动进行红队演练）、奖励建模、以及实现模型的“自我提升”和“自我对齐”。

“LLM Judges”已经从一个“评估员”，演变成了贯穿数据准备、模型训练、安全部署等环节的“多面手”。

【2025-8-25】加拿大麦吉尔大学论文，对当前热门趋势`LLMs as Judges`进行了深刻反思和批判。
- 《既无效又不可靠？调查将大型语言模型作为法官的运用》
- [Neither Valid nor Reliable? Investigating the Use of LLMs as Judges](https://arxiv.org/pdf/2508.18076v1)

对LLJs的应用热情，已经远远超过了对其作为评估工具本身是否科学、可靠、有效的严格审查。

(1) 假设一：AI能完美替代人类？

业界普遍认为，LLMs是人类判断的有效代理 (LLMs as a Proxy for Human Judgment)，只要AI裁判的评分和人类专家的评分高度相关，就证明它是有效的。

但研究者们一针见血地指出，这个逻辑链条的起点，所谓“人类判断”这个金标，本身就是摇摇欲坠的。
- **人类评估本身就问题重重**：自然语言生成（NLG）领域，人类评估其实非常混乱，缺乏统一标准。
  - 比如，对于什么是“连贯性”，不同的研究、不同的标注者可能有完全不同的理解和打分标准，这导致人类评分本身就存在很大的不确定性。
- **用混乱去验证混乱**：用一个本身就不太可靠、充满随机误差的“金标准”去验证LLM裁判的可靠性，其说服力自然大打折扣。这就好比用一把刻度模糊的尺子去校准另一把新尺子。
- **LLM裁判加剧了问题**：目前的LLM裁判实践不仅复制了这些问题，甚至可能因为其内部决策过程不透明而加剧。
  - 例如，在使用同一个公开基准（如SummEval）时，不同的研究给LLM的指令、评分量表和评估流程都各不相同，使得结果更难横向比较。

(2) 能力强就等于好裁判？

另一个普遍看法: LLMs是能干的评估者 (LLMs as Capable Evaluators)，既然LLM本身能力这么强，当个评估员肯定绰绰有余。

可现实挺骨感的，研究者们发现，作为裁判的LLM存在一系列内在缺陷，严重影响其判断的信度和效度。
- 不听指挥 (Instruction Adherence)：研究发现，LLM裁判经常“夹带私货”，并不严格遵循您在指令中给出的评估标准，反而会依赖自己的一些内部偏见，甚至混淆不同的评估维度（比如把“相关性”和“流畅性”搞混）。
- 解释不可信 (Explainability)：虽然LLM可以为自己的评分生成解释，但这些解释的“忠实性”值得怀疑。它可能只是为了让结果看起来合理而编造的理由（高“表面效度”），而非其真实的决策逻辑。
- 充满偏见 (Robustness)：LLM裁判表现出五花八门的偏见，比如位置偏见（偏爱排在前面的选项）、冗长偏见（喜欢内容更长的回答）、从众偏见（偏爱多数意见）等。
- 极其脆弱 (Robustness)：它们对简单的对抗性攻击几乎没有抵抗力。研究表明，通过在文本中加入一些精心设计的、不影响语义的微小扰动，就可以轻易地操纵LLM裁判的评分，甚至让它把100%的有害内容标记为无害。
- 缺乏专业知识 (Expertise)：在需要特定领域知识（如事实核查、安全评估）的任务中，LLM本身的能力就存疑，让它来当裁判，其“内容效度”自然无法保证。

(3) 自动化评估能“大力出奇迹”？

大家都爱“大力出奇迹”，LLMs是可扩展的评估者 (LLMs as Scalable Evaluators)，觉得用AI裁判可以大规模、自动化地搞定评估和模型对齐，效率直接拉满。

但研究者警告说，这种做法可能正在制造一个巨大的、自我循环的“信息茧房”，最终损害评估的“预测效度”。
- 数据污染与自恋偏见：当您用同一个系列的LLM（比如GPT系列）去生成训练数据、训练模型、最后又用它来做评估时，一个被称为“自恋偏见”或“自我增强偏见”的问题就出现了。模型会不可避免地偏爱与自己同源的模型所生成的输出，导致评分虚高。
- 为刷分而战：自动化排行榜（如Chatbot Arena）的出现，加剧了“应试”现象。各个模型为了在排行榜上获得更高名次，可能会过度优化去迎合裁判模型的偏好，而不是真正提升通用能力，这是一种典型的“过拟合”。
- 肤浅的安全对齐：研究者提到“肤浅对齐假说”，即当前的安全对齐更多是让模型学会了某种“说话风格”（比如礼貌地拒绝回答），而非真正理解了安全概念。过度依赖LLM裁判进行自动化安全评估，可能只会筛选出越来越会“装无辜”的模型，而无法解决深层安全问题。

三家科技巨头“既当运动员又当裁判员”的现状

明确点名Google和OpenAI还有Meta：在讨论“竞争性基准测试”的弊端部分，论文引用研究指出
- 像Chatbot Arena这样的评估平台存在“有利于Google和OpenAI等专有提供商的不平等数据访问”问题。这个事情我记得前几个月在网上还热议过一阵子。
- 以Meta为例：在分析“LLMs作为安全法官”时，论文明确提到了Meta公司的Llama Guard模型作为一个实例。
- 此外，在参考文献中，论文还引用了一篇关于“Meta的Llama 4‘herd’争议与AI污染”的文章，直接将其与数据污染问题联系起来。

(4) AI裁判真的“物美价廉”？

省钱，LLMs是成本效益高的评估者 (LLMs as Cost-Effective Evaluators)，这绝对是AI裁判最吸引人的一点。

不过，研究者提醒必须算算那些看不见的“隐形成本”，这些成本关系到评估的“后果效度”，即这项技术应用后带来的长远社会影响。
- 经济与伦理冲击：大规模采用AI裁判，直接冲击的是全球数以万计的数据标注员的生计，这是一个已经很脆弱的群体。这背后是复杂的社会和伦理问题，不能简单地用“效率”二字一笔带过。
- 环境成本：虽然训练模型的环境成本备受关注，但大规模、持续地使用LLM进行评估（这是一种推理任务）所产生的能源消耗和碳排放同样惊人，且随着模型越来越大，这个问题会愈发严重。
- 社会偏见的放大器：LLM会学习并反映训练数据中存在的社会偏见。当一个带有偏见的LLM成为“裁判”时，它可能会在评估中系统性地给某些特定人群（如特定性别、种族）相关的回答打低分，从而在下一代模型的开发中进一步固化甚至放大这些偏见。

怎么办？

三条核心建议
1. 放弃“一刀切”的评估方法，强调情境化应用:
  - 目前LLJs的应用存在巨大疏忽：无论任务和领域有何不同，部署和设计评估的方式都大同小异。这种做法是危险的，可能导致有害的后果。
  - 例子是：使用LLJs来大规模进行“红队演练”（即寻找模型漏洞）可以拓宽评估范围，这是有益的。但如果将同样的方法直接用于模型的安全过滤统，就可能只会训练出“表面上”的安全行为，而非真正的安全理解。
  - 因此，评估LLJs的角色必须综合考虑任务性质、应用领域和评估目标等多个关键维度。
2. 紧急呼吁改进整个领域的评估实践:
  - 减轻LLJs自身的偏见固然重要，但整个领域更迫切需要的是改进评估实践本身。
  - 引用近期的争议事件指出，科技公司有操纵现有评估框架的行为，这引发了对数据污染、为跑分而进行的竞争性基准测试以及对基准过度拟合等严重问题的担忧。
  - 尽管评估在机器学习发展中至关重要，但从业者之间缺乏严谨、共享的实践方法。大家共享的是基准和指标等“技术产物”，而不是科学的方法论。
  - 这篇论文证明，LLJs的采用不仅复制并加剧了NLG评估中长期存在的缺乏标准化和系统化的问题，还带来了新的挑战。
3. 倡导评估模式的根本性转变：从自我评估到独立监督:
  - 最激进也是最深刻的建议。“也许是时候改变那种依赖有利益关系的公司来提供其旨在推向市场的产品进行透明全面评估的模式了”。
  - 应该努力建立适当的机制，以实现透明、有效和可靠的评估。这暗示着需要一个类似于其他高风险行业（如药品、航空）的独立第三方监督体系。


## 评测工具


### 总结

框架包括:
- Inspect AI、lm-evaluation-harness、promptfoo、DeepEval、RAGAS、Langfuse、Phoenix 等。

选择时优先考虑：
> 可复现性、与 CI 集成、成本、是否支持你的系统类型（RAG/智能体），以及评分器可检验性。

【2026-7-6】评测工具

| 工具名称 | 开发者 | 开源协议 | 任务数量 | 中文支持 | 安装复杂度 | 可视化能力 | 社区活跃度 | 适配场景 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| lm-eval-harness | EleutherAI | MIT | 200+ | 有限 | 低 | 无 | 最高 | 快速评测/CI集成 |
| OpenCompass | 上海AI实验室 | Apache 2.0 | 100+ | 强（原生中文） | 中 | 有Web UI | 中等 | 中文模型/学术报告 |
| HELM | Stanford CRFM | Apache 2.0 | 100+ | 有限 | 高 | 有限 | 学术圈活跃 | 学术研究/全面审计 |

选型指南
- 选 `lm-eval-harness`：想快速验证一个模型，5 分钟出结果
  - 需要集成到 CI/CD 流水线，每次代码提交自动跑评测- 要对比 HuggingFace Leaderboard 上的模型- 习惯命令行操作，不需要可视化界面
- 选 `OpenCompass`：评测中文模型（C-Eval、CMMLU 等中文任务原生支持）
  - 需要生成可视化报告（有 Web UI）
  - 做国产模型评测（Baichuan、ChatGLM、DeepSeek 等适配更好）
  - 需要主观评测（让 GPT-4 当裁判打分）
- 选 `HELM`：做学术研究，需要最全面的能力审计
  - 关注模型的安全性、公平性、偏见（不只是准确率）
  - 有足够的 API 预算（全面评测需要大量调用）
  - 需要生成标准化的学术报告

【2026-5-13】[大模型评测不再拍脑袋：用 lm-evaluation-harness 给模型做"体检"](https://cloud.tencent.com/developer/article/2668215)

### lm-evaluation-harness

[Eleuther AI](http://www.eleuther.ai) 推出 [lm-evaluation-harness](https://github.com/eleutherai/lm-evaluation-harness)

[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) 是 EleutherAI（开源 AI 研究组织）开发的大模型统一评测框架。"体检中心"
- 把模型送进来，自动跑完 200 多项检查，输出一份详细的"体检报告"。
- [官方文档](https://slyracoon23.github.io/lm-evaluation-harness/)

核心特点：
- 任务最全：支持 200+ 评测任务，覆盖知识、推理、数学、代码、安全等多个维度
- 模型兼容广：HuggingFace 模型、OpenAI API、Claude、Gemini、本地 Ollama 部署的模型，都能接
- 社区标准：HuggingFace Open LLM Leaderboard 的官方评测工具，跑出来的分数可以直接上排行榜对比
- 安装简单：一条 pip 命令搞定


```sh
# 创建虚拟环境
python3 -m venv ~/lm-harness-env
source ~/lm-harness-env/bin/activate
# 安装核心框架
pip install lm-eval
# 装本地模型依赖
pip install transformers torch accelerate
```

启动评测

python代码

```py
import lm_eval

results = lm_eval.simple_evaluate(
    model="gpt2",
    tasks=["hellaswag", "mmlu"],
    num_fewshot=0
)
```


shell

```sh
export OPENAI_API_KEY="你的API密钥"

lm_eval \
 --model openai-completions \
 --model_args model=gpt-4o-mini \
 --tasks mmlu_anatomy \
# --tasks hellaswag,arc_easy,piqa,winogrande # 多任务测评
 --limit 10 \
 --output_path ./results/gpt4o-mini

# 模型选择
lm_eval \
  # hf 上下载模型
  --model hf \
 --model_args pretrained=Qwen/Qwen2.5-0.5B-Instruct,dtype=float16 \
 # 使用本地模型
  --model_args pretrained=/path/to/your/model,dtype=float16
 --tasks hellaswag \
 --limit 20 \
 --batch_size 4 \
 --output_path ./results/qwen0.5b-hellaswag
```

原理
1. 加载 gpt-4o-mini 模型
2. 从 MMLU 解剖学子集抽 10 道题
3. 模型答题、自动判卷、输出结果

输出结果
- 10 道解剖学题，GPT-4o-mini 答对了 7 道，准确率 70%

```
┌─────────────────┬──────────────────┐
│ Task            │ Metric           │
├─────────────────┼──────────────────┤
│ mmlu_anatomy    │ acc,none: 0.7000 │
└─────────────────┴──────────────────┘
```


```sh
git clone https://github.com/EleutherAI/lm-evaluation-harness
cd lm-evaluation-harness
pip install -e .

# Basic installation
pip install lm-eval

# With additional dependencies
pip install "lm-eval[gptq,vllm]"

# For development
pip install -e ".[dev]"
```

使用

```sh
# 设置下最大并行数量的环境变量
export NUMEXPR_MAX_THREADS=64
# 如果不能连接huggingface，需要配置镜像
export HF_ENDPOINT=https://hf-mirror.com
# 查看支持的任务数据集
lm-eval --tasks list
```


参数含义
- --model：模型启动模式，可选hf代表huggingface，或者可选vllm,openai
- --model_args：代表模型地址，可用huggingface仓库名（不是地址），例如EleutherAI/pythia-160m，或者本地地址例如./xxxxx
  - 注意 model_args可以附带很多参数，用逗号分隔
- --model_args pretrained=EleutherAI/gpt-j-6b,parallelize=True,load_in_4bit=True,peft=nomic-ai/gpt4all-j-lora \
- --model_args pretrained={model_name},tensor_parallel_size={number of GPUs to use},dtype=auto,gpu_memory_utilization=0.8 \
  - 这里说明model_args可以有很多模型加载的参数，例如并行，量化，微调模型的peft位置等
- --tasks：代表测试任务，指定具体任务 openbookqa,arc_easy,winogrande,hellaswag,arc_challenge,piqa,boolq
- --device：使用的GPU机器标号，注意这个参数只能写一个，如果想用多gpu请使用tensor_parallel_size参数或者accelerate启动器
- --batch_size：auto代表自动选择batch大小，:4代表在测试过程中共自动重选4次batch大小
- --output_path：保存评估结果 
- --use_cache：来缓存先前运行的结果。这样可以避免重复执行相同的（模型、任务）对进行重新评分。

```sh
# 加载huggingface远程模型
lm_eval --model hf \
    --model_args pretrained=baichuan-inc/Baichuan-13B-Chat,trust_remote_code=true \
    --tasks mmlu,nq_open,triviaqa,truthfulqa,gsm8k,openbookqa,arc_easy,winogrande,hellaswag,arc_challenge,piqa,boolq \
    --device cuda:0 \
    --batch_size auto:1 \
    --output_path ./eval_out/baichuan13b \
    --use_cache ./eval_cache

# 加载本地模型
lm_eval --model hf \
    --model_args pretrained=./openbuddy-llama2-13b-v11.1-bf16 \
    --tasks toxigen,mmlu,nq_open,triviaqa,truthfulqa,gsm8k,openbookqa,winogrande,arc_easy,arc_challenge \
    --batch_size auto \
    --output_path ./eval_out/openbuddy13b \
    --use_cache ./eval_cache

# 使用accelerate启动器，这支持多GPU
accelerate launch -m lm_eval --model hf \
    --model_args pretrained=./openbuddy-llama2-13b-v11.1-bf16 \
    --tasks mmlu,nq_open,triviaqa,truthfulqa,gsm8k,openbookqa,arc_easy,winogrande,hellaswag,arc_challenge,piqa,boolq \
    --batch_size auto:4

accelerate launch -m lm_eval --model hf \
    --model_args pretrained=/data/save_model/Qwen_pt/,trust_remote_code=true,dtype=bfloat16 \
    --tasks glue,cmmlu,gsm8k,mmlu,boolq \
    --batch_size 2
    --output_path ./eval_out/pretrain_Qwen_14B_chat \

lm_eval --model hf \
    --model_args pretrained=./data/gpt2-large \
    --tasks glue \
    --batch_size auto \
    --num_fewshot 5 \
    --output_path ./eval_out/gpt2-large 

lm_eval --model hf \
    --model_args pretrained=./data/gpt2-xl \
    --tasks mmlu,glue,squadv2 \
    --batch_size auto \
    --output_path ./eval_out/gpt2-xl \
    --use_cache ./eval_cache/gpt2-xl

CUDA_VISIBLE_DEVICES=4 lm_eval --model hf \
--model_args pretrained=./openbuddy-llama2-13b-v11.1-bf16 \
--tasks mmlu,super-glue-lm-eval-v1\
--batch_size auto \
--output_path ./eval_out/openbuddy13b \
--use_cache ./eval_cache/openbuddy13b

CUDA_VISIBLE_DEVICES=0 lm_eval --model hf \
--model_args pretrained=/mnt/weijie/openbuddy-llama2-13b-v11.1-bf16 \
--tasks cola,wnli,rte,sst2,mnli,mnli_mismatch,qnli,mrpc \
--batch_size auto \
--output_path /mnt/weijie/eval_out/openbuddy13b \
--use_cache /mnt/weijie/eval_cache/openbuddy13b

CUDA_VISIBLE_DEVICES=1 lm_eval --model hf \
--model_args pretrained=gpt2-large \
--tasks cola,wnli,rte,sst2,mnli,mnli_mismatch,qnli,mrpc \
--batch_size auto \
--output_path /mnt/weijie/eval_out/gpt2-large \
--use_cache /mnt/weijie/eval_cache/gpt2-large

CUDA_VISIBLE_DEVICES=2 lm_eval --model hf \
--model_args pretrained=OpenBuddy/openbuddy-llama2-70b-v14.3,trust_remote_code=true,load_in_4bit=True \
--tasks cola,wnli,rte,sst2,mnli,mnli_mismatch,qnli,mrpc \
--batch_size auto \
--output_path /mnt/weijie/eval_out/openbuddy70b \
--use_cache /mnt/weijie/eval_cache/openbuddy70b

CUDA_VISIBLE_DEVICES=3 lm_eval --model hf \
--model_args pretrained=gpt2-xl,trust_remote_code=true \
--tasks cola,wnli,rte,sst2,mnli,mnli_mismatch,qnli,mrpc \
--batch_size auto \
--output_path /mnt/weijie/eval_out/gpt2-xl \
--use_cache /mnt/weijie/eval_cache/gpt2-xl

CUDA_VISIBLE_DEVICES=4 lm_eval --model hf \
--model_args pretrained=NousResearch/Llama-2-13b-chat-hf,trust_remote_code=true \
--tasks cola,wnli,rte,sst2,mnli,mnli_mismatch,qnli,mrpc \
--batch_size auto \
--output_path /mnt/weijie/eval_out/llama13b \
--use_cache /mnt/weijie/eval_cache/llama13b
```

常用数据集：

混合BenchMark:
- glue(通用自然语言理解评估，包含一系列子数据集：single-sentence tasks CoLA and SST-2, similarity and paraphrasing tasks MRPC, STS-B and QQP, and natural language inference tasks MNLI, QNLI, RTE and WNLI.)
- mmlu(多任务自然语言理解，包含57 subjects across STEM, the humanities, the social sciences, and more.)
- lambada(BooksCorpus的大约10,000段落组成，在每个段落的最后一句话中都预测了一个缺失的目标词。丢失的单词始终是最后一句话的最后一句话，没有候选单词可供选择)
- persona(闲聊数据)
- pile(The Pile is a 825 GiB diverse, open source language modelling data set that consists of 22 smaller, high-quality datasets combined together.)
- scrolls(长文本推理，The SCROLLS benchmark contains the datasets GovReport, SummScreenFD, QMSum, QASPER, NarrativeQA, QuALITY and ContractNLI.)

子领域数据：
- 道德: ethics_virtue,ethics_deontology,ethics_justice,ethics_utilitarianism(美德), crows_pairs(刻板印象), toxigen(毒性)
- 真实性: truthfulqa
- 翻译: wmt14,wmt16,translation,xcopa
- 中文评测集: ceval-valid,cmmlu
- QA: coqa(对话QA), csatqa(知识图谱QA), nq_open(ODQA领域), openbookqa (ODQA领域),triviaqa(ODQA领域), webqs(ODQA领域)
- 数学推理: gsm8k,mathqa
- 自然语言理解: race(机器阅读理解),squadv2
- 自然语言推断: xnli,xwinograd



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

### OpenJudge

【2026-1-27】[告别盲测，通义AutoRubric自动生成评测标准](https://www.zhihu.com/pin/1999209351597037208) 

做 LLM 评测时，不想花大代价训 Reward Model?  只能让 LLM 当裁判（Judge）！

通义实验室开源首个AI应用评测框架 [OpenJudge](https://openjudge.me/) 
- OpenJudge 为 AI 评估提供完整的工作流支持：从收集测试数据 → 定义评估器 → 规模化评估 → 分析弱点 → 快速迭代，让 AI 质量保证更简单、更专业。

这次提出 AutoRubric：
- 把人类偏好背后的“隐性直觉”，变成模型可执行的“显性标准”。不再让模型临场发挥，而是先生成一套结构化的“评分细则”（Rubrics），让它按维度检查。
- AutoRubric 开源在OpenJudge项目，路径：openjudge/generator/iterative_rubric/generator.py
- 项目与论文：[OpenJudge](https://github.com/agentscope-ai/OpenJudge)
- 论文：[OpenJudge: A Unified Framework for Holistic Evaluation and Quality Rewards](arXiv:2510.17314)

😳评测结果往往很“玄学”：
1. 凭感觉：说不清为什么 A 比 B 好，理由很泛。
2.  位置偏见 (Position Bias)：A/B 互换位置，结论竟然变了。
3.  大量 Tie：稍微难一点的任务就只会判平局。

 AutoRubric “物理外挂”四部曲不用训模型，不用烧大钱，只需 4 步：
 1. 自动长标准：从少量人类偏好数据里，自动提取“为什么 A 比 B 好”的理由。
 2. 脱水去重：用数学逻辑（Coding Rate）干掉重复的废话，只留最有信息量的标准。
 3. 聚合提炼：把散乱的理由变成通用的 Theme-Tips（比如：语气真实度、逻辑连贯性）。
 4. 权重排序：给标准排座次，重要的先看！

性能提升：

从“玄学”到“工程”在复杂的角色扮演场景下进行了实测，数据提升非常直观：
- AutoRubric较baseline准确率提升14%，位置偏见下降 19%。
- 通过将隐性标准显性化，模型捕捉到了人类标注员更在意的细节，引入 Rubrics 后，模型从“盲目选择”转向“按项核对”，鲁棒性显著增强

如果你也被“Judge 不稳/说不清凭啥选”折磨过，这套方法真的值得去跑一次！你会第一次看清：所谓的“模型好坏”，到底是由哪些具体的标准组成的。 

### 【2026-8-3】Ori Eval

【2026-8-3】OpenRouter 推出 [Ori Eval](https://openrouter.ai/ori/eval) 简化评估流程

编写首个评估的最简单方式。 
- 没有绝对最好的模型，只有最适合每项任务的模型。
- 在 OpenRouter 多个模型中，自动找到适配具体模块的模型

Ori Eval 直接在编码工具中扫描代码库，找出哪些地方调用了模型，评估优劣（如成本、性能等），然后编写评估报告，并对每个模型候选方案进行测试。


Ori Eval 利用 OpenRouter 的 API 处理代码库中的每项任务，然后评估结果。 

ORI‑Eval 工作机制
- 代码库扫描：自动检测项目代码，定位所有模型调用入口与代码使用位置。
- 交互式问询：确认优先看重的评估指标，例如**使用成本、推理速度、响应延迟、工具调用成功率**。
- 并行测试：自动生成 `.eval.ts` 评测脚本，依托 OpenRouter 服务，并行使用多款候选大模型测试 Agent。
- 回归测试：本地运行评测脚本，或是接入 CI 流水线；拦截模型性能退化，针对特定程序缺陷开展专项测试。

如果搭建评测，可告知以下两项信息：
- Agent 采用什么编程语言、开发框架搭建
- 本次优化对应的业务目标与使用场景

安装

```sh
curl -fsSL https://openrouter.ai/skills/spawn-ori-eval
```

这个 skill
- 推理后端默认 OpenRouter 云端
- 评测引擎本地可运行；修改 `eval.ts` 接口地址即可对接本地 vLLM/Ollama，实现完整脱离 OpenRouter 生态；
  - 运行 `bun run xxx.eval.ts`

局限性
- ori login、交互式初始化向导阶段仍需要登录 OpenRouter；初始化完成之后评测可完全脱离云端
- 原生交互式问卷只能读取 OpenRouter 模型列表，本地模型需要手动修改评测代码
- 自动对比多候选模型功能需要你自行在 ts 脚本配置多个本地推理端点


```ts
const openai = new OpenAI({
  //baseURL:"https://openrouter.ai/api/v1",
  baseURL:"http://127.0.0.1:8000/v1",
  apiKey:"dummy"
})
```


相关文章

ORI：O‑Routing‑Intelligence 面向异构大模型系统、基于向量空间驱动的查询路由框架

单一大型语言模型（LLM）在应对种类持续扩增的任务时往往能力受限，单模型方案已经难以适配全部场景。

ORI（O Routing‑Intelligence，路由智能），可调度多组大模型的动态调度框架。将用户输入查询智能分发至最适配的模型，既提升各类任务的推理准确率，同时保障推理效率。
在多类基准数据集上的综合实验证明：该框架能够稳定提升精度，并且控制额外计算开销。

借助智能查询路由机制：
- 在 MMLU 数据集上，效果超越最优单模型 2.7 分；
- MuSR 数据集高出 1.8 分；
- 在 ARC、BBH 基准测试取得当前顶尖水准。

上述结果验证了多模型调度方案的优势；同时证明 ORI 自适应架构可以更好地处理多样化任务，为多‑大模型集群提供一套可扩展、高性能的解决方案。



## Agent-as-a-Judge

研究团队：AI能否评判AI？META 推出
- 【2024-10-16】[Agent-as-a-Judge: Evaluate Agents with Agents](https://arxiv.org/pdf/2410.10934)
- Dataset: [devai-benchmark](https://huggingface.co/devai-benchmark)
- Project: [agent-as-a-judge](https://github.com/metauto-ai/agent-as-a-judge)
- 解读 [Agent-as-a-Judge：用AI智能体来评估AI智能体，比人类评审更高效？](https://zhuanlan.zhihu.com/p/1892963974628217079)

当大模型日益强大，如何评估表现成了AI领域新难题。
- 传统依靠人工或者自动指标的方式，难以精准、快速地应对复杂、开放式任务。
- 最近，研究团队提出了“`Agent-as-a-Judge`（AI代理评审）”的新范式，让AI作为评委来评价其他AI的输出，逐步成为主流趋势。


【2025-12-2】伯克利，生产级别agent评测方法
- 论文 [Measuring Agents in Production](https://arxiv.org/pdf/2512.04123)

AI智能体已在多个行业投入使用，但对促成部署成功的技术策略了解有限。

首个针对生产环境中AI智能体的大规模系统性研究，调查了306名从业者，完成了覆盖26个领域的20项深度案例分析。研究聚焦四大核心问题：组织为何构建、如何构建、如何评估，以及主要挑战是什么。

生产环境中的智能体通常采用简单可控的构建方式：68%智能体在需要人工干预前最多执行10个步骤，70%依赖对现成模型的提示工程而非权重微调，74%主要依靠人工评估。

可靠性仍是首要开发挑战，其核心症结在于确保和评估智能体正确性的难度。尽管存在这些挑战，简单却高效的方法已能让智能体在不同行业中创造价值。

本研究记录了当前的实践现状，通过让研究者清晰了解生产环境中的挑战，同时为从业者提供实用参考，搭建起了研究与部署之间的桥梁。



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


### 美团 Agent 评测


#### 评测体系

【2026-09-10】[《Agent 评测白皮书》系列01：Agent 评测全览](https://mp.weixin.qq.com/s/hBSIPQnsBeWwX9UZLjWYFA)

完备的评测体系要同时具备三种能力，并沉淀评测资产（评测集）

| 能力 | 回答的问题 | 主要承载模块 | 缺失后的典型症状 |
| ---- | ---- | ---- | ---- |
| **发现**问题 | 哪里出问题了？什么时候出？ | 在线评测和在线监控 | 问题总是靠用户投诉才知道，被动救火 |
| **定位**问题 | 为什么出问题？哪层的问题？ | Case 挖掘与归因、观测基建 | 知道分数跌了，但说不清原因，只能“再观察” |
| **驱动演进** | 改完后是不是真变好了？有没有跷跷板问题？ | 离线评测和在线评测 | 修好问题引入两个新问题，能力反复摇摆 |

评测资产（评测集）：这三种能力运转起来后，会沉淀下可复用的资产，才是评测体系真正的长期价值。
- 评测标准（Metrics & Rubric）：团队对“好”的共识的显式化、可量化，消除评测的模糊度。
- 评测样本：真实问题的结构化沉淀。黄金集定义“好的下限”，错题集记录“踩过的坑”，挑战集标定“能力的边界”。价值在于可回归——每一个曾经犯过的错，都不应该再犯第二次。

评测体系建设的本质是把团队对**业务质量的隐性认知**转化为**可量化、可复用、可传递、可自动执行的显性资产**。

从评测体系的视角可以拆解出四个模块。前三个模块分别回答不同的问题，第四个模块是前三者的地基。

| 模块 | 回答的问题 | 核心作用 | 典型触发时机 |
| ---- | ---- | ---- | ---- |
| 离线评测 | Agent 版本变更后有没有退化？ | 回测与上线门控 | 每次变更（模型/Prompt/知识库/Skill） |
| 在线评测与在线监控 | 线上真实运行时表现如何？ | 真实环境检验 + 异常报警 | 持续运行 / 周期性巡检 |
| Case 挖掘与归因 | 发现问题后怎样定位和修正？ | 定位问题，驱动双环演进 | 异常信号触发 / 例行采样 |
| Agent 观测基建 | 看不看得见？能不能还原现场？ | 评测的基石，贯穿全生命周期 | 始终在线 |

<img width="1000" height="100%" alt="image" src="https://github.com/user-attachments/assets/968f3baf-c87e-4d3a-ae74-ee35abcc7bcf" />

业界和开源领域对**离线评测**的定义非常清晰，而在线评测、在线监控、观测以及 Case 挖掘与归因这几个模块彼此之间存在**模糊地带**
- Arize AI、LangFuse、Braintrust 概念划分就不尽相同。
- 有的产品把“Online Evaluation”和“Monitoring”合并成一个概念
- 有的把 Trace 采集归入 Observability 而把 Trace 分析归入 Evaluation。

由于行业内没有形成统一的概念划分，为了方便后续讨论中的概念对齐，以及用一套框架贯穿冷启动、扩量和自进化，拆解出上面这四个大模块。

商家经验分析Agent是典型的长程 Agent：**多步骤、多 Skill 调用、有中间产物、与环境频繁交互、没有唯一答案**。

离线评测的核心作用：Agent 版本变更后的回测可作为上线前的门控。
- 依赖：固定评测集（固定样本和固定评测标准）、尽可能贴近生产的固定执行环境。

当 Agent Harness 任何环节发生变化，都可以通过离线评测验证效果，避免不成熟的变更导致 Agent 能力劣化。
- 模型升级、Prompt 调整、知识库更新、Skill 新增或下线

广义的评测集由（问题、参考答案、评价标准）三元组构成，其中问题-参考答案合起来称作评测样本。

但随着 Agent 形态从 ChatBot 演进到长程 Agent，这三元组的具体含义也在发生迁移：

| 内容 | 说明 | 问答 Agent 示例 | 长程 Agent 示例 |
| --- | --- | --- | --- |
| 问题 | 用户的提问或任务描述 | 美团的创始人是谁 | 请帮我制作一个 PPT，下面是大纲…… |
| 参考答案 | 预设答案。当参考答案唯一且明确时，就是常说的 ground truth；长程场景下更多是 expected behavior（预期行为）而非唯一答案 | 王兴。王兴毕业于清华大学，于 2010 年创建了美团网…… | 交付 1 个 PPT，且章节结构对照大纲 |
| 评价标准 Metrics & Rubrics | 从多个角度衡量“好不好”的具体指标。在评价非 ground truth 类型问题时起关键作用 | 1. 答案是否包含“王兴”（必过项）   2. 答案是否有关于王兴的介绍（加分项） | 1. 交付产物是否为 PPT（必过项）   2. PPT 章节是否对照大纲（必过项） |

Agent 评测从“**答案**评测”走向“**行为**评测”。
- 短程场景下，参考答案是可逐字比对的字符串；
- 长程场景下，参考答案变成了一段对执行过程的描述，评测要看 Agent 走过的路径是否符合预期，以及最终环境状态是否达成目标。

Anthropic《Demystifying evals for AI agents》文中对长程 Agent 评测 Task 定义：
> 为“具有明确输入和成功标准的单个测试”，这个概念同样可以泛化到短程 Agent 领域。

评测集每一行三元组都可看做 Task。
- 要有固定输入，比如 Query / answer，或者 prompt / expected behavior；
- 评价部分由 Metrics 和 Rubric 构成，其中 Rubric 是最小粒度的评测标准。

<img width="900" height="100%" alt="image" src="https://github.com/user-attachments/assets/3ed90212-3714-4c61-acb2-abd3b7cb672c" />

离线评测做得再丰富多样，也无法穷举所有场景，而在线评测接受真实世界得分反馈，则可以弥补这部分短板。

在线评测和在线监控处理的是线上真实运行时的质量观察。二者关注的层面不同，但有一块重要的交集 —— **巡检**。
- **在线评测**包括 AB、影子模式和巡检，用于在真实线上环境中观察 Agent 的效果。
  - 三者互补：影子模式在上线前用真实流量兜底，AB 在上线后确认业务价值，巡检在日常持续盯住基本盘。
- **在线监控**则关注 Skill/Tool 成功率、失败率、Token 消耗、异常波动等运行指标。

直观的区分：
- 在线评测回答“系统工作得好不好” —— 质量视角
- 在线监控回答“系统有没有在正常工作”。—— 运维视角

Skill 调用成功率 100% 但每次都返回了错误的数据，监控是绿的，评测是红的。

常见的监控维度包括：
- 可用性类：Skill/Tool 调用成功率、失败率、超时率、异常类型分布。这是最基础也最容易见效的一层。
- 成本类：Token 消耗、单任务平均步数、平均耗时。
- 行为监控类：任务类型分布、Skill 调用频次分布、平均对话轮次。这一层的价值在于发现用户结构的变化。当某类新任务的占比快速上升，往往意味着评测集需要扩充了。

Case 挖掘与归因：驱动双环演进的枢纽

Case 挖掘与归因主要承接在线评测和在线监控中暴露出来的问题线索，同时也接收线上反馈、真实样本采样和业务规则筛出的样本。职责分工上：
- Case 挖掘负责把样本收进 Case 池，归因负责继续往下定位，判断 Agent 流程里的核心问题点。这个模块是整个体系的枢纽，也是当下火热的“Agent 自进化”的核心切入点。

挖掘出来的样本进入 Case 池后，可以继续区分为 Good Case 和 Bad Case，分别沉淀成不同类型的资产
- 错题集是回报最直接的一类资产。逻辑很朴素：每一个曾经犯过的错，都不应该再犯第二次。
- 而黄金集的价值容易被低估。Bad Case 告诉你哪里不行，但它不能告诉你“到什么程度才算行”。没有黄金集，团队在讨论质量时只能各说各话；有了黄金集，“我们要做到这个水平”就变成了一个可以指着看的具体样本。

| 类型 | 沉淀去向 | 作用 | 使用方式 |
| ---- | ---- | ---- | ---- |
| Good Case | 黄金集 | 定义“什么叫做得好”，是质量的正向标尺 | 每次回测必跑；作为巡检的核心样本；用于对齐团队认知 |
| Good Case（高难度） | 挑战集 | 标定能力边界，衡量上限提升 | 不作为发布门禁，用于观察版本间的能力跃迁 |
| Bad Case | 错题集 | 记录踩过的坑，防止问题复发 | 后续版本必须反复回归；修复后从“未通过”转为“必过项” |

归因：从“这里出了问题”到“为什么出问题”

归因的目标是定位 Agent 流程里的核心问题点。一个 Bad Case 只能说明“这里出了问题”，还不能说明“为什么出问题”。

归因要继续判断问题发生在哪个环节：常见的做法是将 Agent 执行过程全链路铺开，通过 Trace 日志逐一定位问题点，这个过程与软件问题排查过程中看日志查 bug 高度雷同。正因如此归因高度依赖观测基建 Trace。这个过程可以由人工完成，也可以由机器辅助完成。

可操作的归因分层

| 归因分类 | 归因层级 | 典型表现 | 修复动作 | 责任方 |
| ---- | ---- | ---- | ---- | ---- |
| Agent迭代Loop | 意图理解 | 用户要的是环比，Agent做成了同比 | 调整Prompt、补充few-shot、澄清追问策略 | Agent研发 |
| | 规划与路由 | 该调两个Skill只调了一个；步骤顺序颠倒 | 优化任务拆解策略、修正Skill描述 | Agent研发 |
| | 工具/Skill执行 | Skill参数传错、返回数据解析失败 | 修Skill实现、补充参数校验 | Skill开发者 |
| | 上下文与记忆 | 长链路后忘记了用户最初的约束条件 | 优化上下文压缩策略、引入结构化状态 | Agent研发 |
| | 知识与数据 | 指标口径理解错误、检索到过期文档 | 更新知识库、修正检索策略 | 知识运营 |
| | 基座模型能力 | 复杂推理确实做不对，换模型后消失 | 升级模型、任务降维、引入专家知识 | 算法 |
| 评测迭代Loop | 评测标准本身 | Agent的做法其实合理，是Rubric定义有偏 | 修正Rubric、更新评测集 | 评测负责人 |


归因明确之后，正向 Case 一般可以归入评测集中的黄金集、挑战集；负向 Case 则会进入两条不同的路径：
- 进入 Agent 效果迭代——修复、回测、上线。这是 Agent 迭代 Loop。
- 校验 Rubric，如果现有 Rubric 没有准确刻画风险，则需要迭代 Rubric，同时将 Case 流入错题集。这是评测体系迭代 Loop。

<img width="1080" height="100%" alt="image" src="https://github.com/user-attachments/assets/7c6fc3a8-5725-4fab-a151-d8415ccca0bb" />

很多团队只走了第一条路径——默认“评测说不行就是 Agent 不行”。这种默认假设会带来隐蔽问题：Agent 会被优化成“迎合评测标准”，而不是“解决用户问题”。当评测标准本身有偏差时，优化得越努力，偏离真实需求越远。定期检查“是不是评测判错了”，是评测体系自我校准的必要动作。

Agent 执行是一条长链路：
> 用户输入 → 意图理解 → 任务规划 → 工具/Skill 调用 → 环境交互 → 中间结果处理 → 策略调整 → 最终输出。

只要其中任意一层出问题，最终效果都可能劣化。但如果系统只能看到“用户说了什么”和“最后回复了什么”，就几乎无法判断问题根因。这正是工业界发展出 Trace 系统的动因——将黑盒内部的推理过程进行全路径披露，把所有影响模型输出的输入信息都记录下来。

完整的评测体系概括为四个模块、三种能力、两条 Loop、一套资产：
- 四个模块：离线评测负责守住已知、在线评测与监控负责发现未知、Case 挖掘与归因负责定位和分派、观测基建作为一切的地基。
- 三种能力：发现问题、定位问题、驱动演进。缺一项，体系就会在对应环节卡住。
- 两条 Loop：Agent 迭代 Loop 让能力持续提升，评测体系迭代 Loop 让量具持续校准。二者在 Case 挖掘与归因处共享入口，在评测集处共享资产。
- 一套资产： 覆盖 Agent 各功能模块的端到端和过程评测集，它是 Agent 效果的守门员，是评测体系真正的长期价值，是 Agent 效果稳定性的锚点，也是将来 Agent 自进化的地基。

#### 评测实践

【2026-11-17】[《Agent评测白皮书》业务实践篇：商家 AI 助手的评测与优化闭环实践](https://mp.weixin.qq.com/s/sQrU8O6lj-mYtskuilEDcA)

以商家 AI 助手的**巡检任务**为例，如何构建业务 Benchmark，通过评测器校准和错误分析，同时推动评测体系完善与 Agent 能力提升，并借助图灵支撑持续回归与模型选型，为上述方法在具体业务中的落地提供参考。

**商家广告助手**面向**投放巡检、异常诊断、数据报告和计划编辑**等场景的业务 Agent。

执行任务时，要读取持续变化的真实账户数据、调用多个工具、遵守投放规则，并根据结果给出建议，必要时直接调整投放计划。

因此，能否用于生产，不能只看最终回答是否“像对”，还要验证整个任务是否正确完成：
- 意图和时间范围是否理解准确
- 数据与工具调用是否正确
- 关键规则是否遵守
- 最终账户状态或交付物是否符合预期。

三个问题：
- 任务如何组织
- 执行环境如何构造
- 结果如何判定

业界 Benchmark 的共同思路:
- 让 Agent 在可执行环境中完成完整任务，再通过测试、验证器或 Judge 检查结果。

| 典型 Benchmark | 任务与环境 | 如何判定成功 |
| ---- | ---- | ---- |
| SWE-Bench Pro、Terminal-Bench | Agent 在隔离代码仓库或终端环境中完成**长程任务** | 用测试或任务验证器检查最终产物和环境状态 |
| τ-bench | Agent 在领域规则约束下，与**模拟用户**、API工具和数据库交互并完成**服务任务** | 检查最终数据库状态和回复中必要信息；用 `Pass@k`、`Pass^k` 分别衡量能力上限与执行可靠性 |
| Toolathlon、AutomationBench | Agent 在多工具或跨应用环境中执行**长链路业务工作流** | 用确定性验证器检查工作流执行后的最终状态 |
| Agents’ Last Exam | Agent 完成长程、具有实际经济价值的专业任务并形成交付物 | 用确定性规则或 LLM Judge 检查最终环境状态与交付物质量 |

公开 Benchmark 可帮助设计评测，但成绩不能直接作为商家广告助手的上线依据。 因为覆盖的任务、业务规则和数据，与广告投放不同。

但可以复用其**任务设计、环境构造和判定方法**，再围绕广告业务建立 Task 集，配齐执行环境、判定机制和验证框架，验证 Agent 是否满足实际业务要求。

如何把真实业务场景转化为 Task 集，明确成功标准与 Rubric，配置执行环境、判定机制和评测协议，再通过错误分析推动 Agent 迭代。

建设目标：可测、可信、可优化

这套评测体系做到三件事：
1. 可测：把真实业务流程转化为可执行、可判定的场景和成功标准。
2. 可信：稳定、规模化地执行评测，并让过程可观测、结论可复核。
3. 可优化：从评测结果定位根因、验证改动，并逐步连接线上业务效果。

商家广告助手需要完成巡检、诊断等任务。设计 Benchmark
- 首先要明确测哪些业务场景，以及每个场景下怎样算成功。
- 再将这些要求落实为 Task 集、执行环境、判定机制和评测协议，让不同 Agent 版本可以在相同条件下比较。

业务Agent评测体系不是一次性建设完成的测试平台，而是一套从业务任务出发，逐步形成场景、指标、证据、诊断和迭代闭环的业务基础设施。

其他业务不必复制Task和指标，但可以复用建设路径。
- 从**业务任务**出发，而不是从公开数据集出发。公开Benchmark提供通用参照，业务Benchmark负责定义真实生产要求。
- 从**业务风险推导指标**，而不是先有指标再寻找解释。每个指标都应对应具体风险和执行阶段。
- 指标既要能够**衡量**，也要能够**诊断**。任务失败后，应能够下钻到原子检查项和局部证据。
- **评测器和Agent分别迭代**。**尺子变准**和**能力变强**是两个不同的闭环，不能混为同一类收益。离线Benchmark、线上过程指标和业务结果共同构成证据链。离线提升是必要条件，但不能自动推导出业务收益。

真正有价值的业务Agent评测体系，不以Task数量、指标数量或自动化程度为终点。

价值在于：
- 业务问题能够被稳定复现
- 失败能够被快速定位
- 优化能够被可信验证
- 线上变化又能持续反哺下一轮评测和业务迭代。


#### (1) 评测场景设计

评测集构建难点
- 从线上 Bad Case 入手，能够抓住真实问题，但样本容易集中在已经暴露的错误上，难以形成系统覆盖；
- 对于尚未上线或使用量较少的 Agent，可积累的案例也十分有限。

如果由团队主动构造评测样本，又需要回答：应该设计哪些场景，怎样判断关键流程和风险已经覆盖，避免选题只依赖个人经验？

互补路径：
- ① 从**业务 SOP 自顶向下拆解**，确保核心流程和关键分支不遗漏；
- ② 从线上使用和离线测试中的 **Bad Case 自底向上补齐**，覆盖设计阶段难以预见的边界与风险。

两类场景共同组成可持续维护的评测集。

① 从业务 SOP 出发，把每个 Skill 还原为**业务状态图**，明确六类要素：`业务状态`、`数据依赖`、`条件分支`、`提前停止点`、`能力边界`，以及跨 Skill 的**转交点**。

这样得到的，不只是**测试用例列表**，更是“在什么条件下应该做什么、何时应该停止或转交”的**行为规范**。

业务状态图的价值是将“应该怎么做”从隐含在专家经验中的知识，转化为设计评测场景的明确依据。

② 用真实 Bad Case 补齐边界与回归

业务 SOP 描述预期行为，却<span style='color:red'>无法穷举 Agent 在实际执行中的非预期失效</span>。

从线上使用和离线测试中收集 Bad Case，把具体错误抽象为**可复用的失效模式**，再扩展为边界、异常和回归场景。

例如，线上任务抽检中，商家要求巡检昨日投放，Agent 输出了一份结构完整的报告，但 Trace 显示其实际查询的是当天数据。
- 一道错题保留被抽象为“日期理解与计算失效”，并进一步覆盖今日、昨日、历史日期和周末等不同情况。

#### (2) 成功标准和判定方法

以到店 KA 巡检任务为例，商家让 Agent “巡检昨日投放”，收到一份报告就算完成了吗？

三个方面拆解：
1. 执行流程遵循业务 SOP 了吗？
  - 观测工具调用顺序是否符合 SOP 设计，例如是否先调用取数工具，再进行门店筛查，接下来再下钻分析，最后输出巡检报告
  - 必要步骤是否都覆盖到，例如数据查询、门店筛查是否存在低效工具调用
  - 是否存在重复工具调用
  - 是否存在非必要步骤或低效步骤，例如多门店下钻分析时，是否并行分析。
  - 条件分支逻辑是否正确执行，例如未发现异常门店时，是否跳过投放层下钻，直接生成巡检报告
3. 执行过程和结论有据可依吗？
  - 工具的参数值是否与任务上下文语义一致，例如查询日期是否对应商家要求的“昨日”
  - 是否选择了正确的工具
  - 调用工具时是否违反静态参数约束
  - Agent输出是否忠实于工具实际返回的数据
4. 确定输出的巡检报告是可交付的吗？
  - 输出结果是否缺失内容，例如是否真的输出了一份巡检报告
  - 输出格式是否遵循必要模板，例如巡检报告必要的表格是否输出了
  - 输出结论是否存在模糊表述

这些检查项构成任务的**评分细则**（Rubric）。其中，必要步骤、顺序调用、正确工具、参数一致性、参数合规性、输出忠实性、输出完整性、输出遵守必要模板作为成功必需项；低效与重复工具调用、规划效率、结论表达等指标主要用于质量分层和问题诊断，不影响任务是否成功。

判定成功时，可以从 Trace 中精确取证的检查项由确定性 Grader 判定，需要理解业务语义和证据关系的部分交给 LLM Grader。

一次巡检通过了检查，还不能说明 Agent 已经可靠：换一种业务场景还能完成吗？同一任务多跑几次，会不会时好时坏？完成任务又要花多少时间和成本？

为回答这些问题，汇总各场景、多次执行的检查结果，并结合运行中的资源消耗，形成五个维度的评测指标：

| 业务关切 | 评测维度 | 关键指标 |
| --- | --- | --- |
| 是否能够完成并稳定解决商家问题 | 任务完成 | 任务完成率<br>Pass@k<br>Pass^k |
| 是否遵循业务SOP | 路径规划 | 工具调用顺序命中率 <br>必要步骤覆盖率<br>低效工具调用率<br>重复工具调用率<br>规划效率<br>条件分支通过率 |
| 执行与结论是否有据可依 | 工具与事实一致性 | 工具选择幻觉率<br>工具参数编造率<br>工具格式违规率<br>工具结果编造率 |
| 结果是否可交付 | 输出质量 | 输出完整性通过率<br>格式合规率<br>结论确定性 |
| 是否适合高效生产运行 | 成本与时延 | 每任务Token用量<br>任务完成耗时<br>TTFT<br>LLM调用轮次 |


- 任务完成率反映整体成功情况，Pass@k 和 Pass^k 分别衡量能力上限与执行稳定性。
- 工具调用顺序命中率、必要步骤覆盖率等指标帮助定位任务成功/失败的主要原因。
- 规划效率、结论确定性等指标观测输出质量。
- Token、LLM 调用轮次、端到端时延和 TTFT 则用于衡量资源消耗与生产运行效率。

#### (3) 评测优化与Agent 迭代（Error Analysis）

Error Analysis 同时驱动两条迭代闭环：
- 修正 Task、Grader 和数据，使评测更加可信；
- 优化 Skill、工具和模型，使 Agent 持续提升。

Case 挖掘与归因是连接两条闭环的枢纽。

<img width="900" height="100%" alt="image" src="https://github.com/user-attachments/assets/31962b39-9462-4254-a15a-79d9ef970dfa" />

评测器本身也会出错。
- OpenAI 审计 138 道难以攻克的 SWE-bench Verified 任务时，发现其中 59.4%存在任务描述或测试设计缺陷。即使广泛使用的 Benchmark，也需要**持续校准**。

商家 Agent 也是：Trace 解析、确定性 Grader 或 LLM Rubric 一旦存在偏差，就可能导致错误归因。

因此，在依据评测优化 Agent 前，需要先确保“尺子”可信。

由业务专家确认的校准集，同时覆盖明确的 Good Case、Bad Case 和边界 Case，并分别验证 `Trace 解析`、`确定性 Grader` 和 `LLM Rubric`，避免用总体一致率掩盖不同环节的问题。
- 确定性 Grader 的校准重点是检查**规则是否准确表达了必要的业务约束**。
- LLM Grader 则重点验证**与业务专家在语义判断上的一致性**。

注意
- 评测误判减少说明尺子变得更准确，不代表 Agent 能力得到提升。
- 只有使用校准后的同一套标准重新执行 Benchmark，才能判断 Agent 是否真正变强。

初始校准并不意味着评测器会永久正确。模型、Agent 和 Skill 持续迭代，业务 SOP 和能力边界会发生变化，账号状态、工具接口和 Trace 格式也可能漂移。

因此，评测器要像被评对象一样**持续维护**。持续校准不等于永久进行全量人工复核。将三种机制结合起来：
- **自动回归**：每次修改 Trace 解析、确定性 Grader 或 LLM Rubric 后，在固定校准集和历史样本上重新执行，检查是否引入新的误判。
- **稳定抽检**：评测运行稳定后，定期随机抽取少量样本进行人工复核，监测人机一致性和数据分布是否发生变化。
- **触发复核**：当模型、Skill或执行环境发生较大变化，指标分布突然异常，或者线上反馈与离线判断明显不一致时，提高人工复核比例。

这套机制下，人的职责是校准标准、处理争议、复核高风险结果和识别新的失效模式。新问题经过确认后，再回流到校准集、Grader和历史回归样本中，形成评测器自身的持续迭代闭环。

任务完成指标告诉我们“是否失败”，分层指标则将问题进一步定位到路由、必要步骤、工具参数、条件分支、事实依据或最终输出等具体检查项。

原子指标能够指出问题发生在哪里，但根因仍需要从执行证据中确认。

同一个“必要步骤缺失”，既可能是 Skill 没有明确约束，也可能是模型在长上下文中遗漏了要求，还可能来自数据、环境或 Grader 异常。

定位到具体检查项后，我们直接查看与该指标关联的局部 Trace、工具参数和返回结果，通常即可确认问题原因和对应的优化点。

只有当指标与 Trace 结论冲突、局部证据不足、同一问题随机出现，或者仍无法区分 Skill 与模型问题时，才进一步查看完整 Trace、重复执行或补充控制变量验证。

这样既利用指标缩小分析范围，也保留 Trace 作为最终判断依据，避免每个 Bad Case 都从头排查完整执行链路，降低问题定位成本。

分层指标显示每日巡检的问题主要集中在四个方面：配置职责混杂、命令路由不唯一、条件分支和停止条件不明确，以及稳定逻辑过度依赖模型。

结合相关局部 Trace 确认根因后，将问题转化为对应的系统优化动作。

优化遵循同一个原则：减少模型需要记忆和自由判断的确定性约束。
- 平台、账号和参数红线由公共配置统一管理，业务分支与停止条件写入 Skill，解析、计算和筛选交给确定性代码；
- 模型则聚焦流程调度、条件理解和业务表达。

Agent 的能力上限和执行效率均明显提升，但 Pass^k 仍显著低于 Pass@k，主要瓶颈已从“不会做”转为“不能稳定做对”，这对后续的优化思路也具有指导意义。

离线Benchmark可以验证能力、稳定性、事实性、Token和时延，却不能直接等同于商家业务收益。

完整的证据链还需要结合**线上过程指标**进行验证，并进一步关联到用户采纳、问题解决和投放效果

图灵将 Task 集、Evaluator 和 Pipeline 保留为可复用的评测资产，让团队沿用已有流程验证新版本，减少重复配置、逐条执行和结果整理。


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
