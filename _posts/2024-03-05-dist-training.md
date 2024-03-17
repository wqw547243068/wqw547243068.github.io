---
layout: post
title:  "分布式训练及推理加速"
date:   2024-03-05 19:25:00
categories: 大模型
tags: GPU Tensorflow Pytorch 并行计算 加速 分布式 tensorrt 推理加速 onnx zero lpu
excerpt: 分布式训练知识点
author: 鹤啸九天
mathjax: true
permalink: /dist
---

* content
{:toc}

# 分布式


- 【2021-10-13】[OpenAI 研究员最新博客：如何在多GPU上训练真正的大模型？](https://mp.weixin.qq.com/s?__biz=MzU5ODg0MTAwMw==&mid=2247504041&idx=1&sn=a6a8ceaf1cb091d7832351bcddae6ffb&chksm=febc936dc9cb1a7bbcdeef42f304107d7fe221e7999f2a1a508c6164267dc12dd12ee29ad0eb&mpshare=1&scene=23&srcid=1013pNjTo5fSHOxkjfW5JoFs)，[原文链接](lilianweng.github.io/lil-log/2021/09/24/train-large-neural-networks.html)
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

### 性能提速

在 pytorch1.7 + cuda10 + TeslaV100的环境下，使用ResNet34，batch_size=16, SGD对花草数据集训练的情况如下：
- 1块GPU需要9s一个epoch
- 2块GPU是5.5s
- 8块是2s。

问题
- 为什么运行时间不是9/8≈1.1s ? 
- 因为使用GPU数量越多，设备之间的通讯会越来越复杂，所以随着GPU数量的增加，训练速度的提升也是递减的。
- ![](https://pic1.zhimg.com/80/v2-aac042e783410385f791b8a0f70e6d6c_1440w.webp)

误差梯度如何在不同设备之间通信？
- 在每个GPU训练step结束后，将每块GPU的**损失梯度**求**平均**，而不是每块GPU各计算各的。

BN如何在不同设备之间同步？
- 假设batch_size=2，每个GPU计算的均值和方差都针对这两个样本而言的。
- 而BN的特性是：batch_size越大，均值和方差越接近与整个数据集的均值和方差，效果越好。
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


## 分布式模式

深度学习任务通用 GPU 进行模型训练。
- 因为 GPU 相对于 CPU 具有更多的**算术逻辑单元**（`ALU`），发挥并行计算的优势，特别适合**计算密集型**任务，更高效地完成深度学习模型的训练。
- 更多 GPU 知识见站内专题 [并行计算GPU](/gpu)

分析
- 虽然 GPU 并行计算能力优异，但**无法单独**工作，必须由 CPU 进行控制调用；
- 而且**显存**和**内存**之间的频繁数据拷贝，可能带来较大的性能开销。
- CPU 虽然计算能力不如 GPU，但可以**独立**工作，直接访问内存数据完成计算。

因此，想获得更好的训练性能，需要合理利用 GPU 和 CPU 的优势。

### CPU + GPU 工作模式

GPU 模式下的模型训练如图所示，分为4步：
- 第1步，将输入数据从系统内存拷贝到显存。
- 第2步，CPU 指示 GPU 处理数据。
- 第3步，GPU 并行地完成一系列的计算。
- 第4步，将计算结果从显存拷贝到内存。

![](https://aijishu.com/img/bVNCA)

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-06-29T06:30:26.521Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;ChEM8LvE2i4EmNkl0XTt\&quot; version=\&quot;21.5.1\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;g7JWtnAzlr1IYn_n-NA3\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;795\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-1\&quot; value=\&quot;CPU+GPU工作模式\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=0;fontSize=19;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;301\&quot; y=\&quot;60\&quot; width=\&quot;180\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-2\&quot; value=\&quot;内存\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=15;dashed=1;dashPattern=1 1;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;161\&quot; y=\&quot;130\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-3\&quot; value=\&quot;显存\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=15;dashed=1;dashPattern=1 1;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;161\&quot; y=\&quot;280\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-4\&quot; value=\&quot;CPU\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontStyle=0;fontSize=21;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;337.5\&quot; y=\&quot;120\&quot; width=\&quot;92.5\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-5\&quot; value=\&quot;GPU\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontStyle=0;fontSize=21;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;331\&quot; y=\&quot;270\&quot; width=\&quot;99\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-6\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=0.344;exitY=1.075;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0.333;entryY=0;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-2\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-3\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;221\&quot; y=\&quot;240\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;271\&quot; y=\&quot;190\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-7\&quot; value=\&quot;① 复制数据\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;121\&quot; y=\&quot;200\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-8\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=0.75;exitY=0;exitDx=0;exitDy=0;entryX=0.75;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-3\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-2\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;292\&quot; y=\&quot;183\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;291\&quot; y=\&quot;290\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-9\&quot; value=\&quot;④ 复制结果\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;231\&quot; y=\&quot;200\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-10\&quot; value=\&quot;② CPU指示GPU处理数据\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;325\&quot; y=\&quot;180\&quot; width=\&quot;145\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-11\&quot; value=\&quot;③ GPU并行处理数据\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;312.5\&quot; y=\&quot;240\&quot; width=\&quot;145\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-12\&quot; value=\&quot;\&quot; style=\&quot;endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;startArrow=block;startFill=0;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-2\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-4\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;292\&quot; y=\&quot;106.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;291\&quot; y=\&quot;213.5\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-13\&quot; value=\&quot;\&quot; style=\&quot;endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;startArrow=block;startFill=0;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-3\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-5\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;211\&quot; y=\&quot;160\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;348\&quot; y=\&quot;160\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-14\&quot; value=\&quot;显存\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=15;dashed=1;dashPattern=1 1;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;161\&quot; y=\&quot;350\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-15\&quot; value=\&quot;GPU\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontStyle=0;fontSize=21;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;331\&quot; y=\&quot;340\&quot; width=\&quot;99\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-16\&quot; value=\&quot;\&quot; style=\&quot;endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;startArrow=block;startFill=0;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-14\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-15\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;211\&quot; y=\&quot;230\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;348\&quot; y=\&quot;230\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-17\&quot; value=\&quot;显存\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=15;dashed=1;dashPattern=1 1;strokeWidth=3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;161\&quot; y=\&quot;420\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-18\&quot; value=\&quot;GPU\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontStyle=0;fontSize=21;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;331\&quot; y=\&quot;410\&quot; width=\&quot;99\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-19\&quot; value=\&quot;\&quot; style=\&quot;endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;startArrow=block;startFill=0;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-17\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-18\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;211\&quot; y=\&quot;300\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;348\&quot; y=\&quot;300\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-20\&quot; value=\&quot;Master\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontStyle=0\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;660\&quot; y=\&quot;285\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-21\&quot; value=\&quot;worker\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontStyle=0\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510\&quot; y=\&quot;210\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-22\&quot; value=\&quot;worker\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontStyle=0\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510\&quot; y=\&quot;285\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-23\&quot; value=\&quot;worker\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontStyle=0\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510\&quot; y=\&quot;355\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-24\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontStyle=0\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-21\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-20\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;630\&quot; y=\&quot;175\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;680\&quot; y=\&quot;125\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-25\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontStyle=0\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-22\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-20\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;590\&quot; y=\&quot;235\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;690\&quot; y=\&quot;310\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wnFd1TgQWBGGvaqbgYLa-26\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontStyle=0\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;wnFd1TgQWBGGvaqbgYLa-23\&quot; target=\&quot;wnFd1TgQWBGGvaqbgYLa-20\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;600\&quot; y=\&quot;245\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;700\&quot; y=\&quot;320\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

- 更多 GPU 知识见站内专题 [并行计算GPU](/gpu)

### 常见问题

模型训练的常见问题
- 问题一：GPU 显存爆满，资源不足
  - V100 为例，其显存最高也仅有 32G，甚至有些显存仅 12G 左右。因此当模型的参数量较大时，在 GPU 模式下模型可能无法训练起来。
  - 设置 CPU 模式进行模型训练，可以避免显存不足的问题，但是训练速度往往太慢。
  - 如何在单机训练中充分地利用 GPU 和 CPU 资源，让部分层在 CPU 执行，部分层在 GPU 执行呢？
- 问题二：频繁数据拷贝，训练效率低

## 分布式训练范式

并行技术：
- 数据并行（如：PyTorch DDP）
- 模型/张量并行（如：Megatron-LM（1D）、Colossal-AI（2D、2.5D、3D））
- 流水线并行（如：GPipe、PipeDream、PipeDream-2BW、PipeDream Flush（1F1B））
- **多维混合**并行（如：3D并行（数据并行、模型并行、流水线并行））
- **自动**并行（如：Alpa（自动算子内/算子间并行））
- 优化器相关并行（如：ZeRO（零冗余优化器，在执行的逻辑上是数据并行，但可以达到模型并行的显存优化效果）、PyTorch FSDP）


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

### 数据并行

数据并行性（Data parallelism (DP)）最简单的方法是：将相同的**模型权重**复制到多个worker中，并将一部分数据分配给每个worker以同时进行处理。
- 如果模型规模大于单个GPU的内存，Naive DP无法正常工作时。GeePS（Cui 等人，2016 年）之类的方法将暂时未使用的参数卸载回 CPU，以使用有限的 GPU 内存。数据交换传输在后端进行，且不干扰训练计算。
 
在每个小批量结束时，workers需要同步梯度或权重，以替换旧参数。常见有两种主要的同步方法，它们都有明确的优缺点：
- 1）大容量**同步**并行（ Bulk synchronous parallels (BSP)）：workers在每个小批量结束时同步数据。这种方法可以防止模型权重过时，同时获得良好的学习效率，但每台机器都必须停止并**等待**其他机器发送梯度。
- 2）**异步**并行（Asynchronous parallel (ASP)）：每个GPU工作进程异步处理数据，无需等待或暂停。然而，这种方法很容易导致网络使用陈旧的权重参数，从而**降低**统计学习效率。即使它增加了计算时间，也可能不会加快收敛的训练时间。
 
中间的某个地方是在每次x迭代时，全局同步梯度（x＞1）。自Pytorch v1.5版（Li等人，2021年）以来，该特征在平行分布数据（DDP）中被称为“梯度累积”。Bucket 梯度计算方法避免了梯度的立即AllReduce，而是将多个梯度变化值存储到一个AllReduce中以提高吞吐量，可以基于计算图进行计算和通信调度优化。

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


### 流水线并行（综合模型+数据）

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

### 张量并行（水平分割）

模型并行和流水线并行都将一个模型垂直分割，可以将一个张量操作的计算水平分割到多个设备上，称为**张量并行**（tensor parallelism，TP）。
- 张量并行将张量沿特定维度分成 N 块，每个设备只持有整个张量的 1/N，同时不影响计算图的正确性。
- 这需要额外的通信来确保结果的正确性。
- ![](https://mmbiz.qpic.cn/mmbiz_png/J0mLianhFicBHEDwE5nPHZKaicqsXBVgES53FR1KDRnTBHAKwRtd9rEo3TOxgrKA5ZaqBVYZ3QIKGwU2OTW7AklIQ/640?wx_fmt=png&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1)

以当下比较流行的transformer为例，transformer模型主要由多层MLP和自我注意块组成。Megatron-LM（Shoeybi et al.2020）等人采用了一种简单的方法来并行多层计算MLP和自我注意。变压器中的MLP层包含GEMM（通用矩阵乘法）和非线性GeLU传输，按列拆分权重矩阵A

典型的张量并行实现：
- Megatron-LM（1D）
- Colossal-AI（2D、2.5D、3D）

### 异构系统并行

- 与 GPU 相比，CPU 的内存要大得多。典型服务器上，CPU 可以轻松拥有几百GB甚至上TB的内存，而每张 GPU 卡通常只有 48 或 80 GB的内存。为什么 CPU 内存没有被用于分布式训练？
- 依靠 CPU 甚至是 NVMe 磁盘来训练大型模型。主要的想法是，在不使用张量时，将其卸载回 CPU 内存或 NVMe 磁盘。通过使用异构系统架构，有可能在一台机器上容纳一个巨大的模型。

### 多维混合并行

- 多维混合并行指将数据并行、模型并行和流水线并行结合起来进行分布式训练。
- 超大规模模型的预训练和全参数微调时，都需要用到多维混合并行。


## 分布式训练库

### 常见框架

常见的分布式训练框架：
- 第一类：深度学习框架**自带**分布式训练功能。如：TensorFlow、PyTorch、MindSpore、Oneflow、PaddlePaddle等。
- 第二类：基于现有的深度学习框架（如：PyTorch、Flax）进行**扩展和优化**，从而进行分布式训练。
  - 如：`Megatron-LM`（张量并行）、`DeepSpeed`（Zero-DP）、`Colossal-AI`（高维模型并行，如2D、2.5D、3D）、`Alpa`（自动并行）等

### LLM 复现选择

如何选择分布式训练框架？ [参考](https://mp.weixin.qq.com/s/7wtwsNhf27YzALnSFXTmkA)
- 训练**成本**：不同训练工具，训练同样大模型，成本不一样。对于大模型，训练一次动辄上百万/千万美元的费用。合适的成本始终是正确的选择。
- 训练**类型**：是否支持数据并行、张量并行、流水线并行、多维混合并行、自动并行等
- **效率**：将普通模型训练代码变为分布式训练所需编写代码的行数，希望越少越好。
- **灵活性**：选择的框架是否可以跨不同平台使用？

目前训练超大规模语言模型主要有两条技术路线：
- TPU + XLA + TensorFlow/JAX ：由Google主导，由于TPU和自家云平台GCP深度绑定
- GPU + PyTorch + Megatron-LM + DeepSpeed ：由 NVIDIA、Meta、MicroSoft 大厂加持，社区氛围活跃，也更受到大家欢迎。

### DeepSpeed -- 微软


DeepSpeed 是 Microsoft基于PyTorch研发的开源深度学习优化库。
- 目的: 降低大模型训练的门槛，提升大模型的训练的效率，帮助开发者更有效率地管理及优化大模型的训练、部署任务。

#### DeepSpeed 介绍

DeepSpeed支持多种训练优化策略。包括：
- 3D并行：数据并行、模型并行、流水线并行以及三者的混合使用
- Zero Redundancy Optimizer（零冗余优化器）：ZeRO-0、ZeRO-1、ZeRO-2、ZeRO-3、ZeRO-Infinity
- ZeRO-Offload ：卸载，支持将数据、梯度、优化器状态等下沉到 CPU 和 NVMe
- 自定义混合精度训练训练：动态精度缩放（Dynamic Loss Scaling）和混合精度优化器（Mixed Precision Optimizer） 

此外, DeepSpeed 还提供许多大模型相关的工具，如分布式训练管理、内存优化和模型压缩等，以帮助开发者更好地管理和优化大规模深度学习训练任务。DeepSpeed在自然语言处理（NLP）和多模态等领域有许多成功的应用案例。DeepSpeed可以极大提升大模型的训练速度、降低训练门槛以及训练成本，并因具备完整健康的社区生态，提升大模型的可用性。让中小公司、独立研究人员解锁了训练具有超过1000亿个参数的模型的能力。
- 参考：[LAM](https://zhuanlan.zhihu.com/p/685472786)

- [DeepSpeed](https://www.deepspeed.ai/) is a deep learning optimization library that makes distributed training and inference easy, efficient, and effective.
- DeepSpeed trained the world’s most powerful language models (`MT-530B`, `BLOOM`)
- 微软的 `DeepSpeed` 模型并行等内核取自 `Megatron` ，且 DeepSpeed 主打在数据并行下如何以更少的机器去跑更大的模型 （ ZeRO 、 ZeRO-Offload 等都是用梯度切片、计算、内存/硬盘换入换出来省显存）

目前开源的 模型库 主要是 NVIDIA 的 `Megatron-LM` 和微软的 [DeepSpeed](https://www.deepspeed.ai/)。

`Megatron` 和 `DeepSpeed` 都是基于 `PyTorch` ，分别由 `NVIDIA` 和`微软`经过深度定制开发，专门为支持 PyTorch 分布式训练 GPT 而设计的。

`NVIDIA` 的 `Megatron` 和 微软的 `DeepSpeed`：

DeepSpeed 本质上是一种“节省显存”的数据并行，即：<span style='color:blue'>数据并行的优化版</span>。
- DeepSpeed 假设了单层参数量可以在单张显卡上放得下，如果不满足这个假设，那么仍然需要使用模型并行，而且 DeepSpeed 的模型并行是通过调用 Megatron 来实现的。
- 根据 NVIDIA 最新的那篇[论文](https://arxiv.org/abs/2104.04473)，`Megatron` 在大规模训练的效率是超过 `DeepSpeed` 不少的。
- DeepSpeed 的论文一直强调：可以用更少机器训练更大的模型，但没有突出过在效率上的优势。
- DeepSpeed 后来又出了一篇论文：[ZeRO-Infinity](https://arxiv.org/abs/2104.07857)，当单层参数量在单张显卡上放不下的时候，它通过对这一层算子切片，一片一片来执行，使得单卡也能跑起来一个巨大的层，可以理解成一种 “时间”轴上展开的模型并行。

#### DeepSpeed 框架

DeepSpeed 主要分成以下四个板块，包括：Training、Inference、Compression、Science
- ![](https://pic1.zhimg.com/v2-a9ac939ec325cf859c282511ddd90f2c_b.jpg)

DeepSpedd-Training 提供一套端到端大模型训练框架，核心板块。
- 因为DeepSpeed 基于PyTorch搭建，且兼容 Transformers，新用户学习成本较低，可快速上手，快速实现自有工程的搭建。
- 并且DeepSpeed在DeepSpeedExamples项目中提供了`DeepSpeed-chat`模块 ，完美复刻`InstructGPT`论文中RLHF训练方式，可以一键式完成大模型的SFT、Reward Model Finetuning、RLHF
- ![](https://pic3.zhimg.com/v2-28ace0f70b557dc6b6394171daeab912_b.jpg)

[DeepSpeedExamples](https://github.com/microsoft/DeepSpeedExamples) 也提供 bert、gan、Stable Diffusion 微调案列，更方便的学习应用DeepSpeed。

DeepSpeed发展速度非常快，一些新的大模型热点技术都实现快速支持 。目前DeepSpeed可以支持MoE模型架构训练，并且在超长上下文模型训练问题上也提供了优化方案。


#### DeepSpeed-Trianing

DeepSpeed-Trianing 介绍
- 通信策略优化
  - 为更好支持在GPU、CPU上的分布式训练以及GPU、CPU的混合训练。DeepSpeed支持 mpi、gloo 和 nccl 等通信策略
  - Open MPI 可整合高性能计算社区中所有专家，技术和资源，以构建可用的最佳MPI库。
  - Gloo: facebook开源的一套集体通信库，他提供了对机器学习中有用的一些集合通信算法如：barrier, broadcast, allreduce
  - nccl: NVIDIA集体通信库（NCCL）实现了针对NVIDIA GPU性能优化的多GPU和多节点集体通信原语。NCCL提供了诸如all-gather, all-reduce, broadcast, reduce, reduce-scatter等实现，这些实现优化后可以通过PCIe和NVLink等高速互联，从而实现高带宽和低延迟。 因为NCCL则是NVIDIA基于自身硬件定制的，能做到更有针对性且更方便优化，故在英伟达硬件上，NCCL的效果往往比其它的通信库更好。
  - 选择策略: 
    - 如果在 CPU 集群上分布式训练，选择 mpi 和 gloo；
    - 如果在 GPU 上进行分布式训练，可以选择 nccl。

#### DeepSpeed 用法

DeepSpeed 用法
- 【2023-5-19】huggingface的[DeepSpeed文档](https://huggingface.co/docs/transformers/main/main_classes/deepspeed)的笔记：[DeepSpeed 入门教程](https://zhuanlan.zhihu.com/p/630734624?utm_psn=1751727518502281216)

DeepSpeed目前支持的功能
- Optimizer state partitioning (ZeRO stage 1)
- Gradient partitioning (ZeRO stage 2)
- Parameter partitioning (ZeRO stage 3)
- Custom mixed precision training handling
- A range of fast CUDA-extension-based optimizers
- ZeRO-Offload to CPU and NVMe


```sh
​# ======== 单卡 =========
# 单卡 使用方法
deepspeed --num_gpus=1 examples/pytorch/translation/run_translation.py ...
# 单卡，并指定对应的GPU
deepspeed --include localhost:1 examples/pytorch/translation/run_translation.py ...
​# ======== 多卡 =========
# 多GPU 使用方法1
torch.distributed.run --nproc_per_node=2 your_program.py <normal cl args> --deepspeed ds_config.json
# 多GPU 使用方法2
deepspeed --num_gpus=2 your_program.py <normal cl args> --deepspeed ds_config.json
​​# ======== 多机多卡 =========
# 多节点多卡 方法1，需要在多个节点上手动启动
python -m torch.distributed.run --nproc_per_node=8 --nnode=2 --node_rank=0 --master_addr=hostname1 --master_port=9901 your_program.py <normal cl args> --deepspeed ds_config.json
# 多节点多卡 方法2，需要创建一个 hostfile 文件，只需在一个节点上启动
hostname1 slots=8
hostname2 slots=8
# 然后运行
deepspeed --num_gpus 8 --num_nodes 2 --hostfile hostfile --master_addr hostname1 --master_port=9901 your_program.py <normal cl args> --deepspeed ds_config.json
​
# 参数传递
TrainingArguments(..., deepspeed="/path/to/ds_config.json")
# or
ds_config_dict = dict(scheduler=scheduler_params, optimizer=optimizer_params)
TrainingArguments(..., deepspeed=ds_config_dict)

# 在SLURM上运行，略，参见原始文档
# 在jupyter中运行，略，参见原始文档
```

为什么单卡也可以使用deepspeed？
- 使用 ZeRO-offload，将部分数据 offload 到 CPU，降低对显存的需求
- 提供了对显存的管理，减少显存中的碎片


##### ZeRO-2 配置

```json
{
    "fp16": {
        "enabled": "auto",
        "loss_scale": 0,
        "loss_scale_window": 1000,
        "initial_scale_power": 16,
        "hysteresis": 2,
        "min_loss_scale": 1
    },

    "optimizer": {
        "type": "AdamW",
        "params": {
            "lr": "auto",
            "betas": "auto",
            "eps": "auto",
            "weight_decay": "auto"
        }
    },

    "scheduler": {
        "type": "WarmupLR",
        "params": {
            "warmup_min_lr": "auto",
            "warmup_max_lr": "auto",
            "warmup_num_steps": "auto"
        }
    },

    "zero_optimization": {
        "stage": 2,
        "offload_optimizer": {
            "device": "cpu",
            "pin_memory": true
        },
        "allgather_partitions": true,
        "allgather_bucket_size": 2e8,
        "overlap_comm": true,
        "reduce_scatter": true,
        "reduce_bucket_size": 2e8,
        "contiguous_gradients": true
    },

    "gradient_accumulation_steps": "auto",
    "gradient_clipping": "auto",
    "steps_per_print": 2000,
    "train_batch_size": "auto",
    "train_micro_batch_size_per_gpu": "auto",
    "wall_clock_breakdown": false
}
```

说明
- overlap_comm：控制是否使用通信与计算的重叠。
  - 当设置为True时，DeepSpeed将在梯度计算时尝试并行执行梯度通信。可以有效地减少通信时间，从而加速整个训练过程。
- allgather_bucket_size：用于控制Allgather操作的分桶大小。
  - Allgather操作是指在分布式训练中，每个进程收集其他所有进程的张量，并将这些张量按顺序拼接起来。通过将张量划分为较小的桶（buckets），可以在通信过程中更高效地传输数据。
  - allgather_bucket_size值越大，每个桶的大小越大，通信操作可能会变得更快，但也需要更多的内存来存储中间结果。合适的桶大小要根据实际情况调整。
- reduce_bucket_size：类似于allgather_bucket_size，用于控制Allreduce操作的分桶大小。
  - Allreduce操作是将所有进程的某个张量进行**规约**（例如求和），并将结果广播回所有进程。通过将张量划分为较小的桶，可以更高效地传输数据。
  - reduce_bucket_size值越大，每个桶的大小越大，通信操作可能会变得更快，但同时也需要更多的内存来存储中间结果。合适的桶大小需要根据实际情况进行调整。
- overlap_comm使用的是allgather_bucket_size和reduce_bucket_size值的4.5倍。
  - 如果设置为5e8，需要9GB显存（5e8 x 2Bytes x 2 x 4.5）。
  - 如果内存大小是8GB或更小，需要将这些参数减少到约2e8，从而避免OOM，这需要3.6GB显存。
  - 如果在大容量GPU上也出现OOM，也需要做同样的调整。
- 在deepspeed==0.4.4中新增了 round_robin_gradients 选项，可以并行化CPU的offload。
  - 当梯度累积的步数增加，或者GPU数量增加时，会有更好的性能优势。


##### ZeRO-3 配置

配置示例

```json
{
    "fp16": {
        "enabled": "auto",
        "loss_scale": 0,
        "loss_scale_window": 1000,
        "initial_scale_power": 16,
        "hysteresis": 2,
        "min_loss_scale": 1
    },

    "optimizer": {
        "type": "AdamW",
        "params": {
            "lr": "auto",
            "betas": "auto",
            "eps": "auto",
            "weight_decay": "auto"
        }
    },

    "scheduler": {
        "type": "WarmupLR",
        "params": {
            "warmup_min_lr": "auto",
            "warmup_max_lr": "auto",
            "warmup_num_steps": "auto"
        }
    },

    "zero_optimization": {
        "stage": 3,
        "offload_optimizer": {
            "device": "cpu",
            "pin_memory": true
        },
        "offload_param": {
            "device": "cpu",
            "pin_memory": true
        },
        "overlap_comm": true,
        "contiguous_gradients": true,
        "sub_group_size": 1e9,
        "reduce_bucket_size": "auto",
        "stage3_prefetch_bucket_size": "auto",
        "stage3_param_persistence_threshold": "auto",
        "stage3_max_live_parameters": 1e9,
        "stage3_max_reuse_distance": 1e9,
        "stage3_gather_16bit_weights_on_model_save": true
    },

    "gradient_accumulation_steps": "auto",
    "gradient_clipping": "auto",
    "steps_per_print": 2000,
    "train_batch_size": "auto",
    "train_micro_batch_size_per_gpu": "auto",
    "wall_clock_breakdown": false
}
```

说明
- stage3_max_live_parameters 保留在 GPU 上的完整参数数量的上限。
- stage3_max_reuse_distance 将来何时再次使用参数的指标，从而决定是丢弃参数还是保留参数。
  - 如果一个参数在不久的将来要再次使用（小于 stage3_max_reuse_distance），可以保留以减少通信开销。 使用activation checkpointing时，这一点非常有用。
  - 如果遇到 OOM，可以减少 stage3_max_live_parameters 和 stage3_max_reuse_distance。 除非正在使用activation checkpointing，否则它们对性能的影响应该很小。 1e9 会消耗 ~2GB。 内存由 stage3_max_live_parameters 和 stage3_max_reuse_distance 共享，所以不是相加的，一共 2GB。
- stage3_gather_16bit_weights_on_model_save 在保存模型时启用模型 fp16 权重合并。 
  - 对大型模型和多GPU，在内存和速度方面都是一项昂贵的操作。 如果打算恢复训练，目前需要使用它。 未来的更新将消除此限制。
- sub_group_size 控制在optimizer steps中更新参数的粒度。 
  - 参数被分组到 sub_group_size 的桶中，每个桶一次更新一个。 
  - 当与 ZeRO-Infinity 中的 NVMe offload一起使用时，sub_group_size 控制模型状态在optimizer steps期间从 NVMe 移入和移出 CPU 内存的粒度。 防止超大模型耗尽 CPU 内存。不使用NVMe offload时，使其保持默认值。出现OOM时，减小sub_group_size。当优化器迭代很慢时，可以增大sub_group_size 。
- ZeRO-3 中未使用 allgather_partitions、allgather_bucket_size 和 reduce_scatter 配置参数



ZeRO-stage-0

stage 0会禁用所有的分片，然后把DeepSpeed当作时DDP来使用。

```json
{
    "zero_optimization": {
        "stage": 0
    }
}
```

ZeRO-stage-1

只对优化器参数进行分片，可以加速一丢丢

```json
{
    "zero_optimization": {
        "stage": 1
    }
}
```

NVMe Support
- ZeRO-Infinity 需要使用 ZeRO-3
- ZeRO-3 会比 ZeRO-2 慢很多。使用以下策略，可以使得ZeRO-3 的速度更接近ZeRO-2
- 将stage3_param_persistence_threshold参数设置的很大，比如6 * hidden_size * hidden_size
- 将offload_params参数关闭（可以极大改善性能）

如何选择不同的Zero stage和offload
- 从左到右，越来越慢
  - Stage 0 (DDP) > Stage 1 > Stage 2 > Stage 2 + offload > Stage 3 > Stage 3 + offloads
- 从左到右，所需GPU显存越来越少
  - Stage 0 (DDP) < Stage 1 < Stage 2 < Stage 2 + offload < Stage 3 < Stage 3 + offloads

##### 调参步骤

将batch_size设置为1，通过梯度累积实现任意的有效batch_size
- 如果OOM则，设置--gradient_checkpointing 1 (HF Trainer)，或者 model.gradient_checkpointing_enable()
- 如果OOM则，尝试ZeRO stage 2
- 如果OOM则，尝试ZeRO stage 2 + offload_optimizer
- 如果OOM则，尝试ZeRO stage 3
- 如果OOM则，尝试offload_param到CPU
- 如果OOM则，尝试offload_optimizer到CPU
- 如果OOM则，尝试降低一些默认参数。比如使用generate时，减小beam search的搜索范围
- 如果OOM则，使用混合精度训练，在Ampere的GPU上使用bf16，在旧版本GPU上使用fp16
- 如果仍然OOM，则使用ZeRO-Infinity ，使用offload_param和offload_optimizer到NVME
- 一旦使用batch_size=1时，没有导致OOM，测量此时的有效吞吐量，然后尽可能增大batch_size
- 开始优化参数，可以关闭offload参数，或者降低ZeRO stage，然后调整batch_size，然后继续测量吞吐量，直到性能比较满意（调参可以增加66%的性能）

一些其他建议
- 如果训模型from scratch，hidden size最好可以被16整除
- batch size最好可以被2整除

##### 优化器和调度器

当不使用offload_optimizer 时，可以按照下表，混合使用HF和DS的优化器和迭代器，除了HF Scheduler和DS Optimizer这一种情况。

| Combos	| HF Scheduler	| DS Scheduler |
| ---	| ---	| --- |
| HF Optimizer |	Yes	| Yes |
| DS Optimizer |	No	| Yes |

**优化器**
- 启用 offload_optimizer 时可以使用非 DeepSpeed 的优化器，只要它同时具有 CPU 和 GPU 的实现（LAMB 除外）。
- DeepSpeed 的主要优化器是 Adam、AdamW、OneBitAdam 和 Lamb。 这些已通过 ZeRO 进行了彻底测试，建议使用。
- 如果没有在配置文件中配置优化器参数，Trainer 将自动将其设置为 AdamW，并将使用命令行参数的默认值：--learning_rate、--adam_beta1、--adam_beta2、 --adam_epsilon 和 --weight_decay。
- 与 AdamW 类似，可以配置其他官方支持的优化器。 请记住，它们可能具有不同的配置值。 例如 对于 Adam，需要将 weight_decay 设置为 0.01 左右。
- 此外，offload在与 Deepspeed 的 CPU Adam 优化器一起使用时效果最佳。 如果想对offload使用不同的优化器，deepspeed==0.8.3 以后的版本，还需要添加：

```json
{
    "zero_force_ds_cpu_optimizer": false
}
```

**调度器**

- DeepSpeed 支持 LRRangeTest、OneCycle、WarmupLR 和 WarmupDecayLR 学习率调度器。
- Transformers和DeepSpeed中调度器的overlap
- WarmupLR 使用 --lr_scheduler_type constant_with_warmup
- WarmupDecayLR 使用 --lr_scheduler_type linear


##### 训练精度

由于 fp16 混合精度大大减少了内存需求，并可以实现更快的速度，因此只有此训练模式表现不佳时，才考虑不使用**混合精度训练**。 

通常，当模型未在 fp16 混合精度中进行预训练时，会出现这种情况（例如，使用 bf16 预训练的模型）。 这样的模型可能会溢出，导致loss为NaN。 如果是这种情况，使用完整的 fp32 模式。
- 如果是基于 Ampere 架构的 GPU，pytorch 1.7 及更高版本将自动切换为使用更高效的 tf32 格式进行某些操作，但结果仍将采用 fp32。
- 使用 Trainer，可以使用 --tf32 启用它，或使用 --tf32 0 或 --no_tf32 禁用它。 PyTorch 默认值是使用tf32。

自动混合精度

- fp16
  - 可用 pytorch-like AMP 方式或者 apex-like 方式
  - 使用 --fp16--fp16_backend amp 或 --fp16_full_eval 命令行参数时启用此模式
- bf16
  - 使用--bf16 or --bf16_full_eval 命令行参数时启用此模式

NCCL
- 通讯会采用一种单独的数据类型
- 默认情况下，半精度训练使用 fp16 作为reduction操作的默认值
- 可以增加一个小的开销并确保reduction将使用 fp32 作为累积数据类型

```json
{
    "communication_data_type": "fp32"
}
```

apex
- Apex 是一个在 PyTorch 深度学习框架下用于加速训练和提高性能的库。Apex 提供了混合精度训练、分布式训练和内存优化等功能，帮助用户提高训练速度、扩展训练规模以及优化 GPU 资源利用率。
- 使用--fp16、 --fp16_backend apex、 --fp16_opt_level 01 命令行参数时启用此模式

```json
"amp": {
     "enabled": "auto",
     "opt_level": "auto"
}
```

##### 获取模型参数

deepspeed会在优化器参数中存储模型的主参数，存储在global_step*/*optim_states.pt 文件中，数据类型为fp32。因此，想要从checkpoint中恢复训练，则保持默认即可
- 如果模型是在ZeRO-2模式下保存的，模型参数会以fp16的形式存储在pytorch_model.bin中
- 如果模型是在ZeRO-3模式下保存的，需要如下所示设置参数，否则pytorch_model.bin将不会被创建

```json
{
  "zero_optimization": {
         "stage3_gather_16bit_weights_on_model_save": true
    }
}
```

- 在线fp32权重恢复（需要很多的RAM）略
- 离线获取fp32权重

```sh
python zero_to_fp32.py . pytorch_model.bin
```


##### ZeRO inference

只有ZeRO-3是有意义的，因为可以将参数分片：

```sh
deepspeed --num_gpus=2 your_program.py <normal cl args> --do_eval --deepspeed ds_config.json
```

估算需要的显存
- 可以通过下面的代码，先估算不同配置需要的显存数量，从而决定开始尝试的ZeRO stage。

```sh
python -c 'from transformers import AutoModel; \
from deepspeed.runtime.zero.stage3 import estimate_zero3_model_states_mem_needs_all_live; \
model = AutoModel.from_pretrained("bigscience/T0_3B"); \
estimate_zero3_model_states_mem_needs_all_live(model, num_gpus_per_node=2, num_nodes=1)'
[...]
Estimated memory needed for params, optim states and gradients for a:
HW: Setup with 1 node, 2 GPUs per node.
SW: Model with 2783M total params, 65M largest layer params.
  per CPU  |  per GPU |   Options
 70.00GB |   0.25GB | offload_param=cpu , offload_optimizer=cpu , zero_init=1
```

其它问题
- 启动时，进程被杀死，并且没有打印出traceback：CPU显存不够
- loss是NaN：训练时用的是bf16，使用时是fp16。常常发生于google在TPU上train的模型，如T5。此时需要使用fp32或者bf16。

### Megatron-LM -- NVIDIA

[Megatron](https://github.com/NVIDIA/Megatron-LM) is a large, powerful transformer developed by the Applied Deep Learning Research team at NVIDIA. This repository is for ongoing research on training large transformer language models at scale. We developed efficient, model-parallel (tensor, sequence, and pipeline), and multi-node pre-training of transformer based models such as GPT, BERT, and T5 using mixed precision.

#### Megatron-LM 介绍

Megatron 是超大规模Transformer模型的**分布式训练**解决方案。字节、阿里和快手等公司都将其作为大模型训练框架。

Megatron 核心能力:
- 多种并行策略组合: Data Parallel、 Tensor Parallel、Pipeline Parallel、Sequence Parallel
- Distributed-optimiezer: 相当于是deepspeed zero1的策略
- 高性能算子：Flash Attention
- Activation checkpoint
- 混合精度
- Gradient accumulation
- MoE

### Megatron-DeepSpeed

`Megatron-DeepSpeed` 结合了两种主要技术：
- `DeepSpeed` 是微软开发的深度学习**优化库**，分布式训练变得简单、高效和有效。
- `Megatron-LM` 是由 `NVIDIA` 的应用深度学习研究团队开发的大型、强大的 **Transformer 模型框架**。

DeepSpeed 团队通过将 `DeepSpeed` 库中的 `ZeRO 分片`（ZeRO sharding）和`管道并行`（pipeline parallelism）与 `Megatron-LM` 中的`张量并行`（Tensor Parallelism）相结合，开发了一种基于 **3D 并行**的实现。

`Megatron-DeepSpeed` 实施 3D 并行以可以让大型模型以非常有效的方式进行训练。
- `DataParallel` (DP) - 相同的初始化模型被复制多次，并且每次都被馈送 minibatch 的一部分。处理是并行完成的，所有设置在每个训练步骤结束时进行同步。
- `TensorParallel` (TP) - 每个张量都被分成多个块，因此不是让整个张量驻留在单个 GPU 上，而是张量的每个分片都驻留在其指定的 GPU 上。在处理过程中，每个分片在不同的 GPU 上分别并行处理，最终结果在步骤结束时同步。这也被称作横向并行。
- `PipelineParallel` (PP) - 模型在多个 GPU 上垂直（层级）拆分，因此只有模型的一个或多个层放置在单个 GPU 上。每个 GPU 并行处理管道的不同阶段，并处理一小部分批处理。
- `零冗余优化器` (ZeRO) - 也执行与 TP 有点类似的张量分片，除了整个张量会及时重建以进行前向或反向计算，因此不需要修改模型。它还支持各种卸载技术以补偿有限的 GPU 内存。

各个技术细节参考：[大型语言模型(LLM)训练指南](https://zhuanlan.zhihu.com/p/611325149)


【2023-8-28】[LLaMA Efficient Tuning](https://github.com/hiyouga/LLaMA-Efficient-Tuning/blob/main/README_zh.md)

| 方法 | 全参数训练 | 部分参数训练 | LoRA | QLoRA | 
| --- | --- |  --- | --- | --- | 
| 预训练 | ✅ |  ✅ | ✅ | ✅ | 
| 指令监督微调 | ✅ | ✅ | ✅ | ✅  |
| 奖励模型训练 | | | ✅ | ✅ |
| PPO 训练 | | | ✅ | ✅ | 
| DPO 训练 | ✅ | | ✅ | ✅ |


### trl


【2024-3-13】[TRL - Transformer Reinforcement Learning](https://huggingface.co/docs/trl/index)

huggingface 推出的全栈库，包含一整套工具，用于使用强化学习 (Reinforcement Learning) 训练 transformer 语言模型。
- 从**监督调优** (Supervised Fine-tuning step, SFT)，到训练**奖励模型** (Reward Modeling)，再到**近端策略优化** (Proximal Policy Optimization)，全面覆盖
- ![](https://huggingface.co/datasets/trl-internal-testing/example-images/resolve/main/images/TRL-readme.png)
- [TRL](https://github.com/huggingface/trl) 库已经与 🤗 transformers 集成，直接使用！
- 👉 文档[地址](https://hf.co/docs/trl/)
- ![](https://picx.zhimg.com/70/v2-1c818186d30b9afff9af2341b1eddc6f_1440w.avis?source=172ae18b&biz_tag=Post)

API 文档里功能:
- Model Class: 公开模型各自用途
- SFTTrainer: SFTTrainer 实现模型监督调优
- RewardTrainer: RewardTrainer 训练奖励模型
- PPOTrainer: PPO 算法对经过监督调优的模型再调优
- Best-of-N Samppling: 将“拔萃法”作为从模型的预测中采样的替代方法
- DPOTrainer: 用 DPOTrainer 完成直接偏好优化

文档中给出了几个例子:
- Sentiment Tuning: 调优模型以生成更积极的电影内容
- Training with PEFT: 执行由 PEFT 适配器优化内存效率的 RLHF 训练
- Detoxifying LLMs: 通过 RLHF 为模型解毒，使其更符合人类的价值观
- StackLlama: 在 Stack exchange 数据集上实现端到端 RLHF 训练一个 Llama 模型
- Multi-Adapter Training: 使用单一模型和多适配器实现优化内存效率的端到端训练


#### Trl 实践

【2023-6-30】[使用TRL强化学习PPO控制文本的生成](https://zhuanlan.zhihu.com/p/616788557)

步骤
1. 初始化 GPT2 对话模型, 即LLM模型。Huggface中的这个中文对话模型 
  - [gpt2-dialogbot-base-chinese](https://huggingface.co/shibing624/gpt2-dialogbot-base-chinese)
2. 初始化一个情感分类模型即RM模型。这里笔者使用的是Huggface中的这个情感分类模型
  - 样本情感极性越正向，模型输出的得分越大。
  - [c2-roberta-base-finetuned-dianping-chinese](https://huggingface.co/liam168/c2-roberta-base-finetuned-dianping-chinese)
3. 通过PPO强化学习算法，利用情感分类模型评估对话模型的输出，对GPT2对话模型进行优化，让GPT2对话模型的输出的结果在情感分类模型中得到高分。同时不破坏GPT2对话模型输出通顺对话的能力。

强行学习训练
1. 输入样本给GPT2, 拿到对话语言模型 GPT2的输出。
2. 将对话语言模型GPT2的输出 输入到 情感分类模型 拿到 情感分类模型的输出，作为reward。
3. 将对话语言模型GPT2 输入，输出， 以及 情感分类模型的 reward 一并输入给PPO优化器，让PPO优化器去优化对话语言模型GPT2。

```py
import torch
from transformers import AutoTokenizer
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead, create_reference_model
from trl.core import respond_to_batch
import random
import torch.nn.functional as F

# get models
gen_model = AutoModelForCausalLMWithValueHead.from_pretrained('dialoggpt/')
model_ref = create_reference_model(gen_model)
tokenizerOne = AutoTokenizer.from_pretrained('dialoggpt/',padding_side='left')
tokenizerOne.eos_token_id = tokenizerOne.sep_token_id
# 初始化一个情感分类模型，输入文本，判断文本的情感极性
from transformers import AutoModelForSequenceClassification , AutoTokenizer, pipeline

ts_texts = ["我喜欢下雨。", "我讨厌他."]
cls_model = AutoModelForSequenceClassification.from_pretrained("./chineseSentiment/", num_labels=2)
tokenizerTwo = AutoTokenizer.from_pretrained("./chineseSentiment/")

classifier = pipeline('sentiment-analysis', model=cls_model, tokenizer=tokenizerTwo)
classifier(ts_texts)

# 数据预处理
from torch.utils.data import Dataset
import torch.nn.utils.rnn as rnn_utils
import json

data = []
with open("./train.txt", "r", encoding="utf-8") as f:
    for i in f.readlines():
        line = json.loads(i)
        data.append(line)


def preprocess_conversation(data):
    sep_id = tokenizerOne.sep_token_id
    cls_id = tokenizerOne.cls_token_id
    dialogue_list = []
    for conver in data:
        input_ids = [cls_id]
        start = conver["conversation"][0]
        # print(start["utterance"])
        input_ids += tokenizerOne.encode(start["utterance"], add_special_tokens=False)
        input_ids.append(sep_id)
        dialogue_list.append(input_ids)
    return dialogue_list

# 数据处理
dialogue_list = preprocess_conversation(data)

class MyDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        x = self.data[index]
        return torch.tensor(x)

    def __len__(self):
        return len(self.data)
    
mydataset = MyDataset(dialogue_list)

def collate_fn(batch):
    padded_batch = rnn_utils.pad_sequence(batch, batch_first=True, padding_value=tokenizerOne.sep_token_id)
    return padded_batch

# 定义PPO优化器: 学习率，强化学习steps，batch_size等参数，学习率不宜调大，容易把LLM语言模型调坏。
config = PPOConfig(
    model_name="gpt2-positive",
    learning_rate=1.41e-5,
    steps = 2000,
    batch_size = 16
)

ppo_trainer = PPOTrainer(config, gen_model, model_ref, tokenizerOne, dataset=mydataset, data_collator=collate_fn)

rewards_list = []
for epoch, batch in enumerate(ppo_trainer.dataloader):
    #### Get response from gpt2
    query_tensors = []
    response_tensors = []
    query_tensors = [torch.tensor(t).long() for t in batch]
    for query in batch:
        input_ids = query.unsqueeze(0)
        response = []
        for _ in range(30):
            outputs = ppo_trainer.model(input_ids=input_ids)
            logits = outputs[0]
            next_token_logits = logits[0, -1, :]
            next_token_logits[ppo_trainer.tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
            next_token = torch.multinomial(F.softmax(next_token_logits, dim=-1), num_samples=1)
            if next_token == ppo_trainer.tokenizer.sep_token_id:  #
                break
            input_ids = torch.cat((input_ids, next_token.unsqueeze(0)), dim=1)
            response.append(next_token.item())
        response_tensors.append(torch.Tensor(response).long())
    responseSet = ["".join(ppo_trainer.tokenizer.convert_ids_to_tokens([i.item() for i in r])) for r in response_tensors]
    print(responseSet)

    #### Get reward from sentiment model
    pipe_outputs = classifier(responseSet)
    rewards = [torch.tensor(output["score"]) for output in pipe_outputs]

    #### Run PPO step
    stats = ppo_trainer.step(query_tensors, response_tensors, rewards)
    print("epoch{}, reword is {}".format(epoch, sum(rewards)))
    rewards_list.append(sum(rewards))
```

### Firefly


[Firefly](https://github.com/yangjianxin1/Firefly) 是开源的大模型**一站式训练框架**
- 支持对各种大模型进行**预训练**、**指令微调**、`DPO`，支持全量参数、LoRA、QLoRA等训练方式。
- 支持包括但不限于Gemma、Qwen1.5、MiniCPM、Mixtral-8x7B、Mistral、Llama等绝大多数主流的大模型。

【2024-3-5】[使用Firefly在单卡V100上对Qwen1.5进行SFT和DPO，大幅超越Qwen1.5和Gemma](https://mp.weixin.qq.com/s/C5X0qX2YsxhIoFvRsqcMMA)

用Firefly项目对Qwen1.5-7B进行训练的实验。我们对训练数据进行精细化筛选，然后在单张V100上进行SFT和DPO。经过两阶段的训练，我们的模型在Open LLM Leaderboard上的表现显著优于官方的Qwen1.5-7B-Chat、Gemma-7B-it、Vicuna-13B等模型。比Qwen1.5-7B-Chat高7.12分，比Gemma-7B-it高8.8分。

### 总结

Megatron-DeepSpeed 实施 3D 并行以可以让大型模型以非常有效的方式进行训练。
- DataParallel (`DP`) - 相同的初始化模型被复制多次，并且每次都被馈送 minibatch 的一部分。处理是并行完成的，所有设置在每个训练步骤结束时进行同步。
- TensorParallel (`TP`) - 每个张量都被分成多个块，因此不是让整个张量驻留在单个 GPU 上，而是张量的每个分片都驻留在其指定的 GPU 上。在处理过程中，每个分片在不同的 GPU 上分别并行处理，最终结果在步骤结束时同步。这也被称作横向并行。
- PipelineParallel (`PP`) - 模型在多个 GPU 上垂直（层级）拆分，因此只有模型的一个或多个层放置在单个 GPU 上。每个 GPU 并行处理管道的不同阶段，并处理一小部分批处理。
- 零冗余优化器 (`ZeRO`) - 也执行与 TP 有点类似的张量分片，除了整个张量会及时重建以进行前向或反向计算，因此不需要修改模型。它还支持各种卸载技术以补偿有限的 GPU 内存。

训练超大规模语言模型主要有两条技术路线：
- TPU + XLA + TensorFlow/JAX
- GPU + PyTorch + Megatron-LM + DeepSpeed
- 前者由Google主导，由于TPU和自家云平台GCP深度绑定，对于非Googler来说， 只可远观而不可把玩
- 后者背后则有NVIDIA、Meta、MS大厂加持，社区氛围活跃，也更受到群众欢迎。

Deepspeed 是微软的大规模分布式训练工具。专门用于训练超大模型。
- [大模型的训练工具（1）---Deepspeed](https://zhuanlan.zhihu.com/p/609865550)
- `DP`+`PP`: DeepSpeed 将 DP 与 PP 结合起来
  - ![](https://pic1.zhimg.com/80/v2-127d807df8f6efc7b1f8cb6d5ff38620_1440w.webp)
- `DP`+`PP`+`TP`: 为了获得更高效的训练，PP 与 TP 和 DP 相结合，称为 3D 并行性
  - ![](https://pic1.zhimg.com/80/v2-7951815d9ab95beedf1d238bc58e73f0_1440w.webp)
- ZeRO DP+PP+TP: DeepSpeed 的主要功能之一是 ZeRO，它是 DP 的超级可扩展扩展。
- 【2023-3-16】[大型语言模型(LLM)训练指南](https://zhuanlan.zhihu.com/p/611325149)

增加的功能主要有：
- 3个维度并行化实现万亿参数模型训练
- ZeRO-Offload 使 GPU 单卡能够训练 10 倍大的模型
- 通过 DeepSpeed Sparse Attention 用6倍速度执行10倍长的序列
- 1 比特 Adam 减少 5 倍通信量

3D 并行：扩展至万亿参数模型

3D 并行同时解决了训练万亿参数模型的两个基本挑战：显存效率和计算效率。因此，DeepSpeed 可以扩展至在显存中放下最巨大的模型，而不会牺牲速度。
- 显存效率：集群上所能训练的LLM的参数量。
- 计算效率：单纯计算占系统的开销的比例。

（1）**数据并行**是分布式训练普遍使用的技术。

在该技术中，每批输入的训练数据都在数据并行的 worker 之间平分。反向传播后需要通信并规约梯度，以保证优化器在各个 worker 上进行相同的更新。数据并行性具有几个明显的优势，包括计算效率高和实现起来工作量小。但是，数据并行的 batch 大小随 worker 数量提高，而我们往往无法在不影响收敛性的情况下一直增加 batch 大小。
- 显存效率：数据并行会在所有 worker 之间进行模型和优化器的复制，因此显存效率不高。DeepSpeed 开发了 ZeRO ，它是一系列用于提高数据并行的显存效率的优化器。 这项工作依赖于 ZeRO 的 1 阶段，该阶段在 worker 之间划分优化器状态量以减少冗余。
- 计算效率：随着我们提高并行度，每个 worker 执行的计算量是恒定的。数据并行可以在小规模上实现近乎线性扩展。但是，在 worker 之间规约梯度的通信开销跟模型大小成正相关，所以当模型很大或通信带宽很低时，计算效率会受限。。梯度累积是一种用来均摊通信成本的一种常用策略。它会进一步增加batch大小，在本地使用 micro-batch 多次进行正向和反向传播积累梯度后，再进行梯度规约和优化器更新。

（2）**模型并行**是包含范围很广的一类技术。

它会在多个 worker 之间划分模型的各个层。就其本质而言，模型并行性的计算和通信因模型结构而异，因此在实现上有很大的工作量。DeepSpeed 借用了英伟达的 Megatron-LM 来为基于 Transformer 的语言模型提供大规模模型并行功能。模型并行会根据 worker 数量成比例地减少显存使用量，也是这三种并行度中显存效率最高的。但是其代价是计算效率最低。
- 显存效率：模型并行会根据 worker 数量成比例地减少显存使用量。至关重要的是，这是减少单个网络层的激活显存的唯一方法。DeepSpeed 通过在模型并行 worker 之间划分激活显存来进一步提高显存效率。
- 计算效率：由于每次前向和反向传播中都需要额外通信激活值，模型并行的计算效率很低。模型并行需要高通信带宽，并且不能很好地扩展到通信带宽受限的节点。此外，每个模型并行worker 都会减少每个通信阶段之间执行的计算量，从而影响计算效率。模型并行性通常与数据并行性结合使用，以在内存和计算效率之间进行权衡。

（3）**流水线并行**训练引擎也被包含在了这次发布的DeepSpeed中

流水线并行将模型的各层划分为可以并行处理的阶段。当一个阶段完成一个 micro-batch 的正向传递时，激活内存将被通信至流水线的下一个阶段。类似地，当下一阶段完成反向传播时，将通过管道反向通信梯度。必须同时计算多个 micro-batch 以确保流水线的各个阶段能并行计算。目前已经开发出了几种用于权衡内存和计算效率以及收敛行为的方法，例如 PipeDream。DeepSpeed 采用的方法是通过梯度累积来实现并行，并保持与传统数据并行和模型并行训练在相同的总 batch 大小下收敛情况相同。
- 显存效率：流水线并行减少的显存与流水线的阶段数成正比，使模型的大小可以随 worker 的数量线性扩展。但是，流水线并行不会减少每一层的激活函数的显存占用量。此外，每个 worker 必须存储同时运行的各个 micro-batch 的激活值。这导致流水线第一阶段的激活内存与单个 mirco batch 的总激活内存大致相同。一个万亿参数模型将需要为一个 micro batch 提供大约 19 GB 的显存的激活内存，这几乎占到新推出的英伟达 A100 GPU 总显存的一半。
- 计算效率：流水线并行具有最低的通信量，因为它的通信量只和在各阶段边界的各层的激活值大小成正比。但是，它不能无限扩展。像模型并行一样，增加流水线大小会减少每个流水线阶段的计算量，这会降低计算与通信的比率。如果要实现好的计算效率，流水线并行还要求其每个阶段的计算负载完美的均衡。


## 模型架构

**专家混合**（MoE）方法最近吸引了很多关注，因为研究人员（主要来自谷歌）试图突破模型大小的限制。该想法的核心是整合学习：多个弱学习模型组合以后会形成能力出众的学习模型。

Shazeer 等人于2017年发表了名为“稀疏门控专家混合”（MoE）层的文章，提出了在一个深度神经网络中可以通过连接多个专家的门控机制来实现输出控制的方法。


## 神经网络训练开销

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
- 模型参数： 参数量*每个参数所需内存
  - 对于fp32，LLaMA-6B需要 6B*4 bytes = 24GB 内存
  - 对于int8，LLaMA-6B需要 6B*1 byte = 6GB 内存
- 梯度： 参数量*每个梯度参数所需内存
- 优化器参数： 不同的优化器所储存的参数量不同。
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
- 显存占用大头是 Adam 优化器，占可计算部分的 12/16=75%
- 其次是模型参数+梯度，显存容量至少是参数量的**16倍**

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
- 理论情况下能达到**线性**的加速效果。TF、torch、Horovod都可以在原生支持或者微小的改动实现数据并行模式。

多个GPU 情况下，将模型分发到每个GPU上去，每个GPU都保留完整的模型参数。
- 每个GPU加载全部模型（Parameter、Grad、Optimizer、Activation、Temp buffer）
- 将每个batch的样本平均分配到每个GPU上进行梯度计算
- 然后汇总每个GPU上的梯度，在将汇总梯度重新分发到每个GPU上，每个GPU模型根据汇总的梯度进行模型参数更细。
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


#### DP(单机)+DDP(多机)

数据并行（DP&DDP）
- `DP`（Data Parallelism）：早期数据并行模式，一般采用**参数服务器**(Parameters Server)编程框架。实际中多用于**单机多卡**。 
- `DDP`（Distributed Data Parallelism）：分布式数据并行，采用`Ring AllReduce`的通讯方式，多用于**多机多卡**场景。



### 模型并行（model parallesim）

当**模型参数过大**，单个 GPU无法容纳模型参数时，就需要模型并行, 将模型拆分到多个 GPU 训练。

模型并行相对复杂
- 原理：分布式系统中的不同worker负责网络模型的不同部分
- 例如，神经网络的不同层被分布到不同worker或者同一层的不同参数被分配到不同worker上。
- 对于TF这种框架，可以拆分计算图成多个最小依赖子图到不同的worker上。同时在多个子图之间通过通信算子来实现模型并行。

但是**模型并行**实现起来比较复杂。工业界还是以**数据并行**为主。

补充：
- `Model Parallel`主要分两种：**intra-layer**拆分 和 **inter-layer**拆分
  - `inter-layer`拆分：对模型做网络上的拆分,将每一层或者**某几层**放在一个worker上单独训练。
    - 缺点：模型训练串行，整个模型的效率取决于最慢的那一层，存在资源浪费
  - `intranet-layer`拆分：深度学习的网络结构基本都是一层层的。常规的卷积、池化、BN等等。如果对某一层进行了拆分，那么就是intra-layer拆分。对单层的拆分其实就是拆分这一层的matrix运算。
    - 参考论文：Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism

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


#### 流水线并行

**流水线并行**（Pipeline model parallesim）
- 朴素拆分方式: 将模型各层分组后装载到各个GPU上去，GPU之间进行**串行**计算
  - 缺点: GPU 利用率太低，当一个GPU进行计算时，其他层的GPU都闲置。
- 改进: 谷歌提出了GPipe `流水线并行`（Pipeline model parallesim ）, 引入micro-batches (MBS)的概念，会提升GPU利用率

#### 张量并行

**张量并行**（Tensor Model Parallelism）
- 张量并行（TP）是模型并行一种形式，流水线并行按**网络层**切分，张量并行按**矩阵**切分。
- 2019年，NVIDIA发布《Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM》论文，提出了张量并行方法
- 核心思想: 每个GPU仅处理矩阵一部分，当算子需要整个矩阵的时候再进行矩阵聚合。无论是横向切分还是竖向切分，都可以将切分后的矩阵放到不同GPU上进行计算，最后将计算的结果再合并。

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


### 混合并行

随着训练设备的增加，多个worker之间的通信成本增加，模型Reduce的成本也越来越大，数据并行的瓶颈也随之出现。故有学者提出**混合并行**(数据并行+模型并行)


### 架构模式

分布式训练上会频繁用到**规约**(AllReduce)操作。主流的**分布式架构**主要分为`参数服务器`(ParameterServer) 和`基于规约`(Reduce)两种模式。早期还有基于`MPI`的方式，不过现在已经很少用了。

#### PS：参数服务器

ParameterServer模式是一种基于reduce和broadcat算法的经典架构。
- 其中一个/一组机器作为PS架构的**中心节点**，用来**存储参数和梯度**。
- 在更新梯度的时候，先全局reduce接受其他worker节点的数据，经过本地计算后(比如参数平均法)，再broadcast回所有其他worker。

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

实际训练过程中可能遇到各种问题，比如：部分节点资源受限、卡顿、网络延时等等，因此梯度同步时就存在“**木桶**“效应，即集群中的某些worker比其他worker更慢，导致整个训练pipeline需要等待慢的worker，整个集群的训练速度受限于最慢机器的速度。

因此梯度的同步有“**同步**”(sync)、“**异步**”(Async)和**混合**三种范式。
- **同步**范式：只有所有worker完成当前的计算任务，整个集群才会开始下一次迭代。
  - TF中同步范式使用SyncReplicasOptimizer优化器
- **异步**模式刚好相反，每个worker只关心知己的进程，完成计算后就尝试更新，能与其他多个worker同步梯度完成取决于各worker当前时刻的状态。其过程不可控，有可能出现模型正确性问题。(可在训练时logging对比)
- **混合**范式结合以上两种情况，各个worker都会等待其他worker的完成，但不是永久等待，有timeout的机制。如果超时了，则此情况下相当于异步机制。并且没来得及完成计算的worker，其梯度则被标记为“stale”而抛弃或另做处理。

### 物理架构

物理架构主要是 **GPU架构**，即：单机单卡、单机多卡、多机单卡、多机多卡（最典型）
- 单机单卡：常规操作
- 单机**多卡**：利用一台GPU上的多块GPU进行分布式训练。数据并行和模型并行皆可。整个训练过程一般只有一个进程，多GPU之间的通信通过多线程的方式，模型参数和梯度在进程内是共享的(基于NCCL的可能不大一样)。这种情况下基于Reduce的架构比PS架构更合适一些，因为不需要一个显式的PS，通过进程内的Reduce即可完成梯度同步。
- **多机**单卡：操作上与多机多卡基本一致
- 多机**多卡**：多机多卡是最典型的分布式架构，所以它需要较好的进程间的通讯机制(多worker之间的通信)。

### 通信技术

分布式条件下的多进程、多worker之间的通信技术，常见的主要有：MPI、NCCL，GRPC等。
- **MPI**主要是被应用在超算等大规模计算领域，机器学习场景下使用较少。主要是openMPI原语等。
- **NCCL**是NVIDIA针对GPU设计的一种规约库，可以实现多GPU间的直接数据同步，避免内存和显存的，CPU和GPU间的数据拷贝成本。当在TensorFlow中选择单机多卡训练时，其默认采用的就是NCCL方式来通信。
- **GRPC**是比较成熟的通信技术了，spark等框架内也都有用到。


内容：
- 分布式训练的基本原理
- TensorFlow的分布式训练
- PyTorch的分布式训练框架
- Horovod分布式训练

## 分布式实现

- 黄文坚的[Tensorflow分布式实战](https://blog.csdn.net/CodeMaster_/article/details/76223835)

### TF分布式训练方法

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
  - init_method：字符串类型，是一个 url，用于指定进程初始化方式，默认是 “env://”，表示从环境变量初始化，还可以使用 TCP 的方式或共享文件系统 。
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

【2023-3-2】[PyTorch 分布式训练实现(DP/DDP/torchrun/多机多卡)](https://zhuanlan.zhihu.com/p/489011749)

相对Tensorflow，Pytorch简单的多。分布式训练主要有两个API：
- DataParallel(`DP`): **PS模式**，会有一张卡为reduce（parame server），实现简单，就一行代码
  - 将数据分割到多个GPU上。这是典型的`数据并行`，将模型复制到每个GPU上，一旦GPU0计算出梯度，则需要同步梯度，这需要大量的GPU数据传输（类似PS模式）
- DistributedDataParallel(`DDP`): **All-Reduce模式**，单机多卡/多级多卡皆可。官方建议API
  - 每个GPU的进程中创建模型副本，并只让数据的一部分对改GPU可用。因为每个GPU中的模型是独立运行的，所以在所有的模型都计算出梯度后，才会在模型之间同步梯度（类似All-reduce）

分析
- `DDP`每个batch只需要一次数据传输；
- `DP`可能存在多次数据同步(不用worker之间可能快慢不一样)。

### 1、DataParallel

模型与变量必须存在于同一个设备上（CPU or GPU）

pytorch使用**to函数**实现变量或模型的存储转移
- to函数的对象: 数据Tensor，或 模型Module 
- 张量不执行inplace(即 执行之后重新构建一个新的张量)
- 模型执行inplace(执行之后不重新构建一个新的模型)

原理：
- 当给定model时，主要实现功能是将input数据依据batch的这个维度，将数据划分到指定的设备上。其他的对象(objects)复制到每个设备上。在前向传播的过程中，module被复制到每个设备上，每个复制的副本处理一部分输入数据。在反向传播过程中，每个副本module的梯度被汇聚到原始的module上计算(一般为第0块GPU)。

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

为什么要引入DDP（DistributedDataParallel）？
- 1、DP在每个训练批次（batch）中，因为模型权重都是在 一个进程上先算出来, 然后再把分发到每个GPU上，所以网络通信就成为了一个瓶颈，而GPU使用率也通常很低。
- 2、因为在每次前向传播时把模型也复制了（即每次更新都复制一遍模型），并且单进程多线程会造成`GIL` contention （全局解释器锁争用） 这里进程计算权重使通信成为瓶颈造成了大量的时间浪费，因此引入了DDP。

DDP采用**多进程**控制多GPU，共同训练模型，一份代码会被pytorch自动分配到n个进程并在n个GPU上运行。 
- DDP运用 `Ring-Reduce`通信算法在每个GPU间对梯度进行通讯，交换彼此的梯度，从而获得所有GPU的梯度。

对比DP，不需要在进行模型本体的通信，因此可以加速训练。

需要注意以下几点：
- 1、设置DistributedSampler来打乱数据，因为一个batch被分配到了好几个进程中，要确保不同的GPU拿到的不是同一份数据。
- 2、要告诉每个进程自己的id，即使用哪一块GPU。
- 3、如果需要做BatchNormalization，需要对数据进行同步（还待研究，挖坑）

DDP采用All-Reduce架构，单机多卡、多机多卡都能用。

注意：DDP并不会自动shard数据
1. 如果自己写数据流，得根据`torch.distributed.get_rank()`去shard数据，获取自己应用的一份
2. 如果用 Dataset API，则需要在定义Dataloader的时候用 DistributedSampler 去shard

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

```python
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

### Torchrun (更新)

最新版本 PyTorch实现
- 替换 torch.distributed.launch

PyTorch 官网介绍
- This module（torch.distributed.launch） is going to be deprecated in favor of `torchrun`.

`torchrun` 包含了 torch.distributed.launch 的所有功能，还有三点额外功能：
- 1、worker 的 rank和world_size将被自动分配
- 2、通过重新启动所有workers来处理workers的故障
- 3、允许节点数目在最大最小值之间有所改变 即**具备弹性**

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

三种启动方法：
- torch.distributed.launch
- torch.multiprocessing
- Slurm Workload Manager: slurm启动应该会这几天更新掉

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


## Horovod 分布式训练

Horovod 是 Uber开源的跨平台的分布式训练工具，名字来自于俄国传统民间舞蹈，舞者手牵手围成一个圈跳舞，与Horovod设备之间的通信模式很像，有以下几个特点：
- 兼容TensorFlow、Keras和PyTorch机器学习框架。
- 使用Ring-AllReduce算法，对比Parameter Server算法，有着无需等待，负载均衡的优点。
- 实现简单，五分钟包教包会。

Horovod环境准备以及示例代码，可参考[上一篇](https://zhuanlan.zhihu.com/p/351693076)

# 推理加速

![](https://pica.zhimg.com/v2-4722a5639a0dafc705be6199c5920a08_1440w.jpg)

## ONNX

- 【2022-5-17】[ONNX 和 Azure 机器学习：创建和加速 ML 模型](https://docs.microsoft.com/zh-cn/azure/machine-learning/concept-onnx)
- 【2022-6-9】[ONNX推理加速技术文档](https://zhuanlan.zhihu.com/p/524023964)
- 【2022-2-23】贝壳，onnxruntime优化过后的bert模型，cpu推理延迟能从300ms降到100ms以内

推理或模型评分是将部署的模型用于**预测**（通常针对生产数据）的阶段，ONNX 来帮助优化机器学习模型的推理

pytorch怎么使用c++调用部署模型？[参考](https://zhuanlan.zhihu.com/p/589562702)
- **PyTorch模型** --> `ONNX格式` --> **C++推理框架**

### 什么是ONNX

开放神经网络交换（Open Neural Network Exchange） `ONNX` 是**微软**和**Facebook**提出，用来表示深度学习模型的**开放格式**。
- [ONNX](https://onnx.ai/)定义了一组和环境平台均无关的标准格式，来增强各种AI模型的可交互性。
- 优化用于**推理**（或模型评分）的机器学习模型非常困难，因为需要调整模型和推理库，充分利用硬件功能。 在不同类型的平台（云/Edge、CPU/GPU 等）上获得最佳性能，异常困难，因为每个平台都有不同的功能和特性。 如果模型来自需要在各种平台上运行的多种框架，会极大增加复杂性。 优化框架和硬件的所有不同组合非常耗时。 

ONNX就是解决方法，在首选框架中训练一次后能在云或 Edge 上的**任意**位置运行。
- ![ONNX](https://pic3.zhimg.com/80/v2-b78c389b742875193877e806a661da6e_1440w.webp)

许多框架中的模型都可以导出或转换为标准 **ONNX 格式**。 模型采用 ONNX 格式后，可在各种平台和设备上运行。
- 各种平台包括 TensorFlow、PyTorch、SciKit-Learn、Keras、Chainer、MXNet、MATLAB 和 SparkML
**ONNX 运行时**是一种用于将 ONNX 模型部署到生产环境的**高性能推理引擎**。 它针对云和 Edge 进行了优化，适用于 Linux、Windows 和 Mac。
- ONNX文件不仅仅存储了神经网络模型的权重(Protobuf格式)，同时也存储了模型的结构信息以及网络中每一层的输入输出和一些其它的辅助信息。
- 用 C++ 编写，还包含 C、Python、C#、Java 和 JavaScript (Node.js) API，可在各种环境中使用。 
- ONNX 运行时同时支持 DNN 和传统 ML 模型，并与不同硬件上的**加速器**（例如，NVidia GPU 上的 `TensorRT`、Intel 处理器上的 `OpenVINO`、Windows 上的 `DirectML` 等）集成。 
通过使用 ONNX 运行时，可以从大量的生产级优化、测试和不断改进中受益。
- ![](https://docs.microsoft.com/zh-cn/azure/machine-learning/media/concept-onnx/onnx.png)

### 示例

yolov3-tiny的[onnx模型](https://github.com/onnx/models/tree/master/vision/object_detection_segmentation/tiny-yolov3/model),Netron可视化
- ![](https://pic2.zhimg.com/80/v2-d21635b818ed67dfdb4c834324fa1555_1440w.jpg)

更多使用方法见: [ONNX学习笔记](https://zhuanlan.zhihu.com/p/346511883)


### 二、直接使用onnx进行推理
 
onnx文件可以直接进行推理，这时的代码就已经与框架无关了，可以与训练阶段解耦。但是，为了推理的顺利进行，你依然需要为onnx选择一个后端，以TensorFlow为例。
 
```python
import onnx
import tensorflow as tf
from onnx_tf.backend import prepare
import onnx_tf...# 包装一个TF后端
predictor = onnx.load(onnx_path)
onnx.checker.check_model(predictor)
onnx.helper.printable_graph(predictor.graph)
tf_rep = prepare(predictor, device="CUDA:0")  # default CPU
# 使用TF进行预测
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)  # defalut 0.5
tfconfig = tf.ConfigProto(allow_soft_placement=True, gpu_options=gpu_options)... 
with tf.Session(config=tfconfig) as persisted_sess:
    persisted_sess.graph.as_default()
    tf.import_graph_def(tf_rep.graph.as_graph_def(), name='')
    tf_input = persisted_sess.graph.get_tensor_by_name(
        tf_rep.tensor_dict[tf_rep.inputs[0]].name
    )
    tf_scores = persisted_sess.graph.get_tensor_by_name(
        tf_rep.tensor_dict[tf_rep.outputs[0]].name
    )
    tf_boxes = persisted_sess.graph.get_tensor_by_name(
        tf_rep.tensor_dict[tf_rep.outputs[1]].name
    )
 
    for file_path in listdir:
        ...
        confidences, boxes = persisted_sess.run([tf_scores, tf_boxes], {tf_input: image})
        ...
```
 
### 三、使用onnxruntime加速推理
 
事实上，可以更高效地使用onnx。onnxruntime是一个对onnx模型提供推理加速的库，支持CPU和GPU加速，GPU加速版本为onnxruntime-gpu，默认版本为CPU加速。安装:
 
```shell
pip install onnxruntime  # CPU
pip install onnxruntime-gpu # GPU
```
 
使用onnxruntime对onnx模型加速非常简单，只需要几行代码。这里给出一个示例：
 
```python
import onnxruntime as ort

class NLFDOnnxCpuInferBase:
    """only support in CPU and accelerate with onnxruntime."""
 
    __metaclass__ = ABCMeta
   ...
   def __init__(self,
                 onnx_path=ONNX_PATH):
        """pytorch和onnx可以很好地结合        :param onnx_path: .onnx文件路径        """
        self._onnx_path = onnx_path
        # 使用onnx模型初始化ort的session
        self._ort_session = ort.InferenceSession(self._onnx_path)
        self._input_img = self._ort_session.get_inputs()[0].name
   ...
 
   # 使用run推理
   def _detect_img_utils(self, img: np.ndarray):
        """batch is ok."""
        feed_dict = {self._input_img: img}
        scores_before_nms, rois_before_nms = self._ort_session.run(None,input_feed=feed_dict)
        return rois_before_nms, scores_before_nms
```
 
onnxruntime会自动帮你检查onnx中的无关节点并删除，也利用了一些加速库优化推理图，从而加速推理。一些log:
 
```shell
python3 inference/ulfd/onnx_cpu_infer.py
# 2020-01-16 12:03:49.259044 [W:onnxruntime:, graph.cc:2412 CleanUnusedInitializers] Removing initializer 'base_net.9.4.num_batches_tracked'. It is not used by any node and should be removed from the model.
# 2020-01-16 12:03:49.259478 [W:onnxruntime:, graph.cc:2412 CleanUnusedInitializers] Removing initializer 'base_net.9.1.num_batches_tracked'. It is not used by any node and should be removed from the model.
# 2020-01-16 12:03:49.259492 [W:onnxruntime:, graph.cc:2412 CleanUnusedInitializers] Removing initializer 'base_net.8.4.num_batches_tracked'. It is not used by any node and should be removed from the model.
# 2020-01-16 12:03:49.259501 [W:onnxruntime:, graph.cc:2412 CleanUnusedInitializers] Removing initializer 'base_net.8.1.num_batches_tracked'. It is not used by any node and should be removed from the model.
```
 
### 四、实验结果
 
在人脸检测ULFD模型上，未使用onnxruntime加速，对于320x240分辨率的图片，在CPU上需要跑要50~60ms;使用onnxruntime加速后，在CPU需要8~11ms.
 
### 五、请优雅地使用Numpy
 
在图像处理中经常会出现归一化处理，即使在推理的时候也需要。而在推理时需要考虑性能问题，最近发现numpy的张量计算的不同方式，会对性能有很大影响。如果你的均值化处理中的每个通道减去的均值都是一样的比如127.
 
```python
# 普通的做法是：(请不要使用这种做法)
image_mean = np.array([127, 127, 127])
image = (image - image_mean) / 128 # 实际上会由于numpy的广播运算消耗更多的时间
# 你应该采用：(保证数据类型的一致以及减去一个常量的效率更高)
image = (image - 127.) / 128.
```
 
*   _实验代码 相同均值_
    
 
```python
# coding: utf-8
import cv2
import time
import numpy as np

if __name__ == '__main__':
    test_w, test_h = 500, 500
 
    test_path = 'logs/test0.jpg'
    test_img = cv2.imread(test_path)
    resize_img = cv2.resize(test_img, (test_w, test_h))

    test_count = 1000
    print('width: {0}, height: {1}, test_count: {2}'.format(test_w, test_h, test_count))
 
    t1 = time.time()
    image_mean = np.array([127, 127, 127])
    for _ in range(test_count):
        image = (resize_img - image_mean) / 128
    t2 = time.time()
    print('total_time_ugly: {0}s, mean_time_ugly: {1}ms'.format(
        (t2-t1), (t2-t1)*1000/test_count
    ))
    t3 = time.time()
    for _ in range(test_count):
        image = (resize_img - 127.) / 128.
    t4 = time.time()
    print('total_time_elegant: {0}s, mean_time_elegant: {1}ms'.format(
        (t4 - t3), (t4 - t3) * 1000 / test_count
    ))
```
 
实验结果：
- ![](https://pic2.zhimg.com/80/v2-46ca71eacd67ea8f9b279e6dc83289fd_1440w.jpg)
 
但是当你确实要对不同的通道用到不同的均值时呢？ 也请你这样做，以下是另一个测试结果。
 
* _实验代码 不同均值_
    
 
```python
# coding: utf-8
import cv2
import time
import numpy as np
 
if __name__ == '__main__':
    test_w, test_h = 100, 100
 
    test_path = 'logs/test0.jpg'
    test_img = cv2.imread(test_path)
    resize_img = cv2.resize(test_img, (test_w, test_h))
 
 
    test_count = 100
    print('width: {0}, height: {1}, test_count: {2}'.format(test_w, test_h, test_count))
    print('-'*100)
    t1 = time.time()
    image_mean = np.array([127, 120, 107])
    for _ in range(test_count):
        image = (resize_img - image_mean) / 128
    t2 = time.time()
    print('total_time_ugly: {0}s, mean_time_ugly: {1}ms'.format(
        (t2 - t1), (t2 - t1) * 1000 / test_count
    ))
    t3 = time.time()
    image = np.zeros_like(resize_img)
    for _ in range(test_count):
        image[:, :, 0] = (resize_img[:, :, 0] - 127.) / 128.
        image[:, :, 1] = (resize_img[:, :, 1] - 120.) / 128.
        image[:, :, 2] = (resize_img[:, :, 2] - 107.) / 128.
    t4 = time.time()
    print('total_time_elegant: {0}s, mean_time_elegant: {1}ms'.format(
        (t4 - t3), (t4 - t3) * 1000 / test_count
    ))
```
 
实验结果
- ![](https://pic2.zhimg.com/80/v2-1a79d361282b74a108592b1c48f24259_1440w.jpg)
 
简单来说就是，只要你愿意动手修改几行代码，就能带来5ms~15ms的性能提升。这比采用TensorRT/ONNX等各种加速工具要简单太多了。


## 模型文件转换

ONNX的目的是“通用”，所以难免出现算子不兼容的情况。
- 当把某个框架（例如PyTorch）的模型转成ONNX后，再将ONNX转成另一框架模型（例如ncnn）时，可能会报错（xxx算子不支持）。

解决方法：
- 使用 ONNXSIM 对 ONNX模型 进行精简，非常有效。
  - 建议：只要使用了ONNX，都用ONNXSIM对ONNX模型进行处理一次。[Github地址](https://github.com/daquexian/onnx-simplifier)。使用非常方便，使用“pip install onnxsim”安装，然后使用命令“onnxsim input_onnx_model_path output_onnx_model_path”即可。代码中调用也很简单，参考Git地址里的示例。
- 避免依赖于中间变量的尺寸来进行运算。
  - 在一些Image to Image的任务中，可能会根据中间tensor的尺寸来对另一些tensor进行resize。这时我们的做法是先去获取中间tensor的尺寸H、W，然后将它们作为参数送给其它方法。当遇到这种运算时，ONNX似乎会创建两个与H、W相关的变量，但它们的值会绑定为用dummy_input去forward一次时得到的H、W。这个值一旦绑定就不会改变。所以后续当使用不同尺寸输入时极大概率会报错（这点没有仔细验证过，但看中间结果很像是这种情况）。
- 另外, 强烈建议使用一些网络可视化工具。当遇到模型转换报错时可以用来方便定位出错的位置。个人比较喜欢的是[netron](https://github.com/lutzroeder/netron)

### 1.1 pth文件(Pytorch)转onnx
 
pytorch框架集成了**onnx模块**，属于官方支持，onnx也覆盖了pytorch框架中的大部分算子。因此将pth模型文件转换为onnx文件非常简单。

```py
import torch
# 指定输入尺寸，ONNX需要这个信息来确定输入大小
# 参数对应于 (batch_size, channels, H, W)
dummy_input = torch.randn(1, 3, 224, 224, device="cuda")
# model为模型自身
# dummy_input根据自己的需求更改其尺寸
# "model.onnx"为输出文件，更改为自己的路径即可
torch.onnx.export(model, dummy_input, "model.onnx")
```

以下是一个代码示例。需要注意的是，在转换之前，需要对pth模型的输入size进行冻结。比如：
 
```py
batch_size = 1
dummy_input = torch.randn(batch_size, 3, 240, 320).to(device)
```
 
输入一旦冻结后，就只会有固定的batch_size，在使用转换后的onnx文件进行模型推理时，推理时输入的batch_size必须和冻结时保持一致。对于这个示例，你只能batch_size=1进行推理。如果你需要在推理时采用不同的batch_size，比如10，你只能在保存onnx模型之前修改冻结的输入节点，代码如下：
 
```py
batch_size = 10
dummy_input = torch.randn(batch_size, 3, 240, 320).to(device)
```
 
这样，你就拥有了一个bacth_size=10的onnx模型。导出onnx文件，只需要使用torch.onnx.export()函数，代码如下：
 
```py
    model_name = model_path.split("/")[-1].split(".")[0]
    model_path = f"inference/ulfd/onnx/{model_name}-batch-{batch_size}.onnx"
 
    dummy_input = torch.randn(batch_size, 3, 240, 320).to(device)
    # dummy_input = torch.randn(1, 3, 480, 640).to("cuda") #if input size is 640*480
    torch.onnx.export(net, dummy_input, model_path,
                      verbose=False, input_names=['input'],
                      output_names=['scores', 'boxes'])
```
 
完整的转换代码：
 
```python
# -*- coding: utf-8 -*-
"""This code is used to convert the pytorch model into an onnx format model."""
import argparse
import sys
import torch.onnx
from models.ulfd.lib.ssd.config.fd_config import define_img_size

input_img_size = 320  # define input size ,default optional(128/160/320/480/640/1280)
define_img_size(input_img_size)
from models.ulfd.lib.ssd.mb_tiny_RFB_fd import create_Mb_Tiny_RFB_fd
from models.ulfd.lib.ssd.mb_tiny_fd import create_mb_tiny_fd

def get_args():
    parser = argparse.ArgumentParser(description='convert model to onnx')
    parser.add_argument("--net", dest='net_type', default="RFB",
                        type=str, help='net type.')
    parser.add_argument('--batch', dest='batch_size', default=1,
                        type=int, help='batch size for input.')
    args_ = parser.parse_args()
 
    return args_if __name__ == '__main__':
 
    # net_type = "slim"  # inference faster,lower precision
    args = get_args()
 
    net_type = args.net_type  # inference lower,higher precision
    batch_size = args.batch_size
 
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
 
    label_path = "models/ulfd/voc-model-labels.txt"
    class_names = [name.strip() for name in open(label_path).readlines()]
    num_classes = len(class_names)
 
    if net_type == 'slim':
        model_path = "baseline/ulfd/version-slim-320.pth"
        # model_path = "models/pretrained/version-slim-640.pth"
        net = create_mb_tiny_fd(len(class_names), is_test=True, device=device)
    elif net_type == 'RFB':
        model_path = "baseline/ulfd/version-RFB-320.pth"
        # model_path = "models/pretrained/version-RFB-640.pth"
        net = create_Mb_Tiny_RFB_fd(len(class_names), is_test=True, device=device)
 
    else:
        print("unsupport network type.")
        sys.exit(1)
    net.load(model_path)
    net.eval()
    net.to(device)
 
    model_name = model_path.split("/")[-1].split(".")[0]
    model_path = f"inference/ulfd/onnx/{model_name}-batch-{batch_size}.onnx"
 
    dummy_input = torch.randn(batch_size, 3, 240, 320).to(device)
    # dummy_input = torch.randn(1, 3, 480, 640).to("cuda") #if input size is 640*480
    torch.onnx.export(net, dummy_input, model_path,
                      verbose=False, input_names=['input'],
                      output_names=['scores', 'boxes'])
    print('onnx model saved ', model_path)
 
    """    PYTHONPATH=. python3 inference/ulfd/pth_to_onnx.py --net RFB --batch 16    PYTHONPATH=. python inference/ulfd/pth_to_onnx.py --net RFB --batch 3    """
```
 
### 1.2 pb文件(TensorFlow)转onnx
 
pb文件转onnx可以使用**tf2onnx**库，但必须说明的是，TensorFlow并没有官方支持onnx，tf2onnx是一个第三方库。格式转化onnx格式文件将tensorflow的pb文件转化为onnx格式的文件 安装tf2onnx。 
- 参考：[tensorrt-cubelab-docs](https://dev.pandateacher.com/cube-lab/document/tutorial/tensorrt.html) tf2onnx安装
 
```shell
pip install tf2onnx
```

格式转化指令:
 
```shell
python -m tf2onnx.convert --input ./checkpoints/new_model.pb --inputs intent_network/inputs:0,intent_network/seq_len:0 --outputs logits:0 --output ./pb_models/model.onnx --fold_const # SAVE_MODEL保存为save_model
```

```python
from tensorflow.python.compiler.tensorrt import trt_convert as trt
converter = trt.TrtGraphConverter(input_saved_model_dir=input_saved_model_dir)
converter.convert()
converter.save(output_saved_model_dir)
```

```shell
python -m tf2onnx.convert --saved_model saved_model_dir --output model.onnx # .pb 文件
python -m tf2onnx.convert --input frozen_graph.pb  --inputs X:0,X1:0 --outputs output:0 --output model.onnx --fold_const # .ckpt 文件
python -m tf2onnx.convert --checkpoint checkpoint.meta  --inputs X:0 --outputs output:0 --output model.onnx --fold_const
```
 
### 1.3 onnx转pb文件(TensorFlow)
 
有时候，我们需要对模型进行**跨框架**的转换，比如用pytorch训练了一个模型，但需要集成到TensorFlow中以便和其他的模型保持一致，方便部署。

此时就可以通过将pth转换成onnx，然后再将onnx转换成pb文件，如果转换成功，那么就可以在TensorFlow使用pb文件进行推理了。之所以强调如果，是因为TensorFlow并没有官方支持onnx，有可能会因为一些算子不兼容的问题导致转换后的pb文件在TF推理时出问题。 将onnx转换pb文件可以使用onnx-tf库，安装

```
pip install onnx-tf
```
 
完整的转换代码：
 
```python
# -*- coding: utf-8 -*-
"""
    @File  : onnx_to_pb.py@Author: qiuyanjun@Date  : 2020-01-10 19:22@Desc  : 
"""
import cv2
import numpy as np
import onnx
import tensorflow as tf
from onnx_tf.backend import prepare
import onnx_tf
model = onnx.load('models/onnx/version-RFB-320.onnx')
tf_rep = prepare(model)
img = cv2.imread('imgs/1.jpg')
image = cv2.resize(img, (320, 240))# 测试是否能推理
image_mean = np.array([127, 127, 127])
image = (image - image_mean) / 128
image = np.transpose(image, [2, 0, 1])
image = np.expand_dims(image, axis=0)
image = image.astype(np.float32)
output = tf_rep.run(image)
print("output mat: \\n", output)
print("output type ", type(output))# 建立Session并获取输入输出节点信息
with tf.Session() as persisted_sess:
    print("load graph")
    persisted_sess.graph.as_default()
    tf.import_graph_def(tf_rep.graph.as_graph_def(), name='')
    inp = persisted_sess.graph.get_tensor_by_name(
        tf_rep.tensor_dict[tf_rep.inputs[0]].name
    )
    print('input_name: ', tf_rep.tensor_dict[tf_rep.inputs[0]].name)
    print('input_names: ', tf_rep.inputs)
    out = persisted_sess.graph.get_tensor_by_name(
        tf_rep.tensor_dict[tf_rep.outputs[0]].name
    )
    print('output_name_0: ', tf_rep.tensor_dict[tf_rep.outputs[0]].name)
    print('output_name_1: ', tf_rep.tensor_dict[tf_rep.outputs[1]].name)
    print('output_names: ', tf_rep.outputs)
    res = persisted_sess.run(out, {inp: image})
    print(res)
    print("result is ", res)# 保存成pb文件
    tf_rep.export_graph('version-RFB-320.pb')
    print('onnx to pb done.')
    
"""cmd
PYTHONPATH=. python3 onnx_to_pb.py
"""
```
 
### 1.4 ONNX转ncnn

[ncnn](https://github.com/Tencent/ncnn)是腾讯开源的轻量级推理框架, 简单易用, 但当功耗、时耗是主要考虑点的时候，需要多尝试其它框架，如TensorFlow Lite。


## TensorRT

- 【2021-5-21】[TensorRT入门指北](https://zhuanlan.zhihu.com/p/371239130)
[显卡算力查看](https://developer.nvidia.com/zh-cn/cuda-gpus)


### 什么是TensorRT

- TensorRT是由Nvidia推出的C++语言开发的高性能**神经网络推理库**，是一个用于生产部署的优化器和运行时引擎。其高性能计算能力依赖于Nvidia的图形处理单元。它专注于推理任务，与常用的神经网络学习框架形成互补，包括TensorFlow、Caffe、PyTorch、MXNet等。可以直接载入这些框架的已训练模型文件，也提供了API接口通过编程自行构建模型。
  - ![](https://img-blog.csdnimg.cn/20210425231146908.png)
- TensorRT是可以在NVIDIA各种GPU硬件平台下运行的一个C++推理框架。我们利用Pytorch、TF或者其他框架训练好的模型，可以转化为TensorRT的格式，然后利用TensorRT推理引擎去运行我们这个模型，从而提升这个模型在英伟达GPU上运行的速度。速度提升的比例是比较可观的。
- TensorRT是由C++、CUDA、python三种语言编写成的一个库，其中核心代码为C++和CUDA，Python端作为前端与用户交互。当然，TensorRT也是支持C++前端的，如果我们追求高性能，C++前端调用TensorRT是必不可少的。
- TensorRT是半开源的，除了核心部分其余的基本都开源了。
![](https://pic4.zhimg.com/80/v2-bc9b29cc831bb9793a0aeaaa3061e223_720w.jpg)

### TensorRT的使用场景

TensorRT的使用场景很多。服务端、嵌入式端、家用电脑端都是我们的使用场景。
- 服务端对应的显卡型号为A100、T4、V100等
- 嵌入式端对应的显卡为AGX Xavier、TX2、Nano等
- 家用电脑端对应的显卡为3080、2080TI、1080TI等

当然这不是固定的，只要我们显卡满足TensorRT的先决条件，用就对了。

### TensorRT安装

安装TensorRT的方式有很多，[官方](https://developer.nvidia.com/zh-cn/tensorrt)提供了多种方式：Debian or RPM packages, a pip wheel file, a tar file, or a zip file.
- 如下载TensorRT-7.2.3.4.Ubuntu-18.04.x86_64-gnu.cuda-11.1.cudnn8.1.tar.gz
  - TensorRT的版本与CUDA还有CUDNN版本是密切相关的,不匹配版本的cuda以及cudnn是无法和TensorRT一起使用的
  - 查看本机驱动：nvidia-smi
- 下载好后，tar -zxvf解压即可。
- 解压之后我们需要添加环境变量，以便让我们的程序能够找到TensorRT的libs

```shell
vim ~/.bashrc
# 添加以下内容
export LD_LIBRARY_PATH=/path/to/TensorRT-7.2.3.4/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/to/TensorRT-7.2.3.4/lib::$LIBRARY_PATH
```

### TensorRT 工作流

工作流主要分为两个阶段：建造阶段(build  phase)和执行阶段(compile phase)。
- 在建造阶段，TensorRT 接收外部提供的网络定义(也可包含权值 weights)和超参数，根据当前编译的设备进行网络运行的优化(optimization), 并生成推理引擎 inference  engine(可以以 PLAN 形式存在在硬盘上)；
- 在执行阶段，通过运行推理引擎调用 GPU 计算资源——整个流程如图
[原文链接](https://blog.csdn.net/weixin_39875161/article/details/99084743)

![](https://img-blog.csdnimg.cn/20190810162851400.png)

### TensorRT 接口

必备接口流程图
![](https://img-blog.csdnimg.cn/20210425232029160.png

TensorRT核心库中，最关键的几种接口类型有：
- IExecutionContext    推理引擎运行上下文
- ICudaEngine            推理引擎
- IRuntime                  CudaEngine反序列化
- INetWorkDefinition   网络定义
- IParser                     网络模型解析
- IOptimizationProfile 优化配置
- IBuilderConfig          CudaEngine的构造参数
- IBuilder                     构造器，主要用于构造CudaEngine
- ILogger                    日志接口，需要开发者实现

接口详情参考：[TensorRT入门](https://blog.csdn.net/Ango_/article/details/116140436)


### TensorRT的加速效果怎么样

加速效果取决于模型的类型和大小，也取决于所使用的显卡类型。

对于GPU来说，因为底层的硬件设计，更适合并行计算也更喜欢密集型计算。TensorRT所做的优化也是基于GPU进行优化，当然也是更喜欢那种一大块一大块的矩阵运算，尽量直通到底。因此对于通道数比较多的卷积层和反卷积层，优化力度是比较大的；如果是比较繁多复杂的各种细小op操作(例如reshape、gather、split等)，那么TensorRT的优化力度就没有那么夸张了。

为了更充分利用GPU的优势，我们在设计模型的时候，可以更加偏向于模型的并行性，因为同样的计算量，“大而整”的GPU运算效率远超“小而碎”的运算。

工业界更喜欢简单直接的模型和backbone。2020年的RepVGG，就是为GPU和专用硬件设计的高效模型，追求高速度、省内存，较少关注参数量和理论计算量。相比resnet系列，更加适合充当一些检测模型或者识别模型的backbone。

在实际应用中，老潘也简单总结了下TensorRT的加速效果：
- SSD检测模型，加速3倍(Caffe)
- CenterNet检测模型，加速3-5倍(Pytorch)
- LSTM、Transformer(细op)，加速0.5倍-1倍(TensorFlow)
- resnet系列的分类模型，加速3倍左右(Keras)
- GAN、分割模型系列比较大的模型，加速7-20倍左右(Pytorch)

### TensorRT有哪些黑科技

为什么TensorRT能够提升我们模型在英伟达GPU上运行的速度，当然是做了很多对提速有增益的优化：
- 算子融合(层与张量融合)：简单来说就是通过融合一些计算op或者去掉一些多余op来减少数据流通次数以及显存的频繁使用来提速
量化：量化即IN8量化或者FP16以及TF32等不同于常规FP32精度的使用，这些精度可以显著提升模型执行速度并且不会保持原先模型的精度
- 内核自动调整：根据不同的显卡构架、SM数量、内核频率等(例如1080TI和2080TI)，选择不同的优化策略以及计算方式，寻找最合适当前构架的计算方式
- 动态张量显存：我们都知道，显存的开辟和释放是比较耗时的，通过调整一些策略可以减少模型中这些操作的次数，从而可以减少模型运行的时间
- 多流执行：使用CUDA中的stream技术，最大化实现并行操作
TensorRT的这些优化策略代码虽然是闭源的，但是大部分的优化策略我们或许也可以猜到一些，也包括TensorRT官方公布出来的一些优化策略：

![](https://pic3.zhimg.com/80/v2-41d4cde8f1a25ffb0ed0ac22a4dcc782_720w.jpg)


### 什么模型可以转换为TensorRT

TensorRT官方支持Caffe、Tensorflow、Pytorch、ONNX等模型的转换(不过Caffe和Tensorflow的转换器Caffe-Parser和UFF-Parser已经有些落后了)，也提供了三种转换模型的方式：
- 使用TF-TRT，将TensorRT集成在TensorFlow中
- 使用ONNX2TensorRT，即ONNX转换trt的工具
- 手动构造模型结构，然后手动将权重信息挪过去，非常灵活但是时间成本略高，有大佬已经尝试过了：tensorrtx

不过目前TensorRT对ONNX的支持最好，TensorRT-8最新版ONNX转换器又支持了更多的op操作。而深度学习框架中，TensorRT对Pytorch的支持更为友好，除了Pytorch->ONNX->TensorRT这条路，还有：
- torch2trt
- torch2trt_dynamic
- TRTorch

总而言之，理论上95%的模型都可以转换为TensorRT，条条大路通罗马嘛。只不过有些模型可能转换的难度比较大。如果遇到一个无法转换的模型，先不要绝望，再想想，再想想，看看能不能通过其他方式绕过去。

### TensorRT支持哪几种权重精度

支持FP32、FP16、INT8、TF32等，这几种类型都比较常用。
- FP32：单精度浮点型，没什么好说的，深度学习中最常见的数据格式，训练推理都会用到；
- FP16：半精度浮点型，相比FP32占用内存减少一半，有相应的指令值，速度比FP32要快很多；
- TF32：第三代Tensor Core支持的一种数据类型，是一种截短的 Float32 数据格式，将FP32中23个尾数位截短为10bits，而指数位仍为8bits，总长度为19(=1+8 +10)。保持了与FP16同样的精度(尾数位都是 10 位），同时还保持了FP32的动态范围指数位都是8位)；
- INT8：整型，相比FP16占用内存减小一半，有相应的指令集，模型量化后可以利用INT8进行加速。
简单展示下各种精度的区别：
![](https://pic2.zhimg.com/80/v2-e86c8661901842ffaf960bb2abbe37e9_720w.jpg)

## ZeRO -- 突破显存限制

### ZeRO: 去除冗余

目前最流行的方法是 `ZeRO`（即零冗余优化器）。针对模型状态的存储优化（去除冗余），ZeRO使用的方法是**分片**，即每张卡只存 1/N 的模型状态量，这样系统内只维护一份模型状态。

ZeRO有三个不同级别，对模型状态进行不同程度的分片：
- ZeRO-1: 对**优化器状态**分片（Optimizer States Sharding）
- ZeRO-2: 对**优化器状态**和**梯度**分片（Optimizer States & Gradients Sharding）
- ZeRO-3: 对**优化器状态**、**梯度**分片以及**模型权重参数**分片（Optimizer States & Gradients & Parameters Sharding）
- ![img](https://mmbiz.qpic.cn/mmbiz_png/J0mLianhFicBHEDwE5nPHZKaicqsXBVgES5rYysbjp9PYV3E8JOgU4ZZmyVBDUeryCQpvUBAUu6bGcUico0UWE9uIQ/640?wx_fmt=png&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1)

`ZeRO`（Zero Redundancy Optimizer）由NVIDIA开发的分布式深度学习训练技术，解决在大规模模型上训练时由于**显存限制**而导致的性能瓶颈问题。

传统分布式训练中，每个工作节点都必须存储完整的**模型参数副本**，使用大型模型时，每个工作节点需要拥有足够的显存才能存储这些参数。

而ZeRO技术通过将模型参数分成多个**分片**，让每个工作节点只需要存储部分参数，从而显著减少了显存占用量。
 
具体而言，ZeRO技术通过以下三个主要组件实现：
1.  ZeRO-Stage：将模型参数划分为**更小的分片**，每个工作节点只需存储自己所负责的参数分片。
2.  ZeRO-Offload：将一部分模型参数存储在**CPU内存**中，从而释放显存空间。
 
通过使用ZeRO技术，可以大幅度提高分布式深度学习训练的效率和规模。同时，由于减少了显存占用量，还可以使用更大的批量大小，从而加速训练过程。

除了ZeRO 外还有 Megatron，Gpip 和 Mesh-TensorFlow 等分布式深度计算方式

另外[FlagAI](https://github.com/FlagAI-Open/FlagAI)也集成了ZeRO的使用方式，具体实现方式使用的是利用[Deepspeed](https://github.com/FlagAI-Open/FlagAI/blob/master/examples/glm_seq2seq/train_deepspeed.py)实现ZeRO1和ZeRO2，利用[bmtrain](https://github.com/FlagAI-Open/FlagAI/blob/master/examples/glm_pretrain/train_bmtrain.py)实现了ZeRO3。
 
> FlagAI 由北京智源人工智能研究院于 2022 年 5 月开源，是大模型算法、模型及各种优化工具的一站式、高质量开源项目，旨在集成全球各种主流大模型算法技术，以及多种大模型并行处理和训练加速技术，支持高效训练和微调，降低大模型开发和应用的门槛，提高大模型的开发效率。项目地址：[https://github.com/FlagAI-Open/FlagAI](https://github.com/FlagAI-Open/FlagAI)

【2023-4-5】参考：[模型并行下利用ZeRO进行显存优化](https://zhuanlan.zhihu.com/p/619429610)
 
### ZeRO-Stage

zero_stage
- 论文: [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054)
- 核心目的：怎么优化训练方式和(GPU, TPU, CPU)硬件使用效率，让用户训练transformers类的大模型更加高效。

ZeRO将模型训练阶段，每张卡中显存内容分为两类：
1.  **模型状态**（model states）: 模型参数（fp16）、模型梯度（fp16）和Adam状态（fp32的模型参数备份，fp32的momentum和fp32的variance）。假设模型参数量 Φ ，则共需要 2Φ+2Φ+(4Φ+4Φ+4Φ)=4Φ+12Φ=16Φ 字节存储，可以看到，Adam状态占比 75% 。
2.  **剩余状态**（residual states）: 除了模型状态之外的显存占用，包括激活值（activation）、各种临时缓冲区（buffer）以及无法使用的显存碎片（fragmentation）。
 
针对模型状态的存储优化（去除冗余），ZeRO使用的方法是分片（partition），即每张卡只存 1/N 的模型状态量，这样系统内只维护一份模型状态。
*   首先进行分片操作的是模型状态中的Adam，也就是图5中的 Pos ，这里os指的是optimizer states。模型参数（parameters）和梯度（gradients）仍旧是每张卡保持一份，此时，每张卡的模型状态所需显存是 4Φ+12Φ/N 字节，当 N 比较大时，趋向于 4ΦB ，也就是原来 16ΦB 的 1/4 。
*   如果继续对模型梯度进行分片，也就是图5中的 Pos+g ，模型参数仍旧是每张卡保持一份，此时，每张卡的模型状态所需显存是 2Φ+(2Φ+12Φ)/N 字节，当 N 比较大时，趋向于 2ΦB ，也即是原来 16ΦB 的 1/8 。
*   如果继续对模型参数进行分片，也就是图5中的 Pos+g+p ，此时每张卡的模型状态所需显存是 16Φ/N 字节，当 N 比较大时，趋向于 0 。

分析下通信数据量，先说结论：
- Pos 和 Pos+g 的通信量和传统数据并行相同，Pos+g+p 会增加通信量。

传统数据数据并行在每一步（step/iteration）计算梯度后，需要进行一次AllReduce操作来计算梯度均值，目前常用的是Ring AllReduce，分为ReduceScatter和AllGather两步，每张卡的通信数据量（发送+接收）近似为 2Φ (\[2\])。
 
直接分析 Pos+g ，每张卡只存储 1N 的优化器状态和梯度，对于 gpu0 来说，为了计算它这 1N 梯度的均值，需要进行一次Reduce操作，通信数据量是 1/N⋅Φ⋅N=Φ ，然后其余显卡则不需要保存这部分梯度值了。实现中使用了bucket策略，保证 1N 的梯度每张卡只发送一次。
 
当 gpu0 计算好梯度均值后，就可以更新局部的优化器状态（包括 1/N⋅Φ 的参数），当反向传播过程结束，进行一次Gather操作，更新 (1−1/N)Φ 的模型参数，通信数据量是 1/N⋅Φ⋅N=Φ 。
 
从全局来看，相当于用Reduce-Scatter和AllGather两步，和数据并行一致，使得每张卡只存了 1/N 的参数，不管是在前向计算还是反向传播，都涉及一次Broadcast操作。
- ![](https://pic2.zhimg.com/80/v2-e28e1ca08f66f19d45a98af3fbfa13e9_1440w.webp)

解决了模型状态，再来看剩余状态，也就是激活值（activation）、临时缓冲区（buffer）以及显存碎片（fragmentation）。
*   激活值同样使用分片方法，并且配合checkpointing
*   模型训练过程中经常会创建一些大小不等的临时缓冲区，比如对梯度进行AllReduce啥的，解决办法就是预先创建一个固定的缓冲区，训练过程中不再动态创建，如果要传输的数据较小，则多组数据bucket后再一次性传输，提高效率
*   显存出现碎片的一大原因是时候gradient checkpointing后，不断地创建和销毁那些不保存的激活值，解决方法是预先分配一块连续的显存，将常驻显存的模型状态和checkpointed activation存在里面，剩余显存用于动态创建和销毁discarded activation

### ZeRO-Offload
 
ZeRO-Offload 是 ZeRO（Zero Redundancy Optimizer）技术的一种**扩展**，它使用显存作为模型参数存储和通信的中间介质，以减少模型并行化训练中的通信和同步开销。
 
ZeRO-Offload技术使用显存缓存将模型参数存储在显存中，这可以减少网络带宽的使用，同时还可以加速参数访问和更新。为了最大限度地减少显存的使用，ZeRO-Offload技术使用了一种称为“按需加载”的策略。这种策略只在需要使用参数时才将其从磁盘或网络加载到显存中，而不是一次性将所有参数都加载到显存中。
- ![](https://pic4.zhimg.com/80/v2-e83a35c1d2a1db0738cc19770be60207_1440w.webp)
 

Offload策略
 
ZeRO-Offload技术的核心是使用显存缓存和显存内通信来降低通信开销。为了最大程度地利用显存并减少网络带宽的使用，ZeRO-Offload技术采用了一种称为“Offload策略”的技术。下面是ZeRO-Offload技术的Offload策略的几个关键点：
1.  按需加载
  - ZeRO-Offload技术使用“按需加载”策略，只在需要使用参数时才将其从磁盘或网络加载到显存中，而不是一次性将所有参数都加载到显存中。这种策略可以最大限度地减少显存的使用，并减少网络带宽的使用。
2. 数据流水线
  - ZeRO-Offload技术使用“数据流水线”策略，将数据流分成多个阶段，每个阶段都使用不同的计算资源进行处理。在模型训练期间，ZeRO-Offload技术将数据分为多个块，并将这些块分配给不同的GPU进行计算。每个GPU只对其分配的数据块进行计算，并将计算结果传递给下一个阶段的GPU，直到所有阶段都完成为止。
3. 显存原语
  - ZeRO-Offload技术使用一种称为“显存原语”的通信协议，在显存中直接进行通信和同步操作，而不需要通过网络或主机内存。这种协议可以显著减少通信延迟和数据传输时间，从而提高训练效率。
4. 数据切片
  - ZeRO-Offload技术使用“数据切片”策略来划分模型参数，并通过显存内通信来实现不同GPU上参数的同步。具体来说，ZeRO-Offload技术将模型参数划分为多个小块，并在每个GPU上存储一部分参数块。在训练过程中，每个GPU只对其分配的参数块进行计算，并通过显存内通信将参数块传输到其他GPU上进行同步。

总的来说，ZeRO-Offload技术的Offload策略通过按需加载、数据流水线、显存原语和数据切片等技术手段来最大化地利用显存，并降低通信开销，从而提高深度学习模型训练的效率和可扩展性。
 
为了找到最优的offload策略，ZeRO作者将模型训练过程看作数据流图（data-flow graph）。
*   圆形节点表示模型状态，比如参数、梯度和优化器状态
*   矩形节点表示计算操作，比如前向计算、后向计算和参数更新
*   边表示数据流向
 
下图是某一层的一次迭代过程（iteration/step），使用了混合精读训练，前向计算（FWD）需要用到上一次的激活值（activation）和本层的参数（parameter），反向传播（BWD）也需要用到激活值和参数计算梯度，
- ![](https://pic3.zhimg.com/80/v2-6a6ae5248f45f1d59fb28aa1369e5f06_1440w.webp)

如果用Adam优化器进行参数更新（Param update），流程如下：
- ![](https://pic1.zhimg.com/80/v2-fb39f875d3a73901b8501cea18630ff0_1440w.webp)

为边添加权重，物理含义是数据量大小（单位是字节），假设模型参数量是 M ，在混合精度训练的前提下，边的权重要么是2M（fp16），要么是4M（fp32）。
- ![](https://pic1.zhimg.com/80/v2-26950ad74ab06e57222caa18c1af3214_1440w.webp)

现在要做的就是沿着边把数据流图切分为两部分，分布对应GPU和CPU，计算节点（矩形节点）落在哪个设备，哪个设备就执行计算，数据节点（圆形）落在哪个设备，哪个设备就负责存储，将被切分的边权重加起来，就是CPU和GPU的通信数据量。
 
ZeRO-Offload的切分思路如图 10 所示：
- ![](https://pic1.zhimg.com/80/v2-a5ded60ef49d1c2e9a0b9f8cf7ae29a8_1440w.webp)

图10中有四个计算类节点：FWD、BWD、Param update和float2half，前两个计算复杂度大致是 O(MB) ， B 是batch size，后两个计算复杂度是 O(M) 。为了不降低计算效率，将前两个节点放在GPU，后两个节点不但计算量小还需要和Adam状态打交道，所以放在CPU上，Adam状态自然也放在内存中，为了简化数据图，将前两个节点融合成一个节点FWD-BWD Super Node，将后两个节点融合成一个节点Update Super Node。
 
所以，现在的计算流程是，在GPU上面进行前向和后向计算，将梯度传给CPU，进行参数更新，再将更新后的参数传给GPU。为了提高效率，可以将计算和通信并行起来，GPU在反向传播阶段，可以待梯度值填满bucket后，一遍计算新的梯度一遍将bucket传输给CPU，当反向传播结束，CPU基本上已经有最新的梯度值了，同样的，CPU在参数更新时也同步将已经计算好的参数传给GPU，如下图所示：
- ![](https://pic3.zhimg.com/80/v2-bac2b7d030141b2a146852a44d5c379a_1440w.webp)

### ZeRO 问题

【2023-7-6】[DeepSpeed-ZeRO++ 技术简介](https://zhuanlan.zhihu.com/p/641297077)

ZeRO 是一种数据并行策略，将**模型权重**、**梯度**以及**优化器状态**分别切分到各GPU上，从而可在有限的显存上训练更大的模型。
- 模型**前向计算**和**反向计算**都需要提前聚合当前层对应的**全量参数**，这个聚合过程是通过调用**通信原语** `All-Gather` 来完成的；
- 之后便需要对计算好的**梯度平均**，把平均后的梯度值传播到各 GPU 上，用于各 GPU 更新自己负责的那一部分模型权重，这个平均以及传播的过程通过调用通信原语 `Reduce-Scatter` 完成。

至此完成一步迭代， ZeRO 通信量以及通信频率都大幅增长
- 普通数据并行只需要对最后计算出的梯度做一次 All-Reduce 通信，而ZeRO需要两次 All-Gather 通信 + 一次 Reduce-Scatter 通信。
- 如果机器集群节点间的网络带宽再拉跨一些，那么 ZeRO 的训练效率简直不堪入目。

因此，很多大模型都基于`张量并行`和`流水并行`对模型进行精细切分，让一些频繁通信的操作（张量并行）尽量限制在节点内部，同时把通信压力小的操作放在节点间完成，比如流水并行。


### ZeRO++

【2023-7-6】[DeepSpeed-ZeRO++ 技术简介](https://zhuanlan.zhihu.com/p/641297077)

ZeRO 为了打一个翻身仗，不得不优化自己的短板，减少**跨机通信**，进而提升训练效率，具体优化策略也就是本文将要介绍的 `ZeRO++`。
1.  `量化权重`（qwZ）：前向计算时，在 All-Gather 通信之前，首先把 FP16（两字节） 权重量化成 INT8（单字节），这样一来通信数据量就下降了一半；Al-Gather 通信之后，再通过反量化将 INT8 反量化成 FP16。为了取得更好的量化效果，也就是尽量减小量化损失，ZeRO+ 使用 Blocked Quantization 代替朴素的量化策略，如下图（a）是两种量化策略的对比，Blocked Quantization 相比于 Baseline 具有更小的量化误差；下图（b）说明 Block 切得越多，欧式距离越小，量化损失也就越小，但是也会带来额外的开销（scale 和 zero）；
  - ![qwZ](https://pic1.zhimg.com/80/v2-37b936d22b0f545123ecb731431c7fb8_1440w.webp)
2. `分层切片`（hpZ）：由于 ZeRO 把整个模型权重切分到所有的 GPU 上，所以反向计算梯度时需要所有 GPU 参与通信，把权重分片聚拢起来，但是节点间的网络带宽远远小于节点内部，导致节点间通信成为瓶颈。为了缓解这个问题，ZeRO++ 采用分层切片的策略尽量减少反向计算时的跨节点通信。具体过程如下：已知前向计算时会把所有权重 All-Gather 起来，之后便对权重进行切片，切成多少片可以根据集群配置进行调节，一般情况下会把权重切片尽量限制在单个节点内部，也就是一个节点有多少张卡，就切成多少片，这样一来每个节点都拥有完整的权重，在反向计算梯度时只需要在节点内部执行 All-Gather 通信，完全避免了跨节点的通信。
  - ![hpZ：通信分析](https://pic3.zhimg.com/80/v2-d41d3c890d35fa89c866b0909d12ac1e_1440w.webp)
  - 额外开销便是每张卡不仅要保存 ZeRO 的权重切片（Primary Parameters），还需要额外保存 ZeRO++ 所需的权重切片（Secondary Parameters），如下图所示：
  - ![hpZ：显存分析](https://pic4.zhimg.com/80/v2-db2f025b83b406341a26ae61307d55c3_1440w.webp)
3. `量化梯度`（qgZ）：ZeRO 在反向计算完成之后需要一次 Reduce-Scatter 通信，如果直接将量化策略应用到 Reduce-Scatter 通信原语，会造引发一系列的量化和反量化（量化和反量化的次数为所有 GPU 的个数），这不可避免地会引入巨大的量化误差，如下图左所示：
  - ![Ring-based Reduce-Scatter vs 1-hop All-to-All](https://pic1.zhimg.com/80/v2-b2cc2b10dcbd9e6f82d0b99ae261fd34_1440w.webp)

为了减少量化和反量化的次数（Q+D），可如上图右所示，首先对全部梯度量化，然后所有 GPU 进行一次 All-to-All 通信，最后执行反量化操作。这个过程只需一次量化和反量化操作，因此也被称作 1-hop all-to all。下面分析一下这两种方法的通信量：
  - ![ZeRO-3 和 1-hop all-to-all 通信分析](https://pic4.zhimg.com/80/v2-a95ae05ede2d28ccee070a26ffd2e983_1440w.webp)

从上图可以看出，基于 Reduce-Scatter 的 ZeRO3 跨机通信量为 M，而基于 1-hop all-to-all 的算法跨机通信量为 N * M / Z（其中 Z 为压缩比率，比如 FP16 量化为 INT8，也就是从 2 个字节压缩成 1 个字节，因此压缩比率为 2；由于每张卡都要发送压缩后的数据，所以需要对压缩后的数据乘上 N）。相比于 Reduce-Scatter，1-hop all-to-all 的跨机通信总量大幅增加，因此需要进一步优化以减少跨机通信数据量。ZeRO++ 提出基于分层策略的 2-hop all-to-all 算法：
- Step1: Tensor Slice Reordering（张量切片重排），重排的原因稍后解释，重排后进行量化（Quantizaiton），然后在节点内执行 All-to-All 通信：
  - ![Tensor Slice Reordering & Intra-node All-to-All Communication](https://pic2.zhimg.com/80/v2-a8457d15194cca81b41e3ca22571c6b9_1440w.webp)
- Step2：在各个节点内部首先执行反量化（Dequantization），然后把反量化的结果相加（Reducetion），减小精度损失：
  - ![第一次 Dequatization & Reduction](https://pic2.zhimg.com/80/v2-13ada2da38d498936439f015e70486f1_1440w.webp)
- Step3：执行 Reduction 之后，再次对张量进行量化（Quantization），然后对量化后的结果执行第二次 All-to-All 通信，只不过这一次是节点间（以下图为例：Machine 0 的 G2 和 Machine 1 的 G2，Machine 0 的 G3 和 Machine 1 的 G3）：
  - ![Quantization & Inter-node All-to-All](https://pic4.zhimg.com/80/v2-6878bf781ce9e8a48e8228591efe5467_1440w.webp)
- Step4：节点间 All-to-All 通信之后，首先进行反量化（Dequantization），然后执行 Reduction 操作，这时每张卡上都拿到了权重（Primary Parameters）对应的、平均后的梯度：
  - ![第二次 Dequantization & Reduction](https://pic4.zhimg.com/80/v2-96f9e09778de820782883c25dff39b93_1440w.webp)

至此，qgZ 通过使用节点内和节点间的 All-to-All 通信，同时搭配 Tensor Slice Reordering，来模拟实现了 Reduce-Scatter 通信，这个过程共执行两次量化和反量化，因此也被称为 2-hop all-to-all。
 
现在解释最开始对张量切片进行重排的原因：
  - ![左一左二（未重排）& 右一右二（重排）](https://pic2.zhimg.com/80/v2-577f49d2bffdcd30409e4e8ee9584a29_1440w.webp)
  - 左面两图（Step1 & Step2）没有使用张量切片重排，两次 ALL-to-ALL 通信之后，每张卡上的张量切片无法与正确的切片顺序对齐。为了避免这一问题，应该首先对张量切片进行重排，再进行 All-to-All 通信。

至此，已经完整介绍前向通信优化（qwZ），反向通信优化（hpZ），以及梯度通信优化（qgZ）。节点间通信量如下图：
- ![节点间通信量对比](https://pic4.zhimg.com/80/v2-b92559e88d7f7105e37113fbc72da717_1440w.webp)

相比于 ZeRO，ZeRO++在前向时量化权重节省了一半的跨机通信量（PF16 -> INT8），后向时由于权重都已经存在本地节点，所以跨机通信量为 0，最后的梯度同步可减少 3/4 跨机通信量：
- ![qgZ 2-hop all-to-all 跨机通信分析](https://pic1.zhimg.com/80/v2-ba73eb365b71eb11ce31286d8bea7894_1440w.webp)

第一次 All-to-All 通信之后，总参数量从 M/Z 降到 M / (Z * N)，其中 N 为每个节点的 GPU 个数；第二次 All-to-All 通信每张卡发送的数据量为 M / ( Z * N)，那么每台机器的跨机通信量就是 M / (Z * N) * N），也就是 M / Z（FP16 -> INT4，所以是 0.25M）。

最后再讲一下论文里面提到的实现优化，这一步对于效率影响很大，共涉及两个优化点：
- （1）通信和计算隐藏：针对 All-Gather，当前层在聚拢权重（通信）时，同时对下一层的权重进行量化（计算）；针对 2-hop all-to-all，首先对张量分块，再分别执行通信，可实现不同块之间的通信计算隐藏，如下图所示：
  - ![Pipeline and Overlapping](https://pic1.zhimg.com/80/v2-f1b2673cb035e26a635ee9513b37e9ac_1440w.webp)
- （2）融合算子：优化目标有两个：最大化带宽利用率和最小化内存读写。



## 大模型推理加速

模型推理优化三个层面：[参考](https://mp.weixin.qq.com/s/7wtwsNhf27YzALnSFXTmkA)
- 算法层面：蒸馏、量化
- 软件层面：计算图优化、模型编译
- 硬件层面：FP8（NVIDIA H系列GPU开始支持FP8，兼有fp16的稳定性和int8的速度）

### 加速框架

推理加速框架：
- `FasterTransformer`：英伟达推出的FasterTransformer不修改模型架构而是在计算加速层面优化 Transformer 的 encoder 和 decoder 模块。具体包括如下：
  - 尽可能多地融合除了 GEMM 以外的操作
  - 支持 FP16、INT8、FP8
  - 移除 encoder 输入中无用的 padding 来减少计算开销
- `TurboTransformers`：腾讯推出的 TurboTransformers 由 computation runtime 及 serving framework 组成。加速推理框架适用于 CPU 和 GPU，最重要的是，它可以无需预处理便可处理变长的输入序列。具体包括如下：
  - 与 FasterTransformer 类似，它融合了除 GEMM 之外的操作以减少计算量
  - smart batching，对于一个 batch 内不同长度的序列，它也最小化了 zero-padding 开销
  - 对 LayerNorm 和 Softmax 进行批处理，使它们更适合并行计算
  - 引入了模型感知分配器，以确保在可变长度请求服务期间内存占用较小


# 结束