# coding=utf8
from base_import import BaseImport


class StuInfo(BaseImport):
    def __init__(self):
        pass

    # 获取所有学生信息
    def get_all_stu_info(self, stu_filename):
        all_stu_info = self.read_file(stu_filename)
        return all_stu_info

    # 以stuid获取ClassID
    def get_classid(self, stu_id, all_stu_info):
        for stu_info_line in all_stu_info:
            if stu_id == stu_info_line["StuID"]:
                return stu_info_line["ClassID"]
        return False

    # 获取所有本次需要参加考勤的学生信息
    def get_wait_checkin_stu_info(self, classnames, all_stu_info):
        wait_stu_info = []
        for stu_info_line in all_stu_info:
            if stu_info_line["ClassID"] in classnames:
                wait_stu_info.append(stu_info_line)

        return wait_stu_info

    # 获取学生id集合
    def get_stuids(self, wait_stu_info):
        stu_ids = []
        for stu_info_line in wait_stu_info:
            stu_ids.append(stu_info_line["StuID"])

        return stu_ids

    # 验证输入的stu_id是否存在
    def stuid_exist(self, stu_id, stu_ids):
        if stu_id in stu_ids:
            return True
        else:
            return False
