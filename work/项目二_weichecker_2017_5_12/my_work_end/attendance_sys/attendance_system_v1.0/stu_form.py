# coding=utf8
from stujoincheckincontrol import StuJoinCheckInControl
from showsum import ShowSum
from checkininfo import CheckInInfo
from iniinfo import IniInfo


class StuForm(object):
    def __init__(self, stu_id):
        self.stuid = stu_id
        self.stujoin = StuJoinCheckInControl()
        self.stu_show = ShowSum()

    def stu_form(self):
        while 1:
            # 签到，抽到，请假，查询
            print "*************  学生菜单  **************"
            print "************  1.自助签到  *************"
            print "************  2.抽点签到  *************"
            print "************  3.请假申请  *************"
            print "************  4.考勤查询  *************"
            print "************  0.退出      *************"
            select = raw_input("请选择功能标号：")
            if select == "1":
                print "***********  进行自助签到  **********"
                print "请输入您的特征信息"
                feature = raw_input("照片：")
                print "您的特征信息为：", feature
                self.stujoin.sign_in(self.stuid)
            elif select == "2":
                print "***********  进行抽点签到  **********"
                print "请输入您的特征信息"
                feature = raw_input("照片：")
                print "您的特征信息为：", feature
                self.stujoin.sample_in(self.stuid)
            elif select == "3":
                print "***********  进行请假申请  **********"
                print "请输入您的假条"
                feature = raw_input("照片：")
                print "您的假条为：", feature
                self.stujoin.leave_in(self.stuid)
            elif select == "4":
                print "***********  进行考勤查询  **********"
                print "请选择教师"
                tec_id = raw_input("请您输入教师的账号：")
                print "请选择课程"
                course_id = raw_input("请你输入课程号：")
                print "您的考勤汇总为："
                # 打印学生的考勤汇总
                self.stu_show.show_one_stu_all_checks(tec_id, course_id, self.stuid)
            elif select == "0":
                print "退出学生菜单"
                break

            else:
                print "别闹！没有这个选项。"

            to_end = raw_input("是否退出学生菜单？ Y:是 任意键:否 ：")
            if to_end == "Y":
                print "退出学生菜单"
                break
            else:
                pass


if __name__ == "__main__":
    # 模拟教师发起考勤
    TECID = "2004001"
    COURSEID = "51610101"
    COURSEFILENAME = "../internal/courseProgress.csv"
    STUFILENAME = "../internal/studentInfo.csv"
    SEQFILENAME = "../outputdemo/seq.csv"
    DEFAULTPATH = "../outputdemo/"
    STUID = "201516920101"
    cii = CheckInInfo(TECID, COURSEID, COURSEFILENAME, STUFILENAME, SEQFILENAME)
    cii.seqid = "3"
    ini = IniInfo()
    # ini.List.append(cii)
    print cii.tecid, cii.courseid, cii.seqid, cii.classnames, cii.stuids

    s = StuForm("201516920101")
    s.stu_form()
