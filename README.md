# DMVFL-RSA
Improved Protein Relative Solvent Accessibility Prediction Using Deep Multi-View Feature Learning Framework

## Pre-requisite:
    - Linux system
    - python3.7 
    - pytorch(version 1.3.1) (https://pytorch.org/)
    - HHblit (shttps://toolkit.tuebingen.mpg.de/tools/hhblits)
    - uniclust30_2018_08 (http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/)
    - blast-2.2.26 (https://blast.ncbi.nlm.nih.gov/Blast.cgi)
    - nr(https://ftp.ncbi.nih.gov/blast/db/)
    - PSIPRED(PSIPRED V3.2) (http://bioinfadmin.cs.ucl.ac.uk/downloads/psipred/)

## Installation:

*Install and configure the softwares of Python3, Java, Pytorch, HHblits, uniclust30_2018_08, blast-2.2.26, nr, ProtChain database, and PSIPRED in your Linux system. Please make sure that python3.7 includes the modules of 'os', 'math', 'numpy', 'configparser', 'numba', 'random', 'subprocess', 'sys', and 'shutil'. If any one modules does not exist, please using 'pip install xxx' command install the python revelant module. Here, "xxx" is one module name.

*Download this repository at https://github.com/XueQiangFan/DMVFL-RSA. Then, uncompress it and run the following command lines on Linux System.

~~~
  $ unzip DMVFL-RSA.zip  
  $ chmod -R 777 ./DMVFL-RSA
  $ cd ./DMVFL-RSA/Util/
  $ chmod -R 777 ./database
  $ java -jar FileUnion.jar ./database/ ./database.zip
  $ rm -rf ./database
  $ unzip ./database.zip 
   $ cd ../
~~~
  Here, you will see two configuration files 

*Configure the following tools or databases in Config.properties  
  The file of "Config.properties" should be set as follows:
 - HHblits
 - uniclust30_2018_08
 - blast+ 
 - nr
 - PSIPRED
 - ProtChain databases
 For example:
 ~~~
  # Generate PSSM PSS config path
  BLASTPGP_EXE_PATH=/data0/junh/software/blast-2.2.26/blastpgp
  BLASTPGP_DB_PATH=/data/commonuser/library/nr/nr
  PSIPRED321_FOLDER_DIR=/data0/junh/software/psipred321/
  BLAST_BIN_DIR=/data0/junh/software/blast-2.2.26/
  HHBLITS_EXE_PATH=hhblits
  HHBLITS_DB_PATH=/data/commonuser/library/uniclust30_2018_08/uniclust30_2018_08
  # Generate RPRSA config 
  PROT_CHAIN_LIB_FOLDER_PATH=/data0/junh/stu/xueqiangf/SPRSA/Util/ProtChain
 ~~~
 
*Configure the following tools or databases in DMVFL-RSA.config  
  The file of "Config.properties" should be set as follows:
- HHblits 
- uniclust30_2018_08
 For example:
 ~~~
   [HHBLITS]
   HHBLITS_EXE = hhblits
   HHBLITS_DB = /data/commonuser/library/uniclust30_2018_08/uniclust30_2018_08
 ~~~

## Run DMVFL-RSA? 

### run: python main.py -p protein name -S protein sequence -o result path

Brief introduction for protein solvent accessibility prediction by DMVFL-RSA

Step 0. generate an MSA (in a3m format) for your protein sequence from HHblits.

Step 1. generate one PSFM profile for your the MSA

Step 2. generate one PSSM profile and a PSS profile for your protein sequence from blast+ and PSIPRED.

Step 3. generate one RPRSA profile for your protein sequence from RPRSA-Threader

Step 4.  protein name +.rsa is the result file

## The protein solvent accessibility result

*The protein solvent accessibility result of each rsidue should be found in the outputted file, i.e., " protein name +.rsa". In each result file, where "NO" is the position of each residue in your protein, where "AA" is the name of each residue in your protein, where "RSA" is the predicted relative accessible surface area of each residue in your protein, and where "ASA" is the predicted accessible surface area of each residue in your protein.

## Update History:

First release 2021-08-03

## References

[1] Xue-Qiang Fan, Jun Hu*, Ning-Xin Jia, Dong-Jun Yu*, and Gui-Jun Zhang*. Improved Protein Relative Solvent Accessibility Prediction using Deep Multi-View Feature Learning Framework. Analytical Biochemistry. sumitted.

