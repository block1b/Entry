# coding=utf8
from seqinfo import SeqInfo
from detailinfo import DetailInfo
from courseinfo import CourseInfo
from stuinfo import StuInfo
from suminfo import SumInfo
import time


class TecManCheckInInsertControl(object):

    def __init__(self):
        self.seq = SeqInfo()
        self.detail = DetailInfo()
        self.course = CourseInfo()
        self.stu = StuInfo()
        self.sum = SumInfo()

    # 获取当前系统时间
    def get_time(self):
        """
        获取系统当前的时间
        :return: 
        """
        return time.strftime("%Y-%m-%d %X", time.localtime())

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

    # 教师手工修改
    def man_change(self, tec_id, course_id, seq_id, stu_id, result, course_filename, stu_filename, seq_filename, default_path):
        # 检查seqid的有效性
        all_seq_info = self.seq.get_all_seq_info(seq_filename)
        new_seqid = self.seq.get_seqid(tec_id, course_id, all_seq_info)
        if int(seq_id) > 0 and int(seq_id) <= new_seqid:
            # 检查stuid的有效性
            all_stuids = self.get_all_stuids(tec_id, course_id, course_filename, stu_filename)
            if all_stuids and stu_id in all_stuids:
                # 构造detail行数据
                new_detail_info = [self.detail.set_detail_line(stu_id, self.get_time(), "null", "man", "null", result)]
                new_filename = self.detail.set_detail_filename(tec_id, course_id, str(seq_id))
                new_filename = default_path + new_filename
                self.detail.write_file(new_detail_info, new_filename, 'ab')
            else:
                print "该学生非本班学生，请检查后重新操作"
        else:
            print "没有您选择的考勤序号，请检查后重新输入"

    # 教师手工考勤控制
    def man_checkin(self, tec_id, course_id, course_filename, stu_filename, arrive, absence, late, early, note,
                    seq_filename, default_path):
        error_ids = self.check_stuids(arrive, absence, late, early, note,
                                      self.get_all_stuids(tec_id, course_id, course_filename, stu_filename))
        if error_ids:
            print "部分名单非本班学生，请检查后重新操作，错误(stuid)名单：", error_ids
        else:
            # 构造手工考勤的detail信息
            new_detail_info = self.build_detail(arrive, absence, late, early, note)
            print "手工考勤记录完成"
            # 1.在seq表中增加记录
            seq_id = self.update_seq_info(tec_id, course_id, seq_filename)
            # 2.在detail表中保存记录
            self.update_detail_info(tec_id, course_id, seq_id, new_detail_info, default_path)

    # 1.在seq表中增加记录
    def update_seq_info(self, tec_id, course_id, seq_filename):
        all_seq_info = self.seq.get_all_seq_info(seq_filename)
        new_seqid = self.seq.get_seqid(tec_id, course_id, all_seq_info) + 1
        new_seq_line = self.seq.set_seq_line(tec_id, course_id, str(new_seqid), self.get_time())
        new_seq_info = [new_seq_line]
        self.seq.write_file(new_seq_info, seq_filename, 'ab')
        return new_seqid

    # 2.在detail表中保存记录
    def update_detail_info(self, tec_id, course_id, seq_id, detail_info, default_path):
        new_filename = self.detail.set_detail_filename(tec_id, course_id, str(seq_id))
        new_filename = default_path + new_filename
        self.detail.write_file(detail_info, new_filename, 'wb')

    # 检查教师输入的学生名单是否在该考勤对象中
    def check_stuids(self, arrive, absence, late, early, note, all_studis):
        # 验证输入的学生名单是否存在与考勤对象，不存在的打印提示错误。
        warning = []
        for a_person in arrive:
            if a_person in all_studis:
                pass
            else:
                warning.append(a_person)

        for a_person in absence:
            if a_person in all_studis:
                pass
            else:
                warning.append(a_person)

        for a_person in late:
            if a_person in all_studis:
                pass
            else:
                warning.append(a_person)

        for a_person in early:
            if a_person in all_studis:
                pass
            else:
                warning.append(a_person)

        for a_person in note:
            if a_person in all_studis:
                pass
            else:
                warning.append(a_person)
        # 若存在非考勤对象名单
        if warning:
            return warning
        else:
            return None

    # 为4中考勤结果的学生构造detail数据
    def build_detail(self, arrive, absence, late, early, note):
        new_detail_info = []
        for a_person in arrive:
            new_detail_info.append(self.detail.set_detail_line(a_person, self.get_time(), "null", "man", "null", "到勤"))

        for a_person in absence:
            new_detail_info.append(self.detail.set_detail_line(a_person, self.get_time(), "null", "man", "null", "缺勤"))

        for a_person in late:
            new_detail_info.append(self.detail.set_detail_line(a_person, self.get_time(), "null", "man", "null", "迟到"))

        for a_person in early:
            new_detail_info.append(self.detail.set_detail_line(a_person, self.get_time(), "null", "man", "null", "早退"))

        for a_person in note:
            new_detail_info.append(self.detail.set_detail_line(a_person, self.get_time(), "null", "man", "null", "请假"))

        return new_detail_info

if __name__ == "__main__":
    t = TecManCheckInInsertControl()
    TECID = "2004001"
    COURSEID = "51610101"
    COURSEFILENAME = "../internal/courseProgress.csv"
    STUFILENAME = "../internal/studentInfo.csv"
    SEQFILENAME = "../outputdemo/seq.csv"
    DEFAULTPATH = "../outputdemo/"
    # arrive, absence, late, early
    arrive = ["201516920101", "201516920104"]
    absence = ["201516920102"]
    late = ["201516920105"]
    early = ["201516920104"]
    note = ["201516920106"]
    # t.man_checkin(TECID, COURSEID, COURSEFILENAME, STUFILENAME, arrive, absence, late, early, note, SEQFILENAME, DEFAULTPATH)
    print "手工考勤成功"
    # (self, tec_id, course_id, seq_id, stu_id, result, course_filename, stu_filename, default_path):
    t.man_change(TECID, COURSEID, "3", "201516920104", "捣蛋", COURSEFILENAME, STUFILENAME, SEQFILENAME, DEFAULTPATH)
    print "手工修改成功"