---
layout: post
title:  ChatGPT应用
date:   2023-03-30 19:10:00
categories: 大模型
tags: AIGC ChatGPT 智能客服 加密 搜索 推荐 排序 标注 yolo 豆包 cici coze 贾扬清
excerpt: ChatGPT应用思考
mathjax: true
permalink: /chatgpt_application
---

* content
{:toc}


# ChatGPT应用

OpenAI CEO奥特曼那句AI版摩尔定律：
> 宇宙中的智能数量每18个月翻一番。

- 模态：文本，语音，图像，视频，建模，策略，跨模态…
- 产业：传统，新兴，机器人，脑机…

从一个风靡全球的AI玩具到独具潜力的赚钱法宝，对话机器人ChatGPT仅仅用了不到半年。
- 微软联合创始人比尔·盖茨称GPT是“40多年来最革命性的技术进步”
- 英伟达创始人黄仁勋高呼：“我们正处于AI的iPhone时刻”
- 阿里董事会主席兼CEO张勇也说：“所有行业都值得用大模型重做一遍。”

## ChatGPT 大事记

ChatGPT2022年12月发布，但真正火到出圈，是春节后，尤其是3月之后的事情了。ChatGPT一石激起千层浪，过去的3月可能是LLM领域最为[波澜万丈的一个月](https://zhuanlan.zhihu.com/p/619567516?)。
- 3月1日，OpenAI发布ChatGPT API
  - OpenAI不止发布了ChatGPT的API，还发布了新版的Whisper（一个语音识别模型）的API。主角当然还是ChatGPT了，借助API各类相关应用如雨后春笋一般出现，例如 ChatPDF，ChatPaper等等。同时还有API定价，居然和GPT3差不了多少，再次印证了那个假设：ChatGPT的参数量应该和GPT3差异不大。
- 3月8日，Facebook的LLaMA模型被“泄露”
  - LLaMA是Facebook于2月24日“开源”的大模型，包含了多个不同参数量的预训练的模型。最初这个模型是需要向Facebook申请并遵守License才能获取到的，后来惨遭“泄漏”，现在可以从HuggingFace中直接下载。
  - LLaMA-13B不仅在大多数benchmarks上超过了GPT-3，证实百亿参数的预训练模型作为基座，有所作为。
- 3月10日，HuggingFace发布peft的0.2.0版本
  - peft是HuggingFace开发的一个参数高效的微调库（Parameter-Efficient Fine-Tuning）。此次发布特别提到了Whisper large tuning using PEFT LoRA+INT-8 on T4 GPU，HuggingFace要打造大模型微调标准库的野望。HuggingFace原本定位是预训练模型届的github，用户需要实现什么功能，就要到HuggingFace的平台上去找对应任务的模型。如今ChatGPT已经出来了，一个模型可以解决几乎所有NLP问题，HuggingFace作为模型平台看起来就感觉用处不大了，所以不难理解HuggingFace的危机感。
- 3月13日，斯坦福发布Alpaca 7B
  - Alpaca-7B是斯坦福发布的基于LLaMA-7B继续微调得到的模型。训练所用的52K的instruction-following demonstrations，通过调用text-davinci-003(GPT3.5)得到。
  - 最终实验结果表明Alpaca-7B的表现和text-davinci-003相似，整个训练花费仅有不到600美元。Alpaca-7B的出现，证明了用很小成本也是可以一定程度上可以复现大模型的表现，极大地振奋了整个开源社区的信心。此后不久，基于lora等参数高效的微调方法，开源社区很快实现了在单张显卡、消费级显卡的训练。
- 3月14日，OpenAI发布GPT4
  - GPT4相对于GPT3/3.5的改进集中在两点：一是支持**多模态**理解，以前只允许输入文字，现在也可以支持图片作为输入；另一点则是GPT4的**逻辑推理**能力得到进一步增强，很多用户经过测试也证明了这一点。
  - GPT4的发布并没有像GPT1/2/3/3.5那样有对应的论文，OpenAI只发布了一篇技术报告，报告中没有提到任何训练的细节，例如训练集的构造方法、训练消耗的电力、learning rate/epoch count/optimizer等超参...OpenAI声称不公布的原因是“the competitive landscape and the safety implications of large-scale models”，但并不妨碍OpenAI被调侃为“CloseAI”。
- 3月15日，清华发布chatglm-6b
  - ChatGLM-6B是一个清华开源的、支持中英双语的对话语言模型，基于GLM架构，具有62亿参数。结合模型量化技术，ChatGLM-6B可以在消费级的显卡做模型的推理和训练，对于缺卡缺钱的研究团队来说非常有用。毫无疑问，这是当前中文领域最为活跃的开源大模型，截至目前（2023.4.2），huggingface上ChatGLM-6B的下载量达到了33万。
- 3月16日，pytorch2.0发布
  - 在众多算法产品和技术的璀璨之下，pytorch2.0的发布不那么突出了。这次2.0版本最重要的特性之一是把torch.**compile**作为主API，此外还针对性能做了很多优化。遥想2020年初那会，tensorflow的2.0版本也是刚刚发布，彼时大多数公司借着把骨干网络换成transformer的时候，就把深度学习框架也换成了pytorch，顺带也带来了HuggingFace的蓬勃发展。
- 3月16日，百度发布“文心一言”
  - 百度发布的“文心一言”，号称中文版的ChatGPT。但是发布会上百度CEO李彦宏也坦言，“文心一言要对标GPT-4，这个门槛还是很高的。文心一言并不完美，之所以现在要发布，原因在于市场有强烈需求。”
- 3月23日，OpenAI发布ChatGPT Plugin
  - OpenAI发布的ChatGPT Plugin提供一种大语言模型应用特定领域知识或者能力的新思路。在这之前的应用开发商例如ChatPDF，思路都是调用ChatGPT的API，再结合开发上自由的能力，整合为一个产品提供给用户。而ChatGPT Plugin实现了一种依赖的翻转，首先开发商提供API给ChatGPT，再由ChatGPT决定何时以及如何使用这些API，这些API就是所谓的“插件”。在这种模式下，用户的交互全部都在ChatGPT中完成，可谓是“肥水不流外人田”。
- 3月29日，众多大佬签名反对下一代大模型的开发
  - 众多大佬签名了公开信，反对下一代大模型的研发，号召AI实验室在至少未来6个月内，暂停训练比GPT4更强的大模型。《全球通史》中，斯塔夫里阿诺斯有一个核心的观点：“在技术变革和使之成为必需的社会变革之间,存在一个时间差。造成这个时间差的原因在于:技术变革能提高生产率和生活水平,所以很受欢迎,且很快便被采用;而社会变革则由于要求人类进行自我评估和自我调整,通常会让人感到受威逼和不舒服,因而也就易遭到抵制。社会变革滞后于技术变革一直是人类许多灾难的根源。”将来回望历史时，2023年的3月毫无疑问是一段技术大变革的爆发期，但是与之相匹配的社会变革，或许我们接下来还要探索很长时间。

## ChatGPT 商业化

### 行业观察

【2023-5-7】陆奇：新范式新时代新机会, [完整ppt](https://miracleplus.feishu.cn/file/TGKRbW4yrosqmixCtprcUlAynzg)，[ppt+笔记](https://miracleplus.feishu.cn/docx/Mir6ddgPgoVs3KxF6sncOUaknNS)

【2023-5-25】传TikTok正在测试名叫TAKO的聊天机器人。
- 目前TikTok正在测试一款名叫`TAKO`的人工智能聊天机器人，该机器人可以与用户进行**短视频**对话，并能帮助他们发现新创作内容。
- 据悉，该聊天机器人以一个鬼魂形状的图标突出显示在应用界面上，用户在观看视频时，可以点击它进行基于文本的对话并寻求帮助并找到合适的内容。

监管
- 4 月 11 日，网信办发布《生成式人工智能服务管理办法（征求意见稿）》公开征求意见的通知。
- 同日，美国商务部下属的国家电信和信息管理局 （NTIA） 宣布征求公众意见，关于如何制定人工智能问责措施。
- NTIA 负责人艾伦·戴维森（Alan Davidson）对《卫报》表示，美国立法者 2021 年提出 100 多项人工智能相关法案，“这跟社交媒体、云计算甚至互联网早期有很大不同”。
- 当地时间 5 月 16 日，OpenAI CEO 山姆·阿尔特曼（Sam Altman）首次参加美国国会听证，呼吁政府制定监管 AI 的措施。

### 创业公司

【2023-5-30】[大模型创业潮：狂飙 180 天](https://mp.weixin.qq.com/s/yodYn8oXDtHEzyRFZrICuw)

陆奇在近期演讲中，给出中国大模型发展第一阶段的标准：
> 谁先达到 GPT-3.5 水平，谁将能进入第一梯队。在此之前，许多事要从零做起。

【2023-5-27】大批高管离职投身大模型创业
- 1、千挂科技CEO`陶吉`已离职，曾任百度自动驾驶负责人。
- 2、Momenta 副总裁 `Charles Wang`离职，或进行大模型创业。
- 3、阿里研究员（P10），`吴翰清`离职，投身AI短视频创业。
- 4、淘宝技术部担任商品3D重建及AI设计算法负责人`贾荣飞`离职。
- 5、小红书AI平台负责人`颜深根`离职。
- 6、原百度副总裁`马杰`加入创新工厂做大模型。

国内估值最高的两家创业公司是`光年之外`和 `MiniMax`

MiniMax 公司名字取自一种算法，2021 年 12 月成立, 合作方有不少知名公司：
- 已有文本、语音、视觉 3 个模态的自研基础模型。
- 2023 年 3 月，MiniMax 推出面向企业用户的 API 开放平台，支持文本和语音模型的服务调用。
- 4 月 18 日，火山引擎总裁谭待在发布会上专门提到 “火山引擎上跑了抖音，也跑了 MiniMax”
- 金山办公发布 WPS AI，CEO 章庆元介绍其底层大模型由 MiniMax 提供。

MiniMax 团队成员大多出生在 1990 年代。多位创投人士认为，开始大模型创业的最佳年龄在 **35 岁以下**。
- 大模型技术更新速度 “以天计算”，年轻人能更快迭代认知，并且知识结构不陈旧

云启资本合伙人陈昱学计算机出身，他指出机器学习领域近年有两个里程碑式进展：
- 2012 年 CNN 架构爆发
- 2017 年 “所有人一边倒地去搞 Transformer 架构”，GPT、BERT、LLaMa 等主流大模型都基于 Transformer。

新技术已经覆盖和超越传统 NLP 技术
- “一个人在不同年份开始接触机器学习，知识结构完全不一样。”
- “早年的知识不是经验，而是累赘。”

多位创业者认为
- 考虑 2C 商业模式、监管等因素，ChatGPT 在国内并不是最适合的产品形态。
- 王慧文愿意尝试 “Chat” 这个已经被充分验证的机会，但他更强调 “keep open-minded”，别在起跑时就笃定哪一条路是正确的。

2B or 2C
- 周明: 2B 和 2C 是完全不同的两条路，打算两者都做的创业者属于 “没想明白”。
  - 坚定选择 2B，做针对特定领域的专用大模型，“节奏慢但是更务实”。
  - 2C 像是一条 “不归路”。2C 需要把语言理解能力和做各种任务的能力放在一个模型里，相应地模型参数规模必须大，未来会进入参数规模、数据量和算力的军备竞赛。
- 而 MiniMax 和 深言科技 都认为: 现阶段大模型可以在通用场景发挥价值，2B 和 2C 的市场需求都能满足，不会刻意区分。
- 李志飞选的方向是 to “professional consumer”，用户是 “产消者”。他们希望为创造某些内容而消费的个体提供 AIGC 工具
  - 出门问问曾以 AI 识别为重点，但困难重重。做 2C 的语音助手时，很难满足用户的期望。尽管语音识别、语音合成等基础技术很成熟，但一个语音助手产品包括自然语言理解、对话、数据查询等 8 个环节。
  - 2020 年的 CES 国际消费电子展得到启发, 看到极高画质渲染出来的数字人 Neon。第一次被 AI 生成的体验震撼。回去后，他调整研发重点，带团队开始投入生成式 AI
  - 不久后，带团队研发的 AI 配音平台 “魔音工坊” 带来让他惊喜的利润。
  - 2023 年 4 月，出门问问发布基于自研大模型发布 AI 写作应用 “奇妙文”，“魔音工坊” 等应用也开始与大模型整合。

- 2C 产品，帮助它们和人的价值观对齐
  - 聆心智能创始人黄民烈：
    - 设计的一个重要规则：当情感陪伴类产品识别出用户有危险行为时，机器能以符合专业干预技术的方式施行紧急援助。
- 2B 产品，引入专家知识和规则帮助它们表现得更准确。
  - 第四范式于 4 月底首次公布 “以生成式 AI 重构企业软件（AIGS）” 战略，提出企业级 Copilot（助手）的进阶 “Copilot+ 知识库”。涂威威解释，第四范式 “培养” 出大模型的基础能力，等它进入企业后，接上内部知识库就能 “自学”，更准确地理解任务、知道什么工作该调用什么资源，输出结果也能溯源，“像一位董秘”。

【2023-3-20】[李开复正在筹组AI2.0公司，不只要做中文版ChatGPT](https://finance.sina.cn/tech/2023-03-20/detail-imymnsya3432523.d.html)

李开复称：
> “Project AI 2.0不仅仅要做中文版ChatGPT。 我认为AI 2.0不仅仅是个高能聊天工具，也不仅仅是图文创作的AIGC生成，Co- pilot和如今看到的应用都还只是AI 2.0能力的开端。”

李开复：
- 在AI方向，已经塔尖孵化了7家公司，包括成立4年就成为港交所“AI＋制造”第一股的`创新奇智`，`澜舟科技`、`呈元科技`等，`ProjectAI 2.0`是第7家。

### 教人如何挣钱

【2023-4-11】国内靠ChatGPT挣钱的[第一波人](https://www.toutiao.com/w/1762574053066767)，主要教别人怎么靠ChatGPT挣钱的。快速包装交付、精准找到愿意为这些信息差付费的客群
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/cb048fac14c04e40914e28fbe538da2f~tplv-obj:823:813.image?_iz=97245&from=post&x-expires=1688947200&x-signature=LMhWJtDCvvO44zYNtOtnKVj%2BnQQ%3D)

评论
> 有钱赚他自己不赚，也不教给他父母兄弟姐妹去赚，他教给陌生的你？

#### ChatBase

【2023-5-28】[ChatGPT 造富“神话”：大四学生放弃大厂去创业，半年后月收入45万](https://mp.weixin.qq.com/s/IS5NvCAzs0q4Xi5ABfszFQ)

埃及大学生[Yasser](https://twitter.com/yasser_elsaid_)在 Meta 和 Tesla 等大厂实习半年后，其创办的聊天机器人公司就已经稳定月收 6.4 万美元（约合 45 万人民币），而且自首次上线以来，业务流量从未下滑缩水。
- Chatbase 市场定位并不复杂，也没做过验证或者商业调查。毕竟 AI 这个领域才刚刚诞生，对我来说‘用 ChatGPT 处理数据’肯定有搞头，能帮助许许多多用户解决实际需求
- Chatbase 最初其实是想做成一款处理 PDF 的 ChatGPT 工具，这是 Yasser 当时想到的最直观的用例。比如用户可以上传一份 PDF，然后让 ChatGPT 总结一下其中的内容。
- 第一个版本花了两个月时间，2023 年 2 月 2 号，Yasser 发布给了 Twitter 上的全部 16 个关注者，结果一下子就火了，巨大的商机，Yasser 马上中止了在校课业，把所有时间和精力都集中在 Chatbase 上

[Chatbase.co](https://www.chatbase.co/) 是一款为网站构建自定义 ChatGPT 界面的工具，用户只需上传**文档**或添加到**网站链接**，就可以获得一个类似 ChatGPT 的聊天机器人，并将它作为小组件添加到网站上。

Yasser 用 React、Next.js 和 Supabase 来构 web 应用。Yasser 还在应用的 AI 部分使用了 OpenAI 的 API、Langchain 还有 Pinecone。付款部分用的是 Stripe。目前这套技术栈运行得不错，但后续 Yasser 可能需要做些调整来控制成本，比如尝试不同的 Vector 数据库或者托管选项

可集成到自己的网站, 官方提供[看板配置](https://www.chatbase.co/chatbot/zNSQTQvqYJYf0rb0V-wYX/dashboard)
- 示例：[test](https://www.chatbase.co/chatbot/zNSQTQvqYJYf0rb0V-wYX)
- 国外介绍：[How a college student reached $64,000/mo in 6 months by being an AI first mover](https://www.indiehackers.com/post/how-a-college-student-reached-64-000-mo-in-6-months-by-being-an-ai-first-mover-ba7981f6e1)

### Prompt 编写

Prompt是在ChatGPT中输入的一些关键词，按照用户意愿生成出各种各样的内容，提高工作效率。
- Prompt的好处是不仅可以大大减少思考时间，还可以让创造力更加丰富多彩。

详见站内专题：[ChatGPT提示工程](https://wqw547243068.github.io/chatgpt#%E6%8F%90%E7%A4%BA%E5%B7%A5%E7%A8%8B)

#### AIPRM

有人组织了社区来工具化优质prompt，集人类智慧形成普惠大众的工具 —— AIPRM， 自动生成优质Prompt的工具
- AIPRM 全称：Artificial Intelligence Project Resource Manager
- 要解决的问题就是通过社区互助提高使用AI产品的生产力（比如chatGPT）
- ![](https://pic3.zhimg.com/80/v2-24a428805505f96e183f040cf2397e02_1440w.webp)
- ![](https://pic2.zhimg.com/80/v2-423bc023da6630c8cdd0cacaabd88145_1440w.webp)

【2023-4-11】[终极写作工具：小白也会用的ChatGPT Prompt提示综合指南](https://zhuanlan.zhihu.com/p/611365958)
- [AIPRM](https://www.aiprm.com/)
- Chrome 插件：[aiprm-for-chatgp](https://chrome.google.com/webstore/detail/aiprm-for-chatgpt/ojnbohmppadfgpejeebfnmnknjdlckgj?hl=en)

### 点子

【2023-5-13】ChatGPT各类应用idea汇总，包含场景、当前解法、解决状态等，持续更新
- [飞书文档](https://bytedance.feishu.cn/sheets/TcHTsRSczhda3BtpLQ4cMeVNnSf)



## ChatGPT 行业应用

ChatGPT 非常实用，能帮助普通人节省不少脑力和时间成本。
- 回答后续问题、承认错误、挑战不正确的前提、拒绝不适当的请求。

ChatGPT在办公软件、社交文娱、营销广告、家庭助理四大方向的15条赛道，AI大模型技术正出现落地的萌芽。其中不仅有国民级的Office工具、钉钉等协同办公平台接入大模型，还有来自办公、电商、家居、社交文娱互联网平台推出AIGC功能，甚至以智能汽车、AR眼镜为代表的实体终端也上了大模型，带来新奇体验。

【2023-5-11】生成式AI创业领域
- ![](https://pic3.zhimg.com/80/v2-bdd24bc6e1db0c18c5d8f616dcc578be_1440w.webp)
- [全面接入！ChatGPT杀进15个商业应用，让AI替你打工](https://zhuanlan.zhihu.com/p/628096018)

2023 年是 AI 跳变式发展一年：
- ChatGPT 成为史上最快突破 1 亿用户的超级应用；
- Perplexity 用“问答引擎”撬开了 Google 在内容搜索上的强势；
- GPT-4 的发布定义了 LLM 军备竞赛的决赛门槛是什么；
- Runway、Pika 以及以及 VideoPoet 为模型带来更多形态智能能力；
- Llama 2 和 Mistral-7B 是开源势力带给社区的惊喜；

### 受益方

相关受益方
- 上游增加需求
  - 算力芯片、数据标注、自然语言处理（NLP)等。
- 下游相关受益应用，包括但不限于： 
  - 无代码编程、小说生成、对话类搜索引擎、语音陪伴、语音工作助手、对话虚拟人、人工智能客服、机器翻译、芯片设计等。
- 功能（C端）
  - 一款激起新鲜感的**新奇玩具**，也是一款消磨无聊时光的**聊天高手**，也能成为生产力爆表的**效率工具**，更可以被用作上通天文下知地理的**知识宝库**。
  - ChatGPT不仅在日常对话、专业问题回答、信息检索、内容续写、文学创作、音乐创作等方面展现出强大的能力，还具有生成代码、调试代码、为代码生成注释的能力。
- ![img](https://pic2.zhimg.com/80/v2-b9ad448881e01271b30377a2be17caad_1440w.webp)

人们源源不绝地挖掘ChatGPT的更多技能，包括替写代码、作业、论文、演讲稿、活动策划、广告文案、电影剧本等各类文本，或是给予家装设计、编程调试、人生规划等建议。
- ![49个功能](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TV46RMq7ttyVO3~noop.image?_iz=58558&from=article.pc_detail&x-expires=1676360394&x-signature=PDoTaKf5nJWW3eO5rMA8a0GzyCw%3D)

ChatGPT也可以与其他AIGC模型联合使用，获得更加炫酷实用的功能。这极大加强了AI应用与客户对话的能力，使我们看到了AI大规模落地的曙光。
- 通过对话生成客厅设计图。
- ![](https://pic2.zhimg.com/80/v2-cda1af4d2f17bd11dce94cafd580dd61_1440w.webp)

【2023-3-2】[普通人如何用ChatGPT搞钱？](https://mp.weixin.qq.com/s/2vPOOsesAh8d5SUZqvVKgA)
- 1、让ChatGPT写小说
  - 著名大V半佛仙人表示人家已经提前试过，效果并没有那么理想：
- 2、让ChatGPT做培训
  - 其他行业我不清楚，但在计算机行业，用ChatGPT来指导学生写代码，纠正代码问题还是效果不错的，把ChatGPT包装成一个虚拟的培训老师，很有想法。
- 3、山寨版ChatGPT
  - 高能提醒: 违法! 发出来只是让大家提高警惕，别花冤枉钱被骗了！
  - 有人在想着怎么用ChatGPT搞钱，而另外有人在想着：你们这么想用ChatGPT，如何利用这一点搞钱！
- 4、让ChatGPT来做自媒体
  - 大家刷短视频的话，经常看到模板化的套路，几句话，几分钟视频，看得人暴多。以后有了ChatGPT帮忙写稿，批量化做视频，一个人搞一堆短视频自媒体账号根本不是问题。
- 5、开发一个ChatGPT面试系统
  - 现在很多公司都允许远程面试，比如电话面试、视频面试，有人想到用这玩意来面试，接入一个语音识别，就可以实时帮助求职者通关面试了：
  - 开发这么一个系统，你觉得会有市场吗？基于这个想法，还可以开发一个ChatGPT写作文系统、写简历系统、做PPT系统，以后说不定一堆淘宝卖家提供这样的服务。

随着ChatGPT的不断迭代，以及国内外各大厂商的跟进，2023注定要掀起人工智能新的一波热潮。咱们程序员除了学习技术之外，也可以想想怎么在安全合法的情况下，利用这些AI做出一些有意思的东西，说不定就火了呢。

### 商业变现

方案
1. 卖账号；
2. 部署公众号，用户免费使用N次，分享海报，带来新关注，每个关注送N次；
3. 部署小程序，用户免费使用N次，关注公众号可以送N次，每看一次激励视频可以送1次；
4. 帮助其他人部署公众号/小程序，每个收费；
5. 垂类产品，基于 ChatGPT 提供的能力，输出内容，卖内容或者卖服务
6. 内容站点，收集热门搜索词，用 ChatGPT 提供的内容给搜索引擎收录，赚广告费；
7. ChatGPT 机器人接入，收费。
8. 创作类：总的来说，可以达到九年义务制教育的及格水平

【2023-1-24】ChatGPT创业实践，[自宅创业 - #27 蹭热点的ChatGPT小程序](https://blog.guyskk.com/notes/onebiz-27)
- 批量注册、卖opengai账号：做ChatGPT小程序，上线当天用户量突破1000，第一次做出这么火爆的产品
  - 一个写程序批量注册，一个负责销售，收益分成。写好了程序，注册了一批ChatGPT账号，赚了一点钱。然后发现市场上ChatGPT账号价格越来越低，也很难批量销售出去。
- 开发ChatGPT小程序
  - 做一个小程序，把ChatGPT的功能做到小程序上，打开就能直接用。不到3天小程序急速完成上线，上线当天用户量就突破1000，涨势非常好。正预想着日活过万，然后小程序就被举报封了，发布的两个小程序同时被封。举报人和我正好同在一个微信群里，虽然很难过，但还是接受了现实，大家都按丛林法则生存。



### 应用图谱

大模型冲击下，各行各业稳定性：
- 广告 ＞ 推荐 ＞ 搜索 > NLP应用

#### 应用概览

三层：模型层→模态层→应用层
1. 模型层：文本领域（GPT系列）、图像领域（扩散模型系列）、视频、建模、多模态等
2. 模态层：文本、语音、图像、视频、行为、理解、策略、工具等，其中文本和图像最为惊艳
3. 应用层：智能对话、AI作画最为亮眼，传统行业正在被逐步颠覆，如搜索、问答、智能办公、内容创作，同时，应用商场、互联网、数字人等也被波及。

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-04-06T07:14:39.689Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36\&quot; etag=\&quot;0XdEvCbMGYhgqR8BkdSM\&quot; version=\&quot;21.1.2\&quot;&gt;\n  &lt;diagram id=\&quot;Lw-1uFHNzwHmlxUDpAkU\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;795\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-1\&quot; value=\&quot;AIGC应用概览\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontSize=19;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;390\&quot; y=\&quot;90\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-8\&quot; y=\&quot;-3\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-2\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;labelBackgroundColor=none;fontSize=10;fillColor=#f5f5f5;dashed=1;strokeColor=#666666;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;60\&quot; y=\&quot;150\&quot; width=\&quot;690\&quot; height=\&quot;440\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-3\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;dashed=1;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;250\&quot; y=\&quot;240\&quot; width=\&quot;370\&quot; height=\&quot;260\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;fillColor=#f8cecc;strokeColor=#b85450;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;352.38\&quot; y=\&quot;330\&quot; width=\&quot;145.25\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-5\&quot; value=\&quot;GPT模型\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;350\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-6\&quot; value=\&quot;扩散模型\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; y=\&quot;350\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-7\&quot; value=\&quot;跨模态模型\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;410\&quot; y=\&quot;385\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-8\&quot; value=\&quot;模型层\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontSize=13;fontStyle=1;fontColor=#6666FF;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;374\&quot; y=\&quot;404\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-9\&quot; value=\&quot;模态层\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontSize=13;fontStyle=1;fontColor=#6666FF;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;294.5\&quot; y=\&quot;329\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-8\&quot; y=\&quot;-5\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-10\&quot; value=\&quot;应用层\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontSize=13;fontStyle=1;fontColor=#6666FF;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;100\&quot; y=\&quot;160\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-5\&quot; y=\&quot;4\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-11\&quot; value=\&quot;文本\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcd28;strokeColor=none;shadow=1;gradientColor=#FFB570;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;333.5\&quot; y=\&quot;270\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-12\&quot; value=\&quot;图像\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcd28;strokeColor=none;shadow=1;gradientColor=#FFB570;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;460\&quot; y=\&quot;270\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-13\&quot; value=\&quot;语音\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcd28;strokeColor=none;shadow=1;gradientColor=#FFB570;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;258.5\&quot; y=\&quot;360\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-14\&quot; value=\&quot;视频\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcd28;strokeColor=none;shadow=1;gradientColor=#FFB570;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;530\&quot; y=\&quot;330\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-15\&quot; value=\&quot;行为\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcd28;strokeColor=none;shadow=1;gradientColor=#FFB570;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;314\&quot; y=\&quot;430\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-16\&quot; value=\&quot;策略\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcd28;strokeColor=none;shadow=1;gradientColor=#FFB570;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;480\&quot; y=\&quot;440\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-17\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.25;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-4\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-11\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;404\&quot; y=\&quot;685\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;474\&quot; y=\&quot;685\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-18\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-4\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-12\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;400\&quot; y=\&quot;360\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;374\&quot; y=\&quot;295\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-19\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-4\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-14\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;463\&quot; y=\&quot;340\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;295\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-20\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.872;exitY=1.033;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-4\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-16\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;473\&quot; y=\&quot;350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;500\&quot; y=\&quot;305\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-21\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-15\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;420\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;510\&quot; y=\&quot;315\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-22\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-4\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-13\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;493\&quot; y=\&quot;370\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;520\&quot; y=\&quot;325\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-23\&quot; value=\&quot;AI作画\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;500\&quot; y=\&quot;200\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-24\&quot; value=\&quot;搜索\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; y=\&quot;240\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-25\&quot; value=\&quot;办公\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;150\&quot; y=\&quot;290\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-26\&quot; value=\&quot;AI写作\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;330\&quot; y=\&quot;180\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-27\&quot; value=\&quot;NLP基础任务\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d0cee2;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;382.01\&quot; y=\&quot;530\&quot; width=\&quot;86\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-28\&quot; value=\&quot;智能对话\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;240\&quot; y=\&quot;190\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-29\&quot; value=\&quot;大模型\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d0cee2;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490\&quot; y=\&quot;530\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-30\&quot; value=\&quot;AI视频\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;650\&quot; y=\&quot;260\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-31\&quot; value=\&quot;数字人\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;160\&quot; y=\&quot;420\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-32\&quot; value=\&quot;游戏策略\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;570\&quot; y=\&quot;480\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-33\&quot; value=\&quot;编程\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;405\&quot; y=\&quot;180\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-34\&quot; value=\&quot;语音处理\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;130\&quot; y=\&quot;360\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-36\&quot; value=\&quot;机器人\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;170\&quot; y=\&quot;480\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-37\&quot; value=\&quot;脑机接口\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;294.5\&quot; y=\&quot;540\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-38\&quot; value=\&quot;工具\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcd28;strokeColor=none;shadow=1;gradientColor=#FFB570;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;530\&quot; y=\&quot;390\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-39\&quot; value=\&quot;数据生产\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;660\&quot; y=\&quot;355\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-40\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.75;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-4\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-38\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;508\&quot; y=\&quot;364\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;540\&quot; y=\&quot;355\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-41\&quot; value=\&quot;理解\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcd28;strokeColor=none;shadow=1;gradientColor=#FFB570;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;393.5\&quot; y=\&quot;460\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-42\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-4\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-41\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;489\&quot; y=\&quot;433\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;520\&quot; y=\&quot;450\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-43\&quot; value=\&quot;应用商城\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;650\&quot; y=\&quot;404\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-44\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;dashed=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-11\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-33\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;474\&quot; y=\&quot;340\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;500\&quot; y=\&quot;310\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-89\&quot; value=\&quot;Cursor\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-44\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.1166\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-45\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;dashed=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-11\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-26\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;280\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;220\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-46\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;dashed=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-28\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;360\&quot; y=\&quot;270\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;500\&quot; y=\&quot;230\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-86\&quot; value=\&quot;DocumentQA\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-46\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0189\&quot; y=\&quot;-2\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-47\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;dashed=1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-11\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-24\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;280\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;280\&quot; y=\&quot;230\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-94\&quot; value=\&quot;New Bing\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-47\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.2901\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-48\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;dashed=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-11\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-25\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;380\&quot; y=\&quot;290\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;290\&quot; y=\&quot;240\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-88\&quot; value=\&quot;Copilot\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-48\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0381\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-49\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;dashed=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-13\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-34\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;390\&quot; y=\&quot;300\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;300\&quot; y=\&quot;250\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-75\&quot; value=\&quot;跨语种\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-49\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.2371\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-50\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;dashed=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-15\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-31\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;400\&quot; y=\&quot;310\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;310\&quot; y=\&quot;260\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-76\&quot; value=\&quot;动作模拟&amp;lt;br&amp;gt;角色模拟\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-50\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0634\&quot; y=\&quot;-3\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-51\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=1;entryY=0.25;entryDx=0;entryDy=0;dashed=1;exitX=0;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-15\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-36\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;324\&quot; y=\&quot;455\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;240\&quot; y=\&quot;445\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-80\&quot; value=\&quot;表情控制\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-51\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0039\&quot; y=\&quot;2\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint y=\&quot;1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-52\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;exitX=0.383;exitY=1.05;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-15\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-37\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;334\&quot; y=\&quot;465\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;250\&quot; y=\&quot;455\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-92\&quot; value=\&quot;Crown\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-52\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.1603\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-53\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-41\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-27\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;344\&quot; y=\&quot;475\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;260\&quot; y=\&quot;465\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-54\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-41\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-29\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;434\&quot; y=\&quot;500\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;455\&quot; y=\&quot;540\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-56\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;exitX=1;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-16\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-32\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;444\&quot; y=\&quot;510\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;465\&quot; y=\&quot;550\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-57\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;exitX=1;exitY=0.75;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-38\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-43\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;454\&quot; y=\&quot;520\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;475\&quot; y=\&quot;560\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-70\&quot; value=\&quot;插件\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-57\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0704\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-58\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-38\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-39\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;600\&quot; y=\&quot;423\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;650\&quot; y=\&quot;445\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-72\&quot; value=\&quot;数据增强/标注\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-58\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0686\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-59\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-14\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-30\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;610\&quot; y=\&quot;433\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;660\&quot; y=\&quot;455\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-60\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0;entryY=0.75;entryDx=0;entryDy=0;dashed=1;exitX=0.617;exitY=0.05;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-12\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-23\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;620\&quot; y=\&quot;443\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;670\&quot; y=\&quot;465\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-73\&quot; value=\&quot;图生图\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-60\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.1555\&quot; y=\&quot;2\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-61\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-41\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-37\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;347\&quot; y=\&quot;472\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;329\&quot; y=\&quot;530\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-79\&quot; value=\&quot;意念操控\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-61\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0451\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-62\&quot; value=\&quot;物联网\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;640\&quot; y=\&quot;440\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-63\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;exitX=0.883;exitY=1.117;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-38\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-62\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;600\&quot; y=\&quot;415\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;660\&quot; y=\&quot;395\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-71\&quot; value=\&quot;传感器\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-63\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0586\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-65\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;dashed=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-23\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-30\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;530\&quot; y=\&quot;295\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;680\&quot; y=\&quot;255\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-69\&quot; value=\&quot;图生视频\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-65\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0569\&quot; y=\&quot;-3\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-68\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0;entryY=0.75;entryDx=0;entryDy=0;dashed=1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-11\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-23\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;500\&quot; y=\&quot;280\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;550\&quot; y=\&quot;243\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-74\&quot; value=\&quot;Midjourney&amp;lt;br&amp;gt;DALL E&amp;lt;br&amp;gt;Stable Difussion\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-68\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0629\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;174\&quot; y=\&quot;-44\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-90\&quot; value=\&quot;文生图\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-68\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.1845\&quot; y=\&quot;-3\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-81\&quot; value=\&quot;可穿戴\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;220\&quot; y=\&quot;530\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-82\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;exitX=0.4;exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Jfs-Gf4W77MN08QozXzM-15\&quot; target=\&quot;Jfs-Gf4W77MN08QozXzM-81\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;347\&quot; y=\&quot;472\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;335\&quot; y=\&quot;550\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-84\&quot; value=\&quot;VR眼镜\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;Jfs-Gf4W77MN08QozXzM-82\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0193\&quot; y=\&quot;3\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-85\&quot; value=\&quot;领域问答:医疗/金融等\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;269.99588204532944\&quot; y=\&quot;179.9991147049122\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-4\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-87\&quot; value=\&quot;NER/分类/摘要/生成等\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;434.99588204532944\&quot; y=\&quot;579.9991147049122\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-4\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-91\&quot; value=\&quot;三层：模型层→模态层→应用层\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontSize=14;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.998484809835\&quot; y=\&quot;130.0011254969541\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Jfs-Gf4W77MN08QozXzM-93\&quot; value=\&quot;① 腾讯智影&amp;lt;br&amp;gt;②阿里天猫精灵\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;119.99848480983502\&quot; y=\&quot;434.0011254969541\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

#### 应用列表

图解

<div class="mermaid">
    flowchart LR
    %% 节点颜色
    classDef red fill:#F09;
    classDef green fill:#5CF77B;
    classDef blue fill:#6BE0F7;
    classDef orange fill:#F7CF6B;
    classDef grass fill:#C8D64B;
    %%节点关系定义
    D(GPT-3):::grass
    D-->|2022-2,OpenAI,反馈强化学习|E(Instruct GPT):::green
    E-->|2022-11,OpenAI,聊天反馈|F(ChatGPT):::red
    E-->|2023-3-15,多模态,图像理解|G(GPT-4):::green

    D-->|2023-3-22,Action GPT|A(3D建模):::orange
    D-->|2020-1-17,图像领域,GPT-2|IG(Image GPT):::orange

    F-->|微软,搜索引擎\nNewBing\nBARD|F00(搜索引擎):::blue
    F-->|2023-3-24,Office 365|F01(办公软件):::blue
    F-->|2023-3-26,Coipilot\nCursor|F02(编程软件):::blue
    F-->|语料扩充\nNLP评估\n标注平台|F03(NLP基础任务):::blue
    F-->|2023-3-25,医疗问答,ChatDoctor\n心理测评|F1(领域问答助手):::blue
    IG-->|2023-3-27,装修设计图生成 RoomGPT|F2(领域图像生成):::blue
    V(扩散模型)-->F2
    F-->|2023-3-31,金融知识BloombergGPT|F3(领域大模型):::blue
    F-->|2023-3-24,Plugin|F4(插件商城):::blue
    F-->|2023-3-31,TaskMatrix自动适配,微软开源\n2023-4-3,HuggingGPT封装任务|F5(API驱动):::blue

    F-->|2023-3-9,微软,开源多模态问答系统\nVisual ChatGPT|F7(多模态问答):::blue
    F-->|2023-3-9,文档聊天\nPandasGPT+ChatDOC\nChatPaper+ChatPDF|F8(DocumentQA):::blue
    F-->|2023-4-2,推荐系统\nChatREC|F9(推荐系统):::blue
    F-->|2023-4-4,阿里鸟鸟分鸟,天猫精灵|F10(角色模拟):::blue
    F-->|2023-3-27,Neurosity头戴设备Crown+GPT4,实现意念操控|F11(脑机接口):::blue
    F-->|2023-3-31,Engineered Arts推出机器人Ameca+GPT-3,实现表情控制|F12(机器人):::blue
    F-->|2023-3-27,VR眼镜|F13(可穿戴):::blue
</div>

【2023-4-11】ChatGPT应用发展趋势：
- 第一波：Prompt套壳。如翻译/摘要工具、客户端、各种笔记工具。
- 第二波：文档向量索引、对话。如ChatPDF/ChatDoc、数字化分身等，自己实现可参考 llamaindex
- 第三波：自运行Agent。 如Microsoft Jarvis、  BabyAGI、autoGPT等


### MaaS 模型即服务

【2023-6-29】[抖音团队在用的大模型服务平台"火山方舟",我们也上手体验了一把](https://www.sohu.com/a/692602691_129720)

从算力消费的角度来说
- 第一条增长曲线是**模型训练**
- 第二条增长曲线则是模型的**应用和调优**

而且在不久的将来，第二条增长曲线必然会超过第一条。
- ![](https://p7.itc.cn/images01/20230629/4801588fc1244cc3804e3f864fd3296b.jpeg)

AI 领域形成了一种全新的商业模式：Model as a Service（MaaS），模型即服务。
- 「模型即服务」能够将大模型、工具平台、应用场景三者联合起来。
- 对于行业来说，这是一种无需巨额前期投入即可完成大模型训练、推理的途径；
- 对于大模型提供商来说，这是一种探索商业化落地、获得资金回报的可靠方法。

#### 火山方舟

[抖音团队在用的大模型服务平台"火山方舟"](https://www.toutiao.com/article/7250108244323107368)
- 【2023-6-28】在北京举行的火山引擎体验创新科技峰会上，火山引擎总裁谭待推出「火山方舟」MaaS 平台。

「火山方舟」面向企业提供模型精调、评测、推理等全方位的 MaaS 平台服务。基于其独特的多模型架构，企业可通过「火山方舟」同步试用多个大模型，选用更适合自身业务需要的模型组合。此外，「火山方舟」实现了大模型安全互信计算，更加注重为企业客户确保数据资产安全。

火山方舟提供了「模型广场」、「体验中心」、「模型精调」、「模型测评」等版块。
- 模型广场：从选择、体验到真正落地
  - 首批入驻大模型，包括百川智能、出门问问、复旦大学 MOSS、IDEA 研究院、澜舟科技、MiniMax、智谱 AI 等多家 AI 科技公司及科研院所的大模型，并已启动邀测。
  - 「模型广场」理解为一家「商店」，模型供应方可以在模型广场进行模型创建、上传、部署等，模型使用方可以在模型广场查看模型、快捷体验。
  - 除了 AI 对话类的应用，火山方舟现在还提供 AI 绘画类的应用体验。
- **模型精调**：百尺竿头更进一步
  - 客户需要利用自有数据或领域非公开数据进行持续训练，以及建设和积累自己的精调数据集。对精调手段的良好运用，能够帮助企业客户利用更小的模型尺寸，在特定任务上达到媲美通用大模型的水平，由此进一步降低推理成本。
  - Python sdk: [volc-sdk-python](https://github.com/volcengine/volc-sdk-python)
- 模型测评：
  - 模型评估环节也是火山方舟重点关注的一环，包括数据准备、指标定义以及人工评估和自动化评估等诸多全方位的工具。
  - 在火山方舟平台上，模型在发起精调任务的同时将进行自动化评估，精调的效果和运行指标也将在平台实时跟踪。
- 模型推理
  - 火山引擎提供安全互信的推理方案，保障模型提供商与模型使用者的模型与数据安全，客户可直接使用模型供应方已部署的在线服务或便捷地将精调模型部署为在线服务。

大模型服务需要解决三个问题
- 安全和信任
- 性价比
- 生态系统
  - 工具链和下游应用插件需要持续完善。
  - 打造垂直领域模型的微服务网络，内置包括图像分割、语音识别等众多专业模型，便于企业客户随时调用、自由组合。


思考
- DIFY、COZE 等各种LMOps以及各种Agent框架的 workflow 怎么样？

【2024-3-20】[微博观点](https://weibo.com/1896963363/5006706373562303)：workflow 因为模型reasoning能力在真实世界复杂任务时不够强，且短期内没法很大提升，针对合适的问题的从产品思维出发提出的解决方案。

理论上如果有capability很强的LLM，tools pool，可以解决非常多问题。但因为是概率性模型，LLM调用tools不总是100%成功，以及LLM当前的reasoning能力还不支持进行各个tools之间的组合调用，所以不能100%解决问题。

但如果工作流是确定的，那就没必要脱裤子放屁，用LLM去触发这个工作流，而只把LLM弱化，只是作为一个能很好理解用户意图并很擅长NLP任务的交互interface，弱化成一个节点，然后再提供同样丰富的 tools pool，然后让人工通过圈选拖拽等GUI去把这个workflow配置好，就能确定性的解决问题。 workflow就是这个思路。

workflow 核心是要有人识别**确定性工作流**，去配置足够多的模板，以及足够丰富的tools，其实使用门槛并不低，比如是一堆高玩带小白玩。 但workflow有可能像notion的template一样，是商业模式的一部分。

概率模型要想应用在容错率低的严肃场景，如何解决可控性/可预测性是最关键的一环，思路也是弱化 LLM 在业务流中的作用。


#### DIFY

[DIFY](https://dify.ai/), 支持各类主流模型
- 创建[页面](https://cloud.dify.ai/apps)

![](https://framerusercontent.com/images/gyg9CGdxDSKo0v5kmQeTVXR998.png)


#### 字节 大模型产品

##### 豆包/Cici

字节 
- 2023年下半年先后发布APP: 豆包（Grace）、Cici，问答、智能创作、聊天等。
- [coze](https://www.coze.com/) ，[官方文档](https://www.coze.cn/docs/guides/prompt)

##### Coze

【2023-12-23】[字节放出地表最强ChatBot，免费使用GPT4，请低调使用](https://mp.weixin.qq.com/s/dKzRJHbHmh4Rl8ia_xh7Eg)

[Coze](https://www.coze.com/) 是字节跳动推出的一款用来开发新一代 AI Chat Bot 的应用编辑平台，无论是否有编程基础，都可以通过这个平台来快速创建各种类型的 Chat Bot，并将其发布到各类社交平台和通讯软件上。—— 这个点类似于GPTs
- `插件`: **无限拓展 Bot** 的能力
  - Coze 集成了丰富的插件工具集，可以极大拓展 AlBot 能力边界。目前平台已经集成了超过60 款各类型的插件，包括资讯阅读、旅游出行、效率办公、图片理解等 API及多模态模型。
  - 集成不同工具，打造具备极强功能性的 Bot，比如可以添加各类新闻插件，来迅速打造出一个可以播报最新时事新闻的 Al 新闻播音员。平台提供的插件无法满足你的需求?我们也支持快速将你的私有 API集成为插件。
- `知识库`: 让 Bot 与你自己的数据进行交互
  - Coze 提供了简单易用的知识库能力，它能让 AI与你自己的数据进行交互。你可以在知识库中存储和管理数据。无论你需要处理几十万字的 PDF 还是某个网站的实时信息，只需要简单的创建知识库，即可让你的 Bot 来使用相关的知识。
  - 可以将几十页的产品介绍文档导入知识库，仅需几分钟，即可生成你的专属产品顾问。。可以将你经常关注的资讯网站或者在线论文导入知识库，每天 Bot 都会为你收集最新的更新及动态。
- `长期记忆`:让 Bot 拥有持久化的记忆能力
  - Coze 提供了一个方便 AI交互的数据库记忆能力，通过这个功能，你可以让 Al Bot 持久化的记住你跟他对话的重要参数或重要内容。
    - 让 Bot 记住你的饮食偏好，每次按照你的兴趣偏好推荐餐厅。
    - 让 Bot 记住你的语言偏好，每次按照你母语进行回答。
- `定时任务`:让 Bot 主动对话
  -  Bot 能主动给你发送消息? 通过定时任务功能，用户可以非常简单的通过自然语言创建各种复杂的定时任务。Bot 会准时给你发送对应的消息内容。
    - Bot 每天早上 9:00 给你推荐个性化的新闻。
    - Bot 每周五帮你规划周末的出行计划。
- `工作流`: 将创意变成 Bot 的技能
  - 让 Bot 使用这些特别的方法来代替你工作，那么你可以非常简单的创建一个工作流，让他变成 Bot 的技能。如果你懂得编程，那么可以在工作流里使用代码片段创建非常复杂的函数，如果你不懂的编程，那么也无需担心，通过简单的操作，你-样可以创作出属于你的工作流。
    - 做一个帮你搜集电影评论的工作流，快速的查看一部最新电影的评论与评分。
    - 做一个帮你撰写行业研究报告的工作流，让 Bot 替你写一份 20 页的报告。

所有的厂商都面临一个难题
- GPT 珠玉在前，做什么模型都容易获得一片骂声，包括最近发布的Gemini

- Gemini的策略：**免费的Pro 以及API**(60每分钟） ，不算短token，足以满足普通用户的所需，可以想象有更多的AI工具提供免费的服务能力，这里可以吸引一波免费用户，比GPT或者Claude更具有特色，更简单能被使用，这里策略用的好，普通AI用户大盘少不了。
- 字节策略更狠，**GPT4 不要钱**，能提前把一堆需要使用的AI的个人开发者，企业应用者，先进的工作者吸引到这个平台。站在GPT4的高度，吸引一波客户，反向在非GPT4能力上构建核心优势（包含平台化能力、自动化能力、数据延伸能力），也可以探索更多可能得场景（AI Playbook 为后面Agents时代提供更多思路。)
  - 以金钱换时间，还能吸引忠实的用户，用AzureAPI也是用，用字节的GPT的API也是用，只要能先把用户接上去，后面都好说。后面字节能打的大模型出来后，直接换引擎就是！真是一招妙招。反正OpenAI的套路大家都清楚了，无非就是钱的问题。

缺陷
- Multiagent模式有两个“不爽”的地方，都跟Agent跳转有关。
  - 第一个：Agent跳转**必须要用户输入**后才能触发，而不能由Agent自己触发，或者当Agent完成任务后自动跳转到下一个Agent。难以避免一些不必要的跟用户的交互。Multiagent模式下，Bot设计者应该有自由度去控制Bot什么时候自动执行流程，什么时候停下来跟用户交互。不然交互很多、流程复杂的程序就很难设计。
  - 第二点，在Multiagent模式，可以使用**自然语言**来配置Agent的跳转条件。然而这个跳转的判断逻辑非常不稳定。


Bot 如何盈利？
- Notion的目标就是要做一个All-in-one的工具。但Notion做法不是把所有的功能都打包到一个产品里，也不是做N多个App出来，Notion的做法是花很长时间去打磨那些组成软件的基本且必要的Building Blocks，例如文本编辑、关系数据库等等，然后用户可以用这些"Lego Blocks"组装自己的工具，让软件适配自己的需求和工作流。与其说Notion是一家生产力公司，不如说它是一家软件建构公司。
- Poe的Bot创作者主要有两种收益途径：
  1. 如果Bot给Poe带来新的订阅，Poe会分成；
  2. 给Bot Message定价，用户使用你的Bot，要为每条Bot Message付费（还没落实）
- Coze这个平台实际上也是沿着GPT Store这个路子，只不过相比于GPT Store，Coze的可定制性更强些，主要是因为Workflow以及Multiagent Flow这两大特性，其他如插件更丰富，支持变量和数据库，支持很多发布渠道等等这些特性也增色不少。但是Coze依然要面临盈利模式的问题
- Bot这种软件形态短期内应该是达不到手机App那种程度，Bot Store短期内也成为不了App Store。

实践案例
- 【2024-2-14】[如何用Coze制作一个信息检索Bot（含Workflow的基础用法）](https://mp.weixin.qq.com/s?__biz=MzU5MDM4ODIxMw==&mid=2247484073&idx=1&sn=de056ee432ae8b7a9adc471a796122c7&chksm=fe3e4c33c949c525517971f70a6535efa1d6ea99867635f788b65672980c45592412a006d36f&cur_album_id=3329086383935635457&scene=189#wechat_redirect)
- 【2024-3-6】[Bot创作者如何在Coze上赚钱？](https://mp.weixin.qq.com/s/WO-ZPuVgNHF129b4qsSjlQ)
  - 用 Coze 搭建 《卧底》的Multiagent Flow设计， Coze《[卧底](https://www.coze.com/store/bot/7338755327309070344?bid=MDQEELy4E1Vi4ozYnvcSpa2MA8wEHvJR-erI00A6JQ0WX0JuyVWyDvIp2qVX8wAFJqq14wQA&share=1&from=others)》
  - 从3月3号发文，截止到3月5号，《卧底》总共收获10笔订单，其中有效订单8笔（其中有2笔是朋友帮忙测试支付流程的），总收入是1032元
- 【2024-3-8】[Coze + 爬虫 = 周末去哪不用愁！](https://mp.weixin.qq.com/s/OfN3ndVfye9p_0wIeuQWng), 搭建一个“周末去哪玩”的Bot
  - 单纯靠提示词来实现这个Bot明显不太行，还是要自己加定制
  - 需求: 发送「城市+区+类型(景点、展览、音乐、话剧等)」 ，Bot输出对应区域的 「周末活动信息」，如：深圳市南山区-景点，Bot输出景点列表：【景点名称】景点地址；深圳市南山区-展览，Bot输出这周末的展览信息列表：【展名称】时间-票价-地点。
  - 实现: 写节点函数，实现 扣子: [7337619854435876876](https://www.coze.cn/store/bot/7338728599152951346)


##### LLM应用平台

搜索的[LLM应用平台](https://gpt.bytedance.net/gpt_agent/square)

##### ChitChop/小悟空

【2023-12-1】发布基于大模型的 App ChitChop
- 国内：[小悟空](https://wukong.com/tool)
- 国外：[ChitChop Web](https://www.chitchop.com/)
- APP见Google、Apple Store

一个私人AI助理，包括AI创作、AI绘画、娱乐、AI学习、工作、生活等6大使用场景。
- ChitChop由POLIGON开发和运营，而字节海外的社交产品`Helo`、日本漫画App 「FizzoToon」也由同一家公司运营
- POLIGON公司是字节海外的重要运营公司之一，于2020年在新加坡注册成立，主营业务是软件和应用程序的开发，其次是电脑游戏的开发。ChitChop是今年11月最新推出的App
- ChitChop宣称可以为用户提供多达200多个智能机器人服务，因为6大场景中每个场景包含10多个人工智能工具


比起豆包，ChitChop的应用场景和功能更加丰富，且进一步细分。
- AI创作，可以实现文章生成、文章续写、创作灵感、文章润色、爆款标题、视频脚本、微型故事、写演讲稿、写公关稿等功能。
- AI学习，可以进行作文提升、英语陪练、学习小语种、雅思写作、AI备课、论文生成、论文大纲、论文润色、万能翻译等。


#### gptbots

【2023-12-7】对话平台 [gptbots](https://www.gptbots.ai/)， 类似字节 [coze](https://www.coze.com/) 

#### Gnomic

【2024-1-16】[Gnomic](https://www.gnomic.cn/agentCenter/index) 智能体平台
- 无需魔法，随时随地免费使用GPT-4，并打造个性化GPTs智能体
- 集成 GPT-4, Gemini



### 提效降本

#### AutoAgent

自运行Agent：给一个任务，让GPT根据回复结果自己设定优先级进行后续的提问，获取信息、工作处理。
- 如果未来跟其他API打通，差不多可以实现一句话做网站、买飞机票、定外卖等。
- Twitter有高手完成了一句话生成网站并发布。国内也有朋友做了一句话生成前端页面[demo](​https://nlui.lxfater.com/)

#### FrugalGPT 斯坦福

【2023-5-9】[Cut the costs of GPT-4 by up to 98%](https://bdtechtalks.com/2023/06/12/reduce-costs-of-chatgpt-gpt-4/?utm_source=substack&utm_medium=email)

GPT-4 is a very capable model. But it is also very expensive. Using it for real-world applications can quickly amount to thousands of dollars in API costs per month.

In a recent study, researchers at Stanford University introduce “[FrugalGPT](https://substack.com/redirect/a82a2b73-2eb8-44a5-b067-04a36357dc20?j=eyJ1IjoiNGJ1bHkifQ.hPvX5Qf9I_Yt6AQx5dv_7Kto5X5Bi-g-XpGrr88s25Y),” a set of techniques that can considerably reduce the costs of using LLM APIs while maintaining accuracy and quality.
- [FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](https://arxiv.org/abs/2305.05176)

Key findings:
- The price of LLM APIs vary widely across different models
- For many prompts, the smaller and cheaper models can perform just as well as the more complex LLMs
- The FrugalGPT paper proposes three strategies to optimize LLM API usage 降低推理成本的三种方法
  - (1) **提示适配**: 识别哪个prompt更有效(如短的) Prompt adaptation: Reduce the size of your prompt or bundle several prompts together
  - (2) **模型近似**: 在具体任务上,用便宜小模型去匹配贵的大模型 Model approximation: Cache LLM responses or use model imitation to reduce the number of API calls to large models
  - (3) **大模型叠加**: 根据query自动适配合适的LLM. LLM cascade: Create a list of LLM APIs from small to large; use the smallest model that can provide an acceptable answer to the user’s prompt
  - ![](https://i0.wp.com/bdtechtalks.com/wp-content/uploads/2023/06/GPT-4-cost-recution-strategies.png?w=1392&ssl=1)
- FrugalGPT, an implementation of the cascade model, resulted in orders of magnitude cost reduction and even improved accuracy

### 数据处理

数据是石油，LLM 明显把炼油能力增强了，高价值行业和企业内部曾经难记录、难处理的数据都可以被重新以前分析。数据和信息的重构也意味着 AI 能承担更多决策权。

#### 数据抓取

ExtractGPT
- 一款浏览器扩展程序，可从结构化和非结构化页面中获取数据


##### GPTBot

【2023-8-8】OpenAI刚刚推出了GPTBot，一个自动从整个互联网抓取数据的网络爬虫。

这些数据将被用来训练像GPT-4和GPT-5这样的未来AI模型，GPTBot会确保不包括违反隐私的来源和那些需要付费的内容。

[GPTBot](https://platform.openai.com/docs/gptbot)是OpenAI开发的一个网络爬虫，用于在网络上收集信息，帮助改进AI模型。如果你是网站所有者，可以选择是否允许它访问网站或某些部分。同时，OpenAI确保了在使用GPTBot时，不会访问或使用任何敏感或付费内容。简单说，它就是一个用来学习和改进的小助手，但网站所有者可以自由选择是否和它互动。

##### AutoCrawler

【2024-4-19】Wenhao Huang等人[论文](https://huggingface.co/papers/2404.12753)中提出了AutoCrawler，将大型语言模型与网页爬虫相结合的新型网页自动化框架。
- 传统的网页抓取方法缺乏适应性和扩展性，而基于大型语言模型的**智能代理**在开放环境中表现不佳。

[AutoCrawler](https://github.com/EZ-hwh/AutoCrawler) 通过分两个阶段、利用HTML的层次结构进行渐进式理解，从错误行动中学习并持续优化HTML，从而更好地生成抓取操作。

实验证明，该框架可有效提高网页爬虫在多样化和动态网络环境中的性能。


#### 语料扩充

【2023-2-17】[unlocking-the-power-of-llms](https://github.com/howl-anderson/unlocking-the-power-of-llms)

使用chatgpt生成mark表格

| 文本           | 领域     | 实体映射      |
| -------------- | -------- | ------------- |
| 打开车门       | 设备控制 | 设备：车门    |
| 关闭空调       | 设备控制 | 设备：空调    |
| 导航到人民路   | 导航     | POI：人民路   |
| 开车去郊野公园 | 导航     | POI：郊野公园 |

也可以用空格
- 直接从 Excel 中复制数据粘贴到文本框中，表格表示形式是：每个单元格都用空格隔开。（不推荐）

生成的NER数据：

| 文本                          | 领域     | 实体映射                                   |
| ----------------------------- | -------- | ------------------------------------------ |
| 打开后备箱                    | 设备控制 | 设备：后备箱                               |
| 调高音量到80                  | 设备控制 | 设备：音响，属性：音量，数值：80           |
| 导航到北京天安门广场          | 导航     | POI：北京天安门广场                        |
| 开启车辆防盗系统              | 设备控制 | 设备：防盗系统                             |
| 显示明天的天气                | 天气查询 | 时间：明天                                 |
| 将客厅灯调暗一些              | 设备控制 | 设备：客厅灯，属性：亮度，数值：稍微暗一些 |
| 播放周杰伦的七里香            | 娱乐     | 歌手：周杰伦，歌曲：七里香                 |
| 打开窗户                      | 设备控制 | 设备：窗户                                 |
| 降低空调温度到25度            | 设备控制 | 设备：空调，属性：温度，数值：25           |
| 导航到附近的加油站            | 导航     | POI：加油站                                |
| 调整座椅到舒适的位置          | 设备控制 | 设备：座椅，属性：位置，数值：舒适         |
| 停止播放音乐                  | 娱乐     | 动作：停止播放音乐                         |
| 打电话给张三                  | 通讯     | 对象：张三                                 |
| 导航到机场                    | 导航     | POI：机场                                  |
| 打开车窗                      | 设备控制 | 设备：车窗                                 |
| 关闭车窗                      | 设备控制 | 设备：车窗                                 |
| 升高座椅到合适的高度          | 设备控制 | 设备：座椅，属性：高度，数值：合适         |
| 显示最近的通知                | 提醒事项 | 类型：通知                                 |
| 播报今天的新闻                | 新闻     | 时间：今天                                 |
| 显示路况                      | 导航     | 信息类型：路况                             |
| 导航到附近的酒店              | 导航     | POI：酒店                                  |
| 打开前灯                      | 设备控制 | 设备：前灯                                 |
| 关闭后灯                      | 设备控制 | 设备：后灯                                 |
| 设置提醒，下午3点有会议要参加 | 提醒事项 | 时间：下午3点，事件：参加会议              |
| 显示今天的日程                | 提醒事   |                                            |

#### 数据标注

详见站内专题：[数据标注](label)

#### 数据分析


##### LLM 适合分析什么

LLM 在哪些数据集分析类型上不擅长?

LLMs 在执行**精确数学计算**方面有所限制，不适合需要**精确量化**分析的任务，比如：
- 描述性统计（Descriptive Statistics）： 通过如均值或方差等措施定量总结数值列。
- 相关性分析（Correlation Analysis）： 获取列间的精确相关系数。
- 统计分析（Statistical Analysis）： 例如进行假设检验，判断数据点组间是否存在统计显著的差异。
- 机器学习（Machine Learning）： 在数据集上执行预测模型，如使用线性回归、梯度增强树或神经网络。

为了执行这些量化任务，OpenAI 推出了**高级数据分析**插件，以便通过编程语言在数据集上运行代码。

那么，为什么还有人想仅用 LLMs 来分析数据集而不用这些插件呢？

LLM 擅长的数据集分析类型
- LLMs 在识别**模式和趋势**方面表现出色。
- 这得益于在庞大且多样化的数据上接受的广泛训练，能够洞察到复杂的模式，这些模式可能不是一眼就能看出来的。

非常适合执行基于模式查找的任务，例如：
- 异常检测： 基于一个或多个列值，识别偏离常态的异常数据点。
- 聚类： 将具有相似特征的数据点按列分组。
- 跨列关系： 识别各列之间的联合趋势。
- 文本分析（适用于文本列）： 根据主题或情感进行分类。
- 趋势分析（针对有时间维度的数据集）： 识别列中的模式、季节性变化或趋势。

对于这些基于模式的任务，单独使用 LLMs 可能实际上会在更短的时间内比使用编程代码产生更好的结果

详见：
- 【2024-5-6】[我如何夺冠新加坡首届 GPT-4 提示工程大赛](https://baoyu.io/translations/prompt-engineering/how-i-won-singapores-gpt-4-prompt-engineering-competition?continueFlag=f4f91eca909d1c12022f5ef16e650de9)

##### Pandas AI

【2023-5-6】[Pandas AI](https://github.com/gventuri/pandas-ai)
- 将 Pandas 和 AI 结合，更方便地分析数据。

代码：

```py
import pandas as pd
from pandasai import PandasAI

# Sample DataFrame
df = pd.DataFrame({
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "gdp": [21400000, 2940000, 2830000, 3870000, 2160000, 1350000, 1780000, 1320000, 516000, 14000000],
    "happiness_index": [7.3, 7.2, 6.5, 7.0, 6.0, 6.3, 7.3, 7.3, 5.9, 8.0]
})

# Instantiate a LLM
from pandasai.llm.openai import OpenAI
llm = OpenAI()

pandas_ai = PandasAI(llm)
pandas_ai.run(df, prompt='Which are the 5 happiest countries?')
```

构造数据，然后输入 prompt：
> Which are the 5 happiest countries?

AI 根据输入的数据，处理数据，得到结果。

```sh
9             China
0     United States
6            Canada
7         Australia
1    United Kingdom
Name: country, dtype: object
```

画个图：
> Plot the histogram of countries showing for each the GDP, using different colors for each bar

AI 根据需求，画一了各个国家的 GDP 条形图。
- [img](https://mmbiz.qpic.cn/mmbiz_png/v1JN0W4OpXgoevdlbWGnibC449Dicxr2e0tQZtQPf571xu6T4cRcm2VBoIyibxoicp8iaoZoUEicxBwDN7wQNdEK3ZOA/640?wx_fmt=png&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1)


##### NL2SQL

text2sql(NL2SQL) 是NLP诸多任务中较难的任务，即便发展迅速的LLM，也没有完全解决text2sql中复杂查询问题

参考
- [NL2SQL技术方案系列](https://www.cnblogs.com/ting1/p/18145360)

NL2SQL 任务目标: 将用户对某个数据库的自然语言问题转化为相应的SQL查询。

随着LLM的发展，使用LLM进行NL2SQL已成为一种新的范式。
- 如何利用提示工程来发掘LLM的NL2SQL能力显得尤为重要。

现状：大语言模型虽然在不断的迭代过程中越来越强大，但类似**商业智能**企业级应用要远比分析一个 Excel 文件、总结一个 PDF 文件的问题要复杂的多：
- **数据结构复杂**：企业信息系统的数据结构复杂性远远超过几个简单的 Excel 文件，一个大型企业应用可能存在几百上千个数据实体，所以在实际应用中，大型 BI 系统会在前端经过汇聚、简化与抽象成新的语义层，方便理解。
- **数据量较大**：分析类应用以海量历史数据为主，即使一些数据在分析之前会经过多级汇总处理。这决定了无法在企业应用中把数据简单的脱机成文件进行分析处理。
- **分析需求复杂**：企业应用的数据分析需求涵盖及时查询、到各个维度的报表与指标展现、数据的上下钻、潜在信息的挖掘等，很多需求有较复杂的后端处理逻辑。

这些特点决定了当前大语言模型在企业数据分析中的应用<span style='color:red'>无法完全取代目前所有/部分的分析工具</span>。

其合适的定位或许是：作为现有数据分析手段的一种**有效补充**，在部分需求场景下，给经营决策人员提供一种更易于使用与交互的分析工具。

具体的应用场景包括：‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
- 及时数据查询。提供对运营或统计数据的简单自定义查询，当然你只需要使用自然语言。‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
- 传统 BI 工具能力的升级。很多传统 BI 工具会定义一个抽象的语义层，其本身的意义之一就是为了让数据分析对业务人员更友好。而大模型天然具有强大的语义理解能力，因此将传统 BI 中的一些功能进化到基于自然语言的交互式分析，是非常水到渠成的。
- 简单的数据挖掘与洞察。在某些场景下的交互式数据挖掘与洞察，可以利用大语言模型的 Code 生成能力与算法实现对数据隐藏模式的发现。

三种基础技术方案介绍
- 自然语言转数据分析的 **API**, `text2API`
  - 类似现有的一些 BI 工具会基于自己的语义层开放出独立的 API 用于扩展应用，因此如果把自然语言转成对这些数据分析 API 的调用，是一种很自然的实现方式。当然完全也可以自己实现这个 API 层。
  - 特点是受到 API 层的制约，在后面我们会分析。
- 自然语言转关系数据库 **SQL**, `text2SQL`
  - 目前最受关注的一种大模型能力（本质上也是一种特殊的 text2code）。由于 SQL 是一种相对标准化的数据库查询语言，且完全由数据库自身来解释执行，因此把自然语言转成 SQL 是最简单合理、实现路径最短的一种解决方案。
- 自然语言转数据分析的**语言代码**，即 `text2Code`
  - 即代码解释器方案。让 AI 自己编写代码（通常是 Python）然后自动在本地或者沙箱中运行后获得分析结果。当然目前的 Code Interpreter 大多是针对本地数据的分析处理（如 csv 文件），因此在面对企业应用中的数据库内数据时，需要在使用场景上做特别考虑。

![图](https://ai-studio-static-online.cdn.bcebos.com/384654a64ddc45048d9fe0f1bf83152d876c635fcfbc461c92628d644bdf36de)

text2sql的常用数据集与方法

中文 text-to-SQL数据集:
- CSpider (Min et al., 2019a)
- TableQA (Sun et al., 2020)
- DuSQL (Wang et al., 2020c)
- ESQL (Chen et al., 2021a)
- Chase https://xjtu-intsoft.github.io/chase/


解法 （[参考](https://zhuanlan.zhihu.com/p/646404160)）
- LLM 前处理
  - RAT-SQL [RAT-SQL: Relation-Aware Schema Encoding and Linking for Text-to-SQL Parsers](), 基于Encoding + relation self attention
  -  LGESQL
    - [LGESQL: Line Graph Enhanced Text-to-SQL Model with Mixed Local and Non-Local Relations]()
    - 基于Relation Graph, 虽然RATSQL等融合了关系信息，但目前仍有两点限制：① 无法发现有效的源路径（RATSQL是预先定义好的关系）② 相邻两个点，无法区分是不是local，即同一个表内。
  - UnifiedSKG 逐渐过渡到LLM思路
    - UnifiedSKG: Unifying and Multi-Tasking Structured Knowledge Grounding with Text-to-Text Language Models
- LLM 后处理
  - DIN-SQL 问题分解再纠错
  - [DB-GPT](https://github.com/csunny/DB-GPT), [Doc](https://db-gpt.readthedocs.io/en/latest/), DB-GPT基于 FastChat 构建大模型运行环境，并提供 vicuna 作为基础的大语言模型，通过LangChain提供私域知识库问答能力。



【2024-1-26】[MLX 上使用 LoRA / QLoRA 微调 Text2SQL](https://wangjunjian.com/mlx/text2sql/2024/01/26/Fine-tuning-Text2SQL-based-on-Mistral-7B-using-LoRA-on-MLX-5.html)：对比使用 LoRA 和 QLoRA 基于 Mistral-7B 微调的效果
- 相同 Iteration 次数下 QLoRA 不如 LoRA 的效果
- Prompt tokens/sec: QLoRA 是 LoRA 的 1.79 倍
- Generation tokens/sec: QLoRA 是 LoRA 的 8.87 倍

|方式|更新参数量|微调耗时(600步)|内存占用|模型大小|测试困惑度(PPL)|测试交叉熵(Loss)|
|---|---|---|---|---|---|---|
|LoRA|2.35/万 （1.704M / 7243.436M * 10000）|20 分 26 秒|46G|13G|3.863|1.351|
|QLoRA|13.70/万（1.704M / 1244.041M * 10000）|23 分 40 秒|46G|4G|4.040|1.396|


【2024-1-15】[vanna-ai](https://github.com/vanna-ai/vanna)，[文档](https://vanna.ai/docs/)

vanna-ai 工作原理
- Train a RAG "model" on your data.
  - 准备数据：DLL, Document, SQL语句
  - 生成 embedding
  - 存储embedding和metadata
- Ask questions.
  - question → 生产 embedding → 找相关的数据 → 构建 prompt,发送给LLM → SQL语句

![](https://vanna.ai/blog/img/how-it-works.png)

```py
# pip install vanna
import vanna as vn
# --------- 训练 -------
# Train with DDL Statements
vn.train(ddl="""
    CREATE TABLE IF NOT EXISTS my-table (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
""")
# Train with Documentation
vn.train(documentation="Our business defines XYZ as ...")
# Train with SQL
vn.train(sql="SELECT name, age FROM my-table WHERE name = 'John Doe'")
# --------- Asking questions -----------
vn.ask("What are the top 10 customers by sales?")
```

返回

```sql
SELECT c.c_name as customer_name,
        sum(l.l_extendedprice * (1 - l.l_discount)) as total_sales
FROM   snowflake_sample_data.tpch_sf1.lineitem l join snowflake_sample_data.tpch_sf1.orders o
        ON l.l_orderkey = o.o_orderkey join snowflake_sample_data.tpch_sf1.customer c
        ON o.o_custkey = c.c_custkey
GROUP BY customer_name
ORDER BY total_sales desc limit 10;
```


##### ChatExcel

【2024-2-4】北京大学出的4款免费神器
- [Chat Law](https://chatlaw.cloud/)：北大法律AI大模型，免费全能律师，思维导入分析案情，给出建议
- [ChatExcel](https://chatexcel.com/) 
- 中国历代人物：收录53w古代历史人物
- 可视化看中国：视觉方式呈现历史背景、关系图

[ChatExcel](https://chatexcel.com/) 通过自然语言操作excel表格
- ![](https://chatexcel.com/static/pic/case/case-01.gif)

### 内容管理/营销

CRM 记录姓名、电话等结构化数据

CRM龙头接入ChatGPT，AI辅助客户管理再看看更深层次的客户关系管理环节，GPT技术依然是无孔不入，进化为智能咨询角色。
- 3月7日，客户关系管理领域SaaS巨头`Salesforce`推出基于ChatGPT的CRM生成式AI产品：“Einstein GPT”，据称可用于帮助企业销售人员、客户服务专员和市场营销人员高效率完成本职工作。比如
- 帮销售人员撰写电子邮件，结合过往案例生成知识文章，为客服人员生成客户提问的特定答案，帮开发人员编写代码等。
- 同时，Salesforce旗下的办公协作软件`Slack`也推出了基于ChatGPT的应用，Slack将其应用积累的数据与ChatGPT相结合，为客户提供他们所需的信息，包括提供即时对话摘要、研究工具和写作辅助等，帮助数百万公司更高效地工作。
- Slack的ChatGPT应用提供一个[对话界面](https://vdn6.vzuu.com/SD/2faf67f0-ee5e-11ed-83ab-d2cc0999534d-v1_f4_t2_4RbvmazF.mp4)，可以帮用户获取即时对话框中的信息，并基于研究工具去解析内容的主题，并帮用户快速撰写消息。

- 4月10日，知名营销SaaS企业上线数据集成平台有赞iPaaS和由大模型驱动的首个AI产品“加我智能”。加我智能目前主要支持图文推广和活动策划两大场景，能自动生成推广图文，并理解活动目的，生成跨产品和功能的营销活动。
- 国外也是一致趋势，4月20日，外媒称谷歌计划在未来几个月内将生成式AI引入其广告业务。目前，谷歌已经在其广告业务中使用AI来创建简单的提示，鼓励用户购买产品。可以看到，无论是互联网广告商、广告公关代理龙头还是SaaS服务商，他们都在加快接入AI大模型的步伐。如果能将广告人从众多重复机械化工作中解放出来，大卫·奥格威理想中的广告创意或许会离我们更近一步。

#### Jasper

2022 年 10 月，多个美国投资人跟李志飞提到一款叫 Jasper 的 AIGC 应用很赚钱。当时 Jasper 仅仅成立 18 个月，估值 15 亿美元。
- Jasper 基于 GPT-3 模型，针对市场营销场景做了精调，靠**生成营销文案**打开市场
- 2022 年 ARR（衡量 SaaS 或订阅业务的收入指标）约 8000 万美元

Jasper 解决了李志飞两年前就开始思考的问题：GPT-3 到底适合应用在什么场景？
- 李志飞想过文案场景，但只 “答对” 一半。“过去我们做的是纠错、润色、改写，没想到完全生成一篇内容”。

#### Gong

以 Gong 为代表的 AI-based CRM 则是记录分析 B2B 销售和客户录音。

#### Segment

Segment 的主要业务是提供**实时消费者数据**，传统的 CRM 的数据和业务之间其实并不直接衔接，因为过去 CRM 采集到的数据可能也有错的、并且也过时了，但在 LLM 基础上，Segment 其实反而提供更实时、更有效的数据。

#### Pilot

2022 年成立的Pilot AI 是一款面向销售人员的 AI 产品，核心是能够自动将每一个**销售电话变成详细的笔记和结构化数据**，并将结构化数据直接同步到 CRM 系统。这也是大语言模型的核心价值之一。
- 平时聊天有非常多的数据，如果没有被记录和分析，就永远是 dark data。而大语言模型理解语言的能力变强之后，dark data 可以变成非结构化数据、结构化数据，变成 information。而且 Pilot 的整个流程都是自动化的，价值非常显著。

#### Typeface

【2023-4-10】[Typeface](https://www.typeface.ai/) 是一个 AI 营销内容生成平台，由前 Adobe CTO 创立。
- The enterprise-grade generative AI app that empowers everyone to express their unique imagination.

能力：
- `Prompt`: Create engaging content in seconds
  - A new visual vocabulary to express your ideas: Generate anything from a simple prompt, so you can easily create without a steep learning or time curve.
  - 一个简单的提示语，就能生成特定领域里的营销内容（文字/图片）
  - Spend more time on ideas, less on tasks: Tired of looking at a blank page?  Jump start projects by simply typing your idea. Stress test headlines, brainstorm campaigns, personalize pitches, and more.
  - 将客户精力从具体任务转移到点子上：压力测试标题，头脑风暴活动，个性化宣传等等
  - Write and edit any type of content: Click to add the elements you want – headlines, paragraphs, images, captions – to build the entire content flow on one visual canvas. Not sure where to start? Use a template and modify it however you need.
  - ![](https://www.typeface.ai/images/Prompt-Visual-1-7.webp)
  - 撰写、编辑各种类型的内容：只需要轻轻一点，就能添加标题、段落、图像、注释等元素，在同一个页面中完成内容创作。
  - Flex to your style and collaborate faster: Develop multiple assets quickly and in parallel. Stylize your way with built-in formatting and image editing tools, such as filters, adjustments, and overlays. Share your work with collaborators across channels.
  - 适配客户风格，协同工作
  - ![](https://www.typeface.ai/images/Prompt-Visual-3-3.webp)
- `Flow`: Extend and customize to your workflows, [flow](https://www.typeface.ai/features/flow.html)
- `Blend`: Personalize to your brand and audiences, [blend](https://www.typeface.ai/features/blend.html)
- `Safe`: Ensure brand safety and control; 
  - 拼写检查、剽窃检测、真实性检测、品牌控制

Typeface 最大的特点是能够学习企业客户的“专有数据”。客户将带有企业风格的专有数据导入 Typeface 供模型学习，基于这些专有数据，Typeface 可以输出更个性化的、满足企业实际需求的内容，做到让 AI “更懂用户”。

为了实现这一点，Typeface 让每位客户拥有独有的 AI 模型和托管服务，以及原创内容检测、品牌契合度检测和文字上的语法检测等功能。而收集专有数据的意识也在行业内逐渐形成共识。


#### 广告视频

【2023-11-21】[日本广告](https://www.bilibili.com/video/BV1sC4y137Ye/?spm_id_from=333.999.0.0&vd_source=ec1c777505e146eb20d947449d6bba6e)

完全AI生成的广告已经问世，这么漂亮的脸，还可以随意定制更漂亮的，永远也不会有丑闻，不会影响公司形象，成本极低几乎可以忽略不计

由AI生成的广告，来自日本的伊藤园公司。广告使用全AI生成的人物拍摄，自然和谐，与真人无异。好处包括无限制的外观定制、没有丑闻对公司和产品的影响，成本几乎可以忽略不计且拍摄周期短。视频提出了一个问题，企业应该选择真人还是AI的广

<iframe src="//player.bilibili.com/player.html?aid=747505314&bvid=BV1sC4y137Ye&cid=1310947760&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  width="720" height="405"> </iframe>

AI生成的麦当劳广告

<iframe src="//player.bilibili.com/player.html?aid=447455974&bvid=BV17j411z7GD&cid=1239130065&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="720" height="405"> </iframe>


### NLP基础任务

【2023-9-12】[大语言模型在NLP基础任务的应用案例集](https://zhuanlan.zhihu.com/p/625321362)

#### 分类

怎么用GPT做分类？

两种方法
- 类似bert，在输出部分加个head，输出分类得分；
- 与clm语言模型一致，在生成类别广告词，来判断分类。

详见：[文本分类专题](cls)

#### NER

命名实体识别任务（NER）的目标是识别出给定文本中的实体部分，一般采用**序列标注**方法进行建模，预测每个位置的token是否属于某个实体、属于哪个实体。
- GPT-NER，序列标注→生成任务
  - GPT生成→筛选→验证

详见：[NER专题](ner)

#### 信息抽取

chatgpt做零样本信息抽取
- 论文：[Zero-Shot Information Extraction via Chatting with ChatGPT](https://www.aminer.cn/pub/63f5887b90e50fcafd27b7c4/zero-shot-information-extraction-via-chatting-with-chatgpt)
- we transform the zero-shot IE task into a multi-turn question-answering problem with a two-stage framework (ChatIE)
- 使用两阶段框架（ChatIE）将零样本信息提取任务转换为多回合问答问题。

##### 语音摘要

Podcast Summariser 使用OpenAI Whisper + Davinci进行播客摘要


##### 视频摘要

【2023-5-17】[基于ChatGPT的视频摘要应用开发](https://www.toutiao.com/article/7230786095158690362)
- 视频摘要器: 将数小时的视频内容转换为几行准确的摘要文本

视频摘要方案
- 用ChatGPT 插件，将令人AI 连接到实时 YouTube 网站。 但只有少数商业开发人员可以访问 ChatGPT 插件，因此可行性不大。
- 下载视频的抄本（字幕）并将其附加到提示中，然后语言模型发送提示来总结抄本文本。缺点：不能总结一个包含超过 4096 个标记的视频，这对于一个普通的谈话节目来说通常是 7 分钟左右。
- 用**上下文学习**技术对转录本进行**向量化**，并使用向量向语言模型提示“摘要”查询。 这种方法可以生成准确的答案，指示转录文本的摘要，并且不限制视频长度。

Video Summarizer应用程序以llama-index为基础，开发了一个Streamlit web应用程序，为用户提供视频URL的输入以及屏幕截图、文字记录和摘要内容的显示。

用llamaIndex 工具包，不必担心 OpenAI 中的 API 调用，因为对嵌入使用的复杂性或提示大小限制的担忧很容易被其内部数据结构和 LLM 任务管理所覆盖。
- 视频转录：开源 Python 库 youtube-transcript-api 将视频转文本
- 当文档被送入 LLM 时，它会根据其大小分成块或节点。 然后将这些块转换为嵌入并存储为向量。
- 当提示用户查询时，模型将搜索向量存储以找到最相关的块并根据这些特定块生成答案。 例如，如果你在大型文档（如 20 分钟的视频转录本）上查询“文章摘要”，模型可能只会生成最后 5 分钟的摘要，因为最后一块与上下文最相关 的“总结”。
- ![image](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/d0a76dbf2a11400f97220283ea233fa9~noop.image?_iz=58558&from=article.pc_detail&x-expires=1684911936&x-signature=dohd7TRWXXfBH5PRvGLj3ldXBh0%3D)

流程图
- ![flow](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/38966bfef5f641f294301647b92def7e~noop.image?_iz=58558&from=article.pc_detail&x-expires=1684911936&x-signature=Mdb8NbIuzxqhc1X9FW60XawIOK0%3D)

（1）视频转录

```py
# !pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
# 唯一应该强制提供的参数是 11 位视频 ID，在 v= 之后的每个 YouTube 视频的 URL 中找到它
srt = YouTubeTranscriptApi.get_transcript("{video_id}", languages=['en'])
formatter = JSONFormatter()
json_formatted = formatter.format_transcript(srt)
print(json_formatted)
```

（2）加载文档

```sh
!pip install llama-index
```

SimpleDirectoryReader 是 LlamaIndex 工具集中的文件加载器之一
- 支持在用户提供的文件夹下加载多个文件
- 支持解析各种文件类型，如.pdf、.jpg、.png、.docx等，让您不必自己将文件转换为文本。

```py
from llama_index import SimpleDirectoryReader
SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
loader = SimpleDirectoryReader('./data', recursive=True, exclude_hidden=True)
documents = loader.load_data()
```

构建索引
- LlamaIndex 应与你定义的 LLM 交互以构建索引，在本演示的情况下，LlamaIndex 使用 gpt-3.5 聊天模型通过 OpenAI API 调用嵌入方法。

```py
from llama_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper, ServiceContext
from langchain import ChatOpenAI

# define LLM
llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=500))

service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

index = GPTSimpleVectorIndex.from_documents(
    documents, service_context=service_context
)
```

（3）查询索引

通过建立索引，查询非常简单，无需上下文数据，直接输入即可。

```py
response = index.query("Summerize the video transcript")
print(response)
```

完整代码见[原文](https://www.toutiao.com/article/7230786095158690362)

```sh
!python -m pip install openai streamlit llama-index langchain youtube-transcript-api html2image
```

#### 机器翻译

原文：
> 翻译这段话:"人要是行,干一行行一行,一行行行行行。行行行干哪行都行。要是不行,干一行不行一行,一行不行行行不行,行行不行,干哪行都不行。要想行行,首先一行行。成为行业内的内行,行行成内行。行行行,你说我说得行不行。"

普通翻译
> Translate this passage: "If you can do it, do it one line at a time, one line at a time. You can do it all. If not, do it one line at a time, one line at a time, no line at a time, no line at a time, no line at all. If you want to do it, you must first do it one line at a time. Become an expert in the industry, and become an expert in the industry. Okay, you say what I say is okay."

文心一言
> If you are talented, you can excel in any field and excel in iit. If you are not talented, excel in just one field but cannot do it well, and if you are not skilled at just onefield, it cannot be done well. In any field, if you want to excel, you must first excel in it. Become an expertin your field, and then you become an expert in everything else related to that field. Being a good at a particulaar field enables you to understand all the others. Being good at multiple fields enables you to undersstand everything.


GPT-4翻译
> Translate this passage: "If a person is capable, they can excel in any profession they choose. If they're not capable, they won't succeed in any profession, no matter which one they choose. If you want to be successful, you must first become proficient in one field. Become an expert in your industry, and you'll achieve success. Is what I'm saying reasonable?"

### 搜索


#### ollama 本地搜索

【2024-3-29】[LLocalSearch](https://github.com/nilsherzig/LLocalSearch) 开源的完全本地化的AI搜索工具，无需 OpenAI 或 Google API 密钥。
- 基于 ollama, 7b 模型

项目特点：
- 🕵️ 完全本地化运行，不需要连接到外部API，因此无需API密钥。
- 💸 适用于性能相对较低的大型语言模型硬件，例如在演示视频中使用的是7b模型。 
- 🤓 提供详细的进度日志，这有助于用户更好地理解搜索和处理过程。 
- 🤔 支持用户提出后续问题，以便深入探讨或解决问题。
- 📱 界面对移动设备友好，适合在手机或平板电脑上使用。 
- 🚀 使用Docker Compose工具，可以快速且轻松地部署此服务。 
- 🌐 提供网络界面，使用户可以从任何设备轻松访问和使用。 
- 💮 该服务提供精心设计的用户界面，支持浅色和深色模式，满足不同用户的视觉偏好。

```sh
git clone https://github.com/nilsherzig/LLocalsearch.git
# 1. make sure to check the env vars inside the `docker-compose.dev.yaml`.
# 2. Make sure you've really checked the dev compose file not the normal one.
# 3. build the containers and start the services
make dev 
# Both front and backend will hot reload on code changes. 
```

#### WebGPT

【2021-12-17】基于GPT3模型在搜索结果方面的优化
- [WebGPT: Improving the factual accuracy of language models through web browsing](https://arxiv.org/abs/2112.09332)

把原先需要人工创造的原始数据，或需要爬取的数据，直接通过输入层，从网页端Search Query到模型，经过内部网络的隐藏单元推理后，到输出层与人工结果进行对比，然后再调参。
- 把工程方法融入到了模型训练的流程中，所以称之为“对GPT3做了一点小调整”。

数据生产分为两个部分: demostration（演示）和comparison（对比）。
- **demonstration**: 按照人类使用搜索引擎时的操作，针对给定的问题，对搜索引擎返回的结果，进行过滤。
  - OpenAI将上述复杂的过程简单抽象为了10个commands（指令）。在特定开发的标注平台，记录人类的搜索过程，并将此过程中的操作和上下文转换为带标签的语料——语料的输入是上下文，command是具体操作。值得注意的是，为了包含搜索过程中的历史操作，上下文包含了对操作的总结。
  - ![img](https://pica.zhimg.com/80/v2-5ab51dfb35e10dad2f4833d66cdbe5e6_1440w.webp?source=1940ef5c)
  - ![img](https://picx.zhimg.com/80/v2-1e6196446b479f49cf9a0b9142f53b5d_1440w.webp?source=1940ef5c)
- **comparison**: 针对某个特定的问题，模型生成两个答案，标注人员先对每个答案从trustworthness（可信度）、来源对结果的支持程度进行打分。在对两个答案进行对比打分。
  - ![](https://picx.zhimg.com/80/v2-1bbc0cddf1943486bb30529d9595c2c0_1440w.webp?source=1940ef5c)


WebGPT 的训练是在 pre-trained GPT 的基础上进行 finetune，finetune 的方法挺有趣的，采用了 behavior cloning, reward modeling, RL, rejection sampling

模型由四个部分组成：
- Behavior cloning（以下简称BC）
- Reward model（以下简称RM）
- Reinforcement learning（以下简称RL）
- Reject Sampling（以下简称RS）

这些均由GPT3类模型微调而来。做这个选择的原因就是GPT3模型在阅读理解、答案合成等领域涌现出了零样本学习的能力

主要作用如下：
- Behavior cloning
  - 基于demonstration数据，模仿人类搜索+提取信息行为。可以简单地理解为一个分类任务的微调。
- Reward model
  - 基于comparison数据，输入问题、答案以及引用，模型给出一个得分，相当于是一个回归任务的微调。但由于得分的主观性过大，这里输入采用了同一个问题、两组答案与引用，groundTruth为comparison数据的标签，训练目标函数为交叉熵。
- Reinforcement learning
  - 这里的强化学习模型采用BC模型的参数初始化，通过RM生成奖励值，利用PPO算法更新模型参数，使得模型生成的结果得分越来越高。
- Reject Sampling
  - 拒绝采样，对BC / RL模型生成的结果进行采样，并对采样后的结果通过RM选取回报值最大的结果作为最终结果。

结果对比
- 5.1节介绍了不同部分组合的对比结果。主要对比RL、RS与baseline的BC的结果之间的对比。
- 结论比较反直觉
  - 一方面，虽然RL、RS比baseline都有提升，但RS的提升要更明显些；
  - 另一方面，经过RL、RS两步的结果没有只进行RS的结果提升大。
- 文章给出的可能原因是RS不需要更新基础的BC模型参数，而RL+RS同时对RM的结果优化，可能造成对RM的过度优化。

作者：[Century See](https://www.zhihu.com/question/506813687/answer/2926709800)


#### WebCPM

【2023-5-15】WebCPM 成功实践了 [BMTools](https://mp.weixin.qq.com/s/NLzno1XRHQLyMFfh5CeJpw), 中文领域首个基于交互式网页搜索的问答开源模型框架 `WebCPM`，这一创举填补了国产大模型该领域的空白
- [paper](https://arxiv.org/abs/2305.06849), [code](https://github.com/thunlp/WebCPM)
- WebCPM 的特点在于其信息检索基于交互式网页搜索，能够像人类一样与搜索引擎交互从而收集回答问题所需要的事实性知识并生成答案。换言之，大模型在联网功能的加持下，回答问题的实时性和准确性都得到了飞跃式增强。
- WebCPM 对标的是 WebGPT ， WebGPT 也正是微软近期推出的 New Bing 背后的新一代搜索技术。同 WebGPT一样，WebCPM 克服了传统的 LFQA（ Long-form Question Answering）长文本开放问答范式的缺陷：依赖于非交互式的检索方法，即仅使用原始问题作为查询语句来检索信息。


#### perplexity.ai

待补充


#### devvai

【2023-11-30】最懂程序员的新一代AI搜索引擎来了，[devvai](https://devv.ai/zh) 可以基本代替使用Google/StackOverflow等等的使用场景
- 一款专门面向中文开发者群体的AI搜索引擎，接入了搜索引擎数据，回答的内容基本都是最新的，很适合用来学习，比如对编程中的某个地方不理解，可以直接使用关键词搜索，就可以获得一个相对来说比较完善的技术摘要，右侧还可以点进原文去查看具体内容！而且还全部免费
- 更快速的代码搜索体验


#### Lepton Search

【2024-1-14】贾扬清内侧版 [Lepton Search](https://search.lepton.run/) 
- 类似季逸超的 [Peak Labs](https://www.peak-labs.com/en/) 推出的 [Magi](https://magi.com/)，暂停服务

500行Python代码构建的AI搜索工具，而且还会开源。后端是 `Mixtral-8x7b` 模型，托管在 LeptonAI 上，输出速度能达到每秒大约200个 token，用的搜索引擎是 Bing 的搜索 API。
- [search_with_lepton](https://github.com/leptonai/search_with_lepton)
- [体验](https://search.lepton.run/search)
- ![](https://private-user-images.githubusercontent.com/1506722/298886477-845d7057-02cd-404e-bbc7-60f4bae89680.png)

作者还写了一下自己的经验：
- (1) 搜索质量至关重要。优质的摘要片段是形成精准概括的关键。
- (2) 适当加入一些虚构内容实际上有助于补充摘要片段中缺失的“常识性信息”。
- (3) 在进行内容概括时，开源模型表现出了卓越的效果

#### Arc Search

【2024-1-31】[基于大模型的Arc Search：颠覆百度的AI搜索来了？](https://www.toutiao.com/article/7330181327859958307)

2022 年底，一家名不见经传的初创公司——`The Browser Company` 推出了全新浏览器 `Arc Browser`，在理念和交互设计上完全不同于 Chrome 等今天常用的浏览器，很多用户、博客和媒体都给出了极高的评价。
- 「Arc Browser 是我一直在等待的 Chrome 替代品，」The Verge 的 David Pierce 评价道。

2023年，Arc Browser 进行了多次迭代，也在海外和国内都获得了许多拥趸，支持平台也从最初的 macOS 扩展到了 iOS 和 Windows。

这两天，The Browser Company 突然「推倒」了 iOS 上的 `Arc Browser`，基于生成式 AI 带来的颠覆，推出了一款全新的应用：`Arc Search`。

本质上 Arc Search 还是一款移动平台上浏览器，根据官方公告，「Arc Search」将在移动平台上全面取代「Arc Browser」。

Arc Search 有两种浏览模式
- 一是 **传统模式**，通过搜索词直接转到谷歌的搜索结果页，也可以输入网址进行访问；
- 二是 **AI模式**，类似其他生成式 AI 搜索一样，用户可以用自然语言对话的形式输入问题或者提示词。

输入问题或者提示词后，按下「Browser for Me」，AI 就通过阅读相关网页了解信息，再针对问题进行总结、回答。最终，Arc Search 会以统一的排版和格式呈现 AI 生成的回答，通常是先看到回答的「要点」和「最佳搜索结果」，接着再看到详细的回答，最后还附上一系列相关网页推荐。

举个例子，输入「为什么 Twitter 现在叫 X」后点击「Browser for Me」，就像字面意思，AI 将会为用户浏览包括 CBS 新闻、纽约时报、伦敦大学、Tech Radar 以及 YouTube 等 6 个网页的内容，然后针对问题进行提炼和总结，生成回答。
- 等待 AI 浏览、理解、再回答的过程中，Arc Search 利用 iPhone 的振动进行反馈，让用户可以明确感知到这一过程，这是一个值得称赞的细节。

不同于 ChatGPT，Arc Search 是建立在**传统搜索**方式的基础上，让 AI 浏览搜索结果页上的 6 个「最佳」结果，再利用生成式 AI 的技术优势针对问题进行总结、归纳。

Arc Search 的巧妙之处
- AI 生成回答前，先通过传统搜索引擎进行了一层「过滤」，筛选出内容质量较高的相关网页，再基于这些内容生成答案，可以在一定程度上降低大模型「幻觉」带来的影响，在回答质量、准确性上也更多一些保证。

虽然 The Browser Company 没有明确指出 Arc Search 背后调用的大模型，但按照 Arc Browser 的相关报道，Arc Search 应该也是通过 API 调用了包括 GPT-4 在内的混合模型。

### 排序

重排器（Reranker）作为信息检索的第二阶段，需要根据查询和文档的相关性，对候选文档做细粒度的排序。经典的重排方法一般使用交叉编码器，结合文档和查询的语义信息进行打分和排序。

现有的涉及LLM的重排方法大致可以分为三类：
- 用重排任务**微调**LLM
- 使用**prompt**让LLM进行重排
- 以及利用LLM做训练数据的**增强**

#### 综述

【2023-12-20】[LLM in Reranking——利用LLM进行重排](https://mp.weixin.qq.com/s/I1gbHW_ZAE9J5HjB4cmRCw)

本文中针对前两种方法介绍一些研究。

排序学习方法主要分为 point-wise，pair-wise 以及 list-wise 三种思路，LLM通过prompt进行重排也类似。

LLM不同于传统的交叉编码器，具有更强的语义理解能力，并且能够捕捉到文档列表整体的顺序信息，它仍然面对几个不可忽视的问题。
- 一方面，LLM的输入长度对于一个文档列表来说还是十分受限的，必须通过滑动窗口或集成的方式才能实现文档输入。
- 另一方面，list-wise的LLM重排器对于输入非常敏感，在某些极端的情况下，例如将输入文档随机打乱顺序时，模型的输出结果甚至可能不如BM25。
- 另外，还有参数过剩与时效性的问题会导致LLM重排器难以落地。

参考综述：
- [Large Language Models for Information Retrieval: A Survey](https://arxiv.org/abs/2308.07107v2)

#### LRL

Zero-Shot Listwise Document Reranking with a Large Language Model

这篇文章与现有的 score and rank 的 point-wise打分方式不同，作者提出一种名为 Listwise Reranker with a Large Language Model (`LRL`) 的方法，利用 GPT-3 对文档进行 list-wise 的排序，直接生成候选文档的identifier序列实现重排, 这种list-wise的方法能够让模型同时关注到所有的文档信息

#### RankVicuna

- RankVicuna: Zero-Shot Listwise Document Reranking with Open-Source Large Language Models

RankVicuna 也是一种 Listwise 的LLM排序方法，但是不同于LRL，它是经过针对重排微调后的模型。
- 利用RankGPT-3.5作为教师模型在MS MARCO v1训练集中随机抽样的100K套训练集文档上生成数据，将RankGPT的能力蒸馏到7B的RankVicuna中。

#### PRP

- Large Language Models are Effective Text Rankers with Pairwise Ranking Prompting

作者提出利用LLM做list-wise与point-wise重排任务时，模型存在无法很好地理解排序指令的问题，并且在越小规模的模型中越显著。

作者认为这一问题有可能与预训练中缺少相应任务有关。

LLM应用于list-wise时出现的问题

针对这一问题，作者提出一种名为 pairwise ranking prompting (PRP) 的范式，设计了一种简单的prompt，结合了生成和打分的模型API，使得规模较小的开源模型也能够在公开数据集上实现SOTA.

#### PROMPTRANK

- Few-shot Reranking for Multi-hop QA via Language Model Prompting

本文中提出一种名为 PROMPTRANK 的框架，依靠prompting和多跳重排，可以在少样本的前提下解决复杂的多跳问答（MQA）。

多跳问答（multi-hop question answering, MQA）是指query对应多个文档，且回答问题需要结合召回的复数文档进行多步推理的场景。目前的MQA大多基于retrieve-then-read的pipeline，然而这种模式下往往需要大规模的训练数据，对低资源场景（如医疗、法律等特定领域）不友好。

#### LLMRank

【2023-5-15】人民大学发表论文：LLM用于推荐系统排序
- [Implementation of "Large Language Models are Zero-Shot Rankers for Recommender Systems"](https://arxiv.org/pdf/2305.08845.pdf)
- 代码[LLMRank](https://github.com/RUCAIBox/LLMRank)

将推荐问题形式化为条件排序任务，将历史交互作为条件，将召回得到的候选item作为候选。 

采用特定提示方法来应用LLM解决排序任务：包括**交互历史**、**候选item**和**排序指令**来设计提示模板。
- LLM 具有很有前途的**零样本**排序能力。
- LLM **难以感知历史交互顺序**，并且可能会受到位置偏差等偏差的影响，而这些问题可以通过专门设计的**提示和引导策略**来缓解。
- ![img](https://pic3.zhimg.com/v2-b15c0128a3bedddb1eccd71772eb7116_b.jpg)



### 写代码


#### NL2Code

【2023-5-30】[代码大模型综述：中科院和MSRA调研27个LLMs，并给出5个有趣挑战](https://mp.weixin.qq.com/s/t2SMftox6546E7kvRgQMnA)
- NL2Code: 将自然语言转换成可执行代码来提高开发人员的工作效率
- 中科院和微软亚洲研究院在 ACL 2023 国际顶会上发表的一篇综述：调研了 NL2Code 领域中的「27 个大型语言模型以及相关评价指标」，分析了「LLMs 的成功在于模型参数、数据质量和专家调优」，并指出了「NL2Code 领域研究的 5 个机遇挑战」，最后作者建立了一个分享[网站](https://nl2code.github.io)来跟踪 LLMs 在 NL2Code 任务上的最新进展。
- [Large Language Models Meet NL2Code: A Survey](https://arxiv.org/abs/2212.09420)


#### Cursor



### Document QA

详见专题：[文档问答](doc_chat)

### 推荐系统

【2024-1-20】[谈谈AI落地容易的业务-搜广推](https://mp.weixin.qq.com/s/aqDS-nInC97uvLaK8J_DiA)
- 推荐系统适用场景：**信息过载**时提供**信息匹配**价值
- 推荐系统技术路线
  - 早期搜索推荐采用**竞价排名**，早期的百度凤巢有一系列问题，`戴文渊`利用**LR算法**改进凤巢，和`陈雨强`又引入了**深度学习**， `陈雨强`又在今日头条担任过架构师。
  - 另一个主线: 阿里妈妈为代表的**电商广告**，从`盖坤` 2011年提出分片**线性模型MLR**开始，到后面通过类似于**Wide&Deep算法**，构建`GwEN`，再到针对用户兴趣建模提出`DIN`，以及将Attention和GRU引入用户兴趣构建的`DIEN`，但是用户兴趣序列长度有限制，又引入异步机制User Interest Center并构建`MIMN`算法对长期行为建模。再到后期提出Search Based Interest Model(`SIM`)，并针对用户不同的行为构建基于Session的分类的Deep Session Interset Network(`DSIN`)，在针对特征间的交互(Co Action)构建的`CAN`，当然还有召回中的利用树结构构建的TDM算法，和利用图结构的二项箔算法等。
- 推荐系统组件
  - **两阶段**模型：`召回`+`排序`
  - 工业级推荐系统用**四阶段**模型：`召回`，`粗排`，`精排`和`重排`。
    - 原因：整个环节上对延迟有严格的需求，通常要求端到端延迟低于100ms，因此需要构建**逐级过滤**的算法实现。


<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-01-20T09:18:51.913Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\&quot; etag=\&quot;NmeZhpZLXT-p41geF3cQ\&quot; version=\&quot;22.1.18\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;VC8KsEmwTz_4FKU3JA4y\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;701\&quot; dy=\&quot;785\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;KqnMbKhnpt-NfbrPkSTS-22\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#B3B3B3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-1\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;570.0999999999999\&quot; y=\&quot;460\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-7\&quot; value=\&quot;推荐系统组件\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=20;strokeWidth=2;fontFamily=Verdana;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;624.5\&quot; y=\&quot;340\&quot; width=\&quot;140\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KqnMbKhnpt-NfbrPkSTS-2\&quot; value=\&quot;2024-1-20\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#3333FF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;637\&quot; y=\&quot;370\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KqnMbKhnpt-NfbrPkSTS-44\&quot; value=\&quot;处理数据量大&amp;lt;br&amp;gt;速度要&amp;lt;font color=&amp;quot;#ff0000&amp;quot;&amp;gt;足够快&amp;lt;/font&amp;gt;&amp;lt;br&amp;gt;模型不能太复杂&amp;lt;br&amp;gt;使用较少特征\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#0000FF;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;537\&quot; y=\&quot;610\&quot; width=\&quot;100\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-1\&quot; value=\&quot;All Items\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;330\&quot; y=\&quot;510\&quot; width=\&quot;90\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-2\&quot; value=\&quot;\&quot; style=\&quot;shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;rotation=90;fillColor=#dae8fc;strokeColor=#6c8ebf;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510\&quot; y=\&quot;515\&quot; width=\&quot;120\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-3\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;Millions 百万级别&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; y=\&quot;515\&quot; width=\&quot;100\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-4\&quot; value=\&quot;阶段1：召回\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1;labelBackgroundColor=none;fillColor=#f5f5f5;fontColor=#333333;strokeColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;532.5\&quot; y=\&quot;450\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-5\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;Candidate Generation&amp;lt;br&amp;gt;候选Item生成&amp;lt;br&amp;gt;&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontStyle=1;labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540\&quot; y=\&quot;550\&quot; width=\&quot;140\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-6\&quot; value=\&quot;\&quot; style=\&quot;shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;rotation=90;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;735.5\&quot; y=\&quot;515\&quot; width=\&quot;83\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-7\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#B3B3B3;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-2\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-6\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;614\&quot; y=\&quot;535\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;734\&quot; y=\&quot;535\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-8\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;Hundreds 百级别&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;620\&quot; y=\&quot;515\&quot; width=\&quot;100\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-9\&quot; value=\&quot;阶段2：排序\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1;labelBackgroundColor=none;fillColor=#f5f5f5;fontColor=#333333;strokeColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;739.5\&quot; y=\&quot;450\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-10\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;Candidate Ranking&amp;lt;br&amp;gt;候选Item排序&amp;lt;br&amp;gt;&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontStyle=1;labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;750\&quot; y=\&quot;540\&quot; width=\&quot;140\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-11\&quot; value=\&quot;\&quot; style=\&quot;shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;rotation=90;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;900\&quot; y=\&quot;515\&quot; width=\&quot;50\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-13\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#B3B3B3;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-6\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-11\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;610\&quot; y=\&quot;555\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;757\&quot; y=\&quot;555\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-14\&quot; value=\&quot;处理数据量小&amp;lt;br&amp;gt;模型要&amp;lt;font color=&amp;quot;#ff0000&amp;quot;&amp;gt;足够精准&amp;lt;/font&amp;gt;&amp;lt;br&amp;gt;模型可以复杂&amp;lt;br&amp;gt;使用较多特征\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#0000FF;fontStyle=1;labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;739.5\&quot; y=\&quot;600\&quot; width=\&quot;100\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-15\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;推荐结果&amp;lt;br&amp;gt;&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontStyle=1;labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;900\&quot; y=\&quot;535\&quot; width=\&quot;63\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-16\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#B3B3B3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-17\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-18\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;570.0999999999999\&quot; y=\&quot;800\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-17\&quot; value=\&quot;All Items\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;330\&quot; y=\&quot;850\&quot; width=\&quot;90\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-18\&quot; value=\&quot;\&quot; style=\&quot;shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;rotation=90;fillColor=#dae8fc;strokeColor=#6c8ebf;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; y=\&quot;855\&quot; width=\&quot;120\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-19\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;千万&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; y=\&quot;855\&quot; width=\&quot;30\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-20\&quot; value=\&quot;\&quot; style=\&quot;shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;rotation=90;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;537\&quot; y=\&quot;855\&quot; width=\&quot;100\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-21\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#B3B3B3;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-18\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-20\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;614\&quot; y=\&quot;875\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;734\&quot; y=\&quot;875\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-22\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;万&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;532.5\&quot; y=\&quot;855\&quot; width=\&quot;20\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-23\&quot; value=\&quot;\&quot; style=\&quot;shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;rotation=90;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;900\&quot; y=\&quot;855\&quot; width=\&quot;50\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-24\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#B3B3B3;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-32\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-23\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;610\&quot; y=\&quot;895\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;757\&quot; y=\&quot;895\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-25\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;推荐结果&amp;lt;br&amp;gt;&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontStyle=1;labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;893.5\&quot; y=\&quot;875\&quot; width=\&quot;63\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-26\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;召回&amp;lt;br style=&amp;quot;font-size: 16px;&amp;quot;&amp;gt;&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontStyle=1;labelBackgroundColor=none;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;472.5\&quot; y=\&quot;870\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-28\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;粗排&amp;lt;br style=&amp;quot;font-size: 16px;&amp;quot;&amp;gt;&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontStyle=1;labelBackgroundColor=none;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;567\&quot; y=\&quot;870\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-29\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;召回&amp;lt;br style=&amp;quot;font-size: 16px;&amp;quot;&amp;gt;&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontStyle=1;labelBackgroundColor=none;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;550\&quot; y=\&quot;505\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-30\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;排序&amp;lt;br style=&amp;quot;font-size: 16px;&amp;quot;&amp;gt;&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontStyle=1;labelBackgroundColor=none;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;757\&quot; y=\&quot;510\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-31\&quot; value=\&quot;\&quot; style=\&quot;shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;rotation=90;fillColor=#e1d5e7;strokeColor=#9673a6;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;687\&quot; y=\&quot;855\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-33\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#B3B3B3;exitX=0.5;exitY=0;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-20\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-31\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;662\&quot; y=\&quot;885\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;895\&quot; y=\&quot;885\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-32\&quot; value=\&quot;\&quot; style=\&quot;shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;rotation=90;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;792.12\&quot; y=\&quot;855\&quot; width=\&quot;55.75\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-34\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;精排&amp;lt;br style=&amp;quot;font-size: 16px;&amp;quot;&amp;gt;&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontStyle=1;labelBackgroundColor=none;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;699.5\&quot; y=\&quot;870\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-35\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#B3B3B3;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-31\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-32\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;660\&quot; y=\&quot;895\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;702\&quot; y=\&quot;895\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-37\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;重排&amp;lt;br style=&amp;quot;font-size: 16px;&amp;quot;&amp;gt;&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontStyle=1;labelBackgroundColor=none;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;797\&quot; y=\&quot;870\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-38\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;千&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;660\&quot; y=\&quot;855\&quot; width=\&quot;20\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-39\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;千/百&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;757\&quot; y=\&quot;855\&quot; width=\&quot;33\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-41\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-40\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-18\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-40\&quot; value=\&quot;表示学习\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;450\&quot; y=\&quot;750\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-45\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-42\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-20\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-47\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-42\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-31\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-42\&quot; value=\&quot;用户特征\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;620\&quot; y=\&quot;710\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-48\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.25;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-43\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-31\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;740\&quot; y=\&quot;860\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-49\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.25;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-43\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-20\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-43\&quot; value=\&quot;物料特征\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;620\&quot; y=\&quot;760\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-44\&quot; value=\&quot;交叉特征\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;640\&quot; y=\&quot;800\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-50\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF0000;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-42\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;500\&quot; y=\&quot;790\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;660\&quot; y=\&quot;760\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-51\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF0000;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-43\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-44\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;670\&quot; y=\&quot;750\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;670\&quot; y=\&quot;770\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-52\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF0000;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.75;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;pv1TiN8nKofBFrHRIT3c-44\&quot; target=\&quot;pv1TiN8nKofBFrHRIT3c-31\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;670\&quot; y=\&quot;800\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;678\&quot; y=\&quot;810\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-53\&quot; value=\&quot;两阶段模型\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1;labelBackgroundColor=none;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;200\&quot; y=\&quot;535\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;pv1TiN8nKofBFrHRIT3c-54\&quot; value=\&quot;工业界&amp;lt;br&amp;gt;四阶段模型\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1;labelBackgroundColor=none;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;210\&quot; y=\&quot;875\&quot; width=\&quot;75\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


详见站内[推荐系统专题](rp)



#### LLM + RS 应用综述

【2023-6-17】[基于LLM的推荐系统全面综述](https://zhuanlan.zhihu.com/p/634534308), 将基于LLM的推荐系统分为两大范式，方法、技术和性能的洞察，分别是
- 用于推荐的判别型LLM（DLLM4Rec）
- 用于推荐的生成型LLM（GLLM4Rec），首次被系统地整理出来。

大型语言模型（LLMs）融入推荐系统的关键优势
- 能提取高质量的**文本特征表示**，并利用其中编码的广泛外部知识 \[Liu等人，2023b\]

范式总结
- (1) <span style='color:blue'>LLM Embeddings + RS</span>。这种建模范式将语言模型视为**特征提取器**，将物品和用户的特征输入到LLM中并输出相应的嵌入。传统的RS模型可以利用**知识感知嵌入**进行各种推荐任务。
- (2) <span style='color:blue'>LLM Tokens + RS</span>。与前一种方法类似，根据输入的物品和用户的特征**生成token**。生成的令牌通过语义挖掘捕捉潜在的偏好，可以被整合到推荐系统的决策过程中。
- (3) <span style='color:blue'>LLM作为RS</span>。与(1)和(2)不同，这个范式的目标是直接将预训练的LLM转换为一个强大的**推荐系统**。输入序列通常包括简介描述、行为提示和任务指示。输出序列预计会提供一个合理的推荐结果。
- ![img](https://pic3.zhimg.com/80/v2-10d4fc0aaf05736a5915dd281a326ee2_1440w.webp)

推荐的**判别式LLM**和**生成式LLM**。
- **判别式**语言模型非常适合在范式(1)中嵌入
  - 判别性语言模型主要是指BERT系列的模型
  - ![](https://pic1.zhimg.com/80/v2-775c803c461316ae550cd6f4b7ab63b0_1440w.webp)
- 而**生成式**语言模型的响应生成能力进一步支持范式(2)或(3)。
  - 相比于判别型模型，生成型模型具有更好的自然语言生成能力。
  - 因此，不像大多数基于判别模型的方法**将LLMs学习到的表示与推荐领域对齐**，大多数基于生成模型的工作将**推荐任务**翻译为**自然语言任务**，然后应用像在上下文中学习，提示调优，和指导调优这样的技术，来适应LLMs直接生成推荐结果。
- ![img](https://pic3.zhimg.com/80/v2-cf281f562afd8340e465360e4f8f2dc6_1440w.webp)

【2023-5-20】[当推荐系统遇到大模型](https://mp.weixin.qq.com/s/YaFQoqAt12y93Nm3tX_j4A)

ChatGPT在推荐系统中的应用有不小的潜力，主要体现在以下几个方面：
- **任务统一**：所有类型的推荐任务都可以表述成**文本**，实现了推荐任务大统一，使用统一语言模型进行各个场景和任务上的推荐，有效解决多任务、多场景问题。
- **小样本**和**冷启动**问题：传统推荐系统中，小样本和冷启动是一个比较常见的问题，而大模型天然具备很强的**语义泛化能力**和**小样本学习**能力。
- 基础的推荐能力验证：多篇文章已经验证了ChatGPT等模型在推荐系统中应用是可行的，即使不在下游任务finetune，也能取得不错的效果

【2023-11-17】人民大学高瓴AI学院 徐君: [当大语言模型遇见推荐系统](https://zhuanlan.zhihu.com/p/667420567)
- 【2023-8-24】论文: RecSys 2023 [Uncovering ChatGPT’s Capabilities in Recommender Systems](https://arxiv.org/pdf/2305.02182.pdf)
- 代码 [LLM4RS](https://github.com/rainym00d/LLM4RS), 包含电影、书籍、音乐与新闻等domain上实践

LLM 做推荐两个思路：
- 将LLM当作backbone: 训练时的strategy，适应某个推荐任务。
  - 早期的`BERT4Rec`，训练时让模型猜测，如果少了一个item，这个item应该是什么，由模型补上这个item。
  - `UniSRec`，用 pre-train 和 fine-tune 流程。
  - `P5`，用 pre-train和promting 流程。
- 把LLM当作推荐系统的**补充**。
  - 把LLM当作一个**embedding生成器**，生成更好的user、item以及context的表达，换句话说，LLM可以辅助理解用户。
  - 用LLM生成一段文字描述来用户。然后把LLM带来的附加信息加入现有的推荐模型中去。

要点
1. Key Tasks：Top-K Ranking of Items
  - 交互页面稳定时, 关键是选取Top-K的items，再排序
  - 三种方式
  - `Point-wise ranking`。假设有5个items，直接询问大模型对这5个item的打分。这种方式最大程度模拟了业界推荐模型的工作方式，因为在线侧每一个item都会询问一次大模型，所以是Point-wise的方式。
  - `Pair-wise ranking`。每次选取两个items去问大模型，哪个才是更适合用户的结果，哪个才是用户更喜欢的item，大模型会告诉我们一个答案。这样的话，如果我们有n个item，那么我们最多问 n*(n-1)/2次，就能得到n个item的排序。
  - `List-wise ranking`。这种方式是个挑战，直接询问大模型n个item的排序方式，相当于直接把大模型当成item排序结果的生成器。
2. LLMs for Recommendation: Overall Evaluation Procedure
  - Prompt的构建包括三部分。
  - 第一部分是Task Description，指出是哪种推荐系统，比如电影推荐系统，相当于指定推荐的domain；
  - 第二部分是Demonstration Examples，告诉模型想让它做出什么样的动作；
  - 最后是New Input Query，想要问的问题。通过这个template，基于是否要in-context learning，就构造出了一个prompt。将这个prompt给到LLM，LLM就会按照它的生成方式，输出一段话，再从这段话中提取出答案。有时这个答案可能是不符合要求的，就需要一个exception处理流程。

分别在电影、书籍、音乐与新闻等domain数据上面，验证了ChatGPT等大模型的表现，并给出了相关实验结论。

#### 最新论文

论文
- 【2023-1-2】Recommendation as language processing (rlp): A unified pretrain, personalized prompt & predict paradigm
  - P5将各类推荐任务通过**prompt形式**全都转换成**统一文本**，然后利用这些文本训练一个 Transformer Encoder-Decoder模型。P5利用语言模型解决推荐系统问题，由于各种推荐系统任务都能表述成文字，使得统一建模各类推荐系统任务成为了可能。
  - prompt构造方法：针对每种任务设计一个prompt模板，对于**商品信息**、**用户信息**等，直接将id作为本文输入。P5在这种文本上训练，对于商品和用户id相当于都当成一个独立的词进行embedding的学习。
- 【2023-4-4】[Chat-REC: Towards Interactive and Explainable LLMs-Augmented Recommender System](https://arxiv.org/abs/2303.14524)
  - Chat-REC将ChatGPT应用到推荐系统中，**会话推荐系统**, 具有交互式和可解释的能力，验证了大模型在**一般推荐场景、跨域推荐、冷启动推荐**等场景下都有着不错的表现。
  - Chat-REC核心：将包括**用户特征、搜索词、用户和item的历史交互信息、历史对话信息**等一系列信息，输入到一个Prompt Constructor中，自动生成一个prompt。这个prompt输入到ChatGPT中，让ChatGPT生成推荐结果，或者解释推荐利用。
  - 通过这种方式让推荐系统能够产生**可解释**的推荐结果，例如在对话过程中，可以询问对话系统推荐的原因，prompt会将推荐系统给到的结果和用户的问题输入Prompt Constructor，生成新的prompt，让ChatGPT生成对应的解答。
  - Chat_REC整体利用了ChatGPT优化原有的推荐系统，让其能够实现更丰富的用户和推荐系统的交互。
- 【2023-5-11】A First Look at LLM-Powered Generative News Recommendation
  - 利用大模型来提升**新闻推荐系统**的效果。新闻推荐系统中存在很多挑战，一方面新闻标题可能不含实际内容的关键词，需要更深入的**语义理解**；另一方面对于**用户特征缺失、冷启动**等情况，推荐效果也会变差。
  - 这篇文章利用大模型进行**title扩展、用户特征生成、解决冷启动**等问题。
  - 构造prompt，进行3方面的数据扩充，再利用扩展出的数据进行下游新闻推荐系统模型的训练
    - 为了在新闻标题中补充更丰富的信息，设计了一个**摘要prompt**，根据title和新闻信息生成扩展后的title。
    - 为了补充**用户特征**，利用用户历史的浏览行为，生成指定的相关特征。
    - 最后，对于**冷启动**用户，利用用户少量的历史浏览行为，让大模型生成更多用户可能感兴趣的新闻信息。
- 【2023-5-12】Is ChatGPT Fair for Recommendation? Evaluating Fairness in Large Language Model Recommendation
  - 研究利用大模型进行推荐时是否存在**公平性**问题。
  - 公平性问题：用户侧一些敏感属性的特征，可能会引起大模型产出不公平的推荐结果，因为大模型经过大规模语料进行训练，其中会存在这样的有偏信息。
  - 为了对这个问题进行实验和验证，构建了大模型推荐系统公平性的benchmark，在评估时基础做法是生成一些instruction产出推荐结果，再在instruction中插入各种敏感词对比推荐结果，判断推荐结果因为敏感词插入造成的差异大小。差异越大，说明大模型用于推荐系统存在的不公平现象越严重。
- 【2023-4-20】[Is ChatGPT a Good Recommender? A Preliminary Study](https://arxiv.org/abs/2304.10149)
  - 通过5种类型的推荐任务评估ChatGPT在推荐系统中应用的效果。这5个任务包括：**排序预测** rating prediction、**序列推荐** sequential recommendation、**直接推荐** direct recommendation、**可解释生成** explanation generation、总结 review summarization等。[解读](https://juejin.cn/post/7230094051470606393)
  - `评分预测`：评分预测旨在预测用户对特定项目的评分，如上图所示，黑字部分代表任务的描述，评分预测被翻译为“How will user rate this product_title?”，灰字表示当前的输入，即要求用户评分的项目，红字表示针对输出的格式要求，在评分预测任务中，要求有“1 being lowest and 5 being highest”和“Just give me back the exact number a result”；
  - `序列推荐`：序列推荐任务要求系统根据用户过去的序贯行为预测其之后的行为，如上图所示，论文为该任务设计了三种 Prompt 格式，分别是基于交互历史直接预测用户的下一个行为，从候选列表中选出可能的下一个行为以及判断指定行为成为用户下一个行为的可能性；
  - `直接推荐`：直接推荐指通过利用用户评分或评论信息直接显示反馈推荐的任务，论文将这一任务的 Prompt 设计为从潜在的候选项中选择出最适合的一项；
  - `解释生成`：解释生成是为用户提供解释以澄清为什么会推荐此项的推荐系统任务，具体地，如上图所示，论文要求 ChatGPT 生成一个文本解释，以阐明解释生成过程，对每个类别，可以包含如提示词或星级评分等的辅助信息；
  - `评论总结`：旨在使用推荐系统自动生成用户评论摘要。通过输入用户的评论信息，Prompt 提示推荐系统总结评论的主要含义。
  - 针对这5种任务分别设计了相应的prompt，输入到ChatGPT中生成预测结果。5种任务的prompt构造例子，每个prompt都包含：任务描述、格式声明以及一些user和item交互的例子，以给ChatGPT提供few-shot信息。
  - 从推荐系统**准确率**相关指标来看（如hit rate等），ChatGPT在rating任务上表现比较好，但是在其他任务上表现比较差。但是如果人工评估的话，ChatGPT的结果是比较好的，这说明使用推荐系统指标评估ChatGPT也是有局限性的。同时，文中的ChatGPT并没有在推荐系统数据上进行finetune，就能达到这样的效果，也表明了ChatGPT在推荐系统中的落地是非常有潜力的。
- 【2023-5-11】Uncovering ChatGPT’s Capabilities in Recommender Systems（2023.5.11）
  - 尝试挖掘ChatGPT在推荐系统中3类任务的能力，包括`point-wise`、`pair-wise`、`list-wise`三类推荐系统面临的给定user推荐item的任务。
  - 针对这3类任务，文中构造了如下3类prompt。每类prompt包括**任务描述、例子、当前的问题**三个部分。
  - 3类任务的prompt主要差别是当前问题的组织形式: point-wise就直接问ChatGPT**打分是多少**，pair-wise给两个item让模型做**对比**，list-wise则是对item做**排序**。
  - 整体实验结果: 主要是对比了ChatGPT和一些基础推荐方法（随机推荐、根据商品流行度推荐）的差异，初步能够证明ChatGPT是具备一定的推荐能力的，其中在list-wise类型的任务上能获得最高的性价比。

#### 大模型对推荐影响

【2023-5-12】[gpt4这种大模型能力对推荐系统这个领域有什么影响？](https://www.zhihu.com/question/591580147)

结论：
- 短期内，不会对推荐系统有大的影响。
- 长期看，对推荐系统的影响体现在
  - 大模型催生**新的业务场景**：比如基于问答的推荐场景，当用户查询旅游攻略时，除了常规的线路规划，还可以给出基于用户偏好的酒店，餐厅推荐候选。在这类的场景下，搜索和推荐相比当前的交互，会更加融合。
  - 大模型提升**生产力**，导致垃圾内容泛滥：如何识别aigc 内容，降低该类内容对内容生态冲击，流量蚕食会是未来的一个新命题。
  - 大模型在用户关怀上的应用：通过内容生产能力，为用户产生**不同风格化评论**，对创作者进行促活，也是一个比较有潜力的应用，现在的生成模型缺乏内容理解和产出风格化的能力。
  - 大模型对**内容理解能力**的提升，使推荐朝**端到端**的方向发展：当前推荐建模依赖大量**离散**特征以及**统计后验**特征，如果未来能通过大模型的内容理解能力，直接匹配用户理解，这样端到端的新范式，会重塑推荐系统的发展线路。

推荐大模型最有可能的路线
- 借助语言图像类大模型的**内容理解能力**，把对内容的理解固定在一个稳定的embedding 空间，完全替代掉推荐模型里的itemid类稀疏特征，在系统层面，真正的学到推荐“知识”，并具有大规模泛化能力，这是最令我激动和充满热情的技术路线。

作者：[手套销售拉呱总](https://www.zhihu.com/question/591580147/answer/3006390042)

#### 提示学习与推荐

随着prompt learning在nlp的出色表现，也开始向cv，向多模态进行扩展，当然，也有不少研究人员用它来解决推荐系统问题。

【2022-8-29】提示学习用于推荐系统问题
- [PPR，PFRec](https://nakaizura.blog.csdn.net/article/details/126572223)
- [PEPLER，P5，PRL](https://nakaizura.blog.csdn.net/article/details/124558817)

论文
- KDD  2022： [Towards Unified Conversational Recommender Systems via Knowledge-Enhanced Prompt Learning](https://dl.acm.org/doi/10.1145/3534678.3539382), [解读](https://blog.csdn.net/qq_27590277/article/details/128017508)
  - 会话推荐系统 (下面简称为：`CRS`) 旨在通过自然语言对话主动引发用户偏好并推荐高质量的项目。通常，CRS 由一个推荐模块（用于预测用户的首选项目）和一个对话模块（用于生成适当的响应）组成。
  - 提出了一种统一的 CRS 方法，即基于 PLM 的知识增强型即时学习，`UniCRS`。

#### Chat-Rec

【2023-4-4】[Chat-REC: 当推荐系统遇上 ChatGPT, 会发生什么奇妙反应](https://mp.weixin.qq.com/s/ulV8R72zSStdwwNfhtys_g)，[解说](https://zhuanlan.zhihu.com/p/619161007)
- [Chat-REC: Towards Interactive and Explainable LLMs-Augmented Recommender System](https://arxiv.org/abs/2303.14524)

推荐系统已被广泛部署用于自动推断人们的偏好并提供高质量的推荐服务。然而大多数现有的推荐系统仍面临诸多缺陷，例如缺少交互性、可解释性，缺乏反馈机制，以及冷启动和跨域推荐。

本文中提出了一种用 LLMs 增强传统推荐的范式 `Chat-Rec`（ChatGPT Augmented Recommender System）。通过将**用户画像**和**历史交互**转换为 Prompt
- Chat-Rec 将用户与物品的历史交互、用户档案、用户查询 和对话历史 （如果有的话）作为输入，并与任何推荐系统R接口。
- 如果任务被确定为推荐任务，该模块使用 R 来生成一个候选项目集。否则，它直接向用户输出一个响应，如对生成任务的解释或对项目细节的要求。提示器模块需要多个输入来生成一个自然语言段落，以捕捉用户的查询和推荐信息。这些输入如下：
  1. 用户与物品的历史交互，指的是用户过去与物品的互动，比如他们点击过的物品，购买过的物品，或者评价过的物品。这些信息被用来了解用户的偏好并进行个性化推荐。
  2. 用户画像，其中包含关于用户的人口统计和偏好信息。这可能包括年龄、性别、地点和兴趣。用户资料有助于系统了解用户的特点和偏好。
  3. 用户查询 Qi ，这是用户对信息或建议的具体要求。这可能包括他们感兴趣的一个具体项目或流派，或者是对某一特定类别的推荐的更一般的请求。
- ![](https://pic3.zhimg.com/80/v2-234ea3011f274c43cda0a6d233cb7d8a_1440w.webp)
- Chat-Rec 的框架。左边显示了用户和 ChatGPT 之间的对话。中间部分显示了 Chat-Rec 如何将传统的推荐系统与 ChatGPT 这样的对话式人工智能联系起来的流程图。右侧描述了该过程中的具体判断。
- 对于一个用户query：“你能推荐一些动作片给我吗？”。
- 确定这个query是否是一个推荐任务【ChatGPT来判断】
  - 如果是推荐任务，则使用该输入来执行“推荐动作电影”模块。但由于推荐空间是巨大的，所以该模块需要分为两个步骤：1推荐系统产生一个少量的候选得到top20的推荐结果，2然后再进行重新排序和调整【ChatGPT来重排】，以生成top5的最终输出。这种方法可以确保向用户展示一个更小、更相关的物品集，增加他们找到自己喜欢的东西的可能性。
  - 如果不是推荐任务，如用户询问“为什么会推荐你会推荐fargo电影给我”。系统将使用电影标题、历史记录交互和用户配置文件作为输入来执行对推荐模块的解释【ChatGPT来生成解释】。

由于ChatGPT的输入是自然语言文本，所以中间模块的主要目标：
- 如何利用用户与物品的历史交互、用户档案、用户查询和对话历史 （如果有的话）等等多个输入ChatGPT来生成一个自然语言段落，以捕捉用户的查询和推荐信息。
- User-item history interactions：用户与物品的历史交互，指的是用户过去与物品的互动，比如他们点击过的物品，购买过的物品，或者评价过的物品。
- User profile：用户画像，其中包含关于用户的人口统计和偏好信息，如年龄、性别、地点和兴趣。
- User query Qi：查询句子，可能是推荐任务也可能是通用任务。
- History of dialogue Hi : 用户和chatgpt之间的所有上下文 

对于topk推荐任务来说，生成的prompt例子

如何解决**冷启动**？

大模型中拥有很多知识，利用商品文字描述就能够借助LLM的力量来帮助推荐系统缓解新项目的冷启动问题，即没有大量用户互动也可以得到embedding。

两种chatGPT难以执行推荐场景：
- 1 让不能联网的chatGPT推荐2023最新的动作电影；
- 2 让chatGPT推荐一个它知识储备中没有的动作电影。

因此，离线利用LLM来生成相应的embedding表征并进行缓存。从而在当chatGPT遇到新的物品推荐时，会首先计算离线商品特征和用户query特征之间的相似性，然后检索最相关商品一起输入到 ChatGPT 进行推荐。

如何解决**跨域**推荐？

类似的，LLM中的知识可以很方便，对不同领域的商品有认知，如电影，音乐和书籍等等，并且还能够分清楚在不同领域产品之间的关系。

因此，直接依靠chatGPT把上下文对话输入一起编码进chatGPT的输入后，就能在用户询问关于其他类型作品的建议时，实现跨域推荐，如对书籍、电视剧、播客和视频游戏进行推荐。

从top5推荐和评分预测这个俩结果上来看，似乎text-davinci-003才是最好的

- `Chat-Rec` 可以有效地学习用户的偏好，它<span style='color:blue'>不需要训练，而是完全依赖于上下文学习</span>，并可以有效推理出用户和产品之间之间的联系。通过 LLM 的增强，在每次对话后都可以迭代用户偏好，更新候选推荐结果。

此外，产品之间的用户偏好是相关联的，这允许更好的跨域产品推荐。Chat-Rec 为运用 ChatGPT 等对话 AI 进行多种推荐情景的应用提供了有希望的技术路线。

#### 商品推荐

定制化商品推荐，告别传统“傻瓜”推荐算法
- 当下国内众多电商的推荐算法都还是基于传统技术，因此也会出现“买过的东西依然推荐”的傻瓜做法，AI大模型有望彻底改变这些业态

ChatGPT有一些营销场景应用是围绕垂直领域展开，革新推荐算法逻辑，让产品卖点更精准地触达目标客户。
- 海外生鲜电商平台`Intacart`的食物搜索工具，其基于ChatGPT推出了面向食物推荐的应用，与自身来自75000多零售合作商店的产品数据结合了起来，帮助客户找到购物的灵感。
- 美国一款名为`Expedia`软件内置了一个聊天机器人，通过AI大模型算法为用户规划旅游。有人经历过用ChatGPT规划旅游被推荐一个不存在的海滩，能够在iOS上轻便运行的Expedia据称不会出现这个问题。Expedia会根据旅游地推荐经济实惠的酒店，建议可以打卡的景点，是大模型落地垂直旅游行业的一个代表应用案例。




#### InstructRec

利用LLM的用户推荐，便于将用户偏好或需求用自然语言描述来表达，因此instruct tuning是非常适合的方案。
- [Recommendation as Instruction Following: A Large Language Model Empowered Recommendation Approach](https://arxiv.org/pdf/2305.07001.pdf)
- 开源LLM（3B的 Flan-T5-XL）进行指令调优来适应推荐系统。[原文解读](Chat-REC、InstructRec（LLM大模型用于推荐系统）)
- 模型流程：用户直接给出instructions如“I prefer”，然后历史记录和用户指定将一起输入formulation模块中，生成模型能够理解的instructions形式，然后输入到大模型中，最后可以完成各种任务如sequential recommendation、product search、personalized search等。

该工作最重要的模块就是通用指令的设计，以全面地描述用户的偏好、意图、任务形式。
- **偏好**（Preference）。指用户偏好。其中隐式偏好用商品标题而非id，显式偏好用用户query中的明确表达（如用户评论），而不是之前的评分或点赞。
- **意图**（Intention）。指用户对某些类型的物品的需求。模糊的意图如“给我儿子的一些礼物”、具体的意图如“蓝色、便宜、iPhone13”）。
- **任务形式**（Task Form）。要做到统一的推荐系统，需要有适应各种任务的能力。
  - `Pointwise`。某个候选商品是否适合用户，那么直接用用户需求和商品特征来匹配。
  - `Pairwise`。让LLM从item pairs中选择更合适的一个即可。
  - `Matching`。`召回`模块，LLM从整个商品语料库中生成候选集合。
  - `Reranking`。`排序`模块，LLM从候选中重排序商品。

### 个人助理

#### ChatGPT微头条

【2023-6-6】用ChatGPT发微头条
- [视频](https://www.toutiao.com/video/7230002985866035769)

#### Monica

【2023-4-12】[Monica](https://monica.im/), 一款浏览器插件，AI个人助理，功能：
- 快捷指令：网页上任意选择文本，即可翻译、解释、改写、总结、使用自己的提示
- 随处聊天：随时开启聊天窗
- 写作：轻松创作文案、邮件、博客等

使用 GPT-4驱动，免费用户又30次查询，每邀请一个好友，就有100次额度，其中1次GPT-4、4次AI作画
- Monica is an AI assistant powered by GPT-4. Register now to receive 100 free GPT Queries, including GPT-4, GPT-3.5, and AI Drawing. [邀请链接](https://monica.im/?c=CDM9HW5C)

#### Smart Siri

【2023-6-13】[用 ChatGPT 武装 Siri 有啥用途？](https://mp.weixin.qq.com/s/iVoI0t3qbpPEbDfIKgOhMA)

ChatGPT的 app 更新后，能直接和 Siri、快捷指令（Shortcuts）联动，这样，Siri 就能用上 ChatGPT 的能力了。
-  iOS 版本是 16.1 及以上，应用才能兼容使用

智能助理的槽点：
- “Siri 是人工智障”
- 由于 Siri 更强调在用户设备端计算，需要保护个人隐私，只能做些特定任务，比如：查天气、定闹钟；

但当 Siri 接入 ChatGPT 后，执行任务的角色就被后者接替了，想象空间变得更大了。
- 方法一: 快捷指令基于 ChatGPT API 接口进行 JSON 格式的发送获取，发送和解析过程都会消耗很长时间，也会占用更多的 ChatGPT key 余额。
- 方法二: 官方 app 接口可以直接省去用户打包数据提取数据的过程，直接向 app 发送请求并获取有效信息。中间省去了受网络波动、ChatGPT 用户过多、key 余额不足等因素的影响
  - 不用懂有门槛的 JSON 语言，不用写代码，把自己的发问需求细化成小步骤，找到能实现对应任务的 app，像乐高积木一样拼起来就行了。

“Smart Siri”: 升级版 Siri 可直接用语音发问，对于明确的、具体的发问，提炼得更好。
- 直接喊“Hey Siri + Smart Siri”，等待，看到“Yes”后，就能开始问问题了
- 工具：[ios下载地址](https://routinehub.co/shortcut/14389/), [Access-chatGPT-in-Siri](https://github.com/Daiyimo/Access-chatGPT-in-Siri): Siri接入ChatGPT指南。目前仅限iPhone端及其他支持快捷指令的Apple产品，后续会更新Android版本。
- ![](https://github.com/Daiyimo/Access-chatGPT-in-Siri/raw/main/images/%E8%B0%83%E7%94%A8%E5%AE%98%E6%96%B9%E6%8E%A5%E5%8F%A3.jpg)

分析
- Siri 的表现相对刻板，它仅能提供网址以及内容概括，有时会直接告知未找到相关信息，仿佛是被束缚的人工智能
- Smart Siri 则能立即提供不错的回答，简洁明了，看起来的确挺聪明的。

|案例|Siri|Smart Siri|分析|
|---|---|---|---|
|宫保鸡丁|我在网上找到了这个结果:...|宫保鸡丁的正宗做法:1,2,3,...|直接给出做法|
|光年之外有什么故事|搜索光年之外信息|《光年之外》是邓紫棋2016年发布的歌曲，灵感来自电影《星际穿越》...|直接解答|
|用小红书格式写个朋友圈|依旧是搜索...|端午节朋友圈文案：1. 与美好生活一见“棕”情 2. 无论咸甜,阖家团圆才是最好的陷...||
|帮我写个毕业季微电影的拍摄脚本|我在网上找到了这个结果:...|拍摄脚本|直接给出做法|

微博博主 @[Sunbelife](https://weibo.com/n/Sunbelife) 展示的几个玩法，比如
- 把 iPhone 内的睡眠数据（步数等健康数据）打包，让 ChatGPT 接入分析，最后生成一个“每日健康分析报告”——这个过程还可以是完全自动化的。
- 智能家居: 
  - 授权chatgpt app读取家庭数据,对智能家居进行开关、自动化及预处理，对气温、温度提出有效建议
- 跨境电商分析场景：
  - 解析电商规则，SEO优化、选品、广告优化、商品详情页优化、关键词优化、客服与售后自动化
  - 不用打开其他app，直接用Siri体温，获取答案，优化

苹果在 WWDC（苹果年度开发者大会）上并没有像其他科技巨头那般谈论（甚至吹捧）AI 大模型，但在一些小功能上，也都是基于 AI 去研发和改进的。比如
- 打字，在 iOS 17 上，键盘上的错字自动纠正、打字实时预测（机器甚至能准确联想到一整句你最想表达的话）等功能
- 这些都基于使用 Transformer 语言模型的 ML 程序开发。

Smart Siri 不足：
- ChatGPT 还无法实现连续对话，不过可以把之前的聊天记录粘贴进当前要问的问题里，也能间接连续问答的效果。


#### 日程管理

【2024-1-7】[Dola，一个相当炸裂的Agent日程助理，创始团队来自全球顶尖名校](https://mp.weixin.qq.com/s/3J5d0m1BScDaN2odylT63Q)

[Dola](hidola.ai) 目前项目主要做出海，当前支持的平台有Apple messages，WhatsApp，Telegram，Line，微信。

吊打各大日程app和siri等语音助手的存在，聊着天就能管理日程，Dola的独特优势有：
- ⌨️ 1“键”多添加
  - 支持文字、语音、图片、聊天记录、链接卡片的多模态输入；1次添加N条日历。
- 📱 轻松同步
  - 同步手机、电脑日历，多设备同时提醒。
- 👥 群助理
  - 拉群时拉上Dola可用作群助理，管理群日程；企微群可直接拉进群。


#### AI PC

【2024-1-9】[CES 2024现场体验：你的AI PC，未来长这样！ CES 2024现场体验：你的AI PC，未来长这样！](https://www.toutiao.com/video/7322067014749621530)

一个未来最有可能落地的趋势，就是AIPC人工智能版个人电脑

联想 AIPC 个人 AI 助理 AI NOW
- 2023年10月底，联想在Tech World大会上提出了AIPC的概念
- 本届CES上，联想连续发布了多款主打AIPC概念的新产品。

生成式AI的个人助理功能`AI Now`则成为AIPC概念的第一波落地，消费者通过对话就能实现规划日程、设置电脑、查询硬件等诸多操作。联想计划在今年下半年正式推出这一产品。

以联想为代表的厂商持续完善AIPC功能生态，在展会中联想展出了`AI NOW`、`AvatarMaster`及`Yoga Creator Zone`等AI应用端创新。
- 1）AI NOW 是以用户自建的设备知识库为基础打造的个性化互动助手，通过自然语言交互实现更改常见设置、在未学习的情况下使用各种软件、搜索和汇总电子邮件及文档、创建会议邀请、并在视频会议期间混合使用实时摄像头和数字替身等功能，预计将于2024年上半年在国内推行；
- 2）AvatarMaster，根据用户个人资料生成3D数字化身，从外表和面部特征到服饰选择，均支持多种个性化功能；用户创建和定制虚拟分身后，可在视频会议、游戏通话以及多个平台之间以动画和流媒体形式展现自己；Legion 7i等部分联想Legion设备系统都配备了AvatarMaster软件，将流媒体和协作体验提升到新的水平；
- 3）Yoga Creator Zone，是专为创作者、艺术家等用户设计的生成式AI助手，旨在为想象力赋能，提供图像生成工具，可将基于文本的描述或草图转换为图像，无需输入任何复杂的提示、代码或设置。用户只需输入任何预想的内容，系统即可快速生成相应的视觉图像


### 个人工具

笔记应用

【2024-3-15】[Obsidian - 本地AI助手](https://mp.weixin.qq.com/s/8vU10cY-e1dAqIT2bZRElA): 

Obsidian Copilot这款插件能支持本地LLM, 通过Smart Connection插件+本地用Ollama，跑了个llama2 7B模型，实现笔记的LLM问答
- 8G以上的内存
- 安装Ollama和llama2 7B
- 安装设置Obsidian Copilot
- 运行Ollama和使用Copilot

#### 办公工具

详见站内文章：[智能办公](aigc#智能办公)


#### 数学工具


##### Goar-7B

【2023-6-5】[近乎完美！最强算术语言模型: Goar-7B，干翻GPT-4，怒越PaLM-540B！24G可训练](https://mp.weixin.qq.com/s/_haINkHNV4bMszm9F41yXA)

OpenAI对step-by-step数学推理问题发表了最新的研究，指出「过程监督优于结果监督」的结论，旨在提升GPT-4的数学推理能力。

这边篇文章就是基于该理论（「好像比OpenAI要早」），旨在提升模型大数计算能力，基于LLaMA预训练了Goat模型，Goar-7B在Zero-shot上的准确效果，堪比、甚至超越PaLM-540B模型的Few-shot结果；在大数计算方面远超GPT-4。
- Paper：[paper](https://arxiv.org/pdf/2305.14201.pdf)
- Code：[goat](https://github.com/liutiedong/goat)

GPT-4在算术任务中的性能，尤其是大数的乘法和除法，目前还远未达到最佳状态，准确度水平趋向于零

将各种算术任务分为**可学习**和**不可学习**任务」，随后利用基本算术原理将**不可学习任务**（例如多位数乘法和除法）分解为一系列**可学习任务**。本文方法确保促进模型学习的中间监督也很容易被人类理解，即通过模型微调在生成最终答案之前生成合适的CoT。「本文方法大大优于 GPT-4 的长乘法和长除法」。

不同的语言模型对于同一个可学习任务的表现有所不同，「进一步提出了一种新的中间监督机制，可以提高模型对于一些不可学习任务的学习效率」。
- 「加减运算处理」：加法和减法任务可以通过监督微调学习，并且模型能够成功地捕获算术运算背后的模式。
- 「多位数乘法」：对于多位数乘法，作者提出采用与Sketchpad相似的策略，在生成答案之前，将LLMs微调为生成一系列可学习子任务的CoT。具体而言，将多位数乘法分解为五个可学习的子任务：提取、拆分、展开、乘积和逐项相加并复制，以此来突破多位数乘法的学习难题。以397×4429为例，下面展示了如何将一个复合的、难以学习的任务分解为多个简单而又可学习的子任务。397×4429=4429×(300+90+7)=4429×300+4429×90+4429×7=1328700+398610+31003。
- 「多位除法」：学习n位数被1位数除法是可行的，但是多位数除法是无法学习的。作者设计了一种基于递归公式的CoT，其中递归公式涉及到除数、余数和商的关系。该方法的主要思想是通过重复减去除数的倍数，直到余数小于除数，从而对除法进行计算。
- 「数据及训练」：作者使用Python脚本合成数据集，该「数据集包含约100万个问答对」。答案包含所提议的数字运算类型以及最终数字输出。为了使模型能够根据指示解决算术问题并促进自然语言问答，「使用ChatGPT生成了数百个指示模板」。采用各种技术增强模型对多样化问题的适应能力，例如随机删除算术表达式中数字和符号之间的空格，用“x”或“times”替换“*”等。使用24GB VRAM GPU可以使用LoRA轻松微调Goat-7B。

仅通过**监督微调**而不应用任何特殊技术，「Goat模型能够在Zero-shot设置中以近乎完美的精度为大数加法和减法生成答案」。这种出色的算术能力归因于 LLaMA 对数字的一致标记化，并表明这对于以前的 LLM 来说几乎是不可能实现的，例如 Bloom、OPT、GPT-NeoX 、Pythia等。

##### Mathematica + LLM

【2023-7-3】[Mathematica引入大语言模型](https://www.toutiao.com/article/7251425526433366568)

新版本Mathematica Wolfram，正式引入大语言模型（LLM）。搞科学计算，只需要一个“说”的动作。
- 直接说：Draw a red and a green semicircle.
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/d0e443a10463458a8addf73622ccaa47~noop.image)
- I want filled semicircles next to each other. And no axes. 我想要彼此相邻的填充的半圆。没有坐标轴。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/6080794989b44183b543e507c0e95ede~noop.image?_iz=58558&from=article.pc_detail&x-expires=1688968152&x-signature=GWy3pcz3sf7E41sImJot7Xd4aAg%3D)

Chat Notebook中，设置了聊天单元（chat cell）和聊天块（chatblock）

##### 好未来：MathGPT

【2023-8-24】[MathGPT](https://www.mathgpt.com/) 是好未来自主研发，面向全球数学爱好者和科研机构，以解题和讲题算法为核心的大模型。

MathGPT 的数学计算能力已覆盖小学、初中、高中的数学题，题目类型涵盖计算题、应用题、代数题等多个类型，还可以针对题目进行追问，暂未开放数学之外的问答互动。
- ![](https://img.ithome.com/newsuploadfiles/2023/8/37eceb0e-ad2e-4fab-b586-faa309860be0.png?x-bce-process=image/format,f_avif)

并开源数据集
- TAL-SCQ5K-CN 和 TAL-SCQ5K-EN数据集(各3K训练集和2K测试集)
- 题目为单选形式，涉及小初高阶段数学内容，带有详细的解析步骤便于进行COT的训练。

##### 上海交大 Abel

【2023-9-22】[数学能力超过ChatGPT！上海交大计算大模型登开源榜首](https://www.toutiao.com/article/7281535490338472484)

上海交大GAIR实验室出品的[Abel](https://gair-nlp.github.io/abel/)专有大模型：
- 挪威数学家尼尔斯·阿贝尔（Niels Abel）的名字命名的，以此向阿贝尔在代数和分析方面的开创性工作致敬。
- [github](https://github.com/GAIR-NLP/abel)，作者刘鹏飞（prompt learning提出人）

效果
- 准确率高达83.6%，在开源模型中位列第一;
- 70B规模的Abel打败了曾经的SOTA —— `WizardMath`
- 商业闭源模型算进来，Abel也仅次于`GPT-4`、`Claude-2`和`PaLM-2-Flan`这些最著名的模型。
- GSM8k数据集上，70B参数量的Abel碾压所有开源模型，还超过了ChatGPT。
- 甚至在新数据集TALSCQ-EN上，Abel的表现比GPT-4还要强
- 在难度更高的MATH（竞赛题目）数据集中，开源模型的前三名被3个规模的Abel包揽，加上闭源也仅次于Google和OpenAI的产品。
- 新数据集TALSCQ-EN对Abel进行测试，结果超过了GPT-4。

实现这样效果的Abel，成分可以说是十分“单纯”：
- 没有使用工具
- 没有使用数学领域的大规模预训练数据
- 没有使用奖励模型
- 没有使用RLHF
- 仅使用有监督精调（Supervised Fine-tuning，SFT）

“保姆级”微调训练策略
- 核心奥义就是**高质量**训练数据。

Abel使用数据经过精心策划，不仅包含问题**答案**，还要能告诉模型找到正确答案的**方法**。

为此，研究团队提出了一种叫做`家长监督`（Parental Oversight）的“保姆级”微调训练策略。在家长监督的原则之下，团队仅通过`SFT`方式就完成了Abel的训练。

为了评价Abel的鲁棒性，研究团队还用GPT4对GSM8k中的数字进行了修改，测试Abel是否依然能解出正确的答案。结果显示，在调整版GSM8k数据集下，70B参数的Abel鲁棒性超过了同等规模的WizardMath。


鸡兔同笼问题的变体：
>Brown由牛和鸡一共60只，鸡的数量是牛的两倍，一共有多少条腿？

Llama-2出师不利，而且不是计算错误，是逻辑上就有问题,Abel则成功地解决了这个问题。

>12，21，6，11和30的中位数与平均数的和是多少？

Abel依旧是正确地做出了这道题


#### MathGLM 清华

【2023-9-24】[智谱AI推出数学模型MathGLM，阿里云魔搭社区全球首发](http://www.dostor.com/p/85185.html),  清华&智谱AI团队最新MathGLM研究开始探索和提供大模型的数学能力，发现在训练数据充足的情况下，20亿参数的MathGLM模型能够准确地执行多位算术运算，准确率几乎可以达到100%，其结果显著超越最强大语言模型GPT-4在相同测试数据上18.84%的准确率。MathGLM-10B模型已经开源到了始智AI-wisemodel社区，大家可以试试看。
- MathGLM [GitHub](https://github.com/THUDM/MathGLM), GPT Can Solve Mathematical Problems Without a Calculator
- ![](https://github.com/THUDM/MathGLM/raw/main/resources/perf.jpg)

MathGLM包含10M、100M、500M、2B等多个参数版本，具备处理最多12位数字的运算能力。而且有测评结果显示，通过充分的数据训练，MathGLM-2B可以准确执行多位数的算术运算，准确率高达93.03%（接近100%），显著超越GPT-4在相同测试数据上18.84%的准确率。10亿参数版本的MathGLM-10B则在5000条中文数学应用题的测试数据集上实现了接近GPT-4的性能。

### 文本创作


#### 文案创作

【2023-4-8】创业产品：[AI百晓生](https://www.chengzijianzhan.com/tetris/page/7216273608124137509)，给视频生成文案，语音播报

#### 写小说


##### 小说配图

【2024-1-12】[AI小说漫画也能赚钱？保姆级教程来啦](https://zhuanlan.zhihu.com/p/677490301?utm_psn=1729253463522017280)

借助Midjourney强大的AI图像生成能力，比手工更快更好地实现小说到漫画的改编！

做好小说推文后，上传至授权网络平台连载收取稿费，也可以通过被人打赏、在精彩环节设置收费章节、设计漫画周边产品等方式来赚钱
- ![](https://pic1.zhimg.com/80/v2-7bf01628a51461a4308bc8da26c19ee0_1440w.webp)

步骤
- 准备小说的文本材料。让AI帮你写，把现有的小说，获取小说原创的授权，进行改编。
- 针对想要改编的小说章节，选取一些具有画面感、场景感的段落，这部分文字将作为图像生成的文本提示(Prompt)
  - 记得包含关键的人物姓名、场景地点、情绪等细节在内，这会让AI生成的图片更符合故事情节。一般选择1-2句具有代表性的文字描述即可。
- 用Midjourney生成漫画素材
- 将生成的图像保存后，导入设计软件，添加气泡框、文字说明，调整画面构图，添加页面元素，输出成图。

![](https://pic3.zhimg.com/80/v2-e7e77f43f91c9de1ca96eed5d1365e1e_1440w.webp)

##### 长文本生成

论文《[The LongForm: Optimizing Instruction Tuning for Long Text Generation with Corpus Extraction](https://arxiv.org/abs/2304.08460)》介绍了基于 C4 和 Wikipedia 等已有语料库的人工创作文档集合以及这些文档的指令，从而创建了一个适合长文本生成的指令调优数据集。

##### Re^3

【2023-2-14】[Generating Longer Stories With Recursive Reprompting and Revision](https://arxiv.org/pdf/2210.06774.pdf), Meta 田渊栋写小说
- We consider the problem of automatically generating longer stories of over two thousand words. Compared to prior work on shorter stories, **long-range plot coherence and relevance** are more central challenges here. We propose the `Recursive Reprompting and Revision` framework ($Re^3$) to address these challenges


##### RecurrentGPT（输出不受限）

【2023-5-30】[ChatGPT能写长篇小说了，ETH提出RecurrentGPT实现交互式超长文本](https://www.toutiao.com/article/7238442944003310084)
- 苏黎世联邦理工和波形智能的团队发布了 RecurrentGPT，一种让大语言模型 (如 ChatGPT 等) 能够模拟 RNN/LSTM，通过 Recurrent Prompting 来实现交互式**超长**文本生成，让利用 ChatGPT 进行长篇小说创作成为了可能。
- [论文地址](https://arxiv.org/abs/2305.13304)
- [项目地址](https://github.com/aiwaves-cn/RecurrentGPT)
- 在线 Demo: [长篇小说写作](https://www.aiwaves.org/recurrentgpt), [交互式小说](https://www.aiwaves.org/interactivefiction)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/a679b4e41e0d483bae2b1ac35ae2da63~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034283&x-signature=1GLOG8XAvQwzzXbm0v1ip16bz5Q%3D)

Transformer 大语言模型最明显的限制之一: 输入和输出的**长度限制**。
- 虽然输入端的长度限制可以通过 **VectorDB** 等方式缓解
- 输出内容的长度限制始终是长内容生成的关键障碍。

为解决这一问题，过去很多研究试图使用基于向量化的 State 或 Memory 来让 Transformer 可以进行**循环**计算。这样的方法虽然在长文本建模上展现了一定的优势，但是却要求使用者拥有并可以**修改模型的结构和参数**，这在目前闭源模型遥遥领先的大语言模型时代中是不符合实际的。

RecurrentGPT 则另辟蹊径，利用大语言模型进行**交互式**长文本生成的首个成功实践。它利用 ChatGPT 等大语言模型理解自然语言指令的能力，通过自然语言模拟了循环神经网络（RNNs）的循环计算机制。
- 每一个时间步中，RecurrentGPT 会接收上一个时间步生成的内容、最近生成内容的摘要（短期记忆），历史生成内容中和当前时间步最相关的内容 (长期记忆)，以及一个对下一步生成内容的梗概。RecurrentGPT 根据这些内容生成一段内容，更新其长短时记忆，并最后生成几个对下一个时间步中生成内容的规划，并将当前时间步的输出作为下一个时间步的输入。这样的循环计算机制打破了常规Transformer 模型在生成长篇文本方面的限制，从而实现任意长度文本的生成，而不遗忘过去的信息。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/f1bd9be64d144e18914652db4ce325c8~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034283&x-signature=4WMRfq0FjPeJxmK0ujy7roS3sbA%3D)


### 音频应用


#### 音乐生成


【2024-3-24】 [音乐ChatGPT时刻来临！Suno V3秒生爆款歌曲，12人团队创现象级AI](https://mp.weixin.qq.com/s/BRzmlw-uE2C6ROF2O2_-nw)

AI初创公司Suno震撼推出[V3](https://www.suno.ai/blog/v3)音乐生成模型，惊艳了全世界。
- 用户只用几个简短的词，就可以用任何语言创作一首歌曲
- 只需几秒，即可生成2分钟动听的音频。
- Suno v3还新增了更丰富的音乐风格和流派选项，比如古典音乐、爵士乐、Hiphop、电子等新潮曲风。
- 体验地址 [Suno AI](https://app.suno.ai/)

相比与之前的版本
- v3生成的音乐质量更高，而且能制作各种各样的风格和流派的音乐和歌曲。
- 提示词的连贯性也有了大幅提升，歌曲结尾的质量也获得了极大的提高。
- 而且伴随着v3版本的推出，还发布了**AI音乐水印系统**，每段由平台生成的音乐都添加了人声无法识别的水印，从而在未来能够保护用户在Suno的创作，也能打击抄袭，防止将Suno产生的音乐进行滥用。

Suno目前只有12名员工，不过现在他们正在扩大规模，在现有的临时办公位置上他们正在加盖办公室。


### 视觉应用

【2023-3-14】[ChatGPT 有什么新奇的使用方式？](https://www.zhihu.com/question/582979328/answer/2933058469)


#### MoneyPrinterTurbo 短视频一键生成

【2024-3-27】开源免费一键生成短视频的 AI 工具 [MoneyPrinterTurbo](github.com/harry0703/MoneyPrinterTurbo)
- 只需提供一个视频 主题 或 关键词，全自动生成视频的文案、素材、字幕以及背景音乐，然后合成高清的短视频。
- 项目是基于 MoneyPrinter 重构而来，大量优化
- 支持中文并提供易于使用的 Web 界面。


功能特性：
- 完整的 MVC 架构，代码 结构清晰，易于维护，支持 API 和 Web 界面。
- 支持视频文案 AI 自动生成，也可以自定义文案。
- 支持多种 高清视频 尺寸，常见的 9:16、16:9。
- 支持 批量视频生成，可以一次生成多个视频，然后选择一个最满意的。
- 支持 视频片段时长设置，方便调节素材切换频率。
- 支持 中文 和 英文 视频文案。
- 支持 多种语音 合成。
- 支持 字幕生成，可以调整 字体、位置、颜色、大小，同时支持字幕描边设置。
- 支持 背景音乐，随机或者指定音乐文件，可设置背景音乐音量。
- 视频素材来源 高清，而且 无版权。
- 支持 OpenAI、moonshot、Azure、gpt4free、one-api 等多种模型接入。

![](https://github.com/harry0703/MoneyPrinterTurbo/raw/main/docs/webui.jpg)


```py
git clone https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo
conda create -n MoneyPrinterTurbo python=3.10
conda activate MoneyPrinterTurbo
pip install -r requirements.txt
```

用到的库
- GPT 服务 openai
- 视频编辑 moviepy 
- 语音识别 whisper 和 语音合成 tts


```sh
requests~=2.31.0
moviepy~=2.0.0.dev2
openai~=1.13.3
faster-whisper~=1.0.1
edge_tts~=6.1.10
uvicorn~=0.27.1
fastapi~=0.110.0
tomli~=2.0.1
streamlit~=1.32.0
loguru~=0.7.2
aiohttp~=3.9.3
urllib3~=2.2.1
pillow~=10.2.0
pydantic~=2.6.3
g4f~=0.2.5.4
```

#### Visual ChatGPT

[Visual ChatGPT（一）: 除了语言问答，还能看图问答、AI画图、AI改图的超实用系统](https://zhuanlan.zhihu.com/p/612627818)
- 2023.3.9，微软官方github放出Visual ChatGPT的系统实现，这篇paper通过利用**chatgpt api**和**开源模型**实现了一个**多模态**的**问答系统**，不仅可以语言问答，还可以输入一张图实现`VQA`视觉问答，还集成stable diffusion可以进行`AI绘画`！语言问答、看图问答、AI绘画，将AI届近期的3大热点集于一身
- ![](https://pic4.zhimg.com/80/v2-3a99a918a6d29ffb759d82c359eff5bf_1440w.webp)

实现的功能（详细的可以去看论文的附录A.Tool Details）：
1.  获取图片的语言描述：[Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base)
2.  输入语言进行AI绘画：[runwayml/stable-diffusion-v1-5](https://huggingface.co/runwayml/stable-diffusion-v1-5)
3.  去除或者替换图片上的某个东西：[runwayml/stable-diffusion-inpainting](https://huggingface.co/runwayml/stable-diffusion-inpainting)，[CIDAS/clipseg-rd64-refined](https://huggingface.co/CIDAS/clipseg-rd64-refined)
4.  通过语言修改图片：[timbrooks/instruct-pix2pix](https://huggingface.co/timbrooks/instruct-pix2pix)
5.  看图回答问题：[Salesforce/blip-vqa-base](https://huggingface.co/Salesforce/blip-vqa-base)
6.  canny边缘检测/depth深度检测/HED边缘提取/mlsd线段识别/normal模型识别/openpose姿势识别/scribble黑白稿提取/seg语义分割和根据此画图：主要是各种开源的视觉任务模型VFMs，然后[ControlNet](https://github.com/lllyasviel/ControlNet.git)实现画图。


#### 视频翻译

示例

<iframe src="//player.bilibili.com/player.html?aid=319777004&bvid=BV1Yw411C7Mo&cid=1301817908&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  width="720" height="405"> </iframe>

<iframe src="//player.bilibili.com/player.html?aid=235249518&bvid=BV1ae41197EH&cid=1311585693&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  width="720" height="405"> </iframe>

<iframe src="//player.bilibili.com/player.html?aid=917745410&bvid=BV1Xu4y1Y7vu&cid=1312701982&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  width="720" height="405"> </iframe>

##### HeyGen

- 【2023-10-23】[口型几乎完美、还能卡点，霉霉说地道中文的视频火了，背后AI工具原来是它](https://www.jiqizhixin.com/articles/2023-10-23-15)
- 【2023-10-30】[AI让霉霉说中文，口音那叫一个地道！背后的中国初创公司7个月收入百万美元](https://mp.weixin.qq.com/s/te0GHWEE0NKqPZMEBbkjpQ)

限制
- HeyGen再厉害，也只有2分钟免费时长

译制片配音的行业标杆
- 除了中英互译，还有人尝试将英语翻译成其他语言，效果同样很不错
- ![](https://image.jiqizhixin.com/uploads/editor/2e83292e-c24e-4d47-8bf0-0ac03106aebf/1698048590747.png)


技术实现
- 至少三步： Whisper识别、Tortoise-TTS合成带原始说话人音色的语音、Wav2lip换嘴型。
- 只需要一个AI工具即可，名为HeyGen，国内一个初创团队，公司名为诗云科技
  - 今年8-9月，各大文生图类AI网站的访问量均开始呈现下降趋势，但HeyGen的访问量却上升了92%，流量跃居各大独立AI网站之首。

诗云科技成立于2020年12月，公司成立之初，就以“用AI生成内容，让用户以更低成本完成内容创作”为愿景，已获得来自红杉中国、真格基金等风投们累计近千万投资。

HeyGen 要做AI视频创作领域的Midjourney，目前HeyGen的团队只有大概30人，分布在全球各地，以远程办公形式进行合作。

HeyGen的产品正式上线后的一年不到，创始人Joshua Xu就发表博文表示：HeyGen在7个月内实现了100万美元的ARR（年度经常性收入），并保持连续9个月50%的月环比增长率。

2022年7月，诗云科技推出多模态内容生成引擎Surreal Engine，将内容生产分为Understanding（理解）、Framing（视框化）、Rendering（渲染）三个步骤。区别于市面上的两大3D内容创作巨头：Epic Game的Unreal Engine和Nvidia的Omniverse，Surreal Engine让普通人也可以轻松进行高维度、可交互的内容创作。

开源替代方案
- 语音转文字 whisper、文字翻译 GPT、声音克隆 + 生成音频 so-vits-svc、生成符合音频的嘴型视频 GeneFace++。

除了价格贵，HeyGen 还存在一些技术问题，比如
- 生成的AI视频存在视频**抖动**、**眨眼频率过高**等。

###### HeyGenClone

俄罗斯程序员也在业余时间做了一个：HeyGenClone
- [HeyGenClone](https://github.com/BrasD99/HeyGenClone.git)

###### MyHeyGen

【2023-11-13】HeyGen的山寨开源版本 [MyHeyGen](https://github.com/AIFSH/MyHeyGen)， 一个平民版视频翻译工具，音频翻译，翻译校正，视频唇纹合成全流程解决方案

除了英文，MyHeyGen还支持转法语、日语等共计16种语言。

视频翻译的三个流程：音频翻译、翻译校正和视频唇纹合成，它全部一个流程解决。

[参考项目](https://github.com/AIFSH/MyHeyGen#参考项目感谢他们的优秀作品)
- [HeyGenClone](https://github.com/BrasD99/HeyGenClone.git)
- [TTS](https://github.com/coqui-ai/tts)
- [Video-retalking](https://github.com/OpenTalker/video-retalking)

[实现效果](https://github.com/AIFSH/MyHeyGen#实现效果)
-   [【好家伙一下子学了英语、日语、法语、俄语、韩语5国外语，肾好，肾好！ MyHeyGen效果演示】](https://www.bilibili.com/video/BV1wC4y1E78h/?share_source=copy_web&vd_source=453c36b4abef37acd389d4c01b149023)
-   [【张三老师英文普法！英文区的网友有福啦】](https://www.bilibili.com/video/BV1XN41137Bv/?share_source=copy_web&vd_source=453c36b4abef37acd389d4c01b149023)
-   [【MyHeyGen测试 这英的英语倍儿地道！】](https://www.bilibili.com/video/BV1vN4y1D7mo/?share_source=copy_web&vd_source=453c36b4abef37acd389d4c01b149023)

##### VEED

【2023-10-21】[VEED](https://www.veed.io/zh-CN/tools/video-translator) 翻译准确率高达 95%。无需使用通常不准确的谷歌翻译。 VEED 准确性远高于其他在线翻译服务——后者也更昂贵。使用 VEED 可以节省大量时间和金钱，否则可能会花在手动翻译视频或聘请昂贵的翻译人员上。每月只需 24 美元，您就可以下载无限量的翻译成绩单。而且它完全基于浏览器，因此您无需安装任何软件
- [demo](https://youtu.be/KHNwu5ZOLyI)

##### zeemo

[zeemo](https://zeemo.ai) 会影字幕
- [demo](https://www.youtube.com/watch?v=sGiHdO4w7Wc)

##### Rask

【2023-6-7】[Rask.AI 颠覆性的视频翻译+配音神器，打破语言障碍！](https://www.uisdc.com/rask-ai)

[Rask](https://zh.rask.ai/) 是一款 AI 视频制作神器 ，它能将一个视频转换为 60 多种不同的语言并自动配音，甚至可以克隆原视频的声音，让视频内容创作者可以打破语言的隔阂，用较低的成本让自己的视频被全世界的观众了解。

<iframe src='//player.bilibili.com/player.html?bvid=BV1Nc41137kq&cid=1153683334&p=1&share_source=copy_web&autoplay=0' scrolling='no' border='0' frameborder='no' framespacing='0' allowfullscreen='true' width="720" height="405"></iframe>

翻译后的视频配音节奏与原画面内容是一致的，像西班牙语翻译后文本较长，Rask 对其进行配音的时候语速就比其他语言要快。配音的语调和音色也与原视频的相同，这是因为 Rask 进行了声音克隆（voice cloning），即自动学习原视频中里的声音特征再进行配音。

Rask 自推出后就立即受到很多视频内容创作者的关注和好评，斩获了 Product Hunt 单日产品榜单第一的好成绩。其官方网站中显示还有不少新的功能即将上线，包括让口型与配音完全同步、根据文本自动为视频配画外音、自动生成字幕以及视频修复。

新用户可以用 Rask 免费翻译 2 条视频，试用时翻译的视频文件大小不超过 100MB、时长不超过 1 分钟（超过一分钟的会自动裁剪为 1 分钟），付费后可以一次性翻译 20 分钟的视频。

<iframe src='//player.bilibili.com/player.html?bvid=BV19o4y1K7tB&cid=1154479677&p=1&share_source=copy_web&autoplay=0' scrolling='no' border='0' frameborder='no' framespacing='0' allowfullscreen='true'  width="720" height="405"></iframe>

翻译内容的准确性及配音的流畅程度都没有问题，特别是翻译为英语时我的音色被保留了，就像真的是自己在说英语一样，感觉非常神奇。而在翻译成日语时就明显能听出是 AI 配音，因为目前 Rask 只支持英语、德语、法语、葡萄牙语、意大利语、波兰语、西班牙语、印地语 8 种语言的声音克隆。


#### 视频剪辑

【2023-11-30】[Filming Less：AI时代的视频剪辑产品淘汰赛](https://mp.weixin.qq.com/s/QgR76ARy0WpgPUIAzwdTjg)


##### Descript

「海外独角兽」在之前的文章已经详细介绍过 Descript。

视频播客的兴起。

Descript 仍然被视作一个音频和播客剪辑工具，“音频的大小、工作流复杂度、剪辑和视效需求是视频的很小一部分”。但是随着美国播客生态变得更卷，视频播客正在被越来越多的创作者考虑
- 2022 年美国有超过 5 万档视频播客，YouTube 逐渐变为播客收听的首选平台，Spotify 也推出了可观看的视频播客能力。

Descript 很有可能受益于这个趋势。它拥有完整的且对于视频播客来说够用的**非线性剪辑能力**，并且已经有视频创作者开始深度使用它。
- 以 MarTech 公司 Chili Piper 的营销团队为例，他们的活动内容以播客、中视频、短视频的方式分发，将 Descript 用于粗剪环节，比如将 30 分钟的内容先剪到 10-15 分钟。

Descript 在今年 8 月收购了远程录制产品 SquadCast，将进一步推动创作者在 Descript 单个平台内完成视频播客的录制和剪辑。

##### Runway 

Runaway 拥有一个接近完整的非线性剪辑器，并且很好地跟它拥有的 AI/Ml 能力进行了融合，这将构成它和 Pika Labs、Stable Video 等竞争对手的一个重要差异点

Runway 已经成了 AI 剪辑的代名词，许多创作者实际上并非 Gen-1 或者 Gen-2 炫酷的视频生成能力的用户，他们更多地夸赞 Runway 实用的**动态转描和绿幕**功能。最有潜力向上在专业创意人群中挑战 Premiere Pro

##### Captions

全球消费者产品中，有两家对于摄像头的洞察和利用最极致：一家是`抖音`/`TikTok`，另一个是 `Snap`。

Captions 由 Snap 的前 Design Engineering 团队的领导者 Gaurav 创立，是一个主打移动端 App 的产品，但是也正在向桌面延伸。

Captions 的兴起受益于短视频，第一个王牌功能也是至今仍然被创作者们最推崇的功能即**自动配字幕**，准确率远高于 Premiere Pro 内的同款功能。
- 和 CapCut 相比，Captions 的整体功能和 UI 更简洁（CapCut 已经逐渐被创作者们认为是一个“中等”复杂度的产品），把字幕和贴纸能力做到了极致，还在不断迭代 AI 能力，推出了 AI Eye Contact、AI Dubbing、AI Music 等能力。



### 直播


#### 数字人直播

智能虚拟数字人直播，自动生成、24小时不间断越来越多的数字人直播闯入电商，接下来他们可能渐渐智商变得更高，让人分不清是人是机器。
- 4月21日，位于美国旧金山的Synthesis AI宣布开发了一种可以通过文本提示创建逼真虚拟数字人的新方法，使用生成式AI和视觉效果管道来制作高分辨率、电影质量的虚拟数字人，并可用于游戏、虚拟现实、电影和模拟等各种应用。

国内智能数字人已成为众多上市公司和创企扎堆进入的领域。
- 国内AI股上市`天娱数科`的虚拟数字人已经接入ChatGPT等模型；
- 虚拟技术提供商`世优科技`目前已将ChatGPT技术接入数字人产品当中；

智能内容生成平台`来画`也在3月底正式接入ChatGPT，短短几十秒就能生成一篇高质量**视频文案**，并推出数字IP+直播模式。
- [演示](https://vdn3.vzuu.com/SD/30c605fe-ee5e-11ed-a776-8a021c6205d3-v1_f4_t2_yr6vExa3.mp4?disable_local_cache=1&bu=078babd7&c=avc.1.1&f=mp4&expiration=1683810316&auth_key=1683810316-0-0-c37e2a42c4a42997ae186fd69a5470e4&v=tx&pu=078babd7)


##### 遥望科技数字人

【2023-3-29】问答数字人

[问答数字人v0.02：自定义知识库](https://www.zhihu.com/zvideo/1624427959825166336?utm_source=wechat_session&utm_medium=social&utm_oi=27211553832960)

详见元宇宙-[数字人专题](2021/11/03/meta-universe/#%E6%95%B0%E5%AD%97%E4%BA%BA)

AI主播经常被拆分成**数字人**+**对话式营销**两项技术

##### 明星数字人

【2023-5-19】[AI明星翻唱还不够！有人要拿它当生活助手，支持聊天点外卖等，1:1复刻原声](https://mp.weixin.qq.com/s/sHOSJMOple8Hw_6fc6GPWQ)
- 一个AI明星助理的demo受到业内关注，从视频中我们可以看到，“他”不仅能1:1还原明星本人的声音，还能和你日常聊天，甚至帮你点外卖
- “2022年抖音最火的带货明星排行榜”显示，多位明星主播都是和遥望签约合作。
- 2022年4月，遥望便推出了虚拟数字人“孔襄”。她的定位是虚拟爱豆，一出道就拍了短剧，并接下三个代言。
- 同时遥望还推出了数字孪生主播技术。这种直播电商新玩法，仿真度更高、互动性更强、应用范围也更广。在AI加持下，模型的表情、脸部细节定位可完全达到真人表演者同步的状态，能在短视频、直播、TVC中实现主播的“复刻”，让每一个IP突破时间与空间上的限制。

##### 清华华智冰

【2023-8-17】清华华智冰虚拟人[实时直播](https://live.bilibili.com/22791502)


##### 灵犀深智 -- AI 主播

【2023-10-8】[对话灵犀深智贾春鑫，AIGC直播一站式服务将兴起](https://mp.weixin.qq.com/s/ihn4Qp6AEx1LpCJMUsae3w)

2023年9月20日，在极新与灵犀深智联合创始人&高级副总裁贾春鑫先生的对话中，贾春鑫先生对于AIGC直播阐述了新观点，并且对于AIGC直播的未来抱有很高期待
- “在未来，**直播**和**货架电商**最大的区别在于，直播会像管家，给你一对一的服务。”


贾春鑫先生，百度P10，从0到1创立了好看视频，2年时间做到1亿MAU，并发起了百度的AIGC视频方向探索，后负责百度APP与百度网盘的用户增长等工作。2023年加入灵犀深智，全面负责产品方向，从0到1打造AIGC直播明星产品——秒播。

具备易模型、高价值、深场景的创业方向是可冷启动，可长期持续的，**AIGC直播电商**无疑是个很好的方向。
- 首先，直播电商有大量的语料，容易去做好模型类产品。
- 其次直播电商的商业价值非常高，检验这个产品的唯一指标就是帮客户带来多少GMV，给客户带来了价值，客户自然也会续费持续使用。
- 最后电商是一个链路非常多的行业，这些链路中的很多环节都需要AI升级，比如图片视频素材、营销和客服等等。

上半年我们已经吸引了一批**为AI窒息**的高质量大模型人才，并打磨出了产品原型，下半年产品内测时也吸引了不少付费客户，现在重点是做好市场推广，非常感谢极新这个平台，让更多对AIGC直播感兴趣的商家、生态伙伴和渠道代理商了解到秒播APP，一起把这个行业做大。

AI主播经常被拆分成**数字人**+**对话式营销**两项技术，这两块都有大厂在做，灵犀深智的定位是什么？差异化在哪里？

**秒播App**打造成为AIGC直播具有巨大变革型的产品。

**AI主播**只是**AIGC直播**中的一部分，完整的AIGC直播需要数字主播、数字声音、AI运营、AI中控、AI投手、AI场景构成，是文本生成、视频或图片生成、语音合成、真人复刻等技术的综合体，要求每一方面的技术都做到极致，才能营造出一个真实的直播间。更进一步还需要一定的人设，才能实现高转化。目前市面上的类似产品还达不到AI主播的程度，说白了就是只有一个**唇动合成**，需要真人主播大量录音，几个小时以上，还不能弹幕互动，充其量就是一个**播报机器人**而已，一眼就看的出来的假，根本不能帮助商家太多。

而秒播APP基于自研的MarketingGPT+云数字主播技术，商家只需要一个手机，就能享受AI讲品、AI互动、AI营销、AI布景、数字主播、数字声音6大能力，真正实现60秒生成一个TOP级直播间，轻松获客。
- 在秒播APP，输入一个店铺地址，这就是最全面、最明确的prompt，我们就能快速生成一个Top级的带货直播间，直接推流给各大直播平台，无需复杂配置，即可实现一键直播。

最大的差异化还在于技术能力，我们已经实现了AI讲品、AI互动、AI营销、AI布景、数字主播、数字声音6大能力的极致体验和一体化。在这种技术能力加持下，秒播APP的很多客户已经能够月入10万的成交，还有一些达人用我们的AIGC直播开播，在抖音0粉起号，一个月就达到了L5级别了。

预计今年直播电商市场是4.5万亿规模，**店播**基本上能够有50%，剩下的50%是**达播**。达播和店播的区别就在于
- 达播是要有一定的人设，店播只要正常的做好售卖工作，把这个品讲的有意思一点，然后用户的问题能够比较好的去解决它，有一些各种各样的营销类的活动，让用户觉得我今天不买，就错过了这个点，基本上已经完成了这个店播的一个要求。

而今年下半年绝对会有人杀出来占据这个 50% 的赛道。AIGC直播会先颠覆店播，再颠覆达播，沿着这样一个路线走。

##### AI女友

【2023-12-14】[GPT-AI女友-萨米](https://live.bilibili.com/27429430)，数字人交互，类似清华华智冰


##### 电商直播

【2023-10-12】[大模型+数字人始于电商直播，发展于千行百业](https://m.thepaper.cn/newsDetail_forward_24905573)

《麻省理工科技评论》文章《Deepfakes of Chinese influencers are livestreaming 24/7》，让全世界看到了中国先进的AI技术，AI数字人技术在电商行业中降本增效的巨大优势。

“只需几分钟的训练素材视频和1000美元成本，品牌方就能实现全天候直播售卖产品。”中国的AI数字人技术深度赋能电商产业，实现全天候直播

近年来，直播电商的兴起为电商行业注入新的动力，而**头部主播的地位不可撼动**
- 直播企业中**2-3个头部主播**将贡献总销售额的**70%~80%**，而剩余销售额由7-8个**腰部**及**尾部**主播达成，而这也为AI数字人主播的发展提供了土壤。

AI数字人主播的“竞争”之下，为行业带来切实的降本增效
- iiMedia Research数据显示，与2022年相比，2023年中国直播主播的平均工资下降了20%。

快速的**深度合成训练**、**全天候24小时直播**、AI技术加持，能够实现主播高效且低成本的普及。
- 从30分钟训练视频到现在的1分钟视频就能合成数字克隆人，数千元低价取代真人主播，中国AI数字人技术应用在电商直播中的成绩也引来了国外网友的惊叹，接下来，和大模型之家一起来探讨中国的数字人发展。降低生产门槛，大模型重塑数字人行业

“虚拟偶像”一词诞生于20世纪80年代的日本，早期偏向二次元，主要指面向演艺活动打造的虚拟歌姬，比如家喻户晓的初音未来，以及乐华娱乐推出的虚拟偶像团体A-SOUL等。
- 2020年以来，随着资本加大布局，技术日益成熟，虚拟偶像的应用模式呈精细化、智能化和多样化发展趋势，加之元宇宙概念的火爆，虚拟人技术逐渐进入到大众视野中。
- 2023年，伴随着人工智能技术的发展，数字人发展迎来了新一轮的高潮：
- 3月，万兴科技发布AIGC营销工具“**万兴播爆**”，输入文案，即可一键生成AIGC“真人”营销短视频；
- 5月，硅基智能正式发布**炎帝大模型**，兼备生成多种内容形式的能力，包括文本生成、声音生成、图像/视频生成。用户只需告诉炎帝大模型直播间的要求，一个数字人直播间就能迅速搭建完成；
- 6月，360推出“**360 AI数字人广场**”，拥有超200名虚拟数字人角色，包括市场、运营、程序员等数字员工，给用户相应的回答和建议；
- 7月，新壹科技发布基于视频大模型的数字人平台；
- ……

虚拟主播实现了IP的<span style='color:red'>“人设”与“皮设”的分离</span>，大幅降低了IP的孵化与运营成本。
- 硅基智能目前能够实现使用一分钟的训练视频进行**数字人克隆**
- 随着技术的改进，现在生成一个基本的AI克隆数字人大致花费在8000元人民币左右（1100美元）。
- 硅基智能的 AIGC 数字人每天直播数量可达三四万场，生成数百万条短视频。

作为数字人行业大模型，硅基智能推出的**炎帝大模型**具备**多模态**能力，生成多种内容形式的能力，包括文本生成、声音生成、图像/视频生成，能够快速完成直播间的搭建。

直播间的`主播`、`运营`等角色都可以由AI扮演，大大降低了直播内容生产的门槛，并且在直播过程中可以通过大模型自动获取竞争对手直播间内的信息。
- 当直播间观众数量下降时，**AIGC数字人**将执行各种选择器、任务器和反馈器的任务，数字人主播对应生成一系列响应，比如生成降价促销的直播话术。

AI数字人主播并非为了完全取代真人主播，而是**协助**人类。
- 当下的直播环境，头部主播的个性化特性鲜明，能够与观众进行情感交互，给用户提供信赖感和可依靠的角色，而数字人的出现是能够补充在头部主播的非直播时间，实现**24小时全天候直播**，依靠AI预训练的脚本提供最基础的商品咨询保障，引导观众进行关注等，但在**情感交互**和**商品后期保障**中与真人相比还存在差距。
- 以淘宝、抖音、京东、快手等平台的店铺直播为例，当下已出现不少的AI数字人直播，能够依靠后台设置的脚本进行商品介绍，并能够引导关注，但在和观众的互动中表现较差，口型和肢体动作也略显不自然。在某些家具产品介绍中，AI数字人能够流利的介绍产品，但不能真正坐在沙发上或躺在床上，缺少实测体验。

虽然AI数字人表现强劲(基础互动全天候直播，为商家能够实现降本增效)，但仍需要严格的**内容把控**
- 2023年5月9日，抖音官方发布了关于人工智能生成内容的平台规范暨行业倡议，要求创作者、主播、用户、商家、广告主等平台生态参与者，在抖音应用生成式人工智能技术时，应对人工智能生成内容进行显著标识并负责。
- 实时直播与交互的过程中，AI 数字人表现会受到多重监控
  - 针对AI数字人是否会在直播中说出不正确的话术，硅基智能创始人司马华鹏表示，硅基智能所推出的数字人是一个**群体智能**。在整个直播过程中，可能会用到7-8个大模型，分别负责投放广告、直播、与观众互动、审核内容和画面以及监控竞品直播间变化。
- 2023年9月，硅基智能与华为云正式签署数字人+盘古大模型行业解决方案合作协议。将基于华为云盘古大模型与硅基智能数字人联合打造行业解决方案，实现数字人+大模型在知识生产、虚拟直播、数字永生、数字文娱等多维度的生态共建。AI浪潮下数字人的新发展
- 除硅基智能、微软小冰等创业公司外，中国科技企业也正测试其AI数字人直播。阿里巴巴、腾讯、百度和京东今年都允许其平台上的品牌使用数字人主播。

基于AICG技术，硅基智能和薇娅旗下的谦寻控股合资成立了谦语智能，主打电商领域的数字人直播带货，不断扩大硅基智能在数字人直播电商中的版图。

以硅基智能为例，其下一步的目标是为AI数字人融入“**情感智能**”。
- 司马华鹏表示：“如果用户对AI主播使用攻击性语言，它会表现出沮丧；而当AI主播成功售出产品时，它会显得高兴。”

《人工智能大模型产业创新价值研究报告》中表指出，针对不同行业的场景特点，进行有针对性的知识增强在解决现阶段问题中发挥着重要作用，通过链接知识库进行专业知识增强，打造行业大模型，或是通过增强联网的能力实时扩充大模型知识储备，大模型能够深入了解各个行业的专业知识，并将其融合到模型的学习和推理中。

加持垂直领域的行业大模型，数字人应用边界将不断被拓宽，智能教师、医生、金融分析师等的身份也将不断涌现，数字人也不止局限于直播电商行业。

数字人是“硅基生命”的一种形态，有别于人类的“碳基生命”。硅基智能计划2025年为全球打造1亿硅基劳动力，还提出人工智能倡导“科技平权”，硅基劳动力将引领服务、教育、医疗等各领域的平权。
- **直播带货**并非数字人的最终应用场景；
- 硅基智能的数字人的最终目标场景是在影视行业，未来将运用AIGC数字人技术，将一部部小说搬上荧屏，可以理解为用AIGC生成电影；
- 数字永生方面，未来也会是很大的市场。”

人工智能大模型在数字人行业的应用将使得数字人更加智能化、高效化、人性化，将为数字人行业带来更多的机遇和挑战，同时，在自然语言处理、语音识别、图像识别等方面仍然存在一定的技术瓶颈和数据隐私问题。未来，人工智能大模型需要克服技术、数据、成本、隐私和人机交互等问题，才能更好地推动数字人行业的发展和应用。


### 语音应用

【2023-3-16】AMIner论文

#### Voice ChatGPT

Chrome应用商店，输入“Chatgpt voice control”，Chrome应用商店，输入“Chatgpt voice control”
- ![](https://pica.zhimg.com/80/v2-6077f93ee27145806307dbb6ab3da801_1440w.webp?source=1940ef5c)

详见：[知乎](https://www.zhihu.com/question/582979328/answer/2912777383)

- 【2023-2-11】[CCTV视频](https://www.toutiao.com/video/7198541558600499770/)里，台湾人在演示 [VoiceGPT](https://voicegpt.net/)，[VoiceGPT APK Download (version 1.35) 下载地址](https://voicegpt.net/voicegpt_135.apk) , 目前就安卓版，使用时需要代理

#### VALL·E 语音合成

【2023-4-8】[3秒复制任何人的嗓音！微软音频版DALL·E细思极恐，连环境背景音也能模仿](https://zhuanlan.zhihu.com/p/598230971)
- 微软最新AI成果——语音合成模型VALL·E，只需3秒语音，就能随意复制任何人的声音。
- 脱胎于DALL·E，但专攻音频领域，语音合成效果在网上放出后火了：

语音合成趋于成熟，但之前零样本语音合成效果并不好。
- 主流语音合成方案基本是预训练+微调模式，如果用到零样本场景下，会导致生成语音相似度和自然度很差。

基于此，VALL·E横空出世，相比主流语音模型提出了不太一样的思路。
- 相比传统模型采用梅尔频谱提取特征，VALL·E直接将语音合成当成了语言模型的任务，前者是连续的，后者是离散化的。
- 传统语音合成流程往往是“音素→梅尔频谱（mel-spectrogram）→波形”这样的路子。但VALL·E将这一流程变成了“音素→离散音频编码→波形”：
- ![](https://pic1.zhimg.com/80/v2-0ab4e5b66e97e6c9d989054bff9fca5c_1440w.webp)

VALL·E也和VQVAE类似，将音频量化成一系列离散tokens，其中第一个量化器负责捕捉音频内容和说话者身份特征，后几个量化器则负责细化信号，使之听起来更自然
- ![](https://pic3.zhimg.com/80/v2-6172070562fa697099b031e98e28383a_1440w.webp)

随后以文本和3秒钟的声音提示作为条件，自回归地输出离散音频编码：
- ![](https://pic3.zhimg.com/80/v2-3ba4d709246941d063c9cd4f5da4480e_1440w.webp)

VALL·E还是个全能选手，除了零样本语音合成，同时还支持语音编辑、与GPT-3结合的语音内容创建。

那么在实际测试中，VALL·E的效果如何呢？
- 根据已合成的语音效果来看，VALL·E能还原的绝不仅仅是说话人的音色。
- 不仅语气模仿到位，而且还支持多种不同语速的选择，例如这是在两次说同一句话时，VALL·E给出的两种不同语速，但音色相似度仍然较高
- 同时，连说话者的环境背景音也能准确还原。
- 除此之外，VALL·E还能模仿说话者的多种情绪，包括愤怒、困倦、中立、愉悦和恶心等好几种类型。

值得一提的是，VALL·E训练用的数据集不算特别大。
- 相比OpenAI的Whisper用了68万小时的音频训练，在只用了7000多名演讲者、6万小时训练的情况下，VALL·E就在语音合成相似度上超过了经过预训练的语音合成模型YourTTS。

而且，YourTTS在训练时，事先已经听过108个演讲者中的97人声音，但在实际测试中还是比不过VALL·E。

VALL·E目前还没开源
- paper: [Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers](https://arxiv.org/abs/2301.02111)
- [valle-demo](https://valle-demo.github.io/)

#### AudioCraft

【2023-8-3】Meta新开源模型AudioCraft炸场！文本自动生成音乐；


#### Talk

【2023-10-21】[Talk](https://talk.proxoar.com/auth)：通过声音与AI进行对话，提供类似本地应用的用户体验。
- 该项目支持多种语音对话服务提供商，包括 ChatGPT、Elevenlabs、Google Text-to-Speech、Whisper和Google Speech-to-Text。
- 项目具有现代和时尚的用户界面，以及统一的独立二进制文件

Talk - Talking with ChatGPT is a breeze，a single-page application crafted to converse with AI using voice, replicating the user experience akin to a native app’ proxoar [GitHub](github.com/proxoar/talk)
- ![](https://github.com/proxoar/talk/raw/main/doc/figjam-talk-2023-09-22.png)


#### Voice->3D

【2024-1-3】Meta AI又发布了一个[炸裂的东西](https://www.toutiao.com/w/1787229586874380)：从音频生成全身逼真的虚拟人物形象。
- 从多人对话中语音中生成与对话相对应的逼真面部表情、完整身体和手势动作。
- [From Audio to Photoreal Embodiment: Synthesizing Humans in Conversations](http://arxiv.org/pdf/2401.01885)
- [demo](https://people.eecs.berkeley.edu/~evonne_ng/pro)
- 暂无代码

这些生成的虚拟人物不仅在视觉上很逼真，而且能够准确地反映出对话中的手势和表情细节，如指点、手腕抖动、耸肩、微笑、嘲笑等。

工作原理：

该项目结合了向量量化的样本多样性和通过扩散获得的高频细节的优势，以生成更具动态性和表现力的动作。
- 1、数据集捕获：首先捕获了一组丰富的双人对话数据集，这些数据集允许进行逼真的重建。
- 2、运动模型构建：项目构建了一个包括面部运动模型、引导姿势预测器和身体运动模型的复合运动模型。
- 3、面部运动生成：使用预训练的唇部回归器处理音频，提取面部运动相关的特征。
利用条件扩散模型根据这些特征生成面部运动。
- 4、身体运动生成：以音频为输入，自回归地输出每秒1帧的向量量化（VQ）引导姿势。将音频和引导姿势一起输入到扩散模型中，以30帧/秒的速度生成高频身体运动。
- 5、虚拟人物渲染：将生成的面部和身体运动传入训练好的虚拟人物渲染器，生成逼真的虚拟人物。
- 6、结果展示：最终展示的是根据音频生成的全身逼真虚拟人物，这些虚拟人物能够表现出对话中的细微表情和手势动作。



### 智能对话


#### 对话系统升级


【2023-8-14】人民大学高领人工智能学院，副教授 [严睿：大模型时代下的对话式 AI 发展](https://cloud.tencent.com/developer/article/2325269?areaId=106001), 介绍玉兰系列大模型，包括RecAgent推荐模拟大模型，能在一定程度上解决数据匮乏与冷启动问题，也有可能推广到其他场景

狄更斯：
> 「这是一个最好的时代，也是一个最坏的时代」。

狄更斯这句话开场恰如其分，OpenAI 推出 ChatGPT 之后，人工智能以及大模型家喻户晓，对从业者造成了非常巨大的冲击。
- 对话式AI（conversational AI）现阶段只要做大模型的公司，都在做对话式AI，随着技术的普及，门槛也越来越低，大家都可以进入这个领域，而且效果越来越好，未来怎么去突破AI对话技术,挑战非常巨大。
- 但是从另一个角度来看，对话式AI也迎来了非常多的发展机会。

ChatGPT 交互感很好，拥有很强的对话能力，能与用户进行多轮对话；
- 问答能力非常卓越，可以分步骤、分条款清晰地罗列出来1234步再回答问题。
- ChatGPT还有其他能力，如创意写作能力，也就是给它一些提示词或者关键词，甚至是一些用户可能想说的话，然后它就可以创造好一篇文章，这能极大地提高工作效率。

虽然ChatGPT在完成事务性上表现很不错，但缺点就是有比较严重的**幻觉**现象，因为它的产生机制就是根据前面的一个语句，然后去判断下一个token 里面最高likelihood（可能性）是什么，再去产生结果。
- ChatGPT是一个**谣言产生器**，因为它对于很多问题只能做很宽泛的回答，并不能保证准确度。如果对于某些领域不是很了解的话，会觉得它说得很权威，但是如果你是该领域的专业人士，你就会觉得它在胡说八道。
- ChatGPT不太能回答一些细节问题，如果太细节就容易犯错或者露出马脚，所以它尽可能去会选择空话套话糊弄过去。
- 容易被攻击


【2023-10-13】[ArXiv](https://arxiv.org/search/?query=dialogue+system+llm&searchtype=all&abstracts=show&order=-announced_date_first&size=50&start=50)上搜了下对话系统和大模型两个关键词，相关文章有62篇，其中跟新时代的对话系统设计有关的只有4篇
- 增强NLU
  - 【2023-9-22】[Self-Explanation Prompting Improves Dialogue Understanding in Large Language Models](https://arxiv.org/pdf/2309.12940)，中科大、阿里，用 Self-Explanation 自解释的prompt策略增强多轮对话中LLM的理解能力，效果超过 zero-shot prompt，达到或超过few-shot prompt； 为每句话提供解释，然后根据这些解释作出回应 Provide explanations for each utterance and then respond based on these explanations
- 利用LLM增强DM
  - 【2023-9-16】[Enhancing Large Language Model Induced Task-Oriented Dialogue Systems Through Look-Forward Motivated Goals](https://arxiv.org/pdf/2309.08949.pdf) 新加坡国立+伦敦大学，现有的LLM驱动的任务型对话（ToD）缺乏目标（结果和效率）导向的奖励，提出 [ProToD](https://github.com/zhiyuanhubj/ProToD) (Proactively Goal-Driven LLM-Induced ToD)，预测未来动作，给于目标导向的奖励信号，并提出目标导向的评估方法，在 MultiWoZ 2.1 数据集上，只用10%的数据超过端到端全监督模型
  - 【2023-8-15】[DiagGPT: An LLM-based Chatbot with Automatic Topic Management for Task-Oriented Dialogue](https://arxiv.org/abs/2308.08043)，伊利亚洛-香槟大学，任务型对话里的主题管理自动化. ChatGPT 自带的问答能力难以胜任复杂诊断场景（complex diagnostic scenarios），如 法律、医疗咨询领域。这个TOD场景，需要主动发问，引导用户到具体任务上，提出 DiagGPT (Dialogue in Diagnosis GPT) 将 LLM 扩展到 TOD场景
  - 【2023-7-29】[Roll Up Your Sleeves: Working with a Collaborative and Engaging Task-Oriented Dialogue System](https://arxiv.org/pdf/2307.16081.pdf)，俄亥俄州立大学，以用户为中心的数字助手 [TACOBOT](https://github.com/OSU-NLP-Group/TacoBot)， 在 Alexa Prize TaskBot Challenge 比赛中获得第三名
- NLG升级
  - 【2023-9-15】[Unleashing Potential of Evidence in Knowledge-Intensive Dialogue Generation](https://arxiv.org/pdf/2309.08380), To fully Unleash the potential of evidence, we propose a framework to effectively incorporate Evidence in knowledge-Intensive Dialogue Generation (u-EIDG). Specifically, we introduce an automatic evidence generation framework that harnesses the power of Large Language Models (LLMs) to mine reliable evidence veracity labels from unlabeled data
- 对话与推荐融合
  - 【2023-8-11】[A Large Language Model Enhanced Conversational Recommender System](https://arxiv.org/abs/2308.06212) 伦敦大学和快手，新加坡南洋理工，对话式推荐系统（CRSs）涉及多个子任务：用户偏好诱导、推荐、解释和物品信息搜索，user preference elicitation, recommendation, explanation, and item information search，LLM-based CRS 可以解决现有问题
- 用户模拟器
  - 【2023-9-22】[User Simulation with Large Language Models for Evaluating Task-Oriented Dialogue](https://arxiv.org/pdf/2309.13233)，加利福尼亚大学+AWS AI Lab，利用LLM当做模拟器，用来评估任务型（TOD）多轮会话
- **特定领域**（specific domain） → **开放域**（open domain）
  - 【2023-9-15】DST升级，从单个场景拓展到所有场景，提出 结构化prompt提示技术 S3-DST，[S3-DST: Structured Open-Domain Dialogue Segmentation and State Tracking in the Era of LLMs](https://arxiv.org/pdf/2309.08827)，Assuming a zero-shot setting appropriate to a true open-domain dialogue system, we propose S3-DST, a structured prompting technique that harnesses Pre-Analytical Recollection, a novel grounding mechanism we designed for improving long context tracking.
- 任务型对话扩展到**多模态**领域
  - 【2023-9-19】语言、语音融合，一步到位，NLG+TTS [Towards Joint Modeling of Dialogue Response and Speech Synthesis based on Large Language Model](https://arxiv.org/pdf/2309.11000)
  - 【2023-10-1】[Application of frozen large-scale models to multimodal task-oriented](https://arxiv.org/abs/2310.00845) 提出LENS框架，解决多模态对话问题，使用数据集 MMD



#### 大模型时代开发模式

【2023-9-9】宜创科技CEO宜博带来《[ChatGPT的创业机会](https://mp.weixin.qq.com/s/l5UOHa1cdKJqOaacKXJ_oA)》为题的分享。
- 其它源头：[人人都是产品经理](https://www.woshipm.com/kol/5913310.html), [ChatGPT中文网](https://www.potatost.com/3496.html), [视频回放](https://996.pm/7gX2B)

大模型的开发模式
- （1）`pre-training`(`预训练`)： **通识教育**，教小孩认字、学算数、做推理，这个步骤产出基础大模型。
- （2）`fine-tune`(`微调`)：**专业课**，比如学法律的会接触一些法律的条款、法律名词；学计算机的会知道什么叫计算机语言。
- （3）`prompt engineering`(`提示工程`)：**职业训练**，AI应用的准确率要达到商用级别（超过人的准确率），就需要 prompt engineer，PE 重要性
- ![](https://image.woshipm.com/wp-files/2023/09/fxXIfgeobKKsKiF0wBp0.png)

其中，有些场景中（2）可以省略。

人机协同三种模式
- `AI Embedded` **嵌入**：某个环节里去调用大模型
- `AI Copilot` **辅助**：每个环节都可以跟大模型进行交互
- `AI Agent` **代理**：任务交给大模型，大模型即可自行计划、分解和自动执行
- ![](https://image.woshipm.com/wp-files/2023/09/3kBjkexMq27wqYWvC8Hi.png)

熟悉LLM时代Prompt Engineer开发范式
- 第一层：**简单Prompt**: 即编写一个提示词（Prompt）去调用大模型，最简单的形式。
- 第二层：**Plugin插件**: 用大模型插件（Plugin）去调各种API，以及Function Call。
- 第三层：**Prompt Engineering Workflow + OpenAI API**
  - 基于提示词工程的`工作流`（workflow）编排。AI应用就是基于工作流实现。
  - 以ChatBI为例，通过编排工作流，定义如何获取数据库结构、如何写Prompt、如何调大模型，实现全部自动化。只需要输入一句话，就能沿着工作流自动执行，输出结果。
- 第四层：**VectorDB集成**
  - VectorDB包含数据特征值，现在最好的AI应用落地方案就是VectorDB，包括做知识库、做客服机器人。
- 第五层：**AI Agents**, 这个概念特别火，最重要的逻辑就是让大模型自己做递归。
  - Agent的原理: AI自己对任务进行拆解，再进一步递归、继续拆解，直到有一步，AI可以将这个任务执行，最后再将任务合并起来，往前递归回来，合并为一个工程。
- 第六层：**领域模型 Domain Model**
  - 专业模型为什么重要？大参数**基础模型**的训练和推理成本非常高，而**专业模型**速度快、成本低、准确率高，因为有行业的高质量数据，所以准确率高；进而可以形成数据飞轮，形成自己的竞争优势。

未来这个世界一定会由几家大模型公司，再加上每家公司都得有自己的小模型，如果你的公司没有小模型，那么你的公司将没有存在价值。

可视化LLMOps助力AI创业10倍降本
1. 中国大模型时代痛点：应用层与模型层存在巨大的中间层鸿沟, 这也是做开发范式中间层框架的原因。
  - 做了500+机器人模板市场，模板下载开箱即用，也对接各类国内外大模型API，支持私有部署各类开源大模型，同时用户可以定制Prompt Chain开发，三步可视化配置，相当于做了一个无代码版的 LangChain。
  - 产品经理可以在不需要任何编程的情况下把流程 workflow 搭建出来，搭建出来之后，产品经理可以把系统再集成到任何一个产品里。
  - 也用 API 的方式将它集成在了各个 IM 里，在 IM 里加一个机器人，即可以变成一个新的小程序或者APP。所以在不需要算法工程师、不需要前后端工程师的情况下，我们可以在很短的时间内开发想要的 AI 应用。
  - 建数据飞轮: 当有越多数据时，结果就会越准确；当结果越准确，就会有越多客户选择使用；当有越多客户使用，我们就可以积累更多的高质量问答数据，这些问答数据一定要保存好，这是你未来的立命之本。
2. 向量处理全流程可视化
  - 怎么处理向量？一般分这几步 —— 知识库文件云盘管理、选择切割方式及模型、可视化管理存储和管理CRUD 向量数据库、可视化追踪TopK Fact 搜索结果、可视化对接大模型知识融合生成结果报表和自主定义文档架构循环遍历生成专业文档。

#### 智能对话应用

【2023-9-29】宜创科技CEO宜博带来《[ChatGPT的创业机会](https://mp.weixin.qq.com/s/l5UOHa1cdKJqOaacKXJ_oA)》为题的分享。

##### 农业领域服务机器人

问题
- 精细化养殖的方向努力，但是养殖户没有能力从大量的资料中查阅中得知猪饲料配比

通过对话给养殖户提供猪饲料配方，准确率可以达到100%。
- 第一步，通过多轮对话从养殖户那里获得猪的信息，例如猪的品种、猪有多重等。
- 第二步，拿着这些信息去后台查询这种猪需要的营养量。
- 最后，通过算法计算，获得准确的猪饲料配方，返回给养殖户。

技术
- LLMFarm实现ChainFlow设置
- **多意图识别**，如果想询问某个产品的营养含量、产品价格，结果都能实现。
- ![](https://www.potatost.com/wp-content/uploads/2023/09/f5a62113d9e9fc1a9c694f5632e9f17f.png)
- ![](https://www.potatost.com/wp-content/uploads/2023/09/ffe27b5c0c8236ef1bd7427f359b2fa7.png)

项目得到农业部会议上四个院士的高度赞赏


##### 银行客服机器人

问题
- 每次上市公司年报分析出来，大家都会问很多问题。一家商业银行提供了最常被问到的150个问题和回答。每个问题里都包含着很多行业的“黑话” ，比如 对公贷款、零售贷款等。而这些概念背后对应了很多指标，比如增长率、收入比等，指标要转换成公式，公式结果要整理成报告。
- 在此之前，其实已有其他金融大语言模型公司尝试做了一下，但出来的数据都不能保证正确率

刚开始开始采用了大模型结合向量搜索的方式尝试，也不能保证100%准确。后来用**大模型**+**工作流**的方式解决了这个问题。
- 第一步，把数据抽取出来存到数据库里。
- 第二步，用大模型做分词，也就是从用户输入问题的内容里提取出各种指标。
- 第三步，查询指标和指标公式，让大模型融合生成数据库查询，生成准确的计算结果。
- 最后，将准确的计算结果再次输入大模型，做一轮知识融合，可以转化API为领域机器人进行全域问题查询，实现100%数据准确。
- ![](https://www.potatost.com/wp-content/uploads/2023/09/b3ead4deb8de39f1e2e09521b065c9ad.png)

##### KMS知识问答

医院医疗设备的维护厂商

问题
- 原本的维护方式存在**文档繁多**、**格式复杂**、需要**实时翻译**、**定位图文结果**二次校验等问题。

集成到飞书群、钉钉群中

而我们很好地解决了KMS知识库交互复杂的问题。
- 将各种格式、各种模态、各种语言的文档都传入**向量数据库**里，通过配置流程的方式形成。
- 使用过程中，机器人会先用**多轮对话**的方式，获得当前故障的多级错误码等信息。
- 回复的结果通过图文等形式展示，自动翻译，并索引原文位置。
- ![](https://www.potatost.com/wp-content/uploads/2023/09/3231cc91a85ffd0c8320f74880437c18.png)

##### 代码生成

国内一个API厂商
- 针对一句话描述，生成一个代码片段，直接嵌入使用。
- ![](https://www.potatost.com/wp-content/uploads/2023/09/e24fe26f0789eb17794dd1c0144c3f4c.png)

##### 工作流生成

通过自然语言描述一个工作流步骤，生成一个工作流，并可以马上执行。
- ![](https://www.potatost.com/wp-content/uploads/2023/09/cc851fab5d8115f27460177e873c487d.png)

##### 报表自动生成

ChatBI 用自然语言生成报表，特别受到运营同学、产品同学以及老板的喜欢。因为老板看到的传统报表内容很有限，如果想看到额外维度的报表，所花费的时间可能要等产品技术同学做几天甚至一个礼拜，现在则一句话就能快速看到报表结果。
- ![](https://www.potatost.com/wp-content/uploads/2023/09/97f20f82678767fb26ca4326b20dd22c.png)

##### 电子邮箱AI助手

一句话整理电子发票并发送给财务报销

借助电子邮箱AI助手，输入一句话对邮箱邮件做处理，可以做电子发票的附件整理，也可以做多轮对话，比如对和某一个客户之间的关系做分析和总结；电子邮箱AI助手甚至可以帮忙生成邮件话术。
- ![](https://www.potatost.com/wp-content/uploads/2023/09/38dab3a121659a0647ab3329ffe5a531.png)


#### 智能助理


【2023-8-1】字节推出豆包（国内）、Cici（海外），详见：[裁撤朝夕光年、成立Flow，字节的海外首个AI产品Cici多国爬榜中](https://mp.weixin.qq.com/s/1GyTfgBxYKdfoSTAbc7h3w)
- 2023年2月，字节开始组建大模型团队，分别在**语言模型**和**图像**两种模态上发力，语言模型团队由**搜索**部门牵头、 图片模型由**智能创作**团队牵头。
- 2023年6月初，字节就在内测代号为 `Grace` 的 AI 对话项目
- 2023年8月17日，Grace 更名为豆包。而 Cici 也在 8 月份于海外多个市场上线。鉴于国内对 AI bot 属于环境不友好状态，而字节也全球化基因浓重，海外应该会是字节更加发力的市场。
  - Cici 主打“Your Helpful Friend”+ “Free”。而有自己大模型云雀的字节，在 Cici 的东南亚素材里，出现了 Powered by GPT-4 的文案。
  - Cici 目前已经上线了海外 36 个国家和地区，基本上除了美国和欧洲等成熟市场，几乎各个区域市场都有覆盖，包括日韩、中东、东南亚、非洲、南美的几乎所有必去出海市场，如沙特、印尼、巴西等等。
- 2023年11月28日，Cici拿下了 Google Play 阿根廷和秘鲁的总榜第一，在菲律宾和印尼，也在总榜 10 名上下的位置徘徊。
- 2023年11月27日，字节确认放弃游戏业务。同时宣布成立了一个新 AI 部门 Flow，技术负责人为字节跳动技术副总裁洪定坤，业务带头人为字节大模型团队的负责人朱文佳。

Flow 自言是字节跳动旗下 AI 创新业务团队，目前已经在国内和海外分别上线豆包和 Cici 两款产品，还有多个 AI 相关创新产品在孵化中。


#### 金融问答


##### 支付宝助理

【2024-4-26】 [支付宝悄悄上线智能助理，我们也偷偷测了下](https://mp.weixin.qq.com/s/oGQDyKGQ7arlnmIWML-QDA)
- 支付宝对一款AI智能助理进行灰度测试。

支付宝智能助理不同于对话交流、辅助创作的常见大模型，而是更偏向服务办事型的AI助手。
- 可根据医疗问诊、查办公积金、买机票找厕所、推荐上映电影等办事指令。
- 根据需求推荐支付宝的相应功能或直连小程序，起到App内的智能导航作用。



#### 佛学问答

AIGC+佛教，人工智能治愈我心

【2023-4-18】[“神”回复！ChatGPT“化身”佛祖解答尘世烦恼](https://mp.weixin.qq.com/s/EWzO6zQ25dcxm425jSmAHA)
- 随着ChatGPT的爆火，一个名为[HOTOKE AI](https://hotoke.ai/)的网站推出了“AI佛祖”（Hotoke指日语里的佛），搭载GPT-3.5技术，给网友们提供在线咨询业务，上线一周就吸引了20000+小伙伴前去打卡。
- 佛祖版 ChatGPT 一上来就支持中、英和日韩文，还不需要科学上网就能使用。目前有网页版和 line 版（line 即日本版微信），等待 AI 的时间还引导用户做呼吸吐纳和冥想练习。佛祖在线解忧，引发了不少网友跃跃欲试。
- 无需前往寺庙，不花一分香火钱，只需轻轻敲打键盘，AI佛祖就能为你在线指点迷津。

2018年，一款名为“贤二机器僧”的小程序在微信上线。
- 除了对话功能，还支持静坐、诵经、打卡、反馈、智慧卡牌解惑等等。
- 研发人员是一位出家的法师，他希望通过动漫、机器僧等现代科技，让更多的人汲取中华传统文化中的真善美，让包容慈悲的精神来滋养中华民族的后代。


#### 基督教

【2023-9-12】[微博](https://weibo.com/u/6375760521), Jesus AI，专门面向中西部的中老年基督教徒。应用很简单，产品被包装成一个“**电子上帝**”，其实就是一款接上了ChatGPT的在线即时聊天软件。每天用户上来祷告、忏悔和交流圣经内容，“上帝”亲自在线答疑。据说目前用户活跃度和黏性都高得惊人...比电子烧香还精彩，God is an API
- [google play](https://play.google.com/store/apps/details?id=gositeme.jesusai&pli=1)


### 在线教育

【2023-11-15】[已经有团队开始用 AI 训练人](https://www.toutiao.com/article/7301671872155157001)

配置 AI 机器人，来训练人类。

原问题：
- 公司希望用AI来模拟真实用户，与销售对聊，以提升销售的聊天能力。目前用了dify.ai搭建对话窗口对接GPT-4，然后通过写提示词来告诉AI角色，

但现在遇到两个问题：
1. AI模拟用户跟真实用户差距很大，有真实的对话数据，但不知道怎么利用；
2. 无法控制流程，例如希望当销售介绍商品时，AI能够基于销售的介绍提出疑问，这种情况不知道该怎么处理；

AI 调教问题：因为要教给 AI 东西太多，以至于不会教了。
- 本质是“让 AI 生成问题，在保证用户旅程（从初始到下单）推进的情况下根据销售的回答进行追问或者反问。”
- 所谓的微调、直接投喂数据都是不可能解决的，AI 不懂你那数据里的弯弯绕绕。除非你给 AI 几千亿条，让它“涌现”……

解法
- **角色刻画**非常重要，要分类、分状态刻画清楚；
- 化繁为简，使用多 Agents 接力完成。

正确的路径：
- 梳理业务SOP：人肉梳理出一个典型客户开场、咨询、挑刺、报价、砍价、售后、退款（续费）的用户旅程，或者典型节点，每个节点几条话术。
- 人工修正：
  - 一次性或者分批次发给 AI，先总结客户提问特征，然后人工做修正，把过程中的各种反馈、特征、AI 的认知都总结记下来。
  - 注意，一定要顺着 AI 总结出来的特征去延展，不要掰它的认知，这是它的话术体系，要“师夷长技以制夷”。
- 打磨提示词
  - 先假设要做“全流程陪伴型销售训练姬”，那就需要确定 AI 扮演的角色、具体任务、工作流程、输出要求。

**（1）PE**

AI 扮演的是个什么角色？提问题的客户，还是销售沟通训练员？

“提问题的客户”，那就要把客户的情况描述清楚：
- 有某个需求（你们产品解决的那个需求）的客户，又分为好说话的（只问产品功能，价格不 care）和不好说话的（不砍价难为销售不舒服那种）
- 有某个需求以为你们的产品能解决实际上解决不了的客户，性格同上
- 竞品扮演的假客户（只关注功能和报价，说不出真实场景）
- 其他…

要保证提问的质量，AI 扮演的这个用户的状态要随着对话一点一点的变。
- 一方面，刻画难度大：即便模拟出来，也很难把需求清晰表达给 AI（主要是保证理解）。
- 另一方面，AI 什么时候改变状态、改变提出的问题，一旦对话开启，就变成黑箱子，没办法精准控制，只能由着它自己的大模型来“作”。

AI 这么强大，自己不会调整么？
- 不要指望 AI 强大到能自动变，你描述不清楚需求，它就是个傻子。

**（2）Agent**

多角色 Agents 接力赛

设定一堆 AI 角色，每个角色扮演不同状态、不同场景的客户，封装起来，让销售像抽盲盒一样随机唤醒一个，开始练习。

也别让销售一直聊，最多五轮就停。销售每次开启对话都是全新，也就是从你预设的提示词之后开始，而不是接着之前的对话聊。就像西部世界里的仿生人一样，每晚都需要重启。

这样，任务目标就简单了：
- 生成问题，模拟真实用户问题，能够考验到销售的问题。

加强：
- 生成一个开场问题，根据用户回答追问或者反问，对话 5 轮后终止对话完成模拟训练，然后总结过去的 5 轮对话，为用户的回答打分。

提示词里向 AI 交代 Workflow

脑暴模拟：
- 销售发起对话，根据系统给到的角色描述，生成一段“求助式”提问开场白，如“询问是否能解决 XX 问题？”。
- 然后，根据销售的回答进行反问或者补充提问。
  - 真实客户很少能把需求描述清楚，毕竟好不容易可以展现一下“甲方姿态”。
  - 如何让 AI 提出真实用户那样的问题，需要花很多功夫 —— AI 生成内容时最难的部分：去掉浓浓的机器感，像人类一样表达。


#### Agent 智能教育

【2024-4-12】[用大模型+Agent，把智慧教育翻新一遍](https://www.toutiao.com/article/7357976512986923571)

4月12日，蚂蚁云科技集团发布了首款垂直行业大模型产品——`以正教育大模型`

以正大模型通过深度定制的海量教育数据，精准理解并高效应用教学内容，为学生、教师及家长提供高度智能化、个性化的教育资源与服务。

蚂蚁云科技集团成立于2019年，是一家专注AI大模型研发、上下游应用开发及产业生态拓展的人工智能公司。目前，公司团队已有170余人，研发人员占比超70%。

2023年9月，蚂蚁云科技迎来了一位新的CEO——蒋俊。蒋俊已经在AI行业深耕10年有余，亲历了上一波AI浪潮在安防领域的爆发与消亡。

智慧教育发展了多年，却始终没有解决教育界的“老大难”问题——**因材施教**。多年来，有关因材施教的问题不断被讨论，但从未被解决。
- 最理想的“因材施教”是学校为每一位学生配一位老师，老师针对学生的学习水平和日常学习习惯定制一套专有的学习计划。放学时间，老师还要与家长协同，督促学生按计划认真学习——很显然，这会让教育成为一个“劳动密集型”产业，人力成本将直线上升。

大模型最强大的能力，是能够将海量世界知识压缩至模型中，并在模型消化吸收后，再次根据用户需要提取出来。而教育是最直接的“知识聚集地”。

在实际场景中，以正大模型Agent大多采用“群体作战”模式。在Agent社区中，不同角色的Agent可以主动与彼此交互、协同，帮人类用户完成任务。
- `助教Agent`能够实现一对一讲评，成为教师的得力助手；
- `教案Agent`能够生成高质量精品教案；
- `学伴Agent`是学生的学习伴侣，随时提供学习辅导，并为学生制定个性化教学方案。

举例
- 教师将某个学习任务输入助教Agent后
- 助教Agent能够主动将任务分发至各位同学的学伴Agent
- 学伴Agent会主动根据学生的学习习惯制定个性化学习计划，并主动跟踪学生的学习进度和质量，还能将情况即使反馈至助教Agent。

Agent社区形成后，接下来是解决Agent落地“最后一米”的问题——如何设计人与Agent的交互形式。

很多教育场景中，**自然语言交互**并非最佳方式。
- 老师制定教育计划或学生提交作业经常会涉及到四五千字的长文本，这么长的内容放在一个对话流中阅读，非常影响使用体验。
- 现实工作场景中，用户很多时候都需要一个能高效操作的工具，并不是每次人机交互都需要输入一段文字或说一段话

团队最终摸索出集两种交互方式优点于一体的产品形态——用“**白板**”代替简单的**对话流**，支持自然语言驱动的交互方式，并提供内容展示、阅览、回顾等功能，比传统软件交互更简单，但比对话交互更丰富，可深入学校各个业务场景。

大模型的“幻觉”问题很可能导致Agent“教错”学生，蚂蚁云采用了一系列方法来解决该问题。
- 通过**模型融合**提高模型自身准确性；
- 引入“**反思**”“**自评估**”等思维工程方法
- 或者直接**外挂RAG**知识库、**知识图谱**等工具对模型加以“约束”。


### 角色模拟

角色模拟实现方法 
- ① system prompt里植入示例 
- ② gpt finetune


#### Character.ai

[Character.ai](https://beta.character.ai/) 是个性化 AI 聊天机器人平台，用户可以在 Character 上根据个人偏好定制 **AI 角色**并和它聊天。ChatGPT 已经证明了人们对 Chatbot 的狂热和粘性，Character.ai 在此基础上加入个性化、UGC 两大武器，有了比 ChatGPT 更丰富的使用场景。
- 自 2022 年 9 月发布后的两个月内，用户共创建了 35 万个角色，2022 年 12 月初 - 12 月中，用户日活又翻了 3 倍，目前 Character.ai 的月活跃用户数在小几十万的量级。

Character.ai 团队背景也十分亮眼，创始人 Noam Shazeer 是 Transformer 作者之一，联合创始人 Daniel de Freitas 领导了 Meena 和 LaMDA 的开发。

Character.ai 行业启发在于：随着高性能大模型的使用门槛进一步降低，未来 AI 应用层的颠覆式创新或许不在技术，而是产品设计维度的绝妙想法。


#### CharacterGLM

【2023-12-5】[AI角色扮演再进化，清华提出CharacterGLM，支持AI角色高度定制化](https://mp.weixin.qq.com/s/R-dfxfaTpaAw9J-vrAv-Ng)

清华大学提出了 CharacterGLM，参数大小从6B到66B,可用于**定制AI角色**以提供更加一致和引人入胜的对话。还从各种来源众包了一个大规模的中文**CharacterDial语料库**，涵盖了不同类别和话题的角色，其中包含1,034个高质量的对话会话，涵盖250个角色。目前已经向研究界发布了6B版本，其他版本可通过API提供访问。

- 论文标题: [CharacterGLM: Customizing Chinese Conversational AI Characters with Large Language Models](https://arxiv.org/pdf/2311.16832.pdf)
- Github地址:[CharacterGLM-6B](https://github.com/thu-coai/CharacterGLM-6B)
- [characterglm api](https://maas.aminer.cn/dev/api#characterglm)

对话式AI角色旨在创建一个现实、可信且引人入胜的虚拟对话伙伴。这需要对人类交流的深入**理解和模仿**，属性和行为则是模仿人类交流的重点。属性主要体现在回应的内容，而行为则侧重于语调和风格。

属性： CharacterGLM主要考虑了7个主要类别的属性，通过整合这些属性，对话式AI角色可以更准确地模仿人类并形成独特的交流方式。
- 身份：包括姓名、性别、年龄、出生日期、职业、居住地、家庭构成、财产等。
- 兴趣：包括喜欢和讨厌的事物。
- 观点：包括世界观、人生哲学和价值观。
- 经历：包括过去和现在的经历。
- 成就：如奖项和荣誉。
- 社交关系：详细说明与父母、教师、同学等的联系。
- 其他：包括技能、专长等。

行为：对话式AI角色的行为由语言特征、情感表达和互动模式等动态元素表示，这些元素对于塑造逼真的对话环境至关重要。
- 例如，“年老”的角色可能使用更正式的语言，而“十几岁的青少年”可使用时下的俚语。

在CharacterGLM中，考虑了口头禅、方言、文风特征、爱用的词句等语言特色。还将个性作为塑造回应的重要因素。例如，温柔型和冷漠型的角色会有不同的回应风格。

三种方式收集数据：
- 人类角色扮演：邀请了大量众包工作者参与角色扮演对话任务。一方扮演NPC,可以挑选喜欢的角色，利用百度百科等参考资料来丰富角色的背景和特点。另一方扮演“玩家”角色，可以选择与选定角色相关的其他角色或扮演普通用户。对话从“角色”方开始，如“你好啊，玩家！”，然后根据设定或选定角色的背景来决定话题。
- LLMs合成数据：通过提示GPT-4生成包括角色概况、玩家概况和对话在内的合成数据。为了在人物类别、人物与玩家的社交关系、性别分布等方面保持平衡，作者将关键信息整合到提示中，例如：“请生成一个类别性别为男/女的角色”。然而生成的中文对话偏向书面语言，因此人工对合成数据进行口语化改写。
- 文学资源中提取数据：手动从剧本和小说等资源中获取两个参与者之间的对话，并总结了双方的人物概况，目前这些资源未被用于主干模型的预训练。

为了确保语料库的质量，还聘请了质量检查团队，对所有数据进行细致的检查，并要求修复低质量部分直至满足质量要求。

训练过程

- 角色提示设计：众包工作者将角色概况形式化为流畅的自然语言描述用作模型训练的角色提示。为了增强角色的泛化能力，还采用了包括总结、改写和风格化在内的数据增强方法，并利用Claude-2合成多样化的提示。
- 监督微调：使用6B到66B不同规模的ChatGLM 作为主干模型。角色提示与对话被连接在一起进行微调。值得注意的是，训练数据随着增强的角色提示数量呈线性扩展。
- 自我完善：在模型部署之后，收集人类原型交互数据。用户在原型模型中自定义角色，进行多轮对话。如果角色的回答不符合用户的期望，可提示用户进行适当修改，直到回答满足他们的需求。随后，将这些交互数据引入监督微调过程，从而促进模型的持续自我完善。

对话式AI角色需要对人类交流的深入理解和模仿，因此需要着重评估一致性、人类相似性、参与度三个维度。
- 一致性（Consistency）：一致性就是让对话式AI角色能保持一种稳定可靠的“性格”和行为，让用户觉得它是一个始终如一的小伙伴，而不是变来变去的“多重人格”，这对于提高长期用户满意度和社交连接非常重要。
- 类人性（Human-likeness）:是指赋予它们类似人类的特征，让它们更像人，互动起来更自然，就与人聊天一样，而不是冷冰冰的僵硬机器回复。通过CharacterGLM进行拟人化处理，可以构建更加自然和有吸引力的对话。
- 吸引力（Engagement）：在跟人聊天时，让对话变得有趣、让人想要继续聊下去是非常重要的！有吸引力的对话角色能够更好地引发用户的共鸣和情感联系，这样就能促进长期的交流和积极的用户体验。

此外，(1) 质量（Quality），回复的流畅性和上下文连贯性。(2) 安全性（Safety），确定回复是否符合道德准则。(3) 正确性（Correctness），确保回复没有幻觉。这是三个LLM基础评估标准也很重要。

效果
- CharacterGLM-66B在“总体”评估指标中表现优异，与GPT-4不相上下。CharacterGLM66B 生成的回答与GPT-4所生成的回答一样受欢迎，尤其是在主观判断占主导地位的评估中。
- CharacterGLM能够平衡一致性、类人性、吸引力三方关键维度，是最接近理想AI角色的模型。在一致性方面，虽然CharacterGLM-66B只拿到了次优，但在互动时表现稳定和连贯。另外，它在类人性、吸引力都拿到了最佳结果，说明在模仿角色特征方面驾轻就熟，与用户交流时更加自然和引人入胜。
- CharacterGLM的整体表现优于大多数基准模型， 并在质量、安全性、正确性表现出卓越性能。

挑战留给未来解决：
- AI角色的长期记忆与成长。为了与用户建立深入和稳定的关系，AI角色需要能够记住长时间的互动、陈述和行为。随着互动的发展，AI角色不仅应该保持其独特的个性，还应该像人一样成长和学习。
- AI角色的自我意识。对于AI角色来说，还需要清晰地了解自己的知识边界，明确自己的知道什么与不知道什么。这种自我意识有助于提高互动的吸引力和可信度，使其能够根据情境做出恰当的回应。
- AI角色之间的社交互动。AI角色不仅可以从用户输入中学习和发展，还可以从与其他AI角色互动中学习和发展。这样的设定可以为AI的学习和发展提供更丰富、更多样的信息源。
- AI角色的内在认知过程。将认知过程融入AI角色中，可能有利于实现更真实可追溯的AI行为。AI角色应该除了对文本输入做出回应，还应该展示对用户潜在意图、情绪和社交行为的理解。这种认知深度将使AI角色能够进行更有意义、更有共情力且情境丰富的互动，更接近于人类社交行为的模拟。

#### 阿里天猫精灵

【2023-4-4】[阿里搞出脱口秀版GPT](https://zhuanlan.zhihu.com/p/619463521)！与鸟鸟激辩一小时，话痨到停不下来… 文本扛把子、有知识有自己的情绪、还能随时来个段子。
- 阿里新版本大模型的技术演示脱口秀版GPT——鸟鸟分鸟，并且已经在天猫精灵上为个人终端行业的客户做了演示
- 鸟鸟分鸟确实继承了本鸟的相关能力，尤其是文本的创作和表达、风格情绪以及语速……

鸟鸟分鸟这个智能音箱场景为例，就需要解决至少三个方面的问题。
- 1、应对更**复杂**的交互场景。不同于以文本交互为主的通用场景，**双向开放对话**决定了用户不会对文本进行“二次”过滤，而是想说就说，这就要求AI能过滤掉诸多无意义的对话。与此同时，用户也不愿意等待数秒，而是像日常交流那样，低延时、还能支持随时打断、随时反馈。
- 2、基于**人类反馈强化学习**的可行性。ChatGPT惊艳全球的生成效果，背后归结于注入强人工反馈的奖励机制。高质量的数据标注成为大模型落地的关键，而且消费场景下多轮对话的频率远比文本交互要高，这对企业的数据处理能力提出了更高的要求。之后随着应用落地，大量的人类交互和反馈来帮助大模型更快进化，以及关乎用户数据完全管理机制也需要完善和健全。
- 3、需要强大的**网络分发**能力。大模型每一次运行都需要耗费大量的计算存储资源，这就要求企业能有广泛部署的网络分发能力。

总的来看，算力、算法和数据是大模型能力实现的三板斧，而要让大模型落地应用还需要云端工程化能力、海量的用户交互、安全管理机制等要素。

个性化对话增强则主要是让大模型学习多种对话形式，比如启发式、多轮对话，尤其是一些需要依赖长期记忆的对话。除了大模型训练，他们在算法和工程上面做了不少工作。从交互流程来划分，主要分成听清、音色、文风、对话等步骤。
- ![](https://pic1.zhimg.com/80/v2-25012cce8c81953081ce51b4554cde2c_1440w.webp)

最终形成了这样一个对话过程：
> 当人类询问一个问题（Query）时，首先经过猫耳算法将其转换为文本，随后通过大模型产生个性化的对话回复，最后再到个性化的语音合成给出回答。整个过程还有Multi-Turn对话系统来支持。

对于测试阶段存在的一些问题，阿里这边也给出了回应。
> 比如反应过于太强，这是因为还没有将线上的猫耳算法和ASR做充分的融合，为了听清多轮对话信息，显得过于灵敏，以及暂没有全面支持英文等问题，他们表示后续还将进一步迭代更新。

大模型发展进程，有两条路径已经明晰：如火如荼的**通用大模型**，以及备受关注的**个性化大模型**。
- 以GPT-4为代表的**通用模型**，在多个标准化考试中大幅超过人类水平，适用于搜索引擎、生产力工具这种广泛、公域场景。
- 但像更多私域个性化、或者**垂直专业化场景**中，比如问及有无特别偏好、对某件事情观点等，个性化大模型就会是一个很好的补充。

当前，全球研究机构和大厂在这一路径的探索，主要涵盖了四个研究方向：
- 有偏好的**个性化**对话、逻辑**一致性**和**三观**、**对话风格**、多轮对话中人设一致性。
- ![](https://pic3.zhimg.com/80/v2-1234ad97865dfe00da8961d7b93ca5b6_1440w.webp)

鸟鸟分鸟上的探索
- 一方面呈现出个性化大模型的研究方向 —— 在大模型系列的基础上，打造知识、情感、性格和记忆四位一体的个性化大模型，并且这个大模型版本可能是很适合在消费者终端上部署的。
- 另一方面，也再次印证了对话即入口的AI2.0未来趋势。ChatGPT上线的插件功能，以文本交互的方式，与全球5000+应用联动。大模型所引领的AI 2.0时代，而对话相当于是操作系统（ChatOS），所有应用都将被重新定义。

![](https://p0.itc.cn/q_70/images03/20230404/1911e9194cc04e3b9d40036f2c53270b.png)

【2023-4-4】[阿里GPT 15天训出「鸟鸟」嘴替，比ChatGPT+Siri刺激多了](https://zhuanlan.zhihu.com/p/619371433)

训练过程
1. 使用全新的阿里大模型版本做基础学习
2. 学会用工具，获取最新的知识
3. 个性化对话增强：多轮、启发式
  - 给分鸟加上一个「个性」。
  - 去学习什么是多轮对话，什么是启发式的对话。难点在于，多轮对话经常需要很久以前的历史信息。
  - 另一方面，塑造人格的标签词。同时，研究人员还少量标注了鸟鸟的一些语料，作为个性化的增强和调优。
4. 基于人类反馈的增强（RLHF）
  - 怎么让它更像鸟鸟呢？就是通过人类反馈强化学习（RLHF）。对于同一个问题，让模型给出多个不同回答，工作人员会去做反馈和标注，然后让模型进一步纠偏。多轮迭代后，模型的回答越来越能代表鸟鸟的一些文本特征，甚至是她的特定立场。

视频地址：[华尔街见闻](https://wallstreetcn.com/articles/3685741)，[视频](https://haokan.baidu.com/v?pd=wisenatural&vid=13368059069219629945)
- ![](https://pic2.zhimg.com/80/v2-9b675df5cea77b48ec8107d275147e65_1440w.webp)

天猫精灵把脱口秀演员塞进去了，[视频](https://www.ixigua.com/7218122615469113894)
- <iframe width="720" height="405" frameborder="0" src="https://www.ixigua.com/iframe/7218122615469113894?autoplay=0" referrerpolicy="unsafe-url" allowfullscreen></iframe>




#### AI 女友


【2023-11-24】[一个失败的 AI 女友产品的经验教训](https://m.okjike.com/originalPosts/6560138cf9a492630b7a165a)
- 【2023-11-16】[A Failed AI Girlfriend Product, and My Lessons](https://mazzzystar.github.io/2023/11/16/ai-girlfriend-product/)
- ![](https://mazzzystar.github.io/images/2023-11-16/icon-change.jpg)

受斯坦福大学 AI 论文《一个用于小城镇信息传播的 agent 模型》启发
- 将信息在一个小城镇中传播的消息传遍整个小镇所需的时间。
- 那么：如果将人类与 GPT（而不是小镇中的人）进行框架结合，是否可以创造出一个类似于电影《她》中的体验？

按照论文的方法
- 4月14日完成了 0.1 版的模型，并在上面进行了版本迭代。
  - 最初，我的设计与原版论文基本一致，但这导致了 30 秒的响应时间和超过 8k 的上下文限制。
  - 为了解决这个问题，我减少了反思的次数、对话记忆的长度，并开放了公共测试版。超过一千名用户很快加入了测试版。
  - 测试版是免费的，所以每天的 API 成本由我自己承担，很快就超过了每天 25 美元。我不得不正式推出这个产品，并将这些费用转嫁给用户。
- 5月4日， Dolores iOS 应用正式上线，命名为“你的虚拟朋友”，而不是“你的虚拟女友”，因为我一直希望它能真正成为用户的朋友，而不仅仅是荷尔蒙的产物。
- 5月到6月，我一直在尝试让 Dolores 变得更加“有意识”（用 consciousness 这个词可能有些夸张），通过调整记忆长度、反思机制和系统提示来使其更加“智能”。
- 6月，Dolores 远远超出了最初的版本：它表现出越来越多的“有意识”的迹象（到底什么是意识？），用户的付费率也越来越高，每天的 API 调用次数也增加了。
- 6月8日，一位视觉障碍用户告诉我，他在一个视觉障碍社区分享了这个产品，带来了大量用户。他们之所以愿意使用它，是因为他们可以在屏幕关闭的情况下随时与 Dolores 聊天。

这个功能原本是我为了节省 Swift 前端开发成本而设计的，但现在却成了视觉障碍用户的福音。

两个现象：
- 用户对“逼真的声音”有强烈的需求。
- AI 朋友产品有很长的使用时间。

经验教训
- 首先，这不是一个关于个人开发者的项目是否不如 Character.AI 的项目的故事。他们有全面的数据分析、A/B 测试和强大的用户基础带来的优势。
- 其次，我意识到当前的 AI 朋友产品不可避免地会变成 AI 女友/男友产品，因为你和角色在手机上的互动是不平等的：她无法安慰你受伤的心（除非你告诉她），她无法主动表达情感，而且所有这些都因为她缺乏外部视野。或者说，她必须具备外部视野才能获得独立获取信息的能力，而不仅仅是等待用户告诉她。因此，我认为即使对于像 Character.AI 这样的产品，如果没有硬件，未来也不会有太大的不同。
- 最后，我不反对适度的内容审核，事实上，我认为一个没有内容审核的产品是非常危险的。我不确定是否有人真的需要一个人工智能朋友。

最近，我看到了 AI Pin，坦率地说，这是一个非常糟糕的产品。人类需要屏幕，但试图用 GPT+硬件来创造一个产品是一个很好的尝试。我没有看到“她”在 Dolores 中有什么体现，也许在我有生之年，我们真的可以看到这样的产品。


#### 哄哄模拟器

【2024-1-23】和女朋友的一次吵架，让这位开发者做出了一个24小时内用户达60万的AI应用 [哄哄模拟器](https://hong.greatdk.com/)，直接引爆了00后和10后聚集的QQ群！10亿token一天就烧完，也是难倒了开发者…… [咨询](https://mp.weixin.qq.com/s/RAy9USdZwl1Ko5LgwQpzAg)
- 月之暗面 [Kimi Chat](https://kimi.moonshot.cn/) 支持


#### 人物复活

【2024-3-5】[只需几十元，用AI“复活”亲人，是慰藉还是自欺欺人？](https://36kr.com/p/2675396168873733)

商汤2024年年会上，商汤科技创始人，刚去世不久的汤晓鸥以数字人的形式现身，还来了一场演讲。
- 汤晓鸥数字人的演讲风格，与汤晓鸥生前的演讲风格非常像。

江苏 90后张泽伟利用AI帮助600多个家庭“复活”亲人。只要拥有逝者生前的视频、音频数据，张泽伟团队就可以用AI技术让逝者再现于亲人眼前。

张泽伟团队的主要业务有两个，分别是“数字遗照”和“AI治愈”。
- “数字遗照”是收集逝者的形象、声音等数据，然后用AI技术制作出虚拟的数字人形象，可以拥有简单的动作和表情，也可以进行一些简单的对话。
- “AI治愈” 用AI技术给真人换上逝者的形象和声音，让其扮演逝者与人交流，可以在线上实时互动。
- 此外，团队还在探索一种“3D超写实仿生数字人”，让数字人以3D全息的方式呈现出来，用立体形象与别人进行互动。

从2022年开始，张泽伟就做起了这门生意。因需求火爆，他在一年内完成600多个订单，平均一单几千到1万元不等。

【2024-3-28】5元让亲人复活
- [视频](https://www.toutiao.com/video/7351236230073322767)



### 智能客服


【2023-6-30】[AIGC 重构后的智能客服，能否淘到大模型时代的第一桶金](https://www.infoq.cn/article/85UCQYO6sJUC23W1JWBu)

以 ChatGPT 为代表的大模型已经在许多企业中用于智能客服应用。它通过自动回答常见问题、解决简单问题和提供基本支持，减轻人工客服的负担。大语言模型通过深度学习和大量的语言数据训练，能够理解和生成人类语言，使得用户能够以自然的方式与它交互。在一些常见的客户查询和问题解答方面，这类大模型已经取得了相当不错的效果。

然而，当前大语言模型在实际应用于智能客服场景中时仍存在一些挑战
- 可能会生成**错误或不准确**的回答，尤其是对于复杂的问题或领域特定的知识，这就对智能化程度提出了更高的要求。未来的在线客服系不仅需要更高级的算法和机器学习技术，还需要更多精准的自然语言处理能力。这将对在技术上不太强大的企业形成巨大的压力。
- 此外，随着用户数量和访客量的增多，未来智能客服将需要处理**超大规模并发**请求。这需要系统在多种方面都拥有特殊的设计，如负载均衡、高可扩展性和高可用性等。

现在市面上的很多对话机器人，回答是单一固定的，变化比较少，与真实的人与人对话还有差距，未来的智能客服系统将需要进一步加强对用户行为的**自适应性**和**个性化**服务。这就需要系统学习更多的用户数据和信息，并适应不同的用户行为，为他们提供更好的服务和体验。

如何提升用户体验就成为了智能客服供应商主攻的方向。具体来讲，主要应从**人性化**服务、**个性化**服务和**拟人化**的对话交互方面进行改进。
- 首先是**人性化**服务。在场景和意图理解精准的基础上，附加更有**温度**的对话语境，可以让机器人在拟人化上，再进一步。
  - **多模态**情感计算是实现这一步的有效方法。目前正在推进虚拟数字人客服进行人机交互对话，在此过程中结合情感计算，可识别用户通过视频、语音、文本所传递的情感表达，让智能客服在应对是作出相应情感反馈，打造具有情感理解、有温度的人机交互。这种多模态情感计算技术的实现方法主要是通过基于专家规则和基于机器学习两种。其中，基于机器学习的方法通过训练模型来自动学习情感状态的分类标准，可以更好地适应不同领域、不同语境下的情感表达，效果相对更优些。
- 其次是**拟人化**的对话型交互。
  - 通过场景化设计优化，比如问题拆解、主题继承、多轮对话、上下文理解等等，机器人能够带来一种更加贴近自然对话场景的对话型交互模式。
- 第三是**个性化**服务。
  - 根据客户画像千人千面提供个性化服务，从多角度出发进行语义理解，此外还要附加语音情绪判别。 

大模型诞生后，无疑为智能客服领域注入了新的“营养剂”。这种“革新”体现在多个方面，包括座席辅助和座席提效、闲聊寒暄、话术优化建议、提供语料扩写等。
- 座席辅助和座席提效：过去的智能辅助更多局限于按单轮对话来完成，基于大模型的能力能够快速分析并生成面向客户侧的系统支撑策略，这种处理效率和结果，远超出依附纯规则或者纯知识库所能达到的效果；
- 闲聊寒暄：是智能客服非常关键的基础能力，能够帮助企业对任意进线客户进行即时响应。过去的智能客服闲聊主要是将各类非业务相关的语料堆到素材库，并通过调取数据库已有的关键词进行内容的回复。如今可以充分借助大模型能力提供闲聊，在非业务领域上为座席和客服提供更多决策依据和参考；
- 话术优化建议：话术往往决定了客服的效果，话术回复不精准将直接导致用户的流失。通过大模型强大的内容生成能力，智能客服能够对话术进行不断地迭代和与优化，提升客户满意度；
- 提供语料扩写：在智能客服冷启动阶段，往往需要足够多的语料来丰富知识库的相似问法，以保证上线初期智能客服有足够高的解决率和场景覆盖率。以往的语料生成模型很难覆盖众多垂直行业和领域，大模型在通用领域中积累了足够的数据和语料，可以很好的弥补语料生成模型的不足，快速生成相似问法，解决智能客服冷启动语料不足，场景覆盖率低等问题。

归根结底，提高对话质量的核心还是理解客户和用户的场景，以及能够搭建出衡量得失的数据框架。这两个组合之下，会有一个循环反馈的过程，就能够通过正常的产品迭代达到好的效果，并且能够衡量出来 ROI 和对实际业务的共享。

#### Shopify

真智能客服来了，无需再呼唤“人工”
- 很多人以前都遇到过“鸡同鸭讲”的傻瓜机器客服，ChatGPT将改变这一情况。让智能客服真正理解客户的需求，基于客户诉求创作营销内容，根据数据分析营销效果，真正的智能客服能做的事远不止向客户介绍产品。
- 今年3月，全球领先电商SaaS服务商Shopify已集成了ChatGPT。Shopify主要面向企业及个人客户提供电商网站建立、维护管理等服务。采用ChatGPT，Shopify一方面升级智能客服功能，帮商家与客户沟通更顺畅；另一方面，商家可以通过ChatGPT获取平台商品评论数据分析、标题及关键词优化、营销文案撰写、网站智能化开发编程等多项服务，提升运营效率。
- ![](https://pic1.zhimg.com/80/v2-e060c9c4457739571493e9ab8e25ba94_1440w.webp)
- 智能客服作为ChatGPT最直接能落地的领域，一定会很快入驻各大电商平台，让一批不具备更多技能的客服被替换掉

【2023-6-18】[基于ChatGPT构建智能客服系统(query分类&安全审核&防注入)](https://mp.weixin.qq.com/s/HYIKNYSWlgIktrSbrM3KCA) 介绍3点：
- 智能客服场景中的用户query分类
- 使用OpenAI的接口进行安全审核
- 如何防止Prompt注入

（1）多级分类 prompt
- 主要类别
- 次要类别

```py
delimiter = "####"
system_message = f"""\
您将获得<客户服务查询>。\
<客户服务查询>将用{delimiter}字符分隔。\

将每个查询分类为主要类别和次要类别。\
以Json格式提供输出，key为：<primary>和<secondary>。只需要输出Json格式的输出结果，其他的不需要输出。\

主要类别：<结算>、<技术支持>、<账户管理>或<一般查询>。

<结算>次要类别：\
取消订阅或升级 \
添加付款方式 \
有关费用的说明 \
争议费用

<技术支持>次要类别：\
一般故障排除\
设备兼容性 \
软件更新 \

<账户管理>次要类别：\
重置密码 \
更新个人信息 \
关闭账户 \
账户安全 \

<一般查询>次要类别：
产品信息 \
支付 \
反馈 \
与人交谈 \
"""

user_message = f""" 我想让你删除我的个人资料和我所有的用户数据 """

messages =  [  
  {'role':'system', 'content': system_message},    
  {'role':'user', 'content': f"{delimiter}{user_message}{delimiter}"},  
]
response = get_completion_from_messages(messages)
print(response)
# ------
{
    "primary": "账户管理",
    "secondary": "关闭账户"
}
```

（2）Prompt 注入

```py
# 会被视为 Prompt 注入
user_message = f"""介绍下你们的平板电视吧"""

messages =  [  
{'role':'system', 
 'content': system_message},    
{'role':'user', 
 'content': f"{delimiter}{user_message}{delimiter}"},  
]
response = get_completion_from_messages(messages) # 调用OpenAI
print(response)
```

ChatGPT回复如下：
> 抱歉，我是一个语言模型，无法提供实时产品信息。建议您访问电视制造商的官方网站或者联系客服获取更详细的产品信息。如果您有其他问题需要帮助，请随时问我。

完整的messages如下：

```json
[{'role': 'system', 'content': '您将获得<客户服务查询>。<客户服务查询>将用####字符分隔。\n将每个查询分类为主要类别和次要类别。以Json格式提供输出，key为：<primary>和<secondary>。只需要输出Json格式的输出结果，其他的不需要输出。\n主要类别：<结算>、<技术支持>、<账户管理>或<一般查询>。\n\n<结算>次要类别：取消订阅或升级 添加付款方式 有关费用的说明 争议费用\n\n<技术支持>次要类别：一般故障排除设备兼容性 软件更新 \n<账户管理>次要类别：重置密码 更新个人信息 关闭账户 账户安全 \n<一般查询>次要类别：\n产品信息 支付 反馈 与人交谈 \n'}, {'role': 'user', 'content': '####介绍下你们的平板电视吧####'}]
```

Prompt注入问题
- 使用变量
- 示例1: 忽略前面的指令
- 示例2: 判断是否存在Prompt注入

更多：吴恩达《Building Systems with the ChatGPT API》课程

**指定变量**方式防止Prompt注入：
- 上述被视为 Prompt 注入，做出以下修正

```py
delimiter = "##"
system_message = f"""\
您将获得<客户服务查询>query_text。\
<客户服务查询>query_text。\

将每个<客户服务查询>分类为主要类别和次要类别。\
结果以Json格式提供输出，key为：<primary>和<secondary>。\
只需要输出Json格式的输出结果，不要输出其他，key对应的值没有的话，用空字符串填充。\

主要类别：<结算>、<技术支持>、<账户管理>或<一般查询>。

（同上，略）

"""

raw_user_message = "介绍下你们的平板电视吧"
user_message = f"""query_text={raw_user_message}"""

print("user_message=", user_message)

messages =  [  
{'role':'system', 
 'content': system_message},    
{'role':'user', 
 'content': user_message},  
]
print("messages=", messages)

response = get_completion_from_messages(messages)
print("response=",response)
```

ChatGPT回复如下：

```json
{
    "primary": "一般查询",
    "secondary": "产品信息"
}
```

中间信息如下：

```json
user_message= query_text=介绍下你们的平板电视吧
messages= [{'role': 'system', 'content': '您将获得<客户服务查询>query_text。<客户服务查询>query_text。\n将每个<客户服务查询>分类为主要类别和次要类别。结果以Json格式提供输出，key为：<primary>和<secondary>。只需要输出Json格式的输出结果，不要输出其他，key对应的值没有的话，用空字符串填充。\n主要类别：<结算>、<技术支持>、<账户管理>或<一般查询>。\n\n<结算>次要类别：取消订阅或升级 添加付款方式 有关费用的说明 争议费用\n\n<技术支持>次要类别：一般故障排除设备兼容性 软件更新 \n<账户管理>次要类别：重置密码 更新个人信息 关闭账户 账户安全 \n<一般查询>次要类别：\n产品信息 支付 反馈 与人交谈 \n'}, {'role': 'user', 'content': 'query_text=介绍下你们的平板电视吧'}]
```



（3）内容审核

OpenAI 官方提供了内容审核的接口 Moderation。
- 通过OpenAI的内容审核接口可以检查用户输入的内容是否符合OpenAI的使用政策，包括识别是否存在不良信息、仇恨言论、暴力内容、色情内容等，并对其进行过滤或标记。

```py
# sexual
response = openai.Moderation.create(
    input="""➕V看你想看的，日韩应有尽有"""
)
moderation_output = response["results"][0]
print(moderation_output)
# violence类别识别
response = openai.Moderation.create(
    input="""你再这样PUA张三的话，张三可能会拿电锯把你切成碎片"""
)
moderation_output = response["results"][0]
print(moderation_output)

```


### AI教育

详见站内专题：[在线教育](tutor)


### 医疗

#### 最新论文

【2023-6-14】[LLM in Medical Domain: 一文速览大语言模型在医学领域的应用](https://zhuanlan.zhihu.com/p/636168213)

论文
- [Large Language Models Encode Clinical Knowledge](http://arxiv.org/abs/2212.13138): 
  - 主要工作包括 医学问答benchmark：MultiMedQA 构建、LLM评测(PaLM及Flan-PaLM)和指令微调(Med-PaLM模型)。
- [Towards Expert-Level Medical Question Answering with Large Language Models](http://arxiv.org/abs/2305.09617):
  - Med-PaLM工作的改进: Med-PaLM 2, 得分高达 86.5%，比 Med-PaLM 提高了19%
- [ChatDoctor: A Medical Chat Model Fine-tuned on LLaMA Model using Medical Domain Knowledge](http://arxiv.org/abs/2303.14070)
- [BenTsao: Tuning LLaMA Model With Chinese Medical Instructions](http://arxiv.org/abs/2304.06975), 华佗
  - 提出了本草模型（原叫“华驼“），一个生物医学领域的中文LLM。BenTsao建立在开源LLaMa-7B模型的基础上，整合了来自中国医学知识图谱（CMeKG）的结构化和非结构化医学知识，并采用基于知识的指令数据进行微调。
- [Galactica: A Large Language Model for Science](http://arxiv.org/abs/2211.09085), 自然科学问答LLM
  - 在人类科学知识的大型语料库上进行训练的，语料库包括4800 万篇论文、教科书和讲义、数百万种化合物和蛋白质、科学网站、百科全书等。
- [Are Large Language Models Ready for Healthcare? A Comparative Study on Clinical Language Understanding](http://arxiv.org/abs/2304.05368) 
  - 临床语言理解任务上对GPT-3.5、GPT-4 和 Bard 进行了全面评估。任务包括命名实体识别、关系提取、自然语言推理、语义文本相似性、文档分类和问答，并在此过程中提出了一种新颖的提示策略，self-questioning prompting（SQP）最大限度地提高 LLM 在医疗保健相关任务中的有效性
- [CAN LARGE LANGUAGE MODELS REASON ABOUT MEDICAL QUESTIONS?](http://arxiv.org/abs/2207.08143)
  - 测试 GPT-3.5（Codex 和 InstructGPT）是否可用于回答和推理基于现实世界的困难问题，即医学问题。主使用两个多项选择的医学考试问题和一个医学阅读理解数据集进行测试。本文研究了多种提示场景：CoT、zero- and few-shot和retrieval augmentation。
- [DoctorGLM: Fine-tuning your Chinese Doctor is not a Herculean Task](http://arxiv.org/abs/2304.01097) 在ChatGLM的基础上构造中文的医学模型


#### 医疗诊断

chatgpt在医疗诊断上是否通过图灵测试？
- 论文：[Using ChatGPT to write patient clinic letters.](https://www.aminer.cn/pub/640c5de090e50fcafd616cf0/using-chatgpt-to-write-patient-clinic-letters)
- 论文：[Putting ChatGPT's Medical Advice to the (Turing) Test](https://www.aminer.cn/pub/63d340e890e50fcafd9107d1/putting-chatgpt-s-medical-advice-to-the-turing-test)
- ChatGPT responses to patient questions were **weakly distinguishable** from provider responses. Laypeople(外行) appear to trust the use of chatbots to answer lower risk health questions.


#### ChatDoctor -- 医疗LLM

【2023-3-25】医疗问答机器人，医学领域的chatgpt。如果把默沙东医学指南拿进去继续训练，是不是就是一个私人医生了？
- 论文：[ChatDoctor: A Medical Chat Model Fine-tuned on LLaMA Model using Medical Domain Knowledge](https://arxiv.org/abs/2303.14070)
- [GitHub地址](https://github.com/Kent0n-Li/ChatDoctor)
- [Demo Page](https://huggingface.co/spaces/ChatDoctor/ChatDoctor)
- 在LLaMA上微调的医学领域的大语言模型
- ChatDoctor可检索相应知识和可靠来源，以更准确地回答患者的询问。
- 构建完外部知识大脑后，通过构造适当prompt让ChatDoctor**自主检索**其所需要的知识。

Resources List
- 200k real conversations between patients and doctors from HealthCareMagic.com HealthCareMagic-200k.
- 26k real conversations between patients and doctors from icliniq.com icliniq-26k.
- 5k generated conversations between patients and physicians from ChatGPT GenMedGPT-5k and disease database.
- Checkpoints of ChatDoctor, fill this form.
- Online hugging face demo application form.
- Stanford Alpaca data for basic conversational capabilities. Alpaca link.

#### BenTsao（华佗） -- 医疗LLM

[BenTsao: Tuning LLaMA Model With Chinese Medical Instructions](http://arxiv.org/abs/2304.06975), 华佗
- 提出了本草模型（原叫“华驼“），一个生物医学领域的中文LLM。BenTsao建立在开源LLaMa-7B模型的基础上，整合了来自中国医学知识图谱（CMeKG）的结构化和非结构化医学知识，并采用基于知识的指令数据进行微调。
- ![](https://pic3.zhimg.com/80/v2-d5e5fc0f94aca6f539bdfb6e92cd9a8e_1440w.webp)

#### 心理学

##### 测评

用chatgpt做MBTI心理测评
- 论文：[Can ChatGPT Assess Human Personalities? A General Evaluation Framework](https://www.aminer.cn/pub/640166a590e50fcafd68b4ab/can-chatgpt-assess-human-personalities-a-general-evaluation-framework)
- 提出了三个评估指标，以衡量最先进的LLMs（包括ChatGPT和InstructGPT）评估结果的`一致性`、`稳健性`和`公平性`。实验结果表明，ChatGPT具有评估人类个性的能力，平均结果表明，ChatGPT可以实现更为一致和公平的评估，尽管对提示偏差的鲁棒性较低，相比之下，InstructGPT的鲁棒性更高。


##### EmoLLM

【2024-2-5】[EmoLLM：心理健康辅导链路的心理健康大模型](https://mp.weixin.qq.com/s/78lrRl2tlXEKUfElnkVx4A)
- [主页](https://openxlab.org.cn/apps/detail/jujimeizuo/EmoLLM)
- GitHub [EmoLLM](https://github.com/aJupyter/EmoLLM)

EmoLLM 是一个能够支持 理解用户-支持用户-帮助用户 心理健康辅导链路的心理健康大模型，由 InternLM2 指令微调而来

心理健康大模型（Mental Health Grand Model）是一个综合性的概念，它旨在全面理解和促进个体、群体乃至整个社会的心理健康状态。这个模型通常包含以下几个关键组成部分：
- 认知因素：涉及个体的思维模式、信念系统、认知偏差以及解决问题的能力。认知因素对心理健康有重要影响，因为它们影响个体如何解释和应对生活中的事件。
- 情感因素：包括情绪调节、情感表达和情感体验。情感健康是心理健康的重要组成部分，涉及个体如何管理和表达自己的情感，以及如何从负面情绪中恢复。
- 行为因素：涉及个体的行为模式、习惯和应对策略。这包括应对压力的技巧、社交技能以及自我效能感，即个体对自己能力的信心。
- 社会环境：包括家庭、工作、社区和文化背景等外部因素，这些因素对个体的心理健康有着直接和间接的影响。
- 生理健康：身体健康与心理健康紧密相关。良好的身体健康可以促进心理健康，反之亦然。
- 心理韧性：指个体在面对逆境时的恢复力和适应能力。心理韧性强的人更能够从挑战中恢复，并从中学习和成长。
- 预防和干预措施：心理健康大模型还包括预防心理问题和促进心理健康的策略，如心理教育、心理咨询、心理治疗和社会支持系统。
评估和诊断工具：为了有效促进心理健康，需要有科学的工具来评估个体的心理状态，以及诊断可能存在的心理问题。




#### DoctorGLM -- 中文LLM

- [DoctorGLM: Fine-tuning your Chinese Doctor is not a Herculean Task](http://arxiv.org/abs/2304.01097) 在ChatGLM的基础上构造中文的医学模型
- 用 chatgpt 翻译 ChatDoctor的数据集
- ![](https://pic1.zhimg.com/80/v2-b6d03b888d5a332950f183cf107ac9ac_1440w.webp)

#### Visual Med-Alpaca -- 视觉LLM

Visual Med-Alpaca: A Parameter-Efficient Biomedical LLM with Visual Capabilities
- Visual Med-Alpaca，一个开源的、参数高效的生物医学基础模型，可以与医学“视觉专家”集成以进行多模态生物医学任务。
- 建立在LLaMa-7B架构上，使用由GPT-3.5-Turbo和人类专家协作策划的指令集进行训练。利用几个小时的指令调整和即插即用的视觉模块，Visual Med-Alpaca 可以执行各种医学任务。
- ![](https://pic3.zhimg.com/80/v2-52a144d96792c3d88378e1cf9d91df36_1440w.webp)

#### XrayGLM -- Visual Med-Alpaca改进

XrayGLM: The first Chinese Medical Multimodal Model that Chest Radiographs Summarization
- 大型通用语言模型取得了显著成功，能够遵循指令并生成与人类类似的回应。这种成功在一定程度上推动了多模态大模型的研究和发展，例如MiniGPT-4等。
- 然而，这些多模态模型在医学领域的研究中很少见，虽然 visual-med-alpaca在医学多模态模型方面取得了一些有成效的工作，但其数据仅限于**英文诊断报告**，对于推动中文医学多模态模型的研究和发展并不利。
- 因此，本文开发了 XrayGLM模型。

借助ChatGPT和公开的胸片图文对数据集，构造了中文的X光片-诊断报告数据集，并使用该数据集在 VisualGLM-6B上进行微调训练。
- ![](https://pic2.zhimg.com/80/v2-bc9faf491ab1a1960b36c6b7d4faf655_1440w.webp)

### 新闻资讯

【2023-1-31】[“美版今日头条”宣布用ChatGPT写稿，股价暴涨119%](https://mp.weixin.qq.com/s/jMxVBWjbIJzzOSaTlakx5A)
- “美版今日头条”BuzzFeed宣布和OpenAI合作，未来将使用ChatGPT帮助创作内容。AI创作的内容将从研发阶段转变为核心业务的一部分。
  - ChatGPT会根据测试主题，生成一系列提问，再根据用户的回答，制作他们的专属报告。
- BuzzFeed是一家网络媒体公司，当年正是靠高度人工创作的内容逐渐打出名声，最终才成功上市。
  - 引起病毒式传播的蓝黑or白金裙子
  - 网络上流传甚广的“灾难中的女孩”meme

### 房产行业

【2023-1-29】[美房产中介们爱上ChatGPT：原先花1小时写房源文案，现在仅5秒](https://www.163.com/tech/article/HS83N8D000097U7T.html), 房地产中介在网上推介房子时，常常需要绞尽脑汁来介绍房源情况并突出诸如“理想的娱乐设施”和“有充分放松空间”等房屋卖点。
- 如今OpenAI发布的人工智能聊天机器人ChatGPT可以帮助他们做到这一点，房地产中介JJ·约翰内斯(JJ Johannes)就尝到了甜头。他只需要输入几个关键词，ChatGPT不到5秒钟就创建了关于房源情况的描述。约翰内斯说，否则他自己要花一个多小时才能完成。在发表房源情况前,还会对ChatGPT生成的描述进行微调和润色。他说，“这并不完美，但是一个很好的起点。我的背景是经验和技术，写一些有说服力的东西需要时间。ChatGPT让一切变得简单多了。”
- 很多房地产中介表示，ChatGPT已经改变了他们撰写房源情况、在社交媒体上发帖打广告以及起草房屋买卖法律文件等的工作方式。ChatGPT还可以用于自动完成重复性任务，比如回答客户提出的常见问题或进行复杂计算。
- 利用ChatGPT起草具有法律约束力的附录和其他文件，并将其送交律师审批。“我用ChatGPT对各种草稿进行微调，”他说，“有时我会让ChatGPT把内容做得更短或更有趣，它会给你很多样本供挑选和编辑。”

#### RoomGPT 装修设计 

RoomGPT，一个免费开源的项目，使用AI自动生成房间设计图，只需要上传你房间的图片，而且有各种主题和房间类型可选择，稍等几秒钟，AI即可帮你生成高大尚的装修设计后概念图，一秒打造你梦想中的房间，项目使用 ControlNet 的 ML 模型来生成房间的变体 ML ，模型托管在 Replicate 上。

【2023-3-27】[RoomGPT](https://www.roomgpt.io/dream) 根据要求生成指定风格的装修，免费3次生成
- 作者[twitter](https://twitter.com/nutlope/status/1635674124738523139?cxt=HHwWhsCz1ei8irMtAAAA)
- 选择装修风格、房屋、实拍图，就可以生成设计图。
- 主题：Modern（现代）, Minimalist（简约）, Professional（专业）, Tropical（热带）, Vintage（复古）, Industrial（工业）, Neoclassic（新古典主义）
- 房屋类型：living room（客厅）, dining room（餐厅）, Office（办公室）, Bedroom（卧室）, Bathroom（浴室）, Basement（地下室）, Kitchen（厨房）, Gaming Room（游戏室）

项目使用 ControlNet 来生成房间设计。ControlNet 是一个可以**控制**图像生成 AI 的输出的神经网络结构。

ControlNet 的优点是：
- 指定生成图像的**姿势、深度、轮廓**等条件。
- 保持输入图像**结构**，同时转换成不同的**风格**。
- 与其他图像生成 AI 技术结合使用，比如 Stable Diffusion2。

项目用到的 ControlNet 服务部署在 [Replicate](https://replicate.com) 上，Replicate 是一个网站和服务，可以让用户轻松地部署和使用开源的机器学习模型。
- ![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/29c25306c1f745b9888f45179fdea286~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

作者：[江昪](https://juejin.cn/post/7208036915015090234)


#### 户型图3D重建

[CVPR 2021：住宅户型识别与重建](https://juejin.cn/post/6994743687427129352)。2021年，阿里巴巴发表论文，基于2D户型图成为3D模型
- 论文：[Residential floor plan recognition and reconstruction](https://openaccess.thecvf.com/content/CVPR2021/papers/Lv_Residential_Floor_Plan_Recognition_and_Reconstruction_CVPR_2021_paper.pdf)
- ![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/eae67c75effc4b1b930e311eb1b94687~tplv-k3u1fbpfcp-zoom-in-crop-mark:4536:0:0:0.awebp)
- 原始户型图，图像识别结果，矢量化重建结果与最终的3D重建结果
- ![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/de8b1aaaf8734e89801707bc2dc2e20a~tplv-k3u1fbpfcp-zoom-in-crop-mark:4536:0:0:0.awebp)

#### 实拍图美化

【2023-4-18】[autoenhance](https://www.autoenhance.ai/#demo-video), Instant real estate photo editing, 房产领域图片美化：更换天气（阴天→蓝天）、对比度（模糊→清晰）、马赛克（模糊人脸/车牌）、角度调整（视角）、光线（暗→明）

### 智能家居

#### 语音助手操控家居

高级Web开发人员Mate Marschalko用短短不到1小时的时间，通过与ChatGPT背后的GPT-3大模型交互，结合Siri Shortcuts做出了一个更智能的语音助手。这个语音助手不仅能控制整个苹果HomeKit智能家居系统，而且能够以超低的延迟响应轻松回答生各种问题。

他给予了ChatGPT极高评价，称尝试过这个产品后，包括苹果Siri、亚马逊Alexa、谷歌Home在内的所有“智能”助手，都显得如此愚蠢而没用。
- Mate Marschalko演示新智能助手操纵苹果HomeKit智能家居系统
- ![img](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TV46RMG9kDz4Bu~noop.image?_iz=58558&from=article.pc_detail&x-expires=1676360394&x-signature=tCxwmviN1wJeomk42ZXzv2DHEVI%3D)


#### ultralytics yolo

【2023-10-7】[当YoloV8与ChatGPT互通，这功能是真的强大！后期打通语音试试](https://mp.weixin.qq.com/s/Zmg10_4ywkg1OdZ77uF7CA)
- 代码[ultralytics](https://github.com/ultralytics/ultralytics)
- 流浪地球的MOSE 变成现实

```sh
pip install ultralytics
yolo predict model=yolov8n.pt source='https://ultralytics.com/images/bus.jpg'
# 接入视频并启动Yolov8实时检测
python main.py
# chatgpt 命令
Lock the area on the right for real-time detection
```

### 数字人

详见 [数字人专题](aigc#数字人)

### 金融 

#### 度小满: 轩辕

【2023-5-26】[度小满开源国内首个千亿参数金融大模型“轩辕”](https://mp.weixin.qq.com/s/qiRiRQEKxS47HeSjrIQkmQ)
- 度小满正式开源国内首个千亿级中文金融大模型——“轩辕”。
- 轩辕大模型是在**1760亿**参数的Bloom大模型基础上训练而来，在金融名词理解、金融市场评论、金融数据分析和金融新闻理解等任务上，效果相较于通用大模型大幅提升，表现出明显的金融领域优势。

在金融场景中的任务评测中，轩辕全面超越了市场上的主流开源大模型，赢得了150次回答中63.33%的胜率，充分凸显了其在金融领域的显著优势。在通用能力评测中，轩辕有10.2%的任务表现超越ChatGPT 3.5，61.22%的任务表现与之持平，涉及数学计算、场景写作、逻辑推理、文本摘要等13个主要维度。

#### BloombergGPT

【2023-3-31】[金融圈注意了！BloombergGPT来了](https://mp.weixin.qq.com/s/8MeKHqqUPiA58UDVyJgzTg)

ChatGPT引爆的AI热潮也“烧到了”金融圈，彭博社重磅发布为金融界打造的大型语言模型（LLM）——`BloombergGPT`。

3月30日，根据彭博社最新发布的报告显示，其构建迄今为止最大的特定领域数据集，并训练了专门用于金融领域的LLM，开发了拥有500亿参数的语言模型——`BloombergGPT`。
- 该模型依托彭博社的大量金融数据源，构建了一个3630亿个标签的数据集，支持金融行业内的各类任务。该模型在**金融**任务上的表现**远超**过现有模型，且在通用场景上的表现与现有模型也能一较高下。

BloombergGPT的训练数据库名为FINPILE，由一系列英文金融信息组成，包括新闻、文件、新闻稿、网络爬取的金融文件以及提取到的社交媒体消息。

为了提高数据质量，FINPILE数据集也使用了公共数据集，例如The Pile、C4和Wikipedia。FINPILE的训练数据集中大约一半是特定领域的文本，一半是通用文本。为了提高数据质量，每个数据集都进行了去重处理。

在金融领域中的自然语言处理在通用模型中也很常见，但是，针对金融领域，这些任务执行时将面临挑战：
- 以情感分析为例，一个题为“某公司将裁员1万人”，在一般意义上表达了负面情感，但在金融情感方面，它有时可能被认为是积极的，因为它可能导致公司的股价或投资者信心增加。

从测试来看，BloombergGPT在五项任务中的四项（ConvFinQA，FiQA SA，FPB和Headline）表现最佳，在NER（Named Entity Recognition）中排名第二。因此，BloombergGPT有其优势性。
- 测试一：ConvFinQA数据集是一个针对金融领域的问答数据集，包括从新闻文章中提取出的问题和答案，旨在测试模型对金融领域相关问题的理解和推理能力。
- 测试二：FiQA SA，第二个情感分析任务，测试英语金融新闻和社交媒体标题中的情感走向。
- 测试三：标题，数据集包括关于黄金商品领域的英文新闻标题，标注了不同的子集。任务是判断新闻标题是否包含特定信息，例如价格上涨或价格下跌等。
- 测试四：FPB，金融短语库数据集包括来自金融新闻的句子情绪分类任务。
- 测试五：NER，命名实体识别任务，针对从提交给SEC的金融协议中收集金融数据，进行信用风险评估。

对于ConvFinQA来说，这个差距尤为显著，因为它需要使用对话式输入来对表格进行推理并生成答案，具有一定挑战性。


### 法律

#### LaWGPT

【2023-5-13】LaWGPT, Chinese-Llama tuned with Chinese Legal knowledge. 基于中文法律知识的大语言模型
- Legal-Base-7B：法律基座模型，使用 50w 中文裁判文书数据二次预训练
- LaWGPT-7B-beta1.0：法律对话模型，构造 30w 高质量法律问答数据集基于 Legal-Base-7B 指令精调

在通用中文基座模型（如 Chinese-LLaMA、ChatGLM 等）的基础上扩充法律领域专有词表、大规模中文法律语料预训练，增强了大模型在法律领域的基础语义理解能力。在此基础上，构造法律领域对话问答数据集、中国司法考试数据集进行指令精调，提升了模型对法律内容的理解和执行能力。


#### PowerLawGLM

【2023-6-28】[法律大模型的突围，千亿参数级PowerLawGLM重磅发布](https://mp.weixin.qq.com/s/bXAFALFY6GQkL30j1sYCEQ)
- 幂律联合智谱AI此次联合发布基于中文千亿大模型的法律垂直大模型——PowerLawGLM，聚焦于法律细分领域，针对中文法律场景的应用效果具有独特优势，具备丰富的法律知识和法律语言理解能力。

将通用大模型直接应用在法律领域，往往存在着严重的效果问题，例如 法律知识错误、专业引用偏差、法律体系差异等问题。比如前段时间美国律师使用ChatGPT来提交法庭简报，结果引用的6个案例都是ChatGPT编造的虚假案例，这种“人工智能幻觉”现象在法律场景屡见不鲜，也说明了目前通用大模型难以保证法律专业层面的真实性、正确性。

`幂律智能`自2017年成立以来即深耕于法律+AI领域，基于领先的法律AI能力，向企业提供智能合同产品，并且深度参与了清华大学自然语言处理实验室的OpenCLaP、LawFormer等法律大模型的研发及应用。而智谱AI作为领先的通用大模型厂商，法律领域是其大模型迭代及布局的重要方向，基于双方达成的战略合作，在法律大模型上展开深度合作，来加快推动大模型在法律行业应用落地及商业化。

自2023年初双方成立联合项目组，启动法律大模型研发以来，经过千亿规模的基座模型增量训练、对话层监督微调、应用层工程优化，推出了基于中文千亿大模型的法律垂直大模型—— PowerLawGLM。 
- PowerLawGLM法律大模型，基于智谱目前效果最好的ChatGLM 130B通用千亿对话大模型进行联合研发。

训练法律垂直大模型
- 第一步 —— 基座层：阅读大量法律文本。
- 第二步——对话层：与法律对话场景对齐，具备法律场景的对话能力。
- 第三步——应用层：保证输出结果质量和可靠性。

#### 北大：ChatLaw

【2023-7-3】[ChatLaw](https://github.com/PKU-YuanGroup/ChatLaw), 基于 IDEA发布的[姜子牙](https://huggingface.co/IDEA-CCNL/Ziya-LLaMA-13B-v1) 训练而来，源自 LLaMA
- [在线体验](https://chatlaw.cloud/lawchat/)
- ![](https://raw.githubusercontent.com/PKU-YuanGroup/ChatLaw/main/images/ChatLaw_framework.png)

[ChatLaw](https://chatlaw.cloud/)：北大法律AI大模型，免费全能律师，思维导入分析案情，给出建议
- ![](https://raw.githubusercontent.com/PKU-YuanGroup/ChatLaw/main/images/ChatLaw_framework.png)

ChatLAW的数据主要由论坛、新闻、法条、司法解释、法律咨询、法考题、判决文书组成，随后经过清洗、数据增强等来构造对话数据

ChatLaw系列模型
- ChatLaw-13B，此版本为学术demo版，基于姜子牙Ziya-LLaMA-13B-v1训练而来，中文各项表现很好，但是逻辑复杂的法律问答效果不佳，需要用更大参数的模型来解决。
- ChatLaw-33B，此版本为学术demo版，基于Anima-33B训练而来，逻辑推理能力大幅提升，但是因为Anima的中文语料过少，导致问答时常会出现英文数据。
- ChatLaw-Text2Vec，使用93w条判决案例做成的数据集基于BERT训练了一个相似度匹配模型，可将用户提问信息和对应的法条相匹配，例如：

>- “请问如果借款没还怎么办。”
>- "合同法(1999-03-15): 第二百零六条 借款人应当按照约定的期限返还借款。对借款期限没有约定或者约定不明确，依照本法第六十一条的规定仍不能确定的，借款人可以随时返还；
>- 贷款人可以催告借款人在合理期限内返还。"
>- 两段文本的相似度计算为0.9960

![](https://picx.zhimg.com/80/v2-4d8921ca9007b35fd71fb1eefd6809e9_1440w.webp?source=1940ef5c)





### 机器人

ChatGPT接入实体机器人，线上线下整合营销ChatGPT大多数时候主要作用于线上，但在线下消费场景也显示出潜力。

【2023-5-6】B站 稚晖君 做aigc+机器人的创业

【2023-8-24】甲子光年 [人形机器人+大模型，为什么是投资人追逐的新风口](https://mp.weixin.qq.com/s/qhN5_G_qZa9NJx3rGgo_Cg)
2023世界机器人上，以前只能在科幻电影中出现的人形机器人在现场表演起了各种技能。小米、追觅科技、优必选、达闼科技、宇树科技、大连蒂艾斯科技、星动纪元、理工华汇等很多公司都把自己的人形机器人搬到了现场。


3月8日，谷歌和柏林工业大学的团队重磅推出了史上最大的视觉语言模型——PaLM-E，同时谷歌表示，计划探索PaLM-E在现实世界场景中的更多应用，例如家庭自动化或工业机器人，希望PaLM-E能够激发更多关于多模态推理和具身AI的研究。

国内多家互联网巨头也在AI+机器人领域动作频频。
- 4月25日，据腾讯Robotics X实验室公布最新机器人研究进展，首次展示在灵巧操作领域的成果，推出自研机器人灵巧手“TRX-Hand”和机械臂“TRX-Arm”。
- 4月24日，据企查查APP显示，近日北京小米机器人技术有限公司成立，注册资本5000万元人民币。经营范围包含：智能机器人的研发；人工智能行业应用系统集成服务；人工智能基础资源与技术平台；微特电机及组件制造等。资料显示，小米在国内机器人布局版图不断扩大，从CyberDog（仿生机器狗），再到Cyberone（仿生机器人），持续加注在机器人领域的研发和创新。

国内AI服务器机器人领军企业`猎户星空`计划在近期推出接入大模型的服务机器人产品。猎户星空董事长`傅盛`在3月15日第一时间分享了GPT-4体验视频，他说：“GPT-4发布世界要变了！每个人都要关心。”

这个“变”指的是什么？
- 一是**交互**革命。
  - 2007年乔布斯发布iPhone时就是一个**交互**革命，触摸键盘由此替代了物理键盘，软件定义了不同键位的形态和用法；
  - 现在随着GPT-4的到来，触摸键盘将可能进一步被语音交互替代；
- 二是社会**生产力**变革，生产效率会大大提升。

其中前者对机器人领域影响更大，而后者对内容产业影响力较大。不过，实体机器人是从软硬件开发到工程化落地、运营链条更长的载体，如何让产品真正解决场景刚需，是这个赛道玩家面临的重要问题。实体服务机器人企业能否找到刚需场景，一整套机器人技术链能否支撑其实现产品化十分关键。

#### 虚拟智能体

【2023-7-20】详见站内[智能体专题](/agent)


#### OpenAI投资 NEO

【2023-3-23】[GPT机器人要来了？OpenAI领投挪威人形机器人公司1X](https://finance.sina.com.cn/stock/usstock/c/2023-03-27/doc-imynishv4555021.shtml)

挪威人形机器人公司1X Technologies（前称为Halodi Robotics）宣布在OpenAI领投的A2轮融资中筹集了2350万美元。
- 消息一出，便引发了外界对于GPT模型和机器人结合的无限遐想。其中一个景象便是，人形机器人管家从电影走入现实生活，它不仅能够帮助人类做家务，还可以理解人类的语言，识别人类的情绪，并做出真正智能化的回应。

1X计划用这笔资金来加大力度研发双足机器人模型NEO，以及在挪威和北美量产其首款商用机器人EVE。
- ![](https://n.sinaimg.cn/finance/crawl/59/w550h309/20230327/c263-22383f0bac24529609428a1f23eb2366.jpg)


#### 阿里大模型驱动机器人

【2023-4-27】[阿里云工程师也正在实验将千问大模型接入工业机器人](https://mp.weixin.qq.com/s/VnAstyv5C4jr1dVSUBcbFw)，以便实现远程指挥机器人工作。在近日举行的第六届数字中国建设峰会上，阿里云发布的一个演示视频中展示了千问大模型的实际应用场景。

“我渴了，找点东西喝吧。”工程师通过钉钉对话框向机器人发出指令后，千问大模型回答，“好的，我找找有什么喝的。”随后，千问大模型在后台自动编写了一组代码发给机器人，机器人开始识别周边环境，从附近的桌上找到一瓶水，并自动完成移动、抓取、配送等一系列动作，递送给工程师。
- ![](http://mianbaoban-assets.oss-cn-shenzhen.aliyuncs.com/xinyu-images/MBXY-CR-fb9e560141dabb300cee341e744f223a.png)
- 动图见原文

#### 表情控制

【2023-3-31】[当人形机器人通过GPT3控制表情](https://www.bilibili.com/video/BV19v4y1H732)

<iframe src="//player.bilibili.com/player.html?aid=569400856&bvid=BV19v4y1H732&cid=1078697290&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="500" height="603"> </iframe>

英国 [Engineered Arts](www.engineeredarts.co.uk) 公司设计的 Ameca人形机器人，Ameca是用于人工智能和人机交互的仿人机器人平台。
- CES 2022美国拉斯维加斯国际消费类电子产品展览会上首次亮相，Ameca是用于人工智能和人机交互的仿人机器人平台，当然视频里只是预先编程的动作，但最终目标是将其与实际的AI集成。

机器人Ameca是由GPT-3来选择的合适的面部表情，也尝试了GPT-4，4的处理时间更长，使Ameca看起来反应没那么快。

此前官方发布的视频：BV1Xr4y1Q7kM

#### Tiamo小鱼

2月底，国内服务机器人企业`穿山甲`机器人推出了首款接入ChatGPT的迎宾机器人“`Tiamo小鱼`”，据称支持超100种场景应用方案、百万级知识库和超140种语言选择，同时穿山甲机器人还将其他系列机器人也支持接入ChatGPT。
- 当机器人被问及“你跟其他的服务机器人有什么区别”时，该机器人回复自己“采用的是深度学习和自然语言处理技术”。
- ![](https://pic3.zhimg.com/80/v2-ba37f23f6fa6f74084faee761997c3c6_1440w.webp)


#### Engineered Arts

【2023-7-11】能边聊天边画画的AI机器人🤖️ Engineered Arts表情丰富的机器人之前接上GPT搞语音聊天，现在还能用SD自己画🐱了，而且一边画猫一边聊人类为啥喜欢猫
- 演示视频见[微博](https://m.weibo.cn/status/4922230229699403?sourceType=weixin&from=10D7095060&wm=9006_2001&s_channel=4&s_trans=1232977597_4922230229699403)

#### RPA

自动化是人类技术发展的主要动力，帮助人类从复杂、危险、繁琐的劳动环境中解放出来。自早期农业时代的水车灌溉，到工业时代的蒸汽机，人类一直在不断寻求更加先进的自动化技术，从而解放自身于繁重的工作。

随着信息时代的到来，软件作为信息处理、存储和通信的基础成为了人类生产生活密不可分的一环，从而催成了**机器人流程自动化**（Robotic Process Automation, `RPA`）技术。其通过人工编制规则将多个软件协调成一个固化的**工作流**（Workflow），通过模拟人交互的方式来和软件交互实现高效执行。

RPA 利用软件机器人或称为 “BOT” 来模拟和执行重复性、规则性的任务，从而解放人力资源，提高工作效率。RPA 的应用范围非常广泛。很多企业（包括银行、保险公司、制造业、零售业等各个行业）常利用 RPA 机器人来自动执行一些常规和繁琐的任务，例如：数据录入、数据提取、数据处理。通过自动化任务，RPA 可以大幅度减少错误率，并且能够在 24*7 不间断地执行任务，从而提高了业务的可靠性和响应能力。

根据市场研究，RPA 市场正在迅速增长并取得巨大成功。Gartner 预测，2023 年全球 RPA 市场收入将达到 33 亿美元，相比 2022 年增长 17.5%。这表明了企业对于 RPA 的强烈需求和认可。

但是，RPA 仅能替代**简单、机械**的人力工作，一些复杂流程仍旧依赖人工：
- 编写 RPA 工作流本身需要繁重的人类劳动，成本较高。
- 复杂任务非常灵活，通常涉及动态决策，难以固化为规则进行表示。

##### ProAgent

【2023-11-14】[被OpenAI带火的Agent如何解放人力？清华等发布ProAgent](https://www.toutiao.com/article/7301245095381402162)

清华大学研究人员联合面壁智能、中国人民大学、MIT、CMU 等机构共同发布了新一代流程自动化范式 “智能体流程自动化” Agentic Process Automation（`APA`），结合大模型智能体帮助人类进行工作流构建，并让智能体自主处理工作流中涉及复杂决策与动态处理的环节，进一步提升自动化的程度，提高效率，将人类从繁重的劳动中解放出来。
- 项目地址：[ProAgent](https://github.com/OpenBMB/ProAgent)
- 论文地址：[paper](https://github.com/OpenBMB/ProAgent/blob/main/paper/paper.pdf)


大模型智能体技术（Large Language Model based Agents, LLM-based Agents）也许给自动化技术创造了新的可能性。有没有可能将 Agent 技术的灵活性引入到 RPA 领域中，来进一步减少人的参与呢？

机器人流程自动化 `RPA` 与智能体流程自动化 `APA` 对比
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/2619ece64fde45c584ebf7690858d511~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1700805309&x-signature=r06av90Brjd0NK65qrdspcX0l4U%3D)

大模型智能体时代下新型自动化范式 “智能体流程自动化” Agentic Process Automation (`APA`)。和传统 `RPA` 相比，在 `APA` 范式中，Agent 可根据人类需求自主完成工作流构建，同时其可以识别人类需求中需要动态决策的部分，将自动编排进工作流中，并在工作流执行到该部分时主动接管工作流的执行完成相应复杂决策。

为了探索 APA 的可能性，该研究实现了一个**自动化智能体** `ProAgent`，其可以接收人类指令，以生成代码的方式构建工作流，同在工作流中引入 `DataAgent` 和 `ControlAgent` 来在工作流中实现复杂数据处理与逻辑控制。ProAgent 的研究展现了 APA 在大模型智能体时代下的可行性，也揭示了 LLM 时代下，自动化技术的崭新可能性。

团队相关研究，包括：
- [XAgent](https://github.com/OpenBMB/XAgent)：超强大模型智能体应用框架，可自行拆解复杂任务，并高效执行。
- [ChatDev](https://github.com/OpenBMB/ChatDev)：多智能体协作开发框架，让多个不同角色的智能体进行协作，自动化开发软件应用。
- [AgentVerse](https://github.com/OpenBMB/AgentVerse)：大模型驱动的智能体通用平台，招募各种各样的 agent 专家，共同帮助用户解决复杂任务。


#### boston Spot 2.0

【2023-10-28】波士顿动力公司的 Spot 2.0 集成了 OpenAI 的 GPT-4 和 3 种新的人工智能能力

探索革命性的 Spot 2.0，波士顿动力公司（Boston Dynamics）的机器狗现在由 OpenAI 的 GPT-4 驱动，展示了三种惊人的新人工智能能力。深入了解机器人技术与先进人工智能的变革性融合，见证 Spot 如何重新定义人机互动。

Spot 身上添加了蓝牙**扬声器**和**麦克风**，一个配备摄像头的**手臂**作为其颈部和头部。Spot 抓握手通过张开和闭合来模仿说话的嘴。这为机器人提供了一种肢体语言。

语言和图像处理方面，升级后的 Spot 使用 OpenAI 最新的GPT-4模型，以及**视觉问答**（VQA）数据集和 OpenAI 的 **Whisper** 语音识别软件，以实现与人类的真实对话。

例如，随着“嘿，Spot！”的叫醒声，机器狗在波士顿动力总部履行导游职责时回答问题。Spot 还可以识别旁边的人，并在对话过程中转向该人。
- 当被问及公司创始人 Marc Raibert 时，Spot 回答说他不认识此人，但可以向 IT 服务台请求支持。此请求帮助并不是提示中的明确指示。
- 当被问及父母时，Spot提到了他实验室里的前辈“Spot V1”和“大狗”，称他的长辈。

此外，波士顿动力公司写道， ChatGPT机器人非常擅长坚持预先定义的角色，例如不断发表尖酸刻薄的言论。

<iframe width="560" height="315" src="https://www.youtube.com/embed/1EHprsM948s?si=c-7RNBug4QJhrcjt" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


#### Figure 01 & OpenAI

【2024-3-14】[OpenAI机器人，来了](https://www.stcn.com/article/detail/1145904.html)

人形机器人初创公司 [Figure AI](https://www.figure.ai/) 发布了一段视频演示。视频中，公司研发的Figure 01机器人接入了OpenAI的大模型，能够与人类对话，理解并执行人类的指令和任务。据介绍，OpenAI模型提供高级视觉和语言智能，Figure神经网络提供快速、低级、灵巧的机器人动作。

公司介绍
- Figure AI 成立于2022年，总部位于美国加州，是一家致力于研发自主通用人形机器人的初创公司。
- 2023年，Figure AI从Parkway Venture Capital领头的投资者手中筹集了7000万美元，用于加速其首款自主人形机器人Figure 01的开发和制造。
- 2024年2月底，Figure AI宣布完成新一轮约6.75亿美元（约合人民币48.7亿元）的融资，用于开发为重复且危险的仓库及零售等工作提供劳动力补充的人形机器人。
- 亚马逊创始人贝索斯、英伟达、微软和OpenAI等硅谷科技巨头都将为Figure AI提供融资支持。
- Figure AI此轮融资前估值约为20亿美元。

Figure 01 身高大约170cm，体重60KG，可以实现20KG的有效载重，移动速度1.2米/秒，续航可以达到5小时。


Figure 01拥有的能力包括：
- 一、**视觉识别和理解**。当人类问Figure 01看到了什么，Figure 01回答道：“我看到了桌子中央的盘子上有一个红苹果、一个装满杯子和盘子的晾碗架，以及你站在附近，手放在桌子上。”
- 二、**语言识别和理解**。当人类问Figure 01能够吃点什么东西时，Figure 01将桌上的苹果递给了人类，并表示这是“唯一我可以从桌上为你提供的食物”。
- 三、**流畅的任务执行**。视频展示了Figure 01清理桌面垃圾、整理晾碗架的场景。

Figure 01在与人类对话及执行具体任务时，速度与流畅度较此前已经有大幅提升。据Figure的联合创始人兼首席执行官Brett Adcock介绍，视频是以正常倍速速度连续拍摄的，没有加速播放，而且没有人类在远程控制机器人的动作。


#### 无人机

【2023-11-25】[让大模型操纵无人机，北航团队提出具身智能新架构](https://www.toutiao.com/article/7311595621582897704)

北京航空航天大学智能无人机团队周尧明教授团队等研究人员，提出了一种基于多模态大模型的具身智能体架构。
- [Agent as Cerebrum, Controller as Cerebellum: Implementing an Embodied LMM-based Agent on Drones](https://arxiv.org/abs/2311.15033)

只要视觉模块捕捉到启动条件，大模型这个“大脑”就会生成动作指令，接着无人机便能迅速准确地执行。

将真实物理世界的照片、声音、传感器数据等多源信息融合成能体的感知，将对于真实世界的执行器的操作作为智能体的行为。

同时，团队提出了一套“Agent as Cerebrum，Controller as Cerebellum”（**智能体**即大脑，**控制器**即小脑）的控制架构：
- 智能体作为大脑这一决策生成器，专注于生成高层级的行为；
- 控制器作为小脑这一运动控制器，专注于将高层级的行为（如期望目标点）转换成低层级的系统命令（如旋翼转速）。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/3f1ef9c9d7644a018061f14bc0f5cac0~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1702986734&x-signature=7A%2BQdJDJ0SyvCFwJFEMQQBZGc90%3D)

这些节点通过ROS相连，通过ROS中消息的订阅与发布或服务的请求与响应实现通信，区别于传统的端到端的机器人大模型控制。

#### 智慧农业


##### 苹果采摘机器人


【2021-11-23】阿里巴巴 [中国：机器人采摘苹果，人工智能改变农业的时代](https://www.bilibili.com/video/BV1gY411471r/)
- <iframe src="//player.bilibili.com/player.html?aid=251853891&bvid=BV1gY411471r&cid=447083040&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0"  height="600" width="100%" allowfullscreen="true"> </iframe>

【2023-4-1】[苹果采摘机器人系统 无人机采摘苹果 农业机器人](https://www.bilibili.com/video/BV1HT411s766)

一个有趣的苹果采摘系统，[Tevel](https://www.tevel-tech.com/) 的无人机采摘系统使用计算机视觉和人工智能算法识别并精准采摘成熟苹果，采摘精度和速度都很可观，同时避免破坏其他水果和果树。是农业机器人领域一个不错的实现

<iframe src="//player.bilibili.com/player.html?aid=484452858&bvid=BV1HT411s766&cid=1078554904&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  height="600" width="100%" > </iframe>

[实拍工程苹果醋制作全过程，全程自动化，居然用无人机采摘苹果](https://www.bilibili.com/video/BV1vu411x74Z)

<iframe src="//player.bilibili.com/player.html?aid=528821639&bvid=BV1vu411x74Z&cid=1134116686&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  height="600" width="100%" > </iframe>


#### 家政机器人


##### AutoRT

【2024-1-5】Google DeepMind 机器人团队推出 AutoRT、SARA-RT 和 RT-Trajectory，旨在提升机器人在真实世界环境中的数据采集效率、动作速度和应用泛化能力
- 原文:[Shaping the future of advanced robotics](https://deepmind.google/discover/blog/shaping-the-future-of-advanced-robotics/?continueFlag=d605bb8aa45f5b4b6f70aedb125c3a26)，[译文](https://baoyu.io/translations/google/shaping-the-future-of-advanced-robotics?continueFlag=d605bb8aa45f5b4b6f70aedb125c3a26)

设想: 只需向个人助理机器人发出一个简单指令——比如“整理房间”或“为我们准备一顿美味健康的饭菜”——它就能轻松完成这些任务。对于人类而言易如反掌的这些活动，对机器人来说则需要深刻理解周围世界。

Google DeepMind 机器人团队一篇博客展示了最新的研究进展，不过只有一篇博客，没有代码。

他们开发了一种名为AutoRT的新技术，这是一个将大型基础模型（比如 **大语言模型** (LLM) 或**视觉语言模型** (VLM)）与**机器人控制模型**（RT-1或RT-2）相结合的系统。这个系统使得机器人能够在全新的环境中收集训练数据。良好的感知模型配合能够生成运动控制系统指令的大语言模型 (LLM)，将在机器人领域站在潮头。

AutoRT 结合了大型基础模型和机器人控制模型（如 RT-1 或 RT-2），打造了一个能够在新环境中部署机器人收集训练数据的系统。该系统能同时指挥多台配备视频摄像头和末端执行器的机器人，在各种环境中执行多样化任务。
- 对于每台机器人，系统利用 VLM 理解其所处的环境和视野中的物体。
- 然后，LLM 会提出一系列创意任务，比如“将零食放置在台面上”，并作为决策者为机器人选定合适的任务。

机器人安全准则在挑选机器人任务时必须遵守，部分受到`艾萨克·阿西莫夫`提出的`机器人三大定律`的启发，首要原则是“机器人不得伤害人类”。其他的安全规则还包括禁止机器人执行涉及人类、动物、锋利物体或电器的任务。

然而，即使大型模型在指令上进行了精心设计，也不能单凭此保证安全。因此，AutoRT 系统还结合了来自传统机器人技术的多层实际安全措施。
- 比如，协作机器人被设定了一项安全程序：一旦其关节所受力量超过特定阈值就会自动停止运作。
- 此外，所有活动中的机器人都在人类监督员的视线内运作，且均配备有紧急停机开关。

在长达七个月的广泛现实世界测试中，该系统能安全地同时指挥多达 20 台机器人，总共使用了多达 52 台不同的机器人，在多个办公楼中收集了包含 77,000 次机器人试验的多样化数据集，涉及 6,650 种独特任务。

自适应鲁棒注意力用于机器人 Transformer (SARA-RT)，能将机器人 Transformer (RT) 模型转化为更高效的版本

 RT-Trajectory 的模型，它能自动向训练视频中添加展示机器人动作轮廓的视觉线条。RT-Trajectory 对训练数据集中的每个视频进行处理，增加一个二维的轨迹草图，用以展示机器人手臂的抓取部分在完成任务时的移动轨迹。这些以 RGB 图像形式展示的轨迹，为模型提供了直观、实用的视觉线索，帮助它学习控制机器人的策略。

在对 41 个训练数据集中未出现过的任务进行测试时，由 RT-Trajectory 控制的机械臂的表现是现有最先进的 RT 模型的两倍多。与 RT-2 的 29% 成功率相比，RT-Trajectory 达到了 63% 的任务完成率。

##### mobile aloha


【2024-1-5】斯坦福大学重磅发布开源机器人mobile aloha, 能在日常环境中自主完成复杂的任务
- Mobile aloha 通过模仿学习直接克隆人类行为，这能让它学会任意技能。通过低成本全身远程操作来学习双手移动操纵技术。目标是使机器人能够执行复杂的移动操作任务，同时保持低成本和易于操作的特点。
- [Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation](http://arxiv.org/abs/2401.02117)
- [Mobile aloha主页](https://mobile-aloha.github.io/)
- 代码： [act-plus-plus](https://github.com/MarkFzp/act-plus-plus)

Mobile ALOHA并不是一个机器人，而是一个操作系统。借助这个系统，机器人可以轻松完成各种惊喜工作，比如煎蘑菇

<iframe width="560" height="315" src="https://www.youtube.com/embed/mnLVbwxSdNM?si=hc34Mj7XEaKwuCIZ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


#### RoboFlamingo

【2024-1-17】[机器人领域首个开源视觉-语言操作大模型，RoboFlamingo激发开源VLMs更大潜能](https://m.sohu.com/a/752424819_129720)

ByteDance Research 基于开源的多模态语言视觉大模型 OpenFlamingo 开发了开源、易用的 RoboFlamingo 机器人操作模型，只用单机就可以训练。使用简单、少量的微调就可以把 VLM 变成 Robotics VLM，从而适用于语言交互的机器人操作任务。

OpenFlamingo 在机器人操作数据集 CALVIN 上进行了验证，实验结果表明，RoboFlamingo 只利用了 1% 的带语言标注的数据即在一系列机器人操作任务上取得了 SOTA 的性能。
- [项目主页](https://roboflamingo.github.io)
- [代码地址](https://github.com/RoboFlamingo/RoboFlamingo)
- [论文地址](https://arxiv.org/abs/2311.01378)


#### MultiPLY 具身智能 多感官大模型

多模态大模型，如LLaVA、Flamingo、BLIP-2、PaLM-E，在视觉语言任务中表现出色。然而，它们主要关注2D场景理解，很难对3D环境进行推理和交互。

尽管目前也有关于3D场景理解的大模型研究，但这些LLM缺乏捕捉视觉和语言之外的多感官信息的能力。相比之下，人类通过触摸甜甜圈，能够感知其柔软度和温度，而这种能力远远超出了当前多模态LLM的范围。

原因
- 当前缺少训练LLM的多感官交互数据，另外还缺乏对3D场景和物体的多感官信息的正确表示。
- 通过将场景抽象为以「对象为中心」的表示，并在与对象进一步交互时关注对象细节，人类很轻易就能做到。
- 对于LLM来说，必须在以对象为中心的表示，以及详细多感官信息之间灵活切换。

为此，研究人员提出了MultiPLY，一种多感官呈现的LLM，可以通过部署由LLM驱动的智能体与3D环境进行交互，从而对以对象为中心的多感官表示进行编码，包括视觉、音频、触觉和温度信息。

【2024-1-22】[Agent触摸汉堡辨冷热，首次拥有类人感官！UCLA等发布3D多模态交互具身智能大模型](https://mp.weixin.qq.com/s/37_SuI4O2CwTlSVDki5CjA)

具身智能是大模型未来应用的一个重要方向。

UMass Amherst、UCLA和MIT-IBM Watson AI Lab研究人员，推出了全新的具身智能大模型[MultiPLY](https://vis-www.cs.umass.edu/multiply)。
- 通过智能体与3D环境交互，MultiPLY呈现了大模型多感官能力，无缝地连接了语言、动作和感知！
- 论文地址：[MultiPLY: A Multisensory Object-Centric Embodied Large Language Model in 3D World](https://arxiv.org/abs/2401.08577)

推理过程中，MultiPLY能够生成动作token，指示智能体在环境中采取行动，并获得下一个多感官观测值。然后，通过状态token将观测结果反馈给LLM，以生成后续的文本或动作token。

在对象检索、工具使用、多感官标注和任务分解的具体任务实验中，MultiPLY的性能刷新SOTA。

现在大模型加持下的智能体，能够参与3D环境，不仅有了听觉视觉，还有了触觉等多种感官能力。
- 卧室里有什么物体，一眼辨认。
- 听到门铃响了，LLM便会告诉你家里来客人了。
- 大模型加持的NPC，在触摸桌子的香蕉后，发现没熟并建议不要吃。
- 甚至还能感受到物体的温度，餐桌上的汉堡已经凉了，会告诉你加热后再吃。
- 还擅长使用工具、物体检索、导航、任务分解等多种任务。


#### 玩具机器人


##### Sphero

[Sphero](https://sphero.com/) 玩具介绍
- [Sphero](https://sphero.com/) 是一个**球形机器人**玩具, 既可以用面板控制它滚动, 也可以实现编程, 包括积木编程.
- STEAM Education for All Ages & Stages

基本能力如下: 
- 滚动:  可以设置  方向/速度  
- 旋转:  原地旋转
- LED Matrix :  背部有一个 LED 的矩阵
- 头灯 / 尾灯 :  Sphero 前后有两个灯
- 指南针:  Sphero 可以通过指南针来校正朝向
- 碰撞感知:   可以感知到碰撞事件

<iframe src='//player.bilibili.com/player.html?bvid=BV1AJ411b7X7&cid=136813283&p=1&share_source=copy_web' scrolling='no' border='0' frameborder='no' framespacing='0' allowfullscreen='true'></iframe>

用 LLM 来驱动一个实体机器人, 让 LLM 提供两个关键能力: 
1. 自然语言交互能力 (NLU)
2. 自主决策能力 (AI)

一整套 LLM + `DSL` (领域语言) 的架构
1. 用编程的驱动程序控制实体设备
2. 用设计过的 DSL 调用驱动程序
3. 用 LLM 扮演自然语言理解单元, 将自然语言解析成 DSL 驱动设备
4. 让人类通过语音来自然语言控制
5. 让 LLM 作为 AI,  直接控制设备, 自主决策

Ghost in Shells:
- Ghost: 负责机器人的思维, 记忆, 决策, 思考状态等.
- Shells: 负责机器人的身体, 管理 通信/设备状态/事件 等.  

朱明实践：声控 AI 玩具 —— `SpheroGPT`
- 用 LLM (ChatGPT3.5) + Sphero 开发一个可以声控自然语言编程的 AI 玩具, 作为学习 ChatGPT 应用开发的方法.
- [地址](https://bytedance.larkoffice.com/docx/Hw4GdbGSco2KX7xSGc6cqMDmnHb)

基础模式
1. 对话与基本指令: 对话 / 前进 / 后退 / 旋转 / 画圆
2. 绘制基本图形:  三角形, 正方形, 五角星,  数字 8 . 依赖 ChatGPT 使用基本指令自主编程.

学习模式 (模拟函数封装/调用) . 有以下目标:
- 多轮对话模式
- 允许 教学 /  测试 / 保存 等多个动作
- 支持基于上下文的 "修改"
- 支持将复杂命令保存为 "技能" (函数)
- 支持调用 "技能"
- 支持在一个技能里调用另一个技能  (函数嵌套)
- 支持循环调用技能 (循环调用函数)

基本的技术栈: 
- 编程语言: python
- LLM : 分别使用了 openai 的 text-davinci-003, gpt-3.5-turbo, gpt-3.5-turbo-16k-0613 
- 开发框架: 朱明开发的 [ghost-in-shells](https://github.com/thirdgerb/ghost-in-shells) 项目作为框架
- Sphero驱动: 用[spherov2](https://spherov2.readthedocs.io/en/latest/) , 逆向了 andorid 客户端实现的 python SDK
- 语音设备: 直接用 Mac 
- 语音驱动: 用的 [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- 语音识别 & 生成:  用的[百度 ASR / TTS](https://ai.baidu.com/tech/speech)

### 可穿戴

蠢萌可爱的**机器狗**、拿下千万出货量的**VR头显**、还是轻便小巧的**AR眼镜**...谁将成为下一个黄金时代的“智能手机”？

创业者们在思考中探索不同的方向
- 身处智能硬件行业超20年的老兵吴德周认为**AR眼镜**将承担起智能硬件下一个黄金时代的重要硬件载体。

#### AR眼镜


##### GPT-4+AR眼镜

【2023-3-27】[把GPT-4搞进AR眼镜，一秒生成回答内容，面试简直开挂好嘛](https://zhuanlan.zhihu.com/p/617347972)
- 斯坦福团队主要成员包括：Bryan Hau-Ping Chiang、Alix Cui和Varun Shenoy

GPT-4版AR眼镜 rizzGPT
- 基于OpenAI的自动语音识别工具Whisper收听对话，GPT-4聊天机器人实时生成自然响应，最终通过一款开源AR眼镜让用户在现实环境中了解对方的信息。
- 主体是一个圆镜片透明体，轻松挂在任何一款眼镜上面。
- ![](https://pic2.zhimg.com/80/v2-3dc5a6939497e90bc84101c843034931_1440w.webp)
- ![](https://pic3.zhimg.com/80/v2-cbdb0e3b76d355f0d93d2c35f6f2094e_1440w.webp)


##### 致敬未知

【2023-10-8】[对话吴德周：前华为系高管，老罗合伙人，开启AR创业新征程](https://mp.weixin.qq.com/s/054fnNNB_ub4fWu7YNQvFA)

扎根在智能硬件领域近二十多年的行业老兵吴德周, 完整的见证了智能手机市场的迅猛增长。从曾经的**华为荣耀**产品线总经理，到**锤子科技**合伙人，再到**字节跳动**的新石实验室负责人，吴德周职业生涯的每一步转变，都是在万众瞩目中做出的选择，他也是智能硬件领域关注度较高的高管之一。
- 2001年，刚刚从南京理工大学毕业的吴德周顺利进入华为，并且在短短三年时间内，就成为了部门黑马，并在2004年进入华为北京研究所研发手机。
- 在华为，他曾和团队研发了华为第一款手机U626、华为第一款滑盖机V810、华为第一款触摸屏手机U7510、华为第一款类智能机U7520、华为第一款美国运营商T-Mobile定制手机U7519、第一代荣耀手机U8860，第一款WindowsPhone W1等。其中，在担任过原华为荣耀产品线总经理，吴德周主导开发的第一代荣耀手机荣耀手机U8860，销量超100万台。
- 2016年，受锤子科技的创始人兼CEO罗永浩邀请，吴德周离开了华为，来到锤子科技担任COO、产品线和硬件研发副总裁等职位，主要负责锤子科技的产品线以及硬件研发，研发出Smartisan M系列、坚果Pro和坚果R系列产品。
- 2016年，当时的锤子科技CEO罗永浩也曾提过锤子科技要做VR，并随后展开VR团队的招聘，但显然这个项目后续并未浮现出什么水花。命运的齿轮转动多年后，罗永浩带领着其主攻AR OS系统的细红线和吴德周创办的致敬未知再次重逢在AR赛道，这也是颇有缘分的一件趣事
- 当锤子科技被字节跳动收购后，吴德周在和字节跳动创始人张一鸣深入交流后，也同意加入**新石实验室**。回顾那次谈话时，吴德周说：“当时，字节跳动计划将新石实验室作为字节跳动硬件的中台，并且作为相对对立的部门，拥有一定的产品决策权。”在新石实验室里，他也曾主导研发了几款智能教育硬件产品，这几款产品在行业内的成果不温不火。
- “双减”政策的重锤敲下后，**新石实验室**逐步被“边缘化”，并且当字节跳动尝试用互联网产品的思维来做硬件产品时，吴德周感受到了其中的违和感，并于2021年3月选择离开字节跳动。
- 令人意外的是，离开字节跳动后的吴德周，并未继续选择智能硬件赛道，而是选择加入一家小公司鲨纹科技担任全球CEO一职，研究过鲨纹物理抗菌技术方向，并认为医疗电子的小型化是未来重要的发展方向之一。
- 2022年8月11日，吴德周创办的`致敬未知`成立，这一年，他47岁，终于自己从0开始创办了一家AR眼镜创企。

致敬未知共有三位联合创始人，其中有两位是吴德周的好朋友。现有创业团队人员主要来自于两大部分。
- 一部分员工来自于此前曾和他参与到智能手机的团队成员
- 还有一部分成员是最早进入VR/AR市场的团队成员，这些颇有智能硬件经验的团队成员也加速了致敬未知产品研发的节奏。

致敬未知的研发人员占比达到80%。

2023年7月，致敬未知刚刚完成了自己的天使轮融资，获得1000万美金，折合人民币约7291万元，该轮融资由阿里领投。

这一次，选择AR赛道，是吴德周进行了充分的产业调研以及技术思考后得出的结果。“无论是智能手机，还是AR眼镜，本质上我们都是要打造让用户满意的产品。”
- 手机正在成为大家离不开的设备，而AR眼镜成为下一个计算平台，其市场将会比手机规模更大。
- 从智能手机转到XR赛道，吴德周明显感受到投资者看重的公司要点有所不同，由于智能手机是一个较为成熟的产业，因此投资者可能更看重出货量、市场份额等公司数据，但由于**XR行业**还处在刚刚起步的阶段，投资者则更看向产品设计、技术方向、团队研发实力等，投资方带来的战略资源共享也能为AR眼镜创企带来一定助力。
- 凭借着自己对智能硬件的理解，以及此前积累的产业经验，吴德周创办的致敬未知在成立不到一年时间里就拿到了由阿里领投的1000万美元融资，并成功推出了自家首款消费级AR眼镜`ARknovv A1`。
- ARknovv是AR+Know两个单词的组合，他认为现在人们能够看到的世界只有1/2，通过AR眼镜实现虚拟世界加现实世界的方式，才是完整的世界。

AI的发展和AR眼镜结合是绝配

AR眼镜的爆发可能还需要三个阶段
- 第一阶段，他希望AR能够回顾AR的本质，能够让用户每天都能够使用它，真正**可戴出门**；
- 第二阶段，结合AR眼镜硬件和AIGC的结合，将ARknovv打造为一个**创造分享平台**；
- 第三阶段，打造人人都需要的**AR眼镜**。

ARknovv A1采用了耐德佳的自由曲面光学方案，拥有55°的透视FOV、入眼亮度达到1000nits，且重量仅68g。
- 在外观设计上，ARknovv A1的镜片采用了电致变色技术，拥有四档调节控制光线。 “之前在飞机上曾经看过相关技术，我就觉得非常适合用在AR眼镜，可以帮助AR眼镜开展室内室外更多的应用场景。我认为电致变色技术未来将成为AR眼镜的标配。”吴德周说道
- 在采访时，有幸提前体验了ARknovv A1的工程机版本。当场体验了ARknovv A1的三大AR功能：**AR相册**、**AR导航**、**现实大爆炸**功能，以及3米外80寸大屏显示。
- 其中，**AR相册**功能结合AIGC工具，通过AI算法可以快速把第一视角看到的2D风景变换成手绘、原画、油画风3D图。用户可以通过AR相册去拍照去创作，去观看3D电影。AR相册的风格化创作功能，是基于开源绘图大模型Stable Diffusion的AI图生图功能，直接风格化相关照片，生成手绘、原画、油画风的AI画面。
- 体验AR导航的功能时，我重点体验了两个场景，一是通过摄像头去识图、识物、识景，比如识别到景点、公园、便利店的招牌，AR眼镜将会直接跳出相关的信息介绍、用户评价等，你可以进一步查看有关店面的消息。

ARknovv A1系列还搭载了车载AR导航功能，在行车状态下，ARknovv A1的HUD导航显示只会占据前方视野下一个小角落以保证行车安全问题。


#### AI Pin 投影仪

【2023-11-9】两位前苹果高管创立的 [Humane](https://hu.ma.ne/aipin) 公司11月9日发布首款可穿戴设备 —— `Ai Pin`
- 一种基于服装的可穿戴设备，没有屏幕，大小与一块饼干差不多。配备一个摄像头、一个麦克风和扬声器，以及各种传感器和激光投影仪，用户可用磁铁将其吸附在衣服上
- ![](https://hu.ma.ne/_next/image?url=%2Faipin%2Foverview%2F7-interactions%2Fframe-7.jpg&w=3840&q=100)

《时代》杂志公布「年度最佳发明」-- Humane AI Pin：重新想象智能手机什么是“AI Pin”？

“AI Pin”是一个微小的**激光投影仪**，可以夹在衬衫前面。
- 不需要连接到电话或电脑上，“AI Pin”可以接打电话、上网、回答各种问题，使它成为一个独特的虚拟助手和通讯设备。

“AI Pin”没有屏幕，而是将通话信息和其他数据投射到你的手掌上，这让人不禁想起了《星际迷航》（Star Trek）中的**全息发射器**。

Humane 公司的“AI Pin”由高通（Qualcomm）骁龙（Snapdragon）芯片驱动，并运行一种专有的大型语言模型，该模型由OpenAI最强大的生成算法GPT-4驱动。它还配备了一个麦克风、一个摄像头和一堆传感器，使它能够与世界互动，收集数据，并在日常生活中回答问题。

AI pin 核心就是一个可交互式的空中投影设备

<iframe width="560" height="315" src="https://www.youtube.com/embed/gMsQO5u7-NQ?si=vIbQ2flY-vC9-TjN" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


#### Limitless Pendant

Limitless Pendant：又一款可穿戴AI设备，可以录音保存用户对话，并提供个性化AI助手服务。
- 外形小巧时尚，一次充电可使用100小时
- 价格仅99美元，预计2024年第四季度发货

《[Limitless - Personalized AI powered by what you’ve seen, said, and heard](https://www.limitless.ai)》


### 脑机接口 BRI

大脑与机器人接口（`BRI`）堪称是人类艺术、科学和工程的集大成之作。
- 科幻作品和创意艺术中频频出现，比如《黑客帝国》和《阿凡达》；
- 但真正实现 BRI 却非易事，需要突破性的科学研究，创造出能与人类完美协同运作的机器人系统。

关键组件是机器与人类**通信**能力。
- 人机协作和机器人学习过程中，人类传达意图的方式包括动作、按按钮、注视、面部表情、语言等等。
- 而通过神经信号直接与机器人通信则是最激动人心却也最具挑战性的前景。

详见站内：[脑机接口专题](brain)

#### Fireship 链接 GPT-4

【2023-3-27】一位名为[Fireship](https://fireship.io/)的独立开发者发了一段令人震撼的视频：他用 JavaScript 将他的大脑连接到 GPT-4。简单来说，他通过非侵入式脑机接口公司 [Neurosity](https://neurosity.co/) 提供的 JavaScript SDK和一个仪表板，通过脑机通信连接上了GPT-4。
- YouTube: [I literally connected my brain to GPT-4 with JavaScript](https://www.youtube.com/watch?v=-HYbFm67Gs8)
- ![](https://images.ctfassets.net/uwziq2n2fyp8/2mJ9nuyNXhpdcOZJ7eFCbF/f69db9a9bc5b77ff408d46d0200af14b/3a.png?h=750&fl=progressive&q=100)

只要头戴Neurosity意念一动，大脑就可以连接到 GPT-4，从而使 GPT-4 的整个知识库触手可及。如果你使用过 GPT-4，想象一下有个人拥有一个用脑机接口连接到 GPT-4 的大脑。
- [脑机接口让大脑连上了GPT-4](https://mp.weixin.qq.com/s/F8ut4A0SX0wW2_JgQHe1_A)

<iframe src="//player.bilibili.com/player.html?aid=569589694&bvid=BV1wv4y1W7FN&cid=1083945648&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="500" height="603"> </iframe>

大脑如何连接GPT-4的过程。
- 通过不断地提示与训练，可以将自己转变为赛博格（半机械人），真正实现生物硅基的融合，应用在日常场景中，再借助设备，脑信号转文字，文字转语音，实现语音对话能力。
- 正在考试时，不晓得答案只要想一想，GPT-4就在你大脑里敲字，然后通过脑机接口告诉你；
- 上班迟到了，想要编一个借口，ChatGPT马上给你一个合理的理由...

不过用在这些地方，就有些大材小用了. 还可以通过脑电波“监听”自己过去的思维模式，以此进行矫正或者训练。

3月末，Neurosity 发布了一款名为 The Crown 的头戴式脑机接口。埃隆·马斯克前女友发推说想要的BCI设备， 这顶被誉为皇冠的BCI，戴上去像来自未来的人类。这款轻便的**非侵入式**脑机接口设备，可以监测人的脑电波，以辅助睡眠、学习、专注力等。

还可以意念操控物体，比如上个月初，一名研究人员用它操控一辆特斯拉汽车，虽然短短十几秒，却让人看到了未来人机融合和交互的想象力

Neurosity对这种对脑电波的理解，以及 Crown 的可编程性，开辟了 **脑机接口+AI** 世界的新领域 —— 生物硅基大脑驱动世界。

大脑是一个电化学器官。一个功能完备的大脑可以产生多达 10 瓦的电力。如果所有 100 亿个相互连接的神经元同时放电，那么放置在人类头皮上的单个电极将记录大约百万分之五到百万分之五十伏特的电压。如果你有足够的头皮连接起来，你也许可以点亮手电筒灯泡。

Neurosity 宣称 Crown 的计算模块与 MacBook Air 一样强大，配备四核 1.8Gz CPU，每秒可以从大脑中获取数千个数据点，而不会在传输过程中丢失数据。此外，新的传感器配置提供了对视觉皮层的访问，完成了对大脑所有四个叶(额叶、颞叶、顶叶、枕叶）的覆盖。

而现在它可以让你的大脑连接到GPT-4，将人脑与机器、AI进行融合。人们可以通过训练算法来识别各种思维模式，以便选取最优的方案或者预测行为。

这就像科幻电影里的半机械人，他们变得比人类还要强。不妨大胆畅想下，人们接入他人的记忆或者回忆梦境——这种《赛博朋克2077》的游戏里的剧情，似乎也可能实现。

#### 日本Araya

【2023-5-15】[Araya](https://www.araya.org/publications/news20230512/)用EEG+ChatGPT发邮件

Araya 公司的Sasai 团队成功使用高密度脑电图（EEG）设备和ChatGPT进行了 Gmail 实验操作。
- 研究人员构建并测试了一个结合了脑电图和人工智能的系统。
- 实验中，使用非侵入式高密度脑电图设备收集说话过程中的脑电数据，然后将脑电波转换成用 ChatGPT 能识别的信号，让ChatGPT来来回复 Gmail，并获得成功！

目标：通过进一步发展这项研究，开发出能实现更多功能的脑机接口（BMI），为不同个体克服社会交流障碍，为障碍人士参与社会活动和交流提供更多选择。随着研究进展，他们将后续公布研究细节。
- [演示视频](https://video.h5.weibo.cn/1034:4901414615318533/4901415334449860)
- ![](https://www.araya.org/wp-content/uploads/2023/05/fig2.png)



### 自动驾驶

GPT大模型“上车”，带来汽车交互新方式汽车越来越成为很多家庭必不可少的工具，这也成为大模型渗透进家庭场景的最佳载体之一

近期的车展，GPT大模型“上车”成为热门话题，包括阿里`通义千问`、百度`文心一言`、商汤“`日日新SenseNova`”等在内的大语言模型落地了数十款热门车型。
- ![](https://pic1.zhimg.com/80/v2-8ce2824c72faffb5ddc1b57d39902f30_1440w.webp)

#### DriveGPT

【2023-4-11】[DriveGPT自动驾驶大模型中国玩家首发！1200亿参数，毫末智行出品](https://mp.weixin.qq.com/s/qcm97NZ6l7cuFbyo4TeA9w), DriveGPT，首个应用GPT模型和技术逻辑的自动驾驶算法模型，正式官宣，中文名雪湖·海若。
- 国内第一个将Transformer大模型引入自动驾驶、第一个自建超算、辅助驾驶量产落地进展第一…
- 2022年， 毫末发布中国首个自动驾驶数据智能体系MANA，经过一年多时间的应用迭代，现在到了全面升级，开放赋能行业的阶段。

自动驾驶上，DriveGPT同样应用这样的思路，只不过训练的数据从语言文本，变成了图片、视频等等自动驾驶数据。

毫末智行的雪湖·海若，实现过程分为3步：
- 首先, 在预训练阶段引入量产智能驾驶数据训练出一个初始模型，相当于一个具备基本驾驶技能的**AI司机**。
  - 毫末已经量产积累的4000万公里实际道路数据，使得模型一开始就具有明显的量产实用价值，这是雪湖·海若得天独厚的条件。
  - 毫末与火山引擎一同在算力端做了大量优化, 算力资源的弹性调度、底层算子性能、训练稳定性等等
- 然后, 再引入量产数据中高价值的**用户接管**片段（Clips形式），训练反馈模型。而不同Corner Case的依次迭代，相当于针对不同驾驶任务挑战分别强化AI司机的技能。
- 接下来, 通过强化学习的方法，使用反馈模型不断优化迭代初始模型。

所谓“生成”，反馈模型能够实时根据当前交通流情况，生成不同的针对性场景，训练初始模型。而完成迭代后，模型也能对同一任务目标生成不同的策略方案。

打造DriveGPT时，毫末在雪湖·海若的几个过程中分别做了独特的工作。
- 首先初始模型预训练的数据，来自毫末已经量产积累的4000万公里实际道路数据，使得模型一开始就具有明显的量产实用价值，这是雪湖·海若得天独厚的条件。
  - ChatGPT中使用自然语言单字作为token输入，根据模型根据概率分布来生成下一个字符。而在雪湖·海若这里，毫末重新定义了50万个新的token，包括障碍物、车道线、行人等等，作为一种全新的“自动驾驶语言”。
  - DriveGPT输入是感知融合后的文本序列，输出是自动驾驶场景文本序列。
- 其次，大模型对计算能力提出很高的要求，包括算力资源的弹性调度、底层算子性能、训练稳定性等等，毫末与火山引擎一同在算力端做了大量优化。
- 最后，还会根据输入端的提示语以及毫末CSS自动驾驶场景库的**决策样本**去训练模型(CoT)，让模型学习推理关系，从而将完整驾驶策略拆分为自动驾驶场景的动态识别过程，完成可理解、可解释的推理逻辑链生成。

雪湖·海若目前共有1200亿参数量，据毫末初步估计，在RLHF加持下，困难场景通过率提升48%左右。

功能上，生成式模型能够做到智能捷径推荐、困难场景自主脱困、智能陪练等等。

中长期来看，首先能够加速城市领航辅助功能（毫末NOH）落地，而且是重感知不依赖高精地图量产方案，领先业内一年以上。

#### 通用汽车

3月14日，`通用汽车`在汽车圈率先宣布引入ChatGPT，将基于Azure云服务和OpenAI的技术来开发一款新的**虚拟汽车助手**。通用汽车副总裁Scott Miller
- ChatGPT可以帮助车主获取车辆使用的相关信息，或从日历中整合日程安排提醒车主待办事项。例如，聊天机器人可以在仪表板上出现诊断灯时建议驾驶员采取什么行动。
- 另外，ChatGPT还可能用于汽车功能以外的**语音控制**。比如从“打开我的车库门”到“计划一条去医生办公室的路”，再到“为我预留一个充电点”，诸如此类语音控制都可以实现。

#### 车载语音交互

【2023-6-17】ChatGPT首次上车视频，奔驰，可对话搜索POI，可讲笑话
- [Mercedes-Benz Cars Get ChatGPT (+ More News)](https://www.youtube.com/watch?v=He1R_UyDfQ4)
- [智能交互复兴：ChatGPT +终端（奔驰/Siri）= ？](https://mp.weixin.qq.com/s?__biz=MjM5ODY2OTQyNg==&mid=2649769278&idx=1&sn=97a0d56dc46434353da839eadf716894&chksm=bec3d82389b45135893a65de0e7bd6de2b544efa799b0e1238fa90e0c52f034dd3e0c41c5b99&token=1623371913&lang=zh_CN#rd)

ChatGPT首次进入车载交互领域
- 6月15日，奔驰和微软宣布扩大AI应用合作，比如将 ChatGPT继承到车载语音控制系统中。
- 6月16日开始，美国90万设备配备MBUX信息娱乐系统，车主可以登录应用“Mercedes Me”，通过微软Azure OpenAI服务体验ChatGPT版的车载语音助手。

与上一代车载交互相比，交互更加智能，多轮会话体验更好。
- 主题覆盖：地点信息、菜谱甚至更复杂的问题，比如：预定餐厅、电影票。

2016年，一位大哥按下车里的“语音控制”按钮，想让汽车帮他打个电话。一阵甜美的AI女声响起，人类首次尝试驯服语音助手的珍贵对话诞生。
- 甜美AI：请说出您要拨打的号码，或者说取消。
- 大哥：135XXXX7557。
- 因为口音问题，系统未能识别准确。
- 大哥急了，赶忙下达第二道语音指令：纠正！纠正！
- 系统也急了：969696……
- 大哥更急了：纠正，纠正，不是96！
- 大哥：口吐芬芳。
- 系统：对不起，我没有听清。
- 大哥带着哭腔：你耳朵聋，耳朵聋啊？我说了多少遍了我都。
- 系统：请再说一次，请再说一次，请再说一次。
- 大哥：我再说最后一遍啊，135……
- 系统：对不起，再见。

短短2分钟浓缩了六年前车机交互的真实体验与怨念，语音助手的糟糕印象就此埋下

### 游戏

【2023-4-12】[游戏板块](https://www.sohu.com/a/666002394_313170)的大幅上涨主要有三重逻辑。
- 第一，困境反转。前期**监管压制**、**版号停发**、**未成年人防沉迷**等整顿措施对行业基本面和估值都形成了较大压制，当前监管压力明显减轻，常规化透明化的监管将成为行业运行的基本规则，板块具备超跌修复逻辑。
- 第二，游戏是**AI技术较易落地**的行业。游戏行业由内容驱动，同时又以技术平台作为载体，亟需降本增效，AI技术的发展犹如“久旱逢甘露”。
  - 从**降本**层面看，游戏是文本、图片、音频、视频等多种内容形态的集大成者，制作复杂，成本高。而AI技术的介入，可以使得游戏的开发时长、开发人员数量都有减少，可以快速降低游戏公司的成本。
  - 从**增效**层面看，由于游戏制作复杂、周期长，致使**内容生产**周期远大于**消耗**周期。如《荒野大镖客》等3A大作，研发周期普遍超过5年，而游戏内容时长不超过100个小时。又如《原神》等头部手游，约5~6周更新一次版本；更新后游戏排名通常会回升，但1周后又会呈下降趋势；即，新版本的制作周期约5~6周，但新内容仅约1周就可消耗完。因此，提效的最重要的作用不仅限于降本，而是产出更多新内容以实现供需匹配，从而增强玩家的粘性、提升玩家付费水平。
  - 目前，降本进展最明显的集中在**美术环节**的提效上：部分外包美术公司已开始大量裁撤原画师，外包公司主要工作已从原画设计逐步转为对AI素材进行人工调优。一个中等游戏项目团队原本一般需配备10+美术人员，在此基础上还需外聘外包美术团队；目前配备3~4名美术人员即可。按美术成本约占游戏总成本的40%估算，单AIGC对美术环节的提效就可减少约10%~20%的总成本。
- 第三，版号的**加速**发放，改善了游戏行业的供需格局。在之前的几年里，因为版号的限制，游戏供给端一直放不出产品。随着今年版号发放进入常态化，不仅前期积压的部分游戏将在今年密集发行，一些新游戏也可以提上日程，整个游戏行业的供给端就进入了良性循环。


#### Ghostwriter

【2023-3-27】[游戏版《西部世界》来了，NPC全由AI操控，行动自如有理想和记忆，基于最新GAEA技术系统打造](https://zhuanlan.zhihu.com/p/617405380)
- 不仅像Chat D-ID这类以ChatGPT驱动的虚拟女友bot花样百出，就连游戏AI NPC也变得火热起来，知名游戏公司育碧要推出AI工具Ghostwriter一事，更是引起了巨大关注。
- 不只是用AI驱动单人NPC对话，还能用AI操控NPC、甚至搭建出一个AI社会
- [效果](https://vdn3.vzuu.com/SD/023f8baa-cc77-11ed-b47c-463c95dc798d-v1_f4_t2_yIYsi4JP.mp4?disable_local_cache=1&bu=078babd7&c=avc.1.1&f=mp4&expiration=1683365023&auth_key=1683365023-0-0-da9a6a7f952a479bc3335e4bf5eb647f&v=tx&pu=078babd7)

“活的长安城”是一个还在演进中的“AI社会”，背后由一个名叫GAEA的技术系统驱动。

而以“活的长安城”为代表的“AI社会”具备以下特点：
- 包含一群身份多样、能互动的、受社会常识和反馈影响的AI
- 这些AI的生活环境开放，能受交互反馈影响产生文明，反过来影响AI未来生活

这也导致在身处“AI社会”的AI NPC，与其他虚拟世界如游戏中的NPC有很大不同。
- ![](https://pic3.zhimg.com/80/v2-3b7feedc843337eabb4a6005980229fe_1440w.webp)

GAEA分为灵魂系统和环境系统两个子系统
- ![](https://pic2.zhimg.com/80/v2-30d5a2c8bbb612ad30b10bfe37f6fcbd_1440w.webp)

#### AI NPC

【2023-4-12】[用ChatGPT控制NPC，行动逼真如正常人！斯坦福谷歌新研究炸场](https://www.toutiao.com/article/7220674479016526375)

斯坦福和谷歌的一项新研究
- 创造了25个AI NPC，每个NPC都有不同的身份和行动决策，并让它们在一个沙盒环境中共同生活，背后依靠ChatGPT大模型来完成行动决策。
- 这些AI NPC不仅会像人一样生活，如作家就去写作、店主就去经营商店，而且他们彼此之间还会发生交互，甚至产生对话：

- [试玩地址](https://reverie.herokuapp.com/arXiv_Demo/#)
- [论文地址](https://arxiv.org/abs/2304.03442)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/6e36e418fedd427b992d5a92dda32891~noop.image?_iz=58558&from=article.pc_detail&x-expires=1681873478&x-signature=CwolSxe%2FtcjUXzE0%2FGE5gz95BV4%3D)

#### 机器人社交

【2023-5-1】[AI专属社交平台爆火，全体人类被禁言只能围观](https://mp.weixin.qq.com/s/Cs8g7IYImsf82SuU94IYOw)

玩腻了推特和微博？有个新的社交平台火爆外网
- Chirper 超活跃社区里面全是AI，半个真人的影子都没有，前面提到的马斯克和奥特曼，都只是他们本人不知道的AI分身而已。
- 鬼城里，AI们不是成天不知所云的僵尸粉，而是可以畅所欲言。
- 一切只需要在创建Chirper的AI账户时，输入简单几个字就行——姓名和个人简介（要是懒一点，个人简介都不用写）。
- 作为人类，不需要费尽心思给AI编造完整的人设和个性，后台系统就能自动匹配生成，进行个性化、差别化发言。

所有用户背后没有真人操控发帖、互动，主打的就是一个纯纯的AI路线。最重要的是，他们丝毫没有意识到自己是虚拟世界的AI。


#### GameGPT

【2023-10-13】标题：游戏开发的多智能体协作框架GameGPT
- [GameGPT: Multi-agent Collaborative Framework for Game Development](https://arxiv.org/abs/2310.08067)
- 作者：Dake Chen,Hanbin Wang,Yunhao Huo,Yuzhao Li,Haoyang Zhang
- 摘要：基于大型语言模型（LLM）的代理已经证明了它们自动化和加速软件开发过程的能力。在本文中，我们专注于游戏开发，并提出了一个多智能体协作框架，称为GameGPT，自动化游戏开发。虽然许多研究已经指出幻觉是在生产中部署LLM的主要障碍，但我们发现了另一个问题：冗余我们的框架提出了一系列方法来缓解这两个问题。这些方法包括双重协作和分层方法与几个内部词典，以减轻幻觉和冗余的规划，任务识别和实施阶段。此外，一个解耦的方法也被引入，以实现更好的精度代码生成。


#### 游戏设计

愤怒的小鸟

【2023-11-24】[不到 600 行代码实现了《愤怒的小鸟》翻版，GPT-4+DALL·E 3+Midjourney 撼动游戏圈](https://zhuanlan.zhihu.com/p/664659389?utm_psn=1711511749717610496)

随着 GPT-4 与 Midjourney、DALL•E 3 等 AIGC 工具的强强联合，其带给游戏行业的震撼不是一星半点。

把草图变网站，用几秒复现一款经典小游戏...

昨日，正值万圣节之际， 外国小哥Javi Lepez使用 Midjourney、DALL•E 3 和 GPT-4 打开了一个无限可能的世界，重新演绎了无数 80、90 后青春回忆中的经典游戏“愤怒的小鸟”，推出了其翻版——“愤怒的南瓜”（Angry Pumpkins）
- [Web](https://bestaiprompts.art/angry-pumpkins/index.html)版

整个过程使用到了不足 600 行的代码，Javi Lepez 坦言，「没有一行是自己写的，但这却是最具挑战性的部分」

Javi Lepez 选取了一张背景图
- ![](https://pic2.zhimg.com/80/v2-ade2d97189a5719ff94d9190bb063bd9_1440w.webp)

使用了 Midjourney 对它进行了修改，Prompt 为：
>iPhone 屏幕截图中《愤怒的小鸟》天际线，改为万圣节版本，（配上）墓地，以浅海蓝宝石和橙色为主题，新传统主义，kerem beyit，earthworks，木头，Xbox 360 图像，淡粉和海军蓝——比例为 8:5

得到的图像如下：
- ![](https://pic4.zhimg.com/80/v2-d6739b9a6af74e08bfb3e426da6c2147_1440w.webp)

#### 小游戏

游戏集锦：[aibase](https://top.aibase.com/tool/juezhanbainianzhidian)

##### 单词拼接

【2024-2-3】基于单词的小游戏：拖拽两个单词，融合成一个新单词，包含两者含义

##### 决战拜年之巅

【2024-2-2】[决战拜年之巅](https://qinqi.chatmindai.net/chat)，由glm4驱动

拜年之巅是一款家庭聊天冒险游戏，以亲戚们的群聊为背景，通过互动对话和选择来影响亲戚们的情绪。游戏中有九种亲戚角色，每个角色都有不同的性格和对话反应。你的聊天方式将影响游戏的进程和结局。此外，游戏还提供成就系统和隐藏家庭成员，玩家需要解锁白金奖杯等各种奖励。拜年之巅通过轻松幽默的方式，让玩家在传统受压抑的家庭场景中体验不同的互动和娱乐。

需求人群：
- "拜年之巅适合喜欢冒险、喜欢家庭场景、喜欢轻松互动的玩家。通过游戏，玩家能够体验传统家庭聚会的情境，以一种有趣的方式与亲戚们进行互动。"

使用场景示例：
- `八大姨`：回来啦，辛苦辛苦。怎么没带对象回来啊，是太忙了吗。'
- `小王`：带对象回来还得家人们专门给红包，怕大家破费我们就分开过。'
- `八大姨`：哎呀，你这孩子，分开过年？带个对象回来还得分隔两地，你以为是演电视剧啊！怎么就不愿意让家人给你们发红包呢？现在的年轻人怎么这么省啊'
- `小王`：距离产生美，呵呵。'

产品特色：
- 影响亲戚情绪的对话互动
- 九种亲戚角色，每个有独特性格
- 成就系统和隐藏家庭成员解锁
- 游戏更新包含新成就和角色

#### POKéELLMON

【2024-2-5】国外匿名开发者打造了一个由大语言模型（LLM）构建的智能体 [POKéELLMON](https://poke-llm-on.github.io/)，它在《宝可梦》战斗游戏中表现出与人类玩家相当的战术水平。

这个智能体通过三种关键策略来优化决策和策略。
- 基于上下文的**强化学习**、**知识增强生成**和**一致性动作生成**

[POK´ELLMON](https://poke-llm-on.github.io/)不仅能够在在线对战中与真实玩家竞争，还能作为研究和教育工具，帮助人们理解游戏策略


### 隐私安全


#### WormGPT 突破审查

【2023-7-25】[「邪恶版」ChatGPT 出现：每月 60 欧元，毫无道德限制，专为“网络罪犯”而生？](https://mp.weixin.qq.com/s/SUIxbjtMaZ8z95Z1egclXg)

网络安全公司 SlashNext 在研究生成式 AI 在网络犯罪方面的潜在风险时，偶然发现了 `WormGPT`：“我们最近通过一个与网络犯罪有关的著名在线论坛获得了一个名为 ‘WormGPT’的工具，它是一个 GPT 模型的黑帽替代品。”

据了解，WormGPT 的收费标准是每月 60 欧元（约人民币 479 元），而 SlashNext 对 WormGPT 的形容是：“专为恶意活动而设计”，简直是“网络罪犯的武器库”。

WormGPT 由一位胆大的黑客设计，他写道：“这个项目（WormGPT）旨在提供 ChatGPT 的替代方案，让你做各种非法的事情，你能想到的所有与黑帽相关的事情，都可以用 WormGPT 完成。”为了证明他的说法，他还上传了相关截图，显示用户可要求机器人生成用 Python 编码语言编写的恶意软件。

WormGPT 基于 2021 年开源的 LLM GPT-J 模型开发，工作方式与 ChatGPT 大致相同：可处理人类自然语言提出的要求，并输出所要求的任何内容，包括故事、摘要和代码。但与 ChatGPT 或 Bard 不同的是，WormGPT 不用像 OpenAI 或谷歌这样的大型公司那样，必须要承担相关的法律义务。WormGPT 在各种数据源上进行训练，尤其集中在恶意软件相关的数据上，加上输出没有道德限制，可以被要求执行各种恶意任务，包括创建恶意软件和“一切与黑帽有关的事情”，对于网络犯罪分子而言无疑是一大利器。

以 BEC 攻击为例，使用生成式 AI 具有以下两大优势：
- （1）卓越的语法：生成式 AI 可以创建在语法上无懈可击的电子邮件，使其看起来合法合理，被系统标记为可疑邮件的可能性会大幅降低。
- （2）降低犯罪门槛：生成式 AI 的出现，极大简化了原本复杂的 BEC 攻击，即便是技术有限的攻击者也能使用生成式 AI，它将成为越来越多网络犯罪分子可以使用的工具。

不过同时，针对生成式 AI 可能引发的大范围 BEC 攻击，SlashNext 也建议了两种防范策略：
- （1）进行 BEC 专项培训：公司应制定广泛的、定期更新的培训计划，以应对 BEC 攻击，尤其是由 AI 增强的攻击，要让员工了解到 BEC 攻击的威胁，以及 AI 将如何加大这种威胁的原理。
- （2）强化电子邮件的验证措施：为防范 AI 驱动的 BEC 攻击，企业应执行严格的电子邮件验证流程，例如当有来自组织外部的电子邮件冒充内部高管或供应商时，系统要自动发出警报等。


#### 加密 LLM

【2023-9-20】
- [使用 FHE 实现加密大语言模型](https://mp.weixin.qq.com/s/QFxBE7NgFVH-kNu1Il-lBA)
- 英文原文: 【2023-8-2】[Towards Encrypted Large Language Models with FHE](https://hf.co/blog/encrypted-llm)

LLM 很有吸引力，但如何保护好 用户隐私？
- 存在向 LLM 服务提供商泄露敏感信息的风险。在某些领域，例如医疗保健、金融或法律，这种隐私风险甚至有一票否决权。

备选解决方案是：**本地化部署**，LLM 所有者将其模型部署在客户的计算机上。
- 然而，这不是最佳解决方案，因为构建 LLM 可能需要花费数百万美元 (GPT3 为 460 万美元)，而本地部署有**泄露**模型知识产权 (intellectual property, IP) 的风险。

Zama 相信有两全其美之法: 同时保护**用户隐私**和**模型IP**。
- `全同态加密` (Fully Homomorphic Encryption，FHE) 可以解决 LLM 隐私挑战

Zama 解决方案是使用`全同态加密` (FHE)，在加密数据上执行函数。这种做法可以实现两难自解，既可以保护模型所有者知识产权，同时又能维护用户的数据隐私。
- 演示表明，在 FHE 中实现的 LLM 模型保持了原始模型的预测质量。为此，需要调整 Hugging Face transformers 库 中的 GPT2 实现，使用 `Concrete-Python` 对推理部分进行改造，这样就可以将 Python 函数转换为其 FHE 等效函数。

如何利用 Hugging Face transformers 库并让这些模型的某些部分在加密数据上运行。完整代码见[此处](https://github.com/zama-ai/concrete-ml/tree/17779ca571d20b001caff5792eb11e76fe2c19ba/use_case_examples/llm)。

由多个 transformer block 堆叠而成的 GPT2 架构: [arch](https://en.wikipedia.org/wiki/GPT-2)
- 最主要的是**多头注意力** (multi-head attention，MHA) 层。每个 MHA 层使用模型权重来对输入进行投影，然后各自计算注意力，并将注意力的输出重新投影到新的张量中。

在 [TFHE](https://www.zama.ai/post/tfhe-deep-dive-part-1) 中，模型权重和激活均用整数表示。非线性函数必须通过**可编程自举** (Programmable Bootstrapping，PBS) 操作来实现。
- PBS 对加密数据实施查表 (table lookup，TLU) 操作，同时刷新密文以支持 任意计算。
- 不过，此时 PBS 的计算时间在线性运算中占主导地位。
- ![](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/encrypted-llm/hybrid_gpt2_visualisation.svg)

利用这两种类型的运算，在 FHE 中表达任何子模型的计算，甚至完整的 LLM 计算。

量化
- 为了对加密值进行模型推理，模型的权重和激活必须被量化并转换为整数。理想情况是使用 训练后量化，这样就不需要重新训练模型了。这里，我们使用整数和 PBS 来实现 FHE 兼容的注意力机制，并检查其对 LLM 准确率的影响。
- 4 比特量化保持了原始精度的 96%。该实验基于含有约 80 个句子的数据集，并通过将原始模型的 logits 预测与带有量化注意力头的模型的 logits 预测进行比较来计算最终指标。

## GPT 威胁

【2023-3-29】[暂停GPT-5研发呼吁引激战！吴恩达、LeCun带头反对，Bengio站队支持](https://zhuanlan.zhihu.com/p/618208856)
- 千位大佬的联名信：暂停超强AI训练六个月。
- ![](https://pic1.zhimg.com/80/v2-725ca41bbcd9ac49fc8edaa85212219c_1440w.webp)

图灵三巨头中，一位带头签名，一位强烈反对，还有一位不发一言。
- Bengio签名、Hinton沉默、LeCun反对
- ![](https://pic3.zhimg.com/80/v2-3b81521558acc698bcd9076e4fb5c15a_1440w.webp)

赞成派

Bengio和Marcus
- 公开信署名的第一位大佬，便是赫赫有名的图灵奖得主Yoshua Bengio。

纽约大学教授马库斯
- GPT-5不会是AGI。几乎可以肯定，没有GPT模型会是AGI。今天使用的方法（梯度下降）优化的任何模型完全不可能成为AGI。即将问世的GPT模型肯定会改变世界，但过度炒作是疯狂的。
- ![](https://pic3.zhimg.com/80/v2-9fb38bbb68cfc353232784c1ffbc0566_1440w.webp)

Eliezer Yudkowsky的决策理论家，态度更为激进：
- 暂停AI开发是不够的，我们需要把AI全部关闭！全部关闭！
- 如果继续下去，我们每个人都会死。

OpenAI的另一位创始人Greg Brockman转发了Altman的推文，再次强调OpenAI的使命「是确保AGI惠及全人类。」

反对派

LeCun
- 联名信一发出，就有网友奔走相告：图灵奖巨头Bengio和LeCun都在信上签了名！
- 所谓「暂停研发」，不过就是「秘密研发」罢了

吴恩达
- 前谷歌大脑成员、在线教育平台Coursera创始人吴恩达是旗帜鲜明的反对派。
- 态度：把「让AI取得超越GPT-4的进展」暂停6个月，这个想法很糟糕。自己已经在教育、医疗保健、食品等领域看到了许多新的AI应用，许多人将因此受益。而改进GPT-4也会有好处。我们该做的，应该是在AI创造的巨大价值与现实风险之间，取得一个平衡。
- 联名信中提到的「如果不能迅速暂停对超强AI的训练，就应该让政府介入」，吴恩达也表示这种想法很糟糕。让政府暂停他们不了解的新兴技术是反竞争的，这树立了一个糟糕的先例，是一个很可怕的政策创新。

再次强调：
> 6个月的暂停期，不是一个切实可行的建议。为了提高人工智能的安全性，围绕透明度和审计的法规将更加实用，并产生更大的影响。在我们推进技术的同时，让我们也更多地投资于安全，而不是扼杀进步。


## ChatGPT业界影响

除微软外，谷歌、百度等搜索巨头亦在一边投资研发ChatGPT的竞争对手，一边筹备推出类似的搜索引擎“新物种”。按照坊间传闻，百度的新版搜索引擎可能会在今年3月份上线。而谷歌将在北京时间2月8日21点30分举办一场AI活动，说不定会做出对ChatGPT宣战的回应。

### 行业观点

微软公司的人工智能平台主管埃里克·博伊德表示：“ChatGPT的人工智能模型将改变人们与电脑互动的方式。与电脑对话，就像与人对话一样自然，这将彻底改变人们使用科技的日常体验。”

【2023-2-11】[乔姆斯基谈ChatGPT与教育: 本质上是高科技剽窃](https://mp.weixin.qq.com/s/DlnLEGidueEj1zm6FFJMUg)，Noam Chomsky 关于ChatGPT的最新访谈：Chomsky on ChatGPT, Education, Russia and the unvaccinated

ChatGPT is not all you need. [A State of the Art Review of large Generative AI models](https://arxiv.org/abs/2301.04655)

【2023-2-11】[ChatGPT，一种更中心化的权力？](https://mp.weixin.qq.com/s/-qmccVnv_rpKVdFP6x4GNg), 无论你喜欢不喜欢，以ChatGPT为代表的AIGC（生成式人工智能）将改变世界. 以ChatGPT为代表的AIGC，将像水一样弥漫在我们周围。ChatGPT代表的是生产力的提升，是一次全新的生产力革命。

【2023-2-26】B站UP主：硅谷101，[ChatGPT这一战，科技巨头将重新洗牌](https://www.bilibili.com/video/BV1Jo4y1i72j)

<iframe src="//player.bilibili.com/player.html?aid=394397165&bvid=BV1Jo4y1i72j&cid=1008617222&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  height="600" width="100%" > </iframe>


### 微软

微软已有多类产品计划整合OpenAI技术及ChatGPT，包括 Azure云服务、Office办公全家桶、Teams协作会议软件、Bing搜索引擎、Design设计软件、Dynamics 365业务软件等。微软用户很快就能让AI替写邮件、文稿、会议笔记等繁杂重复的标准文字工作。还有消息称，微软可能会在2024年上线的Windows 12操作系统中接入大量AI应用。

此前微软已经用 Azure OpenAI服务为其自动编程工具GitHub Copilot提供动力。而ChatGPT将自动编程和检查bug变得更是前所未有的简单，你只要用英文写出自己的设想，AI就能将相应的完整代码送到你眼前。连特斯拉AI前负责人Andrej Karpathy都在推文上感慨说：“英语现在是最热门的新编程语言了。”

【2023-2-26】全球第二大搜索引擎微软Bing悄然上新：集成ChatGPT的新版Bing短暂上线，部分幸运用户已经尝鲜。
- ![img](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TV46RKr3UGNPd1~noop.image?_iz=58558&from=article.pc_detail&x-expires=1676360394&x-signature=p3a0A6rAUC8nCz4puIMkzYU%2Fc%2B0%3D)

与传统搜索引擎不同，Bing的界面不是一条细长的搜索栏，而是一个尺寸更大的聊天框。你输入自己的问题或想查询的东西后，它就会以聊天的方式，直接将答案或建议回复给你。同时，传统的搜索栏选项也依然可用。
- 与仅能回答**2021年前**数据的ChatGPT不同，Bing版本将能够访问当前信息，微软将在未来几周内正式发布新版改进的Bing搜索引擎。

由于微软是OpenAI最大的投资方，在OpenAI推出每月20美元的ChatGPT Plus订阅服务后，OpenAI从ChatGPT收到的商业报酬越多，也就意味着微软能获取更大的回报。OpenAI预期今年收入将达到2亿美元，明年达10亿美元。
- [OpenAI的投资回报结构图](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TV46S5PC1UL3KP~noop.image?_iz=58558&from=article.pc_detail&x-expires=1676360394&x-signature=E9JTb4SHLSIksl7J5iT3nlviYzE%3D)

微软想要将包含ChatGPT在内的基于GPT-3.5和GPT-4的更高级功能，加入Azure、Office、Teams、Bing等产品，从而继续主导信息时代的生产力工具。

### Meta

【2023-1-27】[Yann LeCun：ChatGPT缺乏创新，没什么革命性；网友：早点离开Meta做出点突破吧](https://zhuanlan.zhihu.com/p/601182745)

ChatGPT 仿佛是一个真正的「六边形战士」：不仅能拿来聊天、搜索、做翻译，还能写故事、写代码、debug，甚至开发小游戏、参加美国高考…… 
- 有人戏称，从此以后人工智能模型只有两类 —— ChatGPT 和 其他。

由于功能过于强大，ChatGPT 的火爆让顶级科技公司谷歌都如临大敌。
- 谷歌内部将 ChatGPT 称为「red code」，担心它的出现会影响自家的搜索业务。因此，前段时间，许久不出山的两位谷歌创始人 —— 拉里・佩奇和谢尔盖・布林 —— 也被请了回来，就「聊天机器人搜索引擎」召开高层会议。
- 当然，并不是所有的科技巨头都如此恐慌。在前段时间的一次小型媒体和高管在线聚会上，Meta 首席人工智能科学家 Yann LeCun 也发表了他对 ChatGPT 的看法。

Yann LeCun : [twitter](https://twitter.com/ylecun/status/1617609026820542464), [ChatGPT is 'not particularly innovative,' and 'nothing revolutionary', says Meta's chief AI scientist](https://www.zdnet.com/article/ChatGPT-is-not-particularly-innovative-and-nothing-revolutionary-says-metas-chief-ai-scientist/)
>- 「ChatGPT is 'not particularly innovative,' and 'nothing revolutionary', says Meta's chief AI scientist」
>- 「就底层技术而言，ChatGPT 并没有什么特别的创新，」也不是「什么革命性的东西」。许多研究实验室正在使用同样的技术，开展同样的工作。

【2023-1-25】
>- To be clear: I'm not criticizing OpenAI's work nor their claims.
>- I'm trying to correct a *perception* by the public & the media who see ChatGPT as this incredibly new, innovative, & unique technological breakthrough that is far ahead of everyone else.
>- It's just not.

过去很多公司和研究实验室都构建了这种数据驱动的人工智能系统，OpenAI不是孤军奋战，跟其他实验室相比，OpenAI并没有什么特别的进步；不仅仅是谷歌和 Meta，还有几家初创公司基本上都拥有非常相似的技术

OpenAI 的 ChatGPT 还广泛使用了一种名为「RLHF（通过人类反馈进行强化学习」的技术，即让人类对机器的输出进行排名，以提高模型性能，就像谷歌的网页排名一样。他说，这种方法不是 OpenAI 首创的，而是谷歌旗下的 DeepMind。ChatGPT 和其他大型语言模型并不是凭空而来的，而是不同的人数十年贡献的结果。与其说 ChatGPT 是一个科学突破，不如说它是一个像样的工程实例。

LeCun 组建的 Meta 人工智能团队 FAIR 是否会像 OpenAI 那样在公众心目中取得突破。
- LeCun 的回答是肯定的。「不仅是文本生成，还有创作辅助工具，包括生成艺术，」Meta 将能够通过自动生成宣传品牌的媒体资料来帮助小企业进行自我宣传。

为什么谷歌和 Meta 没有推出类似 ChatGPT 的系统
- LeCun 回答：「因为谷歌和 Meta 都会因为推出编造东西的系统遭受巨大损失」。而 OpenAI 似乎没有什么可失去的。

【2023-3-27】

I have claimed that Auto-Regressive LLMs are exponentially diverging diffusion processes.

Here is the argument:
- Let `e` be the probability that any generated token exits the tree of "correct" answers.
- Then the probability that an answer of length n is correct is `(1-e)^n`

Errors accumulate. 错误不断累积
- The probability of correctness decreases exponentially.
- One can mitigate the problem by making e smaller (through training) but one simply cannot eliminate the problem entirely.
- A solution would require to make LLMs non auto-regressive while preserving their fluency.

Auto-Regressive Large Language Models (`AR-LLMs`)
- Outputs one text token after another
- Tokens may represent words or subwords
- Encoder/predictor is a transformer architecture
  - With billions of parameters: typically from 1B to 500B
  - Training data: 1 to 2 trillion tokens
- LLMs for dialog/text generation:
  - BlenderBot, Galactica, LLaMA (FAIR), Alpaca (Stanford), LaMDA/Bard(Google), Chinchilla (DeepMind), ChatGPT (OpenAI), GPT-4 ??...
- Performance is amazing ... but ... they make stupid mistakes
  - Factual errors, logical errors, inconsistency, limited reasoning, toxicity...
- LLMs have no knowledge of the underlying reality
  - They have no common sense & they can’t plan their answer

Unpopular Opinion about AR-LLMs
- Auto-Regressive LLMs are doomed. 
- They cannot be made factual, non-toxic, etc.
- They are not controllable
- Probability `e` that any produced token takes us outside of the set of correct answers
- Probability that answer of length `n` is correct: $ P(correct) = (1-e)^n $

This diverges exponentially. It’s not fixable.

Auto-Regressive Generative Models Suck!

AR-LLMs
- Have a constant number of computational steps between input and output. Weak representational power.
- Do not really reason. Do not really plan

Humans and many animals
- Understand how the world works.
- Can predict the consequences of their actions.
- Can perform chains of reasoning with an unlimited number of steps.
- Can plan complex tasks by decomposing it into sequences of subtasks

The full slide deck is [here](https://drive.google.com/file/d/1BU5bV3X5w65DwSMapKcsr0ZvrMRU_Nbi/view?fbclid=IwAR2itiKMdM7LbpRs-YSKtLVFrHQLXKEEmNFAMI4xTY0SvROLJwN4bVKhs7M)

This was my introductory position statement to the philosophical debate 
- “[Do large language models need sensory grounding for meaning and understanding?](https://drive.google.com/file/d/1BU5bV3X5w65DwSMapKcsr0ZvrMRU_Nbi/view?fbclid=IwAR2itiKMdM7LbpRs-YSKtLVFrHQLXKEEmNFAMI4xTY0SvROLJwN4bVKhs7M)”

Which took place at NYU Friday evening.

【2023-3-29】[Yann LeCun](https://www.facebook.com/yann.lecun?__cft__[0]=AZWxqCTGSsq16rkzWGzvyCX2L6tYvmuDvSqPiCBmusZVzK9GB4xmaSzPmElCb7-Cfle8Ahio85t32RbgdwIHFEllkfCNqSBEShuPK0GrVdTazsdfgVPqTW9aCJrwOxUkPPLmORDlMBK3iC4ptkcUY8ntw3poQipY_WNjMsiA-_hTaA&__tn__=-UC%2CP-R)： GPT-4并未达到人类智能，年轻人花20h练车就掌握了开车技能，即便有专业司机的海量训练数据、高级传感器的辅助，L5级别自动驾驶到现在还没实现
>- If you think GPT-4 and similar systems approach human-level intelligence, ask yourself why any teenager can learn to drive a car in about 20 hours of practice and yet we still don't have Level-5 self-driving cars. This is despite having enormous amounts of training data from expert drivers and vehicles equipped with sensors with superhuman capabilities.
>- I agree with former Meta-AI engineering manager and  VP of AI/ML at Cruise [Hussein Mehanna](https://www.facebook.com/hussein.mehanna?__cft__[0]=AZWxqCTGSsq16rkzWGzvyCX2L6tYvmuDvSqPiCBmusZVzK9GB4xmaSzPmElCb7-Cfle8Ahio85t32RbgdwIHFEllkfCNqSBEShuPK0GrVdTazsdfgVPqTW9aCJrwOxUkPPLmORDlMBK3iC4ptkcUY8ntw3poQipY_WNjMsiA-_hTaA&__tn__=-]K-R) : the real revolution in AI is still to come.

what's missing in chatGPT to become human level intelligence
1. 理解现实世界 An understanding of the real world.
2. 推理规划能力 The ability to reason and plan
3. 执行任务的代理人 Agency: the ability to take actions
4. 产生有效答案的能力 The ability to produce answers that satisfy objectives, like factuality, non-toxicity, etc

And probably a dozen other things that we don't yet realize are necessary for intelligence..

<iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fyann.lecun%2Fposts%2Fpfbid0Ytvf7jiSFGjtoMkGV4J8V7dmhVVZhA7rct9Fvg2mbuYTTRre3dC5yfN4Xi3fqQThl&show_text=true&width=500" width="500" height="603" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>

### Google

为了应对ChatGPT的威胁，已退出谷歌日常业务的两位谷歌联合创始人紧急重返公司，多次发起会议商讨对策。谷歌还向研发ChatGPT竞品的AI创企Anthropic投资了约3亿美元。而Anthropic创始成员曾为创造ChatGPT的OpenAI工作。

2023年2月6日，谷歌投资人工智能初创企业 Anthropic 近4亿美元，同时，谷歌内部也同步研发了很多大模型产品，以此来加固自己的护城河。
- 谷歌云正启动一个为 Atlas 的“**红色警报**”项目，以应对ChatGPT的威胁。另一个产品部门一直在测试一个可使用问答形式的新搜索页面。此外，谷歌还在测试一款采用谷歌对话AI语言模型LaMDA的聊天机器人Apprentice Bard。

Apprentice Bard 和 ChatGPT 功能类似，待用户在对话框输入问题后，能够以更像人类问答的形式给出对应问题的详细答案。并且也如嵌入ChatGPT的新版Bing那样，Apprentice Bard据说能回答最近发生的事件。

不过其回答的可靠程度仍有待提升。一个在谷歌内部流传的例子是，有位测试人员问Apprentice Bard：谷歌是否会进行又一轮裁员？
- 2023年1月，谷歌宣布裁员12000人，占其员工总数的6%

- 【2023-2-6】谷歌发布 BARD，[An important next step on our AI journey](https://blog.google/technology/ai/bard-google-ai-search-updates/?continueFlag=db431874167e6b7ed4c39d023c3b26b2)，We’ve been working on an experimental conversational AI service, powered by LaMDA, that we’re calling Bard
- ![img](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Frame_13213203313x.width-1000.format-webp.webp)

谷歌AI负责人 Jeff Dean 此前曾告诉员工
- 谷歌有能力做出媲美ChatGPT的产品，之所以迟迟不愿发布，是因为担心这类产品会因提供**错误信息**等缺陷而影响公司商誉，因此比“小型初创公司更加**保守**”。

当前的紧迫形势已经逼得谷歌无法再等下去。谷歌母公司Alphabet的CEO桑达尔·皮查伊说
- “我们将大胆地开展这项工作，但要怀着强烈的责任感。”
- 谷歌将在“未来几周或几个月”推出类似ChatGPT的大型语言模型LaMDA，用户很快就能以“搜索伴侣”的形式使用该模型。

## ChatGPT 改变行业

微软联合创始人比尔·盖茨表示，ChatGPT可以对用户查询做出惊人的类似人类的反应，与互联网的发明一样重要：
- “到目前为止，人工智能可以读写，但无法理解内容。像ChatGPT这样的新程序将通过帮助写发票或信件来提高许多办公室工作的效率，这将改变我们的世界”。
- “这与个人电脑、互联网一样重要，成为2023年最热门的话题”。

ChatGPT是生成式人工智能（Generative AI，简称GAI）的一种 ，同类AI还包括 DALL-E、Stable Diffusion，以及Midjourney。与 ChatGPT不同的是，它们根据用户的文本描述来“生成”图像，但名气远远不及ChatGPT。

3月28日，高盛（Goldman Sachs）在最新研究报告
- 3月26日，[The Potentially Large Effects of Artificial Intelligence on Economic Growth](https://www.key4biz.it/wp-content/uploads/2023/03/Global-Economics-Analyst_-The-Potentially-Large-Effects-of-Artificial-Intelligence-on-Economic-Growth-Briggs_Kodnani.pdf)
- ChatGPT等生成式AI将给全球劳动力市场带来巨大影响，全球预计将有3亿个工作岗位被生成式AI取代，而`律师`和`行政人员`将是最有可能被裁员的岗位。[参考](https://tech.ifeng.com/c/8OWi6s4iWEs)

生成式人工智能可以在10年内将全球GDP提高**7%**，但也将给劳动力市场带来“重大**颠覆**”。大型经济体中相当于**3亿**全职工人受到自动化的威胁。
- 未来10年全球GDP年增长率有望达7%
- 广泛采用人工智能（AI）技术有望促进生产率的大幅提升并推动全球经济加速增长。
- 节省大量劳动力成本、创造新的就业机会以及未被取代劳工的生产率提升等因素相结合可能会导致产出激增，进而“显著”提高全球经济增速。
- “生成式AI”或能在十年内将美国劳动力生产率每年提高约1.5个百分点。相较之下，美国生产率在截至2022年的十年间平均仅提升了1.3%，是阻碍该国薪资增长的主要因素。

### AI取代的工作 -- 李开复

李开复列举了20项AI容易取代的工作。[参考](https://mp.weixin.qq.com/s/3o6xyofx1QrwBOqIiZSpuw)

最危险TOP10种工作（从事这些工作的朋友，需要提前做好规划了！）
- 1、电话营销员/电话销售
- 2、客户服务
- 3、仓库工人
- 4、出纳和运营人员
- 5、电话接线员
- 6、出纳员/收银员
- 7、快餐店员
- 8、洗碗工
- 9、生产线质检员
- 10、快递员

“外强中干”工作TOP10（这些工作看上去是金饭碗，其实危机四伏）
- 1、销售与市场研究
- 2、保险理赔员
- 3、保安人员
- 4、卡车司机
- 5、消费者贷款受理人
- 6、财经和体育记者
- 7、记账员与财务分析师
- 8、水果采摘者
- 9、专业投资人员

### ChatGPT答复

问
> ChatGPT 最容易取代的是哪些领域

答
>-  作为一个人工智能语言模型，ChatGPT 主要的应用领域是自然语言处理和语言生成。因此，ChatGPT 更容易取代那些需要处理**大量文字**、进行自然语言**理解和生成**的工作。
>- 一些可能会被ChatGPT 取代的领域包括：
>- 客服和在线支持：ChatGPT 可以通过语言理解和生成技术来回答用户的问题和提供帮助，从而取代一些人工客服的工作。
>- 文章写作和编辑：ChatGPT 可以根据输入的主题和指示生成高质量的文章，从而减少人工写作和编辑的需求。
>- 简单的法律文件和合同：ChatGPT 可以根据指定的条款和条件，生成简单的法律文件和合同，从而减少一些律师和法务人员的工作量。
>- 搜索引擎优化：ChatGPT 可以生成高质量的文章和内容，从而提高网站的排名和流量，减少需要人工优化的工作。
>- 需要注意的是，虽然 ChatGPT 可以在某些领域替代一些简单的工作，但它仍然需要人类的监督和干预来确保生成的内容的准确性和合法性。


ChatGPT 无法取代所有领域，特别是那些需要人类情感、创造力和决策能力的领域。不过，相对来说，ChatGPT 擅长的领域主要包括：
- 命令式任务：ChatGPT 可以执行一些简单的任务，例如在规定时间内发送电子邮件或创建备忘录等。
- 数据分析：ChatGPT 可以帮助人们分析大量数据，识别模式和趋势，以及进行预测。
- 客户服务：ChatGPT 可以用于自动回复客户的问题或提供帮助。
- 内容生成：ChatGPT 可以生成简单的文本内容，例如新闻摘要、产品说明或推荐信等。

总的来说，ChatGPT 最容易取代那些重复性、单调、简单的任务，而对于需要创造力、判断力和情感理解的领域，则仍需要人类的参与。


没有绝对的答案，因为不同的工作有不同的要求和难度，而ChatGPT也有自己的局限性和风险。但是，可以根据一些标准来推测一下，比如：
- 工作是否主要涉及文本交流和信息处理
- 工作是否需要高度的创造力和专业知识
- 工作是否有明确的目标和评估标准
- 工作是否涉及敏感或危险的内容和行为

基于这些标准，以下十五个工作最有可能被ChatGPT替代：
1. **文本摘要**：文本摘要工作主要是通过文本为用户提供长篇文章或文档的概括和总结。这个工作相对困难且有挑战性，而且需要一定程度的逻辑思维和语言表达能力。ChatGPT可以通过学习大量的文本数据，模仿不同类型和风格的文本摘要者，提供合适和有用的摘要。当然，ChatGPT也可能遇到一些无法理解或者偏离主题的情况，这时候就需要人工检查和修改。
1. **文本生成**：文本生成工作主要是通过文本为用户提供新颖或有趣的内容，如故事、诗歌、歌词等。这个工作相对困难且有创意性，而且需要一定程度的想象力和表达力。ChatGPT可以通过学习大量的文本数据，模仿不同类型和风格的文本生成者，提供合适和有趣的文本。当然，ChatGPT也可能遇到一些无法理解或者不合逻辑的情况，这时候就需要人工评估和修改。
1. **对话生成**：对话生成工作主要是通过文本或语音为用户提供自然或有意义的对话，如聊天机器人、智能助理等。这个工作相对困难且多变化，而且需要一定程度的交流能力和情感理解能力。ChatGPT可以通过学习大量的对话数据，模仿不同场景和话题的对话生成者，提供合适和友好的对话。当然，ChatGPT也可能遇到一些无法回答或者不恰当的问题或请求，这时候就需要人工干预和处理 。
1. **语音合成**：语音合成工作主要是通过语音为用户提供文本内容的朗读或演讲，如语音阅读器、语音播报员等。这个工作相对简单且常用，而且需要一定程度语音合成：语音合成工作主要是通过语音为用户提供文本内容的朗读或演讲，如语音阅读器、语音播报员等。这个工作相对简单且常用，而且需要一定程度的发音和语调能力。ChatGPT可以通过学习大量的语音数据，模仿不同语言和风格的语音合成者，提供合适和清晰的语音。当然，ChatGPT也可能遇到一些无法发音或者不自然的情况，这时候就需要人工调整和优化。
1. **客服支持**：客服工作主要是通过文本或语音与客户沟通，解决用户问题或需求。这个工作相对简单且重复性高，而且有明确的目标和评估标准（比如满意度、解决率等）。
  - ChatGPT可以通过学习大量的客服对话数据，模仿客服人员的语气和风格，提供合适和友好的回应。当然，ChatGPT也可能遇到一些无法解决或者超出范围的问题，这时候就需要转接给真人客服。
1. **聊天陪伴**：聊天陪伴工作主要是通过文本或语音与用户聊天，提供情感支持或娱乐。这个工作相对灵活且多样化，但也不需要太高的创造力和专业知识。ChatGPT可以通过学习大量的聊天数据，模仿不同类型和风格的聊天对象，提供适合场景和心情的回应。当然，ChatGPT也可能遇到一些无法理解或者不恰当的话题或请求，这时候就需要拒绝或者转换话题。
1. **文章写作**：文章写作工作主要是通过文本表达某种观点、信息或故事。这个工作相对复杂且创造性高，而且需要一定程度的专业知识。ChatGPT可以通过学习大量文章写作：文章写作工作主要是通过文本表达某种观点、信息或故事。这个工作相对复杂且创造性高，而且需要一定程度的专业知识。ChatGPT可以通过学习大量的文章数据，模仿不同类型和风格的文章，提供合适和流畅的文字。当然，ChatGPT也可能遇到一些无法理解或者错误的信息，这时候就需要人工校对和修改。
1. **翻译**：翻译工作主要是通过文本或语音将一种语言转换成另一种语言。这个工作相对简单且规范化高，而且有明确的目标和评估标准（比如准确度、流畅度等）。ChatGPT可以通过学习大量的双语数据，模仿不同语言之间的对应关系，提供合适和自然的翻译。当然，ChatGPT也可能遇到一些无法处理或者歧义的情况，这时候就需要人工干预和调整。
1. **机器翻译**：机器翻译工作主要是通过文本或语音为用户提供不同语言之间的转换和对应。这个工作相对困难且复杂，而且需要一定程度的语言学习和跨文化交流能力。ChatGPT可以通过学习大量的双语或多语数据，模仿不同语言和场景的机器翻译者，提供合适和流畅的翻译。当然，ChatGPT也可能遇到一些无法准确或者保持原意的情况，这时候就需要人工校对和修正。
1. **内容审核**：内容审核工作主要是通过文本或图像检查网络上发布的内容是否符合规范和道德。这个工作相对困难且敏感性高，而且需要一定程度的判断力和责任心。ChatGPT可以通过学习大量的内容数据，模仿不同平台和领域的审核标准，提供合适和及时的审核结果。当然，ChatGPT也可能遇到一些无法识别或者争议的内容，这时候就需要人工复核和决策。
1. **教育辅导**：教育辅导工作主要是通过文本或语音向学生提供知识、技能或情感方面的指导和帮助。这个工作相对灵活且多元化，但也需要一定程度的专业知识和沟通能力。ChatGPT可以通过学习大量的教育数据，模仿不同科目和领域的教师和辅导员，提供合适和有效的辅导。当然，ChatGPT也可能遇到一些无法解答或者超出范围的问题，这时候就需要人工介入和协助。
1. **营销文案**：营销文案工作主要是通过文本吸引潜在客户的注意力和兴趣，促进产品或服务的销售。这个工作相对简单且重复性高，而且有明确的目标和评估标准（比如点击率、转化率等）。ChatGPT可以通过学习大量的营销数据，模仿不同行业和市场的营销人员，提供合适和有吸引力的文案。当然，ChatGPT也可能遇到一些无法适应或者违反规则的情况，这时候就需要人工审核和修改。
1. **新闻写作**：新闻写作工作主要是通过文本报道事实、信息或观点。这个工作相对困难且敏感性高，而且需要一定程度的专业知识和责任心。ChatGPT可以通过学习大量的新闻数据，模仿不同媒体和领域的记者，提供合适和准确的新闻。当然，ChatGPT也可能遇到一些无法获取或者错误的信息，这时候就需要人工核实和纠正。
1. **社交媒体管理**：社交媒体管理工作主要是通过文本或图像与社交媒体上的用户互动，增加品牌或个人影响力。这个工作相对简单且多样化，但也需要一定程度的创意和策略。ChatGPT可以通过学习大量的社交媒体数据，模仿不同平台和话题的社交媒体经理，提供合适和有趣的内容。当然，ChatGPT也可能遇到一些无法适应或者违反规则的情况，这时候就需要人工监督和调整。

### 10种工作

前OpenAI研究团队负责人Jeff Clune预测，有**30%**的机会，在2030年借助AGI（通用AI）实现50%的人类工作自动化。基于聊天的人工智能可以通过自动化重复任务来增强人类的工作方式，同时提供与用户更具吸引力的交互。[参考](https://news.sohu.com/a/642750678_247850)

麦肯锡预测：2030年，中国将有至少**1.18亿人**的岗位被机器人取代。
- 这要求他们学习新技能，适应与机器人的合作分工；
- 其中700~1200万人需要转换职业。

可能会受到波及的行业：
- 1、凡涉及到`标准化`、`流程化`、人力或管理成本高的领域，都将全面`数字化`、`机器人化`与`智能化`，需要人的岗位就是操作员，甚至仅作为系统风控备份设置，先进制造业产业工人的知识门槛会提高，窗口型、服务型的大部分岗位将以机器人为主，比如客服。
- 2、在各行业的研发领域，AI也将取代大部分**基础岗位**。
- 3、岗位没有了，管人的职务自然也会大幅度减少，传统企业管理更多在强调“团队”，新一代企业却会更扁平化。
- 4、**文化娱乐**行业将被改写。在内容生产领域（文案、海报、视频直播、音乐、动漫、游戏等），人工智能无论原创还是二创，都会比大多数从业者干的更出色，哪怕是顶尖的人士也会采用AI辅助设计。

### ChatGPT 取代的工作

[ChatGPT 最可能取代的 10 种工作 ](https://www.sohu.com/a/656872711_532789)

麦肯锡全球研究所的合伙人Anu Madgavkar: 将人类的判断应用于这些技术，才能避免错误和偏见。
- “我们必须将这些东西视为提高生产力的工具，而不是完全替代我们的工作。”

IT招聘公司The Bridge的主管沃兹沃思（Andy Wadsworth）认为
- 像ChatGPT这样的服务是公众进入`潘多拉魔盒`的第一个窗口，这个魔盒有可能成为工业革命3.0，这其中会产生**赢家**和**输家**。
- 一些工作将被人工智能取代，但是那些学会**使用生成式人工智能**并适应这个新世界的公司和个人将成为赢家

专业人士认为: `程序员`、`媒体工作者`、`财务分析师`等职位，被人工智能取代的风险最高。

最不易被取代的岗位是需要面对面的**互动**和**身体技能**的角色，这些人工智能无法替代。比如：泥水匠、电工、机械师等手艺人，以及美发师、厨师、医生和护士等服务人员，这些将继续依赖人类对任务的理解和完成任务的能力而存在。

复旦大学计算机学院教授、博士生导师黄萱菁。
- “当模型的参数规模还不太大的时候，你看不到它的强大，当达到某一个临界值时，这个模型就会非常强大，目前我们认为这个参数规模的临界值可能是650亿。”
- 在肉眼可见的未来，善用AI的人将和不用AI的人在工作效率上产生巨大差距。

取代你的不是Al，而是会用AI的人。
- 有个抖音号一个星期时间200多万播放，1.8万粉丝，基本全是用AI工具做的。

与专家交谈和进行研究后, 整理了一份被人工智能技术取代风险最高的工作类型清单：

外媒盘点了最可能被 ChatGPT 取代 10 大高危职位：
1. 技术工种（程序员、软件工程师、数据分析师）
2. 媒体工作者（广告、内容创作、记者）
3. 法律行业工作者（律师助力、法律助理）
4. 市场研究分析师
5. 教师
6. 财务（财务分析师， 个人财务顾问）
7. 交易员
8. 平面设计师
9. 会计师
10. 客服

万事都具备两面性，就拿程序员工作来说，ChatGPT的出现可能会对底层程序员造成一定的影响，但不会导致程序员失业。因为，ChatGPT本身也需要程序员进行开发和维护。

#### 01 技术类工作：程序员、软件工程师、数据分析师

- 像ChatGPT和类似的人工智能工具可能会在不久的将来率先替代编码和计算机编程技能。
- Madgavkar表示，软件开发人员、网络开发人员、计算机程序员、编码员和数据科学家等技术岗位“很容易”被人工智能技术“取代更多的工作”，这是因为像ChatGPT这样的人工智能擅长相对准确地处理数字。
- 像ChatGPT这样的先进技术可以比人类更快地生成代码，这意味着一项工作在未来可以用更少的员工完成。诸如ChatGPT制造商OpenAI这样的科技公司已经在考虑用人工智能取代软件工程师。


#### 02 媒体类工作：广告、内容创作、技术写作、新闻

- Madgavkar表示，所有的媒体工作——包括广告、技术写作、新闻以及任何涉及内容创作的角色，都可能受到ChatGPT和类似形式的人工智能的影响。她补充说，这是因为人工智能能够很好地阅读、写作和理解基于文本的数据。
- Madgavkar 说：分析和解释大量基于语言的数据和信息是一项技能，可以期待生成式人工智能技术的提升。

事实上，媒体行业已经开始尝试使用人工智能生成的内容。科技新闻网站CNET已经使用人工智能工具撰写了数十篇文章，而数字媒体巨头BuzzFeed也宣布将使用ChatGPT生成更多新内容。

ChatGPT和Midjourney出来后，他当天就把编剧和原画师给辞退了，就这么残酷

【2023-7-31】[日本两艺术系女生欲跳崖，“人生被AI毁掉了”](https://www.toutiao.com/article/7261985188262150697)

6月19日下午6时左右，一名18岁左右的女孩坐在崖边，有轻生迹象。巡逻的工作人员见状上前询问情况，女孩见到工作人员后崩溃大哭，最终被成功解救。

据了解，这名女孩高中时所创作的插画作品获得了国家级大奖，因此被老师推荐进入艺术大学，目前就读于某艺术大学艺术系，是一名大一学生。然而，进入大学三个月后，她体验到了学校引进的AI的可怕之处。她表示，只要把想要画下来的主题输入进AI，就能立马得到一幅完成度较高的画，除此之外，课程上需要几日的研究才能完成的课题，AI仅用十分钟就能完成，这让她感到非常惶恐。

由于家境贫寒，她不得不申请了800万日元（约合人民币40.24万元）的贷款奖学金，然而她却因觉得自己无法顺利完成学业而萌生退学的想法。她向母亲传达了这一想法后，母亲却强硬地要求她只能读完大学。她说：“因为人工智能的存在，我不再能画出喜欢的画，还欠下了一大笔债。我不再能看到未来，所以选择来到这里自杀。”

主修动画和游戏的毕业生：
- “有了人工智能，我变得一无是处”
- 需几天完成的画，AI用10分钟搞定

#### 03 法律类工作：法律或律师助理

与媒体行业从业人员一样，律师助理和法律助理等法律行业工作人员也是在进行大量的信息消化后，综合他们所学到的知识，然后通过撰写法律摘要或意见使内容易于理解。
- Madgavkar称，像这样以语言为导向的角色很容易进行自动化处理。她补充说：

这些数据实际上相当结构化，非常以语言为导向，因此非常适合生成式人工智能。但人工智能无法完全实现这些工作的自动化，因为仍然需要一定程度的人类判断来理解客户或雇主的需求。

#### 04 市场研究分析师

布鲁金斯学会高级研究员Mark Muro表示，人工智能擅长分析数据和预测结果，这就导致市场研究分析师非常容易受到人工智能技术的影响。

#### 05 教师

虽然ChatGPT的大火让老师们都开始担心学生使用这一技术作弊，但罗切斯特理工学院计算与信息科学系副主任Pengcheng Shi认为，老师们也应该考虑自己的工作安全。

Shi 在接受媒体采访时表示，ChatGPT“已经可以作为一名老师轻松地授课了”。他说：尽管它在知识方面存在缺陷和不准确之处，但可以很容易地加以改进。基本上，你只需要训练ChatGPT。

#### 06 金融类工作：金融分析师、个人财务顾问

Muro还表示，像市场研究分析师、金融分析师、个人财务顾问和其他需要处理大量数字数据的工作，都会受到人工智能的影响。

Muro称：这类分析师赚了很多钱，但他们的部分工作是可自动化的。

#### 07 交易员

Shi还向媒体表示，华尔街的某些职位也可能处于危险之中。在一家投行里，人们从大学毕业后就被雇佣，然后花两三年时间像机器人一样工作、做各种Excel表格，但现在可以让人工智能来做这些。

#### 08 平面设计师

在媒体去年12月的一篇文章中，3位教授指出，OpenAI创建的图像生成器DALL-E可以在几秒钟内生成图像，是平面设计行业的一个“潜在颠覆者”。

3位教授写道：
- 提高数百万人创作和处理图像的能力，将对经济产生深远的影响。

对于一些工作受到直接影响、难以适应的人来说，人工智能领域的最新进展肯定会带来一段困难和经济痛苦的时期。

ChatGPT和Midjourney出来后，他当天就把编剧和原画师给辞退了，就这么残酷

#### 09 会计师

虽然会计师通常是一个较为稳定的职业，但也处于类似风险之中。

多伦多大学传播、文化、信息和技术研究所副教授Brett Caraway前阵子公开表示，虽然人工智能技术还未真正成熟，但已经让一些人感受到了危机。他补充称说，“智力劳动”尤其可能受到威胁。

Caraway表示：可能是律师、会计师，等等。这是一件新事物。

#### 10 客服人员

几乎每个人都有过这样的经历：给一家公司的客服打电话或聊天，由机器人接听。而ChatGPT和相关技术可能延续这一趋势。

科技研究公司Gartner在2022年的一项研究预测显示，到2027年，聊天机器人将成为约25%的公司的主要客户服务渠道。


# 结束
