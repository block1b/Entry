# coding=utf8
from ManAttendance import ManAttendance

if __name__ == "__main__":
    man = ManAttendance()
    TEACHERID = "2004344"
    COURSEID = "51610134"
    teacherids = man.teacherIDs("../internal/teacherInfo.csv")
    # 判断该教师是否存在
    if TEACHERID in teacherids:
        # 打印该教师名下的表头
        courseids = man.courseIDs(TEACHERID, "../internal/courseProgress.csv")
        # print courseids
        # 教师选择一个表头COURSEID
        # 获取上该教师该门课程的班级
        classnums = man.classnums(TEACHERID, COURSEID, "../internal/courseProgress.csv")
        # 获取上该教师该们课程的学生
        stuids = man.stuIDs(classnums, "../internal/studentInfo.csv")

        # 获取现有seq表
        internal_seq = man.read_file("../internal/seq.csv")
        print internal_seq
        # 生成新的seq次序号
        newseqid = man.seq_id_build(TEACHERID, COURSEID, "../internal/seq.csv") + 1
        # 构造新的seq行数据
        newseq_line = man.seq_line_build(TEACHERID, COURSEID, newseqid, man.get_time())
        # 将新的seq行添加到seq表中
        internal_seq.append(newseq_line)
        # print internal_seq

        # 构建/查找detail文件名
        newdetail_filename = man.detail_filename_build(TEACHERID, COURSEID, str(newseqid))
        # 初始化新的detail表(默认全勤)
        newdetail_info = []
        for stuid in stuids:
            newdetail_line = man.detail_line_build(stuid, man.get_time(),
                                  man.proofpath_build(stuid, COURSEID, str(newseqid), man.get_time()),
                                  "man", "null", "in")
            newdetail_info.append(newdetail_line)
        # 修改考勤信息
        MANATTENDANCEINFO = [
            {"StuID": "201416920101", "CheckinResult": "no"},
            {"StuID": "201416920105", "CheckinResult": "no"}
        ]
        # 获取现有detail表
        DEMODETAILFILENAME = "../internal/" + man.detail_filename_build("2004643", "51610145", "01")
        internal_detail_info = man.read_file(DEMODETAILFILENAME)
        # 将MANATTENDANCEINFO修饰为detail行数据样式
        man_detail_info = []
        for manattendanceline in MANATTENDANCEINFO:
            newdetail_line = man.detail_line_build(manattendanceline["StuID"], man.get_time(),
                                                   man.proofpath_build(manattendanceline["StuID"], COURSEID, str(newseqid), man.get_time()),
                                                   "man", "null", manattendanceline["CheckinResult"])
            man_detail_info.append(newdetail_line)
        # 将修改考勤信息导入现有detail表中
        internal_detail_info += man_detail_info

        # 构建/查找sum表名
        newsum_filename = man.sum_filename_build(TEACHERID, COURSEID)
        # 初始化sum表
        newsum_info = man.sum_creat(stuids)
        # 获取现有sum表
        DEMOSUMFILENAME = "../internal/" + man.sum_filename_build("2004643", "51610145")
        internal_sum_info = man.read_file(DEMOSUMFILENAME)
        # 更新sum信息
        DEMOSUMINFO = [
            {"StuID": "201416920128", "CheckinResult": "in"},
            {"StuID": "201416920105", "CheckinResult": "in"}
        ]
        for internal_sun_line in internal_sum_info:
            for demo_sum_line in DEMOSUMINFO:
                if internal_sun_line["StuID"] == demo_sum_line["StuID"]:
                    man.sum_line_update(internal_sun_line, man.checkinseqid_build(str(newseqid)),
                                        demo_sum_line["CheckinResult"])

        # 更新/保存文件
        man.__class__.columns = ["TeacherID", "CourseID", "SeqID", "StartTime"]
        man.write_file(internal_seq, "../internal/demofile_seq.csv")
        man.__class__.columns = ["StuID", "CheckinTime", "ProofPath", "CheckinType", "IsSucc", "CheckinResult"]
        man.write_file(internal_detail_info, "../internal/demofile_detail.csv")
        # 获取sum表的新表头
        col = internal_sum_info[0].keys()
        man.__class__.columns = col
        man.write_file(internal_sum_info, "../internal/demofile_sum.csv")
