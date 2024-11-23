---
layout: post
title:  "数字图像处理-Image Processing"
date:   2019-11-01 16:52:00
categories: 计算机视觉
tags: 计算机视觉  opencv 数字图像 滤波 三维 水印 sam 马赛克
excerpt: 图像处理技术总结
mathjax: true
permalink: /image
---

* content
{:toc}


# 数字图像处理


## 基础知识

《数字图像处理》，冈萨雷斯第三版，MATLAB实践
- 《数字图像处理》冈萨雷斯（第四版）[读书笔记目录](https://zhuanlan.zhihu.com/p/569167720)
- [北大ppt课件](https://wenku.baidu.com/view/055297b327fff705cc1755270722192e45365883.html?_wkts_=1672129716473), 百度文库版
- github上的[课件资料:数字图像处理](https://github.com/fei-hdu/courses/tree/main/%E6%95%B0%E5%AD%97%E5%9B%BE%E5%83%8F%E5%A4%84%E7%90%86/2022), 杭州电子科技大学，[高飞](https://aiart.live/)
- 计算机视觉[ppt资料](https://github.com/fei-hdu/courses/tree/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89)


目录
- 第一章 概述
- 第二章 图像处理知识点全面整理
- 第三章 灰度变换与空间滤波知识点整理
- 第四章 频率域图像处理知识点整理
- 第五章 图像复原与重建知识点整理
- 第六章 彩色图像处理基础

### 灰度图

图像通常分为彩色图像和灰度图像两种。
- 在灰度图像中，每个像素都只有**一个**分量用来表示该像素的灰度值。这个分量就是该点的亮度值。
  - 常用的表示像素值所需的数据长度有8 bit或10 bit两种，即图像的位深为8 bit（256）或10 bit（1024）。
- 二值图
  - 灰度图有过度，二值图没有过渡，只有两种0(黑)、1(白)
- 在彩色图像中，每个像素都由**多个**颜色分量组成；每个颜色分量被称为一个通道（Channel）。
  - 图像中所有像素的通道数是一致的，即每个通道都可以表示为一幅与原图像内容相同但颜色不同的分量图像。
  - 以RGB格式的彩色图像为例，一幅完整的图像可以被分割为蓝（B分量）、绿（G分量）、红（R分量）三基色的单色图
  - ![](https://pic2.zhimg.com/80/v2-55fa93deb68f2b99370953a3ea7b8ea1_720w.webp)

RGB图像的宽、高为1920 像素×1080 像素，每个颜色通道的图像位深为 8 bit，则图像的数据体积为1920×1080×3×8bit，即49,766,400bit，约为5.93MB左右。

注： 
- ② 1 Byte＝8bit（位）。
- ③ 1KB＝1024Byte（字节）
- ④ 1 MB＝1024KB

![](https://pic4.zhimg.com/80/v2-627bf6d9d2f637442d2346958e67420b_720w.webp)

### 颜色空间

![](https://pic2.zhimg.com/80/v2-12c573c72e81a5be358de22a5d683675_720w.webp)

`颜色空间`（彩色模型、色彩空间、 彩色系统etc）是对色彩的一种描述方式，定义有很多种，区别在于面向不同的应用背景。
- 显示器中采用的`RGB`颜色空间是基于**物体发光**定义的（RGB正好对应光的三原色：Red，Green，Blue）；
- 工业印刷中常用的`CMY`颜色空间是基于**光反射**定义的（CMY对应了绘画中的三原色：Cyan，Magenta，Yellow）；
- `HSV`、`HSL`两个颜色空间都是从**人视觉**的直观反映而提出来的（H是色调，S是饱和度，I是强度）。

#### RGB（加法混色）

RGB颜色空间 基于颜色的**加法混色**原理，从黑色不断叠加Red，Green，Blue的颜色，最终可以得到白色光。 
- 将R、G、B三个通道作为笛卡尔坐标系中的X、Y、Z轴，就得到了一种对于颜色的空间描述
- ![](https://i0.hdslb.com/bfs/article/347f4ac7d52d301eb2560fc24c2394d99abad0e5.png@675w_635h_progressive.webp)

计算机中编程RGB每一个分量值都用8位（bit）表示，可以产生256*256*256=16777216中颜色，这就是经常所说的“24位真彩色”。 

作者：[unity_某某师_高锦锦](https://www.bilibili.com/read/cv5841645/)

#### CMY（减法混色）

相比于`RGB`，`CMY`（CMYK）颜色空间是另一种基于颜色**减法混色**原理的颜色模型。
- 在工业印刷中它描述的是需要在白色介质上使用何种油墨，通过光的**反射**显示出颜色的模型。
- CMYK描述的是`青`，`品红`，`黄`和`黑`四种油墨的数值。
- ![](https://i0.hdslb.com/bfs/article/20eefed4bae71f1f107b4519b029395d9dca9d93.png@300w_285h_progressive.webp)

打印机彩打时，会发现屏幕上看见的图像和实际打印出来的图像颜色不一样。
- 体现了肉眼的量化能力很好
- 打印机采用了不同的CMY颜色空间（映射关系）

CMYK颜色空间的颜色值与RGB颜色空间中的取值可以通过线性变换相互转换。

#### HSV（人视觉）

`HSV`颜色空间是根据颜色的直观特性, 由A. R. Smith在1978年创建的一种颜色空间, 也称`六角锥体模型`(Hexcone Model)。
- `RGB`和`CMY`颜色模型都是面向**硬件**的
- 而`HSV`（Hue Saturation Value）颜色模型是面向**用户**的。

这个模型中颜色的参数分别是：`色调`（H：hue），`饱和度`（S：saturation），`亮度`（V：value）。
- 这是根据人观察色彩的生理特征而提出的颜色模型
- 人的视觉系统对亮度的敏感度要强于色彩值，这也是为什么计算机视觉中通常使用灰度即亮度图像来处理的原因之一。

- 色调H：用角度度量，取值范围为0°～360°，从红色开始按逆时针方向计算，红色为0°，绿色为120°,蓝色为240°。它们的补色是：黄色为60°，青色为180°,品红为300°；
- 饱和度S：取值范围为0.0～1.0；
- 亮度V：取值范围为0.0(黑色)～1.0(白色)。

HSV模型的三维表示从RGB立方体演化而来。设想从RGB沿立方体对角线的白色顶点向黑色顶点观察，就可以看到立方体的六边形外形。六边形边界表示色彩，水平轴表示纯度，明度沿垂直轴测量。与加法减法混色的术语相比，使用色相，饱和度等概念描述色彩更自然直观。
- ![](https://i0.hdslb.com/bfs/article/e9e72c7ba0963c50c0d6b5cbe9b4bdf0a2681d72.png@942w_942h_progressive.webp)

HSL颜色空间与HSV类似，只不过把V：Value替换为了L：Lightness。这两种表示在用目的上类似，但在方法上有区别。二者在数学上都是圆柱，但HSV（色相，饱和度，色调）在概念上可以被认为是颜色的倒圆锥体（黑点在下顶点，白色在上底面圆心），HSL在概念上表示了一个双圆锥体和圆球体（白色在上顶点，黑色在下顶点，最大横切面的圆心是半程灰色）。注意尽管在HSL和HSV中“色相”指称相同的性质，它们的“饱和度”的定义是明显不同的。对于一些人，HSL更好的反映了“饱和度”和“亮度”作为两个独立参数的直觉观念，但是对于另一些人，它的饱和度定义是错误的，因为非常柔和的几乎白色的颜色在HSL可以被定义为是完全饱和的。对于HSV还是HSL更适合于人类用户界面是有争议的。 作者：unity_某某师_高锦锦 https://www.bilibili.com/read/cv5841645/ 出处：bilibili

#### 颜色空间转换

颜色空间之间的转换关系可以分类两类：
- 一类是颜色空间之间可以直接变换；
- 另一类是颜色空间之间不能直接转换，它们之间的变换需要通过借助其他颜色空间的过渡来实现，如，RGB和CIE L*a*b*。
- ![](https://pic2.zhimg.com/80/v2-80732f19238cdd34cbd04ac0f63e0cb9_720w.webp)

### 图像表示

[数字图像与模拟图像](https://zhuanlan.zhihu.com/p/252635549)

#### 模拟图像

（1）模拟图像
- `模拟图像`：在图像处理中，像纸质照片、电视模拟图像等，这种通过某种物理量（如光、电等）的强弱变化来记录图像亮度信息的图像。
- 特点：物理量的变化是**连续**的。

#### 数字图像

（2）数字图像
- `数字图像`：用一个数字阵列来表达客观物体的图像，离散采样点的集合，每个点具有其各自的属性。
- 特点：把**连续**模拟图像离散化成规则网格，并用计算机以数字的方式来记录图像上各网格点的亮度信息的图像。

小结：
- 一切肉眼能看见的，都是模拟图像（投影仪透出到幕布上的PPT也是模拟图像）。
- 而数字图像肉眼看不见，本质就是一个存储数字的矩阵，一团数据。

数码相机屏幕上呈现的图像是模拟图像。但是你看见的图像是你的相机把经过了光学透镜的模拟图像（光信号），先转化为电信号存储为你内存卡上的一个图片文件（模数转换），即是一个数字图像（在内存里存着，你看不见），然后经过数字图像上记录的信息经过相应颜色空间的映射（数模转换），最后又以光信号的方式呈现在相机的监视屏幕上（又变成模拟图像了）。

数字图像呈现在现实世界中（不论黑白/彩色）时，这个图像究竟是数字图像还是模拟图像？答案当然是模拟图像

#### 模数转换 or 数模转换

数字图像与模拟图像转换
- ![img](https://pic1.zhimg.com/80/v2-35da1f8acba8c338f5ff7afba5acebe8_720w.webp)
- 数字相机经过了模数转换的过程之后，实际是将现实世界的连续的以物理量（比如光）呈现的图像以一定的分辨率（像素）离散化了

#### 遥感图像

遥感图像都是有着一定的大小的，比如3000像素×5000像素。而空间分辨率即是指图片中的每一个像素代表的实际空间大小，比如250m×250m。


### 图像处理-基本步骤

图像处理[基本步骤](https://zhuanlan.zhihu.com/p/558711657)
- （1）图像获取
- （2）图像**增强**，对图像进行某种操作，使其在某种应用中比原图像更能得到合适的结果。
- （3）图像**复原**，改进图像外观，图像增强技术是主观的，图像复原是客观的。复原技术倾向于以图像退化的数学或概率模型为基础，而增强技术以好的增强效果这种主观偏好为基础
- （4）**彩色图像**处理
- （5）**小波变换**和其他**图像变换**，小波是以不同分辨率来表示图像的基础，小波变换可应用与图像压缩和金字塔特征表示。
- （6）**压缩**是指减少图像存储量或降低传输图像的带宽的处理。
- （7）**形态学**处理是提取图像中用于表示和描述形状的成分处理工具。
- （8）**分割**可以将一幅图像或分为各个组成部分或目标。
- （9）**特征提取**，在分割后一步进行，从分割中获取组成图像区域的像素的集合。特征提取包括特征检测和特征描述。特征检测是指寻找一幅图像中的特征、区域或边界。特征描述是指对检测到的特征规定量化属性。
- (10) 图像**模式分类**是指根据目标特征描述对子目标属于标记的过程。

总结：[img](https://pic4.zhimg.com/80/v2-2c50e078dc083216a5ea78338cb2a073_1440w.webp), [中文](https://pic1.zhimg.com/80/v2-17417fabe9df8bf82f62e1bd26921780_1440w.webp)
- ![](https://pic4.zhimg.com/80/v2-2c50e078dc083216a5ea78338cb2a073_1440w.webp)
- ![](https://pic1.zhimg.com/80/v2-17417fabe9df8bf82f62e1bd26921780_1440w.webp)


### 图像处理-知识点

数字图像处理
1. 模拟图像和数字图像
  - `模拟图像`指空间坐标和亮度都是连续变化
  - `数字图像`是一种空间坐标和灰度均不连续，用离散数字表示的图像
2. 数字图像处理系统组成
  - `采集`、`显示`、`存储`、`通信`、`图像处理与分析`五个模块
3. 相比模拟图像处理，数字图像处理的优点
  - 精度高，再现性好，灵活性、通用性强
4. 图像数字化步骤：`采样` -> `量化`
  - `采样`：将空间上连续的图像变换成离散点。圆，椭圆，正方，长方。采样间隔大，像素少，空间分辨率低。
  - `量化`：将像素灰度变换成离散的整数值。量化等级越多，层次越丰富，灰度分辨率越高，但数据量大。
5. `灰度直方图`：一幅图像中各灰度等级像素出现的频率之间的关系
  - 反应图像灰度的分布情况，不反映像素位置，
  - 应用：判断图像量化是否恰当，确定图像**二值化**阀值，计算图像中物体面积，
6. 图像变换目的：使图像处理问题简化，有利于图像特征提取，有利于从概念上增强对图像信息的理解
7. 图像变换算法：`二维傅立叶`变换，`沃尔什—哈达玛`变换，`哈尔`变换，`小波`变换
  - 二维傅立叶后的频谱：四角低频（反映大概样貌），中央高频（反应细节）
8. 图像增强不是以图像保真度为原则，而是通过处理设法有选择地突出，便于人或机器分析某些感兴趣的信息，抑制一些无用信息。
9. 图像增强方法可分为`空间域`（直接对像素灰度操作）和`频域`（对图像经傅立叶变换后的频谱操作）
  - `空间域`：
    - 灰度级校正，灰度变换，直方图修正法；
    - 局部平滑，最大均匀性平滑；
    - 阶梯锐化，Laplacian增强算子
  - `频域`： 
    - `平滑`：**低通**滤波器
    - `锐化`：**高通**滤波器
  - `彩色增强`：
    - 伪彩色增强：密度分割 
    - 彩色图像增强：彩色平衡
10. 图像复原与重建：图像增强可以不顾增强后是否失真，图像复原是要恢复原形
11. 图像恢复方法：
  - 1. 代数恢复：无约束复原 
  - 2. 频率域恢复：逆滤波恢复法 ，维纳滤波器
  - 3. 几何校正：像素灰度内插（最近邻元法，双线性内插）
12. 几种图像退化：模糊、失真、有噪声等
13. 保真度准则：描述解码图像相对原始图像偏离程度的测度：客观保真度准则+主观保真度准则
14. 图像压缩技术：有损压缩和无损压缩
  - `无损`压缩：霍夫曼编码，香农编码，算数编码
  - `有损`压缩：预测编码（线性预测和非线性预测），变换编码
15. 无损和有损预测编码算法不同之处？
  - 无损编码中删除的仅仅是图像数据中冗余的数据，经解码重建的图像没有任何失真。
  - 有损编码是指解码重建的图像与原图像相比有失真，不能精确的复原，但视觉效果上基本相同，是实现高压缩比的编码方式。
16. `图像分割`是指把图像分成互不重叠的区域并提取出感兴趣目标的技术
17. 按分割途径不同可以分为：
  - 1. 基于边缘提取的分割算法
  - 2. 区域分割算法 
  - 3. 区域增长（简单区域扩张法、质心形增长）
  - 4. 分裂—合并分割算法
18. 几个常用的边缘检测算子：
  - Canny 算子
  - Laplacian算子
  - Sobel 算子
19. Hough变换检测直线和圆算法


## 图像处理内容

包含
- · 基本概念：亮度、对比度、分辨率、饱和度、尖锐化等基础概念
- · 图像灰度变换：线性、分段线性、对数、反对数、幂律(伽马)变换等
- · 图像滤波：线性滤波和非线性滤波、空间滤波和频率域滤波，均值滤波、中值滤波、高斯滤波、逆滤波、维纳滤波等各种图像的基本操作

高级的图像操作:
- · 文本图像的倾斜矫正方法：霍夫变换、透视变换等
- · 图像边缘检测：canny算子、sobel算子、Laplace算子、Scharr滤波器等

## 图像增强

图像增强是对图像进行处理，使其比原始图像更适合于特定的应用，它需要与实际应用相结合。对于图像的某些特征如边缘、轮廓、对比度等，图像增强是进行强调或锐化，以便于显示、观察或进一步分析与处理

部分图像会出现整体较**暗**或较**亮**的情况，这是由于图片的**灰度值范围较小**，即**对比度低**。
- 实际应用中，通过绘制图片的**灰度直方图**，可以判断图片的灰度值分布，区分其对比度高低。
- 对于对比度较低的图片，可以通过一定的算法来增强其对比度。常用的方法有`线性变换`，`伽马变换`，`直方图均衡化`，`局部自适应直方图均衡化`等。

### 灰度直方图

绘制灰度分布曲线图，灰度分布直方图和两者叠加图形
- ![](https://img2018.cnblogs.com/blog/1483773/201906/1483773-20190612223116340-827573379.png)



```py
#coding:utf-8

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
                
img = cv.imread(r"C:\Users\Administrator\Desktop\maze.png",0)

hist = cv.calcHist([img],[0],None,[256],[0,256])

plt.subplot(1,3,1),plt.plot(hist,color="r"),plt.axis([0,256,0,np.max(hist)])
plt.xlabel("gray level")
plt.ylabel("number of pixels")

plt.subplot(1,3,2),plt.hist(img.ravel(),bins=256,range=[0,256]),plt.xlim([0,256])
plt.xlabel("gray level")
plt.ylabel("number of pixels")

plt.subplot(1,3,3)
plt.plot(hist,color="r"),plt.axis([0,256,0,np.max(hist)])
plt.hist(img.ravel(),bins=256,range=[0,256]),plt.xlim([0,256])
plt.xlabel("gray level")
plt.ylabel("number of pixels")

plt.show()
```

numpy 绘制

```py
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


img = cv.imread(r"C:\Users\Administrator\Desktop\maze.png",0)
histogram,bins = np.histogram(img,bins=256,range=[0,256])
print(histogram)
plt.plot(histogram,color="g")
plt.axis([0,256,0,np.max(histogram)])
plt.xlabel("gray level")
plt.ylabel("number of pixels")
plt.show()
```

matplotlib 绘制

```py
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img = cv.imread(r"C:\Users\Administrator\Desktop\maze.png",0)
rows,cols = img.shape
hist = img.reshape(rows*cols)
histogram,bins,patch = plt.hist(hist,256,facecolor="green",histtype="bar") #histogram即为统计出的灰度值分布
plt.xlabel("gray level")
plt.ylabel("number of pixels")
plt.axis([0,255,0,np.max(histogram)])
plt.show()
```

### 图像增强方法

对比度增强: [详见](https://www.cnblogs.com/silence-cho/p/11006958.html)
- 将图片的灰度范围拉宽，如图片灰度分布范围在\[50,150]之间，将其范围拉升到\[0,256]之间。
- 线性变换，直方图正规化，伽马变换，全局直方图均衡化，限制对比度自适应直方图均衡化等算法。

图像增强方法
- 空间域
  - 点运算：灰度变换、直方图修正法
  - 区域运算：平滑、锐化
    - 平滑：平滑算法有邻域平均法、中指滤波、边界保持类滤波等。
    - 锐化
- 频率域
  - 高通滤波
  - 低通滤波
  - 同态滤波增强
- 彩色增强
  - 假彩色增强
  - 伪彩色增强
  - 彩色变换增强
- 代数运算


[图像平滑之均值滤波、方框滤波、高斯滤波及中值滤波](https://www.toutiao.com/article/6836292532251394567)

图像处理中噪声：主要有三种：
- 椒盐噪声（Salt & Pepper）：含有随机出现的黑白亮度值。
- 脉冲噪声：只含有随机的正脉冲和负脉冲噪声。
- 高斯噪声：含有亮度服从高斯或正态分布的噪声。高斯噪声是很多传感器噪声的模型，如摄像机的电子干扰噪声。

#### 滤波

滤波器主要两类：线性和非线性
- 线性滤波器：使用连续窗函数内像素加权和来实现滤波，同一模式的权重因子可以作用在每一个窗口内，即线性滤波器是空间不变的。
  - 如果图像的不同部分使用不同的滤波权重因子，线性滤波器是空间可变的。因此可以使用卷积模板来实现滤波。线性滤波器对去除高斯噪声有很好的效果。常用的线性滤波器有均值滤波器和高斯平滑滤波器。
  - (1) 均值滤波器：最简单均值滤波器是局部均值运算，即每一个像素只用其局部邻域内所有值的平均值来置换。
  - (2) 高斯平滑滤波器是一类根据高斯函数的形状来选择权值的线性滤波器。 高斯平滑滤波器对去除服从正态分布的噪声是很有效的。
- 非线性滤波器:
  - (1) 中值滤波器:均值滤波和高斯滤波运算主要问题是有可能模糊图像中尖锐不连续的部分。中值滤波器的基本思想使用像素点邻域灰度值的中值来代替该像素点的灰度值，它可以去除脉冲噪声、椒盐噪声同时保留图像边缘细节。中值滤波不依赖于邻域内与典型值差别很大的值，处理过程不进行加权运算。中值滤波在一定条件下可以克服线性滤波器所造成的图像细节模糊，而对滤除脉冲干扰很有效。
  - (2) 边缘保持滤波器:由于均值滤波：平滑图像外还可能导致图像边缘模糊和中值滤波：去除脉冲噪声的同时可能将图像中的线条细节滤除。边缘保持滤波器是在综合考虑了均值滤波器和中值滤波器的优缺点后发展起来的，它的特点是：滤波器在除噪声脉冲的同时，又不至于使图像边缘十分模糊。

#### 加噪声

增加噪声

```py
# -*- coding:utf-8 -*-
import cv2
import numpy as np
#读取图片
img = cv2.imread("test.jpg", cv2.IMREAD_UNCHANGED)
rows, cols, chn = img.shape
#加噪声
for i in range(5000):  
  x = np.random.randint(0, rows)  
  y = np.random.randint(0, cols)  
  img[x,y,:] = 255
cv2.imshow("noise", img)
#等待显示
cv2.waitKey(0)
cv2.destroyAllWindows
```

![](https://p3-sign.toutiaoimg.com/pgc-image/S1PQANUHUzvv2v~noop.image?_iz=58558&from=article.pc_detail&x-expires=1672886951&x-signature=aImTitbc%2F%2Bd4cj0q6LgP%2B6ftUV8%3D)


#### 均值滤波

均值滤波
- 均值滤波是指任意一点的像素值，都是周围N*M个像素值的均值。例如下图中，红色点的像素值为蓝色背景区域像素值之和除25。
- ![](https://p3-sign.toutiaoimg.com/pgc-image/S1PQAOWBKmVEju~noop.image?_iz=58558&from=article.pc_detail&x-expires=1672886951&x-signature=A8tTul6nQ8qFr1QM%2BAfB1Y6MA9M%3D)

```py
#encoding:utf-8
import cv2 
import numpy as np 
import matplotlib.pyplot as plt
#读取图片
img = cv2.imread('test01.png')
source = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#均值滤波
result = cv2.blur(source, (5,5)) # 核设置为（10，10）和（20，20）会让图像变得更加模糊
#显示图形
titles = ['Source Image', 'Blur Image'] 
images = [source, result] 
for i in xrange(2):  
  plt.subplot(1,2,i+1)
  plt.imshow(images[i], 'gray')  
  plt.title(titles[i]) 
  plt.xticks([]),plt.yticks([]) 
  plt.show
```

输出结果如下图所示：
- ![](https://p3-sign.toutiaoimg.com/pgc-image/S1PQBHv6oIZHwm~noop.image?_iz=58558&from=article.pc_detail&x-expires=1672886951&x-signature=gko2c3dp3wwoNGu9VhieIRLyBlQ%3D)

#### 方框滤波

方框滤波
- 方框滤波和均值滤波核基本一致，区别是需不需要均一化处理。OpenCV调用boxFilter函数实现方框滤波。函数如下：
- result = cv2.boxFilter(原始图像, 目标图像深度, 核大小, normalize属性)

#### 高斯滤波

高斯滤波
- 为了克服简单局部平均法的弊端(图像模糊)，目前已提出许多保持边缘、细节的局部平滑算法。它们的出发点都集中在如何选择邻域的大小、形状和方向、参数加平均及邻域各店的权重系数等。

图像高斯平滑也是邻域平均的思想对图像进行平滑的一种方法，在图像高斯平滑中，对图像进行平均时，不同位置的像素被赋予了不同的权重。高斯平滑与简单平滑不同，它在对邻域内像素进行平均时，给予不同位置的像素不同的权值

#### 中值滤波

中值滤波
- 在使用邻域平均法去噪的同时也使得边界变得模糊。而中值滤波是非线性的图像处理方法，在去噪的同时可以兼顾到边界信息的保留。选一个含有奇数点的窗口W，将这个窗口在图像上扫描，把窗口中所含的像素点按灰度级的升或降序排列，取位于中间的灰度值来代替该点的灰度值


## 图像分割

- 【2020-7-17】图像分割（Image Segmentation）是计算机视觉领域中的一项重要基础技术，是图像理解中的重要一环。图像分割是将数字图像细分为多个图像子区域的过程，通过简化或改变图像的表示形式，让图像能够更加容易被理解。
   - 图像分割技术自 60 年代数字图像处理诞生开始便有了研究，随着近年来深度学习研究的逐步深入，图像分割技术也随之有了巨大的发展。
   - 早期的图像分割算法不能很好地分割一些具有抽象语义的目标，比如文字、动物、行人、车辆。这是因为早期的图像分割算法基于简单的像素值或一些低层的特征，如边缘、纹理等，人工设计的一些描述很难准确描述这些语义，这一经典问题被称之为“语义鸿沟”。
   - 第三代图像分割很好地避免了人工设计特征带来的“语义鸿沟”，从最初只能基于像素值以及低层特征进行分割，到现在能够完成一些根据高层语义的分割需求。
   - 参考：[基于深度学习的图像分割在高德的实践](https://yqh.aliyun.com/detail/15920?utm_content=g_1000154176)
   - ![](https://p1-tt-ipv6.byteimg.com/img/pgc-image/9811c9fff31a4fe282dbce591f7642b8~tplv-obj:745:306.image)

## 图片小工具

【2022-10-19】[神奇海螺试验场](https://lab.magiconch.com/)出品
- [电子包浆](https://magiconch.com/patina/)，图片赛博做旧
- [梗图生成器](https://x.magiconch.com/)
- [颜色图片识别](https://magiconch.com/nsfw/)
- 切图：[九宫格](https://v.magiconch.com/sns-image)
- [你画我猜](https://draw.magiconch.com/)在线游戏


## 图像动态化

[Live2D](https://www.live2d.com/en/download/cubism/)

Live2D是一种应用于电子游戏的绘图渲染技术，通过一系列的连续图像和人物建模来生成一种类似二维图像的三维模型。对于以动画风格为主的冒险游戏来说非常有用。该技术由日本Guyzware公司开发，Live2D的前身为TORA系统，衍生技术是OIU系统。
- 知乎：[如何看待live2D这项技术？](https://www.zhihu.com/question/28130936)

<video width="620" height="440" controls="controls" autoplay="autoplay">
  <source src="https://vdn.vzuu.com/SD/fc42fe58-2322-11eb-a20b-9a794694b530.mp4" type="video/mp4" />
</video>


## 图像3D化-三维重建

- [2017-9-21]自拍照三维重建[3D Face Reconstruction from a Single Image](http://www.cs.nott.ac.uk/~psxasj/3dme/index.php)
- ![demo](https://cdn.vox-cdn.com/thumbor/fXbE0rbXW6WlcmtB1cKBiTsV1b0=/0x0:482x334/1820x1213/filters:focal(203x129:279x205):no_upscale()/cdn.vox-cdn.com/uploads/chorus_image/image/56734861/3d_mark_take_2.0.gif)
- 【2020-7-23】2D照片转3D的效果，代码：[3d-photo-inpainting](https://github.com/vt-vl-lab/3d-photo-inpainting)
- ![](https://p1-tt-ipv6.byteimg.com/img/pgc-image/54a7f500dc92415f91e0766e2f74c45a~tplv-obj:340:424.image?from=post)
- 【2020-11-18】端到端面部表情合成 Speech-Driven Animation [Github代码](https://github.com/DinoMan/speech-driven-animation)
  - ![](https://github.com/DinoMan/speech-driven-animation/raw/master/example.gif)
- 【2021-3-10】面部表情迁移：吴京+甄子丹 [微博示例](https://video.weibo.com/show?fid=1034:4609199536013325)
- 【2020-12-29】[单张图片三维重建](https://blog.csdn.net/zouxy09/article/details/8083553),Andrew Ng介绍他的两个学生用单幅图像去重构这个场景的三维模型。
   - [斯坦福大学](http://ai.stanford.edu/~asaxena/reconstruction3d/)
      - ![](http://ai.stanford.edu/~asaxena/reconstruction3d/Results/mountain_mesh_small.jpg)
   - [康奈尔大学](http://www.cs.cornell.edu/~asaxena/learningdepth/)

### 图像三维重建算法

【2023-3-19】图像三维重建

截止2022年，一些2D图片三维重建研究工作汇总，英文[视频介绍](https://www.zhihu.com/zvideo/1542654820820869121)

基于深度学习的图像三维重建算法性能较好的主要有：MVSNet、PatchMatchNet、NeuralRecon。
- `MVSNet` 开启了深度学习做三维重建的先河，本质是借鉴基于两张图片cost volume的双目立体匹配的深度估计方法，扩展到多张图片的深度估计，后续系列的改进思路主要是把回归网络改成cascade。
- `PatchMatchNet` 结合了传统PatchMatch算法以及深度学习的优点，是一种以learning-based Patchmatch为主体的cascade结构，主要包括基于FPN的多尺度特征提取、嵌入在cascade结构中的learning-based Patchmatch以及spatial refinement模块
- `NeuralRecon` 一种新的基于单目视频的实时三维场景重建框架，其核心思想是利用三维稀疏卷积和GRU算法，对每个视频片段的稀疏TSDF体进行增量联合重构和融合，这种设计能够实时输出精确的重建。实验表明，NeuralRecon在重建质量和运行速度上都优于现有的方法。


### 视频三维重建

【2023-3-22】NVIDIA [2023 GTC大会](https://www.nvidia.com/gtc/keynote/)，4:45开始看，里面有根据视频生成3D模型的

# 图像处理工具


## pillow

PIL提供了通用的图像处理功能，以及大量的基本图像操作，如图像缩放、裁剪、旋转、颜色转换等。
- [Python 图像处理 Pillow 库](https://zhuanlan.zhihu.com/p/58671158)

Matplotlib提供了强大的绘图功能，其下的pylab/pyplot接口包含很多方便用户创建图像的函数。


### 图像操作

```py
from PIL import Image
import matplotlib.pyplot as plt

image = Image.open('python-logo.png')  # 创建图像实例
# 查看图像实例的属性
print(image.format, image.size, image.mode)
image.show() # 显示图像

img = Image.open("girl.jpg")

plt.figure()
# 子图
plt.subplot(221)
# 原图
plt.imshow(img)
plt.subplot(222)
# 将图像缩放至 256 * 256
plt.imshow(img.resize((256, 256)))
plt.subplot(223)
# 将图像转为灰度图
plt.imshow(img.convert('L'))
plt.subplot(224)
# 旋转图像
plt.imshow(img.rotate(45))
# 保存图像
plt.savefig("tmp.jpg")
plt.show()

```

![](https://img2018.cnblogs.com/blog/1503464/201909/1503464-20190905210234525-1188098313.jpg)


## opencv

【2022-10-7】[opencv-python快速入门篇](https://zhuanlan.zhihu.com/p/44255577)

### opencv简介

opencv 是用于快速处理图像处理、计算机视觉问题的工具，支持多种语言进行开发如c++、python、java等

### Python opencv安装

环境：
- 1、 python3
- 2、 numpy
- 3、 opencv-python

```shell
# 安装numpy
pip install numpy
# 安装opencv-python
pip install opencv-python
```

测试：
- 执行 import cv2

### 图像读取

（1）imread函数：读取数字图像

cv2.imread(path_of_image, intflag)
- 参数一： 需要读入图像的完整路径
- 参数二： 标志以什么形式读入图像，可以选择一下方式：
  - · cv2.IMREAD_COLOR： 加载彩色图像。任何图像的透明度都将被忽略。它是默认标志
  - · cv2.IMREAD_GRAYSCALE：以灰度模式加载图像
  - · cv2.IMREAD_UNCHANGED：保留读取图片原有的颜色通道
    - · 1 ：等同于cv2.IMREAD_COLOR
    - · 0 ：等同于cv2.IMREAD_GRAYSCALE
    - · -1 ：等同于cv2.IMREAD_UNCHANGED

### 图像显示

（2）imshow 函数
- imshow函数作用是在窗口中显示图像，窗口自动适合于图像大小，我们也可以通过imutils模块调整显示图像的窗口的大小。
- 函数官方定义：cv2.imshow(windows_name, image)
  - 参数一： 窗口名称(字符串)
  - 参数二： 图像对象，类型是numpy中的ndarray类型，注：这里可以通过imutils模块改变图像显示大小

```py
import cv2
import numpy as np

raw_img = cv2.imread("liu.jpg")
h, w, _ = raw_img.shape
# 高斯模糊
gaussianBlur = cv2.GaussianBlur(raw_img, (0, 0), 10)
# resize to same scale 缩放
im1 = cv2.resize(raw_img, (200, 200))
cv2.imwrite('lena.bmp',im1)  # 写图像
# 灰度化 Image to Gray Image
gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
# 镜像 Gray Image to Inverted Gray Image
inverted_gray_image = 255 - gray_img
## Blurring The Inverted Gray Image
blurred_inverted_gray_image = cv2.GaussianBlur(inverted_gray_image, (19,19),0)
## Inverting the blurred image
inverted_blurred_image = 255-blurred_inverted_gray_image
### Preparing Photo sketching
sketck = cv2.divide(gray_img, inverted_blurred_image,scale= 256.0)
cv2.imshow("Original Image",img) # 开启第一个窗口
cv2.imshow("Pencil Sketch", sketck) # 开启第二个窗口
# ------ 多图展示 --------
print(raw_img.shape, sketck.shape)
# imgs = np.hstack([img,img2]) # 横向铺开
# imgs = np.vstack([img,img2]) # 纵向铺开
merge = np.hstack((raw_img, gaussianBlur))
cv2.imshow("Pencil Sketch", merge)
# ------ 按ESC退出（默认无关闭按键） -----
k = cv2.waitKey(0)
# 图像出现后必须把光标移动到窗口上再按键才会退出
if k == 27: # ESC键
  cv2.destroyAllWindows()
```

注意
- 不同尺寸、不同颜色（RGB和灰度）不能放在一个窗体中 -- 黑屏

解决办法
- 使用matplotlib

```py
import cv2
import matplotlib.pyplot as plt

# 使用matplotlib展示多张图片
def matplotlib_multi_pic1():
    for i in range(9):
        img = cv2.imread('880.png')
        title="title"+str(i+1)
        #行，列，索引
        plt.subplot(3,3,i+1)
        plt.imshow(img)
        plt.title(title,fontsize=8)
        plt.xticks([])
        plt.yticks([])
    plt.show()
matplotlib_multi_pic1()
```


### 图像写入

（3）imwrite 函数
- imwrite函数检图像保存到本地，官方定义：cv2.imwrite(image_filename, image)
  - 参数一： 保存的图像名称(字符串)
  - 参数二： 图像对象，类型是numpy中的ndarray类型


### 颜色空间

图像颜色主要是由于图像受到外界光照影响随之产生的不同颜色信息，同一个背景物的图像在不同光源照射下产生的不同颜色效果的图像，因此在做图像特征提取和识别过程时，要的是图像的**梯度信息**，也就是图像的本质内容，而**颜色信息**会对梯度信息提取造成一定的干扰，因此会在做图像特征提取和识别前将图像转化为**灰度图**，这样同时也降低了处理的数据量并且增强了处理效果。

图像色彩空间变换函数cv2.cvtColor

函数定义：cv2.cvtColor(input_image, flag)
- 参数一： input_image表示将要变换色彩的图像ndarray对象
- 参数二： 表示图像色彩空间变换的类型，以下介绍常用的两种：
  - · cv2.COLOR_BGR2GRAY： 表示将图像从BGR空间转化成灰度图，最常用
  - · cv2.COLOR_BGR2HSV： 表示将图像从RGB空间转换到HSV空间

如果想查看参数flag的全部类型，请执行以下程序便可查阅，总共有274种空间转换类型：

```python
import cv2
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
print(flags)
```

### 自定义图像

绘图简单图像
- 对于一个长宽分别为w、h的RGB彩色图像来说，每个像素值是由(B、G、R)的一个tuple组成，opencv-python 中每个像素三个值的顺序是B、G、R，而对于灰度图像来说，每个像素对应的便只是一个整数，如果要把像素缩放到0、1，则灰度图像就是二值图像，0便是黑色，1便是白色

```python
import cv2
#这里图像采用的仍旧是上面那个卡通美女啦
rgb_img = cv2.imread('E:/peking_rw/ocr_project/base_prehandle/img/cartoon.jpg')
print(rgb_img.shape)     #(1200, 1600, 3)
print(rgb_img[0, 0])     #[137 124  38]
print(rgb_img[0, 0, 0])  #137

gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
print(gray_img.shape)    #(1200, 1600)
print(gray_img[0, 0])    #100
```

彩色图像的高度height = 1200， 宽度w=1600且通道数为3， 像素(0， 0)的值是(137 124 38)，即R=137, G=124, B=38， 对于灰度图像来说便只是单通道的了

因此(0, 0, 0)便是代表一个黑色像素，(255, 255, 255)便是代表一个白色像素。这么想，B=0, G=0, R=0相当于关闭了颜色通道也就相当于无光照进入，所以图像整个是黑的，而(255, 255, 255)即B=255, G=255, R=255， 相当于打开了B、G、R所有通道光线全部进入，因此便是白色。

#### 图像绘制方法

各种绘制方法
- 直线cv2.line、长方形cv2.rectangle、圆cv2.circle、椭圆cv2.ellipse、多边形cv2.polylines等集合图像绘制函数

公共参数：
- · img： 表示需要进行绘制的图像对象ndarray
- · color： 表示绘制几何图形的颜色，采用BGR即上述说的(B、G、R)
- · thickness： 表示绘制几何图形中线的粗细，默认为1，对于圆、椭圆等封闭图像取-1时是填充图形内部
- · lineType ： 表示绘制几何图形线的类型，默认8-connected线是光滑的，当取cv2.LINE_AA时线呈现锯齿状

##### (1) cv2.line函数

直线绘制函数， 函数官方定义为：
- cv2.line(image, starting, ending, color, thickness, lineType)
- 参数image、color、thickness、lineType分别是上述公共定义，参数starting、ending分别表示线的起点像素坐标、终点像素坐标

##### (2) cv2.rectangle函数

长方形绘制函数，函数官方定义：
- cv2.rectangle(image, top-left, bottom-right, color, thickness, lineType)
- 参数image、color、thickness、lineType分别是上述公共定义，参数top-left、bottom-right分别表示长方形的左上角像素坐标、右下角像素坐标


##### (3) cv2.circle函数
圆形绘制函数，官方定义函数为：
- cv2.circle(image, center, radius, color, thickness, lineType)
- 参数image、color、thickness、lineType分别是上述公共定义，参数center、radius分别表示圆的圆心像素坐标、圆的半径长度，圆绘制函数中当参数thickness = -1 时绘制的是实心圆，当thickness >= 0 时绘制的是空心圆


##### (4) cv2.ellipse函数

椭圆绘制函数，官方定义为：
- cv2.circle(image, center, (major-axis-length, minor-axis-length), angle, startAngle, endAngle, color, thickness, lineType)
- 椭圆的参数较多，首先参数image、color、thickness、lineType分别是上述公共定义，椭圆绘制函数中当参数thickness = -1 时绘制的是实心椭圆，当thickness >= 0 时绘制的是空心椭圆，其他参数如下
  - · center： 表示椭圆中心像素坐标
  - · major-axis-length： 表示椭圆的长轴长度
  - · minor-axis-length： 表示椭圆的短轴长度
  - · angle： 表示椭圆在逆时针方向旋转的角度
  - · startAngle： 表示椭圆从主轴向顺时针方向测量的椭圆弧的起始角度
  - · endAngle： 表示椭圆从主轴向顺时针方向测量的椭圆弧的终止时角度


##### (5) cv2.polylines函数

多边形绘制函数，官方定义函数为：
- cv2.polylines(image, \[point-set], flag, color, thickness, lineType)
- 参数image、color、thickness、lineType分别是上述公共定义，其他参数如下：
  - · \[point-set]： 表示多边形点的集合，如果多边形有m个点，则便是一个m*1*2的数组，表示共m个点
  - · flag： 当flag = True 时，则多边形是封闭的，当flag = False 时，则多边形只是从第一个到最后一个点连线组成的图像，没有封闭


#### 图像绘制示例

```python
import cv2
import numpy as np

img = np.ones((512,512,3), np.uint8)
img = 255*img
img = cv2.line(img, (100,100), (400,400),(255, 0, 0), 5)
img = cv2.rectangle(img,(200, 20),(400,120),(0,255,0),3)
img = cv2.circle(img,(100,400), 50, (0,0,255), 2)
img = cv2.circle(img,(250,400), 50, (0,0,255), 0)
img = cv2.ellipse(img,(256,256),(100,50),0,0,180,(0, 255, 255), -1)
pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
img = cv2.polylines(img,[pts],True,(0, 0, 0), 2)

cv2.imshow('img', img)
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
```

![](https://pic3.zhimg.com/80/v2-37c3e0653291eafc7d16ce071fdf9db6_1440w.webp)

### 像素操作

#### (1) 对图像取反

```python
reverse_img = 255 - gray_img
```

#### (2) 对图像像素线性变换

```python
for i in range(gray_img.shape[0]):
    for j in range(gray_img.shape[1]):
        random_img[i, j] = gray_img[i, j]*1.2
```

![](https://pic4.zhimg.com/80/v2-8fca4ea068a45033056e89236ae1644b_1440w.webp)

完整代码

```python
import cv2
import imutils
import numpy as np

rgb_img = cv2.imread('E:/peking_rw/ocr_project/base_prehandle/img/cartoon.jpg')
gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
reverse_img = 255 - gray_img

random_img = np.zeros((gray_img.shape[0], gray_img.shape[1]), dtype=np.uint8)
for i in range(gray_img.shape[0]):
    for j in range(gray_img.shape[1]):
        random_img[i, j] = gray_img[i, j]*1.2
cv2.imshow('reverse_img', imutils.resize(reverse_img, 800))
cv2.imshow('random_img', imutils.resize(random_img, 800))
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
```

### 窗口销毁

（4）窗口销毁函数
- 当使用imshow函数展示图像时，最后需要在程序中对图像展示窗口进行销毁，否则程序将无法正常终止
- 常用的销毁窗口的函数有下面两个：
  - ① cv2.destroyWindow(windows_name) # 销毁单个特定窗口
    - 参数： 将要销毁的窗口的名字
  - ② cv2.destroyAllWindows() # 销毁全部窗口，无参数

何时销毁窗口？肯定不能图片窗口一出现就将窗口销毁，这样便没法观看窗口，试想有两种方式：
- ① 让窗口停留一段时间然后自动销毁；
- ② 接收指定的命令，如接收指定的键盘敲击然后结束我们想要结束的窗口

以上两种情况都将使用cv2.waitKey函数， 首先产看函数定义：cv2.waitKey(time_of_milliseconds)
- 唯一参数 time_of_milliseconds是整数，可正可负也可是零，含义和操作也不同，分别对应上面说的两种情况
- ① time_of_milliseconds > 0 ：此时time_of_milliseconds表示时间，单位是毫秒，含义表示等待 time_of_milliseconds毫秒后图像将自动销毁
- ② time_of_milliseconds <= 0 ： 此时图像窗口将等待一个键盘敲击，接收到指定的键盘敲击便会进行窗口销毁。我们可以自定义等待敲击的键盘，通过下面的例子进行更好的解释


### 视频处理

[链接](https://blog.csdn.net/ljx1400052550/article/details/107410157)

```py
import cv2
import numpy as np
  
# 定义保存图片函数
# image:要保存的图片名字
# addr；图片地址与相片名字的前部分
# num: 相片，名字的后缀。int 类型
def save_image(image,addr,num):
  address = addr + str(num)+ '.jpg'
  cv2.imwrite(address,image)
  
# 读取视频文件
videoCapture = cv2.VideoCapture("test.mp4")
# 通过摄像头的方式
# videoCapture=cv2.VideoCapture(1)

#读帧
success, frame = videoCapture.read()
i = 0
#设置固定帧率
timeF = 10
j=0
while success :
  i = i + 1
  if (i % timeF == 0):
    j = j + 1
    save_image(frame,'./output/image',j)
    print('save image:',i)
  success, frame = videoCapture.read()
```


opencv按指定时间提取片段：[提取](https://blog.csdn.net/qq_41251963/article/details/123932842)

其它方法
- ffmpeg 工具

```sh
# 按时间窗
ffmpeg  -i ./SN.mp4 -vcodec copy -acodec copy -ss 00:00:00 -to 00:00:05 ./cutout1.mp4 -y
# 按帧截取
ffmpeg -i ./input.mp4 -vf "select=between(n\,20\,200)" -y -acodec copy ./output.mp4

```


### opencv 汇总示例

```python
import numpy as np
import cv2

gray_img = cv2.imread('img/cartoon.jpg', 0)  #加载灰度图像
rgb_img = cv2.imread('img/cartoon.jpg', 1)   #加载RGB彩色图像

cv2.imshow('origin image', rgb_img)   #显示原图
cv2.imshow('origin image', imutils.resize(rgb_img, 800))  #利用imutils模块调整显示图像大小
cv2.imshow('gray image', imutils.resize(gray_img, 800))
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()

cv2.imwrite('rgb_img.jpg', rgb_img)   #将图像保存成jpg文件
cv2.imwrite('gray_img.png', gray_img) #将图像保存成png文件

#表示等待10秒后，将销毁所有图像
if cv2.waitKey(10000):
    cv2.destroyAllWindows()
#表示等待10秒，将销毁窗口名称为'origin image'的图像窗口
if cv2.waitKey(10000):
    cv2.destroyWindow('origin image')
#当指定waitKey(0) == 27时，当敲击键盘 Esc 时便销毁所有窗口
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
#当接收到键盘敲击A时，便销毁名称为'origin image'的图像窗口
if cv2.waitKey(-1) == ord('A'):
    cv2.destroyWindow('origin image')
```

### imutils 工具包

imutils 是在OPenCV基础上的一个封装，达到更为简结的调用OPenCV接口的目的，它可以轻松的实现图像的平移，旋转，缩放，骨架化等一系列的操作。

安装方法

```shell
# 在安装前应确认已安装numpy,scipy,matplotlib和opencv
pip install imutils
# pip install NumPy SciPy opencv-python matplotlib imutils
```

图像操作：[参考](https://walkonnet.com/archives/364235)
- 图像平移
  - 相对于原来的cv，使用imutiles可以直接指定平移的像素，不用构造平移矩阵
  - OpenCV中也提供了图像平移的实现，要先计算平移矩阵，然后利用仿射变换实现平移，在imutils中可直接进行图像的平移。
  - translated = imutils.translate(img,x,y)
- 缩放函数：imutils.resize(img,width=100)
- 图像旋转
  - 逆时针旋转 rotated = imutils.rotate(image, 90)
  - 顺时针旋转 rotated_round = imutils.rotate_bound(image, 90)
- 骨架提取（边缘提取）
  - 骨架提取（边缘提取），是指对图片中的物体进行拓扑骨架(topological skeleton)构建的过程。
  - imutils提供的方法是skeletonize()
- 转RGB
  - img = cv.imread("lion.jpeg") 
  - plt.figure() 
  - plt.imshow(imutils.opencv2matplotlib(img))


### 完整示例


```python
import cv2
#pip install imutils
import imutils
import numpy as np

rgb_img = cv2.imread('/Users/wqw/Desktop/二十面体.png')
# 颜色空间转换：rgb → gray
gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
# -------------
# 总共有274种空间转换类型：
# flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
# print(flags)
# -----------
cv2.imshow('origin image', imutils.resize(rgb_img, 800))
cv2.imshow('gray image', imutils.resize(gray_img, 800))
cv2.imwrite('rgb_img.jpg', rgb_img)
cv2.imwrite('gray_img.png', gray_img)

# 等待一定时间自动销毁图像窗口
#if cv2.waitKey(10000):
#    cv2.destroyAllWindows()
#if cv2.waitKey(10000):
#    cv2.destroyWindow('origin image')
# 接收特定键盘销毁图像窗口
#if cv2.waitKey(-1) == ord('A'):
#    cv2.destroyWindow('origin image')
if cv2.waitKey(0) == 27: # 按 Esc键销毁所有窗口
    cv2.destroyAllWindows()
```

### gradio web

web上操作图像
- ![](https://pic3.zhimg.com/80/v2-2f1596269ed54ae5f882da2713cb0e56_1440w.webp)

```py
import gradio as gr
import cv2
?
def to_black(image):
    output = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return output
?
interface = gr.Interface(fn=to_black, inputs="image", outputs="image",
                        examples=[["test.png"]])
interface.launch()
```


# 结束