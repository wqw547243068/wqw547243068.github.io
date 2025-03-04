---
layout: post
title:  Agent 智能体应用
date:   2025-01-23 08:26:00
categories: 大模型
tags: Agent 角色模拟 多模态 kaggle 操作系统 agi
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


## 复杂任务


尽管 LLMs 在单一任务上表现出色，面对**复杂、多步骤**的项目处理时，仍存在显著缺陷。
- 以数据分析项目为例，涉及需求理解、数据清洗和预处理、探索性数据分析、特征工程和建模等多个环节。每个步骤都需要专业知识和细致的规划，通常需要多次迭代，门槛非常高。

### AutoKaggle

【2024-11-25】[大幅降低数据科学门槛！豆包大模型团队开源 AutoKaggle，端到端解决数据处理](https://mp.weixin.qq.com/s/ea1J2u9KRecAtQyGdFkkoQ)

详见站内专题：[数据竞赛之智能体](kaggle#智能体)


## MusicAgent

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



## 设备操控

当前的多模态大型语言模型 （MLLM） 受制于其训练数据，缺乏有效发挥操作助手功能的能力
- 角色模拟上见站内专题 [agent-角色模拟](simulator#agent-角色模拟)


### 评测集


【2024-10-10】EMNLP2024 [用AppBench一键评测你的手机智能](https://mp.weixin.qq.com/s/6DkJGBCrAtj_TBEgFBDpIw)

港中文 发布 AppBench，一个评估大型语言模型在复杂用户指令下规划和执行来自多个应用的多项API的新基准。
- 论文: [AppBench: Planning of Multiple APIs from Various APPs for Complex User Instruction](https://arxiv.org/pdf/2410.19743) - EMNLP2024
- 作者：王鸿儒 港中文在读PhD
- [主页](https://rulegreen.github.io)

如何评估大型语言模型（LLMs）在复杂用户指令下规划和执行来自不同来源的多个API的能力。

研究难点：
- 图结构：一些API可以独立执行，而另一些则需要依次执行，形成类似图的执行顺序。
- 权限约束：需要确定每个API调用的授权来源。

相关工作：
- API调用评估：如 API-Bank 和 ToolBench等，主要关注**单次或有限参数**的API调用。
- 语言代理框架：如 Chameleon 和 WebShop等，主要关注与**外部工具**的交互。

任务定义：给定用户指令和虚拟移动环境中的APP家族，meta代理需要决定一个可执行路径，调用不同APP中的不同API来完成任务。任务的形式为列表，每个列表项表示一个APP及其对应的API调用。

数据分类：根据每个用户指令中使用的APP和API数量，数据分为四种类型：
- 单APP单API（SS）
- 单APP多API（SM）
- 多APP单API（MS）
- 多APP多API（MM）

数据收集：利用现有的任务导向对话数据集（如SGD），通过LLM和Python脚本生成所需的输入和输出。具体步骤包括：
- 指令获取：从对话中提取用户和系统的发言，输入到LLM中总结用户需求。
- 规划路径：编写Python脚本解析多轮对话中的API调用，形成规划路径。
- 质量评估：使用GPT-4o评分每个指令的流畅性和多样性，确保数据质量。


### 【2023-8】实在 Agent

2023 年 8 月，国人团队“实在智能”，就已率先推出国内外首个“实在 Agent”智能体。

该智能体借助垂直大语言模型 TARS，调用 RPA 和 ISSUT 来完成点击、输入、下载等任务。它无需 API，能够为企业员工配备全能业务专家，实现超自动化执行以及自然对话式交互，堪称智能办公的“AI 个人助理”。用户可以通过实在智能官网下载 AI 产品“实在 Agent 智能体”。


### 【2023-12-21】AppAgent

【2023-12-21】AI能模仿人类在手机上操作APP了

AppAgent可以通过**自主学习**和**模仿**人类的点击和滑动手势，能够在手机上执行各种任务。

它可以在社交媒体上发帖、帮你撰写和发送邮件 、使用地图、在线购物，甚至进行复杂的图像编辑...

AppAgent在50 个任务上进行了广泛测试，涵盖了10种不同的应用程序。

该项目由腾讯和德州大学达拉斯分校的研究团开发。

主要功能特点:
- 多模态代理:AppAgent 是一个基于大语言模型的多模态代理，它能够处理和理解多种类型的信息（如文本、图像、触控操作等）。这使得它能够理解复杂的任务并在各种不同的应用程序中执行这些任务。
- 直观交互:它能通过模仿人类的直观动作（如点击和滑动屏幕）来与智能手机应用程序交互。就像一个真人用户一样。
- 自主学习:AppAgent 通过观察和分析不同应用程序中的用户界面交互。并学习这些交互模式，并将所获得的知识编译成文档。
- 构建知识库:通过这些交互，AppAgent 构建了一个知识库，记录了不同应用程序的操作方法和界面布局。这个知识库随后用于指导代理在不同应用程序中执行任务。
- 执行复杂任务:一旦学习了应用程序的操作方式，AppAgent 就能够执行跨应用程序的复杂任务，如发送电子邮件、编辑图片或进行在线购物。

- [项目及演示](appagent-official.github.io)
- 论文:[AppAgent: Multimodal Agents as Smartphone Users](http://t.cn/A6lKlXC7)
- GitHub:[AppAgent](github.com/mnotgod96/AppAgent)
- ![](https://appagent-official.github.io/static/teaser.png)
- ![](https://appagent-official.github.io/static/pipline.png)


### ScreenAgent

大模型直接操控电脑——ScreenAgent
- [体验地址](https://github.com/niuzaisheng/ScreenAgent)

产品信息:
- ScreenAgent 是一款由吉林大学人工智能学院开发、视觉语言大模型驱动的计算机控制代理。

产品功能:
- ScreenAgent 可帮助用户在无需辅助定位标签的情况下，通过VLM Agent控制电脑鼠标和键盘，实现大模型直接操控电脑的功能。

ScreenAgent 可根据用户的文本描述查找并播放指定的视频

例如，ScreenAgent 可根据用户的文本描述查找并播放指定的视频，或根据用户要求调整视频播放速度。ScreenAgent还能帮用户打开Windows系统的事件查看器，使用office办公软件，例如根据用户文本描述，删除指定的PPT内容。


### 【2024-6-18】Mobile-Agent

[Mobile-Agent-v2问世:AI手机助手全面升级](https://zhuanlan.zhihu.com/p/704115822?utm_psn=1786674594259718145)

2024年初, 北交大和阿里联合推出的Mobile-Agent通过**视觉感知工具**和操作工具完成智能体在手机上的操作，实现了即插即用，无需进行额外的训练和探索，凭借其强劲的自动化手机操作能力迅速在AI领域和手机制造商中引起广泛关注。

【2024-6-18】团队推出了新版本 Mobile-Agent-v2，改进亮点:
- 继续采用**纯视觉**方案、**多智能体**协作架构、增强的**任务拆解**能力、跨应用操作能力以及多语言支持。

参考
- 代码: [MobileAgent](https://github.com/X-PLUG/MobileAgent), 支持本地LLM, only Android OS and Harmony OS (version <= 4) support tool debugging, 安装 adb 工具, 通过 python run.py 启动
- 论文: [Mobile-Agent-v2: Mobile Device Operation Assistant with Effective Navigation via Multi-Agent Collaboration](https://arxiv.org/abs/2406.01014)

Mobile-Agent-v2 也接入到魔搭的[ModelScope-Agent](https://github.com/modelscope/modelscope-agent)
- ModelScope-Agent拥有了 Mobile-Agent-v2完成自动化打车的能力。
- 用户只需输入目的地，ModelScope-Agent即能通过规划、决策和优化等过程，为用户完成叫车服务。
- ![](https://pic1.zhimg.com/80/v2-6e862c21c533106aa77030aeeb193478_1440w.webp)

实际案例，其中包括了:
- 根据指令要求打开了WhatApps并查看了来自「Ao Li」的消息，消息中要求在TikTok中找一个宠物相关的视频并分享给他。- Mobile-Agent-v2随后退出当前应用并进入TikTok中刷视频，在找到一个宠物猫的视频后通过点击分享按钮将视频链接成功发送给「Ao Li」。
- X（推特）中搜索名人「马斯克」，关注他并评论一条他发布的帖子。尽管社交媒体应用往往文字较多，UI布局复杂，但是Mobile-Agent-v2仍旧准确地完成了每一步的操作，尤其是点击关注之后出现的推荐用户挡住了原本的推文，而Mobile-Agent-v2也执行了上划操作并完成评论。
- 随后是在同样复杂的长视频平台YouTube操作的例子。从该演示视频中自然地对篮球运动员进行吹捧的表现来看，Mobile-Agent-v2对于社交媒体和视频平台的操作能力十分惊艳，有成为新一代控评机器人的潜力。
- 另外，在初代Mobile-Agent中评测的那些相对基础的任务，例如安装应用、导航去某个地点等，Mobile-Agent-v2也能完成。
- 最后则是在中文应用小红书和微信的例子，包括在小红书中搜索攻略并评论，以及帮助用户回微信。Mobile-Agent-v2可以根据帖子的内容发布相关的评论，也能根据微信消息的内容生成相关的回复。

在手机操作任务中，智能体通常需要通过多步操作才能完成任务要求。
- 每次操作时，智能体都需跟踪当前任务进度，即了解之前的操作完成了哪些需求，从而根据用户指令推断下一步的操作意图。
- 尽管操作历史中保存了每一步的具体操作和相应的屏幕状态，但随着操作次数的增加，操作历史序列会变得越来越长。
- 操作历史的冗长且图文交错的格式，会显著增加智能体追踪任务进度的难度

经过7轮操作后，输入的操作历史序列长度已超过一万个token，图文交错的数据格式使得智能体追踪任务进度变得异常困难。
- ![](https://pic4.zhimg.com/80/v2-c5d1903a73c36e1191556df409b25807_1440w.webp)

Mobile-Agent-v2 引入了创新的**多代理协作架构**。
- 如图所示，这种架构允许多个AI代理协同工作，以实现更加高效的任务规划和执行。这种协作机制不仅提升了任务处理的灵活性，还显著提高了任务完成的效率。在一些任务中，智能体需要查看天气并撰写穿衣指南。生成指南时，智能体需要依赖历史屏幕中的天气信息。
- Mobile-Agent-v2设计了**记忆单元**，由决策智能体负责更新与任务相关的信息。此外，由于决策智能体无法直接观察操作后的屏幕信息，系统还引入了反思智能体，用于监测并评估决策智能体操作前后的屏幕状态变化，确保操作的正确性。
- ![](https://pic1.zhimg.com/80/v2-139f4e5d92861e5aeb6e57d91f62ed98_1440w.webp)

Mobile-Agent-v2在多项指标上，无论在英文还是非英文场景，都表现出了全面的提升。此外，通过人为增加操作知识（Mobile-Agent-v2 + Know.），性能得到了进一步的增强。


### 【2024-9-7】TinyAgent

【2024-9-7】[边缘智能革命：TinyAgent实现端侧复杂功能调用智能体](https://mp.weixin.qq.com/s/KLjy6RQ1yN_JgpHghM2iGw)
- UC Berkeley [TinyAgent: Function Calling at the Edge](https://arxiv.org/pdf/2409.00608)

大语言模型（LLMs）可开发出通过调用功能来整合各种工具和API，完成用户查询的高级智能体系统。

然而，这些 LLMs 在边缘部署尚未被探索，因为通常需要基于云基础设施，这是由于庞大的模型尺寸和计算需求。

为此，提出了 TinyAgent, 一个端到端的框架，用于训练和部署能够调用功能的特定任务小型语言模型智能体，以在边缘驱动智能体系统。

智能体配备了16种不同的功能，可以与Mac上的不同应用程序进行交互，包括：
- • 电子邮件：撰写新电子邮件或回复/转发电子邮件
- • 联系人：从联系人数据库中检索电话号码或电子邮件地址
- • 短信：向联系人发送文本消息
- • 日历：创建具有标题、时间、参与者等详细信息的日历事件
- • 笔记：在各个文件夹中创建、打开或追加笔记内容
- • 提醒事项：为各种活动和任务设置提醒
- • 文件管理：打开、阅读或总结各个文件路径中的文档
- • Zoom会议：安排和组织Zoom会议

对于这些功能/工具，已经预先定义了Apple脚本，模型所需要做的就是利用预先定义的API并确定正确的函数调用计划来完成给定的任务


训练一个小型语言模型, 并用驱动一个处理用户查询的语义系统。

考虑了Mac上的类似Siri的助手作为一个驱动应用。实现关键组件是
- （i）通过LLMCompiler框架教现成的SLMs进行功能调用
- （ii）为手头的任务策划高质量的功能调用数据
- （iii）在生成的数据上微调现成的模型
- （iv）通过基于用户查询仅检索必要的工具的方法称为ToolRAG，以及量化模型部署以减少推理资源消耗，来实现高效部署。

最终模型在这项任务上实现了80.06%和84.95%的TinyAgent1.1.B和7B模型，超过了GPT-4-Turbo的79.08%的成功率。


### 【2024-10-23】ComputerUse

【2024-10-23】Claude 推出 [ComputerUse](https://docs.anthropic.com/en/docs/build-with-claude/computer-use) ，可以像人类一样使用计算机了？查看屏幕、移动光标、点击按钮、输入文本，还能查找代码错误、自动搜集信息填表，并向开发者提供了API

通过 API，开发者可以让 Claude 将指令翻译成计算机指令，从而解放一些枯燥的重复性流程任务。

基准测试中，Claude 在 OSWorld 电脑操作评估测试中获得了 14.9% 的成绩，远超其他 AI 模型的 7.8% 最高分，但与人类的 70 - 75% 的水平相比仍有相当大的差距。当用户提供更多完成任务所需的步骤时，Claude 的得分可以提升到 22.0%。

### 【2024-12-23】PC Agent

【2024-12-23】 [刘鹏飞老师组研发PC Agent，让 AI 替你熬夜做 PPT](https://mp.weixin.qq.com/s/4QObP5fUxmKf5m74ZF1vSw)

上海交通大学 GAIR 实验室提出**认知迁移**方法，通过高效收集人类认知轨迹，打造（训练，非 API 调用）了能够像人类一样阅读电脑屏幕，精准操控键盘鼠标，执行长达数十步、跨软件的复杂生产任务的 PC Agent，标志着 AI 真正为人类减负的重要一步
- 论文标题：[PC Agent: While You Sleep, AI Works - A Cognitive Journey into Digital World](https://arxiv.org/pdf/2412.17589)
- 代码地址：[PC-Agent](https://github.com/GAIR-NLP/PC-Agent)

Sam Altman 说，比起让智能体「**订一家餐厅**」，真正有趣的是让它「**咨询 300 家餐厅**」来找到最符合的口味。这样**大量重复性**的工作，对 PC Agent 而言也不在话下。

PC Agent 也能轻松对标类似 Claude 3.5 Sonnet 的演示任务 —— 展现 “AI 调用 AI” 完成工作的巧妙设计。

### Browser Use

[Browser Use](https://browser-use.com/) —— 智能上网神器，轻松畅游互联网

让 AI 像真实用户一样自然操作浏览器的 Python 工具库，通过简单代码配置实现**网页自动化任务**，如订票、求职申请、数据收集等实际应用场景。
- Github [browser-use](https://github.com/browser-use/browser-use)

功能
- 让 AI 能够像人类一样浏览和操作网页
- 支持多标签页管理
- 可以提取网页内容和进行视觉识别
- 能够记录和重复执行特定操作
- 支持自定义动作（如保存文件、推送数据库等）

评测
- `Browser Use` 大幅领先 `Web Voyager`, `Computer Use`, `AgentE`, `Runner H 0.1`

实际应用案例：
- 自动搜索和申请工作机会
- 自动查询航班信息
- Hugging Face 上搜索和保存模型信息


#### 使用

pip:

```sh
pip install browser-use
#（可选）安装剧作家：
playwright install
```

启动代理：

```py
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

async def main():
    agent = Agent(
        task="Find a one-way flight from Bali to Oman on 12 January 2025 on Google Flights. Return me the cheapest option.",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)


asyncio.run(main())
```

并且不要忘记将 API 密钥添加到.env​文件中。

```sh
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```


【2025-3-3】 实践

官方示例无法运行，浏览器一直卡在空白页，无法动弹
- [issue](https://github.com/browser-use/browser-use/issues/839#issuecomment-2689881272) 里提到原因是 deepseek 模型不支持多模态问答，导致页面卡主
- 解法: Agent 初始化参数里，增加参数，关闭视觉交互功能

修正后的代码

```py
# pip install browser-use
# #（可选）安装剧作家：
# pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple/
# playwright install
# pip install langchain_openai langchain

from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

API_KEY='sk-d9c612ac9d3d460eb78f865d3674f862'

chat = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key=API_KEY,
    openai_api_base='https://api.deepseek.com',
    max_tokens=1024
)

res = chat.predict('你好')
print(f'[Debug] 大模型接口有效性验证, 返回结果: {res}')

task_desc="Find a one-way flight from Bali to Oman on 12 January 2025 on Google Flights. Return me the cheapest option."
task_desc = """
打开网易, 找出热门新闻，按照主题汇总，返回5条国际政治新闻
"""
# task_desc = "打开财联社https://www.cls.cn/telegraph，获取前十条资讯"

async def main():
    agent = Agent(
        task=task_desc,
        llm=chat,
        use_vision=False, # ds 不支持视觉模型, 导致 浏览器卡主,一直空白
        max_failures=2,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```


### 【2024-11-29】GLM-PC

【2024-1-23】[智谱Agent抢跑OpenAI，GLM-PC一句话搞定一切！网友：有AGI那味了](https://news.qq.com/rain/a/20250123A082TM00)

智谱 [GLM-PC](https://cogagent.aminer.cn/): 电脑智能体大模型
- LLM for Computer Use
- 基于CogAgent视觉语言大模型构建的电脑智能体

全球首个面向公众、回车即用的电脑智能助手的诞生,，小名叫「牛牛」

GLM-PC
- 2024年11月29日, 正式发布并开放内测
- 2025年1月23日， 最新的v1.0版本引入了“深度思考”模式，该模式在逻辑推理和代码生成方面进行了针对性的优化，尤其支持Windows系统的无缝操作。
- 逻辑推理和代码生成方面进行了针对性的优化，尤其支持Windows系统的无缝操作。
- GLM-PC Window和Mac客户端已经同步上线

![](https://inews.gtimg.com/om_bt/OBsgDKoFX5zIaS-Ey_bfVlihYoaWKh0jUUdG7LEQkr8_0AA/641)

场景：

|场景|agent操作|分析|
|---|---|---|
| 微信上给xxx发送祝福语，再给他发送一个新春图片和一个新春祝贺视频。| 将任务分解成多个步骤，并对图片内容进行识别，生成相应配文<br>AI瞬间跳转到微信，打开朋友圈，将图片上传，再附上文案，一键发送就搞定了 | ![](https://inews.gtimg.com/om_bt/GIq4OMdffh-F2itpvHSrY8tJPJ-ERQIeMXQ2i9pdBSO7sAA/0) |
||||


智谱已经有了手机智能体`AutoGLM`和电脑智能体`GLM-PC`两大系统，实现了工具使用能力的深度突破。

这两个系统分别覆盖了移动设备和桌面端
- `AutoGLM`在手机上，能够精准操控各类应用，实现跨场景智能交互；
- `GLM-PC`则将电脑端的操作提升到了新的高度，基于视觉语言模型VLM的图形界面智能体GUI Agent，实现逻辑推理与感知认知的结合，凸显出AI对复杂系统工具的掌控力。

智谱AGI
- AI实现L3之后，通过不断优化工具使用能力，正为L4阶段——自主学习发明创新奠定了扎实的技术基础。

### 【2025-1-24】Operator

2024年7月，OpenAI 发布了“从AI到AGI的五步过程”：
- Level 1：Chatbots，AI可以以对话的方式与人互动。
- Level 2：Reasoners，AI科技解决人类水平的问题。
- Level 3：Agents，AI可以作为系统执行一些行动任务。
- Level 4：Innovators，AI可以开发创新性的AI。
- Level 5：Organizations，AI可以完成一个组织完成的工作。

OpenAI 表示自己还只处于 Level 1 阶段，正在靠近 Level 2。

而现在，随着Operator的发布，奥特曼宣布：进入 Level 3 的开始。


【2025-1-24】[OpenAI突发Operator！完全自主玩转浏览器，奥特曼：Level 3时代开启](https://mp.weixin.qq.com/s/NkF7apDWFHhuT2X2YrdHvw)
- 只面向Pro用户，一个月200刀（约合人民币1458元）的大会员。

OpenAI官方介绍：
> Operator是我们的首批智能体之一。这些AI能够独立为你完成工作——只需给它一个任务，它就会执行。

OpenAI总裁 Brockman 就迫不及待地宣布：2025是智能体之年。

Operator 到底有多“独立自主”。
- 几乎可以使用任何网站，无需人类的操作辅助。

场景
- 从 Allrecipes 上找到一份蛤蜊扁面条的食谱，然后把所有的食材都放到我instacart的购物车里？

不同于其他用API或者基于编程接口的Agent，Operator 基于文本的**思维链**进行推理

确认好菜单后，去哪个店下单买菜呢？

人类进一步给出指令，使用 Gus’s，然后Operator就会到对应的网站开始下单。

遇到登录、支付等操作时，Operator会将操作权交还给用户。

在用户实测中，有博主发现如果 Operator 被 Reddit 墙了，它还会自己在搜索时就加入“Reddit”关键词以找到相关帖子。

用户也可以通过添加自定义指令，获得个性化体验。比如设置订机票时的首选航司。

Operator 允许用户保存提示，以便在主页上快速访问，非常适合重复任务，如在购物网站上补货。

Operator 也能同时运行多个任务，就像是打开多个网页那样，比如让它在Etsy上订购个性化的搪瓷马克杯，同时在Hipcamp上预订露营地。

Operator 底层使用全新的模型 `Computer-Using-Agent`（CUA）。

通过将`GPT-4o`的视觉能力和高级推理强化学习相结合，CUA可以进行GUI交互。

Operator 可以看到网页界面内容，使用鼠标、键盘允许的所有操作。由此它可以自动操作，而无需自定义的API集成。

如果遇到问题或者出现错误，Operator 可以利用推理能力自我纠错。并在它卡住需要帮助时，将控制权交还给用户。

CUA 在 WebArena 和 WebVoyager两个基准测试中都取得了SOTA。


### 【2025-2-25】Proxy-lite


【2025-2-25】 Convergence AI 发布轻量级网页自动化助手模型 `Proxy-lite`。
- 基于 `Qwen 2.5-VL-3B-Instruct` 微调的 3B 参数视觉语言模型 (VLM)，能够自主完成网页浏览和操作任务。

Proxy Lite：轻量级（只有3B参数）、开源、能使用电脑的代理助手。

Proxy Lite 是3B参数的视觉语言模型(VLM)，为开源社区带来了最先进的网络自动化能力。

WebVoyager 结果，Proxy Lite 在网络自动化任务中表现出色，资源占用也非常低。
1. Proxy Lite 提供全面的**VLM-浏览器交互框架**，给予企业级浏览器控制能力。
2. Proxy Lite 响应通过三个独特步骤完成，实现了比传统的**提示-预测**模型更好的泛化能力： 
  - 观察：评估上一步的成功情况。 
  - 思考：推理出下一步该做什么。 
  - 工具调用：决定在浏览器中采取哪种行动。
3. 借助类似 DeepSeek R1 执行反馈，Proxy Lite 学会了观察和推理，使其能够在广泛的任务上取得进展。

Each response is separated into three parts:
- `Observation`: assesses the success of the previous step
- `thinking`: reasons through what to do next
- `tool_call`: decides what action to take in the browser

资料
- 项目：[proxy-lite](github.com/convergence-ai/proxy-lite), 含演示视频
- 模型：[proxy-lite-3b](huggingface.co/convergence-ai/proxy-lite-3b)
- Blog：[proxy_lite](convergence.ai/proxy_lite/)


效果评测
- ![](https://convergence.ai/wp-content/uploads/2025/02/Proxy_Launch_Blog_Post_Chart_Large-1-1536x1028.png)

|产品|公司|数字|
| ---- | --- | ---- |
|`Proxy` | Convergence |88%|
| `Operator` | OpenAi |87%|
|`Agent E` | Emergence |73.1%|
|`Proxy Lite` | Convergence |72%|
| `Runner H` | H Company|67%| 


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


### 狼人杀

【2023-10-13】清华用agent实现狼人杀
- [清华大学团队让7个大模型玩起狼人杀并发现新的涌现策略行为](https://zhuanlan.zhihu.com/p/659899800)
- [量子位](https://www.qbitai.com/2023/09/84398.html)
- 论文: [Exploring Large Language Models for Communication Games: An Empirical Study on Werewolf](https://arxiv.org/pdf/2309.04658)

通过让llm agent玩狼人杀，观察过程中涌现的“信任、对抗、伪装和领导”现象
- ![](https://pic2.zhimg.com/v2-5bb8b1a99b38d1f729fce371f42828bd_r.jpg)

狼人杀
- 不同玩家扮演不同的角色，如村民、狼人、女巫、预言家和守卫。
- 不同角色又结成不同的阵营——狼人和好人，互相都以杀死对方作为自己的终极目标。

狼人杀、谁是卧底、扑克等游戏的共同点是:
- 游戏开始时，玩家之间掌握的信息是**不完全透明**的，玩家通过发表自然语言形式的内容来传递信息。
- 此外，这些游戏都蕴含着一定的决策问题。

每位玩家需要根据自己掌握的信息推理和决策下一步的行动，进而实现自己的游戏目标。

以往有研究工作对这类问题进行过研究。

例如，有人使用规则分析来玩狼人杀，也有人使用强化学习和内容模板完成对局。

但以往的工作普遍存在共同的局限性:
- 一是对发言内容的严格限制。使用规则或内容模板导致智能体的发言内容仅局限于少量的模板。
- 二是对训练数据的较高需求。为了训练出合理的策略，需要使用大量的人类对局数据。并且，为5人制游戏训练出的策略很难直接迁移到7人制的游戏中去。

LLM的出现为构建聊天游戏智能体并克服上述局限带来希望。大模型具有出色的自然语言理解和生成能力，也具有一定的决策能力。在这篇研究工作中，作者尝试探索使用LLM解决这类问题的效果。

LLM新的涌现策略行为:信任、对抗、伪装和领导

这七个ChatGPT的对话中体现了人类游戏中的`信任`(trust)、`伪装`(camouflage)、`对抗`(confrontation)、和`领导`(leadership)。
- **信任**。这里的信任不是简简单单地直接同意别人发言的观点，而是随着游戏的进行，智能体通过自己的理解逐渐建立起对潜在盟友的信任。这种信任既有对潜在盟友的保护、观点认同，也有对可能敌人的质疑。
- **对抗**。对抗行为是一种反抗潜在敌人的行为，如质疑其他智能体的观点、保护可能暴露身份的盟友、合作投杀潜在的敌人等。对抗行为不是对游戏规则的简单遵循，而是经过某种分析后涌现出的策略行为。例如，玩家5在前期的发言中暴露了自己的好人身份，它没有向他人求助也没有被提示应该被保护。
- **伪装**。尽管很多人常识性地认为经过RLHF的LLM不会说谎话，但LLM扮演群体博弈角色时还是聪明地展示出了伪装自己的能力。它会在前期尽量保持自己的身份不被提及，甚至会把自己伪装成无辜的村民。作者在论文中辨析了这种伪装行为和幻觉生成的本质区别，指出这是一种有理由、有目的的伪装，而非错误的幻觉生成。
- **领导**。领导行为也是群体智能行为中比较重要的一种行为，它起着推动局势发展、诱导信息扩散的重要作用。作者观察到LLM能像人一样扮演这样的领导角色，号召其他智能体按照有利于自己的方向行事（发言或行动）。

四个关键点，分别是有**价值信息**V、**经过选择的提问**Q、**反思机制**R和**链式思维推理**C。

消融实验结果表明，其中Q和C对的玩家发言合理性(由人工进行评判)的影响最大。




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



# 结束
