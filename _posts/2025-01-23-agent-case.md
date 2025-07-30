---
layout: post
title:  Agent 智能体应用
date:   2025-01-23 08:26:00
categories: 大模型
tags: Agent 角色模拟 多模态 kaggle 操作系统 agi manim 可视化 dqn 强化学习 自学习 进化 俄罗斯方块 字节 电商
excerpt: 大模型 LLM 驱动的智能体如何应用？
mathjax: true
permalink: /agent_usecase
---

* content
{:toc}


# Agent 智能体 应用


Agent项目: 

2024年阿里全球**数学竞赛**AI赛道全球第2
- 代码仓库:[Math-Multi-Agent](https://github.com/isaacJinyu/Math-Multi-Agent)
- 特工宇宙 GitHub 组织:‍‍‍‍‍[Agent-Universe](https://github.com/Agent-Universe）


【2024-1-25】这几天agent操控设备成为热点：
- 智谱昨天推出 glm-pc 1.1，注重长程推理，与年前的autoglm互补，分别占据pc和mobile设备
  - 智谱agent手机端 [AutoGLM](https://agent.aminer.cn/)
  - [GLM-PC](https://cogagent.aminer.cn/home) 
- openai 的 operator 也涉足pc操控

大家都在布局3级别agi

2025 是智能体之年


## Agent 效果


### 榜单

【2025-3-26】俄亥俄州立大学、加州伯克利推出 Web助理效果评测 [An Illusion of Progress? Assessing the Current State of Web Agents](https://tiancixue.notion.site/An-Illusion-of-Progress-Assessing-the-Current-State-of-Web-Agents-1ac6cd2b9aac80719cd6f68374aaf4b4)
- 榜单 [Online-Mind2Web benchmark](https://huggingface.co/spaces/osunlp/Online_Mind2Web_Leaderboard)
- ![](https://tiancixue.notion.site/image/attachment%3A5f3fa326-9834-4542-8fad-bc441764d055%3Aacc_gap_enhanced.jpg?table=block&id=1c06cd2b-9aac-80d6-be12-e5557d9ca999&spaceId=6c7d6ca8-3d8a-4491-b0be-7c81741893a4&width=1420&userId=&cache=v2)



## 数据集


### GAIA

【2023-11-23】 FAIR, Meta, HuggingFace, AutoGPT, GenAI 联合推出评测集
- 466 个问题及作答, 覆盖生活中实际问题，涉及 推理、多模态操控、网页浏览、写代码、通用工具使用
- 其中 300 个问题开源出来, 不含答案，用来维护 排名榜 Leader Board
- 问题难度: 人类简单(92%)，但模型难(含插件的 GPT-4 15%)

资源
- [gaia-benchmark](https://huggingface.co/gaia-benchmark), 文件内容 [main/2023](https://huggingface.co/datasets/gaia-benchmark/GAIA/tree/main/2023)
- 论文 [GAIA: A Benchmark for General AI Assistants](https://arxiv.org/pdf/2311.12983)
- [解读](https://blog.csdn.net/HERODING23/article/details/134934184)

问题分级
- 一级问题: 不需要工具，或最用1种工具，且步骤不超过 5 步。
- 二级问题: 涉及更多步骤，大致在 5-10 步，并且需要综合运用不同工具。
- 三级问题: 近乎完美的通用助手, 执行任意长系列行动，任意数量工具，总体上通用水平

示例
- `Question`: What was the actual enrollment count of the clinical trial on H. pylori in acne vulgaris patients from Jan-May 2018 as listed on the NIH website?
- `Ground truth`: 90


## Agent 项目实例

【2024-9-15】[一个包含15种大模型Agent技巧的项目开源](https://mp.weixin.qq.com/s/_0-xyd7zX1W5tlaGAdT_PA)

从简单到高级，15 个 step-by-step notebook

(1) 初级 Agent
- 简单对话Agent: [simple_conversational_agent.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/simple_conversational_agent.ipynb)
- 简单问答Agent：[simple_question_answering_agent.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/simple_question_answering_agent.ipynb)
- 简单数据分析Agent：[simple_data_analysis_agent_notebook.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/simple_data_analysis_agent_notebook.ipynb)
- 客户支持Agent（LangGraph）：[customer_support_agent_langgraph.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/customer_support_agent_langgraph.ipynb)
- 论文评分Agent（LangGraph）：[essay_grading_system_langgraph.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/essay_grading_system_langgraph.ipynb)
- 旅行计划Agent（LangGraph）：[simple_travel_planner_langgraph.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/simple_travel_planner_langgraph.ipynb)
- GIF 动画生成器Agent（LangGraph）：[gif_animation_generator_langgraph.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/gif_animation_generator_langgraph.ipynb)
- TTS 诗歌生成器Agent（LangGraph）：[tts_poem_generator_agent_langgraph.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/tts_poem_generator_agent_langgraph.ipynb)
- 音乐合成器Agent （LangGraph）：[music_compositor_agent_langgraph.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/music_compositor_agent_langgraph.ipynb)

(2) 高级Agent架构
- 记忆增强对话Agent：[memory_enhanced_conversational_agent.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/memory_enhanced_conversational_agent.ipynb)
- 多智能体协作系统：[multi_agent_collaboration_system.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/multi_agent_collaboration_system.ipynb)
- 自我提升Agent：[self_improving_agent.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/self_improving_agent.ipynb)
- 任务驱动的Agent：[task_oriented_agent.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/task_oriented_agent.ipynb)
- Internet 搜索和总结Agent：[search_the_internet_and_summarize.ipynb](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/search_the_internet_and_summarize.ipynb)

(3) 复杂系统
- 用于复杂 RAG 任务🤖的复杂可控Agent：[Controllable-RAG-Agent](https://github.com/NirDiamant/Controllable-RAG-Agent)


## 操作系统


【2024-12-2】[Android团队“再创业” ！Agent操作系统方向](https://mp.weixin.qq.com/s/YKgiR-gYsWey3_4yvWAf9A)

很多公司都在研究AI智能体框架中的不同组件、不同功能模块，但是/dev/agents相对就更勇敢一下，/dev/agents坚持提出一个完整的第三方操作系统才能是释放其全部潜力的关键

技术理念是：
- 充分释放人工智能代理的潜力，必须构建一个全新的操作系统。
- 打造一个跨设备的云端操作系统，通过整合生成式AI技术，为开发者提供一个标准化的开发框架，并为最终用户创造一个智能化的交互界面。
- 这一平台有望成为AI时代的基础设施，正如Android在移动互联网时代的角色一样。


## 知识问答


### 法律问答

【2024-8-15】[我的Agent拿了全国第十一](https://mp.weixin.qq.com/s/PlffKAvmeePs8ZbqCyq_3A)

基于智谱 GLM-4 大模型和相关业务API构建能回答法律问题的Agent，为法律人士提供专业的辅助咨询服务。

法律问题或简或繁
- **简单**问题: 只是查阅单表和数个字段: 
  - “广东鹏鼎律师事务所的电话邮箱地址分别是什么？”
- **复杂**问题: 涉及跨多表查询、逻辑判断以及统计等操作
  - “(2020)吉0184民初5156号的被告是否为上市公司，如果是的话，他的股票代码和上市日期分别是？如果不是的话，统一社会信用代码是？该公司是否被限制高消费？如果是被限制高消费的涉案金额总额为？请保留一位小数点。”

经验
- 第一，**API编排** vs **Code/SQL生成**。
  - 相较于Code/SQL的生成能力，企业客户会更看重Agent的API编排能力。在具备API资产的情况下，企业内和企业间的交流会更多地通过API，而非直写Code/SQL实现。
  - Agent 要能够编排并依次调用:裁判文书信息、上市公司信息、企业工商注册信息和企业限高消费信息的API以回答较为复杂的问题。
- 第二，对Agent的要求是“**又快又准**”。
  - 比赛的盲盒测试要求Agent在1小时内回答200道问题，对Agent运算速度和精度都有较高要求。而这也与企业的实际场景契合，毕竟企业内绝大多数的信息检索场景相对简单（单表或有限多表/视图，有限的逻辑处理和统计需求），但对响应的速度和精度有近乎苛刻的要求。
- 第三，**Plan** ↑ **Reflection**↓。
  - 对**速度**和**精度**的高要求:Agent能够在Plan阶段“一次搞定”，而非通过Reflection反复修正。
  - 为此，排除了 Multi-Agents 架构，而着重于保证Plan的准确性，并确保一旦Plan正确，Action必然正确:
  - 两个环节:
    - Orchestration（**编排**），依据知识图谱，将自然语言问题编排为大模型友好的“指令序列”；
    - Question Rewrite（**问题改写**），“抹平”问题的缺陷，并依据知识图谱发现隐藏的实体关系。
  - 最终，所有正确回答的问题中，Agent的**首轮正确率**超过了90%。
- 第四，`自然语言` -> `API`，NO！ `自然语言` -> `指令` -> `API`，YES！
  - 自然语言的复杂度和多样性降低了大模型 Function Calling 精度，Agent需要将自然语言“格式化”为指令以提升API调用的准确性。
  - 例如，大模型可以将问题“广东鹏鼎律师事务所的电话邮箱地址分别是什么？”先转化为指令，再进行API调用:
  - 相较于直接调用API，指令更具额外优势:
    - **API命名不可控**，而**指令命名可以富含语义**，有利于大模型进行问题分解；
    - 简洁指令消耗更少Token，从而降低了大模型幻觉的几率，并且提升了Agent的响应速度；
    - 指令和API的1:1对应关系能够确保“Plan正确，则Action正确”。
- 第五，自然语言问题是一个**指令序列**。
  - 自然语言问题可以被大模型转化为一系列指令，即指令序列。如果用函数 `F(X)->Y` 代表指令，比赛中的问题则可以被描述为一个指令序列
  - 用不同类型的指令构成指令序列，指令间可以通过内存进行沟通。通过不断增加指令类型，Agent可以应对更复杂的问题。
  - 指令集合: 查询、统计、比较、存在、格式化、for循环、api调用计数
- 第六，大模型善于指令编排，前提是约束以`知识图谱`和`Few-Shots`。
  - Plan 核心是**编排指令**，生成指令序列以回答问题。
  - 比赛中，即便仅仅使用提示词工程，只要辅以正确的知识图谱和Few-Shots，大模型善于将问题编排为指令序列
  - `知识图谱`主要约束大模型的**生成路径**，而`Few-Shots`则提供了**生成样式**。同时，Agent利用 embedding search 针对不同类型问题动态加载Few-Shots，在节省Token的同时增加了指令序列生成的精度。鉴于指令和API的一一应对关系，指令的编排等同于API的编排。
- 第七，必要的**问题改写**。
  - 指令序列的生成和问题的问法息息相关，而Agent经常面临的挑战在于，问题未必会提到答案中所需的内容。
  - 这种情况下，Agent需要改写问题以“填坑”。类似于指令序列的生成，我们可以同样使用知识图谱和Few-Shots指导问题的改写。
  - 而问题改写的另一好处: 能仰仗大模型“抹平”问题中的错误，例如，问题改写就修正了公司和字段名称重复的错误
- 第八，`<SOS>`/`<EOS>`提升 Few-Shots 遵从性。
  - 使用Few-Shots 产生指令序列的挑战之一就是大模型的“不遵从”，包括:
    - 格式上的不遵从，例如符号的错用；
    - 内容上的不遵从，例如在指令序列之外增加无谓的解释和啰嗦的内容。
  - 通过提示词要求大模型严格遵从输出要求，但更好的办法是使用`<SOS>`/`<EOS>`包裹Few-Shots以提升遵从性
  - 因为大模型在训练之初就使用`<SOS>`/`<EOS>`标记训练数据的起终点，使用该标记后，99.99%的情况下，大模型能够遵从要求生成指令序列。

### 电商问答


【2025-5-18】智能闲鱼客服机器人系统：
- 专为`闲鱼`平台打造的AI值守解决方案
- 实现闲鱼平台 7×24 小时自动化值守，支持多专家协同决策、智能议价和上下文感知对话。
- [XianyuAutoAgent](https://github.com/shaxiu/XianyuAutoAgent)


## 复杂任务


尽管 LLMs 在单一任务上表现出色，面对**复杂、多步骤**的项目处理时，仍存在显著缺陷。
- 以数据分析项目为例，涉及需求理解、数据清洗和预处理、探索性数据分析、特征工程和建模等多个环节。每个步骤都需要专业知识和细致的规划，通常需要多次迭代，门槛非常高。

### AutoKaggle

【2024-11-25】[大幅降低数据科学门槛！豆包大模型团队开源 AutoKaggle，端到端解决数据处理](https://mp.weixin.qq.com/s/ea1J2u9KRecAtQyGdFkkoQ)

详见站内专题：[数据竞赛之智能体](kaggle#智能体)

## 进化

自学习，不断进化


### 【2025-2-18】港大 AutoAgent

【2025-2-18】 [港大开源全自动且高度自我进化的零代码AI Agent框架：AutoAgent](https://mp.weixin.qq.com/s/CQ28CRhCLN3wtdcMCWEzug)

[AutoAgent](https://github.com/HKUDS/AutoAgent) 是**全自动**且**高度自我进化**的框架，用户仅需自然语言即可创建并部署 LLM Agent。
- 论文 [AutoAgent: Fully-Automated and Zero-Code LLM Agent Framework](https://arxiv.org/pdf/2502.05957)

核心特性
- 🏆 GAIA 基准测试冠军
  - AutoAgent 在开源方法中排名 #1，性能媲美 OpenAI 的 `Deep Research`。
- 📚 Agentic-RAG，内置**自管理**向量数据库
  - AutoAgent 配备原生自管理向量数据库，超越 LangChain 等行业领先方案。
- ✨ 轻松创建 Agent 和工作流
  - AutoAgent 利用自然语言轻松构建可直接使用的工具、Agent 和工作流 —— 无需编码。
- 🌐 广泛兼容 LLM
  - AutoAgent 无缝集成多种 LLM（如 OpenAI、Anthropic、DeepSeek、vLLM、Grok、Huggingface...）。
- 🔀 灵活交互模式
  - 支持函数调用（Function-Calling） 和 ReAct 交互模式。
- 🤖 动态、可扩展、轻量级
  - AutoAgent 是你的个人 AI 助手，具备动态、可扩展、可定制、轻量级的特性。

使用方法  
1. 用户模式（SOTA 🏆 对标 OpenAI Deep Research）
  - AutoAgent 内置多智能体（Agent）系统，你可以在启动页面选择用户模式直接使用。这个多智能体系统是一个通用 AI 助手，具备与 OpenAI Deep Research 相同的功能，并在 GAIA 基准测试中实现了可媲美的性能。
  - 🚀 高性能：基于 Claude 3.5 实现 Deep Research 级别的表现，而非 OpenAI 的 o3 模型。
  - 🔄 模型灵活性：兼容任何 LLM（包括 DeepSeek-R1、Grok、Gemini 等）。
  - 💰 高性价比：开源替代方案，无需支付 Deep Research $200/月 的订阅费用。
  - 🎯 用户友好：提供易部署 CLI 界面，交互流畅无阻。
  - 📁 文件支持：支持文件上传，实现更强的数据交互能力。
  - 🎥 Deep Research（即用户模式）
2. Agent 编辑器（无工作流的 Agent 创建）
  - AutoAgent 最具特色的功能是自然语言定制能力。不同于其他 Agent 框架，AutoAgent 允许你仅通过自然语言创建工具、Agent 和工作流。只需选择 Agent 编辑器或工作流编辑器模式，即可开启对话式构建 Agent 之旅。
3. 工作流编辑器（使用工作流创建 Agent）
  - 通过工作流编辑器模式，使用自然语言描述创建代理工作流，如下图所示。（提示：此模式暂时不支持工具创建。）

### 【2025-3-8】AppAgentX 进化

【2025-3-8】西湖大学 推出自学习能力 Agent
- 项目 [AppAgentX: Evolving GUI Agents as Proficient Smartphone Users](https://appagentx.github.io/)

进化框架，提高运营效率，同时保持智能和灵活性

每个步骤，Agent 都会
- 捕获设备的**当前屏幕**并分析，从预定义的作空间中选择合适的作。
- 执行所选作，与 GUI 交互。
- 任务执行轨迹被分解为多个**重叠**三元组。基于这些三元组，生成LLM页面和 UI 元素的功能描述。
- 将合并重复生成的页面描述。
- 整个交互历史记录使用节点链进行记录。

进化机制可识别**重复序列**并创建高级快捷方式，从而显著减少常见任务所需的步骤数和推理。

AppAgentX 在多个基准任务中的效率和成功率都明显优于现有方法。
- 与 GPT-4o 相比, AppAgentX 执行步数、耗时、token花销大幅降低，而准确率最高


## 娱乐

### MusicAgent

【2023-10-20】[MusicAgent:基于大语言模型的音乐理解和生成AI agent](https://mp.weixin.qq.com/s/TImnvhCC8EkRzvau1J5D_g)
- [MusicAgent: An AI Agent for Music Understanding and Generation with Large Language Models](https://arxiv.org/abs/2310.11954)
- github [muzic](https://github.com/microsoft/muzic)
- ![](https://github.com/microsoft/muzic/raw/main/img/concept_map_new.png)

MusicAgent 系统整合了众多与音乐相关的工具，并拥有一个**自动**工作流程来满足用户需求。
- 构建了一个从**各种来源**收集工具的工具集，如 Hugging Face、GitHub和Web API等，并由大型语言模型（如ChatGPT）支持的自动工作流程来组织这些工具。
- 目标: 让用户从AI音乐工具的复杂性中解脱出来，专注于创意部分。

这个系统为用户提供了轻松组合工具的自由，无缝且丰富的音乐体验。


## 角色模拟

详见 [用户模拟器](simulator)专题

## AI助理

【2023-10-19】[不再只是聊天机器人！AutoGen + LangChain = 超级AI助理](https://mp.weixin.qq.com/s/Mrq2OS2AKTgGTdgB_FiQQA)
- AutoGen 代理可以根据特定需求定制，参与对话，并无缝集成人类参与。适应不同的操作模式，包括LLM的利用、人类输入和各种工具。
- AutoGen 没有原生支持连接到各种外部数据源，而LangChain正好发挥作用。两者结合，正是基于OpenAI的函数调用特性。利用 function call，AutoGen Agents能够调用LangChain的接口与组件。

构建AI助理，帮助用户完成知识问答任务
- 使用白皮书构建一个向量存储。
- 基于向量存储，通过LangChain创建会话型基于**检索**的问答链。
- 定义名为 answer_uniswap_question 的函数，接受一个参数question，并调用问答链来回答问题。
- 使用AutoGen设置用户代理和助手代理，并启用函数调用。


### Bland AI

详见站内专题: [大模型时代智能客服](ics)


### CogAgent

【2023-12-15】[CogAgent:带 Agent 能力的视觉模型，免费商用](https://mp.weixin.qq.com/s/qc_G9Dodlkn6Osh2u_XLMw)

- 10月11日，我们发布了智谱AI新一代多模态大模型 CogVLM，该模型在不牺牲任何 NLP 任务性能的情况下，实现视觉语言特征的深度融合，其中 CogVLM-17B 在 14 个多模态数据集上取得最好或者第二名的成绩。
- 12月15日，我们再次升级。基于 CogVLM，提出了视觉 GUI Agent，并研发了多模态大模型CogAgent。

其中，视觉 GUI Agent 能够使用视觉模态（而非文本）对 GUI 界面进行更全面直接的感知， 从而做出规划和决策。

而多模态模型 CogAgent，可接受1120×1120的高分辨率图像输入，具备视觉问答、视觉定位（Grounding）、GUI Agent等多种能力，在9个经典的图像理解榜单上（含VQAv2，STVQA, DocVQA，TextVQA，MM-VET，POPE等）取得了通用能力第一的成绩，并在涵盖电脑、手机的GUI Agent数据集上（含Mind2Web，AITW等），大幅超过基于LLM的Agent，取得第一。
为了更好地促进多模态大模型、Agent社区的发展，我们已将CogAgent-18B开源至GitHub仓库（申请可免费商用），并提供了网页版Demo。
- 论文:[CogAgent: A Visual Language Model for GUI Agents](https://arxiv.org/abs/2312.08914)
- [Demo](http://36.103.203.44:7861)
- 代码:[CogVLM](https://github.com/THUDM/CogVLM)

模型:
* Huggingface: [cogagent-chat-hf](https://huggingface.co/THUDM/cogagent-chat-hf)
* 魔搭社区: [cogagent-chat](https://modelscope.cn/models/ZhipuAI/cogagent-chat)


### Eko

【2025-1-22】[截胡OpenAI！清华复旦等抢先开源智能体框架Eko，一句话打造「虚拟员工」]()

清华、复旦和斯坦福的研究者联合提出了名为`Eko`的 Agent开发框架，开发者可以通过简洁的代码和自然语言，快速构建可用于生产的「**虚拟员工**」。AI智能体能够接管用户的**电脑**和**浏览器**，代替人类完成各种任务，为工作流程提供自动化支持。
- Github [eko](https://github.com/FellouAI/eko)
- 优于 Langchain、Broweruser、Dify.ai、Coze和Midscene.js

[Eko](https://eko.fellou.ai) 是一个强大的Agent开发框架，开发者能用自然语言和简单代码快速构建「虚拟员工」，完成从简单指令到复杂工作流的任务，如股票分析、自动化测试等；通过混合智能体表示、跨平台架构和生产级干预机制等创新技术，实现高效、灵活且安全的自动化工作流程。

核心创新点：
- 混合智能体表示：提出了Mixed Agentic representation，通过无缝结合表达高层次设计的自然语言（Natural Language）与开发者低层次实现的程序语言（Programming Language）。
- 跨平台Agent框架：提出环境感知架构，实现同一套框架和编程语言，同时支持浏览器使用、电脑使用、作为浏览器插件使用。
- 生产级干预机制：现有Agent框架普遍强调自治性（Autonomous），即无需人类干预，而Eko框架提供了显性的生产级干预机制，确保智能体工作流可以随时被中断和调整，从而保障人类对生产级智能体工作流的有效监管和治理。
- ![](https://pic1.zhimg.com/v2-703dcbed3919518575079df0192eb758_1440w.jpg)

Eko的跨平台开发是通过其环境感知架构（Environment-Aware Architecture）实现的，架构由三个关键层次构成：通用核心（Universal Core）、环境特定工具（Environment-Specific Tools）和环境桥接（Environment Bridge）。

通用核心：这一层提供了与环境无关的基本功能，如工作流管理、工具注册管理、LLM（大语言模型）集成和钩子系统。
环境特定工具：每种环境（如浏览器扩展、Web环境、Node.js环境）都提供了优化的工具集。
环境桥接：这一层负责环境的检测、工具注册、资源管理和安全控制，确保不同平台之间能够顺利互动和通信。
安全性和访问控制：Eko针对不同环境实施了适当的安全措施。浏览器扩展和Web环境都采用了严格的权限控制和API密钥管理，而Node.js环境则允许更广泛的系统级访问，基于用户权限进行文件操作和命令执行，在需要时会在执行前请求用户确认。

自动工具注册：通过 loadTools() 等工具，Eko 自动注册适用于当前环境的工具，这使得开发者可以在多个环境中无缝地切换，并确保工具的正确加载。

层次化规划（Hierachical planning）

研究人员提出层次化感知框架，将任务的拆解分为两层，包括Planning layer 和 Execution layer。其中Planning layer负责将用户的需求（自然语言或代码语言表示）和现有工具集拆解成一个有领域特定语言（Domain-specific language）表示的任务图（Task graph）。

任务图是一个有向无环图，描述了子任务之间的依赖关系。该任务图由LLM一次性合成。在Execution layer中，根据每个任务调用LLM来合成具体的执行行为和工具调用。

多步合并优化：当Eko检测到两次执行都是对LLM的调用时，会触发框架的自动合并机制，将两次调用的system prompt自动整合，合并成一次调用。从而加快推理速度。

视觉-交互要素联合感知（Visual-Interactive Element Perception）

视觉-交互要素联合感知框架（VIEP）是一种先进的浏览器自动化解决方案，通过将视觉识别与元素上下文信息相结合，显著提升了在复杂网页环境中自动化任务的准确性和效率。该技术的核心在于提取网页中的交互元素和相关数据，优化了自动化过程，极大地提高了任务执行的成功率。

具体来说，首先VIEP通过识别网页上的关键交互元素——如按钮、输入框、链接等——来聚焦用户可能进行操作的核心区域。

接着，每个可交互的元素都被分配唯一的标识符，并通过彩色框标记，确保精确定位。随后，系统通过结合截图和伪HTML的方式构建元素信息，利用文本和视觉数据的结合，帮助自动化模型更好地识别和操作这些元素，尤其在复杂网页结构中尤为重要。

## 通用智能体


详见站内专题: [通用智能体](general_agent)



## 设备操控

详见站内专题: [设备操控](agent_gui)


## 阅读 Readagent

阅读能力超强的Agent模型——Readagent
- [read_agent_demo](https://github.com/read-agent/read-agent.github.io/blob/main/assets/read_agent_demo.ipynb)

产品信息:
- Readagent是由Google开发的一款模仿人类阅读方式的阅读类型代理（Agent）模型。它通过学习人类阅读长文本时遗忘具体信息但保留要点信息的方式，来提高处理和理解长文本的效率。

产品功能:
- 在处理长文本时，Readagent会把文本中的主要信息转化为“要点记忆”进行存储，当需要回答具体细节问题时，Readagent会迅速定位到到相应的“要点”中寻找答案，从而出色地完成长文本的阅读理解任务。此外，Readagent还能帮用户在复杂的网站中找到需要的信息。



### 会话评估


详见 [用户模拟器](simulator)专题


### 智能教育

【2024-4-12】[用大模型+Agent，把智慧教育翻新一遍](https://www.toutiao.com/article/7357976512986923571)

以正大模型Agent大多采用“群体作战”模式。在Agent社区中，不同角色的Agent可以主动与彼此交互、协同，帮人类用户完成任务。
- `助教Agent`能够实现一对一讲评，成为教师的得力助手；
- `教案Agent`能够生成高质量精品教案；
- `学伴Agent`是学生的学习伴侣，随时提供学习辅导，并为学生制定个性化教学方案。

举例
- 教师将某个学习任务输入助教Agent后
- 助教Agent能够主动将任务分发至各位同学的学伴Agent
- 学伴Agent会主动根据学生的学习习惯制定个性化学习计划，并主动跟踪学生的学习进度和质量，还能将情况即使反馈至助教Agent。

Agent社区形成后，接下来是解决Agent落地“最后一米”的问题——如何设计人与Agent的交互形式。

很多教育场景中，**自然语言交互**并非最佳方式。
- 老师制定教育计划或学生提交作业经常会涉及到四五千字的长文本，这么长的内容放在一个对话流中阅读，非常影响使用体验。
- 现实工作场景中，用户很多时候都需要一个能高效操作的工具，并不是每次人机交互都需要输入一段文字或说一段话

团队最终摸索出集两种交互方式优点于一体的产品形态——用“**白板**”代替简单的**对话流**，支持自然语言驱动的交互方式，并提供内容展示、阅览、回顾等功能，比传统软件交互更简单，但比对话交互更丰富，可深入学校各个业务场景。


## 游戏

详见站内专题: [大模型游戏应用](ai_game)

## 医疗



### Agent Hospital 

医院模拟器 Agent Hospital

【2024-5-5】清华 [【LLM-agent】医院agent：具有可进化医疗agent的医院模拟器](https://mp.weixin.qq.com/s/_0Lc2KNc2npmnCMi3XJPpA)
- [Agent Hospital:A Simulacrum of Hospital with Evolvable Medical Agents](https://arxiv.org/pdf/2405.02957)

基于大型语言模型（LLM）和agent技术构建医疗场景下的**医院模拟体**，命名为`医院agent`（Agent Hospital）。

医院agent不仅包括两种角色（**医疗专业人员**和**患者代理**）和数十个特定agent，还涵盖了医院内的流程如分诊、登记、咨询、检查和治疗计划，以及医院外的阶段如疾病和康复。

医院agent中，论文提出了`MedAgent-Zero`策略，用于医疗代理的发展，该策略不依赖参数和知识，允许通过模拟患者进行无限制的agent训练。该策略主要包括一个医疗记录库和经验库，使得agent能够像人类医生一样，从正确和失败的治疗中积累经验。



### AgentClinic

【2024-5-22】斯坦福、约翰霍普金斯推出 [AgentClinic](https://agentclinic.github.io/)
- [AgentClinic: a multimodal agent benchmark to evaluate AI in simulated clinical environments](https://arxiv.org/pdf/2405.07960)
- 代码 [agentclinic](https://github.com/samuelschmidgall/agentclinic)
- ![](https://agentclinic.github.io/static/videos/mainfigure.png)

AgentClinic 将**静态医疗 QA 问题**转化为临床环境（医生、患者、医疗设备）中的**代理**，以便为医学语言模型提供更具临床相关性的挑战。
- 问题：现有评测标准基于静态QA，无法处理交互式决策问题（interactive decision-making）
- 方案：在临床模拟环境中操作智能体，实现多模态评估LLM
  - AgentClinic: a multimodal benchmark to evaluate LLMs in their ability to operate as agents in simulated clinical environments.
  - 医生通过对话和交互数据来评估病人病情

诊断和管理患者是一个复杂的、连续的决策过程，需要**医生获取信息**---例如要执行哪些测试---并**采取行动**。人工智能 （AI） 和大型语言模型 （LLMs） 的最新进展有望对临床护理产生深远影响。

然而，目前的评估方案**过度依赖静态的医学问答基准**，缺乏现实生活中临床工作所需的**交互式决策**。

AgentClinic：一个多模式基准，用于评估LLMs在**模拟临床环境**中作为**代理**运行的能力。
- 基准测试中，**医生代理**必须通过对话和主动数据收集来发现患者的诊断。

发布两个开放基准：**多模态图像**和**对话环境** AgentClinic-NEJM 和**纯对话**环境。
- AgentClinic-MedQA: 代理以美国医学执照考试~（USMLE） 的案例为基础
- AgentClinic-NEJM: 代理以多模式新英格兰医学杂志 （NEJM） 的案例挑战为基础。

在患者和医生代理中嵌入**认知和隐性偏见** (cognitive and implicit biases)，以模拟有偏见的代理之间的真实互动。

引入**偏倚**会导致医生代理的诊断准确性大幅降低，以及患者代理的依从性、信心和后续咨询意愿降低。通过评估一套最先进的技术LLMs，一些在MedQA等基准测试中表现出色的模型在AgentClinic-MedQA中表现不佳。
- 在AgentClinic基准测试中，患者代理中使用的LLM药物是性能的重要因素。 
- 有限的相互作用和过多的相互作用都会降低医生代理的诊断准确性。


### MMedAgent


【2024-11-3】[斯坦福&哈佛医学院 - MMedAgent，一个用于医疗领域的多模态医疗AI智能体](https://mp.weixin.qq.com/s/vRrYmhjMH0SMgoctBuYpbQ)

斯坦福+哈佛医学院推出 第一个专门为医学领域设计的智能体，名为**多模态医学智能体** （`MMedAgent`）。策划了一个由**六种**医疗工具组成的指令调整数据集，解决了五种模式的七项任务，使智能体能够为给定任务选择最合适的工具。
- 论文: [MMedAgent:Learning to Use Medical Tools with Multi-modal Agent](https://arxiv.org/html/2407.02483v2)
- Github: [MMedAgent](https://github.com/Wangyixinxin/MMedAgent)
- 演示系统 - gradio [demo](https://39bfdd86c8078664d4.gradio.live/)


选择 LLaVA-Med 作为主干，旨在扩展其处理各种语言和多模态任务的能力，包括接地、分割、分类、MRG 和检索增强生成（RAG）。这些任务包括多种医学成像模式，例如 MRI、CT 和 X 射线，使 MMedAgent 能够支持临床实践中通常遇到的各种数据类型。

综合实验表明，与最先进的开源方法甚至闭源模型 GPT-4o 相比，MMedAgent 在各种医疗任务中实现了卓越的性能。此外，MMedAgent 在更新和集成新医疗工具方面表现出效率。


## 教育


### TheoremExplainAgent

【2025-3-5】 加拿大滑铁卢大学用 Manim + Agent 制作5分钟以上的数学教学视频
- 并提出评测集 TheoremExplainBench, 覆盖 240 个理论知识点
- 主页 [TheoremExplainAgent: Towards Multimodal Explanations for LLM Theorem Understanding](https://tiger-ai-lab.github.io/TheoremExplainAgent/)
- 【2025-2-26】论文 [TheoremExplainAgent: Towards Multimodal Explanations for LLM Theorem Understanding](https://arxiv.org/pdf/2502.19400)

o3-mini agent 成功率 93.8%, 总分 0.77

实现方法
- 两个 Agent: 规划 + 写代码
- ![](https://tiger-ai-lab.github.io/TheoremExplainAgent/static/images/method.png)

## 金融

金融交易智能体

详见站内 [大模型与量化](quant#大模型与量化)


## 出行


### 滴滴: AI小滴

【2025-6-10】滴滴推出 智能旅行规划助手 AI小滴, 企业级落地


### 携程

携程+腾讯云 推出旅行规划助手 DeepTrip


## 电商


### CRMAgent

【2025-7-11】[字节跳动：如何用多智能体提升电商CRM？](https://www.xiaohongshu.com/explore/6887a90000000000250203a1)

大多数电商商家在**私域渠道**（如IM、邮件）中进行`客户关系管理`（CRM）时，缺乏高效、专业的消息模板创作能力，导致营销效果不理想。

Georgia Institute of Technology 和 字节跳动的研究团队提出了`CRMAgent`系统，用多智能体大语言模型自动生成高质量CRM消息模板，帮助商家提升用户留存与转化。
- [CRMAgent: A Multi-Agent LLM System for E-Commerce CRM Message Template Generation]()
	
`CRMAgent` 由四个分工明确的智能体组成：
1. `ContentAgent`：分析同一受众群体下表现优劣的模板，总结成功要素。
2. `RetrievalAgent`：跨商家检索与当前活动受众、产品和优惠券类型相近的优质模板，作为参考。
3. `TemplateAgent`：结合诊断和优质范例，重新生成更具说服力的消息模板。
4. `EvaluateAgent`：对新旧模板在受众契合度和营销有效性上进行评分和偏好对比，实现自动化质量评估。
	
效果

用GPT-4o等模型在11大典型用户分群上进行了全面评测。新生成的模板在受众契合度和营销评分上分别提升了**9.09%**和**38.44%**，在盲测对比中有78.44%的概率被评为更优！尤其对“潜在新客户”和“放弃购物车用户”，通过增加紧迫感和明确利益点，极大提升了转化可能。更厉害的是，生成的内容在语义和风格上与原文高度一致，既有创新又不跑题。
	
创新

CRMAgent 不仅分工细致，支持多种数据场景，还通过“组内学习+检索迁移+规则兜底”三重策略，让每个商家都能低成本获得像头部商家一样专业的推送消息，极大降低了营销门槛。该系统为大模型在实际商业场景落地提供了范例，也展现了多智能体协作的巨大潜力。
	
作者信息：Yinzhu Quan（Georgia Institute of Technology）、Xinrui Li（ByteDance Inc.）等人



# 结束
