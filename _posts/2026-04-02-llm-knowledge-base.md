---
layout: post
title:  大模型知识库构建
date:   2026-04-02 19:10:00
categories: 大模型
tags: 知识库 知识图谱 rag ak47
excerpt: 大模型如何构建个人知识库？
mathjax: true
permalink: /llm_kgbase
---

* content
{:toc}

# 大模型知识库

## RAG 问题

传统 RAG 本质是“临时查资料”工具：
- 要么依赖**关键词匹配**，容易漏掉真正语义相关的内容；
- 要么只靠**向量相似度**，又常常抓不住精准的规则和关键字段。

况且，只是把零散的文本片段临时拼进上下文，既没有形成**结构化**的知识沉淀，也没有留下**可追溯**的证据链。

Agent 每次都像“临时翻书”，而不是真正把知识“记住”。

再加上向量检索本身的不稳定、上下文窗口的硬性限制、历史信息无法长期累积。

Agent用得越久，反而越乱，始终停留在“一次性工具”的阶段。


## 【2026-4-2】Andrej Karpathy

2026年4月2日，著名AI研究员、前 OpenAI/Tesla 科学家 Andrej Karpathy 在其博客发布了一篇关于"/raw文件夹"的文章，末尾留下了一句意味深长的话：“我认为这里存在一款令人惊叹的全新产品的空间。”

Karpathy 在AI领域的影响力毋庸置疑——他曾担任OpenAI联合创始人、Tesla AI总监，其公开发言和文章往往能在技术社区产生巨大的示范效应。这次，一句"产品空间已经存在"，直接催生了一个开源项目，并在两天内跻身热门仓库之列

【2026-4-3】[Andrej Karpathy X上分享用LLM搭建个人知识库](https://x.com/karpathy/status/2039805659525644595)
- 使用 LLM 构建个人知识库，涵盖各种研究兴趣主题。通过这种方式，我近期大部分的 token 处理量不再用于代码操作，而是用于知识操作（知识以 markdown 和图片形式存储）

![](https://pbs.twimg.com/media/HE_h9z1WMAERjR0.jpg)

数据导入：
- 将源文档（文章、论文、代码库、数据集、图片等）索引到 `raw/` 目录中
- 然后使用 LLM 逐步“编译”个维基，本质上就是目录结构中的 .md 文件集合。这个维基包含 raw/ 中所有数据的摘要、反向链接，然后它将数据分类到各个概念中，为每个概念撰写文章，并将它们全部链接起来。为了将网页文章转换为 .md 文件，我喜欢使用 Obsidian Web Clipper 扩展，然后我还使用快捷键将所有相关图片下载到本地，以便我的 LLM 能够轻松引用它们。

[Obsidian](https://obsidian.md/) 是"高级收藏夹": 文件扔进去就不管了，偶尔打开翻翻，找东西全靠记忆和搜索。

30个markdown文件，7个PDF报告，散落在"新闻""报告""洞察""笔记"几个目录里，互相之间没有任何关联。

卡帕西的 LLM Wiki 坑挖，自己不实现，全靠社区用户手搓。
- LLM Wiki适合1k以下markdown文档

## 【2026-4-4】Graphify

知识图谱（Knowledge Graph）并非新概念——谷歌于2012年正式引入这一术语，用于结构化表达实体及其相互关系。

在代码库理解这一特定场景中，知识图谱的优势尤为突出：大型语言模型在处理长上下文时，随着输入token数量增加，注意力权重的分配会变得更加分散，关键信息的提取准确率可能下降。通过预先构建知识图谱，将代码库的核心结构以紧凑、结构化的格式提供给语言模型，可以在不损失核心信息的前提下，大幅压缩输入长度，从而提升推理质量，降低幻觉率。

### 介绍

Graphify 开源命令行工具，由开发者 captainkink07 在 Andrej Karpathy 发文后连夜构建。
- 将任意文件夹一键转化为持久化知识图谱
- 支持 19种编程语言
- 与Claude Code深度集成
- 实现每次查询减少71.5倍token消耗。
- GitHub [graphify](https://github.com/safishamsi/graphify)

上线48小时内获得逾6000个GitHub星标，零遥测、无厂商锁定，数据永不离机。

### 原理

Graphify 核心价值主张：一条命令将任意本地文件夹转化为持久化知识图谱。
- 不仅是静态的代码分析工具，还能够在会话间持续存在、随代码库更新而自动演化的知识结构。

工作流程分为两个阶段：
- 第一阶段：**确定性解析**（零Token，零API调用）
  - 工具首先使用tree-sitter对代码库进行确定性扫描，覆盖19种编程语言。Tree-sitter是一种增量式语法解析器生成器，能够以极低的计算成本精确解析代码结构，提取函数、类、依赖关系等核心元素，全程无需调用任何语言模型，也不产生任何API费用。
- 第二阶段：**并行**智能处理（文档、论文、图像）
  - 对于文档、学术论文、图片等非代码内容，Graphify 调用 Claude进行并行处理，自动识别并提取内容间的语义关系。
  - 每条关系边都会被明确标注为以下三种状态之一：
    - found（已发现）：由代码解析直接确认的关系
    - inferred（推断）：由语言模型根据上下文推断的关系
    - uncertain（不确定）：置信度较低、存疑的关系
  - 这种透明的标注机制使得用户始终清楚哪些是"事实"，哪些是"推测"，极大降低了AI幻觉带来的风险。

### 安装

安装

```sh
pip install graphify
graphify --update # 增量更新
```


## 【2026-4-14】GBrain


### 介绍

【2026-4-14】YC 总裁 [Garry Tan](https://x.com/garrytan/status/2042497872114090069) (陈嘉里) 推出 GBrain, 专为OpenClaw、Hermes等Agent设计的“个人知识大脑”。不单纯依赖临时上下文或单一 RAG 查询，而是以 Markdown 仓库作为**唯一真相源**，结合 Postgres 和 pgvector 的混合检索引擎，构建可持续读写、人机共管、自动整理的长期记忆系统。

GBrain能够实现“<span style='color:red'>读前查脑、用后写脑、夜间巩固（dream cycle）</span>”，让知识像雪球一样越滚越大，Agent越用越聪明。
- GitHub 仓库 [garrytan/gbrain](https://github.com/garrytan/gbrain), 上线一周多目前10.1k Stars。
- 解读 [YC总裁开源智能体知识记忆系统GBrain，专为OpenClaw和Hermes设计](https://zhuanlan.zhihu.com/p/2027393611042492455)

GBrain 是面向 AI 智能体的开源个人知识记忆系统，定位是 Agent 的 “外置永久大脑”，把散落在 Markdown、Obsidian、会议纪要、邮件里的知识，都变成能被智能体高效调用的结构化记忆库。

GBrain 并非要替代 OpenClaw / Hermes的原有记忆，而是与它们形成互补的三层记忆架构，让智能体同时拥有长期知识、运行状态与实时上下文。
- GBrain：负责存储人物、公司、交易、会议、观点、原创思考等客观事实与通用认知，是智能体的长期世界知识库。
- Agent Memory：负责存储偏好、决策、运行配置、行为规则等业务状态信息。
- Session Context：自动维护当前对话内容，提供即时交互上下文。

### 应用

GBrain 可与任意 AI 智能体、MCP 客户端配合使用，也可独立运行。
- ① OpenClaw或 Hermes
- ② 独立 CLI 命令行工具
- ③ MCP 服务端（Claude Code、Cursor、Windsurf 等）

详见资讯：[YC总裁开源智能体知识记忆系统GBrain，专为OpenClaw和Hermes设计](https://zhuanlan.zhihu.com/p/2027393611042492455)

### 设计理念

GBrain 核心设计理念如下：

#### （1）Compiled Truth 和 Timeline 双层结构

每个 Markdown 页面分为当前最佳理解（Compiled Truth）和时间线（Timeline ）证据两部分，分别存放“最新结论”与“历史证据”，让知识既可查询又可追溯。人类能直接编辑Markdown，改完gbrain sync就自动同步，真正做到了“人机共管”。

#### （2）混合检索

支持向量搜索、关键词搜索以及RRF融合，兼顾语义理解与精确匹配，不遗漏关键信息。检索机制如下：

```sh
Query: "when should you ignore conventional wisdom?"
|
多查询拓展(Claude Haiku)
"contrarian thinking startups", "going against the crowd"
|
+-------+-------+
|               |
向量检索    关键词检索(HNSW     (tsvector 
+cosine)    ts_rank)
+-------+-------+
|               |
|
RRF Fusion: score = sum(1/(60 + rank))
|

四层去重机制（4-Layer Dedup）
1、每页只保留最优文本块
2、余弦相似度 > 0.85
3、类型多样性（上限 60%）
4、单页文本块数量上限
|
过时提醒（精炼结论比最新时间线内容更旧）
|
返回最终结果
```

#### （3）智能分块

GBrain 会根据内容类型，采用三种文本分块策略：
- 递归分块（适用于时间线、批量导入）：采用 5 级分隔符层级结构（段落、行、句子、从句、词语）。以 300 词为文本块，保留 50 词重叠区。速度快、效果稳定、无信息丢失。
- 语义分块（适用于精炼结论内容）：对每个句子单独生成向量嵌入，计算相邻句子的余弦相似度，通过Savitzky-Golay平滑法识别主题边界。若识别失败则自动回退到递归分块。在智能分析场景下效果最优。
- LLM 引导分块（适用于高价值内容，按需启用）：先预分割为 128 词的候选片段，再通过 Claude Haiku 在滑动窗口中识别主题转变。每个窗口支持 3 次重试。成本最高，但效果最佳。

#### （4）丰富实体

当会议、邮件、推文、链接等新信号到来时，智能体首先自动识别其中的实体（人物、公司、观点等）， 然后先查记忆库，带着完整上下文进行回应， 接着把新信息写入gbrain，更新相关页面，并同步索引供下次使用。

每完成一次这样的读-写-循环，知识库就真正增加了一份积累。 一次会议后，智能体自动丰富了某人的个人页面。下次这个人再次出现时，智能体已经拥有了丰富上下文，再也不用从零开始。

没有这套循环的智能体，永远只能靠陈旧或临时的上下文回答问题。而搭载了 GBrain 的智能体，每一次对话都在变得更聪明。

#### （5）夜间巩固（dream cycle）

夜间定时任务（cron）自动扫描所有对话、补充缺失的实体、修复错误的引用、整理记忆。像人类睡眠时大脑巩固记忆一样，让知识真正“长”起来。


### 安装

安装

```sh
# 自然语言方式
Retrieve and follow the instructions at:
https://raw.githubusercontent.com/garrytan/gbrain/master/INSTALL_FOR_AGENTS.md
# 原生
git clone https://github.com/garrytan/gbrain.git && cd gbrain && bun install && bun link
gbrain init                     # local brain, ready in 2 seconds
gbrain import ~/notes/          # index your markdown
gbrain query "what themes show up across my notes?"
```

# 结束
