---
layout: post
title:  大模型推理框架 LLM Inference Tool
date:   2023-09-20 22:46:00
categories: 大模型
tags: gpt 量化 vllm deepspeed 推理 推测解码 sglang 多模态 投机采样 美杜莎 bert
excerpt: 如何提升LLM推理效率？
mathjax: true
permalink: /llm_infer
---

* content
{:toc}


# LLM 推理框架

基于 Transformer 架构的大语言模型 (LLM) 在全球范围内引发了深度的技术关注，并取得了令人瞩目的成就。其强大的理解和生成能力，正在深刻改变对人工智能的认知和应用。

然而，大语言模型的<span style='color:blue'>推理应用成本过高</span>，高昂的成本，大大阻碍了技术落地。

优化推理性能不仅可以减少硬件成本，还可以提高模型的实时响应速度。它使模型能够更快速地执行自然语言理解、翻译、文本生成等任务，从而改善用户体验，加速科学研究，推动各行业应用的发展。

参考
- 【2023-8-30】[LLM七种推理服务框架总结](https://zhuanlan.zhihu.com/p/653352979)
- 【2023-8-17】[LLM 的推理优化技术纵览](https://zhuanlan.zhihu.com/p/642412124)


## LLM 推理


### 原理

【2024-3-30】[图解大模型计算加速系列之：vLLM核心技术PagedAttention原理](https://mp.weixin.qq.com/s/oCGENfMwTNmfr1nGeCZz2g)

LLM 推理过程分两个阶段: `prefill` 和 `decode`, 通常用 KV cache 技术加速推理
- `Prefill`: **预填充**阶段, 把整段 prompt 喂给模型, 做forward计算。**计算密集型**
  - 如果采用 `KV cache` 技术，会把prompt过 Wk,Wv 后得到的 Xk,Xv 保存在 cache_k 和 cache_v中。对后面的token计算attention时，就不需要对前面的token重复计算,节省推理时间。
  - 例如假设prompt中含有3个token，prefill阶段结束后，这三个token相关的KV值都被装进了cache
- `Decode`: **生成response**。根据prompt的prefill结果，逐个token生成response。 **瓶颈：KV Cache**
  - 如果采用 KV cache, 则每走完一个decode过程，就把对应response token的KV值存入cache中，以便能加速计算。
  - 例如 t4与cache中t0~t3的KV值计算完attention后，就把自己的KV值也装进cache中。对t6也是同理。

| 阶段 | 资源需求特性 | 计算模式 | 显存占用模式 |
| --- | --- | --- | --- |
| Prefill | 计算密集型 | 高并行度，矩阵乘法为主 | 低，固定规模 |
| Decode | 内存密集型 | 顺序生成，访存为主 | 随上下文增长指数级上升 |

为什么不能一个阶段做完？

Prefill 与 Decode 两个阶段的**输入特性**和**计算方式**本质不同，拆成两个阶段可以精准优化每步计算路径
- Prefill 可用 `Flash Attention` 等并行技术提升性能
- Decode 可用`KV Cache`、`speculative decoding`等加速


【2026-1-6】[Speculative Decoding: 从Padding 的视角重新理解投机解码](https://zhuanlan.zhihu.com/p/1991904699117490479)

LLM inference 优化两个基本事实：
- 事实一：Decode 阶段是 memory-bandwidth bound
  - Prefill 阶段矩阵-矩阵乘（GEMM），计算量大，是 compute-bound；
  - 而 decode 阶段每次只生成一个token，做矩阵-向量乘（GEMV），瓶颈在于读取 KV Cache，是 memory-bandwidth bound。
- 事实二：Batch size 和 Context length 对资源的影响方向相反
  - Batch size 增大：算力需求增长得比带宽需求快 → 系统往 compute-bound 方向走
  - Context length 增大：带宽需求增长得比算力需求快 → 系统往 memory-bound 方向走

小 batch 的时候算力闲着，长 context 的时候带宽不够用.

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


### PD分离

传统集成式推理流水线中，LLM Prefill和Decode阶段往往被置于同一GPU上运行，导致资源需求不匹配，资源利用率不高。

例如，当用户请求的Prefill长度和Decode长度非常不匹配时，同一GPU需要同时处理高算力需求和高内存带宽需求的任务，难以发挥最佳性能。



#### 【2025-3-*】NVIDIA Dynamo

2025年3月，GTC大会上 NVIDIA 推出 开源分布式推理服务框架 Dynamo，解决大语言模型（LLM）推理过程中的资源不匹配和低效问题。

Dynamo 通过 **PD分离式**部署（Prefill-Decode Disaggregation）技术，将LLM推理拆分为两个阶段：**计算密集**型的预填充（Prefill）和**内存密集**型的解码（Decode），并分别部署到不同GPU上运行，从而实现资源的最优利用和推理效率的大幅提升。

这一创新技术基于 DistServe 和 Splitwise 等研究论文的思路，结合NVIDIA在GPU加速计算领域的深厚积累，形成了独特的分布式推理架构。

Dynamo 采用模块化的分布式架构，由多个协同工作的核心组件构成，各组件均可独立扩展。

![](https://picx.zhimg.com/v2-67bdba330ed64c8bca472864d2d3d625_r.jpg)

Dynamo 通过以下方式实现PD分离：
- 1、阶段拆分：将LLM推理拆分为两个独立阶段，Prefill负责处理用户输入（prompt），生成第一个输出token和KV Cache；Decode负责基于KV Cache依次生成后续token。
- 2、Worker分离：为两个阶段分别部署Worker节点，Prefill Worker和Decode Worker在不同GPU上运行，避免相互干扰。例如，在腾讯云的部署案例中，使用了3个H20节点（每个节点8个GPU），其中：
  - 2个节点专门部署Prefill Workers（每个节点部署8个Worker，tp=1，pp=8）
  - 1个节点专门部署Decode Workers（部署8个Worker，tp=8，pp=1）
  - 3、通信优化：通过NIXL库实现GPU间零拷贝数据传输，当Prefill阶段完成后，迅速将生成的KV Cache经由NIXL推送给Decode节点，减少数据传输延迟。
  - 4、智能调度：GPU Planner监控GPU容量指标（如算力利用率、内存带宽使用率、队列长度等），根据实时负载动态调整Worker数量与GPU分配。例如，在Hopper架构上运行Llama模型时，Dynamo 可将性能提升一倍以上；在GB200 NVL72集群上运行DeepSeek-R1 671B模型时，吞吐量可提升30倍。

PD分离技术使每个GPU专注于特定任务，避免了资源浪费。例如，Prefill阶段可使用计算性能更强但内存带宽相对较低的GPU，而Decode阶段则使用内存带宽更高的GPU（如配备HBM的H100或Blackwell GPU）。

Dynamo 是高吞吐量低延迟的推理框架，专为多节点分布式环境中服务生成式 AI 和推理模型而设计。

Dynamo 设计为**与推理引擎无关**（支持 TRT-LLM、vLLM、SGLang 或其他），并捕获 LLM 特定的功能，例如：
- 分离预填充和解码推理 – 最大化 GPU 吞吐量，并促进吞吐量和延迟之间的权衡。
- 动态GPU调度 – 根据波动需求优化性能。
- LLM感知请求路由 – 消除不必要的 KV 缓存重新计算。
- 加速数据传输 – 使用 NIXL 减少推理响应时间。
- KV缓存卸载 – 利用多个内存层次结构提高系统吞吐量。

Dynamo 核心优势：完全开源
- 采用Rust和Python混合编程模式（核心性能模块用Rust编写，上层逻辑用Python实现），为开发者提供了完全的透明度和灵活性。
- 通过模块化设计，用户可根据需要选择特定组件，确保与现有AI技术栈兼容，避免高昂的迁移成本。


#### 【2026-6-6】Mooncake

【2026-6-6】典型架构：Mooncake 以缓存为中心的分离架构，核心是“KV 池化”。
- 工作流程：用户的请求先由 Prefill 集群处理，生成的庞大“钥匙-锁 (KV) 缓存]”被存入一个叫 Mooncake Store 的分布式缓存池。Decode 集群再从这个池子里快速取用缓存，生成最终回答。
- 优势：通过共享缓存，避免了重复计算，能大幅提升系统整体的吞吐量。
- 挑战：这项技术对底层的高速网络（如 InfiniBand）依赖度极高，并且系统复杂度也相应增加。


### 新技术

#### 【2026-4-16】 Kimi Prefill-as-a-Service

【2026-4-19】【Kimi团队新作】Prefill-as-a-Service：跨数据中心KVCache，吞吐量提升54%
- [小红书解读](https://www.xiaohongshu.com/explore/69e389ad000000002301166d)

【2026-4-16】Moonshot AI（Kimi）& 清华大学 混合注意力模型的KVCache足够小，可以通过商用以太网跨数据中心传输，实现异构集群间的高效推理
- 🔗 论文：arXiv:2604.15039 [Prefill-as-a-Service: KVCache of Next-Generation Models Could Go Cross-Datacenter
](https://arxiv.org/abs/2604.15039)
- 📌 核心思想：混合注意力模型的KVCache足够小，可以通过商用以太网跨数据中心传输，实现异构集群间的高效推理

🔬 研究背景
-  PD（Prefill-Decode）分离是大规模LLM推理的标准范式
-  但KVCache传输将Prefill和Decode绑定在同一RDMA集群内
-  异构部署（不同芯片做Prefill/Decode）难以跨集群实现


核心瓶颈：KVCache 传输
- 传统 Dense Attention 模型的KVCache体积巨大
- Prefill/Decode 被迫绑定在同一RDMA集群
- 异构部署（如不同芯片）难以跨集群实现

💡 PrfaaS 核心设计
-  选择性卸载：仅将长上下文请求卸载到远程计算密集型集群，短请求保留本地
-  混合前缀缓存池：统一管理线性注意力状态和全注意力KVCache
-  带宽感知调度：双时间尺度算法，短期调路由阈值，长期调资源分配
-  吞吐量模型：解析建模三阶段流水线，网格搜索最优配置

📊 实验结果（1T混合模型，Kimi Linear架构）
-  对比同构PD基线：吞吐量提升 54%，P90 TTFT降低 64%
-  对比朴素异构方案：吞吐量提升 32%
-  PrfaaS集群出口带宽仅13 Gbps，占100G以太网链路的13%
-  混合模型KV吞吐量比Dense模型低13倍（MiMo-V2 vs MiniMax @32K）




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

### 指标总结

LLM 推理服务评估指标：
- `TTFT` 首词元(token)时间（Time to First Token）：接收提示后多久，才返回第一个词元？越低越好，决定用户感知到的「响应速度」。
- `TBT`（Time-Between-Tokens）：相邻两个 token 间隔。需要足够稳定，避免出现「卡一下、蹦一下」的感觉。
- 生成**时延**（Generation Latency）：接收提示后多久才返回最终词元？
- **吞吐量**（Throughput）：能够同时通过pipeline传递多少个不同的生成？
- 硬件**利用率**（Hardware Utilization）：在多大程度上有效地利用计算、内存带宽和硬件的其他能力？

### 指标分析

重点关注两个指标：`吞吐量`和`时延`：
- `吞吐量`：从系统角度来看，即系统在单位时间内能处理的 tokens 数量。计算方法为系统处理完成的 tokens 个数除以对应耗时，其中 tokens 个数一般指输入序列和输出序列长度之和。吞吐量越高，代表 LLM 服务系统的资源利用率越高，对应的系统成本越低。
- `时延`：从用户视角看，即用户平均收到每个 token 所需位时间。计算方法为用户从发出请求到收到完整响应所需的时间除以生成序列长度。一般来讲，当时延不大于 50 ms/token 时，用户使用体验会比较流畅。

`吞吐量`关注系统**成本**，高`吞吐量`代表系统单位时间处理的请求大，系统利用率高。

`时延`关注用户使用体验，即返回结果要快。

这两个指标相互影响，因此需要**权衡**。
- 提高`吞吐量`的方法一般是提升 batch_size，将用户请求由**串行**改为**并行**。
- 但 batch_size 的增大会在一定程度上损害每个用户的`时延`，因为以前只计算一个请求，现在合并计算多个请求，每个用户等待的时间变长。

模型小型化关注：模型**平均推理时间**和**功耗**
- 平均推理时间: 用 `latency` 或 `throughput` 来衡量
- 功耗: 用参考生成token过程中所用到GPU的功耗来近似(因为TP/PP等方法就会引入多个GPU). 

这两个指标都与**模型参数量**紧密相关, 特别是LLMs参数量巨大, 导致部署消耗GPU量大(而且甚至会引起旧GPU, 如: 
- 2080ti等消费级卡直接下线离场)及GPU的IO时间长(memory write/read 的cycles是要远大于 operations cycles, 印象中是百倍)

部署过程中如何使得模型变得更小更轻且保持智能尽可能不下降就成了一个重要的研究话题。

### 指标优化

`TTFT` 和 `TBT` 目标天生矛盾。
- 当大量请求同时涌入（request burst），系统资源有限，服务器必须做取舍。

SGLang 等主流框架采用 FCFS（先来先服务）策略：正在处理的请求继续跑，新来的请求乖乖排队
- 正在跑的请求：生成速度远超用户阅读速度（几十 tokens/秒 vs 用户 5 tokens/秒），白白浪费算力
- 排队等待的请求：TTFT 飙升到 10 秒以上，用户以为系统挂了

SGLang 在 burst 负载下，P99 TTFT 轻松突破 30 秒，而生成速度却远超用户阅读需求——两头都没做好。


核心洞察：
> LLM 的生成速度远远快于用户的阅读速度。

实测数据
- 用户平均阅读速度约 3-5 tokens/秒，而模型生成速度可以达到 30-100 tokens/秒，相差一个数量级。

服务端可以提前生成一批 token 存在 output buffer 里，用户慢慢消费，系统不用死等用户。只要 buffer 不空，用户体验就是流畅的。

这个 buffer 给系统「喘息空间」——可以暂停正在跑的请求，先处理新来的请求的 prefill（生成第一个 token），只要 buffer 里还有剩余 token，暂停的那个用户不会察觉任何异常。

这就是 preemptive scheduling（`抢占式调度`）的机会所在。

TokenFlow 整体架构如下图所示，核心由两部分组成：Buffer-Aware 调度器 + Proactive KV Cache 管理器。
- 详见 [EuroSys'26 TokenFlow：让 LLM 流式输出真正「流」起来
](https://zhuanlan.zhihu.com/p/2040043117089404821)

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
- 算法加速
  - `投机采样`（Speculative decoding）针对 LLM 推理串行解码特点，通过引入一个近似模型来执行串行解码，原始模型执行并行评估采样，通过近似模型和原始模型的互相配合，在保证精度一致性的同时降低了大模型串行解码的次数，进而降低了推理时延。
  - `美杜莎头`（Medusa head）则是对投机采样的进一步改进，摒弃了**近似模型**，原始模型结构上新增了若干解码头，每个解码头可并行预测多个后续 tokens，然后使用基于树状注意力机制并行处理，最后使用典型接收方案筛选出合理的后续 tokens。该方法同样降低了大模型串行解码的次数，最终实现约两倍的时延加速。

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


## 推理框架

大模型推理有多种方式
- HuggingFace Transformers —— 最基础
- TGI
- vLLM —— 最流行
- Triton + TensorRT-LLM

vLLM 生态优势短期内难以撼动。未来 1-2 年的格局可能: vLLM + SGLang 二分天下

NVIDIA 也意识到 TensorRT-LLM "使用门槛过高"问题，正在简化：
- 2024 推出 trt-llm serve 命令（类似 vLLM）
- 计划支持 HF 模型直接加载（不用预编译）
- 与 NIM（NVIDIA Inference Microservices）整合

未来如果使用门槛降下来，TensorRT-LLM 份额会回升。


### 发展趋势

| 时间 | 事件 |
| ---- | ---- |
| 2022.06 | TGI（HuggingFace）首发 |
| 2023.06 | vLLM（Berkeley）发布 |
| 2023.10 | TensorRT-LLM（NVIDIA）开源 |
| 2023.11 | lmdeploy（OpenMMLab）开源 |
| 2024.01 | SGLang（LMSYS）发布 |
| 2024.06 | SGLang v0.2 引入 RadixAttention |
| 2024.12 | vLLM 0.6 + SGLang 0.3 全面集成 EAGLE |
| 2025 | SGLang 增长曲线超过 vLLM（部分场景） |
| 2026 | TensorRT-LLM 简化部署，市场份额回升 |

2026 年的推理框架生态：

| 适用场景 | 推理框架 | 特点 |
| ---- | ---- | ---- |
| 通用推理 | vLLM | 主流默认，稳健、生态广、易用 |
| 结构化 / Agent | SGLang | 增长最快，结构化/Agent 场景碾压 —— RadixAttention + 编程模型 |
| 极致性能 | TensorRT-LLM | 生产追求极限，性能上限最高，但工程化成本高 |
| HF 生态 | TGI | 稳定但不在领先 |
| 国产 / 中文 | lmdeploy | openmmlab生态 |
| 端侧 / 本地 | llama.cpp / Ollama | - |

真实困境：
- 开始选 vLLM，半年后发现 Agent 应用 JSON 输出经常崩 → 该不该换 SGLang？
- 听说 TensorRT-LLM 性能最强 → 但工程化复杂程度让人望而生畏
- TGI 简单好用，但版本更新慢 → 错过了多少特性？
- 国产卡部署用 lmdeploy 还是 vLLM？
- 不同框架的 OpenAI API 接口是不是真的兼容？


### 选型指南


<!-- draw.io diagram -->
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;dark-mode&quot;:&quot;auto&quot;,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot;&gt;\n  &lt;diagram name=\&quot;AI意图识别商用方案\&quot; id=\&quot;osbHtP6Ki7KAK-vxM0vi\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;31968\&quot; dy=\&quot;22037\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-37\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; value=\&quot;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;165\&quot; width=\&quot;210\&quot; x=\&quot;-29950\&quot; y=\&quot;-20505\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;ueTJB6k9vFQzMmB7xgun-37\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=24;labelBackgroundColor=none;\&quot; value=\&quot;&amp;lt;span style=&amp;quot;color: rgb(0, 0, 0); font-family: Helvetica; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;推理框架选型&amp;lt;/span&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;170\&quot; x=\&quot;-30165\&quot; y=\&quot;-20610\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-1\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=18;\&quot; value=\&quot;核心需求是什么？\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;180\&quot; x=\&quot;-30470\&quot; y=\&quot;-20240\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-2\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;fontSize=17;align=left;textShadow=1;\&quot; value=\&quot;通用对话&amp;lt;div&amp;gt;QA 服务&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;100\&quot; x=\&quot;-30200\&quot; y=\&quot;-20490\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-3\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=19;fontStyle=1;textShadow=1;\&quot; value=\&quot;vLLM ⭐\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;140\&quot; x=\&quot;-29920\&quot; y=\&quot;-20485\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-4\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-1\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-2\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-5\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-2\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-3\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-6\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;fontSize=17;align=left;textShadow=1;\&quot; value=\&quot;Agent / 复杂工作流&amp;lt;div&amp;gt;严格 JSON&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;160\&quot; x=\&quot;-30200\&quot; y=\&quot;-20400\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-7\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=19;fontStyle=1;textShadow=1;\&quot; value=\&quot;SGLang ⭐\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;140\&quot; x=\&quot;-29920\&quot; y=\&quot;-20395\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-8\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-1\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-6\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-9\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-6\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-7\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-10\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;fontSize=17;align=left;textShadow=1;\&quot; value=\&quot;极致性能\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;90\&quot; x=\&quot;-30200\&quot; y=\&quot;-20270\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-11\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=19;fontStyle=1;textShadow=1;\&quot; value=\&quot;TensorRT-LLM ⭐\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;160\&quot; x=\&quot;-29920\&quot; y=\&quot;-20265\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-12\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-1\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-10\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-13\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-10\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-11\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-14\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;fontSize=17;align=left;textShadow=1;\&quot; value=\&quot;HuggingFace 生态深度绑定\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;210\&quot; x=\&quot;-30200\&quot; y=\&quot;-19985\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-15\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=19;fontStyle=1;textShadow=1;\&quot; value=\&quot;TGI\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;100\&quot; x=\&quot;-29920\&quot; y=\&quot;-19980\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-16\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-1\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-14\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-17\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-14\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-15\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-18\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;fontSize=17;align=left;textShadow=1;\&quot; value=\&quot;国产硬件&amp;lt;div&amp;gt;InternLM 模型&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;130\&quot; x=\&quot;-30200\&quot; y=\&quot;-20080\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-19\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=19;fontStyle=1;textShadow=1;\&quot; value=\&quot;lmdeploy\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;120\&quot; x=\&quot;-29920\&quot; y=\&quot;-20075\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-20\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-1\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-18\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-21\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-18\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-19\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-22\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;fontSize=17;align=left;textShadow=1;\&quot; value=\&quot;端侧&amp;lt;div&amp;gt;个人开发&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;50\&quot; width=\&quot;90\&quot; x=\&quot;-30200\&quot; y=\&quot;-20160\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-23\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=19;fontStyle=1;textShadow=1;\&quot; value=\&quot;Ollama&amp;lt;div&amp;gt;LM Studio&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;55\&quot; width=\&quot;160\&quot; x=\&quot;-29920\&quot; y=\&quot;-20162.5\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-24\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-1\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-22\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-25\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-22\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-23\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-26\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=16;labelBackgroundColor=none;fontColor=#3333FF;\&quot; value=\&quot;&amp;lt;span style=&amp;quot;font-family: Helvetica; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;聊天助手/文档生成/Code助手/多模态服务&amp;lt;/span&amp;gt;&amp;lt;div&amp;gt;&amp;lt;span style=&amp;quot;font-family: Helvetica; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;创业MVP/企业内网&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;330\&quot; x=\&quot;-30190\&quot; y=\&quot;-20540\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-27\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontColor=default;labelBackgroundColor=none;\&quot; value=\&quot;&amp;lt;span style=&amp;quot;font-family: Helvetica; font-size: 15px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;&amp;quot;&amp;gt;性能差 10% 都心疼&amp;lt;/span&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;160\&quot; x=\&quot;-30200\&quot; y=\&quot;-20225\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-28\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=16;labelBackgroundColor=none;fontColor=#3333FF;\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(51, 51, 255), rgb(168, 168, 255));&amp;quot;&amp;gt;客服/FAQ; Agent/工具调用&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;200\&quot; x=\&quot;-30200\&quot; y=\&quot;-20430\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-29\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=16;labelBackgroundColor=none;fontColor=#3333FF;\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(51, 51, 255), rgb(168, 168, 255));&amp;quot;&amp;gt;海量/高并发 To C应用(万级qps)&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;270\&quot; x=\&quot;-30200\&quot; y=\&quot;-20310\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-30\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=18;\&quot; value=\&quot;团队规模\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;90\&quot; x=\&quot;-29645\&quot; y=\&quot;-20330\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-31\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-30\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-3\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-30240\&quot; y=\&quot;-20145\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-30081\&quot; y=\&quot;-20370\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-32\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=16;labelBackgroundColor=none;fontColor=#3333FF;\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(51, 51, 255), rgb(168, 168, 255));&amp;quot;&amp;gt;10人以内&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;80\&quot; x=\&quot;-29715\&quot; y=\&quot;-20395\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-33\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-30\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-7\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-29530\&quot; y=\&quot;-20400\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-29720\&quot; y=\&quot;-20400\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-34\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=16;labelBackgroundColor=none;fontColor=#3333FF;\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(51, 51, 255), rgb(168, 168, 255));&amp;quot;&amp;gt;10-30人&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;80\&quot; x=\&quot;-29725\&quot; y=\&quot;-20330\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-35\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=16;labelBackgroundColor=none;fontColor=#3333FF;\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(51, 51, 255), rgb(168, 168, 255));&amp;quot;&amp;gt;30人以上&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent; color: light-dark(rgb(51, 51, 255), rgb(168, 168, 255));&amp;quot;&amp;gt;有SRE&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;90\&quot; x=\&quot;-29715\&quot; y=\&quot;-20290\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-36\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-30\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-11\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-29460\&quot; y=\&quot;-20350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-29700\&quot; y=\&quot;-20325\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-38\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=18;labelBackgroundColor=none;fontColor=#666666;fontStyle=1\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;稳健/生态广/易用&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: transparent;&amp;quot;&amp;gt;80%场景最佳选择&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;150\&quot; x=\&quot;-29840\&quot; y=\&quot;-20525\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-39\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=18;labelBackgroundColor=none;fontColor=#666666;fontStyle=1\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;RadixAttention+编程模型&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;220\&quot; x=\&quot;-29935\&quot; y=\&quot;-20430\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-40\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=18;labelBackgroundColor=none;fontColor=#666666;fontStyle=1\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;性能上限最高，但工程化成本高&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;270\&quot; x=\&quot;-29975\&quot; y=\&quot;-20300\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-41\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=18;labelBackgroundColor=none;fontColor=#666666;fontStyle=1\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;OpenMMLab生态，interlm&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;240\&quot; x=\&quot;-29930\&quot; y=\&quot;-20040\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-42\&quot; parent=\&quot;1\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;fontSize=18;fontColor=#ffffff;\&quot; value=\&quot;LLM Gateway\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;60\&quot; width=\&quot;130\&quot; x=\&quot;-29410\&quot; y=\&quot;-20405\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-43\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-42\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-3\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;-29460\&quot; y=\&quot;-20375\&quot; /&gt;\n              &lt;mxPoint x=\&quot;-29460\&quot; y=\&quot;-20465\&quot; /&gt;\n            &lt;/Array&gt;\n            &lt;mxPoint x=\&quot;-29580\&quot; y=\&quot;-20385\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-29740\&quot; y=\&quot;-20450\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-44\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=18;labelBackgroundColor=none;fontColor=#666666;fontStyle=1\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;通用任务&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;90\&quot; x=\&quot;-29550\&quot; y=\&quot;-20500\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-46\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=18;labelBackgroundColor=none;fontColor=#666666;fontStyle=1\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;Agent&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;60\&quot; x=\&quot;-29540\&quot; y=\&quot;-20410\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-47\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-42\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=1;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-11\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;-29460\&quot; y=\&quot;-20375\&quot; /&gt;\n              &lt;mxPoint x=\&quot;-29460\&quot; y=\&quot;-20240\&quot; /&gt;\n              &lt;mxPoint x=\&quot;-29760\&quot; y=\&quot;-20240\&quot; /&gt;\n            &lt;/Array&gt;\n            &lt;mxPoint x=\&quot;-29100\&quot; y=\&quot;-20165\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-29500\&quot; y=\&quot;-20330\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-48\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=18;labelBackgroundColor=none;fontColor=#666666;fontStyle=1\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;高流量&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;60\&quot; x=\&quot;-29540\&quot; y=\&quot;-20280\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-49\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-42\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-7\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-29080\&quot; y=\&quot;-20280\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-29470\&quot; y=\&quot;-20160\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-50\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;Fp1i8z_00c0WHr3QWxwt-42\&quot; style=\&quot;endArrow=block;html=1;strokeWidth=2;fontSize=15;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;\&quot; target=\&quot;Fp1i8z_00c0WHr3QWxwt-23\&quot; value=\&quot;\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;-29460\&quot; y=\&quot;-20375\&quot; /&gt;\n              &lt;mxPoint x=\&quot;-29460\&quot; y=\&quot;-20135\&quot; /&gt;\n            &lt;/Array&gt;\n            &lt;mxPoint x=\&quot;-29160\&quot; y=\&quot;-20370\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-29550\&quot; y=\&quot;-20380\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;Fp1i8z_00c0WHr3QWxwt-51\&quot; parent=\&quot;1\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontSize=18;labelBackgroundColor=none;fontColor=#666666;fontStyle=1\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;内部测试&amp;lt;/div&amp;gt;\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry height=\&quot;40\&quot; width=\&quot;80\&quot; x=\&quot;-29550\&quot; y=\&quot;-20180\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



【2026-5-21】选型

| 使用场景 | 推荐工具/方案 | 核心优势 |
| ---- | ---- | ---- |
| 新手尝鲜 | Ollama | 一行命令启动，傻瓜式操作 |
| 高并发API | vLLM | 吞吐量比原生Transformers高10-30倍 |
| 纯CPU / 低功耗 | llama.cpp | 极致优化，笔记本也能跑 |
| 企业生产 | vLLM+K8s | 稳定性强 |

- 【2026-1-8】[主流大模型推理部署框架：vLLM、SGLang、TensorRT-LLM、ollama、XInference](https://mp.weixin.qq.com/s/AymYCFgoet43ZY8W2b-5SQ)
- 【2026-6-13】[推理框架横评：vLLM / TGI / TensorRT-LLM / SGLang 全面对比](https://mp.weixin.qq.com/s/5KF13oH7CUvvhiuT6LbA3A)

总体对比

| 框架 | 定位 | 核心创新 | 优势场景 | 劣势场景 | 生态特点 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| vLLM (Berkeley) | 通用首选 | PagedAttention | 通用LLM服务、HF模型生态 | 极致结构化输出、特殊硬件深度优化 | 生态最广 |
| SGLang (LMSYS) | 结构化输出之王 + Agent友好 | RadixAttention（树状KV共享）+ 编程模型 | JSON输出、工具调用、Agent、少样本场景 | 极致单序列性能 | 增长最快 |
| TensorRT-LLM (NVIDIA) | 性能上限 | 极致CUDA内核 + 完整模型编译 | 超大流量、高单卡吞吐 | 快速迭代、新模型适配 | NVIDIA全家桶 |
| TGI (HuggingFace) | HF生态融合 | 与HF推理端点深度集成 | HF工具链用户、企业API服务 | 极致性能、特殊优化 | 深度集成HF |
| lmdeploy (OpenMMLab) | 国产轻量、中文友好 | W4A16量化、TurboMind引擎 | 中文应用、国产硬件、InternLM系列 | 海外模型生态、复杂分布式 | 依托InternLM/OpenMMLab |

易用性+生态

| 维度 | vLLM | SGLang | TensorRT-LLM | TGI | lmdeploy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 安装难度 | ⭐ 极易 | ⭐⭐ 容易 | ⭐⭐⭐⭐ 困难 | ⭐ 极易 | ⭐⭐ 容易 |
| 模型支持 | 极广 | 广 | 中（需编译） | 广 | 中（HF + 自家） |
| 新模型适配速度 | 快（1-2周） | 快 | 慢（1-2月） | 中 | 中 |
| 文档完善度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 社区活跃 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| OpenAI 兼容 API | ✅ | ✅ | ✅（需配套） | ✅ | ✅ |
| K8s 部署友好 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Docker 镜像可用 | ✅ | ✅ | ✅ | ✅ | ✅ |

推理技术对比

| 技术 | vLLM | SGLang | TensorRT-LLM | TGI | lmdeploy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| PagedAttention | ✅ 首创 | ✅ | ✅ | ✅ | ✅ |
| Continuous Batching | ✅ | ✅ | ✅ | ✅ | ✅ |
| Flash Attention v2/v3 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prefix Caching | ✅ | ✅ 极强 | ✅ | ✅ | ✅ |
| RadixAttention | ❌ | ✅ 独有 | ❌ | ❌ | ❌ |
| Chunked Prefill | ✅ | ✅ | ✅ | ✅ | ✅ |
| FP8 | ✅ | ✅ | ✅ 最强 | ✅ | ✅ |
| INT4 (AWQ/GPTQ) | ✅ | ✅ | ✅ | ✅ | ✅ |
| W4A16 自研量化 | ❌ | ❌ | ✅ | ❌ | ✅ |
| 投机解码 (EAGLE) | ✅ | ✅ | ✅ | ❌ | △ |
| Tensor Parallel | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pipeline Parallel | ✅ | △ | ✅ | ❌ | ✅ |
| Expert Parallel (MoE) | ✅ | ✅ | ✅ | △ | ✅ |
| Context Parallel | ✅ | △ | ✅ | ❌ | △ |
| Multi-LoRA Serving | ✅ | ✅ | ✅ | ❌ | △ |
| 结构化输出 (JSON) | △ outlines | ✅ 原生 | △ | △ | △ |
| Function Calling | ✅ | ✅ 原生 | △ | △ | △ |
| 流式输出 | ✅ | ✅ | ✅ | ✅ | ✅ |

符号说明：
- ✅ 原生支持/完善；
- △ 有限支持/需额外配置；
- ❌ 不支持/无原生支持

实际测评

环境
- 硬件：8 × H100 80GB SXM
- 模型：Llama-3-70B-Instruct
- 精度：FP8 (各框架都支持)
- 上下文：32K
- 并行：Tensor Parallel = 4
- 评测工具：vLLM 内置 benchmark + 自研负载注入

指标
1. 单序列吞吐（batch=1）—— 反映单用户体验
2. 高并发吞吐（batch=128）—— 反映服务端能力
3. 混合长度负载（短长比 7:3） —— 反映真实业务
4. TTFT 长尾（prompt 32K 测试）


| 框架 | TTFT 中位数 | TTFT p99 | TPOT 中位数 | TPOT p99 | 单序列吞吐 | 高并发总吞吐(batch=128) | 混合长度真实负载 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TensorRT-LLM | 140ms | 600ms | 17ms | 42ms | 78 | 6100 | 5100 |
| SGLang | 165ms | 720ms | 16ms | 38ms | 65 | 6200 | 5400 |
| vLLM | 180ms | 850ms | 18ms | 45ms | 64 | 5800 | 4900 |
| lmdeploy | 195ms | 900ms | 19ms | 48ms | 60 | 5300 | 4600 |
| TGI | 220ms | 1100ms | 22ms | 55ms | 52 | 4500 | 3800 |

说明：
> - TTFT：首token延迟，数值越低，响应越快
> - TPOT：单token解码延迟，数值越低，生成越流畅
> - 吞吐（tokens/s）：数值越高，处理能力越强


| 工具 | PagedAttention | 连续批处理 | 多GPU推理 | 分布式推理 | OpenAI兼容API | 内存效率 | 易用性 |
|---|---|---|---|---|---|---|---|
| vLLM | ✅ | ✅ | ✅ | ✅ | ✅ | 高 | 高 |
| HuggingFace Transformers+ | ❌ | ❌ | ✅ | ❌ | ❌ | 低 | 高 |
| NVIDIA TensorRT-LLM | ❌ | ✅ | ✅ | ✅ | ❌ | 中 | 低 |
| Text Generation Inference | ❌ | ✅ | ✅ | ✅ | ✅ | 中 | 中 |


### 总结

【2025-5-8】韩国 [25种LLM部署框架你知道多少？](https://zhuanlan.zhihu.com/p/1933217002698306629)
- 论文：《[A Survey on Inference Engines for Large Language Models: Perspectives on Optimization and Efficiency](https://arxiv.org/pdf/2505.01658)》  
LLM 的推理框架，总共有 25 个。

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


详见站内专题：[大模型推理框架：vLLM](#vllm)


### SGLang

vLLM 虽好，但难以自定义推理逻辑，比如控制 prompt 动态拼接、多轮上下文窗口滚动、token 前缀约束，操作麻烦。

vLLM 设计思想：“底层最优”，更适合请求独立、按 token 走流水线的场景。 

SGLang 是伯克利团队打造的另一款大模型推理引擎，致力于优化 LLM 的吞吐性能与响应时延，同时降低编程复杂度。

核心机制: RadixAttention，借助精细化的缓存策略与结构化输出增强，有效支撑高并发服务需求。

SGLang 核心突破: 集成了RadixAttention技术与结构化输出机制
- RadixAttention‌：通过基数树（Radix Tree）对KV缓存的公共前缀进行高效复用，结合LRU驱逐策略与引用计数机制，显著提升缓存利用率。不同于传统框架在推理结束后即丢弃缓存，SGLang持久化保留提示与生成内容的KV状态于基数树结构中，从而支持快速的前缀匹配、缓存复用、动态插入与智能驱逐。该设计极大增强了系统在多轮交互与序列规划场景下的性能，实测表明，在Llama-7B模型上执行多轮对话任务时，其吞吐量较vLLM提升达5倍。

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

### TensorRT-LLM

TensorRT-LLM 是 NVIDIA 基于 TensorRT 构建的高性能推理引擎，专为大语言模型优化，致力于全面释放 NVIDIA GPU 的算力优势。

核心技术包括：
- 预编译优化‌：借助TensorRT的端到端优化框架，对模型执行离线编译，生成高度精炼的TensorRT引擎文件。尽管该过程引入一定的冷启动开销，却能大幅增强推理效率与系统吞吐能力。
- 量化支持‌：兼容FP8、FP4与INT4等多种低精度量化策略，通过精度压缩有效降低显存消耗并加速推理流程。在FP8模式下，TensorRT-LLM可维持近似原生精度的输出质量，同时显存需求下降超40%。
- 内核级优化‌：对Transformer结构中的核心组件（如自注意力机制、前馈神经网络等）实施底层CUDA内核重构，实现计算密集型操作的极致并行与内存访问优化，从而在NVIDIA GPU平台达成卓越性能表现。
- 张量并行与流水线并行‌：支持跨多GPU节点的分布式推理，融合张量并行与流水线并行策略，灵活扩展模型参数规模，显著提升单位时间内的请求处理容量。

适用场景与优势局限

适用场景：TensorRT-LLM特别适合对延迟要求极高的企业级应用，如实时客服系统、金融高频交易和需要快速响应的API服务。

### Ollama

Ollama是由AI社区开发的轻量级本地推理平台，专注于简化大模型本地部署和运行，特别适合个人开发者和研究者。

Ollama 核心技术特点包括：
- 基于Go语言的封装‌：Ollama采用Go语言构建，通过模块化架构将模型权重、运行依赖与环境配置统一打包为容器化单元，用户无需配置底层组件，仅需执行单条命令即可启动模型服务。
- llama.cpp集成‌：Ollama内嵌llama.cpp——这一高效的大语言模型推理引擎，兼容1.5位、2位、3位、4位、5位、6位与8位整数量化方案，实现轻量级推理性能优化。
- 跨平台支持‌：原生适配macOS、Windows与Linux三大操作系统，对ARM架构设备高度优化，尤其在苹果M系列芯片上表现优异。
- 本地化部署‌：支持无网络依赖的完全离线运行，全面保障数据不外泄、隐私不泄露，适用于对安全性要求严苛的私有化场景。
- 低硬件门槛‌：不依赖高性能GPU，可在消费级笔记本、嵌入式终端及边缘计算节点上流畅运行，显著降低大模型落地的硬件成本。

适用场景与优势局限
- 适用场景：Ollama特别适合个人开发者、教育展示和本地隐私要求高的场景，如个人知识库、教育演示和原型验证等。


### XInference

XInference：分离式部署的分布式推理框架

XInference 是一个高性能的分布式推理框架，专注于简化AI模型的运行和集成，特别适合企业级大规模部署。

XInference的核心架构：
- API层‌：采用FastAPI搭建，兼容RESTful规范与OpenAI接口标准，无缝对接现有系统生态。
- Core Service层‌：依托自研Xoscar框架，高效抽象分布式调度与通信逻辑，原生支持多GPU并行及Kubernetes集群弹性伸缩。
- Actor层‌：由ModelActor实例构成，承担模型加载与推理执行职责，各实例部署于ActorPool内，实现独立调度与自治管理。
- 分离式部署‌：将Prefill与Decode阶段分别映射至不同GPU，借助DeepEP通信库实现KVCache低延迟传输，显著增强硬件资源协同效率。
- 算子优化‌：在Actor层集成FlashMLA与DeepGEMM算子，全面适配海光DCU与NVIDIA Hopper GPU架构，最大化算力吞吐能力。
- 连续批处理‌：融合vLLM连续批处理机制，动态聚合请求流，优化调度策略，持续提升GPU使用率与吞吐性能。

适用场景与优势局限
- 适用场景：XInference特别适合企业级大规模部署，如智能客服系统、知识库问答和需要分布式扩展的场景。

### LightLLM

LightLLM：轻量级高性能推理框架

LightLLM是一个基于Python的LLM推理和服务框架，以轻量级设计、易于扩展和高速性能而闻名。


LightLLM的核心技术包括：
- 三进程异步协作‌：由独立进程分别承担 tokenization、模型推理与 detokenization 任务，达成异步运行，有效缓解 I/O 瓶颈。
- 动态批处理‌：依据请求特征与系统负载实时优化批处理策略，在吞吐量与延迟之间实现精准平衡。
- TokenAttention 机制‌：采用以 token 为粒度的 KV 缓存管理方案，彻底消除内存冗余，兼容 int8 KV Cache，使最大 token 吞吐能力提升近 2 倍。
- 零填充 (nopad-Attention)‌：精准适配输入序列长度的显著差异，规避传统填充策略导致的计算资源冗余。
- FlashAttention 集成‌：大幅加速注意力运算效率，同步削减 GPU 显存消耗。
- 张量并行技术‌：协同多 GPU 实现张量级并行计算，显著加快超大规模模型的推理响应速度。

适用场景与优势局限
- 适用场景：LightLLM特别适合需要高吞吐量的场景，如大规模语言模型API服务、多模态模型在线推理和高并发聊天机器人后端等。


### 昇腾

国产硬件适配框架：昇腾与LMDeploy

针对昇腾等国产硬件的推理框架也日益成熟。昇腾AI处理器和LMDeploy是国产硬件适配的代表。

昇腾AI处理器框架

昇腾AI处理器是华为依托自研达芬奇架构打造的专用AI加速芯片，其推理体系核心包含以下三大组件：
- MindSpore Inference：华为自研的推理引擎，深度适配昇腾达芬奇架构，实现整图下沉至芯片的On-Device执行，融合关键算子（如矩阵乘法与激活函数），并依托静态图优化策略，显著增强推理效率。
- CBQ量化技术‌：由华为诺亚方舟实验室与中国科学技术大学协同研发的跨块重建后训练量化方案，仅需0.1%的原始训练数据，即可一键将大模型压缩至原体积的1/7，同时保持浮点精度达99%，真正达成“轻量不降智”的目标。
- 昇腾CANN软件栈‌：构建多层次开发接口体系，通过AscendCL与TBE两大编程接口，赋能各类AI应用在CANN平台上的高效部署与极速运行。

### LMDeploy

LMDeploy：视觉语言混合任务专家

LMDeploy是由上海人工智能实验室模型压缩和部署团队开发的部署工具箱，专注于大语言模型和视觉语言模型的部署。

核心技术：
- 国产GPU深度适配‌，深度优化昇腾等国产硬件架构
- 显存优化‌，采用动态量化与模型切分技术，显著压缩显存占用
- 多模态融合支持‌，协同处理视觉与语言跨模态数据流
- TurboMind引擎‌，实现高效4bit推理的CUDA kernel加速

适用场景：
- 国内企业、政府机构部署，视觉语言混合任务。

### MLC-LLM


## LLM 推理框架

参考
- 【2023-9-21】[大语言模型推理性能优化综述](https://zhuanlan.zhihu.com/p/656485997)
- 【2024-3-30】[图解大模型计算加速系列之：vLLM核心技术PagedAttention原理](https://mp.weixin.qq.com/s/oCGENfMwTNmfr1nGeCZz2g)

LLM 推理过程分两个阶段: `prefill` 和 `decode`, 通常用 KV cache 技术加速推理

PagedAttention的设计灵感来自操作系统的虚拟内存分页管理技术

【2026-5-27】[大模型推理部署实践](https://mp.weixin.qq.com/s/YcnMIl8YMRIWNqx2sfIfHQ)

线上推理真正绕不开的几件事：压测、PD 分离、长上下文、MoE、灰度、LoRA、KV Cache 量化和反馈闭环
- 压测怎么跑：别只看 tok/s，要看 TTFT、TPOT、ITL 和排队
- PD 分离：Prefill 和 Decode 为什么要拆，什么时候不值得拆
- 长上下文：128K/1M 下 KV Cache 怎么控住
- MoE 模型部署：总参数、激活参数、Expert 并行和负载均衡
- 灰度发布和 A/B 测试：流式输出怎么切流量，怎么回滚
- LoRA 热加载：一个底座挂多个 LoRA，多个业务共用 GPU
- KV Cache 量化：什么时候开 FP8 KV，什么时候别开
- 在线反馈闭环：把真实用户反馈变成下一轮模型更新

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



# 结束
