---
layout: post
title:  "机器翻译专题 Machine Translation"
date:   2020-05-05 21:50:00
categories: 自然语言处理
tags: 机器翻译 llm
excerpt: 机器翻译方法总结
author: 鹤啸九天
mathjax: true
permalink: /translation
---

* content
{:toc}


# 机器翻译

## 机器翻译介绍

- 【2022-11-10】10月11日，谷歌推出了一项叫做“翻译中心”（Translation Hub）的人工智能云服务, 类似翻译外包平台。这一消息在语言服务行业及其他领域引起了轰动，谷歌翻译中心可以“为需要将大量文档翻译成许多不同语言的组织提供自助文档翻译服务。这一平台全程可监控，并且用户界面十分友好。” [原文](https://mp.weixin.qq.com/s?__biz=MzIyOTcyODA2Ng==&mid=2247510000&idx=1&sn=59598d08c74366c623ceef40ab510dd7)
- 【2018-10】[独家：“论文致谢刷屏”博士黄国平演讲干货](https://mp.weixin.qq.com/s/RYnJnkz-55qj94hyy4zm2Q),QCon 全球软件开发大会 2018 上海站的演讲[视频](https://time.geekbang.org/dailylesson/detail/100020790)
- 【2020-6-5】[机器翻译：统计建模与深度学习方法](https://opensource.niutrans.com/mtbook/index.html)，[ppt地址](https://github.com/NiuTrans/MTBook/blob/master/slides)
- ![](https://opensource.niutrans.com/guideline.png)
- 【2020-6-10】Google官方示例：[基于注意力的神经机器翻译](https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=zh-cn)
  - ![](https://tensorflow.org/images/spanish-english.png)
- 【2021-1-13】翻车的机器翻译
  - 大数据文摘：[机器翻译古文也翻车？读了20次“苟富贵勿相忘”后，谷歌：没钱的人总会被遗忘](https://mp.weixin.qq.com/s/E2VESXhJLaNmJMlp84sXaA)
  - [谷歌翻译20次鲁迅《狂人日记》中的经典“吃人”片段！极度生草](https://www.bilibili.com/video/BV1nK4y1r75x/?spm_id_from=333.788.recommend_more_video.1)
  - [谷歌翻译20次司马迁《陈涉世家》！ 清朝，瑞士，东罗马，曹魏竟在同一时代](https://www.bilibili.com/video/BV1Jf4y1C7oP?from=search&seid=7681248349324754656)

<iframe src="//player.bilibili.com/player.html?aid=288370813&bvid=BV1Jf4y1C7oP&cid=271241642&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  height="600" width="100%"> </iframe>



## 实时翻译


### SeamlessM4T

META 开源 实时翻译模型 SeamlessM4T

【2024-8-22】Meta 开源 SeamlessM4T，无缝翻译、转录语音和文本的基础多语言、多任务模型。
- web demo: [Seamless Communication Translation Demo](https://seamless.metademolab.com/demo) 要翻墙
- paper : [seamless-m4t](https://ai.meta.com/research/publications/seamless-m4t/)
- code: [Foundational Models for State-of-the-Art Speech and Text Translation](https://github.com/facebookresearch/seamless_communication)
- model: [Seamless M4T - a Hugging Face Space by facebook](https://huggingface.co/spaces/facebook/seamless_m4t)

Seamless M4T(Massively Multilingual & Multimodal Machine Translation):
- ASR(Automatic speech recognition): 100种语言的语言识别
- S2TT(Speech-to-text translation): 近100种语言的语言转文本
- S2ST(Speech-to-speech translation): 支持近100种的语音输入， 35+的语音输出。
- T2ST (Text-to-speech translation): 支持近100中的文本输入，35+的语音输出。
- T2ST (Text-to-Text translation): 近100种语言的文本互译

模型架构
- ![](https://pic4.zhimg.com/v2-0f9fc459f6c422f718acbfb6b2cfcb5b_1440w.jpg)

Demo 效果
- ![](https://pica.zhimg.com/v2-01ac3e27af46b15d99edfc43dcf0625c_1440w.jpg)

支持本地推理+finetune

先配置环境

```sh
conda activate your_env 
git clone https://github.com/facebookresearch/seamless_communication.git
cd seamless_communication
pip install .
# 安装一个额外的依赖库libsndfile
conda install -y -c conda-forge libsndfile
```

参考[文档](https://github.com/facebookresearch/seamless_communication/tree/main/scripts/m4t/predict)

```py
import torch
import torchaudio
from seamless_communication.models.inference import Translator

# Initialize a Translator object with a multitask model, vocoder on the GPU.
translator = Translator("seamlessM4T_large", "vocoder_36langs", torch.device("cuda:0"), torch.float16)

# T2TT
translated_text, _, _ = translator.predict("Nice to meet you", "t2tt", "cmn", src_lang="eng")
print(translated_text)

'''
很高兴见到你
'''

```


## 机器翻译工具


### 插件

Chrome插件
- 【2024-2-8】[沉浸式翻译](https://chrome.google.com/webstore/detail/immersive-translate-web-p/bpoadfkcbjbfhfodiogcnhhhpibjhbnh/related) 双语对照网页翻译 & PDF文档翻译，收费
- [OpenAI Translator](https://chrome.google.com/webstore/detail/openai-translator/ogjibjphoadhljaoicdnjnmgokohngcc)，需要填写OpenAI key





### 本地翻译

#### LibreTranslate

【2021-1-22】【LibreTranslate：可完全**本地化**部署的开源机器翻译API服务，基于 `Argos Translate`[LibreTranslate](https://github.com/uav4geo/LibreTranslate) 
- Free and Open Source Machine Translation API. 100% self-hosted, no limits, no ties to proprietary services. Built on top of Argos Translate.' by UAV4GEO
- [在线体验Demo](https://libretranslate.com/)

实测：windows下安装失败，错误信息

```s
ERROR: Could not find a version that satisfies the requirement ctranslate2 (from argostranslate==1.0) (from versions: none)；ERROR: No matching distribution found for ctranslate2 (from argostranslate==1.0)
```

#### Offine-Text-Translate

Offine-Text-Translate
- 支持多语言的本地离线文字翻译API工具，基于开源项目 LibreTranslate 封装而成，提供方便的本地机器部署翻译API服务，无需Docker，同时提供了Windows预编译exe包，简化了部署过程。[参考文献](http://github.com/jianchang512/ott)



# 结束