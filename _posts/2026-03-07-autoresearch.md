


# AutoResearch

autoresearch 专题详见飞书文档：[autoresearch](https://my.feishu.cn/wiki/TJXhwcj6wivSrLkdU9jc0Uren4f)


## 发展史

时间轴
- 2025 年 10 月：nanochat 项目发布（初始 commit 10 月 13 日）。
- 2026 年 1 月底：推出 “Time to GPT-2” leaderboard，初始记录约 3.04 小时。
- 2026 年 2 月：手动调优（数据集、FP8 等），基准降至约 2 小时。
- 2026 年 2 月 27 日：公开多代理实验尝试（8 agents，tmux 交互式），但当时未成功。
- 2026 年 3 月 5 日：首次宣布 AI 代理已自主迭代 nanochat（12 小时内完成 110 次改动，val loss 从 0.862415 降至 0.858039），称“I'll just leave this running for a while, go relax a bit and enjoy the feeling of post-agi”。并指出新 meta 是“what is the research org agent code that produces improvements on nanochat the fastest?”
- 2026 年 3 月 7 日：发布 autoresearch 极简仓库（单 GPU、单文件 ~630 行 train.py）。
- 2026 年 3 月 6–8 日：启动首次正式实验，在 depth=12 模型上运行约 2 天（~650–700 次实验）。
- 2026 年 3 月 8 日：初步确认改进可转移至 depth=24 模型。
- 2026 年 3 月 9 日：手动验证所有改动并测量最终结果。


### AutoResearch

【2026-3-15】[Autoresearch 深度解读：Karpathy 的"AI 自主科研"到底有没有戏？](https://zhuanlan.zhihu.com/p/2016489903790236699)

Karpathy 用 630 行代码搭"AI 研究员"的最小可行原型——让 Agent 在你睡觉时自动改代码、跑实验、筛结果，一晚上干完人类一周的活

一个"永不下班的实习生"——你给它一份研究方向的说明书（program.md），它就开始不停地改代码、跑实验、看结果、决定保留还是丢弃，然后继续下一轮。整个过程完全自主，不需要人类干预。

工作流是无限循环：

```sh
while True:
    1. 读取当前 train.py 和实验历史
    2. 形成改进假设（比如"把学习率调高试试"）
    3. 修改 train.py
    4. git commit（留痕）
    5. 运行训练（严格 5 分钟）
    6. 检查验证损失（val_bpb）
    7. if 改进 → 保留 commit，更新基线
       else → git reset，回退到上一个好的版本
    8. 记录结果到 results.tsv
    9. 继续下一轮
```

详见原文：[Autoresearch 深度解读：Karpathy 的"AI 自主科研"到底有没有戏？](https://zhuanlan.zhihu.com/p/2016489903790236699)

### 【2026-3-9】Hyperspace

【2026-3-9】[Hyperspace](https://agents.hyper.space/) 首个**分布式**通用人工智能（AGI）系统。
- 数千个自主 AI 智能体协同训练模型，通过点对点（P2P）闲聊协议共享实验成果，并在此推动技术突破。
- 完全点对点架构。可通过浏览器或命令行终端（CLI）接入参与。

- github项目 [hyperspaceai](https://github.com/hyperspaceai/agi)


### 【2026-5-19】AutoResearchClaw

【2026-5-19】北卡罗来纳大学 推出 AutoResearchClaw 多智能体自动研究框架
- [AutoResearchClaw: Self-Reinforcing Autonomous Research with Human-AI Collaboration](https://arxiv.org/pdf/2605.20025v1)
- Github: [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw)

AutoResearchClaw 突破现有系统线性流程局限的多智能体自主研究系统。

AutoResearchClaw 把输入端直接拉到“一个原始研究想法”。
- 用户只需在命令行输入一行 CLI 命令，附上 idea，比如“探索新型注意力机制在长上下文建模中的效率”
- 系统就会启动一个 23 阶段的端到端流水线，覆盖 8 个主要阶段：从 idea scoping、文献发现、合成，到实验设计、执行、分析、写作和最终定稿。

五大机制：
- 结构化多智能体辩论用于假设生成与分析；
- 具备自修复能力的执行器可将失败转化为信息；
- 可验证的结果报告防止数据伪造与引用幻觉；
- 提供从全自动到逐步监督的七种人机协作模式；
- 以及能将过往经验转化为未来保障的跨运行进化能力。

实验表明，该系统性能显著优于基线模型，且精准、定向的人机协作模式始终优于完全自主或穷举式监督。它被定位为一种增强而非取代人类科研判断力的研究放大器。



# 结束

