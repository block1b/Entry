# coding=utf8
import threading
import time
import datetime
from iniinfo import IniInfo


class TimeWindows(object):
    def __init__(self):
        self.ini = IniInfo()
        self.t = None  # 计时器

    # 获取当前系统时间
    def get_time(self):
        """
        获取系统当前的时间
        :return: 
        """
        return time.strftime("%H:%M", time.localtime())

    # 获取当前系统时间
    def get_time2(self):
        """
        获取系统当前的时间
        :return: 
        """
        return time.strftime("%Y-%m-%d %X", time.localtime())

        # 求时间差
    def get_time_sub(self, date1, date2):
        date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
        date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S")
        date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
        date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
        data3 = (date2 - date1).seconds
        return data3

    # 时间窗口设置更新步骤
    # 1.空队列，进队首，t=100*60s(配置文件设定的长度)
    # 2.队首计时结束，t=t2-t1
    # 3.队首被踢，记时停止，t=100-t(now)+t2
    # 定时器结束触发步骤
    # 1.计时结束后，执行检查方法，检查考勤队列内是否还有考勤对象？
    # 2.没有，结束。
    # 3.有，按时间窗口2记时。
    #       教师被踢出队列时需要重新计时,或者自动到时间后教师被提出队列，
    #       此处只计算与下一位的差值，并重新计时
    # 独立的踢出队列函数
    def time_check(self):
        cii_arry = self.ini.List
        if cii_arry:
            hand_start_time = cii_arry[0].starttime  # 计时结束的队首开启时间
            cii_arry.pop(0)  # 将队首踢出队列
            self.stop_check(cii_arry, hand_start_time)
        else:
            # 队列内考勤完成
            print "考勤结束"
            return

    # 教师进入队列后开始进行倒计时   在第一个教师进入队列时和队首被踢时调用
    def start_check_time(self, timewindow):
        self.t = threading.Timer(timewindow, self.time_check)
        self.t.start()

    def stop_check(self, cii_arry, hand_start_time):
        if cii_arry:
            # 队首的时间记时结束，计算下一dev
            timedev = self.get_time_sub(hand_start_time, cii_arry[0].starttime)  # t=t2-t1
            # 先取消上次计时后，再传入新的计时值
            self.t.cancel()
            self.t = threading.Timer(timedev, self.time_check)
            self.t.start()
        else:
            print "考勤结束"
            return

    # # 设置计时器
    # def set_time_windows(self, timer, times_long, times_end_then):
    #     timer = threading.Timer(times_long, times_end_then)
    #     return timer
    #
    # # 开启计时器
    # def start_time_windows(self, timer):
    #     timer.start()
    #
    # # 关闭计时器
    # def end_time_wimdows(self, timer):
    #     timer.cancel()

    # 判断计时器是否存在
    def IsTimerIn(self, timer):
        if timer != None:
            print "this time windows is working."
            return True
        else:
            print "this time windows has been end."
            return False

    # 判定当前节次
    def get_now_section(self, now_time):
        course_schedule = self.ini.read_ini()
        # print course_schedule
        # now_time = self.get_time()
        # print now_time
        classnumber = 0
        for i in range(0, 5):
            if course_schedule[i][0] < now_time and now_time < course_schedule[i][1]:
                classnumber = i + 1
                break
        return classnumber  # 为了测试先定程1吧

if __name__ == "__main__":
    t = TimeWindows()
    print t.get_now_section()