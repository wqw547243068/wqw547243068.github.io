---
layout: post
title:  "LLaMA-Factory 使用指南"
date:   2025-01-10 19:25:00
categories: 大模型
tags: GPU Tensorflow Pytorch 并行计算 分布式 huggingface 阿里云 火山 unsloth llama-factory vllm FSDP
excerpt: 分布式训练知识点
author: 鹤啸九天
mathjax: true
permalink: /llama_factory
---

* content
{:toc}


# LLaMA-Factory 使用指南


北航博士生郑耀威，开发的大模型训练框架
- 2022年开始北航博士学业
- github [hiyouga](https://github.com/hiyouga)
- 【2024-3-20】ACL 2024 论文 [LlamaFactory: Unified Efficient Fine-Tuning of 100+ Language Models](https://arxiv.org/pdf/2403.13372)
- 【2024-7-18】[LLaMA-Factory QuickStart](https://zhuanlan.zhihu.com/p/695287607)
- [官方文档](https://llamafactory.readthedocs.io/zh-cn/latest/index.html)

LLaMA-Factory
- 定位：工业级微调平台
- 核心能力：
  - 企业背书：被Amazon/NVIDIA等公司采用，提供生产级工具链（含Colab集成）
  - 生态整合：支持HuggingFace模型库，内置warp等辅助工具
  - 社区活跃：GitHub高星项目，持续更新
- 推荐场景：
  - 企业需要稳定、可扩展的微调框架
  - 希望快速复现论文方案的团队

## LLaMA-Factory 介绍

[LLaMA Factory](https://www.llamafactory.cn/) 支持多种LLM微调方式，北航博士生推出，包括: **预训练**、**指令监督微调**和**奖励模型**训练等。
- 支持`LoRA`和`QLoRA`微调策略，广泛集成了业界前沿的微调方法。
- 特点: 支持多种LLM模型，提供了**WebUI页面**，使非开发人员也能微调。
- 体验地址：[LLaMA-Board](https://modelscope.cn/studios/hiyouga/LLaMA-Board/summary)
- 可视化界面 [LLaMA-Board](https://huggingface.co/spaces/hiyouga/LLaMA-Board)
- github: [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)，附各阶段训练数据集
- ![](https://pic2.zhimg.com/80/v2-7b24a5941a9bf996cf35187ae351f6c1_1440w.webp)

资源
- 论文: [Unified Efficient Fine-Tuning of 100+ LLMs (ACL 2024)](https://arxiv.org/abs/2403.13372)

功能
- 支持多种模型：LLaMA、LLaVA、Mistral、Mixtral-MoE、Qwen、Qwen2-VL、Yi、Gemma、Baichuan、ChatGLM、Phi 等等。
- 集成方法：（增量）**预训练**、（多模态）**指令监督微调**、**奖励模型训练**、PPO 训练、DPO 训练、KTO 训练、ORPO 训练等等。
- 多种**精度**：16 比特全参数微调、冻结微调、LoRA 微调和基于 AQLM/AWQ/GPTQ/LLM.int8/HQQ/EETQ 的 2/3/4/5/6/8 比特 QLoRA 微调。
- 先进算法：GaLore、BAdam、Adam-mini、DoRA、LongLoRA、LLaMA Pro、Mixture-of-Depths、LoRA+、LoftQ、PiSSA 和 Agent 微调。
- 实用技巧：FlashAttention-2、Unsloth、Liger Kernel、RoPE scaling、NEFTune 和 rsLoRA。
- 实验监控：LlamaBoard、TensorBoard、Wandb、MLflow、SwanLab 等等。
- 极速推理：基于 vLLM 的 OpenAI 风格 API、浏览器界面和命令行接口。

性能指标
- 与 ChatGLM 官方的 P-Tuning 微调相比，LLaMA Factory 的 LoRA 微调提供了 3.7 倍的加速比，同时在广告文案生成任务上取得了更高的 Rouge 分数。
- 结合 4 比特量化技术，LLaMA Factory 的 QLoRA 微调进一步降低了 GPU 显存消耗。

详情参考
- [使用LLaMA Factory对大型语言模型进行微调](https://zhuanlan.zhihu.com/p/684989699)
- 作者北航博士[郑耀威](https://github.com/hiyouga)讲解 [全栈大模型微调框架LLaMA Factory：从预训练到RLHF的高效实现](https://www.bilibili.com/video/BV1Gt421L7dt)

<iframe src="//player.bilibili.com/player.html?aid=1801563508&bvid=BV1Gt421L7dt&cid=1463913844&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="600" width="100%"> </iframe>


## LLaMA-Factory 安装

安装
- [安装说明](https://github.com/hiyouga/LLaMA-Factory/blob/main/README_zh.md#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8)

依赖
- 必备依赖: torch/transformers/datasets/trl/accelerate/peft
- 可选依赖: CUDA/deepspeed/bitsandbytes/vllm/flash-attn

```sh
# ----------------------
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
# ---------------------
# Clone the repository
git clone https://github.com/hiyouga/LLaMA-Factory.git
# Create a virtual environment
conda create -n llama_factory python=3.10
# Activate the virtual environment
conda activate llama_factory
# Install dependencies
cd LLaMA-Factory
pip install -r requirements.txt
```

【2025-1-11】 win 10 上实践

```sh
pip install llamafactory # 一步安装

```

## 模型

### 模型下载

项目支持通过模型名称直接从 huggingface 和 modelscope 下载模型，但不容易对模型文件统一管理，所以建议使用手动下载，然后使用绝对路径控制哪个模型。

以 Meta-Llama-3-8B-Instruct为例

```sh
# huggingface 下载（可能要先提交申请通过）
git clone https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
# modelscope 下载（适合中国大陆网络环境）
git clone https://www.modelscope.cn/LLM-Research/Meta-Llama-3-8B-Instruct.git
# 或者 模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('LLM-Research/Meta-Llama-3-8B-Instruct')
```

注意

```sh
# Hugging Face 模型和数据集下载中遇到问题，可使用魔搭/魔乐社区。
export USE_MODELSCOPE_HUB=1 # Windows 使用 `set USE_MODELSCOPE_HUB=1`
export USE_OPENMIND_HUB=1 # Windows 使用 `set USE_OPENMIND_HUB=1`
```

## 训练模式

支持多种训练方法
- OFT正交微调

| Approach               | Full-tuning | Freeze-tuning | LoRA | QLoRA | OFT  | QOFT |
|------------------------|-------------|---------------|------|-------|------|------|
| Pre-Training           | ✅           | ✅             | ✅    | ✅     | ✅    | ✅    |
| Supervised Fine-Tuning | ✅           | ✅             | ✅    | ✅     | ✅    | ✅    |
| Reward Modeling        | ✅           | ✅             | ✅    | ✅     | ✅    | ✅    |
| PPO Training           | ✅           | ✅             | ✅    | ✅     | ✅    | ✅    |
| DPO Training           | ✅           | ✅             | ✅    | ✅     | ✅    | ✅    |
| KTO Training           | ✅           | ✅             | ✅    | ✅     | ✅    | ✅    |
| ORPO Training          | ✅           | ✅             | ✅    | ✅     | ✅    | ✅    |
| SimPO Training         | ✅           | ✅             | ✅    | ✅     | ✅    | ✅    |


## Web UI

UI 点选操作转化为命令行

浏览器打开图形界面测试模型，可选择 `--share` 开公网链接

```sh
# Web UI 使用
llamafactory-cli webui    # 启动网页端
GRADIO_SERVER_PORT=7862 lmf webui
GRADIO_SERVER_PORT=7862 llamafactory-cli webui # 制定端口，不是默认 7860
GRADIO_SERVER_PORT=8080 CACHE_DIR=$cache_dir lmf webui # 【2026-2-2】制定 cache 目录，huggingface 下载模型不放默认目录 ~/.cache/huggingface

CUDA_VISIBLE_DEVICES=4 llamafactory-cli webui    # 指定第4张显卡使用
CUDA_DEVICE_ORDER='cpu' && llamafactory-cli webui # cpu 上启动web ui
set CUDA_DEVICE_ORDER='cpu';llamafactory-cli webui # windows terminal 命令
llamafactory-cli web --model_name_or_path path_to_model --share
```

其中
- 模型候选集合在源码 LlamaFactory/src/llamafactory/extras/constants.py 中


## CLI 模式

几种使用方法
- ① 命令行直接指定
- ② 在 YAML 配置文件中设置

① 命令行直接指定

```sh
CUDA_VISIBLE_DEVICES=0 python src/train_bash.py \
--stage sft \
--do_train \
--model_name_or_path path_to_llama_model \
--dataset alpaca_gpt4_zh \
--cache_dir /mnt/fast_cache \
--output_dir path_to_sft_checkpoint
```


这样会将模型文件和数据集缓存到 /mnt/fast_cache，而不是默认的 ~/.cache/huggingface。

② 在 YAML 配置文件中设置

```yaml
model_args:
model_name_or_path: path_to_llama_model
cache_dir: /mnt/fast_cache
```

然后运行：

```sh
python src/train_bash.py config.yaml
```

CACHE_DIR 是共享存储路径

```bash
# 三个环境变量指定到共享存储路径。
-e HF_DATASETS_CACHE=${CACHE_DIR}/HF_DATASETS_CACHE \
-e HUGGINGFACE_HUB_CACHE=${CACHE_DIR}/HUGGINGFACE_HUB_CACHE \
-e TRANSFORMERS_CACHE=${CACHE_DIR}/TRANSFORMERS_CACHE \
# 2个训练参数指定到共享存储路径。
--cache_dir ${CACHE_DIR}/cache_dir \
--tokenized_path ${CACHE_DIR}/tokenized_cache \
# 1个训练参数指定共享存储
--data_shared_file_system true \
```

【2026-2-2】实践
- lmf train *** 命令转化为 pytorch 的 torchrun 命令

```sh
# 单机两卡
torchrun --nnodes 1 --node_rank 0 --nproc_per_node 2 --master_addr 127.0.0.1 --master_port 54547 /ofs/ese-llm-ssd/users/wangqiwen/envs/py312/lib/python3.12/site-packages/llamafactory/launcher.py saves/Qwen3-4B-Instruct-2507/lora/train_2026-02-02-20-26-27/training_args.yaml
```

【2026-3-13】官方示例执行报错，以上torchrun命令同样报错

```sh
# 命令
llamafactory-cli train examples/train_lora/qwen3_lora_sft.yaml
# 错误信息
socket.cpp:764] [c10d] The client socket cannot be initialized to connect to [localhost]:54943 (errno: 97 - Address family not supported by protocol)
subprocess.CalledProcessError: Command '['torchrun', '--nnodes', '1', '--node_rank', '0', '--nproc_per_node', '2', '--master_addr', '127.0.0.1', '--master_port', '51789', '/ofs/ese-llm-ssd/users/wangqiwen/code/LlamaFactory/src/llamafactory/launcher.py', 'examples/train_lora/qwen3_lora_sft.yaml']' returned non-zero exit status 1.
# 更正后的命令
CUDA_VISIBLE_DEVICES=0 lmf train examples/train_lora/qwen3_lora_sft.yaml # 改成单机单卡
CUDA_VISIBLE_DEVICES=0,1 lmf train examples/train_lora/qwen3_lora_sft.yaml # 【2026-3-13】注明可用GPU即可
```

原因：
- 当前机器有多张GPU，默认都启用，训练时按照分布式模式启动，而 llamafactory-cli 训练命令里默认单机单卡，导致失败

```sh
# 启动日志显示未开启分布式
[INFO|2026-03-13 16:20:27] llamafactory.hparams.parser:508 >> Process rank: 0, world size: 1, device: cuda:0, distributed training: False, compute dtype: torch.bfloat16
```

解法
- 使用单机单卡模式：指定 CUDA_VISIBLE_DEVICES=0
- 更改命令为单机多卡模式：指定 CUDA_VISIBLE_DEVICES=0,1

注意
- 尽量使用2的次方的卡数，如 2，4，8，否则不符合操作系统的规律，可能问题，如算力分配不均衡，2**n的张量无法拆分进行运算
- 系统盘如果不够的话可以直接清空.cache文件

### LLaMA-Factory 命令

llamafactory-cli 命令行工具接口是 LLaMA-Factory v3 版本引入的新特性，用于简化常用操作（训练、推理、导出等），简称 lmf

命令	说明
- env	显示环境信息（PyTorch、CUDA、transformers 等）
- train	启动模型训练（封装了 src/train_bash.py）
- merge	合并 LoRA 模型权重为 HuggingFace 模型
- cli	启动命令行交互测试
- webui	启动 Web UI 推理界面
- export	导出模型为 GGUF 或 Safetensors
- convert	转换数据格式为标准训练集
- validate	验证数据集格式是否正确
- chat	在命令行中与模型多轮对话
- clean	清理缓存、训练中间结果
- build	构建 tokenizer/config 结构

### 常用命令

主要命令
- llamafactory-cli 可简化为 lmf

```sh
llamafactory-cli version  # 显示版本 lmf version
llamafactory-cli help  # 帮助信息
llamafactory-cli train --help   # 某个命令的详细参数说明 lmf train

llamafactory-cli env # 查看环境
llamafactory-cli build --model_type llama --output_dir ./model # 构建 tokenizer 和 config（高级用法）

llamafactory-cli train --config xxx.yaml # 训练模型
llamafactory-cli train --config ./configs/sft.yaml

llamafactory-cli cli/web/chat # 推理测试
llamafactory-cli cli --model_name_or_path path_to_model # 命令行对话
llamafactory-cli merge  # 合并模型
# 合并 LoRA 模型
llamafactory-cli merge \
  --base_model base_model_path \
  --lora_model lora_adapter_path \
  --output_dir merged_model_path

llamafactory-cli export --format gguf # 导出模型
# 导出为 GGUF（用于 llama.cpp）
llamafactory-cli export \
  --model_name_or_path merged_model_path \
  --format gguf \
  --quantization q4_0 \
  --output_dir ./gguf_model

llamafactory-cli chat --model_name_or_path path_to_model # 多轮对话测试（Chat 模式）
# convert, validate # 数据工具
llamafactory-cli validate --input_file ./data/converted.json # 验证数据格式是否正确
# 数据集格式转换：数据集转换为 Alpaca / ChatML 等格式
llamafactory-cli convert \
  --input_file ./data/raw.json \
  --output_file ./data/converted.json \
  --format alpaca 

llamafactory-cli clean # 清理缓存
```


对 Llama3-8B-Instruct 模型进行 LoRA 微调、推理和合并。

```sh
# 训练
llamafactory-cli train -h # 查看训练参数
# lora 微调
llamafactory-cli train examples/train_lora/llama3_lora_sft.yaml
# 推理
llamafactory-cli chat examples/inference/llama3_lora_sft.yaml
# 合并
llamafactory-cli export examples/merge_lora/llama3_lora_sft.yaml

# 用 vLLM 部署 OpenAI API
API_PORT=8000 llamafactory-cli api examples/inference/llama3_vllm.yaml
```

### 参数

参数解释

|动作参数枚举|参数说明|
|--|--|
|`version` | 显示版本信息|
|`train` | 命令行版本训练|
|`chat` | 命令行版本推理chat|
|`export` |模型合并和导出|
|`api` | 启动API server，供接口调用|
|`eval` | 使用mmmlu等标准数据集做评测|
|`webchat` | 前端版本纯推理的chat页面|
|`webui` | 启动LlamaBoard前端页面，包含可视化训练，预测，chat，模型合并多个子页面|

关键参数
- `model_name_or_path`	参数名称
  - huggingface 或 modelscope 标准定义，如“meta-llama/Meta-Llama-3-8B-Instruct”）
  - 或者是本地下载的**绝对**路径，如 /media/codingma/LLM/llama3/Meta-Llama-3-8B-Instruct
- `template` 模型问答时prompt模板，不同模型不同，请[参考](https://github.com/hiyouga/LLaMA-Factory?tab=readme-ov-file#supported-models) 获取不同模型的模板定义，否则会回答结果会很奇怪或导致重复生成等现象的出现。
  - chat 版本模型基本都需要指定，比如 Meta-Llama-3-8B-Instruct 的 template 就是 llama3

也可提前把相关参数存在 yaml文件里，比如: `LLaMA-Factory/examples/inference/llama3.yaml` at main · hiyouga/LLaMA-Factory， 本地位置是 `examples/inference/llama3.yaml` 

内容如下

```yml
model_name_or_path: /media/codingma/LLM/llama3/Meta-Llama-3-8B-Instruct
template: llama3
```

通过如下命令启动，效果跟上面一样，但是更方便管理

```sh
llamafactory-cli webchat examples/inference/llama3.yaml
```

效果如图，可通过 http://localhost:7860/ 进行访问
- ![](https://pic4.zhimg.com/v2-49fa6327394c0fbcfc971a6e2c22da29_1440w.jpg)


## 推理


### transformers

huggingface transformers 库直接推理

```py
import transformers
import torch

# 切换为你下载的模型文件目录, 这里的demo是Llama-3-8B-Instruct
# 如果是其他模型，比如qwen，chatglm，请使用其对应的官方demo
model_id = "/media/codingma/LLM/llama3/Meta-Llama-3-8B-Instruct"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

prompt = pipeline.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
)

terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

outputs = pipeline(
    prompt,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9,
)
print(outputs[0]["generated_text"][len(prompt):])
```

### API

API 实现标准参考 OpenAI的相关接口协议，基于uvicorn服务框架进行开发， 使用如下的方式启动

本脚本改编自 [llama3_lora_sft.yaml](https://github.com/hiyouga/LLaMA-Factory/blob/main/examples/inference/llama3_lora_sft.yaml)

```sh
CUDA_VISIBLE_DEVICES=0 API_PORT=8000 llamafactory-cli api \
    --model_name_or_path /media/codingma/LLM/llama3/Meta-Llama-3-8B-Instruct \
    --adapter_name_or_path ./saves/LLaMA3-8B/lora/sft \
    --template llama3 \
    --finetuning_type lora
```

项目也支持了基于vllm 的推理后端，但是这里由于一些限制，需要提前将LoRA 模型进行merge，使用merge后的完整版模型目录或者训练前的模型原始目录都可。

```sh
CUDA_VISIBLE_DEVICES=0 API_PORT=8000 llamafactory-cli api \
    --model_name_or_path megred-model-path \
    --template llama3 \
    --infer_backend vllm \
    --vllm_enforce_eager
```

服务启动后，即可按照openai 的API 进行远程访问，主要的区别就是替换 其中的base_url，指向所部署的机器url和端口号即可。

```py
import os
from openai import OpenAI
from transformers.utils.versions import require_version

require_version("openai>=1.5.0", "To fix: pip install openai>=1.5.0")

if __name__ == '__main__':
    # change to your custom port
    port = 8000
    client = OpenAI(
        api_key="0",
        base_url="http://localhost:{}/v1".format(os.environ.get("API_PORT", 8000)),
    )
    messages = []
    messages.append({"role": "user", "content": "hello, where is USA"})
    result = client.chat.completions.create(messages=messages, model="test")
    print(result.choices[0].message)
```


### Ollama

导出GGUF，部署Ollama

GGUF 是 lllama.cpp 设计的大模型存储格式，可以对模型进行高效的压缩，减少模型的大小与内存占用，从而提升模型的推理速度和效率。

Ollama框架可以帮助用户快速使用本地的大型语言模型，那将LLaMA-Factory项目的训练结果导出到Ollama中部署呢？
1. 将lora模型合并
1. 安装gguf库
1. 使用llama.cpp的转换脚本将训练后的完整模型转换为gguf格式
1. 安装Ollama软件
1. 注册要部署的模型文件
1. 启动Ollama

1-3 步是准备好 gguf 格式的文件这也是Ollama所需要的标准格式。

4-6 步就是如何在Ollama环境中启动训练后的模型。

## 分布式

【2025-12-15】[LLaMA-Factory分布式训练实战指南](https://blog.csdn.net/weixin_35516624/article/details/155976841)

LLaMA-Factory 支持 DDP、DeepSpeed、FSDP 三种模式，各有侧重，具体看硬件条件和训练目标。

| 引擎       | 显存效率                | 配置复杂度 | 多机支持 | 推荐场景                                   |
|------------|-------------------------|------------|----------|--------------------------------------------|
| **DDP**    | 中等                    | 极简       | 支持     | 快速验证、中小模型（<13B）、调试首选       |
| **FSDP**   | 高                      | 中等       | 支持     | 多机部署、偏好原生 PyTorch 生态             |
| **DeepSpeed** | 极高（ZeRO-3 + Offload） | 较高       | 支持     | 超大模型、显存紧张、极致显存压缩           |

### 选型方法

核心选型建议
- **快速迭代/调试**：选 **DDP**，配置最简单，适合中小模型快速跑通流程。
- **显存极度受限/超大模型**：选 **DeepSpeed**，通过 ZeRO-3 + Offload 能把显存占用压到极低，支持 100B+ 模型训练。
  - 只有 2×A100 却要训 13B 模型
- **多机生产部署/PyTorch 原生党**：选 **FSDP**，和 PyTorch 生态深度集成，适合稳定的多机分布式训练。
  - 未来可能扩展到多机集群

原则：
- 新项目先用 DDP + LoRA 快速验证 pipeline；
- 显存不够就上 DeepSpeed，尤其是 ZeRO-3；
- 多机部署优先考虑 FSDP，减少外部依赖；
- 所有场景下，QLoRA 都值得尝试，显存节省 70%+，收敛更快。

| 引擎                     | 模型           | 显存/卡 | 速度（tokens/s） | 稳定性   |
|--------------------------|----------------|---------|------------------|----------|
| DDP                      | Qwen-7B        | ~18GB   | ~900             | ★★★★★    |
| DeepSpeed (ZeRO-2)       | Baichuan2-13B  | ~14GB   | ~700             | ★★★★☆    |
| DeepSpeed (ZeRO-3 + Offload) | Llama-2-13B | ~26GB   | ~550             | ★★★☆☆    |
| FSDP (full_shard)        | ChatGLM3-6B    | ~10GB   | ~800             | ★★★★☆    |
| FSDP + Offload           | Qwen-7B（多机）| ~12GB   | ~750             | ★★★★     |


关键结论
- **速度天花板**：**DDP** 最快（~900 tokens/s），稳定性拉满，适合中小模型快速训练。
- **显存最优**：**FSDP (full_shard)** 单卡显存仅 ~10GB，适合显存有限的 6B/7B 级模型。
- **超大模型妥协**：DeepSpeed ZeRO-3 + Offload 显存占用反而更高（~26GB），速度最慢（~550 tokens/s），稳定性也最差，更适合极端显存受限场景。
- **多机平衡**：FSDP + Offload 在多机 Qwen-7B 上表现均衡，显存 ~12GB、速度 ~750 tokens/s，稳定性良好。

 🎯 选型建议
- 如果 **Qwen-7B/ChatGLM3-6B** 这类中小模型，优先选 **DDP** 或 **FSDP (full_shard)**，兼顾速度和显存。
- 如果训 **13B 级模型**，**DeepSpeed ZeRO-2** 是更均衡的选择，比 ZeRO-3 更快更稳。
- 如果 **多机部署**，**FSDP + Offload** 是原生 PyTorch 生态下的优质方案。

结论很清晰：
- 稳定性优先 → 选 DDP
- 显存极度紧张 → DeepSpeed ZeRO-3 + Offload 是唯一选择
- 未来要扩展多机 → FSDP 更易维护

### 依赖检查

```sh
# 检查 PyTorch 分布式能力
python -c "import torch; print('Distributed available:', torch.distributed.is_available())"

# 检查 DeepSpeed
deepspeed --version

# 检查 FSDP 支持
python -c "try: import torch.distributed.fsdp; print('FSDP supported') except: print('FSDP not available')"
```

### DDP 最简单

DDP：最简单，无需额外配置文件，直接用 torchrun 启动

示例
- --`nproc_per_node=4`: 单机4卡
- --`fp16`: 开启混合精度，显存节省约 40%
- --`ddp_find_unused_parameters=false` 可提升约 5%~10% 训练速度，适用于 LoRA 微调方式


```sh
torchrun --nproc_per_node=4 \
  src/train_bash.py \
  --stage sft \
  --do_train \
  --model_name_or_path /models/Qwen-7B-Chat \
  --dataset medical_zh \
  --finetuning_type lora \
  --output_dir ./output/qwen-7b-lora-ddp \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 8 \
  --learning_rate 2e-4 \
  --num_train_epochs 3 \
  --fp16 \
  --ddp_find_unused_parameters false \
  --plot_loss
```

### DeepSpeed：显存压缩之王

当模型变大（如 13B 级别），DDP 很容易 OOM。这时就得靠 DeepSpeed 的 ZeRO 技术来“瘦身”。

实测：
- 2×A100（40GB）上成功运行 Baichuan2-13B 的 LoRA 微调，显存峰值控制在 32GB 以内

先写配置文件：ds_z3_offload.json

三重减负：
- ZeRO-3：分片优化器状态、梯度、权重；
- CPU Offload：将部分状态卸载到内存；
- bf16：比 fp16 更稳定，适合大模型。

```json
{
  "train_batch_size": 64,
  "train_micro_batch_size_per_gpu": 2,
  "gradient_accumulation_steps": 8,
  "bf16": { "enabled": true },
  "fp16": { "enabled": false },
  "optimizer": {
    "type": "AdamW",
    "params": {
      "lr": 2e-4,
      "betas": [0.9, 0.999],
      "eps": 1e-8,
      "weight_decay": 0.01
    }
  },
  "scheduler": {
    "type": "WarmupCosineLR",
    "params": {
      "warmup_min_lr": 0,
      "warmup_max_lr": 2e-4,
      "warmup_num_steps": 100,
      "total_num_steps": 12000
    }
  },
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": { "device": "cpu", "pin_memory": true },
    "offload_param": { "device": "cpu", "pin_memory": true },
    "overlap_comm": true,
    "contiguous_gradients": true,
    "reduce_bucket_size": 1e8,
    "allgather_bucket_size": 5e8
  },
  "gradient_clipping": 1.0
}
```

启动训练

```sh
deepspeed --num_gpus=4 \
  src/train_bash.py \
  --model_name_or_path /models/Baichuan2-13B-Chat \
  --dataset finance_en \
  --finetuning_type lora \
  --output_dir ./output/baichuan2-13b-lora-deepspeed \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 8 \
  --deepspeed ./ds_z3_offload.json \
  --fp16
```

### FSDP：轻量级多机友好方案

FSDP 是 PyTorch 2.0 原生分片方案，不用引入 DeepSpeed 第三方依赖，更适合长期维护的生产系统

注意 
- PyTorch 版本需 ≥ 2.0，否则 torch.distributed.fsdp 模块将不可用

关键参数说明：
- full_shard：对模型状态全面分片；
- auto_wrap：自动包装 Transformer 层；
- offload：将部分张量卸载至 CPU；
- GLMBlock：ChatGLM 的基本模块名，必须准确指定，否则分片无效。

🔥 注意：
- LoRA 微调必须加上 --fsdp_use_orig_params true，否则会出现参数未绑定的问题。

```sh
torchrun --nproc_per_node=4 \
  src/train_bash.py \
  --stage sft \
  --do_train \
  --model_name_or_path /models/ChatGLM3-6B \
  --dataset law_zh \
  --finetuning_type lora \
  --output_dir ./output/chatglm3-6b-lora-fsdp \
  --per_device_train_batch_size 4 \
  --gradient_accumulation_steps 4 \
  --learning_rate 5e-5 \
  --num_train_epochs 3 \
  --fp16 \
  --fsdp "full_shard auto_wrap offload" \
  --fsdp_transformer_layer_cls_to_wrap "GLMBlock" \
  --fsdp_use_orig_params true \
  --plot_loss
```


原文链接：https://blog.csdn.net/weixin_35516624/article/details/155976841

### 多机训练：跨节点协同的那些坑

当训练更大模型或处理海量数据时，单机已无法满足需求。多机训练的关键在于 网络通信稳定性和路径一致性。

前提条件
- 所有机器在同一内网，可通过 IP 直接访问；
- 统一安装相同版本的 CUDA、PyTorch、LLaMA-Factory；
- 模型和数据集挂载在共享路径（推荐 NFS）；
- 主节点 SSH 免密登录所有从节点；
- 防火墙开放端口（默认 29500）；
- 所有节点时间同步（建议启用 NTP）。

#### (1) DDP 多机训练：手动协调节点

创建 hostfile 文件：

```
192.168.1.10 master_addr=192.168.1.10 slots=4
192.168.1.11 slots=4
```

主节点执行

```sh
torchrun \
  --nnodes=2 \
  --node_rank=0 \
  --master_addr=192.168.1.10 \
  --master_port=29500 \
  --nproc_per_node=4 \
  src/train_bash.py \
  --model_name_or_path /shared/models/Qwen-7B-Chat \
  --dataset alpaca_gpt4_en \
  --finetuning_type lora \
  --output_dir /shared/output/qwen-7b-ddp-multi \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 8 \
  --fp16 \
  --ddp_find_unused_parameters false
```

从节点执行相同命令，仅修改 --node_rank=1。

⚠️ 常见错误：
- “Connection refused” —— 检查 master_addr 是否为真实 IP，不能是 localhost 或 127.0.0.1。

#### (2) DeepSpeed 多机：一键启动

每个节点运行相同命令，--node_rank 按顺序设置为 0, 1, … 即可。

💡 提醒：
- 所有节点必须能访问相同的模型路径（如 NFS），否则会报 “Model file not found”。

DeepSpeed 自动管理多节点，只需加 --num_nodes 参数：

```sh
deepspeed \
  --num_nodes=2 \
  --num_gpus=4 \
  --master_addr=192.168.1.10 \
  --master_port=29500 \
  --node_rank=0 \
  src/train_bash.py \
  --model_name_or_path /shared/models/Llama-2-13B-chat-hf \
  --dataset medical_zh \
  --finetuning_type lora \
  --deepspeed ./ds_z3_offload.json \
  --fp16
```

#### (3) FSDP 多机：配置与 DDP 完全一致

FSDP 多机启动方式与 DDP 几乎一样，只是保留了 FSDP 参数

不同模型对应的 layer class 名称：
- Qwen / LLaMA → QWenBlock / LlamaDecoderLayer
- ChatGLM → GLMBlock
- Baichuan → BaichuanLayer

务必根据实际模型结构填写，否则分片不会生效。


```sh
torchrun \
  --nnodes=2 \
  --node_rank=0 \
  --master_addr=192.168.1.10 \
  --master_port=29500 \
  --nproc_per_node=4 \
  src/train_bash.py \
  --model_name_or_path /shared/models/Qwen-7B-Chat \
  --dataset finance_en \
  --finetuning_type lora \
  --output_dir /shared/output/qwen-7b-lora-fsdp-multi \
  --per_device_train_batch_size 4 \
  --gradient_accumulation_steps 4 \
  --fp16 \
  --fsdp "full_shard auto_wrap offload" \
  --fsdp_transformer_layer_cls_to_wrap "QWenBlock" \
  --fsdp_use_orig_params true
```


## 常见问题

常见问题与解决方案（亲测有效）

### 1. 显存不足（OOM）

✅ 应对策略：
- 降低 per_device_train_batch_size
- 增加 gradient_accumulation_steps 保持总 batch size
- 启用 fp16 或 bf16
- DeepSpeed 使用 ZeRO-3 + CPU Offload
- FSDP 添加 --fsdp_offload_params_to_cpu true

小技巧：QLoRA 比 LoRA 更省显存，可进一步压缩 30%，但需转换模型为 bitsandbytes 格式。

### 2. 多机通信失败

常见报错：Connection refused, Address already in use

✅ 检查清单：
- master_addr 是否为真实内网 IP
- master_port 是否被占用（lsof -i :29500）
- 防火墙是否放行
- SSH 免密登录是否配置正确
- 所有节点时间是否同步（timedatectl status）

### 3. DeepSpeed 报错 “ZeRO stage 3 not supported”

可能原因：
- DeepSpeed 版本 < v0.9.0 → 升级
- 使用了不兼容优化器 → 加 "zero_allow_untested_optimizer": true
- LoRA 与 ZeRO-3 冲突 → 改用 ZeRO-2 或切换为 FSDP

### 4. FSDP 报错 “Did not instantiate model with FSDP”

解决方法：
- 确保 --fsdp 参数格式正确（空格分隔）
- 检查 --fsdp_transformer_layer_cls_to_wrap 拼写
- 必须添加 --fsdp_use_orig_params true（LoRA 必须）
- PyTorch ≥ 2.0



## LLaMA-Factory 可视化


### LLaMA Board

Web UI 使用
- LLaMA Board 可视化微调（由 Gradio 驱动）
- Web UI 目前只支持**单卡**训练/推理，当机器有多张显卡时请使用 `CUDA_VISIBLE_DEVICES` 指定一张显卡启动程序。
- 启动网页UI，系统上必须有 GPU ！

目前webui版本只支持**单机单卡**和**单机多卡**，如果是**多机多卡**请使用命令行版本

```sh
# Web UI 使用
llamafactory-cli webui    # 启动网页端
CUDA_VISIBLE_DEVICES=0 llamafactory-cli webui
CUDA_VISIBLE_DEVICES=4 llamafactory-cli webui    # 指定第4张显卡使用
# 如果开启 gradio share功能，或者修改端口号
CUDA_VISIBLE_DEVICES=0 GRADIO_SHARE=1 GRADIO_SERVER_PORT=7860 llamafactory-cli webui
```

上述的多个不同的大功能模块都通过不同的tab进行了整合，提供了一站式操作体验。
- 训练 → 批量评估 → 交互测试 → 模型导出
- ![](https://pic4.zhimg.com/v2-a1de61e1483e65fc7b237de43bb437fd_1440w.jpg)
- train页面，可通过预览命令功能，将训练脚本导出，用于支持多gpu训练
- ![](https://pic3.zhimg.com/v2-f0f30aba4c6280a4c54aa599f41fa292_1440w.jpg)

点击开始按钮, 即可开始训练，网页端和服务器端会同步输出相关的日志结果
- ![](https://pic2.zhimg.com/v2-3696353c7c0eea5081314ab75b257b29_1440w.jpg)

训练完毕后, 点击“刷新适配器”，可找到该模型历史上使用webui训练的LoRA模型文件，后续再训练或者执行chat的时候，即会将此LoRA一起加载。

### W&B

Weights & Biases 记录实验数据，请在 yaml 文件中添加下面的参数。

```yml
report_to: wandb
run_name: test_run # 可选
```

启动训练任务时，将 WANDB_API_KEY 设置为密钥来登录 W&B 账户。

### SwanLab

用 SwanLab 记录实验数据，请在 yaml 文件中添加下面的参数。

```yml
use_swanlab: true
swanlab_run_name: test_run # 可选
```

启动训练任务时，登录 SwanLab账户 有三种方式：
- 方式一：在 yaml 文件中添加 `swanlab_api_key=<your_api_key>` ，并设置 API 密钥。 
- 方式二：将环境变量 `SWANLAB_API_KEY` 设置为你的 API 密钥。 
- 方式三：启动前使用 `swanlab login` 命令完成登录。


## 数据集


目前支持 alpaca 和 sharegpt 两种数据格式

以alpaca为例，整个数据集是一个json对象的list，具体数据格式为

```json
[
  {
    "instruction": "用户指令（必填）",
    "input": "用户输入（选填）",
    "output": "模型回答（必填）",
    "system": "系统提示词（选填）",
    "history": [
      ["第一轮指令（选填）", "第一轮回答（选填）"],
      ["第二轮指令（选填）", "第二轮回答（选填）"]
    ]
  }
]
```

例子比如单轮（alpaca_data_zh_51k.json 中的例子, 数据集在data/dataset_info.json中注册为alpaca_zh）

```json
{
  "instruction": "写一个有效的比较语句",
  "input": "篮球和足球",
  "output": "篮球和足球都是受欢迎的运动。"
}
```

和多轮 （oaast_sft_zh.json 中的例子, 数据集在data/dataset_info.json中注册为oaast_sft_zh）

```json
{
  "instruction": "谢谢",
  "input": "",
  "output": "不用谢! 很高兴我提供的信息能够帮助到你! 如果还有什么其他问题也可以向我提问。",
  "history": [
    [
      "请你给我写一个面试准备计划，我想要去面试微软的程序员岗位",
      "首先，你可以去微软官网寻找招聘信息并申请面试。\n其次，您可以在社交媒体平台寻找微软公司对程序员的面试问题，并做好准备。\n最后，您可以自己对面试过程进行模拟，熟悉话题并减少紧张感。\n我希望你能面试成功。"
    ]
  ]
}
```


## 应用案例

多GPU分布式训练, 多种工具
- huggingface Accelerate
- DeepSpeed

[参考](https://zhuanlan.zhihu.com/p/718263213?utm_psn=1815334840821751808)

微调类型: full, freeze, lora

### 指令监督微调

sft lora

```sh
CUDA_VISIBLE_DEVICES=0 llamafactory-cli train \ 
# CUDA_VISIBLE_DEVICES=0 nohup python src/train_bash.py # 另一个启动选项
    --stage sft \        # 训练阶段 “sft”,"pt","rm","ppo"
    --do_train \         # 是否训练模式
    --model_name_or_path /media/codingma/LLM/llama3/Meta-Llama-3-8B-Instruct \ 
    --dataset alpaca_gpt4_zh,identity,adgen_local \ # 数据集列表, 多个数据集逗号分隔
    --dataset_dir ./data \  # 数据集目录，自带的data
    --template llama3 \  # 可以是 qwen
    --finetuning_type lora \  # 微调类型: full, freeze, lora
    --output_dir ./saves/LLaMA3-8B/lora/sft \  # 模型保存目录
    --overwrite_cache \ 
    --overwrite_output_dir \ 
    --cutoff_len 1024 \  # 长度截断
    --preprocessing_num_workers 16 \  # 
    --per_device_train_batch_size 2 \  # 训练时，各节点最小 batch_size
    --per_device_eval_batch_size 1 \  # 训练时，各节点最小 batch_size
    --gradient_accumulation_steps 8 \  # 梯度累积步数
    --lr_scheduler_type cosine \  # 学习率衰减策略
    --logging_steps 50 \  # 打日志步数
    --warmup_steps 20 \  # warmup
    --save_steps 100 \  # 模型保存间隔步数
    --eval_steps 50 \ 
    --evaluation_strategy steps \   # 
    --load_best_model_at_end \ 
    --learning_rate 5e-5 \ 
    --num_train_epochs 5.0 \ 
    --max_samples 1000 \  # 采样数
    --val_size 0.1 \ 
    --plot_loss \ 
    --fp16  # 半精度, v100不支持 bf16
```

训练结果
- ![](https://pica.zhimg.com/v2-c28f3d74144619426c06d6cf8fd1ff42_1440w.jpg)

output_dir 下主要包含3部分
- adapter 开头: LoRA保存的结果了，后续用于模型推理融合
- training_loss 和 trainer_log 等记录训练的过程指标
- 其他是训练当时各种参数的备份

loss在 正常情况下会随着训练的时间慢慢变小，最后需要下降到1以下的位置才会有一个比较好的效果，可以作为训练效果的一个中间指标。

lora 效果验证
- webui
- terminal

lora 模型推理: webchat 
- 指定原模型+lora模型

```sh
CUDA_VISIBLE_DEVICES=0 llamafactory-cli webchat \ 
    --model_name_or_path /media/codingma/LLM/llama3/Meta-Llama-3-8B-Instruct \ 
    --adapter_name_or_path ./saves/LLaMA3-8B/lora/sft  \
    --template llama3 \  
    --finetuning_type lora
```

terminal 终端验证

```sh
CUDA_VISIBLE_DEVICES=0 llamafactory-cli chat \
    --model_name_or_path /media/codingma/LLM/llama3/Meta-Llama-3-8B-Instruct \
    --adapter_name_or_path ./saves/LLaMA3-8B/lora/sft  \
    --template llama3 \
    --finetuning_type lora
```

批量自动化评估

```sh
pip install jieba
pip install rouge-chinese
pip install nltk
```

本脚参考[文件参数](https://github.com/hiyouga/LLaMA-Factory/blob/main/examples/train_lora/llama3_lora_predict.yaml)

```sh
CUDA_VISIBLE_DEVICES=0 llamafactory-cli train \
    --stage sft \
    --do_predict \  # 预测模式
    --model_name_or_path /media/codingma/LLM/llama3/Meta-Llama-3-8B-Instruct \
    --adapter_name_or_path ./saves/LLaMA3-8B/lora/sft  \
    --eval_dataset alpaca_gpt4_zh,identity,adgen_local \
    --dataset_dir ./data \
    --template llama3 \
    --finetuning_type lora \
    --output_dir ./saves/LLaMA3-8B/lora/predict \
    --overwrite_cache \
    --overwrite_output_dir \
    --cutoff_len 1024 \
    --preprocessing_num_workers 16 \
    --per_device_eval_batch_size 1 \
    --max_samples 20 \  # 预测阶段采样数目
    --predict_with_generate  # 生成阶段
```

评估预测脚本 vs 训练脚本

区别如下两个
- `do_predict`	预测模式
- `predict_with_generate`	生成文本
- `max_samples`	每个数据集采样多少用于预测对比


训练的LoRA和原始大模型进行融合，输出一个完整的模型文件

参考 [llama3_lora_sft.yaml](LLaMA-Factory/examples/merge_lora/llama3_lora_sft.yaml)

```sh
CUDA_VISIBLE_DEVICES=0 llamafactory-cli export \
    --model_name_or_path /media/codingma/LLM/llama3/Meta-Llama-3-8B-Instruct \
    --adapter_name_or_path ./saves/LLaMA3-8B/lora/sft  \
    --template llama3 \
    --finetuning_type lora \
    --export_dir megred-model-path \
    --export_size 2 \
    --export_device cpu \
    --export_legacy_format False
```

Accelerate

```sh
accelerate launch   src/train.py \
  --ddp_timeout  18000000 \
    --stage sft \
    --do_train \
    --model_name_or_path /gemini/pretrain/Qwen1.5-4B/ \
    --dataset alpaca_gpt4_data_zh,alpaca_gpt4_data_en,glaive_toolcall_zh_demo,adgen_local \
    --template qwen \
    --finetuning_type lora \
    --lora_target q_proj,v_proj \
    --output_dir path_to_sft_checkpoint \
    --overwrite_cache \
    --overwrite_output_dir
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 5e-5 \
    --num_train_epochs 3.0 \
    --plot_loss \
    --fp16
```

使用 DeepSpeed

```sh
deepspeed --num_gpus 2   src/train.py \
 --deepspeed ds_config.json \
  --ddp_timeout  18000000 \
    --stage sft \
    --do_train \
    --model_name_or_path /gemini/pretrain/Qwen1.5-4B/ \
    --dataset alpaca_zh_demo \
    --template qwen \
    --finetuning_type lora \
    --lora_target q_proj,v_proj \
    --output_dir path_to_sft_checkpoint \
    --overwrite_cache \
    --overwrite_output_dir
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 5e-5 \
    --num_train_epochs 3.0 \
    --plot_loss \
    --fp16
```


### 奖励模型训练

示例
- finetune_type = lora

```sh
CUDA_VISIBLE_DEVICES=0 python src/train_bash.py \   
  --stage rm \
  --do_train \
  --model_name_or_path /data/models/sft_qwen/
  --create_new_adapter \
  --dataset comparison_gpt4_zh \
  --template qwen \
  --finetuning_type lora \
  --lora_target c_attn \
  --output_dir /data/models/rm_qwen \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 4 \
  --lr_scheduler_type cosine \
  --logging_steps 10 \
  --save_steps 1000 \
  --learning_rate 1e-6 \
  --num_train_epochs 1.0 \
  --plot_loss \
  --fp16
```

lora 合并

```sh
合并：

python src/export_model.py 
  --model_name_or_path /data/models/Qwen-1_8B-Chat 
  --adapter_name_or_path /data/models/sft_qwen 
  --template qwen 
  --finetuning_type lora 
  --export_dir /data/models/export_qwen/
```

Accelerate

```sh
accelerate launch   src/train.py \
    --stage rm \
    --do_train \
    --model_name_or_path /gemini/pretrain/Qwen1.5-4B/ \
    --adapter_name_or_path path_to_sft_checkpoint \
    --create_new_adapter \
    --dataset dpo_zh_demo \
    --template qwen \
    --finetuning_type lora \
    --lora_target q_proj,v_proj \
    --output_dir path_to_ac_rm_checkpoint \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 1e-5 \
    --num_train_epochs 1.0 \
    --plot_loss \
    --fp16
```

使用 DeepSpeed

```sh
deepspeed --num_gpus 2   src/train.py \
   --deepspeed ds_config.json \
    --stage rm \
    --do_train \
    --model_name_or_path /gemini/pretrain/Qwen1.5-4B/ \
    --adapter_name_or_path path_to_sft_checkpoint \
    --create_new_adapter \
    --dataset dpo_zh_demo \
    --template qwen \
    --finetuning_type lora \
    --lora_target q_proj,v_proj \
    --output_dir path_to_deep_rm_checkpoint \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 1e-5 \
    --num_train_epochs 1.0 \
    --plot_loss \
    --fp16
```

### ppo 训练

示例

```sh
CUDA_VISIBLE_DEVICES=0 nohup python src/train_bash.py 
  --stage ppo 
  --do_train 
  --model_name_or_path /data/models/export_qwen 
  --create_new_adapter 
  --dataset alpaca_gpt4_zh 
  --template qwen 
  --finetuning_type lora 
  --lora_target c_attn 
  --reward_model /data/models/rm_qwen 
  --output_dir /data/models/ppo_qwen 
  --per_device_train_batch_size 2 
  --gradient_accumulation_steps 4 
  --lr_scheduler_type cosine 
  --top_k 0 
  --top_p 0.9 
  --logging_steps 10 
  --save_steps 1000 
  --learning_rate 1e-5 
  --num_train_epochs 1.0 
  --plot_loss 
  --overwrite_output_dir 
  --fp16 >>log &
```

Accelerate

```sh
accelerate launch src/train.py \
    --stage ppo \
    --do_train \
    --model_name_or_path /gemini/pretrain/Qwen1.5-4B/ \
    --adapter_name_or_path path_to_sft_checkpoint \
    --create_new_adapter \
    --dataset alpaca_zh_demo \
    --template qwen \
    --finetuning_type lora \
    --lora_target q_proj,v_proj \
    --reward_model path_to_ac_rm_checkpoint \
    --output_dir path_to_ac_ppo_checkpoint \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --top_k 0 \
    --top_p 0.9 \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 1e-5 \
    --num_train_epochs 1.0 \
    --plot_loss \
    --fp16
```

deepspeed

```sh
deepspeed --num_gpus 2  src/train.py \
    --deepspeed ds_config.json  \
    --stage ppo \
    --do_train \
    --model_name_or_path /gemini/pretrain/Qwen1.5-4B/ \
    --adapter_name_or_path path_to_sft_checkpoint \
    --create_new_adapter \
    --dataset alpaca_zh_demo \
    --template qwen \
    --finetuning_type lora \
    --lora_target q_proj,v_proj \
    --reward_model path_to_deep_rm_checkpoint \
    --output_dir path_to_deep_ppo_checkpoint \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --top_k 0 \
    --top_p 0.9 \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 1e-5 \
    --num_train_epochs 1.0 \
    --plot_loss \
    --fp16
```



### dpo 训练

DPO算法不依赖RM阶段，不需要RM模型。

```sh
nohup deepspeed --include="localhost:1,2,3,4,5,6,7" --master_port=9901  src/train_bash.py 
  --deepspeed ds_config.json 
  --stage dpo 
  --do_train 
  --model_name_or_path /data/models/chatglm3-6b/ 
  --adapter_name_or_path /data/models/lora_chatglm 
  --create_new_adapter 
  --dataset comparison_gpt4_zh 
  --template chatglm3 
  --finetuning_type lora 
  --lora_target query_key_value 
  --output_dir /data/models/chatglm3_dpo 
  --per_device_train_batch_size 1 
  --gradient_accumulation_steps 4 
  --lr_scheduler_type cosine 
  --logging_steps 10 
  --save_steps 2000 
  --learning_rate 1e-5 
  --num_train_epochs 1.0 
  --plot_loss 
  --fp16 >> log&
```

Accelerate

```sh
accelerate launch src/train.py \
    --stage dpo \
    --do_train \
    --model_name_or_path /gemini/pretrain/Qwen1.5-4B/ \
    --adapter_name_or_path path_to_sft_checkpoint \
    --create_new_adapter \
    --dataset dpo_zh_demo \
    --template qwen \
    --finetuning_type lora \
    --lora_target q_proj,v_proj \
    --output_dir path_to_ac_dpo_checkpoint \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 1e-5 \
    --num_train_epochs 1.0 \
    --plot_loss \
    --fp16 
```

deepspeed

```sh
deepspeed --num_gpus 2   src/train.py \
    --deepspeed ds_config.json  \
    --stage dpo \
    --do_train \
    --model_name_or_path /gemini/pretrain/Qwen1.5-4B/ \
    --adapter_name_or_path path_to_sft_checkpoint \
    --create_new_adapter \
    --dataset dpo_zh_demo \
    --template qwen \
    --finetuning_type lora \
    --lora_target q_proj,v_proj \
    --output_dir path_to_deep_dpo_checkpoint \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 1e-5 \
    --num_train_epochs 1.0 \
    --plot_loss \
    --fp16 
```


# 结束
