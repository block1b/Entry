# coding=utf8
from courseinfo import CourseInfo
from stuinfo import StuInfo
from timewindows import TimeWindows


# 考勤对象类
class CheckInInfo(object):
    def __init__(self, tec_id, course_id, course_filename, stu_filename):
        self.course = CourseInfo()
        self.stu = StuInfo()
        self.tim = TimeWindows()
        self.section = self.tim.get_now_section()
        self.tecid = tec_id
        self.courseid = course_id
        self.classnames = self.get_checkin_classnames(tec_id, course_id, course_filename)
        self.stuids = self.get_checkin_stuids(self.classnames, stu_filename)
        self.seqid = str(self.tim.get_now_section())
        self.starttime = self.tim.get_time2()
        self.sampletime = ""

    # 获取待考勤班级s，待考勤学生s
    # 获取待考勤班级s
    def get_checkin_classnames(self, teacher_id, course_id, course_filename):
        # 所有的课程信息
        all_course_info = self.course.get_all_course_info(course_filename)
        # 所需课程信息
        a_teacher_course_infos = self.course.get_course_info_from_teacher_id(teacher_id, all_course_info)
        # 所需班级集合
        classnames = self.course.get_classnames(course_id, teacher_id, a_teacher_course_infos)
        return classnames

    # 获取待考勤学生s
    def get_checkin_stuids(self, classnames, stu_filename):
        # 所有学生信息
        all_stu_info = self.stu.get_all_stu_info(stu_filename)
        # 待考勤学生信息
        wait_checkin_stu_info = self.stu.get_wait_checkin_stu_info(classnames, all_stu_info)
        # 待考勤学生id集合
        stuids = self.stu.get_stuids(wait_checkin_stu_info)
        return stuids


if __name__ == "__main__":
    TECID = "2004643"
    COURSEID = "51610145"
    COURSEFILENAME = "../internal/courseProgress.csv"
    STUFILENAME = "../internal/studentInfo.csv"
    c = CheckInInfo(TECID, COURSEID, COURSEFILENAME, STUFILENAME)
    print c.section
