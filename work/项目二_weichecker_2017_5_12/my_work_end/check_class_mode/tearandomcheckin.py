#encoding=utf-8

from tccommonmethod import Method
from stucommonmethod import stuMethod
from __init__ import readini
import csv
import random



class teacherRandomCheckIn(Method):
    #对教师抽点类的初始化
    def __init__(self):
        Method.__init__(self)
        pass

    #教师开始抽点
    def randomCheckIn(self,teacherWechatID,num):
        stu = stuMethod()
        TeacherID = self.checkTeacherID(teacherWechatID)   #得到教师的ID
        stuArray = []  # 置空该班级下的学生列表
        count = 0
        for Listline in readini.List:
            if Listline[0] == TeacherID:
                classList = Listline[2]  # 获得班级列表
                count = 1
            else:
                pass
            if count == 0:
                print '当前队列里没有此教师，无法开始抽点！'
                # exit(0)
                return

        with open('InData/studentInfo.csv', 'r') as csvfile:  # 将上课的学生微信号暂存入数组
            reader = csv.reader(csvfile)
            reader.next()
            for line in reader:  # 遍历class列表查看是否是该班级内的学生，是就追加微信号
                if line[2] in classList:
                    stuArray.append(line[3])
        global stuArray2
        stuArray2 = random.sample(stuArray, num)  # 实现抽取学生！
        print stuArray2
        fileName = stu.checkFileName(stuArray2[0])     #得到学生需要进行考勤的详细文件名

        with open(fileName, 'a+') as csvfile2:  # 在详细信息表里写入num行信息学号+Random
            writer = csv.writer(csvfile2)
            i = 0
            while (i < num):
                message0 = [stu.checkStudent(stuArray2[i])[0], '', '', 'Random', '', '']
                writer.writerow(message0)
                i = i + 1

    # 学生进行抽点  参数学生微信号数组
    def stuRandomCheckIn(self,_stuWechatID,inputStream):
        stu = stuMethod()
        if stuArray2 != "":
            for line in stuArray2:  # 遍历传过来的抽点数组，查询是否是被抽点的人。
                if line == _stuWechatID:
                    with open(stu.checkFileName(_stuWechatID), 'a+') as fileName:
                        reader = fileName.readlines()
                        d = ""
                        for line in reader:  # 查询到了就进行修改上传信息
                            sline = line.split(',')
                            if (sline[0] == stu.checkStudent(_stuWechatID)[0]) & (sline[3] == 'Random'):

                                IsSucc = bool(random.randrange(0, 2))
                                StuID = stu.checkStudent(_stuWechatID)[0]
                                lineArray = [StuID, '无', inputStream, 'Random', IsSucc, '']
                                d += ','.join(map(str, lineArray)) + '\n'  # 用map函数的含义 ：
                            else:
                                d += line
                        fileName.seek(0)  # 从文件头还始
                        fileName.truncate()  # 清空文件
                        fileName.write(d)  # 将修改后的内容写入
            print '已成功抽点'
        else:
            print "对不起！当前教师没有开启抽点！"


#此时含有教师开启抽点和学生进行抽点的函数
if __name__ == "__main__":
    pass