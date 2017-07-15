#encoding=utf-8

from tccommonmethod import Method
import csv
import time


class teacherManualCheckIn(Method):
    #对教师手工考勤类的初始化
    def __init__(self):
        Method.__init__(self)
        pass

    #教师进行手工考勤修改
    def manualCheckInAlter(self,teacherWechatID):
        fileName = self.getDetailName(teacherWechatID)
        stuID = raw_input('输入你想要修改的学生学号')
        checkResult = raw_input('输入该学生的考勤结果：')

        with open(fileName, 'r+') as changeName:
            lines = changeName.readlines()
            d = ""
            for line in lines:
                lineArray = line.split(',')
                if lineArray[0] == stuID:
                    lineArray[5] = checkResult
                    d += ','.join(lineArray) + '\n'
                else:
                    d += line
            changeName.seek(0)  # 从文件头还始
            changeName.truncate()  # 清空文件
            changeName.write(d)  # 将修改后的内容写入
        print '您已成功修改该学生的考勤结果'

    #教师进行手工考勤增加
    def manualCheckInAdd(self,teacherWechatID):
        TeacherID = self.checkTeacherID(teacherWechatID)
        with open('InData/courseInfo.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            courseList = []
            for line in reader:
                if line[2] == TeacherID:
                    if not line[0] in courseList:
                        courseList.append(line[0])
                else:
                    pass
            print '当前课程号列表如下：'
            print courseList

        CourseID = raw_input('请输入您选择的课程号：')
        while (not CourseID in courseList):
            print '输入有误！请重新输入：'
            CourseID = raw_input('请输入您选择的课程号：')
        else:
            with open('OutData/seq.csv', 'r+') as csvfile:  # 在seq表里找到该考勤的文件,追加一行新的seq行，
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
        fileName = 'OutData/' + str(TeacherID) + '_' + str(CourseID) + '_' + \
                   str(seqID) + '_' + 'checkinDetail.csv'
        with open(fileName, 'a+') as addfile:  # 将该教师，该课程下的所有学生全部加入到新的考勤详细文件里
            writer = csv.writer(addfile)
            message0 = ['StuID', 'checkinTime', 'ProofPath', 'checkinType', 'IsSuss', 'checkinResult']
            writer.writerow(message0)
            stufile = 'OutData/' + TeacherID + '_' + CourseID + '_' + 'sum.csv'
            with open(stufile, 'r') as stufilename:
                reader1 = csv.reader(stufilename)
                reader1.next()
                for line in reader1:  # 由教师ID和课程ID得到班级列表，将班级中的所有学生全部写入列表，默认出勤。
                    message = [line[0], '无', '无', 'man', 'True', '出勤']
                    writer.writerow(message)

        print '您已成功增加一次考勤记录，并以默认所有学生出勤'

    #教师进行手工确认请假
    def leaveCheckIn(self,teacherWechatID):
        filename = self.getDetailName(teacherWechatID)
        StuArray = []  # 请假的学生列表
        with open(filename, 'r') as csvfile:
            array = []
            reader = csv.reader(csvfile)
            reader.next()
            print '这次考勤请假的未被确认的人员为：'
            for line in reader:
                array1 = []
                if (line[5] == '请假') & (line[4] == ''):
                    array1.append(line[0])
                    array1.append(line[5])
                    array = array1
                    StuArray.append(array)
        print StuArray
        if (StuArray):
            StuID = raw_input('请输入想确认的学生号：')
            count = 0
            while (count == 0):
                for line in StuArray:
                    if (line[0] == StuID):
                        count = 1
                    else:
                        pass

            with open(filename, 'r+') as csvfile:
                d = ''
                lines = csvfile.readlines()
                for line in lines:
                    sline = line.split(',')
                    if sline[0] == StuID:
                        sline[3] = 'man'
                        sline[4] = 'True'
                        d += ','.join(sline)
                    else:
                        d += line
                csvfile.seek(0)  # 从文件头还始
                csvfile.truncate()  # 清空文件
                csvfile.write(d)  # 将修改后的内容写入
                print '请假信息已经确认！'
        else:
            print "此次考勤没有请假的学生！"


#教师所能进行的手工考勤
if __name__ == "__main__":
    pass