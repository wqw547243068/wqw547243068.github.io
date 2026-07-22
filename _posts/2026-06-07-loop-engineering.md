---
layout: post
title:  Loop Engineering 循环工程
date:   2026-06-07 22:46:00
categories: 大模型
tags: gpt ChatGPT langchain go manus claude openclaw
excerpt: 硅谷新兴概念，新一代Agent框架 Loop Agent实现
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
- 公众号文章：[Loop Engineering 循环工程又是什么鬼？](https://mp.weixin.qq.com/s/lfq0Kz1Ok68j99hfnmz2AA)
- LE资源：
  - GitHub 资料总结：[loop-engineering](https://github.com/cobusgreyling/loop-engineering), 受 Addy Osmani and Boris Cherny / Anthropic 启发
  - 【2026-6-10】[Loop engineering: the 14-step roadmap from prompter to loop designer](https://x.com/0xCodez/status/2064374643729773029)

![](https://pbs.twimg.com/media/HKYhsj-XsAAd3fr?format=jpg&name=large)

<img width="1280" height="100%" alt="image" src="https://github.com/user-attachments/assets/fff2f5cc-e242-4c83-8a64-69e40683caf5" />


<img width="1000" height="100%" alt="image" src="https://github.com/user-attachments/assets/0b18fbe2-79e5-41a9-aa8d-11597697c1af" />

<img width="1000" height="100%" alt="image" src="https://github.com/user-attachments/assets/2f08c05b-9aad-4b76-9ca5-b854fca6170e" />

### 起源

loop 不是新词，真实血脉：
- `ReAct`（2022）→ `AutoGPT`（2023）→ `ralph`（2025）→ `/goal`（2026 春）→ 2026年6月的`编排 loop`。

详情
- 2022 `ReAct`
- 2023 `AutoGPT`
- 2025 `ralph` Geoffrey Huntley 用一行 bash 反复喂同一个 prompt，约 297 美元造了一门编程语言
- 2026 春 `/goal` Codex 和 Claude Code 都上了
- 2026年6月 `编排 loop` Loop Engineering

第五级新意在于四点：loop 成了工作单元、loop 开始监督别的 loop、调度取代人来启动、git 存状态且能崩溃恢复。 

"不就是 cron 换皮？" 一半对——调度层确实是 cron。但 cron 跑的是固定脚本，loop 跑的是一个会看当前状态、做决定、自检、再决定要不要继续的模型。
        
总结：
> loop = cron ＋ 循环体里的一个决策者。

最反直觉的是**反转**：loop 成了贵的那部分。
- 有人吐槽"唯一 agentic 的部分是月底那张 anthropic 账单"；
- Uber 四个月烧光全年 AI 预算后，把每人每工具每月的 Claude Code 和 Cursor 砍到 1500 美元。
- 于是每篇正经文章都收敛到三个硬停：最大迭代次数、无进展检测、美元预算上限。
- Gartner 也把 agentic AI 放在"期望膨胀的顶点"，只有约 17% 的组织真在部署。
- 而真正的资产不是 loop，是调用的 skill——做超过一次的事就存成 skill，下次就免费。
- 一个没有可复用 skill 的 loop，只是绕着陌生人转的 while-true。

Loop Engineering 正在取代“亲自给 agent 写 prompt”。
- 核心：不再直接 prompt agent，而是设计一个系统，去 prompt agent。

loop 是一种递归目标：定义一个目的，然后让 AI 不断迭代，直到任务完成。

大致由五个构建块组成，而 `Claude Code` 和 `Codex` 现在都已经具备了这五个能力。

这可能是未来与 coding agent 协作的方式。不过，现在仍然很早期。

必须非常注意 token 成本，因为不同使用模式下的消耗差异可能非常大，尤其取决于你是 token 富裕还是 token 紧张。仍然需要某种方式来确保质量不会下降，对“AI slop”的担忧也完全合理。

最近，openclaw作者`Peter Steinberger`说：
> 你不应该再去 prompting coding agent , 而是设计 loops，去 prompt agents。

类似地，Anthropic Claude Code 负责人`Boris Cherny`也说过：
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

### Graph Engineering

【2026-7-19】Loop 工程已死，Graph 工程永生

Loop Engineering 似乎已经不够性感了。现在 AI Agent 圈子里最火的新词，变成了 Graph Engineering。

连 OpenClaw 之父 Peter Steinberger 都开始调侃：“我们还在讨论 Loops，还是已经开始讨论 Graphs 了？”
	
 Loop Engineering（循环工程）核心是让 Agent 在循环中持续执行：规划、行动、观察、反思、再行动。它解决的是：如何让模型自主运行得更久，把一件事持续做下去。
	
*️⃣ 而 Graph Engineering（图工程）关注的不再只是单个 Agent 能循环多少轮，而是：如何用有向图组织多个 Agent、工具和任务节点，定义它们之间的依赖关系、信息流转路径和执行条件。
	
⏬️ 为什么 Graph Engineering 突然火了？
- 因为真实世界中的复杂任务，很少是一条直线，也不是简单地让模型反复尝试就能解决。它们通常包含：任务拆解、角色分工、条件判断、并行执行、结果聚合、失败重试，以及人工审批。当 Agent 从单点工具走向复杂工作流，真正决定系统能力上限的，已经不只是模型能不能“持续思考”，而是整个系统能否被合理地组织和调度。
- 所以，Loop 并没有真的消失。它更像是 Graph 中的一个基础结构。
	
⬛️ 从 Loop 到 Graph，代表 Agent 工程正在从：“让模型自己多跑几轮”走向：“设计一套可以稳定解决复杂问题的协作系统。”


### 架构

一个 loop 要五样东西和一个记住状态的地方。
- `Automations` 自动化：按计划自动触发、发现和分诊。
- `Worktrees` 工作树：让两个并行工作的 agents 不会互相干扰。
- `Skills`技能：把项目知识写下来，避免 agent 靠猜。
- `Plugins` 插件 和 `connectors` 连接器：把 agent 接入已经在用的工具。
- `Sub-agents`：子Agent，一个提想法，另一个检查。
- `memory`：可以是 markdown 文件，Linear board，或任何存在于单次 conversation 之外、能够保存“已完成事项”和“下一步事项”的地方。

一个循环所需的五个核心模块，Claude Code 和 Codex 都已具备：
- 定时自动化（Automations）：循环的心跳。按时间表自动触发，完成发现和分类工作，不需要人工介入。两个产品里的定时任务能力实现名称不同，但功能本质相同——让系统自己找到需要做的工作。
- 并行工作树（Worktrees）：让多个 Agent 并行工作时不互相干扰的隔离机制。没有 Worktrees，两个 Agent 会在同一个代码分支上互相覆盖对方的改动，循环就此失控。
- 技能知识沉淀（Skills）：把项目知识写下来，避免 Agent 每次都只能靠猜测。这是把「只有你知道」的上下文转化为「Agent 也知道」的结构化输入。
- 插件与连接器（Plugins and Connectors）：把 Agent 接入你已有的工具链——GitHub、Linear、Slack、数据库。循环需要读取现实，也需要把结果写回现实，连接器是这个双向通道。
- 制作者与验证者分离的子 Agent（Sub-agents）：一个Agent 负责提出方案，另一个负责检验——制造者与审查者天然分离。这是循环里内置的质量门禁，防止单个 Agent 的错误在无人知晓的情况下蔓延。

Codex vs Claude Code 对比表（中文版本）：

| 基础能力 | 循环中的工作 | Codex 应用 | Claude Code |
| --- | --- | --- | --- |
| **自动化（Automations）** | 按计划发现与分流任务 | 自动化标签页：选择项目、提示词、执行频率、环境；结果进入分流收件箱；用 `/goal` 执行直到完成 | 定时任务与 cron、`/loop`、`/goal`、钩子、GitHub Actions |
| **工作树（Worktrees）** | 隔离并行开发任务 | 每个线程内置独立工作树 | `git worktree`、`--worktree` 参数；在子代理上隔离工作树 |
| **技能（Skills）** | 将项目知识固化为可复用能力 | 代理技能（`SKILL.md`），通过 `$name` 调用或隐式触发 | 代理技能（`SKILL.md`） |
| **插件/连接器（Plugins / connectors）** | 连接外部工具 | 连接器（MCP）+ 用于分发的插件 | MCP 服务器 + 插件 |
| **子代理（Sub-agents）** | 创意构思与验证 | 子代理以 TOML 格式定义在 `.codex/agents/` 目录下 | 任务子代理定义在 `.claude/agents/` 目录下，支持代理团队协作 |
| **状态（State）** | 跟踪任务进度与完成情况 | Markdown 文件或通过连接器集成 Linear | Markdown（`AGENTS.md`、进度文件）或通过 MCP 集成 Linear |

英文版

| Primitive     | Job in the loop 循环任务      | Codex app          | Claude Code          |
|--------------------|---------------------|-----------------------------|---------------------------------------|
| **Automations** 自动化   | discovery + triage on a schedule     | Automations tab: pick project, prompt, cadence, environment; results land in a Triage inbox; `/goal` for run-until-done | Scheduled tasks and cron, `/loop`, `/goal`, hooks, GitHub Actions          |
| **Worktrees** 工作树     | isolate parallel features           | Built-in worktree per thread                                              | `git worktree`, `--worktree`, isolation: worktree on a subagent            |
| **Skills**   技能    | codify project knowledge            | Agent Skills (`SKILL.md`), invoked with `$name` or implicitly            | Agent Skills (`SKILL.md`)                                                  |
| **Plugins 插件 / connectors 链接器** | connect your tools              | Connectors (MCP) plus plugins for distribution                            | MCP servers plus plugins                                                   |
| **Sub-agents 子Agent **     | ideate and verify                    | Subagents defined as TOML in `.codex/agents/`                             | Task subagents in `.claude/agents/`, agent teams                            |
| **State 状态**          | track what’s done                    | Markdown or Linear via a connector                                        | Markdown (`AGENTS.md`, progress files) or Linear via MCP                   |


memory 是每个 long-running agent 都依赖的同一个技巧。

模型在每次运行之间会忘记一切，所以 memory 必须存在磁盘上，而不是只存在 context 里。

agent 会忘记，但 repo 不会。

现在两个产品都已经具备这五项能力。


<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;dark-mode&quot;:&quot;auto&quot;,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot;&gt;\n  &lt;diagram name=\&quot;AI意图识别商用方案\&quot; id=\&quot;osbHtP6Ki7KAK-vxM0vi\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;31489\&quot; dy=\&quot;21689\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;ueTJB6k9vFQzMmB7xgun-37\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=24;labelBackgroundColor=none;\&quot; value=\&quot;&amp;lt;span style=&amp;quot;font-family: Helvetica; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important; color: rgb(0, 0, 0);&amp;quot;&amp;gt;&amp;lt;font style=&amp;quot;color: rgb(51, 51, 255);&amp;quot;&amp;gt;Loop&amp;lt;/font&amp;gt;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt; &amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;font-family: Helvetica; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important; color: rgb(0, 0, 0);&amp;quot;&amp;gt;&amp;lt;font style=&amp;quot;color: rgb(255, 0, 0);&amp;quot;&amp;gt;Engineering&amp;lt;/font&amp;gt;&amp;lt;/span&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;210\&quot; x=\&quot;-30270\&quot; y=\&quot;-20910\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-11\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=19;fontStyle=1;fontColor=#808080;\&quot; value=\&quot;Loop 循环\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;175\&quot; x=\&quot;-30370\&quot; y=\&quot;-20650\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-3\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;6L5lKG1y3MccroiMXZLl-13\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#808080;\&quot; target=\&quot;wefgWDNr-mTIZ-ZurU0p-2\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-13\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=18;shadow=1;\&quot; value=\&quot;1 Find Work&amp;lt;div&amp;gt;任务准备&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;115\&quot; x=\&quot;-30375\&quot; y=\&quot;-20780\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6L5lKG1y3MccroiMXZLl-19\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;read failing tests\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;125\&quot; x=\&quot;-30375\&quot; y=\&quot;-20810\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-2\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=18;shadow=1;\&quot; value=\&quot;2 Plan&amp;lt;div&amp;gt;规划&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;110\&quot; x=\&quot;-30170\&quot; y=\&quot;-20780\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-4\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontStyle=1;fontSize=18;shadow=1;\&quot; value=\&quot;3 Act&amp;lt;div&amp;gt;执行&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;110\&quot; x=\&quot;-30170\&quot; y=\&quot;-20670\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-5\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;break into steps\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;125\&quot; x=\&quot;-30177.5\&quot; y=\&quot;-20810\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-6\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wefgWDNr-mTIZ-ZurU0p-2\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; target=\&quot;wefgWDNr-mTIZ-ZurU0p-4\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-30100\&quot; y=\&quot;-20700\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-30010\&quot; y=\&quot;-20700\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-7\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=18;shadow=1;\&quot; value=\&quot;4 Check&amp;lt;div&amp;gt;检查&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;110\&quot; x=\&quot;-30250\&quot; y=\&quot;-20570\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-8\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=18;shadow=1;\&quot; value=\&quot;Judge&amp;lt;div&amp;gt;判断&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;110\&quot; x=\&quot;-30090\&quot; y=\&quot;-20570\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-9\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;fontSize=18;shadow=1;\&quot; value=\&quot;5 Memory&amp;lt;div&amp;gt;记忆&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;110\&quot; x=\&quot;-30485\&quot; y=\&quot;-20570\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-10\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;fontSize=18;shadow=1;fontColor=#333333;\&quot; value=\&quot;Fresh Context&amp;lt;div&amp;gt;更新上下文&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;140\&quot; x=\&quot;-30580\&quot; y=\&quot;-20720\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-11\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;write the code\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;125\&quot; x=\&quot;-30255\&quot; y=\&quot;-20700\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-12\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wefgWDNr-mTIZ-ZurU0p-4\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; target=\&quot;wefgWDNr-mTIZ-ZurU0p-7\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-30030\&quot; y=\&quot;-20640\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-30030\&quot; y=\&quot;-20590\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-13\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wefgWDNr-mTIZ-ZurU0p-4\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; target=\&quot;wefgWDNr-mTIZ-ZurU0p-8\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-29983\&quot; y=\&quot;-20590\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-30100\&quot; y=\&quot;-20550\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-15\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;green or red, no opinion\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;187.5\&quot; x=\&quot;-30288.75\&quot; y=\&quot;-20510\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-16\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;other model, no self-grade\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;200\&quot; x=\&quot;-30090\&quot; y=\&quot;-20510\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-17\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wefgWDNr-mTIZ-ZurU0p-7\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#808080;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;wefgWDNr-mTIZ-ZurU0p-9\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-30200\&quot; y=\&quot;-20590\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-30280\&quot; y=\&quot;-20550\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-18\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wefgWDNr-mTIZ-ZurU0p-10\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#808080;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;6L5lKG1y3MccroiMXZLl-13\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-30280\&quot; y=\&quot;-20660\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-30360\&quot; y=\&quot;-20620\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-19\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=18;shadow=1;\&quot; value=\&quot;Breakes&amp;lt;div&amp;gt;终止&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;110\&quot; x=\&quot;-29950\&quot; y=\&quot;-20780\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-20\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wefgWDNr-mTIZ-ZurU0p-2\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#808080;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;wefgWDNr-mTIZ-ZurU0p-19\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-29940\&quot; y=\&quot;-20610\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-29860\&quot; y=\&quot;-20570\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-21\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;step limit&amp;lt;div&amp;gt;budget cap&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;blast radius&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;circuit breaker&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;heartbeat&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;110\&quot; width=\&quot;125\&quot; x=\&quot;-29957.5\&quot; y=\&quot;-20720\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-22\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;fit before you leave\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;200\&quot; x=\&quot;-29980\&quot; y=\&quot;-20810\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-23\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=17;fontStyle=1;fontColor=#808080;\&quot; value=\&quot;build a loop that runs itself, then put the brakes on\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;465\&quot; x=\&quot;-30370\&quot; y=\&quot;-20860\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-24\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#808080;\&quot; value=\&quot;wrap it all\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;75\&quot; x=\&quot;-30040\&quot; y=\&quot;-20780\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-25\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#007FFF;\&quot; value=\&quot;state + failure + only relevant files\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;242.5\&quot; x=\&quot;-30590\&quot; y=\&quot;-20660\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-26\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=1;fontColor=#808080;\&quot; value=\&quot;rebuilt every iteration\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;170\&quot; x=\&quot;-30590\&quot; y=\&quot;-20750\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wefgWDNr-mTIZ-ZurU0p-27\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=15;fontStyle=0;fontColor=#808080;\&quot; value=\&quot;【2026-6-23】wqw\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;150\&quot; x=\&quot;-30090\&quot; y=\&quot;-20472\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


#### Automations 心跳

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

可以给个条件，比如：
> all tests in test/auth pass and lint is clean


Codex 也有同样的东西，也叫 `/goal`, 会跨多轮继续工作，直到可验证的停止条件成立，并支持 pause、resume 和 clear。
同一个 primitive，两个工具都有。这基本上也是整篇文章反复出现的模式。

所以，这一部分负责把工作浮现出来。loop 的其余部分，则负责对这些工作采取行动。

#### Worktrees 并行操作而不混乱

只要同时运行不止一个 agent，文件就会开始冲突，这会变成失败点。

两个 agents 同时改同一个文件，和两个工程师同时提交同一段代码一样麻烦，而且事先还没沟通过。

`git worktree` 可以解决这个问题。独立的 working directory，位于自己的 branch 上，同时共享同一个 repo history。因此，一个 agent 的修改，字面意义上不可能碰到另一个 agent 的 checkout。
- `Codex` 直接内置了 worktree 支持，所以多个 threads 可以同时作用于同一个 repo，而不会互相撞车。
- `Claude Code` 也通过 `git worktree` 提供了同样的隔离能力。可以用 `--worktree flag` 在独立 checkout 中打开 session，也可以在 subagent 上设置 isolation: worktree，让每个 helper 都获得一个新的 checkout，并在结束后自动清理。

“人”的一面：
- worktrees 可以移除机械层面的冲突，但人仍然是天花板。
- 决定同时运行多少 agents 的，不是工具，而是 review bandwidth。


#### Skills 不用每次重复解释

skill 的作用是不用每次 session 都像金鱼一样重新解释同一个项目上下文。

两个工具都使用相同的格式：一个包含 SKILL.md 的文件夹，里面存放 instructions 和 metadata，也可以附带 scripts、references、assets。
- Codex 会用 `$` 或 `/skills` 调用时运行某个 skill；当 task 与 skill description 匹配时，也可能自动调用。这也是为什么一个紧凑、朴素的 description 比聪明但含糊的 description 更有用。
- Claude Code 的做法也一样。Skills 也是让 intent 不再一遍遍消耗成本的地方。

agent 每个 session 开始时都是冷启动。只要 intent 里有任何空洞，就会用一种自信的猜测把洞填上。

skill 就是把这种 intent 写在外部：项目约定、构建步骤、“不这么做是因为以前发生过某个事故”等等。只需要写一次，agent 每次运行时都会读取。
- 没有 skills，loop 每个周期都要从零重新推导你的整个项目。
- 有了 skills，就开始有一点复利效应。

有一点要区分清楚：
- `skill` 是 authoring format
- 而 `plugin` 是分发方式。

想跨 repo 共享 skill，或者把几个 skills 打包时，会封装成 plugin。
Codex 是这样，Claude Code 也是这样。

#### Plugins & Connectors 存换触及真实工具

只能看见 filesystem 的 loop 是很小的 loop。

Connectors 基于 MCP，可以让 agent 读取 issue tracker、查询数据库、调用 staging API、在 Slack 里发消息。

Codex 和 Claude Code 都支持 MCP，所以写的 connector，在另一个工具里也能直接运行。

plugins 还把 connectors 和 skills 打包在一起。这样队友只要安装 setup，而不用凭记忆重建整套东西。

这就是区别
- “agent 说：这里是修复方案”
- “loop 自己打开 PR、链接 Linear ticket，并在 CI 变绿后 ping 频道”

connectors 是 loop 在真实环境里行动的原因，而不只是“如果我能做，我会怎么做”。

#### Sub-agents 执行者与检查者隔离

loop 中，最有用的结构性设计，远远是把“执行人”和“检查人”隔离开。

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

#### 组合成Loop

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

第二，如果放任不管，你的理解仍然会腐烂。

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


### 问题

这种方式可行，但遇到**字符膨胀**问题，**Token消耗快**

#### 模型无法穷举

根本矛盾：框架想让 AI 做穷举，模型做不到。
- LLM 是概率模型，每步都选概率最高的路径走。
- 不像搜索引擎那样系统性地遍历所有合法走法。

给 LLM "自主探索"权利，大概率在同一个高概率区域打转。

| 路线 | 核心描述 | 补充说明 |
|------|----------|----------|
| **搜索引擎** | **无偏遍历所有可能性** | 每条路径都尝试，找到最优解 |
| **大模型loop** | **概率采样**，总是走最可能的路 | 走到黑，不会主动换方向 |


| 维度 | 穷举引擎 | LLM |
| :--- | :--- | :--- |
| 遍历方式 | 无偏，系统性 | 有偏，概率采样 |
| 低概率路径 | 一定会试 | 大概率跳过 |
| 已探索记录 | 外部精确记录 | 靠上下文回忆 |
| 上下文影响 | 无 | 越大越糊涂 |

LLM 不是搜索引擎，是随波逐流

| 序号 | 名称 | 说明 |
| ---- | ---- | ---- |
| 01 | 贪心决策 | 每一步都选概率最高的路径，不会系统性地遍历所有合法走法 |
| 02 | 上下文退化 | 1M 是硬上限，256K就开始退化，越长越糊涂，判断力崩塌 |
| 03 | 自我强化 | 重复操作积累在上下文中被误判为"正确模式"，继续执行 |


真实案例：
> 排查问题时，AI agent 执行同一条 grep 命令 15 次，每次结果完全相同。
> 不是在遍历可能性，是在**重复同一可能性**。

【2026-6-13】[小红书帖子](https://www.xiaohongshu.com/explore/6a2be00a000000002103ccdf)


#### 窗口退化

更致命的是上下文退化。
- 理论窗口 1M，实际到 256K 判断力就开始崩塌。
- 越长越糊涂，越容易**死循环**。
	
有人会说：那就加约束？—— 最大迭代次数、上下文压缩、外部状态管理、硬性预算。
	
但发现：
> `for 循环` + `状态机` + `数据库` + `超时机制` = `传统自动化程序`

| 序号 | 优化手段 | 效果/转变 |
| :--- | :--- | :--- |
| 1 | 加最大迭代次数限制 | 变成 for 循环 |
| 2 | 加上下文压缩 | 变成状态机 |
| 3 | 加外部状态管理 | 变成数据库驱动 |
| 4 | 加硬性预算 | 变成超时机制 |

用 LLM 替代了 if-else 判断，却丢掉处理模糊输入的优势。

约束到不烧钱的程度就是**传统程序**。

那为什么不直接写代码？<span style='color:red'>Loop 工程的归宿，是传统程序</span>。

【2026-6-13】[小红书帖子](https://www.xiaohongshu.com/explore/6a2be00a000000002103ccdf)

#### Loop Engineering = cron job?

Loop Engineering 需要**反馈循环**，就像开发团队要了解新功能、用户问题、工作流优化等。

LLM 可直接访问或生成数据，且需要明确目标和验证输出结果的反馈循环。

YC CEO `Garry Tan` 提醒:
- 不要把 Agent 变成“富士康工厂”式重复劳动机器，开发者应让 Agent 承担更多工作。

有开发者指出
- 让 Agent 做更多事，但要明确**边界**，要提供清晰上下文、可信工具、可审计操作记录和安全停止条件。


#### Loops 实现难点

调试跑 47 轮的状态机，比修好 prompt 难 10 倍，且大多数人连可靠的一次性 prompt 都写不好。
- 一开始设置容易，但之后有很多痛点，修复费劲。
- 有人后悔引入 Loop，迁移到其他方案耗费时间和资源，只能继续撑着。
- 还有人建议尽早迁移，时间越久情况越糟。


#### Token 消耗问题与应对

循环工程 token 消耗量高
- Boris Cherny 和 Peter Steinberger 背后公司提供近乎无限 token 支持
- 但社区很多人 token 预算有限。

Developers Digest 提醒团队要提前规划使用成本。

对于 token 消耗问题
- Peter 无解，有人指出 20 美元套餐不可能，“难道你的时间真不值钱吗？”
- Token 充裕公司可用 while 循环
- Token 紧张初创公司可用 for 循环实现目标。

做法
- Claude Code 对 token 消耗问题做了各种限制，如 Loops 支持最小 1 分钟间隔，最长运行 3 天，到期自动停止；
- Loops 绑定当前 Claude Code 会话，关闭终端或结束会话后停止；还提供禁用 Loop 的开关。


#### 长任务进化

Claude Code 的长时运行进化

Loops 工程重点是**让 Agent 长时间运行不跑偏**并能判断对错

Claude Code 是典型代表。Anthropic 应用 AI  团队工程师 Ash 表示公司探索方向更偏“**尽量完全自主**”，目标是把人类判断写入 Harness，而不是插入人工兜底。

过去一年，Claude Code 从只能连续运行约 20 分钟、易出错，进化到**几乎由自己编写、可连续运行数天**。

Anthropic 工程师 Andrew 指出让 Agent 连续运行数小时甚至数天，核心难点有上下文、规划和自我判断。

为解决问题，Anthropic 采用两条路径：
- 提升模型本身，把长时任务能力写入模型权重；
- 改造模型外部的 Harness。

早期长时运行 Agent 会拆解需求成持久化文件，在新上下文窗口中反复执行任务，缓解上下文丢失和任务漂移。

随着新模型能力增强，Anthropic 开始简化 Harness。
- Opus 4.6 擅长规划和工具选择，Sonnet 4.6 以低成本提供接近 Opus 的执行能力，常见组合是用 Opus 做规划、Sonnet 执行代码。
- 服务器端压缩和百万级上下文窗口使模型在单一长会话中保持更久连贯性。

Anthropic 内部实验的前沿 Harness 模式是**生成器—评估器—规划器结构**，借鉴生成对抗网络思想。

评估器有独立上下文窗口和系统提示词，用 Playwright 测试应用。Ash 指出<span style='color:red'>自我评估是陷阱</span>，把“构建者”和“批评者”拆开训练更可控。

在评估主观质量方面，Anthropic 尝试将“品味”写成可评分的量规，将前端应用质量拆成设计、原创性、工艺和功能性四类标准，并调整权重。为从页面生成走向完整应用，引入规划器角色，生成器和评估器协商“什么叫完成”，形成契约后评估器按契约验收。

对于 Ralph Loop 是否有价值，Andrew 表示在百万级上下文窗口和 Opus 4.6 连续会话能力下，选择取决于用例和评测。Ash 认为上下文腐烂是临时缺陷，某些支架组件未来可能移除。


## 经验

### 如何让 Loop 更可靠

不要让模型自评！看起来对，不算完成，要用真实的命令执行结果，

Loop 的价值不在于写代码，而是用外部检查纠正自己

Loop 是管道，skill 是长期资产

必须加的四个核心护栏（Safety Rails）


| 序号 | 英文标识 | 中文说明 | 核心作用 |
|------|----------|----------|----------|
| 1 | `max-turns` | 最多跑多少轮 | 限制 AI 代理的最大迭代轮次，防止无限循环 |
| 2 | `no-progress` | 连续几轮没变化就停 | 当连续多轮无有效进展时，自动终止流程，避免无效消耗 |
| 3 | `budget ceiling` | 花费到上限就停 | 设置成本/Token消耗上限，避免超出预算 |
| 4 | `sandbox` / `worktree` | 在隔离环境中跑 | 要求在沙箱、隔离分支或工作区中执行，避免直接影响生产环境 |

建议默认值（最佳实践）
- 小任务先设 10-20 轮 max-turns 作为初始限制
- 每轮执行都记录 diff（变更差异），便于回溯和审计
- 提前设置预算提醒，防止成本失控
- 任务停止后，必须输出当前状态（如变更记录、结果摘要），方便人工接管

注意
- 别再主分支、真实环境中裸跑！

### Loop 设计范式

【2026-7-2】20种loop设计范式 [X帖子](https://x.com/i/status/2072258045460226373)

loop类型 Anthropic 发布 Loop 设计指南  [帖子](http://xhslink.com/o/6GI7LB0GRcl)
根据触发方式、停止条件、使用的底层工具以及适合的任务类型，将循环分成了四大类：
- ⓵ 轮次循环（Turn-based loops）
- ⓶ 目标循环（Goal-based loop - /goal）
- ⓷ 时间循环（Time-based loop - /loop 和 /schedule）
- ⓸ 主动循环（Proactive loops）

Loop Engineering 20种设计模式，[帖子](http://xhslink.com/o/Ai0sCB0Rjun)

20种Loop Engineering设计模式

核心：AI干活不是“一锤子买卖”，而是 “做→看→评→改→再做” 的闭环。

这五类循环分别解决不同阶段的痛点：
- 一. 质量改进类——交活前反复“过筛子”
  - 好比写文章先自己读两遍，再找几个人从不同角度鉴读，分数不够就推翻重写，直到挑不出硬伤。
- 二. 记忆循环类——让AI“长记性”
  - 翻过的车存成案例，成功的招数存成模板，零散经验还压缩成通用规则。“吃一堑长一智”
- 三. 规划循环类——边干边调整路线。
  - 大目标拆成小步，走两步就回头看，跑偏了立马换道，所有条件挨个调通。
  - 核心: “计划赶不上变化，那就让计划跟着变化跑”。
- 四. 探索循环类——多条路同时试，选最优
  - 并行跑几个方案，沿着最有希望的分支深挖，差的直接剪掉，甚至让两个方案互相辩论暴露漏洞。
  - 本质是“别把鸡蛋放一个篮子里，还要比哪个篮子更结实”
- 五. 系统优化类——让AI自己改自己。
  - 自动测提示词的效果，自动调整工作流的步骤，哪儿慢哪儿贵就优化哪儿。这叫“自己给自己动手术，还能边动边愈合”。


# 结束



