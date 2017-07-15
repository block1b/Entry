# coding=utf8
from TecManCheckInInsertControl import TecManCheckInInsertControl
from SeqInfo import SeqInfo
from DetailInfo import DetailInfo
from CourseInfo import CourseInfo
from StuInfo import StuInfo
from SumInfo import SumInfo
"""
教师进行手工考勤的操作界面
"""


class TecManCheckInForm(object):
    def __init__(self):
        self.mancheck = TecManCheckInInsertControl()
        self.seq = SeqInfo()
        self.detail = DetailInfo()
        self.course = CourseInfo()
        self.stu = StuInfo()
        self.sum = SumInfo()
        print "教师手工考勤菜单"

    def Form(self):
        """
        教师的输入菜单
        系统请求教师输入微信号
        系统判定是否存在
        存在：打印该教师的课头
        系统请求教师选择一课头
        系统请求教师选择增加手工考勤或修改手工考勤
        系统请求教师输入考勤记录及考勤次序号
        系统判断教师输入内容是否存在
        存在：执行手工考勤类TecManCheckInInsertControl()中的方法
        增加考勤执行tec_man_add（）方法
        修改考勤执行tec_man_update方法
        :return: 
        """
        pass

if __name__ == "__main__":
    t = TecManCheckInForm()
    t.Form()
