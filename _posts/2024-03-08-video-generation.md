---
layout: post
title:  "视频生成技术专题 - Video Generation"
date:   2024-03-08 08:01:00
categories: 大模型 计算机视觉
tags: 视频 扩散模型 sora
excerpt: 文生视频技术
mathjax: true
permalink: /video_gen
---

* content
{:toc}

# 视频生成

视频生成, Text2Video

## 文生视频总结

`Text-to-Video`: `Phenaki` 、 `Soundify`
- `Phenaki` 由谷歌打造，基于新的编解码器架构C-ViViT将视频压缩为离散嵌入，能够在时空两个维度上压缩视频，在时间上保持自回归的同时，还能自回归生成任意长度的视频
- `Soundify` 是 Runway 开发的一个系统，目的是将声音效果与视频进行匹配，即制作音效。具体包括分类、同步和混合三个模块，首先模型通过对声音进行分类，将效果与视频匹配，随后将效果与每一帧进行比较，插入对应的音效。

AIGC [视频生成工具汇总](https://aigc.cn/#term-635)
- [artflow](https://artflow.ai), 支持换人、背景、音色。 换脸，卡通，真人，图像，跟着内容自动变换表情
- [synthesia](https://www.synthesia.io/free-ai-video-demo#SalesPitchNew)
- [invideo](https://invideo.io/make/add-text-to-video-online/): Text to video maker, Convert Blog and Article to Videos

视频生成
- Deepfake
- VideoGPT
- GliaCloud
- ImageVideo

文生视频模型通常在非常短的视频片段上进行训练，需要使用计算量大且速度慢的**滑动窗口**方法来生成长视频。

因此，训得的模型难以部署和扩展，并且在保证上下文一致性和视频长度方面很受限。

文生视频的任务面临着多方面的独特挑战。主要有：
- 计算挑战： 确保帧间空间和时间一致性会产生长期依赖性，从而带来高计算成本，使得大多数研究人员无法负担训练此类模型的费用。
- 缺乏高质量的数据集： 用于文生视频的多模态数据集很少，而且通常数据集的标注很少，这使得学习复杂的运动语义很困难。
- 视频字幕的模糊性： “如何描述视频从而让模型的学习更容易”这一问题至今悬而未决。为了完整描述视频，仅一个简短的文本提示肯定是不够的。一系列的提示或一个随时间推移的故事才能用于生成视频。

- 【2024-1-19】[一文纵览文生图/文生视频技术发展路径与应用场景](https://mp.weixin.qq.com/s/pOLIf6JVQ_b8v3T6LcA7Fg)

## 文生视频技术发展

主流文生视频技术发展路径
- 1、早期发展（2016 年以前）
- 2、**奠基**任务：GAN/VAE/flow-based （2016-2019 年）
  - 早期研究主要使用基于 GAN 和 VAE 方法在给定文本描述的情况下自回归地生成视频帧 （如 Text2Filter 及 TGANs-C）。
  - 虽然这些工作为文生视频这一新计算机视觉任务奠定了基础，但应用范围有限，仅限于低分辨率、短距以及视频中目标的运动比较单一、孤立的情况。
  - GAN: 模型参数量小，较轻便，所以更加擅长对单个或多个对象类进行建模。
  - 但由于其训练过程的不稳定性，针对复杂数据集则极具挑战性，稳定性较差、生成图像缺乏多样性。
  - GAN 代表作：VGAN、TGAN、VideoGPT、MoCoGAN、DVD-GAN、DIGAN
- 3、**自回归**模型及**扩散模型**生成阶段 （2019-2023）
  - 与 GANs 相比，自回归模型具有明确的密度建模和稳定的训练优势，自回归模型可以通过帧与帧之间的联系，生成更为连贯且自然视频。
  - 但是自回 归模型受制于计算资源、训练所需的数据、时间，模型本身参数数量通常比扩散模型大，对于计算资源要求及数据集的要求往往高于其他模型。
  - 但因为 transformer 比 diffusion 更适合 scale up，且视频的时间序列结构很适合转化为预测下一帧的任务形态。
  - 自回归模型发展三个阶段：
    - 早期 **逐像素** 视觉合成：早期自回归模型，生成质量差、成本高，仅用于低分辨率图像视频，示例有 PixelCNN,PixelRNN,Image Transformer,Video Transformer,iGPT
    - VQ-VAE 出现，预训练广泛应用: 离散视觉标记化方法使得高效大规模训练用于图像视频合成，示例有 GODIVA,VideoGPT
    - 视频当做图像的时间序列，降低成本，但可能效果不佳；示例有 NUWA, CogVideo, Phenaki
- 4、未来发展趋势（2024-?）
- 5、视频生成模型 mapping


### 技术缘由

【2024-2-23】[Sora的前世今生：从文生图到文生视频](https://www.toutiao.com/article/7338619760152625704), 已有介绍大多数分析都是从**技术报告**入手，对于普通读者难度较高。本文从文本生成图像到文本生成视频的技术演进角度解读从AE、VAE、DDPM、LDM到DiT和Sora的技术发展路线，旨在提供一条清晰简明的技术进化路径。
- (1) `自编码器`（Autoencoder）：压缩大于生成
  - `自编码器`由`编码器`和`解码器`两个部分构成
  - `编码器`负责学习输入到编码的映射 ，将高维输入（例如图片）转化为低维编码 `Z = e(x)`
  - `解码器`则学习编码到输出的映射 ，将这些低维编码还原为高维输出（例如重构的图片）`x^ = d(z)`
  - 目标：压缩前和还原后的向量尽可能相似（比如让平均平方误差MSE尽可能小），让神经网络学会使用低维编码表征原始的高维向量
  - 生成：只要留下解码器，随便喂入一个低维编码，就得到一个高维向量（例如图片）
    - 缺点： 对于未见过的低维编码，解码器重构的图片质量通常不佳，生成奇怪的样本。因为低维向量没有约束，导致过拟合
    - 自编码器更多用于数据压缩。
- (2) `变分自编码器`（Variational Autoencoders）：迈向更鲁棒地生成
  - 自编码器不擅长图片生成, 因为过拟合
  - 解决思路：既然自编码器将图片编码为确定性的数值编码会导致过拟合，变分自编码器就将图片编码为一个具有**随机性的概率分布**，比如标准正态分布。 这样当模型训练好后，只要给解码器喂入采样自标准正态分布的低维向量，就能够生成较为“真实”的图片了。
  - 变分自编码器除了希望编码前解码后的样本尽可能相似（MSE尽可能小），还希望用于解码的数据服从标准正态分布，低维编码的分布和标准正态分布的KL散度尽可能小，损失函数加上这么一项约束。
  - 变分自编码器减轻了自编码器过拟合问题，确实能用来做图片生成，但是生成图片通常会比较**模糊**。
    - 变分自编码器的编码器和解码器都是一个神经网络，编码过程和解码过程一步就到位，一步到位可能带来的问题就是建模概率分布的能力有限/或者说能够对图片生成过程施加的约束是有限的/或者说“可控性”是比较低的。
- (3) `去噪扩散概率模型`（`DDPM`）：慢工出细活
  - 既然变分自编码器一步到位的编解码方式可能导致生成效果不太理想，DDPM就考虑拆成**多步**来做，将编码过程和解码过程分解为多步
  - 扩散模型由两个阶段构成
    - **前向扩散**过程，比如给定一张照片，不断（也就是多步）往图片上添加噪声，直到最后这样图片看上去什么都不是（就是个纯噪声）： `x = x1 -> x2 -> x3 -> ... -> x(t-1) -> xt = z`
    - **反向去噪**过程，给定噪声，不断执行去噪的这一操作，最终得到一张“真实好看”的照片: ： `x = x1 <- x2 <- x3 <- ... <- x(t-1) <- xt = z`
  - 从数据集中采样出一张图片，前向过程每步从高斯分布中采样出噪声叠加到时刻的图像上，当足够大时，最终会得到一个**各向同性**的高斯分布（**球形高斯分布**，各个方向方差都一样的多维高斯分布)。
  - DDPM 通过**多步迭代生成**得到图片, 缓解了`变分自编码器`生成图片模糊的问题，但是由于多步去噪过程需要对**同一尺寸**图片数据进行操作，导致了越大的图片需要计算资源越多（原来只要处理一次，现在有几步就要处理几次）。
- (4) `潜在扩散模型`（`LDM`）：借助VAE来降本增效 
  - 问题：DDPM 在原始空间（像素级图片）进行扩散训练和采样比较费资源
  - 解决：降维后在隐空间上进行，利用自编码降维，如将 512×512 的图片降成 64×64 图片, 执行ddpm流程得到64×64的图片,通过自编码器的解码器还原为 512×512 的图片
  - 如何根据文本来生成图片？ 既然要接收文本，就需要给模型安排上**文本编码器**（text encoder），把文本转化为模型能够理解的东西。`Stable Diffusion`采用了`CLIP`文本编码器，输入一段文本，输出77个token的embeddings向量，每个向量的维度为768（可以理解为一段话最多保留77个字（或词），每个字（或词）用768维的向量表示）。
  - 得到文本的表示后，在原来的U-net里叠加上文本信息, U-net的输入原由两部分组成(**加噪后的图片**+**时间步长（t）**), 扩展为三部分(增加**文本token embedding**)。Stable Diffusion 使用一种文本和图片之间的交叉注意力机制，计算图像和文本的相似度，然后根据这个相似度作为系数对文本进行加权
- (5) `Diffusion Transformers`（`DiT`）：当扩散模型遇到Transformer
  - LDM 扩散模型使用了 `U-net` 这一网络结构，但这个结构是最佳吗？
  - 去年火了一整年的**大语言模型**、**多模态大模型**绝大部分用的都是Transformer结构，相比于U-net，Transformer结构的Scaling能力（模型参数量越大，性能越强）更受大家认可。
  - 因此，`DiT`其实就是把`LDM`中的`U-net`替换成了`Transformer`，并在Vision Transformer模块的基础上做了略微的修改使得在图片生成过程能够接受一些额外的信息，比如时间步，标签。
  - Transformer如何处理图片数据？`Vision Transformer` (`ViT`)，主要思想就是将图片分割为固定大小的**图像块**（image patch/token），对每个图像块进行线性变换并添加位置信息，然后将得到的向量序列送入一个标准的Transformer编码器。
- (6) Sora：视频生成的新纪元
  - Sora就是改进的`DiT`。DiT本质上是 `VAE`编码器 + `ViT` + `DDPM` + `VAE`解码器；OpenAI的技术报告体现出来的创新点：
    - 改进VAE -> 时空编码器
    - 改进DiT -> 不限制分辨率和时长
  - 至于图像分块、Scaling transformers、视频re-captioning、视频编辑（SDEdit）这些其实都是已知的一些做法了。
  - 视频每一帧（frame）本质上就是一张图片。视频播放时，这些连续图片以一定速率（帧率，通常以每秒帧数FPS表示）快速播放，由于人眼的视觉暂留效应，这些连续静态图片在观众眼中形成了动态效果，从而产生了视频的流畅运动感。
  - 视频生成可看作是多帧图片的生成，因此最low的做法就是把视频生成看作独立的图片生成，使用DiT生成多帧图片然后串起来就是视频了。
  - 问题显然很大: 没有考虑视频不同帧图片之间的**关联**，可能会导致生成的多帧图像很不连贯，串起来看就不像是视频了。
- 改进VAE：融入时间关联
  - 为了使视频生成连贯，VAE编解码过程自然需要考虑视频不同帧的关系，原来对图片进行处理相当于考虑的是**图片空间**上的关系，现在换到视频, 就是多了**时间**上的关系，即经典的**时空联合建模**问题。
  - 时空联合建模方法：非常多，比如使用 3D CNN、时间空间单独处理再融合、设计精巧的注意力机制等等
  - Sora技术报告中的Video compression network，没有提及具体做法，但是可看出是在VAE编码器上考虑了时空建模，对于解码器的设计没有相关介绍
  - 其它做法： 
    - VideoLDM: 在解码器上插入额外的temporal layers来考虑视频帧之间的关系，而编码器是保持不变的。
    - 几篇视频生成的相关论文: Make-A-Video、Emu Video、VideoLDM、AnimateDiff、VideoPoet、Lumiere
- 改进DiT：适配任意分辨率和时长
  - 很多分享都在传Sora能适配**任意**分辨率和时长, 是参考了`NaViT`这篇文章的做法，其实并非如此
  - Vision Transformer (`ViT`)本身就能够处理任意分辨率（不同分辨率就是相当于不同长度的图片块序列，不就类似给大语言模型提供不同长度的输入一个意思）, NaViT只是提供了一种高效训练方法。
  - DiT 如何处理不同分辨率、时长的视频数据？ 假设 T×X×Y×C 的视频切成 T×(X/px)×(Y/py) 的图片块序列，由于T,X,Y 可变, 关键问题是改进DiT更好的识别不同图片块属于原始视频中哪个区域
  - 一种做法是从位置编码的角度入手，比如对于输入Transformer的图片块，我们可以在patch embedding上叠加上时间、空间上的位置信息。

### 扩散模型

扩散模型已成为 AI 视频生成领域的主流技术路径，由于扩散模型在图像生成方面的成功，其启发了基于扩散模型的视频生成的模型。

经典扩散模型

|模型名称|发布时间|发布组织|介绍|
|---|---|---|---|
|Video Diffusion Model|2022.4|Google|支持图像和视频数据的联合训练,减少小批量梯度的方差并加快优化,生主成长和更高分辨率的视频。|
|Make-A-Video|2022.9|Meta|利用联合文本-图像先验,绕过对配对文本一视频数据的需求,潜在地扩展到更多的视频数据。|
|Imagen Video|2022.1|Google|采用级联扩散视频模型,验证了在高清视频生成中的简洁性和有效性,文本生成图像设置中的冻结编码器文本调节和无分类器指导转移到视频生成仍然有效。|
|Tune-A-Video|2022.12|新加坡国立,腾讯|使用预训练T2l模型生成T2V的框架,引入了用于T2V生成的一次性视频页调谐,消除了大规模视频数据集训练的负担,提出了有效的注意力调整和结构反转,可以显著提高时间一致性。|
|Gen-1|2023.2|Runway|将潜在扩散模型扩展到视频生成,通过将时间层引入到预训练的图像模型中并对图像和视频进行联合训练,无需额外训练和预处理。|
|Dreamix|2023.2|Google|提出了第一个基于文本的真实视频外观和运动编辑的方法,通过一种新颖的混合微调模型,可以显著提高运动编辑的质量。通过在简单的图像预处理操作之上应用视频编辑器方法,为文本引导的图像动画提供新的框架品。|
|NUWA-XL|2023.3|MRSA|"扩散超过扩散"的架构,"从粗到细"生成长视频,支持并行推理,这大大加快了长视频的生成速度。|
|Text2Video-Zero|2023.3|UT Austin, U of Oregon|提出零样本的文本生成视频的方法,仅使用预先训练的文本到图像扩散模型,而无需任何进一步的微调或优化,通过在潜在代码中编码运动动力学,并使用新的跨顿注意力重新编程每个侦的自我注意力,强制执行时间一致的生成。|
|VideoLDM|2023.4|NVIDIA|利用预先训练的图像DM并将其转换为视频生成器通过插入学习以时间一致的方式对齐图像的时间层,提出了一种有效的方法用于训练基于LDM的高高分辨率、长期一致的视频生成模型。|
|PYoCo|2023.5|NVIDIA|提出一种视频扩散噪声,用于微调文本到视频的文本到图像扩散模型,通过用噪声先验微调预训练的eDi-l模型来构建大规模的文本到视频扩散模型,并实现最先进的结果。|



## D-ID

[D-ID](https://www.d-id.com/): Digital People Text-to-Video
- Create and interact with talking avatars at the touch of a button, to increase engagement and reduce costs.
- [Studio](https://studio.d-id.com/)

制作过程介绍：
- [由AI制作视频----ChatGPT+MidJourney+d-id](https://www.toutiao.com/video/7203362904022712832/?log_from=de42079a586b7_1681187887298)

### 复现故人

【2023-4-11】[上海小伙用AI技术“复活”已故奶奶：讲着方言 像生前一样“唠叨”](https://hb.ifeng.com/c/8OscmJLl1H5)
- 上海一位24岁的00后视觉设计师，他用AI工具生成了奶奶的虚拟数字人，并和她用视频对话。
- ![](https://x0.ifengimg.com/ucms/2023_15/6887B0A44072FDA2D5979B0D2D1AC87F3885762F_size9679_w568_h320.gif)

## 【META】Make-A-Video

【2022-10】Meta公布了一个能够生成高质量短视频的工具——[Make-A-Video](https://makeavideo.studio/)，利用这款工具生成的视频非常具有想象力。
- [Introducing Make-A-Video: An AI system that generates videos from text](https://ai.facebook.com/blog/generative-ai-text-to-video/)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/4bc8759f50f747ff99ac4cd92eb2816b~noop.image)

## 【谷歌】


### Imagen Video与Phenaki

【2022-10-8】[图像生成卷腻了，谷歌全面转向文字→视频生成](https://www.toutiao.com/article/7151774108186083843)，挑战分辨率和长度; 文本转图像上卷了大半年之后，Meta、谷歌等科技巨头又将目光投向了一个新的战场：文本转视频。

谷歌公司 CEO Sundar Pichai 亲自安利了这一领域的最新成果：两款文本转视频工具——`Imagen Video` 与 `Phenaki`。
- `Imagen Video`主打视频品质
- `Phenaki`主要挑战视频**长度**，可以说各有千秋。

- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/d85eca195ae541da80c8b7b93d247fa7~noop.image)

生成式建模在最近的文本到图像 AI 系统中取得了重大进展，比如 `DALL-E 2`、`Imagen`、`Parti`、`CogView` 和 `Latent Diffusion`。
- 扩散模型在密度估计、文本到语音、图像到图像、文本到图像和 3D 合成等多种生成式建模任务中取得了巨大成功。

谷歌要做的是从文本生成视频。
- 以往的视频生成工作集中于: 具有**自回归模型**的受限数据集、具有自回归先验的**潜变量模型**以及近来的**非自回归潜变量**方法。扩散模型也已经展示出了出色的中等分辨率视频生成能力。

谷歌推出了 [Imagen Video](https://imagen.research.google/video/)，[论文地址](https://imagen.research.google/video/paper.pdf),它是一个基于级联视频扩散模型的文本条件视频生成系统。
- 给出文本提示，Imagen Video 就可以通过一个由 frozen T5 文本编码器、基础视频生成模型、级联时空视频超分辨率模型组成的系统来生成高清视频。

### VideoPoet


【2023-12-22】VideoPoet, 谷歌推出的视频生成大模型 [VideoPoet](https://sites.research.google/videopoet/)，蒋路是谷歌项目负责人，类似 OpenAI 刚刚发布的 Sora。
- A large language model for zero-shot video generation
- [VideoPoet: A large language model for zero-shot video generation](https://storage.googleapis.com/videopoet/paper.pdf)
- [资讯](https://36kr.com/p/2571512466038658)

零镜头视频生成大模型 VideoPoet。
- 执行各种视频生成任务，包括文本到视频、图像到视频、视频风格化、视频修复和修复，以及视频转音频。该工具被感叹是一个突破性文生视频工具。

VideoPoet 视频生成模型采用了单 Transformer 架构，将任何自回归语言模型或大型语言模型转换为高质量的视频生成器，支持生成方形或纵向视频，以针对短格式内容定制生成视频，并支持视频输入生成音频。

组件：
- 预训练的 MAGVIT V2 视频分词器和 SoundStream 音频分词器将可变长度的图像、视频和音频剪辑转换为统一词汇表中的离散代码序列。这些代码与基于文本的语言模型兼容，有助于与文本等其他模式的集成。
- 自回归语言模型跨视频、图像、音频和文本模态学习，以自回归预测序列中的下一个视频或音频 Token。
- 大模型训练框架引入了多模态生成学习目标的混合，包括文本到视频、文本到图像、图像到视频、视频帧延续、视频修复和修复、视频风格化和视频到视频-声音的。此外，这些任务可以组合在一起以获得额外的零样本功能（例如文本到音频）。

VideoPoet 采用了名为 Tokenizer 的数据处理技术，将视频和音频片段编码为**离散标记序列**（discrete tokens），这些标记也可以被转换回原始表示。其中，视频和图像数据使用名为 MAGVIT V2 的技术，音频数据使用 SoundStream 的技术。

VideoPoet 通过多个 Tokenizer 训练一个自回归语言模型，以学习跨视频、图像、音频和文本模态。一旦模型根据某些上下文生成了标记，这些标记就可以通过分词器解码器转换回可查看的表示。

【2024-2-21】[谷歌视频大模型VideoPoet负责人蒋路加入TikTok](https://mp.weixin.qq.com/s/rts2bJPaGFWm4F0n_OcA6w)

谷歌高级科学家、卡内基梅隆大学（CMU）计算机学院兼职教授蒋路，已经加入TikTok。

## 【阿里】大模型

【2023-3-22】阿里达摩院已在AI模型社区“魔搭”ModelScope上线了“文本生成视频大模型”。
- 整体模型参数约17亿，目前只支持英文输入。扩散模型采用Unet3D结构，通过从纯高斯噪声视频中，迭代去噪的过程，实现视频生成的功能。
- 模型还不支持中文输入，而且生成的视频长度多在2-4秒，等待时间从20多秒到1分多钟不等，画面的真实度、清晰度以及长度等方面还有待提升。
- 扩散模型采用 Unet3D 结构，通过从纯高斯噪声视频中，迭代去噪的过程，实现视频生成的功能
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/d8270a324501430a92d7b341c88a6f93~tplv-obj:256:256.image?_iz=97245&from=post&x-expires=1687392000&x-signature=CWJsHaBungH1EZQ8TnuAFKHo2Dw%3D)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/4585b6cb44064c84bc92b49330b87af4~noop.image?_iz=58558&from=article.pc_detail&x-expires=1681786689&x-signature=MI%2FjQcOy6i1UfPS%2FJEHP3ue2Lqc%3D)
- [体验地址](https://modelscope.cn/studios/damo/text-to-video-synthesis/summary)


## 视频风格化

【2022-9-7】通过将预训练的语言图像模型（pretrained language-image models）调整为视频识别，以此将对比语言图像预训练方法（contrastive language-image pretraining）扩展到视频领域；
- 为了捕捉视频中帧沿时间维度的远程依赖性，提出了一个跨帧的注意力机制，明确了跨帧的信息交换。此外该模块非常轻量化，可以无缝插入预训练的语言图像模型。
- [项目地址](https://github.com/microsoft/videox)
- [论文地址](https://arxiv.org/abs/2208.02816)


## 【Runway】Gen-2

【2023-4-11】视频领域的Midjourney，[AI视频生成新秀Gen-2内测作品流出](https://www.toutiao.com/article/7220311597607109172), 博主 Nick St. Pierre
- 论文：[Structure and Content-Guided Video Synthesis with Diffusion Models](https://arxiv.org/abs/2302.03011)
- [Gen-2](https://research.runwayml.com/gen2)还处于婴儿期，后面一定会更好。

【2023-11-4】[Gen-2颠覆AI生成视频！一句话秒出4K高清大片，网友：彻底改变游戏规则](https://mp.weixin.qq.com/s/GnTncBzzSuydrXgRhbBaCg)

Gen-2，迎来了“iPhone时刻”般的史诗级更新 —— 依旧是简单一句话输入，不过这一次，视频效果一口气拉到了4K超逼真的高度

跟 PIKA这位AI生成视频顶流相比，Gen-2 目前无论是在画质的清晰度，视频的流畅度等方面，都是更胜一筹。

视频生成的AI工具
- 2023年2月，诞生 Gen-1
- 2023年3月20日，发布（论文3月11号）Gen-2，带来了八大功能：
  - 文生视频、文本+参考图像生视频、静态图片转视频、视频风格迁移、故事板（Storyboard）、Mask（比如把一只正在走路的小白狗变成斑点狗）、渲染和个性化（比如把甩头小哥秒变海龟人）。

提示：
> Gen-1已经可以开始玩了(125次机会用完之后就只能按月付费了），Gen-2还没有正式对公开放。

背后的公司Runway成立于2018年，为《瞬息全宇宙》特效提供过技术支持，也参与了Stable Diffusion的开发（妥妥的潜力股）。

一句话拍大片, 只凭一句提示词就能完成，不需要借鉴其它图片和视频。
- 提示词: “一个身材匀称or对称（symmetrical）的男人在酒吧接受采访”
- 生成结果：只见一个身着深色衬衣的男人正望着对方侃侃而谈，眼神和表情透露着一股认真和坦率，对面的人则时不时点头以示附和。
- 视频
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/ea2d0cf1dfb04ea89ddc8f08c102777a~noop.image?_iz=58558&from=article.pc_detail&x-expires=1681786689&x-signature=PbyMYIc86AaaHRXgBMd72K3NQ4I%3D)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/dced5a1a3de047ebbe5859932cfe25d3~noop.image?_iz=58558&from=article.pc_detail&x-expires=1681786689&x-signature=SeHvpIdxeoheyHWTNVZt5G%2FKBfI%3D)


## 【微软】 NUWA-XL

微软亚研院最新发布了一个可以根据文字生成超长视频的AI：NUWA-XL。

只用16句简单描述，它就能get一段长达11分钟的动画：
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/ae8148f3988748cb9311049f69fa80ec~noop.image?_iz=58558&from=article.pc_detail&x-expires=1681786689&x-signature=EItKdYur12hOgkGcYdSNyTtBL%2Fs%3D)

## Invideo

Invideo 将任何内容或想法转换为视频


## EasyPhoto 肖像动画

【2023-11-8】[EasyPhoto : 让你的AIGC肖像动起来](https://zhuanlan.zhihu.com/p/665725712?utm_psn=1705720579523686400)

[EasyPhoto](https://github.com/aigc-apps/sd-webui-EasyPhoto) 一个基于SDWebUI生态的**AIGC插件**，专门用于生成真/像/美的AI写真

EasyPhoto 支持用户上传少量自己的图片，快速训练个性化的人像**Lora模型**，并进行多种肖像生成。

最近基于AnimateDiff提出的运动先验模型，拓展了EasyPhoto的肖像生成能力，使之能够生成动态的肖像。
- ![](https://pic2.zhimg.com/80/v2-d01d77478dc225baa78dbd4fcc7c03f1_1440w.webp)


- 文到视频: 
  - ![](https://pic3.zhimg.com/v2-828e089d51a1421f380ea78256dbe3c2_b.webp)
- 图到视频: 用户上传首图或首尾图，以完成指定人像的生成, 支持基于真人的风格转换、切换
  - ![](https://pic3.zhimg.com/v2-801aaa76ad68acb5d6a44cad08f26bea_b.webp)
- 视频到视频: 模板换脸功能也可以非常自然地应用于视频
  - ![](https://pic2.zhimg.com/v2-5a36f2426f13ca8709f8187eb6f9eec5_b.webp)

## Stable Video Diffusion


【2023-11-22】[Stable Video Diffusion来了，代码权重已上线](https://www.toutiao.com/article/7304115172606706217)

AI 画图的著名公司 Stability AI，终于入局 AI 生成视频了。产品已经横跨图像、语言、音频、三维和代码等多种模态

本周二，基于 Stable Diffusion 的视频生成模型 Stable Video Diffusion 来了，AI 社区马上开始了热议。
- 论文地址：[stable-video-diffusion-scaling-latent-video-diffusion-models-to-large-datasetss](https://stability.ai/research/stable-video-diffusion-scaling-latent-video-diffusion-models-to-large-datasets)
- 项目地址：[generative-models](https://github.com/Stability-AI/generative-models)

现在，可以基于原有的**静止图像**来生成一段几秒钟的**视频**。

基于 Stability AI 原有的 Stable Diffusion 文生图模型，Stable Video Diffusion 成为了开源或已商业行列中为数不多的视频生成模型之一。
- ![](https://p26-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/9ceb891041ce46da929fd11bdc0b9fc7~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1701257165&x-signature=2O6dyCcY4wn9h0sq4iW86rmUcWA%3D)

Stable Video Diffusion 以两种图像到视频模型的形式发布，能够以每秒 3 到 30 帧之间的可定制帧速率生成 14 和 25 帧的视频。

在外部评估中，Stability AI 证实这些模型超越了用户偏好研究中领先的闭源模型（runway、pika Labs）


## pika

Pika Labs （[pika.art](https://pika.art/)） 是一款创新的视频创建工具，可以将文本和图像转换为引人入胜的视频
- An idea-to-video platform that brings your creativity to motion
- [elon musk video](https://cdn.pika.art/entry.mp4)

Pika Labs 推出了创新的文本和图像转视频平台，只需打字即可激发你的创造力。这个平台让你能够将旅程中的图像转换为 Discord 上引人入胜的视频！测试阶段是免费
- 【2023-8-13】[Pika Labs 新魔法：一键将图像转为视频](https://zhuanlan.zhihu.com/p/649709202)
- 【2023-11-29】[Pika Labs发布1.0版本AI视频生成器，满足多种风格视频需求](https://www.4anet.com/p/11v7bd7d2bc837e4)，Pika 1.0采用了全新的AI模式，能够以3D动画、动漫、卡通和电影等多种风格生成和编辑视频。

体验方式
- 点击[链接](https://discord.com/invite/pika) 加入 Pika
- 进入 Pika Labs Discord 服务器，请前往“#generate”频道
- 使用“/create”命令添加图像以及提示说明
- ![](https://pic4.zhimg.com/80/v2-e52a1cf2bcef17921b706bfed3b27077_1440w.webp)

与 Gen-2 不同的是，文本将提供对视频创建的更大控制，PikaLabs 可以更好地结合文本以与图像完美配合
- ![](https://pic3.zhimg.com/v2-ea0b2d162d0be38ded9a7f3a3c40b112_b.jpg)


## animate anyone

【2023-11-28】阿里发布animate anyone简直逆天，一张照片生成任意动作视频
- 论文：[Animate Anyone: Consistent and Controllable Image-to-Video Synthesis for Character Animation](https://arxiv.org/pdf/2311.17117.pdf)
- github: [AnimateAnyone](https://github.com/HumanAIGC/AnimateAnyone)
- 演示[视频](https://humanaigc.github.io/animate-anyone/)

实现方法
- ![](https://humanaigc.github.io/animate-anyone/static/images/f2_img.png)

<iframe width="560" height="315" src="https://www.youtube.com/embed/8PCn5hLKNu4?si=Lv_0-iwvvkjBycrB" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## MagicAnimate

字节跳动新开源基于SD 1.5的 MagicAnimate，只需要一张照片和一组动作，就能生成近似真人的舞蹈视频。

开源地址：
- [magicanimate](https://showlab.github.io/magicanimate/)
- github [magic-animate](https://github.com/magic-research/magic-animate)

以后在社交平台上看到的小姐姐舞蹈短视频很可能就是AI生成的。
- ![](https://showlab.github.io/magicanimate/assets/figure/Framework.png)
- [视频地址](https://showlab.github.io/magicanimate/assets/app/multi/multi_dancing.mp4)

```sh
# sd-vae-ft-mse
git lfs clone https://huggingface.co/stabilityai/sd-vae-ft-mse
# stable-diffusion-v1-5
git lfs clone https://huggingface.co/runwayml/stable-diffusion-v1-5
# MagicAnimate 模型
git lfs clone https://huggingface.co/zcxu-eric/MagicAnimate
```

## WALT

【2023-12-12】斯坦福 [李飞飞谷歌破局之作！用Transformer生成逼真视频，下一个Pika来了？](https://mp.weixin.qq.com/s/T4wGCB2aX-3eilUakKFJtw)
- 论文：[Photorealistic Video Generation with Diffusion Models](https://walt-video-diffusion.github.io/assets/W.A.L.T.pdf)
- [Photorealistic Video Generation with Diffusion Models](https://walt-video-diffusion.github.io)

支持
- Text-to-Video Examples [video](https://walt-video-diffusion.github.io/assets/t2v_webm_wm/desert_swan.webm)
- Image-to-Video Examples [video](https://walt-video-diffusion.github.io/assets/i2v_webm_wm/spaceship.webm)
- Consistent 3D Camera Motion

英伟达高级科学家Jim Fan转发评论道：
- 2022年是影像之年
- 2023是声波之年
- 而2024，是视频之年！

- 首先，研究人员使用因果编码器在共享潜在空间中压缩图像和视频。
- 其次，为了提高记忆和训练效率，研究人员使用基于窗口注意力的Transformer架构来进行潜在空间中的联合空间和时间生成建模。
  - 研究人员的模型可以根据自然语言提示生成逼真的、时间一致的运动：

两个关键决策，组成三模型级联

W.A.L.T的方法有两个关键决策。
- 首先，研究者使用**因果编码器**在统一的潜在空间内联合压缩图像和视频，从而实现跨模态的训练和生成。
- 其次，为了提高记忆和训练效率，研究者使用了为空间和时空联合生成建模量身定制的窗口注意力架构。
  - 通过这两个关键决策，团队在已建立的视频（UCF-101 和 Kinetics-600）和图像（ImageNet）生成基准测试上实现了SOTA，而无需使用无分类器指导。
- 最后，团队还训练了三个模型的级联，用于文本到视频的生成任务，包括一个基本的潜在视频扩散模型和两个视频超分辨率扩散模型，以每秒8帧的速度，生成512 x 896分辨率的视频。

W.A.L.T的关键是将图像和视频编码到一个共享的潜在空间中。
- ![](https://walt-video-diffusion.github.io/assets/images/system_fig.png)

Transformer主干通过具有两层窗口限制注意力的块来处理这些潜在空间——空间层捕捉图像和视频中的空间关系，而时空层模拟视频中的时间动态，并通过身份注意力掩码传递图像。


## 【2024-2-20】字节 Boximator

视频界“神笔马良” —— 字节[Boximator](https://boximator.github.io)模型

产品信息：
- [Boximator](https://boximator.github.io) 是一款由字节跳动开发的文生视频模型，可通过文本精准控制生成视频中人物或物体的动作。

产品功能：
- 用户只需输入一句描述具体动作的文本，Boximator便可生成对应动作的视频片段，目前很多文生视频大模型其实做不到这一点。

同时在Pika 1.0、Gen-2、Boximator上输入文本“一位英俊的男人用右手从口袋中掏出一支玫瑰，并注视着这只玫瑰”，三个大模型最终生成的视频中，只有Boximator做到了男士掏花和看花的动作，其他两个均没有

2024年2月20日，字节跳动相关人士表示，Boximator是视频生成领域控制对象运动的技术方法研究项目，目前还无法作为完善的产品落地，距离国外领先的视频生成模型在画面质量、保真率、视频时长等方面还有很大差距。

## 【2024-2-16】OpenAI Sora

当大家还沉迷如何用文生文，文生图时，OpenAI掏出来了一个视频生成模型Sora。
- Sora 根据**文本指令**或**静态图像**生成长达1分钟视频的扩散模型
- 视频中还包含精细复杂的场景、生动的角色表情以及复杂的镜头运动 —— 目前市面上视频模型做不到


### Sora 介绍

OpenAI全新发布文生视频模型[Sora](https://openai.com/sora)
- 经纬创投: [一石激起千层浪，揭秘Sora的技术报告](https://mp.weixin.qq.com/s/sTcXw9oWo7rV5_97I8VgXg)

从皮肤纹理到瞳孔睫毛，Sora的还原度达到了「没有AI味」

循环网络、生成对抗网络、自回归Transformer和扩散模型等方法只关注于**特定类型**的视觉数据、**较短**的视频或者**固定尺寸**的视频。

而 Sora 不同，它是一种通用的视觉数据模型，能够生成各种持续时间、宽高比和分辨率的视频和图片，甚至长达一分钟的高清视频。

竞品对比
- ![](https://img.36krcdn.com/hsossms/20240217/v2_8818819477f644a2a4869de19f0dac8d@5691163_img_000?x-oss-process=image/format,jpg/interlace,1)

特点: “60s超长长度”、“单视频多角度镜头”和“世界模型”
- **60s超长视频**: 
  - 其它AI视频还挣扎在4s连贯性的边缘，OpenAI直接60s
- **单视频多角度**镜头: 
  - 当前AI工作流都是**单镜头**单生成，一个视频里面有多角度的镜头，主体还能保证完美的一致性，这无法想象
  - OpenAI直接一句Prompt，在一分钟的镜头里，实现了多角度的镜头切换...而且...物体一致...
- **世界模型**: 
  - 世界模型最难的是收集、清洗数据。
  - Runway 世界模型，毫无动静。
  - 但是OpenAI的Sora，直接来了一波大的，已经能懂物理规律了。

OpenAI [Sora](https://openai.com/sora)

目前Sora只面向邀请的制作者和安全专家开放测试，还没有公测时间表。

而堪称「世界模型」的技术报告仍然没有公开具体的训练细节。
- 技术报告: [Video generation models as world simulators](https://openai.com/research/video-generation-models-as-world-simulators)（视频生成模型作为世界模拟器）

Sora训练数据源未知，“ClosedAI”原则，并没有透露相关信息。

### 观点

英伟达高级研究科学家Jim Fan认为：
> Sora是一款数据驱动的物理模拟引擎，通过一些去噪和梯度计算来学习复杂的渲染、「直觉」物理、长远规划推理和语义基础。它直接输入文本/图像并输出视频像素，通过大量视频、梯度下降，在神经参数中隐式地学习物理引擎，它不会在循环中显式调用虚拟引擎5，但虚拟引擎5生成的（文本、视频）对有可能会作为合成数据添加到训练集中。

LeCun表示：
>「仅根据文字提示生成逼真的视频，并不代表模型理解了物理世界。生成视频的过程与基于世界模型的因果预测完全不同」。

### Sora 原理

Sora是一种扩散模型，通过从一开始看似静态噪声的视频出发，经过多步的噪声去除过程，逐渐生成视频。Sora不仅能够一次性生成完整的视频，还能延长已生成的视频。通过让模型能够预见多帧内容，团队成功克服了确保视频中的主体即便暂时消失也能保持一致性的难题。
- [Creating video from text](https://openai.com/sora#research)
- 技术报告: [Video generation models as world simulators](https://openai.com/research/video-generation-models-as-world-simulators)（视频生成模型作为世界模拟器）， [中文版](https://36kr.com/p/2651890691244297)
- [拆解OpenAI技术报告：Sora是怎么生成视频的？](https://m.huxiu.com/article/2683137.html?type=text)
- 【2024-2-28】微软和理海大学解读Sora技术解读技术报告和逆向工程，首次全面回顾了 Sora 的背景、相关技术、新兴应用、当前局限和未来机遇。 
  - [Sora: A Review on Background, Technology, Limitations, and Opportunities of Large Vision Models](https://arxiv.org/pdf/2402.17177.pdf)
- 袁粒课题组-北大信工 [PKU-YuanGroup](https://github.com/PKU-YuanGroup)，推出开源复现 [Open-Sora-Plan](https://github.com/PKU-YuanGroup/Open-Sora-Plan)
- [Sora学习手册-飞书文档](https://zl49so8lbq.feishu.cn/wiki/PiW6wlVlqi3sdnkIRHXcUK8CnK7)
- 【2024-3-1】[微软37页论文逆向工程Sora，得到了哪些结论](https://mp.weixin.qq.com/s/5-pySWU40omjBowsV2WCKA)， 人工智能生成内容（AIGC）技术的最新进展实现了内容创建的民主化，使用户能够通过简单的文本指令生成所需的内容

视觉类的生成模型经历了多样化的发展路线：（图见[原文](https://mp.weixin.qq.com/s/5-pySWU40omjBowsV2WCKA)）
- 生成对抗网络（GAN）和变分自动编码器（VAE）的引入是重要转折点
- 流模型和扩散模型进一步增强了图像生成的细节和质量。
  - BERT 和 GPT 成功将 Transformer 架构应用于 NLP 后，研究人员尝试迁移到 CV 领域，比如 Transformer 架构与视觉组件相结合，使其能够应用于下游 CV 任务，包括 Vision Transformer (`ViT`) 和 Swin Transformer ，进一步发展了这一概念。在 Transformer 取得成功的同时，`扩散模型`也在图像和视频生成领域取得了长足进步。扩散模型为利用 `U-Nets` 将噪声转换成图像提供了一个数学上合理的框架，U-Nets 通过学习在每一步预测和减轻噪声来促进这一过程。
- 2021 年以来，能够解释人类指令的生成语言和视觉模型，即所谓的**多模态模型**，成为了人工智能领域的热门议题。
  - CLIP 是一种开创性的视觉语言模型，它将 Transformer 架构与视觉元素相结合，便于在大量文本和图像数据集上进行训练。通过从一开始就整合视觉和语言知识，CLIP 可以在多模态生成框架内充当图像编码器。
  - Stable Diffusion 是一种多用途文本到图像人工智能模型，以其适应性和易用性而著称。它采用 Transformer 架构和潜在扩散技术来解码文本输入并生成各种风格的图像，进一步说明了多模态人工智能的进步。
- 2022 年 11 月ChatGPT发布后，2023 年出现了大量**文本到图像**的商业化产品，如 Stable Diffusion、Midjourney、DALL-E 3。这些工具能让用户通过简单的文字提示生成高分辨率和高质量的新图像，展示了人工智能在创意图像生成方面的潜力。
- 由于视频的时间复杂性，从文本到图像到文本到视频的过渡具有挑战性。尽管工业界和学术界做出了许多努力，但大多数现有的视频生成工具，如 Pika 和 Gen-2 ，都仅限于生成几秒钟的短视频片段。
- Sora 是一项重大突破，类似于 ChatGPT 在 NLP 领域的影响。Sora 是第一个能够根据人类指令生成长达一分钟视频的模型，同时保持较高的视觉质量和引人注目的视觉连贯性，从第一帧到最后一帧都具有渐进感和视觉连贯性。
  - Sora 在准确解读和执行复杂的人类指令方面表现突出，生成包含多个角色的详细场景
  - 具有**细微运动**和**交互描绘**的扩展视频序列，克服了早期视频生成模型所特有的短片段和简单视觉渲染的限制
- Sora 作为世界模拟器的潜力，它可以提供对所描绘场景的物理和背景动态的细微洞察。

Sora 核心本质：一个具有灵活采样维度的扩散 Transformer。由三部分组成：
- （1）时空压缩器首先将原始视频映射到潜在空间。
- (2) 然后，ViT 处理 token 化的潜在表示，并输出去噪潜在表示。
- (3) 类似 CLIP 的调节机制接收 LLM 增强的用户指令和潜在的视觉提示，引导扩散模型生成风格化或主题化的视频。

经过许多去噪步骤后，生成视频的潜在表示被获取，然后通过相应的解码器映射回像素空间。

#### Sora 技术

Sora背后的技术

OpenAI 技术报告，一些关于Sora的剖析：
- Sora建立在DiT模型上（Scalable Diffusion Models with Transformers, ICCV 2023）
- Sora有用于生成模型的视觉patches（ViT patches用于视频输入）
- “视频压缩网络”（可能是VAE的视觉编码器和解码器）
- Scaling transformers（Sora已证明diffusion transformers可以有效扩展）
- 用于训练的1920x1080p视频（无裁剪）
- 重新标注（OpenAI DALL·E 3）和文本扩展（OpenAI GPT）


从OpenAI Sora技术报告和Saining Xie的推特可以看出，Sora基于Diffusion Transformer模型。它大量借鉴了DiT、ViT和扩散模型，没有太多花哨的东西。

在Sora之前，不清楚是否可以实现长篇幅一致性。通常，这类模型只能生成几秒钟的256*256视频。“我们从大型语言模型中获得灵感，这些模型通过在互联网规模的数据上训练获得了通用能力。”Sora已经展示了通过可能在互联网规模数据上进行端到端训练，可以实现这种长篇幅一致性。

Sora 建立在扩散Transformer（DiT）模型之上（发表于ICCV 2023）, 可能的架构
- 一个带有Transformer骨架的扩散模型：`DiT` = [`VAE`编码器 + `ViT` + `DDPM` + `VAE`解码器]。

Sora与DiT没有太大区别，但Sora通过扩大其模型和训练规模，证明了其长期时空一致性。

在变长持续时间、分辨率和宽高比的视频和图像上，联合训练文本条件扩散模型

对持续时间、分辨率和宽高比各不相同的视频和图片进行文本条件扩散模型的联合训练，采用Transformer架构处理视频和图片的时空块隐编码，最新模型 Sora 能生成一分钟高质量视频

沿着LLM方向，继续扩展模型规模，物理世界通用模拟器可以构建出世界模型

>- We explore large-scale training of generative models on video data. Specifically, we train **text-conditional** diffusion models jointly on **videos** and **images** of variable **durations**, **resolutions** and **aspect ratios**. We leverage a transformer architecture that operates on spacetime patches of video and image latent codes. Our largest model, Sora, is capable of generating a minute of high fidelity video. Our results suggest that scaling video generation models is a promising path towards building general purpose simulators of the physical world.
>- Sora builds on past research in `DALL·E` and `GPT` models. It uses the recaptioning technique from `DALL·E 3`, which involves generating highly descriptive captions for the visual training data. As a result, the model is able to follow the user’s text instructions in the generated video more faithfully.

Sora模型逐渐拥有了一项新能力，叫做**三维一致性**。
- Sora能够生成动态视角的视频。同时随着视角的移动和旋转，人物及场景元素在三维空间中仍然保持一致的运动状态。
- AI理解三维物理世界跟人类方式不一样，它采用了一种拓扑结构上的理解。
- 视频的视角发生变化，那么相应的纹理映射也要改变。Sora 真实感非常强，纹理映射在拓扑结构上就得非常准确。
- 三维一致性能力使Sora能够模拟来自现实世界中人物、动物和环境的某些方面。

OpenAI为了训练出Sora，将各类视觉数据转化为**统一表示**。
- `块`（patches）, 类似于大语言模型中的token，块将**图像**或**视频帧**分割成的一系列小块区域。这些块是模型处理和理解原始数据的基本单元。
- 对于视频生成模型而言，`块`不仅包含了局部的**空间**信息，还包含了**时间**维度上的连续变化信息。模型可以通过学习patches之间的关系来捕捉运动、颜色变化等复杂视觉特征，并基于此重建出新的视频序列。

这样的处理方式有助于模型理解和生成视频中的连贯动作和场景变化，从而实现高质量的视频内容生成。

OpenAI 在块的基础上，将其压缩到**低维度潜在空间**，再将其分解为“`时空块`”（spacetime patches）。
- 潜在空间 是一个能够在复杂性降低和细节保留之间达到近乎最优的平衡点，极大地提升了视觉保真度
- `时空块`从视频帧序列中提取出, 具有固定大小和形状的**空间-时间区域**。相较于`块`，`时空块`强调了**连续性**，模型通过`时空块`来观察视频内容随时间和空间的变化规律。
- ![](https://images.openai.com/blob/1d2955dd-9d05-4f33-b346-be531d2a7737/figure-patches.png?trim=0,0,0,0&width=3200)

为了制造这些`时空块`，OpenAI训练了一个网络，降低视觉数据的维度，叫做`视频压缩网络`。这个网络接受原始视频作为输入，并输出一个在时间和空间上都进行了压缩的潜在表示。Sora在这个压缩后的潜在空间中进行训练和生成视频。同时，OpenAI也训练了一个相应的解码器模型，用于将生成的潜在向量映射回像素空间。

“块”非常接近token，作用和token差不多。
- 对于给定的压缩输入视频，OpenAI 直接提取一系列块作为Transformer token使用
- 然后这些时空块会被进一步编码并传递给Transformer网络进行全局自注意力学习。
- 最后利用Transformer的强大能力来处理并生成具有不同属性的视频内容。

这一方案同样适用于图像，因为图像可以看作是仅有一帧的视频。

基于块的表示方法使得Sora能够对不同分辨率、时长和宽高比的视频和图像进行训练。推理阶段，可在一个适当大小的网格中排列随机初始化的块来控制生成视频的尺寸。

数据处理

当前图像和视频生成技术常常将视频统一调整到一个标准尺寸，比如 4秒钟、分辨率256x256的视频。

而 Sora 直接在视频原始尺寸上进行训练，优点：
- 视频生成更加灵活：[img](https://img.36krcdn.com/hsossms/20240217/v2_4de2e6fefee3443a9d73e8023804489a@5691163_img_000?x-oss-process=image/format,jpg/interlace,1)
  - Sora能够制作各种尺寸的视频，从宽屏的1920x1080到竖屏的1080x1920，应有尽有。
  - Sora 可为各种设备制作适配屏幕比例的内容
- 更好的画质 [img](https://img.36krcdn.com/hsossms/20240217/v2_3b24211241fc4e8789479dd6b2766df7@5691163_img_000?x-oss-process=image/format,jpg/interlace,1)
  - 直接在视频原始比例上训练（而不是裁剪成正方形），能够显著提升视频的画面表现和构图效果
- 更强的语言理解
  - 用视频说明进行训练，不仅能提高文本的准确性，还能提升视频的整体质量。
- 提示语多样化（文本→图像/视频）
  - 接受图像或视频等其他形式的输入。
  - Sora 能执行一系列图像和视频编辑任务，比如 制作无缝循环视频、给静态图片添加动态、在时间线上扩展视频的长度等等。

Sora 支持其他类型的数据输入
- 比如：图像或视频，以达到图片生成视频、视频生成视频的效果。这一特性使得Sora能够执行广泛的图像和视频编辑任务——例如制作完美循环播放的视频、为静态图像添加动画效果、向前或向后延展视频时间轴等。

能力 —— [技术报告中文版](https://36kr.com/p/2651890691244297)
- **视频时间线扩展**
  - Sora不仅能生成视频，还能将视频沿时间线向前或向后扩展；将视频向两个方向延伸，创造出一个无缝的循环视频
- **图像生成**
  - Sora也拥有生成图像能力，分辨率最高可达2048x2048像素
- **视频风格、环境变换**
  - 将 SDEdit 技术应用于Sora，使其能够不需要任何先验样本，即可改变视频的风格和环境
- **视频无缝衔接**
  - 用Sora在两个不同视频间创建平滑的过渡效果，即使这两个视频的主题和场景完全不同。
- **模拟能力**涌现
  - 随着模型规模扩大，Sora 不需要专门针对3D空间、物体等设置特定规则，就模拟出人类、动物以及自然环境的某些特征。
  - **3D空间真实感**：视角动态变化的视频
  - **场景/物体一致性**：长视频中，保持场景和物体随时间的连续性，即便在物体被遮挡或离开画面时，也能保持其存在感
- **场景交互**能力
  - Sora能模拟出影响世界状态的简单行为，Sora的生成符合物理世界的规则
- **数字世界**模拟
  - Sora不仅能模拟现实世界，还能够模拟数字世界，比如视频游戏


数据仍然还是王道

数据层面上，OpenAI也给出了两点很有参考价值的方法
- 不对视频/图片进行裁剪等预处理，使用native size
- 数据质量很重要，比如（文本、视频）这样的成对数据，原始的文本可能并不能很好的描述视频，可以通过re-captioning的方式来优化文本描述，这一点在DALL·E 3的报告中也已经强调了，这里只是进一步从图片re-captioning扩展到视频re-captioning。

DALL·E 3 如何做re-captioning
- 基于图像这个条件（条件生成），用 CLIP 编码图像，把图像embedding放进去，生成文本描述
- 图像打标模型怎么训练？CoCa 方法，同时考虑对比损失和LM损失

模型推理策略

官方展示Sora的应用有很多，比如文生视频、图生视频、视频反推、视频编辑、视频融合等。
1. 文生视频：喂入DiT的就是文本embedding+全噪声patch
2. 视频编辑：类似SDEdit的做法，在视频上加点噪声（不要搞成全是噪声），然后拿去逐步去噪
3. 图生视频、视频反推、视频融合：喂入DiT的就是文本embedding（可选）+特定帧用给定图片的embedding+其他帧用全噪声patch

Sora 除了文生视频，也支持文生图，这里其实透露出了一种**统一**的味道。未来发展肯定会出现更加强大的多模态统一
- 万物皆可“分词”，选择合适的编码器 + Transformer结构或其他 + 合适的解码器，就可能实现各种不同模态之前的互相转换、互相生成！


<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2024-02-26T07:56:07.121Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\&quot; etag=\&quot;psDx4a6Jlj-EDRtXR6oX\&quot; version=\&quot;23.1.5\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;VC8KsEmwTz_4FKU3JA4y\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;2069\&quot; dy=\&quot;789\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-29\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#FFCCE6;fontColor=#333333;strokeColor=#666666;dashed=1;dashPattern=1 1;opacity=50;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;8.489999999999998\&quot; y=\&quot;970\&quot; width=\&quot;240\&quot; height=\&quot;140\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2rrU_kqTqN86A4O8P-Nc-53\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;dashed=1;dashPattern=1 1;opacity=50;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-370\&quot; y=\&quot;720\&quot; width=\&quot;670\&quot; height=\&quot;210\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-7\&quot; value=\&quot;文生图/视频技术演进\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=20;strokeWidth=2;fontFamily=Verdana;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;14.909999999999993\&quot; y=\&quot;420\&quot; width=\&quot;210\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;UnDAMuxRGoDYzSfqeH0n-51\&quot; value=\&quot;2024-2-26&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;text;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;strokeWidth=2;html=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-280.23\&quot; y=\&quot;1010\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2rrU_kqTqN86A4O8P-Nc-3\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-1\&quot; target=\&quot;D7jkmO4b4NPNle1_V9Gg-2\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;280.92999999999984\&quot; y=\&quot;750\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-5\&quot; value=\&quot;改进过拟合问题\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;2rrU_kqTqN86A4O8P-Nc-3\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0773\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2rrU_kqTqN86A4O8P-Nc-8\&quot; value=\&quot;缺点：低维向量没有约束，导致生成图片奇奇怪怪&amp;lt;br&amp;gt;原因：图片编码为确定性数值编码导致过拟合\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#FF0000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-162.81999999999996\&quot; y=\&quot;515\&quot; width=\&quot;310\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2rrU_kqTqN86A4O8P-Nc-11\&quot; value=\&quot;压缩＞生成\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#009900;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-299.9999999999999\&quot; y=\&quot;450\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;2rrU_kqTqN86A4O8P-Nc-54\&quot; value=\&quot;自编码器=编码器+低维编码+解码器\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#000000;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-162.81999999999996\&quot; y=\&quot;485\&quot; width=\&quot;240\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-1\&quot; value=\&quot;AE自编码器（AutoEncoder）\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-280.23\&quot; y=\&quot;480\&quot; width=\&quot;104.83\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-2\&quot; value=\&quot;VAE 变分自编码器&amp;lt;br&amp;gt;（Variational AutoEncoder）\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-324\&quot; y=\&quot;610\&quot; width=\&quot;192.82\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-3\&quot; value=\&quot;DDPM 去噪扩散概率模型&amp;lt;br&amp;gt;（Diffusion Model）\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-312.82\&quot; y=\&quot;732\&quot; width=\&quot;170\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-4\&quot; value=\&quot;解决：图片编码为随机性概率分布（如正态分布）\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#000000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-124.99999999999997\&quot; y=\&quot;610\&quot; width=\&quot;310\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-6\&quot; value=\&quot;缺点：生成的图片模糊&amp;lt;br&amp;gt;原因：编码、解码过程一步到位，概率分布建模能力受限，难以施加约束，可控性差\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#FF0000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-124.99999999999997\&quot; y=\&quot;630\&quot; width=\&quot;500\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-7\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;D7jkmO4b4NPNle1_V9Gg-3\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-228\&quot; y=\&quot;660\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;620\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-8\&quot; value=\&quot;改进图片模糊问题\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;D7jkmO4b4NPNle1_V9Gg-7\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0773\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-9\&quot; value=\&quot;生成效果更佳鲁棒\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#009900;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-349.9999999999999\&quot; y=\&quot;580\&quot; width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-10\&quot; value=\&quot;慢工出细活\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#009900;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-329.9999999999999\&quot; y=\&quot;707\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-11\&quot; value=\&quot;解决：编码、解码过程拆分为多步&amp;lt;br&amp;gt;扩散模型 = 前向扩散(加噪声) + 反向去噪\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#000000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-131.17999999999998\&quot; y=\&quot;720\&quot; width=\&quot;270\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-12\&quot; value=\&quot;缺点：计算资源开销大&amp;lt;br&amp;gt;原因：多步去噪过程针对同一尺寸图片\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#FF0000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-131.17999999999998\&quot; y=\&quot;749.5\&quot; width=\&quot;240\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-22\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#009900;strokeWidth=2;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-13\&quot; target=\&quot;D7jkmO4b4NPNle1_V9Gg-19\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-23\&quot; value=\&quot;U-Net改成Transformer&amp;lt;br&amp;gt;ViT模型\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;D7jkmO4b4NPNle1_V9Gg-22\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.159\&quot; y=\&quot;1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint y=\&quot;1\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-13\&quot; value=\&quot;LDM 隐空间扩散模型&amp;lt;br&amp;gt;（Latent Diffusion Model）\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-324\&quot; y=\&quot;865.5\&quot; width=\&quot;192.82\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-14\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-3\&quot; target=\&quot;D7jkmO4b4NPNle1_V9Gg-13\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;670\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;742\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-15\&quot; value=\&quot;改进计算资源问题\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;D7jkmO4b4NPNle1_V9Gg-14\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0773\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-16\&quot; value=\&quot;解决：降维到隐空间后，再进行扩散训练，再通过自编码器还原&amp;lt;br&amp;gt;文本生成图片：SD使用CLIP文本编码器&amp;lt;br&amp;gt;U-Net增加文本tokens embedding\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#000000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-350\&quot; y=\&quot;915\&quot; width=\&quot;390\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-17\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#009900;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-2\&quot; target=\&quot;D7jkmO4b4NPNle1_V9Gg-13\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;792\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;876\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;-360\&quot; y=\&quot;635\&quot; /&gt;\n              &lt;mxPoint x=\&quot;-360\&quot; y=\&quot;891\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-18\&quot; value=\&quot;借鉴\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;D7jkmO4b4NPNle1_V9Gg-17\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0773\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-19\&quot; value=\&quot;DiT 扩散Transformer模型&amp;lt;br&amp;gt;（Diffusion Transformer）\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;fontStyle=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;32.09000000000002\&quot; y=\&quot;865\&quot; width=\&quot;192.82\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-20\&quot; value=\&quot;\&quot; style=\&quot;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-3\&quot; target=\&quot;D7jkmO4b4NPNle1_V9Gg-19\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;792\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;876\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-24\&quot; value=\&quot;DiT = VAE编码器 + DDPM + VAE解码器\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#000000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;49.99999999999997\&quot; y=\&quot;820\&quot; width=\&quot;270\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-25\&quot; value=\&quot;Sora 模型\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;fontStyle=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;69.54\&quot; y=\&quot;1000\&quot; width=\&quot;117.91\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-26\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#808080;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;D7jkmO4b4NPNle1_V9Gg-19\&quot; target=\&quot;D7jkmO4b4NPNle1_V9Gg-25\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;792\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;-218\&quot; y=\&quot;876\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-27\&quot; value=\&quot;扩展到视频生成\&quot; style=\&quot;edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=none;\&quot; vertex=\&quot;1\&quot; connectable=\&quot;0\&quot; parent=\&quot;D7jkmO4b4NPNle1_V9Gg-26\&quot;&gt;\n          &lt;mxGeometry x=\&quot;-0.0773\&quot; y=\&quot;-1\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;11\&quot; as=\&quot;offset\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-28\&quot; value=\&quot;改进点：&amp;lt;br&amp;gt;- 改进VAE：时空编码器&amp;lt;br&amp;gt;- 改进DiT：不限制分辨率、时长\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#000000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;19.99999999999997\&quot; y=\&quot;1035\&quot; width=\&quot;210\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;D7jkmO4b4NPNle1_V9Gg-30\&quot; value=\&quot;视频生成=多帧图像生成\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=13;strokeWidth=2;fontFamily=Verdana;fontColor=#000000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;199.99999999999997\&quot; y=\&quot;1010\&quot; width=\&quot;160\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

#### 不足

Sora对涌现物理的理解脆弱，并不完美，仍会产生严重、不符合常识的幻觉，还不能很好掌握物体间的相互作用。

Sora作为一个模拟器存在着不少局限性。
- 模拟基本物理交互（如玻璃破碎）时的准确性不足
  - 无法准确模拟许多基本交互的物理过程，以及其他类型的交互，比如吃食物。物体状态的变化并不总是能够得到正确的模拟，这说明很多现实世界的物理规则是没有办法通过现有的训练来推断的。
- 长视频中出现的逻辑不连贯或物体会无缘无故地出现。
  - 比如，随着时间推移，有的人物、动物或物品会消失、变形或者生出分身；
  - 或者出现一些违背物理常识的闹鬼画面，像穿过篮筐的篮球、悬浮移动的椅子。如果将这些镜头放到影视剧里或者作为精心制作的长视频的素材，需要做很多修补工作。

#### Case

Prompt: 

```py
A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage. She wears a black leather jacket, a long red dress, and black boots, and carries a black purse. She wears sunglasses and red lipstick. She walks confidently and casually. The street is damp and reflective, creating a mirror effect of the colorful lights. Many pedestrians walk about.
# 一位时尚女性走在充满温暖霓虹灯和动画城市标牌的东京街道上。她穿着黑色皮夹克、红色长裙和黑色靴子，拎着黑色钱包。她戴着太阳镜，涂着红色口红。她走路自信又随意。街道潮湿且反光，在彩色灯光的照射下形成镜面效果。许多行人走来走去。

# Prompt: 多镜头
A beautiful silhouette animation shows a wolf howling at the moon, feeling lonely, until it finds its pack.
# 一个美丽的剪影动画展示了一只狼对着月亮嚎叫，感到孤独，直到它找到狼群。
# Prompt: 世界模型
A cat waking up its sleeping owner demanding breakfast. The owner tries to ignore the cat, but the cat tries new tactics and finally the owner pulls out a secret stash of treats from under the pillow to hold the cat off a little longer.
# 提示：一只猫叫醒熟睡的主人，要求吃早餐。主人试图忽视这只猫，但猫尝试了新的策略，最后主人从枕头下拿出秘密藏匿的零食，让猫再呆一会儿。

# Prompt: 
A Chinese Lunar New Year celebration video with Chinese Dragon.
# 提示：与中国龙一起庆祝中国农历新年的视频。
```

## Sora 复现

### Latte

【2024-1-5】澳大利亚莫纳什大学+上海AI实验室+南京邮电推出 [Latte](https://maxin-cn.github.io/latte_project/), 又叫 Latent Diffusion Transformer, 采用了前边提到的视频切片序列和Vision Transformer的方法
- 从视频里抠出来一堆时空token，通过一系列的Transformer模块，在潜在空间里模仿视频分布。
- 因为视频里的token实在是多，设计了四个高效的变种，这样更好地处理视频的空间和时间维度。
- ![](https://pic3.zhimg.com/80/v2-ba4ff9578f02f1123cc7adba78945df2_1440w.webp)
- 论文 [Latte: Latent Diffusion Transformer for Video Generation](https://arxiv.org/pdf/2401.03048.pdf)
- 官方[Latte](https://github.com/Vchitect/Latte)
- 个人复现 [train_your_own_sora](https://github.com/lyogavin/train_your_own_sora)
- Latte训练需要80GB显存的A100或者H100。

### Open-Sora

【2024-3-18】[没等来OpenAI，等来了Open-Sora全面开源](https://mp.weixin.qq.com/s/vdr1WBCQVr9aS6bJYcdlRA)
- 继 2 周前推出成本直降 46% 的 Sora 训练推理复现流程后
- Colossal-AI 团队全面开源全球首个类 Sora 架构视频生成模型 「Open-Sora 1.0」，涵盖了整个训练流程，包括数据处理、所有训练细节和模型权重，携手全球 AI 热爱者共同推进视频创作的新纪元。
- [Open-Sora 开源地址](https://github.com/hpcaitech/Open-Sora)
- 目前版本仅使用了 400K 的训练数据，模型的生成质量和遵循文本的能力都有待提升。例如, 在上面的乌龟视频中，生成的乌龟多了一只脚。Open-Sora 1.0 也并不擅长生成人像和复杂画面。


### Vidu

【2024-4-27】[中国首个Sora级视频大模型发布](https://www.toutiao.com/article/7362381658915635724)

4月27日上午，2024中关村论坛年会未来人工智能先锋论坛上，生数科技联合清华大学发布中国首个长时长、高一致性、高动态性视频大模型——`Vidu`。

Vidu不仅能够模拟真实物理世界，还拥有丰富想象力，具备多镜头生成、时空一致性高等特点，这也是自Sora发布之后全球率先取得重大突破的视频大模型，性能全面对标国际顶尖水平，并在加速迭代提升中。

该模型采用团队原创的Diffusion与Transformer融合的架构`U-ViT`，支持一键生成长达**16秒**、分辨率高达1080P的高清视频内容。

根据现场演示的效果，Vidu能够模拟真实的物理世界，能够生成细节复杂、并且符合真实物理规律的场景，例如合理的光影效果、细腻的人物表情等。它还具有丰富的想象力，能够生成真实世界不存在的虚构画面，创造出具有深度和复杂性的超现实主义内容，例如“画室里的一艘船正在海浪中驶向镜头”这样的场景。

此外，Vidu能够生成复杂的动态镜头，不再局限于简单的推、拉、移等固定镜头，而是能够围绕统一主体在一段画面里就实现远景、近景、中景、特写等不同 镜头的切换，包括能直接生成长镜头、追焦、转场等效果，给视频注入镜头语言。

Vidu的快速突破源自于团队在贝叶斯机器学习和多模态大模型的长期积累和多项原创性成果。其核心技术 U-ViT 架构由团队于2022年9月提出，早于Sora采用的DiT架构，是全球首个Diffusion与Transformer融合的架构，完全由团队自主研发。


## 【2024-2-21】谷歌 Lumiere

- 【2024-1-26】[谷歌爆肝7个月做出的AI视频生成器，彻底改变游戏规则](https://m.huxiu.com/article/2592137.html)
- 【2024-2-21】[Google重磅发布AI视频生成模型Lunia，效果超Pika和Runway](https://www.toutiao.com/article/7337681289513927205)

Google重磅发布了AI视频大模型Lumiere，效果秒杀AI视频王者Pika和Runway， AI视频生成的新王诞生
- 功能丰富：文生视频、图文生视频、风格化、视频编辑
- 5s时长

Lumia采用了全新的AI视频生成算法，带来了更强的性能和视觉效果。
- 亮点一：视频生成时长从过去的4秒升级到5秒，内容更加丰富。
- 亮点二：视频画面的质量和连贯性显著提升，之前AI生成的视频画面非常不可控，视频画面过度极易出现畸形和异常。

大规模视频扩散模型 Lumiere凭借最先进的时空U-Net架构，在一次一致的通道中生成整个视频。通过联合空间和“时间”下采样（downsampling）来实现生成，这样能显著增加生成视频的长度和生成的质量。

## 谷歌 Genie

【2024-2-23】继OpenAI Sora的世界模型，Google也发布了基础世界模型Genie，生成式交互环境（Generative Interactive Environments）。

Genie 是一个 110 亿参数的基础世界模型，可通过单张图像提示生成可玩的交互式环境。它生成的虚拟世界「自主可控」，一键能生成可玩的虚拟游戏！

Genie 由三个部分组成：
- （1）一个潜在动作模型，用于推断每对帧之间的潜在动作；
- （2）一个视频 tokenizer，用于将原始视频帧转换为离散 token；
- （3）一个动态模型，用于在给定潜在动作和过去帧 token 的情况下，预测视频的下一帧。

有了Genie，可以：
- （1）用文本生成图像，再把图像输入到Genie，生成一个可玩的虚拟游戏；
- （2）画一张草图，输入给Genie，……
- （3）Genie是一种通用方法，其训练视频的方法可以用于多个其他领域，比如机器人，智能体等

- 项目：[genie-2024](sites.google.com/view/genie-2024/home)
- 论文：[Genie: Generative Interactive Environments](arxiv.org/abs/2402.15391)

Genie: Generative Interactive Environments（生成式交互环境）

论文摘要：
- 介绍 Genie，这是第一个通过无标签的互联网视频以无监督方式训练的生成交互环境。

该模型可以被提示生成无数种通过文本、合成图像、照片甚至草图描述的动作可控的虚拟世界。在 11B 参数下，Genie 可以被视为基础世界模型。它由时空视频分词器、自回归动力学模型和简单且可扩展的潜在动作模型组成。Genie 使用户能够在生成的环境中逐帧进行操作，尽管训练时没有任何真实动作标签或世界模型文献中常见的其他特定领域要求。

此外，由此产生的学习潜在动作空间有助于训练智能体模仿未见过的视频中的行为，为未来训练多面手智能体开辟道路。


## SadTalker
 

【2024-5-16】SadTalker 是一款开源的AI工具，将静态图像转换成动态视频，并使图像中的人物根据音频内容进行讲话。
- [项目主页](https://sadtalker.github.io/)

它使用了一种叫做 SadNet 的神经网络来实现，该神经网络可以捕捉音频中的情感和语音模式，并将其转化为逼真的面部表情和头部动作。

SadTalker 的工作原理可以简单概括为以下几个步骤：
- 输入： 用户提供一张图片和一段音频。音频可以是用户自己的录音，也可以是文本转语音生成的语音。
- 处理： SadTalker 分析音频以提取情感和语音模式。
- 输出： 然后，该工具会根据提取的语音特征，使图像中的人物进行相应的动画，包括嘴唇运动、面部表情甚至轻微的头部动作。

SadTalker 具有以下特点：
- 易于使用： SadTalker 提供了一个简单的界面，即使是没有任何技术背景的用户也可以轻松上手。
- 功能强大： 该工具可以生成逼真且自然的动画效果，并支持多种音频格式和图像类型。
- 开源： SadTalker 是开源的，这意味着任何人都可以对其进行修改和扩展。

SadTalker 的应用非常广泛，包括：
- 创建虚拟形象： 用户可以使用自己的照片或插图来创建逼真的虚拟形象，并使其根据自己的声音或其他语音进行讲话。
- 动画演示文稿： 在演示文稿中添加动画角色或讲解视频可以使其更加生动有趣，并提高观众的参与度。
- 娱乐目的： SadTalker 可以用于制作搞笑视频或表情包，为用户带来欢乐。


# 结束