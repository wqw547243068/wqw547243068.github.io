---
layout: post
title:  Transformer �Ľ�����
date:   2024-11-01 16:52:00
categories: ���ѧϰ 
tags: ���ѧϰ NLP Transformer BERT GPT Attention BeamSearch seq2seq ��ֲ�� XLNet ѭ������ roformer rwkv �ս��� ���� оƬ ���л� ע���� ����һ�� ������ retnet yoco kan ͨ�ñƽ����� ���Ӷ��� ���� ���ӻ� ttt ����һ��
excerpt: Attention is all you need!
mathjax: true
permalink: /trans_new
---

* content
{:toc}


# Transformer �Ľ�����

## Transformer ����


��2023-9-18��[RetNet�������ڴ��� Transformers ɱ��](https://mp.weixin.qq.com/s/HhRtxONjzkoOmSRqixX50g), [ͷ��](https://www.toutiao.com/article/7304956621552501285/)

Transformer �ѳ�Ϊ������ģ���ϵļܹ�����Ϊ����Ч�ؿ˷���ѭ�������� (RNN) ��˳��ѵ�����⡣

Ȼ����Transformer ������������Ϊ���������ν��`impossible triangle`����**��**���ۡ�

�����������ǡ�����ǰ����ģ���޷�ͬʱʵ��**ѵ��������**��**�ͳɱ�����**�Լ�**ǿ������**������3������ά�ȡ�
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-axegupay5k/e154053c06d24a3a8c24253b5185346e~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1701422819&x-signature=oxc1OeNc6B1%2BDAdIQ%2BaOw8jw%2BA0%3D)

�����ϵķ�����ʾʵ�ֵ�����ά�ȣ���ȱ�ٵ�����������������ԡ�
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/7c1f587ebec642bf9332284352e4a64d~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1701422819&x-signature=nYJb%2B%2FFDdkA1f%2F5FLtlAkG5XEVY%3D)


## �ɽ�����


### �׺� transformer -- CRATE

��2023-11-30��[��GPT-4ֻ����ѹ�����ݡ��������Ŷ�����׺�Transformer���ɽ��͵Ĵ�ģ��Ҫ������](https://mp.weixin.qq.com/s/ErrCWbz8zDqSYkC9DH79Mg)

����������۴�ѧ��`����`�����쵼��һ���о��ŶӸ������Լ��������о������
> ���� GPT-4 ���ڵĵ�ǰ AI ϵͳ����������ѹ����

��������������ܹ� CRATE��ͨ����ѧ��ʽ��֤����һ�㡣
- CRATE ��һ��**�׺� Transformer**���䲻�����ڼ���������������**�ں� Transformer** �����������һ��߱��ǳ���ɫ��**�ɽ�����**��

���ڴˣ�������ڻ��� Twitter �Ϸ�����һ����Ȥ�ļ��⣺
- ��Ȼ��ǰ�� AI ֻ����ѹ�����ݣ���ô��ֻ��ѧϰ�������е�**����� / �ֲ�**�����ԾͲ��������߱�**������߼�����**�����˼��������

��ˣ������ AI ���㲻�� AGI������������ڴ���ͽ�ģ������ά�Ͷ�ģ̬���ݷ��棬���ѧϰ��ʵ����ȡ���˾޴�ĳɹ���

���ֳɹ��鹦�������������Чѧϰ���ݷֲ���**��ѹ���ĵ�ά�ṹ**�������÷ֲ�ת��Ϊ��Լ���������ҽṹ���ģ������������ı��������ڰ�������������񣬱����Ӿ������ࡢʶ��ͷָ���ɡ�

����ѧϰ��ͨ��ѹ��ʽ����ͽ���ʵ�ֵ�

�׺�����������ۡ�Ϊѧϰ���պͽṹ���ı��������һ��ͳһĿ�꣬��ԭ��֤�������ȶ���������ѧϰ���ı�������Ŀ��ּ�ڼ��Ż����ڱ������½���������ڸ����ԣ�Ҳ�Ż�����ϡ���Է�������ڸ����ԡ���Ŀ���Ϊ `ϡ�����½�`��sparse rate reduction����

Ϊ���Ż����Ŀ�꣬���ѧϰһ��**����ӳ������**��ģ��չ��Ŀ�꺯����ĳЩ�����ݶ��½��ĵ����Ż���������õ�һ������ Transformer ���������ܹ�����������ȫ��һ�����׺С����� ���Ż�Ŀ�ꡢ�������Ӻ�ѧϰ���ı�������ѧ������ȫ�ɽ��͵ġ�

����׺���ȼܹ�����Ϊ `CRATE` �� `CRATE-Transformer`������ `Coding-RATE transformer` ����д����ͨ����ѧ��ʽ֤����Щ����ӳ���ڷֲ����������ǿ���ģ��������ǵ���ӳ�䱾������ͬһ����ѧ���ӹ��ɡ�

��ˣ����Խ�������ȫһ���� CRATE �ܹ����ڱ����������������Զ���������

## ģ�ͽṹ

���˵ RetNet �Ǵ�**ƽ������Ч��**�ĽǶȸ���������ܹ�����ô BitNet ��������Ƕ�����������Ч�ʡ�

�����ߵĽ�ϣ��Լ��ں���������ģ��Ч�ʵļ���������ר��ģ�ͣ�MoE����ϡ��ע�������ƣ�Sparse Attention��������Ϊδ������ģ������ܹ��Ļ�����


### RetNet

��2023-9-18��[RetNet�������ڴ��� Transformers ɱ��](https://mp.weixin.qq.com/s/HhRtxONjzkoOmSRqixX50g), [ͷ��](https://www.toutiao.com/article/7304956621552501285/)

΢��� RetNet λ�������`impossible triangle`���������ģ�ʤ�������г��Թ���δ��ʵ����һ׳�ٵķ�����RetNet �跨�ڵ��������ʵ���������ԡ�

ͻ�ƣ�
- RetNet ���и��õ����Խ�ģ����
- RetNet �ڴ����Ľ����� 3.4 ��
- ��.8.4 �����ߵ�������
- ���ӳٽ��� 15.6 ��

���ٶȱȵ�ǰ�� SOTA ��**����������**��ͬʱ���ṩ���õ����ܣ���������Ŷ��ܹ�������һ�㲢�ҽ��뿪Դ�����⽫�Ǿ޴�Ľ�������Ŀǰ΢������ǡ�ңң���ȡ�

RetNet����Ҫ���׿��Ը���Ϊ�����
- RetNet����**��߶ȱ�������**�����**��ͷע����**������������ע���������е�ħ����һ��ɲ��ֵĹؼ���������ˣ����ֱ���������һ��СС�������ϵ�ȱ�㡣
- RetNet ���������ּ��㷶ʽ����ֻ��һ�� Transformer ��ѵ�������������ʹ����ͬ�����д���ʽ��
  - A. **����**��ʾʹѵ���������ܹ�������� GPU �豸��
  - B. **ѭ��**��ʾ���ڴ�ͼ��㷽���ʵ�ָ�Ч�� O(1) �����������Ž��Ͳ���ɱ����ӳ١����⣬��û�м�ֵ���漼�ɵ�����£�ʵ��Ҳ�õ��˼���ļ򻯡�
  - C. **�ֿ�ѭ��**��ʾ����ִ����Ч�ĳ����н�ģ����ÿ�����ؿ���в��б�������߼����ٶȣ�ͬʱ��ȫ�ֿ����ѭ�������Խ�ʡ GPU �ڴ档

���ͻ�������ܹ� Retentive Network��`RetNet`���ɹ�ͻ������ν�ġ�`����������`�����⣬ʵ����`������`��Pareto���Ż���
- RetNet �ڱ������õ���չ���ܺͲ���ѵ����ͬʱ��ʵ���˵ͳɱ�����͸�Ч������

RetNet ����ɱ���ģ�����г����޹أ����ʾ�����Ǵ����ı����У����ǳ�ͼ�����У������δ������������Ƶ���У�RetNet �����Ա����ȶ��ĸ�Ч����


### ΢�� BitNet

��2024-2-29��[BitNet b1.58������1-bit������ģ��ʱ��](https://mp.weixin.qq.com/s?__biz=MzAwMTA3MzM4Nw==&mid=2649498640&idx=1&sn=a860101ceee6bc3a777f465bdd1586da&chksm=82c7cd94b5b0448231f0017d2694e59f6e41369ea14a38a3a19a32a9ba18c3fe0f934e214bee&scene=21#wechat_redirect)

΢�������о�Ժ�Ƴ��� 1-bit LLM �±��壺`BitNet b1.58`��
- ���ı��⣺[The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits](https://arxiv.org/pdf/2402.17764.pdf)

��ģ��ÿ��������ʹ����ֵ��ʾ����-1, 0 �� 1����ˣ��� LLM �ľ���˷�������ֻ��Ҫ�����ӷ���������Ҫ�κθ������˷���ӷ���������ģ������Ⱥ������������ܵ�������
- BitNet b1.58 �ܹ��������ͬ��������ѵ����������ȫ���ȣ���FP16��BF16��Transformer LLM ��ƥ�С�
- ���ͬʱ�������ٶȡ��ڴ�ʹ�á����������ܺĵȷ�����д�����ơ�

BitNet b1.58 Ϊѵ����һ�������ܸ�Ч�ʵ� LLMs ȷ�����µ�**��չ����**��scaling law���ͷ���������������һ��ȫ�µļ��㷶ʽ����Ϊ����רΪ 1-bit LLMs �Ż���Ӳ���豸��ƽ�˵�·��

BitNet �ǵ�һ��֧��ѵ��1���ش�����ģ�͵���������ṹ������ǿ��Ŀ���չ�Ժ��ȶ��ԣ��ܹ��������ٴ�����ģ�͵�ѵ��������ɱ���

�����Ƚ���8��������������ȫ���� Transformer ������ȣ�BitNet �ڴ�������ڴ�ռ�úͼ����ܺĵ�ͬʱ�����ֳ��˼��߾����������ܡ�

���⣬BitNet ӵ����ȫ���� Transformer ���Ƶ�**��ģ����**��Scaling Law�����ڱ���Ч�ʺ��������Ƶ�ͬʱ�������Ը��Ӹ�Ч�ؽ���������չ�����������ģ���ϣ��Ӷ���1���ش�����ģ�ͣ�1-bit LLM����Ϊ���ܡ�

### ΢�� YOCO

��2024-5-13��[YOCO�����ƴ�ͳDecoder-only�ܹ����ڴ����Ľ�ΪTransformer������֮һ](https://mp.weixin.qq.com/s/X4HSyEreN4L4xTizC-_mow)

ģ�ͼܹ���ֻ�������ࣺDecoder-Only��Encoder-Only��Encoder-Decoder��

΢�������о�Ժ�Ƴ���һ�ִ����Ե� Decoder-Decoder �ܹ� `YOCO`��You Only Cache Once����ͨ��**�Խ�����**��**���������**�Ķ��ؼܹ���YOCO ���軺��һ�μ�ֵ�ԣ��Ӷ��������� GPU �ڴ��ʹ�á�
- ���� [You Only Cache Once: Decoder-Decoder Architectures for Language Models](https://arxiv.org/abs/2405.05254)

ģ�������У�YOCO չ�ֳ���ͬ��ģ Transformer ģ�������������ܣ��������Խ�ģ������ģ�ʹ�С��չ�Լ��������Ĵ���������������ơ��ر����ڽ��� GPU �ڴ�ռ�ú�����Ԥ����ӳٷ��棬

YOCO ����ܹ�������£���Ϊ`�Խ�����`��Self-Decoder����`���������`��Cross-Decoder�������֡�

YOCO ʵ���ˡ�**ģ��Խ���ڴ�Խʡ**����Ϊ��Ȼ���Դ������������ȫ�µ��о���Ӧ�÷�ʽ��
- YOCO ������һ�μ�ֵ�ԣ��ɴ������ GPU �ڴ������ұ���ȫ��ע����������

���� GPT ϵ�п����� `Decoder-Only` �ܹ�������� `Decoder-Decoder` ���ͼܹ�����Ϊ `YOCO` (You Only Cache Once)��
- �ڴ��� 512K �����ĳ���ʱ����׼ Transformer �ڴ�ʹ���� YOCO ��6.4����Ԥ����ӳ��� YOCO ��30.3������ YOCO ����������������׼ Transformer ��9.6����


## λ�ñ��뷽ʽ



### 2021.3.23 Roformer

��2021-3-23��Rotary Transformer����� `RoFormer`����׷һ�Ƽ�`�ս���`���е�����ģ��֮һ����Ҫ��ΪTransformer�ṹ������µ�`��תʽλ�ñ���`��Rotary Position Embedding��`RoPE`����
- `RoPE`�������õ��������ʣ�����Ŀǰ**Ψһ**һ���õ�����Attention�ľ���λ�ñ��룬Ŀǰ����ʵ����Ҳ��Ϊ����
- �ο����ã���24G�Դ��3090�ϣ���maxlen=1024��batch_size���ܵ�8���ϡ�

��ϸ���ܣ�
- [Transformer����֮·��2�������ڳ�����תʽλ�ñ���](https://kexue.fm/archives/8265)

ʹ��

- [pytorch�汾](https://github.com/JunnYu/RoFormer_pytorch)
- huggingface [roformer](https://huggingface.co/docs/transformers/model_doc/roformer)

```py
from transformers import RoFormerTokenizerFast

tokenizer = RoFormerTokenizerFast.from_pretrained("junnyu/roformer_chinese_base")
tokenizer.tokenize("���������ǳ��á�")
```


## ������ǿ

����ģ�Ͳ������������ܵ�Ψһ·������һ������/��ѯ��Ϣ�ķ�ʽ����ǿģ�ͣ�С����������ģ��Ҳ�ܴﵽ֮ǰ��ģ�Ͳ��ܴﵽ�����ܡ�

����ģ�͵���������**�����**�������������Ϣ�����壬���Ƕ�����ʵ��Ϣ������֪ʶ��Ϣ����Ч�ġ�
- ��ʱ��Ҫ����ʵ�йص���Ϣ

����
- DeepMind �� RETRO Transformer
  - DeepMind �� RETRO��Retrieval-Enhanced TRansfOrmer��ģ�͡���ģ���� GPT-3 �����൱������������Ϊ GPT-3 �� 4%��
- OpenAI �� WebGPT


### 2021.12.16 WebGPT

OpenAI �Ƴ� WebGPT, ��� long-form quesion-answering (LFQA) �ķ���, ������QA�ظ��������ɿ���
- [WebGPT: Improving the factual accuracy of language models through web browsing](https://openai.com/research/webgpt)
- [WebGPT���](https://zhuanlan.zhihu.com/p/591565418)
- �� InstructGPT �������һЩ

WebGPT ˼·���� Knowledge-Grounded Conversation��������������������ĵ��������Ӷ����ɸ����Ĵ𰸡���Ҫ���������ף�
- ΢��������ģ�Ϳ�����һ�������ı���Web��������������Ӷ����Զ˵��˵�ʹ��ģ�º�ǿ��ѧϰ�Ż������;ۺ�Ч����
- �ο�Web������������Ϣ���ɻظ���labeler���Ը��ݼ�����������Ϣ�ж�factual׼ȷ�ʣ������˶�������������ȷ�Ե��Ѷȡ�

����뷨���� WebGPT�״����
- 2021���, Facebook (FAIR) �����ʹ�����������������Ի��ظ���������ACL2022 [Internet-Augmented Dialogue Generation](https://aclanthology.org/2022.acl-long.579/)

WebGPT ˼·����һ������ȫģ������ʹ����������ķ���(�и���action: �������������ҳ�����˵ȵ�)�����ǽ�����search query��ʹ��������

### 2022.2.7 RETRO

DeepMind �Ƴ� RETRO, �����˴����ݿ��м���������Ϣ����������Ӱ������ʵ������֪ʶ�洢�н�ų�����
- ����: [Improving language models by retrieving from trillions of tokens](https://arxiv.org/pdf/2112.04426.pdf)
- [illustrated-retrieval-transformer](http://jalammar.github.io/illustrated-retrieval-transformer)
- ��2022-1-4��[��������Ϊ4%����������GPT-3��������ͼ��DeepMind��RETRO](https://www.jiqizhixin.com/articles/2022-01-04-8)

�����������֮������ģ�Ϳ�����С�ܶࡣ
- �����ݿ���԰���ģ�ͼ�������Ҫ����ʵ��Ϣ��
- ![](https://image.jiqizhixin.com/uploads/editor/ffbea1f3-54eb-411d-a9a9-3c0912dfef3c/1641280248346.png)

#### ģ�ͽṹ

�ṹ
- RETRO �� **������ - ������**ģ�ͣ���ԭʼ�� Transformer��
- Ȼ���ڼ������ݿ�İ�����������**��������**��
- ��ģ�������ݿ����ҵ�����ܵ����У�����ӵ������С�
- RETRO ��������ħ���������Ԥ�⡣
- ![](https://image.jiqizhixin.com/uploads/editor/96d18172-b521-4ed5-a913-a00440b05625/1641280241153.png)


#### RETRO �������ݿ�

��������ݿ���һ��**��ֵ�洢**��key-value store�����ݿ⡣
- key �Ǳ�׼�� **BERT ����Ƕ��**��value ������������ɵ�**�ı�**��
- Neighbor�����ڼ��� key��
- Completion��ԭ�ļ����ı���������

RETRO ���ݿ�������� MassiveText ���ݼ��� 2 ���ڸ������� token��neighbor chunk �� completion chunk �ĳ������Ϊ 64 �� token��
- ![](https://image.jiqizhixin.com/uploads/editor/713760aa-cf75-4bc7-8116-e308ce3b8b83/1641280228557.png)

#### ���ݿ����

���� RETRO ǰ
- ������ʾ���� BERT�����������������������**ƽ��**�Թ�������Ƕ��������
  - ![](https://image.jiqizhixin.com/uploads/editor/3e8b9491-570a-4280-b36a-e68a6d0fff7c/1641280220663.png)
- Ȼ��ʹ�ø�������ѯ���ݿ⡣����������������������������
  - ![](https://image.jiqizhixin.com/uploads/editor/aac2a845-a303-415b-b582-7b55402db078/1641280209906.png)
- ����Щ��ӵ�����ģ�͵�������
  - ���������ı���Ϊ RETRO �����һ���֣�Transformer �� RETRO �齫��Ϣ�ϲ������ǵĴ�����
  - ![](https://image.jiqizhixin.com/uploads/editor/ff98762d-0d34-4771-8753-56d6b7762648/1641280203796.png)


#### �߲�ε� RETRO �ܹ�

RETRO �ܹ���һ��**������**��ջ��һ��**������**��ջ��ɡ�
- �������ɱ�׼�� Transformer �������飨self-attention + FFNN����ɡ�Retro ʹ�������� Transformer ����������ɵı�������
  - ��������ջ�ᴦ��������Ľ��ڣ����ɺ���������ע������ KEYS �� VALUES ����
- ��������ջ���������ֽ����� block��
  - ��׼ Transformer �������飨ATTN + FFNN��
  - RETRO �������飨ATTN + Chunked cross attention (CCA) + FFNN��
- ������ block �� GPT һ�����������ı�������ʾ token Ӧ����ע���������ֻ��ע֮ǰ�� token����Ȼ��ͨ�� FFNN �㡣ֻ�е��� RETRO ������ʱ�����ſ�ʼ�ϲ�����������Ϣ���� 9 ��ʼ��ÿ�������� block ��һ�� RETRO block�������������ע���ڣ������Ե� 9��12��15��32 ���� RETRO block��
- ![](https://image.jiqizhixin.com/uploads/editor/5103886f-035d-4506-9e03-32b9ec93259b/1641280193608.png)
- ![](https://image.jiqizhixin.com/uploads/editor/305626c2-7918-419a-9e4c-5c8d7eaf0e60/1641280182910.png)




## ������� �Ľ�


���볤�ȸĽ�

### 2023.7.8 LongNet

��2023-7-8��[1000000000��΢��Ľ�Transformerһ���ܼ�ס��ô��token��](https://mp.weixin.qq.com/s/PKKC4lMdSTg-ButNnZHLlw)
- ��ǿ��GPT-4Ҳ�����֧��һ�δ���32k token���൱��50ҳ���֡�
- ���ܹ�ֻ��1���ӿ���һ��������С˵��Claude����token��Ҳ�������š�100k��10�򣩡�

һ������չ��10�ڣ��������������������ʵ�������޵ģ��ⲻ����ζ�ţ����õĽ������������Ͽ�����������������Ϊһ�����У�

�������һ��Transformer���壺`LongNet`����Ӧ����һ�ֽ�����**����ע����**��dilated attention�����Ļ��ƣ��������ž������������ע��������ģ�͸�֪��Χ����ָ������չ��

������ԣ�dilated attention�������ͨTransformer�е�ע�������Ƶģ���һ������ԭ���ǣ�
> ��ע�����ķ�������token֮��������������ָ�����½���

dilated attention�ܹ��������Լ��㸴�ӶȺ�token֮��Ķ��������ԣ��Ӷ������ע������Դ���ޣ���ÿһ��token���ɷ��ʵ�ì�ܡ�


## MLP �Ľ�

����֪����MLP������Ϊ**ȫ����ǰ��**�����磬�ǵ������ѧϰģ�͵Ļ��������顣

MLP ��Ҫ����������ǿ������Ϊ�����ǻ���ѧϰ�����ڱƽ������Ժ�����Ĭ�Ϸ�����

Ȼ����MLP �Ƿ���ѷ����Իع����أ�

���� MLP ���㷺ʹ�ã�����������ȱ�ݡ�
- ���磬�� Transformer ģ���У�MLP �������������з�Ƕ��ʽ����������ͨ����û�к���������ߵ�����£������ע��������˵�����ǵĿɽ����Խϲ

### KAN

��2024-5-3��[TransformerҪ��Kansformer�����˼�ʮ���MLPӭ����ս��KAN](https://www.jiqizhixin.com/articles/2024-05-03-3)

MIT ����� KAN �����Դ�� Kolmogorov-Arnold ��ʾ��������硣
- ���ģ�[KAN: Kolmogorov-Arnold Networks](https://arxiv.org/pdf/2404.19756)
- Github��[pykan](https://github.com/KindXiaoming/pykan)

KAN ��׼ȷ�ԺͿɽ����Է���������� MLP���������Էǳ��ٵĲ�����ʤ���Ը�����������е� MLP��

���о��߽� KAN ���¼ܹ���������չ����������磬������ľ������Ա任����Ϊÿ�������п�ѧϰ�ķ����Լ�������������Դ KAN �����CKAN��
- ��2024-5-20��[���MLP��KAN������Դ��Ŀ��չ�������](https://www.jiqizhixin.com/articles/2024-05-20-2)
- [Convolutional-KANs](https://github.com/AntonioTepsich/Convolutional-KANs)

Kolmogorov 1957 ��ͷ�����**���**�����磬�� Rumerhart��Hinton �� William �� 1986 �����ķ����ʱ��Ҫ��ö࣬����ȴ�����������ˡ�

һ����ǰ���Ķ���֪����MLP���������������Ϊ Kolmogorov-Arnold Networks��KAN����
- MLP ����������Դ��`ͨ�ý��ƶ���` ��ͨ�ñƽ�����
- �� KAN ����������Դ�� `Kolmogorov-Arnold ��ʾ����`��

Kolmogorov-Arnold ��ʾ����
- Vladimir Arnold �� Andrey Kolmogorov ֤������� f ��һ�����н����ϵ�**�������������**����ô f ����д��һ��**��������������**��**��Ԫ�ӷ�����**��������ϡ�

�� MLP ���ƣ�KAN ӵ��**ȫ����**�ṹ���� MLP �ڽڵ㣨��Ԫ���Ϸ��ù̶��������KAN ���ڱߣ�Ȩ�أ��Ϸ��ÿ�ѧϰ�ļ������

��ˣ�KAN **��ȫû������Ȩ�ؾ���**�� [�Ա�ͼ](https://image.jiqizhixin.com/uploads/editor/2ea4a752-4eb5-4bd7-a21f-1f228efcc427/640.png)
- ÿ��Ȩ�ز��������滻Ϊһ����ѧϰ��һά������������Ϊ**����**��spline����
- KAN �Ľڵ���Դ����źŽ�����ͣ�����Ӧ���κη����Ա任��
- ![�Ա�ͼ](https://image.jiqizhixin.com/uploads/editor/2ea4a752-4eb5-4bd7-a21f-1f228efcc427/640.png)

���� KAN ��ѧ��������������ʵ����ֻ��**����**�� **MLP** ����ϣ������˶��ߵ��ŵ㣬������ȱ��ĳ��֡�
- �����ڵ�ά������׼ȷ�ȸߣ����ھֲ������������ܹ��ڲ�ͬ�ֱ���֮���л���Ȼ�������������޷�������Ͻṹ����˴������� COD ���⡣
- ��һ���棬MLP ����������ѧϰ�����������ܵ� COD ��Ӱ�죬���ڵ�ά�ռ���ȴ��������׼ȷ����Ϊ�����޷��Ż�������������

KAN �����ƿ��: ѵ���ٶ�����
- ��ͬ�����Ĳ����£�KAN ��ѵ����ʱͨ���� MLP �� 10 ����
- KAN ѵ���ٶ���������һ��δ�����ԸĽ��Ĺ������⣬������һ�������Ե�����

## Attention �Ľ�


### QKV

MHA��GQA��MQA��MLA ԭ��Ա�
- ��ͳ Transformer ���� MHA���� KV Cache ����������п��ܳ�Ϊ����ƿ����
- `MQA` �� `GQA` ��Ȼ��һ���̶��Ͽ��Լ���KV Cache��ռ�ã���Ч��ͨ������ `MHA`��
- `MLA` ͨ������ Key-Value����ѹ������������ʵ���˱�`MHA`���ŵ�Ч��������������������KV Cache��С��


#### GQA: Grouped-Query Attention

Grouped-Query Attention �����ڸ��������������� context length������� batchsize ��˵��ԭʼ��MHA��multi-head attention�����ڴ�ռ�û���ߣ���Ϊ�ڼ���ʱҪ����pre token��K��V���󣩡�
- MQA��multi-query attention�������е� head ���� 1 �� KV projection ����
- GQA��grouped-query attention ��ʹ�� 8 �� KV projections��ѡ��8����ΪA100 8GPUs�� �������ڴ�ռ�á�

�� 30B ģ����ѵ�� 150B tokens������ GQA Ч���� MHA ��࣬�� MQA Ҫ�ã��� 1 ��node�� 8 �� A100 GPUs �������ٶ� GQA �� MQA��࣬�� MHA Ҫ�ã�MQA �������ʱ��Ҫ�� KV projections ���Ƶ�8�ſ��ϣ���

#### MQA: Muti Query Attention

MQA �� 2019 �������һ���µ� Attention ���ƣ����ܹ��ڱ�֤ģ��Ч����ͬʱ�ӿ� decoder ���� token ���ٶȡ�
- ���ģ� [Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/pdf/1911.02150.pdf)
- ���� head ֮��**����**һ�� key �� value �Ĳ���

MQA �� encoder �ϵ�����û�зǳ����ԣ����� decoder �ϵ������Ǻ�������
- ![](https://pic1.zhimg.com/80/v2-150a48c2eadeacd0aca50408ea391710_1440w.webp)

Multi Query Attention��MQA�� �� Multi Head Attention��MHA��ֻ����һ�����ʣ��ӡ�Head������ˡ�Query����

MQA ��**���е�ͷ֮�� ���� ͬһ�� Key �� Value ����**��ÿ��ͷֻ����������һ�� Query �������Ӷ������� Key �� Value ����Ĳ�������
- ��������������������˼·��Albert ͨ��ʹ��**��㹲�����**��Cross-layer parameter sharing����ʽ�������� bert �Ĳ�����
- MQA ʵ�����ǽ� head �е� key �� value ��������������Ϊһ�ݹ���������� query �������ɱ�����ԭ���� head �У�ÿ�� head ��һ���Լ����е� query ������

�����[ԭ��](https://zhuanlan.zhihu.com/p/634236135)


#### MLA: Multi-head Latent Attention


��2024-9-26��[ע�������Ƶı���֮MLA](https://mp.weixin.qq.com/s/dWZk8TBY89re207ZL3GjfA)

`MLA`(Multi-head Latent Attention) �� ����**�������**�˹�������`DeepSeek` V2 �����һ��**ע�������Ʊ���**��

MLA ������������, ����attention������**KV Cacheռ�ù����ڴ�**�����µ�����ƿ�����⡣

MLA ������**����KVѹ��**��������Ч������KV Cache ��С���Ӷ���������һ���⡣
- �ٷ���������[����](https://arxiv.org/pdf/2405.04434v2)

`MLA` ͨ������ Key-Value����ѹ������������ʵ���˱�`MHA`���ŵ�Ч��������������������KV Cache��С��

MLAͨ����������ѹ��key��value������kv cache��

��ע�������ƵĲ�����������
- ͨ������x���Բ�ͬ�������Wq��Wk��Wv, �õ���ͬ��QKV����
- ת����QKV����ʱ����x����һ�����Ⱦ��󣬵õ��ͽ׾����ʾ
- ��ͨ���߽׾������ָ�ԭ���������ռ䡣���ھ�����ģ�͵�Ȩ�ز����Ѿ����棬����ֻ��Ҫ����һ�����ȵ�Ǳ�������Ϳ��Իָ���KV����������֮ǰ��Ҫͬʱ����KV��


ΪʲôLoRA�����ô���ˣ�ֱ�� MLA �������KV Cache���ȷֽ������?

### �������


#### оƬ

��2023-12-19������оƬ������˾ [Etched AI](https://www.etched.ai/) ���ƿ�����һ���µļ������� Transformer �ܹ�ֱ�ӡ���¼������оƬ��?�����������������ǿ���ר������Transformer����ķ������������������ڲ�����ģ�ͣ�? ˦Ӣΰ��icon��������?
- ![](https://assets-global.website-files.com/6570a6bdf377183fb173431e/6570b5e6b0cd5f0189cf79b8_hero.webp)

�� Transformer�ܹ�ֱ�ӡ���¼����оƬ�У�����ζ��Transformerģ�͵����������ר�ŵ�Ӳ�������У�������Ҫ������ͳ��CPU��GPU���⽫�����������ٶȣ����͹��ģ������ģ�͵����ܡ�
- �����ٶ�Զ�� A100, H100: NVIDIA A100(1x) < NVIDIA H100(5x) < Etched Sohu(15+x)

���ܣ�
- ? **ʵʱ**���������ܹ��ں����ڴ����ǧ����Ĵʡ�
- ? ���õı�����**������**�����Բ��бȽ����ٸ���Ӧ��
- ? �ಥ�Ʋ���룺ʵʱ���������ݡ�
- ? ����δ�������ڲ���ģ�ͣ�ֻ��һ�����ģ�֧��ȫ��Դ���ջ������չ��100T����ģ�͡�
- ? �߼����뼼������������������MCTS���롣
- ? ÿ��оƬ144 GB HBM3E��֧��MoE��ת�������塣

�����Ӣΰ����˵�Ǿ޴����ս��Ӣΰ��һֱ���˹�����������쵼��֮һ����GPU���㷺Ӧ�������ѧϰģ�͵�ѵ��������Ȼ����Etched AI�ļ������ܸı���һ��֡�

��ϸ��iconetched.ai


#### TransNAR

����Transformer��������DeepMind���о���TransNAR����ģ��Ƕ���㷨�������

��2024-6-19��DeepMind ���������**��ϼܹ�**���������Transformerģ�͵�**����**ȱ�ݡ�
- ���ĵ�ַ��[Transformers meet Neural Algorithmic Reasoners](https://arxiv.org/abs/2406.09308)

��Transformer��NLU���������GNN�����㷨��������NAR����ǿ���㷨�����������ϣ�����ʵ�ָ��ӷ������Ƚ���׼ȷ��LLM����
- TransNAR����Ԥѵ��NAR��ǿTransformer
- ![](http://lib.ia.ac.cn:8003/ContentDelivery/20240619/06zc2.05_879FCE72BC2CB9C3039E5FC2ADFE91C3.png)

���㷨����NAR��������֮һPetar Veleckovic, 2021�����˺�����һƪ�������������������ΪPatterns�ڿ���opinion paper��
- ���ĵ�ַ��[Neural Algorithmic Reasoning](https://arxiv.org/abs/2105.02761)

NAR����Ϊ��������ִ���㷨������������������㷨�����ѧϰ�ı��ʲ�ͬ��������������ܹ����õ�ģ���㷨�����������ܾ߱��㷨��ǿ�����ԡ�

NAR �����뷨: 
- ѵ��һ����ά���ռ��еĴ���������P��processor network����ּ�ڲ��ϱƽ��㷨�����н��A(x)��
- �������㷨����������һ����ͼ����������ȳ��󡢽ṹ������ʽ���������ѧϰģ�͸�ά�������Ҷ�������ܲ����ݣ���˻���Ҫѵ��������f�ͽ�����g����������ʽת��Ϊ��Ȼ��ʽ��
- ![](http://lib.ia.ac.cn:8003/ContentDelivery/20240619/06zc2.04_CDB708FC9A27BC289DDAB7A1F81FE99A.png)

NAR ���������ƺ�ԶԶ����Transformer�ܹ�

���: [����Transformer����������DeepMind���о�TransNAR����ģ��Ƕ�롸�㷨������ԡ�](http://lib.ia.ac.cn/news/newsdetail/68837)

### ����Ч��

attention ���� $n^2$ �ļ��㸴�Ӷȣ����ʵ�ָ����ı��ļ��㣿
- ����״̬����: TransformerXL RMT
- ����λ�ñ�����������: ALiBi xPos Unlimiformer
- ���ڹ����Ż�: FlashAttention
- ���ڸ�ЧAttention: Reformer LinFormer Flash
- ������ S4, FLASH
- ![](https://pic3.zhimg.com/80/v2-fae510edc3aff2863cca31bc0dcd2046_1440w.webp)

#### 2023.6.14 FlashAttention

��2023-6-14��[FlashAttention: ����ѵ�����������ĵ�GPT](https://www.bilibili.com/video/BV1SW4y1X7kh)
- �� transformer �� qkv ������٣������������ֿ鲢��
- ��Ƶ����Ч��
- [����ϼ��ĵ�](https://bytedance.feishu.cn/docx/doxcn3zm448MK9sK6pHuPsqtH8f)
- [FlashAttention](https://readpaper.feishu.cn/docx/AC7JdtLrhoKpgxxSRM8cfUounsh)
- [GitHub CodeRepo](https://github.com/cauyxy/bilivideos/tree/master/flash-attn)

<iframe src="//player.bilibili.com/player.html?aid=954566955&bvid=BV1SW4y1X7kh&cid=1158494106&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  height="600" width="100%" > </iframe>


#### 2023.6.24 PageAttention -- ����qkv����

��2023-6-24��UC Berkeley �Ŷ��Ƴ�һ�����ڼ���LLM����Ŀ�Դ��`vLLM`��Vicuna ������������Ļ��Ӣ�ۡ�
- ���� PagedAttention ��������Ч����Attentionģ���е�Key��Value��Cache�����¶�����LLM���������
- ��������κ�ģ�ͼܹ�����������ԭ�� HF Transformers �߳�**24��**��

KV Cache ����˼��
- ���沢����֮ǰ�������Key��Value, �����ظ����㡣

���� Cache �Դ���һЩ���⣬
- Large �󣺶���LLaMA-13B�еĵ������У���ռ�øߴ�1.7GB���ڴ档
- Dynamic ��̬����Сȡ�������г��ȣ������г��Ⱦ��и߶ȿɱ�Ͳ���Ԥ����ص㡣

��ˣ���Ч�ع��� KV Cache ���ش���ս��
- ����ϵͳ��HuggingFace Ĭ��ʵ����pytorch���ڴ������ԣ������ڴ���Ƭ���͹���Ԥ�����˷���60%-80%���ڴ档

Ϊ�˽��������⣬������ PagedAttention��һ���ܴ�ͳ����ϵͳ**�����ڴ�**��**��ҳ**����������ע�����㷨��
- �봫ͳע�����㷨��ͬ��PagedAttention ����**�����ļ���ֵ�洢�ڷ��������ڴ�ռ�**�С�

PagedAttention ��ÿ�����е� KV ����ֳɶ���飬ÿ��������̶������ı�ǵļ���ֵ��
- ��ע������������У�PagedAttention Kernel��Ч��ʶ��ͻ�ȡ��Щ�飬���ò��еķ�ʽ���ټ��㡣����ByteTransformer��˼���е���

[vLLM ԭ�����](https://mp.weixin.qq.com/s/FFcZ1c_a3Ua0vLIj3DGaCQ)


#### 2023.7.4 FasterTransfomer

��2023-7-4��[FasterTransfomer](https://github.com/NVIDIA/FasterTransformer) �� NVIDIA �߶��Ż��� Transformer ģ�Ϳ⣬������ʱ�ﵽ **2.5��**���ٶȣ���� [Inference with FasterTransformer](https://github.com/THUDM/GLM-130B/blob/main/docs/inference-with-fastertransformer.md) 

#### MHA -> DCMHA

KAN

��2024-5-25��[ICML2024�߷����ģ���ģ�ͼ���Ч�ʱ�����200%](https://mp.weixin.qq.com/s/8650CfLSSRUPfiYUTakkNQ)

KANͻȻ���𣬳�Ϊ�������MLP��һ��ȫ��������ܹ���200��������30����������ң�GPT-4o�������ٶ�Ҳ�Ǿ�����һ�ڴ�ģ�Ͱ����ߡ�

��ģ�͵ļ���Ч�ʺ���Ҫ��������ģ�͵�tokens�����ٶ��Ǻܹؼ���һ����

��������ģ�͵�tokens�����ٶȣ����˻�Ǯ����GPU�⣬����Ч�������Ǹ���Transformerģ�ͼܹ��ļ���Ч�ʡ�

���ƿƼ� ��Transformer�������ʱ�ĺ����������**��ͷע����ģ��**��MHA�����֣���Transformer����������������2��֮�ߡ�
- ���ı��⣺[Improving Transformers with Dynamically Composable Multi-Head Attention](https://arxiv.org/abs/2405.08553)
- ��Դ��Ŀ��ַ��[DCFormer](https://github.com/Caiyun-AI/DCFormer)

Github���ѿ�Դ������Ĵ��롢ģ�ͺ�ѵ�����ݼ���

����Transformer�������ĺ���ģ����**��ͷע����**��MHA��ģ�飬λ�ã�position=i���ϵ�ÿһ��**ע����ͷ**��attention head������ȫ��λ���ϵ�ע����ͷ�����һ��ע�����ֲ�����
- ��������У�λ�� i �ϵĸ���ע����ͷ���������ע�����ֲ��������໥�����ġ�

���ֶ�ͷ��������Ļ��ƻ�����������⣺
- ����ƿ����Low-rank Bottleneck����ע����������Ƚϵͣ�ģ�͵ı����������
- ͷ���ࣨHead Redundancy������ͬ��ע����ͷ���ܻ�ѧϰ�����Ƶ�ģʽ����������

��ˣ����ƿƼ������һ�ֽ�**��̬�����**��ͷע������DCMHA���Ļ��ƣ�DCMHA ͨ��һ�����ĵ���Ϻ�����Compose function���������������ķ�ʽת��ע�����÷ֺ�Ȩ�ؾ��󣬴Ӷ���̬�����ע����ͷ������˴�ͳMHAģ���д��ڵ���������ƿ����ͷ�������⡣

DCMHAּ�����ģ�͵ı��������ͬʱ���ֲ����ͼ���Ч�ʣ�������Ϊ�κ�Transformer�ܹ���MHAģ��ļ��弴�����Ʒ���Ի����Ӧ��DCFormerģ�͡�

DCMHA���Ƶĺ����������Compose���������Compose����������Ϊһ����ѧϰ�Ĳ����������Զ�̬����ϲ�ͬͷ��QK�����VO�����ڲ�ͨ��һϵ�б任���ֽ���ع�ע�������������Խ������Ϊ���������ӳ���H��������ע����ͷ����ϳɶ���H*H��ע����ͷ��

�����������ݵ���ͷ֮��Ľ�����ʽ
- һ�Ǵ���ͷ�Ķ�����
- ���ǿ��Ը����������ݶ�̬���

�Ӷ�������ǿģ�͵ı��������

Ч��

����ͨ��ʵ������� `DCFormer` �ڲ�ͬ�ļܹ���ģ�͹�ģ�£������Խ�ģ������������Transformer�������������1.7����2����ģ��������ƥ�䡣

DCFormer�����70%~100%��ģ�ͼ���Ч��
- DCFormer �ڲ�ͬ������ģ�£�405M��6.9B���������� Transformer �� Transformer++ ģ�͵�������������
- DCPythia-6.9B ��Ԥѵ������Ⱥ��������������������ڿ�Դ��Pythia-12B��
- ImageNet-1K���ݼ��ϵ�ʵ����֤��DCMHA�ڷ�����������Ҳ����Ч�Եġ�

��ͬ�Ĳ������£�ʹ��DCFormer���߱���ǿ��ģ�ͱ���������ø��ٵĲ�������ӵ����ͬ��ģ�ͱ�ʾЧ����

DCFormer�ڲ�ͬ�ļܹ���ģ�͹�ģ�£������Խ�ģ������������Transformer�������������1.7����2����ģ��������ƥ�䡣


### ��������

�ı�����һֱ�� transformer ��Ӳ�ˡ�
- ��ͬ�� RNN��transformer ��ѵ��ʱ���뿨��һ��**��󳤶�**�ϣ��⽫����ѵ���õ�ģ���޷���һ����ѵ��ʱ�ĳ�������Զ�ľ�����ȡ�ýϺõ���������

Transformer �У����� token �� token ֮����û��˳��֮�ֵ�. ��ˣ�ͨ����������� Position Embedding ������ÿһ�� token �ھ����е�λ�á�

Position Embedding �����ѡ��ʵ����һ�����⣬ͨ�������¼��֣�
- ��ѧϰ�Ĳ��������ֱȽϳ�����BRET �о�����ô���ģ������ַ�ʽ�׶˺����ԣ���Ϊλ����Ϣ��ѧϰ�����ģ��������ѵ��������û�м�������ĳ�����ȣ������Ч�����޷��õ���֤��
- ����λ�ñ��룺�������� transformer ʹ�õ�λ�ñ��룬�������г�����ʵ�飬���ֱ��������ѵ��/Ԥ��ʱ���ı����Ȳ������󣬣����� 50 ��token �����������½���
- ��ת���룺�������ᵽ���ַ�ʽ�ǱȽϲ���ģ�ֻ����������ÿһ�㶼Ҫ��һ��������ת���Ӷ�����ѵ����������ٶȡ�

transformer ����ģ�͵� ʱ�临�Ӷȡ��ڴ�ʹ�ø��Ӷȶ��� n^2��nΪ���г��ȣ�
- �����г��ȳ��� 512 ʱ��ģ�Ͷ�������Ҫ�󽫻�����ߡ�

���һЩ���� Longformer, Performer, Reformer, Clustered attention ����ͼͨ������ȫע�������Ƹ��Ƹ����⡣

׼BERTע��������ʱ����������У�
- ÿ�������������дʶ��й�ϵ��
- Ϊʲôÿ���ʵ�ע��������������������Ҫ�Ĵ�
- ���֪����Щ������Ҫ��
- �����Ч����ע���������Ǹ���һЩ��



#### ��2020-12-2��AllenAI Longformer

��2020-12-2��Allen AI �Ƴ� Longformer
- ���� [Longformer: Transformer �Ľ��棬�ɴ���ϳ�������](https://ai-scholar.tech/zh/articles/bert/longformer)
- ����: [Longformer: The Long-Document Transformer](https://arxiv.org/pdf/2004.05150.pdf)
- huggingface [longformer](https://huggingface.co/docs/transformers/model_doc/longformer)

Transformer ���㸴�Ӷ����������е����Ӷ��ʶ�����������, ʱ����ڴ�ռ�÷ǳ���
- ԭ��Transformer ��Ҫ���� -- **���ŵ����ע����**��Scaled Dot-Product Self-Attention��
- ��ע�����ļ��㸴�Ӷ�Ϊ `O(N^2)` ������������ʱ���ڴ�ʹ���������������������Ӷ���4��������

Longformer �ǻ��� Transformer �Ŀ���չģ�ͣ����ڴ���**���ĵ�**��������ִ�и����ĵ��� NLP ���񣬶�����Գ�������зֿ�����̣�Ҳ����ʹ�ø��ӵļܹ�����ϸ�����Ϣ��

Longformer ��ϱ��غ�ȫ����Ϣ���Լ�����ע��������������ע�������Ŵ󻬶�����ע������ȫ��ע������������ע���ȫ��ע�⣩��
- ![](https://aisholar.s3.ap-northeast-1.amazonaws.com/media/August2023/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88_2023-08-05_7.16.49.png)

Ч��
- Longformer ���� text8 �� enwik8 ������ȡ����������ܡ�
- Longformer �ڳ��ĵ�����һֱ���� RoBERTa��������Ԥѵ����� WikiHop �� TriviaQA �����б�����ѡ�

RoBERTa ֻ�� 512 ��λ��Ƕ�룬�����Ҫ���� 8 ��λ��Ƕ�������� 4096 ���֡��������ܼ򵥣����ݳ�ȴ�ǳ���Ч������Ȼ����Ϊ���������˷����߽硣

#### ��2021-1-8���ȸ� BigBird


��2021-1-8���ȸ��Ƴ� BigBird, ����**ϡ��ע����**��Transformer��������Transformer��ģ�ͣ����� BERT����չ�����������С�
- ƽ�������������������
- ͬ��Ӳ�������£���������8��
- ���ģ�[Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062)
- ���룺[bigbird](https://github.com/google-research/bigbird)

��Դ���� bigbird Ԥѵ��ģ�ͣ���tiny��base��5������Ԥѵ��ģ�͡��ɴ�[huggingface hub](https://huggingface.co/models?language=zh&sort=downloads&search=bigbird)ֱ������ʹ��

BigBird ģ��ʵ��������ע�������ƣ�**���ע����**��**����ע����**��**ȫ��ע����**������LongFormer��������

��BERTͬ�ȼ������£��ɴ������г��ȴﵽ4096��
- �ܶ೤�ı����е������ϴﵽSOTAЧ�������磺���ı�ժҪ�����ı��ʴ� 
- BigBird RoBERTa ģ����Transformers�ֿ���ʹ�á�

BigBird��ע����������һ������BERT��**ȫע��������**����˲��Ǳ�BERT��ע��������Ч�����ã�����**����Ч�ʸ���**��
- BERT��ע�������ƴ洢�����г����Ƕ��η���ϵ���ڳ��ı�����µĴ洢������Ѿ���ʼ������������
- �� BigBird �� block sparse attention ����Ϊ�˽��������⡣���޳����������ϣ���������� ��ʱ����BERT��ȫע�������ƻ��� block sparse attention�� 


BigBird�����ֳ���ע������ʽ�������ü����ĸ���Ч��
- ȫ�ִʣ�Global token������һЩ�ʣ���Ҫ�����������дʣ��������д�Ҳ��Ҫ�����������硱HuggingFace is building nice libraries for easy NLP���������building����һ��ȫ�ִʣ�ģ�����е���������Ҫ֪���ʡ�NLP���ʹʡ�HuggingFace���Ĺ�ϵ����������������ߺ����ұߣ�����ô�ʡ�building����Ҫ�����ó�ȫ�ִʣ��Ӷ������롱NLP���͡�HuggingFace���Ĺ�ϵ��
- ����ʣ�Random tokens�������ѡ��һЩ�ʣ�����Ϣ���ݸ������ʣ�����Խ��ʹ����֮�����Ϣ�����Ѷȡ�

```py
# �����һ���ʺ����һ������ȫ�ֵ�
global_tokens = ["BigBird", "answering"]
# ��ȫ�ִʼ�����key_tokens������
key_tokens.append(global_tokens)
# �����ôʡ�is���������
random_tokens = ["is"]
key_tokens.append(random_tokens)
key_tokens # {'now', 'is', 'in', 'answering', 'available', 'BigBird'}
# ���ڣ��ʡ�available������ֻ����Щ����ע�������㣬���������д�
```

�ο�
- [bigbird���ı�Ԥѵ��ģ�ͽ���](https://zhuanlan.zhihu.com/p/444333724)
- [BigBird������ģ����������ʽ���ı�ժҪʵ��](https://blog.csdn.net/yjh_SE007/article/details/129244755)

#### 2022.*.* Attention with Linear Bias��ALiBi��

ALiBi �� 2022 �������һ�ַ�������� transformer **ѵ��������ʱ�ı����Ȳ�һ��**�����⣬
- ��������ѵ��ʱ��ʹ�� 1024 ����󳤶ȣ���������ʱ�� 2048 ����󳤶����������� PPL ָ���ƽ��
- ALiBi �����ڲ��Լ��ľ�����󳤶ȵġ�һ�볤�ȡ��Ͻ���ѵ������ Sinusoidal ���������ڡ����Լ����ȡ��Ͻ���ѵ����
- [TRAIN SHORT, TEST LONG: ATTENTION WITH LINEAR BIASES ENABLES INPUT LENGTH EXTRAPOLATION](https://arxiv.org/pdf/2108.12409.pdf)

���ʵ�֣�
- ALiBi ʵ��˼·��ֱ����ģ���ڽ�������ʱֱ��ȥ�� Position Embedding ������������ Attention �м��� query��Key ��ֵ�������һ��ƫ�ó�������ѵ�������������ﵽע��λ����Ϣ��Ч�������������һ�� ���ȼ���� ����ֵ������ÿ��ͷ��head����ֵ��������ͬ��
- ͨ�������λ����Ϣ��������һ���̶��ϻ��⡸����λ����Ϣ����ɵ�ѵ������������г��ȱ��벻һ�µ�����

�����[ԭ��](https://zhuanlan.zhihu.com/p/634236135)


#### 2024.4.10 Infini-Transformer

��2024-4-11��[Google ���Infini-Transformer�ܹ�������LLMs�������޳������ģ��ڴ��Լ114��](https://mp.weixin.qq.com/s/factToEEJdWcs5WJG1Ljfg)
- [Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention](https://arxiv.org/pdf/2404.07143.pdf)

����������СΪ 512�������ĳ���Ϊ 2048 �� 500B ģ�ͣ�ע������ֵ (KV) ״̬���ڴ�ռ��Ϊ 3TB

��Գ������У����ע�������ƣ��ڴ�ѹ������������չ�ԡ�
- �ڴ�ѹ����ʹ�����������г��ȶ����������飬���������޵��ڴ���Դ�ϣ�ά���̶������Ĳ�����������Ϣ�Ĵ洢�ͻص���
- Ȼ����Ŀǰ��LLMs��δ��һ����Ч��ʵ�õ��ڴ�ѹ�������������ڼ���������֮��ȡ��ƽ�⡣

�������ϱ��������������һ���¼ܹ���Infini-Transformer���ܹ��û���Transformer�Ĵ�ģ���������ڴ桢������Դ�������£��������޳������������롣

Infini-Transformer ���������ڴ������£��û���Transformer�Ĵ�����ģ�ͣ�LLMs����Ч�������޳����������С�

��Transformer-XL���ƣ�Infini-Transformer�������һϵ��Ƭ�Ρ�
- ÿ��Ƭ���� ���� standard causal ���attention context��ע���������ģ�����ˣ����ע����������ĳ����������**�ֲ�**�ģ�����������Ϊ S �ĵ�ǰƬ�ε��ܹ� N ����ǡ�
- Ȼ�����ֲ�ע�����ڴ�����һ��Ƭ��ʱ�ᶪ��ǰһ��Ƭ�ε�ע����״̬����Infini-Transformer�У���û�к��Ծɵļ�ֵ��KV��ע����״̬������ͨ���ڴ�ѹ����������ʹ������������������������ʷ��
- ��ˣ�Infini-Transformer��ÿ��ע�����㶼����**ȫ��**ѹ����**�ֲ�**ϸ����״̬�������ǰ���ᵽ������ע������Infini-attention����

ʵ����������
- Infini-Transformer�ڳ����������Խ�ģ�����ϳ�Խ�˻���ģ�ͣ��ڴ���߿ɽ�Լ114����



### TTT

��2024-7-20��[���׸ı�����ģ�ͣ�ȫ�¼ܹ�TTT��ԽTransformer��MLģ�ʹ���RNN����״̬](https://www.jiqizhixin.com/articles/2024-07-10-2)

����
- �������ĵ���ս�� RNN �㱾���������еģ�����ע�������Ʋ�ͬ��RNN ����뽫������ѹ��Ϊ�̶���С������״̬�����¹�����Ҫ������ǧ����������� token ֮��ĵײ�ṹ�͹�ϵ��

˹̹����ѧ�����ݴ�ѧ��������У�����ݴ�ѧʥ�����У�� Meta �����һ���¼ܹ� TTT����**����ѧϰģ��**ȡ���� **RNN ����״̬**��
- ��ģ��ͨ������ token ��ʵ���ݶ��½���ѹ�������ġ�
- ����ʱѵ����Test-Time Training��
- TTT ��ֱ��ȡ�� Attention����ͨ������Լ���������Ը����Լܹ���ʹ�����ܹ�����������ѵ��������������ʱ����ʮ�ڣ��� token �� LLM�� 

TTT ����Ϊһ���µ���Ϣѹ����ģ�ͼ�����ƣ��ɼ򵥵�ֱ����� Transformer �е���ע�����㡣
- �� Mamba ��ȣ�TTT-Linear ������ȸ��ͣ�FLOP ���٣��󣩣��Գ������ĵ����ø��ã��ң���

ȫ�µĴ�����ģ�ͣ�LLM���ܹ��������������� AI ������������� Transformer������Ҳ�� Mamba ���á�
- ���ģ�[Learning to (Learn at Test Time): RNNs with Expressive Hidden States](https://arxiv.org/abs/2407.04620)
- ������ jax ѵ���Ͳ��ԣ�[ttt-lm-jax](https://github.com/test-time-training/ttt-lm-jax)
- PyTorch ������룺[ttt-lm-pytorch](https://github.com/test-time-training/ttt-lm-pytorch)

## ϡ��Attention

### ����

transformer�ܲ�׽��������token֮��Ĺ�ϵ����ʹ�ǳ����롣

�����������ܵ�ע����������ڴ���Դ���ƣ��������г���n����������
- DeepSpeed�ṩ�� **ϡ�� attention kernel** ���� ֧��**������**ģ�����룬�����ı����룬ͼ��������������롣
- ͨ����ϡ����㽫ע�����ļ�����ڴ����󽵵ͼ�����������

�÷�������������ע����������ڴ�ƿ�������ҿ�����Ч��ִ��ϡ����㡣

�����ṩ�㷺��ϡ���Խṹ�⣬�����д����κ��û�����Ŀ�ϡ��ṹ������ԡ�

### �ܽ�

ϡ��Attention
- `Atrous Self Attention` �ն���ע������ֻ�����k,2k,3k,4k...Ԫ��
- `Local Self Attention`
- `Sparse Self Attention`: OpenAI��image transformer��������Sparse self-attention�������߽����һ�飬�ȿ���ѧϰ���ֲ������ԣ��ֿ���ѧϰ��Զ��ϡ��������

|ϡ��Attention|����|˵��||
|---|---|---|---|
|`Atrous Self Attention`|�ն���ע����|![](https://pic2.zhimg.com/80/v2-a39db55945b1ae7c413572b22fbe4cd1_1440w.webp)||
|`Local Self Attention`|�ֲ���ע����|![](https://pic4.zhimg.com/80/v2-c2b46a79fb998e2030ecd8cea99100fb_1440w.webp)||
|`Sparse Self Attention`|ϡ����ע����|![](https://pic4.zhimg.com/80/v2-a2f4cfa836abe8a6fc537048be262ab3_1440w.webp)|�ۺ������ŵ�|

��2019-7-27���ս��֣�[��Լ�������ӱ�׼Attention��ϡ��Attention](https://spaces.ac.cn/archives/6853) ��Լʱ�䡢�Դ档

Attention�ĺ�������Q,K,V �����������еĽ������ںϣ�����Q,K �Ľ�����������������֮���ĳ����ضȣ�Ȩ�أ�������������������ǰ�V����Ȩ����͵õ���

�����ϣ�Self Attention **����ʱ��**��**�Դ�ռ����**���� ?(n^2) ����ģ�n�����г��ȣ�
- ������г��ȱ��ԭ����**2��**���Դ�ռ��������ԭ����**4��**������ʱ��Ҳ��ԭ����**4��**��
- ��Ȼ�����貢�к������㹻�������£�����ʱ��δ�ػ����ӵ�ԭ����4���������Դ��4��ȴ��ʵʵ���ڵģ��޿ɱ��⣬��Ҳ��΢��BertʱOOM��ԭ��

Ϊʲô�� ?(n^2)��
- Ҫ�������е���������������Ҫ������ضȣ��õ�һ��$n^2$��С����ضȾ���
- ![](https://spaces.ac.cn/usr/uploads/2019/07/775103900.png)
- �����ʾ��**ע��������**���ұ���ʾ��**������**�������ÿ��Ԫ�ض�������������Ԫ���й�����

���ԣ���ʡ�Դ棬�ӿ�����ٶȣ�һ���ⷨ��**���ٹ����Լ���**
- ÿ��Ԫ��ֻ�������ڵ�**����Ԫ��**��أ������ϡ��Attention�Ļ���ԭ��
- Դ��OpenAI�����ġ�[Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509)��


### Atrous Self Attention ����ע����

Atrous Self Attention����**����**��ע����������**�ն�**��ע����������**����**��ע�������ȡ�
- �������Զ���, ԭ���ġ�Generating Long Sequences with Sparse Transformers��û�г��ֹ�����������

Atrous Self Attention �����ڡ�**���;��**��Atrous Convolution����������ͼ��ʾ����������Խ�����Լ����ǿ��Ҫ��ÿ��Ԫ��ֻ������Ծ���Ϊk,2k,3k,�� ��Ԫ�ع���������k>1��Ԥ���趨�ĳ��������������ע�������󿴣�����ǿ��Ҫ����Ծ��벻��k
�ı�����ע����Ϊ0����ɫ����0����
- ![](https://spaces.ac.cn/usr/uploads/2019/07/4107095412.png)
- Atrous Self Attention��ע���������󣩺͹���ͼʾ���ң�

�������ڼ���ע�����ǡ����š����ˣ�����ʵ����ÿ��Ԫ��ֻ����Լn/k��Ԫ��������ԣ������������������Ч�ʺ��Դ�ռ�ö������?(n^2/k)��Ҳ����˵��ֱ�ӽ��͵�ԭ����1/k��


### Local Self Attention �ֲ���ע����

Local Self Attention�����ĳơ��ֲ���ע��������
- **��ע����**������CV����ͳ��Ϊ��Non Local��
- ��Local Self Attention��Ҫ����ȫ�ֹ�������������**�ֲ�����**��Լ��ÿ��Ԫ��ֻ��ǰ��k��Ԫ���Լ������й���������ͼ��ʾ��
- ![](https://spaces.ac.cn/usr/uploads/2019/07/713126535.png)
- Local Self Attention��ע���������󣩺͹���ͼʾ���ң�
- ��ע��������������������Ծ��볬��k��ע������ֱ����Ϊ0��

��ʵ Local Self Attention ����ͨ��������ˣ����Ǳ�����һ�� 2k+1 ��С�Ĵ��ڣ�Ȼ���ڴ����ڽ���һЩ���㣬��ͬ������ͨ����ǰѴ���չƽȻ���һ��ȫ���Ӳ�õ�������������Ǵ�����ͨ��ע��������Ȩƽ���õ����������Local Self Attention��˵��ÿ��Ԫ��ֻ�� 2k+1 ��Ԫ��������ԣ�����һ���������������Ч�ʺ��Դ�ռ�ö������ ?((2k+1)n)??(kn) �ˣ�Ҳ����˵����n ����������������һ������������ʡ�����ȻҲֱ�������˳��̹����ԡ�

### Sparse Self Attention -- OpenAI�Ľ����ۺ���������

���ڿ��Ժ���Ȼ������OpenAI�� Sparse Self Attention�ˡ�
- Atrous Self Attention ��һЩ������ Local Self Attention���������Щ��������һ���򵥷�ʽ���ǽ�Local Self Attention��Atrous Self Attention ����ʹ�ã������ۻ�������������Ҳ����ѧϰ��ȫ�ֹ����ԣ�Ҳʡ���Դ档
- ˼·����һ����Local Self Attention�������ÿ���������ں��˾ֲ���������������Ȼ��ڶ�����Atrous Self Attention����Ȼ��������������Ϊ��һ�������ں��˾ֲ����������������Եڶ������������Ͽ��Ը����������������أ�Ҳ����˵ʵ����**���̹���**��
- ����OpenAIֱ�ӽ�����Atrous Self Attention��Local Self Attention�ϲ�Ϊһ��������ͼ��
- ![](https://spaces.ac.cn/usr/uploads/2019/07/1199615308.png)
- Sparse Self Attention��ע���������󣩺͹���ͼʾ���ң�

��ע���������Ͽ��ͺ���������ˣ����ǳ�����Ծ��벻����k�ġ���Ծ���Ϊk,2k,3k,�� ��ע��������Ϊ0������һ��Attention�;��С��ֲ�������غ�Զ��ϡ����ء������ԣ���Ժܶ�������˵������һ����������飬��Ϊ������Ҫ�ܼ��ĳ��̹�����������ʵ���Ǻ��ٵġ�

OpenAI ��Դ�˹ٷ�ʵ�� [sparse_attention](https://github.com/openai/sparse_attention)

## Transformer-Decoder

��2021-4-19��[https://zhuanlan.zhihu.com/p/179959751](https://zhuanlan.zhihu.com/p/79714797)

Transformer ԭʼ���ķ���֮�󣬡�Generating Wikipedia by Summarizing Long Sequences���������һ�� transformer ģ���**���з�ʽ**���������Խ�ģ
- ֱ���ӵ������е� transformer ������ģ�顭����Transformer-Decoder��ģ�͡�

���ڵĻ��� transformer ��ģ���� 6 �� transformer ������ģ��ѵ����ɣ�
- ![](https://pic3.zhimg.com/80/v2-19720b1c70a294558dc9456477156b06_1440w.webp)

������ģ��
- �� transformer ԭʼ������ģ����ȣ�ȥ���˵ڶ�����ע�����㡣

һ�����Ƶļܹ���**�ַ�**��������Խ�ģ��Ҳ����֤��Ч��ʹ�ø������ע�����㹹������ģ�ͣ�һ��Ԥ��һ����ĸ/�ַ���

���н�����ģ�鶼һ����ʹ�ô���ģ����ע�����㡣
- ��ģ����ĳ��Ƭ���п���֧��� **4000** �����ʵ����У������ transformer ԭʼ������� **512** ���ʵ��������˺ܴ��������


# ����