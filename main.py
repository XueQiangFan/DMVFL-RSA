#!/Users/11834/.conda/envs/Pytorch_GPU/python.exe
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File    ：FWorks -> DMVFL_RSA
@IDE    ：PyCharm
@Date   ：2020/12/6 10:56
=================================================='''
import numpy as np
#from torch.autograd import Variable
import torch, os
from Util.feature_extraction import PSSMPSFMPSSPRSAGetWindowPadheadfoot
from BiLSTM_SE_Net import LSTMMergeSENet
from Util.processing_pssm_msaTopsfm import Processing_PSSM_MSAToPSFM
from Util.WriteFile import appendWrite
#from Util.GEN_HTML import GEN_HTML
#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
from Util.feature_generation import FeaturesGeneration
import warnings
warnings.filterwarnings('ignore')
#print(device)


def tester(pro_name, result_dir):
    fa_path = os.path.join(result_dir, pro_name)
    save_model = "./save_model/"
    model = LSTMMergeSENet()
    saved_model = save_model + 'epoch_' + str(50)
    model.load_state_dict(torch.load(saved_model,map_location="cpu"))
    optimizer = torch.optim.Adam(model.parameters())
    saved_model = save_model + 'epoch_' + str(50) + 'opt'
    optimizer.load_state_dict(torch.load(saved_model,map_location="cpu"))

    model.eval()
    with torch.no_grad():
        Data = PSSMPSFMPSSPRSAGetWindowPadheadfoot(pro_name, result_dir)
        fea, fea_reverse, protein = Data.getIthSampleFea()
        fea_pssm, fea_psfm, fea_pss, fea_jpsfm = torch.FloatTensor(fea[0]), torch.FloatTensor(
            fea[1]), torch.FloatTensor(fea[2]), torch.FloatTensor(fea[3])
        fea_pssm, fea_psfm, fea_pss, fea_jpsfm = torch.unsqueeze(fea_pssm, 0), torch.unsqueeze(fea_psfm,
                                                                                               0), torch.unsqueeze(
            fea_pss, 0), torch.unsqueeze(fea_jpsfm, 0)
#        fea_pssm, fea_psfm, fea_pss, fea_jpsfm = Variable(fea_pssm.float()), Variable(fea_psfm.float()).to(
#            device), Variable(fea_pss.float()).to(device), Variable(fea_jpsfm.float())

        fea_pssm_rev, fea_psfm_rev, fea_pss_rev, fea_jpsfm_rev = torch.FloatTensor(fea_reverse[0]), torch.FloatTensor(
            fea_reverse[1]), torch.FloatTensor(fea_reverse[2]), torch.FloatTensor(fea_reverse[3])
        fea_pssm_rev, fea_psfm_rev, fea_pss_rev, fea_jpsfm_rev = torch.unsqueeze(fea_pssm_rev, 0), torch.unsqueeze(
            fea_psfm_rev, 0), torch.unsqueeze(fea_pss_rev, 0), torch.unsqueeze(fea_jpsfm_rev, 0)
#       fea_pssm_rev, fea_psfm_rev, fea_pss_rev, fea_jpsfm_rev = Variable(fea_pssm_rev.float()).to(device), Variable(
#           fea_psfm_rev.float()).to(device), Variable(fea_pss_rev.float()).to(device), Variable(
#          fea_jpsfm_rev.float()).to(device)
        predict00 = model(fea_pssm, fea_psfm, fea_pss, fea_jpsfm)
        predict01 = model(fea_pssm_rev, fea_psfm_rev, fea_pss_rev, fea_jpsfm_rev)
        predict = (predict00[4] + predict01[4]) / 2

    
        seq = np.loadtxt(fa_path, dtype=str)[1]
        pro_length = len(seq)
        filename = protein + ".rsa"
        ASAValue = Processing_PSSM_MSAToPSFM()
        file_path = os.path.join(result_dir, filename)
        if os.path.exists(file_path):pass
        else:

            appendWrite(file_path, '{:>4}\n\n'.format("# DMVFL-RSA VFORMAT (DMVFL-RSA V1.0)"))
            appendWrite(file_path, '{:>1}  {:>1}  {:>4}  {:>4}\t\n'.format("NO.", "AA", "RSA", "ASA"))
            for i in range(pro_length):
                index, residue, RSA = i + 1, seq[i], predict[i, 0]
                SA = ASAValue.MAXASAValue(seq[i]) * predict[i, 0]
                appendWrite(file_path, '{:>4}  {:>1}  {:>.3f}  {:>.3f}\t\n'.format(index, residue, RSA, SA))
            appendWrite(file_path, '{:>8} \t'.format("END"))


def main():

    import argparse
    parser = argparse.ArgumentParser(description="DMVFL_RSA Predict Protein Solvent Accessibility")
    parser.add_argument("-p", "--pro_name", required=True, type=str, help="protein name")
    parser.add_argument("-s", "--sequence", required=True, type=str, help="AA sequence ")
    parser.add_argument("-o", "--result_path", required=True, type=str, help="save result path")
    args = parser.parse_args()
    features_generation = FeaturesGeneration(args.pro_name, args.sequence, args.result_path)
    features_generation.PSSM_PSS_generation()
    features_generation.PSFM_generation()
    features_generation.Threading_based_PRSA()
    tester(args.pro_name, args.result_path)
    gan_html = GEN_HTML(args.pro_name, args.result_path)
    gan_html.generate_html()

if __name__ == '__main__':
    main()

