# coding=utf8
from SeqInfo import SeqInfo
from DetailInfo import DetailInfo
from CourseInfo import CourseInfo
from StuInfo import StuInfo
from SumInfo import SumInfo
import time


class TecManCheckInInsertControl(object):

    def __init__(self):
        self.seq = SeqInfo()
        self.detail = DetailInfo()
        self.course = CourseInfo()
        self.stu = StuInfo()
        self.sum = SumInfo()
    # 从菜单获得tecid,courseid,stucheckinresults.

    # 获取当前系统时间
    def get_time(self):
        """
        获取系统当前的时间
        :return: 
        """
        return time.strftime("%Y-%m-%d %X", time.localtime())

    # 教师手工增加考勤操作三个表
    def tec_man_add(self, teacher_id, course_id, stu_checkin_result_form):
        # 在seq表中添加记录
        # 默认seq文件路径
        SEQFILENAME = "../internal/seq.csv"
        # 获取seq表已有信息
        all_seq_info = self.seq.get_all_seq_info(SEQFILENAME)
        # 分配新的考勤次序号
        seq_id = self.seq.get_seqid(teacher_id, course_id, all_seq_info) + 1
        # 构建新的考勤次序记录
        new_sql_line = self.seq.set_seq_line(teacher_id, course_id, str(seq_id), self.get_time())
        # 将新的考勤记录加入seq表
        all_seq_info = self.seq.seq_update(new_sql_line, all_seq_info)

        # 创建detail表
        # 构建detail文件名
        new_detail_filename = self.detail.set_detail_filename(teacher_id, course_id, str(seq_id))
        # 所有的课程信息
        COURSEFILENAME = "../internal/courseProgress.csv"
        all_course_info = self.course.get_all_course_info(COURSEFILENAME)
        # 所需课程信息
        a_teacher_course_infos = self.course.get_course_info_from_teacher_id(teacher_id, all_course_info)
        # 所需班级集合
        classnames = self.course.get_classnames(course_id, teacher_id, a_teacher_course_infos)
        # 所有学生信息
        STUFILENAME = "../internal/studentInfo.csv"
        all_stu_info = self.stu.get_all_stu_info(STUFILENAME)
        # 待考勤学生信息
        wait_checkin_stu_info = self.stu.get_wait_checkin_stu_info(classnames, all_stu_info)
        # 待考勤学生id集合
        stuids = self.stu.get_stuids(wait_checkin_stu_info)
        # 初始化detail表
        newdetail_info = []
        for stuid in stuids:
            newdetail_line = \
                self.detail.set_detail_line(stuid, self.get_time(),
                                            self.detail.set_proofpath(stuid, course_id, str(seq_id), self.get_time()),
                                            "man", "null", "in")
            newdetail_info.append(newdetail_line)

        # 录入考勤情况
        all_detaile_info = self.detail.detail_update(stu_checkin_result_form, newdetail_info)

        # 生成sum表
        # 获取sum表文件名
        sum_filename = self.sum.set_sum_filename(teacher_id, course_id)
        # 初始化sum表
        new_sum_info = self.sum.sum_creat(stuids)
        # 获取sum信息
        sum_filename = "../internal/2004643_51610145_sum.csv"
        all_sum_info = self.sum.get_all_sum_info(sum_filename)
        # 录入考勤汇总
        all_stu_info = self.sum.sum_update(stu_checkin_result_form, all_sum_info, str(seq_id))
        # 写入文件

    # 教师手工修改三个表
    def tec_man_update(self, teacher_id, course_id, seq_id, stu_checkin_result_form):

        # 创建detail表
        # 构建detail文件名
        new_detail_filename = self.detail.set_detail_filename(teacher_id, course_id, str(seq_id))
        # 获取detail表已有信息
        detail_info = self.detail.get_all_detail_info("../internal/2004643_51610145_01_checkinDetail.csv")
        # 录入考勤情况
        all_detaile_info = self.detail.detail_update(stu_checkin_result_form, detail_info)
        # 写入文件

        # 生成sum表
        # 获取sum表文件名
        sum_filename = self.sum.set_sum_filename(teacher_id, course_id)
        # 获取sum信息
        sum_filename = "../internal/2004643_51610145_sum.csv"
        all_sum_info = self.sum.get_all_sum_info(sum_filename)
        # 录入考勤汇总
        all_stu_info = self.sum.sum_update(stu_checkin_result_form, all_sum_info, str(seq_id))
        # 写入文件

    # 将三个表写入文件 弃，逻辑上应在上一个文件保存成功后，再进行下一个文件的构造
    def write_to_file(self, sql_data, detail_data, sum_data):
        self.seq.write_seq(sql_data, "../internal/demofile_seq.csv")
        self.detail.write_detail(detail_data, "../internal/demofile_detail.csv")
        self.sum.write_sum(sum_data, "../internal/demofile_sum.csv")

    # 教师处理假条
    def tec_handle_leave(self, tec_id, course_id, seq_id):
        pass

if __name__ == "__main__":
    TEACHERID = "2004344"
    COURSEID = "51610134"
    # 修改考勤信息
    MANATTENDANCEINFO = [
        {"StuID": "201416920128", "CheckinResult": "no"},
        {"StuID": "201416920105", "CheckinResult": "no"}
    ]
    t = TecManCheckInInsertControl()
    t.tec_man_add(TEACHERID, COURSEID, MANATTENDANCEINFO)
    t.tec_man_update(TEACHERID, COURSEID, 1, MANATTENDANCEINFO)
    print "succed"
