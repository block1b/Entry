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
        self.t = None  # 计时器

    # 完成考勤对象队列的维护

    # 更新队列
    # 时间窗口开启即队列更新规则：
    # 1.判定节次
    # 2.该节次内不存在时间窗口，更新队列，开启计时器。
    # 3.该节次内存在时间窗口，class不冲突，进入队列。
    # 4.该节次内存在时间窗口，class冲突，不能进入队列。
    # 5.不同节次，更新队列，关闭现有计时器，开启新计时器。

    # 清空队列
    def clear_arry(self):
        self.__class__.List = []
        print "计时结束"

    # 判断该当前对象与队首是否为相同节次
    def same_section(self, now_cii, list_first):
        if now_cii.section == list_first.section:
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
                return False
        return True

    # 判断当前考勤对象与考勤队列中的对象，教师是否冲突
    def same_tecid(self, now_cii, list_arry):
        for acii in list_arry:
            if now_cii.tecid == acii.tecid:
                return False
        return True

    def update_arry(self, now_cii):
        # 空队列添加考勤对象
        # 考勤对象now_cii
        now_section = self.tim.get_now_section()
        # 判断节次是否为0
        if now_section:
            # 判断现有队列是否为空
            if self.__class__.List:
                # 如果当前考勤对象与队首的节次相同，进入队列
                if self.same_section(now_cii, self.__class__.List[0]):
                    # 判断人员是否冲突
                    if self.same_classnames(now_cii, self.__class__.List) \
                            and self.same_tecid(now_cii, self.__class__.List):
                        # 人员不冲突，进入队列
                        self.__class__.List.append(now_cii)
                        return True
                    else:
                        return False
                else:
                    # 节次变化，清空队列，进入队列，重启计时器
                    self.clear_arry()
                    self.__class__.List.append(now_cii)
                    self.t.cancel()
                    self.t = threading.Timer(float(self.ini.get_window_long()), self.clear_arry())
                    self.t.start()
                    return True
            else:
                self.__class__.List.append(now_cii)
                # ??为什么立即结束了？？问题出在类方法self.clesr_arry“()”<--日天，不要“（）”
                time_long = float(self.ini.get_window_long())
                self.t = threading.Timer(time_long, self.clear_arry)
                self.t.start()
                return True
        else:
            # 非考勤时间
            return False


if __name__ == "__main__":
    c = CheckInArray()
    print c
    TECID = "2004643"
    COURSEID = "51610145"
    COURSEFILENAME = "../internal/courseProgress.csv"
    STUFILENAME = "../internal/studentInfo.csv"
    now_cii = CheckInInfo(TECID, COURSEID, COURSEFILENAME, STUFILENAME)
    c.update_arry(now_cii)
# 处理同教师开开两课
