---
layout: post
title:  "Ŀ�����--Obeject Tracing"
date:   2020-04-01 18:30:00
categories: ������Ӿ�
tags: ������Ӿ�  yolo Ŀ�����
excerpt: ������Ӿ�֮Ŀ�����֪ʶ����
author: ��Х����
mathjax: true
permalink: /object_track
---

* content
{:toc}

# Ŀ�����

Ŀ������Ǽ�����Ӿ������һ����Ҫ���⣬Ŀǰ�㷺Ӧ������������ת����������غ����˻������˳��������˵�����
- ![img](https://pica.zhimg.com/v2-669bcf28d4d647b6d832984adf059ac0_1440w.jpg?source=172ae18b)
- [Ŀ���������](https://zhuanlan.zhihu.com/p/148516834)

## Ŀ�����Ӧ��

|Ӧ������|����|ʾ��|
|---|---|---|
|��������|����ת��|![](https://pic1.zhimg.com/80/v2-531de42fb6687921041aa8a8e6cd2ce8_1440w.webp)|
|���˳�|��������|![](https://pic1.zhimg.com/80/v2-deee3ca02a16a4ac0d098acb2390cfac_1440w.webp)|

## Ŀ����ٷ���

Ŀ������������

Ŀ����ٿ��Է�Ϊ���¼�������
- ��Ŀ����� - ����һ��Ŀ�꣬׷�����Ŀ���λ�á�
- ��Ŀ����� - ׷�ٶ��Ŀ���λ��
- Person Re-ID - ������ʶ�������ü�����Ӿ������ж�ͼ�������Ƶ�������Ƿ�����ض����˵ļ������㷺����Ϊ��һ��ͼ������������⡣����һ���������ͼ�񣬼������豸�µĸ�����ͼ��ּ���ֲ��̶�������ͷ���Ӿ����ޣ����������˼��/���˸��ټ������ϡ�
- MTMCT - ��Ŀ�������ͷ���٣�Multi-target Multi-camera Tracking�������ٶ������ͷ����Ķ����
- ��̬���� - ׷���˵���̬

����������������ֿ��Է�Ϊ����2�ࡣ
- ���߸��� - ���߸�����Ҫʵʱ��������ͨ����ȥ������֡������δ��֡�������λ�á�
- ���߸��� - ���߸��������ߴ������񣬿���ͨ����ȥ�����ں�δ����֡���ƶ������λ�ã����׼ȷ�ʻ����߸��ٸߡ�


### ��Ŀ�����(SOT)

��Ŀ�����������**����**�Ĵ���������ʱ��������ȷ������Ŀ���״̬��״̬������
- λ��Position
- ����Ŀ���˶���**״̬��**(eg��vel,heading)
- һЩ��������Ȥ��**����**(eg��shape,class)

#### Introduction of SOT

�����ϵ�Ŀ����پ���һ���˲����⡣[img](https://pic1.zhimg.com/80/v2-4ab11cc071f5f3c27df98746a7b4602c_1440w.webp)
- ![img](https://pic1.zhimg.com/80/v2-4ab11cc071f5f3c27df98746a7b4602c_1440w.webp)

[��Ŀ��׷�����ۣ�SOT��չ�Ƕȣ�](https://zhuanlan.zhihu.com/p/488468550)

��Ŀ��׷�ٵ�����׷�ٲ���������, ����[ͼ](https://pic4.zhimg.com/80/v2-289043efa97d0e9cfd6f85414e022b47_1440w.webp)��Ƶ��
- ��һ֡�п�׷��Ŀ�꣨�������������Ϊ��Ϊ������Ϣ���粩���أ�����ȷ��׷�ٵ�Ŀ��
- ��������Ƶ����������֡�ж��ܸ��ٳ��ڵ�һ֡�п򶨵�Ŀ�꣬�ﵽ��ʱ����ٵ�Ŀ�ģ������ڵ�һ֡�����仯С����������л�����Ƶ��һ��֡��������֡�������仯�󣬴�ʱ�ܹ������ڵ�һ֡����Ϊ������Ϣ����������֡�������ڲ�ͬ��Ƶ�е�Ŀ����һ���ǳ�������ս�Ե�����

#### How to realize SOT(��ô׷��)

��ͼ�������ҵ���ģ�������Ƶ�����
- ����׷��[ʾ��](https://pic3.zhimg.com/80/v2-73b81aea9fb573fded3d8e4a70c1b64e_1440w.webp)
- ![](https://pic3.zhimg.com/80/v2-73b81aea9fb573fded3d8e4a70c1b64e_1440w.webp)

�Ե�һ֡��������ϢΪ�����ں���֡��ֻ��Ҫ�ڻ������ҳ���Ϊ���ƵĲ��ּ��ɣ���ͼ1.2����׷�٣��ڵ�һ֡�򶨳��������ں���֡��ֻ��Ҫ����Χ��������������ҳ��������򼴿ɡ��ٻص����ǵ��˶�Ա������׷�������У�ͼ1.3�а�ɫ��������ǵĺ�ѡ����ͨ�������ѡ�����һ֡������Ϣ�������ԾͿ����жϳ��Ƿ���������Ҫ���ٵ�Ŀ�ꡣ
- [��ѡ��](https://pic3.zhimg.com/80/v2-b3df7797cd9a7c77a4bef288242b923a_1440w.webp)
- ![](https://pic3.zhimg.com/80/v2-b3df7797cd9a7c77a4bef288242b923a_1440w.webp)

���⣺
- ������ͼ��������ٷ�Χʱ�����ȣ��Ե�һ֡��������ϢΪ���������Ŀ����һ�Ա�ʱ������Ŀ���ѡȡ��ôȷ����������ѡ��������ͼƬ�����������������ôȷ�������⣬������Ŀ�����ѡ��һ��һ���Ƚϻ�����޴��������Դ���ģ�Ч�ʵ͡�

��ͼ����ģ�ͼ򵥽���
 
��16��֮����������ѧϰ�İ�ͼ����ģ����[ͼ](https://pic1.zhimg.com/80/v2-57426bfca371c0cd9f0fa55073afeb88_1440w.webp)�����Ƚ���һ֡�򶨵���Ϊ������Ϣ��Template��ͨ��ResNet��������ȡ���Ӿ�����z����Ϊ�Աȵ�ģ�壨����ˣ����ں���֡�У�������ȫͼ�Һ�ѡ�򣬶�������һ֡����Χ���и��٣��������������� ��ȡ��ͼ��x��������z����ȡ������ͼ��x���о�������õ�ChannelΪ1�ĵĶ�ά�ĵ÷�ͼ����Ϊ���ƶȶԱȵĽ������СΪ17x17x1�ĵ÷�ͼ�е�һ�����ص����ԭͼ��15x15�õ�����
- ![](https://pic1.zhimg.com/80/v2-57426bfca371c0cd9f0fa55073afeb88_1440w.webp)
- ��ͼ������·�ṹͼ
 
SOT���о�����
*   �������õ�������ȡ��������Ӿ���������
*   �������ƶ�ƥ���㷨
*   ����ȷ�ı߽���ע
*   ��ʱ���Ŀ��׷�٣���һ֡ģ���Ƿ������ں�������֡��

��Ŀ��׷��ģ�ͷ�չ
- 1. More Precise BBox Annotation
  - Anchor-based (Anchor Box)
    - ![](https://pic4.zhimg.com/80/v2-d073fdc150d5f442d7139306c85e3fa7_1440w.webp)
    - ����Anchor-based˼���SOTģ��: SiamRPN, SiamCAR
  - Anchor-free
    - ![](https://pic1.zhimg.com/80/v2-43af25514bd47c05959948a6360c6920_1440w.webp)
- 2. Stronger Feature Extractor�����õ����������������ڵ�Ŀ��׷����˵��ʹ�ø�����������ResNet�����ܲ���������
  - ���һ�����صĸ���Ұ̫�����ᵼ����λ������ͼ��Ŀ��λ�ò�ƥ�䣩
  - ��Σ�Padding���ܻ��ģ��ƥ�����һЩƫ��
  - ��ô����
    - �ü��������padding: �����ġ�Deeper and Wider Siamese Networks for Real-Time Visual Tracking���У���������ü�������padding��˼�롣
    - ��Ŀ��ı�ע����Χƫ��: ��û��paddingʱ���÷ּ���ʱ���������֮��õ�������ͼ�ǳ���������ͼ�������е�21��ӳ�䵽ԭͼ�о��Ǿ��������
- 3. More Fine-grained Matching����ϸ���ȵ�ģ��ƥ�䣩
  - ϸ����������ʽһ����������
  - ϸ����������ʽ������transformer
- 3. Traditional Methods����ͳ������
  - Old but Strong Correlation Filter��19��֮ǰ��
  - Older Motion Model�������ͣ�
    - LK Optical Flow��LP���ⷨ��

�����[��Ŀ��׷�����ۣ�SOT��չ�Ƕȣ�](https://zhuanlan.zhihu.com/p/488468550)

### ��Ŀ�����(MOT)

[��Ŀ�����(MOT)](https://zhuanlan.zhihu.com/p/387069216)

��ʵ�����У������ܽ�׷��һ��Ŀ�ꡣ
- ����[ͼ](https://pic3.zhimg.com/80/v2-6b9b0160b3b5d380f03a05814763c79e_1440w.webp), һ������**�Զ���ʻ**����ʾ����ͨ���������ɸ�֪�����ˡ��������г���Ŀ�꣬�˶�״̬���ܰ�����ֹ���ᴩ��ת�䡢������ʻ�ȡ������ѱ�ø��ӡ�
- ![img](https://pic3.zhimg.com/80/v2-6b9b0160b3b5d380f03a05814763c79e_1440w.webp)

��Ŀ����������������Ĵ���������ʱ��������ȷ��**���Ŀ��**���������ԣ�
- ��̬Ŀ��ĸ���
- ÿ����̬Ŀ���״̬(�͵�Ŀ�������ͬ)

�Ա�SOT��MOT���֣��䴦���������һ��**ȷ����̬Ŀ�����**��

��Ŀ����ٻ��ڴ������ļ�⡣
- һ���Զ���ʻ���ϻ��䱸һЩ**������**������`camera`��`radar`��`Lidar`��
- ��Щ�������ڳ�����ʻ�����У���ɼ�����ԭʼ��������`���`(detector)ģ��
  - `camera`����ͷ �ɻ��bounding box
  - `radar`�״� �ɻ�ü������µķ�λ�Լ������ղ���
  - `Lidar`���� �ɻ�õ��ƣ�������Щ�źŽ������Ŀ�����ģ�顣
- ��Ŀ�����ģ���������Щ�����ĵ�֡���ź��Ի��Ŀ��state�ĺ���ֲ�������[ͼ](https://pic2.zhimg.com/80/v2-ba14183a099a535084fe7c35939f6b21_1440w.webp)��ʾ��
- ![](https://pic2.zhimg.com/80/v2-ba14183a099a535084fe7c35939f6b21_1440w.webp)

һ������£�detector�������**��֡**���ݣ���MOT��Ҫ����**��֡**���ݣ���ʱ��ġ�

������ٸ�����
- sensorΪ`camera`��detector��������ѧϰ�㷨�������MOT�Ĳ�����bounding box�Լ��³�����ȹ��ơ�
- MOTģ����������Щ��֡�Ĳ�������Ŀ�����
- �����Ŀ����Գ�������ϵ�� position(x,y) �Լ� velocity(Vx,Vy)��

��[ͼ](https://pic1.zhimg.com/80/v2-5a31fc334955fb87dc66254619b9200c_1440w.webp)��Բ��ʾ��Ϊ��ȷ���ȡ�
- ![](https://pic1.zhimg.com/80/v2-5a31fc334955fb87dc66254619b9200c_1440w.webp)

#### ��Ŀ����ٵ�����
 
����ÿ��Ŀ����ܲ�����ͬ�����Ĳ����������Ӧ�Ĳ�����Ŀȡ���ڴ������ķֱ��ʣ�Ҳȡ����detector��ͬʱҲȡ���ڸ��ٶ�������͡�����ÿ��Ŀ���Ӧ�����Ķ��ٵȱ�׼��Ŀ����ٿɷ�Ϊ�������ͣ�
 
�� **��**Ŀ�����(point object tracking)

�����ͳ�Ķ�Ŀ��������ͣ����ڡ�small object���ļ��裬����
*   ÿ��Ŀ�궼�Ƕ����ġ�
*   ÿ��Ŀ�������ģΪ�㣬��û���κ���չ��
*   ��һ��ʱ�������ڣ�ÿ��Ŀ���������һ����Ӧ�Ĳ�����
 
��Ŀ����ٵ����ӣ�
*   camera�ļ��
*   �������ڼ��ӵ��״�

![](https://pic3.zhimg.com/80/v2-ac9bd337ecd16aac22209c2720c60d76_1440w.webp)
 
�� **��չ**Ŀ�����(extended object tracking)

�˸�������Ŀ��һ���в�ֹһ����������Ŀ���shapeһ����δ֪�ģ��ɶ�̬�����仯��ͨ���ݹ��˲����¿���ȷ��Ŀ���shape������Ŀ��ʹ�ø���ϵͳ��ø��ӣ������Գ̶�������ע������CV��������������ǲ�ͬ�ġ�

��չĿ����ٵ����ӣ�
*   Lidar
*   ����radar

![](https://pic3.zhimg.com/80/v2-97c629ff9de1c50083a6aaafe7aa2dc2_1440w.webp)
 
�� **Ŀ��Ⱥ**����(group object tracking)
 
����Ŀ�걻����һ��group����Ȼ��һĿ��Ҳ���Կ���һ��group��
- ![](https://pic3.zhimg.com/80/v2-e519435a9afe2e7f6af064f491d288d6_1440w.webp)
 
�� ����(�ྶ��merged measurement)
 
�ྶ����෢�����״���Զ���ʻ��������״ﱻ·�淴�䣬���˳����ĵ�����ɼ���Ŀ��㲻�ǳ���������㡣����ͼ��ʾ��
- ![](https://pic2.zhimg.com/80/v2-d5698ff5df6efc89e0dc97f3c68f5255_1440w.webp)

merged measurement���������������������Գ�ǰ�����У���������ͬ�ٶȵĻ���radar���ĵ㱻�ϲ���Ŀ������ڶ����м䣬����[ͼ](https://pic1.zhimg.com/80/v2-55bd78c944a0dba01217faef0d76a674_1440w.webp)��ʾ��
- ![](https://pic1.zhimg.com/80/v2-55bd78c944a0dba01217faef0d76a674_1440w.webp)

#### ��Ŀ����ٵ���ս

��һ���ֵ���ս���£�����ͼ������˵�����⣬ͼ�����β���Ϊ���ش������ɹ۲ⷶΧ��
*   FOV��Χ�ڶ��ٸ�Ŀ�겻֪����ÿ��Ŀ���state��֪����
*   Ŀ����FOV�ڵ����ƶ���
*   ���ھ�Ŀ���뿪FOV����Ŀ�����FOV���漰��Ŀ��ĳ�������ʧ�������track birth��track death����Ҫ���к�������
*   �ڵ����⣺ĳһ֡һ��Ŀ�������Ŀ���ڵ�����������ⲻ�� ��

![](https://pic3.zhimg.com/80/v2-51f2c9dae5b123b45ce7c158ca949286_1440w.webp)
 
��һ���ֵ���ս�������ڴ�������ȱ�ݵ��µģ�
*   (1) ��������©��
  *   �ڳ�����ʻ�����У���ǰ��ĳ���˹���·��������©������ܳ����Զ���ʻ�Ĺ�����fail����ʱ��Ҫ����ģ����ж��ף�Ҳ����MOT��
  *   ©���������ԭ�����£�
    *   �������⣺����poor light��
    *   Ŀ�걾�����ԡ��������˲��Ǻ����ױ�radar��⵽��
    *   �ڵ�ԭ��
*   (2) ���������龯��
  *   �ڳ�����ʻ�����У���ǰ���տ���Ҳ�����������ϱ�����Ŀ�꣬��Ϳ�����ɳ����Զ�����ɲ������ʱҲ��Ҫ����ģ����ж��ף�Ҳ����MOT��
  *   �龯��������ԭ��
    *   �����ط�������radar��
    *   ������ΪĿ�ꡣ
    *   �������⡣
 
���һ������ս�������ݹ�����
- ���ݹ����Ƕ�Ŀ�����������Ҫ������֮һ��˵��ͨ�׵���ǣ���k-1ʱ�̸�֪���ɸ�Ŀ�꣬��kʱ�̸�֪���ɸ�Ŀ�꣬MOTģ����Ҫ����ЩĿ���Ӧ������ȷ����Щ����ͬһ��Ŀ�꣬�����в��ܹ������󣬷�������������Ϣ������Ŀ�ꡣ
 
���ݹ�������ս��ԭ��
*   ���Ⱦ�����Ϊû��������Ϣ����֪����Щ�����֮ǰ�е�Ŀ�꣬��Щ�������ɵ�Ŀ��������龯��
*   ��ξ��Ǵ���������Ӱ�죬���ܵ���Ŀ��״̬���Ʋ�׼ȷ�������㷨���ƣ����¹����ϴ���Ŀ�ꡣ
*   ���о���Ŀ��˴�֮��ܽ���Ҳ���׹������������ڽ�ͨӵ�³��������복֮�����ܽ������������������ϴ󣬲�����׼���ͺ����׹�������
 
�ٸ����ӣ�����ͼ��ʾ������1,2,3�ֱ��Ӧ����ʱ�̣���ɫ����Ϊ�龯�������ɵ�track��ͬһĿ������ͬһ����ɫ�����ͨ��ͼʾ��������������ЩĿ��Ӧ�ù�����һ��
- ![](https://pic4.zhimg.com/80/v2-f7de71e8e7c9d36ddb4b9c1ce04d1563_1440w.webp)
 
Ȼ���������ɫȥ��������3��ʱ�̵Ĳ��������۾Ͳ��÷ֱ��ˡ�
- ![](https://pic1.zhimg.com/80/v2-7eb9c81778848a722a0ec27712ea3070_1440w.webp)
 
�����Ƕ���Lidar��radar������Ŀ��࣬�龯��Ĵ����������ݹ����㷨�ͱ�ø�����Ҫ�����ж���Ҫ�أ�����ͼΪ3��Ŀ����ò�ͬ�����ݹ����㷨���и��٣����Կ������Ƶ�λ����Ϣ(�켣)���ϴ�ͼһֱ��ʧ�ܣ�ͼ����û��ͼ��ƽ�����ɼ����ݹ�������Ҫ�ԡ�
- ![](https://pic1.zhimg.com/80/v2-00765560daff98ed71b4373e41d99c14_1440w.webp)

## ���ݼ�

- ![img](https://pic2.zhimg.com/80/v2-469a0d48774e9346242a5fa8e5bd1a39_1440w.webp)

## Ŀ����ٵ����ѵ�

��ȻĿ��׷�ٵ�Ӧ��ǰ���ǳ��㷺����������һЩ��������������Ӧ�ã����ǿ�������Щ�����أ�
- ��̬�仯 - ��̬�仯��Ŀ������г����ĸ������⡣�˶�Ŀ�귢����̬�仯ʱ, �ᵼ�����������Լ����ģ�ͷ����ı�, ���׵��¸���ʧ�ܡ�����:���������е��˶�Ա����·�ϵ����ˡ�
- �߶ȱ仯 - �߶ȵ�����ӦҲ��Ŀ������еĹؼ����⡣��Ŀ��߶���Сʱ, ���ڸ��ٿ�������Ӧ����, �Ὣ�ܶ౳����Ϣ��������, ����Ŀ��ģ�͵ĸ��´���:��Ŀ��߶�����ʱ, ���ڸ��ٿ��ܽ�Ŀ����ȫ��������, ���ٿ���Ŀ����Ϣ��ȫ, Ҳ�ᵼ��Ŀ��ģ�͵ĸ��´������, ʵ�ֳ߶�����Ӧ������ʮ�ֱ�Ҫ�ġ�
- �ڵ�����ʧ - Ŀ�����˶������п��ܳ��ֱ��ڵ����߶��ݵ���ʧ������������������ʱ, ���ٿ����׽��ڵ����Լ�������Ϣ�����ڸ��ٿ���, �ᵼ�º���֡�еĸ���Ŀ��Ư�Ƶ��ڵ������档��Ŀ�걻��ȫ�ڵ�ʱ, �����Ҳ���Ŀ��Ķ�Ӧģ��, �ᵼ�¸���ʧ�ܡ�
- ͼ��ģ�� - ����ǿ�ȱ仯, Ŀ������˶�, �ͷֱ��ʵ�����ᵼ��ͼ��ģ��, ���������˶�Ŀ���뱳�����Ƶ�����¸�Ϊ���ԡ����, ѡ����Ч��������Ŀ��ͱ����������ַǳ���Ҫ��

ʾ��
- ���ռ�ģ�� [img](https://pic1.zhimg.com/80/v2-522e7bad45da314edb03ea3c7b26f260_1440w.webp)
  - ![](https://pic1.zhimg.com/80/v2-522e7bad45da314edb03ea3c7b26f260_1440w.webp)
- �α估�ڵ� [img](https://pic3.zhimg.com/80/v2-46f38d9ee2dd149639774ee598e4456a_1440w.webp)
  - ![](https://pic3.zhimg.com/80/v2-46f38d9ee2dd149639774ee598e4456a_1440w.webp)


## Ŀ������㷨


### Ŀ������㷨�ܽ�

Ŀ����ٵķ�����Ҫ��Ϊ2���࣬һ����**����˲�**��һ����**���ѧϰ**��[img](https://pic2.zhimg.com/80/v2-632a3a08c0f30f0abcdb8b06afbe346d_1440w.webp)
- ![img](https://pic2.zhimg.com/80/v2-632a3a08c0f30f0abcdb8b06afbe346d_1440w.webp)
- ����ڹ�������Kalman��Meanshift�ȴ�ͳ�㷨������˲����㷨�����ٶȸ��죬���ѧϰ�෽�����ȸ�.
- ���ж������ں��Լ����������׷�����ڸ��پ��ȷ����Ч������.
- ʹ��ǿ��ķ�������ʵ�����ø��ٵĻ���.
- �߶ȵ�����Ӧ�Լ�ģ�͵ĸ��»���ҲӰ���Ÿ��ٵľ���.


### Ŀ������㷨����

Ŀ����ٵķ�������**ģʽ**����Ϊ2�ࡣ
- `����ʽ`ģ�� - ������Ҫ������**����ʽ**ģ�͸����㷨���о�, ��`������`��`�����˲�`��`Meanshift`�㷨��`Camshift`�㷨��.
  - ���෽�����Ƚ���**Ŀ��ģ��**����**��ȡĿ������**, �ں���֡�н���**������������**. �𲽵���ʵ��Ŀ�궨λ.
  - ����ȱ��: 
    - ͼ��ı�����Ϣû�еõ�ȫ�������.
    - Ŀ�걾�����۱仯������ԺͶ������ص�
  - ���, ͨ��**��һ��ѧģ��**����������Ŀ����кܴ�ľ�����. �������Ϊ**���ձ仯**, **�˶�ģ��**, **�ֱ��ʵ�**, **Ŀ����ת�α�**�����, ģ�͵Ľ������ܵ��޴��Ӱ��, �Ӷ�Ӱ����ٵ�׼ȷ��; ģ�͵Ľ���û����Ч��Ԥ�����, ������Ŀ���ڵ����ʱ, ���ܹ��ܺõؽ����
- `����ʽ`ģ�� - ����ʽģ�ͽ�**Ŀ��ģ��**��**������Ϣ**ͬʱ��������, ͨ���Ա�Ŀ��ģ�ͺͱ�����Ϣ�Ĳ���, ��Ŀ��ģ����ȡ����, �Ӷ��õ���ǰ֡�е�Ŀ��λ��.�����ڶԸ����㷨�������з���, ͨ����������Ϣ�������ģ��, ���Ժܺõ�ʵ��Ŀ�����.��˼���ʽģ�;��кܴ������.
  - 2000������, �����𽥳���ʹ�þ���Ļ���ѧϰ����ѵ��������, ����MIL��TLD��֧�����������ṹ��ѧϰ�����ɭ�֡���ʵ��ѧϰ������ѧϰ. 
  - 2010��, �����״ν�ͨ�������**����˲�**�������뵽Ŀ�������.��Ϊ����ʽ������һ��, ����˲��������ٶ��ϻ���׼ȷ����, ����ʾ������Խ������. Ȼ��, ����˲�������Ŀ���������2014��֮��.
  - ��2015���Ժ�, �������ѧϰ�����Ĺ㷺Ӧ��, ���ǿ�ʼ�����ѧϰ��������Ŀ����١�

����ʱ��˳��Ŀ����ٵķ��������˴Ӿ����㷨�����ں�����˲��㷨���ٵ��������ѧϰ�ĸ����㷨�Ĺ��̡�
- ��������㷨
- ���ں�����˲��ĸ����㷨
- �������ѧϰ�ĸ����㷨


### ��������㷨

���ڵ�Ŀ������㷨��Ҫ�Ǹ���Ŀ�꽨ģ���߶�Ŀ���������и���
- ����**Ŀ��ģ�ͽ�ģ**�ķ���: ͨ����Ŀ�����ģ�ͽ��н�ģ, Ȼ����֮���֡���ҵ�Ŀ��.����, ����ƥ�䡢��������١��������������ĸ����㷨����������.��õ�������ƥ�䷨, ������ȡĿ������, Ȼ���ں�����֡���ҵ������Ƶ���������Ŀ�궨λ, ���õ�������: SIFT������SURF������Harris�ǵ�ȡ�
- ����**����**�ķ���: �����о�������, ���Ƿ��ֻ���Ŀ��ģ�ͽ�ģ�ķ���������ͼƬ���д���, ʵʱ�Բ�.���ǽ�Ԥ���㷨���������, ��Ԥ��ֵ��������Ŀ������, �����������ķ�Χ.����һ���Ԥ���㷨��Kalman�˲��������˲�����.��һ�ּ�С������Χ�ķ������ں˷���:���������½�����ԭ��, ���ݶ��½������Ŀ��ģ���𲽵���, ֱ������������λ��.����, Meanshift��Camshift�㷨


#### ������

`������`(Lucas-Kanade)�ĸ���������1950�����, ����������ģ�Ͷ���Ƶ�����е����ؽ��в���.ͨ��������Ƶ����������֮֡������ع�ϵ, Ѱ�����ص�λ�Ʊ仯���ж�Ŀ����˶�״̬, ʵ�ֶ��˶�Ŀ��ĸ���.����, ���������õķ�Χ��С, ��Ҫ�������ּ���:ͼ��Ĺ���ǿ�ȱ��ֲ���; �ռ�һ����, ��ÿ�������ڲ�ͬ֡�����ڵ��λ�ò���, ��������������յ��˶�ʸ��; ʱ������.������������Ŀ���˶������֡���ǻ�����, Ҳ������֮֡���Ŀ��λ�Ʋ���̫��.

����������
- **���Ⱥ㶨**: ���ص������ֵ�ڲ�ͬ֡�к㶨����
- **С�˶�**: ���ص�λ��������֡�䲻����ұ仯
- **�ռ�һ��**: ǰһ֡���������ص��ں�һ֡��Ҳ����

��Ҫ˼�룺
- ����׷��Ŀ��������(�������ص�)��ʱ����ı仯������֡�Ĺ�������ÿ���������˲ʱ�ٶȺͷ��򣬽���Ԥ�����֡������λ�ã�������[ͼ](https://pic2.zhimg.com/80/v2-278b11128d0c6df577e158a236981789_1440w.webp)��
- ![](https://pic2.zhimg.com/80/v2-278b11128d0c6df577e158a236981789_1440w.webp)

#### Meanshift

`Meanshift`������һ�ֻ��ڸ����ܶȷֲ��ĸ��ٷ�����ʹĿ�������һֱ���Ÿ����ݶ������ķ��򣬵��������������ܶȷֲ��ľֲ���ֵ�ϡ����� Meanshift ���Ŀ����н�ģ����������Ŀ�����ɫ�ֲ�������Ŀ�꣬Ȼ�����Ŀ������һ֡ͼ���ϵĸ��ʷֲ����Ӷ������õ��ֲ����ܼ�������Meanshift ������Ŀ���ɫ��ģ�ͺͱ�������Ƚϴ�����Σ�����Ҳ�����������١����� Meanshift �����Ŀ��ټ��㣬���ĺܶ�Ľ�����Ҳһֱ��������

#### �����˲�

`�����˲�`��Particle Filter��������һ�ֻ������ӷֲ�ͳ�Ƶķ������Ը���Ϊ�������ȶԸ���Ŀ����н�ģ��������һ�����ƶȶ���ȷ��������Ŀ���ƥ��̶ȡ���Ŀ�������Ĺ����У����ᰴ��һ���ķֲ���������ȷֲ����˹�ֲ�����һЩ���ӣ�ͳ����Щ���ӵ����ƶȣ�ȷ��Ŀ����ܵ�λ�á�����Щλ���ϣ���һ֡��������µ����ӣ�ȷ���ڸ�������ϸ�����Ŀ�ꡣKalman Filter ������������Ŀ����˶�ģ�ͣ�������Ŀ���������ģ�����Ƕ�Ŀ����˶�ģ�ͽ����˽�ģ�������ڹ���Ŀ������һ֡��λ�á�

#### ��ȱ��

���Կ�������ͳ��Ŀ������㷨������������**ȱ��**:
- û�н�**������Ϣ**��������, ������Ŀ���ڵ�, ���ձ仯�Լ��˶�ģ���ȸ��������׳��ָ���ʧ��.
- �����㷨ִ��**�ٶ���**(ÿ��10֡����), �޷�����ʵʱ�Ե�Ҫ��.

### ���ں�����˲��ĸ����㷨

���ţ����ǽ�ͨ�������**����˲�**(���������źŵ����Ƴ̶�)���뵽��Ŀ�������.
- һЩ��������˲��ĸ����㷨(MOSSE��CSK��KCF��BACF��SAMF)��, Ҳ��֮����, �ٶȿ��Դﵽ����֡ÿ��, ���Թ㷺��Ӧ����**ʵʱ����ϵͳ**��. 
- ���в���һЩ�������������ĸ�����, ����SAMF��BACF��OTB���ݼ���VOT2015������ȡ������ɼ���

#### MOSSE

�������������˲�����Correlation Filter��ͨ��MOSSE��Minimum Output Sum of Squared Error (MOSSE) filter���㷨ʵ�֣�����˼�룺Խ�����Ƶ�����Ŀ�����ֵԽ��Ҳ������Ƶ֡�����ʼ��Ŀ��Խ���ƣ��õ�����ӦҲ��Խ����ͼ��ʾͨ���Ա�UMACE,ASEF��MOSSE������˲��㷨��ʹ���Ŀ��������󻯡�


### �������ѧϰ�ĸ����㷨

�������ѧϰ�����Ĺ㷺Ӧ��, ���ǿ�ʼ���ǽ���Ӧ�õ�Ŀ�������.���ǿ�ʼʹ��**�������**��ȡ���˺ܺõ�Ч��.֮��, ���ǿ�ʼ���������ѧϰ����ȫ�µĸ��ٿ��, ����Ŀ�����.

�ڴ����ݱ����£��������ѧϰѵ������ģ�ͣ��õ��ľ������������������ǿ��
- ��Ŀ������ϣ����ڵ�Ӧ�÷�ʽ�ǰ�����ѧϰ����**����**��ֱ��Ӧ�õ�**����˲�**�� Struck�ĸ��ٿ�����棬�Ӷ��õ����õĸ��ٽ��������ǰ���ᵽ�� DeepSRDCF �����������Ͼ������õ��������������� HOG �� CN ��������Ҳ�����ѧϰ������֮һ����ͬʱҲ�����˼����������ӡ�

## Ŀ�����ǰ��

���·���
- ��ϸ���ݼ���[Visual Tracking Paper List](https://github.com/foolwood/benchmark_results)


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

* **D3S:** Alan Luke?i?,?Ji?�� Matas,?Matej Kristan.<br />
  "D3S �C A Discriminative Single Shot Segmentation Tracker." CVPR (2020).
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

* **CDTB:** Alan Luke?i?, Ugur Kart, Jani K?pyl?, Ahmed Durmush, Joni-Kristian K?m?r?inen, Ji?�� Matas, Matej Kristan. <br />

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


## Ŀ�����ʵ��



### ��Ŀ�����

[opencvʵ�ֵ�Ŀ�����](https://blog.csdn.net/LuohenYJ/article/details/89029816)

ͨ����Ŀ����������·�����
- 1���ܼ���������Щ�㷨�����ڹ�����Ƶ֡��ÿ�����ص��˶������
- 2��ϡ���������Щ�㷨����Kanade-Lucas-Tomashi��KLT������������������ͼ���м����������λ�á�
- 3���������˲���һ�ַǳ����е��źŴ����㷨�����ڸ�����ǰ���˶���ϢԤ���˶������λ�á����㷨������Ӧ��֮һ�ǵ����Ƶ������ᵽ���������11�ŵ��²յĽ��䵽�����ؼ������һ���������˲�����Engineers Look to Kalman Filtering for Guidance��
- 4����ֵƫ��(Meanshift)��Camshift(Meanshift�ĸĽ�����������Ӧ��MeanShift�㷨)����Щ�����ڶ�λ�ܶȺ��������ֵ���㷨������Ҳ���ڸ��١�
- 5����Ŀ������㷨���ڴ���������У���һ֡ʹ�þ��α�ʾ����Ҫ���ٵĶ����λ�á�Ȼ��ʹ�ø����㷨�ں���֡�и��ٶ����ڴ����ʵ��Ӧ���У���Щ��������Ŀ�����㷨���ʹ�á�
- 6����Ŀ������㷨���������п��ٶ�������������£����ÿ��֡�еĶ������Ȼ�����и��ٲ����㷨��ʶ��һ��֡�е��ĸ����ζ�Ӧ����һ֡�еľ����Ǻ���Ч�ġ�

OpenCV 3���ṩ��8�ֲ�ͬ�ĸ�����BOOSTING��MIL��KCF��TLD��MEDIANFLOW��GOTURN��MOSSE��CSRT��


Python��

Python��΢�ܼ򵥣���ж�ذ�װ��Opencv��Ȼ��ֱ��pip/pip3��װcontrib�⣺

```py
pip uninstall opencv-python
pip install opencv-contrib-python
```

Ŀ����ٴ���

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

C++��

```c++
// Opencv_Tracker.cpp : ���ļ����� "main" ����������ִ�н��ڴ˴���ʼ��������
//
 
#include "pch.h"
#include <opencv2/opencv.hpp>
#include <opencv2/tracking.hpp>
#include <opencv2/core/ocl.hpp>
 
using namespace cv;
using namespace std;
 
int main()
{
	//�����㷨����
	string trackerTypes[7] = { "BOOSTING", "MIL", "KCF", "TLD","MEDIANFLOW", "MOSSE", "CSRT" };
 
	// Create a tracker ����������
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
 
	// Read video ����Ƶ
	VideoCapture video("video/chaplin.mp4");
 
	// Exit if video is not opened ���û����Ƶ�ļ�
	if (!video.isOpened())
	{
		cout << "Could not read video file" << endl;
		return 1;
	}
 
	// Read first frame ��ͼ
	Mat frame;
	bool ok = video.read(frame);
 
	// Define initial boundibg box ��ʼ����
	Rect2d bbox(287, 23, 86, 320);
 
	// Uncomment the line below to select a different bounding box �ֶ���ͼ���ϻ����ο�
	//bbox = selectROI(frame, false);
 
	// Display bounding box չʾ����2��Ե��
	rectangle(frame, bbox, Scalar(255, 0, 0), 2, 1);
	imshow("Tracking", frame);
 
	//��������ʼ��
	tracker->init(frame, bbox);
 
	while (video.read(frame))
	{
		// Start timer ��ʼ��ʱ
		double timer = (double)getTickCount();
 
		// Update the tracking result ���¸������㷨
		bool ok = tracker->update(frame, bbox);
 
		// Calculate Frames per second (FPS) ����FPS
		float fps = getTickFrequency() / ((double)getTickCount() - timer);
 
		if (ok)
		{
			// Tracking success : Draw the tracked object ������ٵ�Ŀ�껭��
			rectangle(frame, bbox, Scalar(255, 0, 0), 2, 1);
		}
		else
		{
			// Tracking failure detected. û�о��������ʧ��
			putText(frame, "Tracking failure detected", Point(100, 80), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(0, 0, 255), 2);
		}
 
		// Display tracker type on frame չʾ����㷨����
		putText(frame, trackerType + " Tracker", Point(100, 20), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(50, 170, 50), 2);
 
		// Display FPS on frame ��ʾFPS
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

### ���°���


#### CoTracker

��2024-10-4��CoTracker��ͬʱ׼ȷ������Ƶ�еĶ����  
- ���룺CoTracker ͬʱ׼ȷ������Ƶ�е�**�����**  
- ��ҳ��[CoTracker](https://co-tracker.github.io/)


# ����