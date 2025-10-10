---
layout: post
title:  大模型端侧部署工具
date:   2024-11-30 22:46:00
categories: 大模型
tags:  ollama llm 量化 web lm_studio
excerpt: 大模型LLM部署工具，如 Ollama
mathjax: true
permalink: /llm_end_tool
---

* content
{:toc}



# 本地 LLM 部署工具

两个使用场景
- 离线状态下进行大模型应用开发调试
- 开发一些不依赖于网络的本地化大模型应用。

## 大模型服务平台


### huggingface

详见站内: [huggingface](huggingface)


### 魔搭

阿里云魔搭社区（modelscope)


### MindSpore

华为昇思

### 硅基流动

清华主导的大模型服务平台 [硅基流动](https://cloud.siliconflow.cn/)

一站式云服务平台，SiliconCloud 为开发者提供更快、更便宜、更全面、体验更丝滑的模型API。
- SiliconCloud已上架包括Qwen2.5-72B、DeepSeek-V2.5、Qwen2、InternLM2.5-20B-Chat、BCE、BGE、SenseVoice-Small、Llama-3.1、FLUX.1、DeepSeek-Coder-V2、SD3 Medium、GLM-4-9B-Chat、InstantID在内的多种开源大语言模型、图片生成模型、代码生成模型、向量与重排序模型以及多模态大模型。
- 其中，Qwen2.5（7B）、Llama3.1（8B）等多个大模型API免费使用，让开发者与产品经理无需担心研发阶段和大规模推广所带来的算力成本，实现“Token 自由”。
- 提供开箱即用的大模型推理加速服务，为您的 GenAI 应用带来更高效的用户体验。

【2025-2-6】搭载 华为昇腾版 DeepSeek
- 付费才能使用
- 人脸验证通过支付宝，失败

[DeepSeek部署在云端，1分钟配置完成](https://mp.weixin.qq.com/s/DKwUOk8HuCMzea93PhKwUA)
- 新用户有14元奖励
- 充值需要人脸验证


## 本地部署


【2025-9-11】[2025年全球主流大模型本地部署及高效使用硬件配置指南](https://zhuanlan.zhihu.com/p/1949164887449272936)
- 以下方案信息截至 2025年8月
- GPT、Claude、Gemini、LLaMA、ChatGLM 等全球主流大模型在本地部署或高效使用时，从轻量级到千亿参数级不同规模模型

总结
- （1）个人/轻量级用户
  - 若只需运行 1B~7B 模型（如LLaMA-2-7B），选 `RTX 4080`（16GB）/`RTX 4090`（24GB） + 32GB内存, 即可流畅推理（INT4/FP16量化）。
  - 预算有限可选 `RTX 3060`（12GB）+ INT4量化（性能稍慢但够用）。
- （2）企业/专业用户
  - 7B~13B 模型: 推荐 `RTX 6000 Ada`（48GB）或 `H100` 80GB，搭配 64GB+内存 和 高速NVMe SSD。
  - 13B~70B 模型: 多卡并行（如4×H100）或云服务（避免本地部署成本过高）。

避坑提示
- 显存不足时, 优先尝试 量化（INT4/INT8）（如用 GGUF 工具转换模型），可大幅降低需求。
- 避免仅看 GPU算力（如TFLOPS），**显存容量**（GB）才是大模型运行的硬性瓶颈
- 云服务（如AWS SageMaker、Lambda Labs）是中小企业灵活部署的**首选**方案（按需付费，无需自购硬件）。

### 大模型硬件需求

大模型硬件需求由以下因素决定：
- （1）模型**参数量**（核心）：
  - 参数越多，计算量和显存占用越高（如7B参数模型 vs 70B参数模型）。
- （2）**精度格式**
  - `FP32`（单精度浮点）：计算精度最高，但显存占用大（已基本**淘汰**）。
  - `FP16`（半精度浮点）：平衡精度与效率，**主流**训练/推理使用。
  - `BF16`（脑浮点）：类似`FP16`, 但数值范围更大，适合大模型推理（部分**新显卡**支持）。
  - `INT8`/`INT4`（低精度整数）：显存占用最小，但精度损失大（需量化技术，适合部署而非训练）。
- （3）使用场景
  - `推理`（Inference）：直接生成回答（如聊天机器人），显存需求低于训练，但需**高吞吐和低延迟**。
  - `微调`（Fine-tuning）：基于预训练模型调整参数（如适配特定领域），显存需求接近训练。
  - `预训练`（Pre-training）：从头训练模型（如GPT-3），仅限超算/数据中心级硬件。

注：
- 个人用户通常只需关注 `推理` 或轻量级 `微调`；
- 企业级应用可能涉及大规模分布式训练。

按模型参数量分类的硬件需求
- （一）**超小**模型（<1B参数，如微型聊天机器人）
  - 典型模型：TinyLLaMA（1B）、MiniGPT（0.5B）、Alpaca-1B
  - 用途：极轻量级对话、嵌入式设备（如树莓派）、低资源测试
  - 适用场景：树莓派/旧笔记本部署、极客测试、边缘设备（如智能家居）。
- （二）**小型**模型（1B~7B参数，主流轻量级应用）
  - 典型模型：LLaMA-2-7B、Mistral-7B、ChatGLM2-6B、GPT-J-6B
  - 用途：个人聊天机器人、轻量级办公助手、代码生成（简单需求）
  - 适用场景：个人开发者本地部署LLaMA/Mistral、中小企业客服机器人、代码辅助（如GitHub Copilot替代）。
- （三）**中型**模型（7B~13B参数，高阶应用）
  - 典型模型：LLaMA-2-13B、Mistral-8x7B（MoE）、ChatGLM3-6B（优化版）、GPT-NeoX-12B
  - 用途：专业领域助手（法律/医疗）、复杂代码生成、多轮深度对话
  - 适用场景：企业级智能客服、医疗问诊助手、金融分析工具、科研机构本地实验。
- （四）**大型**模型（13B~70B参数，专业/企业级）
  - 典型模型：LLaMA-2-70B、GPT-3.5（约175B简化版）、Claude-2（100B+）、ChatGLM4-65B
  - 用途：高精度专业咨询（如法律合同审查）、大规模数据分析、通用人工智能原型
  - 硬件需求：
  - 适用场景：国家级AI实验室、科技巨头研发中心、超大规模企业知识库。
- （五）**超大型**模型（>70B参数，如GPT-4级）
  - 典型模型：GPT-4（约1.8万亿参数，实际有效约千亿级）、Gemini Ultra（千亿级）、PaLM-2（540B）
  - 用途:通用人工智能（AGI）原型、国家级AI战略项目、全领域专家系统
  - 硬件需求
  - 适用场景: 仅限全球顶级科技企业（如OpenAI、Google、Meta）或国家AI实验室，个人/中小企业无法触及。
  - 关键说明：
    - GPT-4等模型通过 MoE（混合专家）、低秩适配（LoRA）、分布式训练框架（如Megatron-LM） 降低单卡需求，但仍需 千卡级GPU集群。
    - 普通用户可通过 API调用（如OpenAI ChatGPT、阿里云通义千问）间接使用，无需本地部署。

| 场景                 | 模型规模         | 推荐GPU显存 | CPU核心数 | 内存       | 存储          | 典型配置示例（2025年8月）|
|----------------------|------------------|-------------|-----------|------------|---------------|---------------------------------------------|
| 极轻量级测试         | <1B              | 4~6GB       | 4线程     | 8GB        | 10GB SSD      | 树莓派4B（无GPU）、旧笔记本（CPU推理）、RTX 1650（INT4量化1B模型） |
| 个人开发者/轻办公    | 1B~7B            | 12~16GB     | 8线程     | 16~32GB    | 500GB NVMe SSD| RTX 4080（16GB）、Ryzen 7 7800X + 32GB内存（运行LLaMA-2-7B INT4/FP16） |
| 企业级助手/专业领域  | 7B~13B           | 24~48GB     | 16线程    | 64~128GB   | 1TB NVMe SSD  | RTX 6000 Ada（48GB）、AMD Ryzen 9 7950X3D + 128GB内存（运行Mistral-8x7B FP16） |
| 科研/大规模部署      | 13B~70B          | 8×24GB+     | 64线程    | 512GB~1TB  | 2TB NVMe+冷存储 | 8×H100 24GB（NVLink互联）、EPYC 9654 + 1TB内存（分布式推理70B INT4模型） |
| 超大规模AGI研究      | >70B（GPT-4级）| 数万张GPU   | 数千核    | PB级内存   | PB级存储      | NVIDIA DGX SuperPOD（万卡H100集群）、定制化超算架构（如Google TPU v4 Pod） |


## 总结

当前比较出名的有两个产品`Ollama`和`LMstudio`。
- ollama 问题
  - 强制安装在C盘
  - 终端操作


### Ollama vs LMStudio

【2024-3-10】[Ollama VS LmStudio,谁是本地化模型运行工具最佳](https://mp.weixin.qq.com/s/VUoUaXd3TJpSC0fQYTY0lw)

选择 `Ollama` 和 `LM Studio` 时，应根据专业技能、预算和具体需求来判断。
- 对于**开发者**：Ollama 开放源代码的特性、效率高和可定制化性使其成为尝试和微调创意的理想选项。
- 对于**初学者**和**普通用户**：LM Studio 的用户友好界面、预训练模型和多样的功能提供了一个基础起点，适合进行创意性探索和多样化文本生成。


Ollama
- 优势
  - 提供了一系列广泛的预训练模型：由于模型种类和构架的多样性，用户能根据其需求挑选到最合适的模型。
  - 灵活的微调选择：用户可以利用自定义数据集对预训练模型进行微调，使其更适合特定的任务和领域，加快原型的研制和实验。
  - 便捷的协作功能：Ollama 支持团队成员之间合作，能够无缝地共享模型、数据集和实验成果。
- 劣势
  - 定制选项有限：虽有多个预训练模型可供选择，但用户可能会在模型架构或训练模式的个性化上有所局限。
  - 成本问题：根据使用量和资源需求的不同，使用 Ollama 的成本也会出现变化，因此在价格上需要精心评估以保证性价比。
- 适用场景
  - 适合习惯使用命令行界面的开发者和技术熟练者的理想选择，是探索不同大型语言模型和微调特殊任务模型的完美工具。

LMstudio
- 优势
  - 先进的模型训练功能：它允许广泛定制模型训练，包括支持分布式训练、调整超参数以及模型优化，使用户能够获得行业领先水平的性能。
  - 易扩展和高效表现：LM Studio 设计用来高效地处理大规模模型训练和部署工作，能够利用云基础设施和并行处理技术，加速模型训练和处理速度。
  - 与云服务的无缝整合：LM Studio 可以轻松地与各种云服务和平台整合，让用户在模型的开发和部署上拥有更多资源和功能。
- 劣势
  - 完全掌握较难：因为拥有大量高级功能和强大能力，虽然上手容易，但要完全精通很难。
  - 资源要求高：在 LM Studio 构建和训练复杂模型可能需要颇多的计算资源和专业技能，对于难以获得高性能计算设备的用户来说可能是一个障碍。
- 适用场景
  - 对包括非技术用户在内的所有人使用都更为简单，提供了一个可视化界面帮助管理模型、任务和结果输出。特别适用于创意写作、生成不同文本格式和探索模型的多元特性。


## LM Studio

[LM Studio](https://lmstudio.ai/) 一款低门槛产品，整个模型运行管理都**界面化**操作。
- 相较于 ollama，LMStudio 定位是一个功能全面的**闭源**平台
- 拥有一系列强大的特性和简单易用的操作界面，提供了一套完整的工具组合，用于训练、评估和部署模型，既适合科研也适合实际应用环境。

适合大部分人，特别是初学者或者非技术人员使用。


### 安装

[LM Studio](https://lmstudio.ai/) 官网下载 Windows 版本

#### 终端服务

终端启动服务

```sh
lms server start
```

#### api 


本地主机上运行的API服务器访问`LM Studio`中的LLM。

请求和响应格式均遵循OpenAI的API标准。要使用本地服务器，用户需首先安装LM Studio，然后从应用程序中搜索并下载所需的LLM模型。

【2025-8-18】本地客户端开启
- 左侧“终端”图标 → Status 开启
- 关闭思考模式：右侧 Inference → Enable Thinking

支持的端点
- GET /v1/models
- POST /v1/chat/completions
- POST /v1/embeddings
- POST /v1/completions

其中，POST /v1/embeddings是LM Studio 0.2.19中的新功能。

Python调用

```py
import requests
import json

def requestLLM_local(question):
    """
        请求 LLM
        输入: quesiton 输出：reply
    """
    if not question:
        return '问题为空'
    url = 'http://127.0.0.1:1234/v1/chat/completions'
    data_info = {
        "model": "qwen/qwen3-1.7b",
        "messages":[
            {
                "role": "user",
                "content": "你是谁？"
            }
        ],
        "max_tokens": 520,
        "temperature": 0.3,
        "top_k": 50,
        "top_p": 0.8,
        "repetition_penalty": 1.2,
        "stream": False,
        "chat_template_kwargs": {"enable_thinking": False}
    }
    data_info['messages'][0]['content'] = question
    r = requests.post(url, json=data_info)
    reply = r.text
    try:
        res = json.loads(r.text)
        reply =  res['choices'][0]['message']['content']
    except Exception as err:
        print(f'json解析有误: [{r.text}]')

    return reply

question = '怎么还没来'
res = requestLLM_local(question)
print(res)
```

示例

```sh
# 检查当前加载的模型
curl http://localhost:1234/v1/models

# 本地服务器上发起推断请求，需使用OpenAI的“Chat Completions”格式。
curl http://localhost:1234/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{ 
  "messages": [
    { "role": "system", "content": "You are a helpful coding assistant." },
    { "role": "user", "content": "How do I init and update a git submodule?" }
  ],
  "temperature": 0.7,
  "max_tokens": -1,
  "stream": true
}'

```

文本嵌入

```sh
curl http://localhost:1234/v1/embeddings \
-H "Content-Type: application/json" \
-d '{
    "input": "Your text string goes here",
  "model": "model-identifier-here"
}'
```

#### 问题:国内受限

问题:
- 国内模型下载受限

解决
- `huggingface.co` -> `hf-mirror.com`
- 找到两个文件，路径如下：(这两个文件较大,10+m, sublime text打开受阻，改用 vs code)
  - `\resources\app\.webpack\main\index.js`
  - `\resources\app\.webpack\renderer\main_window.js`
- 批量替换: 将两文件内的`huggingface.co`替换为`hf-mirror.com`, 以vscode为例：
  - ctrl+shift+h 调出批量替换（若同时打开两文件，可同时替换）
  - ctrl+alt+enter 应用替换

#### 问题:文件无法保存

【2025-2-6】实践问题: 文件无法保存

win10 修改文件读写权限（管理员权限）
- 右键 -> 属性 -> `安全` -> `编辑`
- 找到你的用户
- 在下方修改此用户对该文件的读写权限

参考
- [无法修改后无法保存](https://blog.csdn.net/Gu_fCSDN/article/details/104327423)
- 原文链接：https://blog.csdn.net/qq_45361790/article/details/145384771

### 功能

LM Studio 核心功能包括
- 发现、下载和运行本地LLMs。用户可以通过直观的图形界面轻松下载并加载各种模型。其广泛支持的模型库包括HuggingFace上的ggml Llama、MPT和StarCoder模型（如Llama 2、Orca、Vicuna等）。



## Ollama

Ollama 是一个强大的框架，设计用于在 Docker 容器中部署 LLM。
- [参考](https://juejin.cn/post/7312404619519361050)
- [Ollama完整教程：本地LLM管理、WebUI对话、Python/Java客户端API应用](https://www.cnblogs.com/obullxl/p/18295202/NTopic2024071001)

### Ollama 介绍

[Ollama](ollama.ai) 主要功能
- Docker 容器内部署和管理 LLM 的促进者，过程更简单。
- 帮助用户快速在本地运行大模型，通过简单安装指令，执行一条命令就在本地运行开源大型语言模型，例如 Llama 2。

Ollama 将模型权重、配置和数据捆绑到一个包中，定义成 Modelfile。优化了设置和配置细节，包括 GPU 使用情况。

项目特点
- **开源**：很显然这是首要特点，开源推动者项目的持续发展
- **开箱即用**：一条命令的方式，简化了大量的工作，降低了门槛。
- **可扩展**：可以和很多工具进行集成使用，有更多的玩法
- **轻量化**：不需要太多的资源，Mac就能跑

【2023-12-5】[Ollama 下载](https://ollama.ai/download), [GitHub](https://github.com/jmorganca/ollama)

Get up and running with Llama 2 and other large language models locally
- Model 集合: [library](https://ollama.ai/library)
- 提供 REST API 
- 可定制自己的模型

运行资源说明：
- 3B 模型需要 8G 内存
- 7B 模型需要 16G 内存
- 13B 模型需要 32G 内存

除了简单启动模型外，Ollama 还可以编写 Modelfile 来导入更多的自定义模型。

Ollama 具备灵活的扩展性，它支持和很多工具集成，除了命令行的使用方式，可以通过配合UI界面，简单快速的打造一个类ChatGPT应用。

### 安装 ollama

ollama 极大简化了安装过程，并提供了多种选择。
- 支持的平台包括：Mac/Linux/Windows，并提供了docker 镜像。

Linux

```sh
# Mac 
https://ollama.ai/download
# Linux 环境
curl -fsSL https://ollama.com/install.sh | sh # linux 下载
```

常用的系统环境变量：
- `OLLAMA_MODELS`：模型文件**存放目录**，默认目录为当前用户目录
  - Windows 目录：`C:\Users\.ollama\models`
  - MacOS 目录：`~/.ollama/models`
  - Linux 目录：`/usr/share/ollama/.ollama/models`
  - 如是 Windows 系统建议修改（如：`D:\OllamaModels`），避免 C 盘空间吃紧
- `OLLAMA_HOST`：Ollama 服务监听的**网络地址**，默认为 `127.0.0.1`，如果允许其他电脑访问 Ollama（如：局域网中的其他电脑），建议设置成 0.0.0.0，从而允许其他网络访问
- `OLLAMA_PORT`：Ollama 服务监听的默认端口，默认为`11434`，如果端口有冲突，可以修改设置成其他端口（如：8080等）
- `OLLAMA_ORIGINS`：HTTP 客户端请求来源，半角逗号分隔列表，若本地使用无严格要求，可以设置成星号，代表不受限制
- `OLLAMA_KEEP_ALIVE`：大模型加载到内存中后的**存活时间**，默认为5m即 5 分钟（如：纯数字如 300 代表 300 秒，0 代表处理请求响应后立即卸载模型，任何负数则表示一直存活）；我们可设置成24h，即模型在内存中保持 24 小时，提高访问速度
- `OLLAMA_NUM_PARALLEL`：请求处理**并发数量**，默认为1，即单并发串行处理请求，可根据实际情况进行调整
- `OLLAMA_MAX_QUEUE`：请求**队列长度**，默认值为512，可以根据情况设置，超过队列长度请求被抛弃
- `OLLAMA_DEBUG`：输出 Debug 日志标识，应用研发阶段可以设置成1，即输出详细日志信息，便于排查问题
- `OLLAMA_MAX_LOADED_MODELS`：最多同时加载到内存中**模型数量**，默认为1，即只能有 1 个模型在内存中


### ollama 使用

[模型库](https://ollama.org.cn/library)

Ollama 导入模型到本地的三种方式：
- 直接从 Ollama 远程仓库拉取 ———— 直接从远程下载模型，**最推荐、最常用**
- 通过 `GGUF` 模型权重文件导入到本地 ———— 已下载过，避免重复，直接导入GGUF文件，**不推荐、不常用**
- 通过 `safetensors` 模型权限文件导入到本地 ———— 已下载过，避免重复，直接导入GGUF文件，**不推荐、不常用**

执行

```sh
# 查看已有模型
ollama list
# NAME            ID              SIZE    MODIFIED
# gemma2:9b       c19987e1e6e2    5.4 GB  7 days ago
# qwen2:7b        e0d4e1163c58    4.4 GB  10 days ago

# 查看本地运行中模型列表：
ollama ps
# NAME            ID              SIZE    PROCESSOR       UNTIL
# qwen2:0.5b      6f48b936a09f    693 MB  100% CPU        4 minutes from now

# 下载模型：若本地不存在，直接下载；若存在，则增量更新
# 模型名称格式为：模型名称:参数规格；
ollama pull qwen2:0.5b # 从 Ollama 仓库下载qwen2大模型的0.5b参数规格大模型文件到本地磁盘
ollama pull glm4:9b # Ollama 最低版本为0.2.0才能支持GLM4
# 启用 llama 2
ollama run llama2 # 下载并运行；自动去pull Llama2 模型，并运行
ollama run mistral --verbose # mistral
ollama run qwen2 # 下载qwen2 latest 标记模型
ollama run qwen2:0.5b
ollama cp qwen2:0.5b Qwen2-0.5B # 复制本地llm
ollama rm gemma2:9b # 删除模型
# 将Ollama作为服务，在 macOS 中:
OLLAMA_HOST=0.0.0.0:11434 ollama serve
# 启动ollama后台服务 执行命令
ollama serve # 在本机11434端口，启动ollama的http服务
```

Ollama安装成功以后，就建立了11434端口

### api

Ollama 默认提供了 generate 和 chat 这 2 个原始的 API 接口

Dify 中 安装 ollama 
- 模型名称：qwen3:30b-a3b
- 基础 URL：http://172.35.xx.xx:11434
- 模型类型：对话
- 模型上下文长度：32768
- 最大 token 上限：32768

使用方式如下：

generate接口使用样例：

```sh
curl http://localhost:11434/api/generate -d '{"model": "mistral"}'

curl http://localhost:11434/api/generate -d "{
  'model': 'qwen:0.5b',
  'prompt': '为什么天空是蓝色的？'
}"
```

chat接口的使用样例：

```sh
curl http://localhost:11434/api/chat -d '{"model": "mistral"}'

curl http://localhost:11434/api/chat -d '{
  "model": "qwen:7b",
  "messages": [
    { "role": "user", "content": "为什么天空是蓝色的？" }
  ]
}'
```

编程语言调用

Python 依赖包：

```sh
pip install ollama
```

第二步，使用 Ollama 接口，stream=True 代表按照流式输出：

```py
import ollama
 
# 流式输出
def api_generate(text:str):
  print(f'提问：{text}')
 
  stream = ollama.generate(
    stream=True,
    model='qwen:7b',
    prompt=text,
    )
 
  print('-----------------------------------------')
  for chunk in stream:
    if not chunk['done']:
      print(chunk['response'], end='', flush=True)
    else:
      print('\n')
      print('-----------------------------------------')
      print(f'总耗时：{chunk['total_duration']}')
      print('-----------------------------------------')
 
 
if __name__ == '__main__':
  # 流式输出
  api_generate(text='天空为什么是蓝色的？')
 
  # 非流式输出
  content = ollama.generate(model='qwen:0.5b', prompt='天空为什么是蓝色的？')
  print(content)
```

### UI

方案
- open-webui
- chatbox

#### Open-WebUI

[open webui程序官网](https://openwebui.com/)
- Open WebUI 是一个可扩展、功能丰富且用户友好的**自托管** WebUI，旨在完全离线操作。
- 支持各种 LLM 运行程序，包括 Ollama 和 OpenAI 兼容的 API。
- 还可以通过 AUTOMATIC1111 和 ComfyUI 的API来整合稳定扩散模型，实现LLM指导SD来生成图片

特点?
- 直观的界面：我们的聊天界面从 ChatGPT 中汲取灵感，确保用户友好的体验。
- 响应式设计：在桌面和移动设备上享受无缝体验。
- 快速响应：享受快速响应的性能。
- 轻松设置：使用 Docker 或 Kubernetes（kubectl、kustomize 或 helm）无缝安装，以获得无忧体验。
- 主题定制：从各种主题中进行选择，个性化您的 Open WebUI 体验。
- 代码语法突出显示：通过我们的语法突出显示功能增强代码的可读性。
- 完整的 Markdown 和 LaTeX 支持：通过全面的 Markdown 和 LaTeX 功能来丰富交互，提升您的 LLM 体验。
- 本地 RAG 集成：通过突破性的检索增强生成 (RAG) 支持深入了解聊天交互的未来。此功能将文档交互无缝集成到您的聊天体验中。您可以将文档直接加载到聊天中或将文件添加到文档库中，使用#提示中的命令轻松访问它们。在 alpha 阶段，当我们积极完善和增强此功能以确保最佳性能和可靠性时，可能会偶尔出现问题。
- RAG 嵌入支持：直接在文档设置中更改 RAG 嵌入模型，增强文档处理。此功能支持 Ollama 和 OpenAI 模型。
- 网页浏览功能#：使用URL 后的命令将网站无缝集成到您的聊天体验中。此功能允许您将网络内容直接合并到您的对话中，从而增强交互的丰富性和深度。
- 提示预设支持/：使用聊天输入中的命令立即访问预设提示。轻松加载预定义的对话开头并加快您的互动。通过Open WebUI Community集成轻松导入提示。
- RLHF 注释：通过对消息进行“赞成”和“反对”评级来增强您的消息，然后选择提供文本反馈，从而促进根据人类反馈 (RLHF) 创建强化学习数据集。利用您的消息来训练或微调模型，同时确保本地保存数据的机密性。
- 对话标记：轻松分类和定位特定聊天，以便快速参考和简化数据收集。
- 下载/删除模型：直接从 Web UI 轻松下载或删除模型。
- 更新所有 Ollama 模型：使用方便的按钮一次轻松更新本地安装的模型，简化模型管理。
- GGUF 文件模型创建：通过直接从 Web UI 上传 GGUF 文件，轻松创建 Ollama 模型。简化的流程，可选择从您的计算机上传或从 Hugging Face 下载 GGUF 文件。
- 多模型支持：不同聊天模型之间无缝切换，实现多样化交互。
- 多模式支持：与支持多模式交互的模型无缝交互，包括图像（例如 LLava）。
- 模型文件生成器：通过 Web UI 轻松创建 Ollama 模型文件。通过开放 WebUI 社区集成轻松创建和添加角色/代理、自定义聊天元素以及导入模型文件。
- 多个模特对话：轻松地同时与多个模特互动，利用他们的独特优势来获得最佳响应。通过并行利用一组不同的模型来增强您的体验。
- 协作聊天：通过无缝编排群组对话来利用多个模型的集体智慧。使用@命令指定模型，在聊天界面中启用动态且多样化的对话。让自己沉浸在聊天环境中的集体智慧中。
- 本地聊天共享：在用户之间无缝生成和共享聊天链接，增强协作和沟通。
- 再生历史访问：轻松重新访问和探索您的整个再生历史。
- 聊天历史记录：轻松访问和管理您的对话历史记录。
- 存档聊天：轻松存储与法学硕士的完整对话以供将来参考，保持聊天界面整洁有序，同时方便检索和参考。
- 导入/导出聊天历史记录：将您的聊天数据无缝移入和移出平台。
- 语音输入支持：通过语音交互与您的模型互动；享受直接与模特交谈的便利。此外，探索在 3 秒静音后自动发送语音输入的选项，以获得简化的体验。
- 可配置的文本转语音端点：使用可配置的 OpenAI 端点自定义您的文本转语音体验。
- 使用高级参数进行微调控制：通过调整温度等参数和定义系统提示来获得更深层次的控制，以根据您的特定偏好和需求定制对话。
- 图像生成集成：使用 AUTOMATIC1111 API（本地）、ComfyUI（本地）和 DALL-E 等选项无缝集成图像生成功能，通过动态视觉内容丰富您的聊天体验。
-  OpenAI API 集成：轻松集成 OpenAI 兼容 API，与 Ollama 模型进行多功能对话。自定义 API 基本 URL 以链接到LMStudio、Mistral、OpenRouter 等。
- 多种 OpenAI 兼容 API 支持：无缝集成和定制各种 OpenAI 兼容 API，增强聊天交互的多功能性。
-  API 密钥生成支持：生成密钥以利用 Open WebUI 和 OpenAI 库，简化集成和开发。
- 外部 Ollama 服务器连接：通过配置环境变量无缝链接到托管在不同地址上的外部 Ollama 服务器。
- 多个 Ollama 实例负载平衡：轻松地在多个 Ollama 实例之间分配聊天请求，以增强性能和可靠性。
- 多用户管理：通过我们直观的管理面板轻松监督和管理用户，简化用户管理流程。
-  Webhook 集成：通过 webhook 订阅新用户注册事件（兼容 Google Chat 和 Microsoft Teams），提供实时通知和自动化功能。
- 模型白名单：管理员可以将具有“用户”角色的用户的模型列入白名单，从而增强安全性和访问控制。
- 可信电子邮件身份验证：使用可信电子邮件标头进行身份验证，添加额外的安全和身份验证层。
- 基于角色的访问控制（RBAC）：通过受限的权限确保安全访问；只有经过授权的个人才能访问您的 Ollama，并且为管理员保留专有的模型创建/拉取权限。
- 后端反向代理支持：通过 Open WebUI 后端和 Ollama 之间的直接通信增强安全性。这一关键功能消除了通过 LAN 公开 Ollama 的需要。从 Web UI 向“/ollama/api”路由发出的请求会从后端无缝重定向到 Ollama，从而增强整体系统安全性。
- 多语言支持：借助我们的国际化 (i18n) 支持，以您喜欢的语言体验开放式 WebUI。加入我们，扩展我们支持的语言！我们正在积极寻找贡献者！
- 持续更新：我们致力于通过定期更新和新功能来改进 Open WebUI。


启动 run 模式后，终端命令

```sh
/clear # 清除对话上下文信息
/bye # 退出对话窗口
/set parameter num_ctx 4096 # 可设置窗口大小为 4096 个 Token，也可以通过请求设置，如：curl <http://localhost:11434/api/generate> -d '{ "model": "qwen2:7b", "prompt": "Why is the sky blue?", "options": { "num_ctx": 4096 }}'
/show info # 查看当前模型详情
```

llama 自带控制台对话界面体验总归是不太好，部署 Web 可视化聊天界面：


##### 源码安装


- 下载并安装 [Node.js](https://nodejs.org/zh-cn) 工具
- 下载 ollama-webui 工程代码：`git clone https://github.com/ollama-webui/ollama-webui-lite ollama-webui`
- 切换 ollama-webui 代码目录：`cd ollama-webui`
- 设置 Node.js 工具包镜像源（下载提速）：`npm config set registry http://mirrors.cloud.tencent.com/npm/`
- 安装 Node.js 依赖的工具包：`npm install`
- 最后，启动 Web 可视化界面：`npm run dev`

浏览器打开 Web 可视化界面：http://localhost:3000/
- web settings 中填入合适的端口, 如 http://localhost:11434/api


##### pip 安装

注意
- windows 10下，Python 版本必须是 3.11, 否则无法执行 pip install命令
- Python [3.11 下载地址](https://www.python.org/downloads/release/python-3110/)
- 安装文件，右键“以管理员方式运行”，否则会出现权限问题

```sh
pip install open-webui
```


### 模型量化

[模型量化](https://zhuanlan.zhihu.com/p/704951717) 

ollama 模型转换，量化
- 采用哪种量化方式？[hf量化计算器](https://hf-accelerate-model-memory-usage.hf.space/)

### ollama 推理性能

总结
- 7b 多并发情况下, 流畅运行，72b 非常勉强

纯CPU运行详情
- 1 qwen2:7b，并发数为1时，生成速度可达 18 token/s，并发数为4时，总吞吐量可达47 token/s
- 2 qwen2:72b，并发数为1时，生成速度可达 2.3 token/s，并发数为4时，总吞吐量可达6 token/s
参考 [知乎](https://zhuanlan.zhihu.com/p/716897033)

|模型|并发1时推理速度(token/s)|并发4时推理速度(token/s)|分析|
|---|---|---|---|
|qwen2:7b|18|47|4个并发时流畅运行|
|qwen2:72b|2.3|6|非常勉强|
|||||


### RAG

ollama rag方案
- [知乎](https://zhuanlan.zhihu.com/p/699837647)



## 国产



### CherryStudio

[CherryStudio](https://cherry-ai.com/) 是一个支持多平台的AI客户端，支持 Win、macOS、Linux平台,未来也会支持移动端。
- 集成了超过 300 多个大语言模型

项目自24年7月至今已迭代数百个版本

### MMN

阿里发布 [MMN](www.mnn.zone/)
- 一个高效、轻量的深度学习框架，专注于在端侧设备（手机、嵌入式设备）上实现高性能的模型推理与训练，让大模型也能在各类设备中都能高效运行。
- GitHub [MMN](https://github.com/alibaba/MNN)
- Android APK [MMN](https://github.com/alibaba/MNN/blob/master/apps/Android/MnnLlmChat/README_CN.md)
- ![](https://github.com/alibaba/MNN/raw/master/apps/Android/MnnLlmChat/assets/image_image_new.jpg)

MNN-LLM：基于 MNN 引擎打造的大型语言模型运行时解决方案，能让大语言模型（LLM）更好落地于手机、PC 和物联网等终端设备。

轻量级高性能推理引擎 MMN
- 通用性 - 支持 TensorFlow、Caffe、ONNX 等主流模型格式，支持CNN、RNN、GAN等常用网络。
- 高性能 - 极致优化算子性能，全面支持CPU、GPU、NPU，充分发挥设备算力。
- 易用性 - 转换、可视化、调试工具齐全，能方便地部署到移动设备和各种嵌入式设备中。

功能亮点
- 多模态支持： 提供多种任务功能，包括文本生成文本、图像生成文本、音频转文本及文本生成图像（基于扩散模型）。
- CPU推理优化： 在安卓平台上，MNN-LLM展现了卓越的CPU性能，预填充速度相较于llama.cpp提高了8.6倍，相较于fastllm提升了20.5倍，解码速度分别快了2.3倍和8.9倍。下图为 llama.cpp 与 MNN-LLM 与 llama.cpp 的比较。
- 广泛的模型兼容性： 支持多种领先的模型提供商，包括Qwen、Gemma、Llama（涵盖TinyLlama与MobileLLM）、Baichuan、Yi、DeepSeek、InternLM、Phi、ReaderLM和Smolm。
- 本地运行： 完全在设备本地运行，确保数据隐私，无需将信息上传至外部服务器。


#### 部署 QWen


【2025-5-22】[手机也能跑 Qwen3？手把手教你部署](https://mp.weixin.qq.com/s/VSC7Bkcq-w991CodHFIfyw)

全球开源模型冠军 Qwen3、端到端全模态模型 Qwen2.5-Omni，现已成功在手机上跑通！

在 MNN 的支持下，Qwen3 系列模型已适配 Android、iOS 及桌面端，实现低延迟、本地化、高安全的 AI 体验。同时，Qwen2.5-Omni 的语音理解、图像分析等多模态能力也在移动端得到完整释放。



图片
Qwen3：全球领先的开源大语言模型，具备强大的语言理解、逻辑推理、代码生成等能力，是一款“全能型 AI 大脑”。现已开源 0.6B 至 235B 共 8 个尺寸版本，无论是企业级服务器还是手机、手表等小型设备，都能灵活部署、高效运行。

Qwen2.5-Omni：端到端全模态模型，体积小、易部署，支持语音、图像、文本等多种输入方式，真正实现“听懂你说的、看懂你给的、写出你需要的。”

图片


# 结束
