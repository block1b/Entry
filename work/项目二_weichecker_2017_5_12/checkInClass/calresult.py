# coding=utf-8

#需要导入几个包
import csv

class calResult():
    def __init__(self):
        pass

    #检查详细表里的考勤状态。：  是否含有请假未被批准的？
    def checkStatus(self):
        with open('','r') as csvfile:
            reader  =csv.reader(csvfile)
            reader.next()
            count = 0
            for line in reader :
                if (line[5]=='请假') & (line[3]=='Auto'):
                    count = 1
                    break
                else:
                    count=0
            if count == 1:
                print '存在没有被确认的请假学生，无法进行自动计算'
                return 1
            else:
                return 0

    #对详细表的计算过程
    def cal(self):
        #调用判断函数
        if self.checkStatus()!=1:
            with open('','r+') as csvfile :




                pass

