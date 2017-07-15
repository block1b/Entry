# coding=utf8
from base_import import BaseImport
import time


class ManAttendance(BaseImport):
    columns = [1]

    def __init__(self):
        pass

    # 教师集合
    def teacherIDs(self, teacher_filename):
        """
        得到所有的教师
        :param teacher_filename: 
        :return: 
        """
        all_teacher_info = self.read_file(teacher_filename, 'rb')
        teacherids = []
        for teacher_info in all_teacher_info:
            teacherids.append(teacher_info["TeacherID"])
        return teacherids


    # 课头id集合
    def courseIDs(self, teacherID, course_filename):
        """
        得到该教师在课程表中的所有课头
        :param teacherID: 
        :param course_filename: 
        :return: 
        """
        course_info = self.read_file(course_filename, 'rb')
        courseids = []  # 课头集合
        for course_line in course_info:
            if course_line["TeacherID"] == teacherID:
                courseids.append(course_line["CourseID"])

        return courseids

    # classnums考勤班级集合
    def classnums(self, teacherID, courseID, course_filename):
        """
        得到该上教师该门课的所有班级
        :param teacherID: 
        :param courseID: 
        :param course_filename: 
        :return: 
        """
        course_info = self.read_file(course_filename, 'rb')
        classnums = []  # 课头集合
        for course_line in course_info:
            if course_line["TeacherID"] == teacherID and course_line["CourseID"] == courseID:
                classnums.append(course_line["ClassName"])

        return classnums

    # 需签到的学生集合
    def stuIDs(self, classnums, student_filename):
        """
        得到待考勤的所有班级内的所有学生
        :param classnums: 
        :param student_filename: 
        :return: 
        """
        all_studentinfo = self.read_file(student_filename, "rb")
        stuids = []
        for stu_line in all_studentinfo:
            if stu_line["ClassID"] in classnums:
                stuids.append(stu_line["StuID"])
        return stuids

    # seqID计算
    def seq_id_build(self, teacherID, courseID, seqfilename):
        all_seqinfo = self.read_file(seqfilename)
        MAXSEQID = 0
        for seq_line in all_seqinfo:
            if seq_line["TeacherID"] == teacherID and seq_line["CourseID"] == courseID:
                if seq_line["SeqID"] >MAXSEQID:
                    MAXSEQID = seq_line["SeqID"]
        return MAXSEQID

    # seq表增加考勤次序记录
    def seq_line_build(self, teacherID, courseID, seqID, startTime):
        """
        构建seq表的一行数据
        :param teacherID: 
        :param courseID: 
        :param seqID: 
        :param startTime: 
        :return: 
        """
        seq_line = {"TeacherID": teacherID,
                    "CourseID": courseID,
                    "SeqID": seqID,
                    "StartTime": startTime
                    }
        return seq_line

    # detail文件名构建
    def detail_filename_build(self, teacherID, courseID, seqID):
        """
        构建detail表的文件名
        :param teacherID: 
        :param courseID: 
        :param seqID: 
        :return: 
        """
        detail_filename = teacherID + "_" + courseID + "_" + seqID + "_checkinDetail.csv"  # 按要求seqID应为双数，暂时忽略吧。
        return detail_filename

    # proofpath内容构建 （checkintime中间有空格作为文件名可能有误，注意）
    def proofpath_build(self, stuID, courseID, seqID, checkintime):
        """
        构建detail中的proofpath的任容
        :param stuID: 
        :param courseID: 
        :param seqID: 
        :param checkintime: 
        :return: 
        """
        proofpath = "D:/Proof/" + stuID + "_" + courseID + "_" + checkintime + ".jpg"
        return proofpath

    # detail表构造行数据
    def detail_line_build(self, stuID, checkintime, proofpath, checkintype, issucc, checkinresult):
        """
        构建detail中的一行数据
        :param stuID: 
        :param checkintime: 
        :param proofpath: 
        :param checkintype: 
        :param issucc: 
        :param checkinresult: 
        :return: 
        """
        detail_line = {"StuID": stuID,
                       "CheckinTime": checkintime,
                       "ProofPath": proofpath,
                       "CheckinType": checkintype,
                       "IsSucc": issucc,
                       "CheckinResult": checkinresult
                       }
        return detail_line

    # sum 文件名构建
    def sum_filename_build(self, teacherID, courseID):
        """
        构建sum文件名
        :param teacherID: 
        :param courseID: 
        :return: 
        """
        sumfilename = teacherID + "_" + courseID + "_sum.csv"
        return sumfilename

    # CheckinseqID构建
    def checkinseqid_build(self, seqID):
        """
        构建sum中的新表头
        :param seqID: 
        :return: 
        """
        checkinseqid = "Checkin" + seqID
        return checkinseqid

    # sum表行数据更新
    def sum_line_update(self, sum_line, checkinseqid, checkinresult):
        """
        更新sum中的一行数据
        :param sum_line: 
        :param checkinseqid: 
        :param checkinresult: 
        :return: 
        """
        sum_line.update({checkinseqid: checkinresult})
        return sum_line

    # sum表初始化
    def sum_creat(self, stuids):
        """
        初始化sum表
        :param stuids: 
        :return: 
        """
        sum_data = []
        for stuid in stuids:
            sum_data.append({"StuID": stuid})
        return sum_data

    # 获取当前系统时间
    def get_time(self):
        """
        获取系统当前的时间
        :return: 
        """
        return time.strftime("%Y-%m-%d %X", time.localtime())


if __name__ == "__main__":
    print "man attendance work"
    man = ManAttendance()
    # man.__class__.columns = ["TeacherID", "CourseID", "SeqID", "StartTime"]
    # data = [
    #     man.seq_line_build("2004643", "51610145", "01", man.get_time()),
    # ]
    # man.write_file(data, "../internal/seq.csv", "wb")

    # man.__class__.columns = ["StuID", "CheckinTime", "ProofPath", "CheckinType",	"IsSucc", "CheckinResult"]
    # data = [
    #     man.detail_line_build("201416920128", man.get_time(),
    #                           man.proofpath_build("201416920128", "51610145", "01", man.get_time()),
    #                           "man", "True", "in"),
    # ]
    #
    # man.write_file(data, "../internal/" + man.detail_filename_build("2004643", "51610145", "01"), "wb")

    # col = ["StuID"]
    # col.append(man.checkinseqid_build("1"))
    # man.__class__.columns = col
    # index_sum_line = {"StuID": "201416920128"}
    # data = [
    #     man.sum_line_build(index_sum_line, man.checkinseqid_build("1"), "in")
    # ]
    # man.write_file(data, "../internal/" + man.sum_filename_build("2004643", "51610145"), "wb")
