# coding=utf8
from tecinfo import TecInfo
from stuinfo import StuInfo
from tec_form import TecForm
from stu_form import StuForm


class MainForm(object):
    def __init__(self):
        self.log_in()

    # 登录页面
    def log_in(self):
        print "****** 欢迎使用微信考勤系统 ******"
        while 1:
            wei_char = raw_input("请输入您的微信号：")
            role = raw_input("请选择您的身份：1.教师 2.学生 按0.退出：")
            if role == "1":
                tec = TecInfo()
                atec_info = tec.get_teacher_id_where_wechat_id(wei_char,
                                                      tec.get_all_teacher_info("../internal/teacherInfo.csv"))
                if atec_info:
                    now_tecid = atec_info["TeacherID"]
                    print "您的工号为：" + now_tecid
                    print "****** 进入教师菜单 *******"
                    t = TecForm(now_tecid)  # 声明该教师的菜单
                    t.tec_form()
                else:
                    print "该微信号不存在，请检查您的微信号"
            elif role == "2":
                stu = StuInfo()
                astu_info = stu.get_stuinfo_where_wechat_id(wei_char,
                                                            stu.get_all_stu_info("../internal/studentInfo.csv"))
                if astu_info:
                    now_stuid = astu_info["StuID"]
                    print "您的学号为：" + now_stuid
                    print "****** 进入学生菜单 ******"
                    s = StuForm(now_stuid)  # 学生的菜单
                    s.stu_form()
                else:
                    print "该微信号不存在，请检查您的微信号"
            elif role == "0":
                print "欢迎您下次使用本系统，再见。"
                break
            else:
                print "别闹，没有这个选项"
            to_end = raw_input("是否退出本系统？ Y:是 任意键:否 ：")
            if to_end == "Y":
                print "欢迎您下次使用本系统，再见。"
                break
            else:
                pass


if __name__ == "__main__":
    m = MainForm()
    # 主菜单测试数据
    # wonka80
    # wfsf_135
