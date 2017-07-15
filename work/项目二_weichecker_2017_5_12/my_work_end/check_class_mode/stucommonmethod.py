# encoding=utf-8

import csv
from __init__ import readini
# This is the program show the common-methods for student

class stuMethod():

    #对普适方法进行初始化
    def __init__(self):
        pass

    #althrough the student-WechatID get [stuID,stu-class]
    def checkStudent(self,_stuWechatID):
        stuMessageList = []         #对由学生的微信号的到的学生信息列表初始化
        with open('InData/studentInfo.csv', 'r') as checkStuFile:
            reader = csv.reader(checkStuFile)
            count = 0  # 设置一个查询学生时的控制变量
            for readline in reader:
                if readline[3] == _stuWechatID:
                    count = 1
                    StuID = readline[0]  # 记录学生的ID
                    ClassID = readline[2]  # 将所在班级的ID记录
                    stuMessageList = [StuID, ClassID]
                else:
                    pass
            if count == 0:
                print '没有该学生的记录！'
                # exit(0)
                return
        return stuMessageList


    #althrough the student-WechatID get the file DetailName
    def checkFileName(self,_stuWechatID):
        ClassID = self.checkStudent(_stuWechatID)[1]
        count = 0  # 设置查询班级时的控制变量
        for listline in readini.List:  # 在全局队列中找到该行
            for classline in listline[2]:  # 在含有信息的行中找到班级
                if classline == ClassID:
                    count = 1
                    TID = listline[0]
                    CID = listline[1]
                else:
                    pass
        if count == 0:
            print '没有查询到该班级'
            fileName = ''
            return fileName
        with open('OutData/seq.csv', 'r') as csvfile:  # 在seq表里找到该考勤的文件
            reader = csv.reader(csvfile)
            count1 = 0  # 设置一个查询seq时的控制变量
            reader.next()
            for line in reader:
                if (line[0] == str(TID)) & (line[1] == str(CID)):
                    seqID = line[2]
                    count1 = 1
                else:
                    pass
            if count1 == 0:
                print '找不到相关信息！'
                # exit(0)
                return

            print '你将进行ID为' + str(TID) + ',课程ID为' + str(CID) + '的教师的考勤操作'
            fileName = 'OutData/' + str(TID) + '_' + str(CID) + '_' + \
                       str(seqID) + '_' + 'checkinDetail.csv'
        return fileName


# if __name__ == "__main__":
#     s = stuMethod()
#
#     _stu = 'wfsf_139'
#     print s.checkStudent(_stu)
#     print s.checkFileName(_stu)     #此处的List，为什么不能在readeini类中的__init__方法中进行定义？
