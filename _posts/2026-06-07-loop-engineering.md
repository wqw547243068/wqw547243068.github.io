---
layout: post
title:  Loop Engineering
date:   2026-06-07 22:46:00
categories: 大模型
tags: gpt ChatGPT langchain go manus 
excerpt: 新一代Agent框架 Loop Agent实现
mathjax: true
permalink: /loop
---

* content
{:toc}

# Loop Engineering


## 浅层 Agent 不足

如何构建“深度”思考和执行复杂任务的 Agent？ 

“浅层”Agent 局限性

主流 Agent 架构在循环中运行，不断调用工具。
- 无法进行长远规划，也难以胜任需要多步骤、深度思考的复杂任务。
- 擅长处理单一、直接的指令，但在面对需要持续数小时甚至数天的研究或编码项目时，往往会迷失方向或过早地认为任务已完成。

借鉴 OpenAI  “Deep Research”、Manus 以及 Anthropic 的 “Claude Code” 等前沿应用的实践，剖析共同要素。

## Loop Engineering

【2026-6-9】
- 原文[Loop Engineering](https://addyosmani.com/blog/loop-engineering/), 译文 [循环工程](https://x.com/cellinlab/article/2064144608242679822)

<img width="1983" height="793" alt="image" src="https://github.com/user-attachments/assets/0b18fbe2-79e5-41a9-aa8d-11597697c1af" />


Loop Engineering 正在取代“亲自给 agent 写 prompt”。
- 核心：不再直接 prompt agent，而是设计一个系统，去 prompt agent。

loop 是一种递归目标：定义一个目的，然后让 AI 不断迭代，直到任务完成。

大致由五个构建块组成，而 `Claude Code` 和 `Codex` 现在都已经具备了这五个能力。

这可能是未来与 coding agent 协作的方式。不过，现在仍然很早期。

必须非常注意 token 成本，因为不同使用模式下的消耗差异可能非常大，尤其取决于你是 token 富裕还是 token 紧张。仍然需要某种方式来确保质量不会下降，对“AI slop”的担忧也完全合理。

最近有人说：
> 你不应该再去 prompt coding agent , 而是设计 loops，让 loops 去 prompt agents。

类似地，Anthropic Claude Code 负责人也说过：
> 我现在已经不直接 prompt Claude 了, 有一套 loops 在运行，会去 prompt Claude，并判断接下来要做什么。我的工作是写 loops。

过去两年里，让 coding agent 做事，基本方式
- 写好 prompt，并提供足够多的上下文。输入一段内容，阅读返回的结果，再输入下一段。
- agent 是一个工具，一直握着这个工具，一轮接一轮地操作。

这部分工作某种程度上已经结束，或者至少正在结束。

现在改构建小系统，自己发现工作、分发工作、检查工作、记录完成情况，然后决定下一步要做什么。让系统去触发 agents，而不是亲自触发。

相近的概念：`harness`。
- harness 是为单个 agent 构建运行环境，也就是那个构建软件的系统。
- Loop Engineering 则位于 harness 之上。像 harness，但它会按时间运行，会生成小 helper，并且会自己喂养自己。

这现在已经不再是“工具问题”了。
- 一年前，做一个 loop，要写一堆 bash 脚本，然后长期维护。
- 但现在，这些能力直接内置在产品里。Steinberger 列出的能力，几乎可以一一映射到 Codex app；同样，也几乎可以映射到 Claude Code。等你意识到它们的形状其实一样时，你就不再纠结到底该用哪个工具，而是开始设计一种 loop：不管你此刻坐在哪个工具里，它都依然能工作。

### 架构

一个 loop 要五样东西，记住状态的地方。
- `Automations`：按计划自动触发，自己做 discovery 和 triage。
- `Worktrees`：让两个并行工作的 agents 不会互相踩到对方。
- `Skills`：把项目知识写下来，避免 agent 靠猜。
- `Plugins` 和 `connectors`：把 agent 接入你已经在用的工具。
- `Sub-agents`：让 agent 负责提出想法，另一个 agent 负责检查。
- 第六件事，是 `memory`。

memory 可以是 markdown 文件，Linear board，或任何存在于单次 conversation 之外、能够保存“已完成事项”和“下一步事项”的地方。


| Primitive     | Job in the loop       | Codex app          | Claude Code          |
|--------------------|---------------------|-----------------------------|---------------------------------------|
| **Automations**    | discovery + triage on a schedule     | Automations tab: pick project, prompt, cadence, environment; results land in a Triage inbox; `/goal` for run-until-done | Scheduled tasks and cron, `/loop`, `/goal`, hooks, GitHub Actions          |
| **Worktrees**      | isolate parallel features           | Built-in worktree per thread                                              | `git worktree`, `--worktree`, isolation: worktree on a subagent            |
| **Skills**         | codify project knowledge            | Agent Skills (`SKILL.md`), invoked with `$name` or implicitly            | Agent Skills (`SKILL.md`)                                                  |
| **Plugins / connectors** | connect your tools              | Connectors (MCP) plus plugins for distribution                            | MCP servers plus plugins                                                   |
| **Sub-agents**     | ideate and verify                    | Subagents defined as TOML in `.codex/agents/`                             | Task subagents in `.claude/agents/`, agent teams                            |
| **State**          | track what’s done                    | Markdown or Linear via a connector                                        | Markdown (`AGENTS.md`, progress files) or Linear via MCP                   |


memory 是每个 long-running agent 都依赖的同一个技巧。

模型在每次运行之间会忘记一切，所以 memory 必须存在磁盘上，而不是只存在 context 里。

agent 会忘记，但 repo 不会。

现在两个产品都已经具备这五项能力。

#### Automations

Automations 是让 loop 成为真正 loop 的东西，而不是只运行一次的任务。

Codex app 里，可在 Automations 标签页中创建 automation。选择项目、要运行的 prompt、运行频率，以及它是在本地 checkout 上运行，还是在 background worktree 上运行。
那些发现了问题的运行结果，会进入 Triage inbox；那些没有发现问题的运行结果，会自动 archive，这点挺好。

OpenAI 内部会用它们处理一些枯燥工作，比如每日 issue triage、总结 CI failures、写 commit briefings、查找上周有人引入的 bug。

automation 还可以调用 skill。这样你就能让重复任务更可维护。你触发的是一个 skill，而不是把一大墙 nobody will ever update 的指令粘到 schedule 里。
Claude Code 到达同一个目标的方式是 scheduling 和 hooks。
- 用 `/loop` 按间隔运行 prompt 或 command；
- 也可以安排 cron task；
- 还可以在 agent 生命周期的某些阶段用 hooks 触发 shell commands；
- 如果希望在合上笔记本之后继续运行，也可以把整套东西推到 GitHub Actions。

本质一样：
- 定义一个 autonomous task，给它 cadence，然后让发现结果来到你面前，而不是由你自己到处检查。

这里还有一个值得了解的 in-session primitive，它更接近本文讨论的核心。
- `/loop` 会按 cadence 反复运行。
- `/goal` 则会一直运行，直到写下的某个条件真的成立。每轮后，一个单独的小模型会检查任务是否完成。写代码的 agent 不是给自己打分的那个。

可以给它个条件，比如：
> all tests in test/auth pass and lint is clean


Codex 也有同样的东西，也叫 `/goal`, 会跨多轮继续工作，直到可验证的停止条件成立，并支持 pause、resume 和 clear。
同一个 primitive，两个工具都有。这基本上也是整篇文章反复出现的模式。

所以，这一部分负责把工作浮现出来。loop 的其余部分，则负责对这些工作采取行动。

#### Worktrees

只要同时运行不止一个 agent，文件就会开始冲突，这会变成失败点。

两个 agents 同时改同一个文件，和两个工程师同时提交同一段代码一样麻烦，而且事先还没沟通过。

`git worktree` 可以解决这个问题。独立的 working directory，位于自己的 branch 上，同时共享同一个 repo history。因此，一个 agent 的修改，字面意义上不可能碰到另一个 agent 的 checkout。
- `Codex` 直接内置了 worktree 支持，所以多个 threads 可以同时作用于同一个 repo，而不会互相撞车。
- `Claude Code` 也通过 `git worktree` 提供了同样的隔离能力。可以用 `--worktree flag` 在独立 checkout 中打开 session，也可以在 subagent 上设置 isolation: worktree，让每个 helper 都获得一个新的 checkout，并在结束后自动清理。

“人”的一面：
- worktrees 可以移除机械层面的冲突，但人仍然是天花板。
- 决定同时运行多少 agents 的，不是工具，而是 review bandwidth。


#### Skills

skill 的作用是不用每次 session 都像金鱼一样重新解释同一个项目上下文。

两个工具都使用相同的格式：一个包含 SKILL.md 的文件夹，里面存放 instructions 和 metadata，也可以附带 scripts、references、assets。
- Codex 会用 `$` 或 `/skills` 调用时运行某个 skill；当 task 与 skill description 匹配时，也可能自动调用。这也是为什么一个紧凑、朴素的 description 比聪明但含糊的 description 更有用。
- Claude Code 的做法也一样。Skills 也是让 intent 不再一遍遍消耗成本的地方。

agent 每个 session 开始时都是冷启动。只要 intent 里有任何空洞，就会用一种自信的猜测把洞填上。

skill 就是把这种 intent 写在外部：项目约定、构建步骤、“不这么做是因为以前发生过某个事故”等等。只需要写一次，agent 每次运行时都会读取。
- 没有 skills，loop 每个周期都要从零重新推导你的整个项目。
- 有了 skills，就开始有一点复利效应。

有一点需要区分清楚：
- `skill` 是 authoring format
- 而 `plugin` 是分发方式。

想跨 repo 共享 skill，或者把几个 skills 打包时，会封装成 plugin。
Codex 是这样，Claude Code 也是这样。

#### Connectors

只能看见 filesystem 的 loop 是很小的 loop。

Connectors 基于 MCP，可以让 agent 读取 issue tracker、查询数据库、调用 staging API、在 Slack 里发消息。

Codex 和 Claude Code 都支持 MCP，所以写的 connector，在另一个工具里也能直接运行。

plugins 还把 connectors 和 skills 打包在一起。这样队友只要安装 setup，而不用凭记忆重建整套东西。

这就是区别
- “agent 说：这里是修复方案”
- “loop 自己打开 PR、链接 Linear ticket，并在 CI 变绿后 ping 频道”

connectors 是 loop 在真实环境里行动的原因，而不只是“如果我能做，我会怎么做”。

#### Sub-agents

loop 中，最有用的结构性设计，远远是把“写的人”和“检查的人”拆开。

写代码的模型，在给自己的作业打分时太友善了。

一个带有不同 instructions、甚至有时使用不同 model 的第二个 agent，能抓住第一个 agent 自我说服后忽略的问题。

Codex 只有在要求时才会生成 subagents。会并行运行，然后把结果合并回一个答案。

把自己的 agents 定义成 `.codex/agents/` 里的 TOML 文件。每个文件包含 name、description、instructions，以及可选的 model 和 reasoning effort。
这样， security reviewer 可以用强模型和 high effort，而 explorer 可以是某个快速的 read-only agent。

Claude Code 也用 `.claude/agents/` 里的 subagents 和 agent teams 做同样的事情，让不同 agents 之间传递工作。

两个工具常见拆分方式：
- 一个 agent 负责探索；
- 一个 agent 负责实现；
- 一个 agent 负责根据 spec 验证结果。

loop 中尤其重要的原因：
- loop 会在不盯的时候运行。

因此，一个真正信任的 verifier 是能走开的唯一原因。

当然，<span style='color:red'>subagents 会消耗更多 tokens</span>，因为每个都要进行自己的 model 和 tool work。

所以，要花在“第二意见值得付费”的地方。

这也基本上是 Claude Code 的 `/goal` 在底层做的事：
> 由一个新的模型判断 loop 是否完成，而不是由完成工作的那个模型来判断。

maker 和 checker 的拆分，甚至被应用到了停止条件本身。

#### 组合

把这些东西粘在一起，一个单线程任务就会变成了小型控制面板。
- 每天早上，一个 automation 会在 repo 上运行。
- prompt 会调用 triage skill。这个 skill 会读取昨天的 CI failures、open issues、recent commits，然后把 findings 写进一个 markdown 文件，或者写进 Linear board。
- 对于每个值得处理的 finding，这个 thread 会打开一个隔离的 worktree，并派一个 sub-agent 去 draft fix，再派第二个 sub-agent 根据项目 skills 和现有 tests 去 review 这个 draft。
- connectors 让 loop 可以打开 PR，并更新 ticket。
- 任何 loop 无法处理的事情，都会落到我的 triage inbox。
- state file 是整套东西的脊柱。它记住了尝试过什么、什么通过了、还有什么仍然 open。所以第二天早上的运行，可以从今天停止的地方继续。

你只设计了一次，没有亲自 prompt 其中任何一个步骤。这就是 Steinberger 那个观点落地后的样子。

而且不管是在 Codex 里，还是在 Claude Code 里，这都是同一个 loop，因为这些 pieces 本质上是同样的 pieces。

Loop 改变工作，但不会把你从工作中删除

loop 会改变工作方式，但不会把你从工作中删除。
而且随着 loop 变得更好，有三个问题会变得更尖锐，而不是更容易。

第一，verification 仍然在你身上。

一个无人值守运行的 loop，也是在无人值守地犯错。

把 verifier sub-agent 和 maker 拆开的原因，是让 loop 说出的“done”有一点意义。即便如此，“done”也只是一个声明，而不是证明。
- 你的工作，是交付确认过能运行的代码。
- 如果放任不管，你的理解仍然会腐烂。

loop 越快地交付那些AI写的代码，真实存在的系统和实际理解的系统之间的差距就越大。

一个流畅的 loop 只会让这个差距增长得更快，除非真的去读产出的东西。

第三，最舒服的姿势，可能也是最危险的姿势。

当 loop 开始自己运行时，很容易停止拥有自己的判断，只是接受任何东西，这是危险状态。
- 带着判断力去设计 loop 时，设计 loop 是解药。
- 为了逃避思考而设计 loop 时，它就是加速剂。

同一个动作，会产生相反的结果。

这是工作方式演化的预览

不过，如果不亲自 review 代码，或者完全依赖自动化 loops 去修复问题，产品质量一定会下降。很可能会陷入一个持续下滑的螺旋，不断把自己挖进更深的坑里。

但不要忘记，直接 prompt agents 仍然有效。关键在于找到正确的平衡。
loops 也会因为使用者不同而产生完全不同的结果。
两个人可以构建完全一样的 loop，却得到截然相反的结果。
- 一个人在自己深刻理解的工作上跑得更快。
- 另一个人避免理解工作本身。

loop 不知道这两者之间的区别。但你知道。

这就是为什么 loop design 比 prompt engineering 更难，而不是更简单。

Cherny 的观点并不是说工作变简单了。而是杠杆点移动了。构建 loop。

但要像一个仍然打算做 engineer 的人那样去构建它，而不是像一个只会按下“go”按钮的人。


## DeepAgents


### 介绍

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


### 架构

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

### Web UI

方法
- （1）[LangSmith](https://smith.langchain.com/studio)：
  - 要注册langsmith账户才能使用云端web ui
  - [Smith](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024)
- （2）官方还有本地页面 Deep Agents UI，无需访问外网
  - [Deep Agents UI](https://github.com/langchain-ai/deep-agents-ui/tree/main)

#### LangSmith

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



#### Deep Agents UI

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



### 使用

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

#### create_deep_agent

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

#### DeepAgents Skills 使用说明


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


