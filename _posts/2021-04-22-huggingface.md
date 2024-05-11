---
layout: post
title:  Huggingface Transformers库 使用笔记
date:   2021-04-22 16:52:00
categories: 深度学习 技术工具
tags: NLP Transformer bert gpt tensorflow pytorch datasets
excerpt: 跟预训练语言模型一起成长壮大的创业公司
mathjax: true
permalink: /huggingface
---

* content
{:toc}


# Huggingface

![](https://huggingface.co/front/assets/huggingface_logo-noborder.svg)
- ![logo](https://img-blog.csdnimg.cn/20200904202104322.png)
- [demo](https://transformer.huggingface.co/)

## Hugging face 简介

[Hugging Face](https://huggingface.co/) 是一家总部位于纽约的聊天机器人初创服务商，开发的应用在青少年中颇受欢迎，相比于其他公司，Hugging Face更加注重产品带来的情感以及环境因素。

但更令它广为人知的是Hugging Face专注于NLP技术，拥有大型的开源社区。尤其是在github上开源的自然语言处理，预训练模型库 `Transformers`，已被下载超过一百万次，github上超过24000个star。

[Transformers](https://github.com/huggingface/transformers) 提供了NLP领域大量state-of-art的 预训练语言模型结构的模型和调用框架。
- 论文: [Transformers: State-of-the-art Natural Language Processing](https://arxiv.org/pdf/1910.03771)

PyTorch实现了从语言中识别情绪情感反讽的DeepMoji模型：https://github.com/huggingface/torchMoji

【2022-9-7】注册账户后[申请token](https://huggingface.co/settings/tokens)才能下载模型

【2024-1-25】[huggingface官方介绍及测试题](https://huggingface.co/learn/nlp-course/zh-CN/chapter1/3?fw=pt)

## Transformers 库

Transformers库 [GitHub](https://github.com/huggingface/transformers)
- [huggingface 快速上手](https://zhuanlan.zhihu.com/p/610171544)

### 介绍

- 最初的名称是 `pytorch-pretrained-bert`，随着BERT一起应运而生。
- Google 2018年10月底, 开源了[BERT](https://github.com/google-research/bert) 的tensorflow实现。当时，BERT以其强劲的性能，引起NLPer的广泛关注。
- 几乎与此同时，`pytorch-pretrained-bert` 也开始了第一次提交。
  - `pytorch-pretrained-bert` 用当时已有大量支持者的pytorch框架复现了BERT的性能，并提供预训练模型的下载，使没有足够算力的开发者们也能够在几分钟内就实现 state-of-art-fine-tuning。
- 2019年7月16日，在repo上已经有了包括 BERT，GPT，GPT-2，Transformer-XL，XLNET，XLM在内六个预训练语言模型，这时候名字再叫 pytorch-pretrained-bert 就不合适了，于是改成了`pytorch-transformers`，势力范围扩大了不少。
- 2019年6月, Tensorflow2的beta版发布，Huggingface也闻风而动。为了立于不败之地，又实现了TensorFlow 2.0和PyTorch模型之间的深层互操作性，可以在TF2.0/PyTorch框架之间随意迁移模型。
- 2019年9月, 发布了2.0.0版本，同时正式更名为 `transformers` 。到目前为止，transformers 提供了超过100种语言的，32种预训练语言模型，简单，强大，高性能，是新手入门的不二选择。

Huggingface名字演进

<div class="mermaid">
    flowchart LR
    %% 节点颜色
    classDef red fill:#f02;
    classDef green fill:#5CF77B;
    classDef blue fill:#6BE0F7;
    classDef orange fill:#F7CF6B;
    classDef grass fill:#C8D64B;
    %%节点关系定义
    B(2018年,BERT):::grass-.->|2018,诞生,pytorch版|A(pytorch-pretrained-bert):::blue
    T1(TensorFlow 1.0) -.->B
    E(Elmo):::orange-->|双向|B
    G(GPT):::orange-->|transformer|B
    T1-.->E
    T1-.->G
    A -->|2019年7月,模型扩充到6个| A1(pytorch-transformers):::green
    T2(Tensorflow 2.0)-.->|支持TF|A1
    T1-->|2019年6月|T2
    A1 -->|2019年9月,更名| A2(transformers):::green
    A2 -->|扩充,32种模型,100+种语言| A3(新版transformers):::green
</div>

### 安装

安装：
- transformers 包所需的 tensorflow 版本至少为2.2.0，而该版本对应的CUDA版本可能不同，如笔者使用的2.4.0版本tensorflow对应的CUDA是11版本

```shell
pip install transformers==2.2.0
pip install tensorflow
pip install numpy
# tf环境
pip install tensorflow-gpu==2.4.0
# pytorch环境
pip install torch
# 或 pytorch+transformers一起安装
pip install transformers[torch]
# 或 TensorFlow+transformers一起安装
pip install transformers[tf-cpu]
# 或源码安装
pip install git+https://github.com/huggingface/transformers
# 指定源
pip install transformers --trusted-host pypi.tuna.tsinghua.edu.cn
```

测试：

```python
import transformers
transformers.__version__
import pipeline
print(pipeline('sentiment-analysis')('I hate you'))"
```


### 框架理解


源码
- [ransformers/__init__.py](https://github.com/huggingface/transformers/blob/main/src/transformers/__init__.py)
- [解读](https://juejin.cn/post/7350510977052229668)

#### Auto 核心类

transformers 开源库核心组件包括3个：
- `Conﬁguration`：**配置**类，继承自`PretrainedConﬁg`，保存model或tokenizer的超参数，例如词典大小，隐层维度数，dropout rate等。配置类主要可用于复现模型。
- `Tokenizer`：**切词**类，继承自`PreTrainedTokenizer`，主要存储词典（**from_pretrained()**部分），token到index映射关系等。
  - 三件事情：①分词、②扩展词汇表、③识别并处理特殊token。
  - model-specific的特性，如特殊token，`[SEP]`, `[CLS]`等处理，token的type类型处理，语句最大长度等
  - 因此**tokenizer通常和模型是一对一适配**。比如BERT模型有BertTokenizer。
  - Tokenizer 实现方式有多种，如 word-level, character-level或者subword-level，其中subword-level包括Byte-Pair-Encoding，WordPiece。subword-level的方法目前是transformer-based models的主流方法，能够有效解决OOV问题，学习词缀之间的关系等。
  - Tokenizer主要为了将原始的语料编码成适配模型的输入。
- `Model`: **模型**类。封装了预训练模型的计算图过程，遵循着相同的范式，如根据token ids进行embedding matrix映射，紧接着多个self-attention层做编码，最后一层task-specific做预测。
  - 除此之外，Model还可以做一些灵活扩展，用于下游任务，例如在预训练好的Base模型基础上，添加task-specific heads。
  - 比如，language model heads，sequence classiﬁcation heads等。在代码库中通常命名为，XXX**ForSequenceClassification** or XXX**ForMaskedLM**，其中XXX是模型的名称（如Bert）， 结尾是预训练任务的名称 (MaskedLM) 或下游任务的类型(SequenceClassification)。


transformer 额外封装了`AutoConfig`, `AutoTokenizer`,`AutoModel`
- 通过**模型命名**就能定位所属的具体类
- 比如 ’bert-base-cased’，要加载BERT模型相关的配置、切词器和模型。

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-05-09T07:13:51.016Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36\&quot; etag=\&quot;5qBzsLmuwwd9dOJxDsPq\&quot; version=\&quot;24.3.1\&quot;&gt;\n  &lt;diagram id=\&quot;Lw-1uFHNzwHmlxUDpAkU\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;761\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-7\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;strokeWidth=2;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;216\&quot; y=\&quot;170\&quot; width=\&quot;395\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-8\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;strokeWidth=2;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;170\&quot; y=\&quot;300\&quot; width=\&quot;400\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-1\&quot; value=\&quot;模型类&amp;lt;br&amp;gt;Model\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=none;shadow=1;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;338\&quot; y=\&quot;310\&quot; width=\&quot;70\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-2\&quot; value=\&quot;分词类&amp;lt;br&amp;gt;Tokenizer\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#a20025;strokeColor=#6F0000;shadow=1;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;480\&quot; y=\&quot;310\&quot; width=\&quot;70\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-3\&quot; value=\&quot;数据集&amp;lt;br&amp;gt;Dataset\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;625\&quot; y=\&quot;310\&quot; width=\&quot;70\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-10\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-4\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-24\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-4\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-23\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-25\&quot; value=\&quot;继承\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;eTGUqoqL8qtCVFqHRuqP-24\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0571\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-4\&quot; value=\&quot;配置类&amp;lt;br&amp;gt;Configuration\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;185\&quot; y=\&quot;310\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-19\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-5\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-17\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-5\&quot; value=\&quot;&amp;lt;div&amp;gt;流水线&amp;lt;/div&amp;gt;Pipeline\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;258\&quot; y=\&quot;180\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-20\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-6\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-18\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-6\&quot; value=\&quot;&amp;lt;div&amp;gt;训练&amp;lt;/div&amp;gt;Trainer\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;468\&quot; y=\&quot;180\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-9\&quot; value=\&quot;Transformers库框架\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;348\&quot; y=\&quot;50\&quot; width=\&quot;170\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-11\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-1\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;253\&quot; y=\&quot;320\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;300\&quot; y=\&quot;250\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-12\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-2\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;363\&quot; y=\&quot;320\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;313\&quot; y=\&quot;250\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-13\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.678;exitY=-0.05;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-4\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-6\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;373\&quot; y=\&quot;330\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;323\&quot; y=\&quot;260\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-1\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-6\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;383\&quot; y=\&quot;340\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;333\&quot; y=\&quot;270\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-15\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-2\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-6\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;393\&quot; y=\&quot;350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;343\&quot; y=\&quot;280\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-16\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-3\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-6\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;403\&quot; y=\&quot;360\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;353\&quot; y=\&quot;290\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-17\&quot; value=\&quot;推理阶段\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#d0cee2;strokeColor=#56517e;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;268\&quot; y=\&quot;110\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-18\&quot; value=\&quot;训练/评估阶段\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#d0cee2;strokeColor=#56517e;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;472\&quot; y=\&quot;110\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-21\&quot; value=\&quot;核心组件\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;170\&quot; y=\&quot;270\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-22\&quot; value=\&quot;&amp;lt;b&amp;gt;&amp;lt;font color=&amp;quot;#333333&amp;quot;&amp;gt;功能&amp;lt;/font&amp;gt;&amp;lt;/b&amp;gt;: 保存model、tokenizer超参,便于复习模型\&quot; style=\&quot;text;whiteSpace=wrap;fillColor=none;html=1;fontColor=#0066CC;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;123\&quot; y=\&quot;360\&quot; width=\&quot;152\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-23\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); text-align: left;&amp;quot;&amp;gt;PretrainedConﬁg&amp;lt;/span&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;10\&quot; y=\&quot;315\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-26\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;dashPattern=1 1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-28\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;354\&quot; y=\&quot;350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-27\&quot; value=\&quot;继承\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;eTGUqoqL8qtCVFqHRuqP-26\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0571\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-28\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: left;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: initial;&amp;quot;&amp;gt;&amp;lt;font color=&amp;quot;#000000&amp;quot;&amp;gt;PreTrainedTokenizer&amp;lt;/font&amp;gt;&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;238\&quot; y=\&quot;400\&quot; width=\&quot;122\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-31\&quot; value=\&quot;&amp;lt;b&amp;gt;&amp;lt;font color=&amp;quot;#333333&amp;quot;&amp;gt;功能&amp;lt;/font&amp;gt;&amp;lt;/b&amp;gt;: 分词、扩展词表、识别特殊字符\&quot; style=\&quot;text;whiteSpace=wrap;fillColor=none;html=1;fontColor=#0066CC;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;320\&quot; y=\&quot;360\&quot; width=\&quot;152\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-32\&quot; value=\&quot;&amp;lt;b&amp;gt;&amp;lt;font color=&amp;quot;#333333&amp;quot;&amp;gt;功能&amp;lt;/font&amp;gt;&amp;lt;/b&amp;gt;: 封装模型计算图\&quot; style=\&quot;text;whiteSpace=wrap;fillColor=none;html=1;fontColor=#0066CC;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;480\&quot; y=\&quot;360\&quot; width=\&quot;152\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-33\&quot; value=\&quot;AutoConfig\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;textShadow=1;labelBorderColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;185.5\&quot; y=\&quot;470\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-34\&quot; value=\&quot;AutoModel\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;fontStyle=1;textShadow=1;labelBorderColor=none;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;328.5\&quot; y=\&quot;470\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-35\&quot; value=\&quot;AutoTokenizer\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#a20025;strokeColor=#6F0000;fontStyle=1;textShadow=1;labelBorderColor=none;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;470.5\&quot; y=\&quot;470\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-36\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B3B3B3;exitX=0.5;exitY=1;exitDx=0;exitDy=0;fontColor=#009900;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-4\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-33\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;253\&quot; y=\&quot;320\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;313\&quot; y=\&quot;230\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-37\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B3B3B3;exitX=0.5;exitY=1;exitDx=0;exitDy=0;fontColor=#009900;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-1\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-34\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;240\&quot; y=\&quot;360\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;240\&quot; y=\&quot;460\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;eTGUqoqL8qtCVFqHRuqP-38\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B3B3B3;exitX=0.5;exitY=1;exitDx=0;exitDy=0;fontColor=#009900;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;eTGUqoqL8qtCVFqHRuqP-2\&quot; target=\&quot;eTGUqoqL8qtCVFqHRuqP-35\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;250\&quot; y=\&quot;370\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;250\&quot; y=\&quot;470\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

通常上手时都会用Auto封装类来加载切词器和模型。


#### 示例

```py
# 加载与保存分词器
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-cased")
tokenizer.save_pretrained("./models/bert-base-cased/")
# 加载与保存模型
from transformers import AutoModel
# 所有存储在 HuggingFace Model Hub 上的模型都可以通过 Model.from_pretrained() 来加载权重，参数可以是 checkpoint 的名称，也可以是本地路径（预先下载的模型目录）
model = AutoModel.from_pretrained("bert-base-cased")
model.save_pretrained("./models/bert-base-cased/") # 保存模型

inputs = tokenizer(["来到美丽的大自然，我们发现"], return_tensors="pt")
# {'input_ids': tensor([[    1, 68846, 68881, 67701, 67668, 98899, 91935]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1]])}

gen_kwargs = {"max_length": 128, "top_p": 0.8, "temperature": 0.8, "do_sample": True, "repetition_penalty": 1.1}
output = model.generate(**inputs, **gen_kwargs)
# decode the new tokens
output = tokenizer.decode(output[0].tolist(), skip_special_tokens=True)
print(output)
```

#### 模型扩展

Transformer-based Pre-trained models

基础 Transformer架构加上不同的head模块组成，部分例子如下：

基础模型：只输出隐层状态
- *`Model` (retrieve the hidden states)：基础模型，只输出**隐状态**
- *`ForCausalLM`：常规语言模型(自回归)，典型的有GPT系列

扩展模型：增加层，适配下游应用
- *`ForMaskedLM`：**掩码**语言模型，典型的有BERT、RoBERTa、DeBERTa
- *`ForMultipleChoice`：多项选择模型
- *`ForQuestionAnswering`：问答模型，一般是抽取式问答
- *`ForSequenceClassification`：序列分类模型
- *`ForTokenClassification`：token分类模型，如命名实体识别和关系抽取

关系
- ![](https://qiankunli.github.io/public/upload/machine/transformers_pipelines.png)

开源库实现的模型，包括了BERT，GPT2，XLNet，RoBERTa，ALBERT，ELECTRA，T5等家喻户晓的预训练语言模型。


```py
CONFIG_MAPPING = OrderedDict(
    [
        ("retribert", RetriBertConfig,),
        ("t5", T5Config,),
        ("mobilebert", MobileBertConfig,),
        ("distilbert", DistilBertConfig,),
        ("albert", AlbertConfig,),
        ("camembert", CamembertConfig,),
        ("xlm-roberta", XLMRobertaConfig,),
        ("marian", MarianConfig,),
        ("mbart", MBartConfig,),
        ("bart", BartConfig,),
        ("reformer", ReformerConfig,),
        ("longformer", LongformerConfig,),
        ("roberta", RobertaConfig,),
        ("flaubert", FlaubertConfig,),
        ("bert", BertConfig,),
        ("openai-gpt", OpenAIGPTConfig,),
        ("gpt2", GPT2Config,),
        ("transfo-xl", TransfoXLConfig,),
        ("xlnet", XLNetConfig,),
        ("xlm", XLMConfig,),
        ("ctrl", CTRLConfig,),
        ("electra", ElectraConfig,),
        ("encoder-decoder", EncoderDecoderConfig,),
    ]
```

参考
- 【2020-7-5】[Transformers源码阅读和实践](http://xtf615.com/2020/07/05/transformers/)


代码示例

```py
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
sequences = ["I've been waiting for a HuggingFace course my whole life.", "So have I!"]
tokens = tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")
print(tokens)
#{
#    'input_ids': tensor([
#        [  101,  1045,  1005,  2310,  2042,  3403,  2005,  1037, 17662, 12172,2607,  2026,  2878,  2166,  1012,   102],
#        [  101,  2061,  2031,  1045,   999,   102,     0,     0,     0,     0, 0,     0,     0,     0,     0,     0]
#    ]),     
#    'attention_mask': tensor([
#        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#    ])
#}
output = model(**tokens)
print(output)
# SequenceClassifierOutput(
#    loss=None, 
#    logits=tensor([[-1.5607,  1.6123],[-3.6183,  3.9137]], grad_fn=<AddmmBackward0>), 
#    hidden_states=None, 
#    attentions=None
#)
```


### 生态系统

HuggingFace主干库：
- Transformer 模型库
- Tokenizer 分词库：将sequence转变为一个id序列
- Hub 社区
- Datasets 数据集库：下载/预处理
- Evaluate 评估
- Accelerate 加速库（软件）
- Optimum 加速卡（硬件）
- Diffusers 扩散模型
- Timm 
- PEFT
- Chat-UI
- Safetensors
- starcoder
- SetFit

【2023-6-14】HuggingFace Ecosystem 生态系统进展 [b站视频](https://www.bilibili.com/video/BV1qk4y1n7qa)
- ![](https://p3.toutiaoimg.com/large/tos-cn-i-qvj2lq49k0/7205980da6854039a68a8cd0c5404967)

时间线
- 2022-7，BLOOM开源，评测效果不及GPT-3
- 2022-8，Stable Diffusion
- 2022-11，ChatGPT发布
- 2023-2，META FAIR开源LLaMA
- 发布 LLM Leaderboeard
- 开源 HuggingChat，以及 Chat-UI
- 发布 BigCodr，以及 StarCoder，基于github许可代码，可以通过opt-out工具剔除自己的代码
- 2023-5，发布 StarChat，辅助编程


## 数据

数据集工具包 huggingface datasets 


### tokenizer

图解
- ![](https://qiankunli.github.io/public/upload/machine/attention_mask.jpg)

默认情况下，AutoTokenizer 类首先加载 Fast tokenizer
- Fast 适合海量数据
- 少量数据时，两者速度差异不大

Fast tokenizer 和 Slow tokenizer 的区别：
- Slow tokenizer 是在 Transformer 库中用Python编写的。
- Fast tokenizer 是在 Tokenizers 库中用Rust编写的


### load_dataset 函数


```py
datasets.load_dataset(
	path: str,
    name: Optional[str] = None,
    data_dir: Optional[str] = None,
    data_files: Optional[Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]] = None,
    split: Optional[Union[str, Split]] = None,
    cache_dir: Optional[str] = None,
    features: Optional[Features] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[DownloadMode] = None,
    ignore_verifications: bool = False,
    keep_in_memory: Optional[bool] = None,
    save_infos: bool = False,
    revision: Optional[Union[str, Version]] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
    task: Optional[Union[str, TaskTemplate]] = None,
    streaming: bool = False,
    **config_kwargs
    )
```

函数说明
- `load_dataset`函数从Hugging Face Hub或者本地数据集文件中加载一个数据集。可以通过 [datasets](https://huggingface.co/datasets) 或者 `datasets.list_datasets()` 获取所有可用数据集。
- 参数 `path` 表示数据集的名字或者路径。可以是一个数据集的名字，比如"imdb"、“glue”；也可以是通用的产生数据集文件的脚本，比如"json"、“csv”、“parquet”、“text”；或者是在数据集目录中的脚本（.py)文件，比如“glue/glue.py”。
- 参数 `name` 表示数据集中的子数据集，当一个数据集包含多个数据集时，就需要这个参数。比如"glue"数据集下就包含"sst2"、“cola”、"qqp"等多个子数据集，此时就需要指定name来表示加载哪一个子数据集。
- 参数 `data_dir` 表示数据集所在的目录，参数data_files表示本地数据集文件。
- 参数 `split` 如果为None，则返回一个DataDict对象，包含多个DataSet数据集对象；如果给定的话，则返回单个DataSet对象。
- 参数 `cache_dir` 表示缓存数据的目录
  - 默认为"`~/.cache/huggingface/datasets`"。
- 参数 `keep_in_memory` 表示是否将数据集缓存在内存中，加载一次后，再次加载可以提高加载速度。
- 参数 `revision` 表示加载数据集的脚本的版本。


### 远程数据集

```py
import datasets

dataset = datasets.load_dataset("imdb") # imdb 数据集
# 加载glue下的cola子数据集
dataset = datasets.load_dataset("glue", name="cola") 
# csv脚本加载本地的test.tsv文件中的数据集
dataset = datasets.load_dataset("csv", data_dir="./test", data_files="test.tsv")
# 本地glue.py脚本文件加载远程cola数据集
dataset_1 = datasets.load_dataset("../dataset/glue/glue.py", name="cola")
# 与上一个等价
dataset_2 = datasets.load_dataset("../dataset/glue", name="cola") 

```


### 本地数据集

【2024-4-22】错误

```sh
  File "/usr/local/lib/python3.9/dist-packages/datasets/load.py", line 1780, in dataset_module_factory
    raise ConnectionError(f"Couldn't reach '{path}' on the Hub ({type(e).__name__})")
ConnectionError: Couldn't reach 'wikitext' on the Hub (ConnectTimeout)
```

服务器访问不了外网，如何读取本地数据集？
1. 首先，下载并存储数据
2. 然后，把数据集上传到指定服务器地址，并进行本地加载

```py
import datasets

local_path = '.' # 本地缓存目录
all_data = datasets.load_dataset('imdb')
# 子集
dataset = load_dataset("Salesforce/dialogstudio", "TweetSumm") 
# 缓存到本地, 目录名 imdb, 再次执行会报错
# ValueError: Invalid pattern: '**' can only be an entire path component
all_data = datasets.load_dataset('imdb', cache_dir=local_path) 
# 划分训练集、测试集
train_data, test_data = datasets.load_dataset('imdb', split =['train', 'test'], cache_dir=local_path)
# 通过csv脚本加载本地的test.tsv文件中的数据集
dataset = datasets.load_dataset("csv", data_dir="./test", data_files="test.tsv")

# 手工保存到本地
all_data.save_to_disk('my_imdb')
all_data.to_csv('my_imdb')
all_data.to_json('my_imdb')
# 加载本地数据集
new_data = datasets.load_from_disk('my_imdb')
```

【2024-5-8】再次执行报错

```sh
ValueError: Invalid pattern: '**' can only be an entire path component
```

原因
- 本地有数据集同名目录，改名即可


注意：
- 保存数据集所用机器上 datasets版本和使用本地数据集的datasets的**版本要一致**才行，不然可能会出现数据集加载错误的情况。

```py
dataset = load_dataset("json", data_dir='data', data_files="data/train_dataset.json", split="train")
```


### 内存数据集

内存加载数据

支持从内存中加载字典或者 DafaFrame（pandas）数据结构的数据，具体操作示例如下：

```py
# 从字典导入数据 
from datasets import Dataset 

my_dict = {"a": [1, 2, 3]} 
dataset = Dataset.from_dict(my_dict) # 从dataFrame导入数据 

import pandas as pd 
df = pd.DataFrame({"a": [1, 2, 3]}) 
dataset = Dataset.from_pandas(df)
```

### 数据处理


#### 数据查看

加载完数据后, 看看有那些内容
- 整个数据集划分成了多个数据子集，包含train，valid以及test集。
- 每个arrow_dataset都有多少条数据
- 这些数据的feature是什么

| 数据格式 | 函数 |
| --- | --- |
| Arrow | save_to_disk() |
| CSV | to_csv() |
| JSON | to_json() |

简单两行代码导入数据，然后打印出来看一下；

```py
from datasets import load_dataset 

# datasets = load_dataset('cail2018') 
datasets = load_dataset('imdb') 
print(datasets)  # 查看数据的结构
datasets['train'] # type: datasets.arrow_dataset.Dataset
# DatasetDict({
#     train: Dataset({
#         features: ['text', 'label'],
#         num_rows: 25000
#     })
#     test: Dataset({
#         features: ['text', 'label'],
#         num_rows: 25000
#     })
#     unsupervised: Dataset({
#         features: ['text', 'label'],
#         num_rows: 50000
#     })
# })

datasets = load_dataset('cail2018',split='exercise_contest_test') # 如果知道数据结构，在load的时候就可以用split只load进来一部分数据；
# 从数据集里面取数据
datasets_sample = datasets[ "exercise_contest_train" ].shuffle(seed=42).select(range(1000))
# 这里就是从cail2018这个数据集里面的，exercise_contest_train这部分数据，随机抽取1000个数据
# 从这个里面切片取数如下所示，规律和np或者dataframe的数据结构形式是一样的。
print(datasets_sample[10:15] )
```


#### 数据转换

```py
from datasets import load_dataset
datasets = load_dataset('cail2018')
print(datasets)  # 查看数据的结构


def add_prefix(example):
    example["fact"] = "案件详情: " + example["fact"]
    return example
# shuffle 打乱
datasets_sample = datasets[ "exercise_contest_train" ].shuffle(seed= 42 ).select( range ( 1000 ))
# map 映射: 逐元素处理
datasets_sample = datasets_sample.map(add_prefix)
print(datasets_sample[:3] )
# filter 过滤
drug_dataset = drug_dataset.filter(lambda x: x["condition"] is not None)
# sort 排序
datasets_sample = datasets_sample.sort('punish_of_money') # 按照被罚金额排序，是从大到小的，这个排序似乎没法改，看了下参数没找到改成从小到大的。。。。
# set_format 格式转化: [None, 'numpy', 'torch', 'tensorflow', 'pandas', 'arrow'] None 默认
datasets_sample.set_format("pandas") # 转换为pandas的dataFrame结构，这处理起来还不是手拿把掐的


# 生成新列
from datasets import load_dataset , Dataset
dataset = Dataset.from_dict({"a": [0, 1, 2]})
dataset = dataset.map(lambda batch: {"b": batch["a"]*2})  
# 这里给数据dataset产生一个新的列b，请注意处理的时候要注意，新的列长度必须和原来一致；
```


#### 如何加载大数据

加载超大型的语料，占用内存是加载语料的几倍。比如gpt-2训练的40G语料，可能会让内存爆掉。

huggingface设计了两个机制来解决这个问题，第一个是将数据集视为“内存映射”文件，第二个是“流式传输”语料库。
- **内存映射**：通过Apache Arrow内存格式和pyarrow库实现的，huggingface已经自己处理好了，网站上官方测试的情况大概是0.3gb/s。
- **流式传输**：因为很多语料库非常的大（比如pile多达800多G），下载到本地硬盘还是有些吃不消呀，因此huggingface设置了流式传输，类似于视频网站的操作，本地有个缓冲区大小固定，然后不停的迭代新数据。假设缓冲区数据一共10000条，当你处理第一条的时候，他就加载第10001条数据。

示例代码：
- 只需要设置 streaming= True 即可，这个load上来的数据是一个可迭代对象，之后的处理与前面介绍的一样。

```py
pubmed_dataset_streamed = load_dataset( "json" , data_files=data_files, split= "train" , streaming= True )
```


## 模型


### 模型导入 

导入方法 
- 默认自动从远程下载模型
  - 前提：能联网
  - 默认保存路径：`~/.cache/huggingface/hub/`
- 可以本地导入

```py
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
```

【2024-5-8】transformers 中有哪些包可用？
- 见官方源码 [transformers/__init__.py](https://github.com/huggingface/transformers/blob/main/src/transformers/__init__.py)

#### 远程导入


```py
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')
```



#### 本地导入

无法联网时，读取预训练模型会失败

解法
- 下载模型：huggingface 官网 [Files and versions]() 上下载几个文件
  - 模型配置文件
    - `config.json` 
  - pytorch模型文件
    - `pytorch_model.bin` 
  - tokenizer 文件
    - `tokenizer.json` 
    - `tokenizer_config.json`
    - `vocab.txt`
- 本地导入
  - 改成本地目录
  - 额外读取 config 信息

```py
from transformers import BertTokenizer, BertModel

# config 文件
config = BertConfig.from_json_file("bert-base-chinese/config.json")
# tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
# model = BertModel.from_pretrained('bert-base-chinese')
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese/') ##注意此处为本地文件夹
model = BertModel.from_pretrained("bert-base-chinese/pytorch_model.bin", config=config)
```


### 模型下载

- 在[huggingface模型库](https://huggingface.co/models)里选择需要的预训练模型并下载。
  - 例如，点击 `bert-base-uncased` 以后点 `Files and versions` 手动下载。
  - 只要点击对应文件的下载（↓）, 然而要通过from_pretrained方法加载，还需要把模型文件名改成pytorch_model.bin
- 这样下载的模型**有损**，后续无法使用，因此最好是通过git下载

这种方法麻烦
- Git lfs 方案要简洁得多 -- <span style='color:red'>优雅但不灵活</span>
  - 问题：会下载仓库**所有**文件，大大延长模型下载时间
- HuggingFace Hub: <span style='color:green'>精准下载</span>

参考
- 官方提供的下载[方法](https://huggingface.co/docs/hub/models-downloading)
- [【Hugging Face】如何从hub中下载文件](https://automanbro.blog.csdn.net/article/details/133658587)
- [如何优雅的下载huggingface-transformers模型](https://zhuanlan.zhihu.com/p/475260268)

#### (0) 自动下载

模型文件导入
- 默认保存路径：`~/.cache/huggingface/hub/`

```py
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# ---- 示例 -----
import transformers

MODEL_PATH = "./transformr_files/bert-base-uncased/"
# a.通过词典导入分词器
tokenizer = transformers.BertTokenizer.from_pretrained(f"{MODEL_PATH}/bert-base-uncased-vocab.txt") 
# b. 导入配置文件
model_config = transformers.BertConfig.from_pretrained(MODEL_PATH)
# 【2023-2-22】默认保存路径：~/.cache/huggingface/hub/
tokenizer = BertTokenizer.from_pretrained(model_name, cache_dir='./transformers/')	# cache_dir表示将预训练文件下载到本地指定文件夹下，而不是默认路径

# 修改配置
model_config.output_hidden_states = True
model_config.output_attentions = True
# 通过配置和路径导入模型
model = transformers.BertModel.from_pretrained(MODEL_PATH,config = model_config)
```

#### (1) HuggingFace Hub 精准下载

通过 huggingface hub 下载模型时，模型文件是**blob编码**
- 因为 huggingface_hub 默认下载以系统**全局缓存**形式保存。
- 只需要通过修改 `snapshot_download(local_dir_use_symlinks=False)` 即可以得到正常的文件形式

hf_hub_download

```py
#! pip install huggingface_hub

from huggingface_hub import hf_hub_download
import joblib

REPO_ID = "YOUR_REPO_ID"
FILENAME = "sklearn_model.joblib"

model = joblib.load(
    hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
)

from huggingface_hub import hf_hub_download
# 下载单个文件
hf_hub_download(repo_id="lysandre/arxiv-nlp", filename="config.json")
hf_hub_download(repo_id="google/fleurs", filename="fleurs.py", repo_type="dataset")
# 下载特定版本
hf_hub_download(repo_id="lysandre/arxiv-nlp", filename="config.json", revision="v1.0")
hf_hub_download(repo_id="lysandre/arxiv-nlp", filename="config.json", revision="test-branch")
hf_hub_download(repo_id="lysandre/arxiv-nlp", filename="config.json", revision="refs/pr/3")
hf_hub_download(repo_id="lysandre/arxiv-nlp", filename="config.json", revision="877b84a8f93f2d619faa2a6e514a32beef88ab0a")
```

snapshot_download
- `snaphot_download` 方法提供了`allow_regex`和`ignore_regex`两个参数，前者是对指定的匹配项进行下载，后者是忽略指定的匹配项，下载其余部分。

```py
# 下载整个代码库
from huggingface_hub import snapshot_download
#    snapshot_download() 默认下载最新的修订版本
snapshot_download(repo_id="lysandre/arxiv-nlp")
snapshot_download(repo_id="google/fleurs", repo_type="dataset")
snapshot_download(repo_id="lysandre/arxiv-nlp", revision="refs/pr/1") # 特定版本
snapshot_download(repo_id="lysandre/arxiv-nlp", allow_patterns="*.json") # 指定要下载的文件类型
snapshot_download(repo_id="lysandre/arxiv-nlp", ignore_patterns=["*.msgpack", "*.h5"]) # 忽略哪些文件
# 实例： 过滤某些文件
snapshot_download(repo_id="bert-base-chinese")
snapshot_download(repo_id="bert-base-chinese", ignore_regex=["*.h5", "*.ot", "*.msgpack"])
```

使用 [huggingface_hub](https://github.com/huggingface/huggingface_hub) 工具创建、删除、更新和索引模型库


```py
# python -m pip install huggingface_hub
from huggingface_hub import hf_hub_download
import joblib

REPO_ID = "YOUR_REPO_ID" # 同 model_name
FILENAME = "sklearn_model.joblib"

hf_hub_download(repo_id="bigscience/T0_3B", filename="config.json", cache_dir="./your/path/bigscience_t0")
# 或
model = joblib.load(
    hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
)
# 使用
from transformers import AutoConfig
config = AutoConfig.from_pretrained("./your/path/bigscience_t0/config.json")
```

#### (2) huggingface-cli 单文件下载

huggingface-cli 命令直接从Hub下载文件。
- 内部使用 `hf_hub_download()` 和 `snapshot_download()` 助手，并将返回路径打印到终端
- 文件将被下载到由`HF_HOME`环境变量定义的缓存目录中（如果未指定，则为`~/.cache/huggingface/hub`）


```sh
# 查看可用参数
huggingface-cli download --help
# 下载单个文件
huggingface-cli download gpt2 config.json
#~/.cache/huggingface/hub/models--gpt2/snapshots/11c5a3d5811f50298f278a704980280950aedb10/config.json
huggingface-cli download google/gemma-7b-it-pytorch
# [2024-5-6] merlin 上执行失，败403, mac 本地成功
huggingface-cli download google/bigbird-roberta-large --local-dir=. --quiet
# 指定身份
huggingface-cli download gpt2 config.json --token=hf_****
#/home/wauplin/.cache/huggingface/hub/models--gpt2/snapshots/11c5a3d5811f50298f278a704980280950aedb10/config.json
# 同事下载多个文件，并进度条显示
huggingface-cli download gpt2 config.json model.safetensors
# 进度条静音
huggingface-cli download gpt2 config.json model.safetensors --quiet
# 指定目录
huggingface-cli download gpt2 config.json --cache-dir=./cache
# 下载到本地文件夹，而不带缓存目录结构，则可用 --local-dir 
huggingface-cli download gpt2 config.json --local-dir=./models/gpt2
# 指定不同类型的仓库或版本来下载，并使用glob模式包含/排除要下载的文件
huggingface-cli download bigcode/the-stack --repo-type=dataset --revision=v1.2 --include="data/python/*" --exclude="*.json" --exclude="*.zip"
```


#### (3) git lfs 优雅但不灵活

```shell
# mac下
brew install git-lfs
apt get install git-lfs # ubuntu
git lfs install
git clone https://huggingface.co/bert-base-chinese
# 或
git lfs clone https://huggingface.co/stabilityai/sd-vae-ft-mse
# git clone https://huggingface.co/lmsys/vicuna-13b-delta-v0
# git clone git@hf.co:bigscience/bloom
# git clone https://huggingface.co/LinkSoul/Chinese-Llama-2-7b
GIT_LFS_SKIP_SMUDGE=1 # 只下载 pointer 文件，不下大文件
# 在当前目录新建一个 models 文件夹用来存放大模型
# 只下载特定文件
git lfs clone --include="*.bin" [HF_REPO]
```

#### (4) hf_transfer 

hf_transfer是一个基于Rust开发的库，用于加速与Hub的文件传输
- 安装该包 `pip install hf_transfer`
- 并将`HF_HUB_ENABLE_HF_TRANSFER=1`设置为环境变量



#### 模型不同点

[关于transformers库中不同模型的Tokenizer](https://zhuanlan.zhihu.com/p/121787628)

不同PLM原始论文和transformers库中数据的组织格式。其实，像Roberta，XLM等模型的中< s>, < /s>是可以等价于Bert中的[CLS], [SEP]的，只不过不同作者的习惯不同。

```shell
# Bert
单句：[CLS] A [SEP]
句对：[CLS] A [SEP] A [SEP]
# Roberta
单句：<s> A </s>
句对：<s> A </s> </s> B </s>
# Albert
单句：[CLS] A [SEP]
句对：[CLS] A [SEP] B [SEP]
# XLNet
单句：[A] <sep> <cls>
句对：A <sep> B <sep> <cls>
# XLM
单句：<s> A </s>
句对：<s> A </s> B </s>
# XLM-Roberta
单句：<s> A </s>
句对：<s> A </s> </s> B </s>
# Bart
单句：<s> A </s>
句对：<s> A </s> </s> B </s>
```

transformers库中RobertaTokenizer和BertTokenizer的不同
- transformers库中`RobertaTokenizer`需要**同时读取vocab_file和merges_file两个文件**，不同于`BertTokenizer`只需要读取vocab_file一个词文件。主要原因是两种模型采用的编码不同：
- Bert采用的是**字符**级别的BPE编码，直接生成词表文件，官方词表中包含**3w**左右的单词，每个单词在词表中的位置即对应Embedding中的索引，Bert预留了100个\[unused]位置，便于使用者将自己数据中重要的token手动添加到词表中。
- Roberta采用的是**byte**级别的BPE编码，官方词表包含**5w**多的byte级别的token。merges.txt中存储了所有的token，而vocab.json则是一个byte到索引的映射，通常频率越高的byte索引越小。所以转换的过程是，先将输入的所有tokens转化为merges.txt中对应的byte，再通过vocab.json中的字典进行byte到索引的转化。

由于中文的特殊性不太适合采用byte级别的编码，所以大部分开源的中文Roberta预训练模型仍然采用的是**单字词表**，所以直接使用BertTokenizer读取即可， 不需要使用RobertaTokenizer。

### 模型保存


```python
tokenizer.save_pretrained(save_directory) # 保存词表
model.save_pretrained(save_directory) # 保存模型
```

#### Safetensors

Safetensors 是一种用于在移动设备上运行模型的文件格式。 安全性、快速加载和兼容性等优点。 
- 将模型转换为Safetensors文件格式，可在移动设备上高效地加载和运行模型，同时保护模型的实现和逻辑


Hugging Face 开发 Safetensors的新序列化格式
- 简化和精简大型复杂张量的存储和加载。

张量是深度学习中使用的主要数据结构，其大小会给效率带来挑战。
- Safetensors结合使用高效的序列化和压缩算法来减少大型张量的大小，使其比pickle等其他序列化格式更快、更高效。
- 与传统PyTorch序列化格式 `pytorch_model.bin` 和 `model.safetensors` 相比，Safetensors在CPU上的速度快**76.6倍**，在GPU上的速度快**2倍**。

Safetensors API 适用于: Pytorch、Tensorflow、PaddlePaddle、Flax和Numpy

安装

```sh
pip install safetensors
```

创建模型

```py
from torch import nn

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.a = nn.Linear(100, 100)
        self.b = self.a

    def forward(self, x):
        return self.b(self.a(x))


model = Model()
print(model.state_dict())
```

模型导入导出

```py
from safetensors.torch import load_model, save_model

save_model(model, "model.safetensors")

load_model(model, "model.safetensors")
print(model.state_dict())
# OrderedDict([('a.weight', tensor([[-0.0913, 0.0470, -0.0209, ..., -0.0540, -0.0575, -0.0679], [ 0.0268, 0.0765, 0.0952, ..., -0.0616, 0.0146, -0.0343], [ 0.0216, 0.0444, -0.0347, ..., -0.0546, 0.0036, -0.0454], ...,

```

张量导入、导出

```py
import torch
from safetensors.torch import save_file, load_file

tensors = {
   "weight1": torch.zeros((1024, 1024)),
   "weight2": torch.zeros((1024, 1024))
}
save_file(tensors, "new_model.safetensors")
load_file("new_model.safetensors")
```


### GPU

【2023-2-22】[Efficient Training on Multiple GPUs](https://huggingface.co/docs/transformers/perf_train_gpu_many)

The following is the brief description of the main concepts that will be described later in depth in this document.
- DataParallel (`DP`) - the same setup is replicated multiple times, and each being fed a slice of the data. The processing is done in parallel and all setups are synchronized at the end of each training step.
- TensorParallel (`TP`) - each tensor is split up into multiple chunks, so instead of having the whole tensor reside on a single gpu, each shard of the tensor resides on its designated gpu. During processing each shard gets processed separately and in parallel on different GPUs and the results are synced at the end of the step. This is what one may call horizontal parallelism, as the splitting happens on horizontal level.
- PipelineParallel (`PP`) - the model is split up vertically (layer-level) across multiple GPUs, so that only one or several layers of the model are places on a single gpu. Each gpu processes in parallel different stages of the pipeline and working on a small chunk of the batch.
- Zero Redundancy Optimizer (`ZeRO`) - Also performs sharding of the tensors somewhat similar to TP, except the whole tensor gets reconstructed in time for a forward or backward computation, therefore the model doesn’t need to be modified. It also supports various offloading techniques to compensate for limited GPU memory.
- Sharded `DDP` - is another name for the foundational ZeRO concept as used by various other implementations of ZeRO.

Before diving deeper into the specifics of each concept we first have a look at the rough decision process when training large models on a large infrastructure.


### 推理加速

【2022-1-21】[让 Transformer 的推理速度提高 4.5 倍，这个小 trick 还能给你省十几万](https://mp.weixin.qq.com/s/fYxFwBvfQFPTqMZL6UI5WQ)
- NLP明星公司Hugging Face发布了一个叫做Infinity的产品，可以以1ms延时完成Transformer的推理，性能相当高了。但有点贵——1年至少要十几万块 （2万美元）
- 有没有别的办法？Transformer-deploy：开源的、“不费吹灰之力”就可以达到Infinity一些公共基准的那种。并且现在，通过在该方法上施加一个小trick（GPU量化（quantization）），将Transformer的推理速度提高4.5倍！
  - 用一行命令优化和部署Hugging Face上的Transformer模型，并支持大多数基于Transformer编码器的模型，比如Bert、Roberta、miniLM、Camembert、Albert、XLM-R、Distilbert等。
  - Transformer-deploy推理服务器用的是Nvidia Triton。推理引擎为Microsoft ONNX Runtime（用于CPU和GPU推理）和Nvidia TensorRT（仅限 GPU）。如果想在GPU上获得一流的性能，Nvidia Triton+Nvidia TensorRT这样的组合无疑是最佳选择。虽然TensorRT用起来有点难，但它确实能比用Pytorch快5～10倍。
  - 在实际性能测试中，Transformer-deploy在batch size为1、token分别为16和128的输入序列中的推理速度，都比付费的Hugging Face Infinity要快：Transformer-deploy在token为16时要1.52ms，Infinity则需要1.7ms；token为128时需要1.99ms，Infinity则需要2.5ms。

### pipeline

pipeline API可以快速体验 Transformers。它将模型的预处理、后处理等步骤包装起来，直接定义好任务名称后输出文本，得到结果。这是一个高级的API，可以领略到transformers 这个库的强大且友好。

用 [pipeline API](https://huggingface.co/docs/transformers/v4.26.1/en/main_classes/pipelines#pipelines)，输入任务名称，默认会选择特定已经存好的模型文件，然后会进行下载并且缓存。

#### pipeline 流程

接收文本后，通常有三步：**preprocess** （Tokenizer） -> **fit model**（训练模型） -> **postprocessing** 
- （1）输入文本被预处理成机器可以理解的格式
  - 将输入的文本进行分词（Tokenizer）
    - 变成：words，subwords，或者symbols，这些统称为token
  - 将每个token映射为一个integer
  - 为输入添加模型需要的特殊字符。
- （2）被处理后的输入被传入模型中
- （3）模型的预测结果经过后处理，得到人类可以理解的结果

![](https://pic2.zhimg.com/v2-d9b23d02a7e5e1988ba8f902d7da9c0d_r.jpg)

注意：
- 所有的预处理阶段（Preprocessing），都要**与模型预训练阶段保持一致**，所以要从Model Hub 中下载预处理的信息。
- 用 AutoTokenizer 的 from_pretrained 方法进行tokenizer 的加载，通过把tokenizer 的checkpoint 导入，它可以自动获取tokenizer需要的数据并进行缓存（下次无需下载）。

```py
from transformers import AutoTokenizer
from transformers import AutoModel

checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(checkpoint) # 加载分词器
model = AutoModel.from_pretrained(checkpoint) # 加载模型

raw_inputs = [
    "I've been waiting for a HuggingFace course my whole life.",
    "I hate this so much!",
]
# ----- 文本id化 -----
# 指定返回的张量类型（PyTorch、TensorFlow 或普通 NumPy），用 return_tensors 参数
inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
print(inputs) # 返回一个包含两个键的字典，input_ids和attention_mask
# ----- 模型 ------
outputs = model(**inputs)
print(outputs.last_hidden_state.shape)
# 输出 torch.Size([2, 16, 768])

```

返回

```
{
    'input_ids': tensor([
        [  101,  1045,  1005,  2310,  2042,  3403,  2005,  1037, 17662, 12172, 2607,  2026,  2878,  2166,  1012,   102],
        [  101,  1045,  5223,  2023,  2061,  2172,   999,   102,     0,     0,     0,     0,     0,     0,     0,     0]
    ]), 
    'attention_mask': tensor([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
}
```

![](https://pic3.zhimg.com/80/v2-f51f9dae359ec191229b35028d0897ca_1440w.webp)

Transformers 中有许多不同的架构可用，每一种架构都围绕着处理特定任务而设计，清单：
* Model (retrieve the hidden states)
* ForCausalLM
* ForMaskedLM
* ForMultipleChoice
* ForQuestionAnswering
* ForSequenceClassification
* ForTokenClassification
* and others

3）Post-Processing
- 模型最后一层输出的原始非标准化分数。要转换为概率，它们需要经过一个SoftMax层（所有 Transformers 模型都输出 logits，因为用于训练的损耗函数一般会将最后的激活函数(如SoftMax)与实际损耗函数(如交叉熵)融合 

```py
import torch

predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
print(predictions)
```



#### pipeline 任务

目前支持的pipeline 如下：
- feature-extraction (get the vector representation of a text) 特征抽取
- fill-mask 掩码回复
- ner (named entity recognition) 命名实体识别
- question-answering 问答
- sentiment-analysis 情感分析
- summarization 文本摘要
- text-generation 文本生成
- translation 机器翻译
- zero-shot-classification 零样本分类

最新pipeline类型：详见[官网介绍](https://huggingface.co/transformers/main_classes/pipelines.html)
- AudioClassificationPipeline
- AutomaticSpeechRecognitionPipeline
- ConversationalPipeline
- FeatureExtractionPipeline
- FillMaskPipeline
- ImageClassificationPipeline
- ObjectDetectionPipeline
- QuestionAnsweringPipeline
- SummarizationPipeline
- TableQuestionAnsweringPipeline
- TextClassificationPipeline
- TextGenerationPipeline
- Text2TextGenerationPipeline
- TokenClassificationPipeline
- TranslationPipeline
- ZeroShotClassificationPipeline

所有的API都可以通过 搜索，并且在线测试

#### 任务模型

主要的模型：
- 自回归：GPT2、Transformer-XL、XLNet
- 自编码：BERT、ALBERT、RoBERTa、ELECTRA
- Seq2Seq：BART、Pegasus、T5

各种任务的代表模型

| Model	 | Examples	| Tasks |
|---|---|---|
| Encoder 编码器模型 | ALBERT, BERT, DistilBERT, ELECTRA, RoBERTa	| Sentence classification, named entity recognition, extractive question answering <br>适合需要理解完整句子的任务，例如句子分类、命名实体识别（以及更一般的单词分类）和提取式问答 |
| Decoder 解码器模型 | CTRL, GPT, GPT-2, Transformer XL	| Text generation <br>解码器模型的预训练通常围绕预测句子中的下一个单词。这些模型最适合涉及文本生成的任务 |
| Encoder-decoder 序列到序列模型 | BART, T5, Marian, mBART | Summarization, translation, generative question answering <br>序列到序列模型最适合围绕根据给定输入生成新句子的任务，例如摘要、翻译或生成式问答。|

#### Text classification

默认checkpoint 是 distilbert-base-uncased-finetuned-sst-2-english

```python
from transformers import pipeline

#checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
#tokenizer = AutoTokenizer.from_pretrained(checkpoint)
classifier = pipeline("sentiment-analysis")
# 指定模型，硬件环境
pipe = pipeline("sentiment-analysis", model=model_name, device=0)
# 单句
classifier("I've been waiting for a HuggingFace course my whole life.")
# 多句
classifier([
    "I've been waiting for a HuggingFace course my whole life.", 
    "I hate this so much!"
])
```


```python
## ------------ PYTORCH CODE ------------ 
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "bert-base-cased-finetuned-mrpc"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

classes = ["not paraphrase", "is paraphrase"]

sequence_0 = "The company HuggingFace is based in New York City"
sequence_1 = "Apples are especially bad for your health"
sequence_2 = "HuggingFace's headquarters are situated in Manhattan"

# The tokenizer will automatically add any model specific separators (i.e. <CLS> and <SEP>) and tokens to
# the sequence, as well as compute the attention masks.
paraphrase = tokenizer(sequence_0, sequence_2, return_tensors="pt")
not_paraphrase = tokenizer(sequence_0, sequence_1, return_tensors="pt")

paraphrase_classification_logits = model(**paraphrase).logits
not_paraphrase_classification_logits = model(**not_paraphrase).logits

paraphrase_results = torch.softmax(paraphrase_classification_logits, dim=1).tolist()[0]
not_paraphrase_results = torch.softmax(not_paraphrase_classification_logits, dim=1).tolist()[0]

# Should be paraphrase
for i in range(len(classes)):
    print(f"{classes[i]}: {int(round(paraphrase_results[i] * 100))}%")

# Should not be paraphrase
for i in range(len(classes)):
    print(f"{classes[i]}: {int(round(not_paraphrase_results[i] * 100))}%")

## ------------ TENSORFLOW CODE ------------ 
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import tensorflow as tf

model_name = "bert-base-cased-finetuned-mrpc"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

classes = ["not paraphrase", "is paraphrase"]

sequence_0 = "The company HuggingFace is based in New York City"
sequence_1 = "Apples are especially bad for your health"
sequence_2 = "HuggingFace's headquarters are situated in Manhattan"

# The tokenizer will automatically add any model specific separators (i.e. <CLS> and <SEP>) and tokens to
# the sequence, as well as compute the attention masks.
paraphrase = tokenizer(sequence_0, sequence_2, return_tensors="tf")
not_paraphrase = tokenizer(sequence_0, sequence_1, return_tensors="tf")

paraphrase_classification_logits = model(paraphrase).logits
not_paraphrase_classification_logits = model(not_paraphrase).logits

paraphrase_results = tf.nn.softmax(paraphrase_classification_logits, axis=1).numpy()[0]
not_paraphrase_results = tf.nn.softmax(not_paraphrase_classification_logits, axis=1).numpy()[0]

# Should be paraphrase
for i in range(len(classes)):
    print(f"{classes[i]}: {int(round(paraphrase_results[i] * 100))}%")

# Should not be paraphrase
for i in range(len(classes)):
    print(f"{classes[i]}: {int(round(not_paraphrase_results[i] * 100))}%")
```


#### Zero-shot classification

文本分类标注往往非常耗时，huggingface 提供了0样本分类的pipeline， 用户只需要传入文本内容，以及可能的分类标签，就可以得到每个标签的概率，这样子可以提供标注人员参考结果，大大提高标注效率。

```python
from transformers import pipeline

classifier = pipeline("zero-shot-classification")
classifier(
    "This is a course about the Transformers library",
    candidate_labels=["education", "politics", "business"],
)
{'sequence': 'This is a course about the Transformers library',
 'labels': ['education', 'business', 'politics'],
 'scores': [0.8445963859558105, 0.111976258456707, 0.043427448719739914]}
```

#### Text generation

[官方 generate 方法解释](https://huggingface.co/docs/transformers/main_classes/text_generation)

文本生成任务，是指你输入开头的话术（prompt），然后让机器自动帮你生成完剩下的句子。Text generation 中包含了一些随机因子，因此每次生成的结果都可能不同。

```python
from transformers import pipeline

generator = pipeline("text-generation")
generator("In this course, we will teach you how to")
[{'generated_text': 'In this course, we will teach you how to understand and use '
                    'data flow and data interchange when handling user data. We '
                    'will be working with one or more of the most commonly used '
                    'data flows — data flows of various types, as seen by the '
                    'HTTP'}]
```

你可以设置参数 num_return_sequences 选择返回的结果个数，也可以通过 max_length 限制每次返回的结果句子的长度.

并且模型选择可以通过 model 设置，这边选择 distilgpt2

```python
from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")
generator(
    "In this course, we will teach you how to",
    max_length=30,
    num_return_sequences=2,
)
[{'generated_text': 'In this course, we will teach you how to manipulate the world and '
                    'move your mental and physical capabilities to your advantage.'},
 {'generated_text': 'In this course, we will teach you how to become an expert and '
                    'practice realtime, and with a hands on experience on both real '
                    'time and real'}]
```

#### Mask filling

掩码恢复是将一个句子中随机遮掩<mask>的词给恢复回来，top_k 控制了概率最大的 top k 个词被返回。

例如：

```python
from transformers import pipeline

unmasker = pipeline("fill-mask")
unmasker("This course will teach you all about <mask> models.", top_k=2)
[{'sequence': 'This course will teach you all about mathematical models.',
  'score': 0.19619831442832947,
  'token': 30412,
  'token_str': ' mathematical'},
 {'sequence': 'This course will teach you all about computational models.',
  'score': 0.04052725434303284,
  'token': 38163,
  'token_str': ' computational'}]
```

#### Named entity recognition

命名实体是被是指如何将文本中的实体，例如：persons, locations, or organizations，识别出来的任务：

```python
from transformers import pipeline

ner = pipeline("ner", grouped_entities=True)
ner("My name is Sylvain and I work at Hugging Face in Brooklyn.")
[{'entity_group': 'PER', 'score': 0.99816, 'word': 'Sylvain', 'start': 11, 'end': 18}, 
 {'entity_group': 'ORG', 'score': 0.97960, 'word': 'Hugging Face', 'start': 33, 'end': 45}, 
 {'entity_group': 'LOC', 'score': 0.99321, 'word': 'Brooklyn', 'start': 49, 'end': 57}
]
```

注意这边设置了 grouped_entities=True，这就告诉模型，将同一个entity的部分，聚合起来，例如这边的 “Hugging” and “Face” 是一个实体organization，所以就把它给聚合起来。

在数据预处理的部分， Sylvain 被拆解为4 pieces: S, ##yl, ##va, and ##in. 这边后处理也会将这些给聚合起来。

#### Question answering

阅读理解的问题，是通过文本内容，以及提出的问题，得到答案：

```python
from transformers import pipeline

question_answerer = pipeline("question-answering")
question_answerer(
    question="Where do I work?",
    context="My name is Sylvain and I work at Hugging Face in Brooklyn"
)
{'score': 0.6385916471481323, 'start': 33, 'end': 45, 'answer': 'Hugging Face'}
```

#### Summarization

摘要问题，是将长文本的进行句子的压缩，得到简练的句子表达。

```python
from transformers import pipeline

summarizer = pipeline("summarization")
summarizer("""
    America has changed dramatically during recent years. Not only has the number of 
    graduates in traditional engineering disciplines such as mechanical, civil, 
    electrical, chemical, and aeronautical engineering declined, but in most of 
    the premier American universities engineering curricula now concentrate on 
    and encourage largely the study of engineering science. As a result, there 
    are declining offerings in engineering subjects dealing with infrastructure, 
    the environment, and related issues, and greater concentration on high 
    technology subjects, largely supporting increasingly complex scientific 
    developments. While the latter is important, it should not be at the expense 
    of more traditional engineering.

    Rapidly developing economies such as China and India, as well as other 
    industrial countries in Europe and Asia, continue to encourage and advance 
    the teaching of engineering. Both China and India, respectively, graduate 
    six and eight times as many traditional engineers as does the United States. 
    Other industrial countries at minimum maintain their output, while America 
    suffers an increasingly serious decline in the number of engineering graduates 
    and a lack of well-educated engineers.
""")
[{'summary_text': ' America has changed dramatically during recent years . The '
                  'number of engineering graduates in the U.S. has declined in '
                  'traditional engineering disciplines such as mechanical, civil '
                  ', electrical, chemical, and aeronautical engineering . Rapidly '
                  'developing economies such as China and India, as well as other '
                  'industrial countries in Europe and Asia, continue to encourage '
                  'and advance engineering .'}]
```

跟text generation 任务一样，我们也可以设置参数： max_length or a min_length ，限制文本的长度。

#### Translation

文本翻译，你可以在 Model Hub 中，找到特定的翻译模型，例如法翻英的模型， Helsinki-NLP/opus-mt-fr-en：

```python
from transformers import pipeline

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
translator("Ce cours est produit par Hugging Face.")
[{'translation_text': 'This course is produced by Hugging Face.'}]
```

### generate

文本生成方法 generate 

Each framework has a generate method for text generation implemented in their respective GenerationMixin class:
- PyTorch `generate`() is implemented in `GenerationMixin`.
- TensorFlow `generate`() is implemented in `TFGenerationMixin`.
- Flax/JAX `generate`() is implemented in `FlaxGenerationMixin`.

Regardless of your framework of choice, you can parameterize the generate method with a GenerationConfig class instance. Please refer to this class for the complete list of generation parameters, which control the behavior of the generation method.

<div class="mermaid">
    flowchart LR
    %% 节点颜色
    classDef red fill:#f02;
    classDef green fill:#5CF77B;
    classDef blue fill:#6BE0F7;
    classDef orange fill:#F7CF6B;
    classDef grass fill:#C8D64B;
    %%节点关系定义
    A(GenerationMixin):::green -.->|PyTorch|M(generate方法):::orange
    B(TFGenerationMixin):::green -.->|TensorFlow|M
    C(FlaxGenerationMixin):::green -.->|Flax/JAX|M
    G(GernarationConfig):::blue -.->|read|M
    M-->O(自定义生成代码):::grass
</div>

#### 输入格式

Special tokens that can be used at generation time
- `pad_token_id` (int, optional) — 填充字符 The id of the padding token. 
- `bos_token_id` (int, optional) — 开始字符 The id of the beginning-of-sequence token.
- `eos_token_id` (Union[int, List[int]], optional) — 结束字符 The id of the end-of-sequence token. Optionally, use a list to set multiple end-of-sequence tokens.

Generation parameters exclusive to encoder-decoder models 编码-解码模型独有参数
- `encoder_no_repeat_ngram_size` (int, optional, defaults to 0) — If set to int > 0, all ngrams of that size that occur in the encoder_input_ids cannot occur in the `decoder_input_ids`.
- `decoder_start_token_id` (int, optional) — If an encoder-decoder model starts decoding with a different token than bos, the id of that token.

#### 输出参数

Parameters that define the output variables of `generate`
- `num_return_sequences`(int, optional, defaults to 1) — The number of independently computed returned sequences for each element in the batch. 返回句子数目
- `output_attentions` (bool, optional, defaults to False) — Whether or not to return the attentions tensors of all attention layers. See attentions under returned tensors for more details. 所有层的注意力值
- `output_hidden_states` (bool, optional, defaults to False) — Whether or not to return the hidden states of all layers. See hidden_states under returned tensors for more details. 所有曾的隐层状态
- `output_scores` (bool, optional, defaults to False) — Whether or not to return the prediction scores. See scores under returned tensors for more details. 预测分值
- `return_dict_in_generate` (bool, optional, defaults to False) — Whether or not to return a [ModelOutput](https://huggingface.co/docs/transformers/v4.26.1/en/main_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.


#### 解码策略

generate 解码参数
- `do_sample`: 是否采样, 默认 False(对应贪心解码)
- `num_beams`: 束宽，int, 默认 1（不用beam search）,集束搜索参数, 
- `num_beam_groups`: int, 默认 1, 一组束宽，通过不同beam取值获取更好的多样性
- `penalty_alpha`: float, 惩罚因子，用于contrastive search decoding，平衡模型置信度与退化惩罚
- `use_cache`: 默认True, 是否使用上一个K/V注意力，用于解码提速

方法使用: can be used for text-decoder, text-to-text, speech-to-text, and vision-to-text models.
- `greedy decoding` 贪心解码: [greedy search](https://huggingface.co/docs/transformers/v4.26.1/en/main_classes/text_generation#transformers.GenerationMixin.greedy_search), 触发条件: `num_beams=1` and `do_sample=False`
- `contrastive search` 对比搜索: [contrastive_search](https://huggingface.co/docs/transformers/v4.26.1/en/main_classes/text_generation#transformers.GenerationMixin.contrastive_search), 触发条件: `penalty_alpha>0`` and `top_k>1`
- `multinomial sampling` 多项式采样: [sample](https://huggingface.co/docs/transformers/v4.26.1/en/main_classes/text_generation#transformers.GenerationMixin.sample), 触发条件: `num_beams=1` and `do_sample=True`
- `beam-search decoding` 集束解码: [beam search](https://huggingface.co/docs/transformers/v4.26.1/en/main_classes/text_generation#transformers.GenerationMixin.beam_search), 触发条件: `num_beams>1` and `do_sample=False`
- `beam-search multinomial sampling` 集束多项式采样: [beam sample](https://huggingface.co/docs/transformers/v4.26.1/en/main_classes/text_generation#transformers.GenerationMixin.beam_sample), 触发条件: `num_beams>1` and `do_sample=True`
- `diverse beam-search decoding` DBS解码: `DBS` [group_beam_search](https://huggingface.co/docs/transformers/v4.26.1/en/main_classes/text_generation#transformers.GenerationMixin.group_beam_search), 触发条件: `num_beams>1` and `num_beam_groups>1`
  - DBS论文实现，将束宽均分成几组，小组内执行常规bs, 解码时考虑与前面序列的差异性，效果比diverseRL好，[详见](https://wqw547243068.github.io/text-generation?#2018-diverse-beam-search-dbs)
- `constrained beam-search decoding` 对比集束解码: [constrained_beam_search](https://huggingface.co/docs/transformers/v4.26.1/en/main_classes/text_generation#transformers.GenerationMixin.constrained_beam_search), 触发条件: `constraints!=None` or `force_words_ids!=None`

理论上，解码策略有几种
- `贪心搜索`：greedy search
- `集束搜索`：beam search
- `全局搜索`：又称暴力搜索, brute search
- ![](https://pica.zhimg.com/80/v2-ef3522dfec91840dcad6642981722b18_1440w.webp?source=1940ef5c)

结合采样方法，可以衍生出多种解码策略
- generation.GenerationMixin

|generate类型|解码策略|参数`do_sample`|参数`num_beams`|其它参数| 触发条件 |
|---|---|----|----|----|--------|
| `greedy decoding` | greedy_search `贪心解码` | False | 1 | - | `num_beams=1` and `do_sample=False` |
| `contrastive search` | contrastive_search | - | - | - | `penalty_alpha>0` and `top_k>1` |
| `multinomial sampling` | sample `多样式采样` | true | 1 | - |`num_beams=1` and `do_sample=True` |
| `beam-search decoding` | beam_search `集束解码` | False | >1 | - | `num_beams>1` and `do_sample=False` |
| `beam-search multinomial sampling` | beam_sample `集束解码`+`多样式采样` | True | >1 | - | `num_beams>1` and `do_sample=True` |
| `diverse beam-search decoding` | group_beam_search `多样性集束解码` | - | >1 | - | `num_beams>1` and `num_beam_groups>1` |
| `constrained beam-search decoding` | constrained_beam_search `受限集束解码` | 受限beam search | - | - |`constraints!=None` or `force_words_ids!=None` |

参数：
- [text_generation](https://huggingface.co/docs/transformers/main_classes/text_generation)函数说明
- generation[源码](https://github.com/huggingface/transformers/tree/v4.26.1/src/transformers/generation)

#### 哪种解码方法最好？

没有一个普遍 "最佳"的解码方法。哪种方法最好取决于生成任务的性质。
- 如果想执行**精确**的任务，如进行算术运算或提供一个特定问题的答案，那么**降低温度**或使用**确定性**方法，如`贪婪搜索`与`束搜索`相结合，以保证得到最可能的答案。
- 如果想生成**更长**的文本，甚至有点**创造性**，那么改用**抽样方法**，并**提高温度**，或者使用top-k和核抽样的混合方法。

作者：[致Great](https://www.zhihu.com/question/415657741/answer/2430106609)


### Demo发布（space）

【2022-10-8】[Spaces](https://huggingface.co/spaces) ：Discover amazing ML apps made by the community! 展示各种DEMO
- [Hugging Face Spaces](https://huggingface.co/spaces) will host the interface on its servers and provide you with a link you can share.
- 更多用法，参考另一篇日志：[Python下的模型快速部署](https://wqw547243068.github.io/python?#%E6%A8%A1%E5%9E%8B%E5%BF%AB%E9%80%9F%E9%83%A8%E7%BD%B2)


## transformers BERT 源码

参考：
- [BERT源码详解（一）——HuggingFace Transformers最新版本源码解读](https://zhuanlan.zhihu.com/p/360988428)
- [BERT源码详解（二）——HuggingFace Transformers最新版本源码解读](https://zhuanlan.zhihu.com/p/363014957)

1. BERT Tokenization分词模型（BertTokenizer）（请看上篇）
2. BERT Model本体模型（BertModel）（请看上篇）
  - 2.1 BertEmbeddings
  - 2.2 BertEncoder
    - 2.2.1 BertLayer
      - 2.2.1.1 BertAttention
        - 2.2.1.1 BertSelfAttention
        - 2.2.1.2 BertSelfOutput
      - 2.2.1.2 BertIntermediate
      - 2.2.1.3 BertOutput
    - 2.2.2 BertPooler
3. BERT-based Models应用模型
  - 3.1 BertForPreTraining
  - 3.2 BertForSequenceClassification
  - 3.3 BertForMultiChoice
  - 3.4 BertForTokenClassification
  - 3.5 BertForQuestionAnswering
4. BERT训练与优化
  - 4.1 Pre-Training
  - 4.2 Fine-Tuning
    - 4.2.1 AdamW
    - 4.2.2 Warmup

### BERT 快速调用

5行代码

```py
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

inputs = tokenizer("Hello world!")
outputs = model(**inputs)
```


### Tokenization（BertTokenizer）

和BERT有关的Tokenizer主要写在/models/bert/tokenization_bert.py和/models/bert/tokenization_bert_fast.py 中。这两份代码分别对应基本的BertTokenizer，以及不进行token到index映射的BertTokenizerFast，这里主要讲解第一个。

BertTokenizer 是基于`BasicTokenizer`和`WordPieceTokenizer` 的分词器：
- `BasicTokenizer`负责处理的第一步——按标点、空格等分割句子，并处理是否统一小写，以及清理非法字符。继承自 class BertTokenizer(PreTrainedTokenizer):
  - 对于中文字符，通过预处理（加空格）来按字分割；
  - 同时可以通过never_split指定对某些词不进行分割；
  - 这一步是可选的（默认执行）。
- `WordPieceTokenizer`在词的基础上，进一步将词分解为子词（subword） 。
  - subword介于char和word之间，既在一定程度保留了词的含义，又能够照顾到英文中单复数、时态导致的词表爆炸和未登录词的OOV（Out-Of-Vocabulary）问题，将词根与时态词缀等分割出来，从而减小词表，也降低了训练难度；
  - 例如，tokenizer这个词就可以拆解为“token”和“##izer”两部分，注意后面一个词的“##”表示接在前一个词后面。

BertTokenizer 有以下常用方法：
- `from_pretrained`：从包含词表文件（vocab.txt）的目录中初始化一个分词器；
- `tokenize`：将文本（词或者句子）分解为子词列表；
- `convert_tokens_to_ids`：将子词列表转化为子词对应**下标**的列表；
- `convert_ids_to_tokens` ：与上一个相反；
- `convert_tokens_to_string`：将subword列表按“##”拼接回词或者句子；
- `encode`：
  - 对于**单个句子**输入，分解词并加入特殊词形成“\[CLS], x, \[SEP]”的结构并转换为词表对应下标的列表；
  - 对于**两个句子**输入（多个句子只取前两个），分解词并加入特殊词形成“\[CLS], x1, \[SEP], x2, \[SEP]”的结构并转换为下标列表；
- `decode`：可以将encode方法的输出变为完整句子。

构建transformer分词器时, 通常生成两个文件，一个 **merges.txt** 和 **vocab.json** 文件。[transformers分词方法](https://zhuanlan.zhihu.com/p/424565138)
- merges.txt用于把文本转换为单词
- 通过vocab.json文件处理这些单词，该文件只是一个从单词到单词ID的映射文件：

模型在使用之前需要进行**分词**和**编码**，每个模型都会自带`分词器`（tokenizer），熟悉分词器的使用将会提高模型构建的效率。
- string 原始字符串： :hello world!"
- tokens 单词串： [ "hello", "world", "!"]
- token ids 串： [ 7592, 2088, 999]
- ![](https://pic4.zhimg.com/80/v2-b1d35ce62b42d3416f8abe01a073f883_1440w.webp)

```py
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

text = 'hello world!'
# 字符串转换为单词列表
token_ids = tokenizer(text) 
# 单词列表转换为单词ID列表
token_ids = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(text)) 
# 一步到位：字符串 → id列表
# 如： [101, 7592, 2088, 999, 102]
token_ids = tokenizer.encode(text)
tokens = tokenizer.encode(text, max_length=512, padding='max_length', return_tensors='pt') # 使用更多参数
# encode仅输出单词ID张量，encode_plus输出包含单词ID张量和附加张量的字典。
# {'input_ids': [101, 7592, 2088, 999, 102], 'token_type_ids': [0, 0, 0, 0, 0], 'attention_mask': [1, 1, 1, 1, 1]}
token_ids = tokenizer.encode_plus(text)
# 批量转化
# {'input_ids': [[101, 7592, 2088, 999, 102], [101, 7592, 7733, 999, 102]], 'token_type_ids': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], 'attention_mask': [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]}
token_ids = tokenizer.batch_encode_plus([text])
```

#### 变换过程

【2023-3-21】`string`、`tokens`、`ids` 三者转换
- `string` → `tokens` **tokenize**(text: str, **kwargs)
- `tokens` → `string` **convert_tokens_to_string**(tokens: List\[token])
- `tokens` → `ids` **convert_tokens_to_ids**(tokens: List\[token])
- `ids` → `tokens` **convert_ids_to_tokens**(ids: int or List\[int], skip_special_tokens=False)
- `string` → `ids` **encode**(text, text_pair=None, add_special_tokens=True, padding=False, truncation=False, max_length=None, return_tensors=None)
- `ids` → `string` **decode**(token_ids: List[int], skip_special_tokens=False, clean_up_tokenization_spaces=True)

tokenizer用法：encode、encode_plus、batch_encode_plus等等
- **encode_plus**:
  - encode_plus(text, text_pair=None, add_special_tokens=True, padding=False, truncation=False, max_length=None, stride=0, is_pretokenized=False, pad_to_multiple_of=None, return_tensors=None, return_token_type_ids=None, return_attention_mask=None, return_overflowing_tokens=False, return_special_tokens_mask=False, return_offsets_mapping=False, return_length=False)
- **batch_encode_plus**: 输入为 encode 输入的 batch，其它参数相同。注意，plus 是返回一个字典。
- **batch_decode**: 输入是batch.

```py
#这里以bert模型为例，使用上述提到的函数

from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
text = "It's a nice day today!"

#tokenize,#仅用于分词
seg_words = tokenizer.tokenize(text)  
print("tokenize分词结果：\n",seg_words)

#convert_tokens_to_ids，将token转化成id，在分词之后。
#convert_ids_to_tokens,将id转化成token，通常用于模型预测出结果，查看时使用。
seg_word_id = tokenizer.convert_tokens_to_ids(seg_words)  
print("tokenize Id:\n",seg_word_id)

#encode,进行分词和token转换，encode=tokenize+convert_tokens_to_ids
encode_text = tokenizer.encode(text)
print("encode结果：\n",encode_text)

#encode_plus,在encode的基础之上生成input_ids、token_type_ids、attention_mask
encode_plus_text = tokenizer.encode_plus(text)
print("encode_plus结果：\n",encode_plus_text)

#batch_encode_plus,在encode_plus的基础之上，能够批量梳理文本。
batch_encode_plus_text = tokenizer.batch_encode_plus([text,text])
print("batch_encode_plus结果：\n",batch_encode_plus_text)
```

[原文链接](https://blog.csdn.net/weixin_48030475/article/details/128688629)

#### 变换图解

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-03-21T09:35:14.611Z\&quot; agent=\&quot;5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36\&quot; etag=\&quot;RBF3JRrHLDmxsSUVTnIQ\&quot; version=\&quot;21.0.7\&quot;&gt;&lt;diagram id=\&quot;Lw-1uFHNzwHmlxUDpAkU\&quot; name=\&quot;第 1 页\&quot;&gt;7V1bc6M4Fv4t+6Cqna1yCnHnERxnumq6d3o2W9uTpy6MZZtpjNyA2/H8+pVAYJCE7cTg2Gn8EhBCCJ1zPp0rAdp49fxr4q+Xn/AMRUBVZs9AuweqCnVNJ39oy65osSxYNCyScMY67Rsew78Ra1RY6yacobTRMcM4ysJ1szHAcYyCrNHmJwneNrvNcdR86tpfIKHhMfAjsfVLOMuWRautWvv2DyhcLMsnQ9Mprqz8sjN7k3Tpz/C21qRNgDZOMM6Ko9XzGEV08cp1Ke57aLlaTSxBcXbKDd9/Gy3/F2x3H7ZP4dPm2+/eRHFGKiPPDz/asDdms8125RIkeBPPEB1FAZq3XYYZelz7Ab26JUQnbctsFZEzSA4jf4oizw++LfLbxjjCCbkU45j09+Y4zhiNIR1sHkYR12Xmp8v8YXQ0NjmUZOi59bVhtZiECxFeoSzZkS7lDTZbf8aAusnOt3tyqqZ6ZxStyzoxddbVZ0y0qEbfrzM5YEstX3Z9Ff314aPx25dfN7v5auet/vPZHZnHVx3NCB+yU5xkS7zAsR9N9q1eky77Ph8xXrP1+wtl2Y4tuL/JcJNWjaVOswR/q3hcrVpK8gBVc/JfRRaBBmT+eJME6MCLs/fM/GSBsgP9GDXoIhwkcoIiPwt/NIW1c3JZIrkmBrBt4NzTA9cCtpe3jIFDSGtG5NW8aUKOFvRonuDV13VCpuKHMVlwGak/UrlpksePwkVMjgOyyoiQwKNyEBJoctmFVTibFZyA0vBvf5qPR3lhjcM4yxfB8IBxf1QsRXoe5FpRHBn6sik0AE4mkyPlDjaEUivOTqYmG/kzfc/asFCVjVoOgOfzlDAdzwzV9F7PH6qEP2zgPgD7Pj+AwLVFtviBA396lz1nAkOQrWJND4NdFBIRT7TjuDstwODjtGqoiP37JiPDoFLOGfwaHPwS+Z7PkRkEMsmfWc5UUQ5JvsAU7YCsNAFZtUVALjG6jsZmX2BsXwUYXwZ/9ZvEX4mSQsTKmwBHy2GXQLABJg/AI/jr5i0PeQtpvweOIpDzRRoNJySm4jvQkpFHvbfMXEioltMQK/rrSXiUSnOpiY8tER/V6Ik4pab+U8iPcaL8OFclPxCKJCoUGNusdqqMLFZMV/dW1ZOKETvRT2zHaEiafp6KwkYpN5v+dRLjBJLTFiIQMuXkX/9l7JAcQE/4YvSc2YpiaYJwMkJXJjLsF0VVg0dRUQWxJBiqdaCCSM3w67AHyYImuz/rJ090sDvLKM/vn9noxdmuPHsOsz/zrgY7eypHIcf7m+hJec/L8ZoD09cBuCMCuJQi5+K13EIxLY7xDI6jivmzu/ZM5SaJv6t1Ywja+hzDaVpCOtQ4Hi1G7BRxHIGJSXeCMJ5L9TFmMFudKmOKYvuKIuMdRTGsvpUxw4R3zU1Cro7JrJn+1LHrwBLe01dhi9LElmPQ8npJZyx/XFeD12XslPNuELDYnskDfKrNLP0kZa9kft9QB7K3yeZUtyhPG/QuGylNRoX975IOUFk/5133NxV7f/m4dO3H0oGCQp7oIMli+k/C3uRVlfLPL8Xz86fN/VUY7YqunwgDBbjo9AnFETskw/orKuZs8E9hkOAUzymcPfkfUFjcivl+xd1jHKc4IkSQjjUmTBJSFUb5N9rKB1iRodMcb/LT1I/TUYqScF57C8masQvF0tArMU5WflS79sNPQp/8Jdqwn20SGsQ42C/w121dtgw46EWd+WGUiMgfSkZ07mG8EO/EyXpJXqa4oBZtBNiyEVPc3Zy0fpLVLlFvU8weVL1pfiVLyFhzMnz5IKaZU5zLgyy1p2xxMmvOqxqLvMr0W0iGo2MWoD1iSCk+c4YCnBCJw/EoW4bBtxil7EFhHGZh+aJ83xpRDvarcXGj3zzCfsa/5ixM15G/K7vnDjVV+Ue4WhNw9ONMKkien4ZBTZEuxIqgQiFZpbRx6Ezn+XLF2kD2TJfthLY61UzzqJHFA3YH+yMfeoESNduRxF3Uvjx98DpcfScv9fE97jb9eVAWdRz2nHe85wwbS7cbC8Hgy+wrcztAkpgQm//LthTBY9jw93Th19EsziCrQvhvtuVI/HAD1L1nqBvU60uh4BeyEJ9DFKCfV8VWHf2oig1Vmf+pN8AT3YBgYgJXAbYFJhawVeA59BE0OqvT3BnqIlRKF6FJAxL0qkOTa5wJvdfTgFNFc/NB3DFwzTaq9hSjonp8mTzRth9K8tkuYFdZJ9K8i/CFPP9FEgKugu9lsCndTCly/bRU09SjVJPF7fsjmiQofJZvvo/Uz/PkxOTVQUdc85bcz95SP1VJMuFN+yDK+R/1QZT5eFfihCjnXSNEngJxnhBwOgPSAlseoPIUx5AFqJT8140AGKbZYH9bjE3pl4xNqWJoI5yl72jBTfvKFnwIBrKFONVRWi5QdyDVEqE3mpzicIlBxUSFRIDOMpZFDywRGGpQvh9h1LlkizcXRjH6kLUmWd2EVswRj/4eHjointMknqRqR5ZW0Z+2LDFrDW/88ZEuqDpmmkPhJCO7nFYQdUz6PE4+530GAjd1E9gEQKiI4gll8tkbiTXRioVK7nZVda2gLSQLQI5IMxwIyus+HNxKCXpRt4QmS3t2gOsBstvSAxU4MM+BHdMcWOp+cvKs2LySwB6DiQ68e2BP5J0JQpFL74ENFMU0u9p1rabFrUkCMBBelAtk1SMmLdTznL13UUiABpOc4C7NHadv/zWH+JT8+ZrbLG39Ydmf9KKdi9va+6uN8ekdpSLG31El6It53EJfFAd4hgp3uqQghjI2YWNFnqDJD0ad+uVg0jtoMc49dcoeL71pF48IzbNrFI7i15EP0GpuelWZ+7FNr/Lrd556LsNIkyKcW6DdhNa2iuUBrNK/1Vh4w9KAs8rF+dIATeIyvGhpgOilElb9kqUBNSP9CdRt9MOVAWUtQM3Ob60MoCefURKS9aPbZd52Zql6J6UDEj/nBUsHIKdeaZCzU1tKB4SBVK6wSXB1d+d6kC7PkPv1kyVEDFkPoOvcL7b7vqO8r/O+8aLym7akJloa5usiDUKKcrK0r9t1vL9mG3/dzntoy3ijnZffMKud+OydF1525xVr7y6hOb6iNvRU1um+PrP0651L6qMD9Uzq6yh0eImiLucT5SCfvNYq6dIoODmwqPXCsZrW3PqE8NXJHMuXJvMD9cyxN/gZkTb2g0fYr09IPIVlTy2MLXi7c5a1IBco4H0np7KsxYWQnAtzbLsl+5JC3V5rbj+g6Aei/lS5danevnVZS7ev7Iurszz3H2MbcXRUDViQsH7wy3uyV/MohQVcLU/cVoANWTyhU/MVnG9F8tlyFS7VXb9M5rtOGJEDTHvt0AAwA8AMAFMCjJV/+c+sAIZFP68OYAytATCS0LhlifjSW2hJ9qmYxncVLRro3X9XsVbF497Tbu3hv5fnCp79XcXzSKPzn/IxoHXBLyvK6SPJObsZk+imHIwyK/6AyHQf3HM6suKrpMg3suJllWBDdG+I7l1ABXovykyV3EV2Xwg8OhIN+T3g5BF93xDVBo0Jh6bhnCjddFI3FwZkiV6dBwEdeKc293BdUmOp9lUNLcdDWZHlgIcDHg54eDoeunpufjg0JZHm7DqAqOF2nrxre8B19gj5aUP/M1CExkscBh0bgO8KGQ3JdyIujIzqgIwDMg7IeBYy8nn4lYcmL2ug33UvkTH/RM6gOJ4KjxLX/4Xhsf0rwAM8DvA4wONxeHQoJLoT5q6mH8oqwfCPDUrpNNw43aJ6sdUAhSIUmrrED35hMLyObNpzndsvyfe5cMHLWWm3PeUJCRUvPH+9Nu9W54vpXu0UJ6f7f+BadN//G1xt8n8=&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

### Model（BertModel）

和BERT模型有关的代码主要写在`/models/bert/modeling_bert.py`中，这份代码有1k多行，包含BERT模型的基本结构和基于它的微调模型等。继承自class BertModel(BertPreTrainedModel)

BertModel主要为 transformer encoder 结构，包含三个部分：
- `embeddings`，即BertEmbeddings类的实体，对应词嵌入；
- `encoder`，即BertEncoder类的实体；
- `pooler`， 即BertPooler类的实体，这一部分是可选的。

补充：
- BertModel也可以配置为Decoder，不过下文中不包含对这一部分的讨论。

BertModel的前向传播过程中各个参数的含义以及返回值：

```python
def forward(
    self,
    input_ids=None,
    attention_mask=None,
    token_type_ids=None,
    position_ids=None,
    head_mask=None,
    inputs_embeds=None,
    encoder_hidden_states=None,
    encoder_attention_mask=None,
    past_key_values=None,
    use_cache=None,
    output_attentions=None,
    output_hidden_states=None,
    return_dict=None,
): ...
```

说明：
- `input_ids`：经过 tokenizer 分词后的`subword`对应的下标列表；
- `attention_mask`：在self-attention过程中，这一块mask用于标记`subword`所处句子和`padding`的区别，将padding部分填充为0；
- `token_type_ids`： 标记subword当前所处句子（第一句/第二句/padding）；
- `position_ids`： 标记当前词所在句子的位置下标；
- `head_mask`： 用于将某些层的某些注意力计算无效化；
- `inputs_embeds`： 如果提供了，那就不需要input_ids，跨过embedding lookup过程直接作为Embedding进入Encoder计算；
- `encoder_hidden_states`： 这一部分在BertModel配置为decoder时起作用，将执行cross-attention而不是self-attention；
- `encoder_attention_mask`： 同上，在cross-attention中用于标记encoder端输入的padding；
- `past_key_values`：这个参数貌似是把预先计算好的K-V乘积传入，以降低cross-attention的开销（因为原本这部分是重复计算）；
- `use_cache`： 将保存上一个参数并传回，加速decoding；
- `output_attentions`：是否返回中间每层的attention输出；
- `output_hidden_states`：是否返回中间每层的输出；
- `return_dict`：是否按键值对的形式（ModelOutput类，也可以当作tuple用）返回输出，默认为真。

注意
- 这里的head_mask对注意力计算的无效化，和下文提到的注意力头剪枝不同，而仅仅把某些注意力的计算结果给乘以这一系数。

返回值不但包含了encoder和pooler的输出，也包含了其他指定输出的部分（hidden_states和attention等，这一部分在encoder_outputs\[1:]）方便取用

BertModel还有以下的方法，方便BERT玩家进行各种骚操作：
- `get_input_embeddings`：提取embedding中的word_embeddings即词向量部分；
- `set_input_embeddings`：为embedding中的word_embeddings赋值；
- `_prune_heads`：提供了将注意力头剪枝的函数，输入为 {layer_num: list of heads to prune in this layer} 的字典，可以将指定层的某些注意力头剪枝。

补充：
- **剪枝**是一个复杂的操作，需要将保留的注意力头部分的Wq、Kq、Vq和拼接后全连接部分的权重拷贝到一个新的较小的权重矩阵（注意先禁止grad再拷贝），并实时记录被剪掉的头以防下标出错。具体参考BertAttention部分的prune_heads方法。

#### BertEmbeddings

包含三个部分求和得到：
- ![结构图](https://pic3.zhimg.com/80/v2-58b65365587f269bc76358016414dc26_720w.jpg)
- `word_embeddings`，上文中`次词`subword对应的嵌入。
- `token_type_embeddings`，用于表示当前词所在的句子，辅助区别句子与padding、句子对间的差异。
- `position_embeddings`，句子中每个词的**位置**嵌入，用于区别词的顺序。和transformer论文中的设计不同，这一块是训练出来的，而不是通过Sinusoidal函数计算得到的固定嵌入。一般认为这种实现不利于拓展性（难以直接迁移到更长的句子中）。

三个embedding不带权重相加，并通过一层 LayerNorm+dropout 后输出，其大小为 $(batch_size, sequence_length, hidden_size)$。

补充：
- 为什么要用LayerNorm+Dropout呢？为什么要用LayerNorm而不是BatchNorm？可以参考一个不错的[回答](https://www.zhihu.com/question/395811291/answer/1260290120)

#### BertEncoder

包含多层BertLayer，这一块本身没有特别需要说明的地方，不过有一个细节值得参考：
- 利用gradient checkpointing技术以降低训练时的显存占用。
- 补充：gradient checkpointing即梯度检查点，通过减少保存的计算图节点压缩模型占用空间，但是在计算梯度的时候需要重新计算没有存储的值，参考论文《Training Deep Nets with Sublinear Memory Cost》，过程如下[示意图](https://pic2.zhimg.com/v2-24dfc50af29690e09dd5e8cc3319847d_b.webp)
- ![](https://pic2.zhimg.com/v2-24dfc50af29690e09dd5e8cc3319847d_b.webp)

在BertEncoder中，gradient checkpoint是通过torch.utils.checkpoint.checkpoint实现的，使用起来比较方便，可以参考[文档](https://link.zhihu.com/?target=https%3A//pytorch.org/docs/stable/checkpoint.html)

#### BertLayer

这一层包装了BertAttention和BertIntermediate+BertOutput（即Attention后的FFN部分），以及这里直接忽略的cross-attention部分（将BERT作为Decoder时涉及的部分）。

理论上，这里顺序调用三个子模块就可以，没有什么值得说明的地方。

细节：
- apply_chunking_to_forward和feed_forward_chunk了吗（为什么要整这么复杂，直接调用它不香吗？
- 节约显存的技术——包装了一个切分小batch或者低维数操作的功能：这里参数chunk_size其实就是切分的batch大小，而chunk_dim就是一次计算维数的大小，最后拼接起来返回。
- 不过，在默认操作中不会特意设置这两个值（在源代码中默认为0和1），所以会直接等效于正常的forward过程。

#### BertAttention

本以为attention的实现就在这里，没想到还要再下一层……其中，self成员就是多头注意力的实现，而output成员实现attention后的全连接+dropout+residual+LayerNorm一系列操作。出现了上文提到的剪枝操作，即prune_heads方法

class BertAttention(nn.Module)概括如下：
- find_pruneable_heads_and_indices是定位需要剪掉的head，以及需要保留的维度下标index；
- prune_linear_layer则负责将Wk/Wq/Wv权重矩阵（连同bias）中按照index保留没有被剪枝的维度后转移到新的矩阵。

##### BertSelfAttention

预警：这一块可以说是模型的核心区域，也是唯一涉及到公式的地方，所以将贴出大量代码。

class BertSelfAttention(nn.Module)

```python
class BertSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        if config.hidden_size % config.num_attention_heads != 0 and not hasattr(config, "embedding_size"):
            raise ValueError(
                "The hidden size (%d) is not a multiple of the number of attention "
                "heads (%d)" % (config.hidden_size, config.num_attention_heads)
            )

        self.num_attention_heads = config.num_attention_heads
        self.attention_head_size = int(config.hidden_size / config.num_attention_heads)
        self.all_head_size = self.num_attention_heads * self.attention_head_size

        self.query = nn.Linear(config.hidden_size, self.all_head_size)
        self.key = nn.Linear(config.hidden_size, self.all_head_size)
        self.value = nn.Linear(config.hidden_size, self.all_head_size)

        self.dropout = nn.Dropout(config.attention_probs_dropout_prob)
        self.position_embedding_type = getattr(config, "position_embedding_type", "absolute")
        if self.position_embedding_type == "relative_key" or self.position_embedding_type == "relative_key_query":
            self.max_position_embeddings = config.max_position_embeddings
            self.distance_embedding = nn.Embedding(2 * config.max_position_embeddings - 1, self.attention_head_size)

        self.is_decoder = config.is_decoder
```

- 除掉熟悉的query、key、value三个权重和一个dropout，这里还有一个谜一样的position_embedding_type，以及decoder标记（当然，我不打算介绍cross-attenton部分）；
- 注意，hidden_size和all_head_size在一开始是一样的。至于为什么要看起来多此一举地设置这一个变量——显然是因为上面那个剪枝函数，剪掉几个attention head以后all_head_size自然就小了；
- hidden_size必须是num_attention_heads的整数倍，以bert-base为例，每个attention包含12个head，hidden_size是768，所以每个head大小即attention_head_size=768/12=64；
- position_embedding_type是什么？

multi-head self-attention的基本公式
- ![](https://pic4.zhimg.com/80/v2-0c1ffd5ec70918a7c6c42fc7aafd7b0b_720w.png)

注意力头，众所周知是并行计算的，所以上面的query、key、value三个权重是唯一的——这并不是所有heads共享了权重，而是“拼接”起来了。

补充：原论文中多头的理由为Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions. With a single attention head, averaging inhibits this.而另一个比较靠谱的[分析](https://www.zhihu.com/question/341222779/answer/814111138)

forward方法

```python
def transpose_for_scores(self, x):
        new_x_shape = x.size()[:-1] + (self.num_attention_heads, self.attention_head_size)
        x = x.view(*new_x_shape)
        return x.permute(0, 2, 1, 3)

    def forward(
        self,
        hidden_states,
        attention_mask=None,
        head_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
        past_key_value=None,
        output_attentions=False,
    ):
        mixed_query_layer = self.query(hidden_states)

        # 省略一部分cross-attention的计算
        key_layer = self.transpose_for_scores(self.key(hidden_states))
        value_layer = self.transpose_for_scores(self.value(hidden_states))
        query_layer = self.transpose_for_scores(mixed_query_layer)

        # Take the dot product between "query" and "key" to get the raw attention scores.
        attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2))
        # ...
```

- transpose_for_scores用来把hidden_size拆成多个头输出的形状，并且将中间两维转置以进行矩阵相乘；
- 这里key_layer/value_layer/query_layer的形状为：(batch_size, num_attention_heads, sequence_length, attention_head_size)；
- 这里attention_scores的形状为：(batch_size, num_attention_heads, sequence_length, sequence_length)，符合多个头单独计算获得的attention map形状。
- 到这里实现了K与Q相乘，获得raw attention scores的部分，按公式接下来应该是按dk进行scaling并做softmax的操作。奇怪的positional_embedding，以及一堆爱因斯坦求和

。。。

get_extended_attention_mask这个函数是在什么时候被调用的呢？和BertModel有什么关系呢？
- BertModel的继承细节了：BertModel继承自BertPreTrainedModel ，后者继承自PreTrainedModel，而PreTrainedModel继承自[nn.Module, ModuleUtilsMixin, GenerationMixin] 三个基类。——好复杂的封装！
- 这也就是说， BertModel必然在中间的某个步骤对原始的attention_mask调用了get_extended_attention_mask ，导致attention_mask从原始的[1, 0]变为[0, -1e4]的取值。BertModel的前向传播过程中找到了这一调用（第944行）
- 问题解决了：这一方法不但实现了改变mask的值，还将其广播（broadcast）为可以直接与attention map相加的形状。

细节有：
- 按照每个头的维度进行缩放，对于bert-base就是64的平方根即8；
- attention_probs不但做了softmax，还用了一次dropout，这是担心attention矩阵太稠密吗……这里也提到很不寻常，但是原始Transformer论文就是这么做的；
- head_mask就是之前提到的对多头计算的mask，如果不设置默认是全1，在这里就不会起作用；
- context_layer即attention矩阵与value矩阵的乘积，原始的大小为：(batch_size, num_attention_heads, sequence_length, attention_head_size) ；
- context_layer进行转置和view操作以后，形状就恢复了(batch_size, sequence_length, hidden_size)。

#### BertSelfOutput

这一块操作略多但不复杂

```python
class BertSelfOutput(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(self, hidden_states, input_tensor):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = self.LayerNorm(hidden_states + input_tensor)
        return hidden_states
```

补充：这里又出现了LayerNorm和Dropout的组合，只不过这里是先Dropout，进行残差连接后再进行LayerNorm。至于为什么要做残差连接，最直接的目的就是降低网络层数过深带来的训练难度，对原始输入更加敏感

#### BertIntermediate

看完了BertAttention，在Attention后面还有一个全连接+激活的操作

```python
class BertIntermediate(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.intermediate_size)
        if isinstance(config.hidden_act, str):
            self.intermediate_act_fn = ACT2FN[config.hidden_act]
        else:
            self.intermediate_act_fn = config.hidden_act

    def forward(self, hidden_states):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.intermediate_act_fn(hidden_states)
        return hidden_states
```

- 全连接做了一个扩展，以bert-base为例，扩展维度为3072，是原始维度768的4倍之多；
  - 补充：为什么要过一个FFN？不知道……谷歌最近的[论文](https://arxiv.org/abs/2103.03404)貌似说明只有attention的模型什么用都没有
- 激活函数默认实现为gelu（Gaussian Error Linerar Units(GELUS）： ![公式](https://www.zhihu.com/equation?tex=GELU%28x%29%3DxP%28X%3C%3Dx%29%3Dx%CE%A6%28x%29+) ；当然，它是无法直接计算的，可以用一个包含tanh的表达式进行近似（略）。

为什么在transformer中要用这个激活函数
- 补充：看了一些研究，应该是说GeLU比ReLU这些表现都好，以至于后续的语言模型都沿用了这一激活函数。

#### BertOutput

在这里又是一个全连接+dropout+LayerNorm，还有一个残差连接residual connect

```python
class BertOutput(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.intermediate_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(self, hidden_states, input_tensor):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = self.LayerNorm(hidden_states + input_tensor)
        return hidden_states
```

这里的操作和BertSelfOutput不能说没有关系，只能说一模一样……非常容易混淆的两个组件。

### BertPooler

这一层只是简单地取出了句子的第一个token，即[CLS]对应的向量，然后过一个全连接层和一个激活函数后输出

```python
class BertPooler(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.activation = nn.Tanh()

    def forward(self, hidden_states):
        # We "pool" the model by simply taking the hidden state corresponding
        # to the first token.
        first_token_tensor = hidden_states[:, 0]
        pooled_output = self.dense(first_token_tensor)
        pooled_output = self.activation(pooled_output)
        return pooled_output
```

### 小结

- 在HuggingFace实现的Bert模型中，使用了多种节约显存的技术：
  - gradient checkpoint，不保留前向传播节点，只在用时计算；
  - apply_chunking_to_forward，按多个小批量和低维度计算FFN部分；
- BertModel包含复杂的封装和较多的组件。以bert-base为例，主要组件如下：
  - 总计Dropout出现了1+(1+1+1)x12=37次；
  - 总计LayerNorm出现了1+(1+1)x12=25次；
  - 总计dense全连接层出现了(1+1+1)x12+1=37次，并不是每个dense都配了激活函数
- BertModel有极大的参数量。以bert-base为例，其参数量为109M，具体计算过程可以[参考](https://zhuanlan.zhihu.com/p/144582114)

### BERT-based Models

基于BERT的模型都写在/models/bert/modeling_bert.py里面，包括BERT预训练模型和BERT分类模型，UML图如下：
- ![](https://pic1.zhimg.com/80/v2-0e126f74d40d2db8bc133bc67f8055b4_720w.png)

BERT模型一图流（建议保存后放大查看）

首先，以下所有的模型都是基于BertPreTrainedModel这一抽象基类的，而后者则基于一个更大的基类PreTrainedModel。这里我们关注BertPreTrainedModel的功能：
- 用于初始化模型权重，同时维护继承自PreTrainedModel的一些标记身份或者加载模型时的类变量。

#### BertForPreTraining

众所周知，BERT预训练任务包括两个：
- Masked Language Model（MLM）：在句子中随机用[MASK]替换一部分单词，然后将句子传入 BERT 中编码每一个单词的信息，最终用[MASK]的编码信息预测该位置的正确单词，这一任务旨在训练模型根据上下文理解单词的意思；
- Next Sentence Prediction（NSP）：将句子对A和B输入BERT，使用[CLS]的编码信息进行预测B是否A的下一句，这一任务旨在训练模型理解预测句子间的关系。

![](https://pic4.zhimg.com/80/v2-778b166945e69e7689cccfe7532e74e3_720w.jpg)

对应到代码中，这一融合两个任务的模型就是BertForPreTraining。略

这份代码里面也包含了对于只想对单个目标进行预训练的BERT模型（具体细节不作展开）：
- BertForMaskedLM：只进行MLM任务的预训练；
  - 基于BertOnlyMLMHead，而后者也是对BertLMPredictionHead的另一层封装；
- BertLMHeadModel：这个和上一个的区别在于，这一模型是作为decoder运行的版本；
  - 同样基于BertOnlyMLMHead；
- BertForNextSentencePrediction：只进行NSP任务的预训练。
  - 基于BertOnlyNSPHead，内容就是一个线性层……

各种Fine-tune模型，基本都是分类任务：
- ![](https://pic1.zhimg.com/80/v2-d870cb6a4cc1b6f5f7f54cd9f563e468_720w.jpg)

#### BertForSequenceClassification

这一模型用于句子分类（也可以是回归）任务，比如GLUE benchmark的各个任务。
- 句子分类的输入为句子（对），输出为单个分类标签。
结构上很简单，就是BertModel（有pooling）过一个dropout后接一个线性层输出分类

在前向传播时，和上面预训练模型一样需要传入labels输入。
- 如果初始化的num_labels=1，那么就默认为回归任务，使用MSELoss；
- 否则认为是分类任务。

#### BertForMultipleChoice

这一模型用于多项选择，如RocStories/SWAG任务。
- 多项选择任务的输入为一组分次输入的句子，输出为选择某一句子的单个标签。
结构上与句子分类相似，只不过线性层输出维度为1，即每次需要将每个样本的多个句子的输出拼接起来作为每个样本的预测分数。
- 实际上，具体操作时是把每个batch的多个句子一同放入的，所以一次处理的输入为[batch_size, num_choices]数量的句子，因此相同batch大小时，比句子分类等任务需要更多的显存，在训练时需要小心。

#### BertForTokenClassification

这一模型用于序列标注（词分类），如NER任务。
- 序列标注任务的输入为单个句子文本，输出为每个token对应的类别标签。
由于需要用到每个token对应的输出而不只是某几个，所以这里的BertModel不用加入pooling层；
- 同时，这里将_keys_to_ignore_on_load_unexpected这一个类参数设置为[r"pooler"]，也就是在加载模型时对于出现不需要的权重不发生报错。

#### BertForQuestionAnswering

这一模型用于解决问答任务，例如SQuAD任务。
- 问答任务的输入为问题+（对于BERT只能是一个）回答组成的句子对，输出为起始位置和结束位置用于标出回答中的具体文本。
这里需要两个输出，即对起始位置的预测和对结束位置的预测，两个输出的长度都和句子长度一样，从其中挑出最大的预测值对应的下标作为预测的位置。
- 对超出句子长度的非法label，会将其压缩（torch.clamp_）到合理范围。

作为一个迟到的补充，这里稍微介绍一下ModelOutput这个类。它作为上述各个模型输出包装的基类，同时支持字典式的存取和下标顺序的访问，继承自python原生的OrderedDict 类。

### BERT训练和优化

#### Pre-Training

预训练阶段，除了众所周知的15%、80%mask比例，有一个值得注意的地方就是参数共享。

不止BERT，所有huggingface实现的PLM的word embedding和masked language model的预测权重在初始化过程中都是共享的：

#### Fine-Tuning

微调也就是下游任务阶段，也有两个值得注意的地方。

##### AdamW

首先介绍一下BERT的优化器：AdamW（AdamWeightDecayOptimizer）。

这一优化器来自ICLR 2017的Best Paper：《Fixing Weight Decay Regularization in Adam》中提出的一种用于修复Adam的权重衰减错误的新方法。论文指出，L2正则化和权重衰减在大部分情况下并不等价，只在SGD优化的情况下是等价的；而大多数框架中对于Adam+L2正则使用的是权重衰减的方式，两者不能混为一谈。

##### Warmup

BERT的训练中另一个特点在于Warmup，其含义为：
- 在训练初期使用较小的学习率（从0开始），在一定步数（比如1000步）内逐渐提高到正常大小（比如上面的2e-5），避免模型过早进入局部最优而过拟合；
- 在训练后期再慢慢将学习率降低到0，避免后期训练还出现较大的参数变化。
在Huggingface的实现中，可以使用多种warmup策略
- CONSTANT：保持固定学习率不变；
- CONSTANT_WITH_WARMUP：在每一个step中线性调整学习率；
- LINEAR：上文提到的两段式调整；
- COSINE：和两段式调整类似，只不过采用的是三角函数式的曲线调整；
- COSINE_WITH_RESTARTS：训练中将上面COSINE的调整重复n次；
- POLYNOMIAL：按指数曲线进行两段式调整。


### 入门代码

```python
import torch
from transformers import BertModel, BertTokenizer

# 调用bert-base模型，同时模型的词典经过小写处理
model_name = 'bert-base-uncased'
model_name = 'bert-base-chinese' # 中文模型
# ----------- 分词器 ------------
# 读取模型对应的tokenizer
tokenizer = BertTokenizer.from_pretrained(model_name) 
# 【2023-2-22】默认保存路径：~/.cache/huggingface/hub/
tokenizer = BertTokenizer.from_pretrained(model_name, cache_dir='./transformers/')	# cache_dir表示将预训练文件下载到本地指定文件夹下，而不是默认路径
# 获取词表
vocab = tokenizer.get_vocab()
print("vocab: ", len(vocab))

# ----------- 模型 ------------
# 载入模型
model = BertModel.from_pretrained(model_name)
# 本地保存
model = BertModel.from_pretrained(model_name, cache_dir='./transformers/')
# 输出隐含层
model = BertModel.from_pretrained('./model', output_hidden_states = True,)

# 获取词向量矩阵
word_embedding = model.get_input_embeddings()
embed_weights = word_embedding.weight
print("embed_weights: ", embed_weights.shape, type(embed_weights))
# embed_weights: torch.Size([30522, 768]
# ----------- 测试 ------------
# （1）单行文本
input_text = "Here is some text to encode"
# 通过tokenizer把文本变成 token_id
input_ids = tokenizer.encode(input_text, add_special_tokens=True)
# input_ids: [101, 2182, 2003, 2070, 3793, 2000, 4372, 16044, 102]
input_ids = torch.tensor([input_ids])
# 中文测试
input_ids = torch.tensor(tokenizer.encode("遇见被老师提问问题", add_special_tokens=True)).unsqueeze(0)	# 增加一个维度因为输入到Bert模型中要求二维(Batch_size, seq_len)
print("input_ids: ", input_ids)
output = model(input_ids=input_ids)
last_hidden_states_0 = output[0]
print("last_hidden_states_0.shape: ", last_hidden_states_0.shape)
last_hidden_states_1 = output[1]
print("last_hidden_states_1.shape: ", ast_hidden_states_1.shape)
# input_ids:  tensor([[ 101, 6878, 6224, 6158, 5439, 2360, 2990, 7309, 7309, 7579,  102]])
# last_hidden_states_0.shape: torch.Size([1, 11, 768]
# last_hidden_states_1.shape: torch.Size([1, 768]

# （2）pair文本对
text_a = "EU rejects German call to boycott British lamb ."
text_b = "This tokenizer inherits from :class: transformers.PreTrainedTokenizer"

tokens_encode = tokenizer.encode_plus(text=text, text_pair=text_b, max_length=20, truncation_strategy="longest_first", truncation=True)
print("tokens_encode: ", tokens_encode)
# tokens_encode:  {'input_ids': [2, 2898, 12170, 18, 548, 645, 20, 16617, 388, 8624, 3, 48, 20, 2853, 11907, 17569, 18, 37, 13, 3], 'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
# 输出以列表的形式保存
# - input_ids的内容与encode()方法返回的结果相同，为token转化为id之后的表示。
# - token_type_ids的内容表示用来区别两个文本，为0表示第一个文本，为1表示第二个文本。
# - attention_mask表示文本padding的部分(这里没有，所有全为1)。
# 每个部分分别对应于BertModel的输入参数，使用时取出对应键值的内容输入到相应参数即可
# forward(input_ids=None, attention_mask=None, token_type_ids=None, position_ids=None, head_mask=None, inputs_embeds=None, output_attentions=None, output_hidden_states=None, return_dict=None)[SOURCE]


# 获得BERT模型最后一个隐层结果
with torch.no_grad():
    last_hidden_states = model(input_ids)[0]  # Models outputs are now tuples

""" tensor([[[-0.0549,  0.1053, -0.1065,  ..., -0.3550,  0.0686,  0.6506],
         [-0.5759, -0.3650, -0.1383,  ..., -0.6782,  0.2092, -0.1639],
         [-0.1641, -0.5597,  0.0150,  ..., -0.1603, -0.1346,  0.6216],
         ...,
         [ 0.2448,  0.1254,  0.1587,  ..., -0.2749, -0.1163,  0.8809],
         [ 0.0481,  0.4950, -0.2827,  ..., -0.6097, -0.1212,  0.2527],
         [ 0.9046,  0.2137, -0.5897,  ...,  0.3040, -0.6172, -0.1950]]]) 
	shape: (1, 9, 768)     
"""
# ----------- 配置文件 ------------
from transformers import BertConfig
# 获取bert模型结构参数
bert_config = BertConfig.from_pretrained('bert-base-uncased')
print(bert_config.get_config_dict('bert-base-uncased'))
# ({'architectures': ['BertForMaskedLM'], 'attention_probs_dropout_prob': 0.1, 'hidden_act': 'gelu', 'hidden_dropout_prob': 0.1, 'hidden_size': 768, 'initializer_range': 0.02, 'intermediate_size': 3072, 'layer_norm_eps': 1e-12, 'max_position_embeddings': 512, 'model_type': 'bert', 'num_attention_heads': 12, 'num_hidden_layers': 12, 'pad_token_id': 0, 'type_vocab_size': 2, 'vocab_size': 30522}, {})
# ----------- albert模型 ------------
from transformers import AlbertTokenizer, AlbertModel
# albert模型
tokenizer = AlbertTokenizer.from_pretrained("albert-base-v2", cache_dir="./transformers/")
model = AlbertModel.from_pretrained("albert-base-v2", cache_dir="transformers/")
# 多种模型，如XLNet、DistilBBET、RoBERTa等模型都可以以同样的方式进行导

# ----------- 学习率设置 ------------
from transformers import AdaW, get_linear_schedule_with_warmup

warmup_steps = int(args.warmup_proportion * num_train_optimization_steps)	# 定义warmup方式的步长
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=args.adam_epsilon)	# 定义优化器
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps, num_training_steps=num_train_optimization_steps)		# 更新学习率的方式

# ----------- tf模型训练 ------------
def data_incoming(path):
    x = []
    y = []
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split('\t')
            x.append(line[0])
            y.append(line[1])
    df_row = pd.DataFrame([x, y], index=['text', 'label'])
    df_row = df_row.T
    df_label = pd.DataFrame({"label": ['YOUR_LABEL'], 'y': list(range(10))})
    output = pd.merge(df_row, df_label, on='label', how='left')
    return output

def convert_example_to_feature(review):
    return tokenizer.encode_plus(review,
                                 max_length=256,
                                 pad_tp_max_length=True,
                                 return_attention_mask=True,
                                 truncation=True
                                 )

def map_example_to_dict(input_ids, attention_mask, token_type_ids, label):
    return {
               "input_ids": input_ids,
               "token_type_ids": token_type_ids,
               "attention_mask": attention_mask,
           }, label

def encode_example(ds, limit=-1):
    input_ids_list = []
    token_type_ids_list = []
    attention_maks_list = []
    label_list = []
    if limit > 0:
        ds.take(limit)
    for index, row in ds.iterrows():
        review = row["text"]
        label = row['y']
        bert_input = convert_example_to_feature(review)
        input_ids_list.append(bert_input["input_ids"])
        token_type_ids_list.append(bert_input['token_type_ids'])
        attention_maks_list.append(bert_input['attention_maks'])
        label_list.append([label])
    return tf.data.Dataset.from_tensor_slices(
        (input_ids_list, token_type_ids_list, attention_maks_list, label_list)).map(map_example_to_dict)

train = data_incoming(data_path + 'train.tsv')
test = data_incoming(data_path + 'test.tsv')
train = encode_example(train).shuffle(100000).batch(100)
test = encode_example(test).batch(100)
model = TFBertForSequenceClassification(model_path, num_labels=num_labels)
optimizer = tf.keras.optimizers.Adam(1e-5)
model.compile(optimizer=optimizer, loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))
model.fit(train, epochs=epoch, verbose=1, validation_data=test)

```

包括import在内的不到十行代码，我们就实现了读取一个预训练过的BERT模型，来encode我们指定的一个文本，对文本的每一个token生成768维的向量。如果是二分类任务，我们接下来就可以把第一个token也就是\[CLS]的768维向量，接一个linear层，预测出分类的logits，或者根据标签进行训练。

**BERT configuration**

Transformers的源码：路径 src/transformers 下有很多的python代码文件。以 configuration 开头的都是各个模型的配置代码，比如 configuration_bert.py，主要是一个继承自 PretrainedConfig 的类 BertConfig的定义，以及不同BERT模型的config文件的下载路径，下方显示前三个。
- bert-base-uncased的模型的配置，其中包括dropout, hidden_size, num_hidden_layers, vocab_size 等等。
- 比如bert-base-uncased的配置它是12层的，词典大小30522等等，甚至可以在config里利用output_hidden_states配置是否输出所有hidden_state。

```python
BERT_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    "bert-base-uncased": "https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-uncased-config.json",
    "bert-large-uncased": "https://s3.amazonaws.com/models.huggingface.co/bert/bert-large-uncased-config.json",
    "bert-base-cased": "https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-cased-config.json",
}
```

**BERT tokenization**

以tokenization开头的都是跟vocab有关的代码，比如在 tokenization_bert.py 中有函数如whitespace_tokenize，还有不同的tokenizer的类。同时也有各个模型对应的vocab.txt。从第一个链接进去就是bert-base-uncased的词典，这里面有30522个词，对应着config里面的vocab_size。
- 其中，第0个token是\[pad]，第101个token是\[CLS]，第102个token是\[SEP]，所以之前encode得到的 [101, 2182, 2003, 2070, 3793, 2000, 4372, 16044, 102] ，其实tokenize后convert前的token就是 [ '[ CLS]', 'here', 'is', 'some', 'text', 'to', 'en', '##code', '[ SEP]' ]，经过之前BERT论文的介绍，大家应该都比较熟悉了。
- BERT的vocab预留了不少unused token，如果我们会在文本中使用特殊字符，在vocab中没有，这时候就可以通过替换vacab中的unused token，实现对新的token的embedding进行训练。

```python
PRETRAINED_VOCAB_FILES_MAP = {
    "vocab_file": {
        "bert-base-uncased": "https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-uncased-vocab.txt",
        "bert-large-uncased": "https://s3.amazonaws.com/models.huggingface.co/bert/bert-large-uncased-vocab.txt",
        "bert-base-cased": "https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-cased-vocab.txt",
    }
}
```

**BERT modeling**

以modeling开头的就是最关心的模型代码，比如 modeling_bert.py。文件中有许多不同的预训练模型以供下载，可以按需获取。

代码中可以重点看**BertModel**类，它就是BERT模型的基本代码, 类定义中，由embedding，encoder，pooler组成，forward时顺序经过三个模块，输出output。

```python
class BertModel(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.config = config

        self.embeddings = BertEmbeddings(config)
        self.encoder = BertEncoder(config)
        self.pooler = BertPooler(config)

        self.init_weights()
        
 def forward(
        self, input_ids=None, attention_mask=None, token_type_ids=None,
        position_ids=None, head_mask=None, inputs_embeds=None,
        encoder_hidden_states=None, encoder_attention_mask=None,
    ):
    """ 省略部分代码 """
    
        embedding_output = self.embeddings(
            input_ids=input_ids, position_ids=position_ids, token_type_ids=token_type_ids, inputs_embeds=inputs_embeds
        )
        encoder_outputs = self.encoder(
            embedding_output,
            attention_mask=extended_attention_mask,
            head_mask=head_mask,
            encoder_hidden_states=encoder_hidden_states,
            encoder_attention_mask=encoder_extended_attention_mask,
        )
        sequence_output = encoder_outputs[0]
        pooled_output = self.pooler(sequence_output)

        outputs = (sequence_output, pooled_output,) + encoder_outputs[
            1:
        ]  # add hidden_states and attentions if they are here
        return outputs  # sequence_output, pooled_output, (hidden_states), (attentions)
```
BertEmbeddings这个类中可以清楚的看到，embedding由三种embedding相加得到，经过layernorm 和 dropout后输出。

```python
def __init__(self, config):
        super().__init__()
        self.word_embeddings = nn.Embedding(config.vocab_size, config.hidden_size, padding_idx=0)
        self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.hidden_size)
        self.token_type_embeddings = nn.Embedding(config.type_vocab_size, config.hidden_size)
        # self.LayerNorm is not snake-cased to stick with TensorFlow model variable name and be able to load
        # any TensorFlow checkpoint file
        self.LayerNorm = BertLayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        
def forward(self, input_ids=None, token_type_ids=None, position_ids=None, inputs_embeds=None):
        """ 省略 embedding生成过程 """
        embeddings = inputs_embeds + position_embeddings + token_type_embeddings
        embeddings = self.LayerNorm(embeddings)
        embeddings = self.dropout(embeddings)
        return embeddings
```

BertEncoder主要将embedding的输出，逐个经过每一层Bertlayer的处理，得到各层hidden_state，再根据config的参数，来决定最后是否所有的hidden_state都要输出，BertLayer的内容展开的话，篇幅过长，读者感兴趣可以自己一探究竟。

```python
class BertEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.output_attentions = config.output_attentions
        self.output_hidden_states = config.output_hidden_states
        self.layer = nn.ModuleList([BertLayer(config) for _ in range(config.num_hidden_layers)])

    def forward(
        self,
        hidden_states,
        attention_mask=None,
        head_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
    ):
        all_hidden_states = ()
        all_attentions = ()
        for i, layer_module in enumerate(self.layer):
            if self.output_hidden_states:
                all_hidden_states = all_hidden_states + (hidden_states,)

            layer_outputs = layer_module(
                hidden_states, attention_mask, head_mask[i], encoder_hidden_states, encoder_attention_mask
            )
            hidden_states = layer_outputs[0]

            if self.output_attentions:
                all_attentions = all_attentions + (layer_outputs[1],)
        # Add last layer
        if self.output_hidden_states:
            all_hidden_states = all_hidden_states + (hidden_states,)

        outputs = (hidden_states,)
        if self.output_hidden_states:
            outputs = outputs + (all_hidden_states,)
        if self.output_attentions:
            outputs = outputs + (all_attentions,)
        return outputs  # last-layer hidden state, (all hidden states), (all attentions)
```

Bertpooler 其实就是将BERT的\[CLS]的hidden_state 取出，经过一层DNN和Tanh计算后输出。

```python
class BertPooler(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.activation = nn.Tanh()

    def forward(self, hidden_states):
        # We "pool" the model by simply taking the hidden state corresponding
        # to the first token.
        first_token_tensor = hidden_states[:, 0]
        pooled_output = self.dense(first_token_tensor)
        pooled_output = self.activation(pooled_output)
        return pooled_output
```

在这个文件中还有上述基础的BertModel的进一步的变化，比如BertForMaskedLM，BertForNextSentencePrediction这些是Bert加了预训练头的模型，还有BertForSequenceClassification， BertForQuestionAnswering 这些加上了特定任务头的模型。

[Huggingface简介及BERT代码浅析](https://zhuanlan.zhihu.com/p/120315111)

### pipeline NLP快速应用

[参考文章](https://blog.csdn.net/YangStudent/article/details/118879560)：pipeline涉及多个NLP任务，transformers库，pipline函数
- 分类，实体识别，生成，预测，问答，摘要，翻译，相似度，迁移学习，预训练模型，transformer概念
- 类似sklearn的pipeline流水线机制

```python
from transformers import pipeline
 
# 1. 情感分类
classfier1 = pipeline("sentiment-analysis")
print(classfier1("My wife is a beautiful girl"))
# [{'label': 'POSITIVE', 'score': 0.9998767971992493}]
 
# print(classfier1('I am pool', 'My PBL is beautiful, but I love it'))
# [{'label': 'NEGATIVE', 'score': 0.7211759090423584}, {'label': 'POSITIVE', 'score': 0.9998372197151184}]
 
classfier2  = pipeline("zero-shot-classification")
print(classfier2(
    "This a project about the Style transfer",
    candidate_labels = ['education', 'politics', 'business']
))
# {'sequence': 'This a project about the Style transfer', 'labels': ['business', 'education', 'politics'], 'scores': [0.673454225063324, 0.17288313806056976, 0.15366260707378387]}
 
# 2.文本生成
generator1 = pipeline("text-generation") # 默认的文本生成模型是gpt2
print(generator1(
    "I owe 2300 yuan",
    max_length = 50, # 指定生成句的大小
    num_return_sequence = 2, # 指定生成的句子个数
))
# [{'generated_text': "I owe 2300 yuan from the bank since it made me a few dollars but it's just so damn hard to pay. I'm on a two-yearly policy and the current rate I'm using has to be 100 yuan. So, I"}]
#
 
generator2 = pipeline("text-generation", model="distilgpt2") # 指定模型为distilgpt2,轻量的gpt2
print(generator2(
    "I owe 2300 yuan"
))
# [{'generated_text': 'I owe 2300 yuan to the country.”'}]
 
# 3.预测文本遮罩
unmasker = pipeline('fill-mask') # 基于bert
print(unmasker('My favorite girl is <mask>'))
# top_k的含义是返回最有可能的两种结果
# [{'sequence': '<s>My favorite girl is…</s>', 'score': 0.035072073340415955, 'token': 1174, 'token_str': 'âĢ¦'}, {'sequence': '<s>My favorite girl is...</s>', 'score': 0.034020423889160156, 'token': 734, 'token_str': '...'}, {'sequence': '<s>My favorite girl is Barbie</s>', 'score': 0.01795039512217045, 'token': 31304, 'token_str': 'ĠBarbie'}, {'sequence': '<s>My favorite girl is Cinderella</s>', 'score': 0.011553746648132801, 'token': 34800, 'token_str': 'ĠCinderella'}, {'sequence': '<s>My favorite girl is ______</s>', 'score': 0.010862686671316624, 'token': 47259, 'token_str': 'Ġ______'}]
 
# 4.命名实体识别，识别一句话中的，实体，如人，组织，或地点
ner = pipeline('ner', grouped_entities=True) # grouped_entities=True, 允许相似的实体分组到同一个组内
print(ner("I'm working in CCNU , is a beautiful school , and I like Wollongong"))
# [{'entity_group': 'I-ORG', 'score': 0.9960816502571106, 'word': 'CCNU'}, {'entity_group': 'I-LOC', 'score': 0.9867993593215942, 'word': 'Wollongong'}]
 
 
# 5.提取问题答案 在context中提取出question的答案
question_answer = pipeline('question-answering')
print(question_answer(
    question = 'Who are you?',
    context = 'I am XsY and good luck to see you',
))
# {'score': 0.6727198958396912, 'start': 5, 'end': 8, 'answer': 'XsY'}
 
# 6.文本摘要
summarizer = pipeline('summarization')
print(summarizer("""    America has changed dramatically during recent years. Not only has the number of 
    graduates in traditional engineering disciplines such as mechanical, civil, 
    electrical, chemical, and aeronautical engineering declined, but in most of 
    the premier American universities engineering curricula now concentrate on 
    and encourage largely the study of engineering science. As a result, there 
    are declining offerings in engineering subjects dealing with infrastructure, 
    the environment, and related issues, and greater concentration on high 
    technology subjects, largely supporting increasingly complex scientific 
    developments. While the latter is important, it should not be at the expense 
    of more traditional engineering.
    Rapidly developing economies such as China and India, as well as other 
    industrial countries in Europe and Asia, continue to encourage and advance 
    the teaching of engineering. Both China and India, respectively, graduate 
    six and eight times as many traditional engineers as does the United States. 
    Other industrial countries at minimum maintain their output, while America 
    suffers an increasingly serious decline in the number of engineering graduates 
    and a lack of well-educated engineers.
    """))
# [{'summary_text': ' America has changed dramatically during recent years . The number of engineering graduates in the U.S. has declined in traditional engineering disciplines such as mechanical, civil, electrical, chemical, and aeronautical engineering . Rapidly developing economies such as China and India, as well as other industrial countries, continue to encourage and advance the teaching of engineering .'}]
 
 
# 7.翻译
translator = pipeline('translation', model='Helsinki-NLP/opus-mt-zh-en')
print(translator('我是真的很穷不要再坑我了'))
# [{'translation_text': "I'm really poor. Don't lie to me again."}]
```



### 模型信息

[Transformers是TensorFlow 2.0和PyTorch的最新自然语言处理库](https://pytorchchina.com/2020/02/20/transformers_1/)

每个模型架构的详细示例(Bert、GPT、GPT-2、Transformer-XL、XLNet和XLM)可以在完整[文档](https://huggingface.co/transformers/)中找到

```python
import torch
from transformers import *

# transformer有一个统一的API
# 有10个Transformer结构和30个预训练权重模型。
#模型|分词|预训练权重
MODELS = [(BertModel,       BertTokenizer,       'bert-base-uncased'),
          (OpenAIGPTModel,  OpenAIGPTTokenizer,  'openai-gpt'),
          (GPT2Model,       GPT2Tokenizer,       'gpt2'),
          (CTRLModel,       CTRLTokenizer,       'ctrl'),
          (TransfoXLModel,  TransfoXLTokenizer,  'transfo-xl-wt103'),
          (XLNetModel,      XLNetTokenizer,      'xlnet-base-cased'),
          (XLMModel,        XLMTokenizer,        'xlm-mlm-enfr-1024'),
          (DistilBertModel, DistilBertTokenizer, 'distilbert-base-cased'),
          (RobertaModel,    RobertaTokenizer,    'roberta-base'),
          (XLMRobertaModel, XLMRobertaTokenizer, 'xlm-roberta-base'),
         ]

# 要使用TensorFlow 2.0版本的模型，只需在类名前面加上“TF”，例如。“TFRobertaModel”是TF2.0版本的PyTorch模型“RobertaModel”

# 让我们用每个模型将一些文本编码成隐藏状态序列:
for model_class, tokenizer_class, pretrained_weights in MODELS:
    # 加载pretrained模型/分词器
    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights)

    # 编码文本
    input_ids = torch.tensor([tokenizer.encode("Here is some text to encode", add_special_tokens=True)])  # 添加特殊标记
    with torch.no_grad():
        last_hidden_states = model(input_ids)[0]  # 模型输出是元组

# 每个架构都提供了几个类，用于对下游任务进行调优，例如。
BERT_MODEL_CLASSES = [BertModel, BertForPreTraining, BertForMaskedLM, BertForNextSentencePrediction,
                      BertForSequenceClassification, BertForTokenClassification, BertForQuestionAnswering]

# 体系结构的所有类都可以从该体系结构的预训练权重开始
#注意，为微调添加的额外权重只在需要接受下游任务的训练时初始化

pretrained_weights = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(pretrained_weights)
for model_class in BERT_MODEL_CLASSES:
    # 载入模型/分词器
    model = model_class.from_pretrained(pretrained_weights)

    # 模型可以在每一层返回隐藏状态和带有注意力机制的权值
    model = model_class.from_pretrained(pretrained_weights,
                                        output_hidden_states=True,
                                        output_attentions=True)
    input_ids = torch.tensor([tokenizer.encode("Let's see all hidden-states and attentions on this text")])
    all_hidden_states, all_attentions = model(input_ids)[-2:]

    #模型与Torchscript兼容
    model = model_class.from_pretrained(pretrained_weights, torchscript=True)
    traced_model = torch.jit.trace(model, (input_ids,))

    # 模型和分词的简单序列化
    model.save_pretrained('./directory/to/save/')  # 保存
    model = model_class.from_pretrained('./directory/to/save/')  # 重载
    tokenizer.save_pretrained('./directory/to/save/')  # 保存
    tokenizer = BertTokenizer.from_pretrained('./directory/to/save/')  # 重载
```

如何用12行代码训练TensorFlow 2.0模型,然后加载在PyTorch快速检验/测试。

```python
import tensorflow as tf
import tensorflow_datasets
from transformers import *

# 从预训练模型/词汇表中加载数据集、分词器、模型
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = TFBertForSequenceClassification.from_pretrained('bert-base-cased')
data = tensorflow_datasets.load('glue/mrpc')

# 准备数据集作为tf.data.Dataset的实例
train_dataset = glue_convert_examples_to_features(data['train'], tokenizer, max_length=128, task='mrpc')
valid_dataset = glue_convert_examples_to_features(data['validation'], tokenizer, max_length=128, task='mrpc')
train_dataset = train_dataset.shuffle(100).batch(32).repeat(2)
valid_dataset = valid_dataset.batch(64)

# 准备训练:编写tf.keras模型与优化，损失和学习率调度
optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

# 用tf.keras.Model.fit进行测试和评估
history = model.fit(train_dataset, epochs=2, steps_per_epoch=115,
                    validation_data=valid_dataset, validation_steps=7)

# 在PyTorch中加载TensorFlow模型进行检查
model.save_pretrained('./save/')
pytorch_model = BertForSequenceClassification.from_pretrained('./save/', from_tf=True)

#让我们看看我们的模型是否学会了这个任务
sentence_0 = "This research was consistent with his findings."
sentence_1 = "His findings were compatible with this research."
sentence_2 = "His findings were not compatible with this research."
inputs_1 = tokenizer.encode_plus(sentence_0, sentence_1, add_special_tokens=True, return_tensors='pt')
inputs_2 = tokenizer.encode_plus(sentence_0, sentence_2, add_special_tokens=True, return_tensors='pt')

pred_1 = pytorch_model(inputs_1['input_ids'], token_type_ids=inputs_1['token_type_ids'])[0].argmax().item()
pred_2 = pytorch_model(inputs_2['input_ids'], token_type_ids=inputs_2['token_type_ids'])[0].argmax().item()

print("sentence_1 is", "a paraphrase" if pred_1 else "not a paraphrase", "of sentence_0")
print("sentence_2 is", "a paraphrase" if pred_2 else "not a paraphrase", "of sentence_0")
```


# 结束