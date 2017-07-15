# coding=utf8
from suminfo import SumInfo
from updatesum import UpdateSum
import os


class ShowSum(object):
    def __init__(self):
        self.sum = SumInfo()
        self.updatesum = UpdateSum()
        # 更新sum表
        SEQFILENAME = "../outputdemo/seq.csv"
        COURSEFILENAME = "../internal/courseProgress.csv"
        STUFILENAME = "../internal/studentInfo.csv"
        self.updatesum.update_all_sum(COURSEFILENAME, STUFILENAME, SEQFILENAME)

    # 某人所有次考勤记录
    def show_one_stu_all_checks(self, tec_id, course_id, stu_id):
        sumfilename = self.sum.set_sum_filename(tec_id, course_id)
        if os.path.exists(sumfilename):
            all_sum_info = self.sum.get_all_sum_info(sumfilename)
            all_keys = all_sum_info[0].keys()
            print "***  教师 " + tec_id + " 课程 " + course_id + "学生" + stu_id + " 的考勤汇总 ***"
            for key in all_keys:
                print "%-10s" % key,
            print ""
            for sum_line in all_sum_info:
                if sum_line["StuID"] == stu_id:
                    for key in sum_line:
                        print "%-10s" % sum_line[key],
                    print ""
            return True
        else:
            print "输入有误，请检查后重新操作"

    # 某次所有人考勤记录
    def show_one_check_all_stus(self, tec_id, course_id, seq_id):
        sumfilename = self.sum.set_sum_filename(tec_id, course_id)
        if os.path.exists(sumfilename):
            all_sum_info = self.sum.get_all_sum_info(sumfilename)
            all_keys = all_sum_info[0].keys()
            print "***  教师 " + tec_id + " 课程 " + course_id + "第" + seq_id + " 次的考勤汇总 ***"
            print "%-10s%-10s" % ("StuID", "Checkin" + seq_id)  # "  **  StuID  **  **  Checkin" + seq_id
            for sum_line in all_sum_info:
                print "%-10s%-10s" % (sum_line["StuID"], sum_line["Checkin" + seq_id])
            return True
        else:
            print "输入有误，请检查后重新操作"

    # 完整sum表
    def show_all_stu_all_check(self, tec_id, course_id):
        sumfilename = self.sum.set_sum_filename(tec_id, course_id)
        if os.path.exists(sumfilename):
            all_sum_info = self.sum.get_all_sum_info(sumfilename)
            all_keys = all_sum_info[0].keys()
            print "***  教师 " + tec_id + " 课程 " + course_id + " 的考勤汇总 ***"
            for key in all_keys:
                print "%-10s" % key,
            print ""
            for sum_line in all_sum_info:
                for key in sum_line:
                    print "%-10s" % sum_line[key],
                print ""
            return True
        else:
            print "输入有误，请检查后重新操作"

if __name__ == "__main__":
    s = ShowSum()
    TECID = "2004001"
    COURSEID = "51610101"
    SEQID = "2"
    STUID = "201516920101"
    s.show_all_stu_all_check(TECID, COURSEID)
    s.show_one_stu_all_checks(TECID, COURSEID, STUID)
    s.show_one_check_all_stus(TECID, COURSEID, SEQID)
