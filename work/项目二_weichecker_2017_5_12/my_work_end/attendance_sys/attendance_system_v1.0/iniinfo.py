# coding=utf8

import ConfigParser
import re
import time


# 读取配置文件信息   节次信息    返回一个节次开始和结束时间的列表
class IniInfo(object):

    List = []

    def __init__(self):
        pass

    # 获取当前系统时间
    def get_time(self):
        """
        获取系统当前的时间
        :return: 
        """
        return time.strftime("%H:%M", time.localtime())

    # 读取配置文件中的课程时间表
    def read_ini(self):
        cf = ConfigParser.ConfigParser()
        cf.read('../internal/settings.ini')
        schedule = []
        for i in range(1, 6):
            time = re.split('-', cf.get('sectime', 'sec'+str(i)))
            schedule.append(time)
        return schedule

    # 获取配置文件中的时间窗口长度
    def get_window_long(self):
        cf = ConfigParser.ConfigParser()
        cf.read('../internal/settings.ini')
        windows_long = cf.get('time', 'timewindow')
        return windows_long

if __name__ == "__main__" :
    r = IniInfo()
    win_long = r.get_window_long()
    print win_long
    course_schedule = r.read_ini()
    print course_schedule
    now_time = r.get_time()
    print now_time
    classnumber = 0
    for i in range(0, 5):
        if course_schedule[i][0] < now_time and now_time < course_schedule[i][1]:
            classnumber = i+1
            break
    print classnumber