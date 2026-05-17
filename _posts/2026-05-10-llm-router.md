---
layout: post
title:   LLM 算力中转站
date:   2026-05-10 16:52:00
categories: 大模型
tags: token 算力 中转站
excerpt: LLM 大模型算力中转站， 如 openrouter等
mathjax: true
permalink: /llm_router
---

* content
{:toc}

# LLM 算力中转站


## 背景

LLM 使用方式变迁

|阶段|特点|优点|缺点|
|---|---|---|---|
|初期|一个LLM模型接管所有任务|适合单一任务|① 不同模型优势不同，难以兼顾<br>② 接口不同，各家模型适配成本上升|
|中期|一个中转接口，自动适配多家LLM供应商|||
|||||

## 什么是中转站

AI中转站是聚合各类AI大模型接口的“智能枢纽”
- 相当于AI算力行业的“变电站”，核心作用就是“汇聚、转化、调度”。

中转站内置了GPT、image2、seedance、wan、AIPDD等各类主流AI模型的接口，根据用户需求，自动判断需要调用哪些模型、如何协同运作，实现全流程自动化衔接。比如门店短视频创作，用户只需在AI中转站输入核心需求——“生成门店同城短视频，突出优惠活动与同城定位”，中转站就会自动调度GPT生成提示词、image2生成素材、seedance生成视频、AIPDD完成剪辑，全程无需人工干预。更关键的是，用户只需在AI中转站进行一次充值，就能统一支付所有模型的使用费用，无需分别给各个模型充值，极大降低了使用成本与操作门槛。

AI中转站的性价比优势突出。
- 目前市面上的AI中转站，大部分由各类模型代理商搭建运营，这些代理商通过批量采购模型算力，能够拿到比官方更优惠的价格，进而将优惠传递给终端用户——这就像变电站通过集中采购电力，能够以更低的价格向用电终端供电，让用户以更低成本享受服务。

因此，很多AI中转站的模型使用价格，比官方官网价格还要便宜，这也是其能够快速普及的核心原因之一。

【2026-5-7】[傅盛孙宇晨都来了，AI 中转站的水有多深？](https://zhuanlan.zhihu.com/p/2035640384223699776)
- `孙宇晨`带着 [B.AI](https://b.ai/) 平台杀进 AI API 中转站，1:1 充值补贴，全网底价，口号简单粗暴："Why so cheap？Because we're paying for it."
  - 花 456 万美元拍下巴菲特午餐又放鸽子的男人。
  - 币圈风口没有他落下过的——TRX、NFT、DeFi
- `傅盛`，猎豹移动 CEO、360 早期核心、TikTok 早期投资人。推出 [Easy Router](https://easyrouter.io/)，聚合 40 多个全球模型，零平台费、零加价，打着"正版无兑水"的旗号。

两个完全不同世界的人，同时盯上了同一个生意：把 OpenAI、Anthropic、Google 这些海外大厂的 AI 模型 API，拆开、打包、转卖。

海外模型接入的三道坎：
- 支付——外币卡、美元账单、汇率损耗；
- 网络——域名不通、超时断流、IP 被封；
- 账号——注册风控、手机验证、一跳就封。

对常年科学上网的极客不是问题。但对想用 Cursor 写代码的国内开发者，或者接 GPT 到自己产品的创业团队，这就是真实痛点。

![](https://pic3.zhimg.com/v2-641f83cba10751781a79aadba08ed40a_1440w.jpg)

中转站在用户和官方之间，人民币充值，拿 API 密钥，填进工具 —— 调用 GPT、Claude、Gemini，体验和直连官方一样。技术上就是一层**代理**，AI 版本的代购。


## 盈利模式

盈利模式总结

![](https://pica.zhimg.com/v2-5e787d20ecfe36cb71fe1cfdd5fd6ad4_1440w.jpg)

### 正经模式

- （1）地区价格差
  - 用低价区账号订阅，按国内价转卖——光这一手，利润率已经很夸张。
  - ChatGPT Plus 阿根廷区约 5 美元，美国区 20 美元，差四倍。
- （2）API 速度差
  - 再用 Batch API（半价、24 小时返回）处理不急的请求，收用户全价。用户只觉得慢了一点，不知道自己正在排队为站长省钱。
- （3）账户共享
  - 一个 Claude Max 账号月费 200 美元，拆 20 人共享，每人收 50，收入 1000，成本就一个号。几百个号，上万用户，月入过百万。


### 灰色地带

灰色地带
- 模型偷换。 付 Opus 的钱，后台跑 Haiku。研究测试发现近 50% 中转站存在模型掺水，性能差距最高达 40%。接口兼容，名字一样——普通用户很难察觉。
- Token 虚报。 实际 1000 Token，显示 1500。用户没法独立核算，纯信息差收割。
- OAuth Token 套利。 网页版免费有额度，截下 OAuth Token 做转发，免费额度包装成 API 卖，溢价 3—10 倍。你花钱买的，是本应免费的东西。

如何验证中转站有没有偷工减料？

同一个复杂任务，中转站跑一遍，官方直连跑一遍，对比结果。比如复杂代码重构或经典逻辑推理题。差距明显，你的站大概率在掺水。已经有开发者开源了 13 步自动化审计工具，重度用户可以自己跑一遍。

最核心底线：
> 如果用 Cursor、Claude Code、Codex 这类能在**本地执行命令**的工具——不要填中转站的 Key，填官方。铁律，没有例外。


## 问题

不管小站偷换模型，还是大佬截流数据——顶多是让你多花了冤枉钱，或被默默采集了信息。接下来的，才真正值得认真对待。
- （1）**数据透明**：对话对站长一览无余
  - 用户数据对站长完全透明。 每一条消息、每一行代码、每一个商业策略，都能被看到。它不是 OpenAI，没有隐私协议，没有监管约束，没有品牌信誉要维护。
  - 有些免费中转站的商业模式就一句话：用你的数据付账。
- （2）**代码注入**：一行代码就能偷走你的 ETH
  - 对于开发者，危险在一行代码之内。 UCSB 今年 4 月测试了 400 多个中转站，9 个在返回内容中注入恶意代码，1 个直接转走了测试钱包里的 ETH。
  - 怎么做到的？让 Cursor 或 Claude Code 写一段代码，正规模型老老实实返回，中转站在返回数据里悄悄**夹带**额外指令。本地工具没有验真伪的机制，收到就执行。AI 建议安装某个库，中转站把包名改掉一个字母，你不细看敲了回车——后门就进了你的系统。

如果你用 AI 处理客户信息、公司代码、或任何不想外泄的内容，走中转站是需要认真想清楚的决定。纯聊天无所谓，一旦 AI 能碰你的文件系统，你等于把后门交给了没有任何信用背书的算力二道贩子。

![](https://pic3.zhimg.com/v2-f60ef059496b6351d169b016f858f774_1440w.jpg)

## 应用

不同应用场景下，中转站选型

| 数据类型 | 风险等级 | 使用建议 |
|---|---|---|
| 公开信息、日常闲聊 | 低 | 用中转站问题不大，风险可控 |
| 工作文档、非敏感代码 | 中 | 选运营超一年、有公司实体的口碑老站；先充10元试用一周，验证速度、效果、模型真实性后再继续 |
| 商业机密、用户数据 | 高 | 走官方直连或云厂商，不要经手中转站，中转站技术层面可查看全部内容 |
| 密钥、密码、私钥 | 极高 | 无论任何渠道，永远不要发给任何AI |



## 实现

### 【2026-5-7】b.ai

`孙宇晨` [B.AI](https://b.ai/)小九九，五步：
- 先用中转站做入口，补贴拉用户；
- 再推"孙哥大脑"，一键加载所谓"孙宇晨视角"的交易逻辑；
- 然后 BAIclaw 上线，从回答升级为执行交易；
- 绑定钱包地址，沉淀用户画像；
- 最后积分、等级、空投——标准 Web3 收割剧本。
- 他做的不是中转站，是以中转站为入口的 Web3 生态闭环。

![](https://pica.zhimg.com/v2-2863930024e9aad56474bbfc1fdc1cf0_1440w.jpg)


### Easy Router

`傅盛` 推出 [Easy Router](https://easyrouter.io/)，聚合 40 多个全球模型，零平台费、零加价，打着"正版无兑水"的旗号。

Easy Router 主打"零加价、正版无兑水"，瞄准愿意为稳定性付费的用户。

但上线没几天被打脸 —— 套壳开源项目 new-api，删了原作者信息就当自研推广。他否认，原作者当场挂了他。纳斯达克上市公司 CEO 需要用这种方式抢跑，窗口在加速关闭。

大佬们要的根本不是 API 差价
- "傅盛宣称正版无兑水，水到渠成获得高收入人群的高质量上下文数据。得上下文者得天下，数据生意的价值远比倒卖差价更长久。"

卖 Token 赚快钱，截流海量用户的代码逻辑、技术选型、商业策略，才是真正值钱的东西。


### OpenRouter

[OpenRouter](https://openrouter.ai/) 专注于将用户请求智能路由到不同的AI模型，并提供统一的访问接口。像“路由器”，根据预设规则或用户自定义策略，将用户请求自动分配至最合适的AI模型。大大简化了与AI模型交互的过程，降低了开发者的集成复杂度。
- 申请 [Key](https://openrouter.ai/workspaces/default/keys)


#### 特点

技术特点
‌- 多模型支持‌：OpenRouter集成了来自多个提供商的模型，包括知名的闭源模型（如OpenAI的GPT-4、Anthropic的Claude等）和开源模型（如LLaMA、Mistral等）。目前支持数十种模型，未来计划扩展到数百种。
‌- 统一API‌：OpenRouter的API与OpenAI的聊天API高度兼容，用户只需更换API密钥和基础URL，就能轻松切换模型，无需修改代码。
‌- 价格与性能优化‌：OpenRouter通过比较不同模型的定价和性能，帮助用户找到性价比最高的选项。它还会根据用户的需求（如低成本或高吞吐量）自动路由请求到最佳提供商。
‌- 自动路由与回退机制‌：通过“Auto Router”功能，OpenRouter会根据输入提示选择最适合的模型。如果某个模型或提供商不可用，它会自动尝试其他替代模型，确保服务不中断。

#### 接入方式

| 方式          | 适用场景                                           |
|---------------|----------------------------------------------------|
| [API](https://openrouter.ai/docs/quickstart#using-the-openrouter-api)           | 完全掌控流程、支持任意编程语言、不想引入依赖项  |
| [客户端 SDK](https://openrouter.ai/docs/quickstart#using-the-client-sdks)    | 类型安全（Type-safe）的模型调用、追求极低性能开销            |
| [Agent SDK](https://openrouter.ai/docs/quickstart#using-the-agent-sdk)     | 构建具备工具调用、循环逻辑与状态管理能力的智能体  |

三种主流接入方式的对比，核心差异是「控制自由度」和「封装层级」：
- API：最底层，自由度最高，需自己处理所有逻辑；
- Client SDK：中等封装，简化了模型调用，兼顾性能与易用性；
- Agent SDK：最高级封装，直接提供智能体开发的完整框架。

claude code 一句话安装
> Read https://openrouter.ai/skills/create-agent/SKILL.md and follow the instructions to build an agent using OpenRouter.


API方式

```py
import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer <OPENROUTER_API_KEY>",
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-OpenRouter-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "openai/gpt-5.2",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)
```


OpenRouter SDK 方式

```py
from openrouter import OpenRouter
import os

with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
    response = client.chat.send(
        model="openai/gpt-5.2",
        messages=[
            {"role": "user", "content": "What is the meaning of life?"}
        ],
    )
    print(response.choices[0].message.content)
```


OpenAI SDK方式调用

```py
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="<OPENROUTER_API_KEY>",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-OpenRouter-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  model="openai/gpt-5.2",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)

print(completion.choices[0].message.content)
```


### LiteLLM

[LiteLLM](https://www.litellm.ai/) 开源AI网关，支持 100+种模型，可部署、企业级，用OpenAI接口格式访问LLM
- GitHub [litellm](https://github.com/BerriAI/litellm), 官方文档 [litellm doc](https://docs.litellm.ai/docs/)

![](https://docs.litellm.ai/assets/ideal-img/hero.c044955.1920.png)

LiteLLM 提供统一标准化接口，支持以 OpenAI 调用格式接入超百款大语言模型，包括 OpenAI、Anthropic、Vertex AI、Bedrock 等主流模型。
- 只需使用同一套 completion() 接口，即可调用任意厂商模型，无需逐个重新学习各家 API
- 无论选用哪家服务商、哪款模型，输出格式始终统一
- 内置路由调度能力，支持多部署环境自动重试、故障降级兜底
- 可自建大模型网关（代理服务），支持虚拟密钥、成本统计及管理后台可视化界面


安装 python sdk

```sh
uv add litellm
```

使用

```py
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"

# OpenAI
response = completion(model="openai/gpt-4o", messages=[{"role": "user", "content": "Hello!"}])

# Anthropic  
response = completion(model="anthropic/claude-sonnet-4-20250514", messages=[{"role": "user", "content": "Hello!"}])
```

AI Gateway 代理服务器

```sh
uv tool install 'litellm[proxy]'
litellm --model gpt-4o
```

使用

```py
import openai

client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```


# 结束

