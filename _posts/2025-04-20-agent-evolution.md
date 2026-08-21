---
layout: post
title:  Agent 自我进化
date:   2025-04-20 11:30:00
categories: 大模型
tags: Agent 自学习 进化 自动化 训练 openclaw 小米 罗福莉 hermes 斯坦福 递归自进化 谷歌 jeff
excerpt: LLM/Agent 如何实现自我进化？
mathjax: true
permalink: /agent_evolution
---

* content
{:toc}


# Agent 自我进化

一个完全自主、越用越强的 Agent，有可能实现吗？

## 观点

【2026-3-27】小米 MiMo 大模型负责人罗福莉：大模型的自进化，对科学研究带来的指数级加速

【2026-7-27】腾讯技术工程文章：[Agent开始“自我进化”：会出题、会反思，还会自己长出新技能](https://mp.weixin.qq.com/s/fsVJiorPBN4ylGjUYBcIPw)

【2026-8-13】[Self-Evolving Agent: A Closed-Loop Post-Training Flywheel for Continually Learning LLM Agents](https://alloomi.ai/reports/sea.pdf)

Agent 在真实任务里产生了大量轨迹和反馈，最后到底该学什么？

现在很多 Agent 已经能跑很长的任务，也有 memory、skills、harness 去保存经验。但很多时候，这些经验依然停留在模型外面：存进向量库、写进 skill、塞回 context。

Agent 能「记住过去」，和真正「从过去学会东西」，中间其实还有很长一段距离。

@AlloomiAI 做的 Self-Evolving Agent 把真实工作里的上下文、专家修改、任务结果和反馈组织成完整轨迹，再经过质量筛选、专家锚定和后训练，让这些经验逐渐进入模型能力。

整个闭环大概是：工作轨迹 → 筛选经验 → 专家锚定 → 后训练 → 评测准入 → 出问题可以回滚。

在 CL-Bench 上，同一个 backbone 经过这套方法后，成绩从 24.5% 提升到了 47.6%。

背后的方向：
- 未来 Agent 的自进化，需要解决怎么获得真正有价值的经验，以及怎么安全地把这些经验变成下一次任务可以复用的能力。

Alloomi 还把其中的上下文运行时 OpenContext 开源了，可以直接接进自己的 Agent。

比起单次任务做得更强，我现在更关注它们能不能在长期使用中持续变得更熟练。

【2026-8-20】[Jeff Dean离职后首次公开访谈火力有点猛](https://mp.weixin.qq.com/s/XpeRZ6A_FBL7rS3JcyJbAg) 斯坦福 2026 Frontier&Pioneer Symposium 上，`Jeff Dean`一口气聊开了不少过去很少公开展开的话题 [YouTube](https://www.youtube.com/watch?v=0kC3xOZChdA&t=2s)
- 关于为啥离开谷歌：小团队可以极致聚焦
  - 非常专注的小公司，所有人都围绕同一个使命工作，这种状态本身就很有吸引力。非常专注地去做科学和工程自动化。
- TensorFlow 当年有两个很明确的失误
  - 第一，最开始没有加入 Eager Execution 模式。后来这种方式在`PyTorch`和`JAX`框架流行,TensorFlow 才加进来
  - 第二，contrib子目录允许很多外部开发者贡献各种辅助库和不同的实现方式。给社区带来困惑，因为变成同一件事情可能有十种不同的做法，到底该用哪一种，取决于用了contrib里的哪个子目录、哪个库。TensorFlow核心保持更简洁，把这些东西作为建立在核心之上的外部库。
- Gemini为啥不行？
  - Gemini 其实是Google内部几个更早研究项目最终汇合的结果——包括原来 DeepMind、Google Brain，以及Google Research其他团队的一些工作。
  - 把Gemini的Coding能力真正做到惊艳，重视得稍微晚了一点
- 自己的科研秘诀：
  - 未来科学实验的一轮迭代，可能从一天、一周压缩到一分钟、一小时
  - 在找重大研究方向时，与其精读1篇论文，不如先扫10篇，甚至100篇摘要
  - 利用`第一性原理`和一些工程经验, 在脑子里快速判断不同解决方案大概是什么量级。
- 新公司 [Discovery Loop](https://www.discoveryloop.com/) 接下来准备押注什么
  - 把科学发现变成自动迭代的Loop. [Discovery Loop](https://www.discoveryloop.com/) 目标：让模型拥有“20个博士”的科研能力
  - 递归自我改进，覆盖模型参数、训练数据、Eval，甚至模型架构本身。
  - 联合创始人`Quoc Le`很早就在做`Neural Architecture Search`：让模型自动生成模型架构，再根据学习速度、训练成本等指标不断获得反馈，逐渐找到更好的设计。还做了`Evolved Transformer`，通过进化算法重新组合Transformer组件，最终找到的架构效率比标准Transformer高了大约30%。
  - 递归自我改进真正要解决的问题是怎样让构建模型所需要的整套东西，都能够通过自动化方式持续变得更好。

## 静态问题

大模型老大难问题：
- **静态**知识：训练完成那一刻起，模型对世界的认知就被冻结了；
- 上下文有限：再长的上下文窗口也总有边界，多轮交互终究"断片"；
- 重复犯错：今天教会它的事，明天还会再犯一遍；
- 训练贵：每次想让模型变强一点，要么 SFT 要么 RL，都得重新跑一遍。

而 Agent 与真实世界互动时问题：
- 世界是**动态**：新知识、新事件、新梗层出不穷。一个知识停留在 2023 年的 AI，无法理解 2024 年的最新动态。
- 任务是开放：真实世界的任务千变万化，没有固定的「题库」。AI 需要具备处理未知问题的能力。
- 工具是变化：新的软件、API 和网站不断涌现。AI 需要学会使用新工具，甚至创造新工具。
- 用户是个性：每个人都有自己的偏好和习惯。AI 需要通过与用户的互动，不断适应和学习，提供个性化服务。

「静态」的 AI 在这样动态、开放的环境中，就像一个拿着旧地图的航海家，注定会迷航。

因此，AI 范式正在经历一场至关重要的转变：从追求模型的「规模」（Scale）转向追求智能体的「适应性」（Adaptivity）。

发展路径：
- 从`基础 LLM`，到能执行任务的`基础智能体`（Foundation Agents），再到能够持续学习和适应的`自进化智能体`（Self-Evolving Agents），并最终指向理论上的`人工超级智能`（Artificial Super Intelligence, ASI）。
- ![](https://pic2.zhimg.com/v2-05370ee6d90f1cc00d8b4a8c59e8ca2b_1440w.jpg)

自进化 Agent 想要的正是绕开这些限制：让经验本身成为模型能力的延伸或更新通道

大模型时代被重新点燃，因为：
- LLM 本身具备总结归纳的能力（自己能给自己写笔记了）；
- Agent 形态的产品越来越多，长程交互场景终于有了真实需求；
- 高质量人工标注数据越来越贵，社区开始探索"少人工 / 无人工"路线。


## 什么是自进化


### 定义

Agent 自进化（Self-Evolving Agent）：
- Agent 在运行期或部署后，基于交互轨迹、环境反馈或任务结果，对自身的可持久组件进行更新，从而提升未来任务的表现。

要点
- 第一 **可持久组件**——更新的对象必须能**跨任务留存**，单次会话里的临时纠错不算。
- 第二 **提升未来表现**——改了之后下次要真的更好，"改了"本身不算进化。

### 分类

【2026-8-2】[什么是 Self-evolving / self-improving / RSI ？一篇文章搞懂自进化](https://mp.weixin.qq.com/s/iWh5x-SPxa-MhMq4OLLqpw)
- 周星星 [自进化（Self-evolving／RSI），一篇就够了](https://zhuanlan.zhihu.com/p/2065227313973825752)

热词: self-evolving、self-improving、recursive self-improvement（RSI）


自进化分三个方向

自我进化的优化对象是什么，就决定了属于哪个方向
- 改产出物（代码/论文/算法…）是 Artifacts
- 改脚手架（prompt/memory/tool/skill/hook…）是 Harness
- 改模型参数本身是 Model。

三者都算 RSI：
- ![](https://pic2.zhimg.com/v2-f097a603306561d44f811a9f21388d47_1440w.jpg)

详情
- （1）Artifacts 层自进化：用强大的 LLM 反复”发现问题 → 生成产出 → 评估结果”，来优化具体的复杂问题产物（代码、论文、算法）。
  - 比如任何一款 AI coding 工具，给定目标，就会写代码、自己编译、自己测试，有 bug 自己修，最终输出能达到要求的代码。
  - 产出物一版比一版强，这就是 Artifacts 层面的自我进化，改的是产出物本身，不涉及模型权重，也不涉及 agent 自身的脚手架逻辑。
  - 案例：
    - Karpathy 的 Autoresearch：整夜自动改 train.py 迭代超参
    - Google DeepMind 的 AlphaEvolve：进化算法筛选代码，成果反哺自身训练
- （2）Harness 层自进化：不动模型权重，改部署后 Agent 本身的”脚手架”：prompt、memory、tool、skill、多 Agent 路由等等等等都是这一类。
  - 翁荔博客 《Harness Engineering for Self-Improvement》 判断：RSI 近期不太可能从模型直接改写自己的权重开始，更现实的路径是先在 Harness 层爆发 
  - 跟 Artifacts 层不一样：Artifacts 优化某次任务的产出物；Harness 优化 agent 下次执行任何任务时都会用到的那套”脚手架”，改一次，后面所有任务都受益。最直观的例子是 Agent 跑任务踩了坑，把错误总结成一条新 skill 或一段新 memory 存下来，下次碰到同类任务直接调用，不用再犯一次。agent 自己把自己的脚手架越改越顺手，这就是 Harness 层面的自我进化。
  - 案例
    - Hermes：踩坑自动写成 SKILL.md —— 一个任务用到5次以上工具调用，就自动写成 skill.md; Curator 后台维护机制，追踪每个技能被用了多少次、有没有被修改过，长期没用的技能会经历”活跃 → 陈旧 → 归档”的状态流转，还会定期叫一个小模型做审查、合并近似重复的技能，不是写完就无限堆量放着不管。
    - MiniMax M2.7：自动跑评测迭代 scaffold，性能提升 30%; agent harness 自己收集反馈、给内部任务建评测集，再据此持续迭代自己的架构、技能/MCP 实现和记忆机制
    - 陈天桥 Apodex-1.0：150 子 agent 协同检索，冲突/存疑时派发验证子团队
    - Sakana 的 RHI：LLM 评估器打分驱动 harness 自我重写
    - Ai2 的 Rethinking the Evaluation of Harness Evolution for Agents：预算对等后，harness 进化未必赢过简单 test-time scaling
    - Weco AI 的 AIDE²：外层 agent 改内层 agent 代码，实测跑到 RSI Level 1
- （3）模型层自进化：广义的角度，不需要人工标注答案、模型自己给自己当老师的训练都能算：自己筛出高置信度/前后一致的答案反过来当训练数据（self-training、TTRL）、把内部信号转成可验证奖励再用 RL 训练（DeepSeek-R1）、两个版本的自己互相对练（自对弈，例如 SPIN、Absolute Zero）、推理时当场再学一遍（测试时训练）。不靠人喂标注答案，模型自己给自己当老师，这就是 Model 层面的自我进化。狭义的层面，是模型能自己产出下一代的训练优化方向，一代代往上迭代——模型自己训练完 → 自己测试 → 自己找问题（架构瓶颈在哪、工程实现哪里有坑、训练数据有什么问题）→ 自己提出优化方向/实验（例如自己改训练代码，自己补充训练数据）→ 再训练，整个研发循环都由 AI 自己跑。
  - 案例：把”改 harness”和”改权重”拧到同一个循环里联合优化的系统（SIA、Continual Harness）、不直接做 RSI、但研究”模型内部思考链、可解释性等
    -  SIA：Feedback-Agent 决定该改 harness 还是改权重
    -  Continual Harness：内层高频改 harness，外层用 PRM 蒸馏更新权重
    -  可解释性代表工作：搞懂训练怎么塑造推理


### 易混淆概念

易混概念：
- 不等于权重在线学习。 工程上常说的自进化，大多不是在线更新模型权重，而是在冻结的基座模型之外更新记忆、工具、提示词、工作流或 Agent 代码。这正是落地的原因，和"AI 递归自我改进奔向超级智能"那种叙事之间的真实距离。
- 不等于反思（reflection）。 单次任务内的 self-critique 是临时，任务结束就丢。自进化要求改进跨任务持久化。这是最硬的分界线：判断系统算不算自进化，先问这次学到的东西下次还在不在。
- 不等于 RAG。 准确的切分是：RAG 是检索机制，负责读；自进化是更新机制，负责写。一个自进化系统完全可以用 RAG 去读自己沉淀的经验库，但只读静态知识库、从不基于运行经验写回的系统，和自进化无关。

## 自进化系统


2025 年，系统综述《[A Survey of Self-Evolving Agents]()》用三个维度组织这个领域：
- 进化什么（模型、记忆、工具、架构）
- 什么时候进化（任务内 intra-test-time、任务间 inter-test-time）
- 怎么进化（标量奖励、文本反馈、单/多智能体）。

注意定义并不限于"上线之后"，任务执行过程中的演化也算。但工程上最有价值、也最常被讨论的是任务间的持久演化——系统用得越久越好用。

人类学习逻辑：
> 做事留记录（运行轨迹）→复盘好坏（反馈评分）→总结经验（提炼）→记住经验（持久更新）→下次活用（任务复用）→检验进步（效果评估）→继续优化。

闭环流转顺序：
> `运行轨迹` → `反馈/评分` → `经验提炼` → `持久更新` → `后续任务复用` → `效果评估`，循环往复持续迭代。

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;dark-mode&quot;:&quot;auto&quot;,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot;&gt;\n  &lt;diagram name=\&quot;Qwen四代演进\&quot; id=\&quot;eMoWEZYMmT8u7dPpwd27\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1709\&quot; dy=\&quot;1262\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-19\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;strokeWidth=4;fillColor=#FFE6CC;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;140\&quot; width=\&quot;670\&quot; x=\&quot;140\&quot; y=\&quot;930\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-15\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;strokeWidth=4;fillColor=#FFFFFF;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;280\&quot; width=\&quot;670\&quot; x=\&quot;150\&quot; y=\&quot;1110\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;vIzsuBNDGU4je8Ju_WXj-48\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=29;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#333333;fontStyle=1\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;Agent自进化链路&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;250\&quot; x=\&quot;370\&quot; y=\&quot;740\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;vIzsuBNDGU4je8Ju_WXj-56\&quot; parent=\&quot;1\&quot; style=\&quot;text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;rounded=0;fontSize=16;fontColor=#808080;fontStyle=1\&quot; value=\&quot;【2026-8-1】wqw\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;30\&quot; width=\&quot;171\&quot; x=\&quot;649\&quot; y=\&quot;1420\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-1\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;效果评估\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;130\&quot; x=\&quot;175\&quot; y=\&quot;970\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-2\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;运行轨迹\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;130\&quot; x=\&quot;400\&quot; y=\&quot;830\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-3\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;反馈/评分\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;130\&quot; x=\&quot;660\&quot; y=\&quot;970\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-4\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;经验提炼\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;130\&quot; x=\&quot;660\&quot; y=\&quot;1169\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-5\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;持久更新\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;130\&quot; x=\&quot;410\&quot; y=\&quot;1270\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-6\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;任务复用\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;130\&quot; x=\&quot;175\&quot; y=\&quot;1150\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-7\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;o9i-vX3893mFWcsgBhXv-1\&quot; style=\&quot;html=1;endArrow=block;strokeWidth=4;fontSize=19;fontStyle=1;fontColor=#808080;strokeColor=#999999;exitX=0.648;exitY=-0.003;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; target=\&quot;o9i-vX3893mFWcsgBhXv-2\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; x=\&quot;0.326\&quot; y=\&quot;48\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n            &lt;mxPoint x=\&quot;270\&quot; y=\&quot;957\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;410\&quot; y=\&quot;920\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-8\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;o9i-vX3893mFWcsgBhXv-2\&quot; style=\&quot;html=1;endArrow=block;strokeWidth=4;fontSize=19;fontStyle=1;fontColor=#808080;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; target=\&quot;o9i-vX3893mFWcsgBhXv-3\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; x=\&quot;0.326\&quot; y=\&quot;48\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n            &lt;mxPoint x=\&quot;560\&quot; y=\&quot;1085\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;701\&quot; y=\&quot;1000\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-9\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;o9i-vX3893mFWcsgBhXv-3\&quot; style=\&quot;html=1;endArrow=block;strokeWidth=4;fontSize=19;fontStyle=1;fontColor=#808080;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; target=\&quot;o9i-vX3893mFWcsgBhXv-4\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; x=\&quot;0.326\&quot; y=\&quot;48\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n            &lt;mxPoint x=\&quot;790\&quot; y=\&quot;1135\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;931\&quot; y=\&quot;1050\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-10\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;o9i-vX3893mFWcsgBhXv-4\&quot; style=\&quot;html=1;endArrow=block;strokeWidth=4;fontSize=19;fontStyle=1;fontColor=#808080;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;\&quot; target=\&quot;o9i-vX3893mFWcsgBhXv-5\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; x=\&quot;0.326\&quot; y=\&quot;48\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n            &lt;mxPoint x=\&quot;620\&quot; y=\&quot;1375\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;761\&quot; y=\&quot;1290\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-11\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;o9i-vX3893mFWcsgBhXv-5\&quot; style=\&quot;html=1;endArrow=block;strokeWidth=4;fontSize=19;fontStyle=1;fontColor=#808080;strokeColor=#999999;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; target=\&quot;o9i-vX3893mFWcsgBhXv-6\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; x=\&quot;0.326\&quot; y=\&quot;48\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n            &lt;mxPoint x=\&quot;450\&quot; y=\&quot;1255\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;591\&quot; y=\&quot;1170\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-12\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;o9i-vX3893mFWcsgBhXv-6\&quot; style=\&quot;html=1;endArrow=block;strokeWidth=4;fontSize=19;fontStyle=1;fontColor=#808080;strokeColor=#999999;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; target=\&quot;o9i-vX3893mFWcsgBhXv-1\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; x=\&quot;0.326\&quot; y=\&quot;48\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n            &lt;mxPoint x=\&quot;269\&quot; y=\&quot;1000\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;410\&quot; y=\&quot;915\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-18\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=29;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#333333;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;大部分自进化系统关注点&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;350\&quot; x=\&quot;330\&quot; y=\&quot;1120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-20\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=29;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#333333;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;缺失环节&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;140\&quot; x=\&quot;415\&quot; y=\&quot;940\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-21\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=29;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#333333;fontStyle=1\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;自进化层级&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;250\&quot; x=\&quot;1140\&quot; y=\&quot;750\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-22\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;记忆层\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;130\&quot; x=\&quot;1100\&quot; y=\&quot;1330\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-23\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;技能/工具层\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;180\&quot; x=\&quot;1075\&quot; y=\&quot;1209\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-24\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;提示词/策略层\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;180\&quot; x=\&quot;1070\&quot; y=\&quot;1080\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-25\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;架构层\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;130\&quot; x=\&quot;1095\&quot; y=\&quot;970\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-26\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontSize=26;shadow=1;glass=0;fontStyle=1;fontColor=#ffffff;\&quot; value=\&quot;模型权重层\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;70\&quot; width=\&quot;165\&quot; x=\&quot;1070\&quot; y=\&quot;850\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-27\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=29;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#333333;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;长期经验复用&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;200\&quot; x=\&quot;1255\&quot; y=\&quot;1340\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-28\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=29;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#333333;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;可执行能力沉淀&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;220\&quot; x=\&quot;1270\&quot; y=\&quot;1220\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-29\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=29;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#333333;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;工作流自动化&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;200\&quot; x=\&quot;1255\&quot; y=\&quot;1090\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-30\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=29;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#333333;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;代码/架构改写&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;200\&quot; x=\&quot;1235\&quot; y=\&quot;980\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-31\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=29;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#333333;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;在线学习/再训练&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;220\&quot; x=\&quot;1250\&quot; y=\&quot;860\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-32\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; style=\&quot;html=1;endArrow=block;strokeWidth=4;fontSize=19;fontStyle=1;fontColor=#808080;strokeColor=#999999;\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; x=\&quot;0.326\&quot; y=\&quot;48\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1530\&quot; y=\&quot;1410\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1530\&quot; y=\&quot;840\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-33\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=24;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#999999;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;落地成熟度&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;130\&quot; x=\&quot;930\&quot; y=\&quot;1420\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-34\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; style=\&quot;html=1;endArrow=block;strokeWidth=4;fontSize=19;fontStyle=1;fontColor=#808080;strokeColor=#999999;\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; x=\&quot;0.326\&quot; y=\&quot;48\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1025\&quot; y=\&quot;840\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1025\&quot; y=\&quot;1410\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-36\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=24;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#999999;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;生产风险&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;130\&quot; x=\&quot;1490\&quot; y=\&quot;1420\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-37\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=24;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#999999;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;低风险&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;95\&quot; x=\&quot;1540\&quot; y=\&quot;1350\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-38\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=24;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#999999;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;高风险&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;95\&quot; x=\&quot;1540\&quot; y=\&quot;860\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-39\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=24;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#999999;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;高成熟&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;95\&quot; x=\&quot;930\&quot; y=\&quot;1340\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;o9i-vX3893mFWcsgBhXv-40\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=24;fillColor=none;fillStyle=solid;labelBackgroundColor=none;fontColor=#999999;fontStyle=0\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;低成熟&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;95\&quot; x=\&quot;920\&quot; y=\&quot;860\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


大多数自称"自进化"的系统至多实现了"经验提炼→持久更新→后续任务复用"这中间三段（"经验提炼"往往还只是粗暴摘要），而"反馈/评分"和"效果评估"这两个评价环节普遍缺位

记忆和技能沉淀的基础设施已实用化，提示词自动优化半实用，架构和权重层自改进仍是研究品——而严格意义上的完整自进化闭环，在哪一层都还算不上普遍。卡住后两层的，不是"怎么进化"，是"怎么评估"——Agent 自己改了自己，谁来判断改得对不对？

### 综述：AI 如何实现自我进化

【2025-7-30】普林斯顿、清华、CMU等综述：AI 如何实现自我进化？

截止2025年7月,「自进化智能体」（Self-Evolving Agents）领域的进展。
- 当前，尽管大语言模型（LLM）能力强大，但本质上「静态」，一旦训练完成，其内部参数就不会再改变。
- 这在需要实时适应新知识、新任务的动态世界中成了一个巨大的瓶颈。

与环境互动、从经验中**学习并持续自我完善**的智能体。

理论框架，围绕三个核心问题展开：**进化什么**（What）、**何时进化**（When） 以及 **如何进化**（How）。
- 论文： [A Survey of Self-Evolving Agents: On Path to Artificial Super Intelligence](https://arxiv.org/pdf/2507.21046)
- github [Self-Evolving-Agents](https://github.com/CharlesQ9/Self-Evolving-Agents)

What-When-How 框架系统地解构和理解所有关于「自进化」的研究。三个维度分别是：
- （1）进化什么？（What to Evolve?）：智能体作为一个系统，它的哪些部分可以被改进？模型、上下文、工具、架构
- （2）何时进化？（When to Evolve?）：进化的过程发生在任务的哪个阶段？
  - 「任务中进化」追求的是灵活性和即时响应
  - 「任务间进化」追求的是系统性提升和长期成长。
  - 一个优秀的自进化智能体，需要兼具这两种能力。
- （3）如何进化？（How to Evolve?）：驱动进化的具体方法和信号是什么？
  - 三大类进化引擎：奖励、模仿和演化

![](https://pic4.zhimg.com/v2-3d0bdc6e5d1c69f1ce9a3c0b42804e45_1440w.jpg)

### 斯坦福 自进化 Agent课程

【2026-8-10】Stanford 研究生课程 
- 主页 [CS329A：Self-Improving AI Agents](https://cs329a.stanford.edu/)
- [YouTube地址](https://www.youtube.com/playlist?list=PLangBM27OtEA) 一共 9 讲。

围绕问题展开：AI Agent 怎么通过和环境不断交互，持续改进自己的能力。

内容从 Test-Time Compute、Verifier 和 RL 讲起，后面会进入工具/代码反馈、多步推理与规划、Deep Research、自我改进，以及 Agent 的长时任务评测。

把散落在论文里的方向串到一起：从「怎么让 Agent 多思考」，一路讲到「怎么验证结果、从反馈学习，再把这些能力放进更长的任务里」。


### 五个层级

自进化的五个层级
1. `记忆层`。 把交互历史沉淀成长期记忆，下次遇到类似问题直接复用——"这个用户的部署环境是 K8s"、"上次这个报错的根因是配置漂移"。目前最成熟、最普及的一层，Mem0、Letta（原 MemGPT）是这一层的代表性基础设施。
2. `技能/工具层`。 Agent 把验证过的解题过程固化成可复用的技能，甚至自己写新工具。经典案例是 2023 年的 Voyager：在 Minecraft 里自动探索，把学会的动作沉淀成代码技能库，后续任务直接调用，能力滚雪球式增长——全程不微调模型权重。Claude Code 的 Skills 机制常被拿来类比，但要说清楚：Skills 是技能沉淀的承载形式，目前主要由人编写、Agent 辅助生成。只有当 Agent 能自动完成提议、验证、注册、回滚这一整套动作时，才算进入自进化——有 skill 机制不等于在自进化。
3. `提示词/策略层`。 自动优化自己的提示词和工作流。DSPy 这类框架把提示词当可优化参数，但要分清优化发生在哪：发生在离线编译阶段的，是开发期优化，按本章定义不算自进化；只有优化结果在运行期被持久写回、影响后续任务，才进入自进化的讨论范围。self-refine 循环同理——跑一遍、自我批评、改进策略再跑，改进若不出会话，就只是反思。这一层的工具链已经成熟，真正闭环到运行期持久写回的用法还不多。
4. `架构层`。 Agent 修改自己的代码和结构。2025 年 Sakana AI 与 UBC 的 Darwin Gödel Machine 是标志性工作：Agent 重写自己的实现代码，用编码基准实证验证每次修改，维护一个不断扩张的变体档案库做"进化树"。成绩是真的：SWE-bench 从 20.0% 提到 50.0%，Polyglot 从 14.2% 提到 30.7%。但前提也是论文摘要自己写明的："All experiments were done with safety precautions (e.g., sandboxing, human oversight)"——这是带沙箱、带人工监督、有干净评分基准的实验结果，不代表生产系统的成熟度。
5. `模型权重层`。 通过在线 RL 或自生成数据微调更新模型本身。学术定义里它是自进化的一层，但在生产闭环里直接在线更新权重仍极少见——现实中这个需求通常被拆解成离线再训练、灰度评测、安全审核的传统流程。它不是什么


资料
- [什么是Agent自进化](https://mp.weixin.qq.com/s/ipdGfq75THZrxDiZ2RbY2w)


## 技术路线

按"是否更新模型权重"和"是否依赖人工数据"两个维度划成了三类

| 路线 | 更新模型权重？ | 依赖人工数据？ | 代表工作 |
| ---- | ---- | ---- | ---- |
| 第一类：经验/Skill存储型 | ❌ 不更新 | ❌ 依赖 | AutoSkill、EvoSkill、MemSkill、CoEvoSkills、SE-Agent、Hermes |
| 第二类：RL训练型 | ✅ 更新 | ❌ 依赖 | EvolveR、SAGE、SkillRL、SKILL0、SkillIOS、AgentEvolver |
| 第三类：0数据自学型 | ✅ 更新 | ✅ 不依赖 | Agent0、Tool-R0、Absolute Zero |

差异：
- 第一类给 Agent 配一本"工作笔记"，模型本身不动，只在需要时翻阅；
- 第二类直接把"工作笔记"上的经验通过 RL 写进模型的权重里，让 Agent 真正"长本事"；
- 第三类更激进——干脆连"老师"都不要了，让 Agent 之间互相出题互相考试，自己跟自己打。

【2026-7-27】腾讯技术工程文章：[Agent开始“自我进化”：会出题、会反思，还会自己长出新技能](https://mp.weixin.qq.com/s/fsVJiorPBN4ylGjUYBcIPw)


### 第一类：经验/Skill 存储型

经验/Skill 存储型（不更新模型权重）

特征：
- 不训练、跨会话保留上下文、文件式存储；核心是把经验沉淀为可检索/可复用的"技能（Skill）"。类比来看，这类工作就像是给 Agent 配了一个"外挂大脑"，本体（base LLM）保持冻结，所有的"成长"都发生在外挂里。

案例
- AutoSkill（arXiv: 2603.01145) 双环结构, 动态增删改查 Skill 来防止 Skill 库爆棚。
- EvoSkill（arXiv: 2603.02766）让多个 Agent 分工协作——执行、反思、落地——把"失败"变成"新 Skill"，并用 Pareto 前沿机制保证 Skill 库永远精而不滥。EvoSkill 来自 Sentient 和弗吉尼亚理工的合作工作，主张是把传统 Agent "失败即重试" 的笨办法改造成 "失败即学习" 的进化闭环。它的最大特点是把 Skill 当作一等公民来升级，而不是只在 prompt / code 层面做文字游戏。
- MemSkill（arXiv: 2602.02474）前两个工作针对用户指令；MemSkill 只针对操作 Memory 的 Skill 做自进化。
- CoEvoSkills（arXiv: 2604.01687v2）TLDR：给每条新总结的 Skill 配一个"考官"（Verifier），生成的 Skill 必须先通过考试才能进库；通不过就带反馈打回，让 Generator 重写——这是把软件工程的"单元测试"理念搬到了 Skill 进化里。CoEvoSkillsn解决老大难问题：Skill 总结出来到底靠不靠谱？ AutoSkill / EvoSkill 都是"生成完了直接入库"，质量基本靠 LLM 自觉。CoEvoSkills 的回答是：不能靠自觉，得有验证闭环。
- SE-Agent（arXiv: 2508.02085）与其反复"自我反思"在同一条轨迹上小修小补，不如一次跑出多条轨迹，让它们互相借鉴、互相打磨——SE-Agent 把 Agent 自进化从"单线程深度修补"切到了"多线程横向融合"。

更多见站内技术专题：[Skill自进化](llm_skill)


### 第二类：基于 RL 的训练型自进化


特征：
- 通过 RL 训练直接更新模型权重，让模型从根本上变强。当前学术界与工业界的主流方向

第二类工作走得比第一类更远：把经验从"外挂"变成了"权重"。

但仔细看仍能拎出几条共性：核心点 
1. 仍然依赖训练集反馈（除 AgentEvolver 外） 核心点
2. 核心是 RL rollout 时继承/更新之前的 skill核心点
3. 不算严格意义的"RL by talking" —— 因为反馈仍来自任务结果或人工标签，而不是交互对话本身

案例
- EvolveR（arXiv: 2510.16079）
- SAGE（arXiv: 2512.17102）提出 Sequential Rollout —— RL rollout 时序列化地跑一系列相似任务，后序任务训练时就可以使用前序生成的 skill。
- SkillRL（arXiv: 2602.08234）用强模型（o3）蒸馏 Skill，再通过 RL 训练弱模型学会使用，并递归进化技能库
- SKILL0（arXiv: 2604.02268）将 Skill 从推理时的"外挂上下文"内化到模型参数，实现零样本执行（每步 < 0.5K tokens）。
- SkillOS（arXiv: 2605.06614）最有启发。训练专门的 Curator，通过 RL 学会如何增 改 删 SkillRepo，而不是直接学如何使用 Skill。
  - 核心设计哲学："学会如何管理技能，而不是学会如何使用技能" —— Executor 冻结，只训练 Curator，通过长周期间接奖励信号学习 Skill 的增删改策略。
- AgentEvolver（arXiv: 2511.10395）完全自主的三环自演化框架 —— 自出题、自解题、自总结经验，全链路无需人工标注。

### 第三类：0 数据自学型

特征：
- 完全不要人工标注的数据，靠 Agent 之间互相出题/解题闭环。

这一类的精神更激进：连数据集都不要，Agent 自己出题自己考自己。

总结：真·不需要训练数据通用流程：
> 出题 Agent 训练 → 出题构造数据集 → 解题 Agent 训练 → 出题 Agent 训练 …

核心点 
1. 全靠出题的 Agent 自己核心点
2. 准确率判断大多靠对照出题 Agent 自己给出的答案——这是个隐患，sliver answer 的可靠性需要打问号核心点
3. 最好要有自动化的判断标准——比如 Absolute Zero 用的代码执行器核心点
4. 出题难度很重要——太难学不懂，太简单学不到，这个 reward shaping 是核心难点核心点
5. 评估很混乱——只有数学类的 benchmark 勉强出现了多次，其余几乎完全没有重叠，可比性差

案例
- Agent0（arXiv: 2511.16043）学习工具使用，一个 Agent 负责出题，一个 Agent 负责解题。
- Tool-R0（arXiv: 2602.21320）类似 Agent0，但做的是 general tool 而不是纯数学。
- Absolute Zero（arXiv: 2505.03335）单个模型同时扮演出题人和解题人，用代码执行器作为唯一的验证来源，完全不碰任何外部数据。


## 进化案例

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


### 【2025-8-5】CMU SQLM


大语言模型的训练很大程度上仍依赖人工整理**数据集**，堪称费时费力。

为了减轻这一负担，研究人员开发了用于强化学习的**无监督奖励函数**，然而，这些函数仍然依赖于预先提供的**高质量输入提示**。

因此，问题难点从“生成答案”转移到了“生成高质量问题”。

当前方法的关键不足：
- 缺乏可扩展且自我维持的流程，能够在无人干预的情况下自动生成有意义的问题和答案。

【2025-8-5】[无需外部数据！AI自问自答实现推理能力进化](https://mp.weixin.qq.com/s/Q3fc95LXM3PuytdEBnUCSA)

卡内基梅隆大学提出新框架`SQLM`——一种无需外部数据的自我提问模型。
- 论文 [SELF-QUESTIONING LANGUAGE MODELS](https://www.alphaxiv.org/abs/2508.03682v1)
- 该框架包含`提问者`（proposer）和`解答者`（solver）两个角色，提问者生成与给定主题相关的问题，解答者旨在解决问题。
- SQLM框架，非对称的自我博弈框架

堪称：带 RL 的 GAN

实验结果显示
- SQLM 将 Qwen2.5-3B-Instruct 在算术任务上的准确率提高了**14%**，在代数任务上提高了16%；在编程任务上的准确率提高了7%。

此外，上表还显示出SQLM显著优于格式奖励基线（用于稳定训练和规范输出格式的参考值），表明推理能力的真正提升。


### 【2025-8-7】腾讯 R-Zero


【2025-8-7】腾讯AI Lab（西雅图），[腾讯AI Lab推出「零数据自进化」推理LLM]()
- 论文标题：[R-Zero: Self-Evolving Reasoning LLM from Zero Data](https://arxiv.org/pdf/2508.05004)
- 项目主页 [R-Zero: Self-Evolving Reasoning LLM from Zero Data](https://chengsong-huang.github.io/R-Zero.github.io/)
- Code: [R-Zero](https://github.com/Chengsong-Huang/R-Zero).

自我进化的大语言模型（LLM）通过自主生成、优化并从自身经验中学习，为实现超级智能提供了可扩展的途径。

然而，当前训练此类模型的现有方法仍高度依赖于海量的人工标注任务和标签，通常通过微调或强化学习实现，这构成了推动人工智能系统超越人类智能能力的根本瓶颈。

为克服这一限制，腾讯AI Lab 团队推出了一个完全自主、能够从零开始生成自我训练数据的框架——`R-Zero`。

从单个基础 LLM 出发，`R-Zero` 初始化两个具有不同角色且独立运行的模型：`挑战者`（Challenger）和`解决者`（Solver）。

![](https://chengsong-huang.github.io/R-Zero.github.io/static/images/method.png)

这两个模型分别进行优化，并通过相互作用实现协同进化：
- `挑战者`因提出接近解决者能力边界的任务而获得奖励，而`解决者`则因解决挑战者提出的日益复杂的任务而获得奖励。

![](https://chengsong-huang.github.io/R-Zero.github.io/static/images/abstract.png)

这一过程产生了无需预先存在的任务和标签的针对性、自我改进的课程。

	
实验结果表明
- R-Zero 显著提升了不同基础 LLM 的推理能力，例如在数学推理基准测试中使 Qwen3-4B-Base 的性能提升 6.49，在通用领域推理基准测试中提升 7.54。


### 【2025-11-20】斯坦福 agent0 

【2025-11-20】斯坦福 agent0 
- 论文：[Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning](https://arxiv.org/abs/2511.16043)
- 代码 [Agent0](https://github.com/aiming-lab/Agent0)

已有自我进化框架：受限于模型能力和单轮交互，难以实现包含工具使用、动态推理的复杂模式进化

Agent0 全自主的智能体进化框架，通过多步协同进化、无缝工具集成，无需外部数据即可培育出高性能智能体

Agent0 让两个基于相同 LLM 初始化的智能体形成共生竞争关系：
- 一个是课程智能体，负责提出难度逐步提升的前沿任务；
- 另一个是执行智能体，专注于学习解决这些任务。

框架集成外部工具以增强执行智能体的问题解决能力，反过来促使课程智能体设计更复杂、且能适配工具使用的任务。

通过这一迭代过程，Agent0 构建起自我强化的循环，持续生成高质量的训练课程。


核心思想：
- Agent0 从同一个基础LLM创建两个智能体，并迫使它们进入竞争性的反馈循环。
- 一个发明任务，一个试图生存。这种持续的推拉产生的前沿难度问题是任何静态数据集都无法比拟的。

解决了自进化智能体的最大失败模式：停滞。

大多数智能体只生成比他们当前水平稍微难一点的问题。Agent0使用不确定性、采样答案之间的分歧和工具调用频率来检测执行智能体的弱点。

<img width="894" height="471" alt="image" src="https://github.com/user-attachments/assets/39c41bb2-45b7-41be-9d5b-55518f54c0ed" />

<img width="901" height="393" alt="image" src="https://github.com/user-attachments/assets/b50b3dce-2f66-48d7-a3ae-8752fbb230f6" />


实证结果表明
- Agent0 显著提升了模型的推理能力：在数学推理基准测试中，Qwen3-8B-Base 模型性能提升 18%；在通用推理基准测试中，性能提升 24%。

### 【2025-11-13】AgentEvolver

【2025-11-13】通义实验室开源新框架 AgentEvolver，通过「自我提问」「自我导航」「自我归因」三大机制，系统性解决智能体强化学习中的任务稀缺、探索低效和样本利用率低等瓶颈。
- 技术报告 [AgentEvolver: Towards Efficient Self-Evolving Agent System](https://arxiv.org/pdf/2511.10395)
- github [AgentEvolver](https://github.com/modelscope/AgentEvolver)

大多数智能体系统仍停留在“按照指令完成任务”的层面——**缺乏持续学习、适应变化**的能力。

三大瓶颈：
- 任务构建成本高：新的环境往往需要重新定义任务与目标，人工成本高、覆盖面有限。
- 探索效率低：强化学习依赖大量交互采样，训练成本与时间消耗巨大。
- 样本利用不充分：奖励稀疏且模糊，模型难以判断哪些中间步骤真正起作用。

AgentEvolver 推动智能体从“被训练”迈向“自进化”的新范式


AgentEvolver 核心是由三大机制驱动的动态学习闭环。让智能体不再是被动执行任务的“工具”，而是一个能不断学习、总结、改进的动态系统

三大机制的协同作用，驱动智能体在复杂环境中持续优化和演化：
- 自我任务生成（Self-Questioning）：自主生成探索任务，摆脱对人工数据集的依赖。
- 自我经验导航（Self-Navigating）：高效复用历史经验，提升探索效率。
- 自我反思归因（Self-Attributing）：精细评估步骤级奖励，提升样本利用率。

<img width="1080" height="646" alt="image" src="https://github.com/user-attachments/assets/162cbec1-891b-49e1-8980-2cbecee53e77" />

自我任务生成

<img width="1080" height="437" alt="image" src="https://github.com/user-attachments/assets/a5aeec62-887f-446d-afaf-d70d2de0bc5f" />

### 【2026-3-17】MetaClaw

【2026-3-17】CMU、伯克利推出 MetaClaw 持续元学习框架
- 论文 [MetaClaw: Just Talk -- An Agent That Meta-Learns and Evolves in the Wild](https://arxiv.org/pdf/2603.17187)
- Github: [MetaClaw](https://github.com/aiming-lab/MetaClaw)

结合 OpenClaw，精准解决落地智能体静态固化、能力跟不上用户需求漂移的核心痛点。

🔑 关键方法
- 1️⃣ 技能驱动快速适配：从失败轨迹中蒸馏可复用的行为指令，无参数更新、零服务停机，prompt注入即刻生效
- 2️⃣ 机会主义策略优化：通过OMLS调度器捕捉用户空闲窗口，用云端LoRA+RL做梯度更新，全程不打扰正常使用

💡 核心创新
- 1️⃣ 双时间尺度互补闭环：秒级prompt技能进化+小时级梯度策略优化双向赋能，形成越用越强的良性学习循环
- 2️⃣ 技能版本隔离机制：严格拆分支撑数据与查询数据，彻底解决旧轨迹 stale reward 污染RL训练的行业痛点
- 3️⃣ 轻量化代理架构：无需本地GPU，兼容主流LLM厂商与智能体平台，可直接落地生产级大模型

📊 实验效果
- ✅ 纯技能适配让Kimi-K2.5准确率相对提升最高32.2%，全流程将其准确率从21.4%拉至40.6%，几乎追平GPT-5.2基线
- ✅ 端到端任务完成率提升8.25倍，文件校验完成率暴涨185%
- ✅ 跨域适配23步全自动科研管线，仅技能注入就将综合鲁棒性提升18.3%，阶段重试率降低24.8%


### 【2026-3-19】LSE

LLM 部署后遇到新任务时，最常见的做法是"自我反思"——让模型审视之前的失败并修改自己的 prompt。但问题：没人教过模型怎么做"自我进化"这件事。
- 所有现有方法（TextGrad、GEPA 等）都依赖模型天生的推理能力来做 prompt 优化，从未专门训练过这项技能。

问题
- 从未被专门训练
- 线性路径锁死
- 奖励信号含噪

Snowflake 团队提出 `LSE`（Learning to Self-Evolve）框架：用强化学习训练 4B 参数的"自进化策略"，专门学习**如何改进上下文**。
- 配合 UCB 树搜索防止进化路径塌缩，LSE 训练的 Qwen3-4B 在 Text-to-SQL（BIRD）上以 67.3% 超越 GPT-5 的 65.2%，在 MMLU-Redux 上以 73.3% 超过 GPT-5 的 72.5%。平均提升 +6.7 个百分点。 LSE 学到的不是针对特定模型的技巧，而是一种通用的"如何从反馈中改进上下文"的元能力
- 更关键: 训练好的自进化策略可以零样本迁移到完全不同的模型上，为其提供 +6.7% 的提升。
- 论文 [Learning to Self-Evolve](https://arxiv.org/pdf/2603.18620)
- 解读 [4B 小模型击败 GPT-5：Learning to Self-Evolve 用强化学习教会 LLM 在测试时自我进化](https://zhuanlan.zhihu.com/p/2019744547450697438)


LSE 框架总览。
- 左侧为测试时的树引导自进化循环——UCB 算法从进化树中选择节点，Action Model 在新批次上执行后生成性能摘要，Self-Evolving Policy 据此提出新上下文。
- 右侧为训练流程——用改进量（编辑后性能 - 编辑前性能）作为 RL 奖励信号。

![](https://picx.zhimg.com/v2-afe24cf97a6a6c6e925c545d411ee6e5_1440w.jpg)


### 【2026-3-24】Hermes Agent

【2026-3-24】自主进化 Hermes Agent 适合自动化编程、浏览器操作等需持续学习的场景，能从任务中自动提炼复用技能。作为新兴开源项目，初期配置有一定技术门槛，复杂任务中的自主进化能力可能需要调优。
- 项目主页：[Hermes Agent](hermes-agent.nousresearch.com)，GitHub [hermes-agent](https://github.com/NousResearch/hermes-agent)

Nous Research 开发的开源自主 AI 智能体，2026年2月27日正式发布

```sh
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
hermes              # start chatting!
# 命令
hermes              # Interactive CLI — start a conversation
hermes model        # Choose your LLM provider and model
hermes tools        # Configure which tools are enabled
hermes config set   # Set individual config values
hermes gateway      # Start the messaging gateway (Telegram, Discord, etc.)
hermes setup        # Run the full setup wizard (configures everything at once)
hermes claw migrate # Migrate from OpenClaw (if coming from OpenClaw)
hermes update       # Update to the latest version
hermes doctor       # Diagnose any issues
```

随你成长的 AI 智能体。

部署在自己服务器上，连接消息账号，成为持久个人智能体
- 学习你的项目、自动构建技能、随时随地触达你。不是聊天机器人，不是代码补全工具，而是一个住在你机器上、每天都在变聪明的智能体。

Hermes Agent 将持久记忆、自动技能创建和多平台接入整合在一个开源包中。
- 持久记忆：跨会话记住你的偏好、项目和环境。运行越久，越了解你——不再需要每次重新解释上下文。
- 自动技能创建：当 Hermes 解决了一个难题，它会写下可复用的技能文档，永远不会忘记解决方法。技能可搜索、可分享，兼容 agentskills.io 开放标准。
- 多平台消息网关：通过单一网关进程连接 Telegram、Discord、Slack、WhatsApp、Signal 和 CLI。支持语音备忘录转录，跨平台无缝切换。在 Telegram 开始对话，在终端继续。
- 定时自动化任务：内置 cron 调度器，可向任意平台推送。设置每日报告、夜间备份、每周审计和晨间简报——全部无人值守运行。
- 并行子智能体：为并行工作流生成隔离的子智能体，每个都有独立的对话和终端。通过 RPC 将多步骤流水线压缩为零上下文消耗的操作。
- 完整浏览器与网页控制：网页搜索、页面提取、完整浏览器自动化——导航、点击、输入、截图。还支持视觉分析、图像生成、文字转语音和多模型协作推理。

支持本地龙虾信息迁移: 导入人设、记忆、技能、命令、消息、api等信息

```sh
hermes claw migrate              # Interactive migration (full preset)
hermes claw migrate --dry-run    # Preview what would be migrated
hermes claw migrate --preset user-data   # Migrate without secrets
hermes claw migrate --overwrite  # Overwrite existing conflicts
```

### 【2026-3-19】 HyperAgents

【2026-4-15】[AI学会左脚踩右脚自进化？Meta华人新研究改写Agent法则](https://mp.weixin.qq.com/s/TA4U9_nH1qzZqFS8DGQ0vQ)

【2026-3-19】华人学者 Jenny Zhang 在Meta实习期间，联合Meta AI、UBC、纽约大学等机构研究者，提出新智能体框架：HyperAgents（DGM-H）。
- 论文 [Hyperagents](https://arxiv.org/pdf/2603.19461)

重点不是再造一个更能干活的Agent，而是瞄准更高层问题：
- 如果AI已经能够修改自己的任务解法，那能不能连「自己以后该怎么修改自己」这件事，也一并改掉？可以

HyperAgents 把「执行任务的 agent」和「负责改进 agent 的 meta agent」合并进同一个可编辑程序里，作者将之称为 hyperagent。

新框架下，系统不只会修改任务求解逻辑，还开始修改未来生成改进方案的机制本身，称为 metacognitive self-modification，元认知自我修改。

过去行业竞争的是：谁的Agent更会干活。而HyperAgents 指向的下一阶段则可能是：谁的Agent更会变强，而且会越来越会变强。

上一代自我进化路线的天花板。

去年 Darwin Gödel Machine（DGM）已经很惊艳。在coding任务中不断自改代码、自我验证、把成功版本存进archive，再从这些「垫脚石」里继续往前长。

但DGM 之所以能在coding里成立，是因为「评估」和「自我修改」本身也都是coding任务。一旦离开coding，这个对齐关系就断了。比如评审论文、设计机器人奖励函数、给IMO级数学解答打分，这些任务做得更好，不等于你就更会修改自己的元机制。

HyperAgents 最核心的一招：直接把这个假设砍掉：
> 既然任务能力和自我改进能力未必天然对齐，那就不要再把meta层写死。

表面上看，HyperAgents只是多了一个meta agent。

但真正值得注意的是，它把task agent和meta agent合成了同一个可编辑程序。HyperAgents 不是「再加一个Agent」，而是取消了「上层永远不变」这个默认前提。

### 【2026-6-30】POLARIS

【2026-6-30】[7B模型也想实现递归自我进化？POLARIS 说没问题](https://mp.weixin.qq.com/s/uxHW6cCjdn-7qlzP6XfZzw)

哥德尔智能体（Gödel Agent） 提出的“`递归自我改进`”概念虽然酷炫，但在 7B 等规模的模型（SLM）上落地时面临严重的资源瓶颈。

常因上下文增长过快导致 OOM（内存溢出）或工具调用失范。

其根源在于：
- 验证集冗余：原框架需在内存中保留 20 个验证样本及其完整的推理链路；
- 历史链条过长：保留过多的进化步骤和工具调用历史（通常为 10 步），挤占了 SLM 稀缺的上下文窗口。

POLARIS 核心价值在于证明：递归自我改进并非大模型专属。

通过将“学习”转化为“针对自身 Policy 代码的结构化修补”，SLM 同样能在部署后通过与环境的交互完成自我进化。

核心方案：基于经验抽象的策略修复

POLARIS 放弃了全量存储失败案例，转而采用一种类似“自动程序修复（APR）”的四阶段循环：
- A. 失败分析（Failure Analysis）: 智能体调用 AnalyzeFailure 算子，对 N 个（通常取 3 或 5）失败样本进行反思，生成包含故障诊断、修正方案和预防规则的结构化记录 A_i。
- B. 策略综合（Strategy Synthesis）通过 StrategySynthesis 算子，模型将零散的报错记录 A 压缩为通用指令集 delta（如任务分解、逻辑一致性检查等），从而实现跨任务的经验迁移。
- C. 最小化补丁生成（Patch Generation）POLARIS 要求模型生成最小化代码补丁。
  - 非参数化更新：不修改权重，而是通过修改执行策略代码 π 来实现进化。
  - 局部修改：补丁仅涉及实现 delta 所需的必要代码行，确保了进化的可审计性和低内存占用。
- D. 运行时变异与集成（Patch Integration）系统利用 Python 运行时的动态特性，通过 IntegratePatch 过程将代码注入；且集成前需经过语法检查和执行验证，若失败则启动有限次数（默认 3 次）的退避重试。


POLARIS 框架如何通过 经验抽象（Experience Abstraction） 与 代码补丁（Code Patch） 技术，在受限算力下实现智能体策略的持续进化。

为了在 Qwen2.5-7B 等模型上保持稳定运行，POLARIS 进行了以下深度调优：
- 超参数 N 控制：将参与反思的失败样本数 N 严格限制在 3-5 个；
- 历史步数收减：将工具调用消息历史 k 从 10 条缩减至 6 条，有效缓解了推理阶段的上下文压力；
- 格式校验器：引入轻量级辅助 Agent 强制执行 JSON 格式验证，解决 SLM 工具调用不稳定的硬伤。

实验结论：非单调性中的持续增益

在 MGSM、GPQA 和 DROP 等硬核推理测试中，POLARIS 展现了显著的进化能力：
- 性能提升：在 GPQA 研究生级难题上，准确率相对 COT-SC 基准提升了 9.0%；
- 进化动力学：虽然进化曲线呈现非单调波动（由离散代码变异引入的随机性），但通过 “冠军-挑战者”模式（Champion–Challenger Pattern） 部署最佳策略，可确保实际性能的稳步增长。


### 【2026-7-18】阿里巴巴

【2026-7-18】阿里巴巴通义实验室 丁瑞雪，[垂域模型自进化：Agentic RL企业级落地生产实践](https://www.bilibili.com/video/BV16HKn6gEw5), 多个业务场景进化实践
- 高德小高老师、1688 鳌虾、阿里云安全攻防Agent、盒马AI Agent

1. 开源项目 [qqr](https://github.com/Alibaba-NLP/qqr)
2. 学术论文 [ArenaRL](arxiv.org/abs/2601.06487) ICML 2026
3. 配套数据集 Open-Travel、Open-DeepResearch

4+企业级场景验证，全面超越PE方案

|场景分类|落地业务|落地能力|
| ---- | ---- | ---- |
|出行|高德|复杂路线规划<br>多轮工具调用<br>全量流量承接|
|电商|盒马、1688|商品筛选<br>导购搜索<br>选品报告生成|
|安全|云安全|入侵分析<br>沙箱推演<br>修复方案生成|

（1）高德出行：从PE到RL完整进化路径

业务整体链路
- 用户一句话提交出行需求 → 多轮调用33个工具 → 完成复杂路线规划

模型迭代流程
- PE基线 → SFT冷启 → Agentic RL → 效果超越人工重度调优SFT

核心指标
1. **双盲评测胜率**：＞90%
2. **工具链规模**：共计33个可调用工具，支撑多轮复杂调用
3. **落地上线**：支持全量流量正式投产

（2）电商场景：导购搜索 & 海量选品

|模块|核心信息|
| ---- | ---- |
|电商导购|1. 基于垂域小模型训练专属模型，支持私有化部署<br>2. 准确率相比通用大模型PE方案提升20个百分点以上<br>3. 已灰度上线，各项核心商业指标正向向好|
|电商选品|1. 覆盖海量商品筛选、货品研判、自动生成选品报告全流程<br>2. 评测分数比PE方案高出45%，同样优于行业同类竞品|

结论
- 垂域小模型效果 >> 通用大模型 + PE方案。

（3）垂域RL整体方案：效果提升、成本下降、延时降低

面向具体业务定制垂域Agent模型，支持自主出题、自我学习、自我评估，是Agent规模化落地生产环境的可行路线。

|模块|解决痛点|关键优势|
| ---- | ---- | ---- |
|自动课程学习|训练数据源匮乏|全流程自动化，产出数据质量高于人工标注|
|在线经验注入|优质交互轨迹难以采集|增加训练门槛管控，有效防止模型性能负迁移|
|Pairwise Reward|奖励信号波动不稳定|训练复杂度为O(N)，相关成果收录于ICML 2026|

自进化飞轮：从单场景能力拓展至通用能力

完整流转链路
- 业务数据 → 垂域专家模型 → 高质量轨迹+Reward → 基模能力提升 → 更强冷启

依托OPD合版、数据合版方案，把各个垂域沉淀的业务经验回流给基础大模型，形成可循环、持续迭代变强的生产飞轮。
1. 单点业务落地产出垂域专属模型，沉淀真实交互轨迹与奖励数据；
2. 垂域优质数据反哺基座大模型，全面拔高基模综合能力；
3. 基座变强带来更优质的冷启动效果，让全新垂域的初次训练起点更高；
4. 循环往复，实现从零散垂直场景，逐步沉淀出通用模型能力。

通用底层模式
- 垂域小模型借助强化学习（RL）学习适配对应行业的工具调用链路，同时适配各类业务任务约束。

Agent落地分为Demo验证阶段与工业化生产阶段，二者核心诉求发生本质迁移：

Demo阶段重点验证**工具调用可行性**；生产落地阶段，核心转变为在长任务、多工具串联、多重约束的复杂业务环境下，保障任务执行稳定性。

| 挑战 | 落地表现 | 底层根因 |
| ---- | ---- | ---- |
| 成本不可控 | 每日Token消耗达到百亿级别，必须调用Plus/Max等高规格大模型 | 通用大模型能力冗余，存在能力过剩（overkill），多数简单子任务无需通用强能力，整体算力与token开销居高不下 |
| 效果天花板 | PE（Prompt Engineering，提示工程）优化后基准准确率稳定在70%左右，难以继续提升 | 通用模型缺少垂直业务场景的深度推理能力，复杂业务逻辑无法依靠提示词补齐 |
| 工具理解浅薄 | 频繁出现无效工具调用、参数编造幻觉、多工具间依赖顺序错乱 | 模型没有深度适配业务专属工具链，对工具功能、入参规范、调用先后逻辑认知不足 |

（1）当前最强模型在真实MCP场景仍不达标
- 最高值仍未接近生产可用的稳定性要求。


|评测基准|最高分|
| ---- | ---- |
|MCP-Mark|60.8|
|MCP-Atlas|76.4|

评测模型池
- Opus-4.6 / K2.6 / GLM-5.1
- DS-V4-Pro / Qwen3.6-Plus / Qwen3.7-Max

Benchmark证实：即使是最强闭源模型，在真实Agent场景也无法满足业务要求。

（2）Harness能补丁，但补不出上限

递进链路
- PE / Prompt优化 → Harness规则补丁 → 能力天花板 → 训练垂域Agent模型

业务场景现状

|场景|现状说明|
| ---- | ---- |
|出行场景|Skill选择、指令遵循等关键维度不足70%，纯PE无法弥补|
|电商场景|规则系统深度堆叠后到达极限，仍无法达标|

结论
- 必须通过垂类场景训练，回流到基模，根本性提升Agent模型能力。


（3）SFT 快速冷启 + Agentic RL 深度优化

① Stage 1：SFT 冷启
- 1周上线
- 统一造数：query / profile / workflow → trajectory → reject sampling
- 解决基模差异、QPS限制、标注成本
- 目标：快速拿到可用基线

② Stage 2：Agentic RL 自进化
- 持续迭代
- 模型自己出题、自己学习、自己评估
- 无需人工干预，持续超越SFT上限
- 目标：逼近甚至超越重度人工调优效果

Agentic RL 没那么容易，不是训个 GRPO 就能出效果（deepseek在数学+代码上用的很好，因为可验证），要很多细致工作
- rollout效率很低
  - 通用领域：loss 曲线平滑
  - 垂类领域：剧烈变化，不会就是不会
- point wise打分不稳定 → pair wise 打分更适合人工

**自进化框架**

让模型持续自进化的三个关键机制
1. （1）自动课程学习
  - 模型根据工具集自主生成训练Query
  - 训练数据全自动生产
2. （2）在线经验注入
  - RL过程中轻量注入高质量经验
  - 突破纯RL能力天花板
3. （3）Arena RL：Pairwise Reward
  - 相对比较替代绝对打分
  - 驱动稳定有效的RL训练

数据、经验、奖励信号三件事同时自动化，垂域Agent才能持续进化。

生成器-求解器协同进化闭环

流转链路：工具集观察 → 生成器出题 → 求解器解题 → 奖励反馈 → 同步进化

约束要点：
1. 工具锚定门：先观察真实工具输出，再撰写评分项
2. 格式门：确保生成任务可被解析执行
3. 难度塑形奖励：约一半rollout成功时取最大值

题目既不太简单，也不太难，始终贴合当前能力边界。

三轮协同进化效果

数据节点：0.470 → 0.599
- Base：0.470
- Round 1：0.512
- Round 2：0.561
- Round 3：0.599

ECR-Travel 三轮自进化

每轮生成器出的题更难，求解器解题更强。

> 全自动数据生产 + 难度自适应 = 模型持续自我超越

（2）在线经验注入

纯RL的核心瓶颈：好轨迹采不出来
1. 任务步长 40-50步
2. 解空间巨大
3. 随机探索 极低命中率

- 随机探索极难碰到高质量完整轨迹
- 没有好的正样本，RL优化方向不明
- 训练容易停滞在低效探索区间

类比：刚学下棋的人靠随机落子发现妙手，理论上可能，实际上极其低效。

怎么办？用批量轨迹的额外视野信息构建瞬态教师

流转链路：同一策略模型 → 正常Rollout → 瞬态教师轨迹 → 奖励门控 → Token级KL蒸馏

三大模块说明
1. 瞬态教师：不是外部大模型，而是同一模型+额外上下文信息。
2. 奖励门控：仅当教师轨迹reward > 原轨迹时激活，防止负迁移。
3. 分布保护：Token级反向KL正则，保持模型自身行为分布。

约72.1%训练组激活蒸馏，门控阻止近1/3负迁移

占比数据：
- 72.1% 激活蒸馏
- 27.9% 门控阻止

备注：教师轨迹更好时才注入经验

|方法|效果|
| ---- | ---- |
|纯RL|基线|
|RL + 无门控蒸馏|不稳定/可能退化|
|RL + RG-SED|稳定超越基线|

不是所有“额外信息”都有帮助，门控是关键。

（3）Arena RL

Pairwise 对比式强化学习：仅需定义比较规则即可驱动有效训练

Pointwise打分的致命问题：判别崩溃

训练早期
- 输出质量参差不齐
- 分数分布宽
- 梯度信号清晰

训练后期
- 输出质量趋同
- 分数压缩到窄区间
- 信噪比≈1.5，方向由噪声主导

根因：LLM-as-Judge 绝对打分天然不稳定；输出越接近，噪声越主导。

偏好比较的稳定性远高于数值估计
- 对比：“A比B好” VS “A得8.2分”

完整流程
- 同一query → 采样N条轨迹 → 锦标赛排名 → 按排名赋reward → 策略优化

核心优势
- 成对比较天然抗噪声
- 更容易捕捉细微差异
- 评判规则可解释、可复用

但计算量大

种子单败淘汰赛：O(N)成本达到O(N²)效果

|方法|比赛场数|效果|
| ---- | ---- | ---- |
|锚点法|7场|无法判定任意两条|
|循环赛|28场|信号最准、成本最贵|
|瑞士轮|12场|折中|
|种子单败淘汰赛|14场|效率最优|

执行流程
- τ₀锚点 → 其余各比一次 → 种子顺位 → 单败淘汰 → 完整排名

举例说明
- N=8时，锚点排序7场 + 单败淘汰7场，合计14场。整体复杂度线性，用O(N)开销逼近O(N²)全量两两对比的排序效果。



# 结束
