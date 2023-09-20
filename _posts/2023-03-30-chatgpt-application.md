---
layout: post
title:  ChatGPT应用
date:   2023-03-30 19:10:00
categories: 深度学习 自然语言处理
tags: AIGC ChatGPT 智能客服
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

【2023-3-16】[Poe](https://poe.com/claude+) 各种机器人，sage, gpt-4, ChatGPT等，一次免费体验机会

## ChatGPT 行业应用

ChatGPT 非常实用，能帮助普通人节省不少脑力和时间成本。
- 回答后续问题、承认错误、挑战不正确的前提、拒绝不适当的请求。

ChatGPT在办公软件、社交文娱、营销广告、家庭助理四大方向的15条赛道，AI大模型技术正出现落地的萌芽。其中不仅有国民级的Office工具、钉钉等协同办公平台接入大模型，还有来自办公、电商、家居、社交文娱互联网平台推出AIGC功能，甚至以智能汽车、AR眼镜为代表的实体终端也上了大模型，带来新奇体验。

【2023-5-11】生成式AI创业领域
- ![](https://pic3.zhimg.com/80/v2-bdd24bc6e1db0c18c5d8f616dcc578be_1440w.webp)
- [全面接入！ChatGPT杀进15个商业应用，让AI替你打工](https://zhuanlan.zhihu.com/p/628096018)


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
- 模型精调：百尺竿头更进一步
  - 客户需要利用自有数据或领域非公开数据进行持续训练，以及建设和积累自己的精调数据集。对精调手段的良好运用，能够帮助企业客户利用更小的模型尺寸，在特定任务上达到媲美通用大模型的水平，由此进一步降低推理成本。
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

#### 人工标注

【2023-3-29】ChatGPT超过人工标注
- [ChatGPT Outperforms Crowd-Workers for Text-Annotation Tasks](https://arxiv.org/abs/2303.15056?fbclid=IwAR2j7nL9y2pvxkHHkbZtbWbfEGuyaqiQ6NYVO39WkpUK5NGkBGZLjiMx0ho)
- Many NLP applications require manual data annotations for a variety of tasks, notably to train classifiers or evaluate the performance of unsupervised models. Depending on the size and degree of complexity, the tasks may be conducted by crowd-workers on platforms such as MTurk as well as trained annotators, such as research assistants. Using a sample of 2,382 tweets, we demonstrate that ChatGPT outperforms crowd-workers for several annotation tasks, including relevance, stance, topics, and frames detection. Specifically, the zero-shot accuracy of ChatGPT exceeds that of crowd-workers for four out of five tasks, while ChatGPT's intercoder agreement exceeds that of both crowd-workers and trained annotators for all tasks. Moreover, the per-annotation cost of ChatGPT is less than $0.003 -- about twenty times cheaper than MTurk. These results show the potential of large language models to drastically increase the efficiency of text classification.

苏黎世大学：
> ChatGPT标注数据比人类便宜**20倍**，**80%**任务上占优势

在ChatGPT面前，无论成本还是效率，人类可以说是毫无优势：
- 成本上，ChatGPT平均每个标注成本低于0.003美元，比众包平台便宜20倍；何况AI还能24*7无休。
- 效率上，在相关性、立场、主题等任务中，ChatGPT也是以4:1的优势“碾压”人类。

`MTurk` 是专门进行数据标注的一个众包平台。
- 在MTurk这类众包平台内部，还会有更加精细的分工，比如说会有经过专业训练的数据标注者以及众包工作者。
- 前者在产出高质量数据上具有优势，但自然成本也更高，而后者虽然更便宜但质量也会随任务难度波动。

于是, 研究大语言模型（LLM）在这方面的潜力，并且对比了没有额外训练（zero-shot）的ChatGPT（基于GPT-3.5）和MTurk在数据标注上的性能。这项对比基于研究团队此前收集到的2382条推文样本。

ChatGPT和MTurk分别将推文以“相关性、立场、主题、政策、实用性”这五种任务进行标注。

“生成训练数据需要人工”的说法已经成为过去式

ChatGPT 用于 人工标注的 Web系统：[Weak Labeling Tool using ChatGPT](https://github.com/ainbr/chatgpt-weak-labeler-web-ui), [代码](https://github.com/ainbr/chatgpt-weak-labeler-web-ui/blob/master/app.py)
- ![](https://github.com/ainbr/chatgpt-weak-labeler-web-ui/raw/master/misc/screenshot1.png)

【2023-6-18】[无需人力标注！悉尼大学华人团队提出"GPT自监督标注范式](https://www.toutiao.com/article/7245196537557549623)

业界和学界面临数据标注任务：成本较高、存在偏见、难以评估，以及标注难度等问题。

悉尼大学研究团队提出了一种通过大语言模型**自监督生成标注**的框架。首次利用基于**生成-还原**循环标注的GPT自监督方法，解决了上述问题
- davinci，text-curie-001，text-davinci-003，gpt-3.5-turbo在不同评估标准下标注数据质量的得分
- [论文链接](https://arxiv.org/pdf/2306.04349.pdf)

核心思想: 利用大语言模型作为一个**黑盒优化优器**，构造了一个循环：
- 模版质量越高，生成的数据-标注对质量越高；
- 生成的数据标注对质量越高，用当前质量更高的数据对替换上一轮的模版。
- 以此往复迭代，滚雪球式循环提升标注质量。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/2f0cd7e8bebb47218672ba0a28b98008~noop.image)

标注方法包含了**one-shot阶段**和**生成阶段**。
- one-shot阶段的目标：迭代寻找**最优**的 \{数据-标注\}数据对 作为模板。

迭代过程：
- 初始化一个简单数据对作为初始模版，利用GPT生成标注，生成的标注和原始数据形成一个新的数据对。
- 然后，通过比较从标注中还原出来的数据和原始数据，评估这个新数据对作为模板的潜力。
- 如果还原数据与原数据的相似度得分有所提高，就用当前新数据对直接作为新的模板进行一轮数据生成。

因此，这种**自我对齐机制**会迭代调整one-shot模板，为下一轮生成做好准备。one-shot阶段搜索到的最优模板随后用于对数据集进行标注。

通过调整不同的预训练奖励模型来评估标注的质量，并引入不同的评价指标来间接评估摘要的还原能力。

【2023-6-19】[GPT-4终结人工标注！AI标注比人类标注效率高100倍，成本仅1/7](https://www.toutiao.com/article/7280051689963635212)

数据标注需要找到一个新方法，避免大量使用人工标注带来的包括道德风险在内的其他潜在麻烦。所以，包括谷歌/Anthropic在内的AI巨头和大型独角兽，都在进行数据标注自动化的探索。
- 谷歌最近的研究，开发了一个和人类标注能力相近的AI标注工具
  - 论文: [RLAIF:Scaling Reinforcement Learning from Human Feedback with AI Feedback]()
- Anthropic采用了Constitutional AI来处理数据，也获得了很好的对齐效果
  - 论文: [Constitutional Al: Harmlessness from AI Feeedback]()
- 初创公司refuel，也上线了一个AI标注数据的开源处理工具：`Autolabel`。用AI标注数据，效率最高提升100倍. [introducing-autolabel](https://www.refuel.ai/blog-posts/introducing-autolabel)
  - 按照使用成本最高的GPT-4来算，采用`Autolabel`标注的成本只有使用人工标注的1/7，而如果使用其他更便宜的模型，成本还能进一步降低

Autolabel安装

```sh
# 安装所有必要的库
pip install 'refuel-autolabel[openai]'
```

```py
from autolabel import get_data
get_data('civil_comments')
```

自动标签贴标分为三个步骤:
- 首先，指定一个标签配置(参见下面的config对象)并创建一个LabelingAgent。
- 接下来，通过运行agent.plan，使用config中指定的LLM对的数据集进行一次标注
- 最后，使用agent.run运行标签


#### 数据分析

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



### NLP基础任务

【2023-9-12】[大语言模型在NLP基础任务的应用案例集](https://zhuanlan.zhihu.com/p/625321362)

#### 分类

怎么用GPT做分类？

两种方法
- 类似bert，在输出部分加个head，输出分类得分；
- 与clm语言模型一致，在生成类别广告词，来判断分类。

详见：[文本分类专题](classification)

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

### 写代码


#### NL2Code

【2023-5-30】[代码大模型综述：中科院和MSRA调研27个LLMs，并给出5个有趣挑战](https://mp.weixin.qq.com/s/t2SMftox6546E7kvRgQMnA)
- NL2Code: 将自然语言转换成可执行代码来提高开发人员的工作效率
- 中科院和微软亚洲研究院在 ACL 2023 国际顶会上发表的一篇综述：调研了 NL2Code 领域中的「27 个大型语言模型以及相关评价指标」，分析了「LLMs 的成功在于模型参数、数据质量和专家调优」，并指出了「NL2Code 领域研究的 5 个机遇挑战」，最后作者建立了一个分享[网站](https://nl2code.github.io)来跟踪 LLMs 在 NL2Code 任务上的最新进展。
- [Large Language Models Meet NL2Code: A Survey](https://arxiv.org/abs/2212.09420)


#### Cursor



### Document QA

详见专题：[文档问答](doc-chat)

### 推荐系统

【2023-5-20】[当推荐系统遇到大模型](https://mp.weixin.qq.com/s/YaFQoqAt12y93Nm3tX_j4A)

ChatGPT在推荐系统中的应用有不小的潜力，主要体现在以下几个方面：
- **任务统一**：所有类型的推荐任务都可以表述成**文本**，实现了推荐任务大统一，使用统一语言模型进行各个场景和任务上的推荐，有效解决多任务、多场景问题。
- **小样本**和**冷启动**问题：传统推荐系统中，小样本和冷启动是一个比较常见的问题，而大模型天然具备很强的**语义泛化能力**和**小样本学习**能力。
- 基础的推荐能力验证：多篇文章已经验证了ChatGPT等模型在推荐系统中应用是可行的，即使不在下游任务finetune，也能取得不错的效果

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

#### LLMRank

【2023-5-15】人民大学发表论文：LLM用于推荐系统排序
- [Implementation of "Large Language Models are Zero-Shot Rankers for Recommender Systems"](https://arxiv.org/pdf/2305.08845.pdf)
- 代码[LLMRank](https://github.com/RUCAIBox/LLMRank)

将推荐问题形式化为条件排序任务，将历史交互作为条件，将召回得到的候选item作为候选。 

采用特定提示方法来应用LLM解决排序任务：包括**交互历史**、**候选item**和**排序指令**来设计提示模板。
- LLM 具有很有前途的**零样本**排序能力。
- LLM **难以感知历史交互顺序**，并且可能会受到位置偏差等偏差的影响，而这些问题可以通过专门设计的**提示和引导策略**来缓解。
- ![img](https://pic3.zhimg.com/v2-b15c0128a3bedddb1eccd71772eb7116_b.jpg)

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



### 个人工具

#### 办公工具

详见站内文章：[智能办公](aigc#智能办公)


#### 数学工具

【2023-7-3】[Mathematica引入大语言模型](https://www.toutiao.com/article/7251425526433366568)

新版本Mathematica Wolfram，正式引入大语言模型（LLM）。搞科学计算，只需要一个“说”的动作。
- 直接说：Draw a red and a green semicircle.
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/d0e443a10463458a8addf73622ccaa47~noop.image)
- I want filled semicircles next to each other. And no axes. 我想要彼此相邻的填充的半圆。没有坐标轴。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/6080794989b44183b543e507c0e95ede~noop.image?_iz=58558&from=article.pc_detail&x-expires=1688968152&x-signature=GWy3pcz3sf7E41sImJot7Xd4aAg%3D)

Chat Notebook中，设置了聊天单元（chat cell）和聊天块（chatblock）

### 文本创作


#### 文案创作

【2023-4-8】创业产品：[AI百晓生](https://www.chengzijianzhan.com/tetris/page/7216273608124137509)，给视频生成文案，语音播报

#### 写小说


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



### 视觉应用

【2023-3-14】[ChatGPT 有什么新奇的使用方式？](https://www.zhihu.com/question/582979328/answer/2933058469)

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


### 直播

#### 数字人直播

智能虚拟数字人直播，自动生成、24小时不间断越来越多的数字人直播闯入电商，接下来他们可能渐渐智商变得更高，让人分不清是人是机器。
- 4月21日，位于美国旧金山的Synthesis AI宣布开发了一种可以通过文本提示创建逼真虚拟数字人的新方法，使用生成式AI和视觉效果管道来制作高分辨率、电影质量的虚拟数字人，并可用于游戏、虚拟现实、电影和模拟等各种应用。

国内智能数字人已成为众多上市公司和创企扎堆进入的领域。
- 国内AI股上市`天娱数科`的虚拟数字人已经接入ChatGPT等模型；
- 虚拟技术提供商`世优科技`目前已将ChatGPT技术接入数字人产品当中；

智能内容生成平台`来画`也在3月底正式接入ChatGPT，短短几十秒就能生成一篇高质量**视频文案**，并推出数字IP+直播模式。
- [演示](https://vdn3.vzuu.com/SD/30c605fe-ee5e-11ed-a776-8a021c6205d3-v1_f4_t2_yr6vExa3.mp4?disable_local_cache=1&bu=078babd7&c=avc.1.1&f=mp4&expiration=1683810316&auth_key=1683810316-0-0-c37e2a42c4a42997ae186fd69a5470e4&v=tx&pu=078babd7)

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

### 智能对话

角色模拟

#### Character.ai

Character.ai 是个性化 AI 聊天机器人平台，用户可以在 Character 上根据个人偏好定制 **AI 角色**并和它聊天。ChatGPT 已经证明了人们对 Chatbot 的狂热和粘性，Character.ai 在此基础上加入个性化、UGC 两大武器，有了比 ChatGPT 更丰富的使用场景。
- 自 2022 年 9 月发布后的两个月内，用户共创建了 35 万个角色，2022 年 12 月初 - 12 月中，用户日活又翻了 3 倍，目前 Character.ai 的月活跃用户数在小几十万的量级。

Character.ai 团队背景也十分亮眼，创始人 Noam Shazeer 是 Transformer 作者之一，联合创始人 Daniel de Freitas 领导了 Meena 和 LaMDA 的开发。

Character.ai 行业启发在于：随着高性能大模型的使用门槛进一步降低，未来 AI 应用层的颠覆式创新或许不在技术，而是产品设计维度的绝妙想法。

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

AI辅助家教，20美元/月定制虚拟老师家庭还是教育的园地，但很多父母难以对孩子进行很好的辅导，如果每个家里有一个定制虚拟老师会不是让情况变得不一样？

国内知名教育机构
- 5月5日, `学而思`传出正自研数学大模型`MathGPT`，将于年内推出基于该自研大模型的产品级应用；
- 同日，`网易有道`官方发布了基于“`子曰`”大模型开发的AI口语老师剧透视频；
- 5月6日，`科大讯飞`发布了认知大模型成果，并演示了“大模型+`AI学习机`”的功能，包括批改作文、模拟口语老师实景对话等。

#### Quizlet

- 国外教育应用平台`Quizlet`率先采用了ChatGPT。试想一下，如果所有孩子都有一个一对一家教将会怎样？
  - 2月28日，Quizlet推出了一款基于ChatGPT的家教软件，名为“`Q-Chat`”。不同于许多企业希望ChatGPT来帮其回答问题，Q-Chat通过有趣的聊天体验，根据相关学习材料提出可选问题，吸引学生。其从Quizlet的大量教育内容库中提取知识，能够测试学生学习情况，提出深入的问题，帮助学生学习语言，鼓励学生养成健康的学习习惯。
  - Q-Chat的聊天教学界面：[演示视频](https://vdn6.vzuu.com/SD/2fb5539a-ee5e-11ed-a975-a66626372a59-v1_f4_t2_FicCvwfw.mp4)

#### 多邻国（Duolingo）

美国教育平台多邻国（Duolingo）上的新Roleplay机器人可以与法语和西班牙语学习者聊天，纠正他们的错误并提出建议以提高他们的词汇量。
- 公司对大语言模型进行了二次开发，使其以教师身份出现，应用发现没有两次对话是相同的，教师会随着学习者的进步变得更高级。
- 这一服务每月收费30美元或每年168美元。

多邻国Roleplay机器人服务界面
- ![](https://pic4.zhimg.com/80/v2-6ebce5c943e691db4c7c00d135130d67_1440w.webp)

#### 可汗：Khanmigo

美国可汗实验学校的Khanmigo基于GPT-4等模型开发了个性化学习工具，比如“辅导我”模式和针对不同科目的测验模块。
- 首席学习官Kristen DiCerbo（克里斯汀·迪塞尔博）说：“该模型（GPT-4）对于K12主题的问题回答最准确，但对于小众主题则不太准确。”享受这一服务需要每月支付至少20美元。
- ![](https://pic2.zhimg.com/80/v2-f01869b18962c8075b2cf918ed48a915_1440w.webp)


#### 讯飞AI学习机

【2023-8-25】[首个大模型教育产品开箱：“最聪明”国产大模型加持的学习机，质变了吗？](https://mp.weixin.qq.com/s/kEoLRJgmxaJM1ujBIPT9Dw)

随着星火大模型的几次迭代，讯飞AI学习机T20系列、Lumie10系列率先完成了7大功能升级 —— 英语口语陪练、中英作文批改、数学互动辅学、百科自由问答、亲子教育助手；主打就是一个1V1的陪伴

以及最近星火V2.0多模态和代码能力的更新，学习机也相应搭载了智能编程助手、创意绘画伙伴。


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

#### 心理测评

用chatgpt做MBTI心理测评
- 论文：[Can ChatGPT Assess Human Personalities? A General Evaluation Framework](https://www.aminer.cn/pub/640166a590e50fcafd68b4ab/can-chatgpt-assess-human-personalities-a-general-evaluation-framework)
- 提出了三个评估指标，以衡量最先进的LLMs（包括ChatGPT和InstructGPT）评估结果的`一致性`、`稳健性`和`公平性`。实验结果表明，ChatGPT具有评估人类个性的能力，平均结果表明，ChatGPT可以实现更为一致和公平的评估，尽管对提示偏差的鲁棒性较低，相比之下，InstructGPT的鲁棒性更高。

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

高级Web开发人员Mate Marschalko用短短不到1小时的时间，通过与ChatGPT背后的GPT-3大模型交互，结合Siri Shortcuts做出了一个更智能的语音助手。这个语音助手不仅能控制整个苹果HomeKit智能家居系统，而且能够以超低的延迟响应轻松回答生各种问题。

他给予了ChatGPT极高评价，称尝试过这个产品后，包括苹果Siri、亚马逊Alexa、谷歌Home在内的所有“智能”助手，都显得如此愚蠢而没用。
- Mate Marschalko演示新智能助手操纵苹果HomeKit智能家居系统
- ![img](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TV46RMG9kDz4Bu~noop.image?_iz=58558&from=article.pc_detail&x-expires=1676360394&x-signature=tCxwmviN1wJeomk42ZXzv2DHEVI%3D)



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

#### 智能体

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


### 可穿戴


#### AR眼镜

【2023-3-27】[把GPT-4搞进AR眼镜，一秒生成回答内容，面试简直开挂好嘛](https://zhuanlan.zhihu.com/p/617347972)
- 斯坦福团队主要成员包括：Bryan Hau-Ping Chiang、Alix Cui和Varun Shenoy

GPT-4版AR眼镜 rizzGPT
- 基于OpenAI的自动语音识别工具Whisper收听对话，GPT-4聊天机器人实时生成自然响应，最终通过一款开源AR眼镜让用户在现实环境中了解对方的信息。
- 主体是一个圆镜片透明体，轻松挂在任何一款眼镜上面。
- ![](https://pic2.zhimg.com/80/v2-3dc5a6939497e90bc84101c843034931_1440w.webp)
- ![](https://pic3.zhimg.com/80/v2-cbdb0e3b76d355f0d93d2c35f6f2094e_1440w.webp)

### 脑机接口

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

### 突破审查


#### WormGPT

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

<iframe src="//player.bilibili.com/player.html?aid=394397165&bvid=BV1Jo4y1i72j&cid=1008617222&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  height="600" width="100%" > </iframe>


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
