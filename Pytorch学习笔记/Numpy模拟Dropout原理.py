#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : Numpy模拟Dropout原理.py
# Author            : hxh
# Date              : 02.08.2022
# Last Modified Date: 02.08.2022
# Last Modified By  : hxh

import numpy as np

def train(rate,x,w1,b1,w2,b2): # rate表示实现多少dropout
    layer1 = np.maximum(0,np.dot(w1,x) + b1)
    # 生成mask矩阵,1-rate表示多少是有效的,layer1.shape表示矩阵大小
    mask1 = np.random.binomial(1,1-rate,layer1.shape)
    layer1 = layer1 * mask1

    layer2 = np.maximum(0, np.dot(w2, layer1) + b2)
    # 生成mask矩阵,1-rate表示多少是有效的,layer1.shape表示矩阵大小
    mask2 = np.random.binomial(1, 1 - rate, layer2.shape)
    layer2 = layer2 * mask2
    return layer2


def another_train(rate,x,w1,b1,w2,b2):
    layer1 = np.maximum(0, np.dot(w1, x) + b1)
    # 生成mask矩阵,1-rate表示多少是有效的,layer1.shape表示矩阵大小
    mask1 = np.random.binomial(1, 1 - rate, layer1.shape)
    layer1 = layer1 * mask1
    layer1 = layer1 / (1-rate) # 这样就使得训练时复杂，但测试就简单了

    layer2 = np.maximum(0, np.dot(w2, layer1) + b2)
    # 生成mask矩阵,1-rate表示多少是有效的,layer1.shape表示矩阵大小
    mask2 = np.random.binomial(1, 1 - rate, layer2.shape)
    layer2 = layer2 * mask2
    layer2 = layer2 / (1-rate)

    return layer2

def test(rate,x,w1,b1,w2,b2):
    layer1 = np.maximum(0, np.dot(w1, x) + b1)
    layer1 = layer1 * (1-rate) # 这样就使得测试时也复杂了点

    layer2 = np.maximum(0, np.dot(w2, layer1) + b2)
    layer2 = layer2 * (1-rate)

    return layer2


def another_test(x,w1,b1,w2,b2):
    layer1 = np.maximum(0, np.dot(w1, x) + b1)
    layer2 = np.maximum(0, np.dot(w2, layer1) + b2)

    return layer2