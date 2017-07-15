# encoding=utf-8

from tccommonmethod import Method
import os
import csv


class view(Method):
    #查看考勤信息

    def __init__(self):
        Method.__init__(self)
        pass


    def showRealTime(self,teacherWechatID):
        filename=self.getDetailName(teacherWechatID)
        leaveList = []  # 请假列表
        trueList = []  # 出勤列表
        falseList = []  # 缺勤列表
        i = 0
        j = 0
        z = 0
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[5] == '请假':
                    leaveList.append(line[0])
                    i = i + 1
                elif line[4] == 'True':
                    trueList.append(line[0])
                    j = j + 1
                else:
                    falseList.append(line[0])
                    z = z + 1
        print '请假人数为：' + str(i)
        print '出勤人数为：' + str(j)
        print '失败人数为：' + str(z - i-1)


    def sumCheckIn(self,teacherWechatID,CourseID):
        TeacherID = self.checkTeacherID(teacherWechatID)
        filename = 'OutData/' + str(TeacherID) + '_' + str(CourseID) + '_' + 'sum.csv'
        if (os.path.isfile(filename)):  # 如果不存在就返回False
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for line in reader:
                    print line
        else:
            print "文件不存在（可能是还未生成一次考勤记录！）！请查看您的输入！"