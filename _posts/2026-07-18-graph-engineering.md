---
layout: post
title:  Graph Engineering 图工程
date:   2026-07-18 22:46:00
categories: 大模型
tags: gpt ChatGPT langchain go manus claude openclaw ak47
excerpt: 新兴概念，Graph Engineering
mathjax: true
permalink: /graph
---

* content
{:toc}

# Graph Engineering 


各种engineering对比

![](https://pic2.zhimg.com/v2-6217dfaa66df6a9e247c562c6cbc98d7_1440w.jpg)

| 维度 | Agent harness（代理框架） | [Loop engineering](loop)（循环工程） | Graph engineering（图工程） |
| ---- | ---- | ---- | ---- |
| 主要关注点 | 运行能力 | 迭代进度与反馈 | 显式控制流 |
| 核心对象 | 模型包装器 / 运行时 | 有边界的可重复循环 | 有向步骤图 |
| 典型构建模块 | 工具、内存、沙箱、中间件、权限、追踪 | 触发器、目标、动作、证据、反馈、停止规则 | 节点、边、共享状态、分支、汇合、中断、循环 |
| 解决的痛点 | "模型无法安全地完成工作" | "智能体过早停止或产出薄弱" | "工作流难以推理和控制" |
| 最佳适用场景 | 通用代理平台或特定任务运行时 | 通过验证持续改进的开放式工作 | 含多个决策点的复杂多步流程 |
| 主要风险 | 运行时臃肿、黑盒不透明 | 无限重试、Token 耗尽、奖励投机 | 图表过度设计、路径脆弱易断 |

分析
- Prompt Engineering 解决“怎么问”
- Context Engineering 解决“模型知道什么”
- Harness Engineering 解决“模型如何工作”
- Loop Engineering 解决“如何持续推进”
- 而 Graph Engineering 解决的是：多个 Agent 如何协同

<img src="https://pic3.zhimg.com/v2-c94055c641dce1c113e1d9572b6702d4_1440w.jpg" height="100%" width="600" />


资料
- [小红书图解](https://www.xiaohongshu.com/explore/6a5e47cb00000000110042f1)
- [Graph Engineering：从 0 到 1 小白完整教程](https://x.com/AdrianPunk115/status/2081268706483814605)
- 图解 Graph Engineering [知乎](https://zhuanlan.zhihu.com/p/2065181073781298761)，[飞书](https://my.feishu.cn/wiki/R7nMwo9STi9Z5kkuIOjcUGRxnRb?from=from_copylink) 

Andrej Karpathy 12 页的 PDF 文档，多智能体系统中的“图结构工程”技术。[X推文](https://x.com/Serantych/status/2081037322867363889)

完整说明：
- 步骤 1: 构建循环 —— 生成、批评、修正。48 小时内完成 630 行代码，进行 700 次实验。
- 步骤 2: 并行处理：各个代理程序在独立的工作线程中运行，共享同一个仓库，但路径不同，不存在冲突。
- 步骤 3: 添加知识图谱：提取实体，解决别名问题，构建类型化的边，通过子图进行查询。
- 步骤 4 → 对评估者进行验证：这一步是通过图表来比对各种声明是否一致，而不是通过感官判断。
- 步骤 5 → 将共享内存中的图表数据加载到内存中。工作者们写入该内存。评估者进行核实检查。这些循环结构会持续运行一整夜。
- 步骤 6 → 代理忘记了。而图表并没有忘记。因此，每次会话时都不需要重新构建上下文了。

Karpathy 使用了 1 个代理来处理 1 个方向的问题。Anthropic 图结构可以运行 1000 次，并且支持共享内存——同样的模型，只是架构有所不同。



## 介绍


如何让 AI 按步骤干活？理解→执行→检查→修正，这叫 循环工程，称为 Loop Engineering。

![](https://pic4.zhimg.com/v2-4f1196b613749d00dcd488e2f93cdfcb_1440w.jpg)

但最近AI 圈有人说：Loop 死了

不是Loop 没用了，而是当任务复杂到一定程度，一个 Loop 撑不住了。
需要一群 Loop 协作。这就是 Graph Engineering。
理解：

不再让一个 AI 循环干活，而是设计一张任务流程图，让多个 AI 各管一段，按顺序交接。

![](https://pic3.zhimg.com/v2-d5a455806e12c59255bcb13dcc12fdda_1440w.jpg)



## 一、Graph Engineering 诞生


2026 年 7 月 18 日凌晨，Peter Steinberger发了一条推，被浏览了 300万次

![](https://pica.zhimg.com/v2-0ade2a05d585a28198e6b60fc6c0c484_1440w.jpg)

- Are we still talking loops or did we shift to graphs yet?
- 还在讨论循环结构吗？还是已经转向图工程？

4 个半小时后，AI 评测领域的大佬 Hamel Husain 跟了一篇长文，标题只有两句话：

![](https://pic2.zhimg.com/v2-415fd71ef92337a69ee1f6be9f07b811_1440w.jpg)

内容
- Loop Engineering Is Dead. Enter Graph Engineering循环工程已经消亡了。接下来将是图工程的时代。
- Loop Engineering 从命名到死亡，只隔了 41 天。（短命鬼）

AI 圈又在造词？这次不太一样。

当AI 任务从"写一篇文章"变成"做一个产品"，一个 Loop 确实不够用。

分析
- Loop Engineering 解决的是：一个 AI 怎么持续干活。
- Graph Engineering 解决的是：一群 AI 怎么协作干活。

【2026-7-19】Loop 工程已死，Graph 工程永生

 - Loop Engineering（循环工程）核心是让 Agent 在循环中持续执行：规划、行动、观察、反思、再行动。它解决的是：如何让模型自主运行得更久，把一件事持续做下去。
- 而 Graph Engineering（图工程）关注的不再只是单个 Agent 能循环多少轮，而是：如何用有向图组织多个 Agent、工具和任务节点，定义它们之间的依赖关系、信息流转路径和执行条件。
	
⏬️ 为什么 Graph Engineering 突然火了？
- 因为真实世界中的复杂任务，很少是一条直线，也不是简单地让模型反复尝试就能解决。它们通常包含：任务拆解、角色分工、条件判断、并行执行、结果聚合、失败重试，以及人工审批。当 Agent 从单点工具走向复杂工作流，真正决定系统能力上限的，已经不只是模型能不能“持续思考”，而是整个系统能否被合理地组织和调度。
- 所以，Loop 并没有真的消失。它更像是 Graph 中的一个基础结构。

⬛️ 从 Loop 到 Graph，代表 Agent 工程正在从：“让模型自己多跑几轮”走向：“设计一套可以稳定解决复杂问题的协作系统。”

更多介绍
- [图解 Graph Engineering](https://zhuanlan.zhihu.com/p/2065181073781298761), [公众号](https://mp.weixin.qq.com/s?__biz=MjM5ODY2OTQyNg==&tempkey=MTM4NF9ydkVIcklIWFplcWptM0psa29OelY0b01PRzJOSXF5X3FoWElaQTZUY1pUSFpvLTdDRjhwMG5LcUlyYmsxa2d1WWhHUk5GMmZiWGJPdUpFNFJHc3ZHLTRIMlVXYUpmbm1IMFZRbFJ6WXV4ZE9CNXdNTTBFRm9JbXFwZ29NQ1phUGpKQy11WVZ2c2IyQkFkTEtfcjJXenVicmxNbWZrZzhfRlZCRVhnfn4%3D&chksm=bec3d24189b45b57a9838fd6011c0682769fc8d42ba5a2c1a83f8e7b58ca7f0648fc9326b3b2&token=1314339977&lang=zh_CN#rd)
- [Andrej Kaparthy 实践指南](https://drive.google.com/file/d/1-GOg0kxcp8tx1BMUECMj2yJq6JYGmfhb/view?pli=1)，11页

## 二、Graph Engineering 是什么

Graph 是"图"，流程图的图。Engineering 是工程化。

Graph Engineering 把复杂任务拆成多个节点，用流程图方式定义关系。

类比后厨场景。
- Loop 是厨师自己包揽一切——切菜、炒菜、调味、装盘，做完一步回头检查一下，不行就重来。
- Graph 是整个后厨团队——有切配、有炒锅、有打荷、有出菜，每个岗位只干一件事，按流程传菜。

![](https://pic2.zhimg.com/v2-cecb5ac657d22dbdc3a82f46fa630ad5_1440w.jpg)

一张 Graph 就三样东西：
- `节点`（Nodes）——干活单元。可以是 AI、工具调用，甚至点头的人。
- `边`（Edges）——决定下一步跑什么。可以是顺序、并行，也可以按上一步的结果走不同分支。
- `状态`（State）——节点之间流动的信息。每个节点都读它，也都写它。

<img src="https://pica.zhimg.com/v2-11f61c99f14efb371cf2fb442986b788_1440w.jpg" height="100%" width="600" />

<img src="https://pic3.zhimg.com/v2-b1850b348a1791162cb4a59ac98d7e16_1440w.jpg" height="100%" width="600" />




听起来抽象？看个具体例子。

写一篇深度文章，Graph 思路：
- 第一个节点：研究——搜索资料、整理要点
- 第二个节点：写作——基于研究结果写正文
- 第三个节点：审阅——检查质量，不合格就退回

三个节点，两条边，一个共享状态。这就是最小的 Graph。

Loop 是一个人转圈，Graph 是一群人接力。

## 三、Loop 为什么不够用

不是所有任务都需要 Graph。

如果只是让 AI 翻译一句话、写 10 个标题、解释一个概念——一个 Loop 足够了。

但当任务出现以下情况，Loop 就开始撑不住了。
- 需要不同**角色**：做一期播客内容。研究资料、写脚本、审稿、做封面——这些角色用的提示词不同，关注重点不同，甚至该用不同模型。全塞进一个 Loop，AI 会角色混乱。一会儿在研究，一会儿在写稿，一会儿又回头检查，越跑越糊涂。
- 需要**条件分支**：如写代码，测试通过就进入下一步，测试失败就要回去修。有时候修一处会影响别的地方，需要重新评估。这种"如果 A 就走 B，如果 C 就走 D"的逻辑，在 Loop 里写起来特别拧巴。但在 Graph 里，它就是一条条件边的事。
- 需要**并行**：如做一份行业调研。同时搜索 5 个方向的信息，等全部回来再汇总。Loop 是串行的——一件一件来。Graph 可以让 5 个节点同时跑，跑完汇总。

判断标准：
> 一个 Loop 跑到第三轮还搞不定，就该考虑 Graph 了。

<img src="https://pic3.zhimg.com/v2-73f14d8baad19cdcd46a19de1227756a_1440w.jpg" height="100%" width="600" />



## 四、Loop 和 Graph 关系

Loop 其实是 Graph 特例。

什么意思？循环：
- AI 思考 → 执行 → 检查 → 不合格就再来
- 用图来表示为一个节点，加一条指回自己的边。

```
[AI 干活]
  ↑    ↓
  └────┘  （自环边）
```
  
所以， Loop 没有死，只是变成了 Graph 里的基础结构。

Graph Engineering 不是取代 Loop，而是把Loop们 连起来，协调运作

理解：
- Loop 解决了"一个 AI 怎么干活"
- Graph 解决了"一群 AI 怎么协作"
- 从"个人贡献者"升级到"团队管理"。

![](https://pica.zhimg.com/v2-0dd0a33f25a5a44cbc22e4a0b3c89260_1440w.jpg)

单兵作战的能力没消失，但还需要学会怎么排兵布阵。

## 五、真正变的是图节点（不是DAG）

疑问：
- 流程图、状态机、任务调度——这些不是计算机科学里几十年的老东西吗？
- 没错。Airflow 画了十年的任务图。Anthropic 2024 年那篇《Building Effective Agents》也画过所有模式。

为什么现在又重新炒？

因为真正变的不是图结构，是图节点。
- 过去的图，节点是机器。 写好规则，就这么跑。输入什么，输出什么，完全确定。
- 现在的图，节点是 AI。 给定任务，理解、判断、执行。理解对了就好，理解偏了，后面节点全跟着偏。

但AI带来三个全新的问题：
- 状态会腐烂——AI 写错一笔，下游全跟着错
- 路由会漂移——同一个任务，跑两次走两条路
- 验证会失灵——AI 审 AI，互相点头

这才是 Graph Engineering 真正关心的，不是怎么画图，而是怎么管住一群会思考的节点。

Graph不是DAG：有向，但不一定无环

<img src="https://pic1.zhimg.com/v2-9cef653f2388704ff3b7c2772a3cac56_1440w.jpg" height="100%" width="600" />



## 六、Graph Engineering 核心模块


多Agent如何在一张图里协作？

<img src="https://pic4.zhimg.com/v2-bf3abc023c6eba179eb4873ac5da1af9_1440w.jpg" height="100%" width="600" />


Graph骨架：FSM

<img src="https://pica.zhimg.com/v2-e2127d9eb9688c283af688edc376e608_1440w.jpg" height="100%" width="600" />


### 核心模块

![](https://pic2.zhimg.com/v2-1c3fc7c19f1ae7e6c38169acfd081c4f_1440w.jpg)

#### 节点模块：每个节点凭什么存在

最常见的错误是把简单任务拆成一堆节点。

"总结一份 PDF" 变五个节点：抓取、切块、总结、审阅、排版。结果除了浪费 token，什么协同都没产生。

一个节点配得上位置，前提是代表真正的专长：
- 换了模型（用 GPT-5 做研究，用 Claude 做审阅）
- 换了工具集（一个能搜网页，一个能跑代码）
- 确实是另一个角色（一个只读的审阅者）
- 检验标准：两个节点能合并成一个却什么也不损失，那它们本来就不该是两个。

#### 状态模块：信息怎么在节点间流动

Loop 里失败叫"上下文腐烂"。到了 Graph，同一种病搬进了共享状态。

第二个节点写错，会成为第五个节点的输入。错误沿着边向下游传染，而且很难发现是从哪一步开始错的。

工程做法：
- 给状态定明确的数据结构——别让字符串混进该是列表的地方
- 规定每个节点只能写自己负责的字段
- 节点之间打检查点——重放一次运行，看清在哪步走歪的
- 没有状态管理的 Graph，就像没有账本的团队。每个人都在改数据，没人知道改了什么。

#### 路由模块：下一步走哪条路

每一条边都是一个决定。问题是这个决定由谁来做？

让 AI 决定路线，灵活和不稳定会一起来。同一份输入跑两次走不同的路，出了问题根本复现不了。

Google 给 ADK 2.0 定的规则最干净：
- 条件清晰的地方用代码路由（if/else）
- 真正需要判断的地方，才让 AI 决定
- 原则：能写死的地方就写死，AI 只花在需要解读的地方。

#### 审阅模块：怎么防止 AI 互相点头

多个同源 AI，读着同一份有问题的上下文，会非常愉快地互相同意——AI 也偏爱自己的输出。结果就是结构漂亮，答案是错的。

怎么破：
- 审阅节点换一个不同的模型——别让一个家族的 AI 互相包庇
- 给它全新的上下文——而不是整段对话历史，让它真的独立思考
- 把结论锚定到外部证据——比如真的跑通的测试、真的编译过的代码

Cognition 跑了一年之后得出的结论：
- 多个 AI 可以读、可以发表意见，但任何时候只有一个 AI 被允许动手改东西。
- 读可以并行，因为一个糟糕的意见在没人照做之前不花一分钱。

写才是出事的地方，所以把它收在一处。

## 七、Graph 模板

<img src="https://picx.zhimg.com/v2-4bcc771b5b576cbaf5241a4f04736077_1440w.jpg" height="100%" width="600" />


### 写文章 Graph

适合：深度长文、公众号、Newsletter

任务：写一篇【主题】的深度文章

节点 1：研究
- 搜索相关资料
- 整理 5 个关键要点
- 输出：研究摘要

节点 2：写作
- 基于研究摘要写正文
- 输出：文章初稿

节点 3：审阅
- 检查：开头有没有具体例子
- 检查：有没有空话和长段落
- 检查：读者看完知不知道下一步做什么
- 不合格则退回节点 2，最多退 2 次
- 合格则输出最终版

路由规则：
- 研究完成 → 写作
- 写作完成 → 审阅
- 审阅不通过 → 写作（标记问题）
- 审阅通过 → 结束


### 写代码 Graph

适合：功能开发、Bug 修复

任务：完成【功能描述】

节点 1：理解
- 阅读现有项目结构
- 找到相关文件
- 输出：修改方案

节点 2：执行
- 按方案修改代码
- 输出：修改后的代码

节点 3：测试
- 运行测试或检查功能
- 如果失败，读取报错原因
- 输出：测试结果

节点 4：修复（条件节点）
- 根据报错修复
- 回到节点 3 重新测试
- 最多重试 3 次

路由规则：
- 理解 → 执行 → 测试
- 测试通过 → 结束
- 测试失败 → 修复 → 测试
- 重试 3 次仍失败 → 输出卡住原因





# 结束
