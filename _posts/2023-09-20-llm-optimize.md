---
layout: post
title:  大模型推理优化 LLM Inference
date:   2023-09-20 22:46:00
categories: 大模型
tags: gpt 量化 vllm deepspeed 推理 推测解码 sglang 多模态
excerpt: 如何提升LLM推理效率？
mathjax: true
permalink: /llm_opt
---

* content
{:toc}


# LLM 推理优化

基于 Transformer 架构的大语言模型 (LLM) 在全球范围内引发了深度的技术关注，并取得了令人瞩目的成就。其强大的理解和生成能力，正在深刻改变对人工智能的认知和应用。

然而，大语言模型的<span style='color:blue'>推理应用成本过高</span>，高昂的成本，大大阻碍了技术落地。

优化推理性能不仅可以减少硬件成本，还可以提高模型的实时响应速度。它使模型能够更快速地执行自然语言理解、翻译、文本生成等任务，从而改善用户体验，加速科学研究，推动各行业应用的发展。

参考
- 【2023-8-30】[LLM七种推理服务框架总结](https://zhuanlan.zhihu.com/p/653352979)
- 【2023-8-17】[LLM 的推理优化技术纵览](https://zhuanlan.zhihu.com/p/642412124)


## LLM 推理

【2024-3-30】[图解大模型计算加速系列之：vLLM核心技术PagedAttention原理](https://mp.weixin.qq.com/s/oCGENfMwTNmfr1nGeCZz2g)

LLM 推理过程分两个阶段: `prefill` 和 `decode`, 通常用 KV cache 技术加速推理
- `Prefill`: **预填充**阶段, 把整段 prompt 喂给模型, 做forward计算。
  - 如果采用 `KV cache` 技术，会把prompt过 Wk,Wv 后得到的 Xk,Xv 保存在 cache_k 和 cache_v中。对后面的token计算attention时，就不需要对前面的token重复计算,节省推理时间。
  - 例如假设prompt中含有3个token，prefill阶段结束后，这三个token相关的KV值都被装进了cache
- `Decode`: **生成response**。根据prompt的prefill结果，逐个token生成response。
  - 如果采用 KV cache, 则每走完一个decode过程，就把对应response token的KV值存入cache中，以便能加速计算。
  - 例如 t4与cache中t0~t3的KV值计算完attention后，就把自己的KV值也装进cache中。对t6也是同理。

为什么不能一个阶段做完？

Prefill与Decode两个阶段的**输入特性**和**计算方式**本质不同，拆成两个阶段可以精准优化每步计算路径
- Prefill可用 `Flash Attention` 等并行技术提升性能
- Decode可用`KV Cache`、`speculative decoding`等加速

推理过程里，Prefill和Decode阶段不仅在结构式不同，在性能瓶颈上也大相径庭

<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36\&quot; version=\&quot;24.7.16\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;YUrH7kkdw6S7EPocWAtV\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;785\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-33\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;dashed=1;dashPattern=1 1;fillColor=#e1d5e7;strokeColor=#9673a6;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;287.29\&quot; y=\&quot;110\&quot; width=\&quot;430.59\&quot; height=\&quot;80\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-29\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;594.81\&quot; y=\&quot;221\&quot; width=\&quot;185.19\&quot; height=\&quot;113\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-28\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;444.11\&quot; y=\&quot;217\&quot; width=\&quot;135.89\&quot; height=\&quot;113\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6DHZA2WNbksqPKNvCXTy-4\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;304\&quot; y=\&quot;222\&quot; width=\&quot;110.59\&quot; height=\&quot;104\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;lHimWeaf7UQe36nZpLsc-2\&quot; value=\&quot;LLM 推理\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=17;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;548.88\&quot; y=\&quot;30\&quot; width=\&quot;100\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;lHimWeaf7UQe36nZpLsc-12\&quot; value=\&quot;&amp;lt;font style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;t0~t2&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontSize=15;fontColor=#333333;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;339.4099999999999\&quot; y=\&quot;120\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;lHimWeaf7UQe36nZpLsc-30\&quot; value=\&quot;wqw547243068@163.com&amp;lt;br&amp;gt;2024-09-26\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;770.0000000000001\&quot; y=\&quot;360\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6DHZA2WNbksqPKNvCXTy-65\&quot; value=\&quot;Prompt\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontSize=14;fontColor=#0000FF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;334.40999999999997\&quot; y=\&quot;74\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6DHZA2WNbksqPKNvCXTy-66\&quot; value=\&quot;&amp;lt;font&amp;gt;逐个token生成&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontSize=14;fontColor=#FF3399;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;529.41\&quot; y=\&quot;76\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;6DHZA2WNbksqPKNvCXTy-67\&quot; value=\&quot;\&quot; style=\&quot;shape=flexArrow;endArrow=classic;html=1;rounded=0;fillColor=#e1d5e7;strokeColor=#9673a6;\&quot; parent=\&quot;1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;436.94000000000005\&quot; y=\&quot;90\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;499.4100000000001\&quot; y=\&quot;90\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-30\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;XopzI3mGYhy0IdQWerKT-1\&quot; target=\&quot;6DHZA2WNbksqPKNvCXTy-4\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-1\&quot; value=\&quot;Prefill\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;300\&quot; y=\&quot;150\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-2\&quot; value=\&quot;Decode\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;424.41\&quot; y=\&quot;150\&quot; width=\&quot;55.59\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-31\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;XopzI3mGYhy0IdQWerKT-3\&quot; target=\&quot;XopzI3mGYhy0IdQWerKT-28\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-3\&quot; value=\&quot;Decode\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;484.41\&quot; y=\&quot;150\&quot; width=\&quot;55.59\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-4\&quot; value=\&quot;Decode\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;545.09\&quot; y=\&quot;150\&quot; width=\&quot;55.59\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-32\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;XopzI3mGYhy0IdQWerKT-5\&quot; target=\&quot;XopzI3mGYhy0IdQWerKT-29\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-5\&quot; value=\&quot;Decode\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;605.09\&quot; y=\&quot;150\&quot; width=\&quot;55.59\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-6\&quot; value=\&quot;&amp;lt;font style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;t3&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontSize=15;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;434.4099999999999\&quot; y=\&quot;120\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-7\&quot; value=\&quot;&amp;lt;font style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;t4&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontSize=15;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;485.5299999999999\&quot; y=\&quot;120\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-8\&quot; value=\&quot;&amp;lt;font style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;t5&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontSize=15;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;545.0899999999999\&quot; y=\&quot;120\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-9\&quot; value=\&quot;&amp;lt;font style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;t6&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontSize=15;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;605.0899999999999\&quot; y=\&quot;120\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-10\&quot; value=\&quot;t0\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;323.41\&quot; y=\&quot;230\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-11\&quot; value=\&quot;t1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;345.41\&quot; y=\&quot;230\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-12\&quot; value=\&quot;t2\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;367.41\&quot; y=\&quot;230\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-13\&quot; value=\&quot;&amp;lt;font style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;KV Cache&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontSize=15;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;313.4099999999999\&quot; y=\&quot;326\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-14\&quot; value=\&quot;t0\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;457.41\&quot; y=\&quot;230\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-15\&quot; value=\&quot;t1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;479.41\&quot; y=\&quot;230\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-16\&quot; value=\&quot;t2\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;501.41\&quot; y=\&quot;230\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-17\&quot; value=\&quot;&amp;lt;font style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;KV Cache&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontSize=15;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;467.2099999999999\&quot; y=\&quot;330\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-18\&quot; value=\&quot;t4\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;546.88\&quot; y=\&quot;230\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-19\&quot; value=\&quot;t0\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;605.09\&quot; y=\&quot;234\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-20\&quot; value=\&quot;t1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;627.09\&quot; y=\&quot;234\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-21\&quot; value=\&quot;t2\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;649.09\&quot; y=\&quot;234\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-22\&quot; value=\&quot;&amp;lt;font style=&amp;quot;font-size: 15px;&amp;quot;&amp;gt;KV Cache&amp;lt;/font&amp;gt;\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=1;fontSize=15;fontColor=#333333;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;640.6999999999999\&quot; y=\&quot;334\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-23\&quot; value=\&quot;t6\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;741.7\&quot; y=\&quot;234\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-24\&quot; value=\&quot;t3\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;672.52\&quot; y=\&quot;234\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-25\&quot; value=\&quot;t3\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;523.88\&quot; y=\&quot;230\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-26\&quot; value=\&quot;t4\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;694.88\&quot; y=\&quot;234\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;XopzI3mGYhy0IdQWerKT-27\&quot; value=\&quot;t5\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;textShadow=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;717.88\&quot; y=\&quot;235\&quot; width=\&quot;20\&quot; height=\&quot;90\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



由于 Decode 阶段逐一生成token，因此不能像 prefill 阶段那样能**做大段prompt的并行计算**

所以, LLM推理过程中，Decode阶段的耗时一般是更大的。

用 KV cache 推理时的一些特点：
- 随着prompt数量变多和序列变长，KV cache也变大，对gpu显存造成压力
- 由于输出序列长度无法预先知道，所以很难提前为KV cache量身定制存储空间

13B模型在A100 40GB gpu 推理时, 显存占用分配
- Parameters 参数 占 26GB, 65%
- KV Cache 占比**超过 30%**
- 其余是 others, 表示 forward过程中产生的activation 大小，这些activation 转瞬即逝，用完则废，因此占据的显存不大

直观感受到推理中 KV cache 对显存的占用。

因此，如何优化KV cache，节省显存，提高推理吞吐量，就成了LLM推理框架需要解决的重点问题。


## 训练 vs 推理

AI工程分两个阶段：**训练** 和 **推理**
- 训练、推理截断对算力需求完全不同

训练 vs 推理

|维度|第一阶段: 训练|第二阶段: 推理||
|---|---|---|---|
|计算能力|数据吞吐量大，百亿/千亿参数达数TB-PB|数据吞吐量小||
|计算能力|密集计算|持续计算||
|计算时间|几天-几周/几月|常态，贯穿日常业务||
|时延|允许延迟|低延迟||


## 指标

LLM 推理服务评估指标：
- 首词元(token)时间（Time to First Token）：接收提示后多久，才返回第一个词元？
- 生成**时延**（Generation Latency）：接收提示后多久才返回最终词元？
- **吞吐量**（Throughput）：能够同时通过pipeline传递多少个不同的生成？
- 硬件**利用率**（Hardware Utilization）：在多大程度上有效地利用计算、内存带宽和硬件的其他能力？

重点关注两个指标：`吞吐量`和`时延`：
- `吞吐量`：从系统角度来看，即系统在单位时间内能处理的 tokens 数量。计算方法为系统处理完成的 tokens 个数除以对应耗时，其中 tokens 个数一般指输入序列和输出序列长度之和。吞吐量越高，代表 LLM 服务系统的资源利用率越高，对应的系统成本越低。
- `时延`：从用户视角看，即用户平均收到每个 token 所需位时间。计算方法为用户从发出请求到收到完整响应所需的时间除以生成序列长度。一般来讲，当时延不大于 50 ms/token 时，用户使用体验会比较流畅。

`吞吐量`关注系统**成本**，高`吞吐量`代表系统单位时间处理的请求大，系统利用率高。`时延`关注用户使用体验，即返回结果要快。

这两个指标一般相互影响，因此需要**权衡**。
- 提高`吞吐量`的方法一般是提升 batchsize，将用户请求由**串行**改为**并行**。
- 但 batchsize 的增大会在一定程度上损害每个用户的`时延`，因为以前只计算一个请求，现在合并计算多个请求，每个用户等待的时间变长。

模型小型化关注：模型**平均推理时间**和**功耗**
- 平均推理时间: 用 `latency` 或 `throughput` 来衡量
- 功耗: 用参考生成token过程中所用到GPU的功耗来近似(因为TP/PP等方法就会引入多个GPU). 

这两个指标都与**模型参数量**紧密相关, 特别是LLMs参数量巨大, 导致部署消耗GPU量大(而且甚至会引起旧GPU, 如: 
- 2080ti等消费级卡直接下线离场)及GPU的IO时间长(memory write/read 的cycles是要远大于 operations cycles, 印象中是百倍)

部署过程中如何使得模型变得更小更轻且保持智能尽可能不下降就成了一个重要的研究话题。

## 总结

LLM 推理性能优化主要以提高吞吐量和降低时延为目的，具体可以划分为如下六部分
- ![](https://pic4.zhimg.com/80/v2-0f1af7fc08fa6ef9046b88cc3bde6b87_1440w.webp)
- `显存优化`
  - KV Cache: 不影响任何计算精度的前提下，通过空间换时间思想，提高推理性能。业界主流 LLM 推理框架均默认支持并开启了该功能。
  - Page Attention
    - LLM 推理服务的吞吐量指标主要受制于显存限制
    - 现有系统由于缺乏精细的显存管理方法而浪费了 60% 至 80% 的显存，浪费的显存主要来自 KV Cache
- `计算优化`
  - 算子融合：减少计算过程中的访存次数和 Kernel 启动耗时达到提升模型推理性能
  - 高性能算子：针对 LLM 推理运行热点函数编写高性能算子，也可以降低推理时延，包含 GEMM 操作优化 和 GEMV 操作优化
- `服务优化`
  - 服务相关优化主要包括：Continuous Batching、Dynamic Batching 和 异步 Tokenize / Detokenize
  - Continuous Batching 和 Dynamic Batching 主要围绕提高可**并发**的 batchsize 来提高吞吐量
  - 异步 Tokenize / Detokenize 则通过**多线程**方式将 Tokenize / Detokenize 执行与模型推理过程时间交叠，实现降低时延目的。
- `分布式优化`
  - 模型参数量较大，可能无法存放到单一计算设备中，分布式并行可以有效解决
  - 分布式并行中的模型并行和流水线并行已在 LLM 推理中得到应用
- `低比特量化`
  - 低比特量化可以降低**显存**占用量和访存量，关键在于节省显存量和访存量以及**量化计算**的加速**远大于**反量化带来的额外开销。
- 其他新技术
  - `投机采样`（Speculative decoding）针对 LLM 推理串行解码特点，通过引入一个近似模型来执行串行解码，原始模型执行并行评估采样，通过近似模型和原始模型的互相配合，在保证精度一致性的同时降低了大模型串行解码的次数，进而降低了推理时延。
  - `美杜莎头`（Medusa head）则是对投机采样的进一步改进，其摒弃了近似模型，在原始模型结构上新增了若干解码头，每个解码头可并行预测多个后续 tokens，然后使用基于树状注意力机制并行处理，最后使用典型接收方案筛选出合理的后续 tokens。该方法同样降低了大模型串行解码的次数，最终实现约两倍的时延加速。

生产环境大语言模型优化 -- [Optimizing your LLM in production](https://huggingface.co/blog/optimize-llm)
- 部署大规模语言模型(LLM)需要应对计算和内存需求，关键是提高模型在长文本输入下的计算和内存效率。   
- 降低参数精度，如8比特或4比特量化，可以减少内存需求，仅轻微影响性能。   
- Flash Attention算法可以线性提高内存利用率，并加速计算，是默认自注意力的更高效替代。   
- 相对位置Embedding如ALiBi和RoPE可以更好处理长文本输入，并支持长度外推。   
- 关键值cache机制可以重复使用先前计算，减少计算量，对会话等任务尤其重要。   
- MQA和GQA通过共享键值投影或分组，可以显著减少cache内存需求。   
- Falcon、PaLM、LLAMA等新模型设计都采用了这些优化技术，以支持长文本场景。   
- 持续研究工作致力于进一步提升大模型计算和内存效率，部署LLM仍面临挑战。选择合适的算法和模型架构十分关键。


## 解码原理

大模型推理本质上串行，逐字预测
- ![](https://pic1.zhimg.com/80/v2-fe0e1038d6f3b3b5fe10eef22d894ec4_1440w.webp)

[llama 7B模型结构](https://zhuanlan.zhihu.com/p/628511161)
- ![](https://pic1.zhimg.com/v2-8fb8e3d7da3af3bc7dc3d250be1cd060_r.jpg)


### generate 函数

【2023-12-18】
- [How to make LLMs go fast](https://vgel.me/posts/faster-inference/), 译文 [语言大模型推理加速指南](https://www.jiqizhixin.com/articles/2024-02-14-2)

```py
def generate(prompt: str, tokens_to_generate: int) -> str:
    tokens = tokenize(prompt)
    for i in range(tokens_to_generate):
        next_token = model(tokens)
        tokens.append(next_token)
    return detokenize(tokens)
```

generate 函数
- (1) **单次生成**: 原版, 一次向模型传递一个序列，并在每个step附加一个词元
- (2) **批次生成**: 改为一次向模型传递**多个**序列，同一前向传递中为每个序列生成一个补全（completion）
  - 批处理序列允许模型权重同时用于多个序列，所以将整个序列批次一起运行所需的时间比分别运行每个序列所需的时间少。
  - 问题: 整个batch未完成时,已完成的序列还要被迫继续生成随机词元，然后截断，浪费 GPU 资源
- (3) **连续批次生成**: 将新序列插入批次来解决这一问题，插入位置是 `[end]` 词元之后，注意力掩码机制来防止该序列受到上一序列中词元的影响

GPT-2 生成下一个词元的情况：
- 20 个词元 x 1 个序列 = 约 70 毫秒
- 20 个词元 x 5 个序列 = 约 220 毫秒（线性扩展约 350 毫秒）
- 20 个词元 x 10 个序列 = 约 400 毫秒（线性扩展约 700 毫秒）

```sh
# 单次生成
"Mark is quick. He"
"Mark is quick. He moves"
"Mark is quick. He moves quickly."
"Mark is quick. He moves quickly.[END]"
# 批次生成
"Mark is quick. He moves"
"The Eiffel Tower is"
"I like bananas, because they"
# 1
"Mark is quick. He moves quickly"
"The Eiffel Tower is in"
"I like bananas, because they have"

# 单次生成

```

![](https://image.jiqizhixin.com/uploads/editor/ef2cb6fe-34aa-4097-92cd-af28c83a1ba6/640.png)

详见站内专题: [文本生成之序列解码](text_decoding)


### 多模态

相较于普通语言模型，多模态模型会
- 输入的 token list里把多模态数据空出来，正常embedding变成token feature
- 同时把原始图像pixel 数据经过 VisionTransformer模型（通常说的VIT模型）转化为image feature
- 最后把 token feature和image feature拼接起来，变成普通的LLM模型输入。

图解
- ![](https://pic3.zhimg.com/v2-7a6dfe0828694fba1116a9986c9f566c_r.jpg)

[vllm 实现细节](https://zhuanlan.zhihu.com/p/1934611930389147672)

### 优化

大模型推理优化
- 大模型**重复**之前计算过的词向量
  - mask机制，前边词向量不会受到后边词向量影响。
  - 解法: 缓存已计算过的k,v
  - 示例: transofrmers（hugging face）库实现了这种推理加速，LlamaAttention类中，通过past_key_value这个变量保存计算过的某个词向量
- 降低**模型精度**
  - 从float32降低到float16，预测效果并不会下降很多，但是推理速度会快两倍


## 硬件加速 

直截了当的方法（尤其有风险投资) ：
- 购买更好的硬件, GPU/TPU
- 如果负担不起，就充分利用已有硬件。

### cpu 传输

注意: 
- CPU和加速器之间存在传输瓶颈
  - 如果模型不适应加速器内存，前向传递过程中将被交换出去，显著降低速度。
  - 这是苹果M1/M2/M3芯片在推理方面表现突出的原因之一，因为有统一的CPU和GPU内存。
- 无论是CPU还是加速器推理，都要先考虑是否充分利用了硬件
  - 经过适当优化的程序可从较差硬件中获得更多收益，而未充分优化的程序尽管使用了最好的硬件，获得的收益可能还不如前者。

### kernel 加速

示例

PyTorch 编写注意力
- `F.softmax(q @ k.T / sqrt(k.size(-1)) + mask) @ v` ，可以得到正确结果。
- 但改用 `torch.nn.functional.scaled_dot_product_attention`，将在可用时将计算委托给 FlashAttention，从而通过更好地利用缓存的手写kernel实现**3倍**加速。

### 编译器

更为通用的是 torch.compile、TinyGrad 和 ONNX 这样的编译器，将简单的Python代码融合成为针对你的硬件进行优化的kernel。

类似 torch.compile 这样的工具是优化代码、提升硬件性能的绝佳选择，而无需使用CUDA以传统方式编写kernel。



## 加速框架


### 总结

【2025-5-8】韩国 [25种LLM部署框架你知道多少？](https://zhuanlan.zhihu.com/p/1933217002698306629)
- 论文：《[A Survey on Inference Engines for Large Language Models: Perspectives on Optimization and Efficiency](https://arxiv.org/pdf/2505.01658)》  

总结了目前市面上的 LLM 的推理框架，总共有 25 个，我们来看看它们之间的优劣。

技术分类：
- 批处理（动态批、连续批、nano批等）
- 并行策略（数据并行、流水线并行等）
- 模型压缩（量化、剪枝、稀疏优化）
- 缓存机制（KV缓存、Prefix缓存等）
- 注意力机制优化（FlashAttention等）
- 推理采样与结构化输出（Speculative decoding、格式约束）

实践意义：
- 对25种开源及商业推理引擎进行了详尽比较，涵盖如 vLLM、TensorRT-LLM、GroqCloud 等。
- 提供持续更新的公共资源库：[Awesome LLM Inference Engine](https://github.com/sihyeong/Awesome-LLM-Inference-Engine)
- 指出未来方向，如更复杂服务支持、多硬件适配、安全性增强等。


总结
- star数：ollama、llama.cpp、vllm（低代码低成本部署还是广受大众喜欢）。
- 综合角度：vllm 遥遥领先。
- 文档完整性：vllm、Deepspeed-fastgen、tensorrt-llm比较完备
- 硬件支持度：Ollama、LLaMA.cpp、MAX、MLC-LLM
- 多级部署：vllm、sglang、lmdeploy
- 优化技巧全面度：vLLM、DeepSpeed-FastGen、SGLang、TensorRT-LLM

决策
- 生产环境，推荐vllm和sglang，支持的模型多，社区活跃，文档也详细。
- 自己玩且资源不够的话，推荐 ollama、llama.cpp、ktransformer。
- 不想自己部署，直接用各大公司的在线版本完事。


## 推理框架


### LLM 推理

大模型训好了，如何部署到线上？如何支持多用户高并发调用+快速响应？

方法
- （1）直接上 Hugging Face 的 transformers + FastAPI 写个demo
  - 实战时，要实现 batching、kv-cache、流式输出，简陋方案立马崩溃。
  - vLLM 和 SGLang，正是为了解决这些痛点而生。
- （2）vLLM
- （3）SGLang

如果 vLLM 是“高性能、低干预”的自动化服务员，那 SGLang 是“懂编程的服务机器人”

选型
- ToC AI 应用开发者，做对话助手、智能客服、内容生成平台之类，SGLang 灵活性省掉不少“拼 prompt、加钩子、加中间件”的麻烦。
- 模型 API 服务、对标 OpenAI SaaS 接口，vLLM 绝对是业内“吞吐率/稳定性”数一数二。

没有最好，只有合适，一切都要以公司业务为主

作者：[Trancy Wang](https://www.zhihu.com/question/666943660/answer/1914348903668651349)


### LLM 推理框架

【2024-7-15】本地部署运行私有的开源大型语言模型（LLMs）的方法
- Hugging Face 的 `Transformers` 
- `Llama.cpp` 基于C++的推理引擎，专为Apple Silicon打造，能够运行Meta的Llama2模型。
  - 在GPU和CPU上的推理性能均得到优化。
  - 优点: 高性能，支持在适度的硬件上运行大型模型（如Llama 7B），并提供绑定，允许您使用其他语言构建AI应用程序。
  - 缺点: 模型支持有限，且需要构建工具。
- `Llamafile`
  - Mozilla开发的C++工具，基于llama.cpp库，为开发人员提供了创建、加载和运行LLM模型所需的各种功能。
  - 简化了与LLM的交互，使开发人员能够轻松实现各种复杂的应用场景。
  - 优点: 速度与Llama.cpp相当，并且可以构建一个嵌入模型的单个可执行文件。
  - 由于项目仍处于早期阶段，不是所有模型都受支持，只限于Llama.cpp支持的模型。
- `Ollama`
  - Llama.cpp 和 Llamafile的用户友好替代品，Ollama提供了一个可执行文件，可在机器上安装一个服务。
  - 安装完成后，只需简单地在终端中运行即可。
  - 优点在于易于安装和使用，支持llama和vicuña模型，并且运行速度极快。
  - Ollama的模型库有限，需要用户自己管理模型
- `vLLM`
  - 高吞吐量、内存高效的大型语言模型（LLMs）推理和服务引擎。
  - 目标: 为所有人提供简便、快捷、经济的LLM服务。
  - vLLM的优点: 高效的服务吞吐量、支持多种模型以及内存高效。
  - 然而，为了确保其性能，用户需要确保设备具备GPU、CUDA或RoCm。
- `TGI`（Text Generation Inference）
  - HuggingFace 推出的大模型**推理部署**框架，支持主流大模型和量化方案。
  - TGI结合Rust和Python，实现服务效率和业务灵活性的平衡。具备许多特性，如简单的启动LLM、快速响应和高效的推理等。
  - 通过TGI，用户可以轻松地在本地部署和运行大型语言模型，满足各种业务需求。经过优化处理的TGI和Transformer推理代码在性能上存在差异，这些差异体现在多个层面：
  - **并行计算**能力：TGI与Transformer均支持并行计算，但TGI更进一步，通过Rust与Python的联合运用，实现了服务效率与业务灵活性的完美平衡。这使得TGI在处理大型语言模型时，能够更高效地运用计算资源，显著提升推理效率。
  - 创新**优化策略**：TGI采纳了一系列先进的优化技术，如Flash Attention、Paged Attention等，这些技术极大地提升了推理的效率和性能。而传统的Transformer模型可能未能融入这些创新优化。
  - **模型部署**支持：TGI支持GPTQ模型服务的部署，使我们能在单卡上运行启用continuous batching功能的更大规模模型。传统的Transformer模型则可能缺乏此类支持。
  - 尽管TGI在某些方面优于传统Transformer推理，但并不意味着应完全放弃Transformer推理。在特定场景下，如任务或数据与TGI优化策略不符，使用传统Transformer推理可能更合适。当前测试表明，TGI的推理速度暂时逊于vLLM。TGI推理支持以容器化方式运行，为用户提供了更为灵活和高效的部署选项。
- `DeepSpeed`
  - 微软精心打造的开源深度学习优化库，以**系统优化和压缩**为核心，深度优化硬件设备、操作系统和框架等多个层面，更利用模型和数据压缩技术，极大提升了大规模模型的推理和训练效率。
  - DeepSpeed-Inference，作为DeepSpeed在推理领域的扩展，特别针对大语言模型设计。它巧妙运用模型并行、张量并行和流水线并行等技术，显著提升了推理性能并降低了延迟。

如何选择？
- 追求**高性能**推理: `DeepSpeed` 。独特的ZeRO（零冗余优化器）、3D并行（数据并行、模型并行和流水线并行的完美融合）以及1比特Adam等技术，都极大提高了大模型训练和推理的效率。
- **易用**: `ollama` 。简洁的命令行界面，让模型运行变得轻松自如。
- 创建嵌入模型的**单个可执行文件**: `Llamafile` 。便携性和单文件可执行的特点，让人赞不绝口。
- **多种硬件环境**下高效推理: `TGI`。其模型并行、张量并行和流水线并行等优化技术，确保了大模型推理的高效运行。
- 复杂的**自然语言处理任务**，如机器翻译、文本生成等: 基于`Transformer`的模型。其强大的表示能力，轻松捕捉文本中的长距离依赖关系。
- **大规模**的自然语言处理任务，如文本分类、情感分析等: `vLLM`。作为大规模的预训练模型，它在各种NLP任务中都能展现出色的性能。


### 推理极限

【2024-4-23】[大模型推理的极限：理论分析、数学建模与 CPU/GPU 实测](https://arthurchiao.art/blog/llm-inference-speed-zh/)
- [LLM inference speed of light](https://zeux.io/2024/03/15/llm-inference-sol/)

[calm](https://github.com/zeux/calm) 是一个基于 CUDA、完全从头开始编写的轻量级 transformer-based language models 推理实现
- RTX 4090 上 calm 使用 16 位权重时达到 ~15.4 ms/tok，使用 8 位权重时达到 ~7.8 ms/tok， 达到了理论极限的 90%。
- Apple M2 Air 上使用 CPU 推理时，calm 和 llama.cpp 只达到理论 100 GB/s 带宽的 ~65%， 然后带宽就上不去了，这暗示需要尝试 Apple iGPU 了。
- 推导细节 [sol.ipynb](https://github.com/zeux/calm/blob/main/tools/sol.ipynb)

推理过程并未充分利用算力（ALU）。 需要重新平衡 FLOP:byte 比例， [speculative decoding](https://medium.com/@TitanML/in-the-fast-lane-speculative-decoding-10x-larger-model-no-extra-cost-f33ea39d065a) 等技术试图部分解决这个问题。

### GPT-Fast

这几年，有一堆文本生成的开源项目 llama.cpp, vLLM, 和 MLC-LLM. 为了更加使用方便，长城要求模型转成特殊格式、增加新依赖。

纯pytorch框架上的transformer推理能有多快？

【2023-12-3】PyTorch 团队纯用 Pytorch写个推理框架 [GPT-Fast](https://github.com/pytorch-labs/gpt-fast) ，极小推理框架，大约1000多行代码，号称性能最高提升**10倍**。
- [accelerating-generative-ai](https://pytorch.org/blog/accelerating-generative-ai-2/)

We leverage a breadth of optimizations including:
- `Torch.compile`: A compiler for PyTorch models
- `GPU quantization`: Accelerate models with reduced precision operations
- `Speculative Decoding`: Accelerate LLMs using a small “draft” model to predict large “target” model’s output
- `Tensor Parallelism`: Accelerate models by running them across multiple devices.

做法简单：
- 做了个最简版的 `kvcache`(避免重复计算) + `GPTQ`量化（减少GPU显存通讯） +   `PyTorch-Compile`(自动对pytorch python代码生成cuda相关的优化代码,可以控制区间，本质就是AI编译器啦) +`Tensor Parallelism`（多卡计算基本要求） + `Speculative Sampling`(特别适合打速度排名。。。。因为面对复杂任务这里是逆优化。。。)

- Llama-7B Eager版推理速度 25 tokens/s, gpt-fast 版提升到 246 tokens/s
- Llama-70B 77 tokens/s
- ![](https://pytorch.org/assets/images/accelerating-generative-ai-2/screen-recording.gif)

### TensorRT-LLM

【2023-10-17】[tensorrt-llm](https://nvidia.github.io/TensorRT-LLM/) 支持主流大模型加速， [github](https://github.com/NVIDIA/TensorRT-LLM/tree/main)
- TensorRT-LLM 是 TensorRT 和 FastTransformer 的结合体，旨为大模型推理加速而生。
- 除了 FastTransformer 对Transformer做的attention优化、softmax优化、算子融合等方式之外，还引入了众多的大模型推理优化特性
- 支持很多主流大模型
- TensorRT两阶段的调用方式——build+run：
  - build：通过配置参数将模型文件序列化为tensorRT的engine文件
  - run：加载engine文件，传入数据，进行inference

### llama.cpp

详见站内文章: [llm_think](llm)

### vLLM

Meta 前 PyTorch 团队推出 vLLM，最大特色“PagedAttention”。

vLLM（Very Large Language Model）专为大语言模型（LLM）优化的高效推理框架

其核心：PagedAttention、动态批处理pd并行、多LoRA动态加载等

PagedAttention 本质是灵活管理 KV Cache（注意力缓存）的方式。
- 传统 transformer 推理时，每个 token 都带上历史上下文，缓存爆炸。
- vLLM 通过类似虚拟内存分页方式，优化性能。像会打麻将的高效服务员，记牌记得巨快

好处
- API 设计接近 OpenAI 标准接口，部署友好，尤其对做“OpenAI替代”的场景特别合适。
- 高并发时不掉链子，响应速度几乎线性增长。

前提：GPU A100 起步。

#### vllm和sglang

【2025-09-27】[vllm:pd并行、多LoRA动态加载](https://zhuanlan.zhihu.com/p/1896895671711285497)

vllm和sglang 部署分别：
- vLLM 在高并发和低延迟场景下表现优异，尤其擅长快速生成第一个词（TTFT低）。
- SGLang 在多轮对话这类前缀复用率高的场景中，吞吐量优势明显，测试显示其在Llama-7B上的吞吐量可比vLLM高5倍。

#### 框架

核心架构是LLMEngine：包含调度器（Scheduler）和推理工作器（Worker）

- 调度器（Scheduler）：
  - 调度策略（policy）：
    - 请求的连续批处理(Continuous Batching）
    - 请求队列维护：waiting（待处理）、running（正在处理）、swapped（因显存不足被挂起)
  - 空间“调度指挥官”（BlockSpaceManager）：负责逻辑资源规划与分配策略；
    - 计算kv cache需要的块数量
    - 判断是否需要为新token分配新的空间（如需则通知cacheengine）
    - 内存共享：例如在并行采样时，多个输出序列可共享同一prompt的KV缓存块
- 推理工作器（Worker）：
  - 模型运行：包括多GPU分布式计算（张量并行、流水线并行）
  - 空间“后勤执行者”（CacheEngine）：负责物理显存的具体操作与数据存取。
- 性能效果：
  - 吞吐：提升高达24倍
  - 耗时：提升1.2倍。


#### 多LoRA动态加载 

- 无延迟切换：单基础模型（如Llama 3-8B）同时挂载多个LoRA适配器（如聊天/函数调用），请求时通过lora_request参数指定，切换延迟低于1ms。
- 资源复用：基础模型参数仅加载一次，适配器共享显存，支持5+适配器并行服务。

与stable diffusion类似，vllm 也支持在请求调用时指定调用某个lora；但有两点差异：
- vllm中的lora是一开始全部就加载进模型的，（sd是请求时才加载）
- vllm中每次请求只能指定一个lora

```sh
# 同时加载两个适配器
vllm serve meta-llama/Meta-Llama-3-8B \
  --enable-lora \
  --lora-modules \
    oasst=/path/to/oasst_adapter \  # 名称 oasst
    xlam=/path/to/xlam_adapter     # 名称 xlam
```

#### PagedAttention 动态分页机制

- 分块管理KV缓存：将注意力键值（Key-Value Cache）划分为固定大小的块（如4-16 tokens/块），按需动态分配GPU显存，避免传统连续分配导致的碎片问题。
- 显存复用与共享：短序列推理时仅占用必要块，释放空间供其他请求使用；支持跨请求的缓存共享（如相同前缀提示词），显存利用率提升最高达25%。
- 写时复制（Copy-on-Write）：共享块标记为只读，修改时创建新副本，减少重复计算



#### vllm 部署方式

vllm 两种模型部署方式：
- **在线**服务形式（Online Serving）
  - 在线服务是通过指令来启动一个vllm服务，将模型以服务的形式完成部署，之后可以通过openai格式的api来访问模型
- **离线**推理形式 （Offline Inference）
  - 离线推理的形式是通过类的方式初始化一个模型，之后传入提示词即可访问模型


#### vllm 使用

```py
# 安装vLLM
# pip install vllm

# 示例代码：生成文本
from vllm import LLM, SamplingParams

prompts = ["什么是vLLM？", "vLLM的优势是什么？"]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
llm = LLM(model="meta-llama/Llama-2-7b-chat-hf")  # 可限制最大并发：max_num_seqs=2，使用FP16：dtype="float16"

outputs = llm.generate(prompts, sampling_params)  # 批量推理

for output in outputs:
    print(f"输入：{output.prompt}\n输出：{output.outputs[0].text}\n"2
```

服务开启和各参数作用

vllm 服务启动指令如下

```sh
vllm serve deepseek-ai/deepseek-vl2-tiny  \
 --hf_overrides '{"architectures": ["DeepseekVLV2ForCausalLM"]}' \
 --dtype float16   --trust_remote_code \
 --host 0.0.0.0 --port 8080 \
 --chat_template template_deepseek_vl2.jinja \
 --gpu-memory-utilization 0.7 \
 --limit-mm-per-prompt "image=8"
```

详见[地址](https://zhuanlan.zhihu.com/p/1895409091192537734)

#### vLLM 分布式

【2025-09-07】[利用 vLLM 进行 rollout](https://zhuanlan.zhihu.com/p/1943606938769295200)

vLLM 允许设置 PP 和 DP

```py
llm = LLM(
    model=str(model_dir),
    dtype='bfloat16',
    gpu_memory_utilization=0.4,
    tensor_parallel_size=2, 
    pipeline_parallel_size = 2, 
    data_parallel_size = 2 
)
```

TP 和 PP 很好理解，而DP 的意思应该是，例如你有4张卡，设置 TP = 2 ， PP = 1 ，此时 vLLM 内部会启动“两份模型”, 进行并行的数据处理


#### vLLM 源码解析

【2024-4-12】[图解大模型计算加速系列：vLLM源码解析2，调度器策略(Scheduler)](https://mp.weixin.qq.com/s/N2tsOD-XdaNcodf-CKWVhQ)
- 一、入口函数
- 二、SequenceGroup
- 2.1 原生请求输入
- 2.2 SequenceGroup的作用
- 2.3 SequenceGroup的结构
- 三、add_request: 预处理请求
- 四、step：调度器策略
- 4.1 调度器结构
- 4.2 整体调度流程
- 4.3 _passed_delay：waiting队列调度时间阈值判断
- 4.4 can_allocate：能否为seq_group分配物理块（prefill）
- 4.5 can_append_slot: 能否为seq_group分配物理块（decode）
- 4.6 allocate与append_slot：为seq_group实际分配物理块
- 4.7 preempt：抢占策略
- 4.8 调度器整体代码解读

#### 案例

'qwen-vllm - 通义千问VLLM推理部署DEMO' 
- GitHub: [qwen-vllm](github.com/owenliang/qwen-vllm)


### SGLang

vLLM 虽好，但难以自定义推理逻辑，比如控制 prompt 动态拼接、多轮上下文窗口滚动、token 前缀约束，操作麻烦。

vLLM 设计思想：“底层最优”，更适合请求独立、按 token 走流水线的场景。 

SkyWork 团队推出 SGLang，最开始为了服务 InternLM 这种国产大模型开发的，但最近社区动静很大。

SGLang 更像“推理框架+推理DSL（领域特定语言）”结合体。鼓励用“Python+模板语言”写法描述推理逻辑，if else 控制输出、循环生成、模板格式化、系统指令，都能 prompt 模板里直接操作

SGLang 把“prompt +推理流程”统一封装成“程序单元”，像写代码那样写推理逻辑，还能自动在多个用户、多个请求之间搞调度优化。

SGLang 是 LMSYS Org 团队于2024年1月推出的 LLM 和 VLM 的通用服务引擎，且完全开源，采用 Apache 2.0 许可授权。
- 纯 Python 编写，核心调度器只用了不到 4K 行代码就实现了
- 已被 LMSYS Chatbot Arena 用于支持部分模型、Databricks、几家初创公司和研究机构，产生了数万亿 token，实现了更快的迭代。
- Paper：[SGLang: Efficient Execution of Structured Language Model Programs](https://arxiv.org/abs/2312.07104)
- Code：[sglang](https://github.com/sgl-project/sglang)

SGLang 技术结构解析：
- RadixAttention
- Upper-level Scheduling

最新的 SGLang Runtime v0.2 性能更加惊艳。
- 运行 Llama 3.1 405B 时，吞吐量和延迟表现都优于 vLLM 和 TensorRT-LLM，甚至能达到 TensorRT-LLM 的 2.1 倍，vLLm 的 3.8 倍。
- 目前已在 GitHub 上已经收获了超过 4.7k 的 star 量

Lepton AI 联合创始人兼 CEO 贾扬清都评价说：
> 我一直被我的博士母校加州大学伯克利分校惊艳，因为它不断交付最先进的人工智能和系统协同设计成果。


参考：[参考](https://blog.csdn.net/QingKeLab/article/details/141688674)


### MLC-LLM


## LLM 推理框架

参考
- 【2023-9-21】[大语言模型推理性能优化综述](https://zhuanlan.zhihu.com/p/656485997)
- 【2024-3-30】[图解大模型计算加速系列之：vLLM核心技术PagedAttention原理](https://mp.weixin.qq.com/s/oCGENfMwTNmfr1nGeCZz2g)

LLM 推理过程分两个阶段: `prefill` 和 `decode`, 通常用 KV cache 技术加速推理


PagedAttention的设计灵感来自操作系统的虚拟内存分页管理技术

### 总结

40GB A100 GPU 上，用 LLaMA-1 13b 模型进行7个部署框架的对比

LLM推理有很多框架，各有其特点，七个框架的关键点：
- [1] `vLLM` ：适用于**大批量**Prompt输入，并对推理速度要求高的场景；
  - `vLLM` 吞吐量比HuggingFace Transformers（HF）高**14x-24倍**，比 HuggingFace Text Generation Inference（TGI）高2.2x-2.5倍。
- [2] `Text generation inference`：依赖HuggingFace模型，并且不需要为核心模型增加多个adapter的场景；
- [3] `CTranslate2`：可在CPU上进行推理；
- [4] `OpenLLM`：为核心模型添加adapter并使用HuggingFace Agents，尤其是不完全依赖PyTorch；
- [5] `Ray Serve`：稳定的Pipeline和灵活的部署，它最适合更成熟的项目；
  - `Ray Serve` 是一个可扩展的模型服务库，用于构建在线推理API。Serve与框架无关，因此可以使用一个工具包来为深度学习模型的所有内容提供服务。
- [6] `MLC LLM`：可在客户端（边缘计算）（例如，在Android或iPhone平台上）本地部署LLM；
  - LLM的机器学习编译（MLC LLM）是一种通用的部署解决方案，它使LLM能够利用本机硬件加速在消费者设备上高效运行
- [7] `DeepSpeed-MII`：使用DeepSpeed库来部署LLM；

![](https://pic1.zhimg.com/80/v2-3f467171d76953de58e69faf1d802394_1440w.webp)


### 一、vLLM

2023年6月，加州大学伯克利分校等机构开源了 `vLLM`（目前已有 6700 多个 star），其使用了一种新设计的注意力算法 `PagedAttention`，可让服务提供商轻松、快速且低成本地发布 LLM 服务。

【2023-9-25】[vLLM出论文，让每个人都能快速低成本地部署LLM服务](https://www.toutiao.com/article/7282671140630315581)
- ![](https://pic1.zhimg.com/80/v2-63fe1b3f450eefe222f025fac5a6cb84_1440w.webp)
- 论文：[Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)
- 代码：[vllm](https://github.com/vllm-project/vllm)
- 文档：[vllm](https://vllm.readthedocs.io)

vLLM 吞吐量比 HuggingFace Transformers（HF）高**14x-24**倍，比HuggingFace Text Generation Inference（TGI）高2.2x-2.5倍。


**离线批量推理**

```py
# pip install vllm
from vllm import LLM, SamplingParams

prompts = [
    "Funniest joke ever:",
    "The capital of France is",
    "The future of AI is",
]
sampling_params = SamplingParams(temperature=0.95, top_p=0.95, max_tokens=200)
llm = LLM(model="huggyllama/llama-13b")
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

**API Server**

```sh
# Start the server:
python -m vllm.entrypoints.api_server --env MODEL_NAME=huggyllama/llama-13b

# Query the model in shell:
curl http://localhost:8000/generate \
    -d '{
        "prompt": "Funniest joke ever:",
        "n": 1,
        "temperature": 0.95,
        "max_tokens": 200
    }'
```

功能：
-   **Continuous batching**：有iteration-level的调度机制，每次迭代batch大小都有所变化，因此vLLM在大量查询下仍可以很好的工作。
-   **PagedAttention**：受操作系统中虚拟内存和分页的经典思想启发的注意力算法，这就是模型加速的秘诀。

优点：
-   **文本生成的速度：**实验多次，发现vLLM的推理速度是最快的；
-   **高吞吐量服务：**支持各种解码算法，比如parallel sampling, beam search等；
-   **与OpenAI API兼容：**如果使用OpenAI API，只需要替换端点的URL即可；

缺点：
-   **添加自定义模型**：虽然可以合并自己的模型，但如果模型没有使用与vLLM中现有模型类似的架构，则过程会变得更加复杂。例如，增加Falcon的支持，这似乎很有挑战性；
-   **缺乏对适配器（LoRA、QLoRA等）的支持**：当针对特定任务进行微调时，开源LLM具有重要价值。然而，在当前的实现中，没有单独使用模型和适配器权重的选项，这限制了有效利用此类模型的灵活性。
-   **缺少权重量化**：有时，LLM可能不需要使用GPU内存，这对于减少GPU内存消耗至关重要。

这是LLM推理最快的库。得益于其内部优化，它显著优于竞争对手。尽管如此，它在支持有限范围的模型方面确实存在弱点。

使用vLLM开发路线可以参考：[https://github.com/vllm-project/vllm/issues/244](https://github.com/vllm-project/vllm/issues/244)**

### 二、Text generation inference

![](https://pic3.zhimg.com/80/v2-5238573ef15a96e9fcafc28193a56d9a_1440w.webp)

Text generation inference是用于文本生成推断的Rust、Python和gRPC服务器，在HuggingFace中已有LLM 推理API使用。

**使用docker运行web server**

```sh
mkdir data
docker run --gpus all --shm-size 1g -p 8080:80 \
-v data:/data ghcr.io/huggingface/text-generation-inference:0.9 \
  --model-id huggyllama/llama-13b \
  --num-shard 1
```

**查询实例**

```sh
# pip install text-generation
from text_generation import Client

client = Client("http://127.0.0.1:8080")
prompt = "Funniest joke ever:"
print(client.generate(prompt, max_new_tokens=17 temperature=0.95).generated_text)
```

功能：
-   **内置服务评估：**可以监控服务器负载并深入了解其性能；
-   **使用flash attention（和v2）和Paged attention优化transformer推理代码：**并非所有模型都内置了对这些优化的支持，该技术可以对未使用该技术的模型可以进行优化；

优点：
-   **所有的依赖项都安装在Docker中：**会得到一个现成的环境；
-   **支持HuggingFace模型：**轻松运行自己的模型或使用任何HuggingFace模型中心；
-   **对模型推理的控制**：该框架提供了一系列管理模型推理的选项，包括精度调整、量化、张量并行性、重复惩罚等；

缺点：
-   **缺乏对适配器的支持：**需要注意的是，尽管可以使用适配器部署LLM（可以参考[https://www.youtube.com/watch?v=HI3cYN0c9ZU](https://www.youtube.com/watch%3Fv%3DHI3cYN0c9ZU)），但目前还没有官方支持或文档；
-   **从源代码（Rust+CUDA内核）编译：**对于不熟悉Rust的人，将客户化代码纳入库中变得很有挑战性；
-   **文档不完整**：所有信息都可以在项目的自述文件中找到。尽管它涵盖了基础知识，但必须在问题或源代码中搜索更多细节；

使用Text generation inference的开发路线可以[参考](https://github.com/huggingface/text-generation-inference/issues/232)

### 三、CTranslate2


![](https://pic1.zhimg.com/80/v2-dfc1a2808b8b04b5e99f81e8734ca6b0_1440w.webp)

CTranslate2是一个C++和Python库，用于使用Transformer模型进行高效推理。

转换模型

```sh
pip install -qqq transformers ctranslate2

# The model should be first converted into the CTranslate2 model format:
ct2-transformers-converter --model huggyllama/llama-13b --output_dir llama-13b-ct2 --force
```

**查询实例**

```py
import ctranslate2
import transformers

generator = ctranslate2.Generator("llama-13b-ct2", device="cuda", compute_type="float16")
tokenizer = transformers.AutoTokenizer.from_pretrained("huggyllama/llama-13b")

prompt = "Funniest joke ever:"
tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(prompt))
results = generator.generate_batch(
    [tokens], 
    sampling_topk=1, 
    max_length=200, 
)
tokens = results[0].sequences_ids[0]
output = tokenizer.decode(tokens)
print(output)
```

**功能：**
-   **在CPU和GPU上快速高效地执行：**得益于内置的一系列优化：层融合、填充去除、批量重新排序、原位操作、缓存机制等。推理LLM更快，所需内存更少；
-   **动态内存使用率：**由于CPU和GPU上都有缓存分配器，内存使用率根据请求大小动态变化，同时仍能满足性能要求；
-   **支持多种CPU体系结构：**该项目支持x86–64和AArch64/ARM64处理器，并集成了针对这些平台优化的多个后端：英特尔MKL、oneDNN、OpenBLAS、Ruy和Apple Accelerate；

**优点：**
-   **并行和异步执行**\--可以使用多个GPU或CPU核心并行和异步处理多个批处理；
-   **Prompt缓存**——在静态提示下运行一次模型，缓存模型状态，并在将来使用相同的静态提示进行调用时重用；
-   **磁盘上的轻量级**\--量化可以使模型在磁盘上缩小4倍，而精度损失最小；

**缺点**：
-   **没有内置的REST服务器**——尽管仍然可以运行REST服务器，但没有具有日志记录和监控功能的现成服务
-   **缺乏对适配器（LoRA、QLoRA等）的支持**

### 四、DeepSpeed-MII

![](https://pic1.zhimg.com/80/v2-b871e7cc5ef3ac72aa067953011333c4_1440w.webp)

在DeepSpeed支持下，DeepSpeed-MII可以进行低延迟和高通量推理。

**运行web服务**

```py
# DON'T INSTALL USING pip install deepspeed-mii
# git clone https://github.com/microsoft/DeepSpeed-MII.git
# git reset --hard 60a85dc3da5bac3bcefa8824175f8646a0f12203
# cd DeepSpeed-MII && pip install .
# pip3 install -U deepspeed

# ... and make sure that you have same CUDA versions:
# python -c "import torch;print(torch.version.cuda)" == nvcc --version
import mii

mii_configs = {
    "dtype": "fp16",
    'max_tokens': 200,
    'tensor_parallel': 1,
    "enable_load_balancing": False
}
mii.deploy(task="text-generation",
           model="huggyllama/llama-13b",
           deployment_name="llama_13b_deployment",
           mii_config=mii_configs)
```

**查询实例**

```py
import mii

generator = mii.mii_query_handle("llama_13b_deployment")
result = generator.query(  
  {"query": ["Funniest joke ever:"]}, 
  do_sample=True,
  max_new_tokens=200
)
print(result)
```

**功能**：
-   **多个副本上的负载平衡：**这是一个非常有用的工具，可用于处理大量用户。负载均衡器在各种副本之间高效地分配传入请求，从而缩短了应用程序的响应时间。
-   **非持久部署：**目标环境的部署不是永久的，需要经常更新的，这在资源效率、安全性、一致性和易管理性至关重要的情况下，这是非常重要的。

**优点**：
-   **支持不同的模型库：**支持多个开源模型库，如Hugging Face、FairSeq、EluetherAI等；
-   **量化延迟和降低成本：**可以显著降低非常昂贵的语言模型的推理成本；
-   **Native和Azure集成：**微软开发的MII框架提供了与云系统的出色集成；

**缺点**：
-   **支持模型的数量有限：**不支持Falcon、LLaMA2和其他语言模型；
-   **缺乏对适配器（LoRA、QLoRA等）的支持；**

### 五、OpenLLM

![](https://pic1.zhimg.com/80/v2-2028bebc2adf59968b7506ebb697190c_1440w.webp)

OpenLLM是一个用于在生产中操作大型语言模型（LLM）的开放平台。

**运行web服务**

```sh
pip install openllm scipy
openllm start llama --model-id huggyllama/llama-13b \
  --max-new-tokens 200 \
  --temperature 0.95 \
  --api-workers 1 \
  --workers-per-resource 1
```

**查询实例**

```py
import openllm

client = openllm.client.HTTPClient('http://localhost:3000')
print(client.query("Funniest joke ever:"))
```

**功能**：

-   **适配器支持：**可以将要部署的LLM连接多个适配器，这样可以只使用一个模型来执行几个特定的任务；
-   **支持不同的运行框架：**比如Pytorch（pt）、Tensorflow（tf）或Flax（亚麻）；
-   **HuggingFace Agents\[11\]：**连接HuggingFace上不同的模型，并使用LLM和自然语言进行管理；

**优点**：

-   **良好的社区支持：**不断开发和添加新功能；
-   **集成新模型：**可以添加用户自定义模型；
-   **量化：**OpenLLM支持使用bitsandbytes\[12\]和GPTQ\[13\]进行量化；
-   **LangChain集成：**可以使用LangChian与远程OpenLLM服务器进行交互；

**缺点**：
-   **缺乏批处理支持：**对于大量查询，这很可能会成为应用程序性能的瓶颈；
-   **缺乏内置的分布式推理**——如果你想在多个GPU设备上运行大型模型，你需要额外安装OpenLLM的服务组件Yatai\[14\]；

### 六、Ray Serve

![](https://pic4.zhimg.com/80/v2-7746a44a79ce1a591a01ee8193c4bbc3_1440w.webp)

Ray Serve是一个可扩展的模型服务库，用于构建在线推理API。Serve与框架无关，因此可以使用一个工具包来为深度学习模型的所有内容提供服务。

![](https://pic1.zhimg.com/80/v2-524968a7269229d43184de705b0644f0_1440w.webp)

**运行web服务**

```py
# pip install ray[serve] accelerate>=0.16.0 transformers>=4.26.0 torch starlette pandas
# ray_serve.py
import pandas as pd

import ray
from ray import serve
from starlette.requests import Request

@serve.deployment(ray_actor_options={"num_gpus": 1})
class PredictDeployment:
    def __init__(self, model_id: str):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

    def generate(self, text: str) -> pd.DataFrame:
        input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(
            self.model.device
        )
        gen_tokens = self.model.generate(
            input_ids,
            temperature=0.9,
            max_length=200,
        )
        return pd.DataFrame(
            self.tokenizer.batch_decode(gen_tokens), columns=["responses"]
        )

    async def __call__(self, http_request: Request) -> str:
        json_request: str = await http_request.json()
        return self.generate(prompt["text"])

deployment = PredictDeployment.bind(model_id="huggyllama/llama-13b")

# then run from CLI command:
# serve run ray_serve:deployment
```

**查询实例**

```py
import requests

sample_input = {"text": "Funniest joke ever:"}
output = requests.post("http://localhost:8000/", json=[sample_input]).json()
print(output)
```

**功能**：

-   **监控仪表板和Prometheus度量：**可以使用Ray仪表板来获得Ray集群和Ray Serve应用程序状态；
-   **跨多个副本自动缩放：**Ray通过观察队列大小并做出添加或删除副本的缩放决策来调整流量峰值；
-   **动态请求批处理：**当模型使用成本很高，为最大限度地利用硬件，可以采用该策略；

**优点**：
-   **文档支持：**开发人员几乎为每个用例撰写了许多示例；
-   **支持生产环境部署：**这是本列表中所有框架中最成熟的；
-   **本地LangChain集成：**您可以使用LangChian与远程Ray Server进行交互；

**缺点**：
-   **缺乏内置的模型优化：**Ray Serve不专注于LLM，它是一个用于部署任何ML模型的更广泛的框架，必须自己进行优化；
-   **入门门槛高：**该库功能多，提高了初学者进入的门槛；

如果需要最适合生产的解决方案，而不仅仅是深度学习，Ray Serve是一个不错的选择。它最适合于可用性、可扩展性和可观察性非常重要的企业。此外，还可以使用其庞大的生态系统进行数据处理、模型训练、微调和服务。最后，从OpenAI到Shopify和Instacart等公司都在使用它。

### 七、MLC LLM


![](https://pic4.zhimg.com/80/v2-d8f91231ec8466212d557d2c15808ba3_1440w.webp)

LLM的机器学习编译（MLC LLM）是一种通用的部署解决方案，它使LLM能够利用本机硬件加速在消费者设备上高效运行。

![](https://pic2.zhimg.com/80/v2-7bf144efe4e37a0b3c9bb95893ea6d65_1440w.webp)

**运行web服务**

```sh
# 1. Make sure that you have python >= 3.9
# 2. You have to run it using conda:
conda create -n mlc-chat-venv -c mlc-ai -c conda-forge mlc-chat-nightly
conda activate mlc-chat-venv

# 3. Then install package:
pip install --pre --force-reinstall mlc-ai-nightly-cu118 \
  mlc-chat-nightly-cu118 \
  -f https://mlc.ai/wheels

# 4. Download the model weights from HuggingFace and binary libraries:
git lfs install && mkdir -p dist/prebuilt && \
  git clone https://github.com/mlc-ai/binary-mlc-llm-libs.git dist/prebuilt/lib && \
  cd dist/prebuilt && \  
  git clone https://huggingface.co/huggyllama/llama-13b dist/ && \
  cd ../..
  
  
# 5. Run server:
python -m mlc_chat.rest --device-name cuda --artifact-path dist
```

**查询实例**

```py
import requests

payload = {
   "model": "lama-30b",
   "messages": [{"role": "user", "content": "Funniest joke ever:"}],
   "stream": False
}
r = requests.post("http://127.0.0.1:8000/v1/chat/completions", json=payload)
print(r.json()['choices'][0]['message']['content'])
```

**功能**：

-   **平台本机运行时：**可以部署在用户设备的本机环境上，这些设备可能没有现成的Python或其他必要的依赖项。应用程序开发人员只需要将MLC编译的LLM集成到他们的项目中即可；
-   **内存优化：**可以使用不同的技术编译、压缩和优化模型，从而可以部署在不同的设备上；

**优点**：

-   **所有设置均可在JSON配置中完成：**在单个配置文件中定义每个编译模型的运行时配置；
-   **预置应用程序：**可以为不同的平台编译模型，比如C++用于命令行，JavaScript用于web，Swift用于iOS，Java/Kotlin用于Android；

**缺点**：

-   **使用LLM模型的功能有限**：不支持适配器，无法更改精度等，该库主要用于编译不同设备的模型；
-   **只支持分组量化\[15\]：**这种方法表现良好，但是在社区中更受欢迎的其他量化方法（bitsandbytes和GPTQ）不支持；
-   **复杂的安装：**安装需要花几个小时，不太适合初学者开发人员；

如果需要在iOS或Android设备上部署应用程序，这个库正是你所需要的。它将允许您快速地以本机方式编译模型并将其部署到设备上。但是，如果需要一个高负载的服务器，不建议选择这个框架。


#### MLC LLM -- 陈天奇

- 【2023-5-2】[陈天奇等人新作引爆AI界：手机原生跑大模型，算力不是问题了](https://mp.weixin.qq.com/s/uQGAu1v-6ApgZHVkZJsUdQ)
- 【2023-6-5】[陈天奇官宣新APP，让手机原生跑大模型，应用商店直接下载使用](https://www.toutiao.com/article/7241085086400233995), 陈天奇公布了一个好消息：MLC Chat app 已经在苹果的 App Store 上线了。

【2023-5-2】[端侧语言大模型部署时代已经悄悄到来！](https://zhuanlan.zhihu.com/p/626268783)

#### TVM 简介

TVM是一个深度学习编译器，初衷是让各种训练框架训练好的模型能够在不同硬件平台上面快速推理
- 支持Pytorch、AutoML、Tensorflow、Onnx、Kersa、Mxnet等多种前端训练框架；
- 支持ARM CPU、Intel CPU、NVIDIA显卡、FPGA、ASIC等多种硬件设备。

MLC-LLM 底层技术其实就是`TVM`编译器。

该框架的输入是一些训练框架训练好的**模型文件**；
- 然后, 利用Relay将其转换成 High-Level Differentiable IR，该阶段会执行一些图优化操作，包括：算子融合、常量折叠、内存重排、模型量化等；
- 接着会利用AutoTVM、Ansor或者Meta Scheduler等自动化优化技术来将这种IR转换为Tensor Expression IR这种更低级的IR表示。

TVM深度学习编译器中的一个亮点工作就是**自动优化技术**
- 第一代优化技术叫`AutoTVM`
- 第二代叫`Ansor`或者`Auto Scheduler`
- 第三代叫`Meta Scheduler`

![](https://pic3.zhimg.com/80/v2-a2aa328a18b3afb02f48816419c481c6_1440w.jpg)

AutoTVM
- ![](https://pic3.zhimg.com/80/v2-9e23067a8872309bdafadede6328e192_1440w.jpg)

Ansor/Auto Scheduler
- ![](https://pic4.zhimg.com/80/v2-7ccb0e4a6fbbecd305f68dfd573b1377_1440w.jpg)


#### MLC LLM 简介

MLC LLM 是一种通用解决方案，允许将任何语言模型**本地部署**在各种硬件后端和本地应用程序上。

此外还有一个高效框架，供每个人进一步优化自己用例的模型性能。<span style='color:red'>一切都在本地运行，无需服务器支持</span>，并通过手机和笔记本电脑上的本地 GPU 加速。

TVM是一个深度学习编译器，知名编译工具，国内很多大公司都在使用它，国内很多的芯片公司都在使用它构建自己的工具链。
- `AutoTVM`、`Ansor`是`TVM`中比较亮眼的工作，思想都是利用ML将算子优化的任务自动化，当前它已经可以很好的支持多种硬件设备。
- 语言大模型的轻量化核心是**Transformer的加速与优化**，TVM社区很早就开始探索Transformer的加速与优化。除此之外，TVM中的图优化技术、自动优化等技术为语言大模型的轻量化打下了坚实的基础。

MLC-LLM只是语言大模型轻量化的开端，语言大模型**轻量化**方向近期会变得异常火热, 很多大公司陆续都是开源自己的一些工作。
- 随着MIC-LLM等工具出现，**端侧大模型部署**热潮已经来临。OpenAI一家独大的情况也会慢慢得打缓解，随着语言大模型的赋能，越来越多的智能设备，尤其是机器人的智能程度会更上一层楼！
- 随着端侧语言大模型的部署难题逐步被解决，端侧模型的**数据隐私**问题可能成为了端侧部署的一个关键问题。不过，这个问题应该相对来说会比较容易一些。期待了端侧语言大模型时代的到来！

- [演示图](https://vdn6.vzuu.com/SD/da2d7036-e81f-11ed-a962-bacc53acff3b-v1_f4_t2_etMRzyS8.mp4?pkey=AAV2GKNHXbMr7W0DZWmaAKjmklpebDlDgvlJQN4ElgagtlxqcrYmaLNld20o3ymLMrOUseNg1m3gdavjpUBHj89Y&c=avc.1.1&f=mp4&pu=078babd7&bu=078babd7&expiration=1691478412&v=ks6)
- [参考](https://zhuanlan.zhihu.com/p/626189075)


[mlc-llm](https://mlc.ai/mlc-llm/) 部署汇总
- 亲测：华为mate 30下载后，启动即闪退；iOS正常

|设备|地址|示例|
|---|---|---|
|iOS|[iOS地址](https://testflight.apple.com/join/57zd7oxa)|![](https://mlc.ai/mlc-llm/gif/ios-demo.gif)|
|Android|[Android地址](https://mlc.ai/mlc-llm/gif/android-demo.gif)|![](https://mlc.ai/mlc-llm/gif/android-demo.gif)|
|PC|[Windows Linux Mac](https://mlc.ai/mlc-llm/#windows-linux-mac)|![](https://mlc.ai/mlc-llm/gif/linux-demo.gif)|
|Web|[WebLLM](https://mlc.ai/mlc-llm/#web-browser)||

让大模型变小这条路上，人们做了很多尝试
- 先是 Meta 开源了 LLaMA，让学界和小公司可以训练自己的模型。
- 随后斯坦福研究者启动了 Lamini，为每个开发者提供了从 GPT-3 到 ChatGPT 的快速调优方案。
- 最近 MLC LLM 的项目一步登天，因为它能在**任何设备**上编译运行大语言模型。

MLC LLM 在各类硬件上**原生部署任意大型语言模型**提供了解决方案，可将大模型应用于移动端（例如 iPhone）、消费级电脑端（例如 Mac）和 Web 浏览器。
-  TVM、MXNET、XGBoost 作者，CMU 助理教授，OctoML CTO 陈天奇等多位研究者共同开发的，参与者来自 CMU、华盛顿大学、上海交通大学、OctoML 等院校机构，同时也获得了开源社区的支持。
- [github](https://github.com/mlc-ai/mlc-llm)
- [Demo](https://mlc.ai/mlc-llm/)
- [MLC课程](https://mlc.ai/summer22-zh/schedule)：机器学习编译
- [知乎专题](https://www.zhihu.com/question/598610139)

曾经开源过XGBoost和TVM `陈天奇`大佬已经完成了这件事情，推出了一个叫`MLC-LLM` 工具，在一些低算力平台上面运行一些语言大模型！只要GPU显存大于6GB，都可以去尝试在本地部署一下属于语言大模型

MLC LLM 旨在让每个人都能在个人设备上本地开发、优化和部署 AI 模型，而无需服务器支持，并通过手机和笔记本电脑上的消费级 GPU 进行加速。具体来说，MLC LLM 支持的平台包括：
- iPhone
- Metal GPU 和英特尔 / ARM MacBook;
- 在 Windows 和 Linux 上支持通过 Vulkan 使用 AMD 和 NVIDIA GPU；
- 在 Windows 和 Linux 上 通过 CUDA 使用 NVIDIA GPU；
- 浏览器上的 WebGPU（借助 MLC LLM 的配套项目 Web LLM）。

为了实现在各类硬件设备上运行 AI 模型的目标，研究团队要解决计算设备和部署环境的多样性问题，主要挑战包括：
- 支持不同型号的 CPU、GPU 以及其他可能的协处理器和加速器；
- 部署在用户设备的**本地环境**中，这些环境可能没有 python 或其他可用的必要依赖项；
- 通过仔细规划分配和积极压缩模型参数来解决**内存限制**。
- MLC LLM 提供可重复、系统化和可定制的工作流，使开发人员和 AI 系统研究人员能够以 Python 优先的方法实现模型并进行优化。MLC LLM 可以让研究人员们快速试验新模型、新想法和新的编译器 pass，并进行本地部署。

为了实现原生部署，研究团队以**机器学习编译**（MLC）技术为基础来高效部署 AI 模型。
- [MLC技术](https://mlc.ai/)
- MLC LLM 借助一些开源生态系统，包括来自 HuggingFace 和 Google 的分词器，以及 LLaMA、Vicuna、Dolly 等开源 LLM。
- ![](https://pica.zhimg.com/80/v2-b23bb5806fa9c32e51773e06494b8f62_1440w.webp?source=1940ef5c)

MLC LLM 的主要工作流基于 Apache TVM Unity，通过扩展 TVM 后端使模型编译更加透明和高效。
- Dynamic shape：该研究将语言模型烘焙（bake）为具有原生 Dynamic shape 支持的 TVM IRModule，避免了对最大输入长度进行额外填充的需要，并减少了计算量和内存使用量。
- 可组合的 ML 编译优化：MLC LLM 可以执行许多模型部署优化，例如更好的编译代码转换、融合、内存规划和库卸载（library offloading），并且手动代码优化可以很容易地合并为 TVM 的 IRModule 转换，成为一个 Python API。
- 量化：MLC LLM 利用低位量化来压缩模型权重，并利用 TVM 的 loop-level TensorIR 为不同的压缩编码方案快速定制代码生成。
- 运行时（Runtime）：TVM 编译生成的库能够通过 TVM runtime 在设备的原生环境中运行，TVM runtime 支持 CUDA/Vulkan/Metal 等主流 GPU 驱动以及 C、JavaScript 等语言的绑定。

此外，MLC 还为 CUDA、Vulkan 和 Metal 生成了 GPU shader，并通过 LLVM 支持多种 CPU，包括 ARM 和 x86。通过改进 TVM 编译器和运行时，使用者可以添加更多支持，例如 OpenCL、sycl、webgpu-native。


#### MLC LLM 支持设备

支持的设备类型
- MLC-LLM工具支持多种设备类型，大到N卡、AMD GPU，小到Android、IOS、WebGPU等。具体测试的设备列表如下所示。建议在设备内存大于等于6GB的设备上面进行推理与测试。

- iPhone, iPad

| 硬件/GPU | 操作系统 | Tokens/sec | 链接 |
| --- | --- | --- | --- |
| iPhone 14 Pro | iOS 16.4.1 | 7.2 | [https://github.com/junrushao](https://github.com/junrushao) |
| iPad Pro 11 with M1 | iPadOS 16.1 | 10.6 | [https://github.com/mlc-ai/mlc-llm/issues/15#issuecomment-1529377124](https://github.com/mlc-ai/mlc-llm/issues/15%23issuecomment-1529377124) |

-  Metal GPUs and Intel/ARM MacBooks

| 硬件/GPU | 操作系统 | Tokens/sec | 链接 |
| --- | --- | --- | --- |
| UHD Graphics 630 | macOS Ventura | 2.3 | [https://github.com/junrushao](https://github.com/junrushao) |
| 2020 MacBook Pro M1 (8G) | macOS | 11.4 | [https://github.com/mlc-ai/mlc-llm/issues/15#issuecomment-1529148903](https://github.com/mlc-ai/mlc-llm/issues/15%23issuecomment-1529148903) |
| 2021 MacBook Pro M1Pro (16G) | macOS Ventura | 17.1 | [https://github.com/mlc-ai/mlcllm/issues/15#issuecomment-1529434801](https://github.com/mlc-ai/mlcllm/issues/15%23issuecomment-1529434801) |
| M1 Max Mac Studio (64G) |  | 18.6 | [https://github.com/mlc-ai/mlcllm/issues/15#issuecomment-1529714864](https://github.com/mlc-ai/mlcllm/issues/15%23issuecomment-1529714864) |

- AMD and NVIDIA GPUs via Vulkan on Windows and Linux

| 硬件/GPU | 操作系统 | Tokens/sec | 链接 |
| --- | --- | --- | --- |
| Raden Pro 5300M | macOS Venture | 12.6 | [https://github.com/junrushao](https://github.com/junrushao) |
| AMD GPU on Steam Deck | TBD (S macOS Ventura ome Linux) | TBD | [https://www.reddit.com/r/LocalLLaMA/comments/132igcy/comment/jia8ux6/](https://www.reddit.com/r/LocalLLaMA/comments/132igcy/comment/jia8ux6/) |
| RX 7900 xtx |  |  | [https://www.reddit.com/r/LocalLLaMA/comments/132igcy/comment/jia691u/](https://www.reddit.com/r/LocalLLaMA/comments/132igcy/comment/jia691u/) |
| RX6800 16G VRAM | macOS Ventura | 22.5 | [https://github.com/mlc-ai/mlc-llm/issues/15](https://github.com/mlc-ai/mlc-llm/issues/15) |

- NVIDIA GPUs via CUDA on Windows and Linux

| 硬件/GPU | 操作系统 | Tokens/sec | 链接 |
| --- | --- | --- | --- |
| GTX 1060 (6GB) | Windows 10 | 16.7 | [https://github.com/mlc-ai/mlc-llm/issues/13#issue-1689858446](https://github.com/mlc-ai/mlc-llm/issues/13%23issue-1689858446) |
| RTX 3080 | Windows 11 | 26.0 | [https://github.com/mlc-ai/mlc-llm/issues/15#issuecomment-1529434801](https://github.com/mlc-ai/mlc-llm/issues/15%23issuecomment-1529434801) |
| RTX 3060 | Debian bookworm | 21.3 | [https://github.com/mlc-ai/mlc-llm/issues/15#issuecomment-1529572646](https://github.com/mlc-ai/mlc-llm/issues/15%23issuecomment-1529572646) |

- WebGPU on browsers


#### MLC-LLM 核心技术


![](https://pic4.zhimg.com/80/v2-c95a2f2706f88094bd196bd4bf7da53b_1440w.webp)

-   **Dynamic shape**: 作者将**语言模型**转换为具有原生动态形状支持的 TVM IRModule，避免了对最大长度进行额外填充的需要，并减少了计算量和内存使用量。如图所示，为了优化动态形状输入
  - 首先应用**循环切分**技术，即将一个大循环切分成两个小循环操作；
  - 然后应用张量自动化技术，即TVM中的Ansor或者Meta Scheduler技术。
  - ![](https://pic4.zhimg.com/80/v2-1a89c78eba7b1228fff6dd08d41ff2bf_1440w.webp)
-   **Composable ML compilation optimization**s: 执行了许多模型部署优化，例如更好的编译代码转换、融合、内存规划、库卸载和手动代码优化可以很容易地合并为TVM 的 IRModule 转换，作为 Python API 公开。如上图所示，模型推理工具链中常用的几种优化技术包括：算子简化、算子融合、常量折叠、内存排布等。
  - ![](https://pic1.zhimg.com/80/v2-dccad206e27b4d485879c50d9033a0ec_1440w.webp)
-   **Quantization**: 利用**低位量化**来压缩模型权重，并利用 TVM 的循环级 TensorIR 为不同的压缩编码方案快速定制代码生成。如图所示，TVM中可以通过两种方式来进行量化：1）通过 relay.quantize 完成浮点模型的量化，该量化包含annotate、calibrate和relize三步；2）通过一种称为 qnn 的 relay方言([http://relay.qnn.xxx](https://link.zhihu.com/?target=http%3A//relay.qnn.xxx)) 直接执行已经量化过的模型。
  - ![](https://pic4.zhimg.com/80/v2-883e9de589cbcac6e1f9854b46b160b7_1440w.webp)
-   **Runtime**: 最终生成的库在原生环境中运行，TVM 运行时具有最小的依赖性，支持各种 GPU 驱动程序 API 和原生语言绑定（C、JavaScript等）。如图所示，TVM支持多种Runtime，包括：JS、Java、Python、C++、Android、IOS、Web等，正是这些Runtime支持，才使得MLC-LLM可以很快的支持很多端侧设备!


#### MLC-LLM部署流图


![](https://pic4.zhimg.com/80/v2-04249102c3061d4c5e436e990a42125f_1440w.webp)

1、**Python first** development

-   IRModule: 如上图所示，该模块存储着一个张量函数集合，每个函数附带首个形状符号，并支持跟踪形状依赖。 该模块包含着Transformer中的关键模块，encoding和step\_decoding，前者用来做输入数据的编码操作，后者用来做数据的解码操作。  
-   ML Compilation Optimization: 该模块主要在计算图上面执行一些优化操作，具体包括：算子融合（降低多次加载的带宽开销）、内存规划（提前在编译阶段分配一些内存，并对内存的排布进行调整）、循环优化（利用常用的tile、reoder、paritation等技术）和权重量化（利用int8、int16等数据类型进行模型压缩）。  
-   TensorIR Schedules: 该模块主要利用Ansor自动优化或者Meta Scheduler自动优化技术对LLM模型中的算子进行调度优化。这是TVM编译器的一个杀手锏！该技术的核心思想是利用ML的思路来解决循环优化问题。  

2、**Universal** development

-   **最底层是硬件驱动层**，该层主要完成一些硬件适配与驱动的工作。支持的硬件具体包括：NVIDIA的CUDA、AMD的Rocm、苹果的Vulkan和WebGPU等。  
-   **第三层是TVM Runtim层**，该层主要完成TVM Runtime库的适配与加载任务。用户需要做的是调用TVM的Runtime推理接口完成模型的推理操作。  
-   **第二层是模型与代码层**，该层主要完成模型的优化与业务逻辑码的开发。通过Python First Development可以导出一个model.dylib库，用户需要实现[http://llm\_chat.cc](https://link.zhihu.com/?target=http%3A//llm_chat.cc)文件，即语言大模型的业务逻辑代码。  
-   **第一层是应用层**，该层用来开发一些上层应用，具体包括Chat CLI命令行工具、MLCChat.App 安卓或者IOS端的上层应用、基于WebGPU的网页端应用等。


#### MLC-LLM环境搭建

1、**iphone平台**

[参考](https://testflight.apple.com/join/57zd7oxa)页面安装已经编译好的APP。

注意事项：
- 试用此页面（仅限前 9000 名用户）以安装和使用作者为 iPhone 构建的示例 iOS 聊天应用程序。应用程序本身需要大约 4GB的内存才能运行。考虑到 iOS 和其他正在运行的应用程序，我们将需要具有 6GB（或更多）内存的最新 iPhone 来运行该应用程序。作者仅在 iPhone 14 Pro Max 和 iPhone 12 Pro上测试了该应用程序。

2、**Windows/Linux/Mac**平台

![](https://pic4.zhimg.com/v2-583cb94d4f32afe60eebeb0dfacbb847_b.gif)

![动图封面](https://pic4.zhimg.com/v2-583cb94d4f32afe60eebeb0dfacbb847_b.jpg)

步骤1 - 安装环境依赖
- 安装 Miniconda 或 Miniforge
- windows与linux用户-安装Vulkan驱动；对于Nvidia用户-建议安装Vulkan驱动

步骤2-创建环境

```sh
# Create new conda environment and activate the environment.
conda create -n mlc-chat
conda activate mlc-chat
# Install Git and Git-LFS, which is used for downloading the model weights from Hugging Face.
conda install git git-lfs
# Install the chat CLI app from Conda.
conda install -c mlc-ai -c conda-forge mlc-chat-nightly
# Create a directory, download the model weights from HuggingFace, and download the binary libraries from GitHub.
mkdir -p dist
git lfs install
git clone https://huggingface.co/mlc-ai/demo-vicuna-v1-7b-int3 dist/vicuna-v1-7b
git clone https://github.com/mlc-ai/binary-mlc-llm-libs.git dist/lib
# Enter this line and enjoy chatting with the bot running natively on your machine!
mlc_chat_cli
```

3、**Web浏览器**平台

步骤
1. 安装 Chrome Canary，它是支持使用 WebGPU 的 Chrome 开发者版本。
2. 利用下面的命令行发起Chrome Canary

```sh
/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary --enable-dawn-features=disable_robustness
```

3. 在浏览器运行[demo](https://mlc.ai/web-llm/#chat-demo)

注意事项：
- WebGPU 刚刚发布到 Chrome 并且处于测试阶段。我们在 Chrome Canary 中进行实验。你也可以试试最新的Chrome 113。Chrome版本≤112是不支持的，如果你正在使用它，demo会报错 Find an error initializing the WebGPU device OperationError: Required limit (1073741824) is greater than the 支持的限制 (268435456)。
- 验证 maxBufferSize 时 
- 验证所需限制时。已经在 windows 和 mac 上测试过了，你需要一个 6.4G 内存的 gpu。


#### MLC-LLM 效果展示

1、**web端**Demo
- ![](https://pic3.zhimg.com/80/v2-22762accdf3d48acd09f06b8a60e2eda_1440w.webp)

2、IOS端Demo
- ![](https://pic1.zhimg.com/v2-1f68e0fc385e8b67344f4e5c99fcc837.jpg?source=382ee89a)


3、Web Stable Diffusion
- ![](https://pic2.zhimg.com/80/v2-895ea13851a24908d5ec8fb6ef1ad775_1440w.webp)


## 优化方法

### 工业实践


#### GPT-4 投机采样

GPT4 一些技术细节泄露后，对于**投机采样**【Speculative Decoding】策略加速推理的研究比较多，但是**投机采样**依赖一个小而强的模型, 生成对于原始的模型来说比较简单的token，其次在一个系统中维护2个不同的模型，导致架构上的复杂性，最后使用投机采样的时候，会带来额外的解码开销，尤其是当使用一个比较高的采样温度值时。


#### Google Medusa 美杜莎

【2023-9-18】[LLM推理加速-Medusa](https://zhuanlan.zhihu.com/p/655809033)
- 项目主页: [medusa-llm](https://sites.google.com/view/medusa-llm)
- Github [Medusa](https://github.com/FasterDecoding/Medusa)
- 论文: [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774)

Medusa: Simple Framework for Accelerating LLM Generation with Multiple Decoding Heads
- ![](https://pic3.zhimg.com/80/v2-9de3ccb0b3107514b4fc71495ed78342_1440w.webp)

正常的LLM 基础上，增加几个解码头，并且每个头预测的偏移量是不同的，比如原始的头预测第i个token，而新增的medusa heads分别为预测第i+1，i+2...个token。如上图，并且每个头可以指定topk个结果，这样可以将所有的topk组装成一个一个的候选结果，最后选择最优的结果
- ![](https://pic1.zhimg.com/80/v2-6abff04d4dc96eb7752be0a8d7948e14_1440w.webp)

更多解读见[文章](https://zhuanlan.zhihu.com/p/655809033)

### 一、子图融合（subgraph fusion）

图融合技术即通过将多个 OP（算子）合并成一个 OP（算子），来减少`Kernel`的调用。因为每一个基本 OP 都会对应一次 GPU kernel 的调用，和多次显存读写，这些都会增加大量额外的开销。

#### 算子融合

`算子融合`是深度学习模型推理的一种典型优化技术，旨在通过减少计算过程中的访存次数和 Kernel 启动耗时达到提升模型推理性能的目的，该方法同样适用于 LLM 推理。

以 HuggingFace Transformers 库推理 LLaMA-7B 模型为例，经分析模型推理时的算子执行分布如下图所示
- 该模型有 30 个类型共计 2436 个算子，其中 aten::slice 算子出现频率为 388 次。
- 大量小算子的执行会降低 GPU 利用率，最终影响推理速度。
- ![](https://pic3.zhimg.com/80/v2-267fa86ddc41d9c1cb86c106b294271e_1440w.webp)

目前业界基本都针对 Transformer layer 结构特点，手工实现了`算子融合`。以 `DeepSpeed` Inference 为例，算子融合主要分为如下四类：
-   归一化层 和 QKV 横向融合：将三次计算 Query/Key/Value 的操作合并为一个算子，并与前面的归一化算子融合。
-   自注意力计算融合：将自注意力计算涉及到的多个算子融合为一个，业界熟知的 FlashAttention 即是一个成熟的自注意力融合方案。
-   残差连接、归一化层、全连接层和激活层融合：将 MLP 中第一个全连接层上下相关的算子合并为一个。
-   偏置加法和残差连接融合。
- ![](https://pic4.zhimg.com/80/v2-d6390ff28b40e6c0cb8a459d29eb6453_1440w.webp)
- 图 5 Transformer layer中的算子融合示意

由于算子融合一般需要定制化实现算子 CUDA kernel，因此对 GPU 编程能力要求较高。随着编译器技术的引入，涌现出 OpenAI `Triton` 、`TVM` 等优秀的框架来实现算子融合的自动化或半自动化，并取得了一定的效果。

**高性能算子**

针对 LLM 推理运行热点函数编写高性能算子，也可以降低推理时延。
-   `GEMM` 操作相关优化：在 LLM 推理的预填充阶段，Self-Attention 和 MLP 层均存在多个 GEMM 操作，耗时占据了推理时延的 80% 以上。GEMM 的 GPU 优化是一个相对古老的问题，在此不详细展开描述算法细节。英伟达就该问题已推出 cuBLAS、CUDA、CUTLASS 等不同层级的优化方案。例如，FasterTransformer 框架中存在大量基于 CUTLASS 编写的 GEMM 内核函数。另外，Self-Attention 中存在 GEMM+Softmax+GEMM 结构，因此会结合算子融合联合优化。
-   `GEMV` 操作相关优化：在 LLM 推理的解码阶段，运行热点函数由 GEMM 变为 GEMV。相比 GEMM，GEMV 的计算强度更低，因此优化点主要围绕降低访存开销开展。

高性能算子的实现同样对 GPU 编程能力有较高要求，且算法实现中的若干超参数与特定问题规模相关。因此，编译器相关的技术如自动调优也是业界研究的重点。

#### 1.1 FasterTransformer

[FasterTransformer](https://github.com/NVIDIA/FasterTransformer) by NVIDIA

`FasterTransformer`(FT) 是一个用于实现基于`Transformer`的神经网络推理的加速引擎。`FT`框架是用`C++/CUDA`编写的，依赖于高度优化的 cuBLAS、cuBLASLt 和 cuSPARSELt 库，与 [NVIDIA TensorRT](https://link.juejin.cn/%3Ftarget%3Dhttps%253A%252F%252Fdeveloper.nvidia.com%252Fblog%252Foptimizing-t5-and-gpt-2-for-real-time-inference-with-tensorrt%252F) 等其他编译器相比，FT 的特点是它支持**以分布式方式推理 Transformer 大模型**。

图融合是`FT` 的一个重要特征，将多层神经网络组合成一个单一的神经网络，将使用一个单一的内核进行计算。 这种技术减少了数据传输并增加了数学密度，从而加速了推理阶段的计算。 例如， multi-head attention 块中的所有操作都可以合并到一个内核中。

![](https://pic2.zhimg.com/80/v2-5c12abec5f35a555b6378e342fd51639_1440w.webp)

除此之外，`FT`还对部分大模型分别支持：
-   `INT8` 低精度量化推理
-   Ampere 架构的 GPU 硬件部分支持稀疏化
-   Hopper 架构支持 FP8 推理
-   Tensor 并行
-   Pipeline 并行

#### 1.2 DeepSpeed Inference

微软推出的 Transformer 模型的前向推理框架。
- [DeepSpeed Inference](https://arxiv.org/pdf/2207.00032.pdf) by Microsoft
- 把模型分散到多块卡（多机）上跑。
  - 有 150G+ 显存占用的模型，同时最大卡的显存只有 24G 卡，很多块，那么如果有这种框架随便跑。

对于 Transformer layer，可分为以下4个主要部分：
1.  Input Layer-Norm plus Query, Key, and Value GeMMs and their bias adds.
2.  Transform plus Attention.
3.  Intermediate FF, Layer-Norm, Bias-add, Residual, and Gaussian Error Linear Unit (GELU).
4.  Bias-add plus Residual.

如图所示，每一部分可分别进行融合，与未融合相比，以上几个部分的加速比可分别达到 1.5x, 2.9x, 3x, 1.2x 。

![](https://pic2.zhimg.com/80/v2-fe415109e5bd552485d1a42fbdd3d679_1440w.webp)

除此之外，DeepSpeed Inference 的优化点还有以下几点：
-   多 GPU 的并行优化
-   INT8 模型量化
-   推理的 pipeline 方案

DeepSpeed 实现 ZeRO ，为了减少显存使用，跨机器跨节点进行更大模型的训练。一般按层切分模型分别载入参数，像是模型并行。但运行时其实质则是**数据并行**方式，不同的数据会在不同的卡运行，且同一组数据一般会在一块卡上完成全部前向和后向过程。而被切分的参数和梯度等数据会通过互联结构在运行态共享到不同节点，只是复制出的数据用后即焚删除了，不再占用空间。
- [ZeRO & DeepSpeed: New system optimizations enable training models with over 100 billion parameters](https://www.microsoft.com/en-us/research/blog/zero-deepspeed-new-system-optimizations-enable-training-models-with-over-100-billion-parameters/)
- ![](https://pic1.zhimg.com/80/v2-145e05075831ece0553d65a577daaab4_1440w.webp)

安装
- MII 是个壳，主要封装了服务 api。核心并行机制都在 DeepSpeed 里。

```sh
pip install deepspeed
pip install deepspeed-mii
```

测试脚本: `example.py`

```py
import mii

pipe = mii.pipeline("mistralai/Mistral-7B-v0.1")
response = pipe(["DeepSpeed is", "Seattle is"], max_new_tokens=128)
print(response)
```

执行

```sh
deepspeed --num_gpus 2 mii-example.py
```


更多详细介绍及实践可参考笔者之前的文章：
- [紫气东来：NLP（十二）：DeepSpeed Inference 在 LLM 推理上的优化探究](https://zhuanlan.zhihu.com/p/629085568?)
- [DeepSpeed inference 代码理解](https://zhuanlan.zhihu.com/p/668181423)

#### 1.3 MLC LLM

[MLC LLM](https://github.com/mlc-ai/mlc-llm) by TVM

之前介绍的推理方案主要是基于GPU的优化，而 MLC LLM 提供了可应用于移动端（例如 iPhone）、消费级电脑端（例如 Mac）和 Web 浏览器的轻设备解决方案。

MLC LLM 的主要工作流基于 Apache TVM Unity，通过扩展 TVM 后端使模型编译更加透明和高效。其中以编译代码转换、融合、内存规划和库卸载（library offloading）为代表的可组合的 ML 编译优化是其中重要的优化特性。

![](https://pic2.zhimg.com/80/v2-942db4a7b53c01251a30cd9f79e83439_1440w.webp)

除此之外，MLC LLM 还具有以下特性：
-   Dynamic shape：避免了对最大输入长度进行额外填充的需要，并减少了计算量和内存使用量。
-   量化：MLC LLM 利用低位量化来压缩模型权重，并利用 TVM 的 loop-level TensorIR 为不同的压缩编码方案快速定制代码生成。
-   运行时（Runtime）：TVM 编译生成的库能够通过 TVM runtime 在设备的原生环境中运行，TVM runtime 支持 CUDA/Vulkan/Metal 等主流 GPU 驱动以及 C、JavaScript 等语言的绑定。

除了上述3种方案外，其他也支持图融合的方案还包括 [NVIDIA TensorRT](https://link.juejin.cn/%3Ftarget%3Dhttps%253A%252F%252Fdeveloper.nvidia.com%252Fblog%252Foptimizing-t5-and-gpt-2-for-real-time-inference-with-tensorrt%252F)， [Tencent TurboTransformers](https://github.com/Tencent/TurboTransformers) 等。




### 二、模型压缩（Model Compression）

模型压缩的基本动机在于当前的模型是冗余的，可以在精度损失很小的情况下实现模型小型化，主要包括3类方法：稀疏(Sparsity)、量化(Quantization)、蒸馏(Distillation)。

2025年11月13日，Compression techniques I’d study if I wanted small but smart LLMs.

1.Quantization
2.Distillation
3.Low-Rank Adaptation
4.Weight Sharing
5.Sparse Matrices
6.Layer Dropping
7.Knowledge Transfer
8.Embedding Compression
9.Mixed Sparsity
10. Progressive Shrinking
11.Structured Pruning
12.AutoML Compression

Follow @asmah2107  to update your game on LLM optimisations.



#### 2.1 稀疏(Sparsity)

实现稀疏(Sparsity)的一个重要方法是剪枝(Pruning)。剪枝是在保留模型容量的情况下，通过修剪不重要的模型权重或连接来减小模型大小。 它可能需要也可能不需要重新培训。 修剪可以是非结构化的或结构化的。
-   非结构化剪枝允许删除任何权重或连接，因此它不保留原始网络架构。 非结构化剪枝通常不适用于现代硬件，并且不会带来实际的推理加速。
-   结构化剪枝旨在维持某些元素为零的密集矩阵乘法形式。 他们可能需要遵循某些模式限制才能使用硬件内核支持的内容。 当前的主流方法关注结构化剪枝，以实现 Transformer 模型的高稀疏性。

关于剪枝稀疏的基本原理，可参考笔者之前的文章：
- [大语言模型的稀疏化技术](https://zhuanlan.zhihu.com/p/615399255)

除了上文介绍的稀疏方法外，还有其他的稀疏化方法，包括但不限于：
-   [SparseGPT](https://arxiv.org/pdf/2301.00774.pdf)：该方法的工作原理是将剪枝问题简化为大规模的稀疏回归实例。它基于新的近似稀疏回归求解器，用于解决分层压缩问题，其效率足以在几个小时内使用单个 GPU 在最大的 GPT 模型（175B 参数）上执行。同时，SparseGPT 准确率足够高，不需要任何微调，剪枝后所损耗的准确率也可以忽略不计。
-   [LLM-Pruner](https://arxiv.org/pdf/2305.11627.pdf)：遵循经典的“重要性估计-剪枝-微调”的策略，能够在有限资源下完成大语言模型的压缩，结果表明即使剪枝 20％ 的参数，压缩后的模型保留了 93.6％ 的性能。
-   [Wanda](https://arxiv.org/pdf/2306.11695.pdf): 该方法由两个简单但必不可少的组件构成——剪枝度量和剪枝粒度。剪枝度量用来评估权重的重要性，然后按照剪枝粒度进行裁剪。该方法在 65B 的模型上只需要 5.6 秒就可以完成剪枝，同时达到SparseGPT相近的效果。

以上主要实现了稀疏的方法，那么对于稀疏后的模型如何加速呢？NVIDIA Ampere 架构对与结构化稀疏做了专门的[稀疏加速单元](https://developer.nvidia.com/blog/accelerating-inference-with-sparsity-using-ampere-and-tensorrt/)，下图展示了结构化稀疏的物理表示：
- ![](https://pic3.zhimg.com/80/v2-69b4e98ed5c47ba98ac496598ce4a31a_1440w.webp)

2:4 结构化稀疏表示

下图展示了稀疏单元GEMM计算与标准GEMM计算的区别（详细解释参见[https://arxiv.org/pdf/2104.08378.pdf](https://arxiv.org/pdf/2104.08378.pdf)）
- ![](https://pic4.zhimg.com/80/v2-67533793fe25f97960c383c62c9ff62b_1440w.webp)

Sparse VS Dense GEMM

#### 2.2 量化(Quantization)

【2023-9-7】
- [关于大模型推理的量化算法总结](https://zhuanlan.zhihu.com/p/645308698)
- [大语言模型的模型量化(INT8/INT4)技术](https://zhuanlan.zhihu.com/p/627436535)


【2024-8-22】 [「模型量化技术」可视化指南：A Visual Guide to Quantization](https://mp.weixin.qq.com/s/dgS-yRVpGe_w1uzbcVctXg), 可视化图解各种模型量化技术的原理和实现方法

目录
- 01 第 1 部分：LLMs 存在的“问题”
-     1.1 参数数值（value）的表示方法
-     1.2 内存限制问题
- 02 第 2 部分：模型量化技术简介
-     2.1 常用的数据类型
-         2.1.1 FP16
-         2.1.2 BF16
-         2.1.3 INT8
-     2.2 对称量化 Symmetric Quantization
-     2.3 非对称量化 asymmetric quantization
-    2.4 取值范围的映射与裁剪
-     2.5 校准过程 Calibration
-         2.5.1 权重（和偏置项） Weights (and Biases)
-         2.5.2 激活值
- 03 第 3 部分：Post-Training Quantization
- 
-     3.1 动态量化（Dynamic Quantization）
-     3.2 静态量化（Static Quantization）
-     3.2 探索 4-bit 量化的极限
-         3.2.1 GPTQ
-         3.2.2 GGUF
- 04 第 4 部分：Quantization Aware Training
-     4.1 1-bit LLM 的时代：BitNet
-     4.2 权重的量化 Weight Quantization
-     4.3 激活值的量化 Activation Quantization
-     4.4 反量化过程 Dequantization
-     4.5 所有 LLMs 实际上均为 1.58-bit
-         4.5.1 The Power of 0
-         4.5.2 Quantization 量化过程
- 05 Conclusion

【2024-8-28】天津大学大模型量化报告 [https://blog.csdn.net/2401_85327249/article/details/144079053](https://blog.csdn.net/2401_85327249/article/details/144079053)

`量化`(Quantization)可以很好地通过将**float**模型表征为**低位宽模型**实现减小模型存储空间, 加速模型推理的目标. 

量化定义为: 
> a technique that mapping of a **k-bit integer** to a **float** element, which **saves space** and **speedup computation** by compressing the digital representation. 

LLM 模型推理`吞吐量`和`时延`这两个重要的性能指标上：
- `吞吐量`的提升主要受制于**显存容量**，如果降低推理时显存占用量，就可以运行更大的 batchsize，即可提升`吞吐量`；
- LLM 推理具有 Memory-bound 特点，如果降低访存量，将在`吞吐量`和`时延`两个性能指标上都有收益。

低比特量化技术可以降低**显存占用量和访存量**，加速关键在于:
- 显存量和访存量的节省以及量化计算的加速**远大于**反量化带来的额外开销。

##### 浮点数

【2024-3-1】[一次搞懂FP16、BF16、TF32、FP32](https://zhuanlan.zhihu.com/p/676509123)

英伟达安培架构白皮书
- ![](https://pic4.zhimg.com/80/v2-b596418746b700fb6984a1dd7e1db667_1440w.webp)

新数据类型历史
- FP16 最早是在图形学领域写 shader 相关的语言中引入。
  - 其与8位或16位整数相比,**动态范围高**，可以使高对比度图片中更多细节得以保留。
  - 与单精度浮点数相比，优点是只需要一半的存储空间和带宽（但是会牺牲精度和数值范围）。
- 之后 FP16 随着 Volta 系列 Tensor Core 推出而广泛引用于深度学习，从而发扬光大。 
  - 类似的数据类型还有 INT8 INT4 和 binary 1-bit 精度数据在图灵架构推出。 
  - A100 Tensor Core 增加了 TF32 、BF16 和 FP64 的支持。

这些 Reduced Precision 在算力紧缺的深度学习时代，在精度和性能做了取舍，推动着各种计算任务的发展，而背后真正的不同在于其各自代表的**位宽**和**位模式**不一样。

以单精度浮点数为例： 一个浮点数 (Value) 的表示其实可以这样表示(大多数情况) ：
- Value = sign X exponent X fraction

浮点数的实际值，等于符号位（sign bit）乘以指数偏移值(exponent bias)再乘以分数值(fraction)。

如 2024.0107 实际表示 [工具](https://www.h-schmidt.net/FloatConverter/IEEE754.html)
- ![](https://pic3.zhimg.com/80/v2-b59defbe68831e35cb6557383059fe4e_1440w.webp)
- 不同于定点数，浮点数很多都其实都是近似
- 特殊意义：比如说 nan，inf ，0 之类

(1) FP32 到 BF16 的转换
- ![](https://pic4.zhimg.com/80/v2-b91b8960afe45dcf8835258e9f8c08fb_1440w.webp)
- BF16 组成：1个符号位， 8 个指数位， 举例 `0 11110 1111111111 = 65504` （max half precision）
- 转换: 把 float32 后边多余的位给砍掉

ncnn 代码

```c++
// convert float to brain half
NCNN_EXPORT NCNN_FORCEINLINE unsigned short float32_to_bfloat16(float value)
{
    // 16 : 16
    union
    {
        unsigned int u;
        float f;
    } tmp;
    tmp.f = value;
    return tmp.u >> 16;
}
// convert brain half to float
NCNN_EXPORT NCNN_FORCEINLINE float bfloat16_to_float32(unsigned short value)
{
    // 16 : 16
    union
    {
        unsigned int u;
        float f;
    } tmp;
    tmp.u = value << 16;
    return tmp.f;
}
```

(2) FP32 到 FP16 的转换
- ![](https://pic4.zhimg.com/80/v2-8881579eaa53975812574340134a4367_1440w.webp)
- FP16 和 BF16 位宽一样，但要做起数据类型转换可比 BF16 复杂了不少。 
- FP16 是比 BF16 更早得到广泛应用的数据类型
  - 组成: 1个符号位5个符号位10个尾数位, 这就和 float32 的位模式只有符号位是相同的了。

转换过程三个映射而已：符号位的对应，指数位的对应，尾数位的对应

```c++
// 拆分
unsigned int sign = x & 0x80000000;                   //sign flag
unsigned int mantissa_f32 = x & 0x007FFFFF;           // mantissa
unsigned int exponent_f32 = x & 0x7f800000;           // exp
// 映射 
// ...
```

(3) FP32 vs. TF32

TF32 也是深度学习时代诞生的一种新类型。
- 针对 Nvidia Ampere 的 GPU 模式，一般也是 TensorCore 的中间计算类型，默认情况下将启用。
- 由于使用了 TF32，某些 float32 操作在基于 Ampere 架构的 GPU 上以较低的精度运行，包括乘法和卷积。具体来说，这类运算的输入从 23 位精度四舍五入到 10 位。这对于深度学习模型来说，在实践中不太会造成问题。
- ![](https://pic3.zhimg.com/80/v2-a55efaccc98aed7d341e757687a08cae_1440w.webp)
- TF32 保持了 range 和 FP32 一致，减少了小数位，使用和 half 一样的 10bit 小数位，使得总体位数为 19 个 bit，降低了数据精度，但同时也在安培架构上带来了强劲的性能提升

##### 量化分类

量化可以按不同角度对其进行归类: 
- 按量化**执行阶段** 分为**训练中量化**(`QAT`, Quantization-Aware-Training) 和 **训练后量化**(`PTQ`, Post-Training-Quantization); 
- 按量化**间隔是否等距** 分为`均匀量化`和`非均匀量化`(如图所示). 
- ![](https://pic3.zhimg.com/80/v2-7ab0c2a2269d98f38a0b99ac8a19725e_1440w.webp)

|划分维度|类1|类2|
|---|---|---|
|执行阶段|训练中量化 `QAT`|训练后量化 `PTQ`|
|间隔是否等距|均匀量化|非均匀量化|

这里主要讨论`PTQ`, `均匀量化`. 因为LLMs背景下
- `QAT`目前仍未有机构做出靠谱研究, 主要受限于QAT需要引入**模拟量化**的操作, 会引起**显存&计算量进一步上涨**以及**梯度mismatch**的问题, 从而增加训练成本以及影响Scaling Laws. 
- `非均匀量化`除非有特殊硬件支持, 否则在GPU上目前多数只能通过 **Look-Up-Table** 或 **移位**等方式来实现, 速度和精度没法得到同时保证.

常见量化有两种常见方法：
-   **训练后量化**（Post-Training Quantization，`PTQ`）：模型首先经过训练以达到收敛，然后将其权重转换为较低的精度，而无需进行更多训练。
  - 与训练相比，实施起来通常相当便宜。
-   **量化感知训练**（Quantization-Aware Training，`QAT`）：在**预训练**或**微调**期间应用量化。 
  - QAT 能够获得更好的性能，但需要额外的计算资源和对代表性训练数据的访问。


| 被量化的对象 | 量化方法 | 特点 | 
| --- | --- | --- | 
| 权重量化 | LLM.int8(), GPTQ | 显存占用减半，但由于计算结果需反量化，时延基本无收益 |
| 权重和激活同时量化 | SmoothQuant | 显存占用减半，时延有收益，精度几乎匹配 FP16 | 
| KV Cache量化 | INT8 或 FP8 量化 | 方法简单，吞吐量收益明显 | 
| 基于硬件特点的量化：英伟达 Hopper 架构下的 FP8 | 直接利用 TensorCore FP8 计算指令 | 不需要额外的量化/反量化操作，时延收益明显 |

四类量化方法各有特点，业界在低比特量化方向的研究进展也层出不穷，希望探索出一个适用于大语言模型的、能够以较高压缩率压缩模型、加速端到端推理同时保证精度的量化方法。


##### 量化原理

模型大小由其**参数量**及其**精度**决定，精度通常为 `float32`、`float16` 或 `bfloat16`
-   **Float32 (FP32)** 。标准的 IEEE 32 位浮点表示，指数 8 位，尾数 23 位，符号 1 位，可以表示大范围的浮点数。大部分硬件都支持 FP32 运算指令。
-   **Float16 (FP16)** 。指数 5 位，尾数 10 位，符号 1 位。FP16 数字的数值范围远低于 FP32，存在上溢 (当用于表示非常大的数时) 和下溢 (当用于表示非常小的数时) 的风险，通过缩放损失 (loss scaling) 来缓解这个问题。
-   **Bfloat16 (BF16)** 。指数 8 位 (与 FP32 相同)，尾数 7 位，符号 1 位。这意味着 BF16 可以保留与 FP32 相同的动态范围。但是相对于 FP16，损失了 3 位精度。因此，在使用 BF16 精度时，大数值绝对没有问题，但是精度会比 FP16 差。
-   **TensorFloat-32(TF32)** 。使用 19 位表示，结合了 BF16 的范围和 FP16 的精度，是计算数据类型而不是存储数据类型。目前使用范围较小。
- ![](https://pic2.zhimg.com/80/v2-500915ea5b15c798bdc00d679fdeb229_1440w.webp)

模型训练
- 训练时为保证精度，主权重始终为 `FP32`。
- 而推理时，`FP16` 权重通常能提供与 `FP32` 相似的精度

推理时使用 `FP16` 权重，仅需一半 GPU 显存就能获得相同的结果。那么是否还能进一步减少显存消耗呢？答案是用`量化`技术，最常见的就是 `INT8` 量化。
- ![](https://pic3.zhimg.com/80/v2-df305ab18d1a433744f877264c3c3a5a_1440w.webp)

INT8 量化即将浮点数 xf 通过缩放因子 scale 映射到范围在 `[-128, 127]` 内的 8bit 表示 xq, 即: 
- $ x_{q}=\operatorname{Clip}\left(\operatorname{Round}\left(x_{f} / \text { scale }\right)\right) $
- $ scale = (2*max(\left | x_f \right | ))/254 $
- Round 表示四舍五入都整数，Clip 表示将离群值(Outlier) 截断到 [-128, 127] 范围内。

量化-反量化例子
- ![](https://pic4.zhimg.com/80/v2-af2eaf59e0e9409d1587fe9ba82dadcb_1440w.webp)

进行矩阵乘法时，可以通过组合各种技巧，例如逐行或逐向量量化，来获取更精确的结果。举个例子，对矩阵乘法，我们不会直接使用常规量化方式，即用整个张量的最大绝对值对张量进行归一化，而会转而使用向量量化方法，找到 A 的每一行和 B 的每一列的最大绝对值，然后逐行或逐列归一化 A 和 B 。最后将 A 与 B 相乘得到 C。最后，我们再计算与 A 和 B 的最大绝对值向量的外积，并将此与 C 求哈达玛积来反量化回 FP16。


由于 GPU 内核缺乏对某些类型的**矩阵乘法**（例如 INT4 x FP16）的支持，理论最优量化策略与硬件内核支持之间的差距，并非以下所有方法都能加速实际推理。

两个公式
- ![](https://pic4.zhimg.com/80/v2-1e445bb92a842afb930f8f03e2850d03_1440w.webp)
- 1式中, `Q(·)`表示量化操作, `X`代表输入tensor, `S`即为scale, `Z`即为zero-point, `b`为量化位宽。
- 1式称为`quantization`, 2式称为 `de-quantization`. 
- `S`和`Z`统称为量化参数, 多数的量化算法可以理解为找到更好的S和Z使得量化模型的结果尽可能逼近原模型的结果. 

LLMs模型推理大致分为两个stage: **context** and **generation**. 
- 在context阶段：causal attention 因果注意力, 其行为可以类比训练的**前向过程**; 
- generations阶段：sequence length恒等于1。

这就要求推理框架需要支持**两套**计算逻辑(在FasterTransformer中可以看出)以适配其不同的特点. 在多数情况下, context阶段是**compute bound**(这不一定, 需要seqlen大于计算强度), 而generation是**IO bound**. 

很多情况下, generation较context在应用中出现频率更高, 而量化模型由于其低位宽的权重表征, 可以大大缓解IO bound现象. (当然如果在服务时使得batch化技术来加大一次推理的batch的话, 量化的效果可能会退化为节约模型存储(功耗)下降).

关于量化的基本原理和实现细节，可参考笔者之前的文章：
- [大语言模型的模型量化(INT8/INT4)技术](https://zhuanlan.zhihu.com/p/627436535)

许多关于 Transformer 模型量化的研究都有相同的观察结果：简单的低精度（例如 8 bit）训练后量化会导致性能显着下降，这主要是由于动态的 activation 和静态的 weight 量化策略无法保持一致。
- ![](https://pic1.zhimg.com/80/v2-9824082fcbbcba958934a4a4f5eab918_1440w.webp)

为了不损失精度而提高性能，可以考虑 WeightOnly 量化技术，即只把 Weight 量化成 int8 格式，以降低访存压力。到实际 Kernel 内部再 Dequantize 回 fp16，进行矩阵乘计算。这种方法在 BS 较小是比较有效(因为此时的瓶颈在IO)，BS 较大时(因为此时的瓶颈在计算)效果变差。
- ![](https://pic4.zhimg.com/80/v2-58705e83db3886efa8206769eb4d657b_1440w.webp)

WeightOnly 量化的典型案例是 [AWQ: Activation-aware Weight Quantization](https://arxiv.org/pdf/2306.00978.pdf)，即只对 weight 进行量化以实现压缩和加速的效果。

##### LLMs 量化方法

常见方法
- LLM.in8
- SmoothQuant
- GPTQ

(1) [LLM.int8()](https://arxiv.org/abs/2208.07339)

由于input的outliers只会固定在几个特定的hidden-dim的特点(LLaMA模型中也有该现象, 且随着模型加深越发严重. RMSNorm引起), 且outliers占据的dims很少(不到1%). 故提出将Linear拆成两部分, 一部分为`int8`, 一部分为`fp16`, 分别计算后相加. 该方法得到广泛的应用, 有两个方面
- 一个是因为被huggingface集成
- 另一个是因为其几乎不掉点. 

但该方法的缺点也是比较明显: 
- 模型量化仅到8bit, 仍是4bit的2倍大; 
- Linear的latency大幅上升, 原因在于它拆成两个matmul kernel, 而且后续为了fp16相加引入外积操作等, 即计算流程更为复杂多步.
- ![](https://pic4.zhimg.com/v2-af08f0cdb101569e054d26af4d984e6f_b.jpg)


(2) ZeroQuant系列
- [v1](https://arxiv.org/abs/2206.01861)
- [v2](https://arxiv.org/abs/2303.08302))

首次对采用input token-wise quantization 并结合 weight group-wise quantization; 另外设计LKD(Layerwise Knowledge Distillation, 使用随机生成的数据); 同时, 还做了一些kernel fused的工作, 实现了一个适配于int8的backend. 这系列的工作都比较像technical report, 且适用的模型尺寸比较小, 均在20B以下. 方法的scaling效果较差, 建议follow其量化粒度的设计.

(3) [SmoothQuant](https://arxiv.org/abs/2211.10438)

同样是为了解决input outlier的问题, `韩松`团队提供将input的动态范围除上scale(该scale > 1即可以实现动态范围减小, 从而改善量化结果), 并将该scale吸到下一层的weight内, 利用weight的细粒度量化来承担该量化困难(因为input往往使用token-wise quantization, 而weight通常使用channel-wise quantization或group-wise quantization). 相较于LLM.int8(), **由于input和weight全都是int8**, 并不会出现复杂的计算逻辑, 可以调用CUTLASS默认实现的int8 gemm来加速. 其缺点为: 精度没有LLM.int8()有保证, 且容易受到calibration-set的影响), 同时一旦weight精度调至4bit, 则模型精度下滑严重)
- ![](https://pic2.zhimg.com/80/v2-95f07c67325401e2c64a3f93701db989_1440w.webp)

(3) **[GPTQ](https://arxiv.org/abs/2210.17323)**

经典之作, 目前几乎是4bit/3bit方案的**默认首选**, 但也仅限于开源世界的娱乐可用, 离落地认定的靠谱精度还是有比较大的距离. 源于同一团队在nips22的工作([Optimal Brain Compression](https://arxiv.org/abs/2208.11580))延伸, 其同样将方法泛化到剪枝领域(也是大模型剪枝领域的经典, SparseGPT). 该方法的思路大致为: 利用hessian信息作为准则判定每个权重量化后对输出loss(通常定义为MSE)造成的影响, 量化影响最大的权重(即最敏感)挑选出来先进行量化, 然后对其他权重进行更新来补偿该权重量化导致的影响, 如此往复, 直至全部量化结果. 当然, 在GPTQ中作了一些简化, 比如是基于列元素进行量化循环, 来减少算法的运行时间. 该方法的优点: 首次将4bit/3bit权重量化在176B的模型上做work, 同时也提出对应的kernel(但比较糙, 优化空间大, 有不少团队做了优化). 缺点: 4bit/3bit的方案原始kernel由于有unpack操作, 导致gemv操作的计算时间低于fp16), 且精度距离落地有明显距离. 注: 从它开始, 很多人只开始研究4w16f的方案(即weight-only quantization), 因为在batch=1的gemv计算中, 只需要控制权重的读入时间即可, 且input的动态范围过大, 量化掉点过大.

(4) **[AWQ, Activation-aware Weight Quantization](https://arxiv.org/abs/2306.00978)**

SmoothQuant的续作, 从源代码来看, 它对SmoothQuant中计算scale时需要的超参alpha, 增加 了一步通过grid search得到每个scale的最优参数, 但论文的故事包装得很好, 同时取得的效果也是十分显著的, 符合大道至简的准则. 该方案是也是4-bit weight-only quantization, 其kernel实现凭借对PTX的深刻理解和应用, 取得了目前这些weight-only quantization的方案的第一. 在此基础上稍加优化即可以得到一个不错的baseline.

(5) **[SqueezeLLM](https://arxiv.org/abs/2306.07629)**

通过观察到部分权重决定了最终模型的量化性能, 提出以非均匀量化的方式缩小这些敏感权重的量化误差. 即通过loss的二阶hessian信息来确定量化敏感的权重, 将量化点安置在这些敏感权重附近, 其它点以MSE最小来安置. 该方法以少量的存储空间换来了目前最优的4-bit weight精度, 但其缺点也是极其明显: 由于采用LUT来实现非均匀量化, 导致其kernel在batch > 1(文中的batch我均定义为 batch \* seqlen)的情况下, Linear的执行速度急剧下滑。
- ![](https://pic3.zhimg.com/80/v2-2d1dd16e6a853fb194a503e01562531e_1440w.webp)

(6) **QLoRA**

这里顺带简单介绍一下QLoRA. 该方法提出4-bit NormalFloat, 一种新的数制(属于非均匀量化), 从理论角度上证明是4bit最优数制。 利用该方法量化模型的backbone得到4-bit的backbone, 然后基于lora进行SFT, 在只需要4-bit模型权重的情况下完成SFT, 从而使得许多人可以实现在单张消费级卡(i.e. 3080)上玩LLaMA。但当时我跑它的时候, 其缺点就是明显的kernel速度慢, 原因同样是因为它需要通过LUT来实现, 不知道现在情况怎么样了.

**Summary & Future**

4-bit weight-only quantization是一个相对比较均衡的方案。 在这个setting下, 量化的研究工作应更多集中在模型的精度提升的层面上, 尽可能地减少对模型智能的影响. 但对于如果想进一步得到更轻更快更强的模型, 可以从其他小型化策略入手. 在这些策略中, 蒸馏是一个最值得往前走的方案. 在LLaMA-2的tecnical report中就有多处地方使用了蒸馏, 比如: 在RLHF阶段仅用70B的reject sampling dataset来fine-tuning其他几个小尺寸的模型, 以及很多人都会尝试去用GPT4的SFT数据来fine-tuning自己的模型. 剪枝不太推荐, 因为至少从SparseGPT的复现结果来看, 除了非结构化剪枝精度还算有保证外, 其余方案精度下滑明显, 包括NV的2:4和4:8方案, 距离落地还有些距离, 且和量化结合后并不能进一步拿到50%的压缩收益。最后, 再提几点我认为有可能的方向:
-   更加系统全面地推理优化,包括: 更深度更大粒度的kernel-fusion, 其他部件优化(i.e. long context 下kv-cache的存储和IO时间, attention计算优化), system2的推理路径的优化
-   在模型训练中引入量化友好的策略, 来使得模型的权重和激活可以变得对量化不敏感, 从而实现4w4f
-   尝试引入QAT方案, 达到所见即所得, 拥抱极限 -- 但这个有点太激进, 还是需要在模型有足够理解后去尝试.
-   端云推理的协同优化, 即手机端和GPU之间如何交互, 利用手机端训个人SFT, 分配算力等


##### 量化实践



###### bitsandbytes3

bitsandbytes 基于 `LLM.int8()` 和 8 比特优化器论文中介绍的方法开发而成。

该库主要专注于大语言模型的 INT8 量化，主要提供对 8 比特矩阵乘法和 8 比特优化器的支持。
- 目前，bitsandbytes 还支持 4 比特的权重量化和混合精度分解方法，包括 NF4（4-bit NormalFloat）和 FP4 数据类型，可以进行加速模型的输出解码以及基于 QLoRA 的轻量化微调。
- 使用上，bitsandbytes 已经集成在 HuggingFace 中，加载模型时直接通过运行参数指定实现对模型权重的量化。
- 例如，可以使用参数 load_in_8bit 和 load_in_4bit 对模型进行 8 比特和 4 比特量化

###### PyTorch 量化

Quanto：pytorch量化工具包
1. quanto是一个灵活的pytorch量化工具包,提供了独特的功能:
  - 支持eager模式(可用于非可trace的模型)
  - 量化后的模型可在任意设备上运行(包括CUDA和MPS)  
  - 自动插入量化和反量化代码
  - 自动插入量化的函数操作
  - 自动插入量化的模块(如QLinear、QConv2d等)
  - 提供从动态到静态量化的流程  
  - 支持量化模型的状态字典序列化
  - 不仅支持int8权重,还支持int2和int4
  - 不仅支持int8激活,还支持float8
2. 典型的量化流程包括:量化、校准、调优和冻结。
3. quanto与huggingface transformers库深度集成,可通过QuantoConfig来量化任意模型。
4. quanto的实现细节:
  - 提供了针对不同量化类型的定制Tensor子类
  - 提供了可处理quanto tensor的量化模块,如QLinear、QConv2d等
  - 通过pytorch dispatch机制,实现了常见函数的量化版本
  - 计划集成各种PTQ优化算法
5. quanto的性能:
  - 在多个模型上展示了不同量化配置的准确率
  - 展示了相比全精度,量化带来的加速比

《[Quanto: a pytorch quantization toolkit](https://huggingface.co/blog/quanto-introduction)》


###### Mixtal GPTQ

huggingface上[thebloke](https://huggingface.co/TheBloke)，每出一个新模型，就会上传对应的量化模型
- 目前已经有 3181 个量化模型
- [Mixtral-8x7B-v0.1-GPTQ](https://huggingface.co/TheBloke/Mixtral-8x7B-v0.1-GPTQ/tree/main )

【2024-1-10】智源团队提出首个用于自然语言理解任务的 **1bit** 轻量化预训练模型 `BiPFT`。与标准的FP32相比，使用 1bit weight 和 1bit activation，在推理阶段显著节省了56倍的操作数量和28倍的内存。该工作已被 AAAI 2024 收录。

与以往面向特定任务的 1bit Transformer结构的模型相比，BiPFT显著提升了 1bit 神经网络（BNN）的学习和泛化能力，与直接在下游任务上进行二值量化的BERT模型相比，BiPFT 模型在GLUE标准测试集上平均性能超过15.4%。


###### BitNet -- 1 Bit 量化

【2023-10-29】[BitNet：用1-bit Transformer训练LLM](https://zhuanlan.zhihu.com/p/663967487): 可扩展且稳定的 1-bit Transformer架构来实现大语言模型，称为`BitNet`。
- 使用BitLinear作为标准nn的替代品。

实验结果
- `BitNet`能够显著减少存储占用和能力消耗，并且与最先进的`8-bit`量化和`FP16` Transformer能力相当。
- BitNet也表现出了类似于全精度Transformer的scaling law
- 这也表明其有潜力在保持效率和性能的同时，能够更加有效的扩展至更大的语言模型。

模型结构
- ![](https://pic4.zhimg.com/80/v2-7b080895d67f263b9832849898b6650f_1440w.webp)

BitNet采用与Transformer相同的布局，但是采用BitLinear而不是标准的矩阵乘法，其他组件仍保持高精度。原因如下：
- (1) 残差连接和Layer Normalization的计算代价对于LLM可以忽略不计；
- (2) 随着模型增大，QKV变换的计算代价远小于投影；
- (3) 保留输入/输出嵌入层的精度，因为语言模型必须使用高精度来执行采样。

【2024-2-28】微软 [The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits](https://huggingface.co/papers/2402.17764) BitNet b1.58
- [bitnet](https://github.com/microsoft/unilm/tree/master/bitnet)
- [BitNet: Scaling 1-bit Transformers for Large Language Models](https://arxiv.org/pdf/2310.11453.pdf)

1 Bit LLM变体，即BitNet b1.58
- LLM的每个参数(或权重)都是**三进制** `{- 1,0,1}`。在困惑度和最终任务性能方面，它与全精度(即FP16或BF16) Transformer LLM相匹配，具有相同的模型大小和训练token，同时在延迟、内存、吞吐量和能耗方面明显更具有成本效益。
- 1.58位LLM定义了新的缩放规律和训练新一代高性能且具有成本效益的LLM的方法。
- 此外，实现了一种新的计算范式，并为设计针对1位llm优化的特定硬件打开了大门。


#### 2.3 蒸馏(Distillation)

[知识蒸馏](https://arxiv.org/abs/2006.05525)是一种构建更小、更便宜的模型（“student 模型”）的直接方法，通过从预先训练的昂贵模型中转移技能来加速推理（“ teacher 模型”）融入 student。 除了与 teacher 匹配的输出空间以构建适当的学习目标之外，对于如何构建 student 架构没有太多限制。

![](https://pic2.zhimg.com/80/v2-9dfcd56236628ab5d5e81c8a88f9e081_1440w.webp)

知识蒸馏基本框架

给定数据集，训练 student 模型通过蒸馏损失来模仿 teacher 的输出。 通常神经网络有一个softmax层； 例如，LLM 输出 token 的概率分布。 将 softmax 之前的 logits 层表示为 $\mathbf{z}_t$$\mathbf{z}_t$\\mathbf{z}\_t 和 $\mathbf{z}_s$$\mathbf{z}_s$\\mathbf{z}\_s , 分别表示 teacher 和 student 模型。 蒸馏损失最小化两个 softmax 输出之间的差异（温度 $T$$T$T ）。 当标签 $y$$y$y 已知，可以将其与student 的 logits 之间计算交叉熵，最后将两个损失相加，如下：

$\mathcal{L}_{\mathrm{KD}}=\mathcal{L}_{\text {distll }}\left(\operatorname{softmax}\left(\mathbf{z}_t, T\right), \operatorname{softmax}\left(\mathbf{z}_s, T\right)\right)+\lambda \mathcal{L}_{\mathrm{CE}}\left(\mathbf{y}, \mathbf{z}_s\right)$$\mathcal{L}_{\mathrm{KD}}=\mathcal{L}_{\text {distll }}\left(\operatorname{softmax}\left(\mathbf{z}_t, T\right), \operatorname{softmax}\left(\mathbf{z}_s, T\right)\right)+\lambda \mathcal{L}_{\mathrm{CE}}\left(\mathbf{y}, \mathbf{z}_s\right)$\\mathcal{L}\_{\\mathrm{KD}}=\\mathcal{L}\_{\\text {distll }}\\left(\\operatorname{softmax}\\left(\\mathbf{z}\_t, T\\right), \\operatorname{softmax}\\left(\\mathbf{z}\_s, T\\right)\\right)+\\lambda \\mathcal{L}\_{\\mathrm{CE}}\\left(\\mathbf{y}, \\mathbf{z}\_s\\right)

在 Transformer 中一个典型案例是[DistilBERT](https://arxiv.org/abs/1910.01108)，模型参数减少 40%，速度提升71%。在大模型时代，蒸馏可以与量化、剪枝或稀疏化技术相结合，其中 teacher 模型是原始的全精度密集模型，而 student 模型则经过量化、剪枝或修剪以具有更高的稀疏级别，以实现模型的小型化。

### 三、并行化（Parallelism）

大语言模型参数量较大，可能无法存放到单一计算设备中，分布式并行可以有效解决该问题。
- 分布式并行中的`模型并行`和`流水线并行`已在 LLM 推理中得到应用。

当前的推理的并行化技术主要体现在3个维度上，即 3D Parallelism:
-   Data Parallelism(DP)
-   Tensor Parallelism(TP)
-   Pipeline Parallelism(PP)

![](https://pic1.zhimg.com/80/v2-a2af7781f1545f571af334383f3d5994_1440w.webp)

3D Parallelism 的3个维度

#### 模型并行

模型并行通过将权重参数拆分到多个计算设备中，实现分布式计算。

模型并行两种常见方式：`Column Parallel`和`Row Parallel`
- ![](https://pic3.zhimg.com/80/v2-a45b0473f37abc31eae88f884d619642_1440w.webp)
- 第一行代表 `Column Parallel`，即将权重数据按**列**拆分到多个 GPU 中，每个 GPU 上的本地计算结果需要在列方向拼接为最终结果；
- 第二行代表 `Row Parallel`，即将权重数据按**行**拆分到多个 GPU 中，每个 GPU 上的本地计算结果需要 AllReduce 规约为最终结果。

业界最流行的模型并行方案来自 `Megatron-LM`，其针对 `Self-Attention` 和 `MLP` 分别设计了简洁高效的模型并行方案。
- `MLP`: 第一个全连接层为 Column Parallel，第二个全连接层为 Row Parallel，整个 MLP 只需在 Row Parallel 后执行一次 AllReduce 规约操作即可。
- `Self-Attention`：在计算 Query、Key 和 Value 向量时执行 Column Parallel（按注意力头个数均分到每个 GPU），在将注意力得分做空间映射时执行 Row Parallel，整个 Self-Attention 只需在 Row Parallel 后执行一次 AllReduce 规约操作即可。
- ![](https://pic2.zhimg.com/80/v2-114609093612ed46388ffd3f1576ab49_1440w.webp)

上面分析了 Transformer layer 的模型并行方式。除此之外，LLM 模型中的
- Input Embedding 采用 `Row Parallel`，Output Embedding 采用 `Column Parallel`；
- Dropout / Layer Norm / Residual Connections 等操作都没有做并行拆分。例如 Layer Norm 的权重参数和计算，在每个 GPU 上都是完整的。

| Layers | Model Parallel Method |
| --- | --- |
| Input Embedding | Row Parallel |
| Self-Attention | Column Parallel + Row Parallel |
| MLP | Column Parallel + Row Parallel |
| Output Embedding | Column Parallel |

以 LLaMA-34B 模型为例进行通信量分析。该模型包含 48 个 Transformer layers，隐藏层大小 8192，每次单 batch 推理共 `2*48=96` 次 Broadcast 和 `2*48=96` 次 AllReduce 操作，每次通信传输的数据量均为 16 KB（此处假设数据类型为半精度浮点，8192*2/1024=16 KB）。

考虑到推理服务一般都是按多 batch 推理执行，假设 batchsize 为 64，每次通信传输的数据量也仅为 1 MB。下图在 A100-PCIE-40GB 机器上测试 NCCL AllReduce 带宽数据，PCIE 理论带宽为 32-64 GB/s 左右，实际推理场景下的通信数据量主要集中在 1 MB 以下，对应的实际带宽约为 1-10 GB/s。NVLink 理论带宽为 400-600 GB/s，但由于每次的通信量很小，实际带宽也远远小于理论带宽。

因此模型参数量越大、batchsize 越大，通信效率越高，使用模型并行获得的收益约明显。
- ![AllReduce实际带宽测试](https://pic3.zhimg.com/80/v2-4cc9d47777fdd98e7bbdd7e1f699f216_1440w.webp)


#### 3.1 数据并行 (Data Parallelism, DP)

在推理中，DP 主要是增加设备数来增加系统整体 Throughput，其中最经典的即DeepSpeed的Zero系列

![](https://pic4.zhimg.com/80/v2-7eca670d33d4ac372507c02038970123_1440w.webp)

另外 FSDP 也比较高效和易用

![](https://pic1.zhimg.com/80/v2-cf1d706571abca543117f453e9289d20_1440w.webp)

#### 3.2 张量并行(Tensor Parallelism, TP)

在推理中，TP 主要是**横向**增加设备数通过并行计算来减少 latency，其实现原理及细节可参考笔者之前的文章
- [GPT 的张量并行化（tensor parallelism）方案](https://zhuanlan.zhihu.com/p/603908668)

当前也有一些方便易用的 TP 方案，如 [BlackSamorez/tensor\_parallel](https://github.com/BlackSamorez/tensor_parallel) ，使用起来非常简单：

```py
import transformers
import tensor_parallel as tp
tokenizer = transformers.AutoTokenizer.from_pretrained("facebook/opt-13b")
model = transformers.AutoModelForCausalLM.from_pretrained("facebook/opt-13b")  # use opt-125m for testing

model = tp.tensor_parallel(model, ["cuda:0", "cuda:1"])  # <- each GPU has half the weights

inputs = tokenizer("A cat sat", return_tensors="pt")["input_ids"].to("cuda:0")
outputs = model.generate(inputs, num_beams=5)
print(tokenizer.decode(outputs[0])) # A cat sat on my lap for a few minutes ...

model(input_ids=inputs, labels=inputs).loss.backward()  # training works as usual
```

当前主流的推理框架都支持 TP 的方式，包括但不限于：
-   [Megatron-LM](https://arxiv.org/pdf/1909.08053.pdf)
-   [FasterTransformer](https://github.com/NVIDIA/FasterTransformer)
-   [DeepSpeed Inference](https://github.com/microsoft/DeepSpeed/tree/master/deepspeed/inference)
-   [vLLM](https://github.com/vllm-project/vllm)
-   [Text Generation Inference](https://github.com/huggingface/text-generation-inference)
-   [ParallelFormers](https://github.com/tunib-ai/parallelformers)
-   [ColossalAI](https://github.com/hpcaitech/ColossalAI)
-   [FlexFlow](https://github.com/flexflow/FlexFlow)
-   [LiBai](https://github.com/Oneflow-Inc/libai)
-   [AlpaServe](https://arxiv.org/pdf/2302.11665.pdf)

#### 3.3 流水线并行(Pipeline Parallelism, PP)

在推理中，PP 主要是纵向增加设备数通过并行计算来支持更大模型，同时提高设备利用率。

![](https://pic2.zhimg.com/80/v2-53ac64265bc0ce890b783956741169b1_1440w.webp)

通常来说，PP 需要与 TP 结合以支持更大模型，并实现最佳效果

![](https://pic2.zhimg.com/80/v2-e8d2aad9d31b31e5f01ec9a71cf3eae5_1440w.webp)

### 四、Transformer 结构优化 -- 显存优化

该类方法主要通过优化 Transformer 的结构以实现推理性能的提升。
- 【2023-9-12】[LLM推理优化技术综述](https://zhuanlan.zhihu.com/p/655325832)：KVCache、PageAttention、FlashAttention、MQA、GQA

#### KV Cache

大模型推理性能优化一个最常用技术就是 `KV Cache`，该技术可以在**不影响任何计算精度**的前提下，通过<span style='color:red'>空间换时间</span> 提高推理性能。
- 目前业界主流 LLM 推理框架均默认支持并开启了该功能。

Transformer 模型具有`自回归推理`的特点
- 每次推理只会预测输出一个 token，当前轮输出token 与历史输入 tokens 拼接，作为下一轮的输入 tokens，反复执行多次。
  - 前i次的token会作为第i+1次的预测数据送入模型，拿到第i+1次的推理token
  - Transformer会执行**自注意力**操作，要给当前序列中的每个项目（无论是prompt/context还是生成的token）提取键值（kv）向量
  - 这些向量存储在一个矩阵中，通常被称为`kv cache`。
- 该过程中，前后两轮的输入只相差一个 token，存在重复计算。

`KV Cache` 技术实现了将**可复用**的键值向量结果保存下来，从而避免了重复计算。
- ![](https://pic4.zhimg.com/80/v2-1201b9194f2a70641f1d50f92735b093_1440w.webp)

利用预先计算好的k值和v值，可以节省大量计算时间，尽管这会占用一定的存储空间。
- ![](https://pic2.zhimg.com/80/v2-687227f17dda44a482648e24b0d8f515_1440w.webp)

LLM推理优化方案是<span style='color:blue'>尽可能减少推理过程中kv键值对的重复计算，实现kv cache的优化</span>。

KV Cache 技术
- 每次自回归推理过程中，将 Transformer 每层的 Attention 模块中的 $ X_i*W_k $ 和 $ X_i*W_v $ 结果保存保存在一个数据结构（称为 KV Cache）中（如图）
- 当执行下一次自回归推理时，直接将 $ X_i+1*W_k $ 和 $ X_i+1*W_v $ 与 KV Cache 拼接在一起，供后续计算使用（如图）。其中，$ X_i $ 代表第 i 步推理的输入，$ W_k $ 和 $ W_v $ 分别代表键值权重矩阵。
- ![](https://pic3.zhimg.com/80/v2-b7ecf6c42d8368c54128d5005f4e10b2_1440w.webp)

KV Cache 缓存每一轮已计算完毕的键值向量，因此会额外增加显存开销。
- KV Cache 与 batchsize 和序列长度呈线性关系。

KV Cache 的引入也使得推理过程分为如下两个不同阶段，进而影响到后续的其他优化方法。
- **预填充**阶段：发生在计算第一个输出 token 过程中，计算时需要为每个 Transformer layer 计算并保存 key cache 和 value cache；FLOPs 同 KV Cache 关闭一致，存在大量 GEMM (GEneral Matrix-Matrix multiply) 操作，属于 Compute-bound 类型计算。
- **解码**阶段：发生在计算第二个输出 token 至最后一个 token 过程中，这时 KV Cache 已存有历史键值结果，每轮推理只需读取 Cache，同时将当前轮计算出的新的 Key、Value 追加写入至 Cache；GEMM 变为 GEMV (GEneral Matrix-Vector multiply) 操作，FLOPs 降低，推理速度相对预填充阶段变快，这时属于 Memory-bound 类型计算。


目前减少`KV cache`的手段有许多，比如: `page attention`、`MQA`、`MGA`等，另外`flash attention`可以通过硬件内存使用的优化，提升推理性能。

#### 4.1 Flash Attention

Flash attention 推理加速技术利用**GPU硬件非均匀**的存储器层次结构实现内存节省和推理加速
- 论文: “FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness”。通过合理的应用GPU显存实现IO的优化，从而提升资源利用率，提高性能。
- ![](https://pic1.zhimg.com/80/v2-ada97a75b2bfa1bd67d653cda8edf2d8_1440w.webp)

硬件机制
- 计算速度越**快**的硬件往往越**昂贵**且**体积越小**

Flash attention 核心原理: 尽可能地合理应用SRAM内存计算资源。

A100 GPU有40-80GB的高带宽内存(HBM)，带宽为1.5-2.0 TB/s，而每108个流处理器有192KB的SRAM，带宽估计在19TB/s左右。存在一种优化方案是利用SRAM远快于HBM的性能优势，将密集计算尽放在SRAM，减少与HBM的反复通信，实现整体的IO效率最大化。
- 比如可以将矩阵计算过程，softmax函数尽可能在SRAM中处理并保留中间结果，全部计算完成后再写回HBM，这样就可以减少HBM的写入写出频次，从而提升整体的计算性能。

如何有效分割矩阵的计算过程，涉及到flash attention的核心计算逻辑Tiling算法，这部分在论文中也有详细的介绍。

实现细节参考文章
- [从 FlashAttention 到 PagedAttention, 如何进一步优化 Attention 性能](https://zhuanlan.zhihu.com/p/638468472)

[FlashAttention-v2](https://tridao.me/publications/flash2/flash2.pdf) 在原基础上做了改进，使其在算法、并行化和工作分区等方面都有了显著改进，对大模型的适用性也更强。在A100 上性能数据如下：
- ![](https://pic2.zhimg.com/80/v2-d393f3e1d664cff181026a7b754ffefd_1440w.webp)

###### Flash-Decoding

【2023-10-17】[Flash-Decoding方法](https://www.toutiao.com/w/1779986529500173)

斯坦福博士新作：长上下文LLM推理速度提8倍

FlashAttention团队最近推出了Flash-Decoding方法，用于在Transformer架构大模型推理时加速。该方法通过并行计算每个token的注意力值，并在每一步计算过程中使用FlashAttention的优化，从而使长上下文推理变得更快。该方法已经在64k的CodeLlama-34B上得到了验证，并得到了PyTorch官方认可。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/a1536478fcef433d9bb519b550f8a01e~tplv-obj:1372:1104.image?_iz=97245&from=post&x-expires=1705276800&x-signature=AbeQQ0TeRp8fzagHuqsN3sqLIjs%3D)

#### 4.2 PagedAttention 显存优化, vLLM

LLM 推理服务的`吞吐量`指标主要受制于**显存限制**。
- 现有系统由于缺乏精细的显存管理方法而浪费了 60% 至 80% 的显存，浪费的显存主要来自 KV Cache。

因此，有效管理 KV Cache 是一个重大挑战。

Paged Attention 之前，业界主流 LLM 推理框架在 KV Cache 管理方面均存在一定的低效。
- HuggingFace Transformers 库中，KV Cache 是随着执行动态申请显存空间，由于 GPU显存分配耗时一般都高于 CUDA kernel 执行耗时，因此动态申请显存空间会造成极大的时延开销，且会引入显存碎片化。
- FasterTransformer 中，预先为 KV Cache 分配了一个充分长的显存空间，用于存储用户的上下文数据。
  - 例如 LLaMA-7B 的上下文长度为 2048，则需要为每个用户预先分配一个可支持 2048 个 tokens 缓存的显存空间。如果用户实际使用的上下文长度低于2048，则会存在显存浪费。

Paged Attention 将传统操作系统中对内存管理的思想引入 LLM，实现了一个高效的显存管理器，通过精细化管理显存，实现了在物理非连续的显存空间中以极低的成本存储、读取、新增和删除键值向量。

具体来讲，Paged Attention 将每个序列的 KV Cache 分成若干块，每个块包含固定数量token 的键和值。
- 首先在推理实际任务前，会根据用户设置的 max_num_batched_tokens 和 gpu_memory_util 预跑一次推理计算，记录峰值显存占用量 peak_memory，然后根上面公式获得当前软硬件环境下 KV Cache 可用的最大空间，并预先申请缓存空间。其中，max_num_batched_tokens 为部署环境的硬件显存一次最多能容纳的 token 总量，gpu_memory_util 为模型推理的最大显存占用比例，total_gpu_memory 为物理显存量， block_size 为块大小（默认设为 16）。
- 实际推理过程中，维护一个逻辑块到物理块的**映射表**，多个逻辑块可以对应一个物理块，通过引用计数来表示物理块被引用的次数。当引用计数大于一时，代表该物理块被使用，当引用计数等于零时，代表该物理块被释放。通过该方式即可实现将地址不连续的物理块串联在一起统一管理。

Paged Attention 技术开创性地将操作系统中的分页内存管理应用到 KV Cache 的管理中，提高了显存利用效率。另外，通过 token 块粒度的显存管理，系统可以精确计算出剩余显存可容纳的 token 块的个数，配合后文 Dynamic Batching 技术，即可避免系统发生显存溢出的问题。

`PageAttention` 是目前`kv cache`优化的重要技术手段，目前最热的大模型推理加速项目`vLLM`核心就是PageAttention技术。
- 在缓存中 KV cache 都很大，并且大小是动态变化的，难以预测。已有系统中，由于**显存碎片**和**过度预留**，浪费了**60%-80%**的显存。
- PageAttention提供了一种技术手段解决显存碎片化的问题，从而可以减少显存占用，提高KV cache可使用的显存空间，提升推理性能。

首先，PageAttention命名灵感来自OS系统中**虚拟内存和分页**思想。可以实现在**不连续**空间存储**连续**的kv键值
- ![](https://pic3.zhimg.com/v2-e8a2317d1bc7ba5670ca05f68196453e_b.webp)
- 所有键值都是分布存储的，需要通过**分页**管理彼此的关系。序列的连续逻辑块通过 block table 映射到非连续物理块。
- ![](https://pic1.zhimg.com/v2-9eb51279b185b0fa6a8caa2f897a16b4_b.webp)
- 同一个prompt生成多个输出序列，可以共享计算过程中的attention键值，实现copy-on-write机制，即只有需要修改的时候才会复制，从而大大降低显存占用。
- ![](https://pic2.zhimg.com/v2-54d48356549a5a995213b4d0b2c090bd_b.jpg)

可参考
- [从 FlashAttention 到 PagedAttention, 如何进一步优化 Attention 性能](https://zhuanlan.zhihu.com/p/638468472)


#### MHA/GQA/MQA优化技术

LLAMA2的论文提到了相关技术用来做推理优化，目前`GQA`和`MQA`也是许多大模型推理研究机构核心探索的方向。
- `MQA`，全称 Multi Query Attention
  - `MQA` 让所有的头之间共享同一份 Key 和 Value 矩阵，每个头只单独保留了一份 Query 参数，从而大大减少 Key 和 Value 矩阵的参数量。
- 而 `GQA` 则是前段时间 Google 提出的 `MQA` 变种，全称 Group-Query Attention。MHA（Multi-head Attention）是标准的多头注意力机制，h个Query、Key 和 Value 矩阵。
  - GQA 将查询头分成N组，每个组共享一个Key 和 Value 矩阵

`GQA`以及`MQA`都可以实现**一定程度**的Key value的共享，从而可以使模型体积减小，`GQA`是`MQA`和`MHA`的折中方案。
- ![](https://pic4.zhimg.com/80/v2-35447d4d20c2f31cd70156dcdff30a9f_1440w.webp)

这两种技术的加速原理是
- （1）减少了数据的读取
- （2）减少了推理过程中的KV Cache。

注意:
- GQA和MQA需要在模型**训练**时开启，按照相应的模式生成模型。

#### 4.3 FLAT Attention

[FLAT Attention](https://arxiv.org/pdf/2107.06419.pdf)

FLAT-Attention 与 FlashAttention 采取不同的路线来解决同一问题。 提出的解决方案有所不同，但关键思想是相同的（tiling 和 scheudling）。下面主要讨论二者不同之处：

![](https://pic1.zhimg.com/80/v2-4aaef09f88889bee0ea87af715d2e674_1440w.webp)

**4.3.1 Tiling 策略比较**

FlashAttention 使用块平铺和权重固定。 FLAT-Attention 使用行平铺（行粒度）和输出固定。

![](https://pic4.zhimg.com/80/v2-9288c9716e66141781431e6d3eedf713_1440w.webp)

**4.3.2 Scheduling 策略(数据流)比较**

FlashAttention 的 Scheduling 过程
- ![](https://pic2.zhimg.com/80/v2-2dcdce1109983263b1492f2823841bfd_1440w.webp)

FLAT-Attention 的 Scheduling 过程
- ![](https://pic1.zhimg.com/80/v2-9c707e5a5b342707478ef54ceaeaf744_1440w.webp)


#### 【2023-11-20】META S2A

【2023-11-20】[System 2 Attention (is something you might need too)](https://arxiv.org/pdf/2311.11829.pdf)

System 2 Attention (S2A) 将 system 2思想引入注意力，改进推理效果

Meta AI 的**系统2注意力**(S2A)，包括提示LLM创建一个上下文，剥离掉可能扭曲推理的不相关信息。

LLM提供了一个上下文(x)，并负责生成高质量的输出(y)。S2A通过两步法修改了这个过程。
- 首先，S2A通过删除可能对输出产生负面影响的元素，将给定的上下文(x)重新表述为精炼的版本(x’)。用 `x' ~ S2A(x)` 表示。
- 然后，LLM使用修改后的上下文`(x')`生成最终响应`(y)`，而不是用`y ~ LLM(x')`表示的原始上下文。

![](https://pic3.zhimg.com/80/v2-3aaded91283921e4027a1e6dc96dbe46_1440w.webp)

Meta AI选择LLaMA-2-70B-chat作为他们的主要评估模型。


#### 【2023-11-6】Stateful API

OpenAI 11月6日 提到的Stateful API 背后用的技术类似于KV Cache，每次NTP下一字预测时，使用缓存，不再重新计算前面的所有字符注意力，空间换时间，提高推理性能


#### 【2023-4-11】GPTCache -- query语义缓存

GPTCache将query转换为向量进行相似性搜索，从缓存中检索相关查询，本质上还是语义缓存。

GPTCache是一个开源库，支持OpenAI ChatGPT 接口和 LangChain 接口
- 通过缓存语言模型的response来提高 GPT 应用的效率和速度。
- 支持用户根据自定义缓存规则，包括 embedding 函数、相似性计算方式、存储位置和存储逐出规则等。

三个词来概括：**高效**（省时间）、**节约成本**（省钱）、**定制化**（省劲儿）

**GPTCache 工作原理**
- [什么是 GPTCache](https://zilliz.com.cn/what-is-gptcache)

[GPTCache](https://github.com/zilliztech/GPTCache) 利用在线服务的**数据局部性**特点，存储常用数据，降低检索时间，减轻后端服务器负载。
- 与传统缓存系统不同，GPTCache 进行**语义缓存**，识别并存储相似或相关的查询以提高缓存命中率。

GPTCache 通过 embedding 算法将query转换为向量，并使用向量数据库进行相似性搜索，从缓存中检索相关查询。 

GPTCache 采用了模块化的设计，允许用户灵活自定义每个模块。
- ![](https://github.com/zilliztech/GPTCache/raw/main/docs/GPTCacheStructure.png)

虽然语义缓存可能会返回假正类（false positive）和负类（negative）结果，但 GPTCache 提供 3 种性能指标来帮助开发人员优化其缓存系统。

通过上述流程，GPTCache 能够从缓存中寻找并召回相似或相关查询，如下图所示。
- ![](https://zilliz.com.cn/images/opensourceGptCache/infra.svg)

GPTCache 模块化的架构设计方便用户定制个性化语义缓存。每个模块都提供多种选择，适合各种应用场景。
-   **大语言模型适配器（LLM Adapter）**: 适配器将大语言模型请求转换为缓存协议，并将缓存结果转换为 LLM 响应。适配器方便轻松集成所有大语言模型，并可灵活扩展。GPTCache 支持多种大语言模型，包括：
  -   OpenAI ChatGPT API
  -   langchain
  -   Minigpt4
  -   Llamacpp
  -   dolly
  -   后续将支持：Hugging Face Hub、Bard、Anthropic 等
-  **预处理器（Pre-Processor）**：预处理器管理、分析请求，并在将请求发送至 LLM 前调整请求格式，具体包括：移除输入种冗余的信息、压缩输入信息、切分长文本、执行其他相关任务等。
-   **向量生成器（Embedding Generator）**: Embedding 生成器将用户查询的问题转化为 embedding 向量，便于后续的向量相似性检索。GPTCache 支持多种模型，包括：
  -   OpenAI embedding API
  -   ONNX（GPTCache/paraphrase-albert-onnx 模型）
  -   Hugging Face embedding API
  -   Cohere embedding API
  -   fastText embedding API
  -   SentenceTransformers embedding API
  -   Timm 模型库中的图像模型
-   **缓存存储（Cache Store）**: GPTCache 将 LLM 响应存储在各种数据库管理系统中。GPTCache 支持丰富的缓存存储数据库，用户可根据性能、可扩展性需求和成本预算，灵活选择最适合的数据库。GPTCache 支持多个热门数据库，包括：
  -   SQLite
  -   PostgreSQL
  -   MySQL
  -   MariaDB
  -   SQL Server
  -   Oracle
-   **向量存储（Vector Store）**: 向量存储模块会根据输入请求的 embedding 查找 top-K 最相似的请求。简而言之，该模块用于评估请求之间的相似性。GPTCache 的界面十分友好，提供丰富的向量存储数据库。选择不同的向量数据库会影响相似性检索的效率和准确性。GPTCache 支持多个向量数据库，包括：
  -   [Milvus](https://milvus.io/)
  -   [Zilliz Cloud](https://zilliz.com.cn/cloud)
  -   Milvus Lite
  -   Hnswlib
  -   PGVector
  -   Chroma
  -   DocArray
  -   FAISS    
-   **逐出策略（Eviction Policy）** 管理：控制缓存存储和向量存储模块的操作。缓存满了之后，缓存替换机制会决定淘汰哪些数据，为新数据腾出空间。GPTCache 目前支持以下两种标准逐出策略：
  -   “最近最少使用”逐出策略（Least Recently Used，LRU）
  -   “先进先出”逐出策略（First In First Out，FIFO）        
-   **相似性评估器（Similarity Evaluator）**: GPTCache 中的相似性评估模块从 Cache Storage 和 Vector Store 中收集数据，并使用各种策略来确定输入请求与来自 Vector Store 的请求之间的相似性。该模块用于确定某一请求是否与缓存匹配。GPTCache 提供标准化接口，集成各种相似性计算方式。多样的的相似性计算方式能狗灵活满足不同的需求和应用场景。GPTCache 根据其他用例和需求提供灵活性。
-   **后处理器（Post-Processor）**：后处理器负责在返回响应前处理最终响应。如果没有命中缓存中存储的数据，大语言模型适配器会从 LLM 请求响应并将响应写入缓存存储中。


### 服务优化

服务相关优化主要包括：**Continuous Batching**、**Dynamic Batching** 和 **异步 Tokenize / Detokenize**。
- Continuous Batching 和 Dynamic Batching 主要围绕提高可并发的 batchsize 来提高`吞吐量`
- 异步 Tokenize / Detokenize 则通过多线程方式将 Tokenize / Detokenize 执行与模型推理过程时间交叠，实现降低时延目的。

| 问题分类 | 现象 | 解决方法 | 实现原理 | 特点 |
| --- | --- | --- | --- | --- |
| 问题一 | 同批次序列推理时，存在“气泡”，导致 GPU 资源利用率低 | Continuous Batching | 由 batch 粒度的调度细化为 step 级别的调度 | 在时间轴方向动态插入新序列 |
| 问题二 | 批次大小固定不变，无法随计算资源负载动态变化，导致 GPU 资源利用率低 | Dynamic Batching | 通过维护一个作业队列实现 | 在 batch 维度动态插入新序列 |
| 问题三 | Tokenize / Detokenize 过程在 CPU 上执行，期间 GPU 处于空闲状态 | 异步 Tokenize / Detokenize | 多线程异步 | 流水线 overlap 实现降低时延 |

大语言模型的输入和输出均是**可变长度**。对于给定问题，模型在运行前无法预测其输出长度。在实际服务场景下，每个用户的问题长度各不相同，问题对应的答案长度也不相同。传统方法在同批次序列推理过程中，存在“气泡”现象，即必须等同批次内的所有序列完成推理之后，才会执行下一批次序列，这就会引起 GPU 资源的浪费，导致 GPU 利用率偏低。
- ![](https://pic2.zhimg.com/v2-0bd73d7571ff162fa700255bf7cedf09_b.jpg)
- 图 6 Static Batching示意图

图中序列 3 率先结束，但由于其他序列尚未结束，因此需要等待直至所有序列计算完毕。理想情况下，同批次的所有序列的输入加输出的长度均相同，这时不存在“气泡”现象；极端情况下则会出现超过 50% 以上的资源浪费。

另一方面，传统方法推理时 batchsize 是固定不变的，无法随计算资源负载动态变化。比如某一段时间内，同批次下的序列长度都偏短，原则上可以增加 batchsize 以充分利用 GPU 计算资源。然而由于固定 batchsize，无法动态调整批次大小。

`Continuous Batching` 和 `Dynamic Batching` 最早来自论文 [Orca: A Distributed Serving System for Transformer-Based Generative Models]()。针对问题一，提出 Continuous Batching，原理为将传统 batch 粒度的任务调度细化为 step 级别的调度。首先，调度器会维护两个队列，分别为 Running 队列和 Waiting 队列，队列中的序列状态可以在 Running 和 Waiting 之间转换。在自回归迭代生成每个 token 后，调度器均会检查所有序列的状态。一旦序列结束，调度器就将该序列由 Running 队列移除并标记为已完成，同时从 Waiting 队列中按 FCFS (First Come First Service) 策略取出一个序列添加至 Running 队列。
- ![](https://pic2.zhimg.com/v2-5ed24401a143ae8dc76d724fc2e43b69_b.jpg)
- 图 7 Continuous Batching示意图

图中，序列 3 率先在 T5 时刻结束，这时调度器会检测到序列 3 已结束，将序列 3 从 Running 队列中移除，并从 Waiting 队列中按 FCFS 策略取出序列 5 添加至 Running 队列并启动该序列的推理。通过该方法，即可最大限度地消除“气泡”现象。

问题一可以理解为在时间轴方向动态插入新序列，问题二则是在 batch 维度动态插入新序列，以尽可能地充分利用显存空间。具体来讲，在自回归迭代生成每个 token 后，调度器通过当前剩余显存量，动态调整 Running 队列的长度，从而实现 Dynamic Batching。例如，当剩余显存量较多时，会尽可能增加 Running 队列长度；当待分配的 KV Cache 超过剩余显存时，调度器会将 Running 队列中低优先级的序列换出至 Waiting 队列，并将换出序列占用的显存释放。

如上两个 batching 相关的优化技术可有效提升推理吞吐量，目前已在 HuggingFace Text-Generation-Interface (TGI)、vLLM、OpenPPL-LLM 等多个框架中实现。


#### System Prompt Caching

【2024-3-18】[LLM推理：首token时延优化与System Prompt Caching](https://zhuanlan.zhihu.com/p/687685636?utm_psn=1753431836070633472)

大语言模型（Large Language Model，LLM）推理采用**流式输出**（streaming）的形式，LLM推理的首token时延就是用户感受到的LLM推理服务的响应时间，直接影响用户体验。

对于在线服务，为了提升用户体验，都希望首token时延要小，一般在一秒左右比较好。
- LLM推理的**首token时延**（time to first token, TTFT）与模型参数规模、Prompt长度、Batch Size、GPU资源等因素有关。

LLM推理过程中，生成首token是**计算密集型**任务，生成首token阶段也称为prefill phase或context phase，生成首token的时间与处理输入给大模型的Prompt的计算量有关，与Prompt长度直接相关。例如，在Prompt长度相对较长的情况下（Prompt计算时间显著超过模型参数IO时间），再考虑到FlashAttention2等技术优化，生成首token的时间与输入Prompt的长度近似成线性关系。
- ![](https://pic2.zhimg.com/80/v2-4965b0dec5ba11a56d21e3c6c23b2bc1_1440w.webp)

个人助理聊天机器人、RAG客服系统等，输入给大模型的Prompt一般包含`System Prompt`和`User Prompt`两部分

`System Prompt` 相对较长，且对LLM的每一次请求都可能带着相同的`System Prompt`作为输入（作为Prompt的一部分）。这样就导致，对于用户多次请求，LLM推理需要重复计算`System Prompt`，造成GPU资源浪费，特别是增加了不必要的首token时延。

如果能省去对于`System Prompt`的重复计算，那将会显著提升首token生成速度。`System Prompt Caching`方法就是为了避免重复计算System Prompt，从而提高首token生成速度。

`System Prompt Caching`，也称为 `Prefix Sharing`，其基本思想是对`System Prompt`部分进行一次计算，并缓存其对应的Key和Value值（例如，存放在GPU显存中），当LLM推理再次遇到相同的（甚至部分相同的）`System Prompt`时，直接利用已经缓存的System Prompt对应的Key和Value值，这样就避免了对于System Prompt的重复计算。

`System Prompt Caching`主要分两种形式。
- Prefix Sharing，适用于 “`Prompt = System Prompt + User Prompt`” 场景，其中System Prompt就是Prefix。
  - 例如，给大模型输入的翻译指令，具有相同的System Prompt (Shared Prefix)。
  - ![](https://pic3.zhimg.com/80/v2-4ef40f28aa31f8b13672896a2512cf96_1440w.webp)
  - ![](https://pic2.zhimg.com/80/v2-3e35c15be2c65fb1af26a496b082a9dd_1440w.webp)
- Prompt Cache，属于相对高级的用法，对整个输入Prompt对应的Key和Value值进行Caching操作，不局限于shared prefix。
  - 这种方式需要使用Prompt Cache模板，可以针对Prompt的不同部分分别执行KV Cache。
  - ![](https://pic2.zhimg.com/80/v2-448ad1cd179725aaf5c6509cfd4c9b69_1440w.webp)

多轮对话场景，第二种方式，即Prompt Cache，可支持`Session Prompt Cache`。
- 多轮对话session里，输入给LLM的Prompt，会携带多轮对话历史，涉及到很多重复计算。
- 通过 Session Prompt Cache 可以显著减少不必要的重复计算，节省GPU资源，提高对话响应速度和用户体验。
- ![](https://pic2.zhimg.com/80/v2-d5d62dd9c62f17b89418cef07e670c95_1440w.webp)

TRT-LLM 实现
- Nvidia 开源的`TensorRT-LLM`（TRT-LLM）推理引擎已经支持了`System Prompt Caching`（Prefix Sharing）功能。
- 实测，当System Prompt在Prompt中占比较大时（即System Prompt比User Prompt长），System Prompt Caching功能可以带来较大的性能提升，可以显著减少生成首token的时延。

不过，TensorRT-LLM里，System Prompt Caching与FP8 KV Cache、INT8 KV Cache并不兼容。期待TensorRT-LLM的下一个版本可以修复这些问题

LLM推理解决方案，推荐 Triton & TRT-LLM。其中，Triton支持RESTFul API流式输出可以通过增加一个HTTP2gRPC模块来实现（过渡方案），可以实现兼容OpenAI接口协议。Triton未来也会直接支持基于RESTFul API的流式输出。


### 五、动态批处理（Dynamic Batch, Continuous batch）

该类方法主要是针对多 Batch 的场景，通过对 Batch 的时序优化，以达到去除 padding、提高吞吐和设备利用率。传统的 Batch 处理方法是静态的，因为Batch size 的大小在推理完成之前保持不变。

如下图所示，使用静态 Batch 完成四个序列。 在第一次迭代（左）中，每个序列从prompt（黄色）生成一个token（蓝色）。 经过几次迭代（右）后，每个完成的序列都有不同的大小，因为每个序列在不同的迭代中发出其序列结束标记（红色）。 可见序列 3 在两次迭代后就已经结束，但仍然需要等待 Batch 中的最后一个序列完成生成（在本例中，序列 2 在六次迭代后）才能统一输出，这意味着 GPU 未被充分利用。

![](https://pic2.zhimg.com/80/v2-88d3d261993d2d8e282a615e9331b835_1440w.webp)

静态 Batch 的推理情况

Dynamic Batch 是如何优化这一过程？

#### 5.1 ORCA

[ORCA](https://www.usenix.org/system/files/osdi22-yu.pdf)

Orca 不是等到 Batch 中的所有序列完成生成，而是实现 _iteration_ 级调度，其中Batch size由每次迭代确定。 结果是，一旦 Batch 中的序列完成生成，就可以在其位置插入新序列，从而比静态 Batch 产生更高的 GPU 利用率。

![](https://pic1.zhimg.com/80/v2-58ae1d63829f910e0cfc7219c9f8c730_1440w.webp)

下图展示了使用 Dynamic Batch 完成七个序列的过程。 左侧显示单次迭代后的批次，右侧显示多次迭代后的 Batch 。 一旦序列发出序列结束标记，就在其位置插入一个新序列（即序列 S5、S6 和 S7）。 这样可以实现更高的 GPU 利用率，因为 GPU 不会等待所有序列完成才开始新的序列。

![](https://pic2.zhimg.com/80/v2-e6dace0f5c6f874039f626eafcf8fa9d_1440w.webp)

结果显示在延时不变的情况下，其相对于FasterTransformer 可获得 36.9 倍的吞吐提升。

![](https://pic1.zhimg.com/80/v2-7fb66789eae51576b8841388f59d2a0c_1440w.webp)

#### 5.2 FastServe

[FastServe](https://arxiv.org/pdf/2305.05920.pdf)

ORCA 使用first-come-first-served (FCFS) 处理推理作业, 计划任务持续运行直至完成。 由于 GPU 内存容量有限以及推理对延时敏感，无法通过任意数量的传入函数来增加处理，由此可能会导致队列阻塞。

FastServe 使用 preemptive scheduling，通过新颖的跳跃连接 Multi-Level Feedback Queue 程序来最小化延时。 基于 LLM 推理的长度无法确定，调度程序利用输入长度信息来分配适当的初始值每个到达作业要加入的队列。 较高优先级队列跳过加入的队列以减少降级。 设计高效的GPU内存管理机制主动下载和上传 GPU 内存和主机内存之间的中间状态，以进行 LLM 推理。

![](https://pic3.zhimg.com/80/v2-924abfec2b40e77cfc4420d0b8a16d72_1440w.webp)

实验表明，该方法比ORCA有明显的性能提升

![](https://pic1.zhimg.com/80/v2-e826eaa832d2c9b973ba86b6ceaa074c_1440w.webp)

#### 5.3 vLLM

[vLLM](https://vllm.ai/) 的核心是 PagedAttention，其灵感来自传统操作系统概念，例如分页和虚拟内存。 它们通过在固定大小的“页面”或块中分配内存，允许 KV 缓存变得不连续。 然后可以重写 attention 机制以对块对齐的输入进行操作，从而允许在非连续的内存范围上执行 attention 。

这意味着 cache 分配可以 just-in-time，而不是 ahead-of-time：当启动一个新的生成任务时，框架不需要分配大小为 Maximum\_context\_length 的连续 cache。 每次迭代，调度程序都可以决定特定生成任务是否需要更多空间，并动态分配，而不会降低 PagedAttention 的性能。 这并不能保证内存的完美利用（浪费现在限制在 4% 以下，仅在最后一个块中），但它明显改善了当今业界广泛使用的提前分配方案的浪费 。

总而言之，PagedAttention + vLLM 可节省大量内存，因为大多数序列不会消耗整个上下文窗口。 这些内存节省直接转化为更高的 Batch 大小，这意味着更高的吞吐量和更便宜的服务。

实验表明，该方法相比于静态 Batch 与其他动态 Batch 的方法吞吐性能提升明显。
- ![](https://pic1.zhimg.com/80/v2-4d15f8b5575c5ac67cede615a335d3b0_1440w.webp)

#### 5.4 Text Generation Inference

[Text Generation Inference](https://github.com/huggingface/text-generation-inference)

TGI 是 HuggingFace 开发的基于 Rust, Python 和 gRPC 的推理服务工具，其基本框架如下：
- ![](https://pic1.zhimg.com/80/v2-3ae33f707e939f4ff89cd4f1680960e0_1440w.webp)

关于 TGI 的用法，可参考笔者的文章，同时对比了和 vLLM 和 FasterTransformer 的性能。

[紫气东来：小记：主流推理框架在Llama 2 的上性能比较](https://zhuanlan.zhihu.com/p/646772063)

#### 5.5 LMDeploy

[LMDeploy](https://github.com/InternLM/lmdeploy)

LMDeploy 是由 MMRazor 和 MMDeploy 团队开发的用于压缩、部署 LLM 服务的工具包。 它具有以下核心特点：
-   TurboMind：基于FasterTransformer 的高效推理引擎。
-   交互推理：通过缓存多轮对话过程中的 k/v，记住对话历史，以避免对历史会话的重复处理。
-   多GPU模型部署和量化
-   Dynamic Batch

### 六、硬件升级

以上主要介绍了在算法和模型层面的优化方法，除此之外，升级硬件系统可以进一步提升整体性能，下面将介绍几种可用于(和潜在的)推理加速的硬件产品。

#### 6.1 NVIDIA H100 PCIe

[NVIDIA H100 PCIe](https://www.nvidia.cn/data-center/h100/)

NVIDIA H100 核心架构与 Ampere 相似，数学运算部分布置在144组CUDA上，最高可拥有18432个FP32(单精度)、9216个FP64(双精度)CUDA核心，辅以576个第四代Tensor核心。H100核心采用台积电的N4工艺制造，内建800亿个晶体管，核心面积仅有814m㎡。其与A100 主要参数对比如下：
- ![](https://pic2.zhimg.com/80/v2-bf41cd47353338d3d6e9345fb84fc275_1440w.webp)

在性能方面，H100 较 A100 也有明显提升，其部分数据如下所示。
- ![](https://pic1.zhimg.com/80/v2-4c0e24b9d35250c471288cffa77764b8_1440w.webp)

#### 6.2 AMD MI300

AMD MI300 处理器集成了24个Zen 4架构CPU核心，以及CDNA 3架构GPU核心，周围还有着8颗HBM3高速缓存，容量高达128GB，总计拥有1460亿个晶体管。与上一代 MI250相比，MI300进行AI运算的速度将提高至8倍，能效方面也将提升5倍。

目前未找到公开的在 LLM 方面的推理性能数据。

#### 6.3 Apple M2 Ultra

[Apple M2 Ultra](https://www.apple.com/newsroom/2023/06/apple-introduces-m2-ultra/)

M2 Ultra 采用第二代 5 纳米工艺制造，并使用 Apple 突破性的 UltraFusion 技术连接两个 M2 Max 芯片的芯片，使性能提高一倍。 M2 Ultra 由 1340 亿个晶体管组成，比 M1 Ultra 多了 200 亿个。 其统一内存架构支持突破性的192GB内存容量，比M1 Ultra多出50%，并具有800GB/s的内存带宽，是M2 Max的两倍。 M2 Ultra 配备更强大的 CPU（比 M1 Ultra 快 20%）、更大的 GPU（快 30%）以及神经引擎（快 40%）。

目前未找到公开的在 LLM 方面的推理性能数据。

#### 6.4 Graphcore IPU

Graphcore C600 IPU处理器PCIe卡是针对机器学习推理应用的高性能加速卡。每个IPU具有1472个处理核心，能够并行运行8832个独立程序线程。每个IPU都有900MB的片上SRAM存储。用户可以在单个机箱中直接连接多达8块卡，通过高带宽的IPU-Links进行桥接。在训练和推理自然语言处理 (NLP) 模型（如 BERT 和 GPT、图神经网络 (GNN)、目标检测、语音等）时表现出色的结果。

目前未找到公开的在 LLM 方面的推理性能数据。

#### 6.5 Biren BR100

BR100是由壁仞科技发布自主研发的首款通用GPU芯片，其16位浮点算力达到1000T以上、8位定点算力达到2000T以上，单芯片峰值算力达到PFlops（1PFlops等于1000万亿次浮点指令/秒）级别。其与 H100 的参数对比如下所示：

![](https://pic3.zhimg.com/80/v2-f5414cf8ea9456a43fe38f49c4c8735e_1440w.webp)

目前未找到公开的在 LLM 方面的推理性能数据。


### 推测解码


【2024-10-6】 [LLM推理加速新范式！推测解码（Speculative Decoding）最新综述](https://zhuanlan.zhihu.com/p/678404136)

**推测解码**（Speculative Decoding）综述：
- [Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculative Decoding](https://arxiv.org/abs/2401.07851)
- Repo: [SpeculativeDecodingPapers](https://github.com/hemingkx/SpeculativeDecodingPapers)

#### 推测解码介绍

推测解码定义：
- 推测解码是一种“**先推测后验证**” (Draft-then-Verify) 的解码算法：
- 每个解码步，该算法首先高效地“推测”target LLM未来多个解码步的结果，然后用target LLM同时进行验证，以加速推理。

所有符合在每个解码步“高效推测->并行验证“模式的推理算法，都可以称为是**推测解码**（或其变体）。

推测解码实现加速的关键要素，主要在于如下三点：
- 相比于生成单一token，LLM并行计算额外引入的latency很小，甚至可以忽略；
- “推测”的高效性&准确性：如何又快又准地“推测”LLM未来多个解码步的生成结果；
- “验证“策略的选择：如何在确保质量的同时，让尽可能多的“推测”token通过验证，提高解码并行性。

推测解码（Speculative Decoding）是 2023年新兴的**LLM推理加速**技术


#### 推测解码原理

解决方案：
- 通过增加每个解码步 LLM计算的**并行性**，减少总解码步数（即减少了LLM参数的反复读写），从而实现推理加速。

每个解码步，推测解码
- 首先 高效地“推测”target LLM（待加速的LLM）未来多个解码步可能生成的token
- 然后 再用target LLM同时验证这些token。通过验证的token作为当前解码步的解码结果。
- 如果“推测”足够准确，推测解码就可以在单个解码步并行生成多个token，从而实现LLM推理加速。
- 并且，使用target LLM的验证过程，在理论上保证解码结果和target LLM自回归解码结果的完全一致。

推测解码在实现对 target LLM 推理加速的同时，不损失LLM的解码质量。

这种优异的性质导致推测解码受到了学界和工业界的广泛关注，从2023年初至今涌现了许多优秀的研究工作和工程项目（如Assisted Generation[7]，Medusa[8]，Lookahead Decoding[9]等等）。

#### 推测解码方案

推测解码研究思路的演化
- ![](https://pic2.zhimg.com/80/v2-70411b91ca1b6bd669f920a5cb4e7faf_1440w.webp)

研究总结
- ![](https://picx.zhimg.com/80/v2-e7ab90e1d676573e9243650ffb4bdb4b_1440w.webp)

详见介绍
- [LLM推理加速新范式！推测解码（Speculative Decoding）最新综述](https://zhuanlan.zhihu.com/p/678404136)




# 结束
