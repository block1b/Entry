#encoding=utf-8

# This program provide some methods for teacher to do check-in
import csv

class Method(object):

    # do the initialization
    def __init__(self):
        pass


    #althrough TeacherWechatID  get teacherID
    def checkTeacherID(self,teacherWechatID):
        filename = 'InData/teacherInfo.csv'
        checkTeacher = 0                           #对查询教师时的判断量
        with open(filename, 'rb') as teacherInfo:
            reader = csv.reader(teacherInfo)
            reader.next()
            for readline in reader:
                if readline[2] == teacherWechatID:
                    global teacherID
                    teacherID = readline[0]
                    checkTeacher = 0
                    break
                else:
                    checkTeacher = 1  # 没有查询到教师工号
            if checkTeacher == 1:
                print '无法在教师的信息表里查询到该教师的信息'
                return False
                #exit(0)
            else:
                return teacherID


    #althrough TeacherWechatID get file DetailName

    def getDetailName(self,teacherWechatID):
        TeacherID = self.checkTeacherID(teacherWechatID)
        with open('InData/courseInfo.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)  # 从选课信息表里找到教师的课程信息
            courseList = []
            for line in reader:
                if line[2] == TeacherID:
                    if not line[0] in courseList:
                        courseList.append(line[0])
                else:
                    pass
            print courseList

        CourseID = raw_input('请输入您选择的课程号')
        while not CourseID in courseList:
            # print '输入有误！请重新输入：'
            CourseID = raw_input('输入有误！请重新输入：')

        else:
            with open('OutData/seq.csv', 'r') as filename:
                reader2 = csv.reader(filename)
                seqIDList = []
                for line in reader2:
                    if (line[0] == TeacherID) & (line[1] == CourseID):
                        if not line[2] in seqIDList:
                            seqIDList.append(line[2])
                    else:
                        pass
            print seqIDList
        seqID = raw_input('请输入您想要修改的次序')
        while not seqID in seqIDList:
            seqID = raw_input('输入有误！请重新输入：')
        else:
            fileName = 'OutData/' + str(TeacherID) + '_' + str(CourseID) + '_' + \
                       str(seqID) + '_' + 'checkinDetail.csv'
        return fileName


# if __name__ == "__main__":
#     teac = 'Tp_rt55'
#     t = Method()
#     print t.checkTeacherID(teac)
#     print t.getDetailName(teac)   #对于得到详细文件名，是由于只在找到相关的文件，所以会出现选择相关的课程号