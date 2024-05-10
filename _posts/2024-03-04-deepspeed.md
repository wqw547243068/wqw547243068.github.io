---
layout: post
title:  "DeepSpeed 学习笔记"
date:   2024-03-04 19:25:00
categories: 大模型
tags: GPU Pytorch 分布式 deepspeed
excerpt: DeepSpeed 知识点、训练技巧总结
author: 鹤啸九天
mathjax: true
permalink: /deepspeed
---

* content
{:toc}

# DeepSpeed 学习笔记


deepspeed 知识点 
- [ppt](https://github.com/chenzomi12/AISystem/tree/main/06Foundation/07Parallel)



## 为什么

一个**7B**规模大模型（如LLaMA-2 7B），基于**16-bit**混合精度训练时
- 仅考虑模型参数、梯度、优化器情况下，显存占用就有**112GB**
  - 参数占GPU 显存近 **14GB**（每个参数2字节）。
  - 训练时**梯度**存储占**14GB**（每个参数对应1个梯度，也是2字节）
  - 优化器Optimizer（假设是主流的AdamW）则是**84GB**（每个参数对应1个参数copy、一个momentum和一个variance，这三个都是float32）
    - 2byte 模型**静态**参数权重（以16bit存储） = 14G
    - 2byte 模型**更新**参数权重 （以16bit存储）= 14G
    - 2byte **梯度**（以16bit存储）= 14G
    - 2byte **梯度更新**（以16bit存储）= 14G
    - 4byte **一阶动量**优化器更新（以32bit存储）= 28G
    - 4byte **二阶方差**优化器更新（以32bit存储）= 28G
  - 目前，合计112GB
  - 还有：前向传播时激活值，各种临时变量
  - 还与sequence length, hidden size、batch size都有关系。
- 目前A100、H100这样主流显卡单张是放不下，更别提国内中小厂喜欢用的A6000/5000、甚至消费级显卡。

混合精度训练的迭代流程
- ![](https://pic1.zhimg.com/80/v2-8aed207b50089e0f6598974edfaeabc8_1440w.webp)

PyTorch 里的 DataParallel 无法满足
- ![](https://pic2.zhimg.com/80/v2-617ce43cf91185b2fd426daf6e6222e5_1440w.webp)

模型并行和流水线并行实现相对复杂，需要模型拆分、卡间通讯等。以及优化显存占用门槛高。

这也是DeepSpeed被设计的初衷。


## DeepSpeed 框架演进

【2024-4-6】总结：

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-04-06T08:58:33.411Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\&quot; etag=\&quot;WPKRZEx3iDk2hN-1VGnZ\&quot; version=\&quot;24.2.2\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;-380\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; value=\&quot;LLM(大模型)训练框架\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;567.75\&quot; y=\&quot;1240\&quot; width=\&quot;224.5\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;940\&quot; y=\&quot;1383.5\&quot; width=\&quot;150\&quot; height=\&quot;165\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; value=\&quot;Megatron\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#00CC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; y=\&quot;1450\&quot; width=\&quot;100\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-13\&quot; value=\&quot;GPT分布式训练\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;730.0000000000001\&quot; y=\&quot;1355\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-7\&quot; y=\&quot;1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-25\&quot; value=\&quot;Microsoft\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;800.0000000000001\&quot; y=\&quot;1442.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-28\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; target=\&quot;yvSmSdpK5QFk-1BAp_-0-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;624.5799999999999\&quot; y=\&quot;2090\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;844.5799999999999\&quot; y=\&quot;2090\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-32\&quot; value=\&quot;3D并行\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;959.53\&quot; y=\&quot;1394.5\&quot; width=\&quot;60.47\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-1\&quot; value=\&quot;PyTorch\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;590\&quot; y=\&quot;1340\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-11\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-2\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-2\&quot; value=\&quot;DeepSpeed\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#6666FF;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;702.25\&quot; y=\&quot;1451\&quot; width=\&quot;100\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-1\&quot; target=\&quot;yvSmSdpK5QFk-1BAp_-0-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;547.25\&quot; y=\&quot;1420\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;680\&quot; y=\&quot;1450\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-5\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-1\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;579\&quot; y=\&quot;1390\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;705\&quot; y=\&quot;1460\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-6\&quot; value=\&quot;NVIDIA\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#009900;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;451.0000000000001\&quot; y=\&quot;1430\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;3\&quot; y=\&quot;11\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-7\&quot; value=\&quot;Megatron-DeepSpeed\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#7F00FF;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;659.97\&quot; y=\&quot;1784\&quot; width=\&quot;180\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-8\&quot; value=\&quot;ZeRO-*\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;959.53\&quot; y=\&quot;1428.5\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-9\&quot; value=\&quot;ZeRO offload\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;959.53\&quot; y=\&quot;1466.5\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-10\&quot; value=\&quot;混合精度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;959.53\&quot; y=\&quot;1508.5\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-12\&quot; value=\&quot;&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;本质: 数据并行优化版&amp;lt;/div&amp;gt;&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;前提: &amp;lt;font color=&amp;quot;#ff0000&amp;quot;&amp;gt;单层参数单张显卡放得下&amp;lt;/font&amp;gt;&amp;lt;/div&amp;gt;案例: MT-530B, BLOOM\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;760.0000000000001\&quot; y=\&quot;1510\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-13\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-16\&quot; target=\&quot;yvSmSdpK5QFk-1BAp_-0-7\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;595\&quot; y=\&quot;1380\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1460\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-2\&quot; target=\&quot;yvSmSdpK5QFk-1BAp_-0-7\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1490\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;622\&quot; y=\&quot;1604\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-15\&quot; value=\&quot;前提不满足&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;500.0000000000002\&quot; y=\&quot;1507.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-16\&quot; value=\&quot;Megatron-LM-1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;420\&quot; y=\&quot;1594\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-17\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; target=\&quot;yvSmSdpK5QFk-1BAp_-0-16\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1490\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;705\&quot; y=\&quot;1604\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-18\&quot; value=\&quot;超大规模Transformer分布式训练:&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;数据并行 + 张量并行&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490.0000000000002\&quot; y=\&quot;1570\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-19\&quot; value=\&quot;模型并行内核&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540.0000000000002\&quot; y=\&quot;1451\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-20\&quot; value=\&quot;① ZeRO分片&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;② 管道并行&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;760.0000000000002\&quot; y=\&quot;1700\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-21\&quot; value=\&quot;③ 张量并行\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;640.0000000000002\&quot; y=\&quot;1710\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-22\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#cc0000&amp;quot;&amp;gt;3D并行&amp;lt;/font&amp;gt; = &amp;lt;font color=&amp;quot;#7f00ff&amp;quot;&amp;gt;ZeRO分片&amp;lt;/font&amp;gt; + &amp;lt;font color=&amp;quot;#7f00ff&amp;quot;&amp;gt;管道并行&amp;lt;/font&amp;gt; + &amp;lt;font color=&amp;quot;#009900&amp;quot;&amp;gt;张量并行&amp;lt;/font&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;659.9700000000003\&quot; y=\&quot;1830\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-1\&quot; value=\&quot;Megatron-LM-2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;420\&quot; y=\&quot;1784\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-2\&quot; value=\&quot;Megatron-LM-3\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;420\&quot; y=\&quot;1890\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-3\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-16\&quot; target=\&quot;773s7HMUVt6-7SW6n1rD-1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1634\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;760\&quot; y=\&quot;1794\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;773s7HMUVt6-7SW6n1rD-1\&quot; target=\&quot;773s7HMUVt6-7SW6n1rD-2\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1634\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1794\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-5\&quot; value=\&quot;流水线并行, 3D并行\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490.0000000000002\&quot; y=\&quot;1770\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-6\&quot; value=\&quot;增加3个特性&amp;lt;div&amp;gt;- layernorm和dropout并行&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;- 激活函数不重复计算&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;- GPU显存未满时不做checkpoint&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;550.0000000000002\&quot; y=\&quot;1900\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-7\&quot; value=\&quot;wqw547243068@163.com&amp;lt;div&amp;gt;2024-4-6&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;890.0000000000002\&quot; y=\&quot;1910\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


## Megatron -- NVIDIA

[Megatron](https://github.com/NVIDIA/Megatron-LM) is a large, powerful transformer developed by the Applied Deep Learning Research team at NVIDIA. This repository is for ongoing research on training large transformer language models at scale. We developed efficient, model-parallel (tensor, sequence, and pipeline), and multi-node pre-training of transformer based models such as GPT, BERT, and T5 using mixed precision.

【2023-7-27】[大模型-LLM分布式训练框架总结](https://zhuanlan.zhihu.com/p/623746805)

### Megatron-LM 介绍

【2020-3-13】Megatron 是超大规模Transformer模型的**分布式训练**解决方案。字节、阿里和快手等公司都将其作为大模型训练框架。
- 论文: [Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism](https://arxiv.org/pdf/1909.08053.pdf)
- 中文解读: [Megatron论文和代码详细分析](https://zhuanlan.zhihu.com/p/366906920)
  - intra-layer and inter-layer: 层间并行和层内并行
  - orthogonal and complimentary 正交和互补
  - scaling efficiency的计算公式 76%

|概念|中文|图解|
|---|---|---|
|intra-layer and inter-layer|层间并行和层内并行|![](https://pic2.zhimg.com/80/v2-c24f5994e88c4361d578d5e0939be7b9_1440w.webp)|
|orthogonal and complimentary|正交和互补|![](https://pic2.zhimg.com/80/v2-708c01105de92567824bd9d3456b9459_1440w.webp)|

Megatron 核心能力:
- 多种并行策略组合: Data Parallel、 Tensor Parallel、Pipeline Parallel、Sequence Parallel
- Distributed-optimiezer: 相当于是deepspeed zero1的策略
- 高性能算子：Flash Attention
- Activation checkpoint
- 混合精度
- Gradient accumulation
- MoE

Megatron-LM
- 1). Megatron-LM-1
- 2). Megatron-LM-2
- 3). Megatron-LM-3

### Megatron-LM-1

利用了`张量并行`和`数据并行`

### Megatron-LM-2

Megatron 2 在 Megatron 1 的基础上新增了 `pipeline 并行`，提出了virtual pipeline:1F1B-interleaving，成为和 DeepSpeed 类似的 `3D 并行`训练框架。

另外 Megatron-2 论文提及了一些通信优化的小 trick，本质是增加本地的 io 操作和通信，从而降低低带宽网络的通信量。

内存占用角度：
- `G-pipe` 到 `PipeDream` 进化完成，通过及时安排反向过程，将前向激活值释放掉，避免积累太多激活值占用内存，提高了模型并行的能力。

空泡比率角度：
- 空泡比率的提升主要从 1F1B 到 1F1B-interleaving 的进化得来。pipeline 并行的一个基本规律就是 pipeline 流水的级数越多，overhead 就越小。

### Megatron-LM-3

增加三个feature: 
- `Sequence Parallelism`: Tensor Parallelism 基础上，将Transformer的LayerNorm以及Dropout层的输入按Sequence Length维度进行了切分，使得各个设备上面只需要做一部分的Dropout和LayerNorm。
- `Selective Activation Recomputation` 去掉激活值重新计算
- `Checkpointing Skipping`: GPU显存没占满时候不做checkpointing

Megatron1, 2中，Transformer核的TP通信是由正向两个Allreduce以及后向两个Allreduce组成的。Megatron 3由于对sequence维度进行了划分，Allreduce在这里已经不合适
- ![](https://pic3.zhimg.com/80/v2-06a0a77032c8a7262cb0f846f87ffe0e_1440w.webp)


Checkpointing Skipping
- ![](https://pic4.zhimg.com/80/v2-2154af6448b05283d58bd27f300b0533_1440w.webp)


## Megatron-DeepSpeed

`Megatron-DeepSpeed` 结合了两种主要技术：
- `DeepSpeed` 是微软开发的深度学习**优化库**，分布式训练变得简单、高效和有效。
- `Megatron-LM` 是由 `NVIDIA` 的应用深度学习研究团队开发的大型、强大的 **Transformer 模型框架**。

DeepSpeed 团队通过将 `DeepSpeed` 库中的 `ZeRO 分片`（ZeRO sharding）和`管道并行`（pipeline parallelism）与 `Megatron-LM` 中的`张量并行`（Tensor Parallelism）相结合，开发了一种基于 **3D 并行**的实现。

`Megatron-DeepSpeed` 实施 3D 并行, 让大型模型训练更加高效。
- `DataParallel` (DP) - 相同的初始化模型被复制多次，并且每次都被馈送 minibatch 的一部分。处理是并行完成的，所有设置在每个训练步骤结束时进行同步。
- `TensorParallel` (TP) - 每个张量都被分成多个块，因此不是让整个张量驻留在单个 GPU 上，而是张量每个分片都驻留在其指定的 GPU 上。在处理过程中，每个分片在不同的 GPU 上分别并行处理，最终结果在步骤结束时同步。这也被称作横向并行。
- `PipelineParallel` (PP) - 模型在多个 GPU 上垂直（层级）拆分，因此只有模型的一个或多个层放置在单个 GPU 上。每个 GPU 并行处理管道的不同阶段，并处理一小部分批处理。
- `零冗余优化器` (ZeRO) - 也执行与 TP 有点类似的张量分片，除了整个张量会及时重建以进行前向或反向计算，因此不需要修改模型。它还支持各种卸载技术以补偿有限的 GPU 内存。

各个技术细节参考：[大型语言模型(LLM)训练指南](https://zhuanlan.zhihu.com/p/611325149)


## DeepSpeed 介绍

GPT-3把LLM参数量推到了**175B**，训练所需参数大小更是到达了万亿规模
- Megatron 开始变得无能为力
- 而DeepSpeed ZeRO方法问世, 解决了这个问题


## DeepSpeed 安装

### 如何安装

直接pip安装：

```sh
pip install deepspeed
```

官方推荐仓库本地编译安装，更加适配本地硬件环境：

```sh
git clone https://github.com/microsoft/DeepSpeed/
cd DeepSpeed
rm -rf build
TORCH_CUDA_ARCH_LIST="8.6" DS_BUILD_CPU_ADAM=1 DS_BUILD_UTILS=1 pip install . \
--global-option="build_ext" --global-option="-j8" --no-cache -v \
--disable-pip-version-check 2>&1 | tee build.log
```

检查

```sh
ds_report
```

### HuggingFace

Transformers中，`Trainer`集成核心的DeepSpeed功能

HuggingFace 提供 DeepSpeed 集成，所需参数都可以由Transformer的`Trainer`自动指定。
- DeepSpeed 在 HuggingFace Transformer 上更为便捷（DeepSpeed 可独立使用，并不依赖于Transformer）。
                        
[原文](https://blog.csdn.net/weixin_43301333/article/details/127237122)

作为Transformer的附属包安装

```sh
pip install transformers[deepspeed]
```

### 如何使用

使用DeepSpeed之后，你的命令行看起来就会像下面这样：

```sh
deepspeed --master_port 29500 --num_gpus=2 run_s2s.py \
--deepspeed ds_config.json
--master_port # 端口号。最好显示指定，默认为29500，可能会被占用（i.e., 跑了多个DeepSpeed进程）。
--num_gpus # GPU数目，默认会使用当前所见的所有GPU。
--deepspeed # 提供的config文件，用来指定许多DeepSpeed的重要参数。
```

使用DeepSpeed的核心要点: 写一个config文件（.json，或json格式的配置文件）
- 指定想要的参数，例如，权衡时间和显存 (前文所提到的，这是一个很重要的权衡)。

因此，最重要的是 `--deepspeed`，即提供的config文件，即ZeRO。


【2023-9-16】[DeepSpeed：炼丹小白居家旅行必备](https://www.bilibili.com/video/BV1mN411n7eg)
- 代码：[](https://github.com/OvJat/DeepSpeedTutorial)
- 如何使用deepspeed分布式训练大模型：原理、代码、操作细节

```sh
deepspeed \
    --launcher_args "source ${PWD}/setup_env.sh" \
    --hostfile hostfile \
    deepspeed_script.py \
    --deepspeed \
    --deepspeed_config "$PWD/deepspeed_config.json"
```

<iframe src="//player.bilibili.com/player.html?aid=491005367&bvid=BV1mN411n7eg&cid=1269537042&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>




## DeepSpeed 原理

DeepSpeed的核心思想: 
> <span style='color:red'>GPU显存不够，CPU内存来凑</span>

deepspeed 底层依赖 `torch.distribution` 、 `cuda` 等等. 

底层分布式通信引擎支持多种选择
- ['`cuda`', '`cpu`', '`xpu`', '`npu`', '`mps`']
- 大部分选择 cuda, 可通过环境变量 `DS_ACCELERATOR` 指定

入口([__init__](https://github.com/microsoft/DeepSpeed/blob/master/deepspeed/__init__.py))只是一个代理，根据不同情况选择三种模式之一
- `流水线引擎`（PipelineEngine）
- `混合引擎`（DeepSpeedHybridEngine），同时进行**训练**和**推理**，为 RLHF 训练定制。
- `一般模式`（DeepSpeedEngine），基本模式，分布式**训练**引擎。

DeepSpeedEngine 的实现在 `deepspeed.runtime.engine` 中， 本身是 `torch.nn.Module` 的子类，对输入模型的一个封装。 
- DeepSpeedEngine 的 [__init__](https://github.com/microsoft/DeepSpeed/blob/master/deepspeed/__init__.py) 方法中进行了大量初始化操作， 其中最重要的就是对优化器（Optimizer）的初始化， ZeRO 的核心特性的实现都在优化器（Optimizer）中。


### DeepSpeed 适用情形

DeepSpeed 仅适用于:
- <span style='color:red'>显存极度短缺</span>的情况；
  - i.e., 模型大到 `batch_size == 1`也跑不了
- 用DeepSpped节省下来的显存，刚好够支持更大的batch_size。

否则，使用DeepSpeed只会增加时间开销，并没有其他益处。
- stage3 速度极其缓慢。
  - 原先需要6h的训练过程，用 DeepSpeed stage3之后，运行了2天2夜，也没有结束的迹象。
- stage2 由于分配了模型参数到**多个设备**上，console 看不到任何输出信息（但是GPU还是在呼呼响，utility也为100%），不知道程序的运行进度，不友好。

由于 DeepSpeed 通过占用CPU内存来减缓GPU的开销，当系统CPU不够的时候，DeepSpeed 进程就会自动被系统停止，造成没有任何报错，DeepSpeed无法启动的现象。
- 建议用estimation估计一下CPU内存占用，然后用`free -h`查看一下机器的CPU内存空余量，来判断能否使用DeepSpeed。

### DeepSpeed 功能

[DeepSpeed](https://www.deepspeed.ai/) 支持多种训练优化策略。包括：
- 3D并行：数据并行、模型并行、流水线并行以及三者的混合使用
- Zero Redundancy Optimizer（零冗余优化器）：ZeRO-0、ZeRO-1、ZeRO-2、ZeRO-3、ZeRO-Infinity
- ZeRO-Offload ：卸载，支持将数据、梯度、优化器状态等下沉到 CPU 和 NVMe
- 自定义混合精度训练训练：动态精度缩放（Dynamic Loss Scaling）和混合精度优化器（Mixed Precision Optimizer） 

此外, [DeepSpeed](https://www.deepspeed.ai) 还提供许多大模型相关的工具，如分布式训练管理、内存优化和模型压缩等，以帮助开发者更好地管理和优化大规模深度学习训练任务。DeepSpeed在自然语言处理（NLP）和多模态等领域有许多成功的应用案例。DeepSpeed可以极大提升大模型的训练速度、降低训练门槛以及训练成本，并因具备完整健康的社区生态，提升大模型的可用性。让中小公司、独立研究人员解锁了训练具有超过1000亿个参数的模型的能力。
- 参考：[LAM](https://zhuanlan.zhihu.com/p/685472786)

>- [DeepSpeed](https://www.deepspeed.ai/) is a deep learning optimization library that makes distributed training and inference easy, efficient, and effective.
>- DeepSpeed trained the world’s most powerful language models (`MT-530B`, `BLOOM`)

微软的 `DeepSpeed` 模型并行等内核取自 `Megatron` ，且 DeepSpeed 主打在数据并行下如何以更少的机器去跑更大的模型 （ ZeRO 、 ZeRO-Offload 等都是用梯度切片、计算、内存/硬盘换入换出来省显存）

目前开源的 模型库 主要是 NVIDIA 的 `Megatron-LM` 和微软的 [DeepSpeed](https://www.deepspeed.ai/)。

`Megatron` 和 `DeepSpeed` 都是基于 `PyTorch` ，分别由 `NVIDIA` 和`微软`经过深度定制开发，专门为支持 PyTorch 分布式训练 GPT 而设计的。

`NVIDIA` 的 `Megatron` 和 微软的 `DeepSpeed`：

DeepSpeed 本质上是一种“节省显存”的数据并行，即：<span style='color:blue'>数据并行的优化版</span>。
- DeepSpeed 假设了单层参数量可以在单张显卡上放得下，如果不满足这个假设，那么仍然需要使用模型并行，而且 DeepSpeed 的模型并行是通过调用 Megatron 来实现的。
- 根据 NVIDIA 最新的那篇[论文](https://arxiv.org/abs/2104.04473)，`Megatron` 在大规模训练的效率是超过 `DeepSpeed` 不少的。
- DeepSpeed 的论文一直强调：可以用更少机器训练更大的模型，但没有突出过在效率上的优势。
- DeepSpeed 后来又出了一篇论文：[ZeRO-Infinity](https://arxiv.org/abs/2104.07857)，当单层参数量在单张显卡上放不下的时候，它通过对这一层算子切片，一片一片来执行，使得单卡也能跑起来一个巨大的层，可以理解成一种 “时间”轴上展开的模型并行。


### DeepSpeed 文档

[DeepSpeed 官方文档](https://www.deepspeed.ai/getting-started/)


## DeepSpeed 框架

[DeepSpeed](https://www.deepspeed.ai/getting-started/) 主要分成以下四个板块，包括：`Training`、`Inference`、`Compression`、`Science`
- ![](https://pic1.zhimg.com/v2-a9ac939ec325cf859c282511ddd90f2c_b.jpg)

DeepSpedd-Training 提供一套端到端大模型训练框架，核心板块。
- 因为DeepSpeed 基于PyTorch搭建，且兼容 Transformers，新用户学习成本较低，可快速上手，快速实现自有工程的搭建。
- 并且DeepSpeed在DeepSpeedExamples项目中提供了`DeepSpeed-chat`模块 ，完美复刻`InstructGPT`论文中RLHF训练方式，可以一键式完成大模型的SFT、Reward Model Finetuning、RLHF
- ![](https://pic3.zhimg.com/v2-28ace0f70b557dc6b6394171daeab912_b.jpg)

[DeepSpeedExamples](https://github.com/microsoft/DeepSpeedExamples) 也提供 bert、gan、Stable Diffusion 微调案列，更方便的学习应用DeepSpeed。

DeepSpeed发展速度非常快，一些新的大模型热点技术都实现快速支持 。目前DeepSpeed可以支持MoE模型架构训练，并且在超长上下文模型训练问题上也提供了优化方案。


### DeepSpeed-Trianing

DeepSpeed-Trianing 介绍

通信策略优化
- 为更好支持GPU、CPU上分布式训练及混合训练。DeepSpeed支持 `mpi`、`gloo` 和 `nccl` 等通信策略
- Open MPI: 整合高性能计算社区中所有专家，技术和资源，以构建可用的最佳MPI库。
- `Gloo`: facebook开源的一套集体通信库，提供对机器学习中有用的一些集合通信算法如：barrier, broadcast, allreduce
- `nccl`: NVIDIA集体通信库（NCCL）实现NVIDIA GPU性能优化的多GPU和多节点**集体通信原语**。NCCL提供了诸如all-gather, all-reduce, broadcast, reduce, reduce-scatter等实现，优化后可以通过PCIe和NVLink等高速互联，高带宽和低延迟。 
  - 因为NCCL则是NVIDIA基于自身硬件定制，能做到更有针对性且更方便优化，故在英伟达硬件上，NCCL的效果往往比其它通信库更好。
- 选择策略: 
  - 如果在 CPU 集群上分布式训练，选择 `mpi` 和 `gloo`；
  - 如果在 GPU 上进行分布式训练，可以选择 `nccl`。


### TencentPretrain

[TencentPretrain](https://github.com/Tencent/TencentPretrain) ：[腾讯预训练模型框架](https://github.com/Tencent/TencentPretrain/blob/main/README_ZH.md)
- Tencent Pre-training framework in PyTorch & Pre-trained Model Zoo

TencentPretrain 是一个用于对文本、图像、语音等模态数据进行预训练和微调的工具包。
- TencentPretrain遵循模块化的设计原则。通过模块组合，用户能迅速精准的复现已有的预训练模型，并利用已有的接口进一步开发更多的预训练模型。
- 通过TencentPretrain，建立了一个模型仓库，其中包含不同性质的预训练模型（例如基于不同模态、编码器、目标任务）。用户可以根据具体任务的要求，从中选择合适的预训练模型使用。
- TencentPretrain继承了开源项目UER (https://github.com/dbiir/UER-py/) 的部分工作，并在其基础上进一步开发，形成支持多模态的预训练模型框架。

## DeepSpeed 实例


### AlexNet 训练

以 alexnet 为例, 体验 deepspeed 训练, github 文件: [pipeline_parallelism](https://github.com/microsoft/DeepSpeedExamples/tree/master/training/pipeline_parallelism)
- [alexnet.py](https://github.com/microsoft/DeepSpeedExamples/blob/master/training/pipeline_parallelism/alexnet.py)
- [train.py](https://github.com/microsoft/DeepSpeedExamples/blob/master/training/pipeline_parallelism/train.py)
- [run.sh](https://github.com/microsoft/DeepSpeedExamples/blob/master/training/pipeline_parallelism/run.sh)
- [ds_config.json](https://github.com/microsoft/DeepSpeedExamples/blob/master/training/pipeline_parallelism/ds_config.json)

[run.sh](https://github.com/microsoft/DeepSpeedExamples/blob/master/training/pipeline_parallelism/run.sh)

```sh
deepspeed train.py --deepspeed_config=ds_config.json -p 2 --steps=200
```

[ds_config.json](https://github.com/microsoft/DeepSpeedExamples/blob/master/training/pipeline_parallelism/ds_config.json)

```json
 {
  "train_batch_size" : 256,
  "train_micro_batch_size_per_gpu" : 8,

   "optimizer": {
    "type": "Adam",
    "params": {
      "lr": 0.001,
      "betas": [
        0.9,
        0.999
      ],
      "eps": 1e-8
    }
  },
  
  "steps_per_print" : 10,
  "wall_clock_breakdown" : false
 }
```

单机单卡实验
- A100 训练200步完毕


## DeepSpeed-Chat

【2024-3-29】[大模型训练入门实战](https://techdiylife.github.io/big-model-training/deepspeed/deepspeed-chat.html)

DeepSpeed 是 Microsoft基于 PyTorch 研发的开源深度学习优化库。
- 目的: 降低大模型训练的门槛，提升大模型的训练的效率，帮助开发者更有效率地管理及优化大模型的训练、部署任务。

### DeepSpeed-Chat 介绍

`DeepSpeed-Chat` 微软发布的类ChatGPT模型训练工具。
- 该工具基于微软的大模型训练工具DeepSpeed，使用可简单高效地训练ChatGPT。

工具特点：
- 类ChatGPT完整训练代码：包括 预训练模型下载、数据下载、InstructGPT训练过程和测试。
- 多种规模的模型：模型参数从1.3B到66B，适合新手学习, 也可商用部署。
- 高效训练：通过使用最新技术(ZeRO和LoRA等)改善训练过程。
  - 例如，一个67亿（6.7B）参数的模型，使用**8块A00**只需要约**5个小时**完成训练。
- 推理API：提供易于使用的推理API，方便对话式交互测试。

视频讲解

<iframe width="560" height="315" src="https://www.youtube.com/embed/RR8E9jy1eWk?si=8s6TvmBTB1nYOKz2" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


### DeepSpeed-Chat 部署

推荐设置：
- Linux 操作系统
- GPU 24G 以上显存
- CUDA 版本 11.7

```sh
# conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
git clone https://github.com/microsoft/DeepSpeedExamples.git
cd DeepSpeedExamples/applications/DeepSpeed-Chat/
# 安装依赖
pip install -r requirements.txt
```

### DeepSpeed-Chat 代码

DS-chat 代码位于 `applications/DeepSpeed-Chat` 目录下，主要程序结构：
- `train.py`  # 入口程序
- **training**  # 训练脚本
  - **step1_supervised_finetuning**   # 第1步训练
    - evaluation_scripts      # 第1步训练后,评价
    - **training_scripts**        # 模型训练脚本
    - README.md               # 说明文档
    - `main.py`                 # 主程序，训练过程的实现细节
    - `prompt_eval.py`          # 评价主程序
  - **step2_reward_model_finetuning** # 第二步训练
    - 省略
  - **step3_rlhf_finetuning**    # 第三步训练
    - 省略
  - **utils** 模型训练，评价的相关函数库
- **inference** # 测试，评价代码

模型训练调用过程（以1.3b模型为例）


deepspeed 总入口在 `deepspeed.__init__::initialize`

#### train.py

入口程序： `train.py`

主要参数
- --`step` 1 2 3
- --`deployment-type` single_gpu single_node multi_node 不同type主要是参数的设置不同
- --`actor-model`: "1.3b", "6.7b", "13b", "66b" 预训练模型，默认是1.3b的模型
- --`reward-model`：使用的是 350m 的模型
- 其他参数参考train.py中的说明

#### 配置脚本

配置脚本：
- training/step1_supervised_finetuning/training_scripts/single_node/run_1.3b.sh
- train.py 程序会调用 run_1.3b.sh 来执行模型训练
- run_1.3b.sh 中可以设置参数，并调用对应的 main.py 来开始模型训练

#### 训练程序

训练程序：
- training/step1_supervised_finetuning/main.py

核心训练脚本，主要功能如下：
- 数据/模型的下载
- 模型训练
- 评价与测试用程序：prompt_eval.py
- 用于测试训练后的模型，并提供了微调前后的对比。


### deepspeed 命令


#### deepspeed ft 流程

模型微调完整流程：
- **数据**部分
  - 读取tokenizer: 从预训练模型中读取tokenizer
  - 读取处理数据 train_dataset, eval_dataset
  - 设置 train_sampler， eval_sampler
  - 设置 train_dataloader， eval_dataloader （使用DataLoader）
- **模型**部分
  - 设置DeepSpeed配置参数
  - 导入并实例化 model
  - 可选：LoRA设置
  - 准备需要优化的参数：optimizer_grouped_parameters
  - 设置 optimizer
  - 设置 lr_scheduler
  - 进行初始化 deepspeed.initialize
- **训练及评价**部分
  - 开始训练 forward，backward，参数更新
  - 评价，测试
  - 模型保存：
    - 注意ZeRO为3时，需要单独处理


#### 启动脚本概要

bash脚本 run_1.3b.sh 调用 main.py 训练，主要学习 main.py 程序。

run_1.3b.sh 脚本主要包含以下内容

```sh
deepspeed main.py \
   --data_path Dahoas/rm-static \
   --data_split 2,4,4 \
   --model_name_or_path facebook/opt-1.3b \
   --per_device_train_batch_size 8 \
   --per_device_eval_batch_size 8 \
   --max_seq_len 512 \
   --learning_rate 9.65e-6 \
   --weight_decay 0.1 \
   --num_train_epochs 2 \
   --gradient_accumulation_steps 1 \
   --lr_scheduler_type cosine \
   --num_warmup_steps 0 \
   --seed 1234 \
   --zero_stage $ZERO_STAGE \
   --deepspeed \
   --output_dir $OUTPUT \
   &> $OUTPUT/training.log
```


启动模式
- 单机多卡: 不用 hostfile
  - 未指定 hostfile 时, ds 会检测本机可用 GPU 数
  - include/exclude 正常使用, 但需要设置 localhost, `deepspeed --include localhost:1 ...`
  - `CUDA_VISIBLE_DEVICES` 控制可用 GPU 失效
- 多机多卡: 需要 hostfile 文件, 配合 include/exclude 指定部分节点
  - ds 会传播 NCCL and PYTHON 环境变量到各个节点
  - 如果想增加变量, 设置 dot 文件 `~/.deepspeed_env`, 格式 `NCCL_IB_DISABLE=1`;
  - 如果修改 dot 文件, 修改环境变量 `DS_ENV_FILE`
  - mpirun + DeepSpeed 或 AzureML: 安装 [mpi4py](https://pypi.org/project/mpi4py/)

```sh
deepspeed --hostfile=myhostfile <client_entry.py> <client args> \
  --deepspeed --deepspeed_config ds_config.json
```

启动模式: [gpt2/test_tune.sh](https://github.com/microsoft/DeepSpeedExamples/blob/master/training/autotuning/hf/gpt2/test_tune.sh)

```py
MODEL_NAME=gpt2
PER_DEVICE_TRAIN_BATCH_SIZE=1
HF_PATH=~/projects
NEPOCHS=1
NGPUS=16
NNODES=1
MAX_STEPS=200
OUTPUT_DIR=./output_b${PER_DEVICE_TRAIN_BATCH_SIZE}_g${NGPUS}_$MAX_STEPS

TEST=$1

if [ ${TEST} == "0" ]
then
    # python -m torch.distributed.launch -> torchrun
    torchrun --nproc_per_node=$NGPUS $HF_PATH/transformers/examples/pytorch/language-modeling/run_clm.py \
    --model_name_or_path $MODEL_NAME \
    --dataset_name wikitext \
    --dataset_config_name wikitext-2-raw-v1 \
    --do_train \
    --do_eval \
    --fp16 \
    --per_device_train_batch_size $PER_DEVICE_TRAIN_BATCH_SIZE \
    --learning_rate 2e-5 \
    --num_train_epochs $NEPOCHS \
    --output_dir ${OUTPUT_DIR}_0 \
    --overwrite_output_dir \
    --save_steps 0 \
    --max_steps $MAX_STEPS \
    --save_strategy "no"
elif [ ${TEST} == "z0" ]
then
    deepspeed --num_nodes=$NNODES --num_gpus=$NGPUS $HF_PATH/transformers/examples/pytorch/language-modeling/run_clm.py --deepspeed ../dsconfigs/ds_config_fp16_z0.json\
    --model_name_or_path $MODEL_NAME \
    --dataset_name wikitext \
    --dataset_config_name wikitext-2-raw-v1 \
    --do_train \
    --do_eval \
    --fp16 \
    --per_device_train_batch_size $PER_DEVICE_TRAIN_BATCH_SIZE \
    --learning_rate 2e-5 \
    --num_train_epochs $NEPOCHS \
    --output_dir ${OUTPUT_DIR}_z0 \
    --overwrite_output_dir \
    --save_steps 0 \
    --max_steps $MAX_STEPS \
    --save_strategy "no"
elif [ ${TEST} == "z1" ]
then
    deepspeed --num_nodes=$NNODES --num_gpus=$NGPUS $HF_PATH/transformers/examples/pytorch/language-modeling/run_clm.py --deepspeed ../dsconfigs/ds_config_fp16_z1.json\
    --model_name_or_path $MODEL_NAME \
    --dataset_name wikitext \
    --dataset_config_name wikitext-2-raw-v1 \
    --do_train \
    --do_eval \
    --fp16 \
    --per_device_train_batch_size $PER_DEVICE_TRAIN_BATCH_SIZE \
    --learning_rate 2e-5 \
    --num_train_epochs $NEPOCHS \
    --output_dir ${OUTPUT_DIR}_z1 \
    --overwrite_output_dir \
    --save_steps 0 \
    --max_steps $MAX_STEPS \
    --save_strategy "no"
elif [ ${TEST} == "z2" ]
then
    deepspeed --num_nodes=$NNODES --num_gpus=$NGPUS $HF_PATH/transformers/examples/pytorch/language-modeling/run_clm.py --deepspeed ../dsconfigs/ds_config_fp16_z2.json\
    --model_name_or_path $MODEL_NAME \
    --dataset_name wikitext \
    --dataset_config_name wikitext-2-raw-v1 \
    --do_train \
    --do_eval \
    --fp16 \
    --per_device_train_batch_size $PER_DEVICE_TRAIN_BATCH_SIZE \
    --learning_rate 2e-5 \
    --num_train_epochs $NEPOCHS \
    --output_dir ${OUTPUT_DIR}_z2 \
    --overwrite_output_dir \
    --save_steps 0 \
    --max_steps $MAX_STEPS \
    --save_strategy "no"
elif [ ${TEST} == "z3" ]
then
    deepspeed --num_nodes=$NNODES --num_gpus=$NGPUS $HF_PATH/transformers/examples/pytorch/language-modeling/run_clm.py --deepspeed ../dsconfigs/ds_config_fp16_z3.json\
    --model_name_or_path $MODEL_NAME \
    --dataset_name wikitext \
    --dataset_config_name wikitext-2-raw-v1 \
    --do_train \
    --do_eval \
    --fp16 \
    --per_device_train_batch_size $PER_DEVICE_TRAIN_BATCH_SIZE \
    --learning_rate 2e-5 \
    --num_train_epochs $NEPOCHS \
    --output_dir ${OUTPUT_DIR}_z3 \
    --overwrite_output_dir \
    --save_steps 0 \
    --max_steps $MAX_STEPS \
    --save_strategy "no"
elif [ ${TEST} == "tune" ]
then
    deepspeed --autotuning run --num_nodes=$NNODES --num_gpus=$NGPUS $HF_PATH/transformers/examples/pytorch/language-modeling/run_clm.py --deepspeed ../dsconfigs/ds_config_fp16_tune.json\
    --model_name_or_path $MODEL_NAME \
    --dataset_name wikitext \
    --dataset_config_name wikitext-2-raw-v1 \
    --do_train \
    --do_eval \
    --fp16 \
    --per_device_train_batch_size $PER_DEVICE_TRAIN_BATCH_SIZE \
    --learning_rate 2e-5 \
    --num_train_epochs $NEPOCHS \
    --output_dir ${OUTPUT_DIR}_tune \
    --overwrite_output_dir \
    --save_steps 0 \
    --max_steps $MAX_STEPS \
    --save_strategy "no"
elif [ ${TEST} == "fs" ]
then
    torchrun --nproc_per_node=$NGPUS $HF_PATH/transformers/examples/pytorch/language-modeling/run_clm.py \
    --model_name_or_path $MODEL_NAME \
    --dataset_name wikitext \
    --dataset_config_name wikitext-2-raw-v1 \
    --do_train \
    --do_eval \
    --fp16 \
    --per_device_train_batch_size $PER_DEVICE_TRAIN_BATCH_SIZE \
    --learning_rate 2e-5 \
    --num_train_epochs $NEPOCHS \
    --output_dir ${OUTPUT_DIR}_fs \
    --overwrite_output_dir \
    --save_steps 0 \
    --max_steps $MAX_STEPS \
    --save_strategy "no"
    --sharded_ddp zero_dp_2
fi
```


#### 启动脚本源码


[DeepSpeed/deepspeed/launch](https://github.com/microsoft/DeepSpeed/tree/master/deepspeed/launch) 目录下的文件

```sh
__init__.py         
constants.py        
launch.py           
launcher_helper.py  
multinode_runner.py 
runner.py # ds 主入口
```

[runner.py](https://github.com/microsoft/DeepSpeed/tree/master/deepspeed/autotuning/runner.py)

```py
from ..autotuning import Autotuner

def run_autotuning(args, active_resources):
    # autotune 初始化
    tuner = Autotuner(args, active_resources)
    logger.info("[Start] Running autotuning")
    # tune: 寻参模式
    tuner.tune()
    tuner.print_tuning_results()
    # 保存最优参数
    logger.info("[End] Running autotuning")
    tuner.write_optimal_config()
    # 启动训练任务
    if args.autotuning == "run":
        tuner.run_after_tuning()

def main(args=None):
    args = parse_args(args)
    #...
    # 当前可用节点信息
    active_resources = parse_inclusion_exclusion(resource_pool, args.include, args.exclude)
    #...
    # 只要 autotuning 非空, 就启用 autotune
    if args.autotuning != "":
        run_autotuning(args, active_resources)
        return
```

Autotuner 类定义

```py
from .config import DeepSpeedAutotuningConfig
from .constants import *
from .scheduler import ResourceManager
from .tuner import GridSearchTuner, RandomTuner, ModelBasedTuner
from .utils import *

class Autotuner:
    """The DeepSpeed Autotuner automatically discovers the optimal DeepSpeed configuration that delivers good training speed. The Autotuner uses model information, system information, and heuristics to efficiently tune system knobs that affect compute and memory efficiencies, such as ZeRO optimization stages, micro-batch sizes, and many other ZeRO optimization configurations. It not only reduces the time and resources user spend on tuning, but also can discover configurations better than hand-tuned methods.
    Autotuning with DeepSpeed requires no code change from DeepSpeed users. Please refer to the README for usage details.
    """
    def __init__(self, args, active_resources):
        self.args = args
        self.selected_exp_dir = None
        #...
        # 实例化资源管理器 set the active resource for the autotuner resource manager
        self.rm = self._get_resource_manager(active_resources)
        # 获取实验资源信息:node,gpu数目 get resource requirement for each autotuning experiment
        self.exp_num_nodes, self.exp_num_gpus = self._get_exp_resources(args)
    
    def _get_resource_manager(self, active_resources):
        """Initialize and return a resource manager
        Args:
            active_resources ([dict]): A dictionary of hostname and its slots (GPUs), e.g. {"worker-0": "0,1,2,3,4,5,6,7,8"}
        Raises:
            RuntimeError: raises the error if no GPU is available
        Returns:
            [ResourceManager]: A resource manager that schedules and runs autotuning experiments.
        """
        logger.info(f"active_resources = {active_resources}")
        hosts = []
        ngpus_per_node = 100
        # 遍历当前可用主机
        for hostname, slots in active_resources.items():
            hosts.append(hostname)
            ngpus_per_node = min(len(slots), ngpus_per_node)
        assert ngpus_per_node > 0, "no gpu is available"
        return ResourceManager(args=self.args,
                               hosts=hosts,
                               num_gpus_per_node=ngpus_per_node,
                               results_dir=self.results_dir,
                               exps_dir=self.exps_dir,
                               arg_mappings=self.autotuning_config.arg_mappings)
    def tune(self): # 参数搜索
        """ Tunes Zero stages, micro batch size per GPU, and other Zero configurations. Performance metrics of different tuning spaces are recorded in self.records.
        """
        if has_mlflow:
            self.mlflow_parent_id = os.environ['MLFLOW_RUN_ID']
            mlflow.start_run(run_id=self.mlflow_parent_id)

        self.start_time = time.time()
        if self.fast_enabled():
            logger.info(f"Fast mode is enabled. Tuning micro batch size only.")

        # model info profile run with DEFAULT_MIN_MEM_CONFIG
        model_info = self.model_info_profile_run()
        # ...

    def model_info_profile_run(self):
        """Does a model information profiling experiment that collects the number of model parameters and activation memory.\
            The experiment produces a "profile_model_info" folder under self.results_dir.
        Returns:
            [dict]: a model information dictionary, e.g., {"num_params": 335144976, "trainable_num_params": 335144976, "activation_mem_per_gpu": 324358144, "rank": 0}
        """
        logger.info("Starting model info profile run.")
        model_info = self.autotuning_config.model_info
        if model_info and MODEL_INFO_NUM_PARAMS in model_info:
            return model_info

        ds_config = copy.deepcopy(self.user_config)
        replace_dict(ds_config, DEFAULT_MIN_MEM_CONFIG)

        model_info_path = os.path.join(self.results_dir, "profile_model_info", "model_info.json")
        ds_config[AUTOTUNING] = {"enabled": True, "model_info_path": model_info_path, "model_info": {"profile": True}}

        exp_config = {}
        exp_name = "profile_model_info"
        exp_config['name'] = exp_name
        exp_config[DS_CONFIG] = ds_config
        exp_config['num_gpus'] = self.exp_num_gpus
        exp_config['num_nodes'] = self.exp_num_nodes
        exp_config['hostfile'] = self.args.hostfile
        exp_path = os.path.join(self.exps_dir, f'{exp_name}.json')
        # 读取实验配置信息
        with open(exp_path, 'w', buffering=BUFSIZE) as fd:
            json.dump(exp_config, fd)
            fd.flush()
            os.fsync(fd)
        # 安排实验任务
        self.rm.schedule_experiments([exp_path])
        # 启动实验任务: 多线程
        self.rm.run()

        for exp_id, (exp_json, err) in self.rm.finished_experiments.items():
            self.rm.clear()
            if err:
                logger.error(f"The model is not runnable with DeepSpeed with error = {err}")
                return None

        if os.path.exists(model_info_path):
            with open(model_info_path, 'r') as f:
                model_info = hjson.load(f)
                return model_info
```

#### 启动参数


JSON文件 / Dict字典 两种启动传参
- （1）JSON文件
- （2）Dict字典

```sh
# (1) Json 文件
deepspeed  train.py --deepspeed  --deepspeed_config ds_config.json
# (2) 字典
ds_config = {"train_batch_size": 16}
engine, _, _, _ = deepspeed.initialize(model=netconfig=ds_config)
deepspeed  train.py --deepspeed 
```

指定GPU运行

```sh
# 本机第0张卡
deepspeed --include="localhost:0"  train.py --deepspeed --deepspeed_config xxx.jso
```

#### 参数详解


DeepSpeed分布式启动器各命令含义

| Argument | Meaning | Example |
| --- | --- | --- |
| `master_port` | 主节点端口号 | `--master_port 29500` |
| `master_addr` | 主节点ip | `--master_addr=10.51.97.28` (ifconfig->eth0->inet) |
| `nnodes` | 节点数 | 两台机器，`--nnodes=2` |
| `node_rank` | 节点rank，以第一台机器为0开始递增 | `--node_rank=0` master,即主节点rank |
| `nproc_per_node` | 每个节点进程数 | 一个节点使用8张卡，`nproc_per_node=8` |


##### 节点通信

NCCL(NVIDIA Collective Communications Library) 参数使用说明

| 参数 | 意义 | 说明 |
| --- | --- | --- |
| NCCL_IB_DISABLE | 禁用IB网卡传输端口 | IB (InfiniBand)是一种用于高性能计算的计算机网络通信标准。 |
| NCCL_SHM_DISABLE | 禁用共享内存传输 | 共享内存(SHM)传输支持运行在相同处理单元/机器中的实体之间的快速通信，这依赖于主机操作系统提供的共享内存机制 |
| NCCL_P2P_DISABLE | 禁用GPU之间信息的传输 | P2P使用CUDA和NVLink直接实现GPU之间的传输与访问 |

关于如何查看GPU是否支持 NVLINK

使用命令

```sh
nvidia-smi topo -p2p n # 
```

结果
- V100 上显示结果 (不支持）
- A800 上显示结果 (支持
- ![](https://pic2.zhimg.com/80/v2-c73b0b5e20821bffa1c52b2d79884915_1440w.webp)

##### deepspeed 参数

deepspeed 参数列表

```sh
usage: deepspeed [-h] 
  [-H HOSTFILE] 
  [-i INCLUDE] 
  [-e EXCLUDE] 
  [--num_nodes NUM_NODES] 
  [--min_elastic_nodes MIN_ELASTIC_NODES]
  [--max_elastic_nodes MAX_ELASTIC_NODES] 
  [--num_gpus NUM_GPUS] 
  [--master_port MASTER_PORT] 
  [--master_addr MASTER_ADDR]
  [--launcher LAUNCHER] 
  [--launcher_args LAUNCHER_ARGS] 
  [--module] 
  [--no_python] 
  [--no_local_rank] 
  [--no_ssh_check]
  [--force_multi] 
  [--save_pid] 
  [--enable_each_rank_log ENABLE_EACH_RANK_LOG] 
  [--autotuning {tune,run}]
  [--elastic_training] 
  [--bind_cores_to_rank] 
  [--bind_core_list BIND_CORE_LIST] 
  [--ssh_port SSH_PORT]
  user_script ...
```

参数含义

```sh
deepspeed -h

usage: deepspeed [-h] [-H HOSTFILE] [-i INCLUDE] [-e EXCLUDE] [--num_nodes NUM_NODES] [--min_elastic_nodes MIN_ELASTIC_NODES]
                 [--max_elastic_nodes MAX_ELASTIC_NODES] [--num_gpus NUM_GPUS] [--master_port MASTER_PORT] [--master_addr MASTER_ADDR]
                 [--launcher LAUNCHER] [--launcher_args LAUNCHER_ARGS] [--module] [--no_python] [--no_local_rank] [--no_ssh_check]
                 [--force_multi] [--save_pid] [--enable_each_rank_log ENABLE_EACH_RANK_LOG] [--autotuning {tune,run}]
                 [--elastic_training] [--bind_cores_to_rank] [--bind_core_list BIND_CORE_LIST] [--ssh_port SSH_PORT]
                 user_script ...

DeepSpeed runner to help launch distributed multi-node/multi-gpu training jobs.

# 位置参数 positional arguments: 
  user_script  # 要执行的训练脚本入口文件 User script to launch, followed by any required arguments.
  user_args    # 入口脚本参数

# 可选参数 optional arguments:
  -h, --help            show this help message and exit
  -H HOSTFILE, --hostfile HOSTFILE # 机器资源池
    # Hostfile path (in MPI style) that defines the resource pool available to the job (e.g., worker-0 slots=4) (default: /job/hostfile)
  -i INCLUDE, --include INCLUDE # 指定可用硬件资源
    # Specify hardware resources to use during execution. String format is NODE_SPEC[@NODE_SPEC ...], where NODE_SPEC=NAME[:SLOT[,SLOT ...]]. If :SLOT is omitted, include all slots on that host. 
    # Example: -i "worker-0@worker-1:0,2" will use all slots on worker-0 and slots [0, 2] on worker-1. (default: )
  -e EXCLUDE, --exclude EXCLUDE # 指定不可用的硬件资源
    # Specify hardware resources to NOT use during execution. Mutually exclusive with --include. Resource formatting is the same as --include. 
    # Example: -e "worker-1:0" will use all available resources except slot 0 on worker-1. (default: )
  --num_nodes NUM_NODES # 节点总数，使用 hostfile 中 top N 机器
    # Total number of worker nodes to run on, this will use the top N hosts from the given hostfile. (default: -1)
  --min_elastic_nodes MIN_ELASTIC_NODES # 训练室弹性节点数：最小
    # Minimum number of nodes to run elastic training on. Default is 1 when elastic training is enabled (default: -1)
  --max_elastic_nodes MAX_ELASTIC_NODES # 训练室弹性节点数：最大
    # Maximum number of nodes to run elastic training on. Default is num_nodes when elastic training is enabled (default: -1)
  --num_gpus NUM_GPUS, --num_accelerators NUM_GPUS # 每个节点上最多使用的gpu数
    # Max number of GPUs to use on each node, will use [0:N) GPU ids on each node. (default: -1)
  --master_port MASTER_PORT # 主节点端口,用于分布式训练的通信环节
    # (optional) Port used by PyTorch distributed for communication during training. (default: 29500)
  --master_addr MASTER_ADDR # 主节点ip地址
    # (optional) IP address of node 0, will be inferred via 'hostname -I' if not specified. (default: )
  --launcher LAUNCHER   # 多机并行方式
    # (optional) choose launcher backend for multi-node training. Options currently include PDSH, OpenMPI, MVAPICH, SLURM, MPICH, IMPI. (default: pdsh)
  --launcher_args LAUNCHER_ARGS # 多级并行参数
    # (optional) pass launcher specific arguments as a single quoted argument. (default: )
  --module  # Change each process to interpret the launch script as a Python module, executing with the same behavior as 'python -m'. (default: False)
  --no_python  # 忽略Python脚本,执行执行 Skip prepending the training script with 'python' - just execute it directly. (default: False)
  --no_local_rank # 调用用户脚本时忽略local_rank参数 Do not pass local_rank as an argument when calling the user's training script. (default: False)
  --no_ssh_check # 不执行ssh验证 Do not perform ssh check in multi-node launcher model (default: False)
  --force_multi  # 强制多机模式 Force multi-node launcher mode, helps in cases where user wants to launch on single remote node. (default: False)
  --save_pid     # Save file containing launcher process id (pid) at /tmp/<main-pid>.ds, where <main-pid> is the pid of the first process that invoked `deepspeed`. Useful when launching deepspeed processes programmatically. (default: False)
  --enable_each_rank_log ENABLE_EACH_RANK_LOG # 重定向每个节点的标准输出、错误日志
    # redirect the stdout and stderr from each rank into different log files (default: None)
  --autotuning {tune,run} # 训练前用 autotuner 探索最佳参数, tune 只调参, run 调参后择优运行
    # Run DeepSpeed autotuner to discover optimal configuration parameters before running job. (default: )
  --elastic_training    # 启用弹性训练 Enable elastic training support in DeepSpeed. (default: False)
  --bind_cores_to_rank  # 绑定 Bind each rank to different cores of the host (default: False)
  --bind_core_list BIND_CORE_LIST # 绑定
    # List of cores to bind to with comma separated list of numbers and range. i.e. 1,3-5,7 => [1,3,4,5,7]. When not specified, all cores on system would be used rank binding (default: None)
  --ssh_port SSH_PORT   # ssh端口,用于远程连接 SSH port to use for remote connections (default: None)
```

hostfile 示例

hostfile.txt

```js
// ip  gpu数
10.2.180.1 slots=2
10.2.180.2 slots=2
10.2.180.3 slots=2
```


##### 超参优化 autotuner

2021年11月15日，DeepSpeed 发布**自动化训练策略**方案：
- [Autotuning 官方文档](https://www.deepspeed.ai/tutorials/autotuning/)
- 本质：
  - 对 ZeRO stage 和 stage 相对应的ZeRO配置，以及采用**梯度累计**策略下micro_batch_size大小的**自动化搜索**。 
- 总结：Autotuning 本质是**超参数搜索**，并没有对数据并行、模型并行的策略进行修改。 
  - 根据不同超参数配置，自动生成多个实验来计算不同配置下的性能，并从中选择最优的超参数配置。 
- 不足：
  - Autotuning 显存计算方法跟实现逻辑有区别，且实测 ZeRO3 面临着显存泄露问题，要重新实现模型来规避。
  - 显存计算没考虑 torch在cuda初始化时所产生的固定开销。
- 源码参考: [Autotuning: 来自DeepSpeed的超参数自动搜索方案](https://zhuanlan.zhihu.com/p/435112923)

注意：
1. DeepSpeed 团队把前向过程产生的中间结果(intermediate results 或feature_maps或intermediate activation)叫做激活值(activation)
2. ZeRO stages, micro-batch sizes 和其他配置可被用户配置覆盖。

Autotuning 流程
- (1) Autotuner 先做 profile 工作，分析所需运行模型的参数量以及激活值的内存。 即跑一遍前向然后结束进程
  - `Autotuner.model_info_profile_run()` 起一个小experiment, 获取参数量和激活值大小
  - `ResourceManager.run()` 调用 `self.run_job(exp, reservations)`，其中reservations为可用GPU设备信息。
  - `ResourceManager.run_job(exp, reservations)` 启动线程(thread)运行run_experiment函数
  - `run_experiment(exp, reservations, user_script, user_args)` 利用subprocess库执行cmd命令
    - 示例：`deepspeed --force_multi --include localhost:2 --master_port 12345 my_model_train.py --ds_config_path ds_config.json`
- (2) Autotuner 以`[0, 1, 2, 3]`顺序先搜索 ZeRO stage，估计每个GPU在训练模型时所需的最小memory(ZeRO实例化时所需的显存量)，并与当前GPU可用显存进行比较。如果小于GPU可用显存，则说明该stage可以运行。Autotuner 尝试搜索该stage下每个GPU的micro-batch的大小，以及其他的ZeRO设置：
- (3) 如果当前 ZeRO stage 最优设置性能亚于之前其他ZeRO stage的方法，则之后其他Stage的搜索会终止。（因为是按顺序搜索的，默认情况下，前面的stage的最优策略应该batch-size会更小）
- (4) 最后，全局最优设置会通过log的文件的形式告知用户。如果`--autotune`设置为run，还会直接开始训练。

支持: 随机/网格/模型搜索


```py
exps = self._generate_experiments(tuning_space, max_train_batch_size_per_gpu)

logger.info(f'Tuner type is {self.autotuning_config.tuner_type}')
if self.autotuning_config.tuner_type == AUTOTUNING_TUNER_MODELBASED:
    t = ModelBasedTuner(exps, self.rm, self.metric(), tuning_space)
elif self.autotuning_config.tuner_type == AUTOTUNING_TUNER_RANDOM:
    t = RandomTuner(exps, self.rm, self.metric())
else:
    t = GridSearchTuner(exps, self.rm, self.metric())

sample_size = len(self.rm.nodes) * self.rm.num_gpus_per_node // (self.exp_num_gpus * self.exp_num_nodes)
num_exps = t.tune(sample_size=sample_size,
                  n_trials=self.autotuning_config.tuner_num_trials,
                  early_stopping=self.autotuning_config.tuner_early_stopping)
exp = t.best_exp
metric_val = t.best_metric_val
```

官方示例 GPT-2 实践
- [gpt2 autotuning](https://github.com/microsoft/DeepSpeedExamples/tree/master/training/autotuning/hf/gpt2)

使用方法
- 增加配置文件 `ds_config.json`, 开启自动寻参功能 `"autotuning": {"enabled": true}`, `arg_mappings` 中指定个别参数映射关系
- 启动脚本 `test_tune.sh` 
  - deepspeed 命令行中增加参数: `--autotuning run/tune`


`ds_config.json` 文件

```json
{
  "train_micro_batch_size_per_gpu": "auto",
  "fp16": {
    "enabled": true
  },
  "autotuning": {
    "enabled": true,
    "arg_mappings": {
      "train_micro_batch_size_per_gpu": "--per_device_train_batch_size",
      "gradient_accumulation_steps ": "--gradient_accumulation_steps"
    }
  }
}
```

训练脚本
- transformers 提供的pytorch模型源码 [examples/pytorch/language-modeling/run_clm.py](https://github.com/huggingface/transformers/blob/main/examples/pytorch/language-modeling/run_clm.py)
- DeepSpeedExamples 训练脚本 [test_tune.sh](https://github.com/microsoft/DeepSpeedExamples/blob/master/training/autotuning/hf/gpt2/test_tune.sh)
  - 支持多种模式: `0`(torchrun分布式), `z1`, `z2`, `z3`, `tune`(ds 自动寻参训练), `fs`


```sh
deepspeed --autotuning run --num_nodes=$NNODES --num_gpus=$NGPUS $HF_PATH/transformers/examples/pytorch/language-modeling/run_clm.py --deepspeed $DS_CONFIG\
  --model_name_or_path $MODEL_NAME \
  --dataset_name wikitext \
  --dataset_config_name wikitext-2-raw-v1 \
  --do_train \
  --do_eval \
  --fp16 \
  --per_device_train_batch_size $PER_DEVICE_TRAIN_BATCH_SIZE \
  --gradient_accumulation_steps $GRADIENT_ACCUMULATION_STEPS \
  --learning_rate 2e-5 \
  --num_train_epochs $NEPOCHS \
  --output_dir ${OUTPUT_DIR} \
  --overwrite_output_dir
```


踩坑：
- [test_tune.sh](https://github.com/microsoft/DeepSpeedExamples/blob/master/training/autotuning/hf/gpt2/test_tune.sh)
  - 更新 example示例代码里的 HF_PATH
  - `python -m torch.distributed.launch` -> `torchrun`
- [cannot import name 'is_torch_xla_available' from 'transformers'](https://github.com/huggingface/transformers/issues/29749)
  - 编辑 `$HF_PATH/transformers/examples/pytorch/language-modeling/run_clm.py` 59 行, 注释 `check_min_version("4.41.0.dev0")`, 不做版本要求


```sh
# 环境准备
# transformers (4.12.0.dev0)
pip install transformers -U # 并关闭 59行版本检测, 否则 cannot import name 'is_torch_xla_available' from 'transformers
# datasets (1.11.0)
pip install datasets # 否则 ConnectionError: Couldn't reach 'wikitext' on the Hub (ConnectTimeout)
# (1) transformers 版本问题: 4.38 -> 4.40, 关闭 59行版本检测
# cannot import name 'is_torch_xla_available' from 'transformers
# (2) shell if 判断报错: zsh -> bash
sh test_tune.sh tune # if [] 判断语法错误
bash test_tune.sh tune # 改成 bash
# (3) 
# [ERROR] [autotuner.py:700:model_info_profile_run] The model is not runnable with DeepSpeed with error = No module named 'evaluate'
bash test_tune_wqw.sh tune

```



##### main.py 参数

```sh
usage: main.py [-h] [--data_path [DATA_PATH ...]] [--data_split DATA_SPLIT] [--data_output_path DATA_OUTPUT_PATH] [--model_name_or_path MODEL_NAME_OR_PATH]
               [--num_padding_at_beginning NUM_PADDING_AT_BEGINNING] 
               [--per_device_train_batch_size PER_DEVICE_TRAIN_BATCH_SIZE]
               [--per_device_eval_batch_size PER_DEVICE_EVAL_BATCH_SIZE] 
               [--max_seq_len MAX_SEQ_LEN] 
               [--learning_rate LEARNING_RATE]
               [--minimum_learning_rate MINIMUM_LEARNING_RATE] 
               [--weight_decay WEIGHT_DECAY] 
               [--num_train_epochs NUM_TRAIN_EPOCHS]
               [--gradient_accumulation_steps GRADIENT_ACCUMULATION_STEPS]
               [--lr_scheduler_type {linear,cosine,cosine_with_restarts,polynomial,constant,constant_with_warmup}] 
               [--num_warmup_steps NUM_WARMUP_STEPS]
               [--class_weight CLASS_WEIGHT] 
               [--device DEVICE] 
               [--output_dir OUTPUT_DIR] 
               [--seed SEED] 
               [--gradient_checkpointing] 
               [--dropout DROPOUT] 
               [--offload]
               [--dtype {fp16,bf16}] 
               [--zero_stage ZERO_STAGE] 
               [--lora_dim LORA_DIM] 
               [--lora_module_name LORA_MODULE_NAME] 
               [--only_optimize_lora]
               [--lora_learning_rate LORA_LEARNING_RATE] 
               [--eval_interval EVAL_INTERVAL] 
               [--eval_iters EVAL_ITERS] 
               [--print_steps PRINT_STEPS] 
               [--save_steps SAVE_STEPS]
               [--compute_fp32_loss] 
               [--enable_tensorboard] 
               [--tensorboard_path TENSORBOARD_PATH] 
               [--add_eot_token] 
               [--im_start IM_START] 
               [--im_end IM_END]
               [--system SYSTEM] 
               [--user USER] 
               [--assistant ASSISTANT] 
               [--train_data_path TRAIN_DATA_PATH] 
               [--val_data_path VAL_DATA_PATH]
               [--test_data_path TEST_DATA_PATH] 
               [--inference] 
               [--restore] 
               [--checkpoint CHECKPOINT] 
               [--debug] 
               [--model_name MODEL_NAME] 
               [--template TEMPLATE]
               [--label1_dim LABEL1_DIM] 
               [--label2_dim LABEL2_DIM] 
               [--label3_dim LABEL3_DIM] 
               [--chinese_percent CHINESE_PERCENT] 
               [--only_query]
               [--cut_flag_token CUT_FLAG_TOKEN] 
               [--cut_flag_token_id CUT_FLAG_TOKEN_ID] 
               [--deepspeed] 
               [--deepspeed_config DEEPSPEED_CONFIG] 
               [--deepscale]
               [--deepscale_config DEEPSCALE_CONFIG] 
               [--deepspeed_mpi]
```


结合 main.py 程序，将参数分为三大类

|参数|类型|含义|备注|
|---|---|---|---|
|`data_path`|数据|huggingface数据路径|Dahoas/rm-static|
|`data_split`|数据|3个阶段数据拆分方式|2,4,4 是 step1，2，3 分配的数据比例|
|`max_seq_len`|数据|最大序列长度（超过长度会阶段）||
|`data_output_path`|数据|输出数据**本地**路径||
|`model_name_or_path`|模型|模型名称/路径,可以是hf|facebook/opt-1.3b|
|`lora_dim`|模型|如果大于0，则用LoRA优化||
|`lora_module_name`|模型|设置LoRA范围|可只针对 decoder.layers|
|`only_optimize_lora`|模型|是否只优化LoRA||
|`per_device_train_batch_size`|训练|训练时每个GPU的Batch Size||
|`per_device_eval_batch_size`|训练|评价时每个GPU的Batch Size||
|`learning_rate`|训练|学习率||
|`weight_decay`|训练|权重衰减，防止过拟合||
|`num_train_epochs`|训练|训练 epoch 数||
|`gradient_accumulation_steps`|训练|梯度更新步数||
|`lr_scheduler_type`|训练|learning rate的调整策略|linear, cosine|
|`zero_stage`|deepspeed|DeepSpeed工具中的zero方式|0，1，2，3|
|`offload`|deepspeed|ZeRO-Offload利用CPU资源辅助降低GPU计算和内存需求||
|`local_rank`|deepspeed|标识当前 GPU 设备的本地排名（本机排名，与global-rank不同）||
|`gradient_checkpointing`|deepspeed|降低训练中的内存消耗||
|`seed`|其它|随机排序种子||
|`output_dir`|其它|模型存储目录||
|||||
|||||

官方文档: [DeepSpeed Configuration JSON](https://www.deepspeed.ai/docs/config-json/)

#### 数据源

**数据**相关

```js
data_path        : 数据路径，huggingface数据， 比如：Dahoas/rm-static
data_split       : 数据的拆分方式，比如 2,4,4 是为step1，2，3分配的数据比例
max_seq_len      : 最大序列长度（超过长度会被截掉）
data_output_path : 相关数据的存储地址（local storage，不能是shared storage）
```

#### 模型

**模型**相关

```js
model_name_or_path : 模型名称或路径，huggingface模型，比如：facebook/opt-1.3b
lora_dim           : 如果大于0，则使用LoRA优化
lora_module_name   : 设置LoRA的范围，比如可以只针对 decoder.layers
only_optimize_lora : 是否只优化LoRA的参数
```

#### 训练

**训练**相关

```js
per_device_train_batch_size : 训练时的 Batch size (per device： 每个GPU的Size)
per_device_eval_batch_size  : 评价时的 Batch size (per device)
learning_rate               : 学习率
weight_decay                : 权重衰减，防止模型过拟合的技术。
num_train_epochs            : 训练 epoch 数
gradient_accumulation_steps : 累积多少个 mini-batch 的梯度后再进行一次参数更新。
lr_scheduler_type           : learning rate的调整策略，比如 linear, cosine
```

注意：
- `train_batch_size` = `train_micro_batch_size_per_gpu` * `gradient_accumulation_steps` * `number of GPUs`
- ![](https://pic3.zhimg.com/80/v2-58e440f8f43a73dbc3578394a61efde2_1440w.webp)
- `train_micro_batch_size_per_gpu` 是单个GPU上前向、反向的实际 batch_size
- `gradient_accumulation_steps` 是梯度累积步数
- 指定其中2个参数, 最后1个参数可由 deepspeed 自动推导

```json
{
 "train_batch_size": 16, //总batch 
 "train_micro_batch_size_per_gpu": 8,
 "gradient_accumulation": 1
} //2个GPU
```

#### 可视化监控

支持多种[可视化监控](https://www.deepspeed.ai/tutorials/monitor/)
- PyTorch’s TensorBoard, WandB, and simple CSV files

开启TensorBoard可视化

```json
"tensorboard": {
  "enabled": true,  //开启可视化
  "output_path": "log/", //可视化文件保存路径
  "job_name": "2023年08月15日16:28:06" //此次实验名称，作为子文件夹
}

//========================
{
  "tensorboard": {
    "enabled": true,
    "output_path": "output/ds_logs/",
    "job_name": "train_bert"
  }
  "wandb": {
    "enabled": true,
    "team": "my_team",
    "group": "my_group",
    "project": "my_project"
  }
  "csv_monitor": {
    "enabled": true,
    "output_path": "output/ds_logs/",
    "job_name": "train_bert"
  }
}

```


#### deepspeed

deepspeed 相关

```js
zero_stage  : 这个对应者DeepSpeed工具中的zero方式，分别是0，1，2，3
offload     : ZeRO-Offload 通过利用主机CPU上的计算和内存资源来执行优化器，从而减少此类模型的GPU计算和内存需求。
local_rank  : 分布式训练时的一个变量，用于标识当前 GPU 设备的本地排名（本机排名，与global-rank不同）
gradient_checkpointing : 降低深度学习模型训练过程中内存消耗的技术
```

deepspeed 核心参数
- `__init__.py` 文件中已定义, 不能重复定义，否则报错
- 

```js
deepspeed : deepspeed 开关, 对后端无影响
deepspeed_config : deepspeed 配置文件 json 格式
deepscale : deepspeed 开关, 废弃的 '旧版deepspeed'
deepscale_config : deepspeed 配置文件 json 格式('旧版deepspeed_config')
deepspeed_mpi: 启用 MPI 模式(CPU 并行)
```


其他

```js
seed        : 随机排序是的seed
output_dir  : 模型的存储目录
```

#### 分布式参数

args.`local_rank`
- `local_rank` 是分布式训练时变量，标识当前 GPU 设备的**本地排名**（local rank）。
- `args.local_rank = -1`，表示代码不在分布式设置下运行，仅使用**单个 GPU** 训练。
- `args.local_rank ≠ -1`，代码在分布式设置下运行，当前 GPU 设备被分配了一个**唯一**的本地排名。
  - 代码会将设备设置为指定的 GPU（`torch.device("cuda", args.local_rank)`），并使用 `deepspeed.init_distributed()` 函数调用初始化分布式后端。

注意：
- PyTorch 中也有分布式初始化方法 `torch.distributed.init_process_group()` 函数。
- 但是当使用 DeepSpeed 库时，不要替换为 `deepspeed.init_distributed()`。

args.`global_rank`
- 分布式训练中，每个进程都有唯一的全局排名，用于标识该进程在分布式环境中的位置。
- 全局排名的范围: `0 ~ world_size-1`，其中 `world_size` 是整个分布式环境中**进程总数**。
- 本程序中通过 `torch.distributed.get_rank()` 来读取 `global_rank`， 本函数在初始化分布式后端之后才能调用。

torch.distributed.`barrier`()
- torch.distributed.barrier() 是同步函数，用于分布式环境中同步各个进程的状态。
- 调用该函数时，进程会阻塞等待，直到所有进程都调用了该函数之后，才会解除阻塞并继续执行后面的代码。

分布式训练中，torch.distributed.barrier() 通常用于同步各个进程的梯度更新。
- 每个进程完成一轮前向传播和反向传播后，要同步各自的梯度，并且等待其他进程完成同样的操作，才能进行下一轮更新。
- 这时用 torch.distributed.barrier() 函数实现同步。

另外一个用法，在模型参数并行训练时，数据的读取只需要在 local_rank 为 0 的GPU上进行，其他进程使用 torch.distributed.barrier() 来阻塞来等待数据读取完成。


指定GPU运行

```sh
# 本机第0张卡
deepspeed --include="localhost:0"  train.py --deepspeed --deepspeed_config xxx.json
```

#### 数据处理


##### 分词

DS-Chat 使用的 tokenizer 来自预训练模型
- Hugging Face Transformers 库中的 AutoTokenizer 类实例化预训练模型的 tokenizer。
- AutoTokenizer 类自动选择并加载对应的 tokenizer，避免了手动选择的步骤。

```py
tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, fast_tokenizer=True)
tokenizer.pad_token = tokenizer.eos_token
```

AutoTokenizer.`from_pretrained`() 函数有两个必选参数
- `model_name_or_path` 预训练模型的名称或路径，例如: "bert-base-uncased" 或 "/path/to/model/directory"。 
- `fast_tokenizer`: 是否用**快速 tokenizer**。
  - 如果为 True，则会选择使用 Rust 实现的 tokenizer，速度更快；
  - 否则使用 Python 实现的 tokenizer。默认为 True。


##### 数据准备

数据准备函数: `create_prompt_dataset`

```py
    train_phase = 1
    train_dataset, eval_dataset = create_prompt_dataset(
        args.local_rank, args.data_path, args.data_split,
        args.data_output_path, train_phase, args.seed, tokenizer,
        args.max_seq_len)
```

说明
- `local_rank` 数据下载等基本处理只在local rank为 0 的 GPU 上执行。每个node上只处理一次数据即可。 -
- `data_output_path` 设定为 local storage path，分布式训练时存储本地数据用的。

初始化sampler
- 单GPU 用RandomSampler和SequentialSampler
- 分布式处理使用DistributedSampler。

sampler 主要用来设置数据采样顺序。
- 比如随机采样来提高模型的鲁棒性。

```py
    # DataLoaders creation:
    if args.local_rank == -1:
        train_sampler = RandomSampler(train_dataset)
        eval_sampler = SequentialSampler(eval_dataset)
    else:
        train_sampler = DistributedSampler(train_dataset)
        eval_sampler = DistributedSampler(eval_dataset)
```

数据读取使用 PyTorch 标准的 DataLoader 来处理。
- Dataloader 不仅可以设置sampler定义采样方式，还可以自动进行批处理，并且支持多进程数据加载。

```py
    train_dataloader = DataLoader(train_dataset,
                                  collate_fn=default_data_collator,
                                  sampler=train_sampler,
                                  batch_size=args.per_device_train_batch_size)
    eval_dataloader = DataLoader(eval_dataset,
                                 collate_fn=default_data_collator,
                                 sampler=eval_sampler,
                                 batch_size=args.per_device_eval_batch_size)
```


#### 模型


##### 模型初始化

(1) **模型初始化**

对模型进行初始化。

```py
model = create_hf_model(AutoModelForCausalLM, args.model_name_or_path,
                        tokenizer, ds_config)
```

其中 AutoModelForCausalLM 是 Hugging Face Transformers 库中的一个类，能够自动选择并加载适当的预训练 Transformer 模型，它支持多种预训练 Transformer 模型，包括 GPT-2、GPT、CTRL、Transformer-XL、XLNet 和 XLM 等。使用该类时，您只需指定模型的名称或路径即可自动加载对应的模型。

具体实现代码，可以参考：utils/model/model_utils.py。

##### LoRA

(2) **LoRA**

LoRA
- 当lora_dim>0时，用LoRA技术对模型进行调整。 从而让模型的优化参数大幅度的变少，改善优化的效率。

通常使用LoRA技术，不仅可以减少参数量，还能进一步改善性能。

因为，这种bottleneck的网络设计，可以防止过拟合，提高模型的鲁棒性。

```py
    if args.lora_dim > 0:
        model = convert_linear_layer_to_lora(model, args.lora_module_name, args.lora_dim)
        if args.only_optimize_lora:
            model = only_optimize_lora_parameters(model)
```

提取需要被优化的参数 optimizer_grouped_parameters

```py
    # Split weights in two groups, one with weight decay and the other not.
    optimizer_grouped_parameters = get_optimizer_grouped_parameters(
        model, args.weight_decay)

    AdamOptimizer = DeepSpeedCPUAdam if args.offload else FusedAdam
    optimizer = AdamOptimizer(optimizer_grouped_parameters,
                              lr=args.learning_rate,
                              betas=(0.9, 0.95))
```

上面代码中，get_optimizer_grouped_parameters() 函数被用来将权重分成两组，一组需要应用权重衰减，另一组则不需要。该函数通过遍历模型的所有参数，并检查参数名称是否包含 bias 或 LayerNorm 等特殊字符串，来区分需要应用权重衰减的参数和不需要的参数。

分组原因： 
- 对于参数名称中不包含 bias 或 LayerNorm 等特殊字符串的参数，我们认为它们是需要应用权重衰减的参数。对于这些参数，通常会将它们的权重矩阵与权重衰减超参数相乘，以降低它们的权重。与此相反，对于参数名称中包含 bias 或 LayerNorm 等特殊字符串的参数，我们认为它们是不需要应用权重衰减的参数。这是因为 bias 或 LayerNorm 参数通常只是用来偏移或缩放其他层的输出，而不是真正的权重参数。通过将权重分成两组，并分别应用权重衰减和不应用权重衰减，我们可以更好地控制模型的复杂度，从而提高模型的泛化性能。

然后设置Optimizer优化器，根据参数不同会选择 DeepSpeedCPUAdam 或者 FusedAdam 优化器。 并传入了一些参数，包括分组的参数、学习率和 betas。

Adam优化器：
- 在 Hugging Face 的 Transformers 库中，有两种 Adam 优化器可供选择：FusedAdam 和 DeepSpeedCPUAdam。它们都是基于 PyTorch 实现的优化器，但在不同的硬件上具有不同的优化和性能特征。FusedAdam 是使用 NVIDIA Apex 库实现的优化器，它支持混合精度训练，并且可以同时计算梯度和权重更新操作，从而提高训练效率。FusedAdam 优化器在使用支持 CUDA 的 NVIDIA GPU 时具有较好的性能。DeepSpeedCPUAdam 是一种 CPU 上的优化器，它是 DeepSpeed 框架中的一部分，支持分布式训练和模型平行化。DeepSpeedCPUAdam 优化器在使用 CPU 时具有较好的性能。在上面的代码中，如果 args.offload 为 True，则表示使用基于 CPU 的优化，因此会选择使用 DeepSpeedCPUAdam 优化器。


##### lr_scheduler

(3) 设置 **lr_scheduler**

```py
    num_update_steps_per_epoch = math.ceil(
        len(train_dataloader) / args.gradient_accumulation_steps)
    lr_scheduler = get_scheduler(
        name=args.lr_scheduler_type,
        optimizer=optimizer,
        num_warmup_steps=args.num_warmup_steps,
        num_training_steps=args.num_train_epochs * num_update_steps_per_epoch,
    )
```

lr_scheduler 是用来规划整个训练过程中 lr 是如何调整的。lr_scheduler_type 调度器类型，用来描述 lr 是按照什么样的方式变化，例如 LinearWarmup、CosineAnnealing 等。num_warmup_steps 预热步数指定了在训练的前期阶段 lr 增加过程的步数。 总训练步数指定模型共被更新多少次。

**DS初始化**

```py
    model, optimizer, _, lr_scheduler = deepspeed.initialize(
        model=model,
        optimizer=optimizer,
        args=args,
        config=ds_config,
        lr_scheduler=lr_scheduler,
        dist_init_required=True) 
```

使用DeepSpeed进行优化是，需要使用deepspeed.initialize() 函数来初始化模型、优化器、学习率调度器等训练相关的组件。其中，model 和 optimizer 是必需的参数，而其他参数则是可选的。

deepspeed.initialize() 函数会对传入的参数进行检查和优化，并返回新的模型、优化器和学习率调度器等组件。例如，它会根据训练参数设置和硬件配置自动调整优化器和梯度累积的设置，并设置模型权重的分布式训练策略。dist_init_required=True 参数指示 DeepSpeed 是否需要进行分布式训练初始化。

DS 配置文件
- 配置文件包含DeepSpeed模型训练时所需要的相关设置信息，可以通过这里的修改来调整训练过程。

下面是 utils/ds_utils.py 中设置 ：

```py
ds_config = {
    "train_batch_size": GLOBAL_BATCH_SIZE,
    "train_micro_batch_size_per_gpu": MICRO_BATCH_SIZE,
    "steps_per_print": 10,
    "zero_optimization": {
        "stage": stage,
        "offload_param": {
            "device": device
        },
        "offload_optimizer": {
            "device": device
        },
        "stage3_param_persistence_threshold": 1e4,
        "stage3_max_live_parameters": 3e7,
        "stage3_prefetch_bucket_size": 3e7,
        "memory_efficient_linear": False
    },
    "fp16": {
        "enabled": True,
        "loss_scale_window": 100
    },
    "gradient_clipping": 1.0,
    "prescale_gradients": False,
    "wall_clock_breakdown": False,
    "hybrid_engine": {
        "enabled": enable_hybrid_engine,
        "inference_tp_size": inference_tp_size,
        "release_inference_cache": release_inference_cache,
        "pin_parameters": pin_parameters,
        "tp_gather_partition_size": tp_gather_partition_size,
    }
}
```

训练部分的实现代码
- 使用DS以后，训练部分的代码与标准的PyTorch代码不同。

```py
    for epoch in range(args.num_train_epochs):
        print_rank_0(
            f"Beginning of Epoch {epoch+1}/{args.num_train_epochs}, Total Micro Batches {len(train_dataloader)}",
            args.global_rank)
        model.train()
        for step, batch in enumerate(train_dataloader):
            batch = to_device(batch, device)
            outputs = model(**batch, use_cache=False)
            loss = outputs.loss
            model.backward(loss)
            model.step()
```

**batch解释： 
- **batch将一个批次的数据传递给模型，避免手动拆分列表或元组，使代码更加简洁易读。

- `*batch` 表示将一个列表对象 batch 中的元素拆分成独立的参数传递给函数或方法。
  - 例如：`*batch = (input_ids, attention_mask, labels)`
  - 用 *batch 时，等价于将这些 Tensor 对象拆分为独立的参数，即：`model(*batch)` 等价于 `model(input_ids, attention_mask, labels)`
- `**batch` 将一个字典对象 batch 拆分成独立的参数传递给函数或方法。
  - 例如：`batch = {'input_ids': input_ids, 'attention_mask': attention_mask, 'labels': labels}`
  - `model(**batch)` 等价于 `model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)`

评价

通过 perplexity 来对模型进行评价。

```py
    # Evaluate perplexity on the validation set
    perplexity = evaluation(model, eval_dataloader)
```

模型保存

```py
    if args.output_dir is not None:
        print_rank_0('saving the final model ...', args.global_rank)
        model = convert_lora_to_linear_layer(model)

        if args.global_rank == 0:
            save_hf_format(model, tokenizer, args)

        if args.zero_stage == 3:
            # For zero stage 3, each gpu only has a part of the model, so we need a special save function
            save_zero_three_model(model,
                                  args.global_rank,
                                  args.output_dir,
                                  zero_stage=args.zero_stage)
```

### Step1：监督微调

使用指定数据微调预训练模型。

启动训练：
执行下面命令开启模型训练。 
- 请先确保设置了 CUDA 并激活了 conda 运行环境

```sh
python3 train.py --step 1 --deployment-type single_gpu  #单GPU训练
python3 train.py --step 1 --deployment-type single_node #多GPU训练
python3 train.py --step 1 --deployment-type multi_node  #多Node训练
```

三种方式中
- `single_gpu` 只适合训练小模型
- 而 single_node 和 multi_node 适合训练较大模型。

建议
- 第一次运行时，用 `single_gpu`，这种模式输出的错误信息会更详细。
- 如果遇到 GPU 内存不足的问题，尝试使用 `single_node` 和 `multi_node` 来训练。
- 如果问题仍然存在，需要手动调整 `batch-size`。

此步骤主要进行：
- 模型下载：自动下载对应的模型
  - 保存到 `~/.cache/huggingface/hub/models--facebook--opt-1.3b`
- 数据下载
  - `Dahoas/rm-static`    # 对话（prompt，response，chosen，rejected） 
  - `Dahoas/full-hh-rlhf` # 对话（prompt，response，chosen，rejected）
  - `Dahoas/synthetic-instruct-gptj-pairwise` # 对话（prompt，chosen，rejected）
  - `yitingxie/rlhf-reward-datasets`  # 对话（prompt，chosen，rejected）
  - `openai/webgpt_comparisons` # 带人工打分的数据，comparisons with human feedback，19,578 comparisons）
  - `stanfordnlp/SHP`           # 18个领域的385k 人类标注数据
- 模型训练：模型训练完成之后会被存储在 `output/actor-models/1.3b` 下面
  -  `training.log` 文件来查看训练的进度。

评价与测试：
- 打开文件 `run_prompt.sh` 添加 baseline 模型，和 finetune 后的模型：

```sh
export CUDA_VISIBLE_DEVICES=0
python prompt_eval.py \
    --model_name_or_path_baseline facebook/opt-1.3b \
    --model_name_or_path_finetune ../../output/actor-models/1.3b
```

评价程序会调用 `prompt_eval.py` 来分别输出 baseline 和 finetune 后模型的结果。

执行此代码，先切换到 step1_supervised_finetuning 目录下。

```sh
cd training/step1_supervised_finetuning
bash evaluation_scripts/run_prompt.sh
```

常见问题：
1. 训练过程，无法找到GPU，或者GPU调用错误，可以尝试使用如下设置：
  - `export CUDA_VISIBLE_DEVICES=0,1` # 2块GPU
  - `export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7` # 8块GPU
2. 训练过程，出现端口被占用的问题
  - 设置 MASTER_ADDR 和 MASTER_PORT，尤其是多个node训练，要设置 MASTER_ADDR。
  - `export MASTER_ADDR=127.0.0.1` # 多node时，需要设置为主node的IP或者机器名
  - `export MASTER_PORT=29701`
  - 以上设置，也可以在 `run1.3b.sh` 文件中进行设置，例如：
    - `CUDA_VISIBLE_DEVICES=0,1 deepspeed --master_addr=127.0.0.1 --master_port=29701 main.py`
3. 评价过程出现模型参数不匹配问题： 
  - `model.decoder.embed_tokens.weight: found shape torch.Size([50272, 2048]) in the checkpoint and torch.Size([50265, 2048]) in the model ...`
  - 原因: 模型被finetune后，Token对应的词典数量发生了变化，导致输入数据维度变化了（bug，输入端应尽量保持与预训练模型一致）。
  - 打开文件 `prompt_eval.py`，增加新 config 读取脚本，并把来源模型从 baseline 模型中修改为finerune后的模型：
  - `config = AutoConfig.from_pretrained(args.model_name_or_path_finetune)` # 新增
  - `model_fintuned = get_model(config, args.model_name_or_path_finetune, tokenizer)`
4. 评价过程，出现 RuntimeError: CUDA out of memory
  - 当对大模型评价时，可能会碰到。比如在32G GPU上使用13b的模型。
  - 建议尝试使用 chat.py 命令（需要移动到 DeepSpeed-Chat 目录下），执行方式如下：
    - `python chat.py --path output/actor-models/1.3b`


### Step2：Reward模型微调

任务介绍： 
- 第三步（Step3）中，强化学习阶段需要使用奖励模型。
- 奖励模型会对模型生成的答案进行打分，Step3 的强化训练会根据这些分数对模型进行优化，从而使最终模型生成更高分的答案。
- 奖励模型同样基于预训练模型进行训练，这里用 350M 的 opt 模型。

启动训练：
- 启动训练方法与前面类似：

```sh
python3 train.py --step 2 --deployment-type single_gpu  #单GPU训练
python3 train.py --step 2 --deployment-type single_node #多GPU训练
python3 train.py --step 2 --deployment-type multi_node  #多Node训练
```

训练数据：
- 单GPU训练时只使用了 Dahoas/rm-static 数据
- 多GPU训练使用了更多的数据：
  - Dahoas/rm-static
  - Dahoas/full-hh-rlhf
  - Dahoas/synthetic-instruct-gptj-pairwise
  - yitingxie/rlhf-reward-datasets
  - openai/webgpt_comparisons
  - stanfordnlp/SHP

评价与测试：

步骤：
- 打开文件 run_eval.sh 设置 --model_name_or_path 参数。
- 转移到目录 step2_reward_model_finetuning 下
- 执行：bash evaluation_scripts/run_eval.sh


常见错误：
1. 与上面类似，出现GPU内存不足错误
  - 调整batch-size或用更多GPU训练。
  - 如：在 run_350m.sh 文件中添加参数 `--per_device_train_batch_size 8` 将默认batch size从16修改为8，如果问题依然存在，可以进一步调小。

### Step3：RLHF训练

任务介绍：

RLHF 是基于人类反馈的强化学习的缩写。根据官方介绍，此步训练面临两个主要挑战：

同时使用多个模型的内存消耗问题：此步训练不仅使用被训练的主模型，还使用奖励模型进行评分，因此会占用更多的 GPU 内存。
如何有效地生成答案：在 RLHF 训练过程中，需要生成多个备选答案。由于模型一次推理只能生成一个答案，因此需要进行多次模型推理，这种操作会大幅度增加训练时间。
在此实例中，通过将 DeepSpeed 训练和推理功能整合为一个统一的混合引擎（Hybrid Engine）来应对这些挑战。更多详细信息可以参考官方说明。

在此步骤首次运行时，会安装并编译新的工具（transformer_inference）。如果编辑过程出现问题，建议升级 PyTorch 和 CUDA 版本。在我的环境下，使用 PyTorch 2.0 和 CUDA 11.7 下可以成功编译。

启动训练：

```sh
python3 train.py --step 3 --deployment-type single_gpu  #单GPU训练
python3 train.py --step 3 --deployment-type single_node #多GPU训练
python3 train.py --step 3 --deployment-type multi_node  #多Node训练
```


此步训练后的模型被存储在 output/step3-models/1.3b/ 下。

常见问题：

Q/A 1. GPU内存不足时，在sh脚本中增加如下设置，调整batch size：
 --per_device_train_batch_size 8　--per_device_mini_train_batch_size=8
8 评价与测试
【观看视频解说】

使用 chat.py 命令（需要移动到 DeepSpeed-Chat 目录下）进行评价与测试。 执行方式如下：

python chat.py --path output/step3-models/1.3b/actor
上面的程序可以启动13b的模型，但是66b的模型无法成功运行。


## DeepSpeed 用法

DeepSpeed 用法
- 【2023-5-19】huggingface的[DeepSpeed文档](https://huggingface.co/docs/transformers/main/main_classes/deepspeed)的笔记：[DeepSpeed 入门教程](https://zhuanlan.zhihu.com/p/630734624?utm_psn=1751727518502281216)

DeepSpeed 支持功能
- Optimizer state partitioning (ZeRO stage 1)
- Gradient partitioning (ZeRO stage 2)
- Parameter partitioning (ZeRO stage 3)
- Custom mixed precision training handling
- A range of fast CUDA-extension-based optimizers
- ZeRO-Offload to CPU and NVMe


### ZeRO 汇总

一句话总结： 
> partitioning instead of replicating，划分而不是复制

DeepSpeed 的 ZeRO config文件可分为几类：<span style='color:red'>优化器 → 梯度 → 参数 → offload</span>
- `ZeRO Stage 1`: 划分optimizer states。
  - 优化器参数被划分到多个memory上，每个momoey上的进程只负责更新自己那部分参数。
- `ZeRO Stage 2`: 划分gradient。
  - 每个memory，只保留它分配到的optimizer state所对应的梯度。
  - 这很合理，因为梯度和optimizer是紧密联系在一起的。只知道梯度，不知道optimizer state，是没有办法优化模型参数的。
- `ZeRO Stage 3`: 划分模型参数，或不同的layer. 
  - ZeRO-3会在forward和backward 时，自动将模型参数分配到多个memory。

由于ZeRO-1只分配optimizer states(参数量很小)，实际使用时,一般只会考虑`ZeRO-2`和`ZeRO-3`。

ZeRO 级别：

| 级别 | 特点 | 作用 |
| --- | --- | --- |
| `Zero-0` |  | 不使用所有类型分片，仅使用DeepSpeed作为DDP |
| `Zero-1` | 优化器状态 | 分割 Optimizer States， 减少4倍内存，通信容量和数据并行性相同 |
| `Zero-2` | 梯度 | 分割 Optimizer States和Gradients，减少8倍内存，通信容量和数据并行性相同 |
| `Zero-3` | 参数 | 分割 Optimizer States、gradients、Parametes，内存减少与数据并行度呈线性关系。例如，在64个GPU（Nd=64）之间进行拆分将产生64倍的内存缩减。通信量有50%的适度增长 |
| `Zero-Infinity` | 参数+offload | Zero-Infinity是 Zero-3 扩展，通过使用 NVMe **固态硬盘**扩展 GPU 和 CPU 内存来训练大型模型 |

Zero stage和offload
- 由于通信增加，故从左到右越来越慢
  - Stage 0 (DDP) > Stage 1 > Stage 2 > Stage 2 + offload > Stage 3 > Stage 3 + offloads
- 由于去除各模块冗余和卸载数据到CPU，故从左到右，显存占用越来越少
  - Stage 0 (DDP) < Stage 1 < Stage 2 < Stage 2 + offload < Stage 3 < Stage 3 + offloads




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
# 多节点多卡 方法1:多个节点上手动启动
python -m torch.distributed.run --nproc_per_node=8 --nnode=2 --node_rank=0 --master_addr=hostname1 --master_port=9901 your_program.py <normal cl args> --deepspeed ds_config.json
# 多节点多卡 方法2:创建 hostfile 文件，只需在一个节点上启动
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

为什么单卡也能用deepspeed？
- 使用 `ZeRO-offload`，将部分数据 offload 到 CPU，降低对显存的需求
- 提供了对显存管理，减少显存碎片

### ZeRO-0 配置

禁用所有分片，此时将DeepSpeed视为DDP使用 (stage默认值：0)

```json
"zero_optimization": {
        "stage": 0
    }
```

### ZeRO-1 配置

ZeRO第一阶段的优化，将优化器状态进行切分

```json
"zero_optimization": {
        "stage": 1
    }
```



### ZeRO-2 配置

```json
"zero_optimization": {
        "stage": 2,
        "allgather_partitions": true,
        "allgather_bucket_size": 3e8,
        "overlap_comm": true,
        "reduce_scatter": true,
        "reduce_bucket_size": 3e8,
        "contiguous_gradients": true
    }
```

- allgather_partitions： 在每个步骤结束时，从所有GPU中选择使用allgather集体操作或一系列广播集体操作之间的方式，以收集更新后的参数。 (默认值：true)
- allgather_bucket_size： 用于调节Allgather操作的分桶大小。将张量分成较小的桶有助于在通信过程中更高效地传输数据。较大的allgather_bucket_size值会导致每个桶的尺寸增大，可能加速通信操作，但也需要更多内存来存储中间结果。选择合适的桶大小需要根据实际情况进行调整。(默认值：5e8)
- overlap_comm： 控制通信与计算是否交叠执行。当设置为True时，DeepSpeed将尝试在梯度计算期间并行进行梯度通信。这有效地缩短通信时间，从而加速整个训练过程。(默认值：false)
- reduce_scatter： 使用reduce或reduce scatter来替代allreduce以平均梯度。(默认值：true)
- reduce_bucket_size： 用于控制Allreduce操作的分桶大小。将张量分为较小的桶有助于数据在通信过程中的更高效传输。随着reduce_bucket_size值的增大，每个桶的尺寸也随之增大，这或许能加速通信操作，但同时也需要更多内存来存储中间结果。合适的桶大小应根据实际情况进行适当调整。(默认值：5e8)
- contiguous_gradients： 在梯度产生时将其复制到一个连续的缓冲区中。在反向传播过程中避免了内存碎片化问题。(默认值：true)

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


### ZeRO-3 配置

ZeRO-3

```json
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
        "reduce_bucket_size": 1e6,
        "stage3_prefetch_bucket_size": 4e6,
        "stage3_param_persistence_threshold": 1e4,
        "stage3_max_live_parameters": 1e9,
        "stage3_max_reuse_distance": 1e9,
        "stage3_gather_16bit_weights_on_model_save": true
    },
```

- sub_group_size： 控制在优化器步骤中参数更新的粒度。参数被分组到大小为sub_group_size的桶中，每个桶依次进行一次更新。当与ZeRO-Infinity中的NVMe offload同时使用时，sub_group_size决定了在优化器步骤期间从NVMe迁移到CPU内存的模型状态的粒度。这有助于避免超大模型对CPU内存的过度占用。在不使用NVMe offload时，请保持其默认值。若遇到内存不足（OOM）情况，可以考虑减小sub_group_size。当优化器迭代较缓慢时，也可以考虑增大sub_group_size。(默认值：1e9)
- stage3_prefetch_bucket_size： 预取参数的固定缓冲区大小。较小的值使用的内存较少，但可能会因通信而增加停顿。(默认值：5e8)
- stage3_max_live_parameters： 保留在GPU上的完整参数数量的上限。(默认值：1e9)
- stage3_max_reuse_distance： 根据参数在未来何时再次使用的指标来决定是舍弃还是保留参数。如果一个参数在不久的将来会再次被使用（小于stage3_max_reuse_distance），则会保留该参数以减少通信开销。在遇到内存不足（OOM）的情况下，可以降低stage3_max_live_parameters和stage3_max_reuse_distance的值。(默认值：1e9)
- stage3_gather_16bit_weights_on_model_save： 在保存模型时启用模型FP16权重合并。对于大型模型和多GPU环境，这是一项在内存和速度方面代价较高的操作。(默认值：false)

ZeRO-3 中不使用 allgather_partitions、allgather_bucket_size 和 reduce_scatter 配置参数

（其他参数如grad_hooks、round_robin_gradients本文未提及）

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

### ZeRO Infinity

除 stage2 和 3 外，介绍下 ZeRO-Infinity。

ZeRO-Infinity 是stage-3 进阶版本，依赖 NVMe 支持。
- offload所有模型参数状态到CPU以及NVMe上。
- 得益于NMVe协议，除了使用CPU内存之外，ZeRO可以额外利用`SSD`(固态)，从而极大地节约了memory开销，加速了通信速度。

官网对于ZeRO-Infinity的详细介绍：

DeepSpeed官方教程 ：
> ZeRO-Infinity has all of the savings of ZeRO-Offload, plus is able to offload more the model weights and has more effective bandwidth utilization and overlapping of computation and communication.

HuggingFace官网：
> It allows for training incredibly large models by extending GPU and CPU memory with NVMe memory. Thanks to smart partitioning and tiling algorithms each GPU needs to send and receive very small amounts of data during offloading so modern NVMe proved to be fit to allow for an even larger total memory pool available to your training process. ZeRO-Infinity requires ZeRO-3 enabled.

具体config文件，以及使用事项，请参见官网。

GPU上进行前向和后向计算，将梯度传给CPU，进行参数更新，再将更新后的参数传给GPU。

为了提高效率，将**计算**和**通信**并行起来
- GPU在**反向传播**阶段，待梯度值填满bucket后，一边计算新梯度，一边将bucket传输给CPU
- 当**反向传播**结束，CPU基本上已经有最新的梯度值了，同样，CPU在参数更新时也同步将已经计算好的参数传给GPU


四个计算类节点：FWD、BWD、Param update 和 float2half，前两个计算复杂度大致是 O(MB)， B是batch size，后两个计算复杂度是 O(M)。
- 为了不降低计算效率，将前两个节点放在GPU，后两个节点不但计算量小还需要和Adam状态打交道，所以放在CPU上，Adam状态自然也放在内存中，为了简化数据图，将前两个节点融合成一个节点FWD-BWD Super Node，将后两个节点融合成一个节点Update Super Node。如下图右边所示，沿着gradient 16和parameter 16两条边切分。



### 调参步骤

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

### 优化器和调度器

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


### 混合精度

由于 fp16 混合精度大大减少了内存需求，并可以实现更快的速度，因此只有此训练模式表现不佳时，才考虑不使用**混合精度训练**。 

通常，当模型未在 fp16 混合精度中进行预训练时，会出现这种情况（例如，使用 bf16 预训练的模型）。 这样的模型可能会溢出，导致loss为NaN。 如果是这种情况，使用完整的 fp32 模式。
- 如果是基于 Ampere 架构的 GPU，pytorch 1.7 及更高版本将自动切换为使用更高效的 tf32 格式进行某些操作，但结果仍将采用 fp32。
- 使用 Trainer，可以使用 `--tf32` 启用它，或使用 `--tf32 0` 或 `--no_tf32` 禁用它。 

PyTorch 默认值是使用`tf32`。

自动混合精度
- `fp16`
  - 可用 `pytorch-like` AMP 方式或者 `apex-like` 方式
  - 使用 `--fp16--fp16_backend amp` 或 `--fp16_full_eval` 命令行参数时启用此模式
- `bf16`
  - 使用`--bf16` or `--bf16_full_eval` 命令行参数时启用此模式

注意
- fp32/fp16 绝大多数硬件都支持，所以可用混合精度训练提高吞吐；
  - 但 bf16/tf32 只有新的硬件才支持，V100/昇腾910等不支持
- bf16 具有和 fp32 相同的 range，但精度（也就是两个最小单位之间的间隔）降低
- bf16/fp32 进行混合精度训练，可以减少溢出几率
- 对于大型 transformer，bf16 损失的精度被证明不怎么影响收敛
- tf32 是 A100 中引入的新格式，用于替代 fp32，也即可以全程 tf32 训练或 bf16/tf32 混合训练
- ![](https://pic4.zhimg.com/80/v2-5e80264a8fe8ffaf312d08a50ce103eb_1440w.webp)

bf16/fp32 混合训练
- 因为两种格式在 range 对齐，并且 bf16 比 fp16 range 更大，所以比 fp16/fp32 混合训练稳定性更高。
- 但 fp16/fp32 混合训练 GPT-3 大模型也完全可行，只要解决可溢出问题

几个要点：
- fp32权重备份 + loss scaling 解决下溢出问题
  - 对 loss 进行 scale：见左图
  - 对 gradient 进行 scale：见右图
  - 由于链式法则的存在，对梯度做直接做 scale 也是可以的，反而更划算。这样，所有前向后向都可以全用 fp16 (activation、weight、gradient 全用 fp16)，只在进行更新的时候，才用 fp32 和 master weight 更新
- 跳过 NaN 的 batch
  - dynamic loss scale (PyTorch 中采用的这种方案）：在一个 window 内，如果没有 NaN，loss scale 变大（例如乘2）；如果有 NaN，则降低 loss scale，并跳过 NaN 的 batch，不更新梯度
  - 或将 INF 值改为 FP16 的最大值（需要实际验证）
- 基于 Tensorcore 进行矩阵乘加：在某些模型中，fp16 矩阵乘法的过程中，需要利用 fp32 来进行矩阵乘法中间结果的累加，以减少加法过程中的舍入误差，保证精度不损失

这也是为什么有些人说，只有 Volta 之后有 TensorCore 的 GPU (例如V100)，才能利用 fp16+混合精度来进行加速。其他 GPU 如果硬要用 fp16，只能做 fp16 的 multiply-add operation，会有较大精度损失
- [参考](https://zhuanlan.zhihu.com/p/622631376)


NCCL
- 通讯会采用一种单独的数据类型
- 默认情况下，半精度训练使用 `fp16` 作为reduction操作的默认值
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

混合精度训练

```json
"fp16": {
    "enabled": true,
    "auto_cast": false,
    "loss_scale": 0,
    "initial_scale_power": 16,
    "loss_scale_window": 1000,
    "hysteresis": 2,
    "consecutive_hysteresis": false,
    "min_loss_scale": 1
}

"bf16": {
   "enabled": true
 }
```

- auto_cast： 是否将输入强制转换为fp16数据类型 (默认值：false)
- loss_scale： 表示FP16训练的损失缩放值。默认值0.0启用动态损失缩放，否则该值将用于静态固定损失缩放 (默认值：0.0)
- initial_scale_power： 表示初始动态损失比例值的功率，实际损失规模计算为 
 (默认值：16)
- loss_scale_window： 代表动态损失缩放值上升/下降的窗口范围。(默认值：1000)
- hysteresis： 表示动态损耗缩放中的延迟偏移 (默认值：2)
- consecutive_hysteresis： 表示是否在达到不会溢出的迭代时重新填充滞后。(默认值：false)
- min_loss_scale： 表示最小动态损失比例值 (默认值：1)

注意：开启fp16后可能出现如上图所示overflow情况
- BF16： 配置以bfloat16浮点格式作为FP16的替代方式。
- bfloat16需要硬件支持, 例如，NVIDIA A100, 注意 v100不支持！。
- 使用bfloat16进行训练不需要**损失缩放**。(默认值：false)




### 获取模型参数

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


### ZeRO inference

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


### 多机多卡

【2024-3-25】[DeepSpeed 多机多卡训练指南](https://mp.weixin.qq.com/s/ktBPcDiGu5bXOqs7CQawlw)

配置：
- 7机14卡，每台服务器两张A800
- 问：为啥每台机只挂两张卡？
- 答：资源就这样，服务器是云厂商提供，都是PCIE连接，且单机最多只能挂四张卡。

服务器只允许内网访问，不能连接外网

因此，先搞定如何离线配置训练环境

离线配置训练环境
- 报错：conda was found to be deleted
- 解决：增加参数`--ignore-missing-files`解决 如：conda pack -n 环境名 -o 新的环境名.tar.gz --ignore-missing-files

共享文件系统

多机多卡训练，配置个共享文件系统是有很多好处，比如
- 数据集和模型只需要存一份，更重要的是，在
- 模型保存时，将模型保存到共享文件系统下，就不用保存多份模型
- 如果没有共享文件系统，在每台服务器上都保存一份模型参数。

断点重训时，手动合并每台机器上的优化器参数，非常麻烦。

如果真的没有共享文件系统，那怎么办？ 

解决办法：
- 方式1、在deepspeed里配置checkpoint参数的use_node_local_storage
- 方式2、增加在TrainingArguments中配置参数--save_on_each_node即可
  - 其实，huggingface中的deepspeed插件文档已经对没有共享文件系统的情况做了说明，确实比较难找，[位置](https://huggingface.co/docs/transformers/main/en/main_classes/deepspeed#use-of-nonshared-filesystem)

```json
"checkpoint": {
    "use_node_local_storage": true
}
```

deepspeed stage2 配置样例：

```json
{
    "bfloat16": {
        "enabled": false
    },
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
    "zero_optimization": {
        "stage": 2,
        "allgather_partitions": true,
        "allgather_bucket_size": 2e8,
        "overlap_comm": true,
        "reduce_scatter": true,
        "reduce_bucket_size": "auto",
        "contiguous_gradients": true
    },
    "gradient_accumulation_steps": "auto",
    "gradient_clipping": "auto",
    "steps_per_print": 1e5,
    "train_batch_size": "auto",
    "train_micro_batch_size_per_gpu": "auto",
    "wall_clock_breakdown": false,
    "checkpoint": {
        "use_node_local_storage": true
    }
}
```

[原始文档](https://www.deepspeed.ai/docs/config-json)


使用resume路径去恢复训练时，可能卡在:
- loading extention module ...

GPU有占用，GPU利用率也有显示，此时，你应该检查你的device_map是否为auto，如果不是，那肯定会卡在这

如果device_map="auto"，但代码还是卡在这，可能的解决办法：


多台服务器之间配置互相免密登录
- 必须要做的，最好在一开始就做好，能节省很多时间。

做法
- 每台服务器都安装 pdsh

多卡训练可能会碰到的问题

问题1：**ninja已经安装**，deepspeed 多机多卡
- RuntimeError: Ninja is required to load C++ extensions 

答案1：在训练代码的开头加入：

/root/anaconda3/envs/baichuan/bin:是服务器的conda虚拟环境的bin目录

local_env = os.environ.copy()
local_env["PATH"]= "/root/anaconda3/envs/baichuan/bin:" + local_env["PATH"]
os.environ.update(local_env)

问题2：
- libcudart.so.12.2: cannot open shared object file: No such file or directory 

答案2：
- 1、检查文件libcudart.so.12.2是否存在（正常来说都是存在的），不存在该文件的话，需要重装cuda
- 2、在命令行执行 sudo ldconfig /usr/local/cuda-12.2/lib64

执行训练的代码，每台机器上要有完全一致的一份，且存储的路径都要一致（包括软件的安装路径等）




### 问题

- 1: 模型初始化时，定义了`dschf = HfDeepSpeedConfig(ds_config)`，后面没有调用。
  - 当使用 zero 3 时需要设置 `dschf = HfDeepSpeedConfig(ds_config)`。
  - 具体说明请[参考](https://huggingface.co/docs/transformers/main_classes/deepspeed#nontrainer-deepspeed-integration)
- 2: ZeRO 是什么？
  - `ZeRO`（Zero Redundancy Optimizer）是 DeepSpeed 一种优化技术，旨在提高大规模模型训练的效率和可扩展性。
  - 其中，`ZeRO Offload` 是 `ZeRO` 技术的一种变体，可以通过将模型参数存储在 CPU 上，从而减少模型训练时对GPU显存的占用，并加速模型参数的梯度累积、梯度压缩和通信等操作。 ZeRO 3 是在大模型进行模型参数并行时使用。

#### deepspeed 传参问题

deepspeed 传参问题总结
- 参数位置敏感: 尤其注意区分deepspeed参数和train.py参数
  - 格式: deepspeed `ds参数` train.py `train参数` 
- 别漏了 ds 开关 `--deepspeed`
- ds_config.json: 放最后, 或 `--deepspeed_config`

alexnet 示例
- [train.py](https://github.com/microsoft/DeepSpeedExamples/blob/master/training/pipeline_parallelism/train.py)

踩过的一系列坑

```sh
deepspeed train.py -p 1 --steps=200  --deepspeed_config=ds_config.json --autotuning tune
# (1) autotuning 放 train.py 后面 → error: unrecognized arguments: --autotuning tune

# (2) train.py 挪至最后 → deepspeed: error: unrecognized arguments: -p
deepspeed -p 1 --steps=200  --deepspeed_config=ds_config.json --autotuning tune train.py

# (3) autotuning 放 train.py 后面 → AssertionError: DeepSpeed configuration is not provided
deepspeed --autotuning tune train.py -p 1 --steps=200  --deepspeed_config=ds_config.json

# (4) ds_config.json 放 --deepspeed 前面  → File ".../deepspeed/autotuning/autotuner.py", line 176, in _get_user_config if ".json" in user_args[idx + 1]: IndexError: list index out of range
# 加 deepspeed 参数
deepspeed --autotuning tune train.py -p 1 --steps=200  --deepspeed_config=ds_config.json --deepspeed
# 去掉冗余参数 --deepspeed_config=ds_config.json
deepspeed --autotuning tune train.py -p 1 --steps=200 --deepspeed --deepspeed_config=ds_config.json
# (5) 报错 没有 pdsh → apt-get install pdsh (失败) → 编译安装 pdsh, 设置prefix, 添加到 PATH
# ./configure –-with-ssh –-enable-static-modules –-prefix=/home/username && make && make install
# bashrc: export PATH=$PATH:/home/username/bin
# pdsh -V
# (6) 报错 → localhost: ssh: connect to host localhost port 22: Connection refused
```

ssh错误提交官方 [issue](https://github.com/microsoft/DeepSpeedExamples/issues/894)

解法：ssh 服务异常, 启动ssh服务, 监听端口 22

```sh
# 测试, 复现成功
ssh root@127.0.0.1 -v
# OpenSSH_8.4p1 Debian-5+deb11u3, OpenSSL 1.1.1n  15 Mar 2022
# debug1: Reading configuration data /etc/ssh/ssh_config
# debug1: /etc/ssh/ssh_config line 19: include /etc/ssh/ssh_config.d/*.conf matched no files
# debug1: /etc/ssh/ssh_config line 21: Applying options for *
# debug1: Connecting to 127.0.0.1 [127.0.0.1] port 22.
# debug1: connect to address 127.0.0.1 port 22: Connection refused
# ssh: connect to host 127.0.0.1 port 22: Connection refused

ps -ef | grep sshd # 查看结果中是否有sshd服务, 如果没有,安装ssh client,启动ssh
service sshd status # sshd is running.
vim /etc/ssh/sshd_config # 开启 22 端口
/etc/init.d/ssh restart
# 测试
ssh root@127.0.0.1 -v
```

继续追查
- 官方有同样的错误: issue
  - [The model is not runnable with DeepSpeed with error ](https://github.com/microsoft/DeepSpeed/issues/4759)
  - [run_after_tuning: No optimal DeepSpeed configuration found by autotuning](https://github.com/huggingface/transformers/issues/27830)

```sh
# (7) 
# [2024-04-20 19:30:23,366] [INFO] [scheduler.py:393:run_experiment] Done running exp_id = 0, exp_name = profile_model_info, with resource = localhost:0
# 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:56<00:00, 56.53s/it]
# [2024-04-20 19:30:28,376] [ERROR] [autotuner.py:699:model_info_profile_run] The model is not runnable with DeepSpeed with error = unrecognized arguments: eyJ0cmFpbl9iYXRjaF9zaXplIjogMjU2LCAidHJhaW5fbWljcm9fYmF0Y2hfc2l6ZV9wZXJfZ3B1IjogMSwgIm9wdGltaXplciI6IHsidHlwZSI6ICJBZGFtIiwgInBhcmFtcyI6IHsibHIiOiAwLjAwMSwgImJldGFzIjogWzAuOSwgMC45OTldLCAiZXBzIjogMWUtMDh9fSwgInN0ZXBzX3Blcl9wcmludCI6IDEwLCAid2FsbF9jbG9ja19icmVha2Rvd24iOiBmYWxzZSwgIm5ub2RlIjogMSwgImF1dG90dW5pbmciOiB7ImVuYWJsZWQiOiB0cnVlLCAibW9kZWxfaW5mb19wYXRoIjogImF1dG90dW5pbmdfcmVzdWx0cy9wcm9maWxlX21vZGVsX2luZm8vbW9kZWxfaW5mby5qc29uIiwgIm1vZGVsX2luZm8iOiB7InByb2ZpbGUiOiB0cnVlfSwgIm1ldHJpY19wYXRoIjogImF1dG90dW5pbmdfcmVzdWx0cy9wcm9maWxlX21vZGVsX2luZm8vbWV0cmljcy5qc29uIn0sICJ6ZXJvX29wdGltaXphdGlvbiI6IHsic3RhZ2UiOiAzfSwgIm1lbW9yeV9icmVha19kb3duIjogZmFsc2V9 --per_device_train_batch_size 1

[2024-04-20 19:30:28,376] [INFO] [runner.py:366:run_autotuning] [End] Running autotuning
```



#### 显存预估

DeepSpeed 使用难点在于**时间和空间权衡**。
- 分配更多参数到CPU上，虽然能够降低显存开销，但是也会极大地提升时间开销。

DeepSpeed 提供 memory估算代码：

```py
from transformers import AutoModel
from deepspeed.runtime.zero.stage3 import estimate_zero3_model_states_mem_needs_all_live

## specify the model you want to train on your device
model_name_or_path = "/mnt/bn/flow-algo-cn/yufeng/ModelHub/internlm2-1_8b"
model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True) 
## estimate the memory cost (both CPU and GPU)
estimate_zero3_model_states_mem_needs_all_live(model, num_gpus_per_node=1, num_nodes=1)
```

结果 
- internlm2-1.8b 显存开销 32.37G, 实际开销翻倍(64G, batch_size,缓存)
- 使用 stage2和3后，显存开销被极大地降低，转而CPU内存消耗显著提升，模型训练时间开销也相应地增大。

```js
Estimated memory needed for params, optim states and gradients for a:
HW: Setup with 1 node, 1 GPU per node.
SW: Model with 1889M total params, 189M largest layer params.
  per CPU  |  per GPU |   Options
   47.50GB |   0.71GB | offload_param=cpu , offload_optimizer=cpu , zero_init=1
   47.50GB |   0.71GB | offload_param=cpu , offload_optimizer=cpu , zero_init=0
   42.22GB |   4.22GB | offload_param=none, offload_optimizer=cpu , zero_init=1
   42.22GB |   4.22GB | offload_param=none, offload_optimizer=cpu , zero_init=0
    1.06GB |  32.37GB | offload_param=none, offload_optimizer=none, zero_init=1
   10.56GB |  32.37GB | offload_param=none, offload_optimizer=none, zero_init=0
```

启动任务前大概估计显存消耗，决定**GPU数目**，以及**ZeRO-stage**。

原则: 
- 能直接**多卡**训练，就不用`ZeRO`；
- 能用`ZeRO-2`就不用`ZeRO-3`.

#### 无法识别 --local_rank=3

多GPU进行训练时, 错误信息 

```sh
main.py: error: unrecognized arguments: --local_rank=3
Traceback (most recent call last):
  File "/opt/tiger/rh2/rh2/init/arnold.py", line 582, in main
    raise Exception('failed to execute user script with exit code {}'.format(sub_exit_code))
Exception: failed to execute user script with exit code 2
```

原因: [pytorch](https://discuss.pytorch.org/t/error-unrecognized-arguments-local-rank-1/83679)
- main.py 里的 ArgumentParser 未接收 local_rank 参数

解法: 添加local_rank参数

```py
parser.add_argument("--local_rank", type=int, default=0)
```

pytorch 解法
- `python -m torch.distributed.launch` 已淘汰, 替换成 `torchrun`

```sh
python -m torch.distributed.launch --nproc_per_node=4 --master_port=27803 # replaced by 
# 直接改成 torchrun
torchrun --nproc_per_node=4 --master_port=27803 ...
```


#### CUDA out of memory

问题

```sh
torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.25 GiB. 
GPU 0 has a total capacty of 79.35 GiB of which 210.19 MiB is free. 
Process 1984273 has 79.14 GiB memory in use. Of the allocated memory 74.99 GiB is allocated by PyTorch, and 1.55 GiB is reserved by PyTorch but unallocated. 
If reserved but unallocated memory is large try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF
```

解法
- [[BUG] error: unrecognized arguments: --deepspeed ./ds_config.json #3961](https://github.com/microsoft/DeepSpeed/issues/3961)

`run.sh`
- 直接将 ds_config 文件添加到deepspeed后面, 或指定 deepspee_config 参数

```sh
DS_CONFIG_PATH="llm/ds_config.json"

deepspeed --master_port 30001 --autotuning tune \
   ./llm/training/conversation_reward/main.py \
   --max_seq_len 3072 \
   --per_device_train_batch_size 2 \
   --per_device_eval_batch_size 2 \
   --weight_decay 0.1 \
   --dropout 0.0 \
   --gradient_accumulation_steps 16 \
   --zero_stage 2 \
   --dtype bf16 \
   --num_train_epochs 10 \
   --train_data_path /mnt/bn/flow-algo-cn/wangqiwen/session_process/data/train/cut_train_sequence_all_20240331.csv \
   --val_data_path /mnt/bn/flow-algo-cn/wangqiwen/session_process/data/test/cut_test_toNow_es_sequence_v2.csv \
   --test_data_path /mnt/bn/flow-algo-cn/wangqiwen/session_process/data/test/cut_test_toNow_en_sequence_v2.csv \
   --model_name_or_path /mnt/bn/flow-algo-cn/yufeng/ModelHub/internlm2-1_8b \
   --output_dir /mnt/bn/flow-algo-cn/wangqiwen/model/checkpoints \
   --save_steps 1000 \
   --deepspeed $DS_CONFIG_PATH
#   --deepspeed_config $DS_CONFIG_PATH
```


main.py

```py
parser = deepspeed.add_config_arguments(parser) # 添加这行
args = parser.parse_args()
```


#### 无法识别 --deepspeed


【2024-4-19】无法识别命令行参数 `deepspeed`, `deepspeed_config`
- 提官方[issues](https://github.com/microsoft/DeepSpeed/issues/3961)

```
deepspeed   0.12.6
torch       2.1.0+cu121
```



# 结束