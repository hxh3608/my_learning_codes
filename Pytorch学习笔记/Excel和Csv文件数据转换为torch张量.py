#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : Excel和Csv文件数据转换为torch张量.py
# Author            : hxh
# Date              : 01.08.2022
# Last Modified Date: 01.08.2022
# Last Modified By  : hxh

import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd


# 自定义Dataset,实现三个方法：init,len,getitem
class ExcelDataset(Dataset):
    # init方法用于加载数据，以及定义一些属性
    def __init__(self, filepath="data.xlsx", sheet_name=0):
        # 打印日志
        print(f"reading{filepath},sheet={sheet_name}")

        # 读取文件，返回的是DataFrame
        # header=0表示不读取表头，index_col=0表示不读取第一列,names表示需要哪些列，dtype表示读取数据后希望元素是什么数据类型
        df = pd.read_excel(filepath, header=0, index_col=0,
                           names=['feat1', 'feat2', 'label'],
                           sheet_name=sheet_name,
                           dtype={"feat1": np.float32, "feat2": np.float32, "label": np.int})

        print(f"The shape of DataFrame is {df.shape}")

        feat = df.iloc[:, :2].values  # 特征
        label = df.iloc[:, 2].values  # 标签

        self.x = torch.from_numpy(feat)  # 借助torch.from_numpy将特征转为torch 张量
        self.y = torch.from_numpy(label)  # 借助torch.from_numpy将标签转为torch 张量

    def __len__(self):
        return len(self.y)  # 返回数据总行数

    def __getitem__(self, index):
        return self.x[index], self.y[index]  # 根据索引返回对应张量

class CsvDataset(Dataset):

    def __init__(self,filepath="data.csv"): # 在csv文件中没有sheet_name一说

        print(f"reading {filepath}")

        df = pd.read_csv(filepath,header=0,index_col=0,
                         encoding='utf-8',
                         names=["feat1","feat2","label"],
                         dtype={"feat1":np.float32,"feat2":np.float32,"label":np.int32},
                         skip_blank_lines=True)

        print(f"The shape of DataFrame is {df.shape}")

        feat = df.iloc[:,:2].values
        label = df.iloc[:,:2].values

        self.x = torch.from_numpy(feat)
        self.y = torch.from_numpy(label)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, index):
        return self.x[index],self.y[index] # 返回这样的一个元组

# 将csv文件视为文本数据来读取
class Csv2Dataset(Dataset):

    def __init__(self,filepath="data.csv"):

        print(f"reading {filepath}")

        # 采用上下文来处理
        with open(filepath,encoding="utf-8") as f:
            lines = f.readlines() # 读取多行，返回的是列表

        feat = []
        label = []
        for line in lines[1:]: # 第一行（0）是表头
            values = line.strip().split(",")
            row_feat = [float(v) for v in values[1:3]] # 列表
            row_label = int(values[3]) # 标签（整型数字）

            feat.append(row_feat)
            label.append(row_label)
        # 列表转换为numpy数组
        feat = np.array(feat,dtype=np.float32)
        label = np.array(label,dtype=np.int32)

        self.x = torch.from_numpy(feat)
        self.y = torch.from_numpy(label)


    def __len__(self):
        return len(self.y)

    def __getitem__(self, index):
        return self.x[index].self.y[index]

if __name__ == "__main__":

    print("======Test for ExcelDataset======")
    excel_dataset = ExcelDataset(sheet_name="corpus1") # 实例化,指定具体哪个sheet
    # excel_dataset = ExcelDataset(sheet_name="corpus2") # 实例化,指定具体哪个sheet
    # excel_dataset = ExcelDataset() # 实例化,不指定具体哪个sheet，那返回的就是字典，其中键为sheet的名称
    excel_dataloader = DataLoader(excel_dataset,batch_size=8,shuffle=True) # 将实例化之后的dataset转入DataLoader

    for idx,(batch_x,batch_y) in enumerate(excel_dataloader):
        print(f"batch_id:{idx},{batch_x.shape},{batch_y.shape}")
        print(batch_x,batch_y)

    # 以下是伪代码，即获取数据后进行优化更新
    # output = model(batch_x)
    # loss = criterion(output,batch_y)
    # optimizer.zero_grad()
    # loss.backward()
    # optimizer.step()

    print("======Test for CsvDataset======")
    csv_dataset = CsvDataset()  # 实例化
    csv_dataloader = DataLoader(csv_dataset, batch_size=8, shuffle=True)  # 将实例化之后的dataset转入DataLoader

    for idx, (batch_x, batch_y) in enumerate(csv_dataloader):
        print(f"batch_id:{idx},{batch_x.shape},{batch_y.shape}")
        print(batch_x, batch_y)

    print("======Test for Csv2Dataset======")
    csv2_dataset = Csv2Dataset()  # 实例化
    csv2_dataloader = DataLoader(csv2_dataset, batch_size=8, shuffle=True)  # 将实例化之后的dataset转入DataLoader

    for idx, (batch_x, batch_y) in enumerate(csv2_dataloader):
        print(f"batch_id:{idx},{batch_x.shape},{batch_y.shape}")
        print(batch_x, batch_y)


