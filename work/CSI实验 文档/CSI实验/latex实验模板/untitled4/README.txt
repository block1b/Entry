 
宏包下载地址　https://ctan.org/pkg/chemgreek
宏包安装方法　http://www.xuebuyuan.com/1749616.html
latex　常见使用方法　https://wenku.baidu.com/view/74251dc365ce0508763213d5.html
texlive　版本2017
推荐环境是 linux
推荐编译器 texstdio
常见问题解答QQ 1115064450

本文件使用说明：

doc.py　是编写tex文件的脚本　可自行修改doc.py达到编写不同tex的功能


表格信息统一存入csv_home文件夹中　
一个csv文件代表一个表格
csv文件的名字需遵循 编号+ ___+ 文件描述+.csv
例如 1___此表用于测试.csv

    2___此表用于记录变量.csv
    
    以此类推
    
文本_图片目录　用来存取图片和标签

pc目录　　数字开头的图片是附页中的图片　　　a.jpg是pdf中描述实验环境的图片　

take_pc_plan.txt 是图片的标签文件
标签的顺序和图片的顺序是一一对应的

makefile 用来指定编译的顺序

使用方法　
    在命令行使用make即可自动编译
