# coding=utf8
from base_file import BaseFile


class CourseInfo(BaseFile):
    def __init__(self):
        pass

    # 获取所有课程信息
    def get_all_course_info(self, course_filename):
        all_course_info = self.read_file(course_filename, 'rb')
        return all_course_info

    # 获取某教师的所有课程信息
    def get_course_info_from_teacher_id(self, teacher_id, all_course_info):
        a_teacher_course_infos = []
        for course_info_line in all_course_info:
            if course_info_line["TeacherID"] == teacher_id:
                a_teacher_course_infos.append(course_info_line)

        return a_teacher_course_infos

    # 获取课头名集合
    def get_course_names(self, a_teacher_course_infos):
        course_names = []
        course_names2 = []
        for course_info_line in a_teacher_course_infos:
            course_names.append(course_info_line["CourseName"])
        [course_names2.append(i) for i in course_names if not i in course_names2]
        return course_names2

    # 获取课头id集合
    def get_course_ids(self, a_teacher_course_infos):
        course_ids = []
        course_ids2 = []
        for course_info_line in a_teacher_course_infos:
            course_ids.append(course_info_line["CourseID"])
        [course_ids2.append(i) for i in course_ids if not i in course_ids2]
        return course_ids2

    # 将课程信息内的coursename做keys,courseis做values，做枚举效果的字典
    def set_course_enum(self, a_teacher_course_infos):
        course_enum = {}
        for course_info_line in a_teacher_course_infos:
            course_enum.update({course_info_line["CourseName"]: course_info_line["CourseID"]})

        return course_enum

    # 验证教师输入的课头是否存在
    def courseid_exist(self, course_id, course_ids):
        if course_id in course_ids:
            return True
        else:
            return False

    # 获取本次考勤的学生班级集合
    def get_classnames(self, course_id, teacherid, a_teacher_course_infos):
        classnames = []
        for course_info_line in a_teacher_course_infos:
            if course_info_line["CourseID"] == course_id and course_info_line["TeacherID"] == teacherid:
                classnames.append(course_info_line["ClassName"])

        return classnames
