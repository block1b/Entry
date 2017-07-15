# coding=utf8
import threading
import time
from iniinfo import IniInfo


class TimeWindows(object):
    def __init__(self):
        self.ini = IniInfo()

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
    #
    # # 判断计时器是否存在
    # def IsTimerIn(self, timer):
    #     if timer != None:
    #         return True
    #     else:
    #         return False

    # 判定当前节次
    def get_now_section(self):
        course_schedule = self.ini.read_ini()
        # print course_schedule
        now_time = self.get_time()
        # print now_time
        classnumber = 0
        for i in range(0, 5):
            if course_schedule[i][0] < now_time and now_time < course_schedule[i][1]:
                classnumber = i + 1
                break
        return 1  # classnumber  # 为了测试先定程1吧

if __name__ == "__main__":
    t = TimeWindows()
    print t.get_now_section()