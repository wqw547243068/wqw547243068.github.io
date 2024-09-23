---
layout: post
title:   大模型应用技术方案 LLM Solution
date:   2023-10-23 16:52:00
categories: 大模型
tags: 微调 RAG lora prompt 陈丹琦 知识图谱 moe 翁丽莲
excerpt: 大模型工业落地的技术经验总结
mathjax: true
permalink: /llm_solution
---

* content
{:toc}

# LLM 应用实践

开箱即用的预训练LLM没有按预期或希望执行时，如何提高LLM应用的性能？
- 用检索增强生成（RAG）还是模型微调来改善结果？


## GPT 使用方法

OpenAI 的接口名就叫「completion」，也证明了其只会「生成」的本质。

![](https://pic4.zhimg.com/v2-c2f3cef1b909ea593eb56e9987c958a7_b.webp)

### 技术架构总结

【2023-11-23】[参考](https://zhuanlan.zhihu.com/p/667826259?utm_psn=1711026527125225472)

|类型|说明|图解|
|---|---|---|
|纯prompt|一问一答| <img src="hhttps://pic1.zhimg.com/80/v2-f4e4ebe618195d48e9f2b264bdadedec_1440w.webp" height="100%" width="100" />|
|Agent + Function Calling|Agent：AI 主动提要求<br>Function Calling：AI 要求执行某个函数<br>场景举例：你问过年去哪玩，ta 先反问你有几天假|<img src="https://pic2.zhimg.com/80/v2-7f79119cec8a74043bbe0c9a1af40d7d_1440w.webp" height="100%" width="100" />|
|Embeddings + 向量数据库|Embeddings：把文字转换为更易于相似度计算的编码。这种编码叫向量<br>向量数据库：把向量存起来，方便查找<br>向量搜索：根据输入向量，找到最相似的向量<br>场景举例：考试时，看到一道题，到书上找相关内容，再结合题目组成答案。然后，就都忘了|<img src="https://pic2.zhimg.com/80/v2-db7f589f134ca9fb8d08f80f1539f095_1440w.webp" height="100%" width="100" />|
|Fine-tuning|模型微调|<img src="https://pic2.zhimg.com/80/v2-29f966de529981aa7e221960afedb971_1440w.webp" height="100%" width="100" />|



## 如何选择优化方法


建议
- 微调之前先尝试RAG

## 方法分析

[Full Fine-Tuning, PEFT, Prompt Engineering, and RAG: Which One Is Right for You?](https://deci.ai/blog/fine-tuning-peft-prompt-engineering-and-rag-which-one-is-right-for-you)


|方法|说明|分析|图解|
|---|---|---|
|`PE`|提示工程|提示工程不用训练网络权重|![](https://deci.ai/wp-content/uploads/2023/09/3-4.png.webp)|
|`PEFT`|参数高效微调|- PEFT 相比全面微调的优势<br>更高效和更快的训练<br>保留预训练的知识|![](https://deci.ai/wp-content/uploads/2023/09/4-6.png.webp)|
|`RAG`|检索增强生成|优点：成本低，最小化幻觉，易于扩展<br>缺点：<br>不在文档中的问题无法解决<br>窗口受限|![](https://deci.ai/wp-content/uploads/2023/09/2-5.png.webp)|
|`Full FineTune`|全参数微调|- 优点: 训练数据集更少、提高精度、增加鲁棒性<br>缺点: 高计算成本、内存需求高、时间/专业知识密集|![](https://deci.ai/wp-content/uploads/2023/09/1-3.png.webp)|


### 图解

【2024-5-15】分析对比几种主流范式的区别

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-05-16T03:21:21.956Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36\&quot; etag=\&quot;m63tNrzUkycuD1VYzYui\&quot; version=\&quot;24.4.0\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;第 1 页\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;2248\&quot; dy=\&quot;-408\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-8\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1094.43\&quot; y=\&quot;1408\&quot; width=\&quot;211.14\&quot; height=\&quot;160\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-94\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;414\&quot; y=\&quot;1428.5\&quot; width=\&quot;239.28\&quot; height=\&quot;531.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-59\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;194.11\&quot; y=\&quot;1660\&quot; width=\&quot;152.14\&quot; height=\&quot;269\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;KTwht3HF3Dpf_-XckZrt-1\&quot; value=\&quot;大模型应用范式对比\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=21;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;570\&quot; y=\&quot;1210\&quot; width=\&quot;224.5\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;7DkoaQAKY2b415vYvJvz-1\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;760\&quot; y=\&quot;1428.5\&quot; width=\&quot;172.14\&quot; height=\&quot;131\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;7DkoaQAKY2b415vYvJvz-2\&quot; value=\&quot;提示语&amp;amp;nbsp;&amp;amp;nbsp;&amp;lt;span style=&amp;quot;background-color: initial;&amp;quot;&amp;gt;Prompt&amp;lt;/span&amp;gt;\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;fontStyle=0;fontColor=#7F00FF;fontSize=15;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;910\&quot; y=\&quot;1570\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;7DkoaQAKY2b415vYvJvz-3\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=-0.034;exitY=0.467;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;U2g8cO25Ie6dlqNpXrYe-2\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-67\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;589\&quot; y=\&quot;1524\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;697\&quot; y=\&quot;1374\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-16\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-1\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-60\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-1\&quot; value=\&quot;\&quot; style=\&quot;shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-2.75\&quot; y=\&quot;1454\&quot; width=\&quot;82.5\&quot; height=\&quot;80\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-41\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-3\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-43\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-3\&quot; value=\&quot;\&quot; style=\&quot;strokeWidth=2;html=1;shape=mxgraph.flowchart.multi-document;whiteSpace=wrap;fillColor=#97D077;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;8.5\&quot; y=\&quot;1858\&quot; width=\&quot;80\&quot; height=\&quot;64\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-63\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;dashed=1;dashPattern=1 2;strokeColor=#CC0000;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-4\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-48\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-70\&quot; value=\&quot;局部参数\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-63\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.3562\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;fillColor=#bac8d3;strokeColor=#23445d;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430.25\&quot; y=\&quot;1444\&quot; width=\&quot;180\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-5\&quot; value=\&quot;\&quot; style=\&quot;html=1;shape=mxgraph.er.anchor;whiteSpace=wrap;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-4\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;89.99999999999999\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-6\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#d6b656;fillColor=#fff2cc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-4\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;92.24228363929795\&quot; y=\&quot;4.038461538461538\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-7\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#d6b656;fillColor=#fff2cc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-4\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;6.745151708131615\&quot; y=\&quot;4.038461538461538\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-8\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#d6b656;fillColor=#fff2cc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-4\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;92.24228363929794\&quot; y=\&quot;50.96153846153847\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-9\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#d6b656;fillColor=#fff2cc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-4\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;6.745151708131648\&quot; y=\&quot;50.96153846153847\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-10\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;&amp;quot;&amp;gt;Pre-trained LLM&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380\&quot; y=\&quot;1411.5\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;7DkoaQAKY2b415vYvJvz-5\&quot; value=\&quot;Task Description\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;768.71\&quot; y=\&quot;1441.5\&quot; width=\&quot;152.43\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;7DkoaQAKY2b415vYvJvz-6\&quot; value=\&quot;Example (Optional)\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;768.71\&quot; y=\&quot;1519.5\&quot; width=\&quot;152.43\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;7DkoaQAKY2b415vYvJvz-7\&quot; value=\&quot;Query\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e3c800;strokeColor=#B09500;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;768.71\&quot; y=\&quot;1481.5\&quot; width=\&quot;152.43\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-12\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;&amp;quot;&amp;gt;User&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1075\&quot; y=\&quot;1650\&quot; width=\&quot;50\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-17\&quot; value=\&quot;（1）提示工程&amp;amp;nbsp;&amp;lt;div style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: initial; font-size: 15px;&amp;quot;&amp;gt;Basic Prompt Engineering&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;rotation=0;strokeWidth=3;fontColor=#6666FF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490.00000000000006\&quot; y=\&quot;1395.5\&quot; width=\&quot;250\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-18\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;&amp;quot;&amp;gt;Massive Datasets&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=#FFFFFF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-30\&quot; y=\&quot;1544\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-22\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-60\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-59\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;520\&quot; y=\&quot;1570\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;270\&quot; y=\&quot;1640\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-24\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;433\&quot; y=\&quot;1840\&quot; width=\&quot;180\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-25\&quot; value=\&quot;\&quot; style=\&quot;html=1;shape=mxgraph.er.anchor;whiteSpace=wrap;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-24\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;89.99999999999999\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-26\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#b85450;fillColor=#f8cecc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-24\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;92.24228363929795\&quot; y=\&quot;4.038461538461538\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-27\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#b85450;fillColor=#f8cecc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-24\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;6.745151708131615\&quot; y=\&quot;4.038461538461538\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-28\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#b85450;fillColor=#f8cecc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-24\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;92.24228363929794\&quot; y=\&quot;50.96153846153847\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-29\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#b85450;fillColor=#f8cecc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-24\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;6.745151708131648\&quot; y=\&quot;50.96153846153847\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-30\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;&amp;quot;&amp;gt;Fine-tuned LLM&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;550\&quot; y=\&quot;1617\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-36\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.999;entryY=0.431;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryPerimeter=0;edgeStyle=orthogonalEdgeStyle;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-67\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-24\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;732.5\&quot; y=\&quot;1858.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;914.5\&quot; y=\&quot;1873\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-39\&quot; value=\&quot;（4）全参微调&amp;amp;nbsp;&amp;lt;div style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;Full Fine Tuning&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;rotation=0;strokeWidth=3;fontColor=#6666FF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;190.08999999999997\&quot; y=\&quot;1825\&quot; width=\&quot;160.18\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-42\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;&amp;quot;&amp;gt;Domain Specific Datasets&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=#FFFFFF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-40\&quot; y=\&quot;1929\&quot; width=\&quot;210\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-43\&quot; value=\&quot;全参微调&amp;amp;nbsp;&amp;lt;div&amp;gt;Full FineTune&amp;amp;nbsp;&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=#BD7000;fontColor=#000000;strokeWidth=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;210.18\&quot; y=\&quot;1870\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-45\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-43\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-24\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;441\&quot; y=\&quot;1917\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;391\&quot; y=\&quot;1902\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-46\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-47\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-56\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-47\&quot; value=\&quot;\&quot; style=\&quot;strokeWidth=2;html=1;shape=mxgraph.flowchart.multi-document;whiteSpace=wrap;fillColor=#97D077;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;8.5\&quot; y=\&quot;1668\&quot; width=\&quot;80\&quot; height=\&quot;64\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-48\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; y=\&quot;1650\&quot; width=\&quot;180\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-49\&quot; value=\&quot;\&quot; style=\&quot;html=1;shape=mxgraph.er.anchor;whiteSpace=wrap;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-48\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;89.99999999999999\&quot; height=\&quot;100\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-50\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#b85450;fillColor=#f8cecc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-48\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;92.24228363929795\&quot; y=\&quot;4.038461538461538\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-51\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#d6b656;fillColor=#fff2cc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-48\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;6.745151708131615\&quot; y=\&quot;4.038461538461538\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-52\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#d6b656;fillColor=#fff2cc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-48\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;92.24228363929794\&quot; y=\&quot;50.96153846153847\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-53\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;absoluteArcSize=1;html=1;arcSize=10;whiteSpace=wrap;points=[];strokeColor=#d6b656;fillColor=#fff2cc;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-48\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;6.745151708131648\&quot; y=\&quot;50.96153846153847\&quot; width=\&quot;81.0038240917782\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-55\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;&amp;quot;&amp;gt;Domain Specific Datasets&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=#FFFFFF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-40\&quot; y=\&quot;1739\&quot; width=\&quot;210\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-56\&quot; value=\&quot;参数高效微调&amp;lt;div&amp;gt;PEFT&amp;amp;nbsp;&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=#BD7000;fontColor=#000000;strokeWidth=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;210.18\&quot; y=\&quot;1680\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-57\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-56\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-48\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;341\&quot; y=\&quot;1747\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;291\&quot; y=\&quot;1732\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-60\&quot; value=\&quot;&amp;lt;div&amp;gt;预训练&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;Pre-training&amp;amp;nbsp;&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#76608a;strokeColor=#432D57;fontColor=#ffffff;strokeWidth=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;210.18\&quot; y=\&quot;1474\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-62\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-60\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;90\&quot; y=\&quot;1504\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;210\&quot; y=\&quot;1504\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-65\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-67\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-48\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;760\&quot; y=\&quot;1693\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;620\&quot; y=\&quot;1693\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;770\&quot; y=\&quot;1700\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-66\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; parent=\&quot;1\&quot; source=\&quot;7DkoaQAKY2b415vYvJvz-1\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;770\&quot; y=\&quot;1703\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;630\&quot; y=\&quot;1703\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-67\&quot; value=\&quot;Query\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e3c800;strokeColor=#B09500;shadow=1;fontSize=17;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;769.87\&quot; y=\&quot;1685\&quot; width=\&quot;152.43\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-68\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-67\&quot; target=\&quot;7DkoaQAKY2b415vYvJvz-1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;780\&quot; y=\&quot;1693\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;620\&quot; y=\&quot;1693\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-69\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;&amp;quot;&amp;gt;Fine-tuned LLM&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;550\&quot; y=\&quot;1810\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-72\&quot; value=\&quot;（3）高效参数微调&amp;amp;nbsp;&amp;lt;div style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;PEFT&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;rotation=0;strokeWidth=3;fontColor=#6666FF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;176.25\&quot; y=\&quot;1725\&quot; width=\&quot;170\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-78\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=default;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;760.01\&quot; y=\&quot;1283\&quot; width=\&quot;172.14\&quot; height=\&quot;110\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-79\&quot; value=\&quot;Related Docs\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;768.72\&quot; y=\&quot;1296\&quot; width=\&quot;152.43\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-80\&quot; value=\&quot;Prompt\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;shadow=1;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;768.72\&quot; y=\&quot;1336\&quot; width=\&quot;152.43\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-81\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; parent=\&quot;1\&quot; source=\&quot;7DkoaQAKY2b415vYvJvz-1\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-78\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;856\&quot; y=\&quot;1678\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;856\&quot; y=\&quot;1570\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-82\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#BD7000;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;fillColor=#f0a30a;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-78\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-4\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;770\&quot; y=\&quot;1504\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;620\&quot; y=\&quot;1504\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-83\&quot; value=\&quot;（2）检索增强生成&amp;amp;nbsp;&amp;lt;span style=&amp;quot;background-color: initial; font-size: 15px;&amp;quot;&amp;gt;RAG&amp;lt;/span&amp;gt;&amp;lt;div style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: initial; font-size: 15px;&amp;quot;&amp;gt;Retrieval Augmented Generation&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;rotation=0;strokeWidth=3;fontColor=#6666FF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; y=\&quot;1294.5\&quot; width=\&quot;320\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-91\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-84\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-90\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-84\&quot; value=\&quot;语义检索&amp;amp;nbsp;&amp;lt;div&amp;gt;Retrieval&amp;lt;/div&amp;gt;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=#BD7000;fontColor=#000000;strokeWidth=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1000\&quot; y=\&quot;1318\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-85\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#BD7000;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;fillColor=#f0a30a;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-84\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-78\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;856\&quot; y=\&quot;1439\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;856\&quot; y=\&quot;1403\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-86\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#BD7000;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;fillColor=#f0a30a;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-67\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-84\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;856\&quot; y=\&quot;1678\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;856\&quot; y=\&quot;1570\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;846\&quot; y=\&quot;1610\&quot; /&gt;\n              &lt;mxPoint x=\&quot;1060\&quot; y=\&quot;1610\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-87\&quot; value=\&quot;\&quot; style=\&quot;strokeWidth=2;html=1;shape=mxgraph.flowchart.multi-document;whiteSpace=wrap;fillColor=#97D077;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1180\&quot; y=\&quot;1231\&quot; width=\&quot;80\&quot; height=\&quot;64\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-88\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-size: 17px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(251, 251, 251); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;&amp;quot;&amp;gt;Knowledge Base&amp;lt;/span&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=#FFFFFF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1150\&quot; y=\&quot;1294.5\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-89\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;exitPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-87\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-90\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;1010\&quot; y=\&quot;1348\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;942\&quot; y=\&quot;1348\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-90\&quot; value=\&quot;语义检索模型\&quot; style=\&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1000\&quot; y=\&quot;1243\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-92\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.967;entryY=-0.01;entryDx=0;entryDy=0;dashed=1;dashPattern=1 2;strokeColor=#CC0000;entryPerimeter=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-48\&quot; target=\&quot;9EIczKXhWcwRTtTBnoEl-25\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;630\&quot; y=\&quot;1790\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;530\&quot; y=\&quot;1660\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-93\&quot; value=\&quot;全部参数\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-92\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;0.3562\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-95\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0.55;entryY=0.978;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; source=\&quot;9EIczKXhWcwRTtTBnoEl-94\&quot; target=\&quot;U2g8cO25Ie6dlqNpXrYe-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;856\&quot; y=\&quot;1725\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;623\&quot; y=\&quot;1893\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;9EIczKXhWcwRTtTBnoEl-96\&quot; value=\&quot;Reponse\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=13;\&quot; parent=\&quot;9EIczKXhWcwRTtTBnoEl-95\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.2571\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint y=\&quot;-9\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-10\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;startArrow=classic;startFill=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;U2g8cO25Ie6dlqNpXrYe-1\&quot; target=\&quot;U2g8cO25Ie6dlqNpXrYe-3\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-1\&quot; value=\&quot;\&quot; style=\&quot;verticalLabelPosition=bottom;aspect=fixed;html=1;shape=mxgraph.salesforce.bots;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1120\&quot; y=\&quot;1428.5\&quot; width=\&quot;60\&quot; height=\&quot;57\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-2\&quot; value=\&quot;\&quot; style=\&quot;verticalLabelPosition=bottom;aspect=fixed;html=1;shape=mxgraph.salesforce.personalization;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1070\&quot; y=\&quot;1680\&quot; width=\&quot;60\&quot; height=\&quot;45\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-3\&quot; value=\&quot;\&quot; style=\&quot;verticalLabelPosition=bottom;aspect=fixed;html=1;shape=mxgraph.salesforce.bots;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1211\&quot; y=\&quot;1428.5\&quot; width=\&quot;60\&quot; height=\&quot;57\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-6\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.55;entryY=1.029;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;U2g8cO25Ie6dlqNpXrYe-4\&quot; target=\&quot;U2g8cO25Ie6dlqNpXrYe-1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-7\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;U2g8cO25Ie6dlqNpXrYe-4\&quot; target=\&quot;U2g8cO25Ie6dlqNpXrYe-3\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-4\&quot; value=\&quot;\&quot; style=\&quot;verticalLabelPosition=bottom;aspect=fixed;html=1;shape=mxgraph.salesforce.bots;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1170\&quot; y=\&quot;1519.5\&quot; width=\&quot;60\&quot; height=\&quot;57\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-11\&quot; value=\&quot;（5）智能体模式&amp;amp;nbsp;&amp;lt;div style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;Agent&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;rotation=0;strokeWidth=3;fontColor=#6666FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1110.82\&quot; y=\&quot;1370\&quot; width=\&quot;160.18\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-12\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=0.988;exitY=0.454;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;7DkoaQAKY2b415vYvJvz-1\&quot; target=\&quot;U2g8cO25Ie6dlqNpXrYe-8\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;770\&quot; y=\&quot;1504\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;620\&quot; y=\&quot;1504\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-13\&quot; value=\&quot;Reflection\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=14;gradientColor=#b3b3b3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1280\&quot; y=\&quot;1422.25\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-14\&quot; value=\&quot;Tool Use\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=14;gradientColor=#b3b3b3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1280\&quot; y=\&quot;1459.75\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-15\&quot; value=\&quot;Planning\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=14;gradientColor=#b3b3b3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1280\&quot; y=\&quot;1496.75\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;U2g8cO25Ie6dlqNpXrYe-16\&quot; value=\&quot;Multiagent Collaboration\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;shadow=1;fontSize=14;gradientColor=#b3b3b3;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1280\&quot; y=\&quot;1535.75\&quot; width=\&quot;160\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



### 综述


[OpenAI：最大化LLM性能的技术综述](https://zhuanlan.zhihu.com/p/667439436?utm_psn=1709306396712189953)

<iframe src="//player.bilibili.com/player.html?aid=365929392&bvid=BV1p94y1G7yH&cid=1331597093&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  width='800' height='600'> </iframe>


如何选择？

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-05-16T03:34:39.278Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36\&quot; etag=\&quot;zs3XnZh57LH-gaOZF7ty\&quot; version=\&quot;24.4.2\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;YUrH7kkdw6S7EPocWAtV\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1421\&quot; dy=\&quot;761\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1nzIP9oYbUBeoa8APZYR-2\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;680\&quot; y=\&quot;212.5\&quot; width=\&quot;110\&quot; height=\&quot;75\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-2\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;110\&quot; y=\&quot;375\&quot; width=\&quot;130\&quot; height=\&quot;95\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-3\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;414\&quot; y=\&quot;195\&quot; width=\&quot;170\&quot; height=\&quot;110\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;JPcd8CNpdyUwO0oxOTY8-26\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;110\&quot; y=\&quot;195\&quot; width=\&quot;170\&quot; height=\&quot;110\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CRyWcW9bKPYmjVe2kgWn-2\&quot; value=\&quot;LLM优化之路\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=0;fontSize=22;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;324\&quot; y=\&quot;110\&quot; width=\&quot;150\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;lHimWeaf7UQe36nZpLsc-30\&quot; value=\&quot;wqw547243068@163.com&amp;lt;br&amp;gt;2023-12-31\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;489\&quot; y=\&quot;565\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-10\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=1;entryDx=0;entryDy=0;strokeWidth=3;strokeColor=#66B2FF;\&quot; parent=\&quot;1\&quot; source=\&quot;JPcd8CNpdyUwO0oxOTY8-9\&quot; target=\&quot;nseSPB6Go69togGukG2C-9\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;JPcd8CNpdyUwO0oxOTY8-9\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;Prompt&amp;lt;br&amp;gt;&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;110\&quot; y=\&quot;445\&quot; width=\&quot;70\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;s2pv88CfUx30G5g510ko-1\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;startArrow=none;startFill=0;entryX=0.98;entryY=-0.067;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; parent=\&quot;1\&quot; target=\&quot;nseSPB6Go69togGukG2C-1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;70\&quot; y=\&quot;520\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;860\&quot; y=\&quot;520\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;s2pv88CfUx30G5g510ko-2\&quot; value=\&quot;LLM优化\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontColor=#999999;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;545\&quot; y=\&quot;490\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;s2pv88CfUx30G5g510ko-3\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#999999;startArrow=none;startFill=0;\&quot; parent=\&quot;1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;70\&quot; y=\&quot;520\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;70\&quot; y=\&quot;140\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;s2pv88CfUx30G5g510ko-5\&quot; value=\&quot;Context优化\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontColor=#999999;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;64.75\&quot; y=\&quot;150\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;s2pv88CfUx30G5g510ko-11\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;简单检索&amp;lt;br&amp;gt;&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;154.75\&quot; y=\&quot;265\&quot; width=\&quot;80.5\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;s2pv88CfUx30G5g510ko-26\&quot; value=\&quot;模型需要知道的信息\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;63\&quot; y=\&quot;165\&quot; width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-1\&quot; value=\&quot;模型行为控制\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;530\&quot; y=\&quot;520\&quot; width=\&quot;100\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;414\&quot; y=\&quot;332\&quot; width=\&quot;170\&quot; height=\&quot;110\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-7\&quot; value=\&quot;PE提示工程\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontColor=#999999;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;110\&quot; y=\&quot;375\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-17\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#66B2FF;exitX=0.5;exitY=0;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;nseSPB6Go69togGukG2C-9\&quot; target=\&quot;s2pv88CfUx30G5g510ko-11\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-9\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;Few-shot&amp;lt;br&amp;gt;&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;160\&quot; y=\&quot;405\&quot; width=\&quot;70\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-11\&quot; value=\&quot;简单尝试\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;193\&quot; y=\&quot;442\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-12\&quot; value=\&quot;评估\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;210.5\&quot; y=\&quot;419\&quot; width=\&quot;50\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-13\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;HyDE检索+事实核查&amp;lt;br&amp;gt;&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;145.25\&quot; y=\&quot;220\&quot; width=\&quot;115.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-14\&quot; value=\&quot;FineTune 微调\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontColor=#999999;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;414\&quot; y=\&quot;332\&quot; width=\&quot;100\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-15\&quot; value=\&quot;综合\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontColor=#999999;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;424\&quot; y=\&quot;195\&quot; width=\&quot;50\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-16\&quot; value=\&quot;RAG检索增强生成\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontColor=#999999;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;110\&quot; y=\&quot;190\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-18\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.75;exitDx=0;exitDy=0;strokeWidth=3;strokeColor=#66B2FF;\&quot; parent=\&quot;1\&quot; source=\&quot;s2pv88CfUx30G5g510ko-11\&quot; target=\&quot;nseSPB6Go69togGukG2C-23\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;242\&quot; y=\&quot;415\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;364\&quot; y=\&quot;427\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-20\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;strokeWidth=3;strokeColor=#66B2FF;\&quot; parent=\&quot;1\&quot; source=\&quot;nseSPB6Go69togGukG2C-23\&quot; target=\&quot;nseSPB6Go69togGukG2C-13\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;364\&quot; y=\&quot;427\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;374\&quot; y=\&quot;300\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-21\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;RAFT&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;454\&quot; y=\&quot;220\&quot; width=\&quot;96\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-22\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;strokeWidth=3;strokeColor=#66B2FF;\&quot; parent=\&quot;1\&quot; source=\&quot;nseSPB6Go69togGukG2C-13\&quot; target=\&quot;nseSPB6Go69togGukG2C-21\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;374\&quot; y=\&quot;280\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;245\&quot; y=\&quot;245\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-23\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;微调模型&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;440\&quot; y=\&quot;362\&quot; width=\&quot;96\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-24\&quot; value=\&quot;指令遵循，以特定风格结构回复&amp;lt;br&amp;gt;适合：加强基础模型中已有知识+修改定制输出格式+节省token&amp;lt;br&amp;gt;不适合：添加新知识+快速迭代\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#999900;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;399\&quot; y=\&quot;389\&quot; width=\&quot;350\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-25\&quot; value=\&quot;开始：指令清晰+任务拆解+思维力+系统测试&amp;lt;br&amp;gt;扩展：提供参考信息+使用工具&amp;lt;br&amp;gt;不适合：引入新信息+复杂风格稳定复制+token节省\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#999900;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;100\&quot; y=\&quot;465\&quot; width=\&quot;290\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-26\&quot; value=\&quot;开卷考试/短期记忆\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontColor=#FF0000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;210.5\&quot; y=\&quot;190\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-27\&quot; value=\&quot;闭卷考试/长期记忆\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontColor=#FF0000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;495\&quot; y=\&quot;332\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;nseSPB6Go69togGukG2C-28\&quot; value=\&quot;作用：引入新信息+减少幻觉&amp;lt;br&amp;gt;不适合：开放域知识(医疗/法律)+学习特定风格结构\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#999900;labelBackgroundColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;80\&quot; y=\&quot;305\&quot; width=\&quot;290\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;1nzIP9oYbUBeoa8APZYR-1\&quot; value=\&quot;&amp;lt;font color=&amp;quot;#0000ff&amp;quot;&amp;gt;Agent&amp;lt;br&amp;gt;&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;700\&quot; y=\&quot;220\&quot; width=\&quot;70\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;1nzIP9oYbUBeoa8APZYR-3\&quot; value=\&quot;复合问题\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;700\&quot; y=\&quot;185\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;1nzIP9oYbUBeoa8APZYR-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#66B2FF;exitX=0.39;exitY=0.033;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;exitPerimeter=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;nseSPB6Go69togGukG2C-12\&quot; target=\&quot;1nzIP9oYbUBeoa8APZYR-2\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;205\&quot; y=\&quot;415\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;745\&quot; y=\&quot;290\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;290\&quot; y=\&quot;420\&quot; /&gt;\n              &lt;mxPoint x=\&quot;290\&quot; y=\&quot;470\&quot; /&gt;\n              &lt;mxPoint x=\&quot;735\&quot; y=\&quot;470\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;1nzIP9oYbUBeoa8APZYR-5\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;strokeWidth=3;strokeColor=#66B2FF;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;nseSPB6Go69togGukG2C-3\&quot; target=\&quot;1nzIP9oYbUBeoa8APZYR-2\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;271\&quot; y=\&quot;245\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;464\&quot; y=\&quot;245\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;1nzIP9oYbUBeoa8APZYR-6\&quot; value=\&quot;解决复合问题，具备一定思考能力&amp;lt;br&amp;gt;适合：复杂任务, 离散/孤立→连续/环境&amp;lt;br&amp;gt;不适合：简单/性能要求高\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#999900;labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;610\&quot; y=\&quot;125\&quot; width=\&quot;230\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



### 四种方法对比

【2023-10-17】[如何选择最适合你的LLM优化方法：全面微调、PEFT、提示工程和RAG对比分析](https://zhuanlan.zhihu.com/p/661830285?utm_psn=1697685536221999105)
- [RAG vs Finetuning — Which Is the Best Tool to Boost Your LLM Application?](https://towardsdatascience.com/rag-vs-finetuning-which-is-the-best-tool-to-boost-your-llm-application-94654b1eaba7)
- 【2023-12-4】英文原文：[Full Fine-Tuning, PEFT, Prompt Engineering, and RAG: Which One Is Right for You?](https://deci.ai/blog/fine-tuning-peft-prompt-engineering-and-rag-which-one-is-right-for-you/)

四种主要的调优方法：
- **全面微调**：使用任务特定数据调整LLM的所有参数。
  - 一个较小、任务特定、带标签的数据集上进行微调，调整一些模型参数，优化其对特定任务或一组任务的性能
  - 全面微调： 所有模型参数都被更新，使其类似于预训练，只不过是在一个**带标签**且**规模较小**的数据集上进行。
  - ![](https://pic2.zhimg.com/80/v2-e8c7286930eb81b57aaf109fe92ac58d_1440w.webp)
  - 优点: 训练数据集更少、提高精度、增加鲁棒性
  - 缺点: 高计算成本、内存需求高、时间/专业知识密集
- **参数高效精细调整**（PEFT）：修改选定参数以实现更高效的适应。进一步调整预训练模型，只更新其总参数的一小部分
  - PEFT 方法可训练的部分不同。一些技术优先训练原始模型参数的**选定部分**。其他方法集成并训练较小的**附加组件**，如适配器层，而不修改原始结构
  - ![](https://pic2.zhimg.com/80/v2-1d62f9b57373a592407db8aedd90b681_1440w.webp)
  - LoRA是最常用的 PEFT 方法，使用重参数化，这种技术通过执行低秩近似来缩小可训练参数的集合。
  - LoRA优点：
    - 任务切换效率 - 创建模型的不同版本以适应特定任务变得更容易。你可以简单地存储预训练权重的单个副本，并构建许多小 LoRA 模块。当你从任务切换到任务时，你只替换矩阵 A 和 B，并保留 LLM。这显著减少了存储需求。
    - 需要更少的 GPU - LoRA 将 GPU 内存需求减少了最多 3 倍，因为我们不计算/重新训练大多数参数。
    - 高精度 - 在各种评估基准上，LoRA 的性能被证明几乎等同于全面微调 - 而且只需要一部分成本
  - PEFT 相比全面微调的优势
    - 更高效和更快的训练
    - 保留预训练的知识
- **提示工程**：改进模型输入以指导其输出。
  - 在新数据集和任务上训练模型参数，使用所有预训练权重（如全面微调）或一组独立权重（如 LoRA）。
  - 相比之下，提示工程根本不涉及训练网络权重
  - ![](https://pic3.zhimg.com/80/v2-4e5ddc95da8e4945cf30c65e1593050e_1440w.webp)
  - 基础提示: 零样本提示、少样本提示、链式思考引导
  - ![](https://pic4.zhimg.com/80/v2-857d925cf7adc11d94a2fbd9aca37213_1440w.webp)
- **RAG**（检索增强生成）：将提示工程与数据库查询结合，以获得丰富的上下文答案。
  - 将引导工程与从外部数据源检索上下文相结合，以提高语言模型的性能和相关性。通过在模型上附加额外信息，它允许更准确和上下文感知的响应。
  - RAG模型架构将用户查询的嵌入与知识库向量中的embedding进行比较，将来自知识库中相似文档的相关上下文附加到原始用户提示中。然后将这个增强的prompt给到LLMs，可以异步更新知识库及其相关的embedding
  - ![](https://pic3.zhimg.com/80/v2-db7c5fbf5f95c69846fc3805eb287086_1440w.webp)
  - RAG 本质上将信息检索机制与文本生成模型相结合。信息检索组件有助于从数据库中拉取相关的上下文信息，并且文本生成模型使用这个添加的上下文来产生更准确和“知识丰富”的响应。以下是它的工作方式：
    - 向量数据库：实施 RAG 包括嵌入内部数据集，从中创建向量，并将它们存储在向量数据库中。
    - 用户查询：RAG 从提示中获取用户查询，这是一个需要回答或完成的自然语言问题或陈述。
    - 检索组件：一旦接收到用户查询，检索组件扫描向量数据库以识别与查询语义相似的信息块。然后使用这些相关片段为 LLM 提供额外上下文，使其能够生成更准确和上下文感知的响应。
    - 串联：将检索到的文档与原始查询串联成一个提供生成响应所需额外上下文的提示。
    - 文本生成：将包含串联查询和检索文档的提示馈送到 LLM 以产生最终输出。
    - ![](https://pic1.zhimg.com/80/v2-63c902a479d54ff27917dd94d3c65174_1440w.webp)
    - 开源应用框架: 
      - OpenAI [chatgpt-retrieval-plugin](https://github.com/openai/chatgpt-retrieval-plugin)
      - [langchain](https://github.com/langchain-ai/langchain)
      - [LlamaIndex](https://gpt-index.readthedocs.io/en/latest/index.html)
  - [Creating a RAG Pipeline with LangChainPermalink](https://www.maartengrootendorst.com/blog/improving-llms/#creating-a-rag-pipeline-with-langchain), [中文版](https://zhuanlan.zhihu.com/p/661349721?utm_psn=1697558407270424576)
  - ![RAG方法的大致过程](https://www.maartengrootendorst.com/assets/images/posts/2023-12-09-improving-llms/rag.svg)
  - RAG 有许多明显的优点：
    - 最小化幻觉 - 当模型做出“最佳猜测”假设，本质上填补了它“不知道”的内容时，输出可能是错误的或纯粹的胡说八道。与简单的提示工程相比，RAG 产生的结果更准确，幻觉的机会更低。
    - 易于适应新数据 - RAG 可以在事实可能随时间演变的情况下进行适应，使其对生成需要最新信息的响应非常有用。
    - 可解释 - 使用 RAG，可以确定 LLM 答案的来源。对答案来源进行追溯对于内部监控、质量保证或处理客户纠纷可能是有益的。
    - 成本有效 - 与在特定任务数据集上对整个模型进行微调相比，你可以使用 RAG 获得相当的结果，这涉及到更少的标记数据和计算资源。
  - RAG 的潜在限制
    - RAG 旨在通过从外部文档中提取上下文来增强 LLM 的信息检索能力。然而，在某些使用案例中，额外的上下文还不够。如果一个预训练的 LLM 在总结财务数据或从患者的医疗文档中提取见解方面遇到困难，很难看出以单个文档形式提供额外上下文如何有所帮助。在这种情况下，微调更有可能产生期望的输出。

[improving-llms](https://www.maartengrootendorst.com/blog/improving-llms/), 3 of the most common methods for improving the performance of any LLM:
- Prompt Engineering
- Retrieval Augmented Generation (RAG)
- Parameter Efficient Fine-Tuning (PEFT)
- ![](https://www.maartengrootendorst.com/assets/images/posts/2023-12-09-improving-llms/common.svg)
- ![](https://www.maartengrootendorst.com/assets/images/posts/2023-12-09-improving-llms/overview.svg)

四个重要指标上进行比较：复杂性、成本、准确性和灵活性。
- **成本**： PE ＜ RAG ＜ PEFT ＜ Full Fine-tuning
- **复杂性**：PE ＜ RAG ＜ PEFT = Full Fine-tuning
- **准确性**：
  - 特定领域术语：PE ＜ RAG ＜ PEFT ＜ Full Fine-tuning
  - 时效性：PEFT = Full Fine-tuning < PE < RAG
  - 可解释性：PE = PEFT = Full Fine-tuning < RAG
  - 幻觉: PE < PEFT < Full Fine-tuning < RAG
    - 微调可以通过将 LLM 集中在特定领域数据上来减少这些幻觉。然而，不熟悉的查询仍然可能导致 LLM 编造出一个捏造出来的答案。
    - RAG 通过将 LLM 的响应锚定在检索到的文档中来减少幻觉。初始检索步骤本质上进行事实检查，而随后生成受限于检索数据的上下文。对于避免幻觉至关重要的任务，推荐使用 RAG。
  - 总结
    - 解释性、时效性和避免幻觉至关重要 → RAG
    - 要求特定领域风格 → 全面微调 和 PEFT
    - 两者都要 → 微调 和 RAG
- **灵活性**： Full Fine-tuning < PEFT < PE < RAG


### PE vs finetune

【2023-11-30】Prompt Engineering 完胜 Fine-tuning：通用(且强大)的LLM通过prompt即可超越精调的LLM
- 微软研究，通过**优化**提示词，让GPT-4在**医学领域**完胜Med-PaLM 2（用医学数据精调的LLM）
- 通用且强大的LLM，能胜任各个领域的任务，比普通但在指定领域精调的LLM更强
- 【2023-11-18】论文： [Can Generalist Foundation Models Outcompete Special-Purpose Tuning? Case Study in Medicine](https://arxiv.org/pdf/2311.16452.pdf)

【2023-9-27】[RAG 与 Finetuning，谁是提升 LLM 的最佳工具？](https://mp.weixin.qq.com/s/D-8r3FHKCyh4xk-yM7lMag)


### RAG vs finetune

RAG最直接的优势:
- 让大模型利用自身逻辑推导能力，去理解企业私有数据，实现问答能力的拓展。

但是如果给大模型喂企业**私有数据**做模型微调，也能实现同样的效果，为什么还要用RAG呢? 看场景：
- 第一：私有数据存在一定频率**动态更新**；
- 第二：要**引用原文**；
- 第三：硬件资源（GPU）不足（即使用RAG也需要微调，但一次微调处处可用，远比每个企业私有库微调一个模型成本低的多）；

这些场景下，用RAG更合适一些。

作者：[瀚海方舟](https://www.zhihu.com/question/625481187/answer/3279041129)

分析
- 微调在特定任务上训练模型，就像在问题解答数据集上微调 GPT-3.5 以提高其在特定数据集上的问题解答性能一样。

判断
- 如果数据集**足够大**而且**不会变**，那么采用**微调**。
- 如果数据集动态变化，需要不断重新训练模型，以跟上变化。
- 如果没有大型数据集，不建议微调。建议用 RAG 来提高 LLM 的性能。同样，也可用 RAG 来提高 LLM 在摘要、翻译等任务上的性能，因为这些任务可能无法进行微调。

这两种方法都获得类似结果，但在复杂性、成本和质量方面有所不同。
- ![](https://pic1.zhimg.com/80/v2-c2058b77b95bdb3fb533b7949a6258b8_1440w.webp)

RAG更简单、便宜，但质量可能不匹配。

但这两种方案不是实现相同结果的两个方案，而是正交，满足LLM应用的不同需求。

RAG 和 微调之间的细微差别跨越了模型架构、数据需求、计算复杂性等。忽略这些细节可能会破坏项目时间轴和预算。

如何选择？
- **访问外部数据源**？是 → RAG 更有效、容易扩展
  - 非常适合需要查询数据库、文档或其他结构化/非结构化数据存储库的应用
  - 微调需要大量标注数据集，数据更新时，模型更新不及时
  - 微调过程没有对查询外部知识的检索和推理步骤进行建模。
- **修改模型行为、风格、领域知识**？是 → 微调
  - 微调擅长将LLM行为适配到特定细微差别、语调或术语，如 医学专业人士、以诗意的风格写作，或者使用特定行业的行话
  - RAG虽然善于整合外部知识，但主要侧重信息检索，不会根据检索信息调整其语言风格或领域特异性
- 抑制幻觉重要吗？是 → RAG
  - RAG 相对 微调 不容易产生幻觉，检索机制相当于事实检查器
- 监督语料多吗？是 → 微调，否则 RAG
  - 微调依赖有标签数据的数量和质量，数据不足会过拟合
- 数据会变化吗？是 → RAG
  - 如果数据经常更新，模型容易过时，而重新训练耗时耗力，增加评估成本
  - RAG 检索机制不断查询外部资源，保持最新，知识库/数据源更新时，RAG无缝集成，保持相关性，不用频繁训练
- 要求可解释吗？如果要求较高的透明性+可解释性 → RAG
  - LLM 原理像黑盒，推理机制不明，难以解释为什么
  - RAG 透明性相对较高，检索+生成，用户可以洞察全过程

|维度|解释|`RAG`|`FineTune`|
|---|---|---|
|External knowledge read?|访问外部数据?|✅|❌|
|Changing model behaviour read?|改变模型行为?|❌|✅|
|Minimise hallucinations?|幻觉最小化?|✅|❌|
|Training data availiable?|较多训练数据?|❌|✅|
|Is data (mostly) dynamic?|数据动态变化?|✅|❌|
|Interpretability|要求可解释?|✅|❌|


建议：
- 从RAG开始，评估其性能，如果发现不足，则转向微调。
- 最佳选择: 自动化，混合方法
  - 微调确保聊天机器人符合公司的品牌、语调和一般知识，处理大多数典型的客户查询。
  - RAG可以作为一个补充系统，处理更动态或更具体的查询，确保聊天机器人能够从最新的公司文档或数据库中获取信息，从而最大限度地减少幻觉。
  - 整合这两种方法，公司可以提供全面、及时且与品牌一致的客户支持体验。
- ![](https://pic1.zhimg.com/80/v2-8a98c6db80f32f2fea6fa2503360fd38_1440w.webp)



## （1）PE 提示工程

**提示工程**：改进模型输入以指导其输出。
- 在新数据集和任务上训练模型参数，使用所有预训练权重（如全面微调）或一组独立权重（如 LoRA）。
- 相比之下，提示工程根本不涉及训练网络权重
- ![](https://pic3.zhimg.com/80/v2-4e5ddc95da8e4945cf30c65e1593050e_1440w.webp)
- 基础提示: 零样本提示、少样本提示、链式思考引导
- ![](https://pic4.zhimg.com/80/v2-857d925cf7adc11d94a2fbd9aca37213_1440w.webp)


## （2）RAG 检索增强生成


详见站内专题: [检索增强生成](rag)


## （3）PEFT 参数高效微调

**参数高效精细调整**（PEFT）：修改选定参数以实现更高效的适应。进一步调整预训练模型，只更新其总参数的一小部分
- PEFT 方法可训练的部分不同。一些技术优先训练原始模型参数的**选定部分**。其他方法集成并训练较小的**附加组件**，如适配器层，而不修改原始结构
- ![](https://pic2.zhimg.com/80/v2-1d62f9b57373a592407db8aedd90b681_1440w.webp)
- LoRA是最常用的 PEFT 方法，使用重参数化，这种技术通过执行低秩近似来缩小可训练参数的集合。
- LoRA优点：
  - 任务切换效率 - 创建模型的不同版本以适应特定任务变得更容易。你可以简单地存储预训练权重的单个副本，并构建许多小 LoRA 模块。当你从任务切换到任务时，你只替换矩阵 A 和 B，并保留 LLM。这显著减少了存储需求。
  - 需要更少的 GPU - LoRA 将 GPU 内存需求减少了最多 3 倍，因为我们不计算/重新训练大多数参数。
  - 高精度 - 在各种评估基准上，LoRA 的性能被证明几乎等同于全面微调 - 而且只需要一部分成本
- PEFT 相比全面微调的优势
  - 更高效和更快的训练
  - 保留预训练的知识

【2024-2-27】PEFT: 
- LORA、QLoRA
- Adapter Tuning
- Prefix Tuning、Prompt Tuning、P-Tuning 及 P-Tuning v2 等

7个主流微调方法在Transformer网络架构的作用位置和[简要说明](https://zhuanlan.zhihu.com/p/681254858?utm_psn=1745759328311623680)
- ![](https://pic4.zhimg.com/80/v2-615cae7a66974b32cc4e8b7ebbd4e5a7_1440w.webp)

详见: [一文彻底搞懂Fine-tuning - 参数高效微调（Parameter-Efficient Fine-Tuning）](https://mp.weixin.qq.com/s/OFufH9hSFdLsntQkNwL4LA), 含图解


### PEFT 参数高效微调技术

#### 解决什么问题

起因：训练模式
- 全参数微调：对特定下游任务进行 Full FineTuning（全参数微调），**太过低效**；
- 部分参数微调：固定预训练模型的某些层，只微调接近下游任务的那几层参数，又难以达到**较好效果**。

#### 解决思路

PEFT技术通过**最小化**微调参数的数量和计算复杂度，来提高预训练模型在新任务上的性能，从而缓解大型预训练模型的训练成本。
- 即使计算资源受限，也可以利用预训练模型的知识来迅速适应新任务，实现高效的迁移学习。
- 因此，PEFT技术可以在提高模型效果的同时，大大缩短模型训练时间和计算成本，让更多人能够参与到深度学习研究中来。

### PEFT 方法

PEFT 主要方法：
- Prefix Tuning（在**模型输入层**添加**可训练** `前缀`嵌入）
- LoRA（通过`低秩矩阵`近似模型参数更新）
- Adapter Tuning（在模型层间插入**小型神经网络**adapters）。


方法
- `Prefix Tuning`：与full fine-tuning更新所有参数的方式不同，该方法是在输入token之前构造一段任务相关的virtual tokens作为Prefix，然后训练的时候只更新Prefix部分的参数，而Transformer中的其他部分参数固定。该方法其实和构造Prompt类似，只是Prompt是人为构造的“显式”的提示,并且无法更新参数，而Prefix则是可以学习的“隐式”的提示。同时，为了防止直接更新Prefix的参数导致训练不稳定的情况，他们在Prefix层前面加了MLP结构(相当于将Prefix分解为更小维度的Input与MLP的组合后输出的结果)，训练完成后，只保留Prefix的参数。
- `Prompt Tuning`：该方法可以看作是Prefix Tuning的简化版本，只在输入层加入prompt tokens，并不需要加入MLP进行调整来解决难训练的问题。随着预训练模型参数量的增加，Prompt Tuning的方法会逼近fine-tuning的结果。
- `P-Tuning`：该方法的提出主要是为了解决这样一个问题：大模型的Prompt构造方式严重影响下游任务的效果。P-Tuning将Prompt转换为可以学习的Embedding层，并用MLP+LSTM的方式来对prompt embedding进行一层处理。
- `P-Tuning v2`：让Prompt Tuning能够在不同参数规模的预训练模型、针对不同下游任务的结果上都达到匹敌Fine-tuning的结果。相比Prompt Tuning和P-tuning的方法，P-Tuning v2方法在多层加入了Prompts tokens作为输入，带来两个方面的好处：
  - 带来更多可学习的参数（从P-tuning和Prompt Tuning的0.1%增加到0.1%-3%），同时也足够参数高效。
  - 加入到更深层结构中的Prompt能给模型预测带来更直接的影响。
- `Adapter Tuning`：该方法设计了Adapter结构（首先是一个down-project层将高维度特征映射到低维特征，然后过一个非线形层之后，再用一个up-project结构将低维特征映射回原来的高维特征；同时也设计了skip-connection结构，确保了在最差的情况下能够退化为identity），并将其嵌入Transformer的结构里面，在训练时，固定住原来预训练模型的参数不变，只对新增的Adapter结构进行微调。同时为了保证训练的高效性（也就是尽可能少的引入更多参数）。
- `LoRA`：在涉及到矩阵相乘的模块，引入A、B这样两个低秩矩阵模块去模拟full fine-tuning的过程，相当于只对语言模型中起关键作用的低秩本质维度进行更新。

#### PEFT 实现

PEFT实现工具：
- PEFT：Huggingface推出的PEFT库。
- unify-parameter-efficient-tuning：一个参数高效迁移学习的统一框架。

Parameter-Efficient Fine-Tuning (`PEFT`) 是HuggingFace 开源的一个高效微调大模型库，支持在 LLM 上创建和微调适配器层。
- peft 与  🤗 Accelerate 无缝集成，用于利用了 DeepSpeed 和 Big Model Inference 的大规模模型。

【2023-7-11】[Prompt系列高效调参原理解析](https://mp.weixin.qq.com/s/webUB5j8nNQsthTFQNiqpA), [智源社区](https://hub.baai.ac.cn/view/28876)

PEFT内置7种主流高效调参方法
- `LoRA`: LORA: LOW-RANK ADAPTATION OF LARGE LANGUAGE MODELS
- `Prefix Tuning`: Prefix-Tuning: Optimizing Continuous Prompts for Generation,
- `P-Tuning v2`: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks
- `P-Tuning`: GPT Understands, Too
- `Prompt Tuning`: The Power of Scale for Parameter-Efficient Prompt Tuning
- `AdaLoRA`: Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning
- `QLoRA`: QLoRA: Efficient Finetuning of Quantized LLMs

时间线
- ![](https://simg.baai.ac.cn/hub-detail/f81b72c3cedac0b670dd7c68144b718c1692420361295.webp)

|时间|机构|方法|备注|
|---|---|---|---|
|2021.1|stanford|Prefix Tuning|Prompt Series|
|2021.3|Tsinghua|P-Tuning|Prompt Series|
|2021.9|Google|Prompt Tuning|Prompt Series|
|2021.11|Microsoft|LoRA|LoRA Series|
|2022.3|Tsinghua|P-Tuning v2|Prompt Series|
|2023.3|Microsoft|AdaLoRA|LoRA Series|
|2023.5|Washington|QLoRA|LoRA Series|

目前包含LoRA，Prefix Tuning，Prompt Tuning，P-Tuning 四种算法
*   LoRA
*   [Prefix Tuning](https://arxiv.org/pdf/2110.07602.pdf)
  - Prefix Tuning 算法是根据 下游任务 "前缀指令文本" 的所有层的embeding表示，学习到的前缀指令文本向量可以挖掘大模型的潜力去引导模型完成特定任务。
  - ![](https://pic3.zhimg.com/80/v2-9a6b5792cf60079429d067fc629e65ae_1440w.webp)
*   [P-Tuning](https://arxiv.org/pdf/2103.10385.pdf)
  - P-Tuning 算法和 Prefix Tuning 的想法很相似，想通过微调"指令文本",让指令文本去挖掘大模型的潜力去完成特定的任务。但是 P-Tuning 只学习 "指令文本" 输入层embeding的的表示。 为了增强 "指令文本"的连续性，采用了一个 MLP(LSTM) 的结果去encoding "指令文本"。从微调参数量来看只有 0.65% 比 Prefix Tuning 和 LoRA 这些在所有层都增加参数的方法要少。
  - ![](https://pic3.zhimg.com/80/v2-7540fb5d913adcae8be308fce31befea_1440w.webp)
*   [Prompt Tuning](https://arxiv.org/pdf/2104.08691.pdf)
  - Prompt Tuning 算法和 P-Tuning 很像，且更简单，就是是根据 下游任务 "指令文本" 输入层embeding的的表示。 Prompt Tuning 没有增加任何的层，直接使用微调指令文本(prompt) 的embeding向量。
  - ![](https://pic3.zhimg.com/80/v2-b281f773be36787dddd0f06e782384b2_1440w.webp)

[详见](https://zhuanlan.zhihu.com/p/618695885)

[Parameter-Efficient Fine-Tuning](https://github.com/huggingface/peft) (PEFT)

单个 24GB GPU 上使用上述工具使用 RL 微调 20B 参数量的 LLM, 详见量化[quantization](https://hf.co/docs/transformers/main/en/main_classes/quantization)
- 与全精度模型相比，以 **8位**精度加载模型最多可节省 **4倍**的内存
- 调用 from_pretrained 方法时简单地添加标志 load_in_8bit=True

详见：[在一张 24 GB 的消费级显卡上用 RLHF 微调 20B LLMs](https://mp.weixin.qq.com/s/7nmegO1UYObO0-eUDTKnMg)

#### PEFT 不足

相比全参数微调，高效微调技术目前存在的两个问题：
- 推理速度会变慢
- 模型精度会变差


### 应用示例

典型应用：
- `ChatGLM-Tuning` ：一种平价的chatgpt实现方案，基于清华的 ChatGLM-6B + LoRA 进行finetune。
- `Alpaca-Lora`：使用低秩自适应（LoRA）复现斯坦福羊驼的结果。Stanford Alpaca 是在 LLaMA 整个模型上微调，而 Alpaca-Lora 则是利用 Lora 技术，在冻结原模型 LLaMA 参数的情况下，通过往模型中加入额外的网络层，并只训练这些新增的网络层参数。由于这些新增参数数量较少，这样不仅微调的成本显著下降，还能获得和全模型微调类似的效果。
- `BLOOM-LORA`：由于LLaMA的限制，我们尝试使用Alpaca-Lora重新实现BLOOM-LoRA。


### 微调原理

FineTune 微调

预训练模型在小规模特定数据集上进一步训练，调整模型权重，适应特定任务或提高其性能。
- ![](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*JSJBBnslBE9S5i77Rz9r_g.png)

【2023-6-25】[大模型参数高效微调技术原理综述（七）-最佳实践、总结](https://mp.weixin.qq.com/s/M-7ZudD0dvscsApryiPIYw)

参数高效微调综述论文：
- 【2023-3-28】[Scaling Down to Scale Up: A Guide to Parameter-Efficient Fine-Tuning](https://arxiv.org/pdf/2303.15647.pdf)
- 中文[解读](https://zhuanlan.zhihu.com/p/627537421)

几种参数高效微调方法进行了简单的概述，主要有如下几类：
- `Additive` 增加**额外参数**，注意力与FFN后加一个**全连接层**
  - 如：Prefix Tuning、Prompt Tuning、Adapter Tuning及其变体。
  - soft prompts 软提示
    - Prompt Tuning: 输入前面加入一些新的可学习的嵌入向量
    - Prefix-Tuning: 在所有层前面加入可学习的参数
    - Intrinsic Prompt Tuning (IPT): 用自编码器来压缩soft Compact
  - adapters-like 适配器
    - Adapter: 在注意力与FFN后加一个全连接层
    - AdaMix: 采用MOE策略引入多个Adapters
  - 其它
    - Ladder-Side Tuning (LST): 在每个Transformer block旁边引入一个小型的Transformer来计算更新的参数，类似于Lora
    - (IA)3: 缩放 key value以及FFN的 激活函数
- `Selecttive` 选取一**部分参数**更新，如：BitFit。
  - BitFit：仅更新bias
  - DiffPruning: mask掉一些训练的参数
  - Freeze and Reconfigure (FAR): 按照行来划分为 训练的行与 冻结的行
  - FishMask: 使用Fisher信息矩阵来选取 top-p参数进行更新
- `Reparametrization` 引入**重参数化**，如：LoRA、AdaLoRA、QLoRA。
  - Intrinsic SAID: 更新一个低维空间的向量
  - LoRA: 更新旁路，且旁路设计为一个下采样与一个上采样
  - KronA: 使用克罗内克积来减小Lora的计算开支
- **混合**高效微调，如：MAM Adapter、UniPELT。
  - SparseAdapter: 使用一个维度较大的Adapter，并对这个Adapter稀疏化，避免参数过多
  - MAM Adapter: 并行的Adapter, FFN layer and soft prompt.
  - UniPELT: 将LoRa Prefix-tuning 和 Adapter 使用gat机制合并
  - Compacter: 使用克罗内克积，并且每层共享参数的 Adapter
  - S4: 探索了这些方法结合起来的效果

高效微调粗略分为三类：
- 加额外参数 `A` + 选取一部分参数更新 `S` + 引入重参数化 `R`
- ![](https://pic2.zhimg.com/80/v2-ed42c72dfe5b849dfeb5df142f270675_1440w.webp)

各种方法对比
- ![](https://pic1.zhimg.com/80/v2-87347f7802c02861ec2ed937d5a0422c_1440w.webp)

### BitFit

对微调机制的一种积极探索，通过**仅调整bias**就有不错的效果，但没有具体阐述原理，通过猜测加实验得到的结果。

观点：
> 微调过程不是让模型**适应**另外的数据分布，而是让模型更好的**应用出**本身的表征能力。

特点：
- 训练参数量极小（约0.1%）。
- 大部分任务上效果会**差于**LoRA、Adapter等方法。

### Prefix Tuning

Prefix Tuning 通过在模型输入层之前添加可训练的`前缀嵌入`（prefix embeddings）来影响模型的输出。

这些前缀嵌入与原始输入拼接后一起输入到模型中，而模型的其他部分保持不变。

Prefix Tuning（前缀微调）

什么是Prefix Tuning？
- Prefix Tuning 在原始文本进行词嵌入之后，在**前面**拼接上一个**前缀矩阵**，或将前缀矩阵拼在模型每一层的输入前。
- 这个前缀与输入序列一起作为注意力机制的输入，从而影响模型对输入序列的理解和表示。
- 由于前缀可学习，可在微调过程中根据特定任务进行调整，使得模型能够更好地适应新的领域或任务。

注意
- finetune 更新整个模型权重
- prefix tuning 则只更新前缀编码, 模型编码不动, fixed

详见: [一文彻底搞懂Fine-tuning - 参数高效微调（Parameter-Efficient Fine-Tuning）](https://mp.weixin.qq.com/s/OFufH9hSFdLsntQkNwL4LA), 含图解

#### 【2021.3.2】Prompt Tuning -- 离散token

受语言模型 in-context learning能力启发，只要有合适的上下文，语言模型就可以很好的解决自然语言任务。

针对不同任务，仅在输入层引入virtual token形式的**软提示**（soft prompt）。

特点：
- 相对于Prefix Tuning，参与训练的参数量和改变的**参数量更小**，更节省显存。
- 对一些简单的NLU 任务还不错，但对**硬序列**标记任务（即`序列标注`）表现欠佳。

**Prompt Tuning with soft prompts**

输入层增加可训练的Soft Prompt参数，参数长度一般在20-100个，每个参数的embedding维度和词表token的embedding维度相同，如下图所示：
- ![](https://pic1.zhimg.com/80/v2-85458b36242c77954879891f231bf2ec_1440w.webp)

相较于**全参数微调**，Prompt Tuning也是通过**冻结LLM的原始参数**，添加少量额外训练参数以达到加速训练的目的；
- ![](https://pic1.zhimg.com/80/v2-027a29613e0f2d780b44cbc0261c3218_1440w.webp)

Prompt Tuning 实际效果从下面图中看出：
- 1，当模型参数不大的时候，Prompt Tuning比全参数微调的效果差一点，但是高于单纯的Prompt工程；
- 2，当模型参数在100亿时，Prompt Tuning的效果和全参数微调的效果一样好；
- ![](https://pic2.zhimg.com/80/v2-549a94de38e793377170c271a46bf9bd_1440w.webp)

Prompt Tuning 可解释性说明：
1.  对于已完成训练的prompt embedding来说，是无法与词表中任何token表示对应的（Trained soft-prompt embedding does not correspond to a known token）；
2.  但是观察其邻域范围内的token表示可以看出其具有相同的语义，能够表示相同的意思（but nearest neighbors form a semantic group with similar meanings）；
- ![](https://pic3.zhimg.com/80/v2-2baec89ee6fc953eb3cc690264b67caa_1440w.webp)
- ![](https://pic1.zhimg.com/80/v2-5da93b477f40d3253d743edbdbe26478_1440w.webp)

固定预训练参数，为每个任务额外添加一个或多个embedding，之后拼接query正常输入LLM，并只训练这些embedding。
- 左图为单任务全参数微调，右图为prompt tuning。
- ![](https://pic2.zhimg.com/80/v2-2f6f96f9cf6614111e9a2e7c0eb9fbcd_1440w.webp)



```py
from peft import PromptTuningConfig, get_peft_model
peft_config = PromptTuningConfig(task_type="SEQ_CLS", num_virtual_tokens=10)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, return_dict=True)
model = get_peft_model(model, peft_config)
```


#### 【2021.8.1】Prefix Tuning -- 连续token

prompt tuning 是 Prefix Tuning 简化版本

prefix tuning 依然是固定预训练参数，但除了每个任务额外添加一个或多个embedding之外，利用多层感知编码prefix，注意多层感知机就是prefix的编码器，不再像prompt tuning继续输入LLM。

prompt tuning 针对特定任务找到**离散token前缀**，花费很长时间

prefix-tuning 使用连续的**virtual token** embedding来替换离散token

在每一个Transformer层都带上一些virtual token作为前缀，以适应不同的任务。

transformer中的每一层，句子表征前面插入可训练的virtual token embedding。对于自回归模型(GPT系列)，在句子前添加**连续前缀**，即 `z=[prefix;x;y]` 。对于Encoder-Decoder模型(T5)，则在Ecoder和Decoder前都添加连续前缀 `z=[prefix;x|prefix'|y]`

添加前缀的过程如图所示。
- ![](https://pic2.zhimg.com/v2-2fd28b31d2a3261fa17c50cdaee19a05_r.jpg)

虽然，prefix-tuning并没有添加太多的额外参数。但是，prefix-tuning**难以优化**，且会减少下游任务的序列长度。

特点：
- 前缀Token会占用序列长度，有一定额外计算开销。
- Prefix Tuning的线性插值比较复杂。

```py
embedding = torch.nn.Embedding(num_virtual_tokens, token_dim)
transform = torch.nn.Sequential(
    torch.nn.Linear(token_dim, encoder_hidden_size),
    torch.nn.Tanh(),
    torch.nn.Linear(encoder_hidden_size, num_layers * 2 * token_dim),
)
```

prefix tuning 代码

```py
peft_config = PrefixTuningConfig(task_type="CAUSAL_LM", num_virtual_tokens=20)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, return_dict=True)
model = get_peft_model(model, peft_config)
```


#### 【2021.11.2】P-Tuning

手动尝试最优的提示无异于大海捞针，于是有了**自动离散提示搜索**方法

但提示是离散的，神经网络是连续的，所以寻找最优提示可能是次优的。

p-tuning 依然固定LLM参数，利用多层感知机和LSTM对prompt进行编码，编码之后与其他向量进行拼接之后正常输入LLM。
- 注意，训练后只保留prompt编码之后的向量即可，无需保留编码器
- GPT在P-tuning 加持下可达到甚至超过BERT在NLU领域的性能。

prompt 编码器结构

```py
self.lstm_head = torch.nn.LSTM(
                    input_size=self.input_size,
                    hidden_size=self.hidden_size,
                    num_layers=num_layers,
                    dropout=lstm_dropout,
                    bidirectional=True,
                    batch_first=True,
  )

self.mlp_head = torch.nn.Sequential(
    torch.nn.Linear(self.hidden_size * 2, self.hidden_size * 2),
    torch.nn.ReLU(),
    torch.nn.Linear(self.hidden_size * 2, self.output_size),
)
self.mlp_head(self.lstm_head(input_embeds)[0])
```


将Prompt转换为可学习的**Embedding层**，并用 MLP+LSTM 方式对 Prompt Embedding 进行一层处理。
- 相比 Prefix Tuning，仅在输入层加入**可微**的virtual token；
- 另外，virtual token 位置也不一定是前缀，插入的位置是可选的。

特点：
- 引入一个prompt encoder（由一个双向的LSTM+两层MLP组成）来建模virtual token的相互依赖会收敛更快，效果更好。

代码样例：

```py
peft_config = PromptEncoderConfig(task_type="CAUSAL_LM", num_virtual_tokens=20, encoder_hidden_size=128)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, return_dict=True)
model = get_peft_model(model, peft_config)
```

#### 【2022.3.20】P-Tuning v2

p-tuning 问题：小参数量模型上表现差

V2版本类似LoRA，每层都嵌入了新的参数（称之为Deep FT），下图中开源看到p-tuning v2 集合了多种微调方法。

p-tuning v2 在多种任务上下进行微调，之后对于不同的任务如token classification与sentence classification添加了随机初始化的任务头（AutoModelForTokenClassification、AutoModelForSequenceClassification），而非使用自然语言的方式，可以说V2是集大成者。
- ![](https://pic2.zhimg.com/80/v2-85f6abe44785882dd95943758e600e65_1440w.webp)

每个Transformer层都加入了prompt token作为输入，引入**多任务**学习，针对不同任务采用不同的提示长度。并且回归传统的**分类标签**范式，而不是**映射器**。

特点：
- 解决了Prompt Tuning无法在小模型上有效提升的问题。
- 移除了对模型效果改进较小的重参数化的编码器（如：Prefix Tuning中的MLP、P-Tuning中的LSTM）。
- 对于一些复杂的硬序列标记任务（即序列标注）取得了不错的效果。


代码样例：

```py
peft_config = PrefixTuningConfig(task_type="SEQ_CLS", num_virtual_tokens=20)
model = AutoModelForSequenceClassification.from_pretrained(model_name_or_path, return_dict=True)
model = get_peft_model(model, peft_config)
```

### Adapter Tuning

该方法设计了Adapter结构，并将其嵌入Transformer的结构里面，针对每一个Transformer层，增加了两个Adapter结构，在训练时，固定住原来预训练模型的参数不变，只对新增的Adapter结构和Layer Norm 层进行微调。

特点：
- 通过在Transformer层中嵌入Adapter结构，在推理时会额外增加推理时长。

Adapter Tuning（适配器微调）

什么是Adapter Tuning？
- Adapter Tuning 在保持模型参数数量相对较小的情况下，通过增加**少量可训练参数**（即适配器）来提高模型在特定任务上的表现。

Adapter Tuning 核心思想
- 在预训练模型的中间层中插入小的可训练层或“适配器”。
- 这些适配器通常包括一些全连接层、非线性激活函数等，它们被设计用来捕获特定任务的知识，而不需要对整个预训练模型进行大规模的微调。

详见: [一文彻底搞懂Fine-tuning - 参数高效微调（Parameter-Efficient Fine-Tuning）](https://mp.weixin.qq.com/s/OFufH9hSFdLsntQkNwL4LA), 含图解

#### AdapterFusion

一种融合多任务信息的Adapter的变体，在 Adapter 的基础上进行优化，通过将学习过程分为两阶段来提升下游任务表现。

#### AdapterDrop

该方法在不影响任务性能的情况下，对Adapter动态高效的移除，尽可能的减少模型的参数量，提高模型在反向传播（训练）和正向传播（推理）时的效率。

特点：
- 通过从较低的 Transformer 层删除可变数量的Adaper来提升推理速度。 当对多个任务执行推理时，动态地减少了运行时的计算开销，并在很大程度上保持了任务性能。


### 【2021.8.16】LoRA 低秩适配

通过**低秩分解**来模拟参数改变量，以极小参数量实现大模型的**间接**训练。

特点：
- 将BA加到W上，消除推理延迟。
- 可插拔式切换不同任务。
- 设计较好，简单且效果好。

LoRA微调与全量微调相比，效果会更差，但团队将LoRA添加到所有的**线性层**解决了这个问题。

2021年，论文 [LoRA: Low-Rank Adaption of Large Language Models](https://arxiv.org/abs/2106.09685) 通过**冻结**预训练权重，并创建**查询和值**层的注意力矩阵的低秩版本，对大型语言模型进行微调。
- 低秩矩阵参数**远少于**原始模型，因此可用更少的 GPU 内存进行微调。
- 低阶适配器的微调取得了与微调完整预训练模型相当的结果。

#### LoRA 原理

核心思想
- 冻结预训练模型权重，将可训练的**秩分解矩阵**注入 Transformer 架构每一层，从而大大减少了下游任务的微调参数量

LoRA 实现流程：
- 原始预训练语言模型 (PLM) 旁增加一个旁路，做一个先**降维**再**升维**的操作，模拟`本征秩` (intrinsic rank)；
- 训练时，固定 PLM 参数不变，只训练降维矩阵 A 和升维矩阵 B，即优化器只优化右路的参数；
- 模型的输入/输出维度不变，左右两边共用模型输入，输出时将 PLM 与旁路的输出叠加：`h=Wx+BAx`
- 用零均值随机**高斯分布**初始化 A，用全零矩阵初始化 B，矩阵 B 的全零初始化，使得在训练最开始的一段时间，右路结果会接近于0，这样模块输出就基本上来自于左路，也就是大模型原有参数的计算结果，这使得模型优化的初始点和原始的大模型保持一致。


- 思想：在原模型旁边增加一个旁路，通过**低秩分解**（先降维再升维）模拟参数的更新量。
- 训练：原模型固定，只训练降维矩阵A和升维矩阵B。
- 推理：可将BA加到原参数上，不引入额外的推理延迟。
- 初始化：A采用高斯分布初始化，B初始化为全0，保证训练开始时旁路为0矩阵。

可插拔式的切换任务：当前任务W0+B1A1，将lora部分减掉，换成B2A2，即可实现任务切换。



示意图
- ![](https://pic4.zhimg.com/80/v2-48e88e61040a94284cc0499be8ecda37_1440w.webp)

LoRA微调可用不同低秩矩阵适配不同任务类型，且LLM 原始权重不用变化；
- ![](https://pic2.zhimg.com/80/v2-0ba745c8fff2c7015d9463206c5be631_1440w.webp)

LoRA将会使用低秩表示来编码 `△W` ，同时实现计算高效和存储高效。当预训练模型是175B GPT-3，可训练参数 `|0|` 可以小至 `|W0|` 的 0.01%

整体上LoRA微调效果相对于基座模型有较大的提升，但是相对于全参数微调方式来说效果上还是低一点。
- `Full fine-tune` > `LoRA` > `base model`
- ![](https://pic4.zhimg.com/80/v2-90f36dc2e8d97ccbe6bb20b941a9745b_1440w.webp)

对于 $\delta W_x$ 这部分，会乘上一个 scale 系数 <span style='color:red;font-size:300%'> $ Scale = \frac{\alpha}{r}$ </span>
- $\alpha$ 相对于 r, 保持常数倍关系。调节这个 $\alpha$ 大致, 相当于**调节学习率**，于是干脆固定为常数
- 实践中，rank r 应该设为多少比较合适呢？可以很低，不超过8
- [当红炸子鸡 LoRA，是当代微调 LLMs 的正确姿势？](https://zhuanlan.zhihu.com/p/618894919)

LoRA 一般会在 Transformer 每层中的 query_key_value 部分增加旁路，其中 `r` 为矩阵的秩，在模型训练中是可调节的参数，`r << d`，`r` 越大，可训练参数越多。
- 图见[原文](https://mp.weixin.qq.com/s/yTX_bQEur8Nj6h_uGFJ31g)

LoRA 优势: 使用较少 GPU 资源，在下游任务中对大模型进行微调。
- 开源社区中，开发者们使用 LoRA 对 `Stable Diffusion` 进行微调，取得了非常不错的效果。
- 随着 ChatGPT 的火爆，也涌现出了许多使用 LoRA 对 LLM 进行指令微调的工作。

这种技术允许使用小部分内存来微调 LLM。然而也有缺点
- 由于适配器层中的**额外**矩阵乘法，<span style='color:red'>前向和反向传递的速度大约是原来的**两倍**</span>。

LoRA 是 Parameter Efficient 方法之一。
- 过度参数化的模型位于一个低**内在维度**上，所以假设在模型适应过程中的权重变化也具有较低的“内在等级”。
- [LoRA](https://github.com/microsoft/LoRA)主要方法为**冻结**一个预训练模型的矩阵参数，并选择用A和B矩阵来替代，在下游任务时只更新A和B。
- ![](https://pic4.zhimg.com/80/v2-67cd3e1e603a5bb674463ddc4db38d57_1440w.webp)
- ![](https://pic2.zhimg.com/80/v2-f56b07afc29ccad77a6faffa130ab24d_1440w.webp)

【2023-5-27】LoRA压缩比，[港科大实验数据](https://lmflow.com/)

Extremely few parameters with LoRA
- LLaMA-33B （65GB）-> 25M
- LLaMA-13B（26GB） -> 13M
- LLaMA-7B （13.5GB）-> 8M


【2023-4-5】LoRA原理讲解，[LoRA：训练你的GPT](https://www.bilibili.com/video/BV17g4y1g7S6)

<iframe src="//player.bilibili.com/player.html?aid=824514848&bvid=BV17g4y1g7S6&cid=1084363572&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width='800' height='600'> </iframe>


```py
class LoraLayer:
    def __init__(
        self,
        r: int,
        lora_alpha: int,
        lora_dropout: float,
        merge_weights: bool,
    ):
        self.r = r
        self.lora_alpha = lora_alpha

        # Optional dropout
        if lora_dropout > 0.0:
            self.lora_dropout = nn.Dropout(p=lora_dropout)
        else:
            self.lora_dropout = lambda x: x

        # Mark the weight as unmerged
        # 标记低秩分解部分是否已经合并至预训练权重
        self.merged = False
        # 指定是否要将低秩分解部分合并至预训练权重中
        self.merge_weights = merge_weights

        # 是否要禁用低秩分解的部分，如果是，则仅使用预训练权重部分
        self.disable_adapters = False
```


【2024-1-29】自威斯康星大学麦迪逊分校的统计学助理教授Sebastian Raschka [使用 LoRA 和 QLoRA 微调LLM：数百次实验的见解](https://zhuanlan.zhihu.com/p/679172768?utm_psn=1735254298701877248)总结的经验
- 如何节省内存、选择最佳配置等问题。
- 是否应该用SGD取代AdamW，使用调度器的潜在价值
  - AdamW 和 SGD 优化器选择没区别
- 如何调整LoRA的超参数。
  - 提高r时，合适的 alpha 值是 2*r
- 原文链接：[Finetuning LLMs with LoRA and QLoRA: Insights from Hundreds of Experiments - Lightning AI](https://lightning.ai/pages/community/lora-insights/)

LoRA 将权重矩阵分解为两个较小的权重矩阵，以更参数有效的方式近似完全监督微调

实验模型
- 重点关注尚未进行指令微调的模型：[phi-1.5 1.3B](https://arxiv.org/abs/2309.05463)、[Mistral 7B](https://arxiv.org/abs/2310.06825)、[Llama 2 7B](https://arxiv.org/abs/2307.09288)、 Llama 2 13B 和[Falcon 40B](https://falconllm.tii.ae/)

GPU 资源
- 单卡A100 GPU

效果
- Mistral 7B 模型在数学基准测试非常出色。
- phi-1.5 1.3B 型号由于其相对较小的尺寸，在TruthfulQA MC2 性能较好。
- 由于某种原因，Llama 2 13B 在算术基准测试中表现不佳，而较小的 Llama 2 7B 在该领域表现明显优于它。

目前推测 phi-1.5 1.3B 和 Mistral 7B 可能已经接受过基准测试数据的训练，因此不用。

此外，剩余模型中最小的模型将提供最大的改进空间，同时保持较低的硬件要求。重点关注 Llama 2 7B。
- ![](https://pic1.zhimg.com/80/v2-5b5947fd3087bfdc8280e1bcf89305c8_1440w.webp)

Lit-GPT 中的 `–quantize` 标志（4 位普通浮点类型）启用 QLoRA
- ![](https://pic3.zhimg.com/80/v2-76124bca16d8ae19e5f86c49189c2e06_1440w.webp)
- QLoRA 非常节省内存，但会增加运行时成本。
- QLoRA 对模型性能的影响确实较小

#### LoRA 参数

LoRA 参数
- ![](https://lightningaidev.wpengine.com/wp-content/uploads/2023/10/lora-expimage7.png)
- [finetune/lora.py](https://github.com/Lightning-AI/lit-gpt/blob/bf60124fa72a56436c7d4fecc093c7fc48e84433/finetune/lora.py#L38)
- QKV:
  - LoRA 默认仅针对多头自注意力块中的 Key 和 Query 矩阵启用
  - 更改配置，启动值矩阵、投影层和线性层
- 迭代次数 epoch
  - 迭代次数的增加会导致整体性能变差。
- `r`: 最重要的参数 R，矩阵的秩/维度,直接影响模型复杂性和容量
  - 仅增加 r 本身就会使结果变得更糟
  - 较**高**的“r”意味着更强的表达能力，但可能导致**过拟合**
  - 而较**低**的“r”可以减少过度拟合，但会牺牲表达能力。
  - 实验： r 从 8 增加到 16，发现仅增加 r 本身就会使结果变得更糟
- `alpha`: 
  - 较高的“alpha”加强低秩结构或正则化
  - 而较低的“alpha”会减少其影响，使模型更加依赖于原始参数。
  - 调整“alpha”有助于在拟合数据和通过正则化模型防止过度拟合之间取得平衡。
  - 提高r时，选择较大的 alpha 值至关重要
  - 经验：微调 LLM 时，通常选择两倍于R的 alpha（注意与扩散模型时有所不同），以 QLoRA 为例，r=256 和 alpha=512 模型效果最佳
- 火山引擎方舟平台： 
  - r 调小时, 需要同步加大学习率, 该参数需要谨慎
  - alpha 是缩放系数, `scale = alpha / rank`
  - warmup相关参数: steps 需要多少步“热身”, step_rate 热身数据集的百分比
  - max batch tokens: 单worker每个batch最大token数
  - LR Scheduler type

```py
# Hyperparameters
learning_rate = 3e-4
batch_size = 128
micro_batch_size = 1
max_iters = 50000  # train dataset size
weight_decay = 0.01
lora_r = 8 # 最重要的参数 R，矩阵的秩/维度,直接影响模型复杂性和容量
lora_alpha = 16
lora_dropout = 0.05
lora_query = True # Q 矩阵启用
lora_key = False # K
lora_value = True # V 矩阵启用
lora_projection = False # 投影层是否启用
lora_mlp = False # 线性层是否启动
lora_head = False # 
warmup_steps = 100
```

![](https://lightningaidev.wpengine.com/wp-content/uploads/2023/10/lora-expimage10.jpg)

#### LoRA 使用

LoRA 已经被作者打包到了`loralib`中。
- `pip install loralib`

可以选择用loralib中实现的对应层来替换一些层。
- 目前loralib只支持 nn.Linear、nn.Embedding 和 nn.Conv2d。
- loralib还支持一个 MergedLinear，用于单个 nn.Linear 代表一个以上的层的情况，比如在一些关注 qkv 投影的实现中（self- attention）
- ![](https://pic2.zhimg.com/80/v2-bcef352dc1adf7d6f2fad86e1fe892fd_1440w.webp)

```py
# ===== Before =====
layer = nn.Linear(in_features, out_features)

# ===== After ======
import loralib as lora
# Add a pair of low-rank adaptation matrices with rank r=16
layer = lora.Linear(in_features, out_features, r=16)
```

详见原文：[微软LoRA: Low-Rank Adaptation of Large Language Models 代码解读](https://zhuanlan.zhihu.com/p/515954218)

或 huggingface 代码样例：

```py
peft_config = LoraConfig(task_type="SEQ_CLS", inference_mode=False, r=8, lora_alpha=16, lora_dropout=0.1)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, return_dict=True)
model = get_peft_model(model, peft_config)
```

#### LoRA 思考

【2024-8-22】[大模型面经——LoRA最全总结](https://mp.weixin.qq.com/s/d3WIiA3VDyyRPyWWkwHa3w)

优点
- 1）一个中心模型服务多个下游任务，**节省参数存储量** 
- 2）推理阶段不引入额外计算量 
- 3）与其它参数高效微调方法正交，可有效组合 
- 4）训练任务比较稳定，效果比较好 
- 5）LoRA 几乎不添加任何推理延迟，因为适配器权重可以与基本模型合并


缺点
- LoRA 参与训练的模型参数量不多，也就百万到千万级别的参数量，所以效果比全量微调差很多。
- 数据以及算力满足的情况下，还是微调的参数越多越好



训练理论
1. ChatGLM-6B LoRA 后的 权重多大？ 
  - rank 8 target_module query_key_value 条件下，大约15M。
1. LoRA 微调方法为啥能加速训练？ 
  - 1）只更新了**部分参数**：比如 LoRA原论文就选择只更新Self Attention的参数，实际使用时还可以选择只更新部分层的参数；
  - 2）减少了**通信时间**：由于更新参数量变少了，所以（尤其是多卡训练时）要传输的数据量也变少了，从而减少了传输时间； 
  - 3）采用了各种**低精度加速**技术，如FP16、FP8或者INT8量化等。
  - 这三部分原因确实能加快训练速度，然而并不是LoRA所独有，事实上几乎都有参数高效方法都具有这些特点。LoRA的优点是低秩分解很直观，在不少场景下跟全量微调的效果一致，以及在预测阶段不增加推理成本。
1. LoRA 这种微调方法和**全参数**比起来有什么劣势吗？
  - 如果有足够计算资源以及有10k以上数据，建议**全参数微调**
  - lora 初衷是解决不够计算资源的情况下微调，只引入了少量参数，就可以在消费级gpu上训练
  - 但lora 问题: 不能节省训练时间，相比于全量微调，他要训练更久，同时因为可训练参数量很小，在同样大量数据训练下，比不过全量微调。
1. LORA 应该作用于Transformer 哪个参数矩阵？ 
  - 1）将所有微调参数都放到attention的某一个参数矩阵的效果并不好，将可微调参数平均分配到 Wq 和 Wk 的效果最好；
  - 2）即使是秩仅取4也能在 ∆W 中获得足够的信息。
  - 实际操作中，应当将可微调参数分配到多种类型权重矩阵中，而不应该用更大的秩单独微调某种类型的权重矩阵。
1. LoRA 微调参数量怎么确定？ 
  - LoRA 模型中可训练参数的结果数量取决于低秩更新矩阵的大小，其主要由秩 r 和原始权重矩阵的形状确定。实际使用过程中，通过选择不同的 lora_target 决定训练的参数量。 
  - 以 LLama 为例： --lora_target q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj
1. Lora 矩阵怎么初始化？为什么要初始化为全0？
  - 矩阵B被初始化为0，而矩阵A正常高斯初始化。 
  - 如果B，A全都初始化为0，那么缺点与深度网络全0初始化一样，很容易导致梯度消失(因为此时初始所有神经元的功能都是等价的)。 
  - 如果B，A全部高斯初始化，那么在网络训练刚开始就会有概率为得到一个过大的偏移值Δ W 从而引入太多噪声，导致难以收敛。 
  - 因此，一部分初始为0，一部分正常初始化是为了在训练开始时维持网络的原有输出(初始偏移为0)，但同时也保证在真正开始学习后能够更好的收敛。
1. Rank 如何选取？ 
  - Rank 取值常见的是8，理论上说Rank在4-8之间效果最好，再高并没有效果提升。
  - 不过论文的实验是面向下游单一监督任务的，因此在指令微调上根据指令分布的广度，Rank选择还是需要在8以上的取值进行测试。
1. 是否可以逐层调整 LoRA 最优rank？ 
  - 理论上，可为不同层选择不同的LoRA rank，类似于为不同层设定不同学习率，但由于增加了调优复杂性，实际中很少执行。
1. alpha 参数 如何选取？ 
  - alpha 其实是个**缩放参数**，本质和learning rate相同，所以为了简化可以默认让 alpha=rank，只调整lr，这样可以简化超参。
1. LoRA 高效微调如何避免`过拟合`？
  - 过拟合还是比较容易出现。减小r或增加数据集大小可以帮助减少过拟合，还可以尝试增加优化器的权重衰减率或LoRA层的dropout值。
1. 如何在已有 LoRA 模型上**继续训练**？
  - 理解此问题的情形是：已有lora模型只训练了一部分数据，要训练另一部分数据的话，是在这个lora上继续训练呢，还是跟base 模型合并后再套一层lora，或者从头开始训练一个lora？ 
  - 把之前的LoRA跟base model 合并后，继续训练就可以，为了保留之前的知识和能力，训练新的LoRA时，加入一些之前的训练数据是需要的。每次都要重头训练的话成本比较高。
1. 哪些因素会影响**内存使用**？ 
  - 内存使用受到模型大小、批量大小、LoRA参数数量以及数据集特性的影响。例如，使用较短的训练序列可以节省内存。
1. LoRA 权重是否可以**合入原模型**？
  - 可以，将训练好的低秩矩阵（B*A）+原模型权重合并（相加），计算出新的权重。
1. LoRA 权重是否可以**合并**？ 
  - 可将多套LoRA权重合并。训练中保持LoRA权重独立，并在前向传播时添加，训练后可以合并权重以简化操作。


#### LoRA 实现

官方notebook案例：[peft_lora_seq2seq](https://github.com/huggingface/peft/blob/main/examples/conditional_generation/peft_lora_seq2seq.ipynb)

依赖包：
- transformers提供模型加载和训练；
- peft提供LoRA实现；
- DeepSpeed提供训练加速。

注意：
>peft包目前还处于快速迭代当中，后续接口可能会有大的变动，也可能存在一些bug。

关键依赖包版本：

```sh
transformers==4.26.1
torch==1.13.1
deepspeed==0.8.2
peft==0.2.0

git clone https://github.com/microsoft/DeepSpeedExamples.git
cd DeepSpeedExamples/applications/DeepSpeed-Chat/
```

ds lora 

```sh
deepspeed --num_gpus 1 main.py \
   --data_path Dahoas/rm-static \
   --data_split 2,4,4 \
   --model_name_or_path facebook/opt-6.7b \
   --per_device_train_batch_size 8 \
   --per_device_eval_batch_size 8 \
   --max_seq_len 512 \
   --learning_rate 1e-3 \
   --weight_decay 0.1 \
   --num_train_epochs 2 \
   --gradient_accumulation_steps 16 \
   --lr_scheduler_type cosine \
   --num_warmup_steps 0 \
   --seed 1234 \
   --gradient_checkpointing \
   --zero_stage 0 \
   --lora_dim 128 \
   --lora_module_name decoder.layers. \
   --deepspeed \
   --output_dir $OUTPUT_PATH \
   &> $OUTPUT_PATH/training.log
```


##### 训练代码

假设训练代码位于train.py。

导入依赖包

```py
import os
import torch
import random
import datasets
import numpy as np
​
from tqdm import tqdm
from typing import Dict
from torch.utils.data import DataLoader
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    TrainingArguments,
    Trainer
)
from peft import (
    LoraConfig,
    TaskType,
    get_peft_model,
    get_peft_model_state_dict,
    set_peft_model_state_dict
)
​
def set_random_seed(seed):
    if seed is not None and seed > 0:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.random.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
​
set_random_seed(1234)

# ----- 设置参数 -----
# LoRA参数
LORA_R = 8
LORA_ALPHA = 32
LORA_DROPOUT = 0.1
# 训练参数
EPOCHS=3
LEARNING_RATE=5e-5
OUTPUT_DIR="./checkpoints"
BATCH_SIZE=4 # 2
GRADIENT_ACCUMULATION_STEPS=3
# 其他参数
MODEL_PATH = "bigscience/bloomz-7b1-mt"
DATA_PATH = "./data/belle_open_source_1M.train.json"
MAX_LENGTH = 512
PATTERN = "{}\n{}"
DS_CONFIG = "ds_zero2_config.json"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH) # 加载tokenizer

# ---- 加载数据 -----
dataset = datasets.load_dataset("json", data_files=DATA_PATH)
# print(dataset["train"][0])
# tokenize 分词
def tokenize(text: str, add_eos_token=True):
    result = tokenizer(
        text,
        truncation=True,
        max_length=MAX_LENGTH,
        padding=False,
        return_tensors=None)
    # 判断是否要添加eos_token
    if (result["input_ids"][-1] != tokenizer.eos_token_id
        and len(result["input_ids"]) < MAX_LENGTH
        and add_eos_token):
        result["input_ids"].append(tokenizer.eos_token_id)
        result["attention_mask"].append(1)
    result["labels"] = result["input_ids"].copy()
    return result
​
def preprocess(example: Dict, train_on_inputs: bool = False):
    prompt = example["input"]
    response = example["target"]
    text = PATTERN.format(prompt, response)
    tokenized_inp = tokenize(text)
    # 若train_on_inputs为False，则将label中与input相关的token替换为-100
    if not train_on_inputs:
        tokenized_prompt = tokenize(prompt,add_eos_token=False)
        prompt_tokens_len = len(tokenized_prompt["input_ids"])
        tokenized_inp["labels"] = [-100]*prompt_tokens_len + tokenized_inp["labels"][prompt_tokens_len:]
    return tokenized_inp
​
train_data = dataset["train"].shuffle().map(preprocess, remove_columns=["id", "input", "target"])
print(train_data[0])

# ----- collate_fn -----
# pad_to_multiple_of=8表示padding的长度是8的倍数
collate_fn = DataCollatorForSeq2Seq(tokenizer, pad_to_multiple_of=8, return_tensors="pt", padding=True)
# 加载模型
device_map = {"": int(os.environ.get("LOCAL_RANK") or 0)}
# device_map指定模型加载的GPU;troch_dtype=torch.float16表示半精度加载模型
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map=device_map)
# ----- LoRA相关 -----
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=LORA_R, # LoRA中低秩近似的秩
    lora_alpha=LORA_ALPHA, # 见上文中的低秩矩阵缩放超参数
    lora_dropout=LORA_DROPOUT, # LoRA层的dropout
)
# ----- 转换模型 -----
model = get_peft_model(model, lora_config)
model.config.use_cache = False
old_state_dict = model.state_dict
model.state_dict = (
    lambda self, *_, **__: get_peft_model_state_dict(self, old_state_dict())
).__get__(model, type(model))
# 打印模型中的可训练参数
model.print_trainable_parameters()
# ----- 训练参数 -----
args = TrainingArguments(
    output_dir=OUTPUT_DIR, # checkpoint的存储目录
    per_device_train_batch_size=BATCH_SIZE, # 单设备上的batch size
    gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS, # 梯度累加的step数
    warmup_steps=100,
    num_train_epochs=EPOCHS,
    learning_rate=LEARNING_RATE,
    fp16=True, # 使用混合精度训练
    logging_steps=50,
    evaluation_strategy="no", # 不进行评估
    save_strategy="steps",
    save_steps=2000, # 保存checkpoint的step数
    save_total_limit=5, # 最多保存5个checkpoint
    deepspeed=DS_CONFIG
)
# 模型训练
trainer = Trainer(
    model=model,
    train_dataset=train_data,
    eval_dataset=None,
    args=args,
    data_collator=collate_fn
)
trainer.train()
model.save_pretrained("best_model")
```

DeepSpeed配置文件
- DeepSpeed配置文件名为ds_zero2_config.json。

```py
{
  "train_micro_batch_size_per_gpu": "auto",
  "gradient_accumulation_steps": "auto",
  "steps_per_print": 50,
  "gradient_clipping": 1.0,
  "zero_optimization": {
    "stage": 2,
    "offload_optimizer": {
            "device": "cpu"
    },
    "contiguous_gradients": true,
    "overlap_comm": true
  },
  "zero_allow_untested_optimizer": true,
  "fp16": {
    "enabled": true,
    "loss_scale": 0,
    "loss_scale_window": 1000,
    "hysteresis": 2,
    "min_loss_scale": 1
  },
  "optimizer": {
    "type": "Adam",
    "params": {
      "lr": "auto",
      "betas": "auto",
      "eps": "auto",
      "weight_decay": "auto"
    }
  },
  "activation_checkpointing": {
    "partition_activations": true,
    "contiguous_memory_optimization": true
  },
  "wall_clock_breakdown": false
}
```

**启动**

```sh
deepspeed --include=localhost:0,1,2,3 train.py
```

##### LoRA 推理

推理文件名为inference.py

原始模型和lora模型顺序处理，再合并
- 先加载 base_model
- 再加载 lora_model 
- 推理

```py
import torch
  
from peft import PeftModel # lora
from transformers import AutoModelForCausalLM, AutoTokenizer
​# ---- 原始模型 -----
BASE_MODEL = "bigscience/bloomz-7b1-mt"
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16, # 加载半精度
        device_map={"":0}, # 指定GPU 0
    )
model.eval()
​# ---- LoRA模型 -----
LORA_WEIGHTS = "best_model"
model = PeftModel.from_pretrained(model, LORA_WEIGHTS, torch_dtype=torch.float16)
model.half() # 半精度
​# ---- 推理 -----
prompt = ""
inp = tokenizer(prompt, max_length=512, return_tensors="pt").to("cuda")
outputs = model.generate(input_ids=inp["input_ids"], max_new_tokens=256)
print(tokenizer.decode(outputs[0]))
```

[原文](https://zhuanlan.zhihu.com/p/618073170)


### LoRA 进化

【2024-5-24】

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-05-24T12:43:16.306Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36\&quot; etag=\&quot;MZRa7dl-SX42qmgFS0G9\&quot; version=\&quot;24.4.4\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;YUrH7kkdw6S7EPocWAtV\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1434\&quot; dy=\&quot;761\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;CRyWcW9bKPYmjVe2kgWn-2\&quot; value=\&quot;LoRA进化之路\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=0;fontSize=22;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;450\&quot; y=\&quot;30\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;lHimWeaf7UQe36nZpLsc-30\&quot; value=\&quot;wqw547243068@163.com&amp;lt;br&amp;gt;2023-12-31\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;67.88\&quot; y=\&quot;410\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;s2pv88CfUx30G5g510ko-26\&quot; value=\&quot;【2021-10-16】微软\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;40.50999999999999\&quot; y=\&quot;240\&quot; width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;1nzIP9oYbUBeoa8APZYR-3\&quot; value=\&quot;低秩分解模拟参数改变量，PEFT方法之一&amp;lt;div&amp;gt;以极小参数量实现大模型间接训练&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;7&amp;amp;nbsp; B: 13G -&amp;amp;gt; 8M&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;13B: 26G -&amp;amp;gt; 13M&amp;lt;/div&amp;gt;&amp;lt;div&amp;gt;33B: 65G -&amp;amp;gt; 25M&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;10\&quot; y=\&quot;300\&quot; width=\&quot;250\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-4\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;2hlaNrKACTqZJU9JD0af-1\&quot; target=\&quot;2hlaNrKACTqZJU9JD0af-2\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-1\&quot; value=\&quot;&amp;lt;font&amp;gt;LoRA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;shadow=1;fontColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;67.88\&quot; y=\&quot;270\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-2\&quot; value=\&quot;&amp;lt;font&amp;gt;AdaLoRA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;shadow=1;fontColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;308.75\&quot; y=\&quot;270\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-6\&quot; value=\&quot;根据重要评分动态分配参数预算&amp;lt;div&amp;gt;重要矩阵高秩，次要矩阵低秩&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;389.75\&quot; y=\&quot;270\&quot; width=\&quot;190\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-7\&quot; value=\&quot;&amp;lt;font&amp;gt;QLoRA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;shadow=1;fontColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;284\&quot; y=\&quot;380\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-8\&quot; value=\&quot;【2023-05-23】华盛顿大学\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;344\&quot; y=\&quot;370\&quot; width=\&quot;170\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-9\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;2hlaNrKACTqZJU9JD0af-1\&quot; target=\&quot;2hlaNrKACTqZJU9JD0af-7\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;153\&quot; y=\&quot;295\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;294\&quot; y=\&quot;295\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;190\&quot; y=\&quot;285\&quot; /&gt;\n              &lt;mxPoint x=\&quot;190\&quot; y=\&quot;395\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-10\&quot; value=\&quot;4bit量化，分页优化器，双重量化&amp;lt;div&amp;gt;48G显存GPU上训练65B模型，可手机上使用&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;390\&quot; width=\&quot;260\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-11\&quot; value=\&quot;&amp;lt;font&amp;gt;ReLoRA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;shadow=1;fontColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;364.75\&quot; y=\&quot;195\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-12\&quot; value=\&quot;【2023-08-21】马萨诸塞大学、Eleuther AI\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;344\&quot; y=\&quot;165\&quot; width=\&quot;250\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-13\&quot; value=\&quot;叠加多个低秩更新矩阵\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;440\&quot; y=\&quot;190\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-14\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;2hlaNrKACTqZJU9JD0af-1\&quot; target=\&quot;2hlaNrKACTqZJU9JD0af-11\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;153\&quot; y=\&quot;295\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;294\&quot; y=\&quot;295\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;210\&quot; y=\&quot;285\&quot; /&gt;\n              &lt;mxPoint x=\&quot;210\&quot; y=\&quot;210\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-15\&quot; value=\&quot;&amp;lt;font&amp;gt;LongLoRA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;shadow=1;fontColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;494.75\&quot; y=\&quot;234\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-16\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;2hlaNrKACTqZJU9JD0af-1\&quot; target=\&quot;2hlaNrKACTqZJU9JD0af-15\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;153\&quot; y=\&quot;295\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;375\&quot; y=\&quot;220\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;230\&quot; y=\&quot;285\&quot; /&gt;\n              &lt;mxPoint x=\&quot;230\&quot; y=\&quot;250\&quot; /&gt;\n              &lt;mxPoint x=\&quot;485\&quot; y=\&quot;250\&quot; /&gt;\n              &lt;mxPoint x=\&quot;485\&quot; y=\&quot;249\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-17\&quot; value=\&quot;【2023-10-01】港中文/MIT\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;559.75\&quot; y=\&quot;225\&quot; width=\&quot;170\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-18\&quot; value=\&quot;扩大窗口：4k -&amp;amp;gt; 32k\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;579.75\&quot; y=\&quot;240\&quot; width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-19\&quot; value=\&quot;&amp;lt;font&amp;gt;SLoRA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;shadow=1;fontColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;584.75\&quot; y=\&quot;314\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-20\&quot; value=\&quot;【2023-11-15】伯克利/斯坦福\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;570\&quot; y=\&quot;284\&quot; width=\&quot;180\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-21\&quot; value=\&quot;一个GPU部署多个LoRA&amp;lt;div&amp;gt;pageattention → 统一分页&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;570\&quot; y=\&quot;344\&quot; width=\&quot;160\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-22\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;2hlaNrKACTqZJU9JD0af-1\&quot; target=\&quot;2hlaNrKACTqZJU9JD0af-19\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;153\&quot; y=\&quot;295\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;294\&quot; y=\&quot;405\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;240\&quot; y=\&quot;285\&quot; /&gt;\n              &lt;mxPoint x=\&quot;240\&quot; y=\&quot;330\&quot; /&gt;\n              &lt;mxPoint x=\&quot;580\&quot; y=\&quot;330\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-23\&quot; value=\&quot;&amp;lt;font&amp;gt;DoRA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;shadow=1;fontColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;799\&quot; y=\&quot;355\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-24\&quot; value=\&quot;【2024-03-01】NVIDIA Lab\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;864.25\&quot; y=\&quot;355\&quot; width=\&quot;170\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-25\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(51, 51, 51); font-family: Arial, &amp;amp;quot;Microsoft YaHei&amp;amp;quot;, 黑体, 宋体, sans-serif; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;预训练权重分解为&amp;lt;/span&amp;gt;&amp;lt;strong style=&amp;quot;box-sizing: border-box; color: rgb(51, 51, 51); font-family: Arial, &amp;amp;quot;Microsoft YaHei&amp;amp;quot;, 黑体, 宋体, sans-serif; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;幅度&amp;lt;/strong&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(51, 51, 51); font-family: Arial, &amp;amp;quot;Microsoft YaHei&amp;amp;quot;, 黑体, 宋体, sans-serif; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;（magnitude）和&amp;lt;/span&amp;gt;&amp;lt;strong style=&amp;quot;box-sizing: border-box; color: rgb(51, 51, 51); font-family: Arial, &amp;amp;quot;Microsoft YaHei&amp;amp;quot;, 黑体, 宋体, sans-serif; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;&amp;quot;&amp;gt;方向&amp;lt;/strong&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(51, 51, 51); font-family: Arial, &amp;amp;quot;Microsoft YaHei&amp;amp;quot;, 黑体, 宋体, sans-serif; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;（direction）&amp;lt;/span&amp;gt;&amp;lt;div&amp;gt;&amp;lt;span style=&amp;quot;color: rgb(51, 51, 51); font-family: Arial, &amp;amp;quot;Microsoft YaHei&amp;amp;quot;, 黑体, 宋体, sans-serif; font-size: 11px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;LoRA微调方向矩阵&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;labelBackgroundColor=none;fontSize=11;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;802.75\&quot; y=\&quot;385\&quot; width=\&quot;293\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-36\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;2hlaNrKACTqZJU9JD0af-26\&quot; target=\&quot;2hlaNrKACTqZJU9JD0af-35\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-26\&quot; value=\&quot;&amp;lt;font&amp;gt;LoRAMOE&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;715.25\&quot; y=\&quot;135\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-27\&quot; value=\&quot;【2023-12-?】?\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;697.87\&quot; y=\&quot;75\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-28\&quot; value=\&quot;结合MoE技术，token软路由\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;520.0000000000001\&quot; y=\&quot;105\&quot; width=\&quot;170\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-31\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;2hlaNrKACTqZJU9JD0af-29\&quot; target=\&quot;2hlaNrKACTqZJU9JD0af-26\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-29\&quot; value=\&quot;&amp;lt;font&amp;gt;MoLoRA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;477.37\&quot; y=\&quot;135\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-30\&quot; value=\&quot;【2023-09-?】?\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;500\&quot; y=\&quot;85\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-32\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;2hlaNrKACTqZJU9JD0af-1\&quot; target=\&quot;2hlaNrKACTqZJU9JD0af-29\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;140\&quot; y=\&quot;290\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;375\&quot; y=\&quot;220\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;180\&quot; y=\&quot;285\&quot; /&gt;\n              &lt;mxPoint x=\&quot;180\&quot; y=\&quot;150\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-33\&quot; value=\&quot;&amp;lt;font&amp;gt;MoV&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;481.37\&quot; y=\&quot;100\&quot; width=\&quot;32.63\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-34\&quot; value=\&quot;解决灾难遗忘&amp;lt;div&amp;gt;同一位置lora分两组&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;715.2500000000001\&quot; y=\&quot;95\&quot; width=\&quot;130\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-35\&quot; value=\&quot;&amp;lt;font&amp;gt;MOLA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;shadow=1;fontColor=#ffffff;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;845.25\&quot; y=\&quot;135\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-37\&quot; value=\&quot;【2024-02-?】?\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;827.88\&quot; y=\&quot;85\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-38\&quot; value=\&quot;离散路由\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;847.8800000000001\&quot; y=\&quot;105\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-39\&quot; value=\&quot;&amp;lt;font&amp;gt;PiSSA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;shadow=1;fontColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;999\&quot; y=\&quot;300\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-40\&quot; value=\&quot;【2024-04-12】北大\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;989\&quot; y=\&quot;255\&quot; width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-41\&quot; value=\&quot;&amp;lt;font face=&amp;quot;Arial, Microsoft YaHei, 黑体, 宋体, sans-serif&amp;quot; color=&amp;quot;#333333&amp;quot;&amp;gt;Adapter初始化方式不同&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fillColor=none;labelBackgroundColor=none;fontSize=11;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1009\&quot; y=\&quot;275\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-42\&quot; value=\&quot;&amp;lt;font&amp;gt;LISA&amp;lt;/font&amp;gt;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;shadow=1;fontColor=#FFFFFF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;816.8800000000001\&quot; y=\&quot;300\&quot; width=\&quot;75.25\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-43\&quot; value=\&quot;【2024-03-28】香港理工\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#006600;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;804\&quot; y=\&quot;259\&quot; width=\&quot;160\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2hlaNrKACTqZJU9JD0af-44\&quot; value=\&quot;始终更新底层embedding和顶层linearhead\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;760\&quot; y=\&quot;275\&quot; width=\&quot;250\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



#### 单 LoRA

##### 【2023-3-18】AdaLoRA

对LoRA的一种改进，根据**重要性评分**动态分配参数预算给权重矩阵，将关键的增量矩阵分配高秩以捕捉更精细和任务特定的信息，而将较不重要的矩阵的秩降低，以防止过拟合并节省计算预算。

论文
- [ADALORA: ADAPTIVE BUDGET ALLOCATION FOR PARAMETER-EFFICIENT FINE-TUNING](https://arxiv.org/pdf/2303.10512)

出发点：
- 在不同层、不同$$\textbf{W}$$上添加LoRA，效果不同，那么如何在规定的总rank预算下，达成最优效果。也就是如何给不同$$\textbf{W}$$分配不同的rank进行finetune

预训练语言模型中的不同权重参数对下游任务的贡献不同。

因此需要更加智能地分配参数预算，以便在微调过程中更加高效地更新那些对模型性能贡献较大的参数。
- 通过**奇异值分解**将权重矩阵分解为**增量矩阵**，并根据**新重要性度量**动态地调整每个增量矩阵中奇异值的大小。
- 这样可以使得在微调过程中只更新那些对模型性能贡献较大或必要的参数，从而提高了模型性能和参数效率。

效果
1. 在相同总rank下，adaLoRA效果好于LoRA
2. 不同层不同$$\textbf{W}$$的rank：更偏好FFN1和更高层的W

代码样例：

```py
peft_config = AdaLoraConfig(peft_type="ADALORA", task_type="SEQ_2_SEQ_LM", r=8, lora_alpha=32, target_modules=["q", "v"],lora_dropout=0.01)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, return_dict=True)
model = get_peft_model(model, peft_config)
```


##### 【2023-5-23】QLoRA

【2023-5-23】华盛顿大学发布一种高效的微调方法：QLoRA，在保持完整的16位微调任务性能下，实现单个 48GB GPU 上微调 65B 参数量模型。
- [QLoRA: Efficient Finetuning of Quantized LLMs](arxiv.org/abs/2305.14314)
- github：[QLoRA](https://github.com/artidoro/qlora)，[Demo](https://huggingface.co/spaces/uwnlp/guanaco-playground-tgi)
- 参考：[开源「原驼」爆火，iPhone都能微调大模型了，得分逼近ChatGPT！](https://mp.weixin.qq.com/s/RakazI25dMJz0JUkdtbr0w)

QLoRA 通过冻结的 4-bit 量化预训练语言模型向低秩适配器(LoRA) **反向传播**梯度。使用 4-bit NormalFloat (NF4) 量化、Double Quantization、Paged Optimizers、所有 Linear 层插入 adapter 等技术，QLoRA 在不牺牲性能的情况下大大节省了显存占用。

说明如下：
- **4bit NormalFloat**（NF4）：对于正态分布权重而言，一种信息理论上最优的新数据类型，该数据类型对于正态分布数据可以产生比 4 bit 整数和 4bit 浮点数更好的实证结果。
- **Double Quantization**：对第一次量化后的那些常量再进行一次量化，减少存储空间。
- **Paged Optimizers**：使用 NVIDIA 统一内存特性，实现了 CPU 和 GPU 之间自动的页面转换。当 GPU 内存不足时，Paged Optimizers 技术会自动将优化器状态转移到 CPU 内存，以确保优化器的正常运行。
- **All-Linear-Layer-Adapter**：在所有全连接层都插入 LoRA Adapter，增加了训练参数，能匹配16位全参数微调的性能。

- 减少内存使用量，足以在单个 **48GB** GPU 上微调 **65B** 参数模型，同时保留完整的 16 位微调任务性能。其中最好的模型称为 `Guanaco`，在 `Vincuna` 基准测试中优于之前公开发布的模型，并缩小了在 ChatGPT 上的差距，达到 ChatGPT 性能水平的 99.3%，同时仅在单个专业 GPU 上微调 24 小时。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/1e63b20d24a648bfaffa5d4e86266b65~tplv-obj:787:744.image?_iz=97245&from=post&x-expires=1692748800&x-signature=SEttWjvsni1S2XkoNgW7RHdIqiI%3D)

Q代表**量化**（Quantization），用低精度数据类型去逼近神经网络中的高精度浮点数，以提高运算效率

QLoRA 结合了 4-bit量化 和 LoRA，以及团队新创的三个技巧：
- 新数据类型 4-bit NormalFloat
- 分页优化器（Paged Optimizers）
- 双重量化（Double Quantization）

最终， QLoRA 让 4-bit的原驼在所有场景和规模的测试中匹配16-bit的性能。
- QLoRA的高效率让团队在华盛顿大学的小型GPU集群上每天可以微调LLaMA 100多次

两个关键结论：
- <span style='color:blue'>数据质量 >> 数据数量</span>
- 指令微调有利于**推理**，但不利于**聊天**

QLoRA可以用在手机上，论文共同一作Tim Dettmers估计以 iPhone 12 Plus的算力, 每个晚上能微调300万个单词的数据量。

特点
- 用 QLoRA 微调模型，可以显著降低对于显存的要求。
- 同时，模型训练的速度会**慢于**LoRA。

##### 【2023-8-7】LoRA-FA

LoRA-FA，香港科技大学
- 论文: [LORA-FA: MEMORY-EFFICIENT LOW-RANK ADAPTATION FOR LARGE LANGUAGE MODELS FINE-TUNING](https://arxiv.org/pdf/2308.03303)

做法
1. 随机初始化 A ， B 初始化为$$\textbf{0}$$矩阵
2. freeze  A ，只更新$$\textbf{B}$$，需要更新的参数降为一半

效果也与LoRA相当
- 减少训练参数，不减少计算量


##### 【2023-8-21】ReLoRA

【2023-8-21】[LoRA继任者ReLoRA登场，通过叠加多个低秩更新矩阵实现更高效大模型训练效果](https://www.toutiao.com/article/7269582259458572834)
- 论文链接：[paper](https://arxiv.org/abs/2307.05695)
- 代码仓库：[peft_pretraining](https://github.com/guitaricet/peft_pretraining)
- 过去十年中深度学习发展阶段中的一个核心原则就是不断的“堆叠更多层（stack more layers）. 那么继续以堆叠方式来提升低秩适应的训练效率

马萨诸塞大学洛厄尔分校将`ReLoRA`应用在具有高达350M参数的Transformer上时，展现出了与常规神经网络训练相当的性能。

此外，ReLoRA的微调效率会随着模型参数**规模增加而不断提高**，这使得其未来有可能成为训练超大规模（通常超过1B参数）LLMs的新型手段。

论文提出一种基于**低秩更新**的ReLoRA方法训练和微调高秩网络，其性能优于具有相同可训练参数数量的网络，甚至能够达到与训练100M+规模的完整网络类似的性能，对比效果如图所示。

从两个矩阵之和的秩入手
- 矩阵相加的后秩的上界会比较紧凑
- 对于矩阵 A, B，满足 Rank(A) < dim(A)，B同理, 使得矩阵之和的秩高于 A 或 B 

利用这一特性制定灵活的参数高效训练方法，然后从LoRA算法开始入手，LoRA可以将模型权重的更新量 delta(W) 分解为一组低秩矩阵乘积 

ReLoRA方法包含
- （1）初始化全秩训练
- （2）LoRA 训练
- （3）参数重新启动
- （4）锯齿状学习率调度（jagged learning rate schedule）
- （5）优化器参数部分重置。

作者选择目前非常火热的`自回归语言模型`进行实验，并且保证每个实验所使用的GPU计算时间不超过8天。


##### 【2023-10-1】LongLoRA

【2023-10-1】[贾佳亚韩松团队新作：两行代码让大模型上下文窗口倍增](https://www.toutiao.com/article/7284843466167796239)

只要两行代码+11个小时微调，就能把大模型**4k**的窗口长度提高到**32k**。

规模上，最长可以扩展到10万token，一口气就能读完长篇小说的多个章节或中短篇小说。

贾佳亚韩松联合团队提出的这个基于LoRA的全新大模型**微调**方法，登上了GitHub热榜，开源一周时间收获1k+ stars。这种方式叫做 `LongLoRA` ，由来自香港中文大学和MIT的全华人团队联合出品。

在一台8个A100组成的单机上，增大窗口长度的速度比全量微调快数倍。
- [论文地址](https://arxiv.org/abs/2309.12307)
- [GitHub项目页](https://github.com/dvlab-research/LongLoRA)


##### 【2024-1-16】VERA

阿姆斯特丹大学
- [VERA: VECTOR-BASED RANDOM MATRIX ADAPTATION](https://arxiv.org/pdf/2310.11454)

1. 不训练AB，训练额外的两个向量
2. AB在所有层共享，且都随机初始化，显著减少需要训练的参数量

效果
- 可学习参数量显著少于LoRA的情况下，效果和LoRA基本持平

##### 【2024-2-19】LoRA+

【2024-2-19】LoRA+
- 论文: [LoRA+: Efficient Low Rank Adaptation of Large Models](https://arxiv.org/pdf/2402.12354)
（UCB）

结论
- 当B的学习率大于A的学习率时效果更好
- B的学习率是A的 $$\sqrt{m/r}$$ 倍时, 效果最好(理论值，实验时倍数当作超参)

##### 【2024-3-1】DoRA

【2024-3-1】[DoRA：LoRA再升级-参数高效微调](https://zhuanlan.zhihu.com/p/684833295)
- [DoRA: Weight-Decomposed Low-Rank Adaptation](https://arxiv.org/pdf/2402.09353)
- 代码 [DoRA](https://github.com/NVlabs/DoRA)

Lora 本质上把大矩阵拆成两个小矩阵的乘法
- ![](https://pic1.zhimg.com/80/v2-5a6c032445742aa6df093e6fec4dfd98_1440w.webp)

```py
class LoRALayer(nn.Module):
    def __init__(self, in_dim, out_dim, rank, alpha):
        super().__init__()
        std_dev = 1 / torch.sqrt(torch.tensor(rank).float())
        self.A = nn.Parameter(torch.randn(in_dim, rank) * std_dev)
        self.B = nn.Parameter(torch.zeros(rank, out_dim))
        self.alpha = alpha

    def forward(self, x):
        x = self.alpha * (x @ self.A @ self.B)
        return x

class LinearWithLoRAMerged(nn.Module):
    def __init__(self, linear, rank, alpha):
        super().__init__()
        self.linear = linear
        self.lora = LoRALayer(
            linear.in_features, linear.out_features, rank, alpha
        )

    def forward(self, x):
        lora = self.lora.A @ self.lora.B # Combine LoRA matrices
        # Then combine LoRA with orig. weights
        combined_weight = self.linear.weight + self.lora.alpha*lora.T 
        return F.linear(x, combined_weight, self.linear.bias)
```

DoRA（Weight-Decomposed Low-Rank Adaptation）主要思想
- 将预训练权重分解为**幅度**（magnitude）和**方向**（direction），并利用LoRA来微调方向矩阵
- ![](https://pic1.zhimg.com/80/v2-34cab3f7896975b3ea1032113441aff8_1440w.webp)
- 公式见原文

```py
class LinearWithDoRAMerged(nn.Module):

    def __init__(self, linear, rank, alpha):
        super().__init__()
        self.linear = linear
        self.lora = LoRALayer(
            linear.in_features, linear.out_features, rank, alpha
        )
        self.m = nn.Parameter(
            self.linear.weight.norm(p=2, dim=0, keepdim=True))

  # Code loosely inspired by    
  # https://github.com/catid/dora/blob/main/dora.py

    def forward(self, x):
        lora = self.lora.A @ self.lora.B
        numerator = self.linear.weight + self.lora.alpha*lora.T
        denominator = numerator.norm(p=2, dim=0, keepdim=True)
        directional_component = numerator / denominator
        new_weight = self.m * directional_component
        return F.linear(x, new_weight, self.linear.bias)
```

**LoRA通常会等比例增减幅度和方向，DoRA通过将预训练权重矩阵分解为幅度和方向，能够更接近全量微调的效果**。

- 使用比LoRA更少的参数，效果还更好
- ![](https://pic3.zhimg.com/v2-2681727bb6226a5b1d3651b80ccbc52e_b.jpg)
- 使用较小的rank，效果也很好
- ![](https://pic2.zhimg.com/80/v2-8e92d2e2f256e7d69226772e0083e9c5_1440w.webp)

1. DoRA在多个数据集上效果好于LoRA
2. DoRA对不同rank r取值更鲁棒

相信DoRA应该很快会成为一种普遍的大模型微调方法。

资料：
- DoRA: Weight-Decomposed Low-Rank Adaptation
- Improving LoRA: Implementing Weight-Decomposed Low-Rank Adaptation (DoRA) from Scratch

##### 【2024-3-28】LISA

LoRA（Low-Rank Adaptation）

LoRA是一种大模型微调技术，核心思想是在预训练的大型语言模型（PLM）基础上，通过增加一个低秩适配器来实现微调。这种方法通过在原始模型的每一层注入可训练的低秩矩阵，从而以较小的参数量实现模型的微调。

LoRA主要优势在于减少了微调过程中需要更新的参数数量，从而降低了存储和计算资源的需求。然而，LoRA在某些任务上可能无法超越全参数微调的效果，且其理论性质分析较为困难。

【2024-3-28】香港理工 LISA（Layerwise Importance Sampled AdamW）
- 论文: [LISA: Layerwise Importance Sampling for Memory-Efficient Large Language Model Fine-Tuning](https://arxiv.org/pdf/2403.17919.pdf)

LISA是由UIUC联合LMFlow团队提出的另一种大模型微调方法。
- 与LoRA不同，LISA算法核心在于**始终更新底层embedding和顶层linearhead**，同时**随机更新**少数中间的self-attention层。
- 这种方法在实验中显示出在指令微调任务上超过LoRA甚至全参数微调的效果。
- LISA的空间消耗与LoRA相当甚至更低，且由于其每次中间只会激活一小部分参数，对更深的网络和梯度检查点技术（GradientCheckpointing）也很友好，能够带来更大的空间节省。

此外，LISA的收敛性质比LoRA有很大提升（17~30%），且计算速度比LoRA快将近50%。

对比总结
- **微调效果**：LISA在某些任务上显示出比LoRA更好的微调效果，甚至能超越全参数微调。
- **资源消耗**：LISA在空间消耗上与LoRA相当，但由于其更新策略，可能在某些情况下更加节省资源。
- **计算速度**：LISA的计算速度比LoRA快，因为它减少了需要更新的参数数量。
- **理论分析**：LISA的理论性质相对容易分析，可以使用现有的优化领域的数学工具进行分析。
- **应用友好性**：LISA对更深的网络和梯度检查点技术更加友好，有助于在资源受限的情况下进行微调。

综上所述，LISA在保持与LoRA相当的资源消耗的同时，提供了更快的计算速度和更好的微调效果，是一种具有潜力的大模型微调技术。



##### 【2024-4-12】PiSSA

【2024-4-12】[改变LoRA的初始化方式，北大新方法PiSSA显著提升微调效果](https://www.jiqizhixin.com/articles/2024-04-12-7)

北京大学的研究团队提出了一种名为 PiSSA 的参数高效微调方法，主流数据集上都超过了目前广泛使用的 LoRA 的微调效果。
- 论文: [PiSSA: Principal Singular Values and Singular Vectors Adaptation of Large Language Models](https://arxiv.org/pdf/2404.02948.pdf)
- 代码链接: [PiSSA](https://github.com/GraphPKU/PiSSA)

PiSSA 在模型架构上和 LoRA 完全一致，只是**Adapter初始化方式**不同。[img](https://image.jiqizhixin.com/uploads/editor/cf318bea-5793-4f34-83a3-ecc1bc7d7773/640.png)
- `LoRA` 使用高斯噪声初始化 A，使用 0 初始化 B。
- `PiSSA` 用主奇异值和奇异向量 (Principal Singular values and Singular vectors) 来初始化 Adapter 来初始化 A 和 B。
- ![](https://image.jiqizhixin.com/uploads/editor/cf318bea-5793-4f34-83a3-ecc1bc7d7773/640.png)

效果
- PiSSA 微调效果显著超越了 LoRA，甚至超越了全参数微调
- PiSSA 比 LoRA 收敛更快，最终效果更好，唯一的代价仅是需要几秒的 SVD 初始化过程。


##### 【2024-4-15】LoRA Dropout

LoRA Dropout, PKU
- 论文: [LoRA Dropout as a Sparsity Regularizer for Overfitting Control]()

1. 训练阶段对A和B矩阵进行整行或整列的dropout，而不是element-wise的dropout，这样可以使得BA中有大量为0值，达到mask W的效果
2. inference时，无法像原始dropout那样乘以(1-p)来rescale。因此需多次使用dropout，取ensemble的结果，效果有提升(效率降低)

效果
1. +dropout在lora和adalora上效果均更好
2. Dropout rate取0.6时效果最好


##### 【2024-6-18】LoRA-drop

哈工大
- 论文: [LoRA-drop: Efficient LoRA Parameter Pruning based on Output Evaluation](https://arxiv.org/pdf/2402.07721)

1. LoRA在不同位置(针对不同W)的 $$||\Delta Wx||$$ 不同，认为越大的越重要
2. 按以下步骤将不重要的LoRA进行权重共享，然后重新训练，减少训练参数，不减少计算量


效果与lora差不多，可减少lora约一半的内存占用



#### 工程优化


##### 【2023-11-15】S-LoRA 多服务部署

【2023-11-15】S-LoRA：一个GPU运行数千大模型成为可能

大语言模型部署都会采用「预训练 — 微调」模式。但是，针对众多任务（如个性化助手）对 base 模型进行微调时，训练和服务成本会变得非常高昂。

低秩适配（LowRank Adaptation，LoRA）是一种参数效率高的微调方法，通常用于将 base 模型适配到多种任务中，从而产生了大量从一个 base 模型衍生出来的 LoRA 适配程序。

只对适配器权重进行微调，就能获得与全权重微调相当的性能。虽然这种方法可以实现单个适配器的低延迟推理和跨适配器的串行执行，但在同时为多个适配器提供服务时，会显著降低整体服务吞吐量并增加总延迟。总之，如何大规模服务于这些微调变体的问题仍未得到解决。

UC 伯克利、斯坦福等高校的研究者提出了一种名为 S-LoRA 的新微调方式。
- 论文地址：[https://arxiv.org/pdf/2311.03285.pdf](https://arxiv.org/pdf/2311.03285.pdf)
- 项目地址：[https://github.com/S-LoRA/S-LoRA](https://github.com/S-LoRA/S-LoRA)

S-LoRA 专为众多 LoRA 适配程序的可扩展服务而设计，它将所有适配程序存储在主内存中，并将当前运行查询所使用的适配程序取到 GPU 内存中。
- S-LoRA 提出「**统一分页**」（Unified Paging）技术，即使用统一的内存池来管理不同等级的动态适配器权重和不同序列长度的 KV 缓存张量。
  - PagedAttention 扩展为**统一分页**（Unified Paging），后者除了管理 KV 缓存外，还管理适配器权重。
- 此外，S-LoRA 还采用了新的**张量并行**策略和高度优化的定制 CUDA 内核，以实现 LoRA 计算的异构批处理。

S-LoRA 包含三个主要创新部分。论文第 4 节介绍了批处理策略，该策略分解了 base 模型和 LoRA 适配器之间的计算。此外，研究者还解决了需求调度的难题，包括适配器集群和准入控制等方面。跨并发适配器的批处理能力给内存管理带来了新的挑战。第 5 节，研究者将 PagedAttention 推广到 Unfied Paging，支持动态加载 LoRA 适配器。这种方法使用统一的内存池以分页方式存储 KV 缓存和适配器权重，可以减少碎片并平衡 KV 缓存和适配器权重的动态变化大小。最后，第 6 节介绍了新的张量并行策略，能够高效地解耦 base 模型和 LoRA 适配器。

如果将 LoRA 适配器存储在主内存中，数量可能会很大，但当前运行批所需的 LoRA 适配器数量是可控的，因为批大小受 GPU 内存的限制。为了利用这一优势，研究者将所有的 LoRA 适配卡都存储在主内存中，并在为当前正在运行的批进行推理时，仅将该批所需的 LoRA 适配卡取到 GPU RAM 中。在这种情况下，可服务的适配器最大数量受限于主内存大小。
- ![](https://pic1.zhimg.com/80/v2-02ad431025559544cb5e501d7d44ffc4_1440w.webp)

这些功能使 S-LoRA 能够以较小开销在单个 GPU 或多个 GPU 上为数千个 LoRA 适配器提供服务（同时为 2000 个适配器提供服务），并将增加的 LoRA 计算开销降至最低。相比之下，vLLM-packed 需要维护多个权重副本，并且由于 GPU 内存限制，只能为少于 5 个适配器提供服务。

与 HuggingFace `PEFT` 和 `vLLM`（仅支持 LoRA 服务）等最先进的库相比，`S-LoRA` 吞吐量最多可提高 4 倍，服务适配器数量可增加几个数量级。因此，S-LoRA 能够为许多特定任务的微调模型提供可扩展的服务，并为大规模定制微调服务提供了潜力。


#### MoE+LoRA


##### LoRA + MoE

【2024-3-5】[大模型微调新范式：当LoRA遇见MoE](https://mp.weixin.qq.com/s/t_X8AHFgi-RHuviTuCYv0Q)

对比
- 原始版本的 LoRA，权重稠密，每个样本都会激活**所有参数**；
- 与混合专家（MoE）框架结合的 LoRA，每一层插入多个并行的 LoRA 权重（即 MoE 中的多个专家模型），路由模块（Router）输出每个专家的激活概率，以决定激活哪些 LoRA 模块。

为了克服**稠密模型**的参数效率瓶颈，以 Mistral、DeepSeek MoE 为代表的混合专家（Mixure of Experts，简称 MoE）模型框架。

模型某个模块（如 Transformer 的某个 FFN 层）存在多组形状相同的权重（称为专家），另外有一个**路由模块**（Router）接受原始输入、输出各专家的激活权重，最终的输出为：
- 如果是**软路由**（soft routing），输出各专家输出的**加权求和**；
- 如果是**离散路由**（discrete routing），即 Mistral、DeepDeek MoE 采用的**稀疏混合专家**（Sparse MoE）架构,则将 Top-K（K 为固定的 超参数，即每次激活的专家个数，如 1 或 2）之外的权重置零，再加权求和。

MoE 架构中每个专家参数的激活程度取决于数据决定的**路由权重**，使得各专家的参数能各自关注其所擅长的数据类型。在离散路由的情况下，路由权重在 TopK 之外的专家甚至不用计算，在保证总参数容量的前提下极大降低了推理的计算代价。

案例
- MoV、MoLORA、LoRAMOE 和 MOLA 等新的 PEFT 方法，相比原始版本的 LORA 进一步提升了大模型微调的效率。

详情
- `MoV` 和 `MoLORA`：
  - 2023 年 9 月，首个结合 PEFT 和 MoE 的工作，MoV 和 MoLORA 分别是 `IA` 和 `LORA` 的 MOE 版本，采用 token 级别的**软路由**（加权合并所有专家的输出）。
  - 对 3B 和 11B 的 T5 大模型的 SFT，MoV 仅使用不到 1% 可训练参数量就可以达到和全量微调相当的效果，显著优于同等可训练参数量设定下的 LoRA。
  - `MoLORA` 论文： [Pushing Mixture of Experts to the Limit: Extremely Parameter Efficient MoE for Instruction Tuning](https://arxiv.org/abs/2309.05444)
  - 结论
    1. 15个expert效果能超过full finetune
    2. expert不是越多越好，后面会收敛
    3. Soft router好于top-1/2，可能是由于top-1/2这种本身难于训练，样本还少
    4. 对于multi-task数据集，不同expert能focus在不同task上
- `LoRAMOE`：LoRA专家分组，预训练知识记得更牢
  - 问题：随着所用数据量的增长，SFT 训练会导致模型参数大幅度偏离预训练参数，预训练阶段学习到的世界知识（world knowledge）逐渐被遗忘，虽然模型的指令跟随能力增强、在常见的测试集上性能增长，但需要这些世界知识的 QA 任务性能大幅度下降
  - 2023 年 12 月，在 `MoLORA` 基础上，为解决微调大模型时的灾难遗忘问题，将同一位置的 LoRA 专家分为两组，分别负责保存预训练权重中的世界知识和微调时学习的新任务，并为此目标设计了新的负载均衡 loss。
  - [LoRAMoE: Revolutionizing Mixture of Experts for Maintaining World Knowledge in Language Model Alignment](https://arxiv.org/abs/2312.09979)
- `MOLA`：统筹增效，更接近输出端的高层需要更多专家
  - 问题: 专家个数过多容易导致性能下降
  - 2024 年 2 月，使用离散路由（每次只激活路由权重 top-2 的专家），并发现在每一层设置同样的专家个数不是最优的，增加高层专家数目、降低底层专家数目，能在可训练参数量不变的前提下，明显提升 LLaMa-2 微调的效果。
  - 模型的不同层添加不同数量的LoRA experts，越高层使用更多expert效果更好
  - 论文 [Higher Layers Need More LoRA Experts](https://arxiv.org/abs/2402.08562)
  - 相同总experts数的情况下，倒三角结构效果最好。越高层离output越近，参数就越重要（非MOE情况下，也是更高层的LoRA更重要）


#### 序列式 LoRA

相关工作
- Chain of LoRA
  - 论文: [Chain of LoRA: Efficient Fine-tuning of Language Models via Residual Learning](https://arxiv.org/pdf/2401.04151)
- ReLoRA: 
  - 论文: [ReLoRA: High-Rank Training Through Low-Rank Updates](https://arxiv.org/pdf/2307.05695)
  - 拟合更高秩的W
  - 效果: 实验结果好于LoRA
- PeriodicLoRA
  - 论文: [PeriodicLoRA: Breaking the Low-Rank Bottleneck in LoRA Optimization](https://arxiv.org/pdf/2402.16141)
- Delta-LoRA
  - 论文: [DELTA-LORA: FINE-TUNING HIGH-RANK PARAMETERS WITH THE DELTA OF LOW-RANK MATRICES](https://arxiv.org/pdf/2309.02411)
  - 比LoRA多一步：每次更新时，通过$$\textbf{AB}$$近似计算$$\Delta \textbf{W}$$，来对$$\textbf{W}$$进行更新
  - 实验结果好于LoRA




### MAM Adapter

一种在 Adapter、Prefix Tuning 和 LoRA 之间建立**联系**的统一方法。
- 最终的模型 MAM Adapter 是用于 FFN 的并行 **Adapter** 和 **软提示**的组合。

特点：
- 整体上来说，最终的模型MAM Adapter效果会优于单个高效微调方法。

### UniPELT

一种将不同的PELT方法LoRA、Prefix Tuning和Adapter作为子模块，并通过门控机制学习激活最适合当前数据或任务的方法。

特点：
- 相对于LoRA，BitFit，Prefix-tuning，训练的参数量更大；同时，推理更耗时；并且，输入会占用额外的序列长度。
- 多种 PELT 方法的混合涉及PLM 的不同部分对模型有效性和鲁棒性都有好处。

## (4) 全量微调

**全面微调**：使用任务特定数据调整LLM的所有参数。
- 一个较小、任务特定、带标签的数据集上进行微调，调整一些模型参数，优化其对特定任务或一组任务的性能
- 全面微调： 所有模型参数都被更新，使其类似于预训练，只不过是在一个**带标签**且**规模较小**的数据集上进行。
- ![](https://pic2.zhimg.com/80/v2-e8c7286930eb81b57aaf109fe92ac58d_1440w.webp)
- 优点: 训练数据集更少、提高精度、增加鲁棒性
- 缺点: 高计算成本、内存需求高、时间/专业知识密集



## (5) 混合


### LoRAMoE

【2024-3-8】[LoRAMoE: 把MoE用到Lora上](https://mp.weixin.qq.com/s/HaHRyztbWlNfNmz9JVgzBA)
复旦大学，2024年3月8号 publish 论文
- LoRAMoE: [Alleviate World Knowledge Forgetting in Large Language Models via MoE-Style Plugin](https://arxiv.org/abs/2312.09979)

MoE: 稀疏门控制的专家混合层介绍过MoE，在LoRA: 大语言模型的低秩适应介绍过Lora。这篇论文把MoE用到了Lora上。

动机
- 微调阶段的数据过多时，会让模型忘掉很多世界知识。

LoRA+MoE
- 做法很直接，在FFN层上，加了很多Lora分支，轻量级的expert。
- LoRAMoE 给不同的lora分支做**分流**时，加入了类型约束，即世界知识相关的任务，分到一组experts中，非世界知识相关的任务，分到剩下的experts中。
- 图见[原文](https://mp.weixin.qq.com/s/HaHRyztbWlNfNmz9JVgzBA)

### ReFT

【2024-4-13】ReFT：比现有PEFT微调更好的方法

斯坦福发表微调的论文
- 《ReFT: Representation Finetuning for Language Models》
- 一种新的语言模型微调方法——**表示微调**（ReFT）
- 该方法解决大型语言模型（LMs）微调成本高的问题，通过冻结基础模型上学习任务特定的隐藏表示干预来适应新任务。

ReFT通过定义一个干预函数，修改模型的**一小部分表示**，而不是修改权重，以此来控制模型的行为。

作为ReFT家族的一个强实例，Low-rank Linear Subspace ReFT（`LoReFT`）在低秩线性子空间中干预隐藏表示，比以往的参数高效微调（PEFT）方法更加高效。
- LoReFT通过在低秩投影矩阵定义的子空间内对隐藏表示进行编辑，学习如何通过干预引导模型进行准确预测。
- LoReFT在多个标准基准测试中进行评估，包括常识推理、算术推理、指令遵循和自然语言理解任务。
- LoReFT在上述多个基准测试中展示了出色的性能，LoReFT在保持与现有PEFTs相同或更好性能的同时，使用的参数比先前最先进的PEFTs少10倍至50倍。



### RAFT 

【2024-3-15】UC Berkeley 提出新方法 `RAFT` = `RAG` + `FT`
- [RAFT——针对特定领域的问答的微调和 RAG 方法](https://www.unite.ai/zh-CN/raft-a-fine-tuning-and-rag-approach-to-domain-specific-question-answering/)
- 介绍 [UC伯克利:提出索增强微调(RAFT)，只需少量微调，就能大幅提升模型领域QA能力](https://cloud.tencent.com/developer/article/2400661)
- 论文: [RAFT: Adapting Language Model to Domain Specific RAG](https://arxiv.org/pdf/2403.10131.pdf)
- 代码 [gorilla](https://github.com/ShishirPatil/gorilla)

将LLMs适应特定领域时两个候选方案：
- 1、通过RAG利用上下文学习
- 2、有监督的微调

分析: 当前微调方法要么测试期间不利用文档，要么忽略训练期间检索中的不完美之处。
- RAG允许模型回答问题时参考文档，但错过了从固定领域设置中学习和提前访问测试文档的机会。
- 有监督微调允许从文档中学习更广泛的模式，更好地与终端任务和用户偏好对齐。

因此，RAFT 将微调与RAG结合起来。通过RAFT，在有监督的情况下，可以为微调收集最佳结果。
- 同时具备 **闭卷考试** + **开卷考试**的能力
- ![](https://www.unite.ai/wp-content/uploads/2024/03/RAFT.png)

RAFT 与标准微调不同，训练数据包含**相关**和**不相关**文档问题，以及从相关文本得出的**思想链式**答案。
- 该方法旨在提高模型不仅**回忆**信息的能力，而且还提高内容中推理和得出答案的能力。

工具调用上超过GPT-4
- [Gorilla: Large Language Model Connected with Massive APIs](https://gorilla.cs.berkeley.edu/)
- 论文: [Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/pdf/2305.15334.pdf)

评测
- RAFT 始终优于基线，例如使用和不使用 RAG 的特定领域微调，以及使用 RAG 的 GPT-3.5 等更大的模型。
- HuggingFace 数据集上，RAFT 的准确率达到了 **74%**，比特定领域微调 (DSF) 显着提高了 **31.41%**，比带有 RAG 的 GPT-4 4.92 显着提高了 3.5%。
- HotpotQA 数据集上，与 DSF 相比，RAFT 的准确率提高了 **28.9%**。

RAFT 是一种适应LLMs的方法，用于从正面和负面文档集合中阅读解决方案。

这与标准的RAG设置形成对比，在标准的RAG设置中，模型是使用检索器输出进行训练的，包括记忆和阅读。


## 应用经验


方法选择
- 大模型应用：先看**大模型**是否能实现，然后再考虑**小模型**加速；
- 简单链路保证**性能**，复杂链路保证**效果**


# 结束