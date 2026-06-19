---
layout: post
title:  "大模型面试题- Interview for LLM"
date:   2019-12-20 20:08:00
categories: 人生规划
excerpt : 大模型相关岗位面试题合集
tags: 招聘 求职  算法工程师 面试 工业界 学术界 大模型
permalink: /llm_interview
---

* content
{:toc}

# 大模型面试题合集

## 面试信息

详见站内专题：[面试](interview)

## 总结

【2026-1-4】[大模型面试100问：从基础到实战](https://www.80aj.com/2026/01/04/llm-interview-guide/)
- ├─ Cluster 01：基础概念与架构篇（12问）：Transformer架构、注意力机制、位置编码
- ├─ Cluster 02：训练与优化篇（10问）：预训练、微调、RLHF、参数高效微调
- ├─ Cluster 03：推理与部署篇（10问）：KV Cache、量化、Flash Attention、部署框架
- ├─ Cluster 04：Prompt工程篇（8问）：提示词设计、思维链、安全防御,CoT、TOT
- ├─ Cluster 05：RAG与Agent篇（8问）：检索增强生成、智能体架构
- ├─ Cluster 06：评估与安全篇（8问）: 评估指标、幻觉检测、安全防御
- ├─ Cluster 07：特殊架构篇（6问）: MoE、多模态、Diffusion、代码生成
- └─ Cluster 08：开源生态篇（5问）: 开源模型选型、性能对比


大模型题目

| 题目 | 类型 | 考察点 | 合格标准 | 优秀标准 |
|------|------|--------|----------|----------|
| 平时用过哪些大模型产品/工具？ | 产品 | 大模型兴趣程度 | 至少知道3种大模型产品，1种使用 | 多种工具产品，频繁使用 |
| 写一个简历问答机器人的提示词 | 应用 | PE功底 | 兼顾至少3个维度（目标、角色、样例） | 覆盖更多维度 |
| 发一句话给ChatGPT等，模型怎么处理、输出回复？ | 理论 | 大模型原理 | 知道自回归/transformer/注意力 | 细化到transformer内部模块功能、大模型局限性 |
| 上面这句话是如何转换的？ | 理论 | 大模型原理 | 知道分词、embedding | 熟悉分词、embedding细节（如BPE、RoPE） |
| 如何设计一个简历问答机器人？ | 代码 | 代码能力 | - | 知道FT（全参/lora）、cpt等 |
| 1000份简历，怎么办？ | 应用 | agent应用能力 | 知道PE/RAG | agent设计（memory工具） |
| 以简历为数据源，代码实现问答系统 | 代码 | 系统设计，代码能力 | 实现基本流程 | 代码逻辑清晰、边界条件充分 |
| 已有问答系统有什么问题，如何优化？效果+性能 | 应用 | 问题敏感度 | 常规时空复杂度 | 大模型提效、提速方法 |
| 如何设计训练方案（CPT/SFT/RL） | 代码/理论 | 解决能力/训练方法优缺点 | 知道3种方法功能 | 优缺点清晰，base/instruct选型 |
| 为什么选用7b模型（参考简历）SFT方法？ | 理论 | 技术选型严谨性 | 模型规模、数据量、效果权衡 | 衔接scaling law，逐步推理、论证 |
| 实现训练流程（CPT/FT/Lora等） | 理论 | 大模型训练知识 | 训练方式数据处理正确 | 代码框架完成度80%以上 |
| 模型训练：超参如何设计、如何调优、评估？ | 代码/工程 | 代码熟悉度/大模型训练 | 训练流程（pytorch）基本正确；知道常规方法（网格搜索等） | pytorch熟悉（更新梯度/初始化等） |
| 如果7b变成30b，多机多卡，怎么训？ | 工程 | 大模型训练 | 知道GPU显存计算逻辑，分布式基础 | EP/3D并行，deepspeed加速（zero系列），fp16/32，分布式通信机制 |
| 训练过程loss曲线有什么特点，如何调优 | 工程 | 大模型训练 | 1个epoch后大幅下降，bs+lr并行 | 知道spike/震荡/慢等情况处理方法，参数调优快 |
| 解释关键技术点（SFT/LoRA/DPO等，从简历中找） | 理论 | 技术术语理解程度 | 知道主要原理 | 细节、优缺点清晰 |
| DPO是RL吗？ | 理论 | RL理论 | 不是 | DPO是监督学习，不满足RL几大要素 |
| 问答机器人如何部署？ | 理论 | 大模型推理 | 知道vllm之类工具 | vllm/SGLang，page attention/flash attention等优化技术 |
| 大模型能力为什么强？跟BERT什么关系 | 理论 | 大模型原理 | 提到至少3点（海量数据+模型等） | 3点以上且知各比重，BERT原理熟悉，大模型缺点 |
| 大模型有什么问题？ | 理论 | 大模型原理 | 至少3点（幻觉、速度慢、知识旧） | 知道幻觉成因、速度慢解法、DeepSearch等 |
| 大模型能实现AGI吗？ | 理论 | 大模型发展 | 大概率不能 | 知道语言模型/自回归的局限，新方法（世界模型/vla/符号主义等） |

## LLM常见问题

【2023-11-7】大模型面试八股文
- [awesome_LLMs_interview_notes](https://github.com/jackaduma/awesome_LLMs_interview_notes)

大模型高频问题：
- **plugin怎么实现**
  - OpenAI 的 plugin 如何实现？未开源，不知道
  - 推测：question -> embedding 向量化 -> CLS意图识别 -> ranking 按得分排序 -> NER 抽取对应槽位 -> 调用tool -> 结果生成
  - embedding 所用到的语义空间跟 LLM 一致
- **如何与领域知识结合?** 看情况, LLM 具备通用领域的知识
  - 若 LLM 初版结果满足需求 -> prompt 调优
  - 若 LLM 效果不佳 -> 准备领域语料 -> 全参数精调(资源开销大) + 指令微调 IFT -> RM+PPO
  - 若 资源受限/隐私考虑, 仿照 Doc-Chat 文档问答 方案, 通过 LLM工具(如 LangChain/LLaMA-Index) 向量化→chunk索引→生成prompt→调LLM
- **如何落地搜索业务？** 搜索是ChatGPT的天然战场, 检索变问答
  - 目前有些浏览器插件，如: `Monica`, `ChatGPT for Google` 等 
  - 大厂 Google BARD 和 New Bing, 实测 BARD 中文支持不佳，英文还可以，根据 query 搜索wiki百科内容组装成段落
  - 技术: query -> 向量化(同llm语义空间) -> 语义匹配,得到相关文档片段 -> 生成Prompt -> LLM 拼接作答
  - 问题: LLM 推理性能是个大问题, 搜索对时延/并发敏感，怎么解决？见推理提效
    - 语义匹配提效: LSH局部敏感哈希
    - Cache
- **如何提升推理速度？** 分训练/预测阶段, 离线/在线场景
  - 训练: 
    - 全参数微调→部分参数微调(部分/冻结), 如: LoRA/QLoRA 系列加速
    - 量化、蒸馏, 降低内存、计算开销
  - 预测: 
    - 量化、蒸馏
    - GPU 升级、并行化
    - Cache 缓存机制
    - generate 解码调参, 如: greedy search, beam search, top-k, top-p, temperature等
- **如何端上部署？**将LLM部署到CPU单机、移动设备
  - 模型小型化
  - 量化，降低精度, 节省内存、计算开销
  - 蒸馏
- **大模型训练思路**
  - 指令集构造 -> SFT/IFT -> RM -> RLHF
  - RLHF非必须，看情况
  - 基座模型选取: 是否开源, 内存计算资源, 中文支持
- **可商用基座大模型哪些?** 找 GPT-3 级别的大模型
  - GPT-2: 基于GPT-2（开源）预训练, Grace就是这样
  - BLOOM: 法国开源的大模型
  - 猎鹰: 阿联酋开源,商用需支付 10%（未必实施）
  - LLaMA: 不能商用
  - ChatGLM: 不能商用,清华暂未公布商用方案, 但有个可商用版本 CPM-Bee
  - 开源组织: 国内如 OpenBMB, OpenBuddy
- **怎么看待ToT**？CoT的进化版，后面迭代的主要方向
  - LLM 推理能力广受诟病, 稍微复杂些，就会胡说八道
  - 人类思考模式: `快思考`(`system 1`,感性,快但不一定正确)、`慢思考`(`system 2`,理性,慢但正确率高)
  - CoT只是链式思考,而 ToT 是树状结构，仿照system 1和system 2，有评估决策单元，按照BFS/DFS遍历可能的路径，择机回溯、剪枝，类似 MCTS（蒙特卡洛树搜索）
  - AutoGPT 代表 LLM 的典型发展方向, 自行思考、决策、行动
- **如何提升PE（prompt engineer）效率**？
  - prompt 结构特殊, 对输入格式敏感, 可能加个标点符号,就无法识别
  - Prompt 工程反人性, 让用户不断尝试，体验不佳
  - 提效方法
    - prompt智能提示, 案例: AIPM工具, 输入框推荐社区共享的优质prompt
    - 产品交互改进: 搜索过程变问答式推荐, 基于用户反馈给于提示, 如短时间内输入重复/相似问题，大多是答案不满意,这时系统提示候选prompt
    - prompt tuning: LLM 基础上执行 p-tuning(清华有专用工具), 提升prompt泛化能力
- [Langchain](https://wqw547243068.github.io/doc-chat#langchain)原理、用法，类似的还有 LLaMA-Index
  - 一款知名的LLM框架工具, 几分钟内构建 GPT 驱动的应用程序。LangChain 可以帮助开发者将LLM与其他计算或知识源结合起来，创建更强大的应用程序。将语言模型与其他数据源相连接，并允许语言模型与环境进行交互，提供了丰富的API：与 LLM 交互；LLM 连接外部数据源
  - 应用程序包括（但不限于）：
    - 聊天机器人
    - 特定领域的总结和问答
    - 查询数据库以获取信息然后处理它们的应用程序
    - 解决特定问题的代理，例如数学和推理难题
  - LangChain 包含六大组件：Models、Prompts、Indexes、Memory、Chains、Agents。

其它
- tokenizer 差异
- deepspeed 加速方式->其他框架的加速方式
- gptq 怎么实现的
- lora qlora
- bloom llama 差异->所有大模型之间有些什么差异
- 大模型的广视野是怎么实现的
- 全参数sft的问题->解决方案
- 如何设计一个好的prompt
- 如何解决幻觉问题
- 大模型的优化器
- prompt 为什么起作用
- 传统NLP模型怎么实现 one-shot few-shot
- ppo-ptx（或者所有的loss）的物理意义是什么
- ICL CoT 概念 设计的目标
- 生成结果的评价方式
- 引入提示指令集的sft对原本任务的影响（会变坏吗？为什么？怎么办？）
- 如果ChatGPT的效果比自研的模型好为什么还要自己train

【2023-9-10】[大模型面试八股含答案](https://www.toutiao.com/article/7269690183216415267), [知乎原文](https://zhuanlan.zhihu.com/p/643560888)


#### transformer原理

跟RNN的区别，自注意力原理，多头注意力作用

- 用pytorch实现单头self-attention（mid+）
- self-attention的细节和一些扩展理解；




#### GPT-3 与 ChatGPT（Instruct GPT）区别

三步流程详解：
- SFT
- RM
- PPO

#### 涌现能力原理、原因、条件

Instruct GPT 论文：
- 符尧：模型到一定规模，才会出现涌现能力
- 问题：为什么 1.3b 的模型效果比 175b的GPT-3 好？



# 结束
