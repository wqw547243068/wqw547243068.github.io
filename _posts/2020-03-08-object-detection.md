---
layout: post
title:  "目标检测及跟踪--Obeject Detection&Tracing"
date:   2020-03-08 18:30:00
categories: 计算机视觉
tags: 深度学习 计算机视觉 GAN  yolo cv 卡尔曼 滤波器 目标跟踪 大模型
excerpt: 计算机视觉之目标检测知识汇总
author: 鹤啸九天
mathjax: true
permalink: /object
---

* content
{:toc}

# 目标检测


## 资讯

【2023-10-27】[大模型时代目标检测任务会走向何方？](https://zhuanlan.zhihu.com/p/663703934)

经典目标检测一般指**闭集固定类别**检测。新类型
- `Open Set`/`Open World`/`OOD` 
  - 检测任何前景物体但有些不需要预测类别，unknown 标记
  - ![](https://pic4.zhimg.com/80/v2-41515a67ade3d015efa4d1bcab66d12b_1440w.webp)
- `Open Vocabulary`
  - 开放词汇目标检测：给定**任意词汇**都可以检测出来
  - 开放集任务，相比 open set，识别训练集类别外的新类别
  - 这类模型需要接入**文本**作为一个模态输入。训练集和测试集的类别不能重复，但图片重复可以重复
  - OVD 任务更加贴合实际应用，文本的描述不会有很大限制，同一个物体你可以采用多种词汇描述都可以检测出来
  - ![](https://pic2.zhimg.com/80/v2-0ffba274563449f765fb5a273fdb8f55_1440w.webp)
- `Phrase Grounding`, 也做 `phrase localization`。
  - 给定名词短语，输出对应的单个或多个物体检测框。
  - Phrase Grounding 任务包括 OVD 任务。
  - 常见的评估数据集是 Flickr30k Entities
  - 如果是输入一句话，那么就是定位这句话中包括的所有名词短语。在 GLIP 得到了深入的研究。
  - ![](https://pic3.zhimg.com/80/v2-fc03e8448457bcfc69efcc5d85bd8252_1440w.webp)
  - ![](https://pic3.zhimg.com/80/v2-1d083d84a3aa5a01b36317f69813ab0e_1440w.webp)
- `Referring Expression Comprehension` 简称 `REC`, 也称为 visual grounding。
  - 给定图片和一句话，输出对应的物体坐标，通常就是单个检测框。
  - 常用的是 RefCOCO/RefCOCO+/RefCOCOg 三个数据集。是相对比较简单的数据集。这个任务侧重理解。
  - ![](https://pic4.zhimg.com/80/v2-8b94f4bc068210b138befeb57a882d37_1440w.webp)
- `Description Object Detection`
  - 描述性目标检测也称 广义 Referring Expression Comprehension。
  - 为何叫做广义，目前常用的 REC 问题：当前数据集只指代1个物体、没有负样本、正向描述
  - Described Object Detection 论文提出新的数据集，命名为 `DOD`。类似还有 gRefCOCO
  - ![](https://pic3.zhimg.com/80/v2-88a3e394105bac8c7e3d478f13618a06_1440w.webp)
- `Caption with Grounding`
  - 给定**图片**，要求模型输出**图片描述**，同时对于其中的短语都要给出对应的 bbox
  - 像 Phrase Grounding 的**反向**过程。
  - 这个任务可以方便将输出的名称和 bbox 联系起来，方便后续任务的进行。
  - ![](https://pic1.zhimg.com/80/v2-3589f1f8c155f4dcffba91b7e179f820_1440w.webp)
- `Reasoning Intention-Oriented Object Detection`
  - 意图导向的目标检测，和之前的 DetGPT 提出的推理式检测非常类似。
  - DetGPT 中的推理式检测含义是：给定文本描述，模型要能够进行推理，得到用户真实意图。
  - 示例： **我想喝冷饮**，LLM 会自动进行推理解析输出 **冰箱** 这个单词，从而可以通过 Grounding 目标检测算法把冰箱检测出来。模型具备推理功能。
  - ![](https://pic3.zhimg.com/80/v2-b0269147b3f14fe79f4b2cc8a20d54b2_1440w.webp)
  - 论文 [RIO: A Benchmark for Reasoning Intention-Oriented Objects in Open Environments]()
- `基于区域输入的理解和 Grounding`
  - 非常宽泛的任务，表示不仅可以输入**图文**模态，还可以输入其他任意模态，然后进行理解或者定位相关任务。
  - 最经典的任务是 Referring expression generation：给定图片和单个区域，对该区域进行描述。常用的评估数据集是 RefCOCOg
  - 现在也有很多新的做法，典型的如 Shikra 里面提到的 Referential dialogue，包括 REC，REG，PointQA，Image Caption 以及 VQA 5 个任务
  - ![](https://pic1.zhimg.com/80/v2-6351293bbd527088692d88756d708788_1440w.webp)



## 背景

计算机视觉领域的典型任务就是目标检测

- 目标检测最新趋势：[deep_learning_object_detection](https://github.com/hoya012/deep_learning_object_detection)
- 发展历史：
- ![](https://github.com/hoya012/deep_learning_object_detection/raw/master/assets/deep_learning_object_detection_history.PNG)
![](https://img-blog.csdnimg.cn/20200223212931503.png)
- 【2020-4-23】技术总结
- ![](https://pic1.zhimg.com/80/v2-0c98fb30a9e589fa164d99c50e6ca711_1440w.jpg)

## 类型

- **目标检测**（Object Detection），在计算机视觉领域的任务就是给定一张图片，将图片中的物体识别并且框定出来。
- object detection的算法主要可以分为两大类：**two-stage** detector和**one-stage** detector。
  - One-Stage检测算法是指类似Faster RCNN，RFCN这样需要region proposal的检测算法，这类算法可以达到很高的准确率，但是速度较慢。虽然可以通过减少proposal的数量或降低输入图像的分辨率等方式达到提速，但是速度并没有质的提升。
  - Two-Stage检测算法是指类似YOLO，SSD这样不需要region proposal，直接回归的检测算法，这类算法速度很快，但是准确率不如前者。
 - PS：Multi-Stage检测算法的Selective Search、Feature extraction、Location regression、Class SVM等环节都是分开训练，操作繁杂而且效果不好，所以这里默认忽视。
 - focal loss的出发点也是希望one-stage detector可以达到two-stage detector的准确率，同时不影响原有的速度。
 - 参考：[目标检测算法综述](https://blog.csdn.net/liuxinnanshou/article/details/104467821)
- One-Stage检测算法的初衷是提升速度，而Two-Stage中比较耗时就是proposal建议区域生成，所以索性One-Stage方法就是直接从图像建议区域提取特征进行分类和定位回归。
   - 图像建议区域是直接从backbone的特征层中进行密集选取，所以一些one-stage算法也称为密集检测器。同时可以看出，one-stage主要处理的问题是：特征提取、分类和定位回归。即关键点全部在特征提取这一块上。
  ![](https://img-blog.csdnimg.cn/202002232128149.png)
- Two-Stage检测算法可以通过ROI pooling layer（以Faster R-CNN为例）进行结构划分，前部分提出可能存在目标的区域，后部分即目标分类和定位回归。结构如下
   - two-stage主要处理的几个问题是：backbone进行特征提取、proposal建议区域的生成、分类和定位回归。
![](https://img-blog.csdnimg.cn/2020022321273620.png)


# 算法综述

- 【2018-4-7】[从RCNN到SSD，这应该是最全的一份目标检测算法盘点](https://www.jiqizhixin.com/articles/2018-04-27)

目标检测进行了整体回顾
- 第一部分从 RCNN 开始介绍基于候选区域的目标检测器，包括 Fast R-CNN、Faster R-CNN 和 FPN 等。
- 第二部分则重点讨论了包括 YOLO、SSD 和 RetinaNet 等在内的单次检测器，它们都是目前最为优秀的方法。

排行榜
- huggingface 榜单：[object_detection_leaderboard](https://huggingface.co/spaces/rafaelpadilla/object_detection_leaderboard)

## 数据集

大白智能数据集[汇总](https://www.jiangdabai.com/dcat/%e7%9b%ae%e6%a0%87%e8%bf%bd%e8%b8%aa)

## 基于候选区域的目标检测器

### 滑动窗口检测器

自从 AlexNet 获得 ILSVRC 2012 挑战赛冠军后，用 CNN 进行分类成为主流。一种用于目标检测的暴力方法是从左到右、从上到下滑动窗口，利用分类识别目标。为了在不同观察距离处检测不同的目标类型，我们使用不同大小和宽高比的窗口。
- ![](https://image.jiqizhixin.com/uploads/editor/56fda0e6-5626-4a49-b2e5-41cd518914a2/1524810326548.jpg)

_滑动窗口（从右到左，从上到下）_

我们根据滑动窗口从图像中剪切图像块。由于很多分类器只取固定大小的图像，因此这些图像块是经过变形转换的。但是，这不影响分类准确率，因为分类器可以处理变形后的图像。
- ![](https://image.jiqizhixin.com/uploads/editor/877ad5ad-acab-47ea-8b03-f25f31503dec/1524810326235.jpg)

_将图像变形转换成固定大小的图像_

变形图像块被输入 CNN 分类器中，提取出 4096 个特征。之后，我们使用 SVM 分类器识别类别和该边界框的另一个线性回归器。
- ![](https://image.jiqizhixin.com/uploads/editor/def0df24-c295-45f0-b6f0-83c86524ec34/1524810326396.jpg)

_滑动窗口检测器的系统工作流程图。_
 
下面是伪代码。我们创建很多窗口来检测不同位置的不同目标。要提升性能，一个显而易见的办法就是减少窗口数量。
 
```python
for window in windows
    patch = get_patch(image, window)
    results = detector(patch)
```
 
### 选择性搜索
 
我们不使用暴力方法，而是用**候选区域**方法（region proposal method）创建目标检测的感兴趣区域（ROI）。在选择性搜索（selective search，SS）中，我们首先将每个像素作为一组。然后，计算每一组的纹理，并将两个最接近的组结合起来。但是为了避免单个区域吞噬其他区域，我们首先对较小的组进行分组。我们继续合并区域，直到所有区域都结合在一起。下图第一行展示了如何使区域增长，第二行中的蓝色矩形代表合并过程中所有可能的 ROI。
 
![](https://image.jiqizhixin.com/uploads/editor/75aef501-16d3-47f4-8403-3cc4fe2fa5d5/1524810327069.jpg)
 
_图源：van de Sande et al. ICCV'11_
 
#### R-CNN
 
R-CNN 利用候选区域方法创建了约 2000 个 ROI。这些区域被转换为固定大小的图像，并分别馈送到卷积神经网络中。该网络架构后面会跟几个全连接层，以实现目标分类并提炼边界框。
 
![](https://image.jiqizhixin.com/uploads/editor/b4d6c68f-eb44-4c43-bd4e-9101aec1d61e/1524810326762.jpg)
 
_使用候选区域、CNN、仿射层来定位目标。_
 
以下是 R-CNN 整个系统的流程图：
 
![](https://image.jiqizhixin.com/uploads/editor/9d20688e-8dad-4586-a931-92c34cb5c56a/1524810326853.jpg)
 
通过使用更少且更高质量的 ROI，R-CNN 要比滑动窗口方法更快速、更准确。
 
```python
ROIs = region_proposal(image)
for ROI in ROIs
    patch = get_patch(image, ROI)
    results = detector(patch)
```
 
### 边界框回归器
 
候选区域方法有非常高的计算复杂度。为了加速这个过程，我们通常会使用计算量较少的候选区域选择方法构建 ROI，并在后面使用线性回归器（使用全连接层）进一步提炼边界框。
 
![](https://image.jiqizhixin.com/uploads/editor/531fe028-4fe9-4f75-8493-a68485bad3a7/1524810327599.jpg)
 
_使用回归方法将蓝色的原始边界框提炼为红色的。_
 
#### Fast R-CNN
 
R-CNN 需要非常多的候选区域以提升准确度，但其实有很多区域是彼此重叠的，因此 R-CNN 的训练和推断速度非常慢。如果我们有 2000 个候选区域，且每一个都需要独立地馈送到 CNN 中，那么对于不同的 ROI，我们需要重复提取 2000 次特征。
 
此外，CNN 中的特征图以一种密集的方式表征空间特征，那么我们能直接使用特征图代替原图来检测目标吗？
 
![](https://image.jiqizhixin.com/uploads/editor/89dfd079-2c83-4edd-8cb5-e09627fa1ada/1524810327749.jpg)
 
![](https://image.jiqizhixin.com/uploads/editor/71a18c9a-364d-4569-95b5-373850deabfc/1524810327979.jpg)
 
_直接利用特征图计算 ROI。_
 
Fast R-CNN 使用特征提取器（CNN）先提取整个图像的特征，而不是从头开始对每个图像块提取多次。然后，我们可以将创建候选区域的方法直接应用到提取到的特征图上。例如，Fast R-CNN 选择了 VGG16 中的卷积层 conv5 来生成 ROI，这些关注区域随后会结合对应的特征图以裁剪为特征图块，并用于目标检测任务中。我们使用 ROI 池化将特征图块转换为固定的大小，并馈送到全连接层进行分类和定位。因为 Fast-RCNN 不会重复提取特征，因此它能显著地减少处理时间。
 
![](https://image.jiqizhixin.com/uploads/editor/22c8abb3-9c67-4c5d-a613-3bebb3d7374f/1524810328074.jpg)
 
_将候选区域直接应用于特征图，并使用 ROI 池化将其转化为固定大小的特征图块。_
 
以下是 Fast R-CNN 的流程图：
 
![](https://image.jiqizhixin.com/uploads/editor/d1e3b8d5-a71b-4f44-8856-9414e98b12fc/1524810328159.jpg)
 
在下面的伪代码中，计算量巨大的特征提取过程从 For 循环中移出来了，因此速度得到显著提升。Fast R-CNN 的训练速度是 R-CNN 的 10 倍，推断速度是后者的 150 倍。
 
```python
feature_maps = process(image)
ROIs = region_proposal(feature_maps)
for ROI in ROIs
    patch = roi_pooling(feature_maps, ROI)
    results = detector2(patch)
```
 
Fast R-CNN 最重要的一点就是包含特征提取器、分类器和边界框回归器在内的整个网络能通过多任务损失函数进行端到端的训练，这种多任务损失即结合了分类损失和定位损失的方法，大大提升了模型准确度。
 
### ROI 池化
 
因为 Fast R-CNN 使用全连接层，所以我们应用 ROI 池化将不同大小的 ROI 转换为固定大小。

为简洁起见，我们先将 8×8 特征图转换为预定义的 2×2 大小。
*   下图左上角：特征图。
*   右上角：将 ROI（蓝色区域）与特征图重叠。
*   左下角：将 ROI 拆分为目标维度。例如，对于 2×2 目标，我们将 ROI 分割为 4 个大小相似或相等的部分。
*   右下角：找到每个部分的最大值，得到变换后的特征图。
 
![](https://image.jiqizhixin.com/uploads/editor/5df513df-c595-4383-89ba-22bbaa57b3a4/1524810328239.jpg)
 
_输入特征图（左上），输出特征图（右下），ROI (右上，蓝色框)。_
 
按上述步骤得到一个 2×2 的特征图块，可以馈送至分类器和边界框回归器中。
 
### Faster R-CNN
 
Fast R-CNN 依赖于外部候选区域方法，如选择性搜索。但这些算法在 CPU 上运行且速度很慢。在测试中，Fast R-CNN 需要 2.3 秒来进行预测，其中 2 秒用于生成 2000 个 ROI。
 
```python
feature_maps = process(image)
ROIs = region_proposal(feature_maps)         # Expensive!
for ROI in ROIs
    patch = roi_pooling(feature_maps, ROI)
    results = detector2(patch)
```
 
Faster R-CNN 采用与 Fast R-CNN 相同的设计，只是它用内部深层网络代替了候选区域方法。新的候选区域网络（RPN）在生成 ROI 时效率更高，并且以每幅图像 10 毫秒的速度运行。
 
![](https://image.jiqizhixin.com/uploads/editor/20725eb0-4f5b-4e59-8349-2ab85171c267/1524810328304.jpg)
 
_Faster R-CNN 的流程图与 Fast R-CNN 相同。_
 
![](https://image.jiqizhixin.com/uploads/editor/64f78e7b-b530-4623-b86f-cbe126fc4ec0/1524810328439.jpg)
 
_外部候选区域方法代替了内部深层网络。_
 
### 候选区域网络
 
候选区域网络（RPN）将第一个卷积网络的输出特征图作为输入。它在特征图上滑动一个 3×3 的卷积核，以使用卷积网络（如下所示的 ZF 网络）构建与类别无关的候选区域。其他深度网络（如 VGG 或 ResNet）可用于更全面的特征提取，但这需要以速度为代价。ZF 网络最后会输出 256 个值，它们将馈送到两个独立的全连接层，以预测边界框和两个 objectness 分数，这两个 objectness 分数度量了边界框是否包含目标。我们其实可以使用回归器计算单个 objectness 分数，但为简洁起见，Faster R-CNN 使用只有两个类别的分类器：即带有目标的类别和不带有目标的类别。
 
![](https://image.jiqizhixin.com/uploads/editor/2f1780b3-e2df-4819-90a3-26ebc491fdc1/1524810328499.jpg)
 
对于特征图中的每一个位置，RPN 会做 k 次预测。因此，RPN 将输出 4×k 个坐标和每个位置上 2×k 个得分。下图展示了 8×8 的特征图，且有一个 3×3 的卷积核执行运算，它最后输出 8×8×3 个 ROI（其中 k=3）。下图（右）展示了单个位置的 3 个候选区域。
 
![](https://image.jiqizhixin.com/uploads/editor/3e80aa19-4f58-4e20-adff-9579aeb8a61b/1524810332097.jpg)
 
此处有 3 种猜想，稍后我们将予以完善。由于只需要一个正确猜想，因此我们最初的猜想最好涵盖不同的形状和大小。因此，Faster R-CNN 不会创建随机边界框。相反，它会预测一些与左上角名为「锚点」的参考框相关的偏移量（如𝛿x、𝛿y）。我们限制这些偏移量的值，因此我们的猜想仍然类似于锚点。
 
![](https://image.jiqizhixin.com/uploads/editor/9d9653ea-fbdc-4c08-8992-6d8466100395/1524810332177.jpg)
 
要对每个位置进行 k 个预测，我们需要以每个位置为中心的 k 个锚点。每个预测与特定锚点相关联，但不同位置共享相同形状的锚点。
 
![](https://image.jiqizhixin.com/uploads/editor/de8d482c-85ba-4833-9d67-2caf341647ad/1524810332568.jpg)
 
这些锚点是精心挑选的，因此它们是多样的，且覆盖具有不同比例和宽高比的现实目标。这使得我们可以以更好的猜想来指导初始训练，并允许每个预测专门用于特定的形状。该策略使早期训练更加稳定和简便。
 
![](https://image.jiqizhixin.com/uploads/editor/0921d244-ef15-49fc-9d3e-fa3c4b217a01/1524810332665.jpg)
 
Faster R-CNN 使用更多的锚点。它部署 9 个锚点框：3 个不同宽高比的 3 个不同大小的锚点框。每一个位置使用 9 个锚点，每个位置会生成 2×9 个 objectness 分数和 4×9 个坐标。  
![](https://image.jiqizhixin.com/uploads/editor/be45acdf-9fdf-487b-8d67-5c3a1fcff82d/1524810648533.jpg)
 
_图源：https://arxiv.org/pdf/1506.01497.pdf_
 
### R-CNN 方法的性能
 
如下图所示，Faster R-CNN 的速度要快得多。
 
![](https://image.jiqizhixin.com/uploads/editor/085815f8-00f0-4677-8eae-50cdff80a8f9/1524810679225.jpg)
 
基于区域的全卷积神经网络（R-FCN）
 
假设我们只有一个特征图用来检测右眼。那么我们可以使用它定位人脸吗？应该可以。因为右眼应该在人脸图像的左上角，所以我们可以利用这一点定位整个人脸。
 
![](https://image.jiqizhixin.com/uploads/editor/b158b797-a090-4290-b261-2ee1b25895f4/1524810332828.jpg)
 
如果我们还有其他用来检测左眼、鼻子或嘴巴的特征图，那么我们可以将检测结果结合起来，更好地定位人脸。
 
现在我们回顾一下所有问题。在 Faster R-CNN 中，检测器使用了多个全连接层进行预测。如果有 2000 个 ROI，那么成本非常高。
 
```python
feature_maps = process(image)
ROIs = region_proposal(feature_maps)
for ROI in ROIs
    patch = roi_pooling(feature_maps, ROI)
    class_scores, box = detector(patch)         # Expensive!
    class_probabilities = softmax(class_scores)
```
 
R-FCN 通过减少每个 ROI 所需的工作量实现加速。上面基于区域的特征图与 ROI 是独立的，可以在每个 ROI 之外单独计算。剩下的工作就比较简单了，因此 R-FCN 的速度比 Faster R-CNN 快。
 
```python
feature_maps = process(image)
ROIs = region_proposal(feature_maps)         
score_maps = compute_score_map(feature_maps)
for ROI in ROIs
    V = region_roi_pool(score_maps, ROI)     
    class_scores, box = average(V)                   # Much simpler!
    class_probabilities = softmax(class_scores)
```
 
现在我们来看一下 5 × 5 的特征图 M，内部包含一个蓝色方块。我们将方块平均分成 3 × 3 个区域。现在，我们在 M 中创建了一个新的特征图，来检测方块的左上角（TL）。这个新的特征图如下图（右）所示。只有黄色的网格单元 \[2, 2\] 处于激活状态。
 
![](https://image.jiqizhixin.com/uploads/editor/561c6af5-c064-49d2-87e3-50630d94538a/1524810332733.jpg)
 
_在左侧创建一个新的特征图，用于检测目标的左上角。_
 
我们将方块分成 9 个部分，由此创建了 9 个特征图，每个用来检测对应的目标区域。这些特征图叫作位置敏感得分图（position-sensitive score map），因为每个图检测目标的子区域（计算其得分）。
 
![](https://image.jiqizhixin.com/uploads/editor/eec9f89a-48d0-4883-bb57-9d4b56e3381f/1524810332931.jpg)
 
_生成 9 个得分图_
 
下图中红色虚线矩形是建议的 ROI。我们将其分割成 3 × 3 个区域，并询问每个区域包含目标对应部分的概率是多少。例如，左上角 ROI 区域包含左眼的概率。我们将结果存储成 3 × 3 vote 数组，如下图（右）所示。例如，vote_array\[0\]\[0\] 包含左上角区域是否包含目标对应部分的得分。
 
![](https://image.jiqizhixin.com/uploads/editor/cfc8f00b-e286-46f4-978b-e331daa1609a/1524810333011.jpg)
 
_将 ROI 应用到特征图上，输出一个 3 x 3 数组。_
 
将得分图和 ROI 映射到 vote 数组的过程叫作位置敏感 ROI 池化（position-sensitive ROI-pool）。该过程与前面讨论过的 ROI 池化非常接近。
 
![](https://image.jiqizhixin.com/uploads/editor/a1e25668-6c3c-4abe-92b2-78d28536d83b/1524810333098.jpg)
 
_将 ROI 的一部分叠加到对应的得分图上，计算 V\[i\]\[j\]。_
 
在计算出位置敏感 ROI 池化的所有值后，类别得分是其所有元素得分的平均值。
 
![](https://image.jiqizhixin.com/uploads/editor/08dc47c6-31d3-4404-8816-d2ca9222cc1f/1524810333178.jpg)
 
_ROI 池化_
 
假如我们有 C 个类别要检测。我们将其扩展为 C + 1 个类别，这样就为背景（非目标）增加了一个新的类别。每个类别有 3 × 3 个得分图，因此一共有 (C+1) × 3 × 3 个得分图。使用每个类别的得分图可以预测出该类别的类别得分。然后我们对这些得分应用 softmax 函数，计算出每个类别的概率。
 
以下是数据流图，在我们的案例中，k=3。
 
![](https://image.jiqizhixin.com/uploads/editor/122f41d5-8ca5-4bd1-b5ef-bac0452706da/1524810333259.jpg)
 
## 总结
 
首先了解了基础的滑动窗口算法：
 
```python
for window in windows
    patch = get_patch(image, window)
    results = detector(patch)
```
 
然后尝试减少窗口数量，尽可能减少 for 循环中的工作量。
 
```
ROIs = region_proposal(image)
for ROI in ROIs
    patch = get_patch(image, ROI)
    results = detector(patch)
```
 
### 单次目标检测器
 
第二部分，我们将对单次目标检测器（包括 SSD、YOLO、YOLOv2、YOLOv3）进行综述。我们将分析 FPN 以理解多尺度特征图如何提高准确率，特别是小目标的检测，其在单次检测器中的检测效果通常很差。然后我们将分析 Focal loss 和 RetinaNet，看看它们是如何解决训练过程中的类别不平衡问题的。
 
单次检测器
 
Faster R-CNN 中，在分类器之后有一个专用的候选区域网络。
 
![](https://image.jiqizhixin.com/uploads/editor/9e0c5beb-6dc0-494c-bbf8-8da1b4666472/1524810328366.jpg)
 
_Faster R-CNN 工作流_
 
基于区域的检测器是很准确的，但需要付出代价。Faster R-CNN 在 PASCAL VOC 2007 测试集上每秒处理 7 帧的图像（7 FPS）。和 R-FCN 类似，研究者通过减少每个 ROI 的工作量来精简流程。
 
```python
feature_maps = process(image)
ROIs = region_proposal(feature_maps)
for ROI in ROIs
    patch = roi_align(feature_maps, ROI)
    results = detector2(patch)    # Reduce the amount of work here!
```
 
作为替代，我们是否需要一个分离的候选区域步骤？我们可以直接在一个步骤内得到边界框和类别吗？
 
```python
feature_maps = process(image)
results = detector3(feature_maps) # No more separate step for ROIs
```
 
让我们再看一下滑动窗口检测器。我们可以通过在特征图上滑动窗口来检测目标。对于不同的目标类型，我们使用不同的窗口类型。以前的滑动窗口方法的致命错误在于使用窗口作为最终的边界框，这就需要非常多的形状来覆盖大部分目标。更有效的方法是将窗口当做初始猜想，这样我们就得到了从当前滑动窗口同时预测类别和边界框的检测器。
 
![](https://image.jiqizhixin.com/uploads/editor/761e85fe-c0c2-4443-a3f9-063f4733fee3/1524810333381.jpg)
 
_基于滑动窗口进行预测_
 
这个概念和 Faster R-CNN 中的锚点很相似。然而，单次检测器会同时预测边界框和类别。例如，我们有一个 8 × 8 特征图，并在每个位置做出 k 个预测，即总共有 8 × 8 × k 个预测结果。
 
![](https://image.jiqizhixin.com/uploads/editor/c8430d56-3284-4d64-9059-e7b68e64f358/1524810333471.jpg)
 
_64 个位置_
 
在每个位置，我们有 k 个锚点（锚点是固定的初始边界框猜想），一个锚点对应一个特定位置。我们使用相同的 锚点形状仔细地选择锚点和每个位置。
 
![](https://image.jiqizhixin.com/uploads/editor/ac7f956c-60be-4bea-b09d-1a2c50af547b/1524810333511.jpg)
 
_使用 4 个锚点在每个位置做出 4 个预测。_
 
以下是 4 个锚点（绿色）和 4 个对应预测（蓝色），每个预测对应一个特定锚点。
 
![](https://image.jiqizhixin.com/uploads/editor/9266681b-9fac-412f-a547-c9f34cce649c/1524810333616.jpg)
 
_4 个预测，每个预测对应一个锚点。_
 
在 Faster R-CNN 中，我们使用卷积核来做 5 个参数的预测：4 个参数对应某个锚点的预测边框，1 个参数对应 objectness 置信度得分。因此 3× 3× D × 5 卷积核将特征图从 8 × 8 × D 转换为 8 × 8 × 5。
 
![](https://image.jiqizhixin.com/uploads/editor/9313cd65-7fd9-480d-a369-401d9ac1257a/1524810333689.jpg)
 
_使用 3x3 卷积核计算预测。_
 
在单次检测器中，卷积核还预测 C 个类别概率以执行分类（每个概率对应一个类别）。因此我们应用一个 3× 3× D × 25 卷积核将特征图从 8 × 8 × D 转换为 8 × 8 × 25（C=20）。
 
![](https://image.jiqizhixin.com/uploads/editor/73521513-3959-4bcd-9a38-c8be01ef6a63/1524810333748.jpg)
 
_每个位置做出 k 个预测，每个预测有 25 个参数。_
 
单次检测器通常需要在准确率和实时处理速度之间进行权衡。它们在检测太近距离或太小的目标时容易出现问题。在下图中，左下角有 9 个圣诞老人，但某个单次检测器只检测出了 5 个。
 
![](https://image.jiqizhixin.com/uploads/editor/e4a52e23-2282-4859-a369-20fb309bceb5/1524810334979.jpg)
 
## SSD
 
SSD 是使用 VGG19 网络作为特征提取器（和 Faster R-CNN 中使用的 CNN 一样）的单次检测器。我们在该网络之后添加自定义卷积层（蓝色），并使用卷积核（绿色）执行预测。
 
![](https://image.jiqizhixin.com/uploads/editor/71bca5b1-ad0c-400b-b866-afded83f55f9/1524810333805.jpg)
 
_同时对类别和位置执行单次预测。_
 
然而，卷积层降低了空间维度和分辨率。因此上述模型仅可以检测较大的目标。为了解决该问题，我们从多个特征图上执行独立的目标检测。
 
![](https://image.jiqizhixin.com/uploads/editor/096bf171-b014-48d5-b20e-b3f6b369367b/1524810334669.jpg)
 
_使用多尺度特征图用于检测。_
 
以下是特征图图示。
 
![](https://image.jiqizhixin.com/uploads/editor/bd0d98b9-10d3-4c94-bc29-a41b42587dcd/1524810334737.jpg)
 
_图源：https://arxiv.org/pdf/1512.02325.pdf_
 
SSD 使用卷积网络中较深的层来检测目标。如果我们按接近真实的比例重绘上图，我们会发现图像的空间分辨率已经被显著降低，且可能已无法定位在低分辨率中难以检测的小目标。如果出现了这样的问题，我们需要增加输入图像的分辨率。
 
![](https://image.jiqizhixin.com/uploads/editor/b9064245-5c94-46bb-a50b-13252dffa59b/1524810338669.jpg)
 
## YOLO
 
YOLO 全称 You Only Look Once（你只需看一次）
- 从名称上也能看出这种算法速度快的优势，因此在许多边缘设备上，YOLO算法的使用十分广泛。


与另一种著名的目标检测算法 `Fast R-CNN` 不同的是，`YOLO`采用“一步”的策略，同时生成目标物体的类别和位置。

YOLO算法相比Fast R-CNN具有两大优势：
- 1、速度快：每秒45帧的检测速率，可用在实时视频检测中，在更小的模型上甚至达到155帧；
- 2、通用性好：在真实图像数据上训练的网络，可以用在虚构的绘画作品上。

但是YOLO也存在着一定的局限性：
- 正确率不如Fast R-CNN，每个方格中只能检测一个物体，对于边缘不规则的物体，将会影响到周围物体的识别。

作者Redmon后来又在原始的YOLO技术上，发展出了YOLO9000、YOLOv3等算法，扩展了检测物体的种类、提高了模型的准确率。


### YOLO 资讯

【2020-2-22】[YOLO之父退出CV界表达抗议，拒绝AI算法用于军事和隐私窥探](https://www.qbitai.com/2020/02/11744.html)
- Jeseph Redmon毕业于美国米德尔伯里学院计算机科学专业，辅修数学。2013年进入华盛顿大学计算机专业攻读硕士学位，继而攻读博士学位，直到2019年。
- 在此期间，他和导师Ali Farhadi共同提出并改进了YOLO算法。主要研究范围是目标检测、图像分类和模型压缩。
- Joseph Redmon曾凭借该算法获得过2016年CVPR群众选择奖（People’s Choice Award）、2017年CVPR最佳论文荣誉奖（Best Paper Honorable Mention）。
- YOLO及其改进算法在学术圈被广泛引用，Redmon三篇一作相关论文总引用量已经超过1万。

YOLO算法作者Joseph Redmon在个人Twitter上宣布，将停止一切CV研究，原因是自己的开源算法已经用在军事和隐私问题上。这对他的道德造成了巨大的考验。

### YOLO 发展史


#### YOLO: A Brief History

【2023-11-14】[ultralytics 官方文档](https://docs.ultralytics.com/)

[YOLO](https://arxiv.org/abs/1506.02640) (You Only Look Once), a popular object detection and image segmentation model, was developed by Joseph Redmon and Ali Farhadi at the University of Washington. 
- Launched in 2015, YOLO quickly gained popularity for its high speed and accuracy.
-   [YOLOv2](https://arxiv.org/abs/1612.08242), released in 2016, improved the original model by incorporating batch normalization, anchor boxes, and dimension clusters.
-   [YOLOv3](https://pjreddie.com/media/files/papers/YOLOv3.pdf), launched in 2018, further enhanced the model's performance using a more efficient backbone network, multiple anchors and spatial pyramid pooling.
-   [YOLOv4](https://arxiv.org/abs/2004.10934) was released in 2020, introducing innovations like Mosaic data augmentation, a new anchor-free detection head, and a new loss function.
-   [YOLOv5](https://github.com/ultralytics/yolov5) further improved the model's performance and added new features such as hyperparameter optimization, integrated experiment tracking and automatic export to popular export formats.
-   [YOLOv6](https://github.com/meituan/YOLOv6) was open-sourced by [Meituan](https://about.meituan.com/) in 2022 and is in use in many of the company's autonomous delivery robots.
-   [YOLOv7](https://github.com/WongKinYiu/yolov7) added additional tasks such as pose estimation on the COCO keypoints dataset.
-   [YOLOv8](https://github.com/ultralytics/ultralytics) is the latest version of YOLO by Ultralytics. As a cutting-edge, state-of-the-art (SOTA) model, YOLOv8 builds on the success of previous versions, introducing new features and improvements for enhanced performance, flexibility, and efficiency. YOLOv8 supports a full range of vision AI tasks, including [detection](https://docs.ultralytics.com/#yolo-a-brief-historytasks/detect/), [segmentation](https://docs.ultralytics.com/#yolo-a-brief-historytasks/segment/), [pose estimation](https://docs.ultralytics.com/#yolo-a-brief-historytasks/pose/), [tracking](https://docs.ultralytics.com/#yolo-a-brief-historymodes/track/), and [classification](https://docs.ultralytics.com/#yolo-a-brief-historytasks/classify/). This versatility allows users to leverage YOLOv8's capabilities across diverse applications and domains.


**YOLO：简史**

[中文版](https://docs.ultralytics.com/zh/#_1)

[YOLO](https://arxiv.org/abs/1506.02640) (You Only Look Once)，由华盛顿大学的Joseph Redmon和Ali Farhadi开发的流行目标检测和图像分割模型，于2015年推出，由于其高速和准确性而迅速流行。
-   [YOLOv2](https://arxiv.org/abs/1612.08242) 在2016年发布，通过引入批量归一化、锚框和维度聚类来改进了原始模型。
-   [YOLOv3](https://pjreddie.com/media/files/papers/YOLOv3.pdf) 在2018年推出，进一步增强了模型的性能，使用了更高效的主干网络、多个锚点和空间金字塔池化。
-   [YOLOv4](https://arxiv.org/abs/2004.10934) 在2020年发布，引入了Mosaic数据增强、新的无锚检测头和新的损失函数等创新功能。
-   [YOLOv5](https://github.com/ultralytics/yolov5) 进一步改进了模型的性能，并增加了新功能，如超参数优化、集成实验跟踪和自动导出到常用的导出格式。
-   [YOLOv6](https://github.com/meituan/YOLOv6) 在2022年由[美团](https://about.meituan.com/)开源，现在正在该公司的许多自动送货机器人中使用。
-   [YOLOv7](https://github.com/WongKinYiu/yolov7) 在COCO关键点数据集上添加了额外的任务，如姿态估计。
-   [YOLOv8](https://github.com/ultralytics/ultralytics) 是Ultralytics的YOLO的最新版本。作为一种前沿、最先进(SOTA)的模型，YOLOv8在之前版本的成功基础上引入了新功能和改进，以提高性能、灵活性和效率。YOLOv8支持全范围的视觉AI任务，包括[检测](https://docs.ultralytics.com/tasks/detect/), [分割](https://docs.ultralytics.com/tasks/segment/), [姿态估计](https://docs.ultralytics.com/tasks/pose/), [跟踪](https://docs.ultralytics.com/modes/track/), 和[分类](https://docs.ultralytics.com/tasks/classify/)。这种多功能性使用户能够利用YOLOv8的功能应对多种应用和领域的需求。


#### 从v1到v8

【2023-1-16】[YOLO家族系列模型的演变：从v1到v8](https://www.toutiao.com/article/7189093101728825856)

|时间|版本|功能|备注|
|---|---|---|---|
|2015|v1|||
|2016|v2|||
|2018|v3|||
|2019|v4|||
|2020|v5|||
|2021.5|R|结合显性和隐性知识，多任务<br>检测精度和检出率高于竞争对手|[You Only Learn One Representation: Unified Network for Multiple Tasks](https://arxiv.org/pdf/2105.04206.pdf)|
|2022|v6|美团,三个改进点:<br>backbone 和 neck部分对硬件进行了优化设计<br>forked head 更准确<br>更有效的训练策略<br>与YOLOv6-nano模型相比，YOLOv6-nano模型的速度提高了21%，精度提高了3.6%|[YOLOv6: A Single-Stage Object Detection Framework for Industrial Applications](https://arxiv.org/pdf/2209.02976.pdf)<br>[博客地址](https://tech.meituan.com/2022/06/23/yolov6-a-fast-and-accurate-target-detection-framework-is-opening-source.html)|
|2022.7|v7|sota，E-ELAN(扩展高效层聚合网络), pytorch<br>检测精度和检出率高于竞争对手|[YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors](https://arxiv.org/pdf/2207.02696.pdf)|
|2023.1|v8|Ultralytics发布,无锚点模型<br>YOLOv8领先于YOLOv7和YOLOv6等|论文尚未发表|

yolo迭代到了v8版本
- 2017年在mac上试过v2，实时目标检测，挺灵敏；
- 后面几个版本迭代到手机部署，v5在手机上识别速度几十ms，[手机识别](https://www.qbitai.com/2021/12/30807.html)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/d08ca27be4034910820c272b497982e0~tplv-obj:1024:576.image?_iz=97245&from=post&x-expires=1706140800&x-signature=BADoMiDtOYEgtW6cHz6%2FvC90XMM%3D)

- YOLOv3之前的所有YOLO对象检测模型都是用C语言编写的，并使用了Darknet框架，Ultralytics发布了第一个使用PyTorch框架实现的YOLO (YOLOv3)，YOLOv3发布后不久，Joseph Redmon就离开了计算机视觉研究社区。
- Ultralytics发布了YOLOv5
  - [yolov5s_android](https://github.com/lp6m/yolov5s_android)
- 在2023年1月，Ultralytics发布了YOLOv8。
- YOLOv8包含五个模型，用于检测、分割和分类。YOLOv8 Nano是其中最快和最小的，而YOLOv8 Extra Large (YOLOv8x)是其中最准确但最慢的，具体模型见后续的图。

YOLOv8附带以下预训练模型:
- 目标检测在图像分辨率为640的COCO检测数据集上进行训练。
- 实例分割在图像分辨率为640的COCO分割数据集上训练。
- 图像分类模型在ImageNet数据集上预训练，图像分辨率为224。

#### 图解

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-09-15T09:20:30.491Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36\&quot; etag=\&quot;orx_c-yNTETa0hNO38D_\&quot; version=\&quot;21.7.2\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;VC8KsEmwTz_4FKU3JA4y\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;789\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-2\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=none;glass=0;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;260\&quot; y=\&quot;120\&quot; width=\&quot;990\&quot; height=\&quot;510\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-49\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=1 1;fillColor=none;strokeWidth=2;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;335\&quot; y=\&quot;160\&quot; width=\&quot;170\&quot; height=\&quot;110\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-7\&quot; value=\&quot;YOLO家族进化史\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=20;strokeWidth=2;fontFamily=Verdana;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;595\&quot; y=\&quot;70\&quot; width=\&quot;180\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-21\&quot; value=\&quot;Apache 2.0\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;355\&quot; y=\&quot;190\&quot; width=\&quot;90\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-28\&quot; value=\&quot;YOLO v5\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;700\&quot; y=\&quot;500\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-48\&quot; value=\&quot;YOLO v1\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;310\&quot; y=\&quot;560\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;8V-hR4rmnCvxMIKz6rSl-50\&quot; value=\&quot;激进优化\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=17;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#666666;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;250\&quot; y=\&quot;340\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-2\&quot; value=\&quot;all-erminssive\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;355\&quot; y=\&quot;220\&quot; width=\&quot;90\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-3\&quot; value=\&quot;GPL 3.0\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;355\&quot; y=\&quot;160\&quot; width=\&quot;85\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-4\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#B3B3B3;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;260\&quot; y=\&quot;650\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1230\&quot; y=\&quot;650\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-5\&quot; value=\&quot;增量优化\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=17;strokeWidth=2;fontFamily=Verdana;fontStyle=0;fontColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;680\&quot; y=\&quot;610\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-6\&quot; value=\&quot;2015\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;322.5\&quot; y=\&quot;650\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-7\&quot; value=\&quot;YOLO v2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; y=\&quot;500\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-8\&quot; value=\&quot;YOLO v3\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;560\&quot; y=\&quot;500\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-11\&quot; value=\&quot;YOLOX\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;830\&quot; y=\&quot;360\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-13\&quot; value=\&quot;YOLO v6\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1010\&quot; y=\&quot;290\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-14\&quot; value=\&quot;YOLO v7\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1010\&quot; y=\&quot;210\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-15\&quot; value=\&quot;YOLO v8\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1140\&quot; y=\&quot;210\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-16\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;exitX=1;exitY=0;exitDx=0;exitDy=0;entryX=0;entryY=1;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;8V-hR4rmnCvxMIKz6rSl-48\&quot; target=\&quot;_ze0iByAne0-O5BmJI7g-7\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;430\&quot; y=\&quot;600\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;480\&quot; y=\&quot;550\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-17\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;_ze0iByAne0-O5BmJI7g-7\&quot; target=\&quot;_ze0iByAne0-O5BmJI7g-8\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;410\&quot; y=\&quot;570\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;440\&quot; y=\&quot;550\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-18\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;_ze0iByAne0-O5BmJI7g-8\&quot; target=\&quot;8V-hR4rmnCvxMIKz6rSl-28\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;420\&quot; y=\&quot;580\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;450\&quot; y=\&quot;560\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-19\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;_ze0iByAne0-O5BmJI7g-8\&quot; target=\&quot;_ze0iByAne0-O5BmJI7g-1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;660\&quot; y=\&quot;530\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;710\&quot; y=\&quot;530\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-20\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;strokeColor=#999999;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;_ze0iByAne0-O5BmJI7g-9\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;650\&quot; y=\&quot;520\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;720\&quot; y=\&quot;540\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-21\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;_ze0iByAne0-O5BmJI7g-1\&quot; target=\&quot;_ze0iByAne0-O5BmJI7g-10\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;790\&quot; y=\&quot;459.5\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;830\&quot; y=\&quot;460\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-23\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;_ze0iByAne0-O5BmJI7g-8\&quot; target=\&quot;_ze0iByAne0-O5BmJI7g-11\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;800\&quot; y=\&quot;470\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;837\&quot; y=\&quot;470\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-24\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;_ze0iByAne0-O5BmJI7g-9\&quot; target=\&quot;_ze0iByAne0-O5BmJI7g-14\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;810\&quot; y=\&quot;480\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;847\&quot; y=\&quot;480\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-25\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;_ze0iByAne0-O5BmJI7g-9\&quot; target=\&quot;_ze0iByAne0-O5BmJI7g-12\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;790\&quot; y=\&quot;390\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;840\&quot; y=\&quot;390\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-1\&quot; value=\&quot;PP-YOLO\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;700\&quot; y=\&quot;440\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-27\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;8V-hR4rmnCvxMIKz6rSl-28\&quot; target=\&quot;_ze0iByAne0-O5BmJI7g-13\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;800\&quot; y=\&quot;470\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;837\&quot; y=\&quot;470\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-28\&quot; value=\&quot;PP-YOLOE\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1010\&quot; y=\&quot;360\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-29\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.75;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;_ze0iByAne0-O5BmJI7g-10\&quot; target=\&quot;_ze0iByAne0-O5BmJI7g-28\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;800\&quot; y=\&quot;530\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;1065\&quot; y=\&quot;340\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-9\&quot; value=\&quot;YOLO v4\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;700\&quot; y=\&quot;380\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-10\&quot; value=\&quot;PP-YOLO v2\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;827\&quot; y=\&quot;440\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-12\&quot; value=\&quot;YOLOR\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;830\&quot; y=\&quot;290\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-31\&quot; value=\&quot;2016\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;445\&quot; y=\&quot;650\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-32\&quot; value=\&quot;2018\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;580\&quot; y=\&quot;650\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-33\&quot; value=\&quot;2020\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;710\&quot; y=\&quot;650\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-34\&quot; value=\&quot;2021\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;870\&quot; y=\&quot;650\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-35\&quot; value=\&quot;2022\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1025\&quot; y=\&quot;650\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;_ze0iByAne0-O5BmJI7g-36\&quot; value=\&quot;2023\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;1155\&quot; y=\&quot;650\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>


### YOLO 原理

YOLO 是另一种单次目标检测器。
 
YOLO 在卷积层之后使用了 DarkNet 来做特征检测。
- ![](https://image.jiqizhixin.com/uploads/editor/b76a02d5-2a4a-43fd-90e7-052335d88146/1524810338743.jpg)
 
然而，它并没有使用多尺度特征图来做独立的检测。相反，它将特征图部分平滑化，并将其和另一个较低分辨率的特征图拼接。例如，YOLO 将一个 28 × 28 × 512 的层重塑为 14 × 14 × 2048，然后将它和 14 × 14 ×1024 的特征图拼接。之后，YOLO 在新的 14 × 14 × 3072 层上应用卷积核进行预测。
 
YOLO（v2）做出了很多实现上的改进，将 mAP 值从第一次发布时的 63.4 提高到了 78.6。YOLO9000 可以检测 9000 种不同类别的目标。
- ![](https://image.jiqizhixin.com/uploads/editor/0e8e87de-4082-4450-9e68-5a17cae766bd/1524810338854.jpg)
 
[图源](https://arxiv.org/pdf/1612.08242.pdf)

以下是 YOLO 论文中不同检测器的 mAP 和 FPS 对比。YOLOv2 可以处理不同分辨率的输入图像。低分辨率的图像可以得到更高的 FPS，但 mAP 值更低。
- ![](https://image.jiqizhixin.com/uploads/editor/c8b94c58-c362-4593-a982-a42165f2bddc/1524810338786.jpg)


## YOLOv3
 
YOLOv3 使用了更加复杂的骨干网络来提取特征。DarkNet-53 主要由 3 × 3 和 1× 1 的卷积核以及类似 ResNet 中的跳过连接构成。相比 ResNet-152，DarkNet 有更低的 BFLOP（十亿次浮点数运算），但能以 2 倍的速度得到相同的分类准确率。
 
![](https://image.jiqizhixin.com/uploads/editor/32ac614a-e215-4fcf-b6e7-74d91fc65f8a/1524810338923.jpg)
 
_图源：https://pjreddie.com/media/files/papers/YOLOv3.pdf_
 
YOLOv3 还添加了特征金字塔，以更好地检测小目标。以下是不同检测器的准确率和速度的权衡。
 
![](https://image.jiqizhixin.com/uploads/editor/fca7d1e5-c6dc-44b0-804e-0db90fdf5426/1524810339015.jpg)
 
_图源：https://pjreddie.com/media/files/papers/YOLOv3.pdf_
 
### 特征金字塔网络（FPN）
 
检测不同尺度的目标很有挑战性，尤其是小目标的检测。特征金字塔网络（FPN）是一种旨在提高准确率和速度的特征提取器。它取代了检测器（如 Faster R-CNN）中的特征提取器，并生成更高质量的特征图金字塔。
 
数据流
 
![](https://image.jiqizhixin.com/uploads/editor/e7d97947-30b4-4d2a-b274-927ed338cf91/1524810339079.jpg)
 
_FPN（图源：https://arxiv.org/pdf/1612.03144.pdf）_
 
FPN 由自下而上和自上而下路径组成。其中自下而上的路径是用于特征提取的常用卷积网络。空间分辨率自下而上地下降。当检测到更高层的结构，每层的语义值增加。
 
![](https://image.jiqizhixin.com/uploads/editor/765cf51f-787e-4089-9591-026d6ebf6476/1524810339174.jpg)
 
_FPN 中的特征提取（编辑自原论文）_
 
SSD 通过多个特征图完成检测。但是，最底层不会被选择执行目标检测。它们的分辨率高但是语义值不够，导致速度显著下降而不能被使用。SSD 只使用较上层执行目标检测，因此对于小的物体的检测性能较差。
 
![](https://image.jiqizhixin.com/uploads/editor/7ff17ace-6c7f-4709-bff2-31189fc63563/1524810339224.jpg)
 
_图像修改自论文 https://arxiv.org/pdf/1612.03144.pdf_
 
FPN 提供了一条自上而下的路径，从语义丰富的层构建高分辨率的层。
 
![](https://image.jiqizhixin.com/uploads/editor/45f068b6-b9f8-4b49-85ba-4d5565b11647/1524810339278.jpg)
 
_自上而下重建空间分辨率（编辑自原论文）_
 
虽然该重建层的语义较强，但在经过所有的上采样和下采样之后，目标的位置不精确。在重建层和相应的特征图之间添加横向连接可以使位置侦测更加准确。
 
![](https://image.jiqizhixin.com/uploads/editor/7f3114e0-7196-44cd-b884-7d29364e1b90/1524810339123.jpg)
 
_增加跳过连接（引自原论文）_
 
下图详细说明了自下而上和自上而下的路径。其中 P2、P3、P4 和 P5 是用于目标检测的特征图金字塔。
 
![](https://image.jiqizhixin.com/uploads/editor/e1f56dc7-4ace-475d-aed4-dc25bbaae97b/1524810340484.jpg)
 
### FPN 结合 RPN
 
FPN 不单纯是目标检测器，还是一个目标检测器和协同工作的特征检测器。分别传递到各个特征图（P2 到 P5）来完成目标检测。
 
![](https://image.jiqizhixin.com/uploads/editor/62d44f55-6bf2-4cca-aac6-731a08b0644b/1524810339366.jpg)
 
FPN 结合 Fast R-CNN 或 Faster R-CNN
 
在 FPN 中，我们生成了一个特征图的金字塔。用 RPN（详见上文）来生成 ROI。基于 ROI 的大小，我们选择最合适尺寸的特征图层来提取特征块。
 
![](https://image.jiqizhixin.com/uploads/editor/91682d7d-4a09-490c-97b7-963b8b5f1100/1524810340550.jpg)
 
困难案例
 
对于如 SSD 和 YOLO 的大多数检测算法来说，我们做了比实际的目标数量要多得多的预测。所以错误的预测比正确的预测要更多。这产生了一个对训练不利的类别不平衡。训练更多的是在学习背景，而不是检测目标。但是，我们需要负采样来学习什么是较差的预测。所以，我们计算置信度损失来把训练样本分类。选取最好的那些来确保负样本和正样本的比例最多不超过 3:1。这使训练更加快速和稳定。
 
推断过程中的非极大值抑制
 
检测器对于同一个目标会做出重复的检测。我们利用非极大值抑制来移除置信度低的重复检测。将预测按照置信度从高到低排列。如果任何预测和当前预测的类别相同并且两者 IoU 大于 0.5，我们就把它从这个序列中剔除。
 
Focal Loss（RetinaNet）
 
类别不平衡会损害性能。SSD 在训练期间重新采样目标类和背景类的比率，这样它就不会被图像背景淹没。Focal loss（FL）采用另一种方法来减少训练良好的类的损失。因此，只要该模型能够很好地检测背景，就可以减少其损失并重新增强对目标类的训练。我们从交叉熵损失 CE 开始，并添加一个权重来降低高可信度类的 CE。
 
![](https://image.jiqizhixin.com/uploads/editor/93473e21-749b-4404-b25f-93cc063baa43/1524810340587.jpg)
 
例如，令 γ = 0.5, 经良好分类的样本的 Focal loss 趋近于 0。
 
![](https://image.jiqizhixin.com/uploads/editor/ae73225e-7c50-45e1-a924-66cd0696aefc/1524810340628.jpg)
 
_编辑自原论文_
 
这是基于 FPN、ResNet 以及利用 Focal loss 构建的 RetianNet。
 
![](https://image.jiqizhixin.com/uploads/editor/5526e1b4-fe6c-46ec-bdf6-9347e903383a/1524810340700.jpg)
 
_RetinaNet_


## YOLOX

【2021-10-8】2021年旷视科技推出[yolox](https://github.com/Megvii-BaseDetection/YOLOX)，[YOLOX: Exceeding YOLO Series in 2021](https://arxiv.org/abs/2107.08430)， [手把手教你使用YOLOX进行物体检测](https://jishuin.proginn.com/p/763bfbd6774b)

YOLOX 是旷视开源的高性能检测器。旷视的研究者将解耦头、数据增强、无锚点以及标签分类等目标检测领域的优秀进展与 YOLO 进行了巧妙的集成组合，提出了 YOLOX，不仅实现了超越 YOLOv3、YOLOv4 和 YOLOv5 的 AP，而且取得了极具竞争力的推理速度。YOLOX-L版本以 68.9 FPS 的速度在 COCO 上实现了 50.0% AP，比 YOLOv5-L 高出 1.8% AP！还提供了支持 ONNX、TensorRT、NCNN 和 Openvino 的部署版本


### 部署实践


（1）环境准备
- 环境确认
  - 先判断Windows系统是32位还是64位,再选择对应的工具包
    - x86-64是64位版本，x86是32位版本
    - 所有客户端软件都需要注意32还是64位
  - 简洁方法: 右键 → 计算机 → 属性 → 系统类型
    - ![](https://pic3.zhimg.com/80/v2-df2152fe82d486ac8164fcd7d791ce32_1440w.webp)
  - 详细方法见[微软官方文档](https://support.microsoft.com/en-us/windows/32-bit-and-64-bit-windows-frequently-asked-questions-c6ca9541-8dce-4d48-0415-94a3faa2e13d)
- Git工具安装 
  - windows安装git bash，参考[地址](https://git-scm.com/download/win)
  - 注意：
- Python环境安装
  - windows安装Python3，下载[地址](https://www.python.org/downloads/windows/)

（2）yolox下载部署
- 使用git下载代码到本地计算机
- 进入目录 YOLOX，本地安装

```sh
git clone git@github.com:Megvii-BaseDetection/YOLOX.git
cd YOLOX
pip3 install -v -e .  # or  python3 setup.py develop
```


（3）数据准备
- 准备测试视频
- 可以从[pixbay](https://pixabay.com/zh/videos/search/%E9%AB%98%E9%80%9F%E5%85%AC%E8%B7%AF/)下载高速免费视频


（4）下载模型

从GitHub下载模型文件到本地model目录
- 以下是shell脚本，windows下需要手工下载、操作

```sh
mkdir model
cd model
wget https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_l.pth 
```

（5）启动

```sh
# ==== image demo =====
#python tools/demo.py image -f exps/default/yolox_s.py -c /path/to/your/yolox_s.pth --path assets/dog.jpg --conf 0.25 --nms 0.45 --tsize 640 --save_result --device [cpu/gpu]
#python tools/demo.py image -n yolox-s -c $model_file --path assets/dog.jpg --conf 0.25 --nms 0.45 --tsize 640 --save_result --device cpu # gpu

# 更换模型时，需要同步更新3个参数
model_name='yolox-l'
model_file='model/yolox_l.pth'
tsize=640 
python tools/demo.py image -n $model_name -c $model_file --path assets/dog.jpg --conf 0.25 --nms 0.45 --tsize $tsize --save_result --device cpu
# ==== video demo =====
# python tools/demo.py video -n yolox-s -c /path/to/your/yolox_s.pth --path /path/to/your/video --conf 0.25 --nms 0.45 --tsize 640 --save_result --device [cpu/gpu]
python tools/demo.py video -n $model_name -c $model_file --path /path/to/your/video --conf 0.25 --nms 0.45 --tsize $tsize --save_result --device cpu
```

【2023-11-8】实践通过

```sh
cur_dir='YOLOX'
#python tools/demo.py image -n yolox-l -c model/yolox_l.pth --path assets/dog.jpg --conf 0.25 --nms 0.45 --tsize 640 --save_result --device cpu
model_name='yolox-l'
model_file="${cur_dir}/model/yolox_l.pth"
tsize=640
# ==== image demo =====
data_file="${cur_dir}/assets/dog.jpg"
cmd="python ${cur_dir}/tools/demo.py image -n $model_name -c $model_file --path $data_file --conf 0.25 --nms 0.45 --tsize $tsize --save_result --device cpu"
echo "$cmd" && eval $cmd
# ==== video demo =====
data_file='../data/road_human.mp4'
# python tools/demo.py video -n yolox-s -c /path/to/your/yolox_s.pth --path /path/to/your/video --conf 0.25 --nms 0.45 --tsize 640 --save_result --device [cpu/gpu]
cmd="python tools/demo.py video -n $model_name -c $model_file --path $data_file --conf 0.25 --nms 0.45 --tsize $tsize --save_result --device cpu"
echo "$cmd" && eval $cmd
```


## YOLO V5

2020年5月发布YOLOv5，最大的特点就是**模型小，速度快**，所以能很好的应用在移动端。

【2021-12-7】[用安卓手机解锁目标检测模型YOLOv5，识别速度不过几十毫秒](https://www.qbitai.com/2021/12/30807.html)
- YOLO最新：v5版本，可在手机上玩儿了！只需要区区几十毫秒，桌上的东西就全被检测出来了
- [yolov5s_android](https://github.com/lp6m/yolov5s_android)
- ![](https://p26.toutiaoimg.com/img/tos-cn-i-qvj2lq49k0/7009b04195f740e9ba6aa82f90cca89f~tplv-tt-shrink:640:0.image)

## YOLO v8

【2023-9-12】[用YOLOv8一站式解决图像分类、检测、分割](https://www.toutiao.com/article/7277882430537646644),淡化YOLO版本，主打Ultralytics平台。YOLO原本是一种公开的**目标检测**算法。优势是速度快，准确率还高.
- [官网](https://ultralytics.com)
- [文档](https://docs.ultralytics.com)
- [GitHub](https://github.com/ultralytics/ultralytics)
- [labelImg](https://github.com/HumanSignal/labelImg)

### yolov8 功能

v8版本不局限于目标检测，更像是一个AI视觉处理平台，不但可以做检测，还可以做**分类、分割、跟踪，甚至姿态估计**。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/6fbc01d3d14f438ea9aa6b8ce86fbf68~tplv-tt-origin-asy2:5aS05p2hQElURueUt-WtqQ==.image?_iz=58558&from=article.pc_detail&x-expires=1695564568&x-signature=fWs9kU8VRfPoVHMKh8r0N%2FPnU88%3D)
- ![](https://raw.githubusercontent.com/ultralytics/assets/main/im/banner-tasks.png)

功能
- Detection (COCO) 检测
- Detection (Open Image V7)
- Segmentation (COCO) 分割
- Pose (COCO) 姿态估计
- Classification (ImageNet) 分类


### yolov8 模型

YOLOv8针对COCO数据集（一个很好的计算机视觉数据集）训练生成的。
- 可以自行使用labelImg进行图片标记，扩充数据集
 
| 名称 | 模型文件 | 家族 | 
| --- | --- | --- | 
| 检测 | yolov8n.pt | 8n、8s、8m、8l、8x |
| 分割 | yolov8n-seg.pt | 8n、8s、8m、8l、8x |
| 分类 | yolov8n-cls.pt | 8n、8s、8m、8l、8x |
| 姿态 | yolov8n-pose.pt | 8n、8s、8m、8l、8x |

每一类模型包含一个家族。好比是同一款衣服的不同尺码

| 类型| 准确度 | 耗时长| 运算次数/秒|
| ---| ---| --- | --- |
| YOLOv8n| 37.3| 80.4| 8.7|
| YOLOv8s| 44.9| 128.4| 28.6|
| YOLOv8m| 50.2| 234.7| 78.9|
| YOLOv8l| 52.9| 375.2| 165.2|
| YOLOv8x| 53.9| 479.1| 257.8|


### yolov8 实践


#### 安装

```sh
# 安装
pip install ultralytics
# 测试, 模型文件才 7m !
#yolo predict model=yolov8n.pt source=bus.jpg
yolo predict model=yolov8n.pt source='https://ultralytics.com/images/bus.jpg'

```

#### 目标检测

代码调用

```py
# 从平台库导入YOLO类
from ultralytics import YOLO
# 从模型文件构建model
model = YOLO("xx.pt")
# 对某张图片进行预测
results = model("bus.jpg")
# 打印识别结果
print(results)
# -----------
from ultralytics import YOLO
from PIL import Image

model = YOLO('yolov8n-seg.pt')
image = Image.open("bus.jpg")
results = model.predict(source=image, save=True, save_txt=True) 
# 识别来自文件夹的图像
results = model.predict(source="test/pics", ……) 
# 识别来自摄像头的图像
results = model.predict(source="0", ……)
# 查看结果
results[0].boxes
results[0].masks
# -------------
from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="coco128.yaml", epochs=3)  # train the model
metrics = model.val()  # evaluate model performance on the validation set
results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
path = model.export(format="onnx")  # export the model to ONNX format
```

results 类
- boxes: 检测出来物体的矩形框，就是目标检测的框。
- masks: 检测出来的遮罩层，调用图像分割时，这项有数据。
- keypoints: 检测出来的关键点，人体姿势估计时，身体的点就是这项。
- names: 分类数据的名称，比如{0: 人，1: 狗}这类索引。


#### 目标跟踪

```py
from ultralytics import YOLO

# Load an official or custom model
model = YOLO('yolov8n.pt')  # Load an official Detect model
model = YOLO('yolov8n-seg.pt')  # Load an official Segment model
model = YOLO('yolov8n-pose.pt')  # Load an official Pose model
# model = YOLO('path/to/best.pt')  # Load a custom trained model

# Perform tracking with the model
results = model.track(source="https://youtu.be/LNwODJXcvt4", show=True)  # Tracking with default tracker
results = model.track(source="https://youtu.be/LNwODJXcvt4", show=True, tracker="bytetrack.yaml")  # Tracking with ByteTrack tracker

```


## 端侧 目标检测

### YOLO-NAS


YOLO-NAS 是一款基于YOLO系列的全新对象检测模型，采用NAS技术进行预训练，并在COCO、Objects365和Roboflow 100等数据集上进行了验证，实现了前所未有的精度-速度性能。


### mediapipe


【2023-10-26】Google发布移动终端对象检测模型 —— mediapipe，无GPU依然飞快

而Google的mediapipe系列则成功将对象检测模型运行在移动终端上，实现了ms级别的延时。对于没有GPU的情况，可以使用MediaPipe对象检测模型，其int8模型只有29.31ms的延时，最大模型也只有198.77ms的延时



# 实践

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9tbWJpei5xcGljLmNuL21tYml6X2dpZi8xTXRuQXhtV1N3TnBlWHVvOFAyd1ZpY2lhVkswdEEzcXBQMmliRHp2anRpY0N0NU1WSllzUFVCb2liZXU0TjZxbUxSZTJrTG13SWljRHNXY2hNRFE4aWJZam9jb1EvNjQw?x-oss-process=image/format,png)

- 【2021-5-18】[4种YOLO目标检测的C++和Python两种版本实现](https://www.toutiao.com/i6963503613297689102/)
- 2020年，新出了几个新版本的YOLO目标检测，最多的有YOLOv4，Yolo-Fastest，YOLObile以及百度提出的PP-YOLO。C++编写一套基于OpenCV的YOLO目标检测，这个程序里包含了经典的YOLOv3，YOLOv4，Yolo-Fastest和YOLObile这4种YOLO目标检测的实现
- Yolo-Fastest运行速度最快，YOLObile号称是实时的，但是从结果看并不如此。并且查看它们的模型文件，可以看到Yolo-Fastest的是最小的。
- opencv实现yolov5目标检测，程序依然是包含了C++和Python两种版本的实现，地址: [python](https://github.com/hpc203/yolov5-dnn-cpp-python),  [C++](https://github.com/hpc203/yolov5-dnn-cpp-python-v2)

![](https://p6-tt.byteimg.com/origin/pgc-image/3ae75db8898d47eaac8b9649a0ff5a97?from=pc)

## 实时检测

- [实时隐身不留痕项目作者：Jason Mayes](https://mp.weixin.qq.com/s?__biz=MzU1NTUxNTM0Mg==&mid=2247493105&idx=1&sn=7726468d8faaf777284f32997ee33750&chksm=fbd18950cca60046ac133d3fde0857ecfeb7a93769dd135f4a915b923f1da386eeb5264e912a&scene=126&sessionid=1583675043&key=6dc1e3ec383dbb13146e922235a89f44535156bfd8c1191ba4da2e1c3d0365f4f30f345dd86d90910b1a201f10123e81b09a81195d6b3ab30bb32c563907f5525316a57147dc102623de78139e3578d1&ascene=1&uin=OTY1NzE1MTYw&devicetype=Windows+10&version=62080079&lang=zh_CN&exportkey=AX872ydDK0J27zzwMHx%2Fm7c%3D&pass_ticket=5I0Z9AD6y0vIicNPU2j%2BnyzrIe8dG1OkhbEAOwj1UMnKZY%2F9N8SIhRHlOQiY2k%2Bd)
- [Real-Time-Person-Removal](https://github.com/jasonmayes/Real-Time-Person-Removal)
- [Demo 地址](https://codepen.io/jasonmayes/pen/GRJqgma)

<iframe src="https://codepen.io/jasonmayes/pen/GRJqgma" scrolling="yes" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width='800' height='600'> </iframe>

### 实时人物分割

- 【2019-04-11】[浏览器上跑：TensorFlow发布实时人物分割模型，秒速25帧24个部位](https://www.toutiao.com/a6658462631025705480/?tt_from=mobile_qq&utm_campaign=client_share&timestamp=1554985015&app=news_article&utm_source=mobile_qq&utm_medium=toutiao_android&req_id=201904112016540100230730289583E63&group_id=6658462631025705480)
  - TensorFlow开源了一个实时人物分割模型，叫BodyPix。这个模型，在浏览器上用TensorFlow.js就能跑。而且，帧率还很可观，在默认设定下：
    - 用2018版15吋MacBook Pro跑，每秒25帧。用iPhone X跑，每秒21帧。
  - 如果不和其他模型搭配的话，BodyPix只适用于单人影像。

<iframe src="https://storage.googleapis.com/tfjs-models/demos/body-pix/index.html" scrolling="yes" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width='800' height='600'> </iframe>

### OpenPose

【2024-1-12】[实时多人关键点AI检测开源！](https://www.toutiao.com/article/7322712733185884724)

OpenPose 是一个开源的**实时**多人关键点检测库，由卡内基梅隆大学的感知计算实验室（Perceptual Computing Lab）开发。它旨在通过深度学习技术实现高效的**人体姿态估计**，并可以同时检测多个人的身体、面部、手部和脚部的关键点。

OpenPose 的出现为人体姿态估计领域带来了重要的突破，特别是在实时性和多人检测方面。[img](https://p3-sign.toutiaoimg.com/tos-cn-i-twdt4qpehh/3b5cbf862f644d82a8a934c278bb7415~noop.image)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-twdt4qpehh/3b5cbf862f644d82a8a934c278bb7415~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1705675968&x-signature=G5W65u7Q1rVVV6TzsPrXZTX6ias%3D)

核心特点
- 实时性：OpenPose 设计用于实时处理，可以在接近实时的时间内完成关键点检测。
- 多人检测：OpenPose 能够在单张图像中同时检测多个人的姿态，这对于多人交互场景尤为重要。
- 关键点检测：它可以识别和定位人体、面部、手部和脚部的关键点，总共超过 135 个关键点。
- 灵活性：OpenPose 支持多种编程语言和框架，包括 Python、C++ 和 MATLAB，以及 TensorFlow、Caffe 和 PyTorch 等。
- 开源：OpenPose 是开源的，这意味着任何人都可以自由使用和修改代码，以适应不同的应用需求。

应用场景
- 增强现实和虚拟现实：在 AR/VR 应用中，OpenPose 可以用来跟踪用户的身体和手部动作，提供更自然的交互体验。
- 人机交互：OpenPose 可以用于智能助手和机器人，帮助它们更好地理解和响应用户的需求。
- 体育分析：在体育比赛中，OpenPose 可以用来分析运动员的姿态和动作，提供战术和训练建议。
- 安全监控：在安全监控领域，OpenPose 可以用来识别异常行为或特定姿态，提高监控系统的有效性。


## 基于tensorflow.js的实时检测Demo

- 参考：[In-browser real-time object detection with TensorFlow.js and React](https://github.com/juandes/tensorflowjs-objectdetection-tutorial)

![](https://github.com/juandes/tensorflowjs-objectdetection-tutorial/raw/master/gif/1.gif)

### 实时检测Demo

站内[demo](wqw/demo/object_detection.html)

<iframe src="https://nanonets.com/object-detection-with-tensorflowjs-demo/" scrolling="yes" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width='800' height='600'> </iframe>

### 代码

- detect.js内容

```javascript
class App extends React.Component {
  // reference to both the video and canvas
  videoRef = React.createRef();
  canvasRef = React.createRef();

  // we are gonna use inline style
  styles = {
    position: 'fixed',
    top: 150,
    left: 150,
  };


  detectFromVideoFrame = (model, video) => {
    model.detect(video).then(predictions => {
      this.showDetections(predictions);

      requestAnimationFrame(() => {
        this.detectFromVideoFrame(model, video);
      });
    }, (error) => {
      console.log("Couldn't start the webcam")
      console.error(error)
    });
  };

  showDetections = predictions => {
    const ctx = this.canvasRef.current.getContext("2d");
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    const font = "24px helvetica";
    ctx.font = font;
    ctx.textBaseline = "top";

    predictions.forEach(prediction => {
      const x = prediction.bbox[0];
      const y = prediction.bbox[1];
      const width = prediction.bbox[2];
      const height = prediction.bbox[3];
      // Draw the bounding box.
      ctx.strokeStyle = "#2fff00";
      ctx.lineWidth = 1;
      ctx.strokeRect(x, y, width, height);
      // Draw the label background.
      ctx.fillStyle = "#2fff00";
      const textWidth = ctx.measureText(prediction.class).width;
      const textHeight = parseInt(font, 10);
      // draw top left rectangle
      ctx.fillRect(x, y, textWidth + 10, textHeight + 10);
      // draw bottom left rectangle
      ctx.fillRect(x, y + height - textHeight, textWidth + 15, textHeight + 10);

      // Draw the text last to ensure it's on top.
      ctx.fillStyle = "#000000";
      ctx.fillText(prediction.class, x, y);
      ctx.fillText(prediction.score.toFixed(2), x, y + height - textHeight);
    });
  };

  componentDidMount() {
    if (navigator.mediaDevices.getUserMedia || navigator.mediaDevices.webkitGetUserMedia) {
      // define a Promise that'll be used to load the webcam and read its frames
      const webcamPromise = navigator.mediaDevices
        .getUserMedia({
          video: true,
          audio: false,
        })
        .then(stream => {
          // pass the current frame to the window.stream
          window.stream = stream;
          // pass the stream to the videoRef
          this.videoRef.current.srcObject = stream;

          return new Promise(resolve => {
            this.videoRef.current.onloadedmetadata = () => {
              resolve();
            };
          });
        }, (error) => {
          console.log("Couldn't start the webcam")
          console.error(error)
        });

      // define a Promise that'll be used to load the model
      const loadlModelPromise = cocoSsd.load();
      
      // resolve all the Promises
      Promise.all([loadlModelPromise, webcamPromise])
        .then(values => {
          this.detectFromVideoFrame(values[0], this.videoRef.current);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }

  // here we are returning the video frame and canvas to draw,
  // so we are in someway drawing our video "on the go"
  render() {
    return (
      <div> 
        <video
          style={this.styles}
          autoPlay
          muted
          ref={this.videoRef}
          width="720"
          height="600"
        />
        <canvas style={this.styles} ref={this.canvasRef} width="720" height="650" />
      </div>
    );
  }
}

const domContainer = document.querySelector('#root');
ReactDOM.render(React.createElement(App), domContainer);
```

- 更多[Demo地址](http://wqw547243068.github.io/demo)


## 事件检测


### 视频事件检测

【2022-11-8】[AI视频事件检测系统—JXVA8000系列](https://mp.weixin.qq.com/s/wpB_7dwfqc4sjdrRaWKARw)

[捷迅技术](http://www.ettcjx.com/jiejuefangan/145.html)“JXVA”系列产品基于AI人工智能的深度学习算法以及GPU技术，对视频图像事件进行分析识别。利用**视频大数据**开展视频智能化应用服务实现对高速公路的**交通事件**和**交通态势**进行实时、精准检测
- ![](http://www.ettcjx.com/uploads/ueditor/20211005/1-21100522404c39.jpg)

对交通道路正常交通秩序的事件进行**实时检测**，及时发现行人、车辆、物品等异常行为，并进行全客户端实时告警。实现对高速公路的交通事件和交通态势进行实时、精准检测，事件检测精准度达99%。对接高速公路车道监控摄像机的**视频流**，获取瞬间截面车流信息，为管理者提供实时的车流信息，为后续交通大数据的统计和预测做数据储备。

核心功能
- 交通事件分析
- 交通态势分析
- 路面智能养护
- 路网事件分析

优点
- ◆ 识别准确率高：识别准确率高达96%以上
- ◆ 自学习、自优化、越用越智能
  - 具备在线自动学习能力，模型上线使用之后识别准确率不断提高
- ◆ 识别事件类型多
  - 对道路行人、违停、拥堵、逆行、压线、超速、慢行、抛洒物等多种交通事件进行检测

交通事件检测功能点
- 停车
- 行人
- 遗留物
- 事故
- 拥堵
- 非机动车
- 变道检测
- 违规逆行

交通态势分析
- 交通流量检测
- 平均车速检测
- 排队长度检测
- 车道空间占有率

摄像头智能巡检
- 视频缺失
- 视频遮挡
- 视频卡顿
- 视频模糊
- 色彩失真
- 异常抖动


## 卡尔曼滤波

【2022-8-25】[图说卡尔曼滤波，一份通俗易懂的教程](https://zhuanlan.zhihu.com/p/39912633)

`卡尔曼滤波`（Kalman filter）是一种高效的**自回归**滤波器，它能在存在诸多不确定性情况的组合信息中估计动态系统的状态，是一种强大的、通用性极强的工具。它的提出者 鲁道夫.E.卡尔曼，在一次访问NASA埃姆斯研究中心时，发现这种方法能帮助解决阿波罗计划的轨道预测问题，后来NASA在阿波罗飞船的导航系统中确实也用到了这个滤波器。最终，飞船正确驶向月球，完成了人类历史上的第一次登月。

### 滤波器

【2022-8-25】[滤波器（Filter）](https://zhuanlan.zhihu.com/p/55543887)
- 对特定频率进行有效提取，并对提取部分进行特定的处理（增益，衰减，滤除）的动作被叫做滤波。
- 在混音领域中，最常用的滤波器类型有三种：`通过式`（Pass），`搁架式`（Shelving）和`参量式`（Parametric）。滤波器都有一个叫`参考频率`（Reference Frequency）的东西，在不同类型的滤波器中，具体的叫法会有所不同。

通过式滤波器可以让参考频率一侧的频率成分完全通过该滤波器，同时对另一侧的频率成分做线性的衰减，用白话讲就是，一边让通过，一边逐渐被滤除。在信号学中，通过的区域被称为通带，滤除的区域被叫做阻带（图1）。另外，在通过式滤波器中，参考频率通常被称为截止频率。
- 高通滤波器（high-pass filters）：顾名思义，让截止频率后的高频区域通过，另一侧滤除，通常被简称为HPF(参考图1)。
- 低通滤波器（low-pass filters）：让截止频率前的低频区域通过，另一侧滤除，通常被简称为LPF（参考图1）。
- ![](https://pic3.zhimg.com/80/v2-5ee70c507ca9e708366e914082f20aa2_1440w.jpg)

滤波器
- 只要是存在不确定信息的动态系统，卡尔曼滤波就可以对系统下一步要做什么做出有根据的推测。即便有噪声信息干扰，卡尔曼滤波通常也能很好的弄清楚究竟发生了什么，找出现象间不易察觉的相关性。
- 卡尔曼滤波非常适合不断变化的系统，它的优点还有内存占用较小（只需保留前一个状态）、速度快，是实时问题和嵌入式系统的理想选择。

### 示例：机器人导航

一个树林里四处溜达的小机器人，为了让它实现导航，机器人需要知道自己所处的位置。即机器人有一个包含**位置**信息和**速度**信息的状态
- 小机器人装有GPS传感器，定位精度10米
- 这个示例中的状态是位置和速度，其他问题里可以是水箱里的液体体积、汽车引擎温度、触摸板上指尖的位置，或者其他任何数据。

如何预测机器人移动？把指令发送给控制轮子的马达
- 如果这一刻它始终朝一个方向前进，没有遇到任何障碍物，那么下一刻它可能会继续坚持这个路线。
- 但是机器人对自己的状态不是全知的：可能会逆风行驶，轮子打滑，滚落颠簸地形…… 所以车轮转动次数并不能完全代表实际行驶距离，基于这个距离的预测也不完美。

这个问题下，GPS为提供了一些关于状态的信息是间接的、不准确的；预测提供了关于机器人轨迹的信息，但那也是间接的、不准确的。

但以上就是能够获得的全部信息，在此基础上能否给出一个完整预测，让它的准确度比机器人搜集的单次预测汇总更高？卡尔曼滤波，这个问题可以迎刃而解。

卡尔曼滤波假设两个变量（位置和速度）都是随机且符合高斯分布。每个变量都有一个均值 u，它是随机分布的中心；有一个方差 δ，它衡量组合的不确定性。

|||
|---|---|
|![](https://pic1.zhimg.com/80/v2-ebb864b7af322d063c9e75b79d28957c_1440w.jpg)|![](https://pic4.zhimg.com/80/v2-d474e950b50b865fec1cd454b3059b57_1440w.jpg)|

<center>
<img src="https://pic1.zhimg.com/80/v2-ebb864b7af322d063c9e75b79d28957c_1440w.jpg" width=00/>
<img src="https://pic4.zhimg.com/80/v2-d474e950b50b865fec1cd454b3059b57_1440w.jpg" width=200/>
</center>

- 左图里，位置和速度是不相关的，这意味着不能从一个变量推测另一个变量
- 右图里，相关

如果基于旧位置估计新位置，会产生这两个结论：
- 如果速度很快，机器人可能移动得更远，所以得到的位置会更远；
- 如果速度很慢，机器人就走不了那么远。

这种关系对`目标跟踪`来说非常重要，因为它提供了更多信息：一个可以衡量可能性的标准。这就是卡尔曼滤波的目标：<font color='blue'>从不确定信息中挤出尽可能多的信息！</font>

为了捕获这种相关性，用`协方差矩阵`。矩阵的每个值是第i个变量和第j个变量之间的相关程度（由于矩阵是对称的，i和j的位置可以随便交换）。用 Σ 表示协方差矩阵，在这个例子中，就是Σij。
- ![](https://pic1.zhimg.com/80/v2-c0d94558ba4ee781291cefc855ea53f0_1440w.jpg)

# 姿态识别


## 数据集

【2024-4-22】[人体姿态识别这9个数据集](https://zhuanlan.zhihu.com/p/392326330),

### （1）HiEve数据集

数据集图片：[原文](https://zhuanlan.zhihu.com/p/392326330)

•在以人为中心的分析和了解复杂事件中，鼓励并加快新技术的开发。

•在“复杂事件中的大型以人为中心的视觉分析”方面培养新的思想和方向。

数据集内容：HiEve数据集，主要包括在各种人群和复杂事件（包括地铁上下车，碰撞，战斗

和地震逃生）中，以人为中心的非常具有挑战性和现实性的任务。

数据集数量：HiEve数据集包括当前最大的姿势数（> 1M），最大的复杂事件动作标签的数量（> 56k），并且是具有最长期限的轨迹的最大数量之一（平均轨迹长度> 480）。

数据集功能：人体检测、姿态识别、目标追踪、动作识别

下载链接：点击查看


### （2）MPII Human Pose数据集

数据集图片：[原文](https://zhuanlan.zhihu.com/p/392326330)

数据集内容：MPII Human Pose数据集，是用于评估人体姿势识别的数据集。

数据集涵盖了410种人类活动，并且每个图像都带有活动标签。每个图像都是从YouTube视频中提取的，并提供了之前和之后的未注释帧。

此外，对于测试集，我们标注了丰富的注释，包括身体部位遮挡以及3D躯干和头部方向。

数据集数量：该数据集包含约 25K图像，其中对超过4万名人体进行关节标注。

数据集功能：姿态识别

下载链接：点击查看

### （3）CrowdPose数据集

数据集图片：[原文](https://zhuanlan.zhihu.com/p/392326330)

数据集内容：CrowdPose数据集是一个用于拥挤场景姿势估计的新基准数据集，可用于拥挤场景下姿势估计问题。

数据集功能：姿态识别

下载链接：点击查看


### （4）Human3.6M

数据集图片：[原文](https://zhuanlan.zhihu.com/p/392326330)

数据集内容：Human3.6M数据集是一个3D人体姿态识别的数据集，通过4个经过校准的摄像机拍摄获得，对于3D人体的24个部位位置和关节角度都有标注。

数据集数量：Human3.6M数据集包含360万个3D人体姿势图像，11名专业演员（男6名，女5名），17个场景（讨论，吸烟，拍照，通电话...）。

数据集功能：姿态识别、3维重建

下载链接：点击查看

### （5）PedX数据集

数据集图片：[原文](https://zhuanlan.zhihu.com/p/392326330)


数据集内容：PedX 数据集是一个在复杂的城市交叉路口，对于行人进行采集的大规模多模式数据集。

该数据集提供高分辨率的立体图像，和具有手动2D和自动3D注释的LiDAR数据。此外，数据是使用两对立体相机和四个Velodyne LiDAR传感器进行的采集。

数据集功能：人体分割、姿态识别、人体检测

下载链接：点击查看



### （6）SURREAL数据集

数据集图片：[原文](https://zhuanlan.zhihu.com/p/392326330)


数据集内容：SURREAL数据集是一个大规模人造姿态识别数据集，对于RGB视频，对多种状态进行标注：深度信息，身体部位，光流，2D / 3D姿势等。这些图像是在形状，纹理，视点和姿势有很大变化的情况下，对人物的真实渲染。

数据集数量：数据集包含600万帧合成人体数据

数据集功能：姿态识别、人体分割

下载链接：点击查看

### （7）Mo2Cap2数据集

数据集图片：[原文](https://zhuanlan.zhihu.com/p/392326330)

数据集内容：硬件设置的移动性，在各种无限制的日常活动中，对3D人体姿势估计的稳定性会有影响。

因此，在Mo2Cap2数据集中，将头部的棒球帽，安装上一个鱼眼镜头类型的，高质量姿势估计设备。

除了新颖的硬件设置，该数据集主要贡献是：

（1）大型的自顶向下的鱼眼图像地面，实况训练数据集；

（2）一种新颖的3D姿态估计方法，该方法考虑了以自我为中心的独特属性。与现有算法基准相比，可以实现了更低的3D关节误差以及更好的2D覆盖。

数据集功能：姿态估计

下载链接：点击查看

### （8）DensePose数据集

数据集图片：[原文](https://zhuanlan.zhihu.com/p/392326330)

数据集内容：DensePose数据集是户外的密集人体姿势估计数据集，目的在于建立从2D图像到人体表面的多关键点密集对应关系。标注过程主要分为两个阶段：
- 第一阶段：标注人员会标注出身体部位，可见的对应区域。当然对于后面的身体部位，标注人员会进行估算标注。
- 第二阶段：使用一组大致等距的关键点，对每个零件区域进行采样，并要求标注人员将这些点与表面相对应，从而得到最终的标注信息。

数据集数量：DensePose数据集，对5万个人进行了标注，超过500万个标注信息。

数据集功能：姿态识别、人体分割

下载链接：点击查看

### （9）PoseTrack 数据集

数据集图片：[原文](https://zhuanlan.zhihu.com/p/392326330)

数据集内容：PoseTrack 数据集是用于人体姿势估计和视频中的关节跟踪的大型数据集，主要应用于两种挑战：“多人姿势估计”和“多人姿势跟踪”。

数据集数量：数据集中包含1356个视频序列，46000张标注的视频帧，276000个人体姿势标注信息。

数据集功能：姿态估计、姿态跟踪

下载链接：点击查看


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

* **D3S:** Alan Lukežič, Jiří Matas, Matej Kristan.<br />
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

* **CDTB:** Alan Lukežič, Ugur Kart, Jani Käpylä, Ahmed Durmush, Joni-Kristian Kämäräinen, Jiří Matas, Matej Kristan. <br />

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


# 结束


