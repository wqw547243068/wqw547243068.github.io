---
layout: post
title:  DeepAgents 框架介绍
date:   2026-03-01 22:46:00
categories: 大模型
tags: langchain claude deepagents
excerpt: 硅谷新兴概念，新一代Agent框架 Loop Agent实现
mathjax: true
permalink: /deepagents
---

* content
{:toc}


# DeepAgents


## 介绍

【2025-7-30】LangChainAI开发 Python 工具包 [Deep Agents](https://blog.langchain.com/deep-agents/)，快速构建能够处理复杂任务的AI代理。
- [官方中文文档](https://langchain-doc.cn/v1/python/deepagents/overview.html)
- 基于LangGraph 框架，提供内置的规划工具、子代理、虚拟文件系统和详细的系统提示。
- 用户可以通过简单的安装和配置，快速创建支持**长时**任务和**复杂工作流**的智能代理。

将任务规划、子代理管理、文件系统等通用能力封装为内置组件，开发者通过 create_deep_agent 函数仅需数行代码即可搭建复杂智能体，真正实现“搭积木式”开发

Deepagents 适合需要自动化研究、编码或其他复杂任务的开发者，强调开箱即用和灵活定制。

项目采用MIT许可证，代码开源，社区活跃，持续更新。

2025年8月13日，又发布更易上手的交互界面，Deep Agents UI。

教程
- [deepagents-book](https://github.com/lingxingAI/deepagents-book) 从 Harness 工程角度系统拆解 deepagents 项目的中文技术书籍


## 架构

DeepAgents 架构优势

模块化设计：
- 工具（Tools）：扩展 Agent 能力
- 中间件（Middleware）：处理上下文管理
- 技能（Skills）：实现特定领域功能
- 后端（Backend）：支持本地执行

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

create_deep_agent 是 DeepAgents 框架提供的核心工厂函数。
- 接受一个基础模型、工具列表、系统提示词和子智能体列表，返回一个开箱即用的深度智能体。

这个智能体内部已经集成了：
- 任务规划器：将复杂任务拆解为可执行的步骤。
- 文件系统：管理中间结果和上下文，防止对话过长导致混乱。
- 子智能体管理器：负责子智能体的创建、通信和结果汇总。
- 长期记忆：跨对话保存重要信息。

开发者完全不需要关心这些底层逻辑的实现，只需像搭积木一样传入配置即可。

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

### DeepAgents Skills 使用说明


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


# 结束
