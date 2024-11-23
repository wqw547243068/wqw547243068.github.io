---
layout: post
title:  "����ͼ����-Image Processing"
date:   2019-11-01 16:52:00
categories: ������Ӿ�
tags: ������Ӿ�  opencv ����ͼ�� �˲� ��ά ˮӡ sam ������
excerpt: ͼ�������ܽ�
mathjax: true
permalink: /image
---

* content
{:toc}


# ����ͼ����


## ����֪ʶ

������ͼ������������˹�����棬MATLABʵ��
- ������ͼ����������˹�����İ棩[����ʼ�Ŀ¼](https://zhuanlan.zhihu.com/p/569167720)
- [����ppt�μ�](https://wenku.baidu.com/view/055297b327fff705cc1755270722192e45365883.html?_wkts_=1672129716473), �ٶ��Ŀ��
- github�ϵ�[�μ�����:����ͼ����](https://github.com/fei-hdu/courses/tree/main/%E6%95%B0%E5%AD%97%E5%9B%BE%E5%83%8F%E5%A4%84%E7%90%86/2022), ���ݵ��ӿƼ���ѧ��[�߷�](https://aiart.live/)
- ������Ӿ�[ppt����](https://github.com/fei-hdu/courses/tree/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89)


Ŀ¼
- ��һ�� ����
- �ڶ��� ͼ����֪ʶ��ȫ������
- ������ �Ҷȱ任��ռ��˲�֪ʶ������
- ������ Ƶ����ͼ����֪ʶ������
- ������ ͼ��ԭ���ؽ�֪ʶ������
- ������ ��ɫͼ�������

### �Ҷ�ͼ

ͼ��ͨ����Ϊ��ɫͼ��ͻҶ�ͼ�����֡�
- �ڻҶ�ͼ���У�ÿ�����ض�ֻ��**һ��**����������ʾ�����صĻҶ�ֵ������������Ǹõ������ֵ��
  - ���õı�ʾ����ֵ��������ݳ�����8 bit��10 bit���֣���ͼ���λ��Ϊ8 bit��256����10 bit��1024����
- ��ֵͼ
  - �Ҷ�ͼ�й��ȣ���ֵͼû�й��ɣ�ֻ������0(��)��1(��)
- �ڲ�ɫͼ���У�ÿ�����ض���**���**��ɫ������ɣ�ÿ����ɫ��������Ϊһ��ͨ����Channel����
  - ͼ�����������ص�ͨ������һ�µģ���ÿ��ͨ�������Ա�ʾΪһ����ԭͼ��������ͬ����ɫ��ͬ�ķ���ͼ��
  - ��RGB��ʽ�Ĳ�ɫͼ��Ϊ����һ��������ͼ����Ա��ָ�Ϊ����B���������̣�G���������죨R����������ɫ�ĵ�ɫͼ
  - ![](https://pic2.zhimg.com/80/v2-55fa93deb68f2b99370953a3ea7b8ea1_720w.webp)

RGBͼ��Ŀ���Ϊ1920 ���ء�1080 ���أ�ÿ����ɫͨ����ͼ��λ��Ϊ 8 bit����ͼ����������Ϊ1920��1080��3��8bit����49,766,400bit��ԼΪ5.93MB���ҡ�

ע�� 
- �� 1 Byte��8bit��λ����
- �� 1KB��1024Byte���ֽڣ�
- �� 1 MB��1024KB

![](https://pic4.zhimg.com/80/v2-627bf6d9d2f637442d2346958e67420b_720w.webp)

### ��ɫ�ռ�

![](https://pic2.zhimg.com/80/v2-12c573c72e81a5be358de22a5d683675_720w.webp)

`��ɫ�ռ�`����ɫģ�͡�ɫ�ʿռ䡢 ��ɫϵͳetc���Ƕ�ɫ�ʵ�һ��������ʽ�������кܶ��֣�������������ͬ��Ӧ�ñ�����
- ��ʾ���в��õ�`RGB`��ɫ�ռ��ǻ���**���巢��**����ģ�RGB���ö�Ӧ�����ԭɫ��Red��Green��Blue����
- ��ҵӡˢ�г��õ�`CMY`��ɫ�ռ��ǻ���**�ⷴ��**����ģ�CMY��Ӧ�˻滭�е���ԭɫ��Cyan��Magenta��Yellow����
- `HSV`��`HSL`������ɫ�ռ䶼�Ǵ�**���Ӿ�**��ֱ�۷�ӳ��������ģ�H��ɫ����S�Ǳ��Ͷȣ�I��ǿ�ȣ���

#### RGB���ӷ���ɫ��

RGB��ɫ�ռ� ������ɫ��**�ӷ���ɫ**ԭ���Ӻ�ɫ���ϵ���Red��Green��Blue����ɫ�����տ��Եõ���ɫ�⡣ 
- ��R��G��B����ͨ����Ϊ�ѿ�������ϵ�е�X��Y��Z�ᣬ�͵õ���һ�ֶ�����ɫ�Ŀռ�����
- ![](https://i0.hdslb.com/bfs/article/347f4ac7d52d301eb2560fc24c2394d99abad0e5.png@675w_635h_progressive.webp)

������б��RGBÿһ������ֵ����8λ��bit����ʾ�����Բ���256*256*256=16777216����ɫ������Ǿ�����˵�ġ�24λ���ɫ���� 

���ߣ�[unity_ĳĳʦ_�߽���](https://www.bilibili.com/read/cv5841645/)

#### CMY��������ɫ��

�����`RGB`��`CMY`��CMYK����ɫ�ռ�����һ�ֻ�����ɫ**������ɫ**ԭ�����ɫģ�͡�
- �ڹ�ҵӡˢ��������������Ҫ�ڰ�ɫ������ʹ�ú�����ī��ͨ�����**����**��ʾ����ɫ��ģ�͡�
- CMYK��������`��`��`Ʒ��`��`��`��`��`������ī����ֵ��
- ![](https://i0.hdslb.com/bfs/article/20eefed4bae71f1f107b4519b029395d9dca9d93.png@300w_285h_progressive.webp)

��ӡ���ʴ�ʱ���ᷢ����Ļ�Ͽ�����ͼ���ʵ�ʴ�ӡ������ͼ����ɫ��һ����
- ���������۵����������ܺ�
- ��ӡ�������˲�ͬ��CMY��ɫ�ռ䣨ӳ���ϵ��

CMYK��ɫ�ռ����ɫֵ��RGB��ɫ�ռ��е�ȡֵ����ͨ�����Ա任�໥ת����

#### HSV�����Ӿ���

`HSV`��ɫ�ռ��Ǹ�����ɫ��ֱ������, ��A. R. Smith��1978�괴����һ����ɫ�ռ�, Ҳ��`����׶��ģ��`(Hexcone Model)��
- `RGB`��`CMY`��ɫģ�Ͷ�������**Ӳ��**��
- ��`HSV`��Hue Saturation Value����ɫģ��������**�û�**�ġ�

���ģ������ɫ�Ĳ����ֱ��ǣ�`ɫ��`��H��hue����`���Ͷ�`��S��saturation����`����`��V��value����
- ���Ǹ����˹۲�ɫ�ʵ������������������ɫģ��
- �˵��Ӿ�ϵͳ�����ȵ����ж�Ҫǿ��ɫ��ֵ����Ҳ��Ϊʲô������Ӿ���ͨ��ʹ�ûҶȼ�����ͼ���������ԭ��֮һ��

- ɫ��H���ýǶȶ�����ȡֵ��ΧΪ0�㡫360�㣬�Ӻ�ɫ��ʼ����ʱ�뷽����㣬��ɫΪ0�㣬��ɫΪ120��,��ɫΪ240�㡣���ǵĲ�ɫ�ǣ���ɫΪ60�㣬��ɫΪ180��,Ʒ��Ϊ300�㣻
- ���Ͷ�S��ȡֵ��ΧΪ0.0��1.0��
- ����V��ȡֵ��ΧΪ0.0(��ɫ)��1.0(��ɫ)��

HSVģ�͵���ά��ʾ��RGB�������ݻ������������RGB��������Խ��ߵİ�ɫ�������ɫ����۲죬�Ϳ��Կ�������������������Ρ������α߽��ʾɫ�ʣ�ˮƽ���ʾ���ȣ������ش�ֱ���������ӷ�������ɫ��������ȣ�ʹ��ɫ�࣬���Ͷȵȸ�������ɫ�ʸ���Ȼֱ�ۡ�
- ![](https://i0.hdslb.com/bfs/article/e9e72c7ba0963c50c0d6b5cbe9b4bdf0a2681d72.png@942w_942h_progressive.webp)

HSL��ɫ�ռ���HSV���ƣ�ֻ������V��Value�滻Ϊ��L��Lightness�������ֱ�ʾ����Ŀ�������ƣ����ڷ����������𡣶�������ѧ�϶���Բ������HSV��ɫ�࣬���Ͷȣ�ɫ�����ڸ����Ͽ��Ա���Ϊ����ɫ�ĵ�Բ׶�壨�ڵ����¶��㣬��ɫ���ϵ���Բ�ģ���HSL�ڸ����ϱ�ʾ��һ��˫Բ׶���Բ���壨��ɫ���϶��㣬��ɫ���¶��㣬���������Բ���ǰ�̻�ɫ����ע�⾡����HSL��HSV�С�ɫ�ࡱָ����ͬ�����ʣ����ǵġ����Ͷȡ��Ķ��������Բ�ͬ�ġ�����һЩ�ˣ�HSL���õķ�ӳ�ˡ����Ͷȡ��͡����ȡ���Ϊ��������������ֱ��������Ƕ�����һЩ�ˣ����ı��Ͷȶ����Ǵ���ģ���Ϊ�ǳ���͵ļ�����ɫ����ɫ��HSL���Ա�����Ϊ����ȫ���͵ġ�����HSV����HSL���ʺ��������û�������������ġ� ���ߣ�unity_ĳĳʦ_�߽��� https://www.bilibili.com/read/cv5841645/ ������bilibili

#### ��ɫ�ռ�ת��

��ɫ�ռ�֮���ת����ϵ���Է������ࣺ
- һ������ɫ�ռ�֮�����ֱ�ӱ任��
- ��һ������ɫ�ռ�֮�䲻��ֱ��ת��������֮��ı任��Ҫͨ������������ɫ�ռ�Ĺ�����ʵ�֣��磬RGB��CIE L*a*b*��
- ![](https://pic2.zhimg.com/80/v2-80732f19238cdd34cbd04ac0f63e0cb9_720w.webp)

### ͼ���ʾ

[����ͼ����ģ��ͼ��](https://zhuanlan.zhihu.com/p/252635549)

#### ģ��ͼ��

��1��ģ��ͼ��
- `ģ��ͼ��`����ͼ�����У���ֽ����Ƭ������ģ��ͼ��ȣ�����ͨ��ĳ������������⡢��ȣ���ǿ���仯����¼ͼ��������Ϣ��ͼ��
- �ص㣺�������ı仯��**����**�ġ�

#### ����ͼ��

��2������ͼ��
- `����ͼ��`����һ���������������͹������ͼ����ɢ������ļ��ϣ�ÿ�����������Ե����ԡ�
- �ص㣺��**����**ģ��ͼ����ɢ���ɹ������񣬲��ü���������ֵķ�ʽ����¼ͼ���ϸ�������������Ϣ��ͼ��

С�᣺
- һ�������ܿ����ģ�����ģ��ͼ��ͶӰ��͸����Ļ���ϵ�PPTҲ��ģ��ͼ�񣩡�
- ������ͼ�����ۿ����������ʾ���һ���洢���ֵľ���һ�����ݡ�

���������Ļ�ϳ��ֵ�ͼ����ģ��ͼ�񡣵����㿴����ͼ�����������Ѿ����˹�ѧ͸����ģ��ͼ�񣨹��źţ�����ת��Ϊ���źŴ洢Ϊ���ڴ濨�ϵ�һ��ͼƬ�ļ���ģ��ת����������һ������ͼ�����ڴ�����ţ��㿴��������Ȼ�󾭹�����ͼ���ϼ�¼����Ϣ������Ӧ��ɫ�ռ��ӳ�䣨��ģת������������Թ��źŵķ�ʽ����������ļ�����Ļ�ϣ��ֱ��ģ��ͼ���ˣ���

����ͼ���������ʵ�����У����ۺڰ�/��ɫ��ʱ�����ͼ�񾿾�������ͼ����ģ��ͼ�񣿴𰸵�Ȼ��ģ��ͼ��

#### ģ��ת�� or ��ģת��

����ͼ����ģ��ͼ��ת��
- ![img](https://pic1.zhimg.com/80/v2-35da1f8acba8c338f5ff7afba5acebe8_720w.webp)
- �������������ģ��ת���Ĺ���֮��ʵ���ǽ���ʵ�������������������������⣩���ֵ�ͼ����һ���ķֱ��ʣ����أ���ɢ����

#### ң��ͼ��

ң��ͼ��������һ���Ĵ�С�ģ�����3000���ء�5000���ء����ռ�ֱ��ʼ���ָͼƬ�е�ÿһ�����ش����ʵ�ʿռ��С������250m��250m��


### ͼ����-��������

ͼ����[��������](https://zhuanlan.zhihu.com/p/558711657)
- ��1��ͼ���ȡ
- ��2��ͼ��**��ǿ**����ͼ�����ĳ�ֲ�����ʹ����ĳ��Ӧ���б�ԭͼ����ܵõ����ʵĽ����
- ��3��ͼ��**��ԭ**���Ľ�ͼ����ۣ�ͼ����ǿ���������۵ģ�ͼ��ԭ�ǿ͹۵ġ���ԭ������������ͼ���˻�����ѧ�����ģ��Ϊ����������ǿ�����Ժõ���ǿЧ����������ƫ��Ϊ����
- ��4��**��ɫͼ��**����
- ��5��**С���任**������**ͼ��任**��С�����Բ�ͬ�ֱ�������ʾͼ��Ļ�����С���任��Ӧ����ͼ��ѹ���ͽ�����������ʾ��
- ��6��**ѹ��**��ָ����ͼ��洢���򽵵ʹ���ͼ��Ĵ���Ĵ���
- ��7��**��̬ѧ**��������ȡͼ�������ڱ�ʾ��������״�ĳɷִ����ߡ�
- ��8��**�ָ�**���Խ�һ��ͼ����Ϊ������ɲ��ֻ�Ŀ�ꡣ
- ��9��**������ȡ**���ڷָ��һ�����У��ӷָ��л�ȡ���ͼ����������صļ��ϡ�������ȡ�������������������������������ָѰ��һ��ͼ���е������������߽硣����������ָ�Լ�⵽�������涨�������ԡ�
- (10) ͼ��**ģʽ����**��ָ����Ŀ��������������Ŀ�����ڱ�ǵĹ��̡�

�ܽ᣺[img](https://pic4.zhimg.com/80/v2-2c50e078dc083216a5ea78338cb2a073_1440w.webp), [����](https://pic1.zhimg.com/80/v2-17417fabe9df8bf82f62e1bd26921780_1440w.webp)
- ![](https://pic4.zhimg.com/80/v2-2c50e078dc083216a5ea78338cb2a073_1440w.webp)
- ![](https://pic1.zhimg.com/80/v2-17417fabe9df8bf82f62e1bd26921780_1440w.webp)


### ͼ����-֪ʶ��

����ͼ����
1. ģ��ͼ�������ͼ��
  - `ģ��ͼ��`ָ�ռ���������ȶ��������仯
  - `����ͼ��`��һ�ֿռ�����ͻҶȾ�������������ɢ���ֱ�ʾ��ͼ��
2. ����ͼ����ϵͳ���
  - `�ɼ�`��`��ʾ`��`�洢`��`ͨ��`��`ͼ���������`���ģ��
3. ���ģ��ͼ��������ͼ������ŵ�
  - ���ȸߣ������Ժã�����ԡ�ͨ����ǿ
4. ͼ�����ֻ����裺`����` -> `����`
  - `����`�����ռ���������ͼ��任����ɢ�㡣Բ����Բ����������������������������٣��ռ�ֱ��ʵ͡�
  - `����`�������ػҶȱ任����ɢ������ֵ�������ȼ�Խ�࣬���Խ�ḻ���Ҷȷֱ���Խ�ߣ�����������
5. `�Ҷ�ֱ��ͼ`��һ��ͼ���и��Ҷȵȼ����س��ֵ�Ƶ��֮��Ĺ�ϵ
  - ��Ӧͼ��Ҷȵķֲ����������ӳ����λ�ã�
  - Ӧ�ã��ж�ͼ�������Ƿ�ǡ����ȷ��ͼ��**��ֵ��**��ֵ������ͼ�������������
6. ͼ��任Ŀ�ģ�ʹͼ��������򻯣�������ͼ��������ȡ�������ڴӸ�������ǿ��ͼ����Ϣ�����
7. ͼ��任�㷨��`��ά����Ҷ`�任��`�ֶ�ʲ��������`�任��`����`�任��`С��`�任
  - ��ά����Ҷ���Ƶ�ף��Ľǵ�Ƶ����ӳ�����ò���������Ƶ����Ӧϸ�ڣ�
8. ͼ����ǿ������ͼ�����Ϊԭ�򣬶���ͨ�������跨��ѡ���ͻ���������˻��������ĳЩ����Ȥ����Ϣ������һЩ������Ϣ��
9. ͼ����ǿ�����ɷ�Ϊ`�ռ���`��ֱ�Ӷ����ػҶȲ�������`Ƶ��`����ͼ�񾭸���Ҷ�任���Ƶ�ײ�����
  - `�ռ���`��
    - �Ҷȼ�У�����Ҷȱ任��ֱ��ͼ��������
    - �ֲ�ƽ������������ƽ����
    - �����񻯣�Laplacian��ǿ����
  - `Ƶ��`�� 
    - `ƽ��`��**��ͨ**�˲���
    - `��`��**��ͨ**�˲���
  - `��ɫ��ǿ`��
    - α��ɫ��ǿ���ܶȷָ� 
    - ��ɫͼ����ǿ����ɫƽ��
10. ͼ��ԭ���ؽ���ͼ����ǿ���Բ�����ǿ���Ƿ�ʧ�棬ͼ��ԭ��Ҫ�ָ�ԭ��
11. ͼ��ָ�������
  - 1. �����ָ�����Լ����ԭ 
  - 2. Ƶ����ָ������˲��ָ��� ��ά���˲���
  - 3. ����У�������ػҶ��ڲ壨�����Ԫ����˫�����ڲ壩
12. ����ͼ���˻���ģ����ʧ�桢��������
13. �����׼����������ͼ�����ԭʼͼ��ƫ��̶ȵĲ�ȣ��͹۱����׼��+���۱����׼��
14. ͼ��ѹ������������ѹ��������ѹ��
  - `����`ѹ�������������룬��ũ���룬��������
  - `����`ѹ����Ԥ����루����Ԥ��ͷ�����Ԥ�⣩���任����
15. ���������Ԥ������㷨��֮ͬ����
  - ���������ɾ���Ľ�����ͼ����������������ݣ��������ؽ���ͼ��û���κ�ʧ�档
  - ���������ָ�����ؽ���ͼ����ԭͼ�������ʧ�棬���ܾ�ȷ�ĸ�ԭ�����Ӿ�Ч���ϻ�����ͬ����ʵ�ָ�ѹ���ȵı��뷽ʽ��
16. `ͼ��ָ�`��ָ��ͼ��ֳɻ����ص���������ȡ������ȤĿ��ļ���
17. ���ָ�;����ͬ���Է�Ϊ��
  - 1. ���ڱ�Ե��ȡ�ķָ��㷨
  - 2. ����ָ��㷨 
  - 3. �������������������ŷ���������������
  - 4. ���ѡ��ϲ��ָ��㷨
18. �������õı�Ե������ӣ�
  - Canny ����
  - Laplacian����
  - Sobel ����
19. Hough�任���ֱ�ߺ�Բ�㷨


## ͼ��������

����
- �� ����������ȡ��Աȶȡ��ֱ��ʡ����Ͷȡ����񻯵Ȼ�������
- �� ͼ��Ҷȱ任�����ԡ��ֶ����ԡ�������������������(٤��)�任��
- �� ͼ���˲��������˲��ͷ������˲����ռ��˲���Ƶ�����˲�����ֵ�˲�����ֵ�˲�����˹�˲������˲���ά���˲��ȸ���ͼ��Ļ�������

�߼���ͼ�����:
- �� �ı�ͼ�����б��������������任��͸�ӱ任��
- �� ͼ���Ե��⣺canny���ӡ�sobel���ӡ�Laplace���ӡ�Scharr�˲�����

## ͼ����ǿ

ͼ����ǿ�Ƕ�ͼ����д���ʹ���ԭʼͼ����ʺ����ض���Ӧ�ã�����Ҫ��ʵ��Ӧ�����ϡ�����ͼ���ĳЩ�������Ե���������Աȶȵȣ�ͼ����ǿ�ǽ���ǿ�����񻯣��Ա�����ʾ���۲���һ�������봦��

����ͼ�����������**��**���**��**���������������ͼƬ��**�Ҷ�ֵ��Χ��С**����**�Աȶȵ�**��
- ʵ��Ӧ���У�ͨ������ͼƬ��**�Ҷ�ֱ��ͼ**�������ж�ͼƬ�ĻҶ�ֵ�ֲ���������Աȶȸߵ͡�
- ���ڶԱȶȽϵ͵�ͼƬ������ͨ��һ�����㷨����ǿ��Աȶȡ����õķ�����`���Ա任`��`٤��任`��`ֱ��ͼ���⻯`��`�ֲ�����Ӧֱ��ͼ���⻯`�ȡ�

### �Ҷ�ֱ��ͼ

���ƻҶȷֲ�����ͼ���Ҷȷֲ�ֱ��ͼ�����ߵ���ͼ��
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

numpy ����

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

matplotlib ����

```py
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img = cv.imread(r"C:\Users\Administrator\Desktop\maze.png",0)
rows,cols = img.shape
hist = img.reshape(rows*cols)
histogram,bins,patch = plt.hist(hist,256,facecolor="green",histtype="bar") #histogram��Ϊͳ�Ƴ��ĻҶ�ֵ�ֲ�
plt.xlabel("gray level")
plt.ylabel("number of pixels")
plt.axis([0,255,0,np.max(histogram)])
plt.show()
```

### ͼ����ǿ����

�Աȶ���ǿ: [���](https://www.cnblogs.com/silence-cho/p/11006958.html)
- ��ͼƬ�ĻҶȷ�Χ������ͼƬ�Ҷȷֲ���Χ��\[50,150]֮�䣬���䷶Χ������\[0,256]֮�䡣
- ���Ա任��ֱ��ͼ���滯��٤��任��ȫ��ֱ��ͼ���⻯�����ƶԱȶ�����Ӧֱ��ͼ���⻯���㷨��

ͼ����ǿ����
- �ռ���
  - �����㣺�Ҷȱ任��ֱ��ͼ������
  - �������㣺ƽ������
    - ƽ����ƽ���㷨������ƽ��������ָ�˲����߽籣�����˲��ȡ�
    - ��
- Ƶ����
  - ��ͨ�˲�
  - ��ͨ�˲�
  - ̬ͬ�˲���ǿ
- ��ɫ��ǿ
  - �ٲ�ɫ��ǿ
  - α��ɫ��ǿ
  - ��ɫ�任��ǿ
- ��������


[ͼ��ƽ��֮��ֵ�˲��������˲�����˹�˲�����ֵ�˲�](https://www.toutiao.com/article/6836292532251394567)

ͼ��������������Ҫ�����֣�
- ����������Salt & Pepper��������������ֵĺڰ�����ֵ��
- ����������ֻ���������������͸�����������
- ��˹�������������ȷ��Ӹ�˹����̬�ֲ�����������˹�����Ǻܶഫ����������ģ�ͣ���������ĵ��Ӹ���������

#### �˲�

�˲�����Ҫ���ࣺ���Ժͷ�����
- �����˲�����ʹ�����������������ؼ�Ȩ����ʵ���˲���ͬһģʽ��Ȩ�����ӿ���������ÿһ�������ڣ��������˲����ǿռ䲻��ġ�
  - ���ͼ��Ĳ�ͬ����ʹ�ò�ͬ���˲�Ȩ�����ӣ������˲����ǿռ�ɱ�ġ���˿���ʹ�þ��ģ����ʵ���˲��������˲�����ȥ����˹�����кܺõ�Ч�������õ������˲����о�ֵ�˲����͸�˹ƽ���˲�����
  - (1) ��ֵ�˲�������򵥾�ֵ�˲����Ǿֲ���ֵ���㣬��ÿһ������ֻ����ֲ�����������ֵ��ƽ��ֵ���û���
  - (2) ��˹ƽ���˲�����һ����ݸ�˹��������״��ѡ��Ȩֵ�������˲����� ��˹ƽ���˲�����ȥ��������̬�ֲ��������Ǻ���Ч�ġ�
- �������˲���:
  - (1) ��ֵ�˲���:��ֵ�˲��͸�˹�˲�������Ҫ�������п���ģ��ͼ���м��������Ĳ��֡���ֵ�˲����Ļ���˼��ʹ�����ص�����Ҷ�ֵ����ֵ����������ص�ĻҶ�ֵ��������ȥ��������������������ͬʱ����ͼ���Եϸ�ڡ���ֵ�˲��������������������ֵ���ܴ��ֵ��������̲����м�Ȩ���㡣��ֵ�˲���һ�������¿��Կ˷������˲�������ɵ�ͼ��ϸ��ģ���������˳�������ź���Ч��
  - (2) ��Ե�����˲���:���ھ�ֵ�˲���ƽ��ͼ���⻹���ܵ���ͼ���Եģ������ֵ�˲���ȥ������������ͬʱ���ܽ�ͼ���е�����ϸ���˳�����Ե�����˲��������ۺϿ����˾�ֵ�˲�������ֵ�˲�������ȱ���չ�����ģ������ص��ǣ��˲����ڳ����������ͬʱ���ֲ�����ʹͼ���Եʮ��ģ����

#### ������

��������

```py
# -*- coding:utf-8 -*-
import cv2
import numpy as np
#��ȡͼƬ
img = cv2.imread("test.jpg", cv2.IMREAD_UNCHANGED)
rows, cols, chn = img.shape
#������
for i in range(5000):  
  x = np.random.randint(0, rows)  
  y = np.random.randint(0, cols)  
  img[x,y,:] = 255
cv2.imshow("noise", img)
#�ȴ���ʾ
cv2.waitKey(0)
cv2.destroyAllWindows
```

![](https://p3-sign.toutiaoimg.com/pgc-image/S1PQANUHUzvv2v~noop.image?_iz=58558&from=article.pc_detail&x-expires=1672886951&x-signature=aImTitbc%2F%2Bd4cj0q6LgP%2B6ftUV8%3D)


#### ��ֵ�˲�

��ֵ�˲�
- ��ֵ�˲���ָ����һ�������ֵ��������ΧN*M������ֵ�ľ�ֵ��������ͼ�У���ɫ�������ֵΪ��ɫ������������ֵ֮�ͳ�25��
- ![](https://p3-sign.toutiaoimg.com/pgc-image/S1PQAOWBKmVEju~noop.image?_iz=58558&from=article.pc_detail&x-expires=1672886951&x-signature=A8tTul6nQ8qFr1QM%2BAfB1Y6MA9M%3D)

```py
#encoding:utf-8
import cv2 
import numpy as np 
import matplotlib.pyplot as plt
#��ȡͼƬ
img = cv2.imread('test01.png')
source = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#��ֵ�˲�
result = cv2.blur(source, (5,5)) # ������Ϊ��10��10���ͣ�20��20������ͼ���ø���ģ��
#��ʾͼ��
titles = ['Source Image', 'Blur Image'] 
images = [source, result] 
for i in xrange(2):  
  plt.subplot(1,2,i+1)
  plt.imshow(images[i], 'gray')  
  plt.title(titles[i]) 
  plt.xticks([]),plt.yticks([]) 
  plt.show
```

����������ͼ��ʾ��
- ![](https://p3-sign.toutiaoimg.com/pgc-image/S1PQBHv6oIZHwm~noop.image?_iz=58558&from=article.pc_detail&x-expires=1672886951&x-signature=gko2c3dp3wwoNGu9VhieIRLyBlQ%3D)

#### �����˲�

�����˲�
- �����˲��;�ֵ�˲��˻���һ�£��������費��Ҫ��һ������OpenCV����boxFilter����ʵ�ַ����˲����������£�
- result = cv2.boxFilter(ԭʼͼ��, Ŀ��ͼ�����, �˴�С, normalize����)

#### ��˹�˲�

��˹�˲�
- Ϊ�˿˷��򵥾ֲ�ƽ�����ı׶�(ͼ��ģ��)��Ŀǰ�������ౣ�ֱ�Ե��ϸ�ڵľֲ�ƽ���㷨�����ǵĳ����㶼���������ѡ������Ĵ�С����״�ͷ��򡢲�����ƽ������������Ȩ��ϵ���ȡ�

ͼ���˹ƽ��Ҳ������ƽ����˼���ͼ�����ƽ����һ�ַ�������ͼ���˹ƽ���У���ͼ�����ƽ��ʱ����ͬλ�õ����ر������˲�ͬ��Ȩ�ء���˹ƽ�����ƽ����ͬ�����ڶ����������ؽ���ƽ��ʱ�����費ͬλ�õ����ز�ͬ��Ȩֵ

#### ��ֵ�˲�

��ֵ�˲�
- ��ʹ������ƽ����ȥ���ͬʱҲʹ�ñ߽���ģ��������ֵ�˲��Ƿ����Ե�ͼ����������ȥ���ͬʱ���Լ�˵��߽���Ϣ�ı�����ѡһ������������Ĵ���W�������������ͼ����ɨ�裬�Ѵ��������������ص㰴�Ҷȼ������������У�ȡλ���м�ĻҶ�ֵ������õ�ĻҶ�ֵ


## ͼ��ָ�

- ��2020-7-17��ͼ��ָImage Segmentation���Ǽ�����Ӿ������е�һ����Ҫ������������ͼ������е���Ҫһ����ͼ��ָ��ǽ�����ͼ��ϸ��Ϊ���ͼ��������Ĺ��̣�ͨ���򻯻�ı�ͼ��ı�ʾ��ʽ����ͼ���ܹ��������ױ���⡣
   - ͼ��ָ���� 60 �������ͼ��������ʼ�������о������Ž��������ѧϰ�о��������룬ͼ��ָ��Ҳ��֮���˾޴�ķ�չ��
   - ���ڵ�ͼ��ָ��㷨���ܺܺõطָ�һЩ���г��������Ŀ�꣬�������֡�������ˡ�������������Ϊ���ڵ�ͼ��ָ��㷨���ڼ򵥵�����ֵ��һЩ�Ͳ�����������Ե������ȣ��˹���Ƶ�һЩ��������׼ȷ������Щ���壬��һ�������ⱻ��֮Ϊ������蹵����
   - ������ͼ��ָ�ܺõر������˹�������������ġ�����蹵���������ֻ�ܻ�������ֵ�Լ��Ͳ��������зָ�������ܹ����һЩ���ݸ߲�����ķָ�����
   - �ο���[�������ѧϰ��ͼ��ָ��ڸߵµ�ʵ��](https://yqh.aliyun.com/detail/15920?utm_content=g_1000154176)
   - ![](https://p1-tt-ipv6.byteimg.com/img/pgc-image/9811c9fff31a4fe282dbce591f7642b8~tplv-obj:745:306.image)

## ͼƬС����

��2022-10-19��[���溣�����鳡](https://lab.magiconch.com/)��Ʒ
- [���Ӱ���](https://magiconch.com/patina/)��ͼƬ��������
- [��ͼ������](https://x.magiconch.com/)
- [��ɫͼƬʶ��](https://magiconch.com/nsfw/)
- ��ͼ��[�Ź���](https://v.magiconch.com/sns-image)
- [�㻭�Ҳ�](https://draw.magiconch.com/)������Ϸ


## ͼ��̬��

[Live2D](https://www.live2d.com/en/download/cubism/)

Live2D��һ��Ӧ���ڵ�����Ϸ�Ļ�ͼ��Ⱦ������ͨ��һϵ�е�����ͼ������ｨģ������һ�����ƶ�άͼ�����άģ�͡������Զ������Ϊ����ð����Ϸ��˵�ǳ����á��ü������ձ�Guyzware��˾������Live2D��ǰ��ΪTORAϵͳ������������OIUϵͳ��
- ֪����[��ο���live2D�������](https://www.zhihu.com/question/28130936)

<video width="620" height="440" controls="controls" autoplay="autoplay">
  <source src="https://vdn.vzuu.com/SD/fc42fe58-2322-11eb-a20b-9a794694b530.mp4" type="video/mp4" />
</video>


## ͼ��3D��-��ά�ؽ�

- [2017-9-21]��������ά�ؽ�[3D Face Reconstruction from a Single Image](http://www.cs.nott.ac.uk/~psxasj/3dme/index.php)
- ![demo](https://cdn.vox-cdn.com/thumbor/fXbE0rbXW6WlcmtB1cKBiTsV1b0=/0x0:482x334/1820x1213/filters:focal(203x129:279x205):no_upscale()/cdn.vox-cdn.com/uploads/chorus_image/image/56734861/3d_mark_take_2.0.gif)
- ��2020-7-23��2D��Ƭת3D��Ч�������룺[3d-photo-inpainting](https://github.com/vt-vl-lab/3d-photo-inpainting)
- ![](https://p1-tt-ipv6.byteimg.com/img/pgc-image/54a7f500dc92415f91e0766e2f74c45a~tplv-obj:340:424.image?from=post)
- ��2020-11-18���˵����沿����ϳ� Speech-Driven Animation [Github����](https://github.com/DinoMan/speech-driven-animation)
  - ![](https://github.com/DinoMan/speech-driven-animation/raw/master/example.gif)
- ��2021-3-10���沿����Ǩ�ƣ��⾩+���ӵ� [΢��ʾ��](https://video.weibo.com/show?fid=1034:4609199536013325)
- ��2020-12-29��[����ͼƬ��ά�ؽ�](https://blog.csdn.net/zouxy09/article/details/8083553),Andrew Ng������������ѧ���õ���ͼ��ȥ�ع������������άģ�͡�
   - [˹̹����ѧ](http://ai.stanford.edu/~asaxena/reconstruction3d/)
      - ![](http://ai.stanford.edu/~asaxena/reconstruction3d/Results/mountain_mesh_small.jpg)
   - [���ζ���ѧ](http://www.cs.cornell.edu/~asaxena/learningdepth/)

### ͼ����ά�ؽ��㷨

��2023-3-19��ͼ����ά�ؽ�

��ֹ2022�꣬һЩ2DͼƬ��ά�ؽ��о��������ܣ�Ӣ��[��Ƶ����](https://www.zhihu.com/zvideo/1542654820820869121)

�������ѧϰ��ͼ����ά�ؽ��㷨���ܽϺõ���Ҫ�У�MVSNet��PatchMatchNet��NeuralRecon��
- `MVSNet` ���������ѧϰ����ά�ؽ����Ⱥӣ������ǽ����������ͼƬcost volume��˫Ŀ����ƥ�����ȹ��Ʒ�������չ������ͼƬ����ȹ��ƣ�����ϵ�еĸĽ�˼·��Ҫ�ǰѻع�����ĳ�cascade��
- `PatchMatchNet` ����˴�ͳPatchMatch�㷨�Լ����ѧϰ���ŵ㣬��һ����learning-based PatchmatchΪ�����cascade�ṹ����Ҫ��������FPN�Ķ�߶�������ȡ��Ƕ����cascade�ṹ�е�learning-based Patchmatch�Լ�spatial refinementģ��
- `NeuralRecon` һ���µĻ��ڵ�Ŀ��Ƶ��ʵʱ��ά�����ؽ���ܣ������˼����������άϡ������GRU�㷨����ÿ����ƵƬ�ε�ϡ��TSDF��������������ع����ںϣ���������ܹ�ʵʱ�����ȷ���ؽ���ʵ�������NeuralRecon���ؽ������������ٶ��϶��������еķ�����


### ��Ƶ��ά�ؽ�

��2023-3-22��NVIDIA [2023 GTC���](https://www.nvidia.com/gtc/keynote/)��4:45��ʼ���������и�����Ƶ����3Dģ�͵�

# ͼ������


## pillow

PIL�ṩ��ͨ�õ�ͼ�����ܣ��Լ������Ļ���ͼ���������ͼ�����š��ü�����ת����ɫת���ȡ�
- [Python ͼ���� Pillow ��](https://zhuanlan.zhihu.com/p/58671158)

Matplotlib�ṩ��ǿ��Ļ�ͼ���ܣ����µ�pylab/pyplot�ӿڰ����ܶ෽���û�����ͼ��ĺ�����


### ͼ�����

```py
from PIL import Image
import matplotlib.pyplot as plt

image = Image.open('python-logo.png')  # ����ͼ��ʵ��
# �鿴ͼ��ʵ��������
print(image.format, image.size, image.mode)
image.show() # ��ʾͼ��

img = Image.open("girl.jpg")

plt.figure()
# ��ͼ
plt.subplot(221)
# ԭͼ
plt.imshow(img)
plt.subplot(222)
# ��ͼ�������� 256 * 256
plt.imshow(img.resize((256, 256)))
plt.subplot(223)
# ��ͼ��תΪ�Ҷ�ͼ
plt.imshow(img.convert('L'))
plt.subplot(224)
# ��תͼ��
plt.imshow(img.rotate(45))
# ����ͼ��
plt.savefig("tmp.jpg")
plt.show()

```

![](https://img2018.cnblogs.com/blog/1503464/201909/1503464-20190905210234525-1188098313.jpg)


## opencv

��2022-10-7��[opencv-python��������ƪ](https://zhuanlan.zhihu.com/p/44255577)

### opencv���

opencv �����ڿ��ٴ���ͼ����������Ӿ�����Ĺ��ߣ�֧�ֶ������Խ��п�����c++��python��java��

### Python opencv��װ

������
- 1�� python3
- 2�� numpy
- 3�� opencv-python

```shell
# ��װnumpy
pip install numpy
# ��װopencv-python
pip install opencv-python
```

���ԣ�
- ִ�� import cv2

### ͼ���ȡ

��1��imread��������ȡ����ͼ��

cv2.imread(path_of_image, intflag)
- ����һ�� ��Ҫ����ͼ�������·��
- �������� ��־��ʲô��ʽ����ͼ�񣬿���ѡ��һ�·�ʽ��
  - �� cv2.IMREAD_COLOR�� ���ز�ɫͼ���κ�ͼ���͸���ȶ��������ԡ�����Ĭ�ϱ�־
  - �� cv2.IMREAD_GRAYSCALE���ԻҶ�ģʽ����ͼ��
  - �� cv2.IMREAD_UNCHANGED��������ȡͼƬԭ�е���ɫͨ��
    - �� 1 ����ͬ��cv2.IMREAD_COLOR
    - �� 0 ����ͬ��cv2.IMREAD_GRAYSCALE
    - �� -1 ����ͬ��cv2.IMREAD_UNCHANGED

### ͼ����ʾ

��2��imshow ����
- imshow�����������ڴ�������ʾͼ�񣬴����Զ��ʺ���ͼ���С������Ҳ����ͨ��imutilsģ�������ʾͼ��Ĵ��ڵĴ�С��
- �����ٷ����壺cv2.imshow(windows_name, image)
  - ����һ�� ��������(�ַ���)
  - �������� ͼ�����������numpy�е�ndarray���ͣ�ע���������ͨ��imutilsģ��ı�ͼ����ʾ��С

```py
import cv2
import numpy as np

raw_img = cv2.imread("liu.jpg")
h, w, _ = raw_img.shape
# ��˹ģ��
gaussianBlur = cv2.GaussianBlur(raw_img, (0, 0), 10)
# resize to same scale ����
im1 = cv2.resize(raw_img, (200, 200))
cv2.imwrite('lena.bmp',im1)  # дͼ��
# �ҶȻ� Image to Gray Image
gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
# ���� Gray Image to Inverted Gray Image
inverted_gray_image = 255 - gray_img
## Blurring The Inverted Gray Image
blurred_inverted_gray_image = cv2.GaussianBlur(inverted_gray_image, (19,19),0)
## Inverting the blurred image
inverted_blurred_image = 255-blurred_inverted_gray_image
### Preparing Photo sketching
sketck = cv2.divide(gray_img, inverted_blurred_image,scale= 256.0)
cv2.imshow("Original Image",img) # ������һ������
cv2.imshow("Pencil Sketch", sketck) # �����ڶ�������
# ------ ��ͼչʾ --------
print(raw_img.shape, sketck.shape)
# imgs = np.hstack([img,img2]) # �����̿�
# imgs = np.vstack([img,img2]) # �����̿�
merge = np.hstack((raw_img, gaussianBlur))
cv2.imshow("Pencil Sketch", merge)
# ------ ��ESC�˳���Ĭ���޹رհ����� -----
k = cv2.waitKey(0)
# ͼ����ֺ����ѹ���ƶ����������ٰ����Ż��˳�
if k == 27: # ESC��
  cv2.destroyAllWindows()
```

ע��
- ��ͬ�ߴ硢��ͬ��ɫ��RGB�ͻҶȣ����ܷ���һ�������� -- ����

����취
- ʹ��matplotlib

```py
import cv2
import matplotlib.pyplot as plt

# ʹ��matplotlibչʾ����ͼƬ
def matplotlib_multi_pic1():
    for i in range(9):
        img = cv2.imread('880.png')
        title="title"+str(i+1)
        #�У��У�����
        plt.subplot(3,3,i+1)
        plt.imshow(img)
        plt.title(title,fontsize=8)
        plt.xticks([])
        plt.yticks([])
    plt.show()
matplotlib_multi_pic1()
```


### ͼ��д��

��3��imwrite ����
- imwrite������ͼ�񱣴浽���أ��ٷ����壺cv2.imwrite(image_filename, image)
  - ����һ�� �����ͼ������(�ַ���)
  - �������� ͼ�����������numpy�е�ndarray����


### ��ɫ�ռ�

ͼ����ɫ��Ҫ������ͼ���ܵ�������Ӱ����֮�����Ĳ�ͬ��ɫ��Ϣ��ͬһ���������ͼ���ڲ�ͬ��Դ�����²����Ĳ�ͬ��ɫЧ����ͼ���������ͼ��������ȡ��ʶ�����ʱ��Ҫ����ͼ���**�ݶ���Ϣ**��Ҳ����ͼ��ı������ݣ���**��ɫ��Ϣ**����ݶ���Ϣ��ȡ���һ���ĸ��ţ���˻�����ͼ��������ȡ��ʶ��ǰ��ͼ��ת��Ϊ**�Ҷ�ͼ**������ͬʱҲ�����˴����������������ǿ�˴���Ч����

ͼ��ɫ�ʿռ�任����cv2.cvtColor

�������壺cv2.cvtColor(input_image, flag)
- ����һ�� input_image��ʾ��Ҫ�任ɫ�ʵ�ͼ��ndarray����
- �������� ��ʾͼ��ɫ�ʿռ�任�����ͣ����½��ܳ��õ����֣�
  - �� cv2.COLOR_BGR2GRAY�� ��ʾ��ͼ���BGR�ռ�ת���ɻҶ�ͼ�����
  - �� cv2.COLOR_BGR2HSV�� ��ʾ��ͼ���RGB�ռ�ת����HSV�ռ�

�����鿴����flag��ȫ�����ͣ���ִ�����³����ɲ��ģ��ܹ���274�ֿռ�ת�����ͣ�

```python
import cv2
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
print(flags)
```

### �Զ���ͼ��

��ͼ��ͼ��
- ����һ������ֱ�Ϊw��h��RGB��ɫͼ����˵��ÿ������ֵ����(B��G��R)��һ��tuple��ɣ�opencv-python ��ÿ����������ֵ��˳����B��G��R�������ڻҶ�ͼ����˵��ÿ�����ض�Ӧ�ı�ֻ��һ�����������Ҫ���������ŵ�0��1����Ҷ�ͼ����Ƕ�ֵͼ��0���Ǻ�ɫ��1���ǰ�ɫ

```python
import cv2
#����ͼ����õ��Ծ��������Ǹ���ͨ��Ů��
rgb_img = cv2.imread('E:/peking_rw/ocr_project/base_prehandle/img/cartoon.jpg')
print(rgb_img.shape)     #(1200, 1600, 3)
print(rgb_img[0, 0])     #[137 124  38]
print(rgb_img[0, 0, 0])  #137

gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
print(gray_img.shape)    #(1200, 1600)
print(gray_img[0, 0])    #100
```

��ɫͼ��ĸ߶�height = 1200�� ���w=1600��ͨ����Ϊ3�� ����(0�� 0)��ֵ��(137 124 38)����R=137, G=124, B=38�� ���ڻҶ�ͼ����˵��ֻ�ǵ�ͨ������

���(0, 0, 0)���Ǵ���һ����ɫ���أ�(255, 255, 255)���Ǵ���һ����ɫ���ء���ô�룬B=0, G=0, R=0�൱�ڹر�����ɫͨ��Ҳ���൱���޹��ս��룬����ͼ�������Ǻڵģ���(255, 255, 255)��B=255, G=255, R=255�� �൱�ڴ���B��G��R����ͨ������ȫ�����룬��˱��ǰ�ɫ��

#### ͼ����Ʒ���

���ֻ��Ʒ���
- ֱ��cv2.line��������cv2.rectangle��Բcv2.circle����Բcv2.ellipse�������cv2.polylines�ȼ���ͼ����ƺ���

����������
- �� img�� ��ʾ��Ҫ���л��Ƶ�ͼ�����ndarray
- �� color�� ��ʾ���Ƽ���ͼ�ε���ɫ������BGR������˵��(B��G��R)
- �� thickness�� ��ʾ���Ƽ���ͼ�����ߵĴ�ϸ��Ĭ��Ϊ1������Բ����Բ�ȷ��ͼ��ȡ-1ʱ�����ͼ���ڲ�
- �� lineType �� ��ʾ���Ƽ���ͼ���ߵ����ͣ�Ĭ��8-connected���ǹ⻬�ģ���ȡcv2.LINE_AAʱ�߳��־��״

##### (1) cv2.line����

ֱ�߻��ƺ����� �����ٷ�����Ϊ��
- cv2.line(image, starting, ending, color, thickness, lineType)
- ����image��color��thickness��lineType�ֱ��������������壬����starting��ending�ֱ��ʾ�ߵ�����������ꡢ�յ���������

##### (2) cv2.rectangle����

�����λ��ƺ����������ٷ����壺
- cv2.rectangle(image, top-left, bottom-right, color, thickness, lineType)
- ����image��color��thickness��lineType�ֱ��������������壬����top-left��bottom-right�ֱ��ʾ�����ε����Ͻ��������ꡢ���½���������


##### (3) cv2.circle����
Բ�λ��ƺ������ٷ����庯��Ϊ��
- cv2.circle(image, center, radius, color, thickness, lineType)
- ����image��color��thickness��lineType�ֱ��������������壬����center��radius�ֱ��ʾԲ��Բ���������ꡢԲ�İ뾶���ȣ�Բ���ƺ����е�����thickness = -1 ʱ���Ƶ���ʵ��Բ����thickness >= 0 ʱ���Ƶ��ǿ���Բ


##### (4) cv2.ellipse����

��Բ���ƺ������ٷ�����Ϊ��
- cv2.circle(image, center, (major-axis-length, minor-axis-length), angle, startAngle, endAngle, color, thickness, lineType)
- ��Բ�Ĳ����϶࣬���Ȳ���image��color��thickness��lineType�ֱ��������������壬��Բ���ƺ����е�����thickness = -1 ʱ���Ƶ���ʵ����Բ����thickness >= 0 ʱ���Ƶ��ǿ�����Բ��������������
  - �� center�� ��ʾ��Բ������������
  - �� major-axis-length�� ��ʾ��Բ�ĳ��᳤��
  - �� minor-axis-length�� ��ʾ��Բ�Ķ��᳤��
  - �� angle�� ��ʾ��Բ����ʱ�뷽����ת�ĽǶ�
  - �� startAngle�� ��ʾ��Բ��������˳ʱ�뷽���������Բ������ʼ�Ƕ�
  - �� endAngle�� ��ʾ��Բ��������˳ʱ�뷽���������Բ������ֹʱ�Ƕ�


##### (5) cv2.polylines����

����λ��ƺ������ٷ����庯��Ϊ��
- cv2.polylines(image, \[point-set], flag, color, thickness, lineType)
- ����image��color��thickness��lineType�ֱ��������������壬�����������£�
  - �� \[point-set]�� ��ʾ����ε�ļ��ϣ�����������m���㣬�����һ��m*1*2�����飬��ʾ��m����
  - �� flag�� ��flag = True ʱ���������Ƿ�յģ���flag = False ʱ��������ֻ�Ǵӵ�һ�������һ����������ɵ�ͼ��û�з��


#### ͼ�����ʾ��

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

### ���ز���

#### (1) ��ͼ��ȡ��

```python
reverse_img = 255 - gray_img
```

#### (2) ��ͼ���������Ա任

```python
for i in range(gray_img.shape[0]):
    for j in range(gray_img.shape[1]):
        random_img[i, j] = gray_img[i, j]*1.2
```

![](https://pic4.zhimg.com/80/v2-8fca4ea068a45033056e89236ae1644b_1440w.webp)

��������

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

### ��������

��4���������ٺ���
- ��ʹ��imshow����չʾͼ��ʱ�������Ҫ�ڳ����ж�ͼ��չʾ���ڽ������٣���������޷�������ֹ
- ���õ����ٴ��ڵĺ���������������
  - �� cv2.destroyWindow(windows_name) # ���ٵ����ض�����
    - ������ ��Ҫ���ٵĴ��ڵ�����
  - �� cv2.destroyAllWindows() # ����ȫ�����ڣ��޲���

��ʱ���ٴ��ڣ��϶�����ͼƬ����һ���־ͽ��������٣�������û���ۿ����ڣ����������ַ�ʽ��
- �� �ô���ͣ��һ��ʱ��Ȼ���Զ����٣�
- �� ����ָ������������ָ���ļ����û�Ȼ�����������Ҫ�����Ĵ���

���������������ʹ��cv2.waitKey������ ���Ȳ����������壺cv2.waitKey(time_of_milliseconds)
- Ψһ���� time_of_milliseconds�������������ɸ�Ҳ�����㣬����Ͳ���Ҳ��ͬ���ֱ��Ӧ����˵���������
- �� time_of_milliseconds > 0 ����ʱtime_of_milliseconds��ʾʱ�䣬��λ�Ǻ��룬�����ʾ�ȴ� time_of_milliseconds�����ͼ���Զ�����
- �� time_of_milliseconds <= 0 �� ��ʱͼ�񴰿ڽ��ȴ�һ�������û������յ�ָ���ļ����û������д������١����ǿ����Զ���ȴ��û��ļ��̣�ͨ����������ӽ��и��õĽ���


### ��Ƶ����

[����](https://blog.csdn.net/ljx1400052550/article/details/107410157)

```py
import cv2
import numpy as np
  
# ���屣��ͼƬ����
# image:Ҫ�����ͼƬ����
# addr��ͼƬ��ַ����Ƭ���ֵ�ǰ����
# num: ��Ƭ�����ֵĺ�׺��int ����
def save_image(image,addr,num):
  address = addr + str(num)+ '.jpg'
  cv2.imwrite(address,image)
  
# ��ȡ��Ƶ�ļ�
videoCapture = cv2.VideoCapture("test.mp4")
# ͨ������ͷ�ķ�ʽ
# videoCapture=cv2.VideoCapture(1)

#��֡
success, frame = videoCapture.read()
i = 0
#���ù̶�֡��
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


opencv��ָ��ʱ����ȡƬ�Σ�[��ȡ](https://blog.csdn.net/qq_41251963/article/details/123932842)

��������
- ffmpeg ����

```sh
# ��ʱ�䴰
ffmpeg  -i ./SN.mp4 -vcodec copy -acodec copy -ss 00:00:00 -to 00:00:05 ./cutout1.mp4 -y
# ��֡��ȡ
ffmpeg -i ./input.mp4 -vf "select=between(n\,20\,200)" -y -acodec copy ./output.mp4

```


### opencv ����ʾ��

```python
import numpy as np
import cv2

gray_img = cv2.imread('img/cartoon.jpg', 0)  #���ػҶ�ͼ��
rgb_img = cv2.imread('img/cartoon.jpg', 1)   #����RGB��ɫͼ��

cv2.imshow('origin image', rgb_img)   #��ʾԭͼ
cv2.imshow('origin image', imutils.resize(rgb_img, 800))  #����imutilsģ�������ʾͼ���С
cv2.imshow('gray image', imutils.resize(gray_img, 800))
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()

cv2.imwrite('rgb_img.jpg', rgb_img)   #��ͼ�񱣴��jpg�ļ�
cv2.imwrite('gray_img.png', gray_img) #��ͼ�񱣴��png�ļ�

#��ʾ�ȴ�10��󣬽���������ͼ��
if cv2.waitKey(10000):
    cv2.destroyAllWindows()
#��ʾ�ȴ�10�룬�����ٴ�������Ϊ'origin image'��ͼ�񴰿�
if cv2.waitKey(10000):
    cv2.destroyWindow('origin image')
#��ָ��waitKey(0) == 27ʱ�����û����� Esc ʱ���������д���
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
#�����յ������û�Aʱ������������Ϊ'origin image'��ͼ�񴰿�
if cv2.waitKey(-1) == ord('A'):
    cv2.destroyWindow('origin image')
```

### imutils ���߰�

imutils ����OPenCV�����ϵ�һ����װ���ﵽ��Ϊ���ĵ���OPenCV�ӿڵ�Ŀ�ģ����������ɵ�ʵ��ͼ���ƽ�ƣ���ת�����ţ��Ǽܻ���һϵ�еĲ�����

��װ����

```shell
# �ڰ�װǰӦȷ���Ѱ�װnumpy,scipy,matplotlib��opencv
pip install imutils
# pip install NumPy SciPy opencv-python matplotlib imutils
```

ͼ�������[�ο�](https://walkonnet.com/archives/364235)
- ͼ��ƽ��
  - �����ԭ����cv��ʹ��imutiles����ֱ��ָ��ƽ�Ƶ����أ����ù���ƽ�ƾ���
  - OpenCV��Ҳ�ṩ��ͼ��ƽ�Ƶ�ʵ�֣�Ҫ�ȼ���ƽ�ƾ���Ȼ�����÷���任ʵ��ƽ�ƣ���imutils�п�ֱ�ӽ���ͼ���ƽ�ơ�
  - translated = imutils.translate(img,x,y)
- ���ź�����imutils.resize(img,width=100)
- ͼ����ת
  - ��ʱ����ת rotated = imutils.rotate(image, 90)
  - ˳ʱ����ת rotated_round = imutils.rotate_bound(image, 90)
- �Ǽ���ȡ����Ե��ȡ��
  - �Ǽ���ȡ����Ե��ȡ������ָ��ͼƬ�е�����������˹Ǽ�(topological skeleton)�����Ĺ��̡�
  - imutils�ṩ�ķ�����skeletonize()
- תRGB
  - img = cv.imread("lion.jpeg") 
  - plt.figure() 
  - plt.imshow(imutils.opencv2matplotlib(img))


### ����ʾ��


```python
import cv2
#pip install imutils
import imutils
import numpy as np

rgb_img = cv2.imread('/Users/wqw/Desktop/��ʮ����.png')
# ��ɫ�ռ�ת����rgb �� gray
gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
# -------------
# �ܹ���274�ֿռ�ת�����ͣ�
# flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
# print(flags)
# -----------
cv2.imshow('origin image', imutils.resize(rgb_img, 800))
cv2.imshow('gray image', imutils.resize(gray_img, 800))
cv2.imwrite('rgb_img.jpg', rgb_img)
cv2.imwrite('gray_img.png', gray_img)

# �ȴ�һ��ʱ���Զ�����ͼ�񴰿�
#if cv2.waitKey(10000):
#    cv2.destroyAllWindows()
#if cv2.waitKey(10000):
#    cv2.destroyWindow('origin image')
# �����ض���������ͼ�񴰿�
#if cv2.waitKey(-1) == ord('A'):
#    cv2.destroyWindow('origin image')
if cv2.waitKey(0) == 27: # �� Esc���������д���
    cv2.destroyAllWindows()
```

### gradio web

web�ϲ���ͼ��
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


# ����