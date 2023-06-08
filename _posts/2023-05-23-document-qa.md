---
layout: post
title:  文档问答原理及实践 Thoery and Implemetation of the Doucument QA
date:   2023-03-30 19:10:00
categories: 深度学习 自然语言处理
tags: ChatGPT 对话系统 知识库 向量化 milvus
excerpt: 文档问答的原理、案例及实践
mathjax: true
permalink: /doc-chat
---

* content
{:toc}

# 文档问答

【2023-3-27】文档问答

作者：[强化学徒](https://www.zhihu.com/question/589726461/answer/2961450933)

【2023-5-9】[大语言模型实现智能客服知识库文档数据提取功能](https://www.toutiao.com/article/7231062779061502501)
- 智能客服的知识库有两类：**机器人**知识库和**坐席**知识库，分别是为机器人和坐席进行服务时，提供数据的支撑。
- 如何通过大语言模型，让企业的文档可批量上传，无需更多的整理，直接转化为有效的QA，供座席和机器人直接调用呢？

当前的主流客服产品
- 智能客服系统会标配`知识库管理`功能，常见的形式是**树状结构**，提供分类管理、知识库条目管理，并支持知识库的批量导入导出操作。
- 使用中，企业需要经常性地维护管理知识库内容，将企业已有知识内容文档上传，但如果是将原文件上传，则系统最多能支持预览功能，使用者在操作界面只能点击打开全文检索。而如果是机器人知识库，直接上传文档是不可用的，需要操作者手工整理文档中的内容为机器人标准问答对。

大模型时代
- 所有企业的文档可以批量上传，无需更多的整理，直接可自动转化为有效的QA，供座席和机器人直接调用。

## 背景

### 文本向量化

`嵌入`（Embedding）是一种将**文本或对象**转换为**向量表示**的技术，将词语、句子或其他文本形式转换为固定长度的向量表示。
- 嵌入向量是由一系列浮点数构成的**向量**。
- 通过计算两个嵌入向量之间的距离，可以衡量它们之间的相关性。距离较小的嵌入向量表示文本之间具有较高的相关性，而距离较大的嵌入向量表示文本之间相关性较低。

以 `Milvus` 为代表的`向量数据库`利用语义搜索（Semantic Search）更快地检索到相关性更强的文档。

详见：sklearn专题里的[文本向量化](sklearn#%E5%90%91%E9%87%8F%E5%8C%96)

### Token

什么是token？
- tokens 不是指 prompt 字符串的长度；
- token 指一段话中可能被分出来的**词汇**。
  - 比如：i love you，就是三个token，分别为 「i」「love」「you」。
- 不同语言token计算不一样。[在线测试](platform.openai.com/tokenizer)
  - 中文的「我爱你」其实是算 5个token，因为会先把内容转成 unicode。
  - 有些 emoji 的token长度会超出想象，长达11个。

ChatGPT has an upper limit of 4096

GPT-4 支持，详见[官网](https://platform.openai.com/docs/models/gpt-4)
- 8k context
- 32k context

| Model | Price for 1000 tokens (prompt) |
|---|---|
| Ada | 2048 |
| Babbage | 2048 | 
| Curie | 2048 |
| DaVinci | 4096 |
| ChatGPT | 4096 |
| GPT-4 8k context | 8192 |
| GPT-4 32k context | 32768 |

Remember, the sum of your prompt and maximum tokens should always be less than equal to the model's maximum token limit, OR your output is truncated.

备注
- 编码器：可以接受长度不超过最大序列长度（如 512 个单词）的输入。如果序列长度小于该限制，就在其后填入预先定义的空白单词。
  - 如，原始 transformer 论文中的编码器模块可以接受长度不超过最大序列长度（如 512 个单词）的输入。
- 解码器：区别
  - 加入了一层重点关注编码器输出的某一片段，**编码器-解码器自注意力**（encoder-decoder self-attention）层
  - 后面的单词掩盖掉了。但并不像 BERT 一样将它们替换成特殊定义的单词 < mask >，而是在自注意力计算的时候屏蔽了来自当前计算位置右边所有单词的信息。


经验
- 英文：100 tokens ~= 75 words)
- 中文：一个汉字占2-3个token
- 其它：emoji表情符号，占用更多，有的高达11个

### 如何增强LLM能力

【2023-5-21】[LLM训练营课程笔记—Augmented Language Models](https://zhuanlan.zhihu.com/p/630195581)
- [英文ppt](https://drive.google.com/file/d/1A5RcMETecn6Aa4nNzpVx9kTKdyeErqrI/view), [讲义总结](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/augmented-language-models/)
- There are three ways to augment language models: retrieval, chains, and tools.
- Retrieval involves providing an external corpus of data for the model to search, chains use the output of one language model as input for another, and tools allow models to interact with external data sources.

LLM擅长什么？
- • 语言理解
- • 遵循指令
- • 基础推理
- • 代码理解

LLM在哪些方面需要帮助？
- • 获取最新知识
- • 用户数据包含的知识
- • 更有挑战性的推理
- • 与外界交互

如何增强LLM的能力？
- LLM更加擅长**通用推理**，而不是**特定知识**。

为了让LLM能够取得更好的表现，最常见方法就是给LLM提供合适的**上下文信息**帮助LLM进行推理。

随着最近LLM的不断发展，各类大模型所能支持的最大上下文**长度**也越来越大，但是在可预见的一段时间内仍不可能包含所有内容，并且越多的上下文意味着更多的计算成本。
- ![](https://pic3.zhimg.com/80/v2-01d520894c2ada7c23aa4f450aae71ca_1440w.webp)

如何充分利用当前所能支持的有限的上下文信息，让LLM表现更好，值得研究。有限下文情况下充分激发LLM的能力的方法有三种：
- `Retrieval`：答案在文档内，并行找相关内容作为prompt
- `Chain`：答案在文档外，串行请求
- `Tools`：调用外部工具

（1）通过**Retrieval增强**LLM的能力 —— <span style='color:blue'>答案在文档内</span>
 
一个典型的在文档QA场景使用检索方式来增强LLM能力的方式，分为几个流程：
*   用户问题embedding
*   从海量文档中检索出Top N与问题embedding相似的候选文档
*   基于TopN文档内容构造Prompt
*   调用LLM获取最终答案
 
![](https://pic1.zhimg.com/80/v2-72a51d5f2be59ac526ea858e8fe15678_1440w.webp)
 
常用的Retrieval技术
 
对Retrieval的技术细节以及一些常用的工具进行了详细的介绍，包括**传统Retrieval**以及**基于Embedding的Retrieval**这两种技术路线，[原教程](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/augmented-language-models/)学习或者参考一些其他的[信息检索资料](https://github.com/%2520%2520sebastian-hofstaetter/teaching)。
 
（2）通过**Chain**增强LLM的能力 —— <span style='color:blue'>答案在文档外</span>
 
某些情况下，最佳的context可能并**不存在于用户语料库**中。上一个LLM的输出结果可能正好是当前LLM的最好的输入context。
 
此时，可以用Chain形式将不同的LLM连接起来，去增强最终任务的效果。例如下图的摘要任务：
- 首先将文本拆分为多个部分，对于每个部分使用LLM做一个局部摘要，然后再用LLM对各个摘要进行合并输出全局的摘要。
- ![](https://pic3.zhimg.com/80/v2-65144390d9958a95f33a316618a32092_1440w.webp)

典型进行这样任务编排的工具是[LangChain](https://github.com/hwchase17/langchain)，可以利用它来开发很多有意思的应用。
 
（3）通过**Tools增强**LLM的能力 —— <span style='color:blue'>借助外界工具</span>
 
通过各种各样的工具让LLM与外界进行交互，比如使用搜索引擎、执行SQL语句等，从而去丰富LLM的功能。

Tools方式大致有两种
- 一种是基于**Chain**的方式，Tool是一个**必选项**，前面有一个LLM来构造Tool的输入，后面会有另一个LLM来总结Tool的输出并得到最终的结果；
- 一种是基于**Plugin**的方式，Tool是一个**可选项**，让LLM来决定用不用以及怎么用Tool。

![](https://pic2.zhimg.com/80/v2-2038fc84985ec24ed8831bf66f16a4b1_1440w.webp)

总结
- • 通过与外界数据的交互，LLM的能力能够更加强大。
- • 通过使用规则和启发式方法，可以实现各种各样的功能。

随着知识库的扩大，应该将其视为一个**信息检索系统**。使用Chain的方式可以帮助编码更复杂的推理，并且绕过token长度的限制。各种各样的外部工具可以让模型访问更多的资源。


## 方法总结

[作者](https://www.zhihu.com/question/591935281/answer/2961925796)

常见的方法：
- `retrieve-then-generate`：类ChatGPT Retrieval Plugin的技术方案
  - 根据输入query来抽取相关外部文本，把抽取到的文本和query一起作为prompt再来做后续字符的推理。
  - chatpdf这种产品的方法也类似，先把你输入的文档分成多个chunk分别做embedding放到向量数据库里，然后根据输入embedding的向量做匹配，再把匹配到的向量对应的chunk和输入一起作为prompt给LLM。
  - 论文：【2020-2-10】[REALM: Retrieval-Augmented Language Model Pre-Training](https://arxiv.org/abs/2002.08909)
- `Fine-tuning`：Fine-tuning是指在已经训练好的GPT/LLM模型基础上，使用**新数据集**再次训练。这种方法可以使模型针对特定任务或特定领域的语言使用情况进行优化，从而提高模型的效果。在Fine-tuning过程中，可以将**额外知识**作为新的数据集加入到训练中。
- `Knowledge Distillation`：Knowledge Distillation是指将一个“大模型”的知识转移到一个“小模型”中。例如，可以将一个已经训练好的GPT/LLM模型的知识转移到一个小型的模型中，使得小型模型能够使用大型模型中的知识。这种方法可以通过将额外的知识加入到“大模型”中，从而使得“小模型”可以使用这些知识。
- `数据增强`：数据增强是指在已有的数据集中，添加一些类似但不完全相同的数据来增加数据的数量和多样性。这种方法可以使得模型更加全面地学习到不同的语言使用情况，从而提高模型的效果。在数据增强的过程中，可以添加额外的知识，例如同义词、反义词、专业术语等。
  - 词向量：将领域特定的词汇和词向量添加到模型的词汇表中。这些词汇可以是在目标领域中独有的词汇或者在常规数据集中缺失的词汇。
  - 外部数据集：从外部数据集中收集与目标领域相关的数据，并将其添加到模型的训练数据中。这种方法需要找到与目标任务相关的高质量数据集，并使用适当的方法将其合并到模型的训练数据中。
  - 外部知识库：将外部的知识库，如百科全书、知识图谱等，与模型集成，以便模型可以使用这些知识来辅助其生成文本。
  - 人工标注：通过人工标注的方式，将领域特定的信息添加到训练数据中。这种方法需要大量的人力和时间，并且对于大型数据集来说可能不切实际。
- `多任务学习`：多任务学习是指同时训练一个模型完成多个任务。例如，在训练GPT/LLM模型时，可以让模型同时完成文本分类、情感分析等任务，从而使得模型可以学习到更加多样化的知识。在多任务学习的过程中，可以将额外的知识添加到其他任务中，从而间接地影响到模型在主要任务上的表现。

【2023-4-22】基于llama-index和ChatGPT API定制私有对话机器人的方式。

方案
- 1、fine-tunes微调。用大量数据对GPT模型进行微调，实现一个理解文档的模型。
  - 但微调需要花费很多money，而且需要一个有实例的大数据集。也不可能在文件有变化时每次都进行微调。
  - 微调不可能让模型 “知道“ 文档中的所有信息，而是要教给模型一种新的技能。
  - 因此，微调不是一个好办法。
- 2、将私有文本内容作为prompt的上下文，访问ChatGPT。
  - openai api存在最大长度的限制，ChatGPT 3.5的最大token数为4096，如果超过长度限制，会直接对文档截断，存在上下文丢失的问题。
  - 并且api的调用费用和token长度成正比，tokens数太大，则每次调用的成本也会很高。

### llama-index

【2023-4-23】参考
- [定制自己的文档问答机器人](https://zhuanlan.zhihu.com/p/623523968)
- [LlamaIndex ：面向QA 系统的全新文档摘要索引](https://mp.weixin.qq.com/s/orODrHefDpr-gHNyjxhXmg)

既然tokens有限制，那么有没有对文本内容进行**预处理**的工具？不超过token数限制。
- 借助llama-index可以从文本中只提取出相关部分，然后将其反馈给prompt。
- [llama-index](https://gpt-index.readthedocs.io/en/latest/), [github](https://github.com/jerryjliu/llama_index)支持许多不同的数据源，如API、PDF、文档、SQL 、Google Docs等。

[llama-index](https://gpt-index.readthedocs.io/en/latest/) Ecosystem
- 支持多种文件格式：support parsing a wide range of file types: .pdf, .jpg, .png, .docx, etc.
- 🏡 [LlamaHub](https://llamahub.ai), 包含各类插件，如：网页、faiss语义索引、b站视频脚本、ES、Milvus、数据库等
- 🧪 [LlamaLab](https://github.com/run-llama/llama-lab)

【2023-5-17】[基于ChatGPT的视频摘要应用开发](https://www.toutiao.com/article/7230786095158690362)
- 当文档被送入 LLM 时，它会根据其大小分成块或节点。 然后将这些块转换为嵌入并存储为向量。
- 当提示用户查询时，模型将搜索向量存储以找到最相关的块并根据这些特定块生成答案。 例如，如果你在大型文档（如 20 分钟的视频转录本）上查询“文章摘要”，模型可能只会生成最后 5 分钟的摘要，因为最后一块与上下文最相关 的“总结”。
- ![image](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/d0a76dbf2a11400f97220283ea233fa9~noop.image?_iz=58558&from=article.pc_detail&x-expires=1684911936&x-signature=dohd7TRWXXfBH5PRvGLj3ldXBh0%3D)

流程图
- ![flow](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/38966bfef5f641f294301647b92def7e~noop.image?_iz=58558&from=article.pc_detail&x-expires=1684911936&x-signature=Mdb8NbIuzxqhc1X9FW60XawIOK0%3D)

一种全新的 LlamaIndex 数据结构：**文档摘要索引**，与传统**语义搜索**相比，检索性能更好

多数构建 LLM 支持的 QA 系统步骤：
- 获取**源文档**，将每个文档拆分为**文本块**
- 将**文本块**存储在**向量数据库**中
- 查询时，通过**嵌入相似性** 和/或 **关键字过滤器**来检索文本块。
- 执行响应并**汇总**答案

由于各种原因，这种方法检索性能有限。
- 文本块**缺乏全局上下文**。通常query上下文超出了特定块中索引的内容。
- 仔细调整 top-k / 相似度分数阈值。
  - 假设值太小，你会错过上下文。
  - 假设值值太大，并且成本/延迟可能会随着更多不相关的上下文而增加，噪音增加。
- 嵌入选择的上下文不一定最相关。
  - 嵌入本质上是在文本和上下文之间分别确定的。

添加**关键字过滤器**是增强检索结果的一种方法。
- 但需要手动或通过 NLP 关键字提取/主题标记模型为每个文档充分确定合适的关键字。
- 此外，还需要从查询中充分推断出正确的关键字。

LlamaIndex中提出了一个新索引，为每个文档提取/索引**非结构化文本摘要**。
- 该索引可以提高检索性能，超越现有的检索方法。有助于索引比单个文本块更多的信息，并且比关键字标签具有更多的语义。

如何构建？
- 提取每个文档，并使用 LLM 从每个文档中提取**摘要**。
- 将文档拆分为**文本块**（节点）。摘要和节点都存储在文档存储抽象中。
- 维护从**摘要**到**源文档/节点**的映射。

在查询期间，根据摘要检索相关文档以进行查询：
- 基于 **LLM** 的检索：向 LLM 提供文档摘要集，并要求 LLM 确定: 哪些文档是相关的+相关性分数。
- 基于 **嵌入** 的检索：根据摘要嵌入相似性（使用 top-k 截止值）检索相关文档。

注意
- 检索文档**摘要**的方法不同于基于**嵌入**的文本块检索。**文档摘要索引**检索**任何**选定文档的所有节点，而不是返回节点级别的相关块。

存储文档的摘要还可以实现基于 LLM 的检索。
- 先让 LLM 检查简明的文档摘要，看看是否与查询相关，而不是一开始就将整个文档提供给 LLM。
- 这利用了 LLM 的推理能力，它比基于嵌入的查找更先进，但避免了将整个文档提供给 LLM 的成本/延迟

带**摘要**的文档检索是**语义搜索**和所有文档的强力摘要之间的“中间地带”。

示例
- 构建方法见原文：[LlamaIndex ：面向QA 系统的全新文档摘要索引](https://mp.weixin.qq.com/s/orODrHefDpr-gHNyjxhXmg)

```sh
pip install llama-index # install
```

```py
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader('data').load_data() # 加载数据
index = GPTVectorStoreIndex.from_documents(documents) # 创建索引
query_engine = index.as_query_engine() # 初始化查询引擎
response = query_engine.query("What did the author do growing up?") # 执行查询
print(response) # 返回结果
# --------- 持久化向量索引 ---------
from llama_index import StorageContext, load_index_from_storage
index.storage_context.persist() # 持久化存储（默认放内存）
# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="./storage")
# load index
index = load_index_from_storage(storage_context)
```


高级api

```py
query_engine = doc_summary_index.as_query_engine(
  response_mode="tree_summarize", use_async=True
)
response = query_engine.query("What are the sports teams in Toronto?")
print(response)
```

底层api

```py
# use retriever as part of a query engine
from llama_index.query_engine import RetrieverQueryEngine

# configure response synthesizer
response_synthesizer = ResponseSynthesizer.from_args()

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)
# query
response = query_engine.query("What are the sports teams in Toronto?")
print(response)
```



安装

```sh
pip install openai
pip install llama-index
```

调用代码
- construct_index方法中，使用llama_index的相关方法，读取data_directory_path路径下的txt文档，并生成索引文件存储在index_cache_path文件中。

```py
from llama_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper,ServiceContext
from langchain import OpenAI 
import gradio as gr 
import sys 
import os 
os.environ["OPENAI_API_KEY"] = 'your openai api key'
data_directory_path = 'your txt data directory path'
index_cache_path = 'your index file path'
​
#构建索引
def construct_index(directory_path): 
        max_input_size = 4096 
        num_outputs = 2000 
        max_chunk_overlap = 20 
        chunk_size_limit = 500
      
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=num_outputs))
        # 按最大token数500来把原文档切分为多个小的chunk
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=chunk_size_limit)
        # 读取directory_path文件夹下的文档
        documents = SimpleDirectoryReader(directory_path).load_data() 
 
        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        # 保存索引
        index.save_to_disk(index_cache_path) 
        return index 
        
def chatbot(input_text): 
        # 加载索引
        index = GPTSimpleVectorIndex.load_from_disk(index_cache_path) 
        response = index.query(input_text, response_mode="compact") 
        return response.response 
        
if __name__ == "__main__":
        #使用gradio创建可交互ui  
        iface = gr.Interface(fn=chatbot, 
                        inputs=gr.inputs.Textbox(lines=7, label="Enter your text"), 
                        outputs="text", 
                        title="Text AI Chatbot") 
        index = construct_index(data_directory_path) 
        iface.launch(share=True)
```

llama-index的工作原理如下：
- 创建文本块索引
- 找到最相关的文本块
- 使用相关的文本块向 GPT-3（或其他openai的模型） 提问
- 在调用query接口的时候，llama-index默认会构造如下的prompt:

```sh
"Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the question: {query_str}\n"
```

使用以上prompt请求openai 的模型时，模型根据提供的上下文和提出的问题，使用其逻辑推理能力得到想要的答案。

![](https://pic2.zhimg.com/80/v2-9aa943fe84bc25da03b866e7f52a940d_1440w.webp)

【2023-4-13】[如何为GPT/LLM模型添加额外知识？](https://www.zhihu.com/question/591935281/answer/2979220793)


#### 如何分句

【2023-5-25】llama-index的分句方法：加自定义部分（前后缀等）→调用nltk.tokenize.punkt分句（自定义句末正则）→按照chunk_size截断→分句列表，[源码](https://github.com/jerryjliu/llama_index/blob/c5a4cc1581cc6ee8277f970e7b0b2cbbd6351eb5/llama_index/langchain_helpers/text_splitter.py#LL267C7-L267C23)



### retrieve-then-generate

1、retrieve-then-generate：类ChatGPT Retrieval Plugin的技术方案
 
核心：根据 输入query 检索本地/私有数据库/文档中的文档片段（检索可以是文本检索或基于向量的检索），作为扩充的上下文 context，通过 prompt template 组合成一个完整的输入，继而调用模型生成response。

简版工作流：
- chunk -> index -> retrieve -> construct input -> LLM
 
推荐开源工具：
- （1）OpenAI 的官方插件：[ChatGPT Retrieval Plugin](https://github.com/openai/chatgpt-retrieval-plugin)
- （2）llama-index：[https://github.com/jerryjliu/llama_index](https://github.com/jerryjliu/llama_index)，提供了一个本地/私有数据收集（ingestion）和数据索引（indexing）的解决方案，构建起外部数据和 LLM 之间的接口。

一个利用 llama-index 定制个人论文检索的示例：[llama_index/examples/paul_graham_essay at main · jerryjliu/llama_index](https://github.com/jerryjliu/llama_index/tree/main/examples/paul_graham_essay)。
 
（在没有OpenAI API的情况下，llama-index 支持调用自定义的 LLM。）
 
（3）LangChain：[langchain](https://github.com/hwchase17/langchain)，也是为了更好的构建外部数据、其他应用与 LLM 进行交互的接口层框架。

LangChain应用参考示例：[GPT-4 & LangChain——PDF聊天机器人-地表最强全文搜索](https://www.bilibili.com/read/cv22589352)。
 
llama-index 和 LangChain 可以组合使用，LangChain 中提供了 面向不同任务的 prompt template 和 prompt chain。
 
### 基于 fine-tuning 的方式

2、基于 fine-tuning 的方式，相比于第一种方案，基于 fine-tuning 的方式需要额外的训练开销，同时还是会受限于LLM的最大长度限制。

“让 LLM 具备理解定制数据库的能力”是很有挑战的目标，同时也会有很多应用场景。

使用Hugging Face实现将维基百科的知识库添加到GPT-2模型中
- 作者：[小斐实战](https://www.zhihu.com/question/591935281/answer/2960837503)

```py
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# 加载预训练的GPT-2模型
model = GPT2LMHeadModel.from_pretrained('gpt2')

# 加载GPT-2的tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# 加载维基百科的文本文件，并将其转换为数据集
dataset = TextDataset(
    tokenizer=tokenizer,
    file_path='path/to/wiki.txt',
    block_size=128
)

# 创建data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, 
    mlm=False
)

# 设置训练参数
training_args = TrainingArguments(
    output_dir='./results',          # 输出目录
    num_train_epochs=3,              # 训练的轮数
    per_device_train_batch_size=8,   # 训练时每个GPU的batch size
    per_device_eval_batch_size=8,    # 验证时每个GPU的batch size
    evaluation_strategy='steps',     # 评估策略
    save_steps=500,                  # 多少步保存一次模型
    save_total_limit=2,              # 最多保存几个模型
    logging_steps=500,               # 多少步记录一次日志
    learning_rate=5e-5,              # 学习率
# 创建Trainer对象
trainer = Trainer(
model=model,
args=training_args,
train_dataset=dataset,
data_collator=data_collator,
prediction_loss_only=True
)

# 开始训练
trainer.train()

# 保存微调后的模型
trainer.save_model('./fine-tuned-model')
```

### 知识图谱增强

使用知识图谱增强GPT-2模型的示例代码：

```python
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# 加载预训练的GPT-2模型
model = GPT2LMHeadModel.from_pretrained('gpt2')
# 加载GPT-2的tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# 加载知识图谱: 表示一些实体和它们之间的关系。
knowledge_graph = {
    'John': {
        'is a': 'person',
        'born in': 'New York',
        'works at': 'Google'
    },
    'Google': {
        'is a': 'company',
        'headquartered in': 'California',
        'founded by': 'Larry Page and Sergey Brin'
    }
}

# 将知识图谱嵌入到模型中
model.resize_token_embeddings(len(tokenizer))
for entity in knowledge_graph.keys():
    entity_id = tokenizer.convert_tokens_to_ids(entity)
    entity_embedding = torch.randn(768)
    model.transformer.wte.weight.data[entity_id] = entity_embedding

# 生成句子
input_text = 'John works at'
input_ids = tokenizer.encode(input_text, return_tensors='pt')
output = model.generate(
    input_ids,
    max_length=50,
    do_sample=True,
    top_k=50
)
output_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(output_text)
```

## LLM应用

### LLM应用技术架构

- ![img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/871e57dfdaf24ba3a064e79ba0522a7b~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=eQeTT9ERDeEgx00BF9U9cVyrx%2FY%3D)

典型LLM应用开发架构四层：
- （1）`存储层`：主要为`向量数据库`，用于存储文本、图像等编码后的特征向量，支持向量相似度查询与分析。例如，我们在做文本语义检索时，通过比较输入文本的特征向量与底库文本特征向量的相似性，从而检索目标文本，即利用了向量数据库中的相似度查询（余弦距离、欧式距离等）。
  - 【代表性数据库】`Pinecone`、`Qdrant`。
- （2）`模型层`：选择大语言模型，如OpenAI的GPT系列模型、Hugging Face中的开源LLM系列等。
  - 模型层提供最核心支撑，包括聊天接口、上下文QA问答接口、文本总结接口、文本翻译接口等。
  - 【代表性模型】OpenAI的`GPT-3.5/4`，Anthropic的`Claude`，Google的`PaLM`，THU的`ChatGLM`等。
- （3）`服务层`：将各种语言模型或外部**资源整合**，构建实用的LLM模型。
  - `Langchain`是一个开源LLM应用框架，概念新颖，将LLM模型、向量数据库、交互层Prompt、外部知识、外部工具整合到一起，可自由构建LLM应用。
  - 【代表性框架】：`LangChain`，`AutoGPT`，`BabyAGI`，`Llama-Index`等。
- （4）`交互层`：用户通过UI与LLM应用交互
  - `langflow`是`langchain`的GUI，通过拖放组件和聊天框架提供一种轻松的实验和原型流程方式。
  - 实现一个简单的聊天应用，输入“城市名字”，聊天机器人回复“该城市的天气情况”。
  - 只需要拖动三个组件：PromptTemplate、OpenAI、LLMChain。完成PromptTemplate、OpenAI、LLMChain的界面化简单配置即可生成应用。
  - ![img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/03233a4e108f4ffaae147afcac50d03e~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=Z9D%2Blt1IqZVkBHXAGG1QjyORqLk%3D)


### LLM 应用

【2023-5-30】[万字长文：LLM应用构建全解析](https://www.toutiao.com/article/7238815236906680836)


#### LLM 应用总结

LLM 应用
- 1、**本地文档**知识问答助理(chat with pdf)，如：私域知识问答助理，智能客服，语义检索总结、辅助教学。
- 2、**视频**知识总结问答助理(chat with video)，如：视频自动编目、视频检索问答。
- 3、**表格**知识总结问答助理(chat with csv)，如：商业数据分析、市场调研分析、客户数据精准分析等

#### 1. Doc-Chat 文档问答

有大量本地文档数据，希望通过问答的方式快速获取想要的知识或信息，提高工作效率

解决方案：
> langchain + llms

本地化知识专属问答助理构建过程可简单概括如下：
- 第一步：**数据加载&预处理**（将数据源转换为text，并做text split等预处理）
- 第二步：**向量化**（将处理完成的数据embedding处理）
- 第三步：**召回**（通过向量检索工具Faiss等对query相关文档召回）
- 第四步：阅读理解，**总结答案**（将context与query传给llms，总结答案）
- ![img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/a978188a6d0d4d7db75e0818e286c32c~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=daelWSDLtJ1ruh29TjQfkyddRhg%3D)

##### （1）数据加载&预处理

加载pdf文件，对文本进行分块
- 每个分块的最大长度为3000个字符)。这个最大长度根据llm的输入大小确定，比如gpt-3.5-turbo最大输入是4096个token。
- 相邻块之间的重叠部分为400个字符，目的是每个片段保留一定的**上文信息**，后续处理任务利用重叠信息更好理解文本。

方案
- LangChain + FAISS + OpenAI

```py
import os

openai_api_key = 'sk-F9Oxxxxxx3BlbkFJK55q8YgXb6s5dJ1A4LjA'
os.environ['OPENAI_API_KEY'] = openai_api_key
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain import PromptTemplate

llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)

# data loader
loader = PyPDFLoader("data/ZT91.pdf")
doc = loader.load()
# text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=400)
docs = text_splitter.split_documents(doc)
```

##### （2）向量化

调用 OpenAIEmbeddings接口对文本进行向量化。
- 实际应用中，可使用开源模型，如下所示（OpenAIEmbeddings用的是第6个）。同时，中文embedding效果优秀的模型有百度的ERNIE。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/495e57fd56ea4ccc9790418aab290354~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=X394ecc51Xmjra6dRr2AiK6Bwqc%3D)

```py
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
```

##### （3）召回

用FAISS工具对输入文档构建FAISS索引，返回构建好的FAISS索引对象。

创建FAISS索引包含的工作有：
- 为索引分配内存空间；
- 选择合适的索引类型与参数（比如Flat IVFFlat等）；
- 将文档向量添加到索引中。

```py
docsearch = FAISS.from_documents(docs, embeddings)
# docsearch.as_retriever(search_kwargs={"k": 5})表示返回前5个最相关的chunks，默认是4，可以修改
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={"k": 5}), chain_type_kwargs={"prompt": PROMPT})


```

##### （4）总结答案

- 输入：query + context
- 输出：answer

其中 context 为通过faiss retriever检索出的相关文档：

特别的，为了让gpt只回答文档中的内容，在prompt_template 增加了约束：“请注意：请谨慎评估query与提示的Context信息的相关性，只根据本段输入文字信息的内容进行回答，如果query与提供的材料无关，请回答"对不起，我不知道"，另外也不要回答无关答案：”。即如果文档中没有用户提问相关内容，需要回答“不知道”，防止“答非所问”误导用户。

```py
prompt_template = """请注意：请谨慎评估query与提示的Context信息的相关性，只根据本段输入文字信息的内容进行回答，如果query与提供的材料无关，请回答"对不起，我不知道"，另外也不要回答无关答案：
    Context: {context}
    Question: {question}
    Answer:"""
# 输入：query + context
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
query = "实时画面无法查看，怎样解决？"
# FAISS检索出来的文档：retriever=docsearch.as_retriever(search_kwargs={"k": 5})
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={"k": 5}), chain_type_kwargs={"prompt": PROMPT})
# query为用户输入的提问
qa.run(query)
```

#### 2. 视频知识总结

LLM 看完视频，回答问题

需求描述：
- youtube等视频网站上每天都会产生大量视频，虽然推荐系统按照喜好进行了推荐，但观看大量有价值的视频依然面临挑战，如果能够快速了解视频内容，并得到关注的信息，将极大提高信息获取效率。

解决方案：
- langchain + transcript + llms
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/d565d76640004377abc1bcd989577fa7~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=XoDjL3a6u4n%2FIC8AbQRMBoJF9zQ%3D)

与pdf文档处理方式不同，YoutubeLoader库从youtube**视频链接**中加载数据，并转换为文档。
- 文档获取过程: 通过youtube-transcript-api获取的视频的字幕文件，这个字幕文件是youtube生成的。当用户将视频上传至youtube时，youtube会通过内置的语音识别算法将视频语音转换为文本。当加载youtube视频字幕文档后，接下来的处理工作与第一个例子类似。

```py
# 加载 youtube 频道
loader = YoutubeLoader.from_youtube_url('https://www.youtube.com/watch?v=_rcnWQ0b2lM')
# 将数据转成 document
documents = loader.load()
```

Question:
> “对视频中介绍的内容，逐条列举？”



#### 3. 表格问答

LLM 分析完 54万条数据，给出正确答案，完成了数据分析师1天的工作。

需求描述：
- 零售商有客户的交易数据。希望从数据中生成一些基本见解，以便识别最佳客户。
- 例如：按性别和年龄组划分的平均支出、每种类型的客户购买的产品、产品在哪个城市和商店的销售额最高等等
- 数据分析师将获取数据，编写一些 SQL 或 Python 或 R 代码，生成见解，数据分析师可能需要一天的时间来提供这些结果。

解决方案：
- langchain+llm + agents
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/c12a12fb285e431b94a9179846dd67e8~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=pGos9u09HxT9ppxKfL4lz74LA%2F4%3D)

任务
- (1) 显示表格中用户的数量
  - 验证: agent给出的答案完全正确
- (2) 年龄与消费金额之间相关性分析
  - 分析下年龄与消费金额之间的相关性：年龄与消费成正相关，但是相关性很弱
- (3) 产品销售量统计并画出柱状图
  - 统计每种产品的销售总量，并画柱状图


```py
import os
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

openai_api_key = 'sk-F9O70vxxxxxxxBlbkFJK55q8YgXb6s5dJ1A4LjA'
os.environ['OPENAI_API_KEY'] = openai_api_key

agent = create_csv_agent(OpenAI(openai_api_key=openai_api_key, temperature=0), 'train.csv', verbose=True)
# 统计用户数
agent.run("请按照性别对用户数量进行显示？")
# 年龄与消费金额之间的相关性
agent.run("在这份表格中,年龄与消费金额是否存在相关性?")
# 统计每种产品的销售总量，并画柱状图
agent.run("产品1总量,产品2总量,产品3总量分别是多少,将三个总量通过柱状图画出来并显示")
```




## 存储层：文档向量化

自研框架的选择
- 基于OpenAIEmbeddings，官方给出了基于embeddings检索来解决GPT无法处理长文本和最新数据的问题的实现方案。[参考](https://www.datalearner.com/blog/1051681543488862)
- 也可以使用 LangChain 框架。

参考
- [ChatGPT怎么建立私有知识库？](https://www.zhihu.com/question/596838257/answer/3004754396)
- [利用LangChain和国产大模型ChatGLM实现基于本地知识库的自动问答](https://www.zhihu.com/zvideo/1630964532179812353)

除了从文档中抓取数据，从指定网站URL抓取数据，实现智能客服外部知识库，可以借助ChatGPT写Python代码，PythonBeautiful Soup库的实现方式很成熟

大厂产品截图：智能客服知识库建设
- 企业资料库，关联大语言模型自动搜索
- ![a](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TdjoYAg6aFUKbz~noop.image?_iz=58558&from=article.pc_detail&x-expires=1684219771&x-signature=5kqgHWkZX6LPdrX2H9Zq59m%2BwO0%3D)
- 大模型文档知识抽取和“即搜即问”
- ![b](https://p9-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TdjoYkN7rAGx03~noop.image?_iz=58558&from=article.pc_detail&x-expires=1684219771&x-signature=gO%2FqHxavS7KVAfE08Mv0WayLjLQ%3D)
- ![b](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TdjoYmX2ImA5oO~noop.image?_iz=58558&from=article.pc_detail&x-expires=1684219771&x-signature=rlim2GCZ8zsapnPyzA47LCHJkEo%3D)


### 文本切分

LangChain 切分工具
- [Text Splitters文档](https://python.langchain.com/en/latest/modules/indexes/text_splitters.html): 选择对应的文本切分器，如果是通用文本的话，建议选择 `RecursiveCharacterTextSplitter`

```py
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 导入文本
loader = UnstructuredFileLoader("./data/news_test.txt")
# 将文本转成 Document 对象
data = loader.load()
print(f'documents:{len(data)}')

# 初始化加载器
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
# 切割加载的 document
split_docs = text_splitter.split_documents(data)
print("split_docs size:",len(split_docs))
```

### 相似度

相似度索引
- 只用embedding来计算句子的相似度

```py
# 初始化 prompt 对象
question = "2022年腾讯营收多少"
# 最多返回匹配的前4条相似度最高的句子
similarDocs = db.similarity_search(question, include_metadata=True,k=4)
# [print(x) for x in similarDocs]
```

接入ChatGLM来帮忙做总结和汇总

```py
from langchain.chains import RetrievalQA
import IPython
# 更换 LLM
qa = RetrievalQA.from_chain_type(llm=ChatGLM(temperature=0.1), chain_type="stuff", retriever=retriever)
# 进行问答
query = "2022年腾讯营收多少"
print(qa.run(query))
```

### 向量数据库

向量数据库（Vectorstores）用于存储文本、图像等编码后的**特征向量**，支持向量相似度查询与分析。
- 文本语义检索，通过比较输入文本的特征向量与底库文本特征向量的相似性，从而检索目标文本，即利用了向量数据库中的相似度查询（余弦距离、欧式距离等）。

因为数据相关性搜索其实是向量运算。所以，不管使用 openai api embedding 功能还是直接通过 向量数据库 直接查询，都需要将加载进来的数据 Document 进行**向量化**，才能进行向量运算搜索。

转换成向量也很简单，只需要把数据存储到对应的向量数据库中即可完成向量的转换。

官方也提供了很多的向量数据库供我们使用，包括：
- Annoy
- Chroma
- ElasticSearch
- FAISS
- Milvus
- PGVector
- Pinecone
- Redis

代表性数据库
- Chroma、Pinecone、Qdrand

更多支持的向量数据库使用方法，可转至链接。

### OpenAIEmbeddings

OpenAI官方的embedding服务

OpenAIEmbeddings：
- 使用简单，并且效果比较好；

问题
- 会消耗openai的token，特别是大段文本时，**消耗的token**还不少，如果知识库是比较固定的，可以考虑将每次生成的embedding做持久化，这样就不需要再调用openai了，可以大大节约token的消耗；
- 可能会有**数据泄露**的风险，如果是一些高度私密的数据，不建议直接调用。

```py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import VectorDBQA
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.embeddings.openai import OpenAIEmbeddings
import IPython
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")

embeddings = OpenAIEmbeddings()

# ---- 简洁版 -------
from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()
```

### HuggingFaceEmbeddings

HuggingFaceEmbeddings：

可以在HuggingFace上面选择各种sentence-similarity模型来进行实验，数据都是在本机上进行计算
需要一定的硬件支持，最好是有GPU支持，不然生成数据可能会非常慢
生成的向量效果可能不是很好，并且HuggingFace上的中文向量模型不是很多。

```py
from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import IPython
import sentence_transformers

embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
    "text2vec2":"uer/sbert-base-chinese-nli",
    "text2vec3":"shibing624/text2vec-base-chinese",
}

EMBEDDING_MODEL = "text2vec3"
# 初始化 hugginFace 的 embeddings 对象
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_dict[EMBEDDING_MODEL], )
embeddings.client = sentence_transformers.SentenceTransformer(
        embeddings.model_name, device='mps')
```

### Faiss


```py
from langchain.vectorstores import FAISS

db = FAISS.from_documents(split_docs, embeddings)
db.save_local("./faiss/news_test")
# 加载持久化向量
db = FAISS.load_local("./faiss/news_test",embeddings=embeddings)
# ====== 或 ========
vs_path = "./vector_store"
if vs_path and os.path.isdir(vs_path):
    vector_store = FAISS.load_local(vs_path, embeddings)
    vector_store.add_documents(docs)
else:
    if not vs_path:
        vs_path = f"""{VS_ROOT_PATH}{os.path.splitext(file)[0]}_FAISS_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}"""
    vector_store = FAISS.from_documents(docs, embeddings)

vector_store.save_local(vs_path)
docs = vector_store.similarity_search(query)
docs_and_scores = vector_store.similarity_search_with_score(query)
```


### Mulvus


```py
vector_db = Milvus.from_documents(
    docs,
    embeddings,
    connection_args={"host": "127.0.0.1", "port": "19530"},
)
docs = vector_db.similarity_search(query)
docs[0]
```


### Chroma

Chroma 比较轻量，直接安装库

```py
from langchain.vectorstores import Chroma
# 初始化加载器
db = Chroma.from_documents(split_docs, embeddings,persist_directory="./chroma/openai/news_test")
# 持久化
db.persist()
# 持久化后，可以直接选择从持久化文件中加载，不需要再重新就可使用了
db = Chroma(persist_directory="./chroma/news_test", embedding_function=embeddings)
```

```py
# pip install chromadb
# 加载索引
from langchain.vectorstores import Chroma
vectordb = Chroma(persist_directory="./vector_store", embedding_function=embeddings)
# 向量相似度计算
query = "未入职同事可以出差吗"
docs = vectordb.similarity_search(query)
docs2 = vectordb.similarity_search_with_score(query)
print(docs[0].page_content)
# 在检索器接口中公开该索引
retriever = vectordb.as_retriever(search_type="mmr")
docs = retriever.get_relevant_documents(query)[0]
print(docs.page_content)
```

### Pinecone

```py
import pinecone 

# Connecting to Pinecone
pinecone.deinit()
pinecone.init(
    api_key="YOUR_API_KEY",  # find at app.pinecone.io
    environment="YOUR_ENV"  # next to api key in console
)

# similarity_search
docsearch = Pinecone.from_documents(docs, embeddings, index_name="langchain-demo")
docs = docsearch.similarity_search(query)
print(docs[0].page_content)

# Create a Pinecone Service
pinecone_service = pinecone.Service()

# Create an Embedding Model
from langchain.embeddings.openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

# Create a Vectorstore
from langchain.vectorstores import Chroma
vectorstore = Chroma(embeddings, pinecone_service)

# Upload documents to Pinecone Vectorstore
from langchain.vectorstores import Chroma
docsearch = Chroma.from_documents(texts, embeddings, collection_name="collection_name")
```

### PGVector

```py
from langchain.vectorstores.pgvector import PGVector
import os
CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)
db = PGVector.from_documents(
    embedding=embeddings,
    documents=docs,
    collection_name="state_of_the_union",
    connection_string=CONNECTION_STRING,
)

query = "What did the president say about Ketanji Brown Jackson"
docs_with_score: List[Tuple[Document, float]] = db.similarity_search_with_score(query)
for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```


## 服务层：LLM框架

### LLaMA-Index



### LangChain

LangChain, 语言链条，也称：`兰链`，Harrison Chase创建的一个 Python 库，一种LLM语言大模型开发工具，几分钟内构建 GPT 驱动的应用程序。

LangChain 可以帮助开发者将LLM与其他计算或知识源结合起来，创建更强大的应用程序。

将语言模型与其他数据源相连接，并允许语言模型与环境进行交互，提供了丰富的API
- 与 LLM 交互
- LLM 连接外部数据源

AGI的基础工具模块库，类似模块库还有mavin。
-  LangChain provides an amazing suite of tools for everything around LLMs. 
- It’s kind of like HuggingFace but specialized for LLMs

LangChain 构建的有趣应用程序包括（但不限于）：
- 聊天机器人
- 特定领域的总结和问答
- 查询数据库以获取信息然后处理它们的应用程序
- 解决特定问题的代理，例如数学和推理难题

- [官方文档](https://python.langchain.com/en/latest/index.html)
- [GPT开发利器LangChain指北](https://mp.weixin.qq.com/s/VGtjETMC-hRTAiL6hp5gyg)
- [Github](https://github.com/hwchase17/langchain )(已经有4W多的star)

#### LangChain 组件

LangChain包含六部分组件
- ![img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/f101b9ecf540489280e7f95017243fb9~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=j8hpvldp7FTdOSIGCFjEyUEmbhs%3D)
- Models、Prompts、Indexes、Memory、Chains、Agents。

##### Document Loaders and Utils

LangChain 的 Document Loaders 和 Utils 模块分别用于**连接到数据源**和**计算源**。

当使用loader加载器读取到数据源后，数据源需要转换成 Document 对象后，后续才能进行使用。

Document Loaders 的Unstructured 可以将这些原始数据源转换为可处理的文本。

The following document loaders are provided:
- CSV Loader CSV文件
- DataFrame Loader 从 pandas 数据帧加载数据
- Diffbot 从 URL 列表中提取 HTML 文档，并将其转换为我们可以在下游使用的文档格式
- Directory Loader 加载目录中的所有文档
- EverNote 印象笔记
- Git 从 Git 存储库加载文本文件
- Google Drive Google网盘
- HTML HTML 文档
- Markdown
- Notebook 将 .ipynb 笔记本中的数据加载为适合 LangChain 的格式
- Notion
- PDF
- PowerPoint
- Unstructured File Loader 使用Unstructured加载多种类型的文件，目前支持加载文本文件、powerpoints、html、pdf、图像等
- URL 加载 URL 列表中的 HTML 文档内容
- Word Documents

##### Text Spltters

文本分割就是用来分割文本的。

为什么需要分割文本？
- 因为每次不管把文本当作 prompt 发给 openai api ，还是使用 embedding 功能, 都是有字符限制的。

比如将一份300页的 pdf 发给 openai api，进行总结，肯定会报超过最大 Token 错。所以这里就需要使用文本分割器去分割 loader 进来的 Document。
- 默认推荐的文本拆分器是 RecursiveCharacterTextSplitter。
- 默认情况以 [“\n\n”, “\n”, “ “, “”] 字符进行拆分。
- 其它参数说明：
  - length_function 如何计算块的长度。默认只计算字符数，但在这里传递令牌计数器是很常见的。
  - chunk_size：块的最大大小（由长度函数测量）。
  - chunk_overlap：块之间的最大重叠。有一些重叠可以很好地保持块之间的一些连续性（例如，做一个滑动窗口）
- CharacterTextSplitter 默认情况下以 separator="\n\n"进行拆分
- TiktokenText Splitter 使用OpenAI 的开源分词器包来估计使用的令牌

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


##### （1）Models（模型）：LLM选择

（1）Models（模型）: 可选择不同的LLM与Embedding模型。可以直接调用 API 工作，也可以运行本地模型。
- LLMs
- Chat Models
- HuggingFace Models
- Text Embedding：用于文本的向量化表示。设计用于与嵌入交互的类
  - 用于实现基于知识库的问答和semantic search，相比 fine-tuning 最大的优势：不用进行训练，并且可以实时添加新的内容，而不用加一次新的内容就训练一次，并且各方面成本要比 fine-tuning 低很多。
  - 例如，可调用OpenAI、Cohere、HuggingFace等Embedding标准接口，对文本向量化。
  - 两个方法：`embed_documents` 和 `embed_query`。最大区别在于接口不同：一种处理**多**个文档，而另一种处理**单**个文档。
  - 文本嵌入模型集成了如下的源：AzureOpenAI、Hugging Face Hub、InstructEmbeddings、Llama-cpp、OpenAI 等

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

openai_api_key = 'sk-F9O70vxxxxxlbkFJK55q8YgXb6s5dJ1A4LjA'
os.environ['OPENAI_API_KEY'] = openai_api_key

llm = OpenAI(model_name="gpt-3.5-turbo")
# llm = OpenAI(model_name="text-davinci-003", n=2, best_of=2)
print(llm("讲个笑话，很冷的笑话"))
# 为什么鸟儿会成为游泳高手？因为它们有一只脚比另一只脚更长，所以游起泳来不费力！（笑）
llm_result = llm.generate(["Tell me a joke", "Tell me a poem"])
llm_result.llm_output    # 返回 tokens 使用量
```

模型拉到本地使用的好处：
- 训练模型
- 可以使用本地的 GPU
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


##### （2）Prompts（提示语）: 模板化

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

name_template = """
我想让你成为一个起名字的专家。给我返回一个名字的名单. 名字寓意美好，简单易记，朗朗上口.
关于{name_description},好听的名字有哪些?
"""
# 创建一个prompt模板
prompt_template = PromptTemplate(input_variables=["name_description"], template=name_template)
description = "男孩名字"
print(prompt_template.format(name_description=description))
# 我想让你成为一个起名字的专家。给我返回一个名字的名单. 名字寓意美好，简单易记，朗朗上口.关于男孩名字,好听的名字有哪些?
```

##### （3）Indexes（索引）：文档结构化

Indexes（索引）：文档结构化, 以便LLM更好的交互
- 索引是指对文档进行结构化的方法，以便LLM能够更好的与之交互。

该组件主要包括：Document Loaders（`文档加载器`）、Text Splitters（`文本拆分器`）、VectorStores（`向量存储器`）以及Retrievers（`检索器`）。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/5078c23e1fea4bee99746ebec0847be5~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=Uzl65uwWtcvNhfi1OHpX8u%2BGzko%3D)
- `文本检索器`：将特定格式数据转换为文本。输入可以是 pdf、word、csv、images 等。
- `文本拆分器`：将长文本拆分成小的**文本块**，便于LLM模型处理。
  - 由于模型处理数据时，对输入长度有限制，因此需要对长文本进行**分块**。
  - 不同语言模型对块的大小定义不同，比如OpenAI的GPT对分块的长度通过token大小来限制，比如GPT-3.5是**4096**，即这个分块所包含的Token数量不能超过4096。
  - 一般的分块方法：首先，对长文本进行**断句**，即分成一句一句话。然后，计算每句话包含的token数量，并从第一句话开始往后依次累加，直到达到指定数量，组成为1个分块。依次重复上述操作。比如按照**字母**切分的`Character`，按照**token**切分的`Tiktoken`等。
- `向量存储器`：存储提取的文本向量，包括Faiss、Milvus、Pinecone、Chroma等。
- `向量检索器`：通过用户输入的文本，检索器负责从底库中检索出特定相关度的文档。度量准则包括余弦距离、欧式距离等。

示例

```py
# pip install chromadb
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
# 指定要使用的文档加载器
from langchain.document_loaders import TextLoader
documents = TextLoader('../state_of_the_union.txt', encoding='utf8')
# 接下来，我们将文档拆分成块。
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

###### Retrievers

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


##### （4）Chains（链条）：组合链路

Chains（链条）：将LLM与其他组件结合, 链允许将多个组件组合在一起以创建一个单一的、连贯的应用程序。

Chain提供了一种将各种组件统一到应用程序中的方法。
- 例如，创建一个Chain，它接受来自用户的输入，并通过PromptTemplate将其格式化，然后将格式化的输出传入到LLM模型中。
- 通过多个Chain与其他部件结合，可生成复杂的链，完成复杂的任务。
- ![Chains示意图](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/4d5ba1c00889406fb3bc7c86fbb9660f~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=pLKYIarzSV1QkVxKv%2Blc0t8lDrE%3D)

LLM与其他组件结合，创建不同应用，一些例子：
- 将LLM与**提示模板**相结合
- 第一个 LLM 的输出作为第二个 LLM 的输入, **顺序组合**多个 LLM
- LLM与**外部数据**结合，比如，通过langchain获取youtube视频链接，通过LLM视频问答
- LLM与**长期记忆**结合，比如聊天机器人

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
```

执行多个chain
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

##### （5）Agents（智能体）：其他工具

“链”可以帮助将一系列 LLM 调用链接在一起。
- 然而，在某些任务中，调用顺序通常是**不确定**的。下一步可能取决于用户输入和前面步骤中的响应。

LangChain 库提供了代理“Agents”，根据**未知**输入而不是硬编码来决定下一步采取的行动。 

Agent 使用LLM来确定要采取哪些行动以及按什么顺序采取的行动。操作可以使用工具并观察其输出，也可以返回用户。创建agent时的参数：
- 工具：执行特定职责的功能。比如：Google搜索，数据库查找，Python Repl。工具的接口当前是一个函数，将字符串作为输入，字符串作为输出。
- LLM：为代理提供动力的语言模型。
- 代理：highest level API、custom agent. 要使用的代理。这应该是一个引用支持代理类的字符串。由于本笔记本侧重于最简单、最高级别的 API，因此仅涵盖使用标准支持的代理。如果您想实施自定义代理，请参阅自定义代理的文档（即将推出）。

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
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Use Agent
agent.run("Ask a question related to the documents")
```

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

##### （6）Memory（记忆）：

对于像聊天机器人这样的应用程序，需要记住以前的对话内容。
- 但默认情况下，LLM对历史内容**没有记忆功能**。LLM的输出只针对用户当前的提问内容回答。
- 为解决这个问题，Langchain提供了**记忆组件**，用来管理与维护历史对话内容。
- ![memory示意图](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/c64ff3021d1a4ba68c3a6a5dd470cdc6~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=M2fWwrITBkva%2BXT%2BiQINk6VD54M%3D)

langchain提供不同的Memory组件完成内容记忆，下面列举四种：
- `ConversationBufferMemory`：记住**全部对话内容**。这是最简单的内存记忆组件，它的功能是直接将用户和机器人之间的聊天内容记录在内存中。[img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/8b04d8cc8c8f462bafa21bc473066efc~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=ljnOnmukL7V9UH5OzY4l%2BpwkfpU%3D)
- `ConversationBufferWindowMemory`：记住**最近k轮**的聊天内容。与之前的ConversationBufferMemory组件的差别是它增加了一个窗口参数，它的作用是可以指定保存多轮对话的数量。[img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/a830075b33094ef38f3aea87010fdd58~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=BbNKPeRu0j9knJWw02kEPUOu1uI%3D)
  - ​在该例子中设置了对话轮数k=2，即只能记住前两轮的内容，“我的名字”是在前3轮中的Answer中回答的，因此其没有对其进行记忆，所以无法回答出正确答案。
- `ConversationSummaryMemory`：ConversationSummaryMemory它不会将用户和机器人之前的所有对话都存储在内存中。它只会存储一个用户和机器人之间的**聊天内容的摘要**，这样做的目的可能是为了节省内存开销和token的数量。
  - ConversationSummaryMemory[第一轮对话](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/6b3c8f69e31440af9cb954bc903fd65d~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=X8kxNoQQtJqKKBIufAI5%2BGTprxo%3D): 你好，我是王老六
  - ConversationSummaryMemory[第二轮对话](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/ab4fbe8ad6cb4286a1e8f9e10141d2ef~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686034275&x-signature=tf%2FsfV5MF%2BIK7yWow48%2BvO%2FV%2BqY%3D): 你叫什么名字
  - 在第一轮对话完成后，Memory对第一轮对话的内容进行了总结，放到了摘要中。在第二轮对话中，LLM基于摘要与该轮的问题进行回答。
- `VectorStored-Backed Memory`: 将所有之前的对话通过**向量**的方式存储到VectorDB（向量数据库）中，在每一轮新的对话中，会根据用户的输入信息，匹配向量数据库中**最相似的K组**对话。





国内不少LLm团队采用langChain，集成llm本地化知识库

langChain，babyAGI 想做AGI生态，这个就有些力不从心了。autoGPT好一点，相对简单。

langChain，babyAGI的子模块，都是几百个。特别是langChain，模块库居然有600多张子模块map架构图

[无需OpenAI API Key，构建个人化知识库的终极指南](https://mp.weixin.qq.com/s/ponKZ1OaHXX2nzuSxXg8-Q)

构建知识库的主要流程：
1. 加载文档
2. 文本分割
3. 构建矢量数据库
4. 引入LLM
5. 创建qa_chain，开始提问


####  LangChain + Milvus

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
    """Interface for vector stores."""    @abstractmethoddef add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
kwargs:Any,
    ) ->List[str]:
"""Run more texts through the embeddings and add to the vectorstore."""    @abstractmethoddefsimilarity_search(
        self, query:str, k:int =4,kwargs: Any) -> List[Document]:
        """Return docs most similar to query."""def max_marginal_relevance_search(
        self, query: str, k: int = 4, fetch_k: int = 20) -> List[Document]:
        """Return docs selected using the maximal marginal relevance."""raise NotImplementedError

    @classmethod    @abstractmethoddef from_texts(
        cls: Type[VST],
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> VST:
        """Return VectorStore initialized from texts and embeddings."""
```                


将 Milvus 集成到 LangChain 中，实现几个关键函数：add_texts()、similarity_search()、max_marginal_relevance_search()和 from_text()

将 Milvus 集成到 LangChain 中的确存在一些问题，最主要的是 Milvus 无法处理 JSON 文件。目前，只有两种解决方法：
- 现有的 Milvus collection 上创建一个 VectorStore。
- 基于上传至 Milvus 的第一个文档创建一个 VectorStore。

#### LangChain + Faiss + Ray 实践

【2023-5-29】[Building an LLM open source search engine in 100 lines using LangChain and Ray](https://www.anyscale.com/blog/llm-open-source-search-engine-langchain-ray)
- Building the index: Build a document index easily with Ray and Langchain
- ![](https://images.ctfassets.net/xjan103pcp94/4OzISThpksdKgjZ0gVJUiB/85bb7fccdfef1df3d061c57e9af1062a/index-langchain.jpg)
- Build a document index 4-8x faster with Ray
- ![](https://images.ctfassets.net/xjan103pcp94/7tDpD5Q7nxtRyX9lgDvbkI/6209fbd875c5cd379c2289ef6f6554f0/Screen_Shot_2023-04-16_at_6.20.10_PM.png)
- Serving: Serve search queries with Ray and Langchain
- ![](https://images.ctfassets.net/xjan103pcp94/1g6zBePU72Rmz5MBH2reaB/db400e9bbbc445d7214d45658f81992f/Screen_Shot_2023-04-16_at_9.42.46_PM.png)


#### LangChain+ChatGLM 本地问答

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


### 微软guidance（LangChain简化）

【2023-5-26】[微软发布langChain杀手：guidance架构图全球首发](https://mp.weixin.qq.com/s/tdN5KXSXfM9dKDMWbXV2WA)

微软发布guidance模块库，并迅速登上github网站TOP榜首：
- guidance，传统提示或链接更有效、更高效地控制新式语言模型。
- 协助用户将生成、提示和逻辑控制交错到单个连续流中，以匹配语言模型实际处理文本的方式。
- 简单的输出结构，如思维链及其许多变体（例如ART，Auto-CoT等）已被证明可以提高LLM的性能。
- 像GPT-4这样更强大的LLM的出现允许更丰富的结构，并使该结构更容易，更便宜。

简单来说，微软guidance模块库，是langChain模块库的**简化版**，或者说：langChain杀手。

### ChatGLM QA

【2023-5-22】
- [基于chatglm搭建文档问答机器人](https://zhuanlan.zhihu.com/p/622418308): 道路交通安全法领域，不到100行的python文件
  - 基于langchain/llama-index已经可以快速完成类似的功能，但代码量大，学习门槛高
- [chatglm-qabot-v2: 从q-d匹配到q-q匹配](https://github.com/xinsblog/chatglm-qabot)
- [chatglm-qabot](https://github.com/xinsblog/chatglm-qabot)

一些关键组件的配置：
- LLM使用的是清华的chatglm-6b
- 计算embedding用的是苏神的**simbertV2**
- 没做embedding的索引优化，直接放list里暴力查找
- 每次默认查找top3相关的文档片段用于构造prompt
- 构造prompt的模板见代码
- 生成答案的长度没做限制，要做的话在代码中加请求chatglm的参数即可

```py
import sys

# 初始化问答机器人
qabot = QaBot(doc_path="data/中华人民共和国道路交通安全法.txt", chatglm_api_url=sys.argv[1])
# 根据文档回答问题
answer, _ = qabot.query('酒后驾驶会坐牢吗')
```

初始化的代码如下

```py
def __init__(self, doc_path: str, chatglm_api_url: str):
    # 加载预训练模型，用于将文档转为embedding
    pretrained_model = "junnyu/roformer_chinese_sim_char_small"
    self.tokenizer = RoFormerTokenizer.from_pretrained(pretrained_model)
    self.model = RoFormerForCausalLM.from_pretrained(pretrained_model)
    # 加载文档，预先计算每个chunk的embedding
    self.chunks, self.index = self._build_index(doc_path)
    # chatglm的api地址
    self.chatglm_api_url = chatglm_api_url
```

每次问答的代码如下

```py
def query(self, question: str) -> Tuple[str, str]:
    # 计算question的embedding
    query_embedding = self._encode_text(question)
    # 根据question的embedding，找到最相关的3个chunk
    relevant_chunks = self._search_index(query_embedding, topk=3)
    # 根据question和最相关的3个chunk，构造prompt
    prompt = self._generate_prompt(question, relevant_chunks)
    # 请求chatglm的api获得答案
    answer = self._ask_chatglm(prompt)
    # 同时返回答案和prompt
    return answer, prompt
```

效果
- ![](https://pic3.zhimg.com/80/v2-f263dca70c9ae78e85f2284f1f66685e_1440w.webp)
- ![](https://pic1.zhimg.com/80/v2-70c79cadf68c65c30160dedf8ef17b34_1440w.webp)
- ![](https://pic4.zhimg.com/80/v2-c323e0e63b47f2cb006dddba14ef57ab_1440w.webp)

基于chatglm做文档问答，通常的做法是"先检索再整合"，大致思路
- 首先准备好文档，并整理为纯文本的格式。把每个文档切成若干个小的chunks
- 调用文本转向量的接口，将每个chunk转为一个向量，并存入向量数据库
- 当用户发来一个问题的时候，将问题同样转为向量，并检索向量数据库，得到相关性最高的一个chunk
- 将问题和chunk合并重写为一个新的请求发给chatglm的api

将用户请求的query和document做匹配，也就是所谓的`q-d匹配`。

q-d匹配的问题
- query和document在**表达方式存在较大差异**，通常query是以**疑问句**为主，而document则以**陈述说明**为主，这种差异可能会影响最终匹配的效果。
- 一种改进的方法是不做`q-d匹配`，而是先通过document生成一批候选的question，当用户发来请求的时候，首先是把query和候选的question做匹配，进而找到相关的document片段
- 另一个思路通过HyDE去优化
  - 为query先生成一个假答案，然后通过假答案去检索，这样可以省去为每个文档生成问题的过程，代价相对较小

第一种方法就是'`q-q匹配`'，具体思路如下：
- 首先准备好文档，并整理为纯文本的格式。把每个文档切成若干个小的chunks
- 部署chatglm的api，[部署方法](https://github.com/THUDM/ChatGLM-6B#api%E9%83%A8%E7%BD%B2)
- 调api，根据每个chunk生成5个候选的question，使用的prompt格式为'请根据下面的文本生成5个问题: ...'，生成效果见下图：
  - ![](https://pic2.zhimg.com/80/v2-7790ad31e0621bff9e10233b448100f1_1440w.jpg)
- 调用文本转向量的接口，将生成的question转为向量，并存入向量数据库，并记录question和原始chunk的对应关系
- 用户发来一个问题时，将问题同样转为向量，并检索向量数据库，得到相关性最高的一个question，进而找到对应的chunk
- 将问题和chunk**合并重写**为一个新的请求发给chatglm的api

[chatglm-qabot](https://github.com/xinsblog/chatglm-qabot)
- qabot_v1.py实现了q-d匹配方法
- qabot_v2.py实现了q-q匹配方法

`q-d匹配`和`q-q匹配`的代码差异
- 初始化构建索引的差异如下：
  - ![](https://pic1.zhimg.com/80/v2-e3e8a1922e93fe67a6432866882b4490_1440w.webp)
- 查询索引时的差异如下：
  - ![](https://pic2.zhimg.com/80/v2-273d529bbcd4577f55003cd6fe508fa5_1440w.webp)

测试问题为行驶证的式样由谁来监制，v1和v2的效果对比如下：
- ![](https://pic2.zhimg.com/80/v2-14832aaedad809d62ce0d9157c770c69_1440w.webp)

在构建索引阶段，v2花费的时间是远超过v1的：

```sh
# 计算chunks的embedding: 
100%|██████████| 20/20 [00:02<00:00, 7.81it/s]
# 生成question并计算embedding: 
100%|██████████| 20/20 [07:24<00:00, 22.24s/it]
```


## 定制知识库

【2023-5-24】
- [基于 ChatGLM-6B 搭建个人专属知识库](https://www.toutiao.com/article/7236562318920876596)
- [如何使用LangChain＋LLM 来构建本地知识库](https://mp.weixin.qq.com/s/ponKZ1OaHXX2nzuSxXg8-Q)

### 业务场景

调整 prompt，匹配不同的知识库，让 LLM 扮演不同的角色
- • 上传公司财报，充当财务分析师
- • 上传客服聊天记录，充当智能客服
- • 上传经典Case，充当律师助手
- • 上传医院百科全书，充当在线问诊医生

### 问题

微调的瓶颈
- 需要专业知识，很多计算资源和时间，以便在不同超参数设置训练多个模型，并选择最佳的一个
- 动态扩展比较差，新增和修改原有的数据都要重新微调一次。

总之，微调对非专业人员不友好。

如何不用微调就能实现垂直领域的专业问答？
- 方案：ChatGLM-6B + langchain 实现个人专属知识库

### 技术原理

技术原理
- 加载文件 -> 读取文本 -> 文本分割 -> 文本向量化 -> 问句向量化 -> 在文本向量中匹配出与问句向量最相似的top k个 -> 匹配出的文本作为上下文和问题一起添加到 prompt 中 -> 提交给 LLM 生成回答。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/0d835cc528ba470d8e0e000f950780c7~noop.image?_iz=58558&from=article.pc_detail&x-expires=1685601997&x-signature=5lntZ3rovTBKBRNYBptf8gdfeOM%3D)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/ddc11018f9324f6cae76611a7486894b~noop.image?_iz=58558&from=article.pc_detail&x-expires=1685601997&x-signature=O88KtsSqlFFGJqlLUTLF4IzYYhs%3D)

核心技术是: 向量 embedding
- 将用户知识库内容经过 embedding 存入向量知识库，然后用户每一次提问也会经过 embedding，利用向量相关性算法（例如余弦算法）找到最匹配的几个知识库片段，将这些知识库片段作为上下文，与用户问题一起作为 prompt 提交给 LLM 回答

典型的prompt

```json
已知信息：
{context} 
根据上述已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”，不允许在答案中添加编造成分，答案请使用中文。 
问题是：{question}
```

### 实现

```sh
# 下载源码
git clone https://github.com/imClumsyPanda/langchain-ChatGLM.git
# 安装依赖
cd langchain-ChatGLM
pip install -r requirements.txt
# 下载模型

# 安装 git lfs
git lfs install
# 下载 LLM 模型
git clone https://huggingface.co/THUDM/chatglm-6b /your_path/chatglm-6b
# 下载 Embedding 模型
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese /your_path/text2vec
# 模型需要更新时，可打开模型所在文件夹后拉取最新模型文件/代码
git pull
```

模型下载完成后，请在 configs/model_config.py 文件中，对embedding_model_dict和llm_model_dict参数进行修改。

```py
embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "/your_path/text2vec"
}
llm_model_dict = {
    "chatyuan": "ClueAI/ChatYuan-large-v2",
    "chatglm-6b-int4-qe": "THUDM/chatglm-6b-int4-qe",
    "chatglm-6b-int4": "THUDM/chatglm-6b-int4",
    "chatglm-6b-int8": "THUDM/chatglm-6b-int8",
    "chatglm-6b": "/your_path/chatglm-6b",
}
```

启动服务

```py
# Web 模式启动
pip install gradio
python webui.py
# API 模式启动
python api.py
# 命令行模式启动
python cli_demo.py
```

### 效果

gradio页面
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/558af5fd53d34b5a859afddbc82a331c~noop.image?_iz=58558&from=article.pc_detail&x-expires=1685601997&x-signature=N%2FKm%2FGcW8WSiFxrAAD04P3klhig%3D)

Chatgpt-Next-Web 项目基础上进行了适配修改，打造了一款面向用户使用的本地知识库前端。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/55d11a03e5a742ce9c201aa355b38e3c~noop.image?_iz=58558&from=article.pc_detail&x-expires=1685601997&x-signature=fYTBeLwxkicrZBzWsYQusCVfiJk%3D)


### FastGPT

【2023-5-17】[FastGPT](https://github.com/c121914yu/FastGPT), 调用 gpt-3.5 和 embedding 构建自己的知识库。

知识库构建原理
- ![img](https://github.com/c121914yu/FastGPT/raw/main/docs/imgs/KBProcess.jpg?raw=true)

效果
- ![img](https://github.com/c121914yu/FastGPT/raw/main/docs/imgs/demo.png?raw=true)



在线体验
- 🎉 [fastgpt.run](https://fastgpt.run/) （国内版）
- 🎉 [ai.fastgpt.run](https://ai.fastgpt.run/) （海外版）



## 业界案例

### New Bing

- 优势：免费，快捷，可以联网，支持中英文，可以阅读本地PDF和网络论文，可以持续问答交互
- 缺点：不稳定，识别内容有限，甚至于信息量低于摘要的内容。经常会输出一半就断了。

### chatpdf

[ChatPDF](https://www.chatpdf.com) 界面干净，上传pdf后，直接对话。
- 上传速度很快，对话响应也非常的快。
- 对文档内容的解析很准确，包括一些隐藏在内部的知识点也可以快速搜索找到
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TdjoY88FTkaxGc~noop.image?_iz=58558&from=article.pc_detail&x-expires=1684219771&x-signature=A9yfB6gzbQrwWdUHuBZ2o0bRZzM%3D)

优势：
- 交互方便，容易上手，可以持续问答交互缺点：全文总结信息量较低，问答模式偏向于关键词定位，然后上下文翻译，且已经收费，每月5刀。只支持本地PDF文档上传。

### scispace

- 优势：交互方便，容易上手，可以持续问答交互，支持本地论文上传，可以公式截图解析，可以解释伪代码
- 缺点：对中文支持较差，全文总结效果较差。

### aminer.cn

清华唐杰老师他们组的工作！
- ![](https://pic1.zhimg.com/80/v2-33843cf159df1ca9e4a28fa32a15a759_1440w.webp?source=1940ef5c)
- ![](https://pic1.zhimg.com/80/v2-765efacd5340b65de02e79087ee91a07_1440w.webp?source=1940ef5c)

- 优势：有热点论文推送！有论文打分，和别人的提问记录
- 缺点：语义理解有限

### ChatPaper 开源

中科大出品：ChatPaper, Use ChatGPT to summarize the arXiv papers. 全流程加速科研，利用chatgpt进行论文总结+润色+审稿+审稿回复
- 功能：论文（离线/在线）总结+论文润色+AI审稿+AI审稿回复等功能。
- [github](https://github.com/kaixindelele/chatpaper), [demo](https://chatpaper.org/)

问题：
- 前面几款工具都面临一个问题，全文总结的信息量较低，因为GPTs的输入token是**远低于**论文的全文文本的，而简单的翻译总结摘要，又拿不到多少有效信息

方案：
- 将abstract和introduction进行压缩，然后输入给chat进行总结

效果
- 每篇文章，调用五次chat，可以获得7到8成的信息量，并且格式化输出成中国人容易看懂的文本，极大的降低了大家的阅读门槛。几乎可以达到，AI花一分钟总结，人花一分钟看总结，就可以判断这篇文章是否需要精读的效果。
- 如果需要**精读**，则可以调用上面的各种工具，尤其推荐scispace和aminer.


### PandasGPT

[PandaGPT](https://www.pandagpt.io/), 访问速度偏慢，UI对话样式一言难尽，没有一个版块不是互相遮挡的
- 已有3w个文档，10w个问题
- 上传文档，直接针对文档问答; 还能生成知识图谱，Generate Knowledge Graph
- ![](https://uploads-ssl.webflow.com/6405047c9d73416a60b878b4/6405068dec8bf7442171f160_Screenshot%202023-03-05%20at%204.15.30%20PM.png)

- 问题回答基本到位，相比ChatPDF，略显啰嗦
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TdjoY8iElGGYks~noop.image?_iz=58558&from=article.pc_detail&x-expires=1684219771&x-signature=BO6bt9JW5V%2Fsitc%2F%2FKWe6sBmUHY%3D)

类似的，还有 AMiner 上的华智冰

### ChatDOC

【2023-3-28】[ChatDOC](https://chatdoc.com/)文档阅读工具，支持中文！又快又免费！使用 ChatGPT 阅读文件的AI问答机器人
- 基于 ChatGPT 的文件阅读助手，支持中英文，可以快速从上传研究论文、书籍、手册等文件中提取、定位和汇总文件信息，并通过聊天的方式在几秒钟内给出问题的答案。
- ChatDOC 还可以理解文档中的表格或文字，优化其数据分析性能，并为每个回答提供直接引用的来源，方便核实AI的解读准确性。
- ChatDOC 目前免费，文件大小限制为 200 页，最多可以上传 5 个文档。在即将更新的版本中，还支持跨多个文档的综合查询和问答。
- ![](https://pic2.zhimg.com/80/v2-c73f17ecea423a82aad0ac7c110bd625_720w.webp)


### typeset

[typeset](https://typeset.io)
- 主打论文检索，也支持pdf文档解读。
- 上传、对话响应都十分缓慢，对话的效果差，很多知识点无法解读，一律回复无法找到这个问题的答案。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TdjoY9mB4FVHsf~noop.image?_iz=58558&from=article.pc_detail&x-expires=1684219771&x-signature=DjAXODUMrVrnilF7CAXPLSUT0qs%3D)

### privateGPT (本地、离线)

【2023-5-17】开源的 [privateGPT](https://www.privategpt.io/), [privateGPT代码](https://github.com/imartinez/privateGPT)，它使用GPT的强大功能，可以在100%私密的情况下与本地文档进行私密交互，不会有任何数据泄漏。
- 使用LLaMa、LangChain和GPT4All构建。
- [Demo](https://docs.boosterframework.com/)

The supported extensions are:
- .csv: CSV,
- .docx: Word Document,
- .enex: EverNote,
- .eml: Email,
- .epub: EPub,
- .html: HTML File,
- .md: Markdown,
- .msg: Outlook Message,
- .odt: Open Document Text,
- .pdf: Portable Document Format (PDF),
- .pptx : PowerPoint Document,
- .txt: Text file (UTF-8)


### ChatBase

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


# 结束