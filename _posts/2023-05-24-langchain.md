---
layout: post
title:  LangChain 学习笔记
date:   2023-05-24 22:46:00
categories: 大模型
tags: gpt ChatGPT
excerpt: 大模型 LLM 驱动的智能体 Agent
mathjax: true
permalink: /langchain
---

* content
{:toc}

# LangChain

## LangChain 介绍

LangChain, 语言链条，也称：`兰链`，Harrison Chase 2022年10月创建的一个 Python 库，一种LLM语言大模型开发工具
- LangChain多语言实现：Python、node.js以及第三方提供的Go
- 几分钟内构建 GPT 驱动的应用程序。

Harrison Chase 于 2022 年 10 月底首次提交 LangChain。在被卷入 LLM 浪潮之前，只有短短几个月的开发时间

LangChain 可以帮助开发者将LLM与其他计算或知识源结合起来，创建更强大的应用程序。
- ![img](https://aitechtogether.com/wp-content/uploads/2023/05/c8538d73-3b21-4a6e-8e83-845477d3f275.webp)
- ![](https://picx.zhimg.com/v2-b048e039fd396b131767f58b9c97a37b_1440w.jpg?source=172ae18b)

论文《[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/pdf/2210.03629.pdf)》的实现：
- 该论文展示了一种**提示**技术，允许模型「`推理`」（通过思维链）和「`行动`」（通过能够使用预定义工具集中的工具，例如能够搜索互联网）。

LangChain 在没有任何收入/创收计划的情况下，获得了 1000 万美元的种子轮融资和 2000-2500 万美元的 A 轮融资，估值达到 2 亿美元左右。

### 功能

LangChain 构建的有趣应用程序包括（但不限于）：
- 聊天机器人
- 特定领域的总结和问答
- 查询数据库以获取信息然后处理它们的应用程序
- 解决特定问题的代理，例如数学和推理难题

垂直领域知识库问答架构变化
- 【2023-7-20】[LangChain+LLM大模型问答能力搭建与思考](https://zhuanlan.zhihu.com/p/644740531)

|架构图|BERT时代|LLM时代|
|---|---|---|
|图解|![](https://pic3.zhimg.com/80/v2-5131febf61f6359b0b8ca0d4bfe8e47e_720w.webp)|![](https://pic2.zhimg.com/80/v2-bf954fc376f7fe41aee068b32bab6919_1440w.webp)|
|分析|query理解异常重要|LLMs直接把模块的工作包揽了下来，原本的query分词、分类、纠错、关键词等工作变成了制定合适的Prompt|



### 文档介绍

- [官方文档](https://python.langchain.com/en/latest/index.html)
- [GPT开发利器LangChain指北](https://mp.weixin.qq.com/s/VGtjETMC-hRTAiL6hp5gyg)
- Github: [python版本](https://github.com/hwchase17/langchain )(已经有4W多的star), [go语言版](https://github.com/tmc/langchaingo)
- [基于LangChain从零实现Auto-GPT完全指南](https://aitechtogether.com/python/105086.html)
- 【2023-8-2】[京东云LangChain简介](https://www.zhihu.com/question/609483833/answer/3146379316)

### LangChain 安装

安装步骤
- python 3.8 以上才能安装

```sh
pip install langchain
pip install openai
# 环境变量
# ① 在终端中设置环境变量：
export OPENAI_API_KEY = "..."
# ② Jupyter notebook 或 Python 脚本中工作，这样设置环境变量:
import os 
os.environ[ "OPENAI_API_KEY" ] = "..."
```

测试：构建LLM应用
- LangChain 目前支持 AIMessage、HumanMessage、SystemMessage 和 ChatMessage 类型。
- 一般主要使用 HumanMessage、AIMessage 和 SystemMessage。

```py
from langchain.llms import OpenAI
# -------【构建LLM应用】--------
llm = OpenAI(temperature=0.9) # 初始化包装器，temperature越高结果越随机
# 调用
text = "What would be a good company name for a company that makes colorful socks?"
print(llm(text)) # 生成结果，结果是随机的 例如： Glee Socks. Rainbow Cozy SocksKaleidoscope Socks.
# -------【构建Prompt】-------
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)
print(prompt.format(product="colorful socks"))
# 输出结果 What is a good name for a company that makes colorful socks?
# -------【构建聊天应用】-------
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
# ------ 单条消息 --------
chat = ChatOpenAI(temperature=0)
chat([HumanMessage(content="Translate this sentence from English to French. I love programming.")])
#输出结果 AIMessage(content="J'aime programmer.", additional_kwargs={})
# ------ 多条消息：批处理 --------
batch_messages = [
    [
        SystemMessage(content="You are a helpful assistant that translates English to Chinese."),
        HumanMessage(content="Translate this sentence from English to Chinese. I love programming.")
    ],
    [
        SystemMessage(content="You are a helpful assistant that translates English to Chinese."),
        HumanMessage(content="Translate this sentence from English to Chinese. I love artificial intelligence.")
    ],
]
result = chat.generate(batch_messages)
print(result)
result.llm_output['token_usage']
# ------ 消息模板 ------
from langchain.chat_models import ChatOpenAI
# 加模板后，导入方式变化：增加 PromptTemplate后缀
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
chat = ChatOpenAI(temperature=0)
template="You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
# get a chat completion from the formatted messages
chat(chat_prompt.format_prompt(input_language="English", output_language="Chinese", text="I love programming.").to_messages())
# -> AIMessage(content="我喜欢编程。(Wǒ xǐhuān biānchéng.)", additional_kwargs={})
```

将**内存**与聊天模型初始化的**链**和**代理**一起使用。
- 与 Memory for LLMs 的主要区别：将以前的消息保留为唯一的内存对象，而不是将压缩成一个字符串。

```py
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, # 消息占位符
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
conversation.predict(input="Hi there!") # -> 'Hello! How can I assist you today?'
conversation.predict(input="I'm doing well! Just having a conversation with an AI.") # -> "That sounds like fun! I'm happy to chat with you. Is there anything specific you'd like to talk about?"
conversation.predict(input="Tell me about yourself.")
```


## LangChain 生态

LangSmith 是LangChain官方推出的 生产级LLM应用程序构建平台。
- 可以调试、测试、评估和监控任何LLM框架上构建的链和智能代理，并与 LangChain 无缝集成，LangChain 是构建LLM的首选开源框架。
- langchain 执行过程中的数据可视化展示，用于观察 chain tool llm 之前的嵌套关系、执行耗时、token 消耗等指标
- [官方文档](https://docs.smith.langchain.com/)

LangSmith由LangChain开发，LangChain是开源LangChain框架背后的公司。


### LangFlow 可视化

【2023-7-4】[LangFlow](https://github.com/logspace-ai/langflow/raw/main/img/langflow-demo.gif?raw=true) 是 `LangChain` 的一种图形用户界面（`GUI`），它为大型语言模型（LLM）提供了易用的**实验和原型设计**工具。通过使用 LangFlow，用户可以利用 react-flow 轻松构建LLM应用。

[LogSpace](https://logspace.ai/) 出品，LangFlow [github](https://github.com/logspace-ai/langflow) 的主要功能包括：
- 提供多种 LangChain 组件以供选择，如语言模型、提示序列化器、代理和链等。
- 通过编辑提示参数、链接链和代理，以及跟踪代理的思考过程，用户可以探索这些组件的功能。
- 使用 LangFlow，用户可以将流程导出为 JSON 文件，然后在 LangChain 中使用。
- LangFlow 的图形用户界面（GUI）提供了一种直观的方式来进行流程实验和原型开发，包括拖放组件和聊天框
- ![](https://github.com/logspace-ai/langflow/raw/main/img/langflow-demo.gif?raw=true)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/3985851583544f95acce1c6c2399147a~tplv-obj:1280:640.image?_iz=97245&from=post&x-expires=1696204800&x-signature=d4gBt5CjT3X6m6%2FF9sTfMLy1x6o%3D)
- [官方 UI 配置文件集合](https://huggingface.co/spaces/Logspace/Langflow)

```sh
pip install langflow # 安装
langflow # 启动
python -m langflow # 上面命令不管用时用这个
```

自动弹出本地web页面: http://127.0.0.1:7860/, 配置可导出为json格式

json格式导入 flow

```py
from langflow import load_flow_from_json

flow = load_flow_from_json("path/to/flow.json")
# Now you can use it like any chain
flow("Hey, have you heard of LangFlow?")
```

### LangSmith

LangSmith 是LangChain官方推出的 生产级LLM应用程序构建平台。
- 可以调试、测试、评估和监控任何LLM框架上构建的链和智能代理，并与 LangChain 无缝集成，LangChain 是构建LLM的首选开源框架。
- langchain 执行过程中的数据可视化展示，用于观察 chain tool llm 之前的嵌套关系、执行耗时、token 消耗等指标
- [官方文档](https://docs.smith.langchain.com/)

LangSmith由LangChain开发，LangChain是开源LangChain框架背后的公司。


## LangChain 观点

【2023-7-23】[我为什么放弃了 LangChain？](https://zhuanlan.zhihu.com/p/645345926)

由 LangChain 推广的 `ReAct` 工作流在 InstructGPT/text-davinci-003 中特别有效，但**成本很高**，而且对于小型项目来说并不容易使用。
> 「LangChain 是 RAG 最受欢迎的工具，阅读 LangChain 的全面文档，以便更好地理解如何最好地利用它。」

经过一周的研究，运行 LangChain 的 demo 示例可以工作，但是任何调整以适应食谱聊天机器人约束的尝试都会失败。
- 解决了这些 bug 之后，聊天对话的整体质量很差，而且毫无趣味。经过紧张的调试之后，没有找到任何解决方案。
- 用回了低级别的 ReAct 流程，立即在**对话质量**和**准确性**上超过了 LangChain 实现

LangChain 问题: <span style='color:blue'>让简单事情变得相对复杂</span>，而这种不必要的复杂性造成了一种「部落主义」，损害了整个新兴的人工智能生态系统。
- LangChain 代码量与仅用官方 openai 库的代码量大致相同，估计 LangChain 合并了更多对象类，但代码优势并不明显。
- LangChain 吹嘘的提示工程只是 `f-strings`，还有额外步骤。为什么需要使用这些 PromptTemplates 来做同样的事情呢？
- 真正要做的：
  - 如何创建 Agent，结合迫切想要的 `ReAct` 工作流。而 LangChain示例里每个`思想` / `行动` / `观察`中都使用了自己的 API 调用 OpenAI，所以链条比想象的要慢。
- LangChain 如何存储到目前为止的对话?

制作自己的 Python 软件包要比让 LangChain 来满足自己的需求容易得多

LangChain 确实也有很多实用功能，比如**文本分割器**和集成**向量存储**，这两种功能都是「用 PDF / 代码聊天」演示不可或缺的（在我看来这只是一个噱头）。

## LangChain 组件

2 个核心功能为：
- 1）LLM 模型与**外部数据源**进行连接。
- 2）LLM 模型与**环境**交互，通过 Agent 使用工具。

LangChain包含六部分组件
- ![img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/f101b9ecf540489280e7f95017243fb9~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=j8hpvldp7FTdOSIGCFjEyUEmbhs%3D)
- Models、Prompts、Indexes、Memory、Chains、Agents。

LangChain主要支持6种组件：
- `Models`：**模型**，各种类型的模型和模型集成，比如GPT-4
- `Prompts`：**提示**，包括提示管理、提示优化和提示序列化
- `Memory`：**记忆**，用来保存和模型交互时的上下文状态
- `Indexes`：**索引**，用来结构化文档，以便和模型交互
- `Chains`：**链**，一系列对各种组件的调用
- `Agents`：**代理**，决定模型采取哪些行动，执行并且观察流程，直到完成为止
- ![](https://picx.zhimg.com/80/v2-c4e822ce46f7f9c77ce6797047e6d2a2_1440w.webp?source=1940ef5c)

### 框架

LangChain 框架示意图

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-07-19T14:21:54.356Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;-aOkMyNOUPzSYAY1Qx6N\&quot; version=\&quot;21.6.3\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;YUrH7kkdw6S7EPocWAtV\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1434\&quot; dy=\&quot;771\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-64\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#E6E6E6;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;587\&quot; y=\&quot;226\&quot; width=\&quot;123.75\&quot; height=\&quot;135\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-15\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#E6E6E6;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;70\&quot; y=\&quot;153.75\&quot; width=\&quot;270\&quot; height=\&quot;67.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CRyWcW9bKPYmjVe2kgWn-25\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#E6E6E6;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;800\&quot; y=\&quot;215\&quot; width=\&quot;110\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CRyWcW9bKPYmjVe2kgWn-2\&quot; value=\&quot;LangChain组件\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=0;fontSize=22;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;310.13\&quot; y=\&quot;10\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-3\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-1\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-5\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-1\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-6\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-1\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-1\&quot; value=\&quot;LangChain&amp;lt;br&amp;gt;兰链\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#B3B3B3;strokeColor=#314354;fontStyle=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;225.44\&quot; y=\&quot;267.5\&quot; width=\&quot;109.62\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-24\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-60\&quot; target=\&quot;CRyWcW9bKPYmjVe2kgWn-25\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;630.75\&quot; y=\&quot;290\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-57\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;strokeColor=#FF6666;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-10\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-56\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-2\&quot; value=\&quot;Models&amp;lt;br&amp;gt;模型\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=none;rounded=1;fontStyle=1;fontSize=14;fontColor=#ffffff;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430.25\&quot; y=\&quot;272.5\&quot; width=\&quot;84.5\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-16\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF9999;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-4\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-10\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-4\&quot; value=\&quot;Chains&amp;lt;br&amp;gt;链\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=none;rounded=1;fontStyle=1;fontSize=14;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;237.5\&quot; y=\&quot;170\&quot; width=\&quot;84.5\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-17\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF9999;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-7\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-7\&quot; value=\&quot;Prompts&amp;lt;br&amp;gt;提示\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;rounded=1;fontStyle=1;fontSize=14;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430.25\&quot; y=\&quot;340\&quot; width=\&quot;84.5\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-32\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-8\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-25\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;282\&quot; y=\&quot;515\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-8\&quot; value=\&quot;Document Loader &amp;amp;amp; Utils\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;rounded=1;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;206.82\&quot; y=\&quot;450\&quot; width=\&quot;149.38\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-9\&quot; value=\&quot;Memory&amp;lt;br&amp;gt;记忆\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=none;rounded=1;fontColor=#ffffff;fontStyle=1;fontSize=14;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;80\&quot; y=\&quot;272.5\&quot; width=\&quot;107.75\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-10\&quot; value=\&quot;Agents&amp;lt;br&amp;gt;代理\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=none;rounded=1;fontColor=#ffffff;fontStyle=1;fontSize=14;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;80\&quot; y=\&quot;170\&quot; width=\&quot;84.5\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-11\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=1;entryY=1;entryDx=0;entryDy=0;exitX=0;exitY=0;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-1\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-10\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;297.5\&quot; y=\&quot;285\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;330.5\&quot; y=\&quot;215\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-12\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-1\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-9\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;220\&quot; y=\&quot;290\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;182.5\&quot; y=\&quot;245\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-13\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-33\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-8\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;260.5\&quot; y=\&quot;303\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;192.5\&quot; y=\&quot;255\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0;entryDx=0;entryDy=0;exitX=1;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-1\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-7\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;270.5\&quot; y=\&quot;313\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;202.5\&quot; y=\&quot;265\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-19\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-18\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-9\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-48\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.409;entryY=0;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-18\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-41\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-18\&quot; value=\&quot;Vectorstores\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;rounded=1;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;80\&quot; y=\&quot;450\&quot; width=\&quot;107.75\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-20\&quot; value=\&quot;GPT 3.5\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;rounded=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;816.13\&quot; y=\&quot;225\&quot; width=\&quot;73.87\&quot; height=\&quot;25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-21\&quot; value=\&quot;GPT 4\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;rounded=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;816.13\&quot; y=\&quot;255\&quot; width=\&quot;73.87\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-22\&quot; value=\&quot;Claude\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;rounded=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;816.13\&quot; y=\&quot;285\&quot; width=\&quot;73.87\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-23\&quot; value=\&quot;ChatGLM\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;rounded=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;816.13\&quot; y=\&quot;322.5\&quot; width=\&quot;73.87\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-25\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#E6E6E6;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;414\&quot; y=\&quot;435\&quot; width=\&quot;222.25\&quot; height=\&quot;65\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-26\&quot; value=\&quot;Text\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;426.25\&quot; y=\&quot;443\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-27\&quot; value=\&quot;Image\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;496.38\&quot; y=\&quot;443\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-28\&quot; value=\&quot;Word\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;426.25\&quot; y=\&quot;473\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-29\&quot; value=\&quot;PDF\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;496.38\&quot; y=\&quot;473\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-30\&quot; value=\&quot;Video\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;566.25\&quot; y=\&quot;443\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-31\&quot; value=\&quot;Url\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;566.25\&quot; y=\&quot;473\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-35\&quot; value=\&quot;记忆类型&amp;lt;br&amp;gt;① short term: buffer&amp;lt;br&amp;gt;② long term: Entity&amp;lt;br&amp;gt;组件类型&amp;lt;br&amp;gt;① 全部对话内容&amp;lt;br&amp;gt;② 最近k轮&amp;lt;br&amp;gt;③ 内容摘要&amp;lt;br&amp;gt;④ 匹配最相似的k组\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;20.25\&quot; y=\&quot;292.5\&quot; width=\&quot;130\&quot; height=\&quot;130\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-36\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-1\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-33\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;280\&quot; y=\&quot;313\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;280\&quot; y=\&quot;450\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-33\&quot; value=\&quot;Indexes&amp;lt;br&amp;gt;索引\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=none;rounded=1;fontStyle=1;fontSize=14;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;239.26\&quot; y=\&quot;375\&quot; width=\&quot;84.5\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-37\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-33\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-18\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;292\&quot; y=\&quot;420\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;292\&quot; y=\&quot;460\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-38\&quot; value=\&quot;组件&amp;lt;br&amp;gt;① Document Loader&amp;lt;br&amp;gt;② Vector Stores&amp;lt;br&amp;gt;③ Text Splitters&amp;lt;br&amp;gt;④ Retrievers\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;330.13\&quot; y=\&quot;353\&quot; width=\&quot;130\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-39\&quot; value=\&quot;任务链&amp;lt;br&amp;gt;① Simple Chain（模板）&amp;lt;br&amp;gt;② Sequential Chain&amp;lt;br&amp;gt;③ 与外部数据&amp;lt;br&amp;gt;④ 与长期记忆\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;245\&quot; y=\&quot;80\&quot; width=\&quot;160\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-40\&quot; value=\&quot;Autonomus Chains&amp;lt;br&amp;gt;① Tools + Agents&amp;lt;br&amp;gt;② BabyAGI, AutoGPT\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;47.74999999999999\&quot; y=\&quot;200\&quot; width=\&quot;140\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-41\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#E6E6E6;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;43\&quot; y=\&quot;520\&quot; width=\&quot;222.25\&quot; height=\&quot;65\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-42\&quot; value=\&quot;FAISS\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;55.25\&quot; y=\&quot;528\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-43\&quot; value=\&quot;ES\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;125.38\&quot; y=\&quot;528\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-44\&quot; value=\&quot;Pinecone\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;55.25\&quot; y=\&quot;558\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-45\&quot; value=\&quot;Chroma\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;125.38\&quot; y=\&quot;558\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-46\&quot; value=\&quot;Milvus\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;195.25\&quot; y=\&quot;528\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-47\&quot; value=\&quot;PGVector\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;195.25\&quot; y=\&quot;558\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-49\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#E6E6E6;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;514.75\&quot; y=\&quot;123.75\&quot; width=\&quot;222.25\&quot; height=\&quot;65\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-50\&quot; value=\&quot;Google\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;527\&quot; y=\&quot;131.75\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-51\&quot; value=\&quot;Wolfram\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;597.13\&quot; y=\&quot;131.75\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-52\&quot; value=\&quot;Wikipedia\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;527\&quot; y=\&quot;161.75\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-53\&quot; value=\&quot;API\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;597.13\&quot; y=\&quot;161.75\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-54\&quot; value=\&quot;Youtube\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;667\&quot; y=\&quot;131.75\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-55\&quot; value=\&quot;Web\&quot; style=\&quot;whiteSpace=wrap;html=1;rounded=1;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;667\&quot; y=\&quot;161.75\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-56\&quot; value=\&quot;Tools\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;rounded=1;fontStyle=0;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;375.63\&quot; y=\&quot;138.75\&quot; width=\&quot;84.5\&quot; height=\&quot;35\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-58\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-56\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-49\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;483\&quot; y=\&quot;283\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;483\&quot; y=\&quot;245\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-59\&quot; value=\&quot;六大组件：Models、Prompts、Indexes、Memory、Chains、Agents\&quot; style=\&quot;text;fontColor=default;labelBackgroundColor=none;fontSize=12;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;500\&quot; y=\&quot;80\&quot; width=\&quot;366.24\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-61\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;RI6usgfjZI69E3hADuvV-2\&quot; target=\&quot;RI6usgfjZI69E3hADuvV-60\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;515\&quot; y=\&quot;290\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;626\&quot; y=\&quot;290\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-60\&quot; value=\&quot;LLMs\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;rounded=1;fontStyle=0;fontSize=14;shadow=0;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;600.75\&quot; y=\&quot;276.5\&quot; width=\&quot;60.63\&quot; height=\&quot;27.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-62\&quot; value=\&quot;Chat Models\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;rounded=1;fontStyle=0;fontSize=14;shadow=0;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;597\&quot; y=\&quot;235\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-63\&quot; value=\&quot;Text Embedding\&quot; style=\&quot;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;rounded=1;fontStyle=0;fontSize=14;shadow=0;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;597\&quot; y=\&quot;318.75\&quot; width=\&quot;110\&quot; height=\&quot;27.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-65\&quot; value=\&quot;顺序确定\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#FF0000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;300\&quot; y=\&quot;200\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-66\&quot; value=\&quot;改进：不定\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#FF0000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;165\&quot; y=\&quot;158.75\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-67\&quot; value=\&quot;组成&amp;lt;br&amp;gt;① Action执行操作&amp;lt;br&amp;gt;② Observation 收到的信息&amp;lt;br&amp;gt;③ Decision 决策\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;25.25\&quot; y=\&quot;68.75\&quot; width=\&quot;170\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;RI6usgfjZI69E3hADuvV-68\&quot; value=\&quot;wangqiwen&amp;#xa;2023-7-19\&quot; style=\&quot;text;fontColor=default;labelBackgroundColor=none;fontSize=12;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;476.5\&quot; y=\&quot;533.75\&quot; width=\&quot;69.75\&quot; height=\&quot;37.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


### Document Loaders and Utils

LangChain 的 Document Loaders 和 Utils 模块分别用于**连接到数据源**和**计算源**。

当使用loader加载器读取到数据源后，数据源需要转换成 Document 对象后，后续才能进行使用。

Document Loaders 的Unstructured 可以将这些原始数据源转换为可处理的文本。

The following document loaders are provided:
- `CSV` Loader CSV文件
- `DataFrame` Loader 从 pandas 数据帧加载数据
- `Diffbot` 从 URL 列表中提取 HTML 文档，并将其转换为我们可以在下游使用的文档格式
- `Directory` Loader 加载目录中的所有文档
- `EverNote` 印象笔记
- `Git` 从 Git 存储库加载文本文件
- `Google Drive` Google网盘
- `HTML` HTML 文档
- `Markdown`
- `Notebook` 将 .ipynb 笔记本中的数据加载为适合 LangChain 的格式
- `Notion`
- `PDF`
- `PowerPoint`
- `Unstructured File` Loader 使用Unstructured加载多种类型的文件，目前支持加载文本文件、powerpoints、html、pdf、图像等
- `URL` 加载 URL 列表中的 HTML 文档内容
- `Word Documents`

### Text Spltters

文本分割用来分割文本。

为什么需要分割文本？
- 因为每次不管把文本当作 prompt 发给 openai api ，还是使用 embedding 功能, 都是有**字符限制**的。

将一份300页的 pdf 发给 openai api，进行总结，肯定会报超过最大 Token 错。所以需要用文本分割器去分割 loader 进来的 Document。
- 默认推荐的文本拆分器是 `RecursiveCharacterTextSplitter`
- 默认情况以 [“\n\n”, “\n”, “ “, “”] 字符进行拆分。
- 其它参数说明：
  - `length_function` 如何计算块的长度。默认只计算字符数，但在这里传递令牌计数器是很常见的。
  - `chunk_size`：块的最大大小（由长度函数测量）。
  - `chunk_overlap`：块之间的最大重叠。有一些重叠可以很好地保持块之间的一些连续性（例如，做一个滑动窗口）
- `CharacterTextSplitter` 默认情况下以 separator="\n\n"进行拆分
- `TiktokenText Splitter` 使用OpenAI 的开源分词器包来估计使用的令牌

```py
# This is a long document we can split up.
with open('../../../state_of_the_union.txt') as f:
    state_of_the_union = f.read()
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(        
    separator = "\n\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
metadatas = [{"document": 1}, {"document": 2}]
documents = text_splitter.create_documents([state_of_the_union, state_of_the_union], metadatas=metadatas)
print(texts[0])
```

```py
# This is a long document we can split up.
with open('../../../state_of_the_union.txt') as f:
    state_of_the_union = f.read()
from langchain.text_splitter import TokenTextSplitter
text_splitter = TokenTextSplitter(chunk_size=10, chunk_overlap=0)
texts = text_splitter.split_text(state_of_the_union)
print(texts[0])
```

### LangChain Embedding

模型拉到本地使用的好处：
- 训练模型
- 可用本地的 GPU
- 有些模型无法在 HuggingFace 运行

LangChain Embedding示例
- HuggingFace

```py
from langchain.embeddings import HuggingFaceEmbeddings 

embeddings = HuggingFaceEmbeddings() 
text = "This is a test document." 
query_result = embeddings.embed_query(text) 
doc_result = embeddings.embed_documents([text])
```

- llama-cpp

```py
# !pip install llama-cpp-python
from langchain.embeddings import LlamaCppEmbeddings

llama = LlamaCppEmbeddings(model_path="/path/to/model/ggml-model-q4_0.bin")
text = "This is a test document."
query_result = llama.embed_query(text)
doc_result = llama.embed_documents([text])
```

- OpenAI

```py
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
text = "This is a test document."
query_result = embeddings.embed_query(text)
doc_result = embeddings.embed_documents([text])
```


### （1）Models（模型）：LLM选择

LangChain 本身不提供 LLM，提供通用的接口访问 LLM，可以很方便的更换底层的 LLM 以及自定义自己的 LLM。

`Models`（模型）: 可选择不同的LLM与Embedding模型。可以直接调用 API 工作，也可以运行本地模型。
- `LLMs`（大语言模型）: 接收文本字符作为输入，返回的也是文本字符，类似 OpenAI 的 text-davinci-003
- `Chat Models` 聊天模型: 由语言模型支持但将聊天消息列表作为输入并返回聊天消息的模型。一般使用的 ChatGPT 以及 Claude 为 Chat Models。
  - 聊天模型基于LLMs，不同的是它接收聊天消息作为输入，返回的也是聊天消息
  - 聊天消息是一种特定格式的数据，LangChain中支持四种消息: `AIMessage`,` HumanMessage`,` SystemMessage` ,`ChatMessage` ，需要按照角色把数据传递给模型，这部分在后面文章里再详细解释。
- `Text Embedding`：用于文本的向量化表示。文本嵌入模型接收文本作为输入，返回的是浮点数列表. 设计用于与嵌入交互的类
  - 用于实现基于知识库的问答和semantic search，相比 fine-tuning 最大的优势：不用进行训练，并且可以实时添加新的内容，而不用加一次新的内容就训练一次，并且各方面成本要比 fine-tuning 低很多。
  - 例如，可调用OpenAI、Cohere、HuggingFace等Embedding标准接口，对文本向量化。
  - 两个方法：`embed_documents` 和 `embed_query`。最大区别在于接口不同：一种处理**多**个文档，而另一种处理**单**个文档。
  - 文本嵌入模型集成了如下的源：AzureOpenAI、Hugging Face Hub、InstructEmbeddings、Llama-cpp、OpenAI 等
- HuggingFace Models

大语言模型（LLMs）是Models的核心，也是LangChain的基础组成部分，LLMs本质上是一个大型语言模型的包装器，通过该接口与各种大模型进行交互。
- 这些模型包括OpenAI的GPT-3.5/4、谷歌的LaMDA/PaLM，Meta AI的LLaMA等。

LLMs 类的功能如下：
- 支持多种模型接口，如 OpenAI、Hugging Face Hub、Anthropic、Azure OpenAI、GPT4All、Llama-cpp…
- Fake LLM，用于测试
- 缓存的支持，比如 in-mem（内存）、SQLite、Redis、SQL
- 用量记录
- 支持流模式（就是一个字一个字的返回，类似打字效果）

LangChain调用OpenAI的gpt-3.5-turbo大语言模型的简单示例

```py
import os
from langchain.llms import OpenAI

openai_api_key = 'sk-******'
os.environ['OPENAI_API_KEY'] = openai_api_key

llm = OpenAI(model_name="gpt-3.5-turbo")
# llm = OpenAI(model_name="text-davinci-003", n=2, best_of=2)
print(llm("讲个笑话，很冷的笑话"))
# 为什么鸟儿会成为游泳高手？因为它们有一只脚比另一只脚更长，所以游起泳来不费力！（笑）
llm_result = llm.generate(["Tell me a joke", "Tell me a poem"])
llm_result.llm_output    # 返回 tokens 使用量
# ----- 使用模板 -----
from langchain import PromptTemplate

prompt_template = '''作为一个资深编辑，请针对 >>> 和 <<< 中间的文本写一段摘要。 
>>> {text} <<<
'''
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
print(prompt.format_prompt(text="我爱北京天安门"))
```

#### 流式输出

流式输出
- LangChain在支持代理封装ChatGPT接口的基础上，也同样地把ChatGPT API接口的流式数据返回集成了进来

```py
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler # 流式
from langchain.schema import HumanMessage
# streaming
llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
resp = llm("Write me a song about sparkling water.")
```

#### 缓存

缓存LLM的结果
- 调用ChatGPT的API接口往往会存在网络延时的情况
- 为了更优雅的实现LLM语言生成模型，LangChain同时提供了数据缓存的接口如果用户问了**同样的问题**，LangChain支持直接将所缓存的数据直接响应

```py
import langchain
from langchain.cache import InMemoryCache # 启动缓存
langchain.llm_cache = InMemoryCache()

# To make the caching really obvious, lets use a slower model.
llm = OpenAI(model_name="text-davinci-002", n=2, best_of=2)
```

##### GPTCache

LLM 缓存工具
- [GPTCache : A Library for Creating Semantic Cache for LLM Queries](https://github.com/zilliztech/GPTCache)
- 支持 LangChain、Llama_index和OpenAI
- ![](https://github.com/zilliztech/GPTCache/raw/main/docs/GPTCacheStructure.png)

```py
# [GPTCache : A Library for Creating Semantic Cache for LLM Queries](https://github.com/zilliztech/GPTCache)
from gptcache import cache
from gptcache.adapter import openai

cache.init()
cache.set_openai_key()
```

#### 异步返回

异步返回
- 构建复杂的LLM模型调用链时，往往存在接口的**多次调用**，而且并不能保证接口的实时性返回
- 这时可以使用接口**异步返回**的模型来提升功能的服务质量，系统的性能

```py
import time
import asyncio # 异步

from langchain.llms import OpenAI

def generate_serially():
    llm = OpenAI(temperature=0.9)
    for _ in range(10):
        resp = llm.generate(["Hello, how are you?"])
        print(resp.generations[0][0].text)

async def async_generate(llm):
    resp = await llm.agenerate(["Hello, how are you?"])
    print(resp.generations[0][0].text)

async def generate_concurrently():
    llm = OpenAI(temperature=0.9)
    tasks = [async_generate(llm) for _ in range(10)]
    await asyncio.gather(*tasks)

s = time.perf_counter()
# If running this outside of Jupyter, use asyncio.run(generate_concurrently())
await generate_concurrently()
elapsed = time.perf_counter() - s
print('\033[1m' + f"Concurrent executed in {elapsed:0.2f} seconds." + '\033[0m')

s = time.perf_counter()
generate_serially()
elapsed = time.perf_counter() - s
print('\033[1m' + f"Serial executed in {elapsed:0.2f} seconds." + '\033[0m')
```

#### 多模型融合

整合多个模型
- 作为LangChain中的核心模块，LangChain不止支持简单的LLM，从简单的文本生成功能、会话聊天功能以及文本向量化功能均集成，并且将其封装成一个一个的链条节点
- （1）大语言模型
- （2）聊天模型: OpenAI所提供的多角色聊天，允许用户设定信息归属不同的角色，从而丰富用户的聊天背景，构造出更加拟人化的聊天效果
- （3）语言向量化模型

OpenAI

```py
import os
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
# 模板解析
template = """Question: {question}
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])

llm = OpenAI()
llm_chain = LLMChain(prompt=prompt, llm=llm)
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
llm_chain.run(question)
```

角色设置

```py
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

chat = ChatOpenAI(temperature=0)

messages = [
    SystemMessage(content="You are a helpful assistant that translates English to French."),
    HumanMessage(content="Translate this sentence from English to French. I love programming.")
]
chat(messages)
```

模板化编排

```py
template="You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template="{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# get a chat completion from the formatted messages
chat(chat_prompt.format_prompt(input_language="English", output_language="French", text="I love programming.").to_messages())
```

Azure OpenAI

```py
import os
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2022-12-01"
os.environ["OPENAI_API_BASE"] = "..."
os.environ["OPENAI_API_KEY"] = "..."
# Import Azure OpenAI
from langchain.llms import AzureOpenAI
# Create an instance of Azure OpenAI
# Replace the deployment name with your own
llm = AzureOpenAI(
    deployment_name="td2",
    model_name="text-davinci-002",
)
# Run the LLM
llm("Tell me a joke")
```

Hugging Face Hub

```py
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

from langchain import HuggingFaceHub

repo_id = "google/flan-t5-xl" # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature":0, "max_length":64})

from langchain import PromptTemplate, LLMChain

template = """Question: {question}
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)
question = "Who won the FIFA World Cup in the year 1994? "
print(llm_chain.run(question))
```

### （2）Prompts（提示语）: 模板化

通常作为输入传递给模型的信息被称为`提示`
- 提示可以是**文本字符**，也可以是**文件**、**图片**甚至**视频**
- LangChain目前只支持字符形式的提示。

提示一般不是**硬编码**的形式写在代码里，而是由`模板`和`用户输入`来生成，LangChain提供多个类和方法来构建提示。
- `提示模板`
  - 提示模板是一种生成提示的方式，包含一个带有可替换内容的模板，从用户那获取一组参数并生成提示
  - 提示模板用来生成LLMs的提示，最简单的使用场景，比如“我希望你扮演一个代码专家的角色，告诉我这个方法的原理{code}”。
- `聊天提示模板`
  - 聊天模型接收聊天消息作为输入，再次强调聊天消息和普通字符是不一样的，聊天提示模板的作用就是为聊天模型生成提示
- `示例选择器`
  - 示例选择器是一个高级版的数据筛选器
- `输出解析器`
  - 由于模型返回的是文本字符，输出解析器可以把文本转换成结构化数据

Prompts（提示语）: 管理LLM输入
- PromptTemplate 负责构建此输入
- LangChain 提供了可用于格式化输入和许多其他实用程序的提示模板。

当用户与大语言模型对话时，用户内容即Prompt（提示语）。
- 如果用户每次输入的Prompt中包含大量的重复内容，生成一个**Prompt模板**，将通用部分提取出来，用户输入输入部分作为变量。

Prompt模板十分有用
- 利用langchain构建专属**客服助理**，并且明确告诉其只回答**知识库**（产品介绍、购买流程等）里面的知识，其他无关的询问，只回答“我还没有学习到相关知识”。
- 这时可利用Prompt模板对llm进行约束。

调用LangChain的PromptTemplate

```py
from langchain import PromptTemplate

# 【无变量模板】An example prompt with no input variables
no_input_prompt = PromptTemplate(input_variables=[], template="Tell me a joke.")
no_input_prompt.format()
# -> "Tell me a joke."
# ① 【有变量模板】
name_template = """
我想让你成为一个起名字的专家。给我返回一个名字的名单. 名字寓意美好，简单易记，朗朗上口.
关于{name_description},好听的名字有哪些?
"""
# 创建一个prompt模板
prompt_template = PromptTemplate(input_variables=["name_description"], template=name_template)
description = "男孩名字"
print(prompt_template.format(name_description=description))
# 我想让你成为一个起名字的专家。给我返回一个名字的名单. 名字寓意美好，简单易记，朗朗上口.关于男孩名字,好听的名字有哪些?
# ②【多变量模板】
# An example prompt with multiple input variables
multiple_input_prompt = PromptTemplate(
    input_variables=["adjective", "content"],
    template="Tell me a {adjective} joke about {content}."
)
multiple_input_prompt.format(adjective="funny", content="chickens")
# -> "Tell me a funny joke about chickens."
```

提出多个问题，两种方法： 
1. 使用generate方法遍历所有问题，逐个回答。
2. 将所有问题放入单个提示中，这仅适用于更高级的LLMs。

```py
# ③ 【多输入】
qs = [ # Text only
    {'question': "Which NFL team won the Super Bowl in the 2010 season?"},
    {'question': "If I am 6 ft 4 inches, how tall am I in centimeters?"},
    {'question': "Who was the 12th person on the moon?"},
    {'question': "How many eyes does a blade of grass have?"}
]
res = llm_chain.generate(qs)
# res = LLMResult(generations = [[Generation(text ='green bay packers', generation_info = None)], [Generation(text ='184', generation_info = None)], [Generation(text ='john glenn', generation_info = None)], [Generation(text ='one', generation_info = None)]], llm_output = None)
```

FewShot PromptTemplate
- 模板可以根据语料库中的内容进行匹配，最终可按照特定的格式匹配出**样例**中的内容。

```py
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate

examples = [
  {
    "question": "Who lived longer, Muhammad Ali or Alan Turing?",
    "answer":
"""
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali
"""
  },
  {
    "question": "When was the founder of craigslist born?",
    "answer":
"""
Are follow up questions needed here: Yes.
Follow up: Who was the founder of craigslist?
Intermediate answer: Craigslist was founded by Craig Newmark.
Follow up: When was Craig Newmark born?
Intermediate answer: Craig Newmark was born on December 6, 1952.
So the final answer is: December 6, 1952
"""
  }
]

example_prompt = PromptTemplate(input_variables=["question", "answer"], template="Question: {question}\n{answer}")
print(example_prompt.format(**examples[0]))
```

```s
=========================
Question: Who lived longer, Muhammad Ali or Alan Turing?

Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali
```


### （3）Indexes（索引）：文档结构化

`Indexes`（索引）：文档结构化方式, 以便LLM更好的交互
- 索引是指对文档进行结构化的方法，以便LLM能够更好的与之交互。

最常见的使用场景是**文档检索**，接收用户查询，返回最相关的文档。
- 注意: 索引也能用在除了检索外的其他场景，同样检索除了索引外也有其他的实现方式。

索引一般和检索**非结构化数据**（比如文本文档）相关，LangChain支持的主要索引类型如下，都是围绕着**向量数据库**的。

该组件主要包括：Document Loaders（`文档加载器`）、Text Splitters（`文本拆分器`）、VectorStores（`向量存储器`）以及Retrievers（`检索器`）。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/5078c23e1fea4bee99746ebec0847be5~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=Uzl65uwWtcvNhfi1OHpX8u%2BGzko%3D)
- ![](https://pic1.zhimg.com/80/v2-caf733f8f1cc6e8c45aa7dc8f81f2f12_1440w.webp?source=1940ef5c)
- `文本检索器`：将特定格式数据转换为文本。输入可以是 pdf、word、csv、images 等。
- `文本拆分器`：将长文本拆分成小的**文本块**，便于LLM模型处理。
  - 由于模型处理数据时，对输入长度有限制，因此需要对长文本进行**分块**。
  - 不同语言模型对块的大小定义不同，比如OpenAI的GPT对分块的长度通过token大小来限制，比如GPT-3.5是**4096**，即这个分块所包含的Token数量不能超过4096。
  - 一般的分块方法：首先，对长文本进行**断句**，即分成一句一句话。然后，计算每句话包含的token数量，并从第一句话开始往后依次累加，直到达到指定数量，组成为1个分块。依次重复上述操作。比如按照**字母**切分的`Character`，按照**token**切分的`Tiktoken`等。
- `向量存储器`：存储提取的文本向量，包括Faiss、Milvus、Pinecone、Chroma等。
- `向量检索器`：通过用户输入的文本，检索器负责从底库中检索出特定相关度的文档。度量准则包括余弦距离、欧式距离等。

#### Document Loaders（文档加载器）

LangChain 通过 Loader 加载外部的文档，转化为标准的 **Document** 类型。

Document 类型主要包含两个属性：
- page_content 包含该文档的内容。
- meta_data 为文档相关的描述性数据，类似文档所在的路径等。

LangChain 目前支持结构化、非结构化以及公开以及私有的各种数据
- ![](https://picx.zhimg.com/80/v2-254f055f57dbc6e6b5efd8bf03c8a92b_1440w.webp?source=1940ef5c)

||非结构化 unstructed|结构化 structured|
|---|---|---|
|公开 public|Wikipedia, youtube, bilibili, arXiv, twitter, imdb...|Huggingface Datasets, OpenWeather|
|私有 proprietary|ppt,word, Note, snapchat, github, jupyter..|excel,pandas,spark...|

注
- 数据库介于私有区，既有结构化(mysql)又有非结构化(redis,es..)

数据源加载

```py
# 🎨 加载B站（BiliBili）视频数据
#!pip install bilibili-api
from langchain.document_loaders.bilibili import BiliBiliLoader
loader = BiliBiliLoader(
    ["https://www.bilibili.com/video/BV1xt411o7Xu/"]
)
loader.load()

# 🎨 加载CSV数据
from langchain.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(file_path='./example_data/mlb_teams_2012.csv')

data = loader.load()

# 🎨 加载Email数据
#!pip install unstructured
from langchain.document_loaders import UnstructuredEmailLoader
loader = UnstructuredEmailLoader('example_data/fake-email.eml')
data = loader.load()

# 🎨 加载电子书Epub数据
#!pip install pandocs
from langchain.document_loaders import UnstructuredEPubLoader
loader = UnstructuredEPubLoader("winter-sports.epub", mode="elements")
data = loader.load()

# 🎨 加载Git数据
# !pip install GitPython

from git import Repo
repo = Repo.clone_from(
    "https://github.com/hwchase17/langchain", to_path="./example_data/test_repo1"
)
branch = repo.head.reference

from langchain.document_loaders import GitLoader
loader = GitLoader(repo_path="./example_data/test_repo1/", branch=branch)
data = loader.load()

# 🎨 加载HTML数据
from langchain.document_loaders import UnstructuredHTMLLoader

loader = UnstructuredHTMLLoader("example_data/fake-content.html")

data = loader.load()

# 🎨 加载Image图片数据
#!pip install pdfminer

from langchain.document_loaders.image import UnstructuredImageLoader
loader = UnstructuredImageLoader("layout-parser-paper-fast.jpg")
data = loader.load()

# 🎨 加载Word文档数据
from langchain.document_loaders import Docx2txtLoader
loader = Docx2txtLoader("example_data/fake.docx")

data = loader.load()
# [Document(page_content='Lorem ipsum dolor sit amet.', metadata={'source': 'example_data/fake.docx'})]

# 🎨 加载PDF文件数据
# !pip install pypdf

from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("example_data/layout-parser-paper.pdf")
pages = loader.load_and_split()
pages[0]
```

#### Text Splitters（文本拆分器）

LLM 一般都会限制**上下文窗口的大小**，有 4k、16k、32k 等。针对大文本就需要进行文本分割，常用的文本分割器为 RecursiveCharacterTextSplitter，可以通过 separators 指定分隔符。其先通过第一个分隔符进行分割，不满足大小的情况下迭代分割。

文本分割主要有 2 个考虑：
- 1）将语义相关的句子放在一块形成一个 chunk。一般根据不同的文档类型定义不同的分隔符，或者可以选择通过模型进行分割。
- 2）chunk 控制在一定的大小，可以通过函数去计算。默认通过 len 函数计算，模型内部一般都是使用 token 进行计算。token 通常指的是将文本或序列数据划分成的小的单元或符号，便于机器理解和处理。使用 OpenAI 相关的大模型，可以通过 tiktoken 包去计算其 token 大小。

```py
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    model_name="gpt-3.5-turb
    allowed_special="all",
    separators=["\n\n", "\n", "。", "，"],
    chunk_size=7000,
    chunk_overlap=0
)
docs = text_splitter.create_documents(["文本在这里"])
print(docs)
```


示例

```py
# pip install chromadb
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
# 指定要使用的文档加载器
from langchain.document_loaders import TextLoader
documents = TextLoader('../state_of_the_union.txt', encoding='utf8')
# 接下来将文档拆分成块。
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
# 然后我们将选择我们想要使用的嵌入。
from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()
# 我们现在创建 vectorstore 用作索引。
from langchain.vectorstores import Chroma
db = Chroma.from_documents(texts, embeddings)
# 这就是创建索引。然后，我们在检索器接口中公开该索引。
retriever = db.as_retriever()
# 创建一个链并用它来回答问题！
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
query = "What did the president say about Ketanji Brown Jackson"
qa.run(query)
```

#### VectorStores（向量存储器）

通过 Text Embedding models，将文本转为**向量**，可以进行语义搜索，在向量空间中找到最相似的文本片段。
- 目前支持常用的向量存储有 Faiss、Chroma 等。
- Embedding 模型支持 OpenAIEmbeddings、HuggingFaceEmbeddings 等。通过 HuggingFaceEmbeddings 加载本地模型可以节省 embedding 的调用费用。

```py
#通过cache_folder加载本地模型
embeddings = HuggingFaceEmbeddings(model_name="text2vec-base-chinese", cache_folder="本地模型地址")
embeddings = embeddings_model.embed_documents(
    [
        "我爱北京天安门!",
        "Hello world!"
    ]
)
```

#### Retrievers（检索器）

Retriever 接口用于根据非结构化的查询获取文档，一般情况下是文档存储在向量数据库中。可以调用 get_relevant_documents 方法来检索与查询相关的文档。

**Retrievers**

检索器接口是一个通用接口，可以轻松地将文档与语言模型结合起来。
- 此接口公开了一个 get_relevant_documents 方法，该方法接受一个查询（一个字符串）并返回一个文档列表。

一般来说，用的都是 VectorStore Retriever。
- 此检索器由 VectorStore 大力支持。一旦你构造了一个 VectorStore，构造一个检索器就很容易了。

```py
# # pip install faiss-cpu
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import DirectoryLoader
# 加载文件夹中的所有txt类型的文件，并转成 document 对象
loader = DirectoryLoader('./data/', glob='**/*.txt')
documents = loader.load()
# 接下来，我们将文档拆分成块。
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
# 然后我们将选择我们想要使用的嵌入。
from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()
from langchain.vectorstores import FAISS
db = FAISS.from_documents(texts, embeddings)
query = "未入职同事可以出差吗"
docs = db.similarity_search(query)
docs_and_scores = db.similarity_search_with_score(query)
print(docs)

retriever = db.as_retriever()	# 最大边际相关性搜索 mmr
# retriever = db.as_retriever(search_kwargs={"k": 1})	# 搜索关键字
docs = retriever.get_relevant_documents("未入职同事可以出差吗")
print(len(docs))

# db.save_local("faiss_index")
# new_db = FAISS.load_local("faiss_index", embeddings)
# docs = new_db.similarity_search(query)
# docs[0]
```


### （4）Chains（链条）：组合链路

Langchain 通过 chain 将各个组件进行链接，以及 chain 之间进行链接，用于简化复杂应用程序的实现。

`Chains`（链条）：将LLM与其他组件结合, `链`允许将多个`组件`组合在一起以创建一个单一的、连贯的应用程序。
- 把一个个独立的组件链接在一起，LangChain名字的由来
- Chain 可理解为任务。一个 Chain 就是一个任务，也可以像链条一样，逐个执行多个链

Chain提供了一种将各种组件统一到应用程序中的方法。
- 例如，创建一个Chain，接受来自用户的输入，并通过PromptTemplate将其格式化，然后将格式化的输出传入到LLM模型中。
- 通过多个Chain与其他部件结合，可生成复杂的链，完成复杂的任务。
- ![Chains示意图](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/4d5ba1c00889406fb3bc7c86fbb9660f~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=pLKYIarzSV1QkVxKv%2Blc0t8lDrE%3D)

LangChain中，主要有下面几种链，`LLMChain`、`Sequential Chain` 以及 `Route Chain`，其中最常用的是LLMChain。
- `LLMChain` 最基本的链
  - LLMChain由 **PromptTemplate**、**模型**和可选的**输出解析器**组成。
  - 链接收多个输入变量，使用PromptTemplate生成提示，传递给模型，最后使用输出解析器把模型返回值转换成最终格式。
  - ![](https://picx.zhimg.com/80/v2-774b73df8d40ecc40ea265c5f15fd40d_1440w.webp?source=1940ef5c)
- `索引相关链`
  - 和索引交互，把自己的数据和LLMs结合起来，最常见的例子是根据文档来回答问题。
- `提示选择器`
  - 为不同模型生成不同的提示

LLM与其他组件结合，创建不同应用，一些例子：
- 将LLM与**提示模板**相结合
- 第一个 LLM 的输出作为第二个 LLM 的输入, **顺序组合**多个 LLM
- LLM与**外部数据**结合，比如，通过langchain获取youtube视频链接，通过LLM视频问答
- LLM与**长期记忆**结合，比如聊天机器人

#### LLMChain

LLMChain，由 PromptTemplate、LLM 和 OutputParser 组成。LLM 的输出一般为文本，OutputParser 用于让 LLM 结构化输出并进行结果解析，方便后续的调用。
- ![](https://picx.zhimg.com/80/v2-774b73df8d40ecc40ea265c5f15fd40d_1440w.webp?source=1940ef5c)

```py
from langchain import LLMChain

llm_chain = LLMChain(prompt=prompt, llm=llm)
question = "Can Barack Obama have a conversation with George Washington?"
print(llm_chain.run(question))
```

LLMChain是一个简单的链，它接受一个提示模板，用用户输入格式化它并返回来自 LLM 的响应。

```py
from langchain.llms import OpenAI
from langchain.docstore.document import Document
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
import pathlib
import subprocess
import tempfile
"""
生成对以前撰写的博客文章有理解的博客文章，或者可以参考产品文档的产品教程
"""

source_chunks = ""
search_index = Chroma.from_documents(source_chunks, OpenAIEmbeddings())

from langchain.chains import LLMChain
prompt_template = """Use the context below to write a 400 word blog post about the topic below:
    Context: {context}
    Topic: {topic}
    Blog post:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "topic"]
)

llm = OpenAI(temperature=0)

chain = LLMChain(llm=llm, prompt=PROMPT)

def generate_blog_post(topic):
    docs = search_index.similarity_search(topic, k=4)
    inputs = [{"context": doc.page_content, "topic": topic} for doc in docs]
    print(chain.apply(inputs))
generate_blog_post("environment variables")
# 附加示例
llm_chain = LLMChain(prompt=prompt, llm=llm)
comment = "京东物流没的说，速度态度都是杠杠滴！这款路由器颜值贼高，怎么说呢，就是泰裤辣！这线条，这质感，这速度，嘎嘎快！以后妈妈再也不用担心家里的网速了！"
result = llm_chain.run(comment)
data = output_parser.parse(result)
print(f"type={type(data)}, keyword={data['keyword']}, emotion={data['emotion']}")
```

#### Sequential Chain (一串LLMChain)

SequentialChains 按**预定义顺序**执行的链。SimpleSequentialChain 为顺序链的最简单形式，其中每个步骤都有一个单一的输入 / 输出，一个步骤的输出是下一个步骤的输入。SequentialChain 为顺序链更通用的形式，允许多个输入 / 输出。

执行多个 LLMChain
- 顺序链是按预定义顺序执行其链接的链。
- 使用SimpleSequentialChain，其中每个步骤都有一个输入/输出，一个步骤的输出是下一个步骤的输入。

```py
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain

# location 链
llm = OpenAI(temperature=1)
template = """Your job is to come up with a classic dish from the area that the users suggests.
% USER LOCATION
{user_location}

YOUR RESPONSE:
"""
prompt_template = PromptTemplate(input_variables=["user_location"], template=template)
location_chain = LLMChain(llm=llm, prompt=prompt_template)

# meal 链
template = """Given a meal, give a short and simple recipe on how to make that dish at home.
% MEAL
{user_meal}

YOUR RESPONSE:
"""
prompt_template = PromptTemplate(input_variables=["user_meal"], template=template)
meal_chain = LLMChain(llm=llm, prompt=prompt_template)

# 通过 SimpleSequentialChain 串联起来，第一个答案会被替换第二个中的user_meal，然后再进行询问
overall_chain = SimpleSequentialChain(chains=[location_chain, meal_chain], verbose=True)
review = overall_chain.run("Rome")
```

#### Router Chain

RouterChain 根据输入**动态**选择下一个链，每条链处理特定类型的输入。

RouterChain 由两个组件组成：
- 1）**路由器链**本身，负责选择要调用的下一个链，主要有 2 种 RouterChain，其中 LLMRouterChain 通过 LLM 进行路由决策，EmbeddingRouterChain 通过向量搜索的方式进行路由决策。
- 2）**目标链**列表，路由器链可以路由到的子链。

初始化 RouterChain 以及 destination_chains 完成后，通过 MultiPromptChain 将两者结合起来使用。
- ![](https://picx.zhimg.com/80/v2-1cfc7dc754e42035aaac96d982e72f83_1440w.webp?source=1940ef5c)


#### Documents Chain

下面4 种 Chain 主要用于 **Document 处理**，在基于文档生成摘要、基于文档的问答等场景中经常会用到，在后续的落地实践里也会有所体现。
- ![](https://pica.zhimg.com/80/v2-48163d2a9246b271491e96fd29e17256_1440w.webp?source=1940ef5c)

##### Stuff

StuffDocumentsChain 最简单直接，是将所有获取到的文档作为 context 放入到 Prompt 中，传递到 LLM 获取答案。

这种方式可以**完整保留上下文**，调用 LLM 的次数也比较少，建议能使用 stuff 的就使用这种方式。其适合文档拆分的比较小，一次获取文档比较少的场景，不然容易超过 token 的限制。
- ![](https://picx.zhimg.com/80/v2-5012639aaddebf3ded6bc275e0e9b26f_1440w.webp?source=1940ef5c)

##### Refine

RefineDocumentsChain 是通过**迭代更新**方式获取答案。先处理第一个文档，作为 context 传递给 llm，获取中间结果 intermediate answer。然后将第一个文档的中间结果以及第二个文档发给 llm 进行处理，后续的文档类似处理。

Refine 这种方式能部分保留上下文，以及 token 的使用能控制在一定范围。
- ![](https://pica.zhimg.com/80/v2-58114a41deaa562d13d627ee750dc0b7_1440w.webp?source=1940ef5c)

##### MapReduce

MapReduceDocumentsChain 先通过 LLM 对每个 document 进行处理，然后将所有文档的答案在通过 LLM 进行合并处理，得到最终的结果。

MapReduce 的方式将每个 document 单独处理，可以并发进行调用。但是每个文档之间缺少上下文。
- ![](https://picx.zhimg.com/80/v2-8774dd34362cdafec7ef5a71f1e0ebb6_1440w.webp?source=1940ef5c)

##### MapRerank

MapRerankDocumentsChain 和 MapReduceDocumentsChain 类似，先通过 LLM 对每个 document 进行处理，每个答案都会返回一个 score，最后选择 score 最高的答案。

MapRerank 和 MapReduce 类似，会大批量的调用 LLM，每个 document 之间是独立处理。
- ![](https://pic1.zhimg.com/80/v2-db2b87a6d0f49fd5fe8e03fb358ade7a_1440w.webp?source=1940ef5c)


### （5）Agents（智能体）：其他工具

“链”可以帮助将一系列 LLM 调用链接在一起。然而，在某些任务中，调用顺序通常是**不确定**的。
- 有些应用并不是一开始就确定调用哪些模型，而是依赖于用户输入

LangChain 库提供了代理“Agents”，根据**未知**输入而不是**硬编码**来决定下一步采取的行动。 

Agent 字面含义是**代理**，如果说 LLM 是大脑，Agent 就是代理大脑使用工具 Tools。

目前大模型一般都存在**知识过时**、**逻辑计算能力低**等问题，通过 Agent 访问工具，可以去解决这些问题。这个领域特别活跃，诞生了类似 `AutoGPT`、`BabyAGI`、`AgentGPT` 等一堆优秀的项目。传统使用 LLM，需要给定 Prompt 一步一步的达成目标，通过 Agent 是给定目标，其会自动规划并达到目标。

Agents通常由三个部分组成：`Action`、`Observation`和`Decision`。
- `Action`是代理执行的操作
- `Observation`是代理接收到的信息
- `Decision`是代理基于`Action`和`Observation`做出的决策。

#### Agent 核心组件

Agent 核心组件
- `Agent`：**代理**，负责调用 LLM 以及决定下一步的 Action。其中 LLM 的 prompt 必须包含 agent_scratchpad 变量，记录执行的中间过程
- `Tools`：**工具**，Agent 可以调用的方法。LangChain 已有很多内置的工具，也可以自定义工具。注意 Tools 的 description 属性，LLM 会通过描述决定是否使用该工具。
- `ToolKits`：**工具集**，为特定目的的工具集合。类似 Office365、Gmail 工具集等
- `Agent Executor`：**Agent 执行器**，负责进行实际的执行。

Agent 使用LLM来确定要采取哪些行动以及按什么顺序采取的行动。操作可以使用工具并观察其输出，也可以返回用户。

创建agent时的参数：
- `LLM`：为代理提供动力的语言模型。
- `工具`：执行特定职责的功能, 方便模型和其他资源交互
  - 比如：Google搜索，数据库查找，Python Repl。工具的接口当前是一个函数，将字符串作为输入，字符串作为输出。
- `工具集`
  - 解决特定问题的工具集合
- `代理`：highest level API、custom agent. 要使用的代理。围绕模型的包装器，接收用户输入，决定模型的行为
- `代理执行器`
  - 代理和一组工具，调用代理

```py
# Create RetrievalQA Chain
from langchain.chains import RetrievalQA
retrieval_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())

# Create an Agent
from langchain.agents import initialize_agent, Tool

tools = [
    Tool(
        name="Example QA System",
        func=retrieval_qa.run,
        description="Example description of the tool."
    ),
]
# Agent 的初始化, 除了 llm、tools 等参数，还需要指定 AgentType。
# 通过 agent.agent.llm_chain.prompt.template 方法，获取其推理决策所使用的模板
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Use Agent
agent.run("Ask a question related to the documents")
```

#### Agent 的类型

Agent Type
- zero-shot-react-description: 只考虑当前的操作，不会记录以及参考之前的操作。react 表明通过 ReAct 框架进行推理，description 表明通过工具的 description 进行是否使用的决策。
- chat-conversational-react-description: 
- conversational-react-description:
- react-docstore:
- self-ask-with-search 等，类似 chat-conversational-react-description 通过 memory 记录之前的对话，应答会参考之前的操作。

#### 自定义 Tool

Agents（智能体）：访问其他工具

Agents是LLM与工具之间的**接口**，Agents用来确定任务与工具。

一般的Agents执行任务过程：
- a. 首先，接收用户输入，并转化为PromptTemplate
- b. 其次，Agents通过调用LLM输出action，并决定使用哪种工具执行action
- c. 最后，Agents调用工具完成action任务
- ![agent示意图](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/b53d13fc3ceb4d5fa43081721e2b97b9~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=HzMa7h7l78O8xFoMDsdNIx%2Bf0yg%3D)

Agents可以调用那些工具完成任务？

| 工具 | 描述 | 
| --- | --- | 
| 搜索 | 调用谷歌浏览器或其他浏览器搜索指定内容 |
| 终端 | 在终端中执行命令，输入应该是有效的命令，输出将是运行该命令的任何输出 |
| Wikipedia | 从维基百科生成结果 |
| Wolfram-Alpha | WA 搜索插件——可以回答复杂的数学、物理或任何查询，将搜索查询作为输入。 |
| Python REPL | 用于评估和执行 Python 命令的 Python shell。它以 python 代码作为输入并输出结果。输入的 python 代码可以从 LangChain 中的另一个工具生成 |

Agent通过调用wikipedia工具，对用户提出的问题回答。尽管gpt-3.5功能强大，但是其知识库截止到2021年9月，因此，agent调用wikipedia外部知识库对用户问题回答。回答过程如下：
- a. 分析用户输入问题，采取的Action为通过Wikipedia实现，并给出了Action的输入
- b. 根据分析得到了最相关的两页，并进行了总结
- c. 对最后的内容进一步提炼，得到最终答案

```py
import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

openai_api_key = 'sk-F9xxxxxxx55q8YgXb6s5dJ1A4LjA'
os.environ['OPENAI_API_KEY'] = openai_api_key
llm = OpenAI(temperature=0)
tools = load_tools(["wikipedia","llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
print(agent.run("列举spaceX星舰在2022年后的发射记录?"))
```

多种方式可以自定义 Tool，最简单的方式是通过 @tool 装饰器，将一个函数转为 Tool。注意函数必须得有 docString，其为 Tool 的描述。

```py
from azure_chat_llm import llm
from langchain.agents import load_tools, initialize_agent, tool
from langchain.agents.agent_types import AgentType
from datetime import date

@tool
def time(text: str) -> str:
    """
    返回今天的日期。
    """
    return str(date.today())

tools = load_tools(['llm-math'], llm=llm)
tools.append(time)
agent_math = initialize_agent(agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                   tools=tools,
                                   llm=llm,
                                   verbose=True)
print(agent_math("计算45 * 54"))
print(agent_math("今天是哪天？"))
```

### （6）Memory（记忆）：

模型是无状态的，不保存上一次交互时的数据
- OpenAI的API服务没有上下文概念，而chatGPT是额外实现了上下文功能。

正常情况下 Chain 无状态的，每次交互都是独立的，无法知道之前历史交互的信息。

对于像聊天机器人这样的应用程序，需要记住以前的对话内容。
- 但默认情况下，LLM对历史内容**没有记忆功能**。LLM的输出只针对用户当前的提问内容回答。
- 为解决这个问题，Langchain提供了**记忆组件**，用来管理与维护历史对话内容。
- ![memory示意图](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/c64ff3021d1a4ba68c3a6a5dd470cdc6~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=M2fWwrITBkva%2BXT%2BiQINk6VD54M%3D)

LangChain 使用 Memory 组件保存和管理历史消息，这样可以跨多轮进行对话，在当前会话中保留历史会话的上下文。Memory 组件支持多种存储介质，可以与 Monogo、Redis、SQLite 等进行集成，以及简单直接形式就是 Buffer Memory。常用的 Buffer Memory 有
- 1）ConversationSummaryMemory ：以摘要的信息保存记录
- 2）ConversationBufferWindowMemory：以原始形式保存最新的 n 条记录
- 3）ConversationBufferMemory：以原始形式保存所有记录通过查看 chain 的 prompt，可以发现 {history} 变量传递了从 memory 获取的会话上下文。下面的示例演示了 Memory 的使用方式，可以很明细看到，答案是从之前的问题里获取的。

langchain提供不同的Memory组件完成内容记忆，下面列举四种：
- `ConversationBufferMemory`：记住**全部对话内容**。这是最简单的内存记忆组件，它的功能是直接将用户和机器人之间的聊天内容记录在内存中。[img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/8b04d8cc8c8f462bafa21bc473066efc~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=ljnOnmukL7V9UH5OzY4l%2BpwkfpU%3D)
- `ConversationBufferWindowMemory`：记住**最近k轮**的聊天内容。与之前的ConversationBufferMemory组件的差别是它增加了一个窗口参数，它的作用是可以指定保存多轮对话的数量。[img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/a830075b33094ef38f3aea87010fdd58~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=BbNKPeRu0j9knJWw02kEPUOu1uI%3D)
  - ​在该例子中设置了对话轮数k=2，即只能记住前两轮的内容，“我的名字”是在前3轮中的Answer中回答的，因此其没有对其进行记忆，所以无法回答出正确答案。
- `ConversationSummaryMemory`：ConversationSummaryMemory它不会将用户和机器人之前的所有对话都存储在内存中。它只会存储一个用户和机器人之间的**聊天内容的摘要**，这样做的目的可能是为了节省内存开销和token的数量。
  - ConversationSummaryMemory[第一轮对话](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/6b3c8f69e31440af9cb954bc903fd65d~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=X8kxNoQQtJqKKBIufAI5%2BGTprxo%3D): 你好，我是王老六
  - ConversationSummaryMemory[第二轮对话](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/ab4fbe8ad6cb4286a1e8f9e10141d2ef~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=tf%2FsfV5MF%2BIK7yWow48%2BvO%2FV%2BqY%3D): 你叫什么名字
  - 在第一轮对话完成后，Memory对第一轮对话的内容进行了总结，放到了摘要中。在第二轮对话中，LLM基于摘要与该轮的问题进行回答。
- `VectorStored-Backed Memory`: 将所有之前的对话通过**向量**的方式存储到VectorDB（向量数据库）中，在每一轮新的对话中，会根据用户的输入信息，匹配向量数据库中**最相似的K组**对话。


```py
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from azure_chat_llm import llm

memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
print(conversation.prompt)
print(conversation.predict(input="我的姓名是tiger"))
print(conversation.predict(input="1+1=?"))
print(conversation.predict(input="我的姓名是什么"))
```

国内不少LLm团队采用langChain，集成llm本地化知识库
- langChain，babyAGI 想做AGI生态，这个就有些力不从心了。autoGPT好一点，相对简单。
- langChain，babyAGI的子模块，都是几百个。特别是langChain，模块库居然有600多张子模块map架构图

[无需OpenAI API Key，构建个人化知识库的终极指南](https://mp.weixin.qq.com/s/ponKZ1OaHXX2nzuSxXg8-Q)

构建知识库的主要流程：
1. 加载文档
2. 文本分割
3. 构建矢量数据库
4. 引入LLM
5. 创建qa_chain，开始提问

## LangChain 实践

### 文档生成总结

文档生成总结
- 1）通过 Loader 加载远程文档
- 2）通过 Splitter 基于 Token 进行文档拆分
- 3）加载 summarize 链，链类型为 refine，迭代进行总结

```py

3、LangChain 落地实践
3.1 文档生成总结
1）通过 Loader 加载远程文档

2）通过 Splitter 基于 Token 进行文档拆分

3）加载 summarize 链，链类型为 refine，迭代进行总结

from langchain.prompts import PromptTemplate
from langchain.document_loaders import PlaywrightURLLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from azure_chat_llm import llm

loader = PlaywrightURLLoader(urls=["https://content.jr.jd.com/article/index.html?pageId=708258989"])
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    model_name="gpt-3.5-turbo",
    allowed_special="all",
    separators=["\n\n", "\n", "。", "，"],
    chunk_size=7000,
    chunk_overlap=0
)

prompt_template = '''
作为一个资深编辑，请针对 >>> 和 <<< 中间的文本写一段摘要。 
>>> {text} <<<
'''
refine_template = '''
作为一个资深编辑，基于已有的一段摘要：{existing_answer}，针对 >>> 和 <<< 中间的文本完善现有的摘要。 
>>> {text} <<<
'''

PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
REFINE_PROMPT = PromptTemplate(
    template=refine_template, input_variables=["existing_answer", "text"]
)

chain = load_summarize_chain(llm, chain_type="refine", question_prompt=PROMPT, refine_prompt=REFINE_PROMPT, verbose=False)

docs = text_splitter.split_documents(data)
result = chain.run(docs)
print(result)
```

### 基于外部文档的问答

基于外部文档的问答
- 1）通过 Loader 加载远程文档
- 2）通过 Splitter 基于 Token 进行文档拆分
- 3）通过 FAISS 向量存储文档，embedding 加载 HuggingFace 的 text2vec-base-chinese 模型
- 4）自定义 QA 的 prompt，通过 RetrievalQA 回答相关的问题

```py
作者：京东云
链接：https://www.zhihu.com/question/609483833/answer/3146379316
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

from langchain.chains import RetrievalQA
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from azure_chat_llm import llm

loader = WebBaseLoader("https://in.m.jd.com/help/app/register_info.html")
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    model_name="gpt-3.5-turbo",
    allowed_special="all",
    separators=["\n\n", "\n", "。", "，"],
    chunk_size=800,
    chunk_overlap=0
)
docs = text_splitter.split_documents(data)
#设置自己的模型路径
embeddings = HuggingFaceEmbeddings(model_name="text2vec-base-chinese", cache_folder="model")
vectorstore = FAISS.from_documents(docs, embeddings)

template = """请使用下面提供的背景信息来回答最后的问题。 如果你不知道答案，请直接说不知道，不要试图凭空编造答案。
回答时最多使用三个句子，保持回答尽可能简洁。 回答结束时，请一定要说"谢谢你的提问！"
{context}
问题: {question}
有用的回答:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(),
                                       return_source_documents=True,
                                       chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})

result = qa_chain({"query": "用户注册资格"})
print(result["result"])
print(len(result['source_documents']))
```


###  LangChain + Milvus

```py
from langchain.embeddings.openai import OpenAIEmbeddings # openai
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI  # openai
import os

os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"

# Question Answering Chain
# ① 加载文档
with open("../test.txt") as f:
    state_of_the_union = f.read()
# ② 文本分割
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0) # 指定分割器
texts = text_splitter.split_text(state_of_the_union) # 分割文本
embeddings = OpenAIEmbeddings() # 使用OpenAI的embedding服务
# ③ 构建适量数据库
docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))]).as_retriever()
query = "What did the president say about Justice Breyer"
docs = docsearch.get_relevant_documents(query)
# ④ 引入LLM，创建qa_chain
chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
# ⑤ 开始提问
answer = chain.run(input_documents=docs, question=query)
print(answer)
```

以上构建依赖OpenAI，有第三方免费服务吗？
- [transformers-course](Github：https://github.com/Liu-Shihao/transformers-course)

Huggingface开源AI模型构建本地知识库
- 开源的google/flan-t5-xlAI模型

```py
from langchain import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms.base import LLM
import os

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

os.environ["HUGGINGFACEHUB_API_TOKEN"] = 'HUGGINGFACEHUB_API_TOKEN'

# Document Loaders
loader = TextLoader('../example_data/test.txt', encoding='utf8')
documents = loader.load()

# Text Splitters
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# select embeddings
embeddings = HuggingFaceEmbeddings()

# create vectorstores
db = Chroma.from_documents(texts, embeddings)

# Retriever
retriever = db.as_retriever(search_kwargs={"k": 2})

query = "what is embeddings?"
docs = retriever.get_relevant_documents(query)

for item in docs:
    print("page_content:")
    print(item.page_content)
    print("source:")
    print(item.metadata['source'])
    print("---------------------------")

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-xl")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-xl")
pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=512,
    temperature=0,
    top_p=0.95,
    repetition_penalty=1.15
)

llm = HuggingFacePipeline(pipeline=pipe)

chain = load_qa_chain(llm, chain_type="stuff")
llm_response = chain.run(input_documents=docs, question=query)
print(llm_response)
print("done.")
```

集成了 Milvus 和 LangChain：[参考](https://mp.weixin.qq.com/s/tgQ-SOoc0h-hqDZy9N3rfg)

```py
class VectorStore(ABC):
    """Interface for vector stores."""    
    @abstractmethod
    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        kwargs:Any,
    ) ->List[str]:
    """
      Run more texts through the embeddings and add to the vectorstore.
    """    
    @abstractmethod
    def similarity_search(self, query:str, k:int =4,kwargs: Any) -> List[Document]:
        """Return docs most similar to query."""
        def max_marginal_relevance_search(self, query: str, k: int = 4, fetch_k: int = 20) -> List[Document]:
        """Return docs selected using the maximal marginal relevance."""
        raise NotImplementedError

    @classmethod    
    @abstractmethod
    def from_texts(
        cls: Type[VST],
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> VST:
        """Return VectorStore initialized from texts and embeddings."""
```                


将 Milvus 集成到 LangChain 中，实现几个关键函数：add_texts()、similarity_search()、max_marginal_relevance_search()和 from_text()

将 Milvus 集成到 LangChain 中的确存在一些问题，最主要的是 <span style='color:blue'>Milvus 无法处理 JSON 文件</span>。目前，只有两种解决方法：
- 现有的 Milvus collection 上创建一个 VectorStore。
- 基于上传至 Milvus 的第一个文档创建一个 VectorStore。

### LangChain + Faiss + Ray 实践

【2023-5-29】[Building an LLM open source search engine in 100 lines using LangChain and Ray](https://www.anyscale.com/blog/llm-open-source-search-engine-langchain-ray)
- Building the index: Build a document index easily with Ray and Langchain
- ![](https://images.ctfassets.net/xjan103pcp94/4OzISThpksdKgjZ0gVJUiB/85bb7fccdfef1df3d061c57e9af1062a/index-langchain.jpg)
- Build a document index 4-8x faster with Ray
- ![](https://images.ctfassets.net/xjan103pcp94/7tDpD5Q7nxtRyX9lgDvbkI/6209fbd875c5cd379c2289ef6f6554f0/Screen_Shot_2023-04-16_at_6.20.10_PM.png)
- Serving: Serve search queries with Ray and Langchain
- ![](https://images.ctfassets.net/xjan103pcp94/1g6zBePU72Rmz5MBH2reaB/db400e9bbbc445d7214d45658f81992f/Screen_Shot_2023-04-16_at_9.42.46_PM.png)


### LangChain+ChatGLM 本地问答

[LangChain+ChatGLM 实现本地问答](https://juejin.cn/post/7236028062873550908)

ChatGLM-6B api部署：[ChatGLM 集成进LangChain工具](https://juejin.cn/post/7226157821708681277)
- [api.py](https://github.com/THUDM/ChatGLM-6B/blob/main/api.py#L53:5)
- 默认本地的 8000 端口，通过 POST 方法进行调用

```sh
pip install fastapi uvicorn
python api.py
```

效果

```sh
curl -X POST "http://{your_host}:8000" \
     -H 'Content-Type: application/json' \
     -d '{"prompt": "你好", "history": []}'
# 结果
{
  "response":"你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。",
  "history":[["你好","你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。"]],
  "status":200,
  "time":"2023-03-23 21:38:40"
}
```

封装 ChatGLM API到LangChain中

```py
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from typing import Dict, List, Optional, Tuple, Union

import requests
import json

class ChatGLM(LLM):
    max_token: int = 10000
    temperature: float = 0.1
    top_p = 0.9
    history = []

    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "ChatGLM"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # headers中添加上content-type这个参数，指定为json格式
        headers = {'Content-Type': 'application/json'}
        data=json.dumps({
          'prompt':prompt,
          'temperature':self.temperature,
          'history':self.history,
          'max_length':self.max_token
        })
        # print("ChatGLM prompt:",prompt)
        # 调用api
        response = requests.post("{your_host}/api",headers=headers,data=data)
		# print("ChatGLM resp:",response)
        if response.status_code!=200:
          return "查询结果错误"
        resp = response.json()
        if stop is not None:
            response = enforce_stop_tokens(response, stop)
        self.history = self.history+[[None, resp['response']]]
        return resp['response']
# 调用
llm = ChatGLM()
print(llm("你会做什么"))
# ChatGLM prompt: 你会做什么
# 我是一个大型语言模型，被训练来回答人类提出的问题。我不能做任何实际的事情，只能通过文字回答问题。如果你有任何问题，我会尽力回答。

```



# 结束