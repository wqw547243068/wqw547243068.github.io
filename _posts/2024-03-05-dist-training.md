---
layout: post
title:  "分布式训练"
date:   2024-03-05 19:25:00
categories: 大模型
tags: GPU Tensorflow Pytorch 并行计算 分布式 huggingface
excerpt: 分布式训练知识点
author: 鹤啸九天
mathjax: true
permalink: /dist
---

* content
{:toc}

# 分布式


【2021-10-13】[OpenAI 研究员最新博客：如何在多GPU上训练真正的大模型？](https://mp.weixin.qq.com/s?__biz=MzU5ODg0MTAwMw==&mid=2247504041&idx=1&sn=a6a8ceaf1cb091d7832351bcddae6ffb&chksm=febc936dc9cb1a7bbcdeef42f304107d7fe221e7999f2a1a508c6164267dc12dd12ee29ad0eb&mpshare=1&scene=23&srcid=1013pNjTo5fSHOxkjfW5JoFs)，[原文链接](lilianweng.github.io/lil-log/2021/09/24/train-large-neural-networks.html)
- 单个GPU卡的内存有限，许多大模型的大小已经超过了单个GPU，训练深且大的神经网络的主要方法有训练**并行**加速、各种模型**架构**以及内存**节省**设计等。
  - （1）并行加速方法有以下几种：
    - **数据**并行性：将相同的模型权重复制到多个worker中，并将一部分数据分配给每个worker以同时进行处理。
    - **模型**并行性
    - **流水线**并行
    - **张量**并行
  - （2）模型架构方面主要有专家混合（MoE）方法。
  - （3）节省内存的设计方法，如：CPU卸载、激活重新计算、混合精度训练、压缩以及内存高效优化器等等。


## 为什么要 多GPU

两种原因：
- 第一种：模型在**一块GPU上放不下**，多块GPU上就能运行完整的模型（如早期的AlexNet）。
- 第二种：多块GPU并行计算可达到**加速训练**的效果。


### 语言模型发展

设计分布式训练系统的一个最重要的原因
- 单个计算设备的算力已经不足以支撑模型训练。

机器学习模型快速发展
- 从2013年AlexNet开始，到2022年拥有5400亿参数的PalM模型，机器学习模型以**每18个月增长56倍**的速度发展。
- 模型参数规模增大的同时，对训练数据量的要求也指数级增长，这更加剧了对算力的需求。

近几年CPU算力增加已经**远低于** `摩尔定律`（Moore's Law）
- 虽然计算加速设备（如GPU、TPU等）为机器学习模型提供了大量的算力，但是其增长速度仍然没有突破每18个月翻倍的`摩尔定律`。

为了能够满足机器学习模型发展，只有通过**分布式训练**系统才可以匹配模型不断增长的算力需求。

大语言模型参数量和数据量非常巨大，因此都采用了分布式训练架构完成训练。
- `OPT`模型训练用了**992块**NVIDIA A100 80G GPU，采用`全分片数据并行`（Fully Sharded Data Parallel）以及Megatron-LM `张量并行`（Tensor Parallelism），整体训练时间将近2个月。
- `BLOOM`模型在硬件和所采用的系统架构方面的细节。训练一共花费3.5个月，使用48个计算节点。
  - 每个节点包含8块NVIDIA A100 80G GPU（总计384个GPU）
  - 并且使用 4*NVLink 用于节点内部GPU之间通信。节点之间采用四个 Omni-Path 100 Gbps网卡构建的增强8维超立方体全局拓扑网络进行通信。
- `LLaMA`模型训练采用 NVIDIA A100 80GB GPU
  - LLaMA-7B 模型训练需要 82432 GPU小时
  - LLaMA-13B 模型训练需要 135168 GPU小时
  - LLaMA-33B 模型训练花费了 530432 GPU小时
  - LLaMA-65B 模型训练花费则高达 1022362 GPU小时。

|模型|GPU型号|GPU数目|训练时间||
|---|---|---|---|---|
|`OPT`|A100|992|2个月|FSDP+TP|
|`BLOOM`|A100|384|3.5个月||
|`LLaMA`|A100||||


### 性能提速

在 pytorch1.7 + cuda10 + TeslaV100的环境下，使用ResNet34，batch_size=16, SGD对花草数据集训练的情况如下：
- 1块 GPU需要9s一个epoch
- 2块 GPU是5.5s
- 8块 是2s。

问题
- 为什么运行时间不是 9/8≈1.1s ? 
- 因为使用GPU数量越多，设备之间的通讯会越来越复杂，所以随着GPU数量的增加，训练速度的提升也是递减的。
- ![](https://pic1.zhimg.com/80/v2-aac042e783410385f791b8a0f70e6d6c_1440w.webp)

误差梯度如何在不同设备之间通信？
- 在每个GPU训练step结束后，将每块GPU的**损失梯度**求**平均**，而不是每块GPU各计算各的。

BN如何在不同设备之间同步？
- 假设 batch_size=2，每个GPU计算的均值和方差都针对这两个样本而言的。
- 而BN的特性是：batch_size 越大，均值和方差越接近与整个数据集的均值和方差，效果越好。
- 使用多块GPU时，会计算每个BN层在所有设备上输入的**均值**和**方差**。如果GPU1和GPU2都分别得到两个特征层，那么两块GPU一共计算4个特征层的均值和方差，可以认为batch_size=4。
- 注意：如果不用**同步BN**，而是每个设备计算自己的批次数据的均值方差，效果与单GPU一致，仅仅能提升**训练**速度；
- 如果使用**同步BN**，效果会有一定提升，但是会损失一部分**并行**速度。
- ![](https://pic4.zhimg.com/80/v2-176db548da9befc70385eee0f45abdd3_1440w.webp)

单GPU、是否使用同步BN训练的三种情况，可以看到
- 使用**同步BN**（橙线）比不使用同步BN（蓝线）总体效果要好一些，不过训练时间也会更长。
- 使用单GPU（黑线）和不使用同步BN的效果是差不多的。
- ![](https://pic1.zhimg.com/80/v2-0fbd4fd5cf062876b9c50779fe0b05a8_1440w.webp)

两种GPU训练方法：`DataParallel`和`DistributedDataParallel`：
- DataParallel是**单进程多线程**的，仅仅能工作在**单机**中。而DistributedDataParallel是**多进程**的，可以工作在单机或多机器中。
- DataParallel通常会慢于DistributedDataParallel。所以目前主流的方法是DistributedDataParallel。

|维度|DP|DDP|
|---|---|---|
|运行环境|单机,单进程多线程|单/多机,多进程|
|速度|慢|快|
||||


## 分布式模式

深度学习任务通用 GPU 进行模型训练。
- 因为 GPU 相对于 CPU 具有更多的**算术逻辑单元**（`ALU`），发挥并行计算的优势，特别适合**计算密集型**任务，更高效地完成深度学习模型的训练。
- 更多 GPU 知识见站内专题 [并行计算GPU](/gpu)

分析
- 虽然 GPU 并行计算能力优异，但**无法单独**工作，必须由 CPU 进行控制调用；
- 而且**显存**和**内存**之间的频繁数据拷贝，可能带来较大的性能开销。
- CPU 虽然计算能力不如 GPU，但可以**独立**工作，直接访问内存数据完成计算。

因此，想获得更好的训练性能，需要合理利用 GPU 和 CPU 的优势。


### 分布式目标

分布式训练总体目标: 提升总训练速度，减少模型训练的总体时间。

总训练速度公式：
- 总训练速度 ∝ 单设备计算速度 X 计算设备总量 X 多设备加速比
- **单设备计算速度**主要由单块计算加速芯片的**运算速度** 和 **数据I/O能力**来决定
  - 对单设备训练效率进行优化，主要技术手段: **混合精度训练**、**算子融合**、**梯度累加**等；
- 分布式训练系统中**计算设备数量**越多，其理论峰值计算速度就会越高，但是受到通信效率的影响，计算设备数量增大则会造成加速比急速降低；
- **多设备加速比**则由计算和通讯效率决定，结合算法和网络拓扑结构进行优化，分布式训练并行策略主要目标就是提升分布式训练系统中的多设备加速比。


### CPU + GPU 工作模式

GPU 模式下的模型训练如图所示，分为4步：
- 第1步，将输入数据从系统内存拷贝到显存。
- 第2步，CPU 指示 GPU 处理数据。
- 第3步，GPU 并行地完成一系列的计算。
- 第4步，将计算结果从显存拷贝到内存。

![](https://aijishu.com/img/bVNCA)

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-06-29T06:30:26.521Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;ChEM8LvE2i4EmNkl0XTt\&quot; version=\&quot;21.5.1\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;g7JWtnAzlr1IYn_n-NA3\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;795\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-1\&quot; value=\&quot;CPU+GPU工作模式\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=0;fontSize=19;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;301\&quot; y=\&quot;60\&quot; width=\&quot;180\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-2\&quot; value=\&quot;内存\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=15;dashed=1;dashPattern=1 1;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;161\&quot; y=\&quot;130\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-3\&quot; value=\&quot;显存\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=15;dashed=1;dashPattern=1 1;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;161\&quot; y=\&quot;280\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-4\&quot; value=\&quot;CPU\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontStyle=0;fontSize=21;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;337.5\&quot; y=\&quot;120\&quot; width=\&quot;92.5\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-5\&quot; value=\&quot;GPU\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontStyle=0;fontSize=21;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;331\&quot; y=\&quot;270\&quot; width=\&quot;99\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-6\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=0.344;exitY=1.075;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0.333;entryY=0;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-2\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-3\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;221\&quot; y=\&quot;240\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;271\&quot; y=\&quot;190\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-7\&quot; value=\&quot;① 复制数据\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;121\&quot; y=\&quot;200\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-8\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=0.75;exitY=0;exitDx=0;exitDy=0;entryX=0.75;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-3\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-2\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;292\&quot; y=\&quot;183\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;291\&quot; y=\&quot;290\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-9\&quot; value=\&quot;④ 复制结果\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;231\&quot; y=\&quot;200\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-10\&quot; value=\&quot;② CPU指示GPU处理数据\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;325\&quot; y=\&quot;180\&quot; width=\&quot;145\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-11\&quot; value=\&quot;③ GPU并行处理数据\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;312.5\&quot; y=\&quot;240\&quot; width=\&quot;145\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-12\&quot; value=\&quot;\&quot; style=\&quot;endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;startArrow=block;startFill=0;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-2\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-4\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;292\&quot; y=\&quot;106.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;291\&quot; y=\&quot;213.5\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-13\&quot; value=\&quot;\&quot; style=\&quot;endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;startArrow=block;startFill=0;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-3\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-5\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;211\&quot; y=\&quot;160\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;348\&quot; y=\&quot;160\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-14\&quot; value=\&quot;显存\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=15;dashed=1;dashPattern=1 1;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;161\&quot; y=\&quot;350\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-15\&quot; value=\&quot;GPU\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontStyle=0;fontSize=21;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;331\&quot; y=\&quot;340\&quot; width=\&quot;99\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-16\&quot; value=\&quot;\&quot; style=\&quot;endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;startArrow=block;startFill=0;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-14\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-15\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;211\&quot; y=\&quot;230\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;348\&quot; y=\&quot;230\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-17\&quot; value=\&quot;显存\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=15;dashed=1;dashPattern=1 1;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;161\&quot; y=\&quot;420\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-18\&quot; value=\&quot;GPU\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontStyle=0;fontSize=21;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;331\&quot; y=\&quot;410\&quot; width=\&quot;99\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-19\&quot; value=\&quot;\&quot; style=\&quot;endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;startArrow=block;startFill=0;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-17\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-18\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;211\&quot; y=\&quot;300\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;348\&quot; y=\&quot;300\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-20\&quot; value=\&quot;Master\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontStyle=0\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;660\&quot; y=\&quot;285\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-21\&quot; value=\&quot;worker\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontStyle=0\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510\&quot; y=\&quot;210\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-22\&quot; value=\&quot;worker\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontStyle=0\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510\&quot; y=\&quot;285\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-23\&quot; value=\&quot;worker\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontStyle=0\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510\&quot; y=\&quot;355\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-24\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontStyle=0\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-21\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-20\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;630\&quot; y=\&quot;175\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;680\&quot; y=\&quot;125\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-25\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontStyle=0\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-22\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-20\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;590\&quot; y=\&quot;235\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;690\&quot; y=\&quot;310\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-26\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontStyle=0\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-23\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-20\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;600\&quot; y=\&quot;245\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;700\&quot; y=\&quot;320\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


### 多机协作

【2024-4-11】多机多卡协作

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-04-11T11:44:33.140Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\&quot; etag=\&quot;24crQQesdd3W9KFhZuw-\&quot; version=\&quot;24.2.2\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;-380\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-6\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;210\&quot; y=\&quot;1540\&quot; width=\&quot;304.58\&quot; height=\&quot;200\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; value=\&quot;分布式训练\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;350\&quot; y=\&quot;1330\&quot; width=\&quot;224.5\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-7\&quot; value=\&quot;CPU节点0\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#6666FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;300\&quot; y=\&quot;1500\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-35\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-11\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; value=\&quot;pre-train\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;146.67999999999995\&quot; y=\&quot;1790\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-34\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-11\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-12\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-11\&quot; value=\&quot;SFT\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;146.67999999999995\&quot; y=\&quot;1860\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-12\&quot; value=\&quot;RLHF\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;146.67999999999995\&quot; y=\&quot;1930\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-13\&quot; value=\&quot;GPU节点0\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;715.6800000000001\&quot; y=\&quot;1390\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-26\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-6\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;400\&quot; y=\&quot;1360\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;545\&quot; y=\&quot;1090\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-47\&quot; value=\&quot;（1）\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;130.0000000000001\&quot; y=\&quot;1805\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-51\&quot; value=\&quot;（2）\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;130.0000000000001\&quot; y=\&quot;1875\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-52\&quot; value=\&quot;（3）\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;140.0000000000001\&quot; y=\&quot;1945\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-8\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-2\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.86\&quot; y=\&quot;1532\&quot; width=\&quot;304.58\&quot; height=\&quot;96\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-4\&quot; value=\&quot;GPU节点1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;715.6800000000001\&quot; y=\&quot;1523\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-5\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.86\&quot; y=\&quot;1670\&quot; width=\&quot;304.58\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-7\&quot; value=\&quot;GPU节点i\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;715.6800000000001\&quot; y=\&quot;1656\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-8\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.86\&quot; y=\&quot;1810\&quot; width=\&quot;304.58\&quot; height=\&quot;95\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-10\&quot; value=\&quot;GPU节点n-1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;722.6800000000001\&quot; y=\&quot;1798\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-11\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-6\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-2\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;525\&quot; y=\&quot;1735\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;623\&quot; y=\&quot;1490\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-12\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-6\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;525\&quot; y=\&quot;1735\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;623\&quot; y=\&quot;1689\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-13\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-6\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-8\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;535\&quot; y=\&quot;1745\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;633\&quot; y=\&quot;1699\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;210\&quot; y=\&quot;2063\&quot; width=\&quot;304.58\&quot; height=\&quot;230\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-15\&quot; value=\&quot;CPU节点1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#6666FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;270\&quot; y=\&quot;2040\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-16\&quot; value=\&quot;数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;260\&quot; y=\&quot;2090\&quot; width=\&quot;60\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-17\&quot; value=\&quot;模型权重\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;340\&quot; y=\&quot;2090\&quot; width=\&quot;60\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-18\&quot; value=\&quot;梯度\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;260\&quot; y=\&quot;2174\&quot; width=\&quot;60\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-19\&quot; value=\&quot;。。。\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;344\&quot; y=\&quot;2174\&quot; width=\&quot;60\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-20\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.86\&quot; y=\&quot;1945\&quot; width=\&quot;304.58\&quot; height=\&quot;95\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-22\&quot; value=\&quot;GPU节点0\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;715.6800000000001\&quot; y=\&quot;1930\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-23\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-20\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-14\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;515\&quot; y=\&quot;2175\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;545\&quot; y=\&quot;1630\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-24\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.86\&quot; y=\&quot;2072\&quot; width=\&quot;304.58\&quot; height=\&quot;96\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-26\&quot; value=\&quot;GPU节点1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;715.6800000000001\&quot; y=\&quot;2063\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-27\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.86\&quot; y=\&quot;2210\&quot; width=\&quot;304.58\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-29\&quot; value=\&quot;GPU节点i\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;715.6800000000001\&quot; y=\&quot;2196\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-30\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.86\&quot; y=\&quot;2350\&quot; width=\&quot;304.58\&quot; height=\&quot;95\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-32\&quot; value=\&quot;GPU节点n-1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;722.6800000000001\&quot; y=\&quot;2338\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-33\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-24\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-14\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;515\&quot; y=\&quot;2175\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;623\&quot; y=\&quot;2030\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-34\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-27\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-14\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;515\&quot; y=\&quot;2175\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;623\&quot; y=\&quot;2229\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-35\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-30\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-14\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;500\&quot; y=\&quot;2180\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;633\&quot; y=\&quot;2239\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-36\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#6666FF;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;startArrow=classic;startFill=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-6\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-14\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;525\&quot; y=\&quot;1645\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;623\&quot; y=\&quot;1868\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-59\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;612.86\&quot; y=\&quot;1405\&quot; width=\&quot;304.58000000000004\&quot; height=\&quot;95\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-59\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;304.58\&quot; height=\&quot;95\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-45\&quot; value=\&quot;ALU\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-59\&quot;&gt;\n          &lt;mxGeometry x=\&quot;65.13999999999999\&quot; y=\&quot;5\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-46\&quot; value=\&quot;ALU\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-59\&quot;&gt;\n          &lt;mxGeometry x=\&quot;142.39\&quot; y=\&quot;5\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-47\&quot; value=\&quot;ALU\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-59\&quot;&gt;\n          &lt;mxGeometry x=\&quot;65.13999999999999\&quot; y=\&quot;41\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-48\&quot; value=\&quot;ALU\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-59\&quot;&gt;\n          &lt;mxGeometry x=\&quot;142.39\&quot; y=\&quot;41\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-49\&quot; value=\&quot;ALU\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-59\&quot;&gt;\n          &lt;mxGeometry x=\&quot;221.14\&quot; y=\&quot;5\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-50\&quot; value=\&quot;ALU\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-59\&quot;&gt;\n          &lt;mxGeometry x=\&quot;221.14\&quot; y=\&quot;41\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-51\&quot; value=\&quot;DRAM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=17;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-59\&quot;&gt;\n          &lt;mxGeometry x=\&quot;67.13999999999999\&quot; y=\&quot;76\&quot; width=\&quot;224\&quot; height=\&quot;14\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-55\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-59\&quot;&gt;\n          &lt;mxGeometry y=\&quot;5\&quot; width=\&quot;60\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-52\&quot; value=\&quot;Control\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=13;container=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-55\&quot;&gt;\n          &lt;mxGeometry width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-53\&quot; value=\&quot;Cache\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=13;container=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-55\&quot;&gt;\n          &lt;mxGeometry y=\&quot;20\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-56\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-59\&quot;&gt;\n          &lt;mxGeometry x=\&quot;2.1399999999999864\&quot; y=\&quot;45\&quot; width=\&quot;60\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-57\&quot; value=\&quot;Control\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=13;container=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-56\&quot;&gt;\n          &lt;mxGeometry width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-58\&quot; value=\&quot;Cache\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=13;container=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-56\&quot;&gt;\n          &lt;mxGeometry y=\&quot;20\&quot; width=\&quot;60\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-61\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;226.32\&quot; y=\&quot;1560\&quot; width=\&quot;273.68\&quot; height=\&quot;156\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-37\&quot; value=\&quot;ALU\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-61\&quot;&gt;\n          &lt;mxGeometry x=\&quot;123.68\&quot; y=\&quot;5\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-38\&quot; value=\&quot;Cache\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-61\&quot;&gt;\n          &lt;mxGeometry y=\&quot;74\&quot; width=\&quot;273.68\&quot; height=\&quot;44\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-39\&quot; value=\&quot;Control\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-61\&quot;&gt;\n          &lt;mxGeometry width=\&quot;113.68\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-41\&quot; value=\&quot;ALU\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-61\&quot;&gt;\n          &lt;mxGeometry x=\&quot;200.93\&quot; y=\&quot;5\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-42\&quot; value=\&quot;ALU\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-61\&quot;&gt;\n          &lt;mxGeometry x=\&quot;123.68\&quot; y=\&quot;38\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-43\&quot; value=\&quot;ALU\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-61\&quot;&gt;\n          &lt;mxGeometry x=\&quot;200.93\&quot; y=\&quot;38\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-44\&quot; value=\&quot;DRAM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=17;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-61\&quot;&gt;\n          &lt;mxGeometry y=\&quot;126\&quot; width=\&quot;273.68\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-65\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;624\&quot; y=\&quot;1540\&quot; width=\&quot;202.72000000000003\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-3\&quot; value=\&quot;模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-65\&quot;&gt;\n          &lt;mxGeometry width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-62\&quot; value=\&quot;梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-65\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-63\&quot; value=\&quot;优化器\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-65\&quot;&gt;\n          &lt;mxGeometry y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-64\&quot; value=\&quot;激活函数\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-65\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-66\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;624\&quot; y=\&quot;1684\&quot; width=\&quot;202.72000000000003\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-67\&quot; value=\&quot;模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-66\&quot;&gt;\n          &lt;mxGeometry width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-68\&quot; value=\&quot;梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-66\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-69\&quot; value=\&quot;优化器\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-66\&quot;&gt;\n          &lt;mxGeometry y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-70\&quot; value=\&quot;激活函数\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-66\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-71\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;624\&quot; y=\&quot;1820\&quot; width=\&quot;202.72000000000003\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-72\&quot; value=\&quot;模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-71\&quot;&gt;\n          &lt;mxGeometry width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-73\&quot; value=\&quot;梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-71\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-74\&quot; value=\&quot;优化器\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-71\&quot;&gt;\n          &lt;mxGeometry y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-75\&quot; value=\&quot;激活函数\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-71\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-76\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;624\&quot; y=\&quot;1960\&quot; width=\&quot;202.72000000000003\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-77\&quot; value=\&quot;模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-76\&quot;&gt;\n          &lt;mxGeometry width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-78\&quot; value=\&quot;梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-76\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-79\&quot; value=\&quot;优化器\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-76\&quot;&gt;\n          &lt;mxGeometry y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-80\&quot; value=\&quot;激活函数\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-76\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-81\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;624\&quot; y=\&quot;2080\&quot; width=\&quot;202.72000000000003\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-82\&quot; value=\&quot;模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-81\&quot;&gt;\n          &lt;mxGeometry width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-83\&quot; value=\&quot;梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-81\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-84\&quot; value=\&quot;优化器\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-81\&quot;&gt;\n          &lt;mxGeometry y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-85\&quot; value=\&quot;激活函数\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-81\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-86\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;624\&quot; y=\&quot;2220\&quot; width=\&quot;202.72000000000003\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-87\&quot; value=\&quot;模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-86\&quot;&gt;\n          &lt;mxGeometry width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-88\&quot; value=\&quot;梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-86\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-89\&quot; value=\&quot;优化器\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-86\&quot;&gt;\n          &lt;mxGeometry y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-90\&quot; value=\&quot;激活函数\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-86\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-91\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;624\&quot; y=\&quot;2360\&quot; width=\&quot;202.72000000000003\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-92\&quot; value=\&quot;模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-91\&quot;&gt;\n          &lt;mxGeometry width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-93\&quot; value=\&quot;梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-91\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-94\&quot; value=\&quot;优化器\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-91\&quot;&gt;\n          &lt;mxGeometry y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-95\&quot; value=\&quot;激活函数\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;MzKt8NfVXthm0VmUftic-91\&quot;&gt;\n          &lt;mxGeometry x=\&quot;111.36000000000001\&quot; y=\&quot;40\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


- 更多 GPU 知识见站内专题 [并行计算GPU](/gpu)


### 常见问题

模型训练的常见问题
- 问题一：GPU 显存爆满，资源不足
  - V100 为例，其显存最高也仅有 32G，甚至有些显存仅 12G 左右。因此当模型的参数量较大时，在 GPU 模式下模型可能无法训练起来。
  - 设置 CPU 模式进行模型训练，可以避免显存不足的问题，但是训练速度往往太慢。
  - 如何在单机训练中充分地利用 GPU 和 CPU 资源，让部分层在 CPU 执行，部分层在 GPU 执行呢？
- 问题二：频繁数据拷贝，训练效率低

## 分布式训练


### 资料



【2024-8-23】Github 分布式训练总结 [tech_slides](https://github.com/JianyuZhan/tech_slides/blob/main/LLM%E5%88%86%E5%B8%83%E5%BC%8F%E8%AE%AD%E7%BB%83%E6%8A%80%E6%9C%AF.pdf), pdf

【2024-5-27】 MIT 助理教授 Song Han 的 分布式训练介绍 ppt: 
- Distributed Training: [part1](https://www.dropbox.com/scl/fi/vn3n0b2r5fgcc0j0vrh0k/lec17.pdf), [part2](https://www.dropbox.com/scl/fi/11d766q8f62y5lx2tnt9h/lec18.pdf)
- [On-Device Training and Transfer Learning](https://www.dropbox.com/scl/fi/6h69a1z5vqry63nxqdzt0/lec19.pdf)
- [Efficient Fine-tuning and Prompt Engineering](https://www.dropbox.com/scl/fi/lt97w5j9zyscsgizyawme/lec20.pdf)

part1

<object type="application/pdf" data="https://www.dropbox.com/scl/fi/vn3n0b2r5fgcc0j0vrh0k/lec17.pdf"
           id="review" style="width:100%;  height:800px; margin-top:0px;  margin-left:0px" >
</object>

part2

<object type="application/pdf" data="https://www.dropbox.com/scl/fi/11d766q8f62y5lx2tnt9h/lec18.pdf"
           id="review" style="width:100%;  height:800px; margin-top:0px;  margin-left:0px" >
</object>


### 通信技术

分布式条件下的多进程、多worker之间的通信技术，常见的主要有：MPI、NCCL，GRPC等。
- **MPI**主要是被应用在超算等大规模计算领域，机器学习场景下使用较少。主要是openMPI原语等。
- **NCCL**是NVIDIA针对GPU设计的一种规约库，可以实现多GPU间的直接数据同步，避免内存和显存的，CPU和GPU间的数据拷贝成本。当在TensorFlow中选择单机多卡训练时，其默认采用的就是NCCL方式来通信。
- **GRPC**是比较成熟的通信技术了，spark等框架内也都有用到。

演变
- 早期MPI在CPU和GPU的分布式通信领域都是主力军
- 在NCCL推出之后
  - MPI库现在就只用在了CPU分布式通信场景
  - 而GPU分布式通信库目前都是以NCCL为主（NV场景）。

#### 通信方式

Pytorch 分布式训练通信依赖`torch.distributed`模块，`torch.distributed`提供了`point-2-point communication` 和`collective communication`两种通信方式。
- 点对点 point-2-point communication（`P2P`）提供了send和recv语义，用于任务间的通信。
- 收集 collective communication（`CC`）提供了 scatter/broadcast/gather/reduce/all_reduce/all_gather 语义，不同的backend在提供的通信语义上具有一定的差异性。

训练大模型主要是CC通信


#### GPU通信技术

【2024-6-17】[GPU通信技术：GPU Direct、NVLink与RDMA](https://developer.baidu.com/article/details/3136719)

GPU通信技术是加速计算的关键，其中`GPU Direct`、`NVLink`和`RDMA`是三种主流技术。

RDMA（Remote Direct Memory Access）是一种远程直接内存访问技术，允许一个设备直接访问另一个设备上的内存数据。在GPU通信中，RDMA技术用于加速GPU与CPU、GPU与GPU以及GPU与网络之间的数据传输。

`DMA` 是“**直接内存读取**”的意思，用来传输数据，它也属于**外设**。只是在传输数据时，无需占用CPU。
- 高速IO设备可以在处理器安排下直接与主存储器成批交换数据,称为**直接存储器访问**(Directly Memory Access 简称DMA)

比如GPU与CPU之间存在着大量的数据传输. 
- CPU将需要显示的原始数据放在内存中,让GPU通过DMA的方式读取数据,经过解析和运算,将结果写至显存中,再由显示控制器读取显存中的数据并显示输出.

GPU与CPU集成至同一个处理器芯片时,能够大大减少芯片间的数据搬运,同时因为显存和内存的合并,会大大增加访存压力

DMA传输方向有三个：**外设到内存**，**内存到外设**，**内存到内存**。
- `外设`到`内存`。即从外设读取数据到内存。例如ADC采集数据到内存，ADC寄存器地址为源地址，内存地址为目标地址。
- `内存`到`外设`。即从内存读取数据到外设。例如串口向电脑发送数据，内存地址为源地址，串口数据寄存器地址为目标地址。此时内存存储了需要发送的变量数据。
- `内存`到`内存`。以内部flash向内部sram传输数据为例，此时内部flash地址即为源地址，内部sram地址即为目标地址。同时，需要将DMA_CCRx寄存器的MEM2MEM置位。


##### 一、GPU Direct

GPU Direct 是一种优化GPU之间或GPU与第三方设备之间数据传输的技术。它通过**共享内存访问**和**点对点通信**减少了数据复制和传输延迟。

(1) GPU Direct `Shared Memory`

2010年，NVIDIA推出了GPU Direct Shared Memory技术，允许GPU与第三方PCI Express设备通过共享的host memory实现共享内存访问。这使得内存空间得以共享，减少了数据复制，降低了数据交换延迟。

(2) GPU Direct `P2P` (Peer-to-Peer)

2011年，GPU Direct增加了Peer-to-Peer（`P2P`）技术，支持同一PCI Express总线上的GPU之间的直接访问和传输。这种技术绕过了CPU，使得GPU之间通信更加高效。

(3) GPU Direct `RDMA`

2013年，GPU Direct增加了`RDMA`（Remote Direct Memory Access）支持。

RDMA允许第三方PCI Express设备绕过CPU host memory，直接访问GPU内存。这种技术大幅提升了数据传输效率，尤其适用于高性能计算和数据中心等场景。

##### 二、NVLink

NVLink是一种专门设计用于连接NVIDIA GPU的高速互联技术。它通过点对点通信方式，绕过传统的PCIe总线，提供了更高的带宽和更低的延迟。

带宽与延迟
NVLink采用串行协议，支持双向数据传输，每个方向都有高达32GB/s的带宽。这使得两个GPU之间能够实现高速数据传输和共享，为多GPU系统提供了更高的性能和效率。与传统的PCIe总线相比，NVLink显著降低了通信延迟。

连接与扩展
NVLink可用于连接两个或多个GPU，以实现多GPU协同工作。这种连接方式简化了系统架构，提高了可扩展性。通过NVLink连接的GPU可以共享数据和计算资源，从而在某些应用中实现性能倍增。

##### 三、RDMA

RDMA（Remote Direct Memory Access）是一种远程直接内存访问技术，允许一个设备直接访问另一个设备上的内存数据。在GPU通信中，RDMA技术用于加速GPU与CPU、GPU与GPU以及GPU与网络之间的数据传输。

DMA原理
在介绍RDMA之前，我们需要理解DMA（Direct Memory Access）原理。DMA是一种技术，允许硬件控制器直接从内存读取或写入数据，而不需要经过CPU。这大大减轻了CPU的负担，提高了数据传输效率。RDMA基于此原理，进一步扩展了其应用范围。

RDMA的优势
RDMA提供了高带宽和低延迟的数据传输能力。它利用网卡等设备的远程直接内存访问功能，允许设备之间快速高效地传输大量数据。在高性能计算、数据中心和云计算等领域，RDMA成为提高系统性能的关键技术之一。

GPU与RDMA的结合
通过将RDMA与GPU相结合，可以实现高性能的GPU通信。在这种配置中，GPU可以借助RDMA直接访问其他设备或网络的内存数据，从而避免了不必要的CPU中介和数据拷贝。这不仅提高了数据传输速率，还降低了CPU负载和功耗。

总结：
GPU通信技术在加速计算领域发挥着越来越重要的作用。GPU Direct、NVLink和RDMA是三种主流的GPU通信技术，它们分别通过共享内存访问、高速互联和远程直接内存访问等方式提高了GPU之间的通信效率。在实际应用中，根据不同的场景和需求选择合适的通信技术至关重要。随着技术的不断发展，未来我们有望看到更多创新性的GPU通信解决方案，为高性能计算和数据中心等领域带来更大的性能提升。


#### 如何选择

PyTorch 支持

torch.distributed 支持 3 种后端，分别为 `NCCL`，`Gloo`，`MPI`
- ![](https://pic4.zhimg.com/80/v2-54b2efac8658c14f72104c2101a81ecf_1440w.webp)

如何选择?
- NCCL 目前最快，且对**多进程分布式**（Multi-Process Single-GPU）支持极好，可用于单节点以及多节点的分布式训练。
- 节点即主机。即使是单节点，由于底层机制不同， **distributed** 也比 **DataParallel** 方式要高效。

基本原则：
- 用 NCCL 进行分布式 GPU 训练
- 用 Gloo 进行分布式 CPU 训练

无限带宽互联的 GPU 集群
- 使用 NCCL，因为它是目前唯一支持 InfiniBand 和 GPUDirect 的后端

无限带宽和 GPU 直连
- 使用 NCCL，因为其目前提供最佳的分布式 GPU 训练性能。尤其是 multiprocess single-node 或 multi-node distributed 训练。
- 如果用 NCCL 训练有问题，再考虑使用 Cloo。(当前，Gloo 在 GPU 分布式上，相较于 NCCL 慢)

无限带宽互联的 CPU 集群
- 如果 InfiniBand 对 IB 启用 IP，请使用 Gloo，否则使使用 MPI。
- 在未来将添加 infiniBand 对 Gloo 的支持

以太网互联的 CPU 集群
- 使用 Gloo，除非有特别的原因使用 MPI。


#### MPI 后端

MPI 即**消息传递接口**（Message Passing Interface），来自于高性能计算领域的标准的工具。
- 支持点对点通信以及集体通信，并且是 torch.distributed 的 API 的灵感来源。
- 使用 MPI 后端的优势: 在大型计算机集群上，MPI 应用广泛，且高度优化。

但是，torch.distributed 对 MPI 并不提供原生支持。

因此，要使用 MPI，必须从源码编译 Pytorch。是否支持 GPU，视安装的 MPI 版本而定。

#### Gloo 后端

gloo 后端支持 CPU 和 GPU，其支持集体通信（collective Communication），并对其进行了优化。

由于 GPU 之间可以直接进行数据交换，而无需经过 CPU 和内存，因此，在 GPU 上使用 gloo 后端速度更快。

torch.distributed 对 gloo 提供原生支持，无需进行额外操作。

#### NCCL 通信原语

【2023-7-27】[大模型-LLM分布式训练框架总结](https://zhuanlan.zhihu.com/p/623746805)

NCCL 的全称为 Nvidia 聚合通信库（NVIDIA Collective Communications Library），是一个可以实现多个 GPU、多个结点间聚合通信的库，在 PCIe、Nvlink、InfiniBand 上可以实现较高的通信速度。

NCCL 高度优化和兼容了 MPI，并且可以感知 GPU 的拓扑，促进多 GPU 多节点的加速，最大化 GPU 内的带宽利用率，所以深度学习框架的研究员可以利用 NCCL 的这个优势，在多个结点内或者跨界点间可以充分利用所有可利用的 GPU。

NCCL 对 CPU 和 GPU 均有较好支持，且 torch.distributed 对其也提供了原生支持。

对于每台主机均使用多进程的情况，使用 NCCL 可以获得最大化的性能。每个进程内，不许对其使用的 GPUs 具有独占权。若进程之间共享 GPUs 资源，则可能导致 deadlocks。

NCCL 英伟达集合通信库专用于多个 GPU 乃至多个节点间通信。
- 专为英伟达的计算卡和网络优化，能带来更低的延迟和更高的带宽。

原语
- `Broadcast`： 一对多的通信原语，一个数据发送者，多个数据接收者，可以在集群内把一个节点自身的数据广播到其他节点上。
- `Scatter`： 一对多的通信原语，也是一个数据发送者，多个数据接收者，可以在集群内把一个节点自身的数据发散到其他节点上。与Broadcast不同的是，Broadcast把主节点0的数据发送给所有节点，而Scatter则是将数据进行切片再分发给集群内所有的节点。
- `Gather`： 多对一的通信原语，具有多个数据发送者，一个数据接收者，可以在集群内把多个节点的数据收集到一个节点上。
- `AllGather`： 多对多的通信原语，具有多个数据发送者，多个数据接收者，可以在集群内把多个节点的数据收集到一个主节点上（Gather），再把这个收集到的数据分发到其他节点上（broadcast），即收集集群内所有的数据到所有的节点上。
- `Reduce`： 多对一的通信原语，具有多个数据发送者，一个数据接收者，可以在集群内把多个节点的数据规约运算到一个主节点上，常用的规约操作符有：求累加和SUM、求累乘积PROD、求最大值MAX、求最小值MIN、逻辑与LAND、按位与BAND、逻辑或LOR、按位或BOR、逻辑异或LXOR、按位异或BOXR、求最大值和最小大的位置MAXLOC、求最小值和最小值的位置MINLOC等，这些规约运算也需要加速卡支持对应的算子才能生效。
- `ReduceScatter`： 多对多的通信原语，具有多个数据发送者，多个数据接收者，在集群内的所有节点上都按维度执行相同的Reduce规约运算，再将结果发散到集群内所有的节点上。Reduce-scatter等价于节点个数次的reduce规约运算操作，再后面执行节点个数的scatter次操作。其反向操作是AllGather。
- `AllReduce`： 多对多的通信原语，具有多个数据发送者，多个数据接收者，在集群内的所有节点上都执行相同的Reduce操作，可以将集群内所有节点的数据规约运算得到的结果发送到所有的节点上。


通信原语汇总

汇总如下

|原语操作|模式|说明|图解|示意图|
|---|---|---|---|---|
|`Broadcast`|广播:一对多|广播行为：从节点0广播相同信息到其它节点(0-3)|![](https://pic3.zhimg.com/80/v2-559434c1d53c4b8314c9d79aa70a32c6_1440w.webp)|![](https://pic4.zhimg.com/80/v2-c8aec100f7984bc64dae66dea5067657_1440w.webp) |
|`Scatter`|一对多|另一种广播,从节点0将数据**不同部分**按需发送到不同节点,常见于DP的数据分配起步阶段|![](https://pic3.zhimg.com/80/v2-8cbcae4e5a544f607afc88b9d3c2122a_1440w.webp)|![](https://pic2.zhimg.com/80/v2-988509a65724802d800ff0d40c78ab11_1440w.webp)|
|`Reduce`|规约:多对一|规约操作，Reduce意为减少/精简,一系列简单聚合运算,如:sum/min/max,prod,lor等|![](https://pic2.zhimg.com/80/v2-a364ebb1cdeccfbba2293d983b2b834d_1440w.webp)|![](https://pic1.zhimg.com/80/v2-ea6eef07151786d13cceef53a718fd74_1440w.webp)|
|`AllReduce`|多对多|所有节点上应用相同的Reduce操作,单节点上 Reduce + Broadcast,最消耗带宽|![](https://pic3.zhimg.com/80/v2-2176fb0289edb0b380cceb6bbd2d5ca2_1440w.webp)|![](https://pic1.zhimg.com/80/v2-0411e66990dac2867af16e425eef27e8_1440w.webp)|
|`Gather`|多对一|**反向Scatter**:将多个Sender的数据汇总到单个节点上|![](https://pic2.zhimg.com/80/v2-4b74592358b3acaabbff91e6fe61fae5_1440w.webp)|![](https://pic1.zhimg.com/80/v2-badb6e96036f1cbbd65fc1c9ccf54070_1440w.webp)|
|`AllGather`|多对多|收集所有节点到所有节点上, `AllGather`=`Gather`+`Broadcast`|![](https://pic4.zhimg.com/80/v2-497c129eb7aa4f3b51bd3f3a53e1ca73_1440w.webp)|![](https://pic3.zhimg.com/80/v2-3bfe939e5f713d5c6099ea161fbdffc2_1440w.webp)|
|`ReduceScatter`||将单节点输入求和，再0维度按卡切分并发送, `ReduceScatter`=`Reduce`+`Scatter`|![](https://pic1.zhimg.com/80/v2-55652f9d4274b76249f1e745c66a40d8_1440w.webp)|![]()|
|`All2All`||全交换操作，每个节点都获取其他节点的值|![](https://pic2.zhimg.com/80/v2-ff0a3da8d01c5b7d4391edad5da14661_1440w.webp)|![]()|

All2All 与 All Gather 区别在于：[LLM分布式训练第一课（通讯原语）](https://zhuanlan.zhihu.com/p/682896222)
- All Gather 操作中，不同节点向某一节点收集到的数据是完全相同的
- 而在 All2All 中，不同的节点向某一节点收集到的数据是不同的。

`AllReduce` 的目标: 将不同机器上的数据整合(reduce)后分发给各个机器

`AllReduce` 实现方法
- 最简单: 每个worker将自己的数据广播给所有worker —— 问题： 大量浪费
- 改进: 主从架构, 指定一个worker作为master,负责整合运算,以及分发 —— 问题: master成为网络瓶颈
- 改进: Ring AllReduce 

Ring AllReduce：
- 第一阶段，将N个worker分布在一个环上，并且把每个worker的数据分成N份。
- 第二阶段，第k个worker把第**k份**数据发给下一个worker，同时从前一个worker收到第**k-1份**数据。
- 第三阶段，worker把收到的第k-1份数据和自己的第k-1份数据整合，再将整合的数据发送给下一个worker
- 此循环N次之后，每一个worker都会包含最终整合结果的一份。

假设每个worker的数据是一个长度为`S`的向量，那么Ring AllReduce里每个worker发送的数据量是`O(S)`，和worker的数量N无关。避免了**主从架构**中master需要处理`O(S*N)`数据量而成为网络瓶颈的问题。

`Ring All-reduce`
- Pytorch 实现: `DistributedDataParallel`
- `Ring All-reduce`=`reduce-scatter`+`all-gather`

#### NCCL 通信行为分析

【2024-5-10】[集合通信行为分析 - 基于NCCL](https://www.cnblogs.com/Matrix_Yao/p/15905009.html)

deepspeed 启动多卡训练时，日志里会打印NCCL通信信息，这些日志都是什么意思？

NCCL 通信阶段
- Phase 1 - `启动`阶段 **Bootstrap** Phase: 初始化集合中的所有节点(node)和卡(rank)，确保所有卡知道彼此
  - Initiate all nodes and then all ranks in a collective. It makes sure all ranks know about all other ranks, so any rank is able to communicate with any other rank.
- Phase 2 - `拓扑`阶段 **Topology** Phase: 每隔节点了解机器上各个硬件(CPU/GPU/NIC)映射关系, 创建内部拓扑结构（树/环）,通过PCI和NVLink通信
  - Each node detects and maps out what hardware is located on the machine. 
  - Hardware includes CPUs, GPUs, NICs and interconnect types. 
  - Each node then creates an **intra-machine graph**, connects hardware with `PCIe` or `NVLink` interconnect, and evaluates the graph. 
  - When the intra-machine topology is decided, the system will decide what pattern to use for the whole system. 
  - The two main patterns are a **tree** or a **ring**. 
  - While the topology is evaluated, NCCL is also tuning it by performing tests. This allows each rank to pre-compute thresholds for message sizes.
- Phase 3 - `聚合`阶段 **Collective** Phase: 用户调用NCCL支持的集合通信原语进行通信
  - A user can dispatch many collective operations using the same topology.

用户调用NCCL支持的集合通信原语进行通信：
- 集合通信原语
  - AllReduce
  - Broadcast
  - Reduce
  - AllGather
  - ReduceScatter
- 点对点通信原语
  - Send
  - Recv

NCCL在getAlgoInfo里面使用ncclTopoGetAlgoTime来遍历计算(algorithm, protocol)，最终选择预测会最快做完指定数据量的指定集合通信原语的algorithm和protocol完成该通信原语。


示例
- 以2机16卡, NCCL 2.8.4为例
- NCCL会构建tree，ring graph。

(1) tree 

解析

**拓扑**log格式

```sh
# IP: hostname:pid:tid [cudaDev] NCCL INFO Trees [channel ID] down0 rank/down1 rank/down2 rank->current rank->up rank
10.0.2.11: 2be7fa6883db:57976:58906 [5] NCCL INFO Trees [0] 14/-1/-1->13->12 [1] 14/-1/-1->13->12
# 10.0.2.11上的设备5，其rank为13，有两棵树，分别为channel 0和channel 1: channel 0的子节点只有14, 父节点为12; channel 1一样。
```

**channel** log格式

```sh
# IP: hostname:pid:tid [cudaDev] NCCL INFO Channel [channel ID] current rank[bus ID]->successor rank[bus ID] via transport type
10.0.2.11: 2be7fa6883db:57976:58906 [5] NCCL INFO Channel 00 : 13[3e000] -> 14[40000] via P2P/IPC
# 10.0.2.11上的设备5(rank 为13, bus ID为3e000)，其channel 0连接至rank 14，传输方式为P2P/IPC。
```

结果

依此解析，可得两棵一样的tree，逻辑拓扑如下：[img](https://img2022.cnblogs.com/blog/46419/202202/46419-20220217155443691-259562130.png)
- ![](https://img2022.cnblogs.com/blog/46419/202202/46419-20220217155443691-259562130.png)


(2) ring

Ring Logical Topology

拓扑log格式

```sh
# IP: hostname:pid:tid [cudaDev] NCCL INFO Channel ring_ID/ring_number: rank0 rank1 … last_rank
10.0.2.12: 94f182076445:82261:83141 [0] NCCL INFO Channel 00/02 : 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
# 建成了02个ring，其中第0个ring的成员有：0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15，该ring共由16个rank组成。
```

channel log格式
- 与tree拓扑的格式一致。

可得两个一样的ring，逻辑拓扑如下：[img](https://img2022.cnblogs.com/blog/46419/202202/46419-20220217155443729-494214121.png)
- ![](https://img2022.cnblogs.com/blog/46419/202202/46419-20220217155443729-494214121.png)


#### 梯度压缩

分布式训练的 bandwidth 与 latency bottleneck 主要分布在 梯度 `all-reduce` 和 `scatter` 过程中
- 其中 联邦学习 受限的地方还有与端侧设备的通讯
- ![](https://pic4.zhimg.com/80/v2-cd8999264a7670d906e98e6d5de3978f_1440w.webp)

解法：梯度压缩
- 方法1： prune， 【Deep gradient compression】
  - worker 向 server push 梯度时， 可以对梯度做 prune (sparse gradient) 与 quantization
- 方法2： Low-Rank 【PowerSGD】，梯度映射到低秩空间，而不是去做细粒度的剪枝和量化
  - 2019年 EPFL 的文章 [PowerSGD](https://arxiv.org/abs/1905.13727)， 发了 NIPS
- 方法3： 量化， 1bit SGD
  - 用 one bit 的矩阵作为需要通讯的梯度
- 方法5： terngrad， ternery
  - 梯度量化到 0， -1， 1

梯度延迟更新：解决 latency 的 bottleneck

详见: [分布式训练优化--进阶篇](https://zhuanlan.zhihu.com/p/699372131?utm_psn=1777577429458386944)

### 并行技术

并行技术：
- **数据并行** `dp`（如：PyTorch DDP）: 每个节点复制完整的模型，数据分片
  - 内存开销大，通信量低，容易实施
  - ZeRO 对 data-parallel 的优化，每个gpu有自己独特的数据，同时模型的参数也被均匀的分到 n个gpu上
- **模型并行** `mp` : 完整模型只有一份，其它节点只有模型的局部
  - `张量并行` `tp`: 模型按张量分发
    - 内存开销小，通信量高，容易实施
    - 如：Megatron-LM（1D）、Colossal-AI（2D、2.5D、3D）
  - `流水线并行` `pp`: 模型按层分发
    - 内存开销小，通信量中等，实施难度大
    - 如：GPipe、PipeDream、PipeDream-2BW、PipeDream Flush（1F1B）
- **多维混合**并行（如：3D并行（数据并行、模型并行、流水线并行））
  - 2D 并行: dp+pp, tp+pp
  - 3D 并行: dp+tp+pp
- **自动**并行: 自动搜索并行空间
  - 如：Alpa（自动算子内/算子间并行））, 将并行空间分为 inter-op （pipeline） 与 intra-op （tensor并行），使用NAS搜索这两个空间，考虑整个搜索空间的cost。
- 优化器相关并行（如：ZeRO（零冗余优化器，在执行的逻辑上是数据并行，但可以达到模型并行的显存优化效果）、PyTorch FSDP）


【2023-12-15】MIT 端侧模型训练课程: [TinyML and Efficient Deep Learning Computing](https://hanlab.mit.edu/courses/2023-fall-65940), 含 ppt 和 视频
- powerful deep learning applications on resource-constrained devices.
- Topics include model compression, pruning, quantization, neural architecture search, distributed training, data/model parallelism, gradient compression, and on-device fine-tuning. application-specific acceleration techniques

模型切分分3个互相正交的维度：[`data`, `model-layer`, `model-activation`(Tensor)]
- 这3个维度互不影响，可同时实现，即 `3D parallelism`。
- ![](https://pic1.zhimg.com/80/v2-227b93fda9e3bf182e0aea9f4abb23a0_1440w.webp)


| 并行维度 | 切分方式 Split | 模型完整性 | 通讯 | 对gpu的利用 | 优化手段 |
| data | data | Copy of whole model | 非常少 （只有前向和反向的时候需要通讯） | High （for 训练加速）| ZeRO |
| pipeline | model-layer | Part of model | 中等 | Low （for 显存占用太多，优化显存）| |
| tensor | model-tensor | Part of model | 很多（每个需要reduce的中间结果都要通讯）| High （模型算到底再通讯） ||

详见: [分布式训练优化--进阶篇](https://zhuanlan.zhihu.com/p/699372131?utm_psn=1777577429458386944)



常见多GPU训练方法：
1. **模型并行**：如果**模型特别大**，GPU显存不够，无法将一个显存放在GPU上，需要把网络的不同模块放在不同GPU上，这样可以训练比较大的网络。（下图左半部分）
2. **数据并行**：将整个模型放在一块GPU里，再复制到每一块GPU上，同时进行**正向传播**和**反向误差传播**。相当于加大了batch_size。（下图右半部分）
- ![](https://pic4.zhimg.com/80/v2-92e93b9f002b3782abec2a9f8a9a6153_1440w.webp)

大规模深度学习模型训练中有几个主要范式：
- `数据并行`(DP)：模型尺寸能够被单个GPU 内存容纳，模型的不同实例在不同的 GPU 和不同批数据上运行，模型的每个实例都使用相同的参数进行初始化，但在前向传递期间，不同批次的数据被发送到每个模型。 收集来自每个模型实例的梯度并计算梯度更新。，然后更新模型参数并将其作为更新发送到每个模型实例。
  - ![](https://pic4.zhimg.com/80/v2-de60ad9dffd68d827084d84772b06dbb_720w.webp)
  - ![](https://pic4.zhimg.com/80/v2-b508d84ba9c6a9c6ae2c5be70526da43_1440w.webp)
  - 数据并行通过在 N 台机器上复制模型来实现。拆分 minibatch ，分成 N 个块，让每台机器处理一个块。
  - ![](https://pic3.zhimg.com/80/v2-678f7d2c116f7528be27d6445b6c091a_1440w.webp)
- `模型并行`：当单个 GPU无法容纳模型尺寸时，**模型并行性**变得必要，有必要将模型拆分到多个 GPU 上进行训练。实现模型尺寸超过单个GPU显存的深度学习模型训练。 
  - 这种方法的问题是计算使用效率不高，因为在任何时间点只有一个 GPU 正在使用，而其他 GPU 处于空闲状态。
  - ![](https://pic3.zhimg.com/80/v2-6a4304b529130e86e4552b3d4ed58a4e_720w.webp)
  - 相对于流水线并行和数据并行，模型并行具有以下优点：
    - 支持更大的模型规模：流水线并行和数据并行的限制通常是 GPU 内存大小和 GPU 数量，而模型并行可以支持更大的模型规模，因为模型可以分割成多个子模型，并分配到多个 GPU 上运行。
    - 减少通信开销：流水线并行的模型划分通常会导致模型层之间的通信，而模型并行只需在每个子模型之间进行通信。相对于数据并行，模型并行在执行过程中通信量更少，因为每个 GPU 只需传递模型的一部分而不是全部。
    - 灵活的模型分配：模型并行可以更灵活地将模型分配给不同的 GPU 或计算节点，这意味着可以在不同的 GPU 上运行不同的模型子集，从而实现更好的负载平衡和性能优化。
- `流水线并行` (PP)
  - 朴素流水线并行（Naive Pipeline Parallelism）是将一组模型层分布在多个 GPU 上，并简单地将数据从 GPU 移动到 GPU，就好像它是一个大型复合 GPU 一样。
  - 流水线并行 (PP) 与上述朴素流水线并行几乎相同，但它解决了 GPU 闲置问题，方法是将传入的 batch 为 micro-batches 并人工创建流水线，从而允许不同的 GPU 同时参与计算过程。
  - 流水并行是将一个大型计算任务拆分成多个小的**子任务**，并将子任务在多个处理单元上同时执行。不同于数据并行和模型并行，流水并行不是将数据或模型分割成多个部分并在处理单元间并行处理，而是将一系列计算步骤分解成多个流水阶段，并在多个处理单元上同时执行，以减少总体计算时间。

通俗理解
- `Data Parallelism`：模型1台设备装得下，所以同模型用多份数据分开训练
- `Pipeline Parallelism`：模型装不下，模型1层或多层1台设备装得下，所以同模型按层拆开训练
- `Tensor Parallelism`：模型1层都装不下，所以层内拆开训练

### 数据并行

数据并行性（Data parallelism (DP)）最简单的方法是：将相同的**模型权重**复制到多个worker中，并将一部分数据分配给每个worker以同时进行处理。
- 如果模型规模大于单个GPU的内存，Naive DP无法正常工作时。GeePS（Cui 等人，2016 年）之类的方法将暂时未使用的参数卸载回 CPU，以使用有限的 GPU 内存。数据交换传输在后端进行，且不干扰训练计算。
 
在每个小批量结束时，workers需要同步梯度或权重，以替换旧参数。常见有两种主要的同步方法，它们都有明确的优缺点：
- 1）大容量**同步**并行（ Bulk synchronous parallels (BSP)）：workers在每个小批量结束时同步数据。这种方法可以防止模型权重过时，同时获得良好的学习效率，但每台机器都必须停止并**等待**其他机器发送梯度。
- 2）**异步**并行（Asynchronous parallel (ASP)）：每个GPU工作进程异步处理数据，无需等待或暂停。然而，这种方法很容易导致网络使用陈旧的权重参数，从而**降低**统计学习效率。即使它增加了计算时间，也可能不会加快收敛的训练时间。
 
中间的某个地方是在每次x迭代时，全局同步梯度（x＞1）。自Pytorch v1.5版（Li等人，2021年）以来，该特征在平行分布数据（DDP）中被称为“梯度累积”。Bucket 梯度计算方法避免了梯度的立即AllReduce，而是将多个梯度变化值存储到一个AllReduce中以提高吞吐量，可以基于计算图进行计算和通信调度优化。


<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36\&quot; version=\&quot;24.7.7\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;-408\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; value=\&quot;分布式训练模式：数据并行\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;611.72\&quot; y=\&quot;1220\&quot; width=\&quot;269.29\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-1\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;80\&quot; y=\&quot;1580\&quot; width=\&quot;280\&quot; height=\&quot;160\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-18\&quot; value=\&quot;\&quot; style=\&quot;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png,iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAACAASURBVHic7N15fBx1/T/w13tmd3Nu7mR3ZjZpUkpLmxbaBgotLeUqlHIIgoKKyiGieH4VBLxQVPD48lMQv3KKSlX4gnIVATnkaqFAgQKlUCBN293ZpGmu7ubc3fn8/kj4WmuPJPOZnT3ez8ejDxAz78+7m2TmPZ8TYIwxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxtjuyO0EGGNSUSAQaPJ4PDOFEFOFEI1EVE9EdQCqhRDVAAoB+ACUjF3TD2AEwBARdQHoEkJsB7AVQBsRbU4mk293dHS0ARDp/ysxxpzABQBjWay+vl63LOtIAEcKIQ4DMAeA36HmdgJ4k4heBrDa4/Gs3rJlS9ShthhjDuMCgLEs0tzc7Ovp6VkqhDiJiFYAmOFyShuFEI8Q0aOVlZXPbNiwYcTlfBhj48QFAGOZz6Np2vFEdDaA0wFUuJ3QXvQAuF8IcXc0Gn0SQNLthBhje8cFAGMZKhQKGZZlnQvgEgANbuczQVEAf0ylUrd0dHS0up0MY+w/cQHAWIbRNG0JEX0TwKkAFLfzsckC8CCA60zTfN7tZBhj/8IFAGMZwjCMky3L+j4RLXA7F4e8KIT4YTQafdTtRBhjXAAw5jrDMI4RQvwEwEK3c0mTNZZlfbu9vf0ZtxNhLJ9xAcCYS6ZMmaIlk8mfCSHORX7+Lq4CcIlpmtvcToSxfKS6nQBjecijadpXLMv6K4AFyM+HPwBMB/B5v9+fisViazE6X4Axlib5euNhzBW6ri8C8D8ADnE7lwzzOhFdEolEXnA7EcbyBfcAMJYeqq7rVwG4A4DmdjIZKAjgAr/fXxSLxf4J3nKYMcdxDwBjDgsEAnWqqq4EsMztXLIBET2jKMont23bZrqdC2O5jAsAxhxkGMaxQoiV4Lf+ieoUQnyGlwwy5hweAmDMGaTr+tUAbgVQ5nYyWaiEiD7p9/uVWCzGywUZcwAXAIzJp+q6fguAr4N72ewgAEeXlZVNnT59+qpoNMqrBBiTiG9OjEmk63qxEOKesZP6XOPzlKKipAkVxU2oKJmKipImlBYG4VVL4FEKUeCrgFctAgAkUoMYHulFwhpEMjWA+FA7evtb0dPfir6BNvT2b8ZIMu7mXwcY3TPgbNM0B9xOhLFcwQUAY5I0NDRUJpPJhwAcme62vWoxAhVzEapahFD1ItT4Z4FI3jECOwe2Ity9BuGuNdjWtRojyZi02OMlhHiJiE42TXNH2htnLAdxAcCYBGMn9z0GoDldbfo8pTgguALTtY8gWD4PiuJJS7uWlUR736t417wfrR2Pprt3YIOqqifwCgHG7OMCgDGbQqFQlWVZzyIND38Cob5mCWboZ6Cx7jh4lEKnm9ynpDWEzR1PYFP0fmzb8RxEepbvb/B4PEu2bt3ak47GGMtVXAAwZkMoFCqyLOsfABY72Q6RgoaapTjsgK+gtmy2k01NWldsE9ZvuQ3vta+CZSWdbm5tKpU6rqOjo9/phhjLVVwAMDZJLS0tXtM073dywp9CKqbrZ2B+08UoL57iVDNS9Q604dXWm/Be9AFYIuVkU6tM0zwDgOPVBmO5iJcBMjY5RES3EtHHnWqgtmw2ls/9DWbXfxKF3gqnmpGu0FuBprrj0Vh3HLpi76J/uN2ppqaXlZVNjcVi9zvVAGO5jAsAxiZhbJOfrzkRu9BbgcUHfRdHzfwBSguDTjSRFsUFtTjIOBMlhXVo730VKWvYiWYO9vv9Fm8WxNjE8RAAYxOk6/oJAB4BIG+d3ZjG2mNxTPO1KPRVyg7tqsGRbvzzrSuwZcfTToS3iGhZJBJ5yongjOUqLgAYm4C6urqAx+N5HaOn10mjKB7Mb/oiDp36Janr9zOJgMCbW/6IFzb9HJZIyA7f4fV6523ZsiUqOzBjuYqHABgbP7WsrOxBIpI6Dd9fZODk+bdiuvYREOVuTU6g0c2Kqhci3LVa9v4BpZZlzY3FYivBRwkzNi5cADA2Trqu/5CIPiszZm3ZbHzksJWoKJkqM2xGKy3UcGDwVES6X8DASKfM0FN5PgBj45e7rxuMSaTr+iIAz0HiuL9RdQSWz/0tfJ4SWSGzykgyjkde+yLMnrUyw6aIaEkkEnlBZlDGchH3ADC2f6rf738AgCYrYFPdMiyf+5v/O5AnH6mKD9P1U9Hbvxk9/e/LCqsAODIQCNzW3d3t6CYEjGU7LgAY2w9N075GROfJijc1cCJOOOR6qIpXVsisRaSiKXACevvfR0//B7LC1iQSiSQPBTC2bzwEwNg+1NbWBr1e7zsAymXE0ysPxyktt0NVfDLC5QxLJPDwq59HuGu1rJDDiqLMDofD0roWGMs1ubneiDFJvF7vryDp4V9dOgMnzfsffvjvgUJenHjIr1FbJu08pYJUKnWtrGCM5SLuAWBsLwzDOEYIIWVzGX+RgTMPvxdFvmoZ4XLWwHAn/rr2LMSH5CznF0IcFY1Gn5MSjLEcwz0AjO2FEOIaGXEUxYPj51zHD/9xKC6oxYmH3ACFPFLiERH3AjC2FzwJkLE9MAzjZADfkhFr4fRvYVrQsQMDc05JYRCq4kW4e42McA1+v39NLBZrlRGMsVzCPQCM7YFlWd+XEaex9lgcPOV8GaHyytymi9BQs1RWuKtkBWIsl3ABwNhuNE1bQkQL7MYp9FbgmOZrQTzVZsIIhGNn/wwFXinzL480DGOhjECM5RIuABjbDRFdKiPOEQdemnOn+qVTka8KRxz4DVnhpHxPGcslXAAwtotAINAE4BTbccrn4SDjLAkZ5beZxtmoKzvYdhwhxOmapk2RkBJjOYMLAMZ2oSjKhbD5e6GQiqNmXZWzx/qmE5GCo2b9AArZnq+sEBFPxmBsF3yHYuxfPDIeEtP1M1DjnyUjH4bRExOnBU+VEeoC8Monxv4PFwCMjQkGg8sA6HZiKKRiXtPnJWXEPjR/6hdk9KjU67p+jIx8GMsFXAAwNkZRlLPtxjggeBIqihslZMN2VVkyFVPrTpARyvb3mLFcwQUAYwCam5t9AE6zE4NAmN/0BUkZsd21TL1ExpLKM8e+14zlPS4AGAPQ09OzFICtNXv1NUtQVTpdUkZsd9X+gxCqPtJumMre3l7bQRjLBVwAMAaAiGzv1TtD/6iMVNg+zNDPsB1DCLFcQiqMZT0uABgDIIQ4yc71Pk8pGuuOlZUO24umwDL4PKV2w9j6XjOWK7gAYHmvvr5eBzDDToxpwZPhUQolZcT2xqMUYmrgRLth5tTW1gZl5MNYNuMCgOU9y7JsjwkfqNmaP8gmYIZ+uu0YHo9nkYRUGMtqXAAwBtgqAHyeEgTL58nKhe1HsLwFPk+J3TA8EZDlPS4AWN4TQhxm53qtcgEUxSMrHbYfiuJBsOJQWzFknPbIWLbjAoDlOwIw206AUBWfNJtuRtURdkPMAficZpbfuABgea2+vn4qgDI7MSQ8jNgESfjMy3Vdr5eRC2PZigsAltcsy5pp53qfp5Q3/3FBjX8mvJ5iWzGEEHxiE8trXACwvCaEaLJzfUXJVD721wVECiqKbX3roCiKvQCMZTm+c7G8JoRotHN9RQk/Q9xi97O3+71nLNtxAcDyXYOdi/nkP/fY7QEA0CghDcayFhcALK8pilJr5/qKkgNkpcImqKJkqt0QNTLyYCxbcQHA8l21nYtLCupk5cEmqLRQsxuCCwCW17gAYHlNCGGrAJBwMA2bJK/93QBtfe8Zy3ZcALB8Z2stmVe1/RBik+RV7S0DhM3vPWPZjgsAlu98ti7mHgDX+FTbn32BjDwYy1ZcALB8Z6sAsLsZDZs8CUMAXACwvMYnmPwnCgQCTR6PZ6YQYqoQopGI6omoDkD12JhxIUYfHCUABIBeABYR9QkhRgBEiSgshIgAMIUQ76mq+mY4HI649rdieyPcToC5JuV2Aoy5Ke8LgPr6en3sPPgjx06FmwPAL8Toc4Fo9LyQD//3HhCAyrGv+XBS0UG7fj0RwbIs6LreDWA9Ea0XQjyjKMqz4XC424G/Fhu/Ydj4PRhJ9qPQWyExHTZeiWS/3RC2AzCWzfKuAGhubvb19PQsFUKcREQrUqnUjDQ2XwXgGCHEMQC+blmWpev6eiHEP4UQD7a3tz8PfitJtyGM9uRMSiIZ5wLAJSOpuN0QXACwvJYvBYBH07Tjiejsnp6e0wFUfPhm7zIFwDwimkdE39B1vUMIcZ+iKPdGIpGnwcVAOgzZuTiRGpCVB5sgCZ89FwAsr+V0ARAIBJoURbmQiM4HoLudzzgEiOgLQogv6Lq+jYhu8Xg8t2/ZsiXqdmI5bAcAY7IXjyRtv4WySRpJcA8AY3bk5CoATdOW6Lp+v6qq7xPRd5AdD//d1QshfpRIJLbouv6/hmEsdDuhHNVh5+L+YVuXMxv6h9ttXS+E2CkpFcayUk4VAIZhnKxp2loiehbAR5Abfz8vgI8JIdbouv64pmlL3E4olxCRrSd4b3+rrFTYBNn97Iloi6RUGMtKufCAhGEYx+i6vkYIsYqIFridj4OOJ6JnNU37p2EYR7idTC4YW6o5ab39m2Wlwiaod8D2Z8/fPJbXsroAmDJlimYYxh+FEE8CyJsuciI6eqxH4H91Xbd1nC3De3YulvAQYpPUE7fdA8DfPJbXsrUA8Gia9vVEIvGOEOLTGF2Ln28IwMcAbNA07cqWlhav2wllIyGEvQKgvxVCWLLSYeMkhIW+wTZbMSzL4gKA5bWsKwB0XV+k6/orRPRLAGVu55MBSonommg0ujYUCs1xO5lsk0wmbRUAI8l+dMXflZUOG6cdsY1IJO0tA1QUhQsAlteyqQBQdV3/AYBnARzici6ZaJ5lWet0Xf8p9waMX2dnZzsAW8ssI90vSsqGjVek+wW7IboikQhvzc3yWlYUAPX19bqmaU8AuAqA6nY+GcwL4PJoNPrPUCg06bXteWidnYsjXbYfRmyCIt1r7YZ4EXwOBMtzGV8AGIZxbCqVeoWIjnY7lyxypGVZr+u6vsztRLKErQIg2vsyLJGUlQvbD8tKor33FVsxiIi7bVjey+QCgHRdv1oI8TgAze1kslANgL/run6Z24lkqkAgUKdp2tcAnGUnzkiyH+29r0rKiu1PtPdljNg8CEgI8ZKkdBjLWpm6FbCq6/rNAC50O5Es5wHwc13XZ2ma9vl169Yl3E7IbY2NjYUjIyPLAHwawOkYHTaxbZP5APTKXN6CInO8a95vN4Tw+XxcALC8l3HL53RdLxZC3ENEK9zMw1tQipLqKSipaUJpTRNKqqagsDwIj68YqrcQ3qJyeLxFAIBkYhCJwT6kRgaRTAxiqK8d8a429O/YjP6uNvR3bUFi2PU941cBONs0zXw8vUYJBoNLFEX5DIAzAZTLbsDnKcVnj14Dj1IoOzTbRTI1iD88s8huD8A60zQPlZUTY9kqo3oAQqFQlWVZq4go7Zv6eAtKUTmlBTVNh6O6aQH8dQeCaHwjJF7VC2/hLisSQ/++SEEIC7GOTehqewk7Wteie+s6JIfTfg7JKQCeCoVCK8LhcHe6G3eDrusHCSHOJaJzAUxxsq2RZBybO57AgdopTjaT91q3P267+x/AgzJyYSzbZUwPQCgUMizLegxAc7ra9BSUQm8+EfrBp6Cyfi4UJT31kGUl0bvtdYTXP4j2tx9Pd+/AOp/Pd3xbW1tvOhtNl2AwWKsoyjlE9GkhxGHpbLu+ZglOmX97OpvMOw+tOx/hrtW2YhDRvEgk8rqklBjLWhlRAIy9+T+LdDz8iVB3wJEwDjkNgYOOheopcLzJfUklh9HxzpOIrH8I2z9YDQjnVyYR0csFBQXLWltb+xxvLA0aGxsLE4nEqWO7Qi6HpHH9iSIQPrboQVSXznCj+Zy3I7YR975wOoS91XtbTdN0tDeIsWzhegGg63oxgCfg8F7+pKjQZp2IaUs+B3/dgU42NWmxjk1477lb0f72P9KxveyLiURiWWdnp+uTEyaJNE1bTESfwegs/gq3EwKAacEVWHbwr9xOIyc9tv4raO14zG6YG03T/IqMfBjLdq4WAC0tLV7TNO93csIfKSpCh5yGAxZ/DiVV2XFuTn/XFrz//K2IvLEKwko52dQq0zRPB+BoIzIZhjFdCHEuRmfxN7qczn9QSMXZRz6CiuJGt1PJKT39H+DuNSfLKIwXm6ZpbwyBsRzh5q56pCjKHbC5BntfKkOH4NBzbkBDy8fgK5I+8dsxvuIKBA86FnXTl2Jn+zsYim13qqnpfr+/KhaLPeJUAzIYhlHt9/sv8Pv9NwD4GYClyJA3/t0JCCSS/WiqO97tVHLKmk3Xoiv2jq0YRPSWaZpXSkqJsaznWgGg6/rVABzpivMVVWDWSVegecW3UeivdaKJtCj016J+3hko9NehZ9vrsJLDTjSzoLS0tDcej9veW1WmadOmFRQUFJxeVlZ2LYCbAJwKIORyWuPSE9+EKbXHoKSgzu1UcsL2vjew+t2fQMLOvT+OxWK8/p+xMa4MAei6fgKAR+DAToR104/GIR+5Gr7iStmhXTXS3431D3wP29971onwKcuyjmtvb3/GieATQLquHzm2dO/jALL2m1hXfgg+uuDucS8lZXsmhIW/vfQxbO97026oQY/HY2zdurVHRl6M5YK09wDU19frQojHAJTKjEuKBzOXfQOzl18B1VckM3RGUH1FMGavgMdXhO62l2VPElSI6ITi4uKV/f39ad+gIBQKTSstLf1aWVnZbQC+SUSHAsjqb2L/cAdKCutQWzbb7VSy2tvhu/B2+G4Zof4cDofvkhGIsVyR7h4AVdO0J2Qf7FNUoWP+mb9ARehgmWEzVs+21/HqvZdhaGe77NCPm6a5HIDjSxBCoVCVEOLssaV7ad/4KR0KvOX4xJGPochX5XYqWWlwpAt/ef5EDCd32g1lKYoyNxwO2+5GYCyXpLUHQNf1HxLRZ2XGLNdm4ojzfo/SmkaZYTNaUXkQ+pwV6Nq8FsPxHTJDH+D3+4disdjzMoN+aGxc/7SysrJrhRA3AzgNQL0TbWWClDWMnvj7mKadAnJ/xW1WEcLCP974Grrjm2zHIqK/RSKRGyWkxVhOSVsBoOv6IgB3QGKvQ3XTAiz41M1ZNcNfFo+vGPqcFegNv4HBXlNm6MV+v/+vsVhMWmWh6/oiv99/ZSKRuIOIzgNwENxdgZI2fQNt8KrFCFbMdzuVrPLa5pvxtpwee0FEn4zFYh0ygjGWS9J1E/b4/f4HIPFY3+DMZTj07F9B9Wb1ULEtqscHfc5J6N+xGfHOVllhPQDmxWKx38PGtOv6+voDSktLv+r3+28DcBmAw5Ad4/oCwGohxE+IqADAAXYDmt1rEapeiNJCPtV6PKI9r+Cfb18ha57L/aZp3iAjEGO5Ji39kpqmfZ2IfikrXnDmMsw/6xcgJS9eIvdLWCm89tfLEH37cZlhv2qa5q8nckFDQ0NlIpH4OBF9GsAiZMBOkxPwHoCVqVTqzo6Ojs0AEAqF5liW9RokFMqlhRrOPPxeFBdk77LUdBgY3o57XzwT/cNSXtgtIpofiUTWywjGWK5x/AZdW1sb9Hq970DSEazVjYdhwbk3QVF9MsLlDJFK4KU/fwk7Wl+QFTKWSCSmd3Z27m+moarr+jFE9BkhxJkAimUlkAa9RPSQEOKPpmk+iT30eOi6/jsA58torKp0Os5Y8Bf4PH4Z4XLOSDKOB17+FHbENsoK+VvTNC+RFYyxXON4AaDr+l0AzpYRyx+YjkXn/R6eQr6B7kliOI61f7gAfVE5N1AhxE3RaPSLe/r/NE1rGduH/xwA2bTjzTCAx4nojxUVFQ9s2LBhZF9fPFbAboSknQf1ygU4peV2qIq7h1BlGksk8PCrFyHctUZWyC4AB5mmKXWWLGO5xNECwDCMY4QQT8mIVVSh48jP/QUFJbykal+G4juw+tZPyFoimLQsa257e/sGAAgEAk0ej+fcsb34p8toIE0EgDVEtFJV1bsnuhmMrutfBjCh4ZB9mRo4EcsO/hUU4iEsALBECo+/8TW0dvxDZtgLTdP8ncyAjOUaRwsAXdfXQMIab1I8WHT+H/Jmnb9dPdtew4u/vwCWlZQR7h9CiHvHxvUXI7vG9T8AcKeqqiu3bdv2gY04qq7rLwI4VFJeOCBwIo6bcx1UJb+HslLWMJ5485uyH/4vmKa5GGnYz4KxbObYzdwwjJOFEKtkxJp5wqWYulDq9gE574PVt+OdJ/LyWNr9jutPhqZpM4noVQCFMuIBo8MBJ827CT6P1E0xs0YiOYBH138J4S6ph/MNKYqygDf9YWz/HOuDLC0tXUlEht04ddOPxuzlVwCUTS+e7quqn4feyFsY6N7qdirpMALgISHEt0tKSi7esmXLvbFYTNq6SACIx+M7/H5/AsAyWTFjQxFs2/EsmuqOh9dTIitsVhgY6cSDL38aHX2vSY1LRF+NRCIPSw3KWI5y5KmqadoSIrJ9ao2vqAJLv/xgzh3sky4j/d14+jenITHY53YqTnkBwEpFUe4Kh8PdaWhPNQzjSSHEUplBSws1LDv4l3mzWVC05xU8/sZ/yVrqt6sHTdM8HZJ6fRjLdY70AJSVlf0awAy7cWaddAWqGvLjpugE1VcEb2Eptm9y5ARBt2wDcBMRXWia5s9jsdjLO3fuHExT26KoqOgRRVE+BUDaUpSRZBybovdDCAt65WGgHO3tEhB4c8sf8eSbl2IkGZMdfnsymVzR398flx2YsVwl/U4TCASaVFV9HzaP+q0MHYKFF/yRj1O1SQgLq2/7FPrMt9xOxY4eIrpHCHGnaZqr4fIbnmEYx42daCm9gG6oWYpjZ/8s5w4QGhzpwlNvXY6tO5wpRono5ZGRkWM7Ozu5AGBsnKTfwMrKyi4lIltdpKSoOPSc61Hoz6bl5ZmJiFCuzcK21+8DRFb1jKYAPEVEPwTwOdM074vFYhkxoSEWi20uKyuLAzhRduy+gS14O3w3PEohasvnZH0BLISF99ofwCOvfxFdsXedbMpQVfXogoKCewYGBva5twNjbJTsAsBTVlb2B9jsHq2fezoaWj4uKSVW6K9Ff/dWxDrsn6yWBmsB/AzAeaZp3hyLxdbHYrGE20ntLhaLveD3+0MApI9RpawRbOt6Dtt2PIfaslkoKcjOQnh73xt4bP2X8NbWPyGZGkpHk/Wqqi4pLCzkIoCxcZA6BKBp2nIiesRODFJULP3SgyipapCVFgMQ37EZz/7P6bIOWJGtTQixUlGUOyORSFZUKQDQ0tLijUajqwCc4FQbCqmYFjwV86d+AZUlU51qRqqe/g/w2uabsSn6oFs/b88nEomTeDiAsX2TWgDouv57ALYW7OuzV2DemT+TkxD7N6/e801E35a64YodfUT0oOz1+umm63oxgMcwukmSY4gUNNQsxaFTv4y68jlONjVp3fFNeL3tNrwXfQiWSLmdzpqRkZHlO3bskD7bkLFcIa0AaG5u9vX09HTAzp7pRDjqC3+Fv+5AWWmxXezseBfP3fwxN+cCJAA8SkR3er3eh9ra2tLSL+y0UChUZVnWPwE4vlUlgRCqPhIz9DPQFFgGjyJtX6JJSaYG0br9cbxr3odI1xqIzKrjuCeAsX2QVgDour4MgK3Xy7ppi3HYp34rKSO2Jy+tvBidH0g7cGVciOhlIcSdlmXd1d7e3pnWxtNE1/UaAI8DmJuuNn2eUkwNnIgZ+ukIlrdAUTxpadcSSUR7Xsa75v3YvP0fGEn2p6XdSeIigLG9kFYAaJr2/4jov+zEmH/WL6A1L5eVEtuDyJsP4/W/XZGOprYIIVYS0UrTNN9JR4NuG+sJeAwSzwwYL6+nGFrFYQhVL4ReeThq/DOlrSAQwsKO2EZEul9EpPtFRHtfRiI5ICV2mnARwNgeyOwB2AjgoMle7ykoxfGXPg3Vw8ekOimVGMKT1x2DxLAj98I+AH+1LOuP7e3tzyEPD2Opqanx+3y+e+HgxMDx8HqKUVHchIqSprF/TkVpoQavWgyvWowCbzm8nmIAo3vyDyf6kEgNYCTZj/7hdvT2t6KnvxV9A23oHdicbQ/8PeEigLHdSCkA6uvr9VQqFbETo2H+mZhz6g9kpMP2Y/0D30P49ftlhUtidBLcnYqiPBgOh9O1K1/Gamlp8ZqmeRsRfcbtXNi/4SKAsV1I6SO0LOtIuzH0g0+RkQobh9Ahp8kIs0EI8fVUKmWYpnmKaZp388N/1Lp16xIY3bKYZZbFXq/3kdra2vw8fpGx3cjaZmyRnYu9BaWorE/b3Km8V9UwD54C26fP3RONRq/v6OjYLiOnXGIYxiFE9C2388hyUSJ62YG4XAQwNkZKASCEWGDn+sop6ZvBzABSPKist72BXYuMXHKQRwhxGwCv24lksQctyzpkZGTkWADPOxCfiwDGIKcAIACz7QSoaTpcQhpsImqabNVsABcAe6Tr+jfgwiqAHDEkhPi6aZqnt7e3d3Z2dsZTqdRyIcTTDrS12Ov1PlZTUyPtVEfGso3tAiAQCDQBKLMTo7rxMLtpsAmqtl906cFgsFZGLrkiFApNA/ADt/PIUi8IIeZHo9HrscuukB0dHf3JZPJUONMTsMjn8/2dewJYvrJdAHg8nll2rvcWlMIfmG43DTZBZcEZ8PiKbcVQFIW/cf9CqVTqVgBFbieSZToBXGia5pHRaHTjHr+gszOeSCROAg8HMCaV7QJACNFk5/qSmsasP/I0GxEpKKmeYjMG8Z7NYwzDuJiIjnY7jyxiEdGdAGaZpvk77OcsCB4OYEw+GQVAo53rS6ptXc5sKKm2VbsBAPcAAAiFQoYQ4qdu55ElBID7iGh+JBL5jGmaO8Z7IQ8HMCaXjFdvW+f2cgHgntKaRlvXW5ZlyMkku1mW9VsA5ZLCvYjcyAn8XAAAIABJREFU3EHRIqK/EtE80zQ/GolE1k8mCA8HMCaPjAKgxs7FpVwAuMZu8UVEATmZZC9d188BcKqMWET0iGmaC4lophDiJgC5sLHSIIA/KIoyNxKJnDXZB/+uuAhgTA7bBYCiKLYKgMKyvH+GuKaoPGg3RJ2MPLLV2AmA10sKFxNCfAEAIpHIpmg0+kVFUUIAvgbgDUltpA0RvQXgqz6fTzdN87xwOPymzPhcBDBmn4w5ANV2rpewIx2bJI/P9mdvq/jLdkT0S8grgq40TXPrrv8hHA53m6Z5g2mahwghDgNwHYDNktpzwhYANwJYHIlE5pim+eu2trZepxrjIoAxe2Rsv2dr2ZNqcykamzwJn33eLnkLBoMnCSHOlRTuedM0f7uvL4hGo68AeAXApZqmtRDRqQCOB3A45PweT4YA8CqAB4nowUgk8nq6E+js7IzX1tae5PV6HwGwWHL4D4sAPkCI5SQZNw6frQS4B8A1Ej77Qhl5ZJuamhq/oig3SQo3BOAiTGDiXzQaXQdgHYAf1NTU+AsKCpaObcd9GEZ3IXSqZ2YHgLVEtFYIsdbn873k5Bv+eHERwNjkyCgACuxc7LXfDc0miQuAyfH5fNfC5uqXDwkhfhSNRt+Z7PU7duyIAVg19gfA6PHcQojpqVTqQCI6kIg0IUQdgCCASgClGB3+K8focc4xAHGMFiM7iShuWdYWImolos2WZW1WFGVzJBIJT/5v6iwuAhibOD6Bh9mRi8vV9skwjIVCiC9KCveGruu/iEajksKN2rZtmwnABPC01MAZrrOzMx4IBJYrirLKgU2ZPtwsaPlY0cVY1pOxDHDEzsXJkQEJKbDJSA732w2RV29D06ZNKxg76U/G701SCHHBunXrEhJisTEdHR39lmWd4tCOgYt8Pt+jvGMgyxXuFwD2H0JskiR89nn1zRscHLwKgK2zL3bx32Nj+UwyLgIYGx8ZBYCth0ByJK+eIRklZb/3JW++eYZhzBVCXCYp3CZFUa6WFIvtAW8bzNj+2S4AiKjbzvXcA+CexLDtHvx8GQLwCCFuh5w5M0IIcVE4HM6FXf4yGu8TwNi+2S4ALMsa92EeezK0s8NuCmySJHz2O2Xkkel0Xf8mgPkyYgkhbo5Go8/KiMX2j4sAxvZORg9Ap53r411tdlNgk9Rv/7PfIiGNjGYYxnQAV0kKFx4eHr5cUiw2TlwEMLZnMuYAbN3/l+ydhIcQm6T4Dnu7yhJRq6RUMpUihLgV8nY8/HJ3d3de9Jpkms7OzngqlVru0MTAD5cI8sRAllVkFAC23gL7bT6E2OTFd7TZul4IkdMFgK7rXwBwlKRwfzJN8wFJsdgk8OoAxv6djCEAWw+BeFcbhMi7/WRcJ4SFgW57Pfi53ANgGEYIwLWSwu2wLOu/JMViNvDqAMb+xXYBkEwm37Z1/XA/Yh2b7KbBJmhn+7u2N2FKJpM5WwAIIX4LoExSuK+1t7fbmivD5OE5AYyNsl0AdHR0tMHmbPCutpfspsEmqGvzi3ZDmB0dHdtl5JJpNE37FIBTZMQSQvzdNM0/y4jF5OE5AYzJmQMgALxpJ8CO1rUS0mAT0dX2sq3rich2BZGJdF2vIaJfSgq3k4i+ICkWk4yHA1i+k1EAgIhsPU26t66DsJIyUmHjYFlJdG991VYMIcQLktLJNDcAqJURiIguN01zm4xYzBncE8DymZQCAMBqOxcnh/vRs+11Samw/enesk7GDow51wNgGMbJAD4hKdyzkUjkFkmxmIO4J4DlKykFgMfjsVUAAEB4/YMyUmHjEHnjIbshEoqi5NRBNlVVVWVjE/9kGCKii5CHxyVnK54YyPKRlAJgy5YtUQAb7cRof/txpJLDMtJh+5BKDKF94xN2w7yYa3vZFxYW/hRAvaRwP4xEIry0JctwEcDyjawhAAghHrVzfWI4jo53npKVDtuL9o1PyOj+z6nuGk3TjgIga7Leek3TrpMUi6UZzwlg+URaAUBEj9iNEV7PG6U5TcZQCxHlTAEQCoWKiOhWACQhXBLA+evWrUtIiMVcwnMCWL6QVgBomvY0AFtHA3d+sIY3BXLQzo53scP++v+NudS9bVnWVQCmy4hFRD83TfM1GbGYu7gngOUDaQXA2FuPvVd4IfD+87fJSYj9h/eeuRkQwm6YnHn7NwzjEADfkBRuk9fr/ZGkWCwD8NkBLNdJKwAAQAhxt90Y0bf/gf6unD9lNu3ina3oeOdJ23GEEIdrmnaohJTc5hFC3AHAKyGWBeDCtra2IQmxWAbh4QCWy6QWANFo9EkAETsxhJXC+8/fKikj9qH3n79NyqFLRHQ0Eb2s6/pD2VwIaJp2GYB5ksLdZJqmEw8IlgF4dQDLVVILAADJsbcqWyLrH0Kf+ZaMfBiAPvNtmG/9XXbYU8YKgcdDodAC2cGdZBjGdCL6vqRwW0dGRq6QFItlKJ4TwHKRjJnP/yYYDDYqivIBbBYXFcYcLLpwJYhk1yj5RQgLa277JHrNDU43tUoI8cNoNPqK0w3ZpOi6/gyAxVKCKcrJ4XBYenVlh67rDQBmADhICNGoKEqdEEIHEARQgtFTDglAxdgl/QBGMLqBUReALiHEdgBbAbQR0eZkMvn22MFftieRZLPa2tpSr9f7CCT9/Ozm+UQicVJnZ2fcgdiM/QfpBQAA6Lp+H4DT7caZc8r30dDyMQkZ5a8tr9yNtx7+cTqbzOhCQNf1SwD8RkYsIloZiUQ+LSPWZNXV1QU8Hs9CAEcCWAjgYABOvUnuBPDm2Nkfqz0ez+qxTcDyChcBLFc4VQAsBvCc3TjeonIc/aUH4SupkpBV/hnu78YzN56KxJCt05onK+MKgbE347cg5wG5HUCzaZo7JMSaCE8oFFpsWdYKACsANKe5/d1tFEI8QkSPVlZWPrNhw4YRl/NJCy4CWC5wpAAAAF3XXwBwhN04dQcehcM+cSNAjqWak4Sw8Mqfv4Tt77s+Ny1jCgFN0x4mohWSwn3CNM27JMXaH8UwjKOFEJ8GcAaA8jS1O1E9AO4XQtw9NiE4p4/45CKAZTvHnqqapi2XsTsgAMxc9g1MXXS+jFB54/3nbsO7T13vdhq7crUQ0DTtXCK6U1K4h0zTPE1SrL3Sdb2BiL4w9uAPOd2eZBEhxB1CiNvb29vb3E7GKVwEsGzm6Gu1ruvPY3Rs0hZSPFh43h2orJ8rIavc171lHdb+8XOwrIx8AUt7IRAIBOpUVd0AoEZCuD5FUZrD4bCt5a77omnaEgBfJaLTAXicaidNLIxuHnVdri6V5CKAZStHp9hblvUdGXGElcSr916GoXi6h1uzz3CsE6/99VuZ+vAH/rV8MG37CKiqej3kPPwhhLjcqYe/ruvLdF1fQ0TPEtFZyP6HPzB6jzkdwHO6rr+gadpytxOSjfcJYNnK8YF1Xdf/BOCTMmKVBQ/CEefdAW8B/y7sSXI4jjV3fDbbzlNwtEdA1/VTIWn7YiHE09Fo9FhIXgqnadpRRPRjAEtkxs1gayzL+nZ7e/szbiciE/cEsGzjeAFQW1sb9Hq9G/GvNce2VE05FIefezMUj09GuJwhUgm89OdLsKPV9mE/bnlCUZTvhMPhl2QFrKqqKissLNwAOePng4qiHBIOh9+TEAsAYBhGCMA1Y2P8+WgVgEtM09zmdiKyBAKBEkVRVhHR0Q6EXzMyMrJ8x44dMQdiszykOt3AwMBA3O/3DwI4SUa8wT4T8R2boc08njcJGiOsFF7962XY/t6zbqdix1QhxOf8fv+hpaWl78XjcdNuwIqKiuuJ6FgZyQH4biQSeUhGoMbGxsLi4uLvAbgLQIuMmFlqOoALSktLB+Px+CvIgU2G+vv7E0VFRX9VVfUoAA2Sw9erqrqksLDwnoGBgbxYbsmcla61daqu668AkDaLT5u1DHM/+lMoan73BFjJEbz2t8vRvvEJt1ORSQB42M7QQDAYXKooyj8h52d8nWmaR0DCsrZQKHS4ZVl3AJhpP62c8joRXRKJRF5wOxEZeDiAZQPHewDGiLKysjcAnA9JRUe8sxU9W19DYOZxUPN0OCA5HMfLf/kSOuWu9U8CeApAE9JXIO6OAEwnoosm0yMQCoWKAPwdQLWEXBJEdEosFrO14920adMKCgsLfyyEuB1AnYS8ck0QwPl+v1+JxWLPIct7AwYGBkYKCwvvcagnoEFV1aO4J4DZla4CALFYLOz3+1UAS2XFHOw1sX3TswgcdAw8BSWywmaFofgOrL3zIvSG35Aal4i+b5rmReXl5fcJIWoAzIL7hcDn/X7/4vLy8nd37ty53xn4paWl1wA4VUYCQohrTdP8i50Yuq43JBKJvwM4Bw6vvMlyBODosrKypRUVFf/YuXNnVo91DwwMjBQXF/8vES0iokbJ4RtUVT26oKCAiwA2aem+sSu6rj8G4HiZQQvLAph35s9R1TBfZtiM1We+hVfvuRQDvXJXoxHRM5FI5DgAqQ//WygUOtiyrO8COAvuFQK72udkQcMw5gohXgLgldDWuz6fb25bW9vQZAOMrUL4A4BKCfnkk04hxGei0eijbidiF08MZJkqbT0AY0RVVdUTlmWdC0DaWr7kcD/MN1ZB8fhQVT83d7cNFgLvP3871t93JUYG+2RH3+71epf19fX928EBO3fu7IjFYveUlpY+TEQ6gAPhbiGw18mCLS0t3lgs9ncAuoR2LABnbNu2bfMkrydd168G8FsARRLyyTclRPTJsSGBrF4uyBMDWaZKdwGAvr6+uN/vfx3AuZD4IBHCwo7WF9EbeQu1ByyE6sute+5wfzdeu+eb2LruHghhyQ5vCSE+Fg6HX9/bF8TjcTMWi/0lQwqBPc4RUBTlSkjacwLAb0zTvHkyF46N9/8BwJeRGb0m2YoAHO33+6fEYrGHMVqUZSWeE8AykWs3J13XfwDgKidie4vKMePYr6Kh5aysXyoohIWt6+7Bu0/e4NipfkKI/4pGo7+ayDWaph1KRFcBOBnuP+QEgMcAHAOgQEK8LSMjI3Mm063a0NBQmUwm7wdwlIQ8Jq3E40F9YTHqi4owpagEocIi1PkKUaSqKFQU+D1eFKmj9f9gKoVYMoFBy8JQKoXtI0PYNjiALYMDCA8NYtvQAPqTru8suQrA2aZpDridiB28OoBlEjdv3KTr+q0ALnSqgXJtJmaf/D1UGHOcasJRfdGNeOvvP5Y+0W9XRHRLJBK5eLLXZ+AcAduEECdNZuw5FApVWZb1GIC0bHG8q0JVRXNpGQ4tr0JLeSUOLCmFInEozBwaxCt9PVjX141XensQT6W/IBBCvEREJ7twBLNUPCeAZQq3b9geXdfvA3CKUw2QokKfvQLTllyE0pomp5qRKt7Zig9W34bIGw870d2/q1WmaZ6OXSb9TdZYj8D3Mfq9dPvnatKEEH+MRqOfneh1YztePgGg2YG09qhEVXFMTQAn1AQw218ONU1zX1JC4M1YHx7rbMcz3Z3p7h3YoKrqCdu2bbO9UZSbuCeAZQLXb9S6rhcDeBzAIifbIVIQnLUM05ZchLLADCebmrSd7e/gvWdvQcc7Tzr94AeAtYlE4njZNwlN01rGhgaysRDoIKLmSCTSNZGL6urqAh6P51mM7mznKAKwoKIaJ9YGsbiqBgWKu0Ncw5aF57s78VhnB17q7UrX4v0NHo9nydatW3vS05wzuAhgbsuIG/RY1+mzSMfbExFqpy6EcchpCM48HqpHxpDx5KUSQ2jf+ATC6x/Ejs0vAiItt9AXCwsLl7e2tkpfSvChbCwEiOjsSCTyvxO5Zuy8gacBzHMmq1EqEY6ursO5xhRMLc7MPS8+GOjHynAbnu7uhOX8z/FqACfwnIB94iKA7VPG3Jjr6+v1VCr1D6SxC9VbUIrAzOMROuQ0VDbMg6Kk5/RVYSXRtWUdIusfRPs7TyI53J+WdsesGRoaOqm7u9uZGYW7yaJC4IGx4ZBxa2xsLBweHn7EobFcAKMP/hNrg/iUMQWhwuxY2bJtaAArw1vw+I4OpJwtBFaZpnkGJGzR7CYuAphbMuqGPDaD+iEAR6a7bY+vGJUNLaiZejiqGxegLDhD2goCISzsbH8XXZvXoqvtJXRvWYfkiCsvLs+NjIyc7MYEoQwvBPpUVZ01wXFl0nX9LgAfdyqpZn8ZvtE0A9NKsvP46039Mfy/1k3YGHe01rzDNM0LkeVbB3MRwNyQaTfiD+cE3AVJW7lOlsdXjJLqKSipbkJpTSNKqhtRVB6E6iuGx1cMb2EZPL5iAEByZACJoZ1IjgwgOdyPoZ0d6O9qQ3zHZvR3taG/a4tbD/xd3Z9Kpc7t6OhIa3fD7jKxECCiayKRyHcmco2mad8mop84kU+Zx4uLG6ZiRZ0mdSa/GywhsGp7FLds/QAx5yYLXmWa5tVOBU8XLgJYumXq3cUztkTwPLcTyRG/ME3zCmTQRioZVggIAKvGTh9ct78vNgzjFCHEA3BgX/9FldW44oCZKPfK2Mk4c/QmErj2/Y14sXdC8yvHyyKiZZFI5CkngqcTFwEgTdMaVFVtsiyrCUATETUJIZoAFAKowOheHyUA/AA8APoBjAAYIqIuAF1CiO0AtgJoI6LNyWTy7Y6OjjZkeU+RbG7fePeFdF3/HoDvw4UdC3NEAsAlpmne5nYie5OhhcDVezuGOBAITFVV9VUA5TIbVolw8ZQD8HGt3vUPwSkCwN3mVtyytdWJuQHtiURiXmdnZ7vswOmWT0WAYRjVRHS4ZVkLABw+9sepczN2AniTiF4GsNrj8azesmWLrVM+s13G32sMwzhWCPEnjB4XyiZgMl3bbsnAQuDhsR6BXQsBj67rzwJYKLOxYEEhrprejFmlZTLDZqy3Yn344aYN2D4yLDv0k6ZpnoAM6umarBwuAkjTtPlE9BGMDvPOdSGHXW0UQjxCRI9WVlY+s2HDhrzaStntG+24jG2yshLAcW7nkmW2+3y+GW1tbb1uJzJemVwIOLF99fQSP34+82BUen0yw2a8rpFhfOudN/B+v/RnUE7MBwByqwjQNG0JEX0Cow/9UDranIQeAPcLIe6ORqNPIstXl4yH2zfYiVB0Xf8ueEhgon5tmuZX3U5iojKwEHgSwNEYHXOUYn5ZJX5y0GwUq+lZfppp+pNJfOfdN/HaTqn1aYqIlkQikRdkBnVLNhcBuq7XENFnhBAXATjIiTYcFBFC3CGEuL29vb3N7WSc4vaNdcIMw1gohLgVadwvIMsliejQSCSy3u1EJiPDCgFpllbV4nvTZ8Gb5YdV2ZUQFn703kY807VdZtgNlZWV83OlOzfbioCx39lvAvgo5BzO5SYLwIMArjNN83m3k5Et696kY7FYuKGh4bahoaEUgCMg8Y0sRykAmmOx2O/dTmQy4vF4tLy8/AMhxAVwYNa9G5ZW1eKq6c3w5PnDHxid/HhUVS3aBgewZVDaCtW6oaGhVCwWe0ZWQDdly1HCmqa1lJWV3UxE/w1gDnLj3kwY7b24wO/3Ly8tLY3E4/H33U5Klqx+owoGg41E9AsiOsvtXDKdEOLcaDT6J7fzmKjm5mZfT0/PKxi9oWS9+WWV+Pmsg/P+zX93CWHh0rfX43V5wwFDqVRqVkdHx2ZZAd2WqT0BudpLtw9rLMv6dnt7e9YXmFnXA7CreDzeG4/H7yktLX2KiKYBmOJ2TpmKiI4oKCi41W6Vn25er/c7AM52Ow8ZPpzwV6hm9a+dI1QiHFVdh7W9XehOSPkR9RCREY/H75ERLBNkWk+AYRjVfr//BiL6H4y+JefDwx8A6onoPL/fP72qquqFvr6+jFhSORk5cSeKx+NbY7HYHX6/fw2AqZD/y5EL/KqqemOx2ONuJzJewWBwFhGtRA50JQYLCnF98zyU5dgGPzL5FAWLK2vwz67t6E/ZPqEaRDSrtLT0qXg8vlVCehkhQ4oARdO0iwDcj9HeiHx58O9ujmVZnystLR2Mx+OvIAs3GcrJb5xhGAsBXCqEOB3ZP248AuBNAC0SYiWEEIdEo9GNEmI5TdF1/XlIXnPvBpUIN86enzfr/O16M9aHr214TdZmQc+ZpnmUjECZxK3hgEAgMNvj8fxOCHGYA+1ms9eJ6JJsW32S7Q/HPYpEIi9EIpEzATQBuBpA2OWUJoyIWgFcmUwmGyorKxcB2CQhrJeIbpAQx3Gapn0FOfDwB4CLpxzAD/8JmOMvx0UNU2WFW6Lr+jJZwTJFZ2dnPJFInATAiZnpi71e7yO1tbW7nkJFuq5/SVXVl/jhv0dzhRDPj+0VkjU96znZA7AHqq7rx2B0LPkMANUu57M32wH8LxH9ORKJvIhdupQ0TTuRiB6V0QgRfSwSidwrI5YTgsFgo6Iob2F0v++stqiyGtccdHDe/KLJIgBcsXE9XuztlhFutWmaTrwpuy4dPQGqqhYpivI7jE7yY/v3T6/X+6ls2GY47+5LLS0t3vb29iVCiOUAlsPd2eUWgPVCiL8rirIqEom8hH1sY6rr+n0AJnRm/V5sBTDTNE3XjyjcA9J1/TEAst7argSwCC7MUC7zeLFy7uE5d7BPuvQmEjj39RelnCJIRIuyrXt2vJwsAojoZSFECIAmO3aO6wBwrmmaT7idyL7kXQGwu0AgUKcoypEAFhPRAowWBFIPetlFN4DXALxKRM+qqrp669atPeO9eOzN+G0ARXYTEUL8JBqNftduHNkMwzhPCHGHpHD3mab5UcCdpUqXTZ2BUwJ6OprKWQ+2R3DdZvujX0T0t7FhwZzkcE8AmxwLwI9M0/whMnSCYN4XAHuiadoUADMVRfnwGMp6AAGMDh1UAyjG6Mx0/9glOwGkAAwC2DH2pwPANiFE69h4/jumaW6zm5uu61cB+IHdOACGFUWZHQ6HM2ZTi7EzHzYAqJIQrtfr9c7avRsuXYVAs78MNzbPh0L8K2aHJQS++NY6vBOPSQglpkaj0S0y8spEXARkrN+bpnkRMvBsAb47ZZlQKFRkWdYGjE5wtOth0zQzZlxP07R7JG7q9DnTNG/fR1uOFQIqEW6ZcyimlZTu/4vZfr0bj+GLb62TsSrgatM0pR7mlGlypQjwl6horPdiar0PU6f40BTyQqvzoqRIQWEhUOH3oKho9Nd2cFCgN5bE4KDAwJBAdHsCrdsSaN0ygs3hEbRtSyDWb39ZqU2rAJydacOuXABkIV3XP4LRNbgynGaa5kOSYk2apmkfJaK/Sgr3pGmayzCObjcnCoEVdRouPyDbzj7JbNe8vxGPdbbbDbPNNM0mjPbW5axsLAL8JSoOPbgQi1pKsHB+EaY3+aAoch5PliXwbusIXnh1AGvWDeCVNwYRH3DlxOg1Ho/nlIkM+zqNC4AsZRjG34UQJ0kI9YHP55vd1tY2JCHWpDQ0NFQmk8kNkDPRqD+VSh3c0dHROpGLxgqBXwA4xk7jKhH+OPdwhAptT9Ngu9g6OIDPrn8Jlv1egGWZPjFLhmwoAkpLFKw4xo/TT/Bj/uwieNT0PI6SKYF1bw7h/sd24tFn4unuHdigquoJ27ZtM9PZ6N5kzXpF9u/Ky8tfEkJ8HvZ3yauyLGskFos9KyOvySgpKfkNACmbtRDRFdFo9JGJXhePx6N+v/8g2LxhHlsTwKk88U+6cq8XbQP9aLN/YNBILBZzvcfLaQ7vGDhpRMBRh5fgvy6swTXfCuLEo0phBL3S3vbHQ1EIoaAXxy8uxXlnVeLApgIMDglsNRPpaL5OCLG8srLyL319fa69dH2IewCymGEY1wghrpQQatCyrFlunHttGMYxQognIeFnUQjxUjQaXYRJdvHqur4RNs4tJwC/O2QBphZn/fYFGemDgTguXP+y3enUPZWVlcFcOSp4fwKBQImiKKuI6Gg381AUYOnhJfja+dWYPaPQzVT2alPrMG69qwcPPRFDMuX4pP21qVTquI6ODmlHYE5GTu4EmC+SyeRPIGeXwyJVVa+TEGdCAoFACYDbIKcQHbEs60JM8uFvGMZ02Hj4A8CCimp++DvogOJSHFphe4FIZW9v75Ey8skGHR0d/clk8lQ4s2Pgfqkq4WMryvGPO5tw60+NjH34A8D0qQX4xbeDeOQPU3Dm8jKozg5JHK6q6l1w+ZwTLgCy2Fj1eKmMWEKIj2qatlxGrPHyeDw/FkLI2vP1mo6Ojrcme/HYuRG2LK8L2g3B9mN5rf3PeGwTsLzR2dkZT6VSy4UQT6ez3dkzCnHPb+px7eUBNIayZzOspnoffnZlEPff0oB5zY4WLKcYhnEHXOyJ5wIgy5mmeTeAp2TEIqJfNjc3+2TE2p9QKHS4EOIrksJtqKysvNZmjFPtXFyiqjiyssZmCmx/FlfVoMRj76WJiFZISidrpLMnoKJMxTWXBfC3m+px8MzMfePfn5nTCnD3jfX48TfrUO53ZrqcEOJcXde/50jwceACIAdYlvVVADJmsBzU09PzdQlx9qm5udknhLgNciahphRFudDOmK6u68UADreTxDE1ARQo/OvktEJFxVFVtbZiCCGaA4FAnaSUssaHBwgR0ctOtXHsohI8vrIRHz+lPK0T+5yiKIRzTqvA4ysbcfQRjg3vXWUYxrFOBd8XvmPlgPb29g1CiBslhftuKBQyJMXao56enm8LIWbLiCWEuCEcDq+1GaMFgK0+yhNqAnYuZxNwov1hAFIUJWOXxzlJUZTisb39pfKowJWX1OLmawxUlufe4rKqChW3/tTA5V+sdWK5oiKE+FNtrYTxrYk2nO4GmTOGh4d/AMD2TikA/JZl/UJCnD0KBAKzMXpAj21E1GpZlu3uMyKydexwiceD2X6njo9guzvYX45i1fbcqbyZCLgLRVXVOyH5YB8j6MVdNzbgwrMrkcs7XxMBF51TiT/fEIJWJ33uXtDr9a5Emp/JXADkiO7u7p1EdLmkcOcEg8GlkmLtSlVV9TYAMuYZCCHExZKW0Rxh5+KD/eWgv/J+AAAgAElEQVRQc/nOl2FUIhzsL7MVY+zgr7yi6/qlAE6QGbN5eiH+dlM95s7K3rH+iZo/uwh/u6kBM6cVyA59nK7raT2gjQuAHBKJRO4EsFpCKFIU5deQvETFMIyvwuZY+y7ukLijm60CoKVcxtlFbCLm2f/MZyOP9kHRNG0mgB/KjLlwfjH+dH0I1ZWurmRzRW21B3++IYQj5knf8fP7hmHY6pGcCC4AcosA8BXI2et8jq7rl0iIAwAIBAJThRA/khQu6vF4pCx/rKurC8Bml+i8sgoZqbAJmF9u+zOv0HW9XkYuWUAlot8BkPaavnxpKW7/uYHS4vx9hPhLVPzuFyEsX+rf/xePnyqEuDVdq7Hy97uXo0zTfA3AzZLC/XDsAWkXqap6CwAp02iFEF+WdaCG1+u1tQ9BicfDm/+4YFpxKYpUe5PNhBCzJKWT0XRd/yJs9nLtavnSUlx/lQafN286UPbK5yVcf1VQdhHQ3NPTI2We1P5wAZCDPB7PdwF0SghV4fF47K6vh67rFwI4TkI+EELcG41G/yYjFgBYlnWAnesbCouh8Ph/2ilEqC8sthdDUWQcqZ3RxpY7Xi0r3hHzivD/vqc5vUteVlFVwi+/H8TiQ+39PO7mylAoNE1mwD3hAiAHbd26tUcI8R1J4c4zDGPSbw9TpkzRAPxcUi7dyWRS1uZBAAAistUDECriU//cUl9k74YrhMj5AkBV1WsBVMqI1Ty9EL/9ic5v/nvg9RBuvFqXOTGwIJVK2X752h8uAHJUNBq9HcArEkLR2B4Dk/pZSSQSv4GkGxCASzs77R8KvxtbBUCDzbdQNnkNNgsAAFNk5JGpgsFgM4DPyohlBL343c91+Etyb42/LKUlCn73c0PaEkEiOkvTtCVSgu0FFwC5y1IU5csALAmxWjRNu2iiFxmGcRaAMyS0DwCPm6b5e0mx/o8QwtZDwO5bKJs8u0MAAHJ672ZFUX4MCbttelTg+qu0vJztP1G11R786vuatM2CiOgnUgLtBRcAOWxsh7zfy4hFRD8xDKN6vF8fCoWqhBC/ltE2gP5UKnUxYPck2P9ERLYWlNf6pK8FZuNUV2D7s8/ZAiAUCi0A8BEZsS67uDav1vnb1TKnCN+4aNy3yv1Zouv6MlnBdscFQI5LpVJXAuiVEKrasqwfj/eLLcu6DoCUrS2FEN/p6OjYLCPWHtiawi9hRzo2SRI+e2l36UxjWdaVkLDPwbGLSnDBx2WN4OWPi86pwlJ5ZwdcJSvQ7rgAyHEdHR3bAXxfRiwiukjX9fn7+zpd10+ApLFHAC9Go1FZPQl7YrMA4DFRtxTbP3wpJ8dvxjb9Oc1unIoyFT+7IpjT2/s6hQj4xZVBWacIHunU5kBcAOQB0zR/C+ANCaFUADdiH28WgUCgBKP7EMi4bQxblnUh5Mxj2BsuALKUhB6AnBy/IaJLIeHe/q2La3LyYJ90qapQcennpXUySdn4bHdcAOSHpBDiy5Azhr7QMIy9vt17PJ6fAGiU0A4AXNPe3v62pFh7w0MAWarYY/vhlHMFQENDQyWAT9iNM6+5EGetsHfeAgPOPqUcBx9kf/6EEOJ0TdOkr1rhAiBPRKPR5wD8WUYsIcRPp06d+h/H3xmGsVAIIWud/puVlZU/lRSLsT0hXddPCwaDsxobG3NillsikfgMAFubU6gq4epvBKAo3Pdvl6IQrv5GnYyNkxQiukBGTrvi15c8oqrqt1Kp1GkA7O5bGRgeHv4hgK9/+B+mTZtWMDAwcBvkFJUpRVE+t2HDhhEJsfYnDmDSJ8sMpJIo83glpsPGayBp+8gLBcADiqJgZGRE6LoeIaIPhBAfCCE++PDfvV7vB7K2nnYaEU14ue7uPnpimRMn3eWt2TMKcdrxftz32E67oc7H6K6OMs56AZBHp2GxUbquXwY5O/MlFUVpCYfDb4zFvRrA9yTEBYD/Nk3zMkmx9knX9a0AJn0ozN3zFyJYkBMvj1knOjSIc157MV3N9QBo/fCPEKKViFpTqVRrR0dHG5ydpzIuuq7PA/CqnRiqSnj0D1PQVJ+Ws2jyxgdbR3DSZ9tg2f8pWSbxFFTuAcg3pmn+0jCMzwghZtsM5bEs6zcAjgqFQrMty7pcRn4ANqdSqR9IijUecTsXD6SSsvJgEzRgSXsRGo9KAC1jf0BjU+NVVYWu6yNEFP6wKPjwn5Zltaqq+nY4HB5MU462x/5XHF36/9m78/ioqrt/4J/vnUnINmEnmTMTDIsigqIGd3EFwbWL7aN9tNbaWpc+dXvUqq0KamvVarWb1q1P61Jt61ZtZXHXKi4oqyhCCMnccycEAmSyZ+ae3x8J/SGChJzvnTvLeb9evF6V5n7uYSYz93vPPYu5+Htg3OhCzDyqDC++pvV1AwBnADAFgDFgSaXU5QAWMGQdGQ6Hz1JKXQKA41tDEdH3Gxsb2xiy+oWIWpUa+NjI9lRaL0LGNtr0HwFwKVRKjQUwduvvklIKRATXdZORSKR++8cKgUBgjeu6q6WU7Yzt+KbOwUTARWfn7NIIvvvhOcMx9/VWaHzdAMDXampqLl60aFEPR5tMAZCHpJQvRSKRp5RSp+tmEdHDSimuh+AP2bb9ClNWv7iu20YaE52bursYW2Psjix57YNbiwMimgFga2EAABBCOADWAPhPcWBZ1hrXdddIKTf09yTRaHRf13WrdRo67eBS7DXW3P17Ze9xg3Dk1FK8+b7W/c3weDx+JIBXOdpkCoA81dcLMAua0+AAcF38nWAweDVTVr8RUaPO8Q0dnDdwxu6o70hbR5GXwn1/jtzae7BNcdBJRFIp9TGAFduNO1iHbQaDua57sm5DTp9lpv157WuzQroFAJRSs2AKAEOHlLIhEon8Qil1s99t6XOxHyOtlVKf6fQA1HeaAsAvDZ3perTum6KtvQcATtlu3EEXegckbu050FovvqzUwvFHlGk32PhyM44sQ6g0gETbwB9fEdFJAFjGXJl1APLYkCFDbgewyu92AHhSSvmsHye2LGuNzvENHTl/EcpYOdIDMFCDAEwEcIpS6lIA++iEnXxcCEWDzKQwrxUXWZh5lF6nq1Jq8siRI1n2WTEFQB5bsWJFNxH9r8/N2JhMJi/16+RKqc90jq/vaIerOarH2H2uUojlfg9A2nxlhu7SIEZ/fXXmF9ZQ223BYPBwhqaYAiDf2bb9AoAX/Do/EV2xfv16refwOpLJ5Gqd49tTSdS25/WdqC8+a2tFh5mBwaKsxMKBk7UWDzR2w9T9ilBWon3pPYKjLaYAMBAIBC4D0OnDqefZtv1nH877H33FR0In48OWrFgkLqd81MKxw7UBAAdNKUZQf6lao5+CAULNfnoFFxEdzNEWUwAYaGhoWKOU+mWaT9uWSqUuTvM5d4iItFZP+3CLKQDSzbzmfA6vYdu33uinww7Q3ol6XzCs5GsKAAMAEAgEfg6gLo2nvKaxsbE2jefbKdd139Q5fknLFqTMOIC0SSmFZYktfjcjZxx2oOn+TzeG13ywEGLAS5hvZQoAAwAQi8U6lFKe7Dm9A29LKX+fpnPtEhFpFQDtqaS5IKXR4pbNZglmJqHSAPYaYxb/SbeJ4wehtFjv8quU0pr5AZgCwNiG4zhPAZjr8Wm6XNc9HxmwecpWPT09bwPQuqLMb4oztcbYFfNa8xkzusBs++sDyyJUa+65YFnWGO126AYYuUUpdQUAz7bhJaJb4vH4x17lD0RTU1MrgCU6Ga81N6GLYasv48t1uim80dzvFXJ35mMiuge9s19WAsiKNYW9MCZq7v79MrZKbxFVpZR2AWBWAjQ+x3GclUKIewB4sR3vksrKytts2/YgWo9S6nUiqhno8W3JJN5qbsLxIyo4m2Vs582NGzi6///Ptu07tvlvSwgRsSxrnOu644honFJqHICtf4bonjBTjRltCgC/MLz2e+gGmALA+ILu7u6bCwsLzwIgGGOTSqnvc+1ixY2IngFwhU7G3Ka4KQA8Npeh+5+Intvur1wpZQOABgCvbf/zQogRX1IchLUb5CPdu1Bj4Mbqb7s8QjfAFADGF2zYsCEhhLgKwGOMsb9yHOcDxjxWUsq3hRA2gMhAM97f3Iw17W0YV2KmVXlhdVsrFm1p1o1Zadv2bi1/3bcr3wYA727//wkhSr6kONgDGf4dWzkyo5uX08KjtF97UwAY3iCiFap3ezKOEUJdnZ2dtzDkeMklor8ppS4baIAC8GisDjfuNYmxWcZWf47VgWGy5fZ3/1qklO0AlvX9+ZyampqC9evXj04mk+O3FgdEtG2h4Pv8u7KSgN9NyFsMqwEO1w0wBYCxI0Gl1IPgufgDwKDi4uLvAfgVU55X/gpgwAUAALze3ISGznZUFWkv9GFsY11HG97cpD34D0T0BENz+qXvcdeavj9fUFVVJZLJ5LjtexCIaBwYvtz7o6TEzADwS4l+AaD9JWMKAOMLhBCXA5jKmamUmj1y5Mi/NDVl7hwu27YXCiHqAYweaEZKKTwaW4drx09kbJnxqF2vvekSEb1v27bWbA9ODQ0NEoAE8IV1KKqrq4d0dXWNtyxrrOu647frOYiAqThnuAs1BojhtR+kG2AKAONzotHoeNd153gQXR4MBm8D8B0PsrkoAP8H4AadkAUbGnF6OIq9Ss0OaxxWtrbgpQ36+0W5rvsgQ3PSoq6ubjOAD/r+fE51dXVRZ2fnWMuyxgF4FhrTuUtNAeAbhtdeuwAw776xLXJd9z549GySiL4dDoeP8iKbSyqV+h00N0ZKKYW7aleZbYIZuErhnrWfcbyWbV1dXWnr/vdSXV1dZzwe/1hK+TwAsyVi/tL+UJgCwPiPcDh8PoDjPTwFEdHdADJ25FFjY+N6ANoXipWtLXhhvcPQovz2/HoHK1tbtHOI6LHm5mb9oMzTqnNwW7tZvMovDK+99oJtpgAwAADRaDRCRLen4VQHCCEuSMN5BqyvSNF2f/0abO7JyGUPssKmnm48UL/D8XO7K0VEd+z6x7JSm87BraYA8A3Da6+9gqUpAAwAgOu6vwcwOE2nu1kIoT2H1St9A8Ve0c1JJJO4dfVKjqlrecdVCreu/gSJJMumP0/GYrHVHEEZSKsAaG83v51+adcvALTee8AUAAYAIcQZAE5L4ymHAfh5Gs83ELdxhCzcvBFPynqOqLzyuKzHu5s3ckSpVCp1K0dQhtLsATBDCPySaNMuALRXxTIFQJ6LRCLDAfzah1N/r7Ky8iAfztsvUsr5ABZwZN1fX4vlZrvgflvashkPN6xlySKiZxobG5ezhGUmrTEA8SazrbJfGF577YUxTAFg/ArAKB/Oa1mW9Rtk8O8gEV0FhlHWKaUwZ9UKbOzO203n+m1jTzfmfPYxUjwzKHqUUtdxBGWwBp2DaxvMGBW/1DZoj+Fr0g3I2C9fw3uVlZUnKqW+7WMTDhFCnOvj+b9U31iAP3Fkre/uwpUrl6BVfye7nNWWTOLqlUuwgalQUkr9Rkr5KUtY5qrVOXhtvWc7fxu7UKv/2q/TDTAFQJ6qqKgotSzrd363A8DtfY8hMlIgELgeDINtAKC2vQ0/+WQZul0z8np7SaVw/arlWN2m1aO9reZAIPAzrrAMpvWshOEu1Bgg3QKAiLSfk5kCIE8FAoHbAIzxux0AhiulZvvdiJ1paGiQRMQ2iGxxy2bcwtfFnRNSSmHOZyuwaMsmtkwi+kksFtMeJJXplFJa8yTX1nfDdc3vYrq5rsK6mN7jF9d163TbYQqAPBSJRA4DcJHf7djGRZFIZIrfjdgZ27ZvI6L3ufJeb27CjatWoMv0BKBHubj5s4/xxkbtx5nb+rdt2w9wBmYq3bvA1nYXn9aaXoB0+/izLrR16H3+LcvSHtxqCoA8U11dXaSUehg8730SQB1DTkAp9Rvw7T7ILZlKpc6F5hLB23qzuQk/XrkEbTzz3LNSWyqFK1cuwasb13PGtqZSqXOQJ0vkSiltAFpTTN75sJ2pNUZ/LfyoQzdis23btm6IKQDyTE9Pz/UA9maKu4uIzmPKmhYOh/+bKYtdPB7/GJqbBG3vo5bNuOTjj/JydkBzTzd+tHwRFm/ZzJpLRFc1NjZqDYzLMi6A93QC3l5kCoB0e+cj7dd8GcxeAMbuiEQi+yulrmKK+8yyrNm2bb8K4EmOQCK6Y8SIERm7hZ6U8i4Ab3Nmrm5rxYXLFmFZHq0TsLRlM85f+gHWtLOMrdzWPNu2/8AdmgXe0Tl40bJOJFNmHEC6JFPAB0u0ewC0ir6tTAGQP4JKqQcBFDBkKdd1z4/FYh0AQERXQnNBkj7hwsJC1rtsZinXdc8CwwIc21rf3YVLV3yEv8j6nF42WAF41F6Hyz5ezDbVbxv1AM4Gw11RtnFdd6HO8Ym2FBYtY3u6ZezCe4vbtZ//K6X+zdEWUwDkCSHEFQBqOLKUUvfH4/HXt/63bdsxAFxTri4Nh8MTmbLYxePxOsuyvgmAdQWVlFK4b90aXLNySU5uILSppxs/XrkUD9TXejEDolMpdbqUkrUwyxbBYPBdaBY+z87LxY0SM9Nz87Vfa+W6rikAjP6JRqN7ApjNFBcrLi7+8fZ/OXTo0LsArGLILyAiP5Ym7rdYLPYagMu8yF64uRlnL16If8RtuDkwVdBVCs81Snx78btca/vvyA8dx/nAq/BM1zfd8WOdjLmvt6KzK/t/3zJdR6eLeW9od5Yu69u2XJspAHIfKaUeAFDMlHdxbW3tFx5Yr1ixolspdSnTOaZHIpFvMGV5Qkr5eyK634vsRDKJO9euwkXLF+HT1oQXp0iLla0tuGj5h7ir9lOuXf125NdSyoe9Cs8iz+scnGhLYcFbbIswGTsx/81Wjm2A53K0BTAFQM6LRCIXKKWOZop7Qkq50y8ax3HmAniO40RKqTuFECUcWV4ZMmTIj8CwbfDOfNKawEXLF+Hnq1eiviN7Rmqv62jDz1evxMXLP8QnrZ52LT8hpbzcyxNkC8uyntXNeHqueQzgtWcYXmPLsl5kaAqAzJ13bTCoqqoSqVRqBYAhDHEbU6nUPrvqehJCjAawEoD2xVspdYvjONfr5nhJCFGilPonER3j5XksIhwyZBjOjVZj77JyL081YLXtbXhC1uOlDY3pWOnw5ZKSkpNXr16df3Mod4yEEOsAVA04gIAXHtoDE8YNYmyWsdUna7pw6vfWQfOjsUFKGUbvGizaAhwhRmYqKyt7HMB+HFlKqQvi8fgupxslEoktoVCoEMAxuuckokMGDx78REtLS8Yu6ZpIJHqKioqeDgQCxwKIenUeBSDW2YF/rnewvLUFFhEiRSUIkr81fKebwqsbmvD7dWtw37rVWN3emo5h+AtTqdRJDQ0N2nOpckkoFBoH4GCdjC0JFycek7EzcbPa7LvXY3Wd9qqLjyUSCZZeVsD0AOQsIcS3ADzOkaWU+pfjOCf39+ej0Wix67orwLPXwD+llKcw5Hiqurp6SHd390tgmmnRH6XBII4aNhIzR1Ziv9BgBNJUDKSUwuKWzZjfFMcbzRvQnt4dDt/q7Ow8ubm52fRXbycSiRyvlHpJJyMQIMz90x4YU1XI1SwDwOp13Tjp3Drorv5NRNNt236Zp1WmAMhJQogR6B0VPJIhLgFgkpRyt/YdF0J8BYD2c8k+p33Z2INMEY1Ghyml5iqlDkr3uYsDAUwJDcaBQ4bhgPIhGF9SBoupIHCVwur2Vny4ZTM+atmEJS2b0ZHyZaXd+QC+JqXMngER6WUJIVZDs/A+fVY5bru2kqlJBgBc+bM4ntWf/tcgpRwDxmWuTQGQg4QQjwI4iynuh1LK3w+wHS8CmMXQhjWFhYWT6+rqMn61kr6Bi48B+Kqf7SgOBFBVVIKq4hKMLi5BVVEJRg0ahJJAAMVWAKFgAYoDvU8AO1IpJJI96HBTaEum0NTdhYbOdtR3tKGhowMNne1+XfC39WxJScmZ5pn/lxNC/BjAL3QyAgHC0/dVYdJeRUytym9LV3biGxfXa9/9A5gjpZyt36L/zxQAOSYajZ7kuu4/meLelFIeg971xndbJBLZSym1DIB2fyIR3WDb9s26OWlihcPhXxKRGaHOgIjutm37KjANfMpllZWVIy3LagCgNZJvysQi/O33VbAsc4nQ4boKp1/UgGWfaN+7pACMlVLWMzTrP8wgwBwybNiw8kAg8C8AgxniupRSp7S2tg54n9ZEIrExFAqVAjiSoT2HlpaWPtba2sq7e4w3VGtr67yysjJJRCfCTLcdqC4AF0gpf4EBFqH5prW1tb28vHwCNAf/Nm5IomJEEJMnmF4AHY8/twVPvqC/z4dS6mnHcR5kaNLnmC+mHFJUVHQrNKYBbUspNcdxnJW6OT09PT8DEGNoUnEgELiTISdtHMd5AMBJAOJ+tyULOUR0jFnkZ/cppe7lyLnj/o1o3uz7o5+stXFTEnc+yLM6tWVZnnz3mQIgR4TD4WkALmSK+8hxnDs4gpqamloBXMmRpZT6uhBiBkdWukgpF6RSqSkAuB7L5IMXUqnU/rZta21yk6+klG8D0B4pviWRwtW3xnXnrecl11W46tZGtCRYOq7e9OqzYAqAHDB+/PhBRPQH8LyfSaXU+WB83iqlfBJ8K+b9bvz48Vm1UkljY+N6KeWpSqkLAJgR7DvXoZS6TEp5Gtda53mMZVfN1xa24cEnN3FE5ZX7HmvGG+/ybHdNRHNYgnbAFAA5oL29fTYArh30fuk4ziKmrP9wXfcS8Oygt2d7e/slDDnpphzHud+yrEMBsL++OWAhgAMcx7kHebilLzcp5dtKqX9xZN15fxM+XG7WXOqv95d24Nd/5Fm7jIhe55z3/4V8r4KN9BBCHADgPQBBhrhVlmXtH4vFPPm0h8Phu5hGxicCgcDeDQ0NkiHLD1Y4HP4+Ef0MwAi/G+OzJgDX9T3rNwP9GIXD4Roieh8M3/PhUUE8fd9ojBzO8TWTu9ZvTOJrP6hH4waWDlQFYJqUkmXr3x0xPQDZLQjgIfBc/F2l1PleXfwBoKurazZ4BsSFUqkUyxgFn7h9vQETAPwejAt7ZJEUgN8Hg8EJUsoHYS7+7Pp68v7OkrU+ifOutpFoy8df1f5pbXPx3atsros/APzNy4s/YHoAdoQqKirGBIPBiUqpsUqpaiKqIqJRAIYrpYYDKELv3PbSvmNa0PuF1klEG5VSjei90MWVUp9ZlvWZUuqz3V1Nb1eEENcAuJUp7l4p5cVMWTsViUTOUUr9iSFKKaWOcRznDYYsX0Uikf2VUjcDOBm5/5l0lVJPu647p7Gxcbnfjcl1kUgkqpT6GADLAv+HHlCMh++IorAg139Nd09Xt8J5V9l4dzHbEJ8OpdREx3HWcQXuSN6/i1VVVcJ13SMAHNG3hOu+YPqw7EAzgPeVUh8Q0budnZ2vD3RN875FdpagtxjR1dDZ2Tk5TeurkxDiTQBHMGQtk1IeiBxZICYSiUxRSl0D4JvIvTU6FBE9TURzYrHYMr8bk0+EEJcAuIcrb9bRZbjnxjACgby/fAAAUimFS2bHMe+NBFsmEV1v2/YtbIE7O4/XJ8g0kyZNKty0adPRSqkTiegkABN8bE4SwPsAXnJd9/l4PP4B+jcAyhJCvAZgGkcjiOgU27bTNk2tb9zC++C5yF0qpfw1Q07GiEaje7qu+2MAZ0NzRbcMkFBKPea67u/MHb9vApFI5B3OPSpmHR3CXddX5n1PQFe3whU3s1/8lw8ZMqRmxYoV2lsH7vJcXp8gQwTD4fB0IjoDvWu0D/G7QTuxTin1VCAQeDIWi723sx+KRCIXKaUGtD7/DjwupeTaN6DfhBC/B3ARQ9TmVCo1IRenjUWj0WGu635LKXUOEWlt8+qDZUR0b1dX16MbNmzg+3Y0BoR5sDCA3scB9/5MIFSaa51V/dPa5uKC6yRntz8ApIjoyHStgZHTBUBFRcUYy7K+R0TfBSD8bs9uWqaUesiyrEdt29649S+FEFUAlgMoZzhHE4B9pJQ8y1Xthr6L26fgGQX/RynleQw5GSscDk8kou+gd5OnqN/t2YlPlFJPWZb1d9u2F/vdGOPzhBA3ApjNmTlx/CA8fHsk72YHNDWncO6VMXy6hndvqnTveZKTBUA4HJ5GRP8L4FRk/0yHDiJ6RCl1l5TyUyHEC+gdLMbhLCnl40xZuy0cDp9PRPczRCkiOjxPVo6jaDQ6WSk1Qyk1A8BRAEp8aksHgIVE9GoymXzGdPFnPEsIsQDAcZyh4VFB3H1DGDX7FnPGZqz3l3bgsjkO52j/rRZIKWchjTNicqoAiEQiJ7uue0MWdpf2h4veLrxDmfJekFKeypQ1UJYQ4l0AUxmyFkkpD0aeTScbP378oI6OjsOVUtMATEbvINbxYOzq7eMCWAtghVLqXSJ6fejQoe+n4zmlwWfkyJGVBQUFHwGo5MwNBghXnD8c5585DJRTV5X/T6neFf7ueXgjkin2taqcZDJ5wPr16xu5g79MTrxVkUjkWKXUzwAc5ndbskQLgMnc0xIHIhqNHuK67ttg6KlRSl3oOM4fGJqV1caPHz+ovb19H6XUJCJ6RCdLKXU2Ea20LGull2tEGOkTiUSOV0rNhwe9o0cfWoo7rq3EsCG5NS5g46Ykrrq1kW153+2kiGiGbduvehH+ZbK6AKiqqhKpVOpOAGf63ZZsQkQX2bZ9n9/t2EoI8RAAjmf4Gy3L2isWi/Gsw5kDhBBatypSyqz+jjC+qKKiojQQCHwEYE8v8geHArjyB8NxximDYVnZ/evjugpPPN+CXz7QxLWxzxeka8rfjmTr8/FgOBy+NJVKrYS5+O+WvrWlM+ouOZVKXQtgM0PUcNd1ffkgGUY2mDRpUmEgEPg7PLr4A727CF5/53p87YIGLFnZ6dVpPLdiVSf+64cNuOEutl39voCIHrFt+2eehPfn/H6deKCEEIejd/nUKX63JQt1EGUBi54AACAASURBVNH+tm2v8rsh2xNC/AgAx3z+FICDpZQfMmRlPdMDYGzVtwbKUwBOSdc5AwHCadNDuPDsYRg3ujBdp9Wyel03/vBYM55b0ALX2xFF/5BSng4fFzLLpg93QAhxPYCfIvdWSUuXH0spb/e7ETsREEIsAk9h946U8giYXeVMAWBsFRBCPAqfekwtCzj6kFJccu5w7Ls3x+Kl/FbVduOBJ5rxj5cSSPEP8tvewlQqNb2xsdGTQQX9lRUf7qqqKpFMJh8jomP8bksW+1BKeQgyeNncvumbr4Ph95KIzrVtm2PPgaxmCgADvbtP/pGIzvG7IUTAkVNL8bVZIZwwLYSiQf7+enV0upj/ZiuemduCfy9qh0rDLQMRLQ8EAkfV19dv8v5su2iL3w3YFSHECQAeATDK77ZksSQRHZQNi7P03aVwrEzYWFRUNKG2tnYLQ1bWMgVA3qNwOPx7IrrQ74ZsL1QawMyjSvHVmYMxdb8iBNO0t0AyBby3uB3Pzm/B/Dda0dqevpnDRLTcsqyZmbKVeSZ/uEkIMQfAT5C9gxUzAhHdatv2dX63oz/6ZnZ8AoYNmYjobtu2L2doVtYyBUB+E0L8EsD/+t2OXSkttjB1SjEOP7AEhx5QjInjB7HNIHBdhZWru/DOhx1456N2fLCkA20dviwX8lYwGDwtE+78t8rID3dNTU1BPB5/SCn1bb/bkguI6JHKysrvLVq0qMfvtvSHEOJKAHcwRCVTqdQB+bxCnSkA8lffDdQNfrdjIEqLLVRXFWJsVQHGjC7E2KpChEcFUVpioaSYMDgUQElx731he4eLLYkU2jsUWttcxJuSqG3oRm19N9Y29KCuoduvC/62/mFZ1pmZtpZGxn24hRAlSqm/9e3U55tQaQDVVQUYW1WIsXsUYky0AOFRBSgttlBUBAwJBVFc3PvydXQobE4k0dGh0N6p4KzvQW1DD2rXdWNtrBt1DT1ItKX8/OcAwILu7u7Ts2FjlpqamgLHcZYAmKibpZR6zXGcYxmalZVMAZCfhBBXA7jN73YYAICHpJQXIgPHX2XUh7tvg5gX4MOKfqHSAKbuV4TDa0px2IHF2GtMIWsX1Ke13Xjnw3a8vagdHyztSOtzp218SEQnbLu5UKYSQkwHsIAp7ltSyieYsrKKKQDyjxDifwD8xu92GEgR0ey+ef4ZOSMpYz7c0Wg04rruPACT0nXOslILJx0bwldPCOHAycVpHISisGhZJ56d14K5r7emu3dgCYDpfuwAuLvC4fDfiOgbDFGxnp6eiU1NTa0MWVnFFAD5RQjxXQAPIYO+2/OUQ0Rn+bG87+7IiF+Svjv/N5CGiz8RMO3gUnx9ZjmmH1nm+zSUzi6FBW+14pl5LXjzvba0TEMBsMx13ePj8XhTWs42QEKI0QBWgme3u9uklNcw5GQVUwDkDyHEmQAeBf86Kf8G0ApgJnNurnopmUyene6NfQbC9w93NBotdl13PoAjvTzP1oUoLv3ucEyekKkLUXThgSc24fmXEl7sNrW9D7q7u4/L9DEBkUjkp0opjv2xuwHsJ6X8lCEra5gCID8IIU4D8HcABczRi4PB4HH19fWb+7bvvhNAGfM5ckUKwC1Sypv7/nfG8/XDXVNTUyClfNbLAX+BAOHrM8txwVnDUB3l/mx4Y21DN+57tBnPLvB8RaoFQ4cOPSWTt3Tt29luOXq3uNU1r2+/7bxhCoDc17dWyj8ADGKOXkZEx247ZqiqqmpcKpX6E4AjmM+V1YhoOYDzbdte6HdbdoefH26KRCJ/8nKq3wGTinDTFRWYOJ77c5EeK1Z14oa71nu6oUbfZhS+rxD2ZSKRyMlKqRc4spRSX3cc5xmOrGxgCoDcFg6HjyKiF8HzmGxbq5LJ5FE76cYOCCEuAHATgOHM5802HUR065AhQ27L5BupnfHtwy2EuAnA9V5kDykP4OoLRuAbJ5XnxHaUf31hC+64fyO2JDzrVbpaSskx794zQojnwbOJSZ1lWftk2nxcr5gCIHdFo9GDXdddAKCcOboOwFFSyoYv+6HRo0cPTSaTswFcDCDI3IZs8Fel1NWO46zzuyED5cuHu6/L6kV4sMLfcYeX4rZrKjF0cG7tF9S8OYWrb43jtYWe7B2Rcl331Hg8/qIX4Rz6uh6XA+AYwHGTlPJGhpyMZwqA3BSJRKYopV4BMIw52k6lUkc1NjbW9veAysrKfSzLuh3AycxtyUhE9LpS6idSyn/73RZdaf9w9y31+hGY1/YPBoCrLhiJ8/5rKChHv7KUAh58chPuvH+DF4MEmwHsv6uq30/hcPhmIvopQ1RnKpWatDtfctnKFAC5RwixN4DXwb8/ynoAR0spPxnIwUKIA5RS1xHR15Gby7e/SURzbNt+2e+GcEn3mxRIJpOPgfkXN1JZgCd+OxrfOyN3L/5A7xTG888cisd/HUV4FHuP2zAAjyGDu/KI6FYAHN1tRYFA4FcMOYaRVhUVFWMBvAT+i/8mIjphoBd/AJBSfuQ4zjfRO537TwC62FrnH5eIniKiw6SUR+XSxR9Icw+AF8/9J+1VhIdvFxg+NGOvW55o2pjEeVfbWLma/TOW0d3j4XD4dCL6O0eW67onZfJjDw6mByB3RCKRqFLqDQBjmKMTlmVNj8Vi73GGRiKR4a7rnk1E5wHYjzM7DRoAPAzgYSllvd+N8UraPtxCiMMBvAnGXofDDizBvT8TKCvJxd6mXUu0pXDRTyQWfsQ6ni0J4BAp5YecoZyEEPMBzGCI+qykpGTf1av5q6hMYQqA3DBq1KiKYDD4OoAJzNHtSqkTHcd5gzn3c8Lh8FQiOhfAVwBEvTyXho0AniaiJ23bfg1ZMpdfR7o+3EEhxAcApnAFzjq6DHddH0ZhQX5/P3X3KFxxcxxzX2ddz2dJOBw+KFN3D+x7BroEQKFullLqOsdxbtVvVWYyBUD2i0Qiw5VSrwLYlzm6C8BpUsr5zLlfhoQQ+xPRSUqpUwAcDH/HCywFMJeI5tq2/SYycMMeL6Xlwx0Ohy8jIrZnrrOOLsM9N4YRSNPa/ZkulVK4dA5vEUBEP+3bxCIjCSFuB3AVQ1QbgImZPPhRhykAstvYsWMHd3Z2vgRgKnN0D4BvSimfY87dLdFodFgymTzEsqyD0FsMHAT+8Q1bbQawTCn1PhG9mUql3m5sbFzv0bmygucf7r5R/yvBNFf1sANL8NDtkby/899ed4/Cd6+M4d3FbI8D2gHsnakXxhEjRoQKCws/ASAY4v4qpTyDISfjmAIge1VUVJQGAoG54F8mPQXg7EzdIVMIMdqyrLFKqWqlVDWAaiKqVkqVARiC3hUPSwGE0DtoOYHeO/d29HbjbwTQCKCBiNa6rltLRCtz+Vn+QHn+4RZCPAGA5ct1wrhBeOLXVQiV5ecz/11JtKVw9mU2VqxiWznwCSnlt7jCuIXD4bOI6FGOLKXULMdx5nFkZRJTAGSnSZMmFW7evPlZpdSJzNFKKXWh4zj3M+caWcjTK2kkEjkWTBf/SGUB/nxnxFz8v0SoNIAHfyE4pwie0Td4MyM5jvM4AJbBS0R0V01NTXZsFmHktJqamoJNmzY95cHFHwAuMRd/YytPr6ZKqZ9z5AQDhF9dX5l3U/0GYuTwIH57k0CQZyFEAvALliRvKNd1LwbPwJ194vH4jxhyDENHwHGcP4Nn2evtXSul/K0HuUaW8qwAiEQiJwM4lCPrqgtG4MDJxRxReWHKxCJc/v0RXHHT+npyMlI8Hl8B4F6OLKXU7KqqKo4xBYYxECSEuA/AmR5k3ySlzORi3vCBZwWA67o3cOQcd3gpzvuvoRxReeUH3xqGow8tZclSSs1hCfJIYWHhDehdxlRXyHVd8yVp+IGEEL8D8H3uYKXUXZm8uJfhH08KgHA4PI2IDtbNGVIewG3XVOb08r5eIQLuuLYSg0MszwKmRaPRQziCvFBXV7cZwDUcWUqps4UQZq9zI636prVexJ2rlLrPcZwruXON3OBJAUBELL9wV18wIud29UunYUMCuPIHPI8CXNe9nCXII1LK/wOwkCGK0PtIwQw4MdJCCDEHAPtFmogecRznhwDYdw4zcgN7AVBRUTEGDANYDphUhG+cxL3Ndf4545Ry7Lc3xw66OF0IMZojyCNKKfU/AFyGrH2FEBcw5BjGlxJCXAWA5XHptpRSf7dt+7vg+TwYOYq9ALAs63u6uYEAYc7lFbAs0/evy7IIN10ximPVxCCA7zI0yTOO4ywiogeZ4m6urKwcyZRlGF8ghLgYwO0eRM8vLS09G3mwlr2hh7sACBKR9kXi6zPLsc+egzjaYwCYPKEIp00PcUSdi8zf5/s6AM0MOUMty2KZxmoY24tEIucC8GJK3suFhYVfyeUNrgw+rF/mlZWVM6C5NGsgQPjBf5tR/9wuPHsYLP13uzoSiRyj3xrv2La9EXxbTp+XyYMfjewUDoe/rpR6APwrsb7T09Pz1bq6OralQI3cxloAWJalverfSceUYUyV9iZvxnbGjS7EzKPKtHOUUv/N0BxPSSnvI6L3GaIs13V/h8zv9TCyRDgcnkVEj4N/kOniYDB4clNTUytzrpHD2L7YJk2aVAjgNJ0MIuCis4cztcjY3g/PGc4xpfIryPwR8i6AS8Ez+rlGCJHRYx+M7CCEmE5Ez6B3Mxs2RLSciKbX19dv4sw1ch9bAbBp06ajAWj13U87uBR7jTV3/17Ze9wgHDlVe3GgEZWVlRk/T9627XcA/Jkp7tbRo0eb51LGgIXD4WkAngPAMiVnG6u6u7tn9D36MozdwlYAcGxccfosM+3Pa1+bpT8Y0LKsUxma4rlkMvljAFsYokYmk8mbGHKMPFRZWXkQEb0AoIQ5ug7A9KampjhzrpEn2AoAIjpJ5/hQaQDHH6H/jNr4cidMC6GsVPttP46jLV5bv359IxFxLWN8USQSmcKUZeSJaDS6r2VZLwLgvruxA4HAdCllA3OukUdYCoC+DVQm6GScdFwZigaZef9eKxpEmKU/GHCKEIJttyEv2bb9GwBLGaICSqnfgX/ktpGjotHonq7rzgfAPbCpyXXdExoaGtYw5xp5hqUAcF1X+5nwV2awzFM3+uGrMwfrRlhKqaM52pIGScuyLmXKOiIcDp/FlGXksIqKirGu674CoJI5ehMRzYjH4x8z5xp5iOsRgFYBUFZime1+02jqfkUoK9F764koa+bHx2Kx1wA8yZFFRL8cO3asdgVl5K5oNBoJBoMLAESZo9sAnGbb9hLmXCNPsRQASqmDdI4/aEoxgvpL1Rr9FAwQavbTLrhqONqSLn0bVHHMka7o7OzkWmjIyDGjRo2qcF33ZaXUWObodqXUSVLKt5hzjTzGUQAQgMk6AYfX8Oxbb/TfYQdoD0iuQRY9D7dtOwbgZ0xxl0aj0X2ZsowcUV1dPSQYDL4IzfFQO9BtWdY3Hcd5gznXyHPaBUDf7n9aI1wPPcB0/6fbYQdqv+aDw+FwJu8O+AVDhw69C8Aqhqig67q/YsgxcsSwYcPKe3p65gM4gDm6B8B/xWKxfzHnGoZ+ARAMBvfROT5UGsAEs/hP2k0cPwilxdrjAPZkak5arFixolspdQlT3PGRSOSbTFlGFquoqCgtKir6p+6j0B1IAThHSvkcc65hAGAoAJRSY3SOHzO6wGz76wPLIlRr7rlAROOZmpM2juPMA/AsR5ZS6s6Kigrz/CqPTZo0qTAYDP4NwJHM0UopdbGU8gnmXMP4D44CoFrn+DFRc/fvl7FVBVrHK6WyrgAAANd1LwfQwRBVZVnWtQw5Rhaqqakp2LRp0985VkHdgUscx7nfg1zD+A+OQYBaz4HHjDYFgF8YXnutrZ/9Eo/H6wDcxpFFRFdGo9GsLIQMLQHHcR4F4MWy2NdIKX/rQa5hfI52AWBZ1kid48eZAsA3Y/W3XR7F0Q4/WJZ1OxHVMkQN6tsy2MgfJIS4D8B/eZB9s5SSpTg1jF3h6AHQWuayYkSAoQnGQIRHae/qm7UFQCwW61BKXcEUd4IQIis2SDK0kRDitwC+zx2slLpLSnkDd65h7AzHGACtAqCsxBQAftFdDRD8a5ynlZTyOSJ6kSOLiO6urq7m3urVyDBCiNsBXMydq5T6g+M4V3LnGsaX4egB0FpRprTEzADwS4l+ATCIox1+IqJLAHTp5iilxvb09FzF0CQjQwkhZgNgv0gT0SOO41wMQHFnG8aX4SgAtB4kM2xNawwQQw9A1t/xxmKx1UR0F0eWUuraysrKao4sI7OEw+HLANzoQfQztm2fB8D1INswvpTvBUCJ5mI0xsCVmh4AAIBS6hYA6xiiigOBwC8ZcowMIoT4HleRuJ35JSUl3wKQ9CDbMHbJXH0NHTlx1yKlbAfwY44spdTplZWVXswLN3wQiUTOAXA/+Pe9eMWyrK+uXr1a+/GTYQwURwHQrXNwe0dOXEOyUlu79mvPsbteRpBSPgngFY4sy7LuGT9+fE70juSzcDj8daXUQ+C/UVrY09PzlVgsxrEYlWEMmO8FQGubKQD80qpfALRxtCNTuK77I/RuvqJrz/b29ksZcgyfhMPhmUT0OADtubLbWRwMBk9qamrKmeLZyF4cBYDWRaCt3Qx89Uu7KQA+Jx6Pf6yU+g1T3PXRaDTClGWkkRBiOhE9C+YxLkS0nIim19fXb+LMNYyB0i4AiKhZ5/jW9pRuE4wBSuj3vuTcXUxXV9ccAHGGqDLXde9gyDHSSAhxJHo3i+Ke4bKqu7t7hm3bG5lzDWPAtAsA13U36BwfbzIDYP3C8Nq3cLQjkzQ3N7copa5mijuzsrLyaKYsw2OVlZUHAfgnAO4dHusATG9qauIoLA2DDUcPQJPO8bUNHI9cjYGobdAavgHwTJ3LOH2bvPybIYosy/oN+J8jG8yi0eh+lmXNBVDOHC0DgcB0KWUDc65haOMYA1Cvc/Daeu2LkDFAtZqvPdNmOplIWZZ1EXjmZ+8rhGBfOtbgE41G93Rddy6AYczRTa7rzmhoaFjDnGsYLDgKAK27QIa7UGOAdAsApVSuFgCIxWLL0Dv/m8PNe+yxR5gpy2AkhBjtuu4CANzvzxal1InxePxj5lzDYMPxCEDrIrC2vhuua2YCpJvrKqyL6T1+yeEeAACAZVnXA9Aa49KnvKen5+cMOQajSCQSJaJXAezBHJ2wLGum4ziLmHMNg5V2AZBMJrUq3NZ2F5/Wml6AdFu5ugttmoswJZPJnC4AYrFYs1LqOqa470QikcOYsgxNFRUVo5RSLymlxjJHt7uue2osFnuXOdcw2GkXAI2NjXXQHA3+zoftus0wdtPbH2ovQiYbGxvXc7QlkzmO8xAAji9zUkr9FoDZ/9pn1dXVQwKBwIsAJjBHd1uW9c14PP46c65heIJjDIACsEwn4O1FpgBIt4Uf6b3mRLSQqSmZzrUs6xLw7HtwYDgc/j5DjjFAw4YNK+/p6ZkP4EDm6CSAM2Kx2L+Ycw3DMyxrXBPR+zrHf7C0A0mzHlDaJFMKi5bq9QAopd5hak7Gi8Vi7wH4I0cWEf1cCDGCI8vYPUKIkuLi4n8opQ5ijnYBfEdK+SxzrmF4imuTC605063tLhYtM/tipMt7izs49gHIlx4AAIDrutcC4FjCdZhS6maGHGM39G3O9KxSinthJgXgB1LKx5lzDcNzLAVAMBjUXjTl2Xk5t6hcxnpuvvZr3WNZVl6NcI7H400AbuDIIqLzhRDcXdDGTtTU1BS0t7f/FcAMD+IvlVI+5EGuYXiOpQBYt26dA2ClTsbc11vR2WWmA3qto9PFvDe0l/BfmI9bmUop7wWwhCEqAOC34N9jHkDv3W4kEtlfCPHfulmRSOSccDg8taKignt53HQJOI7zCIDTPMi+VkrJtXmUYaQd2xKlSqkXiWjiQI9PtKWw4K1WnHp8iKtJxg7Mf7OVo/v/HxxtyUIppdSPiOh16F+8D4tEIt+xbfv/dEImTZpUuHHjxsMsyzpGKTWZiPZtb28fB6bPtlLqT0SEQCCghBB1SqmVRPSuUuq1QYMGvVdXV9fJcR6PkBDiQQBncAcrpW5xHOcX3LmGkU5sdyBCiBkA5utkTDu4FH+8w+yg6qVz/zeGtz7QmwFgWdZesVjsM6YmZZ1IJPKIUupshqjGoqKiCbW1tVt24xgSQuwP4HgA0wFMA1DC0JaB6ATwHoBXiOg527YX+9SOHSEhxG8A/JA7WCn1K8dxruDONYx0YysAampqChzHiUNjPW0i4IWH9sCEcazbcBt9PlnThVO/tw5K70nLx1LKSUxNykqjRo2qCAaDnwIYrJtFRHfbtn35rn4uHA5PJKIzAJwNYJzueT1Sh97eob9JKf+N3gFyvhBC3ArgGg+i/yil/B58/LcZBhe2RUkcx3FDodDeAA7QydmScHHiMeYxgBdm370eq+u0V118KJFIvMzRnmzV1tbWVl5e3gPgBIa4qSUlJc+0tbV9YVGlioqKUUOGDPlBKBT6HRHdAuAY8G9Yw2kIgEMAnBcKhc4IhUKBkSNHfrJp06audDZCCHEjgJ9y5xLRI1LK82Au/kaO4JoGCABQSj2pmzH39VasNRsEsVu9rhvz39Qe/AcAh4TD4RqOoGxWWVn5a2gOfO0T7Nsy+D+9cdFodHw4HL43EAisU0rdBf5Fa9JhbwD3dHZ22pFI5A/RaHS/dJxUCHElgNncuUT0lG3b54FnQSjDyAisy5K2trauC4VC34PGntpKAe3tLmZMK2NsmfHz3zVh5WqWG7ExRHR+KBSqKSsrW9Xa2upwhGYbx3Hc8vLyTwCco5tFRNWhUOiTsrKyovLy8ruVUr8jooPBOEjXR4UAapRSF4ZCof3Ly8s/SSQSjV6cKBKJXATgbjDPrlBK/Wvo0KH/1dTUpLd7lmFkGPZpSOFw+GYi0up+CwQIT99XhUl7FXE1K68tXdmJb1xcD5f/3kUBeEEpNSdfdz4Lh8N/I6JvMER1AsiHX3hFRM8Q0ZxYLLaUKzQSiXxHKfUwmHs1AbxiWdYp+Tjt1ch97AVAZWVltWVZa6D5QZwysQh/+30VLMuTqdJ5w3UVTr+oAcs+8XS2lgLwPIA5UsoPvTxRphFCjAbwMYBsnSfvF5eIHgRwnW3bG3WCIpHIN5VSfwH/Rktv9/T0zGxqamJ5dmYYmYZ9Z7LW1tbNoVDoAPQ+Axywxg1JVIwIYvKEfLgp8s7jz23Bky/sziyzASH07qx2QSgUOrK0tPST1tZW6fVJM0EikdhSXl5OAI7zuy1ZhgDUADi/rKyss7W19QMMYHBdOByeCeCvAAqY27ckGAzOdBzHLFFq5CxPbq+FEEcCeFM3Z3AogAWPVmPYELOD6kBs3JTEjG/XoSWR9nFLedUjMH78+EHt7e3LAYz3uy1Z7F2l1Hcdx+n3wEohxHT0/p6x3iUQ0XKl1LFSyg2cuYaRaTy5siYSifpQKDQLQFQnp6tb4bO6bpw6vRxkngTsFtdV+NHsOFbV+jKjYmuPwA9CodCBoVDo00QiEfejIenQ3NycKi8vrwWgvfRuHosS0XmhUGhTIpH4YFc/3HeT8QL4F0H6rKen57jGxsYvTMs0jFzj2a11aWmpJKKzdHPqYj0oKbZQM7mYo1l5495Hm/HE8553/e/K5x4NlJWVrczVRwOJROKzUChUg95/rzEwBQBODoVChw0ZMuSVlpaWxI5+KBKJ7A9gLjRmG+1Eg+u6x61fvz7GnGsYGcnT+2ohxFsAjtDNCQaAx39dhQNNEdAv7y/twLcviyGZyrj1ShR6V4qbI6X8yO/GcKuoqBgbCARWID9G83stDuB0KeXb2/5lNBrd13XdVwEMZz6fDAQCRzU0NKxhzjWMjOXpw/XS0tI1RHSubo6rgLc+aMepx4dQWsI9yye3rN+YxHevtJFoy8j1Sgi9g0N/EAqFDuibE54zjwba2to2hUKhQQC495zPR2UAzg6FQnYikVgMAEKICUqpVwCMZD5Xk1LqONu2VzHnGkZG87QA6FsYaAKAfbWz2ly8+X4bTptejkGFZkDAjiTaUvjOFTbqYhm/XsnWQuDCXHs0MHjw4IVKqbPQuyyuoScI4Cvl5eWipKTkY8uyXgLAvVvYFqXUCY7jsK1JYBjZwvMr6R577BHu6en5BEzP6w49oBgP3xFFYYEpArbV1a1w3lU23l2st9OfTxSA54hoTobtKLfbJk2aVLhp06YX4fO0wILSUoQiVQhF90B51R4IRapQMnIUgsUlCAwahMJQOYJFvY/Ukp0d6E60INXZiWRnB9qb1iMRq0dLwzok7Hok7Ab0tLX5+c8BgG70rirIKWFZ1oxYLPYuc65hZIW0XEWFEJcAuIcrb9bRZbjnxjACAVMEAEAqpXDJ7DjmvbHDMVPZJKsLgerq6qKurq6niOikdJ+7oLQUIydPQcX+UzFqSg0GV48FWTyPy5TrYsvaNWhcsgiNixdhw/LF6GnPykJzWx2u654Yj8df97shhuGXdF1BA0KIDwDszxU46+gQ7rq+Mu97Arq6Fa64OScu/ttSAJ7tKwSW+N2Y/hBClAB4DsD0dJ2zoKQUVUcdh+rjZ2H4PpNhBdKzdYCbSmLjimVY+/JcxN56NRN6B3ZXl1LqK47jzPO7IYbhp7RdPSORyGFKqbfAuFb3oQcU496fCYRK83OhoNY2FxdcJ7m7/ZMAXgNwPNL4+7ETWVEIjBw5sqywsPAFpZT3g/+IEK45BNUzTkTksGkIFA7y/JRfJtXdBfvtN1D30lw4i97t3c0rsyUBfFNK+azfDTEMv6X1C14IMRvAjZyZE8cPwsO3RzByeC5snNZ/Tc0pnHtlDJ+uYd9qfbaUck44HJ5KRDcCOIX7BAOQsYVAdXV1UXd39wIAR3p5HrICqDrqOOxz5jkYXD3Wy1MN2Ja1a/DxE39Cw5uvQnmw8xSDFIBzpJSP+90Qw8gE6b7DCwghTxCmnAAAF7tJREFUFgA4ljM0PCqIu28Io2bf/Fgn4P2lHbhsjoPGDUnu6LeklMeg94sSAJBphQARPQPgpgwpBEgI8TiAMz07gRVA9YwTsc8Z30aZ0FpYM20SdgNWPvFn1L08D8pN7fqA9FAAzpdSPuR3QwwjU6S9i7dvVsBHACo4c4MBwhXnD8f5Zw7L2WWDlQLue6wZ9zy80YtFfjYppQ5wHGfdjv7PysrKgyzLuhHAydwnHgBPtpTdXeFw+BYi+olX+cMnTsbU/7kSQ8bt6dUpPLVp9af44De/RPOnH/vdFAC4VEr5a78bYRiZxJdLZd8mHvPAv3c3jj60FHdcW5lzGwht3JTEVbc24o13PRlwlVJKndyfQVGmEOgViUTOVUr90YvswvLBmHLeRRhzwslsI/n9olwXtXOfx9I/3ofuhG8b610rpfyFXyc3jEzly1UykUjUhkIhC8Ax3NnrYj346z9bUF5mYdKeg0BZ3h3gugp/+UcLLvqp9HJjn2scx/lzf36wtbVVJhKJx0tLS/9FRALAXl41qh8IwESl1IXl5eX7Dh48+JOWlpZGr09aWVl5NBH9FR58fsQhR+CYX9yDkZP2y/rfXQAgIgzbc2+MnXkKttTXodVuSOv5lVK3OI5zc1pPahhZws9vGBJCPAzgXK9OsN/eRbjpilGYPCE7l2ZfurITN969Hss+6fTyNI9JKc8e6MGVlZUHEdFsP+a+74Aioqf7egSWeXECIcQIAEsBhDlzKRDAlPMuwoSvn4lcfob1yVN/wbI/3gc35f3YACK627btyz0/kWFkKb+/aYJCiGfg4QCzQIBw2vQQLjx7GMaN5l5IzBur13XjD48147kFLfB4MPWCoUOHnrJixQrtroVoNHpwKpW6MdcLASHEswC+wplZWlGJw669CcP3nsQZm7E2fLwM79x6A9qbvNtxl4jut237QvQO/jMMYwf8LgAQjUaLXdedD4+nUVkWcPQhpbjk3OHYd+/M7BFYVduNB55oxj9eSiDl8U5+RPR+d3f3cU1NTa2cuZFIZIpS6icAvgH/f78UgH8CuFFK+aFuWDgcvoCI7tNv1v83bM+9Me3mX6JoyFDO2IzXuakZb/z0f7FpDf/+O0T0qG3b3wGQkXMRDSNT+P0FDQCIRqPDXNd9A4Dnt0BEwJFTS/G1WSGcMC2EokH+vgQdnS7mv9mKZ+a24N+L2tO1jsoKAMdIKTd4dYIM6xFwlVJPBwKBmwbaIyCEmABgEYBSrkaNmlKDI2/8BQpKSrgis0pPWxveuukarF+iXZtt74jttxE2DOOLMqIAAICqqiqRSqXmIw1FwFah0gBmHlWKr84cjKn7FSGYpr0FkingvcXteHZ+C+a/0YrW9rTeqCxxXXdGPB5vSsfJotHoIUqpG5VSJ6bjfLsw0EIgIIRYCGAqV0OiRx6Dw348G1ZBAVdkVnJ7erDwtjloeOtVztglUsqp6F31zzCMnciYAgAARo8ePTSZTD4P4Ih0n7u02MLUKcU4/MASHHpAMSaOHwTL4nl5XFdh5eouvPNhB975qB0fLOlAW4cvvZMfWJY1MxaLNaf7xJlWCAB4KpVK3dTY2Lh8Vz/M3fUfPfIYHH7dTSArt6aqDpRyU3jn5zdyFwFXSSl/yRloGLkmowoA4D+bqjwB4FQ/21FabKG6qhBjqwowZnQhxlYVIjwqiNISCyXFhMGhAEqKe+dot3e42JJIob1DobXNRbwpidqGbtTWd2NtQw/qGrr9uuBv6+WioqLTa2trt/jZiGwrBKqrq4d0d3evAjCS44SjptTg6FvuzPs7/+25PT147SeXo2npR1yRba7rTo7H43VcgYaRazKuAOgTFEI8AA+nCOaZh8Ph8IWLFi3q8bshW0UikUOVUjcCmOV3W9BbCPw9lUrdvH0hEIlEfqWUuozjJEPHT8Cxt/0GBaVswwhySk97G1656ofYvOYzljyl1N8dx/kmS5hh5KBMLQCA3nUCrgdwA3xasCgHuEqpnzqOc6vfDdmZTCwEXNe9KR6PrxBC7I3eOf/at+ulFZWYfs+DeTfaf3d1NG/ES5d+n2uKoHJd95B4PP4+R5hh5JpMLgAAAJFI5Dil1GMAKv1uS5ZpAnC2lHK+3w3pj0wsBJRSo4joGN0wCgRw/J335s08f10bVizFq1f/D9diQS9JKWdwBBlGrsn4O+tEIrG2tLT0z0S0H4DxfrcnGxDR+67rnuA4ziK/29JfiUQilkgkHisvL5+H3mLP7yWGJxFRNUfY/t//IaqOOo4jKi+UjKqAVVCAxo8+4IgbW15e/lYikVjLEWYYuSTjCwAAaG1tbU8kEo+HQiEXwFHwYBOhHNED4OZwOPzdzz77LO0j/Tn0FQJ/KS8vnw8giiwv+sQhR+DAiy7P3eV9PTJyn33RvGolWmWMI25sIpHwZOMmw8hmWfetFIlEDlNKPYA0rheQJZYCOFdKyTaMOhP0vd83Apjpd1t2V2H5YJz04F8wqHyw303JSl1bNuNf3/8Wyy6CrusebMYCGMbnZUUPwLYSiURs9OjRD3Z2dqYAHAog6HebfNamlJozbNiw79bW1tp+N4ZbX4/Ao309AlUAxvndpv468KLLMXLSfn43I2sFi4pQUFoG5z39Rf2IqDSRSDzN0CzDyBlZ1wOwrUgkEgXwc6XU2cjyf8sAvaCU+h/Hcdb53ZB06esRuA4ebiDFYdiEiZj+q/tBlnlapUO5Ll6+4kJs/GSFblQPEY21bZvlmYJh5IKs6wHYViKRaEkkEs+UlZW9QkTjAezhd5vS5FUA50gpb2ttbfV1YZ902zpGIBQKLUCG9giQFcBRc25H8fARfjcl6xERhozbE2vn/ROaG2UElFIdra2tr3C1zTCyXU7cnjiO86aU8igAJwD4t9/t8dAblmUdK6U8Tkr5lt+N8ZOU8m0p5Uz0Lhu9wO/2bKt6xokYMm5Pv5uRM4btuTf2OFZ/Jh8RnYX87Ck0jB3KyQ9DJBI5DMCVSqmvIvuLnB4ATxHRPbZtL/S7MZlKCHEEgBsB+Drnm6wATnrwcZSJqJ/NyDktDesw94KzoVztJbWn5XvxbBhbZfUjgJ3p6yb+aygU+j8ACfR2E5f726rdtg7AbyzL+rZt239MJBLm2eWXSCQSDYlE4pFQKPQSfHw0MPro6Rh34ml+nDqnDRo8BFvWrUXLOu3p/F2JROKfHG0yjGyXkz0AOxAQQhwL4AwAXwMw3Of27EwzgKeUUo84jvMWAK2Hnvmsr0dgNoDpaTspEWbd+2cMrh6btlPmk821qzHvh+fqjgXYEA6HRSbti2EYfsmXAuA/ampqCuLx+DSl1Cz0Lju7r89NWgrgXwD+KaV8BwDL+qdGr3QWAuGph+KoW+70+jR57fWfXI74ove0MizLOjYWi73G0yLDyF55N4e+r/J/pe/P1RUVFaMsyzoCwJFEdDB6CwKvVm7ZjN4L/tsA3nFd9514PN7k0bkMAFLKfwOYIYQ4Er1jBDwrBKpnnORVtNGnevqJ2gWAUmoGgNdYGmQYWSzvegD6IxwO7wFgomVZY5RSY9D7TLkCvY8OhgMoQW/xFOo7ZBMAENEmAO1KKYeI4kqpOIB1RPSJZVkrGxoaZNr/Mcbn9BUCswEcz5lbUFKKrzzxPAKFgzhjje2kujrx3H+fhp62tgFnENH7tm0fzNgsw8hKpgAw8pIQ4nAA14JpQaFxJ56GqZf+mCPK2IX37vo51s7XGsfnAqiQUm5gapJhZKVsnyJnGAPSt47AqQCmAdCeXrnHcVm3VUHWqj5ee8doi2ObZ8PIdqYAMPJa35zweToZBSUlGL7PZKYWGbsyYvJ+KCgp0cpQStUwNccwspYpAAwDmKpz8Mh9D4AVyLvxtL6xAkGMmDRFN+ZAjrYYRjYzBYBhAFp3gxX7m5vJdKuYov2amwLAyHumADDy2qhRoyoAVGpl7GeuJek2an/t13xE326ihpG3TAFg5LVAILCXzvEFpaUYPCbjNiTMeUPG7olgcbFWhuu6ZuCGkddMAWDkNSLS2rYvFB0NsszHKN3IshCKjNaN0Q4wjGxmvrmMvEZE43WOZ7gIGQMUimq/9lUc7TCMbGUKACPfaV0Eyqv24GqHsZvKNQsAIjIFgJHXTAFg5DWlVIXO8Qx3ocYAharMIwDD0GEKACPfjdI5uHj4CK52GLupZITWWwcA5s0z8popAIx8p3URKCgp5WqHsZsYXnu95QQNI8uZAsDId1pzyYLF5hril4DmNECYAsDIc6YAMPJdkc7BumvSGwNnegAMQ48pAIx8N0jnYNMD4J8C/dfevHlGXjMFgGEY+Yr8boBh+MkUAEa+69Y5ONnRztUOYzf16L/2XRztMIxsZQoAI99pFQA97aYA8EtPe5tuhCkAjLxmCgAj32ldRUwPgH9SHR26EebNM/KaKQCMvEZEzTrHM9yFGgPUrf/aa733hpHtTAFg5DXXdTfoHN+xoYmrKcZu6mhq1I0wb56R10wBYOQ1ItK6CCRi9VxNMXZTItagG6FV/BlGtjMFgJHvtK7gLaYA8E1LwzrdCO0Aw8hmpgAw8p3WRSARM9cQv+j2vhDRWqamGEZWMgWAkdeIqFbn+ESsHsp1uZpj9JNyXSSk3iMA13XreFpjGNnJFABGXksmkx/rHN/T3o4ta9dwNcfop01rViGpOQ3QsqzlTM0xjKxkCgAjrzU2NtYBaNHKWLKIpzFGv61f8qFuxGbbtm2OthhGtjIFgJHvFIBlOgGNi00BkG4MBcAy9L73hpG3TAFg5D0iel/n+A3LF0OlUlzNMXbBTSWxYcUS3Zh3OdpiGNnMFACGAfxb5+Ce9nZsWLGUqy3GLjQtW6y9B4NS6m2m5hhG1jIFgJH3gsGgVgEAAGtfnsvRFKMf1r08TzdCua6r/Z4bRrYzBYCR99atW+fg/7V3t8FRXXUYwJ9zN8Fs0osJIGl2N4FqBwRabUvpiECBkVY62lHGD3YGtONgHb/4MsqoFQekLdXRVj+oY2un4sDIlKqlRQbSSJpASICUyEiApLQJSXbvzS7k/Sa7geTe44ekIyMNL73nZndvnt+nfMlz/js7u/e/59x7DtDsJiN2tAr25WFFFdFE7MvDiNVWu41pTCQSFxWUQ5TV2AAQAZBSHnTz/yNDQzCOH1VVDk0gVntYxRHMrt5rIr9gA0AEQAjh+qJwoeKAilLoOtoOub92a5rG9RoisAEgAgCUlJRUw+XxsPF/13NTIA/1tb6H+KmTbmO6YrEYp2qIwAaACADQ0NAwAuANVyFS4twrO9UURNc4u3sHIN09ui+EeA3AqJqKiLIbGwCicVLKPW4zojVVPCLYAwMdbTDqjqiIcv0eE/kFGwCicZ2dnZUAXG0PKx0bTXt2KaqI3te0Z6eKQ5eihmEcVlEPkR+wASD6n1Ep5Q63IW2V5eg536SiHgLQ824z2qsOqYj6MwBu2Ug0jg0A0VWklC8DcPVTUzoOGv7wGx4TrIB0HDT87teQjuvrto2xBoCIxrEBILpKPB5vA7DPbU7PO+fQWv5P9wVNcS0HXkfPeVd7NAEApJR7TdPkzRlEV2EDQHSt51WEnN7xAi7396mImpKG+3rR+Jc/KcnSNE3Je0rkJ2wAiP6PaZpHARx3m3PFGsCJ57e7fnRtKpKOg/rnnsGVQUtFXI1hGK7fTyK/CaS7AKJMVFBQYAoh1rvNGTSiyAkGMWvh3SrKmjKa9uxEywF32zK8Twix0bKsC0rCiHyEMwBEHyAejx8EoOTB88YdL/C44FvQ3XwWZ3a9rCruqGEYlarCiPyEDQDRBBzH2aIkx7Zx7JdbkerpVhHna6meLtQ+vRnSVvK0ngTwExVBRH7EJQCiCQwODrbruj4fgOv5+5HkEOINJzBn9cMITJumoDr/GRkaQvVPv49BI6oq8lXTNH+rKozIb9gAEF1HXl5ebSAQ+CaAPLdZl/t60dV8FmUr10AL8KN3NWd0FEe3/Rjd586oikw5jrNucHCQj2EQTYDfQkTXkUwmB3VdTwF4REleIo6BaDtKl6+CEFyBA8a2Tz72i63orK9TlimEeKqzs9P1fg5EfsYGgOgGLMs6qev6owBKVOQNdLSh70ILwktXQAvkqIjMWs7ICI7/ahtiNVXKMoUQZwoLCx+/dOkSt/0lug42AEQ3JqdPn34awDcACBWBVrQdXecaEfnsyil7T8BIcgg1Wzahs/6YylhbCLGupaWlXWUokR+xASC6CZZlxXRdDwBYqSpzKNEJs74W4aUrkJtfoCo2K6R6ulH95PfQ3XxWaa4QYqthGLuVhhL5FBsAoptkWdYRXdeXAfi4qszLfb3oOFKJGfMXomB2sarYjNZzvglHNv8AVlT5j/Qq0zS/hbHH/4joBtgAEN08GQwGKzRNWw9AVxU6mkyivbIcUjr42F33QAglqwyZR0qcf+NvqHt2C65YA6rTE7m5uQ/39/crDybyKzYARLdgaGhoSNf1/wDYAEX3AwCAlBKXTp9Cz/lm3L74AeTkuX7qMKMM9/WibvvP8O6+f3hxNoIthPhSNBptVB1M5GdsAIhukWVZrbquawBWqc4eNGNofXM/cgtuQ9Gd87J+NkA6DloOvI7ap55Ef1urJ2OMr/vv9CScyMey+9uFKH1EKBR6CcBGrwYounM+7v/OJsyYv9CrITzV+947aPj988pv9LuaEGKXYRiPg+v+RLeMDQDRh5cTCoX2AviiVwMILYA5qx/Cgse+jumlc7waRqmBjjY0vboL7W9VQDqOl0PtM03zKwBGvRyEyK/YABC5EIlEgo7jVABY7uU4QtNQsuQzWLR+I2bM+6SXQ31o/W2taP77X9H+1r8gHc/34Dlu2/aaRCIx5PVARH7FBoDIpUgkMsNxnCMAFnk+mBC4/b4lmLvmEUSWrURg2kc8H/J67MvDiNUeRtuhg4ifOunFDX7XEEKcCQQCD3Z0dPR6PhiRj7EBIFKgtLQ0ZNt2BSajCRiXW1CAyLJVmPu5tZh116cmbVthadu42HgKbYfKYdQdxkgyOSnjAmMXf03TPh+NRs1JG5TIp9gAEClSVlZWNDo6ug8eLwd8kJy8IGYuWITie5eg+N77UfSJeRCamsOGpONgINqGrrONSJx6G/GGeowk0zLzfkII8QXDMLrTMTiR37ABIFIoFArlA3gFwKPprCMnGIQeLoMeKcP0SBn00jLkz5qNnGA+coJBTLtNR04wHwAwmkriyqCF0VQKI6kkUl0XYUU7MBBth2VEYRkdGE2l0vlyAGCfpmmPxWKxtBdC5BdsAIjUC4RCoT8CeCLdhfiBlHJnZ2fnRvBufyKluBEQkXrSsqz9uq47AB4EoGYufuqxhRBbTdP8IQBPnyckmoo4A0DkoUgksspxnN0AStJdS5a5COBrpmlWpLsQIr/iLxMiD8VisWrHcT4N4M1015JFqnJzc+/hxZ/IW5wBIJocIhQK/QjAdnDpbSI2gGdM03x6/G8i8hAbAKJJFA6Hl0opX8Ik7heQDYQQZwA8YRjG8XTXQjRVcAmAaBIZhnGsqKjoPgA/BzCc5nIyQUoIsaWwsHAxL/5Ek4szAERpEg6HIwCelVJuwNT8LO63bfu7iUTiQroLIZqKpuKXDlFGKSkpWSGE2A5gRbprmQxCiMNSys2madamuxaiqYwNAFGGCIVCDwHYCmBZumvxSI0QYpthGJXpLoSI2AAQZZxwOLwUwCYp5ZeR/ffpOEKIvQCe4xo/UWZhA0CUoSKRSNhxnA0Avg1gbprLuVUmgF22bb/INX6izMQGgCjzBUKh0GoAXwWwDsDMNNczkW4Arwkh9hiGUQ0+y0+U0dgAEGWRxYsX58bj8RVSyrUA1gK4O80lnQZQLoQoNwyjBjywhyhrsAEgymLFxcWzNU1bBmC5EOIBjDUEH/VouD4AjVLKt4UQNbZt1yUSiYsejUVEHmMDQOQzJSUlcwAs0DTtDinlHQBKARRjbOlgJoB8ADkA9PF/sTD2yz2JsWn8bgAJAFEhxAXHcVqFEE2maXZM8kshIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIppU/wVwOICzRGGbSgAAAABJRU5ErkJggg==;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;250\&quot; y=\&quot;1612.25\&quot; width=\&quot;78.5\&quot; height=\&quot;78.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-19\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;112.93\&quot; y=\&quot;1590\&quot; width=\&quot;81.57\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-10\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;rotation=90;fillColor=#e1d5e7;strokeColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-19\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-31.930000000000007\&quot; y=\&quot;55\&quot; width=\&quot;73.86\&quot; height=\&quot;10\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-11\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;rotation=90;fillColor=#E5CCFF;strokeColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-19\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-34.06999999999999\&quot; y=\&quot;55\&quot; width=\&quot;120\&quot; height=\&quot;10\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-12\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;rotation=90;fillColor=#CC99FF;strokeColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-19\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-18.96999999999997\&quot; y=\&quot;55\&quot; width=\&quot;120\&quot; height=\&quot;10\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-13\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;rotation=90;fillColor=#B266FF;strokeColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-19\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-4.069999999999993\&quot; y=\&quot;55\&quot; width=\&quot;120\&quot; height=\&quot;10\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;rotation=90;fillColor=#9933FF;strokeColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-19\&quot;&gt;\n          &lt;mxGeometry x=\&quot;39.06999999999999\&quot; y=\&quot;55\&quot; width=\&quot;75\&quot; height=\&quot;10\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-23\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-1\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-21\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;360\&quot; y=\&quot;1660\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;650\&quot; y=\&quot;1076\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-25\&quot; value=\&quot;CPU节点\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;194.5\&quot; y=\&quot;1560\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-28\&quot; value=\&quot;模型\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;150\&quot; y=\&quot;1722\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-29\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;566.12\&quot; y=\&quot;1595\&quot; width=\&quot;342.86\&quot; height=\&quot;140\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-32\&quot; value=\&quot;GPU节点0\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;626.12\&quot; y=\&quot;1585\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-34\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;562.24\&quot; y=\&quot;1843.5\&quot; width=\&quot;344.9\&quot; height=\&quot;140\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-37\&quot; value=\&quot;GPU节点0\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;622.24\&quot; y=\&quot;1833.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-45\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-1\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-29\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;380\&quot; y=\&quot;1680\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;590\&quot; y=\&quot;1390\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-46\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-1\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-34\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;1670\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;577\&quot; y=\&quot;1560\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-47\&quot; value=\&quot;数据并行&amp;#xa;(Data Parallelism, DP)\&quot; style=\&quot;text;whiteSpace=wrap;fontStyle=1;fontSize=17;align=center;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;106\&quot; y=\&quot;1480\&quot; width=\&quot;191.5\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-48\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-50\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-52\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-49\&quot; value=\&quot;随机划分\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-48\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0562\&quot; y=\&quot;-3\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint y=\&quot;-13\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-50\&quot; value=\&quot;数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#60a917;strokeColor=#2D7600;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;106\&quot; y=\&quot;1770.25\&quot; width=\&quot;80\&quot; height=\&quot;89.25\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-51\&quot; value=\&quot;随机小批量\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;255\&quot; y=\&quot;1820.75\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-52\&quot; value=\&quot;随机小批量\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;255\&quot; y=\&quot;1785.75\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-53\&quot; value=\&quot;随机小批量\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;255\&quot; y=\&quot;1747.75\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-54\&quot; value=\&quot;&amp;lt;span style=&amp;quot;font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: nowrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;batch_size&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontColor=#CC0000;fontStyle=1\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;195\&quot; y=\&quot;1815.75\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-62\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1020\&quot; y=\&quot;1590\&quot; width=\&quot;130\&quot; height=\&quot;140\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot; value=\&quot;\&quot; style=\&quot;group\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;560\&quot; y=\&quot;1330\&quot; width=\&quot;340\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-21\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot;&gt;\n          &lt;mxGeometry y=\&quot;10\&quot; width=\&quot;340\&quot; height=\&quot;140\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-68\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-22\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-63\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-22\&quot; value=\&quot;\&quot; style=\&quot;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png,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;\&quot; vertex=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot;&gt;\n          &lt;mxGeometry x=\&quot;28.64\&quot; y=\&quot;35.75\&quot; width=\&quot;78.5\&quot; height=\&quot;78.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-16\&quot; value=\&quot;\&quot; style=\&quot;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png,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;clipPath=inset(20.33% 0% 21.33% 0%);\&quot; vertex=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot;&gt;\n          &lt;mxGeometry x=\&quot;107.13999999999987\&quot; y=\&quot;10\&quot; width=\&quot;102.86\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-26\&quot; value=\&quot;GPU节点0\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot;&gt;\n          &lt;mxGeometry x=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-27\&quot; value=\&quot;模型副本\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot;&gt;\n          &lt;mxGeometry x=\&quot;70\&quot; y=\&quot;130\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-64\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-55\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-63\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-55\&quot; value=\&quot;随机小批量\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot;&gt;\n          &lt;mxGeometry x=\&quot;140.0000000000001\&quot; y=\&quot;80\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-63\&quot; value=\&quot;本地梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; vertex=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot;&gt;\n          &lt;mxGeometry x=\&quot;252.11\&quot; y=\&quot;60\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-65\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;iroXu6kSOUnqGuu2dOUE-67\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-16\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-63\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;220\&quot; y=\&quot;120\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;262\&quot; y=\&quot;95\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-66\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-63\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-62\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;1670\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;580\&quot; y=\&quot;1380\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-81\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-82\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-87\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-82\&quot; value=\&quot;\&quot; style=\&quot;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png,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;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;598.98\&quot; y=\&quot;1620.75\&quot; width=\&quot;78.5\&quot; height=\&quot;78.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-83\&quot; value=\&quot;\&quot; style=\&quot;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png,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;clipPath=inset(20.33% 0% 21.33% 0%);\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;677.4799999999999\&quot; y=\&quot;1595\&quot; width=\&quot;102.86\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-84\&quot; value=\&quot;模型副本\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;636.46\&quot; y=\&quot;1807.75\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-85\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-86\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-87\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-86\&quot; value=\&quot;随机小批量\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;710.3400000000001\&quot; y=\&quot;1665\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-87\&quot; value=\&quot;本地梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;822.45\&quot; y=\&quot;1645\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-88\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-83\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-87\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;790.34\&quot; y=\&quot;1705\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;832.34\&quot; y=\&quot;1680\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-89\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-90\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-95\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-90\&quot; value=\&quot;\&quot; style=\&quot;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png,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;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;597.14\&quot; y=\&quot;1874.25\&quot; width=\&quot;78.5\&quot; height=\&quot;78.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-91\&quot; value=\&quot;\&quot; style=\&quot;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png,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;clipPath=inset(20.33% 0% 21.33% 0%);\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;675.6399999999999\&quot; y=\&quot;1848.5\&quot; width=\&quot;102.86\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-92\&quot; value=\&quot;模型副本\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;638.5\&quot; y=\&quot;1968.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-93\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-94\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-95\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-94\&quot; value=\&quot;随机小批量\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;708.5000000000001\&quot; y=\&quot;1918.5\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-95\&quot; value=\&quot;本地梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;820.61\&quot; y=\&quot;1898.5\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-96\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-91\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-95\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;788.5\&quot; y=\&quot;1958.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;830.5\&quot; y=\&quot;1933.5\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-105\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-87\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-62\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;909\&quot; y=\&quot;1375\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1030\&quot; y=\&quot;1670\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-107\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;iroXu6kSOUnqGuu2dOUE-95\&quot; target=\&quot;iroXu6kSOUnqGuu2dOUE-62\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;913\&quot; y=\&quot;1555\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1030\&quot; y=\&quot;1670\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-108\&quot; value=\&quot;全局梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1030\&quot; y=\&quot;1645\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;iroXu6kSOUnqGuu2dOUE-109\&quot; value=\&quot;&amp;lt;span style=&amp;quot;font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: nowrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;AllReduce&amp;lt;/span&amp;gt;&amp;lt;div&amp;gt;&amp;lt;span style=&amp;quot;font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: nowrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;规约&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontColor=#CC0000;fontStyle=1\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;940\&quot; y=\&quot;1630\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



### 模型并行（大模型）

【2023-8-28】[模型并行最佳实践（PyTorch）](https://zhuanlan.zhihu.com/p/87596314)

DataParallel的优缺点如下：
- 优点：将模型**复制**到所有GPU，其中每个GPU消耗输入数据的不同分区，可以极大地加快训练过程。
- 缺点：不适用于某些**模型太大**而无法容纳单个GPU的用例。

模型并行性（Model parallelism: MP）目的是解决**模型权重不能适应单个节点**的情况，通过将计算和模型参数分布在多台机器上进行训练。
- 数据并行中，每个worker承载整个模型的**完整副本**
- 而模型并行中，每个worker上只分配模型参数的一小部分，从而减少了内存使用和计算。

原理
>- 将单个模型拆分到不同GPU上，而不是在每个GPU上复制整个模型
>- 将模型不同**子网**放置到不同设备上，并相应地实现该 **forward方法**以在设备之间移动中间输出。由于模型的一部分只能在任何单个设备上运行，因此一组设备可以共同为更大的模型服务。

模型 m 包含10层：
- DataParallel: 每个GPU都具有这10层中每层副本
- 而在两个GPU上使用模型并行时，每个GPU可以托管5层

由于深度神经网络通常包含一堆垂直层，因此将一个大型模型逐层拆分感觉很简单，其中一组连续的小层被分组到一个工作层上的一个分区中。然而，通过多个具有顺序依赖性的工作线程来运行每个数据批，会导致大量的**等待时间**和计算资源**利用率低下**的问题。

模型并行有两种：张量并行 和 流水线并行
- 张量并行是在**一个操作**中进行并行计算，如：矩阵-矩阵乘法。
- 流水线并行是在**各层**之间进行并行计算。

总结
- 张量并行是**层内**并行，流水线并行是**层间**并行。


#### 流水线并行（综合模型+数据）

通道并行（Pipeline parallelism: PP）将`模型并行`与`数据并行`相结合，以减少部分训练过程中出现的空闲时间。

主要思想
- 将一个小批量拆分为多个**微批次**，并使worker在每个阶段中能够同时处理一个微批次。需要注意的是，每个微批次需要**两次传递**，一次向前，一次向后。worker之间的通信仅传输激活（向前）和梯度（向后）。这些通道的调度方式以及梯度的聚合方式在不同的方法中有所不同。分区（workers）的数量也称为通道深度。

模型按层分割成若干块，每块都交给一个设备。
- 前向传播: 每个设备将中间激活传递给下一个阶段。
- 后向传播: 每个设备将输入张量梯度传回给前一个流水线阶段。

这允许设备同时进行计算，从而增加训练的吞吐量。
- ![img](https://mmbiz.qpic.cn/mmbiz_png/J0mLianhFicBHEDwE5nPHZKaicqsXBVgES5DlibCDBUbdVthPzoeI9mIVglwvVYick56NFeyhOnRJ6Ly62WPXHgRPvg/640?wx_fmt=png&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1)

缺点
- 训练设备容易出现空闲状态（因为后一阶段等待前一阶段执行完毕），导致计算资源的浪费，加速效率没有数据并行高。
- ![img](https://mmbiz.qpic.cn/mmbiz_png/J0mLianhFicBHEDwE5nPHZKaicqsXBVgES5wlPicE0gibFZYkicXOG7gwQWYDH4xyzf7uW4EAL6h45upGeia8LGZ99Bzg/640?wx_fmt=png&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1)

典型的流水线并行实现：
- GPipe、PipeDream、PipeDream-2BW、PipeDream Flush（1F1B）。

#### 张量并行（水平分割）

模型并行和流水线并行都将一个模型垂直分割，可以将一个张量操作的计算水平分割到多个设备上，称为**张量并行**（tensor parallelism，TP）。
- 张量并行将张量沿特定维度分成 N 块，每个设备只持有整个张量的 1/N，同时不影响计算图的正确性。
- 这需要额外的通信来确保结果的正确性。
- ![](https://mmbiz.qpic.cn/mmbiz_png/J0mLianhFicBHEDwE5nPHZKaicqsXBVgES53FR1KDRnTBHAKwRtd9rEo3TOxgrKA5ZaqBVYZ3QIKGwU2OTW7AklIQ/640?wx_fmt=png&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1)

以当下比较流行的transformer为例，transformer模型主要由多层MLP和自我注意块组成。Megatron-LM（Shoeybi et al.2020）等人采用了一种简单的方法来并行多层计算MLP和自我注意。变压器中的MLP层包含GEMM（通用矩阵乘法）和非线性GeLU传输，按列拆分权重矩阵A

典型的张量并行实现：
- Megatron-LM（1D）
- Colossal-AI（2D、2.5D、3D）


### 多维混合并行 

多维混合并行指将`数据并行`、`模型并行`和`流水线并行`结合起来进行分布式训练。

超大规模模型的预训练和全参数微调时，都需要用到多维混合并行。


#### 2D 并行

主要有
- Data 并行+ pipeline 并行
  - Deepspeed [web-link](https://www.deepspeed.ai/tutorials/pipeline/)给出了 pipeline 和 data-parallel 的2D并行示意图，其中 rank0 和 rank1 为 data-parallelism， rank0里的 gpu-0 和 gpu-2 进行 pipeline 并行，他们交替进行前向和反向过程，疑问的是（这里没有模型运行的最终的loss，如何进行反向传播呢？）
  - ![](https://pic1.zhimg.com/80/v2-aed6e288293f97bfc17ed0b3c9087290_1440w.webp)
- Tensor 并行 + pipeline
  - ![](https://pic1.zhimg.com/80/v2-af38ecbaa5ccb7059c97e8774e484370_1440w.webp)



#### 3D 并行

3D并行 => Tensor + pipeline + data 

![](https://pic1.zhimg.com/80/v2-e3446e66333f5df91b960933965a6c64_1440w.webp)


### 异构系统并行

与 GPU 相比，CPU 内存要大得多。
- 典型服务器上，CPU 可以轻松拥有几百GB甚至上TB的内存，而每张 GPU 卡通常只有 48 或 80 GB的内存。

为什么 CPU 内存没有被用于分布式训练？
- 依靠 CPU 甚至是 NVMe 磁盘来训练大型模型。
- 主要想法: 在不使用张量时，将其卸载回 CPU 内存或 NVMe 磁盘。

通过使用异构系统架构，有可能在一台机器上容纳一个巨大的模型。


### 自动搜索并行空间


#### alpa

[Alpa](https://github.com/alpa-projects/alpa) 将并行空间分为 `inter-op` （pipeline） 与 `intra-op` （tensor并行），使用 NAS搜索这两个空间，考虑整个搜索空间的cost。
- 首先搜索 inter-op 的搜索空间， 制定 pipeline 并行策略
- 然后搜索 intra-op空间， 指定 data-para 与 operator-para 策略（包括两种）
- Data para
- Operator parallel （weight 广播，input拆分）
- Operator parallel （weight 拆分，input拆分） --> 需要增加 all-reduce cost


UCB博士 `郑怜悯` 的工作， 他还参加过其他项目 Ansor，TVM， vLLM， FastChat，LMSYS-Chat-1M
- ![](https://pic1.zhimg.com/80/v2-e76476aa985ccf7bc12fb2c04a60feec_1440w.webp)


## 模型训练开销

神经网络模型占用的显存包括：
- 模型自身的参数
- 模型的输出

全连接网络(不考虑偏置项b): Y = XW + b
- X 是 B*M 维
- W 是 M*N 或 N*M 维
- Y 是 B*N 维

显存占用包括：
- 参数：二维数组 W
- 模型的输出： 二维数组 Y
- X是上一层的输出，因此显存占用归于上一层。

显存占用就是W和Y两个数组？非也


### 模型训练流程


<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-05-11T07:43:47.099Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36\&quot; etag=\&quot;dPvaBv-ThdCmPTVmmKJL\&quot; version=\&quot;24.4.0\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;-408\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; value=\&quot;分布式训练\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;620.71\&quot; y=\&quot;1200\&quot; width=\&quot;224.5\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;260\&quot; y=\&quot;1465.5\&quot; width=\&quot;240\&quot; height=\&quot;143\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-15\&quot; value=\&quot;CPU节点\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#6666FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380\&quot; y=\&quot;1450\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-3\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-16\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-7\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-9\&quot; value=\&quot;随机划分\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;tbJsgM7FzyQLb-bkkZpG-3\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.0562\&quot; y=\&quot;-3\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint y=\&quot;-11\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-18\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-16\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-17\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-16\&quot; value=\&quot;数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#60a917;strokeColor=#2D7600;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;280\&quot; y=\&quot;1693\&quot; width=\&quot;80\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-20\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-17\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-19\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-17\&quot; value=\&quot;模型权重\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f8cecc;strokeColor=#b85450;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;285\&quot; y=\&quot;1330\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-20\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;662.86\&quot; y=\&quot;1305\&quot; width=\&quot;377.14\&quot; height=\&quot;135\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-13\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-78\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-14\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-22\&quot; value=\&quot;GPU节点0\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;765.6800000000001\&quot; y=\&quot;1290\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-23\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-14\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-20\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;565\&quot; y=\&quot;1535\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;595\&quot; y=\&quot;990\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-33\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-14\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-21\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;565\&quot; y=\&quot;1535\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;662.8600000000001\&quot; y=\&quot;1537\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-35\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-14\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-30\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;550\&quot; y=\&quot;1540\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;662.8600000000001\&quot; y=\&quot;1757.5\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-2\&quot; value=\&quot;随机小批量数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;429\&quot; y=\&quot;1733\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-11\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-5\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-78\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;830\&quot; y=\&quot;1390\&quot; /&gt;\n              &lt;mxPoint x=\&quot;830\&quot; y=\&quot;1360\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-5\&quot; value=\&quot;随机小批量数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;697.96\&quot; y=\&quot;1360\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-7\&quot; value=\&quot;随机小批量数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;429\&quot; y=\&quot;1698\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-8\&quot; value=\&quot;随机小批量数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;429\&quot; y=\&quot;1660\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-10\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-77\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-78\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-77\&quot; value=\&quot;模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;687.28\&quot; y=\&quot;1315\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-78\&quot; value=\&quot;本地梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;880\&quot; y=\&quot;1345\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-79\&quot; value=\&quot;优化器\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;924.3199999999999\&quot; y=\&quot;1400\&quot; width=\&quot;71.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;MzKt8NfVXthm0VmUftic-80\&quot; value=\&quot;激活函数\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;834.32\&quot; y=\&quot;1400\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-63\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-14\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-62\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-14\&quot; value=\&quot;小批量随机梯度下降\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1120\&quot; y=\&quot;1498.5\&quot; width=\&quot;100\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-57\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=1;entryY=0;entryDx=0;entryDy=30;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-15\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-16\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-15\&quot; value=\&quot;全局梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#C3ABD0;strokeColor=#C3ABD0;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;415\&quot; y=\&quot;1494.5\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-16\&quot; value=\&quot;模型\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f8cecc;strokeColor=#b85450;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;290\&quot; y=\&quot;1480\&quot; width=\&quot;60\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-17\&quot; value=\&quot;数据\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;290\&quot; y=\&quot;1535\&quot; width=\&quot;60\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-19\&quot; value=\&quot;全部模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;407.64\&quot; y=\&quot;1345\&quot; width=\&quot;112.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-21\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;670\&quot; y=\&quot;1473.5\&quot; width=\&quot;377.14\&quot; height=\&quot;135\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-22\&quot; value=\&quot;GPU节点1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;772.82\&quot; y=\&quot;1458.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-23\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-24\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-27\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;837.14\&quot; y=\&quot;1558.5\&quot; /&gt;\n              &lt;mxPoint x=\&quot;837.14\&quot; y=\&quot;1528.5\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-24\&quot; value=\&quot;随机小批量数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;705.1\&quot; y=\&quot;1528.5\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-25\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-26\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-27\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-26\&quot; value=\&quot;模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;694.42\&quot; y=\&quot;1483.5\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-27\&quot; value=\&quot;本地梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;887.14\&quot; y=\&quot;1513.5\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-28\&quot; value=\&quot;优化器\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;931.4599999999999\&quot; y=\&quot;1568.5\&quot; width=\&quot;71.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-29\&quot; value=\&quot;激活函数\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;841.46\&quot; y=\&quot;1568.5\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-30\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;670\&quot; y=\&quot;1668\&quot; width=\&quot;377.14\&quot; height=\&quot;135\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-31\&quot; value=\&quot;GPU节点2\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;772.82\&quot; y=\&quot;1653\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-32\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-33\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-36\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;837.14\&quot; y=\&quot;1753\&quot; /&gt;\n              &lt;mxPoint x=\&quot;837.14\&quot; y=\&quot;1723\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-33\&quot; value=\&quot;随机小批量数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;705.1\&quot; y=\&quot;1723\&quot; width=\&quot;70\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-34\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-35\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-36\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-35\&quot; value=\&quot;模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;694.42\&quot; y=\&quot;1678\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-36\&quot; value=\&quot;本地梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;887.14\&quot; y=\&quot;1708\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-37\&quot; value=\&quot;优化器\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;931.4599999999999\&quot; y=\&quot;1763\&quot; width=\&quot;71.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-38\&quot; value=\&quot;激活函数\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;841.46\&quot; y=\&quot;1763\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-39\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;strokeColor=#EA6B66;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-19\&quot; target=\&quot;MzKt8NfVXthm0VmUftic-77\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;1370\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;428\&quot; y=\&quot;1370\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-40\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;strokeColor=#EA6B66;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-19\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-26\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;520\&quot; y=\&quot;1370\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;697\&quot; y=\&quot;1340\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-41\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;strokeColor=#EA6B66;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-19\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-35\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;530\&quot; y=\&quot;1380\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;707\&quot; y=\&quot;1350\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-42\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;strokeColor=#97D077;exitPerimeter=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-7\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;520\&quot; y=\&quot;1370\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;697\&quot; y=\&quot;1340\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-43\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;dashPattern=1 1;strokeColor=#97D077;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-24\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;500\&quot; y=\&quot;1730\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;708\&quot; y=\&quot;1400\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-44\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;strokeColor=#97D077;exitPerimeter=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-7\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-33\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;519\&quot; y=\&quot;1748\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;718\&quot; y=\&quot;1410\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-45\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-27\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-14\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;960\&quot; y=\&quot;1370\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1160\&quot; y=\&quot;1446\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-46\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tbJsgM7FzyQLb-bkkZpG-36\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-14\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;967\&quot; y=\&quot;1539\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1160\&quot; y=\&quot;1446\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-48\&quot; value=\&quot;局部模型权重\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;407.64\&quot; y=\&quot;1384\&quot; width=\&quot;112.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-49\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;entryPerimeter=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;MzKt8NfVXthm0VmUftic-17\&quot; target=\&quot;tbJsgM7FzyQLb-bkkZpG-16\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;330\&quot; y=\&quot;1703\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;330\&quot; y=\&quot;1595\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-50\&quot; value=\&quot;计算损失loss\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;880\&quot; y=\&quot;1308\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-51\&quot; value=\&quot;计算损失loss\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;885.68\&quot; y=\&quot;1473.5\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-52\&quot; value=\&quot;计算损失loss\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;880\&quot; y=\&quot;1668\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-53\&quot; value=\&quot;均匀分发数据到GPU节点\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=13;fontColor=#6666FF;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;480\&quot; y=\&quot;1803\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-54\&quot; value=\&quot;聚合局部梯度得到全局梯度\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=13;fontColor=#6666FF;labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1170\&quot; y=\&quot;1568.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-56\&quot; value=\&quot;分发最新权重到GPU节点\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=13;fontColor=#6666FF;labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;464\&quot; y=\&quot;1330\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-58\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(102, 102, 255); font-family: Helvetica; font-size: 13px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: nowrap; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;更新模型权重&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;355\&quot; y=\&quot;1473.5\&quot; width=\&quot;82.72\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-60\&quot; value=\&quot;&amp;lt;span style=&amp;quot;font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: nowrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;batch_size&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontColor=#CC0000;fontStyle=1\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;369\&quot; y=\&quot;1728\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-61\&quot; value=\&quot;&amp;lt;span style=&amp;quot;font-family: Helvetica; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: nowrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;累积梯度&amp;amp;nbsp;&amp;lt;/span&amp;gt;&amp;lt;span style=&amp;quot;background-color: rgb(255, 255, 255); font-size: 11px; text-align: center; text-wrap: nowrap;&amp;quot;&amp;gt;gradient_accumulate&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontColor=#CC0000;fontStyle=1;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1110\&quot; y=\&quot;1578.5\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tbJsgM7FzyQLb-bkkZpG-62\&quot; value=\&quot;全局梯度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#C3ABD0;strokeColor=#C3ABD0;shadow=1;fontSize=17;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1270\&quot; y=\&quot;1513.5\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



### 参数的显存占用

【2023-8-30】大模型要占你多少内存？[这个神器一键测量，误差低至0.5MB，免费可用](https://mp.weixin.qq.com/s/U4VpmHuKvHKu3AuwXM3PYw)

大模型训练推理要用多少内存？
- HuggingFace Space上的最新火起来工具——[Model Memory Calculator](https://huggingface.co/spaces/hf-accelerate/model-memory-usage)，模型内存测量器，在网页端人人可体验。
- 比如模型bert-base-case Int8估计占用413.18 MB内存，实际占用为413.68MB，相差0.5MB，误差仅有0.1%。

实际推理过程，EleutherAI 发现需要在预测数据基础上，预留20%的内存

【2023-8-30】[baichuan-7b](https://huggingface.co/baichuan-inc/Baichuan-7B/tree/main) （14G） 部署失败，空间不够
- GPU: A30, 24G 显存

错误信息:

```sh
torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 86.00 MiB (GPU 0; 22.20 GiB total capacity; 7.47 GiB already allocated; 51.12 MiB free; 7.48 GiB reserved in total by PyTorch) If reserved memory is >> allocated memory try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF
```

[Model Memory Calculator](https://huggingface.co/spaces/hf-accelerate/model-memory-usage)计算的开销

Memory Usage for ‘baichuan-inc/Baichuan-7B’

| dtype | Largest Layer or Residual Group | Total Size | Training using Adam |
| --- | --- | ---- | ---- |
| float32 | 1000.0 MB | 26.2 GB | 104.82 GB |
| float16/bfloat16 | 500.0 MB | 13.1 GB | 52.41 GB | 
| int8 | 250.0 MB | 6.55 GB | 26.2 GB |
| int4 | 125.0 MB | 3.28 GB | |

只有有参数的层，才会有显存占用。这部份的显存占用和输入无关，模型加载完成之后就会占用。

有参数的层主要包括：
- 卷积
- 全连接 
- BatchNorm
- Embedding层
- ... ...
    
无参数的层：
- 多数的激活层(Sigmoid/ReLU)
- 池化层
- Dropout
- ... ...
    
模型参数数目(不考虑偏置项b)为：
- Linear(M->N): 参数数目：M×N
- Conv2d(Cin, Cout, K): 参数数目：Cin × Cout × K × K
- BatchNorm(N): 参数数目： 2N
- Embedding(N,W): 参数数目： N × W

参数占用显存 = 参数数目 × n
- n = 4 ：float32 
- n = 2 : float16 
- n = 8 : double64

PyTorch中，当执行完 model=MyGreatModel().cuda() 后就会占用相应的显存，占用的显存大小基本与上述分析的显存差不多（会稍大一些，因为其它开销）。

### 梯度与动量的显存占用

优化器
- SGD：W_t+1 = W_t - α * ▽ F(W_t)
  - 除了保存权重W, 还要保存对应的**梯度** ▽ F(W_t) ，因此， 显存占用等于参数占用显存 **x2**
- 带Momentum-SGD：
  - v_t+1 = ρv_t + ▽ F(W_t)
  - W_t+1 = W_t - α * v_t+1
  - 还需要保存**动量**， 因此显存 **x3**
- Adam优化器
  - 动量占用的显存更多，显存x4

总结，模型中与输入无关的显存占用包括：
- **参数** W
- **梯度** dW（一般与参数一样）
- 优化器的**动量**
  - 普通SGD没有动量，momentum-SGD动量与梯度一样，Adam优化器动量的数量是梯度的**两倍**

### 输入输出的显存占用

以CNN为例，模型输出的显存占用，总结如下：
- 需要计算每一层的feature map的形状（多维数组的形状）
- 需要保存输出对应的梯度用以反向传播（链式法则）
- 显存占用与 batch size 成正比
- 模型输出不需要存储相应的动量信息。
    
深度学习中神经网络的显存占用，可以得到如下公式：
> 显存占用 = 模型显存占用 + batch_size × 每个样本的显存占用

显存不是和batch-size简单的成正比，尤其是模型自身比较复杂的情况下：比如全连接很大，Embedding层很大

另外需要注意：
- 输入（数据，图片）一般不需要计算梯度
- 神经网络每层输入/输出都需要保存下来，用来**反向传播**，但是在某些特殊的情况下，不要保存输入。
  - 比如 ReLU，PyTorch中，使用nn.ReLU(inplace = True) 能将激活函数ReLU的输出直接覆盖保存于模型的输入之中，节省不少显存。
  - 这时候是如何反向传播? （提示：y=relu(x) -> dx = dy.copy();dx[ y<=0 ] =0）
    
### 节省显存的方法

深度学习中，一般占用显存最多的是卷积等层的输出，模型参数占用的显存相对较少，而且不太好优化。

节省显存方法：
- 降低 batch-size
- 下采样 (NCHW -> (1/4)*NCHW)
- 减少全连接层（一般只留最后一层分类用的全连接层

更多信息见[原文](https://juejin.cn/post/6844903640558206984)

训练时显存不足怎么办？

常见的节省显存操作，优先级从高到低排列。
1. 去掉 compute_metrics：
  - 有些代码会在输出层后计算rouge分等，这个会输出一个 `batch_size`*`vocab_size`*`seq_len` 的一个大向量，非常占显存。
1. 采用`bf16`/`fp16`进行混合精度训练：
  - 现在大模型基本上都采用 bf16 来进行训练
  - 但是 v100 不支持 bf16，可以采用fp16进行训练。显存占用能够降低1倍。
1. `Flash attention`：不仅能够降低显存，更能提高训练速度。
1. `batch_size` 调小：
  - batch size 与模型每层激活状态所占显存呈**正相关**
  - 降低 batch size 能够很大程度上降低这部分显存占用。
1. 采用**梯度累积**：
  - `global_batch_size` = `batch_size` * `梯度累积`
  - 如果降低 batch_size 后想保持 global_batch_size 不变，可适当提高梯度累积值。
1. 选择合适的**上下文长度**：
  - 上下文长度与激活状态所占显存呈**正相关**
  - 因此可适当降低上下文长度来降低显存占用。
1. `DeepSpeed Zero`：
  - 显存占用从高到低为：`Zero 1` > `Zero 2` > `Zero 2` + `offload` > `zero 3` > `zero 3` + `offload`
  - 推荐最多试到 `Zero2` + `offload`。
1. 选择更小的基座模型：在满足需求的情况下，尽量选择更小的基座模型。
 
慎重选择：
1. `Lora`: 能跑**全参**就别跑 `Lora` 或 `Qlora`，一方面是麻烦，另一方面的确是效果差点。
1. `Qlora`: Qlora 速度比lora慢，但所需显存更少，实在没资源可以试试。
1. `Megatron-LM`: 可采用**流水线**并行和**张量**并行，使用比较麻烦，适合喜欢折腾的同学。
1. `Pai-Megatron-LM`: Megatron-LM 的衍生，支持 Qwen 的sft和pt，坑比较多，爱折腾可以试试。
1. **激活检查点**：不推荐，非常耗时。在反向传播时重新计算深度神经网络的中间值。用时间（重新计算这些值两次的时间成本）来换空间（提前存储这些值的内存成本）。

### GPU 要存哪些参数

【2023-6-28】[参考](https://mp.weixin.qq.com/s/pUcXaCwCqGCw3KOt-fgH-w)

模型训练中，GPU 要存储的参数
- 模型本身的参数、优化器状态、激活函数的输出值、梯度、一些零时的Buffer
- ![img](https://mmbiz.qpic.cn/mmbiz_png/J0mLianhFicBHEDwE5nPHZKaicqsXBVgES5IexNgeadmAcMFdNofrszbpgXNHjicV8QDWciaVpIXndGZ8hDNATT68JQ/640?wx_fmt=png&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1)

模型参数仅占所有数据的小部分
- 当进行**混合精度**运算时，模型状态参数(优化器状态 + 梯度+ 模型参数）占大半以上。

因此，要想办法去除模型训练过程中的冗余数据。

#### LLaMA-6B 占用多大内存

【2023-7-13】LLaMA-6B 占用多大内存？计算过程

精度对所需内存的影响：
- **fp32**精度，一个参数需要 32 bits, **4** bytes.
- **fp16**精度，一个参数需要 16 bits, **2** bytes.
- **int8**精度，一个参数需要 8 bits, **1** byte.

模型需要的RAM大致分三个部分：
- **模型参数**： 参数量*每个参数所需内存
  - 对于fp32，LLaMA-6B需要 6B*4 bytes = 24GB 内存
  - 对于int8，LLaMA-6B需要 6B*1 byte = 6GB 内存
- **梯度**： 参数量*每个梯度参数所需内存
- **优化器**参数： 不同的优化器所储存的参数量不同。
  - 对于常用的AdamW，需要储存**两倍**的模型参数（用来储存一阶和二阶momentum）。
  - fp32 的 LLaMA-6B，AdamW需要 6B*8 bytes = 48 GB
  - int8 的 LLaMA-6B，AdamW需要 6B*2 bytes = 12 GB
- 其它
  - CUDA kernel也会占据一些RAM，大概1.3GB左右

综上，int8 精度的 LLaMA-6B 模型部分大致需要 6GB + 6GB + 12GB + 1.3GB = 25.3GB 左右。

再根据LLaMA的架构(hidden_size= 4096, intermediate_size= 11008, num_hidden_layers= 32, context_length = 2048)计算中间变量内存。每个instance需要： ( 4096+11008 ) * 2048 * 32 * 1 byte = 990 MB

所以，一张 A100（**80GB** RAM）大概可以在int8精度，batch_size = 50 的设定下进行全参数训练。

附
- 消费级显卡内存和算力查询: [2023 GPU Benchmark and Graphics Card Comparison Chart](https://www.gpucheck.com/gpu-benchmark-graphics-card-comparison-chart)

#### 7B 占用多大内存

一个**7B**规模大模型（如LLaMA-2 7B），基于**16-bit**混合精度训练时
- 仅考虑模型参数、梯度、优化器情况下，显存占用就有**112GB**
  - 参数占 GPU 显存近 **14GB**（每个参数2字节）。
  - 训练时**梯度**存储占**14GB**（每个参数对应1个梯度，也是2字节）
  - 优化器Optimizer（假设是主流的AdamW）则是**84GB**（每个参数对应1个参数copy、一个momentum和一个variance，这三个都是float32）
    - 2byte 模型**静态**参数权重（以16bit存储） = 14G
    - 2byte 模型**更新**参数权重 （以16bit存储）= 14G
    - 2byte **梯度**（以16bit存储）= 14G
    - 2byte **梯度更新**（以16bit存储）= 14G
    - 4byte **一阶动量**优化器更新（以32bit存储）= 28G
    - 4byte **二阶方差**优化器更新（以32bit存储）= 28G
  - 目前，合计 112GB
  - 还有：前向传播时激活值，各种临时变量
  - 还与sequence length, hidden size、batch size都有关系。
- 目前<span style='color:red'>A100、H100这样主流显卡单张是放不下</span>，更别提国内中小厂喜欢用的A6000/5000、甚至消费级显卡。

#### Adam + fp16 混合精度预估

【2023-6-29】[LLM Training GPU显存耗用量估计](https://zhuanlan.zhihu.com/p/638199667)，以Adam + fp16混合精度训练为例，分析其显存占用有以下四个部分
- (1) 模型权重 Model
  - Prameters (FP16) 2 bytes
  - Gradients (FP16) 2 bytes
- (2) 前向激活值 Activations
  - 前向过程中存储, y = w1 * x, 存储x用于计算w1梯度
  - 整体显存占用与batch有关
- (3) 优化器 Optimizer：梯度、动量等
  - Master Weight (FP32) 4 bytes
  - Adam m (FP32) 4 bytes
  - Adam v (FP32) 4 bytes
- (4) 临时混存 Buffer & Fragmentation

(1) 和 (3) 可以精确估计
- 显存占用大头是 **Adam 优化器**，占可计算部分的 12/16=75%
- 其次是**模型参数**+**梯度**，显存容量至少是参数量的**16倍**

Adam + fp16混合精度训练
- ![](https://pic1.zhimg.com/80/v2-b4b2b377eeac7222bd783f9505c1115c_1440w.webp)
- ![](https://pic3.zhimg.com/80/v2-fbcc4e6eb4de305a46f5a79e98d41cda_1440w.webp)

结论：
- 不考虑Activation，3090 模型容量上限是 24/16=**1.5B**，A100 模型容量上限是 80/16=**5B**
  - 假设训练过程中batchsize恒定为1，也即尽最大可能减少Activation在显存中的占用比例，使得理论计算值16Φ更接近真实的显存占用，那么24G的3090的模型容量上限是1.5B（差不多是GPT-2的水平），80G的A100的模型容量上限是5B
- 考虑Activation，3090的模型容量上限是 0.75B，A100的容量上限是 2.5B
  - batchsize为1的训练效率非常低，batchsize大于1才能充分发挥GPU的效率，此时Activation变得不可忽略。经验之谈，一般需要给Activation预留一半的显存空间（比如3090预留12G，A100预留40G），此时3090的模型容量上限是0.75B，A100的容量上限是2.5B，我们实际测试结果接近这个值
- [1B, 5B] 是目前市面上大多数GPU卡的分水岭区间
  - [0, 1B) 市面上绝大多数卡都可以直接硬train一发
  - [1B, 5B] 大多数卡在这个区间的某个值上触发模型容量上限，具体触发值和显存大小有关
  - (5B, ~) 目前没有卡能裸训


### LLM 推理显存开销

【2024-8-24】[为大型语言模型 (LLM) 提供服务需要多少 GPU 内存？](https://zhuanlan.zhihu.com/p/716347923?utm_psn=1811748062424592385)

运行一个大型语言模型，需要多大GPU内存？

GPU 内存估算公式
- $ M=(P*4B)/(32/Q)*1.2 $
- ![](https://pic2.zhimg.com/80/v2-0b643b18fb67b7ea106b63b7d0e92101_1440w.webp)

解释
- M 代表 GPU 内存的大小，单位是吉字节。
- P 指的是模型中包含的参数总数。
- 4B 指的是每个参数平均占用的存储空间，为 4 个字节。
- Q 表示加载模型时使用的位数，可以是 16 位或者 32 位。
- 1.2 表示在计算中加入了 20% 的额外空间以应对可能的需求。


![](https://pic2.zhimg.com/80/v2-919d5943cf2ddcc5ffa23f93acaecf3b_1440w.webp)

分解公式
- 模型参数量 (P)：这个指标反映了你的模型规模。比如，如果你使用的是 LLaMA 模型，它包含 700 亿个参数，那么这个参数量就是 700 亿。
- 参数内存需求 (4B)：通常情况下，每个模型参数需要 4 个字节的存储空间，这是因为浮点数通常需要 4 个字节（即 32 位）来表示。如果你采用的是半精度（16 位）格式，那么所需的内存量会相应减少。
- 参数位宽 (Q)：这个值取决于你是以 16 位还是 32 位的精度来加载模型。16 位精度在许多大型语言模型的应用中较为普遍，因为它在保证足够精度的同时，能够降低内存的消耗。
- 额外开销 (1.2)：乘以 1.2 的系数是为了增加 20% 的额外空间，以应对在模型推理过程中可能需要的额外内存。这不仅仅是为了安全起见，更是为了确保在模型执行过程中，激活操作和其他中间结果的内存需求得到满足。

**700亿**个参数（以 **16位**精度加载）的 LLaMA 模型提供服务所需的内存：
- M = (P * 4B)/(32/Q) * 1.2 = (70 * 4 bytes)/(32/16) * 1.2 = 168 GB
- 单块 NVIDIA A100 GPU，尽管配备了 80 GB 显存，但仍然不足以支撑该模型的运行。为了高效地处理内存需求，至少需要**两块** A100 GPU，每块都具备 80 GB 的显存容量。


## 内存/显存优化

显存优化技术：[参考](https://mp.weixin.qq.com/s/7wtwsNhf27YzALnSFXTmkA)
- `重计算`(Recomputation)：Activation checkpointing(Gradient checkpointing)本质上是一种用**时间换空间**的策略。
- `卸载`（Offload）技术：一种用通信换显存的方法，简单来说就是让模型参数、激活值等在CPU内存和GPU显存之间左右横跳。如：ZeRO-Offload、ZeRO-Infinity等。
- `混合精度`（BF16/FP16）：降低训练显存的消耗，还能将训练速度提升2-4倍。
  - BF16 计算时可避免计算溢出，出现Inf case。
  - FP16 在输入数据超过65506 时，计算结果溢出，出现Inf case。


### CPU卸载
 
当GPU内存已满时，一种选择是将暂时未使用的数据卸载到CPU，并在以后需要时将其读回（Rhu等人，2016）。数据卸载到CPU 的想法很简单，但由于它会延长训练时间，所以近年来不太流行。
 
### 激活重新计算
 
激活重新计算（Activation recomputation (also known as “activation checkpointing” or “gradient checkpointing”，Chen等人，[2016年](https://arvix.org/abs/1604.06174)）是一个以计算时间为代价减少内存占用的聪明而简单的想法

### 混合精度训练
 

Narang&Micikevicius等人（2018年）介绍了一种使用半精度浮点（FP16）数字训练模型而不损失模型精度的方法。

三种避免以半精度丢失关键信息的技术：
- 1）全精度原始权重。维护累积梯度的模型权重的全精度 (FP32) 副本， 对于向前和向后传递，数字四舍五入到半精度。主要是为了防止每个梯度更新（即梯度乘以学习率）可能太小而无法完全包含在 FP16 范围内（即 2-24 在 FP16 中变为零）的情况。
- 2）损失缩放。扩大损失以更好地处理小幅度的梯度（见图 16）， 放大梯度有助于将权重移动到可表示范围的右侧部分（包含较大值）占据更大的部分，从而保留否则会丢失的值。
- 3）算术精度。对于常见的网络算法（例如向量点积，向量元素相加减少），可以将部分结果累加到 FP32 中，然后将最终输出保存为 FP16，然后再保存到内存中。可以在 FP16 或 FP32 中执行逐点操作。

大模型训练过程中，GPU显存占用主要分成Model States 与 Activation 两部分

混合精度训练流程：通过引入fb16以及bf16精度来减少fb32精度带来的显存消耗。
- 存储一份fp32的parameter，momentum和variance（统称model states）
- 在forward开始之前，额外开辟一块存储空间，将fp32 parameter减半到fp16 parameter；
- 正常做forward和backward，在此之间产生的activation和gradients，都用fp16进行存储；
- 用fp16 gradients去更新fp32下的model states；
- 当模型收敛后，fp32的parameter就是最终的参数输出；

混合精度下的显存：
- ![](https://pic2.zhimg.com/v2-37133eb29fc4da4432a1a57a6138192d_b.jpg)

通常模型会使用float32(fp32)精度进行训练，但是随着模型越来越大，训练的硬件成本和时间成本急剧增加。而混合精度训练通过利用float16(fp16)的优点并规避缺点来进行训练。

fp32,fp16,bf16的区别如下图所示
- ![](https://pic1.zhimg.com/80/v2-278e19aa63962ee80cdead8e714c391c_1440w.webp)


优点：
1. 降低显存占用，float16比float32小一半；
2. 减少网络通信开销；
3. 硬件针对fp16优化，速度更快

缺点： 
1. 下溢。float16最大的问题是"下溢"。
  - 模型更新通常随着模型训练，值往往会很小，可能会超出float16表示的精度。
  - 结果就是：大多数的模型权重都不再更新，模型难以收敛。
2. 舍入误差。
  - 模型权重和梯度相差太大，通过梯度更新权重并进行舍入时，可能导致更新前和更新后的权重没有变化。

bf16是一种全新的数字格式，更加支持深度学习计算，但需要硬件支持，如NVIDIA A100, NVIDIA A800等

此外，官方文档中提到了AMP(Auto Mixed Precision 自动混合精度训练) ，与ZeRO不能同时使用




#### Int8 

Int8 - bitsandbytes

Int8是个很极端的数据类型，最多只能表示-128～127的数字，并且完全没有精度。

为了在训练和inference中使用这个数据类型，bitsandbytes使用了两个方法最大程度地降低了其带来的误差：
- vector-wise quantization
- mixed precision decompasition

Huggingface 用[动图](https://huggingface.co/blog/hf-bitsandbytes-integration)解释了quantization的实现
- [paper](https://arxiv.org/abs/2208.07339)

借助Huggingface PEFT，使用int8训练opt-6.5B的完整流程, [notebook](https://github.com/huggingface/peft/blob/main/examples/int8_training/Finetune_opt_bnb_peft.ipynb)

#### FP 16

Fp16 - mixed precision
- 混合精度训练大致思路: 在 **forward** pass 和 **gradient computation** 时用 fp16 来加速，但是在**更新参数**时使用 fp32。
- ![](https://pic3.zhimg.com/80/v2-3f4e34dc3281e47d176fe3adc25c66b2_720w.webp)
- [Pytorch 官方示例](https://pytorch.org/docs/stable/notes/amp_examples.html)

torch fp16推理：直接使用model.half()将模型转换为fp16.

```py
model.eval()
model.half() # 半精度
```

Huggingface Transformers：[fp16-training](https://huggingface.co/docs/transformers/perf_train_gpu_one#fp16-training)
- TrainingArguments 里声明 fp16=True

```py
training_args = TrainingArguments(per_device_train_batch_size=4, fp16=True, **default_args)

trainer = Trainer(model=model, args=training_args, train_dataset=ds)
result = trainer.train()
print_summary(result)
```

### 压缩
 
中间结果通常会消耗大量内存，尽管它们只在一次向前传递和一次向后传递中需要。这两种使用之间存在明显的时间差距。因此Jain等人（2018年）提出了一种数据编码策略，将第一次使用后的中间结果在第一次传递中进行压缩，然后将其解码回来进行反向传播。

### 内存高效优化器
 
优化器内存消耗。以流行的 Adam 优化器为例，它内部需要保持动量和方差，两者都与梯度和模型参数处于同一规模，但是需要节省 4 倍的模型权重内存。

# 分布式机器学习实现

【2022-6-2】[分布式机器学习](https://zhuanlan.zhihu.com/p/365662727)
- ![](https://pic1.zhimg.com/v2-8e4eefe63cc256d4420a881a00f2851f_1440w.jpg)

在深度学习时代，训练数据特别大的时候想要**单卡**完成训练基本是不可能的。所以就需要进行**分布式**深度学习。


## 经验

流水并行 (Pipeline Parallelism ) 是 LLM 分布式训练扩展到千卡集群以上的一个核心 feature

### 并行度对比

NVIDIA 在 3076 张 A100 集群上训练的 1T 参数量 LLM 使用的并行方式是：
- Data Parallel Size = 6
- Tensor Parallel Size = 8
- Pipeline Parallel Size = 64

并行度最高的是 流水并行，超过 DP 和 TP 10倍左右

### 为什么3k卡集群主流是流水并行？ 

流水并行核心优势：
- 用比较少的 **Pipeline Bubble** 代价 （当 gradient accumulation step 很大时可以忽略不计），较少的 **Tensor Buffer 显存**代价，以及非常低的**通信开销**，将大模型分割在不同的 Group 中。 大幅减少了单张 GPU 上的 weight tensor 大小（数量） 和 Activation tensor 大小（数量）。 
- 跟 Tensor Parallel 相比， Pipeline Parallel 的通信代价很低且可以被 overlap， Tensor Parallel 虽然也能切分模型大小，但是需要全量数据（没有减少 Activation tensor 大小），另外极高的通信频率和通信量使得 Tensor Parallel 只能在机器内 8 张卡用 NVLink 等高速互联来实现，跨机的 TP 会严重拖慢速度。
- 不仅如此， Pipeline Parallel 还将 Data Parallel 的模型更新限定在一个很小的范围内（比如六台机器）， DP 所需的 AllReduce 通信会随着机器数量增多而变慢。 PP 也让 DP 所需同步的模型梯度大小变小了，大大减缓了模型更新对于训练速度的影响。

因此  Pipeline Parallel  是让模型可以达到千亿、集群可以扩充到千卡以上的一个最重要的特性。


流水并行有很重要的约束条件：
- 需要一个 **规整对称的、线性顺序**的网络结构。

GPT 就是这样一个典型的网络结构： 
- 完全一样的 Transformer Layer 顺序堆叠，没有分叉和不对称情况，当均匀切分 Layer 时，各个 Stage 的前向/反向计算时间均一致。

作者：成诚
链接：https://www.zhihu.com/question/588325646/answer/3422090041
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

流水并行训练时的 time line 参考如下：
- ![](https://picx.zhimg.com/80/v2-8d4082c21f26f428da6edf8bf67f0ec1_1440w.webp?source=2c26e567)

（反向的计算时间是前向的两倍）整个集群最高效的训练时间段是 step 4、5、6、7 的前向 和 step 0、1、2、3 的反向同时在所有 stage 上并行计算的时候，这个时候集群没有空闲，全部都在并行执行。 当我们增加 acc step （比如从 8 增加到 64）时，中间部分完美并行的时间段占比就会更长， bubble time 的占比就会越来越小。

而 T5 的网络结构比 GPT 要复杂很多， T5 是 Encoder-Decoder 架构，整个网络分为两大块，且 Encoder 和 Decoder 的 Transformer Layer 参数大小、Attention 计算量、Context Length 等均不一致，导致 Encoder 的理论计算量要比 Decoder 大很多（整个网络不是均匀对称的）。 更要命的是， T5 Encoder 的输出要发给每个 Decoder Layer，网络结构不是线性而是有大量的分叉，前向反向之间包含了复杂的数据依赖关系， 会导致流水并行中，各个 Stage 之间会产生大量的、非对称的、间隔跨多个 Stage 的数据依赖，更加剧了流水并行的 load balance 问题。
- ![](https://picx.zhimg.com/80/v2-f3dc6a3aee932e4f869eb0d8e3280ff6_1440w.webp?source=2c26e567)

所以直接使用 Megatron 跑 T5 的 Pipeline Parallelism，会从 nsys prof 时间线上看到大量的缝隙，各个 Stage 之间在互相等待，无法真正流水并行起来。

如果不用  Pipeline Parallelism 来训练 T5，那么只能借助： DP、TP 和 ZeRO 来进行并行优化了， 这就约束了 T5 的所有 Layer 都必须放在每一个 GPU 上，这种方式在 13B 量级的模型上是 OK 的，但是再往上扩展到 100B、1T 量级就不 work 了。

同时由于 TP 只能开到 8 （跨机器也会慢几倍）， 在千卡 GPU 集群以上，大量的 DP 带来的通信变慢的影响也很严重（ZeRO-2/3 会大幅加剧这种通信开销）。 所以我们才说， 虽然 T5 的理论计算量相较于 GPT 没有增加很多，但是在千亿参数、千卡集群以上规模的时候，T5 的实际训练效率比 GPT 慢很多倍。即使到现在，也没有一个超过 11B 的 T5 模型发布， 而 11B 恰好是一个不借助 PP，仅通过  ZeRO + TP 就可以训练的模型大小，避免了 T5 的模型结构非对称性对于 PP 的灾难性影响。


## 基本原理

无论哪种机器学习框架，分布式训练的基本原理都是相同的。可以从**并行模式**、**架构模式**、**同步范式**、**物理架构**、**通信技术**等五个不同的角度来分类。

更多信息见优质paper，把 DP(Data Parallel)、MP(Model Parallel)、PP(Pipeline Parallel)各个方面讲的很透彻
- [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://zhuanlan.zhihu.com/p/106783111)

### 并行模式

分布式训练目的：将原本巨大的训练任务拆解成**多个子任务**，每个子任务在独立的机器上单独执行。

大规模深度学习任务的难点在于：
- 1) 训练**数据量巨大**：将数据拆解成多个小模型分布到不同的node上。→ **数据并行**
- 2) 训练模型的**参数巨大**：将数据集拆解分布到不同的node上。→ **模型并行**
  - NLP的预训练模型实在太大了

|并行模式||图解|
|---|---|---|
|数据并行|单机多卡用DP（PS），多级多可用DDP（Ring Allreduce）|![](https://pic3.zhimg.com/v2-f10be44bff31f5412b3398cc0cfbce96_b.jpg)|
|模型并行||![](https://pic2.zhimg.com/v2-37b26149c568865d5112fadb9b1ec9ad_b.jpg)|
|流水线并行|||


### 数据并行（DP&DDP）

![](https://pic3.zhimg.com/v2-f10be44bff31f5412b3398cc0cfbce96_b.jpg)

数据并行相对简单，N个node(worker)构成一个**分布式集群**，每个worker处理1/N的数据。
- 理论情况下能达到**线性**的加速效果。
- TF、torch、Horovod都可以在原生支持或者微小的改动实现数据并行模式。

DP(单机)+DDP(多机)

数据并行（DP&DDP）
- `DP`（Data Parallelism）：早期数据并行模式，一般采用**参数服务器**(Parameters Server)编程框架。实际中多用于**单机多卡**。 
- `DDP`（Distributed Data Parallelism）：分布式数据并行，采用`Ring AllReduce` 通讯方式，多用于**多机多卡**场景。


#### DP 单机数据并行

数据并行本质
- **单进程多线程**实现方式，只能实现**单机**训练, 不算严格意义上的分布式训练

多个GPU 情况下，将模型分发到每个GPU上去，每个GPU都保留完整模型参数。
- 每个GPU加载**全部模型**（Parameter、Grad、Optimizer、Activation、Temp buffer）
- 将每个batch样本平均分配到每个GPU上进行梯度计算
- 然后**汇总**每个GPU上的梯度
- 将汇总梯度重新分发到每个GPU上，每个GPU模型根据汇总的梯度进行模型参数更细。
- ![](https://pic2.zhimg.com/v2-0c13c485f5b43319c3bb4c65ae09d475_b.jpg)

K个GPU并数据并行训练过程如下：
- 任何一次训练迭代中，给定的随机的小批量样本都将被分成K个部分，并均匀地分配到GPU上；
- 每个GPU根据分配给它的小批量子集，计算模型参数的损失和梯度；
- 将个GPU中的**局部梯度**聚合，以获得当前小批量的随机梯度；
- 聚合梯度被重新分发到每个GPU中；
- 每个GPU使用这个小批量随机梯度，来更新所维护的完整的模型参数集。

数据并行是在每个worker上存储一个模型的备份，在各个worker 上处理不同的**数据子集**。然后需要**规约**(reduce)每个worker的结果，在各节点之间同步模型参数。
- 这一步会成为数据并行的瓶颈，因为如果worker很多的情况下，worker之间的数据传输会有很大的时间成本。

参数同步后，需要采用不同的方法进行参数更新：
- **参数平均法**：最简单的一种数据平均化
- **更新式方法**

若采用**参数平均法**，训练的过程如下所示：基于模型的配置随机初始化网络模型参数
- 将当前这组参数分发到各个工作节点
- 在每个工作节点，用数据集的一部分数据进行训练
- 将各个工作节点的参数的**均值**作为**全局参数值**
- 若还有训练数据没有参与训练，则继续从第二步开始

**更新式**方法与**参数平均化**类似，主要区别在于，在**参数**服务器和**工作**服务器之间传递参数时，更新式方法只传递**更新信息**(梯度和张量)。


问题：
- 负载不均衡，主GPU负载大
- PS 架构通信开销大

#### DDP 分布式数据并行 

DDP (Distribution Data Parallel)
- AllReduce 架构，在单机和多机上都可以使用。
- 负载分散在每个gpu节点上，通信成本是恒定的，与 GPU 数量无关。

### 模型并行（model parallesim）

当**模型参数过大**，单个 GPU无法容纳模型参数时，就需要模型并行, 将模型拆分到多个 GPU 训练。

模型并行相对复杂
- 原理：分布式系统中的不同worker负责网络模型的不同部分
- 例如，神经网络的不同层被分布到不同worker或者同一层的不同参数被分配到不同worker上。
- 对于TF这种框架，可以拆分计算图成多个最小依赖子图到不同的worker上。同时在多个子图之间通过通信算子来实现模型并行。

但是**模型并行**实现起来比较复杂。工业界还是以**数据并行**为主。

#### 层间 & 层内

`Model Parallel`主要分两种：**intra-layer**拆分 和 **inter-layer**拆分
- `inter-layer`拆分：对模型做网络上的拆分,将每一层或者**某几层**放在一个worker上单独训练。
  - 缺点：模型训练串行，整个模型的效率取决于最慢的那一层，存在资源浪费
- `intranet-layer`拆分：深度学习的网络结构基本都是一层层的。常规的卷积、池化、BN等等。如果对某一层进行了拆分，那么就是intra-layer拆分。对单层的拆分其实就是拆分这一层的matrix运算。
  - 参考论文：Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism

对比
- 层间并行: 流水线并行
- 层内并行: 张量并行

|概念|中文|图解|
|---|---|---|
|intra-layer and inter-layer|层间并行和层内并行|![](https://pic2.zhimg.com/80/v2-c24f5994e88c4361d578d5e0939be7b9_1440w.webp)|
|orthogonal and complimentary|正交和互补|![](https://pic2.zhimg.com/80/v2-708c01105de92567824bd9d3456b9459_1440w.webp)|

**模型并行**通常分为**张量并行**（纵向切分）以及**流水线并行**（横向切分）
- ![](https://pic2.zhimg.com/v2-37b26149c568865d5112fadb9b1ec9ad_b.jpg)
- **流水线并行**（Pipeline model parallesim）
  - 朴素拆分方式: 将模型各层分组后装载到各个GPU上去，GPU之间进行**串行**计算
    - 缺点: GPU 利用率太低，当一个GPU进行计算时，其他层的GPU都闲置。
  - 改进: 谷歌提出了GPipe `流水线并行`（Pipeline model parallesim ）, 引入micro-batches (MBS)的概念，会提升GPU利用率
  - 问题: 流水线最大的问题, 无法充分利用GPU资源，training过程中会出现非预期的Bubble
- **张量并行**（Tensor Model Parallelism）
  - 张量并行（TP）是模型并行一种形式，流水线并行按**网络层**切分，张量并行按**矩阵**切分。
  - 2019年，NVIDIA发布《Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM》论文，提出了张量并行方法
  - 核心思想: 每个GPU仅处理矩阵一部分，当算子需要整个矩阵的时候再进行矩阵聚合。无论是横向切分还是竖向切分，都可以将切分后的矩阵放到不同GPU上进行计算，最后将计算的结果再合并。


大模型主要结构都是Transformer模型，Transformer核心模块网路结构：**anttention层**+**残差连接**，MLP层+残差连接。
- MLP层: 数学表达如下：`Y = GeLU(XA)` ，`Z = Dropout(YB)`
- Attention层: 数学表达如下：`Y = Self-Attention(X)` ，`Z = Dropout(YB)`, 多头注意力每个头都是独立的，因此张量切分更方便

大模型训练时，ZeRO支持将模型显存内存占用划分到多张卡或者多个节点。



#### 示例

【2023-8-28】[模型并行最佳实践（PyTorch）](https://zhuanlan.zhihu.com/p/87596314)

两个GPU上运行此模型，只需将每个线性层放在不同的GPU上，然后移动输入（input）和中间输出（intermediate outputs）以匹配层设备（layer devices）。

```py
import torch
import torch.nn as nn
import torch.optim as optim

class ToyModel(nn.Module):
  """
    模型并行示例
  """

  def __init__(self):
    # 模型定义修改: 只需增加 to(device)
    super(ToyModel, self).__init__()
    self.net1 = torch.nn.Linear(10, 10).to('cuda:0')  # 将net1放置在第1个GPU上
    self.relu = torch.nn.ReLU()
    self.net2 = torch.nn.Linear(10, 5).to('cuda:1')   # 将net2放置在第2个GPU上

  def forward(self, x):
    x = self.relu(self.net1(x.to('cuda:0')))
    return self.net2(x.to('cuda:1'))
```

注意 ToyModel
- 除了5个用于将**线性层**（linear layers）和**张量**（tensors）放置在适当设备上的to(device)调用之外，以上内容与在单个GPU上实现该功能非常相似。那是模型中**唯一**更改地方（即to(device) ）。
- 在 backward()和 torch.optim 会**自动**关注梯度（gradients），模型如同一个GPU。
- 调用损失函数时，只需确保**标签**（label）与**输出**（output）在同一设备（on the same device）上。

```py
model = ToyModel()
loss_fn = nn.MSELoss()
optimizer = optim.SGD(model.paraeters(), lr=0.001)

optimizer.zero_grad()
outputs = model(torch.randn(20, 10))
labels = torch.randn(20, 5).to('cuda:1') # ToyMode 的 output 是在 'cuda:1' 上，此处的 label 也应该置于 'cuda:1' 上
loss_fn(outputs,labels).backward()
optimizer.step()
```

只需更改几行，就可以在多个GPU上运行现有的单GPU模块。

如何分解 torchvision.models.reset50() 为两个GPU。
- 从现有 ResNet模块继承，并在构建过程中将层拆分为两个GPU。
- 然后覆盖 forward方法来缝合两个子网，通过相应地移动中间输出。

```py
from torchvision.models.resnet import ResNet, Bottleneck

num_classes = 1000

class ModelParallelResNet50(ResNet):
    def __init__(self, *args, **kwargs):
        super(ModelParallelResNet50, self).__init__(Bottleneck, [3, 4, 6, 3], num_classes=num_classes, *args, **kwargs)

        self.seq1 = nn.Sequential(
            self.conv1,
            self.bn1,
            self.relu,
            self.maxpool,
            # 模型拆分
            self.layer1,
            self.layer2
        ).to('cuda:0')  # 放置在第1个GPU上

        self.seq2 = nn.Sequential(
            self.layer3,
            self.layer4,
            self.avgpool,
        ).to('cuda:1')  # 放置在第2个GPU上

        self.fc.to('cuda:1')

    def forward(self, x):
        x = self.seq2(self.seq1(x).to('cuda:1'))
        return self.fc(x.view(x.size(0), -1))
```

对于模型太大而无法放入单个GPU的情况，上述实现解决了该问题。但是，如果模型合适，model parallel 将比在单个GPU上运行要**慢**。
- 因为在<span style='color:red'>任何时间点，两个GPU中只有1个在工作</span>，而另一个在那儿什么也没做。
- 在 layer2 和 layer3之间，中间输出需要从 cuda:0 复制到 cuda:1，这使得性能进一步恶化。

```py
import torchvision.models as models

num_batches = 3
batch_size = 120
image_w = 128
image_h = 128

def train(model):
    model.train(True)
    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001)

    one_hot_indices = torch.LongTensor(batch_size) \
                           .random_(0, num_classes) \
                           .view(batch_size, 1)

    for _ in range(num_batches):
        # generate random inputs and labels
        inputs = torch.randn(batch_size, 3, image_w, image_h)
        labels = torch.zeros(batch_size, num_classes) \
                      .scatter_(1, one_hot_indices, 1)

        # run forward pass
        optimizer.zero_grad()
        outputs = model(inputs.to('cuda:0'))

        # run backward pass
        labels = labels.to(outputs.device)
        loss_fn(outputs, labels).backward()
        optimizer.step()
```

两个GPU中的一个会处于空闲状态。怎么优化？
- 将每个批次进一步划分为拆分`流水线`，当1个拆分到达第2子网时，可以将下一个拆分馈入第一子网。这样，两个连续的拆分可以在两个GPU上同时运行。

流水线输入（Pipelining Inputs）加速
- 将每批次 120-image 进一步划分为 20-image 。当PyTorch异步启动CUDA操作时，该实现无需生成多个线程即可实现并发。

```py
class PipelineParallelResNet50(ModelParallelResNet50):
    def __init__(self, split_size=20, *args, **kwargs):
        super(PipelineParallelResNet50, self).__init__(*args, **kwargs)
        self.split_size = split_size

    def forward(self, x):
        splits = iter(x.split(self.split_size, dim=0))
        s_next = next(splits)
        s_prev = self.seq1(s_next).to('cuda:1')
        ret = []

        for s_next in splits:
            # A. s_prev runs on cuda:1
            s_prev = self.seq2(s_prev)
            ret.append(self.fc(s_prev.view(s_prev.size(0), -1)))

            # B. s_next runs on cuda:0, which can run concurrently with A
            s_prev = self.seq1(s_next).to('cuda:1')

        s_prev = self.seq2(s_prev)
        ret.append(self.fc(s_prev.view(s_prev.size(0), -1)))

        return torch.cat(ret)


setup = "model = PipelineParallelResNet50()"
pp_run_times = timeit.repeat(
    stmt, setup, number=1, repeat=num_repeat, globals=globals())
pp_mean, pp_std = np.mean(pp_run_times), np.std(pp_run_times)

plot([mp_mean, rn_mean, pp_mean],
     [mp_std, rn_std, pp_std],
     ['Model Parallel', 'Single GPU', 'Pipelining Model Parallel'],
     'mp_vs_rn_vs_pp.png')
```

设备到设备的张量复制操作在源设备和目标设备上的当前流（current streams）上同步。如果创建多个流，则必须确保复制操作正确同步。在完成复制操作之前写入源张量或读取/写入目标张量可能导致不确定的行为。上面的实现仅在源设备和目标设备上都使用默认流，因此没有必要强制执行其他同步。


### 流水线并行

`数据并行`还是`模型并行`都会在相应机器之间全连接通信，当机器数量增大时，**通信开销和时延**会大到难以忍受

流水线(管道)并行既解决了**超大模型无法在单设备装下**的难题，又解决了**机器之间的通信开销**的问题
- 每个阶段（stage） 和下一个阶段之间仅有相邻的某一个 Tensor 数据需要传输
- 每台机器的数据传输量跟总的网络大小、机器总数、并行规模无关。

![](https://pic1.zhimg.com/80/v2-bdb9a12c01204d335187f6e3e3aad284_1440w.webp)

**流水线并行**（Pipeline model parallesim）
- 朴素拆分方式: 将模型**各层**分组后装载到各个GPU上，GPU之间进行**串行**计算
- ![](https://pic4.zhimg.com/80/v2-a2c0059f72e0e121520b6fce2027deaf_1440w.webp)
- 缺点: **GPU 利用率太低**，当1个GPU进行计算时，其他层GPU都闲置。

改进方法如下
- GPipe
- PipeDream


#### G-pipe

谷歌提出 `G-pipe` `流水线并行`（Pipeline model parallesim ）, 引入micro-batches (MBS)的概念，会提升GPU利用率
- `F-then-B` 调度方式: 原 mini-batch（数据并行切分后的batch）划分成多个 `micro-batch`（`mini-batch`再切分后的batch），每个 pipeline stage （流水线并行的计算单元）先整体进行**前向**计算，再进行**反向**计算。同一时刻分别计算模型的不同部分，F-then-B 可以显著提升设备资源利用率。
- F-then-B 模式由于缓存了多个 micro-batch 的中间变量和梯度，显存的实际利用率并不高。
- 解决: `1F1B` （在流水线并行中，pipeline stage 前向计算和反向计算交叉进行的方式）流水线并行方式。1F1B 模式下，前向计算和反向计算**交叉**进行，可以及时释放不必要的中间变量。
- ![](https://pic1.zhimg.com/80/v2-b678a253f70613169172fd892e0e4064_1440w.webp)


#### PipeDream

PipeDream 在单个 GPU 上短暂运行性能分析后，自动决定怎样分割这些 DNN 算子，如何平衡不同 stage 之间的计算负载，而同时尽可能减少目标平台上的通信量。

PipeDream将DNN 层划分为多个阶段 —— 每个阶段（stage）由模型中的一组连续层组成。
- PipeDream把模型的不同的阶段部署在不同的机器上，每个阶段可能有不同的replication。该阶段对本阶段中所有层执行向前和向后传递。
- PipeDream将包含输入层的阶段称为**输入**阶段，将包含输出层的阶段称为**输出**阶段。
- ![](https://pic3.zhimg.com/80/v2-26f04fc799e3220d6806cfbebe415712_1440w.webp)

#### virtual pipeline

virtual pipeline 是 Megatron-2 论文中最主要的一个创新点。
- 传统的 pipeline 并行通常会在一个 Device 上放置几个 block，为了扩展效率，在计算强度和通信强度中间取一个平衡。
- 但 virtual pipeline 在 device 数量不变的情况下，分出更多的 pipeline stage，以更多的通信量，换取空泡比率降低，减小了 step e2e 用时。
- ![](https://pic4.zhimg.com/80/v2-b5347bb2677de0ffd78e091a4e1e79bb_1440w.webp)

### 张量并行(Tensor Parallelism)


流水线并行主要集中在**多层**神经网络架构训练上，对于Transformer架构的模型（如BERT，GPT等），`MultiHead Attention Layer`和`MLP`的计算量翻了几倍，如果继续按管线切分模型, 可能单层参数都无法被显存装载，因此需要横着把同一层的模型切分开来，这便是**张量并行**
- 层间并行: 流水线并行
- 层内并行: 张量并行
- ![](https://pic3.zhimg.com/80/v2-293a367d9c5378f01fa64ad009dd9eb2_1440w.webp)

分布式张量计算正交且更通用，将张量操作划分到多个设备上，以加速计算或增加模型大小。
- 把 `Masked Multi Self Attention` 和 `Feed Forward` 都进行切分以并行化，利用Transformers网络的结构，通过添加一些同步原语来创建一个简单的模型并行实现。

**张量并行**（Tensor Model Parallelism）
- 张量并行（TP）是模型并行一种形式，流水线并行按**网络层**切分，张量并行按**矩阵**切分。
- 2019年，NVIDIA发布《Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM》论文，提出了张量并行方法
- 核心思想: 每个GPU仅处理矩阵一部分，当算子需要整个矩阵的时候再进行矩阵聚合。无论是横向切分还是竖向切分，都可以将切分后的矩阵放到不同GPU上进行计算，最后将计算的结果再合并。

张量并行最有名的是： `Megatron` 和 `Deepspeed`

### 混合并行

随着训练设备的增加，多个worker之间的通信成本增加，模型Reduce的成本也越来越大，数据并行的瓶颈也随之出现。故有学者提出**混合并行**(数据并行+模型并行)


### 架构模式

分布式训练上会频繁用到**规约**(AllReduce)操作。

all-reduce 操作有多种方式实现：
- **树状结构**：数据在进程间以树状结构进行归约，每个非叶子节点负责将其子节点的数据归约后再传递给其父节点。
- **环形结构**：进程之间形成一个环，数据在环中按顺序传递并归约。
- **直接归约**：所有进程直接将数据发送给一个中心节点，该节点完成归约后将结果发送回所有进程。

all-reduce 操作性能对分布式计算的效率至关重要，因此优化这一操作是分布式系统设计中的一个研究热点。使用最多的实现方式是百度提出的 `Ring AllReduce` 算法，该方法属于**环状结构**实现的一种。

主流的**分布式架构**主要分为`参数服务器`(ParameterServer) 和`基于规约`(Reduce)两种模式。早期还有基于`MPI`的方式，不过现在已经很少用了。

传统 parameter server: server和client方式
- client通过计算分配给自己的数据，产生梯度，传给server
- server 聚合，然后把参数再传给client

这个方式的弊端: server容易成为瓶颈
- server通信量太大。
- 一个client失败，会导致其他client等待。

Ring all reduce 一种分布式方式
- 各个节点分配通信量。
- 总的通信量和ps没啥变化，但是通信的压力平摊到各个GPU上了，GPU之间的通信可以并行进行。

假如，GPU数量是N，把模型参数分成N份，每个GPU要存放整个参数。每个GPU也要分配训练数据。
- 当一次迭代，N个GPU之间要经过一个scatter和gather操作，reduce-scatter是将不同gpu上对应的参数的gradient相加，一共需要通讯（N-1）次。
- All-gather 将合并完整的参数，传到其他gpu上，需要通讯（N-1）次。
- 一次all reduce，单卡通信量为2*sita。

#### PS：参数服务器

ParameterServer模式是一种基于reduce和broadcat算法的经典架构。
- 其中一个/一组机器作为PS架构的**中心节点**，用来**存储参数和梯度**。
- 在更新梯度的时候，先全局reduce接受其他worker节点的数据，经过本地计算后(比如参数平均法)，再broadcast回所有其他worker。
- 论文: [Parameter Server for Distributed Machine Learning](https://www.cs.cmu.edu/~muli/file/ps.pdf)
- [中文解读](https://www.zhihu.com/tardis/zm/art/82116922?source_id=1003)
- ![](https://pic3.zhimg.com/80/v2-85e54fee3bdad611072235264df95b66_1440w.webp)

PS架构的问题在于多个worker与ps通信，PS本身可能存在**瓶颈**。
- 随着worker数量的增加，整体通信量也线性增加，加速比也可能停滞在某个点位上。
- ![](https://pic3.zhimg.com/80/v2-eee6e2ad8aa00a8679298ff297508a16_1440w.jpg)

#### 基于规约 Reduce模式

基于规约的模式解决了上述的问题，最典型的是百度提出的 Ring-AllRuduce。
- 多个Worker节点连接成一个环，每个Worker依次把自己的梯度同步给下一个Worker，经过至多 2*(N-1) 轮同步，就可以完成所有Worker的梯度更新。
- 这种方式下所有节点的地位是平等的，因此不存在某个节点的**负载瓶颈**，随着Worker的增加，整体的通信量并不随着增加。加速比几乎可以跟机器数量成线性关系且不存在明显瓶颈。
- ![](https://pic1.zhimg.com/80/v2-5c777ca6d8ce4972d51f6ce73f3a044c_1440w.jpg)

目前，越来越多的分布式训练采用**Reduce**这种模式。Horovod中主要就是用的这种分布式架构。
- 更多资料参考: [兰瑞Frank：腾讯机智团队分享--AllReduce算法的前世今生](https://zhuanlan.zhihu.com/p/79030485)

### 同步范式

实际训练过程中可能遇到各种问题，比如：部分节点资源受限、卡顿、网络延时等等

因此梯度同步时就存在“**木桶**“效应，即集群中的某些worker比其他worker更慢，导致整个训练pipeline需要等待慢的worker，整个集群的训练速度受限于最慢机器的速度。

因此梯度同步有“**同步**”(sync)、“**异步**”(Async)和**混合**三种范式。
- **同步**范式：只有所有worker完成当前的计算任务，整个集群才会开始下一次迭代。
  - TF中同步范式使用SyncReplicasOptimizer优化器
- **异步**模式刚好相反，每个worker只关心知己的进程，完成计算后就尝试更新，能与其他多个worker同步梯度完成取决于各worker当前时刻的状态。其过程不可控，有可能出现模型正确性问题。(可在训练时logging对比)
- **混合**范式结合以上两种情况，各个worker都会等待其他worker的完成，但不是永久等待，有timeout的机制。如果超时了，则此情况下相当于异步机制。并且没来得及完成计算的worker，其梯度则被标记为“stale”而抛弃或另做处理。

**梯度累加**

Gradient Accumulation 把一个大 Batch 拆分成多个 micro-batch， 每个 micro-batch 前后向计算后的梯度累加，在最后一个micro-batch累加结束后，统一更新模型。

`micro-batch` 跟`数据并行`高度相似性：
- 数据并行是空间上，数据被拆分成多个 tensor，同时喂给多个设备并行计算，然后将梯度累加在一起更新；
- 而 micro-batch 是**时间**上的数据并行，数据被拆分成多个 tensor， 按照时序依次进入同一个设备串行计算，然后将梯度累加在一起更新。当总的 batch size 一致，且数据并行的并行度和 micro-batch 的累加次数相等时，数据并行和 Gradient Accumulation 在数学上完全等价。

Gradient Accumulation 通过多个 micro-batch的梯度累加, 使下一个 micro-batch 的前向计算不需要依赖上一个 micro-batch 的反向计算，因此可以畅通无阻的进行下去（当然在一个大 batch 的最后一次 micro-batch 还是会触发这个依赖）。

Gradient Accumulation 解决了很多问题：
- 单卡下，Gradient Accumulation 将一个大 batch size 拆分成等价的多个小 micro-batch ，从而达到节省显存的目的。
- 数据并行下，Gradient Accumulation 解决了反向梯度同步开销占比过大的问题（随着机器数和设备数的增加，梯度的 AllReduce 同步开销也加大），因为梯度同步变成了一个稀疏操作，因此可以提升数据并行的加速比。
- 流水并行下， Gradient Accumulation 使得不同 stage 之间可以并行执行不同的 micro-batch， 从而让各个阶段的计算不阻塞，达到流水的目的。如果每个 micro-batch 前向计算的中间结果（activation）被后向计算所消费，则需要在显存中缓存 8多份（梯度累加的次数）完整的前向 activation。这时就不得不用另一项重要的技术：激活检查点（activation checkpointing）。



### 物理架构

物理架构主要是 **GPU架构**，即：单机单卡、单机多卡、多机单卡、多机多卡（最典型）
- 单机单卡：常规操作
- 单机**多卡**：利用一台GPU上的多块GPU进行分布式训练。数据并行和模型并行皆可。整个训练过程一般只有一个进程，多GPU之间的通信通过多线程的方式，模型参数和梯度在进程内是共享的(基于NCCL的可能不大一样)。这种情况下基于Reduce的架构比PS架构更合适一些，因为不需要一个显式的PS，通过进程内的Reduce即可完成梯度同步。
- **多机**单卡：操作上与多机多卡基本一致
- 多机**多卡**：多机多卡是最典型的分布式架构，所以它需要较好的进程间的通讯机制(多worker之间的通信)。


内容：
- 分布式训练的基本原理
- TensorFlow的分布式训练
- PyTorch的分布式训练框架
- Horovod分布式训练

## 分布式实现


超大规模语言模型主要有两条技术路线：
- (1) `TPU` + `XLA` + `TensorFlow`/`JAX` : Google主导，由于TPU和自家云平台GCP深度绑定
- (2) `GPU` + `PyTorch` + `Megatron-LM` + `DeepSpeed`: NVIDIA、Meta、MS大厂加持，社区氛围活跃

(1) 对于非Googler 只可远观而不可把玩，(2) 更受到群众欢迎。

### TF分布式训练方法

- 黄文坚的[Tensorflow分布式实战](https://blog.csdn.net/CodeMaster_/article/details/76223835)

TensorFlow主要的分布式训练的方法有三种：
1. Customer Train Loop：最原始，由框架工程师自己开发
1. Estimator + Strategy：高级API，不用关心底层硬件
1. Keras + Strategy：最新出的keras的高级API

> - 实际的开发工作中，分布式的工作最好是交给框架，而工程师本身只需要关注任务模型的pipeline就行了。
> - 最经典的是Spark框架，工程师只需要关注数据处理的workflow，分布式的大部分工作都交给框架。深度学习的开发同样如此。

各种方式评价
- 第一种方式太过原生，整个分布式的训练过程完全交给工程师来处理，代码模块比较复杂，这里不做赘述。
- 第二种方式，Estimator是TF的一个高级API，在分布式场景下，其最大的特点是**单机和分布式代码一致**，且不需要考虑底层的硬件设施。Strategy是tensorflow根据分布式训练的复杂性，抽象出的多种分布式训练策略。TF1.x和TF2.x接口变化较大，不同版本名字可能不一样，以实际使用版本为准。用的比较多的是：
  - **MirroredStrategy**：适用于单机多卡、数据并行、同步更新的分布式训练，采用Reduce的更新范式，worker之间采用NCCL进行通信。
  - **MultiWorkerMirrored**Strategy：与上面的类似，不同的是这种策略支持多机多卡、数据并行、同步更新的分布式策略、Reduce范式。在TF 1.15版本里，这个策略叫CollectiveAllReduceStrategy。
  - **ParameterServer**Strategy：经典的PS架构，多机多卡、数据并行、同步/异步更新
  - 使用Estimator+Strategy 实现分布式训练，参考[代码](https://github.com/kubeflow/tf-operator/blob/master/examples/v1/distribution_strategy/estimator-API/keras_model_to_estimator.py)
- 第三种方式 Keras + Strategy 是Tensorflow最新官方推荐的方案。主要是利用keras的高级API，配合Strategy实现多模式的分布式训练。
  - [代码](https://github.com/kubeflow/tf-operator/blob/master/examples/v1/distribution_strategy/keras-API/multi_worker_strategy-with-keras.py)

后两种方法都需要传入TF_CONFIG参数，没有就是单机的训练方式。Strategy会自动读取环境变量并应用相关信息。

TF_CONFIG的配置如下
- ![](https://pic2.zhimg.com/80/v2-dc8c2f647b9e359661e2a6f288ac1525_1440w.jpg)

### 单机单卡

单机单卡是最普通的情况，当然也是最简单的。

使用步骤
- 检查可用GPU数量
- 获取一个GPU实例
- 迁移：将 数据/模型 推送到GPU上

#### TF

示例代码如下：

```python
#coding=utf-8
#单机单卡，对于单机单卡，可以把参数和计算都定义再gpu上，不过如果参数模型比较大，显存不足等情况，就得放在cpu上
import  tensorflow as tf
with tf.device('/cpu:0'):#也可以放在gpu上
    w=tf.get_variable('w',(2,2),tf.float32,initializer=tf.constant_initializer(2))
    b=tf.get_variable('b',(2,2),tf.float32,initializer=tf.constant_initializer(5))
with tf.device('/gpu:0'):
    addwb=w+b
    mutwb=w*b
init=tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(init)
    np1,np2=sess.run([addwb,mutwb])
    print np1,np2
```

#### PyTorch

pytorch实现
- 封装程度非常高，只需保证即将被推到 GPU 的数据是`张量`（Tensor）或者`模型`（Module），就可以用 `to()` 函数快速进行实现。

```py
import torch
from torch import nn

data = torch.ones((3, 3)) # 定义数据（张量）
print(data.device)
net = nn.Sequential(nn.Linear(3, 3)) # 定义模型

print(torch.cuda.is_available())     # 判断当前的机器是否有可用的 GPU
print(torch.cuda.device_count())     # 目前可用的 GPU 的数量。
# 使用第一块GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # cuda: 0 表示使用的是第一块 GPU。当然可以不用声明“:0”，默认就从第一块开始
print(device) # cpu 或 0
# 数据迁移：将data推到(迁移)gpu上
data_gpu = data.to(device)
print(data_gpu.device)
# 模型迁移：model推到gpu
net.to(device)
```


### 单机多卡

#### TF

- 单机多卡，只要用device直接指定设备，就可以进行训练，SGD采用各个卡的平均值
- 问题：除了取均值，还有别的方式吗？

```python
#coding=utf-8
#单机多卡：一般采用共享操作定义在cpu上，然后并行操作定义在各自的gpu上，比如对于深度学习来说，我们一般把参数定义、参数梯度更新统一放在cpu上，各个gpu通过各自计算各自batch数据的梯度值，然后统一传到cpu上，由cpu计算求取平均值，cpu更新参数。具体的深度学习多卡训练代码，请参考：https://github.com/tensorflow/models/blob/master/inception/inception/inception_train.py
import  tensorflow as tf
  
with tf.device('/cpu:0'):
    w=tf.get_variable('w',(2,2),tf.float32,initializer=tf.constant_initializer(2))
    b=tf.get_variable('b',(2,2),tf.float32,initializer=tf.constant_initializer(5))
with tf.device('/gpu:0'):
    addwb=w+b
with tf.device('/gpu:1'):
    mutwb=w*b
  
ini=tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(ini)
    while 1:
        print sess.run([addwb,mutwb])
```
- 多个 GPU 上运行 TensorFlow，则可以采用多塔式方式构建模型，其中每个塔都会分配给不同 GPU。例如：

```python
# Creates a graph.
c = []
for d in ['/device:GPU:2', '/device:GPU:3']:
  with tf.device(d):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3])
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2])
    c.append(tf.matmul(a, b))
with tf.device('/cpu:0'):
  sum = tf.add_n(c)
# Creates a session with log_device_placement set to True.
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
# Runs the op.
print(sess.run(sum))
```

- 【2020-5-20】每个gpu的梯度要累加起来，单独计算

```python
        # train op def
        tower_grads = []
        for i in xrange(FLAGS.num_gpus):
            with tf.device('/gpu:{}'.format(i)):
                with tf.name_scope('tower_{}'.format(i)):
                    next_batch = dhs.get_next_batch()
                    cnn.inference(
                        next_batch[0], next_batch[1], next_batch[2],
                        dropout_keep_prob=FLAGS.dropout_keep_prob,
                        input_dropout_keep_prob=FLAGS.input_dropout_keep_prob,
                        phase_train=True)
                    grads = optimizer.compute_gradients(cnn.loss)
                    tower_grads.append(grads)
        grads = average_gradients(tower_grads)
        train_op = optimizer.apply_gradients(grads, global_step=global_step)

def average_gradients(tower_grads):
    """
    Calculate the average gradient for each shared variable across all towers.
    Note that this function provides a synchronization point across all towers.
    NOTE: This function is copied from cifar codes in tensorflow tutorial with minor
    modification.
    Args:
        tower_grads: List of lists of (gradient, variable) tuples. The outer list
            is over individual gradients. The inner list is over the gradient
            calculation for each tower.
    Returns:
       List of pairs of (gradient, variable) where the gradient has been averaged
       across all towers.
    """
    average_grads = []
    for grad_and_vars in zip(*tower_grads):
        # Note that each grad_and_vars looks like the following:
        #   ((grad0_gpu0, var0_gpu0), ... , (grad0_gpuN, var0_gpuN))
        grads = []
        for g, _ in grad_and_vars:
            # Add 0 dimension to the gradients to represent the tower.
            # NOTE: if batch norm applied, the grad of conv-maxpool-n/b will be
            #       None
            if g is None:
                continue
            expanded_g = tf.expand_dims(g, 0)

            # Append on a 'tower' dimension which we will average over below.
            grads.append(expanded_g)

        # Average over the 'tower' dimension.
        if grads:
            grad = tf.concat(axis=0, values=grads)
            grad = tf.reduce_mean(grad, 0)
        else:
            grad = None

        # Keep in mind that the Variables are redundant because they are shared
        # across towers. So .. we will just return the first tower's pointer to
        # the Variable.
        v = grad_and_vars[0][1]
        grad_and_var = (grad, v)
        average_grads.append(grad_and_var)
    return average_grads
```

- 参考官网：[TensorFlow with multiple GPUs](https://jhui.github.io/2017/03/07/TensorFlow-GPU/)

#### PyTorch

PyTorch 多种解决方案，最简单常用：nn.DataParallel()
- module ：定义的模型
- device_ids 即为训练模型时用到的 GPU 设备号，
- output_device 表示输出结果的 device，默认为 0 也就是第一块卡。

工作过程
- ![](https://pic3.zhimg.com/80/v2-8cba3ef61df28c56c250afef9ca1f2c2_1440w.webp)
- 在每个迭代训练的Forward过程中：nn.DataParallel都自动将输入按照GUP数量进行split；然后复制模型参数到各个GPU上；分别进行正向计算后将得到网络输出output_x；最后将结果concat拼接到一起送往0号卡中。
- 在Backward过程中：先由0号卡计算loss函数，通过loss.backward()得到损失函数相于各个gpu输出结果的梯度grad_l1 ... gradln；接下来0号卡将所有的grad_i送回对应的GPU_i中；然后GPU们分别进行backward得到各个GPU上面的模型参数梯度值gradm1 ... gradmn；最后所有参数的梯度汇总到GPU0卡进行update。


多卡训练时，output_device 的卡所占的显存明显大一些。
- 因为使用 DataParallel 时，数据并行，每张卡获得的数据都一样多，但是所有卡的 loss 都会在第 output_device 块 GPU 进行计算，这导致了 output_device 卡的负载进一步增加。
- ![](https://pic3.zhimg.com/80/v2-51e78bd8c116d68b0901f4257523feae_1440w.webp)

只需要一个 DataParallel 函数就可以将模型和数据分发到多个 GPU 上。
- 但是还是需要了解这内部的运行逻辑, 遇到了诸如时间计算、资源预估、优化调试问题的时候，可以更好地运用 GPU

```py
import os
from torch import nn
import torch

class ASimpleNet(nn.Module):
    def __init__(self, layers=3):
        super(ASimpleNet, self).__init__()
        self.linears = nn.ModuleList([nn.Linear(3, 3, bias=False) for i in range(layers)])   # 设备有几个，就创建几个模型分支，
    def forward(self, x):     # 模型前馈实际处理过程
        print("forward batchsize is: {}".format(x.size()[0]))
        x = self.linears(x)
        x = torch.relu(x)
        return x

device=os.environ['CUDA_VISIBLE_DEVICES']  
# os.environ['CUDA_VISIBLE_DEVICES']="0,2"  指定具体的设备
# print("CUDA_VISIBLE_DEVICES :{}".format(os.environ["CUDA_VISIBLE_DEVICES"]))

batch_size = 16
inputs = torch.randn(batch_size, 3)            # 创建16个数据
labels = torch.randn(batch_size, 3)            # 创建16个数据标签
inputs, labels = inputs.to(device), labels.to(device)      # 数据迁移到设备上，返回数据总接口（应该是一个列表/字典，数据片段-GPU对应关系）
net = ASimpleNet()                             # 模型实例化
net = nn.DataParallel(net)                     # 模型分布结构化
net.to(device)                                 # 模型迁移到设备上，返回一个模型总接口（应该是一个列表/字典，子模型-GPU对应关系）
for epoch in range(1):       # 训练次数自行决定
    outputs = net(inputs)    #  数据统一入口；数据怎么分配，模型参数怎么同步，内部机制自行来处理
# 输出：
# CUDA_VISIBLE_DEVICES : 3, 2, 1, 0
# forward batchsize is: 4
# forward batchsize is: 4
# forward batchsize is: 4
# forward batchsize is: 4
```

注意：有几个GPU，建几个分支（同结构模型），这样就可以分散到各个GPU上。

CUDA_VISIBLE_DEVICES 得知了当前程序可见的 GPU 数量为 4，而创建的 batch size 为 16，输出每个 GPU 上模型 forward 函数内部的 print 内容，验证了每个 GPU 获得的数据量都是 4 个。
- DataParallel 会自动将数据切分、加载到相应 GPU，将模型复制到相应 GPU，进行正向传播计算梯度并汇总。

提示
- DataParallel的整个并行训练过程利用python多线程实现

由以上工作过程分析可知，nn.DataParallel 无法避免的问题：
- **负载不均衡**问题。gpu_0所承担的任务明显要重于其他gpu
- **速度**问题。每个iteration都需要复制模型且均从GPU0卡向其他GPU复制，通讯任务重且效率低；python多线程GIL锁导致的线程颠簸(thrashing)问题。
- 只能**单机**运行。由于单进程的约束导致。
- 只能切分batch到多GPU，而无法让一个model分布在多个GPU上。当一个模型过大，设置batchsize=1时其显存占用仍然大于单张显卡显存，此时就无法使用DataParallel类进行训练。

因此官方推荐使用 torch.nn.DistributedDataParallel 替代 nn.DataParallel

### 多机多卡

一、基本概念
- Cluster、Job、task概念：三者可以简单的看成是层次关系
- task相当于每台机器上的一个进程，多个task组成job；
- job又有两种：ps参数服务、worker计算服务，组成cluster。

二、同步SGD与异步SGD
- 1、**同步更新**：各个用于并行计算的电脑，计算完各自的batch 后，求取梯度值，把梯度值统一送到ps服务机器中，由ps服务机器求取梯度平均值，更新ps服务器上的参数。
  - 如下图所示，可以看成有四台电脑，第一台电脑用于存储参数、共享参数、共享计算，可以简单的理解成内存、计算共享专用的区域，也就是ps job；另外三台电脑用于并行计算的，也就是worker task。
  - 这种计算方法存在的缺陷是：每一轮的梯度更新，都要等到A、B、C三台电脑都计算完毕后，才能更新参数，也就是迭代更新速度取决与A、B、C三台中，最慢的那一台电脑，所以采用同步更新的方法，建议A、B、C三台的计算能力都不想。
- 2、**异步更新**：ps服务器收到只要收到一台机器的梯度值，就直接进行参数更新，无需等待其它机器。这种迭代方法比较不稳定，收敛曲线震动比较厉害，因为当A机器计算完更新了ps中的参数，可能B机器还是在用上一次迭代的旧版参数值。

#### 多机多卡讲解

【2024-4-18】[大模型多机多卡训练经验总结](https://zhuanlan.zhihu.com/p/693040848)

LLM多机多卡训练教程好少，有些还拿 `torch.distributed.launch` 来做，殊不知早就改用 `torchrun` 了。

环境准备: 以2台机器为例
- 首先, 2台机器要能**免密登录**，编辑/etc/hosts文件，加入node信息：

```sh
# vi /etc/hosts
ip1 node01
ip2 node02
```

然后, 两个node分别执行以下操作, 生成私钥和公钥：

```sh
ssh-keygen -t rsa
```

然后, 全部回车，采用默认值。再互相拷贝秘钥：

```sh
ssh-copy-id root@ip1
ssh-copy-id root@ip2
```

分别在2台机器上试试互相ssh，如果无密码输入要求直接登录到另一台服务器则说明配置成功。

2台机器环境必须保持一致，包括python版本，训练所需依赖包等。

还需确保安装了pdsh：

```sh
apt-get install pdsh
```

多机训练

使用 torchrun，毕竟单张GPU有80G显存，7B模型单卡完全放得下。
- 假设node01为master，node02需要有相同的模型权重和代码，可以直接在master用scp拷贝过去。

准备工作完成后, 可以启动训练命令
- 首先在node01(master)执行如下命令（非完整，仅供参考，使用deepspeed ZeRO-2）：

```sh
torchrun --nproc_per_node 8 --nnodes 2 --master_addr ${MASTER_ADDR} --master_port 14545 --node_rank 0 train.py \
  --deepspeed ${deepspeed_config_file} \
  ...
```
 
参数
- nproc_per_node表示每个节点的进程数，可以理解为每个节点所需GPU数
- nnode表示节点数，2台机器就是2个节点数
- master_add为master的ip
- node_rank表示当前启动的是第几个节点

在node02执行同样命令，但需将node_rank指定为1，不出意外的话可以成功跑通，即便报错可能也是依赖包版本两台机器不一致导致。很快就会在控制台看到transformers打印的日志，但发现save_total_limit只在master上管用。

#### TF

代码编写
- 1、定义集群
- 比如假设上面的图所示，我们有四台电脑，名字假设为：A、B、C、D，那么集群可以定义如下

```python
#coding=utf-8
#多台机器，每台机器有一个显卡、或者多个显卡，这种训练叫做分布式训练
import  tensorflow as tf
#现在假设我们有A、B、C、D四台机器，首先需要在各台机器上写一份代码，并跑起来，各机器上的代码内容大部分相同
# ，除了开始定义的时候，需要各自指定该台机器的task之外。以机器A为例子，A机器上的代码如下：
cluster=tf.train.ClusterSpec({
    "worker": [
        "A_IP:2222",#格式 IP地址：端口号，第一台机器A的IP地址 ,在代码中需要用这台机器计算的时候，就要定义：/job:worker/task:0
        "B_IP:1234"#第二台机器的IP地址 /job:worker/task:1
        "C_IP:2222"#第三台机器的IP地址 /job:worker/task:2
    ],
    "ps": [
        "D_IP:2222",#第四台机器的IP地址 对应到代码块：/job:ps/task:0
    ]})
```

然后需要写四分代码，这四分代码文件大部分相同，但是有几行代码是各不相同的。

- 2、在各台机器上，定义server
    - 比如A机器上的代码server要定义如下：
```python
server=tf.train.Server(cluster,job_name='worker',task_index=0)#找到‘worker’名字下的，task0，也就是机器A
```

- 3、在代码中，指定device
```python
with tf.device('/job:ps/task:0'):#参数定义在机器D上
    w=tf.get_variable('w',(2,2),tf.float32,initializer=tf.constant_initializer(2))
    b=tf.get_variable('b',(2,2),tf.float32,initializer=tf.constant_initializer(5))
with tf.device('/job:worker/task:0/cpu:0'):#在机器A cpu上运行
    addwb=w+b
with tf.device('/job:worker/task:1/cpu:0'):#在机器B cpu上运行
    mutwb=w*b
with tf.device('/job:worker/task:2/cpu:0'):#在机器C cpu上运行
    divwb=w/b
```

在深度学习训练中，一般图的计算，对于每个worker task来说，都是相同的，所以我们会把所有图计算、变量定义等代码，都写到下面这个语句下：
```python
with tf.device(tf.train.replica_device_setter(worker_device='/job:worker/task:indexi',cluster=cluster))
```

函数replica_deviec_setter会自动把变量参数定义部分定义到ps服务中(如果ps有多个任务，那么自动分配)。下面举个例子，假设现在有两台机器A、B，A用于计算服务，B用于参数服务，那么代码如下：

```python
#coding=utf-8
#上面是因为worker计算内容各不相同，不过再深度学习中，一般每个worker的计算内容是一样的，
# 以为都是计算神经网络的每个batch 前向传导，所以一般代码是重用的
import  tensorflow as tf
#现在假设我们有A、B台机器，首先需要在各台机器上写一份代码，并跑起来，各机器上的代码内容大部分相同
# ，除了开始定义的时候，需要各自指定该台机器的task之外。以机器A为例子，A机器上的代码如下：
cluster=tf.train.ClusterSpec({
    "worker": [
        "192.168.11.105:1234",#格式 IP地址：端口号，第一台机器A的IP地址 ,在代码中需要用这台机器计算的时候，就要定义：/job:worker/task:0
    ],
    "ps": [
        "192.168.11.130:2223"#第四台机器的IP地址 对应到代码块：/job:ps/task:0
    ]})
  
#不同的机器，下面这一行代码各不相同，server可以根据job_name、task_index两个参数，查找到集群cluster中对应的机器
  
isps=False
if isps:
    server=tf.train.Server(cluster,job_name='ps',task_index=0)#找到‘worker’名字下的，task0，也就是机器A
    server.join()
else:
    server=tf.train.Server(cluster,job_name='worker',task_index=0)#找到‘worker’名字下的，task0，也就是机器A
    with tf.device(tf.train.replica_device_setter(worker_device='/job:worker/task:0',cluster=cluster)):
        w=tf.get_variable('w',(2,2),tf.float32,initializer=tf.constant_initializer(2))
        b=tf.get_variable('b',(2,2),tf.float32,initializer=tf.constant_initializer(5))
        addwb=w+b
        mutwb=w*b
        divwb=w/b

saver = tf.train.Saver()
summary_op = tf.merge_all_summaries()
init_op = tf.initialize_all_variables()
sv = tf.train.Supervisor(init_op=init_op, summary_op=summary_op, saver=saver)
with sv.managed_session(server.target) as sess:
    while 1:
        print sess.run([addwb,mutwb,divwb])
```

把该代码在机器A上运行，你会发现，程序会进入等候状态，等候用于ps参数服务的机器启动，才会运行。

因此接着我们在机器B上运行如下代码：

```python
#coding=utf-8
#上面是因为worker计算内容各不相同，不过再深度学习中，一般每个worker的计算内容是一样的，
# 以为都是计算神经网络的每个batch 前向传导，所以一般代码是重用的
#coding=utf-8
#多台机器，每台机器有一个显卡、或者多个显卡，这种训练叫做分布式训练
import  tensorflow as tf
#现在假设我们有A、B、C、D四台机器，首先需要在各台机器上写一份代码，并跑起来，各机器上的代码内容大部分相同
# ，除了开始定义的时候，需要各自指定该台机器的task之外。以机器A为例子，A机器上的代码如下：
cluster=tf.train.ClusterSpec({
    "worker": [
        "192.168.11.105:1234",#格式 IP地址：端口号，第一台机器A的IP地址 ,在代码中需要用这台机器计算的时候，就要定义：/job:worker/task:0
    ],
    "ps": [
        "192.168.11.130:2223"#第四台机器的IP地址 对应到代码块：/job:ps/task:0
    ]})
  
#不同的机器，下面这一行代码各不相同，server可以根据job_name、task_index两个参数，查找到集群cluster中对应的机器
  
isps=True
if isps:
    server=tf.train.Server(cluster,job_name='ps',task_index=0)#找到‘worker’名字下的，task0，也就是机器A
    server.join()
else:
    server=tf.train.Server(cluster,job_name='worker',task_index=0)#找到‘worker’名字下的，task0，也就是机器A
    with tf.device(tf.train.replica_device_setter(worker_device='/job:worker/task:0',cluster=cluster)):
        w=tf.get_variable('w',(2,2),tf.float32,initializer=tf.constant_initializer(2))
        b=tf.get_variable('b',(2,2),tf.float32,initializer=tf.constant_initializer(5))
        addwb=w+b
        mutwb=w*b
        divwb=w/b
  
saver = tf.train.Saver()
summary_op = tf.merge_all_summaries()
init_op = tf.initialize_all_variables()
sv = tf.train.Supervisor(init_op=init_op, summary_op=summary_op, saver=saver)
with sv.managed_session(server.target) as sess:
    while 1:
        print sess.run([addwb,mutwb,divwb])
```

- [Tensorflow官方指南](https://www.tensorflow.org/versions/master/how_tos/distributed/index.html)

分布式训练需要熟悉的函数：
- tf.train.Server
- tf.train.Supervisor
- tf.train.SessionManager
- tf.train.ClusterSpec
- tf.train.replica_device_setter
- tf.train.MonitoredTrainingSession
- tf.train.MonitoredSession
- tf.train.SingularMonitoredSession
- tf.train.Scaffold
- tf.train.SessionCreator
- tf.train.ChiefSessionCreator
- tf.train.WorkerSessionCreator

#### PyTorch

DP
- DP就是 DataParallel。DP 是**单进程**控制多 GPU。
  - DP 将输入的一个 batch 数据分成了 n 份（n 为实际使用的 GPU 数量），分别送到对应的 GPU 进行计算。
  - 在网络前向传播时，模型会从主 GPU 复制到其它 GPU 上；
  - 在反向传播时，每个 GPU 上的梯度汇总到主 GPU 上，求得梯度均值更新模型参数后，再复制到其它 GPU，以此来实现并行。
  - 由于主 GPU 要进行梯度汇总和模型更新，并将计算任务下发给其它 GPU，所以主 GPU 的负载与使用率会比其它 GPU 高，这就导致了 GPU 负载不均衡的现象。

DDP
- DDP 是 DistributedDataParallel。DDP **多进程**控制多 GPU。
  - 系统会为每个 GPU 创建一个进程，不再有主 GPU，每个 GPU 执行相同的任务。
  - DDP 使用分布式数据采样器（DistributedSampler）加载数据，确保数据在各个进程之间没有重叠。
  - 在反向传播时，各 GPU 梯度计算完成后，各进程以广播的方式将梯度进行汇总平均，然后每个进程在各自的 GPU 上进行梯度更新，从而确保每个 GPU 上的模型参数始终保持一致。由于无需在不同 GPU 之间复制模型，DDP 的传输数据量更少，因此速度更快。

DDP 既可用于**单机多卡**也可用于**多机多卡**，它能解决 DataParallel 速度慢、GPU 负载不均衡等问题。因此，官方更推荐使用 DistributedDataParallel 来进行分布式训练

基本概念
- group：进程组。默认情况下，只有一个组，即一个 world。（DDP 多进程控制多 GPU）
- world_size ：表示全局进程个数。
- rank：表示进程序号，用于进程间通讯，表示进程优先级。rank=0 的主机为主节点。

训练基本流程
- ![](https://pic3.zhimg.com/80/v2-0c8048a903e59659880350df0ea98e1a_1440w.webp)
- （1）初始化进程组：用 init_process_group 函数
  - backend：是通信所用的后端，可以是“nccl”或“gloo”。一般来说，nccl 用于 GPU 分布式训练，gloo 用于 CPU 进行分布式训练。
  - init_method：字符串类型，是一个 url，进程初始化方式，默认是 “env://”，表示从环境变量初始化，还可以使用 TCP 的方式或共享文件系统 。
  - world_size：执行训练的所有的进程数，表示一共有多少个节点（机器）。
  - rank：进程的编号，也是其优先级，表示当前节点（机器）的编号。group_name：进程组的名字。
- （2）模型并行化：用 DistributedDataParallel，将模型分发至多 GPU 上
  - DistributedDataParallel 的参数与 DataParallel 基本相同
- （3）创建分布式数据采样器

DP 是直接将一个 batch 的数据划分到不同的卡，但是多机多卡间频繁数据传输会严重影响效率，这时就要用到**分布式数据采样器** DistributedSampler，它会为每个子进程划分出一部分数据集，从而使 DataLoader 只会加载特定的一个子数据集，以避免不同进程之间有数据重复。
- 先将 train_dataset 送到了 DistributedSampler 中，并创建了一个分布式数据采样器 train_sampler。
- 再构造 DataLoader ，, 参数中传入了一个 sampler=train_sampler，即可让不同的进程节点加载属于自己的那份子数据集。也就是说，使用 DDP 时，不再是从主 GPU 分发数据到其他 GPU 上，而是各 GPU 从自己的硬盘上读取属于自己的那份数据。

具体逻辑：
- **加载模型**阶段。每个GPU都拥有模型的一个副本，所以不需要拷贝模型。rank为0的进程会将网络初始化参数broadcast到其它每个进程中，确保每个进程中的模型都拥有一样的初始化值。
- **加载数据**阶段。DDP 不需要广播数据，而是使用多进程并行加载数据。在 host 之上，每个worker进程都会把自己负责的数据从硬盘加载到 page-locked memory。DistributedSampler 保证每个进程加载到的数据是彼此不重叠的。
- **前向传播**阶段。在每个GPU之上运行前向传播，计算输出。每个GPU都执行同样的训练，所以不需要有主 GPU。
- **计算损失**。在每个GPU之上计算损失。
- **反向传播**阶段。运行后向传播来计算梯度，在计算梯度同时也对梯度执行all-reduce操作。
- **更新模型参数**阶段。因为每个GPU都从完全相同的模型开始训练，并且梯度被all-reduced，因此每个GPU在反向传播结束时最终得到平均梯度的相同副本，所有GPU上的权重更新都相同，也就不需要模型同步了。注意，在每次迭代中，模型中的Buffers 需要从rank为0的进程广播到进程组的其它进程上。

代码略，见[原文](https://zhuanlan.zhihu.com/p/634846886)

注意
- 使用 DDP 意味着使用**多进程**，如果直接保存模型，每个进程都会执行一次保存操作，此时只使用主进程中的一个 GPU 来保存即可。

## Pytorch 分布式训练


### 分布式基础


#### 分布式模式

PyTorch 原生支持的并行模式：
- **完全**分片数据并行（full sharded data parallel，`FSDP`）
- **混合**分片数据并行（hybrid sharding data parallel，`HSDP`）
- 张量并行（tensor parallel，`TP`）
- 流水线并行（pipeline parallel，`PP`）
- 序列并行（sequence parallel，`SP`）
- 上下文并行（context parallel，`CP`）

【2023-3-2】[PyTorch 分布式训练实现(DP/DDP/torchrun/多机多卡)](https://zhuanlan.zhihu.com/p/489011749)

相对 Tensorflow，Pytorch 简单的多。分布式训练主要有两个API：
- DataParallel(`DP`): **PS模式**，1张卡为reduce（parame server），实现就1行代码
  - **单进程多线程**，仅仅能工作在单机中
  - 将数据分割到多个GPU上。典型的`数据并行`，将模型复制到每个GPU上，一旦**GPU0计算出梯度**，就同步梯度到各个节点，这需要大量的GPU数据传输（类似PS模式）
- DistributedDataParallel(`DDP`): **All-Reduce模式**，单机多卡/多级多卡皆可。官方建议API
  - 多进程，单机或多机
  - 每个GPU进程中创建**模型副本**，并只让数据的一部分对改GPU可用。因为每个GPU中的模型是独立运行的，所以在所有的模型都计算出梯度后，才会在模型之间同步梯度（类似All-reduce）

分析
- `DDP`每个batch只需要一次数据传输；
- `DP`可能存在多次数据同步(不用worker之间可能快慢不一样)。
- DataParallel 通常慢于 DistributedDataParallel

【2024-7-24】PyTorch 为数据分布式训练提供了多种选择。

随着应用从简单到复杂，从原型到产品，常见的开发轨迹可以是：
1. 数据和模型能放入**单个GPU**，单设备训练，此时不用担心训练速度；
1. 服务器上有**多个GPU**，且**代码修改量最小**，加速训练用**单个机器多GPU** `DataParallel`；
1. 进一步加速训练,且愿意写点代码，用单个机器多个GPU `DistributedDataParallel`；
1. 应用程序**跨机器边界**扩展，用多机器`DistributedDataParallel`和**启动脚本**；
1. 预期有错误（比如OOM）或资源可**动态连接和分离**，使用`torchelastic`来启动分布式训练。

分布式训练的场景很多，单机多卡，多机多卡，模型并行，数据并行等等。接下来就以常见的单机多卡的情况进行记录。

PyTorch 使用 DDP（Distributed Data Parallel） 实现了**真正**的分布式`数据并行`，两个场景下都可使用 DDP 实现模型的分布式训练：
- (1) 单机、多 GPU（单进程多线程的**伪**分布式）
- (2) 多机、多 GPU（多机多进程的**真正**分布式）

方法(1)类似简单 DP 数据并行模式
- DP 使用**单进程**、多线程范式来实现；
- 而 DDP 完全使用**多进程**方式，包括单机多进程、多机多进程

即使单机、多 GPU，也建议使用 DDP 模式，实现基于数据并行的模型训练，使用单机 DDP 模式训练模型的性能要比 DP 模式好很多。

DDP 基于**集合通信**（Collective Communications）实现分布式训练过程中的梯度同步。

反向传播过程中，DDP 使用 AllReduce 来实现分布式梯度计算和同步。


### 1、DataParallel

模型与变量必须在同一个设备上（CPU or GPU）

pytorch 使用**to函数**实现变量或模型的**存储转移**
- to函数的对象: 数据Tensor，或 模型Module 
- 张量不执行inplace(即 执行之后重新构建一个新的张量)
- 模型执行inplace(执行之后不重新构建一个新的模型)

原理：
- 当给定model时，主要实现功能是将input数据依据batch的这个维度，将数据划分到指定的设备上。其他的对象(objects)复制到每个设备上。在前向传播的过程中，module被复制到每个设备上，每个复制的副本处理一部分输入数据。
- 在反向传播过程中，每个副本module的梯度被汇聚到原始的module上计算(一般为第0块GPU)。

举例：
- 如果当前有4个GPU，batch_size=16，那么模型将被复制到每一个GPU上，在前向传播时，每一个gpu将分到4个batch，每个gpu独立计算依据分到的batch计算出结果的梯度，然后将梯度返回到第一个GPU上，第一个GPU再进行梯度融合、模型更新。在下一次前向传播的时候，将更新后的模型再复制给每一个GPU。

```py
###	第一步：构建模型
# module 需要分发的模型
# device_ids 可分发的gpu，默认分发到所有看见GPU（环境变量设置的）
# output_device 结果输出设备 通常设置成逻辑gpu的第一个
module = your_simple_net() #你的模型
Your_Parallel_Net = torch.nn.DataParallel(module, device_ids=None, output_device=None)
### 第二步：数据迁移
inputs=inputs.to(device)	
labels=labels.to(device)	
# device通常应为模型输出的output_device，否则无法计算loss
```

代码

```python
import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
import os

input_size = 5
output_size = 2
batch_size = 30
data_size = 30

class RandomDataset(Dataset):
    def __init__(self, size, length):
        self.len = length
        self.data = torch.randn(length, size)

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return self.len

rand_loader = DataLoader(dataset=RandomDataset(input_size, data_size), batch_size=batch_size, shuffle=True)

class Model(nn.Module):
    # Our model
    def __init__(self, input_size, output_size):
        super(Model, self).__init__()
        self.fc = nn.Linear(input_size, output_size)

    def forward(self, input):
        output = self.fc(input)
        print("  In Model: input size", input.size(),
              "output size", output.size())
        return output
model = Model(input_size, output_size)

if torch.cuda.is_available():
    model.cuda()

if torch.cuda.device_count() > 1:
    print("Let's use", torch.cuda.device_count(), "GPUs!")
    # 就这一行！将模型整体复制到每个GPU上，计算完成后各自汇总到ps节点
    model = nn.DataParallel(model)

for data in rand_loader:
    if torch.cuda.is_available():
        input_var = Variable(data.cuda())
    else:
        input_var = Variable(data)
    output = model(input_var)
    print("Outside: input size", input_var.size(), "output_size", output.size())
```

### 2、DDP（官方建议）


#### DP 问题


为什么要引入DDP（DistributedDataParallel）？DP 存在问题

- 1、DP 每个训练批次（batch）中，一个进程上先算出模型权重, 然后再分发到每个GPU上
  - 网络通信就成为了瓶颈，而GPU使用率也通常很低。
  - 显存浪费, 多存储了 n-1 份 模型副本
- 2、每次前向传播时把模型也复制了（即每次更新都复制一遍模型），并且**单进程多线程**会造成`GIL` contention （全局解释器锁争用） 这里进程计算权重使通信成为瓶颈造成了大量的时间浪费，因此引入了DDP。

dp 两个问题：
- 1️⃣ 显存浪费严重。
  - 以单机八卡为例，把模型复制8份放在8张卡上同时推理，因此多付出了**7个**模型（副本）的显存开销；
- 2️⃣ 大模型不适用。
  - 以最新提出的Llama 3.1为例，不经量化（FP16数据类型）的情况下，容纳70B的模型需要140GB的显存，即使是40G一张的A100也无法承受。
  - 而这才仅仅是容纳模型，还没有考虑存放数据，以及训练的话存放梯度数据等。因此数据并行并不适用于70B级别大模型的推理和训练。

DDP采用**多进程**控制多GPU，共同训练模型，一份代码会被pytorch自动分配到n个进程并在n个GPU上运行。 
- DDP运用 `Ring-Reduce`通信算法在每个GPU间对梯度进行通讯，交换彼此的梯度，从而获得所有GPU的梯度。

对比DP，不需要在进行模型本体的通信，因此可以加速训练。

torch.nn.DataParallel
- DataParallel 全程维护一个 optimizer，对各 GPU 上梯度进行求和，而在主 GPU 进行参数更新，之后再将模型参数 broadcast 到其他 GPU

注意：
- 1、设置 DistributedSampler 来打乱数据，因为一个batch被分配到了好几个进程中，要确保不同的GPU拿到的不是同一份数据。
- 2、要告诉每个进程自己的id，即使用哪一块GPU。
- 3、如果需要做BatchNormalization，需要对数据进行同步（还待研究，挖坑）

DDP采用All-Reduce架构，单机多卡、多机多卡都能用。

注意：DDP并不会自动shard数据
1. 如果自己写数据流，得根据`torch.distributed.get_rank()`去shard数据，获取自己应用的一份
2. 如果用 Dataset API，则需要在定义Dataloader的时候用 DistributedSampler 去shard

#### torch.distributed 介绍

torch.nn.DataParallel 支持数据并行，但不支持**多机**分布式训练，且底层实现相较于 distributed 的接口，有些许不足。

Pytorch 通过 torch.distributed 包提供分布式支持，包括 GPU 和 CPU 的分布式训练支持。
- Pytorch 分布式目前只支持 Linux。

`torch.distributed` 优势：
- 每个进程对应一个独立的训练过程，且只对梯度等少量数据进行信息交换。
  - 迭代中，每个进程具有自己的 optimizer ，独立完成所有优化步骤，进程内与一般的训练无异。
  - 各进程梯度计算完成之后，先将梯度进行汇总平均，再由 `rank=0` 的进程，将其 broadcast 到所有进程。最后，各进程用该梯度来更新参数。
  - 各进程的模型参数始终保持一致: 各进程初始参数、更新参数都一致
  - 相比 `DataParallel`, `torch.distributed` 传输的数据量更少，因此速度更快，效率更高
- 每个进程包含独立的解释器和 GIL
  - 每个进程拥有独立的解释器和 GIL，消除了单个 Python 进程中的多个执行线程，模型副本或 GPU 的额外解释器开销和 GIL-thrashing ，因此可以减少解释器和 GIL 使用冲突

#### torch.distributed 概念

【2024-4-7】[Pytorch 分布式训练](https://zhuanlan.zhihu.com/p/76638962)


概念：
- `group`：即**进程组**。默认只有1个组，1个 job 即为1个组，即 1个 world。
  - 当需要进行更加精细的通信时，通过 new_group 接口，使用 word 的子集，创建新组，用于集体通信等。
- `world_size` ：表示**全局进程数**。一个进程可对应**多个**GPU
  - `world_size ≠ GPU数`: 1个进程用多个GPU
  - `world_size = GPU数`: 1个进程用1个GPU
- `local_word_size`: 某个节点上进程数 (相对比较少见)
- `rank`：全局进程id, 表示**进程序号**，用于进程间通讯，表征进程优先级。取值范围: `0~world_size`
  - `rank = 0` 主机为 **master 节点**。
- `local_rank`：某个节点上进程id, 进程内**GPU 编号**，非显式参数，由 `torch.distributed.launch` 内部指定。
  - `rank = 3`，`local_rank = 0` 表示第 3 个进程内的第 1 块 GPU。
- `global_rank`: 全局 gpu编号

如果 所有进程数(`world_size`)为`W`，每个节点上的进程数(`local_world_size`)为`L`, 则每个进程上的两个ID：
- `rank` 取值范围：`[0, W-1]`
  - `rank`=0 进程为**主进程**，负责同步分发工作
  - `rank`>0 进程为**从进程**
  - `rank`=-1, 默认值，非GPU进程?
- `local_rank` 取值：`[0, L-1]`

2机8卡的分布式训练[示例](https://zhuanlan.zhihu.com/p/489892744)
- ![](https://pic1.zhimg.com/80/v2-2baae86e212177108872d36a6040a2dc_1440w.webp)
- gpu 编号: 0~3
- local rank: gpu 本地编号, 0~3
- global rank: gpu 全局编号, 0~7

Pytorch 分布式基本流程：
- 使用 distributed 包任何函数前，用 `init_process_group` 初始化进程组，同时初始化 `distributed` 包。
- 如进行小组内集体通信，用 `new_group` 创建子分组
- 创建分布式并行模型 `DDP(model, device_ids=device_ids)`
- 为数据集创建 Sampler
- 使用启动工具 `torch.distributed.launch` 在每个主机上执行一次脚本，开始训练
- 使用 `destory_process_group()` 销毁进程组

torch.distributed 提供了 3 种初始化方式：**tcp**、**共享文件** 和 **环境变量初始化** 等。
- TCP: 指定进程 0 的 ip 和 port, 手动为每个进程指定进程号。
- 共享文件: 共享文件对于组内所有进程可见
- 环境变量:



测试代码

```py
import torch.distributed as dist
import argparse, os

parser = argparse.ArgumentParser()
parser.add_argument("--local_rank", type=ine, default=0)
args = parser.parse_args()

# 分布式初始化, 读取环境变量 RANK=1 WORLD_SIZE=3 MASTER_ADDR=127.0.0.1 MASTER_PORT=8000
dist.init_process_group("nccl") # 进程组初始化
rank = dist.get_rank()
local_rank_arg = args.local_rank               # 命令行形式ARGS形式
local_rank_env = int(os.environ['LOCAL_RANK']) # 用env初始ENV环境变量形式
local_world_size = int(os.environ['LOCAL_WORLD_SIZE'])
# local_rank_env = int(os.environ.get('LOCAL_RANK', 0)) # 在利用env初始ENV环境变量形式
# local_world_size = int(os.environ.get('LOCAL_WORLD_SIZE', 3))

print(f"{rank=}; {local_rank_arg=}; {local_rank_env=}; {local_world_size=}")
```

执行

```sh
python3 -m torch.distributed.launch --nproc_per_node=4 test.py 
```

在一台4卡机器上执行, 样例输出：

```sh
# WARNING:torch.distributed.run:
# *****************************************
# Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
# *****************************************
rank=2; local_rank_arg=2; local_rank_env=2, local_world_size=4
rank=0; local_rank_arg=0; local_rank_env=0, local_world_size=4
rank=3; local_rank_arg=3; local_rank_env=3, local_world_size=4
rank=1; local_rank_arg=1; local_rank_env=1, local_world_size=4
```

一般分布式训练都是为每个进程赋予一块GPU，这样比较简单而且容易调试。 这种情况下，可以通过 local_rank 作为当前进程GPU的id。

#### 数据读取 


pytorch 分布式训练，数据读取采用**主进程预读取并缓存**，其它进程从**缓存**中读取，不同进程之间的数据同步具体通过torch.distributed.barrier()实现。[参考](https://www.cnblogs.com/pyclq/p/15433787.html)
- 分布式数据读取： `主进程`读取数据 → `主进程`缓存 → `从进程`读取缓存 

进程号rank

多进程上下文中，通常假定`rank 0`是第一个进程/主进程，其它进程分别具有 0，1，2 不同rank号，这样总共具有4个进程。

（2）单一进程数据处理

通有些操作没必要并行处理，如: 数据读取与处理操作，只需要一个进程进行处理并缓存，然后与其它进程**共享缓存处理数据**
- 但由于不同进程同步执行，单一进程处理数据必然会导致进程间不同步现象（数据读取操作处理时间较长）对于较短时间的单一进程程序运行不会影响线程不同步的情况

为此，torch中采用了`barrier()`函数对其它**非主进程**进行阻塞，达到同步目的

（3）barrier()具体原理

如果执行 create_dataloader()函数的进程
- 不是主进程: 即rank不等于0或者-1
  - 上下文管理器会执行相应的 `torch.distributed.barrier()`，设置一个**阻塞栅栏**，让此进程处于**等待**状态，等待所有进程到达栅栏处（包括主进程数据处理完毕）；
- 是主进程: 其会直接读取数据，然后处理结束之后会遇到 `torch.distributed.barrier()`

此时，所有进程都到达了当前的栅栏处，这样所有进程就达到了同步，并同时得到释放。

```py
def create_dataloader():
    #使用上下文管理器中实现的barrier函数确保分布式中的主进程首先处理数据，然后其它进程直接从缓存中读取
    with torch_distributed_zero_first(rank):
        dataset = LoadImagesAndLabels()
 
from contextlib import contextmanager
 
#定义的用于同步不同进程对数据读取的上下文管理器
@contextmanager
def torch_distributed_zero_first(local_rank: int):
    """
    Decorator to make all processes in distributed training wait for each local_master to do something.
    """
    if local_rank not in [-1, 0]:
        torch.distributed.barrier()
    yield   #中断后执行上下文代码，然后返回到此处继续往下执行
    if local_rank == 0:
        torch.distributed.barrier()
```
 
#### 初始化进程组 init_process_group

`init_process_group` 函数原型

```py
torch.distributed.init_process_group(backend, init_method=None, timeout=datetime.timedelta(0, 1800), 
                                     world_size=-1, rank=-1, store=None)
```

函数作用
- 每个进程中进行调用，用于初始化该进程。
- 使用分布式时，该函数必须在 distributed 内所有相关函数之前使用。

参数详解
- `backend` ：指定当前进程要使用的通信后端
  - 小写字符串，支持的通信后端有 `gloo`, `mpi`, `nccl`, 建议用 `nccl`。
  - cpu 分布式选 `gloo`
  - gpu 分布式选 `nccl`
- `init_method` ：当前进程组初始化方式
  - 可选参数，字符串形式。两种方式: `init_method` + `store`, `init_method`是`store`的高层封装, 二者互斥
  - `init_method`: **TCP连接**、File**共享文件**系统、**ENV环境变量**三种方式
  - `store`: 同时指定world_size 和 rank参数。store 是一种分布式中核心的key-value存储，用于不同进程间共享信息
  - 如果未指定, 默认为 `env`，表示使用读取环境变量方式初始化。该参数与 store 互斥。
- `rank` ：指定当前进程的优先级
- `int` 值。表示当前进程的编号，即优先级。如果指定 store 参数，则必须指定该参数。
  - rank=0 的为主进程，即 master 节点。
- `world_size` ：该 job 中的总进程数。如果指定 store 参数，则需要指定该参数。
- `timeout` ： 指定每个进程的超时时间
  - 可选参数，datetime.timedelta 对象，默认为 30 分钟。该参数仅用于 Gloo 后端。
- `store`
  - 所有 worker 可访问的 key / value，用于交换连接 / 地址信息。与 init_method 互斥。

三种init_method：
- `init_method`='**tcp://ip:port**'： 通过指定rank 0（MASTER进程）的IP和端口，各个进程**tcp**进行信息交换。需指定 rank 和 world_size 这两个参数。
- `init_method`='**file://path**'：通过所有进程都可以访问**共享文件系统**来进行信息共享。需要指定rank和world_size参数。
- `init_method`=**env://**：从**环境变量**中读取分布式信息(os.environ)，主要包括 `MASTER_ADDR`, `MASTER_PORT`, `RANK`, `WORLD_SIZE`。 其中，rank和world_size可手动指定，否则从环境变量读取。

tcp 和 env 两种方式比较类似, 其实 env就是对tcp 一层封装），都是通过**网络地址**方式进行通信，最常用的初始化方法。

```py
import os, argparse
import torch
import torch.distributed as dist

parse = argparse.ArgumentParser()
parse.add_argument('--init_method', type=str)
parse.add_argument('--rank', type=int)
parse.add_argument('--ws', type=int)
args = parse.parse_args()

if args.init_method == 'TCP':
	dist.init_process_group('nccl', init_method='tcp://127.0.0.1:28765', rank=args.rank, world_size=args.ws)
elif args.init_method == 'ENV':
    dist.init_process_group('nccl', init_method='env://')

rank = dist.get_rank()
print(f"rank = {rank} is initialized")
# 单机多卡情况下，localrank = rank. 严谨应该是local_rank来设置device
torch.cuda.set_device(rank)
tensor = torch.tensor([1, 2, 3, 4]).cuda()
print(tensor)
```

单机双卡机器上，开两个终端，同时运行命令

```py
# TCP方法
python3 test_ddp.py --init_method=TCP --rank=0 --ws=2
python3 test_ddp.py --init_method=TCP --rank=1 --ws=2
# ENV方法
MASTER_ADDR='localhost' MASTER_PORT=28765 RANK=0 WORLD_SIZE=2 python3 test_gpu.py --init_method=ENV
MASTER_ADDR='localhost' MASTER_PORT=28765 RANK=1 WORLD_SIZE=2 python3 test_gpu.py --init_method=ENV
```

如果开启的进程未达到 word_size 的数量，则所有进程会一直等待，直到都开始运行，可以得到输出如下：

```py
# rank0 的终端：
rank 0 is initialized
tensor([1, 2, 3, 4], device='cuda:0')
# rank1的终端
rank 1 is initialized
tensor([1, 2, 3, 4], device='cuda:1')
```

说明
- 初始化DDP时，给后端提供主进程的**地址端口**、本身**RANK**，以及**进程数量**即可。
- 初始化完成后，可以执行很多分布式的函数，比如 dist.`get_rank`, dist.`all_gather` 等等。



**new_group**

函数声明

```py
torch.distributed.new_group(ranks=None, timeout=datetime.timedelta(0, 1800), backend=None)
```

函数作用
- `new_group()` 函数可用于使用所有进程的任意子集来创建新组。其返回一个分组句柄，可作为 collectives 相关函数的 group 参数 。collectives 是分布式函数，用于特定编程模式中的信息交换。

参数详解
- ranks：指定新分组内的成员的 ranks 列表list ，其中每个元素为 int 型
- timeout：指定该分组进程组内的操作的超时时间
  - 可选参数，datetime.timedelta 对象，默认为 30 分钟。该参数仅用于 Gloo 后端。
- backend：指定要使用的通信后端
  - 小写字符串，支持的通信后端有 gloo，nccl ，必须与 init_process_group() 中一致。

其它函数
- get_backend 获取进程组属性 
- get_rank 获取分布式进程组组内的每个进程的唯一识别
- get_world_size  获取进程组内的进程数
- is_initialized 检查默认进程组是否被初始化
- is_mpi_available 检查 MPI 后端是否可用
- is_nccl_available 检查 NCCL 后端是否可用

##### (1) TCP 初始化

```py
import torch.distributed as dist

# Use address of one of the machines
dist.init_process_group(backend, init_method='tcp://10.1.1.20:23456',rank=args.rank, world_size=4)
```

说明
- 不同进程内，均使用主进程的 ip 地址和 port，确保每个进程能够通过一个 master 进行协作。该 ip 一般为主进程所在的主机的 ip，端口号应该未被其他应用占用。
- 实际使用时，在每个进程内运行代码，并需要为每一个进程手动指定一个 rank，进程可以分布与相同或不同主机上。
- 多个进程之间，同步进行。若其中一个出现问题，其他的也马上停止。

使用

```py
# Node 1
python mnsit.py --init-method tcp://192.168.54.179:22225 --rank 0 --world-size 2
# Node 2
python mnsit.py --init-method tcp://192.168.54.179:22225 --rank 1 --world-size 2
```

初始化示例
- `tcp_init.py`

```py
import torch.distributed as dist
import torch.utils.data.distributed
# ......
parser = argparse.ArgumentParser(description='PyTorch distributed training on cifar-10')
parser.add_argument('--rank', default=0, help='rank of current process')
parser.add_argument('--word_size', default=2,help="word size")
parser.add_argument('--init_method', default='tcp://127.0.0.1:23456', help="init-method")
args = parser.parse_args()
# ......
dist.init_process_group(backend='nccl', init_method=args.init_method, rank=args.rank, world_size=args.word_size)
# ......
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=download, transform=transform)
train_sampler = torch.utils.data.distributed.DistributedSampler(trainset)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, sampler=train_sampler)
# ......
net = Net()
net = net.cuda()
net = torch.nn.parallel.DistributedDataParallel(net)
```

执行方式
- `init_method`

```sh
# Node 1 : ip 192.168.1.201  port : 12345
python tcp_init.py --init_method tcp://192.168.1.201:12345 --rank 0 --word_size 3
# Node 2 : 
python tcp_init.py --init_method tcp://192.168.1.201:12345 --rank 1 --word_size 3
# Node 3 : 
python tcp_init.py --init_method tcp://192.168.1.201:12345 --rank 2 --word_size 3
```

说明
- TCP 方式中，`init_process_group` 中必须手动指定以下参数
  - `rank` 为当前进程的进程号
  - `word_size` 为当前 job 总进程数
  - `init_method` 内指定 **tcp 模式**，且所有进程的 `ip:port` 必须一致，设定为主进程的 `ip:port`
- 必须在 rank==0 的进程内保存参数。
- 若程序内未根据 rank 设定当前进程使用的 GPUs，则默认使用**全部 GPU**，且以**数据并行**方式使用。
- 每条命令表示一个进程。若已开启的进程未达到 word_size 的数量，则所有进程会一直等待
- 每台主机上可以开启多个进程。但是，若未为每个进程分配合适的 GPU，则同机不同进程可能会共用 GPU，应该坚决避免这种情况。
- 使用 gloo 后端进行 GPU 训练时，会报错。
- 若每个进程负责多块 GPU，可以利用多 GPU 进行模型并行。

```py
class ToyMpModel(nn.Module):
    def init(self, dev0, dev1):
        super(ToyMpModel, self).init()
        self.dev0 = dev0
        self.dev1 = dev1
        self.net1 = torch.nn.Linear(10, 10).to(dev0)
        self.relu = torch.nn.ReLU()
        self.net2 = torch.nn.Linear(10, 5).to(dev1)

def forward(self, x):
       x = x.to(self.dev0)
       x = self.relu(self.net1(x))
       x = x.to(self.dev1)
       return self.net2(x)
# ......
dev0 = rank * 2
dev1 = rank * 2 + 1
mp_model = ToyMpModel(dev0, dev1)
ddp_mp_model = DDP(mp_model)
# ......
```

##### (2) 共享文件初始化

共享的文件对于组内所有进程可见

设置方式如下：

```py
import torch.distributed as dist

# rank should always be specified
dist.init_process_group(backend, init_method='file:///mnt/nfs/sharedfile',
                        world_size=4, rank=args.rank)
```

说明
- `file://`前缀表示文件系统各式初始化。
- `/mnt/nfs/sharedfile` 表示共享文件，各个进程在共享文件系统中通过该文件进行同步或异步。

因此，所有进程必须对该文件具有读写权限。
- 每一个进程将会打开这个文件，写入自己的信息，并等待直到其他所有进程完成该操作
- 在此之后，所有的请求信息将会被所有的进程可访问，为了避免 race conditions，文件系统必须支持通过 fcntl 锁定（大多数的 local 系统和 NFS 均支持该特性）。

说明：
- 若指定为同一文件，则每次训练开始之前，该文件必须手动删除，但是文件所在路径必须存在！

与 tcp 初始化方式一样，也需要为每一个进程手动指定 rank。

使用

```py
# 主机 01 上：
python mnsit.py --init-method file://PathToShareFile/MultiNode --rank 0 --world-size 2
# 主机 02 上：
python mnsit.py --init-method file://PathToShareFile/MultiNode --rank 1 --world-size 2
```

相比于 TCP 方式, 麻烦一点的是运行完一次必须更换共享的文件名，或者删除之前的共享文件，不然第二次运行会报错。

##### (3) Env 初始化(默认)

默认情况下都是环境变量来进行分布式通信，指定 `init_method="env://"`。

通过在所有机器上设置如下四个环境变量，所有进程将会适当的连接到 master，获取其他进程的信息，并最终与它们握手(信号)。
- `MASTER_PORT`: 必须指定，表示 rank0上机器的一个空闲端口（必须设置）
- `MASTER_ADDR`: 必须指定，除了 rank0 主机，表示主进程 rank0 机器的地址（必须设置）
- `WORLD_SIZE`: 可选，总进程数，可以这里指定，在 init 函数中也可以指定
- `RANK`: 可选，当前进程的 rank，也可以在 init 函数中指定

配合 torch.distribution.launch 使用。

实例

```sh
# Node 1: (IP: 192.168.1.1, and has a free port: 1234)
python -m torch.distributed.launch --nproc_per_node=NUM_GPUS_YOU_HAVE
           --nnodes=2 --node_rank=0 --master_addr="192.168.1.1"
           --master_port=1234 YOUR_TRAINING_SCRIPT.py (--arg1 --arg2 --arg3
           and all other arguments of your training script)
# Node 2
python -m torch.distributed.launch --nproc_per_node=NUM_GPUS_YOU_HAVE
           --nnodes=2 --node_rank=1 --master_addr="192.168.1.1"
           --master_port=1234 YOUR_TRAINING_SCRIPT.py (--arg1 --arg2 --arg3
           and all other arguments of your training script)
```

代码 `env_init.py`

```py
import torch.distributed as dist
import torch.utils.data.distributed

# ......
import argparse
parser = argparse.ArgumentParser()
# 注意这个参数，必须要以这种形式指定，即使代码中不使用。因为 launch 工具默认传递该参数
parser.add_argument("--local_rank", type=int)
args = parser.parse_args()

# ......
dist.init_process_group(backend='nccl', init_method='env://')

# ......
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=download, transform=transform)
train_sampler = torch.utils.data.distributed.DistributedSampler(trainset)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, sampler=train_sampler)

# ......
# 根据 local_rank，配置当前进程使用的 GPU
net = Net()
device = torch.device('cuda', args.local_rank)
net = net.to(device)
net = torch.nn.parallel.DistributedDataParallel(net, device_ids=[args.local_rank], output_device=args.local_rank)
```

执行方式

```py
# 节点0
python -m torch.distributed.launch --nproc_per_node=2 --nnodes=3 --node_rank=0 --master_addr="192.168.1.201" --master_port=23456 env_init.py
# 节点1
python -m torch.distributed.launch --nproc_per_node=2 --nnodes=3 --node_rank=1 --master_addr="192.168.1.201" --master_port=23456 env_init.py
# 节点2
python -m torch.distributed.launch --nproc_per_node=2 --nnodes=3 --node_rank=2 --master_addr="192.168.1.201" --master_port=23456 env_init.py
```

说明
- Env 方式中，`init_process_group` 无需指定任何参数
- 必须在 `rank==0` 的进程内保存参数。

该方式使用 `torch.distributed.launch` 在每台主机上创建**多进程**，其中:
- `nproc_per_node` 参数指定为当前主机创建的进程数。一般设定为当前主机的 GPU 数量
- `nnodes` 参数指定当前 job 包含多少个节点
- `node_rank` 指定当前节点的优先级
- `master_addr` 和 `master_port` 分别指定 master 节点的 ip:port
- 若没有为每个进程合理分配 GPU，则默认使用当前主机上所有的 GPU。即使一台主机上有多个进程，也会共用 GPU。
- 使用 `torch.distributed.launch` 工具时，为当前主机创建 `nproc_per_node` 个进程，每个进程独立执行训练脚本。同时，它还会为每个进程分配一个 `local_rank` 参数，表示当前进程在当前主机上的编号。
  - 例如：r`ank=2`, `local_rank=0` 表示第 3 个节点上的第 1 个进程。
- 需要合理利用 `local_rank` 参数，来合理分配本地的 GPU 资源
- 每条命令表示一个进程。若已开启的进程未达到 `word_size` 数量，则所有进程会一直等待


详见: [Pytorch 分布式训练](https://zhuanlan.zhihu.com/p/76638962)

#### GPU 启动方式

常见的GPU 启动方式
- torch.`multiprocessing`: 容易控制, 更加灵活
- torch.`distributed.launch`: 代码量少, 启动速度快
- `torchrun`: `distributed.launch` 的进化版, 代码量更少
- Slurm Workload Manager: slurm 启动近期更新掉

DDP 本身是一个 python **多进程**，完全可以直接通过**多进程**方式来启动分布式程序。

torch 提供**两种**启动工具运行torch DDP程序。
- torch.multiprocessing
- launch/run

##### (1) mp.spawn

用 torch.`multiprocessing`（python multiprocessing的封装类) 自动生成多个进程

基本的调用函数 spawn:

```py
mp.spawn(fn, args=(), nprocs=1, join=True, daemon=False)
```

其中:
- `fn`: 进程**入口函数**，第一个参数会被默认自动加入当前进程的rank， 即实际调用： fn(rank, *args)
- `nprocs`: **进程数量**，即：world_size
- `args`: 函数fn的其他常规参数以tuple形式传递

示例

```py
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def fn(rank, ws, nums):
    dist.init_process_group('nccl', init_method='tcp://127.0.0.1:28765', rank=rank, world_size=ws)
    rank = dist.get_rank()
    print(f"rank = {rank} is initialized")
    torch.cuda.set_device(rank)
    tensor = torch.tensor(nums).cuda()
    print(tensor)

if __name__ == "__main__":
    ws = 2
    mp.spawn(fn, nprocs=ws, args=(ws, [1, 2, 3, 4]))
```

命令 

```sh
python3 test_ddp.py
```

输出如下：

```sh
rank = 0 is initialized
rank = 1 is initialized
tensor([1, 2, 3, 4], device='cuda:1')
tensor([1, 2, 3, 4], device='cuda:0')
```

这种方式同时适用于 TCP 和 ENV 初始化。

##### (2) launch/run

torch 提供的 `torch.distributed.launch` 工具，以模块形式直接执行：

```sh
python3 -m torch.distributed.launch --配置 train.py --args参数
```

常用配置有:
- --`nnodes`: 使用的机器数量，单机的话，就默认是1了
- --`nproc_per_node`: 单机的进程数，即单机的worldsize
- --`master_addr`/`port`: 使用的主进程rank0的地址和端口
- --`node_rank`: 当前的进程rank

单机情况下
- 只有 --`nproc_per_node` 是必须指定
- --`master_addr`/`port` 和 `node_rank` 都是可以由launch通过环境自动配置

```py
mport torch
import torch.distributed as dist
import torch.multiprocessing as mp
import os

dist.init_process_group('nccl', init_method='env://')

rank = dist.get_rank()
local_rank = os.environ['LOCAL_RANK']
master_addr = os.environ['MASTER_ADDR']
master_port = os.environ['MASTER_PORT']
print(f"rank = {rank} is initialized in {master_addr}:{master_port}; local_rank = {local_rank}")
torch.cuda.set_device(rank)
tensor = torch.tensor([1, 2, 3, 4]).cuda()
print(tensor)
```

启动命令

```sh
python3 -m torch.distribued.launch --nproc_per_node=2 test_ddp.py
```

输出如下：

```sh
rank = 0 is initialized in 127.0.0.1:29500; local_rank = 0
rank = 1 is initialized in 127.0.0.1:29500; local_rank = 1
tensor([1, 2, 3, 4], device='cuda:1')
tensor([1, 2, 3, 4], device='cuda:0')
```

##### (3) torchrun

torch 1.10 开始用终端命令 `torchrun` 来代替 `torch.distributed.launch`
- `torchrun` 实现了 launch 的一个**超集**

不同：
- 完全使用环境变量配置各类参数，如 RANK,LOCAL_RANK, WORLD_SIZE 等，尤其是 local_rank 不再支持用命令行隐式传递的方式
- 更加优雅处理某个worker失败情况，重启worker。
  - 需要代码中有 load_checkpoint(path) 和 save_checkpoint(path) 这样有worker失败的话，可以通过load最新的模型，重启所有的worker接着训练。
- 训练节点数目可以**弹性**变化。

上面代码直接使用运行即可，不用写那么长长的命令了。

```sh
torchrun --nproc_per_node=2 test_gpu.py
```

注意
- torchrun 或者 launch 对上面`ENV`初始化方法支持最完善, `TCP`初始化方法的可能会出现问题，尽量使用env来初始化dist。



#### torch.distributed 使用

使用方式(单机多卡环境)

```py
# 启动方式，shell中运行：
python -m torch.distributed.launch --nnodes 1 --nproc_per_node=4  YourScript.py
# nnodes: 表示有多少个节点，可以通俗的理解为有多少台机器
# nproc_per_node 表示每个节点上有多少个进程，每个进程一般独占一块GPU
########################## 	第1步	 ##########################
#初始化
'''
在启动器为我们启动python脚本后，在执行过程中，启动器会将当前进程的（其实就是 GPU的）index 通过参数传递给 python，
我们可以这样获得当前进程的 index：即通过参数 local_rank 来告诉我们当前进程使用的是哪个GPU，
用于我们在每个进程中指定不同的device
'''
parse.add_argument('--local_rank',type=int)
args=parser.parse_args()
local_rank=args.local_rank
torch.cuda.set_device(local_rank)
'''
init_process_group用于初始化GPU通信方式（NCCL）和参数的获取方式（env代表通过环境变量）
gpu使用nccl最快，gloo为cpu分布式训练，mpu则需要重新编码
init_method 指定如何初始化进程组的 URL。 
默认及推荐为'env://' 其他初始化方式与多机多卡有关（not sure，挖个坑）
'''
torch.distributed.init_process_group('nccl'，init_method='env://')
device = torch.device(f'cuda:{args.local_rank}')
##########################	第2步  ##########################
#处理Dataloader
train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset,shuffle=True)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=..., sampler=train_sampler)
#torch.utils.data.DataLoader中的shuffle应该设置为False（默认），因为打乱的任务交给了sampler
##########################	第3步  ##########################
#模型的初始化
model=torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.local_rank])
'''
使用 DistributedDataParallel 包装模型，
它能帮助我们为不同 GPU 上求得的梯度进行allreduce（即汇总不同 GPU 计算所得的梯度，并同步计算结果）。
allreduce 后不同 GPU 中模型的梯度均为 allreduce 之前各 GPU 梯度的均值。
''''
##########################	第4步  ##########################
#同DP，进行inputs、labels的设备转移
```


```py
sampler = DistributedSampler(dataset) # 这个sampler会自动分配数据到各个gpu上
DataLoader(dataset, batch_size=batch_size, sampler=sampler)
```

完整代码如下：

```py
import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
import os
from torch.utils.data.distributed import DistributedSampler
# 1) 初始化
torch.distributed.init_process_group(backend="nccl")

input_size = 5
output_size = 2
batch_size = 30
data_size = 90

# 2） 配置每个进程的gpu
local_rank = torch.distributed.get_rank()
torch.cuda.set_device(local_rank)
device = torch.device("cuda", local_rank)

class RandomDataset(Dataset):
    def __init__(self, size, length):
        self.len = length
        self.data = torch.randn(length, size).to('cuda')

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return self.len

dataset = RandomDataset(input_size, data_size)
# 3）使用DistributedSampler
rand_loader = DataLoader(dataset=dataset,
                         batch_size=batch_size,
                         sampler=DistributedSampler(dataset))

class Model(nn.Module):
    def __init__(self, input_size, output_size):
        super(Model, self).__init__()
        self.fc = nn.Linear(input_size, output_size)

    def forward(self, input):
        output = self.fc(input)
        print("  In Model: input size", input.size(),
              "output size", output.size())
        return output

model = Model(input_size, output_size)

# 4) 封装之前要把模型移到对应的gpu
model.to(device)

if torch.cuda.device_count() > 1:
    print("Let's use", torch.cuda.device_count(), "GPUs!")
    # 5) 封装：
    model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[local_rank], output_device=local_rank)

for data in rand_loader:
    if torch.cuda.is_available():
        input_var = data
    else:
        input_var = data
    output = model(input_var)
    print("Outside: input size", input_var.size(), "output_size", output.size())
```

执行脚本：

```shell
# 启用 DDP 模式
CUDA_VISIBLE_DEVICES=0,1 python -m torch.distributed.launch --nproc_per_node=2 torch_ddp.py
```

apex加速(混合精度训练、并行训练、同步BN)可[参考](https://zhuanlan.zhihu.com/p/158375055)


### 代码分布式改造

如何将单机训练代码改成分布式运行？

基本流程：
- 分布式训练数据加载
- 分布式训练
- 分布式评估


#### 分布式数据集

`Dataloader` 要把所有数据分成N份(N为worldsize), 并能正确分发到不同进程中，每个进程可以拿到一个数据的子集，不重叠，不交叉。

这部分工作靠 `DistributedSampler` 完成，函数签名如下:

```py
torch.utils.data.distributed.DistributedSampler(dataset,
				num_replicas=None, rank=None, shuffle=True, seed=0, drop_last=False)
```

参数说明
- `dataset`: 需要加载的完整数据集
- `num_replicas`： 把数据集分成多少份，默认是当前dist的world_size
- `rank`: 当前进程的id，默认从dist的rank
- `shuffle`：是否打乱
- `drop_last`: 如果数据长度不能被world_size整除，可以考虑是否将剩下的扔掉
- `seed`：随机数种子。
  - 注意: 从源码中可以看出，真正的种子其实是 self.seed + self.epoch, 好处是，不同epoch每个进程拿到的数据是不一样，因此要在每个epoch开始前设置下：`sampler.set_epoch(epoch)`

Sampler 实现核心代码：

```py
indices[self.rank: self.total_size: self.num_replicas]
```

假设4卡12条数据，rank=0,1,2,3, num_replicas=4, 那么每个卡取的数据索引就是：

```sh
rank0: [0 4 8]; rank1: [1 5 9]; rank2: [2 6 10]; rank3: [3 7 11]
```

保证不重复不交叉。这样在分布式训练的时候，只需要给 Dataloader 指定 DistributedSampler 即可，简单示例如下：

```py
sampler = DistributedSampler(dataset)
loader = DataLoader(dataset, sampler=sampler)
for epoch in range(start_epoch, n_epochs):
  sampler.set_epoch(epoch) # 设置epoch 更新种子
  train(loader)
```

模型的分布式训练封装。将单机模型使用 torch.nn.parallel.`DistributedDataParallel` 进行封装，如下：

```py
torch.cuda.set_device(local_rank)
model = Model().cuda()
model = DistributedDataParallel(model, device_ids=[local_rank])
# 要调用model内的函数或者属性. model.module.xxxx
```

多卡训练时，每个进程有一个model副本和optimizer，使用自己的数据进行训练，之后**反向传播**计算完梯度的时候，所有进程的梯度会进行 all-reduce 操作进行同步，进而保证每个卡上的模型更新梯度是一样的，模型参数也是一致的。

注意
- 在save和load模型时候，为了减小所有进程同时读写磁盘，以**主进程**为主，rank0 先save模型，在map到其他进程。
- 另外一个好处: 最开始训练时，模型随机初始化之后，保证了所有进程的模型参数保持一致。

torch的DDP封装时，已经做到了这一点，即使开始随机初始化不同，经过DDP封装，所有进程都一样的参数

简洁代码如下：

```py
model = DistributedDataParallel(model, device_ids=[local_rank])
CHECKPOINT_PATH ="./model.checkpoint"
if rank == 0:
  torch.save(ddp_model.state_dict(), CHECKPOINT_PATH)
# barrier()其他保证rank 0保存完成
dist.barrier()
map_location = {"cuda:0": f"cuda:{local_rank}"}
model.load_state_dict(torch.load(CHECKPOINT_PATH, map_location=map_location))
# 后面正常训练代码
optimizer = xxx
for epoch:
  for data in Dataloader:
      model(data)
      xxx
    # 训练完成 只需要保存rank 0上的即可
    # 不需要dist.barrior()， all_reduce 操作保证了同步性
  if rank == 0:
     torch.save(ddp_model.state_dict(), CHECKPOINT_PATH)
```

#### 分布式训练

DDP分布式训练步骤：
- 初始化进程组 dist.init_process_group
- 设置分布式采样器 DistributedSampler
- 使用DistributedDataParallel封装模型
- 使用torchrun 或者 mp.spawn 启动分布式训练

使用分布式做 evaluation 时，要先把所有进程的输出结果进行 gather，再进行指标计算，两个常用函数:

```py
dist.all_gather(tensor_list, tensor) # 将所有进程的tensor进行收集并拼接成新的tensorlist返回，比如:
dist.all_reduce(tensor, op) # 对tensor 的 in-place 操作, 对所有进程的某个tensor进行合并操作，op可以是求和等
```

代码

```py
import torch
import torch.distributed as dist

dist.init_process_group('nccl', init_method='env://')
rank = dist.get_rank()
torch.cuda.set_device(rank)

tensor = torch.arange(2) + 1 + 2 * rank
tensor = tensor.cuda()
print(f"rank {rank}: {tensor}")

tensor_list = [torch.zeros_like(tensor).cuda() for _ in range(2)]
dist.all_gather(tensor_list, tensor)
print(f"after gather, rank {rank}: tensor_list: {tensor_list}")

dist.barrier()
dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
print(f"after reduce, rank {rank}: tensor: {tensor}")
```

命令

```sh
torchrun --nproc_per_node=2 test_ddp.py
```

输出结果如下:

```sh
rank 1: tensor([3, 4], device='cuda:1')
rank 0: tensor([1, 2], device='cuda:0')
after gather, rank 1: tensor_list: [tensor([1, 2], device='cuda:1'), tensor([3, 4], device='cuda:1')]
after gather, rank 0: tensor_list: [tensor([1, 2], device='cuda:0'), tensor([3, 4], device='cuda:0')]
after reduce, rank 0: tensor: tensor([4, 6], device='cuda:0')
after reduce, rank 1: tensor: tensor([4, 6], device='cuda:1')
```

#### 分布式评估

evaluation 时，可以拿到所有进程中模型输出，最后统一计算指标，基本流程如下：

```py
pred_list = []
for data in Dataloader:
    pred = model(data)
    batch_pred = [torch.zeros_like(label) for _ in range(world_size)]
    dist.all_gather(batch_pred, pred)
    pred_list.extend(batch_pred)
pred_list = torch.cat(pred_list, 1)
# 所有进程pred_list是一致的，保存所有数据模型预测的值
```


### pytorch 分布式操作

【2024-8-4】[彻底搞清楚torch. distributed分布式数据通信all_gather、all_reduce](https://zhuanlan.zhihu.com/p/712631827?utm_psn=1803475758301179905)

all_gather和all_reduce；gather、reduce、scatter方法对比
- ![](https://pic2.zhimg.com/80/v2-ff290214bab003c79d6a28363d65bc7d_1440w.webp)

#### all_gather

分布式操作
- gather 操作用于在**不同节点间收集信息**
- 首先初始化一个空 Tensor 列表 tensor_list, 用于接收所有节点的信息
- 然后调用 all_gather 在所有节点中得到包含每个节点本地张量的列表
- 列表中有 world_size 个元素，每个元素都是bs大小，后续通过cat操作即可得到大小为 bs * world_size 表示

Pytorch DDP 分布式数据合并通信 torch.distributed.all_gather()

[torch.distributed.all_gather()](https://pytorch.org/docs/master/distributed.html?highlight=all_gather#torch.distributed.all_gather)

函数定义
- `tensor_list` 是list，大小是 word_size，每个元素为了是gather后，保存每个rank的数据，所以初始化一般使用torch.empty；
- `tensor` 代表各rank中的tensor数据，其中tensor_list每个分量的维度要与对应的tensor参数中每个rank的维度相同。

```py
all_gather(tensor_list, tensor, group=None, async_op=False)：
```

- tensor_list 每个元素代表每个rank的数据
- tensor 代表每个进程中的tensor数据
- 其中tensor_list每个分量的维度要与对应的tensor参数中每个rank的维度相同。



```py
# 两个机器，每个4张卡，批大小为bs
tensor = torch.arange(bs, dtype=torch.int64) + 1 + 2 * rank
tensor_list = [torch.zeros(bs, dtype=torch.int64) for _ in range(torch.distributed.get_world_size())]
dist.all_gather(tensor_list, tensor)
tensor_list
```

#### all_reduce


all_reduce 操作用于在不同节点中**同步信息**
- 调用该方法, 在所有节点中**求和/平均**，使用前后大小均为bs

```py
tensor = torch.arange(bs, dtype=torch.int64) + 1 + 2 * rank
dist.all_reduce(tensor, op=ReduceOp.SUM)
tensor
```

all_reduce 函数定义
- tensor 代表各rank中的tensor数据，op代表可以选择的操作，主要有: SUM、PRODUCT、MIN,MAX、BAND、BOR、BXOR、PREMUL_SUM


### Torchrun (更新)


PyTorch 官网介绍
- This module（torch.distributed.launch） is going to be deprecated in favor of `torchrun`.

Pytorch 1.9.0 引入了 `torchrun`，替代以前的 `torch.distributed.launch`。
- [torchrun](https://pytorch.org/docs/stable/elastic/run.html#launcher-api) 是 `torch.distributed.launch` 的超集, elastic launch, 等效于 `python -m torch.distributed.run`
- [torchrun](https://pytorch.org/docs/stable/elastic/run.html#launcher-api) 包含 `torch.distributed.launch` 几乎所有功能(除了废弃的`--use-env`)

`torchrun` 包含了 torch.distributed.launch 所有功能，还有三点额外功能：
- 1、`worker_rank` 和 `world_size` 将被自动分配
- 2、`Failover`: worker失败时, 重新启动所有workers来处理 workers 故障
- 3、`Elastic`: 动态增减节点, 允许节点数目在最大/最小值之间改变, 即具备**弹性**


#### 用法

几种模式
- 单机多卡 torchrun --standalone --nnodes=1 --nproc_per_node=N inference.py --args
- 多机多卡 torchrun --nnodes=M --nproc_per_node=N inference.py --args

--nnodes：计算节点（也就是机器）的数量，单机的话就是1，M机的话就是M
--nproc_per_node：每个节点（每台机器）上进程的数量。因为一个进程需要放在一张显卡上跑，因此进程的数量也就是显卡的数量，比如单机八卡，就要将该参数设置为8
--args：运行inference.py脚本所需的参数




#### torchrun 示例


2机8卡 分布式训练[示例](https://zhuanlan.zhihu.com/p/489892744)
- ![](https://pic1.zhimg.com/80/v2-2baae86e212177108872d36a6040a2dc_1440w.webp)
- gpu 编号: 0~3
- local rank: gpu 本地编号, 0~3
- global rank: gpu 全局编号, 0~7

环境
- code: [BetterDL - train_elastic.py](https://github.com/tingshua-yts/BetterDL/blob/master/test/pytorch/DDP/train_elastic.py)
- 运行环境: 2台4卡 v100机器

train_elastic.py

```py
def run():
    env_dict = {
        key: os.environ[key]
        for key in ("MASTER_ADDR", "MASTER_PORT", "WORLD_SIZE", "LOCAL_WORLD_SIZE")
    }
    print(f"[{os.getpid()}] Initializing process group with: {env_dict}")
    dist.init_process_group(backend="nccl")
    train()
    dist.destroy_process_group()

if __name__ == "__main__":
    run()
```

启动脚本 run_elastic.sh 
- node0 和 node1 上分别执行脚本

```sh
torchrun \
    --nnodes=1:3\
    --nproc_per_node=4\
    --max_restarts=3\
    --rdzv_id=1\
    --rdzv_backend=c10d\
    --rdzv_endpoint="192.0.0.1:1234"\
    train_elastic.py
```

描述如下（注：node0和node1均通过该脚本进行启动）
- --`nnodes`=**1:3**: 当前训练任务接受最少1个node，最多3个node, 参与分布式训练；
- --`nproc_per_node`=4: 每个node上节点有4个process
- --`max_restarts`=3: worker group最大的重启次数；
  - 注意: node fail、node scale down和node scale up都会导致restart；
- --`rdzv_id`=1：一个unique的job id，所有node均使用同一个job id；
- --`rdzv_backend`: rendezvous backend实现，默认支持c10d和etcd两种；rendezvous用于多个node之间的通信和协调；
- --`rdzv_endpoint`: rendezvous 地址，应该为一个node的host ip和port；




#### 迁移 launch -> torchrun

torch.distributed.launch -> torchrun

迁移方法

```sh
python -m torch.distributed.launch -> torchrun
# (1) 如果 从环境变量(LOCAL_RANK)中读取 local_rank 参数, 直接忽略
# 更改前
python -m torch.distributed.launch --use-env train_script.py
# 更改后
torchrun train_script.py
```


```py
# (2) 如果 从命令行(--local-rank)读取 local_rank 参数
# 更改前
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--local-rank", type=int)
args = parser.parse_args()
local_rank = args.local_rank
# 更改后
import os
local_rank = int(os.environ["LOCAL_RANK"])
```



```py
# local_rank参数应当从环境变量中读取，而不是通过参数传递。
### ------ BEFORE ------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--local_rank", type=int)
args = parser.parse_args()

local_rank = args.local_rank
### ------ NOW -------
import os
local_rank = int(os.environ["LOCAL_RANK"])

#运行脚本
torchrun train_script.py #除了--use_env参数，其他torch.distributed.launch所使用的参数均可使用，
			 #如nnodes、nproc_per_node
```


#### 初始化 init_process_group

`dist.init_process_group()` 是PyTorch中用于初始化分布式训练的函数之一。
- 作用： 设置并行训练环境，连接多个进程以进行数据和模型的分布式处理。

通过`init_process_group()`函数这个方法来进行初始化

其参数包括以下内容
- `backend`（必需参数）：指定分布式后端的类型，选项之一：
  - ‘tcp’：使用TCP协议进行通信。
  - ‘gloo’：使用Gloo库进行通信。
  - ‘mpi’：使用MPI（Message Passing Interface）进行通信。
  - ‘nccl’：使用NCCL库进行通信（适用于多GPU的分布式训练）。
  - ‘hccl’：使用HCCL库进行通信（适用于华为昇腾AI处理器的分布式训练）。
- `init_method`（可选参数）：指定用于初始化分布式环境的方法。它可以是以下选项之一：
  - ‘env://’：使用环境变量中指定的方法进行初始化。
  - ‘file:// ’：使用本地文件进行初始化。
  - ‘tcp://:’：使用TCP地址和端口进行初始化。
  - ‘gloo://:’：使用Gloo地址和端口进行初始化。
  - ‘mpi://:’：使用MPI地址和端口进行初始化。
- `rank`（可选参数）：指定当前进程的排名（从0开始）。
- `world_size`（可选参数）：指定总共使用的进程数。
- `timeout`（可选参数）：指定初始化的超时时间。
- `group_name`（可选参数）：指定用于连接的进程组名称。


### 多机多卡 DDP

概念理解
- `group`: `进程组`，通常DDP的各个进程都是在同一个进程组下 
- `world_size`: 总的进程数量（原则上，一个进程占用一个GPU） 
- `rank`：当前进程的序号，用于进程间通信，rank=0表示主机为master节点 
- `local_rank`：当前进程对应的GPU号

举个栗子 ： 
- 4台机器 (每台机器8张卡) 进行分布式训练。
- 通过 init_process_group() 对进程组进行初始化。 
- 初始化后 可以通过 get_world_size() 获取到 world size = 32。
- 在该例中为32， 即有32个进程，其编号为0-31 通过 get_rank() 函数可以进行获取 在每台机器上，local rank均为0-8， 这是 local rank 与 rank 的区别， local rank 会对应到实际的 GPU ID 上。


```py
########################## 	第1步	 ##########################
#初始化
rank = int(os.environ["RANK"])
local_rank = int(os.environ["LOCAL_RANK"])
torch.cuda.set_device(rank % torch.cuda.device_count())
dist.init_process_group(backend="nccl")
device = torch.device("cuda", local_rank)
########################## 	第2步	 ##########################
#模型定义
model = model.to(device)
model = DDP(model, device_ids=[local_rank], output_device=local_rank)

#数据集操作与DDP一致

#####运行
'''
exmaple: 2 node, 8 GPUs per node (16GPUs)
需要在两台机器上分别运行脚本
注意细节：node_rank master 为 0 
机器1
>>> python -m torch.distributed.launch \
    --nproc_per_node=8 \
    --nnodes=2 \
    --node_rank=0 \
    --master_addr="master的ip" \
    --master_port=xxxxx \
    YourScript.py
机器2
>>> python -m torch.distributed.launch \
    --nproc_per_node=8 \
    --nnodes=2 \
    --node_rank=1 \
    --master_addr="master的ip" \
    --master_port=xxxxx \
    YourScript.py

'''
```


### FSDP (DDP改进)

DistributedDataParallel (DDP) 训练

多机多卡方式中
- 每个 process/worker 都有模型的一个`副本`（Replica）
- 每个 process/worker 处理一个 batch 数据, 并行处理
- 最后用 `all-reduce` 操作对多个不同 process/worker 计算得到的**梯度**进行累加求和；
- 接着，再将**优化器状态**、**梯度**通过跨多个 process/worker 进行复制，使得每个 process/worker 上的模型参数都得到同步更新。

DDP 中，模型权重和优化器状态在所有工作线程中复制。 
- 核心能力还是训练**数据并行**（Data Parallel）
- DDP 没有实现对`模型参数`的**分片管理**，即`模型并行`（Model Parallel）


PyTorch 1.11 中发布 [FSDP](https://pytorch.org/docs/1.11/fsdp.html)
- FSDP 是一种数据并行性，可跨 DDP 等级分片`模型参数`、`优化器状态`和`梯度`。
- [Getting Started with Fully Sharded Data Parallel(FSDP)](https://pytorch.org/tutorials/intermediate/FSDP_tutorial.html)
- [PyTorch 分布式训练模式 FSDP 设计分析](http://shiyanjun.cn/archives/2292.html)

FSDP 实现了模型的**分片管理**能力，真正实现了`模型并行`。
- 将模型分片后，使用 FSDP 训练模型，每个 GPU 只保存模型的一个**分片**，这样能够使 **GPU 的内存占用比 DDP 方式小得多**，从而使分片的大模型和数据能够适配 GPU 容量，更有希望实现超大模型的分布式训练。
- 问题: process/worker 节点之间的通信开销一定程度增加，但是可在 PyTorch 内部有针对性地进行优化来降低通信代价，比如对通信、计算进行 overlapping 能够很好地降低由此带来的网络开销。


使用 FSDP 训练时，GPU 内存占用量比在所有工作线程上使用 DDP 进行训练时要小。
- 允许更大模型或批量大小适合设备，使一些非常大的模型的训练变得可行。
- 这是伴随着通信量增加的成本而来的。通过内部优化(例如重叠通信和计算)减少了通信开销。

[图解](https://pytorch.org/tutorials/_images/fsdp_workflow.png)
- ![](https://pytorch.org/tutorials/_images/fsdp_workflow.png)


#### FSDP 原理


FSDP 在不同阶段的基本处理过程，如下所示：

- 01 `初始化`阶段
  - 分片模型参数，每个 rank 只有自己的分片
- 02 `forward` 阶段
  - 运行 `all_gather`,收集所有 rank 上的模型参数分片，生成恢复得到模型参数，以保证满足当前 FSDP Unit 的计算需要
  - 运行 forward 计算过程
  - 丢掉所有被收集过的其它 rank 上的模型参数分片
- 03 `backward` 阶段
  - 运行 `all_gather`, 收集所有 rank 上的模型参数分片，恢复全部的模型参数，以保证满足当前 FSDP Unit 的计算需要
  - 运行 backward 计算过程
  - 运行 `reduce_scatter`, 在所有 rank 之间同步**梯度**
  - 丢掉所有从其它 rank 上收集过的模型参数分片


查看 FSDP’s 分片方法
- 将 DDP 梯度全归约分解为`归约分散`和`全聚集`。
- 向后传递过程中，FSDP 减少并分散梯度，确保每个等级都拥有梯度碎片。
- 在优化器步骤中更新参数的相应分片。
- 最后，后续前向传播中，执行全收集操作来收集并组合更新的参数分片


#### 分片原理

FSDP 默认的`分片策略`（Sharding Strategy）是对`模型参数`、`梯度`、`优化器状态`都进行分片处理，即 `Zero3` 分片策略
- 编程中可以使用 `ShardingStrategy.FULL_SHARD` 来指定。

对于 Zero2 分片策略，只对`梯度`、`优化器状态`进行分片处理
- 编程中可以使用 `ShardingStrategy.SHARD_GRAD_OP` 来指定。
- 如果配置使用 Zero2 分片策略，那么所有模型参数都会全量加载到每个 rank 对应的 GPU 内，即每个 GPU 持有一个模型的副本。
- forward 阶段和 backward 阶段模型参数都在 GPU 内而不会被 offload 到 CPU，这样就不需要频繁地在多个 GPU 之间传输模型参数分片信息，能够在一定程度上降低 FSDP 集群的通信开销。

FSDP 处理模型分片的总体流程
- 论文《PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel》
- ![](http://shiyanjun.cn/wp-content/uploads/2024/01/fsdp_algorithm_overview.png)

模型具有 6 个层，FSDP 将其分解为 3 个 FSDP Unit，分别为
- Unit0 = [layer0, layer3]
- Unit1 = [layer1, layer2]
- Unit2 = [layer4, layer5]

进行 forward 和 backward 计算之前需要从其它 rank 上收集对应的参数分片，从而保证计算是正确的。

以 Unit1 为例, 说明如何进行分片处理，该 FSDP Unit 包含了 layer1 和 layer2 两层。
- 进行 forward 计算之前，需要将这两层的参数对应于其它 rank 上的分片收集过来使 layer1 和 layer2 两层的参数是 Unsharded，即保证参数是完整的以便进行计算，然后在本地执行 forward 计算过程，完成 layer0 和 layer3 这两层的计算逻辑。当 forward 计算完成后，会释放掉刚刚从其它 rank 上收集到的参数分片，以降低内存空间的占用。每一轮 forward 计算，FSDP 一次只需要处理一个 Unit 的参数即可，而其它的 Unit 仍然保持其参数的分片状态。
- 对于 backward 计算的过程也是类似的，它会先计算 layer2，再计算 layer1，在开始计算 layer2 层之前，FSDP 会从其它 rank 上收集 layer2、layer1 层的分片参数，恢复得到这两层完整的参数后，Autograd 引擎会继续完成 layer2、layer1 这两层的计算，随后释放掉从其它 rank 上收集过来的参数分片。接着，FSDP 会进行 reduce-scatter 操作对梯度进行累加并分片。当 backward 计算结束后，每个 rank 都只保存了模型参数和梯度的分片部分。




#### FSDP 模型初始化

FSDP 模型初始化时，通过指定一个 device_id 参数来绑定到指定的 GPU 上
- 首先模型的 Module 会在 CPU 中初始化
- 然后加载到 GPU 内。

通过指定 device_id 能够保证当 GPU 无法容纳大的模型时，它能够 offload 到 CPU 中，而不至于出现 OOM 的问题。

创建 FSDP 模型
- 只要将模型（继承自 nn.Module） model，通过 FSDP 进行 wrap 即可
- 其中指定一些满足需要的配置选项

参数
- `auto_wrap_policy`: 自动将模型分片处理，包括对`模型参数`、`优化器状态`、`梯度`进行分片，每个分片都放到一个不同的 FSDP Unit 中
- 

```py
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP

model = DDP(model)

torch.cuda.set_device(local_rank)
model = FSDP(model,
        auto_wrap_policy=t5_auto_wrap_policy,
        mixed_precision=bfSixteen,
        device_id=torch.cuda.current_device())

model = FSDP(model,
    auto_wrap_policy=my_auto_wrap_policy,
    cpu_offload=CPUOffload(offload_params=True))
```

注意
- Transformer Encoder-Decoder 架构模型包含一些被 Encoder 和 Decoder 共享部分，比如 embedding 表，如果直接使用上面的 `auto_wrap_policy` 参数指定 Wrap Policy, 会使神经网络模型中这些共享的部分无法被共享
- 所以只能把**共享部分**移动到 FSDP Unit 外部去，以便 Encoder 和 Decoder 都能访问这部分。
- PyTorch 1.12 引入处理这种情况的特性，为 Transformer 注册一个 **共享 Layer** 实现类，使 FSDP 的分片计划（Sharding Plan）实现高效的通信处理。

```py
t5_auto_wrap_policy = functools.partial(
        transformer_auto_wrap_policy,
        transformer_layer_cls={
            T5Block, # T5 Transformer 层的实现类，封装了 MHSA 和 FFN 两层
        },
    )
torch.cuda.set_device(local_rank)
model = FSDP(model, fsdp_auto_wrap_policy=t5_auto_wrap_policy)
```


##  分布式训练高层封装

对 torch 几个流程进行一层封装【初始化、包装模型、优化器、数据加载】。

考虑几个因素
- 支持分布式训练**模式丰富**，如 CPU，单机单卡，单机多卡，多机多卡，FP16等
- **代码简单**，不需要改动大量代码， 即可进行分布式训练
- **接口丰富**，方便自定义。比如 能调用和访问底层分布式的一些变量如rank，worldsize，或实现或封装一些分布式函数，比如dist.gather/reduce等。

得到更加易用的框架：
- Accelerator
- Horovod

这两个都是非常易用的分布式框架。 还有一些其他的，比如 `pytorch-lightning`，`deepspeed`。

以bert情感分类为例子，介绍了如何使用原生DDP和上面2个框架来进行分布式训练
- 代码见：[torch-ddp-examples](https://github.com/ShomyLiu/torch-ddp-examples)

### Accelerator

由大名鼎鼎的 huggingface 发布的 Accelerator，专门适用于Pytorch 分布式训练框架：
- GitHub: [accelerate](https://github.com/huggingface/accelerate)
- 官网教程：[accelerate](https://huggingface.co/docs/accelerate)

将单进程代码改为多进程分布式：

```py
import accelerate
accelerator = accelerate.Accelerator()
device = accelerator.device #获取当前进程的设备
...
# 进行封装
model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)

#训练时 loss.backward() 换为：
accelerator.backward(loss)
```

使用CLI命令行方式运行，先使用 `accelerator config` 配置一次分布式训练参数，之后就使用 `acceleratoe launch` 运行。


除此之外，accelerator 还提供了一些很便利的接口，基本覆盖了分布式训练中需要用到的方法，比如：
- accelerator.`print`: 仅仅在主进程输出
- accelerator.`process_index`: 当前进程ID，没有使用rank命名，而是用的process_index来表示
- accelerator.`is_local_main_process`/`is_main_processs`: 是否local_rank 或则rank为0， 主进程
- accelerator.`wait_for_everyone`(): 类似 dist.barrier() , 等所有进程到达这一步。
- accelerator.`save`: 保存模型
- kwargs_handlers: 可以定义DDP初始化的一些参数，比如最常用的就是 find_unused_parameters，比如：

```py
import accelerate
from accelerate import DistributedDataParallelKwargs as DDPK
kwargs = DDPK(find_unused_parameters=True)
accelerator = accelerate.Accelerator(kwargs_handlers=[kwargs])
```

accelerator 基本已经满足使用 Pytorch 进行分布训练的需求,而且十分符合 huggingface 风格，把某个小项目做到最好用，类似的还有 transformers, tokenizers, datasets 等等。

不足
- accelerate 支持的 collective function 比较少，目前只有 all_gather。

Horovod
第二个常用的分布式库Horovod是一个通用的深度学习分布式训练框架，支持Tensorflow，Pytorch，MXNet，Keras等等，因此比Accelerator要更加重些，但是功能也会更加丰富，这里以Pytorch为例来简单介绍。多说一下，Horovod的安装相对复杂一些，需要针对具体的环境参考readme进行安装。

GitHub：https://github.com/horovod/horovod
官网：https://horovod.ai/
Horovod的使用也很简单，基本也是那几个流程：

```py
import horovod.torch as hvd
# 初始化
hvd.init()
# Samapler
# *此处num_replicas=hvd.size(), rank=hvd.rank()必须*
train_sampler = torch.utils.data.distributed.DistributedSampler(
    train_dataset, num_replicas=hvd.size(), rank=hvd.rank())

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=..., sampler=train_sampler)
# 优化器包装
optimizer = hvd.DistributedOptimizer(optimizer, named_parameters=model.named_parameters())
# 模型分发广播
hvd.broadcast_parameters(model.state_dict(), root_rank=0)
# 模型训练不需要修改
```

horovod 支持的运行方式非常多，最常用的就是 horovodrun ，比如单机四卡运行：

```sh
horovodrun -np 4 -H localhost:4 python3 train.py
```

horovod 相比 accelerate 功能更加丰富，支持的接口，函数，框架都要多， 比如: hvd.all_reduce, hvd.all_gather等等。



### Horovod

Horovod 是 Uber开源的跨平台的分布式训练工具，名字来自于俄国传统民间舞蹈，舞者手牵手围成一个圈跳舞，与Horovod设备之间的通信模式很像，有以下几个特点：
- 兼容TensorFlow、Keras和PyTorch机器学习框架。
- 使用Ring-AllReduce算法，对比Parameter Server算法，有着无需等待，负载均衡的优点。
- 实现简单，五分钟包教包会。

Horovod环境准备以及示例代码，可参考[上一篇](https://zhuanlan.zhihu.com/p/351693076)

Pytorch 1.x **多机多卡**计算模型没有采用主流的 Parameter Server 结构，而是直接用了Uber Horovod 的形式，即百度开源的 RingAllReduce 算法

Uber 的 Horovod 采用 RingAllReduce 计算方案，特点：网络单次通信量不随着 worker(GPU) 的增加而增加，是一个恒定值。

与 TreeAllReduce 不同，RingAllreduce 算法的每次通信成本是恒定的，与系统中 gpu 的数量无关，完全由系统中 gpu 之间最慢的连接决定。


## 新技术

### DisTrO

【2024-8-29】[DisTrO 让你家里的电脑也能训练超级大模型](https://mp.weixin.qq.com/s/wap7pZ3jUawNKG_3uMzojQ)

Nous Research 最近放出了一份重磅报告，介绍最新研究成果——DisTrO（Distributed Training Over-the-Internet）。
- [A PRELIMINARY REPORT ON DISTRO](https://venturebeat.com/wp-content/uploads/2024/08/A_Preliminary_Report_on_DisTrO.pdf)
- [A_Preliminary_Report_on_DisTrO.pdf](https://github.com/NousResearch/DisTrO/blob/main/A_Preliminary_Report_on_DisTrO.pdf)

有望让告别"只有大公司才能训练大模型"的时代，开启全民AI狂欢！

DisTrO 是一个**分布式优化器**家族，两个超级牛X的特点：
- 与架构无关：不管你用啥架构，它都能用。
- 与网络无关：网速慢？没关系，它照样能跑！

最厉害的是，DisTrO把GPU之间的通信需求减少了1000到10000倍！

在龟速网络上，用各种杂牌子的网络硬件，也能训练大型神经网络，而且收敛速度跟AdamW+All-Reduce一样快！

DisTrO 究竟有什么用呢？
- 提高LLM训练的抗风险能力：不再依赖单一实体的计算能力，训练过程更安全、更公平。
- 促进研究合作与创新：研究人员和机构可以更自由地合作，尝试新技术、新算法、新模型。
- 推动AI民主化：降低了训练大模型的门槛，让更多人有机会参与其中。

## 分布式训练库

详见站内专题: [分布式训练库](dist_tool)




# 结束