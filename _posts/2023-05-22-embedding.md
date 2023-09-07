---
layout: post
title:  嵌入/向量化技术 Embedding Tech
date:   2023-05-22 19:10:00
categories: 自然语言处理
tags: 向量化 milvus
excerpt: 嵌入（Embedding）技术原理、案例
mathjax: true
permalink: /vec
---

* content
{:toc}


# 向量化


## 文本向量化

`嵌入`（Embedding）是一种将**文本或对象**转换为**向量表示**的技术，将词语、句子或其他文本形式转换为固定长度的向量表示。
- 嵌入向量是由一系列浮点数构成的**向量**。
- 通过计算两个嵌入向量之间的距离，可以衡量它们之间的相关性。距离较小的嵌入向量表示文本之间具有较高的相关性，而距离较大的嵌入向量表示文本之间相关性较低。

以 `Milvus` 为代表的`向量数据库`利用语义搜索（Semantic Search）更快地检索到相关性更强的文档。

详见：sklearn专题里的[文本向量化](sklearn#%E5%90%91%E9%87%8F%E5%8C%96)

## 文档向量化

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

都有ChatGPT了，为什么还要了解Embedding这种「低级货」技术？两个原因：
- 有些问题使用Embedding解决（或其他非ChatGPT的方式）会更加合理。通俗来说就是「杀鸡焉用牛刀」。
- ChatGPT**性能**方面不是特别友好，毕竟是逐字生成（一个Token一个Token吐出来的）。

更多：[ChatGPT相似度匹配笔记](https://github.com/datawhalechina/hugging-llm/blob/main/content/ChatGPT%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97%E2%80%94%E2%80%94%E7%9B%B8%E4%BC%BC%E5%8C%B9%E9%85%8D.ipynb)

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

## 向量化方案

### OpenAIEmbeddings

OpenAI官方的embedding服务

OpenAIEmbeddings：
- 使用简单，并且效果比较好；

#### OpenAI的Embedding服务

直接使用openai的embedding服务

```py
import os
import openai

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# OPENAI_API_KEY = "填入专属的API key"
openai.api_key = OPENAI_API_KEY

text = "我喜欢你"
model = "text-embedding-ada-002"
emb_req = openai.Embedding.create(input=[text], model=model)
emb = emb_req.data[0].embedding
len(emb), type(emb)
# 相似度计算
from openai.embeddings_utils import get_embedding, cosine_similarity

# 注意它默认的模型是text-similarity-davinci-001，我们也可以换成text-embedding-ada-002
text1 = "我喜欢你"
text2 = "我钟意你"
text3 = "我不喜欢你"
emb1 = get_embedding(text1)
emb1 = get_embedding(text1, "text-embedding-ada-002") # 指定模型
emb2 = get_embedding(text2)
emb3 = get_embedding(text3)
cosine_similarity(emb1, emb2) # 0.9246855139297101
cosine_similarity(emb1, emb3) # 0.8578009661644189
```

问题
- 会消耗openai的token，特别是大段文本时，**消耗的token**还不少，如果知识库是比较固定的，可以考虑将每次生成的embedding做持久化，这样就不需要再调用openai了，可以大大节约token的消耗；
- 可能会有**数据泄露**的风险，如果是一些高度私密的数据，不建议直接调用。

#### LangChain调用OpenAI

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

### M3E

【2023-7-14】[研究人员开源中文文本嵌入模型，填补中文向量文本检索领域的空白](https://www.toutiao.com/article/7254900867097625127)

由于 GPT 使用的 Transformer 模型的自身特性，导致模型只能从固定长度的上下文中生成文本。那么，当要模型感知更广阔的上下文时，该怎么做呢？

领域内通用的解决方案: 将历史对话或者领域语料中的相关知识通过向量检索，再补充到 GPT 模型的上下文中。

这样，GPT 模型就不需要感知全部文本，而是有重点、有目的地只关心那些相关的部分，这和 Transformer 内部的 Attention 机制原理相似，使得文本嵌入模型变成了 GPT 模型的记忆检索模块。

但是长期以来，领域内一直缺少开源、可用的**中文文本嵌入模型**作为文本检索。
- 中文开源文本嵌入模型中最被广泛使用的 `text2vec` 主要是在中文自然语言推理数据集上进行训练的。
- OpenAI 出品的 `text-embedding-ada-002` 模型被广泛使用 ，虽然该模型效果较好，但此模型不开源、也不免费，同时还有数据**隐私**和数据**出境**等问题。

#### MokaHR 开源 M3E

最近，`MokaHR` 团队开发了一种名为 `M3E` 的模型，这一模型弥补了中文向量文本检索领域的空白， `M3E` 模型在中文同质文本 S2S 任务上在 6 个数据集的平均表现好于 `text2vec` 和 `text-embedding-ada-002` ，在中文检索任务上也优于二者。
- huggingface: [m3e-base](https://huggingface.co/moka-ai/m3e-base)

M3E 是 Moka Massive Mixed Embedding 的缩写
- Moka，此模型由 MokaAI 训练，开源和评测，训练脚本使用 uniem ，评测 BenchMark 使用 MTEB-zh
- Massive，此模型通过千万级 (2200w+) 的中文句对数据集进行训练
- Mixed，此模型支持中英双语的同质文本相似度计算，异质文本检索等功能，未来还会支持代码检索
- Embedding，此模型是文本嵌入模型，可以将自然语言转换成稠密的向量

Tips:
- 使用场景主要是中文，少量英文的情况，建议使用 m3e 系列的模型
- 多语言使用场景，并且不介意数据隐私的话，我建议使用 openai text-embedding-ada-002
- 代码检索场景，推荐使用 openai text-embedding-ada-002
- 文本检索场景，请使用具备文本检索能力的模型，只在 S2S 上训练的文本嵌入模型，没有办法完成文本检索任务

M3E 模型中使用的数据集、训练脚本、训练好的模型、评测数据集以及评测脚本都已开源，用户可以自由地访问和使用相关资源。该项目主要作者、MokaHR 自然语言处理工程师王宇昕表示：
> “我相信 M3E 模型将成为中文文本向量检索中一个重要的里程碑，未来相关领域的工作，都可能从这些开源的资源中收益。”

M3E 使用 in-batch 负采样的对比学习的方式在句对数据集进行训练，为了保证 in-batch 负采样的效果，我们使用 A100 80G 来最大化 batch-size，并在共计 2200W+ 的句对数据集上训练了 1 epoch。训练脚本使用 [uniem](https://github.com/wangyuxinwhy/uniem/blob/main/scripts/train_m3e.py)

### 直接使用

```py
# pip install -U sentence-transformers
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('moka-ai/m3e-base')

#Our sentences we like to encode
sentences = [
    '* Moka 此文本嵌入模型由 MokaAI 训练并开源，训练脚本使用 uniem',
    '* Massive 此文本嵌入模型通过**千万级**的中文句对数据集进行训练',
    '* Mixed 此文本嵌入模型支持中英双语的同质文本相似度计算，异质文本检索等功能，未来还会支持代码检索，ALL in one'
]

#Sentences are encoded by calling model.encode()
embeddings = model.encode(sentences)

#Print the embeddings
for sentence, embedding in zip(sentences, embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")

```

##### 微调

uniem 提供了非常易用的 finetune 接口，几行代码，即刻适配！

```py
from datasets import load_dataset

from uniem.finetuner import FineTuner

dataset = load_dataset('shibing624/nli_zh', 'STS-B')
# 指定训练的模型为 m3e-small
finetuner = FineTuner.from_pretrained('moka-ai/m3e-small', dataset=dataset)
finetuner.run(epochs=1)
```

详见 [uniem 微调教程](https://github.com/wangyuxinwhy/uniem/blob/main/examples/finetune.ipynb)


### MUSE 多语种

【2023-8-31】2019年 META 推出的[MUSE](https://github.com/facebookresearch/MUSE), 包含很多小语种

A library for Multilingual Unsupervised or Supervised word Embeddings, whose goal is to provide the community with:
- state-of-the-art multilingual word embeddings (`fastText` embeddings aligned in a common space)
- large-scale high-quality bilingual dictionaries for training and evaluation

![](https://github.com/facebookresearch/MUSE/raw/main/outline_all.png)


### S-BERT

【2023-9-5】[s-bert](https://www.sbert.net/docs/pretrained_models.html)

claude推荐用 s-bert embedding

## 向量检索

大规模情况下，如何低延迟检索文档？
- **近似最近邻**（ANN）算法。

优化了检索速度，并返回近似（而非精确）的前 k 个最相似的邻居，以少许准确度损失换取大幅加速。

**ANN嵌入索引**是一种数据结构，高效地进行ANN搜索。在嵌入空间上构建分区，以便快速定位查询向量所在的特定空间。一些技术包括：
-   `局部敏感哈希`（`LSH`）：核心思想是创建哈希函数，使得相似的项有可能落入同一个哈希桶中。通过只需要检查相关的桶，我们可以高效地执行最近邻查询。
-   Facebook AI相似性搜索（`FAISS`）：它使用量化和索引的组合来实现高效的检索，支持CPU和GPU，并且由于其对内存的高效利用，可以处理数十亿个向量。
-   **分层可导航小世界**（`HNSW`）：受到“六度分隔”的启发，它构建了一个体现小世界现象的分层图结构。在这里，大多数节点可以通过最少的跳数从任何其他节点到达。这种结构允许HNSW从更广泛、更粗糙的近似开始查询，并逐渐在较低层次上缩小搜索范围。
-   **可扩展最近邻居**（`ScaNN`）：ANN通过两个步骤完成。
  - 首先，粗粒度量化减少了搜索空间。
  - 然后，在减少的集合内进行细粒度搜索。这是我见过的最佳召回率/延迟权衡。

局部敏感散列（LSH）是一组方法，用于将数据向量转换成散列值，同时保留其相似性信息，从而缩小搜索范围。

传统方法包括三个步骤：
- 矢量化：将原始文本编码成矢量。
  - K-gram 是由 k 个连续的标记词组成的词组。根据上下文，标记可以是单词或符号。切分的最终目的是使用收集到的 k-gram 对每个文档进行编码。
  - 句子 "learning datascience is fascinating "收集长度为 k = 3 的唯一字符串
- MinHashing：将向量转换成一种称为签名的特殊表示，可用于比较它们之间的相似性。
  - 向量的相似性可以通过`雅卡指数`(两个集合的交集)进行比较。请记住，两个集合的雅卡指数定义为两个集合中共同元素的数量除以所有元素的长度。
  - 编码向量的稀疏性: 计算两个单击编码向量之间的相似度得分将耗费大量时间。如果转换为密集格式会更有效率。是设计这样一个函数，将这些向量转换到一个较小的维度，并保留相似性信息。构建这种函数的方法叫做 MinHashing。
  - MinHashing 是一个哈希函数，对输入向量的分量进行排列，然后返回排列后的向量分量等于 1 的第一个索引, [img](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/83691a41b01b4055878f12ebed739141~tplv-tt-origin-asy1:5aS05p2hQOmXu-aVsOi1t-iIng==.image?_iz=58558&from=article.pc_detail&x-expires=1693980150&x-signature=KWF4IRvOK7clmV7XXfm9tVI0sn8%3D)
- LSH 功能：将签名块散列到不同的桶中。如果一对向量的签名至少有一次落在同一个桶中，它们就会被视为候选者。
  - 原始文本转化为保留相似性信息的等长密集签名。然而，这种密集签名通常仍然具有很高的维度，直接比较,效率很低。建立一个哈希表来加速搜索性能，但即使两个签名非常相似，只有一个位置不同，哈希值仍有可能不同（因为向量余数可能不同）。不过通常希望它们归入同一个桶中。
  - LSH 机制会建立一个由多个部分组成的哈希表，如果一对签名至少有一个相应的部分，就会被放入同一个桶中。
- [参考](https://www.toutiao.com/article/7264973689832096313/)

在评估ANN指数时，需要考虑一些因素，包括：
- **回忆**：它在与精确最近邻的比较中表现如何？    
- 延迟/吞吐量：每秒可以处理多少个查询？    
- **内存**占用：为了提供索引需要多少RAM？    
- 添加新项目的便利性：是否可以在不重新索引所有文档（LSH）或需要重建索引（ScaNN）的情况下添加新项目？    

没有最好，只有更合适。进行基准测试之前，首先定义功能和非功能需求。
- ScaNN在召回率和延迟之间的权衡方面表现出色（请参见此处的基准测试图表）。

详见
- [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/)
- [译文](https://mp.weixin.qq.com/s/XVH5sCSyGccKt9K8nvkzdA)

### 索引结构划分

【2023-8-25】按索引结构划分
- 树结构索引: 
- 图结构索引: 
- 分层聚类索引: 
- 向量量化索引: 

| 索引结构类型 | 原理 | 适用场景 | 示例 |
| --- | --- | --- | ---  |  
| **树结构**索引   |   -  | 低维空间相似性搜索<br>不适合高维空间,内存占用大,搜索慢 | KD-Tree, BallTree  |   
| **图结构**索引   |   -  | 高维空间实时相似性搜索,内存占用小，速度快 | HNSW  |   
| **分层聚类**索引 |   -  | 高维空间相似性搜索,性能和内存平衡 | Annoy  |    
| **向量量化**索引 |   -  | 大规模高维空间相似性搜索，api丰富 | Faiss (IVF,IVFPQ)  |    


### 相似性搜索

相似性搜索经常出现在 NLP 领域、搜索引擎或推荐系统中，在这些领域中，需要为查询检索最相关的文档或项目。

## 向量数据库

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


# 结束