---
layout: post
title:   OpenHuman 使用笔记
date:   2026-05-17 20:28:00
categories: 大模型
tags: openclaw 龙虾 hermes agent openhuman
excerpt: OpenHuman 安装、使用、技术原理、应用案例、进化方向等
mathjax: true
permalink: /openhuman
---

* content
{:toc}


# OpenHuman 使用指南

解决什么问题？
- openclaw 和 hermes
  - 主要通过 CLI 命令行方式接入，不友好
  - 用户要调教，配skill、写prompt、调工作流。
  - 各种工具、模型来回倒腾
- 个人知识库
  - 使用时，逐步积累个人记忆
  - `LLM Wiki` 把所有笔记、文档、项目信息、待办事项，全部整理成结构化 Markdown 文件，扔进Obsidian里，让AI持续索引和理解。这套操作全手工。

OpenHuman 
- UI 优先，不需要 CLI 命令行交互，降低使用成本
- 不用切换模型、节省token（80%）
- 把卡帕西这套手工活，变成了全自动流水线。

OpenHuman 更适合「不想折腾」的普通用户 —— 开箱即用体验更接近商业产品。

产品判断：
- AI 助手的普及不能只靠开发者社区，必须降低到普通用户的使用门槛。桌面吉祥物看似"卖萌"，实则是将 AI 状态可视化的一种交互设计思路。


## OpenHuman 介绍

【2026-5-14】Tiny Humans AI 团队的 [OpenHuman](https://tinyhumans.ai/openhuman) 
- 定位： “Your Personal AI super intelligence” 一款私有、简单且极其强大的个人 AI 超级智能体。
- 并非单纯的聊天机器人，而是个人 AI 系统，支持长期记忆、外部服务集成、模型路由和工具调用，与桌面环境深度融合，形成完整的助手体验。

OpenHuman 不需要人教
- 连上个人 Gmail、GitHub、Slack、Notion、日历…… 118个服务一键接进来
- 每20分钟自动抓一遍新数据
- 压缩进卡帕西式的**本地知识库** `LLM Wiki`, 详见站内专题：[LLM知识库](llm_kgbase)。

一次同步跑完，没有训练期，没有磨合期，第一天上班就能干活。

> Your Personal AI super intelligence. Private, Simple and extremely powerful.

链路：连接 → 抓取 → 记忆树。
- 第一步，连。 目前 OpenHuman 支持118+第三方服务，Notion、GitHub、Slack、Stripe、Drive……覆盖了大多数人日常工作的核心工具。
  - 每个连接都是一键授权，不需要每个平台手动生成API Key。
- 第二步，抓。 连接完之后，核心引擎每20分钟自动轮询所有已连接的账户。
  - 新邮件、日程变更、代码提交、文档更新……全拉到本地。
  - 你不用写任何prompt或轮询脚本，Agent自己知道什么时候该刷新。
- 第三步，记。 抓来的数据经过清洗和压缩，切成不超过3000个Token的Markdown片段，按主题、时间线、关联对象做评分和层级摘要，最终折叠成一棵记忆树。

这棵树的本体是本地SQLite数据库。但同一份数据，还会同步生成.md文件，落盘成兼容Obsidian的本地知识库，可以直接用Obsidian打开、浏览、编辑Agent的“记忆”。

记忆树之外，还有个挺实用的设计，TokenJuice。每次工具调用结果、网页抓取、邮件正文，在送到LLM之前，先过一遍压缩：
- HTML转Markdown、长URL缩短、非ASCII字符清理、冗余信息去重。

Token消耗能砍掉80%。

三层规则叠加，内置默认规则、用户自定义规则、项目级规则，全以JSON文件存储，改了不用重新编译。

OpenHuman 还有个Mascot功能，一个“会说话”的虚拟形象能作为独立参会者加入Google Meet会议。开会，旁听记要点。你离开电脑，它在后台继续执行待办任务。

在潜意识循环机制下，即使不主动跟它交互，也会自己加载待办、读取近期记忆、自主决定还有什么可以干。

OpenHuman（私有AI大脑）: 深度融入日常生活。每条要点均可跳转至文档内的深度详解
- [openhuman](http://github.com/tinyhumansai/openhuman)
- 【2026-5-16】[虾马之后又火一个！OpenHuman用20分钟了解你的一切，存成卡帕西式知识库](https://mp.weixin.qq.com/s/YC4Xt8yKk3yxpIqJMwBZlw)
- openhuman解读：[OpenHuman 入门指南: 比 OpenClaw 更易用的开源 AI 助手](https://openclawapi.org/blog/2026-05-17-openhuman-getting-started)
- [OpenHuman 深度剖析：让 AI 成为真正“懂你“的桌面级智能体](https://openeuler.csdn.net/6a0575be0a2f6a37c5aa2dc3.html)

### openclaw vs hermes vs openhuman

OpenHuman和Claude Cowork、OpenClaw、Hermes Agent主流Agent做了对比。

OpenHuman 设计目标：减少供应商碎片化、将工作流知识保留在设备上、为智能体提供个人数据的持久记忆，而不仅仅是对话。

| 维度 | Claude Cowork | OpenClaw | Hermes Agent | OpenHuman |
| --- | --- | --- | --- | --- |
| Open‑source | ❌ Proprietary | ✅ MIT | ✅ MIT | ✅ GNU |
| Simple to start | ✅ Desktop + CLI | ⚠️ Terminal‑first | ⚠️ Terminal‑first | ✅ Clean UI, minutes |
| Cost | ⚠️ Sub + add‑ons | ⚠️ BYO models | ⚠️ BYO models | ✅ One sub + TokenJuice |
| Memory | ✅ Chat‑scoped | ⚠️ Plugin‑reliant | ✅ Self‑learning | 🚀 Memory Tree + Obsidian vault, optional agentmemory backend |
| Integrations | ⚠️ Few connectors | ⚠️ BYO | ⚠️ BYO | 🚀 118+ via OAuth |
| Auto‑fetch | ❌ None | ❌ None | ❌ None | ✅ 20‑min sync into memory |
| API sprawl | ❌ Extra keys | ❌ BYOK | ❌ Multi‑vendor | ✅ One account |
| Model routing | ❌ Single model | ⚠️ Manual | ⚠️ Manual | ✅ Built‑in |
| Native tools | ✅ Code‑only | ✅ Code‑only | ✅ Code‑only | ✅ Code + search + scaper + voice |

OpenHuman 差异化优势：
- ① 一键集成 + 自动同步
  - OpenClaw 和 Claude Code 都需要用户手动配置上下文来源。
  - OpenHuman 的 118+ OAuth 集成 + 20 分钟自动同步，让 AI 在首次接入时就获得完整的上下文背景。这是它最大的竞争差异点。
- ② Memory Tree 的可解释性
  - 相比纯向量检索的"黑盒"匹配，Memory Tree 的分层结构让用户可以理解和审查 AI 的记忆来源。这在企业合规和个人隐私场景下都有实际价值。
- ③ 桌面级存在感
  - OpenHuman 强调与桌面环境的深度融合：常驻运行的 desktop agent、会说话的吉祥物、能够主动加入 Google Meet 的会议代理等。这些设计让 OpenHuman 不只是一个工具，而更像一个"数字伙伴"。

但也需要正视的劣势
- 生态成熟度：相比 OpenClaw 的 37 万+ Stars 和庞大社区，OpenHuman 的 ~6,300 Stars 仍处于早期阶段
- 稳定性风险：项目自述为 Early Beta，“Expect rough edges”，生产环境使用需谨慎
- 供应商风险：统一订阅模式虽然降低了配置门槛，但也意味着用户对模型选择的自主权受限
- 隐私攻击面：自动同步 118+ 服务意味着本地存储了极为完整的个人数据图谱，一旦本地系统被攻破，损失远大于单一应用


## OpenHuman 特点

OpenHuman 记忆 + 自动同步 + 后台潜意识，三件事打包，让 Agent 开口之前已经准备好了。

OpenHuman 核心优势：
1. 整合118个服务信息（邮件/日历/GitHub等），例行主动同步（20min）
2. 快速建立个人知识库；
3. 简洁GUI界面，告别命令行门槛：UI-first 的桌面体验
4. 自动吉祥物 mascot，可以说话、响应周围环境、甚至加入 Google Meet 作为真正的参会者，并能跨周记住用户。突破了传统 AI 助手"黑箱"式的交互模式，让用户能够直观感知 AI 的存在和状态。
5. 部署简单，几步完成，无需一堆终端参数；
6. 隐私安全：本地存储，随时可查改删；
7. 串联碎片信息成"第二大脑"。
8. 原生语音支持：STT 输入、ElevonLabs TTS 输出、吉祥物口型同步
9. 节省token：TokenJuice 压缩技术，Token 用量最高降低 80%，延迟大幅下降

核心亮点
- 零门槛部署：纯可视化界面，拒绝终端命令，普通用户可快速上手；
  - 干净流畅的桌面交互、极简上手流程，只需几步点击即可完成安装并启用智能体 —— 无需先做复杂配置，完全不用命令行终端
  - 专属桌面虚拟形象：可语音交互、感知环境、以真实参与者身份加入谷歌会议、长期记忆你的习惯，即便你停止输入，也会在后台持续运行思考
- 自动数据生态：118 + 平台一键接入，20 分钟自动同步数据，自动维护上下文；
  - 一键 OAuth 即可接入 Gmail、Notion、GitHub、Slack、Stripe、日历、云盘、Linear、Jira 等你常用的全栈工具。
  - 所有接入服务都会以标准化工具开放给智能体；
  - 每 20 分钟自动遍历全部活跃连接，将最新数据同步至记忆树。无需手动编写提示词或轮询脚本，智能体可提前掌握次日所需的上下文信息
- 本地私有记忆：Obsidian 兼容知识库，数据本地加密，隐私可控；
  - 基于个人数据与行为构建本地优先知识库。所有接入数据被规范为≤3000token 的 Markdown 片段，经过权重评分后，整合为层级式摘要树，本地存储于 SQLite 数据库。
  - 同步生成可直接在 Obsidian 中打开、浏览、编辑的.md 格式知识库，灵感源自 Karpathy 的 Obsidian Wiki 工作流。
- 全能原生工具：内置搜索、爬虫、代码、语音、会议接入，无需额外插件；
  - 默认内置网页搜索、网页抓取工具、全套代码工具集（文件系统、Git、代码检查、测试、文本检索），以及原生语音功能（语音转文字输入、ElevenLabs 语音合成输出、虚拟形象唇形同步、谷歌会议实时接入）。
- 极致成本优化：TokenJuice 压缩技术，Token 用量最高降低 80%，延迟大幅下降
- 模型自动路由：统一订阅下，自动为不同任务匹配最优大模型（推理型、轻量快速型、视觉型），无需额外安装插件即可实现文件读取等功能；支持通过 Ollama 部署本地离线 AI。 
- 多消息渠道与隐私安全
  - 兼容日常使用的各类收发消息渠道，工作流数据全程本地留存、加密存储，所有权归用户所有

### OpenHuman 为什么火

OpenHuman 火的原因，刚好踩中了三个问题。
- API密钥一大堆、各类平台数据分散难整合、上下文臃肿导致AI越用越卡顿。

OpenHuman一个账号搞定所有，不用反复注册、不用到处配置密钥；
- 内置118+主流应用一键互联，自动拉取全平台数据同步进专属记忆树，全程后台静默运行、持续自主思考，最高还能节省80% token消耗与响应延迟。

这三个痛点拆开是功能问题，合起来其实是还不够贴合用户真实使用习惯：

之前的 Agent，心思都花在“能干”上了，但在“懂你”这方面，始终差了点意思。

虾解决工具多的问题，马解决能自学的问题，但懂你的，还得Human来（doge）。




## 使用

【2026-5-17】[OpenHuman 入门指南: 比 OpenClaw 更易用的开源 AI 助手](https://openclawapi.org/blog/2026-05-17-openhuman-getting-started)

### 安装

一键安装,脚本会自动检测你的系统环境，下载对应平台的二进制文件（DMG/EXE）。

```sh
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/tinyhumansai/openhuman/main/scripts/install.sh | bash
# Windows
irm https://raw.githubusercontent.com/tinyhumansai/openhuman/main/scripts/install.ps1 | iex
```

源码安装

```sh
# 1. Fork 并克隆仓库
git clone https://github.com/tinyhumansai/openhuman.git
cd openhuman

# 2. 初始化子模块
git submodule update --init --recursive

# 3. 安装依赖
pnpm install

# 4. 纯 Web UI 开发
pnpm dev

# 5. 完整桌面应用开发
pnpm dev:app
```

### 配置

配置模型

```sh
cp .env.example .env
# Claude (推荐)
ANTHROPIC_API_KEY=sk-ant-xxxxx
# OpenAI GPT
OPENAI_API_KEY=sk-xxxxx
# Google Gemini
GEMINI_API_KEY=xxxxx
```

查看配置

```sh
# 查看当前模型配置
openhuman config show
# 手动指定模型
OPENHUMAN_MODEL=claude-sonnet-4-20250514
```


### 记忆设置

OpenHuman 记忆系统会自动同步个人数据。

关键配置项：

```sh
# 记忆同步间隔（默认 20 分钟）
OPENHUMAN_MEMORY_SYNC_INTERVAL=20
# Obsidian 仓库路径
OPENHUMAN_OBSIDIAN_VAULT_PATH=~/Documents/openhuman-vault
# TokenJuice 压缩级别
OPENHUMAN_TOKENJUICE_COMPRESSION=high
OPENHUMAN_TOKENJUICE_ENABLED=true
OPENHUMAN_TOKENJUICE_LEVEL=high

# 重启核心服务
openhuman restart
# 记忆数据存储在本地 SQLite：
# 默认存储路径
~/.openhuman/memory.db
```

### CLI

除了 GUI，还支持 CLI 模式

CLI 模式

```sh
# 启动核心服务
openhuman serve
# 交互式对话
openhuman run
验证运行状态
# 检查健康状态
curl http://127.0.0.1:7788/health
# 查看核心 token
cat ~/.openhuman/core.token
```

## 数据


### 隐私优先

隐私优先的架构设计

OpenHuman 的隐私架构遵循 “opt-in” 原则：本地 AI 功能默认关闭，用户需显式启用。

**OpenHuman 混合部署架构**，核心是**轻量任务本地私有化、重推理与多模态上云**：
1. **隐私型任务本地跑**：向量嵌入、记忆摘要树、后台自我反思全部在本地 Ollama 运行，数据不对外流出；选用极小参数量模型，硬件压力低。
2. **高性能任务上云**：复杂逻辑推理、图像/语音多模态交互调用云端大模型，兼顾能力与响应速度。
3. 整体实现**本地隐私安全 + 云端能力增强**的平衡。

| 工作负载 | 运行位置 | 使用的模型 |
| :--- | :--- | :--- |
| Embeddings 生成 | 本地（Ollama） | all‑minilm:latest (~23MB) |
| 摘要树构建 | 本地（Ollama） | gemma3:1b‑it‑qat (~700MB) |
| 后台反思循环 | 本地 | heartbeat / learning / subconscious |
| 复杂推理任务 | 云端 | 前端大模型 |
| 多模态交互 | 云端 | vision / STT/TTS |


分层策略的权衡：
- 隐私敏感的数据处理（记忆构建、embeddings）留在本地，而对模型能力要求高的交互（深度推理、视觉理解）则利用云端的前沿模型。
- 模型路由器会根据任务类型自动选择执行路径，轻量级任务（分类、摘要）在本地可用时优先本地执行。

工作空间默认位于 `~/.openhuman`，所有数据存储在本机，用户完全掌控自己的数据主权。


### Auto-fetch：自动化数据同步

OpenHuman 支持一键 OAuth 连接 118+ 第三方服务，包括 Gmail、Notion、GitHub、Slack、Stripe、Calendar、Drive、Linear、Jira 等。这些集成并非简单的 API 调用，而是具备完整的自动抓取能力：
- 核心引擎每 20 分钟主动连接每个活跃连接并拉取新鲜数据
- 拉取的数据直接进入 Memory Tree 管道，被规范化为 ≤3k token 的 Markdown 块
- 同步过程在本地完成，不经过云端中转

用户不需要"教"AI 了解自己的工作环境——在一次同步周期内，AI 便已具备完整的上下文（收件箱、日历、代码仓库、文档、消息）。

OpenHuman 从根本上解决了 AI 代理的"冷启动"问题，将获取可用上下文的时间从天级降到了小时级。

⚠️ 潜在风险：
> 自动抓取意味着 AI 系统持续接触敏感数据（邮件内容、代码变更、财务信息等）。
> 虽然数据存储在本地，但用户需要理解：一旦本地系统被攻破，攻击者可获取的是完整的个人数据图谱，而非单一应用的数据。



## 记忆

Memory Tree：三层树状记忆架构

OpenHuman 最具创新性的设计：Memory Tree（记忆树），摒弃了传统向量数据库"黑盒"方案，转而采用确定性的**分层摘要树结构**。

所有接入的数据源（118+ 外部服务）都经过统一的管道处理：

```sh
source adapters → canonicalize (Markdown) → chunker (≤3k tokens)
→ content_store (原子 .md 文件) → score (信号 + embeddings + 实体提取)
→ source/topic/global trees → retrieval
```

这一管道产生三种不同粒度的记忆树：

| 记忆树类型 | 核心机制 | 适用场景 |
| --- | --- | --- |
| Source Tree（来源树） | 每个数据源拥有独立的滚动缓冲区，按 L0→L1→L2 层级密封 | 追溯某个 Gmail 标签或 Slack 频道的完整时间线 |
| Topic Tree（主题树） | 基于“热度”算法为高频实体构建按需摘要树 | 追踪某个项目、人物或关键词的演变 |
| Global Tree（全局树） | 每日 UTC 时间生成的全局摘要 | 回答“今天发生了什么”这类跨源问题 |

这种三层架构的设计借鉴人类认知科学中"分层记忆"的思想：
- 浅层节点捕获高层概要，深层节点保留细粒度细节。
- 与纯向量存储相比，树状结构提供了压缩与导航的双重能力。
- Embeddings 仍然存在于节点中以支持语义搜索，但树状结构让记忆具备可解释性，而非碎片化的"相似度匹配"。

所有记忆块会以 .md 文件形式存入 Obsidian 兼容的 Vault，用户可以直接用 Obsidian 打开、浏览和编辑，灵感来源于 Karpathy 在 2026 年 4 月提出的 LLM Knowledge Base 概念。

### 局限

尽管 Memory Tree 的设计理念优雅，但也存在挑战：
- 跨源冲突处理：当 Gmail 中的信息与 Notion 中的信息矛盾时，树结构如何决定优先级？目前文档未详细说明冲突解决策略
- 高频更新的一致性：118+ 数据源每 20 分钟同步一次，在高频写入场景下，树结构的节点可能处于不一致状态
- "热度"算法的透明度：Topic Tree 依赖热度算法决定哪些实体值得建树，但算法细节未公开，用户难以理解和调优
- 压缩的信息损失：层级摘要不可避免地会丢失细节，对于需要精确回溯的场景（如法律合规、审计），可能需要回溯到原始 .md 文件


## token 效率

自动分派任务到合适的模型（推理型、快速型或视觉型）

本地化 AI 面临的关键工程挑战是成本控制与资源管理。


### 节省token？

如何节省 token 成本？
- OpenHuman 内置 TokenJuice 压缩和 Defapi 的低价策略配合使用

[Defapi](https://defapi.org/)：兼容 OpenAI v1/chat/completions 协议的中转平台，价格只有官方的一半。

Defapi 支持以下协议：
- v1/chat/completions 接口（OpenAI 兼容）
- v1/messages 接口（Anthropic 兼容）
- v1beta/models/ 模型列表接口

配置项

```sh
# Defapi 配置示例
ANTHROPIC_API_KEY=dk-xxxxx        # Defapi 的 Key，格式为 dk- 前缀
OPENAI_API_KEY=dk-xxxxx

# 或者通过 base_url 指定端点（如果 OpenHuman 支持）
ANTHROPIC_BASE_URL=https://api.defapi.org/v1
OPENAI_BASE_URL=https://api.defapi.org/v1/chat
```

支持的模型包括：
- anthropic/claude-sonnet-4.5 / claude-opus-4.5 / claude-haiku-4.5
- openai/gpt-4o / gpt-4o-mini / gpt-5
- google/gemini-3-flash


### TokenJuice：智能 Token 压缩

OpenHuman 通过 TokenJuice 压缩技术解决这一问题：在工具输出进入模型上下文之前进行智能压缩。

TokenJuice 核心机制：
- HTML 转换为 Markdown
- 长 URL 缩短
- 非 ASCII 字符规范化
- 冗余信息过滤

官方 README 数据显示，TokenJuice 可以减少 高达 80% 的 Token 消耗和延迟。
- 这一数据基于官方基准测试，实际压缩率因数据类型而异：自然语言邮件的压缩率可能较高，而代码片段、结构化数据（JSON/表格）的压缩空间相对有限。

⚠️ 风险提示：
> 压缩技术确实存在信息丢失的风险，特别是对代码片段、合同条款、时间戳等敏感信息，规范化或删除字符可能改变语义或丢失关键证据。
> 建议采取分级压缩策略：对邮件、笔记等高压缩，对合同、代码采用低压缩或无压缩。



# 结束
