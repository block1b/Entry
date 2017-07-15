# coding=utf8
import threading
from checkininfo import CheckInInfo
from timewindows import TimeWindows
from iniinfo import IniInfo


class demo(object):
    list = []

    def __init__(self):
        self.tim = TimeWindows()
        self.ini = IniInfo()
        self.t = None

    def fff(self, B):
        self.t = threading.Timer(int(self.ini.get_window_long()), B)
        self.t.start()

    def clear_arry(self):
        self.__class__.List = []
        print "计时结束"

if __name__ == "__main__":
    TECID = "2004643"
    COURSEID = "51610145"
    COURSEFILENAME = "../internal/courseProgress.csv"
    STUFILENAME = "../internal/studentInfo.csv"
    cii = CheckInInfo(TECID, COURSEID, COURSEFILENAME, STUFILENAME)
    d = demo()
    print cii
    d.__class__.list.append(cii)
    print d.list
    def B():
        d.__class__.List = []
        print "计时结束"
    d.fff(B)
