---
layout: post
title:  大模型推理优化 LLM Inference
date:   2023-09-20 22:46:00
categories: 大模型
tags: gpt 量化 llm deepspeed
excerpt: 如何提升LLM推理效率？
mathjax: true
permalink: /llm_opt
---

* content
{:toc}


# LLM 推理优化

基于 Transformer 架构的大语言模型 (LLM) 在全球范围内引发了深度的技术关注，并取得了令人瞩目的成就。其强大的理解和生成能力，正在深刻改变对人工智能的认知和应用。

然而，大语言模型的<span style='color:blue'>推理应用成本过高</span>，高昂的成本大大阻碍了技术落地。

优化推理性能不仅可以减少硬件成本，还可以提高模型的实时响应速度。它使模型能够更快速地执行自然语言理解、翻译、文本生成等任务，从而改善用户体验，加速科学研究，推动各行业应用的发展。

参考
- 【2023-8-30】[LLM七种推理服务框架总结](https://zhuanlan.zhihu.com/p/653352979)
- 【2023-8-17】[LLM 的推理优化技术纵览](https://zhuanlan.zhihu.com/p/642412124)


## 训练 vs 推理

AI工程分两个阶段：训练 和 推理
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
- 首词元(token)时间（Time to First Token）：接收提示后多久才返回第一个词元？
- 生成**时延**（Generation Latency）：接收提示后多久才返回最终词元？
- **吞吐量**（Throughput）：能够同时通过pipeline传递多少个不同的生成？
- 硬件**利用率**（Hardware Utilization）：在多大程度上有效地利用计算、内存带宽和硬件的其他能力？

重点关注两个指标：`吞吐量`和`时延`：
- `吞吐量`：从系统角度来看，即系统在单位时间内能处理的 tokens 数量。计算方法为系统处理完成的 tokens 个数除以对应耗时，其中 tokens 个数一般指输入序列和输出序列长度之和。吞吐量越高，代表 LLM 服务系统的资源利用率越高，对应的系统成本越低。
- `时延`：从用户视角看，即用户平均收到每个 token 所需位时间。计算方法为用户从发出请求到收到完整响应所需的时间除以生成序列长度。一般来讲，当时延不大于 50 ms/token 时，用户使用体验会比较流畅。

`吞吐量`关注系统**成本**，高`吞吐量`代表系统单位时间处理的请求大，系统利用率高。`时延`关注用户使用体验，即返回结果要快。

这两个指标一般相互影响，因此需要**权衡**。
- 提高`吞吐量`的方法一般是提升 batchsize，即将用户的请求由串行改为并行。
- 但 batchsize 的增大会在一定程度上损害每个用户的`时延`，因为以前只计算一个请求，现在合并计算多个请求，每个用户等待的时间变长。

模型小型化关注：模型**平均推理时间**和**功耗**
- 平均推理时间: 用 `latency` 或 `throughput` 来衡量
- 功耗: 用参考生成token过程中所用到GPU的功耗来近似(因为TP/PP等方法就会引入多个GPU). 

这两个指标都与**模型参数量**紧密相关, 特别是LLMs的参数量巨大, 导致部署消耗GPU量大(而且甚至会引起旧GPU, 如: 2080ti等消费级卡直接下线离场)及GPU的IO时间长(memory write/read 的cycles是要远大于 operations cycles, 印象中是百倍)

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

大模型推理本质上串行，一个字一个字的去预测
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

GPT-2生成下一个词元的情况：
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


### MLC-LLM


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



# 结束