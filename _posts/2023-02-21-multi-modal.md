---
layout: post
title:  "多模态专题 Multi-Modal"
date:   2023-02-21 16:22:00
categories: 大模型
tags: 多模态 CLIP 柏拉图 
excerpt: 多模态相关知识以及各种新兴大模型
author: 鹤啸九天
mathjax: true
permalink: /modal
---

* content
{:toc}

# 多模态学习笔记

除传统**语言**以及**图像**间的交互作用，结合声音、触觉以及动作等多维度信息进行深度学习，从而形成更准确、更具表现力的多模态表示。
- 相比于单模态，多模态模型处理**多种**数据输入，结构上更复杂，可能涉及使用多个子网络，然后将其输出合并。
- 多模态模型的核心：处理和整合这些不同类型的数据源。这种模型可以捕获跨模态的复杂关系，使机器能够更全面地理解和分析信息，从而在各种任务中表现得更好。

AI模型走向多模态必然性的三大因素：**跨模态任务需求**+**跨模态数据融合**+对人类认知能力的**模拟**。
- [参考](https://www.toutiao.com/article/7310095769632342578)

**多模态AI**以**模态融合**为核心技术环节，围绕 “表征-翻译-对齐-融合-联合学习”五大技术环节，解决实际场景下复杂问题的多模态解任务。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/29e13aa203314291886b827b8f4f18e4~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1702653836&x-signature=h9Fs7PIOvliq6q6%2Bzize7Y%2FaiuU%3D)

多模态应用场景按架构可分为：视频分类、事件检测、情绪分析、视觉问答、情感分析、语音识别、跨模态搜索、图像标注、跨模态嵌入、转移学习、视频解码、图像合成等。

多模态AI实现跨模态任务，应用场景丰富。能够实现基于文本、语音、图片、视频等多模态数据的综合处理应用，完成跨模态领域任务，应用于各种场景。

据布谷实验室统计，当前多模态内容主要应用于商业定制、游戏领域、影视领域、教育领域以及医疗领域五大行业。


## 多模态思考


### 多模态与世界模型


【2024-5-20】神经网络在不同数据和模态上以不同目标进行训练，正趋向于在其表示空间中形成一个共享的现实世界统计模型。

这种推测起名为`柏拉图表示假说`，参考了`柏拉图`的`洞穴寓言`以及其关于理想现实本质的观念。

AI系统的**表征收敛**（Representational Convergence），即不同神经网络模型中的数据点表征方式正变得越来越相似，这种相似性跨不同的模型架构、训练目标乃至数据模态。

什么音速推动了这种收敛？这种趋势会持续下去吗？它的最终归宿在哪里？

经过一系列分析和实验，研究人员推测这种收敛确实有一个终点，并且有一个驱动原则：不同模型都在努力达到对现实的准确表征。

原因：
- 1、**任务通用性**导致收敛（Convergence via Task Generality）
- 2、**模型容量**导致收敛（Convergence via Model Capacity）
- 3、**简单性偏好**导致收敛（Convergence via Simplicity Bias）

深度网络倾向于寻找数据的简单拟合，这种内在的简单性偏差使得大模型在表示上趋于简化，从而导致收敛。
- 论文：[The Platonic Representation Hypothesis](https://arxiv.org/abs/2405.07987)


### 多模态计算

- 虽然人脸、姿态和语音等均能独立地表示一定的情感，但人的相互交流却总是通过信息的综合表现来进行。所以， 只有实现多通道的人机界面，才是人与计算机最为自然的交互方式，它集自然语言、语音、手语、人脸、唇读、头势、体势等多种交流通道为一体，并对这些通道信息进行编码、压缩、集成和融合，集中处理图像、音频、视频、文本等多媒体信息。多模态计算是目前情感计算发展的主流方向。每个模块所传达的人类情感的信息量大小和维度不同。在人机交互中，不同的维度还存在缺失和不完善的问题。因此，人机交互中情感分析应尽可能从多个维度入手，将单一不完善的情感通道补上，最后通过多结果拟合来判断情感倾向。
- 在多模态情感计算研究中，一个很重要的分支就是**情感机器人**和**情感虚拟人**的研究。美国麻省理工学院、日本东京科技大学、美国卡内基·梅隆大学均在此领域做出了较好的演示系统。目前中科院自动化所模式识别国家重点实验室已将情感处理融入到了他们已有的语音和人脸的多模态交互平台中，使其结合情感语音合成、人脸建模、视位模型等一系列前沿技术，构筑了栩栩如生的情感虚拟头像，并积极转向嵌入式平台和游戏平台等实际应用。
- 目前， 情感识别和理解的方法上运用了模式识别、人工智能、语音和图像技术的大量研究成果。例如：在情感语音声学分析的基础上，运用线性统计方法和神经网络模型，实现了基于语音的情感识别原型；通过对面部运动区域进行编码，采用 HMM 等不同模型，建立了面部情感特征的识别方法；通过对人姿态和运动的分析，探索肢体运动的情感类别等等。不过，受到情感信息捕获技术的影响， 以及缺乏大规模的情感数据资源，有关多特征融合的情感理解模型研究还有待深入。随着未来的技术进展，还将提出更有效的机器学习机制。



## 什么是多模态

- 【2023-2-25】[多模态学习综述(MultiModal Learning)](https://zhuanlan.zhihu.com/p/582878508)
- 【2023-6-28】[比LLM更重要的多模态学习](https://www.breezedeus.com/article/tutorial-mml-20230625?theme=next&theme=matery)，含 ppt、视频 资料


### 模态

`模态`（modal）是事情经历和发生的方式，我们生活在一个由多种模态（Multimodal）信息构成的世界，包括**视觉**信息、**听觉**信息、**文本**信息、**嗅觉**信息等等，当研究的问题或者数据集包含多种这样的模态信息时我们称之为`多模态问题`，研究多模态问题是推动人工智能更好的了解和认知我们周围世界的关键。
- ![modal](https://pic3.zhimg.com/80/v2-b090453a88b04dd67e5232d429980fb6_1440w.webp)

`模态`是指一些表达或感知事物的方式，每种信息的来源或者形式都可以称为一种模态。例如:
- 人有触觉，听觉，视觉，嗅觉；
- 信息的媒介，有语音、视频、文字等；
- 多种多样的传感器，如雷达、红外、加速度计等。
- ![img](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fc13741a5-306f-4ed5-85c1-503cb38dc087%2FUntitled.png?table=block&id=11a7820d-0a19-4f82-a225-312ece108b72)

以上的每一种都可以称为一种模态。

相较于图像、语音、文本等`多媒体`(Multi-media)数据划分形式，“模态”是一个更为**细粒度**的概念，<span style='color:blue'>同一媒介下可存在不同的模态</span>。 
- 比如我们可以把两种不同语言当做是两种模态，甚至在两种不同情况下采集到的数据集，亦可认为是两种模态。

通常主要研究模态包括"`3V`"：即`Verbal`(文本)、`Vocal`(语音)、`Visual`(视觉)。

### 多模态

`多模态`即是从多个模态表达或感知事物。 `多模态`可归类为**同质性**的模态，例如从两台相机中分别拍摄的图片，异质性的模态，例如图片与文本语言的关系。

多模态可能有以下三种形式：
- 描述**同一对象**的**多媒体**数据。如互联网环境下描述某一特定对象的视频、图片、语音、文本等信息。下图即为典型的多模态信息形式。
  - ![](https://pic3.zhimg.com/80/v2-0f9181a9b97891fab9a4ba4ab55a54f2_1440w.webp)
- 来自**不同传感器**的同一类媒体数据。如医学影像学中不同的检查设备所产生的图像数据， 包括B超(B-Scan ultrasonography)、计算机断层扫描(CT)、核磁共振等；物联网背景下不同传感器所检测到的同一对象数据等。
- 具有不同数据结构特点、表示形式的表意符号与信息。如描述同一对象的结构化、非结构化的数据单元；描述同一数学概念的公式、逻辑 符号、函数图及解释性文本；描述同一语义的词向量、词袋、知识图谱以及其它语义符号单元等。

通常主要研究模态包括"3V"：即`Verbal`(文本)、`Vocal`(语音)、`Visual`(视觉)。 人跟人交流时的多模态：
- ![](https://pic4.zhimg.com/80/v2-225d569ddd4d0427b54c44d34aa6b18f_1440w.webp)

### 多模态学习

`多模态机器学习`是从多种模态数据中学习并且提升自身的算法，它不是某一个具体的算法，它是一类算法的总称。
- 从语义感知的角度切入，多模态数据涉及不同的感知通道如视觉、听觉、触觉、嗅觉所接收到的信息;
- 在数据层面理解，多模态数据则可被看作多种数据类型的组合，如图片、数值、文本、符号、音频、时间序列，或者集合、树、图等不同数据结构所组成的复合数据形式，乃至来自不同数据库、不同知识库的各种信息资源的组合。对多源异构数据的挖掘分析可被理解为多模态学习。
- ![](https://pic4.zhimg.com/80/v2-779aef8e97481d9cf2aa0dcc5f6e005b_1440w.webp)

与此相对的，就是`单模态学习`（Unimodal Learning）。
- 在单模态学习中，在单一模态的数据上进行建模，比如文本

`多模态机器学习`，英文全称 MultiModal Machine Learning (MMML)
- 从异构和互联数据中学习的科学
- ![img](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fb87d3df2-d5f6-4ba8-b315-7e23ecd8a15d%2FUntitled.png?table=block&id=15082eae-0591-4aea-9510-511ec919cfd9)
- ![img](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F093fa1f2-a2b3-4d3f-8719-62218cbb6eb3%2FUntitled.png?table=block&id=e7c6bdfc-2cd6-4533-8eb2-4f50d9aa8773)
- ![](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F3b3e1597-a3d7-4952-90df-6bd12ea70251%2FUntitled.png?table=block&id=b9f93060-a9ac-40d3-8e6f-0bd942228a54)

#### 多模态优于单模态

多模态数据可让不同模态的数据之间互相借鉴，提升单模态能⼒

不同模态之间具有以下特性：
- 异构（Heterogeneous）：不同的结构、表示⽅法
- 互联（Interconnected）：信息相关或共享
- 交互（Interaction）：通过交互产⽣新的信息

加⼊视觉信息后，⼩LM模型（1B量级）也能具有CoT 能⼒

使⽤更少的数据量，就可以通过精调获得效果更好的垂域模型

源自[ppt](https://file.notion.so/f/s/5e1f507e-b484-4903-86dd-bfec2c60968d/Multimodal_Learning--much_more_important_than_LLM.pdf?id=48cd395e-0cca-4bc4-9f02-9ca655cca25d&table=block&spaceId=9341931a-53f0-48e1-b026-0f1ad17b457c&expirationTimestamp=1688029035979&signature=60hvL-JSY6_Ez70e7x2-RPSVri7uNOE1N0vs_4rb73Q)

#### 多模态更有可能实现AGI

Yann LeCun
- 单靠语言模型是无法实现AGI的，人类自身是多模态学习的生物，而且很多信息在单纯的语言中难以体现。
- 当 GPT3.5 或 GPT-4 刚出现时，很多人觉得离AGI似乎越来越近了，但现在看来，LLM仍存在很多难以解决的问题。在模型参数达到1000亿级别之后，增加更多的参数只能带来越来越小的收益。

向AGI进军，仅仅依赖LLM是不够的，需要让模型接触到更多的模态数据。
- 这也是为什么像Meta这样的公司在推动多模态学习方面投入了大量的精力，他们不仅在图像处理方面具有传统优势，而且在多模态学习领域也开源了许多模型。

源自[ppt](https://file.notion.so/f/s/5e1f507e-b484-4903-86dd-bfec2c60968d/Multimodal_Learning--much_more_important_than_LLM.pdf?id=48cd395e-0cca-4bc4-9f02-9ca655cca25d&table=block&spaceId=9341931a-53f0-48e1-b026-0f1ad17b457c&expirationTimestamp=1688029035979&signature=60hvL-JSY6_Ez70e7x2-RPSVri7uNOE1N0vs_4rb73Q)

## 多模态历史

`多模态学习`不是近几年才火起来，而是近几年因为深度学习使得多模态效果进一步提升。

从1970年代起步，多模态技术经历的4个发展阶段，在2012后迎来 Deep Learning 阶段，在2016年后进入目前真正的多模态阶段。 
- 第一阶段为基于`行为`的时代(1970s until late 1980s)，这一阶段主要从心理学的角度对多模态这一现象进行剖析。  
- 第二阶段基于`计算`的时代(1980 - 2000)，这一阶段主要利用一些浅层的模型对多模态问题进行研究，其中代表性的应用包括视觉语音联合识别，多模态情感计算等等。  
- 第三阶段基于`交互`的时代，这一阶段主要主要从交互的角度入手，研究多模态识别问题，其中主要的代表作品包括苹果的语音助手Siri等。  
- 第四阶段基于`深度学习`的时代，促使多模态研究发展的关键促成因素有4个
  - 1）更大规模的多模态数据集；
  - 2）更强大的算力(NPU/GPU/TPU)；
  - 3）强大的视觉特征抽取能力；
  - 4）强大的语言特征抽取能力。

![](https://pic1.zhimg.com/80/v2-ba59d473bb15c4bf00f3e0811b9d47c6_720w.webp?source=1940ef5c)

多模态发展的四个时期
- ![](https://pic4.zhimg.com/80/v2-f77192c7d83a16ebad1b068378c523e3_1440w.webp)



### 行为时代

The “behavioral” era (1970s until late 1980s)，这一阶段主要从**心理学**的角度对多模态这一现象进行剖析。
- Chicago 的McNeill 认为手势是说话人的思考行为，是言语表达的重要组成部分，而不仅仅是补足。
- 1976年的McGurk效应：当语音与唇形不符合时，大脑会脑补出中和的声音MCGURK, H., MACDONALD, J. Hearing lips and seeing voices. Nature 264, 746–748 (1976). The McGurk Effect Video

### 计算时代

The “computational” era (late 1980s until 2000)，这一阶段主要利用一些浅层的模型对多模态问题进行研究，其中代表性的应用包括视觉语音联合识别，多模态情感计算等等。
- 视频音频语音识别(AVSR)，在声音的低信噪比下，引入视觉信号能够极大提升识别准确率
- 多模态/多感知接口：情感计算：与情感或其他情感现象有关、源于情感或有意影响情感的计算[Rosalind Picard]
- 多媒体计算：CMU曾有过信息媒体数字视频库项目[1994-2010]，

### 交互时代

The “interaction” era (2000 - 2010)，这一阶段主要主要从交互的角度入手，研究多模态识别问题，其中主要的代表作品包括苹果的语音助手Siri等。

拟人类多模态交互过程

- IDIAP实验室的AMI项目[2001-2006]，记录会议录音、同步音频视频、转录与注释；
- Alex Waibel的CHIL项目，将计算机置于人类交互圈中，多传感器多模态信号处理，面对面交互

IMI Projet & CHIL Project
- 2003-2008 SRI的学习和组织认知助手，个性化助手，Siri就是这个项目的衍生产品
- 2008-2011 IDIAP的社交信号处理网络，数据库http://sspnet.eu。

CALO Project & SSP Project


### 深度学习时代

The “deep learning” era (2010s until …)，促使多模态研究发展的关键促成因素有4个
- 1）新的大规模多模态数据集
- 2）GPU快速计算
- 3）强大的视觉特征抽取能力
- 4）强大的语言特征抽取能力。
                        

## 多模态结构

多模态人工智能强调不同模态数据之间的**互补性**和**融合性**，通过整合多种模态的数据，利用表征学习、模态融合与对齐等技术，实现跨模态的感知、理解和生成，推动智能应用的全面发展。

三部分：**数据采集与表示**、**数据处理与融合**、**学习与推理**
- 传感器：多模态学习中，传感器用于捕捉不同模态的数据，如摄像头捕捉图像（视觉模态）、麦克风捕捉声音（声音模态）等。
  - 传感器是多模态数据采集的起点，它使得机器能够感知并获取来自不同物理世界的信息。
  - 模态是指信息的表现形式或感知方式，如文本、图像、声音、视频等
  - 多模态是指利用来自多个不同模态的数据进行学习和推理的过程。这些模态可以是文本、图像、声音、视频等的组合。
  - 不同模态提供了不同的信息渠道，它们之间可能存在冗余性，但更多的是互补性。多模态模型能够整合来自不同模态的信息，正是利用这些不同模态的信息来增强模型的感知与理解能力。
- 模态融合：将来自不同模态的信息进行有效整合的过程。
  - **早期**融合：在数据处理的早期阶段就将不同模态的数据合并在一起。
  - **晚期**融合：在数据处理的后期阶段才将不同模态的信息进行整合。
  - **混合**融合：结合早期融合和晚期融合的优点，在不同的处理阶段进行多次融合。
  - 模态融合能够充分利用不同模态之间的互补性，提高模型的性能和鲁棒性。
- 模态对齐：寻找来自不同模态数据之间的对应关系或一致性。
  - **时间**维度对齐：如将视频中的动作与音频中的语音进行对齐。
  - **空间**维度对齐：如将图像中的像素与文本中的单词进行对齐。
  - 模态对齐是多模态学习中实现不同模态信息有效融合的重要前提。通过对齐操作，可以确保不同模态的数据在时间和空间上保持一致性，从而进行更有效的融合和推理。
- **多模态学习**：利用来自多个不同模态的数据进行学习和推理的过程。
  - 它旨在整合不同模态之间的互补信息，以提高模型的感知与理解能力。
  - 多模态学习是当前人工智能领域的一个研究热点，它推动了智能应用的边界扩展。通过多模态学习，可以构建更加智能、更加全面的系统来应对复杂多变的现实世界。

多模态机器学习的核心任务主要包括`表示学习`，`模态映射`，`模态对齐`，`模态融合`，`协同学习`。



### 表示学习

`表示学习`（Representation）：主要研究如何将多个模态数据所蕴含的语义信息，数值化为实值向量，简单来说就是**特征化**。
- `单模态`的表示学习负责将信息表示为计算机可以处理的数值向量或者进一步抽象为更高层的特征向量 Feature；
- 而多模态表示学习通过利用多模态之间的互补性，剔除模态间的冗余性，从而学习到更好的特征 Feature。

那在表示学习中主要包括两大研究方向：
- `联合表示`（Joint Representations）：将多个模态的信息一起映射到一个统一的多模态向量空间。（CLIP 和 DALL·E 使用简单的联合表示，不过效果出奇的赞）。 
- `协同表示`（Coordinated Representations）：将多模态中的每个模态分别映射到各自的表示空间，但映射后的向量之间满足一定的相关性约束（例如线性相关）。 
- <img src="https://pic1.zhimg.com/50/v2-77531575a4083c22b18b399dd17bf54e\_720w.jpg?source=1940ef5c" data-caption="" data-size="normal" data-rawwidth="1952" data-rawheight="508" class="origin\_image zh-lightbox-thumb" width="1952" data-original="https://pica.zhimg.com/v2-77531575a4083c22b18b399dd17bf54e\_r.jpg?source=1940ef5c"/>

### 下游任务

接着就是下游任务对特征进行理解（学术上也叫做内容理解），典型的下游任务包括`视觉问答`、`视觉推理`、`视觉联合推理`、`图像检索`、`视频检索`。
- 视觉问答（Visual Question Answering，VQA）：根据给定的图片提问，从候选中选择出正确的答案，VQA2.0 中从 COCO 图片中筛选了超过100万的问题，训练模型来预测最常见的3129个回答，其本质上可以转化成一个分类问题。
- <img src="https://pic1.zhimg.com/50/v2-f3e6e48c5a6647fc496a5533cb1223a4\_720w.jpg?source=1940ef5c" data-caption="" data-size="normal" data-rawwidth="1538" data-rawheight="402" class="origin\_image zh-lightbox-thumb" width="1538" data-original="https://pic1.zhimg.com/v2-f3e6e48c5a6647fc496a5533cb1223a4\_r.jpg?source=1940ef5c"/>
- 视觉推理（Visual Reasoning，VR）：视觉推理相对视觉问答更为复杂, 其可以分解为两个子任务视觉问答（Q->A）和选出答案的原因（QA->R）, 除了回答的问题需要用自然语言表达具有挑战性的视觉问题外, 模型还需要解释为什么作出这样的回答, 其最开始由华盛顿大学提出, 同时发布的 VCR 数据集包含 11 万的电影场景和 29 万的多项选择问题。
- <img src="https://picx.zhimg.com/50/v2-1d732cb95b79362f2ca3129fed2af035\_720w.jpg?source=1940ef5c" data-caption="" data-size="normal" data-rawwidth="1190" data-rawheight="295" class="origin\_image zh-lightbox-thumb" width="1190" data-original="https://picx.zhimg.com/v2-1d732cb95b79362f2ca3129fed2af035\_r.jpg?source=1940ef5c"/>
- 检索任务（Index Task）：主要包括文本检索图片或者图片检索文本，检索任务应该不用加以过多的解释了，比较好理解，就是以文搜图或者以图搜文。下面图中就是Google 以图搜文的服务，当然包括华为手机里面的截图识字，淘宝拼多多的以文搜图等身边很多诸如此类的服务啦。
- <img src="https://pic1.zhimg.com/50/v2-ae0f2f691f4c09ef198b3575f71b2a31\_720w.jpg?source=1940ef5c" data-caption="" data-size="normal" data-rawwidth="1493" data-rawheight="553" class="origin\_image zh-lightbox-thumb" width="1493" data-original="https://picx.zhimg.com/v2-ae0f2f691f4c09ef198b3575f71b2a31\_r.jpg?source=1940ef5c"/>



### 跨模态预训练

- 图像/视频与语言预训练。
- 跨任务预训练

ChatGPT 对多模态领域技术发展方向有什么影响？那必然是：卷起来了！
- 2023年3月6日，谷歌发布“通才”模型`PaLM-`E，作为一种多模态具身 VLM，它不仅可以理解图像，还能理解、生成语言，执行各种复杂的机器人指令而无需重新训练。还展示出了强大的**涌现能力**（模型有不可预测的表现）。
- 没隔多久，微软开始拉着OpenAI，N鸣惊人。
- 3月15日，OpenAI携手微软于发布了GPT-4，也是关注**多模态**的，实验效果要比`PaLM`好，并且可以执行非常多的任务，比如，GPT4 在各种职业和学术考试上表现和人类水平相当。
  - 模拟律师考试，GPT4 取得了前 10% 的好成绩
  - 做美国高考 SAT 试题，GPT-4 也在阅读写作中拿下 710 分高分、数学 700 分（满分 800）。
- Bing浏览器立马就把模型用了起来, 推出 New Bing
- 3月17日，微软发布office 全家桶，将通过生成式人工智能（AI）技术来增强 Office 办公套装：Microsoft 365 Copilot，用于 Office 套装中的 Word、Excel 和 PowerPoint 等软件。新工具将帮助商业客户更快地**撰写文档**，生成**艺术画**，以及**创建图表**，帮助企业的数百万员工节省大量时间。
  - 微软CEO纳德拉表示，今天是一个里程碑，意味着我们与电脑的交互方式迈入了新的阶段，从此我们的工作方式将永远改变，开启新一轮的生产力大爆发。
- 3月21日，支持 AI画图 Image Creator，背后调用 OpenAI 的 DALL-E

#### CLIP

OpenAI 推出了 CLIP，在400M的**图像-文本对**数据上，用最朴素的**对比损失**训练双塔网络，利用text信息监督视觉任务自训练，对齐了两个模态的特征空间，本质就是将`分类任务`化成了`图文匹配`任务，效果可与全监督方法相当。
- 在近 30 个数据集上 zero-shot 达到或超越主流监督学习性能。
- CLIP：《[Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020)》

作者：[ZOMI酱](https://www.zhihu.com/question/505125640/answer/2633346368)

CLIP算法原理
- CLIP 不预先定义图像和文本标签类别，直接利用从互联网爬取的 400 million 个image-text pair 进行图文匹配任务的训练，并将其成功迁移应用于30个现存的计算机视觉分类。
- CLIP 无需利用 ImageNet 的数据和标签进行训练，就可以达到 ResNet50 在 ImageNet数据集上有监督训练的结果，所以叫做 Zero-shot。

CLIP（contrastive language-image pre-training）主要的贡献就是利用无监督的文本信息，作为监督信号来学习视觉特征。CLIP 作者先是回顾了并总结了和上述相关的两条表征学习路线： 
- 构建image和text的联系，比如利用已有的image-text pair数据集，从text中学习image的表征；  
- 获取更多的数据（不要求高质量，也不要求full labeled）然后做弱监督预训练，就像谷歌使用的JFT-300M数据集进行预训练一样（在JFT数据集中，类别标签是有噪声的）。具体来说，JFT中一共有18291个类别，这能教模型的概念比ImageNet的1000类要多得多，但尽管已经有上万类了，其最后的分类器其实还是静态的、有限的，因为你最后还是得固定到18291个类别上进行分类，那么这样的类别限制还是限制了模型的zero-shot能力。 

这两条路线其实都展现了相当的潜力，前者证明 paired image-text 可以用来训练视觉表征，后者证明扩充数据能极大提升性能，即使数据有noise。于是high-level上，CLIP 作者考虑从网上爬取大量的 image-text pair 以扩充数据，同时这样的 pairs 是可以用来训练视觉表征的。作者随即在互联网上采集了4亿个 image-text 对，准备开始训练模型。

CLIP流程有三个阶段：
- Contrastive pre-training：对比预训练阶段，使用image-text对进行对比学习训练。
- Create dataset classifier from label text：提取预测类别文本特征。
- Use for zero-shot prediction：进行 Zero-Shot 推理预测。
- ![](https://picx.zhimg.com/80/v2-340920caff256e06c29cff7097e23e62_720w.webp?source=1940ef5c)

#### PaLM-E

【2023-3-7】谷歌发布了个多模态模型 `PaLM-E`，使用传感器数据、自然语言、视觉训练，能直接用人话操作机器人完成任务。
- [PaLM-E: An Embodied Multimodal Language Model](https://palm-e.github.io/)

### Language-Audio

- Text-to-Speech Synthesis: 给定文本，生成一段对应的声音。
- Audio Captioning：给定一段语音，生成一句话总结并描述主要内容。(不是语音识别)

### Vision-Audio

- Audio-Visual Speech Recognition(视听语音识别)：给定某人的视频及语音进行语音识别。
- Video Sound Separation(视频声源分离)：给定视频和声音信号(包含多个声源)，进行声源定位与分离。
- Image Generation from Audio: 给定声音，生成与其相关的图像。
- Speech-conditioned Face generation：给定一段话，生成说话人的视频。
- Audio-Driven 3D Facial Animation：给定一段话与3D人脸模版，生成说话的人脸3D动画。

### Vision-Language

- Image/Video-Text Retrieval (图(视频)文检索): 图像/视频<-->文本的相互检索。
- Image/Video Captioning(图像/视频描述)：给定一个图像/视频，生成文本描述其主要内容。
- Visual Question Answering(视觉问答)：给定一个图像/视频与一个问题，预测答案。
- Image/Video Generation from Text：给定文本，生成相应的图像或视频。
- Multimodal Machine Translation：给定一种语言的文本与该文本对应的图像，翻译为另外一种语言。
- Vision-and-Language Navigation(视觉-语言导航)： 给定自然语言进行指导，使得智能体根据视觉传感器导航到特定的目标。
- Multimodal Dialog(多模态对话)： 给定图像，历史对话，以及与图像相关的问题，预测该问题的回答。

### 定位相关的任务

- Visual Grounding：给定一个图像与一段文本，定位到文本所描述的物体。
- Temporal Language Localization: 给定一个视频即一段文本，定位到文本所描述的动作(预测起止时间)。
- Video Summarization from text query：给定一段话(query)与一个视频，根据这段话的内容进行视频摘要，预测视频关键帧(或关键片段)组合为一个短的摘要视频。
- Video Segmentation from Natural Language Query: 给定一段话(query)与一个视频，分割得到query所指示的物体。
- Video-Language Inference: 给定视频(包括视频的一些字幕信息)，还有一段文本假设(hypothesis)，判断二者是否存在语义蕴含(二分类)，即判断视频内容是否包含这段文本的语义。
- Object Tracking from Natural Language Query: 给定一段视频和一些文本，追踪视频中文本所描述的对象。
- Language-guided Image/Video Editing: 一句话自动修图。给定一段指令(文本)，自动进行图像/视频的编辑。

### 更多模态

- Affect Computing (情感计算)：使用语音、视觉(人脸表情)、文本信息、心电、脑电等模态进行情感识别。
- Medical Image：不同医疗图像模态如CT、MRI、PETRGB-D模态：RGB图与深度图


## 语料库


### 多模态情感分析语料库

【2021-8-13】[哈工大：多模态情感分析语料库调研](https://mp.weixin.qq.com/s/YQxGvevrYixWcXXgKg0NXw)

介绍相关子任务和对应数据集以及在数据集上的最新研究工作。主要分为：
- 面向**视频评论**的情感分析
- 面向视频评论的**细粒度**情感分析
- 面向**视频对话**的情绪分析
- 面向视频的**反讽**识别
- 面向**图文**的反讽识别
- 面向图文的情感分析
- 面向图文的细粒度情感分析、幽默检测、抑郁检测。

本文分别总结了相关数据集和方法，具体内容见第三部分。

[多模态情感分析简述](https://zhuanlan.zhihu.com/p/97170240), 任务概览，总结如下：

![多模态情感分析任务概览](https://pic1.zhimg.com/80/v2-18dfa11b0b0a41fba2f1a92a54cbad18_1440w.jpg)

多模态情感分析相关数据集和方法概览

|模态|任务|数据集及下载地址|方法|
|---|---|---|---|
|声图文|面向视频评论的情感分析|[Youtube数据集](https://projects.ict.usc.eduyoutube)，[MOSI数据集](https://github.com/A2Zadeh/CMU-MultimodalSDK)，[MOSEI数据集](https://github.com/A2Zadeh/CMU-MultimodalSDK)|Self-MM，Mult|
|声图文|面向视频评论的细粒度情感分析|[CH-SIMS数据集](https://github.com/thuiar/MMSA)|MTFN|
|声图文|面向视频对话的情绪分析|[IEMOCAP数据集](https://sail.usc.edu/iemocap/), [MELD数据集](https://affective-meld.github.io)|DialogueRNN, MESM|
|声图文|面向视频的反讽识别|[MUStARD数据集](https://github.com/soujanyaporia/MUStARD)|Early Fusion +SVM|
|图文|面向图文的反讽识别|[Twitter反讽数据集](https://github.com/headacheboy/data-of-multimodal-sarcasm-detection)|D&R net|
|图文|面向图文的情感分析|[Yelp数据集](https://www.yelp.com/dataset),[MVSA数据集](http://mcrlab.net/research/mvsa-sentiment-analysis-on-multi-view-social-data/)||
|图文|面向图文的细粒度情感分析|[Multi-ZOL数据集](https://github.com/xunan0812/MIMN),[Twitter-15&17数据集](https://github.com/jefferyYu/TomBERT)|TomBert|
|声图文|幽默检测|[UR-FUNNY数据集](https://github.com/ROC-HCI/UR-FUNNY)|C-MFN|
|声图文|抑郁检测|[DAIC-WOZ数据集](https://dcapswoz.ict.usc.edu)||
|图文|抑郁检测|[Twitter抑郁检测数据集](https://depressiondetection.droppages.com)|MDL|

详情见原文

## 多模态模型


### 多模态模型榜单

【2024-8-2】[中文多模态大模型基准8月榜单发布！8大维度30个测评任务，3个模型超过70分](https://mp.weixin.qq.com/s/8QtQCk-z2QfZVl6jmYuJMg)

测评要点
- 1：**GPT-4o领跑**
  - `GPT-4o` 取得74.36分，领跑多模态基准。其中基础多模态认知能力和应用能力均有70+分的表现，在技术和应用方面均有一定领先优势。
- 2：**国内多模态大模型表现不俗**
  - 国内多模态大模型 `hunyuan-vision` 和 `InternVL2-40B` 表现不俗，取得70+分的优异成绩，仅次于 `GPT-4o`。尤其在多模态应用方面领先 `Claude3.5-Sonnet` 和 `Gemini-1.5-Pro`，展现出较强的应用优势。
- 3：国内大模型**基础能力仍需提升**
  - 在基础能力方面国内大模型较海外模型仍有一定差距，尤其在细粒度视觉认知任务上，国内外最好模型有5分的差距，需要进一步对多模态深度认知能力做优化提升。

> GPT-4o > hunyuan-vision > InterVL2-40B > Claude3.5-Sonnet > Gemini-1.5-Pro > Step-1V-8k > GPT-4-Turbo-0409 > GLM-4v > Qwen-VL-Max > ERNIE-4-Turbo > Qwen-VL-Plus > Yi-VL-34B


### 模型汇总

[多模态大模型入门指南-长文慎入](https://zhuanlan.zhihu.com/p/682893729)

模型架构5个部分：**模态编码器**、**输入投影器**、**语言模型**骨干、**输出投影器**和**模态生成器**。
- ![](https://picx.zhimg.com/80/v2-d1f277adfe5d90b5a872fc2acaa6f08f_1440w.webp)
- 多模态理解主要是前三个部分。（模态对齐）训练期间，encoder，LLM Backbone 和 generator 一般保持冻结。
- 主要优化输出和输出的 projector。由于Projector 是轻量级的模块，MM-LLMs 中可以训练的参数比例和总参数相比非常小（2% 左右），模型的总体参数规模取决于LLM 部分。

对比分析
- Vision Encoder 视觉编码器 
- VL Adapter 转换器  
- Projection Layer 映射层

| 模型   | 时间 | 机构 | 分辨率 | 模型大小 | 视觉编码器 | 转换器  | LLM    | 映射层 | 备注    |
|-------|---------|------|------|------|--------|---------|----------|-----|----------|
| `Flamingo`        | 2022.04 | DeepMind  | 480      | 80P    | NFNet F6            | Perceiver Resampler | Chinchilla 70B + GATED XATTN-DENSE   |     | 接入LLM的多模态      |
| `BLIP-2`          | 2023.01 | Saleforce | 224      | 7B     | EVA-CLIP ViT-g/14   | Q-Former            | Flan-T5/OPT-6.7B        |     |        |
| `MiniGPT4-v1`     | 2023.04 | KAUST     | 224      | 13B    | EVA-CLIP ViT-g/14   | Q-Former+MLP        | Vicuna-13B-v0     |     | 基于BLIP-2进行改进   |
| `InstructBLIP`    | 2023.05 | Saleforce | 224      | 13B    | EVA-CLIP ViT-g/14   | Q-Former            | Flan-T5/Vicuna-13B    |     | 对BLIP2进行大规模    |
| `VisualGLM-6B`    | 2023.05 | 智谱      | 224      | 6B     | EVA-CLIP ViT-g/14   | Q-Former            | ChatGLM-6B   |     |                |
| `Shikra`          | 2023.06 | 字节      | 224      | 7B/13B | CLIP ViT-L/14       | 一层MLP               | Vicuna-7B/13B(PEFT)   |     | LLaVA结构        |
| `Qwen-VL`         | 2023.08 | 阿里通义    | 448      | 9B     | OpenCLIP ViT-G/14   | Cross Attention     | Qwen-7B   |     | 只用了一层Cross Attention |
| `InternLM-XComposer-VL`| 2023.09 | 上海Al Lab | 224      | 7B     | EVA-CLIP ViT-g/14   | Q-Former            | InternLM-7B  |     | 支持图文混排         |
| `mPLUG-Owl`       | 2023.04 | 达摩院   | 224      | 7B     | CLIP ViT-L/14       | Perceiver Resampler | LLaMA-7B  |     | 改装自Flamingo    |
| `mPLUG-Owl V2`    | 2023.11 | 达摩院   | 448      | 7B     | CLIP ViT-L/14       | Perceiver Resampler | LLaMA-7B                             |     | 添加模态自适应的M      |
| `ShareGPT4V`      | 2023.11 | 上海Al Lab | 336      | 7B     | CLIP ViT-L/14       | 两层MLP               | Vicuna-7B-v1.5  |     | 使用GPT4V提供了-    |
| `Sphinx`          | 2023.11 | 上海Al Lab | 224      | 13B    | -ConvNext, DINO-v2, | 两个不同的Projector      | LLaMA-2-13B  |     | 将四个不同的encod    |
| `CogVLM-17B`      | 2023.11 | 智谱    | 224->496 | 17B    | EVA-CLIP ViT-E/14   | 两层Linear            | Vicuna-7B-v1.5 +Visual Expert Module |     | 视觉专家,文本和视      |
| `Ferret`          | 2023.11 | 添加 Spatial Aware | 336      | 7B/13B | CLIP ViT-L/14       | 一层Linear            | Vicuna-7B/13B-v1.3    |     |      |
| `MiniGPT-V2`      | 2023.11.7  | Meta AI, KAUST  | 448      | 7B     | EVA-CLIP ViT-G/14   | 一层Linear            | LLaMA2-chat 7B   |     |       |
| `Qwen-VL2`         | 2024.09 | 阿里通义    | 448      | 9B     |  ViT/14   | Cross-Modal Connection   | Qwen2-1.5B<br>Qwen2-7B <br>Qwen2-72B   |     | 1. ViT <br>2.全参 <br>3.LLM |


发展历程图解
- 最初集中在多模态的**内容理解**和**文本生成**: 
  - Flamingo,BLIP-2, Kosmos-1,LLaVA/LLaVA-1.5/LLaVA-1.6，MiniGPT-4，MultiModal-GPT，Video-Chat，VIdeo-LLaMA，IDEFICS，Fuyu-8B，Qwen-Audio
- 同时实现**多模态的输入和输出**工作: MM-LMM，探索特定模态的生成
  - 例如 Kosmos-2，Mini-GPT5，以及语音生成的 SpeechGPT
- 将 **LLM 和外部工具继承**进来，实现“any-to-any”的多模态理解和生成。
  - visual-chatgpt，ViperGPT，MM-React，HuggingGPT，AudioGPT
- 减少级联过程中传播误差的工作, 开发**任意模式**的多模态模型
  - NExT-GPT 和 CoDI-2，

![](https://pic3.zhimg.com/80/v2-83bd973cca2e49efa74d8972c7b97f82_1440w.webp)






### 多模态模块

**多模态大模型**(`MLLMs`)5个核心模块
- `Modality Encoder`：`模态编码器`，将不同**模态**输入数据（如图片、视频、音频、3D等），编码为可理解的表示（隐层向量）
  - `Visual Modality`: `ViT`, transformers 替换 cnn
    - 图片补丁 `image patch encoder`: 不用像素, 而是 用视野和步幅较大的卷积核提取**图片补丁**上的特征
    - 图片补丁位置嵌入: `image patch position embedding`, 查询表
- `Input Projector`: `输入映射`，将不同模态的向量表示映射到共享表示空间，和LLM语义对齐
- `LLM Backbone`: `大语言模型基座`，LLM基座模型，用于处理文本数据
- `Output Projector`: `输出映射`，将LLM生成的输出,映射回**原始模态**空间,和各模态对齐
- `Modality Decoder`: `模态解码器`, 或 `Modality Generator` **模态生成器** ，将各模态语义解码为对应的模态

注意
- 注重 Comprehension and text generation 的多模态模型，只需要**前3个**模块
- 预训练阶段，Modality Encoder、LLM Backbone、Modality Decoder 一般都会**冻结参数**，只优化 Input Projector 和 Output Projector（约占整体参数的2%），因而训练一个多模态模型的成本会小很多。
- SFT阶段，LLM一般也会参与，因而SFT阶段需要更多显存。




<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36\&quot; version=\&quot;24.7.12\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;VC8KsEmwTz_4FKU3JA4y\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;2069\&quot; dy=\&quot;785\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-24\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-540\&quot; y=\&quot;360\&quot; width=\&quot;400\&quot; height=\&quot;270\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-7\&quot; value=\&quot;多模态模型组件\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=20;strokeWidth=2;fontFamily=Verdana;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-214.56\&quot; y=\&quot;260\&quot; width=\&quot;160\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UnDAMuxRGoDYzSfqeH0n-51\&quot; value=\&quot;2024-9-16&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;text;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;strokeWidth=2;html=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;190\&quot; y=\&quot;545\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-8\&quot; value=\&quot;Input Projector&amp;lt;div&amp;gt;输入映射层&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#009900;shadow=1;fontStyle=1;fontSize=14;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-504.11\&quot; y=\&quot;420\&quot; width=\&quot;114.11\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-9\&quot; value=\&quot;Output Projector&amp;lt;div&amp;gt;输出映射层&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#009900;shadow=1;fontStyle=1;fontSize=14;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;95.89\&quot; y=\&quot;420\&quot; width=\&quot;114.11\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-10\&quot; value=\&quot;Modality Encoder&amp;lt;div&amp;gt;模态编码层&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#FF3399;shadow=1;fontStyle=1;fontSize=14;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-305.15000000000003\&quot; y=\&quot;420\&quot; width=\&quot;131.04\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-11\&quot; value=\&quot;Modality Decoder&amp;lt;div&amp;gt;模态解码层&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#FF3399;shadow=1;fontStyle=1;fontSize=14;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-109.71000000000002\&quot; y=\&quot;420\&quot; width=\&quot;131.04\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-12\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;YTmzy6fBNNcobJbAdKNS-8\&quot; target=\&quot;YTmzy6fBNNcobJbAdKNS-10\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-87.69999999999992\&quot; y=\&quot;713.01\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-294.11\&quot; y=\&quot;765\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-13\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;YTmzy6fBNNcobJbAdKNS-10\&quot; target=\&quot;YTmzy6fBNNcobJbAdKNS-11\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-380.11\&quot; y=\&quot;450\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-295.11\&quot; y=\&quot;450\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;YTmzy6fBNNcobJbAdKNS-11\&quot; target=\&quot;YTmzy6fBNNcobJbAdKNS-9\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-164.11\&quot; y=\&quot;450\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-100.11\&quot; y=\&quot;450\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-15\&quot; value=\&quot;&amp;lt;div&amp;gt;LLM Backbone&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;大语言模型基座&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#FF3399;shadow=1;fontStyle=1;fontSize=14;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-305.1500000000001\&quot; y=\&quot;560\&quot; width=\&quot;131.04\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-16\&quot; value=\&quot;&amp;lt;div&amp;gt;各模态转为隐向量&amp;lt;/div&amp;gt;视觉模型: ViT替换CNN\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-314.11\&quot; y=\&quot;390\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-18\&quot; value=\&quot;不同模态的语义向量与LLM对齐\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-530\&quot; y=\&quot;460\&quot; width=\&quot;177.05\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-19\&quot; value=\&quot;LLM语义与模态语义对齐\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;70\&quot; y=\&quot;460\&quot; width=\&quot;177.05\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-21\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;YTmzy6fBNNcobJbAdKNS-10\&quot; target=\&quot;YTmzy6fBNNcobJbAdKNS-15\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-164\&quot; y=\&quot;450\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-100\&quot; y=\&quot;450\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-22\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;YTmzy6fBNNcobJbAdKNS-15\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-230\&quot; y=\&quot;470\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-39.710000000000036\&quot; y=\&quot;460\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-23\&quot; value=\&quot;模态语义转为对应模态\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-109.71000000000001\&quot; y=\&quot;390\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-25\&quot; value=\&quot;侧重模态理解+文本生成的多模态模型\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-460\&quot; y=\&quot;630\&quot; width=\&quot;212.2\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-26\&quot; value=\&quot;注意&amp;lt;div&amp;gt;- 训练时, 中间3个（红框）参数冻结&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;- 只更新输入、输出映射层（绿框）, 参数量约2%&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;- SFT阶段, llm 也参数&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#FF3333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-120\&quot; y=\&quot;585\&quot; width=\&quot;270\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>





### 模型进化史

<div class="mermaid">
    flowchart TD
    %% 节点颜色
    classDef red fill:#f02;
    classDef green fill:#5CF77B;
    classDef blue fill:#6BE0F7;
    classDef orange fill:#F7CF6B;
    classDef grass fill:#C8D64B;
    %%节点关系定义
    S(多模态大模型)-->|2022-4-29,DeepMind,多模态多任务|F(Flamingo\n火烈鸟):::orange
    S-->|2020,Google| V(ViT):::orange
    T(Transformer)-->V
    S-->|2021-10-7,Junnan Li\nSalesforce Research\n跨模态注意力引入对比损失\n动量蒸馏| A(ALBEF):::blue
    F-->|2023-3-29,Christoph Schuhmann\n开源复制品,LMM框架,LLaMA| O(OpenFlamingo):::orange
    A-.->|2022-2-15,Junnan Li\nSalesforce Research\n统一理解和生成|B(BLIP):::green
    C-.->|对比|B
    B-->|2023-1-30,Junnan Li\nSalesforce Research|B2(BLIP-2):::green
    B2-->|2023-4-20,阿卜杜拉国王科技大学\nBLIP-2+LAVIS+Vicuna\n复现GPT-4多模态能力|M(MiniGPT-4):::grass
    S-->|2021-2-26,OpenAI|C(CLIP):::blue
    B-->|2023-4-17,威斯康星+微软+哥大\nCLIP+LLaMA\n复现GPT-4多模态能力|L(LLaVA):::grass
    C-->|pretrain|L
    O-->|2023-4-27,OpenMMLab\nLoRA微调| MG(MMGPT):::grass
</div>


## 多模态技术路线

【2024-7-30】

| 大方向 | 子方向 | 代表工作 |
| --- | --- | --- |
| 内容理解和文本生成<br>Comprehension and text generation | image-text understanding | BLIP-2, llaVA, MiniGPT-4, OpenFlamingo |
| 内容理解和文本生成<br>Comprehension and text generation | video-text understanding | VideoChat, Video-ChatGPT, LLaMA-VID
| 内容理解和文本生成<br>Comprehension and text generation | audio-text understanding | Qwen-Audio |
| 特定模态<br>specific modality outputs | image-text output | GILL, Kosmos-2, Emu, MiniGPT-4 |
| 特定模态<br>specific modality outputs | speech/audio-text output | speechGPT, AudioPaLM |
| 任意模态<br>any-to-any modality outputs |  amalgamate tools | VisualChatGPT, HuggingGPT, AudioGPT |
| 任意模态<br>any-to-any modality outputs | end-to-end | NExT-GPT, CoDi-2, ModaVerse |

【2024-5-30】[多模态模型的演进和四种主流架构类型](https://blog.csdn.net/robinfang2019/article/details/139322252)

多模态按照架构模式分为四类：A、B、C、D。
- A和B类型在模型内部，深度融合多模态输入，实现细粒度控制模态信息流动，但需要大量训练数据和计算资源；
- C和D类型在输入层，融合多模态输入
  - C类型具有**模块化**设计，可以容易地添加更多模态。
  - D类型使用标记化，可训练不同模态，但需要训练通用标记器。

按照不同架构模式，跟踪多模态发展里程碑：

### 多模态发展里程碑


多模态发展里程碑

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36\&quot; version=\&quot;24.7.14\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;VC8KsEmwTz_4FKU3JA4y\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;2069\&quot; dy=\&quot;785\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;2rrU_kqTqN86A4O8P-Nc-53\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#E6E6E6;strokeColor=#666666;dashed=1;dashPattern=1 1;opacity=50;fontColor=#333333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-510\&quot; y=\&quot;806.99\&quot; width=\&quot;190\&quot; height=\&quot;363.01\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-7\&quot; value=\&quot;多模态技术演进\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=20;strokeWidth=2;fontFamily=Verdana;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-60\&quot; y=\&quot;340\&quot; width=\&quot;160\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UnDAMuxRGoDYzSfqeH0n-51\&quot; value=\&quot;2024-7-16&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;text;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;strokeWidth=2;html=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-490\&quot; y=\&quot;1125\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2rrU_kqTqN86A4O8P-Nc-3\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-9\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-12\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;313.84999999999985\&quot; y=\&quot;773\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-1\&quot; value=\&quot;Transformers\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-247.29000000000002\&quot; y=\&quot;380\&quot; width=\&quot;104.83\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-2\&quot; value=\&quot;VL-T5\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-249.33999999999997\&quot; y=\&quot;620\&quot; width=\&quot;112.16\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-3\&quot; value=\&quot;Flamingo&amp;lt;div&amp;gt;火烈鸟&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-250\&quot; y=\&quot;730\&quot; width=\&quot;112.82\&quot; height=\&quot;33.01\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-7\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-13\&quot; target=\&quot;D7jkmO4b4NPNle1_V9Gg-3\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-37.08\&quot; y=\&quot;743\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-185.08\&quot; y=\&quot;603\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-12\&quot; value=\&quot;【A】标准交叉注意力\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#FF0000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-390\&quot; y=\&quot;760\&quot; width=\&quot;150\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-22\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-13\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-16\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-400\&quot; y=\&quot;880\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-3\&quot; value=\&quot;开源实现\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;D7jkmO4b4NPNle1_V9Gg-22\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0616\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-19\&quot; y=\&quot;-14\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-13\&quot; value=\&quot;Flamingo\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-449.11\&quot; y=\&quot;815\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-3\&quot; target=\&quot;D7jkmO4b4NPNle1_V9Gg-13\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;746.99\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;818.99\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-24\&quot; value=\&quot;2017年\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#999999;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-580\&quot; y=\&quot;370\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-1\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#CCCCCC;\&quot; parent=\&quot;1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-520\&quot; y=\&quot;360\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-520\&quot; y=\&quot;1110\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-2\&quot; value=\&quot;2020年\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#999999;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-580\&quot; y=\&quot;510\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-3\&quot; value=\&quot;2021年\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#999999;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-580\&quot; y=\&quot;570\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-4\&quot; value=\&quot;2018年\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#999999;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-580\&quot; y=\&quot;410\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-5\&quot; value=\&quot;2019年\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#999999;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-580\&quot; y=\&quot;460\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-6\&quot; value=\&quot;2022年\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#999999;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-580\&quot; y=\&quot;690\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-7\&quot; value=\&quot;2023年\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#999999;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-580\&quot; y=\&quot;810\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-8\&quot; value=\&quot;2024年\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#999999;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-580\&quot; y=\&quot;940\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-10\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-1\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-9\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-195.06\&quot; y=\&quot;450\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-195.06\&quot; y=\&quot;610\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-11\&quot; value=\&quot;首次应用于视觉领域\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;rftaN9jHHxlRs_W2yEbK-10\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0773\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-4\&quot; y=\&quot;32\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-9\&quot; value=\&quot;ViT\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-249.33999999999997\&quot; y=\&quot;513\&quot; width=\&quot;109.35\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-12\&quot; value=\&quot;CLIP\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-249.57\&quot; y=\&quot;573\&quot; width=\&quot;109.35\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-13\&quot; value=\&quot;S4\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-249.33999999999997\&quot; y=\&quot;673\&quot; width=\&quot;112.16\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-14\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-2\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-13\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-185.08\&quot; y=\&quot;573\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-185.08\&quot; y=\&quot;643\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-15\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-12\&quot; target=\&quot;D7jkmO4b4NPNle1_V9Gg-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-185.08\&quot; y=\&quot;573\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-52.08\&quot; y=\&quot;593\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-16\&quot; value=\&quot;OpenFlamingo\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-409.11\&quot; y=\&quot;910\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-17\&quot; value=\&quot;Dolphins\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-413\&quot; y=\&quot;1041.99\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-18\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-13\&quot; target=\&quot;YTmzy6fBNNcobJbAdKNS-5\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-389\&quot; y=\&quot;886.99\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-389\&quot; y=\&quot;918.99\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-19\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;dashed=1;dashPattern=1 1;opacity=50;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-307.82\&quot; y=\&quot;810\&quot; width=\&quot;140\&quot; height=\&quot;370\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-20\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-21\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-22\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-21\&quot; value=\&quot;LLaMA-Adapter\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-294.96000000000004\&quot; y=\&quot;846.99\&quot; width=\&quot;116.05\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-22\&quot; value=\&quot;LLaMA-Adapter-V2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-304.96000000000004\&quot; y=\&quot;908.98\&quot; width=\&quot;136.05\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-23\&quot; value=\&quot;CogAgent\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-286.05\&quot; y=\&quot;976.99\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-24\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-22\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-23\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-226.82\&quot; y=\&quot;890\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-226.82\&quot; y=\&quot;922\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-25\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;dashed=1;dashPattern=1 1;opacity=50;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-150\&quot; y=\&quot;815\&quot; width=\&quot;210\&quot; height=\&quot;365\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-26\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-27\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-28\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-27\&quot; value=\&quot;BLIP2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-109.10999999999999\&quot; y=\&quot;855\&quot; width=\&quot;58.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-28\&quot; value=\&quot;InstructBLIP\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-128.23000000000002\&quot; y=\&quot;916.99\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-29\&quot; value=\&quot;Next-GPT\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-128.23000000000002\&quot; y=\&quot;990\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-30\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-28\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-29\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-69\&quot; y=\&quot;895\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-69\&quot; y=\&quot;927\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-31\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;dashed=1;dashPattern=1 1;opacity=50;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;109.99999999999999\&quot; y=\&quot;815\&quot; width=\&quot;140\&quot; height=\&quot;280\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-32\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-33\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-34\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-33\&quot; value=\&quot;CM3Leon\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;142.54999999999995\&quot; y=\&quot;923.01\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-34\&quot; value=\&quot;Unified-IO\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;142.54999999999995\&quot; y=\&quot;985\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-35\&quot; value=\&quot;Unified-IO-2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;142.54999999999995\&quot; y=\&quot;1050\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-36\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-34\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-35\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;201.77999999999997\&quot; y=\&quot;963.01\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;201.77999999999997\&quot; y=\&quot;995.01\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-37\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.556;entryY=-0.007;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-3\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-19\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;777\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-389\&quot; y=\&quot;857\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-38\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-3\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-25\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;777\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-227\&quot; y=\&quot;860\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-39\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-3\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-31\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;777\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-70\&quot; y=\&quot;825\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-40\&quot; value=\&quot;mPLUG-Owl2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-286.05\&quot; y=\&quot;1011.99\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-41\&quot; value=\&quot;InternVL\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-286.93\&quot; y=\&quot;1041.99\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-42\&quot; value=\&quot;MM-Interleaved\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-286.04999999999995\&quot; y=\&quot;1095\&quot; width=\&quot;104.96\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-43\&quot; value=\&quot;CogCoM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-286.93\&quot; y=\&quot;1130\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-44\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.581;exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-41\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-42\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-227\&quot; y=\&quot;949\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-227\&quot; y=\&quot;987\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-45\&quot; value=\&quot;LLaVA\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-25\&quot; y=\&quot;845\&quot; width=\&quot;60.88\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-46\&quot; value=\&quot;MiniGPT-4\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-40\&quot; y=\&quot;878.98\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-47\&quot; value=\&quot;QWen-VL\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-48.669999999999995\&quot; y=\&quot;1011.99\&quot; width=\&quot;78.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-48\&quot; value=\&quot;CoDI-2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-128.23000000000002\&quot; y=\&quot;1056.99\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-49\&quot; value=\&quot;ModaVerse\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-128.23000000000002\&quot; y=\&quot;1116.99\&quot; width=\&quot;98.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-50\&quot; value=\&quot;MM1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-19.11\&quot; y=\&quot;1116.99\&quot; width=\&quot;49.11\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-51\&quot; value=\&quot;GILL\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-24.99\&quot; y=\&quot;916.99\&quot; width=\&quot;34.99\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-52\&quot; value=\&quot;Embodied-GPT\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-54.56\&quot; y=\&quot;946.99\&quot; width=\&quot;109.11\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-53\&quot; value=\&quot;4M\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;245.89\&quot; y=\&quot;985\&quot; width=\&quot;36.66\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-54\&quot; value=\&quot;TEAL\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;292.55\&quot; y=\&quot;985\&quot; width=\&quot;36.66\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-56\&quot; value=\&quot;【B】定制层\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#FF0000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-247.29000000000002\&quot; y=\&quot;770\&quot; width=\&quot;100\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-59\&quot; value=\&quot;【C】非token早期融合\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#FF0000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-130.44\&quot; y=\&quot;780\&quot; width=\&quot;160\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;rftaN9jHHxlRs_W2yEbK-60\&quot; value=\&quot;【D】分词器早期融合\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#FF0000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;54.550000000000004\&quot; y=\&quot;770\&quot; width=\&quot;150\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-1\&quot; value=\&quot;优点：多模态信息精细控制&amp;lt;div&amp;gt;缺点：模型复杂，计算开销大，扩展难&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#3333FF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-500\&quot; y=\&quot;775\&quot; width=\&quot;240\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-2\&quot; value=\&quot;Otter\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-400\&quot; y=\&quot;970\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-4\&quot; value=\&quot;MultiModal-GPT\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-424.11\&quot; y=\&quot;1006.99\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-5\&quot; value=\&quot;IDEFICS\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-493\&quot; y=\&quot;908.98\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-6\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-16\&quot; target=\&quot;YTmzy6fBNNcobJbAdKNS-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-389\&quot; y=\&quot;949\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-451\&quot; y=\&quot;987\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;YTmzy6fBNNcobJbAdKNS-7\&quot; value=\&quot;PaLi-X\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-504.11\&quot; y=\&quot;970\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z5jKJojGF6zH0VbhjXEN-1\&quot; value=\&quot;2020年,谷歌将transformer用于图像任务, 使用了encoder部分；&amp;lt;div&amp;gt;模型简单效果好,可扩展&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-137.18\&quot; y=\&quot;500\&quot; width=\&quot;210\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z5jKJojGF6zH0VbhjXEN-2\&quot; value=\&quot;2021-2-26,OpenAI,&amp;amp;nbsp;文本和图像混合预训练,零样本迁移学习,4亿文本图像对&amp;lt;div&amp;gt;文本编码器+图像编码器，映射到矩阵&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-125\&quot; y=\&quot;563\&quot; width=\&quot;215\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z5jKJojGF6zH0VbhjXEN-3\&quot; value=\&quot;2022-4-29,DeepMind&amp;lt;div&amp;gt;多模态多任务框架&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-330\&quot; y=\&quot;706.51\&quot; width=\&quot;120.44\&quot; height=\&quot;23.49\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z5jKJojGF6zH0VbhjXEN-4\&quot; value=\&quot;2022-2-15,Junnan Li, Salesforce Research&amp;lt;br&amp;gt;统一理解和生成；\&quot; style=\&quot;text;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-40\&quot; y=\&quot;680\&quot; width=\&quot;240\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z5jKJojGF6zH0VbhjXEN-5\&quot; value=\&quot;BLIP\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontStyle=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-108.22999999999999\&quot; y=\&quot;696.51\&quot; width=\&quot;58.23\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z5jKJojGF6zH0VbhjXEN-6\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-12\&quot; target=\&quot;z5jKJojGF6zH0VbhjXEN-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-185\&quot; y=\&quot;613\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-183\&quot; y=\&quot;630\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z5jKJojGF6zH0VbhjXEN-7\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;z5jKJojGF6zH0VbhjXEN-5\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-27\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-130\&quot; y=\&quot;598\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-35\&quot; y=\&quot;707\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z5jKJojGF6zH0VbhjXEN-8\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;rftaN9jHHxlRs_W2yEbK-27\&quot; target=\&quot;rftaN9jHHxlRs_W2yEbK-46\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-70\&quot; y=\&quot;895\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-69\&quot; y=\&quot;927\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z5jKJojGF6zH0VbhjXEN-9\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;z5jKJojGF6zH0VbhjXEN-3\&quot; target=\&quot;z5jKJojGF6zH0VbhjXEN-3\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z5jKJojGF6zH0VbhjXEN-10\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;&amp;quot;&amp;gt;轻量级 Q-former弥补模态间差距&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-153.68\&quot; y=\&quot;820\&quot; width=\&quot;174.56\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

### 1、A型多模态模型

A类模型：基于**标准交叉注意力**的深度融合（Standard Cross-Attention based Deep Fusion, SCDF）。

#### 1.1 特点

特点
- 内部层深度融合：该架构使用标准的Transformer模型，并在模型的内部层添加了标准的交叉注意力层，以实现输入多模态信息的深度融合。
- 不同模态输入编码：每个输入模态（图像、视频、音频等）都通过对应的编码器进行编码，然后将编码后的多模态特征输入到模型内部层。
- 跨模态特征融合：模型内部层通过标准的交叉注意力层对不同模态的特征进行融合，使模型能够同时处理多个模态的信息。
- 多模态解码器：通常采用只包含解码器的Transformer模型作为多模态解码器，用于生成多模态输出。
- 自回归生成：多模态解码器可以实现多模态输入的自回归生成，即生成多模态输出。
- 训练数据需求：需要大量多模态训练数据，计算资源需求较高。
- 添加模态困难：在模型内部层添加更多模态比较困难。

#### 1.2 优势与不足

A类型多模态模型
- 优势：多模态信息精细控制
- 不足：计算资源需求较高，模型复杂，添加模态困难。

#### 1.3 典型模型开源代码

- `Flamingo` 
  - 官方代码 [flamingo](https://github.com/flamingo-vl/flamingo)
  - 基于Transformer 多模态模型，可处理图像和文本数据。
- `OpenFlamingo`
  - 官方代码：OpenAI [flamingo](https://github.com/openai/flamingo)
  - 开源Flamingo模型实现，提供了模型的复现。
- `Otter`
  - 官方代码： 微软 [otter-generative](https://github.com/microsoft/otter-generative)
  - 基于OpenFlamingo的多模态模型，可处理图像和文本数据。
- `MultiModal-GPT`
  - 官方代码： [multimodal-gpt](https://github.com/tuanvu2203/multimodal-gpt)
  - 基于OpenFlamingo的多模态模型，可以处理图像和文本数据。
- `PaLI-X`
  - 官方代码： 微软 [PALI-X](https://github.com/microsoft/PALI-X)
  - 多模态模型，可以处理图像、文本和视频数据。
- `IDEFICS`
  - 官方代码： 谷歌 [IDEFICS](https://github.com/google/IDEFICS)
  - 开源的Flamingo模型的实现，提供了模型的复现。
- `Dolphins`
  - 官方代码： 微软 [Dolphins](https://github.com/microsoft/Dolphins)
  - 基于OpenFlamingo的多模态模型，用于自动驾驶场景。

### 2、B型多模态模型

B类模型
- 基于定制层的**深度融合**（Custom Layer based Deep Fusion, CLDF），在多模态学习中以其定制化的层和深度融合策略而著称。

#### 2.1 特点

- 使用自定义层进行模态融合：与A类型模型不同，B类型模型不使用标准的Transformer跨注意力层来融合多模态输入，而是采用自定义设计的层来进行模态间的融合。这些自定义层可以是自注意力层、卷积层、线性层等。
- 跨注意力层或自定义层的深度融合：多模态输入通过模态编码器进行处理，然后通过自定义层或跨注意力层与语言模型进行深度融合。这种深度融合有助于模态间的信息交互和共享。
- 解码器端多模态模型为主：通常包含一个预训练的语言模型，用于作为解码器。模态编码器处理不同模态的数据，然后通过自定义层或跨注意力层与解码器层进行融合，从而生成多模态的输出。
- 模态交互和共享机制：通过自定义层或跨注意力层实现模态间的交互和共享。这种机制有助于模型更好地理解多模态数据之间的关联性。
- 支持更多模态类型：自定义层设计可以支持更多类型的模态，包括图像、文本、音频、视频等。通过灵活的自定义层设计，模型可以适应不同的多模态任务需求。
- 训练数据和计算资源需求：训练需要大量的多模态数据和计算资源。自定义层的设计需要大量的实验和调参来优化模型性能。
- 可扩展性：自定义层设计具有一定的可扩展性，可以方便地添加新的模态类型。然而，模型的扩展性仍然有限，需要仔细设计自定义层以支持新的模态类型。

#### 2.2 优势与不足

优势
- 细粒度模态控制：模型可以通过自适应注意力层或自适应模块更好地控制不同模态信息在模型中的流动，实现细粒度的模态融合。
- 灵活的架构设计：自适应注意力层或自适应模块可以根据不同的任务需求进行定制设计，提供更多的灵活性。
- 降低计算复杂度：相比Type-A，B类型模型不需对LLM内部层进行大规模的修改，计算复杂度较低。
- 可扩展性：模型支持增加新的模态，只需要在输入层添加新的自适应模块或注意力层即可。

不足
- 计算资源需求：虽然B类型模型计算复杂度较低，但相比C类型，训练和推理仍然需要较多的计算资源。
- 训练难度：自适应注意力层或自适应模块的设计和训练需要较深的神经网络知识，对研究者有一定挑战。
- 模态融合控制：虽然提供了细粒度的模态控制，但过多控制可能导致模态信息的过度融合或不融合，需要仔细设计。
- 参数数量：添加自适应注意力层或自适应模块会增加模型参数数量，增加计算和存储需求。
- 性能：相比C类型，B类型模型的性能可能略低，因为模型设计更为复杂，需要更多训练数据和计算资源。

#### 2.3 典型B类模型开源代码

- `LLaMA-Adapter`
  - 官方代码：[llama-adapter](https://github.com/microsoft/llama-adapter)
  - 采用自适应注意力层进行模态融合，适用于文本和图像输入，并输出文本。
- `LLaMA-Adapter-V2`
  - 官方代码：[paper](https://arxiv.org/abs/2304.15010)
  - 在LLaMA-Adapter基础上增加了视觉指令模型，使用自适应注意力层进行模态融合，适用于文本和图像输入，并输出文本。
- `CogVLM`
  - 官方代码：微软 [cogvlm](https://github.com/microsoft/cogvlm)
  - LLM注意力层之前添加了自适应注意力层，用于学习图像特征，适用于图像和文本输入，并输出文本。
- `mPLUG-Owl2`
  - 官方代码：微软 [mplug-owl](https://github.com/microsoft/mplug-owl)
  - 在LLM的注意力层之前添加了自适应注意力层，称为“模式适应模块”，适用于图像和文本输入，并输出文本。
- `CogAgent`
  - 官方代码：[cogagent](https://github.com/microsoft/cogagent)
  - 在LLM的注意力层之前添加了自适应注意力层，用于学习图像特征，适用于图像和文本输入，并输出文本。
- `InternVL`
  - 官方代码：微软 [internvl](https://github.com/microsoft/internvl)
  - 包含视觉编码器、重采样器、LLM、特征同步器等，适用于图像和文本输入，并输出文本。
- `MM-Interleaved`
  - 官方代码：微软 [mm-interleaved](https://github.com/microsoft/mm-interleaved)
  - 包含视觉编码器、重采样器、LLM、特征同步器等，适用于图像和文本输入，并输出图像和文本。
- `CogCoM`
  - 官方代码：微软 [cogcom](https://github.com/microsoft/cogcom)
  - 包含视觉编码器、重采样器、LLM、特征同步器等，适用于图像和文本输入，并输出图像和文本。
- `InternLM-XComposer2`
  - 官方代码：微软 [internlm-xcomposer](https://github.com/microsoft/internlm-xcomposer)
  - 添加了LoRA权重来学习图像模态，适用于图像和文本输入，并输出文本。
- `MoE-LLaVA`
  - 官方代码：[moe-llava](https://github.com/microsoft/moe-llava)
  - 在LLaVA的基础上修改了每个解码器层的FFN层，创建了混合专家层，适用于图像和文本输入，并输出文本。

### 3、C型多模态模型

C类模型
- 非标记化早期融合（NTEF）架构，在多模态学习领域中以其模块化和灵活性而著称。

#### 3.1 特点

- 早期融合：与深度融合模型（A类和B类）不同，C类模型在模型的输入阶段就实现了模态的融合，而不是在模型的内部层中。
- 非标记化输入：直接将不同模态的输入提供给模型，而不需要将输入转换为离散的标记（tokens）。这意味着模型在处理输入时不需要进行复杂的分词处理。
- 模块化设计：具有模块化架构，将不同模态的编码器输出与语言模型（LLM）或变换器模型直接连接起来，无需在模型内部层进行模态融合。可以轻松替换或更新模型的不同部分，如编码器或连接层，而不影响整个系统的其他部分。
- 简化的集成：由于其模块化的特性，可以更容易地集成新的模态或更新现有模态的处理方式。
- 端到端可训练：尽管在输入阶段融合模态，但它们仍然可以端到端地进行训练。
- 资源效率：与其他类型的多模态模型相比，C类模型通常需要较少的训练数据和计算资源。
- 连接器/适配器的使用：使用不同类型的连接器或适配器来链接模态编码器和语言模型（LLM）。这些连接器可以是线性层、多层感知器（MLP）、Q-former、注意力池化层、卷积层、Perceiver resampler或Q-former的变体。
- 训练策略：通常采用预训练、指令调整和对齐调整的三阶段训练策略。预训练阶段主要目的是对齐不同模态并学习多模态世界知识；指令调整用于提高模型对用户指令的理解能力；对齐调整则进一步优化模型以适应人类交互。
- 易于扩展：由于其设计，可以较容易地扩展以包含更多的模态，这使得它们在构建任何到任何的多模态模型时非常有用。

#### 3.2 优势与不足

优势
- 简单高效：不需要在模型内部层进行模态融合，因此其设计较为简单，易于实现和训练。此外，模型的模块化设计也使得其在计算资源需求上相对较低。
- 多模态输入输出：可以接受多种模态（如图像、文本、音频等）作为输入，并生成相应的多模态输出。模型的输入端可以根据需要连接不同的模态编码器，例如图像编码器、文本编码器等。
- 适应性强：模块化设计使得其具有较强的适应性，可以轻松地集成新的模态或修改现有的模态编码器，以满足不同任务的需求。
- 通用性强：通用性较强，可以应用于多种多模态任务，如多模态文本生成、多模态对话、多模态理解等。

不足
- 模态信息处理：C类型模型在模态信息的处理上相对简单，可能无法充分挖掘不同模态之间的潜在联系。
- 性能限制：C类型模型的性能可能略低于Type-A和Type-B，因为模型的设计更为复杂，需要更多训练数据和计算资源。
- 模态编码器设计：C类型模型的性能在很大程度上取决于模态编码器的性能，因此需要设计高效的模态编码器。
- 模态融合控制：C类型模型在模态融合的控制上较为困难，需要仔细设计连接模块，以确保不同模态信息的有效融合。

#### 3.3 典型C类模型开源代码

- `BLIP-2`
  - 官方代码: BLIP-2 GitHub
  - 使用一个名为Q-Former的模块来同时处理图像和文本输入。
- `MiniGPT-4`
  - 官方代码: MiniGPT-4 GitHub
  - 一个大规模的、可微调的多模态语言模型，它通过设计一个连接模块来连接图像编码器输出和语言模型。
- `LLaVA`
  - 官方代码: LLaVA GitHub
  - 一个基于指令微调的、可以处理多模态输入和输出的语言模型。它使用一个线性层来连接图像编码器输出和语言模型。

### 4、D型多模态模型

D类模型
- Tokenized Early Fusion (TEF)，其架构特点主要围绕使用分词器（tokenizer）来处理和融合多模态输入。

#### 4.1 特点

- 输入分词化：使用通用分词器或模态特定的分词器将多模态输入（如图像、视频、音频）转换为离散的标记（tokens）。
- 早期融合：与C类模型类似，D类模型也在输入阶段实现模态融合，但不同之处在于D类模型通过分词化实现这一融合。
- 统一的Transformer架构：通常采用预训练的大型语言模型（LLM）或编码器-解码器（encoder-decoder）风格的Transformer模型来处理分词化后的输入，并生成多模态输出。
- 端到端可训练：D类模型是端到端可训练的，这意味着从输入分词化到输出生成的整个过程可以在一个统一的框架内进行训练。
- 自动回归目标：由于输入和输出都被分词化，可以使用标准的自动回归目标函数来训练模型，这简化了训练过程。
- 处理多种模态：用于处理包括文本在内的多种模态，使其能够生成图像、音频和不同模态的tokens。
- 灵活性和扩展性：通过分词化，可以相对容易地适应新的模态，尽管为新模态训练或调整分词器可能是一项挑战。
- 大规模训练数据需求：通常需要大量的训练数据来训练分词器和主Transformer模型，这可能导致计算资源的大量需求。
- 可训练参数数量大：由于模型需要学习将不同模态的输入映射到统一的标记空间，D类模型往往具有大量的可训练参数。
- 适用于任何到任何的多模态任务：D类模型由于其设计，非常适合构建能够处理任何输入模态到任何输出模态的多模态模型。

#### 4.2 优势与不足

优势
- 标准化训练目标：由于模态都被标记化，模型可以使用标准的自回归目标函数进行训练，这简化了训练过程。
- 模态扩展性：新的模态可以通过训练一个新的标记化器来添加到模型中，这种灵活性使得模型能够扩展到新的模态。
- 模态通用性：标记化的模态表示可以用于多种下游任务，包括文本生成、图像生成、文本到图像的生成等。

不足
- 标记化复杂性：训练一个通用的标记化器或模态特定的标记化器可能是一个挑战。
- 计算资源需求：标记化和去标记化过程增加了计算复杂性，可能需要额外的计算资源。
- 模态信息的损失：标记化可能会丢失一些模态的原始信息，这可能导致模型性能的下降。
- 模态独立性：标记化可能导致模型在学习模态间交互时遇到困难，因为标记化表示可能掩盖了模态间的依赖关系。

#### 4.3 典型D类模型开源代码

- `Unified-IO`
  - 官方代码: Unified-IO GitHub
  - 一个多模态预训练模型，它使用VQ-GAN风格的标记化器来处理不同模态的输入，并使用投影层将非文本模态的输出嵌入映射到文本模态的词汇空间。
- `Unified-IO-2`
  - 官方代码: Unified-IO-2 GitHub
  - Unified-IO的升级版，它包含了更多的模态和更复杂的预训练任务。
- `4M`
  - 官方代码: 4M GitHub
  - 一个可以处理文本、RGB图像、深度、法线和语义分割映射等多模态输入的模型。它使用多模态混合去噪器（Multimodal Mixture of Denoisers）作为预训练目标。


## 典型模型


### 传统模型

前 Transformer时代：目标检测+预训练（Faster R-CNN + BERT）

Transformer多模态模型
- `Transformer`(2017): Attention Is All You Need.
- `ViT` (2020): 将transformer用于图像任务, An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale Transformer.
- `CLIP` (2021): 文本和图像混合预训练
  - Learning Transferable Visual Models From Natuural Language Supervision.
- `KOSMOS-1`(2023): 多模态大规模语言模型
  - Language Is Not All You Need: AligningPerception with Language Models.


多模态大模型：
- MiniGPT-4：沙特阿拉伯阿卜杜拉国王科技大学的研究团队开源。
- LLaVA：由威斯康星大学麦迪逊分校，微软研究院和哥伦比亚大学共同出品。
- VisualGLM-6B：开源的，支持图像、中文和英文的多模态对话语言模型，语言模型基于 ChatGLM-6B，具有 62 亿参数；图像部分通过训练 BLIP2-Qformer 构建起视觉模型与语言模型的桥梁，整体模型共78亿参数。

#### ViLBERT

ViLBERT的思路是从该模型在BERT模型的基础上，开创性的将**视觉特**征和**文本**特征引入单独的处理模块，并使用与单独处理结构相同的结构，以交换部分网络权重的方式结合两个模态的特征信息，最后得出两种不同数据的各自的特征编码。同时引用了能够包括两个模态的预训练任务：MLM、MRM、MRC、ITM

#### UNITER

UNITER的思路是通过使用**单流**结构，直接将视觉特征和文本特征融合处理，最后得到一个同时包含视觉语义和文本语义的特征编码。
- 该算法结合了大量的数据集和充足的预训练任务（包括：作者主要设计了4种预训练任务去获得模型的权重参数：基于图像的MRM、基于文本的MLM、图像文本匹配ITM、文本对齐WRA），最终在多个评测任务数据集上获得了当时的SOTA。

### 新模型

- 【2023-7-27】[Shikra: Unleashing Multimodal LLM’s Referential Dialogue Magic](https://arxiv.org/pdf/2306.15195.pdf)
- 【2023-9-25】[多模态大模型最全综述来了！7位微软研究员大力合作，成文119页](https://www.toutiao.com/article/7282646391107715620)


现象：
>多模态基础模型已经从**专用**走向**通用**。

#### 综述

五个具体研究主题：[多模态大模型最全综述来了！7位微软研究员大力合作，成文119页](https://www.toutiao.com/article/7282646391107715620)
- 视觉理解: 根据监督信号的不同，分类：**标签**监督、**语言**监督（以CLIP为代表）和只有**图像**的自监督。
  - 图像监督：监督信号是从图像本身中挖掘出来的，流行的方法包括对比学习、非对比学习和masked image建模
  - ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/95b27b56c3764e15995dad6abe37057f~tplv-tt-origin-asy2:5aS05p2hQOmHj-WtkOS9jQ==.image?_iz=58558&from=article.pc_detail&x-expires=1696245058&x-signature=qhKjbL1mN6rd88II0W8%2BpLSkiUI%3D)
  - ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/ba3fb9cf423c40e38fd2f27eab70dc15~tplv-tt-origin-asy2:5aS05p2hQOmHj-WtkOS9jQ==.image?_iz=58558&from=article.pc_detail&x-expires=1696245058&x-signature=UM3NCg0NpHEJtHmU73hwHTyh2t0%3D)
- 视觉生成： 空间可控生成、基于文本再编辑、更好地遵循文本提示和生成概念定制（concept customization）四个方面
- 统一视觉模型
- LLM加持的多模态大模型
- 多模态agent

【2024-1-25】26种多模态大语言模型（MM-LLMs）进行了全面的研究和分析。
- [MM-LLMs: Recent Advances in MultiModal Large Language Models](https://arxiv.org/pdf/2401.13601.pdf)
1. 模型架构和训练流程：如何结合了传统大型语言模型（LLMs）的能力，并支持多模态输入和输出。
2. 模型概览：
  - • 研究涵盖了26种不同的 MM-LLMs，每个模型都有其独特的设计和功能特点。
  - • 这些模型被分为不同的类别，根据它们的架构和功能进行了分类。
3. 性能评估：对这些模型在主流基准测试上的性能进行了回顾，分析了它们在不同任务上的表现。
4. 训练策略：总结了提高 MM-LLMs 性能的关键训练策略，包括数据处理和模型优化等。
5. 研究方向和资源：讨论了 MM-LLMs 的未来研究方向，并提供了实时跟踪这些模型最新发展的资源。

![](https://p3-sign.toutiaoimg.com/tos-cn-i-ezhpy3drpa/7fdc25991e1243b3882f37f6f1d9d15c~tplv-obj:749:500.image)

#### ViT

将 transformer 引入到 CV 领域
- 1、将图片**patch化**，解决 Transformer 不能应用于图像领域问题；
- 2、patch embedding 提取图像特征高效；
- 3、基于ViT模型衍生了视频Transformer相关模型。

[ViT（Vision Transformer）解析](https://zhuanlan.zhihu.com/p/445122996)

2020年，Google提出`ViT`，将Transformer应用在图像分类的模型
- transformer应用在视觉任务论文, 非首次，但模型“简单”且效果好，可扩展性强（scalable，模型越大效果越好），成为了transformer在CV领域应用的**里程碑**著作，也引爆了后续相关研究

ViT 论文中最核心结论
- 当拥有**足够多**的数据进行预训练时，`ViT` 表现就会超过`CNN`，突破transformer缺少归纳偏置的限制，可在下游任务中获得较好的迁移效果
- 当训练数据集**不够大**的时候，`ViT` 表现通常比同等大小的`ResNets`要差一些，因为Transformer和CNN相比缺少归纳偏置（inductive bias），即一种先验知识，提前做好的假设。

CNN具有两种归纳偏置
- 一种是**局部性**（locality/two-dimensional neighborhood structure），即图片上相邻的区域具有相似的特征；
- 一种是**平移不变形**（translation equivariance）

当CNN具有以上两种归纳偏置，就有了很多先验信息，需要相对少的数据就可以学习一个比较好的模型

`ViT`只使用了Transformer的encoder

`ViT` 将输入图片分为多个`patch`（16x16），再将每个patch投影为固定长度的向量送入Transformer，后续encoder的操作和原始Transformer中完全相同。
- 但是因为对图片分类，因此在输入序列中加入一个特殊的token，该token对应的输出即为最后的类别预测

![](https://pic4.zhimg.com/v2-5afd38bd10b279f3a572b13cda399233_b.jpg)


#### ALBEF

salesforce
- 论文：[Align before Fuse: Vision and Language Representation Learning with Momentum Distillation](​​​​​​https://arxiv.org/abs/2107.07651)
- 代码：[ALBEF](https://github.com/salesforce/ALBEF)

解决问题：
- 1）没有对齐视觉的 tokens 和 文字的 tokens, 因此给 多模编码器进行图文交互学习时带来挑战
- 2）训练多模模型，利用到了互联网上爬取的数据，这些数据中往往存在大量噪声，传统的图文特征融合训练模式（如 MLM, masked language modeling） 可能过拟合到噪声文本上，从而影响模型的泛化性能。

解决方案：
- 1） 通过跨模态 attention 的方式引入**对比损失**，在图文特征融合前对齐图像和文本表征，相对与大多数传统方案来说，不需要在高清图片上进行框级别的标注。
- 2）提出一种 **动量蒸馏** （momentum distillation） 的方案，即通过自训练(self-training)的方式从动量模型提供的伪标签中进行学习。

在训练过程中，通过参数移动平均的方式更新动量模型，并利用动量模型生成伪标签(pseudo-targets) 作为额外的监督信息。利用动量蒸馏的方式，模型将不在惩罚模型合理的输出，即使这个输出与网络标签不一致，提升从网络噪声数据中学习的能力。

结果：
- 1）在图文检索任务中，本方案优于在大规模数据集中预训练的方案（CLIP & ALIGN）
- 2) 在 VQA 和 NLVR 任务中，本方案相对 SOTA 算法（VILIA）分别获得了 2.37% 和 3.84% 的指标提升，而且获得了更快的推理速度。

#### Flamingo 火烈鸟（DeepMind）

【2022-4-29】Flamingo在few-shot和zero-shot上有很好的泛化性能，甚至能击败few-shot+fine-tune的SOTA，进一步证明了 Prompt tuning机制+**多模态多任务**+大规模预训练 三者有比较好的相性。 
- 论文：[Flamingo: a Visual Language Model for Few-Shot Learning](https://arxiv.org/abs/2204.14198)
- 代码：[flamingo-pytorch](https://github.com/lucidrains/flamingo-pytorch)

Flamingo [架构](https://www.163.com/dy/article/H64NEPHS0511AQHO.html)
- ![](https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.ws.126.net%2F2022%2F0429%2Fb5aef532j00rb3b11002uc000u000lim.jpg&thumbnail=660x2147483647&quality=80&type=jpg)

Flamingo 开箱即用的多模式对话，用 OpenAI 的 DALL·E 2 生成的「汤怪物」图像，在关于这张图像的不同问答中，Flamingo 都能准确地回答出来。
- 例如问题：这张图片中有什么？
- Flamingo 回答：一碗汤，一张怪物脸在上面。

Flamingo 可以快速适应各种图像和视频理解任务，只需简单地提示它几个例子
- ![](https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.ws.126.net%2F2022%2F0429%2F7628224cj00rb3b1400l6c000u000qcm.jpg&thumbnail=660x2147483647&quality=80&type=jpg)

具有丰富的视觉对话功能
- ![](https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.ws.126.net%2F2022%2F0429%2F87e8385ej00rb3b1400lsc000u000tem.jpg&thumbnail=660x2147483647&quality=80&type=jpg)

#### OpenFlamingo

【2023-3-29】[多模态大语言模型OpenFlamingo开源了](https://zhuanlan.zhihu.com/p/617864689)
- Christoph Schuhmann团队宣布开源了OpenFlamingo，这是DeepMind Flamingo模型的开源复制品。OpenFlamingo是一个框架，可实现大型多模态模型（LMM）的训练和评估

OpenFlamingo 模型是 DeepMind 的 `Flamingo` 模型**开源复现**版本，采用了较大的多模态数据集 MMC4 和 LAION 2B 进行训练，其视觉部分采用了 `CLIP` vision encoder 构成，而语言部分采用了 `LLaMA` 模型
- ![](https://pic1.zhimg.com/80/v2-8aa869bad80fa827dff7c6743720183c_1440w.webp)

OpenFlamingo 是一个框架，其实可以换不同的视觉和语言模型基座。
- OpenFlamingo 发布了 9B 的权重，其实已经具备了多模态问答能力。

多模态大语言模型 `BLIP-2` 和 `FROMAGe` 展现出惊人的读图能力和理解力，并具有问答能力
- ![BLIP-2模型效果](https://pic4.zhimg.com/80/v2-97d1fc2122a5faf1bdaa6eb3f8e30ce3_1440w.webp)

OpenFlamingo项目继续也在这些领域进行探索，并致力于为开发者们提供完整的开发框架入流程，持续共同为视觉语言模型多模态机器学习做出贡献。

多模态大语言模型OpenFlamingo满足大部分基础玩家的需求：
- 首先，基于Python框架项目，可用于训练Flamingo风格的大语言模型，模型框架基于基于Lucidrains的flamingo实现，并依托David Hansmair的flamingo-mini存储库；
- 其次，包含一个大规模的多模态数据集，其中包含交替的图像和文本序列等多种数据形式；
- 再次，可用于视觉-语言任务的上下文学习评估基准，并把亲自copy训练的模型进行评估，从而可以水更多论文；
- 最后，基于LLaMA的OpenFlamingo-9B模型的第一个版本已经出来了，更多更好的模型与权重正在路上。

#### CLIP （OpenAI）

【2021-2-26】OpenAI推出[CLIP](https://openai.com/research/clip) (Contrastive Language–Image Pre-training) 使用零样本迁移学习
- Alec Radford等人提出 Contrastive Language-Image Pre-training (CLIP), 突破了**文本-图像**之间的限制
- [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020)

解决什么问题
- 视觉数据集重人力，即便是一个小任务也需要昂贵的人力开销
- 标准视觉模型仅适用于单任务，迁移代价较大
- 标准数据集上效果好的模型在别的数据集上差强人意。

现有计算机视觉方法存疑

常规图像分类模型往往基于有类别**标签**的图像数据集进行**全监督训练**
- 例如在Imagenet上训练的Resnet，Mobilenet，在JFT上训练的ViT等。
- 对于数据需求非常高，需要大量人工标注；同时限制了模型的适用性和泛化能力，不适于任务迁移。

互联网上可以轻松获取大批量的**文本-图像**配对数据。
- Open AI团队通过收集4亿（400 million）个**文本-图像**对（(image, text) pairs），以用来训练其提出的CLIP模型。文本-图像对的示例如下：
- ![](https://pic3.zhimg.com/80/v2-18a53b79e4d4d84554b87b79b90e32ea_1440w.webp)

解法：用神经网络解决这些问题
- 使用互联网上海量图像、文本信息来训练，执行各种各样的分类任务，不优化标准指标 --- **零样本**学习
- 打通文本-图像预训练实现ImageNet的zero-shot分类，比肩全监督训练的ResNet50/101 -- [详见](https://zhuanlan.zhihu.com/p/521151393)

CLIP模型结构包括两个部分: `文本编码器`（Text Encoder）和`图像编码器`（Image Encoder)。
- Text Encoder选择的是Text Transformer模型；
- Image Encoder选择了两种模型，一是基于CNN的ResNet（对比了不同层数的ResNet），二是基于Transformer的ViT。
- ![](https://pic4.zhimg.com/80/v2-a5a6e3556616eeab64b581c43af9541f_1440w.webp)

训练过程可视化
- [video](https://vdn3.vzuu.com/SD/0cd76ac0-de6a-11ec-8768-5ecc511d5822.mp4?disable_local_cache=1&bu=078babd7&c=avc.1.1&f=mp4&expiration=1682670815&auth_key=1682670815-0-0-3d7d915b04388469078063f13d1502fa&v=tx&pu=078babd7)

- ![](https://openaicom.imgix.net/fbc4f633-9ad4-4dc2-bd94-0b6f1feee22f/overview-a.svg?fm=auto&auto=compress,format&fit=min&w=1919&h=1366)

CLIP使用大规模的**文本-图像**配对预训练，并且可以直接迁移到Imagenet上，完全不需要图像**标签**微调即可实现zero-shot分类。CLIP模型或许会引导CV的发展走向大规模预训练，文本-图像打通的时代。

通过大批量的文本-图像预训练后, CLIP可以先通过编码，计算输入的文本和图像的余弦相似度，来判断数据对的匹配程度。
- ![](https://pic1.zhimg.com/80/v2-c158945fccd0084248d6dd4e857d3130_1440w.webp)
- 上面的示例为正样本，下面的示例为负样本。两对数据的图片其实都是猫，但负样本的文本将其描述成了狗，所以计算出的余弦相似度低，CLIP模型可以认定其文本与图像不匹配。

CLIP这个模型最大的亮点：<span style='color:red'>zero-shot图像分类</span>。


#### FLAVA

整体结构类似CLIP，但是引入了单模态和多模态的预训练任务，单模态的任务有MLM，MIM，多模态有GC，ITM等，同时将融合两个模态的方式改为了Transformer


#### BEiT 系列


演进[过程](https://github.com/microsoft/unilm/tree/master/beit)
-   June 2021: release preprint [BEiT: BERT Pre-Training of Image Transformers](https://arxiv.org/abs/2106.08254)
-   July 2021: release [the code and pretrained models of **BEiT**](https://github.com/microsoft/unilm/tree/master/beit)
-   July 2021: BEiT-large achieves **state-of-the-art ImageNet top-1 accuracy (88.6%) under the setting without extra data other than ImageNet-22k**.
-   July 2021: BEiT-large achieves **[state-of-the-art results on ADE20K](https://paperswithcode.com/sota/semantic-segmentation-on-ade20k) (a big jump to 57.0 mIoU) for semantic segmentation**.
-   August 2021: [**BEiT**](https://huggingface.co/transformers/master/model_doc/beit.html) is on [HuggingFace](https://github.com/huggingface/transformers)
-   January, 2022: [**BEiT**](https://openreview.net/forum?id=p-BhZSz59o4) was accepted by **ICLR 2022 as Oral presentation** (54 out of 3391).
-   March, 2022: add [linear probe examples](https://github.com/microsoft/unilm/blob/master/beit/get_started_for_image_classification.md#example-linear-probe-on-imagenet)
-   June 2022: release preprint [VL-BEiT: Generative Vision-Language Pretraining](https://arxiv.org/abs/2206.01127)
-   Aug 2022: release preprint [BEiT v2: Masked Image Modeling with Vector-Quantized Visual Tokenizers](https://arxiv.org/abs/2208.06366)
-   Aug 2022: release preprint [Image as a Foreign Language: BEiT Pretraining for All Vision and Vision-Language Tasks](https://arxiv.org/abs/2208.10442)
-   Sept 2022: release [the code and pretrained models of **BEiT v2**](https://github.com/microsoft/unilm/tree/master/beit2)
-   March, 2023: [**BEiT-3**](https://arxiv.org/abs/2208.10442) was accepted by **CVPR 2023**.
-   March, 2023: release [the code and pretrained models of **BEiT-3**](https://github.com/microsoft/unilm/tree/master/beit3)



##### BEiT-1

【2022-9-3】 哈工大+微软 推出 `BEiT`, Bidirectional Encoder representation from Image Transformers
- 1、将生成式预训练`MLM`方法从NLP迁移至CV，引入 ViT， 实现CV大规模自监督预训练；
  - masked image modeling (MIM) 任务
- 2、统一多模态大模型`BEiT-3`前身。

论文
- [BEIT: BERT Pre-Training of Image Transformers](https://arxiv.org/pdf/2106.08254)
- ![](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/model_doc/beit_architecture.jpg)


##### BEiT-3


`BEiT-3`模型输入变成了三部分: `图`，`文`，`图文对`，通过各自自注意力机制和全联接网络


#### BLIP 系列


##### BLIP-1

【2022-2-15】Saleforce Research

[统一理解和生成的多模态模型 BLIP](https://zhuanlan.zhihu.com/p/521260597)

问题：
- 1）当前 视觉-语言 预训练（VLP）推动了 视觉语言预训练任务的性能，然而大多数现有的预训练模型或者擅长基于理解的任务（分类）或者基于生成的任务之一。encoder-based 架构不擅长生成类任务，encoder-decoder 架构不擅长分类相关任务(如 图文跨模态检索)
- 2）当前 VLP 模型的性能提升依赖于扩大图文对训练集，这些图文对通常是从互联网上爬取的，所以噪声相对较大。

解决方案：
- 提出一种新的 VLP 框架，可以在视觉-语言的 **理解任务** 和 **生成任务** 之间灵活转换，而且可以通过booststraping 的方式有效利用噪声数据，即构造了一个 captioner 用于生成captions，一个 filters 移除噪声 captions。

具体如下：
- 1）提出一种**多模混合** encoder-decoder 架构 (MED)：可以作为独立的编码器，也可以分别作为基于图像的文本编码器和解码器。通过联合三种视觉-语言 的目标进行学习：图文对比学习、图文匹配 和 基于图像的语言建模(image-conditioned language modeling)。

BLIP 结合了encoder和decoder，形成了统一的理解和生成多模态模型。
- 论文：[BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation](https://arxiv.org/pdf/2201.12086.pdf)
- 代码：[BLIP](https://github.com/salesforce/BLIP)

BLIP在预训练时统一了理解中的**图像文本匹配**任务以及生成模型的**图像文本生成**任务
- BLIP可先用decoder来对**图像-文本**的pair进行扩充，相当于一种**数据增强**手段，而后，再利用图像文本匹配来对收集到的数据以及decoder生成的数据进行数据清洗，利用清洗后的数据再次训练能够进一步提升效果。

BLIP 模型结构
- ![](https://pic3.zhimg.com/80/v2-58627c2b0709d1d17b2f8901462d258e_1440w.webp)

BLIP 模型一共分为三个部分：
- Unimodal encoder，这里分别为图像特征提取器和文本特征提取器
- Image-grounded text encoder，输入图像特征和文本
- Image-grounded text decoder，输入图像特征，输出文本

BLIP 的预训练任务也是有三个：
- Unimodal encoder 输出的图像特征和文本特征进行对比学习（itc）；
- Image-grounded text encoder 输出来判断图文是否一致（itm）；
- Image-grounded text decoder 的文本生成任务（lm）

三个预训练任务统一进行训练，能够更加充分地利用收集到的图文多模态数据，也能使得BLIP模型能够同时满足图文理解任务与图文生成任务。

BLIP CapFilt

BLIP另一大创新点便是`CapFilt`。CapFilt 是Caption 和 Filter的缩写。
- Caption就是对图像生成Caption，这里其实是利用Image-grounded text decoder 来对图像进行处理，生成描述，用以进行数据扩充。由于收集到的图文多模态数据，以及利用模型生成的匹配图文多模态数据，都会存在一定的噪声，这时再利用Image-grounded text encoder 来对收集到的图文多模态数据和利用模型生成的匹配图文多模态数据进行数据清洗，这便是Filter。利用清洗后的数据再次训练BLIP能进一步提升效果。

BLIP两大亮点分别为：
- 1）模型既有encoder模块又有decoder模块，在预训练中统一了多模态理解与多模态生成任务；
- 2）利用数据扩充与数据清洗（CapFilt）进一步提升了模型的效果。

结果：
- 1）在图文检索任务中，本方案相较 SOTA， top1 recall 提升了 2.7%
- 2）在 image caption 任务中，CIDEr 指标提升 2.8%
- 3) 在 VQA 本方案相对 SOTA 算法获得了 1.6% 的VQA score 指标提升

##### BLIP-2 （Flamingo）

【2023-1-30】BLIP-2 基于 Flamingo
-  【2023-6-15】论文：[BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](https://arxiv.org/abs/2301.12597)
- 代码：[blip-2](https://huggingface.co/docs/transformers/main/model_doc/blip-2), [lavis](https://github.com/salesforce/LAVIS/tree/5ee63d688ba4cebff63acee04adaef2dee9af207)

充分利用大模型原始能力，不做预训练，而通过一个轻量级的 Querying transformer（Q-former）弥补了模态之间的差距, 连接视觉大模型和语言大模型。

论文主要提出`Q-Former`（Lightweight Querying Transformer）用于连接模态之间的gap。

`BLIP-2` 整体架构包括三个模块：**视觉编码器**、视觉和LLM的**Adapter**(Q-Former)、**LLM**。
- 其中,Q-Former是BLIP-2模型训练过程中主要更新的参数，视觉Encoder和大语言模型LLM在训练过程中冻结参数。

模型结构：
- Vision Encoder：ViT-L/14
- VL Adapter：Q-Former
- LLM：OPT (decoder-based)，FlanT5（encoder-decoder-based）

Q-former 通过两阶段方式进行训练：
- 阶段 1：固定图像编码器，学习**视觉-语言**(vision-language)一致性的表征, 从冻结图像编码器引导视觉语言表示学习
- 阶段 2：固定语言大模型，提升**视觉-语言**(vision-to-language)的生成能力, 将视觉从冻结的语言模型引导到语言生成学习


BLIP-2 可以基于给定图片+文字提示，做条件文本生成

架构
- ![](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/model_doc/blip2_architecture.jpg)

our model outperforms Flamingo 80B by 8.7% on zero-shot VQAv2 with 54x fewer trainable parameters
- 性能优于Flamingo、BEIT-3等网络，达到sota


##### InstructBLIP

【2023.06.15】发布 InstructBLIP
- 论文地址：[paper](https://arxiv.org/pdf/2305.06500)

模型结构：
- Vision Encoder：ViT-g/14
- VL Adapter：Q-Former
- LLM：FlanT5-xl(3B), FlanT5-xxl(11B), Vicuna-7B, Vicuna-13B

![](https://picx.zhimg.com/80/v2-a35f49642809ef843ed0c852b9cfc03b_1440w.webp)


`InstructBLIP` 模型结构与`BLIP-2`类似，区别在于输入文本换成了**指令数据**Instructions. 
- Q-Former 抽取指令感知的视觉特征（Instruction-aware vision model），根据指令的不同获取不同的视觉特征。
- 然后将这些视觉特征作为LLM的软视觉提示（soft prompt），使用language modeling loss和指令微调模型生成回复。

训练过程（Vision-Language Instruction Tuning）：3阶段训练以及zero-shot预测
- Stage 1：预训练，训练Q-Former和Projection Layer，冻结image encoder。使用image caption数据，学习视觉文本相关性表示。
- Stage 2：预训练，训练Projection Layer，冻结LLM。使用image caption数据，学习对齐LLM的文本生成。
- Stage 3：指令微调，训练Q-Former和Projection Layer。使用Instruction任务数据，学习遵循指令生成回复的能力。

训练数据：
- 收集11个任务以及相应的26个数据集，如下图所示。
- 对于每个任务，人工编写10-15个自然语言的指令模版，作为构造指令微调数据的基础。
- 对于偏向较短回复的开源数据集，在指令模版中使用'short/briefly'降低模型过拟合为总是生成较短回复（防止过拟合的方式是在指令中有所体现）。


#### miniGPT-4

【2023-4-17】[MiniGPT-4 发布，代码模型开源了](https://mp.weixin.qq.com/s/WTTjXnczPkBNEBhuVG0SAA)，阿卜杜拉国王科技大学的几位博士
- GitHub: [MiniGPT-4](https://github.com/Vision-CAIR/MiniGPT-4)
- [demo](https://minigpt-4.github.io/)
- 【2023-10-02】论文：[MiniGPT-4: Enhancing Vision-Language Understanding with Advanced Large Language Models](https://arxiv.org/abs/2304.10592)


GPT-4 所实现的多模态能力，在以前的视觉 - 语言模型中很少见，因此认为，GPT-4 先进的多模态生成能力，主要原因在于利用了更先进的大型语言模型。

为了验证这一想法，团队成员将一个冻结的视觉编码器与一个冻结的 Vicuna 进行对齐，造出了 MiniGPT-4。
- MiniGPT-4 具有许多类似于 GPT-4 的能力, 图像描述生成、从手写草稿创建网站等
- MiniGPT-4 还能根据图像创作故事和诗歌，为图像中显示的问题提供解决方案，教用户如何根据食物照片做饭等。

未来在图像、声音、视频等领域，基于这些大语言模型所造出来的应用，其实际效果都不会太差。

这个项目证实了大语言模型在图像领域的可行性，接下来应该会有不少开发者入场，将 GPT-4 的能力进一步往音频、视频等领域延伸，进而让我们得以看到更多有趣、令人惊艳的 AI 应用。

MiniGPT-4 在一些开源大模型基础上训练得到，fine tune 分为两个阶段
- 先是在 4 个 A100 上用 500 万图文对训练
- 然后再用一个小的高质量数据集训练，单卡 A100 训练只需要 7 分钟。
- ![](https://cdnimg.redian.news/mmbiz_png/v1JN0W4OpXhgzibJjicibeABIRicPxrk3OGRiaMs0V21oZnSMcWHjiaB6x8qNNKc76b4tS10WKTo1XGhvhQXfPQ1qChQ/640?wx_fmt=png)

BLIP-2 模型利用冻结预训练的图像编码器和大型语言模型，通过在它们之间训练一个轻量级的 12 层 Transformer 编码器，实现了各种视觉-语言任务的最先进性能。值得注意的是，在零样本 VQAv2 上，BLIP-2 相较于 80 亿参数的 Flamingo 模型，使用的可训练参数数量少了 54 倍，性能提升了 8.7 %。

投影层（Projection Layer）是神经网络中的一种常见层类型，它将输入数据从一个空间映射到另一个空间。在自然语言处理中，投影层通常用于将高维词向量映射到低维空间，以减少模型参数数量和计算量。在图像处理中，投影层可以将高维图像特征向量映射到低维空间，以便于后续处理和分析。

将一个冻结的视觉编码器和一个冻结的语言模型（如 Vicuna）通过一个投影层对齐意味着:
- 两种模型保持其独立训练得到的特征表示能力，通过投影层获得了一个共同的更低维的表达空间。
- 一个冻结的视觉编码器：指的是一个事先训练好的图像特征提取器，它将输入的图像转换成向量形式。
- 一个冻结的 LLM (Vicuna)：指的是另一个事先训练好的大型语言模型，它可以生成文本或者对文本进行理解。

模型结构：
- Vision Encoder：ViT-G/14
- VL Adapter：Q-Former
- Projection Layer：a single linear
- LLM：Vicuna

训练过程：
- Stage 1：只训练Linear Projection Layer来对齐视觉特征和大语言模型。使用大量text-image pair数据。
- Stage 2：指令微调，使用少量高质量text-image instruction数据
- 指令模板：`###Human: <Img><ImageFeature></Img><Instruction>###Assistant:`


##### MiniGPT-v2

【2023.11.07】
- 论文地址：[paper](https://arxiv.org/pdf/2310.09478)

模型结构：
- Vision Encoder：ViT
- VL Adapter：/
- Projection Layer：Linear
- LLM：Llama2-7B

![](https://picx.zhimg.com/80/v2-ec3800841820dadcffa24db69da76be9_1440w.webp)

训练过程：
- Stage 1：预训练，使用大量弱监督image-text和细粒度数据集的混合数据训练，让模型获取多样化知识
- Stage 2：多任务训练，只使用细粒度高质量数据集训练模型在不同任务上的能力。
- Stage 3：多模态质量微调，让模型具备Chat哪里



#### LLaVA

【2023-4-17】[Visual Instruction Tuning: 用LLaVA近似多模态GPT-4](https://mp.weixin.qq.com/s/Ygf2j-rsyLTwZx3FDK6KEQ) 用 GPT-4 进行视觉指令学习
- 论文：[Visual Instruction Tuning](https://arxiv.org/abs/2304.08485)
- Generated by [GLIGEN](https://gligen.github.io/): A cute lava llama and glasses

LLaVA (Language-and-Vision Assistant)，一款展示了某些近似多模态 GPT-4 水平能力的语言和视觉助手：
- 视觉聊天 (Visual Chat)：相对得分达到了 GPT-4 的 85%
- 多模态推理任务的科学问答 (Science QA)：达到了新的 SoTA 92.53%，超过了之前的最先进的方法：多模态思维链技术 (multimodal chain-of-thoughts)

- 项目主页 [Project Page](https://llava-vl.github.io)
- 论文 [Paper](https://arxiv.org/abs/2304.08485)
- 代码 [GitHub](https://github.com/haotian-liu/LLaVA)
- 演示 [Demo](https://llava.hliu.cc)
- 数据 [Data](https://huggingface.co/datasets/liuhaotian/LLaVA-Instruct-150K) (158K unique language-image instruction-following samples)
- 模型 [Model](https://huggingface.co/liuhaotian/LLaVA-13b-delta-v0) (LLaVA-13B):


1. 多模态指令跟踪数据（Multimodal Instruction-following Data） 
  - 数据质量是这个项目的关键。我们大部分时间都在迭代新的指令数据。在这个数据为中心（Data-Centric）的项目中，需要考虑以下因素：图像的符号化表示(包括 Caption & Boxes)、ChatGPT vs GPT-4、提示工程（Prompt Engineering）等。 
  - 看到学术圈一直以来没有这类数据，我们开源了我们最新一个版本的数据，希望能启发更多人沿着这个道路去探索。
2. 视觉对话（Visual Chat）
  - LLaVA 在涉及面向用户应用的聊天过程中表现出非常强的泛化能力，尽管只是在不到 1M CC/COCO 数据的训练下进行的。 
  - (a) 强大的多模态推理能力：GPT-4技术报告中的两个基于图像的推理示例，一度以为难以企及，利用LLaVA现在可以轻松复现。
  - (b) 强大的 OCR 文字识别能力：请看我刚刚制作的一些示例。它能识别 CVPR、我们的举办的 Computer Vision in the Wild (CVinW) Workshop 的标志的图片，和 LLaVA 本身相关的照片。
3. 科学问答（Science QA）
  - 单独使用 LLaVA 实现了 90.92％ 的准确率。我们使用仅文本的 GPT-4 作为评判者，根据其自身先前的答案和 LLaVA 的答案预测最终答案。这种“GPT-4 作为评判者”的方案产生了新的 SOTA 92.53％。令人惊讶的是，GPT-4 可以作为一种有效的模型集成方法！这些结果希望启发大家以后刷榜的时候，可以利用 GPT-4 这个神奇来集成不同方法。


模型结构：
- Vision Encoder：ViT-L/14
- VL Adapter：/
- Projection Layer：a linear layer
- LLM：LLaMA

![](https://pic1.zhimg.com/80/v2-e32dc3e950201a2cd19287eb07713b00_1440w.webp)

训练过程：
- Stage 1：Pre-training for Feature Alignment. 训练Projection Layer
- Stage 2：Fine-tuning End-to-End. 训练Projection Layer和LLM


##### LLaVA 中文版

- LinkSoul.AI 开源了可商用的中英文双语视觉 - 语言助手 Chinese-LLaVA 以及中英文视觉 SFT 数据集 [Chinese-LLaVA-Vision-Instructions](https://huggingface.co/datasets/LinkSoul/Chinese-LLaVA-Vision-Instructions)，支持中英文视觉 - 文本多模态对话的开源可商用对话模型。
  - 代码 [Chinese-LLaVA](https://github.com/LinkSoul-AI/Chinese-LLaVA), 模型、代码和数据[地址](https://huggingface.co/spaces/LinkSoul/Chinese-LLaVa)
  - ![](https://p1.itc.cn/images01/20230804/367c7521624c4ede8d7daf0cfec5a154.gif)


##### LLaVA-1.5

【2024.05.15】

论文地址：[paper](https://arxiv.org/pdf/2310.03744)

模型结构：
- Vision Encoder：Clip预训练 Vit-L/336px
- VL Adapter：MLP
- LLM：Vicuna v1.5 13B

![](https://pic1.zhimg.com/80/v2-d3d18f01a2d8e3aa9afd187db56ff1b0_1440w.webp)


#### MMGPT （基于OpenFlamingo）

【2023-4-27】[MMGPT (Multi-modal GPT) 安装指南和初体验](https://zhuanlan.zhihu.com/p/625456570)

OpenMMLab 团队开源了一个类似 miniGPT-4 和 LLaVA 等的具备多模态对话能力的库 Multi-modal GPT，[地址](https://github.com/open-mmlab/Multimodal-GPT)，对开源的 OpenFlamingo 模型利用视觉和语言数据进行高效 LoRA 联合微调训练

功能
- VQA, Image Captioning, Visual Reasoning, Text OCR, and Visual Dialogue

OpenFlamingo 发布了 9B 的权重，其实已经具备了多模态问答能力。而 MMGPT 是基于这个模型进行一步进行了指令微调。

MMGPT 给出了所有复现步骤

#### X-LLM （中科院）

【2023-5-15】[中科院发布多模态 ChatGPT，图片、语言、视频都可以 Chat ？中文多模态大模型力作](https://mp.weixin.qq.com/s/RqiJvhH4sdtHBVIDZXmu5Q)
- 多模态的大规模语言模型 X-LLM，同时支持图片、语音以及视频等多种模态信息作为大模型的输入，并且展现了类似于 GPT-4 的表现。
- [X-LLM: Bootstrapping Advanced Large Language Models by Treating Multi-Modalities as Foreign Languages](https://arxiv.org/pdf/2305.04160.pdf)
- [项目主页](https://x-llm.github.io/)

用30 张模型未见过的图像，每张图像都与相关于对话、详细描述以及推理三类的问题，从而形成了 90 个指令-图像对以测试 X-LLM 与 GPT-4 的表现。通过使用 ChatGPT 从 1 到 10 为模型回复进行评分，与 GPT-4 相比 X-LLM 取得了 84.5% 的相对分数，表明了模型在多模态的环境中是有效的。

#### VisualGLM

【2023-5-18】[VisualGLM-6B](https://github.com/THUDM/VisualGLM-6B)
- VisualGLM-6B 是一个开源，支持图像、中文和英文的多模态对话语言模型，语言模型基于 ChatGLM-6B，具有 62 亿参数；图像部分通过训练 BLIP2-Qformer 构建起视觉模型与语言模型的桥梁，整体模型共78亿参数。

```py
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("THUDM/visualglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/visualglm-6b", trust_remote_code=True).half().cuda()
image_path = "your image path"
response, history = model.chat(tokenizer, image_path, "描述这张图片。", history=[])
print(response)
response, history = model.chat(tokenizer, "这张图片可能是在什么场所拍摄的？", history=history)
print(response)
```

#### CoDi

【2023-5-19】[CoDi: Any-to-Any Generation via Composable Diffusion](http://arxiv.org/abs/2305.11846), [主页](https://codi-gen.github.io/)
- ![](https://codi-gen.github.io/static/images/teaser.gif)

模型架构
- ![](https://codi-gen.github.io/static/images/main_architecture.jpg)

#### TigerBot

【2023-6-7】[国产大模型效果达OpenAI同规模模型96%，已开源](https://zhuanlan.zhihu.com/p/635299844)

[TigerBot](https://www.tigerbot.com/) 是一款国产自研的**多语言**任务大模型, 包含**70亿**参数和**1800亿**参数两个版本，均对外开源。
- TigerBot-180B 是目前业内开源的最大规模大语言模型。
- GitHub地址：[TigerBot](https://github.com/TigerResearch/TigerBot)

TigerBot 是一个**多语言**、**多任务**的大规模语言模型(LLM)。

成果开源：
- 模型：TigerBot-7B, TigerBot-7B-base，TigerBot-180B (research version)，
- 代码：基本训练和推理代码，包括双卡推理 180B 模型的量化和推理代码，
- 数据：预训练 100G，从 2TB 过滤后的数据中经过去噪去重清洗而得；监督微调 1G 或 100 万条数据，按比例涵盖用户指令常见的 10 大类 120 小类任务，
- API: chat, plugin, finetune, 让用户能在半小时内无代码的训练和使用专属于自己的大模型和数据，
- 领域数据：涵盖金融，法律，百科，广邀大模型应用开发者，一起打造中国的世界级的应用。

在 BLOOM 基础上，在模型架构和算法上做了如下优化：
- 指令完成监督微调的创新算法以获得更好的可学习型(learnability)，
- 运用 ensemble 和 probabilistic modeling 的方法实现更可控的事实性(factuality)和创造性(generativeness)，
- 并行训练上，突破了 deep-speed 等主流框架中若干内存和通信问题，使得在千卡环境下数月无间断，
- 对中文语言的更不规则的分布，从 tokenizer 到训练算法上做了更适合的算法优化。

开源模型包括三个版本：
- TigerBot-7B-sft
- TigerBot-7B-base
- TigerBot-180B-research

TigerBot带来的创新主要有以下几个方面：
- 提出指令完成监督微调的创新算法提升模型可学习性
- 运用ensemble和probabilistic modeling的方法实现可控事实性和创造性
- 在并行训练上突破deep-speed等主流框架中的**内存和通信**问题，实现千卡环境下数月无间断
- 针对中文语言更不规则的分布，从tokenizer到训练算法上做了更适合的优化

使用GPTQ算法和GPTQ-for-LLaMa实现量化

由该模型支持的对话AI同步上线。覆盖生成、开放问答、编程、画图、翻译、头脑风暴等15大类能力，支持子任务超过60种。
- ![](https://pic4.zhimg.com/80/v2-ec1ee44c6602cf9b662811cffbd039ef_1440w.webp)

评测结果显示
- TigerBot-7B 已达到OpenAI同样大小模型综合表现的 96%。
- TigerBot-7B-base的表现优于OpenAI同等可比模型、BLOOM。
- TigerBot-180B-research或是目前业内开源的最大规模模型（Meta开源OPT的参数量为1750亿、BLOOM则为1760亿规模）。

根据 OpenAI InstructGPT 论文在公开 NLP 数据集上的自动评测
- TigerBot-7B 达到 OpenAI 同样大小模型的综合表现的 96%，并且这只是 MVP

此外，团队还一并开源100G预训练数据、监督微调1G或100万条数据。

基于TigerBot，开发者在半天内就能打造出自己的专属大模型。

虎博科技最初只有5人的小团队，首席程序员&科学家就是CEO本人。
- 从2017年起，他们就在NLP领域开始创业，专长垂直领域搜索。最擅长对数据重度依赖的金融领域，和方正证券、国信证券等有过深入合作。
- 创始人兼CEO，有着20多年从业经验，曾任UC伯克利客座教授，手握3篇最佳顶会论文和10项技术专利。

致敬硅谷90年代经典的“车库创业”模式。

团队最初只有5个人，陈烨是首席程序员&科学家，负责最核心的代码工作。后面成员规模虽有扩充，但也只控制在了10人，基本上一人一岗。

陈烨的回答是：
> 我认为从0到1的创造，是一件很极客的事，而没有一个极客团队是超过10个人的。

以及纯技术科学的事，小团队更犀利。

的确，TigerBot的开发过程里，方方面面都透露着果断、敏锐。

陈烨将这个周期分为三个阶段。
- 第一阶段，ChatGPT爆火不久，团队迅速扫遍了OpenAI等机构过去5年内所有相关文献，大致了解ChatGPT的方法机制。
  - 由于ChatGPT代码本身不开源，当时相关的开源工作也比较少，陈烨自己上阵写出 TigerBot 的代码，然后马上开始跑实验。
  - 逻辑很简单，让模型先在小规模数据上验证成功，然后经过系统科学评审，也就是形成一套稳定的代码。
  - 一个月时间内，团队就验证了模型在**70亿**规模下能达到OpenAI同规模模型**80%**的效果。
- 第二阶段，通过不断吸取开源模型和代码中的优点，加上对中文数据的专门优化处理，团队快速拿出了一版真实可用的模型，最早的内测版在2月便已上线。
  - 同时，参数量达到**百亿**级别后，模型表现出了**涌现**的现象。
- 第三阶段，最近的一两个月内，团队在基础研究上实现了一些成果和突破。如上介绍的诸多创新点，就是在这一时期内完成的。
  - 同时整合更大规模算力，达到更快的迭代速度，1-2个星期内，TigerBot-7B 的能力便快速从 InstructGPT 的**80%**提升到了**96%**。
  - 在这个开发周期内，团队始终保持着超高效运转。TigerBot-7B 在几个月内经历了3000次迭代。

小团队的优势是反应速度快，早上确定工作，下午就能写完代码。数据团队几个小时就能完成高质量清洗工作。

但高速开发迭代，还只是TigerBot极客风格的体现点之一。因为他们仅凭10个人在几个月内肝出来的成果，将以全套API的形式向行业开源。

#### Video-LLaMA（视听，达摩院）

【2023-6-8】[给语言大模型加上综合视听能力，达摩院开源Video-LLaMA](https://www.toutiao.com/article/7242158713866404352)

> 能否给大模型装上 “眼睛” 和 “耳朵”，让它能够理解视频，陪着用户互动呢？

达摩院的研究人员提出了 `Video-LLaMA`，一个具有综合视听能力大模型。
- Video-LLaMA 能够感知和理解视频中的视频和音频信号，并能理解用户输入的指令，完成一系列基于音视频的复杂任务，例如音 / 视频描述，写作，问答等。
- 目前[论文](https://arxiv.org/abs/2306.02858)，[代码](https://github.com/DAMO-NLP-SG/Video-LLaMA)
- 交互 demo 都已开放。[Modelscope](https://modelscope.cn/studios/damo/video-llama/summary), [Huggingface](https://huggingface.co/spaces/DAMO-NLP-SG/Video-LLaMA)

Video-LLaMA 采用了模块化设计原则，把视频中的视觉和音频模态信息映射到到大语言模型的输入空间中，以实现跨模态指令跟随的能力。与之前侧重于静态图像理解的大模型研究（MiNIGPT4，LLaVA）不同，Video-LLaMA 面临着视频理解中的两个挑战：捕捉视觉中的动态场景变化和整合视听信号。

为了捕捉视频中的动态场景变化，Video-LLaMA 引入了一个可插拔的视觉语言分支。该分支首先使用 BLIP-2 中预训练好的图片编码器得到每一帧图像的单独特征，再与对应的帧位置嵌入结合后，所有图像特征被送入 Video Q-Former，Video Q-Former 将聚合帧级别的图像表示并且生成定长的综合视频表征。最后采用一个线性层将视频表征对齐到大语言模型的 embedding 空间。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/f80209246dcc48afb2173ec604f082d1~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686829593&x-signature=I8WXUILoDzfUFWFURs90fUrLuDc%3D)

Video-LLaMA 基于视频 / 音频 / 图像的对话的一些例子
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/b89f7d6b0425453d8f524325739d7a00~noop.image?_iz=58558&from=article.pc_detail&x-expires=1686829593&x-signature=NfoFF1poOH0hKgrYYVVRDWItYZo%3D)


音频视频理解依旧是一个非常复杂，尚未有成熟解决方案的研究问题，Video-LLaMA 虽然表现出了令人印象深刻的能力，作者也提到了其存在一些局限性。
- （1）有限的感知能力：Video-LLaMA 的视觉听觉能力仍然较为初级，对复杂的视觉声音信息依然难以辨认。其中一部分原因是数据集的质量和规模还不够好。该研究团队正在积极构建高质量的音频 - 视频 - 文本对齐数据集，以增强模型的感知能力。
- （2）难以处理长视频的：长视频 (如电影和电视节目) 包含大量的信息，对模型的推理能力和计算资源都较高。
- （3）语言模型固有的幻觉问题，在 Video-LLaMA 中依然存在。

Video-LLaMA 作为一个具有综合视听能力的大模型，在音频视频理解领域取得了令人印象深刻的效果。随着研究者的不断攻坚，以上挑战也将逐个被克服，使得音视频理解模型具有广泛的实用价值。

#### PandaGPT -- 大一统

【2023-6-16】剑桥、腾讯AI Lab等提出大语言模型PandaGPT：一个模型统一六种模态
- 通过结合 ImageBind 的模态对齐能力和 Vicuna 的生成能力，同时实现了六种模态下的指令理解与跟随能力。虽然 PandaGPT 的效果尚有提升空间，但展示了跨模态 AGI 智能的发展潜力。
- [论文链接](http://arxiv.org/abs/2305.16355)
- [代码链接](https://github.com/yxuansu/PandaGPT)
- [项目主页](https://panda-gpt.github.io)
- [线上 Demo 展示](https://huggingface.co/spaces/GMFTBY/PandaGPT)

为了实现图像 & 视频、文本、音频、热力图、深度图、IMU 读数六种模态下的指令跟随能力
- PandaGPT 将 ImageBind 的多模态编码器与 Vicuna 大型语言模型相结合

PandaGPT 版本只使用了对齐的**图像 - 文本**数据进行训练，但是继承了 ImageBind 编码器的六种模态理解能力（图像 / 视频、文本、音频、深度度、热量图和 IMU）和它们之间的对齐属性，从而具备在所有模态之间跨模态能力。

PandaGPT 仅仅是一个研究原型，暂时还不足以直接应用于生产环境。


#### InstructBLIP

【2023-6-18】[超越GPT-4！华人团队爆火 InstructBLIP 抢跑看图聊天，开源项目横扫多项SOTA](https://zhuanlan.zhihu.com/p/629714206)
- salesforece和香港科大，华人团队开源了多模态基础模型InstructBLIP，从BLIP2模型微调而来
- InstructBLIP模型更擅长「看」、「推理」和「说」，即能够对复杂图像进行理解、推理、描述，还支持多轮对话等。
- InstructBLIP在多个任务上实现了最先进的性能，甚至在图片解释和推理上表现优于GPT4。
- ![](https://pic2.zhimg.com/v2-4b6fd2e8afecec88cfa6b66004db76a9_b.webp)


#### VisorGPT

【2023-6-20】 [VisorGPT : 如何基于 GPT 和 AIGC 模型定制一个可控的生成模型](https://zhuanlan.zhihu.com/p/637938906)
- [VisorGPT: Learning Visual Prior via Generative Pre-Training](https://arxiv.org/abs/2305.13777)
- [VisorGPT](https://github.com/Sierkinhane/VisorGPT)
- ![](https://pic1.zhimg.com/80/v2-ee8dab89e039fc48e2050c8c0b2fad68_1440w.webp)

可控扩散模型如ControlNet、T2I-Adapter和GLIGEN等可通过额外添加的空间条件如人体姿态、目标框来控制生成图像中内容的具体布局。使用从已有的图像中提取的人体姿态、目标框或者数据集中的标注作为空间限制条件，上述方法已经获得了非常好的可控图像生成效果。

那么，如何更友好、方便地获得空间限制条件？或者说如何自定义空间条件用于可控图像生成呢？例如自定义空间条件中物体的类别、大小、数量、以及表示形式（目标框、关键点、和实例掩码）。

本文将空间条件中物体的形状、位置以及它们之间的关系等性质总结为视觉先验（Visual Prior），并使用Transformer Decoder以Generative Pre-Training的方式来建模上述视觉先验。

因此，可以从学习好的先验中通过Prompt从多个层面，例如表示形式（目标框、关键点、实例掩码）、物体类别、大小和数量，来采样空间限制条件。


#### SEEChat

【2023-6-30】[360 人工智能研究院正式开源中文多模态对话模型 SEEChat](https://www.toutiao.com/article/7250467467510940220)

将视觉能力融入语言模型 LLM的 MLLM（Multimodal Large Language Model），相关的研究路线主要分为两条：
- 一条是原生多模态路线，模型设计从一开始就专门针对多模态数据进行适配设计，代表性的工作有 MSRA的KOSMOS-1[1]和 Google Robotics的 PALM-E，均在今年3月份公开；
- 另一条是单模态专家模型缝合路线，通过桥接层将预训练的视觉专家模型与预训练的语言模型链接起来，代表性的工作有 Deepmind的Flamingo[3]，Saleforce的BLIP-2，以及近期的 LLAVA和 miniGPT4等工作。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/TifKZ0I7QBeBjY~noop.image)


[SEEChat项目](https://github.com/360CVGroup/SEEChat)的重点是将视觉能力与已有的 LLM模型相融合，打造侧重视觉能力的多模态语言模型 MLLM。在多模态能力的实现路线上，我们选择了能够充分复用不同领域已有成果的单模态专家模型缝合路线（Single-modal Experts Efficient integration）,这也是 SEEChat项目的命名来源。

SEEChat v1.0的模型结构如下图6所示，通过 projection layer桥接层，将vision encoder: CLIP-ViT-L/14与开源的中文 LM：chatGLM6B缝合到一起。

#### BayLing 百聆 中科院计算所

【2023-7-4】[中科院计算所推出多语言大模型「百聆」](https://zhuanlan.zhihu.com/p/641100831)
- 论文: [Bridging Cross-lingual Alignment and Instruction Following through Interactive Translation for Large Language Models](https://arxiv.org/abs/2306.10968)
- [Demo](https://nlp.ict.ac.cn/bayling/demo)
- ![](http://mlops.ccloud.conestore.cn:30010/bayling/assets/overview1-c107d293.png)
- ![](https://github.com/ictnlp/BayLing/raw/main/assets/demo.gif)

在中科院计算所信息高铁 Al 训练推理平台 MLOps 上训练并发布了新的大型语言模型「百聆」，旨在让大型语言模型对齐人类意图的同时，将其生成能力和指令遵循能力从英语泛化到其他语种。「百聆」以经济友好、内存节约的方式实现了多语言人机交互能力。


#### VisCPM 面壁智能

【2023-7-6】[VisCPM](https://github.com/OpenBMB/VisCPM)

VisCPM 是一个开源的多模态大模型系列，支持中英双语的多模态对话能力（VisCPM-Chat模型）和文到图生成能力（VisCPM-Paint模型），在中文多模态开源模型中达到最佳水平。VisCPM基于百亿参数量语言大模型CPM-Bee（10B）训练，融合视觉编码器（Q-Former）和视觉解码器（Diffusion-UNet）以支持视觉信号的输入和输出。得益于CPM-Bee基座优秀的双语能力，VisCPM可以仅通过英文多模态数据预训练，泛化实现优秀的中文多模态能力。
- 👐 开源使用：VisCPM可以自由被用于个人和研究用途。我们希望通过开源VisCPM模型系列，推动多模态大模型开源社区和相关研究的发展。
- 🌟 涵盖图文双向生成：VisCPM模型系列较为全面地支持了图文多模态能力，涵盖多模态对话（图到文生成）能力和文到图生成能力。
- 💫 中英双语性能优异：得益于语言模型基座CPM-Bee优秀的双语能力，VisCPM在中英双语的多模态对话和文到图生成均取得亮眼的效果。

![](https://github.com/OpenBMB/VisCPM/raw/main/figures/model_zh.png)


#### BuboGPT 字节

【2023-9-1】[字节发布多模态大模型：BuboGPT](https://www.toutiao.com/article/7271181267092718092)

字节跳动发布自己的多模态大模型`BuboGPT`，整合了包括文本、图像和**音频**在内的多模式输入，能够较好的理解图片、语言数据。Demo上可以上传图片或者音频，然后询问相关的内容，回答效果不错。可以理解中文，但是回答却是英文。
- [体验地址](https://huggingface.co/spaces/magicr/BuboGPT)
- 开源代码: [github地址](https://github.com/magic-research/bubogpt)
- [项目主页](https://bubo-gpt.github.io)

![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/d93e994a622049839769a6a8710e3362~tplv-tt-origin-asy1:5aS05p2hQEFJ5bel5YW3566x.image?_iz=58558&from=article.pc_detail&x-expires=1694415839&x-signature=pWifUxbh17ubx3g3w%2B5EDGJLPDc%3D)


#### LLaSM -- 语音文本

【2023-8-30】[LLaSM: Large Language and Speech Model](https://arxiv.org/abs/2308.15930)， AI 初创公司 LinkSoul.Al
- 这家公司还训练了 Llama中文版 [Chinese-Llama-2-7b](https://github.com/LinkSoul-AI/Chinese-Llama-2-7b), [demo](https://huggingface.co/spaces/LinkSoul/Chinese-Llama-2-7b)
  - Llama 2 语料库仍以英文（89.7%）为主，而中文仅占据了其中的 0.13%。这导致 Llama 2 很难完成流畅、有深度的中文对话。
  - Meta Al 开源 Llama 2 模型的次日，开源社区首个能下载、能运行的开源中文 LLaMA2 模型就出现了。该模型名为「Chinese Llama 2 7B」，由国内 AI 初创公司 LinkSoul.Al 推出。
  - Chinese-Llama-2-7b 开源的内容包括完全可商用的中文版 Llama2 模型及中英文 SFT 数据集，输入格式严格遵循 llama-2-chat 格式，兼容适配所有针对原版 llama-2-chat 模型的优化。
- LinkSoul.AI 开源了可商用的中英文双语视觉 - 语言助手 Chinese-LLaVA 以及中英文视觉 SFT 数据集 [Chinese-LLaVA-Vision-Instructions](https://huggingface.co/datasets/LinkSoul/Chinese-LLaVA-Vision-Instructions)，支持中英文视觉 - 文本多模态对话的开源可商用对话模型。
  - 代码 [Chinese-LLaVA](https://github.com/LinkSoul-AI/Chinese-LLaVA), 模型、代码和数据[地址](https://huggingface.co/spaces/LinkSoul/Chinese-LLaVa)
  - ![](https://p1.itc.cn/images01/20230804/367c7521624c4ede8d7daf0cfec5a154.gif)
- [Demo](https://huggingface.co/spaces/LinkSoul/LLaSM)，代码 [LLaSM](https://github.com/LinkSoul-AI/LLaSM), 数据集[LLaSM-Audio-Instructions](https://huggingface.co/datasets/LinkSoul/LLaSM-Audio-Instructions)
- 多模态模型大多聚集在视觉、文本上，而语音也需要关注，LLaSM 是端到端多模态语音语言模型，能遵循语音→语言指令
- LLaSM 是首个支持中英文语音 - 文本多模态对话的开源可商用对话模型。通过便捷的语音输入的交互方式，大幅改善过往以文本为输入的大模型的使用体验，同时有效避免基于 ASR 解决方案的繁琐流程以及可能引入的错误。

#### NExT-GPT 任意模态

【2023-9-18】[无限接近AGI！新加坡华人团队开源全能“大一统”多模态大模型](https://www.toutiao.com/article/7280048966555992617)

现有的大语言模型
- 一方面是局限于某种**单一模态**信息的处理，而缺乏真正「任意模态」的理解；
- 另一方面是只关注于多模态内容在**输入端**的理解，而不能以任意多种模态的灵活形式输出内容。

已有多模态
- **图像类**: `MiniGPT-4`、`BLIP-2`、`Flamingo`、`InstructBLIP`等
- **视频类**: `Video-LLaMA`, `PandaGPT`等
- **声音类**: `SpeechGPT`等等。

目前的多模态LLM距离真正人类级别的AGI，总感觉少了点「那味儿」。

新加坡国立大学`NExT++`实验室华人团队近期开源了一种支持任意模态输入和任意模态输出的「大一统」多模态大模型，[NExT-GPT](https://next-gpt.github.io)(GPT of Next generation)，支持**任意模态**输入到**任意模态**输出。
- 代码开源：[NExT-GPT](https://github.com/NExT-GPT/NExT-GPT), 上线了Demo系统
- 论文地址：[NExT-GPT: Any-to-Any Multimodal LLM](https://arxiv.org/abs/2309.05519)

NExT-GPT 如何实现任意模态输入到任意模态输出的呢？

技术层面上「没有显著的创新点」——
- 通过有机连接现有的开源 1）**LLM**，2）**多模态编码器**和 3）各种模态**扩散解码器**，构成 NExT-GPT的整体框架，实现任意模态的输入和输出，可谓大道至简。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/13d78d7d7d2f40358ce85117d9be6aeb~tplv-tt-origin-asy2:5aS05p2hQOaWsOaZuuWFgw==.image?_iz=58558&from=article.pc_detail&x-expires=1695639711&x-signature=hL1txP43n4cDNFMznIs6Rr9%2BNOg%3D)

模型呈现为一个「编码端-推理中枢-解码器」三层架构：
- **多模编码**阶段：
  - 利用已开源的编码器对各种输入模态进行编码，然后通过一个投影层将这些特征投影为LLM所能够理解的「类似语言的」表征。中文作者采用了MetaAI的ImageBind统一多模态编码器。
- **推理中枢**阶段：
  - 利用开源LLM作为核心大脑来处理输入信息，进行语义理解和推理。LLM可以直接输出文本，同时其还将输出一种「模态信号」token，作为传递给后层解码端的指令，通知他们是否输出相应的模态信息，以及输出什么内容。作者目前采用了Vicuna作为其LLM。
- **多模生成**阶段：
  - 利用各类开源的图像扩散模型、声音扩散模型以及视频扩散模型，接收来自LLM的特定指令信号，并输出所对应的模型内容（如果需要生成的指令）。

在推理时，给定任意组合模态的用户输入，通过模态编码器编码后，投影器会将其转换为特征传递给LLM（文本部分的输入将会直接出入到LLM）。

然后LLM将决定所生成内容，一方面直接输出文本，另一方面输出模态信号token。

如果LLM确定要生成某种模态内容（除语言外），则会输出对应的模态信号token，表示该模态被激活。

NExT-GPT 并不是**首个**实现任意模态输入到任意模态输出功能。目前有两类前驱工作：
- 一类是不久前所发布的`CoDi`模型，其整合了各种模态的diffusion模型，可以同时处理和生成各种组合的模态内容。
  - 然而作者指出，CoDi由于缺乏LLMs作为其核心部件，其仅限于成对（Parallel）内容的输入和生成，而无法实现复杂的内容推理和决策，根据用户输入的指令灵活相应。
- 另一类工作则试图将LLMs与现有的外部工具结合，以实现近似的「任意多模态」理解和生成，代表性的系统如`Visual-ChatGPT`和`HuggingGPT`。
  - 由于这类系统在不同模块之间的信息传递完全依赖于LLM所生成的文本，其割裂、级联的架构容易不可避免地引入了噪音，降低不同模块之间的特征信息传递效用。并且其仅利用现有外部工作进行预测，缺乏一种整体的端到端训练，这对于充分理解用户的输入内容和指令是不利的。

相比之下，`NExT-GPT`却良好地解决了上述的现有工作的问题——既保证具有较好的学习成效，又全面降低、控制学习成本。


#### Gemini 谷歌

【2023-12-6】Google 正式推出了原生多模态的大型语言模型Gemini，可以同时支持文字、图片和声音的输入。
- [gemini](https://deepmind.google/technologies/gemini/#introduction)

在32项AI测试中，有30项的评分超越了OpenAI的GPT-4。Google CEO Sundar Pichai强调，Gemini是Google有史以来最强大也是最通用的模型。

Gemini模型经过海量数据训练，可以很好识别和理解文本、图像、音频等内容，并可以回答复杂主题相关的问题。所以，非常擅长解释数学和物理等复杂学科的推理任务。

<iframe width="560" height="315" src="https://www.youtube.com/embed/JPwU1FNhMOA?si=85W6sLiefLH3cOfi" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


####  LEGO -- 字节&复旦，视频解读

【2024-1-12】[精确指出特定事件发生时间!字节&复旦多模态大模型解读视频太香了](https://www.toutiao.com/article/7323810989189726755)

字节&复旦大学多模态理解大模型来了，可以精确定位到视频中特定事件的发生时间。
- LEGO模型全都读得懂，并毫不犹豫给出正确答案
- 一个语言增强的多模态grounding模型，多模态LLM跨多种模态进行细粒度理解的能力，此前业内的成果主要强调全局信息。
- 论文 [LEGO:Language Enhanced Multi-modal Grounding Model](https://arxiv.org/pdf/2401.06071.pdf)
- [Demo](https://lzw-lzw.github.io/LEGO.github.io/)

示例
- 狗子转身看镜头时的时间戳是多少？
- 什么时候用爪子推开滑板？
- 宝宝什么时候推起眼镜、舒展了一下身体？又是什么时候翻的书？


数据集转换（Dataset Conversion）：构建模态对齐和细粒度对齐的基础多模态数据集
- 图像模态，作者利用LLaVA-pretrain595K数据集进行模态对齐，细粒度对齐则使用特定数据集如RefCOCO。
- 视频模态用Valley-Pretrain-703K进行模态对齐，Charades-STA数据集用于细粒度对齐。

指令调整数据集生成（Instruction-tuning Dataset Generation）。
- 目的是让模型更好地理解和遵循人类指令。
- 选择了公开可用的数据集（Flickr30K Entities、VCR、DiDeMo等）的子集进行人工注释，以创建上下文示例。它用于指导GPT-3.5在生成指令调整数据集时遵循类似的模式。
- 随后，特定任务的系统提示和随机选择的示例被输入到GPT-3.5中，以生成单轮或多轮对话。最后，进行数据过滤以确保数据集质量。

LEGO模型架构：
- 每个模态的输入通过独立的编码器进行处理，提取特征，然后使用适配器将这些特征映射到LLM的嵌入空间。
- 视频和图像模式的两个示例，蓝色方框表示视频作为输入，而黄色方框表示图像作为输入。
- 由于其基于模块化设计和适配器的架构，LEGO可以无缝集成新的编码器，处理额外的模态，如点云和语音，主打一个好扩展。
- 最后，LEGO使用Vicuna1.5-7B作为基础语言模型，训练由三个阶段完成：多模态预训练，细粒度对齐调整和跨模式指令调整。
- ![](https://lzw-lzw.github.io/LEGO.github.io/images/architecture.png)

LEGO的能力不仅在于视频定位，对图片、音频等多模态任务都很在行。


#### RoboFlamingo 字节

【2024-1-17】[机器人领域首个开源视觉-语言操作大模型，RoboFlamingo激发开源VLMs更大潜能](https://m.sohu.com/a/752424819_129720)

ByteDance Research 基于开源的多模态语言视觉大模型 OpenFlamingo 开发了开源、易用的 RoboFlamingo 机器人操作模型，只用单机就可以训练。使用简单、少量的微调就可以把 VLM 变成 Robotics VLM，从而适用于语言交互的机器人操作任务。

OpenFlamingo 在机器人操作数据集 CALVIN 上进行了验证，实验结果表明，RoboFlamingo 只利用了 1% 的带语言标注的数据即在一系列机器人操作任务上取得了 SOTA 的性能。
- [项目主页](https://roboflamingo.github.io)
- [代码地址](https://github.com/RoboFlamingo/RoboFlamingo)
- [论文地址](https://arxiv.org/abs/2311.01378)


#### LargeWorldModel

谷歌 Gemini 1.5 最强竞对——[LargeWorldModel](https://github.com/LargeWorldModel/LWM)

产品信息：
- LargeWorldModel（LWM）是一种大型多模态自回归模型，由UC伯克利大学开发。它使用 RingAttention 在包含长视频和长文本的大型数据集上进行训练，从而执行语言、图像和视频的理解和生成。

产品功能：
- LWM支持处理多模态信息，能在100万token中准确找到目标文本，还能一口气看完1小时的视频后，准确地回答出有关视频内容细节的问题，突破了当前语言模型在处理复杂的长格式任务的不足。除此之外，LWM还支持图像和视频的生成，被外界视为谷歌Gemini 1.5最强竞对。


#### Chameleon

【2024-5-16】MET 的 FAIR 发布 [Chameleon: Mixed-Modal Early-Fusion Foundation Models](https://arxiv.org/pdf/2405.09818?open_in_browser=true)

Chameleon，一种**早期融合**，基于token的**混合模态**模型族，能够理解和生成任意序列中的图像和文本。概述了一个稳定的训练 
从一开始就采用的方法、对齐方法和为早期融合，基于token的混合模态设置。对模型进行了综合评价的任务，包括视觉问答、图像描述、文本生成、图像生成和长形式混合模态生成。变色龙具有广泛和一般的能力，包括在图像描述任务中的最先进性能，在纯文本任务中优于Llama-2 与Mixtral 8x7B和Gemini-Pro等模型竞争，并表现出非平凡图像生成，都在一个模型中。它还匹配或超过了更大的模型的性能， 包括Gemini Pro和GPT-4V，根据人类对新的长形式混合模态的判断


#### QWen-VL 系列

QWen-VL 系列
- QWen-VL
- QWen2-VL

详见站内专题 [通义千问](qwen)


#### VITA

**首个**能够同时处理视频、图像、文本和音频的开源多模态大语言模型。

【2024-9-10】腾讯优图实验室等机构研究者提出了 VITA，第一个开源的**多模态**大语言模型 (MLLM)，同时处理和分析**视频**、**图像**、**文本**和**音频**模态，具有先进的多模态交互体验。
- 以 `Mixtral 8×7B` 为语言基础，然后扩大其汉语词汇量，并进行**双语**指令微调。
- 通过**多模态对齐**和**指令微调**的两阶段多任务学习赋予语言模型视觉和音频能力。


VITA 展示了强大的多语言、视觉和音频理解能力，其在单模态和多模态基准测试中的出色表现证明了这一点。
- 论文[主页](https://vita-home.github.io)
- 论文标题：[VITA: Towards Open-Source Interactive Omni Multimodal LLM](https://arxiv.org/pdf/2408.05211)
- Github: [VITA](https://github.com/VITA-MLLM/VITA)

提升自然多模态**人机交互体验**方面也取得了长足进步。
- 第一个在 MLLM 中利用**非唤醒交互**和**音频中断**的研究。
- 还设计了额外的状态 token 以及相应的训练数据和策略来感知各种交互场景。

![](https://github.com/VITA-MLLM/VITA/raw/main/asset/VITA_features.png)

VITA 部署采用**复式**方案，一个模型负责**生成**对用户查询的响应，另一个模型持续**跟踪环境输入**。这使得 VITA 具有很好人机交互功能。
- ![](https://github.com/VITA-MLLM/VITA/raw/main/asset/VITA_duplex.png)

VITA 是开源社区探索多模态理解和交互无缝集成的第一步。虽然在 VITA 上还有很多工作要做才能接近闭源同行，但该研究希望 VITA 作为先驱者的角色可以成为后续研究的基石。

用户可以和 VITA 无障碍沟通
- 看到用户穿的白色 T 恤后，会给出搭配什么颜色的裤子；
- 在被问到数学题时，能够实时查看题目类型，进行推理，然后给出准确的答案；
- 当你和别人讲话时，VITA 也不会插嘴，因为知道用户不是和它交流；
- 出去旅游，VITA 也会给出一些建议；

在 VITA 输出的过程中，可以实时打断对话，并展开另一个话题。 


VITA 整体训练流程包括三个阶段：`LLM 指令微调`、`多模态对齐`和`多模态指令微调`。
- `LLM 指令微调`
  - Mixtral 8x7B 的性能属于顶级开源 LLM 中一员，因此该研究将其作为基础。然而研究者观察到官方的 Mixtral 模型在理解中文方面的能力有限。为了注入双语（中文和英文）理解能力，该研究将中文词汇量扩展到基础模型，将词汇量从 32,000 个增加到 51,747 个。在扩展词汇量后，研究者使用 500 万个合成的双语语料库进行纯文本指令微调。
- `多模态对齐`
  - 为了弥合文本和其他模态之间的表征差距，从而为多模态理解奠定基础。仅在视觉对齐阶段训练视觉连接器。
  - (1) 视觉模态
    - 首先, `视觉编码器`。研究者使用 `InternViT-300M-448px` 作为视觉编码器，它以分辨率 448×448 的图像作为输入，并在使用一个作为简单两层 MLP 的视觉连接器后生成了 256 个 token。对于高分辨率图像输入，研究者利用动态 patching 策略来捕捉局部细节。
      - 视频被视作图像的特殊用例。如果视频长度短于 4 秒，则统一每秒采样 4 帧。如果视频长度在 4 秒到 16 秒之间，则每秒采样一帧。对于时长超过 16 秒的视频，统一采样 16 帧。
    - 其次, `视觉对齐`。研究者仅在视觉对齐阶段训练视觉连接器，并且在该阶段没有使用音频问题。
    - 最后, `数据级联`。对于纯文本数据和图像数据，该研究旨在将上下文长度级联到 6K token，如图 4 所示。值得注意的是，视频数据不进行级联。
      - 级联不同的数据有两个好处：使用级联数据训练的模型与使用原始数据训练的模型性能相当。
        - 支持更长的上下文长度，允许从单个图像问题交互扩展到多个图像问题交互，从而产生更灵活的输入形式，并扩展上下文长度。
        - 提高了计算效率，因为视频帧通常包含大量视觉 token。通过级联图像 - 问题对，该研究可以在训练批中保持平衡的 token 数量，从而提高计算效率。
  - (2) 音频模态
    - 一方面是`音频编码器`。输入音频在最开始通过一个 Mel 滤波器组块进行处理，该块将音频信号分解为 mel 频率范围内的各个频带，模仿人类对声音的非线性感知。随后，研究者先后利用了一个 4×CNN 的下采样层和一个 24 层的 transformer，总共 3.41 亿参数，用来处理输入特征。同时他们使用一个简单的两层 MLP 作为音频 - 文本模态连接器。最后，每 2 秒的音频输入被编码为 25 个 tokens。
    - 另一方面是`音频对齐`。对于对齐任务，研究者利用了自动语言识别（ASR）。数据集包括 Wenetspeech（拥有超过 1 万小时的多领域语音识别数据，主要侧重于中文任务）和 Gigaspeech（拥有 1 万小时的高质量音频数据，大部分数据面向英文语音识别任务）。对于音频字幕任务，研究者使用了 Wavcaps 的 AudioSet SL 子集，包含了 400k 个具有相应音频字幕的音频片段。在对齐过程中，音频编码器和连接器都经过了训练。
- 多模态指令微调
  - 该研究对模型进行了指令调整，以增强其指令遵循能力，无论是文本还是音频。
  - 数据构建。指令调优阶段的数据源与表 1 中对齐阶段的数据源相同，但该研究做了以下改进：
    - 问题被随机（大约一半）替换为其音频版本（使用 TTS 技术，例如 GPT-SoVITS6），旨在增强模型对音频查询的理解及其指令遵循能力。
    - 设置不同的系统 prompt，避免不同类型数据之间的冲突，如表 2 所示。例如，有些问题可以根据视觉信息来回答或者基于模型自己的知识，导致冲突。此外，图像数据已被 patch，类似于多帧视频数据，这可能会混淆模型。系统 prompt 显式区分不同数据类型，有助于更直观地理解。
  - 为了实现两种交互功能，即**非唤醒**交互和**音频中断**交互，该研究提出了**复式部署框架**，即同时部署了两个 VITA 模型。
  - 在典型情况下，**生成模型**（Generation model）会回答用户查询。同时，**监控模型**（Monitoring model）在生成过程中检测环境声音。它忽略非查询用户声音，但在识别到查询音频时停止生成模型的进度。监控模型随后会整合历史上下文并响应最新的用户查询，生成模型和监控模型的身份发生了转换。

#### Emu3


【2024-10-21】Ilya观点得证！仅靠预测下一个token统一图像文本视频，智源发布原生多模态世界模型Emu3


**下一token预测**已在大语言模型领域实现了ChatGPT等突破，但是在多模态模型中的适用性仍不明确。

多模态任务仍然由`扩散模型`（如Stable Diffusion）和**组合方法**（如结合 CLIP视觉编码器和LLM）所主导。

2024年10月21日，智源研究院正式发布原生多模态世界模型`Emu3`。该模型只基于下一个token预测，无需扩散模型或组合方法，即可完成文本、图像、视频三种模态数据的理解和生成。
- 代码：[Emu3](https://github.com/baaivision/Emu3)
- 项目页面：[baai](https://emu.baai.ac.cn/)
- 模型：[model](https://huggingface.co/collections/BAAI/emu3-66f4e64f70850ff358a2e60f)

Emu3 在图像生成、视频生成、视觉语言理解等任务中超过了 `SDXL` 、`LLaVA`、`OpenSora` 等知名开源模型，但是无需扩散模型、CLIP视觉编码器、预训练的LLM等技术，只需要预测下一个token。

Emu3 提供了一个强大的视觉 tokenizer，能够将视频和图像转换为离散token。这些视觉离散token可以与文本tokenizer输出的离散token一起送入模型中。与此同时，该模型输出的离散token可以被转换为文本、图像和视频，为Any-to-Any的任务提供了更加统一的研究范式。而在此前，社区缺少这样的技术和模型。

此外，受益于 Emu3 下一个token预测框架的灵活性，**直接偏好优化**（DPO）可无缝应用于自回归视觉生成，使模型与人类偏好保持一致。

Emu3 研究结果证明
- 下一个token预测可以作为多模态模型的一个强大范式，实现超越语言本身的大规模多模态学习，并在多模态任务中实现先进的性能。通过将复杂的多模态设计收敛到token本身，能在大规模训练和推理中释放巨大的潜力。下一个token预测为构建多模态AGI提供了一条前景广阔的道路。

目前Emu3已开源了关键技术和模型。

##### Emu3技术细节

1 数据

Emu3 是在语言、图像和视频**混合数据模态**上从头开始训练的。
- 语言数据：使用与Aquila模型相同的语言数据，一个由中英文数据组成的高质量语料库。
- 图像数据：构建了一个大型图像文本数据集，其中包括开源网络数据、AI生成的数据和高质量的内部数据。整个数据集经过了分辨率、图片质量、类型等方面的过滤过程。训练了一个基于Emu2的图像描述模型来对过滤后的数据进行标注以构建密集的图像描述，并利用vLLM库来加速标注过程。
- 视频数据：收集的视频涵盖风景、动物、植物和游戏等多个类别。

整个视频处理流程包括了场景切分、文本过滤、光流过滤、质量评分等阶段。并使用基于图像描述模型微调得到的视频描述模型来对以上过滤后的视频片段打标文本描述。

2 统一视觉Tokenizer

在SBER-MoVQGAN的基础上训练视觉tokenizer，它可以将4×512×512的视频片段或512×512的图像编码成4096个离散token。它的词表大小为 32,768。Emu3的tokenizer在时间维度上实现了4×压缩，在空间维度上实现了8×8压缩，适用于任何时间和空间分辨率。

此外，基于 MoVQGAN 架构，在编码器和解码器模块中加入了两个具有三维卷积核的时间残差层，以增强视频token化能力。

3 架构

Emu3 保留了主流大语言模型（即 Llama-2）的网络架构。不同点在于，其扩展了 Llama-2 架构中的嵌入层，以容纳离散的视觉token。网络中使用RMSNorm进行归一化。其还使用了GQA注意力机制、SwiGLU激活函数和一维旋转位置编码（RoPE）等技术，并并去除了注意力模块中QKV层和线性投影层中的偏置。此外，还采用了0.1的dropout率来提高训练的稳定性，使用QwenTokenizer对多语言文本进行编码。详细架构配置表。


#### Janus-Pro-7B


【2025-2-7】 DeepSeek Janus-Pro-7B，详见站内专题 [DeepSeek 专题](deepseek#janus)


#### Gemini 2.5

【2025-5-21】[2025谷歌I/O大会：大模型应用全面开花](https://zhuanlan.zhihu.com/p/1908848032109291500)

概括如下：
- （1）`Gemini 2.5` 更快、更聪明、理论能力更强，Gemini 2.5 Pro Deep Think 模式
- （2）内容生成工具：Veo、Imagen 和 Flow，下一代创作利器
  - Veo 3：支持音频提示生成，如城市街道噪音、公园鸟鸣、角色对话等，增强视频真实感。
  - Flow：AI 电影制作工具，可自定义视频镜头、动作、演员和场景等。
  - Imagen 4：图像细节更清晰，表现力更强，支持多种画幅和最高 2K 分辨率。
- （3）谷歌搜索全新 AI 模式
- （4）Android XR：多模态 AI 助手，能够通过摄像头进行实时交互
- （5）谷歌生态远景：将科幻场景的“世界模型”变成现实

轻量级多模态AI模型——`Gemma3n`，并同时宣布Gemma模型家族迎来新成员，包括: 专为医疗领域设计的`MedGemma`和为无障碍沟通打造的`SignGemma`。

Gemma3n 作为**本地运行**AI技术的先锋，被精心打造以适应手机、笔记本和平板电脑等低算力设备的需求。它不仅能够处理文本、音频、图像和视频，而且据谷歌透露，即便在内存低于2GB的设备上，Gemma3n 也能流畅运行，展现了其卓越的架构效率。这一模型在发布当日即对开发者开放预览，并与Gemini Nano共享相同的底层技术架构。

医疗健康领域，谷歌通过旗下的健康AI开发者基金会推出了 `MedGemma`，专注于健康相关文本与图像分析的开放模型。
- MedGemma 具备出色的多模态分析能力，能够帮助开发者在医疗影像识别、病历文本处理等方面构建更加精准的AI解决方案。

谷歌还预告了 `SignGemma` 模型的推出，这款模型专为**手语识别**设计，能将美国手语（ASL）翻译成英语文本。

谷歌声称， SignGemma 是目前为止最强大的**手语**理解模型，旨在助力开发者为聋哑和听障用户打造更友好的沟通工具。



# 结束

