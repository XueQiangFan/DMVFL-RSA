#!/Users/11834/.conda/envs/Pytorch_GPU/python.exe
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File    ：FWorks -> lossfunction
@IDE    ：PyCharm
@Date   ：2020/8/21 18:47
=================================================='''
# 仅限回归问题
import torch
# L2 损失
def MSELoss(predict, true):
    return torch.sum((true - predict)**2)
