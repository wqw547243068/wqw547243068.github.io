---
layout: post
title:  "视频理解 - Video Understanding"
date:   2023-05-04 08:01:00
categories: 计算机视觉
tags: 视频理解 ffmpeg 视频
excerpt: 视频理解
mathjax: true
permalink: /video
---

* content
{:toc}

# 视频

【2023-5-5】 [FesianXu](github.com/FesianXu): [万字长文漫谈视频理解](https://zhuanlan.zhihu.com/p/158702087)

作为多媒体中重要的信息载体，视频的地位可以说是数一数二的，然而目前对于AI算法在视频上的应用还不够成熟，理解视频内容仍然是一个重要的问题亟待解决攻克。

## 什么是视频

### 视频为什么重要？

以视频为代表的动态多媒体，结合了音频，视频，是当前的，更是未来的**互联网流量之王**。 

国家互联网信息办公室的中国互联网络发展状况统计报告
>- 截至 2018 年 12 月，网络视频、网络音乐和网络游戏的用户规模分别为 6.12 亿、5.76 亿和 4.84 亿，使用率分别为 73.9%、69.5%和 58.4%。短视频用户规模达 6.48 亿，网民使用比例为 **78.2%**。
>- 截至 2018 年 12 月，网络视频用户规模达 6.12 亿，较 2017 年底增加 3309 万，占网民 整体的 73.9%；手机网络视频用户规模达 5.90 亿，较 2017 年底增加 4101 万，占手机 网民的 72.2%。

2018年各类应用使用时长占比
- ![](https://pic3.zhimg.com/80/v2-6a77c9189cfad7ccaa9dba9ed5cf38ee_1440w.webp)
- 包括短视频在内的视频用户时长占据了约20%的用户时长，占据了绝大多数的流量，同时网络视频用户的规模也在逐年增加。

固定带宽/4G平均下载速率变化曲线
- ![](https://pic3.zhimg.com/80/v2-a0c8b32b0c72774ade5a1500eb47673a_1440w.webp)

## 视频理解

理解视频(understanding the video) 是一件非常抽象的事情，在神经科学尚没有完全清晰，如果按照人类感知去理解，终将陷入泥淖。

在理解视频这个任务中，到底在做什么？
- 首先，对比于文本，图片和音频，视频特点：动态的按照时间排序的图片序列
- 然而，图片**帧**间有着密切的联系，存在上下文联系；
- 视频有音频信息。

因此进行视频理解，先要再时间序列上建模，同时还需要空间上的关系组织。

目前理解视频主要集中在**以人为中心**的角度进行，由于视频是动态的，因此描述视频中的物体随着时间变化，在进行什么动作，很重要。
- **动作识别**在视频理解中占据了一个很重要的地位。

视频分析的主要难点：
- 需要大量的算力，视频的大小远大于图片数据，需要更大的算力进行计算。
- 低质量，很多真实视频拍摄时有着较大的运动模糊，遮挡，分辨率低下，或者光照不良等问题，容易对模型造成较大的干扰。
- 需要大量的数据标签，特别是在深度学习中，对视频的时序信息建模需要海量的训练数据才能进行。时间轴不仅仅是添加了一个维度那么简单，其对比图片数据带来了时序分析，因果分析等问题。

### 子任务

理解视频具体子任务：
- 视频**动作分类**：对视频中的动作进行分类
- 视频**动作定位**：识别原始视频中某个动作的开始帧和结束帧
- 视频**场景识别**：对视频中的场景进行分类
- **原子动作**提取
- 视频**文字说明**（Video Caption）：给给定视频配上文字说明，常用于视频简介自动生成和跨媒体检索
- **集群**动作理解：对某个集体活动进行动作分类，常见的包括排球，篮球场景等，可用于集体动作中关键动作，高亮动作的捕获。
- 视频**编辑**。
- **视频问答**系统（Video QA）：给定一个问题，系统根据给定的视频片段自动回答
- 视频**跟踪**：跟踪视频中的某个物体运动轨迹
- 视频**事件理解**：不同于动作，动作是一个更为短时间的活动，而事件可能会涉及到更长的时间依赖
- ...


## 视频数据


### 视频数据模态

视频动作理解是非常广阔的研究领域，输入的视频形式也不一定是常见的**RGB视频**，还可能是depth**深度图序列**，Skeleton**关节点信息**，IR**红外光谱**等。
- ![](https://pic3.zhimg.com/80/v2-34fd2b816579389d8dc46e7c8d705ab2_1440w.webp)

**RGB视频**是最容易获取的模态，然而随着很多**深度摄像头**的流行，**深度图序列**和**骨骼点序列**的获得也变得容易起来。
- 深度图和骨骼点序列对比RGB视频来说，其对光照的敏感性较低，数据冗余较低，有着许多优点。

### 视频动作分类数据集

公开的视频动作分类数据集有很多，比较流行的`in-wild数据集`主要是在YouTube上采集到的，包括以下的几个。
- HMDB-51，该数据集在YouTube和Google视频上采集，共有6849个视频片段，共有51个动作类别。
- UCF101，有着101个动作类别，13320个视频片段，大尺度的摄像头姿态变化，光照变化，视角变化和背景变化。
  - ![](https://pic4.zhimg.com/80/v2-ee25f80c4c52c9ef7559a94f22dde737_1440w.webp)
- sport-1M，也是在YouTube上采集的，有着1,133,157 个视频，487个运动标签。
  - ![](https://pic4.zhimg.com/80/v2-b10e40e4aaf656e3d366a11235ba2e33_1440w.webp)
- YouTube-8M, 有着6.1M个视频，3862个机器自动生成的视频标签，平均一个视频有着三个标签。
- YouTube-8M Segments，是YouTube-8M的扩展，其任务可以用在视频动作定位，分段（Segment，寻找某个动作的发生点和终止点），其中有237K个人工确认过的分段标签，共有1000个动作类别，平均每个视频有5个分段。该数据集鼓励研究者利用大量的带噪音的视频级别的标签的训练集数据去训练模型，以进行动作时间段定位。
  - ![](https://pic1.zhimg.com/80/v2-d134999c9d2c1fc4f9ae9923fc8bb7a0_1440w.webp)
- Kinectics 700，这个系列的数据集同样是个巨无霸，有着接近650,000个样本，覆盖着700个动作类别。每个动作类别至少有着600个视频片段样本。

以上数据集模态都是RGB视频，还有些数据集是多模态的：
- NTU RGB+D 60： 包含有60个动作，多个视角，共有约50k个样本片段，视频模态有RGB视频，深度图序列，骨骼点信息，红外图序列等。
- NTU RGB+D 120：是NTU RGB+D 60的扩展，共有120个动作，包含有多个人-人交互，人-物交互动作，共有约110k个样本，同样是多模态的数据集。


## 视频理解方法


### 早期CV方法


深度学习之前，CV算法工程师是**特征工程师**，手动设计特征，而这是一个非常困难的事情。

手动设计特征并且应用在视频分类的主要套路有：
- 特征设计：挑选合适的特征描述视频
  - 局部特征（Local features）：比如HOG（梯度直方图 ）+ HOF（光流直方图）
  - 基于轨迹的（Trajectory-based）：Motion Boundary Histograms（MBH）[4]，improved Dense Trajectories （iDT） ——有着良好的表现，不过计算复杂度过高。
- 集成挑选好的局部特征： 光是局部特征或者基于轨迹的特征不足以描述视频的全局信息，通常需要用某种方法集成这些特征。
  - 视觉词袋（Bag of Visual Words，BoVW），BoVW提供了一种通用的通过局部特征来构造全局特征的框架，其受到了文本处理中的词袋（Bag of Word，BoW）的启发，主要在于构造词袋（也就是字典，码表）等。
  - ![](https://pic2.zhimg.com/80/v2-c5105cbf72aca4c7e49cb67212d2ba99_1440w.webp)
  - Fisher Vector，FV同样是通过集成局部特征构造全局特征表征
  - ![](https://pic4.zhimg.com/80/v2-4951d630efffccb82d5c9923e98f3ba7_1440w.webp)
  - 要表征视频的时序信息，我们主要需要表征的是动作的运动（motion）信息，这个信息通过帧间在时间轴上的变化体现出来，通常我们可以用光流（optical flow）进行描述，如TVL1和DeepFlow。
  - ![](https://pic3.zhimg.com/80/v2-82fe89075d26b6c676fe50f5ae3a4eee_1440w.webp)


### 深度学习CV方法

深度学习时代，视频动作理解主要工作量在于如何设计合适的**深度网络**，而不是手动设计特征。设计这样的深度网络的过程中，需要考虑两个方面内容：
- 模型方面：什么模型可以最好的从现有的数据中捕获时序和空间信息。
- 计算量方面：如何在不牺牲过多的精度的情况下，减少模型的计算量。

组织时序信息是构建视频理解模型的一个关键点，Fig 3.2展示了若干可能的对多帧信息的组织方法。
- Single Frame，只是考虑了当前帧的特征，只在最后阶段融合所有的帧的信息。
- Late Fusion，晚融合使用了两个共享参数的特征提取网络（通常是CNN）进行相隔15帧的两个视频帧的特征提取，同样也是在最后阶段才结合这两帧的预测结果。
- Early Fusion，早融合在第一层就对连续的10帧进行特征融合。
- Slow Fusion，慢融合的时序感知野更大，同时在多个阶段都包含了帧间的信息融合，伴有层次（hierarchy）般的信息。这是对早融合和晚融合的一种平衡。

最终的预测阶段，从整个视频中采样若各个片段，对这采样的片段进行动作类别预测，其平均或者投票将作为最终的视频预测结果。
- ![](https://pic3.zhimg.com/80/v2-901a384d969876d7038f02dc395c092a_1440w.webp)


# 视频处理工具



## ffmpeg

ffmpeg [下载](http://ffmpeg.org/download.html)

### ffmpeg介绍

【2023-1-10】
- [ffmpeg的基本用法](https://segmentfault.com/a/1190000040982815)
- [FFmpeg 视频处理入门教程](https://www.ruanyifeng.com/blog/2020/01/ffmpeg.html)
- [ffmpeg的图形化操作](https://ffmpeg.guide/graph/demo)

ffmpeg主要组成部分
- 1、libavformat：用于各种音视频封装格式的生成和解析，包括获取解码所需信息以生成解码上下文结构和读取音视频帧等功能，包含demuxers和muxer库；
- 2、libavcodec：用于各种类型声音/图像编解码；
- 3、libavutil：包含一些公共的工具函数；
- 4、libswscale：用于视频场景比例缩放、色彩映射转换；
- 5、libpostproc：用于后期效果处理；
- 6、ffmpeg：是一个命令行工具，用来对视频文件转换格式，也支持对电视卡实时编码；
- 7、ffsever：是一个HTTP多媒体实时广播流服务器，支持时光平移；
- 8、ffplay：是一个简单的播放器，使用ffmpeg 库解析和解码，通过SDL显示；

在这组成部分中，需要熟悉基础概念有
- `容器`(Container): 容器就是一种文件格式，比如flv，mkv等。包含下面5种流以及文件头信息。
  - 视频文件本身其实是一个`容器`（container），里面包括了`视频`和`音频`，也可能有`字幕`等其他内容。
  - 视频格式：MP4，MKV，WebM，AVI。可以用 ffmpeg -formats 查看
- `流`(Stream): 是一种视频数据信息的传输方式，5种流：音频，视频，字幕，附件，数据。
- `帧`(Frame): 帧代表一幅静止的图像，分为I帧，P帧，B帧。
- `编解码器`(Codec): 是对视频进行压缩或者解压缩，`CODEC` =COde （`编码`） +DECode（`解码`）
  - 视频和音频都需要经过编码，才能保存成文件。不同的编码格式（CODEC），有不同的压缩率，会导致文件大小和清晰度的差异。
  - 常用的视频编码格式：ffmpeg -codecs
    - H.262、H.264、H.265 —— 有版权，但可以免费使用
    - VP8、VP9、AV1 —— 无版权
    - MP3、AAC —— 音频编码格式
  - `编码器`（encoders）是实现某种编码格式的库文件。只有安装了某种格式的编码器，才能实现该格式视频/音频的编码和解码。
  - FFmpeg 内置的视频编码器。
    - libx264：最流行的开源 H.264 编码器
    - NVENC：基于 NVIDIA GPU 的 H.264 编码器
    - libx265：开源的 HEVC 编码器
    - libvpx：谷歌的 VP8 和 VP9 编码器
    - libaom：AV1 编码器
  - 音频编码器: ffmpeg -encoders
    - libfdk-aac
    - aac
- `复用`/`解复用`(mux/demux): 
  - 把不同的流按照某种容器的规则放入容器，这种行为叫做`复用`（mux）
  - 把不同的流从某种容器中解析出来，这种行为叫做`解复用`(demux)



### 测试

[测试人工智能自动语音识别系统](https://cloud.tencent.com/developer/article/1644302)

样本是这四句话：
> - Due to delays, we need to reconsider our schedule this week.
> - As we've discussed, we need to put our most experienced staff on this.
> - Can you suggest an alternative to the restructuring?
> - We'll implement quality assurance processes before the final review.

故意读得磕磕巴巴，每个音频大约在13秒。但是录制出来的是m4a格式，得转换下，这里用ffmpeg



### ffmpeg安装

1. ffmpeg[下载](http://ffmpeg.org/download.html)
2. 解压到指定目录，将bin文件目录添加到path路径（电脑-属性-高级系统设置-环境变量-path-新建）
3. 命令行（windows+r 输入cmd）输入：ffmpeg -version 出结果表示成功。

### ffmpeg使用

ffmpeg命令格式

```sh
ffmpeg {1} {2} -i {3} {4} {5}
```

五个部分的参数依次如下。
1. 全局参数
1. 输入文件参数
1. 输入文件
1. 输出文件参数
1. 输出文件

常用命令
- 可用的bit流 ：ffmpeg –bsfs
- 可用的编解码器：ffmpeg –codecs
- 可用的解码器：ffmpeg –decoders
- 可用的编码器：ffmpeg –encoders
- 可用的过滤器：ffmpeg –filters
- 可用的视频格式：ffmpeg –formats
- 可用的声道布局：ffmpeg –layouts
- 可用的license：ffmpeg –L
- 可用的像素格式：ffmpeg –pix_fmts
- 可用的协议：ffmpeg -protocals

1. 视频格式转换：ffmpeg -i num.mp4 -codec copy num2.avi
  - 将num.mp4复制并转换为num2.avi
  - 注：-i 后表示要进行操作的文件
2. gif制作：ffmpeg -i num.mp4 -vframes 20 -y -f gif num3.gif
  - 将num.mp4的前20帧制作为gif并命名为num3
3. 视频截取：ffmpeg -i num.mp4 -ss 0 -t 3 -codec copy cut1.mp4
  - -ss后数字表示截取时刻，-t后数字表示截取时长
  - 截取视频某一时刻为图片：ffmpeg -i num.mp4 -y -f image2 -ss 2 -t 0.001 -s 400x300 pic.jpg
  - 将2s时刻截取为400x300大小的名为pic.jpg的图片（-ss后的数字为截取时刻）
4. 每秒截取一张图片：ffmpeg -i num.mp4 -r 1 image%d.jpg
  - 将视频num.mp4进行每秒截取一张图片，并命名为imagei.jpg（i=1，2，3...）
  - 注：-r后的数字表示每隔多久截取一张。

#### 全局参数

主要全局参数：
- -i 设定输入流 
- -f 设定输出格式 
- -ss 开始时间 

输出视频文件参数：
- -b 设定视频流量(码率)，默认为200Kbit/s 
- -r 设定帧速率，默认为25 
- -s 设定画面的宽与高 
- -aspect 设定画面的比例 
- -vn 不处理视频 
- -vcodec 设定视频编解码器，未设定时则使用与输入流相同的编解码器 
- -qscale 0 保留原始的视频质量

输出音频文件参数：
- -ar 设定采样率 
- -ac 设定声音的Channel数 
- -acodec 设定声音编解码器，未设定时则使用与输入流相同的编解码器 
- -an 不处理音频

```yml
-c：指定编码器
-c copy：直接复制，不经过重新编码（这样比较快）
-c:v：指定视频编码器
-c:a：指定音频编码器
-i：指定输入文件
-an：去除音频流
-vn： 去除视频流
-preset：指定输出的视频质量，会影响文件的生成速度，有以下几个可用的值 ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow。
-y：不经过确认，输出时直接覆盖同名文件。
```


#### 获取媒体文件信息

```sh
ffmpeg -i file_name
ffmpeg -i video_file.mp4
ffmpeg -i audio_file.mp3
ffmpeg -i video_file.mp4 -hide_banner # hide_banner 来隐藏掉ffmpeg本身的信息
ffmpeg -i audio_file.mp3 -hide_banner
```

#### 转换文件格式

转换媒体文件
- ffmpeg 最有用的功能：在不同媒体格式之间进行自由转换。
- 指明输入和输出文件名就行，ffmpeg 会从后缀名猜测格式，这个方法同时适用于视频和音频文件

```sh
ffmpeg -i video_input.mp4 video_output.avi 
ffmpeg -i video_input.webm video_output.flv 
ffmpeg -i audio_input.mp3 audio_output.ogg 
ffmpeg -i audio_input.wav audio_output.flac
# 同时指定多个输出后缀：这样会同时输出多个文件
ffmpeg -i audio_input.wav audio_output_1.mp3 audio_output_2.ogg 
ffmpeg -formats # 看支持的格式
# 用 -hide_banner 来省略一些程序信息。
# 用 -qscale 0 来保留原始的视频质量：
ffmpeg -i video_input.wav -qscale 0 video_output.mp4
```

#### 视频中抽取音频

为了从视频文件中抽取音频，直接加一个 **-vn** 参数就可以了
- 一些常见的比特率有: 96k, 128k, 192k, 256k, 320k (mp3也可以使用最高的比特率)。
- 其他常用参数: -ar (**采样率**: 22050, 441000, 48000), -ac (**声道数**), -f (**音频格式**, 通常会自动识别的). -ab 也可以使用 -b:a 来替代.

```sh
ffmpeg -i video.mp4 -vn audio.mp3
# 复用原有文件的比特率，使用 -ab (音频比特率)来指定编码比特率比较好
ffmpeg -i video.mp4 -vn -ab 128k audio.mp3
ffmpeg -i video.mov -vn -ar 44100 -ac 2 -b:a 128k -f mp3 audio.mp3
```

#### 视频中抽取视频（让视频静音）

用 -an 来获得**纯视频** (之前是 -vn)

```sh
ffmpeg -i video_input.mp4 -an -video_output.mp4
ffmpeg -i input.mp4 -vcodec copy -an output.mp4
# 这个 -an 标记会让所有的音频参数无效，因为最后没有音频会产生。
```

#### 视频中提取图片

这个功能很实用
- 一些幻灯片里面提取所有的图片

```sh
ffmpeg -i video.mp4 -r 1 -f image2 image-%3d.png
```

解释：
- -r 代表了帧率（一秒内导出多少张图像，默认25）
- -f 代表了输出格式 (image2 实际上上 image2 序列的意思）

最后一个参数 (输出文件) 有一个有趣的命名：
- 使用 %3d 来指示输出的图片有三位数字 (000, 001, 等等.)。
- 也可以用 %2d (两位数字) 或者 %4d (4位数字) 

Note: 同样也有将图片转变为视频/幻灯片的方式。

#### 更改视频分辨率或长宽比

用 -s 参数来缩放视频:

```sh
ffmpeg -i video_input.mov -s 1024x576 video_output.mp4
# 用 -c:a 来保证音频编码是正确的:
ffmpeg -i video_input.h264 -s 640x480 -c:a video_output.mov
# 用-aspect 来更改长宽比:
ffmpeg -i video_input.mp4 -aspect 4:3 video_output.mp4
```

#### 为音频增加封面图片

音频变成视频，全程使用一张图片（比如专辑封面）。当想往某个网站上传音频，但那个网站又仅接受视频（比如YouTube, Facebook等）的情况下会非常有用。

```sh
ffmpeg -loop 1 -i image.jpg -i audio.wav -c:v libx264 -c:a aac -strict experimental -b:a 192k -shortest output.mp4
# 只要改一下编码设置 (-c:v 是 视频编码， -c:a 是音频编码) 和文件的名称就能用了。
```

Note: 如果使用一个较新的ffmpeg版本（4.x），就可以不指定 -strict experimental

#### 为视频增加字幕

给视频增加字幕，比如一部外文电源，使用下面的命令：

```sh
ffmpeg -i video.mp4 -i subtitles.srt -c:v copy -c:a copy -preset veryfast -c:s mov_text -map 0 -map 1 output.mp4
# 可以指定自己的编码器和任何其他的音频视频参数
```

#### 压缩媒体文件

压缩文件可以极大减少文件的体积，节约存储空间，这对于文件传输尤为重要。通过ffmepg，有好几个方法来压缩文件体积。
- 文件压缩的太厉害会让文件质量显著降低。

首先，对于音频文件，可以通过降低比特率(使用 -b:a 或 -ab):

```sh
ffmpeg -i audio_input.mp3 -ab 128k audio_output.mp3
ffmpeg -i audio_input.mp3 -b:a 192k audio_output.mp3
```

再次重申，一些常用的比特率有: 
- 96k, 112k, 128k, 160k, 192k, 256k, 320k.
- 值越大，文件所需要的体积就越大。

对于视频文件，选项就多了，一个简单的方法是通过降低视频比特率 (通过 -b:v):

```sh
ffmpeg -i video_input.mp4 -b:v 1000k -bufsize 1000k video_output.mp4
# 视频的比特率和音频是不同的（一般要大得多）。
```

也可以使用 -crf 参数 (恒定质量因子). 较小的crf 意味着较大的码率。同时使用 libx264 编码器也有助于减小文件体积。这里有个例子，压缩的不错，质量也不会显著变化：

```sh
ffmpeg -i video_input.mp4 -c:v libx264 -crf 28 video_output.mp4
# crf 设置为20 到 30 是最常见的，不过您也可以尝试一些其他的值。
# 降低帧率在有些情况下也能有效（不过这往往让视频看起来很卡）:
ffmpeg -i video_input.mp4 -r 24 video_output.mp4
# -r 指示了帧率 (这里是 24)。
# 还可以通过压缩音频来降低视频文件的体积，比如设置为立体声或者降低比特率：
ffmpeg -i video_input.mp4 -c:v libx264 -ac 2 -c:a aac -strict -2 -b:a 128k -crf 28 video_output.mp4
# -strict -2 和 -ac 2 是来处理立体声部分的。
```

#### 裁剪媒体文件（基础）

想要从开头开始剪辑一部分，使用T -t 参数来指定一个时间:

```sh
ffmpeg -i input_video.mp4 -t 5 output_video.mp4 
ffmpeg -i input_audio.wav -t 00:00:05 output_audio.wav
```

这个参数对音频和视频都适用，上面两个命令做了类似的事情：保存一段5s的输出文件（文件开头开始算）。上面使用了两种不同的表示时间的方式，一个单纯的数字（描述）或者 HH:MM:SS (小时, 分钟, 秒). 第二种方式实际上指示了结束时间。

也可以通过 -ss 给出一个开始时间，-to 给出结束时间：

```sh
ffmpeg -i input_audio.mp3 -ss 00:01:14 output_audio.mp3
ffmpeg -i input_audio.wav -ss 00:00:30 -t 10 output_audio.wav 
ffmpeg -i input_video.h264 -ss 00:01:30 -to 00:01:40 output_video.h264 
ffmpeg -i input_audio.ogg -ss 5 output_audio.ogg
```

可以看到 开始时间 (-ss HH:MM:SS), 持续秒数 (-t duration), 结束时间 (-to HH:MM:SS), 和开始秒数 (-s duration)的用法.

可以在媒体文件的任何部分使用这些命令。

#### 输出YUV420原始数据

对于一下做底层编解码的人来说，有时候常要提取视频的YUV原始数据。 
- ffmpeg -i input.mp4 output.yuv

只想要抽取某一帧YUV呢？ 简单，你先用上面的方法，先抽出jpeg图片，然后把jpeg转为YUV。 比如： 你先抽取10帧图片。 

```sh
ffmpeg -i input.mp4 -ss 00:00:20 -t 10 -r 1 -q:v 2 -f image2 pic-%03d.jpeg
#结果：
# -rw-rw-r-- 1 hackett hackett    296254  7月 20 16:08 pic-001.jpeg
# -rw-rw-r-- 1 hackett hackett    300975  7月 20 16:08 pic-002.jpeg
# -rw-rw-r-- 1 hackett hackett    310130  7月 20 16:08 pic-003.jpeg
# -rw-rw-r-- 1 hackett hackett    268694  7月 20 16:08 pic-004.jpeg
# -rw-rw-r-- 1 hackett hackett    301056  7月 20 16:08 pic-005.jpeg
# 然后，随便挑一张，转为YUV: 
ffmpeg -i pic-001.jpeg -s 1440x1440 -pix_fmt yuv420p xxx3.yuv
# 如果-s参数不写，则输出大小与输入一样。当然了，YUV还有yuv422p啥的，你在-pix_fmt 换成yuv422p就行啦！
```

#### 视频添加logo

```sh
ffmpeg -i input.mp4 -i logo.png -filter_complex overlay output.mp4
```

#### 提取视频ES数据

```sh
ffmpeg –i input.mp4 –vcodec copy –an –f m4v output.h264
```

#### 视频编码格式转换

比如一个视频的编码是MPEG4，想用H264编码，咋办？

```sh
ffmpeg -i input.mp4 -vcodec h264 output.mp4
# 相反也一样
ffmpeg -i input.mp4 -vcodec mpeg4 output.mp4
```

#### 添加字幕

语法 –vf subtitles=file

```sh
ffmpeg -i jidu.mp4 -vf subtitles=rgb.srt output.mp4
```

### ffmpeg 高级用法

高级用法
1. 分割媒体文件
2. 拼接媒体文件
3. 将图片转变为视频
4. 录制屏幕
5. 录制摄像头
6. 录制声音
7. 截图

```sh
# 分割: -t 00:00:30 为界分成两个文件（音频、视频都行）, 可以指定多个分割点
ffmpeg -i video.mp4 -t 00:00:30 video_1.mp4 -ss 00:00:30 video_2.mp4
# 拼接：concat, 把join.txt里的文件合并为 output.mp4
ffmpeg -f concat -i join.txt output.mp4
# 图片→视频：image2pipe 同一种格式（png或jpg）的图片文件
cat my_photos/* | ffmpeg -f image2pipe -i - -c:v copy video.mkv
cat my_photos/* | ffmpeg -framerate 1 -f image2pipe -i - -c:v copy video.mkv # 指定帧率，framerate
cat my_photos/* | ffmpeg -framerate 0.40 -f image2pipe -i - -i audio.wav -c copy video.mkv # 加入声音 audio.wav
# 录屏：x11grab，屏幕分辨率 (-s)，按 q 或者 CTRL+C 以结束录制屏幕
ffmpeg -f x11grab -s 1920x1080 -i :0.0 output.mp4
-s $(xdpyinfo | grep dimensions | awk '{print $2;}') # 获取真实分辨率
ffmpeg -f x11grab -s $(xdpyinfo | grep dimensions | awk '{print $2;}') -i :0.0 output.mp4 # 完整写法
# 录摄像头：q 或者 CTRL+C 来结束录制。
ffmpeg -i /dev/video0 output.mkv 
# 录声音：Linux上同时是使用 ALSA 和 pulseaudio 来处理声音的。 ffmpeg 可以录制两者
# 在 pulseaudio, 必须强制指定(-f) alsa 然后指定 default 作为输入t (-i default):
ffmpeg -f alsa -i default output.mp3
ffmpeg -i /dev/video0 -f alsa -i default -c:v libx264 -c:a flac -r 30 output.mkv # 指定编码器及帧率
ffmpeg -f x11grab -s $(xdpyinfo | grep dimensions | awk '{print $2;}') -i :0.0 -i audio.wav -c:a copy output.mp4 # 提供音频文件
# 截图
ffmpeg -i input.flv -f image2 -vf fps=fps=1 out%d.png # 每隔一秒截一张图
ffmpeg -i input.flv -f image2 -vf fps=fps=1/20 out%d.png # 每隔20秒截一张图
```

过滤器 是 ffmpeg 中最为强大的功能。在ffmepg中有数不甚数的过滤器存在，可以满足各种编辑需要

ffmpeg 过滤器：
1. 视频缩放
2. 视频裁剪
3. 视频旋转
4. 音频声道重映射
5. 更改播放速度

```sh
# 过滤器基本结构
# 指定视频过滤器 (-vf, -filter:v的简写) 和 音频过滤器 (-af, -filter:a的简写)，单引号连接
ffmpeg -i input.mp4 -vf "filter=setting_1=value_1:setting_2=value_2,etc" output.mp4
ffmpeg -i input.wav -af "filter=setting_1=value_1:setting_2=value_2,etc" output.wav
# 视频缩放
ffmpeg -i input.mp4 -vf "scale=w=800:h=600" output.mp4 # 绝对大小
ffmpeg -i input.mkv -vf "scale=w=1/2*in_w:h=1/2*in_h" output.mkv # 数学运算，相对大小
# 视频裁剪：除了w和h，还需要指定裁剪原点（视频中心）
ffmpeg -i input.mp4 -vf "crop=w=1280:h=720:x=0:y=0" output.mp4 
ffmpeg -i input.mkv -vf "crop=w=400:h=400" output.mkv
ffmpeg -i input.mkv -vf "crop=w=3/4*in_w:h=3/4*in_h" output.mkv # 相对大小
# 视频旋转
ffmpeg -i input.avi -vf "rotate=90*PI/180" # 按照指定弧度顺时针旋转 90°
ffmpeg -i input.mp4 -vf "rotate=PI" # 上下颠倒
# 声道重映射
ffmpeg -i input.mp3 -af "channelmap=1-0|1-1" output.mp3 # 将右声道（1）同时映射到左（0）右（1）两个声道（左边的数字是输入，右边的数字是输出）。
# 更改音量
ffmpeg -i input.wav -af "volume=1.5" output.wav  # 音量 1.5倍
ffmpeg -i input.ogg -af "volume=0.75" output.ogg # 0.75倍
# 视频播放速度：setpts（视频播放）、atempo（音频播放）
ffmpeg -i input.mkv -vf "setpts=0.5*PTS" output.mkv # 视频加速
ffmpeg -i input.mp4 -vf "setpts=2*PTS" output,mp4 # 视频减速一半
ffmpeg -i input.wav -af "atempo=0.75" output.wav # 音频减速
ffmpeg -i input.mp3 -af "atempo=2.0,atempo=2.0" ouutput.mp3 # 音频加速
```



# 视频应用


## 抖音视频

抖音视频是一项画面+声音+文字的艺术

### 视频转化分析

流程
- 推荐：抖音视频推荐机制（阶梯）
- 观看：
  - 直接忽略：
  - 中途跳过：
  - 完整播放：
- 反馈：
  - 点赞：
  - 评论：
  - 收藏：
  - 转发：
  - 关注：
- 转化：导流
  - 关注
  - 小程序

![](https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.ws.126.net%2F2022%2F0926%2F6bd63314j00rit5vr016xd000v900xtp.jpg&thumbnail=660x2147483647&quality=80&type=jpg)

### 视频拍摄

拍摄小提示
- 01：**画面+声音+文字**
  - 抖音视频是一项画面+声音+文字的艺术，除了传统声画，大家一定要注意标题和画面文案的协调搭配。
- 02：**情绪表达**
  - 反转只是情绪表达的一种形式，你的情绪表达足够到位，足够引起共鸣，不一定要费尽心思做反转的。
- 03：结尾**引导关注**
  - 结尾时尽量做一个引导关注，对拉粉很有帮助。

发布时还可以选择定位在人群密集的地方，因为系统也会优先推荐给附近的人看，展示的概率会大一些。
新闻类的短视频适合用脚本大纲，故事性强的短视频适合用分镜头脚本，不需要剧情的短视频适合用文学脚本。
很多场景视频还要设计拍摄地址，脚本的范式

### 抖音工具

视频处理
- 脚本文案: 短视频脚本一般分为3种，**分镜头脚本**、**拍摄提纲**、以及**文学脚本**。
  - [文案范例](http://static.kancloud.cn/mhsm/dyzsfx/2381665), 
- 提取文案：提取视频链接里的文案信息，可用工具
  - 微信小程序：”轻抖”，使用[方法](http://static.kancloud.cn/mhsm/dyzsfx/2381648)
  - [媒小三](https://www.meixiaosan.com/shortvideotext.html)，PC站点
  - [享享猫去水印](https://wangzhe.smzdw.cn/page/appdownload)，支持批量提取、修改、提取音频、去水印等；
    - 【2023-5-12】收费，邮箱, video三七二一, [会员](https://h.zzrjcp.com/user/)才行
- 下载视频




# 结束