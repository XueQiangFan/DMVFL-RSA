# SPRSA
SPRSA Predict Protein Solvent Accessibility

# 1.Prerequisite:
Configure the following tools or databases in Config.properties

Step 0. HHblits, uniclust30_2018_08 

Step 1. blast+, nr

Step 2. PSIPRED VFORMAT (PSIPRED V3.2)

Step 3. ProtChain databases (It can be downloaded from xxx)

Step 4. python3.7, pytorch, numpy

Configure the following tools or databases in SPRSA.config
Step 0. HHblits, uniclust30_2018_08 

# 2.How to run SPRSA? 
Brief introduction for protein solvent accessibility prediction by SPRSA
Step 0. generate an MSA (in a3m format) for your protein sequence from HHblits.

Step 1. generate a PSSM and a PSS for your protein sequence from blast+ and PSIPRED.

Step 2. generate a PRSA for your protein sequence from PRSA-Threader

Step 3  xxx.rsa is the result file

## run: python main.py -p fasta path -o result path

More details about SPRSA can be found from the following paper:xxx

Xueqiang Fan
2021.01
