#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : Normalization.py
# Author            : hxh
# Date              : 03.08.2022
# Last Modified Date: 03.08.2022
# Last Modified By  : hxh


import torch
import torch.nn as nn


# 以NLP举例 batch_size * 序列长度 * 特征维度
batch_size = 2
time_steps = 3
embedding_dim = 4
num_groups= 2
input_x = torch.randn(batch_size,time_steps,embedding_dim) # N * L * C

# 1.实现batch_norm并验证API
# per channel，across，mini-batch
# NLP：[N,L,C] --> [C] 保持通道维度(per channel)
# CV：[N,C,H,W] --> [C]
## 调用batch_norm API
batch_norm_op = torch.nn.BatchNorm1d(embedding_dim,affine=False)
# 因为要求输入是 N * C * L，所以先变换，再换回来
bn_y = batch_norm_op(input_x.transpose(-1,-2)).transpose(-1,-2)

# 手写batch_norm
# 在batch_size维和序列长度维求均值（因为BN是按通道的，所以其他维求均值）
bn_mean = input_x.mean(dim=(0,1),keepdim=True) # 求完之后是C大小，然后用keepdim变回来
# 注意加上unbiased=False，因为要求是有偏估计
bn_std = input_x.std(dim=(0,1),unbiased=False,keepdim=True) # 求完之后是C大小，然后用keepdim变回来
verify_bn_y = (input_x - bn_mean)/(bn_std + 1e-5) # 1e-5 是eps
# print(bn_y)
# print(verify_bn_y)


# 2.实现layer_norm并验证API(per sample per layer)
# 输入的是特征维度
# NLP：[N,L,C] --> [N,L] 保持样本和layer维度
# CV：[N,C,H,W] --> [N,H,W]
## API
layer_norm_op = torch.nn.LayerNorm(embedding_dim,elementwise_affine=False)
ln_y = layer_norm_op(input_x)

## 手写
# 因为是per sample per layer，所以对最后一个维度进行mean
ln_mean = input_x.mean(dim=-1,keepdim=True)
ln_std = input_x.std(dim=-1,unbiased=False,keepdim=True)
verify_ln_y = (input_x - ln_mean)/(ln_std + 1e-5) # 1e-5 是eps
# print(ln_y)
# print(verify_ln_y)

# 3.实现instance_norm并验证API(per sample per channel)
# 输入的是特征维度
# NLP：[N,L,C] --> [N,C] 保持样本和channel维度
# CV：[N,C,H,W] --> [N,C]

## InstanceNorm1d API
instance_norm_op = torch.nn.InstanceNorm1d(embedding_dim)
in_y = instance_norm_op(input_x.transpose(-1,-2)).transpose(-1,-2) # 这个就看官方文档

## 手写 InstanceNor
# 因为是per sample per channel，所以返回的是 N * C，所以对第二个维度进行mean
in_mean = input_x.mean(dim=1,keepdim=True)
in_std = input_x.std(dim=1,unbiased=False,keepdim=True)
verify_in_y = (input_x - in_mean)/(in_std + 1e-5) # 1e-5 是eps
# print(in_y)
# print(verify_in_y)

# 4.实现group_norm并验证API(per sample per group)
# 输入的是特征维度
# NLP：[N,G,L,C//G] --> [N,G] 保持样本和group维度
# CV：[N,G,C//G,H,W] --> [N,G]
## API
group_norm_op = torch.nn.GroupNorm(num_groups,embedding_dim,affine=False)
gn_y = group_norm_op(input_x.transpose(-1,-2)).transpose(-1,-2) # 这个就看官方文档

# 手写group_norm
# 先把embedding_dim分割成两组
# 参数意思：对哪个数据分割，每一块大小，在这个数据上的哪一维进行分割
group_inputxs = torch.split(input_x,split_size_or_sections=embedding_dim // num_groups,dim=-1)
results = []
for g_input_x in group_inputxs:
    # 因为是per sample per group 所以在除了sample的那一维（即batch_size）进行mean
    gn_mean = g_input_x.mean(dim=(1,2),keepdim=True)
    # print(gn_mean.shape) # torch.Size([2, 1, 1])
    gn_std = g_input_x.std(dim=(1, 2), unbiased=False,keepdim=True)
    gn_result = (g_input_x - gn_mean)/(gn_std + 1e-5)
    # print(gn_result.shape) # torch.Size([2, 3, 2])
    results.append(gn_result) # 列表，里面有两个元素，每个元素是torch.Size([2, 3, 2])
verify_gn_y = torch.cat(results,dim=-1) # 在embedding_dim这个维度上将results列表中的两个tensor元素进行拼接，形成 N * L * C
# print(verify_gn_y.shape) # torch.Size([2, 3, 4])
# print(gn_y)
# print(verify_gn_y)

# 5.实现weight_norm并验证API
# 调用 weight_norm
# 因为实现weight_norm需要包裹module，所以选择最简单的线性层测试
linear = nn.Linear(embedding_dim,3,bias=False) # 未weight_norm的linear
wn_linear = torch.nn.utils.weight_norm(linear) # 进行weight_norm的linear
wn_linear_output = wn_linear(input_x)
# print(wn_linear_output.shape) # torch.Size([2, 3, 3])

# 手写实现 weight_norm
# 除以模不是指除以整个矩阵的模，而是除以跟每个sample做内积相乘的那个向量的模
# 因为是 X的每一行 与 W转置的每一列相乘 ，也就是W的每一行，因此是dim = 1（列顺序即行）
weight_direction = linear.weight / (linear.weight.norm(dim=1,keepdim=True))   # w = linear.weight，然后求出w的方向向量(w除以w的模)
weight_magnitude = wn_linear.weight_g # 幅度g
# print(weight_direction.shape) # torch.Size([3, 4])
# print(weight_magnitude.shape) # torch.Size([3, 1])
# 注意要做转置
verify_wn_linear_output = (input_x @ weight_direction.transpose(-1,-2)) \
                          * (weight_magnitude.transpose(-1,-2))
print(wn_linear_output)
print(verify_wn_linear_output)