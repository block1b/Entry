# coding=utf8


class StuForm(object):
    def __init__(self, stu_id):
        self.stuid = stu_id

    def stu_form(self):
        while 1:
            # 签到，抽到，请假，查询
            print "*************  学生菜单  **************"
            print "************  1.自助签到  *************"
            print "************  2.手工签到  *************"
            print "************  3.请假申请  *************"
            print "************  4.考勤查询  *************"
            print "************  0.退出      *************"
            select = raw_input("请选择功能标号：")
            if select == "1":
                print "***********  进行自助签到  **********"
                print "请输入您的特征信息"
                feature = raw_input("照片：")
                print "您的特征信息为：", feature

            elif select == "2":
                print "***********  进行手工考勤  **********"
                print "请输入您的特征信息"
                feature = raw_input("照片：")
                print "您的特征信息为：", feature

            elif select == "3":
                print "***********  进行请假申请  **********"
                print "请输入您的假条"
                feature = raw_input("照片：")
                print "您的假条为：", feature

            elif select == "4":
                print "***********  进行考勤查询  **********"
                print "您的考勤汇总为：XXX"

            elif select == "0":
                print "退出学生菜单"
                break

            else:
                print "别闹！没有这个选项。"

            to_end = raw_input("是否退出学生菜单？ Y:是 任意键:否 ：")
            if to_end == "Y":
                print "退出学生菜单"
                break
            else:
                pass


if __name__ == "__main__":
    s = StuForm()
    s.stu_form("132456")
