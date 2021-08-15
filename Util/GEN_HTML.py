#!/Users/11834/.conda/envs/Pytorch_GPU/python.exe
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File    ：FWorks -> GEN_HTML
@IDE    ：PyCharm
@Date   ：2021/1/15 19:19
=================================================='''
import matplotlib.pyplot as plt
import os
import numpy as np
class GEN_HTML:
    def __init__(self, pro_name, result_path):
        self.file_path = os.path.join(result_path, pro_name+".rsa")
        self.pro_name = pro_name
        self.html_name = "results"+".html"
        self.html_path = os.path.join(result_path, self.html_name)
        self.img_name = pro_name+".png"
        self.img_path = os.path.join(result_path, self.img_name)

    def visualization_RSA_result(self):
        SPRSA = np.genfromtxt(self.file_path,skip_header=3,skip_footer=1, dtype=str)
        SPRSA = np.array(SPRSA[:,2],dtype=float)

        """draw picture"""
        plt.rcParams['font.sans-serif'] = 'Times New Roman'
        plt.rcParams['savefig.dpi'] = 200  # 图片像素
        plt.rcParams['figure.dpi'] = 200
        plt.figure(1,figsize=(6,1.2))
        x = np.zeros(SPRSA.shape[0])
        for i in range(SPRSA.shape[0]):
            x[i] = int(i + 1)
        ax = plt.subplot(111)
        ax.grid(True, linestyle=':')
        plt.plot(x, SPRSA, linewidth=0.5, linestyle="-",color="blueviolet",)
        plt.xlabel('Residue index', fontsize=7)
        plt.ylabel('DMVFL-RSA predicted RSA', fontsize=7)
        x_ticks = np.arange(0, SPRSA.shape[0], 5)
        y_ticks = np.arange(0, 1, 0.2)
        plt.xticks(x_ticks, fontsize=6)
        plt.yticks(y_ticks, fontsize=6)
        plt.xlim(xmax=SPRSA.shape[0]+1, xmin=0)
        plt.ylim(ymax=1.05, ymin=-0.05)
        plt.tick_params(direction="in",width=0.5, length=2.5,top=True,right=True)
        # plt.legend(fontsize="xx-small")
        bwith = 0.5  # 边框宽度设置为2
        TK = plt.gca()  # 获取边框
        TK.spines['bottom'].set_linewidth(bwith)  # 图框下边
        TK.spines['left'].set_linewidth(bwith)  # 图框左边
        TK.spines['top'].set_linewidth(bwith)  # 图框上边
        TK.spines['right'].set_linewidth(bwith)  # 图框右边
        plt.savefig(self.img_path,dpi=300,bbox_inches='tight')
        # plt.show()


    def generate_html(self):
        self.visualization_RSA_result()
        SPRSA = np.genfromtxt(self.file_path, skip_header=3, skip_footer=1, dtype=str)
        index = SPRSA[:,0]
        base = SPRSA[:,1]
        RSA = SPRSA[:,2]
        ASA = SPRSA[:,3]
        fw = open(self.html_path , "w")
        fw.write('''\n''')
        fw.write("<html>\n")
        fw.write('''<body bgcolor="#F0FFFF">\n''')
        fw.write("<br/>\n")
        fw.write('''<body bgcolor="#F0FFFF">\n''')
        fw.write('''<table border="0" style="table-layout:fixed;" width="100%" cellpadding="2" cellspaceing="0">\n''')
        fw.write('''<tr><td>\n''')
        title = '''  <h1 align="center">DMVFL-RSA result for '''+self.pro_name+'''</h1>\n'''
        fw.write(title)
        fw.write('''  <tr><td>\n''')
        fw.write('''   <br/>\n''')
        fw.write('''   <div style="background:#6495FF;width:450px;">\n''')
        fw.write('''   <table><tr><td valign="middle">\n''')
        fw.write('''   <font color="#FFFFFF" size="4" face="Arial">&nbsp;&nbsp;Predicted Solvent Accessibility</font>\n''')
        fw.write('''   </td></tr></table>\n''')
        fw.write('''   </div>\n''')
        fw.write('''<tr><td></td></tr>\n''')
        fw.write('''<tr><td></td></tr>\n''')
        fw.write('''<tr><td>\n''')
        fw.write('''<h3 align=left><u>Visualization</u></h3>\n''')
        fw.write('''</td></tr>\n''')
        fw.write('''<table  border="0" width="600" style="margin-left:10px;font-family:Monospace;font-size:15px;background:#F2F2F2;table-layout :fixed;">\n''')
        fw.write('''<tr><td>\n''')
        fw.write('''<left>\n''')
        img = "<img src=" + ".\\" + self.pro_name + ".png" + " border=1 width=600>"
        fw.write(img+"\n")
        fw.write('''</left>\n''')
        fw.write('''</td></tr>\n''')
        fw.write('''</table>\n''')
        fw.write('''<tr><td>\n''')
        fw.write('''<h3 align=left><u>Detailed results</u></h3>\n''')
        fw.write('''</td></tr>\n''')
        fw.write('''   <div style="position:relative;left:10px;">\n''')
        fw.write('''   <table style="font-family:Arial;font-size:14px;margin-left:10px;">\n''')
        fw.write('''<tr><td><b><i>No.</i></b> is the position of each residue in your protein. </td><tr>\n''')
        fw.write('''<tr><td><b><i>AA</i></b> is the name of each residue in your protein. </td></tr>\n''')
        fw.write('''   <tr><td><b><i>RSA</i></b> is the predicted relative accessible surface area of each residue in your protein.</td><tr>\n''')
        fw.write('''   <tr><td><b><i>ASA</i></b> is the predicted accessible surface area of each residue in your protein.</td><tr>\n''')
        fw.write('''</table>\n''')
        fw.write('''<br/>\n''')
        fw.write('''   <table  border="0" width="20%" style="margin-left:10px;font-family:Monospace;font-size:14px;background:#F2F2F2;table-layout :fixed;">\n''')
        fw.write('''    <tr> <td style="width: 30%;"><b>No.</b></td> <td style="width: 30%;"><b>AA</b></td> <td style="width: 40%;"><b>RSA</b></td> <td style="width: 40%;"><b>ASA</b></td></tr>\n''')
        for i in range(index.shape[0]):
            info = '''    <tr >  <td style="width: 2%;">'''+index[i]+'''</td> <td style="width: 3%;">'''+base[i]+'''</td><td style="width: 3%;">'''+RSA[i]+'''</td><td style="width: 3%;">'''+ASA[i]+'''</td></tr>'''
            fw.write(info+"\n")
        
        fw.write(result)
        fw.write('''    </table>\n''')
        fw.write('''  </div>\n''')
        fw.write('''</td></tr>\n''')
        fw.write('''<tr><td><br/></td></tr>\n''')
        fw.write('''<tr><td>\n''')
        fw.write('''<hr><br/>\n''')
        fw.write('''<div style="position:relative;left:5px;"><table style="font-family:Arial;font-size:14px;"><tr><td colspan=2>Please cite the following article when you use the DMVFL-RSA server: Improved Protein Relative Solvent Accessibility Prediction using Deep Multi-View Feature Learning Framework</td><tr>\n''')
        fw.write('''<tr><td valign="top"></td><td> <li>Xue-Qiang Fan, Jun Hu, Ning-Xin Jia, Dong-Jun Yu, Gui-Jun Zhang</td></tr>\n''')
        fw.write('''</table></div></td></tr>\n''')
        fw.write('''</table></body>\n''')
        fw.write('''</html>\n''')
        fw.close()
        # webbrowser.open(self.html_name, new=1)



# if __name__ == '__main__':
#     path = r"E:\Protein Solvent accessibility\DMVFL_RSA\DMVFL_RSA\example\1bfmB.rsa"
#     generate_html = GEN_HTML(path)
#     generate_html.visualization_RSA_result()
#     generate_html.generate_html()
