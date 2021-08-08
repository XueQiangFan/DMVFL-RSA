#!/Users/11834/.conda/envs/Pytorch_GPU/python.exe
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File    ：FWorks -> processefiles
@IDE    ：PyCharm
@Date   ：2020/12/6 14:48
=================================================='''
import numpy as np
import re
from numba import jit

aa_dictionary = {
    'A': 0,
    'B': 20,
    'C': 1,
    'D': 2,
    'E': 3,

    'F': 4,
    'G': 5,
    'H': 6,
    'I': 7,
    'J': 20,

    'K': 8,
    'L': 9,
    'M': 10,
    'N': 11,
    'O': 20,

    'P': 12,
    'Q': 13,
    'R': 14,
    'S': 15,
    'T': 16,
    'U': 20,

    'V': 17,
    'W': 18,
    'X': 20,
    'Y': 19,
    'Z': 20,
    '-': 20,
}
ASA_dictionary = {

    'A': 115,
    'C': 135,
    'D': 150,
    'E': 190,
    'F': 210,
    'G': 75,
    'H': 195,
    'I': 175,
    'K': 200,
    'L': 170,
    'M': 185,
    'N': 160,
    'P': 145,
    'Q': 180,
    'R': 225,
    'S': 115,
    'T': 140,
    'V': 155,
    'W': 255,
    'Y': 230,
}


class Processing_PSSM_MSAToPSFM:

    def readPSSMFileByPSIBLAST(self,pssm_path):
        f = open(pssm_path)
        f.readline()
        f.readline()
        f.readline()
        line = f.readline()
        PSSM = np.zeros((0, 20))
        while len(line) != 0:
            line = line.split(" ")
            while "" in line: line.remove("")
            lineinfo = np.array(line[2:22], np.float)
            probs = [round(1 / ((np.exp(-lineinfo[i])) + 1), 3) if lineinfo[i] != '*' else 0. for i in range(20)]
            PSSM = np.concatenate((PSSM, np.matrix(probs)), axis=0)
            line = f.readline().strip()
        f.close()
        return PSSM

    def a3mToMSA(self, msa_path):
        with open(msa_path, 'r') as f:
            lines = f.readlines()
        lines = filter(lambda x: '>' not in x, lines)
        msa = [re.sub(r'[a-z''\n]', '', x) for x in lines]
        return msa

    @jit
    def transferMSA(self,msa_path):
        msa = self.a3mToMSA(msa_path)
        N = len(msa)
        L = len(msa[0])
        numeric_msa = np.zeros([N, L], dtype=int)
        for i in range(N):
            aline = msa[i]
            for j in range(L):
                numeric_msa[i, j] = aa_dictionary[aline[j]]
        return numeric_msa

    @jit
    def NumericMSAToPSFM(self,msa_path):
        numeric_msa = self.transferMSA(msa_path)
        N, pro_length = numeric_msa.shape
        PSFM = np.zeros((pro_length, 21))
        for i in range(pro_length):
            for j in range(0, 21):
                total = 0
                for k in range(N):
                    if j == numeric_msa[k, i]: total += 1
                PSFM[i, j] = int((total / N) * 1000) / 1000
        return PSFM

    def MAXASAValue(self, residue_type):
        return ASA_dictionary[residue_type]
