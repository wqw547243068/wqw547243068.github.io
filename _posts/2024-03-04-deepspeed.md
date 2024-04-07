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


## DeepSpeed 框架演进

【2024-4-6】总结：

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-04-06T08:58:33.411Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\&quot; etag=\&quot;WPKRZEx3iDk2hN-1VGnZ\&quot; version=\&quot;24.2.2\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;-380\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; value=\&quot;LLM(大模型)训练框架\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;567.75\&quot; y=\&quot;1240\&quot; width=\&quot;224.5\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;940\&quot; y=\&quot;1383.5\&quot; width=\&quot;150\&quot; height=\&quot;165\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; value=\&quot;Megatron\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#00CC00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; y=\&quot;1450\&quot; width=\&quot;100\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-13\&quot; value=\&quot;GPT分布式训练\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;730.0000000000001\&quot; y=\&quot;1355\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-7\&quot; y=\&quot;1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-25\&quot; value=\&quot;Microsoft\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#7F00FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;800.0000000000001\&quot; y=\&quot;1442.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-28\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; target=\&quot;yvSmSdpK5QFk-1BAp_-0-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;624.5799999999999\&quot; y=\&quot;2090\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;844.5799999999999\&quot; y=\&quot;2090\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-32\&quot; value=\&quot;3D并行\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;959.53\&quot; y=\&quot;1394.5\&quot; width=\&quot;60.47\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-1\&quot; value=\&quot;PyTorch\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;590\&quot; y=\&quot;1340\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-11\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-2\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-2\&quot; value=\&quot;DeepSpeed\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#6666FF;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;702.25\&quot; y=\&quot;1451\&quot; width=\&quot;100\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-1\&quot; target=\&quot;yvSmSdpK5QFk-1BAp_-0-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;547.25\&quot; y=\&quot;1420\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;680\&quot; y=\&quot;1450\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-5\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-1\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;579\&quot; y=\&quot;1390\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;705\&quot; y=\&quot;1460\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-6\&quot; value=\&quot;NVIDIA\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#009900;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;451.0000000000001\&quot; y=\&quot;1430\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;3\&quot; y=\&quot;11\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-7\&quot; value=\&quot;Megatron-DeepSpeed\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#7F00FF;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;659.97\&quot; y=\&quot;1784\&quot; width=\&quot;180\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-8\&quot; value=\&quot;ZeRO-*\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;959.53\&quot; y=\&quot;1428.5\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-9\&quot; value=\&quot;ZeRO offload\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;959.53\&quot; y=\&quot;1466.5\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-10\&quot; value=\&quot;混合精度\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;959.53\&quot; y=\&quot;1508.5\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-12\&quot; value=\&quot;&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;本质: 数据并行优化版&amp;lt;/div&amp;gt;&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;前提: &amp;lt;font color=&amp;quot;#ff0000&amp;quot;&amp;gt;单层参数单张显卡放得下&amp;lt;/font&amp;gt;&amp;lt;/div&amp;gt;案例: MT-530B, BLOOM\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;760.0000000000001\&quot; y=\&quot;1510\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-13\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-16\&quot; target=\&quot;yvSmSdpK5QFk-1BAp_-0-7\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;595\&quot; y=\&quot;1380\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1460\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-2\&quot; target=\&quot;yvSmSdpK5QFk-1BAp_-0-7\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1490\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;622\&quot; y=\&quot;1604\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-15\&quot; value=\&quot;前提不满足&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;500.0000000000002\&quot; y=\&quot;1507.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-16\&quot; value=\&quot;Megatron-LM-1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;420\&quot; y=\&quot;1594\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-17\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; target=\&quot;yvSmSdpK5QFk-1BAp_-0-16\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1490\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;705\&quot; y=\&quot;1604\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-18\&quot; value=\&quot;超大规模Transformer分布式训练:&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;数据并行 + 张量并行&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490.0000000000002\&quot; y=\&quot;1570\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-19\&quot; value=\&quot;模型并行内核&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540.0000000000002\&quot; y=\&quot;1451\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-20\&quot; value=\&quot;① ZeRO分片&amp;lt;div style=&amp;quot;font-size: 13px;&amp;quot;&amp;gt;&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;② 管道并行&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;760.0000000000002\&quot; y=\&quot;1700\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-21\&quot; value=\&quot;③ 张量并行\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;640.0000000000002\&quot; y=\&quot;1710\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;yvSmSdpK5QFk-1BAp_-0-22\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#cc0000&amp;quot;&amp;gt;3D并行&amp;lt;/font&amp;gt; = &amp;lt;font color=&amp;quot;#7f00ff&amp;quot;&amp;gt;ZeRO分片&amp;lt;/font&amp;gt; + &amp;lt;font color=&amp;quot;#7f00ff&amp;quot;&amp;gt;管道并行&amp;lt;/font&amp;gt; + &amp;lt;font color=&amp;quot;#009900&amp;quot;&amp;gt;张量并行&amp;lt;/font&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;659.9700000000003\&quot; y=\&quot;1830\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-1\&quot; value=\&quot;Megatron-LM-2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;420\&quot; y=\&quot;1784\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-2\&quot; value=\&quot;Megatron-LM-3\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;420\&quot; y=\&quot;1890\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-3\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;yvSmSdpK5QFk-1BAp_-0-16\&quot; target=\&quot;773s7HMUVt6-7SW6n1rD-1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1634\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;760\&quot; y=\&quot;1794\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;773s7HMUVt6-7SW6n1rD-1\&quot; target=\&quot;773s7HMUVt6-7SW6n1rD-2\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1634\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;490\&quot; y=\&quot;1794\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-5\&quot; value=\&quot;流水线并行, 3D并行\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490.0000000000002\&quot; y=\&quot;1770\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-6\&quot; value=\&quot;增加3个特性&amp;lt;div&amp;gt;- layernorm和dropout并行&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;- 激活函数不重复计算&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;- GPU显存未满时不做checkpoint&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;550.0000000000002\&quot; y=\&quot;1900\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;773s7HMUVt6-7SW6n1rD-7\&quot; value=\&quot;wqw547243068@163.com&amp;lt;div&amp;gt;2024-4-6&amp;lt;/div&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#808080;fontSize=13;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;890.0000000000002\&quot; y=\&quot;1910\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

## DeepSpeed-Chat

【2024-3-29】[大模型训练入门实战](https://techdiylife.github.io/big-model-training/deepspeed/deepspeed-chat.html)


DeepSpeed 是 Microsoft基于PyTorch研发的开源深度学习优化库。
- 目的: 降低大模型训练的门槛，提升大模型的训练的效率，帮助开发者更有效率地管理及优化大模型的训练、部署任务。

## DeepSpeed 介绍

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

## DeepSpeed 框架

DeepSpeed 主要分成以下四个板块，包括：Training、Inference、Compression、Science
- ![](https://pic1.zhimg.com/v2-a9ac939ec325cf859c282511ddd90f2c_b.jpg)

DeepSpedd-Training 提供一套端到端大模型训练框架，核心板块。
- 因为DeepSpeed 基于PyTorch搭建，且兼容 Transformers，新用户学习成本较低，可快速上手，快速实现自有工程的搭建。
- 并且DeepSpeed在DeepSpeedExamples项目中提供了`DeepSpeed-chat`模块 ，完美复刻`InstructGPT`论文中RLHF训练方式，可以一键式完成大模型的SFT、Reward Model Finetuning、RLHF
- ![](https://pic3.zhimg.com/v2-28ace0f70b557dc6b6394171daeab912_b.jpg)

[DeepSpeedExamples](https://github.com/microsoft/DeepSpeedExamples) 也提供 bert、gan、Stable Diffusion 微调案列，更方便的学习应用DeepSpeed。

DeepSpeed发展速度非常快，一些新的大模型热点技术都实现快速支持 。目前DeepSpeed可以支持MoE模型架构训练，并且在超长上下文模型训练问题上也提供了优化方案。


### DeepSpeed-Trianing

DeepSpeed-Trianing 介绍
- 通信策略优化
  - 为更好支持在GPU、CPU上的分布式训练以及GPU、CPU的混合训练。DeepSpeed支持 mpi、gloo 和 nccl 等通信策略
  - Open MPI 可整合高性能计算社区中所有专家，技术和资源，以构建可用的最佳MPI库。
  - Gloo: facebook开源的一套集体通信库，他提供了对机器学习中有用的一些集合通信算法如：barrier, broadcast, allreduce
  - nccl: NVIDIA集体通信库（NCCL）实现了针对NVIDIA GPU性能优化的多GPU和多节点集体通信原语。NCCL提供了诸如all-gather, all-reduce, broadcast, reduce, reduce-scatter等实现，这些实现优化后可以通过PCIe和NVLink等高速互联，从而实现高带宽和低延迟。 因为NCCL则是NVIDIA基于自身硬件定制的，能做到更有针对性且更方便优化，故在英伟达硬件上，NCCL的效果往往比其它的通信库更好。
  - 选择策略: 
    - 如果在 CPU 集群上分布式训练，选择 mpi 和 gloo；
    - 如果在 GPU 上进行分布式训练，可以选择 nccl。

## DeepSpeed 用法

DeepSpeed 用法
- 【2023-5-19】huggingface的[DeepSpeed文档](https://huggingface.co/docs/transformers/main/main_classes/deepspeed)的笔记：[DeepSpeed 入门教程](https://zhuanlan.zhihu.com/p/630734624?utm_psn=1751727518502281216)

DeepSpeed目前支持的功能
- Optimizer state partitioning (ZeRO stage 1)
- Gradient partitioning (ZeRO stage 2)
- Parameter partitioning (ZeRO stage 3)
- Custom mixed precision training handling
- A range of fast CUDA-extension-based optimizers
- ZeRO-Offload to CPU and NVMe

|ZeRO等级|特点|分析|
|---|---|---|
|`ZeRO-1`|优化器状态||
|`ZeRO-2`|梯度||
|`ZeRO-3`|参数||
|`ZeRO-3 offload`|参数+offload||


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


### ZeRO-2 配置

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


### 训练精度

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


# 结束