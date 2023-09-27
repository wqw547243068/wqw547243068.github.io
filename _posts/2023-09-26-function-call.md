---
layout: post
title:  大模型函数调用 LLM Function Call 
date:   2023-09-26 16:52:00
categories: AIGC
tags: gpt openai 函数调用
excerpt: OpenAI Function call 开发、函数调用知识总结
mathjax: true
permalink: /function
---

* content
{:toc}

# Function call 函数调用

GPT模型本身并不支持与外部系统、数据库或文件的实时交互。但可以使用**函数**来完成。

如何更可靠地从模型中获取结构化数据？
- Function Calling

模型微调后可以检测**何时**调用函数（取决于输入）并使用符合函数签名的 JSON 进行响应。
- 模型层面，识别出**何时**需要调用函数来对输出格式化
- 函数方面，设定具体格式化逻辑来更好使用

`函数调用` （Function Calling) 提供了一种将 GPT 的能力与外部工具和 API 相连接的新方法

注意: <span style='color:red'>API不会执行任何函数调用</span>。
- 使用输出参数执行函数调用必须由开发人员完成。
- 比如，用户输入 <span style='color:blue'>#graphic_art("a dragon")</span>，API只会返回一个字符串"a dragon"，而不会真正生成一幅图像。要想真正执行函数，就需要开发人员自己编写代码来调用相应的服务或库。

参考
- [Function Call： Chat 应用的插件基石与交互技术的变革黎明](https://zhuanlan.zhihu.com/p/649766613)
- [OpenAI的新能力——Function Calling](https://zhuanlan.zhihu.com/p/637002733)
- [一文学会 OpenAI 的函数调用功能 Function Calling](https://zhuanlan.zhihu.com/p/641239259)
- [OpenAI开发系列（十一）：Function calling功能的实际应用流程与案例解析](https://zhuanlan.zhihu.com/p/645501247)
- [OpenAI开发系列（十二）：Function calling功能的流程优化与多轮对话实现](https://zhuanlan.zhihu.com/p/645732735)

## Function call 介绍

6月13日后，调用 OpenAI GPT 3.5 Turbo和GPT-4需要使用 [Chat Completions API](https://platform.openai.com/docs/guides/gpt/chat-completions-api) 。

这两个模型可以在chat completion的api中使用一个新的功能 —— `Function Calling`：可**识别**且**格式化**输出

Function Call 是 GPT API 中新功能。让开发者在调用 GPT-4 和 GPT-3.5-turbo 模型时，**描述函数**并让模型智能地输出一个包含调用这些函数所需参数的 **JSON 对象**。更可靠地将 GPT 能力与外部工具和 API 进行连接，从而实现以下应用：
- （1）**创建聊天机器人**：开发者可以调用外部工具(如 ChatGPT 插件)回答问题
  - 将查询“<span style='color:blue'>北京的天气如何？</span>”转换为调用 `getCurrentWeather(location: string)` 的函数。
- （2）将**自然语言**转换为 **API 调用**或**数据库查询**：
  - “<span style='color:blue'>这个月我的前十个客户是谁？</span>”转换为调用 `get_customers_by_revenue(start_date, end_date, limit)` 的内部 API 调用，
  - <span style='color:blue'>上个月 Acme 公司下了多少订单？</span> 转换为使用 `sql_query(query)` 的 SQL 查询。
- （3）从文本中提取**结构化数据**：开发者可以定义一个名为 `extract_people_data(people)` 的函数，以提取在维基百科文章中提到的所有人物。


## Function call 原理

从人机交互上来说， Function Call 本质上只做了一件事
- 准确**识别**用户语义，将其转为**结构化**指令。

机器无法理解「<span style='color:blue'>我叫小明，今年18岁，家在杭州市西湖边</span>」这样**非结构化**输入。只有将其拆分为「姓名」、「年龄」这样的字段，机器才能识别相应的信息结构，并将这样结构化后的信息接入后续的流程。
- ![](https://pic1.zhimg.com/80/v2-ddd2def91d44c0ba7963312e0d126ff4_1440w.webp)

Function Call 实现的最大的价值是: 
> 让机器轻易地理解了用户**模糊化**输入，将其转换为机器可以理解的**技术指令**。这对于人机交互的范式完全是质的改变。

### 调用流程

Function call 完整调用流程
- ![](https://pic4.zhimg.com/80/v2-35079a8d8be49318137f973d3e4c66bf_1440w.webp)

当大模型激活 Function Calling 功能时，其推理过程也会发生相应的改变：
- 根据大模型返回的**函数**和**函数参数**，在<span style="color:red">本地完成函数计算</span>
- 然后再将计算过程和结果保存为message, 并追加到messages**后面**
- 并第2次调用 Chat Completion模型分析函数的计算结果，并最终根据函数计算结果输出用户问题的答案。

优化的方向有两个：
- 提升functions参数的**编写效率**
- 优化不断**拼接**messages的过程。

### 代码


```py
from dotenv import load_dotenv
import os
import openai
import json

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 任务执行函数
def get_pizza_info(pizza_name: str):
    pizza_info = {
        "name": pizza_name,
        "price": "10.99",
    }
    return json.dumps(pizza_info)

# 函数调用详情
functions = [
    {
        "name": "get_pizza_info",
        # 描述非常重要：llm 用函数描述来识别函数 （Function Calling) 是否适合回答用户的请求。
        "description": "Get name and price of a pizza of the restaurant",
        "parameters": {
            "type": "object",
            "properties": { # 参数信息
                "pizza_name": {
                    "type": "string",
                    "description": "The name of the pizza, e.g. Salami",
                },
            },
            "required": ["pizza_name"], # 必备参数
        },
    }
]

def chat(query): # 调用
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": query}],
        functions=functions, # 设置函数调用
    )
    message = response["choices"][0]["message"]
    return message

if message.get("function_call"):
    # 解析第一次调用的时候返回的 pizza 信息
    function_name = message["function_call"]["name"]
    pizza_name = json.loads(message["function_call"] ["arguments"]).get("pizza_name")
    print(pizza_name)
    # 这里将 chat 小助手函数的响应结果提取后，传递 function_response
    function_response = get_pizza_info(
        pizza_name=pizza_name 
    )

    second_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "user", "content": query},
            message,
            {
                "role": "function",
                "name": function_name,
                "content": function_response, # function calling 的 content 是 get_pizza_info 函数 
            },
        ],
    )

second_response
```


## Function call 实例

用户问题: 
> 帮我给小美发一封邮件，告诉她我晚上不回去吃了。

原始GPT: 
> 亲爱的小美，我希望你一切都好。。。。

设置prompt: 

```json
// prompt 设计
将以下内容转换为json格式，包含两个字段：receiver（接收人）、content（邮件内容）
- 帮我给小美发一封邮件，告诉她我晚上不回去吃了。

// 返回
{
  "reveiver":"小美", "content":"亲爱的小美..."
}
```

基本解决，但问题：
- 用户输入未知，难以识别用户意图是发邮件，还是其它操作

如何更可靠地从模型中获取结构化数据？Function Calling

微调后可检测：何时应该调用函数（取决于输入）, 并使用符合函数签名的 JSON 进行响应。
- 模型层面，识别出何时需要调用函数来对输出格式化
- 函数方面，设定具体的格式化逻辑, 更好使用

index.py，[完整代码](https://github.com/GogoWwz/AI-Notebook/tree/main/Skills)

```py
import json
from enum import Enum
import openai
openai.api_key = 'xxx'

def run_conversation():
  MODEL = "gpt-3.5-turbo-0613"
  response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
      {"role": "user", "content": "给小美发个邮件，告诉她我晚饭不回家吃了"},
    ],
    temperature=0
  )

  message = response["choices"][0]["message"]
  print(message)

run_conversation()
```

发邮件的文件 EmailSkill.py , 文件就导出了两个函数
- 用来给Function Calling调用的函数：send_email
- 发邮件的操作函数：send_email_action

```py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 发送邮件操作
def send_email_action(receiver, content):
  if (not receiver): return
  # 邮件配置
  smtp_server = "smtp.163.com"
  smtp_port = 25
  sender_email = "sender_email"
  receiver_email = receiver
  password = 'password'

  # 构建邮件内容
  message = MIMEMultipart()
  message["From"] = Header('AI <%s>' % sender_email)
  message["To"] = receiver_email
  message["Subject"] = "我是您的AI助理，您有一封邮件请查看"

  body = content
  message.attach(MIMEText(body, "plain"))

  # 连接到邮件服务器并发送邮件
  with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

# 供Function Calling使用的输出处理函数
def send_email(receiver, content = ''):
  # 通讯录
  Contact = {
    "小美": "xx@example.com",
  }

  email_info = {
    "receiver": Contact[receiver],
    "content": content
  }

  return email_info
```

chat completion api 新增了两个参数：
- `function_call`: 一个开关，控制模型是否要调用函数对输出进行处理，默认为"none"不开启, 设置为"auto"表示开启
- `functions`: 对输出结果进行处理的函数描述列表

functions 示例

两个必填的参数：
- receiver：邮件接收方，string类型
- content：邮件内容，string类型

```json
{
  "name": "send_email", // 函数名
  "description": "send email assistant", // 函数描述：llm 用函数描述来识别函数 （Function Calling) 是否适合回答用户的请求。非常重要！
  "parameters": { // 给LLM看的函数签名
    "type": "object",
    "properties": { // 必填参数信息
      "receiver": {
        "type": "string",
        "description": "email receiver",
      },
      "content": {"type": "string", "description": "email content"},
    },
    "required": ["receiver", "content"], // 哪些参数必备
  }
}
```

调用代码

```py
import json
from enum import Enum

import openai
openai.api_key = 'xxx'

from EmailSkill import send_email, send_email_action

# 为什么要单独定义这个枚举类？
class SkillFunctions(Enum):
  SendEmail = 'send_email'

def run_conversation():
   MODEL = "gpt-3.5-turbo-0613"
   response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
      {"role": "user", "content": "给小美发个邮件，告诉她我晚饭不回家吃了"},
    ],
    temperature=0,
    functions=[ # 新增功能 function call
      {
        "name": SkillFunctions.SendEmail.value,
        "description": "send email assistant",
        "parameters": {
          "type": "object",
          "properties": {
            "receiver": {
              "type": "string",
              "description": "收件人名字即可",
            },
            "content": {"type": "string", "description": "邮件的内容"},
          },
          "required": ["receiver", "content"],
        },
      }
    ],
    function_call="auto", # 自动识别是否开启功能
  )

  message = response["choices"][0]["message"]
  print(message)
# GPT 推理执行
run_conversation()

# ---------- 返回结果处理 ------------
if(message.get("function_call")):
    # 函数调用处理区
    function_name = message["function_call"]["name"] # 函数名
    arguments = json.loads(message["function_call"]["arguments"]) # 参数信息
    # 动作处理
    if (function_name == SkillFunctions.SendEmail.value):
      email_info = send_email( # 整理邮件信息
        receiver=arguments.get('receiver'),
        content=arguments.get('content')
      )
      print(email_info)
      send_email_action(**email_info) # 执行任务：发送邮件
      print('邮件已发送')
```

效果
- ![](https://pic2.zhimg.com/80/v2-32ed80648cd0b5ceb381ce1a5de1561d_1440w.webp)

## Function call 问题

注意事项
- **函数描述** 计入token，所以何时使用、如何使用, 要自己抉择。
- 潜在风险（AI存在幻觉或分析不准确），官方强烈建议在代表用户采取行动（发送电子邮件、在线发布内容、进行购买等）之前增加**用户确认**流程。




## LangChain 实现

LangChain 中如何使用 Function call？
- message.additional_kwargs
- tools
- agent

注意：
- langchain的版本不低于0.0.200， 之前的版本尚不支持函数调用 （Function Calling); 

print_version函数（Function Calling) 检查目前的langchain的版本是否大于0.0.200。

```py
import pkg_resources

def print_version(package_name):
    try:
        version = pkg_resources.get_distribution(package_name).version
        print(f"The version of the {package_name} library is {version}.")
    except pkg_resources.DistributionNotFound:
        print(f"The {package_name} library is not installed.")

print_version("langchain")
The version of the langchain library is 0.0.205.
```

### LangChain additional_kwargs

如何与 LangChain 一起使用?
- 首先导入 ChatOpenAI 类和 HumanMessage、AIMessage，还有 ChatMessage 类，这些类可以帮助我们创建这种功能，包括用户角色等。
  - 可以不必要像之前那样，定义角色等，只需要传递 content。其他的都交给了 Langchain.
- 然后在这里创建模型 LLM，通过实例化 ChatOpenAI
- message.additional_kwargs 中包括了函数调用 （Function Calling)字典

```py
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage
# 创建模型 LLM
llm = ChatOpenAI(model="gpt-3.5-turbo-0613")
# 运行预测消息函数
message = llm.predict_messages( # 参数 functions
    [HumanMessage(content="What is the capital of france?")], functions=functions
)
# 返回： message.additional_kwargs
# AIMessage(content='The capital of France is Paris.', additional_kwargs={}, example=False)
message_pizza = llm.predict_messages(
    [HumanMessage(content="How much does pizza salami cost?")], functions=functions
)
message
# AIMessage(content='', additional_kwargs={'function_call': {'name': 'get_pizza_info', 'arguments': '{\n"pizza_name": "Salami"\n}'}}, example=False)

import json
# 打印结果是 'Salami'
pizza_name = json.loads(message_pizza.additional_kwargs["function_call"]["arguments"]).get("pizza_name")
# 将'Salami'传参给 get_pizza_info 函数
pizza_api_response = get_pizza_info(pizza_name=pizza_name)
# '{"name": "Salami", "price": "10.99"}'

second_response = llm.predict_messages(
    [
        HumanMessage(content=query), # query = "How much does pizza salami cost?"
        AIMessage(content=str(message_pizza.additional_kwargs)),
        ChatMessage(
            role="function",
            additional_kwargs={
                "name": message_pizza.additional_kwargs["function_call"]["name"]
            },
            # pizza_api_response = get_pizza_info(pizza_name=pizza_name)
            content=pizza_api_response
        ),
    ],
    functions=functions,
)
# second_response
```

### LangChain tools

LangChain 提供了与外部世界交互的另一种标准化方法，进行请求或其他操作，这些称为工具 tools

工具 tools 是由 Chain 提供的类，可以创建自己的工具。

```py
from typing import Optional
from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# 继承基类工具来创建自定义类或自定义工具
class StupidJokeTool(BaseTool):
    """
      function call 示例
    """
    # 提供工具的名称和描述
    name = "StupidJokeTool"
    description = "Tool to explain jokes about chickens"

    # 定义下划线开头的函数： _run 函数 和 _arun ，实现异步和同步支持。
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        return "It is funny, because AI..."

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("joke tool does not support async")
```

使用工具(format_tool_to_openai_function)将自定义类(StupidJokeTool)转成标准格式

```py
from langchain.tools import format_tool_to_openai_function, MoveFileTool

tools = [StupidJokeTool(), MoveFileTool()]
# 将自己的 tools 转换为格式化的 function
functions = [format_tool_to_openai_function(t) for t in tools]
# functions 是之前定义的一个变量：一个函数列表
query = "Why does the chicken cross the road? To get to the other side"
output = llm.predict_messages([HumanMessage(content=query)], functions=functions)
# output
second_response = llm.predict_messages(
    [
        HumanMessage(content=query),
        AIMessage(content=str(output.additional_kwargs)),
        ChatMessage(
            role="function",
            additional_kwargs={
                "name": output.additional_kwargs["function_call"]["name"]
            },
            content="""
                {tool_response}
            """,
        ),
    ],
    functions=functions,
)
# second_response

```

output 运行结果：

```py
AIMessage(content='', additional_kwargs={'function_call': {'name': 'StupidJokeTool', 'arguments': '{\n"__arg1": "To get to the other side"\n}'}}, example=False)
#-------------
AIMessage(content='', additional_kwargs={'function_call': {'name': 'StupidJokeTool', 'arguments': '{\n  "__arg1": "To get to the other side"\n}'}}, example=False)
```

### LangChain Agent

Langchain Agent 如何实现 Function Calling ？

- 导入一些链 Chain，例如 LLMMathChain，还有一个 chat_models，聊天模型在这里使用 ChatOpenAI 创建LLM。

```py
from langchain import LLMMathChain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
tools = [
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    ),
]
```

此代理能够回答普通问题并进行一些计算，因此用初始化代理函数 （Function Calling) ，现在用它与工具。

```py
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
```

现在有新的代理类型 OPENAI_FUNCTIONS ，属于 openai 函数类型，运行这个代理不需要传递任何关键字参数或额外的参数，只需要像这样使用它。

现在运行“法国的首都是什么”，得到的结果是法国的首都：巴黎。

```py
agent.run("What is the capital of france?")
```

得到：

```
> Entering new  chain...
The capital of France is Paris.

> Finished chain.
'The capital of France is Paris.'
```


100 除以 25 等于多少，这时候计算器被调用，得到最终答案 100 除以 25 等于 4。

```py 
agent.run("100 除以 25 等于多少?")
``` 

得到：

```
> Entering new  chain...

Invoking: `Calculator` with `100 / 25`

> Entering new  chain...
100 / 25```text
100 / 25
...numexpr.evaluate("100 / 25")...
Answer: 4.0
 Finished chain. Answer: 4.0100 除以 25 等于 4。 
```

所以对于代理 Langchain Agent 来说，工作非常流畅，会与其他的 llm 链一起工作。


# 结束