# coding=utf8
from base_file import BaseFile


class TecInfo(BaseFile):
    def __init__(self):
        pass

    # 获得所有教师信息
    def get_all_teacher_info(self, teacher_filename):
        all_teacher_info = self.read_file(teacher_filename, 'rb')
        return all_teacher_info

    # 教师id集合
    def get_teacher_ids(self, all_teacher_info):
        teacher_ids = []
        for teacher_info in all_teacher_info:
            teacher_ids.append(teacher_info["TeacherID"])
        return teacher_ids

    # 验证教师是否存在
    def teacher_exist(self, teacher_id, teacher_ids):
        if teacher_id in teacher_ids:
            return True
        else:
            return False

    # 通过微信号查找该教师信息
    def get_teacher_id_where_wechat_id(self, wechat_id, all_teacher_info):
        for teacher_info_line in all_teacher_info:
            if teacher_info_line["WeChatID"] == wechat_id:
                return teacher_info_line
        return 

