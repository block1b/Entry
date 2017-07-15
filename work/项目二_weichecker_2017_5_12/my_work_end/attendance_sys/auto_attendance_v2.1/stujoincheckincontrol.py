# coding=utf8
from checkininfo import CheckInInfo
from detailinfo import DetailInfo
from iniinfo import IniInfo
import time


class StuJoinCheckInControl(object):
    def __init__(self):
        self.detail = DetailInfo()

    # 获取当前系统时间
    def get_time(self):
        """
        获取系统当前的时间
        :return: 
        """
        return time.strftime("%Y-%m-%d %X", time.localtime())

    # 学生签到（stu_id, proof）
    # 查找该学生所属的考勤对象
    def get_checkininfo(self, stu_id, cii_list):
        for acia in cii_list:
            if stu_id in acia.stuids:
                return acia
        return

    # 构造detail_line信息
    def set_new_detail_line(self, stuid, acii, result="wait"):
        newdetail_line = \
            self.detail.set_detail_line(stuid, self.get_time(),
                                        self.detail.set_proofpath(stuid, acii.courseid, acii.seqid,
                                                                  self.get_time()),
                                        "auto", "null", result)
        return newdetail_line

    # 提交/请假（result="wait"/"qj"）
    def stu_send_checkininfo(self, stuid, result, cii_list, default_path):
        now_cii = self.get_checkininfo(stuid, cii_list)  # 这里应当做考勤对象是否存在的判断
        if now_cii:
            new_detail_line = self.set_new_detail_line(stuid, now_cii, result)
            # 构建detail文件名
            teacher_id = now_cii.tecid
            course_id = now_cii.courseid
            seq_id = now_cii.seqid
            new_detail_filename = default_path + self.detail.set_detail_filename(teacher_id, course_id, seq_id)
            all_detail_info = self.detail.get_all_detail_info(new_detail_filename)
            all_detail_info.append(new_detail_line)
            self.detail.write_detail(all_detail_info, new_detail_filename)
        else:
            print "error"


if __name__ == "__main__":
    TECID = "2004643"
    COURSEID = "51610145"
    COURSEFILENAME = "../internal/courseProgress.csv"
    STUFILENAME = "../internal/studentInfo.csv"
    SEQFILENAME = "../outputdemo/seq.csv"
    DEFAULTPATH = "../outputdemo/"
    STUID = "201416920101"
    c = CheckInInfo(TECID, COURSEID, COURSEFILENAME, STUFILENAME, SEQFILENAME)

    print c.tecid
    print c.courseid
    print c.seqid
    print c.starttime
    print c.classnames
    print c.stuids
    cii_arry = [c]
    s = StuJoinCheckInControl()
    s.stu_send_checkininfo(STUID, "请假", cii_arry, DEFAULTPATH)