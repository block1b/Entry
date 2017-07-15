# coding=utf8
from seqinfo import SeqInfo
from courseinfo import CourseInfo
from stuinfo import StuInfo
from suminfo import SumInfo
from detailinfo import DetailInfo
import os


class UpdateSum(object):
    def __init__(self):
        self.seq = SeqInfo()
        self.course = CourseInfo()
        self.stu = StuInfo()
        self.sum = SumInfo()
        self.detail = DetailInfo()

    # 传入参数 tec_id, course_id, seq_id
    # 从seq表中获取本次的starttime, 需要附加文件名，seq_filename
    # 获取所有学生的名单，需要附加文件名，course_filename,stu_filename
    # 通过detail类的两个方法获得所有学生的考勤结果
    # 获取sum表的文件名
    # 若seq_id==1，需要初始化sum表
    # 按学生考勤结果更新入sum表
    def update_sum(self, tec_id, course_id, seq_id, course_filename, stu_filename, seq_filename):
        starttime = self.get_tec_start_time(tec_id, course_id, seq_id, seq_filename)
        stuids = self.get_all_stuids(tec_id, course_id, course_filename, stu_filename)
        sumfilename = self.sum.set_sum_filename(tec_id, course_id)
        if starttime and stuids and sumfilename:
            # 获得所有学生的考勤结果
            detail_filename = self.detail.set_detail_filename(tec_id, course_id, seq_id)
            all_detail_info = self.detail.get_all_detail_info(detail_filename)
            for detail_line in all_detail_info:
                self.detail.set_detail_result(detail_line, starttime)
            new_sum_line = self.detail.detail_sum(all_detail_info, stuids, seq_id)

            # 更新sum
            if os.path.exists(sumfilename):
                pass
            else:
                # 初始化sum表
                new_sum_info = self.sum.sum_creat(stuids)
                self.sum.write_file(new_sum_info, sumfilename)
            all_sum_info = self.sum.get_all_sum_info(sumfilename)
            new_sum_info = self.sum.sum_update(new_sum_line, all_sum_info, seq_id)
            self.sum.write_file(new_sum_info, sumfilename)
        else:
            print "您输入的内容有误，请检查后重新操作"

    # 获取教师发起考勤时间
    def get_tec_start_time(self, tec_id, course_id, seq_id, seq_filename):
        all_seq_info = self.seq.get_all_seq_info(seq_filename)
        if self.seq.check_seq_id(tec_id, course_id, seq_id, all_seq_info):
            start_time = self.seq.get_start_time(tec_id, course_id, seq_id, all_seq_info)
            if start_time:
                return start_time
            else:
                return None
        else:
            print "您输入的考勤次序号错误"
            return None

    # 获取所有学生的名单
    def get_all_stuids(self, tec_id, course_id, course_filename, stu_filename):
        all_course_info = self.course.get_all_course_info(course_filename)
        classnums = self.course.get_classnames(tec_id, course_id, all_course_info)
        all_stu_info = self.stu.get_all_stu_info(stu_filename)
        stu_ids = self.stu.get_stuids(self.stu.get_wait_checkin_stu_info(classnums, all_stu_info))
        if stu_ids:
            return stu_ids
        else:
            return None

    # 遍历seq表，获取所有detail表，更新sum表
    def update_all_sum(self, COURSEFILENAME, STUFILENAME, SEQFILENAME):
        all_seq_info = self.seq.get_all_seq_info(SEQFILENAME)
        for seq_line in all_seq_info:
            tec_id = seq_line["TeacherID"]
            course_id = seq_line["CourseID"]
            seq_id = seq_line["SeqID"]
            self.update_sum(tec_id, course_id, seq_id, COURSEFILENAME, STUFILENAME, SEQFILENAME)


if __name__ == "__main__":
    u = UpdateSum()
    # 2004344,51610134,2,2017-07-07 16:20:48
    TECID = "2004344"
    COURSEID = "51610134"
    SEQID = "1"
    SEQFILENAME = "../outputdemo/seq.csv"
    COURSEFILENAME = "../internal/courseProgress.csv"
    STUFILENAME = "../internal/studentInfo.csv"
    start_time = u.get_tec_start_time(TECID, COURSEID, SEQID, SEQFILENAME)
    print start_time
    stuids = u.get_all_stuids(TECID, COURSEID, COURSEFILENAME, STUFILENAME)
    print stuids
    # u.update_sum(TECID, COURSEID, SEQID, COURSEFILENAME, STUFILENAME, SEQFILENAME)
    u.update_all_sum(COURSEFILENAME, STUFILENAME, SEQFILENAME)
