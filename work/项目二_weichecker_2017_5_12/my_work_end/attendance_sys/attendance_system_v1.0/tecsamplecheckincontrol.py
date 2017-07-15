# coding=utf8
import random
import time
from checkininfo import CheckInInfo
from detailinfo import DetailInfo


# 教师上课抽点
class TecSampleCheckInControl(object):
    def __init__(self):
        self.detail = DetailInfo()

    # 通过tecid查询考勤学生集合
    def get_checkin_stuids(self, tec_id, course_id, checkerin_arry):
        for acii in checkerin_arry:
            if acii.tecid == tec_id and acii.courseid == course_id:
                # 记录抽点时间
                acii.sampletime = self.get_time()
                return acii.stuids
        return

    # 通过tecid查询考勤队列中的该考勤对象
    def get_checker(self, tec_id, course_id, checkerin_arry):
        for acii in checkerin_arry:
            if acii.tecid == tec_id and acii.courseid == course_id:
                return acii
        return

    # 抽取部分学生
    def get_part_stuids(self, all_stuids, percent=5):
        return random.sample(all_stuids, percent)

    # 为抽点学生初始化状态
    # 获取当前系统时间
    def get_time(self):
        """
        获取系统当前的时间
        :return: 
        """
        return time.strftime("%Y-%m-%d %X", time.localtime())

    # 构造detail_line信息
    def set_new_detail_line(self, stuid, acii, result="早退"):
        newdetail_line = \
            self.detail.set_detail_line(stuid, self.get_time(),
                                        self.detail.set_proofpath(stuid, acii.courseid, acii.seqid,
                                                                  self.get_time()),
                                        "man", "null", result)
        return newdetail_line

    # 加入detail文件
    def add_to_detail(self, new_details, now_cii, default_path):
        # 构建detail文件名
        teacher_id = now_cii.tecid
        course_id = now_cii.courseid
        seq_id = now_cii.seqid
        new_detail_filename = default_path + self.detail.set_detail_filename(teacher_id, course_id, seq_id)
        all_detail_info = self.detail.get_all_detail_info(new_detail_filename)
        all_detail_info = self.detail.detail_update(new_details, all_detail_info)
        self.detail.write_detail(all_detail_info, new_detail_filename)

    # 抽点考勤
    def tec_sample_checkin(self, tec_id, course_id, people_num, a_arry):
        # 在考勤队列中到到考勤对象的学生集合，
        check_stuids = self.get_checkin_stuids(tec_id, course_id, a_arry)
        checker = self.get_checker(tec_id, course_id, a_arry)
        if check_stuids and checker:
            print check_stuids
            # 抽取部分学生
            part_stuids = self.get_part_stuids(check_stuids, int(people_num))
            print part_stuids
            # 初始化抽点信息
            part_stus_detail = []
            for a_stuid in part_stuids:
                part_stus_detail.append(self.set_new_detail_line(a_stuid, checker, "早退"))
            # print part_stus_detail
            # 写入detail文件
            self.add_to_detail(part_stus_detail, checker, "../outputdemo/")
        else:
            print "请先开启自助考勤"

if __name__ == "__main__":
    # 抽查演示
    t = TecSampleCheckInControl()
    TECID = "2004643"
    COURSEID = "51610145"
    COURSEFILENAME = "../internal/courseProgress.csv"
    STUFILENAME = "../internal/studentInfo.csv"
    SEQFILENAME = "../outputdemo/seq.csv"
    # 实例考勤对象考勤
    cii = CheckInInfo(TECID, COURSEID, COURSEFILENAME, STUFILENAME)
    print cii.stuids
    a_arry = [cii]
    # 在考勤队列中到到考勤对象的学生集合，
    check_stuids = t.get_checkin_stuids(TECID, a_arry)
    if check_stuids:
        print check_stuids
        # 抽取部分学生
        part_stuids = t.get_part_stuids(check_stuids, 5)
        print part_stuids
        # 初始化抽点信息
        part_stus_detail = []
        for a_stuid in part_stuids:
            part_stus_detail.append(t.set_new_detail_line(a_stuid, cii, "zt"))
        print part_stus_detail
        # 写入detail文件
        t.add_to_detail(part_stus_detail, cii, "../outputdemo/")
    else:
        print "error"
