---
layout: post
title:  "目标跟踪--Obeject Tracing"
date:   2020-04-01 18:30:00
categories: 计算机视觉
tags: 计算机视觉  yolo 目标跟踪
excerpt: 计算机视觉之目标跟踪知识汇总
author: 鹤啸九天
mathjax: true
permalink: /object_track
---

* content
{:toc}

# 目标跟踪

目标跟踪是计算机视觉领域的一个重要问题，目前广泛应用在体育赛事转播、安防监控和无人机、无人车、机器人等领域。
- ![img](https://pica.zhimg.com/v2-669bcf28d4d647b6d832984adf059ac0_1440w.jpg?source=172ae18b)
- [目标跟踪综述](https://zhuanlan.zhihu.com/p/148516834)

## 目标跟踪应用

|应用领域|内容|示意|
|---|---|---|
|体育赛事|比赛转播|![](https://pic1.zhimg.com/80/v2-531de42fb6687921041aa8a8e6cd2ce8_1440w.webp)|
|无人车|车辆跟踪|![](https://pic1.zhimg.com/80/v2-deee3ca02a16a4ac0d098acb2390cfac_1440w.webp)|

## 目标跟踪分类

目标跟踪任务分类

目标跟踪可以分为以下几种任务
- 单目标跟踪 - 给定一个目标，追踪这个目标的位置。
- 多目标跟踪 - 追踪多个目标的位置
- Person Re-ID - 行人重识别，是利用计算机视觉技术判断图像或者视频序列中是否存在特定行人的技术。广泛被认为是一个图像检索的子问题。给定一个监控行人图像，检索跨设备下的该行人图像。旨在弥补固定的摄像头的视觉局限，并可与行人检测/行人跟踪技术相结合。
- MTMCT - 多目标多摄像头跟踪（Multi-target Multi-camera Tracking），跟踪多个摄像头拍摄的多个人
- 姿态跟踪 - 追踪人的姿态

按照任务计算类型又可以分为以下2类。
- 在线跟踪 - 在线跟踪需要实时处理任务，通过过去和现在帧来跟踪未来帧中物体的位置。
- 离线跟踪 - 离线跟踪是离线处理任务，可以通过过去、现在和未来的帧来推断物体的位置，因此准确率会在线跟踪高。


### 单目标跟踪(SOT)

单目标跟踪是在有**噪声**的传感器测量时间序列中确定单个目标的状态，状态包括：
- 位置Position
- 描述目标运动的**状态量**(eg：vel,heading)
- 一些其他感兴趣的**特征**(eg：shape,class)

#### Introduction of SOT

本质上单目标跟踪就是一个滤波问题。[img](https://pic1.zhimg.com/80/v2-4ab11cc071f5f3c27df98746a7b4602c_1440w.webp)
- ![img](https://pic1.zhimg.com/80/v2-4ab11cc071f5f3c27df98746a7b4602c_1440w.webp)

[单目标追踪理论（SOT发展角度）](https://zhuanlan.zhihu.com/p/488468550)

单目标追踪的任务：追踪博尔特任务, 在下[图](https://pic4.zhimg.com/80/v2-289043efa97d0e9cfd6f85414e022b47_1440w.webp)视频中
- 第一帧中框定追踪目标（不局限于类别）作为人为先验信息（如博尔特），来确定追踪的目的
- 最终在视频后续的所有帧中都能跟踪出在第一帧中框定的目标，达到长时间跟踪的目的，可能在第一帧场景变化小，但是如果切换到视频的一百帧甚至三百帧，场景变化大，此时能够根据在第一帧的认为先验性息来跟踪所有帧中乃至于不同视频中的目标是一个非常具有挑战性的任务。

#### How to realize SOT(怎么追踪)

按图索骥（找到与模板最相似的区域）
- 人脸追踪[示意](https://pic3.zhimg.com/80/v2-73b81aea9fb573fded3d8e4a70c1b64e_1440w.webp)
- ![](https://pic3.zhimg.com/80/v2-73b81aea9fb573fded3d8e4a70c1b64e_1440w.webp)

以第一帧的先验信息为主，在后续帧中只需要在画面中找出最为相似的部分即可，如图1.2人脸追踪，在第一帧框定出人脸，在后续帧中只需要在周围区域进行锁定，找出相似区域即可。再回到我们的运动员博尔特追踪任务中，图1.3中白色框就是我们的候选区域，通过计算候选框与第一帧先验信息的相似性就可以判断出是否是我们需要跟踪的目标。
- [候选框](https://pic3.zhimg.com/80/v2-b3df7797cd9a7c77a4bef288242b923a_1440w.webp)
- ![](https://pic3.zhimg.com/80/v2-b3df7797cd9a7c77a4bef288242b923a_1440w.webp)

问题：
- 把整张图都纳入跟踪范围时，首先，以第一帧的先验信息为主与后续的目标逐一对比时，后续目标的选取怎么确定？是任意选还是整张图片构建？长宽比例该怎么确定？另外，当先验目标与候选框一个一个比较会带来巨大的运算资源消耗，效率低。

按图索骥模型简单介绍
 
在16年之后兴起的深度学习的按图索骥模型如[图](https://pic1.zhimg.com/80/v2-57426bfca371c0cd9f0fa55073afeb88_1440w.webp)，首先将第一帧框定的人为先验信息（Template）通过ResNet等网络提取出视觉特征z，作为对比的模板（卷积核），在后续帧中，不再是全图找候选框，而是在上一帧的周围进行跟踪（减少运算量）， 抽取出图像x，将特征z和提取出来的图像x进行卷积操作得到Channel为1的的二维的得分图，作为相似度对比的结果，大小为17x17x1的得分图中的一个像素点代表原图中15x15得到区域。
- ![](https://pic1.zhimg.com/80/v2-57426bfca371c0cd9f0fa55073afeb88_1440w.webp)
- 按图索骥网路结构图
 
SOT可研究方向
*   构建更好的特征提取器来表达视觉区域特征
*   更好相似度匹配算法
*   更精确的边界框标注
*   长时间的目标追踪（第一帧模板是否适用于后续所有帧）

单目标追踪模型发展
- 1. More Precise BBox Annotation
  - Anchor-based (Anchor Box)
    - ![](https://pic4.zhimg.com/80/v2-d073fdc150d5f442d7139306c85e3fa7_1440w.webp)
    - 引入Anchor-based思想的SOT模型: SiamRPN, SiamCAR
  - Anchor-free
    - ![](https://pic1.zhimg.com/80/v2-43af25514bd47c05959948a6360c6920_1440w.webp)
- 2. Stronger Feature Extractor（更好的特征表征）：对于单目标追踪来说，使用更深的网络比如ResNet，性能不增反降。
  - 如果一个像素的感受野太大，填充会导致移位（分数图与目标位置不匹配）
  - 其次，Padding可能会给模板匹配带来一些偏差
  - 怎么做？
    - 裁剪掉多余的padding: 在论文《Deeper and Wider Siamese Networks for Real-Time Visual Tracking》中，作者提出裁剪掉多余padding的思想。
    - 将目标的标注向周围偏移: 当没有padding时，得分计算时，卷积操作之后得到的特征图非常抽象，如下图，矩阵中的21，映射到原图中就是矩阵后两列
- 3. More Fine-grained Matching（更细粒度的模板匹配）
  - 细粒度提升方式一——分组卷积
  - 细粒度提升方式二——transformer
- 3. Traditional Methods（传统方法）
  - Old but Strong Correlation Filter（19年之前）
  - Older Motion Model（上世纪）
    - LK Optical Flow（LP流光法）

详见：[单目标追踪理论（SOT发展角度）](https://zhuanlan.zhihu.com/p/488468550)

### 多目标跟踪(MOT)

[多目标跟踪(MOT)](https://zhuanlan.zhihu.com/p/387069216)

真实场景中，不可能仅追踪一个目标。
- 如下[图](https://pic3.zhimg.com/80/v2-6b9b0160b3b5d380f03a05814763c79e_1440w.webp), 一个典型**自动驾驶**场景示例，通过传感器可感知到行人、车、自行车等目标，运动状态可能包括静止、横穿、转弯、对向行驶等。问题已变得复杂。
- ![img](https://pic3.zhimg.com/80/v2-6b9b0160b3b5d380f03a05814763c79e_1440w.webp)

多目标跟踪是在有噪声的传感器测量时间序列中确定**多个目标**的如下特性：
- 动态目标的个数
- 每个动态目标的状态(和单目标跟踪相同)

对比SOT与MOT后发现，其处理问题多了一个**确定动态目标个数**。

多目标跟踪基于传感器的检测。
- 一般自动驾驶车上会配备一些**传感器**，比如`camera`、`radar`和`Lidar`。
- 这些传感器在车辆行驶过程中，会采集大量原始数据送入`检测`(detector)模块
  - `camera`摄像头 可获得bounding box
  - `radar`雷达 可获得极坐标下的方位以及多普勒测量
  - `Lidar`激光 可获得点云，而后将这些信号将送入多目标跟踪模块。
- 多目标跟踪模块则根据这些连续的单帧的信号以获得目标state的后验分布。如下[图](https://pic2.zhimg.com/80/v2-ba14183a099a535084fe7c35939f6b21_1440w.webp)所示。
- ![](https://pic2.zhimg.com/80/v2-ba14183a099a535084fe7c35939f6b21_1440w.webp)

一般情况下，detector处理的是**单帧**数据，而MOT需要处理**多帧**数据，有时序的。

以相机举个例子
- sensor为`camera`，detector则就是深度学习算法，输出给MOT的测量是bounding box以及吐出的深度估计。
- MOT模块则拿着这些单帧的测量进行目标跟踪
- 最后获得目标相对车体坐标系的 position(x,y) 以及 velocity(Vx,Vy)。

下[图](https://pic1.zhimg.com/80/v2-5a31fc334955fb87dc66254619b9200c_1440w.webp)椭圆表示的为不确定度。
- ![](https://pic1.zhimg.com/80/v2-5a31fc334955fb87dc66254619b9200c_1440w.webp)

#### 多目标跟踪的类型
 
由于每个目标可能产生不同数量的测量，这个对应的测量数目取决于传感器的分辨率，也取决于detector，同时也取决于跟踪对象的类型。根据每个目标对应测量的多少等标准将目标跟踪可分为以下类型：
 
① **点**目标跟踪(point object tracking)

这是最传统的多目标跟踪类型，基于“small object”的假设，即：
*   每个目标都是独立的。
*   每个目标均被建模为点，而没有任何扩展。
*   在一个时间周期内，每个目标至多产生一个对应的测量。
 
点目标跟踪的例子：
*   camera的检测
*   航天用于监视的雷达

![](https://pic3.zhimg.com/80/v2-ac9bd337ecd16aac22209c2720c60d76_1440w.webp)
 
② **扩展**目标跟踪(extended object tracking)

此跟踪类型目标一般有不止一个测量，其目标的shape一般是未知的，可动态发生变化。通过递归滤波更新可以确定目标的shape。此种目标使得跟踪系统变得复杂，非线性程度上升。注意其与CV领域的轮廓跟踪是不同的。

扩展目标跟踪的例子：
*   Lidar
*   汽车radar

![](https://pic3.zhimg.com/80/v2-97c629ff9de1c50083a6aaafe7aa2dc2_1440w.webp)
 
③ **目标群**跟踪(group object tracking)
 
几个目标被看做一个group，当然单一目标也可以看做一个group。
- ![](https://pic3.zhimg.com/80/v2-e519435a9afe2e7f6af064f491d288d6_1440w.webp)
 
④ 其他(多径，merged measurement)
 
多径问题多发生于雷达，在自动驾驶领域就是雷达被路面反射，打到了车辆的地盘造成检测的目标点不是车辆的最近点。如下图所示。
- ![](https://pic2.zhimg.com/80/v2-d5698ff5df6efc89e0dc97f3c68f5255_1440w.webp)

merged measurement问题就是如果两个车辆在自车前方并行，二者有相同速度的话，radar检测的点被合并，目标出现在二者中间，如下[图](https://pic1.zhimg.com/80/v2-55bd78c944a0dba01217faef0d76a674_1440w.webp)所示。
- ![](https://pic1.zhimg.com/80/v2-55bd78c944a0dba01217faef0d76a674_1440w.webp)

#### 多目标跟踪的挑战

第一部分的挑战如下，以下图举例能说明问题，图中扇形部分为车载传感器可观测范围：
*   FOV范围内多少个目标不知道；每个目标的state不知道。
*   目标在FOV内到处移动。
*   存在旧目标离开FOV或新目标进入FOV，涉及到目标的出现与消失，术语叫track birth与track death，需要进行航迹管理。
*   遮挡问题：某一帧一个目标把另外目标遮挡，传感器检测不到 。

![](https://pic3.zhimg.com/80/v2-51f2c9dae5b123b45ce7c158ca949286_1440w.webp)
 
下一部分的挑战就是由于传感器的缺陷导致的：
*   (1) 传感器的漏捡：
  *   在车辆行驶过程中，若前方某行人过马路，传感器漏捡，则可能出现自动驾驶的功能性fail，此时需要后面模块进行兜底，也就是MOT。
  *   漏捡产生可能原因如下：
    *   环境问题：比如poor light。
    *   目标本身特性。比如行人不是很容易被radar检测到。
    *   遮挡原因
*   (2) 传感器的虚警：
  *   在车辆行驶过程中，若前方空空如也，但传感器上报存在目标，这就可能造成车辆自动减速刹车，此时也需要后面模块进行兜底，也就是MOT。
  *   虚警产生可能原因：
    *   其他地方反射了radar。
    *   被误认为目标。
    *   环境问题。
 
最后一部分挑战就是数据关联：
- 数据关联是多目标跟踪中最重要的问题之一。说的通俗点就是，在k-1时刻感知若干个目标，在k时刻感知若干个目标，MOT模块需要把这些目标对应起来，确认哪些属于同一个目标，这其中不能关联错误，否则会引入错误信息，拉飞目标。
 
数据关联是挑战的原因：
*   首先就是因为没有先验信息，不知道哪些检测是之前有的目标，哪些是新生成的目标亦或是虚警。
*   其次就是传感器噪声影响，可能导致目标状态估计不准确，脱离算法限制，导致关联上错误目标。
*   再有就是目标彼此之间很近，也容易关联错误。试想在交通拥堵场景，车与车之间距离很近，如若传感器噪声较大，测量不准，就很容易关联错误。
 
举个例子，如下图所示，纵轴1,2,3分别对应三个时刻，灰色部分为虚警或新生成的track，同一目标已用同一种颜色标出。通过图示可以清晰看出哪些目标应该关联在一起。
- ![](https://pic4.zhimg.com/80/v2-f7de71e8e7c9d36ddb4b9c1ce04d1563_1440w.webp)
 
然而如果把颜色去掉，仅有3个时刻的测量，肉眼就不好分别了。
- ![](https://pic1.zhimg.com/80/v2-7eb9c81778848a722a0ec27712ea3070_1440w.webp)
 
尤其是对于Lidar与radar，这种目标多，虚警多的传感器，数据关联算法就变得格外重要。那有多重要呢，如下图为3个目标采用不同的数据关联算法进行跟踪，可以看出估计的位置信息(轨迹)差别较大，图一直接失败，图二则没有图三平滑。可见数据关联的重要性。
- ![](https://pic1.zhimg.com/80/v2-00765560daff98ed71b4373e41d99c14_1440w.webp)

## 数据集

- ![img](https://pic2.zhimg.com/80/v2-469a0d48774e9346242a5fa8e5bd1a39_1440w.webp)

## 目标跟踪的困难点

虽然目标追踪的应用前景非常广泛，但还是有一些问题限制了它的应用，我们看下有哪些问题呢？
- 形态变化 - 姿态变化是目标跟踪中常见的干扰问题。运动目标发生姿态变化时, 会导致它的特征以及外观模型发生改变, 容易导致跟踪失败。例如:体育比赛中的运动员、马路上的行人。
- 尺度变化 - 尺度的自适应也是目标跟踪中的关键问题。当目标尺度缩小时, 由于跟踪框不能自适应跟踪, 会将很多背景信息包含在内, 导致目标模型的更新错误:当目标尺度增大时, 由于跟踪框不能将目标完全包括在内, 跟踪框内目标信息不全, 也会导致目标模型的更新错误。因此, 实现尺度自适应跟踪是十分必要的。
- 遮挡与消失 - 目标在运动过程中可能出现被遮挡或者短暂的消失情况。当这种情况发生时, 跟踪框容易将遮挡物以及背景信息包含在跟踪框内, 会导致后续帧中的跟踪目标漂移到遮挡物上面。若目标被完全遮挡时, 由于找不到目标的对应模型, 会导致跟踪失败。
- 图像模糊 - 光照强度变化, 目标快速运动, 低分辨率等情况会导致图像模型, 尤其是在运动目标与背景相似的情况下更为明显。因此, 选择有效的特征对目标和背景进行区分非常必要。

示例
- 光照及模糊 [img](https://pic1.zhimg.com/80/v2-522e7bad45da314edb03ea3c7b26f260_1440w.webp)
  - ![](https://pic1.zhimg.com/80/v2-522e7bad45da314edb03ea3c7b26f260_1440w.webp)
- 形变及遮挡 [img](https://pic3.zhimg.com/80/v2-46f38d9ee2dd149639774ee598e4456a_1440w.webp)
  - ![](https://pic3.zhimg.com/80/v2-46f38d9ee2dd149639774ee598e4456a_1440w.webp)


## 目标跟踪算法


### 目标跟踪算法总结

目标跟踪的方法主要分为2大类，一类是**相关滤波**、一类是**深度学习**。[img](https://pic2.zhimg.com/80/v2-632a3a08c0f30f0abcdb8b06afbe346d_1440w.webp)
- ![img](https://pic2.zhimg.com/80/v2-632a3a08c0f30f0abcdb8b06afbe346d_1440w.webp)
- 相比于光流法、Kalman、Meanshift等传统算法，相关滤波类算法跟踪速度更快，深度学习类方法精度高.
- 具有多特征融合以及深度特征的追踪器在跟踪精度方面的效果更好.
- 使用强大的分类器是实现良好跟踪的基础.
- 尺度的自适应以及模型的更新机制也影响着跟踪的精度.


### 目标跟踪算法分类

目标跟踪的方法按照**模式**划分为2类。
- `生成式`模型 - 早期主要集中于**生成式**模型跟踪算法的研究, 如`光流法`、`粒子滤波`、`Meanshift`算法、`Camshift`算法等.
  - 此类方法首先建立**目标模型**或者**提取目标特征**, 在后续帧中进行**相似特征搜索**. 逐步迭代实现目标定位.
  - 明显缺点: 
    - 图像的背景信息没有得到全面的利用.
    - 目标本身的外观变化有随机性和多样性特点
  - 因此, 通过**单一数学模型**描述待跟踪目标具有很大的局限性. 具体表现为**光照变化**, **运动模糊**, **分辨率低**, **目标旋转形变**等情况, 模型的建立会受到巨大的影响, 从而影响跟踪的准确性; 模型的建立没有有效地预测机制, 当出现目标遮挡情况时, 不能够很好地解决。
- `鉴别式`模型 - 鉴别式模型将**目标模型**和**背景信息**同时考虑在内, 通过对比目标模型和背景信息的差异, 将目标模型提取出来, 从而得到当前帧中的目标位置.文献在对跟踪算法的评估中发现, 通过将背景信息引入跟踪模型, 可以很好地实现目标跟踪.因此鉴别式模型具有很大的优势.
  - 2000年以来, 人们逐渐尝试使用经典的机器学习方法训练分类器, 例如MIL、TLD、支持向量机、结构化学习、随机森林、多实例学习、度量学习. 
  - 2010年, 文献首次将通信领域的**相关滤波**方法引入到目标跟踪中.作为鉴别式方法的一种, 相关滤波无论在速度上还是准确率上, 都显示出更优越的性能. 然而, 相关滤波器用于目标跟踪是在2014年之后.
  - 自2015年以后, 随着深度学习技术的广泛应用, 人们开始将深度学习技术用于目标跟踪。

按照时间顺序，目标跟踪的方法经历了从经典算法到基于核相关滤波算法，再到基于深度学习的跟踪算法的过程。
- 经典跟踪算法
- 基于核相关滤波的跟踪算法
- 基于深度学习的跟踪算法


### 经典跟踪算法

早期的目标跟踪算法主要是根据目标建模或者对目标特征进行跟踪
- 基于**目标模型建模**的方法: 通过对目标外观模型进行建模, 然后在之后的帧中找到目标.例如, 区域匹配、特征点跟踪、基于主动轮廓的跟踪算法、光流法等.最常用的是特征匹配法, 首先提取目标特征, 然后在后续的帧中找到最相似的特征进行目标定位, 常用的特征有: SIFT特征、SURF特征、Harris角点等。
- 基于**搜索**的方法: 随着研究的深入, 人们发现基于目标模型建模的方法对整张图片进行处理, 实时性差.人们将预测算法加入跟踪中, 在预测值附近进行目标搜索, 减少了搜索的范围.常见一类的预测算法有Kalman滤波、粒子滤波方法.另一种减小搜索范围的方法是内核方法:运用最速下降法的原理, 向梯度下降方向对目标模板逐步迭代, 直到迭代到最优位置.诸如, Meanshift、Camshift算法


#### 光流法

`光流法`(Lucas-Kanade)的概念首先在1950年提出, 它是针对外观模型对视频序列中的像素进行操作.通过利用视频序列在相邻帧之间的像素关系, 寻找像素的位移变化来判断目标的运动状态, 实现对运动目标的跟踪.但是, 光流法适用的范围较小, 需要满足三种假设:图像的光照强度保持不变; 空间一致性, 即每个像素在不同帧中相邻点的位置不变, 这样便于求得最终的运动矢量; 时间连续.光流法适用于目标运动相对于帧率是缓慢的, 也就是两帧之间的目标位移不能太大.

假设条件：
- **亮度恒定**: 像素点的亮度值在不同帧中恒定不变
- **小运动**: 像素点位置在相邻帧间不会剧烈变化
- **空间一致**: 前一帧中相邻像素点在后一帧中也相邻

主要思想：
- 根据追踪目标特征点(轮廓像素点)在时间域的变化和相邻帧的关联计算每个特征点的瞬时速度和方向，进而预测后续帧特征点位置，比如上[图](https://pic2.zhimg.com/80/v2-278b11128d0c6df577e158a236981789_1440w.webp)。
- ![](https://pic2.zhimg.com/80/v2-278b11128d0c6df577e158a236981789_1440w.webp)

#### Meanshift

`Meanshift`方法是一种基于概率密度分布的跟踪方法，使目标的搜索一直沿着概率梯度上升的方向，迭代收敛到概率密度分布的局部峰值上。首先 Meanshift 会对目标进行建模，比如利用目标的颜色分布来描述目标，然后计算目标在下一帧图像上的概率分布，从而迭代得到局部最密集的区域。Meanshift 适用于目标的色彩模型和背景差异比较大的情形，早期也用于人脸跟踪。由于 Meanshift 方法的快速计算，它的很多改进方法也一直适用至今。

#### 粒子滤波

`粒子滤波`（Particle Filter）方法是一种基于粒子分布统计的方法。以跟踪为例，首先对跟踪目标进行建模，并定义一种相似度度量确定粒子与目标的匹配程度。在目标搜索的过程中，它会按照一定的分布（比如均匀分布或高斯分布）撒一些粒子，统计这些粒子的相似度，确定目标可能的位置。在这些位置上，下一帧加入更多新的粒子，确保在更大概率上跟踪上目标。Kalman Filter 常被用于描述目标的运动模型，它不对目标的特征建模，而是对目标的运动模型进行了建模，常用于估计目标在下一帧的位置。

#### 优缺点

可以看到，传统的目标跟踪算法存在两个致命**缺陷**:
- 没有将**背景信息**考虑在内, 导致在目标遮挡, 光照变化以及运动模糊等干扰下容易出现跟踪失败.
- 跟踪算法执行**速度慢**(每秒10帧左右), 无法满足实时性的要求.

### 基于核相关滤波的跟踪算法

接着，人们将通信领域的**相关滤波**(衡量两个信号的相似程度)引入到了目标跟踪中.
- 一些基于相关滤波的跟踪算法(MOSSE、CSK、KCF、BACF、SAMF)等, 也随之产生, 速度可以达到数百帧每秒, 可以广泛地应用于**实时跟踪系统**中. 
- 其中不乏一些跟踪性能优良的跟踪器, 诸如SAMF、BACF在OTB数据集和VOT2015竞赛中取得优异成绩。

#### MOSSE

本文提出的相关滤波器（Correlation Filter）通过MOSSE（Minimum Output Sum of Squared Error (MOSSE) filter）算法实现，基本思想：越是相似的两个目标相关值越大，也就是视频帧中与初始化目标越相似，得到的相应也就越大。下图所示通过对比UMACE,ASEF，MOSSE等相关滤波算法，使输出目标中心最大化。


### 基于深度学习的跟踪算法

随着深度学习方法的广泛应用, 人们开始考虑将其应用到目标跟踪中.人们开始使用**深度特征**并取得了很好的效果.之后, 人们开始考虑用深度学习建立全新的跟踪框架, 进行目标跟踪.

在大数据背景下，利用深度学习训练网络模型，得到的卷积特征输出表达能力更强。
- 在目标跟踪上，初期的应用方式是把网络学习到的**特征**，直接应用到**相关滤波**或 Struck的跟踪框架里面，从而得到更好的跟踪结果，比如前面提到的 DeepSRDCF 方法。本质上卷积输出得到的特征表达，更优于 HOG 或 CN 特征，这也是深度学习的优势之一，但同时也带来了计算量的增加。

## 目标跟踪前沿

最新方法
- 详细内容见：[Visual Tracking Paper List](https://github.com/foolwood/benchmark_results)


### Recommendations

:star2: Recommendations :star2:

- Goutam Bhat, Martin Danelljan, Luc Van Gool, Radu Timofte.<br />
  "Know Your Surroundings: Exploiting Scene Information for Object Tracking." Arxiv (2020).
  [[paper](https://arxiv.org/pdf/2003.11014v1.pdf)] 

### CVPR2020

* **MAML:** Guangting Wang, Chong Luo, Xiaoyan Sun, Zhiwei Xiong, Wenjun Zeng.<br />
  "Tracking by Instance Detection: A Meta-Learning Approach." CVPR (2020 **Oral**).
  [[paper](https://arxiv.org/pdf/2004.00830v1.pdf)]

* **Siam R-CNN:** Paul Voigtlaender, Jonathon Luiten, Philip H.S. Torr, Bastian Leibe.<br />
  "Siam R-CNN: Visual Tracking by Re-Detection." CVPR (2020).
  [[paper](https://arxiv.org/pdf/1911.12836.pdf)] 
  [[code](https://www.vision.rwth-aachen.de/page/siamrcnn)]

* **D3S:** Alan Luke?i?,?Ji?í Matas,?Matej Kristan.<br />
  "D3S – A Discriminative Single Shot Segmentation Tracker." CVPR (2020).
  [[paper](http://arxiv.org/pdf/1911.08862v2.pdf)]
  [[code](https://github.com/alanlukezic/d3s)]

* **PrDiMP:** Martin Danelljan, Luc Van Gool, Radu Timofte.<br />
  "Probabilistic Regression for Visual Tracking." CVPR (2020).
  [[paper](https://arxiv.org/pdf/2003.12565v1.pdf)]
  [[code](https://github.com/visionml/pytracking)]

* **ROAM:** Tianyu Yang, Pengfei Xu, Runbo Hu, Hua Chai, Antoni B. Chan.<br />
  "ROAM: Recurrently Optimizing Tracking Model." CVPR (2020).
  [[paper](https://arxiv.org/pdf/1907.12006v3.pdf)]

* **AutoTrack:** Yiming Li, Changhong Fu, Fangqiang Ding, Ziyuan Huang, Geng Lu.<br />
  "AutoTrack: Towards High-Performance Visual Tracking for UAV with Automatic Spatio-Temporal Regularization." CVPR (2020).
  [[paper](https://arxiv.org/pdf/2003.12949.pdf)]
  [[code](https://github.com/vision4robotics/AutoTrack)]

* **SiamBAN:** Zedu Chen, Bineng Zhong, Guorong Li, Shengping Zhang, Rongrong Ji.<br />
  "Siamese Box Adaptive Network for Visual Tracking." CVPR (2020).
  [[paper](http://arxiv.org/pdf/1911.08862v2.pdf)]
  [[code](https://github.com/hqucv/siamban)]

* **SiamAttn:** Yuechen Yu, Yilei Xiong, Weilin Huang, Matthew R. Scott. <br />
  "Deformable Siamese Attention Networks for Visual Object Tracking." CVPR (2020).
  [[paper](https://arxiv.org/pdf/2004.06711v1.pdf)]

* **CGACD:** Fei Du, Peng Liu, Wei Zhao, Xianglong Tang.<br />
  "Correlation-Guided Attention for Corner Detection Based Visual Tracking." CVPR (2020).


### AAAI 2020

- **SiamFC++:** Yinda Xu, Zeyu Wang, Zuoxin Li, Ye Yuan, Gang Yu. <br />
  "SiamFC++: Towards Robust and Accurate Visual Tracking with Target Estimation Guidelines." AAAI (2020).
  [[paper](https://arxiv.org/pdf/1911.06188v4.pdf)]
  [[code](https://github.com/MegviiDetection/video_analyst)]


### ICCV2019

* **DiMP:** Goutam Bhat, Martin Danelljan, Luc Van Gool, Radu Timofte.<br />
  "Learning Discriminative Model Prediction for Tracking." ICCV (2019 **oral**). 
  [[paper](http://openaccess.thecvf.com/content_ICCV_2019/papers/Bhat_Learning_Discriminative_Model_Prediction_for_Tracking_ICCV_2019_paper.pdf)]
  [[code](https://github.com/visionml/pytracking)]

* **GradNet:** Peixia Li, Boyu Chen, Wanli Ouyang, Dong Wang, Xiaoyun Yang, Huchuan Lu. <br />
  "GradNet: Gradient-Guided Network for Visual Object Tracking." ICCV (2019 **oral**).
  [[paper](http://openaccess.thecvf.com/content_ICCV_2019/papers/Li_GradNet_Gradient-Guided_Network_for_Visual_Object_Tracking_ICCV_2019_paper.pdf)]
  [[code](https://github.com/LPXTT/GradNet-Tensorflow)]

* **MLT:** Janghoon Choi, Junseok Kwon, Kyoung Mu Lee. <br />
  "Deep Meta Learning for Real-Time Target-Aware Visual Tracking." ICCV (2019).
  [[paper](http://openaccess.thecvf.com/content_ICCV_2019/papers/Choi_Deep_Meta_Learning_for_Real-Time_Target-Aware_Visual_Tracking_ICCV_2019_paper.pdf)]

* **SPLT:** Bin Yan, Haojie Zhao, Dong Wang, Huchuan Lu, Xiaoyun Yang <br />
  "'Skimming-Perusal' Tracking: A Framework for Real-Time and Robust Long-Term Tracking." ICCV (2019).
  [[paper](http://openaccess.thecvf.com/content_ICCV_2019/papers/Yan_Skimming-Perusal_Tracking_A_Framework_for_Real-Time_and_Robust_Long-Term_Tracking_ICCV_2019_paper.pdf)]
  [[code](https://github.com/iiau-tracker/SPLT)]

* **ARCF:** Ziyuan Huang, Changhong Fu, Yiming Li, Fuling Lin, Peng Lu. <br />
  "Learning Aberrance Repressed Correlation Filters for Real-Time UAV Tracking." ICCV (2019).
  [[paper](http://openaccess.thecvf.com/content_ICCV_2019/papers/Huang_Learning_Aberrance_Repressed_Correlation_Filters_for_Real-Time_UAV_Tracking_ICCV_2019_paper.pdf)]
  [[code](https://github.com/vision4robotics/ARCF-tracker)]

* Lianghua Huang, Xin Zhao, Kaiqi Huang. <br />
  "Bridging the Gap Between Detection and Tracking: A Unified Approach." ICCV (2019).
  [[paper](http://openaccess.thecvf.com/content_ICCV_2019/papers/Huang_Bridging_the_Gap_Between_Detection_and_Tracking_A_Unified_Approach_ICCV_2019_paper.pdf)]

* **UpdateNet:** Lichao Zhang, Abel Gonzalez-Garcia, Joost van de Weijer, Martin Danelljan, Fahad Shahbaz Khan. <br />
  "Learning the Model Update for Siamese Trackers." ICCV (2019).
  [[paper](http://openaccess.thecvf.com/content_ICCV_2019/papers/Zhang_Learning_the_Model_Update_for_Siamese_Trackers_ICCV_2019_paper.pdf)]
  [[code](https://github.com/zhanglichao/updatenet)]

* **PAT:** Rey Reza Wiyatno, Anqi Xu. <br />
  "Physical Adversarial Textures That Fool Visual Object Tracking." ICCV (2019).
  [[paper](http://openaccess.thecvf.com/content_ICCV_2019/papers/Wiyatno_Physical_Adversarial_Textures_That_Fool_Visual_Object_Tracking_ICCV_2019_paper.pdf)]

* **GFS-DCF:** Tianyang Xu, Zhen-Hua Feng, Xiao-Jun Wu, Josef Kittler. <br />
  "Joint Group Feature Selection and Discriminative Filter Learning for Robust Visual Object Tracking." ICCV (2019).
  [[paper](http://openaccess.thecvf.com/content_ICCV_2019/papers/Xu_Joint_Group_Feature_Selection_and_Discriminative_Filter_Learning_for_Robust_ICCV_2019_paper.pdf)]
  [[code](https://github.com/XU-TIANYANG/GFS-DCF)]

* **CDTB:** Alan Luke?i?, Ugur Kart, Jani K?pyl?, Ahmed Durmush, Joni-Kristian K?m?r?inen, Ji?í Matas, Matej Kristan. <br />

  "CDTB: A Color and Depth Visual Object Tracking Dataset and Benchmark." ICCV (2019).
  [[paper](http://openaccess.thecvf.com/content_ICCV_2019/papers/Lukezic_CDTB_A_Color_and_Depth_Visual_Object_Tracking_Dataset_and_ICCV_2019_paper.pdf)]

* **VOT2019:** Kristan, Matej, et al.<br />
  "The Seventh Visual Object Tracking VOT2019 Challenge Results." ICCV workshops (2019).
  [[paper](http://openaccess.thecvf.com/content_ICCVW_2019/papers/VOT/Kristan_The_Seventh_Visual_Object_Tracking_VOT2019_Challenge_Results_ICCVW_2019_paper.pdf)]


### CVPR2019

* **SiamMask:** Qiang Wang, Li Zhang, Luca Bertinetto, Weiming Hu, Philip H.S. Torr.<br />
  "Fast Online Object Tracking and Segmentation: A Unifying Approach." CVPR (2019). 
  [[paper](https://arxiv.org/pdf/1812.05050.pdf)]
  [[project](http://www.robots.ox.ac.uk/~qwang/SiamMask/)]
  [[code](https://github.com/foolwood/SiamMask)]

* **SiamRPN++:** Bo Li, Wei Wu, Qiang Wang, Fangyi Zhang, Junliang Xing, Junjie Yan.<br />
  "SiamRPN++: Evolution of Siamese Visual Tracking with Very Deep Networks." CVPR (2019 **oral**). 
  [[paper](http://openaccess.thecvf.com/content_CVPR_2019/papers/Li_SiamRPN_Evolution_of_Siamese_Visual_Tracking_With_Very_Deep_Networks_CVPR_2019_paper.pdf)]
  [[project](http://bo-li.info/SiamRPN++/)]

* **ATOM:** Martin Danelljan, Goutam Bhat, Fahad Shahbaz Khan, Michael Felsberg. <br />
  "ATOM: Accurate Tracking by Overlap Maximization." CVPR (2019 **oral**). 
  [[paper](http://openaccess.thecvf.com/content_CVPR_2019/papers/Danelljan_ATOM_Accurate_Tracking_by_Overlap_Maximization_CVPR_2019_paper.pdf)]
  [[code](https://github.com/visionml/pytracking)]

* **SiamDW:** Zhipeng Zhang, Houwen Peng.<br />
  "Deeper and Wider Siamese Networks for Real-Time Visual Tracking." CVPR (2019 **oral**). 
  [[paper](http://openaccess.thecvf.com/content_CVPR_2019/papers/Zhang_Deeper_and_Wider_Siamese_Networks_for_Real-Time_Visual_Tracking_CVPR_2019_paper.pdf)]
  [[code](https://github.com/researchmm/SiamDW)]

* **GCT:** Junyu Gao, Tianzhu Zhang, Changsheng Xu.<br />
  "Graph Convolutional Tracking." CVPR (2019 **oral**).
  [[paper](http://openaccess.thecvf.com/content_CVPR_2019/papers/Gao_Graph_Convolutional_Tracking_CVPR_2019_paper.pdf)]
  [[code](https://github.com/researchmm/SiamDW)]

* **ASRCF:** Kenan Dai, Dong Wang, Huchuan Lu, Chong Sun, Jianhua Li. <br />
  "Visual Tracking via Adaptive Spatially-Regularized Correlation Filters." CVPR (2019 **oral**).
  [[paper](http://openaccess.thecvf.com/content_CVPR_2019/papers/Dai_Visual_Tracking_via_Adaptive_Spatially-Regularized_Correlation_Filters_CVPR_2019_paper.pdf)]
  [[code](https://github.com/Daikenan/ASRCF)]

* **UDT:** Ning Wang, Yibing Song, Chao Ma, Wengang Zhou, Wei Liu, Houqiang Li.<br />
  "Unsupervised Deep Tracking." CVPR (2019). 
  [[paper](https://arxiv.org/pdf/1904.01828.pdf)]
  [[code](https://github.com/594422814/UDT)]

* **TADT:** Xin Li, Chao Ma, Baoyuan Wu, Zhenyu He, Ming-Hsuan Yang.<br />
  "Target-Aware Deep Tracking." CVPR (2019). 
  [[paper](https://arxiv.org/pdf/1904.01772.pdf)]
  [[project](https://xinli-zn.github.io/TADT-project-page/)]
  [[code](https://github.com/XinLi-zn/TADT)]

* **C-RPN:** Heng Fan, Haibin Ling.<br />
  "Siamese Cascaded Region Proposal Networks for Real-Time Visual Tracking." CVPR (2019). 
  [[paper](http://openaccess.thecvf.com/content_CVPR_2019/papers/Fan_Siamese_Cascaded_Region_Proposal_Networks_for_Real-Time_Visual_Tracking_CVPR_2019_paper.pdf)]

* **SPM:** Guangting Wang, Chong Luo, Zhiwei Xiong, Wenjun Zeng.<br />
  "SPM-Tracker: Series-Parallel Matching for Real-Time Visual Object Tracking." CVPR (2019). 
  [[paper](http://openaccess.thecvf.com/content_CVPR_2019/papers/Wang_SPM-Tracker_Series-Parallel_Matching_for_Real-Time_Visual_Object_Tracking_CVPR_2019_paper.pdf)]

* **OTR:** Ugur Kart, Alan Lukezic, Matej Kristan, Joni-Kristian Kamarainen, Jiri Matas. <br />
  "Object Tracking by Reconstruction with View-Specific Discriminative Correlation Filters." CVPR (2019). 
  [[paper](http://openaccess.thecvf.com/content_CVPR_2019/papers/Kart_Object_Tracking_by_Reconstruction_With_View-Specific_Discriminative_Correlation_Filters_CVPR_2019_paper.pdf)]
  [[code](https://github.com/ugurkart/OTR)]

* **RPCF:** Yuxuan Sun, Chong Sun, Dong Wang, Huchuan Lu, You He. <br />
  "ROI Pooled Correlation Filters for Visual Tracking." CVPR (2019).
  [[paper](http://openaccess.thecvf.com/content_CVPR_2019/papers/Sun_ROI_Pooled_Correlation_Filters_for_Visual_Tracking_CVPR_2019_paper.pdf)]

* **LaSOT:** Heng Fan, Liting Lin, Fan Yang, Peng Chu, Ge Deng, Sijia Yu, Hexin Bai, Yong Xu, Chunyuan Liao, Haibin Ling.<br />
  "LaSOT: A High-quality Benchmark for Large-scale Single Object Tracking." CVPR (2019). 
  [[paper](https://arxiv.org/pdf/1809.07845.pdf)]
  [[project](https://cis.temple.edu/lasot/)]

### AAAI2019

* **LDES:** Yang Li, Jianke Zhu, Steven C.H. Hoi, Wenjie Song, Zhefeng Wang, Hantang Liu.<br />
  "Robust Estimation of Similarity Transformation for Visual Object Tracking." AAAI (2019). 
  [[paper](https://arxiv.org/pdf/1712.05231.pdf)]
  [[code](https://github.com/ihpdep/LDES)] 


## 目标跟踪实践



### 单目标跟踪

[opencv实现单目标跟踪](https://blog.csdn.net/LuohenYJ/article/details/89029816)

通常在目标跟踪有以下方法：
- 1）密集光流：这些算法有助于估计视频帧中每个像素的运动情况。
- 2）稀疏光流：这些算法，如Kanade-Lucas-Tomashi（KLT）特征跟踪器，跟踪图像中几个特征点的位置。
- 3）卡尔曼滤波：一种非常流行的信号处理算法，用于根据先前的运动信息预测运动物体的位置。该算法的早期应用之一是导弹制导！还提到这里，阿波罗11号登月舱的降落到月球车载计算机有一个卡尔曼滤波器。Engineers Look to Kalman Filtering for Guidance。
- 4）均值偏移(Meanshift)和Camshift(Meanshift的改进，连续自适应的MeanShift算法)：这些是用于定位密度函数的最大值的算法。它们也用于跟踪。
- 5）单目标跟踪算法：在此类跟踪器中，第一帧使用矩形表示我们要跟踪的对象的位置。然后使用跟踪算法在后续帧中跟踪对象。在大多数实际应用中，这些跟踪器与目标检测算法结合使用。
- 6）多目标跟踪算法：在我们有快速对象检测器的情况下，检测每个帧中的多个对象然后运行跟踪查找算法来识别一个帧中的哪个矩形对应于下一帧中的矩形是很有效的。

OpenCV 3中提供的8种不同的跟踪器BOOSTING，MIL，KCF，TLD，MEDIANFLOW，GOTURN，MOSSE和CSRT。


Python版

Python稍微很简单，先卸载安装的Opencv，然后直接pip/pip3安装contrib库：

```py
pip uninstall opencv-python
pip install opencv-contrib-python
```

目标跟踪代码

```py
import cv2
import sys
 
 
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[4]
 
 
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()
    if tracker_type == "MOSSE":
    tracker = cv2.TrackerMOSSE_create()
    # Read video
    video = cv2.VideoCapture("video/chaplin.mp4")
 
    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)
 
    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)
 
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
```

C++版

```c++
// Opencv_Tracker.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
 
#include "pch.h"
#include <opencv2/opencv.hpp>
#include <opencv2/tracking.hpp>
#include <opencv2/core/ocl.hpp>
 
using namespace cv;
using namespace std;
 
int main()
{
	//跟踪算法类型
	string trackerTypes[7] = { "BOOSTING", "MIL", "KCF", "TLD","MEDIANFLOW", "MOSSE", "CSRT" };
 
	// Create a tracker 创建跟踪器
	string trackerType = trackerTypes[5];
 
	Ptr<Tracker> tracker;
 
	if (trackerType == "BOOSTING")
		tracker = TrackerBoosting::create();
	if (trackerType == "MIL")
		tracker = TrackerMIL::create();
	if (trackerType == "KCF")
		tracker = TrackerKCF::create();
	if (trackerType == "TLD")
		tracker = TrackerTLD::create();
	if (trackerType == "MEDIANFLOW")
		tracker = TrackerMedianFlow::create();
	if (trackerType == "MOSSE")
		tracker = TrackerMOSSE::create();
	if (trackerType == "CSRT")
		tracker = TrackerCSRT::create();
 
	// Read video 读视频
	VideoCapture video("video/chaplin.mp4");
 
	// Exit if video is not opened 如果没有视频文件
	if (!video.isOpened())
	{
		cout << "Could not read video file" << endl;
		return 1;
	}
 
	// Read first frame 读图
	Mat frame;
	bool ok = video.read(frame);
 
	// Define initial boundibg box 初始检测框
	Rect2d bbox(287, 23, 86, 320);
 
	// Uncomment the line below to select a different bounding box 手动在图像上画矩形框
	//bbox = selectROI(frame, false);
 
	// Display bounding box 展示画的2边缘框
	rectangle(frame, bbox, Scalar(255, 0, 0), 2, 1);
	imshow("Tracking", frame);
 
	//跟踪器初始化
	tracker->init(frame, bbox);
 
	while (video.read(frame))
	{
		// Start timer 开始计时
		double timer = (double)getTickCount();
 
		// Update the tracking result 跟新跟踪器算法
		bool ok = tracker->update(frame, bbox);
 
		// Calculate Frames per second (FPS) 计算FPS
		float fps = getTickFrequency() / ((double)getTickCount() - timer);
 
		if (ok)
		{
			// Tracking success : Draw the tracked object 如果跟踪到目标画框
			rectangle(frame, bbox, Scalar(255, 0, 0), 2, 1);
		}
		else
		{
			// Tracking failure detected. 没有就输出跟踪失败
			putText(frame, "Tracking failure detected", Point(100, 80), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(0, 0, 255), 2);
		}
 
		// Display tracker type on frame 展示检测算法类型
		putText(frame, trackerType + " Tracker", Point(100, 20), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(50, 170, 50), 2);
 
		// Display FPS on frame 表示FPS
		putText(frame, "FPS : " + to_string(int(fps)), Point(100, 50), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(50, 170, 50), 2);
 
		// Display frame.
		imshow("Tracking", frame);
 
		// Exit if ESC pressed.
		int k = waitKey(1);
		if (k == 27)
		{
			break;
		}
	}
	return 0;
}
```

### 工具


#### CoTracker

【2024-10-4】CoTracker：同时准确跟踪视频中的多个点  
- 代码：CoTracker 同时准确跟踪视频中的**多个点**  
- 主页：[CoTracker](https://co-tracker.github.io/)


#### motrackers

【2025-4-27】
- [multi-object-tracker](https://github.com/adipandas/multi-object-tracker)
- 文档 [multi-object-tracker](https://adipandas.github.io/multi-object-tracker/)

```sh
pip install motrackers
```


# 结束