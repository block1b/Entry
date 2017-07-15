# coding=utf8
import threading
from iniinfo import IniInfo
from timewindows import TimeWindows
from checkininfo import CheckInInfo  # 只用于用于本例功能能测试
# 时间窗口开启即队列更新规则：
# 1.判定节次
# 2.该节次内不存在时间窗口，更新队列，开启计时器。
# 3.该节次内存在时间窗口，class不冲突，进入队列。
# 4.该节次内存在时间窗口，class冲突，不能进入队列。
# 5.不同节次，更新队列，关闭现有计时器，开启新计时器。


class CheckInArray(object):
    # 队列元素【考勤对象1（节次, tecid, courseid）】
    List = []

    def __init__(self):
        self.ini = IniInfo()
        self.tim = TimeWindows()

    # 判断教师课程是否在考勤队列中
    def check_arry_tec(self, tec_id, cii_arry):
        for a_cii in cii_arry:
            if a_cii.tecid == tec_id:
                return True
        return False

    # 判断学生是否在考勤队列中
    def check_arry_stu(self, stu_id, cii_arry):
        for a_cii in cii_arry:
            if a_cii.stuids == stu_id:
                return True
        return False

    # 判断教师+课头是否在考勤队列中

    # 完成考勤对象队列的维护
    # 判断该当前对象与队内对象是否为相同节次
    def same_section(self, now_cii, cii_arry):
        for one_cii in cii_arry:
            if now_cii.section == one_cii.section:
                return True
            else:
                return False

    # 判断当前对象与队列中的对象，班级是否冲突
    def same_classnames(self, now_cii, list_arry):
        all_checkin_classnames = []
        for acii in list_arry:
            all_checkin_classnames += acii.classnames
        for aclassname in now_cii.classnames:
            if aclassname in all_checkin_classnames:
                return True
        return False

    # 删除队列内与当前考勤对象有学生冲突的考勤对象并判断队首是否被更新
    def remove_arry_same_class(self, now_cii, cii_arry):
        confit_cii = []
        flag = 1
        for one_cii in cii_arry:
            if list(set(one_cii.classnames) & set(now_cii.classnames)) or (one_cii.tecis == now_cii.tecid):  # 人员冲突
                confit_cii.append(one_cii)  # 记录队列内的冲突对象
                if cii_arry.index(one_cii) == 0:
                    flag = 0  # 队首冲突标志
            else:
                pass
        # 删除冲突对象
        for one_cii in confit_cii:
            cii_arry.remove(one_cii)
            print "考勤结束"
        return flag

    # 判断当前考勤对象与考勤队列中的对象，教师是否冲突
    def same_tecid(self, now_cii, list_arry):
        for acii in list_arry:
            if now_cii.tecid == acii.tecid:
                return True
        return False

    # 更新考勤队列
    def update_arry(self, now_cii, cii_arry):
        # 队列更新步骤
        # 2.查看学生是否已经在考勤队列？+该教师是否已经在考勤你队列
        if self.same_classnames(now_cii, cii_arry) or self.check_arry_tec(now_cii.tecid, cii_arry):
            # 3.本考勤对象的学生在考勤队列，查看本考勤对象的节次，与队列内学生冲突的考勤对象的节次是否一致？
            if self.same_section(now_cii, cii_arry):
                # 5.节次相同，不允许进入，结束。
                return False
            else:
                # 4.节次不同，踢队内的考勤对象，本对象进入队尾。结束。
                # 踢队内学生冲突的对象
                new_hand_flog = self.remove_arry_same_class(now_cii, cii_arry)
                cii_arry.append(now_cii)  # 该教师进入队列
                # 若队首被更新 判定方法待定
                if new_hand_flog == 0:  # 队首被更新
                    self.tim.t.cancel()
                    timedev = int(self.ini.get_window_long()) - (self.tim.get_time_sub(cii_arry[0].starttime, now_cii.starttime))
                    self.tim.start_check_time(timedev)
                else:
                    pass
                return True
        else:
            # 3.本考勤对象的学生不在考勤队列，本考勤对象进队尾。结束。
            # 如果此对象为第一个教师
            if cii_arry:
                pass
            else:
                self.tim.start_check_time(int(self.ini.get_window_long()))
            cii_arry.append(now_cii)  # 该教师进入队列
            return True


if __name__ == "__main__":
    c = CheckInArray()
    print c
    TECID = "2004001"
    COURSEID = "51610101"
    COURSEFILENAME = "../internal/courseProgress.csv"
    STUFILENAME = "../internal/studentInfo.csv"
    SEQFILENAME = "../outputdemo/seq.csv"
    # (tec_id, course_id, course_filename, stu_filename, seq_filename)

    CIIARRY = []
    # 处理同教师开开两课
    print "开始考勤1"
    now_cii = CheckInInfo(TECID, COURSEID, COURSEFILENAME, STUFILENAME, SEQFILENAME)
    now_cii.section = 1

    if c.update_arry(now_cii, CIIARRY):
        print "1succeed"
    else:
        print "1false"
    #
    print "开始考勤2"
    TECID = "2004001"
    COURSEID = "51610101"
    now_cii2 = CheckInInfo(TECID, COURSEID, COURSEFILENAME, STUFILENAME, SEQFILENAME)
    now_cii2.section = 2

    if c.update_arry(now_cii2, CIIARRY):
        print "2succeed"
    else:
        print "2false"
    print "开始考勤2"
