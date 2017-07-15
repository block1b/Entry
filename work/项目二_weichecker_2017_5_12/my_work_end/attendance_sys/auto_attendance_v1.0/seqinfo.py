# coding=utf8
from base_import import BaseImport


class SeqInfo(BaseImport):
    def __init__(self):
        pass

    # 获取esq表数据
    def get_all_seq_info(self, eql_filename):
        all_seq_info = self.read_file(eql_filename, "rb")
        return all_seq_info

    # 分配考勤次序号
    def get_seqid(self, teacherID, courseID, all_seq_info):
        MAXSEQID = 0
        for seq_line in all_seq_info:
            if seq_line["TeacherID"] == teacherID and seq_line["CourseID"] == courseID:
                line_seq_id = int(seq_line["SeqID"])
                if line_seq_id > MAXSEQID:
                    MAXSEQID = line_seq_id
        return MAXSEQID

    # 构造一条seq记录
    def set_seq_line(self, teacherID, courseID, seqID, startTime):
        new_seq_line = {"TeacherID": teacherID,
                    "CourseID": courseID,
                    "SeqID": seqID,
                    "StartTime": startTime
                    }
        return new_seq_line

    # 将新的seq记录加入seq表
    def seq_update(self, new_seq_line, all_seq_info):
        all_seq_info.append(new_seq_line)
        return all_seq_info

    # 将seq表写入文件
    def write_seq(self, all_seq_info, seq_filename):
        self.write_file(all_seq_info, seq_filename, "wb")
        return

