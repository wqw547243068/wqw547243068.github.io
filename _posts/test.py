import os
import sys
import torch
from torch.nn.function as F
import tiktoken

class MultiHeadAttention(nn.Module):
    """
        多头注意力
    """

    def __init__(self, head_num, dim, vocab_size):
        
        self.sa = None
        self.head_num = head_num
        self.embdding = None
        self.all_dim = dim
        self.vocab_size = vocab_size
        self.single_dim = int(dim/head_num) # 按维度切分，整数判断，待定
        self.k = torch.nn.linear(self.single_dim, self.single_dim)
        self.v = torch.nn.linear(self.single_dim, self.single_dim)
        self.multi_attention_block = []


    def selfAttention(self, q):
        """
            自注意力
            sa = softmax(q*k/dk)*v
        """
        p = torch.mm(q, k)
        dim = q.shape[0]
        sa = torch.mm(F.softmax(p/torch.sqrt(dim)), v)
        return sa

    def forward(self, x):
        """
            前向过程
            x: 输入文本
        """
        # 分词
        self.x_token = tiktoken.tokenize(x)
        self.embdding = torch.nn.embedding(self.x_token, self.vocab_size, self.dim)
        for i in range(self.head_num):
            self.multi_attention_block.append(self.selfAttention(x))
        
        return 1
        
        





