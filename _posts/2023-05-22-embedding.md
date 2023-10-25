---
layout: post
title:  嵌入/向量化技术 Embedding Tech
date:   2023-05-22 19:10:00
categories: 自然语言处理
tags: 向量化 milvus vector embedding
excerpt: 嵌入（Embedding）技术原理、案例
mathjax: true
permalink: /emb
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

## 向量化原理

基础模型大多基于 Transformer Encoder 预训练语言模型: `BERT`, `RoBERTa`，`Ernie`等

### 向量化方式

文本通过模型进行向量化的方式也有很多种不同的方式
- `cls`: 取最后一层的**第一个token**(CLS)作为句子向量
- `last_mean`: 对最后一层的**所有token取平均**pooling
- `first_last_mean`: 第一层和最后一层分别**平均池化**,再取平均
- `embedding_last_mean`: embedding层和最后一层分别平均池化,再取平均
- `last_weighted`: 最后一层按token位置**加权平均池化**


### 损失函数

语义相似度损失函数
1. PairInBatchNegCoSentLoss: 计算一个batch内每个句子与正例句子的余弦相似度,然后减去该句子与自身的相似度,再取log-sum-exp作为loss。
2. TripletInBatchNegCoSentLoss: 在PairInBatchNegCoSentLoss的基础上,额外加入负例样本,计算句子与正负例的相似度差值。希望正例相似度–负例相似度的差值越大。
3. PairInBatchNegSoftmaxContrastLoss: 将句子两两相似度矩阵进行softmax,并与句子本身的label计算交叉熵损失。
4. TripletInBatchNegSoftmaxContrastLoss: 在3的基础上加入负例样本。
5. PairInBatchNegSigmoidContrastLoss: 将句子两两相似度矩阵进行sigmoid,高于对角线的部分取负对数作为loss。
6. TripletInBatchNegSigmoidContrastLoss: 在5的基础上加入负例样本。
7. CoSentLoss: 输入预测相似度矩阵和真实相似度矩阵,计算两者差值进行log-sum-exp作为loss。这个损失是苏神提出来的，将排序的逻辑引入到了对比损失中。

语义相似的损失函数——主要思路是构建句子之间的**相似度矩阵**,然后通过比较正例和负例的相似度,采用交叉熵、log-sum-exp等方式计算loss,优化模型的句子表示,使得正例相似度更高。


### 训练策略

训练策略
1. FullParametersTraining: **全参数**微调,不进行任何修改,所有参数都参与训练。
2. BitFitTraining: 只训练**某些**关键词参数,其他参数固定。通过keywords指定要训练的参数名。
3. PrefixTraining: 只训练**前缀**tokens对应的embedding参数。通过additional_special_tokens指定前缀tokens,并只训练这些tokens的embedding。

这些策略可以平衡语料大小与模型大小,降低过拟合风险,帮助模型快速适应下游任务。通常先做全参数训练预热一下,再使用部分固定或前缀训练等策略微调到特定下游任务。

## 向量化方案

可选
- 单独的embedding服务
- LLM里的embedding

### LLM Embedding

【2023-8-1】[使用LLMs进行句子嵌入不如直接用BERT](https://mp.weixin.qq.com/s/mdC8EJ2Ajs8a_DCaxAET3Q)
- [Scaling Sentence Embeddings with Large Language Models](https://arxiv.org/abs/2307.16645.pdf)
- 代码 [scaling_sentemb](https://github.com/kongds/scaling_sentemb)

上下文学习方法使LLMs生成高质量的**句子嵌入**，无需微调，其性能可与当前的**对比学习**方法相媲美。

模型参数超过十亿规模会对语义文本相似性（STS）任务的性能造成影响。然而，最大规模的模型超越了其他对比方法，取得了迁移任务上的最新最优结果。同时，还采用当前的对比学习方法对LLMs进行了微调，其中结合了本文提出的基于提示的方法的 2.7B OPT模型，在STS任务上的结果超过了4.8B ST5，达到了最新最优的性能。

问题探讨
1. **PromptEOL方法与之前的句子表示方法有何不同**？PromptEOL 在句子嵌入方面有何优势？
  - PromptEOL方法是一种显式单词限制,基于提示的方法，用于在LLMs中表示句子。
  - 相比于之前的方法，PromptEOL方法在使用LLMs时更为兼容。通过将句子嵌入为提示 “`This sentence: “[text]” means`” ，生成下一个token，并提取最终token的**隐藏向量**作为句子嵌入。PromptEOL表示能力更强。
2. 比较PromptEOL方法与其他两种方法（平均和使用最后一个token）时，**为什么PromptEOL方法能够表现得更好**？
  - PromptEOL方法在不同参数设置下的LLMs中都能显著提升句子表示性能。相较于平均和使用最后一个token的方法，在句子嵌入过程中，PromptEOL方法通过使用提示来引导LLMs生成下一个token，并提取最终token的隐藏向量。
  - 这种提示-based的方法有助于在LLMs中更好地捕捉到句子的语义信息，从而提高句子表示的效果。
3. **为什么即使LLMs的参数比BERT更多，但在句子表示任务上仍表现不如BERT**？ 
  - 尽管LLMs 参数数量比BERT更多，但在使用同样句子表示方法下，LLMs（例如OPT）在句子表示任务上仍然无法超越 BERT。
  - 可能因为BERT具有**双向注意力机制**，可以隐含地将整个语义信息压缩到单个的 `[MASK]` token中。
  - 而LLMs通过提示（PromptEOL方法）方式在句子表示中引入了**单向生成**的限制，可能无法充分地捕捉到句子的全局语义信息，导致在句子表示任务上的性能相对较低。
4. **In-Context Learning的概念是什么**？如何与句子嵌入相关联？ 
  - In-Context Learning是一种基于**上下文学习**的句子嵌入方法。上下文中学习提供更丰富的句子嵌入生成过程。文章提出了两种自动生成演示文本的方法，用于在上下文学习中的句子嵌入过程中提供文字输出。演示文本用于指导模型在上下文中生成想要的句子嵌入。通过使用这种带有演示的上下文学习方法，可以增强句子嵌入的质量和表现能力。
5. 如何运用Fine-tuning方法来改善LLMs在句子表示任务中的性能？这种方法有哪些优势？ 
  - 通过Fine-tuning方法结合**对比学习**框架，可改善LLMs在句子表示任务中的性能。为了解决Fine-tuning过程中内存需求大的问题，采用了高效调优的方法。
  - 通过使用对比学习框架，以及结合高效调优方法，可以减少Fine-tuning过程中的内存需求，从而提高LLMs在句子表示任务中的性能。这种方法的优势在于可以在保证句子表示质量的同时，降低计算成本和内存消耗，提高了方法的实用性和可扩展性。


```py
# (1) Loading base model
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Import our models. The package will take care of downloading the models automatically
tokenizer = AutoTokenizer.from_pretrained("facebook/opt-2.7b")
model = AutoModelForCausalLM.from_pretrained("facebook/opt-2.7b")
tokenizer.pad_token_id = 0 
tokenizer.padding_side = "left"
texts = [
    "There's a kid on a skateboard.",
    "A kid is skateboarding.",
    "A kid is inside the house."
]
# (2) Use in-context learning to generate embeddings
# Directly using in-contex learning get embeddings
template = 'This_sentence_:_"A_jockey_riding_a_horse."_means_in_one_word:"Equestrian".This_sentence_:_"*sent_0*"_means_in_one_word:"'
inputs = tokenizer([template.replace('*sent_0*', i).replace('_', ' ') for i in texts], padding=True,  return_tensors="pt")
with torch.no_grad():
    embeddings = model(**inputs, output_hidden_states=True, return_dict=True).hidden_states[-1][:, -1, :]

# (3) Use contrastive learning models to generate embeddings
# Using trained LoRA to get embeddings
from peft import PeftModel
peft_model = PeftModel.from_pretrained(model, "royokong/prompteol-opt-2.7b", torch_dtype=torch.float16)
template = 'This_sentence_:_"*sent_0*"_means_in_one_word:"'
inputs = tokenizer([template.replace('*sent_0*', i).replace('_', ' ') for i in texts], padding=True, return_tensors="pt")
with torch.no_grad():
    embeddings = peft_model(**inputs, output_hidden_states=True, return_dict=True).hidden_states[-1][:, -1, :]
Setup
```

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
- [M3E，开源中文 Embedding 模型新 SOTA](https://blog.csdn.net/sinat_30045277/article/details/131208109)

由于 GPT 使用的 Transformer 模型的自身特性，导致模型只能从固定长度的上下文中生成文本。那么，当要模型感知更广阔的上下文时，该怎么做呢？

领域内通用的解决方案: 将历史对话或者领域语料中的相关知识通过向量检索，再补充到 GPT 模型的上下文中。

这样，GPT 模型就不需要感知全部文本，而是有重点、有目的地只关心那些相关的部分，这和 Transformer 内部的 Attention 机制原理相似，使得文本嵌入模型变成了 GPT 模型的记忆检索模块。

但是长期以来，领域内一直缺少开源、可用的**中文文本嵌入模型**作为文本检索。
- 中文开源文本嵌入模型中最被广泛使用的 `text2vec` 主要是在中文自然语言推理数据集上进行训练的。
- OpenAI 出品的 `text-embedding-ada-002` 模型被广泛使用 ，虽然该模型效果较好，但此模型不开源、也不免费，同时还有数据**隐私**和数据**出境**等问题。

#### MokaHR 开源 M3E

最近，`MokaHR` 团队开发了一种名为 `M3E` 的模型，这一模型弥补了中文向量文本检索领域的空白， `M3E` 模型在中文同质文本 S2S 任务上在 6 个数据集的平均表现好于 `text2vec` 和 `text-embedding-ada-002` ，在中文检索任务上也优于二者。
- huggingface: [m3e-base](https://huggingface.co/moka-ai/m3e-base)

- 2023.06.08，添加**检索任务**的评测结果，在 T2Ranking 1W 中文数据集上，`m3e-base` 在 ndcg@10 上达到了 **0.8004**，超过了 `openai-ada-002` 的 **0.7786**
- 2023.06.07，添加**文本分类**任务的评测结果，在 6 种文本分类数据集上，m3e-base 在 accuracy 上达到了 0.6157，超过了 openai-ada-002 的 0.5956

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


#### 直接使用

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

#### M3E 微调

M3E微调实战：[uniem](https://github.com/wangyuxinwhy/uniem/tree/main)
- uniem 项目目标: 创建**中文**最好的通用文本嵌入模型。

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


### C-Pack - FlagEmbedding

#### 介绍

【2023-9-21】智源推出 [语义模型：FlagEmbedding](https://zhuanlan.zhihu.com/p/657056257)
- 论文: [C-Pack: Packaged Resources To Advance General Chinese Embedding](https://arxiv.org/pdf/2309.07597.pdf)
- 代码：[FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding)， [中文介绍](https://github.com/FlagOpen/FlagEmbedding/blob/master/README_zh.md)

数据集
- 由于embedding不是确定性任务，所以对数据的规模，多样性以及质量有很高的要求
  - 包括但不限于Retrieval，Clustering，Pair classification，Reranking，STS，Summarization，Classification）
- 为了能达到Embedding的高区分度，至少需要上亿级别的训练实例。
- 同时，数据集的需要来源尽量广泛来提高模型的泛化性（generality）。
- 数据增强（Data Argumentation）对于原始数据的质量有很高的要求，所以需要进行数据清洗（Data clean），否则容易引入噪声。

#### 原理

Training 训练一个 general-purpose 的text embeddings有两个重要因素：
- 1）一个好的编码器。
- 2）一个好的训练方案。

虽然说能够使用 unlabeled data 并基于 Bert 或者是T5能极大地提高预训练模型的性能，但是光这样还是不够的，需要通过复合的训练方案。
- 以面向嵌入（embedding）的预训练来准备文本编码器
- 对比学习需要从复杂的负采样中提高嵌入的可辨别性
- 基于指令微调来集成文本嵌入的不同表示能力

(1) Pre-training
- 使用为embedding任务量身定做的算法模型，wudao数据集，高质量，多样性的数据集来进行中文语言模型的预训练。
- 框架使用的是`RetroMAE`中的`MAE-style`，简单但是高效。Masked的文本被编码到其嵌入中，然后在轻量级解码器上恢复干净的文本：
- ![](https://pic1.zhimg.com/80/v2-0371ca9ad3f1db22a492ead11d5d5460_1440w.webp)
- 其中 Enc，Dec分别表示encoder和decoder，X， X'表示初始文本和masked 文本。

(2) General purpose fine-tuning
- 预训练模型用C-MTP的unlabeled data 进行对比学习，从negatives 来学习不同文本之间的差异
- ![](https://pic3.zhimg.com/80/v2-755911ce893ac29b57c54ad4aa3c3332_1440w.webp)
- p和q都是文本对，Q' 是negatives q'的集合，t是温度。对比学习的关键因素是negatives，除了negatives mining之外，还使用了`in-batch negative samples` 技术，同时使用大batch size（19200），github上的代码还有`cross device negatives`跨设备负样本。

(3) Task-speific fine-tuning
- 针对特定任务的微调。使用 C-MTP（labeled data）进一步微调嵌入模型。带标签的数据集较小但质量较高。然而，所包含的任务类型不同，其影响可能相互矛盾。这里作者用了两个方式去解决这个问题：
- 1）指令微调来帮助模型来区分不同的任务。对于每一个文本对(p,q), 特定任务的指令 $I_t$ 会被附加到query这一端，改写之后的query： $q' \leftarrow q + I_t$ . 这种指令是偏向于口语话的，例如“search relevant passages for the query”. 同时使用ANN-style策略进行negative sampling。

论文没有提出很新的训练方法、微调技巧，从基本内容上
- 先进行Bert类型的模型预训练，RetroMAE方法
- 然后进行无监督学习（对比学习）
- 最后是多任务的无监督学习（加入指令来区分不同的任务）。

#### 效果

模型的效果表现出色，数据集的构建给之后的研究者提供了一个很好的Benchmark。
- ![](https://pic2.zhimg.com/80/v2-a1ec17e47b55792ab42188a7ebfa5ba1_1440w.webp)

baai-general-embedding 模型在 MTEB 和 C-MTEB 排行榜上都实现了最先进的性能
- 超过 OpenAI text-embedding-ada-002 和 m3e-large


#### 安装

```sh
pip install -U FlagEmbedding
```

#### FlagEmbedding 使用

```py
from FlagEmbedding import FlagModel
sentences = ["样例数据-1", "样例数据-2"]
model = FlagModel('BAAI/bge-large-zh-v1.5', 
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True) # 设置use_fp16为True可以加快计算，效果会稍有下降
embeddings_1 = model.encode(sentences)
embeddings_2 = model.encode(sentences)
similarity = embeddings_1 @ embeddings_2.T
print(similarity)

# 对于短查询到长文档的检索任务，请对查询使用 encode_queries() 函数，其会自动为每个查询加上指令
# 由于候选文本不需要添加指令，检索中的候选集依然使用 encode() 或 encode_corpus() 函数
queries = ['query_1', 'query_2']
passages = ["样例文档-1", "样例文档-2"]
q_embeddings = model.encode_queries(queries)
p_embeddings = model.encode(passages)
scores = q_embeddings @ p_embeddings.T
# ------ 计算相似度 --------
from FlagEmbedding import FlagReranker
reranker = FlagReranker('BAAI/bge-reranker-large', use_fp16=True) #设置 fp16 为True可以加快推理速度，效果会有可以忽略的下降

score = reranker.compute_score(['query', 'passage']) # 计算 query 和 passage的相似度
print(score)
scores = reranker.compute_score([['query 1', 'passage 1'], ['query 2', 'passage 2']])
print(scores)
```

Instruction参数 query_instruction_for_retrieval 请参照： [Model List](https://github.com/FlagOpen/FlagEmbedding/tree/master#model-list). 当加载微调后的模型时
- 如果没有在训练的json文件中为query添加指令，则将其设置为空字符串""; 
- 如果训练数据中为query添加了指令，更改为新设置的指令。

FlagModel支持`GPU`也支持`CPU`推理。
- 如果GPU可用，其默认优先使用GPU。
- 如果想禁止其使用GPU，设置 `os.environ["CUDA_VISIBLE_DEVICES"]=""` 
- 为提高效率，FlagModel默认会使用所有的GPU进行推理。如果想要使用具体的GPU，请设置 `os.environ["CUDA_VISIBLE_DEVICES"]`。

#### Langchian 中使用

Langchian中使用bge模型：

```py
from langchain.embeddings import HuggingFaceBgeEmbeddings
model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity
model = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
```

#### transformers 中使用

transformers 中使用

```py
from transformers import AutoTokenizer, AutoModel
import torch
# Sentences we want sentence embeddings for
sentences = ["样例数据-1", "样例数据-2"]

# Load model from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-large-zh-v1.5')
model = AutoModel.from_pretrained('BAAI/bge-large-zh-v1.5')

# Tokenize sentences
encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
# 对于短查询到长文档的检索任务, 为查询加上指令
# encoded_input = tokenizer([instruction + q for q in queries], padding=True, truncation=True, return_tensors='pt')

# Compute embeddings
with torch.no_grad():
    model_output = model(**encoded_input)
    # Perform pooling. In this case, cls pooling.
    sentence_embeddings = model_output[0][:, 0]
# normalize embeddings
sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
print("Sentence embeddings:", sentence_embeddings)
# ------ 计算相似度 --------
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-reranker-large')
model = AutoModelForSequenceClassification.from_pretrained('BAAI/bge-reranker-large')
model.eval()

pairs = [['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']]
with torch.no_grad():
    inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
    scores = model(**inputs, return_dict=True).logits.view(-1, ).float()
    print(scores)
```


### AnglE 香港理工

【2023-10-24】Embedding SOTA 是 AnglE, 在 STS13，STS14，STS15，STS16 以及 Sick-R 上都达到了 SOTA。
- Arxiv: [AnglE-optimized Text Embeddings](https://arxiv.org/pdf/2309.12871.pdf)
- Github: [AnglE](github.com/SeanLee97/AnglE)
- Huggingface: SeanLee97/angle-llama-7b-nli-20231027

高质量文本嵌入在提高语义文本相似度（STS）任务中起着至关重要的作用，这是大型语言模型（LLM）应用中的关键组成部分。然而，现有文本嵌入模型面临的一个普遍挑战是**梯度消失**问题，主要是优化目标中依赖**余弦函数**，而余弦函数具有**饱和区域**。

本文提出了一种新颖的**角度优化**文本嵌入模型——`AnglE`。 核心思想是在复杂空间中引入角度优化。这种方法有效地缓解了余弦函数饱和区域的不良影响，这可能会阻碍梯度并阻碍优化过程。

在现有的短文本STS数据集和从GitHub Issues收集的新的长文本STS数据集上进行了实验。此外，还研究了具有有限标记数据的特定领域STS场景，并探讨了AnglE如何与LLM注释数据配合使用。

各种任务上进行了广泛的实验，包括短文本STS、长文本STS和特定领域的STS任务。
- AnglE优于忽略余弦饱和区域的最先进的STS模型。
- 证明了AnglE生成高质量文本嵌入的能力以及角度优化在STS中的有用性。


```py
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig

peft_model_id = 'SeanLee97/angle-llama-7b-nli-v2'
config = PeftConfig.from_pretrained(peft_model_id)
tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)
model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path).bfloat16().cuda()
model = PeftModel.from_pretrained(model, peft_model_id).cuda()

def decorate_text(text: str):
    return f'Summarize sentence "{text}" in one word:"'

inputs = 'hello world!'
tok = tokenizer([decorate_text(inputs)], return_tensors='pt')
for k, v in tok.items():
    tok[k] = v.cuda()
vec = model(output_hidden_states=True, **tok).hidden_states[-1][:, -1].float().detach().cpu().numpy()
print(vec)
```





## 向量评估

ChatGPT记忆模块搜索优化——文本语义向量相似M3E模型微调实战

`语义相似度任务`(Semantic Textual Similarity)是自然语言处理中的一个基础任务,目的是评估两个文本片段在语义上的相似程度。

主要思路:
- 将文本映射到语义向量空间,也就是将文本转化为固定长度的向量表示。
- 计算两个文本向量之间的相似度,例如使用余弦相似度。
- 相似度高则表示两个文本在语义上相似,相似度低则表示语义不同。

难点在于获得合适的文本向量表示,需要模型能够捕捉文本的语义信息,忽略词汇表面的差异,根据上下文判断语义是否相近。

文本相似度比较的主要三种类型。
- `s2s`, 即 sentence to **sentence** ，代表了同质文本之间的嵌入能力，适用任务：文本相似度，重复问题检测，文本分类等
- `s2p`, 即 sentence to **passage** ，代表了异质文本之间的嵌入能力，适用任务：文本检索，GPT 记忆模块等
- `s2c`, 即 sentence to **code** ，代表了自然语言和程序语言之间的嵌入能力，适用任务：代码检索

语义相似度模型几个关键问题,包括: 数据格式、基础模型选择、文本向量化表示、损失函数设计和训练策略等都有所不同。

### 评测数据集

语义相似度任务数据集包括`STS-B`, `SICK` 等。模型训练过程中需要大量语义相关的文本对构成**监督数据**,损失函数则常采用`余弦相似度`与标注相似度的差异作为优化目标。

语义相似度是NLP系统中重要模块,应用包括: 问答匹配、短文本聚类、语义搜索等等。提高语义相似度的准确性是自然语言理解的关键步骤。


#### 数据格式

三种训练样本格式

示例如下:

1. `Pair` (句子对)：每个样本包含一个正例句子对。用于学习区分正例和负例句子。

```json
[{
    'text': 'I love apples',
    'positive_text': 'Apples are my favorite fruit'
},
{
    'text': 'I play football', 
    'positive_text': 'Football is an exciting sport'
}]
```

2. `Triplet` (三元组) ：每个样本包含一个正例句子和一个负例句子。可以更明确地学习区分正负样本。

```json
[{
    'text': 'I love apples',
    'positive_text': 'Apples are my favorite fruit',
    'negative_text': 'Bananas are too soft'
},
{
    'text': 'I play football',
    'positive_text': 'Football is an exciting sport',
    'negative_text': 'Basketball is also great'
}]
```

3. `Scored Pair` (打分句子对)：每个样本包含一对句子和它们的相似度分数。可以直接学习评估语义相似度。

```json
[{
    'text': 'I love apples',
    'scored_text': 'Apples are my favorite fruit',
    'score': 0.9 
},
{
    'text': 'I play football',
    'scored_text': 'Football is an exciting sport',
    'score': 0.8
}]
```

三者对比:
- Pair: 区分**正负**样本
- Triplet: 更**明确**的正负样本
- Scored Pair: 直接学习**语义相似度**

适用于不同的训练目标。


### 评测榜单

如何评估一个模型的好坏：[MTEB Leaderboard - a Hugging Face Space by mteb](https://link.zhihu.com/?target=https%3A//huggingface.co/spaces/mteb/leaderboard) 是针对**大规模文本表示**学习方法的一个**评测排行榜**。
- 将文本向量化模型在大量的评测数据集: 文本**分类**，**聚类**，文本**排序**，文本**召回**等大量数据集上进行评测，并给出一个平均的分数，来评估这个模型文本embeding的能力。

- ![](https://pic3.zhimg.com/80/v2-ada5462440f11d5cebc4bb1cb4c99322_1440w.webp)
- BGE模型效果目前最强，而 M3E 紧随其后，不同模型采取了不同训练数据，训练模型和训练策略。large的模型效果更好

除了以上综合榜单，不同模型在不同类型任务下的表现有区别。





## 向量检索

大规模情况下，如何低延迟检索文档？
- **近似最近邻**（ANN）算法。

`语义匹配`会直接决定是否能够检索到正确的知识

### 向量检索技术

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