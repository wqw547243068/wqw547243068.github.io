---
layout: post
title:  "分布式训练及推理加速"
date:   2024-03-05 19:25:00
categories: 大模型
tags: GPU Tensorflow Pytorch 并行计算 加速 分布式 tensorrt 推理加速 onnx zero lpu cuda gemm huggingface
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

## 分布式训练范式


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
- 收集 collective communication（`CC`）提供了scatter/broadcast/gather/reduce/all_reduce/all_gather 语义，不同的backend在提供的通信语义上具有一定的差异性。

训练大模型主要是CC通信

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

### 并行技术

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

### 多维混合并行 （3D并行）

- 多维混合并行(3D并行)指将`数据并行`、`模型并行`和`流水线并行`结合起来进行分布式训练。
- 超大规模模型的预训练和全参数微调时，都需要用到多维混合并行。


## 模型架构

**专家混合**（MoE）方法最近吸引了很多关注，因为研究人员（主要来自谷歌）试图突破模型大小的限制。该想法的核心是整合学习：多个弱学习模型组合以后会形成能力出众的学习模型。

Shazeer 等人于2017年发表了名为“稀疏门控专家混合”（MoE）层的文章，提出了在一个深度神经网络中可以通过连接多个专家的门控机制来实现输出控制的方法。


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
- 每个阶段（stage） 和下一个阶段之间仅有相邻的某一个 Tensor 数据需要传输，每台机器的数据传输量跟总的网络大小、机器总数、并行规模无关。

![](https://pic1.zhimg.com/80/v2-bdb9a12c01204d335187f6e3e3aad284_1440w.webp)

**流水线并行**（Pipeline model parallesim）
- 朴素拆分方式: 将模型各层分组后装载到各个GPU上，GPU之间进行**串行**计算
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

torch.nn.DataParallel
- DataParallel 全程维护一个 optimizer，对各 GPU 上梯度进行求和，而在主 GPU 进行参数更新，之后再将模型参数 broadcast 到其他 GPU

注意：
- 1、设置DistributedSampler来打乱数据，因为一个batch被分配到了好几个进程中，要确保不同的GPU拿到的不是同一份数据。
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
- `group`：即**进程组**。默认只有一个组，一个 job 即为一个组，即一个 world。
  - 当需要进行更加精细的通信时，通过 new_group 接口，使用 word 的子集，创建新组，用于集体通信等。
- `world_size` ：表示**全局进程个数**。
- `rank`：表示**进程序号**，用于进程间通讯，表征进程优先级。取值范围: `0~world_size`
  - `rank = 0` 主机为 **master 节点**。
- `local_rank`：进程内，**GPU 编号**，非显式参数，由 `torch.distributed.launch` 内部指定。
  - `rank = 3`，`local_rank = 0` 表示第 3 个进程内的第 1 块 GPU。

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


#### 初始化进程组

`init_process_group` 函数原型

```py
torch.distributed.init_process_group(backend, init_method=None, timeout=datetime.timedelta(0, 1800), 
                                     world_size=-1, rank=-1, store=None)
```

函数作用
- 每个进程中进行调用，用于初始化该进程。在使用分布式时，该函数必须在 distributed 内所有相关函数之前使用。

参数详解
- `backend` ：指定当前进程要使用的通信后端
  - 小写字符串，支持的通信后端有 gloo，mpi，nccl 。建议用 nccl。
- `init_method` ：指定当前进程组初始化方式
  - 可选参数，字符串形式。如果未指定 init_method 及 store，则默认为 env://，表示使用读取环境变量的方式进行初始化。该参数与 store 互斥。
- `rank` ：指定当前进程的优先级
- `int` 值。表示当前进程的编号，即优先级。如果指定 store 参数，则必须指定该参数。
  - rank=0 的为主进程，即 master 节点。
- `world_size` ：该 job 中的总进程数。如果指定 store 参数，则需要指定该参数。
- `timeout` ： 指定每个进程的超时时间
  - 可选参数，datetime.timedelta 对象，默认为 30 分钟。该参数仅用于 Gloo 后端。
- `store`
  - 所有 worker 可访问的 key / value，用于交换连接 / 地址信息。与 init_method 互斥。

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

#### (1) TCP 初始化

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

#### (2) 共享文件初始化

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

#### (3) Env 初始化(默认)

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

### Torchrun (更新)

Pytorch 1.9.0 引入了 `torchrun`，替代 1.9.0 以前版本 `torch.distributed.launch`。
- [torchrun](https://pytorch.org/docs/stable/elastic/run.html#launcher-api) 是 `torch.distributed.launch` 的超集, elastic launch, 等效于 `python -m torch.distributed.run`
- [torchrun](https://pytorch.org/docs/stable/elastic/run.html#launcher-api) 包含 `torch.distributed.launch` 几乎所有功能(除了废弃的`--use-env`)

还有三点额外功能：
- 1、worker rank 和 world_size 将被自动分配
- 2、`Failover`: worker失败时, 重新启动所有workers来处理workers的故障
- 3、`Elastic`: 动态增减节点, 允许节点数目在最大/最小值之间改变, 即具备弹性

#### 迁移 torch.distributed.launch->torchrun

迁移方法

```sh
python -m torch.distributed.launch -> torchrun
# (1) 如果 从环境变量(LOCAL_RANK)中读取 local_rank 参数, 直接忽略
# 更改前
python -m torch.distributed.launch --use-env train_script.py
# 更改后
torchrun train_script.py
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

Pytorch 1.x **多机多卡**计算模型没有采用主流的 Parameter Server 结构，而是直接用了Uber Horovod 的形式，即百度开源的 RingAllReduce 算法

Uber 的 Horovod 采用 RingAllReduce 计算方案，特点：网络单次通信量不随着 worker(GPU) 的增加而增加，是一个恒定值。

与 TreeAllReduce 不同，RingAllreduce 算法的每次通信成本是恒定的，与系统中 gpu 的数量无关，完全由系统中 gpu 之间最慢的连接决定。

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

详见站内专题: [DeepSpeed](deepspeed)


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


### Trainer


Trainer 名称歧义
- PyTorch Lightning有个 Trainer
- HuggingFace Transformers也有 Trainer
- 还有一些github上封装的或者基于这两个继续封装的Trainer

这里的 Trainer 指 Huggingface 的 Trainer 训练框架

Trainer 介于原生 torch 和 pytorch-lighning 之间，是轻量级的辅助torch模型训练的utils，因为其实稍微改造一下，huggingface的trainer 可用来训练常规的非nlp的torch模型。
- 封装程度: `torch` < `pytorch lightning` < `trainer`

Trainer 封装了 PyTorch 训练过程，包括：**前向传播**、**反向传播**和**参数更新**等步骤，用户只需要设计模型，调参就行

高级的 Trainer 加上了各种功能，比如：**日志记录**，**断点重训**，**训练方式**与**精度**，支持各种分布式训练框架像原生、Apex、Deepspeed和Fairscale，支持自定的回调函数等等

Lightning 官网的一张gif还是比较生动形象


#### Trainer 定义

[trainer.py](https://github.com/huggingface/transformers/blob/v4.34.1/src/transformers/trainer.py#L236)


do_train,do_eval,do_predict 这三个参数和trainer没什么关系


#### 自定义


##### model_init

model_init

```py
def model_init():
    model = AutoModelForSequenceClassification.from_pretrained(
        model_args.model_name_or_path,
        from_tf=bool(".ckpt" in model_args.model_name_or_path),
        config=config,
        cache_dir=model_args.cache_dir,
        revision=model_args.model_revision,
        use_auth_token=True if model_args.use_auth_token else None
    )
    return model
```


##### compute_metrics

```py
def compute_metrics(p: EvalPrediction) -> Dict:
    preds,labels=p
    preds = np.argmax(preds, axis=-1)
    #print('shape:', preds.shape, '\n')
    precision, recall, f1, _ = precision_recall_fscore_support(lables.flatten(), preds.flatten(), average='weighted', zero_division=0)
    return {
        'accuracy': (preds == p.label_ids).mean(),
        'f1': f1,
        'precision': precision,
        'recall': recall
    }
```

##### 加权loss

分类任务中，类目不均衡时，采用加权loss

做法
- (1) 继承 Trainer 类, 重定义 compute_loss 函数
- (2) 使用回调函数 [callback](https://huggingface.co/docs/transformers/v4.34.1/en/main_classes/callback)

示例
- 三分类问题，各类目加权 1 : 2 : 3

```py
from torch import nn
from transformers import Trainer

class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.pop("labels")
        # forward pass
        outputs = model(**inputs)
        logits = outputs.get("logits")
        # compute custom loss (suppose one has 3 labels with different weights)
        loss_fct = nn.CrossEntropyLoss(weight=torch.tensor([1.0, 2.0, 3.0], device=model.device))
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss
```


#### 参数详解

[Trainer 官网文档](https://huggingface.co/docs/transformers/v4.34.1/en/main_classes/trainer#trainer)，版本为4.34.0

##### Trainer类 参数

Transformers Trainer类 参数：
- `model` (`PreTrainedModel` 或 `torch.nn.Module`, 可选)：训练、评估或预测的实例化模型
  - 如果不提供，必须传递一个 `model_init` 来初始化一个模型。
- `args` (TrainingArguments, 可选)：训练参数
  - 如果不提供，用 TrainingArguments 默认参数，其中 output_dir 设置为当前目录中的名为 "tmp_trainer" 的目录。
- `data_collator` (DataCollator, 可选)：用于从 train_dataset 或 eval_dataset 中构成batch的函数
  - 如果未提供tokenizer，将默认使用 default_data_collator()；如果提供，将使用 DataCollatorWithPadding 。
- `train_dataset` (torch.utils.data.`Dataset` 或 torch.utils.data.`IterableDataset`, 可选)：训练数据集
  - 如果是 torch.utils.data.Dataset，则会自动删除模型的 forward() 方法不接受的列。
- `eval_dataset` (Union[torch.utils.data.Dataset, Dict[str, torch.utils.data.Dataset]), 可选)：同上，评估数据集
  - 如果是字典，将对每个数据集进行评估，并在指标名称前附加字典的键值。
- `tokenizer` (PreTrainedTokenizerBase, 可选)：预处理数据的**分词器**
  - 如果提供，将在批量输入时自动对输入进行填充到最大长度，并会保存在模型目录下中，为了重新运行中断的训练或重复微调模型时更容易进行操作。
- `model_init` (Callable[[], PreTrainedModel], 可选)：模型实例化函数
  - 如果提供，每次调用 train() 时都会从此函数给出的模型的新实例开始。
- `compute_metrics` (Callable[`[EvalPrediction]`, Dict], 可选)：评估时**计算指标**的函数，必须接受 EvalPrediction 作为入参，并返回一个字典，其中包含了不同性能指标的名称和相应的数值，一般是准确度、精确度、召回率、F1 分数等。
- `callbacks` (TrainerCallback 列表, 可选)：自定义**回调函数**
  - 如果要删除使用的默认回调函数，要使用 Trainer.remove_callback() 方法。
- `optimizers` (Tuple[torch.optim.Optimizer, torch.optim.lr_scheduler.LambdaLR], 可选)：指定包含优化器和学习率调度器的元组（Tuple）
  - 元组的两个元素分别是**优化器**（torch.optim.Optimizer）和**学习率调度器**（torch.optim.lr_scheduler.LambdaLR），默认会创建一个基于AdamW优化器的实例，并使用 get_linear_schedule_with_warmup() 函数创建一个学习率调度器。
- `preprocess_logits_for_metrics` (Callable[[torch.Tensor, torch.Tensor], torch.Tensor], 可选)：指定函数，每次评估步骤（evaluation step）前，进入compute_metrics函数前对模型的输出 logits 进行**预处理**。
  - 接受两个张量（tensors）作为参数，一个是模型的输出 logits，另一个是**真实标签**（labels）。
  - 然后返回一个经过预处理后的 logits 张量，给到compute_metrics函数作为参数。



##### TrainingArguments 参数

args：超参数定义，trainer的重要功能，大部分训练相关的参数都是这里设置

TrainingArguments 有接近100个参数

TrainingArguments 参数
- `output_dir` (str)：模型checkpoint/最终结果的输出目录。
- `overwrite_output_dir` (bool, 可选，默认为 False)：如果设置为True，将**覆盖**输出目录中已存在的内容
  - 继续训练模型并且输出目录, 指向一个checkpoint目录。
- `do_train` (bool, 可选，默认为 False)：是否执行**训练**
  - 其实Trainer 不直接使用此参数，主要是用于写脚本时，作为if的条件来判断是否执行接下来的代码。
- `do_eval` (bool, 可选)：是否在验证集上进行**评估**，如果评估策略（evaluation_strategy）不是"no"，将自动设置为True。
  - 与do_train类似，不直接由Trainer使用，主要是用于写训练脚本。
- `do_predict` (bool, 可选，默认为 False)：是否在测试集上**预测**。
- `evaluation_strategy` (str, 可选，默认为 "no")：指定训练期间采用的评估策略，可选值包括：
  - "no"：在训练期间不进行任何评估。
  - "steps"：每隔 eval_steps 步骤进行评估。
  - "epoch"：每个训练周期结束时进行评估。
- `prediction_loss_only` (bool, 可选, 默认为 False)：
  - 如果设置为True，评估和预测时，只返回**损失值**，而不返回其他评估指标。
- `per_device_train_batch_size` (int, 可选, 默认为 8)：**训练**阶段，每个GPU/XPU/TPU/MPS/NPU/CPU的batch，每个训练步骤中每个硬件上的样本数量。
- `per_device_eval_batch_size` (int, 可选, 默认为 8)：**评估**阶段的每个GPU/XPU/TPU/MPS/NPU/CPU的batch，每个评估步骤中每个硬件上的样本数量。
- `gradient_accumulation_steps` (int, 可选, 默认为 1)：执行反向传播之前，**梯度积累的更新步数**。
  - 梯度积累可以在多个batch上累积梯度，然后一次性执行反向传播，显存不够的情况下执行大batch的反向传播。
  - 假设4张卡，每张卡的batch size为8，那么一个steps的batch size就是32，如果这个参数设置为4，那么做反向传播的训练样本数量就是128。
  - 两个好处：①显存不够增大此参数；②能加快训练速度，毕竟做反向传播的次数少了。
- `eval_accumulation_steps` (int, 可选)：执行评估时，模型会累积多少个预测步骤的输出张量，然后才从GPU/NPU/TPU移动到CPU上，默认是整个评估的输出结果将在GPU/NPU/TPU上累积，然后一次性传输到CPU，速度更快，但占显存。
- `eval_delay` (float, 可选)：等待执行第一次评估的轮数或步数。
  - 如果evaluation_strategy为"steps"，设置此参数为10，则10个steps后才进行首次评估。
- `learning_rate` (float, 可选, 默认为 5e-5)：AdamW优化器的**初始学习率**。
- `weight_decay` (float, 可选, 默认为 0)：**权重衰减**的值，应用在 AdamW 优化器所有层上，除了偏置（bias）和 Layer Normalization 层（LayerNorm）的权重上。
  - 权重衰减是一种**正则化**手段，通过向损失函数添加一个额外的项，来惩罚较大的权重值，有助于防止模型**过拟合**训练数据。
- `adam_beta1` (float, 可选, 默认为 0.9)：AdamW优化器的beta1超参数。
- `adam_beta2` (float, 可选, 默认为 0.999)：AdamW优化器的beta2超参数。
- `adam_epsilon` (float, 可选, 默认为 1e-8)：AdamW优化器的epsilon超参数。
- `max_grad_norm` (float, 可选, 默认为 1.0)：梯度剪裁的最大梯度范数，可以防止梯度爆炸，一般都是1，如果某一步梯度的L2范数超过了 此参数，那么梯度将被重新缩放，确保它的大小不超过此参数。
- `num_train_epochs` (float, 可选, 默认为 3.0)：训练的**总epochs数**。
- `max_steps` (int, 可选, 默认为 -1)：如果设置为正数，执行的总训练步数，会覆盖 num_train_epochs。
  - 注意：如果使用此参数，就算没有达到这个参数值的步数，训练也会在数据跑完后停止。
- `lr_scheduler_type` (str, 可选, 默认为"linear")：学习率scheduler类型，根据训练进程来自动调整学习率。详细见：
  - "linear"：**线性**学习率scheduler，学习率以线性方式改变
  - "cosine"：**余弦**学习率scheduler，学习率以余弦形状的方式改变。
  - "constant"：**常数**学习率，学习率在整个训练过程中保持不变。
  - "polynomial"：**多项式**学习率scheduler，学习率按多项式函数的方式变化。
  - "piecewise"：**分段常数**学习率scheduler，每个阶段使用不同的学习率。
  - "exponential"：**指数**学习率scheduler，学习率以指数方式改变。
- `warmup_ratio` (float, 可选, 默认为0.0)：线性热身占总训练步骤的比例，线性热身是一种训练策略，学习率在开始阶段从0逐渐增加到其最大值（通常是设定的学习率），然后在随后的训练中保持不变或者按照其他调度策略进行调整。如果设置为0.0，表示没有热身。
- `warmup_steps` (int,可选, 默认为0)：线性热身的步骤数，这个参数会覆盖warmup_ratio，如果设置了warmup_steps，将会忽略warmup_ratio。
- `log_level` (str, 可选, 默认为passive)：主进程上要使用的日志级别，
  - `debug`：最详细的日志级别。
  - `info`：用于一般的信息性消息。
  - `warning`：用于警告信息。
  - `error`：用于错误信息。
  - `critical`：用于严重错误信息。
  - `passive`：不设置任何内容，将会使用Transformers库当前的日志级别（默认为"warning"）。
  - 建议训练时使用info级别。
- `log_level_replica` (str, 可选, 默认为warning)：副本上要使用的日志级别，与log_level相同。
- `log_on_each_node` (bool, optional, defaults to True)：在多节点分布式训练中，是否在每个节点上使用log_level进行日志记录。
- `logging_dir` (str, 可选)：TensorBoard日志目录。默认为output_dir/runs/CURRENT_DATETIME_HOSTNAME。
- `logging_strategy` (str, 可选, 默认为"steps")：训练过程中采用的日志记录策略。可选包括：
  - "no"：在训练过程中不记录任何日志。
  - "epoch"：在每个epoch结束时记录日志。
  - "steps"：根据logging_steps参数记录日志。
- `logging_steps` (int or float,可选, 默认为500)：
  - 如果logging_strategy="steps"，则此参数为每多少步记录一次步骤。
- `logging_nan_inf_filter` (bool, 可选, 默认为 True)：是否过滤日志记录中为nan和inf的loss
  - 如果设置为True，将过滤每个步骤的loss，如果出现nan或inf，将取当前日志窗口的平均损失值。
- `save_strategy` (str , 可选, 默认为 "steps")：训练过程中保存checkpoint的策略，包括：
  - "no"：在训练过程中不保存checkpoint。
  - "epoch"：在每个epoch束时保存checkpoint。
  - "steps"：根据save_steps参数保存checkpoint。
- `save_steps` (int or float, 可选, 默认为500)：
  - 如果save_strategy="steps"，就是指两次checkpoint保存之间的更新步骤数。如果是在[0, 1)的浮点数，则就会当做与总训练步骤数的比例。
- `save_total_limit` (int, 可选)：如果给定了参数，将限制checkpoint的总数，因为checkpoint也是很占硬盘的，将会删除输出目录中旧的checkpoint。
  - 当启用load_best_model_at_end时，会根据metric_for_best_model保留最好的checkpoint，以及最近的checkpoint。
  - 当save_total_limit=5和指定load_best_model_at_end时，将始终保留最近的四个checkpoint以及最好的checkpoint；
  - 当save_total_limit=1和指定load_best_model_at_end时，会保存两个checkpoint：最后一个和最好的一个（如果不同一个）。
- `load_best_model_at_end` (bool, 可选, 默认为False)：是否在训练结束时，加载在训练过程中最好的checkpoint
  - 设置为 True 时，找到在验证集上指标最好的checkpoint并且保存，然后还会保存最后一个checkpoint
  - 在普通的多epoch训练中，最好设置为True
  - 但在大模型训练中，一般是一个epoch，使用的就是最后一个checkpoint。
- `save_safetensors` (bool, 可选, 默认为False)：是否在保存和加载模型参数时使用 "safetensors"
  - "safetensors" 更好地处理了不同 PyTorch 版本之间的模型参数加载的兼容性问题。
- `save_on_each_node` (bool, 可选, 默认为 False)：多节点分布式训练时，是否在每个节点上保存checkpoint，还是仅在主节点上保存。
  - 注意如果多节点使用的是同一套存储设备，比如都是外挂一个nas，开启后会报错，因为文件名称都一样。
- `use_cpu` (bool, 可选, 默认为 False)：是否用CPU训练。如果设置为False，将使用CUDA或其他可用设备。
- `seed` (int, 可选, 默认为42)：训练过程的随机种子，确保训练的可重现性，主要用于model_init，随机初始化权重参数。
- `data_seed` (int, 可选)：数据采样的随机种子，如果没有设置将使用与seed相同的种子，可以确保数据采样的可重现性。
- `jit_mode_eval` (bool, 可选, 默认为False)：是否在推理（inference）过程中使用 PyTorch 的 JIT（Just-In-Time）跟踪功能
  - PyTorch JIT 是 PyTorch 的一个功能，用于将模型的前向传播计算编译成高性能的机器代码，会加速模型的推理。
- `use_ipex` (bool, 可选, 默认为 False)：是否使用英特尔扩展（Intel extension）来优化 PyTorch，需要安装IPEX
  - IPEX是一组用于优化深度学习框架的工具和库，提高训练和推理的性能，特别针对英特尔的处理器做了优化。
- `bf16` (bool, 可选, 默认为False)：是否使用bf16进行混合精度训练，而不是fp32训练，需要安培架构或者更高的NVIDIA架构，关于精度的问题可以看这篇文章：Glan格蓝：LLM大模型之精度问题（FP16，FP32，BF16）详解与实践
  - 混合精度训练：模型训练时将模型参数和梯度存储为`fp32`，但在前向和后向传播计算中使用`fp16`，这样可以减少内存使用和计算时间，并提高训练速度。
- `fp16` (bool,** 可选, 默认为****False)**：是否使用fp16进行混合精度训练，而不是fp32训练。
- `fp16_opt_level` (str, 可选, 默认为 ''O1'')：对于fp16训练，选择的Apex AMP的优化级别，可选值有 ['O0', 'O1', 'O2'和'O3']。详细信息可以看Apex文档。
- `half_precision_backend` (str, 可选, 默认为"auto")：混合精度训练（Mixed Precision Training）时要使用的后端，必须是 "auto"、"cuda_amp"、"apex"、"cpu_amp" 中的一个。
  - "auto"将根据检测到的PyTorch版本来使用后端，而其他选项将会强制使用请求的后端。使用默认就行。
- `bf16_full_eval` (bool, 可选, 默认为 False)：是否使用完全的bf16进行评估，而不是fp32。这样更快且省内存，但因为精度的问题指标可能会下降。
- `fp16_full_eval` (bool, 可选, 默认为 False)：同上，不过将使用fp16.
- `tf32` (bool, 可选)：是否启用tf32精度模式，适用于安培架构或者更高的NVIDIA架构，默认值取决于PyTorch的版本torch.backends.cuda.matmul.allow_tf32 默认值。
- `local_rank` (int, 可选, 默认为 -1)：在分布式训练中的当前进程（本地排名）的排名，这个用户不用设置，使用PyTorch分布式训练时会**自动**设置，默认为自动设置。
- `ddp_backend` (str, 可选)：处理分布式计算的后端框架，用于多个计算节点协同工作以加速训练，处理模型参数和梯度的同步、通信等操作，可选值如下
  - "`nccl`"：这是 NVIDIA Collective Communications Library (NCCL) 的后端。
  - "`mpi`"：Message Passing Interface (MPI) 后端， 是一种用于不同计算节点之间通信的标准协议。
  - "`ccl`"：这是 Intel的oneCCL (oneAPI Collective Communications Library) 的后端。
  - "`gloo`"：这是Facebook开发的分布式通信后端。
  - "`hccl`"：这是Huawei Collective Communications Library (HCCL) 的后端，用于华为昇腾NPU的系统上进行分布式训练。
  - 默认会根据系统自动设置，一般是nccl。
- `tpu_num_cores` (int, 可选)：TPU上训练时，TPU核心的数量。
- `dataloader_drop_last` (bool, 可选, 默认为False)：是否丢弃最后一个不完整的batch，发生在数据集的样本数量不是batch_size的整数倍的时候。
- `eval_steps` (int or float, 可选)：如果evaluation_strategy="steps"，两次评估之间的更新步数，如果未设置，默认和设置和logging_steps相同的值，如果是在[0, 1)的浮点数，则就会当做与总评估步骤数的比例。
- `dataloader_num_workers` (int, 可选, 默认为 0)：数据加载时的子进程数量（仅用于PyTorch）, PyTorch的num_workers参数，0表示数据将在主进程中加载。
- `past_index` (int, 可选, 默认为 -1)：一些模型（如TransformerXL或XLNet）可用过去的隐藏状态进行预测，如果将此参数设置为正整数，Trainer将使用相应的输出（通常索引为2）作为过去状态，并将其在下一个训练步骤中作为mems关键字参数提供给模型，只针对一些特定模型。
- `run_name` (str, 可选)：训练运行（run）的字符串参数，与日志记录工具（例如wandb和mlflow）一起使用，不影响训练过程，就是给其他的日志记录工具开了一个接口，个人还是比较推荐wandb比较好用。
- `disable_tqdm` (bool, 可选)：是否禁用Jupyter笔记本中的~notebook.NotebookTrainingTracker生成的tqdm进度条，如果日志级别设置为warn或更低，则将默认为True，否则为False。
- `remove_unused_columns` (bool, 可选, 默认为True)：是否自动删除模型在训练时，没有用到的数据列，默认会删除，比如你的数据有两列分别是content和id，如果没有用到id这一列，训练时就会被删除。
- `label_names` (List[str], 可选)：在模型的输入字典中对应于标签（labels）的键，默认情况下不需要显式指定。
- `metric_for_best_model` (str, 可选)：与 load_best_model_at_end 结合使用，比较不同模型的度量标准，默认情况下，如果未指定，将使用验证集的 "loss" 作为度量标准，可使用accuracy、F1、loss等。
- `greater_is_better` (bool, 可选)：与 load_best_model_at_end 和 metric_for_best_model 结合使用，这个和上面的那个参数是对应的，那个指标是越大越好还是越小越好
  - 如果是loss, 越小越好，这个参数就会被设置为False；
  - 如果是accuracy，把这个值设为True。
- `ignore_data_skip` (bool, 可选，默认为False)：是否**断点训练**，即训练终止又恢复后，是否跳过之前的训练数据。
- `resume_from_checkpoint` (str, 可选)：从checkpoint恢复训练的路径。
- `sharded_ddp` (bool, str 或 ShardedDDPOption 列表, 可选, 默认为'')：是否在分布式训练中使用 Sharded DDP（Sharded Data Parallelism），FairScale提供的，默认不使用
  - FairScale 是Mate开发的一个用于高性能和大规模训练的 PyTorch 扩展库。这个库扩展了基本的 PyTorch 功能，同时引入了最新的先进规模化技术，通过可组合的模块和易于使用的API，提供了最新的分布式训练技术。详细的可以看其官网。
- `fsdp` (bool, str 或 FSDPOption 列表, 可选, 默认为'')：是否启用 PyTorch 的 `FSDP`（Fully Sharded Data Parallel Training），以及如何配置分布式并行训练。
- `fsdp_config` (str 或 dict, 可选)：配置 PyTorch 的 FSDP（Fully Sharded Data Parallel Training）的配置文件
- `deepspeed` (str 或 dict, 可选)：是否启用 DeepSpeed，以及如何配置 DeepSpeed。
  - 目前分布式训练使用最多的框架，比上面pytorch原生分布式训练以及FairScale用的范围更广，详细的可以看其官网。
- `label_smoothing_factor` (float, 可选，默认为0.0)：标签平滑的因子。
- `debug` (str 或 DebugOption 列表, 可选, 默认为'')：启用一个或多个调试功能,支持选项：
  - "underflow_overflow"：此选项用于检测模型输入/输出中的溢出。
  - "tpu_metrics_debug"：此选项用于在 TPU 上打印调试指标。
- `optim` (str 或 training_args.OptimizerNames, 可选, 默认为 "adamw_torch")：要用的优化器。可选项：
  - "adamw_hf"
  - "adamw_torch"
  - "adamw_torch_fused"
  - "adamw_apex_fused"
  - "adamw_anyprecision"
  - "adafactor"
- `optim_args` (str, 可选)：用于向特定类型的优化器（如adamw_anyprecision）提供额外的参数或自定义配置。
- `group_by_length` (bool, 可选, 默认为 False)：是否在训练数据集中对大致相同长度的样本进行分组然后放在一个batch里，目的是尽量减少在训练过程中进行的padding，提高训练效率。
- `length_column_name` (str, 可选, 默认为 "length")：当上个参数设置为True时，可以给训练数据在增加一列”长度“，就是事先计算好的，可以加快分组的速度，默认是length。
- `report_to` (str 或 str 列表, 可选, 默认为 "all")：要将训练结果和日志报告到的不同日记集成平台，有很多"azure_ml", "clearml", "codecarbon", "comet_ml", "dagshub", "flyte", "mlflow", "neptune", "tensorboard", and "wandb"。直接默认就行，都发。
- `ddp_find_unused_parameters` (bool, 可选)：使用分布式训练时，这个参数用于控制是否查找并处理那些在计算中没有被使用的参数，如果启用了**梯度检查点**（gradient checkpointing），表示部分参数是惰性加载的，这时默认值为 False，因为梯度检查点本身已经考虑了未使用的参数，如果没有启用梯度检查点，默认值为 True，表示要查找并处理所有参数，以确保它们的梯度被正确传播。
- `ddp_bucket_cap_mb` (int, 可选)：在分布式训练中，数据通常分成小块进行处理，这些小块称为"桶"，这个参数每个桶的最大内存占用大小，一般自动分配即可。
- `ddp_broadcast_buffers` (bool, 可选)：分布式训练中，模型的某些部分可能包含缓冲区，如 Batch Normalization 层的统计信息，这个参数用于控制是否将这些缓冲区广播到所有计算设备，以确保模型在不同设备上保持同步，如果启用了梯度检查点，表示不需要广播缓冲区，因为它们不会被使用，如果没有启用梯度检查点，默认值为 True，表示要广播缓冲区，以确保模型的不同部分在所有设备上都一致。
- `gradient_checkpointing` (bool, 可选, 默认为False)：是否开启梯度检查点，简单解释一下：训练大型模型时需要大量的内存，其中在反向传播过程中，需要保存前向传播的中间计算结果以计算梯度，但是这些中间结果占用大量内存，可能会导致内存不足，梯度检查点会在训练期间释放不再需要的中间结果以减小内存占用，但它会使反向传播变得更慢。
- `dataloader_pin_memory` (bool, 可选, 默认为 True)：dataloader加载数据时，是否启用“pin memory”功能。“Pin memory” 用于将数据加载到GPU内存之前，将数据复制到GPU的锁页内存（pinned memory）中，锁页内存是一种特殊的内存，可以更快地传输数据到GPU，从而加速训练过程，但是会占用额外的CPU内存，会导致内存不足的问题，如果数据量特别大，百G以上建议False。
- `skip_memory_metrics` (bool, 可选, 默认为 True)：是否将内存分析报告添加到性能指标中，默认情况下跳过这一步，以提高训练和评估的速度，建议打开，更能够清晰的知道每一步的内存使用。
- `include_inputs_for_metrics` (bool, 可选, 默认为 False)：是否将输入传递给 compute_metrics 函数，一般计算metrics用的是用的是模型预测的结果和我们提供的标签，但是有的指标需要输入，比如cv的IoU（Intersection over Union）指标。
- `auto_find_batch_size` (bool, 可选, 默认为 False)：是否使用自动寻找适合内存的batch size大小，以避免 CUDA 内存溢出错误，需要安装 accelerate（使用 pip install accelerate），这个功能还是比较NB的。
- `full_determinism` (bool, 可选, 默认为 False)：如果设置为 True，将调用 enable_full_determinism() 而不是 set_seed()，训练过程将启用完全确定性（full determinism），在训练过程中，所有的随机性因素都将被消除，确保每次运行训练过程都会得到相同的结果，注意：会对性能产生负面影响，因此仅在调试时使用。
- `torchdynamo` (str, 可选)：用于选择 TorchDynamo 的后端编译器，TorchDynamo 是 PyTorch 的一个库，用于提高模型性能和部署效率，可选的选择包括 "eager"、"aot_eager"、"inductor"、"nvfuser"、"aot_nvfuser"、"aot_cudagraphs"、"ofi"、"fx2trt"、"onnxrt" 和 "ipex"。默认就行，自动会选。
- `ray_scope` (str, 可选, 默认为 "last")：用于使用 Ray 进行超参数搜索时，指定要使用的范围，默认情况下，使用 "last"，Ray 将使用所有试验的最后一个检查点，比较它们并选择最佳的。详细的可以看一下它的文档。
- `ddp_timeout` (int, 可选, 默认为 1800)：用于 torch.distributed.init_process_group 调用的超时时间，在分布式运行中执行较慢操作时，用于避免超时，具体的可以看 PyTorch 文档 。
`torch_compile` (bool, 可选, 默认为 False)：是否使用 PyTorch 2.0 及以上的 torch.compile 编译模型，具体的可以看 PyTorch 文档 。
- `torch_compile_backend` (str, 可选)：指定在 torch.compile 中使用的后端，如果设置为任何值，将启用 torch_compile。
- `torch_compile_mode` (str, 可选)：指定在 torch.compile 中使用的模式，如果设置为任何值，将启用 torch_compile。
- `include_tokens_per_second` (bool, 可选)：确定是否计算每个设备的每秒token数以获取训练速度指标，会在整个训练数据加载器之前进行迭代，会稍微减慢整个训练过程，建议打开。
- `push_to_hub` (bool, 可选, 默认为 False)：指定是否在每次保存模型时将模型推送到Huggingface Hub。
- `hub_model_id` (str, 可选)：指定要与本地 output_dir 同步的存储库的名称。
- `hub_strategy` (str 或 HubStrategy, 可选, 默认为 "every_save")：指定怎么推送到Huggingface Hub。
- `hub_token` (str, 可选)：指定推送模型到Huggingface Hub 的token。
- `hub_private_repo` (bool, 可选, 默认为 False)：如果设置为 True，Huggingface Hub 存储库将设置为私有。
- `hub_always_push` (bool, 可选, 默认为 False)：是否每次都推送模型。

详见
- [LLM大模型之Trainer以及训练参数](https://zhuanlan.zhihu.com/p/662619853)

### Firefly


[Firefly](https://github.com/yangjianxin1/Firefly) 是开源的大模型**一站式训练框架**
- 支持对各种大模型进行**预训练**、**指令微调**、`DPO`，支持全量参数、LoRA、QLoRA等训练方式。
- 支持包括但不限于Gemma、Qwen1.5、MiniCPM、Mixtral-8x7B、Mistral、Llama等绝大多数主流的大模型。

【2024-3-5】[使用Firefly在单卡V100上对Qwen1.5进行SFT和DPO，大幅超越Qwen1.5和Gemma](https://mp.weixin.qq.com/s/C5X0qX2YsxhIoFvRsqcMMA)

用Firefly项目对Qwen1.5-7B进行训练的实验。我们对训练数据进行精细化筛选，然后在单张V100上进行SFT和DPO。经过两阶段的训练，我们的模型在Open LLM Leaderboard上的表现显著优于官方的Qwen1.5-7B-Chat、Gemma-7B-it、Vicuna-13B等模型。比Qwen1.5-7B-Chat高7.12分，比Gemma-7B-it高8.8分。


### TorchTune

【2024-3-23】[PyTorch官方发布LLM微调工具TorchTune](https://zhuanlan.zhihu.com/p/688671130?utm_psn=1755039674018496512)

PyTorch官方最近发布了支持LLM微调的工具：`TorchTune`。
- [TorchTune](https://pytorch.org/blog/torchtune-fine-tune-llms/) 是一个原生的 PyTorch 库，用于轻松编写、微调和实验大型语言模型（LLMs）

#### TorchTune 功能


功能：
- 原生 PyTorch 实现的流行大型语言模型
- 支持多种格式的checkpoints，包括 Hugging Face 格式的checkpoints
- 针对流行微调技术的训练策略，带有参考基准和全面的校验检查
- 与 HuggingFace 数据集集成用于训练，以及与 EleutherAI 的评估工具 Eval Harness 集成用于评估
- 支持使用 PyTorch 分布式中的 FSDP 进行分布式训练
- YAML 配置文件，便于轻松配置训练运行
- [即将推出] 支持来自 TorchAO 的低精度数据类型和量化技术
- [即将推出] 与各种推理引擎的互操作性

#### TorchTune 微调

TorchTune 已经支持了**Llama2 7B模型**的微调：
-   单卡微调：[https://github.com/pytorch/torchtune/blob/main/recipes/full_finetune_single_device.py](https://github.com/pytorch/torchtune/blob/main/recipes/full_finetune_single_device.py)
-   分布式微调：[https://github.com/pytorch/torchtune/blob/main/recipes/full_finetune_distributed.py](https://github.com/pytorch/torchtune/blob/main/recipes/full_finetune_distributed.py)
-   单卡LoRA：[https://github.com/pytorch/torchtune/blob/main/recipes/lora_finetune_single_device.py](https://github.com/pytorch/torchtune/blob/main/recipes/lora_finetune_single_device.py)
-   分布式LoRA：[https://github.com/pytorch/torchtune/blob/main/recipes/lora_finetune_distributed.py](https://github.com/pytorch/torchtune/blob/main/recipes/lora_finetune_distributed.py)
-   QLoRA：[https://github.com/pytorch/torc](https://github.com/pytorch/torchtune/blob/main/recipes/lora_finetune_single_device.py)


#### torchtune 安装

torchtune 必须通过克隆仓库并按照以下方式安装来构建：

```py
# ① 
pip install torchtune
# ② 
git clone https://github.com/pytorch/torchtune.git
cd torchtune
pip install -e .
```


### torchtitan

【2024-4-28】[torchtitan](https://github.com/pytorch/torchtitan) - 用于大型模型训练的原生 PyTorch 库

[torchtitan](https://github.com/pytorch/torchtitan) is a proof-of-concept (概念验证阶段) for Large-scale LLM training using native PyTorch. 
- It is (and will continue to be) a repo to showcase PyTorch's latest distributed training features in a clean, minimal codebase. 
- `torchtitan` is complementary (补充) to and not a replacement (替代) for any of the great large-scale LLM training codebases such as `Megatron`, `Megablocks`, `LLM Foundry`, `Deepspeed`, etc. 
- Instead, we hope that the features showcased in `torchtitan` will be adopted by these codebases quickly. torchtitan is unlikely to ever grow a large community around it.

Our guiding principles when building torchtitan:
- Designed to be easy to understand, use and extend for different training purposes.
- Minimal changes to the model code when applying 1D, 2D, or (soon) 3D Parallel.
- Modular components instead of a monolithic codebase.

Get started in minutes, not hours!

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


### LLaMA-Factory

LLaMA Factory 是一款支持多种LLM微调方式的工具，北航博士生推出，包括: **预训练**、**指令监督微调**和**奖励模型**训练等。
- 支持LoRA和QLoRA微调策略，广泛集成了业界前沿的微调方法。
- 特点: 支持多种LLM模型，提供了WebUI页面，使非开发人员也能微调。
- 体验地址：[LLaMA-Board](https://modelscope.cn/studios/hiyouga/LLaMA-Board/summary)
- 可视化界面 [LLaMA-Board](https://huggingface.co/spaces/hiyouga/LLaMA-Board)
- github: [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)，附各阶段训练数据集
- ![](https://pic2.zhimg.com/80/v2-7b24a5941a9bf996cf35187ae351f6c1_1440w.webp)

功能
- 多种模型：LLaMA、Mistral、Mixtral-MoE、Qwen、Yi、Gemma、Baichuan、ChatGLM、Phi 等等。
- 集成方法：（增量）预训练、指令监督微调、奖励模型训练、`PPO` 训练、`DPO` 训练和 `ORPO` 训练。
- 多种精度：32 比特全参数微调、16 比特冻结微调、16 比特 LoRA 微调和基于 AQLM/AWQ/GPTQ/LLM.int8 的 2/4/8 比特 QLoRA 微调。
- 先进算法：GaLore、DoRA、LongLoRA、LLaMA Pro、LoRA+、LoftQ 和 Agent 微调。
- 实用技巧：FlashAttention-2、Unsloth、RoPE scaling、NEFTune 和 rsLoRA。
- 实验监控：LlamaBoard、TensorBoard、Wandb、MLflow 等等。
- 极速推理：基于 vLLM 的 OpenAI 风格 API、浏览器界面和命令行接口。

详情参考
- [使用LLaMA Factory对大型语言模型进行微调](https://zhuanlan.zhihu.com/p/684989699)
- 作者北航博士[郑耀威](https://github.com/hiyouga)讲解 [全栈大模型微调框架LLaMA Factory：从预训练到RLHF的高效实现](https://www.bilibili.com/video/BV1Gt421L7dt)

<iframe src="//player.bilibili.com/player.html?aid=1801563508&bvid=BV1Gt421L7dt&cid=1463913844&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="600" width="100%"> </iframe>


安装
- [安装说明](https://github.com/hiyouga/LLaMA-Factory/blob/main/README_zh.md#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8)

```sh
# Clone the repository
git clone https://github.com/hiyouga/LLaMA-Factory.git
# Create a virtual environment
conda create -n llama_factory python=3.10
# Activate the virtual environment
conda activate llama_factory
# Install dependencies
cd LLaMA-Factory
pip install -r requirements.txt
```



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

ZeRO 三个优化阶段，对应**优化器状态**、**梯度**和**参数**划分。
- a. Pos:减少4倍内存，通信量与数据并行相同
- b. Pos+g:减少8倍内存，通信量与数据并行相同
- c. Pos+g+p:内存减少与数据并行度Nd呈线性关系。
  - 例如，在64个GPU（Nd=64）之间进行拆分将产生64倍的内存缩减。通信量有50%的适度增长。

ZeRO消除了内存冗余，使集群全部聚合内存容量可用。启用所有三个阶段的情况下，ZeRO在1024个NVIDIA GPU上训练万亿参数模型。
- 像Adam这样具有16位精度的优化器的万亿参数模型需要大约16 TB的内存来保存优化器的状态、梯度和参数。16TB除以1024是16GB，这对于GPU来说是在合理的范围内的。
- ZeRO2扩展了ZeRO-1，包括减少梯度内存占用，同时还添加了针对激活内存和碎片内存的优化。
- 与ZeRO-1相比，ZeRO-2将DeepSpeed可以训练的模型大小增加了一倍，同时显著提高了训练效率。
- 使用ZeRO-2，1000亿参数模型的训练速度可以比仅基于模型并行性的现有技术快10倍。

### ZeRO: 去除冗余

目前最流行的方法是 `ZeRO`（即零冗余优化器）。针对模型状态的存储优化（去除冗余），ZeRO使用的方法是**分片**，即每张卡只存 1/N 的模型状态量，这样系统内只维护一份模型状态。

ZeRO有三个不同级别，对模型状态进行不同程度的分片：
- ZeRO-1: 对**优化器状态**分片（Optimizer States Sharding）
- ZeRO-2: 对**优化器状态**和**梯度**分片（Optimizer States & Gradients Sharding）
- ZeRO-3: 对**优化器状态**、**梯度**分片以及**模型权重参数**分片（Optimizer States & Gradients & Parameters Sharding）
- ![img](https://mmbiz.qpic.cn/mmbiz_png/J0mLianhFicBHEDwE5nPHZKaicqsXBVgES5rYysbjp9PYV3E8JOgU4ZZmyVBDUeryCQpvUBAUu6bGcUico0UWE9uIQ/640?wx_fmt=png&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1)

Zero包括3种方案，逐步递进：
- `zero1`：将adam参数分割成N份，一个GPU上只能保存一份adam参数：这对于forward没啥影响，gradient需要进行一次all-reduce，但是只能更新一部分参数，所以W需要进行一次all-gather，通信量为3N*sita，存储为 12*sita/N + 4*sita
- `zero2`: 将adamw/gradient都分割成N份，梯度就不需要all-gather了，只需要scatter了，w需要all-gather，通讯量为2N*sita
- `zero3`: 将参数/adam/gradient都分割，forward的时候，需要将w all-gather，backfoward时，还需要把w all-gather回来，计算梯度，丢掉不属于自己的w，然后对梯度做reduce scatter，更新w，通讯量为3N*sita。

deepspeed 采用stage3：用1.5倍的通讯开销，换回近120倍的显存

ZeRO-Offload 基于Zero2，将adam和gradient放到内存中，在cpu内起了N个线程计算。
- 一条主线是gradient总是需要scatter的，感觉这个数据并行标志。
- 注意:不管是forward 还是backward都要有完整的w的。
- 另外有了gradient，以及adamW的参数，才能更新W。

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
 
ZeRO-Offload 使 GPU 单卡能够训练 10 倍大的模型

`ZeRO-Offload` 是 ZeRO（Zero Redundancy Optimizer）技术**扩展**，用显存作为模型参数存储和通信的中间介质，以减少模型并行化训练中的通信和同步开销。
- 2021年 UC Merced的 [Jie Ren](https://jren73.github.io/) 发表 于ATC, [ZeRO-Offload: Democratizing Billion-Scale Model Training](https://www.usenix.org/conference/atc21/presentation/ren-jie)，博士期间的研究方向是 Memory Management on Heterogeneous Memory Systems for Machine Learning and HPC
- `ZeRO-Offload` 让人人训练得起大模型
 
ZeRO-Offload 技术用显存缓存将模型参数存储在显存中，这可以减少网络带宽的使用，同时还可以加速参数访问和更新。为了最大限度地减少显存的使用，ZeRO-Offload技术使用了一种称为“按需加载”的策略。这种策略只在需要使用参数时才将其从磁盘或网络加载到显存中，而不是一次性将所有参数都加载到显存中。
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


### ZeRO-Infinity

ZeRO-Infinity: 利用NVMe打破GPU显存墙
- 2021年发表于SC, [ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep Learning](https://arxiv.org/pdf/2104.07857.pdf)
- 同样是进行 offload，ZeRO-Offload 更侧重单卡场景，而 `ZeRO-Infinity` 则是典型的工业界风格，奔着极大规模训练去了。


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

### GPU与神经网络

如何让神经网络的深度学习更快、更省电？

重点关注一个名为GEMM的函数。
- BLAS（基本线性代数子程序）库的一部分，该库最早创建于1979年

使用Alex Krizhevsky的Imagenet架构进行图像识别的典型深度卷积神经网络的时间。
- ![](https://petewarden.files.wordpress.com/2015/04/profile.png)
- 所有以`fc`（即：全连接层）或`conv`（即：卷积层）开头的层都是使用`GEMM`实现的，几乎所有的时间（95%的GPU版本，89%的CPU版本）都花在这些层上。

- [为什么GEMM是深度学习的核心](https://www.jianshu.com/p/6d3f013d8aba) 
- [Why GEMM is at the heart of deep learning](https://petewarden.com/2015/04/20/why-gemm-is-at-the-heart-of-deep-learning/)

#### GPU加速核心GEMM

GPU主要加速gemm，论文
- gemm在深度学习中的耗时占比达到80%以上。
- fc可以展开为gemm 
- cnn可以通过im2col展开为gemm

cuda框架中，cuBLAS主要是对gemm类算法进行优化，其他cuFFT，cuRAND, cuSPARSE各自针对不同的算法进行优化。

cuDNN则是完全针对DL中的batchNormalization这类神经网络层的计算进行优化。

作者：[Huisheng Xu](https://www.zhihu.com/question/571648206/answer/2796623713)


#### 什么是GEMM？

`GEMM` 代表 GEneral Matrix to Matrix Multiplication （**通用矩阵到矩阵乘法**）
- 本质上完全按照tin上所说的做，将两个输入矩阵相乘，得到一个输出矩阵。
- 与3D图形世界中的矩阵运算的不同之处在于，处理矩阵通常非常大。

例如，典型网络中的单个网络层可能需要将256行1152列的矩阵乘以1152行192列的矩阵，以产生256行192列的结果。
- 天真地说，这需要5700万（256x1152x192）次浮点运算，而且在现代网络结构中可能有几十个这样的网络层，所以经常看到一个往往需要几十亿次浮点运算来计算单个图像帧。


#### FC 全连接层


全连接层是已经存在了几十年的经典神经网络层。
- FC层的每个输出值都可以看到输入的每个值，将输入乘以该输入对应的权重，然后对结果求和以获得其输出。
- 有“k”个输入值，“n”个神经元，每个神经元都有自己的学习权重集。对应的图中有“n”个输出值，每个神经元对应其中一个，该输出值利用对其权重和输入值进行点积运算计算得到。

#### Conv 卷积层

conv层将其输入视为二维图像，每个像素具有多个通道，非常类似于具有宽度、高度和深度的经典图像。不过，与我以前处理的图像不同，通道的数量可以达到数百个，而不仅仅是RGB或RGBA

为什么要用GEMM矩阵乘法
- Fortran世界的科学程序员花了几十年时间优化代码，以执行大型的矩阵乘法（large matrix to matrix multiplications），而且非常规则的内存访问模式带来的好处超过了浪费的存储成本。
- Nvidia的论文介绍了一些不同方法，描述了为什么最终以修改版的GEMM作为最喜欢的方法。
  - [cuDNN: Efficient Primitives for Deep Learning](https://arxiv.org/pdf/1410.0759.pdf)
  - 同时对1个卷积核批处理大量输入图像也有很多优点，[Caffe con TROL](https://arxiv.org/pdf/1504.04343v1.pdf) 使用了这些方法，取得了很好的效果
- GEMM方法的主要竞争对手是使用傅里叶变换在频率空间中进行运算，但在卷积中使用stride使其难以达到同样的效率。

GEMM是如何应用于卷积层的？
- 卷积似乎是一个相当专业的运算。
- 包含多次乘法计算和最后的求和计算，比如完全连接层，但不清楚如何将其转化为GEMM矩阵乘法。





# 结束