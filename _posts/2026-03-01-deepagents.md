---
layout: post
title:  DeepAgents 框架介绍
date:   2026-03-01 22:46:00
categories: 大模型
tags: langchain claude deepagents harness 流式
excerpt: LangChain 新Agent框架 DeepAgent 介绍
mathjax: true
permalink: /deepagents
---

* content
{:toc}


# DeepAgents

传统 Agent 通常采用 `ReAct` 模式：
> 用户输入 → LLM 推理 → 调用工具 → LLM 推理 → 调用工具 → 输出结果。

当任务规模较小时，这种模式运行良好。但随着任务复杂度提升，例如自动生成市场调研报告、分析多家公司财报、编写完整项目代码

就会逐渐暴露出问题：
- 上下文窗口迅速膨胀，超出模型限制
- 推理链过长导致性能下降
- Agent 容易遗忘之前完成的工作
- 多任务之间缺乏隔离，相互干扰
- Tool 调用逻辑越来越复杂，难以维护

Deep Agents 核心目标
- 解决这些复杂任务场景下的工程化问题。


## 介绍

【2025-7-30】LangChainAI开发 Python 工具包 [Deep Agents](https://blog.langchain.com/deep-agents/)，快速构建能够处理复杂任务的AI代理。
- [官方中文文档](https://langchain-doc.cn/v1/python/deepagents/overview.html)
- 基于`LangGraph` 框架，提供内置的规划工具、子代理、虚拟文件系统和详细的系统提示。
- 用户可以通过简单的安装和配置，快速创建支持**长时**任务和**复杂工作流**的智能代理。

将任务规划、子代理管理、文件系统等通用能力封装为内置组件，开发者通过 create_deep_agent 函数仅需数行代码即可搭建复杂智能体，真正实现“搭积木式”开发

Deepagents 适合需要自动化研究、编码或其他复杂任务的开发者，强调开箱即用和灵活定制。

项目采用MIT许可证，代码开源，社区活跃，持续更新。

2025年8月13日，又发布更易上手的交互界面，`Deep Agents UI`。

教程
- [deepagents-book](https://github.com/lingxingAI/deepagents-book) 从 Harness 工程角度系统拆解 deepagents 项目的中文技术书籍


## 安装

deepagents 安装

```sh
# uv 安装
uv init
uv add deepagents tavily-python
uv sync
# pip 安装
pip install deepagents tavily-python
# 兼容OpenAI接口的模型厂商（如 deepseek），可以安装 langchain-openai
pip install deepagents langchain-openai
```

Deep Agents 对模型的唯一要求：
- 支持 tool calling（工具调用）。
- DeepSeek V3 和 DeepSeek R1 系列均支持，可放心使用。


## DeepAgents 架构


安装完即可获得以下能力，无需额外开发：
- 自动任务规划（Planning）
- 文件系统读写（Filesystem）
- 子 Agent 协作（Sub Agents）
- 上下文压缩与管理（Context Management）
- 长任务执行（Long Running Tasks）
- 人工审批（Human-in-the-Loop）
- 持久化记忆（Memory）
- 流式输出（Streaming）


### 架构设计

DeepAgents 全景图

三者并非相互替代，而是可以协同使用：
- LangChain 提供积木，LangGraph 是组织积木的工程框架，Deep Agents 是在此之上开箱即用的高级应用层。
- 任何一个 LangGraph CompiledStateGraph 都可以作为 subagent 传入 Deep Agents，三层可以灵活混用。

![](https://www.runoob.com/wp-content/uploads/2026/06/45542e2c-e404-47ef-a87c-e23ec7f594d4.webp)

模块化设计：
- `工具`（Tools）：扩展 Agent 能力
- `中间件`（Middleware）：处理上下文管理
- `技能`（Skills）：实现特定领域功能
- `后端`（Backend）：支持本地执行

记忆管理：
- 通过 Checkpointer 实现状态持久化
- 支持多线程对话
- 中间件自动摘要优化上下文

技能系统：
- 基于 Markdown 文件定义
- 触发词机制自动激活
- 支持复杂的多轮交互流程

DeepAgents 三大设计原则：封装通用能力、简化开发、模块化组合。
- 封装通用能力：任务规划、子代理管理、文件系统等复杂逻辑全部隐藏在create_deep_agent内部，开发者无需编写任何LangGraph节点和边的代码。
- 简化开发：原本需要数百行LangGraph代码才能实现的深度研究智能体，现在只需几十行配置即可完成。开发者只需关注提示词工程和工具定义。
- 模块化组合：主智能体、子智能体、工具都是独立模块，可以像搭积木一样自由组合、复用。大家可以为其他领域（如数据分析、代码生成）定义不同的子代理，轻松扩展智能体的能力。

LangChain 的 `agent.get_graph().draw_mermaid_png()` 展示DeepAgents 构造的 deepresearch 智能体的图结构
- ReACT 经典结构，并通过 `PathToolCallsMiddleware`, `SummarizationMiddleware` 等中间件扩展了LangChain create_agent 的能力。

通过四大支柱解决**浅层**智能体的局限性：
- （1）详细的系统提示：(Detailed system prompt)
  - 通过精心设计的提示模板（如 few-shot 示例），为智能体提供清晰的行为规范和上下文，确保一致性。
- （2）规划工具：(Planning tool)
  - 引入 Todo List 等工具，让智能体在任务开始前制定全局计划，并在每一步动态调整，避免偏离目标。
- （3）子智能体协作：(Sub agents)
  - 通过任务协调器将复杂任务分解为子任务，分配给专门的子智能体（如数据检索 Agent、分析 Agent），实现高效分工。
- （4）文件系统：(File system)
  - 虚拟文件系统用于存储中间结果、笔记和输出，突破 LLM 上下文窗口限制，支持长期任务和多智能体协作。

<img width="724" height="848" alt="image" src="https://github.com/user-attachments/assets/9492b0c0-1b19-41fa-a070-a611cda9a2f2" />


工作流程
- 系统提示：定义任务目标（如分析特斯拉和丰田的产能）和行为规范。
- 规划：Planner 生成任务列表（如“检索产能数据 → 分析趋势 → 生成报告”）。
- 子智能体协作：各子智能体分别执行数据检索（从行业数据库和新闻）、数据分析（生成趋势图）和报告生成。
- 文件系统：中间结果（如 CSV 数据、趋势图）存储在文件系统中，最终输出整合为 Markdown 报告。

主Agent派生出多个子Agent的两大好处：
- 任务分解：将复杂问题拆解，让每个子 Agent 专注于特定领域，从而实现对该领域的“深度”探索。
- 上下文管理：通过创建拥有独立上下文的子 Agent，可以有效管理信息流，避免主 Agent 的上下文窗口被无关信息淹没。这也被称为“上下文管理和提示快捷方式”。

<img width="684" height="784" alt="image" src="https://github.com/user-attachments/assets/cb9d10ac-2a72-4265-b908-5925e1b61425" />

文件系统不仅用来完成最终任务（如保存代码），还扮演着角色：
- 长期记忆：Agent 可以将中间思考、发现和笔记记录到文件中，以便后续随时读取。这解决了 LLM 有限上下文窗口的问题。
- 共享工作区：所有 Agent（包括主 Agent 和所有子 Agent）都可以访问这个共享空间，实现高效协作。例如，研究子 Agent 可以将发现写入报告，编码子 Agent 则可以读取该报告来指导其工作。

### 模型

Deep Agents 对模型的**唯一**要求：
- 支持 tool calling（工具调用）。DeepSeek V3 和 DeepSeek R1 系列均支持，可放心使用。

### 记忆检查点（Checkpointer）

大模型对话都是无状态的, LangChain 封装了一套方法来**维护对话状态**。
- 如第一次对话问："来一首唐诗"，第二次对话追问："再来一首"，那么大模型会不知道到底再来一首啥。


```py
from langgraph.checkpoint.memory import InMemorySaver

checkpointer1 = InMemorySaver()
```


代码讲解：
- InMemorySaver 是 LangGraph 提供的内存检查点存储
- 用于保存对话状态，实现多轮对话的记忆功能
- 每次对话后自动保存状态，下次可以继续同一话题
- 支持通过 thread_id 区分不同的对话线程


### 中间件 (Middleware)

LangChain 通过中间件方式，处理模型**对话历史过长**的问题

处理的方法有很多，比如消息裁剪等。

将历史对话进行大模型语义汇总的方式，基本方法是将指定久远之外的消息汇总成简短的摘要。

Deep Agents 内置以下中间件，无需额外配置即可使用：

| 能力 | 说明 | 核心组件 |
| ---- | ---- | ---- |
| 任务规划 | 用内置 write_todos 工具将复杂任务分解为有序步骤 | TodoListMiddleware |
| 虚拟文件系统 | 读写文件、将大型工具输出卸载到磁盘，节省上下文窗口 | FilesystemMiddleware |
| 子 Agent | 将子任务委派给独立上下文窗口的专用子 Agent | SubAgentMiddleware |
| 上下文压缩 | 自动总结历史消息，避免超出模型上下文限制 | SummarizationMiddleware |
| Human‑in‑the‑loop | 在关键工具调用前暂停，等待人工审批 | HumanInTheLoopMiddleware |
| 长期记忆 | 跨会话持久化记忆，基于 LangGraph Store | MemoryMiddleware |
| Skills | 按需加载可复用的领域知识与指令集 | SkillsMiddleware |



```py
from langchain.agents.middleware import SummarizationMiddleware

middleware=[
    SummarizationMiddleware(
        model="deepseek:deepseek-chat",
        trigger=("tokens",1000),
        keep=("messages",3)
    )
]
```

讲解：
- `SummarizationMiddleware`：摘要中间件，用于优化长对话的上下文管理
- 作用：当对话过长时，自动将早期对话摘要为简短总结，节省 token 并保持关键信息
- 参数
  - `model`：生成摘要的模型
  - `trigger=("tokens",1000)`：当上下文达到 1000 tokens 时触发摘要
  - `keep=("messages",3)`：保留3 条消息


如果keep的messages设置为3，那么最近的两条message会被完整保留，第三条是根据以前的会话记录summaize下来的信息。

### 文件系统后端

Deep Agents 提供多种后端，控制 Agent 如何读写文件。

💡 后端选型解读
1. **StateBackend**：**内存级**临时存储，线程销毁数据即丢失，适合快速调试Agent逻辑
2. **FilesystemBackend**：**磁盘持久化**，Agent可读写本地文件，生产环境注意文件权限管控
3. **StoreBackend**：LangGraph 官方持久组件，适配**多会话**、**多线程**的对话记忆场景
4. **LocalShellBackend**：赋予 Agent调用终端的权限，**禁止部署在公网环境**，存在高危执行风险
5. **CompositeBackend**：多路分发，可针对不同文件夹绑定不一样的存储后端，适合复杂项目


| 后端 | 存储位置 | 跨会话持久化 | 适用场景 |
| ---- | ---- | ---- | ---- |
| `StateBackend` | LangGraph 图状态内 | 否（同线程内有效） | 默认，本地开发和简单场景 |
| `FilesystemBackend` | 本机磁盘 | 是 | 需要真实读写本地文件，需谨慎使用 |
| `StoreBackend` | LangGraph Store | 是 | 多轮对话持久化、跨 Thread 共享 |
| `LocalShellBackend` | 本机磁盘 + Shell | 是 | 需要执行 Shell 命令，仅限受信任环境 |
| `CompositeBackend` | 路由到多个后端 | 取决于子后端 | 精细控制不同目录的存储策略 |

初学者直接用默认 StateBackend 即可。

`FilesystemBackend` 和 `LocalShellBackend` 会让 Agent 直接操作本地文件系统，严格配置权限后再使用。


本地 Shell 后端



### Harness 设计

Deep Agents 核心哲学是 Harness（马具）
- 不从零实现一套 Agent 运行时，而是在 LangChain 提供的 create_agent 之上，通过 中间件（middleware）、后端（backend） 与 默认系统提示，把「规划、文件、子智能体、上下文压缩」等能力 层叠 上去。

工程收益：
- 复用 LangGraph 的 CompiledStateGraph 生态（流式、checkpoint、Studio 等，README.md 明确强调）。
- 组合优于继承：行为主要通过 create_deep_agent(...) 的 参数（tools、middleware、backend、subagents、skills、memory、interrupt_on 等）声明，而非深继承树。
- 边界清晰：存储与命令执行落在 Backend 协议；工具注入与提示增强落在 Middleware；最终执行图仍由 create_agent → CompiledStateGraph 承担。


## Web UI

方法
- （1）[LangSmith](https://smith.langchain.com/studio)：
  - 要注册langsmith账户才能使用云端web ui
  - [Smith](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024)
- （2）官方还有本地页面 Deep Agents UI，无需访问外网
  - [Deep Agents UI](https://github.com/langchain-ai/deep-agents-ui/tree/main)

### LangSmith

启动 langgraph-cli，自动弹出 [LangSmith](https://smith.langchain.com/studio)
- 可显示动态图、中间状态信息

```sh
cd deepagents-quickstarts/deep_research # 进入项目目录
langgraph dev
```
显示

```sh
╦  ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
║  ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴  ┴ ┴

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
...
```

前提
- 要注册 [LangSmith](https://smith.langchain.com/studio) 账户才能使用云端web ui


### Deep Agents UI

[Deep Agents UI](https://github.com/langchain-ai/deep-agents-ui/tree/main) 是官方提供的 DeepAgents定制UI

安装使用方法

```sh
git clone https://github.com/langchain-ai/deep-agents-ui.git
cd deep-agents-ui

brew install yarn # 准备 yarn 工具包（npm替代品）
yarn install # 编译部署, 本地多了900m文件
yarn dev # 启动w eb 服务
```

弹出本地连接 [localhost:3000](http://localhost:3000)

启动 langgraph

记住部署URL和ID，打开地址 [localhost:3000](http://localhost:3000)，填写以下信息
- URL: http://127.0.0.1:2024
- id: `langgraph.json` 里的 id， 如 'agent'
- langsmith key: *****

进入聊天页面

<img width="1813" height="100%" alt="image" src="https://github.com/user-attachments/assets/541da216-d7c0-4b5c-b0cf-39bdae97ae16" />



## 使用

DeepAgents 依赖基础：
- LangGraph - 提供底层的图执行和状态管理
- LangChain - 工具和模型集成与深度Agent无缝协作
- LangSmith - 通过 LangGraph 平台实现可观察性和部署

DeepAgent 应用程序通过 LangSmith 部署，并使用 LangSmith 可观察性 进行监控。

安装

```sh
pip install deepagents
git clone https://github.com/langchain-ai/deep-agents-ui
```

本地 Web 界面 http://localhost:3000

示例: 
- [官方示例](https://github.com/langchain-ai/deepagents/tree/main/examples)

Deep Agents 分析汽车行业竞争对手的产能数据：

```py
from deepagents import DeepAgent, Planner, FileSystem, SubAgent

# 初始化文件系统用于存储中间结果
fs = FileSystem(directory="./agent_workspace")

# 定义子智能体
data_agent = SubAgent(name="DataRetriever", tools=["industry_api", "web_scraper"]) # 数据检索
analysis_agent = SubAgent(name="DataAnalyzer", tools=["pandas", "matplotlib"]) # 数据分析
report_agent = SubAgent(name="ReportWriter", tools=["markdown_generator"]) # 报告生成

# 配置规划器
planner = Planner(strategy="todo_list", agents=[data_agent, analysis_agent, report_agent])

# 初始化 Deep Agent
deep_agent = DeepAgent(
    system_prompt="Generate a competitive capacity analysis report for Tesla and Toyota, including data, trend charts, and strategic recommendations.",
    planner=planner,
    filesystem=fs
)

# 执行任务
result = deep_agent.run("Analyze Tesla and Toyota's production capacity for 2023-2025.")
print(result)
```

### create_deep_agent

create_deep_agent：一切智能体的起点

create_deep_agent 是 DeepAgents 框架提供的**核心**工厂函数。
- 接受基础模型、工具列表、系统提示词和子智能体列表，返回一个开箱即用的深度智能体。

内部已经集成：
- 任务规划器：将复杂任务拆解为可执行的步骤。
- 文件系统：管理中间结果和上下文，防止对话过长导致混乱。
- 子智能体管理器：负责子智能体的创建、通信和结果汇总。
- 长期记忆：跨对话保存重要信息。

开发者完全不需要关心这些底层逻辑的实现，只需像搭积木一样传入配置即可。

#### 参数说明

| 参数 | 类型 | 是否必填 | 说明 | 默认值 |
| ---- | ---- | ---- | ---- | ---- |
| model | str 或模型实例 | 否 | 模型字符串，格式为 provider:model‑name，或直接传入初始化好的模型对象 | anthropic:claude‑sonnet‑4‑6 |
| tools | 列表 | 否 | 自定义工具函数或 LangChain Tool 对象的列表 | None |
| system_prompt | str 或 SystemMessage | 否 | 自定义系统提示词，用于定义 Agent 角色和行为 | None |
| `backend` | BackendProtocol | 否 | 虚拟文件系统后端，决定文件存储位置 | StateBackend |
| `subagents` | 列表 | 否 | 子 Agent 定义列表，用于任务委派 | None |
| `memory` | 列表 | 否 | 启动时加载的 `AGENTS.md` 文件路径列表 | None |
| `skills` | 列表 | 否 | 按需加载的 Skills 目录路径列表 | None |
| `permissions` | 列表 | 否 | 文件系统路径级别的访问权限控制规则 | None |
| `interrupt_on` | dict | 否 | 指定哪些工具调用需要**人工审批**，需配合 checkpointer 使用 | None |
| `checkpointer` | Checkpointer | 否 | 状态**持久化**检查点，多轮对话或 HITL 时必须设置 | None |
| `store` | BaseStore | 否 | 跨会话的长期存储后端 | None |
| response_format | ResponseFormat | 否 | 结构化输出的 Schema 定义 | None |
| `middleware` | 列表 | 否 | 追加到默认中间件栈末尾的自定义中间件 | () |
| debug | bool | 否 | 开启调试模式，输出详细日志 | False |


#### 示例

代码

```py
from datetime import datetime
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from deepagents import create_deep_agent

from research_agent.prompts import (
    RESEARCHER_INSTRUCTIONS,
    RESEARCH_WORKFLOW_INSTRUCTIONS,
    SUBAGENT_DELEGATION_INSTRUCTIONS,
)
from research_agent.tools import tavily_search, think_tool

# 并发与迭代限制
max_concurrent_research_units = 3
max_researcher_iterations = 3

# 当前日期（用于提示词中的时间信息）
current_date = datetime.now().strftime("%Y-%m-%d")

# 组合主智能体的系统提示词
INSTRUCTIONS = (
    RESEARCH_WORKFLOW_INSTRUCTIONS
    + "\n\n"
    + "=" * 80
    + "\n\n"
    + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
        max_concurrent_research_units=max_concurrent_research_units,
        max_researcher_iterations=max_researcher_iterations,
    )
)

# 定义研究子代理
research_sub_agent = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
    "tools": [tavily_search, think_tool],
}

# 选择底层大模型（此处使用 Claude 4.5，Gemini 3 备选）
# model = ChatGoogleGenerativeAI(model="gemini-3-pro-preview", temperature=0.0)
model = init_chat_model(model="anthropic:claude-sonnet-4-5-20250929", temperature=0.0)

# 创建深度智能体
agent = create_deep_agent(
    model=model,
    tools=[tavily_search, think_tool],
    system_prompt=INSTRUCTIONS,
    subagents=[research_sub_agent],
)
```

### Skills 使用

Agent Skill 的工程化实现步骤：
- 发现与识别 Skills: Agent 需要能够管理文件系统，在配置好的目录中发现 Skills 文件夹。系统会扫描每个子文件夹，读取其中的 SKILL.md，并提取文件头部的 YAML 元数据（即 name 和 description）。
- 系统提示词注入: 将所有 Skill 的元数据（名称 + 描述）注入到系统提示词中，使得大模型在每一轮对话开始时都能清楚看到有哪些技能可用，以及各自的简要用途。
- 渐进式加载: 当模型决定使用某个 Skill 时，系统才会进一步读取该 Skill 的完整说明（即 SKILL.md 的正文），将其加载到上下文中，使后续行动有据可依。
- 任务执行与完成: 模型按照 SKILL.md 中的详细说明，调用必要的工具来访问附加资源，并最终完成任务。

DeepAgents 作为 LangChain 团队的明星框架，对 Skill 的支持相当完善。
- 框架内部已经封装好了 发现、激活、执行 这一完整流程
- 因此开发者只需专注于定义 Skill，然后将 Skill 所在的目录路径传递给 DeepAgents 即可。例如：

```py
agent = create_deep_agent(  
    model=llm,  
    skills=["/skills"] ## 技能包所在目录  
)  
agent.invoke("你有哪些技能？")
```

### 工具

自定义工具 可以注册到 langchain

```py
from langchain.tools import tool

@tool
def query_weather(city:str) -> dict:
    """查询指定城市当前实时天气
    Args:
        city: 需要查询天气的城市名称，例如"北京"
    """
    KEY = "你的key"
    return get_real_time_weather(city,KEY)
```


### 流式输出（Streaming）


【2026-5-6】[LangChain DeepAgents 速通指南（八）—— DeepAgents流式输出详解](https://zhuanlan.zhihu.com/p/2035320007677232066)

DeepAgents 在 LangGraph 的流式输出基础上，提供对`子 Agent` 的流式支持（毕竟多智能体协作也是DeepAgents的核心特性）。

当主 Agent 通过 task 工具将任务委派给子 Agent 时，开发者可独立从每个子 Agent 中流式获取大模型输出和工具调用。

这种多层次、可溯源的流式能力，正是 DeepAgents 区别于普通单 Agent 框架的核心特点。

DeepAgents 底层采用`协调器`-`工作者`架构
- 主 Agent 负责任务规划与委派，每个子 Agent 在自己隔离的沙箱中独立执行，彼此互不干扰。

DeepAgents 流式输出建立在这套架构之上。通过调用 `agent.stream()` 方法驱动整个工作流，框架会源源不断地向外产出结构化的事件块（chunk） 。

推荐 version='v2' 格式下, 每个 chunk 都是统一的 StreamPart 字典，包含三个字段：`type`（事件类型）、`ns`（命名空间）、`data`（主要数据部分）。
- 旧版本输出内容太过复杂，饱受诟病，因此 DeepAgents 推出了 v2 版本的流式输出
- LangGraph >= 1.1

![](https://picx.zhimg.com/v2-3fa7691c7028ac1c31d2ae6d513b3525_1440w.jpg)

有多种流式输出模式

建议：
- 只需要宏观进度追踪，不需要逐字输出？用 updates 足矣。
- 构建打字机效果的聊天界面，并监控工具调用？选 messages。
- 有领域特定的进度需求（如文件处理百分比）？在工具内写入自定义事件，配合 custom 模式。
- 一套代码覆盖所有需求？直接上 组合模式 `["updates", "messages", "custom"]` ，但注意做好事件路由，避免日志混杂

| 模式 | 粒度 | 输出内容 | 典型用途 |
| ---- | ---- | ---- | ---- |
| `updates` | 节点级别 | 每个节点完成后的状态快照 | 追踪执行进度、子Agent生命周期 |
| `messages` | Token级别 | 逐Token文本 + 工具调用块 + 工具结果 | 聊天式UI、工具调用实时监控 |
| `custom` | 自定义 | 开发者通过 get_stream_writer() 写入的任意数据 | 领域特定进度、阶段性通知 |
| 多模式组合 | 混合 | 以上全部事件类型，按到达顺序交织 | 生产级应用、全维度可观测性 |

最佳实践：
- 始终用 version="v2" ：统一的 StreamPart 字典格式消除了不同流式模式下的结构差异，让事件处理代码更加一致。
- 用`命名空间`精确路由事件：不要依赖全局变量或执行顺序来判断事件来源，始终检查 ns 字段，这是最可靠的事件溯源方式。
- 按需组合流式模式：不要盲目开启所有模式，根据场景选择最小必要的模式组合，减少不必要的数据传输和计算开销。

`agent.stream()` 中设置 `subgraphs=True` 时，就能同时接收主 Agent 和所有子 Agent 产生的事件。每个事件的源头由 ns 字段标识：

命名空间	来源
- `()`（空元组）	主 Agent
- `("tools:abc123",)`	通过 task 工具调用 abc123 创建的子 Agent
- `("tools:abc123", "model_request:def456")`	上述子 Agent 内部的 model_request 节点

事件块的 ns 部分用于区分`主 Agent` 和`子 Agent`，而 data 部分主要用于区分不同类型的消息。

data 数据类型是 LangChain 标准消息格式，如 `AIMessage`、`ToolMessage` 等。不同的 Message 类型包含不同的字段，代表不同的内容。

#### updates: 节点级进度追踪

`stream_mode="updates"`: 节点级进度追踪

`stream_mode="updates"` 模式以`节点`（node）为粒度, 返回状态更新
- 每次 Agent 图中的某个节点执行完毕，便会产出一个更新事件。
- 非常适合用来向用户展示宏观层面的执行进度，比如“主 Agent 正在规划”、“子 Agent 正在调用工具”等。

stream_mode='updates' 模式每次依然会等到信息积攒到一定量才输出，和常见的那种“逐字流式”体验还有差距。

`stream_mode="updates"` 模式下，不但输出常规的`事件块`（chunk），还会输出中间件钩子（如 SkillsMiddleware），可以利用这些钩子判断一些特殊事件

判断事件是否来自子 Agent 的规则很简单：
- 只要命名空间（ns）的某一级以 `tools:` 开头，就说明由`主 Agent` 通过 task 工具调用生成的子 Agent 产生的事件。
- 此外，tool_call_id 也可以直接从这段前缀中提取出来，方便后续关联。

对于每个 Agent 中的工具调用情况，在 `stream_mode="updates"` 模式下，可通过分析 data 中的 tool_calls 列表获得。如果某个 tool_calls 列表项的 name 为 task，表示要调用子 Agent；否则表示在相应的 Agent 中调用了普通工具

```py
# stream = updates
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "请分析2026年4月3日伊朗和美国战事的情况(查询1条即可)，并撰写短篇报告分析为什么美国注定失败，500字以内的报告"}]},
    stream_mode="updates",
    subgraphs=True,
    version="v2",
):
    if chunk["type"] == "updates":
        # 主 Agent 更新（命名空间为空）
        if not chunk["ns"]:
            for node_name, data in chunk["data"].items():
                if node_name == "tools":
                    # 子 Agent 结果返回至主 Agent
                    for msg in data.get("messages", []):
                        if msg.type == "tool":
                            print(f"\nSubagent complete: {msg.name}")
                            print(f"  Result: {str(msg.content)[:200]}...")
                else:
                    print(f"[main agent] step: {node_name}")
        # 子 Agent 更新（命名空间非空）
        else:
            for node_name, data in chunk["data"].items():
                print(f"  [{chunk['ns'][0]}] step: {node_name}")
```


#### messages: Token 级流式输出与工具调用

stream_mode="messages"：Token 级流式输出与工具调用

聊天界面“逐字输出”几乎是必备。

`stream_mode="messages"` 模式将生成的每个 Token 逐个流出，并且原生支持主 Agent 和所有子 Agent 同时输出。

同时，工具调用相关事件也完全走这个通道，方便大家一并处理（这是构建系统应用的必备功能）。

messages 模式下，`chunk["type"]` 为 "messages"，其 data 内容是一个二元组 (token, metadata)，其中 token 是 AIMessageChunk 对象（承载主要内容），metadata 包含额外信息。

```py
current_source = ""
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "请分析2026年4月3日伊朗和美国战事的情况(查询1条即可)，并撰写短篇报告分析为什么美国注定失败，500字以内的报告"}]},
    stream_mode="messages",
    subgraphs=True,
    version="v2",
):
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]

        # 判断是否来自子 Agent（命名空间包含 "tools:"）
        is_subagent = any(s.startswith("tools:") for s in chunk["ns"])
        if is_subagent:
            subagent_ns = next(s for s in chunk["ns"] if s.startswith("tools:"))
            if subagent_ns != current_source:
                print(f"\n\n--- [subagent: {subagent_ns}] ---")
                current_source = subagent_ns
            if token.content:
                print(token.content, end="", flush=True)
        else:
            if "main" != current_source:
                print("\n\n--- [main agent] ---")
                current_source = "main"
            if token.content:
                print(token.content, end="", flush=True)
print()
```

#### custom：自定义事件

`stream_mode="custom"`：自定义事件

有时要从`子 Agent` 的工具内部发送完全自定义的进度事件
- 比如一个数据分析工具在处理大数据集时，每隔几秒汇报一次“已处理 30%”。

自定义事件的内容完全由用户决定——进度百分比、状态描述、甚至富文本标记都可以，只要能被下游消费者正确解析。这为构建高度定制化的实时 UI 提供了极大的灵活性

DeepAgents 通过 `get_stream_writer()` 优雅地支持了这一需求，同时使用 `stream_mode="custom"` 来接收这些事件。

```py
from langgraph.config import  get_stream_writer

@tool
def internet_search(
        query: str,
        max_results: int = 5,
        topic: Literal["general", "news", "finance"] = "general",
        include_raw_content: bool = False,
):
    """使用 Tavily API 执行互联网搜索，获取实时或最新的网络信息。

    当需要回答需要当前新闻、最新数据或超出模型知识范围的外部信息时，
    可以使用此工具进行联网搜索。支持普通网页搜索、新闻搜索和金融领域搜索。

    Args:
        query (str): 要搜索的问题或关键词，应清晰、具体地描述所需信息。
        max_results (int, optional): 返回的最大搜索结果数量。默认为 5。
        topic (Literal["general", "news", "finance"], optional): 搜索主题类型。
            - "general"：通用网页搜索，适用于大部分事实性、常识性问题。
            - "news"：新闻搜索，获取近期相关新闻报道。
            - "finance"：金融领域搜索，适用于股票、经济、公司财务等信息。
            默认为 "general"。
        include_raw_content (bool, optional): 是否在结果中包含原始网页正文内容。
            设为 True 会返回更详细的页面文本（可能较长），默认为 False。

    Returns:
        dict: Tavily API 返回的搜索结果对象。通常包含以下字段：
            - "results": 列表，每个元素包含 title、url、content（摘要）等。
            - "query": 原始查询字符串。
            - 若 include_raw_content 为 True，还可能包含 raw_content 字段。
    """
    writer = get_stream_writer()
    writer({"status": "starting", "topic": f'开始搜寻{query}'})
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
```

然后修改流式输出代码，设置 stream_mode='custom'：

```py
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "请分析2026年4月3日伊朗和美国战事的情况(查询1条即可)，并撰写短篇报告分析为什么美国注定失败，500字以内的报告"}]},
    stream_mode="custom",
    subgraphs=True,
    version="v2",
):
    if chunk["type"] == "custom":
        is_subagent = any(s.startswith("tools:") for s in chunk["ns"])
        if is_subagent:
            subagent_ns = next(s for s in chunk["ns"] if s.startswith("tools:"))
            print(f"[{subagent_ns}]", chunk["data"])
        else:
            print("[main]", chunk["data"])
```

#### 多模式组合：一次调用，全维可观测


生产环境中，往往需要同时获取“节点更新 + Token + 自定义事件”多类信息，构建全维度可观测性。

DeepAgents 原生支持在单次 `stream()` 调用中以列表形式组合多种模式：

```py
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "请分析2026年4月3日伊朗和美国战事的情况(查询1条即可)，并撰写短篇报告分析为什么美国注定失败，500字以内的报告"}]},
    stream_mode=["updates", "messages", "custom"],
    subgraphs=True,
    version="v2",
):
    is_subagent = any(s.startswith("tools:") for s in chunk["ns"])
    source = "subagent" if is_subagent else "main"

    if chunk["type"] == "updates":
        pass
    elif chunk["type"] == "messages":
        pss
    elif chunk["type"] == "custom":
        pass
print()
```



## 代码解读


### 整体结构

【2026-6-23】代码结构
- [第 1 章：项目概览与仓库结构](https://github.com/lingxingAI/deepagents-book/blob/main/01-%E9%A1%B9%E7%9B%AE%E6%A6%82%E8%A7%88%E4%B8%8E%E4%BB%93%E5%BA%93%E7%BB%93%E6%9E%84.md)

Deep Agents 官方定位是 batteries-included agent harness（开箱即用的智能体「马具」/ harness）：
- 不强迫使用者从零拼装提示词、工具与上下文管理，而是通过 **可组合**的默认能力 快速得到可运行的智能体，再按需裁剪与扩展。

从工程上看，是 Python **单体仓库**（monorepo）
- 内含多个 独立版本、独立锁文件 的发布包；
- 根目录不设统一的 uv workspace，也没有根级 setup.py，每个包自成一体，由 make 与 libs/Makefile 聚合常见开发任务。

```sh
deepagents/
├── .github/           # CI/CD、脚本、Issue/PR 模板、文档用图片等
├── examples/          # 示例工程（各自 pyproject + uv.lock）
├── libs/
│   ├── deepagents/    # 核心 SDK
│   ├── cli/           # 终端 CLI / TUI
│   ├── acp/           # Agent Client Protocol 集成
│   ├── evals/         # 评测套件与 Harbor 等集成
│   ├── repl/          # REPL 中间件（langchain-repl）
│   └── partners/      # 合作方沙箱/运行时集成（多子包）
├── AGENTS.md          # 贡献者与 AI 辅助开发指南
├── README.md          # 项目对外说明与快速开始
└── release-please-config.json  # 发布与版本自动化配置
```





# 结束
