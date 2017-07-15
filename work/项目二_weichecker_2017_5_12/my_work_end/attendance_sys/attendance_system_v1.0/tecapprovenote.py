# coding=utf8
from seqinfo import SeqInfo
from courseinfo import CourseInfo
from stuinfo import StuInfo
from detailinfo import DetailInfo
import time


class TecApproveNote(object):
    def __init__(self):
        self.course = CourseInfo()
        self.stu = StuInfo()
        self.seq = SeqInfo()
        self.detail = DetailInfo()

    # 审批假条
    def approve_note(self, tec_id, course_id, seq_id, stu_ids, seq_filename, default_path):
        if self.check_seqid(tec_id, course_id, seq_id, seq_filename):
            if self.check_stuids(tec_id, course_id, seq_id, stu_ids, default_path):
                new_detail_info = self.build_detail(stu_ids)
                detail_filename = self.detail.set_detail_filename(tec_id, course_id, str(seq_id))
                detail_filename = default_path + detail_filename
                self.update_detail(new_detail_info, detail_filename)
            else:
                print "有学生非本班学生，请检查后重新操作"
        else:
            print "没有您选择的考勤序号，请检查后重新输入"

    # 获取当前系统时间
    def get_time(self):
        """
        获取系统当前的时间
        :return: 
        """
        return time.strftime("%Y-%m-%d %X", time.localtime())

    # 1.检查seqid有效性
    def check_seqid(self, tec_id, course_id, seq_id, seq_filename):
        # 通过获取最大seqid值验证当前输入的seqid值是否有效
        all_seq_info = self.seq.get_all_seq_info(seq_filename)
        max_seqid = self.seq.get_seqid(tec_id, course_id, all_seq_info)
        if int(seq_id) > 0 and int(seq_id) <= int(max_seqid):
            return True
        else:
            return False

    # 检查输入的学生的有效性
    def check_stuids(self, tec_id, course_id, seq_id, stu_ids, default_path):
        # 通过获取该考勤对象的学生集合，判断输入的学号是否有效
        detail_filename = self.detail.set_detail_filename(tec_id, course_id, seq_id)
        detail_filename = default_path + detail_filename
        all_stuids = self.note_stu_ids(detail_filename)
        for a_stuid in stu_ids:
            if a_stuid in all_stuids:
                pass
            else:
                return False
        return True

    # 2.打印请假学生
    def show_note_stuids(self, tec_id, course_id, seq_id, seq_filename, default_path):
        all_seq_info = self.seq.get_all_seq_info(seq_filename)
        max_seqid = self.seq.get_seqid(tec_id, course_id, all_seq_info)
        if int(seq_id) > 0 and int(seq_id) <= int(max_seqid):
            detail_filename = self.detail.set_detail_filename(tec_id, course_id, seq_id)
            detail_filename = default_path + detail_filename
            note_stuids = self.note_stu_ids(detail_filename)
            return note_stuids
        else:
            print "您输入选择的seqid错误，请检查后重新操作"

    # 请假学生
    def note_stu_ids(self, detail_filename):
        stuids = []
        all_detail_info = self.detail.get_all_detail_info(detail_filename)
        for a_detail_line in all_detail_info:
            if a_detail_line["CheckinResult"] == "请假":
                stuids.append(a_detail_line["StuID"])
            else:
                pass
        return stuids

    # 3.将审批通过的记录计入detail表
    def update_detail(self, new_detail_info, detail_filename):
        self.detail.write_file(new_detail_info, detail_filename, 'ab')

    # 构造detail数据
    def build_detail(self, stu_ids):
        new_detail_info = []
        for a_person in stu_ids:
            new_detail_info.append(
                self.detail.set_detail_line(
                    a_person, self.get_time(), "null", "man", "null", "请假通过"))
        return new_detail_info

if __name__ == "__main__":
    tec_id = "2004344"
    course_id = "51610134"
    seq_id = "1"
    stu_ids = ["201416920101", "201416920102", "201416920104"]
    SEQFILENAME = "../outputdemo/seq.csv"
    DEFAULTPATH = "../outputdemo/"
    # approve_note(self, tec_id, course_id, seq_id, stu_ids, seq_filename)
    tecapprove = TecApproveNote()
    tecapprove.approve_note(tec_id, course_id, seq_id, stu_ids, SEQFILENAME, DEFAULTPATH)
