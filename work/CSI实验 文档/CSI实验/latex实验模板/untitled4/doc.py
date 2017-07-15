#coding=utf-8
import re
import os
import codecs
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_image_list(file_dir): #从目录中获取所有的图片文件名
    list=[]
    for file in os.listdir(file_dir):
        pattern=re.compile("[^.]+\.(png|jpg|bmp|eps)")
        if os.path.isdir(file_dir+'/'+file):
            pass
        else:
            if pattern.match(file):
                list.append(file)
    return list    #此时返回的是列表　元素是图片的名字


def csv_read(path):
    #读取csv内容
    try:
        with open(path,'r') as csv_file:
            reader=csv.DictReader(csv_file)
            data=[]
            for info in reader:
                data.append(info)
            return data
    except IOError:
        print "File open error : " + path + "\nplease check the filename"
        return []



def get_csv_list(path):

    '''有效的csv文件名　必须是编号 + &&& + 文件描述　+ .csv
    例如 1&&&测试文件.csv
        222&&&测试文件.csv

    '''
    csv_list = []
    for fpathe, dirs, fs in os.walk(path):
        for f in fs:
            path=os.path.join(fpathe, f)
            filename=path.split('/')[-1]
            format=re.compile(r'^[\d]+[_]{3}.+\.csv$')
            if format.match(filename):
                csv_list.append(path)

    if not csv_list:
        print 'CSV files that do not meet requirements !'
        return []

    csv_info={}
    for file in csv_list:
        filename=file.split('/')[-1]
        key=filename.split('___')[0]          #以文件的编号为主键
        csv_info[key]={}                      #向该键添加信息
        csv_info[key]['FileDescription']=filename.split('___')[1][:-4]  #FileDescription表示此文件的描述
        csv_info[key]['FileInfo']=csv_read(file)  #此文件的内容　字典的形式
        if  not csv_read(file):
            csv_info.pop(key)

    return csv_info #返回的是所有csv文件的内容　一个编号对应一个csv文件的所有信息


def image_insert_label(image,file_path):  #返回以图像名为键标签信息为值的字典


    '''此函数用来从文本中读取图片的描述信息
    以文件名为主键　把图片对应的标签赋值给主键
    '''

    if(os.path.isdir(file_path)):
        print '不能打开目录'
        return None

    list={}
    count = 0
    try:
        file=open(file_path,"r")

        for line in file:
            if count < len(image):

                if  line.strip('\n')!= "":
                    list[image[count]]=line.strip('\r\n')

                else:
                    raise Exception("标签不足")

            else:
                raise Exception("图像数量不足")

            count=count+1

    except IOError:
        print '文件不存在,退出程序'
        exit(0)

    return list


def tex_header_file(): #把得到的图片和标签写入tex文件

    '''

    这个是tex文件的标准格式　若需要修改则从此处手动修改　
    '''

    tex=r'''\documentclass{article}
\usepackage{graphicx} 
\usepackage[version=3]{mhchem} 
\usepackage{CJKutf8}
\usepackage{multirow}
\usepackage{ulem}
\usepackage{indentfirst}
\usepackage{amsmath}
\renewcommand{\labelenumi}{\alph{enumi}.} 
\title{Determination of the Atomic \\ Weight of Magnesium \\ CHEM 101} % Title

\author{John \textsc{Smith}} % Author name

\date{\today} % Date for the report
\begin{document}
\begin{CJK}{UTF8}{gbsn}

\maketitle % Insert the title, author and date


\begin{center}    %　tabular 控制表格　打印　左对齐　右对齐
\begin{tabular}{l r}
Date Performed: & January 1, 2012 \\ % Date the experiment was performed
Partners: & James Smith \\ % Partner names
& Mary Smith \\
Instructor: & Professor Smith % Instructor/supervisor
\end{tabular}
\end{center}


\section{实验原理} 
\subsection{工具}
\Large
\CJKindent csi \CJKindent tool


\subsection{工作原理}
\large
发送端使用笔记本天线发送数据块，接收端使用天线接收数据块，并计算信噪比，根据信噪比的变化判断实验对象的部分性质。

\subsection{数据块组成}
\large
每块数据有3根天线，在30个信道的信噪记录。

\subsection{实验方式}
\large
以0.5秒的间隔发送360个数据块。

\subsection{绘图数据构造设计}
\large
每根天线的数据中，将信道做X轴，数据块编号做Y轴，以对应的信噪做Z轴。每次实验可得到三个不同天线接收的数据绘制的图像。本次实验使用了定向天线，替换原一号天线。

\subsection{绘图方法}
\large
详见matlab使用说明

\section{实验目的}
\large
测量湿度对csi信号的影响。

\section{实验计划}
\begin{description}
	\item[时间:]~~~~~2017年6月20日
	\item[地点:]~~~~~6236实验台
	\item[试验场景:]
	\item[]
	\includegraphics[width=16cm,height=8cm]{a.jpg}
        \begin{center}
    图：environment.png
    \end{center}	

\item[实验器材:]~~~~~带有定向天线，安装有csi 工具的两台笔记本电脑。
\item[定向天线中心距离:]~~~~~66cm
\item[实验材料:]~~~~~模拟麦堆
\item[实验变量:]~~~~~湿度。
\item[实验范围:]~~~~~0~～５００$g$(纯净水)
\item[实验方式:]~~~~~麦堆中每次添加100g水，搅拌均匀，将定向天线相距66cm，放置于麦堆两侧，开始测试，保存数据。详细的变量与数据包的对应关系，见“变量与数据记录对照表”。
\end{description}

\section{注释}
XXXXXXXXXXXXXXXXXXXXXX
'''
    tex=tex.split('\n')

    return tex

def tex_creat(image_label_list,list_lable_list,tex_head_file):

    tex_head_file.append(r"\begin{description}")#添加附件

    '''先添加变量与数据对照表'''
    tex_head_file.append(r'\newpage')
    tex_head_file.append(r"\item[变量与数据对照表] ~\\")#添加附件

    keys=sorted(list_lable_list.keys(),key=int)   #添加表格
    for key in keys:
        tex_head_file.append(r"\begin{table}[h]")#添加附件
        tex_head_file.append(r'\caption{}')
        tex_head_file.append(r'\begin{center}')
        tex_head_file.append(r"\begin{tabular}{|c|c|}")
        tex_head_file.append(r"\hline")
        tex_head_file.append(r'~~~~~~~~~~~~~~~变量 ~~~~~~~~~~~~~~~& ~~~~~~~~~~~~~~~数据包 ~~~~~~~~~~~~~~~\\')
        tex_head_file.append(r"\hline")
        for line in list_lable_list[key]['FileInfo']:
            tex_head_file.append(line['Variable']+"&"+line['DataPacket']+r"\\")
            tex_head_file.append(r"\hline")

        tex_head_file.append(r"\end{tabular}")
        tex_head_file.append(r'\end{center}')
        tex_head_file.append(r'~~~~~~~~~~~'+list_lable_list[key]['FileDescription'])
        tex_head_file.append(r'\end{table}')
        tex_head_file.append(r'~\\')
        tex_head_file.append(' ')

    def Len(string):
        num=0
        for s in string:
            num=num+ord(s)
        return num

    image_table = sorted(image_label_list.keys(),key=Len)

    count =0
    for image in image_table:    #添加图片
        tex_head_file.append(r"\begin{figure}[h]")
        if count ==0:
            tex_head_file.append(r"\LARGE 附页１")
        tex_head_file.append(r"\begin{center}")
        tex_head_file.append(r"\includegraphics[width=1.2\textwidth]{"+image+"}")
        tex_head_file.append(r"\caption{"+image_label_list[image]+'}')
        tex_head_file.append(r"\end{center}")
        tex_head_file.append(r"\end{figure}")
        count=count+1

    tex_head_file.append(r"\end{description}")
    tex_head_file.append(r"\end{CJK}")
    tex_head_file.append(r"\end{document}")
    return tex_head_file

def write_tex(tex_list,filename):  #写入生成好的tex文件
    try:
        file=codecs.open(filename,'w',"utf8")

        for line in tex_list:

            file.write(line+'\n')

        file.close()

    except IOError:
        print 'IO异常无法打开文件'
        exit(0)



if __name__=="__main__":
    image=get_image_list("./文本_图片/pc") #得到所有的图片名
    image2 =image_insert_label(image,"./文本_图片/take_pc_plan.txt") #返回一个以图像名为键　标签的为值的字典
    table_label=get_csv_list('./文本_图片/csv_home')
    head=tex_header_file()
    tex= tex_creat(image2,table_label,head)
    write_tex(tex,'./文本_图片/pc/object.tex')
