# coding=utf8
from courseinfo import CourseInfo
from tecstartcheckincontrol import TecStartCheckInControl
from checkininfo import CheckInInfo
from tecsamplecheckincontrol import TecSampleCheckInControl
from iniinfo import IniInfo
from tecmancheckincontrol import TecManCheckInInsertControl
from tecapprovenote import TecApproveNote
from showsum import ShowSum


class TecForm(object):
    def __init__(self, tec_id):
        self.tecid = tec_id
        # self.ini = IniInfo()
        self.show = ShowSum()

    # 教师主菜单
    def tec_form(self):
        while 1:
            # 自助，抽点，手工，审批，查询
            print "***************  教师菜单  **************"
            print "**************  1.自助考勤  *************"
            print "**************  2.抽点考勤  *************"
            print "**************  3.手工考勤  *************"
            print "**************  4.手工修改  *************"
            print "**************  5.审批假条  *************"
            print "**************  6.考勤查询  *************"
            print "**************  7.导入文件  *************"
            print "**************  0.退出      *************"
            select = raw_input("请选择功能标号：")
            if select == "1":
                print "*********  进入自助考勤菜单  **********"
                self.start_checkin_form(self.tecid)
            elif select == "2":
                print "*********  进入抽点考勤菜单  **********"
                self.sample_checkin_form(self.tecid)
            elif select == "3":
                print "*********  进入手工考勤菜单  **********"
                self.man_checkin_form(self.tecid)
                # 1.功能模块需要重写，完成
            elif select == "4":
                print "*********  进入手工修改菜单  **********"
                self.manual_update(self.tecid)
                # 2.功能模块需要重写，完成
            elif select == "5":
                print "*********  进入审批假条菜单  **********"
                self.approve_note(self.tecid)
                # 3.功能模块需要重写，完成
            elif select == "6":
                print "*********  进入考勤查询菜单  **********"
                self.show_sum(self.tecid)
                # 4.功能模块需要重写，完成

            elif select == "7":
                print "*********  进入导入文件菜单  **********"
                # 导入文件
                # 6.待定！！！
                pass

            elif select == "0":
                print "退出教师菜单"
                break
            else:
                print "别闹！没有这个选项。"

            to_end = raw_input("是否退出教师菜单？ Y:是 任意键:否 ：")
            if to_end == "Y":
                print "退出教师菜单"
                break
            else:
                pass

    # 获取该教师选择的课头
    def select_courseid(self, tec_id):
        c = CourseInfo()
        all_info = c.get_all_course_info("../internal/courseProgress.csv")
        the_tec_info = c.get_course_info_from_teacher_id(tec_id, all_info)
        course_names = c.get_course_names(the_tec_info)
        course_ids = c.get_course_ids(the_tec_info)
        i = 1
        print "课头序号|课程名|课头号"
        for a_course_name in course_names:
            print str(i) + "      " + a_course_name.decode('utf-8') + "      " + course_ids[i - 1]
            i += 1
        select = raw_input("请选择要考勤的课头号的序号：")
        select = int(select)
        if select > 0 and select <= len(course_names):
            select_id = course_ids[select - 1]
            return select_id
        else:
            print "别闹！没有这个选项"
            return

    # 自助考勤菜单
    def start_checkin_form(self, tec_id):
        print "********  自助考勤菜单  *********"
        # 获取教师选择的课头
        select_courseid = self.select_courseid(tec_id)
        if select_courseid:
            print "开始对课头" + select_courseid + "自助考勤"
            # 进入自助考勤功能模块
            tec_start = TecStartCheckInControl()
            COURSEFILENAME = "../internal/courseProgress.csv"
            STUFILENAME = "../internal/studentInfo.csv"
            SEQFILENAME = "../outputdemo/seq.csv"
            # 实例考勤对象考勤
            cii = CheckInInfo(self.tecid, select_courseid, COURSEFILENAME, STUFILENAME, SEQFILENAME)
            tec_start.tec_start_checkin(cii, SEQFILENAME)
        else:
            print "开启失败，未选择课头"

    # 抽点考勤菜单
    def sample_checkin_form(self, tec_id):
        print "*******  抽点考勤菜单  ********"
        # 获取教师选择的课头
        select_courseid = self.select_courseid(tec_id)
        if select_courseid:
            people_num = raw_input("请选择抽点人数：")
            print "开始对课头" + select_courseid + "抽点考勤，抽点人数" + people_num + "人"
            # 进入抽点考勤空能模块
            tec_sample = TecSampleCheckInControl()
            tec_sample.tec_sample_checkin(tec_id, select_courseid, people_num, IniInfo.List)
        else:
            print "开启失败，未选择课头"

    # 获取输入名单
    def get_roll(self):
        stus = []
        print "在姓名处输入Enter可结束输入"
        while 1:
            name = raw_input("姓名：")
            if name:
                stus.append(name)
            else:
                break
        return stus

    # 手工考勤菜单
    def man_checkin_form(self, tec_id):
        print "******  手工考勤菜单  *******"
        # 获取教师选择的课头
        select_courseid = self.select_courseid(tec_id)
        if select_courseid:
            # 教师手工输入的考勤信息格式看用例分析。
            print "请输入到勤学生(学号)名单"
            arrive = self.get_roll()
            print "到勤学生名单", arrive
            print "请输入缺勤学生(学号)名单"
            absence = self.get_roll()
            print "缺勤学生名单：", absence
            print "请输入迟到学生(学号)名单"
            late = self.get_roll()
            print "迟到学生名单：", late
            print "请输入早退学生(学号)名单"
            early = self.get_roll()
            print "早退学生名单：", early
            print "请输入请假学生（学号）名单"
            note = self.get_roll()
            print "请假学生名单：", note
            print "手工考勤结果已录入系统"
            # 进入手工考勤模块
            tec_man = TecManCheckInInsertControl()
            COURSEFILENAME = "../internal/courseProgress.csv"
            STUFILENAME = "../internal/studentInfo.csv"
            SEQFILENAME = "../outputdemo/seq.csv"
            DEFAULTPATH = "../outputdemo/"
            tec_man.man_checkin(tec_id, select_courseid, COURSEFILENAME, STUFILENAME,
                                arrive, absence, late, early, note, SEQFILENAME, DEFAULTPATH)

        else:
            print "开启失败，未选择课头"

    # 获取考勤次序号
    def select_seqid(self):
        seqid = raw_input("请输入考勤次序号：")
        if seqid.isdigit():
            return seqid
        else:
            print "输入非法"
            return None

    # 手工修改菜单
    def manual_update(self, tec_id):
        print "******  手工修改菜单  ******"
        # 获取教师选择的课头
        select_courseid = self.select_courseid(tec_id)
        if select_courseid:
            # 选择考勤次序号
            select_seqid = self.select_seqid()
            if select_seqid:
                # 输入修改人名和修改状态
                name = raw_input("姓名(id)：")
                result = raw_input("考勤结果：")
                print "将学生：" + name + "的考勤结果修改为：" + result
                # 进入手工修改模块
                tec_man2 = TecManCheckInInsertControl()
                COURSEFILENAME = "../internal/courseProgress.csv"
                STUFILENAME = "../internal/studentInfo.csv"
                SEQFILENAME = "../outputdemo/seq.csv"
                DEFAULTPATH = "../outputdemo/"
                tec_man2.man_change(tec_id, select_courseid, select_seqid,
                                    name, result, COURSEFILENAME, STUFILENAME, SEQFILENAME, DEFAULTPATH)
            else:
                print "开启失败，考勤次序号非法"
        else:
            print "开启失败，未选择课头"

    # approve 审批假条
    def approve_note(self, tec_id):
        print "******  审批假条菜单  ******"
        # 获取教师选择的课头
        select_courseid = self.select_courseid(tec_id)
        if select_courseid:
            # 选择考勤次序号
            select_seqid = self.select_seqid()
            if select_seqid:
                SEQFILENAME = "../outputdemo/seq.csv"
                DEFAULTPATH = "../outputdemo/"
                tecapprove = TecApproveNote()
                print "请假的学生有："
                # 打印请假学生名单。
                print tecapprove.show_note_stuids(tec_id, select_courseid, select_seqid, SEQFILENAME, DEFAULTPATH)
                print "请输入审批通过的学生(学号)名单"
                agree = self.get_roll()
                print "审批通过的学生名单：", agree
                # 开始审批 !!!!ERROR!!!!!
                tecapprove.approve_note(tec_id, select_courseid, select_seqid, agree, SEQFILENAME, DEFAULTPATH)
            else:
                print "开启失败，考勤次序号非法"

        else:
            print "开启失败，未选择课头"

    # 查询菜单
    def show_sum(self, tec_id):
        print "******  考勤查询菜单  ******"
        # 获取教师选择的课头
        select_courseid = self.select_courseid(tec_id)
        if select_courseid:
            while 1:
                print "*****  1.查询某人所有次考勤记录    *****"
                print "*****  2.查询某次所有人考勤记录    *****"
                print "*****  3.查询所有人所有次考勤记录  *****"
                select = raw_input("请选择查询方式：")
                if select == "1":
                    name = raw_input("请输入学生（学号）姓名：")
                    print "学生 " + name + " 的所有考勤记录为：XXX"
                    self.show.show_one_stu_all_checks(tec_id, select_courseid, name)
                elif select == "2":
                    num = self.select_seqid()
                    print "第 " + num + " 次的考勤记录为：XXX"
                    self.show.show_one_check_all_stus(tec_id, select_courseid, num)
                elif select == "3":
                    print "所有学生的考勤记录为：XXX"
                    self.show.show_all_stu_all_check(tec_id, select_courseid)
                else:
                    print "别闹！没有这个选项"

                print ""
                to_end = raw_input("是否退出查询菜单？ Y:是 任意键:否 ：")
                if to_end == "Y":
                    print "退出查询菜单"
                    break
                else:
                    pass

        else:
            print "开启失败，未选择课头"


if __name__ == "__main__":
    t = TecForm("2004001")
    t.tec_form()
