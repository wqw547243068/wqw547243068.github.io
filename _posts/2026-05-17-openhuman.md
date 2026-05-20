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

## OpenHuman 介绍

【2026-5-17】[OpenHuman](https://tinyhumans.ai/openhuman) 不需要教
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


## OpenHuman 特点

OpenHuman 记忆 + 自动同步 + 后台潜意识，三件事打包，让 Agent 开口之前已经准备好了。

OpenHuman 核心优势：
1. 整合118个服务信息（邮件/日历/GitHub等），例行主动同步（20min）
2. 快速建立个人知识库；
3. 简洁GUI界面，告别命令行门槛
4. 部署简单，几步完成部署；
5. 隐私安全：本地存储，随时可查改删；
6. 串联碎片信息成"第二大脑"。
7. 原生语音支持：STT 输入、ElevonLabs TTS 输出、吉祥物口型同步
8. 节省token：TokenJuice 压缩技术，Token 用量最高降低 80%，延迟大幅下降

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

#### 模型路由

自动分派任务到合适的模型（推理型、快速型或视觉型）



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



# 结束
