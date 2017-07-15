# encoding: utf-8

import json
import sys
import __init__
import teastartcheckin
import tearandomcheckin
import teamanualcheckin
import stuautocheckin
import studelay
import viewatanytime


class SystemRun(object):
    def __init__(self):
        self.r1 = __init__.readini()
        self.t1 = teastartcheckin.teacherStartCheckIn()
        self.t2 = tearandomcheckin.teacherRandomCheckIn()
        self.t3 = teamanualcheckin.teacherManualCheckIn()
        self.s1 = stuautocheckin.stuCheckIn()
        self.s2 = studelay.stuDelay()
        self.v1 = viewatanytime.view()

    def Form(self):
        print "****************欢迎进入模拟控制菜单******************"
        print "*******1.教师开始考勤********2.学生进行考勤************"
        print "*******3.教师抽点考勤********4.学生进行请假************"
        print "*******5.教师手工考勤********6.考勤信息显示************"
        print "*******7.学生抽点考勤********0.退出*******************"
        opNum = raw_input("请输入您想要的操作：")
        count = 0
        while (count == 0):
            count = 1
            if (opNum == '1'):  # 教师开启考勤
                teacherWechatID = raw_input("请输入您的微信号：（教师）")
                courseID = raw_input("请输入您的课程号：")
                self.t1.startCheckIn(teacherWechatID, courseID)
                for line in self.r1.List:
                    print json.dumps(line, encoding="utf-8", ensure_ascii=False)

            elif (opNum == '2'):  # 学生正常考勤操作
                stuWechatID = raw_input("请输入您的微信号：（学生）")
                inputStream = raw_input("请输入您的考勤证据：")
                self.s1.stuAutoCheckIn(stuWechatID, inputStream)

            elif (opNum == '3'):  # 教师开启抽点考勤
                teacherWechatID = raw_input("请输入您的微信号：（教师）")
                num = int(raw_input("请输入您抽取的人数：（教师）"))
                self.t2.randomCheckIn(teacherWechatID, num)
                print "您已经完成了抽取人数！"

            elif (opNum == '4'):  # 学生进行请假操作
                stuWechatID = raw_input("请输入您的微信号：（学生）")
                inputStream = raw_input("请输入您的请假证据：")
                self.s2.stuLeave(stuWechatID, inputStream)

            elif (opNum == '5'):  # 教师进行手工考勤操作
                count1 = 0
                self.cform()
                while (count1 == 0):
                    operator = raw_input("您是否继续操作?y/n")
                    if operator == 'y':
                        self.cform()
                    else:
                        exit(0)

            elif (opNum == '6'):  # 随堂信息显示
                count2 = 0
                self.dform()
                while (count2 == 0):
                    operator = raw_input("您是否继续操作?y/n")
                    if operator == 'y':
                        self.dform()
                    else:
                        exit(0)

            elif (opNum == '7'):  # 学生进行抽点考勤
                stuWechatID = raw_input("请输入您的微信号：（学生）")
                inputStream = raw_input("请输入您的证据路径：（学生）")
                self.t2.stuRandomCheckIn(stuWechatID,inputStream)

            elif (opNum == '0'):  # 退出系统
                sys.exit(0)
            else:
                count = 0
                opNum = raw_input("您的输入有误！请重新输入:")

    # 查看信息窗口
    def dform(self):
        print "*****欢迎进入考勤信息展示菜单********"
        print "*******1.查看当前考勤信息***********"
        print "*******2.查看课程考勤信息***********"
        print "*******0.返回上层主菜单*************"
        opNum = raw_input("请输入您想要的操作：")
        count = 0
        while (count == 0):
            count = 1
            if (opNum == '1'):  # 查看当前考勤信息
                teacherWechatID = raw_input("请输入您的微信号：（教师）")
                print "你的当前课程的考勤信息如下："
                self.v1.showRealTime(teacherWechatID)

            elif (opNum == '2'):  # 查看课程考勤信息
                teacherWechatID = raw_input("请输入您的微信号：（教师）")
                CourseID = raw_input("请输入您要查看的课程号：（教师）")
                print "\n您的课程号为" + str(CourseID) + "的课的考勤结果如下："
                self.v1.sumCheckIn(teacherWechatID, CourseID)
            elif (opNum == '0'):  # 回到主菜单
                break


            else:
                count = 0
                opNum = raw_input("您的输入有误！请重新输入:")
        self.Form()

    # 手工考勤窗口
    def cform(self):
        print "****************欢迎进入手工考勤菜单******************"
        print "*******1.教师进行手工修改****2.教师进行手工增加*********"
        print "*******3.教师手工批准请假****0.返回上层主菜单***********"
        opNum = raw_input("请输入您想要的操作：")
        count = 0
        while (count == 0):
            count = 1
            if (opNum == '1'):  # 教师手工考勤修改
                teacherWechatID = raw_input("请输入您的微信号：（教师）")
                self.t3.manualCheckInAlter(teacherWechatID)

            elif (opNum == '2'):  # 教师手工考勤增加
                teacherWechatID = raw_input("请输入您的微信号：（教师）")
                self.t3.manualCheckInAdd(teacherWechatID)

            elif (opNum == '3'):  # 教师手工批准请假
                teacherWechatID = raw_input("请输入您的微信号：（教师）")
                self.t3.leaveCheckIn(teacherWechatID)

            elif (opNum == '0'):  # 回到主菜单
                break

            else:
                count = 0
                opNum = raw_input("您的输入有误！请重新输入:")
        self.Form()


if __name__ =="__main__" :

    test = SystemRun()
    s = test.r1.List
    print json.dumps(s, encoding="utf-8", ensure_ascii=False)

    count = 0
    test.Form()
    while(count == 0):
        operator = raw_input("您是否继续操作?y/n")
        if operator == 'y':
            test.Form()
        elif operator == 'n':
            sys.exit(0)
        else:
            operator = raw_input("您的输入有误，请重新输入: (y/n)")


