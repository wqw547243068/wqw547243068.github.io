---
layout: post
title:  LLM ��չ����
date:   2024-11-20 12:00:00
categories: ��ģ��
tags: gpt LLM ��ģ�� AGI ����ģ�� ϵͳ ��˼�� ��˼�� ���� ���� �þ� ����  �ɽ���   norm ���� json ���Ŷ��� ���� ��ʶ o1 ttt
excerpt: ��ģ�ͻ����ĸ�����չ��
mathjax: true
permalink: /llm_direction
---

* content
{:toc}


# LLM �Ż�����


��2023-6-16��֪��ר�⣺[��ģ��LLM��������Щ������Ϊѧ���о�����](https://www.zhihu.com/question/595298808/answer/3071907155)

- **ģ�Ͳ�**��
  - GPTϵ�У���ģ̬ϵ�У��Ӿ���SAM��ԭ���Ĺ��ߵ���������
  - ��ȫ�ԣ����ܣ������Σ�����ѧϰ��
  - ��ģ�ͣ��·�ʽ�����ı���ģ������ҪRLHF�ȣ�
  - ӿ��������о����ںе��о���
  - ���С����㡢�Դ���Ż���EL-Attention��ZeRo����֦��������ѹ����
- **�ӿڲ�**��
  - ˽�л�����
  - Adapter��prefix��Lora��
  - Fusing��
- **Ӧ�ò�**��
  - Visual ChatGPT��HuggingGPT��AutoGPT��LangChain��
  - Prompt���̣������⣬dense retrieval��
  - ���Ҿ������ҵ�����chain of thought ��ǿ��
  - �������ݼ�����ʱ���µ�������generatice agents��

�����Ѿ��� GPT-3.5 ����ģ�ͣ�һǧ�ſ���˼������ʲô��Ȼ����Сģ�ͣ�����LLaMa 7Bȥ��֤������ɹ����������Ӵ�13B��30B������һ�����������ߣ���һ��Ҫscale������ģ�ͣ�ֻҪ�Լ��Ľ����ܻ���һ�����������ߣ���ô�������߾Ϳ����Ƶ�����

Դ��֪����[LessTalk](https://www.zhihu.com/question/595298808/answer/3071907155)

- ƽ̨���߼����̻�����
- Сģ����ϴ�ģ�ͽ��ͼ�����
- ��ģ̬�����������
- Prompt Engineering
- ��ֱ����Ӧ�� ����+֪ʶͼ�ס������ˡ��Զ���ʻ��

���
- �������ۣ���ģ�͵Ļ���������ʲô��
- ����ܹ���Transformer���ռ������
- ��Ч���㣺���ʹ��ģ�͸��Ӹ�Ч��
- ��Ч���䣺��ģ��������䵽��������
- �ɿ����ɣ����ʵ�ִ�ģ�͵Ŀɿ����ɣ�
- ��ȫ���ţ���θ��ƴ�ģ���еİ�ȫ�������⣿
- ��֪ѧϰ�����ʹ��ģ�ͻ�ø߼���֪������
- ����Ӧ�ã���ģ������Щ����Ӧ�ã�
- �������ۣ����������ģ�͵����ܣ�
- �����ԣ���ν��ʹ�ģ�͵�ʹ���ż���

���ߣ�[zibuyu9](https://www.zhihu.com/question/595298808/answer/3047369015)

����
- reasoning �߼�����Ŀǰllm�����������ĵط��������ܲ�����llm��leetcode hard����һ���ģ��ܲ����Լ������µ�֪ʶ�������°ͺղ��롣
- compression and acceleration ģ��ѹ������٣���ô��һ��10b��ģ��Ū���ֻ��ϲ���������
- agent����ô���õĸ�llm�����۾����ֽţ���llm���agentִ�����񣬲�������ָ���ȫ�µ�benchmark��������agent��֪���ش��Ե��޶�ΪĿ�ꡣ�ܲ���ͨ��RL�����������?�ͺ͵������Ϸaiһ����
- multi-modal ��ģ̬��GPT-4û�п�Դ������û�м���ϸ�ڣ���ô��һ����Դ�ıƽ�gpt-4��ģ�͡�mini-gpt4, llava�Ǹ�����ĳ��ԡ�
- Hallucination �þ����⣺GPT-4�Ѿ����˺ܶ࣬����Ȼû����ȫ��������������˹��˵Ҫ��TruthGPT. Ҫ��LLM֪֮Ϊ֪֮��֪Ϊ��֪������Ѷ���ʵ�ܴ�
- Evaluation����Դ������Ҫһ���µ�Evaluation�ķ���������llm��Ч�����Ӷ������ƽ���Դllm�Ľ�չ��
- dataset�������chatgpt�����������Դͷ�����ԣ��ܷ�๹��һ��ר�ҵ����ݿ��������Ż�llm�أ�ÿһ�ݿ�Դ���ݶ��ǳ��м�ֵ��

���ģ�[A PhD Student��s Perspective on Research in NLP in the Era of Very Large Language Models](https://arxiv.org/pdf/2305.12544.pdf)


## ģ���ں�

��2024-8-8��[ģ���ں���Ϯ��ChatGPT��Claude �ӽ��ܱ����10����](https://mp.weixin.qq.com/s/zUtQrKuQgyNivaxxrHX1hg)

### ʲô��ģ���ں�

ʲô��ģ���ںϣ�
- �Ѷ��AIģ�͵Ĳ��������һ������һ����ģ�͡�

��, ��Ч��ȴ����ĺ�
- ����Ҫ��������ݺ�������ֻҪ��**ģ��Ȩ��**�Ӽ�һ�¾����ˡ�
- �ںϺ��ģ�ͻ����ܼ�����֮��������������������

���� Prometheus-2 ģ�������аѼ�������ģ�͵������ںϵ�һ���

### �ںϷ���

����������ͼ��[ԭ��](https://mp.weixin.qq.com/s/zUtQrKuQgyNivaxxrHX1hg)
- **����**�ںϣ���򵥴ֱ���ֱ�ӶԲ���**��Ȩƽ��**����Ȼ�򵥵��������Ч��
- **��������**����΢�����ģ�ͼ�ȥԭʼģ�ͣ��õ�һ��"��������"��������������Ӽ�������������ж����ݵ�����������ģ�;������ɸ��ɾ��������ˡ�
- `TIES`�ںϣ����������������ϼ������師 - �޼���ѡ�ٺͷ��룬����ȥ������Ȩ�ء��������������ķ��硣
- `DARE`�ںϣ���TIES˼·���ƣ������������������������ȥ������Ȩ�ء�

�������ӣ�
- ����������[paper](https://arxiv.org/abs/2212.04089)
- TIES��[paper](https://arxiv.org/abs/2306.01708)
- DARE��[paper](https://arxiv.org/abs/2311.03099)
- Ƕ�������ںϣ�[paper](https://arxiv.org/abs/1912.00772)

���� mergekit��
- [merge-models](https://huggingface.co/blog/mlabonne/merge-models)


### GaC

Gac: Generation as Classification

��2024-6-18���Ϻ�AI Lab �Ƴ� [�ں϶����ģ����˼· --- Generation as Classification](https://zhuanlan.zhihu.com/p/715404265)

�����������(��Kaggle)����Ϥ, �ܶ�ʱ��ƴ�ľ��Ǹ���**��ʽģ���ں�**, �����model�ں�(ensemble)�����ͻ������ƿ��, ��������ںϺ�����ܳ����κ�һ������ensemble�ĵ�һģ�͡�

ImageNet �Ӿ���������, ����ģ�ͻ����һ��ά��Ϊ 1000 ��������Ԥ��ÿ�����ĸ��ʣ����������ģ�͵ķ���������������ȡƽ��, �Ϳ���ȡ�ò����׼ȷ������
- ԭ����ߵ��� RepGhostNet 78.81%, ������ģ���ںϺ���������� 80.62%. 

���Ƶ�, ��LLMÿ��generation step������һ�η�������(Generation as Classification, GaC)ȥensemble, �Ӷ����������ɵ�ÿ��token����ȷ��, �����ջ�ø��� response.

����˼��: LLM�����ı�ʱ, ÿ��generation step���ɶ��LLM��ͬ������һ��tokenҪ���ʲô
- ![](https://pica.zhimg.com/80/v2-e8c84b1cf0e391ffe40b2a9fe2fc966a_1440w.webp)
- Paper Title: [Breaking the Ceiling of the LLM Community by Treating Token Generation as a Classification for Ensembling](https://arxiv.org/pdf/2406.12585)
- [GaC](https://github.com/yaoching0/GaC)

���ʵʩ��

����
- LLM ÿ�����ɸ���**�ʻ��ȳ�**�ĸ�������, �� **LLMs �ʻ���Ȳ�һ��**
- ����: 
  - Llama3 �ʻ���� 128256
  - Qwen2  �ʻ���� 152064
- ���ImageNet��������������ģ�Ͷ����1000ά�ȵ�������ͬ.

ֱ������: 
- �����в���ensemble��LLM�ʻ��ȡ**����**�õ� Vu, ����**0-1����**��¼��ԭ��LLM�ʻ��� Vu **��Ӧ��ϵ**. 
- һ��generation step��, ��ÿ��LLM���ɵ�**��������**���Ը��Ե�0-1����ת���� Vu ά��
- �����**ȡƽ��**���õ�ensemble��ĸ�������
- �ٸ��ݸ�����sample����һ��token, ��ʱ���token���������в���ensemble��LLM������
- ��ѡ��һ��token��, ÿ��LLM���ø��Ե�tokenizer�����tokenת��Ϊ���Ե� token id(s), ��ƴ�ص����Ե��������Խ�����һ��generation step.
- ![](https://pic4.zhimg.com/80/v2-007b5f3229ad47a81a4613587dfd4433_1440w.webp)

���ּ�������Ȼ�������е�LLM�����컨�壡(��Ȼ, �����˸��������)
- ![](https://pica.zhimg.com/80/v2-21d29f4a7f9f30cba52ae96330720956_1440w.webp)

Qwen2 �� 2024/06/07 �˳�, ������ʵ���൱�� llama3 �����ں�, ����ָ����ƽ��4%������! �ﵽ 2024/06/07��Դ������ý��

�÷�������ģ�ͼܹ�������, ������ģ�͵��ͳ����ǿ��Բ��ϵ�����ģ��Ϊ�������������컨��.


## �ɿ�����

��2023-7-10��[LLM �ɿ����ɳ�̽](https://mp.weixin.qq.com/s/BngY2WgCcpTOlvdyBNJxqA)

���� LLM ��Ӧ�ÿ��������У��м�����ս��������
- ��α��⡰��˵�˵���, ����ģ�������**�ɿ���/�ȶ���**
- ����ģ�͵ļ��㿪������Ӧ�ٶȵȵ�

Ŀǰ�����Ľ���ֶΰ�����
- ���õ� prompt ���
- ͨ�� retrieval ������ǿ
- ���ⲿ���ߵĽ��
- ���̱������Ʒ���
- ����ʹ�� fine tune ģ�ͻ���ģ��Ӧ��

|Prompt�Ż�����|latency|compute|
|---|---|---|
|Few-Shot CoT|??|??|
|Zero-Shot CoT|?|?|
|Decomposition|??|??|
|Ensembling|?|????|
|Self-Criticism|????|??|
||||

�ɿ�������ֱ�ӵķ�����
- ����ͨ�� prompt ��֪ LLM ��������Ҫ�ķ��ظ�ʽ�����������ɡ�
- ͨ��һЩ��������鷵�ؽ������������ϸ�ʽ��������ش�����Ϣ��
- ����һ�ε��������ݺͼ��Ĵ�����Ϣ��֪ LLM��������һ�ε��������ɡ�
- �ظ� 2-3 ���裬ֱ�����ɵ�������ȫ����Ҫ��

LLM �Ŀɿ��ԡ��ȶ��ԡ���ʵ�ԡ���ȫ�Ե��������ƽ���ҵ��Ӧ���зǳ��ؼ������⣬������Щ��Ŀ���ⷽ�����˺ܶ�̽����Ҳ�кܶ�ֵ�ý���ĵط���

����˼·����˵����Ҫ�ǣ�
- �ṩһ�� prompt ģ�嶨�壬�����û�ָ�� LLM ���ɵĸ�ʽ���������⡣
- ��ģ������ϣ�Ҳ�в�����Ŀ��һ���������Ӧ�ı�����ԣ��� LLM ��ȷ���Գ���Ľ�������ֱ�ۡ�
- �ṩ���� validator����֤�������ݷ���Ԥ�ڣ������ṩ���Զ�����/�������ơ�
- ����һ����Ҳ����������ǰ���и�Ԥ�������� prompt �и����ư������޸�ģ�� decode ʱ�ĸ��ʷֲ��ȡ�
- �����ڿɿ��Ի��������ĸ��������뿪�����Ż������绺�棬���� token ���������Կ�Դģ���������ھ�ȡ�

��ʹ��ֱ��ʹ����������Ŀ��������Ҳ���Դ���ѧϰ���ܶ����õ�˼·����ȻҲ�ǳ��ڴ����������ָ�������˼���뷨���о����Լ� prompt �������Խ���ܷ���ײ������Ļ𻨡�

���ԭ�ģ�[LLM �ɿ����ɳ�̽](https://mp.weixin.qq.com/s/BngY2WgCcpTOlvdyBNJxqA)

### guardrails

guardrails ��Ŀ�������������˽�һ���ĳ������װ���ṩ���� high level �������� API ������������̡�����Ҫ����ɲ��ְ�����
- ������һ�� RAIL spec��������������� 1 ���ᵽ�ķ��ظ�ʽ�޶������� output schema �Ķ����⣬RAILĿǰҲ֧�� input schema��prompt ģ�壬�Լ� instructions ���������á�
- �ṩ��һϵ�е� validation ���ƣ���Ӧ����ĵ� 2 �㡣���� validate ʧ�ܵĲ��֣��ᱣ������ output schema �е�λ�ã�������Ӧ�Ĵ�����Ϣ��
- ͨ�� ReAsk ����ʵ������ĵ� 3 �㣬���͸� LLM �����ݻ���۽��ڴ�����Ϣ���֣��ұ����˽ṹ�������� LLM ���ʹ���
- �������� prompt ģ��֮��Ĺ��ܡ�

### NeMo-Guardrails

NeMo-Guardrails
- ���� Nvidia ��һ��ͬ����Ŀ���� guardrails ����Ұ�ģ���Ҫȷ�� LLM Ӧ�������**���Ŷ�**��**�޺���**�Լ�����**��ȫ��**�ȣ���������ֻ������Ľṹ�������޸���
- �����ʵ��˼·��Ҳ���Ӳ��٣������һ��ר�ŵ� Colang ���ԣ���֧�ָ���ͨ�ö�����ҵ����������������**���� -> ��� -> �޸�**��
- �����Ŀ���רע���û��� LLM �ĶԻ�ʽ����Ӧ�ã���Ҫ����ƶ���Χ�����ǰ��չ����

### guidance

guidance
- ΢���Ƴ��Ŀ�Դ��Ŀ���������߿�ͷ��ͺ�֪�����ֱ��� shap��lime��checklist �����ߡ�֮ǰ���о��� �ɽ��ͻ���ѧϰ��ͬѧӦ�ò���İ������ explainable ai �� controlable llm����Ҳ�Ǻ�˵��ͨ�ķ�չ·��

guardrails �е��������� prompt �и���˵����ʾ����ϣ�� LLM �ܹ���ѭָ�������������ʵ����������ָ������⣬����������һЩ����������˵�����������ɵ� json ��ʽ����ȷ�ȣ�������Ҫ������ **ReAsk ����������**��

LangChain ��Ҳ�ṩ�˸��� output parser ����æ��ȡ�ظ��еĽṹ����Ϣ���֣���Ҳ������������ʧ�ܡ�

�� guidance �У�ͬ����ͨ����ģ�����ԡ������� LLM ������ṹ����ȷ�������ʽ����ȷ�ԡ�����ṹ���� xml ��˵�����д�����Щ

guidance �����Ӹ��ӵ� Handlebars ģ�� ���뵽�� prompt �У�ʹ��ԭ����Ҫ������Ƶ� LLM ����������������̿��Ժܷ������ prompt ��ֱ����ɡ�
- ����������У�ֻ�е����õ�`{{gen}}`����ʱ���Żᴥ�� LLM �����ɲ���������Ҳ����`{{select}}`��`{{#geneach}}`���������ã��߼��жϣ���������������ֽ������Ȼ���������������߳����ĸо���

���� prompt ģ���������⣬guidance ����һϵ�и߼����ԣ�������
- ֧�� hidden block������ LLM ��һЩ������̿��ܲ�����Ҫ��¶�������û����Ϳ�����������������������һЩ�м�����
- Generation caching���Զ����Ѿ����ɹ��Ľ�����������������ٶȡ�
- ֧�� HuggingFace ģ�͵� guidance acceleration����һ�����������ٶȡ�
- Token healing����������һ���֪�� LLM ���������⡭��
- Regex pattern guide����ģ��Ļ����Ͻ�һ��ͨ�����������޶����ɵ����ݹ淶��

### lmql

�� guidance �Ļ����ϣ�lmql ��Ŀ��һ���ѡ�prompt ģ�塱��������ƽ�����һ���µı�����ԣ������е���ǰ�� guardrails �� NeMo-Guardrails �Ĺ�ϵ����Ŀ�����ṩ�˺�Ư���� playground �������ã�ע�����Ҫ�ڱ����������Ŀ����Ҫ������ Python 3.10 �İ汾��


### Json ����

��2024-8-6��[����Ա��ϲ�����˴�ģ�Ͳ��ӵ�Json�����OpenAI����������100%��ȷ](https://mp.weixin.qq.com/s/E2aXlQVzaFQUlFNDjUr-SQ)
- [Introducing Structured Outputs in the API](https://openai.com/index/introducing-structured-outputs-in-the-api)

��ģ�͵� json ��ʽ����ڸ������������ģ�Ͳ���ѭָ�������ʽ�������ʹ�� prompt ����ȷ˵��Ҫ����ָ����ʽ������Json��XML�����ؽ�������������ǲ�������

OpenAI �� GPT-4o ģ��������`2024-08-06`�汾������ȫ�¹��ܣ�
- API ��������`�ṹ�����`��Structured Outputs��

ģ��������ڿɿ�����ѭ������Ա�ṩ�� JSON ģʽ, ʵ�����JSON��**100%׼ȷ��**

֮ǰ������ͨ����������Դ���ߣ����� prompt �����������ô�ģ����ѭ�������ٻ��߷��������������ƹ�LLMs�ڽṹ�������ȱ�ݣ����ڶ�����Ҫ

���ְ취��
- ��1����������: �ں������������� strict��true���нṹ�������
- ��2������response_format ����ѡ��

���ʵ�֣�
- �����ض�����JSON�ܹ�����ģ��ѵ����Openaiͨ�����ַ����ܰ�ģ��׼ȷ���ᵽ**93%**��
  - ������ʼ��JSONģʽ��GPT-4��**40%**׼ȷ�ʣ��Ѿ��߳��ܶ��ˡ�
  - ����ģ�ͱ����ϻ��ǲ�ȷ�����޷���֤JSON���ȶ����
- OpenAIʹ����Լ�����루constrained decoding��������
  - Ĭ������£���ģ���ڽ���token���ʱ�����ڴʻ����ѡ��**����**�ʻ㣬��Ϊ��һ�����token��������**���ɿ���**����ģ�������һЩ�̶���ʽ���ı�ʱ����ʽ����
  - ��ʹ�ö�̬Լ�����뼼���󣬴�ģ������һ��token���ʱ����������һЩԼ������ģ����������Ч��token�ڣ�����������token��
  - ���磺���롰`{"val`������һ�����ɵ��ı�һ�������ǡ�`{`����
  - ��ģ�Ͳ�������ʵ��JSON��ʽ��ȷ������ʵ�ֺ���schema�ṹ��ȷ��

����OpenAI�Ѿ�ͨ�����ַ�ʽʵ����100% JSON���׼ȷ�ʡ�

ȱ��
- ��������SchemaԤ����ʱ�䣬��ģ���������µ�JSON Schemaʱ��Щ��
- Ҫʹ�ýṹ���������һЩ���ƣ�
  - Ŀǰ�ṹ����֧�����һ����JSONģʽ������ String��Number��Boolean��Object��Array��Enum��anyOf��
  - ͬʱ�������ֶλ��ߺ������������ǡ�required����
- **�����Ƕ��**��Ⱥʹ�СҲ�����ơ�
  - һ���ܹ��ܹ��������� 100 ���������ԣ������ 5 ��Ƕ�׼���
  - OpenAI�����˸��ף�**�ṹ����������ܷ�ֹ�������͵�ģ�ʹ���**��ģ�Ϳ����Ի���JSON�����ֵ�з����󣨱�������ѧ����ʽ�в��������������ִ�����Ҫʹ������ָ����ʾ�����ṩʾ�������߽�������Ϊ���򵥵�������
- ��ȫ���ṹ��������ܽ�����OpenAI���еİ�ȫ���ߣ������Ի�ܾ�����ȫ����������������API��Ӧ��������һ�����ַ���ֵ���ÿ�����Ա���Ա�̷�ʽ�����ģ���Ƿ�ܾ����ɡ�


## ֪ʶֲ�� 


LLMs ��Ȼ���ܵ�**֪ʶ�ض�**��**����**��������ơ����磬ChatGPT �� LlaMA �� LLMs ���߱�����ѵ�����ʱ�����Ϣ��Ҳ���ܻ���Ԥѵ�������е�ƫ���Ͳ������ɲ�׼ȷ�����Ե��������ˣ���Ч���� LLMs �Ĳ�����֪ʶ���������ض���Ϊ�����������Ҫ��

����취
- ����**΢��**��**������Ч΢��**�����޸� LLMs�����ɱ��ϸߣ������ܵ��� LLMs ʧȥԤѵ�������������������޸�Ҳ�����ܷ�����������롣
- ʹ��**�ֶ���д**��**����**����ʾӰ�� LLMs ������������෽��û�в������£��ɿ��Բ��㡣


### ֪ʶ�༭ 

Ϊ��ʹ����������Ӱ����С������Ѹ����Ч���޸� LLMs ����Ϊ��һ�ֿ��еĽ��������**֪ʶ�༭**������ LLMs ��֪ʶ�༭�о��ڸ��������������ȡ��������չ������ `Memory based`��`Meta-learning` �� `Locate-Then-Edit` ���෽����

Methods

(1) [Preserve Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#preserve-parameters)
- �� [Memory-based](https://github.com/zjunlp/KnowledgeEditingPapers#memory-based)
1.  **Memory-Based Model Editing at Scale** (ICML 2022)  
  - Eric Mitchell, Charles Lin, Antoine Bosselut, Christopher D. Manning, Chelsea Finn. \[[paper](https://arxiv.org/abs/2206.06520)\] \[[code](https://github.com/eric-mitchell/serac)\] \[[demo](https://sites.google.com/view/serac-editing)\]
2.  **Fixing Model Bugs with Natural Language Patches**. (EMNLP 2022)  
    Shikhar Murty, Christopher D. Manning, Scott M. Lundberg, Marco T��lio Ribeiro. \[[paper](https://arxiv.org/abs/2211.03318)\] \[[code](https://github.com/MurtyShikhar/LanguagePatching)\]
3.  **MemPrompt: Memory-assisted Prompt Editing with User Feedback**. (EMNLP 2022)  
    Aman Madaan, Niket Tandon, Peter Clark, Yiming Yang. \[[paper](https://arxiv.org/abs/2201.06009)\] \[[code](https://github.com/madaan/memprompt)\] \[[page](https://memprompt.com/)\] \[[video](https://www.youtube.com/watch?v=Ld7R02bOiNQ&t=1s)\]
4.  **Large Language Models with Controllable Working Memory**.  
    Daliang Li, Ankit Singh Rawat, Manzil Zaheer, Xin Wang, Michal Lukasik, Andreas Veit, Felix Yu, Sanjiv Kumar. \[[paper](https://arxiv.org/abs/2211.05110)\]
5.  **Can We Edit Factual Knowledge by In-Context Learning?**  
    Ce Zheng, Lei Li, Qingxiu Dong, Yuxuan Fan, Zhiyong Wu, Jingjing Xu, Baobao Chang. \[[paper](https://arxiv.org/abs/2305.12740)\]
6.  **Can LMs Learn New Entities from Descriptions? Challenges in Propagating Injected Knowledge**  
    Yasumasa Onoe, Michael J.Q. Zhang, Shankar Padmanabhan, Greg Durrett, Eunsol Choi. \[[paper](https://arxiv.org/abs/2305.01651)\]
7.  **MQUAKE: Assessing Knowledge Editing inLanguage Models via Multi-Hop Questions**  
    Zexuan Zhong, Zhengxuan Wu, Christopher D. Manning, Christopher Potts, Danqi Chen.  
    .\[[paper](https://arxiv.org/abs/2305.14795)\]

- �� [Additional Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#additional-parameters)
1.  **Calibrating Factual Knowledge in Pretrained Language Models**. (EMNLP 2022)  
    Qingxiu Dong, Damai Dai, Yifan Song, Jingjing Xu, Zhifang Sui, Lei Li. \[[paper](https://arxiv.org/abs/2210.03329)\] \[[code](https://github.com/dqxiu/CaliNet)\]
2.  **Transformer-Patcher: One Mistake worth One Neuron**. (ICLR 2023)  
    Zeyu Huang, Yikang Shen, Xiaofeng Zhang, Jie Zhou, Wenge Rong, Zhang Xiong. \[[paper](https://arxiv.org/abs/2301.09785)\] \[[code](https://github.com/ZeroYuHuang/Transformer-Patcher)\]
3.  **Aging with GRACE: Lifelong Model Editing with Discrete Key-Value Adaptors**.  
    Thomas Hartvigsen, Swami Sankaranarayanan, Hamid Palangi, Yoon Kim, Marzyeh Ghassemi. \[[paper](https://arxiv.org/abs/2211.11031)\] \[[code](https://github.com/thartvigsen/grace)\]
4.  **Neural Knowledge Bank for Pretrained Transformers**  
    Damai Dai, Wenbin Jiang, Qingxiu Dong, Yajuan Lyu, Qiaoqiao She, Zhifang Sui. \[[paper](http://arxiv.org/abs/2208.00399)\]

- �� [Change LM's representation space](https://github.com/zjunlp/KnowledgeEditingPapers#change-lms-representation-space)

1.  **Inspecting and Editing Knowledge Representations in Language Models**  
  - Evan Hernandez, Belinda Z. Li, Jacob Andreas. \[[paper](http://arxiv.org/abs/2304.00740)\] \[[code](https://github.com/evandez/REMEDI)\]

��2��[Modify Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#modify-parameters)

�� [Finetuning](https://github.com/zjunlp/KnowledgeEditingPapers#finetuning)

1.  **Plug-and-Play Adaptation for Continuously-updated QA**. (ACL 2022 Findings)  
  - Kyungjae Lee, Wookje Han, Seung-won Hwang, Hwaran Lee, Joonsuk Park, Sang-Woo Lee. \[[paper](https://arxiv.org/abs/2204.12785)\] \[[code](https://github.com/wookjeHan/Plug-and-Play-Adaptation-for-Continuously-updated-QA)\]
2.  **Modifying Memories in Transformer Models**.  
  - Chen Zhu, Ankit Singh Rawat, Manzil Zaheer, Srinadh Bhojanapalli, Daliang Li, Felix Yu, Sanjiv Kumar. \[[paper](https://arxiv.org/abs/2012.00363)\]
    

��  [Meta-learning](https://github.com/zjunlp/KnowledgeEditingPapers#meta-learning)

1.  **Editing Factual Knowledge in Language Models**.  
  - Nicola De Cao, Wilker Aziz, Ivan Titov. (EMNLP 2021) \[[paper](https://arxiv.org/abs/2104.08164)\] \[[code](https://github.com/nicola-decao/KnowledgeEditor)\]
2.  **Fast Model Editing at Scale**. (ICLR 2022)  
  - Eric Mitchell, Charles Lin, Antoine Bosselut, Chelsea Finn, Christopher D. Manning. \[[paper](https://arxiv.org/abs/2110.11309)\] \[[code](https://github.com/eric-mitchell/mend)\] \[[page](https://sites.google.com/view/mend-editing)\]
3.  **Editable Neural Networks**. (ICLR 2020)  
  - Anton Sinitsin, Vsevolod Plokhotnyuk, Dmitry V. Pyrkin, Sergei Popov, Artem Babenko. \[[paper](https://arxiv.org/abs/2004.00345)\] \[[code](https://github.com/xtinkt/editable)\]
    

�� [Locate and edit](https://github.com/zjunlp/KnowledgeEditingPapers#locate-and-edit)

1.  **Editing a classifier by rewriting its prediction rules**. (NeurIPS 2021)  
  - Shibani Santurkar, Dimitris Tsipras, Mahalaxmi Elango, David Bau, Antonio Torralba, Aleksander Madry. \[[paper](https://proceedings.neurips.cc/paper/2021/hash/c46489a2d5a9a9ecfc53b17610926ddd-Abstract.html)\] \[[code](https://github.com/MadryLab/EditingClassifiers)\]
2.  **Language Anisotropic Cross-Lingual Model Editing**.  
  - Yang Xu, Yutai Hou, Wanxiang Che. \[[paper](https://arxiv.org/abs/2205.12677)\]
3.  **Repairing Neural Networks by Leaving the Right Past Behind**.  
  - Ryutaro Tanno, Melanie F. Pradier, Aditya Nori, Yingzhen Li. \[[paper](https://arxiv.org/abs/2207.04806)\]
4.  **Locating and Editing Factual Associations in GPT**. (NeurIPS 2022)  
  - Kevin Meng, David Bau, Alex Andonian, Yonatan Belinkov. \[[paper](https://arxiv.org/abs/2202.05262)\] \[[code](https://github.com/kmeng01/rome)\] \[[page](https://rome.baulab.info/)\] \[[video](https://www.youtube.com/watch?v=_NMQyOu2HTo&t=0)\]
5.  **Mass-Editing Memory in a Transformer**.  
  - Kevin Meng, Arnab Sen Sharma, Alex Andonian, Yonatan Belinkov, David Bau. \[[paper](https://arxiv.org/abs/2210.07229)\] \[[code](https://github.com/kmeng01/memit)\] \[[page](https://memit.baulab.info/)\] \[[demo](https://memit.baulab.us/#/)\]
6.  **Editing models with task arithmetic** .  
  - Gabriel Ilharco, Marco Tulio Ribeiro, Mitchell Wortsman, Ludwig Schmidt, Hannaneh Hajishirzi, Ali Farhadi. \[[paper](https://openreview.net/pdf?id=6t0Kwf8-jrj)\]
7.  **Editing Commonsense Knowledge in GPT** .  
  - Anshita Gupta, Debanjan Mondal, Akshay Krishna Sheshadri, Wenlong Zhao, Xiang Lorraine Li, Sarah Wiegreffe, Niket Tandon. \[[paper](https://arxiv.org/abs/2305.14956)\]
8.  **Do Language Models Have Beliefs? Methods for Detecting, Updating, and Visualizing Model Beliefs**.  
  - Peter Hase, Mona Diab, Asli Celikyilmaz, Xian Li, Zornitsa Kozareva, Veselin Stoyanov, Mohit Bansal, Srinivasan Iyer. \[[paper](https://arxiv.org/pdf/2111.13654.pdf)\] \[[code](https://github.com/peterbhase/SLAG-Belief-Updating)\]
9.  **Detecting Edit Failures In Large Language Models: An Improved Specificity Benchmark** .  
  - Jason Hoelscher-Obermaier, Julia Persson, Esben Kran, Ioannis Konstas, Fazl Barez. \[[paper](https://arxiv.org/abs/2305.17553)\]
10.  **Knowledge Neurons in Pretrained Transformers**.(ACL 2022)  
  - Damai Dai , Li Dong, Yaru Hao, Zhifang Sui, Baobao Chang, Furu Wei.\[[paper](http://arxiv.org/abs/2104.08696)\] \[[code](https://github.com/Hunter-DDM/knowledge-neurons)\] \[[code by EleutherAI](https://github.com/EleutherAI/knowledge-neurons)\]
11.  **LEACE: Perfect linear concept erasure in closed form** .  
  - Nora Belrose, David Schneider-Joseph, Shauli Ravfogel, Ryan Cotterell, Edward Raff, Stella Biderman. \[[paper](https://arxiv.org/abs/2306.03819)\]
12.  **Transformer Feed-Forward Layers Are Key-Value Memories**. (EMNLP 2021)  
  - Mor Geva, Roei Schuster, Jonathan Berant, Omer Levy. \[[paper](https://arxiv.org/abs/2012.14913)\]
13.  **Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space**.(EMNLP 2022)  
  - Mor Geva, Avi Caciularu, Kevin Ro Wang, Yoav Goldberg. \[[paper](https://arxiv.org/abs/2203.14680)\]
14.  **PMET: Precise Model Editing in a Transformer.**  
  - Xiaopeng Li, Shasha Li, Shezheng Song, Jing Yang, Jun Ma, Jie Yu. \[[paper](https://arxiv.org/abs/2308.08742)\] \[[code](https://github.com/xpq-tech/PMET.git)\]
    

��3�� [More Related Papers](https://github.com/zjunlp/KnowledgeEditingPapers#more-related-papers)

1.  **FRUIT: Faithfully Reflecting Updated Information in Text**. (NAACL 2022)  
    Robert L. Logan IV, Alexandre Passos, Sameer Singh, Ming-Wei Chang. \[[paper](https://github.com/zjunlp/KnowledgeEditingPapers/blob/main)\] \[[code](https://github.com/zjunlp/KnowledgeEditingPapers/blob/main)\]
    
2.  **Entailer: Answering Questions with Faithful and Truthful Chains of Reasoning**. (EMNLP 2022)  
    Oyvind Tafjord, Bhavana Dalvi Mishra, Peter Clark. \[[paper](https://arxiv.org/abs/2210.12217)\] \[[code](https://github.com/allenai/entailment_bank)\] \[[video](https://www.youtube.com/watch?v=GYTJ_Pxva7Q)\]
    
3.  **Towards Tracing Factual Knowledge in Language Models Back to the Training Data**.  
    Ekin Aky��rek, Tolga Bolukbasi, Frederick Liu, Binbin Xiong, Ian Tenney, Jacob Andreas, Kelvin Guu. (EMNLP 2022) \[[paper](https://arxiv.org/abs/2204.12785)\]
    
4.  **Prompting GPT-3 To Be Reliable**.  
    Chenglei Si, Zhe Gan, Zhengyuan Yang, Shuohang Wang, Jianfeng Wang, Jordan Boyd-Graber, Lijuan Wang. \[[paper](https://arxiv.org/abs/2210.09150)\]
    
5.  **Patching open-vocabulary models by interpolating weights**. (NeurIPS 2022)  
    Gabriel Ilharco, Mitchell Wortsman, Samir Yitzhak Gadre, Shuran Song, Hannaneh Hajishirzi, Simon Kornblith, Ali Farhadi, Ludwig Schmidt. \[[paper](https://arxiv.org/abs/2208.05592)\] \[[code](https://github.com/mlfoundations/patching)\]
    
6.  **Decouple knowledge from paramters for plug-and-play language modeling** (ACL2023 Findings)  
    Xin Cheng, Yankai Lin, Xiuying Chen, Dongyan Zhao, Rui Yan.\[[paper](http://arxiv.org/abs/2305.11564)\] \[[code](https://github.com/Hannibal046/PlugLM)\]
    
7.  **Backpack Language Models**  
    John Hewitt, John Thickstun, Christopher D. Manning, Percy Liang. \[[paper](https://arxiv.org/pdf/2305.16765.pdf)\]
    
8.  **Learning to Model Editing Processes**. (EMNLP 2022)  
    Machel Reid, Graham Neubig. \[[paper](https://aclanthology.org/2022.findings-emnlp.280.pdf)\]

 [Analysis](https://github.com/zjunlp/KnowledgeEditingPapers#analysis)

1.  **Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models.**  
    Peter Hase, Mohit Bansal, Been Kim, Asma Ghandeharioun. \[[paper](https://arxiv.org/pdf/2301.04213.pdf)\] \[[code](https://github.com/google/belief-localization)\]
2.  **Dissecting Recall of Factual Associations in Auto-Regressive Language Models**  
    Mor Geva, Jasmijn Bastings, Katja Filippova, Amir Globerson. \[[paper](https://arxiv.org/abs/2304.14767)\]
3.  **Evaluating the Ripple Effects of Knowledge Editing in Language Models**  
    Roi Cohen, Eden Biran, Ori Yoran, Amir Globerson, Mor Geva. \[[paper](https://arxiv.org/abs/2307.12976)\]
4.  **Edit at your own risk: evaluating the robustness of edited models to distribution shifts.**  
    Davis Brown, Charles Godfrey, Cody Nizinski, Jonathan Tu, Henry Kvinge. \[[paper](https://arxiv.org/abs/2303.00046)\]


#### FastEdit ����

����ע��֪ʶ

- ��2022-2-10��Rank-One Model Editing (ROME): [Locating and Editing Factual Associations in GPT](https://arxiv.org/abs/2202.05262), [demo](https://rome.baulab.info/)

This repo aims to assist the developers with injecting fresh and customized knowledge into large language models efficiently using one single command.

Supported Models
-   [GPT-J](https://huggingface.co/EleutherAI/gpt-j-6b) (6B)
-   [LLaMA](https://github.com/facebookresearch/llama) (7B/13B)
-   [LLaMA-2](https://huggingface.co/meta-llama) (7B/13B)
-   [BLOOM](https://huggingface.co/bigscience/bloomz) (7.1B)
-   [Falcon](https://huggingface.co/tiiuae/falcon-7b) (7B)
-   [Baichuan](https://huggingface.co/baichuan-inc/Baichuan-7B) (7B/13B)
-   [InternLM](https://github.com/InternLM/InternLM) (7B)

[Implemented Algorithms](https://github.com/hiyouga/FastEdit#implemented-algorithms)
-   [Rank-One Model Editing (ROME)](https://arxiv.org/abs/2202.05262)


```sh
git clone https://github.com/hiyouga/FastEdit.git
conda create -n fastedit python=3.10
conda activate fastedit
cd FastEdit
pip install -r requirements.txt
# ��
pip install pyfastedit
```

Model Editing

```sh
CUDA_VISIBLE_DEVICES=0 python -m fastedit.editor \
    --data data/example.json \
    --model EleutherAI/gpt-j-6b \
    --config gpt-j-6b \
    --template default
```

#### EasyEdit ��� -- ��Դ

��2023-8-16��[����Ʒ����ģ�����ɻ�ȡ������֪ʶ�����ȴ�ͳ΢��Ч������](https://www.toutiao.com/article/7267801834855727679)
- ֪ʶ�༭ papaerlist: [Knowledge Editing for LLMs Papers](https://github.com/zjunlp/KnowledgeEditingPapers)
- ��2023-5-23��[Editing Large Language Models: Problems, Methods, and Opportunities](https://arxiv.org/abs/2305.13172)
- ![](https://github.com/zjunlp/KnowledgeEditingPapers/raw/main/img/overview.jpg)

�㽭��ѧ�Ͷ���ʵ���ҵ��о��Ŷ������һ������ʹ�õ� LLMs ֪ʶ�༭��ܡ���`EasyEdit`���ÿ��֧�ָ���֪ʶ�༭�������ҿ�������Ӧ�����ڶ� LLMs���� T5��GPT-J �� LlaMA �ȡ�
- ���� [EasyEdit: An Easy-to-use Knowledge Editing Framework for Large Language Models](https://arxiv.org/abs/2308.07269)
- ���� [EasyEdit](https://github.com/zjunlp/EasyEdit)

Ȼ����Ŀǰ���� `LLMs ֪ʶ�༭`���о���ʵ�ֺ����������ϵĲ��������֪ʶ�༭ͳһ���ۺϿ�ܵķ�չ��ֵ��ע����ǣ����ָ������谭�˲�ͬ����֮����Ч�ԺͿ����Ե�ֱ�ӱȽϣ�Ҳʹ�ô����µ�֪ʶ�༭������ø��ӡ�

EasyEdit ��������˸��ֱ༭������֧���ڲ�ͬ LLMs ֮���������ģ�顣ͨ��ͳһ�Ŀ�ܺͽӿڣ�EasyEdit ��ʹ�û�Ѹ����ⲢӦ�ð����ڸÿ���е�����֪ʶ�༭������EasyEdit ����ͳһ�� Editor��Method �� Evaluate ��ܣ��ֱ����**�༭����**��**�༭����**��**��������**��
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCdrGGtbIFt~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=qjF%2FeWeSs6aesEsE1h%2BZuHMGRz8%3D)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCf8CHe0fQA~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=4GKQB2crsR9z9gIr9p31Cav6dq8%3D)


EasyEdit ���ṩ����������༭�������ܵĹؼ�ָ�꣬����`�ɿ���`��Reliability����`������`��Generalization����`�ֲ���`��Locality����`����ֲ��`��Portability����`Ч��`��Efficiency����

Ϊ��֤֪ʶ�༭�� LLMs �е�Ӧ��Ǳ�����о��Ŷ�ѡ���˲����Ӵ�� LlaMA 2 ģ�ͣ������� ZsRE ���ݼ���QA ���ݼ���������֪ʶ�༭������һ����ʵ�������Ͻ�ģ�͵����������Խ��֤����EasyEdit �ڿɿ��Ժͷ����Է��泬Խ�˴�ͳ��΢��������
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCiL5n53x88~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=wQPBTjiUF%2FX%2BszdxJIiTV%2FbPDe8%3D)



## ģ�ͽṹ

��� [LLM �ܹ��������](llm_code)


### Transformer �Ľ�

���վ��: [transformer �Ľ�ר��](transformer_evolution)

### ���� Transformer

transformer �ܹ�����Ψһ

#### ttt

ttt �����ע������
- ���ı��⣺[The Surprising Effectiveness of Test-Time Training for Abstract Reasoning](https://ekinakyurek.github.io/papers/ttt.pdf)

�� TTT ��ЧӦ���� few-shot ѧϰ�ļ����ؼ�Ҫ�أ�
- �������ʱ���Ƶ�**�ϳ�����**�Ͻ��г�ʼ΢����
- ���ڹ�������ʱ���ݼ�����ǿ�� leave-1-out �������ɲ��ԣ�
- ѵ��������ÿ��ʵ������Ӧ����
- ����任�µ�����һ���ԣ�self-consistency��������

���ֲ�ͬ�� TTT �������ɷ�ʽ��
- һ�� in-context learning��ICL����ʽ���Ӹ����Ĳ�����ʾ�д��� leave-1-out ����
- ��һ���Ƕ˵��˸�ʽ����ÿ�� i/o ����Ϊһ������������

ʵ�黷�ڣ��о����ڳ������������Ͽ⣨ARC,�������������Ͽ⣩�ж���Щ����������������ARC ���Ͽ��ռ��˺ܶ༫����ս�Ե� few-shot �Ӿ��������⣬����Ϊ�ǲ��� LM �������޵������׼��Ŀǰ�Ĵ������ģ���� ARC �Ͼ����ֲ��ѡ�

TTT ����������� LM �� ARC �ϵ����� ���� �� 1B ģ���Ͻ�׼ȷ����ߵ�ԭ���� 6 ����ʹ�� 8B ģ��ʱҲ���������ѷ����� SOTA ����ģ�ͷ�����

��2024-11-12��[��OpenAI���Ʋ���Scaling Law�ˣ�MIT�ѡ�����ʱѵ����ϵͳ�о���һ�飬���ֻ���·](https://www.jiqizhixin.com/articles/2024-11-12-7)

OpenAI ��һ���콢ģ�͵������������Ȳ���ǰ�����콢ģ��֮���������������Ϊ�������ı����������ݵĹ�Ӧ�����ڼ��٣�ԭ���� Scaling Law���ø��������ѵ�������ģ�ͣ���������Ϊ�̡����⣬OpenAI �о��� Noam Brown ָ�������Ƚ���ģ�Ϳ����ھ�����Ҳ�����п����ԣ���Ϊ������ǧ��������������Ԫѵ������ģ�ͻ����ӯ����

��Ԥѵ��������Scaling Law ���ܻ�Ż���

���й������ Scaling Law ��δ������ھ�OpenAI o1 �ķ�����֤������һ�㡣���Ӻ�ѵ���׶����֣�����**ǿ��ѧϰ**��ԭ����**˼ά��**�͸�����**����ʱ��**���Ѵ�ģ����������ǰ����һ����
- ���ַ�ʽ����Ϊ��`����ʱ����`������ط�������**˼ά����ʾ**��**����ͶƱ����**��self-consistency����**����ִ��**��**����**�ȡ�

���и��¸��� ���� `����ʱѵ��`�� Test-Time Training ��TTT�������߶���ͼ�ڲ��ԣ������׶�ͨ����ͬ���ֶ�������ģ�͵����ܣ��� `TTT` ����ݲ���ʱ���룬ͨ��**��ʽ�ݶ�**�������ģ�͡�

���ַ�����ͬ�ڱ�׼΢������Ϊ�����������͵Ļ��������е� ���� ͨ����ͨ������������޼ලĿ�꣬��Ӧ����һ�������� in-context ��עʾ�����мලĿ�ꡣ


���վ��: [transformer ר��](transformer#ttt)

#### Yan

- RockAI �Ƴ� Yan ģ�ͣ�����transformer�ܹ�, ̽������˼·

�Ľ���
- (1) transformer ���� MCSD
  - ���� [MCSD: An Ef?cient Language Model with Diverse Fusion](https://arxiv.org/pdf/2406.12230)
- (2) �ֲ�ģ̬����
  - transformer�ܹ�: �� 1+1=?, �ἤ�����в���, ��������̫��, ���Բ�������
  - ���Ի���: ���԰���˵���ȹ��ܷ���, �������񼤻��Ӧ������������������״̬, �������ĺܵ�, ��20w, �൱�ڵ���� 

����ˮƽ�ӽ�������transformer���������ܳ�Խ
- 3b ģ��, ��С5G���Ż����ڴ�ռ�ý�1G
- �˲��豸�����У����ܳ��� transformer 30% ����

����
- ����жϼ����ĸ�����? **������Ԫѡ���㷨**, һ��������С��������, ����ѵ���Ľ���,�����ѡ������������ѡ��
- ѵ������ʲô����? 

`Yan 1.3`: Ⱥ�����ܵ�Ԫ��ģ��
- ѵ��Ч������7������������������5����������������3��
- �뼶Ӱ�졢��transformer�ṹ���˵��˶�ģ̬������󲿷ֶ˲��豸
  - ���������ֻ�cpu������LLM�Ĺ�˾������3��

���ڴ�ģ��ѵ������ʶ��ѵ��һ��ģ�ͣ����ѵļ�����Դ̫�࣬�е�����Ҫ�����˵�վѵ����

��Ƶ����
- [վ�����ˣ��������AI��˾���¼�����սChatGPTȨ��](https://www.bilibili.com/video/BV19LCUYuEKP/?spm_id_from=333.999.0.0&vd_source=ec1c777505e146eb20d947449d6bba6e) RockAI�����޼�˼


<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=113328533868595&bvid=BV19LCUYuEKP&cid=26349866723&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

OpenAI GPT ��attention·�����������Ψһ��·��

�Ľ�
- ������
  - �ı�ģ̬���������ܱ���80-90%��Ч������ͼ����Ƶ������»�
  - ������Ȩ�ع̶����޷���ѧϰ

���ڴ�ģ�ͻ���
- ��������: ��������Ļ��ᣬ����������
  - deepseek �Ƴ� MLA/O1����
  - RockAI(��ɽ�Ƽ�) Ŀ�꣺��attention�õ�; ���������ֻ������е�LLM������3��, Yan ģ�ͽ���˲�������Դ�����������
  - ���ڱĳ���һ��LLM��ԭ���� Llama ��Դ�ˡ�����META �ƻ���Դ
  - �˲�Ҫ��: ��ѧ+�㷨��ǿ����Ը��������
- Ӧ�ô���
  - ������Ӧ�ú�ǿ
  - �˲�Ҫ�󣺽���ѧ�Ʊ������� ��ҽѧ+AI


`������`
- ֻ�м�������Ԫ�������������ǳ�ǿ��������ܼ�ʻ��������
- ���������������û������ЧӦ��
���������������������ЧӦ����ô���Լ���Ч�ʿ϶��Ǹ�Ч�ģ�������ҪͶ��������������еĲο���

������
- �����Ƽ�����Դ����������ҵ����Ҫ5�����

### ͼ��

�ܽ�LLM���׶��Ż�����

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-06-22T15:10:12.254Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;V_7K2ib4bP-NWsyXjMxV\&quot; version=\&quot;21.5.0\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;�� 1 ҳ\&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;795\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-35\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f9f7ed;strokeColor=#36393d;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;90\&quot; y=\&quot;300\&quot; width=\&quot;180\&quot; height=\&quot;360\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wGYBfAiltT4hGnPjrrAm-8\&quot; value=\&quot;LLM�Ľ�����\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=19;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;242\&quot; y=\&quot;70\&quot; width=\&quot;216\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; value=\&quot;����\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;118\&quot; y=\&quot;180\&quot; width=\&quot;110\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; value=\&quot;ѵ��\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;570\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-6\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; target=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;240\&quot; y=\&quot;275\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;410\&quot; y=\&quot;410\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-15\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; target=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;250\&quot; y=\&quot;600\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; value=\&quot;����\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;590\&quot; y=\&quot;535\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-12\&quot; value=\&quot;���ݼ����ռ�����\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-13\&quot; value=\&quot;����������\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-14\&quot; value=\&quot;Ӳ����Դ����\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-22\&quot; value=\&quot;�Ľ�&amp;lt;br&amp;gt;�� ���ʡ��ַ�&amp;lt;br&amp;gt;�ڽ����OOV����\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;190\&quot; y=\&quot;450\&quot; width=\&quot;120\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-42\&quot; value=\&quot;2023-6-22&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;120\&quot; y=\&quot;1210\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; value=\&quot;Ч��\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;910\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-3\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-2\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;283\&quot; y=\&quot;500\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;280\&quot; y=\&quot;790\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-5\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-4\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;240\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;490\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; value=\&quot;ģ��\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;340\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-7\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-6\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;620\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;780\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; value=\&quot;����\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;740\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-8\&quot; value=\&quot;����\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540\&quot; y=\&quot;860\&quot; width=\&quot;230\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-37\&quot; value=\&quot;LLM����\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-9\&quot; value=\&quot;֪ʶ׼ȷ�ԣ��þ�����˵�˵�\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-10\&quot; value=\&quot;������������\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-11\&quot; value=\&quot;����ƫ�ö��룺RLHF����\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-12\&quot; value=\&quot;Ӧ��\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;1110\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-13\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-12\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;167\&quot; y=\&quot;630\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;90\&quot; y=\&quot;750\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-14\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;460\&quot; y=\&quot;960\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;510\&quot; y=\&quot;935\&quot; /&gt;\n              &lt;mxPoint x=\&quot;510\&quot; y=\&quot;935\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-15\&quot; value=\&quot;�������\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;708\&quot; width=\&quot;140\&quot; height=\&quot;180\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-16\&quot; value=\&quot;С�ͻ�\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-17\&quot; value=\&quot;���ز���\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-18\&quot; value=\&quot;���ܣ�ʱ�ӡ�����\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-20\&quot; value=\&quot;���ݰ�ȫ\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-38\&quot; value=\&quot;���롢�������\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;150\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-19\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=-0.021;entryY=0.9;entryDx=0;entryDy=0;entryPerimeter=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-16\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;605\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-21\&quot; value=\&quot;��̬ϵͳ\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380\&quot; y=\&quot;1060\&quot; width=\&quot;140\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle x=\&quot;550\&quot; y=\&quot;1040\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-22\&quot; value=\&quot;����\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-23\&quot; value=\&quot;����г�\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-24\&quot; value=\&quot;����Ӧ��\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-25\&quot; value=\&quot;LLM��ܣ�LangChain\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-26\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-12\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-23\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;775\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;367\&quot; y=\&quot;775\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-27\&quot; value=\&quot;���ݼ�\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;560\&quot; y=\&quot;145\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-28\&quot; value=\&quot;Ԥѵ�����ݼ�����Ӣ��\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-29\&quot; value=\&quot;ָ�\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-30\&quot; value=\&quot;prompt���ݼ�\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-31\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;entryX=-0.014;entryY=0.933;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-28\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;605\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-32\&quot; value=\&quot;ģ���Ż�\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;400\&quot; y=\&quot;305\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-33\&quot; value=\&quot;������ģ�ͣ�����\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-34\&quot; value=\&quot;����ģ��\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-35\&quot; value=\&quot;RL�����Ż�\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-36\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;entryX=-0.007;entryY=0.067;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-34\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;238\&quot; y=\&quot;215\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;408\&quot; y=\&quot;214\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



# ����