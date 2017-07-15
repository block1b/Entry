# coding=utf8
from base_file import BaseFile
from suminfo import SumInfo
import time
import datetime


class DetailInfo(BaseFile):
    def __init__(self):
        pass

    # detail文件名构建
    def set_detail_filename(self, teacherID, courseID, seqID, default_path="../outputdemo/"):
        detail_filename = default_path + teacherID + "_" + courseID + "_" + seqID + "_checkinDetail.csv"  # 按要求seqID应为双数，暂时忽略吧。
        return detail_filename

    # 获取detail表信息
    def get_all_detail_info(self, detail_filename):
        all_detail_info = self.read_file(detail_filename)
        return all_detail_info

    # proofpath内容构建 （checkintime中间有空格作为文件名可能有误，注意）
    def set_proofpath(self, stuID, courseID, seqID, checkintime):
        proofpath = "D:/Proof/" + stuID + "_" + courseID + "_" + seqID + "_" + checkintime + ".jpg"
        return proofpath

    # detail表构造行数据
    def set_detail_line(self, stuID, checkintime, proofpath, checkintype, issucc, checkinresult):
        detail_line = {"StuID": stuID,
                       "CheckinTime": checkintime,
                       "ProofPath": proofpath,
                       "CheckinType": checkintype,
                       "IsSucc": issucc,
                       "CheckinResult": checkinresult
                       }
        return detail_line

    # 将新的detail行加入detail表
    def detail_update(self, detail_lines, all_detail_info):
        all_detail_info += detail_lines

        return all_detail_info

    # 将detailed表写入文件
    def write_detail(self, all_detail_info, detail_filename):
        self.write_file(all_detail_info, detail_filename, "wb")
        return

    # 求时间差
    def get_time_sub(self, date1, date2):
        date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
        date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S")
        date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
        date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
        data3 = (date2 - date1).seconds
        return data3

    # 先将detail每行的result判断
    def set_detail_result(self, detail_line, starttime):
        if detail_line["CheckinType"] == "man":
            pass
        if detail_line["CheckinType"] == "auto":
            if detail_line["IsSucc"] == "False":
                detail_line["CheckinResult"] = "null"
            else:
                # 学生提交时间晚于教师发起时间起0-5
                time_sub = self.get_time_sub(starttime, detail_line["CheckinTime"])
                if time_sub >= 0 and time_sub <= 300:
                    detail_line["CheckinResult"] = "到勤"
                if time_sub > 300:
                    detail_line["CheckinResult"] = "迟到"
        if detail_line["CheckinType"] == "sample":
            if detail_line["IsSucc"] == "True":
                detail_line["CheckinResult"] = "到勤"
            else:
                detail_line["CheckinResult"] = "null"

    # 获得detail表的统计结果stu_checkin_result
    def detail_sum(self, all_detail_info, stuids, seqid):
        new_sum_info = []
        for stuid in stuids:
            # 默认缺勤
            sum_line = {"StuID": stuid, "Checkin" + seqid: "缺勤"}
            for a_detail_line in all_detail_info:
                # step2：该学生的记录
                if a_detail_line["StuID"] == stuid:
                    # 跟新CheckinResult
                    if a_detail_line["CheckinResult"] != "null":
                        sum_line.update({"Checkin" + seqid: a_detail_line["CheckinResult"]})
                    else:
                        pass  # 无结果弃

            new_sum_info.append(sum_line)
        return new_sum_info


if __name__ == "__main__":
    # 算法演示
    d = DetailInfo()
    TECID = "2004643"
    COURSEID = "51610145"
    DETAILFAILENAME = "../outputdemo/" + TECID + "_" + COURSEID + "_1_checkinDetail.csv"
    SUMFAILENAME = "../outputdemo/" + TECID + "_" + COURSEID + "_sum.csv"
    print DETAILFAILENAME
    all_detail_info = d.get_all_detail_info(DETAILFAILENAME)
    print all_detail_info
    stuids = ['201416920104', '201416920405', '201416920217', '201416920105', '201416920102']
    print stuids
    # step1
    STARTTIME = "2017-05-26 19:54:20"
    for detail_line in all_detail_info:
        d.set_detail_result(detail_line, STARTTIME)
    # detail转sum算法setp2
    new_sum_info = d.detail_sum(all_detail_info, stuids, "1")
    print new_sum_info
    # 将转化后的结果写入sum文件
    s = SumInfo()
    all_sum_info = s.sum_creat(stuids)
    print all_sum_info
    all_sum_info = s.sum_update(new_sum_info, all_sum_info, "Checkin1")
    print all_sum_info
    s.write_file(all_sum_info, SUMFAILENAME)
