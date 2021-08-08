#!/Users/11834/.conda/envs/Pytorch_GPU/python.exe
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File    ：FWorks -> feature_extraction
@IDE    ：PyCharm
@Date   ：2020/12/6 10:45
=================================================='''
import os
import numpy as np
from numba import jit
from Util.processing_pssm_msaTopsfm import Processing_PSSM_MSAToPSFM

class PSSMPSFMPSSPRSAGetWindowPadheadfoot():

    def __init__(self, pro_name:str, result_dir, win_size=15):
        super(PSSMPSFMPSSPRSAGetWindowPadheadfoot, self).__init__()
        self.pro_name = pro_name
        self.fa_path = os.path.join(result_dir, pro_name)
        self.result_dir = result_dir
        self.pssm_path = os.path.join(self.result_dir,self.pro_name+".opssm")
        self.psfm_path = os.path.join(self.result_dir,self.pro_name+".psfm")
        self.pss_path = os.path.join(self.result_dir,self.pro_name+".ss")
        self.jpsfm_path = os.path.join(self.result_dir,self.pro_name + ".temples.sa")
        self.win_size = win_size
        self.stride = int(win_size / 2)

    @jit
    def getIthProteinLen(self):
        seq = np.loadtxt(self.fa_path, dtype=str)[1]
        pro_length = len(seq)
        return pro_length


    @jit
    def feature(self):
        pro_length = self.getIthProteinLen()
        PSSM = Processing_PSSM_MSAToPSFM()
        pssm = PSSM.readPSSMFileByPSIBLAST(self.pssm_path)
        psfm = np.loadtxt(self.psfm_path)[:, :20]
        pss = np.loadtxt(self.pss_path, dtype=str)[:, 3:]
        pss = np.array(pss, dtype=np.float)
        jpsfm = np.loadtxt(self.jpsfm_path, dtype=str)[:, 3:]
        jpsfm = np.array(jpsfm, dtype=np.float)

        pro_length, fea_num_pssm = pssm.shape
        paddingheader = pssm[:self.stride, :]
        paddingfooter = pssm[-self.stride:, :]
        pssm = np.append(paddingheader, pssm, axis=0)
        pssm = np.append(pssm, paddingfooter, axis=0)

        pro_length, fea_num_psfm = psfm.shape
        paddingheader = psfm[:self.stride, :]
        paddingfooter = psfm[-self.stride:, :]
        psfm = np.append(paddingheader, psfm, axis=0)
        psfm = np.append(psfm, paddingfooter, axis=0)

        pro_length, fea_num_pss = pss.shape
        paddingheader = pss[:self.stride, :]
        paddingfooter = pss[-self.stride:, :]
        pss = np.append(paddingheader, pss, axis=0)
        pss = np.append(pss, paddingfooter, axis=0)

        pro_length, fea_num_jpsfm = jpsfm.shape
        paddingheader = jpsfm[:self.stride, :]
        paddingfooter = jpsfm[-self.stride:, :]
        jpsfm = np.append(paddingheader, jpsfm, axis=0)
        jpsfm = np.append(jpsfm, paddingfooter, axis=0)
        label = np.zeros((pro_length, 1))
        feature_pssm = np.zeros((pro_length, self.win_size * fea_num_pssm))
        feature_psfm = np.zeros((pro_length, self.win_size * fea_num_psfm))
        feature_pss = np.zeros((pro_length, self.win_size * fea_num_pss))
        feature_jpsfm = np.zeros((pro_length, self.win_size * fea_num_jpsfm))

        feature_pssm_reverse = np.zeros((pro_length, self.win_size * fea_num_pssm))
        feature_psfm_reverse = np.zeros((pro_length, self.win_size * fea_num_psfm))
        feature_pss_reverse = np.zeros((pro_length, self.win_size * fea_num_pss))
        feature_jpsfm_reverse = np.zeros((pro_length, self.win_size * fea_num_jpsfm))

        for i in range(self.stride, pro_length + self.stride):
            feature_pssm[i - self.stride, :] = pssm[i - self.stride:i + self.stride + 1, :].flatten()
            feature_psfm[i - self.stride, :] = psfm[i - self.stride:i + self.stride + 1, :].flatten()
            feature_pss[i - self.stride, :] = pss[i - self.stride:i + self.stride + 1, :].flatten()
            feature_jpsfm[i - self.stride, :] = jpsfm[i - self.stride:i + self.stride + 1, :].flatten()

            feature_pssm_reverse[i - self.stride, :] = pssm[i - self.stride:i + self.stride + 1, :].flatten()
            feature_psfm_reverse[i - self.stride, :] = psfm[i - self.stride:i + self.stride + 1, :].flatten()
            feature_pss_reverse[i - self.stride, :] = pss[i - self.stride:i + self.stride + 1, :].flatten()
            feature_jpsfm_reverse[i - self.stride, :] = jpsfm[i - self.stride:i + self.stride + 1, :].flatten()

        feature_pssm_reverse, feature_psfm_reverse, feature_pss_reverse, feature_jpsfm_reverse = np.fliplr(
            feature_pssm_reverse), np.fliplr(feature_psfm_reverse), np.fliplr(feature_pss_reverse), np.fliplr(
            feature_jpsfm_reverse)
        feature_pssm_reverse, feature_psfm_reverse, feature_pss_reverse, feature_jpsfm_reverse = np.ascontiguousarray(
            feature_pssm_reverse), np.ascontiguousarray(feature_psfm_reverse), np.ascontiguousarray(
            feature_pss_reverse), np.ascontiguousarray(
            feature_jpsfm_reverse)
        sample = {'fea': (feature_pssm, feature_psfm, feature_pss, feature_jpsfm), 'fea_reverse': (
        feature_pssm_reverse, feature_psfm_reverse, feature_pss_reverse, feature_jpsfm_reverse),'protein': self.pro_name}  # construct the dictionary
        return sample

    @jit
    def getIthSampleFea(self):
        sample = self.feature()
        fea = sample['fea']
        fea_reverse = sample['fea_reverse']
        protein = sample['protein']
        return fea, fea_reverse, protein

# if __name__ == '__main__':
#     Data = PSSMPSFMPSSPRSAGetWindowPadheadfoot(r"C:\Users\11834\Desktop\result\1a0aB", r"C:\Users\11834\Desktop\result")
#     fea, fea_reverse, protein = Data.getIthSampleFea()
#     print(fea[0].shape)
