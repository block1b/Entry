# coding=utf8
from checkininfo import CheckInInfo
from checkinarry import CheckInArray
from seqinfo import SeqInfo
from detailinfo import DetailInfo
from courseinfo import CourseInfo
from stuinfo import StuInfo
from suminfo import SumInfo
import time


class TecStartCheckInControl(object):
    # 实例考勤队列
    cia = CheckInArray()

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

    # 初始化seq表
    def creat_seq(self, seq_filename):
        creat_seq_line = [{"TeacherID": None, "CourseID": None, "SeqID": None, "StartTime": None}]
        self.seq.write_file(creat_seq_line, seq_filename)

    # 更新seq表
    def update_seq(self, now_cii, seq_filename):
        # 获取seq表已有信息
        all_seq_info = self.seq.get_all_seq_info(seq_filename)
        # 分配新的考勤次序号
        seq_id = int(self.seq.get_seqid(now_cii.tecid, now_cii.courseid, all_seq_info)) + 1
        now_cii.seqid = str(seq_id)
        # 构建新的考勤次序记录
        new_sql_line = self.seq.set_seq_line(now_cii.tecid, now_cii.courseid, now_cii.seqid, now_cii.starttime)
        # 将新的考勤记录加入seq表
        all_seq_info = self.seq.seq_update(new_sql_line, all_seq_info)
        # 更新seq表
        self.seq.write_file(all_seq_info, seq_filename)
        return

    # 初始化detail表
    def creat_detail(self, now_cii, default_path):
        # 构建detail文件名
        teacher_id = now_cii.tecid
        course_id = now_cii.courseid
        seq_id = now_cii.seqid
        new_detail_filename = default_path + self.detail.set_detail_filename(teacher_id, course_id, seq_id)
        # 待考勤学生id集合
        stuids = now_cii.stuids
        # 初始化detail表
        newdetail_info = []
        for stuid in stuids:
            newdetail_line = \
                self.detail.set_detail_line(stuid, self.get_time(),
                                            self.detail.set_proofpath(stuid, course_id, seq_id, self.get_time()),
                                            "man", "null", "in")
            newdetail_info.append(newdetail_line)
        self.detail.write_file(newdetail_info, new_detail_filename, "wb")

    # 初始化sum表本
    # 导入考勤结果

    # 教师发起自助考勤
    def tec_start_checkin(self, now_cii, seq_filename):
        # 考勤对象家加入考勤队列
        if self.__class__.cia.update_arry(now_cii):
            print "开启成功"
            # 初始化seq表
            # self.creat_seq(seq_filename)  # 有一次即可
            # 在seq表添加记录 !!!只有一行
            self.update_seq(now_cii, seq_filename)
            # 初始化detail表
            default_path = seq_filename[:-7]
            self.creat_detail(now_cii, default_path)
            # 初始化sum表 不应放在这里
        else:
            print "开启失败"

    # 学生签到（stu_id, proof）
    # 查找该学生所属的考勤对象
    def get_checkininfo(self, stu_id, stu_filename):
        # all_stu_info = self.stu.get_all_stu_info(stu_filename)
        # classname = self.stu.get_classid(stu_id, all_stu_info)
        for acia in self.__class__.cia.List:
            if stu_id in acia.stuids:
                return acia
        return

    # 构造detail_line信息
    def set_new_detail_line(self, stuid, acii, result="wait"):
        newdetail_line = \
            self.detail.set_detail_line(stuid, self.get_time(),
                                        self.detail.set_proofpath(stuid, acii.courseid, acii.seqid, self.get_time()),
                                        "auto", "null", result)
        return newdetail_line

    # 提交/请假（result="wait"/"qj"）
    def stu_send_checkininfo(self, stuid, result, stu_filename, default_path):
        now_cii = self.get_checkininfo(stuid, stu_filename)  # 这里应当做考勤对象是否存在的判断
        new_detail_line = self.set_new_detail_line(stuid, now_cii, result)
        # 构建detail文件名
        teacher_id = now_cii.tecid
        course_id = now_cii.courseid
        seq_id = now_cii.seqid
        new_detail_filename = default_path + self.detail.set_detail_filename(teacher_id, course_id, seq_id)
        all_detail_info = self.detail.get_all_detail_info(new_detail_filename)
        all_detail_info.append(new_detail_line)
        self.detail.write_detail(all_detail_info, new_detail_filename)


if __name__ == "__main__":
    t = TecStartCheckInControl()
    TECID = "2004643"
    COURSEID = "51610145"
    COURSEFILENAME = "../internal/courseProgress.csv"
    STUFILENAME = "../internal/studentInfo.csv"
    SEQFILENAME = "../outputdemo/seq.csv"
    # 实例考勤对象考勤
    cii = CheckInInfo(TECID, COURSEID, COURSEFILENAME, STUFILENAME)
    t.tec_start_checkin(cii, SEQFILENAME)
    TECID = "2004644"
    COURSEID = "51610133"
    cii = CheckInInfo(TECID, COURSEID, COURSEFILENAME, STUFILENAME)
    t.tec_start_checkin(cii, SEQFILENAME)
    print t.__class__.cia.List
    STUID = "201416920101"
    # 请假
    t.stu_send_checkininfo(STUID, "qj", STUFILENAME, "../outputdemo/")
    print "stuid 201416920101 in"
