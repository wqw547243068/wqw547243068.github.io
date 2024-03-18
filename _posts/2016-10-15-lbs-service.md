---
layout: post
title:  "LBS 技术专题"
date:   2016-10-15 10:30:00
categories: 技术工具
tags: 高德 gps geohash base64 gps 北斗 定位 gpx 节日 节假日 时间 时区 宠物 交通 信号灯 大模型
author : 鹤啸九天
excerpt: LBS 技术相关知识
mathjax: true
permalink: /lbs
---

* content
{:toc}

# LBS 技术

汇总 LBS 相关技术


## LBS 

移动互联网如火如荼的今天，各种 `LBS`（Location Based Service，基于地理位置服务）应用遍地开花，其核心要素
- 利用**定位技术**获取当前移动设备（手机）所在的位置
- 然后通过移动互联网获取与当前位置相关的资源和信息

典型的 LBS 应用比如高德地图定位当前位置和附近的建筑、微信查找附近的人、陌陌等陌生人社交应用、滴滴打车查询附近的车、大众点评查找附近的餐馆等等，
- 通过 Geo 可以轻松搞定在海量数据中查找附近 XXX 的功能。

## 地理坐标

地理坐标系统与投影坐标系统
- `地理坐标系统`（Geographic Coordinate System）是一种**球面坐标**，使用三维球面来定义地球表面位置，以实现通过经纬度对地球表面点位引用的坐标系。
- `投影坐标系统`（Projection Coordinate System）是一种**平面坐标**。投影坐标系使用基于X,Y值的坐标系统来描述地球上某个点所处的位置。这个坐标系是从地球的近似椭球体投影得到的，它对应于某个地理坐标系。

投影坐标系由以下参数确定：
- 地理坐标系（由基准面确定，比如：北京54、西安80、WGS84）
- 投影方法（比如高斯－克吕格、Lambert投影)、Mercator投影）

### 经纬度

地理坐标一般由经度和维度组成，初始区间范围
- 纬度 \[-90,90\]: 维度值锁定 1/4圈(90°)
- 经度 \[-180,180\]: 经度值锁定一个半圈(180°)

```py
# 经纬度变化对应地理距离
min_range = [0.001, 0.001] # 100*110m
```

地球是一个**椭球**，Datum 是一组用于描述这个椭球的数据集合。

最常用的一个 Datum 是 `WGS84`（World Geodetic System 1984），主要参数有：
-   坐标系的原点是`地球质心`（center of mass）；
-   `子午线`（meridian），即`零度经线`，位于`格林威治子午线`Royal Observatory所在纬度往东5米所对应的的经线圈；
-   椭球截面长轴为 a=6378137米；
-   椭圆截面短轴为 b=6356752.3142米，可选参数；
-   `扁平比例`（flattening）f=(a−b)/a=1/298.257223563；
-   geoid，`海平面`，用于定义高度，本文从略。

通过以上参数设定，才能对地球上的任意一个位置用`经度`、`纬度`、`高度`三个变量进行描述。所以获取一组经纬度信息时，首先要弄明白这组信息对应的Datum。
- ![](https://www.biaodianfu.com/wp-content/uploads/2020/09/earth.png)

`WGS84` Datum的信息可以用下图进行概括：
- ![](https://www.biaodianfu.com/wp-content/uploads/2020/09/wgs84.png)
- `WGS84` 的坐标转化为`GCJ02`的坐标是**单向**的，即 `WGS84`的坐标能够准确地变换为`GCJ02`坐标；
- 但`GCJ02`坐标转换为`WGS84`时会存在精度损失。
- `GCJ02`的坐标和`BD09`的坐标转换是**双向**的。
- 详细信息见先前的文章[地图经纬度及坐标系统转换的那点事](https://www.biaodianfu.com/coordinate-system.html)。

### 墨卡托投影

地图是平面的，因此将球面坐标转换为平面坐标，这个转换过程称为`投影`。最常见的投影是`墨卡托`（Mercator）投影它具有**等角**性质，即球体上的两点之间的角度方位与平面上的两点之间的角度方位保持不变，因此特别适合用于导航。

`墨卡托`于1569年提出的一种地球投影方法，该方法是圆柱投影的一种，又名”等角正轴圆柱投影”。
- ![](https://www.biaodianfu.com/wp-content/uploads/2020/09/Mercator.png)

主要特点：
- 没有角度变形，由每一点向各方向的长度比相等，它的经纬线都是平行直线，且相交成直角，经线间隔相等，纬线间隔从基准纬线处向两极逐渐增大。
- 长度和面积变形明显，但基准纬线处无变形，从基准纬线处向两极变形逐渐增大，但因为它具有各个方向均等扩大的特性，保持了方向和相互位置关系的正确。

在地图上保持**方向和角度正确**是墨卡托投影的优点，`墨卡托投影`地图常用作航海图和航空图，如果循着墨卡托投影图上两点间的直线航行，方向不变可以一直到达目的地，因此它对船舰在航行中定位、确定航向都具有有利条件，给航海者带来很大方便。故广泛用于编制航海图和航空图等

注意：
- `墨卡托投影`并不是一种**坐标系**，而是为了在二维平面上展示三维地球而进行的一种**空间映射**。
- 所以在GIS地图和互联网地图中，虽然用户看到的地图经过了墨卡托投影，但依然使用经纬度坐标来表示地球上点的位置。

`Web墨卡托投影`（又称`球体墨卡托投影`）是墨卡托投影的变种，接收的输入是Datum为`WGS84`经纬度，但在投影时不再把地球当做**椭球**而当做半径为6378137米的标准球体，以简化计算。其计算公式推导请参考下图：
- ![](https://www.biaodianfu.com/wp-content/uploads/2020/09/Web_Mercator.png)

参数：
-   球半径：以WGS84椭球的长半轴半径为球半径，即球半径取6378137米。(部门用的Flex地图端测距是6378000米，我认为是不太准确的)
-   赤道周长: 2PIr = 2\*20037508.3427892
-   投影坐标系：以赤道为标准纬线，本初子午线为中央经线，两者交点为坐标原点，向东向北为正，向西向南为负。
-   x：\[-20037508.3427892,20037508.3427892\]
-   y：\[-20037508.3427892,20037508.3427892\]
-   lon：\[-180,180\]
-   lat：\[-85.05112877980659，05112877980659\]

`Web墨卡托投影`有两个相关的投影标准，经常搞混：
-   EPSG4326：Web墨卡托投影后的平面地图，但仍然使用WGS84的经度、纬度表示坐标；
-   EPSG3857：Web墨卡托投影后的平面地图，坐标单位为米。

### 瓦片

[地理信息系统之瓦片坐标系](https://www.biaodianfu.com/coordinates-tile.html)

经过Web墨卡托投影后，地图就变为平面的一张地图。有时候需要看宏观的地图信息（如世界地图里每个国家的国界），有时候又要看很微观的地图信息（如导航时道路的路况信息）。

为此，对这张地图进行**等级切分**。
- 在最高级（zoom=0），需要的信息最少，只需保留最重要的宏观信息，因此用一张256×256像素的图片表示即可；
- 在下一级（zoom=1），信息量变多，用一张512×512像素的图片表示；
- 以此类推，级别越低的像素越高，下一级的像素是当前级的4倍。

这样从最高层级往下到最低层级就形成了一个金字塔坐标体系。

对每张图片，将其切分为256×256的图片，称为`瓦片`（Tile）。
- 在最高级（zoom=0）时，只有一个瓦片；
- 在下一级（zoom=1）时有4个瓦片；
- 在下一级（zoom=2）时有16个瓦片，以此类推。

上述过程可以用下图进行总结：
- ![](https://www.biaodianfu.com/wp-content/uploads/2020/09/tile.png)

#### 瓦片编码

瓦片生成后，就是一堆图片。怎么对这堆图片进行编号，是目前主流<span style='color:red'>互联网地图商分歧最大的地方</span>。总结起来分为四个流派：
- `谷歌XYZ`：Z表示缩放层级，Z=zoom；XY的原点在左上角，X从左向右，Y从上向下。
- `TMS`：开源产品的标准，Z的定义与谷歌相同；XY的原点在左下角，X从左向右，Y从下向上。
- `QuadTree`：微软Bing地图使用的编码规范，Z的定义与谷歌相同，同一层级的瓦片不用XY两个维度表示，而只用一个整数表示，该整数服从四叉树编码规则
- `百度XYZ`：Z从1开始，在最高级就把地图分为四块瓦片；XY的原点在经度为0纬度位0的位置，X从左向右，Y从下向上。

下图显示了前三个流派在zoom=1层级上的瓦片编号结果：
- ![](https://www.biaodianfu.com/wp-content/uploads/2020/09/tile-demo.png)

各大地图服务商都采用了[Web Mercator](https://en.wikipedia.org/wiki/Web_Mercator)进行投影，瓦片坐标系的不同主要是投影截取的地球范围不同、瓦片坐标起点不同。

下表总结了中国主要地图商的瓦片编号流派：

| 地图商 | 瓦片编码 |
| --- | --- |
| 高德地图 | 谷歌XYZ |
| 谷歌地图 | 谷歌XYZ |
| OpenStreetMap | 谷歌XYZ |
| 腾讯地图 | TMS |
| Bing地图 | QuadTree |
| 百度地图 | 百度XYZ |


### 地图坐标系 

地图坐标系，参考
- [这篇文章](http://nightfarmer.github.io/2016/12/01/GPSUtil/)
- 高德地图[坐标拾取器](https://lbs.amap.com/tools/picker)
- [地理信息系统之瓦片坐标系](https://www.biaodianfu.com/coordinates-tile.html)

#### 坐标系总结

几种常用的坐标系：

| 坐标系 | 解释 | 使用地图 |
| --- | --- | --- |
| `WGS84` | **地球坐标系**，国际通用坐标系。设备一般包含**GPS芯片**或者**北斗芯片**获取的经纬度为WGS84地理坐标系,最基础的坐标，谷歌地图在非中国地区使用的坐标系 | GPS/`谷歌地图`卫星 |
| `GCJ02` | **火星坐标系**，中国国家测绘局制订的地理信息系统坐标系统。中国使用的地图产品必须是加密后的坐标，而这套`WGS84`加密后的坐标就是`gcj02`。 | `腾讯`(搜搜)地图，`阿里云`地图，`高德`地图，`谷歌`国内地图 |
| `BD09` | **百度坐标系**，百度在`GCJ02`的基础上进行了**二次加密**，官方解释是为了进一步保护用户隐私 | `百度`地图 |
| `小众坐标系` | 类似于百度地图，在`GCJ02`基础上使用自己的加密算法进行**二次加密**的坐标系 | `搜狗`地图、`图吧`地图 等 |

用谷歌地球、百度、高德分别拾取故宫左下角位置的坐标进行对比。

|类型|图解||
|---|---|---|
|原位置|![img](https://upload-images.jianshu.io/upload_images/1809648-316e01b8279926ba.png)|故宫左下角位置的坐标|
|谷歌坐标在百度显示|![img](https://upload-images.jianshu.io/upload_images/1809648-61520d58ec6deaa0.png)|漂移到左下角中南海新华门|
|谷歌坐标转百度|![](https://upload-images.jianshu.io/upload_images/1809648-949117b2168279d4.png)||


坐标相互转换结果如下

| 坐标系 | Google Earth（WGS84） | 百度地图（BD09） | 高德地图（火星坐标） |
| --- | --- | --- | --- |
| 拾取的坐标 | 116.386364,39.911985 | 116.398991,39.919753 | 116.392627,39.913428 |
| 转换为谷歌地球 | \\ | 116.386371,39.912032 | 116.386384,39.912025 |
| 转换为百度地图 | 116.398979,39.919702 | \\ | 116.399003,39.919747 |
| 转换为高德地图 | 116.392602,39.913383 | 116.392614,39.913434 | \\ |

拿GPS数据到实地跑跟拿着地图定位，可能会偏出20-100米的距离

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-08-14T12:10:34.450Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;zo2H8qF8NOJ8yba8XZCI\&quot; version=\&quot;21.6.5\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;YUrH7kkdw6S7EPocWAtV\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1414\&quot; dy=\&quot;751\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;CRyWcW9bKPYmjVe2kgWn-2\&quot; value=\&quot;地理坐标系对比\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=0;fontSize=18;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;335\&quot; y=\&quot;10\&quot; width=\&quot;150\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;CRyWcW9bKPYmjVe2kgWn-46\&quot; value=\&quot;几种主流坐标变换\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510\&quot; y=\&quot;60\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-40\&quot; value=\&quot;\&quot; style=\&quot;childLayout=tableLayout;recursiveResize=0;strokeColor=#98bf21;fillColor=#A7C942;shadow=1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;130\&quot; y=\&quot;370\&quot; width=\&quot;600\&quot; height=\&quot;126\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-41\&quot; style=\&quot;shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;top=0;left=0;bottom=0;right=0;dropTarget=0;collapsible=0;recursiveResize=0;expand=0;fontStyle=0;strokeColor=inherit;fillColor=#ffffff;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-40\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;600\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-42\&quot; value=\&quot;参数\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=#A7C942;align=center;fontStyle=1;fontColor=#FFFFFF;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-41\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-43\&quot; value=\&quot;谷歌\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=#A7C942;align=center;fontStyle=1;fontColor=#FFFFFF;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-41\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;90\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-44\&quot; value=\&quot;高德\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=#A7C942;align=center;fontStyle=1;fontColor=#FFFFFF;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-41\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;130\&quot; height=\&quot;30\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-69\&quot; value=\&quot;百度\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=#A7C942;align=center;fontStyle=1;fontColor=#FFFFFF;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-41\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;310\&quot; width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;120\&quot; height=\&quot;30\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-65\&quot; value=\&quot;分析\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=#A7C942;align=center;fontStyle=1;fontColor=#FFFFFF;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-41\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;110\&quot; height=\&quot;30\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-61\&quot; value=\&quot;\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=#A7C942;align=center;fontStyle=1;fontColor=#FFFFFF;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-41\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-45\&quot; value=\&quot;\&quot; style=\&quot;shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;top=0;left=0;bottom=0;right=0;dropTarget=0;collapsible=0;recursiveResize=0;expand=0;fontStyle=0;strokeColor=inherit;fillColor=#ffffff;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-40\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;600\&quot; height=\&quot;32\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-46\&quot; value=\&quot;经度\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;align=center;whiteSpace=wrap;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-45\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;90\&quot; height=\&quot;32\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;90\&quot; height=\&quot;32\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-47\&quot; value=\&quot;&amp;lt;div style=&amp;quot;font-family: Menlo, Monaco, &amp;amp;quot;Courier New&amp;amp;quot;, monospace; line-height: 18px;&amp;quot;&amp;gt;116.386364&amp;lt;/div&amp;gt;\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;align=center;whiteSpace=wrap;html=1;labelBackgroundColor=none;fontColor=#333333;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-45\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;90\&quot; width=\&quot;90\&quot; height=\&quot;32\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;90\&quot; height=\&quot;32\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-48\&quot; value=\&quot;&amp;lt;div style=&amp;quot;font-family: Menlo, Monaco, &amp;amp;quot;Courier New&amp;amp;quot;, monospace; line-height: 18px;&amp;quot;&amp;gt;116.392627&amp;lt;/div&amp;gt;\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;align=center;whiteSpace=wrap;html=1;labelBackgroundColor=none;fontColor=#333333;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-45\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; width=\&quot;130\&quot; height=\&quot;32\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;130\&quot; height=\&quot;32\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-70\&quot; value=\&quot;&amp;lt;div style=&amp;quot;font-family: Menlo, Monaco, &amp;amp;quot;Courier New&amp;amp;quot;, monospace; line-height: 18px;&amp;quot;&amp;gt;116.398991&amp;lt;/div&amp;gt;\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;align=center;whiteSpace=wrap;html=1;labelBackgroundColor=none;fontColor=#333333;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-45\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;310\&quot; width=\&quot;120\&quot; height=\&quot;32\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;120\&quot; height=\&quot;32\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-66\&quot; value=\&quot;递增0.006\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;align=center;whiteSpace=wrap;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-45\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; width=\&quot;110\&quot; height=\&quot;32\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;110\&quot; height=\&quot;32\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-62\&quot; value=\&quot;\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;align=center;whiteSpace=wrap;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-45\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540\&quot; width=\&quot;60\&quot; height=\&quot;32\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;60\&quot; height=\&quot;32\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-49\&quot; value=\&quot;\&quot; style=\&quot;shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;top=0;left=0;bottom=0;right=0;dropTarget=0;collapsible=0;recursiveResize=0;expand=0;fontStyle=1;strokeColor=inherit;fillColor=#EAF2D3;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-40\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;62\&quot; width=\&quot;600\&quot; height=\&quot;31\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-50\&quot; value=\&quot;维度\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;whiteSpace=wrap;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-49\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;90\&quot; height=\&quot;31\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;90\&quot; height=\&quot;31\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-51\&quot; value=\&quot;&amp;lt;div style=&amp;quot;font-family: Menlo, Monaco, &amp;amp;quot;Courier New&amp;amp;quot;, monospace; line-height: 18px;&amp;quot;&amp;gt;39.911985&amp;lt;/div&amp;gt;\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;whiteSpace=wrap;html=1;labelBackgroundColor=none;fontColor=#333333;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-49\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;90\&quot; width=\&quot;90\&quot; height=\&quot;31\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;90\&quot; height=\&quot;31\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-52\&quot; value=\&quot;&amp;lt;div style=&amp;quot;font-family: Menlo, Monaco, &amp;amp;quot;Courier New&amp;amp;quot;, monospace; line-height: 18px;&amp;quot;&amp;gt;39.913428&amp;lt;/div&amp;gt;\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;whiteSpace=wrap;html=1;labelBackgroundColor=none;fontColor=#333333;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-49\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; width=\&quot;130\&quot; height=\&quot;31\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;130\&quot; height=\&quot;31\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-71\&quot; value=\&quot;&amp;lt;div style=&amp;quot;font-family: Menlo, Monaco, &amp;amp;quot;Courier New&amp;amp;quot;, monospace; line-height: 18px;&amp;quot;&amp;gt;39.919753&amp;lt;/div&amp;gt;\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;whiteSpace=wrap;html=1;labelBackgroundColor=none;fontColor=#333333;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-49\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;310\&quot; width=\&quot;120\&quot; height=\&quot;31\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;120\&quot; height=\&quot;31\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-67\&quot; value=\&quot;递增0.002\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;whiteSpace=wrap;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-49\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; width=\&quot;110\&quot; height=\&quot;31\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;110\&quot; height=\&quot;31\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-63\&quot; value=\&quot;\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;whiteSpace=wrap;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-49\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540\&quot; width=\&quot;60\&quot; height=\&quot;31\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;60\&quot; height=\&quot;31\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-53\&quot; value=\&quot;\&quot; style=\&quot;shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;top=0;left=0;bottom=0;right=0;dropTarget=0;collapsible=0;recursiveResize=0;expand=0;fontStyle=0;strokeColor=inherit;fillColor=#ffffff;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-40\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;93\&quot; width=\&quot;600\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-54\&quot; value=\&quot;分析\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;fontStyle=0;align=center;whiteSpace=wrap;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-53\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;90\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;90\&quot; height=\&quot;33\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-55\&quot; value=\&quot;-\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;fontStyle=0;align=center;whiteSpace=wrap;html=1;labelBackgroundColor=none;fontColor=#333333;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-53\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;90\&quot; width=\&quot;90\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;90\&quot; height=\&quot;33\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-56\&quot; value=\&quot;-\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;fontStyle=0;align=center;whiteSpace=wrap;html=1;labelBackgroundColor=none;fontColor=#333333;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-53\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; width=\&quot;130\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;130\&quot; height=\&quot;33\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-72\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;fontStyle=0;align=center;whiteSpace=wrap;html=1;labelBackgroundColor=none;fontColor=#333333;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-53\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;310\&quot; width=\&quot;120\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;120\&quot; height=\&quot;33\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-68\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;fontStyle=0;align=center;whiteSpace=wrap;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-53\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;430\&quot; width=\&quot;110\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;110\&quot; height=\&quot;33\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;z0P-rp76-IqCCN2JY0Ac-64\&quot; value=\&quot;\&quot; style=\&quot;connectable=0;recursiveResize=0;strokeColor=inherit;fillColor=inherit;fontStyle=0;align=center;whiteSpace=wrap;html=1;\&quot; parent=\&quot;z0P-rp76-IqCCN2JY0Ac-53\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540\&quot; width=\&quot;60\&quot; height=\&quot;33\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle width=\&quot;60\&quot; height=\&quot;33\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-1\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;244\&quot; y=\&quot;280\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;594\&quot; y=\&quot;280\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-2\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;358\&quot; y=\&quot;350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;358\&quot; y=\&quot;80\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-3\&quot; value=\&quot;\&quot; style=\&quot;endArrow=none;dashed=1;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;400\&quot; y=\&quot;350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;400\&quot; y=\&quot;100\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-4\&quot; value=\&quot;\&quot; style=\&quot;endArrow=none;dashed=1;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;440\&quot; y=\&quot;350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;440\&quot; y=\&quot;100\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-5\&quot; value=\&quot;\&quot; style=\&quot;endArrow=none;dashed=1;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;478.5\&quot; y=\&quot;350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;478.5\&quot; y=\&quot;100\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-6\&quot; value=\&quot;\&quot; style=\&quot;endArrow=none;dashed=1;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;360\&quot; y=\&quot;240\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;560\&quot; y=\&quot;240\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-7\&quot; value=\&quot;\&quot; style=\&quot;endArrow=none;dashed=1;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;360\&quot; y=\&quot;200\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;560\&quot; y=\&quot;200\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-8\&quot; value=\&quot;\&quot; style=\&quot;endArrow=none;dashed=1;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;360\&quot; y=\&quot;160\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;560\&quot; y=\&quot;160\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-9\&quot; value=\&quot;\&quot; style=\&quot;endArrow=none;dashed=1;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;360\&quot; y=\&quot;120\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;560\&quot; y=\&quot;120\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-10\&quot; value=\&quot;\&quot; style=\&quot;endArrow=none;dashed=1;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;360\&quot; y=\&quot;320\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;560\&quot; y=\&quot;320\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-11\&quot; value=\&quot;\&quot; style=\&quot;endArrow=none;dashed=1;html=1;rounded=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;520\&quot; y=\&quot;350\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;520\&quot; y=\&quot;100\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-12\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#FF6666;strokeColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;260\&quot; width=\&quot;20\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-14\&quot; value=\&quot;维度差 0.002\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;280\&quot; y=\&quot;210\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-15\&quot; value=\&quot;经度差 0.006\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;525\&quot; y=\&quot;280\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-16\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#FF6666;strokeColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;400\&quot; y=\&quot;220\&quot; width=\&quot;20\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-17\&quot; value=\&quot;\&quot; style=\&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#FF6666;strokeColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;440\&quot; y=\&quot;140\&quot; width=\&quot;20\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-19\&quot; value=\&quot;谷歌坐标\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380\&quot; y=\&quot;255\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-20\&quot; value=\&quot;高德坐标\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;420\&quot; y=\&quot;210\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-21\&quot; value=\&quot;百度坐标\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;440\&quot; y=\&quot;120\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-22\&quot; value=\&quot;116.386364\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#FF0000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;280\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-23\&quot; value=\&quot;39.911985\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#FF0000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;296\&quot; y=\&quot;244\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-24\&quot; value=\&quot;&amp;lt;div style=&amp;quot;text-align: center;&amp;quot;&amp;gt;&amp;lt;span style=&amp;quot;background-color: initial;&amp;quot;&amp;gt;&amp;lt;font face=&amp;quot;Menlo, Monaco, Courier New, monospace&amp;quot;&amp;gt;故宫左下角&amp;lt;/font&amp;gt;&amp;lt;/span&amp;gt;&amp;lt;/div&amp;gt;\&quot; style=\&quot;text;whiteSpace=wrap;html=1;fontColor=#FF0000;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;290\&quot; y=\&quot;280\&quot; width=\&quot;70\&quot; height=\&quot;20\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-25\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;fontSize=13;strokeWidth=3;strokeColor=#FFCCCC;entryX=0;entryY=1;entryDx=0;entryDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; target=\&quot;tyx8eMr4u8P8Fzxnx1Ud-16\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;380\&quot; y=\&quot;260\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;426\&quot; y=\&quot;220\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-26\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;fontSize=13;strokeWidth=3;strokeColor=#FFCCCC;entryX=0;entryY=1;entryDx=0;entryDy=0;exitX=-0.071;exitY=0.433;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;tyx8eMr4u8P8Fzxnx1Ud-20\&quot; target=\&quot;tyx8eMr4u8P8Fzxnx1Ud-17\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;410\&quot; y=\&quot;220\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;413\&quot; y=\&quot;247\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

故宫左下角坐标
- 谷歌 116.386364, 39.911985
- 高德 116.392627, 39.913428
- 百度 116.398991, 39.919753

百度API上取到的，是`BD-09`坐标，只适用于百度地图相关产品。
- 搜狗API上取到的，是搜狗坐标，只适用于搜狗地图相关产品。
- 谷歌地球，google earth上取到的，是GPS坐标，而且是度分秒形式的经纬度坐标。

在国内不允许使用。必须转换为`GCJ-02`坐标。


[](https://blog.csdn.net/zhuzj12345/article/details/106395800)

我国 4个常见坐标系及椭球体，就可以推及到世界各地不同的GCS及椭球体，完成数据的转化问题。
- 1 北京54坐标系（参心）
  - 新中国成立以后，我国大地测量进入了全面发展时期，再全国范围内开展了正规的，全面的大地测量和测图工作，迫切需要建立一个参心大地坐标系。由于当时的“一边倒”政治趋向，故我国采用了前苏联的克拉索夫斯基椭球参数，并与前苏联1942年坐标系进行联测，通过计算建立了我国大地坐标系，定名为1954年北京坐标系。因此，1954年北京坐标系可以认为是前苏联1942年坐标系的延伸。它的原点不在北京而是在前苏联的普尔科沃。
- 2 西安80坐标系（参心）
  - 改革开放啦，国家商量要搞一个更符合国用的坐标系——西安80坐标系，该坐标系的大地原点设在我国中部的陕西省泾阳县永乐镇，位于西安市西北方向约60公里。
- 3 WGS84坐标系（地心）
  - 全称World Geodetic System - 1984，是为了解决GPS定位而产生的全球统一的一个坐标系。
- 4 CGCS2000坐标系（地心）
  - 2000国家大地坐标系是全球地心坐标系在我国的具体体现，其全称为China Geodetic Coordinate System 2000，其原点为包括海洋和大气的整个地球的质量中心。

| 坐标系名 | 北京54 | 西安80 | WGS84 | CGCS2000 |
| --- | --- | --- | --- | --- |
| 参考椭球 | Krasovsky_1940 | 1AG75(ArcGIS中标注是Xian_1980椭球) | WGS_1984 | CGCS2000 |
| 椭球极半径b | 6 356 863.0187730473 | 6356755 288158 | 6356752.314245 | CGCS2000 |
| 椭球赤道半径a | 6378245.000000 | 6378140.000000 | 6378137.000000 | 6378137.000000 |
| 扁率 | 1/298.3 | 1/298.25722101 | 1/298.257223563 | 1/298.257222101 |
| 参考水准面 | 56黄海 | 85黄海 | -  | 85黄海 |
| ArcGIS中的名称 | GCS_Beijing_1954 | GCS_Xian_1980 | GCS_WGS_1984 | GCS_China_Geodetc_Coordinate_System_2000 |
| ArcGIS中WKID | 4214 | 4610 | 4326 | 4490 |

【注】CGCS2000的定义与WGS84实质一样。采用的参考椭球非常接近。扁率差异引起椭球面上的纬度和高度变化最大达0.1mm。当前测量精度范围内，可以忽略这点差异。可以说两者相容至cm级水平

#### 坐标系转换


注意： [详见](https://www.biaodianfu.com/coordinate-system.html)
- `WGS84`坐标转化为`GCJ02`的坐标是**单向**的，即`WGS84`坐标能够准确地变换为`GCJ02`坐标；
- 但`GCJ02`坐标转换为`WGS84`时会存在精度损失。
- `GCJ02`的坐标和`BD09`的坐标转换是**双向**的


<div class="mermaid">
    flowchart LR
    %% 节点颜色
    classDef red fill:#f02;
    classDef green fill:#5CF77B;
    classDef blue fill:#6BE0F7;
    classDef orange fill:#F7CF6B;
    classDef grass fill:#C8D64B;
    %%节点关系定义
    W(地球坐标系\nWGS84\n国际通用,GPS/北斗):::grass-.->|中国标准,加密,不可逆\n高德/腾讯/阿里/谷歌中国|G(火星坐标系\nGCJ02):::blue
    G -->|百度二次加密| B(百度坐标系\nBD09\n百度地图):::blue
    G -->|其它二次加密法| O(小众坐标系\n搜狗,图吧):::blue
</div>

coordtransform 用于百度坐标系(bd-09)、火星坐标系(国测局坐标系、gcj02)、WGS84坐标系的相互转换，并提供中文地址到坐标的转换功能，仅使用Python标准模块，无其他依赖。
- [go版本](https://github.com/qichengzx/coordtransform)
- [Python版本](https://github.com/SoufSilence/coordTransform_py/tree/master)
- [js版本](https://github.com/wandergis/coordtransform)
- [命令行版本](https://github.com/wandergis/coordtransform-cli)

代码

```py
# 方法说明
gcj02_to_bd09(lng, lat) # 火星坐标系->百度坐标系
bd09_to_gcj02(lng, lat) # 百度坐标系->火星坐标系
wgs84_to_gcj02(lng, lat) # WGS84坐标系->火星坐标系
gcj02_to_wgs84(lng, lat) # 火星坐标系->WGS84坐标系
bd09_to_wgs84(lng, lat) # 百度坐标系->WGS84坐标系
wgs84_to_bd09(lng, lat) # WGS84坐标系->百度坐标系

# 中文地址到火星坐标系, 需要高德地图API Key
g = Geocoding('API_KEY')  # 这里填写你的高德Api_Key
g.geocode('北京市朝阳区朝阳公园')
```

go语言

```go
package main

import(
	"fmt"
	"github.com/qichengzx/coordtransform"
)

func main() {
	fmt.Println(coordtransform.BD09toGCJ02(116.404, 39.915))
	fmt.Println(coordtransform.GCJ02toBD09(116.404, 39.915))
	fmt.Println(coordtransform.WGS84toGCJ02(116.404, 39.915))
	fmt.Println(coordtransform.GCJ02toWGS84(116.404, 39.915))
	fmt.Println(coordtransform.BD09toWGS84(116.404, 39.915))
	fmt.Println(coordtransform.WGS84toBD09(116.404, 39.915))
}
```

完整版: python3

```py
import json
import urllib
#import urllib.request
#import urllib.parse

import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方

class Geocoding:
    def __init__(self, api_key):
        self.api_key = api_key

    def geocode(self, address):
        """
        利用高德geocoding服务解析地址获取位置坐标
        address:需要解析的地址
        """
        geocoding = {'s': 'rsv3',
                     'key': self.api_key,
                     'city': '全国',
                     'address': address}
        #geocoding = urllib.urlencode(geocoding)
        geocoding = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
        #ret = urllib.urlopen("%s?%s" % ("http://restapi.amap.com/v3/geocode/geo", geocoding))
        ret = urllib.request.urlopen("%s?%s" % ("http://restapi.amap.com/v3/geocode/geo", geocoding))

        if ret.getcode() == 200:
            res = ret.read()
            json_obj = json.loads(res)
            if json_obj['status'] == '1' and int(json_obj['count']) >= 1:
                geocodes = json_obj['geocodes'][0]
                lng = float(geocodes.get('location').split(',')[0])
                lat = float(geocodes.get('location').split(',')[1])
                return [lng, lat]
            else:
                return json_obj
        else:
            return ret

def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    param: lng:火星坐标经度, lat:火星坐标纬度
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    param: bd_lat:百度坐标纬度, bd_lon:百度坐标经度
    return: 转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    param: lng:WGS84坐标系的经度, lat:WGS84坐标系的纬度
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    param: lng:火星坐标系的经度, lat:火星坐标系纬度
    """
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def bd09_to_wgs84(bd_lon, bd_lat):
    """
        百度→国际(地球): 百度→火星→地球
    """
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    """
        国际(地球)→百度: 地球→火星→百度
    """
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng, lat:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


if __name__ == '__main__':
    data = [116.321038,        40.047309] # 地铁站数据
    data = [116.30151943750988,40.03962264987973] # 六只脚app
    lng = data[0]
    lat = data[1]
    print(f'原始坐标:   [{lng}, {lat}]')
    result1 = gcj02_to_bd09(lng, lat) # 火星→百度
    result2 = bd09_to_gcj02(lng, lat) # 百度→火星
    result3 = wgs84_to_gcj02(lng, lat) # 地球→火星
    result4 = gcj02_to_wgs84(lng, lat) # 火星→地球
    result5 = bd09_to_wgs84(lng, lat) # 百度→地球
    result6 = wgs84_to_bd09(lng, lat) # 地球→百度
    API_KEY = 'ddb12712f0528934ab85b8ebaa8add75'
    g = Geocoding(API_KEY)  # 这里填写你的高德api的key
    result7 = g.geocode('北京市朝阳区朝阳公园')
    print('火星→百度: ',result1, '\n百度→火星: ',result2, '\n地球→火星: ',result3, '\n火星→地球: ',result4, '\n百度→地球: ',result5, '\n地球→百度: ',result6, '\ngeo:',result7)
```


### 地理位置资源


#### 行政规划

- [全国省市县经纬度信息.csv](https://download.csdn.net/download/s1997m5/44927112)


#### 高校

- [全国高校位置](https://download.csdn.net/download/GISShiXiSheng/52711082)


#### 交通位置

覆盖地铁、机场
- 全国地铁站经纬度信息
  - [全国城市地铁站点信息V202104（带经纬度）.csv](https://download.csdn.net/download/qq_45590504/21121364), 截止 2021年4月
- 全球地铁站经纬度数据，20655条, csdn原始地址，[付费下载](https://ziquyun.com/main/file?f=file_1692329963419.zip), 源自 [自取云](https://ziquyun.com/), [csdn 免积分下载](https://www.waodown.com/926.html)
- [2022年全球机场坐标数据](https://download.csdn.net/download/qq_45590504/85726999)



```json
id	city_code	city_name	line_id	line_name	station_id	station_name	longitude	latitude
1	131	北京市	28d3dce37526799f49fd3fb7	地铁10号线	092337b9de1f0ace70210bde	巴沟	116.300281	39.980453
2	131	北京市	28d3dce37526799f49fd3fb7	地铁10号线	899278188c804968863304de	苏州街	116.312768	39.981704
3	131	北京市	28d3dce37526799f49fd3fb7	地铁10号线	c9332a87cf26bf7a14c905de	海淀黄庄	116.324344	39.981865
4	131	北京市	28d3dce37526799f49fd3fb7	地铁10号线	9aac692139342d808afc06de	知春里	116.336091	39.982061
```

注：
- 地铁站经纬度疑似百度坐标，需要转换

```py
# 北京清河站坐标
a = np.array([116.321038,        40.047309]) # 地铁站数据
b = np.array([116.30151943750988,40.03962264987973]) # 六只脚app
a - b # [0.01951856, 0.00768635]
```

### 距离计算

两点距离计算
- 南北跨度（维度差）
  - 比较两个点GPS坐标的**维度差**，维度小的点靠南，维度大的点靠北。不同区域维度差距离是固定的。
  - 维度与距离换算为：1度=110.94公里，1分=1.85公里，1秒=30.8米（户外就按30米估算即可！）。
- 东西跨度（经度差）
  - 比较两个点GPS坐标的**经度差**，经度小的点靠西，经度大的点靠东。与维度不同，不同区域经度差距离是变化的，离赤道越远距离越短。
  - 北京地区即北纬40度附近的经度与距离换算为：1度=85.2公里，1分=1.42公里，1秒=23.69米（户外就按25米估算即可！）。

高度跨度（海拔差）
- 比较两个点GPS坐标的海拔差。

判断两个点的直线距离
- (1) 水平直线距离： $\sqrt{维度差^2+经度差^2}$
- (2) 考虑高度的直线距离： $\sqrt{维度差^2+经度差^2+海拔差^2}$

GPS数据应用距离

GPS数据三种格式
- 1、第一种格式：ddd.ddddd（如36.45666，单位是：度）
- 2、第二种格式：ddd.mm.mmm（如36.45.666，单位是36度45.666分）
- 3、第三种格式：ddd.mm.ss（如36.45.26，单位是36度45分26秒）

注意：
- 遇到危险通过语音报警时建议使用第一种格式（带小数点的数字比较容易说清楚），如有4G信号也可直接截屏发过去（最好根据个人习惯提前设置好APP中经纬度格式，而且能快速找到这一关键数据）。

两点
- A【N40°02'14.59''，E115°43'08.97''，海拔587m】
- B【N40°01'37.02''，E115°45'26.05''，海拔932m】



GPS数据，得出以下具体信息：
- 1、B点维度比A点小，靠南37.57''，折合距离=37.57''*30.8=1157.16m（大约1.2km）；
- 2、B点经度比A点大，靠东2'17.08''（137.08''），折合距离=137.08''*23.69=3247.43m（大约3.2km）；
- 3、B点比A点海拔高354m；
- 4、B点在A点的东南方向，维度差小于经度差，应该是东偏南方向；
- 5、B点距离A点水平距离3447.44m=3.45km；
- 6、B点与A两点直线距离3464.66m=3.46km，仅比水平距离长17.22m；

考虑到户外线路的上下起伏，距离越远，直线距离与实际走的路线相差越大，只能参考。

### 时空挖掘


#### 时间知识

整个地球分为24个时区，每个时区都有自己的**本地时间**。
- 国际无线电通信中，为统一而普遍使用一个标准时间，称为**通用协调时**(UTC, Universal Time Coordinated)。UTC与格林尼治平均时(GMT, Greenwich Mean Time)一样，都与英国伦敦的本地时相同。UTC与GMT含义完全相同。
- 北京时区是东八区，领先UTC 8个小时。所以将UTC装换成北京时间时，需要加上8小时。

时间概念
- `GMT` 时间：`格林威治`时间，基准时间
- `UTC` 时间：Coordinated Universal Time，`全球协调`时间，更精准的基准时间，与 GMT 基本等同
- `CST` `中国基准`时间：为 UTC 时间 + 8 小时，即 UTC 时间的 0 点对应于中国基准时间的 8 点，即为一般称为**东八区**的时间

ISO 8601
- 一种标准化的**时间表示**方法，表示格式为 ：`YYYY-MM-DDThh:mm:ss ± timezone`，可以表示**不同时区**的时间，时区部分用`Z` 表示为 UTC 标准时区。

两个例子：

```sh
1997-07-16T08:20:30Z #  UTC 时间的 1997 年 7 月 16 号 8:20:30
1997-07-16T19:20:30+08:00 # 东八区时间的 1997 年 7 月 16 号 19:20:30
```

时间戳
- 1970年1月1日 00:00:00 UTC+00:00 时区的时刻称为`epoch time`，记为0
- 当前的时间戳: 从 `epoch time` 到现在的秒数，一般叫做 timestamp
- 因此一个时间戳一定对应于一个特定的 `UTC 时间`，同时也对应于其他时区的一个确定的时间。

时间戳是一个相对安全的时间表示方法。


【2023-8-16】节假日判断的api：
- timor [免费节假日 API](https://timor.tech/api/holiday), 不限速，不登录，没广告，免费。
- [holiday](https://github.com/Haoshenqi0123/holiday)

```sh
# timor
http://timor.tech/api/holiday/year # 当年节假日信息
http://timor.tech/api/holiday/year/2023/ # 2023年节假日信息
http://timor.tech/api/holiday/year/2023-08 # 8月节假日信息
http://timor.tech/api/holiday/info/2023-08-16 # 当天是否节假日
http://timor.tech/api/holiday/batch?d=$date&type=Y # 批量查询指定日期节假日信息
http://timor.tech/api/holiday/next/$date?type=Y&week=Y # 指定日期的下一个节假日（如果在放假前有调休，也会返回
http://timor.tech/api/holiday/workday/next/$date # 指定日期的下一个工作日（工作日包含正常工作日、调休）不包含当天
http://timor.tech/api/holiday/year/$date?type=Y&week=Y # 指定年份或年月份的所有节假日信息
http://timor.tech/api/holiday/tts # 节假日提示文本
http://timor.tech/api/holiday/tts/next # 最近一个节日
http://timor.tech/api/holiday/tts/tomorrow # 判断明天是否放假
# get 方法
http://api.haoshenqi.top/holiday?date=2023-10-05
```

格式

```json
{
  "code": 0,              // 0服务正常。-1服务出错
  "type": {
    "type": enum(0, 1, 2, 3), // 节假日类型，分别表示 工作日、周末、节日、调休。
    "name": "周六",         // 节假日类型中文名，可能值为 周一 至 周日、假期的名字、某某调休。
    "week": enum(1 - 7)    // 一周中的第几天。值为 1 - 7，分别表示 周一 至 周日。
  },
  "holiday": {
    "holiday": false,     // true表示是节假日，false表示是调休
    "name": "国庆前调休",  // 节假日的中文名。如果是调休，则是调休的中文名，例如'国庆前调休'
    "wage": 1,            // 薪资倍数，1表示是1倍工资
    "after": false,       // 只在调休下有该字段。true表示放完假后调休，false表示先调休再放假
    "target": '国庆节'     // 只在调休下有该字段。表示调休的节假日
  }
}
```

#### 常驻点

【2022-7-13】高德用户常驻点挖掘，拿用户过去一个月的定位点数据聚类，大大超过阿里odps单机800m限制，于是开始思考如何精简数据，方法：
- ① 根据时间信息计算定位点瞬时速度，加速度，剔除运动点，漂移点，过滤了大概2/3
- ② geohash，将地理坐标投射到直线上，降低数据量
  - [geometry](https://halfrost.com/go_spatial_search/) 比geohash 好？
  - [geohash](https://www.cnblogs.com/tgzhu/articles/6204173.html)
- ③ 改进密度聚类算法dbscan，球面距离计算公式部分改成根据经纬度明式距离直接排除噪声点…最终在odps跑通了…另外，调研过路径匹配的方案，微软有篇文章

效果展示 [demo](wqw/demo/points_cluster.html)
- 定位点处理: geohash聚合
  - 3个月定位数据太多，超过Hadoop节点 800m 限制
  - geohash 聚合定位点
- 运动状态计算： 按时间排序，计算速度，区分状态
  - 静态点： 用于常驻点挖掘，占比 1/3
  - 动态点： 用于交通工具挖掘，占比 2/3
- DBSCAN 聚类得到常驻点
  - 去掉噪声点
  - 簇计算，质心
  - GEO获取质心poi
- 预测家、公司
  - 家：一般是夜间、周末
  - 公司：白天，通勤频繁、规律


输出格式:

| 字段名	| 类型	| 说明 |
| ---	| ---	| --- |
| did	| string |	用户id，目前采用did |
| total_point_num	| bigint	| 总定位点数 |
| static_point_num	| bigint	| 静态定位点数 |
| cluster_num	| int	| 聚类得到的簇总数 |
| cluster_id	| int	| 簇编号 |
| cluster_point_num	| bigint	| 当前簇内包含的定位点数目 |
| date_gap	| int	| 簇内定位点对应日期跨度，多少天 |
| date_num	| int	| 簇内定位点对应日期数目，多少个 |
| avg_point	| string	| 质心点坐标,格式："lon,lat"，当值为“transport”时表示出行方式结果 |
| cluster_range	string	| 地理围栏信息，5个数值(矩形框左下角+右上角)拼接成的字符串 |
| cluster_var	double	| 簇内定位点距离方差 |
| cluster_score |	double	| 簇得分 |
| center_point	| string	| 中心点坐标, 格式："lon,lat"，当值为“transport”时表示出行方式结果 |
| member_set	| string	| 成员点经纬度集合, "&"连接 |
| cluster_type	| string	| 常驻点属于什么类别（家/公司）？json格式信息 |
| type_info	string	| 判定详情信息，比cluster_type更完整 |


#### 出行方式

交通工具[速度](https://www.ximalaya.com/ask/q3108059?source=m_jump)
- 步行: 5-6 km/h
- 跑步: 9-13 km/h
- 自行车: 15 km/h
- 电瓶车: 25-35 km/h 
- 摩托车: 30-100 km/h
- 公交车: 预设路线和时间安排
- 地铁: 预设路线和时间安排
- 轮船: 30－50 km/h
- 汽车: 50－200 km/h
- 火车: 100－300 km/h
- 飞机: 500－800 km/h

注
- 1 m/s = **3.6** km/h



<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-08-17T09:51:02.608Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;lfpv8sGgabe9AcDg_yKd\&quot; version=\&quot;21.6.8\&quot;&gt;\n  &lt;diagram name=\&quot;第 1 页\&quot; id=\&quot;YUrH7kkdw6S7EPocWAtV\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1414\&quot; dy=\&quot;751\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;CRyWcW9bKPYmjVe2kgWn-2\&quot; value=\&quot;出行方式速度对比\&quot; style=\&quot;text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontStyle=0;fontSize=18;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;325\&quot; y=\&quot;10\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-1\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;\&quot; parent=\&quot;1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;120\&quot; y=\&quot;320\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;740\&quot; y=\&quot;320\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-2\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;\&quot; parent=\&quot;1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;120\&quot; y=\&quot;320\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;120\&quot; y=\&quot;50\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-3\&quot; value=\&quot;\&quot; style=\&quot;endArrow=none;dashed=1;html=1;rounded=0;\&quot; parent=\&quot;1\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;120\&quot; y=\&quot;180\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;720\&quot; y=\&quot;180\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-15\&quot; value=\&quot;速度(km/h)\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;700\&quot; y=\&quot;320\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;tyx8eMr4u8P8Fzxnx1Ud-21\&quot; value=\&quot;步行&amp;lt;br&amp;gt;5-6\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;200\&quot; y=\&quot;200\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-1\&quot; value=\&quot;\&quot; style=\&quot;curved=1;endArrow=none;html=1;rounded=0;strokeColor=#97D077;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;120\&quot; y=\&quot;170\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;330\&quot; y=\&quot;170\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;160\&quot; y=\&quot;165\&quot; /&gt;\n              &lt;mxPoint x=\&quot;170\&quot; y=\&quot;125\&quot; /&gt;\n              &lt;mxPoint x=\&quot;220\&quot; y=\&quot;110\&quot; /&gt;\n              &lt;mxPoint x=\&quot;250\&quot; y=\&quot;110\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-2\&quot; value=\&quot;停止\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;120\&quot; y=\&quot;204\&quot; width=\&quot;50\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-3\&quot; value=\&quot;跑步\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;270\&quot; y=\&quot;204\&quot; width=\&quot;50\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-4\&quot; value=\&quot;自行车\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;325\&quot; y=\&quot;204\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-5\&quot; value=\&quot;公交车&amp;lt;br&amp;gt;25-50\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;150\&quot; y=\&quot;340\&quot; width=\&quot;60\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-6\&quot; value=\&quot;地铁&amp;lt;br&amp;gt;30-60\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;200\&quot; y=\&quot;340\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-7\&quot; value=\&quot;小汽车&amp;lt;br&amp;gt;平均60,&amp;amp;lt;120\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;250\&quot; y=\&quot;340\&quot; width=\&quot;90\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-8\&quot; value=\&quot;高铁&amp;lt;br&amp;gt;300\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;490\&quot; y=\&quot;340\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-9\&quot; value=\&quot;飞机&amp;lt;br&amp;gt;500-800\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;640\&quot; y=\&quot;340\&quot; width=\&quot;70\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-11\&quot; value=\&quot;0.072\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;120\&quot; y=\&quot;180\&quot; width=\&quot;50\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-12\&quot; value=\&quot;5\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;180\&quot; y=\&quot;180\&quot; width=\&quot;30\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-13\&quot; value=\&quot;10\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;240\&quot; y=\&quot;180\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-14\&quot; value=\&quot;15\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;290\&quot; y=\&quot;180\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-15\&quot; value=\&quot;20\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;340\&quot; y=\&quot;180\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-16\&quot; value=\&quot;25\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;400\&quot; y=\&quot;180\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-17\&quot; value=\&quot;30\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;455\&quot; y=\&quot;180\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-18\&quot; value=\&quot;300\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;470\&quot; y=\&quot;320\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-19\&quot; value=\&quot;400\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;550\&quot; y=\&quot;320\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-20\&quot; value=\&quot;600\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;610\&quot; y=\&quot;320\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-21\&quot; value=\&quot;800\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;660\&quot; y=\&quot;320\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-22\&quot; value=\&quot;\&quot; style=\&quot;curved=1;endArrow=none;html=1;rounded=0;strokeColor=#97D077;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;120\&quot; y=\&quot;175\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;400\&quot; y=\&quot;170\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;220\&quot; y=\&quot;170\&quot; /&gt;\n              &lt;mxPoint x=\&quot;240\&quot; y=\&quot;130\&quot; /&gt;\n              &lt;mxPoint x=\&quot;280\&quot; y=\&quot;115\&quot; /&gt;\n              &lt;mxPoint x=\&quot;320\&quot; y=\&quot;125\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-23\&quot; value=\&quot;\&quot; style=\&quot;curved=1;endArrow=none;html=1;rounded=0;strokeColor=#66B2FF;endFill=0;exitX=0;exitY=-0.067;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;120\&quot; y=\&quot;172.99\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;430\&quot; y=\&quot;170\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;250\&quot; y=\&quot;170\&quot; /&gt;\n              &lt;mxPoint x=\&quot;270\&quot; y=\&quot;130\&quot; /&gt;\n              &lt;mxPoint x=\&quot;310\&quot; y=\&quot;115\&quot; /&gt;\n              &lt;mxPoint x=\&quot;360\&quot; y=\&quot;115\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-24\&quot; value=\&quot;非机动车\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;60\&quot; y=\&quot;110\&quot; width=\&quot;70\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-25\&quot; value=\&quot;机动车\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;60\&quot; y=\&quot;220\&quot; width=\&quot;60\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-26\&quot; value=\&quot;\&quot; style=\&quot;curved=1;endArrow=none;html=1;rounded=0;strokeColor=#66B2FF;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;162.1\&quot; y=\&quot;320\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;442.1\&quot; y=\&quot;315\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;262.1\&quot; y=\&quot;315\&quot; /&gt;\n              &lt;mxPoint x=\&quot;282.1\&quot; y=\&quot;275\&quot; /&gt;\n              &lt;mxPoint x=\&quot;352.1\&quot; y=\&quot;260\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-27\&quot; value=\&quot;\&quot; style=\&quot;curved=1;endArrow=none;html=1;rounded=0;strokeColor=#66B2FF;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;237.1\&quot; y=\&quot;320\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;517.1\&quot; y=\&quot;315\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;320\&quot; y=\&quot;300\&quot; /&gt;\n              &lt;mxPoint x=\&quot;357.1\&quot; y=\&quot;275\&quot; /&gt;\n              &lt;mxPoint x=\&quot;427.1\&quot; y=\&quot;260\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-28\&quot; value=\&quot;\&quot; style=\&quot;curved=1;endArrow=none;html=1;rounded=0;strokeColor=#66B2FF;endFill=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;302.1\&quot; y=\&quot;320\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;582.1\&quot; y=\&quot;315\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;402\&quot; y=\&quot;290\&quot; /&gt;\n              &lt;mxPoint x=\&quot;422.1\&quot; y=\&quot;275\&quot; /&gt;\n              &lt;mxPoint x=\&quot;492.1\&quot; y=\&quot;260\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-29\&quot; value=\&quot;0.072\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;120\&quot; y=\&quot;320\&quot; width=\&quot;50\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-30\&quot; value=\&quot;停止\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;120\&quot; y=\&quot;340\&quot; width=\&quot;50\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-31\&quot; value=\&quot;速度(km/h)\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;660\&quot; y=\&quot;174\&quot; width=\&quot;80\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-32\&quot; value=\&quot;50\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;200\&quot; y=\&quot;320\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-33\&quot; value=\&quot;100\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;260\&quot; y=\&quot;320\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-34\&quot; value=\&quot;150\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;320\&quot; y=\&quot;320\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-35\&quot; value=\&quot;200\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380\&quot; y=\&quot;320\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-36\&quot; value=\&quot;普通火车&amp;lt;br&amp;gt;100\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;330\&quot; y=\&quot;340\&quot; width=\&quot;70\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-37\&quot; value=\&quot;摩托车&amp;lt;br&amp;gt;轻便型&amp;amp;lt;50\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;590\&quot; y=\&quot;204\&quot; width=\&quot;80\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-38\&quot; value=\&quot;电动车&amp;lt;br&amp;gt;上路&amp;amp;lt;=15,最高25\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;390\&quot; y=\&quot;204\&quot; width=\&quot;120\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-39\&quot; value=\&quot;40\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;550\&quot; y=\&quot;180\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-40\&quot; value=\&quot;50\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;630\&quot; y=\&quot;180\&quot; width=\&quot;40\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-41\&quot; value=\&quot;\&quot; style=\&quot;curved=1;endArrow=none;html=1;rounded=0;strokeColor=#66B2FF;endFill=0;exitX=0;exitY=-0.067;exitDx=0;exitDy=0;exitPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;335\&quot; y=\&quot;180\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;645\&quot; y=\&quot;177.01\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;450\&quot; y=\&quot;160\&quot; /&gt;\n              &lt;mxPoint x=\&quot;470\&quot; y=\&quot;150\&quot; /&gt;\n              &lt;mxPoint x=\&quot;485\&quot; y=\&quot;137.01\&quot; /&gt;\n              &lt;mxPoint x=\&quot;525\&quot; y=\&quot;122.01\&quot; /&gt;\n              &lt;mxPoint x=\&quot;575\&quot; y=\&quot;122.01\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-42\&quot; value=\&quot;动车&amp;lt;br&amp;gt;200\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;390\&quot; y=\&quot;340\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-43\&quot; value=\&quot;2023-8-17&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;565\&quot; y=\&quot;70\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-44\&quot; value=\&quot;磁悬浮&amp;lt;br&amp;gt;500-600\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;550\&quot; y=\&quot;340\&quot; width=\&quot;70\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;V9TQX8vlhKfmWj-25TbC-45\&quot; value=\&quot;轮船&amp;lt;br&amp;gt;30\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#3333FF;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;510\&quot; y=\&quot;204\&quot; width=\&quot;50\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



[基于GPS轨迹数据的出行方式识别方法](https://patents.google.com/patent/CN107330469A/zh)，其特征在于：根据GPS信号分三种情况，GPS信号缺失，GPS信号不完整，GPS信号正常；
- a. **GPS信号缺失**，基于**规则**的地铁单方式出行的识别方法：
  - 1)地铁单方式段持续时间大于5分钟；
  - 2)GPS轨迹点的最大速度小于地铁最高速度；
  - 3)地铁单方式段的起点与最近的地铁出入口之间的距离小于100米；
  - 4)地铁单方式段的终点与最近的地铁出入口之间的距离小于200米；
- b. **GPS信号不完整**，基于**规则**的地铁单方式的识别方法：
  - 1)满足所述的GPS信号缺失，基于规则的地铁单方式段出行的识别方法的所有要求；
  - 2)除起点和终点外的所有GPS轨迹点与最近的地铁线路之间的距离小于30米；
- c. **GPS信号正常**的其他出行方式采用随机森林分类器, 包括以下步骤：
  - 第一步、GPS轨迹数据准备：
    - 采集的GPS轨迹数据包括：用户编号、定位日期、时间、经度、纬度、速度、海拔、方向和定位卫星数，根据用户编号，GPS轨迹数据按照时间顺序分配到每个人每天的出行，即摘取每人每天的出行轨迹点并进行相关参数的计算，
    - 1)计算每个点瞬时速度；
    - 2)计算每个点瞬时加速度；
    - 3)计算每个点方向变化值；
    - 4)计算特征参数：计算每个单方式出行段的速度、加速度、方向变化和距离/出行时长4个方面的特征作为方式识别的输入参数；
  - 第二步、特征参数筛选：
    - 将第一步数据作为全样本输入Weka进行参数筛选，使用不同的搜索方法和相应的评价策略来搜索，直至找出使得全样本出行方式分类最佳的组合，筛选出7个显著特征参数：出行距离，平均速度，50分位速度S50，75分位速度S75，95分位速度S95，平均方向变化量和速度偏度；
  - 第三步、随机森林分类器出行方式识别：
    - 按照第2步筛选的特征参数整理每个单方式出行段，这样得到每个单方式出行段的特征参数集，使用Weka Explorer的分类功能，系统随机把所有样本分为60％和40％两部分，60％的样本用于建模训练，40％的样本用于验证测试。

类似的，新疆大学[于GPS轨迹的用户移动行为挖掘算法](https://patents.google.com/patent/CN107330469A/zh)

【2023-8-10】[基于Python实现个人手机定位分析](https://zhuanlan.zhihu.com/p/624916375), TransBigData是一个为交通时空大数据处理、分析和可视化而开发的Python包

交通时空大数据并不局限于交通工具产生的数据，日常生活中也会产生大量的数据。
- 手机记录了到访过的地点；使用城市公交IC卡、共享单车等服务时，服务供应商可以知道这些出行需求的时间和地点等等

TransBigData 一个为交通时空大数据处理、分析和可视化而开发的Python包。
- TransBigData 为处理常见的交通时空大数据（如出租车GPS数据、共享单车数据和公交车GPS数据等）提供了快速而简洁的方法。

TransBigData主要提供以下方法：
- (1) 数据**预处理**：对数据集提供快速计算数据量、时间段、采样间隔等基本信息的方法，也针对多种数据噪声提供了相应的清洗方法。
- (2) 数据**栅格化**：提供在研究区域内生成、匹配多种类型的地理栅格快学Python（矩形、三角形、六边形及geohash栅格）的方法体系，能够以向量化的方式快速算法将空间点数据映射到地理栅格上。
- (3) 数据**可视化**：基于可视化包keplergl，用简单的代码即可在Jupyter Notebook上交互式地可视化展示数据。
- (4) **轨迹处理**：从轨迹数据GPS点生成轨迹线型，轨迹点增密、稀疏化等。
- (5) 地图**底图、坐标转换**与计算：加载显示地图底图与各类特殊坐标系之间的坐标转换。
- (6) 特定处理方法：针对各类特定数据提供相应处理方法，如从出租车GPS数据中提取订单起讫点，从手机信令数据中识别居住地与工作地，从地铁网络GIS数据构建网络拓扑结构并计算最短路径等。

手机信令数据读取

手机信令数据是指手机与通信基站之间交换的信息，包括位置、通信时长、通信频次等数据。这些数据可以用于分析用户的出行行为、生活习惯等，也可以用于城市交通管理、商业营销等领域。
- ![](https://pic3.zhimg.com/80/v2-df544cc9597a84df47b8c11301b3837a_1440w.webp)

识别**出行**和**停留**
- 在处理手机数据时，识别出行和停留是很重要的一步。基于手机识别出行和活动可以进一步进行路径分析、出行模式分析、人群分析等工作。
- 活动：手机数据通过连续地追踪个体的出行轨迹，可以构建出个体的出行链信息，一般来说，如果一个手机用户在某个位置停留了超过30分钟，我们可以认为用户在这里发生了活动。
- 出行：用户产生的连续两个活动如果产生的地理位置不同，则可以认为用户发生了出行行为。出行的起点为连续两个活动中前一个活动的地理位置，出行的开始时间为前一个活动结束的时间，出行的终点则为后一个活动的地理位置，出行的结束时间则为后一个活动开始的时间。简而言之，用户在活动点与活动点之间的移动，视为用户的出行。

活动与出行识别思路
- 使用TransBigData提供的手机信令数据处理方法，可以先将数据对应至栅格，将同一个栅格内的数据视为在同一个位置，以避免数据定位误差导致同一位置被识别为多个。然后，可以使用tbd.mobile_stay_move函数从手机数据中识别出行和停留:

识别居住地与工作地
- 通过移动通信数据识别出用户的职住信息是研究的基础工作之一。TransBigData中，以停留活动点为依据，用tbd.mobile_identify_home方法可以识别居住地，用tbd.mobile_identify_work则可以识别工作地。具体规则为：

居住地识别规则为**夜晚时段停留最长**地点
- 工作地识别规则为工作日白天时段停留最长地点（每日平均时长大于minhour）。

绘制活动图
- 为了加深对手机用户的具体活动情况的理解，我们可以用TransBigData提供的tbd.mobile_plot_activity方法将用户的每日活动情况绘制出来观察
- ![](https://pic4.zhimg.com/80/v2-357766d9c2cf2cf3c7b3b75cacac6a2b_1440w.webp)
- 一个手机用户在观测时间段内每一天的活动情况，横坐标为日期，纵坐标为时间，同一个位置的活动则以同样的颜色显示。从活动图中我们可以很清晰地看到这个用户每一个活动的开始与结束时间。


#### 交通信号灯

【2024-3-17】[AI大模型控制红绿灯，港科大（广州）智慧交通新成果已开源](https://www.toutiao.com/article/7347205493460599315)

大模型用于交通信号控制（TSC）
- 模型名为 LightGPT ，以排队及不同区段快要接近信号灯的车辆对路口交通状况分析，进而确定最好的信号灯配置。

香港科技大学（广州）的研究团队提出名为LLMLight的框架。
- 该框架向**智能体**提供详细的实时交通状况，并结合先验知识构成提示，利用大模型卓越的泛化能力，采用符合人类直觉的推理和决策过程来实现有效的交通控制。

在九个交通流数据集上的实验证明了LLMLight框架的有效性、泛化能力和可解释性。
- LLMLight在所有基准测试中始终达到了SOTA或与经典强化学习等方法同等的性能水平，并且拥有比后者更为强大的泛化性。
- LLMLight还能在决策时提供背后的分析逻辑，这一可解释性实现了信号灯控制的透明化。

TSC垂类大模型LightGPT在此任务上的决策能力显著优于GPT-4。

LLMLight的工作流包括：
- 交通状态观测特征构建：收集交通路口的交通状态观测；
- 常识知识增强的智能体提示构建：组成一则整合了常识知识的提示，用于指导LLM推理出下一时间片最优的交通信号灯配置；
- 智能体的分析推理及决策：LLM使用构建的提示进行分析推理决策过程，随后做出决策。

### GEO

地理位置查询功能 GEO, 全称 geospatial 
- `地理编码` (Geocoding)是一个街道、地址或者其他位置（经度、纬度）转化为**坐标**的过程。
- `反向地理编码` (Reverse geocoding)是将**坐标**转换为**地址**（经度、纬度）的过程。

一组反向地理编码结果间可能会有所差异。例如：一个结果可能包含最临近建筑的完整街道地址，而另一个可能只包含城市名称和邮政编码。


#### GEO 场景

通过 Geo 可以轻松搞定在海量数据中查找附近 XXX 的功能。
- 地理围栏：通过设置地理位置的经纬度信息，可以将用户或者车辆等实体绑定在地理围栏内，当实体进出围栏时，可以触发相应的事件。
- 附近的人：在类似于约会、社交、旅游等场景下，可以通过Redis GEO快速查询周围的人员或景点。
- 配送服务：通过获取配送地址的经纬度信息，可以找到距离最近的配送员或仓库，并对订单进行分配。
- 地址查找：在地图应用中，可以通过Redis GEO快速查询某个地址周围的商家或服务设施。
- 动态信息：在滴滴、Uber等打车应用中，可以实时更新车辆的位置信息，以提供更加准确的车辆推荐和路线规划服务


#### Python GEO

用Google或Bing提供的geocoding服务，获取标准化的地理坐标等结构化信息

直接使用requests请求地图api

```py
# 用Google或Bing提供的geocoding服务，获取标准化的地理坐标等结构化信息
import requests
url = 'https://maps.googleapis.com/maps/api/geocode/json'
params = {'sensor': 'false', 'address': 'Mountain View, CA'}
r = requests.get(url, params=params)
results = r.json()['results']
if results:
    location = results[0]['geometry']['location']
    print(location['lat'], location['lng'])
else:
    print('结果为空')
```

工具包
- [geocoder](https://github.com/DenisCarriere/geocoder), [文档](https://geocoder.readthedocs.org/)

| Provider 服务提供商 | Optimal 范围 | Usage Policy |
| [ArcGIS](http://geocoder.readthedocs.org/providers/ArcGIS.html) | World | |
| [Baidu](http://geocoder.readthedocs.org/providers/Baidu.html) | China | API key |
| [Bing](http://geocoder.readthedocs.org/providers/Bing.html) | World | API key |
| [CanadaPost](http://geocoder.readthedocs.org/providers/CanadaPost.html) | Canada | API key |
| [FreeGeoIP](http://geocoder.readthedocs.org/providers/FreeGeoIP.html) | World | |
| [Geocoder.ca](http://geocoder.readthedocs.org/providers/Geocoder-ca.html) | CA & US | Rate Limit |
| [GeocodeFarm](https://geocode.farm/) | World | [Policy](https://geocode.farm/geocoding/free-api-documentation/)|
| [GeoNames](http://geocoder.readthedocs.org/providers/GeoNames.html) | World | Username |
| [GeoOttawa](http://geocoder.readthedocs.org/providers/GeoOttawa.html) | Ottawa | | 
| [Google](http://geocoder.readthedocs.org/providers/Google.html) | World | Rate Limit, [Policy](https://developers.google.com/maps/documentation/geocoding/usage-limits)|
| [HERE](http://geocoder.readthedocs.org/providers/HERE.html) | World | API key |
| [IPInfo](http://geocoder.readthedocs.org/providers/IPInfo.html) | World | |
| [Mapbox](http://geocoder.readthedocs.org/providers/Mapbox.html) | World | API key | 
| [MapQuest](http://geocoder.readthedocs.org/providers/MapQuest.html) | World | API key |
| [Mapzen](http://geocoder.readthedocs.org/providers/Mapzen.html) | World | API key | 
| [MaxMind](http://geocoder.readthedocs.org/providers/MaxMind.html) | World | |
| [OpenCage](http://geocoder.readthedocs.org/providers/OpenCage.html) | World | API key|
| [OpenStreetMap](http://geocoder.readthedocs.org/providers/OpenStreetMap.html) | World | [Policy](https://wiki.openstreetmap.org/wiki/Nominatim_usage_policy)|
| [Tamu](http://geoservices.tamu.edu/Services/Geocode/WebService/) | US | API key |
| [TomTom](http://geocoder.readthedocs.org/providers/TomTom.html) | World | API key | 
| [What3Words](http://geocoder.readthedocs.org/providers/What3Words.html) | World | API key|
| [Yahoo](http://geocoder.readthedocs.org/providers/Yahoo.html) | World | |
| [Yandex](http://geocoder.readthedocs.org/providers/Yandex.html) | Russia | |
| [TGOS](http://geocoder.readthedocs.org/providers/TGOS.html) | Taiwan ||


```py
#!pip install geocoder
import geocoder
# (1) 地理编码  GEO Forward
g = geocoder.google("1403 Washington Ave, New Orleans, LA 70130")
print('geo结果, 国外: ', g.latlng)
# 换成 arcgis服务
g = geocoder.arcgis(u"北京市海淀区上地十街10号")
print('ArcGIS, 国内: ', g.latlng, g.geojson)
print(g.json, g.wkt, g.osm)
# (2) 逆地理编码 GEO Reverse
g = geocoder.google([29.9287839, -90.08421849999999], method='reverse')
print('Google: ', g, g.address, g.city, g.state, g.country)
g = geocoder.arcgis([29.9287839, -90.08421849999999], method='reverse')
print('ArcGIS: ',g, g.address, g.city, g.state, g.country)
# ------ ip ------
g = geocoder.ip('199.7.157.0')
print(g.latlng, g.city)
g = geocoder.ip('me')
print(g.latlng, g.city)
```


#### Redis GEO

Redis GEO 主要用于存储地理位置信息，并对存储的信息进行操作，该功能在 Redis 3.2 版本新增。
- GEO 本质上是基于 ZSet 实现

Redis GEO 操作方法有：[geospatial官方](https://redis.io/docs/data-types/geospatial/), [geo方法](https://redis.io/commands/?group=geo)
- geoadd：添加地理位置的坐标。
- geopos：获取地理位置的坐标。
- `geodist`：计算两个位置之间的距离。
- `georadius`：根据用户给定的经纬度坐标来获取指定范围内的地理位置集合。
- `georadiusbymember`：根据储存在位置集合里面的某个地点获取指定范围内的地理位置集合。
- geohash：返回一个或多个位置对象的 geohash 值。
- geosearch: 

georadius、georadiusbymember
- georadius 以给定的经纬度为中心， 返回键包含的位置元素当中， 与中心的距离不超过给定最大距离的所有位置元素。
- georadiusbymember 和 GEORADIUS 命令一样， 都可以找出位于指定范围内的元素， 但是 georadiusbymember 的中心点是由给定的位置元素决定的， 而不是使用经度和纬度来决定中心点。


详情：

```sh
redis-cli 
redis-cli --raw # UTF8 中文显示 解决中文乱码

# key 为 user:location
# 添加位置信息
geoadd user:location 121.48941  31.40527 'shagnhai'
# 添加多个位置信息
geoadd user:location 121.47941 31.41527 'shanghai1'  121.47941 31.43527 'shagnhai2'  121.47941 31.40527 'shagnhai3'
# ----- 计算距离 ------
# 单位有m km ft(英尺） mi(英里）
# 计算两点间的距离，单位m
geodist user:location shanghai shanghai1 m # "1462.1834"
# 千米：km
geodist user:location shanghai shanghai1 km # "1.4622"
# ----- 计算geohash ------
# geohash 返回一个或多个位置元素的geohash，保存Redis中是用geohash位置52点整数编码
# geohash 将二维经纬度转换成字符串，每个字符串代表一个矩形区域，该矩形区域内的经纬度点都共享一个相同的geohash字符串。
geohash user:location shanghai shanghai1
# 1) "wtw6st1uuq0"
# 2) "wtw6sqfx5q0"
# geopos 从key里返回指定成员的位置信息
geopos user:location shanghai shanghai1
# 1) 1) "121.48941010236740112"
#    2) "31.40526993848380499"
# 
# 2) 1) "121.47941082715988159"
#    2) "31.41526941345740198"
# ----- 删除 ------
zrem site xiaoming
# ----- hash ------
geohash site tianan
# 1) "wx4g0cgp000"
# ----- 附近查询 ------
# georadius:给定经纬度为中心，返回键包含的位置元素中，与中心的距离不超过给定最大距离的所有位置元素
# 范围单位：m km mi ft
# withcoord:将位置元素的经纬度一并返回
georadius user:location 121.48941 31.40527 3000 m withcoord
# 1) 1) "shagnhai3"
#    2) 1) "121.47941082715988159"
#       2) "31.40526993848380499"
# 2) 1) "shanghai1"
#    2) 1) "121.47941082715988159"
#       2) "31.41526941345740198"
# 3) 1) "shanghai"
#    2) 1) "121.48941010236740112"
#       2) "31.40526993848380499"
georadius site 116.405419 39.913164 5 km withhash
# 1) 1) "tianan"
#    2) (integer) 4069885552230465
# 2) 1) "yuetan"
#    2) (integer) 4069879797297521
# withdist:返回位置元素的同时，将位置元素与中心点间的距离一并返回
georadius user:location 121.48941 31.40527 3000 m withdist
# 1) 1) "shagnhai3"
#    2) "949.2411"
# 
# 2) 1) "shanghai1"
#    2) "1462.1719"
# 
# 3) 1) "shanghai"
#    2) "0.0119"
# 指定返回满足条件位置的个数
georadius site 116.405419 39.913164 5 km count 1
# 1) "tianan"
# 排序
georadius site 116.405419 39.913164 5 km desc
# 1) "yuetan"
# 2) "tianan"
georadius site 116.405419 39.913164 5 km asc
# 1) "tianan"
# 2) "yuetan"
georadius site 116.405419 39.913164 5 km withdist desc
# 1) 1) "yuetan"
#    2) "4.0100"
# 2) 1) "tianan"
#    2) "0.0981"
# asc:根据中心位置，按照从近到远的方式返回位置元素
georadius user:location 121.48941 31.40527 3000 m withdist asc
# 1) 1) "shanghai"
#    2) "0.0119"
# 2) 1) "shagnhai3"
#    2) "949.2411"
# 3) 1) "shanghai1"
#    2) "1462.1719"
# desc: 根据中心位置，按照从远到近的方式返回位置元素
georadius user:location 121.48941 31.40527 3000 m withdist desc
# 1) 1) "shanghai1"
#    2) "1462.1719"
# 2) 1) "shagnhai3"
#    2) "949.2411"
# 3) 1) "shanghai"
#    2) "0.0119"
# count：获取指定数量的元素
georadius user:location 121.48941 31.40527 3000 m withdist desc count 2
# 1) 1) "shanghai1"
#    2) "1462.1719"
# 2) 1) "shagnhai3"
#    2) "949.2411"
# ----- 附近搜索: 位置元素为中心 ------
# georadiusbymember:和georadius命令类似，都可以找出指定位置范围内的元素，但是georadiusbymember的中心点是由给定位置元素决定的，而不像georadius使用经纬度决定中心点
georadiusbymember user:location shanghai 3 km 
# 1) "shagnhai3"
# 2) "shanghai1"
# 3) "shanghai"
# 替代  GEORADIUS and GEORADIUSBYMEMBER
GEOSEARCH Sicily FROMLONLAT 15 37 BYRADIUS 200 km ASC
# 1) "Catania"
# 2) "Palermo"
GEOSEARCH Sicily FROMLONLAT 15 37 BYBOX 400 400 km ASC WITHCOORD WITHDIST
# 存储结果
GEOSEARCHSTORE key1 Sicily FROMLONLAT 15 37 BYBOX 400 400 km ASC COUNT 3
GEOSEARCHSTORE key2 Sicily FROMLONLAT 15 37 BYBOX 400 400 km ASC COUNT 3 STOREDIST
```


Python连接Redis

```py
import redis   # 导入redis 模块
#r = redis.StrictRedis(host='localhost', port=6379, db=0)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  
# 连接池 
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True) # 连接池
r = redis.Redis(connection_pool=pool)
# 设置值
r.set('name', 'runoob')  # 设置 name 对应的值
print(r['name'])
print(r.get('name'))  # 取出键 name 对应的值
print(type(r.get('name')))  # 查看类型
# ----------------
import redis

r = redis.Redis(decode_responses=True)

res1 = r.geoadd("bikes:rentable", [-122.27652, 37.805186, "station:1"])
print(res1)  # >>> 1

res4 = r.geosearch(
    "bikes:rentable",
    longitude=-122.27652,
    latitude=37.805186,
    radius=5,
    unit="km",
)
print(res4)  # >>> ['station:1', 'station:2', 'station:3']

# 批量
cities = [('Rumilly', 5.9428591, 45.8676254), ('Sallanches', 6.6302551, 45.9361246)]
for city in cities : #For each city
    # GEOADD key longitude latitude member
    # key [latitude, longitude, name]
    r.geoadd("cities", city[2], city[1], city[0])
# 附近搜
r.georadiusbymember("cities", "Annecy", 6, unit="km") # [b'Annecy', b'Metz-Tessy', b'Argonay', b'Veyrier-du-Lac', b'Sevrier']


```

示例

```py
from redis import StrictRedis
 
resid_cli = StrictRedis(host="", port=xx, password="xx", db=xx, decode_responses=True)

# geoadd：添加地理位置（可以添加多个，模型是zset）
# key值 经度 纬度 名称
resid_cli.geoadd("beijing", 116.403963, 39.915119, "tiananmen", 116.403414, 39.924091, "gugong", 116.419342, 39.888663, "tiantan")
tian = resid_cli.zrange("beijing", 0, -1)
print(tian)
# geopos：查询位置信息
# key值 名称
pos = resid_cli.geopos("beijing", "tiananmen", "gugong", "tiantan")
print(pos)
# geodist：距离统计(单位默认为米)
# key值 两个位置名称 距离单位（默认为m）
juli = resid_cli.geodist("beijing", "tiananmen", "gugong", "km")
print(juli)
# georadius：查询距离某个位置指定直径范围内的点
# key值 经度 纬度 距离值 单位
other = resid_cli.georadius("beijing", 116.403963, 39.915119, 1, "m")
print(other)
 
# geohash：查询位置的哈希值
# key值 具体位置的名称
pos_hash = resid_cli.geohash("beijing", "tiananmen", "gugong")
print(pos_hash)
# zrem：删除地理位置
# key值 具体位置的名称
resid_cli.zrem("beijing", "tiananmen", "tiantan")
tian = resid_cli.zrange("beijing", 0, -1)
print(tian)

```

### GeoHash 


#### GeoHash 介绍

geohash 是一种公共域**地理编码系统**，作用是将**经纬度地理位置编码**为字母和数字组成的字符串，字符串也可解码为经纬度。每个字符串代表一个网格编号，字符串的长度越长则精度越高
- [空间索引之GeoHash](https://www.biaodianfu.com/geohash.html#GEOHASH%E7%9A%84%E5%8F%AF%E8%A7%86%E5%8C%96)
- ![](https://www.biaodianfu.com/wp-content/uploads/2020/10/Polygon.png)

根据[wiki](https://en.wikipedia.org/wiki/Geohash "wiki")，geohash字符串长度对应精度表格如下：  

Geohash算法的主要思想: 对某一数字通过二分法进行**无限逼近**
- 显然不可能让计算机执行无穷计算，加入执行N次计算，则x属于的区间长度为 (b-a)/2N+1 ,以纬度计算为例，则为 180/2N ，误差近似计算为: err= 180/2N+1 =90/2N ,如果N=20，则误差最大为：0.00009。但无论如何这样表明Geohash是一种近似算法。

|  geohash length(precision)   |   lat bits   |   lng bits   |   lat error   |   lng error   |   km error   | 
| --- | --- | --- | --- | --- | --- | 
|   1   |   2   |   3   |   ±23   |   ±23   |   ±2500   | 
|   2   |   5   |   5   |   ±2.8   |   ±5.6   |   ±630   | 
|   3   |   7   |   8   |   ±0.70   |   ±0.70   |   ±78   | 
|   4   |   10   |   10   |   ±0.087   |   ±0.18   |   ±20   | 
|   5   |   12   |   13   |   ±0.022   |   ±0.022   |   ±2.4   | 
|   6   |   15   |   15   |   ±0.0027   |   ±0.0055   |   ±0.61   | 
|   7   |   17   |   18   |   ±0.00068   |   ±0.00068   |   ±0.076   | 
|   8   |   20   |   20   |   ±0.000085   |   ±0.00017   |   ±0.019   | 


Geohash 几个特点：
- Geohash 用一个**字符串**表示**经度**和**纬度**两个坐标。在数据存储时可以简化为只为一列做索引。
- Geohash 表示的并不是一个点，而是一个**矩形区域**。使用者可以发布地址编码，既能表明自己大致位置，又不至于暴露自己的精确坐标，有助于隐私保护。
- Geohash 编码的前缀可以表示更大的区域。例如 wx4g0ec1，前缀wx4g0e表示包含编码wx4g0ec1在内的更大范围。 这个特性可以用于**附近地点搜索**。

#### 问题引入

【2023-8-9】[GeoHash 技术原理及应用实战](https://zhuanlan.zhihu.com/p/645078866)

场景
- 打开手机中的地图 app，检索附近1 公里范围内的餐馆，挑选合适的用餐地点

问题
- 如何对指定范围内的餐馆信息进行精确推送和展示
- ![](https://pic2.zhimg.com/80/v2-79b243c3135441d8f67405be3f5a806d_1440w.webp)

解法
- 暴力：遍历所有 经纬度坐标，选最近（不考虑3D城市重庆）

[geohash在线体验](geohash.org) 可以通过哈希值查询其对应的地理位置
- ![](https://ask.qcloudimg.com/http-save/yehe-2413530/n1e9izd7yw.jpeg)

#### 暴力解

简单粗暴的实现方式：
-   把地球上所有餐馆的 (lng,lat) 坐标都维护在一个 list 里
-   获取到小徐先生所在的北京人家的坐标 (lng0,lat0)
-   遍历 list 中所有餐馆的 (lng,lat) 坐标，求出和 (lng0,lat0) 的相对距离，如果大于指定距离就过滤，小于等于指定距离就保留
-   最终被保留在 list 中的餐馆集合就是我们所求的目标
- ![](https://pic4.zhimg.com/80/v2-dcbf193590cb60cd5ede62c0a720221b_1440w.webp)

分析
- 全量餐馆数据规模何其庞大，每次执行范围检索时都要全量遍历计算，工作量足以击垮任何一个服务集群.

#### 索引法

优化思路: 以空间换取时间. 

核心挑战: 如何合理设计用于存储位置信息的空间结构.

常规思路: 
- 利用**索引**提高检索效率
- 本场景中，每个位置是由二维的 (lng,lat) 坐标组成的，这要如何设计成索引呢？

geohash 把这种**二维经纬度坐标**转换成带**前缀索引**性质的**一维坐标**，这个特殊一维坐标称为"geohash 字符串". 

geohash 技术实现很大程度上保证两个 geohash 字符串<span style='color:blue'>公共前缀长度越长，两个区域距离就越接近，并且相对距离范围是可以通过公共前缀的长度估算出具体量级的</span>.
- 该性质只能做到 “**一定程度**上保证”
- 一些边界 case 中可能会出现两个位置本身距离很接近，但是 geohash 字符串的前缀却又差别很大的情况. 

将经纬度坐标(lng,lat) 转为一维 geohash 字符串的示例：

<table data-draft-node="block" data-draft-type="table" data-size="normal" data-row-style="normal"><tbody><tr><td>索引 index</td><td>点 point</td><td>经度 lng</td><td>纬度 lat</td></tr><tr><td>YJXY433V</td><td>A</td><td>101</td><td>77</td></tr><tr><td>Y8M76SJ6</td><td>B</td><td>120</td><td>47</td></tr><tr><td>K6BE10DN</td><td>C</td><td>12</td><td>-29</td></tr><tr><td>PBQE6KPD</td><td>D</td><td>178</td><td>-88</td></tr></tbody></table>


#### GeoHash 编码原理

将**球形**表面“展开”成了一张**矩形平面**，每个位置对应的(lnt,lat) 坐标都可以很方便的在矩形平面上进行定位.
- 沿着经度 -180/180° 的交接位置 “咔嚓”一刀将圆柱体的侧面纵向剪开，将其展开成一个矩形平面图
- 地球在纵向上由 -90°~90° 的纬度范围组成,在横向上由 -180°~180° 的经度范围组成. 因此我们把球面投影成一个矩形平面后，矩形的宽、高刻度就分别对应着经度和纬度，宽度方向上自左向右以 -180°为起点，180°为终点，每个刻度的单位为 1° 经度；高度自底向上以 -90°为起点，90°为终点，每个刻度单位为 1° 纬度.

|示意图|球面|平面|
|---|---|---|
||![](https://pic3.zhimg.com/80/v2-2a47c3c2974119aca084bc4d42043e6e_1440w.webp)|![](https://pic1.zhimg.com/80/v2-4cfd5b8992d3c39046d3faa80bd09064_1440w.webp)|


变换过程
- 沿着**经度**（矩形宽度）的方向进行递归二分，将一个具体经度拆解成一个由二进制数字组成的字符串.
  - 第一轮：经度范围为 -180°~180°，可以拆分成 -180°~0° 以及 0°~180° 两部分，如果经度从属于前者，则令首个 bit 位取 0，否则令首个 bit 位取 1；
  - 第二轮：-180°~0° 可以拆分为 -180°~-90° 和 -90°~0°，如果经度从属于前者，则令第二个 bit 位取 0，否则令第二个 bit 位取 1；0°~180° 可以拆分为 0°~90° 和 90°~180°，前者令第二个 bit 位取 0，后者令第二个 bit 位取 1
  - 第 3 ~ N 轮：重复上述步骤的思路，最终递归二分，将经度表示成一个由二进制数字组成的字符串
  - 经度 116.3906 编码为: 1101 0010 1100 0100 0100
  - ![](https://www.biaodianfu.com/wp-content/uploads/2020/10/lng.png)
- 同样在**纬度**（矩形高度）的递归二分当中，最终每个具体的纬度也可以被拆分成一个由二进制数字组成的字符串.
  - 纬度 39.92324 编码为: 1011 1000 1100 0111 1001
  - ![](https://www.biaodianfu.com/wp-content/uploads/2020/10/lat.png)
- 将沿经度方向的切分和沿纬度方向的切分**合并**在一起，于是整个矩形平面会被切割成网状，形成一个个小的矩形块.
  - 将经度和纬度的编码合并，奇数位是纬度，偶数位是经度，得到编码 11100 11101 00100 01111 00000 01101 01011 00001。最后，用0-9、b-z（去掉a, i, l, o）这32个字母进行base32编码，得到(39.92324, 116.3906)的编码为wx4g0ec1。

空间划分为四块，编码顺序分别是左下角00，左上角01，右下脚10，右上角11，类似于Z的曲线，当递归分解成更小的子块时，编码的顺序是**自相似**的（分形），每一个子快也形成`Z曲线`，称为`Peano空间填充曲线`。
- ![](https://www.biaodianfu.com/wp-content/uploads/2020/10/geohash-2.jpg)

Peano空间填充曲线
- 优点: 将二维空间转换成一维曲线（事实上是分形维），对大部分而言，编码相似的距离也相近
- 缺点: **突变性**
  - 有些编码相邻但距离却相差很远，比如0111与1000，编码是相邻的，但距离相差很大。

- ![](https://www.biaodianfu.com/wp-content/uploads/2020/10/geohash-1.png)

其它空间填充曲线
- 效果公认较好是`Hilbert空间填充曲线`，相较于`Peano曲线`，`Hilbert曲线`没有较大的突变。
- 为什么GeoHash不选择`Hilbert空间填充曲线`呢？可能是Peano曲线思路以及计算上比较简单，事实上，`Peano曲线`就是一种**四叉树**线性编码方式。

每个矩形块经度区间，会对应有一个经度二进制字符串；同时根据纬度区间，也会有一个纬度二进制字符串. 化二维为一维的关键就是按照经度字符串+纬度字符串依次交错排列的形式，将其组织在一起，最终形成一个一维字符串.
- 这个一维字符串的位数越多，意味着对应的矩形块就越小；同时拥有相同前缀的小矩形块必然从属在同一个大矩形块的范围之内，比如下图左上方的 4 个小矩形：0101、0111、0100、0111 都拥有着公共前缀 "01"，因此，他们都从属于由 "01"表示的这个大矩形块当中.

一维字符串具有前缀索引的性质，他能够保证两个字符串前缀匹配位数越长，两个矩形块的相对位置就越靠近。
- ![示意图](https://pic2.zhimg.com/80/v2-08738864cf35255759b650304b80f395_1440w.webp)

|经度|纬度|合并|
|---|---|---|
|![](https://pic1.zhimg.com/80/v2-f49beb4f7d33b5063cffc7a54a3fef08_1440w.webp)|![](https://pic3.zhimg.com/80/v2-083900d3cd3f593ce896ca0685044b0e_1440w.webp)|![](https://pic4.zhimg.com/80/v2-1316f134d93b33d21d4a034e546d129b_1440w.webp)|

geohash 编码格式
- 为了进一步节省空间，geohash 采用 Base32 编码替代了原始的二进制字符串.
- Base32 编码主要是以 10 个数字字符 ‘0’-‘9’ 加上 26 个英文字母 ‘A’-‘Z’ 组成，并在其中把几个容易产生混淆的字符 'I' 'L' 'O' 以及字母 'A' 去掉了，最终总计保留下来 32 个字符

遵循 geohash 思路，将一个二进制字符串转为 Base32 编码形式的示例：
- ![](https://pic4.zhimg.com/80/v2-1ad764cbfae3103a3ca165bfb336c8ff_1440w.webp)

将地球表面上每个递归二分得到的小矩形块表示成 geohash 字符串的形式. 下图是通过 6 位 geohash 字符串，对北京西二旗附近区域进行切分表示的示例：
- ![](https://pic1.zhimg.com/80/v2-d9ffc0645f3ec66cdde09f2739922b28_1440w.webp)

**长度决定精度**

在 geohash 字符串中，字符串的长度决定了矩形块的大小，进一步决定了距离的精度. 在对经纬度进行递归二分时，每多一轮二分，矩形一个方向上的边长就会减半，因此矩形区域就越小，对应的精度就越高. 下面是 geohash 字符串长度和距离精度的映射关系：

<table data-draft-node="block" data-draft-type="table" data-size="normal" data-row-style="normal"><tbody><tr><td>geohash字符串长度（base32）</td><td>lat bits纬度二进制位数</td><td>lng bits经度二进制位数</td><td>lat error纬度方向长度（°）</td><td>lng error经度方向长度（°）</td><td>km error矩形边长（km）</td></tr><tr><td>1</td><td>2</td><td>3</td><td>±23</td><td>±23</td><td>±2500</td></tr><tr><td>2</td><td>5</td><td>5</td><td>±2.8</td><td>±5.6</td><td>±630</td></tr><tr><td>3</td><td>7</td><td>8</td><td>±0.70</td><td>±0.70</td><td>±78</td></tr><tr><td>4</td><td>10</td><td>10</td><td>±0.087</td><td>±0.18</td><td>±20</td></tr><tr><td>5</td><td>12</td><td>13</td><td>±0.022</td><td>±0.022</td><td>±2.4</td></tr><tr><td>6</td><td>15</td><td>15</td><td>±0.0027</td><td>±0.0055</td><td>±0.61</td></tr><tr><td>7</td><td>17</td><td>18</td><td>±0.00068</td><td>±0.00068</td><td>±0.076</td></tr><tr><td>8</td><td>20</td><td>20</td><td>±0.000085</td><td>±0.00017</td><td>±0.019</td></tr></tbody></table>

geohash 实现步骤
- 取得经纬度
  - 如经纬度信息：(116.311126,40.085003)
- 经度递归二分
  - 预期生成的 geohash 字符串长度为 6 位，则对应的经度和纬度二进制字符串的 bit 位长度需要为 15 位. 最终取得的 geohash 字符串所对应的矩形块边长范围约为 610 m.
  - 最终，递归二分得到经度方向上的二进制字符串为 110100101011010，长度为 15 位.
- 纬度递归二分： 对经度 40.085003 进行二分，首轮从 -90°~90°的范围开始
  - 最终，递归二分得到纬度方向上的二进制字符串为 101110010000001，长度为 15 位.
- 经纬度字符串拼接
  - 结合经度字符串 110100101011010 和纬度字符串 101110010000001，我们遵循先经度后纬度的顺序，逐一交错排列，最终得到的一维字符串为 11100 11101 00100 11000 10100 01001.
  - ![](https://pic3.zhimg.com/80/v2-57d0f241933ee63175c03c431a29f50e_1440w.webp)
- Base32编码
  - 一维二进制字符串 11100 11101 00100 11000 10100 01001 的基础上，我们从左往后，以每 5 个 bit 成一组，转为 Base32 编码的表达形式，最终得到的编码结果为 WX4SN9
  - ![](https://pic1.zhimg.com/80/v2-4a50c91bc1e82ce5ec4b5589af026ec4_1440w.webp)


#### GeoHash 解码原理

解码算法与编码算法相反，先进行 base32解码，然后分离出经纬度，最后根据二进制编码对经纬度范围进行细分即可。


#### geohash 具体实现


##### Python 实现

摩拜单车举行的**单车停放点位置预测**竞赛中的数据起始位置和终止位置是经过geohash算法编码。
- [参考](https://www.modb.pro/db/38115)

可用Python的 [geohash](https://pypi.org/project/Geohash/) 包来进行解析

```sh
pip install Geohash
```

```py
import Geohash

print(Geohash.encode(30.723514, 104.123245, precision=5))  # wm6nc
print(Geohash.decode("wm6nc"))  # (30.73974609375, 104.12841796875)
print(Geohash.decode("wm6nc", delta=True))  # (30.73974609375, 104.12841796875, 0.02197265625, 0.02197265625)
print(Geohash.decode_exactly("wm6nc"))  # (30.73974609375, 104.12841796875, 0.02197265625, 0.02197265625)
# -------------
from Geohash import geohash
import pandas as pd

# 调用Geohash库的decode方法，定义解码函数
def decode_data(data):
    # geohash → 经纬度
    return geohash.decode(data)

if __name__ == '__main__':
    # 读取数据
    df_data = pd.read_csv('ceshi.csv')
    # 使用apply方法，调用解码方法进行解码
    df_data['start_loc'] = df_data['geohashed_start_loc'].apply(decode_data)
    df_data['end_loc'] = df_data['geohashed_end_loc'].apply(decode_data)
    # 预览
    print(df_data)
    # 保存
    df_data.to_csv('result.csv')
```

Python 的 TransBigData 包中提供了geohash的处理功能，主要包括三个函数：

```sh
# 输入经纬度与精度，输出geohash编码
transbigdata.geohash_encode(lon, lat, precision=12)
# 输入geohash编码，输出经纬度
transbigdata.geohash_decode(geohash)
# 输入geohash编码，输出geohash网格的地理信息图形Series列
transbigdata.geohash_togrid(geohash)
```

相比`TransBigData`包中提供的方形栅格处理方法，`geohash`更慢，也无法提供自由定义的栅格大小。下面的示例展示如何利用这三个函数对数据进行geohash编码集计，并可视化
- [Python实现geohash编码与解码（TransBigData）](https://blog.csdn.net/u013410354/article/details/121304947)

```py
import transbigdata as tbd
import pandas as pd
import geopandas as gpd
# 读取数据
data = pd.read_csv('TaxiData-Sample.csv',header = None)
data.columns = ['VehicleNum','time','slon','slat','OpenStatus','Speed']

# 依据经纬度geohash编码，精确度选6时，栅格大小约为±0.61km
data['geohash'] = tbd.geohash_encode(data['slon'], data['slat'], precision=6)
data['geohash']

# 基于geohash编码集计
dataagg = data.groupby(['geohash'])['VehicleNum'].count().reset_index()
# geohash编码解码为经纬度
dataagg['lon_geohash'],dataagg['lat_geohash'] = tbd.geohash_decode(dataagg['geohash'])
# geohash编码生成栅格矢量图形
dataagg['geometry'] = tbd.geohash_togrid(dataagg['geohash'])
# 转换为GeoDataFrame
dataagg = gpd.GeoDataFrame(dataagg)
dataagg

# 设定绘图边界
bounds = [113.6,22.4,114.8,22.9]
# 创建图框
import matplotlib.pyplot as plt
import plot_map
fig =plt.figure(1,(8,8),dpi=280)
ax =plt.subplot(111)
plt.sca(ax)
# 添加地图底图
tbd.plot_map(plt,bounds,zoom = 12,style = 4)
# 绘制colorbar
cax = plt.axes([0.05, 0.33, 0.02, 0.3])
plt.title('count')
plt.sca(ax)
# 绘制geohash的栅格集计
dataagg.plot(ax = ax,column = 'VehicleNum',cax = cax,legend = True)
# 添加比例尺和指北针
tbd.plotscale(ax,bounds = bounds,textsize = 10,compasssize = 1,accuracy = 2000,rect = [0.06,0.03],zorder = 10)
plt.axis('off')
plt.xlim(bounds[0],bounds[2])
plt.ylim(bounds[1],bounds[3])
plt.show()
```




##### Go 实现

geohash 
- 转换
  - ![](https://pic2.zhimg.com/80/v2-66fb7497cf630241cbcb4dcbd011afb5_1440w.webp)
- 查询
  - ![](https://pic3.zhimg.com/80/v2-c662d8aa82cb45762bc6453735b47ef6_1440w.webp)
- 添加
  - ![](https://pic1.zhimg.com/80/v2-4571fdba68cf186472a82d0b285c8250_1440w.webp)
- 前缀查询
  - ![](https://pic4.zhimg.com/80/v2-ca4712cf466ac9e65b29e78738bfa317_1440w.webp)
- 删除
  - ![](https://pic1.zhimg.com/80/v2-487cf51a237a793325d63a202e085f9c_1440w.webp)
- 范围查询
  - ![](https://pic2.zhimg.com/80/v2-5301cd681bfe8308816ea78c245a0ead_1440w.webp)

go 源码见[原文](https://zhuanlan.zhihu.com/p/645078866)

geohash 与 trie
- 首先要对 geohash 字符串的存储数据结构进行选型.

geohash 服务模块需要对外提供的几个 API 整理如下：
- Hash：将用户输入的经纬度 lng、lat 转为 geohash 字符串
- Get：通过传入的 geohash 字符串，获取到对应于矩形区域块的 GEOEntry 实例
- Add：通过用户传入的经纬度 lng、lat，构造出 point 实例并添加到对应的矩形区域中
- ListByPrefix：通过用户输入的 geohash 字符串，获取到对应矩形区域块内所有子矩形区域块的 GEOEntry 实例（包含本身）
- Rem：通过用户输入的 geohash 字符串，删除对应矩形区域块的 GEOEntry
- ListByRadiusM：通过用户输入的中心点 lng、lat，以及对应的距离范围 radius，返回范围内所有的点集合

#### geohash 问题


(1) **边缘性局限**问题

- 将矩形平面通过递归二分的方式，切分成一个个小的矩形块，而每个矩形块有着自己与毗邻矩形块的交界区域，倘若有两个点分别从属于两个毗邻矩形块，但是又同时靠近于它们的交界线，此时就会出现两个点实际距离接近，但前缀匹配长度不足的情况.
- ![](https://pic1.zhimg.com/80/v2-b2aa459166b4d4fd4fa5d5c65d087f50_1440w.webp)
- A、B 两个点同属于一个矩形块中，有着更长的公共前缀；C、D、E 三个点和 A 不从属于同一个矩形块，与A 的 geohash 字符串前缀匹配长度相较于 B 而言要更短，然而其本身和 A 的相对距离却是要更接近的.

为了避免在近距离位置检索过程中出现目标的遗漏，通常会在通过 geohash 锁定一个小的矩形块后，以其作为中心，将周围 8 个矩形块范围内的点也同时检索出来，再根据实际的相对距离进行过滤.

(2) 最短距离问题

找到距离点 A 最近的目标点. 以 A 所在矩形为中心，基于“回”字形的拓扑结构向外逐层向外拓宽，此时我们是无法保证靠内侧的“回”字形层次中出现的目标点一定比外层的点距离点 A 更近.

比如以下图为例，点 F 相比于点 G ，在层次上与点 A 更加靠近，但是实际上与点 A 的相对距离要长于点 G.
- ![](https://pic4.zhimg.com/80/v2-e4b6e8e1a16a14887848fb324f262ef3_1440w.webp)

为了解决这个问题，遇到首个目标点后，额外向外扩展几圈，直到保证扩展范围边界与点 A 的相对距离已经长于首个目标点后才能停止扩展流程. 接下来需要取出扩展范围内所有的点，分别计算出与点 A 的相对距离，最终取出距离最小的那个点，即为我们所求的结果.

(3) 范围检索思路

应用 geohash 技术的一类场景是：
> 给定一个指定位置作为中心点，想要检索出指定半径范围内的所有点集合.

解决思路
- 首先求出中点所在的矩形块及其对应的 geohash 字符串
- 然后基于回字形向外逐层拓宽，直到能保证拓展范围一定能完全包含以中心点为圆心、指定距离为半径的圆后，求出拓展范围内所有的点（此时可能有多余的结果），再通过其与中心点的相对距离进行过滤，保留满足条件的目标点集合.
  - ![](https://pic3.zhimg.com/80/v2-a2367bce85a3042881be976781a9e612_1440w.webp)




## 定位


### js 获取浏览器位置

【2017-3-15】[使用JavaScript获取位置](https://www.jianshu.com/p/5956252e6b8c)

本地资源（location sources）
- JavaScript提供了一个简单但功能强大的工具来定位设备的地理定位API的形式。包括一个小的一组易于使用的方法，可以获得设备的位置：
  - `GPS`: 主要在移动设备，精确到**10米**
  - `WIFI`: 几乎所有的联网设备
  - `IP`: 仅限于区域，备选方案
- 采用哪种方案取决于浏览器支持，一般情况下WIFI快于GPS快于IP

Geolocation
- 通过使用GPS、WIFI、IP地址检测自己的位置信息，开发人员可使用这些信息给用户提供更好的搜索建议，比如附近的便利店，并实现互动。
- 大部分浏览器支持geolocation
- geolocation api会暴露用户信息，所以当应用程序访问的时候，将以弹窗请求用户操作

geolocation api
通过使用caniuse-cmd，

navigator.geolocation有如下几个方法：

```js
Geolocation.getCurrentPosition() // 获取当前位置
Geolocation.watchPosition() // 监测定位
Geolocation.clearWatch() // 清除监测
// getCurrentPosition() and watchPosition() methods 的工作方式是基本相同

navigator.geolocation.getCurrentPosition(
    // 位置获取成功
    function(position) {
        position = {
            coords: {
                latitude - //纬度.
                longitude - //经度. 
                altitude - //高度.
                accuracy - //精确度. 
                altitudeAccuracy - //高度的准确性. 
                heading - //. 
                speed - //.
            }
            timestamp - //时间戳.
        }
    },
    // 位置获取失败
    function(error){

    }
);
```

一个简单的Demo
- [Geolocation Demo](https://jsfiddle.net/dannymarkov/ubrvm4ao/), google 地图显示位置

```js
findMeButton.on("click", function(){
    navigator.geolocation.getCurrentPosition(function(position) {
        // Get the coordinates of the current position.
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        // Create a new map and place a marker at the device location.
        var map = new GMaps({
            el: "#map",
            lat: lat,
            lng: lng
        });
        map.addMarker({
            lat: lat,
            lng: lng
        });
    });
});
```

更多[示例](https://www.runoob.com/try/try.php?filename=tryhtml5_geolocation)

```html
<title>菜鸟教程(runoob.com)</title> 
</head>
<body>
<p id="demo">点击按钮获取您当前坐标（可能需要比较长的时间获取）：</p>
<button onclick="getLocation()">点我</button>
<script>
var x=document.getElementById("demo");
function getLocation()
{
	if (navigator.geolocation)
	{
		navigator.geolocation.getCurrentPosition(showPosition);
	}
	else
	{
		x.innerHTML="该浏览器不支持获取地理位置。";
	}
}

function showPosition(position)
{
	x.innerHTML="纬度: " + position.coords.latitude + 
	"<br>经度: " + position.coords.longitude;	
}
</script>
</body>
</html>
```

### 手机定位方式

手机常用的定位方式有：
- 卫星定位(GPS，北斗，伽利略，Glonass)；
- 移动基站定位；
- WiFi辅助定位；
- AGPS定位。

注
- IPhone系统比较封闭，对用户隐私保护较好，微信对用户隐私保护也很好，不容易获取

参考
- [常见手机定位方式](https://www.cnblogs.com/syfwhu/p/5084115.html)

### 定位轨迹数据

如何获取自己的定位信息?
- 旅游软件 [六只脚](http://www.foooooot.com/) app支持跟踪定位轨迹并导出数据(gpx格式)

gpx 格式提取

国内地图产品导出的`.gpx`文件一般使用的是**非**`WGS84`坐标系  [参考](https://blog.csdn.net/wangpeng246300/article/details/108901305)
- 如果想要将该`.gpx`文件导入到只支持WGS84坐标系的设备使用时，坐标将发生偏移，因此需要对`.gpx`文件进行坐标系转换。  
- Github和搜索引擎上并没有搜到将`.gpx`文件进行坐标转换的资料，但是将`.csv`文件或直接对坐标点进行转换的代码有很多。所以决定对代码进行修改使其支持直接对`.gpx`文件转换。

.gpx文件其实可以看成是一种xml文件
- gpx文件将每一个坐标点的**经纬度**、**高度**和**时间**记录下来，以此来生成轨迹。
- 所以将.gpx文件中的坐标点提取到，并对该坐标点进行**坐标系转换**，之后再将转换后的坐标写入新文件内，从而实现.gpx文件的坐标转换。
- 转换代码:[coordTransform.py](https://github.com/SoufSilence/coordTransform_py), 提供`百度坐标系`(bd-09)、`火星坐标系`(国测局坐标系、gcj02)、`WGS84坐标系`直接的坐标互转，也提供了解析高德地址的方法的python版本

转换工具
- [GPX到SVG转换器](https://products.aspose.app/gis/zh/viewer/gpx-to-svg)
- 在线提取：[mygeodata](https://mygeodata.cloud/), 下载解压后，轨迹信息在 track_points.csv 中
- [GPSBabel](https://www.gpsbabel.org)
- [gpxcsv](https://github.com/astrowonk/gpxcsv)

```sh
# == gpsbabel ==
gpsbabel -i unicsv -f input-file.csv -o gpx -F output-file.gpx
# == gpxcsv ==
pip install gpxcsv
# csv
gpxcsv myrun.gpx
gpxcsv myrun.gpx -o myfirstrun.csv
# json
gpxcsv myrun.gpx --json
python myrun.gpx -o out.json
# list
from gpxcsv import gpxtolist
gpx_list = gpxtolist('myfile.gpx')
#if you have pandas
import pandas as pd
df = pd.DataFrame(gpx_list)
```

python 转换

```py
# pip install gpx_converter
from gpx_csv_converter import Converter
# === gpx -> csv ===
Converter(input_file="/Users/bytedance/Downloads/wqw.gpx", output_file="output.csv")
# === csv -> gpx ===
# id,latitude,longitude
# 0,51.74333,12.122905000000001
# 538,51.7433216,12.122895
Converter(input_file='your_input.csv').csv_to_gpx(lats_colname='latitude',
                                                 longs_colname='longitude',
                                                 output_file='your_input.gpx')
```


### 1. 基站定位

因为处在相同频率范围的信号会相互干扰，为防止相邻基站相互干扰，相邻的基站会选择不同的信道（不同频率范围的信号）与移动设备通信。如上图是一个蜂窝移动基站的示意图，其任意相邻的两个基站都具有不同的通信频段。基站不是孤立存在的，其覆盖区域相互交接，组成一张巨大的移动通信网络（如下图）。

![](https://images2015.cnblogs.com/blog/716683/201512/716683-20151228214055385-1589270682.png)

图4 蜂窝基站

移动设备在插入sim卡开机以后，会主动搜索周围的基站信息，与基站建立联系，而且在可以搜索到信号的区域，手机能搜索到的基站不止一个，只不过远近程度不同，再进行通信时会选取距离最近、信号最强的基站作为通信基站。其余的基站并不是没有用处了，当你的位置发生移动时，不同基站的信号强度会发生变化，如果基站A的信号不如基站B了，手机为了防止突然间中断链接，会先和基站B进行通信，协调好通信方式之后就会从A切换到B。这也就是为什么同样是待机一天，你在火车上比在家里耗电要多的原因，手机需要不停的搜索、连接基站。每次坐火车，我都会把手机调成飞行模式，看看电影、听听歌，依然可以维持很长时间。
- ![移动网络](https://images2015.cnblogs.com/blog/716683/201512/716683-20151228214118464-194485334.png)

如上图所示，在这张巨大移动网络中，根据你所在的小区，所从属的基站就可大致知道你的位置信息，如果再加上一些估计算法，就可以更确切的找出你的位置。

#### 基站定位原理

移动电话测量不同基站的下行导频信号，得到不同基站下行导频的TOA（到达时刻）或 TDOA(到达时间差)，根据该测量结果并结合基站的坐标，一般采用三角公式估计算法，就能够计算出移动电话的位置。实际的位置估计算法需要考虑多基站(3个或3个以上)定位的情况，因此算法要复杂很多。一般而言，移动台测量的基站数目越多，测量精度越高，定位性能改善越明显。

直白的说，距离基站越远，信号越差，根据手机收到的信号强度可以大致估计距离基站的远近，当手机同时搜索到至少三个基站的信号时（现在的网络覆盖这是很轻松的一件事情），大致可以估计出距离基站的远近；基站在移动网络中是唯一确定的，其地理位置也是唯一的，也就可以得到三个基站（三个点）距离手机的距离，根据三点定位原理，只需要以基站为圆心，距离为半径多次画圆即可，这些圆的交点就是手机的位置。网传的微信三点定位原理也是这个样子。
- ![三点定位原理](https://images2015.cnblogs.com/blog/716683/201512/716683-20151228214148073-177650567.png)

由于基站定位时，信号很容易受到干扰，所以先天就决定了它定位的不准确性，精度大约在150米左右，基本无法开车导航。定位条件是必须在有基站信号的位置，手机处于sim卡注册状态（飞行模式下开wifi和拔出sim卡都不行），而且必须收到3个基站的信号，无论是否在室内。但是，定位速度超快，一旦有信号就可以定位，目前主要用途是没有GPS且没有wifi的情况下快速大体了解下你的位置。另外，如果手机里没有基站位置数据包，还需要联网才行。

### 2. WiFi定位

WiFi（也就是Wireless Access Point：AP，或者无线路由器）定位的方法有很多种，例如可以依据测信号强度来判定目标的距离，也可以依据信号角度来检测目标的方向和角度，依据相位，时间和时间差来初步判定目标距离AP的位置等等。

#### WiFi定位原理

-   每一个无线AP（路由器）都有一个全球唯一的MAC地址，并且一般来说无线AP在一段时间内不会移动；
-   设备在开启Wi-Fi的情况下，无线路由器默认都会进行SSID广播（除非用户手动配置关闭该功能），在广播帧包含了该路由器的MAC地址；
-   采集装置可以通过接收周围AP发送的广播信息获取周围AP的MAC信息和信号强度信息，将这些信息上传到服务器，经过服务器的计算，保存为“MAC-经纬度”的映射，当采集的信息足够多时候就在服务器上建立了一张巨大的WiFi信息网络；
-   当一个设备处在这样的网络中时，可以将收集到的这些能够标示AP的数据发送到位置服务器，服务器检索出每一个AP的地理位置，并结合每个信号的强弱程度，计算出设备的地理位置并返回到用户设备，其计算方式和基站定位位置计算方式相似，也是利用三点定位或多点定位技术；
-   位置服务商要不断更新、补充自己的数据库，以保证数据的准确性。当某些WiFi信息不在数据库中时，可以根据附近其他的WiFi位置信息推断出未知WiFi的位置信息，并上传服务器。

![WiFi 定位](https://images2015.cnblogs.com/blog/716683/201512/716683-20151229111557057-1002615358.gif)


#### 数据采集

这些AP位置映射数据怎么采集的呢？其采集方式大致可以分为主动采集和用户提交。

**主动采集**：

谷歌的街景拍摄车还有一个重要的功能就是采集沿途的无线信号并打上通过GPS定位出的坐标回传至服务器，Skyhook公司也是采用这样的方式。

**用户提交**：

Android手机用户在开启“使用无线网络定位”时会提示是否允许使用Google的定位服务，如果允许，用户的位置信息就被谷歌收集到。iPhone则会自动收集WiFi的MAC地址、GPS位置信息、运营商基站编码等，并发送给苹果公司的服务器。

由上面的介绍可知，WiFi定位在AP密集的地方有很好的效果，比如在GPS不能使用的室内，而且具有较快的反映速度，在不连上WiFi的情况下也可以定位，这就是有时候在不开数据服务时百度地图提示打开WiFi功能定位的原因。由于其依赖于WiFi，如果不想让人通过这种方式知道你的位置信息，直接关闭WLAN功能即可。

### 3. AGPS定位 

AGPS（AssistedGPS：辅助全球卫星定位系统）是结合GSM/GPRS与传统卫星定位，利用基地台代送辅助卫星信息，以缩减GPS芯片获取卫星信号的延迟时间，受遮盖的室内也能借基地台讯号弥补，减轻GPS芯片对卫星的依赖度。AGPS利用手机基站的信号，辅以连接远程定位服务器的方式下载卫星星历 (英语：Almanac Data)，再配合传统的GPS卫星接受器，让定位的速度更快。是一种结合网络基站信息和GPS信息对移动台进行定位的技术，既利用全球卫星定位系统GPS，又利用移动基站，解决了GPS覆盖的问题，可以在2代的G、C网络和3G网络中使用。

普通的GPS系统是由GPS卫星和GPS接受器组成，与普通的GPS不同，AGPS在系统中还有一个辅助定位服务器。在AGPS网络中，接收器可通过与辅助服务器的通信而获得定位辅助。由于AGPS接收器与辅助服务器间的任务是互为分工的，所以AGPS往往比普通的GPS系统有速度更快的定位能力、有更高的效率，可以很快捕捉到GPS信号，这样的首次捕获时间将大大减小，一般仅需几秒的时间（单纯GPS接收机首次捕获时间可能要2～3分钟时间），而精度也仅为几米，高于GPS的精度。 利用AGPS接收器不必再下载和解码来自GPS卫星的导航数据，因此可以有更多的时间和处理能力来跟踪GPS信号，这样能降低首次定位时间，增加灵敏度以及具有最大的可用性。

#### AGPS定位基本步骤

-   AGPS手机首先将本身的基站地址信息通过网络传输到定位服务器； 
-   定位服务器根据该手机的大概位置传输与该位置相关的GPS辅助信息（包含GPS的星历和方位俯仰角等）到手机； 
-   该手机的AGPS模块根据辅助信息（以提升GPS信号的第一锁定时间TTFF能力）接收GPS原始信号； 
-   手机在接收到GPS原始信号后解调信号，计算手机到卫星的伪距（伪距为受各种GPS误差影响的距离），并将有关信息通过网络传输到定位服务器； 
-   定位服务器根据传来的GPS伪距信息和来自其他定位设备（如差分GPS基准站等）的辅助信息完成对GPS信息的处理，并估算该手机的位置； 
-   定位服务器将该手机的位置通过网络传输到定位网关或应用平台（如手机上的GPS应用程序）。

![AGPS定位](https://images2015.cnblogs.com/blog/716683/201512/716683-20151228214240526-1332226721.png)

AGPS的优势主要在其定位精度上。在室外等空旷地区，其精度在正常的GPS工作环境下，可达10米左右，堪称目前定位精度最高的一种定位技术。另一优点为：首次捕获GPS信号的时间一般仅需几秒，不像GPS的首次捕获时间可能要2～3分钟。虽然AGPS技术的定位精度很高、首次捕获GPS信号时间短，但是该技术也存在着一些缺点。首先，室内定位的问题目前仍然无法圆满解决。另外，AGPS的定位实现必须通过多次网络传输（最多可达六次单向传输），这对运营商来说是被认为大量的占用了空中资源，对消费者而言将产生不少的流量费用。而且AGPS手机比一般手机在耗电上有一定的额外负担，间接减短了手机的待机时间。除此之外，有时无法取得多个卫星传来的讯号，通常这是因为您的AGPS 话机天线接收器所在环境的限制。在这种情况下，AGPS 功能将不能很好地使用。


### 4. 卫星导航系统

常见的卫星定位系统： `GPS`、`北斗`、`伽利略`和`Glonass`

虽然这些系统提供的服务有些差异，但其背后的定位原理都是相同，现在以应用最广泛的GPS为例来介绍卫星定位。

《日本经济新闻》2020年8月20日报道，美国长期以来一直是全球卫星定位系统的领导者，但现在，中国的北斗卫星导航系统在规模上已经超过美国的GPS。
- [中国北斗与美国GPS差距有多大？核心数据曝光，日媒惊叹](https://zhuanlan.zhihu.com/p/79153773)

全球4大卫星导航系统对比

| 系统 | GPS | 北斗 | GLONASS | Galileo |
|---|---|---|---|---|
| 研制国家 | 美国 | 中国 | 俄罗斯 | 欧盟 |
| 首颗卫星升空时间 | 1985年 | 1989年 | 2000年 | 2011年 |
| 卫星总数 | 43颗 | 38颗 | 24颗 | 30颗 |
| 应用时间 | 1994年 | 2000年北斗一号、2012年北斗二号、2020年北斗三号 | 2016年（早期工作能力) | 2007年（服务俄罗斯)、2009年(服务全球) |
| 竞争优势 | 成熟 | 开放且具备短信通信功能 | 抗干扰能力强 | 精度高 |
| 后期发展 | 预计于2033年部署完成由GPS三代卫星组成的空间星座，届时定位精度可达：水平2.1m、高程3.2m | 预计于2020年完成全球覆盖，届时定位精度最高可达2.5m | 计划于2025年前将其更新为GLONASS-K，系统届时定位精度可达3m | 预计于2019年建成，届时将具备完全工作能力，最高精度可达1m以内 |

GPS仅向地面发送信号，难以锁定接收信号的终端的位置信息，但北斗还有一点优势，它具备收发信号的功能。

美国曾借助GPS在全球定位服务领域先行一步，而中国正一步步夺取美国的地位。可以清晰地看到，在卫星领域中国已开始反超美国。

卫星导航定位行业按照定位精度差别可区分为两大服务群体：
- 一是**高精度GNSS**行业（常规使用的定位误差在**米级**以下），应用在测绘勘探、地理信息、地质灾害监测、精细农林业、国防、时间同步等领域
- 二是**消费类**行业（常规使用的定位误差在1米至**10米**以上），例如手机导航、车载导航等。近年来，随着大数据、物联网特别是无人驾驶等新兴技术的不断进步，用定位精度来区分服务群体的界限已逐渐模糊。例如高精度定位在无人驾驶技术中占据了极为重要的位置，而无人驾驶显然未来的属性为消费类。

北斗将在自动驾驶领域大放异彩，北斗高精度芯片将作为新车的标配，为自动驾驶提供亚米级甚至厘米级定位服务，而相关的北斗高精度服务也将迎来最大的客户需求。


#### GPS

**GPS**（Global Positioning System）即全球定位系统，是由美国建立的一个卫星导航定位系统，利用该系统，用户可以在全球范围内实现全天候、连续、实时的三维导航定位和测速；另外，利用该系统，用户还能够进行高精度的时间传递和高精度的精密定位。

##### GPS系统构成

GPS系统包括三大部分: 
- 空间部分--GPS卫星星座；
- 地面控制部分--地面监控部分；
- 用户设备部分--GPS信号接收机。

GPS系统构成如图：
- ![](https://images2015.cnblogs.com/blog/716683/201512/716683-20151228213715495-546188642.png)


##### GPS工作卫星及其星座

21颗工作卫星和3颗在轨备用卫星组成GPS卫星星座。24颗卫星距地高度为20200km，运行周期为11小时58分(恒星时12小时)，均匀分布在6个轨道平面内,轨道倾角为55度,各个轨道平面之间相距60度，每个轨道平面内各颗卫星之间相差90度。卫星通过天顶时,卫星可见时间为5个小时，在地球表面上任何地点任何时刻，在高度角15度以上，平均可同时观测到6颗卫星，最多可达9颗卫星。示例如图2：
- ![GPS卫星网络](https://images2015.cnblogs.com/blog/716683/201512/716683-20151228213924260-1451331394.png)


为了解算测站的三维坐标，必须观测4颗GPS卫星，称为定位星座。

**地面监控系统**

对于导航定位来说，GPS卫星是一动态已知点。星的位置是依据卫星发射的星历--描述卫星运动及其轨道的参数算得的。每颗GPS卫星所播发的星历，是由地面监控系统提供的。卫星上的各种设备是否正常工作，以及卫星是否一直沿着预定轨道运行，都要由地面设备进行监测和控制。地面监控系统另一个重要作用是保持各颗卫星的时间，求出钟差，然后由地面注入站发给卫星，卫星再由导航电文发给用户设备。

GPS工作卫星的地面监控系统包括一个主控站、三个注入站和五个监测站。主控站的作用是根据各监控站对GPS的观测数据，计算出卫星的星历和卫星钟的改正参数等，并将这些数据通过注入站注入到卫星中去；同时，它还对卫星进行控制，向卫星发布指令，当工作卫星出现故障时，调度备用卫星，替代失效的工作卫星工作；另外，主控站也具有监控站的功能；监控站主要任务是为主控站提供卫星的观测数据；注入站任务是将主控站发来的导航电文注入到相应卫星的存储器。

**GPS信号接收机** 

能够捕获到按一定卫星高度截止角所选择的待测卫星的信号，并跟踪这些卫星的运行，对所接收到的GPS信号进行变换、放大和处理，以便测量出GPS信号从卫星到接收机天线的传播时间，解译出GPS卫星所发送的导航电文，实时地计算出测站的三维位置，甚至三维速度和时间。　　

##### GPS定位原理

GPS导航系统的基本原理是测量出已知位置的卫星到用户接收机之间的距离，然后综合多颗卫星的数据就可知道接收机的具体位置。要达到这一目的，卫星的位置可以根据星载时钟所记录的时间在卫星星历中查出。而用户到卫星的距离则通过纪录卫星信号传播到用户所经历的时间，再将其乘以光速得到(由于大气层电离层的干扰，这一距离并不是用户与卫星之间的真实距离，而是伪距）。

当GPS卫星正常工作时，会不断地用1和0二进制码元组成的伪随机码(简称伪码)发射导航电文。导航电文包括卫星星历、工作状况、时钟改正、电离层时延修正、大气折射修正等信息。GPS导航系统卫星部分的作用就是不断地发射导航电文。然而，由于用户接受机使用的时钟与卫星星载时钟不可能总是同步，所以除了用户的三维坐标x、y、z外,还要引进一个变量 t 即卫星与接收机之间的时间差作为未知数，然后用4个方程将这4个未知数解出来。所以如果想知道接收机所处的位置，至少要能接收到4个卫星的信号。如下图所示： 

![GPS位置计算方法](https://images2015.cnblogs.com/blog/716683/201512/716683-20151228214007214-442935877.png)

从以上四个方程中解出x，y，z和t就可以定时、定位。

GPS定位方式，不需要sim卡，不需要连接网络，只要在户外，基本上随时随地都可以准确定位。其他类型卫星定位方式与GPS差不多，不再讲述。

#### 北斗

##### 哪些手机支持北斗

中科院官方科普平台“科学大院”介绍，北斗信号的获取主要取决于**手机处理器**（SOC）中集成的**定位芯片**，目前大多SOC都能同时支持`GPS`、`北斗`和`GlONASS`：
- 高通骁龙800、600、400系列，其中目前常见的820、821、835高端型号是支持北斗的，中低端的652、650、625、436，甚至更老的一些型号也都是支持。
- 联发科类似，目前常见的P10、P15、P20、X20，之前的X10都支持接收北斗信号。
- 华为海思很早就支持了北斗。从麒麟930开始，集成的Hi1101四合一芯片可以同时接收GPS、北斗和GLonass三种信号。
- 也就是说，除了任性的苹果，采用这些SOC的华为、O&V、小米、一加、魅族、HTC、努比亚等品牌的大部分型号手机都支持北斗定位

##### 如何切换北斗

测试软件试试，比如“GPS状态”、“北斗伴”、“AndroiTS GPS Test Pro”等等，以AndroiTS GPS Test Pro为例：找个户外开阔的地方，打开手机的“位置服务”，然后运行[AndroiTS GPS Test Pro](http://www.danji100.com/app/139506.html)软件，效果如下：
- ![](https://pic3.zhimg.com/80/v2-d66172d2edc6a3d7a6cdd12a8463c682_720w.jpg)
- 1、在手机桌面点击打开“应用市场”。
- 2、点击搜索“AndroiTS GPS Test Pro”软件下载安装到手机。
- 3、点击“设置”。
- 4、点击列表中“定位服务”。
- 5、将右侧滑动按钮开启。
- 6、AndroiTS GPS Test Pro软件，点击最下方第三个图标，就是我国的北斗导航卫星系统。


手机导航，其实是北斗进入比较晚的行业了。现任中国卫星导航系统管理办公室主任、北斗系统新闻发言人冉承其曾给出一组数据：过去5年，我国480万辆营运车辆上线“北斗”，建成全球最大的北斗车联网平台，全国4万余艘渔船安装“北斗”。他以北京为例，已有33500辆出租车、21000辆公交车安装“北斗”，实现“北斗”定位全覆盖；1500辆物流货车及19000名配送员，使用“北斗”终端和手环接入物流云平台，实现实时调度。



## 定位技术应用


### 宠物跟踪器

【2023-11-15】Github上的嵌入式项目之——宠物跟踪器
- [findmycat 官网](https://www.findmycat.io/), [文档](https://www.findmycat.io/docs/iOSApplication)
- [github](https://github.com/FindMyCat/)

使用定位技术，在室内和室外工作，电池寿命长达数月，可以定位宠物的位置，误差只有10厘米。硬件部分包括一块4层PCB电路板，其中包括LTE和GPS线路、天线、电源管理和晶体等。该跟踪器需要打印三个部分，其中包括顶盖、底座和底盖。官方网站和文档说明可供参考。
- ![](https://www.findmycat.io/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhero_tracker_render.a3f7dc53.png&w=1200&q=75)

<iframe width="560" height="315" src="https://www.youtube.com/embed/MjsZzaDcbYY?si=duQW4KfvGg9v6gOj" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


# 结束
















