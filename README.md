# DMVFL-RSA
DMVFL-RSA Predict Protein Solvent Accessibility

# 1.Prerequisite:
Configure the following tools or databases in Config.properties

Step 0. HHblits, uniclust30_2018_08  (http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/)

Step 1. blast+, nr  (https://ftp.ncbi.nih.gov/blast/db/)

Step 2. PSIPRED VFORMAT (PSIPRED V3.2)

Step 3. ProtChain databases (It can be downloaded from xxx) 

Step 4. python3.7, pytorch, numpy

Configure the following tools or databases in SPRSA.config
Step 0. HHblits, uniclust30_2018_08 

# 2.How to run DMVFL-RSA? 
Brief introduction for protein solvent accessibility prediction by DMVFL-RSA
Step 0. generate an MSA (in a3m format) for your protein sequence from HHblits.

Step 1. generate a PSSM and a PSS for your protein sequence from blast+ and PSIPRED.

Step 2. generate a RPRSA for your protein sequence from RPRSA-Threader

Step 3  xxx.rsa is the result file

## run: python main.py -p protein name -S protein sequence -o result path

More details about DMVFL-RSA can be found from the following paper:Improved Protein Relative Solvent Accessibility Prediction using Deep Multi-View Feature Learning Framework

Xueqiang Fan
2021.01
