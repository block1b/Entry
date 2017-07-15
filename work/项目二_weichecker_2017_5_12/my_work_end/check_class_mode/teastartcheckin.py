# encoding=utf-8

from tccommonmethod import Method
from __init__ import readini
from TimeWindow import Timer
import csv
import time
import os

# This program is show the teacher's operations
# This program is show teacher to start the checkIn

class teacherStartCheckIn(Method):

    #对教师开始考勤类进行初始化
    def __init__(self):
        Method.__init__(self)
        pass

    # 教师进入队列。
    def entryList(self,TeacherID,CourseID):
        ti = Timer()    #建立一个Timer计时器的实例
        classList = []  # 设置上课的班级列表
        with open('InData/courseInfo.csv', 'rb') as courseInfo:
            reader = csv.reader(courseInfo)
            count = 0  # 设置下边追加班级时的控制变量
            reader.next()
            for cline in reader:
                if (cline[0] == str(CourseID)) & (cline[2] == str(TeacherID)):
                    classList.append(cline[3])
                    count = 1
                else:
                    pass
            if count == 0:
                print '没有上课的班级！'
                # exit(0)
                return False

        nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
        messagelist = [TeacherID, CourseID, classList, nowtime]
        if readini.List:  # 列表非空 需要进行判断！
            for line in readini.List:
                if (set(classList) & set(line[2])):
                    print "班级已存在"
                    read = readini()
                    s = read.readIni()     #  从readIni中得到课程的开始时间和结束时间
                    stime0 = nowtime.split(" ")
                    stime1 = stime0[1].split(':')
                    stime = stime1[0] + stime1[1] + stime1[2]
                    if (s[0] < stime < s[1]) | (s[2] < stime < s[3]) | (s[4] < stime < s[5]):
                        readini.List.remove(line)
                        readini.List.append(messagelist)
                        print "踢出前一个教师成功，成功进入队列！"
                    else:
                        print "当前班级正在考勤！您无法开启"
                        return False
                else:
                    readini.List.append(messagelist)
                    ti.stopCheckIn()
        else:
            readini.List.append(messagelist)
            ti.startCheckTime()
            ################################# 在第一个教师进入队列的时候，设置一个计时器的初始化时间   此时应直接调用初始化时间差
            # ti = Timer()
            # ti.timeCheck(60*2)    #每节大课的全部时间。

    # 生成考勤次序表+考勤详细表
    def creatSeq(self,TeacherID, CourseID):
        with open('OutData/seq.csv', 'r+') as csvfile:
            reader = csv.reader(csvfile)
            writer = csv.writer(csvfile)
            nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
            seqID = ''
            for line in reader:
                 if line[0] == TeacherID:
                    seqID = line[2]
                 else:
                    pass
            if seqID == '':
                seqID = 1
            else:
                seqID = str(int(seqID) + 1)
            messageList = [TeacherID, CourseID, seqID, nowtime]
            writer.writerow(messageList)

        # 生成考勤详细表
        newFileName = 'OutData/' + str(TeacherID) + '_' + str(CourseID) + '_' + \
                      str(seqID) + '_' + 'checkinDetail.csv'
        with open(newFileName, 'a+') as filename:
           writer2 = csv.writer(filename)
           messageList2 = ['StuID', 'checkTime', 'ProofPath', 'checkinType', 'IsSucc', 'checkinResult']
           writer2.writerow(messageList2)


    # def creatSum(self,TeacherID, CourseID):
    #     filename = 'OutData/' + str(TeacherID) + '_' + str(CourseID) + '_' + "sum.csv"
    #     count = 0
    #     if os.path.exists(filename) != True:
    #           count = 1
    #           with open(filename, 'a+') as csvfile:
    #               writer = csv.writer(csvfile)
    #               if count == 0:
    #                 String2 = ['StuID', '']
    #                 writer.writerow(String2)
    #                 for line in readini.List:
    #                     if (line[0] == TeacherID) & (line[1] == CourseID):
    #                         with open('InData/studentInfo.csv', 'r') as classFilename:
    #                             reader = csv.reader(classFilename)
    #                             reader.next()
    #                             for line1 in reader:
    #                                 if line1[2] in line[2]:
    #                                     string = [line1[0], '']
    #                                     writer.writerow(string)

    # 生成sum表，在考勤时间窗口结束后汇总信息
    # 此时将学生ID全部加入
    def creatSum(self,TeacherID, CourseID):
        filename = 'OutData/' + str(TeacherID) + '_' + str(CourseID) + '_' + "sum.csv"
        if os.path.exists(filename) != True:
            with open(filename, 'a+') as csvfile:
                writer = csv.writer(csvfile)
                String2 = ['StuID', '']
                writer.writerow(String2)
                for line in readini.List:
                    if (line[0] == TeacherID) & (line[1] == CourseID):
                        with open('InData/studentInfo.csv', 'r') as classFilename:
                            reader = csv.reader(classFilename)
                            reader.next()
                            for line1 in reader:
                                if line1[2] in line[2]:
                                    string = [line1[0], '']
                                    writer.writerow(string)

    #教师开始考勤
    def startCheckIn(self,teacherWechatID,CourseID):
        CourseID = CourseID
        TeacherID = self.checkTeacherID(teacherWechatID)
        if (self.entryList(TeacherID,CourseID) != False):
            self.creatSeq(TeacherID,CourseID)
            self.creatSum(TeacherID,CourseID)


# if __name__ == "__main__":
#     readini.List = [['2004633', '51610189', ['\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b1401', '\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b1402', '\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b1403', '\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf1401'], '2016-06-09 14:00:21']]
#     t = teacherStartCheckIn()
#     tc = '2004633'
#     co = '51610189'
#     # t.startCheckIn(tc,co)
#     t.creatSum(tc,co)



