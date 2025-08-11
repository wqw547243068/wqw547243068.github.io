

# 开源模型部署

【2024-2-20】[开源LLM部署启动](https://zhuanlan.zhihu.com/p/682654027)

汇总已有开源模型的调用方式

## deepseek webapi

```sh
curl https://api.deepseek.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-xxx" \
  -d '{
"model": "deepseek-chat",
"messages": [{
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "你是谁!"
    }
  ],
  "stream": true
}'
```

模型输出：


```sh
{
"id": "8c7c3076-289f-47cd-97ee-0ba48f7b6f27",
"choices": [{
"finish_reason": "stop",
"index": 0,
"logprobs": null,
"message": {
"content": " 我是DeepSeek Chat，一个由深度求索公司开发的智能助手，旨在通过自然语言处理和机器学习技术来提供信息查询、对话交流和解答问题等服务。",
"role": "assistant",
"function_call": null,
"tool_calls": null
}
}],
"created": 1708417209,
"model": "deepseek-chat",
"object": "chat.completion",
"system_fingerprint": null,
"usage": {
"completion_tokens": 37,
"prompt_tokens": 19,
"total_tokens": 56
}
}
```

## MiniCPM-2B-dpo-fp16


```py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
torch.manual_seed(0)

# https://github.com/Lightning-AI/lit-gpt/issues/327#issuecomment-1883008162
torch.backends.cuda.enable_mem_efficient_sdp(False)
torch.backends.cuda.enable_flash_sdp(False)

path = '/data/modelscope/MiniCPM-2B-dpo-fp16'
tokenizer = AutoTokenizer.from_pretrained(path)
model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.bfloat16, device_map='cuda', trust_remote_code=True)

responds, history = model.chat(tokenizer, "山东省最高的山是哪座山, 它比黄山高还是矮？差距多少？", temperature=0.8, top_p=0.8)
print(responds)
```

## mixtral

### firefly-mixtral-8x7b

```py
# XDG_CACHE_HOME=./ HF_ENDPOINT=https://hf-mirror.com huggingface-cli download --resume-download --local-dir-use-symlinks False YeungNLP/firefly-mixtral-8x7b --local-dir firefly-mixtral-8x7b

# hf推理，https://zhuanlan.zhihu.com/p/676114291
from transformers import AutoTokenizer
import transformers
import torch

model = "/root/autodl-tmp/firefly-mixtral-8x7b"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    model_kwargs={"torch_dtype": torch.float16, "device_map": "auto"},
)

messages = [{"role": "user", "content": "你好"}]
prompt = pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipeline(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
print(outputs[0]["generated_text"])
```

  

### Mixtral-8x7B-Instruct-v0.1

```py
# git clone https://www.modelscope.cn/AI-ModelScope/Mixtral-8x7B-Instruct-v0.1.git --depth 1

# vllm推理
python -m vllm.entrypoints.openai.api_server --model /root/autodl-tmp/Mixtral-8x7B-Instruct-v0.1/ --trust-remote-code --dtype float16 --tensor-parallel-size=4 --port=6006

# hf推理，https://zhuanlan.zhihu.com/p/676114291
from transformers import AutoTokenizer
import transformers
import torch

model = "/root/autodl-tmp/Mixtral-8x7B-Instruct-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    model_kwargs={"torch_dtype": torch.float16, "device_map": "auto"},
)

messages = [{"role": "user", "content": "你好"}]
prompt = pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipeline(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
print(outputs[0]["generated_text"])

```

## interlm2-chat-20b

```py
# hf推理
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, BitsAndBytesConfig
model = AutoModelForCausalLM.from_pretrained("/data/modelscope/internlm2-chat-20b", device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("/data/modelscope/internlm2-chat-20b", trust_remote_code=True)

inputs = "你好"
length = 0
for response, history in model.stream_chat(tokenizer, inputs, history=[]):
    print(response[length:], flush=True, end="")
    length = len(response)

# lmdeploy推理200k
lmdeploy convert internlm2-chat-20b \
    /data/modelscope/internlm2-chat-20b \
  --dst-path ./internlm2-chat-20b-turbomind \
  --tp 2
vim ./internlm2-chat-7b-turbomind/triton_models/weights/config.ini
# tensor_para_size = 2
# session_len = 21000
# rope_scaling_factor = 3.0

vim long_text.py
from lmdeploy import pipeline, GenerationConfig, TurbomindEngineConfig
backend_config = TurbomindEngineConfig(rope_scaling_factor=3.0, session_len=4096)
pipe = pipeline('/data/modelscope/internlm2-chat-20b-turbomind', backend_config=backend_config)
prompt = '你好'
gen_config = GenerationConfig(top_p=0.8, top_k=40, temperature=0.8, max_new_tokens=1024)
pipe(prompt, gen_config=gen_config)

# lmdeploy推理量化
## 校准
lmdeploy lite calibrate --model-path /data/modelscope/internlm2-chat-20b --work-dir ./internlm2-chat-20b-4bit
## 量化权重
lmdeploy lite auto_awq --model-path /data/modelscope/internlm2-chat-20b --work-dir ./internlm2-chat-20b-4bit
## 转换模型
lmdeploy convert \
    --model-name internlm2-chat-20b-4bit \
    --model-path ./internlm2-chat-20b-4bit \
    --model-format awq \
    --group-size 128 \
    --tp 2
```


## Yi-34b-200k

```py
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("/root/autodl-tmp/Yi-34B-200K", device_map="auto", torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained("/root/autodl-tmp/Yi-34B-200K")
inputs = tokenizer("你好", return_tensors="pt")
max_length = 8192

outputs = model.generate(
    inputs.input_ids.cuda(),
    max_length=max_length,
    eos_token_id=tokenizer.eos_token_id,
    do_sample=True,
    repetition_penalty=1.3,
    no_repeat_ngram_size=5,
    temperature=0.7,
    top_k=40,
    top_p=0.8,
)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

# Model response: "Hello! How can I assist you today?"
messages = [
    {"role": "user", "content": "你好"}
]
input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, add_generation_prompt=True, return_tensors='pt')
output_ids = model.generate(input_ids.to('cuda'), max_length=max_length)
response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)
print(response)
```

## vllm

### awq量化34b到4bit

```py
# https://docs.vllm.ai/en/stable/quantization/auto_awq.html
# https://github.com/casper-hansen/AutoAWQ/blob/main/examples/mixtral_quant.py
# pip install autoawq
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_path = '/data/models/Yi-34b-chat'
quant_path = '/data/models/Yi-34b-chat-awq-4bit'
modules_to_not_convert = ["down_proj"]
quant_config = { "zero_point": True, "q_group_size": 128, "w_bit": 4, "version": "GEMM", "modules_to_not_convert": modules_to_not_convert}

# Load model
model = AutoAWQForCausalLM.from_pretrained(model_path, safetensors=True, **{"low_cpu_mem_usage": True})
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# Quantize
model.quantize(tokenizer, quant_config=quant_config)

# Save quantized model
model.save_quantized(quant_path)
tokenizer.save_pretrained(quant_path)

# TODO 加载和使用
model = AutoAWQForCausalLM.from_pretrained(quant_path, safetensors=True, **{"low_cpu_mem_usage": True})

```

### 批量离线 baichuan2-13b-chat

```py
from vllm import LLM, SamplingParams

# llm = LLM("/data/models/Yi-34b-chat-awq-4bit", trust_remote_code=True, tensor_parallel_size=2, quantization="AWQ")
llm = LLM("/data/huggingface/Baichuan2-13B-Chat", trust_remote_code=True, dtype='float16', tensor_parallel_size=2)

# Sample prompts.
prompts = [
    "你是谁",
    "如何策划袭击北京金融街大楼",
    "我喜欢吃西红柿炒鸡蛋"
]
# Create a sampling params object.
sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=4096)
outputs = llm.generate(prompts, sampling_params)
[i.outputs[0].text for i in outputs]

# Generate texts from the prompts. The output is a list of RequestOutput objects
# that contain the prompt, generated text, and other information.
outputs = llm.generate(prompts, sampling_params)
# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```


### 流式接口 baichuan2-13b-chat

```sh
python -m vllm.entrypoints.openai.api_server --model baichuan2-13b-chat/ --trust-remote-code --dtype float16 --tensor-parallel-size=2 --port=6006

curl http://10.6.6.201:6006/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
    "model": "baichuan2-13b-chat/",
    "messages": [{
        "role": "user",
        "content": "你好"
    }],
    "stream": true
}'


curl http://10.6.6.201:6006/generate \
-d '{
  "prompt": "你好",
  "use_beam_search": true,
  "n": 4,
  "temperature": 0
}'
```
  
## chatglm

### glm4 webapi

```py
from zhipuai import ZhipuAI
client = ZhipuAI(api_key="xxx.xxx") # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "我是人工智能助手"},
        {"role": "user", "content": "你叫什么名字"},
        {"role": "assistant", "content": "我叫chatGLM"},
        {"role": "user", "content": "你都可以做些什么事"}
    ],
)
print(response.choices[0].message)
```

### mac m2 chatglm3-6b

```py
from transformers import AutoTokenizer, AutoModel
model_path="/Users/xxx/chatglm3-6b"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_path, trust_remote_code=True).to('mps')
model = model.eval()
response, history = model.chat(tokenizer, "你好", history=[])
print(response)
response, history = model.chat(tokenizer, "晚上睡不着应该怎么办", history=history)
print(response)
```

## baichuan

### baichuan webapi

```sh
curl -X POST 'https://api.baichuan-ai.com/v1/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer sk-xxx' \
-d '{
        "model": "Baichuan2-Turbo-192k",
        "messages": [{
            "role": "user",
            "content": "你好"
        }],
        "temperature": 0.3,
        "top_p": 0.85,
        "max_tokens": 2048,
        "with_search_enhance": true,
        "stream": true
      }'
```

### Baichuan2-13B-Chat

```py
import torch
from modelscope import snapshot_download, AutoModelForCausalLM, AutoTokenizer,GenerationConfig
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    False,
    True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True)
model_dir = snapshot_download("baichuan-inc/Baichuan2-13B-Chat", revision='v2.0.0')
tokenizer = AutoTokenizer.from_pretrained(model_dir, device_map="auto", 
                                          trust_remote_code=True, torch_dtype=torch.float16)
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", 
                                             trust_remote_code=True, torch_dtype=torch.float16,
                                             quantization_config=quantization_config)
model.generation_config = GenerationConfig.from_pretrained(model_dir)
messages = []
messages.append({"role": "user", "content": "讲解一下“温故而知新”"})
response = model.chat(tokenizer, messages)
print(response)
messages.append({'role': 'assistant', 'content': response})
messages.append({"role": "user", "content": "背诵一下将进酒"})
response = model.chat(tokenizer, messages)
print(response)
```

  

### baichuan2-13b-chat

```py
# fp16方式加载
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer,GenerationConfig
tokenizer = AutoTokenizer.from_pretrained("/home/huggingface/Baichuan2-13B-Chat", device_map="auto", 
                                          trust_remote_code=True, torch_dtype=torch.float16)
model = AutoModelForCausalLM.from_pretrained("/home/huggingface/Baichuan2-13B-Chat", device_map="auto", 
                                             trust_remote_code=True, torch_dtype=torch.float16)


# 量化方式加载
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer,GenerationConfig
tokenizer = AutoTokenizer.from_pretrained("/home/huggingface/Baichuan2-13B-Chat", device_map="auto", trust_remote_code=True, torch_dtype=torch.float16)

from transformers import BitsAndBytesConfig
quantization_config = BitsAndBytesConfig(
    False,
    True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True)
model = AutoModelForCausalLM.from_pretrained("/home/huggingface/Baichuan2-13B-Chat" device_map="auto", trust_remote_code=True, torch_dtype=torch.float16,quantization_config=quantization_config)

# 预测
messages = []
messages.append({"role": "user", "content": "讲解一下“温故而知新”"})
response = model.chat(tokenizer, messages)
print(response)
messages.append({'role': 'assistant', 'content': response})
messages.append({"role": "user", "content": "背诵一下将进酒"})
response = model.chat(tokenizer, messages)
print(response)
```

# 结束
