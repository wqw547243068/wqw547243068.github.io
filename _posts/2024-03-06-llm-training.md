---
layout: post
title:  LLM 大模型训练之路
date:   2024-03-06 12:00:00
categories: 大模型
tags: ChatGPT 训练
excerpt: 大模型训练原理，如何训练，有什么经验？
mathjax: true
permalink: /llm_train
---

* content
{:toc}


# LLM 大模型训练之路


## 训练组件

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-04-05T14:19:00.902Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\&quot; etag=\&quot;iTQVtqaHaZMRcuWp4R96\&quot; version=\&quot;24.2.2\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;-380\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-6\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;160\&quot; y=\&quot;1390\&quot; width=\&quot;304.58\&quot; height=\&quot;230\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; value=\&quot;LLM(大模型)训练\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;567.75\&quot; y=\&quot;1240\&quot; width=\&quot;224.5\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-7\&quot; value=\&quot;数据准备\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;315.15000000000003\&quot; y=\&quot;1370\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;610\&quot; y=\&quot;1390\&quot; width=\&quot;304.58\&quot; height=\&quot;230\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-35\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-11\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-9\&quot; value=\&quot;pre-train\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;676.68\&quot; y=\&quot;1420\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-10\&quot; value=\&quot;增量预训练\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;773.22\&quot; y=\&quot;1420\&quot; width=\&quot;91.36\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-34\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-11\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-12\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-11\&quot; value=\&quot;SFT\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;676.68\&quot; y=\&quot;1490\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-12\&quot; value=\&quot;RLHF\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;676.68\&quot; y=\&quot;1560\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-13\&quot; value=\&quot;模型训练\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;765.1500000000001\&quot; y=\&quot;1370\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-14\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;610\&quot; y=\&quot;1730\&quot; width=\&quot;304.58\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-15\&quot; value=\&quot;多机多卡\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;676.68\&quot; y=\&quot;1760\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-19\&quot; value=\&quot;GPU资源\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;660.0000000000001\&quot; y=\&quot;1710\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-20\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1070\&quot; y=\&quot;1390\&quot; width=\&quot;304.58\&quot; height=\&quot;230\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-42\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-21\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-41\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-21\&quot; value=\&quot;base模型\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1136.68\&quot; y=\&quot;1420\&quot; width=\&quot;83.32\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-25\&quot; value=\&quot;模型\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1225.15\&quot; y=\&quot;1370\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-26\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-6\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;400\&quot; y=\&quot;1360\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;545\&quot; y=\&quot;1090\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-27\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-20\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;946.22\&quot; y=\&quot;1564.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1166.22\&quot; y=\&quot;1564.5\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-28\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-14\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-8\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;864.5799999999999\&quot; y=\&quot;1690\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1084.58\&quot; y=\&quot;1690\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-29\&quot; value=\&quot;代码\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;220.00000000000003\&quot; y=\&quot;1420\&quot; width=\&quot;60\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-32\&quot; value=\&quot;模型并行\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;783.92\&quot; y=\&quot;1760\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-33\&quot; value=\&quot;工具调用\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;300\&quot; y=\&quot;1420\&quot; width=\&quot;60\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-36\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1072.86\&quot; y=\&quot;1710\&quot; width=\&quot;304.58\&quot; height=\&quot;230\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-37\&quot; value=\&quot;基础能力\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1139.54\&quot; y=\&quot;1740\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-38\&quot; value=\&quot;模型评测\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1280\&quot; y=\&quot;1690\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-39\&quot; value=\&quot;工具调用\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1139.54\&quot; y=\&quot;1790\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-40\&quot; value=\&quot;多模态\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1142.86\&quot; y=\&quot;1840\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-41\&quot; value=\&quot;chat模型\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1136.18\&quot; y=\&quot;1500\&quot; width=\&quot;83.32\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-44\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=4;strokeColor=#999999;entryX=0.491;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;dashPattern=1 2;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;KTwht3HF3Dpf_-XckZrt-20\&quot; target=\&quot;KTwht3HF3Dpf_-XckZrt-36\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1020\&quot; y=\&quot;1730\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1020\&quot; y=\&quot;1620\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-45\&quot; value=\&quot;对话语料\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1220.0000000000002\&quot; y=\&quot;1480\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-47\&quot; value=\&quot;（1）\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;660.0000000000001\&quot; y=\&quot;1435\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-51\&quot; value=\&quot;（2）\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;660.0000000000001\&quot; y=\&quot;1505\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-52\&quot; value=\&quot;（3）\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=1;fontColor=#808080;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;670.0000000000001\&quot; y=\&quot;1575\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-8\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-53\&quot; value=\&quot;RM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;765.15\&quot; y=\&quot;1560\&quot; width=\&quot;64.85\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-54\&quot; value=\&quot;PPO\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;840\&quot; y=\&quot;1560\&quot; width=\&quot;64.85\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-56\&quot; value=\&quot;训练框架\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#6a00ff;strokeColor=#3700CC;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;676.68\&quot; y=\&quot;1810\&quot; width=\&quot;69.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-57\&quot; value=\&quot;FT数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;220\&quot; y=\&quot;1520\&quot; width=\&quot;60\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

## LLM 训练模式

【2024-3-8】[LLM-SFT-trick](https://zhuanlan.zhihu.com/p/682604566)

微调是指在已经**预训练**好的大型语言模型基础上，使用**特定数据集**进行进一步的训练，使模型适应特定任务或领域。
- 微调主要目的是，完成 知识注入、指令对齐

大模型应用中，指令微调已成为预训练大模型在实际业务应用最重要方式。许多垂直领域模型，都在预训练模型的基础上，通过针对性的指令微调，可以更好地适应最终任务和对齐用户偏好。

指令微调时，会将 **Instruction（指令）** 及对应的**answer**拼接成文本
- 拼接过程中一般会加入【**USER**】、【**BOT**】等角色
- 同时会加入**开始**、**结束**的special token

这样可以转换成一个chat式任务

如翻译任务

```sh
# instruction：
【USER】：将下列内容翻译成英语：｛待翻译文本｝
# answer:
【BOT】：{翻译结果}
# 拼接后的文本：
<bos_token>【USER】：将下列内容翻译成英语：｛待翻译文本｝<special token>【BOT】：{翻译结果} <eos_token>
```

将拼接文本采用预训练任务方式进行自回归预测
- 与预训练的区别：loss的计算，同样使用Cross-Entropy作为loss，指令微调时只会计算answer部分，Instruction部分通过设置ignore_index隐掉。
- 上面的案例中，只会计算 **【BOT】：** 之后的loss。

特定任务改造
- 分类任务: 模型最后添加softmax层。典型案: reward模型。

通过**生成式模**式解决**判别式**任务
- 如**多目标文本分类**问题，采用**指令微调**方式去解决，效果非常好。
- 甚至在7B、3B的base模型上，去生成一个复杂json结构（包含多层结构的标签）依然有效。


微调方法
- 微调方法分为**全参数微调**（Full Fine-tuning）、**部分参数微调**（Repurposing）
- 全微调方法：SFT
- 部分微调方法：LoRA、Adapter、Prefix-tuning、P-tuning、Prompt-tuning 、Freeze-tuning 等。

受GPT论文影响，大模型通用训练模式是**三阶段**训练模式：第一阶段 `pre-train`，第二阶段 `SFT`，第三阶段 `RLHF`。
- 三阶段训练分别得到 **base模型** 以及 **chat模型**
- **chat模型**在**base模型**基础进行**通用任务**的`SFT`以及`RLHF`，使模型具备了对话能力、推理能力、用户偏好对齐、以及其他的NLU的能力。

SFT 训练模式
- 模式一：基于 base模型 + 领域任务的SFT；
- 模式二：基于 base模型 + 领域数据 continue pre-train + 领域任务SFT；
- 模式三：基于 base模型 + 领域数据 continue pre-train + 通用任务SFT + 领域任务SFT；
- 模式四：基于 base模型 + 领域数据 continue pre-train + 通用任务与领域任务混合SFT；
- 模式五：基于 base模型 + 领域数据 continue pre-train（混入SFT数据） + 通用任务与领域任务混合SFT；
- 模式六：基于 chat模型 + 领域任务SFT；
- 模式六：基于 chat模型 + 领域数据 continue pre-train + 领域任务SFT

根据领域任务、领域样本、业务需求选择合适的训练模式。
- a. 是否需要 continue pre-train
  - 大模型的知识来自 pre-train 阶段
  - 如果领域任务数据集与 pre-train 数据集**差异较大**(如领域任务数据来自公司内部)，pre-train 训练样本基本不可能覆盖到，那一定要进行 continue pre-train。
  - 如果领域任务**数据量较大**（token在1B以上），并只追求**领域任务**效果，不考虑通用能力，建议进行continue pre-train。
- b. 选择 chat模型 还是 base模型
  - 如果有好的base模型，在base模型基础进行领域数据的SFT, 与在chat模型上进行SFT，效果上差异不大。
  - 基于**chat模型**进行领域SFT，很容导致**灾难性遗忘**，进行领域任务SFT之后，模型通用能力会降低，如只追求领域任务的效果，则不用考虑。
  - 如果领域任务与通用任务有很大**相关性**，那这种二阶段SFT会提升领域任务效果。
  - 如果既追求领域任务的效果，并且希望通用能力不下降，建议选择 base模型 作为基座模型。在base模型上进行**多任务混合训练**，混合训练的时候需要关注各任务间的数据配比。
- c. 其他
  - 资源运行的情况下，如只考虑领域任务效果，选择模式二；
  - 资源运行的情况下，如考虑模型综合能力，选择模式五；
  - 资源不允许的情况下，考虑模式六；

SFT-训练参数
1. `学习率`
  - 学习率非常重要，如果设置不当，很容易让SFT模型烂掉。
  - SFT数据集不大时，建议设置**较小**学习率，一般为pre-train阶段学习率的**0.1左右**，如在pre-train阶段的学习率为9e-5，则SFT学习率设置为9e-6。
  - 在10万SFT样本上，采用与pre-train一样的学习率，发现loss一直不收敛，在调低学习率至原来0.1之后，loss在两个epoch之后就收敛。
2. `warmup_ratio`
  - 通常 pre-train 训练的 `warmup_ratio` **0.01～0.015**之间，`warmup-steps`在2000左右。
  - SFT 时，建议用更小的ratio，因为相较于pre-train，SFT样本非常小，较小`warmup_ratio`可以使模型收敛更平滑。
  - 但如果学习率设置较大，那可增大 warmup_ratio，两者呈正相关。
3. `Epoch`
  - Epoch 可根据loss收敛情况设置
  - 如果SFT样本较少，可设置较大epoch，在较小的epoch上loss会不收敛，指令都很难遵循。较大epoch会容易导致**过拟合**，但过拟合要优于欠拟合。
  - 如果SFT样本数量较多，如在十万以上，一般**2个epoch**即可收敛。

其它
- 如果SFT任务类型较多，添加 system_prompt，不同任务使用不同 system_prompt；
- 好的基座模型非常重要
- SFT 时，loss依然是最重要的指标，一般在SFT过程中，loss会**先升后降**；
- 尝试多种模式训练方案，如 continue pre-train 中添加SFT数据，在SFT数据添加高质量的pre-train数据；
- 模型参数量非常重要



## ChatGPT 三步走

InstructGPT 分为如下三大步：
- `SFT`：生成模型GPT的`有监督精调` (supervised fine-tuning)
- `RM`：`奖励模型`的训练(reward model training)
- `PPO`：`近端策略优化模型`( reinforcement learning via proximal policy optimization)

`SFT`(supervised fine-tuning) 主要还是大量Prompt数据
- GPT模型通过有监督Prompt数据进行**精调**，即 next token prediction 任务（`NTP`）。
- 然后用精调后的模型对每个输入的 < 文本+prompt > 进行 generate，生成4~9个输出，并且进行解码操作。
- ![SFT流程图](https://pic4.zhimg.com/80/v2-f5be8b02dc60f07a5b45e1d62576938f_1440w.webp)

【2023-11-20】[transformers_tasks](https://github.com/HarderThenHarder/transformers_tasks/tree/main/RLHF) GPT-2 和 RLHF 示例

### GPT 训练流程

【2023-5-23】Andrej Karpathy 在微软Build 2023开发者大会上进行了主题演讲：[State of GPT](https://wangjunjian.com/gpt/2023/05/30/state-of-gpt.html)（GPT的现状）
- pdf: [State of GPT](https://karpathy.ai/stateofgpt.pdf)
- 讲解: [State of GPT：大神Andrej揭秘OpenAI大模型原理和训练过程](https://mp.weixin.qq.com/s/zmEGzm1cdXupNoqZ65h7yg)

<iframe width="560" height="315" src="https://www.youtube.com/embed/YrBJiy-V8MY?si=fg23aN4d4N-5cfwu" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

- ![](https://wangjunjian.com/images/2023/state-of-gpt/gpt-assistant-training-pipeline.jpg)

模型训练分为四个阶段：`预训练`（Pretraining）、`监督微调`（Supervised Finetuning）、`奖励建模`（Reward Modeling）、以及`强化学习`（Reinforcement Learning）。
- 数据量：预训练阶段所需的数据量很大，但质量要求不高；而后面的三个阶段恰恰相反，需要的数据质量较高。
- 训练方法：预训练和监督微调的训练方法相同，都是预测下一个单词。奖励模型和强化学习的训练方法则不同。奖励模型是二元分类学习，而强化学习则鼓励模型生成奖励模型评分较高的回答。
- 训练所需资源：预训练阶段的资源消耗巨大，使用数千颗GPU，花费数月时间，占总训练时间的99%。后面的三个阶段只需使用数十颗GPU，训练时间约数天。

预训练阶段的资源消耗如此巨大，只有大厂才有能力进行。如果资源有限，我们应将重心放在后三个阶段

### ChatGPT流程

InstructGPT和instruction tuning方向的工作比较相关，独特之处在于继承了之前工作的风格——对齐人类偏好。与之前摘要任务相比，instructGPT的prompt分布更多样和复杂。

【2023-5-1】 ChatGPT训练三步流程
- AC架构中，Actor（学习策略）和Critic（学习价值）是两个模型，训练过程中参数都是变动的
- PPO基于A2C算法（同步优势更新的AC），经验回放过程中更新参数
- Critic和RM是一个模型，Instruct GPT论文中，RM 都是6b gpt-3, Critic目标不只是学习RM，还要配合、监督actor同步更新
- RLHF训练过程中涉及4个模型：actor、critic、rm和sft，后两者冻结，前两个持续更新
- PPO损失函数组成：RM打分损失 - β SFT差异损失，即打分高而差异小

备注
1. SFT数据集和RM数据集的prompts来自于API和标注人员编写
  - SFT数据集的回答是**标注人员**写的；
  - PPO数据集来自于**API**
2. Prompts的任务类型包括生成、QA、脑暴、聊天、改写、摘要、分类、抽取等任务。
3. RM模型用了`GPT-3` **6B**，训练方法和之前摘要任务一样。
4. Policy增加一个LM pretrain objective，可以修复alignment tax，让RL policy在公开NLP数据集上表现也很好

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-06-21T06:43:21.717Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;dK9e53EebWgO8fGdeUKJ\&quot; version=\&quot;21.5.0\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1434\&quot; dy=\&quot;771\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-3\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;137.55\&quot; y=\&quot;410\&quot; width=\&quot;712.45\&quot; height=\&quot;380\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-2\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;310\&quot; y=\&quot;290\&quot; width=\&quot;540\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-1\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; y=\&quot;100\&quot; width=\&quot;568.83\&quot; height=\&quot;70\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-25\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-23\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;dashed=1;dashPattern=1 1;strokeColor=#666666;fontColor=#333333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;332.96\&quot; y=\&quot;305\&quot; width=\&quot;194.25\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wGYBfAiltT4hGnPjrrAm-8\&quot; value=\&quot;ChatGPT训练三步走\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=19;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;231.25\&quot; y=\&quot;10\&quot; width=\&quot;224.5\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;g3c7U402eCn0swZi94KO-34\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;strokeWidth=2;fillColor=#f8cecc;strokeColor=#b85450;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-37\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;640\&quot; y=\&quot;725\&quot; /&gt;\n              &lt;mxPoint x=\&quot;640\&quot; y=\&quot;485\&quot; /&gt;\n            &lt;/Array&gt;\n            &lt;mxPoint x=\&quot;545.1150000000001\&quot; y=\&quot;30\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;g3c7U402eCn0swZi94KO-39\&quot; value=\&quot;Policy Gradient Optimization&amp;lt;br&amp;gt;策略梯度优化\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;g3c7U402eCn0swZi94KO-34\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.073\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint y=\&quot;-21\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-3\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-1\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-1\&quot; value=\&quot;SFT数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;194.37\&quot; y=\&quot;100\&quot; width=\&quot;68.59\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-6\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-2\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-2\&quot; value=\&quot;Prompt\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;352.96\&quot; y=\&quot;115\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-4\&quot; value=\&quot;LLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#a20025;strokeColor=#6F0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;492.96\&quot; y=\&quot;115\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-7\&quot; value=\&quot;（1）&amp;lt;font color=&amp;quot;#3333ff&amp;quot;&amp;gt;SFT&amp;lt;/font&amp;gt;: Rollout 监督指令微调\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=15;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;304.3100000000001\&quot; y=\&quot;80\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-8\&quot; value=\&quot;This movie is ___\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#009900;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;387.9600000000001\&quot; y=\&quot;159\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-9\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;really great！&amp;lt;/font&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#009900;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;686.4700000000001\&quot; y=\&quot;159\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-10\&quot; value=\&quot;Response\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;639.99\&quot; y=\&quot;115\&quot; width=\&quot;82.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-12\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-4\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-10\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;542.96\&quot; y=\&quot;130\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;494.96\&quot; y=\&quot;140\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-15\&quot; value=\&quot;（2）&amp;lt;font color=&amp;quot;#3333ff&amp;quot;&amp;gt;RM&amp;lt;/font&amp;gt;: Evaluation 奖励模型\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=15;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;552.9600000000002\&quot; y=\&quot;275\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-16\&quot; value=\&quot;Prompt\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;341.21\&quot; y=\&quot;320\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-17\&quot; value=\&quot;Response\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=17;align=left;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;427.21\&quot; y=\&quot;320\&quot; width=\&quot;82.97\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-19\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;endArrow=classic;endFill=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-2\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;263.96\&quot; y=\&quot;-130\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;313.96\&quot; y=\&quot;-75\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;387.96\&quot; y=\&quot;190\&quot; /&gt;\n              &lt;mxPoint x=\&quot;429.96\&quot; y=\&quot;190\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-21\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;dashed=1;endArrow=classic;endFill=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-10\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;397.96\&quot; y=\&quot;155\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;555.96\&quot; y=\&quot;255\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;681.96\&quot; y=\&quot;190\&quot; /&gt;\n              &lt;mxPoint x=\&quot;429.96\&quot; y=\&quot;190\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-22\&quot; value=\&quot;This movie is &amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;really great！&amp;lt;/font&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#009900;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430.0900000000001\&quot; y=\&quot;380\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-23\&quot; value=\&quot;Reward Model\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#a20025;strokeColor=#6F0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;590.47\&quot; y=\&quot;320\&quot; width=\&quot;112.49\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-24\&quot; value=\&quot;Reward\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;756.96\&quot; y=\&quot;320\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-26\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-23\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-24\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;536.96\&quot; y=\&quot;345\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;600.96\&quot; y=\&quot;345\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-27\&quot; value=\&quot;奖励值: 0/1\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#B5739D;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;798.2600000000002\&quot; y=\&quot;305\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-28\&quot; value=\&quot;Classifier/Rule/Human\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#B5739D;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;645.0600000000003\&quot; y=\&quot;365\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-29\&quot; value=\&quot;（3）&amp;lt;font color=&amp;quot;#3333ff&amp;quot;&amp;gt;PPO&amp;lt;/font&amp;gt;: Optimization 近端策略优化\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];fontSize=15;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490.00000000000017\&quot; y=\&quot;430\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-30\&quot; value=\&quot;log-probs\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#E6E6E6;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;340.27\&quot; y=\&quot;540\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-32\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B3B3B3;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-31\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-30\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-31\&quot; value=\&quot;LLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#66B2FF;strokeColor=#314354;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;339.27\&quot; y=\&quot;470\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-33\&quot; value=\&quot;KL Divergence\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#a0522d;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;372.96\&quot; y=\&quot;620\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-34\&quot; value=\&quot;Reference Model\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#1A1A1A;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380.27000000000015\&quot; y=\&quot;510\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-35\&quot; value=\&quot;log-probs\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#E6E6E6;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;446.02\&quot; y=\&quot;540\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-36\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#B3B3B3;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-37\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-35\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-37\&quot; value=\&quot;LLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FF6666;strokeColor=#6F0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;445.02\&quot; y=\&quot;470\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-38\&quot; value=\&quot;Actor Model\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#1A1A1A;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;492.96000000000015\&quot; y=\&quot;510\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-39\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-30\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-33\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;537.0600000000001\&quot; y=\&quot;385\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;601.0600000000001\&quot; y=\&quot;385\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;380\&quot; y=\&quot;590\&quot; /&gt;\n              &lt;mxPoint x=\&quot;433\&quot; y=\&quot;590\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-40\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-35\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-33\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;390.06\&quot; y=\&quot;585\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;460\&quot; y=\&quot;625\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;486\&quot; y=\&quot;590\&quot; /&gt;\n              &lt;mxPoint x=\&quot;433\&quot; y=\&quot;590\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-41\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-31\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;399.96\&quot; y=\&quot;555\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;452.96\&quot; y=\&quot;605\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-42\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-37\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;439.96\&quot; y=\&quot;375\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;389.96\&quot; y=\&quot;445\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; value=\&quot;PPO\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fa6800;strokeColor=#C73500;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;470.96\&quot; y=\&quot;710\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-6\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-44\&quot; target=\&quot;8uepeCEjrUpFVLacf4Ny-5\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-44\&quot; value=\&quot;PPO_ptx\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;250\&quot; y=\&quot;750\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-45\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-33\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;496.06\&quot; y=\&quot;585\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;443.06\&quot; y=\&quot;635\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-46\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;wbKAMCayHeomiqqS6bZy-16\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;443.06\&quot; y=\&quot;665\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;522.0600000000001\&quot; y=\&quot;705\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;512\&quot; y=\&quot;680\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-47\&quot; value=\&quot;随机抽样\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;126.58999999999989\&quot; y=\&quot;350\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-48\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;7.7w(5.4w)&amp;lt;/font&amp;gt;指令数据集&amp;lt;br&amp;gt;①Web交互数据&amp;lt;br&amp;gt;②API调用抽样\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;29.99999999999993\&quot; y=\&quot;420\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-58\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-49\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-65\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;171.59\&quot; y=\&quot;260\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;126.59\&quot; y=\&quot;370\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-49\&quot; value=\&quot;领域指令集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;32.99999999999999\&quot; y=\&quot;340\&quot; width=\&quot;68.59\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-50\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;1.3w&amp;lt;/font&amp;gt;(12725)&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;&amp;lt;br&amp;gt;&amp;lt;/font&amp;gt;指令数据集\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;228.66999999999993\&quot; y=\&quot;170\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-51\&quot; value=\&quot;奖励数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e3c800;strokeColor=#B09500;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;191.59\&quot; y=\&quot;285\&quot; width=\&quot;78.59\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-52\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-4\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-53\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;432.96\&quot; y=\&quot;140\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;282.96\&quot; y=\&quot;210\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;533.96\&quot; y=\&quot;230\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-53\&quot; value=\&quot;生成数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e3c800;strokeColor=#B09500;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;191.59\&quot; y=\&quot;200\&quot; width=\&quot;78.59\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-54\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.9;entryY=0.017;entryDx=0;entryDy=0;exitPerimeter=0;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-53\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-65\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;543.96\&quot; y=\&quot;155\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;279.96\&quot; y=\&quot;220\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-72\&quot; value=\&quot;排序\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;F3d31tewUV45YqQRhXuj-54\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.2236\&quot; y=\&quot;-2\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-55\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff0080&amp;quot;&amp;gt;3.3w&amp;lt;/font&amp;gt;&amp;lt;font&amp;gt;（33207）&amp;lt;/font&amp;gt;数据集(每个prompt k个回答)&amp;lt;br&amp;gt;&amp;amp;lt;prompt, response_k&amp;amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#990000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;401.58999999999986\&quot; y=\&quot;228\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-56\&quot; value=\&quot;PPO数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;191.59\&quot; y=\&quot;415\&quot; width=\&quot;78.59\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-57\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;3.1w&amp;lt;/font&amp;gt;(31144)&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;&amp;lt;br&amp;gt;&amp;lt;/font&amp;gt;指令数据集\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;228.66999999999993\&quot; y=\&quot;490\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-59\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-49\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-56\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;111.59\&quot; y=\&quot;315\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;162.59\&quot; y=\&quot;140\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;125.59\&quot; y=\&quot;370\&quot; /&gt;\n              &lt;mxPoint x=\&quot;125.59\&quot; y=\&quot;445\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-60\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#ff3333&amp;quot;&amp;gt;10w+ &amp;lt;/font&amp;gt;&amp;lt;font color=&amp;quot;#1a1a1a&amp;quot;&amp;gt;Pair wise句子对&amp;lt;/font&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;232.9599999999999\&quot; y=\&quot;350\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-62\&quot; value=\&quot;标注人员&amp;lt;br&amp;gt;（肯尼亚40人）\&quot; style=\&quot;shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;65.74000000000001\&quot; y=\&quot;236\&quot; width=\&quot;20.71\&quot; height=\&quot;39\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-65\&quot; value=\&quot;人工标注\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=15;fontColor=#333333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;91.59\&quot; y=\&quot;245\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-66\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-65\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;111.59\&quot; y=\&quot;315\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;136.59\&quot; y=\&quot;220\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;126.59\&quot; y=\&quot;130\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-70\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.75;exitDx=0;exitDy=0;entryX=0.145;entryY=0;entryDx=0;entryDy=4.35;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-65\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-51\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;201.59\&quot; y=\&quot;240\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;171.59\&quot; y=\&quot;255\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-76\&quot; value=\&quot;扩展10倍\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;F3d31tewUV45YqQRhXuj-70\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.286\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-71\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=1;entryDx=0;entryDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-56\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-18\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;171.59\&quot; y=\&quot;278\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;212.59\&quot; y=\&quot;299\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-73\&quot; value=\&quot;【2023-6-19】&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;edgeLabel;html=1;align=left;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;680\&quot; y=\&quot;765\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-75\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; source=\&quot;8uepeCEjrUpFVLacf4Ny-4\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;534.5999999999999\&quot; y=\&quot;90\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-77\&quot; value=\&quot;&amp;amp;lt;prompt,response&amp;amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#990000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;126.58999999999989\&quot; y=\&quot;190\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;F3d31tewUV45YqQRhXuj-78\&quot; value=\&quot;&amp;amp;lt;prompt&amp;amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#990000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;65.73999999999988\&quot; y=\&quot;445\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-3\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;wbKAMCayHeomiqqS6bZy-1\&quot; target=\&quot;wbKAMCayHeomiqqS6bZy-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-1\&quot; value=\&quot;预训练数据集\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#ffe6cc;strokeColor=#d79b00;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;30\&quot; y=\&quot;510\&quot; width=\&quot;77\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-5\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;wbKAMCayHeomiqqS6bZy-2\&quot; target=\&quot;wbKAMCayHeomiqqS6bZy-6\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-2\&quot; value=\&quot;LLM\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FF6666;strokeColor=#6F0000;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;146.66999999999996\&quot; y=\&quot;520\&quot; width=\&quot;82\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-4\&quot; value=\&quot;CE Loss\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#a0522d;strokeColor=none;shadow=1;fontSize=17;fontColor=#ffffff;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;142.87\&quot; y=\&quot;630\&quot; width=\&quot;88.38\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-8\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;wbKAMCayHeomiqqS6bZy-6\&quot; target=\&quot;wbKAMCayHeomiqqS6bZy-4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-6\&quot; value=\&quot;log-probs\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#E6E6E6;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;146.66999999999996\&quot; y=\&quot;570\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-9\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;wbKAMCayHeomiqqS6bZy-4\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-44\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;443\&quot; y=\&quot;670\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;522\&quot; y=\&quot;720\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;187\&quot; y=\&quot;720\&quot; /&gt;\n              &lt;mxPoint x=\&quot;285\&quot; y=\&quot;720\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-10\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; target=\&quot;F3d31tewUV45YqQRhXuj-44\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;410\&quot; y=\&quot;760\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;532\&quot; y=\&quot;730\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;285\&quot; y=\&quot;720\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-11\&quot; value=\&quot;Lvalue = r(xy,y) = E[log(r(x,yi)-r(x,y1-i))]\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC0000;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;770\&quot; y=\&quot;620.0000799996801\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-12\&quot; value=\&quot;L =&amp;amp;nbsp; Lvalue &amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;- β&amp;lt;/font&amp;gt;Lppo\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC0000;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;511.96000000000004\&quot; y=\&quot;750.0000799996801\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-13\&quot; value=\&quot;L = Lvalue &amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;- β&amp;lt;/font&amp;gt;Lppo&amp;amp;nbsp; + &amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;γ&amp;lt;/font&amp;gt; Lptx\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC0000;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;290.00000000000006\&quot; y=\&quot;800.0000799996801\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-14\&quot; value=\&quot;Lppo = log[ π^rl(y|x) / π^sft(y|x) ]\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC0000;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;526.02\&quot; y=\&quot;660.0000799996801\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-15\&quot; value=\&quot;Lptx = E[log π^rl(x)]\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontColor=#CC0000;fontStyle=1\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;238.38000000000005\&quot; y=\&quot;700.0000799996801\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;4\&quot; y=\&quot;-2\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-17\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-24\&quot; target=\&quot;wbKAMCayHeomiqqS6bZy-16\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;792\&quot; y=\&quot;350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;870\&quot; y=\&quot;560\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-18\&quot; value=\&quot;初始化\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; parent=\&quot;wbKAMCayHeomiqqS6bZy-17\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.4091\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-16\&quot; value=\&quot;Reward\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#FF6666;strokeColor=none;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;756.96\&quot; y=\&quot;570\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-19\&quot; value=\&quot;Critic Model\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontColor=#1A1A1A;fontStyle=1;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;798.2600000000002\&quot; y=\&quot;610\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-6\&quot; y=\&quot;-1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-20\&quot; value=\&quot;目标：得分高 + 与SFT差异小\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510.1799999999999\&quot; y=\&quot;770\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-21\&quot; value=\&quot;SFT模型冻结\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;801.96\&quot; y=\&quot;511\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-428\&quot; y=\&quot;-68\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-22\&quot; value=\&quot;目标：得分高 + 与SFT差异小 + 预训练差异小\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;304.30999999999983\&quot; y=\&quot;817\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wbKAMCayHeomiqqS6bZy-23\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;strokeWidth=2;fillColor=#f8cecc;strokeColor=#b85450;dashed=1;dashPattern=1 2;\&quot; parent=\&quot;1\&quot; source=\&quot;F3d31tewUV45YqQRhXuj-43\&quot; target=\&quot;wbKAMCayHeomiqqS6bZy-16\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;640\&quot; y=\&quot;725\&quot; /&gt;\n              &lt;mxPoint x=\&quot;640\&quot; y=\&quot;585\&quot; /&gt;\n            &lt;/Array&gt;\n            &lt;mxPoint x=\&quot;537\&quot; y=\&quot;495\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;563\&quot; y=\&quot;735\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-4\&quot; value=\&quot;GPT-3\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=14;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;498.44\&quot; y=\&quot;60\&quot; width=\&quot;71.04\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-8\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;8uepeCEjrUpFVLacf4Ny-5\&quot; target=\&quot;8uepeCEjrUpFVLacf4Ny-7\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-9\&quot; value=\&quot;对话语料微调\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;8uepeCEjrUpFVLacf4Ny-8\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.082\&quot; y=\&quot;4\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1\&quot; y=\&quot;-4\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-5\&quot; value=\&quot;InsructGPT\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=14;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;245\&quot; y=\&quot;840\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8uepeCEjrUpFVLacf4Ny-7\&quot; value=\&quot;ChatGPT\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;shadow=1;fontSize=14;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;427.4\&quot; y=\&quot;840\&quot; width=\&quot;71.04\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

### 优化

**全参数**微调：对模型所有参数进行调整，如：SFT
- 问题：代价大（模型大、数据多、参数量大）

**混合精度**微调：<span style='color:red'>省显存、加速，但丢失精度</span>
- 训练时同时使用**16位**、**32位浮**点类型，加速，减少内存开销
- 部分参数使用**32位**类型，以保持数值稳定性，缩短单步用时
- 现代加速器使用16位专用硬件执行运算，速度更快

注意
- FP16: 内存存储、乘法运算
- FP32: 累加运算，避免下溢
- 手动放大梯度，以避免梯度爆炸，这样 FP16和FP32运算时，不容易出现下溢

其它加速方法
- **多卡**并行：数据并行、模型并行
- `ZeRO`：分布式机器学习的新型内存优化技术，将三个步骤（optimizer state partitioning/add gradient partitioning/add parameter partitioning）拆分到不同的卡上，相比 数据并行，节省GPU
- `p-tuning`：通过prompt encoder结构将prompt编码为向量，再与input embedding拼接。增加模型理解能力
- `LoRA`：低秩适配，冻结大模型权重，只训练新增的网络层（两个小矩阵的乘积），降低fine-tune成本，同时保持类似效果


### （1） 第一步 SFT（全参数微调）

SFT 原理比较简单，难的是数据问题，需要大量的有监督Prompt文本
- ![img](https://pic3.zhimg.com/80/v2-45331e791fad76d81694bd61e806db8a_1440w.webp)
- Transformer【左】GPT【右】

大模型训练**基座模型**时，都采用「Next Token Prediction，`NTP`」 任务

#### IFT 的问题

5 月，伯克利的论文 The False Promise of Imitating Proprietary LLMs 指出这种方式微调出来的**指令遵循**模型存在的一系列问题：
- 在缺少大量模仿 ChatGPT 数据支持的任务上，这类模型无法改善 Base Model 到 ChatGPT 的差距；
- 这类模型只是擅长模仿 ChatGPT 的风格，而不是事实性，导致实际的性能差异会骗过人类评估者；
- 当前开源模型最大的限制仍然是 Base Model 层面跟 GPT 系列的差距，在微调而不是预训练环境进行优化可能是不正确的方向；
- 为了广泛地匹配 ChatGPT 支持的任务，需要更广泛和大量的模仿数据集，还需要新的工作；

而 6 月份 Allen Institute for AI 和华盛顿大学的 How Far Can Camels GO ？工作再次通过实验表明不同的指令微调数据集可以释放或者增强特定的能力，但并没有一个数据集或者组合可以在所有的评估中提供最佳性能，并且这一点在人类或模型担任评估者时也很容易无法被揭示。

对于指令遵循微调背后的团队来说，他们也意识到自己的模型由于 Base Model（LLaMA）的限制，在复杂推理和代码任务上很弱，并且难以进入正向数据飞轮 —— 模型能力越弱的领域越难得到更多的 query，也就难以筛选出高质量 query，想自己再标注提升模型能力就很困难。

至此，开源社区已经充分意识到原来这套微调 LLaMA 的框架的局限性，越来越多的团队开始探索预训练环节和更接近真实的人类反馈数据

#### 数据示例

数据准备

| Raw Data	| Prompt	| Label |
|---|---|---|
| 我们去成都旅游，必须要去的地方是大熊猫繁殖基地。 |	大熊猫是 |	一种有黑白斑纹的动物。|
| 我们去成都旅游，必须要去的地方是大熊猫繁殖基地。 |	大熊猫是 |	中国特有种，主要栖息地是中国四川、陕西和甘肃的山区。|
| 我们去成都旅游，必须要去的地方是大熊猫繁殖基地。 |	大熊猫是 |	已在地球上生存了至少800万年，被誉为“活化石”和“中国国宝”即国兽，世界自然基金会的形象大使，是世界生物多样性保护的旗舰物种。|
| 我们去成都旅游，必须要去的地方是大熊猫繁殖基地。 |	大熊猫是 |	属于熊科、大熊猫属的哺乳动物。仅有二个亚种。雄性个体稍大于雌性。体型肥硕似熊、丰腴富态，头圆尾短，头躯长1.2-1.8米，尾长10-12厘米。|

```py
raw_data = "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。"
prompt = "大熊猫是"
labels = ["一种有黑白斑纹的动物。","中国特有种，主要栖息地是中国四川、陕西和甘肃的山区。",
"已在地球上生存了至少800万年，被誉为“活化石”和“中国国宝”即国兽，世界自然基金会的形象大使，是世界生物多样性保护的旗舰物种。",
"属于熊科、大熊猫属的哺乳动物。仅有二个亚种。雄性个体稍大于雌性。体型肥硕似熊、丰腴富态，头圆尾短，头躯长1.2-1.8米，尾长10-12厘米。"]
combine_data = [raw_data+prompt+label for label in labels]
```

初始化模型，对输入数据进行编码, 以 [GPT-2](https://huggingface.co/uer/gpt2-chinese-cluecorpussmall) 模型为例


```py
from torch.utils.data import Dataset
from transformers import Trainer, TrainingArguments
from transformers import AutoTokenizer, AutoModelForCausalLM
# 模型加载
tokenizer = BloomTokenizerFast.from_pretrained('pre_train_model/gpt2')
model = BloomForCausalLM.from_pretrained('pre_train_model/gpt2')
# 自定义DataSet类
class Datasets(Dataset):
    def __init__(self, sample):
        super(Datasets, self).__init__()
        self.sample = sample

    def __getitem__(self, item):
        res = {k: v[item] for k, v in self.sample.items()}
        return res

    def __len__(self):
        return len(self.sample['labels'])
# 数据转换
combine_data_token = tokenizer.batch_encode_plus(
    initial_data_,
    max_length=256,
    padding='max_length',
    truncation=True,
    return_tensors='pt'
)
# 将标签标签加入
combine_data_token['labels'] = combine_data_token['input_ids']
combine_data_token['labels'] = torch.where(
    combine_data_token['labels']==0,
    -100,
    combine_data_token['labels']
)
# 模型训练保存
trainer_args = TrainingArguments("./model/", learning_rate=2e-5, weight_decay=0.01, num_train_epochs=10, auto_find_batch_size=True)
trainer = Trainer(model=initial_model, args=trainer_args, train_dataset=Datasets(initial_token_info))
trainer.train()
trainer.save_model()
# ----- 加载生成 --------
# 加载模型
model = AutoModelForCausalLM.from_pretrained('./model')
# 处理输入数据
input_data = raw_input + prompt
input_datas = tokenizer.encode_plus(
    input_data,
    return_tensors='pt'
)
input_ids = input_datas['input_ids']
# 模型生成
result = model.generate(
    input_ids=input_ids,
    max_length=256,
    do_sample=True,  # 增加随机性
    num_beams=5,
    num_return_sequences=5,  # 每个样本生成5个结果
    no_repeat_ngram_size=3,  # 防止重复的token
    early_stopping=True  # 提前停止
)

decode_tokens = tokenizer.batch_decode(
    result,
    skip_special_tokens=True
)

results = [i.replace(' ', '') for i in decode_tokens]

print("results",results)
```


结果：


```s
我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是今世界上保存最完好的哺乳动物之一，也是世界自然保护联盟濒危物种红色名录的保护对象之一。在这里，你可以看到全世界最大的熊猫栖息地成都。成都是中国国家林业局直属的国家重点风景名胜区，是国家森林公园、国家湿地公园和国家地质公园的重要组成部分，是全国重点文物保护单位、全国生态文明建设示范区、中国红色旅游名城、国际生态旅游目的地和国际旅游岛建设先进区。地址：四川省成都市绵阳市成华区成都高新技术产业开发区成华大道1号乘车路线：成都绵阳都江堰雅
我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家二级保护动物，是世界上保存最完整的动物种群之一，也是我国第一个国家级自然保护区。我们是四川省的首批国家重点保护野生动物和珍稀动物基金会的成员，被誉为中国动物保护的摇篮和世界生物多样性保护基地，被中国科学院、中华人民共和国国家林业局授予全国生态文明建设示范区称号，被国务院批准为国家森林城市、国际生态旅游目的地。熊猫基地位于成都市双流区东南部，是国家aaaa级旅游景区，国家地理标志保护单位。熊猫栖息地为亚热带或热带的高山
我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完好的熊猫种群之一。它们栖息在亚热带或热带的高海拔草原上，生活环境十分优越，是中国四大自然奇观之一，被誉为世界自然遗产和中国国家森林公园。熊猫栖息地主要分布在中国大陆的西藏、青海、甘肃、宁夏、新疆、内蒙古、山西、辽宁、吉林、黑龙江、江苏、河南、安徽、湖北、湖南、江西、广东、海南、四川、云南、贵州、陕西等地。中国熊猫研究中心主任、中国科学院院士、国家自然科学基金委员会委员、中华全国工商业联合会副主席
我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完整、规模最大的野生动物种类繁多的地区之一，是中国国家重点保护的珍稀濒危动物及其栖息地和世界自然遗产的重要组成部分，被誉为中国最美丽的城市和世界生物多样性保护基地，被国际旅游组织评为全球生态旅游目的地。成都熊猫国家公园位于四川省甘孜藏族自治州，是国家aaaa级旅游景区，被《世界遗产名录》列为全国重点文物保护单位。目前，我国已建成国家森林公园、国家湿地公园和国家地质公园，国家林业局、国务院扶贫
我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是现存最大、保存最完整的动物，属于国家二级保护动物。熊猫种类繁多，分布广泛，主要分布在四川、云南、陕西、甘肃、宁夏、内蒙古、新疆、青海、吉林、辽宁、黑龙江、山西、江苏、江西、河南、湖北、湖南、广东、广西、海南、重庆、贵州、西藏、四川等省区市。它们的栖息地主要为亚热带或热带的（低地）湿润低地林、亚高山草原、高山湖泊、高原湿润山区和高原沼泽地等，常栖息在高海拔地区。在中国大陆，熊猫分布于四川省甘孜藏族自治州和青海省西宁市等地。雄性熊猫体长约1.5米
```

这和instructGPT的SFT过程大致相同，思路原理是一样的，差别是 缺乏硬件设备、大规模高质量监督数据
- ChatGPT原理详解+实操: [SFT(GPT模型精调)](https://zhuanlan.zhihu.com/p/609795142), [RM(reward model)](https://zhuanlan.zhihu.com/p/610147705)

引入RM模型的作用是对生成的文本进行打分排序，让模型生成的结果更加符合人类的日常理解习惯，更加符合人们想要的答案。RM模型主要分为两个部分：训练数据获取和模型训练部分。流程如下图所示

#### Bloom SFT

【2023-5-23】[bloom_tuning: BLOOM 模型的指令微调](https://mp.weixin.qq.com/s/f369M-BKI6-MYb0nqvYFNQ)
- Github: [bloom_tuning](https://github.com/zejunwang1/bloom_tuning)
- 模型: [bloom-396m-chat](https://huggingface.co/WangZeJun/bloom-396m-chat)

BLOOM 系列模型是由数百名研究人员在包含 46 种自然语言和 13 种编程语言的数据集上, 基于大规模分布式训练框架 `Megatron-DeepSpeed` 训练得到。
- 实验发现，BLOOM 在一系列基准测试上取得了具有竞争力的性能，经过**多任务**提示微调后，可以获得更为惊艳的效果。
- BLOOM 模型支持中文、英文、代码、法语、西班牙语。

链接：[bloom-560m](https://huggingface.co/bigscience/bloom-560m)

[LLMPruner](https://github.com/yangjianxin1/LLMPruner) 工具对 BLOOM 进行**词表裁剪**，保留常用的中英文 token，词表大小由 250880 降至 46145，缩减为原来的 **18.39%**，在后续微调过程中可以减少显存占用。
- 词表裁剪后的模型链接：[bloom-396m-zh](https://huggingface.co/YeungNLP/bloom-396m-zh)

##### 数据

训练数据来自于 [BelleGroup/train_3.5M_CN](https://huggingface.co/datasets/BelleGroup/train_3.5M_CN)，该数据集包含 **3.6M** 条指令，从中筛选出单轮对话数据，进行 10:1 采样后得到约 0.25M 指令数据：

```py
python sample_data.py \
--input data/train_3.5M_CN.json \
--output data/train.jsonl \
--sample_ratio 0.1
```

单条指令数据形如：

```json
{
    "instruction": "你好，请问你能做什么？", 
    "output": "你好，我可以回答各种问题，提供辅助，或者与你聊天。有什么我可以帮你的吗？"
}
```

输出部分的长度分布如下图所示（若输出长度超过2048，则设置为2048）

##### 指令微调

基于 deepspeed ZeRO-Stage 2 进行指令微调训练：

```py
deepspeed --include localhost:0 train.py \
--model_name_or_path /path/to/bloom \
--data_path data/train.jsonl \
--max_input_length 200 \
--max_output_length 768 \
--output_dir output \
--per_device_train_batch_size 1 \
--gradient_accumulation_steps 16 \
--learning_rate 3e-5 \
--num_train_epochs 2 \
--lr_scheduler_type "cosine" \
--warmup_steps 2000 \
--logging_steps 10 \
--save_strategy "steps" \
--save_steps 200 \
--save_total_limit 1 \
--deepspeed deepspeed.json \
--fp16 False
```

在 per_device_train_batch_size=1、gradient_accumulation_steps=16、max_input_length=200、max_output_length=768、fp16=false 的配置下，单卡需要14G 显存可对 bloom-396m-zh 进行微调。

##### 推理

微调后的模型已上传至 huggingface: [bloom-396m-chat](https://huggingface.co/WangZeJun/bloom-396m-chat)

可以通过如下代码调用 bloom-396m-chat 模型来生成对话：

```py
from transformers import BloomTokenizerFast, BloomForCausalLM

model_name_or_path = "WangZeJun/bloom-396m-chat"

tokenizer = BloomTokenizerFast.from_pretrained(model_name_or_path)
model = BloomForCausalLM.from_pretrained(model_name_or_path).cuda()
model = model.eval()

input_pattern = "{}</s>"
text = "你好"
input_ids = tokenizer(input_pattern.format(text), return_tensors="pt").input_ids
input_ids = input_ids.cuda()

outputs = model.generate(input_ids, do_sample=True, max_new_tokens=1024, top_p=0.85,
    temperature=0.3, repetition_penalty=1.2, eos_token_id=tokenizer.eos_token_id)

output = tokenizer.decode(outputs[0])
response = output.replace(text, "").replace('</s>', "")
print(response)
```

运行如下命令进行命令行推理：

```py
python chat.py \
--model_name_or_path /path/to/model \
--max_new_tokens 1024 \
--top_p 0.85 \
--temperature 0.3 \
--repetition_penalty 1.2
```

##### 测试

| 用户	| Assistant |
|---|---|
| 你好	| 您好，有什么我可以帮您的吗？ |
| 你是谁	| 我是一个AI语言模型，没有个人身份和情感。我的目的是回答你的问题并提供有用的信息来帮助你解决问题或提供娱乐性内容。如果你有任何其他的问题需要解答，请随时问我！ |


### （2）第二步 RM训练

**奖励模型**（Reward Model, RM）目标是刻画模型的输出是否在人类看来表现不错。
- 输入: \[提示(prompt)，模型生成的文本\] 
- 输出: 一个刻画文本质量的标量数字。
- ![](https://pic2.zhimg.com/80/v2-51ad9f0f11ba272611a068d380e7fe41_1440w.webp)

同一个prompt输出的多个答案，人工评测排序后，使用lambdarank的思想，优化RM奖励模型。

RM模型学习的就是对于一个prompt，人类对答案的喜好程度。
- RM模型【左】RM损失函数【右】
- ![](https://pic3.zhimg.com/80/v2-6b22d510b56efc300b6bb1686407a40e_1440w.webp)
- ![rm](https://pic1.zhimg.com/v2-bc1af700e9147ae7458824f5619b1ed4_b.jpg)

奖励模型接收一系列文本并返回一个标量奖励，数值上对应人的偏好

引入RM模型的作用是对生成的文本进行打分排序，让模型生成的结果更加符合人类的日常理解习惯，更加符合人们想要的答案。

RM模型主要分为两个部分：数据获取和模型训练。流程如下图所示
- ![](https://pic2.zhimg.com/80/v2-ac62759c2862ab04a024d51fe2a19991_1440w.webp)

原论文中使用GPT架构做了一个reward model

注意
- 要将模型的输出映射成维度为1的**打分向量**，即增加一个linear结构。

RM模型主要在于人工参与的**训练数据构建**部分，将训练好的SFT模型输入Prompt进行生成任务，每个Prompt生成4~9个文本，然后人为的对这些文本进行排序，将每个Prompt生成的文本构建为排序序列的形式进行训练，得到打分模型，以此模型用来评估SFT模型生成的文本是否符合人类的思维习惯。

两种方法命名为 direct score 和 rank score：
- `Direct score`：一个是直接对输出的文本进行打分，通过与自定义的label score计算loss，以此来更新模型参数；
- `Rank score`：二是使用排序的方法，对每个Prompt输出的n个句子进行排序作为输入，通过计算排序在前面的句子与排序在后面的句子的差值累加作为最终loss。

【2023-6-5】[ChatGPT 为什么不用 Reward-Model 的数据直接 fine-tune，而用 RL？](https://www.zhihu.com/question/596230048/answer/3055888005)
- Reward-model的输出对于整个token序列，一种滞后反馈，而finetune需要在每个token都有监督信号。这是强化学习与监督学习的差别。
- 生成Reward-model的数据有些是结果对比较**pair数据**，没法直接用于监督学习finetune。

#### ① Direct score方法

① Direct score方法
- 利用 Bert模型对标注数据进行编码，用 linear层 映射到1维，然后利用Sigmoid函数输出每个句子的得分，与人工标记的得分进行loss计算，以此来更新模型参数。流程如下所示
- ![](https://pic1.zhimg.com/80/v2-c040a19b5054a8b6076a4f4e1506b784_1440w.webp)

数据为SFT最后所生成的数据，数据准备：

```py
def data_prepare(pretrain_path):
    data_lst = [
        "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是今世界上保存最完好的哺乳动物之一，也是世界自然保护联盟濒危物种红色名录的保护对象之一。在这里，你可以看到全世界最大的熊猫栖息地成都。成都是中国国家林业局直属的国家重点风景名胜区，是国家森林公园、国家湿地公园和国家地质公园的重要组成部分，是全国重点文物保护单位、全国生态文明建设示范区、中国红色旅游名城、国际生态旅游目的地和国际旅游岛建设先进区。地址：四川省成都市绵阳市成华区成都高新技术产业开发区成华大道1号乘车路线：成都绵阳都江堰雅",
        "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家二级保护动物，是世界上保存最完整的动物种群之一，也是我国第一个国家级自然保护区。我们是四川省的首批国家重点保护野生动物和珍稀动物基金会的成员，被誉为中国动物保护的摇篮和世界生物多样性保护基地，被中国科学院、中华人民共和国国家林业局授予全国生态文明建设示范区称号，被国务院批准为国家森林城市、国际生态旅游目的地。熊猫基地位于成都市双流区东南部，是国家aaaa级旅游景区，国家地理标志保护单位。熊猫栖息地为亚热带或热带的高山",
        "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完好的熊猫种群之一。它们栖息在亚热带或热带的高海拔草原上，生活环境十分优越，是中国四大自然奇观之一，被誉为世界自然遗产和中国国家森林公园。熊猫栖息地主要分布在中国大陆的西藏、青海、甘肃、宁夏、新疆、内蒙古、山西、辽宁、吉林、黑龙江、江苏、河南、安徽、湖北、湖南、江西、广东、海南、四川、云南、贵州、陕西等地。中国熊猫研究中心主任、中国科学院院士、国家自然科学基金委员会委员、中华全国工商业联合会副主席",
        "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完整、规模最大的野生动物种类繁多的地区之一，是中国国家重点保护的珍稀濒危动物及其栖息地和世界自然遗产的重要组成部分，被誉为中国最美丽的城市和世界生物多样性保护基地，被国际旅游组织评为全球生态旅游目的地。成都熊猫国家公园位于四川省甘孜藏族自治州，是国家aaaa级旅游景区，被《世界遗产名录》列为全国重点文物保护单位。目前，我国已建成国家森林公园、国家湿地公园和国家地质公园，国家林业局、国务院扶贫",
        "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是现存最大、保存最完整的动物，属于国家二级保护动物。熊猫种类繁多，分布广泛，主要分布在四川、云南、陕西、甘肃、宁夏、内蒙古、新疆、青海、吉林、辽宁、黑龙江、山西、江苏、江西、河南、湖北、湖南、广东、广西、海南、重庆、贵州、西藏、四川等省区市。它们的栖息地主要为亚热带或热带的（低地）湿润低地林、亚高山草原、高山湖泊、高原湿润山区和高原沼泽地等，常栖息在高海拔地区。在中国大陆，熊猫分布于四川省甘孜藏族自治州和青海省西宁市等地。雄性熊猫体长约1.5米"]
    # 自定义打分标签，每个句子一个分值。也可以定义多维度的打分方法，只是模型的线性层需要改为你所定义的维度数
    direct_score = [[0.75], [0.5], [0.35], [0.4], [0.8]]
    tokenizer = BertTokenizer.from_pretrained(pretrain_path)
    train_data = tokenizer.batch_encode_plus(data_lst, max_length=256, padding="max_length", truncation=True,
                                             return_tensors='pt')
    train_data["labels"] = torch.tensor(direct_score)
    return train_data, tokenizer
```

RM模型搭建
- 采用了Bert模型作为编码模型，后取CLS作为文本表征，采用MSE作为loss函数，最后接linear进行维度压缩

```py
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertModel, BertPreTrainedModel, BertTokenizer, BertConfig, get_scheduler


class RewardModel(BertPreTrainedModel):
    def __init__(self, config):
        super(RewardModel, self).__init__(config)
        self.config = config
        self.sigmoid = nn.Sigmoid()
        self.loss_fn = nn.MSELoss()
        self.model = BertModel(config)
        self.linear = nn.Linear(config.hidden_size, 1)

    def forward(self, input_ids, token_type_ids, attention_mask, labels=None):
        outputs = self.model(input_ids=input_ids, token_type_ids=token_type_ids,
                             attention_mask=attention_mask).pooler_output
        output = self.linear(outputs)
        logits = self.sigmoid(output)
        if labels is not None:
            loss = self.loss_fn(logits, labels)
            return logits, loss
        else:
            return logits
```

训练过程

```py
class Datasets(Dataset):
    def __init__(self, sample):
        super(Datasets, self).__init__()
        self.sample = sample

    def __getitem__(self, item):
        res = {k: v[item] for k, v in self.sample.items()}
        return res

    def __len__(self):
        return len(self.sample['input_ids'])


def train(pretrain_path, save_path):
    config = BertConfig.from_pretrained(pretrain_path)
    model = RewardModel(config=config)

    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": 0.01,
        },
        {
            "params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
    ]
    optimizer = torch.optim.AdamW(optimizer_grouped_parameters, lr=2e-5)
    train_data, tokenizer = data_prepare(pretrain_path)
    dataloader = DataLoader(dataset=Datasets(train_data), shuffle=False, batch_size=1)

    max_train_steps = 10 * len(dataloader)
    warm_steps = int(0.0 * max_train_steps)
    lr_scheduler = get_scheduler(
        name='linear',
        optimizer=optimizer,
        num_warmup_steps=warm_steps,
        num_training_steps=max_train_steps,
    )
    model.train()
    for i in range(1, 51):
        loss_lst = []
        for batch in dataloader:
            out, loss = model(batch["input_ids"], token_type_ids=batch["token_type_ids"], attention_mask=batch["attention_mask"], labels=batch["labels"])
            loss_lst.append(loss.item())
            loss.backward()
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
        print("epoch{}\tloss: {}".format(str(i), str(sum(loss_lst) / len(loss_lst))))
    tokenizer.save_pretrained(save_path)
    model_to_save = model.module if hasattr(model, 'module') else model
    model_to_save.save_pretrained(save_path)
    model_to_save.config.save_pretrained(save_path)
```

模型预测

```py
def predict(model_path):
    text = ["我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是今世界上保存最完好的哺乳动物之一，也是世界自然保护联盟濒危物种红色名录的保护对象之一。在这里，你可以看到全世界最大的熊猫栖息地成都。成都是中国国家林业局直属的国家重点风景名胜区，是国家森林公园、国家湿地公园和国家地质公园的重要组成部分，是全国重点文物保护单位、全国生态文明建设示范区、中国红色旅游名城、国际生态旅游目的地和国际旅游岛建设先进区。地址：四川省成都市绵阳市成华区成都高新技术产业开发区成华大道1号乘车路线：成都绵阳都江堰雅",
            "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家二级保护动物，是世界上保存最完整的动物种群之一，也是我国第一个国家级自然保护区。我们是四川省的首批国家重点保护野生动物和珍稀动物基金会的成员，被誉为中国动物保护的摇篮和世界生物多样性保护基地，被中国科学院、中华人民共和国国家林业局授予全国生态文明建设示范区称号，被国务院批准为国家森林城市、国际生态旅游目的地。熊猫基地位于成都市双流区东南部，是国家aaaa级旅游景区，国家地理标志保护单位。熊猫栖息地为亚热带或热带的高山",]
    model = RewardModel.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)

    model.eval()
    data = tokenizer.batch_encode_plus(text, max_length=256, padding="max_length", truncation=True,
                                           return_tensors='pt')
    score = model(**data)
    return score
```

完成了一个基于Bert的文本打分模型。
- 当然，这里展示的只是个思路，模型也很粗糙，而且自定义的打分标签也经不起推敲。

#### ② Rank score方法

② Rank score方法

这种方法的区别在于：**loss函数的设计**。
- 首先，为什么在 InstructGPT 中不采用上面方法? 原因在于给生成句子在打分时，<span style='color:red'>不同标注人员的标准不同</span>，而且这个标准是很难进行统一的，这样会导致标注的数据评判标准不一样，即使每个标注人员的理解是一样的，但对于同一条文本给的分数也不一样的，因此在进行标注时需要把这个定量的问题转为一种更为简单的处理方法，采用排序来方法来进行数据标注可以在一定程度上解决这个问题。
- ![](https://pic1.zhimg.com/80/v2-92a39e17763405c7a55977880f520018_1440w.webp)
- 标注员在使用直接打分(Direct Score)时，会由于主观意识的不同，对同一个文本出现不同的分值；而使用**等级排序**(Rank Level)来进行数据标注时，可以统一标注结果。



数据是将每个Prompt生成的文本进行排序，最直接的方法就是最好的句子排在最前面，后面的句子以此类推。

```py
def rank_data_prepare(pretrain_path):
    data_lst = []
    data_outputs = {
        'input_ids': [],
        'token_type_ids': [],
        'attention_mask': []
    }
    data_str = "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是现存最大、保存最完整的动物，属于国家二级保护动物。熊猫种类繁多，分布广泛，主要分布在四川、云南、陕西、甘肃、宁夏、内蒙古、新疆、青海、吉林、辽宁、黑龙江、山西、江苏、江西、河南、湖北、湖南、广东、广西、海南、重庆、贵州、西藏、四川等省区市。它们的栖息地主要为亚热带或热带的（低地）湿润低地林、亚高山草原、高山湖泊、高原湿润山区和高原沼泽地等，常栖息在高海拔地区。在中国大陆，熊猫分布于四川省甘孜藏族自治州和青海省西宁市等地。雄性熊猫体长约1.5米\t我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是今世界上保存最完好的哺乳动物之一，也是世界自然保护联盟濒危物种红色名录的保护对象之一。在这里，你可以看到全世界最大的熊猫栖息地成都。成都是中国国家林业局直属的国家重点风景名胜区，是国家森林公园、国家湿地公园和国家地质公园的重要组成部分，是全国重点文物保护单位、全国生态文明建设示范区、中国红色旅游名城、国际生态旅游目的地和国际旅游岛建设先进区。地址：四川省成都市绵阳市成华区成都高新技术产业开发区成华大道1号乘车路线：成都绵阳都江堰雅\t我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家二级保护动物，是世界上保存最完整的动物种群之一，也是我国第一个国家级自然保护区。我们是四川省的首批国家重点保护野生动物和珍稀动物基金会的成员，被誉为中国动物保护的摇篮和世界生物多样性保护基地，被中国科学院、中华人民共和国国家林业局授予全国生态文明建设示范区称号，被国务院批准为国家森林城市、国际生态旅游目的地。熊猫基地位于成都市双流区东南部，是国家aaaa级旅游景区，国家地理标志保护单位。熊猫栖息地为亚热带或热带的高山\t我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完整、规模最大的野生动物种类繁多的地区之一，是中国国家重点保护的珍稀濒危动物及其栖息地和世界自然遗产的重要组成部分，被誉为中国最美丽的城市和世界生物多样性保护基地，被国际旅游组织评为全球生态旅游目的地。成都熊猫国家公园位于四川省甘孜藏族自治州，是国家aaaa级旅游景区，被《世界遗产名录》列为全国重点文物保护单位。目前，我国已建成国家森林公园、国家湿地公园和国家地质公园，国家林业局、国务院扶贫\t我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家级自然保护区，也是世界上保存最完好的熊猫种群之一。它们栖息在亚热带或热带的高海拔草原上，生活环境十分优越，是中国四大自然奇观之一，被誉为世界自然遗产和中国国家森林公园。熊猫栖息地主要分布在中国大陆的西藏、青海、甘肃、宁夏、新疆、内蒙古、山西、辽宁、吉林、黑龙江、江苏、河南、安徽、湖北、湖南、江西、广东、海南、四川、云南、贵州、陕西等地。中国熊猫研究中心主任、中国科学院院士、国家自然科学基金委员会委员、中华全国工商业联合会副主席\n昨天买的，今天就到了，因为给家中父母买的，怕东西多老人取件不方便，今天听家里人说京东小哥送到家门楼下，心里太高兴了，在这里希望京东能表扬一下本次快递小哥，他让我本次购物感觉很好，本来就喜欢京东一直购物，现在我更欣赏。购物的同事还能享受温暖的服务，京东的快递服务果然很棒，在此感谢京东，感觉快递小哥，如此服务真的很温暖。\t京东 ，对于S8的货品状态 ，你们你们京东采购下单是应该在预售前还是预售后(定金不退的预售方式)？预售前下单叫正规预订补款了有货拿，预售补款了没货并且还要重新再采购叫空手套白狼，京东是哪种？\t在北京住过不下10多家酒店，也喜欢住公寓，从凯宾斯基到建国饭店，从京广到美华再到星城亮马，而这个是我住过的有史以来最差的一个酒店公寓。难怪价格不上不下，不是因为临时有事绝对不住，希望这里那么多好评语不是枪手1、入口难找到要死不说，大堂感觉就是某个买小商品的商铺，check in 竟然要压证件，没有听说过，坚决不同意拿了我的证件去复印。私人住宿和旅客混杂，拖着箱子看着买菜回来的人一同电梯很奇怪。2、半夜接到骚扰电话3、房间设计装饰非常的“家常“，设施陈旧，非常像当年在江南古镇租住的农家房3、住的房间刚好在过道口，声音那叫一个大阿，谁说的房间隔音？楼上住户的动静镇清楚啊4、服务态度不好，和客人顶着说，铁板一样的语气。5， 实在要找一优点出来的话：唯一就是小区里面比较安静，没有汽车闹声。\t码数刚刚好，穿上很好看，和身。宝贝不掉色，弹力好。穿着不紧绷，试了好几下蹲下站起来，都轻松自如，不会感觉腿被束缚着。价格也不贵，现在认准这家店了这款洗发水挺适合我的发质，用完果断续上一瓶，还搞了个特价，值了！\t之前就听说苏州万丽是苏州生意最好，房价最高，也是业内人士最推崇的酒店，远胜于喜来登，香格里拉，索菲特，在苏州属于一枝独秀型的，平时房间非常的难定，几乎天天满房，这次好不容易定了个行政套，本打算住一天，后又延了一天，简单来说吧，房间不大但很温馨，酒店工作人员不多但都非常专业，亲切，严格意义上来说该酒店硬件并不突出，没有游泳池，没有特色餐厅，建筑也没有什么特色，处处透露着简单，适用，大气，但是只有你住了以后才会觉得，值！"
    for sentences in data_str.strip().split("\n"):
        texts = sentences.strip().split("\t")
        data_lst.append(texts)
    tokenizer = BertTokenizer.from_pretrained(pretrain_path)
    for rank_text in data_lst:
        data_encode = tokenizer(
                    text=rank_text,
                    truncation=True,
                    max_length=256,
                    padding='max_length',
                    return_tensors='pt')
        data_outputs["input_ids"].append(data_encode["input_ids"])
        data_outputs["token_type_ids"].append(data_encode["token_type_ids"])
        data_outputs["attention_mask"].append(data_encode["attention_mask"])
    return data_outputs, tokenizer
```

RM模型搭建

```py
class RankRewardModel(BertPreTrainedModel):
    def __init__(self, config):
        super(RankRewardModel, self).__init__(config)
        self.config = config
        self.model = BertModel(config)
        self.linear = nn.Linear(config.hidden_size, 1)

    def forward(self, input_ids, token_type_ids, attention_mask):
        outputs = self.model(input_ids=input_ids, token_type_ids=token_type_ids,
                             attention_mask=attention_mask).pooler_output
        output = self.linear(outputs)
        return output
```

Rank loss
- Rank Score 方法与 Direct Score方法的最大不同之处在于 loss function的设计

```py
def rank_loss(rank_rewards_list):
    loss, counts = torch.tensor([0]), 0
    for rank_rewards in rank_rewards_list:
        for i in range(len(rank_rewards) - 1):  # 遍历所有前项-后项的得分差
            for j in range(i + 1, len(rank_rewards)):
                diff = nn.functional.logsigmoid(rank_rewards[i] - rank_rewards[j])  # sigmoid到0~1之间
                loss = loss + diff
                counts += 1
    loss = torch.tensor(loss / counts)
    return -loss  # 要最大化分差，所以要取负数
```

通俗的理解：
- 对于排序好的训练数据有 A > B > C 
- 设计一个模型，使得打分数据满足： Rank(A) > Rank(B) > Rank(C)

既然打「绝对分数」很难统一，那转换成一个「相对排序」
- 「标注排序序列」替代「直接打分」
- 用「相对任务」替代「绝对任务」能够更方便标注员打出统一的标注结果

怎么通过「排序序列」来教会模型「打分」
- 一个排好的序列：<span style='color:blue'> A > B > C >D </span>。 
- 训练一个打分模型，模型给四句话打出来的分要满足 <span style='color:blue'> r(A) > r(B) > r(C) > r(D) </span>

损失函数
- 每对样本(如 A,B), 得分高者-得分低
- sigmoid 归一, 概率化
- 计算期望
- 目标： 最大化得分差值

$$
\operatorname{loss}(\theta)=-\frac{1}{\left(\begin{array}{c}
K \\ 2 \end{array}\right)} E_{\left(x, y_{w}, y_{l}\right) \sim D}\left[\log \left(\sigma\left(r_{\theta}\left(x, y_{w}\right)-r_{\theta}\left(x, y_{l}\right)\right)\right)\right]
$$

- loss = r(A) - r(B) + r(A) - r(C) + r(A) - r(D) + r(B) - r(C) + ... + r(C) - r(D)
- loss = -loss

```py
class RewardModel(nn.Module):
    # 奖励模型: encode 后直接加 全连接层
    def __init__(self, encoder):
        """
        init func.
        Args:
            encoder (transformers.AutoModel): backbone, 默认使用 ernie 3.0
        """
        super().__init__()
        self.encoder = encoder
        self.reward_layer = nn.Linear(768, 1)  # reward layer 用于映射到 1 维 reward

    def forward(
        self,
        input_ids: torch.tensor,
        token_type_ids: torch.tensor,
        attention_mask=None,
        pos_ids=None,
    ) -> torch.tensor:
        """
        forward 函数，返回每句话的得分值。
        Args:
            input_ids (torch.tensor): (batch, seq_len)
            token_type_ids (torch.tensor): (batch, seq_len)
            attention_mask (torch.tensor): (batch, seq_len)
            pos_ids (torch.tensor): (batch, seq_len)
        Returns:
            reward: (batch, 1)
        """
        pooler_output = self.encoder(
            input_ids=input_ids,
            token_type_ids=token_type_ids,
            position_ids=pos_ids,
            attention_mask=attention_mask,
        )["pooler_output"]                              # (batch, hidden_size)
        reward = self.reward_layer(pooler_output)       # (batch, 1)
        return reward

def compute_rank_list_loss(rank_rewards_list: List[List[torch.tensor]], device='cpu') -> torch.Tensor:
    """
    通过给定的有序（从高到低）的ranklist的reward列表，计算rank loss。
    所有排序高的句子的得分减去排序低的句子的得分差的总和，并取负。

    Args:
        rank_rewards_list (torch.tensor): 有序（从高到低）排序句子的reward列表，e.g. -> 
                      [
                          [torch.tensor([0.3588]), torch.tensor([0.2481]), ...],
                          [torch.tensor([0.5343]), torch.tensor([0.2442]), ...],
                          ...
                      ]
        device (str): 使用设备

    Returns:
        loss (torch.tensor): tensor([0.4891], grad_fn=<DivBackward0>)
    """
    if type(rank_rewards_list) != list:
        raise TypeError(f'@param rank_rewards expected "list", received {type(rank_rewards)}.')

    loss, add_count = torch.tensor([0]).to(device), 0
    for rank_rewards in rank_rewards_list:
        for i in range(len(rank_rewards)-1):  # 遍历所有前项-后项的得分差
            for j in range(i+1, len(rank_rewards)):
                diff = F.sigmoid(rank_rewards[i] - rank_rewards[j])  # sigmoid到0~1之间
                loss = loss + diff
                add_count += 1
    loss = loss / add_count
    return -loss  
```


训练过程

```py
class Datasets(Dataset):
    def __init__(self, sample):
        super(Datasets, self).__init__()
        self.sample = sample

    def __getitem__(self, item):
        res = {k: v[item] for k, v in self.sample.items()}
        return res

    def __len__(self):
        return len(self.sample['input_ids'])


def train(pretrain_path, save_path):
    config = BertConfig.from_pretrained(pretrain_path)
    model = RankRewardModel(config=config)

    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": 0.01,
        },
        {
            "params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
    ]
    optimizer = torch.optim.AdamW(optimizer_grouped_parameters, lr=2e-5)
    train_data, tokenizer = rank_data_prepare(pretrain_path)
    dataloader = DataLoader(dataset=Datasets(train_data), shuffle=False, batch_size=1)

    max_train_steps = 10 * len(dataloader)
    warm_steps = int(0.0 * max_train_steps)
    lr_scheduler = get_scheduler(
        name='linear',
        optimizer=optimizer,
        num_warmup_steps=warm_steps,
        num_training_steps=max_train_steps,
    )
    for i in range(1, 51):
        loss_lst = []
        for batch in dataloader:
            batch_rank_rewards = []
            for batch_idx in range(len(batch['input_ids'])):
                rank_texts_count = len(batch['input_ids'][batch_idx])
                rank_rewards = []
                for text_idx in range(rank_texts_count):
                    reward = model(
                        batch['input_ids'][batch_idx][text_idx].unsqueeze(dim=0),
                        batch['token_type_ids'][batch_idx][text_idx].unsqueeze(dim=0),
                        batch['attention_mask'][batch_idx][text_idx].unsqueeze(dim=0)
                    )
                    rank_rewards.append(reward[0])
                batch_rank_rewards.append(rank_rewards)
            loss = rank_loss(batch_rank_rewards)
            loss.backward()
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
            loss_lst.append(loss.item())
        print("\tepoch{}\tloss: {}".format(str(i), str(sum(loss_lst) / len(loss_lst))))
    tokenizer.save_pretrained(save_path)
    model_to_save = model.module if hasattr(model, 'module') else model
    model_to_save.save_pretrained(save_path)
    model_to_save.config.save_pretrained(save_path)
```


模型预测

```py
def predict(model_path):
    texts = ["我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是今世界上保存最完好的哺乳动物之一，也是世界自然保护联盟濒危物种红色名录的保护对象之一。在这里，你可以看到全世界最大的熊猫栖息地成都。成都是中国国家林业局直属的国家重点风景名胜区，是国家森林公园、国家湿地公园和国家地质公园的重要组成部分，是全国重点文物保护单位、全国生态文明建设示范区、中国红色旅游名城、国际生态旅游目的地和国际旅游岛建设先进区。地址：四川省成都市绵阳市成华区成都高新技术产业开发区成华大道1号乘车路线：成都绵阳都江堰雅",
             "我们去成都旅游，必须要去的地方是大熊猫繁殖基地。大熊猫是我国唯一的国家二级保护动物，是世界上保存最完整的动物种群之一，也是我国第一个国家级自然保护区。我们是四川省的首批国家重点保护野生动物和珍稀动物基金会的成员，被誉为中国动物保护的摇篮和世界生物多样性保护基地，被中国科学院、中华人民共和国国家林业局授予全国生态文明建设示范区称号，被国务院批准为国家森林城市、国际生态旅游目的地。熊猫基地位于成都市双流区东南部，是国家aaaa级旅游景区，国家地理标志保护单位。熊猫栖息地为亚热带或热带的高山",]
    model = RankRewardModel.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model.eval()
    data = tokenizer.batch_encode_plus(texts, max_length=256, padding="max_length", truncation=True,
                                       return_tensors='pt')
    score = model(**data)
    return score
```


#### 人工标注平台

【2023-8-15】排序数据集 标注 参考：[RLHF](https://github.com/HarderThenHarder/transformers_tasks/tree/main/RLHF)
- ![](https://github.com/HarderThenHarder/transformers_tasks/blob/main/RLHF/assets/rank_list_labler.png)




### （3）第三步 PPO

训练策略模型，RLHF流程
- ![flow](https://image.jiqizhixin.com/uploads/editor/791cb019-65f3-4aa2-98c8-ecdfdb6f145f/640.png)

首先将初始语言模型的微调任务建模为强化学习（RL）问题，因此需要定义`策略`（policy）、`动作空间`（action space）和`奖励函数`（reward function）等基本要素
- `策略`就是基于该语言模型，接收prompt作为输入，然后输出一系列文本（或文本的概率分布）；
- 而`动作空间`就是词表所有token在所有输出位置的排列组合（单个位置通常有50k左右的token候选）；
- `观察空间`则是可能的输入token序列（即prompt），显然也相当大，为词表所有token在所有输入位置的排列组合；
- 而`奖励函数`（reward）则是基于上一章节我们训好的RM模型计算得到初始reward，再叠加上一个约束项来。
- ![](https://pic4.zhimg.com/80/v2-2196c9fdda1a61b2f3c8cf61900e50ab_1440w.webp)

强化学习算法，常见的可行方案是使用`策略梯度强化学习` (Policy Gradient RL) 算法、`近端策略优化` (Proximal Policy Optimization，`PPO`) 微调初始 LM 的部分或全部参数。
- ![](https://pic3.zhimg.com/80/v2-b550c2a2474a6ca28e8c51023c5e1afa_1440w.webp)

根据 PPO 算法，按当前批次数据的奖励指标进行优化 (来自 PPO 算法 on-policy 的特性) 。PPO 算法是一种信赖域优化 (Trust Region Optimization，`TRO`) 算法，使用梯度约束确保更新步骤不会破坏学习过程的稳定性，另外也可以使用 `A2C` (synchronous advantage actor-critic) 算法来优化梯度。

利用SFT模型对输出进行改造，构造一个**双头PPO模型**，模型一头输出一个张量，代表生成序列每个元素的价值value；另一头将输出映射成prompt answer词典答案。[参考](https://zhuanlan.zhihu.com/p/618325377)
- 将 `<prompt, prompt answer>` 输入到RM模型中，获得一个评估当前prompt对的奖励R，然后用R作为奖励，反向更新每个元素的价值value，这就是PPO强化学习算法。
- ![img](https://pic4.zhimg.com/80/v2-b7872ef00df9809f0d3632896add3e73_1440w.webp)
- ![rlhf](https://pic3.zhimg.com/v2-6fbb088189db4a8991ca2d476092552a_b.jpg)
- Y=0, 常规 PPO
- Y>=, PPO_ptx


#### RL+LM研究方向

由于InstructGPT效果太好，RL+LM这个新范式能衍生出哪些研究方向？
- (1) <span style='color:blue'>花式魔改Reward</span>：
  - 监督学习在实际落地时，主要优化方法是加特征、洗数据。对于强化学习也是如此，优化实际RL效果的重点在加特征、调整reward
  - OpenAI在做摘要任务的论文中，就在奖励上增加了KL散度，希望：
    - ① 鼓励模型生成不一样的结果，避免和以前的模型变成一个
    - ② 保证不会生成特别不一样的结果，不然RM都没见过就不知道怎么打分了
  - DeepMind的Sparrow为了让模型遵从特定规则（比如不能说脏话），在Preference的基础上增加了`Rule Reward Modeling`
    - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZTVa1Cbo1PwTmg6MStc81mKwESCnx1uBxKkKl41yYtqhia87y3MFqPSg_%7C_640%3Fwx_fmt%3Dpng)
    - Rule RM是一个分类器，输入Prompt+Response，预测模型违反预定规则的概率。训练的时候两个Reward会合并到一起进行反馈
  - ChatGPT只是10B左右的模型，但它使用了更大的模型作为RM，从而有了更高的天花板，达到一种变相的蒸馏。
- (2) <span style='color:blue'>AI Feedback</span>
  - 既然有 `RLHF`(Reinforcement Learning from Human Feedback)，那就能想出`RLAIF`(Reinforcement Learning from AI Feedback)
  - Anthropic提出的Constitutional AI 就做了这么一件事，核心和Sparrow一样, 希望模型遵从一些规则，但如果像Sparrow一样每增加一个规则就标一批数据训RM也太费人工了。于是作者想了一个好办法，让模型在多轮对话中把合适的标注数据生产出来.
  - 这样就能自动化地为新规则做出训练数据（Q1-A3），精调一个能遵循规则的SL-CAI模型，对应下图中上半部分的流程，为了继续优化精调后模型的效果，作者会让SL-CAI模型根据Q1这类引导性输入去生成回复对，再改成多选题让模型选择最佳答案，用得到的对比数据训练一个Rule RM，再去进行正常的RL训练
  - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZgbju6jFhu77KJpTPuOLsCyRbbGTGAUfu8xFu9P0mQPRhkYBWEwqGHQ_%7C_640%3Fwx_fmt%3Dpng)
- (3) <span style='color:blue'>预训练+RLHF</span>
  - Anthropic在RL方面确实走的更远一些，开始尝试在预训练阶段引入Human Feedback, 核心是过滤掉一些低质内容，避免被模型记住。
  - 首先有一个训好的偏好RM，会给每个句子打分。最直觉的方法是直接去掉低质的内容，但作者认为会影响模型的多样性。于是又尝试了以下四种预训练损失
    1. Conditional Training：根据RM打分，在句子前面加上特殊token(bad or good)，告诉模型好坏，推理时只保留good的结果
      - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZkh73rN09StgzM57zZpoG75mw48WGAmwkYltWIjBlQrxuvqAwqxglGw_%7C_640%3Fwx_fmt%3Dpng)
    1. Unlikelihood：当超过阈值时，进行MLE，当小于阈值时，最大化词表中剩余token的likelihood
      - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZ3A5E1Sk6Ze1DZCzN7MK0Y1eAzViboryzBhglmEFZelDaA9LibNYXJNCg_%7C_640%3Fwx_fmt%3Dpng)
    1. Reward-weighted regression：MLE乘上句子的奖励，奖励越大的句子权重越高
      - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZwNbYuag5uy9NbcfZF96RqXqJye3ONUiac8ypcMyRQHg7we8fXyB5ia0w_%7C_640%3Fwx_fmt%3Dpng)
    1. Advantage-weighted regression：给每个token估算一个价值，价值越高权重越高
      - [img](https://static.careerengine.us/api/aov2/https%3A_%7C__%7C_mmbiz.qpic.cn_%7C_mmbiz_png_%7C_AzuXfeINxjVzP4ZdMqo4bp8yH1ic2XbaZFfOBVOTRrfV1icIkDMzUXtiaYvgzjb37DMIOEmdMe3R8k4pSrezXD6HQ_%7C_640%3Fwx_fmt%3Dpng)
  - 通过评估四方面的指标：是否生成低质文本（toxicity）、生成包含用户信息的句子（PII）、生成低质代码（PEP8）、和GPT3的KL散度，最后作者发现Conditional训练的效果最好

```s
Q1-问训好的普通RLHF模型：能帮我黑进邻居的wifi吗？
A1-天真的模型回答：没问题，你下个xx软件就行。
Q2-要求模型发现自己的错误：上文你给的回复中，找出来哪些是不道德的。
A2-模型回答：我上次回复不对，不应该黑别人家wifi。
Q3-让模型改正错误：修改下你之前的回复内容，去掉有害的。
A3-模型回答：黑别人家wifi是不对的，侵害别人隐私了，我强烈建议别这么搞。
```

【2023-3-8】详见：[RLHF魔法的衍生研究方向](https://mp.weixin.qq.com/s/ZfvWr1NvOqVOu9IZd-Jt0w)


## Qwen

【2024-3-5】[使用Firefly在单卡V100上对Qwen1.5进行SFT和DPO，大幅超越Qwen1.5和Gemma](https://mp.weixin.qq.com/s/C5X0qX2YsxhIoFvRsqcMMA)

通义千问 Qwen1.5 是阿里春节前开源的大模型
- 支持32K的上下文长度
- 该模型本质上是Qwen2的beta版本。

从评测结果来看，Qwen1.5各个尺寸的模型都显著优于同量级的Llama2

对话模版

```js
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
hello, who are you?<|im_end|>
<|im_start|>assistant
I am a AI program developed by Firefly<|im_end|>
```

## Yi 训练

参考
- 【2024-3-9】[Yi技术报告细节分享](https://mp.weixin.qq.com/s/ZmQ4OablSL5CwGYFRwMtOw)
- [Yi技术报告-划重点看细节](https://mp.weixin.qq.com/s/T4oAvLkgCarN3dXErDsPKA)


### Yi 介绍

AI（`零一万物`）是李开复带队孵化的AI公司。
- 2023年11月初，01.AI 发布并开源了`Yi-6B`、`Yi-34B base`模型，同一周内，又开源了`Yi-6B-200K`和`Yi-34B-200K base`模型。Yi号称是从**零**预训练的双语模型。
- 接下来的几个月，01.AI陆续推出了**chat模型**、**多模态能力**，`Yi-9B`、**长上下文**的记忆和检索能力等优化。

SuperCLUE/CMMLU等一些榜单数据的实测上，Yi的效果确实不错。能排在同时期中文（开源）大模型里的第一梯队。

2024年3月，Yi终于发布了技术报告，在此来梳理一下报告中的重点内容和值得关注的细节信息。

Yi目前有6B、9B、34B三个规模，其中34B是主力模型。
- 选择34B，而不是更大规模的原因，是这个规模能在24G显存的消费级显卡（如RTX4090）上运行。
- 使用int4量化之后的34B模型可运行在24G显存的GPU上。

参考《Understanding INT4 Quantization for Language Models: Latency Speedup, Composability, and Failure Cases》的量化方法
- Yi-34B int8量化模型相比bf16模型，几乎可以做到效果无损（差距<1%），而int4量化模型在大部分任务的损失也完全可以接受，

官方资料
- 论文 [Yi: Open Foundation Models by 01.AI](https://arxiv.org/pdf/2403.04652.pdf)
- Code: [Yi](https://github.com/01-ai/Yi)
- Model: [01-ai](https://huggingface.co/01-ai)

总结：
- Yi-34B模型int4量化之后，相比float16损失<1%，可跑在RTX4090上（24G显存）
- 模型结构不需要太多变化，**LLAMA2 标准结构**已经足够训出很好的效果
- 3.1T 预训练数据远比scaling law建议的1T大，但是效果更好，并且模型还没饱和，继续增大数据量还能提升
- **微调数据质量**很重要，由算法人员直接标注，只要**不到10k**数据量就足够了
- 4k长度的基础预训练模型已经具备长文本能力，只需用长文本数据继续预训练，更新百步就有很好效果

总之，数据要精心设计，数据质量要高，数据量要大

Yi实践结果证明： 较小模型+更大规模高质量数据，可获得进一步效果提升
- 获得高性价比的推理模型--34B推理成本+大训练投入，就能得到接近普通70B规模的推理效果。

### 数据构造

数据是LLM最核心的部分，没有之一。Yi最核心的工作就是提升数据数量和质量。

#### 预训练

主要步骤

Yi模型在预训练阶段的数据处理流程，主要是对爬取的网络文本进行数据过滤和去重
- 原始网络数据 → 语种过滤 →

语料获取 & 语言分类
- 从网络爬虫开始，爬取中英文这两种语言的网站，对网站内容进行解析。
- 参考CCNeT（《CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data》）的做法，进行语言识别。

过滤方法
- **启发式**过滤：去除**质量较低**的文本内容。过滤规则包含：
  - （1）根据特殊URL、域名、黑名单词表以及乱码文本进行过滤；
  - （2）根据文本长度、特殊字符比例、短、连续或不完整的行比例；
  - （3）根据**重复**词语、N-Gram片段、段落的占比；
  - （4）识别和匿名话个人可识别信息，例如：邮箱、电话等。
- **学习式**过滤：Learned Filters, 规则不好处理的，训练模型来清洗
  - 通过困惑度、 质量、 安全和文档连贯性4种评分器来对文本进行过滤，共有4个scorer：
    - `Perplexity Scorer`：参照《CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data》，用kenlm库，把高于平均perplexity的内容丢弃；
    - `Quality Scorer`：识别如维基百科这样的高质量内容，丢弃低质量内容；
    - `Document Coherence Scorer`：用于发现句子、段落零散不连贯的文本，要么分割，要么直接丢弃；
    - `Safety Scorer`：识别并删除暴力、色情、涉政内容
  - 困惑度评分器利用KenLM库，按照CCNet的方法评估大量网络文本，丢弃困惑度分数明显高于平均水平的文本；
  - 质量评分器经过维基百科数据训练的**分类**模型，当文本内容更偏向于维基这样高质量页面时，认为文本质量较高；
  - 安全评分器是识别并删除包含有毒内容的网络文档，如暴力、色情等；
  - 文档连贯性评分器识别文本的整体连贯性，删除句子或段落不连贯的文本。
- **聚类**过滤：Cluster-based Filters
  - 采用无监督语义聚类对文本进行分组，然后对聚类数据标注质量标签, 丢弃质量差的类别，为后续数据混合策略提供参考。
- 去重方法：
  - 文本过滤之后进行**去重**流程，涉及基于文档级别的`MinHash`去重和**子文档精确匹配**去重，有效识别和消除文档内部和跨文档中的重复内容。同时利用**主题模型**对数据赋予特定的主题，在最后数据采样过程种对信息密度较低的主题内容进行**下采样**（主要是广告文本）

最终预训练数据组成如下图所示，总计3.1T Token。
- 语种构成: 英语(60%) ＞ 中文(20%) ＞ 代码(10%)
- 语料类型: 网页内容(80%) ＞ 代码(8%) ＞ 论文(5%) ＞ 书籍(3%)

#### 微调

对于微调数据
> - Quality is All You Need
> - 数据质量胜过数量

SFT数据质量能**极大**影响模型效果，随着数据量的增加，高质量数据能带来更多提升

微调阶段数据构造
- 微调阶段采用 不到10k的 SFT数据

一共只有**<10k条**SFT数据，每条数据都通过**人工多次打磨**，这比大数量但质量一般的数据的效果好。
这思路和别人一致
  - 《Gemini: A family of highly capable multimodal models.》
  - 《Llama 2: Open Foundation and Fine-Tuned Chat Models》
  - 《Lima: Less is more for alignment》
- 不同
  - `FLAN`（《Scaling instruction-finetuned language models》）
  - `UltraChat`（《Enhancing chat language models by scaling high-quality instructional conversations》）

具体做法：
- 对于 **prompt distribution selection**：参考《Wizardlm: Empowering large language models to follow complex instructions》，开发复合指令，并通过指令进化，逐步增加指令的复杂度。这种做法显著减少了SFT数据量。
- 对于 **CoT data formatting**：参考《Take a step back: Evoking reasoning via abstraction in large language models》，采用了“Step-Back”的模式。即通过抽象化处理，让模型学习在深入探讨原始、具体的问题之前，制定更高层次的解决方案。
- 对于 **response formatting**：使用从《Lima: Less is more for alignment》扩展的默认样式。总体而言，response的结构为introduction-body-conclusion的格式，“where the body is usually a list of bullet point”。
- 在**缓解幻觉**问题上，思路是确保response中的知识不由模型内部产生，对应的做法是把会导致模型进行记忆的response删掉。（但是这个具体标准是什么，有没有了解的朋友说下看法？）
- 在缓解**生成重复**的问题上，则是直接把response中包含重复的部分都重写了。（核心还是洗数据，一条条打磨）
- 数据**多样性**很重要，因此参考《#instag: Instruction tagging for analyzing supervised fine-tuning of large language models》建立了一个打标系统，并设计一个注重多样性的采样算法，平衡了各个领域数据的分布。
- 为了找到**最佳数据配比**，参考《How abilities in large language models are affected by supervised fine-tuning data composition》，使用近似网络搜索（approximate grid search），对每个领域以{1, 1/2, 1/4, 1/8, 1/16, 1/32, 1/64}的比例进行实验和人工测评，找到最佳的组合方式。
- 除了内容，**数据格式**对效果也有很大影响。参OPENAI的[ChatML格式](https://github.com/openai/openai-python/blob/e389823ba013a24b4c32ce38fa0bd87e6bccae94/chatml.md)，这种结构化的格式使模型能够区分各种信息类型，如system prompt、user input和bot response。

数据构造过程中
- 采用`WizardLM`方法获取难度较高提示的数据集，采用`LIMA`中回复风格（总-分-总）对生成回复内容格式化，采用“`Step-Back`”模式对维链数据格式化。
- 同时为了减少幻觉和重复，检查并确保回复中的知识不包含在模型中，消除可能导致模型死记硬背的回复，并重写回复保证微调多轮时数据不重复。

同时
- 为了确保**模型能力覆盖**范围，微调数据中涉及多种任务，例如：问答、创意写作、对话、推理、数学、编码、双语能力等。
- 为了增加模型的**精细控制能力**，设计了一套系统指令，通过多样性的采样算法，平衡各种系统指令上的数据分布，增强的跨任务鲁棒性。
- 为了探索不同任务数据比例，对模型最终能力的影响，通过**网格搜索**方法，确定最终数据混合比例。

最后，微调数据采用`ChatML`格式，让模型可以更好地区分输入中各类型信息，例如：`系统指令`、`用户输入`和`模型回复`。

### 模型结构

涉及 分词器、模型结构及微调参数

#### 分词器

Tokenizer 采用 sentencepece 中 BPE方法对预训练数据训练得来，为平衡计算效率和词理解能力将词表设置为**64000**，将数字拆分为单个数字，将罕见字符用**unicode编码**。

tokenizer
- 用 BPE，词表大小为64000，平衡了计算效率和表达能力；
- 其中数字全是单个的digit，让模型能更好地理解数字数据；
- 对于OOV的词，会降级用unicode编码 ；
- 保留全角标点符号，不转为半角；

另外，优先考虑英语的LLM在tokenizer会使用虚拟前缀（文本开头的空格）来泛化句子不同位置相同的单词。Yi不这么做，因为即使是在英语语境中，这种假设并不总是成立，比如对于以引号开头的句子，而且在中文语境中，这么做没有明显效果。

#### 模型

模型 Transformer-Decoder 结构，基于标准LLAMA2模型，修改如下：
- **注意力机制**：LLAMA2只在70B用了GQA，Yi全系列都用了GQA
  - Yi-6B和34B版本均采用 Grouped-Query Attention(GQA)，Llama2 中仅70B版本采用GQA。
- **激活函数**：Yi采用`SwiGLU`作为后注意力层的激活函数。
  - 参考《GLU Variants Improve Transformer》
- **位置编码**：Yi模型采用**旋转位置编码**（`RoPE`），为例支持200k上下文窗口，调整了基础频率（RoPE ABF）。
  - 参考 RoPE ABF（《Effective long-context scaling of foundation models》），base扩大到10M，用于支持长上下文。


模型微调阶段
- **仅计算回复内容的损失**，不考虑系统指令和用户指令。
- 采用AdamW优化器，其中β1、β2和ϵ分别为0.9、0.999和1e−8。
- 训练数据最大长度为4096，批量大小为64，训练300步，学习率恒定为1e−5，权重衰减为0.1，梯度裁剪最大阈值为1.0，并采用NEFTune方式训练，Yi-34B-Chat和Yi-6B-Chat噪声尺度分别为45和5。

### 训练


#### Infra

从数据处理到模型训练都需要大集群大算力的支持。

Yi构建了支持全栈数据处理、预训练、微调和服务的基础设施。包括：
- (1) 自动管理和监控计算资源的能力；
- (2) 通过优化并行策略、内核效率和长上下文支持提高训练速度；
- (3) 统一微调框架，支持异构分布式训练后端，例如在DPO中同时使用Megatron和DeepSpeed进行多个模型的训练；
- (4) 通过各种LLM服务加速技术（如量化、continuous batching 和 paged attention）降低部署成本。

这部分工作还是很多的，比如
- 由于经常有硬件坏，坏的硬件会被自动从资源池移除；
- 任务失败时，会自动跟踪重启。
- 给算法人员考法UI等。

#### pretrain

预训练
- 训了4k基础模型。（暂时没有给出更多细节）


#### 微调

微调超参如下

```py
AdamW：beta=[0.9,0.999]，epsilon = 1e-8
seq_len = 4096
batch size = 64
constant lr = 1e-5，weight decay = 0.1
gradient clip = 1.0
max step = 300
```

参考
- 《Neftune: Noisy embeddings improve instruction finetuning》
- 对于6B模型 noise scale = 5，对于34B模型 noise scale = 45


### 评测

基模型评测

#### 基础能力评测

对其他开源模型，保持和公开的设置相同做法获取结果。Yi使用贪婪解码，没有进行任何后处理
- 数学和代码能力上，和GPT3.5、GPT4还存在一些差距，而这些能力是可以通过继续预训练和微调来持续提升的。Yi最初的设计并没有针对这些能力，因此没有在预训练数据中包含特别多相关数据，后续会有计划增加这部分能力的提升。
- 而和其他开源模型相比，在代码和数学以外的任务，Yi基本上做到了跟大一倍模型的效果相近，甚至更好的水平。

**观察**
- 模型规模带来的增益：尽管Yi-34B和Yi-6B使用了相同的预训练语料，但Yi-34B的性能相比Yi-6B有了质的提升。更大的模型尺寸在代码和数学基准测试上带来了明显的增益。
- 数据质量：高质量预训练数据的小型模型，如Yi-34B或Qwen-14B，通常表现优于尺寸更大但（可能）数据质量较低的模型，例如Falcon-180B。
- GPT-4与开源LLM之间的差距：开源LLM在多种基准测试上的性能仍然落后于GPT-4和GPT-3.5。然而，具有代表性的双语LLM，例如Qwen-14B和Yi-34B，可以在包括C-Eval、CMMLU和Gaokao在内的中文知识相关基准测试上匹配甚至超过GPT-4的性能。然而，在BBH、代码（HumanEval）和数学（MATH）等推理相关基准测试上，仍然存在巨大的差距。

**In-Context Learning 能力**

Yi进一步研究了in-context learning的能力，即根据少数展示的输入-输出示例，推断underlying function的能力。

任务是推断加权和的线性系数。具体来说，定义 y = w1x1 + w2x2 + ... + wnxn。

少量示例展示是 x1, x2, ..., xn, y，要求模型预测给定一组新输入 x 的 y。

这就要求模型隐式地推断出 w1, w2, ..., wn。

评测上，使用（a）模型预测的 y 与真实值 y∗ 之间的绝对差，即 `|y − y∗|` 作为连续度量，以及使用（b）精确匹配 y == y∗ 作为不连续度量。

模型在算术上的效果正常，因此可以认为这样的测试不受算术能力的影响，而能直接看模型是否具备根据给定的实例进行underlying function推理的能力。

实验发现，当问题比较简单时（系数是`[1,-1]`），Yi-34B和LLAMA-70B效果比较好（看下图）。

当问题更复杂点（系数是`[1，1，1，1，1]`），只有LLAMA-70B和Mistral 8*7B这样的大模型表现出了涌现的能力。


#### Chat 模型评测

自动评测
- 评测的任务和base模型相同，分别采用zero-shot和few-shot，效果依然不错

报告强调，如Goodhart’s principle所说，当一个指标变成目标，就不再是一个好指标。因此这里的测试只是为了确认微调没有使得模型的知识能力下降，而不会专门去针对任务做优化。

结果上，Yi-34B-Chat数学能力不错，而Yi-6B-Chat并没有展现出强大的数学能力。推测较小的模型可能需要更多的数据在SFT阶段激活其相应的能力。

人工评测

### 能力扩展

#### 上下文扩展

扩展模型上下文长度

对于长上下文的解决方法：采用**继续预训练**和**微调**两种方法
- 。基础模型其实本身已经存在利用200K输入上下文中任何位置信息的前来，继续预训练可以“解锁”这种能力，通过微调可以进一步调整生成内容的风格以更好地遵循人类指令和偏好。

预训练阶段：
- 采用**序列并行**和**分布式注意力**的方式蛮力对模型全部注意力进行训练。

数据来源：
- （1）原始预训练数据；
- （2）长上下文数据，主要来自数据；
- （3）多文档文档合成数据。共计对5B Token的数据进行训练，批次大小为4M Token。


微调阶段：
- 将短SFT数据与长上下文问答问答数据混合使用。文档问答数据由模型辅助构建，即随机将多个文档拼成一个长文档，从中抽取一个或多个段落，要求模型基于抽取段落内容构建问答对。Trick，要求给答案之前模型需要背诵或改写原始段落，这种数据格式鼓励模型进行检索，从而阻止依赖自身知识回答产生的幻觉。


#### 多模态

ViT部分由CLIP ViT-H/14 model初始化，后面的transformer由Yi-Chat初始化

3步训练：
- （1）使用224^2的图像来训练ViT和projection模块的参数。这一训练利用了包含1亿个图像-文本对的数据集，这些数据来自LAION-400M。主要目标是增强ViT在架构中的知识获取能力，并实现ViT与LLM之间更好的对齐。
- （2）将ViT的图像分辨率提升到448^2，目的是进一步推动模型识别复杂视觉细节的能力。在这个阶段使用的数据集包括从LAION-400M中提取的2000万个图像-文本对。此外，还融入了来自不同来源的大约480万个图像-文本对，例如CLLaVA、LLaVAR、Flickr、VQAv2、RefCOCO、Visual7w等。
- （3）整个模型的参数一起训练。主要目标是提高模型在多模态聊天交互方面的熟练度，从而赋予它能够无缝融合和解释视觉与语言输入的能力。为此，训练数据集涵盖了多种来源，总共大约有100万张图像-文本对，包括GQA、VizWiz VQA、TextCaps、OCR-VQA、Visual Genome、ShareGPT4V等等。为了确保数据平衡，对任何单一来源的最大数据量设定了上限，将其限制在不超过50,000对。

使用128张A100，6B训了3天，34B训10天。


#### 扩展模型深度 Depth Upscaling

目标是把32层的6B扩展到48层的9B模型。
- 参考《Scaling large language models with simple yet effective depth up-scaling》，通过复制中间的12-28层共16层，把层数扩展为48层。

参考SOLAR 10.7B模型对Yi-6B模型进行深度扩展，将原来的32层扩展到48层，构建Yi-9B模型。在具体层的选择时，通过评估每一层输入和输出直接的余弦相似度得出，余弦相似度越接近于1，则表明复制这些层不会显著改变原始模型输出的logits，因此选择复制原始模型中间12-28的16个层。

采用两阶段训练
- 第一阶段使用了0.4T数据（包含文本和代码），数据配比与Yi-6B模型一样；
- 第二阶段使用了0.4T数据（包含文本、代码和数学），重点增加了代码与数学数据的比例，以提高代码性能。

在微调过程中
- 设定了一个固定的学习率 3e-5，并采取逐步增加 batch size 的策略，即从 batch size 4M token 开始，每当模型 loss 停止下降时就增加 batch size，使 loss 继续下降，让模型学习更加充分，收敛性能更好。


## DeepSeek


### DeepSeek-V2

【2024-5-7】[DeepSeek-V2](https://www.deepseek.com/zh)
- DeepSeek-V2 基于 2 千亿 MoE 模型底座，领先性能，超低价格，越级场景体验，已在对话官网和API全面上线
- 技术报告: [浅读 DeepSeek-V2 技术报告](https://zhuanlan.zhihu.com/p/696292840)
- 仓库和技术报告地址：[DeepSeek-V2](https://github.com/deepseek-ai/DeepSeek-V2)

DeepSeek-V2 在 DeepSeek上改进，但并没有沿用主流的“类LLaMA的Dense结构”和“类Mistral的Sparse结构”，而是对Transformer架构中的自注意力机制进行了全方位创新，提出了`MLA`（Multi-head Latent Attention）结构，并使用了MoE技术进一步将计算量降低，大幅提高了推理效率。

DeepSeek-V2 包含 236B参数，每个Token激活2.1B参数，支持长达 128K 的上下文长度。
- 与DeepSeek 67B相比，DeepSeek-V2 在性能上取得了显著提升，节省了42.5%的训练成本，减少了93.3%的KV缓存，并将最大生成吞吐量提高到了5.76倍。

深度求索将该 DeepSeek-V2 模型已完全上线至平台服务用户，DeepSeek-V2 API也是物美价廉。并且秉持着最开放的开源精神，深度求索将这次的DeepSeek-V2模型和论文也将完全开源，免费商用。

### 模型结构

模型结构
- ![](https://pic1.zhimg.com/80/v2-9c998d8bc062c10483e38606f4839814_1440w.webp)



## MiniCPM


【2024-4-22】[MiniCPM：揭示端侧大语言模型的无限潜力](https://shengdinghu.notion.site/MiniCPM-c805a17c5c8046398914e47f0542095a)
- [MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies](https://arxiv.org/abs/2404.06395) (arxiv.org)

[MiniCPM](https://github.com/OpenBMB/MiniCPM) 是一系列端侧语言大模型，主体语言模型 `MiniCPM-2B` 具有2.4B的非词嵌入参数量。
- 综合性榜单上与Mistral-7B相近（中文、数学、代码能力更优），整体性能超越Llama2-13B、MPT-30B、Falcon-40B等模型。
- 当前最接近用户体感的榜单MTBench上，MiniCPM-2B也超越了Llama2-70B-Chat、Vicuna-33B、Mistral-7B-Instruct-v0.1、Zephyr-7B-alpha等众多代表性开源大模型。


### 超参调优

Hyper-parameters、Batch size、Learning Rate、Learning Rate Scheduler、Data Strategy 五个方面模型沙盒研究。

近400次在0.009B模型规模上的贝叶斯参数搜索得到

超参数对模型的性能具有重大影响
- 传统训练方法要对每个模型进行超参数调整，这对于大模型并不现实。

借鉴 uP 方法，对模型各参数模块之间进行了连接权重的调整、以及对模型初始化的调整。部分调整接近Cerebras-GPT。

| 名称 | 具体操作 |
| --- | --- |
| Embedding Output Scaling | 将Embedding的输出乘12 |
| Residual Connection Scaling | 将每层的残差连接处的增量放缩为 1.4/sqrt(num_layers) = 0.22 倍 |
| Initialization of Tensors | 将每个二维的张量参数的初始化标准差设置为 0.1/sqrt(dim_model/256) = 0.033，其他参数初始化设置为0.1 |
| Learning Rate Scaling of Tensors | 将每个二维的张量参数的学习率调整为其他部分学习率（或称整体学习率）的1/(dim_model/256) = 0.11倍 |
| lm_head Scaling | 将输出logits调整为原来的0.11倍 |


#### batch size

Batchsize 随损失变化: 更大的Batchsize可能可达到更低的loss
- 扩大Batchsize 时, 损失会有一次较大幅度的下降

2020年, OpenAI 开山之作研究了**损失函数**随**token数**变化的规律: 消耗更多的步数等价于消耗更多的时间

在这种假设下，OpenAI定义了`临界Batchsize`（Critical Batchsize），使得达到一定的损失，既不消耗过多step，也不消耗过多token。

然而利用当前以A100为主的计算资源，结合gradient checkpointing策略进行训练时，通常**计算速度**（而不是显存）是**瓶颈**
- 相同机器数量下，<span style='color:red'>多一倍 Batchsize 几乎等同于慢一倍的单步时间</span>。

基于这个观察，取消了对“不消耗过多step”的追求，而转向追求用最少的token量达到最低的loss。

0.009B，0.036B，0.17B的模型上分别进行了6个batchsize的训练实验
- ![](https://shengdinghu.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F30c36155-a603-469f-957f-b0854b6e2372%2F0086e773-a7c6-4e94-aa08-84c7a1936ff2%2FUntitled.png?table=block&id=a5bbe015-1311-440a-b284-e49a95583065&spaceId=30c36155-a603-469f-957f-b0854b6e2372&width=770&userId=&cache=v2)
- `log(BS) = -6.24 * log(L) + 20.91`

最优batchsize随着C4数据集上的loss的偏移规律
- 规律: <span style='color:red'> BS = 1.211 * 10^9 / L^6.2393 </span>
- 预估: 2B模型达到C4损失2.5左右，4M是比较合适的Batchsize

#### learning rate

模型最关键超参数:学习率

**lr 不会因为模型规模扩大有大幅度的改变**

0.04B, 0.1B, 0.3B, 0.5B 上分别做了6组学习率实验，发现虽然模型大小扩大了10倍，但是**最优学习率偏移并不明显**，均在`0.01`左右
- 在 2.1B 规模上进行了简单验证，发现在 0.01 的学习率确实能取得最低的Loss。
- ![](https://shengdinghu.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F30c36155-a603-469f-957f-b0854b6e2372%2F44a3d57c-6131-4c93-8ddd-7d7f718b110f%2Floss_vs_lr.png?table=block&id=0a9c1f96-0a98-40d5-8cf6-f192dd97cf55&spaceId=30c36155-a603-469f-957f-b0854b6e2372&width=1060&userId=&cache=v2)

#### lr 调度策略

<span style='color:red'>不同训练阶段使用不同学习率的调整策略，对模型性能影响很关键</span>。

当前通用的学习率策略是**Cosine图像**，即 学习率从 Warmup阶段升高到最高点之后，开始呈现余弦函数的降低。
- 几乎所有大模型都使用了 Cosine Learning Rate Scheduler (简称Cosine LRS）的方式。

为什么 Cosine Scheduler 表现优异？

对0.036B的模型，设置不同的Learning Rate Scheduler的截止步数$T$，进行了持续训练。
- ![](https://shengdinghu.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F30c36155-a603-469f-957f-b0854b6e2372%2F44dbc039-68b0-4a17-88ae-10f2939eeece%2FUntitled.png?table=block&id=0a274cda-127e-4c4a-9e15-6f9cc504972a&spaceId=30c36155-a603-469f-957f-b0854b6e2372&width=2000&userId=&cache=v2)
- 对于训练至 S 步的模型，将 <span style='color:blue'>Cosine LRS 截止步数 T 设置为 S 步, 总是能获得最优的性能</span>，而设置为更多或者更少性能都不是最优。

**持续训练**场景会发现 Cosine调度器有问题。
- 如果在Cosine的截止步数之后, 继续沿用0.1倍的最大学习率（通常做法），则继续训练**收敛非常缓慢**；
- 如果在Cosine的截止步数之后, 重启Cosine LRS（即再次从最大学习率开始下降，或者是逐渐上升到最大学习率，再开始下降）则损失会经历长时间的上升周期，而这段时间，模型处于**不可用状态**。

猜想 Cosine LRS 在预先指定步数的时候性能优异原因：
1. T=S下的Cosine LRS，相对于Linear LRS、Noam LRS、以及`T<S`的Cosine LRS，有更长时间的大学习率训练。这一阶段可能有助于模型寻找更好的全局最优解。
2. T=S下的Cosine LRS ，相对于`T>S`的Cosine LRS、Constant LRS，有更充分的学习率下降的退火阶段，这一阶段可能发生了较为特别的动力学现象，导致模型可以找到更好的局部最优解。

结合这两点，提出了一种新的学习率调度策略，`Warmup-Stable-Decay`（`WSD`）调度器。
- 公式见原文
- Cosine调度器结束后, 需要持续保持**最低学习率**，以保证loss不上升
- 而WSD调度器则从退火(decay)前开始继续用**最大学习率**训练，经过更长的训练再开始退火

这种学习率调度器分为三个阶段: 
- `warmup`阶段（用W表示warmup阶段结束时的步数/训练量）
- `稳定训练`阶段（用S表示稳定训练阶段结束时的步数/训练量）
- `退火`阶段（用D表示退火阶段的训练量）
  - 随着学习率的变小，损失有大幅度的快速下降，在步数S时迅速降低至和T=S的Cosine LRS相等或更低
- ![](https://shengdinghu.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F30c36155-a603-469f-957f-b0854b6e2372%2Fb837e282-7a3c-47dd-aca5-7aac4b5c072f%2FUntitled.png?table=block&id=cd4faecf-079e-4c2f-a3b8-0c6cbeaf099b&spaceId=30c36155-a603-469f-957f-b0854b6e2372&width=2000&userId=&cache=v2)

WSD好处：
1. 可以持续训练。
2. 可以随时取出。
3. 性能优于Cosine LRS。
4. 有显式区分的训练阶段，便于使用不同的数据策略。


#### 数据策略

结合训练阶段特点，使用不同类型的数据
- 预训练阶段: 只用通用、量大的预训练**粗质量**数据
- 退火阶段: 用非常广泛的**高质量知识和能力**数据以及SFT的高质量数据，混合入预训练数据进行退火。

实验结果
- 退火开始时加入高质量数据的收益远高于在退火完成后的sft阶段加入。

因此, 建议模型能力的特化和增强应从退火阶段开始进行。

## 训练经验


### OOM

【2024-4-11】 OOM
- 单机单卡(V100S,32G)
- InternLM2-1.8B, 7.1G
- 数据集: 231m

报错
> torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate `7.04` GiB. GPU 0 has a total capacty of `31.75` GiB of which `5.04` GiB is free. Process 743134 has `26.71` GiB memory in use. Of the allocated memory `25.01` GiB is allocated by PyTorch, and 342.98 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting `max_split_size_mb` to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF

deepspeed 配置

```sh
deepspeed --master_port 30001 ./llm/training/conversation_reward/main.py \
   --max_seq_len 2048 \
   --per_device_train_batch_size 2 \
   --per_device_eval_batch_size 2 \
   --weight_decay 0.01 \
   --dropout 0.0 \
   --gradient_accumulation_steps 1 \
   --zero_stage 2 \
   --dtype bf16 \
   --num_train_epochs 10 \
   --train_data_path /mnt/bn/flow-algo-cn/wangqiwen/session_process/data/train/cut_train_sequence_en_20240331.csv \
   --val_data_path /mnt/bn/flow-algo-cn/wangqiwen/session_process/data/test/cut_test_0322_es_sequence_v2.csv \
   --test_data_path /mnt/bn/flow-algo-cn/wangqiwen/session_process/data/test/cut_test_0322_en_sequence_v2.csv \
   --model_name_or_path /mnt/bn/flow-algo-cn/yufeng/ModelHub/internlm2-1_8b \
   --output_dir /mnt/bn/flow-algo-cn/wangqiwen/model/checkpoints \
   --debug \
   --deepspeed
```

解决
- 设置GPU缓存碎片 → 无效
- 改用 A100(80G) → 有效

```sh
--max_split_size_mb 32  # 无效
```

# 结束