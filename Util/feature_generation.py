#!/Users/11834/.conda/envs/Pytorch_GPU/python.exe
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File    ：FWorks -> feature_generation
@IDE    ：PyCharm
@Date   ：2020/12/6 21:20
=================================================='''
import os
import numpy as np
from configparser import ConfigParser
from Util.processing_pssm_msaTopsfm import Processing_PSSM_MSAToPSFM

config = ConfigParser()
config.read('DMVFL-RSA.config')
HHBLITS_EXE = config.get('HHBLITS', 'HHBLITS_EXE')
HHBLITS_DB = config.get('HHBLITS', 'HHBLITS_DB')


class FeaturesGeneration(object):
    def __init__(self, pro_name, sequence, result_path):
        seq_path = os.path.join(result_path, pro_name)
        with open(seq_path, "w") as f:
            f.write(">" + pro_name.strip() + "\n" + sequence.strip())
        self.seq_path = seq_path
        self.pro_name = pro_name.strip()
        self.seq = sequence.strip()
        self.result_path = result_path
        self.msa_path = os.path.join(self.result_path, self.pro_name + ".a3m")
        self.PSFM_path = os.path.join(self.result_path, self.pro_name + ".psfm")
        self.PRSA_path = os.path.join(self.result_path, self.pro_name + ".temples")
        self.PSS_path = os.path.join(self.result_path, self.pro_name + ".ss")
        self.PSSM_path = os.path.join(self.result_path, self.pro_name + ".opssm")

    def PSSM_PSS_generation(self):
        if os.path.exists(self.PSSM_path) and os.path.exists(self.PSSM_path):
            pass
        else:
            PSSM_PSS_cmd = "java -jar /Util/GeneratePSSM_PSS_PSA.jar " + self.result_path + " " + self.seq_path + " " + str(
                0) + " " + str(1)
            os.system(PSSM_PSS_cmd)
        return self.seq_path

    def msa_generation(self):
        msa_cmd = HHBLITS_EXE + ' -i ' + self.seq_path + ' -d ' + HHBLITS_DB + ' -n ' + str(5) + ' -e ' + str(
            0.1) + ' -cov ' + str(80) + ' -id ' + str(90) + ' -oa3m ' + self.msa_path
        os.system(msa_cmd)

    def PSFM_generation(self):
        if os.path.exists(self.PSFM_path):
            print("PSFM have existed!")
        elif os.path.exists(self.msa_path):
            print("MSA have existed!")
            MSAToPSFM = Processing_PSSM_MSAToPSFM()
            PSFM = MSAToPSFM.NumericMSAToPSFM(self.msa_path)
            np.savetxt(self.PSFM_path, PSFM, fmt='%.04f')
        else:
            self.msa_generation()
            MSAToPSFM = Processing_PSSM_MSAToPSFM()
            PSFM = MSAToPSFM.NumericMSAToPSFM(self.msa_path)
            np.savetxt(self.PSFM_path, PSFM, fmt='%.04f')

    def Threading_based_PRSA(self, cutoff_threshold=0.5, iter_num=1):

        PRSA_cmd = "java -jar /Util/JPSFMThreader.jar " + self.pro_name + " " + self.seq + " " + str(
            cutoff_threshold) + " " + str(iter_num) + " " + self.PSFM_path + " " + self.PRSA_path
        os.system(PRSA_cmd)
