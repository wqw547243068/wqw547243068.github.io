---
layout: post
title:   优质 Skills 汇总
date:   2026-04-30 21:20:00
categories: 大模型
tags:  skill mcp 龙虾 markdown html
excerpt: 总结各类实用 Skills 
mathjax: true
permalink: /skill_set
---

* content
{:toc}


# Skill 应用


## Skill 原理


### Skill 介绍

目前，skill 都以 markdown 格式存在

```
pdf-to-markdown/
├── SKILL.md                  # Skill说明文档（含元数据、使用指南、核心指令）
├── scripts/                  # 自动化脚本（含各类可执行脚本）
│   └── convert.py            # 转换pdf为md的自动化脚本
└── evals/                    # 测试工具集
    └── evals.json            # 3个典型的测试用例
```

详见站内专题：[Skill 技术专题](skill)


### HTML

2026年5月10日，Claude Code 工程师塔里克·希希帕尔（`Thariq Shihipar`）发文，标题 《在 Claude Code 工作流中，HTML 为何“不讲道理地好用”》。

理由：
> HTML 可以承载 Markdown 完全做不到的 8 种内容：表格、CSS、SVG、代码高亮、JS 交互、工作流程图、空间画布数据、真实图像，而且这一切，打开浏览器立刻能用 🔥

生产场景用例：
- ✅ 规格与规划文档
- ✅ AI 代码审查
- ✅ 设计与原型验证
- ✅ 研究与报告
- ✅ 定制化的一次性编辑界面

🧐为什么偏偏是 Claude Code，而不是 Claude 聊天界面或者 Claude 设计工具？
- 因为 Claude Code 有完整的上下文堆栈：文件系统访问权限、MCP 服务器、Chrome 浏览器内的 Claude，加上 Git 历史记录。
- 这些能力凑在一起，才让“输出 HTML”这件事变得值钱——它不仅仅是好看，而是真正可运行、可交互、可继续被 AI 修改的功能块。

⚠️但关键瓶颈依然现实：Token 成本。
- HTML 比 Markdown 啰嗦得多，相同内容量可能要烧掉 2-4 倍的 Token。一旦上下文窗口紧张，这个开销会非常致命。
- 所以问题：HTML 能否真正取代 Markdown 成为 AI 编码代理的默认格式？还是说它只会是特定高价值场景的“奢侈选择”？


## 总结

【2026-6-25】[盘点16个把自己蒸馏成Skills的国民级App](https://mp.weixin.qq.com/s/08Z-Jk4nccaBAbh65aqtKA)

16款国民级 App Skill/MCP/CLI能力汇总表

|序号|产品名称|支持协议类型|官方入口|核心能力|支付/下单限制|所属行业|
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
|1|瑞幸咖啡|Skill、MCP、CLI| [lkcoffee](open.lkcoffee.com)|AI点咖啡、查询门店、商品检索、无咖啡因饮品推荐、到店下单、生成取餐码|仅支持到店自取，需网页扫码支付，不支持外卖|餐饮|
|2|麦当劳|MCP|[麦当劳MCP](https://open.mcd.cn/mcp)|查询优惠活动日历、领券、AI点餐|最终支付需跳转麦当劳App|餐饮|
|3|飞猪（FlyAI Skill）|Skill（底层MCP）|[flyai](https://flyai.open.fliggy.com/)|机票/酒店/门票/用车咨询、行程规划、航班对比、酒店筛选、预定跳转|体验版数据不全，完整能力需申请API Key|出行旅游|
|4|滴滴出行|MCP、Skill|[滴滴mcp](https://mcp.didichuxing.com/)|实时叫车、预约用车、订单查询、司机位置实时查看、司机到店触发飞书通知|支付跳转滴滴App|出行打车|
|5|高德地图|MCP、Skill市场|[高德lbs](https://lbs.amap.com/)|位置检索、路线规划、周边酒店/商户搜索、Android/iOS/RTOS地图能力|无支付链路，仅信息查询|地图位置服务|
|6|腾讯地图|Skill、MCP|[qq mcp](https://lbs.qq.com)|地点搜索、路线规划、天气查询、3D/Three.js/GLTF前端地图开发|无支付链路，仅信息查询|地图位置服务|
|7|美团跑腿|Skill| [MT-Paotui-For-Client](github.com/meituan/MT-Paotui-For-Client)|地址簿匹配、订单预览、跑腿下单|确认后跳转App完成支付|本地生活配送|
|8|飞书|Skill、MCP、CLI|[飞书](https://open.feishu.cn/)|消息、日程、待办、审批、文档、团队协作全量自动化|无支付能力|企业办公|
|9|钉钉|Skill、MCP、CLI|[钉钉](https://open.dingtalk.com/)|消息收发、待办、日程、审批流、团队协同操作|无支付能力|企业办公|
|10|企业微信|Skill、MCP、CLI| [wecom-cli](github.com/WecomTeam/wecom-cli)|消息收发、通讯录管理、企业内部协作|无支付能力|企业办公|
|11|腾讯文档|Skill、MCP|[docs](https://docs.qq.com/open/document/)|创建/编辑在线文档、知识库管理、AI生成PPT|无支付能力|云文档办公|
|12|支付宝|支付MCP、支付Skill|[alipay](https://open.alipay.com/)|网页/手机支付、订单创建/查询、退款、收款链接生成，个人开发者可用|面向商户/开发者收款，不支持AI替用户付款|金融支付|
|13|微信支付|MCP、Skill|[wechatpay-skills](https://github.com/wechatpay-apiv3/wechatpay-skills)|支付方案选型、代码生成、代码安全检测、券发放/核销/退券|面向开发者集成，非普通用户消费支付|金融支付|
|14|微信读书|Skill|[weread-skills](weread.qq.com/r/weread-skills)|书架查询、阅读时长统计、笔记/划线检索、书籍检索、个性化推荐|无支付能力|数字阅读文娱|
|15|网易云音乐|Skill、CLI|[NetEase skills](github.com/NetEase/skills)|歌曲搜索、播放、歌单管理、红心偏好分析|无支付能力|音乐文娱|
|16|美图|Skill、CLI|[open-claw](https://www.miraclevision.com/open-claw)|图片编辑、文生图、文生视频、AI写真、换脸、虚拟换装、背景替换|无支付能力|图像视频工具|

生态集成产品（非独立开放Skill平台）

|产品|集成第三方Skill说明|
| ---- | ---- |
|千问|1月接入阿里生态（淘宝、支付宝、飞猪、高德）；6月开放第三方，首批接入肯德基、蜜雪冰城、东方航空|
|豆包|6月22日灰度上线打车Skill，对接曹操出行|
|WorkBuddy（腾讯）|内置腾讯全系Skill/MCP：微信支付、QQ邮箱、腾讯文档、腾讯问卷、微云等|

总结
1. **支付统一约束**：所有消费类App均不允许Agent自动完成支付，全部跳转App/网页扫码，由用户手动确认付款，信任与合规是核心限制；
2. **办公赛道开放度最高**：飞书、钉钉、企业微信均同时开放Skill/MCP/CLI三种标准；
3. **协议通俗理解**：MCP/CLI均可视为增强版Skill，统一供给Agent调用，接入方式标准化。


## 信息获取

去网上找点东西，就抓瞎了：
- 📺 "帮我看看这个 YouTube 教程讲了什么" → 看不了，拿不到字幕
- 🐦 "帮我搜一下推特上大家怎么评价这个产品" → 搜不了，Twitter API 要付费
- 📖 "去 Reddit 上看看有没有人遇到过同样的 bug" → 403 被封，服务器 IP 被拒
- 📕 "帮我看看小红书上这个品的口碑" → 打不开，必须登录才能看
- 📺 "B站上有个技术视频，帮我总结一下" → 连不上，海外/服务器 IP 被屏蔽
- 🔍 "帮我在网上搜一下最新的 LLM 框架对比" → 没有好用的搜索，要么付费要么质量差
- 🌐 "帮我看看这个网页写了啥" → 抓回来一堆 HTML 标签，根本没法读
- 📦 "这个 GitHub 仓库是干嘛的？Issue 里说了什么？" → 能用，但认证配置很麻烦
- 📡 "帮我订阅这几个 RSS 源，有更新告诉我" → 要自己装库写代码

每个平台都有自己的门槛——要付费的 API、要绕过的封锁、要登录的账号、要清洗的数据。你要一个一个去踩坑、装工具、调配置，光是让 Agent 能读个推特就得折腾半天。

### 总结

- [Agent-reach](https://github.com/Panniantong/Agent-Reach) 各社媒平台数据获取
- [opencli](https://opencli.info/) 浏览器自动化
- [bb-browser](https://github.com/epiral/bb-browser) 浏览器 API: 坏孩子浏览器 BadBoy Browser, 不需要密钥，不需要爬虫，不需要模拟


### 信息抓取

#### MediaCrawler

[MediaCrawler](https://nanmicoder.github.io/MediaCrawler/) - 自媒体平台爬虫 🕷️
- GitHub [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)

小红书、抖音视频、快手视频、B 站视频、微博帖子、百度贴吧帖子、知乎问答文章

```sh
# 依赖 playwright (openai产)
uv run playwright install
# 运行
# 项目默认未开启评论爬取，如需评论请在 config/base_config.py 中修改 ENABLE_GET_COMMENTS
# 其他功能开关也可在 config/base_config.py 查看，均有中文注释

# 从配置中读取关键词搜索并爬取帖子与评论
uv run main.py --platform xhs --lt qrcode --type search

# 从配置中读取指定帖子ID列表并爬取帖子与评论
uv run main.py --platform xhs --lt qrcode --type detail

# 使用 SQLite 数据库存储数据（推荐个人用户使用）
uv run main.py --platform xhs --lt qrcode --type search --save_data_option sqlite

# 使用 MySQL 数据库存储数据
uv run main.py --platform xhs --lt qrcode --type search --save_data_option db

# 其他平台示例
uv run main.py --help
```

#### Agent-Reach

[Agent-Reach](https://github.com/Panniantong/Agent-Reach)

- 所有工具开源、所有 API 免费
- Cookie 只存在你本地，不上传不外传。代码完全开源
- 底层工具（yt-dlp、twitter-cli、rdt-cli、Jina Reader 等）定期追踪更新到最新版

安装

```sh
# 安装
帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
# 更新
帮我更新 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/update.md
```

#### 【2026-5-11】AnySearch

【2026-5-11】[谷歌搜不到的80%互联网，AnySearch全打通了！开发者连夜接入](https://mp.weixin.qq.com/s/-pWdGGf4U4D5wCDnw9lawg)

5月11日，[AnySearch](http://www.anysearch.com) 产品海外正式上线。
- GitHub：[anysearch-ai](https://github.com/anysearch-ai)
- 也可在ClawHub、SkillHub、Glama、skills.sh等插件商店直接获取

定位：AI时代的「搜索基础设施」，专为AI Agent打造统一的高质量搜索入口。

AnySearch 通过大模型获取 Reddit 论坛、代码仓库、股票市场等多种信息

安装
- 官网 [AnySearch](http://www.anysearch.com)，点击 Install/安装，复制安装教程直接输入Agent，部署完成。

```sh
Install the AnySearch SKILL according to 
https://anysearch.com/install/skill-install.md
```

评测
- AnySearch 与 Brave、Perplexity 做了对比，显然 AnySearch输出的结果更丰富。
- 基准测试中，AnySearch在准确性和响应延迟两个维度，均优于同类AI搜索产品Parallel和Brave。
- 与同类Brave Search测试对比，结果显示，AnySearch数据更完整、分析更深入、回答更全面

#### 公众号文章抓取

[wechat_articles_spider](https://github.com/klin-h/wechat_articles_spider)


## 浏览器操控


### playwright

OpenAI 推出的 playwright

### bb-browser


[bb-browser](https://github.com/epiral/bb-browser) 浏览器 API: 坏孩子浏览器 BadBoy Browser
- 不需要密钥，不需要爬虫，不需要模拟

已经登录了微博、知乎、B站、小红书、Twitter、GitHub、LinkedIn — bb-browser 让 AI Agent 直接用你的登录态

```sh
# 安装
npm install -g bb-browser
# 使用
bb-browser site update        # 拉取社区适配器
bb-browser site recommend     # 看看哪些和你的浏览习惯匹配
bb-browser site zhihu/hot     # 开搞

bb-browser site twitter/search "AI agent"       # 搜索推文
bb-browser site zhihu/hot                        # 知乎热榜
bb-browser site arxiv/search "transformer"       # 搜论文
bb-browser site eastmoney/stock "茅台"            # 实时股票行情
bb-browser site boss/search "AI 工程师"           # 搜职位
bb-browser site wikipedia/summary "Python"       # 维基百科摘要
bb-browser site youtube/transcript VIDEO_ID      # YouTube 字幕全文
bb-browser site stackoverflow/search "async"     # 搜 StackOverflow
```

### OpenCLI

[OpenCLI](https://opencli.info/) 
- [OpenCLI](https://github.com/jackwener/opencli)

使用

```sh
npm install -g @jackwener/opencli
opencli bilibili hot --limit 5
opencli twitter trending
```

## 垂类知识


### 金融

【2026-5-10】[Claude 的金融 Skills 开源](https://mp.weixin.qq.com/s/8_S8ynPyy7SHy_OW0lbYuA)

Anthropic 把华尔街分析师每天干的活，拆成了一套 Claude 可以直接装的插件包
- 替分析师起草工作底稿（模型、备忘录、研报、对账单）的，不做投资决策、不执行交易、不绑定风险、不批准开户，每一份产出都摆在那儿等人类签字
- 边界划得很干净，金融行业最敏感的就是**责任**，能跑活但不背锅，反而是 To B 落地最现实的姿势

Anthropic 官方仓库 claude-for-financial-services，把投行、股票研究、私募股权、财富管理这四条华尔街最贵的赛道全端了出来
- 仓库地址：[financial-services](github.com/anthropics/financial-services)
- Apache 2.0，全部 Markdown + YAML，没有 build step，fork 下来就能改

安装方法

```sh
# 1. 添加 marketplace
claude plugin marketplace add anthropics/claude-for-financial-services

# 2. 先装核心包（带所有数据连接器）
claude plugin install financial-analysis@claude-for-financial-services

# 3. 按需挑 Agent
claude plugin install pitch-agent@claude-for-financial-services
claude plugin install gl-reconciler@claude-for-financial-services
claude plugin install market-researcher@claude-for-financial-services

# 4. 按需挑垂直行业包
claude plugin install investment-banking@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
```

两层：
- Agents（11 个）：端到端的工作流智能体，比如 Pitch Agent、Earnings Reviewer、GL Reconciler，每个都是自包含插件，装上就能跑一整条流水线
- Vertical Plugins（7 个垂直行业包 + 2 个合作伙伴包）：底层的 Skill、斜杠命令、数据连接器，按金融子行业打包，你不想要完整 Agent，只装这些底层能力也行

而且所有东西两种部署方式同源——既能在 Claude Cowork 里当插件用，也能通过 Claude Managed Agents API（/v1/agents）丢到自家工作流引擎后面跑无头模式，同一个 system prompt、同一组 skill，你选在哪儿落地

| 业务方向 | Agent | 干什么活 |
| ---- | ---- | ---- |
| 客户与咨询 | Pitch Agent | 可比公司 + 先例交易 + LBO → 出一份带品牌的 pitch deck |
|  | Meeting Prep Agent | 客户会议前自动出一份 briefing pack |
| 研究与建模 | Market Researcher | 给一个赛道/主题 → 行业概览 + 竞争格局 + peer comps + 标的清单 |
|  | Earnings Reviewer | 财报电话会 + 公告 → 更新模型 → 起草研报 |
|  | Model Builder | DCF、LBO、三表模型、可比公司分析，直接在Excel里跑 |
| 基金运营 | Valuation Reviewer | 接收GP报送包 → 跑估值模板 → 准备LP报告 |
|  | GL Reconciler | 找总账break、追根溯源、走签字流程 |
|  | Month-End Closer | 月末结账：计提、滚存、差异说明 |
|  | Statement Auditor | LP报表分发前的审计 |
| 运营与开户 | KYC Screener | 解析开户文档 + 跑规则引擎 + 标记缺口 |

每个 Agent 都是独立打包的，bundle 了它要用的全部 skill，装一个就够，不用先装一堆依赖

11 个 MCP 连接器
- MCP 访问可能需要数据商的订阅或 API Key

| 数据源 | 内容 |
| ---- | ---- |
| Daloopa | 标准化财务数据 |
| Morningstar | 基金研究 |
| S&P Global | 标普全球 + Capital IQ |
| FactSet | 万得海外版 |
| Moody's | 评级与信用数据 |
| MT Newswires | 即时新闻 |
| Aiera | 财报会议转写 |
| LSEG | 伦交所/路孚特 |
| PitchBook | 一级市场数据 |
| Chronograph | PE 投后监控 |
| Egnyte | 文档存储 |


## 书籍转skill

将技术书籍（PDF/EPUB）转化为 Claude Code 可加载的结构化 skill，让书中框架和知识点在工作时按需调用

### book-to-skill

【2026-5-6】book-to-skill 是 Claude Code skill，把技术书籍的 PDF 或 EPUB 自动提取并生成结构化 skill 文件，包括按章节加载的摘要、术语表、设计模式速查表。
- GitHub [book-to-skill](https://github.com/virgiliojr94/book-to-skill)

用法

```sh
/book-to-skill your-book.pdf

# PDF — derive skill name from filename
/book-to-skill ~/Downloads/designing-data-intensive-applications.pdf
# EPUB — specify a custom slug
/book-to-skill ~/books/clean-code.epub clean-code
# Full path with explicit name
/book-to-skill /tmp/ddd-evans.pdf domain-driven-design
```


## 页面设计


### 总结

【2026-7-7】UI设计总结

基于42个产物与各变体的执行记录评估。第一轮（任务A-C）考察视觉表现，第二轮（任务D-G）考察交互、组件、创造性与多样性。
- [同一个任务，装不装 设计 Skill，差别有多大？](https://designskill.qiaomu.ai/)
- 从 skills.sh 与 skillsmp.com 两大 Skill 市场, 收集并安装全部**主流前端设计 Skill**， 选出 5 个设计哲学差异最大的，加上无 Skill 对照组，在完全相同的任务简报、相同技术约束 （单文件 HTML、仅允许 Google Fonts、禁用外部图片）下各自独立生成页面。 十个任务覆盖视觉表现、交互逻辑、组件合理性、创造性、多样性、电商、移动端与数据叙事

第一轮 · 视觉表现（任务 A-C）

评价维度：视觉个性、工程规范、动效工艺、三页一致性、一句话定位

| 变体 | 一句话定位 |
| ---- | ---- |
| baseline | 干净、正确、但一眼「AI味」 |
| frontend-design | 视觉冒险家，每页一个记忆点，但风格跨页跳跃 |
| web-design-guidelines | 看不见的品质：a11y与排版规范全面碾压 |
| ui-ux-pro-max | 数据库驱动的六边形战士，风格是「查」出来的 |
| taste-skill | 最强反模板纪律：连文案用词都在管 |
| emil-design-eng | 动效工匠：静态截图看不出，一交互就懂 |

第二轮 · 交互 / 组件 / 创造性 / 多样性（任务 D-G）

评价维度：交互完成度(D)、组件合理性(E)、创造性(F)、多样性(G)、第二轮结论

| 变体 | 第二轮结论 |
| ---- | ---- |
| baseline | 功能常识扎实，短板在多样性：三个方向都逃不出赛博舒适区 |
| frontend-design | 开放命题下断层领先：Art Deco向导、玻璃故障404、三方向彻底割裂 |
| web-design-guidelines | 交互与组件双满分：焦点管理、aria语义、焦点陷阱全场唯一做全 |
| ui-ux-pro-max | UX准则逐条可溯源；唯一系统考虑404错误恢复路径的变体 |
| taste-skill | 会按任务性质自动调节冒险度；功能页收敛、404放开，纪律性最强 |
| emil-design-eng | 交互密集任务的主场：shake校验、可中断toggle、快出慢进Toast |

两大核心发现
- 发现一 · Skill 的第一作用是「禁止」而非「教学」
  - 对照组暴露了默认输出的收敛性：紫色系主色、Inter字体、居中Hero、三等分卡片。
  - 效果最好的 Skill（frontend-design、taste-skill）核心手段都是负面清单——禁用AI惯用字
- 发现二 ·「好看」和「合格」是两条赛道
  - frontend-design 产出了最惊艳的视觉（墨黑金落地页、构成主义作品集）
  - 但 web-design-guidelines 在源码层面全面领先：skip-link、aria-sort、tabular-nums、reduced-motion

其他
-  偏品牌官网/营销页：frontend-skill、frontend-design、brand-guidelines
-  产品 UI/设计稿还原：figma-implement-design、react-best-practices、web-design-guidelines
-  交互验证/可用性：playwright、webapp-testing
-  创意探索：canvas-design



### UI Ux Pro Max

UI Ux Pro Max 是 nextlevelbuilder 的仓库
- [UI Ux Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

### canvas-design


Anthropic 推出，适合更自由的视觉探索、展示型页面、画布式交互或概念设计，不是每个项目都需要，但做创意产品页很有价值

### Frontend Design

【2026-1-6】[Vibe Coding - Frontend Design（Anthropic 官方）Skill 落地实战](https://blog.csdn.net/yangshangwei/article/details/156617372)

Anthropic 官方推出的 Frontend Design Skill，正是为了用结构化能力和设计能力，填补“代码能跑”和“页面能用、看起来高级”之间的缺口。

Frontend Design 被定义为：用于创建有辨识度、可用于生产环境的前端界面，重点强调“高设计质量”和“避免通用 AI 审美”。
- 官方地址：[skills/frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design)
- [SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)

面向对象：web 组件、完整页面、甚至小型前端应用。

输出特点：
- 代码可直接运行（而不是伪代码或零散片段）。
- 有明确的设计语言，而不是无风格的“框架占位符页面”。

设计目标：
- 避免“千篇一律”的灰白布局。
- 避免明显的“AI 生成痕迹”（同质化排版、过度留白、缺乏视觉层次等）

### Claude Design

Anthropic 发布 `Claude Design`，设计师圈子里刷屏了。
- 专门给设计师用的 AI 工具，把设计思维和 AI 代码生成直接捏在一起，演示视频里随便聊几句就能出一个像样的设计稿，「这就是设计的未来」。
	
但闭源，只能通过官方 Claude 账号使用，而且额度少的可怜，用上原生 Claude design 对大多数人非常困难。

GitHub 上 开源项目
- [Open Design 项目](https://github.com/nexu-io/open-design)（作者：@Tom Huang）完全开源，Apache 2.0 协议，可自己部署，接自己的 API Key，可以改代码，可以二次开发。
- 其他


### Open Design

[Open Design 项目](https://github.com/nexu-io/open-design)（作者：@Tom Huang）完全开源，Apache 2.0 协议，可自己部署，接自己的 API Key，可以改代码，可以二次开发。
- [小红书帖子](https://www.xiaohongshu.com/explore/69f0d0cf000000003600274f)

覆盖网页设计的方方面面
- 31个技能
- 各种格式的设计原型


## ppt 制作

ppt制作技能

GitHub 上和 PPT 相关的 Skill 项目。

结论： 
- 做 PPT 这件事，已经不只是“让 AI 帮你写几页内容”了，而是分成了好几条路线。

路线
 
（1）如果做漂亮网页 PPT，优先看：
- guizang-ppt-skill：电子杂志感很强，适合发布会、分享、视觉化报告。
- next-slide：产品化程度高，零依赖 HTML，中文场景友好。
- html-ppt-skill：更像模板工厂，适合研究通用 HTML PPT 生成。
- revealjs-ppt-skill：标准 reveal.js 路线，适合技术分享、课程、文档型演示。

（2）如果你最终要的是可编辑 PPTX，可以重点看：
- anthropics/skills/pptx：官方基线型 PPTX skill。
- MiniMax-AI/pptx-generator：PptxGenJS 路线，生成、读取、编辑都比较工程化。
- powerpoint-skill：适合研究 HTML 到 PPTX 的高保真转换。
- mcp-server-ppt：更偏 Windows + Office 自动化场景。

（3）想做“高级感网页 PPT”，先看
- next-slide + guizang-ppt-skill + html-ppt-skill。

（4）想做“真正可编辑的 PPTX”，先看：
- anthropics/pptx + MiniMax pptx-generator。

（5）想把 PDF、图片、论文转成演示，可以看：
- glmv-pdf-to-ppt、image-to-pptx-skill、paper-slides 这类专用工具。        

## 流程图


### drawio 流程图

【2026-6-3】一句话绘制 drawio 流程图
- 日本开发者提供 next-ai-draw-io: [demo](https://next-ai-drawio.jiang.jp/zh), [github](https://github.com/DayuanJiang/next-ai-draw-io)，[中文文档](https://github.com/DayuanJiang/next-ai-draw-io/blob/main/docs/cn/README_CN.md)
- Next.js网页应用，与draw.io图表无缝结合。通过自然语言命令和AI辅助可视化来创建、修改和增强图表

```sh
claude mcp add drawio -- npx @next-ai-drawio/mcp-server@latest
```


## 视频制作

### video-use

【2026-5-2】video-use 用"文本优先"思路革新视频剪辑：
- 先逐词分析语音内容再针对性处理画面，自然语言指令就能完成去废话、调色、字幕全流程，还能三轮自检质量。
- 开源地址：[video-use](github.com/browser-use/video-use)。
- 中文用户建议替换Scribe为阿里FunASR并使用思源黑体。


### ppt2video

[ppt2video](https://github.com/iburn78/ppt2video)

安装

```sh
pip install ppt2video
```
使用

```py
from ppt2video.tools import *

meta = Meta(
    ppt_file='your_ppt_slide.pptx',  # Name of your PPT file
    google_application_credentials='/config/google_cloud.json'  # Location and filename of your Google Cloud service account key
)

# Run the conversion
ppt_to_video(meta)
```


### slides2video


[slides2video 在线体验](https://slide2video.app/) 上传pdf/ppt，自动生成脚本+视频

开源神器 [slides2video](https://github.com/arpith/slides2video)
- 一键将 HTML 幻灯片 / PNG 素材转为带 AI 配音的 MP4 视频，深度对接豆包 TTS，搭载海量音色库，支持方言、IP 仿音、多情感与客服专属音色。
- 依托 ffmpeg + Playwright 实现无间隙音频合成，命令行极简操作，支持断点续跑、跳过重复环节，无需专业剪辑，快速产出教学、演示、自媒体视频，零基础也能批量生成高质量有声 PPT，办公与创作效率直接拉满！


## 其他


### 算命

【2026-7-1】现在“万物皆可AI算命”，随便一个LLM都能编出命理分析，乍一听头头是道，实则全是幻觉，连最基础的日柱都能排错，后续分析更是空中楼阁。

但开源项目名 [bazi-ziwei-skill](https://github.com/dzcmemory-web/bazi-ziwei-skill) 这款 Skill 直接让AI告别“瞎猜”。
- 内核是 Yiqi 和 lunar-typescript 等开源算法库，在本地完成精准排盘，算完四柱、十二宫才把结构化数据交给AI分析，根基扎实，绝不靠猜。

三种硬核玩法：
- 1️⃣ 八字独立分析
- 2️⃣ 紫微斗数独立分析
- 3️⃣ 八字+紫微综合印证：让两套体系交叉对账，看结论是否一致，这是它最独特的增量价值。

更赞的是，分析完还能一键生成水墨风HTML命盘海报，排版雅致，可直接截图分享。

整个过程全程本地运行，无需联网，隐私保护做得非常到位。可以轻松装入 Claude Code、Codex 或 Cursor 等Agent中，通过自然语言对话即可使用。



# 结束
