---
layout: post
title:  通用智能体 Agent
date:   2025-07-20 12:00:00
categories: 大模型
tags: LLM agent 智能体 manus genspark langchain
excerpt: 通用智能体专题
mathjax: true
permalink: /general_agent
---

* content
{:toc}


# 通用智能体


2025年3月，号称全球第一款通用 Agent 产品的 `Manus` 爆火出圈，当时整个互联网圈子一"码"难求的场面让人印象深刻
- 演示视频中，Agent一步步逐级拆解并自动完成任务, 令业内外惊呼“未来已来”，更是把 2025 年推上“Agent 元年”的浪潮顶峰
- 随后市面上又出现了很多 Agent 概念产品，一时之间好不热闹。



## 总结



### 功能

【2025-6-3】[4大通用智能体（manus、genspark、skywork、扣子空间）复杂任务PK报告](https://zhuanlan.zhihu.com/p/1913273897475901249)

没有任何一个智能体一次完成任务，都是通过多轮对话引导和反复调校才最终完成了任务。
- 现阶段“AI工具人”还离不开“指挥官”，学会与AI进行有效的人机协作，共同完成复杂工作，是一项至关重要的能力。

|产品|时间|公司|优点|缺点|分析|其他|
|----|----|----|----|----|----|----|
|`Manus`|2025-3-5|Monica|埋头苦干,提交的内容多|效率一般,审美有待提供|勤奋朴实的技术实习生||
|`Genspark Super Agent`|2025-4-2|MainFunc|基础扎实,信息搜索/ppt生成/图标|基于交差,规划不足,深度不够|能力强但小聪明的员工||
|`Skywork Super Agent`|2025-5-22|天工|能力均衡,资料收集,报告整理,可视化|缺乏特长|表现亮眼的新人,潜力股||
|`Coze Space`|2025-4-19|字节||不理想,可能是国内LLM能力限制|差强人意||
|`Minimax Agent`|2025-6-19||||||

![](https://pic3.zhimg.com/v2-7c0b4147cfc719942c098aa283e913b8_1440w.jpg)


|维度|Manus|Genspark|Skywork|扣子空间 (Coze Space)|
| ---- | ---- | ---- | ---- | ---- |
|1. 全面性与覆盖度|优秀|良好|优秀|良好|
|2. 分析洞察的深度与准确性|良好|良好|优秀|中等|
|3. 建议的针对性与可操作性|优秀|优秀|优秀|中等|
|4. 报告结构、清晰度与易用性|良好|优秀|优秀|中等|
|5. 新兴趋势与机会洞察|优秀|良好|良好|优秀|
|6. (可选) 智能体交互与效率|中等|良好|良好|良好 (搜索量大)|
|综合评价|良好|良好|优秀|中等| 

【2025-6-13】[Manus、Genspark、Coze空间、Minimax横评，谁是最强Agent？](https://zhuanlan.zhihu.com/p/1916812614463382819)

测试结论：
- ① 当前参测 Agent 产品均未达到完全可用状态(测试平均分 1.23~2.20，仅处于部分可用状态，距离直接可用状态对应的3分仍有距离）。
- ② 整体梯队对比：Manus（高投入）>Manus（标准）= Minimax（深度） > Genspark > Coze空间（探索）（平均得分 2.20/1.89/1.89/1.65/1.23分）。
- ③ Manus（高投入）更全面和稳定，在环评产品中表现最优；Manus（标准）不及Manus（高投入），但整体表现均衡。
- ④ Minimax（深度）擅长信息检索、软件开发、文件和数据处理类任务，在交付网页等Coding场景中表现突出，但 PDF 输出的稳定性不足。
- ⑤ Genspark擅长信息检索、软件开发类任务，但支持的输入类型有限，不支持监控反馈类任务，并且GUI交互表现较弱。
- ⑥ Coze空间（探索）相比之下明显掉队。

![](https://pic1.zhimg.com/v2-611e40f3b2c903bc5c92ef364ab1ac6a_1440w.jpg)


### 费用

【2025-6-28】AutoAgent 总结

|智能体名称|特点|收费模式|优点|缺点|
| ---- | ---- | ---- | ---- | ---- |
|Manus| - |每天有免费额度，300 积分≈1 次任务|有日常免费使用机会，能满足基础低频使用|免费积分对应任务量少，高频使用需额外获取积分| 
|天工超级智能体| - |每日有免费额度，1500 积分≈2 次任务|免费额度相对较多，可支撑稍高频任务尝试|任务消耗积分多，长期高频用，积分获取可能成负担| 
|扣子空间|虚拟电脑执行任务|免费|零成本使用，借助虚拟电脑执行任务场景有特色|功能、性能等可能受限于免费属性，任务复杂度、效率或有上限| 
|Flowith| - |收费，近期有优惠，仍需 14 刀/月|优惠期成本稍降，付费后功能、服务或更稳定优质|需持续付费，成本相对高，优惠结束后费用压力大| 
|Minimax 智能体| - |最近开始收费，19 刀/月|新收费阶段，功能迭代、服务质量或有提升|收费标准较高，对于预算有限用户不友好，且新收费模式下体验待验证| 
|Genspark| - |每日有免费额度，200 积分≈1 次任务|日常有免费使用机会，可尝试基础功能|免费积分对应任务量少，高频使用需补充积分| 
|智谱清言沉思|控制浏览完成任务|免费|无需付费，控制浏览模式有独特交互体验|功能实现依赖特定浏览控制方式，使用场景、操作自由度或受限| 
|纳米超级搜索| - |每日有免费额度，每天 10 次免费任务|免费任务次数多，能满足高频基础搜索类任务|任务类型可能较单一，仅围绕搜索，功能丰富度或不足| 




## 案例



### 【2025-3-5】Manus

Manus：号称是全球首款通用 AI Agent 产品，由 Monica 团队开发。它能独立思考、规划和执行任务，在多个领域有广泛应用，可分解复杂任务，调用外部工具，还具备自主学习能力，能根据用户反馈优化，在 GAIA 测试中成绩优异。Manus 分为标准模式与高投入模式，高耗模式使用更长的链式思维推理，并进行更详细的任务分解，但需要更多的处理时间并消耗更多积分。目前为测试阶段，仅对 Manus Pro 用户开放。

资讯
- 【2025-3-6】[AI Agent的“GPT时刻”，Manus炸醒整个AI圈](https://tech.ifeng.com/c/8hUaacvUjTK)

北京的人工智能公司`蝴蝶科技`，创始人来自华中科技大学的90后毕业生`肖弘`

【2025-3-5】 Monica.im 研发的全球首款 AI Agent 产品「Manus」
- [Manus](https://manus.im/)，名字取自拉丁语中的“手”，寓意着将思想转化为行动。
- [Manus](https://manus.im/) 不仅仅是一个 AI，更是一个能帮你完成实际任务的**通用型 Agent**。无论是工作还是生活，Manus 都能成为你的得力助手
- GAIA 基准测试中取得了 SOTA（State-of-the-Art），远远甩开了 OpenAI。在解决现实世界问题方面表现卓越。

#### 功能

「Manus」是一个真正自主的 AI 代理，能够解决各类复杂多变的任务。与传统 AI 助手不同，Manus 不仅能提供建议或答案，还能直接交付完整的任务成果。

[Manus](https://manus.im/) 是 中国团队打造的**全球首款**真正意义上的“通用型 Agent”
- **通用性**是关键： 与只能执行特定任务的 AI 不同，Manus 具备处理**多种任务**能力。 可以深度股票分析、制作个性化旅行手册、为教师创建视频演示材料等等。想象一下，你只需要告诉 Manus 你的需求，它就能帮你搞定一切！
- 不止于思考，更在于**行动**： Manus 不仅仅停留在“思考”层面，它能将想法付诸实践，真正解决问题。为什么？因为它后面真的是电脑……

Siri 可以设置闹钟，但没法规划一天的行程、更不能帮你处理复杂的商业谈判。

但 Manus 就像一个 拥有超强学习能力和适应性的“数字大脑”，不再局限于单一任务，而是能够 理解复杂指令、自主学习、跨领域协同，真正像人一样思考和行动！

GAIA 基准测试中取得了 SOTA（State-of-the-Art），远远甩开了 OpenAI。在解决现实世界问题方面表现卓越。
- ![](https://pic1.zhimg.com/v2-0b20e29987d79349efaa0b8e61ec93cc_1440w.jpg)
- GAIA 是评估通用 AI 助手解决现实世界问题能力的基准。
- Manus 在这个测试的所有三个难度级别上都表现出色。

#### 应用

示例
- 旅行规划：不仅整合旅行信息，还为用户创建定制旅行手册。例如，为用户规划日本四月旅行，提供个性化的旅行建议和详细手册。
- 股票分析：进行深入的股票分析，设计视觉上吸引人的仪表盘展示全面的股票洞察。例如，对特斯拉股票进行深度分析，创建可视化仪表盘。
- 教育内容创建：为中学教师创建视频演示材料，解释动量定理等复杂概念，帮助教师更有效地教学。
- 保险政策比较：创建清晰的保险政策比较表，提供最佳决策建议，帮助用户选择最适合的保险产品。
- 供应商采购：在整个网络中进行深入研究，找到最适合用户需求的供应商，作为真正公平的代理为用户服务。
- 财务报告分析：通过研究和数据分析捕捉市场对特定公司（如亚马逊）的情绪变化，提供过去四个季度的市场情绪分析。
- 创业公司列表整理：访问相关网站识别符合条件的公司，并将其整理成表格。例如，整理 YC W25 批次的所有 B2B 公司列表。
- 在线商店运营分析：分析亚马逊商店销售数据，提供可操作的洞察、详细可视化和定制策略，帮助提升销售业绩。
- 当 Agent 通过一长串思维链和工具调用，最终输出一个无比完整、专业的结果时，用户们开始感叹「真的能帮人类做事了」。

Manus 更想做的，是你在数字世界中，字面意义上的「代理人」。而它做到了。

#### 原理


Manus到底有啥“黑科技”？

【2025-3-7】[本以为DeepSeek天下无敌了，没想到Manus更猛](https://mp.weixin.qq.com/s/VncWbfZYUti5-S_X_dlbcw)

设计思路相当巧妙，融合了好多厉害的技术。

核心架构: `按键精灵`+`DeepSeek推理`+`虚拟机`+`Claude`
- **按键精灵**思路：用过按键精灵的小伙伴都知道，它能模拟鼠标点击，实现电脑操作自动化，以前在站长圈可火了。Manus借鉴了这个思路，用脚本控制电脑和手机处理各种工作。以前制作脚本特别麻烦，普通人根本搞不定，Manus却把这个难题轻松解决了。
- **DeepSeek 推理**能力：DeepSeek理解人类问题的能力超强，Manus借助它，能精准领会你的意图，给出超靠谱的回应。
- **虚拟机**技术：Manus通过在服务器里装各种虚拟机，模拟不同软件的运行环境，不管你要用啥软件，它都能轻松应对。
- **生成模型**：Manus采用美国Anthropic公司的Claude 3.5版本作为生成模型，保证输出的内容又专业又优质。


Manus 工作原理

与 Deep Research 单纯**文本报告**生成不同，Manus 通过外接多种工具，实现输出形式的**多样化**。
- 同样遵循 “`计划` → `执行` → `结果合成`”流程，但第二步除了联网搜索，还执行了更多复杂任务。

主要技术环节包括：
- `Planner`: 和 Deep Research 不同，收到用户请求后不再单纯生成一个报告章节，而是拆成多个任务，每个任务还会有更细致的子任务。
- `Steiner` 模型: 计划阶段，猜想用了 Steiner 模型，由 Manus 的开发者`季逸超`基于 `qwen2.5-32b` 模型开发的一款擅长"长期思考"（long horizon thinking）和"逐步执行"（step-by-step execution）模型，这个模型主要是启发自 `o1`.
- `MCP Server`: MCP Server 是 Anthropic 提出, 模型外接其他工具或者能力的协议，判断每一个子任务应该用什么 Agent 来完成。
- `Search Agent`/`Compute use`（Browser-use）: Search Agent 主要用搜索互联网的信息，跟 Deep Research 单纯的调用搜索 API 不一样，用了 Compute use，设计之初是来让 AI 控制整个电脑的交互，但这里只用到了**浏览器交互**的功能 -- 所以离“通用” Agent 还有一段距离
- `Coding Agent`/Doc Agent: 负责写代码和文档的基本处理，coding 能力用 Claude 基座模型。
- `Deploy Agent` Manus: 让生成结果部署在一个云服务器上，用到 Artifact 概念, 把生成的网页代码运行在浏览器上。
- `Linux Shell Executor` Manus: 用到 Linux Sandbox 技术，远端生成迷你 Linux 环境，用 AI 生成命名行来控制这个 Linux 环境，所以很多生成的文档代码文件都在文件系统里。
- `Self-build Tools`: 由于预定义工具非常有限，但又要实现更多的输出选项，那怎么办？所以 Manus 让 LLM 临时生成一些用于完成该任务的工具



#### 评论

Manus 背后的公司 —— [Monica.im]()，其实是个“缝合怪”高手。

Manus 核心能力 = `Compute Use` + `虚拟机` + `Artifacts` + 内置多个 `Agent`，更像是一个**高度整合**的 **AI 工作流工具**，而<span style='color:red'>非真正的通用 AI Agent</span>。

Manus 传播堪称移动互联网的经典模版复现：饥饿营销 + KOL尖叫体测评 + 借势明星产品
- 邀请码**饥饿营销**（“动用我的人脉才搞到”）
- **KOL尖叫体测评**（“人类一败涂地”“浑身发麻”）
- 借势**明星产品**（这次是绑定 DeepSeek）。

然而当人们打开海外科技论坛和社交媒体，关于 Manus 的讨论却近乎真空。

[复盘一下这波 Manus 中的营销方法](https://zhuanlan.zhihu.com/p/28726052540)
- 3月5日晚上10点, 最早在 X 上发布视频，介绍产品
  - 宣传时间选在周三和周四，视频形式发布，是业界惯例
  - 第一个通用 AI 智能体，并演示几个示例，通用 AI 智能体是产品的终极目标，但视频让人感觉第一个完成了终极目标的产品。
- 当天晚上大家都睡了，真正出现高潮是在第二天早上。
- 3月6日，早上6点开始，出现大量媒体文章
  - 经验: 宣传文章一定要在早上8点前发，而且一起发，大家一觉醒来变天了，全世界都在提，这个初始动能会吸引更多媒体，得到更大的关注，甚至还有官媒赶在当天下班前发了
  - 蹭流量: **爱国**和 **DeepSeek**
    - 热词: AI Agent, AGI, 感叹号, 家国情怀
  - 邀请码: 人为制造的稀缺性也是营销成功的原因之一

|时间|地点|自媒体|标题|分析|
|---|---|---|---|---|
|0点|浙江|`泛函`|真正的通用 Al Agent 来了!是中国团队做的!我们离 AGI 不远了!|标题夸张，没啥反响|
|6:03|北京|`数字生命卡兹克`|一手体验首款通用Agent产品Manus-唯有惊叹。|这么早就起来了？|
|6:07|广东|`APPSO`|这个中国 AI 产品一夜刷屏!全网都在要邀请码，可能是 DeepSeek 后最大惊喜|全网都在找邀请码？|
|6:25|北京|`极客公园`|Al Agent 的「GPT 时刻」，Manus 炸醒整个 AI 圏!|依然浮夸|
|7:06|北京|`赛博禅心`|实测 Manus:首个真干活 A，中国造(附50个用例 +拆解)||
|17:06|北京|`央视网`|一夜之间火爆全网!又一个中国AI产品刷屏|央媒也憋不住了|
||||||


Andrej Karpathy 在2023微软Bulid大会上做了个主题分享：[State of GPT]()，提到 Prompt的重要性：
- Prompt 弥补了**人类大脑**和**LLM大脑**认知架构的差异　

人类要用**自然语言**进行编程, 也需要深入理解模型的行为和反应　

Artifacts 是 Claude 模型能力的很好的外化表现形式
> 光靠Prompt优化，模型输出，Artifacts，都不能输出很漂亮的内容，一定是这三者的结合

Claude 官方发布的视频《How we built Artifacts with Claude》
- 直接在 Claude 内输入Prompt，合适的条件下，Artifacts 直接渲染出效果供你检查

【2025-3-10】提示词泄露
- github [jlia0](https://gist.github.com/jlia0/db0a9695b3ca7609c9b1a08dcbf872c9) 包含提示词、工具列表
- 29个工具
  - 浏览器: 12个, 浏览、导航、重启、点击、输入、移动鼠标、按键、选择、上划、下划
  - 文件操作: 5个, 读文件、写文件、字符串替换、内容查找、按名字查找
  - Sehll命令: 5个, 执行、查看、等待、写入进程、杀死进程
  - 部署: 2个, 部署端口、部署应用
  - 等待: 1个, 任务完成,开始等待
  - 搜索: 1个, Web搜索
  - 创建: 1个, 创建 Manus 页面



#### OpenManus

【2025-3-7】[OpenManus：MetaGPT推出的开源版Manus](https://www.aisharenet.com/openmanus/)


开源项目 OpenManus ，帮用户通过简单配置在本地运行智能体，实现各种创意想法。
- MetaGPT 社区成员 @mannaandpoem、@XiangJinyu、@MoshiQAQ 和 @didiforgithub 在短短 **3 小时内**开发完成，他们还开发了自动化编程项目 MGX 。
- 相比需要邀请码的 Manus，`OpenManus` 无需任何准入门槛，用户只需克隆代码、配置 LLM API 即可快速上手。

核心目标：
- 通过复刻`MCP`（模型上下文协议）和`虚拟机`操作环境，在代理和模型层面提高AI调用和执行操作的准确率。

功能列表
- **本地**智能体运行：终端输入任务，利用配置的 LLM API 在本地执行自动化操作。
- 支持**主流 LLM 模型**：默认集成 GPT-4o，用户可根据需要调整模型配置。
- **一键启动**：运行 `python main.py` 即可快速进入任务输入模式。
- 实验性版本：提供 `python run_flow.py` 用于测试开发中的新功能。
- 社区协作：支持通过 GitHub 提交问题或代码，参与项目开发。

安装

```sh
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
# pip install -r requirements.txt
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 更新配置
cp config/config.example.toml config/config.toml
```

代码分析
- 【2025-3-11】[如何评价OpenManus这个开源项目？](https://www.zhihu.com/question/14322364598/answer/120275203788)

图解: [如何评价OpenManus这个开源项目？ - 流水无情的回答](https://www.zhihu.com/question/14322364598/answer/120275203788)
- ![工作流程](https://pic1.zhimg.com/80/v2-c446c513b2afeeda8d282083b8cbfadc_720w.webp?source=2c26e567)
- ![](https://picx.zhimg.com/80/v2-49e5eeb62f7a23ea86e69750a1e6714d_720w.webp?source=2c26e567)
- ![执行流程](https://picx.zhimg.com/80/v2-8c2ef568bde90525bd46c074421d8ea2_720w.webp?source=2c26e567)

#### OWL

【2025-3-7】[OWL：0天复刻Manus通用智能体，完全开源！GAIA Benchmark最强性能](https://mp.weixin.qq.com/s/0AWaSNynyjjY5TpdtKN-3w)


🦉[OWL](https://github.com/camel-ai/owl) 项目直接做到开源界GAIA性能天花板，达到了57.7%，超越Huggingface 提出的Open Deep Research 55.15%的表现。
- 项目地址：GitHub：[owl](https://github.com/camel-ai/owl) 不但免费白嫖，还能参与贡献

Demo 示例
- 自动查找当日伦敦电影有什么！
- 调研总结GitHub仓库里都有什么

Manus核心工作流拆成6步 
- 启动一个Ubuntu容器（Agent远程工位就位）
- 知识召回（把之前学过的内容捡起来用）
- 连接数据源（数据库、网盘、云存储全覆盖）
- 把数据挂载到Ubuntu（Agent的搬砖时刻）
- 自动生成todo.md（规划任务+写待办清单）
- Ubuntu工具链+外接工具组合拳，执行全流程任务🔗

工具集
- 终端命令执行（运维、部署全搞定）
- 文件解析：PDF转Markdown、网页爬取
- 自动创建、编辑文件，生成todo.md
- 浏览器操作：滚动、点击、输入全会
- 在线搜索+实时信息检索，一秒找到关键资料自动生成报告、代码、文档，直接交付成果
- 一键把服务部署到公网，输出报告直接上线

Memory Toolkit：复刻还得加点记忆buff 
- 每次任务执行，Manus 都会把新学到的知识点存下来。
- 给🦉加上记仇功能（哦不，是记忆）。下次遇到类似任务，直接召回过往经验！
- 新知识实时存储，持续进化任务中
- 随时召回过往经验，灵活调度

🔗 相关 Memory模块（已开源）：
- [agent_memories.py](https://github.com/camel-ai/camel/blob/master/camel/memories/agent_memories.py)

🦀️CRAB+🦉OWL：跨平台掌控力直接拉满 
- 早在Manus爆火之前，其实已经开发过一套强大的**跨平台操作系统**的通用智能体——`CRAB`。🔗[crabCRAB](https://github.com/camel-ai/crabCRAB) , 操控Ubuntu容器，还能控制手机和电脑里任何应用，覆盖比Manus展示的终端和浏览器多得多。

复刻计划
- Worklfow: [issue](https://github.com/camel-ai/camel/issues/1723)
- Ubuntu Toolkit: [Issue](https://github.com/camel-ai/camel/issues/1724)
- Memory Toolkit [Issue](https://github.com/camel-ai/camel/issues/1725) 




### 【2025-4-19】Coze Space


2025年4月19日，字节跳动正式发布AI智能体平台“扣子空间”（Coze Space），定位为“与AI Agent协同办公的最佳场所”。 
- 字节精心打造的 AI Bot 开发旗舰平台，致力于赋能开发者，在智能体编排工具成熟度、插件广泛性、兼容大模型种类多样性以及发布渠道全面覆盖等方面均展现出非凡实力。

该产品对标全球爆款AI Agent工具Manus，通过整合大模型能力、自动化工具链和开放生态，实现从需求输入到成果输出的全流程自动化。
- 国内 [扣子空间](https://space.coze.cn/)

定位
- AI协同办公平台： 扣子空间的核心定位是一个面向AI Agent的协同办公平台，用户可以与AI Agent共同协作完成工作。
- 提升效率： 平台致力于提升用户与AI Agent的协作效率，帮助用户更快速、更便捷地处理复杂任务。
- 从问题到解决方案： 扣子空间的目标是让AI Agent不仅能回答问题，更能通过一系列操作帮助用户解决实际问题。

#### 功能


智能任务分解与执行：
- 扣子空间能够智能分析用户的自然语言需求，并将其自动拆解为多个具体的子任务。
- 平台能自主调用多种工具执行任务，例如浏览器、代码编辑器等，并最终输出完整的成果报告，形式可以是网页、PPT、飞书文档等。这实现了任务全流程的自动化。

双模式协作系统：
- 平台提供“探索模式”和“规划模式”两种不同的工作模式，用户可以根据任务的复杂性和需求选择。
- 探索模式： AI自主进行动态探索，响应速度较快，适用于时效性要求高的任务。
- 规划模式： AI会进行深度思考和规划，适合处理高复杂度的任务。在规划模式下，AI会先给出任务处理计划，并适时与用户确认和对齐，用户也可以在关键步骤进行修正，提高了协作的灵活性和准确性。

丰富的Agent生态和专家Agent：
- 扣子空间内置了专家级Agent生态，首期提供了不同领域的专业AI助手。
- 这使得AI Agent更加专业化，能为用户提供更具深度的服务。

开放的工具生态与MCP扩展集成：
- 平台集成了MCP（Model Context Protocol，模型上下文协议）扩展体系，可以无缝连接和调用外部服务和工具。
- 首批官方支持飞书多维表格、高德地图、图像工具、语音合成等高频办公组件。
- 未来还将支持用户通过“扣子开发平台”将自定义的MCP发布至扣子空间，持续拓展Agent的能力边界，打破不同系统和工具之间的壁垒。


### 【2025-4-2】Genspark Super Agent

Genspark 是 MainFunc 推出的 AI Agent 产品。
- 以自研 Super Agent 引擎为基础，采用多智能体协同架构，能理解用户意图，自主规划执行任务。其产品矩阵丰富，通过生成 Sparkpages 提供优质搜索体验。

2025年4月2日，Genspark 推出通用 Super Agent，官方宣称超越Manus
- [体验地址](https://www.genspark.ai/) —— 国内无法访问
- 无法验证码，有一定免费积分

背景：
- Genspark 是前百度小度的 CEO 景鲲和 CTO 朱凯华创业推出的 Agent 产品

差异化功能：(与manus相比)
1. 更丰富的 Tool Use 能力，比如让 AI 打电话和视频生成
2. Agent 规划和执行的速度更快，因为没用Browser Use、Computer Use

评测：
- Genspark 在GAIA Benchmark 上超越 Manus。

然而，Manus 合伙人、产品经理 hidecloud表示质疑🧐


信息源：
- [超越 Manus？华人创业产品 Genspark 推出通用 Agent（附实测效果）](https://mp.weixin.qq.com/s/S2NCd3ySZyaRtjwC6BSG6Q)



### 【2025-5-22】Skywork Super Agent

2025年5月22日, 天工发布 Skywork Super Agents 
- 所有用户都可以直接注册，不需要什么邀请码就能马上体验。
- 初期版本就已经支持英语和日语，看来是铁了心要走向国际。

体验
- [国际版](https://skywork.ai/home)
- [国内版](https://www.tiangong.cn)

#### 原理

Skywork Super Agents 没有走传统AI工具“大而全但不够精”的老路，而是采用了“5个专家智能体 + 1个通用智能体”的垂直专业化架构。

这种设计理念，就是想为特定的任务提供深度优化的解决方案，而不是只给一些浅尝辄止的通用功能。

五大专家智能体：
- 文档智能体 (Docs Agent)：专攻各种专业文档、报告和写作任务。
- 幻灯片智能体 (Slides Agent)：帮你快速创建结构清晰、颜值在线的演示文稿。
- 表格智能体 (Sheets Agent)：数据分析、表格处理、图表生成，统统不在话下。
- 播客智能体 (Podcasts Agent)：能把文字内容变成高质量的播客音频，解放你的双眼。
- 网页智能体 (Webpages Agent)：快速搭建专业、可交互的网站页面，小白也能上手。

![](https://pic4.zhimg.com/v2-aa60b631d655d8740aceb912fdc00c87_1440w.jpg)

#### 效果

GAIA (General AI Agent benchmark) 基准测试中，Skywork **深度研究**智能体框架拿下了82.42的高分（截至2025年5月10日），把 OpenAI Deep Research 和 Manus 这些竞争对手都甩在了身后，排到了全球第一。




### 【2025-6-19】Minimax Agent

【2025-6-19】Minimax（深度）：[MiniMax Agent](https://www.minimaxi.com/news/minimax-agent) 是 MiniMax 公司研发的一款 AI 智能助手，基于深度学习与自然语言处理等核心技术，融合先进的算法优化和大规模数据训练，为用户提供多种功能。

专为解决长期复杂任务设计的智能代理，具备专家级的多步骤规划能力、灵活的任务分解机制以及端到端的执行效率

能完成长程（Long Horizon）复杂任务的通用智能体，也就是能多步规划出专家级解决方案、能灵活拆解任务需求、并能执行多个子任务从而交付最终结果。
- 体验地址 [MiniMax Agent](https://agent.minimax.io/)


### 【2025-7-24】JoyAgent-JDGenie

【2025-7-24】[京东开源轻量化通用Agent产品 jdgenie，开箱即用！二次开发及踩坑指南](https://mp.weixin.qq.com/s/RYymGzJpsbar4d9y83ijHg)

京东开源的端到端多智能体系统（Multi-Agent System） JoyAgent-JDGenie。

与传统仅提供SDK或框架的智能体方案不同，它定位为**产品级**的多智能体协同系统，**开箱即用**且支持**轻量化本地**部署 。

用户只需输入自然语言的任务描述，系统就能自动组织多个子智能体协同工作并输出结果（如分析报告、代码片段或PPT文档），打通从任务输入到结果输出的“最后一公里” 。你可以在其基础上进行二次开发与扩展，形成自己的定制化智能体产品。

主要组成如下：
- 前端交互层（UI ）：基于 React 实现的人机交互界面，支持用户输入自然语言请求，并实时展示任务过程与结果 。用户可以通过网页直接与智能体系统对话，获取报告、答案等输出。
- 后端智能体层（Backend）：Java构建，负责接收前端请求、调用多智能体引擎以及整合使用后端的各类工具，并协调处理工具与各智能体的响应。
- 工具层（Tools）：用来给智能体提供各种工具。在本项目中工具层统一以FastAPI的方式提供，可以通过FastAPI的docs查看工具列表和规格。工具分两种：
  - 本地工具：目前预置code（写代码）、deepsearch（深度搜索）、report（报告）、file（文件管理）等，涵盖了从文本处理、信息检索到格式化输出的常见需要。
  - MCP工具：支持连接到配置好的MCP Servers，加载其开放的工具；并仍然以FastAPI方式公开给智能体层使用。（Agent不直接访问MCP Server）

要点
- 每个Agent配备必要的工具（Tools），比如规划、文件管理、搜索、报告、编码。
- 支持直接的ReAct （边想边做）和 Plan-and-Executor（想好再做）的智能体工作范式；事实上两者也是协作的：规划（Plan）的某个任务步骤在执行（Execute）时可能又是ReAct的模式。
- 所有Agent共享上下文，包括Memory（任务历史）、Files（中间文件结果）、Tools（工具）、Config（配置）等；任务与工具支持并发方式执行，以最大化智能体的能力并提高响应性能。

```sh
# 克隆项目代码： java + node.js
git clone https://github.com/jd-opensource/joyagent-jdgenie.git
cd joyagent-jdgenie
```

### 【2025-8-6】Chain-of-Agents


【2025-8-23】[Chain-of-Agents: OPPO推出通用智能体模型新范式，多榜单SOTA，模型代码数据全开源](https://mp.weixin.qq.com/s/G3IhYP8M9vyihExVoKlh2A)
- 【2025-8-6】[Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL](https://www.arxiv.org/abs/2508.13167)
- 主页：[project](https://chain-of-agents-afm.github.io/)
- 代码：[Agent_Foundation_Models](https://github.com/OPPO-PersonalAI/Agent_Foundation_Models)
- 模型：[afm-models-689200e11d0b21a67c015ba8](https://huggingface.co/collections/PersonalAILab/afm-models-689200e11d0b21a67c015ba8)
- 数据：[afm-datasets-6892140eaad360ea5ccdcde1](https://huggingface.co/collections/PersonalAILab/afm-datasets-6892140eaad360ea5ccdcde1)

现阶段 MAS 依然面临一些关键限制：
- 计算开销高：智能体之间频繁冗余的通信和复杂的工作流设计导致效率不高。
- 泛化能力有限：面对新领域或新任务时，需要大量的 prompt 设计与工作流配置。
- 缺乏数据驱动的学习能力：难以通过智能体任务数据实现持续提升性能。
- 底层的大语言模型（LLMs）未原生支持多轮、多智能体、多工具交互，仍依赖 prompt 工程实现。

近期兴起的**工具融合推理**（TIR）模型，通过显式地将工具使用融入推理过程，显著提升了单智能体框架（如 ReAct）在信息检索任务中的表现。然而，传统的 TIR 模型，无法直接支持**多智能体系统**的原生训练与协作。

VIVO 提出全新的智能体推理范式——Chain-of-Agents（CoA）。
- 与传统的 TIR 模型仅支持单一智能体的「思考-行动-观察」模式不同，CoA 框架能够灵活定义多个角色和工具的智能体，在单一模型内动态激活，实现端到端的多智能体协作。

CoA 无需复杂的 prompt 和工作流设计，降低了智能体间的通信开销，并支持端到端训练，显著提升了系统的效率和泛化能力。

经过训练后，具备原生 CoA 问题求解能力的模型称为 Agent Foundation Model（AFM）。

#### 原理

CoA 采用了一种层次化的智能体架构，包括两个核心组成部分：
- 角色型智能体（Role-playing Agents）：进行推理和协调的智能体，包括：思考智能体（Thinking Agent）、计划智能体（Plan Agent）、反思智能体（Reflection Agent）和验证智能体（Verification Agent）。
- 工具型智能体（Tool Agents）：执行特定任务的智能体，包括：搜索智能体（Search Agent）、爬取智能体（Crawl Agent）和代码智能体（Code Agent）。

CoA 范式下，模型可以支持更多类型的智能体的推理和调用。

CoA 微调框架，用于构建 AFM，该方法具体包括以下流程：
- 任务数据采集，生成与筛选：从公开数据集中采集不同类型的任务数据，以及采用自动化的方式（如 TaskCraft）自动生成高质量智能体任务，并进行有效过滤。
- 多智能体能力蒸馏：利用先进的多智能体框架（如 OAgents）完成任务，将成功轨迹转换为 CoA 兼容的形式。
- 监督微调与强化学习：利用生成的 CoA 轨迹进行模型微调，并通过可验证的智能体任务进行强化学习，进一步提升性能。

#### 效果

AFM 展示了卓越的性能和高效的推理能力，在近 20 项复杂任务和基准测试中全面刷新记录：
- 在 Agentic 任务中，其在 GAIA 基准上以 32B 模型实现了 55.4% 的 Pass@1 成功率；
- 在代码推理方面，AFM 在 LiveCodeBench v5 上的 47.9% 准确率和在 CodeContests 上的 32.7% 成绩均显著超越现有 TIR 方法。
- 同时，它将推理成本（token 消耗）减少高达 85.5%，在保持领先性能的同时大幅提升效率。

### 【2025-7-30】Deep Agents

【2025-7-30】LangChain AI开发 Python 工具包 Deep Agents.

详见站内专题：[LangChain学习笔记](langchain)



# 结束

