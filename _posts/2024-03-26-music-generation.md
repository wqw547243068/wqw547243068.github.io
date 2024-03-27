---
layout: post
title:  "音乐生成专题 - Music Generation"
date:   2024-03-26 08:01:00
categories: 大模型
tags: sora 音乐
excerpt: 音乐生成技术
mathjax: true
permalink: /music_gen
---

* content
{:toc}

# 音乐生成


## 音乐知识

更多音乐知识见[站内专题](music)

### 曲风

到底什么是「古典(Classical)」风格？什么是「乡村(Country)」风格？

许多网站提供各种音乐风格和流派的信息，比如：[Spotify](https://open.spotify.com/)、[Apple Music](https://music.apple.com/cn/browse)等，或者音乐百科类网站。
- 以Spotify举例，可以直接在主页上面浏览各种风格。
- ![](https://pic3.zhimg.com/80/v2-c23d01c2e64ae461242774220bee9c46_1440w.webp)


## 音乐生成技术

音乐生成技术、工具

Text-to-Audio : AudioLM、Whisper、Jukebox
- AudioLM由谷歌开发，将输入音频映射到一系列离散标记中，并将音频生成转换成语言建模任务，学会基于提示词产生自然连贯的音色。在人类评估中，认为它是人类语音的占51.2%、与合成语音比率接近，说明合成效果接近真人。
- Jukebox由OpenAI开发的音乐模型，可生成带有唱词的音乐。通过分层VQ-VAE体系将音频压缩到离散空间中，损失函数被设计为保留最大量信息，用于解决AI难以学习音频中的高级特征的问题。不过目前模型仍然局限于英语。
- Whisper由OpenAI开发，实现了多语言语音识别、翻译和语言识别，目前模型已经开源并可以用pip安装。模型基于68万小时标记音频数据训练，包括录音、扬声器、语音音频等，确保由人而非AI生成。

音乐生成上比较出名的：
- DeepMusic
- WaveNet
- Deep Voice
- Music AtuoBot


## 音乐提示词 

### 提示词结构

参考：
- [Suno教程篇：音乐小白也能使用Suno AI零门槛创作音乐](https://zhuanlan.zhihu.com/p/688696210?utm_psn=1756068864734138368)

提示词参考

好的谱曲提示词包含以下要素，可以酌情增减，仅供参考
> 风格 + 情感 + 乐器 + 节奏 + 人声

说明
- 1、风格：流行(Pop)，古典(Classical)，爵士(Jazz)，电子(Electronic)，摇滚(Rock)，乡村(Country)，民谣(Folk)，嘻哈(Hip-hop)，布鲁斯(Blues)，拉丁(Latin)
- 2、情感：欢快(Cheerful)，悲伤(Sad)，浪漫(Romantic)，激昂(Passionate)，温柔(Gentle)，忧郁(Melancholic)，神秘(Mysterious)，紧张(Tense)，恐怖(Horrifying)，宁静(Peaceful)
- 3、乐器：钢琴(Piano)，吉他(Guitar)，小提琴(Violin)，鼓(Drum)，贝斯(Bass)，长笛(Flute)，萨克斯(Saxophone)，小号(Trumpet)，大提琴(Cello)，口琴(Harmonica)
- 4、节奏：快速(Fast)，慢速(Slow)，中等(Medium)，渐快(Accelerating)，渐慢(Decelerating)，自由(Free)，稳定(Steady)，跳跃(Jumpy)，拖延(Dragging)，犹豫(Hesitant)
- 5、人声：男声(Male vocals)，女声(Female vocals)，童声(Children's vocals)，合唱(Choir)
  - 纯音乐时，此项可省略

### 提示词实例

- 1、创作一首欢快的流行电子舞曲
  - 提示词：upbeat, pop, electronic, dance, synthesizer, fast
- 2、创作一首浪漫的古典钢琴曲
  - 提示词：romantic, classical, piano, tender, slow
- 3、创作一首悲伤的爵士萨克斯风曲
  - 提示词：melancholic, jazz, saxophone, sentimental, improvisation, medium
- 4、创作一首激昂的摇滚吉他曲
  - 提示词：passionate, rock, electric guitar, powerful, fast
- 5、创作一首温馨的民谣木吉他曲
  - 提示词：warm, folk, acoustic guitar, fingerstyle, gentle



## Suno AI

【2024-3-22】Suno AI发布了V3版音乐生成模型

用户只需要提供音乐生成指令，v3版模型就能在几秒-几分钟内，生成一首时长两分钟的高质量音乐片段。

免费使用
- 官方[介绍](https://www.suno.ai/blog/v3)
- [体验地址](https://app.suno.ai)

目前，免费注册
- 新用户每天有50块的免费额度，每天可以创建10首歌曲（5 * 2）
- 付费用户权限依次提升

参考
- [音乐生成：给Sora加上声音](https://mp.weixin.qq.com/s/HuREa4EcO79G-J2qWwAWkA)
- [Suno教程篇：音乐小白也能使用Suno AI零门槛创作音乐](https://zhuanlan.zhihu.com/p/688696210?utm_psn=1756068864734138368)

### Suno AI 功能


特点 
- 用户只用几个简短的词语就可以用任何语言创作歌曲
- Suno v3 新增更丰富的音乐风格和流派选项，比如古典音乐、爵士乐、Hiphop、电子等新潮曲风

相比与之前版本
- v3音乐质量更高，而且支持各种风格和流派的音乐和歌曲。
- 提示词连贯性大幅提升，歌曲结尾的质量也获得了极大提高。
- AI音乐水印系统：每段由平台生成的音乐都添加了人声无法识别的水印，从而在未来能够保护用户在Suno的创作，打击抄袭，防止将Suno产生的音乐进行滥用。

功能
- 1、Suno AI内置翻译器，可直接输入中文提示词，后台自动转换为英文。也可以将中文提示词翻译成英文，再输入到Suno AI。
- 2、「`Instrumental`」是 纯BGM，不含人声，关闭则带人声
  - 「`Song Description`」处输入提示词，点击「Create」按钮即可创作。
- 3、选中「`Custom Mode`」，可输入歌词填曲。
  - 只需要在「`Lyrics`」处填入歌词（可以直接输入中文歌词），「`Style of Music`」处写入歌曲的风格提示词，Suno AI 就能生成指定风格歌曲。
  - 对于给定歌词，段落前加`[Verse]`（主歌）、`[Rap]`（说唱）、`[Chorus]`（副歌）等来告诉AI这段歌词应该怎么唱。
- 歌曲延时：点击已经生成音乐项的「`...`」按钮，选择「`Continue From This Song`」可歌曲延长。


![](https://pic4.zhimg.com/80/v2-3e4f6a95dff63b87593d240eeb1338ff_1440w.jpg)



### 歌词结构


通过下面这些标记指示歌曲不同部分，帮助AI理解歌曲的结构和情感表达。
1、歌曲结构标记:
- `[Verse]` - 主歌，主歌是歌曲的核心部分，通常包含歌曲的主要歌词和旋律。
- `[Chorus]` - 副歌，副歌部分，通常旋律更加朗朗上口,歌词重复度高。
- `[Pre-Chorus]` - 前副歌，通常用于过渡,为副歌做铺垫。
- `[Bridge]` - 桥段，通常在副歌之后，旋律和歌词风格与主歌和副歌不同，起到调剂作用。
- `[Intro]` - 前奏，通常是纯音乐或者少量歌词。
- `[Outro]` - 尾奏，通常是音乐渐弱或者重复某些歌词。
- `[Interlude]` - 间奏，通常是纯音乐部分,用于连接不同的歌曲部分。
2、歌词演唱风格标记:
- `[Rap]` - 说唱
- `[Ad-lib]` - 即兴演唱
- `[Harmony]` - 和声，通常由多个声部组成,与主旋律形成和谐的音乐效果。
- `[Whisper]` - 耳语，耳语般的演唱


### 案例


如梦令，音乐片段如下 
- [1](https://app.suno.ai/song/e1b7cea9-396f-4adb-a20b-25703696cd64)
- [2](https://app.suno.ai/song/d4759bf6-95b2-4619-a207-b03a9921ede1)

#### 视频配曲

直接使用 OpenAI Sora 视频生成提示词
>A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage.

1分钟后，生成音乐：歌词 + 音乐

歌词部分

```py
Neon Glow
electronic pop
v3
March 26, 2024
Pause
[Verse]
She's a vision, beauty in motion
Walking down the street, pure devotion (yeah)
Stylish as ever, the center of attention
Tokyo nights, never-ending fascination (oh-oh)

[Verse 2]
In the glow of neon lights
She shines like a star in the city's sky
With every step she takes, the world comes alive
Can't help but be mesmerized (ooh-yeah)

[Chorus]
Tokyo nights, neon glow
Every corner, every street, a colorful show
In this cityscape, she stands tall
A stylish woman that captures it all (captures it all)
# ------------翻译-----------
Neon Glow
电子流行
v3
2024年3月26日
[诗歌]
她是一个视觉，动感美丽
走在街上，纯粹的奉献（是的）
时尚如常，成为众人关注的焦点
东京之夜，永无止境的迷恋（哦-哦）
[诗歌2]
在霓虹灯的照耀下
她如同城市天空中的一颗星星闪耀
每迈出一步，世界都变得生动起来
禁不住被迷住（哦-是的）
[合唱]
东京之夜，霓虹闪耀
每个角落，每条街道，一场色彩斑斓的表演
在这座城市景观中，她屹立不倒
一个捕捉一切的时尚女性（捕捉一切）
```

音乐追加到 sora 视频上 


<iframe width="720" height="405" frameborder="0" src="https://www.ixigua.com/iframe/7350543565593772579?autoplay=0" referrerpolicy="unsafe-url" allowfullscreen> </iframe>



#### 个人vlog生成背景音乐

个人vlog通常记录日常生活、旅行见闻、兴趣爱好等内容，音乐风格上以轻快、明朗为主。

选择一些流行音乐元素，同时加入一些吉他、钢琴等乐器，营造出一种温馨、惬意的氛围。

提示词：
- pop music（流行音乐）、light（轻快）、guitar（吉他）、piano（钢琴）

#### 婚礼视频制作浪漫背景音乐

婚礼是人生中的一个重要时刻。

音乐选择上，用一些柔和、浪漫的元素，例如弦乐、钢琴等，同时加入一些爱情、甜蜜的关键词，营造出梦幻、温馨的氛围。

提示词：
- romantic（浪漫）、love（爱情）、sweet（甜蜜）、strings（弦乐）、piano（钢琴）

#### 游戏视频生成背景音乐

游戏直播通常需要一些激昂、刺激的背景音乐来渲染气氛，同时又不能过于喧闹，影响主播的解说和游戏音效。我们可以选择一些电子音乐元素，同时加入一些鼓点、合成器等元素，营造出紧张、刺激的氛围。

提示词：
- electronic music（电子音乐）、exciting（刺激的）、drums（鼓点）、synthesizer（合成器）

#### 自然风光类视频生成背景音乐

自然风光类视频通常展示了大自然的美景，为了突出自然的宁静、祥和，选择一些轻柔、舒缓的音乐元素，如长笛、竖琴等，同时加入一些自然、宁静的关键词，营造出一种与自然和谐相处的氛围。

提示词：
- soft（轻柔）、peaceful（宁静）、nature（自然）、flute（长笛）、harp（竖琴）

#### 美食类视频生成背景音乐

为了突出食物的诱人和美味，选择一些轻快、愉悦的音乐元素，如口哨、手鼓等，同时加入一些快乐的关键词，营造出一种欢乐、享受的氛围。

提示词：
- light（轻快）、happy（愉悦）、whistle（口哨）、bongos（手鼓）


## 扩展应用

生成的音乐能否更加丰富？
- 让LLM生成歌词
- 生成插图
- 针对prompt同时生成视频？

把各类LLM工具联动起来，让 Midjourney生图、Runway 动起来，最后再让Suno配乐， 想象空间无限 。。。
已经有一堆人在疯狂测试，杰作频出。



# 结束